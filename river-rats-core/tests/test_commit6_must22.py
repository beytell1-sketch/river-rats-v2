"""v2.4 Stage 3.5 commit 6 — MUST #22 reference_evaluator action_history plumbing.

Covers both FB-40 (facing-bet test set) and MW-50 (multiway reference
set) paths. Parallel to commit 5's calibration_exam tests; reuses the
ReferenceHand field extension from commit 5.

Covered:
  - _resolve_action_history_for_ref_hand (MW path)
  - _resolve_action_history_for_record   (FB path)
  - _build_fb_hand_dict plumbs _action_history
  - _evaluate_one_hand (via _resolve helper) plumbs _action_history
  - MUST #35 sentinel semantics (identity compare; raise under strict)
  - Sidecar module Phase 1 stub
"""
import os
import sys

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)


def _make_ref_hand(**overrides):
    """Test helper — ReferenceHand with sensible defaults."""
    from reference_evaluator import ReferenceHand
    defaults = dict(
        ref_id='TEST_RE_01', axis='test',
        hero_cards='AsKs', board='Qh7d2c',
        street='Flop', hero_position='BTN', villain_position='BB',
        num_opponents=1, pot=90.0, facing_bet=False, to_call=0.0,
        opener_position='BTN', bettor_position=None,
        expert_action='CHECK', expert_confidence='HIGH', equity=0.5,
    )
    defaults.update(overrides)
    return ReferenceHand(**defaults)


# =============================================================================
# Sidecar module Phase 1 stub
# =============================================================================

def test_reference_sidecar_module_stub_importable():
    """Phase 1 stub: sidecar module imports; exposes sentinel + lookup."""
    from _reference_action_history_sidecar import (
        _SIDECAR_MISSING, lookup, _REFERENCE_ACTION_HISTORY,
    )
    assert _SIDECAR_MISSING is not None
    assert lookup('NONEXISTENT') is _SIDECAR_MISSING
    assert _REFERENCE_ACTION_HISTORY == {}


def test_reference_sidecar_shares_sentinel_with_calibration():
    """Single source of truth — reference sidecar reuses calibration
    sidecar's _SIDECAR_MISSING (identity equality works across modules)."""
    from _reference_action_history_sidecar import _SIDECAR_MISSING as ref_sentinel
    from _calibration_action_history_sidecar import _SIDECAR_MISSING as cal_sentinel
    assert ref_sentinel is cal_sentinel


# =============================================================================
# _resolve_action_history_for_ref_hand (MW-50 path)
# =============================================================================

def test_resolve_mw_uses_hand_field_when_populated():
    """MUST #22: hand.action_history (from commit 5 schema extension)
    takes precedence over sidecar lookup."""
    from reference_evaluator import _resolve_action_history_for_ref_hand
    ah = [('preflop', 'BTN', 'RAISE'), ('preflop', 'BB', 'CALL')]
    rh = _make_ref_hand(action_history=ah)
    out = _resolve_action_history_for_ref_hand(rh)
    assert out == ah


def test_resolve_mw_falls_to_sidecar_when_hand_field_empty():
    """MUST #22: hand.action_history empty → sidecar consulted.
    Phase 1 stub returns _SIDECAR_MISSING; resolution = empty list
    under unset/warn env."""
    from reference_evaluator import _resolve_action_history_for_ref_hand
    rh = _make_ref_hand(ref_id='NOT_IN_SIDECAR', action_history=[])
    prior = os.environ.get('STAGE4_STRICT_ACTION_HISTORY')
    os.environ.pop('STAGE4_STRICT_ACTION_HISTORY', None)
    try:
        out = _resolve_action_history_for_ref_hand(rh)
        assert out == []
    finally:
        if prior is not None:
            os.environ['STAGE4_STRICT_ACTION_HISTORY'] = prior


def test_resolve_mw_sidecar_miss_raises_when_strict():
    """MUST #35: sidecar miss under STAGE4_STRICT_ACTION_HISTORY=raise
    → RuntimeError citing reference fixture ref_id."""
    import pytest
    from reference_evaluator import _resolve_action_history_for_ref_hand
    rh = _make_ref_hand(ref_id='UNKNOWN_MW_FIXTURE', action_history=[])
    prior = os.environ.get('STAGE4_STRICT_ACTION_HISTORY')
    os.environ['STAGE4_STRICT_ACTION_HISTORY'] = 'raise'
    try:
        with pytest.raises(
            RuntimeError,
            match='MUST #35.*sidecar entry missing.*reference fixture',
        ):
            _resolve_action_history_for_ref_hand(rh)
    finally:
        if prior is None:
            os.environ.pop('STAGE4_STRICT_ACTION_HISTORY', None)
        else:
            os.environ['STAGE4_STRICT_ACTION_HISTORY'] = prior


# =============================================================================
# _resolve_action_history_for_record (FB-40 path)
# =============================================================================

