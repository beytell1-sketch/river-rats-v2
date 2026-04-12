"""Tests for hand_sequence_validator.py

Coverage:
  Original 7 self-tests (converted from __main__ block)
  Facing-bet audit error patterns (4 regression tests)
  Valid sequences that must pass (3 additional)
  validate_all() batch function
  load_from_jsonl() with valid and feature-vector records
"""

import json
import os
import sys
import tempfile

import pytest

# Ensure river-rats-core is on sys.path regardless of cwd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hand_sequence_validator import (
    Action,
    HandSpec,
    StreetSpec,
    load_from_jsonl,
    validate_action_string,
    validate_all,
    validate_hand,
)


# =============================================================================
# Helpers
# =============================================================================

def _valid(positions, street, action_string, hero):
    """Assert that action_string produces no errors."""
    errors = validate_action_string(positions, street, action_string, hero)
    assert errors == [], f"Expected VALID but got errors: {errors}"


def _invalid(positions, street, action_string, hero, *, contains=None):
    """Assert that action_string produces at least one error.

    If *contains* is given, at least one error message must contain that
    substring (case-insensitive).
    """
    errors = validate_action_string(positions, street, action_string, hero)
    assert errors, (
        f"Expected INVALID but got VALID for: {action_string!r}"
    )
    if contains is not None:
        lower_contains = contains.lower()
        assert any(lower_contains in e.lower() for e in errors), (
            f"Expected an error containing {contains!r}, got: {errors}"
        )


# =============================================================================
# Original 7 self-tests
# =============================================================================

class TestOriginalSelfTests:
    """Direct ports of the 7 cases in the __main__ block."""

    def test_1_valid_bb_check_co_bet_btn_call_bb_fold(self):
        """Test 1: BB checks, CO bets 45, BTN calls, BB folds — valid."""
        _valid(
            ['BB', 'CO', 'BTN'], 'flop',
            'BB check, CO bet 45, BTN call 45, BB fold',
            'BB',
        )

    def test_2_invalid_bb_folds_without_bet(self):
        """Test 2: BB folds before any bet on turn — invalid."""
        _invalid(
            ['BB', 'CO', 'BTN'], 'turn',
            'BB fold, CO bet 60',
            'BTN',
            contains='no bet',
        )

    def test_3_invalid_btn_responds_before_co_after_bb_bets(self):
        """Test 3: BB bets, BTN calls before CO responds — wrong response order."""
        _invalid(
            ['BB', 'CO', 'BTN'], 'flop',
            'BB bet 30, BTN call 30, CO fold',
            'CO',
            contains='CO',
        )

    def test_4_invalid_co_skipped_in_initiative_round(self):
        """Test 4: BB checks, BTN bets — CO was skipped in initiative round."""
        _invalid(
            ['BB', 'CO', 'BTN'], 'turn',
            'BB check, BTN bet 60',
            'BB',
            contains='CO',
        )

    def test_5_valid_bet_and_call_co_bets_btn_calls_bb_last(self):
        """Test 5: CO bets, BTN calls, BB is last to act (correct sandwich)."""
        _valid(
            ['BB', 'CO', 'BTN'], 'flop',
            'BB check, CO bet 30, BTN call 30, BB ???',
            'BB',
        )

    def test_6_invalid_bet_and_call_co_responds_before_bb(self):
        """Test 6: BTN bets, CO calls before BB acts — BB should go first
        (BB is clockwise-next from BTN)."""
        _invalid(
            ['BB', 'CO', 'BTN'], 'flop',
            'BB check, CO check, BTN bet 30, CO call 30, BB ???',
            'BB',
            contains='BB',
        )

    def test_7_valid_btn_bets_bb_responds_co_last(self):
        """Test 7: BTN bets, BB responds first (sandwich position), CO last."""
        _valid(
            ['BB', 'CO', 'BTN'], 'flop',
            'BB check, CO check, BTN bet 30, BB call 30, CO ???',
            'CO',
        )


# =============================================================================
# Facing-bet audit regression tests
# =============================================================================

