"""
Tests for board_adjusted_hrp derived feature.

board_adjusted_hrp = hero_range_percentile * equity_vs_range

Collapses HRP when the board doesn't connect with hero's hand.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def _make_hand(hero_cards='AhKd', board='Qs7h2c', pos='BTN', vp='BB'):
    """Minimal hand dict for a flop situation."""
    return {
        'id': 'test_bahrp',
        'pos': pos,
        'vp': vp,
        'fb': 0,
        'pot': 10.0,
        'tc': 0.0,
        'st': 'f',
        'h': hero_cards,
        'b': board,
        'exp': 'B',
        '_is_3bet_pot': 0,
        '_villain_aggression_count': 0,
        '_villain_checked_back': 0,
        '_villain_call_count': 0,
    }


class TestBoardAdjustedHrpExists:
    """board_adjusted_hrp must appear in extract_all_features output."""

    def test_board_adjusted_hrp_exists_in_features(self):
        from feature_extractor import extract_all_features
        hand = _make_hand()
        features = extract_all_features(hand)
        assert 'board_adjusted_hrp' in features, (
            "board_adjusted_hrp missing from extract_all_features output"
        )


class TestBoardAdjustedHrpValue:
    """board_adjusted_hrp must equal hero_range_percentile * equity_vs_range."""

    def test_board_adjusted_hrp_equals_hrp_times_equity(self):
        from feature_extractor import extract_all_features
        hand = _make_hand()
        features = extract_all_features(hand)
        expected = features['hero_range_percentile'] * features['equity_vs_range']
        assert abs(features['board_adjusted_hrp'] - expected) < 1e-6, (
            f"board_adjusted_hrp={features['board_adjusted_hrp']} != "
            f"hrp({features['hero_range_percentile']}) * "
            f"equity({features['equity_vs_range']}) = {expected}"
        )


class TestBoardAdjustedHrpAirOnMonotone:
    """A4d on Qs5s7s (no spade, no connection) should be < 0.35."""

    def test_board_adjusted_hrp_air_on_monotone(self):
        from feature_extractor import extract_all_features
        # A4d: no spade, no connection to Qs5s7s
        hand = _make_hand(hero_cards='Ad4d', board='Qs5s7s', pos='BTN')
        features = extract_all_features(hand)
        assert features['board_adjusted_hrp'] < 0.35, (
            f"A4d on Qs5s7s should have board_adjusted_hrp < 0.35, "
            f"got {features['board_adjusted_hrp']:.4f} "
            f"(hrp={features['hero_range_percentile']:.4f}, "
            f"equity={features['equity_vs_range']:.4f})"
        )


class TestFeatureSurface:
    """Feature-surface invariants for production paths.

    Original 55-pin (v2.3.1) was superseded by Phase 1.5-B 61→59 J-B drop;
    canonical production HU + 3-way surface is 59 (frozen in
    inference_path_59._CANONICAL_FEATURE_COLUMNS_59). feature_extractor.
    FEATURE_COLUMNS may extend beyond 59 (Phase 2-B PILOT appends to 65)
    but the FIRST 59 entries must match canonical.
    """

    def test_production_surface_at_least_59(self):
        from feature_extractor import FEATURE_COLUMNS
        from inference_path_59 import N_FEATURES_59
        assert len(FEATURE_COLUMNS) >= N_FEATURES_59, (
            f"feature_extractor.FEATURE_COLUMNS has {len(FEATURE_COLUMNS)} "
            f"entries; need ≥{N_FEATURES_59} for production 59-feature path."
        )

    def test_first_59_match_canonical(self):
        from feature_extractor import FEATURE_COLUMNS
        from inference_path_59 import (
            FEATURE_COLUMNS_59 as CANONICAL_59,
            N_FEATURES_59,
        )
        assert tuple(FEATURE_COLUMNS[:N_FEATURES_59]) == CANONICAL_59, (
            "feature_extractor.FEATURE_COLUMNS first 59 entries diverged "
            "from canonical production surface; production 59-trained "
            "models will silently produce wrong predictions."
        )

    def test_gto_model_feature_count_is_55(self):
        from gto_model import FEATURE_COLUMNS as GTO_COLS
        assert len(GTO_COLS) == 55, (
            f"Expected 55 in gto_model.FEATURE_COLUMNS, got {len(GTO_COLS)}"
        )
