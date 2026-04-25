"""Stage 3.5 commit 14 — Finding B fold-in: multiway per-villain field
promotion in `extract_range_composition` (specifically in
`extract_all_features`'s Step 10b).

Cross-stream: this commit unblocks teaching HOLD #5 (C5.2 fixture
swap for F3/F4 multiway sentinels) and game per-villain range bars.

MUST #46 — per-villain field promotion contract:
  features['_per_villain_folded']: Dict[str, bool]      — non-empty on MW only
  features['_per_villain_composition']: Dict[str, Dict[str, float]] — non-empty on MW only
  features['_per_villain_overflowed']: Dict[str, bool]  — non-empty on MW only
  HU hands: all three keys present as empty dicts (NOT missing) so
  consumers don't NoneType-error.

Per the orchestrator's commit 14 spec at
MAIN_TERMINAL_PR_6_MERGED_COMMIT14_GREENLIGHT_2026-04-26.md.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from feature_extractor import extract_all_features


def _make_hand(**overrides):
    """Build a valid test hand dict (mirrors test_multiway_features pattern)."""
    base = {
        'h': 'AhKd', 'b': 'Ks7h2d', 'pos': 'BTN', 'vp': 'BB',
        'pot': 10.0, 'tc': 5.0, 'st': 'f', 'fb': 1, 'exp': 'C',
    }
    base.update(overrides)
    return base


def test_must46_per_villain_folded_promoted_in_multiway():
    """Multiway hand (3-way) populates `_per_villain_folded` as a
    Dict[str, bool] keyed by opponent position. Each value is the
    folded-status from the chain meta for that opponent."""
    hand = _make_hand(_num_opponents=3)
    features = extract_all_features(hand)
    pvf = features['_per_villain_folded']
    assert isinstance(pvf, dict), (
        f'_per_villain_folded must be dict, got {type(pvf).__name__}'
    )
    assert pvf, '_per_villain_folded must be non-empty on MW (3-way) hand'
    # Each value is a bool
    for opp_pos, is_folded in pvf.items():
        assert isinstance(opp_pos, str), f'opp_pos must be str, got {opp_pos!r}'
        assert isinstance(is_folded, bool), (
            f'_per_villain_folded[{opp_pos!r}] must be bool, got {is_folded!r}'
        )
    # No action_history → no folds expected
    assert not any(pvf.values()), (
        f'No action_history → no opponent should be folded; got {pvf!r}'
    )


def test_must46_per_villain_composition_promoted_in_multiway():
    """Multiway hand populates `_per_villain_composition` as a
    Dict[str, Dict[str, float]] keyed by opponent position. Each
    composition has keys {tp_plus, medium, draw, air} that sum to
    ≈1.0 when the opponent's range is non-empty (and not folded /
    overflowed)."""
    hand = _make_hand(_num_opponents=3)
    features = extract_all_features(hand)
    pvc = features['_per_villain_composition']
    assert isinstance(pvc, dict), (
        f'_per_villain_composition must be dict, got {type(pvc).__name__}'
    )
    assert pvc, '_per_villain_composition must be non-empty on MW (3-way) hand'
    for opp_pos, comp in pvc.items():
        assert isinstance(comp, dict), (
            f'_per_villain_composition[{opp_pos!r}] must be dict, got {comp!r}'
        )
        # Triple-key contract per spec (4 keys: tp_plus, medium, draw, air)
        for key in ('tp_plus', 'medium', 'draw', 'air'):
            assert key in comp, (
                f'_per_villain_composition[{opp_pos!r}] missing key {key!r}: '
                f'got {sorted(comp.keys())}'
            )
            assert isinstance(comp[key], (int, float)), (
                f'_per_villain_composition[{opp_pos!r}][{key!r}] must be numeric, '
                f'got {comp[key]!r}'
            )
        # Sums to ≈1.0 when non-empty (allow small rounding tolerance from
        # round(_, 4) per category; 4 categories × 4 decimal rounding =
        # ≤ 4e-4 cumulative drift).
        total = sum(comp.values())
        assert 0.99 <= total <= 1.0001, (
            f'_per_villain_composition[{opp_pos!r}] sum {total} not in '
            f'[0.99, 1.0001]; values={comp!r}'
        )


def test_must46_per_villain_overflowed_promoted_in_multiway():
    """Multiway hand populates `_per_villain_overflowed` as a
    Dict[str, bool] keyed by opponent position. Each value is the
    chain-overflowed status from the chain meta for that opponent."""
    hand = _make_hand(_num_opponents=3)
    features = extract_all_features(hand)
    pvo = features['_per_villain_overflowed']
    assert isinstance(pvo, dict), (
        f'_per_villain_overflowed must be dict, got {type(pvo).__name__}'
    )
    assert pvo, '_per_villain_overflowed must be non-empty on MW (3-way) hand'
    for opp_pos, is_overflowed in pvo.items():
        assert isinstance(opp_pos, str), f'opp_pos must be str, got {opp_pos!r}'
        assert isinstance(is_overflowed, bool), (
            f'_per_villain_overflowed[{opp_pos!r}] must be bool, got {is_overflowed!r}'
        )
    # No action_history → no overflow expected
    assert not any(pvo.values()), (
        f'No action_history → no opponent should be overflowed; got {pvo!r}'
    )


def test_must46_per_villain_empty_dict_in_HU():
    """Regression: HU hands (num_opponents == 1) produce EMPTY DICTS
    for the three new `_per_villain_*` keys (NOT missing keys, NOT
    None). Consumers can `len(features['_per_villain_folded'])` and
    `for opp in features['_per_villain_composition']` without
    NoneType-erroring on HU rows."""
    hand_hu = _make_hand(_num_opponents=1)
    features = extract_all_features(hand_hu)
    for key in ('_per_villain_folded', '_per_villain_composition',
                '_per_villain_overflowed'):
        assert key in features, (
            f'HU features dict missing required key {key!r}; '
            f'consumers expect dict not absent'
        )
        assert features[key] == {}, (
            f'HU {key!r} must be empty dict (got {features[key]!r}); '
            f'NOT missing, NOT None — consumers iterate / index into it'
        )
        assert isinstance(features[key], dict), (
            f'HU {key!r} must be dict type (got {type(features[key]).__name__})'
        )

    # Also verify default (no _num_opponents specified) behaves as HU.
    hand_default = _make_hand()
    features_default = extract_all_features(hand_default)
    for key in ('_per_villain_folded', '_per_villain_composition',
                '_per_villain_overflowed'):
        assert features_default[key] == {}, (
            f'Default-num_opponents (HU) {key!r} must be empty dict; '
            f'got {features_default[key]!r}'
        )
