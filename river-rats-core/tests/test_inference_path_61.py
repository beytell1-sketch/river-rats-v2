"""Tests for 61-feature production inference path (Phase 2-C cleanup).

Per dispatch PR #400 (owner-ratified Option B):
  (1) FEATURE_COLUMNS_61 has 61 entries; first 59 match canonical
      FEATURE_COLUMNS_59; last 2 are the pilot winners.
  (2) features_from_dict_61() returns a (61,) float32 numpy array in
      canonical order, deterministic, KeyError-on-missing.
  (3) features_from_dict_61(d)[:59] == features_from_dict_59(d) bit-for-bit
      (regression invariant: 59-trained production models continue to see
      the same input via either path).
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feature_extractor import FEATURE_COLUMNS as FE_COLS, extract_all_features
from feature_keys import F
from inference_path_59 import (
    FEATURE_COLUMNS_59,
    N_FEATURES_59,
    features_from_dict_59,
)
from inference_path_61 import (
    FEATURE_COLUMNS_61,
    N_FEATURES_61,
    features_from_dict_61,
)


def _build_sample_hand_dict():
    return {
        'h': 'AhKs', 'b': 'Ad8c3h', 'pos': 'BTN', 'vp': 'BB',
        'pot': 5.5, 'tc': 0, 'st': 'f', 'fb': 0, 'exp': 'C',
        F.META_NUM_OPPONENTS: 1, F.META_NUM_RAISES: 0,
        F.META_OPENER_POSITION: 'BTN', F.META_BETTOR_POSITION: None,
        '_villain_aggression_count': 0, '_villain_checked_back': 0,
        '_villain_call_count': 0, '_num_callers_to_bet': 0, '_facing_raise': 0,
        '_action_history': [],
    }


@pytest.fixture
def feat_dict():
    return extract_all_features(_build_sample_hand_dict())


class TestFeatureColumns61:
    def test_count_is_61(self):
        assert len(FEATURE_COLUMNS_61) == 61
        assert N_FEATURES_61 == 61

    def test_first_59_match_canonical_59(self):
        """The 61-feature surface's first 59 entries are the 59-canonical."""
        assert tuple(FEATURE_COLUMNS_61[:N_FEATURES_59]) == FEATURE_COLUMNS_59

    def test_last_2_are_pilot_winners(self):
        assert tuple(FEATURE_COLUMNS_61[-2:]) == (
            'players_to_act_after_hero',
            'tpmk_kicker_rank',
        )

    def test_matches_feature_extractor_first_61(self):
        """feature_extractor.FEATURE_COLUMNS first 61 entries == canonical 61."""
        assert tuple(FE_COLS[:N_FEATURES_61]) == FEATURE_COLUMNS_61


class TestFeaturesFromDict61:
    def test_returns_numpy_array_of_correct_shape(self, feat_dict):
        arr = features_from_dict_61(feat_dict)
        assert isinstance(arr, np.ndarray)
        assert arr.shape == (61,)
        assert arr.dtype == np.float32

    def test_deterministic(self, feat_dict):
        a1 = features_from_dict_61(feat_dict)
        a2 = features_from_dict_61(feat_dict)
        np.testing.assert_array_equal(a1, a2)

    def test_raises_keyerror_on_missing_keys(self):
        with pytest.raises(KeyError, match='missing'):
            features_from_dict_61({'street': 0})

    def test_ordered_consistent_with_FEATURE_COLUMNS_61(self, feat_dict):
        arr = features_from_dict_61(feat_dict)
        manual = np.array(
            [float(feat_dict[k]) for k in FEATURE_COLUMNS_61],
            dtype=np.float32,
        )
        np.testing.assert_array_equal(arr, manual)


class TestRegressionVs59Path:
    """61-path's first 59 elements must match 59-path bit-for-bit.

    Production 59-trained models (vNext-HU-59 + v9-3way-on-59) continue to
    consume input via the 59-path; they must see the same bits regardless
    of whether the caller builds via 59-path or slices the 61-path.
    """

    def test_first_59_elements_match_59_path(self, feat_dict):
        arr_61 = features_from_dict_61(feat_dict)
        arr_59 = features_from_dict_59(feat_dict)
        np.testing.assert_array_equal(arr_61[:59], arr_59)

    def test_last_2_elements_match_feat_dict(self, feat_dict):
        arr_61 = features_from_dict_61(feat_dict)
        assert arr_61[59] == float(feat_dict['players_to_act_after_hero'])
        assert arr_61[60] == float(feat_dict['tpmk_kicker_rank'])
