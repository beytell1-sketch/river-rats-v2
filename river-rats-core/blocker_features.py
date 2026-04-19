"""blocker_features.py — v2.4 P1 blocker-direction features.

4 new features per consolidated verdict + directive (spec locked
2026-04-19):

  - nut_flush_block             (bool)       — hero holds A of flush-possible suit
  - flush_draw_block_pct        (float 0-1)  — % of villain's flush-draw combos hero blocks
  - straight_draw_block_pct     (float 0-1)  — % of villain's straight-draw combos hero blocks
  - nut_made_block_pct          (float 0-1)  — % of villain's nut-made combos hero blocks

Design notes:
- `flush_block_pct` (feature 46) is NOT removed — retirement deferred
  per directive-x. These features ship alongside it; A/B + monotone
  sanity sweep gates the retirement decision.
- Per GTO reviewer: inline combo iteration here; do NOT modify
  range_decomposition.py. This module imports classifier helpers and
  runs its own loop.

Invariants:
- All 4 features return numeric types (int or float). No NaN.
- If board or range is empty, features return 0 / 0.0 defaults.
- nut_made_block_pct applies the strong_flush carve-out when A-of-suit
  is on the board AND 3+ of that suit appear on the board (per critical
  M1 mod from plan 3 GTO review).
"""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional

import eval7

from range_decomposition import _classify_combo_subcategory, SUBCATEGORY_ORDER


# =============================================================================
# Subcategory classes
# =============================================================================
# Flush-draw class — straight-flush draws not included (they're nut-made)
_FLUSH_DRAW_SUBCATS = {'nut_flush_draw', 'flush_draw'}

# Straight-draw class
_STRAIGHT_DRAW_SUBCATS = {'oesd', 'gutshot'}

# Combo draw = straight + flush draw simultaneously; counts in BOTH halves
_COMBO_DRAW_SUBCATS = {'combo_draw'}

# Nut-made BASE class (unconditional)
_NUT_MADE_BASE = {
    'straight_flush', 'quads', 'full_house',
    'nut_flush', 'nut_straight', 'top_set',
}

# Conditional addition when A-of-suit is on board with 3+ of suit
_NUT_MADE_CONDITIONAL = {'strong_flush'}


# =============================================================================
# Taxonomy-drift guard (M4 from plan 3 GTO review)
# =============================================================================
# Assert every subcat string we reference exists in range_decomposition's
# SUBCATEGORY_ORDER. Fails at import time if taxonomy renames.
_ALL_REFERENCED = (
    _FLUSH_DRAW_SUBCATS | _STRAIGHT_DRAW_SUBCATS | _COMBO_DRAW_SUBCATS
    | _NUT_MADE_BASE | _NUT_MADE_CONDITIONAL
)
_missing = _ALL_REFERENCED - set(SUBCATEGORY_ORDER)
if _missing:
    raise ImportError(
        f"blocker_features: subcat(s) {_missing} not in "
        f"range_decomposition.SUBCATEGORY_ORDER (taxonomy drifted)"
    )
del _missing, _ALL_REFERENCED


# =============================================================================
# Helpers
# =============================================================================
def _to_eval7_cards_local(cards: List[str]):
    """eval7 expects '2h' format. Pass through; eval7.Card handles it."""
    return [eval7.Card(c) for c in cards]


def _strong_flush_is_effective_nut(board_cards: List[str]) -> bool:
    """Per M1 plan-3 carve-out: when A-of-suit is on board AND there are
    3+ of that suit on board, the K-high flush (strong_flush) IS the
    effective nut and should count in the nut-made class.
    """
    if not board_cards:
        return False
    board_suits = [c[1].lower() for c in board_cards]
    suit_counts = defaultdict(int)
    for s in board_suits:
        suit_counts[s] += 1

    ace_suits_on_board = {
        c[1].lower() for c in board_cards if c[0].upper() == 'A'
    }
    for s in ace_suits_on_board:
        if suit_counts[s] >= 3:
            return True
    return False


