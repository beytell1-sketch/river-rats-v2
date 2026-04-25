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

_EXPECTED_COMMIT13_REFIDS = {'MW-11', 'MW-30', 'FB-17', 'FB-23', 'MW-15'}
_EXPECTED_COMMIT13_2_SYN_REFIDS = {
    'SYN-F3_HU_folded', 'SYN-F5_HU_overflow', 'SYN-F6_MW_all_live',
    'SYN-T_J02_synthetic', 'SYN-T_B05_synthetic',
    # FIX #3 (commit 13.2.5): donk-line bucket
    'SYN-F7_HU_donk_x_bet',
}
# Commit 13.3.1 — batch 1 of 5 (~25-entry sub-batches per
# MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_2026-04-25.md). FB-01..20 minus
# FB-17 (already in commit 13 dry-run set) = 19 entries.
_EXPECTED_COMMIT13_3_1_REFIDS = {
    'FB-01', 'FB-02', 'FB-03', 'FB-04', 'FB-05', 'FB-06', 'FB-07',
    'FB-08', 'FB-09', 'FB-10', 'FB-11', 'FB-12', 'FB-13', 'FB-14',
    'FB-15', 'FB-16', 'FB-18', 'FB-19', 'FB-20',
}
# Commit 13.3.2 — batch 2 of 5. FB-21..40 minus FB-23 = 19 entries.
_EXPECTED_COMMIT13_3_2_REFIDS = {
    'FB-21', 'FB-22', 'FB-24', 'FB-25', 'FB-26', 'FB-27', 'FB-28',
    'FB-29', 'FB-30', 'FB-31', 'FB-32', 'FB-33', 'FB-34', 'FB-35',
    'FB-36', 'FB-37', 'FB-38', 'FB-39', 'FB-40',
}
_EXPECTED_REFERENCE_REFIDS = (
    _EXPECTED_COMMIT13_REFIDS
    | _EXPECTED_COMMIT13_2_SYN_REFIDS
    | _EXPECTED_COMMIT13_3_1_REFIDS
    | _EXPECTED_COMMIT13_3_2_REFIDS
)
_EXPECTED_CALIBRATION_REFIDS = {'MW-11', 'MW-30', 'MW-15'}


def test_reference_sidecar_has_commit13_plus_synthetic_entries():
    """Post-commit-13.2: _REFERENCE_ACTION_HISTORY has commit-13's 5
    real fixtures + commit-13.2's 5 synthetic SYN-* entries = 10 total."""
    from _reference_action_history_sidecar import _REFERENCE_ACTION_HISTORY
    assert set(_REFERENCE_ACTION_HISTORY.keys()) == _EXPECTED_REFERENCE_REFIDS, (
        f'Expected {_EXPECTED_REFERENCE_REFIDS}, got '
        f'{set(_REFERENCE_ACTION_HISTORY.keys())}'
    )


def test_reference_sidecar_synthetic_entries_use_syn_prefix():
    """Commit 13.2: synthetic entries distinguishable from real fixtures
    via SYN- prefix. Reviewer/audit-tooling can filter by vintage."""
    from _reference_action_history_sidecar import _REFERENCE_ACTION_HISTORY
    syn_keys = {k for k in _REFERENCE_ACTION_HISTORY if k.startswith('SYN-')}
    assert syn_keys == _EXPECTED_COMMIT13_2_SYN_REFIDS


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
    from _reference_action_history_sidecar import (
        _REFERENCE_ACTION_HISTORY,
        _REFERENCE_VILLAIN_POS,
    )
    by_shape = _stratify(_REFERENCE_ACTION_HISTORY, _REFERENCE_VILLAIN_POS)
    assert len(by_shape) >= 3, (
        f'Dry-run batch should cover ≥3 shapes; got {len(by_shape)}: '
        f'{list(by_shape.keys())}'
    )