class TestFacingBetAuditPatterns:
    """Error patterns found in the 12/40 failing facing-bet test set situations.

    Each test encodes a structural mistake that the validator must catch.
    """

    def test_audit_1_bb_labeled_closing_when_co_bets_not_sandwich(self):
        """BB should be closing (last to respond) when CO bets from the middle.

        Pattern: CO bets, BTN calls, BB ???
        BB is NOT in a sandwich — BB is closing the action.  This is a valid
        sequence; the validator must NOT flag it as an error.

        The audit found situations mislabeled as 'sandwich' when BB was
        actually last to act (closing position) after CO bet + BTN call.
        """
        _valid(
            ['BB', 'CO', 'BTN'], 'flop',
            'BB check, CO bet 45, BTN call 45, BB ???',
            'BB',
        )

    def test_audit_2_impossible_bet_and_call_hero_acts_before_caller(self):
        """Hero cannot be facing a 'bet-and-call' if the caller acts AFTER hero.

        Pattern: BB check, CO check, BTN bet 30, BB ???, CO call 30
        BB acts before CO calls — hero has not yet seen the call.
        This sequence should produce an error because CO has not yet acted
        when it is BB's turn to respond.

        We validate that the response order check fires: CO should not
        appear AFTER the hero-decision marker in the response sequence
        when the response ordering places CO before hero.
        """
        # In this scenario BTN bets.  Clockwise from BTN: BB responds first,
        # then CO.  So BB acting before CO is CORRECT — CO acts after BB.
        # This is actually a VALID sequence (the audit mistake was the
        # inverse: assuming CO already called before BB acts).
        # The test verifies the correct mechanic: BB goes before CO.
        _valid(
            ['BB', 'CO', 'BTN'], 'flop',
            'BB check, CO check, BTN bet 30, BB ???',
            'BB',
        )
        # And the inverse (CO responds before BB) is invalid:
        _invalid(
            ['BB', 'CO', 'BTN'], 'flop',
            'BB check, CO check, BTN bet 30, CO call 30, BB ???',
            'BB',
            contains='BB',
        )

    def test_audit_3_fold_without_facing_bet(self):
        """A player cannot fold when no bet is live.

        Pattern: BB folds at the start of flop before any bet — illegal.
        """
        _invalid(
            ['BB', 'CO', 'BTN'], 'flop',
            'BB fold, CO bet 40, BTN call 40',
            'CO',
            contains='no bet',
        )

    def test_audit_4_missing_check_in_initiative_round(self):
        """Every active player must act in the initiative round before a bet.

        Pattern: BB checks, BTN bets — CO was skipped.
        This is the same as Test 4 but with 4 players to test the skip
        detection for the middle seat.
        """
        _invalid(
            ['SB', 'BB', 'CO', 'BTN'], 'flop',
            'SB check, BB check, BTN bet 50',
            'SB',
            contains='CO',
        )


# =============================================================================
# Additional valid sequences
# =============================================================================

class TestValidSequences:
    """Sequences that must pass without errors."""

    def test_valid_heads_up_sb_checks_bb_bets(self):
        """Heads-up: SB checks, BB bets (both players act in initiative order)."""
        _valid(
            ['SB', 'BB'], 'flop',
            'SB check, BB bet 30, SB ???',
            'SB',
        )

    def test_valid_4way_check_through(self):
        """4-way pot, all players check — SB→BB→CO→BTN."""
        _valid(
            ['SB', 'BB', 'CO', 'BTN'], 'flop',
            'SB check, BB check, CO check, BTN check',
            'BTN',
        )

    def test_valid_raise_resets_response_order(self):
        """BB bets, CO raises — everyone must respond to the raise.

        BTN calls the raise, then BB must close the action.
        """
        _valid(
            ['BB', 'CO', 'BTN'], 'turn',
            'BB bet 40, CO raise 120, BTN call 120, BB ???',
            'BB',
        )


# =============================================================================
# validate_all() tests
# =============================================================================

class TestValidateAll:

    def _make_spec(self, action_string, positions, street, hero, opener='CO'):
        """Build a HandSpec from an action_string for batch testing."""
        actions = []
        hero_idx = None
        for i, part in enumerate(p.strip() for p in action_string.split(',')):
            tokens = part.split()
            if '???' in part or 'HERO' in part.upper():
                hero_idx = i
                continue
            if len(tokens) >= 2:
                pos = tokens[0].upper()
                act = tokens[1].lower()
                amt = float(tokens[2]) if len(tokens) > 2 else 0.0
                actions.append(Action(pos, act, amt))
        if hero_idx is None:
            hero_idx = len(actions)
        return HandSpec(
            positions=positions,
            opener=opener,
            streets=[StreetSpec(
                name=street, cards=[],
                actions=actions,
                hero_pos=hero,
                hero_action_index=hero_idx,
            )],
        )

    def test_all_pass(self):
        spec1 = self._make_spec(
            'BB check, CO bet 45, BTN call 45, BB fold',
            ['BB', 'CO', 'BTN'], 'flop', 'BB',
        )
        spec2 = self._make_spec(
            'SB check, BB check, CO check, BTN check',
            ['SB', 'BB', 'CO', 'BTN'], 'flop', 'BTN',
        )
        result = validate_all([spec1, spec2])
        assert len(result['pass']) == 2
        assert len(result['fail']) == 0

    def test_some_fail(self):
        good = self._make_spec(
            'BB check, CO bet 45, BTN call 45, BB fold',
            ['BB', 'CO', 'BTN'], 'flop', 'BB',
        )
        bad = self._make_spec(
            'BB fold, CO bet 60',          # fold without a bet live
            ['BB', 'CO', 'BTN'], 'turn', 'CO',
        )
        result = validate_all([good, bad])
        assert len(result['pass']) == 1
        assert len(result['fail']) == 1
        assert result['fail'][0]['spec'] is bad
        assert result['fail'][0]['errors']

    def test_empty_list(self):
        result = validate_all([])
        assert result == {'pass': [], 'fail': []}


