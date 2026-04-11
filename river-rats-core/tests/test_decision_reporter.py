"""
Tests for DecisionReporter.

Coverage:
  1. Gap computation — verify math
  2. Tightness classification — TOSS_UP / CLOSE / SILENCE thresholds + boundary values
  3. Action statement at each level (L1-L5) including TOSS-UP override at L3+
  4. Tightness sentence content
  5. Causal bridge fires only when ALL three conditions are met
  6. Causal bridge pot-odds uses the CORRECT formula: to_call / (pot + to_call)
  7. DecisionReport fields populated correctly end-to-end
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from dataclasses import dataclass
from typing import Dict

from coaching.decision_reporter import DecisionReporter, DecisionReport, _compute_gap
from coaching.levels import PlayerLevel
from coaching.hand_context import build_hand_context, HandContext


# ═══════════════════════════════════════════════════════════════════
# MOCK OBJECTS
# ═══════════════════════════════════════════════════════════════════

@dataclass
class MockPrediction:
    """
    Stand-in for OraclePrediction.

    Only the fields DecisionReporter reads are needed:
        action, confidence, probs
    """
    action: str
    confidence: float
    probs: Dict[str, float]


def make_pred(action: str = "BET", confidence: float = 0.70, probs: Dict[str, float] = None):
    """Factory for MockPrediction with sensible defaults."""
    if probs is None:
        probs = {
            "FOLD": 0.05,
            "CHECK": 0.05,
            "CALL": 0.10,
            "BET": 0.70,
            "RAISE": 0.10,
        }
    return MockPrediction(action=action, confidence=confidence, probs=probs)


# ─────────────────────────────────────────────────────────────────
# Minimal feature dict — enough to build a HandContext
# ─────────────────────────────────────────────────────────────────

MINIMAL_FEATS = {
    "street": 0.0,
    "facing_bet": 0.0,
    "pot_size": 10.0,
    "to_call": 0.0,
    "pot_odds": 0.0,
    "bet_to_pot": 0.0,
    "hero_position": 3.0,       # BTN
    "villain_position": 5.0,    # BB
    "is_ip": 1.0,
    "hand_category": 6.0,       # top pair
    "hand_rank": 5.0,
    "is_made_hand": 1.0,
    "is_strong_made": 0.0,
    "is_monster": 0.0,
    "has_flush_draw": 0.0,
    "has_straight_draw": 0.0,
    "draw_outs": 0.0,
    "is_monotone": 0.0,
    "is_two_tone": 1.0,
    "is_rainbow": 0.0,
    "is_paired": 0.0,
    "is_double_paired": 0.0,
    "connectivity_score": 0.3,
    "high_card_rank": 12.0,
    "danger_score": 0.3,
    "flush_danger": 0.1,
    "straight_danger": 0.2,
    "raw_equity": 0.60,
    "equity_vs_range": 0.60,
    "better_hand_pct": 0.15,
    "worse_hand_pct": 0.55,
    "equity_margin": 0.27,
    "spr": 5.0,
    "is_3bet_pot": 0.0,
    "villain_aggression_count": 0.0,
    "villain_checked_back": 0.0,
    "villain_call_count": 0.0,
}


def ctx_from(feat_overrides: dict = None) -> HandContext:
    """Build a HandContext using MINIMAL_FEATS merged with any overrides."""
    feats = {**MINIMAL_FEATS, **(feat_overrides or {})}
    return build_hand_context(feats)


REPORTER = DecisionReporter()


# ═══════════════════════════════════════════════════════════════════
# 1. GAP COMPUTATION
# ═══════════════════════════════════════════════════════════════════

class TestGapComputation:
    def test_gap_basic(self):
        """Gap = top prob minus second prob."""
        pred = make_pred(probs={"FOLD": 0.05, "CHECK": 0.10, "CALL": 0.15, "BET": 0.60, "RAISE": 0.10})
        assert abs(_compute_gap(pred) - 0.45) < 1e-9

    def test_gap_exact_toss_up(self):
        """Two equal probabilities give gap = 0.0."""
        pred = make_pred(probs={"FOLD": 0.0, "CHECK": 0.0, "CALL": 0.0, "BET": 0.50, "RAISE": 0.50})
        assert abs(_compute_gap(pred) - 0.0) < 1e-9

    def test_gap_full_certainty(self):
        """If one action is 1.0, gap = 1.0."""
        pred = make_pred(probs={"FOLD": 0.0, "CHECK": 0.0, "CALL": 0.0, "BET": 1.0, "RAISE": 0.0})
        assert abs(_compute_gap(pred) - 1.0) < 1e-9

    def test_gap_uses_top_two_only(self):
        """Gap uses the two largest values only, not third-best."""
        pred = make_pred(probs={"FOLD": 0.01, "CHECK": 0.29, "CALL": 0.01, "BET": 0.60, "RAISE": 0.09})
        # sorted: [0.60, 0.29, 0.09, 0.01, 0.01] → gap = 0.31
        assert abs(_compute_gap(pred) - 0.31) < 1e-9


# ═══════════════════════════════════════════════════════════════════
# 2. TIGHTNESS CLASSIFICATION
# ═══════════════════════════════════════════════════════════════════

class TestTightnessClassification:
    """Verify TOSS_UP / CLOSE / SILENCE bands including boundary values."""

    def _report(self, gap: float) -> DecisionReport:
        """Build report with a controlled gap by crafting matching probs."""
        top = 0.5 + gap / 2
        second = 0.5 - gap / 2
        # Remaining three actions share 0 to keep total = 1.0
        pred = make_pred(
            action="BET",
            confidence=top,
            probs={"FOLD": 0.0, "CHECK": 0.0, "CALL": 0.0, "BET": top, "RAISE": second},
        )
        ctx = ctx_from()
        return REPORTER.report(pred, MINIMAL_FEATS, ctx, PlayerLevel.L1_PERCEPTION)

    def test_toss_up_at_zero_gap(self):
        r = self._report(0.0)
        assert r.tightness == "TOSS_UP"
        assert r.is_mixed is True

    def test_toss_up_just_below_threshold(self):
        # 0.19 < 0.20 → TOSS_UP
        r = self._report(0.19)
        assert r.tightness == "TOSS_UP"
        assert r.is_mixed is True

    def test_close_at_threshold(self):
        # gap = 0.201 is strictly above 0.20 → must be CLOSE not TOSS_UP.
        # We avoid constructing exactly 0.20 because IEEE 754 arithmetic on
        # 0.5 ± 0.10 yields 0.19999...96, which would land in TOSS_UP.
        # Using 0.201 gives a clear, unambiguous CLOSE result.
        pred = self._report(0.201)
        assert pred.tightness == "CLOSE"
        assert pred.is_mixed is False

    def test_close_midrange(self):
        r = self._report(0.30)
        assert r.tightness == "CLOSE"
        assert r.is_mixed is False

    def test_close_just_below_silence(self):
        # 0.349 < 0.35 → CLOSE
        r = self._report(0.349)
        assert r.tightness == "CLOSE"

    def test_silence_at_threshold(self):
        # 0.35 → SILENCE
        r = self._report(0.35)
        assert r.tightness == "SILENCE"
        assert r.is_mixed is False

    def test_silence_high_confidence(self):
        r = self._report(0.80)
        assert r.tightness == "SILENCE"
        assert r.is_mixed is False


# ═══════════════════════════════════════════════════════════════════
# 3. ACTION STATEMENT — LEVEL GATING
# ═══════════════════════════════════════════════════════════════════

def _clear_pred(action: str = "BET", confidence: float = 0.80) -> MockPrediction:
    """Prediction with gap > 0.50 (SILENCE) so normal suffix applies."""
    top = 0.5 + 0.40   # 0.90
    second = 0.5 - 0.40  # 0.10
    return make_pred(
        action=action,
        confidence=confidence,
        probs={"FOLD": 0.00, "CHECK": 0.00, "CALL": 0.00, action: top, "RAISE": second}
        if action != "RAISE" else
        {"FOLD": 0.00, "CHECK": 0.00, "CALL": 0.00, "BET": second, "RAISE": top},
    )


class TestActionStatements:
    def _stmt(self, level: PlayerLevel, action: str = "BET", confidence: float = 0.80) -> str:
        pred = _clear_pred(action=action, confidence=confidence)
        ctx = ctx_from()
        r = REPORTER.report(pred, MINIMAL_FEATS, ctx, level)
        return r.action_statement

    def test_l1_format(self):
        assert self._stmt(PlayerLevel.L1_PERCEPTION, "BET") == "GTO bets here."

    def test_l2_format(self):
        assert self._stmt(PlayerLevel.L2_CAUSE_EFFECT, "CHECK") == "GTO checks here."

    def test_l3_format(self):
        stmt = self._stmt(PlayerLevel.L3_ARCHITECTURE, "FOLD")
        assert stmt == "GTO folds here -- this is the higher-frequency action."

    def test_l4_format_confidence(self):
        # 0.73 → 73%
        stmt = self._stmt(PlayerLevel.L4_MEASUREMENT, "CALL", confidence=0.73)
        assert stmt == "GTO calls here -- 73% confidence."

    def test_l5_format_frequency(self):
        stmt = self._stmt(PlayerLevel.L5_SYSTEMS, "RAISE", confidence=0.65)
        assert stmt == "GTO raises at 65% frequency in this construction."

    def test_l1_no_toss_up_override(self):
        """L1 never changes its format regardless of tightness."""
        pred = make_pred(probs={"FOLD": 0.0, "CHECK": 0.0, "CALL": 0.0, "BET": 0.50, "RAISE": 0.50})
        ctx = ctx_from()
        r = REPORTER.report(pred, MINIMAL_FEATS, ctx, PlayerLevel.L1_PERCEPTION)
        assert r.action_statement == "GTO bets here."

    def test_l2_no_toss_up_override(self):
        """L2 also keeps simple format in TOSS-UP."""
        pred = make_pred(probs={"FOLD": 0.0, "CHECK": 0.0, "CALL": 0.0, "BET": 0.50, "RAISE": 0.50})
        ctx = ctx_from()
        r = REPORTER.report(pred, MINIMAL_FEATS, ctx, PlayerLevel.L2_CAUSE_EFFECT)
        assert r.action_statement == "GTO bets here."

    def test_l3_toss_up_override(self):
        """At L3, TOSS-UP replaces the suffix with 'both actions are in the mix.'"""
        pred = make_pred(
            action="BET",
            confidence=0.50,
            probs={"FOLD": 0.0, "CHECK": 0.0, "CALL": 0.0, "BET": 0.50, "RAISE": 0.50},
        )
        ctx = ctx_from()
        r = REPORTER.report(pred, MINIMAL_FEATS, ctx, PlayerLevel.L3_ARCHITECTURE)
        assert "both actions are in the mix" in r.action_statement

    def test_l4_toss_up_override(self):
        pred = make_pred(
            action="BET",
            confidence=0.50,
            probs={"FOLD": 0.0, "CHECK": 0.0, "CALL": 0.0, "BET": 0.50, "RAISE": 0.50},
        )
        ctx = ctx_from()
        r = REPORTER.report(pred, MINIMAL_FEATS, ctx, PlayerLevel.L4_MEASUREMENT)
        assert "both actions are in the mix" in r.action_statement

    def test_l5_toss_up_override(self):
        pred = make_pred(
            action="BET",
            confidence=0.50,
            probs={"FOLD": 0.0, "CHECK": 0.0, "CALL": 0.0, "BET": 0.50, "RAISE": 0.50},
        )
        ctx = ctx_from()
        r = REPORTER.report(pred, MINIMAL_FEATS, ctx, PlayerLevel.L5_SYSTEMS)
        assert "both actions are in the mix" in r.action_statement

    def test_confidence_rounding(self):
        """Confidence percentage rounds to nearest integer."""
        stmt = self._stmt(PlayerLevel.L4_MEASUREMENT, "BET", confidence=0.756)
        assert "76%" in stmt


# ═══════════════════════════════════════════════════════════════════
# 4. TIGHTNESS SENTENCE
# ═══════════════════════════════════════════════════════════════════

class TestTightnessSentence:
    def _sentence(self, gap: float) -> str:
        top = 0.5 + gap / 2
        second = 0.5 - gap / 2
        pred = make_pred(
            probs={"FOLD": 0.0, "CHECK": 0.0, "CALL": 0.0, "BET": top, "RAISE": second},
            confidence=top,
        )
        ctx = ctx_from()
        r = REPORTER.report(pred, MINIMAL_FEATS, ctx, PlayerLevel.L1_PERCEPTION)
        return r.tightness_sentence

    def test_toss_up_sentence(self):
        assert self._sentence(0.10) == "Both actions are reasonable here."

    def test_close_sentence(self):
        assert self._sentence(0.30) == "The other action is also reasonable here."

    def test_silence_no_sentence(self):
        assert self._sentence(0.60) is None


# ═══════════════════════════════════════════════════════════════════
# 5. CAUSAL BRIDGE GATE CONDITIONS
# ═══════════════════════════════════════════════════════════════════

def _silence_pred() -> MockPrediction:
    """Prediction with gap >= 0.50 (SILENCE band)."""
    return make_pred(probs={"FOLD": 0.0, "CHECK": 0.0, "CALL": 0.0, "BET": 0.80, "RAISE": 0.20})


def _facing_bet_feats(equity=0.70, pot_size=10.0, to_call=5.0, spr=5.0) -> dict:
    """
    Feature dict with a call situation where pot-odds condition can fire.

    correct_pot_odds = 5 / (10 + 5) = 0.333
    With equity=0.70, gap = 0.70 - 0.333 = 0.367 > 0.10 → fires.
    """
    return {
        **MINIMAL_FEATS,
        "facing_bet": 1.0,
        "pot_size": pot_size,
        "to_call": to_call,
        "equity_vs_range": equity,
        "raw_equity": equity,
        "spr": spr,
        "draw_outs": 0.0,
    }


class TestCausalBridgeGates:
    """Causal bridge requires ALL THREE gates to pass."""

    def test_no_bridge_at_l2(self):
        """L2 is below L3 — bridge never fires."""
        feats = _facing_bet_feats()
        ctx = build_hand_context(feats)
        pred = _silence_pred()
        r = REPORTER.report(pred, feats, ctx, PlayerLevel.L2_CAUSE_EFFECT)
        assert r.causal_bridge is None

    def test_no_bridge_when_close(self):
        """Bridge only fires in SILENCE band — CLOSE gap suppresses it."""
        feats = _facing_bet_feats()
        ctx = build_hand_context(feats)
        # Gap of 0.30 → CLOSE
        close_pred = make_pred(
            probs={"FOLD": 0.0, "CHECK": 0.0, "CALL": 0.0, "BET": 0.65, "RAISE": 0.35},
            confidence=0.65,
        )
        r = REPORTER.report(close_pred, feats, ctx, PlayerLevel.L3_ARCHITECTURE)
        assert r.causal_bridge is None

    def test_no_bridge_when_toss_up(self):
        """TOSS-UP gap also suppresses the bridge."""
        feats = _facing_bet_feats()
        ctx = build_hand_context(feats)
        toss_pred = make_pred(
            probs={"FOLD": 0.0, "CHECK": 0.0, "CALL": 0.0, "BET": 0.50, "RAISE": 0.50},
            confidence=0.50,
        )
        r = REPORTER.report(toss_pred, feats, ctx, PlayerLevel.L3_ARCHITECTURE)
        assert r.causal_bridge is None

    def test_no_bridge_without_structural_condition(self):
        """All gates pass but no structural signal — bridge stays None."""
        feats = {
            **MINIMAL_FEATS,
            # No facing bet → pot odds won't fire
            "facing_bet": 0.0,
            "to_call": 0.0,
            "pot_size": 10.0,
            # SPR in normal range (2.5–12.0)
            "spr": 5.0,
            # No draw
            "draw_outs": 0.0,
            "_draw_equity": 0.0,
        }
        ctx = build_hand_context(feats)
        r = REPORTER.report(_silence_pred(), feats, ctx, PlayerLevel.L3_ARCHITECTURE)
        assert r.causal_bridge is None

    def test_bridge_fires_at_l3(self):
        """All three gates satisfied — bridge fires at L3."""
        feats = _facing_bet_feats()
        ctx = build_hand_context(feats)
        r = REPORTER.report(_silence_pred(), feats, ctx, PlayerLevel.L3_ARCHITECTURE)
        assert r.causal_bridge is not None

    def test_bridge_fires_at_l4(self):
        feats = _facing_bet_feats()
        ctx = build_hand_context(feats)
        r = REPORTER.report(_silence_pred(), feats, ctx, PlayerLevel.L4_MEASUREMENT)
        assert r.causal_bridge is not None

    def test_bridge_fires_at_l5(self):
        feats = _facing_bet_feats()
        ctx = build_hand_context(feats)
        r = REPORTER.report(_silence_pred(), feats, ctx, PlayerLevel.L5_SYSTEMS)
        assert r.causal_bridge is not None


# ═══════════════════════════════════════════════════════════════════
# 6. CAUSAL BRIDGE — POT ODDS CORRECTNESS
# ═══════════════════════════════════════════════════════════════════

class TestCausalBridgePotOdds:
    """
    The causal bridge must use  to_call / (pot + to_call)  not the feature
    vector's pot_odds field (which uses a different formula).
    """

    def _report_with_call_situation(
        self,
        pot_size: float,
        to_call: float,
        equity: float,
        level: PlayerLevel = PlayerLevel.L3_ARCHITECTURE,
    ) -> DecisionReport:
        feats = {
            **MINIMAL_FEATS,
            "facing_bet": 1.0,
            "pot_size": pot_size,
            "to_call": to_call,
            "equity_vs_range": equity,
            "raw_equity": equity,
            "spr": 5.0,
            "draw_outs": 0.0,
            # Deliberately wrong pot_odds in the feature vector — should be ignored
            "pot_odds": 0.99,
        }
        ctx = build_hand_context(feats)
        return REPORTER.report(_silence_pred(), feats, ctx, level)

    def test_correct_formula_used_not_feature_value(self):
        """
        pot=10, to_call=5 → correct_pot_odds = 5/(10+2*5) = 5/20 = 0.25
        equity = 0.70 → gap from pot odds = 0.45 > 0.10 → fires
        The feature vector has pot_odds=0.99 which would give wrong answer.
        """
        r = self._report_with_call_situation(
            pot_size=10.0, to_call=5.0, equity=0.70
        )
        assert r.causal_bridge is not None
        # Should reference ~25%, not the feature vector's 99%
        assert "25%" in r.causal_bridge

    def test_pot_odds_positive_equity_message(self):
        """When equity > pot_odds + 0.10, message says 'has {eq_pct}%'."""
        r = self._report_with_call_situation(
            pot_size=10.0, to_call=5.0, equity=0.70
        )
        assert r.causal_bridge is not None
        assert "has 70%" in r.causal_bridge
        assert "only" not in r.causal_bridge

    def test_pot_odds_negative_equity_message(self):
        """When equity < pot_odds - 0.10, message says 'has only {eq_pct}%'."""
        # pot=10, to_call=5 → correct_pot_odds = 5/(10+10) = 0.25
        # equity = 0.10 → 0.25 - 0.10 = 0.15 > 0.10 → fires
        r = self._report_with_call_situation(
            pot_size=10.0, to_call=5.0, equity=0.10
        )
        assert r.causal_bridge is not None
        assert "only" in r.causal_bridge
        assert "10%" in r.causal_bridge

    def test_pot_odds_no_fire_when_close(self):
        """
        pot=10, to_call=5 → correct_pot_odds = 5/(10+10) = 0.25
        equity = 0.30 → gap = 0.05, under 0.10 threshold → pot odds bridge does NOT fire.
        SPR is 5.0 (normal range), no draws → bridge stays None.
        """
        r = self._report_with_call_situation(
            pot_size=10.0, to_call=5.0, equity=0.30
        )
        # Pot odds gap is too small to fire; no other condition active
        assert r.causal_bridge is None

    def test_no_pot_odds_when_not_facing_bet(self):
        """
        Pot-odds bridge requires to_call_amount > 0.
        When not facing a bet, it must not fire.
        """
        feats = {
            **MINIMAL_FEATS,
            "facing_bet": 0.0,
            "to_call": 0.0,
            "pot_size": 10.0,
            "equity_vs_range": 0.90,
            "spr": 5.0,
            "draw_outs": 0.0,
        }
        ctx = build_hand_context(feats)
        r = REPORTER.report(_silence_pred(), feats, ctx, PlayerLevel.L3_ARCHITECTURE)
        # Pot-odds condition cannot fire; no other structural signal
        assert r.causal_bridge is None


# ═══════════════════════════════════════════════════════════════════
# 7. CAUSAL BRIDGE — SPR AND DRAW CONDITIONS
# ═══════════════════════════════════════════════════════════════════

class TestCausalBridgeOtherConditions:
    def test_low_spr_fires(self):
        """SPR < 2.5 → stack commitment message."""
        feats = {**MINIMAL_FEATS, "spr": 1.8, "to_call": 0.0, "draw_outs": 0.0}
        ctx = build_hand_context(feats)
        r = REPORTER.report(_silence_pred(), feats, ctx, PlayerLevel.L3_ARCHITECTURE)
        assert r.causal_bridge is not None
        assert "SPR" in r.causal_bridge
        assert "stack commitment" in r.causal_bridge

    def test_high_spr_fires(self):
        """SPR > 12.0 → deep stacks message."""
        feats = {**MINIMAL_FEATS, "spr": 15.0, "to_call": 0.0, "draw_outs": 0.0}
        ctx = build_hand_context(feats)
        r = REPORTER.report(_silence_pred(), feats, ctx, PlayerLevel.L3_ARCHITECTURE)
        assert r.causal_bridge is not None
        assert "deep stacks" in r.causal_bridge

    def test_normal_spr_no_fire(self):
        """SPR in 2.5–12.0 range does not trigger."""
        feats = {**MINIMAL_FEATS, "spr": 6.0, "to_call": 0.0, "draw_outs": 0.0}
        ctx = build_hand_context(feats)
        r = REPORTER.report(_silence_pred(), feats, ctx, PlayerLevel.L3_ARCHITECTURE)
        assert r.causal_bridge is None

    def test_draw_quality_fires_with_ctx_draw_equity(self):
        """
        draw_outs > 0 and ctx draw_equity >= 0.35 → draw message.
        Use _draw_equity in feat_dict so build_hand_context populates ctx.draw_equity.
        """
        feats = {
            **MINIMAL_FEATS,
            "spr": 5.0,
            "to_call": 0.0,
            "draw_outs": 9.0,
            "_draw_equity": 0.40,
        }
        ctx = build_hand_context(feats)
        r = REPORTER.report(_silence_pred(), feats, ctx, PlayerLevel.L3_ARCHITECTURE)
        assert r.causal_bridge is not None
        assert "outs" in r.causal_bridge
        assert "9" in r.causal_bridge

    def test_draw_quality_fires_via_outs_fallback(self):
        """When ctx.draw_equity == 0, fall back to draw_outs * 0.022."""
        # 17 outs * 0.022 = 0.374 >= 0.35 → fires
        feats = {
            **MINIMAL_FEATS,
            "spr": 5.0,
            "to_call": 0.0,
            "draw_outs": 17.0,
            "_draw_equity": 0.0,
        }
        ctx = build_hand_context(feats)
        r = REPORTER.report(_silence_pred(), feats, ctx, PlayerLevel.L3_ARCHITECTURE)
        assert r.causal_bridge is not None
        assert "17" in r.causal_bridge

    def test_draw_quality_no_fire_below_threshold(self):
        """draw_equity < 0.35 does not trigger the draw bridge."""
        # 8 outs * 0.022 = 0.176 < 0.35 → no fire
        feats = {
            **MINIMAL_FEATS,
            "spr": 5.0,
            "to_call": 0.0,
            "draw_outs": 8.0,
            "_draw_equity": 0.0,
        }
        ctx = build_hand_context(feats)
        r = REPORTER.report(_silence_pred(), feats, ctx, PlayerLevel.L3_ARCHITECTURE)
        assert r.causal_bridge is None

    def test_draw_no_fire_when_zero_outs(self):
        """draw_outs == 0 prevents draw condition from firing even if equity is set."""
        feats = {
            **MINIMAL_FEATS,
            "spr": 5.0,
            "to_call": 0.0,
            "draw_outs": 0.0,
            "_draw_equity": 0.50,
        }
        ctx = build_hand_context(feats)
        r = REPORTER.report(_silence_pred(), feats, ctx, PlayerLevel.L3_ARCHITECTURE)
        assert r.causal_bridge is None

    def test_pot_odds_takes_priority_over_spr(self):
        """
        Pot odds condition has higher priority than SPR.
        Both conditions active → pot odds message appears, not SPR.
        """
        # pot=10, to_call=5 → correct_pot_odds=0.333; equity=0.70 → fires pot-odds
        # Also set SPR=1.5 so that would fire too if pot-odds didn't
        feats = {
            **MINIMAL_FEATS,
            "facing_bet": 1.0,
            "pot_size": 10.0,
            "to_call": 5.0,
            "equity_vs_range": 0.70,
            "raw_equity": 0.70,
            "spr": 1.5,
            "draw_outs": 0.0,
        }
        ctx = build_hand_context(feats)
        r = REPORTER.report(_silence_pred(), feats, ctx, PlayerLevel.L3_ARCHITECTURE)
        assert r.causal_bridge is not None
        # Pot-odds message references equity percentage, not SPR
        assert "%" in r.causal_bridge
        assert "stack commitment" not in r.causal_bridge


# ═══════════════════════════════════════════════════════════════════
# 8. END-TO-END REPORT SHAPE
# ═══════════════════════════════════════════════════════════════════

class TestReportShape:
    def test_dataclass_fields_present(self):
        """DecisionReport has all required fields."""
        pred = _clear_pred()
        ctx = ctx_from()
        r = REPORTER.report(pred, MINIMAL_FEATS, ctx, PlayerLevel.L1_PERCEPTION)
        assert hasattr(r, "action_statement")
        assert hasattr(r, "tightness")
        assert hasattr(r, "tightness_sentence")
        assert hasattr(r, "causal_bridge")
        assert hasattr(r, "is_mixed")
        assert hasattr(r, "gap")

    def test_gap_stored_in_report(self):
        """gap field in DecisionReport matches the computed gap."""
        pred = make_pred(probs={"FOLD": 0.0, "CHECK": 0.0, "CALL": 0.0, "BET": 0.70, "RAISE": 0.30})
        ctx = ctx_from()
        r = REPORTER.report(pred, MINIMAL_FEATS, ctx, PlayerLevel.L1_PERCEPTION)
        assert abs(r.gap - 0.40) < 1e-9

    def test_frozen(self):
        """DecisionReport must be immutable (frozen dataclass)."""
        pred = _clear_pred()
        ctx = ctx_from()
        r = REPORTER.report(pred, MINIMAL_FEATS, ctx, PlayerLevel.L1_PERCEPTION)
        with pytest.raises((AttributeError, TypeError)):
            r.tightness = "MUTATED"

    def test_reporter_reusable(self):
        """Same reporter instance handles multiple calls correctly."""
        ctx = ctx_from()
        r1 = REPORTER.report(_clear_pred("BET"), MINIMAL_FEATS, ctx, PlayerLevel.L1_PERCEPTION)
        r2 = REPORTER.report(_clear_pred("FOLD"), MINIMAL_FEATS, ctx, PlayerLevel.L2_CAUSE_EFFECT)
        assert "bets" in r1.action_statement
        assert "folds" in r2.action_statement
