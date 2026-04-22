"""v2.4 Stage 3.5 commit 3 — same-street sequence collapse pre-filter tests.

Covers:
  - MUST #3: check-raise collapse (check-bet same street → bet only)
  - MUST #11: check-call collapse (check-call same street → call only)
  - MUST #12: generic triple / deeper sequences; FOLD terminal
  - Pure check-through preserved (last CHECK is the decision)
  - Empty / single-action passthrough
"""
import os
import sys

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)


# =============================================================================
# Direct helper tests — _collapse_same_street_sequence
# =============================================================================

def _mk(street, pos, action):
    return {'street': street, 'position': pos, 'action': action}


def test_collapse_empty():
    """Empty list → empty list."""
    from range_narrowing import _collapse_same_street_sequence
    assert _collapse_same_street_sequence([]) == []


def test_collapse_single_action_passthrough():
    """Single action → passthrough (no collapse logic applies)."""
    from range_narrowing import _collapse_same_street_sequence
    acts = [_mk('flop', 'BB', 'BET')]
    assert _collapse_same_street_sequence(acts) == acts


def test_collapse_check_bet_same_street():
    """MUST #3 — check-raise collapse. (CHECK, BET) → (BET,).

    The CHECK is a sandbag; the BET is the decisive action. Chaining
    both narrowings would produce inverted composition (mediums up,
    nuts down) instead of check-raise's 60-80% nuts.
    """
    from range_narrowing import _collapse_same_street_sequence
    acts = [
        _mk('flop', 'BB', 'CHECK'),
        _mk('flop', 'BB', 'BET'),
    ]
    out = _collapse_same_street_sequence(acts)
    assert len(out) == 1
    assert out[0]['action'] == 'BET'


def test_collapse_check_raise_same_street():
    """MUST #3 — (CHECK, RAISE) → (RAISE,). RAISE is decisive."""
    from range_narrowing import _collapse_same_street_sequence
    acts = [
        _mk('flop', 'BB', 'CHECK'),
        _mk('flop', 'BB', 'RAISE'),
    ]
    out = _collapse_same_street_sequence(acts)
    assert len(out) == 1
    assert out[0]['action'] == 'RAISE'


def test_collapse_check_call_same_street():
    """MUST #11 — check-call collapse. (CHECK, CALL) → (CALL,).

    Check-call is one continuing action; chaining CHECK + CALL double-
    weights mediums. GTO + practical + research converge: the CALL is
    the decision-bearing move.
    """
    from range_narrowing import _collapse_same_street_sequence
    acts = [
        _mk('flop', 'BB', 'CHECK'),
        _mk('flop', 'BB', 'CALL'),
    ]
    out = _collapse_same_street_sequence(acts)
    assert len(out) == 1
    assert out[0]['action'] == 'CALL'


def test_collapse_triple_check_check_bet():
    """MUST #12 — triple sequence generic collapse.
    (CHECK, CHECK, BET) → (BET,). All prior CHECKs are sandbagged.
    """
    from range_narrowing import _collapse_same_street_sequence
    acts = [
        _mk('flop', 'BB', 'CHECK'),
        _mk('flop', 'BB', 'CHECK'),
        _mk('flop', 'BB', 'BET'),
    ]
    out = _collapse_same_street_sequence(acts)
    assert len(out) == 1
    assert out[0]['action'] == 'BET'


def test_collapse_check_bet_raise_triple():
    """MUST #12 — (CHECK, BET, RAISE). Both BET and RAISE are decisive.
    Keep LAST decision-bearing action (RAISE) + anything after.
    """
    from range_narrowing import _collapse_same_street_sequence
    acts = [
        _mk('flop', 'BB', 'CHECK'),
        _mk('flop', 'BB', 'BET'),
        _mk('flop', 'BB', 'RAISE'),
    ]
    out = _collapse_same_street_sequence(acts)
    # Last decisive = RAISE (index 2); keep index 2+
    assert len(out) == 1
    assert out[0]['action'] == 'RAISE'


def test_collapse_pure_check_through():
    """Edge case — no decision-bearing actions; all CHECKs.
    Keep last CHECK (that IS the decision on this street).
    """
    from range_narrowing import _collapse_same_street_sequence
    acts = [
        _mk('flop', 'BB', 'CHECK'),
        _mk('flop', 'BB', 'CHECK'),
    ]
    out = _collapse_same_street_sequence(acts)
    assert len(out) == 1
    assert out[0]['action'] == 'CHECK'


