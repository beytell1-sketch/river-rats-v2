"""Smoke tests for the self-play loop runner."""
import sys, os, tempfile, json
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from self_play import SelfPlayRunner, Variant, RoundResult
from multiway_adjuster import get_default_params


ORACLE_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'gto_model_v8_38feat.json')
HAS_MODEL = os.path.exists(ORACLE_PATH)


@pytest.mark.skipif(not HAS_MODEL, reason="Model file not available")
class TestSelfPlaySmoke:
    """End-to-end smoke test with real oracle."""

    def _make_variants(self):
        baseline = get_default_params()
        tight = {**baseline, 'value_base': 0.50, 'raise_base': 0.55}
        return [
            Variant("baseline", baseline),
            Variant("tight", tight, rationale="Tighter value and raise thresholds"),
        ]

    def test_run_one_deal(self):
        variants = self._make_variants()
        runner = SelfPlayRunner(variants, num_deals=1, seed=42,
                                oracle_path=ORACLE_PATH)
        result = runner.run_round()
        assert isinstance(result, RoundResult)
        # 1 deal × 6 positions × 2 variants = 12 games
        assert result.num_games == 12
        assert len(result.game_results) == 12

    def test_variant_scores_populated(self):
        variants = self._make_variants()
        runner = SelfPlayRunner(variants, num_deals=2, seed=42,
                                oracle_path=ORACLE_PATH)
        result = runner.run_round()
        for name in ['baseline', 'tight']:
            vs = result.variant_results[name]
            assert vs.num_games == 12  # 2 deals × 6 positions
            assert len(vs.games_by_position) > 0

    def test_reproducible(self):
        variants = self._make_variants()
        r1 = SelfPlayRunner(variants, num_deals=3, seed=99,
                            oracle_path=ORACLE_PATH).run_round()
        r2 = SelfPlayRunner(variants, num_deals=3, seed=99,
                            oracle_path=ORACLE_PATH).run_round()
        for g1, g2 in zip(r1.game_results, r2.game_results):
            assert g1.deal_id == g2.deal_id
            assert g1.variant_name == g2.variant_name
            assert g1.hero_position == g2.hero_position
            assert g1.chips_won == g2.chips_won

    def test_different_seeds_different_results(self):
        variants = self._make_variants()
        r1 = SelfPlayRunner(variants, num_deals=5, seed=1,
                            oracle_path=ORACLE_PATH).run_round()
        r2 = SelfPlayRunner(variants, num_deals=5, seed=2,
                            oracle_path=ORACLE_PATH).run_round()
        # Not all chip results should match (extremely unlikely)
        chips1 = [g.chips_won for g in r1.game_results]
        chips2 = [g.chips_won for g in r2.game_results]
        assert chips1 != chips2

    def test_save_results(self):
        variants = self._make_variants()
        runner = SelfPlayRunner(variants, num_deals=2, seed=42,
                                oracle_path=ORACLE_PATH)
        result = runner.run_round()

        with tempfile.TemporaryDirectory() as tmpdir:
            runner.save_results(result, tmpdir)
            path = os.path.join(tmpdir, 'round_1.json')
            assert os.path.exists(path)
            with open(path) as f:
                data = json.load(f)
            assert 'variants' in data
            assert 'baseline' in data['variants']
            assert 'mbb_per_hand' in data['variants']['baseline']

    def test_mbb_per_hand_is_number(self):
        variants = self._make_variants()
        runner = SelfPlayRunner(variants, num_deals=3, seed=42,
                                oracle_path=ORACLE_PATH)
        result = runner.run_round()
        for vs in result.variant_results.values():
            mbb = vs.mbb_per_hand
            assert isinstance(mbb, float)


@pytest.mark.skipif(not HAS_MODEL, reason="Model file not available")
class TestVariantFromHypothesis:
    """Variant.from_hypothesis() creates from master plan format."""

    def test_from_hypothesis(self):
        hyp = {
            "name": "cold_call_strict",
            "rationale": "Tighter cold-call thresholds",
            "overrides": {
                "cold_call_base": 0.60,
                "cold_call_per_raise": 0.25,
            }
        }
        v = Variant.from_hypothesis(hyp)
        assert v.name == "cold_call_strict"
        assert v.params['cold_call_base'] == 0.60
        assert v.params['cold_call_per_raise'] == 0.25
        # Non-overridden params should be at defaults
        assert v.params['bluff_eq_thresh'] == get_default_params()['bluff_eq_thresh']
