"""Tests for oracle_router.py — specialist model selection by opponent count."""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from oracle_router import OracleRouter, _MODEL_FILES, _LEGACY_HU
from gto_model import GtoOracle


MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')


class TestRouterInit:
    """Router loads available models and reports them."""

    def test_loads_with_legacy_model(self):
        """Router loads when only the legacy v8 model exists."""
        router = OracleRouter(MODELS_DIR)
        assert 1 in router._oracles

    def test_available_models_reports_loaded(self):
        router = OracleRouter(MODELS_DIR)
        available = router.available_models
        assert len(available) >= 1
        assert 1 in available

    def test_raises_if_no_models(self, tmp_path):
        """Router raises FileNotFoundError if models dir is empty."""
        with pytest.raises(FileNotFoundError):
            OracleRouter(str(tmp_path))


class TestRouterDispatch:
    """Router selects the correct model for each opponent count."""

    def test_hu_gets_v8(self):
        router = OracleRouter(MODELS_DIR)
        oracle = router._get_oracle(1)
        assert oracle is not None
        # v8 expects 38 features
        assert oracle._n_features == 38

    def test_3way_falls_back_to_hu(self):
        """Before v9-3way exists, 3-way falls back to v8."""
        router = OracleRouter(MODELS_DIR)
        if not router.has_specialist(2):
            oracle = router._get_oracle(2)
            # Should get v8 as fallback
            assert oracle._n_features == 38

    def test_5way_falls_back(self):
        """5+ opponents falls back to highest available."""
        router = OracleRouter(MODELS_DIR)
        oracle = router._get_oracle(5)
        assert oracle is not None

    def test_6way_same_as_5way(self):
        """6-way and 5-way get the same model (clamped to 4)."""
        router = OracleRouter(MODELS_DIR)
        o5 = router._get_oracle(5)
        o6 = router._get_oracle(6)
        assert o5 is o6


class TestRouterPredict:
    """Router.predict() produces valid OraclePredictions."""

    def _make_feat_dict(self):
        """Minimal feature dict with all 45 keys."""
        from feature_extractor import extract_all_features
        hand = {
            'h': 'AhKd', 'b': 'Ks7h2d', 'pos': 'BTN', 'vp': 'BB',
            'pot': 10.0, 'tc': 5.0, 'st': 'f', 'fb': 1, 'exp': 'C',
        }
        return extract_all_features(hand)

    def test_predict_returns_oracle_prediction(self):
        router = OracleRouter(MODELS_DIR)
        feat_dict = self._make_feat_dict()
        pred = router.predict(feat_dict, num_opponents=1)
        assert pred.action in ('FOLD', 'CHECK', 'CALL', 'BET', 'RAISE')
        assert 0.0 <= pred.confidence <= 1.0

    def test_predict_works_for_all_opponent_counts(self):
        router = OracleRouter(MODELS_DIR)
        feat_dict = self._make_feat_dict()
        for n in [1, 2, 3, 4, 5]:
            pred = router.predict(feat_dict, num_opponents=n)
            assert pred.action in ('FOLD', 'CHECK', 'CALL', 'BET', 'RAISE')


class TestRouterWithSelfPlay:
    """Router integrates correctly with self-play runner."""

    def test_self_play_accepts_router(self):
        from self_play import SelfPlayRunner, Variant
        from multiway_adjuster import get_default_params

        router = OracleRouter(MODELS_DIR)
        variants = [Variant("test", get_default_params())]
        runner = SelfPlayRunner(variants, num_deals=1, seed=42, oracle=router)
        # Should not crash
        assert runner.oracle is router

    def test_self_play_runs_with_router(self):
        from self_play import SelfPlayRunner, Variant
        from multiway_adjuster import get_default_params

        router = OracleRouter(MODELS_DIR)
        variants = [Variant("test", get_default_params())]
        runner = SelfPlayRunner(variants, num_deals=1, seed=42, oracle=router)
        result = runner.run_round(round_id=1)
        assert result.num_deals == 1
        assert "test" in result.variant_results