# =============================================================================
# load_from_jsonl() tests
# =============================================================================

class TestLoadFromJsonl:

    def _write_jsonl(self, records):
        """Write list of dicts to a temp JSONL file, return path."""
        tf = tempfile.NamedTemporaryFile(
            mode='w', suffix='.jsonl', delete=False
        )
        for rec in records:
            tf.write(json.dumps(rec) + '\n')
        tf.close()
        return tf.name

    def test_loads_valid_records(self):
        records = [
            {
                'positions': ['BB', 'CO', 'BTN'],
                'opener': 'CO',
                'street': 'flop',
                'hero_pos': 'BB',
                'action_string': 'BB check, CO bet 45, BTN call 45, BB ???',
            },
            {
                'positions': ['SB', 'BB', 'BTN'],
                'opener': 'BTN',
                'street': 'turn',
                'hero_pos': 'SB',
                'action_string': 'SB check, BB check, BTN bet 60, SB ???',
                'hero_cards': ['Ah', 'Kd'],
                'board_cards': ['Jh', '8c', '2s', '4d'],
            },
        ]
        path = self._write_jsonl(records)
        try:
            specs = load_from_jsonl(path)
            assert len(specs) == 2
            assert specs[0].positions == ['BB', 'CO', 'BTN']
            assert specs[0].opener == 'CO'
            assert specs[1].hero_cards == ['Ah', 'Kd']
        finally:
            os.unlink(path)

    def test_skips_feature_vector_records(self):
        """Feature-vector records (no action_string) are silently skipped."""
        feature_record = {
            'street': 0,
            'facing_bet': 1,
            'pot_size': 90.0,
            'to_call': 30.0,
            '_hero_pos_raw': 'BTN',
            '_villain_pos_raw': 'CO',
            'action': 'CALL',
        }
        hand_spec_record = {
            'positions': ['BB', 'CO', 'BTN'],
            'opener': 'CO',
            'street': 'flop',
            'hero_pos': 'BB',
            'action_string': 'BB check, CO bet 45, BTN call 45, BB ???',
        }
        path = self._write_jsonl([feature_record, hand_spec_record])
        try:
            specs = load_from_jsonl(path)
            # Only the hand-spec record is loaded
            assert len(specs) == 1
            assert specs[0].opener == 'CO'
        finally:
            os.unlink(path)

    def test_skips_records_missing_required_fields(self):
        """Records with action_string but missing positions/opener etc. are skipped."""
        incomplete = {
            'action_string': 'BB check, CO bet 45',
            # missing: positions, opener, street, hero_pos
        }
        path = self._write_jsonl([incomplete])
        try:
            specs = load_from_jsonl(path)
            assert specs == []
        finally:
            os.unlink(path)

    def test_empty_file(self):
        path = self._write_jsonl([])
        try:
            specs = load_from_jsonl(path)
            assert specs == []
        finally:
            os.unlink(path)

    def test_mixed_valid_and_invalid_lines(self):
        """Malformed JSON on one line does not abort the whole load."""
        tf = tempfile.NamedTemporaryFile(
            mode='w', suffix='.jsonl', delete=False
        )
        tf.write('{"positions": ["BB","CO"], "opener": "CO", "street": "flop", '
                 '"hero_pos": "BB", "action_string": "BB check, CO bet 30, BB ???"}\n')
        tf.write('this is not valid json\n')
        tf.write('{"positions": ["BB","BTN"], "opener": "BTN", "street": "turn", '
                 '"hero_pos": "BB", "action_string": "BB check, BTN bet 40, BB ???"}\n')
        tf.close()
        try:
            specs = load_from_jsonl(tf.name)
            assert len(specs) == 2
        finally:
            os.unlink(tf.name)
