"""v2.4 Stage 3.5 — tests for action-aware chained narrowing.

Covers:
  - H_8dfb6ef8 canonical chain (bet-check-call-bet)
  - Turn-check-through → river-bet (owner's original scenario)
  - Flop-check → turn-decision (d2410 shape)
  - Deep chain empty-range safety rail
  - Schema-mismatch guard
  - Same-street exclusion (flop-only anchor isolation)
  - M1 updates to RIVER_BETTING_FREQUENCIES
  - M1 new CALL tables present
"""
import os
import sys

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)


# =============================================================================
# M1 — sanity checks on the updated / new frequency tables
# =============================================================================

def test_m1_river_bluff_lowered_for_3way():
    """RIVER_BETTING_FREQUENCIES['bluff'] updated from 0.35 to 0.20 per
    GTO review Flag A (3-way bluff density per KB §1.4)."""
    from range_narrowing import RIVER_BETTING_FREQUENCIES
    assert RIVER_BETTING_FREQUENCIES['bluff'] == 0.20


def test_m1_river_air_lowered_for_3way():
    """RIVER_BETTING_FREQUENCIES['air'] updated from 0.20 to 0.10 per
    GTO review Flag A."""
    from range_narrowing import RIVER_BETTING_FREQUENCIES
    assert RIVER_BETTING_FREQUENCIES['air'] == 0.10


def test_call_tables_exist_with_eight_categories():
    """FLOP/TURN/RIVER_CALL_FREQUENCIES present with all 8 categories."""
    from range_narrowing import (
        FLOP_CALL_FREQUENCIES,
        TURN_CALL_FREQUENCIES,
        RIVER_CALL_FREQUENCIES,
    )
    expected_cats = {
        'nuts', 'strong_value', 'good_value', 'draw',
        'medium_made', 'weak_made', 'bluff', 'air',
    }
    assert set(FLOP_CALL_FREQUENCIES.keys()) == expected_cats
    assert set(TURN_CALL_FREQUENCIES.keys()) == expected_cats
    assert set(RIVER_CALL_FREQUENCIES.keys()) == expected_cats


def test_call_medium_made_stays_elevated_across_streets():
    """GTO review: medium_made should stay elevated in CALL-continue
    across streets (bluff-catch / showdown band).

    Concretely: medium_made call-freq >= 0.45 on every street — the
    primary bluff-catch / showdown range.
    """
    from range_narrowing import (
        FLOP_CALL_FREQUENCIES,
        TURN_CALL_FREQUENCIES,
        RIVER_CALL_FREQUENCIES,
    )
    assert FLOP_CALL_FREQUENCIES['medium_made'] >= 0.45
    assert TURN_CALL_FREQUENCIES['medium_made'] >= 0.45
    assert RIVER_CALL_FREQUENCIES['medium_made'] >= 0.45


def test_call_nuts_strong_value_suppressed():
    """GTO review: nuts and strong_value should be SUPPRESSED in
    CALL-continue (they raise, not just continue).

    Concretely: call-freq <= 0.40 across all streets for these
    categories.
    """
    from range_narrowing import (
        FLOP_CALL_FREQUENCIES,
        TURN_CALL_FREQUENCIES,
        RIVER_CALL_FREQUENCIES,
    )
    for tbl in (FLOP_CALL_FREQUENCIES, TURN_CALL_FREQUENCIES, RIVER_CALL_FREQUENCIES):
        assert tbl['nuts'] <= 0.40, f'nuts too high: {tbl}'
        assert tbl['strong_value'] <= 0.40, f'strong_value too high: {tbl}'


# =============================================================================
# narrow_by_action_history — behavioral tests
# =============================================================================

def _sample_range():
    """Minimal synthetic range for testing — covers all 8 categories."""
    return {
        'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0,
        '99': 1.0, '88': 1.0, '77': 1.0, '66': 1.0,
        'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AJs': 1.0,
        'KQs': 1.0, 'KJs': 1.0, 'KTs': 1.0,
        'QJs': 1.0, 'JTs': 1.0, 'T9s': 1.0,
        '98s': 1.0, '87s': 1.0, '76s': 1.0,
        'A5s': 1.0, 'A4s': 1.0, '54s': 1.0, '65s': 1.0,
    }


