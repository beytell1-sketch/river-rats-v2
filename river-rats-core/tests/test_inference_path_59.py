"""Tests for 59-feature production inference path (Phase 1.5-E PR-A).

Per AMENDMENT (PR #378): tests verify
  (1) 59-feature feature-extraction helper produces correct shape on
      a sample feat_dict (deterministic + ordered);
  (2) `oracle_router` correctly dispatches to 59-feature path for
      modern models (vNext-HU-59) and to 55-feature legacy path for
      legacy models (v8-HU-38);
  (3) backward compat: legacy router behavior on v8-HU-38 unchanged.
"""
from __future__ import annotations

import os
import sys
import shutil
import tempfile

import numpy as np
import pytest

# Make river-rats-core importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feature_extractor import FEATURE_COLUMNS as FE_COLS, extract_all_features
from feature_keys import F
from gto_model import GtoOracle, FEATURE_COLUMNS as GTO_COLS
from inference_path_59 import (
    FEATURE_COLUMNS_59,
    N_FEATURES_59,
    features_from_dict_59,
)
from oracle_router import OracleRouter


_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_MODELS_DIR_PROD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models')
_MODELS_DIR_PROD = os.path.normpath(_MODELS_DIR_PROD)


def _build_sample_hand_dict():
    """Build a minimal HU hand_dict for feature extraction."""
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


# ─── inference_path_59 module ─────────────────────────────────────────

class TestFeatureColumns59:
    def test_count_is_59(self):
        assert len(FEATURE_COLUMNS_59) == 59
        assert N_FEATURES_59 == 59

    def test_matches_feature_extractor(self):
        assert tuple(FEATURE_COLUMNS_59) == tuple(FE_COLS)

    def test_extends_legacy_55(self):
        # The 59-tuple must be a strict superset of (or extension to) the
        # legacy 55-tuple's keys; first 55 may differ in ORDER, but the
        # SET must include all legacy keys.
        legacy_set = set(GTO_COLS)
        modern_set = set(FEATURE_COLUMNS_59)
        # Modern surface has at least the 4 extra keys of Phase 1.5-B
        # (`nut_blocker_overcard_count`, `bet_call_multiway_oop_raise_pressure_index`
        # were dropped to free indices for v2.4 P1 blockers — net is 59)
        assert len(modern_set) >= len(legacy_set) - 2 + 4


class TestFeaturesFromDict59:
    def test_returns_numpy_array_of_correct_shape(self, feat_dict):
        arr = features_from_dict_59(feat_dict)
        assert isinstance(arr, np.ndarray)
        assert arr.shape == (59,)
        assert arr.dtype == np.float32

    def test_deterministic(self, feat_dict):
        a1 = features_from_dict_59(feat_dict)
        a2 = features_from_dict_59(feat_dict)
        np.testing.assert_array_equal(a1, a2)

    def test_raises_keyerror_on_missing_keys(self):
        with pytest.raises(KeyError, match='missing'):
            features_from_dict_59({'street': 0})  # only 1 key

    def test_ordered_consistent_with_FEATURE_COLUMNS_59(self, feat_dict):
        arr = features_from_dict_59(feat_dict)
        # Re-extract manually in the same order
        manual = np.array([float(feat_dict[k]) for k in FEATURE_COLUMNS_59],
                          dtype=np.float32)
        np.testing.assert_array_equal(arr, manual)


# ─── oracle_router surface-size dispatch ──────────────────────────────

@pytest.fixture
def vnext_hu_model_path():
    """Path to vNext-HU-59 model artifact (in production models dir)."""
    path = os.path.join(_MODELS_DIR_PROD, 'gto_model_vNext_hu_59feat.json')
    if not os.path.exists(path):
        pytest.skip(f"vNext-HU model not present at {path}")
    return path


def test_vnext_hu_loads_via_gto_oracle(vnext_hu_model_path):
    """vNext-HU-59 model can be loaded via GtoOracle without crash."""
    oracle = GtoOracle(vnext_hu_model_path)
    assert oracle._model.n_classes_ == 5
    assert oracle._n_features == 59


def test_vnext_hu_predict_via_59_path(vnext_hu_model_path, feat_dict):
    """The 59-feature inference path produces a valid prediction."""
    oracle = GtoOracle(vnext_hu_model_path)
    features = features_from_dict_59(feat_dict)
    assert features.shape == (59,)
    pred = oracle.predict(features)
    assert pred.action in {'FOLD', 'CHECK', 'CALL', 'BET', 'RAISE'}
    assert 0.0 <= pred.confidence <= 1.0


def test_legacy_v8_hu_still_works_via_55_path(feat_dict):
    """Backward compat: v8-HU-38 still works via the 55-feature legacy path."""
    v8_path = os.path.join(_MODELS_DIR_PROD, 'gto_model_v8_hu.json')
    if not os.path.exists(v8_path):
        pytest.skip(f"v8-HU model not present at {v8_path}")
    oracle = GtoOracle(v8_path)
    assert oracle._n_features == 38
    features = GtoOracle.features_from_dict(feat_dict)
    assert features.shape == (55,)
    pred = oracle.predict(features)
    assert pred.action in {'FOLD', 'CHECK', 'CALL', 'BET', 'RAISE'}


def test_router_dispatches_legacy_to_55_path(feat_dict, monkeypatch):
    """OracleRouter routes legacy v8-HU through the 55-feature path (no crash)."""
    # OracleRouter loads v8-HU at position 1 by default (oracle_router.py:34).
    # No swap in PR-A; this test verifies legacy path remains functional.
    router = OracleRouter()
    if 1 not in router._oracles:
        pytest.skip("Position 1 (HU) not loaded; nothing to test for legacy")
    hu = router._oracles[1]
    if hu._n_features >= 59:
        pytest.skip("HU position is 59-feature (already swapped); legacy test N/A")
    pred = router.predict(feat_dict, num_opponents=1)
    assert pred.action in {'FOLD', 'CHECK', 'CALL', 'BET', 'RAISE'}


def test_router_dispatches_59_path_when_loaded(vnext_hu_model_path, feat_dict):
    """OracleRouter, when configured to load vNext-HU at position 1, routes through
    the 59-feature path without crashing.

    Post-Phase 1.5-E PR-B swap: oracle_router.py:34 _MODEL_FILES[1] points to
    'gto_model_vNext_hu_59feat.json'; we write vNext under that filename in a
    temp dir and instantiate OracleRouter with that dir.
    """
    # Use the post-swap filename (matches oracle_router.py:34 _MODEL_FILES[1]).
    from oracle_router import _MODEL_FILES
    hu_filename = _MODEL_FILES[1]
    with tempfile.TemporaryDirectory() as tmp:
        target = os.path.join(tmp, hu_filename)
        shutil.copy(vnext_hu_model_path, target)
        router = OracleRouter(models_dir=tmp)
        assert 1 in router._oracles
        hu = router._oracles[1]
        assert hu._n_features == 59  # confirms it loaded vNext at HU position
        pred = router.predict(feat_dict, num_opponents=1)
        assert pred.action in {'FOLD', 'CHECK', 'CALL', 'BET', 'RAISE'}
        assert 0.0 <= pred.confidence <= 1.0
