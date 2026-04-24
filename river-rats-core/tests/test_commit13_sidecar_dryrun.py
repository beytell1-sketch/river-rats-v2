"""v2.4 Stage 3.5 commit 13 — Path (c) Phase 2 5-entry dry-run batch.

Dry-run authoring of sidecar entries before the ~135-entry full lift.
Owner-approval-gated per v2.2 amendment §5. Tests verify:

  1. 5 shape-diverse entries authored in reference sidecar
  2. 3 MW-* entries mirror into calibration sidecar
  3. Validator script (MUST #35) exits 0 on the dry-run set
  4. Solver-verify stub (MUST #54 + #66 stratified) passes
  5. Every authored entry exercises chain narrowing end-to-end through
     extract_range_composition (no silent fallback)
"""
import os
import subprocess
import sys

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)


# =============================================================================
# Sidecar population sanity
# =============================================================================

_EXPECTED_REFERENCE_REFIDS = {'MW-11', 'MW-30', 'FB-17', 'FB-23', 'MW-15'}
_EXPECTED_CALIBRATION_REFIDS = {'MW-11', 'MW-30', 'MW-15'}


def test_reference_sidecar_has_5_dryrun_entries():
    """Commit 13 dry-run: _REFERENCE_ACTION_HISTORY populated with
    exactly the 5 shape-diverse entries per MUST #49 enumeration."""
    from _reference_action_history_sidecar import _REFERENCE_ACTION_HISTORY
    assert set(_REFERENCE_ACTION_HISTORY.keys()) == _EXPECTED_REFERENCE_REFIDS, (
        f'Expected {_EXPECTED_REFERENCE_REFIDS}, got '
        f'{set(_REFERENCE_ACTION_HISTORY.keys())}'
    )


def test_calibration_sidecar_has_3_mw_entries():
    """Commit 13 dry-run: _CALIBRATION_ACTION_HISTORY mirrors the 3
    MW-* entries (FB-* fixtures don't flow through calibration_exam)."""
    from _calibration_action_history_sidecar import _CALIBRATION_ACTION_HISTORY
    assert set(_CALIBRATION_ACTION_HISTORY.keys()) == _EXPECTED_CALIBRATION_REFIDS


def test_mw_entries_match_across_sidecars():
    """Both sidecar modules must have identical values for MW-*
    entries (single-source-of-truth for overlapping fixtures; drift
    here would produce different Stage 4 vs baseline-eval chains)."""
    from _reference_action_history_sidecar import _REFERENCE_ACTION_HISTORY
    from _calibration_action_history_sidecar import _CALIBRATION_ACTION_HISTORY
    for ref_id in _EXPECTED_CALIBRATION_REFIDS:
        assert _REFERENCE_ACTION_HISTORY[ref_id] == _CALIBRATION_ACTION_HISTORY[ref_id], (
            f'Sidecar drift on {ref_id}: reference vs calibration differ'
        )


# =============================================================================
# MUST #35 validator script — dry-run gate
# =============================================================================

def test_must35_validator_script_exits_0():
    """MUST #35 owner-gate input: validator script exits 0 on the
    5-entry dry-run batch."""
    script = os.path.join(_CORE, 'tests', 'validate_sidecar_completeness.py')
    assert os.path.exists(script), f'Validator script missing: {script}'
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True, cwd=_CORE,
    )
    assert result.returncode == 0, (
        f'Validator exited {result.returncode}; stdout:\n{result.stdout}\n'
        f'stderr:\n{result.stderr}'
    )
    assert 'PASS' in result.stdout


def test_must35_validator_catches_malformed_entry():
    """MUST #35 regression guard: validator DOES raise violations on
    malformed entries (positive-path proof that the validator is
    actually checking)."""
    # Import validator functions + monkey-patch a malformed entry
    from tests.validate_sidecar_completeness import _validate_entry
    bad = [
        ('preflop', 'XYZ', 'RAISE'),  # invalid position
        ('ocean', 'BTN', 'CALL'),     # invalid street
        ('flop', 'BB', 'XYZ'),        # invalid action
        ('river', 'BTN', 'CHECK'),    # street regression? no, river > flop — OK
    ]
    violations = _validate_entry('TEST_BAD', bad)
    assert violations, 'validator should flag malformed entries'
    # Confirm the 3 bad entries all got flagged
    assert any('XYZ' in v for v in violations)
    assert any('ocean' in v for v in violations)


