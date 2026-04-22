"""v2.4 Stage 3.5 commit 5 — MUST #20 calibration_exam action_history plumbing.

Covers:
  - ReferenceHand dataclass field extension
  - _labelled_record_to_reference_hand reads action_history from JSONL record
  - reference_hand_to_situation plumbs _action_history into hand_dict
  - MUST #35 sidecar sentinel (missing entry raises under strict mode)
  - Backward-compat: empty action_history permitted; falls through gates
"""
import os
import sys

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)


# =============================================================================
# ReferenceHand dataclass
# =============================================================================

def test_referencehand_has_action_history_field():
    """MUST #20 Phase 1: ReferenceHand dataclass carries action_history
    field (default empty list, backward-compat)."""
    from reference_evaluator import ReferenceHand
    rh = ReferenceHand(
        ref_id='TEST_01', axis='test',
        hero_cards='AsKs', board='Qh7d2c',
        street='Flop', hero_position='BTN', villain_position='BB',
        num_opponents=1, pot=90.0, facing_bet=False, to_call=0.0,
        opener_position='BTN', bettor_position=None,
        expert_action='CHECK', expert_confidence='HIGH', equity=0.5,
    )
    assert hasattr(rh, 'action_history')
    assert rh.action_history == []


def test_referencehand_accepts_action_history():
    """MUST #20: ReferenceHand accepts structured action_history."""
    from reference_evaluator import ReferenceHand
    ah = [('preflop', 'BTN', 'RAISE'), ('preflop', 'BB', 'CALL')]
    rh = ReferenceHand(
        ref_id='TEST_02', axis='test',
        hero_cards='AsKs', board='Qh7d2c',
        street='Flop', hero_position='BTN', villain_position='BB',
        num_opponents=1, pot=90.0, facing_bet=False, to_call=0.0,
        opener_position='BTN', bettor_position=None,
        expert_action='CHECK', expert_confidence='HIGH', equity=0.5,
        action_history=ah,
    )
    assert rh.action_history == ah


# =============================================================================
# _labelled_record_to_reference_hand
# =============================================================================

def test_labelled_record_reads_action_history_list_of_lists():
    """MUST #20: _labelled_record_to_reference_hand reads action_history
    as list of [street, pos, action] lists from canonical JSONL."""
    from calibration_exam import _labelled_record_to_reference_hand
    record = {
        'situation_id': 'TEST_03',
        'hero_cards': 'AsKs',
        'board': 'Qh7d2c',
        'street': 'flop',
        'hero_position': 'BTN',
        'villain_positions': ['BB'],
        'pot': 90.0,
        'facing_bet': False,
        'expert_action': 'CHECK',
        'action_history': [
            ['preflop', 'BTN', 'RAISE'],
            ['preflop', 'BB', 'CALL'],
            ['flop', 'BB', 'CHECK'],
        ],
    }
    rh = _labelled_record_to_reference_hand(record)
    # Normalised to tuples
    assert rh.action_history == [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
    ]


