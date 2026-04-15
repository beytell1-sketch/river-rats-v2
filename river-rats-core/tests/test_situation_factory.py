"""Regression tests for situation_factory.py.

v2.3 backlog item 5: validate villain_positions length against num_opponents
at generation time so incomplete villain info is caught early.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from situation_factory import SituationSpec, build_situation


# ---------------------------------------------------------------------------
# Fix 1 regression: villain count mismatch must raise ValueError
# ---------------------------------------------------------------------------

def test_build_situation_raises_when_villain_count_mismatch():
    """Blueprint section 5: num_opponents=2 with only 1 seat in villain_positions
    must raise ValueError at build_situation() time."""
    spec = SituationSpec(
        hero_cards=['As', '9s'],
        board_cards=['Ts', '6s', '3d'],
        hero_pos='BTN',
        villain_positions=['BB'],  # Only 1 seat declared
        num_opponents=2,           # But spec says 2 opponents
        pot=90.0,
        to_call=30.0,
        street='flop',
        action_history=[
            ('preflop', 'BTN', 'raise'),
            ('preflop', 'BB', 'call'),
            ('flop', 'SB', 'check'),
            ('flop', 'BB', 'bet'),
        ],
        opener_position='BTN',
    )
    with pytest.raises(ValueError, match="villain_positions has 1 seats but num_opponents=2"):
        build_situation(spec)


def test_build_situation_passes_when_villain_count_matches():
    """Both villain seats present — build_situation must succeed and
    feat_dict['num_opponents'] must equal 2."""
    spec_correct = SituationSpec(
        hero_cards=['As', '9s'],
        board_cards=['Ts', '6s', '3d'],
        hero_pos='BTN',
        villain_positions=['SB', 'BB'],  # Both seats present
        num_opponents=2,
        pot=90.0,
        to_call=30.0,
        street='flop',
        action_history=[
            ('preflop', 'BTN', 'raise'),
            ('preflop', 'BB', 'call'),
            ('flop', 'SB', 'check'),
            ('flop', 'BB', 'bet'),
        ],
        opener_position='BTN',
    )
    feat_dict = build_situation(spec_correct)
    assert feat_dict['num_opponents'] == 2


def test_build_situation_num_opponents_none_infers_from_list():
    """When num_opponents is None (default), validator uses len(villain_positions)
    and must not raise."""
    spec = SituationSpec(
        hero_cards=['As', '9s'],
        board_cards=['Ts', '6s', '3d'],
        hero_pos='BTN',
        villain_positions=['BB'],
        # num_opponents not set — defaults to None, inferred from list
        pot=90.0,
        to_call=30.0,
        street='flop',
        action_history=[
            ('preflop', 'BTN', 'raise'),
            ('preflop', 'BB', 'call'),
            ('flop', 'BB', 'bet'),
        ],
        opener_position='BTN',
    )
    # Should not raise
    feat_dict = build_situation(spec)
    assert feat_dict is not None


# =============================================================================
# ANOMALY-A regression: normalise_situation() at serialisation boundary
# =============================================================================

def test_normalise_situation_converts_street_strings():
    """String street values become canonical ints (flop=0, turn=1, river=2)."""
    from situation_factory import normalise_situation
    assert normalise_situation({'street': 'flop'})['street'] == 0
    assert normalise_situation({'street': 'turn'})['street'] == 1
    assert normalise_situation({'street': 'river'})['street'] == 2


def test_normalise_situation_converts_hero_position_strings():
    """String hero_position values map via POSITION_ORDINAL."""
    from situation_factory import normalise_situation
    expected = {'UTG': 0, 'HJ': 1, 'CO': 2, 'BTN': 3, 'SB': 4, 'BB': 5}
    for pos, code in expected.items():
        out = normalise_situation({'hero_position': pos})
        assert out['hero_position'] == code, f'{pos} -> {out["hero_position"]} (expected {code})'


def test_normalise_situation_single_call_fixes_both_fields():
    """A single normalise_situation() call converts both street and hero_pos."""
    from situation_factory import normalise_situation
    raw = {'street': 'turn', 'hero_position': 'BTN', 'villain_position': 2}
    out = normalise_situation(raw)
    assert out['street'] == 1
    assert out['hero_position'] == 3
    assert out['villain_position'] == 2
    out2 = normalise_situation(out)
    assert out2 == out


def test_normalise_situation_also_handles_hero_pos_legacy_key():
    from situation_factory import normalise_situation
    out = normalise_situation({'hero_pos': 'SB', 'street': 'flop'})
    assert out['hero_pos'] == 4
    assert out['street'] == 0


def test_normalise_situation_raises_on_unknown_values():
    from situation_factory import normalise_situation
    import pytest
    with pytest.raises(KeyError):
        normalise_situation({'street': 'preflop'})
    with pytest.raises(KeyError):
        normalise_situation({'hero_position': 'XX'})


def test_normalise_situation_passes_numeric_unchanged():
    from situation_factory import normalise_situation
    out = normalise_situation({'street': 2, 'hero_position': 3.0})
    assert out['street'] == 2
    assert out['hero_position'] == 3.0
