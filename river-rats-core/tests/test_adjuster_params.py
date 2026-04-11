"""Tests for multiway_adjuster params dict support.

Blocker 4: adjust() accepts a params dict instead of reading globals.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dataclasses import dataclass
from multiway_adjuster import adjust, get_default_params, AdjustedPrediction
from feature_keys import F


@dataclass
class FakePred:
    action: str


def _make_feat(equity=0.5, is_ip=1, draw_outs=0, facing_bet=0,
               num_raises=0, pot_size=100, to_call=33):
    return {
        F.RAW_EQUITY: equity,
        F.EQUITY_VS_RANGE: equity,
        F.IS_IP: is_ip,
        F.DRAW_OUTS: draw_outs,
        F.FACING_BET: facing_bet,
        F.META_NUM_RAISES: num_raises,
        F.POT_SIZE: pot_size,
        F.TO_CALL: to_call,
        F.HAND_CATEGORY: 5,
        F.HAS_FLUSH_DRAW: 0,
        F.HAS_STRAIGHT_DRAW: 0,
    }


class TestParamsDict:
    """adjust() uses params dict when provided."""

    def test_default_params_returns_dict(self):
        p = get_default_params()
        assert isinstance(p, dict)
        assert 'bluff_eq_thresh' in p
        assert 'cold_call_base' in p

    def test_no_params_uses_globals(self):
        """Without params, behavior matches existing defaults."""
        pred = FakePred(action='BET')
        feat = _make_feat(equity=0.10)  # Low equity → bluff suppression
        result = adjust(pred, feat, num_opponents=3)
        assert result.was_adjusted
        assert result.adjustment_reason == 'bluff_suppression'

    def test_params_override_bluff_threshold(self):
        """With higher bluff threshold in params, same hand is NOT suppressed."""
        pred = FakePred(action='BET')
        feat = _make_feat(equity=0.35)  # Above default 0.30 threshold

        # Default: should pass through (equity > 0.30)
        result_default = adjust(pred, feat, num_opponents=3)
        assert not result_default.was_adjusted or result_default.adjustment_reason != 'bluff_suppression'

        # Override: raise threshold to 0.40, now 0.35 is below → suppressed
        params = {'bluff_eq_thresh': 0.40}
        result_override = adjust(pred, feat, num_opponents=3, params=params)
        assert result_override.was_adjusted
        assert result_override.adjustment_reason == 'bluff_suppression'

    def test_params_override_cold_call(self):
        """Cold-call base can be overridden via params."""
        pred = FakePred(action='CALL')
        feat = _make_feat(equity=0.55, num_raises=1, facing_bet=1)

        # With very high cold_call_base, this should fold
        params = {'cold_call_base': 0.70}
        result = adjust(pred, feat, num_opponents=2, params=params)
        assert result.was_adjusted
        assert result.adjusted_action == 'FOLD'

    def test_params_none_same_as_no_params(self):
        """Explicitly passing params=None gives same result as no params."""
        pred = FakePred(action='BET')
        feat = _make_feat(equity=0.10)
        r1 = adjust(pred, feat, num_opponents=3)
        r2 = adjust(pred, feat, num_opponents=3, params=None)
        assert r1.adjusted_action == r2.adjusted_action
        assert r1.adjustment_reason == r2.adjustment_reason

    def test_partial_params_falls_back(self):
        """Params dict with only some keys — others fall back to globals."""
        pred = FakePred(action='BET')
        feat = _make_feat(equity=0.10)
        # Only override one param, others use defaults
        params = {'cold_call_base': 0.99}
        result = adjust(pred, feat, num_opponents=3, params=params)
        # bluff_suppression should still fire using default bluff threshold
        assert result.was_adjusted
        assert result.adjustment_reason == 'bluff_suppression'

    def test_two_variants_different_results(self):
        """Same hand, two different param sets → different actions."""
        pred = FakePred(action='BET')
        feat = _make_feat(equity=0.35)  # Between 0.30 and 0.40

        params_loose = {'bluff_eq_thresh': 0.20}  # 0.35 > 0.20 → no suppression
        params_tight = {'bluff_eq_thresh': 0.40}  # 0.35 < 0.40 → suppressed

        r_loose = adjust(pred, feat, num_opponents=3, params=params_loose)
        r_tight = adjust(pred, feat, num_opponents=3, params=params_tight)

        assert r_tight.was_adjusted
        assert r_tight.adjustment_reason == 'bluff_suppression'
        # Loose should NOT suppress bluffs at this equity
        assert not r_loose.was_adjusted or r_loose.adjustment_reason != 'bluff_suppression'