def test_collapse_fold_is_terminal():
    """MUST #12 — FOLD is decision-bearing + terminal. CHECK before
    FOLD dropped; FOLD kept.
    """
    from range_narrowing import _collapse_same_street_sequence
    acts = [
        _mk('flop', 'BB', 'CHECK'),
        _mk('flop', 'BB', 'FOLD'),
    ]
    out = _collapse_same_street_sequence(acts)
    assert len(out) == 1
    assert out[0]['action'] == 'FOLD'


def test_collapse_preserves_non_check_prefix():
    """BET followed by RAISE → keep RAISE (last decisive) alone.
    Prior BET is not a sandbag but chain-wise only the final stance
    matters for the collapsed narrowing.
    """
    from range_narrowing import _collapse_same_street_sequence
    acts = [
        _mk('flop', 'BB', 'BET'),
        _mk('flop', 'BB', 'RAISE'),
    ]
    out = _collapse_same_street_sequence(acts)
    assert len(out) == 1
    assert out[0]['action'] == 'RAISE'


# =============================================================================
# Integration tests — narrow_by_action_history with same-street sequences
# =============================================================================

def _sample_range():
    """Minimal synthetic range — covers all 8 categories."""
    return {
        'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0,
        '99': 1.0, '88': 1.0, '77': 1.0, '66': 1.0,
        'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AJs': 1.0,
        'KQs': 1.0, 'KJs': 1.0, 'KTs': 1.0,
        'QJs': 1.0, 'JTs': 1.0, 'T9s': 1.0,
        '98s': 1.0, '87s': 1.0, '76s': 1.0,
        'A5s': 1.0, 'A4s': 1.0, '54s': 1.0, '65s': 1.0,
    }


def test_chain_steps_collapse_check_raise_to_bet_only():
    """Integration: chain applied to check-raise should show single BET
    step (not CHECK then BET) in chain_steps metadata."""
    from range_narrowing import narrow_by_action_history
    r = _sample_range()
    action_history = [
        {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
        {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        # Flop check-raise: BB checks, hero bets, BB raises
        {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
        {'street': 'flop', 'position': 'BTN', 'action': 'BET'},
        {'street': 'flop', 'position': 'BB', 'action': 'RAISE'},
    ]
    _, meta = narrow_by_action_history(
        r, ['Qh', '5d', '2c', '9s'], action_history,
        'BB', decision_street='turn',
    )
    # BB's flop sequence: [CHECK, RAISE]. Collapsed to [RAISE] → chain
    # shows 'flop:BET' (BET narrowing class). No separate flop:CHECK.
    assert 'flop:CHECK' not in meta['chain_steps'], (
        f'Pre-filter failed to collapse check-raise: {meta["chain_steps"]}'
    )
    assert 'flop:BET' in meta['chain_steps'], (
        f'Expected flop:BET from collapsed check-raise: {meta["chain_steps"]}'
    )


def test_chain_steps_collapse_check_call_to_call_only():
    """Integration: check-call → single CALL step."""
    from range_narrowing import narrow_by_action_history
    r = _sample_range()
    action_history = [
        {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
        {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        # Flop check-call: BB checks, BTN bets, BB calls
        {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
        {'street': 'flop', 'position': 'BTN', 'action': 'BET'},
        {'street': 'flop', 'position': 'BB', 'action': 'CALL'},
    ]
    _, meta = narrow_by_action_history(
        r, ['Qh', '5d', '2c', '9s'], action_history,
        'BB', decision_street='turn',
    )
    assert 'flop:CHECK' not in meta['chain_steps'], (
        f'Pre-filter failed to collapse check-call: {meta["chain_steps"]}'
    )
    assert 'flop:CALL' in meta['chain_steps'], (
        f'Expected flop:CALL from collapsed check-call: {meta["chain_steps"]}'
    )


def test_chain_pure_check_through_preserved():
    """Integration: pure check-through (no aggression) keeps CHECK step.
    Both villains check the flop, then hero's turn decision.
    """
    from range_narrowing import narrow_by_action_history
    r = _sample_range()
    action_history = [
        {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
        {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        # Pure check-through flop
        {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
        {'street': 'flop', 'position': 'BTN', 'action': 'CHECK'},
    ]
    _, meta = narrow_by_action_history(
        r, ['Qh', '5d', '2c', '9s'], action_history,
        'BB', decision_street='turn',
    )
    # BB's flop sequence: [CHECK]. Single action → passthrough.
    # Chain shows flop:CHECK.
    assert 'flop:CHECK' in meta['chain_steps'], (
        f'Expected flop:CHECK for pure check-through: {meta["chain_steps"]}'
    )


if __name__ == '__main__':
    import subprocess
    rc = subprocess.call([sys.executable, '-m', 'pytest', '-xvs', __file__])
    sys.exit(rc)
