"""Tests for sequence_reconstructor — Phase 1A.

Tests cover:
1. Basic reconstruction from feature counters
2. CERTAIN/AMBIGUOUS/CORRUPT classification
3. Hero prior_actions matching for AMBIGUOUS selection
4. Edge cases (hero first to act, facing bet, multi-villain)
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sequence_reconstructor import (
    reconstruct_sequence,
    ReconResult,
    _parse_prior_actions,
    _generate_candidates,
    _select_best,
    _sorted_positions,
)


def _make_sit(hero_pos, villain_positions, street, facing_bet,
              prior_actions=None, to_call=0, agg=0, cb=0, cc=0,
              ncb=0, fr=0, situation_id='test_001'):
    """Create a minimal situation dict for testing."""
    return {
        'situation_id': situation_id,
        'hero_position': hero_pos,
        'villain_positions': villain_positions,
        'street': street,
        'prior_actions': prior_actions or [],
        'feat_dict': {
            'facing_bet': facing_bet,
            'villain_aggression_count': agg,
            'villain_checked_back': cb,
            'villain_call_count': cc,
            'num_callers_to_bet': ncb,
            'facing_raise': fr,
            'to_call': to_call,
        },
    }


# ── _parse_prior_actions ────────────────────────────────────────────


class TestParsePriorActions:

    def test_extracts_current_street(self):
        pa = ['preflop: CO raise', 'flop: CO check', 'turn: CO bet']
        assert _parse_prior_actions(pa, 'flop') == ['check']

    def test_filters_other_streets(self):
        pa = ['preflop: CO raise', 'flop: CO check']
        assert _parse_prior_actions(pa, 'turn') == []

    def test_handles_short_street_codes(self):
        pa = ['preflop: CO raise', 'flop: CO check']
        # street='f' should map to 'flop'
        assert _parse_prior_actions(pa, 'f') == ['check']

    def test_empty_prior_actions(self):
        assert _parse_prior_actions([], 'flop') == []

    def test_multiple_actions_same_street(self):
        pa = ['flop: BB check', 'flop: BB call']
        assert _parse_prior_actions(pa, 'flop') == ['check', 'call']


# ── Not facing bet (facing_bet=0) ───────────────────────────────────


class TestNotFacingBet:

    def test_hero_first_to_act(self):
        """BB first to act, villains are CO and BTN."""
        sit = _make_sit('BB', ['CO', 'BTN'], 'flop', facing_bet=0)
        result = reconstruct_sequence(sit)
        assert result.classification == 'CERTAIN'
        assert result.action_string == 'BB ???'

    def test_hero_last_to_act_all_check(self):
        """BTN last, BB and CO checked."""
        sit = _make_sit('BTN', ['BB', 'CO'], 'flop', facing_bet=0)
        result = reconstruct_sequence(sit)
        assert result.classification == 'CERTAIN'
        assert result.action_string == 'BB check, CO check, BTN ???'

    def test_hero_middle_position(self):
        """CO in middle, BB checked, BTN after."""
        sit = _make_sit('CO', ['BB', 'BTN'], 'flop', facing_bet=0)
        result = reconstruct_sequence(sit)
        assert result.classification == 'CERTAIN'
        assert result.action_string == 'BB check, CO ???'

    def test_hero_checked_then_acts_again(self):
        """BB checked, all checked through, BB acts again (new action round).
        This happens when hero checked, villains checked behind, and
        it's a new betting round on the same street (rare in standard poker).

        Actually in standard poker, once all check the street ends.
        So if hero checked and facing_bet=0, hero is in the initiative
        round and hasn't reached ??? yet. The ??? IS the check decision.
        """
        sit = _make_sit('BB', ['CO', 'BTN'], 'flop', facing_bet=0,
                        prior_actions=['flop: BB check'])
        result = reconstruct_sequence(sit)
        # Hero checked on this street in prior_actions, but facing_bet=0
        # means this IS the decision point — the prior check was on a
        # previous orbit or the prior_actions are cross-street
        assert result.classification == 'CERTAIN'


# ── Facing bet (facing_bet=1) ───────────────────────────────────────


class TestFacingBet:

    def test_hero_faces_bet_simple(self):
        """BB faces CO's bet, BTN folded."""
        sit = _make_sit('BB', ['CO', 'BTN'], 'flop', facing_bet=1,
                        to_call=30, ncb=0)
        result = reconstruct_sequence(sit)
        assert result.classification in ('CERTAIN', 'AMBIGUOUS')
        assert '???' in result.action_string
        assert 'bet 30' in result.action_string

    def test_hero_faces_bet_with_caller(self):
        """BB faces bet with a caller. Either CO or BTN could have bet
        (the other called), so this is AMBIGUOUS. Both valid sequences
        should include a call and end with BB ???."""
        sit = _make_sit('BB', ['CO', 'BTN'], 'flop', facing_bet=1,
                        to_call=30, ncb=1)
        result = reconstruct_sequence(sit)
        assert result.classification == 'AMBIGUOUS'
        assert result.num_valid == 2
        assert 'call 30' in result.action_string
        assert result.action_string.endswith('BB ???')

    def test_facing_bet_bttn_hero(self):
        """BTN hero faces a bet. Could be BB or CO who bet."""
        sit = _make_sit('BTN', ['BB', 'CO'], 'flop', facing_bet=1,
                        to_call=45, ncb=0)
        result = reconstruct_sequence(sit)
        # Two villains could be the bettor → AMBIGUOUS
        assert result.classification == 'AMBIGUOUS'
        assert result.num_valid == 2
        # Both options should end with BTN ???
        for v in result.all_valid:
            assert v.endswith('BTN ???')

    def test_ambiguous_resolved_by_prior_actions(self):
        """BTN hero faces bet. prior_actions says hero checked on flop.
        This constrains: hero checked first (not possible if BTN),
        so the bettor must act before BTN in initiative order."""
        sit = _make_sit('BTN', ['BB', 'CO'], 'flop', facing_bet=1,
                        to_call=45, ncb=0,
                        prior_actions=['flop: BTN check'])
        result = reconstruct_sequence(sit)
        # BTN can't have checked in initiative (BTN is last)
        # But the selection rule picks the sequence matching hero actions
        assert result.action_string is not None