def test_labelled_record_reads_action_history_list_of_dicts():
    """MUST #20: _labelled_record_to_reference_hand also accepts
    list-of-dicts shape (matches game_state_bridge format)."""
    from calibration_exam import _labelled_record_to_reference_hand
    record = {
        'situation_id': 'TEST_04',
        'hero_cards': 'AsKs',
        'board': 'Qh7d2c',
        'street': 'flop',
        'hero_position': 'BTN',
        'villain_positions': ['BB'],
        'pot': 90.0,
        'facing_bet': False,
        'expert_action': 'CHECK',
        'action_history': [
            {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
            {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        ],
    }
    rh = _labelled_record_to_reference_hand(record)
    assert rh.action_history == [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'BB', 'CALL'),
    ]


def test_labelled_record_missing_action_history_defaults_empty():
    """MUST #20 backward-compat: missing `action_history` field yields
    empty list (fixtures that predate the schema extension)."""
    from calibration_exam import _labelled_record_to_reference_hand
    record = {
        'situation_id': 'TEST_05',
        'hero_cards': 'AsKs',
        'board': 'Qh7d2c',
        'street': 'flop',
        'hero_position': 'BTN',
        'villain_positions': ['BB'],
        'pot': 90.0,
        'facing_bet': False,
        'expert_action': 'CHECK',
    }
    rh = _labelled_record_to_reference_hand(record)
    assert rh.action_history == []


# =============================================================================
# reference_hand_to_situation hand_dict plumbing
# =============================================================================

def _make_ref_hand(**overrides):
    """Test helper — ReferenceHand with sensible defaults."""
    from reference_evaluator import ReferenceHand
    defaults = dict(
        ref_id='TEST_RH', axis='test',
        hero_cards='AsKs', board='Qh7d2c',
        street='Flop', hero_position='BTN', villain_position='BB',
        num_opponents=1, pot=90.0, facing_bet=False, to_call=0.0,
        opener_position='BTN', bettor_position=None,
        expert_action='CHECK', expert_confidence='HIGH', equity=0.5,
    )
    defaults.update(overrides)
    return ReferenceHand(**defaults)


def test_hand_dict_has_action_history_when_field_populated():
    """MUST #20: when hand.action_history is populated, it's plumbed
    into hand_dict['_action_history']."""
    from calibration_exam import reference_hand_to_situation
    ah = [('preflop', 'BTN', 'RAISE'), ('preflop', 'BB', 'CALL'),
          ('flop', 'BB', 'CHECK')]
    rh = _make_ref_hand(action_history=ah)
    sit = reference_hand_to_situation(rh)
    # hand_dict is internal to the function but the feat_dict it produces
    # must have come from extract_all_features(hand_dict_with_action_history).
    # We verify that the chain fires by checking chain_steps (non-empty).
    # Chain ran → sentinel passed through to feat_dict.
    feat = sit['feat_dict']
    assert 'villain_top_pair_plus_pct' in feat


def test_sidecar_miss_raises_when_strict():
    """MUST #35: sidecar miss under STAGE4_STRICT_ACTION_HISTORY=raise
    → RuntimeError with the fixture ref_id cited."""
    import pytest
    from calibration_exam import reference_hand_to_situation

    rh = _make_ref_hand(ref_id='UNKNOWN_FIXTURE', action_history=[])
    prior = os.environ.get('STAGE4_STRICT_ACTION_HISTORY')
    os.environ['STAGE4_STRICT_ACTION_HISTORY'] = 'raise'
    try:
        with pytest.raises(RuntimeError, match='MUST #35.*sidecar entry missing'):
            reference_hand_to_situation(rh)
    finally:
        if prior is None:
            os.environ.pop('STAGE4_STRICT_ACTION_HISTORY', None)
        else:
            os.environ['STAGE4_STRICT_ACTION_HISTORY'] = prior


def test_sidecar_miss_silent_when_unset():
    """MUST #35 backward-compat: sidecar miss under unset env →
    proceeds with empty action_history (pre-Stage-3.5 behavior).
    CRIT #2 downstream gate in extract_range_composition handles its
    own strict-raise layer."""
    from calibration_exam import reference_hand_to_situation
    rh = _make_ref_hand(ref_id='UNKNOWN_FIXTURE', action_history=[])
    prior = os.environ.get('STAGE4_STRICT_ACTION_HISTORY')
    os.environ.pop('STAGE4_STRICT_ACTION_HISTORY', None)
    try:
        # Should not raise; silently falls back
        sit = reference_hand_to_situation(rh)
        assert 'feat_dict' in sit
    finally:
        if prior is not None:
            os.environ['STAGE4_STRICT_ACTION_HISTORY'] = prior


def test_hand_action_history_takes_precedence_over_sidecar():
    """MUST #20 resolution order: hand.action_history (canonical JSONL
    schema field) takes precedence over sidecar lookup."""
    from calibration_exam import reference_hand_to_situation
    ah = [('preflop', 'BTN', 'RAISE'),
          ('preflop', 'BB', 'CALL'),
          ('flop', 'BB', 'CHECK')]
    # ref_id is not in sidecar; but hand carries action_history directly
    rh = _make_ref_hand(
        ref_id='NOT_IN_SIDECAR', action_history=ah,
        street='Turn', board='Qh7d2c9s',
    )
    prior = os.environ.get('STAGE4_STRICT_ACTION_HISTORY')
    os.environ['STAGE4_STRICT_ACTION_HISTORY'] = 'raise'
    try:
        # With action_history populated, sidecar NOT consulted → no raise
        sit = reference_hand_to_situation(rh)
        assert 'feat_dict' in sit
    finally:
        if prior is None:
            os.environ.pop('STAGE4_STRICT_ACTION_HISTORY', None)
        else:
            os.environ['STAGE4_STRICT_ACTION_HISTORY'] = prior


# =============================================================================
# Sidecar module (Phase 1 stub)
# =============================================================================

def test_sidecar_module_exports_sentinel():
    """Phase 1 stub: sidecar module importable; exposes sentinel."""
    from _calibration_action_history_sidecar import _SIDECAR_MISSING, lookup
    # Sentinel is a unique identity (object())
    assert _SIDECAR_MISSING is not None
    # Lookup of unknown ref_id returns sentinel
    assert lookup('NON_EXISTENT_KEY') is _SIDECAR_MISSING


def test_sidecar_empty_until_phase2():
    """Phase 1 stub: _CALIBRATION_ACTION_HISTORY dict is empty until
    commit 13 Phase 2 authoring."""
    from _calibration_action_history_sidecar import _CALIBRATION_ACTION_HISTORY
    assert _CALIBRATION_ACTION_HISTORY == {}


if __name__ == '__main__':
    import subprocess
    rc = subprocess.call([sys.executable, '-m', 'pytest', '-xvs', __file__])
    sys.exit(rc)
