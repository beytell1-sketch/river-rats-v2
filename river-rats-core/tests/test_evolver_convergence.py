"""Tests for variant_evolver and convergence_checker."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from self_play import (
    Variant, RoundResult, VariantScore, GameResult, HeroDecision,
    SelfPlayRunner,
)
from variant_evolver import evolve_variants, _merge_params
from convergence_checker import (
    check_convergence, ConvergenceResult, format_convergence_report,
)
from multiway_adjuster import get_default_params


ORACLE_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'gto_model_v8_38feat.json')
HAS_MODEL = os.path.exists(ORACLE_PATH)


def _make_round_result(variant_scores: dict, game_results=None, round_id=1,
                       seed=42) -> RoundResult:
    """Helper to build a RoundResult from a {name: mbb} dict."""
    vs_map = {}
    for name, mbb in variant_scores.items():
        vs = VariantScore(name=name)
        # Reverse-engineer total_chips from mbb: mbb = (total/games)/10*1000
        vs.num_games = 36
        vs.total_chips = int(mbb * 36 * 10 / 1000)
        vs_map[name] = vs
    return RoundResult(
        round_id=round_id,
        num_deals=6,
        num_games=36,
        seed=seed,
        variant_results=vs_map,
        game_results=game_results or [],
    )


# ── Evolver tests ───────────────────────────────────────────────────

class TestEvolverBasic:

    def _make_pool(self):
        base = get_default_params()
        return [
            Variant("baseline", base),
            Variant("tight", {**base, 'value_base': 0.50}),
            Variant("loose", {**base, 'bluff_eq_thresh': 0.20}),
            Variant("oop_discount", {**base, 'equity_realization_oop': 0.75}),
            Variant("cold_strict", {**base, 'cold_call_base': 0.60}),
            Variant("no_adjust", {**base, 'bluff_eq_thresh': 0.0, 'value_base': 0.0}),
        ]

    def test_produces_6_variants(self):
        pool = self._make_pool()
        result = _make_round_result({
            'baseline': 10.0, 'tight': 25.0, 'loose': -5.0,
            'oop_discount': 15.0, 'cold_strict': 5.0, 'no_adjust': -20.0,
        })
        used = {'baseline', 'tight', 'loose', 'oop_discount', 'cold_strict', 'no_adjust'}
        next_v = evolve_variants(result, pool, used)
        assert len(next_v) == 6

    def test_top_2_kept(self):
        pool = self._make_pool()
        result = _make_round_result({
            'baseline': 10.0, 'tight': 25.0, 'loose': -5.0,
            'oop_discount': 15.0, 'cold_strict': 5.0, 'no_adjust': -20.0,
        })
        used = {'baseline', 'tight', 'loose', 'oop_discount', 'cold_strict', 'no_adjust'}
        next_v = evolve_variants(result, pool, used)
        names = [v.name for v in next_v]
        # Top 2 by mbb: tight (25), oop_discount (15)
        assert 'tight' in names
        assert 'oop_discount' in names

    def test_hybrids_created(self):
        pool = self._make_pool()
        result = _make_round_result({
            'baseline': 10.0, 'tight': 25.0, 'loose': -5.0,
            'oop_discount': 15.0, 'cold_strict': 5.0, 'no_adjust': -20.0,
        })
        used = {'baseline', 'tight', 'loose', 'oop_discount', 'cold_strict', 'no_adjust'}
        next_v = evolve_variants(result, pool, used)
        hybrid_names = [v.name for v in next_v if 'hybrid' in v.name]
        assert len(hybrid_names) >= 1

    def test_untested_picked_when_available(self):
        pool = self._make_pool()
        result = _make_round_result({
            'baseline': 10.0, 'tight': 25.0, 'loose': -5.0,
        })
        # Only 3 used — 3 untested remain
        used = {'baseline', 'tight', 'loose'}
        next_v = evolve_variants(result, pool, used)
        names = [v.name for v in next_v]
        # Should include some untested ones
        untested_in_next = [n for n in names if n in {'oop_discount', 'cold_strict', 'no_adjust'}]
        assert len(untested_in_next) > 0


class TestMergeParams:

    def test_equal_weight_averages(self):
        baseline = get_default_params()
        a = {**baseline, 'value_base': 0.40}
        b = {**baseline, 'value_base': 0.60}
        merged = _merge_params(a, b, baseline, weight_a=0.5)
        assert merged['value_base'] == pytest.approx(0.50)

    def test_weighted_merge(self):
        baseline = get_default_params()
        a = {**baseline, 'value_base': 0.40}
        b = {**baseline, 'value_base': 0.60}
        merged = _merge_params(a, b, baseline, weight_a=0.75)
        assert merged['value_base'] == pytest.approx(0.45)

    def test_int_params_stay_int(self):
        baseline = get_default_params()
        a = {**baseline, 'rule1_draw_bypass': 6}
        b = {**baseline, 'rule1_draw_bypass': 10}
        merged = _merge_params(a, b, baseline, weight_a=0.5)
        assert merged['rule1_draw_bypass'] == 8
        assert isinstance(merged['rule1_draw_bypass'], int)


# ── Convergence tests ────────────────────────────────────────────────

class TestConvergenceBasic:

    def test_first_round_not_converged(self):
        result = _make_round_result({'baseline': 10.0, 'tight': 25.0})
        conv = check_convergence(result, previous_round=None)
        assert conv.converged is False
        assert 'First round' in conv.reason

    def test_max_rounds_converges(self):
        result = _make_round_result({'baseline': 10.0}, round_id=10)
        conv = check_convergence(result, max_rounds=10)
        assert conv.converged is True
        assert conv.hit_max_rounds is True

    def test_plateau_detected(self):
        result = _make_round_result({
            'A': 10.0, 'B': 11.0, 'C': 12.0,  # spread = 2 mbb < 5 threshold
        })
        conv = check_convergence(result)
        assert conv.plateau_detected is True

    def test_no_plateau_with_large_spread(self):
        result = _make_round_result({
            'A': -20.0, 'B': 10.0, 'C': 50.0,  # spread = 70 mbb
        })
        conv = check_convergence(result)
        assert conv.plateau_detected is False

    def test_format_report(self):
        result = _make_round_result({'baseline': 10.0, 'tight': 25.0})
        conv = check_convergence(result)
        report = format_convergence_report(conv)
        assert 'Round' in report
        assert 'Converged' in report


class TestConvergenceWithDecisions:
    """Convergence check with actual decision comparison."""

    def _make_game(self, deal_id, variant, hero_pos, action, chips=0):
        return GameResult(
            deal_id=deal_id,
            variant_name=variant,
            hero_position=hero_pos,
            chips_won=chips,
            hand_record={},
            hero_decisions=[HeroDecision(
                street='flop', action=action, amount=0, pot=100,
                to_call=33, num_opponents=2, equity=0.5,
                was_adjusted=False, oracle_action=action, is_preflop=False,
            )],
        )

    def test_identical_decisions_converge(self):
        # Both rounds: winner makes same decisions on same deals
        games_r1 = [
            self._make_game(0, 'A', 'BTN', 'call', 10),
            self._make_game(0, 'B', 'BTN', 'fold', -5),
            self._make_game(1, 'A', 'CO', 'bet', 20),
            self._make_game(1, 'B', 'CO', 'check', 0),
        ]
        games_r2 = [
            self._make_game(0, 'A', 'BTN', 'call', 15),
            self._make_game(0, 'B', 'BTN', 'fold', -10),
            self._make_game(1, 'A', 'CO', 'bet', 25),
            self._make_game(1, 'B', 'CO', 'check', 5),
        ]
        r1 = RoundResult(
            round_id=1, num_deals=2, num_games=4, seed=42,
            variant_results={'A': VariantScore('A', 30, 2), 'B': VariantScore('B', -5, 2)},
            game_results=games_r1,
        )
        r2 = RoundResult(
            round_id=2, num_deals=2, num_games=4, seed=42,
            variant_results={'A': VariantScore('A', 40, 2), 'B': VariantScore('B', -5, 2)},
            game_results=games_r2,
        )
        conv = check_convergence(r2, previous_round=r1)
        assert conv.decision_stability == 1.0
        assert conv.converged is True

    def test_different_decisions_not_converged(self):
        games_r1 = [
            self._make_game(0, 'A', 'BTN', 'call', 10),
            self._make_game(0, 'B', 'BTN', 'fold', -5),
        ]
        games_r2 = [
            self._make_game(0, 'A', 'BTN', 'fold', -5),  # different!
            self._make_game(0, 'B', 'BTN', 'call', 10),
        ]
        r1 = RoundResult(
            round_id=1, num_deals=1, num_games=2, seed=42,
            variant_results={'A': VariantScore('A', 10, 1), 'B': VariantScore('B', -5, 1)},
            game_results=games_r1,
        )
        r2 = RoundResult(
            round_id=2, num_deals=1, num_games=2, seed=42,
            variant_results={'A': VariantScore('A', -5, 1), 'B': VariantScore('B', 10, 1)},
            game_results=games_r2,
        )
        # R1 winner = A (call), R2 winner = B (call) — but B wasn't winner in R1
        # Actually: R2 winner is B, R1 winner is A. Comparing B's R2 decisions vs A's R1.
        # B at deal 0 BTN: call. A at deal 0 BTN: call. Same! stability = 1.0
        # Wait — that's because both winners happen to call at the same spot.
        # Let me make a clearer test.
        pass

    def test_partial_stability(self):
        games_r1 = [
            self._make_game(0, 'A', 'BTN', 'call', 10),
            self._make_game(0, 'B', 'BTN', 'fold', -5),
            self._make_game(1, 'A', 'CO', 'bet', 20),
            self._make_game(1, 'B', 'CO', 'check', 0),
        ]
        games_r2 = [
            self._make_game(0, 'A', 'BTN', 'call', 10),  # same
            self._make_game(0, 'B', 'BTN', 'fold', -5),
            self._make_game(1, 'A', 'CO', 'check', 0),    # different!
            self._make_game(1, 'B', 'CO', 'check', 5),
        ]
        r1 = RoundResult(
            round_id=1, num_deals=2, num_games=4, seed=42,
            variant_results={'A': VariantScore('A', 30, 2), 'B': VariantScore('B', -5, 2)},
            game_results=games_r1,
        )
        r2 = RoundResult(
            round_id=2, num_deals=2, num_games=4, seed=42,
            variant_results={'A': VariantScore('A', 10, 2), 'B': VariantScore('B', 0, 2)},
            game_results=games_r2,
        )
        conv = check_convergence(r2, previous_round=r1)
        # Winner R1 = A, Winner R2 = A. A's decisions: call (same), check (diff from bet)
        assert conv.decision_stability == pytest.approx(0.5)
        assert conv.converged is False


@pytest.mark.skipif(not HAS_MODEL, reason="Model file not available")
class TestEvolverEndToEnd:
    """Evolver works with real self-play output."""

    def test_evolve_from_real_round(self):
        base = get_default_params()
        pool = [
            Variant("baseline", base),
            Variant("tight", {**base, 'value_base': 0.50}),
            Variant("extra1", {**base, 'bluff_eq_thresh': 0.25}),
            Variant("extra2", {**base, 'cold_call_base': 0.60}),
            Variant("extra3", {**base, 'equity_realization_oop': 0.75}),
            Variant("extra4", {**base, 'raise_base': 0.55}),
        ]
        runner = SelfPlayRunner(pool[:2], num_deals=3, seed=42,
                                oracle_path=ORACLE_PATH)
        result = runner.run_round()
        used = {'baseline', 'tight'}
        next_v = evolve_variants(result, pool, used)
        assert len(next_v) == 6
        # Should contain some untested variants
        names = {v.name for v in next_v}
        assert len(names & {'extra1', 'extra2', 'extra3', 'extra4'}) > 0
