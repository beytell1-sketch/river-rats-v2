"""
Tests for coaching/situation_describer.py

Coverage:
  1.  hand_strength fires at all levels with correct vocabulary
  2.  draw_quality suppressed on river (street == 2)
  3.  pot_odds only fires when facing_bet == 1 and level >= L3
  4.  board_texture always fires
  5.  range_advantage only fires at L3+ when pfr_advantage deviates from 0.5
  6.  spr_geometry threshold tests
  7.  tightness_preview fires only when gap < 0.50
  8.  SHAP ordering (higher SHAP features sort first)
  9.  Selection rule (max 2 observations + tightness)
  10. Correct pot odds formula used (not feature value)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
from dataclasses import dataclass
from typing import Dict

from coaching.levels import PlayerLevel
from coaching.hand_context import HandContext
from coaching.situation_describer import SituationDescriber, _correct_pot_odds_pct


# ═══════════════════════════════════════════════════════════════════
# MOCKS / FIXTURES
# ═══════════════════════════════════════════════════════════════════

@dataclass
class MockPrediction:
    action: str
    confidence: float
    probs: dict


def _pred(top_prob: float = 0.80, second_prob: float = 0.15) -> MockPrediction:
    """Create a mock prediction with a defined gap between top two actions."""
    remaining = max(0.0, 1.0 - top_prob - second_prob)
    return MockPrediction(
        action="BET",
        confidence=top_prob,
        probs={
            "BET":   top_prob,
            "RAISE": second_prob,
            "CHECK": remaining,
            "CALL":  0.0,
            "FOLD":  0.0,
        },
    )


def _pred_toss_up() -> MockPrediction:
    """Gap < 0.20 — should trigger 'Both actions are reasonable here.'"""
    return _pred(top_prob=0.40, second_prob=0.38)


def _pred_close() -> MockPrediction:
    """Gap between 0.20 and 0.35 — should trigger 'The other action is also reasonable here.'"""
    return _pred(top_prob=0.55, second_prob=0.30)


def _pred_silent() -> MockPrediction:
    """Gap >= 0.50 — no tightness sentence."""
    return _pred(top_prob=0.80, second_prob=0.15)


def _make_ctx(
    *,
    equity_vs_range: float = 0.65,
    raw_equity: float = 0.65,
    worse_hand_pct: float = 0.72,
    better_hand_pct: float = 0.15,
    draw_outs: float = 0.0,
    draw_equity: float = 0.0,
    spr: float = 6.0,
    danger_score: float = 0.25,
    pfr_advantage: float = 0.5,
    hand_category: float = 8.0,
    hand_rank: float = 0.7,
    is_ip: bool = True,
    hero_position_name: str = "BTN",
    villain_position_name: str = "BB",
    street_name: str = "flop",
    street_name_cap: str = "Flop",
    hand_description: str = "top pair, top kicker",
    hand_description_cap: str = "Top pair, top kicker",
    opponent_phrase: str = "your opponent",
    num_opponents: int = 1,
) -> HandContext:
    return HandContext(
        hero_cards="AcKs",
        board_cards="Kd7s2c",
        hero_position_name=hero_position_name,
        villain_position_name=villain_position_name,
        street_name=street_name,
        street_name_cap=street_name_cap,
        hand_description=hand_description,
        hand_description_cap=hand_description_cap,
        hand_description_bare=hand_description,
        hand_verb="is",
        hand_verb_neg="isn't",
        hand_does_neg="doesn't",
        is_ip=is_ip,
        is_initiative=True,
        equity_vs_range=equity_vs_range,
        raw_equity=raw_equity,
        equity_margin=0.0,
        pot_odds=0.33,
        bet_to_pot=0.5,
        spr=spr,
        danger_score=danger_score,
        draw_outs=draw_outs,
        better_hand_pct=better_hand_pct,
        worse_hand_pct=worse_hand_pct,
        hand_category=hand_category,
        hand_rank=hand_rank,
        is_3bet_pot=False,
        villain_aggression_count=0,
        villain_checked_back=False,
        villain_call_count=0,
        num_opponents=num_opponents,
        opponent_phrase=opponent_phrase,
        pfr_advantage=pfr_advantage,
        board_type="dry",
        draw_equity=draw_equity,
        needs_protection=False,
        pot_size=100.0,
        to_call_amount=0.0,
    )


def _make_feat(
    *,
    street: float = 0.0,
    facing_bet: float = 0.0,
    draw_outs: float = 0.0,
    is_rainbow: float = 1.0,
    is_two_tone: float = 0.0,
    is_monotone: float = 0.0,
    connectivity_score: float = 2.0,
    danger_score: float = 0.25,
    flush_danger: float = 0.0,
    pot_size: float = 100.0,
    to_call: float = 0.0,
    spr: float = 6.0,
    hero_position: float = 3.0,
    villain_position: float = 5.0,
    is_ip: float = 1.0,
    equity_vs_range: float = 0.65,
    pot_odds: float = 0.25,
) -> dict:
    return {
        "street": street,
        "facing_bet": facing_bet,
        "draw_outs": draw_outs,
        "is_rainbow": is_rainbow,
        "is_two_tone": is_two_tone,
        "is_monotone": is_monotone,
        "connectivity_score": connectivity_score,
        "danger_score": danger_score,
        "flush_danger": flush_danger,
        "pot_size": pot_size,
        "to_call": to_call,
        "spr": spr,
        "hero_position": hero_position,
        "villain_position": villain_position,
        "is_ip": is_ip,
        "equity_vs_range": equity_vs_range,
        "pot_odds": pot_odds,  # intentionally different from correct formula
    }


NEUTRAL_SHAP: Dict[str, float] = {}

sd = SituationDescriber()


# ═══════════════════════════════════════════════════════════════════
# 1. hand_strength vocabulary at each level
# ═══════════════════════════════════════════════════════════════════

class TestHandStrength:

    def test_L1_strong(self):
        ctx = _make_ctx(equity_vs_range=0.70)
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert any("strong hand" in s for s in result)

    def test_L1_decent(self):
        ctx = _make_ctx(equity_vs_range=0.50)
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert any("decent hand" in s for s in result)

    def test_L1_weak_behind(self):
        ctx = _make_ctx(equity_vs_range=0.35, better_hand_pct=0.70)
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert any("behind most of" in s for s in result)

    def test_L1_weak_no_showdown(self):
        ctx = _make_ctx(equity_vs_range=0.15, better_hand_pct=0.30)
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert any("cannot win at showdown" in s for s in result)

    def test_L2_dominant(self):
        ctx = _make_ctx(equity_vs_range=0.65, worse_hand_pct=0.80)
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L2_CAUSE_EFFECT)
        assert any("ahead of most of" in s for s in result)

    def test_L2_solid(self):
        ctx = _make_ctx(equity_vs_range=0.55, worse_hand_pct=0.55)
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L2_CAUSE_EFFECT)
        assert any("solid but not dominant" in s for s in result)

    def test_L2_behind(self):
        ctx = _make_ctx(equity_vs_range=0.35, worse_hand_pct=0.30, better_hand_pct=0.65)
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L2_CAUSE_EFFECT)
        assert any("behind most of what" in s for s in result)

    def test_L2_zero_showdown(self):
        ctx = _make_ctx(equity_vs_range=0.03, worse_hand_pct=0.10, better_hand_pct=0.40)
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L2_CAUSE_EFFECT)
        assert any("zero showdown value" in s for s in result)

    def test_L3_contains_equity_pct(self):
        ctx = _make_ctx(equity_vs_range=0.65, worse_hand_pct=0.72)
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        assert any("65%" in s and "72%" in s for s in result)

    def test_L4_contains_better_pct(self):
        ctx = _make_ctx(equity_vs_range=0.65, worse_hand_pct=0.72, better_hand_pct=0.15)
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L4_MEASUREMENT)
        assert any("15% has you beat" in s for s in result)

    def test_L5_contains_cat(self):
        ctx = _make_ctx(equity_vs_range=0.65, worse_hand_pct=0.72, hand_category=8.0)
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L5_SYSTEMS)
        assert any("cat 8" in s for s in result)


# ═══════════════════════════════════════════════════════════════════
# 2. draw_quality suppressed on river
# ═══════════════════════════════════════════════════════════════════

class TestDrawQuality:

    def test_draw_fires_on_flop(self):
        ctx = _make_ctx(draw_outs=9.0)
        feat = _make_feat(draw_outs=9.0, street=0.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert any("draw" in s.lower() for s in result)

    def test_draw_fires_on_turn(self):
        ctx = _make_ctx(draw_outs=9.0, street_name="turn")
        feat = _make_feat(draw_outs=9.0, street=1.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert any("draw" in s.lower() for s in result)

    def test_draw_suppressed_on_river(self):
        ctx = _make_ctx(draw_outs=9.0, street_name="river")
        feat = _make_feat(draw_outs=9.0, street=2.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        # draw_quality text specifically uses "draw -- your hand can improve"
        assert not any("your hand can improve" in s for s in result)

    def test_draw_suppressed_when_outs_zero(self):
        ctx = _make_ctx(draw_outs=0.0)
        feat = _make_feat(draw_outs=0.0, street=0.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert not any("your hand can improve" in s for s in result)

    def test_draw_L2_big_outs(self):
        ctx = _make_ctx(draw_outs=9.0)
        feat = _make_feat(draw_outs=9.0, street=0.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L2_CAUSE_EFFECT)
        assert any("powerful hand" in s for s in result)

    def test_draw_L2_small_outs(self):
        ctx = _make_ctx(draw_outs=3.0)
        feat = _make_feat(draw_outs=3.0, street=0.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L2_CAUSE_EFFECT)
        assert any("small number of outs" in s for s in result)

    def test_draw_L4_shows_draw_equity(self):
        ctx = _make_ctx(draw_outs=9.0, draw_equity=0.18)
        feat = _make_feat(draw_outs=9.0, street=0.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L4_MEASUREMENT)
        assert any("draw equity" in s.lower() for s in result)


# ═══════════════════════════════════════════════════════════════════
# 3. pot_odds gating
# ═══════════════════════════════════════════════════════════════════

class TestPotOdds:

    def test_fires_at_L3_with_facing_bet(self):
        ctx = _make_ctx()
        feat = _make_feat(facing_bet=1.0, pot_size=100.0, to_call=50.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        assert any("equity to continue" in s for s in result)

    def test_suppressed_at_L1(self):
        ctx = _make_ctx()
        feat = _make_feat(facing_bet=1.0, pot_size=100.0, to_call=50.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert not any("equity to continue" in s for s in result)

    def test_suppressed_at_L2(self):
        ctx = _make_ctx()
        feat = _make_feat(facing_bet=1.0, pot_size=100.0, to_call=50.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L2_CAUSE_EFFECT)
        assert not any("equity to continue" in s for s in result)

    def test_suppressed_when_no_facing_bet(self):
        ctx = _make_ctx()
        feat = _make_feat(facing_bet=0.0, pot_size=100.0, to_call=50.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        assert not any("equity to continue" in s for s in result)

    def test_fires_at_L4(self):
        ctx = _make_ctx()
        feat = _make_feat(facing_bet=1.0, pot_size=100.0, to_call=50.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L4_MEASUREMENT)
        assert any("equity margin" in s for s in result)

    def test_fires_at_L5(self):
        ctx = _make_ctx()
        feat = _make_feat(facing_bet=1.0, pot_size=100.0, to_call=50.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L5_SYSTEMS)
        assert any("Margin" in s for s in result)

    def test_L3_pot_odds_no_threshold_suffix(self):
        """L3 pot odds states the numbers without ahead/short suffix
        (removed to prevent contradictions with fold-despite-positive-margin)."""
        ctx = _make_ctx(equity_vs_range=0.65)
        feat = _make_feat(facing_bet=1.0, pot_size=100.0, to_call=50.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        pot_odds_obs = [s for s in result if "requires" in s and "equity" in s]
        assert len(pot_odds_obs) > 0, "Pot odds observation should fire"
        for s in pot_odds_obs:
            assert "ahead of the threshold" not in s
            assert "short of the threshold" not in s


# ═══════════════════════════════════════════════════════════════════
# 4. board_texture always fires
# ═══════════════════════════════════════════════════════════════════

class TestBoardTexture:

    def test_always_fires_L1(self):
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert any("board" in s.lower() for s in result)

    def test_always_fires_L5(self):
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L5_SYSTEMS)
        assert any("board" in s.lower() for s in result)

    def test_safe_board_L1(self):
        ctx = _make_ctx(danger_score=0.20)
        feat = _make_feat(danger_score=0.20)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert any("board is safe" in s for s in result)

    def test_dangerous_board_L1(self):
        """High-danger board produces a specific board observation at L1."""
        ctx = _make_ctx(danger_score=0.75)
        feat = _make_feat(danger_score=0.75)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        # With range features, L1 uses specific language instead of generic "dangerous"
        board_obs = [s for s in result if "board" in s.lower() or "range" in s.lower()
                     or "connect" in s.lower() or "danger" in s.lower()
                     or "cautious" in s.lower() or "suit" in s.lower()]
        assert len(board_obs) > 0, f"Expected board texture observation in {result}"

    def test_L2_dry_disconnected(self):
        ctx = _make_ctx()
        feat = _make_feat(is_rainbow=1.0, is_two_tone=0.0, is_monotone=0.0,
                          connectivity_score=2.0, draw_outs=0.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L2_CAUSE_EFFECT)
        assert any("dry and disconnected" in s for s in result)

    def test_L3_includes_numbers(self):
        ctx = _make_ctx(danger_score=0.40)
        feat = _make_feat(danger_score=0.40, connectivity_score=5.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        assert any("0.40" in s for s in result)


# ═══════════════════════════════════════════════════════════════════
# 5. range_advantage gating
# ═══════════════════════════════════════════════════════════════════

class TestRangeAdvantage:

    def test_fires_L3_above_threshold(self):
        ctx = _make_ctx(pfr_advantage=0.65)
        # Give range_advantage features high SHAP so they surface in top-2
        shap = {"hero_position": 0.9, "villain_position": 0.8}
        result = sd.describe(ctx, _make_feat(), shap, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        assert any("range connects better" in s for s in result)

    def test_fires_L3_below_threshold(self):
        ctx = _make_ctx(pfr_advantage=0.35)
        shap = {"hero_position": 0.9, "villain_position": 0.8}
        result = sd.describe(ctx, _make_feat(), shap, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        assert any("opponent's range" in s for s in result)

    def test_suppressed_L2(self):
        ctx = _make_ctx(pfr_advantage=0.65)
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L2_CAUSE_EFFECT)
        assert not any("range connects better" in s for s in result)

    def test_suppressed_L1(self):
        ctx = _make_ctx(pfr_advantage=0.65)
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert not any("range connects better" in s for s in result)

    def test_suppressed_when_neutral_pfr(self):
        # pfr_advantage == 0.50 → range_advantage should NOT fire regardless of SHAP
        ctx = _make_ctx(pfr_advantage=0.50)
        shap = {"hero_position": 0.9, "villain_position": 0.8}
        result = sd.describe(ctx, _make_feat(), shap, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        assert not any("range connects better" in s for s in result)

    def test_suppressed_when_near_neutral(self):
        # pfr_advantage == 0.51 — between 0.45 and 0.55, range_advantage should not fire
        ctx = _make_ctx(pfr_advantage=0.51)
        shap = {"hero_position": 0.9, "villain_position": 0.8}
        result = sd.describe(ctx, _make_feat(), shap, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        # range_advantage-specific phrases (not found in other observations)
        assert not any("range connects better" in s for s in result)
        assert not any("This board connects better with your opponent's range" in s for s in result)

    def test_L4_includes_percentage(self):
        ctx = _make_ctx(pfr_advantage=0.70)
        shap = {"hero_position": 0.9, "villain_position": 0.8}
        result = sd.describe(ctx, _make_feat(), shap, _pred_silent(), PlayerLevel.L4_MEASUREMENT)
        assert any("Range advantage" in s and "%" in s for s in result)

    def test_L5_mentions_frequency(self):
        ctx = _make_ctx(pfr_advantage=0.70)
        shap = {"hero_position": 0.9, "villain_position": 0.8}
        result = sd.describe(ctx, _make_feat(), shap, _pred_silent(), PlayerLevel.L5_SYSTEMS)
        assert any("frequency splits" in s for s in result)


# ═══════════════════════════════════════════════════════════════════
# 6. spr_geometry threshold tests
# ═══════════════════════════════════════════════════════════════════

class TestSprGeometry:

    def test_fires_when_spr_low(self):
        ctx = _make_ctx(spr=2.5)
        feat = _make_feat(spr=2.5)
        # Give spr high SHAP so spr_geometry surfaces in top-2
        shap = {"spr": 0.95}
        result = sd.describe(ctx, feat, shap, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        assert any("SPR" in s for s in result)

    def test_fires_when_spr_very_low(self):
        ctx = _make_ctx(spr=1.0)
        feat = _make_feat(spr=1.0)
        shap = {"spr": 0.95}
        result = sd.describe(ctx, feat, shap, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        assert any("stack-commitment" in s for s in result)

    def test_fires_when_spr_high(self):
        ctx = _make_ctx(spr=15.0)
        feat = _make_feat(spr=15.0)
        shap = {"spr": 0.95}
        result = sd.describe(ctx, feat, shap, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        assert any("deep stacks" in s for s in result)

    def test_suppressed_when_spr_moderate(self):
        # spr between 4 and 10 should NOT fire
        ctx = _make_ctx(spr=6.0)
        feat = _make_feat(spr=6.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        assert not any("SPR" in s for s in result)

    def test_suppressed_at_L2(self):
        ctx = _make_ctx(spr=2.0)
        feat = _make_feat(spr=2.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L2_CAUSE_EFFECT)
        assert not any("SPR" in s for s in result)

    def test_L4_has_context_phrase(self):
        ctx = _make_ctx(spr=2.5)
        feat = _make_feat(spr=2.5)
        shap = {"spr": 0.95}
        result = sd.describe(ctx, feat, shap, _pred_silent(), PlayerLevel.L4_MEASUREMENT)
        assert any("SPR 2.5" in s for s in result)

    def test_L5_has_geometry_phrase(self):
        ctx = _make_ctx(spr=2.5)
        feat = _make_feat(spr=2.5)
        shap = {"spr": 0.95}
        result = sd.describe(ctx, feat, shap, _pred_silent(), PlayerLevel.L5_SYSTEMS)
        assert any("Stack geometry" in s for s in result)

    def test_boundary_spr_4_not_fires(self):
        # Exactly 4.0 — spec says spr < 4.0, so 4.0 should NOT fire
        ctx = _make_ctx(spr=4.0)
        feat = _make_feat(spr=4.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        assert not any("SPR" in s for s in result)

    def test_boundary_spr_10_not_fires(self):
        # Exactly 10.0 — spec says spr > 10.0, so 10.0 should NOT fire
        ctx = _make_ctx(spr=10.0)
        feat = _make_feat(spr=10.0)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        assert not any("SPR" in s for s in result)


# ═══════════════════════════════════════════════════════════════════
# 7. tightness_preview gap thresholds
# ═══════════════════════════════════════════════════════════════════

class TestTightnessPreview:

    def test_toss_up_fires(self):
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_toss_up(), PlayerLevel.L1_PERCEPTION)
        assert "Both actions are reasonable here." in result

    def test_close_fires(self):
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_close(), PlayerLevel.L1_PERCEPTION)
        assert "The other action is also reasonable here." in result

    def test_silent_does_not_fire(self):
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert "Both actions are reasonable here." not in result
        assert "The other action is also reasonable here." not in result

    def test_tightness_is_last(self):
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_toss_up(), PlayerLevel.L1_PERCEPTION)
        assert result[-1] == "Both actions are reasonable here."

    def test_tightness_at_all_levels(self):
        for level in PlayerLevel:
            ctx = _make_ctx()
            result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_toss_up(), level)
            assert "Both actions are reasonable here." in result

    def test_gap_exactly_020_is_close_not_toss_up(self):
        # gap == 0.20 is NOT < 0.20, so should be CLOSE
        pred = _pred(top_prob=0.55, second_prob=0.35)  # gap = 0.20
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, pred, PlayerLevel.L1_PERCEPTION)
        # Should fire as CLOSE, not TOSS_UP
        assert "The other action is also reasonable here." in result
        assert "Both actions are reasonable here." not in result

    def test_gap_above_050_is_silent(self):
        # gap > 0.50 — definitively in SILENCE territory.
        # Explicitly set all 5 action probs so the top-two gap is unambiguous.
        pred = MockPrediction(
            action="BET",
            confidence=0.80,
            probs={"BET": 0.80, "CHECK": 0.10, "CALL": 0.05, "RAISE": 0.03, "FOLD": 0.02},
        )
        # gap = 0.80 - 0.10 = 0.70 — well above 0.50
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, pred, PlayerLevel.L1_PERCEPTION)
        assert "Both actions are reasonable here." not in result
        assert "The other action is also reasonable here." not in result


# ═══════════════════════════════════════════════════════════════════
# 8. SHAP ordering
# ═══════════════════════════════════════════════════════════════════

class TestShapOrdering:

    def test_higher_shap_fires_first(self):
        """
        Give board_texture high SHAP and hand_strength low SHAP.
        board_texture sentence should appear before hand_strength sentence.
        Use L3+ so sentences have distinctive, non-overlapping keywords.
        """
        ctx = _make_ctx(equity_vs_range=0.65, worse_hand_pct=0.72)
        feat = _make_feat()
        shap = {
            # board_texture associated features dominant
            "danger_score": 0.9,
            "connectivity_score": 0.8,
            # hand_strength associated features low
            "equity_vs_range": 0.1,
            "raw_equity": 0.1,
        }
        result = sd.describe(ctx, feat, shap, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        # L3 board_texture sentence: "The board is ... (danger ..., connectivity ...)"
        # L3 hand_strength sentence: "Top pair, top kicker with 65% equity. You beat 72% ..."
        # hand_strength is now guaranteed first (P0 fix from Cycle 2 review),
        # so even when board SHAP dominates, hand_strength leads.
        hand_idx  = next((i for i, s in enumerate(result) if "equity" in s and "%" in s), None)
        board_idx = next((i for i, s in enumerate(result) if "danger" in s.lower()), None)
        assert hand_idx is not None, f"hand_strength not in result: {result}"
        assert board_idx is not None, f"board_texture not in result: {result}"
        assert hand_idx == 0, (
            f"Expected hand_strength always first; got result={result}"
        )
        assert board_idx == 1, (
            f"Expected board_texture second (highest SHAP); got result={result}"
        )

    def test_hand_strength_fires_first_when_shap_highest(self):
        ctx = _make_ctx(equity_vs_range=0.65, worse_hand_pct=0.72)
        feat = _make_feat()
        shap = {
            # hand_strength features dominate
            "equity_vs_range": 0.95,
            "raw_equity": 0.90,
            # board features low
            "danger_score": 0.05,
        }
        result = sd.describe(ctx, feat, shap, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        hand_idx  = next((i for i, s in enumerate(result) if "equity" in s and "%" in s), None)
        board_idx = next((i for i, s in enumerate(result) if "danger" in s.lower()), None)
        assert hand_idx is not None, f"hand_strength not in result: {result}"
        assert board_idx is not None, f"board_texture not in result: {result}"
        assert hand_idx < board_idx, (
            f"Expected hand_strength before board_texture; got result={result}"
        )

    def test_tied_shap_stable_order(self):
        """With all SHAP zero, ordering should still produce a valid 2-item list."""
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        # Non-tightness part should be 2 items
        non_tight = [s for s in result if s not in (
            "Both actions are reasonable here.", "The other action is also reasonable here."
        )]
        assert len(non_tight) == 2


# ═══════════════════════════════════════════════════════════════════
# 9. Selection rule (max 2 observations + tightness)
# ═══════════════════════════════════════════════════════════════════

class TestSelectionRule:

    def test_exactly_two_non_tightness_plus_tightness(self):
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_toss_up(), PlayerLevel.L1_PERCEPTION)
        tightness_sentences = {"Both actions are reasonable here.", "The other action is also reasonable here."}
        non_tight = [s for s in result if s not in tightness_sentences]
        tight     = [s for s in result if s in tightness_sentences]
        assert len(non_tight) == 2
        assert len(tight) == 1

    def test_exactly_two_non_tightness_no_tightness(self):
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        tightness_sentences = {"Both actions are reasonable here.", "The other action is also reasonable here."}
        non_tight = [s for s in result if s not in tightness_sentences]
        assert len(non_tight) == 2

    def test_total_length_with_tightness(self):
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_toss_up(), PlayerLevel.L1_PERCEPTION)
        assert len(result) == 3

    def test_total_length_without_tightness(self):
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert len(result) == 2

    def test_returns_list(self):
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert isinstance(result, list)

    def test_all_items_are_strings(self):
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_toss_up(), PlayerLevel.L5_SYSTEMS)
        assert all(isinstance(s, str) for s in result)

    def test_minimum_one_plus_tightness(self):
        """
        With all gated observations suppressed, at minimum hand_strength and
        board_texture fire (both always-on), giving 2.
        """
        ctx = _make_ctx()
        result = sd.describe(ctx, _make_feat(), NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert len(result) >= 2


# ═══════════════════════════════════════════════════════════════════
# 10. Correct pot odds formula
# ═══════════════════════════════════════════════════════════════════

class TestPotOddsFormula:

    def test_correct_formula_value(self):
        """
        pot_size=100, to_call=50 → correct odds = 50/(100+2*50) = 50/200 = 25.0%
        Feature value pot_odds=0.10 (10%) is intentionally different.
        """
        feat = _make_feat(pot_size=100.0, to_call=50.0, pot_odds=0.10)
        result = _correct_pot_odds_pct(feat)
        assert abs(result - 25.0) < 0.1, f"Expected ~25.0%, got {result:.2f}%"

    def test_pot_odds_sentence_uses_correct_value(self):
        """
        Correct pot odds: 50 / (100 + 2*50) = 50/200 = 25%, not the feature value of 10%.
        With equity_vs_range=0.50 (50%), 10% won't appear anywhere in the sentence,
        letting us confirm the formula is not just using feat_dict['pot_odds'].
        """
        ctx = _make_ctx(equity_vs_range=0.50)
        feat = _make_feat(facing_bet=1.0, pot_size=100.0, to_call=50.0, pot_odds=0.10)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L3_ARCHITECTURE)
        pot_odds_sentences = [s for s in result if "equity to continue" in s]
        assert len(pot_odds_sentences) == 1
        sentence = pot_odds_sentences[0]
        # Correct formula gives 25%; feature gives 10%
        assert "25%" in sentence, f"Expected 25% (correct formula) in sentence, got: {sentence}"
        assert "10%" not in sentence, f"Feature value 10% leaked into sentence: {sentence}"

    def test_zero_to_call_returns_zero(self):
        feat = _make_feat(to_call=0.0, pot_size=100.0)
        assert _correct_pot_odds_pct(feat) == 0.0

    def test_equal_to_call_and_pot(self):
        """to_call == pot_size → odds = 100/(100+200) = 33.33%"""
        feat = _make_feat(pot_size=100.0, to_call=100.0)
        result = _correct_pot_odds_pct(feat)
        assert abs(result - 33.33) < 0.01

    def test_small_bet_into_big_pot(self):
        """to_call=20, pot=100 → 20/(100+40) = 20/140 = 14.29%"""
        feat = _make_feat(pot_size=100.0, to_call=20.0)
        result = _correct_pot_odds_pct(feat)
        assert abs(result - 14.29) < 0.1

    def test_L4_margin_uses_correct_formula(self):
        """L4 sentence includes 'equity margin' — verify it uses corrected pot odds."""
        ctx = _make_ctx(equity_vs_range=0.65)
        feat = _make_feat(facing_bet=1.0, pot_size=100.0, to_call=50.0, pot_odds=0.10)
        result = sd.describe(ctx, feat, NEUTRAL_SHAP, _pred_silent(), PlayerLevel.L4_MEASUREMENT)
        margin_sentences = [s for s in result if "equity margin" in s]
        assert len(margin_sentences) == 1
        # margin = 65% - 25% = +40 (not 65% - 10% = 55%)
        # Correct formula: 50/(100+2*50) = 25%
        sentence = margin_sentences[0]
        assert "+40" in sentence, (
            f"Margin should be ~+40 based on correct pot odds; got: {sentence}"
        )


# ═══════════════════════════════════════════════════════════════════
# POSITION CONTEXT VOCABULARY SMOKE TESTS
# ═══════════════════════════════════════════════════════════════════

class TestPositionContext:

    def test_L1_ip(self):
        ctx = _make_ctx(is_ip=True)
        # Give position features high SHAP so position_context surfaces in top-2
        shap = {"is_ip": 0.95, "hero_position": 0.90}
        result = sd.describe(ctx, _make_feat(is_ip=1.0), shap, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert any("in position" in s for s in result)

    def test_L1_oop(self):
        ctx = _make_ctx(is_ip=False)
        shap = {"is_ip": 0.95, "hero_position": 0.90}
        result = sd.describe(ctx, _make_feat(is_ip=0.0), shap, _pred_silent(), PlayerLevel.L1_PERCEPTION)
        assert any("out of position" in s for s in result)

    def test_L5_includes_both_positions(self):
        ctx = _make_ctx(is_ip=True, hero_position_name="BTN", villain_position_name="BB")
        shap = {"is_ip": 0.95, "hero_position": 0.90}
        result = sd.describe(ctx, _make_feat(), shap, _pred_silent(), PlayerLevel.L5_SYSTEMS)
        assert any("BTN" in s and "BB" in s for s in result)


if __name__ == "__main__":
    import pytest as pt
    pt.main([__file__, "-v"])
