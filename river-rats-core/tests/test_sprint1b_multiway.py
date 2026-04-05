"""
Tests for Sprint 1B multiway coaching items:
  A-4:  Draw price framing (_draw_price_sentence helper)
  A-9:  Reverse implied odds qualifier (flush draws only, inside A-4)
  A-10: Shared burden of defense (window [-8, +5], no caveats)
  Advanced equity display: no "(approximate)", equity is authoritative.

All tests gated on obs.is_multiway per spec.
HU behaviour is unchanged.
"""
import pytest
from coaching.spot_observation import SpotObservation
from coaching.level_renderer import (
    _draw_price_sentence,
    _shared_burden_sentence,
    render_intermediate,
    render_advanced,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_obs(**overrides):
    """Build a minimal SpotObservation for multiway draw scenarios."""
    defaults = dict(
        action="CALL",
        strategic_role="drawing_call",
        hand_bucket="drawing",
        hand_description="flush draw",
        hand_description_cap="Flush draw",
        equity=0.35,
        worse_hand_pct=0.20,
        better_hand_pct=0.65,
        board_texture_label="dangerous",
        danger_score=0.70,
        has_draw=True,
        draw_outs=9,
        draw_description="flush draw",
        draw_equity=0.35,
        pot_odds_pct=20.0,
        equity_margin=15.0,
        facing_bet=True,
        is_ip=True,
        hero_position="BTN",
        villain_position="CO",
        opponent_phrase="your opponents",
        num_opponents=2,
        is_multiway=True,
        hero_label="9-high flush draw",
        tightness="SILENCE",
        confidence=0.80,
    )
    defaults.update(overrides)
    return SpotObservation(**defaults)


# ---------------------------------------------------------------------------
# A-4: Draw price sentence helper — basic firing conditions
# ---------------------------------------------------------------------------

class TestDrawPriceSentenceBasic:
    def test_returns_empty_at_beginner(self):
        obs = make_obs()
        assert _draw_price_sentence(obs, "beginner") == ""

    def test_intermediate_positive_margin_right_price(self):
        obs = make_obs(equity_margin=15.0)
        result = _draw_price_sentence(obs, "intermediate")
        assert "right price" in result

    def test_intermediate_small_negative_margin_needs_better_price(self):
        obs = make_obs(equity_margin=-5.0, equity=0.15)
        result = _draw_price_sentence(obs, "intermediate")
        assert "better price" in result or "too large" in result

    def test_intermediate_large_negative_margin_fold(self):
        obs = make_obs(equity_margin=-12.0, equity=0.08)
        result = _draw_price_sentence(obs, "intermediate")
        assert "fold" in result.lower()

    def test_advanced_positive_margin_shows_equity_and_pot_odds(self):
        obs = make_obs(draw_equity=0.35, pot_odds_pct=20.0, equity_margin=15.0)
        result = _draw_price_sentence(obs, "advanced")
        # Equity: 35%, pot odds: 20%, margin: 15 points — all should appear
        assert "35%" in result
        assert "20%" in result
        assert "15" in result

    def test_advanced_negative_margin_shows_shortfall(self):
        obs = make_obs(draw_equity=0.25, pot_odds_pct=33.0, equity_margin=-8.0, equity=0.25)
        result = _draw_price_sentence(obs, "advanced")
        assert "falls short" in result or "threshold" in result

    def test_advanced_large_negative_margin_equity_deficit(self):
        obs = make_obs(equity_margin=-15.0, equity=0.10)
        result = _draw_price_sentence(obs, "advanced")
        assert "deficit" in result.lower() or "fold" in result.lower()


# ---------------------------------------------------------------------------
# A-4: No "(approximate)" caveats in any output
# ---------------------------------------------------------------------------

class TestNoApproximateCaveats:
    def test_intermediate_no_approximate(self):
        obs = make_obs(equity_margin=15.0, is_multiway=True)
        result = _draw_price_sentence(obs, "intermediate")
        assert "(approximate)" not in result

    def test_advanced_no_approximate(self):
        obs = make_obs(equity_margin=15.0, is_multiway=True)
        result = _draw_price_sentence(obs, "advanced")
        assert "(approximate)" not in result

    def test_advanced_no_tilde_prefix(self):
        obs = make_obs(equity_margin=15.0, is_multiway=True)
        result = _draw_price_sentence(obs, "advanced")
        # Should not use ~ to flag uncertainty
        assert "~" not in result

    def test_shared_burden_advanced_no_approximate(self):
        obs = make_obs(action="FOLD", equity_margin=-3.0, equity=0.17,
                       strategic_role="range_fold")
        result = _shared_burden_sentence(obs, "advanced")
        assert "(approximate)" not in result
        assert "~" not in result

    def test_shared_burden_advanced_call_no_approximate(self):
        obs = make_obs(equity_margin=3.0, equity=0.23, pot_odds_pct=20.0,
                       strategic_role="priced_in")
        result = _shared_burden_sentence(obs, "advanced")
        assert "(approximate)" not in result
        assert "~" not in result


# ---------------------------------------------------------------------------
# A-9: Reverse implied odds — flush draws only, gated conditions
# ---------------------------------------------------------------------------

class TestReverseImpliedOdds:
    def test_intermediate_fires_for_non_nut_flush_draw(self):
        obs = make_obs(equity_margin=15.0, draw_description="flush draw",
                       draw_outs=9, hero_label="9-high flush draw")
        result = _draw_price_sentence(obs, "intermediate")
        assert "higher flush" in result or "completing your draw" in result

    def test_advanced_fires_for_non_nut_flush_draw(self):
        obs = make_obs(equity_margin=15.0, draw_description="flush draw",
                       draw_outs=9, hero_label="9-high flush draw")
        result = _draw_price_sentence(obs, "advanced")
        assert "Reverse implied odds" in result or "non-nut" in result or "not to the nuts" in result

    def test_intermediate_suppressed_for_straight_draw(self):
        obs = make_obs(equity_margin=15.0, draw_description="straight draw",
                       draw_outs=8, hero_label="open-ended straight draw")
        result = _draw_price_sentence(obs, "intermediate")
        assert "higher flush" not in result
        assert "completing your draw" not in result
        assert "Reverse implied odds" not in result

    def test_advanced_suppressed_for_straight_draw(self):
        obs = make_obs(equity_margin=15.0, draw_description="straight draw",
                       draw_outs=8, hero_label="open-ended straight draw")
        result = _draw_price_sentence(obs, "advanced")
        assert "Reverse implied odds" not in result
        assert "non-nut" not in result

    def test_intermediate_suppressed_for_nut_flush_draw(self):
        obs = make_obs(equity_margin=15.0, draw_description="flush draw",
                       draw_outs=9, hero_label="nut flush draw", is_nut_draw=True)
        result = _draw_price_sentence(obs, "intermediate")
        assert "higher flush" not in result
        assert "completing your draw" not in result
        assert "not to the nuts" not in result

    def test_advanced_suppressed_for_nut_flush_draw(self):
        obs = make_obs(equity_margin=15.0, draw_description="flush draw",
                       draw_outs=9, hero_label="nut flush draw", is_nut_draw=True)
        result = _draw_price_sentence(obs, "advanced")
        assert "Reverse implied odds" not in result
        assert "not to the nuts" not in result

    def test_intermediate_suppressed_for_a_high_flush(self):
        obs = make_obs(equity_margin=15.0, draw_description="flush draw",
                       draw_outs=9, hero_label="a-high flush draw", is_nut_draw=True)
        result = _draw_price_sentence(obs, "intermediate")
        assert "higher flush" not in result
        assert "not to the nuts" not in result

    def test_suppressed_when_margin_not_positive(self):
        """RIO only fires when action is profitable (margin > 0)."""
        obs = make_obs(equity_margin=-5.0, equity=0.15, draw_description="flush draw",
                       hero_label="9-high flush draw")
        result = _draw_price_sentence(obs, "intermediate")
        assert "higher flush" not in result
        assert "Reverse implied odds" not in result

    def test_intermediate_suppressed_for_combo_draw(self):
        """Combo draws (10+ outs) suppress RIO."""
        obs = make_obs(equity_margin=29.0, draw_description="combo draw",
                       draw_outs=15, hero_label="combo draw")
        result = _draw_price_sentence(obs, "intermediate")
        assert "Reverse implied odds" not in result
        assert "higher flush" not in result

    def test_advanced_suppressed_for_combo_draw(self):
        obs = make_obs(equity_margin=29.0, draw_description="combo draw",
                       draw_outs=15, hero_label="combo draw")
        result = _draw_price_sentence(obs, "advanced")
        assert "Reverse implied odds" not in result

    def test_beginner_never_fires(self):
        """A-9 must NEVER fire at Beginner (B5 fix)."""
        obs = make_obs(equity_margin=15.0)
        assert _draw_price_sentence(obs, "beginner") == ""


# ---------------------------------------------------------------------------
# A-10: Shared burden of defense — window and gating
# ---------------------------------------------------------------------------

class TestSharedBurdenOfDefense:
    def test_intermediate_fold_fires_in_window(self):
        obs = make_obs(action="FOLD", equity_margin=-3.0, equity=0.17,
                       strategic_role="range_fold")
        result = _shared_burden_sentence(obs, "intermediate")
        assert "fold more hands" in result

    def test_intermediate_call_fires_in_window(self):
        obs = make_obs(equity_margin=3.0, equity=0.23, strategic_role="priced_in")
        result = _shared_burden_sentence(obs, "intermediate")
        assert "price" in result.lower() and "call" in result.lower()

    def test_intermediate_call_s8_leads_with_price(self):
        """S-8 fix: CALL template must lead with price framing."""
        obs = make_obs(equity_margin=3.0, equity=0.23, strategic_role="priced_in")
        result = _shared_burden_sentence(obs, "intermediate")
        assert result.lower().startswith("the price")

    def test_advanced_fold_clean_equity_number(self):
        obs = make_obs(action="FOLD", equity_margin=-3.0, equity=0.17,
                       strategic_role="range_fold")
        result = _shared_burden_sentence(obs, "advanced")
        assert "17%" in result

    def test_advanced_call_clean_equity_and_pot_odds(self):
        obs = make_obs(equity_margin=3.0, equity=0.23, pot_odds_pct=20.0,
                       strategic_role="priced_in")
        result = _shared_burden_sentence(obs, "advanced")
        assert "23%" in result
        assert "20%" in result

    def test_suppressed_at_beginner(self):
        obs = make_obs(action="FOLD", equity_margin=-3.0, equity=0.17,
                       strategic_role="range_fold")
        assert _shared_burden_sentence(obs, "beginner") == ""

    def test_suppressed_when_not_multiway(self):
        """HU behaviour must not change."""
        obs = make_obs(is_multiway=False, num_opponents=1,
                       opponent_phrase="your opponent",
                       equity_margin=3.0)
        assert _shared_burden_sentence(obs, "intermediate") == ""
        assert _shared_burden_sentence(obs, "advanced") == ""

    def test_suppressed_when_not_facing_bet(self):
        obs = make_obs(facing_bet=False, equity_margin=3.0)
        assert _shared_burden_sentence(obs, "intermediate") == ""

    def test_suppressed_for_bet_action(self):
        obs = make_obs(action="BET", equity_margin=3.0)
        assert _shared_burden_sentence(obs, "intermediate") == ""

    def test_suppressed_for_check_action(self):
        obs = make_obs(action="CHECK", equity_margin=3.0, facing_bet=False)
        assert _shared_burden_sentence(obs, "intermediate") == ""

    def test_suppressed_margin_above_plus_five(self):
        """Window is [-8, +5]. Margin > +5 is a clear call, no shared burden."""
        obs = make_obs(equity_margin=6.0, equity=0.26)
        assert _shared_burden_sentence(obs, "intermediate") == ""

    def test_suppressed_margin_below_minus_eight(self):
        """Margin < -8 is a clear fold, no shared burden needed."""
        obs = make_obs(action="FOLD", equity_margin=-9.0, equity=0.11,
                       strategic_role="range_fold")
        assert _shared_burden_sentence(obs, "intermediate") == ""

    def test_fires_at_margin_exactly_plus_five(self):
        """Boundary: +5.0 is inside the window."""
        obs = make_obs(equity_margin=5.0, equity=0.25)
        result = _shared_burden_sentence(obs, "intermediate")
        assert result != ""

    def test_fires_at_margin_exactly_minus_eight(self):
        """Boundary: -8.0 is inside the window."""
        obs = make_obs(action="FOLD", equity_margin=-8.0, equity=0.12,
                       strategic_role="range_fold")
        result = _shared_burden_sentence(obs, "intermediate")
        assert result != ""


# ---------------------------------------------------------------------------
# Integration: render_intermediate and render_advanced wiring
# ---------------------------------------------------------------------------

class TestRenderIntermediateWiring:
    def test_draw_price_appears_in_sentences(self):
        obs = make_obs(equity_margin=15.0)
        sentences = render_intermediate(obs)
        full_text = " ".join(sentences)
        assert "right price" in full_text or "enough equity" in full_text

    def test_draw_price_not_in_hu_sentences(self):
        """HU: A-4 must NOT fire (is_multiway gate)."""
        obs = make_obs(is_multiway=False, num_opponents=1,
                       opponent_phrase="your opponent")
        sentences = render_intermediate(obs)
        full_text = " ".join(sentences)
        # A-4 multiway draw price sentinel phrase must not appear HU
        assert "outs gives you enough equity at this bet size" not in full_text

    def test_sentence_count_capped_at_three(self):
        obs = make_obs(equity_margin=15.0)
        sentences = render_intermediate(obs)
        assert len(sentences) <= 3

    def test_rio_appears_in_intermediate_flush_draw(self):
        obs = make_obs(equity_margin=15.0, draw_description="flush draw",
                       draw_outs=9, hero_label="9-high flush draw")
        sentences = render_intermediate(obs)
        full_text = " ".join(sentences)
        assert "higher flush" in full_text or "completing your draw" in full_text


class TestRenderAdvancedWiring:
    def test_draw_price_appears_in_sentences(self):
        obs = make_obs(equity_margin=15.0, draw_equity=0.35, pot_odds_pct=20.0)
        sentences = render_advanced(obs)
        full_text = " ".join(sentences)
        assert "35%" in full_text or "outs" in full_text

    def test_no_approximate_in_any_advanced_sentence(self):
        obs = make_obs(equity_margin=15.0, is_multiway=True)
        sentences = render_advanced(obs)
        for s in sentences:
            assert "(approximate)" not in s, f"Found '(approximate)' in: {s}"

    def test_no_tilde_in_draw_price_sentence(self):
        obs = make_obs(equity_margin=15.0, draw_equity=0.35, pot_odds_pct=20.0)
        sentences = render_advanced(obs)
        # Find the sentence that contains outs (draw price sentence)
        draw_sentences = [s for s in sentences if "outs" in s]
        for s in draw_sentences:
            assert "~" not in s, f"Found '~' in draw price sentence: {s}"

    def test_sentence_count_capped_at_three(self):
        obs = make_obs(equity_margin=15.0)
        sentences = render_advanced(obs)
        assert len(sentences) <= 3

    def test_rio_appears_in_advanced_flush_draw(self):
        obs = make_obs(equity_margin=15.0, draw_description="flush draw",
                       draw_outs=9, hero_label="9-high flush draw")
        sentences = render_advanced(obs)
        full_text = " ".join(sentences)
        assert "Reverse implied odds" in full_text or "non-nut" in full_text or "not to the nuts" in full_text

    def test_hu_not_affected(self):
        """Advanced HU: A-4 does not fire, no draw price framing in slot 2."""
        obs = make_obs(is_multiway=False, num_opponents=1,
                       opponent_phrase="your opponent")
        sentences = render_advanced(obs)
        full_text = " ".join(sentences)
        # Strategic frame should appear in HU (not draw price multiway framing)
        assert "profitable by" not in full_text  # Advanced draw price format
