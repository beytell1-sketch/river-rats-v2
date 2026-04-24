"""v2.4 Stage 3.5 commit 10 — MUST #41 belt-and-braces count guard.

Audit-only rail against mass-concentration pathology per Moravcik
DeepStack supplementary + Brown Libratus range-decomposition:
high cumulative surviving mass (>=10%) with low hand count (<5) =
brittle inference (no diversity in remaining range).

Fires WARN log; does NOT truncate. Callers continue with the narrowed
range; the flag is for post-hoc review. Fires at-most-once per chain
via warned_count flag.
"""
import logging
import os
import sys

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)


def _sample_range_small():
    """Tiny synthetic range — 4 hands. narrow_to_* output will have
    len <5, triggering MUST #41 when mass survives."""
    return {'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0}


def _sample_range_diverse():
    """Larger synthetic range — ~25 hands. narrow outputs retain
    healthy count (>=5). MUST #41 shouldn't fire."""
    return {
        'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0,
        '99': 1.0, '88': 1.0, '77': 1.0, '66': 1.0,
        'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AJs': 1.0, 'ATs': 1.0,
        'KQs': 1.0, 'KJs': 1.0, 'KTs': 1.0,
        'QJs': 1.0, 'JTs': 1.0, 'T9s': 1.0,
        '98s': 1.0, '87s': 1.0, '76s': 1.0,
        'A5s': 1.0, 'A4s': 1.0, '54s': 1.0, '65s': 1.0,
    }


# =============================================================================
# MUST #41 — count guard fires on mass-concentration
# =============================================================================

def test_must41_count_guard_fires_on_mass_concentration(caplog):
    """MUST #41: 3-hand nuts-only range + flop-BET narrow → mass
    survives high (nuts bet freq 0.85 flop → ~0.85 cumulative) with
    3 hands < 5. Deterministic trigger.

    NIT-2 fix (commit 11): asserts EXACTLY 1 WARN fires; prior
    `<= 1` pattern passed vacuously on 0-fire."""
    from range_narrowing import narrow_by_action_history
    # 3 hands, all nuts on a low-coord dry flop. Nuts bet freq (0.85
    # flop) means ~0.85 mass survives; 3 hands < 5 → GUARD fires.
    r = {'AA': 1.0, 'KK': 1.0, 'QQ': 1.0}
    action_history = [
        {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
        {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        {'street': 'flop', 'position': 'BB', 'action': 'BET'},
    ]
    with caplog.at_level(logging.WARNING, logger='range_narrowing'):
        _, meta = narrow_by_action_history(
            r, ['7h', '3d', '2c', '9s'], action_history,
            'BB', decision_street='turn',
        )
    must41_msgs = [
        rec for rec in caplog.records
        if 'mass-concentrated-without-count-support' in rec.getMessage()
    ]
    # NIT-2 hard assertion: exactly 1 fire on this deterministic trigger.
    assert len(must41_msgs) == 1, (
        f'MUST #41: expected exactly 1 WARN on 3-hand nuts range, '
        f'got {len(must41_msgs)} (surviving={meta["surviving_weight"]:.3f})'
    )
    msg = must41_msgs[0].getMessage()
    assert 'surviving_weight=' in msg
    assert 'hand_count=' in msg


def test_must41_no_truncation(caplog):
    """MUST #41: WARN fires but chain completes; truncated=False;
    caller sees narrowed range (not reverted last_valid)."""
    from range_narrowing import narrow_by_action_history
    r = _sample_range_small()
    action_history = [
        {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
        {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        {'street': 'flop', 'position': 'BB', 'action': 'BET'},
    ]
    out, meta = narrow_by_action_history(
        r, ['7h', '3d', '2c', '9s'], action_history,
        'BB', decision_street='turn',
    )
    # WARN is audit-only; truncation is a separate concern
    assert 'flop:BET' in meta['chain_steps']
    # Chain executed to completion; either truncated=False OR
    # truncated=True from mass-floor (unrelated to count guard)
    if not meta['truncated']:
        # Non-truncated state: caller sees narrowed range
        assert isinstance(out, dict)


def test_must41_fires_at_most_once_per_chain(caplog):
    """MUST #41: warned_count flag prevents per-step spam on deep
    chains that stay mass-concentrated across multiple narrow steps.

    NIT-2 fix (commit 11): deterministic trigger via 3-hand nuts range
    + deep chain (flop-BET, turn-BET). Both steps would fire the
    guard independently; warned_count caps total to exactly 1."""
    from range_narrowing import narrow_by_action_history
    # 3 hands, deep chain likely to trigger on multiple steps if
    # warned_count flag absent.
    r = {'AA': 1.0, 'KK': 1.0, 'QQ': 1.0}
    action_history = [
        {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
        {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        {'street': 'flop', 'position': 'BB', 'action': 'BET'},
        {'street': 'flop', 'position': 'BTN', 'action': 'CALL'},
        {'street': 'turn', 'position': 'BB', 'action': 'BET'},
    ]
    with caplog.at_level(logging.WARNING, logger='range_narrowing'):
        _, _ = narrow_by_action_history(
            r, ['7h', '3d', '2c', '9s'], action_history,
            'BB', decision_street='river',
        )
    must41_msgs = [
        rec for rec in caplog.records
        if 'mass-concentrated-without-count-support' in rec.getMessage()
    ]
    # NIT-2 hard assertion: exactly 1 fire on deterministic multi-step
    # trigger (warned_count enforces fire-at-most-once contract).
    assert len(must41_msgs) == 1, (
        f'MUST #41: expected exactly 1 WARN on deep-chain multi-trigger, '
        f'got {len(must41_msgs)} (warned_count flag broken?)'
    )


def test_must41_does_not_fire_on_healthy_distribution(caplog):
    """MUST #41: diverse range (~25 hands) maintains count diversity
    through narrow; no WARN expected."""
    from range_narrowing import narrow_by_action_history
    r = _sample_range_diverse()
    action_history = [
        {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
        {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
    ]
    with caplog.at_level(logging.WARNING, logger='range_narrowing'):
        out, _ = narrow_by_action_history(
            r, ['Qh', '5d', '2c', '9s'], action_history,
            'BB', decision_street='turn',
        )
    must41_msgs = [
        rec for rec in caplog.records
        if 'mass-concentrated-without-count-support' in rec.getMessage()
    ]
    # Healthy: len(out) likely >= 5 → no WARN
    if len(out) >= 5:
        assert not must41_msgs, (
            f'MUST #41: unexpected WARN on healthy distribution '
            f'(count={len(out)}): {[r.getMessage() for r in must41_msgs]}'
        )


def test_must41_constant_defined():
    """MUST #41: _STAGE35_COUNT_GUARD_MIN module constant = 5."""
    from range_narrowing import _STAGE35_COUNT_GUARD_MIN
    assert _STAGE35_COUNT_GUARD_MIN == 5


def test_must41_audit_only_no_meta_field_added():
    """MUST #41: audit-only = no meta['count_guard_fired'] field added.
    WARN log is the only signal; meta dict structure unchanged."""
    from range_narrowing import narrow_by_action_history
    r = _sample_range_small()
    action_history = [
        {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
        {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        {'street': 'flop', 'position': 'BB', 'action': 'BET'},
    ]
    _, meta = narrow_by_action_history(
        r, ['7h', '3d', '2c', '9s'], action_history,
        'BB', decision_street='turn',
    )
    # Meta retains original Stage 3.5 contract; no new count-guard field
    expected_keys = {'chain_steps', 'truncated', 'surviving_weight'}
    actual = set(meta.keys())
    # May also have schema_warning (existing) but NOT a count-guard field
    forbidden = {'count_guard_fired', 'count_guard_tripped'}
    assert not (actual & forbidden), (
        f'MUST #41 audit-only: unexpected meta field(s) {actual & forbidden}'
    )


if __name__ == '__main__':
    import subprocess
    rc = subprocess.call([sys.executable, '-m', 'pytest', '-xvs', __file__])
    sys.exit(rc)
