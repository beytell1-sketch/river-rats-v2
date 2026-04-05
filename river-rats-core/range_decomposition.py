"""
Range Decomposition Engine
================================================================================

Decomposes villain's range into subcategory buckets, computes blocker effects,
and estimates calling ranges using MDF (Minimum Defense Frequency).

This is the foundation layer for L4-L5 coaching: it turns a villain range dict
into a structured RangeBreakdown that teaching layers consume.

Performance target: <20ms per decomposition (~285 combos).

Architecture:
    decompose_range() -> RangeBreakdown
        - Iterates villain range, expands combos, evaluates each via eval7
        - Classifies into 26 subcategories (monster -> air)
        - Computes blocker counts analytically (theoretical_max - actual)
        - Estimates calling range via MDF adjusted by SPR

See Also:
    - feature_extractor.py: get_valid_combos(), partition_range()
    - range_narrowing.py: classify_hand()
    - hand_evaluator.py: evaluate_hand(), HandEvaluation
    - hand_categories.py: RANK_VALUES, SUITS
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

import eval7

from hand_categories import RANK_VALUES, SUITS
from feature_extractor import get_valid_combos, _to_eval7_cards
from hand_evaluator import evaluate_hand


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class HandBucket:
    """One subcategory bucket in the range breakdown."""
    category: str           # "flush", "straight", "two_pair"
    subcategory: str        # "nut_flush", "weak_flush"
    total_combos: int
    beats_hero: int
    loses_to_hero: int
    pct_of_range: float


@dataclass
class BlockerInfo:
    """Blocker analysis results."""
    total_blocked: int
    by_card: Dict[str, int]               # {"Jh": 3}
    descriptions: List[str]               # ["Jh blocks 3 flush combos"]
    blocks_value: bool                    # Hero blocks hands that would call
    blocks_bluffs: bool                   # Hero blocks hands that would bluff


@dataclass
class RangeBreakdown:
    """Complete range decomposition result."""
    hero_label: str                       # "J-high flush"
    total_combos: int
    buckets: List[HandBucket]             # Sorted best -> worst
    better_pct: float
    worse_pct: float
    blocker_info: BlockerInfo
    # Value targeting (bet-sizing aware via MDF)
    calling_range_pct: float              # Estimated % that calls a raise
    hero_equity_vs_callers: float         # Hero's equity vs calling range
    value_target_pct: float               # Worse hands that would call


# =============================================================================
# SUBCATEGORY HIERARCHY (26 subcategories, best -> worst)
# =============================================================================

SUBCATEGORY_ORDER = [
    'straight_flush', 'quads', 'full_house',
    'nut_flush', 'strong_flush', 'weak_flush',
    'nut_straight', 'weak_straight', 'top_set',
    'combo_draw', 'lower_set', 'top_two_pair', 'other_two_pair',
    'overpair', 'top_pair_strong_kicker', 'top_pair_weak_kicker', 'second_pair',
    'bottom_pair', 'underpair',
    'nut_flush_draw', 'flush_draw', 'oesd', 'gutshot',
    'overcards', 'air',
]

# Map subcategory -> broad category for the HandBucket.category field
_SUBCATEGORY_TO_CATEGORY = {}
_CAT_MAP = {
    'straight_flush': 'straight_flush', 'quads': 'quads', 'full_house': 'full_house',
    'nut_flush': 'flush', 'strong_flush': 'flush', 'weak_flush': 'flush',
    'nut_straight': 'straight', 'weak_straight': 'straight',
    'top_set': 'set', 'lower_set': 'set',
    'combo_draw': 'draw',
    'top_two_pair': 'two_pair', 'other_two_pair': 'two_pair',
    'overpair': 'overpair',
    'top_pair_strong_kicker': 'top_pair', 'top_pair_weak_kicker': 'top_pair',
    'second_pair': 'pair', 'bottom_pair': 'pair', 'underpair': 'pair',
    'nut_flush_draw': 'draw', 'flush_draw': 'draw', 'oesd': 'draw', 'gutshot': 'draw',
    'overcards': 'high_card', 'air': 'air',
}

# Subcategories that are "value" hands (would call a raise)
_VALUE_SUBCATEGORIES = set(SUBCATEGORY_ORDER[:19])  # everything through underpair
# Subcategories that are "bluff" hands
_BLUFF_SUBCATEGORIES = {'nut_flush_draw', 'flush_draw', 'oesd', 'gutshot', 'overcards', 'air'}


# =============================================================================
# RANK HELPERS
# =============================================================================

def _rank_value(rank_char: str) -> int:
    """Convert rank character to numeric value (A=14, K=13, ..., 2=2)."""
    return RANK_VALUES.get(rank_char.upper(), 0)


def _rank_name(val: int) -> str:
    """Convert numeric rank value to display name."""
    names = {14: 'A', 13: 'K', 12: 'Q', 11: 'J', 10: 'T',
             9: '9', 8: '8', 7: '7', 6: '6', 5: '5', 4: '4', 3: '3', 2: '2'}
    return names.get(val, '?')


# =============================================================================
# SUBCATEGORY CLASSIFICATION
# =============================================================================

def _classify_combo_subcategory(
    combo_cards: List[str],
    board_cards: List[str],
    eval7_value: int,
) -> str:
    """
    Classify a specific combo into one of the 26 subcategories.

    Uses eval7 value ranges + card analysis to determine the precise
    subcategory (e.g. nut_flush vs weak_flush).

    Args:
        combo_cards: Villain's two hole cards, e.g. ['Ah', 'Kh']
        board_cards: Board cards, e.g. ['Kh', '7h', '2d', 'Th', '3s']
        eval7_value: eval7.evaluate() result for combo + board

    Returns:
        Subcategory string from SUBCATEGORY_ORDER
    """
    all_cards = combo_cards + board_cards

    # Parse ranks and suits
    combo_ranks = [_rank_value(c[0]) for c in combo_cards]
    combo_suits = [c[1].lower() for c in combo_cards]
    board_ranks = sorted([_rank_value(c[0]) for c in board_cards], reverse=True)
    board_suits = [c[1].lower() for c in board_cards]
    all_ranks = combo_ranks + board_ranks
    all_suits = combo_suits + board_suits

    # Count suits across all cards
    suit_counts = defaultdict(int)
    for s in all_suits:
        suit_counts[s] += 1

    # Count ranks across all cards
    rank_counts = defaultdict(int)
    for r in all_ranks:
        rank_counts[r] += 1

    # Board rank counts (for detecting board pairs vs combo pairs)
    board_rank_counts = defaultdict(int)
    for r in board_ranks:
        board_rank_counts[r] += 1

    # Determine flush suit (5+ of same suit in all cards)
    flush_suit = None
    for s, cnt in suit_counts.items():
        if cnt >= 5:
            flush_suit = s
            break

    # Determine if combo contributes to flush
    combo_flush_cards = []
    if flush_suit:
        combo_flush_cards = [_rank_value(c[0]) for c in combo_cards if c[1].lower() == flush_suit]

    # Check for straight (5 consecutive ranks)
    unique_sorted = sorted(set(all_ranks), reverse=True)
    straight_high = _check_straight_high(all_ranks)

    # Combo contributes to straight?
    combo_in_straight = False
    if straight_high:
        if straight_high == 5:  # wheel
            straight_set = {14, 2, 3, 4, 5}
        else:
            straight_set = set(range(straight_high - 4, straight_high + 1))
        combo_in_straight = any(r in straight_set for r in combo_ranks) or \
                           (14 in combo_ranks and 1 in straight_set)

    # --- Straight Flush ---
    if flush_suit and straight_high and combo_flush_cards:
        flush_ranks_all = sorted(
            [_rank_value(c[0]) for c in all_cards if c[1].lower() == flush_suit],
            reverse=True
        )
        sf_high = _check_straight_high(flush_ranks_all)
        if sf_high:
            return 'straight_flush'

    # --- Quads ---
    quads_ranks = [r for r, c in rank_counts.items() if c == 4]
    if quads_ranks and any(r in combo_ranks for r in quads_ranks):
        return 'quads'

    # --- Full House ---
    trips_ranks = sorted([r for r, c in rank_counts.items() if c >= 3], reverse=True)
    pairs_ranks = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
    if trips_ranks and (pairs_ranks or len(trips_ranks) > 1):
        # Check combo contributes (has a card matching the trips or pair rank)
        trip_r = trips_ranks[0]
        combo_contributes = any(r == trip_r for r in combo_ranks) or \
                           any(r in pairs_ranks for r in combo_ranks) or \
                           (len(trips_ranks) > 1 and any(r in trips_ranks for r in combo_ranks))
        if combo_contributes:
            return 'full_house'

    # --- Flush ---
    if flush_suit and len(combo_flush_cards) >= 1:
        board_flush_count = sum(1 for c in board_cards if c[1].lower() == flush_suit)
        total_flush = board_flush_count + len(combo_flush_cards)
        if total_flush >= 5:
            high_card = max(combo_flush_cards)
            if high_card == 14:
                return 'nut_flush'
            elif high_card >= 12:  # K or Q
                return 'strong_flush'
            else:
                return 'weak_flush'

    # --- Straight ---
    if straight_high and combo_in_straight:
        # Is it the nut straight? Check if a higher straight is possible
        # by seeing if there's a higher 5-consecutive available on the board
        if _is_nut_straight(straight_high, board_ranks):
            return 'nut_straight'
        else:
            return 'weak_straight'

    # --- Three of a Kind (Set vs Trips) ---
    if trips_ranks:
        for tr in trips_ranks:
            # Set = pocket pair hits board; Trips = one in hand, two on board
            combo_count_of_rank = combo_ranks.count(tr)
            if combo_count_of_rank >= 1:
                if combo_count_of_rank == 2:
                    # Pocket pair -> set
                    if tr == board_ranks[0]:
                        return 'top_set'
                    else:
                        return 'lower_set'
                else:
                    # One in hand, two on board -> trips (treat as lower_set)
                    if board_rank_counts.get(tr, 0) >= 2:
                        if tr == board_ranks[0]:
                            return 'top_set'
                        else:
                            return 'lower_set'

    # --- Two Pair ---
    all_pairs = sorted([r for r, c in rank_counts.items() if c >= 2], reverse=True)
    if len(all_pairs) >= 2:
        # Check that combo contributes to at least one pair
        combo_pairs = [r for r in all_pairs if r in combo_ranks]
        if combo_pairs:
            top_pair_rank = all_pairs[0]
            second_pair_rank = all_pairs[1]
            if top_pair_rank == board_ranks[0]:
                return 'top_two_pair'
            elif any(r == board_ranks[0] for r in combo_pairs):
                return 'top_two_pair'
            else:
                return 'other_two_pair'

    # --- One Pair ---
    if all_pairs:
        pair_rank = all_pairs[0]
        combo_is_pocket = combo_ranks[0] == combo_ranks[1]

        if combo_is_pocket:
            if pair_rank > board_ranks[0]:
                return 'overpair'
            elif pair_rank < board_ranks[-1]:
                return 'underpair'
            else:
                # Pocket pair between board cards
                return 'underpair'
        else:
            # One of our cards pairs a board card
            paired_rank = None
            for cr in combo_ranks:
                if cr in board_ranks:
                    paired_rank = cr
                    break

            if paired_rank is None:
                # Board has a pair, we don't contribute -> treat as air/overcards
                pass
            elif paired_rank == board_ranks[0]:
                # Top pair - check kicker
                kicker = max(r for r in combo_ranks if r != paired_rank) if len(set(combo_ranks)) > 1 else combo_ranks[0]
                if kicker >= 12:  # Q+
                    return 'top_pair_strong_kicker'
                else:
                    return 'top_pair_weak_kicker'
            elif len(board_ranks) > 1 and paired_rank == board_ranks[1]:
                return 'second_pair'
            else:
                return 'bottom_pair'

    # --- No made hand: check draws ---
    # Flush draw: 4 to a suit with at least one combo card
    has_flush_draw = False
    fd_suit = None
    fd_is_nut = False
    for s, cnt in suit_counts.items():
        if cnt == 4:
            combo_in_suit = [_rank_value(c[0]) for c in combo_cards if c[1].lower() == s]
            if combo_in_suit:
                has_flush_draw = True
                fd_suit = s
                fd_is_nut = 14 in combo_in_suit
                break

    # Straight draw: check for OESD (8 outs) or gutshot (4 outs)
    sd_type = _check_straight_draw_type(combo_ranks, board_ranks)

    # Combo draw: flush draw + straight draw
    if has_flush_draw and sd_type:
        return 'combo_draw'

    if has_flush_draw:
        if fd_is_nut:
            return 'nut_flush_draw'
        else:
            return 'flush_draw'

    if sd_type == 'oesd':
        return 'oesd'
    elif sd_type == 'gutshot':
        return 'gutshot'

    # --- Overcards or Air ---
    if all(cr > board_ranks[0] for cr in combo_ranks):
        return 'overcards'

    return 'air'


def _check_straight_high(ranks: List[int]) -> Optional[int]:
    """
    Find the highest straight in a set of ranks.
    Returns the high card of the straight, or None.
    """
    unique = sorted(set(ranks), reverse=True)
    # Add low ace
    if 14 in unique:
        unique.append(1)

    for i in range(len(unique) - 4):
        if unique[i] - unique[i + 4] == 4:
            # Check all 5 are consecutive
            window = unique[i:i+5]
            if all(window[j] - window[j+1] == 1 for j in range(4)):
                return unique[i]
    return None


def _is_nut_straight(straight_high: int, board_ranks: List[int]) -> bool:
    """
    Check if the given straight is the highest possible straight
    using the board cards.
    """
    # The nut straight uses the highest possible cards.
    # Check: could a higher straight exist?
    # A straight needs 5 consecutive ranks. The board provides some.
    # If straight_high == 14 (ace-high), it's the nut straight.
    if straight_high == 14:
        return True

    # Check if a higher straight is possible given the board
    all_possible = set(board_ranks)
    if 14 in all_possible:
        all_possible.add(1)

    for high in range(14, straight_high, -1):
        if high == 5:
            needed = {1, 2, 3, 4, 5}
        else:
            needed = set(range(high - 4, high + 1))
        # A higher straight needs at least 3 of its 5 ranks on the board
        # (villain has 2 cards). Actually, just needs board to have 3+.
        board_contribution = len(needed & all_possible)
        if board_contribution >= 3:
            return False  # A higher straight is possible
    return True


def _check_straight_draw_type(combo_ranks: List[int], board_ranks: List[int]) -> Optional[str]:
    """
    Check if combo + board has a straight draw.
    Returns 'oesd', 'gutshot', or None.
    """
    all_ranks = set(combo_ranks) | set(board_ranks)
    if 14 in all_ranks:
        all_ranks.add(1)

    # Check all possible straights and count how many more cards are needed
    best_draw = None
    for high in range(14, 4, -1):
        if high == 5:
            needed = {1, 2, 3, 4, 5}
        else:
            needed = set(range(high - 4, high + 1))

        present = len(needed & all_ranks)
        if present == 4:
            # 4 of 5 cards present = draw
            # Check if combo contributes
            combo_set = set(combo_ranks)
            if 14 in combo_set:
                combo_set.add(1)
            if combo_set & needed:
                # Determine OESD vs gutshot
                # OESD = open-ended = missing card is at either end
                missing = needed - all_ranks
                if len(missing) == 1:
                    missing_rank = list(missing)[0]
                    if missing_rank == min(needed) or missing_rank == max(needed):
                        return 'oesd'
                    else:
                        if best_draw is None:
                            best_draw = 'gutshot'

    return best_draw


# =============================================================================
# HERO LABEL
# =============================================================================

def _make_hero_label(hero_cards: List[str], board_cards: List[str]) -> str:
    """Generate a human-readable label for hero's hand."""
    try:
        ev = evaluate_hand(hero_cards, board_cards)
        return ev.description
    except Exception:
        return "unknown hand"