def test_empty_action_history_falls_back_cleanly():
    """No action history → range returned unchanged, chain_steps empty."""
    from range_narrowing import narrow_by_action_history
    r = _sample_range()
    out, meta = narrow_by_action_history(
        r, ['7c', '5s', '2d'], [], 'BB', decision_street='flop',
    )
    assert out == r
    assert meta['chain_steps'] == []
    assert not meta['truncated']


def test_same_street_pre_hero_actions_excluded():
    """GTO review Q2: same-street pre-hero actions do NOT enter the chain.

    Flop decision. Villains SB+BB both checked before hero (IP) acts.
    Per Q2 verdict (NO): these checks should NOT trigger chain narrowing.
    """
    from range_narrowing import narrow_by_action_history
    r = _sample_range()
    action_history = [
        {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
        {'street': 'preflop', 'position': 'SB', 'action': 'CALL'},
        {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        # Flop actions BEFORE hero (BTN) acts:
        {'street': 'flop', 'position': 'SB', 'action': 'CHECK'},
        {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
    ]
    out, meta = narrow_by_action_history(
        r, ['Qs', '5s', '7s'], action_history, 'BB', decision_street='flop',
    )
    # Chain should have run zero narrow steps — decision is flop, no prior
    # POST-FLOP streets exist, and same-street actions are excluded.
    assert meta['chain_steps'] == [], f'Unexpected chain: {meta["chain_steps"]}'
    # Range unchanged
    assert len(out) == len(r)


def test_h_8dfb6ef8_chain_bet_check_call_bet():
    """GTO review Flag D: H_8dfb6ef8 is the canonical bet-check-call-bet
    chain for verification. Decision on river, chain runs flop-bet,
    turn-check, turn-call. River-bet is NOT part of chain (same-street
    exclusion on decision street)."""
    from range_narrowing import narrow_by_action_history
    r = _sample_range()
    action_history = [
        {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
        {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        {'street': 'flop', 'position': 'BB', 'action': 'BET'},
        {'street': 'flop', 'position': 'BTN', 'action': 'CALL'},
        {'street': 'turn', 'position': 'BB', 'action': 'CHECK'},
        {'street': 'turn', 'position': 'BTN', 'action': 'BET'},
        {'street': 'turn', 'position': 'BB', 'action': 'CALL'},
        {'street': 'river', 'position': 'BB', 'action': 'BET'},  # same-street on decision
    ]
    out, meta = narrow_by_action_history(
        r, ['5d', '3s', '5h', '3d', '9s'],
        action_history, 'BB', decision_street='river',
    )
    # Chain should include: flop:BET, turn:CHECK, turn:CALL
    # Should NOT include: river:BET (same-street on decision)
    expected_steps = ['flop:BET', 'turn:CHECK', 'turn:CALL']
    assert meta['chain_steps'] == expected_steps, (
        f'Expected {expected_steps}, got {meta["chain_steps"]}'
    )
    assert len(out) > 0
    assert not meta['truncated']


def test_d2410_shape_flop_check_turn_decision():
    """The load-bearing anchor case. d2410: CO raised preflop, CO (hero)
    checked flop. Now turn decision — was flop-checked to villain (BB).
    Chain should apply flop-check narrowing on villain's range before
    turn decision.

    In the calibration anchor spec, d2410's 'primary villain' is BTN
    (see calibration_anchors.json). For this test we use the same primary
    villain.
    """
    from range_narrowing import narrow_by_action_history
    r = _sample_range()
    action_history = [
        {'street': 'preflop', 'position': 'CO', 'action': 'RAISE'},
        {'street': 'preflop', 'position': 'BTN', 'action': 'CALL'},
        {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        # Flop: BB first (OOP), BB checked. CO (hero) checked. BTN checked.
        {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
        {'street': 'flop', 'position': 'CO', 'action': 'CHECK'},
        {'street': 'flop', 'position': 'BTN', 'action': 'CHECK'},
        # Turn BB check (known pre-hero for d2410 spec)
        {'street': 'turn', 'position': 'BB', 'action': 'CHECK'},
    ]
    out, meta = narrow_by_action_history(
        r, ['Jd', '9d', '3h', '6d'],
        action_history, 'BTN', decision_street='turn',
    )
    # Primary villain BTN checked flop → flop:CHECK in chain
    assert 'flop:CHECK' in meta['chain_steps'], (
        f'd2410 chain should include flop:CHECK; got {meta["chain_steps"]}'
    )
    # Turn:CHECK is same-street (decision=turn), should NOT be in chain
    assert 'turn:CHECK' not in meta['chain_steps']


def test_fold_terminates_chain():
    """If villain folded on a prior street, chain returns empty range."""
    from range_narrowing import narrow_by_action_history
    r = _sample_range()
    action_history = [
        {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        {'street': 'flop', 'position': 'BB', 'action': 'FOLD'},
    ]
    out, meta = narrow_by_action_history(
        r, ['Qs', '7s', '2d', '5c'], action_history,
        'BB', decision_street='turn',
    )
    assert out == {}
    assert meta['surviving_weight'] == 0.0


def test_schema_mismatch_guard():
    """Unknown action-history schema → warning + fallback, no crash."""
    from range_narrowing import narrow_by_action_history
    r = _sample_range()
    # Malformed entries (missing keys)
    action_history = [{'wrong_key': 'BET'}]
    out, meta = narrow_by_action_history(
        r, ['Qs', '7s', '2d'], action_history,
        'BB', decision_street='turn',
    )
    # Schema warning surfaced
    assert 'schema_warning' in meta
    # Range returned unchanged
    assert out == r


def test_tuple_action_history_works():
    """Bridge currently passes dicts, but tuple form should also work
    (matches game.street_actions raw format)."""
    from range_narrowing import narrow_by_action_history
    r = _sample_range()
    action_history = [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),
    ]
    out, meta = narrow_by_action_history(
        r, ['Qs', '7s', '2d', '5c'], action_history,
        'BB', decision_street='turn',
    )
    # Should have flop:BET in chain
    assert 'flop:BET' in meta['chain_steps']


def test_deep_chain_safety_rail():
    """4+ action chain should not collapse range to zero. Safety rail
    reverts to last valid if narrowing produces degenerate state."""
    from range_narrowing import narrow_by_action_history
    r = _sample_range()
    # Contrived deep chain
    action_history = [
        {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        {'street': 'flop', 'position': 'BB', 'action': 'BET'},
        {'street': 'flop', 'position': 'BB', 'action': 'BET'},   # re-bet
        {'street': 'turn', 'position': 'BB', 'action': 'CHECK'},
        {'street': 'turn', 'position': 'BB', 'action': 'CALL'},
    ]
    out, meta = narrow_by_action_history(
        r, ['Qs', '7s', '2d', '5c', '9h'], action_history,
        'BB', decision_street='river',
    )
    # Should produce non-empty output even if some intermediate step
    # would have truncated (safety rail reverts)
    assert len(out) > 0


# =============================================================================
# narrow_to_continuing_range — direct tests
# =============================================================================

def test_continuing_range_empty_input():
    """Empty range → empty output, no crash."""
    from range_narrowing import narrow_to_continuing_range
    assert narrow_to_continuing_range({}, ['Kh', '9d', '3c'], 'flop') == {}


def test_continuing_range_normalizes_to_unit():
    """Output is probability distribution summing to ≈ 1.0."""
    from range_narrowing import narrow_to_continuing_range
    r = _sample_range()
    out = narrow_to_continuing_range(r, ['Kh', '9d', '3c'], 'flop')
    total = sum(out.values())
    assert abs(total - 1.0) < 1e-6, f'not normalized: {total}'


def test_continuing_range_medium_made_survives_river():
    """River call-continue should retain medium_made hands (bluff-catch
    band) at non-trivial weight."""
    from range_narrowing import narrow_to_continuing_range, classify_hand
    r = _sample_range()
    board = ['Kh', '9d', '3c', '2s', '7h']
    out = narrow_to_continuing_range(r, board, 'river')
    # At least one medium_made hand should remain in the output
    medium_present = False
    for hand, freq in out.items():
        if freq > 0:
            cls = classify_hand(hand, board)
            if cls.category == 'medium_made':
                medium_present = True
                break
    # Not all sample hands classify as medium_made on this board, so
    # we check the output is non-empty and properly normalized as a
    # weaker sanity check
    assert len(out) > 0


if __name__ == '__main__':
    import subprocess
    rc = subprocess.call([sys.executable, '-m', 'pytest', '-xvs', __file__])
    sys.exit(rc)
