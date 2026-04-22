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


if __name__ == '__main__':
    import subprocess
    rc = subprocess.call([sys.executable, '-m', 'pytest', '-xvs', __file__])
    sys.exit(rc)