def test_resolve_fb_uses_record_field_when_populated():
    """MUST #22: record.action_history field takes precedence over
    sidecar when non-empty. Accepts list-of-lists shape."""
    from reference_evaluator import _resolve_action_history_for_record
    record = {
        'situation_id': 'FB-TEST_01',
        'action_history': [
            ['preflop', 'CO', 'RAISE'],
            ['preflop', 'BTN', 'CALL'],
            ['flop', 'CO', 'BET'],
        ],
    }
    out = _resolve_action_history_for_record('FB-TEST_01', record)
    assert out == [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('flop', 'CO', 'BET'),
    ]


def test_resolve_fb_accepts_list_of_dicts():
    """MUST #22: list-of-dicts shape (game_state_bridge format)
    normalised to tuples."""
    from reference_evaluator import _resolve_action_history_for_record
    record = {
        'situation_id': 'FB-TEST_02',
        'action_history': [
            {'street': 'preflop', 'position': 'CO', 'action': 'RAISE'},
            {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        ],
    }
    out = _resolve_action_history_for_record('FB-TEST_02', record)
    assert out == [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BB', 'CALL'),
    ]


def test_resolve_fb_falls_to_sidecar_when_record_empty():
    """MUST #22: record.action_history absent → sidecar consulted."""
    from reference_evaluator import _resolve_action_history_for_record
    record = {'situation_id': 'FB-TEST_03'}  # no action_history field
    prior = os.environ.get('STAGE4_STRICT_ACTION_HISTORY')
    os.environ.pop('STAGE4_STRICT_ACTION_HISTORY', None)
    try:
        out = _resolve_action_history_for_record('FB-TEST_03', record)
        # Phase 1 stub: sidecar empty → fallback empty list
        assert out == []
    finally:
        if prior is not None:
            os.environ['STAGE4_STRICT_ACTION_HISTORY'] = prior


def test_resolve_fb_sidecar_miss_raises_when_strict():
    """MUST #35: FB path sidecar miss under strict → RuntimeError."""
    import pytest
    from reference_evaluator import _resolve_action_history_for_record
    record = {'situation_id': 'FB-UNKNOWN'}
    prior = os.environ.get('STAGE4_STRICT_ACTION_HISTORY')
    os.environ['STAGE4_STRICT_ACTION_HISTORY'] = 'raise'
    try:
        with pytest.raises(
            RuntimeError,
            match='MUST #35.*sidecar entry missing.*reference fixture',
        ):
            _resolve_action_history_for_record('FB-UNKNOWN', record)
    finally:
        if prior is None:
            os.environ.pop('STAGE4_STRICT_ACTION_HISTORY', None)
        else:
            os.environ['STAGE4_STRICT_ACTION_HISTORY'] = prior


# =============================================================================
# Integration: _build_fb_hand_dict + hand_dict in _evaluate_one_hand
# =============================================================================

def test_fb_hand_dict_has_action_history_when_record_populated():
    """MUST #22 integration: _build_fb_hand_dict plumbs _action_history
    into the hand dict. Verifies field presence + correct value."""
    from reference_evaluator import _build_fb_hand_dict
    # Build minimal FB-style record with action_history field
    record = {
        'situation_id': 'FB-01',  # real ref_id, present in _FB_ACTION_HISTORY
        'hero_cards': '7s6s',
        'board': 'Ah6d2c',
        'hero_pos': 'BB',
        'villain_positions': ['CO'],
        'pot': 90.0,
        'to_call': 30.0,
        'street': 'f',
        'facing_bet': True,
        'action_history': [
            ['preflop', 'CO', 'RAISE'],
            ['preflop', 'BTN', 'CALL'],
            ['preflop', 'BB', 'CALL'],
            ['flop', 'CO', 'BET'],
            ['flop', 'BTN', 'FOLD'],
        ],
    }
    hand_dict = _build_fb_hand_dict(record)
    assert '_action_history' in hand_dict
    assert hand_dict['_action_history'] == [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ]


def test_fb_hand_dict_empty_action_history_when_sidecar_miss():
    """MUST #22: FB record without action_history + sidecar miss +
    unset env → _action_history present as empty list. Stage 4 strict
    gate in extract_range_composition is the downstream raiser."""
    from reference_evaluator import _build_fb_hand_dict
    record = {
        'situation_id': 'FB-UNKNOWN',
        'hero_cards': '7s6s',
        'board': 'Ah6d2c',
        'hero_pos': 'BB',
        'villain_positions': ['CO'],
        'pot': 90.0,
        'to_call': 30.0,
        'street': 'f',
        'facing_bet': True,
    }
    prior = os.environ.get('STAGE4_STRICT_ACTION_HISTORY')
    os.environ.pop('STAGE4_STRICT_ACTION_HISTORY', None)
    try:
        hand_dict = _build_fb_hand_dict(record)
        assert hand_dict['_action_history'] == []
    finally:
        if prior is not None:
            os.environ['STAGE4_STRICT_ACTION_HISTORY'] = prior


if __name__ == '__main__':
    import subprocess
    rc = subprocess.call([sys.executable, '-m', 'pytest', '-xvs', __file__])
    sys.exit(rc)