# ── CORRUPT cases ───────────────────────────────────────────────────


class TestCorrupt:

    def test_facing_raise_is_corrupt(self):
        """facing_raise=1 is not handled → CORRUPT."""
        sit = _make_sit('BB', ['CO', 'BTN'], 'flop', facing_bet=1,
                        to_call=60, fr=1)
        result = reconstruct_sequence(sit)
        assert result.classification == 'CORRUPT'


# ── Selection rule ──────────────────────────────────────────────────


class TestSelectBest:

    def test_prefers_hero_action_match(self):
        seqs = [
            'BB bet 45, CO fold, BTN ???',     # BB bets
            'BB check, CO bet 45, BTN ???',    # CO bets, hero didn't act yet
        ]
        # If hero (BTN) had "flop: BTN check" in prior_actions, neither matches
        # well, but the second one is simpler (hero hasn't acted)
        selected = _select_best(seqs, [], 'BTN')
        assert selected is not None

    def test_prefers_simplest_when_tied(self):
        seqs = [
            'BB check, CO bet 45, BTN fold, BB ???',  # 4 parts
            'BB check, CO bet 45, BB ???',             # 3 parts
        ]
        selected = _select_best(seqs, [], 'BB')
        assert selected == 'BB check, CO bet 45, BB ???'


# ── Integration with real data patterns ─────────────────────────────


class TestRealPatterns:
    """Test against the actual feature counter combinations found in the data."""

    def test_fb0_agg1_cb1_cc0(self):
        """Most common: facing_bet=0, agg=1, checked_back=1 (68 situations).
        Hero not facing bet on current street. Cross-street: villain
        was aggressive once and checked back once."""
        sit = _make_sit('BTN', ['BB', 'HJ'], 'turn', facing_bet=0,
                        agg=1, cb=1, cc=0)
        result = reconstruct_sequence(sit)
        assert result.classification == 'CERTAIN'
        assert result.action_string == 'BB check, HJ check, BTN ???'

    def test_fb0_agg1_cb0_cc0(self):
        """Second most common: 49 situations."""
        sit = _make_sit('BB', ['CO', 'BTN'], 'flop', facing_bet=0,
                        agg=1, cb=0, cc=0)
        result = reconstruct_sequence(sit)
        assert result.classification == 'CERTAIN'
        assert result.action_string == 'BB ???'

    def test_fb0_agg0_cb1_cc1(self):
        """Third most common: 42 situations."""
        sit = _make_sit('BTN', ['BB', 'CO'], 'river', facing_bet=0,
                        agg=0, cb=1, cc=1)
        result = reconstruct_sequence(sit)
        assert result.classification == 'CERTAIN'
        assert result.action_string == 'BB check, CO check, BTN ???'

    def test_fb1_agg0_cb1_cc1(self):
        """Facing bet, 12 situations. Hero faces bet on current street.
        Cross-street: villain checked back and called once."""
        sit = _make_sit('CO', ['BB', 'BTN'], 'river', facing_bet=1,
                        to_call=53, agg=0, cb=1, cc=1,
                        prior_actions=['preflop: CO raise', 'flop: CO check',
                                       'turn: CO check'])
        result = reconstruct_sequence(sit)
        assert result.classification in ('CERTAIN', 'AMBIGUOUS')
        assert 'bet 53' in result.action_string

    def test_fb1_agg1_cb1_cc0(self):
        """Facing bet, 11 situations."""
        sit = _make_sit('BTN', ['BB', 'HJ'], 'river', facing_bet=1,
                        to_call=53, agg=1, cb=1, cc=0,
                        prior_actions=['preflop: BTN call', 'flop: BTN check',
                                       'turn: BTN check'])
        result = reconstruct_sequence(sit)
        assert result.classification in ('CERTAIN', 'AMBIGUOUS')
        assert '???' in result.action_string