def test_commit13_2_5_hu_donk_x_bet_bucket_covered():
    """FIX #3 (commit 13.2.5): SYN-F7_HU_donk_x_bet lands in the
    hu_donk_x_bet classifier bucket — covers the last real-world
    shape authoring pattern per GTO review recommendation.
    Commit 13.2.6: classifier signature now requires villain_pos;
    looked up from _REFERENCE_VILLAIN_POS."""
    from tests.solver_verify_sidecars import _classify_shape
    from _reference_action_history_sidecar import (
        _REFERENCE_ACTION_HISTORY,
        _REFERENCE_VILLAIN_POS,
    )
    ah = _REFERENCE_ACTION_HISTORY['SYN-F7_HU_donk_x_bet']
    villain_pos = _REFERENCE_VILLAIN_POS['SYN-F7_HU_donk_x_bet']
    shape = _classify_shape(ah, villain_pos)
    assert shape == 'hu_donk_x_bet', (
        f'SYN-F7 expected hu_donk_x_bet bucket; got {shape!r}'
    )


def test_commit13_2_6_classifier_position_aware_donk():
    """FIX #2 (commit 13.2.6, GTO review APPROVE_WITH_FIXES on 13.2.5):
    classifier's hu_donk_x_bet branch is position-aware. A hand where
    HERO bets flop and VILLAIN bets river (with check-through on turn)
    is NOT a donk shape from villain's range-narrowing POV — pre-fix
    this would mis-route to hu_donk_x_bet (position-agnostic
    flop_bet_count >= 1 matched any flop bettor); post-fix the
    flop_has_villain_bet predicate excludes it."""
    from tests.solver_verify_sidecars import _classify_shape

    # Hero=BTN bets flop, both check turn, Villain=BB bets river.
    # NOT a donk for villain BB (BB called flop, didn't donk).
    hero_bet_flop_villain_bet_river = [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'BB',  'CALL'),
        ('flop',    'BTN', 'BET'),     # HERO bets flop (not villain)
        ('flop',    'BB',  'CALL'),
        ('turn',    'BB',  'CHECK'),
        ('turn',    'BTN', 'CHECK'),
        ('river',   'BB',  'BET'),
    ]
    shape = _classify_shape(hero_bet_flop_villain_bet_river, villain_pos='BB')
    assert shape != 'hu_donk_x_bet', (
        f'Position-aware predicate must exclude hero-bet-flop case '
        f'from hu_donk_x_bet bucket; got {shape!r}'
    )

    # Regression guard: SYN-F7's real BB-donks-flop+BB-bets-river still
    # routes to hu_donk_x_bet (no regression on the original case).
    from _reference_action_history_sidecar import (
        _REFERENCE_ACTION_HISTORY,
        _REFERENCE_VILLAIN_POS,
    )
    syn_f7_ah = _REFERENCE_ACTION_HISTORY['SYN-F7_HU_donk_x_bet']
    syn_f7_pos = _REFERENCE_VILLAIN_POS['SYN-F7_HU_donk_x_bet']
    assert _classify_shape(syn_f7_ah, syn_f7_pos) == 'hu_donk_x_bet'

    # Regression guard: SYN-T_J02 still routes to hu_bet_x_call_bet
    # (4-class chain, turn_has_call=True) — unaffected by FIX #2 which
    # only touched the donk-shape branch.
    syn_tj02_ah = _REFERENCE_ACTION_HISTORY['SYN-T_J02_synthetic']
    syn_tj02_pos = _REFERENCE_VILLAIN_POS['SYN-T_J02_synthetic']
    assert _classify_shape(syn_tj02_ah, syn_tj02_pos) == 'hu_bet_x_call_bet'


def test_commit13_2_6_villain_pos_map_covers_all_reference_entries():
    """FIX #2 (commit 13.2.6): _REFERENCE_VILLAIN_POS must cover every
    ref_id in _REFERENCE_ACTION_HISTORY. _stratify raises KeyError on
    drift; this test catches it earlier with a clearer message."""
    from _reference_action_history_sidecar import (
        _REFERENCE_ACTION_HISTORY,
        _REFERENCE_VILLAIN_POS,
    )
    missing = set(_REFERENCE_ACTION_HISTORY) - set(_REFERENCE_VILLAIN_POS)
    assert not missing, (
        f'_REFERENCE_VILLAIN_POS missing entries for: {sorted(missing)}; '
        f'add to sidecar so classifier can apply position-aware predicate.'
    )


