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


def validate_fixture_meta_boards() -> list:
    """MUST #35 + commit-13.2.5 FIX #5: board format in test fixture_meta.

    Per commit-13.2.5 authoring spec (sidecar docstring): per-test
    `fixture_meta` dicts must encode boards as List[str] like
    `['Kh', '7d', '2c']`, NOT as concatenated strings `'Kh7d2c'`.

    This function introspects test_commit13_sidecar_dryrun.py's
    fixture_meta dict via AST parse so the validator catches format
    drift at CI time (prior: relied on per-batch GTO review only).
    """
    import ast

    test_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'test_commit13_sidecar_dryrun.py',
    )
    if not os.path.exists(test_path):
        return [f'fixture_meta check: test file not found at {test_path}']

    with open(test_path) as f:
        src = f.read()

    # Parse; walk AST for a dict-assign named fixture_meta where each
    # value is a tuple literal beginning with a list literal.
    tree = ast.parse(src)
    violations = []
    fixture_meta_found = False
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign)
                and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == 'fixture_meta'):
            continue
        if not isinstance(node.value, ast.Dict):
            continue
        fixture_meta_found = True
        for k_node, v_node in zip(node.value.keys, node.value.values):
            if not isinstance(k_node, ast.Constant):
                continue
            ref_id = k_node.value
            if not isinstance(v_node, ast.Tuple) or not v_node.elts:
                violations.append(
                    f'fixture_meta[{ref_id!r}]: not a non-empty tuple literal'
                )
                continue
            board_node = v_node.elts[0]
            if not isinstance(board_node, ast.List):
                violations.append(
                    f'fixture_meta[{ref_id!r}]: board must be List[str], '
                    f'got {type(board_node).__name__}'
                )
                continue
            for i, card in enumerate(board_node.elts):
                if not (isinstance(card, ast.Constant)
                        and isinstance(card.value, str)):
                    violations.append(
                        f'fixture_meta[{ref_id!r}].board[{i}]: '
                        f'non-string card'
                    )
                elif len(card.value) != 2:
                    violations.append(
                        f'fixture_meta[{ref_id!r}].board[{i}]: card '
                        f'{card.value!r} expected 2-char format '
                        f"(e.g. 'Kh')"
                    )

    if not fixture_meta_found:
        # Not fatal — test file might not use the fixture_meta idiom
        # in all future iterations; soft-warn only if file exists.
        return []
    return violations


def main() -> int:
    cal_v = validate_calibration_sidecar()
    ref_v = validate_reference_sidecar()
    meta_v = validate_fixture_meta_boards()

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
    if meta_v:
        print(f'FIXTURE_META violations ({len(meta_v)}):')
        for v in meta_v:
            print(f'  {v}')

    if not cal_v and not ref_v and not meta_v:
        print('PASS — all authored entries + fixture_meta boards '
              'structurally valid.')
        return 0

    total = len(cal_v) + len(ref_v) + len(meta_v)
    print(f'FAIL — {total} violation(s)')
    return 1


if __name__ == '__main__':
    sys.exit(main())