# =============================================================================
# Feature 1: nut_flush_block (bool)
# =============================================================================
def compute_nut_flush_block(
    hero_cards: List[str],
    board_cards: List[str],
) -> int:
    """Return 1 if hero holds A-of-suit on a flush-possible board.

    Thresholds per plan-1 M1 mod:
      - Flop (3 board cards): 2+ of same suit qualifies
      - Turn/River (4-5):     3+ of same suit qualifies

    Made-flush exclusion per plan-1 M3 mod: if hero + board together
    have 5+ of the suit, hero has a made flush, not a blocker
    situation. Return 0.
    """
    if not board_cards or len(hero_cards) != 2:
        return 0

    n_board = len(board_cards)
    threshold = 2 if n_board == 3 else 3

    board_suit_counts = defaultdict(int)
    for c in board_cards:
        board_suit_counts[c[1].lower()] += 1

    flush_suits = {s for s, n in board_suit_counts.items() if n >= threshold}
    if not flush_suits:
        return 0

    hero_suit_counts = defaultdict(int)
    for c in hero_cards:
        hero_suit_counts[c[1].lower()] += 1

    # Made-flush exclusion (M3): hero + board total of any flush suit >= 5
    for s in flush_suits:
        if board_suit_counts[s] + hero_suit_counts[s] >= 5:
            return 0

    # Does hero hold A of any flush-possible suit?
    for c in hero_cards:
        if c[0].upper() == 'A' and c[1].lower() in flush_suits:
            return 1
    return 0


# =============================================================================
# Features 2-4: block percentages via combo iteration
# =============================================================================
def compute_block_percentages(
    hero_cards: List[str],
    board_cards: List[str],
    villain_range: Dict[str, float],
) -> Dict[str, float]:
    """Compute flush_draw_block_pct, straight_draw_block_pct,
    nut_made_block_pct in one pass over villain's range.

    Per reviewer guidance: inline combo iteration; do NOT modify
    range_decomposition.py. Uses imported `_classify_combo_subcategory`.

    Args:
        hero_cards: ['Jh', '9h']
        board_cards: ['Kh', '7h', '2d', 'Th', '3s']
        villain_range: {hand_notation: frequency}

    Returns:
        dict with 3 float keys — 0.0 (not NaN) when class is empty.
    """
    defaults = {
        'flush_draw_block_pct': 0.0,
        'straight_draw_block_pct': 0.0,
        'nut_made_block_pct': 0.0,
    }
    if not board_cards or len(hero_cards) != 2 or not villain_range:
        return defaults

    # Lazy import to avoid circular dependency
    from feature_extractor import get_valid_combos

    # Determine which nut-made subcats apply (conditional strong_flush)
    nut_made_subcats = set(_NUT_MADE_BASE)
    if _strong_flush_is_effective_nut(board_cards):
        nut_made_subcats |= _NUT_MADE_CONDITIONAL

    hero_set_lower = {c.lower() for c in hero_cards}

    # We need combos that respect BOARD but NOT hero's cards — because
    # we're measuring hero's blocking effect. If we excluded hero's
    # cards from combos, blocking would always be zero.
    board_only_used = {c.lower() for c in board_cards}

    # Pre-compute board eval7 cards (for combo value evaluation)
    try:
        board_eval7 = _to_eval7_cards_local(board_cards)
    except Exception:
        return defaults

    # Totals + blocked counts (weighted by range frequency)
    fd_total = fd_blocked = 0.0
    sd_total = sd_blocked = 0.0
    nm_total = nm_blocked = 0.0

    for hand_notation, freq in villain_range.items():
        if freq <= 0:
            continue
        try:
            combos = get_valid_combos(hand_notation, board_only_used)
        except Exception:
            continue

        for combo in combos:
            try:
                v_eval7 = _to_eval7_cards_local(combo)
                v_value = eval7.evaluate(v_eval7 + board_eval7)
                subcat = _classify_combo_subcategory(
                    combo, board_cards, v_value,
                )
            except Exception:
                continue

            combo_lower = {c.lower() for c in combo}
            hero_blocks = bool(combo_lower & hero_set_lower)

            # Flush-draw class (includes combo_draw)
            if subcat in _FLUSH_DRAW_SUBCATS or subcat in _COMBO_DRAW_SUBCATS:
                fd_total += freq
                if hero_blocks:
                    fd_blocked += freq

            # Straight-draw class (includes combo_draw)
            if subcat in _STRAIGHT_DRAW_SUBCATS or subcat in _COMBO_DRAW_SUBCATS:
                sd_total += freq
                if hero_blocks:
                    sd_blocked += freq

            # Nut-made class (with conditional strong_flush)
            if subcat in nut_made_subcats:
                nm_total += freq
                if hero_blocks:
                    nm_blocked += freq

    return {
        'flush_draw_block_pct': (
            round(fd_blocked / fd_total, 6) if fd_total > 0 else 0.0
        ),
        'straight_draw_block_pct': (
            round(sd_blocked / sd_total, 6) if sd_total > 0 else 0.0
        ),
        'nut_made_block_pct': (
            round(nm_blocked / nm_total, 6) if nm_total > 0 else 0.0
        ),
    }