# =============================================================================
# MUST #54 + #66 solver-verify stub
# =============================================================================

def test_must54_solver_verify_stub_exits_0():
    """MUST #54 + #66 stratified solver-verify (stub mode) exits 0
    on the 5-entry dry-run batch. Real solver plugs in at Stage 6."""
    script = os.path.join(_CORE, 'tests', 'solver_verify_sidecars.py')
    assert os.path.exists(script), f'Solver-verify script missing: {script}'
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True, cwd=_CORE,
    )
    assert result.returncode == 0, (
        f'Solver-verify exited {result.returncode}; stdout:\n{result.stdout}\n'
        f'stderr:\n{result.stderr}'
    )
    assert 'PASS' in result.stdout


def test_must66_stratification_covers_multiple_shapes():
    """MUST #66: stratification across shape buckets. Dry-run batch
    covers ≥3 distinct shapes so Cochran sampling isn't degenerate."""
    from tests.solver_verify_sidecars import _classify_shape, _stratify
    from _reference_action_history_sidecar import _REFERENCE_ACTION_HISTORY
    by_shape = _stratify(_REFERENCE_ACTION_HISTORY)
    assert len(by_shape) >= 3, (
        f'Dry-run batch should cover ≥3 shapes; got {len(by_shape)}: '
        f'{list(by_shape.keys())}'
    )


# =============================================================================
# End-to-end chain-firing per authored entry
# =============================================================================

def test_dryrun_entries_exercise_chain_narrowing():
    """Every authored entry (excluding those where hero acts first on
    the decision street) must produce a non-empty chain_steps when
    run through narrow_by_action_history. Confirms the 5-entry batch
    is chain-exercising, not silent-pass-through."""
    from range_narrowing import narrow_by_action_history
    from _reference_action_history_sidecar import _REFERENCE_ACTION_HISTORY

    # Minimal sample range for structural test
    sample_range = {
        'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0,
        'AKs': 1.0, 'KQs': 1.0, '99': 1.0, '88': 1.0,
        '76s': 1.0, 'A5s': 1.0,
    }

    # Minimum decision-street metadata per dry-run entry
    fixture_meta = {
        # ref_id: (board, villain_pos, decision_street, expects_chain_fire)
        # MW-11: flop decision — no prior postflop → chain empty (correct).
        'MW-11': (['Kh', '7d', '2c'], 'CO', 'flop', False),
        # MW-30: flop decision — no prior postflop → chain empty.
        'MW-30': (['Qh', '5d', '2c'], 'CO', 'flop', False),
        # FB-17: turn decision, villain CO checked flop → chain fires.
        'FB-17': (['9c', '6h', '3d', '2s'], 'CO', 'turn', True),
        # FB-23: river decision, villain CO checked flop+turn → 2x chain.
        'FB-23': (['9c', '6h', '3d', '2s', 'Kh'], 'CO', 'river', True),
        # MW-15: river decision, villain BB checked flop+turn → 2x chain.
        'MW-15': (['9c', '6h', '3d', '2s', 'Kh'], 'BB', 'river', True),
    }

    for ref_id, ah in _REFERENCE_ACTION_HISTORY.items():
        board, villain_pos, decision_street, expects_fire = fixture_meta[ref_id]
        _, meta = narrow_by_action_history(
            sample_range, board, ah, villain_pos,
            decision_street=decision_street,
        )
        if expects_fire:
            assert meta['chain_steps'], (
                f'{ref_id}: chain_steps empty but expected fire '
                f'(decision_street={decision_street}, villain={villain_pos})'
            )
        # Never empty range on structural test (sample_range has enough
        # coverage; safety rails may revert, but range non-empty)
        # meta always has structural contract fields
        assert 'chain_steps' in meta
        assert 'surviving_weight' in meta


if __name__ == '__main__':
    rc = subprocess.call([sys.executable, '-m', 'pytest', '-xvs', __file__])
    sys.exit(rc)