# =============================================================================
# THEORETICAL MAX COMBOS (for blocker calculation)
# =============================================================================

def _theoretical_max_combos(hand: str) -> int:
    """
    Return the max combos for a hand notation ignoring card removal.
    Pairs: 6, suited: 4, offsuit: 12.
    """
    if len(hand) < 2:
        return 0
    r1, r2 = hand[0], hand[1]
    if r1 == r2:
        return 6
    if len(hand) >= 3 and hand[2].lower() == 's':
        return 4
    return 12


# =============================================================================
# BLOCKER COMPUTATION
# =============================================================================

def _compute_blockers(
    hero_cards: List[str],
    board_cards: List[str],
    hand_combo_counts: Dict[str, Tuple[int, int]],
) -> BlockerInfo:
    """
    Compute blocker effects analytically.

    For each hand notation, theoretical_max - actual_combos = blocked.
    Then attribute blocked combos to hero cards.

    Args:
        hero_cards: Hero's hole cards
        board_cards: Board cards
        hand_combo_counts: {hand_notation: (actual_combos, theoretical_max)}

    Returns:
        BlockerInfo with totals and descriptions
    """
    total_blocked = 0
    by_card: Dict[str, int] = defaultdict(int)

    # Board blocks combos too, but we attribute hero's blocking separately
    # by checking: how many combos does hero's hand specifically remove?
    board_set = {c.lower() for c in board_cards}

    for hand_str, (actual, theoretical) in hand_combo_counts.items():
        # Total blocked = theoretical - actual - board_blocked
        # First compute board-only blocking
        board_only_used = set(board_cards)
        board_combos = get_valid_combos(hand_str, board_only_used)
        board_only_count = len(board_combos)

        # Hero blocks = board_only_count - actual
        hero_blocked = max(0, board_only_count - actual)
        total_blocked += hero_blocked

        if hero_blocked > 0:
            # Attribute to each hero card
            for hc in hero_cards:
                # Check if this card would be used in the hand
                hr = hc[0].upper()
                hs = hc[1].lower()
                r1 = hand_str[0].upper()
                r2 = hand_str[1].upper() if len(hand_str) > 1 else ''
                is_suited = len(hand_str) >= 3 and hand_str[2].lower() == 's'
                is_offsuit = len(hand_str) >= 3 and hand_str[2].lower() == 'o'

                card_blocks = False
                if hr == r1 or hr == r2:
                    if is_suited:
                        # Suited: card must match rank AND removes that suit combo
                        card_blocks = True
                    else:
                        card_blocks = True

                if card_blocks:
                    by_card[hc] += hero_blocked

    # Generate descriptions
    descriptions = []
    for card, count in sorted(by_card.items(), key=lambda x: -x[1]):
        if count > 0:
            # Determine what kind of combos are blocked
            card_rank = card[0].upper()
            card_suit = card[1].lower()
            descriptions.append(f"{card} blocks {count} combos")

    # Determine if hero blocks value or bluffs
    # (simplified: if hero card matches high board cards or flush suit -> blocks value)
    board_suits_list = [c[1].lower() for c in board_cards]
    suit_counts = defaultdict(int)
    for s in board_suits_list:
        suit_counts[s] += 1

    blocks_value = False
    blocks_bluffs = False

    for hc in hero_cards:
        hs = hc[1].lower()
        hr = _rank_value(hc[0])

        # Blocks flush if hero has a card in the flush suit
        flush_suit = None
        for s, cnt in suit_counts.items():
            if cnt >= 3:
                flush_suit = s
                break
        if flush_suit and hs == flush_suit:
            if hr >= 12:  # Q+ in flush suit -> blocks value flushes
                blocks_value = True
            else:
                blocks_bluffs = True

        # Blocks sets/top pair if hero card matches top board rank
        board_ranks = [_rank_value(c[0]) for c in board_cards]
        if hr in board_ranks:
            blocks_value = True

    return BlockerInfo(
        total_blocked=total_blocked,
        by_card=dict(by_card),
        descriptions=descriptions[:5],
        blocks_value=blocks_value,
        blocks_bluffs=blocks_bluffs,
    )


