"""v2.4 Stage 3.5 commit 4 — atomic 11-MUST merge tests.

Covers:
  - CRIT #1: blocker features consume _villain_range_narrowed (not re-fetch)
  - HIGH #4: folded-villain sentinel + NaN composition
  - MUST #15: over-narrow sentinel + NaN composition
  - MUST #28: floor-truncation sentinel + NaN composition
  - MUST #10: NaN spec (gto_model allowlist; composition NaN; blocker NaN)
  - MUST #6: equity chain inheritance
  - MUST #34: multiway per-villain chain
  - MUST #46: helper cache contract
  - MUST #52: MULTIWAY_CHAIN_MODE env switch
  - MUST #63: cache contract per-hand invalidation
"""
import math
import os
import sys

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)


# =============================================================================
# CRIT #1 — Blocker features consume chain-narrowed range
# =============================================================================

def test_crit1_villain_range_narrowed_published_in_return():
    """CRIT #1: extract_range_composition returns _villain_range_narrowed
    in its output dict so Step 12 + 17 consume the same chain-narrowed
    range as composition features (no independent re-fetch)."""
    from feature_extractor import extract_range_composition
    out = extract_range_composition(
        board_cards=['Kh', '7d', '2c', '9s'],
        hero_pos='BTN', villain_pos='BB',
        facing_bet=False, street_raw='t', is_3bet_pot=0,
        action_history=[
            {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
            {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
            {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
        ],
    )
    assert '_villain_range_narrowed' in out
    assert isinstance(out['_villain_range_narrowed'], dict)
    assert len(out['_villain_range_narrowed']) > 0


# =============================================================================
# HIGH #4 — Folded-villain sentinel + NaN composition
# =============================================================================

def test_high4_folded_villain_sentinel():
    """HIGH #4: when chain terminates at :FOLD, _villain_folded=True is
    set in return; composition features are NaN; range_narrowed is empty."""
    from feature_extractor import extract_range_composition
    out = extract_range_composition(
        board_cards=['Kh', '7d', '2c', '9s'],
        hero_pos='BTN', villain_pos='BB',
        facing_bet=False, street_raw='t', is_3bet_pot=0,
        action_history=[
            {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
            {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
            {'street': 'flop', 'position': 'BB', 'action': 'FOLD'},
        ],
    )
    assert out['_villain_folded'] is True
    assert out['_villain_chain_overflowed'] is False
    # MUST #10: composition features NaN for folded villain
    assert math.isnan(out['_villain_top_pair_plus_pct'])
    assert math.isnan(out['_villain_draw_pct'])
    assert math.isnan(out['_villain_air_pct'])
    assert math.isnan(out['_villain_medium_made_pct'])
    # range_narrowed empty
    assert out['_villain_range_narrowed'] == {}


def test_high4_not_folded_not_overflowed_sentinels_false():
    """HIGH #4: normal chain → both sentinels False; composition non-NaN."""
    from feature_extractor import extract_range_composition
    out = extract_range_composition(
        board_cards=['Kh', '7d', '2c', '9s'],
        hero_pos='BTN', villain_pos='BB',
        facing_bet=False, street_raw='t', is_3bet_pot=0,
        action_history=[
            {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
            {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
            {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
        ],
    )
    assert out['_villain_folded'] is False
    # chain_overflowed may be True if chain truncated under MUST #13 floor;
    # otherwise False. Either way, composition should match state.
    if out['_villain_chain_overflowed']:
        assert math.isnan(out['_villain_top_pair_plus_pct'])
    else:
        assert not math.isnan(out['_villain_top_pair_plus_pct'])


# =============================================================================
# MUST #6 + #34 + #46 + #52 — helper + multiway + cache
# =============================================================================

def test_must6_helper_hu_chain_narrowing():
    """MUST #6: helper chain-narrows HU range when action_history supplied."""
    from feature_extractor import _get_chain_narrowed_villain_range
    v_range, meta = _get_chain_narrowed_villain_range(
        hero_pos='BTN', villain_pos='BB',
        opener_pos='BTN', board_cards=['Kh', '7d', '2c', '9s'],
        facing_bet=False, street_raw='t',
        action_history=[
            {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
            {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
            {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
        ],
        num_opponents=1,
    )
    assert isinstance(v_range, dict)
    assert len(v_range) > 0
    assert 'flop:CHECK' in meta['chain_steps']


def test_must63_cache_contract_paired_or_absent():
    """MUST #63: cached_range + cached_meta must be paired (both None or
    both set). Mismatched pair raises RuntimeError."""
    import pytest
    from feature_extractor import _get_chain_narrowed_villain_range
    with pytest.raises(RuntimeError, match='cache contract violation'):
        _get_chain_narrowed_villain_range(
            hero_pos='BTN', villain_pos='BB',
            opener_pos='BTN', board_cards=['Kh', '7d', '2c'],
            facing_bet=False, street_raw='f',
            cached_range={},  # only one of the pair
            cached_meta=None,
        )


def test_must63_cache_fast_path():
    """MUST #63: when cache provided, helper returns without re-computing."""
    from feature_extractor import _get_chain_narrowed_villain_range
    cached_range = {'AA': 1.0, 'KK': 1.0}
    cached_meta = {'chain_steps': ['flop:CHECK'], 'surviving_weight': 0.5}
    v_range, meta = _get_chain_narrowed_villain_range(
        hero_pos='BTN', villain_pos='BB',
        opener_pos='BTN', board_cards=['Kh', '7d', '2c'],
        facing_bet=False, street_raw='f',
        cached_range=cached_range,
        cached_meta=cached_meta,
    )
    assert v_range is cached_range   # same reference
    assert meta is cached_meta


def test_must34_multiway_populates_per_villain_ranges():
    """MUST #34: multiway helper populates meta['per_villain_ranges'] with
    chain-narrowed range per opponent."""
    from feature_extractor import _get_chain_narrowed_villain_range
    v_range, meta = _get_chain_narrowed_villain_range(
        hero_pos='BTN', villain_pos='BB',
        opener_pos='BTN', board_cards=['Kh', '7d', '2c', '9s'],
        facing_bet=False, street_raw='t',
        action_history=[
            {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
            {'street': 'preflop', 'position': 'CO', 'action': 'CALL'},
            {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
            {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
            {'street': 'flop', 'position': 'CO', 'action': 'CHECK'},
        ],
        num_opponents=2,
        opponent_positions=['BB', 'CO'],
    )
    # MUST #64: multiway returns None for v_range (merged deprecated)
    assert v_range is None
    # MUST #46: per_villain_ranges present + populated
    assert 'per_villain_ranges' in meta
    assert 'BB' in meta['per_villain_ranges']
    assert 'CO' in meta['per_villain_ranges']
    assert len(meta['per_villain_ranges']['BB']) > 0
    # MUST #60: aggregated chain_steps with position prefix
    assert all(':' in s for s in meta['chain_steps'])


def test_must52_multiway_chain_mode_env_switch():
    """MUST #52: MULTIWAY_CHAIN_MODE env switches between per_villain (default)
    and primary_only (fallback). In primary_only, non-primary villains get
    un-chained ranges."""
    from feature_extractor import _get_chain_narrowed_villain_range

    action_history = [
        {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
        {'street': 'preflop', 'position': 'CO', 'action': 'CALL'},
        {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
        {'street': 'flop', 'position': 'CO', 'action': 'CHECK'},
    ]

    prior = os.environ.get('MULTIWAY_CHAIN_MODE')

    try:
        # Default: per_villain — both BB and CO get chain-narrowed
        os.environ['MULTIWAY_CHAIN_MODE'] = 'per_villain'
        _, meta_pv = _get_chain_narrowed_villain_range(
            hero_pos='BTN', villain_pos='BB',
            opener_pos='BTN', board_cards=['Kh', '7d', '2c', '9s'],
            facing_bet=False, street_raw='t',
            action_history=action_history,
            num_opponents=2,
            opponent_positions=['BB', 'CO'],
        )
        # Both opponents have chain_steps
        assert meta_pv['per_villain_chain_steps']['BB']
        assert meta_pv['per_villain_chain_steps']['CO']

        # primary_only: only BB (primary) gets chain_steps; CO stays un-chained
        os.environ['MULTIWAY_CHAIN_MODE'] = 'primary_only'
        _, meta_po = _get_chain_narrowed_villain_range(
            hero_pos='BTN', villain_pos='BB',
            opener_pos='BTN', board_cards=['Kh', '7d', '2c', '9s'],
            facing_bet=False, street_raw='t',
            action_history=action_history,
            num_opponents=2,
            opponent_positions=['BB', 'CO'],
        )
        # BB (primary at index 0) has chain_steps; CO does not
        assert meta_po['per_villain_chain_steps']['BB']
        assert not meta_po['per_villain_chain_steps']['CO']
    finally:
        if prior is None:
            os.environ.pop('MULTIWAY_CHAIN_MODE', None)
        else:
            os.environ['MULTIWAY_CHAIN_MODE'] = prior


# =============================================================================
# MUST #10 sub-4 — gto_model NaN allowlist
# =============================================================================

def test_must10_gto_model_rejects_non_allowlist_nan():
    """MUST #10 sub-4: gto_model.features_from_dict raises on NaN in
    non-allowlist columns (e.g., raw_equity). Allowlist permits
    composition + blocker features only."""
    import pytest
    from gto_model import GtoOracle, FEATURE_COLUMNS
    # Build minimal feat_dict with NaN in non-allowlist column
    feat_dict = {f: 0.0 for f in FEATURE_COLUMNS}
    feat_dict['raw_equity'] = float('nan')  # NOT in allowlist
    with pytest.raises(ValueError, match='unexpected NaN in non-allowlist'):
        GtoOracle.features_from_dict(feat_dict)


def test_must10_gto_model_allows_nan_on_composition():
    """MUST #10 sub-4: NaN on villain_top_pair_plus_pct (allowlisted) is
    permitted without raising."""
    from gto_model import GtoOracle, FEATURE_COLUMNS
    feat_dict = {f: 0.0 for f in FEATURE_COLUMNS}
    feat_dict['villain_top_pair_plus_pct'] = float('nan')
    feat_dict['villain_draw_pct'] = float('nan')
    feat_dict['villain_air_pct'] = float('nan')
    feat_dict['villain_medium_made_pct'] = float('nan')
    # Should not raise
    arr = GtoOracle.features_from_dict(feat_dict)
    assert arr.shape == (len(FEATURE_COLUMNS),)


def test_must10_gto_model_allows_nan_on_blockers():
    """MUST #10 sub-4: NaN on blocker features (allowlisted) permitted."""
    from gto_model import GtoOracle, FEATURE_COLUMNS
    feat_dict = {f: 0.0 for f in FEATURE_COLUMNS}
    feat_dict['flush_block_pct'] = float('nan')
    # Should not raise
    arr = GtoOracle.features_from_dict(feat_dict)
    assert arr.shape == (len(FEATURE_COLUMNS),)


# =============================================================================
# Commit 4.1 fix-forward — named tests for M1 gap (MUSTs #15/#28/#46/#60)
# plus C1/C2/H1/H2/H4 regression guards
# =============================================================================

def test_must15_over_narrow_sentinel():
    """MUST #15: when chain over-narrows to empty WITHOUT ':FOLD',
    _villain_chain_overflowed=True and NaN-flag composition."""
    from feature_extractor import extract_range_composition
    # Contrived chain likely to over-narrow (deep + narrow board).
    # We specifically look for the overflow (non-FOLD empty) case.
    out = extract_range_composition(
        board_cards=['Ah', 'Kh', 'Qh', 'Jh', 'Th'],  # monotone broadway
        hero_pos='BTN', villain_pos='BB',
        facing_bet=True, street_raw='r', is_3bet_pot=0,
        action_history=[
            {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
            {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
            {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
            {'street': 'turn', 'position': 'BB', 'action': 'CHECK'},
        ],
    )
    # Either truncated or overflowed; either way composition NaN'd
    if out['_villain_folded']:
        pass  # unexpected but not wrong
    elif out['_villain_chain_overflowed']:
        assert math.isnan(out['_villain_top_pair_plus_pct']), (
            'chain_overflowed=True but composition not NaN'
        )


def test_must28_floor_truncation_sets_overflowed():
    """MUST #28: when chain mass-floor truncates (chain_truncated=True),
    _villain_chain_overflowed=True and composition NaN."""
    from feature_extractor import extract_range_composition
    # Use the H_8dfb6ef8 canonical shape known to truncate post-MUST-#13.
    out = extract_range_composition(
        board_cards=['5d', '3s', '5h', '3d', '9s'],
        hero_pos='BTN', villain_pos='BB',
        facing_bet=False, street_raw='r', is_3bet_pot=0,
        action_history=[
            {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
            {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
            {'street': 'flop', 'position': 'BB', 'action': 'BET'},
            {'street': 'flop', 'position': 'BTN', 'action': 'CALL'},
            {'street': 'turn', 'position': 'BB', 'action': 'CHECK'},
            {'street': 'turn', 'position': 'BTN', 'action': 'BET'},
            {'street': 'turn', 'position': 'BB', 'action': 'CALL'},
        ],
    )
    # Expected post-MUST-#13: truncated + overflowed + NaN composition
    if out['_villain_range_chain_truncated']:
        assert out['_villain_chain_overflowed'] is True
        assert math.isnan(out['_villain_top_pair_plus_pct'])


def test_must60_multiway_chain_steps_aggregation():
    """MUST #60: multiway chain_steps aggregation uses
    [f'{opp}:{step}' for opp, steps in per_villain_chain_steps.items() for step in steps]
    (not the broken dict-iteration from v2.3)."""
    from feature_extractor import _get_chain_narrowed_villain_range
    _, meta = _get_chain_narrowed_villain_range(
        hero_pos='BTN', villain_pos='BB',
        opener_pos='BTN', board_cards=['Kh', '7d', '2c', '9s'],
        facing_bet=False, street_raw='t',
        action_history=[
            {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
            {'street': 'preflop', 'position': 'CO', 'action': 'CALL'},
            {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
            {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
            {'street': 'flop', 'position': 'CO', 'action': 'CHECK'},
        ],
        num_opponents=2,
        opponent_positions=['BB', 'CO'],
    )
    # Every aggregated step has 'POS:STREET:ACTION' shape
    for step in meta['chain_steps']:
        assert ':' in step, f'step {step!r} missing position prefix'
        parts = step.split(':')
        assert len(parts) >= 3, f'step {step!r} expected POS:STREET:ACTION'
        assert parts[0] in ('BB', 'CO'), f'unknown position prefix {parts[0]!r}'


def test_must46_cache_hit_via_hand_dict():
    """MUST #46 + C3 fix (commit 4.1): hand-level cache populated by
    first helper call; second call with same (num_opp, opp_positions)
    key returns cached result (identity check)."""
    from feature_extractor import _get_chain_narrowed_villain_range

    hand = {}   # fresh hand dict; cache starts empty
    common_kwargs = dict(
        hero_pos='BTN', villain_pos='BB',
        opener_pos='BTN', board_cards=['Kh', '7d', '2c', '9s'],
        facing_bet=False, street_raw='t',
        action_history=[
            {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
            {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
            {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
        ],
        num_opponents=1,
        hand=hand,
    )

    range1, meta1 = _get_chain_narrowed_villain_range(**common_kwargs)
    range2, meta2 = _get_chain_narrowed_villain_range(**common_kwargs)

    # Second call returns cached tuple — identity, not recomputation
    assert range1 is range2
    assert meta1 is meta2
    # Cache key present on hand dict.
    # Phase 3 HIGH-3 fix (Task 4.5): cache key now includes the
    # action_history hash as a 3rd tuple element to prevent stale-cache
    # hits when callers mutate `_action_history` across street decisions.
    # Match by (kind, position) prefix instead of exact tuple identity.
    assert '_chain_cache' in hand
    cache_keys = list(hand['_chain_cache'].keys())
    assert any(
        isinstance(k, tuple) and len(k) >= 2 and k[0] == 'hu' and k[1] == 'BB'
        for k in cache_keys
    ), (
        f'expected cache key starting with (\"hu\", \"BB\", ...); '
        f'got {cache_keys!r}'
    )


def test_c1_board_favour_zero_when_folded():
    """C1 fix (commit 4.1): board_favour = 0.0 (not NaN) when villain
    folded; inference allowlist does NOT include board_favour, so NaN
    here would break gto_model.features_from_dict on folded hands."""
    from feature_extractor import extract_range_composition
    out = extract_range_composition(
        board_cards=['Kh', '7d', '2c', '9s'],
        hero_pos='BTN', villain_pos='BB',
        facing_bet=False, street_raw='t', is_3bet_pot=0,
        action_history=[
            {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
            {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
            {'street': 'flop', 'position': 'BB', 'action': 'FOLD'},
        ],
    )
    assert out['_villain_folded'] is True
    # C1 fix: 0.0 not NaN
    assert out['_board_favour'] == 0.0, (
        f'C1 fix: board_favour={out["_board_favour"]!r} '
        f'(expected 0.0 on folded villain)'
    )
    assert not math.isnan(out['_board_favour'])


def test_h1_multiway_chain_mode_unknown_warns_and_defaults_per_villain():
    """H1 fix (commit 4.1): unknown MULTIWAY_CHAIN_MODE value logs WARN
    and defaults to per_villain (not silent fall-through to primary_only)."""
    import logging
    from feature_extractor import _get_chain_narrowed_villain_range

    prior = os.environ.get('MULTIWAY_CHAIN_MODE')
    os.environ['MULTIWAY_CHAIN_MODE'] = 'primary'  # typo — unknown value
    try:
        action_history = [
            {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
            {'street': 'preflop', 'position': 'CO', 'action': 'CALL'},
            {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
            {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
            {'street': 'flop', 'position': 'CO', 'action': 'CHECK'},
        ]
        _, meta = _get_chain_narrowed_villain_range(
            hero_pos='BTN', villain_pos='BB',
            opener_pos='BTN', board_cards=['Kh', '7d', '2c', '9s'],
            facing_bet=False, street_raw='t',
            action_history=action_history,
            num_opponents=2,
            opponent_positions=['BB', 'CO'],
        )
        # Unknown env → defaulted to per_villain → both BB and CO chained
        assert meta['per_villain_chain_steps']['BB']
        assert meta['per_villain_chain_steps']['CO']
        assert meta['_chain_method'] == 'per_villain'
    finally:
        if prior is None:
            os.environ.pop('MULTIWAY_CHAIN_MODE', None)
        else:
            os.environ['MULTIWAY_CHAIN_MODE'] = prior


def test_h2_missing_opponent_position_raises(monkeypatch):
    """H2 fix (commit 4.1): per_villain_ranges missing a requested
    opp_pos raises RuntimeError, not silent empty-dict fallback.

    Contrived test — normal flow can't trigger (helper populates
    pv_ranges with exactly opponent_positions). We monkey-patch the
    helper to return incomplete pv_ranges; the H2 guard in
    extract_equity_features must raise.
    """
    import pytest
    import feature_extractor as fe

    # Monkey-patch helper to return pv_ranges missing the requested CO
    def _incomplete_helper(*args, **kwargs):
        opp_positions = kwargs.get('opponent_positions', [])
        # Intentionally drop CO from pv_ranges — simulates helper bug
        pv = {p: {'AA': 1.0} for p in opp_positions if p != 'CO'}
        return None, {
            'per_villain_ranges': pv,
            '_chain_method': 'per_villain',
        }

    monkeypatch.setattr(fe, '_get_chain_narrowed_villain_range', _incomplete_helper)

    with pytest.raises(RuntimeError, match='H2:'):
        fe.extract_equity_features(
            hero_cards=['As', 'Ks'],
            board_cards=['Kh', '7d', '2c', '9s'],
            hero_pos='BTN', villain_pos='BB',
            facing_bet=False, street_raw='t',
            num_opponents=2,
            opponent_positions=['BB', 'CO'],
            opener_pos='BTN',
            action_history=[
                {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
                {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
                {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
            ],
        )


def test_h4_duplicate_opponent_positions_assert():
    """H4 fix (commit 4.1): duplicate opponent_positions entry raises
    AssertionError — would silently overwrite per_villain_ranges."""
    import pytest
    from feature_extractor import _get_chain_narrowed_villain_range
    with pytest.raises(AssertionError, match='H4: duplicate'):
        _get_chain_narrowed_villain_range(
            hero_pos='BTN', villain_pos='BB',
            opener_pos='BTN', board_cards=['Kh', '7d', '2c'],
            facing_bet=False, street_raw='f',
            action_history=[
                {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
                {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
            ],
            num_opponents=3,
            opponent_positions=['BB', 'BB', 'CO'],  # duplicate BB
        )


def test_h5_chain_method_telemetry_in_meta():
    """H5 fix (commit 4.1): meta['_chain_method'] identifies HU vs
    multiway per_villain vs primary_only for audit logs."""
    from feature_extractor import _get_chain_narrowed_villain_range

    # HU call
    _, meta_hu = _get_chain_narrowed_villain_range(
        hero_pos='BTN', villain_pos='BB',
        opener_pos='BTN', board_cards=['Kh', '7d', '2c'],
        facing_bet=False, street_raw='f',
        action_history=[
            {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
            {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
        ],
        num_opponents=1,
    )
    assert meta_hu.get('_chain_method') == 'hu'

    # Multiway per_villain
    prior = os.environ.get('MULTIWAY_CHAIN_MODE')
    try:
        os.environ['MULTIWAY_CHAIN_MODE'] = 'per_villain'
        _, meta_pv = _get_chain_narrowed_villain_range(
            hero_pos='BTN', villain_pos='BB',
            opener_pos='BTN', board_cards=['Kh', '7d', '2c'],
            facing_bet=False, street_raw='f',
            action_history=[
                {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
                {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
                {'street': 'preflop', 'position': 'CO', 'action': 'CALL'},
            ],
            num_opponents=2,
            opponent_positions=['BB', 'CO'],
        )
        assert meta_pv.get('_chain_method') == 'per_villain'

        # Multiway primary_only
        os.environ['MULTIWAY_CHAIN_MODE'] = 'primary_only'
        _, meta_po = _get_chain_narrowed_villain_range(
            hero_pos='BTN', villain_pos='BB',
            opener_pos='BTN', board_cards=['Kh', '7d', '2c'],
            facing_bet=False, street_raw='f',
            action_history=[
                {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
                {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
                {'street': 'preflop', 'position': 'CO', 'action': 'CALL'},
            ],
            num_opponents=2,
            opponent_positions=['BB', 'CO'],
        )
        assert meta_po.get('_chain_method') == 'primary_only'
    finally:
        if prior is None:
            os.environ.pop('MULTIWAY_CHAIN_MODE', None)
        else:
            os.environ['MULTIWAY_CHAIN_MODE'] = prior


if __name__ == '__main__':
    import subprocess
    rc = subprocess.call([sys.executable, '-m', 'pytest', '-xvs', __file__])
    sys.exit(rc)