def test_commit13_2_5_fixture_meta_boards_list_of_strings():
    """FIX #5 (commit 13.2.5): validator extension catches fixture_meta
    board-format drift. Every fixture_meta board must be List[str]
    with 2-char card strings, not concatenated."""
    from tests.validate_sidecar_completeness import (
        validate_fixture_meta_boards,
    )
    violations = validate_fixture_meta_boards()
    assert not violations, (
        f'FIX #5: fixture_meta board-format violations:\n  '
        + '\n  '.join(violations)
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
        # Commit 13 real fixtures:
        'MW-11': (['Kh', '7d', '2c'], 'CO', 'flop', False),
        'MW-30': (['Qh', '5d', '2c'], 'CO', 'flop', False),
        'FB-17': (['9c', '6h', '3d', '2s'], 'CO', 'turn', True),
        'FB-23': (['9c', '6h', '3d', '2s', 'Kh'], 'CO', 'river', True),
        'MW-15': (['9c', '6h', '3d', '2s', 'Kh'], 'BB', 'river', True),
        # Commit 13.2 synthetic entries:
        # SYN-F3: HU folded — chain terminates at flop:FOLD; chain_steps
        # has flop:FOLD entry → expects_fire=True.
        'SYN-F3_HU_folded': (['Kh', '7d', '2c', '9s'], 'BB', 'turn', True),
        # SYN-F5: HU over-narrow — flop BET-CHECK-CALL collapses per
        # MUST #11 to flop:CALL; turn:CHECK-BET-CALL collapses to
        # turn:CALL; chain fires on river.
        'SYN-F5_HU_overflow': (['Kh', '7d', '2c', '9s', '5h'], 'BB', 'river', True),
        # SYN-F6: MW 3-way all-live — flop check-through (villain CO
        # checks) → chain fires flop:CHECK.
        'SYN-F6_MW_all_live': (['Kh', '7d', '2c', '9s'], 'CO', 'turn', True),
        # SYN-T_J02_synthetic: river decision, villain BB did flop:BET
        # + turn:CHECK→CALL collapse + (river-BET decision-street).
        # Chain: flop:BET + turn:CALL — fires.
        'SYN-T_J02_synthetic': (['Kh', '7d', '2c', '9s', '5h'], 'BB', 'river', True),
        # SYN-T_B05_synthetic: turn decision, villain BB did flop
        # BET-CALL (post-RAISE) collapsed via MUST #11/#12 to flop:CALL.
        # No turn actions before decision → chain fires flop:CALL only.
        'SYN-T_B05_synthetic': (['Kh', '7d', '2c', '9s'], 'BB', 'turn', True),
        # SYN-F7_HU_donk_x_bet (commit 13.2.5 FIX #3): river decision,
        # villain BB donked flop then check-turn. Chain: flop:BET +
        # turn:CHECK — fires. River-BET enters via facing_bet gate.
        'SYN-F7_HU_donk_x_bet': (['Kh', '7d', '2c', '9s', '5h'], 'BB', 'river', True),
        # ─────────────────────────────────────────────────────────────
        # Commit 13.3.1 — FB-01..20 (FB-17 above in commit-13 dryrun)
        # ─────────────────────────────────────────────────────────────
        # Boards from training-data/facing_bet_test_set_40.jsonl. All
        # FB-01..16 are flop decisions → expects_chain_fire=False (no
        # prior postflop street). FB-18/19/20 are turn decisions with
        # at least one prior-street villain action → expects_fire=True.
        'FB-01': (['Ah', '6d', '2c'], 'CO', 'flop', False),
        'FB-02': (['Ah', '6d', '2c'], 'BB', 'flop', False),
        'FB-03': (['Ah', '6d', '2c'], 'CO', 'flop', False),
        'FB-04': (['Kc', '8c', '4d'], 'CO', 'flop', False),
        'FB-05': (['Kc', '8c', '4d'], 'CO', 'flop', False),
        'FB-06': (['Jd', '8s', '6h'], 'CO', 'flop', False),
        'FB-07': (['Jd', '8s', '6h'], 'BB', 'flop', False),
        'FB-08': (['Qh', '7h', '3s'], 'BB', 'flop', False),
        'FB-09': (['Qh', '7h', '3s'], 'CO', 'flop', False),
        'FB-10': (['As', '9s', '4s'], 'CO', 'flop', False),
        'FB-11': (['As', '9s', '4s'], 'BB', 'flop', False),
        'FB-12': (['Th', 'Td', '7c'], 'BTN', 'flop', False),
        'FB-13': (['Th', 'Td', '7c'], 'BTN', 'flop', False),
        'FB-14': (['9d', '7d', '2c'], 'BB', 'flop', False),
        'FB-15': (['9d', '7d', '2c'], 'CO', 'flop', False),
        'FB-16': (['9d', '7d', '2c'], 'CO', 'flop', False),
        # Turn decisions: chain fires on prior-street villain action.
        'FB-18': (['Ac', 'Jh', '5d', 'Ks'], 'CO', 'turn', True),    # flop:CHECK
        'FB-19': (['Kh', '6h', '3d', 'Qc'], 'BTN', 'turn', True),   # flop:CALL
        'FB-20': (['Kh', '6h', '3d', 'Qc'], 'BTN', 'turn', True),   # flop:BET
        # ─────────────────────────────────────────────────────────────
        # Commit 13.3.2 — FB-21..40 (FB-23 above in commit-13 dryrun)
        # ─────────────────────────────────────────────────────────────
        # Boards from training-data/facing_bet_test_set_40.jsonl. Mix of
        # flop / turn / river decisions per the JSONL `street` field.
        # Flop decisions (FB-22/27/28/29/30/31/32/33/34/40):
        #   expects_chain_fire=False (no prior postflop street).
        # Turn decisions (FB-21/35/36/37):
        #   expects_chain_fire=True (prior flop chain step).
        # River decisions (FB-24/25/26/38/39):
        #   expects_chain_fire=True (prior flop+turn chain steps, or
        #   prior flop+turn aggression chain).
        'FB-21': (['Ts', '8c', '4h', 'Jd'],       'CO',  'turn',  True),   # flop:CHECK
        'FB-22': (['Ts', '8c', '4h'],             'BTN', 'flop',  False),
        'FB-24': (['Ad', '9c', '3h', '2s', 'Kd'], 'BB',  'river', True),   # flop:CHECK + turn:CHECK
        'FB-25': (['Qd', '8d', '4c', '7s', 'Jh'], 'CO',  'river', True),   # flop:BET + turn:BET
        'FB-26': (['Qd', '8d', '4c', '7s', 'Jh'], 'BB',  'river', True),   # flop:CHECK + turn:CHECK
        'FB-27': (['8s', '5s', '3d'],             'CO',  'flop',  False),
        'FB-28': (['8s', '5s', '3d'],             'CO',  'flop',  False),
        'FB-29': (['8s', '5s', '3d'],             'BB',  'flop',  False),
        'FB-30': (['8s', '5s', '3d'],             'CO',  'flop',  False),
        'FB-31': (['Jd', '8s', '6h'],             'BB',  'flop',  False),
        'FB-32': (['Jd', '8s', '6h'],             'CO',  'flop',  False),
        'FB-33': (['Th', 'Td', '7c'],             'BTN', 'flop',  False),
        'FB-34': (['As', '9s', '4s'],             'BTN', 'flop',  False),
        'FB-35': (['Kh', '6h', '3d', 'Qc'],       'BTN', 'turn',  True),   # flop:BET
        'FB-36': (['Ts', '8c', '4h', 'Jd'],       'BTN', 'turn',  True),   # flop:BET
        'FB-37': (['Ac', 'Jh', '5d', 'Ks'],       'BTN', 'turn',  True),   # flop:CHECK
        'FB-38': (['Ad', '9c', '3h', '2s', 'Kd'], 'BB',  'river', True),   # flop:CHECK + turn:CHECK
        'FB-39': (['Qd', '8d', '4c', '7s', 'Jh'], 'BTN', 'river', True),   # flop:CHECK + turn:CHECK
        'FB-40': (['Kc', '8c', '4d'],             'BTN', 'flop',  False),
    }

    for ref_id, ah in _REFERENCE_ACTION_HISTORY.items():
        assert ref_id in fixture_meta, (
            f'test fixture_meta missing entry for {ref_id}; '
            f'update test when adding sidecar entries'
        )
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
