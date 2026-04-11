"""Tests for decision_comparator and observer flag tagger."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from self_play import (
    SelfPlayRunner, Variant, GameResult, HeroDecision, RoundResult,
)
from decision_comparator import (
    compare_decisions, Divergence, ComparisonSummary, format_divergence_report,
)
from observer import (
    ObserverFlags, tag_situation, tag_decision, tag_outcome, tag_game,
)
from multiway_adjuster import get_default_params


ORACLE_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'gto_model_v8_38feat.json')
HAS_MODEL = os.path.exists(ORACLE_PATH)


# ── Comparator tests ────────────────────────────────────────────────

class TestComparatorWithSyntheticData:
    """Comparator works on hand-built GameResult objects."""

    def _make_game(self, deal_id, variant, hero_pos, chips_won, decisions):
        return GameResult(
            deal_id=deal_id,
            variant_name=variant,
            hero_position=hero_pos,
            chips_won=chips_won,
            hand_record={},
            hero_decisions=decisions,
        )

    def _make_decision(self, street='flop', action='call', oracle_action='call',
                       equity=0.5, was_adjusted=False):
        return HeroDecision(
            street=street, action=action, amount=0, pot=100, to_call=33,
            num_opponents=2, equity=equity, was_adjusted=was_adjusted,
            oracle_action=oracle_action, is_preflop=False,
        )

    def test_no_divergence_when_same_actions(self):
        games = [
            self._make_game(0, 'A', 'BTN', 10, [self._make_decision(action='call')]),
            self._make_game(0, 'B', 'BTN', -10, [self._make_decision(action='call')]),
        ]
        summary = compare_decisions(games)
        assert summary.divergent_points == 0

    def test_finds_divergence(self):
        games = [
            self._make_game(0, 'A', 'BTN', 10, [self._make_decision(action='call')]),
            self._make_game(0, 'B', 'BTN', -33, [self._make_decision(action='fold')]),
        ]
        summary = compare_decisions(games)
        assert summary.divergent_points == 1
        assert len(summary.divergences) == 1
        d = summary.divergences[0]
        assert d.deal_id == 0
        assert d.hero_position == 'BTN'
        assert d.unique_actions == {'call', 'fold'}

    def test_best_worst_variant(self):
        games = [
            self._make_game(0, 'winner', 'BTN', 50, [self._make_decision(action='raise')]),
            self._make_game(0, 'loser', 'BTN', -50, [self._make_decision(action='fold')]),
        ]
        summary = compare_decisions(games)
        d = summary.divergences[0]
        assert d.best_variant == 'winner'
        assert d.worst_variant == 'loser'
        assert d.chip_spread == 100

    def test_multiple_deals(self):
        games = [
            self._make_game(0, 'A', 'BTN', 10, [self._make_decision(action='call')]),
            self._make_game(0, 'B', 'BTN', 10, [self._make_decision(action='fold')]),
            self._make_game(1, 'A', 'CO', 20, [self._make_decision(action='bet')]),
            self._make_game(1, 'B', 'CO', 20, [self._make_decision(action='bet')]),
        ]
        summary = compare_decisions(games)
        assert summary.divergent_points == 1  # only deal 0 diverges
        assert summary.total_decision_points == 2

    def test_variant_win_rate(self):
        games = [
            self._make_game(0, 'A', 'BTN', 50, [self._make_decision(action='call')]),
            self._make_game(0, 'B', 'BTN', -50, [self._make_decision(action='fold')]),
            self._make_game(1, 'A', 'CO', -30, [self._make_decision(action='fold')]),
            self._make_game(1, 'B', 'CO', 30, [self._make_decision(action='call')]),
        ]
        summary = compare_decisions(games)
        assert summary.divergent_points == 2
        assert summary.variant_win_rate['A'] == 0.5
        assert summary.variant_win_rate['B'] == 0.5

    def test_format_report(self):
        games = [
            self._make_game(0, 'baseline', 'BTN', 10, [self._make_decision(action='call')]),
            self._make_game(0, 'tight', 'BTN', -33, [self._make_decision(action='fold')]),
        ]
        summary = compare_decisions(games)
        report = format_divergence_report(summary)
        assert 'Divergence rate' in report
        assert 'baseline' in report
        assert 'tight' in report

    def test_empty_input(self):
        summary = compare_decisions([])
        assert summary.total_decision_points == 0
        assert summary.divergent_points == 0


@pytest.mark.skipif(not HAS_MODEL, reason="Model file not available")
class TestComparatorEndToEnd:
    """Comparator works with real self-play output."""

    def test_compare_real_round(self):
        baseline = get_default_params()
        tight = {**baseline, 'value_base': 0.50, 'raise_base': 0.55}
        variants = [
            Variant("baseline", baseline),
            Variant("tight", tight),
        ]
        runner = SelfPlayRunner(variants, num_deals=5, seed=42,
                                oracle_path=ORACLE_PATH)
        result = runner.run_round()
        summary = compare_decisions(result.game_results)

        assert summary.total_decision_points >= 0
        assert isinstance(summary.divergence_rate, float)
        # With different params, we expect SOME divergences over 5 deals
        # (though not guaranteed on any specific seed)


# ── Observer tests ──────────────────────────────────────────────────

class TestObserverFlags:
    """Observer flag tagger computes correct flags."""

    def _make_decision(self, **kwargs):
        defaults = dict(
            street='flop', action='call', amount=0, pot=100, to_call=33,
            num_opponents=2, equity=0.5, was_adjusted=False,
            oracle_action='call', is_preflop=False,
        )
        defaults.update(kwargs)
        return HeroDecision(**defaults)

    def test_situation_hero_has_draw(self):
        flags = ObserverFlags()
        dec = self._make_decision()
        feat = {'draw_outs': 9, 'is_made_hand': 0, 'danger_score': 0.2,
                'villain_checked_back': 0, 'is_ip': 1, 'spr': 5.0}
        tag_situation(flags, dec, feat)
        assert flags.hero_has_draw is True

    def test_situation_no_draw(self):
        flags = ObserverFlags()
        dec = self._make_decision()
        feat = {'draw_outs': 0, 'is_made_hand': 1, 'danger_score': 0.2,
                'villain_checked_back': 0, 'is_ip': 1, 'spr': 5.0}
        tag_situation(flags, dec, feat)
        assert flags.hero_has_draw is False

    def test_situation_vulnerable(self):
        flags = ObserverFlags()
        dec = self._make_decision()
        feat = {'draw_outs': 0, 'is_made_hand': 1, 'danger_score': 0.8,
                'villain_checked_back': 0, 'is_ip': 0, 'spr': 5.0}
        tag_situation(flags, dec, feat)
        assert flags.hero_vulnerable is True

    def test_situation_dominating(self):
        flags = ObserverFlags()
        dec = self._make_decision(equity=0.85)
        tag_situation(flags, dec)
        assert flags.hero_dominating is True

    def test_situation_multiway_pressure(self):
        flags = ObserverFlags()
        dec = self._make_decision(num_opponents=3)
        tag_situation(flags, dec)
        assert flags.multiway_pressure is True

    def test_situation_facing_aggression(self):
        flags = ObserverFlags()
        dec = self._make_decision(to_call=33)
        tag_situation(flags, dec)
        assert flags.facing_aggression is True

    def test_situation_pot_committed(self):
        flags = ObserverFlags()
        dec = self._make_decision()
        feat = {'draw_outs': 0, 'is_made_hand': 0, 'danger_score': 0,
                'villain_checked_back': 0, 'is_ip': 0, 'spr': 1.5}
        tag_situation(flags, dec, feat)
        assert flags.pot_committed is True

    def test_decision_tightened(self):
        flags = ObserverFlags()
        dec = self._make_decision(action='check', oracle_action='bet')
        tag_decision(flags, dec)
        assert flags.deviated_from_hu is True
        assert flags.tightened is True
        assert flags.loosened is False

    def test_decision_loosened(self):
        flags = ObserverFlags()
        dec = self._make_decision(action='bet', oracle_action='check')
        tag_decision(flags, dec)
        assert flags.deviated_from_hu is True
        assert flags.loosened is True
        assert flags.tightened is False

    def test_decision_no_deviation(self):
        flags = ObserverFlags()
        dec = self._make_decision(action='call', oracle_action='call')
        tag_decision(flags, dec)
        assert flags.deviated_from_hu is False
        assert flags.tightened is False
        assert flags.loosened is False

    def test_outcome_profitable(self):
        flags = ObserverFlags()
        tag_outcome(flags, chips_won=50, went_to_showdown=True,
                    hero_folded=False)
        assert flags.decision_profitable is True
        assert flags.showdown_winner is True

    def test_outcome_fold_equity(self):
        flags = ObserverFlags()
        tag_outcome(flags, chips_won=30, went_to_showdown=False,
                    hero_folded=False, opponents_folded=True)
        assert flags.fold_equity_captured is True

    def test_outcome_lost(self):
        flags = ObserverFlags()
        tag_outcome(flags, chips_won=-50, went_to_showdown=True,
                    hero_folded=False)
        assert flags.decision_profitable is False
        assert flags.showdown_winner is False

    def test_to_dict(self):
        flags = ObserverFlags()
        flags.hero_has_draw = True
        flags.decision_profitable = True
        d = flags.to_dict()
        assert d['hero_has_draw'] is True
        assert d['decision_profitable'] is True
        assert isinstance(d, dict)

    def test_flag_categories(self):
        flags = ObserverFlags()
        assert 'hero_has_draw' in flags.situation_flags
        assert 'deviated_from_hu' in flags.decision_flags
        assert 'decision_profitable' in flags.outcome_flags


@pytest.mark.skipif(not HAS_MODEL, reason="Model file not available")
class TestObserverEndToEnd:
    """Observer tags real self-play game results."""

    def test_tag_game_results(self):
        baseline = get_default_params()
        variants = [Variant("baseline", baseline)]
        runner = SelfPlayRunner(variants, num_deals=3, seed=42,
                                oracle_path=ORACLE_PATH)
        result = runner.run_round()

        tagged_count = 0
        for gr in result.game_results:
            if gr.hero_decisions:
                flags_list = tag_game(gr)
                assert len(flags_list) == len(gr.hero_decisions)
                for f in flags_list:
                    assert isinstance(f, ObserverFlags)
                tagged_count += 1

        assert tagged_count > 0
