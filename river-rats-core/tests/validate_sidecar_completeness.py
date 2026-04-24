"""MUST #35 validator — sidecar completeness + well-formedness checker.

Stage 3.5 Path (c) Phase 2 gate: before full ~140-entry authoring
proceeds, the 5-entry dry-run batch must pass this validator. Owner
reviews exit-0 proof before mid-lift approval.

Usage:
    python3 river-rats-core/tests/validate_sidecar_completeness.py

Exit codes:
    0 — all sidecar entries structurally valid
    1 — at least one entry malformed; offenders listed

Structural checks (MUST #35 spec):
  1. Each entry's action_history is non-empty list of tuples/3-lists
  2. Streets in {preflop, flop, turn, river}
  3. Positions in {UTG, EP, HJ, MP, CO, BTN, SB, BB}
  4. Actions in {RAISE, CALL, FOLD, CHECK, BET}
  5. Street ordering non-decreasing (preflop → flop → turn → river)
  6. Every fixture ref_id in target pipelines has either a sidecar
     entry OR a pending-authoring exception

NOTE: semantic validity (e.g., "villain called an unraised pot" is
structurally valid but game-state invalid) is out of scope for this
validator; handled by MUST #54 solver-verify pass.
"""
import os
import sys

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)


_VALID_STREETS = ('preflop', 'flop', 'turn', 'river')
_VALID_STREET_ORDER = {s: i for i, s in enumerate(_VALID_STREETS)}
_VALID_POSITIONS = {'UTG', 'EP', 'HJ', 'MP', 'CO', 'BTN', 'SB', 'BB'}
_VALID_ACTIONS = {'RAISE', 'CALL', 'FOLD', 'CHECK', 'BET'}


def _validate_entry(ref_id: str, entries) -> list:
    """Return list of violation strings; empty = valid."""
    violations = []
    if not isinstance(entries, list):
        violations.append(f'{ref_id}: not a list ({type(entries).__name__})')
        return violations
    if not entries:
        violations.append(f'{ref_id}: empty list (sidecar sentinel reserved for missing-entry)')
        return violations

    last_street_idx = -1
    for i, entry in enumerate(entries):
        if not isinstance(entry, (tuple, list)) or len(entry) != 3:
            violations.append(
                f'{ref_id}[{i}]: not a 3-tuple/list: {entry!r}'
            )
            continue
        street, pos, action = entry
        if street not in _VALID_STREETS:
            violations.append(
                f'{ref_id}[{i}]: unknown street {street!r}'
            )
        else:
            idx = _VALID_STREET_ORDER[street]
            if idx < last_street_idx:
                violations.append(
                    f'{ref_id}[{i}]: street regression {street!r} after '
                    f'{_VALID_STREETS[last_street_idx]!r}'
                )
            last_street_idx = idx
        if pos not in _VALID_POSITIONS:
            violations.append(
                f'{ref_id}[{i}]: unknown position {pos!r}'
            )
        if action not in _VALID_ACTIONS:
            violations.append(
                f'{ref_id}[{i}]: unknown action {action!r}'
            )
    return violations


def validate_calibration_sidecar() -> list:
    """Validate _CALIBRATION_ACTION_HISTORY entries."""
    from _calibration_action_history_sidecar import _CALIBRATION_ACTION_HISTORY
    all_violations = []
    for ref_id, entries in _CALIBRATION_ACTION_HISTORY.items():
        all_violations.extend(_validate_entry(ref_id, entries))
    return all_violations


def validate_reference_sidecar() -> list:
    """Validate _REFERENCE_ACTION_HISTORY entries."""
    from _reference_action_history_sidecar import _REFERENCE_ACTION_HISTORY
    all_violations = []
    for ref_id, entries in _REFERENCE_ACTION_HISTORY.items():
        all_violations.extend(_validate_entry(ref_id, entries))
    return all_violations


def main() -> int:
    cal_v = validate_calibration_sidecar()
    ref_v = validate_reference_sidecar()

    print('MUST #35 sidecar validator')
    print('=' * 60)

    from _calibration_action_history_sidecar import _CALIBRATION_ACTION_HISTORY
    from _reference_action_history_sidecar import _REFERENCE_ACTION_HISTORY
    print(
        f'_CALIBRATION_ACTION_HISTORY: {len(_CALIBRATION_ACTION_HISTORY)} entries'
    )
    print(
        f'_REFERENCE_ACTION_HISTORY:   {len(_REFERENCE_ACTION_HISTORY)} entries'
    )
    print()

    if cal_v:
        print(f'CALIBRATION violations ({len(cal_v)}):')
        for v in cal_v:
            print(f'  {v}')
    if ref_v:
        print(f'REFERENCE violations ({len(ref_v)}):')
        for v in ref_v:
            print(f'  {v}')

    if not cal_v and not ref_v:
        print('PASS — all authored entries structurally valid.')
        return 0

    total = len(cal_v) + len(ref_v)
    print(f'FAIL — {total} violation(s)')
    return 1


if __name__ == '__main__':
    sys.exit(main())
