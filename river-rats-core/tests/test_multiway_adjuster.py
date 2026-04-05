"""
Tests for multiway_adjuster.py

Covers:
  1. Passthrough for num_opponents <= 1 (all actions)
  2. Passthrough for FOLD / CHECK / CALL regardless of features
  3. Bluff suppression (equity < 0.30)
  4. Value tightening (equity between bluff threshold and value threshold)
  5. Raise demotion (equity between value and raise threshold)
  6. Draw check (OOP semi-bluff suppression and IP outs gating)
  7. Rule priority (bluff_suppression beats draw_check)
  8. Edge cases (num_opponents=0, very high num_opponents, all-zero features)
  9. Threshold boundary conditions
"""

import sys
sys.path.insert(0, '/home/rupertbeytell/river-rats/river-rats-complete')

from collections import namedtuple
import pytest

from multiway_adjuster import (
    adjust,
    AdjustedPrediction,
    BLUFF_EQUITY_THRESHOLD,
    RULE1_DRAW_BYPASS,
    VALUE_BASE_THRESHOLD,
    VALUE_PER_OPPONENT,
    RAISE_BASE_THRESHOLD,
    RAISE_PER_OPPONENT,
    MAX_OPPONENTS_CAP,
    DRAW_OUTS_IP_BASE,
    DRAW_OUTS_IP_PER_OPPONENT,
    EQUITY_REALIZATION_IP,
    EQUITY_REALIZATION_OOP,
    SIGMOID_TEMPERATURE,
    RULE4_EQUITY_EXCEPTION,
    _adjustment_probability,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

OraclePrediction = namedtuple("OraclePrediction", ["action"])


def _make_feat_dict(**overrides) -> dict:
    """
    Returns a default feature dict representing a typical hand with all 38
    model features set to reasonable defaults.  Override specific features
    via keyword arguments.
    """
    defaults = {
        # Equity / strength
        "equity_vs_range": 0.65,
        "raw_equity": 0.60,
        "hand_strength": 0.70,
        "nut_advantage": 0.50,
        "made_hand_strength": 0.65,
        # Draw features
        "draw_outs": 0,
        "flush_draw": 0,
        "straight_draw": 0,
        "combo_draw": 0,
        "backdoor_draw": 0,
        # Position
        "is_ip": 1,          # in position by default
        "position_score": 1,
        # Bet / action context
        "facing_bet": 0,
        "pot_odds": 0.25,
        "spr": 3.0,
        "effective_stack": 100,
        "pot_size": 20,
        "bet_size": 0,
        "call_amount": 0,
        "raise_size": 0,
        # Board texture
        "board_wetness": 0.4,
        "board_paired": 0,
        "board_monotone": 0,
        "high_card_rank": 12,
        "board_connectedness": 0.3,
        # Player / table
        "num_players": 2,
        "players_to_act": 1,
        "vpip": 0.25,
        "pfr": 0.18,
        "af": 2.0,
        "stack_depth": 100,
        # Street
        "street": 1,         # flop
        "is_preflop": 0,
        "is_flop": 1,
        "is_turn": 0,
        "is_river": 0,
        # Misc
        "fold_equity": 0.40,
        "pot_commitment": 0.15,
        "num_opponents": 1,
    }
    defaults.update(overrides)
    return defaults


def _pred(action: str) -> OraclePrediction:
    return OraclePrediction(action=action)


# ---------------------------------------------------------------------------
# 1. Passthrough tests -- num_opponents=1 (heads-up)
# ---------------------------------------------------------------------------

class TestHeadsUpPassthrough:
    """All actions pass through unchanged when num_opponents <= 1."""

    @pytest.mark.parametrize("action", ["BET", "RAISE", "CALL", "CHECK", "FOLD"])
    def test_hu_all_actions_unchanged(self, action):
        feat = _make_feat_dict(equity_vs_range=0.10)  # would trigger rules if multiway
        result = adjust(_pred(action), feat, num_opponents=1)
        assert result.adjusted_action == action
        assert result.was_adjusted is False
        assert result.adjustment_reason == ""
        assert result.num_opponents == 1

    @pytest.mark.parametrize("action", ["BET", "RAISE", "CALL", "CHECK", "FOLD"])
    def test_zero_opponents_treated_as_hu(self, action):
        feat = _make_feat_dict(equity_vs_range=0.05)
        result = adjust(_pred(action), feat, num_opponents=0)
        assert result.adjusted_action == action
        assert result.was_adjusted is False
        assert result.num_opponents == 0

    def test_negative_opponents_treated_as_hu(self):
        feat = _make_feat_dict(equity_vs_range=0.05)
        result = adjust(_pred("BET"), feat, num_opponents=-1)
        assert result.adjusted_action == "BET"
        assert result.was_adjusted is False


# ---------------------------------------------------------------------------
# 2. Passthrough for FOLD / CHECK / CALL -- never adjusted multiway
# ---------------------------------------------------------------------------

class TestPassiveActionsNeverAdjusted:

    @pytest.mark.parametrize("action", ["FOLD", "CHECK", "CALL"])
    def test_fold_check_call_pass_through_2way(self, action):
        feat = _make_feat_dict(equity_vs_range=0.05)  # horrible equity
        result = adjust(_pred(action), feat, num_opponents=2)
        assert result.adjusted_action == action
        assert result.was_adjusted is False

    @pytest.mark.parametrize("action", ["FOLD", "CHECK", "CALL"])
    def test_fold_check_call_pass_through_5way(self, action):
        feat = _make_feat_dict(equity_vs_range=0.05)
        result = adjust(_pred(action), feat, num_opponents=5)
        assert result.adjusted_action == action
        assert result.was_adjusted is False
        assert result.adjustment_reason == ""

    def test_call_passthrough_preserves_num_opponents(self):
        feat = _make_feat_dict()
        result = adjust(_pred("CALL"), feat, num_opponents=4)
        assert result.num_opponents == 4
        assert result.original_action == "CALL"


# ---------------------------------------------------------------------------
# 3. Bluff suppression tests
# ---------------------------------------------------------------------------

class TestBluffSuppression:

    def test_bet_low_equity_becomes_check_2opp(self):
        feat = _make_feat_dict(equity_vs_range=0.15, raw_equity=0.10)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjusted_action == "CHECK"
        assert result.was_adjusted is True
        assert result.adjustment_reason == "bluff_suppression"

    def test_raise_low_equity_becomes_fold_2opp(self):
        feat = _make_feat_dict(equity_vs_range=0.15, raw_equity=0.10)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjusted_action == "FOLD"
        assert result.was_adjusted is True
        assert result.adjustment_reason == "bluff_suppression"

    def test_bet_low_equity_becomes_check_3opp(self):
        # Override raw_equity too: max(equity_vs_range, raw_equity) must be below threshold
        feat = _make_feat_dict(equity_vs_range=0.10, raw_equity=0.10)
        result = adjust(_pred("BET"), feat, num_opponents=3)
        assert result.adjusted_action == "CHECK"
        assert result.adjustment_reason == "bluff_suppression"

    def test_raise_low_equity_becomes_fold_5opp(self):
        # Override raw_equity too so max() doesn't rescue the equity above the threshold
        feat = _make_feat_dict(equity_vs_range=0.05, raw_equity=0.05)
        result = adjust(_pred("RAISE"), feat, num_opponents=5)
        assert result.adjusted_action == "FOLD"
        assert result.adjustment_reason == "bluff_suppression"

    def test_bluff_suppression_uses_max_of_both_equities(self):
        # raw_equity is above threshold even though equity_vs_range is below
        feat = _make_feat_dict(equity_vs_range=0.10, raw_equity=0.35)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        # max equity = 0.35 >= 0.30, so bluff suppression should NOT fire
        assert result.adjustment_reason != "bluff_suppression"

    def test_bluff_suppression_fires_when_both_equities_low(self):
        # With BLUFF_EQUITY_THRESHOLD=0.19, need equity well below 0.19
        feat = _make_feat_dict(equity_vs_range=0.15, raw_equity=0.12)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason == "bluff_suppression"

    def test_bluff_threshold_boundary_just_below(self):
        # equity = 0.2999... triggers suppression
        equity = BLUFF_EQUITY_THRESHOLD - 0.0001
        feat = _make_feat_dict(equity_vs_range=equity, raw_equity=0.0)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason == "bluff_suppression"

    def test_bluff_threshold_boundary_at_exact_value(self):
        # equity exactly at threshold does NOT trigger bluff suppression (strict <)
        feat = _make_feat_dict(equity_vs_range=BLUFF_EQUITY_THRESHOLD, raw_equity=0.0)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason != "bluff_suppression"

    def test_bluff_suppression_bypassed_with_draws(self):
        """Hands with 6+ draw outs bypass bluff suppression."""
        feat = _make_feat_dict(equity_vs_range=0.20, raw_equity=0.20, draw_outs=8)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        # Should NOT be bluff_suppression -- draw bypass lets it fall through
        assert result.adjustment_reason != "bluff_suppression"

    def test_bluff_suppression_fires_without_draws(self):
        """Hands without draws still get bluff-suppressed."""
        feat = _make_feat_dict(equity_vs_range=0.15, raw_equity=0.12, draw_outs=0)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason == "bluff_suppression"

    def test_bluff_suppression_fires_with_few_draws(self):
        """Hands with <8 outs still get bluff-suppressed (RULE1_DRAW_BYPASS=8)."""
        feat = _make_feat_dict(equity_vs_range=0.15, raw_equity=0.12, draw_outs=4)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason == "bluff_suppression"


# ---------------------------------------------------------------------------
# 4. Value tightening tests
# ---------------------------------------------------------------------------

class TestValueTightening:

    def test_bet_moderate_equity_2opp_becomes_check(self):
        # 2 opponents: value_threshold = 0.40 + 1*0.00 = 0.40
        # equity = 0.38 < 0.40, triggers value_tightening
        feat = _make_feat_dict(equity_vs_range=0.38, raw_equity=0.35)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjusted_action == "CHECK"
        assert result.adjustment_reason == "value_tightening"

    def test_raise_moderate_equity_facing_bet_becomes_call(self):
        # RAISE uses raise_demotion rule; equity=0.45 < raise_threshold(2opp)=0.47, facing a bet
        feat = _make_feat_dict(equity_vs_range=0.45, raw_equity=0.42,
                               facing_bet=1)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjusted_action == "CALL"
        assert result.adjustment_reason == "raise_demotion"

    def test_raise_moderate_equity_not_facing_bet_becomes_check(self):
        # RAISE uses raise_demotion rule; equity=0.45 < raise_threshold(2opp)=0.47, not facing a bet
        feat = _make_feat_dict(equity_vs_range=0.45, raw_equity=0.42,
                               facing_bet=0)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjusted_action == "CHECK"
        assert result.adjustment_reason == "raise_demotion"

    def test_value_threshold_flat_across_opponents(self):
        # PER_OPP=0.00: threshold is flat at 0.40 for all opponent counts
        # equity = 0.38 < 0.40 -> value_tightening for ALL opponent counts
        for n_opp in [2, 3, 4, 5]:
            feat = _make_feat_dict(equity_vs_range=0.38, raw_equity=0.35)
            result = adjust(_pred("BET"), feat, num_opponents=n_opp)
            assert result.adjustment_reason == "value_tightening", (
                f"Expected value_tightening for {n_opp} opponents"
            )
        # equity = 0.42 > 0.40 -> NO value_tightening for ANY opponent count
        for n_opp in [2, 3, 4, 5]:
            feat = _make_feat_dict(equity_vs_range=0.42, raw_equity=0.42)
            result = adjust(_pred("BET"), feat, num_opponents=n_opp)
            assert result.adjustment_reason != "value_tightening", (
                f"Should NOT trigger value_tightening for {n_opp} opponents"
            )

    def test_value_threshold_4opp_just_above_does_not_trigger(self):
        # 4 opponents: value_threshold = 0.50 + 3*0.05 = 0.65; equity = 0.72 -> no tightening
        feat = _make_feat_dict(equity_vs_range=0.72, raw_equity=0.72)
        result = adjust(_pred("BET"), feat, num_opponents=4)
        assert result.adjustment_reason != "value_tightening"

    def test_value_tightening_capped_at_5_opponents(self):
        # Cap: n=5, value_threshold = 0.50 + 4*0.05 = 0.70
        # 8 opponents should use same threshold as 5
        feat_8 = _make_feat_dict(equity_vs_range=0.77, raw_equity=0.77)
        feat_5 = _make_feat_dict(equity_vs_range=0.77, raw_equity=0.77)
        result_8 = adjust(_pred("BET"), feat_8, num_opponents=8)
        result_5 = adjust(_pred("BET"), feat_5, num_opponents=5)
        assert result_8.adjustment_reason == result_5.adjustment_reason


# ---------------------------------------------------------------------------
# 5. Raise demotion tests
# ---------------------------------------------------------------------------

class TestRaiseDemotion:

    def test_raise_below_raise_threshold_facing_bet_becomes_call(self):
        # 2 opponents: raise_threshold = 0.45 + 1*0.02 = 0.47
        # equity = 0.45 is above value_threshold(0.40) but below raise_threshold(0.47)
        feat = _make_feat_dict(equity_vs_range=0.45, raw_equity=0.45,
                               facing_bet=1)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjusted_action == "CALL"
        assert result.adjustment_reason == "raise_demotion"

    def test_raise_below_raise_threshold_not_facing_bet_becomes_check(self):
        # equity = 0.45 is above value_threshold(0.40) but below raise_threshold(0.47)
        feat = _make_feat_dict(equity_vs_range=0.45, raw_equity=0.45,
                               facing_bet=0)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjusted_action == "CHECK"
        assert result.adjustment_reason == "raise_demotion"

    def test_raise_above_raise_threshold_passes_through(self):
        # 2 opponents: raise_threshold = 0.45+1*0.02=0.47; equity = 0.70 -> no demotion
        feat = _make_feat_dict(equity_vs_range=0.70, raw_equity=0.70)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjustment_reason != "raise_demotion"
        assert result.was_adjusted is False

    def test_raise_demotion_threshold_scales_with_opponents(self):
        # PER_OPP=0.02: raise threshold = 0.45 + 0.02*(n-1)
        # equity = 0.42 < threshold for all opponent counts -> raise_demotion
        for n_opp in [2, 3, 4, 5]:
            feat = _make_feat_dict(equity_vs_range=0.42, raw_equity=0.42,
                                   facing_bet=1)
            result = adjust(_pred("RAISE"), feat, num_opponents=n_opp)
            assert result.adjustment_reason == "raise_demotion", (
                f"Expected raise_demotion for {n_opp} opponents"
            )
        # equity = 0.55 > max threshold (0.45+4*0.02=0.53) -> NO raise_demotion
        for n_opp in [2, 3, 4, 5]:
            feat = _make_feat_dict(equity_vs_range=0.55, raw_equity=0.55)
            result = adjust(_pred("RAISE"), feat, num_opponents=n_opp)
            assert result.adjustment_reason != "raise_demotion", (
                f"Should NOT trigger raise_demotion for {n_opp} opponents"
            )

    def test_raise_demotion_boundary_just_below_threshold(self):
        # 2 opp: raise_threshold = 0.65
        equity = RAISE_BASE_THRESHOLD + 1 * RAISE_PER_OPPONENT - 0.001
        feat = _make_feat_dict(equity_vs_range=equity, raw_equity=equity,
                               facing_bet=1)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjustment_reason == "raise_demotion"

    def test_raise_demotion_boundary_at_exact_threshold(self):
        # equity exactly at threshold should NOT trigger demotion (strict <)
        equity = RAISE_BASE_THRESHOLD + 1 * RAISE_PER_OPPONENT
        feat = _make_feat_dict(equity_vs_range=equity, raw_equity=equity)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjustment_reason != "raise_demotion"


# ---------------------------------------------------------------------------
# 6. Draw check tests
# ---------------------------------------------------------------------------

class TestDrawCheck:

    def test_bet_with_draws_oop_always_becomes_check(self):
        feat = _make_feat_dict(
            equity_vs_range=0.65,
            raw_equity=0.65,
            draw_outs=4,
            is_ip=0,
        )
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjusted_action == "CHECK"
        assert result.adjustment_reason == "draw_check"

    def test_bet_with_draws_oop_3opp_becomes_check(self):
        feat = _make_feat_dict(
            equity_vs_range=0.65,
            draw_outs=9,
            is_ip=0,
        )
        result = adjust(_pred("BET"), feat, num_opponents=3)
        assert result.adjustment_reason == "draw_check"

    def test_bet_no_draws_oop_no_draw_check(self):
        feat = _make_feat_dict(
            equity_vs_range=0.65,
            draw_outs=0,
            is_ip=0,
        )
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason != "draw_check"

    def test_bet_with_draws_ip_sufficient_outs_passes_through(self):
        # 2 opponents: ip_threshold = 8 + 1*1 = 9; draw_outs=12 >= 9 -> pass
        feat = _make_feat_dict(
            equity_vs_range=0.65,
            draw_outs=12,
            is_ip=1,
        )
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason != "draw_check"
        assert result.was_adjusted is False

    def test_bet_with_draws_ip_insufficient_outs_becomes_check(self):
        # 2 opponents: ip_threshold = 8 + 1*1 = 9; draw_outs=8 < 9 -> draw_check
        feat = _make_feat_dict(
            equity_vs_range=0.65,
            draw_outs=8,
            is_ip=1,
        )
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjusted_action == "CHECK"
        assert result.adjustment_reason == "draw_check"

    def test_draw_check_ip_threshold_scales_with_opponents(self):
        # 4 opponents (n=4): ip_threshold = 8 + 3*1 = 11, draw_outs=10 < 11 -> draw_check
        # value_threshold(4 opp) = 0.50 + 3*0.05 = 0.65, so equity must be >= 0.65
        # to clear value_tightening and reach the draw_check rule.
        feat = _make_feat_dict(
            equity_vs_range=0.75,
            raw_equity=0.75,
            draw_outs=10,
            is_ip=1,
        )
        result = adjust(_pred("BET"), feat, num_opponents=4)
        assert result.adjustment_reason == "draw_check"

    def test_draw_check_ip_threshold_just_meets_cutoff(self):
        # 4 opponents: ip_threshold = 14; draw_outs=14 -> no draw_check
        feat = _make_feat_dict(
            equity_vs_range=0.65,
            draw_outs=14,
            is_ip=1,
        )
        result = adjust(_pred("BET"), feat, num_opponents=4)
        assert result.adjustment_reason != "draw_check"

    def test_raise_with_draws_not_subject_to_draw_check(self):
        # draw_check rule only applies to BET actions
        feat = _make_feat_dict(
            equity_vs_range=0.65,
            draw_outs=4,
            is_ip=0,
        )
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjustment_reason != "draw_check"


# ---------------------------------------------------------------------------
# 7. Rule priority tests
# ---------------------------------------------------------------------------

class TestRulePriority:

    def test_bluff_suppression_beats_draw_check_bet_oop_few_outs(self):
        # Low equity AND few draws OOP -> bluff_suppression fires first (Rule 1 before Rule 4)
        # draw_outs < RULE1_DRAW_BYPASS so no bypass
        feat = _make_feat_dict(
            equity_vs_range=0.20,
            raw_equity=0.20,
            draw_outs=4,
            is_ip=0,
        )
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason == "bluff_suppression"
        assert result.adjusted_action == "CHECK"

    def test_bluff_suppression_beats_draw_check_raise_oop_few_outs(self):
        # RAISE with low equity and few draws -> FOLD via bluff_suppression, not draw_check
        feat = _make_feat_dict(
            equity_vs_range=0.20,
            raw_equity=0.20,
            draw_outs=4,
            is_ip=0,
        )
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjustment_reason == "bluff_suppression"
        assert result.adjusted_action == "FOLD"

    def test_draw_bypass_overrides_bluff_suppression_bet_oop(self):
        # Low equity but 8+ draw outs -> bypass bluff suppression (RULE1_DRAW_BYPASS=8)
        # Falls through to Rule 2 (value_tightening) since equity 0.15 < 0.40
        feat = _make_feat_dict(
            equity_vs_range=0.15,
            raw_equity=0.12,
            draw_outs=8,
            is_ip=0,
        )
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason != "bluff_suppression"

    def test_raise_below_raise_threshold_uses_raise_demotion(self):
        # RAISE actions now use raise_demotion rule exclusively (Rule 3).
        # 2 opp: raise_threshold=0.45+1*0.02=0.47; equity=0.45 < 0.47 -> raise_demotion
        feat = _make_feat_dict(equity_vs_range=0.45, raw_equity=0.45,
                               facing_bet=1)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjustment_reason == "raise_demotion"

    def test_bluff_suppression_beats_value_tightening(self):
        # equity < BLUFF_EQUITY_THRESHOLD=0.19 -> bluff_suppression (Rule 1)
        # even though it would also fail value_tightening (Rule 2)
        feat = _make_feat_dict(equity_vs_range=0.15, raw_equity=0.12)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason == "bluff_suppression"


# ---------------------------------------------------------------------------
# 8. Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def test_num_opponents_8_capped_same_as_5(self):
        # Behaviour with 8 opponents should match 5 (cap = MAX_OPPONENTS_CAP)
        feat = _make_feat_dict(equity_vs_range=0.55, raw_equity=0.55)
        result_8 = adjust(_pred("BET"), feat, num_opponents=8)
        result_5 = adjust(_pred("BET"), feat, num_opponents=5)
        assert result_8.adjustment_reason == result_5.adjustment_reason
        assert result_8.adjusted_action == result_5.adjusted_action

    def test_all_features_zero_bet(self):
        # With all-zero features equity=0 -> bluff_suppression
        feat = {k: 0 for k in _make_feat_dict()}
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason == "bluff_suppression"

    def test_all_features_zero_raise(self):
        feat = {k: 0 for k in _make_feat_dict()}
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjustment_reason == "bluff_suppression"
        assert result.adjusted_action == "FOLD"

    def test_missing_equity_features_defaults_to_zero(self):
        # feat_dict with no equity keys at all
        feat = {}
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason == "bluff_suppression"

    def test_returns_adjusted_prediction_dataclass(self):
        feat = _make_feat_dict()
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert isinstance(result, AdjustedPrediction)

    def test_original_action_preserved_on_adjustment(self):
        # Override raw_equity so max() is also low and bluff_suppression fires
        feat = _make_feat_dict(equity_vs_range=0.10, raw_equity=0.10)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.original_action == "BET"
        assert result.adjusted_action == "CHECK"

    def test_num_opponents_preserved_in_result(self):
        feat = _make_feat_dict()
        result = adjust(_pred("BET"), feat, num_opponents=3)
        assert result.num_opponents == 3

    def test_high_equity_bet_no_draws_passes_through(self):
        feat = _make_feat_dict(equity_vs_range=0.90, raw_equity=0.90, draw_outs=0)
        result = adjust(_pred("BET"), feat, num_opponents=4)
        assert result.was_adjusted is False
        assert result.adjusted_action == "BET"

    def test_high_equity_raise_no_draws_passes_through(self):
        feat = _make_feat_dict(equity_vs_range=0.90, raw_equity=0.90)
        result = adjust(_pred("RAISE"), feat, num_opponents=5)
        assert result.was_adjusted is False
        assert result.adjusted_action == "RAISE"


# ---------------------------------------------------------------------------
# 9. Threshold boundary tests
# ---------------------------------------------------------------------------

class TestThresholdBoundaries:

    def test_equity_exactly_at_value_threshold_2opp_no_tightening(self):
        # value_threshold (2 opp) = 0.50 + 1*0.07 = 0.57; equity=0.57 -> pass
        equity = VALUE_BASE_THRESHOLD + 1 * VALUE_PER_OPPONENT
        feat = _make_feat_dict(equity_vs_range=equity, raw_equity=equity)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason != "value_tightening"

    def test_equity_just_below_value_threshold_2opp_tightens(self):
        equity = VALUE_BASE_THRESHOLD + 1 * VALUE_PER_OPPONENT - 0.001
        feat = _make_feat_dict(equity_vs_range=equity, raw_equity=equity)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason == "value_tightening"

    def test_equity_exactly_at_raise_threshold_2opp_no_demotion(self):
        # raise_threshold (2 opp) = 0.60 + 1*0.05 = 0.65; equity=0.65 -> pass
        equity = RAISE_BASE_THRESHOLD + 1 * RAISE_PER_OPPONENT
        feat = _make_feat_dict(equity_vs_range=equity, raw_equity=equity)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjustment_reason != "raise_demotion"

    def test_equity_just_below_raise_threshold_2opp_demoted(self):
        equity = RAISE_BASE_THRESHOLD + 1 * RAISE_PER_OPPONENT - 0.001
        # Must also be above value_threshold to reach raise_demotion rule
        value_threshold = VALUE_BASE_THRESHOLD + 1 * VALUE_PER_OPPONENT
        if equity < value_threshold:
            pytest.skip("equity below value_threshold -- would trigger value_tightening instead")
        feat = _make_feat_dict(equity_vs_range=equity, raw_equity=equity,
                               facing_bet=1)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjustment_reason == "raise_demotion"

    def test_draw_outs_exactly_at_ip_threshold_passes(self):
        # 2 opp: ip_threshold = 8 + 1*2 = 10; draw_outs=10 -> pass
        ip_threshold = DRAW_OUTS_IP_BASE + 1 * DRAW_OUTS_IP_PER_OPPONENT
        feat = _make_feat_dict(
            equity_vs_range=0.65,
            draw_outs=ip_threshold,
            is_ip=1,
        )
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason != "draw_check"

    def test_draw_outs_one_below_ip_threshold_triggers_draw_check(self):
        ip_threshold = DRAW_OUTS_IP_BASE + 1 * DRAW_OUTS_IP_PER_OPPONENT
        feat = _make_feat_dict(
            equity_vs_range=0.65,
            draw_outs=ip_threshold - 1,
            is_ip=1,
        )
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason == "draw_check"

    def test_max_opponents_cap_exact(self):
        # n=MAX_OPPONENTS_CAP should be used exactly at the cap value
        n = MAX_OPPONENTS_CAP
        value_threshold = VALUE_BASE_THRESHOLD + (n - 1) * VALUE_PER_OPPONENT
        equity = value_threshold - 0.01
        feat = _make_feat_dict(equity_vs_range=equity, raw_equity=equity)
        result = adjust(_pred("BET"), feat, num_opponents=n)
        assert result.adjustment_reason == "value_tightening"


# ---------------------------------------------------------------------------
# 10. Equity realization tests
# ---------------------------------------------------------------------------

class TestEquityRealization:

    def test_ip_gets_full_realization(self):
        """IP hands use full equity (realization factor 1.0)."""
        # equity 0.42 > value threshold 0.40 -> no adjustment when IP
        feat = _make_feat_dict(equity_vs_range=0.42, raw_equity=0.42, is_ip=1)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.was_adjusted is False

    def test_oop_gets_discounted_realization(self):
        """OOP hands get discounted equity (0.42 * 0.85 = 0.357 < 0.40 threshold)."""
        feat = _make_feat_dict(equity_vs_range=0.42, raw_equity=0.42, is_ip=0)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.was_adjusted is True
        assert result.adjustment_reason == "value_tightening"

    def test_oop_needs_more_equity_for_same_outcome(self):
        """OOP needs ~18% more raw equity to pass the same threshold as IP."""
        # IP at 0.42 passes value threshold (0.40)
        feat_ip = _make_feat_dict(equity_vs_range=0.42, raw_equity=0.42, is_ip=1)
        result_ip = adjust(_pred("BET"), feat_ip, num_opponents=2)
        assert result_ip.was_adjusted is False

        # OOP needs 0.40/0.85 ≈ 0.471 to pass value threshold
        feat_oop_low = _make_feat_dict(equity_vs_range=0.46, raw_equity=0.46, is_ip=0)
        result_oop_low = adjust(_pred("BET"), feat_oop_low, num_opponents=2)
        assert result_oop_low.was_adjusted is True  # 0.46*0.85=0.391 < 0.40

        feat_oop_high = _make_feat_dict(equity_vs_range=0.48, raw_equity=0.48, is_ip=0)
        result_oop_high = adjust(_pred("BET"), feat_oop_high, num_opponents=2)
        assert result_oop_high.was_adjusted is False  # 0.48*0.85=0.408 > 0.40

    def test_oop_bluff_suppression_more_aggressive(self):
        """OOP bluff suppression fires at higher raw equities due to realization discount."""
        # equity 0.33, IP realized=0.33 > 0.30 -> no bluff suppression
        feat_ip = _make_feat_dict(equity_vs_range=0.33, raw_equity=0.33, is_ip=1)
        result_ip = adjust(_pred("BET"), feat_ip, num_opponents=2)
        assert result_ip.adjustment_reason != "bluff_suppression"

        # equity 0.33, OOP realized=0.33*0.85=0.2805 < 0.30 -> bluff suppression
        feat_oop = _make_feat_dict(equity_vs_range=0.33, raw_equity=0.33, is_ip=0)
        result_oop = adjust(_pred("BET"), feat_oop, num_opponents=2)
        assert result_oop.adjustment_reason == "bluff_suppression"

    def test_oop_raise_demotion_more_aggressive(self):
        """OOP raise demotion fires at higher raw equities."""
        # equity 0.55, IP realized=0.55 > 0.50 -> no demotion
        feat_ip = _make_feat_dict(equity_vs_range=0.55, raw_equity=0.55,
                                  is_ip=1, facing_bet=1)
        result_ip = adjust(_pred("RAISE"), feat_ip, num_opponents=2)
        assert result_ip.was_adjusted is False

        # equity 0.55, OOP realized=0.4675 < 0.50 -> raise demotion
        feat_oop = _make_feat_dict(equity_vs_range=0.55, raw_equity=0.55,
                                   is_ip=0, facing_bet=1)
        result_oop = adjust(_pred("RAISE"), feat_oop, num_opponents=2)
        assert result_oop.adjustment_reason == "raise_demotion"

    def test_realization_constants_have_expected_values(self):
        assert EQUITY_REALIZATION_IP == 1.00
        assert EQUITY_REALIZATION_OOP == 0.85


# ---------------------------------------------------------------------------
# 11. Sigmoid transition function tests
# ---------------------------------------------------------------------------

class TestSigmoidTransition:

    def test_sigmoid_at_threshold_returns_half(self):
        """At equity == threshold, probability should be exactly 0.5."""
        prob = _adjustment_probability(0.40, 0.40, temperature=0.05)
        assert abs(prob - 0.5) < 1e-10

    def test_sigmoid_below_threshold_approaches_one(self):
        """Well below threshold, probability approaches 1.0."""
        prob = _adjustment_probability(0.10, 0.40, temperature=0.05)
        assert prob > 0.99

    def test_sigmoid_above_threshold_approaches_zero(self):
        """Well above threshold, probability approaches 0.0."""
        prob = _adjustment_probability(0.70, 0.40, temperature=0.05)
        assert prob < 0.01

    def test_sigmoid_monotonically_decreasing(self):
        """Higher equity -> lower adjustment probability."""
        probs = [_adjustment_probability(eq, 0.40, temperature=0.05)
                 for eq in [0.30, 0.35, 0.40, 0.45, 0.50]]
        for i in range(len(probs) - 1):
            assert probs[i] > probs[i + 1]

    def test_temperature_controls_sharpness(self):
        """Lower temperature = sharper transition (more extreme values near threshold)."""
        # At threshold + 0.02: sharp temp should be closer to 0 than smooth temp
        sharp = _adjustment_probability(0.42, 0.40, temperature=0.01)
        smooth = _adjustment_probability(0.42, 0.40, temperature=0.10)
        assert sharp < smooth  # sharp is closer to 0

    def test_sigmoid_no_overflow_extreme_values(self):
        """Sigmoid handles extreme equity values without overflow."""
        prob_low = _adjustment_probability(-1.0, 0.40, temperature=0.05)
        prob_high = _adjustment_probability(2.0, 0.40, temperature=0.05)
        assert prob_low > 0.99
        assert prob_high < 0.01

    def test_adjustment_confidence_stored_on_result(self):
        """AdjustedPrediction carries the sigmoid confidence score."""
        # Equity 0.38 < value_threshold 0.40 -> value_tightening with confidence
        feat = _make_feat_dict(equity_vs_range=0.38, raw_equity=0.38, is_ip=1)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.was_adjusted is True
        assert 0.5 < result.adjustment_confidence <= 1.0

    def test_confidence_higher_when_further_below_threshold(self):
        """Further below threshold -> higher confidence."""
        feat_close = _make_feat_dict(equity_vs_range=0.39, raw_equity=0.39, is_ip=1)
        feat_far = _make_feat_dict(equity_vs_range=0.36, raw_equity=0.36, is_ip=1)
        r_close = adjust(_pred("BET"), feat_close, num_opponents=2)
        r_far = adjust(_pred("BET"), feat_far, num_opponents=2)
        assert r_close.adjustment_reason == "value_tightening"
        assert r_far.adjustment_reason == "value_tightening"
        assert r_far.adjustment_confidence > r_close.adjustment_confidence

    def test_passthrough_has_default_confidence(self):
        """Non-adjusted results have default confidence of 1.0."""
        feat = _make_feat_dict(equity_vs_range=0.65, raw_equity=0.65, is_ip=1)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.was_adjusted is False
        assert result.adjustment_confidence == 1.0

    def test_sigmoid_temperature_constant_exists(self):
        assert SIGMOID_TEMPERATURE == 0.05


# ---------------------------------------------------------------------------
# 12. Fix verification tests — Rule 3 raise_demotion equity floor
# ---------------------------------------------------------------------------

class TestRaiseDemotionEquityFloor:

    def test_raise_sub_bluff_equity_facing_bet_folds(self):
        """RAISE with equity < BLUFF_EQUITY_THRESHOLD + facing bet + draw bypass -> FOLD."""
        # equity=0.15 < BLUFF_EQUITY_THRESHOLD=0.19
        # draw_outs=9 >= RULE1_DRAW_BYPASS=8, so Rule 1 is bypassed
        # realized_equity=0.15 < RAISE_BASE_THRESHOLD=0.45, so Rule 3 fires
        # realized_equity=0.15 < BLUFF_EQUITY_THRESHOLD=0.19 -> FOLD
        feat = _make_feat_dict(equity_vs_range=0.15, raw_equity=0.15,
                               facing_bet=1, draw_outs=9, is_ip=1)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjusted_action == "FOLD"
        assert result.adjustment_reason == "raise_demotion_to_fold"

    def test_raise_between_bluff_and_raise_thresholds_facing_bet_calls(self):
        """RAISE with equity between bluff and raise thresholds + facing bet -> CALL."""
        # equity=0.40 > BLUFF_EQUITY_THRESHOLD=0.19 but < raise_threshold(2opp)=0.47
        feat = _make_feat_dict(equity_vs_range=0.40, raw_equity=0.40,
                               facing_bet=1, is_ip=1)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjusted_action == "CALL"
        assert result.adjustment_reason == "raise_demotion"


# ---------------------------------------------------------------------------
# 13. Fix verification tests — Rule 4 OOP monster draw exception
# ---------------------------------------------------------------------------

class TestOOPMonsterDrawException:

    def test_oop_monster_draw_passes_through(self):
        """OOP monster draw (12+ outs, 40%+ realized equity) can bet."""
        # draw_outs=14 >= 12, equity=0.50, OOP realized=0.50*0.85=0.425 >= 0.40
        # Value threshold check: realized 0.425 > VALUE_BASE_THRESHOLD 0.40 -> passes
        # Rule 4: monster draw exception lets it through
        feat = _make_feat_dict(equity_vs_range=0.50, raw_equity=0.50,
                               draw_outs=14, is_ip=0)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason != "draw_check"
        assert result.adjusted_action == "BET"

    def test_oop_regular_draw_still_checks(self):
        """OOP regular draw (8 outs, 30% equity) still checks."""
        # draw_outs=8 < 12, so monster draw exception does NOT apply
        feat = _make_feat_dict(equity_vs_range=0.65, raw_equity=0.65,
                               draw_outs=8, is_ip=0)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjusted_action == "CHECK"
        assert result.adjustment_reason == "draw_check"

    def test_oop_many_outs_but_low_equity_still_checks(self):
        """OOP with 12+ outs but realized equity < 0.40 still checks."""
        # draw_outs=14 >= 12 but equity=0.40, OOP realized=0.40*0.85=0.34 < 0.40
        # NOTE: this hand also triggers value_tightening (0.34 < 0.40)
        # Value tightening (Rule 2) fires before Rule 4
        feat = _make_feat_dict(equity_vs_range=0.40, raw_equity=0.40,
                               draw_outs=14, is_ip=0)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjusted_action == "CHECK"


# ---------------------------------------------------------------------------
# 14. Rule 4 equity exception tests
# ---------------------------------------------------------------------------

class TestRule4EquityException:

    def test_oop_high_equity_with_draws_passes_through(self):
        """OOP hand with 70% equity + 3 draw outs passes through (no CHECK).
        realized_equity = 0.70 (IP-equivalent since we need 0.65 realized).
        For OOP: need raw equity >= 0.65/0.85 = 0.765. Use 0.80.
        realized = 0.80 * 0.85 = 0.68 >= 0.65 -> equity exception.
        """
        feat = _make_feat_dict(equity_vs_range=0.80, raw_equity=0.80,
                               draw_outs=3, is_ip=0)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjustment_reason != "draw_check"
        assert result.adjusted_action == "BET"

    def test_oop_below_equity_exception_with_draws_checks(self):
        """OOP hand with 60% equity + 3 draw outs -> CHECK (below 0.65).
        realized = 0.60 * 0.85 = 0.51 < 0.65 -> no exception, draw_check fires.
        """
        feat = _make_feat_dict(equity_vs_range=0.60, raw_equity=0.60,
                               draw_outs=3, is_ip=0)
        result = adjust(_pred("BET"), feat, num_opponents=2)
        assert result.adjusted_action == "CHECK"
        assert result.adjustment_reason == "draw_check"

    def test_rule4_equity_exception_constant_value(self):
        assert RULE4_EQUITY_EXCEPTION == 0.65


# ---------------------------------------------------------------------------
# 15. RAISE_PER_OPPONENT scaling tests
# ---------------------------------------------------------------------------

class TestRaisePerOpponent:

    def test_raise_demoted_with_per_opponent_scaling(self):
        """RAISE with 0.46 equity vs 2 opponents: threshold = 0.45+1*0.02=0.47.
        0.46 < 0.47 -> demoted to CALL."""
        feat = _make_feat_dict(equity_vs_range=0.46, raw_equity=0.46,
                               facing_bet=1, is_ip=1)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.adjusted_action == "CALL"
        assert result.adjustment_reason == "raise_demotion"

    def test_raise_passes_with_sufficient_equity(self):
        """RAISE with 0.48 equity vs 2 opponents: threshold = 0.47.
        0.48 > 0.47 -> passes through."""
        feat = _make_feat_dict(equity_vs_range=0.48, raw_equity=0.48,
                               is_ip=1)
        result = adjust(_pred("RAISE"), feat, num_opponents=2)
        assert result.was_adjusted is False
        assert result.adjusted_action == "RAISE"