# =============================================================================
# CALLING RANGE ESTIMATION (MDF-based)
# =============================================================================

def _estimate_calling_range(
    buckets: List[HandBucket],
    total_combos: int,
    hero_eval7_value: int,
    spr: float,
    bet_to_pot: float,
) -> Tuple[float, float, float]:
    """
    Estimate what portion of villain's range calls a bet/raise using MDF.

    MDF = 1 / (1 + bet_size/pot). At 75% pot bet, MDF = 57%.
    Adjust for SPR: low SPR -> tighter calls, high SPR -> wider.

    Returns:
        (calling_pct, hero_equity_vs_callers, value_target_pct)
    """
    if bet_to_pot <= 0 or total_combos == 0:
        return 0.0, 0.0, 0.0

    mdf = 1.0 / (1.0 + bet_to_pot)

    # SPR adjustment
    if spr < 3:
        mdf *= 0.85
    elif spr > 10:
        mdf *= 1.10

    mdf = min(mdf, 1.0)

    # Sort buckets by strength (subcategory order, which is best -> worst)
    # Buckets are already sorted best -> worst from decompose_range
    # Accumulate from top (strongest) until reaching MDF threshold
    target_combos = mdf * total_combos
    accumulated = 0
    calling_combos = 0
    hero_beats_in_callers = 0
    hero_loses_in_callers = 0
    worse_hands_that_call = 0

    for bucket in buckets:
        remaining = target_combos - accumulated
        if remaining <= 0:
            break

        take = min(bucket.total_combos, remaining)
        fraction = take / bucket.total_combos if bucket.total_combos > 0 else 0

        calling_combos += take
        hero_beats_in_callers += bucket.loses_to_hero * fraction
        hero_loses_in_callers += bucket.beats_hero * fraction
        worse_hands_that_call += bucket.loses_to_hero * fraction
        accumulated += take

    calling_pct = calling_combos / total_combos if total_combos > 0 else 0.0

    total_decided = hero_beats_in_callers + hero_loses_in_callers
    hero_equity = hero_beats_in_callers / total_decided if total_decided > 0 else 0.5

    value_target_pct = worse_hands_that_call / total_combos if total_combos > 0 else 0.0

    return calling_pct, hero_equity, value_target_pct


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def decompose_range(
    hero_cards: List[str],
    board_cards: List[str],
    villain_range: Dict[str, float],
    spr: float = 10.0,
    bet_to_pot: float = 0.0,
) -> RangeBreakdown:
    """
    Decompose villain's range into subcategory buckets with blocker analysis.

    Args:
        hero_cards: Hero's hole cards, e.g. ['Jh', '9h']
        board_cards: Board cards, e.g. ['Kh', '7h', '2d', 'Th', '3s']
        villain_range: {hand_notation: frequency}, e.g. {'AKs': 1.0, 'QJo': 0.5}
        spr: Stack-to-pot ratio
        bet_to_pot: Bet size as fraction of pot (0.75 = 75% pot)

    Returns:
        RangeBreakdown with buckets, blockers, and calling range estimates
    """
    used_cards = set(hero_cards) | set(board_cards)

    # Pre-compute hero's eval7 value
    hero_eval7 = _to_eval7_cards(hero_cards + board_cards)
    hero_value = eval7.evaluate(hero_eval7)

    # Hero label
    hero_label = _make_hero_label(hero_cards, board_cards)

    # Pre-compute board eval7 cards
    board_eval7 = _to_eval7_cards(board_cards)

    # Accumulate subcategory data
    # {subcategory: [total_combos, beats_hero, loses_to_hero]}
    subcat_data: Dict[str, List[int]] = defaultdict(lambda: [0, 0, 0])

    # Track combo counts for blocker calculation
    hand_combo_counts: Dict[str, Tuple[int, int]] = {}

    total_combos = 0

    for hand_str, freq in villain_range.items():
        if freq <= 0:
            continue

        combos = get_valid_combos(hand_str, used_cards)
        actual_count = len(combos)
        theoretical = _theoretical_max_combos(hand_str)
        hand_combo_counts[hand_str] = (actual_count, theoretical)

        for v_combo in combos:
            v_eval7 = _to_eval7_cards(v_combo)
            v_value = eval7.evaluate(v_eval7 + board_eval7)

            beats_hero = 1 if v_value > hero_value else 0
            loses = 1 if v_value < hero_value else 0

            # Classify into subcategory
            subcat = _classify_combo_subcategory(v_combo, board_cards, v_value)

            subcat_data[subcat][0] += 1
            subcat_data[subcat][1] += beats_hero
            subcat_data[subcat][2] += loses

            total_combos += 1

    # Build buckets in subcategory order
    buckets = []
    for subcat in SUBCATEGORY_ORDER:
        if subcat in subcat_data:
            data = subcat_data[subcat]
            cat = _CAT_MAP.get(subcat, subcat)
            buckets.append(HandBucket(
                category=cat,
                subcategory=subcat,
                total_combos=data[0],
                beats_hero=data[1],
                loses_to_hero=data[2],
                pct_of_range=data[0] / total_combos if total_combos > 0 else 0.0,
            ))

    # Any subcategories not in our predefined list
    for subcat, data in subcat_data.items():
        if subcat not in SUBCATEGORY_ORDER:
            cat = _CAT_MAP.get(subcat, subcat)
            buckets.append(HandBucket(
                category=cat,
                subcategory=subcat,
                total_combos=data[0],
                beats_hero=data[1],
                loses_to_hero=data[2],
                pct_of_range=data[0] / total_combos if total_combos > 0 else 0.0,
            ))

    # Compute better/worse percentages
    total_better = sum(b.beats_hero for b in buckets)
    total_worse = sum(b.loses_to_hero for b in buckets)
    better_pct = total_better / total_combos if total_combos > 0 else 0.0
    worse_pct = total_worse / total_combos if total_combos > 0 else 0.0

    # Blocker analysis
    blocker_info = _compute_blockers(hero_cards, board_cards, hand_combo_counts)

    # Calling range estimation
    calling_pct, hero_eq_vs_callers, value_target = _estimate_calling_range(
        buckets, total_combos, hero_value, spr, bet_to_pot
    )

    return RangeBreakdown(
        hero_label=hero_label,
        total_combos=total_combos,
        buckets=buckets,
        better_pct=better_pct,
        worse_pct=worse_pct,
        blocker_info=blocker_info,
        calling_range_pct=calling_pct,
        hero_equity_vs_callers=hero_eq_vs_callers,
        value_target_pct=value_target,
    )
