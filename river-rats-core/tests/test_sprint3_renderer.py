"""
Sprint 3 Tests — Renderer Logic for Sprint 2 Data Fields
=========================================================

Test-first: these tests define the expected behaviour BEFORE implementation.

WI-16: Non-nut draw distinction (C2/C3 companion pair)
WI-14: Bet-and-call signal (D3)
WI-10: Check-raise fold signal (D4) — uses "raised" not "check-raised"
WI-15: Previous-street aggression (B3) — Beginner suppressed
"""
import pytest
from coaching.spot_observation import SpotObservation
from coaching.level_renderer import (
    render_beginner,
    render_intermediate,
    render_advanced,
)


# =====================================================================
# Helper: build a SpotObservation with minimal required fields
# =====================================================================

def _build_obs(**overrides) -> SpotObservation:
    """Build a SpotObservation with sensible defaults, overriding as needed."""
    defaults = dict(
        action="CHECK",
        strategic_role="pot_control",
        hand_bucket="medium_made",
        hand_description="top pair",
        hand_description_cap="Top pair",
        equity=0.45,
        worse_hand_pct=0.50,
        better_hand_pct=0.50,
        board_texture_label="moderate",
        danger_score=0.4,
        has_draw=False,
        draw_outs=0,
        draw_description="",
        draw_equity=0.0,
        pot_odds_pct=0.0,
        equity_margin=0.0,
        facing_bet=False,
        is_ip=True,
        hero_position="BTN",
        villain_position="BB",
        opponent_phrase="your opponents",
        num_opponents=2,
        is_multiway=True,
    )
    defaults.update(overrides)
    return SpotObservation(**defaults)


# =====================================================================
# WI-16: Non-Nut Draw Distinction — C2/C3 Companion Pair
# =====================================================================

class TestWI16NonNutDraw:
    """
    C2 and C3 share: flush draw, 9 outs, is_nut_draw=False, is_multiway=True.
    They differ in: equity_margin (positive vs negative) and action (CALL vs FOLD).
    The renderer MUST produce different output for C2 vs C3.
    """

    def _c2_obs(self, level_extras=None) -> SpotObservation:
        """C2: CALL with non-nut flush draw, positive margin (price is right)."""
        kw = dict(
            action="CALL",
            strategic_role="drawing",
            hand_bucket="drawing",
            hand_description="flush draw",
            hand_description_cap="Flush draw",
            equity=0.35,
            worse_hand_pct=0.30,
            better_hand_pct=0.70,
            has_draw=True,
            draw_outs=9,
            draw_description="flush draw",
            draw_equity=0.35,
            pot_odds_pct=20.0,
            equity_margin=15.0,
            facing_bet=True,
            is_ip=False,
            is_multiway=True,
            num_opponents=2,
            is_nut_draw=False,
            hero_label="9-high flush draw",
        )
        if level_extras:
            kw.update(level_extras)
        return _build_obs(**kw)

    def _c3_obs(self, level_extras=None) -> SpotObservation:
        """C3: FOLD with non-nut flush draw, negative margin (too expensive)."""
        kw = dict(
            action="FOLD",
            strategic_role="drawing",
            hand_bucket="drawing",
            hand_description="flush draw",
            hand_description_cap="Flush draw",
            equity=0.35,
            worse_hand_pct=0.30,
            better_hand_pct=0.70,
            has_draw=True,
            draw_outs=9,
            draw_description="flush draw",
            draw_equity=0.35,
            pot_odds_pct=33.0,
            equity_margin=-8.0,
            facing_bet=True,
            is_ip=False,
            is_multiway=True,
            num_opponents=2,
            is_nut_draw=False,
            hero_label="9-high flush draw",
        )
        if level_extras:
            kw.update(level_extras)
        return _build_obs(**kw)

    def test_c2_c3_intermediate_produce_different_output(self):
        """Critical test: C2 and C3 must NOT produce identical output."""
        c2_result = render_intermediate(self._c2_obs())
        c3_result = render_intermediate(self._c3_obs())
        assert c2_result != c3_result, (
            f"C2 and C3 produced identical Intermediate output: {c2_result}"
        )

    def test_c2_intermediate_contains_price_right_and_nut_warning(self):
        result = render_intermediate(self._c2_obs())
        text = " ".join(result).lower()
        assert "right price" in text or "getting the right" in text or "enough equity" in text, (
            f"C2 Intermediate should mention price is right: {result}"
        )
        assert "not to the nuts" in text or "higher flush" in text or "not the nuts" in text, (
            f"C2 Intermediate should warn about non-nut draw: {result}"
        )

    def test_c3_intermediate_contains_too_large_and_nut_fold(self):
        result = render_intermediate(self._c3_obs())
        text = " ".join(result).lower()
        assert "too large" in text or "better price" in text or "fold" in text, (
            f"C3 Intermediate should mention price too high: {result}"
        )

    def test_c2_c3_advanced_produce_different_output(self):
        c2_result = render_advanced(self._c2_obs())
        c3_result = render_advanced(self._c3_obs())
        assert c2_result != c3_result

    def test_nut_draw_suppresses_non_nut_warning(self):
        """When is_nut_draw=True, no 'not to the nuts' warning should appear."""
        obs = self._c2_obs(level_extras={"is_nut_draw": True})
        result = render_intermediate(obs)
        text = " ".join(result).lower()
        assert "not to the nuts" not in text
        assert "higher flush" not in text


# =====================================================================
# WI-14: Bet-and-Call Signal — D3
# =====================================================================

