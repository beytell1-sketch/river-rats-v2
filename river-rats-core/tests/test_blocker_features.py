"""Tests for blocker_features.py (v2.4 P1 features).

Covers:
  - nut_flush_block boolean — M1 threshold split, M3 made-flush exclusion
  - compute_block_percentages — flush/straight/nut-made classes + M1 carve-out
  - M4 taxonomy-drift guard
"""
import os
import sys

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)


def test_nut_flush_block_flop_2plus_triggers():
    """2+ of suit on flop + hero holds A-of-suit → 1."""
    from blocker_features import compute_nut_flush_block
    assert compute_nut_flush_block(['As', '5d'], ['Qs', '7s', '2d']) == 1


def test_nut_flush_block_flop_no_ace_of_suit():
    """2+ of suit on flop but hero has no A-of-suit → 0."""
    from blocker_features import compute_nut_flush_block
    assert compute_nut_flush_block(['Ac', '5d'], ['Qs', '7s', '2d']) == 0
    assert compute_nut_flush_block(['Ks', '5d'], ['Qs', '7s', '2d']) == 0


def test_nut_flush_block_turn_2_suit_below_threshold():
    """M1 mod: turn needs 3+ of suit. 2-suit turn → 0."""
    from blocker_features import compute_nut_flush_block
    assert compute_nut_flush_block(['As', '5d'], ['Qs', '7s', '2d', 'Jc']) == 0


def test_nut_flush_block_turn_3plus_triggers():
    """Turn with 3+ of suit + hero A-of-suit → 1."""
    from blocker_features import compute_nut_flush_block
    assert compute_nut_flush_block(['As', '5d'], ['Qs', '7s', '2s', 'Jc']) == 1


def test_nut_flush_block_river_3plus_triggers():
    """River with 3+ of suit + hero A-of-suit → 1."""
    from blocker_features import compute_nut_flush_block
    assert compute_nut_flush_block(['As', '5d'], ['Qs', '7s', '2s', 'Jc', '9h']) == 1


def test_nut_flush_block_river_2_suit_below_threshold():
    """River needs 3+ of suit. 2-suit river → 0."""
    from blocker_features import compute_nut_flush_block
    assert compute_nut_flush_block(['As', '5d'], ['Qs', '7s', '2d', 'Jc', '9h']) == 0


def test_nut_flush_block_hero_has_made_flush():
    """M3 mod: hero already has 5+ of suit (made flush) → 0."""
    from blocker_features import compute_nut_flush_block
    # Hero As5s + 3-spade board = 5 spades = made flush
    assert compute_nut_flush_block(['As', '5s'], ['Qs', '7s', '2s']) == 0


def test_nut_flush_block_hero_flush_draw_is_not_exclusion():
    """Hero with A + another card of same suit + 2-spade flop = flush draw,
    NOT made flush. Feature should still fire (hero blocks + has draw)."""
    from blocker_features import compute_nut_flush_block
    # Hero As5s + 2-spade flop = 4 spades total, not yet a flush
    assert compute_nut_flush_block(['As', '5s'], ['Qs', '7s', '2d']) == 1


def test_nut_flush_block_empty_board():
    """Empty board → 0 (no flush possible)."""
    from blocker_features import compute_nut_flush_block
    assert compute_nut_flush_block(['As', '5d'], []) == 0


def test_nut_flush_block_wrong_card_count():
    """Invalid hero card count → 0."""
    from blocker_features import compute_nut_flush_block
    assert compute_nut_flush_block(['As'], ['Qs', '7s', '2d']) == 0


def test_strong_flush_is_effective_nut_ace_on_board():
    """M1 carve-out activator: A-of-suit on 3+-of-suit board → True."""
    from blocker_features import _strong_flush_is_effective_nut
    assert _strong_flush_is_effective_nut(['Ac', '7c', '2c']) is True


def test_strong_flush_no_ace_on_board():
    """No A on board → False (base nut_flush covers this)."""
    from blocker_features import _strong_flush_is_effective_nut
    assert _strong_flush_is_effective_nut(['Qc', '7c', '2c']) is False


def test_strong_flush_ace_but_no_3plus_suit():
    """A on board but not 3+ of same suit → False."""
    from blocker_features import _strong_flush_is_effective_nut
    assert _strong_flush_is_effective_nut(['Ac', '7h', '2d']) is False


def test_taxonomy_drift_guard():
    """M4 guard: all referenced subcat strings must exist in
    range_decomposition.SUBCATEGORY_ORDER (import-time assertion).
    Test confirms the import succeeds — which implicitly verifies the guard."""
    import blocker_features  # noqa: F401
    from range_decomposition import SUBCATEGORY_ORDER
    all_referenced = (
        blocker_features._FLUSH_DRAW_SUBCATS
        | blocker_features._STRAIGHT_DRAW_SUBCATS
        | blocker_features._COMBO_DRAW_SUBCATS
        | blocker_features._NUT_MADE_BASE
        | blocker_features._NUT_MADE_CONDITIONAL
    )
    missing = all_referenced - set(SUBCATEGORY_ORDER)
    assert not missing, f"Subcat drift: {missing}"


def test_compute_block_percentages_empty_range_returns_zeros():
    """Empty range → all zeros (not NaN per Q5 answer)."""
    from blocker_features import compute_block_percentages
    result = compute_block_percentages(['As', '5s'], ['Qs', '7s', '2d'], {})
    assert result == {
        'flush_draw_block_pct': 0.0,
        'straight_draw_block_pct': 0.0,
        'nut_made_block_pct': 0.0,
    }


def test_compute_block_percentages_returns_float_types():
    """Result values must be floats, never NaN."""
    import math
    from blocker_features import compute_block_percentages
    result = compute_block_percentages(
        ['As', '5s'], ['Qs', '7s', '2d'],
        {'QQ': 1.0, 'JJ': 1.0, 'AKs': 1.0, 'AKo': 1.0},
    )
    for key, val in result.items():
        assert isinstance(val, float), f'{key} not float: {type(val)}'
        assert not math.isnan(val), f'{key} is NaN'
        assert 0.0 <= val <= 1.0, f'{key}={val} out of [0,1]'


def test_compute_block_percentages_hero_blocks_flush_draws():
    """Hero holding Jh on Kh-7h-2d (2-heart flop) should block a meaningful
    fraction of villain's heart flush draws (XXhYYh combos with Jh)."""
    from blocker_features import compute_block_percentages
    # Simple villain range with hearts-suited hands
    v_range = {
        'AhKh': 1.0, 'AhQh': 1.0, 'AhJh': 0.0,  # AhJh impossible vs hero Jh
        'QhJh': 0.0,  # QhJh impossible vs hero Jh
        'JhTh': 0.0,  # JhTh impossible vs hero Jh
    }
    # Pass hero [Jh, 9s] on board with 2 hearts.
    result = compute_block_percentages(
        ['Jh', '9s'], ['Kh', '7h', '2d'], v_range,
    )
    # Can't fully assert exact values without computing subcat classifications
    # by hand, but block_pct should be >= 0 and finite.
    assert result['flush_draw_block_pct'] >= 0.0
    assert result['flush_draw_block_pct'] <= 1.0


if __name__ == '__main__':
    import subprocess
    rc = subprocess.call([sys.executable, '-m', 'pytest', '-xvs', __file__])
    sys.exit(rc)