class TestWI14BetAndCall:
    """D3: facing_bet_and_call in multiway, FOLD action."""

    def _d3_obs(self) -> SpotObservation:
        return _build_obs(
            action="FOLD",
            strategic_role="pot_control",
            hand_bucket="weak_made",
            hand_description="middle pair",
            hand_description_cap="Middle pair",
            equity=0.20,
            worse_hand_pct=0.25,
            better_hand_pct=0.75,
            pot_odds_pct=33.0,
            equity_margin=-13.0,
            facing_bet=True,
            is_ip=False,
            is_multiway=True,
            num_opponents=2,
            facing_bet_and_call=True,
        )

    def test_d3_beginner_references_bet_and_call(self):
        result = render_beginner(self._d3_obs())
        text = " ".join(result).lower()
        assert ("bet" in text and "call" in text) or "two" in text or "both" in text, (
            f"D3 Beginner should reference both bet and call: {result}"
        )

    def test_d3_intermediate_references_bet_and_call(self):
        result = render_intermediate(self._d3_obs())
        text = " ".join(result).lower()
        assert "bet" in text and "call" in text, (
            f"D3 Intermediate should reference bet and call: {result}"
        )

    def test_d3_advanced_references_bet_and_call(self):
        result = render_advanced(self._d3_obs())
        text = " ".join(result).lower()
        assert "bet" in text or "call" in text, (
            f"D3 Advanced should reference bet-call sequence: {result}"
        )


# =====================================================================
# WI-10: Check-Raise Fold Signal — D4
# =====================================================================

class TestWI10CheckRaiseFold:
    """
    D4: facing_check_raise in multiway, FOLD action.
    Language must say "raised" not "check-raised" (heuristic limitation).
    """

    def _d4_obs(self) -> SpotObservation:
        return _build_obs(
            action="FOLD",
            strategic_role="pot_control",
            hand_bucket="weak_made",
            hand_description="top pair",
            hand_description_cap="Top pair",
            equity=0.22,
            worse_hand_pct=0.28,
            better_hand_pct=0.72,
            pot_odds_pct=35.0,
            equity_margin=-13.0,
            facing_bet=True,
            is_ip=True,
            is_multiway=True,
            num_opponents=2,
            facing_check_raise=True,
        )

    def test_d4_beginner_references_raise(self):
        result = render_beginner(self._d4_obs())
        text = " ".join(result).lower()
        assert "raise" in text or "raised" in text, (
            f"D4 Beginner should reference the raise: {result}"
        )

    def test_d4_intermediate_references_raise(self):
        result = render_intermediate(self._d4_obs())
        text = " ".join(result).lower()
        assert "raise" in text or "raised" in text or "raising" in text, (
            f"D4 Intermediate should reference the raise: {result}"
        )

    def test_d4_does_not_say_check_raised(self):
        """Heuristic limitation: must NOT assert 'check-raise' sequence."""
        for render_fn in [render_beginner, render_intermediate, render_advanced]:
            result = render_fn(self._d4_obs())
            text = " ".join(result).lower()
            assert "check-raise" not in text and "check raise" not in text, (
                f"D4 must not say 'check-raise' (heuristic limitation): {result}"
            )

    def test_d4_advanced_references_polarised_or_strong(self):
        result = render_advanced(self._d4_obs())
        text = " ".join(result).lower()
        assert "strong" in text or "polar" in text or "narrow" in text, (
            f"D4 Advanced should reference range strength: {result}"
        )


# =====================================================================
# WI-15: Previous-Street Aggression — B3
# =====================================================================

class TestWI15MultiStreetAggression:
    """
    B3: villain_aggression_streets >= 2, multiway.
    Intermediate/Advanced should reference multi-street aggression.
    Beginner must NOT reference it (suppressed per Q3).
    """

    def _b3_obs(self) -> SpotObservation:
        return _build_obs(
            action="FOLD",
            strategic_role="pot_control",
            hand_bucket="weak_made",
            hand_description="top pair, weak kicker",
            hand_description_cap="Top pair, weak kicker",
            equity=0.28,
            worse_hand_pct=0.35,
            better_hand_pct=0.65,
            pot_odds_pct=33.0,
            equity_margin=-5.0,
            facing_bet=True,
            is_ip=False,
            is_multiway=True,
            num_opponents=2,
            villain_aggression_streets=2,
        )

    def test_b3_beginner_suppresses_aggression(self):
        """Beginner must NOT mention multi-street aggression."""
        result = render_beginner(self._b3_obs())
        text = " ".join(result).lower()
        assert "multiple streets" not in text
        assert "multi-street" not in text
        assert "aggression" not in text

    def test_b3_intermediate_references_multi_street(self):
        result = render_intermediate(self._b3_obs())
        text = " ".join(result).lower()
        assert "multiple streets" in text or "multi-street" in text or "bet on" in text, (
            f"B3 Intermediate should reference multi-street aggression: {result}"
        )

    def test_b3_advanced_references_range_narrowing(self):
        result = render_advanced(self._b3_obs())
        text = " ".join(result).lower()
        assert ("narrow" in text or "strong" in text or "weighted" in text
                or "multiple streets" in text), (
            f"B3 Advanced should reference range narrowing from aggression: {result}"
        )

    def test_b3_single_street_does_not_fire(self):
        """villain_aggression_streets=1 should NOT trigger the multi-street signal."""
        obs = self._b3_obs()
        # Create a new obs with 1 street of aggression
        obs_single = _build_obs(
            **{k: getattr(obs, k) for k in obs.__dataclass_fields__
               if k != 'villain_aggression_streets'},
            villain_aggression_streets=1,
        )
        result = render_intermediate(obs_single)
        text = " ".join(result).lower()
        assert "multiple streets" not in text
