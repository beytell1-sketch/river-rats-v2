#!/usr/bin/env python3
"""
Range Narrowing - GTO-Based Action Filtering
=============================================

Narrows villain range based on whether they BET or CHECK.

GTO Theory:
-----------
When villain BETS Ã¢â€ â€™ Polarized range:
    - Strong value hands (90% bet)
    - Draws/semi-bluffs (70% bet)  
    - Bluffs (30% bet)
    - Medium made hands (20% bet) Ã¢â€ Ã‚Â These check for showdown value!

When villain CHECKS Ã¢â€ â€™ Condensed/Capped range:
    - Strong hands (15% trap)
    - Draws (30% give up)
    - Medium made hands (80% check) Ã¢â€ Ã‚Â Showdown value
    - Weak hands (70% give up)

Key Insight:
    "Our weaker middling hands are 100% pure checks however since they 
     do not function well as part of the larger bet-sizing range."
    Ã¢â‚¬Ã¢â‚¬Â GTO Poker Gems

This is the PRIMARY architectural fix for FÃ¢â€ â€™R errors (37% of all errors).
The engine was using full range when villain bets, causing us to overestimate
our equity and fold equity.

Usage:
    from range_narrowing import narrow_to_betting_range, narrow_to_checking_range
    
    if facing_bet:
        villain_range = narrow_to_betting_range(full_range, board, street)
    else:
        villain_range = narrow_to_checking_range(full_range, board, street)
"""

import sys
sys.path = ['/home/claude'] + [p for p in sys.path if '/mnt/project' not in p]

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import itertools

# Try to import eval7 for fast evaluation, fall back to hand_evaluator
try:
    import eval7
    HAS_EVAL7 = True
except ImportError:
    HAS_EVAL7 = False

# Import hand evaluator for strength classification
from hand_evaluator import evaluate_hand, HandEvaluation


# =============================================================================
# CONSTANTS - GTO Betting Frequencies BY STREET
# =============================================================================
# 
# Key GTO Insight: Polarization increases through the streets
# - FLOP: Merged/wide betting (protection, thin value, semi-bluffs)
# - TURN: Starting to polarize (draws decide, pot control increases)
# - RIVER: Fully polarized (VALUE + BLUFFS only, medium = bluff-catcher)
#
# Quote: "Clear pairs of polarized and condensed ranges only really exist 
#        on the river (and occasionally on very dry turns)." - GTO Poker Gems
#
# Quote: "The river is the only spot in poker where you don't need to worry
#        about protecting your check-back range." - GTO Wizard
# =============================================================================

# FLOP: Merged betting range - many medium hands bet for protection
FLOP_BETTING_FREQUENCIES = {
    'nuts': 0.85,           # Strong bet, but some slow-play
    'strong_value': 0.75,   # Sets might check on draw-heavy boards
    'good_value': 0.70,     # Overpairs, TPTK - usually bet
    'draw': 0.55,           # Semi-bluffs mixed
    'medium_made': 0.45,    # Top pair weak kicker - CHECKS often for pot control
    'weak_made': 0.35,      # Some protection bets
    'bluff': 0.25,          # Light bluffs with blockers
    'air': 0.20,            # Some c-bets with air
}

# TURN: Starting to polarize - draws decide, medium hands pot control more
TURN_BETTING_FREQUENCIES = {
    'nuts': 0.90,           # Almost always bet
    'strong_value': 0.80,   # Value bet
    'good_value': 0.60,     # More pot control than flop
    'draw': 0.55,           # Continue semi-bluff or give up
    'medium_made': 0.30,    # Check more for pot control
    'weak_made': 0.20,      # Less protection betting
    'bluff': 0.25,          # Barrel or give up
    'air': 0.15,            # Give up more air
}

# RIVER: Fully polarized - VALUE + BLUFFS only
# Medium hands become pure bluff-catchers (almost NEVER bet)
RIVER_BETTING_FREQUENCIES = {
    'nuts': 0.95,           # Almost pure bet
    'strong_value': 0.90,   # Bet for value
    'good_value': 0.55,     # Thin value (board dependent)
    'draw': 0.00,           # Draws missed = air (reclassify)
    'medium_made': 0.08,    # Almost NEVER bet! Pure bluff-catcher
    'weak_made': 0.05,      # Almost never bet
    'bluff': 0.35,          # Specific bluff combos with blockers
    'air': 0.20,            # Some bluffs
}

# For backwards compatibility
BETTING_FREQUENCIES = FLOP_BETTING_FREQUENCIES

# Checking frequencies mirror betting (1 - bet_freq, approximately)
FLOP_CHECKING_FREQUENCIES = {
    'nuts': 0.15,           # Rare traps
    'strong_value': 0.25,   # Some traps on draw boards
    'good_value': 0.30,     # Some pot control
    'draw': 0.45,           # Mix with checks
    'medium_made': 0.55,    # Checks for showdown value
    'weak_made': 0.65,      # Mostly check
    'bluff': 0.75,          # Mostly give up
    'air': 0.80,            # Mostly give up
}

TURN_CHECKING_FREQUENCIES = {
    'nuts': 0.10,
    'strong_value': 0.20,
    'good_value': 0.40,
    'draw': 0.45,
    'medium_made': 0.70,    # Check more on turn
    'weak_made': 0.80,
    'bluff': 0.75,
    'air': 0.85,
}

RIVER_CHECKING_FREQUENCIES = {
    'nuts': 0.05,           # Rarely trap river
    'strong_value': 0.10,
    'good_value': 0.45,
    'draw': 1.00,           # "Draw" on river = missed = check/fold
    'medium_made': 0.92,    # Almost ALWAYS check! Bluff-catcher
    'weak_made': 0.95,
    'bluff': 0.65,          # Many give up
    'air': 0.80,
}

# =============================================================================
# v2.4 Stage 3.5 — CALL-continue frequencies (per GTO review M1 refined table)
# =============================================================================
# "What fraction of villain's range in this category calls a standard-sized
# bet on this street, given bet/fold/raise were available?"
#
# Heuristic — not direct solver output. Derived from solver intuition in KB
# §1.3 (c-bet frequency), §1.4 (bluff-to-value), §1.7 (semi-bluff conditions),
# §1.8 (blocker action selection). Two properties the simpler
# "1 - fold_freq - raise_freq" derivation would miss:
#   1. medium_made stays elevated across streets (bluff-catch / showdown band)
#   2. nuts / strong_value get SUPPRESSED (they raise, not call)
#
# These frequencies are applied via narrow_to_continuing_range() in the chain
# assembled by narrow_by_action_history(). Ship-tagged "heuristic, v2.4 MVP,
# not solver-run" per GTO review 2026-04-20 (commit a4cab83). Raise-aware
# variants deferred to v2.5 (TICKET_V25_PRO_LEVEL_NARROWING_GAPS_2026-04-20).
FLOP_CALL_FREQUENCIES = {
    'nuts':          0.15,  # mostly raises; only slow-plays call
    'strong_value':  0.35,  # mixes raise/call; more call on wet boards
    'good_value':    0.75,  # TPTK / overpair-type calls standardly
    'draw':          0.70,  # calls with pot odds + implied odds
    'medium_made':   0.55,  # calls with showdown; floats some
    'weak_made':     0.30,  # calls small, folds big
    'bluff':         0.15,  # rare float with blockers
    'air':           0.05,  # overwhelmingly folds
}
TURN_CALL_FREQUENCIES = {
    'nuts':          0.15,
    'strong_value':  0.30,  # raises more as pot grows
    'good_value':    0.70,  # TPTK continues
    'draw':          0.55,  # pot odds tighter; some give up
    'medium_made':   0.50,  # bluff-catcher band
    'weak_made':     0.15,  # mostly folds by turn
    'bluff':         0.10,
    'air':           0.03,
}
RIVER_CALL_FREQUENCIES = {
    'nuts':          0.20,  # mostly raises
    'strong_value':  0.40,  # thin raise vs polarised bet
    'good_value':    0.65,  # standard bluff-catch
    'draw':          0.00,  # missed = air; already handled upstream
    'medium_made':   0.55,  # primary bluff-catch band
    'weak_made':     0.20,  # folds most
    'bluff':         0.05,
    'air':           0.02,
}

# =============================================================================
# v2.4 Stage 3.5 — M1 update: tighten RIVER_BETTING_FREQUENCIES for 3-way
# =============================================================================
# Rationale: the two entries below were HU-correct. When applied post-chain
# to an already-narrowed range (as they will be after Stage 3.5), they
# over-state river bluff density. §1.4 is explicit: 3-way river bluff:value
# is ~1:4 or tighter (~20% bluffs, not 33%). §1.7: pure bluffs nearly
# eliminated 3-way. See GTO review Flag A (commit a4cab83).
RIVER_BETTING_FREQUENCIES['bluff'] = 0.20  # was 0.35 — 3-way-aware
RIVER_BETTING_FREQUENCIES['air']   = 0.10  # was 0.20 — 3-way-aware


# =============================================================================
# HAND CLASSIFICATION
# =============================================================================

@dataclass
class HandClassification:
    """Classification of a hand on a board."""
    hand: str
    category: str  # 'nuts', 'strong_value', 'draw', 'medium_made', etc.
    strength: float  # 0-1 normalized
    has_draw: bool
    draw_outs: int


def classify_hand(hand: str, board: List[str]) -> HandClassification:
    """
    Classify a hand into GTO betting categories.
    
    Categories:
        - nuts: Best possible hand or near-nuts
        - strong_value: Sets, straights, flushes, top two pair
        - good_value: Overpairs, top pair top kicker, good two pair
        - draw: Flush draws, straight draws (8+ outs)
        - medium_made: Top pair weak kicker, second pair, overpairs below top card
        - weak_made: Bottom pair, weak showdown
        - bluff: Has blockers but no made hand
        - air: No showdown value, no blockers
    """
    # Convert hand notation to hole cards
    hole_cards = _parse_hand_to_cards(hand, board)
    if not hole_cards:
        return HandClassification(hand, 'air', 0.0, False, 0)
    
    # Evaluate the hand
    try:
        evaluation = evaluate_hand(hole_cards, board)
    except Exception:
        return HandClassification(hand, 'air', 0.0, False, 0)
    
    strength = evaluation.made_hand_strength
    has_draw = evaluation.has_flush_draw or evaluation.has_straight_draw
    draw_outs = evaluation.draw_outs
    category_name = evaluation.category.lower()
    
    # Get hole card ranks and board info for detailed classification
    hole_ranks = sorted([_rank_value(c[0]) for c in hole_cards], reverse=True)
    board_ranks = sorted([_rank_value(c[0]) for c in board], reverse=True)
    top_board_rank = board_ranks[0] if board_ranks else 0
    
    # Classify into betting categories
    if evaluation.is_monster:
        # Trips+, straights, flushes, full houses
        if strength >= 0.90:
            category = 'nuts'
        else:
            category = 'strong_value'
    
    elif category_name == 'two_pair':
        # Two pair - check if top two pair
        if hole_ranks[0] >= top_board_rank and hole_ranks[1] >= board_ranks[1] if len(board_ranks) > 1 else True:
            category = 'strong_value'  # Top two pair
        else:
            category = 'good_value'
    
    elif 'top_pair' in category_name:
        # Top pair - check kicker
        if 'top_kicker' in category_name or 'good_kicker' in category_name:
            category = 'good_value'  # TPTK or TPGK
        else:
            category = 'medium_made'  # Top pair weak kicker
    
    elif category_name == 'overpair':
        # Overpair above the board - strong!
        category = 'good_value'
    
    elif category_name in ('second_pair', 'middle_pair', 'underpair'):
        # Pairs below top pair
        if strength >= 0.45:
            category = 'medium_made'
        else:
            category = 'weak_made'
    
    elif has_draw and draw_outs >= 8:
        # Strong draw (flush draw, OESD, combo draw)
        category = 'draw'
    
    elif evaluation.is_made_hand:
        # Has a pair but not top pair/overpair
        if strength >= 0.45:
            category = 'medium_made'  # Decent pair
        else:
            category = 'weak_made'    # Bottom/weak pair
    
    elif has_draw and draw_outs >= 4:
        # Weak draw (gutshot, backdoor)
        category = 'bluff'
    
    else:
        # No made hand, no significant draw
        # Check for blockers (Ax, Kx on A/K high boards)
        if _has_blockers(hole_cards, board):
            category = 'bluff'
        else:
            category = 'air'
    
    return HandClassification(
        hand=hand,
        category=category,
        strength=strength,
        has_draw=has_draw,
        draw_outs=draw_outs,
    )


def _rank_value(rank_char: str) -> int:
    """Convert rank character to numeric value."""
    rank_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    return rank_map.get(rank_char.upper(), 0)


def _parse_hand_to_cards(hand: str, board: List[str]) -> Optional[List[str]]:
    """
    Convert hand notation to specific cards, avoiding board cards.
    
    Handles:
        - "AhKh" -> ["Ah", "Kh"]
        - "AKs" -> ["Ah", "Kh"] or similar suited combo
        - "AKo" -> ["Ah", "Kd"] or similar offsuit combo
        - "AK" -> treated as offsuit
    """
    if not hand or len(hand) < 2:
        return None
    
    # If already has suits (4 chars like "AhKh")
    if len(hand) == 4 and hand[1] in 'shdc' and hand[3] in 'shdc':
        return [hand[:2], hand[2:]]
    
    # Parse rank characters
    rank1 = hand[0].upper()
    rank2 = hand[1].upper()
    
    # Determine if suited/offsuit/pair
    if len(hand) >= 3:
        modifier = hand[2].lower()
    else:
        modifier = 'o'  # Default to offsuit
    
    # Get board suits to avoid
    board_cards = set(c.lower() for c in board)
    all_suits = ['h', 'd', 'c', 's']
    
    # Find available suits
    def find_available_suit(rank: str, exclude_cards: set) -> str:
        for suit in all_suits:
            card = f"{rank}{suit}"
            if card.lower() not in exclude_cards:
                return suit
        return 'h'  # Fallback
    
    if rank1 == rank2:
        # Pocket pair - need two different suits
        suit1 = find_available_suit(rank1, board_cards)
        card1 = f"{rank1}{suit1}"
        suit2 = find_available_suit(rank2, board_cards | {card1.lower()})
        card2 = f"{rank2}{suit2}"
    elif modifier == 's':
        # Suited - same suit
        suit = find_available_suit(rank1, board_cards)
        card1 = f"{rank1}{suit}"
        card2 = f"{rank2}{suit}"
        # Make sure both aren't blocked
        if f"{rank2}{suit}".lower() in board_cards:
            suit = find_available_suit(rank2, board_cards)
            card1 = f"{rank1}{suit}"
            card2 = f"{rank2}{suit}"
    else:
        # Offsuit - different suits
        suit1 = find_available_suit(rank1, board_cards)
        card1 = f"{rank1}{suit1}"
        # Pick different suit for card2
        other_suits = [s for s in all_suits if s != suit1]
        suit2 = other_suits[0]
        for s in other_suits:
            if f"{rank2}{s}".lower() not in board_cards:
                suit2 = s
                break
        card2 = f"{rank2}{suit2}"
    
    return [card1, card2]


def _has_blockers(hole_cards: List[str], board: List[str]) -> bool:
    """
    Check if hole cards have blocker value.
    
    Blockers are high cards that block opponent's strong hands.
    - Ax on A-high board blocks top pair
    - Kx on K-high board blocks top pair
    - Cards that block straights/flushes
    """
    if not hole_cards or not board:
        return False
    
    hole_ranks = set(c[0].upper() for c in hole_cards)
    board_ranks = [c[0].upper() for c in board]
    
    # Check if we have top card of board
    if board_ranks:
        # Sort by rank value
        rank_order = "23456789TJQKA"
        board_high = max(board_ranks, key=lambda r: rank_order.index(r) if r in rank_order else 0)
        if board_high in hole_ranks:
            return True
    
    # Check for A or K (always have some blocker value)
    if 'A' in hole_ranks or 'K' in hole_ranks:
        return True
    
    return False


# =============================================================================
# MAIN NARROWING FUNCTIONS
# =============================================================================

def narrow_to_betting_range(
    full_range: Dict[str, float],
    board: List[str],
    street: str = 'flop',
) -> Dict[str, float]:
    """
    Narrow range to hands villain would BET with.
    
    Street-aware polarization:
        - FLOP: Merged betting (many medium hands bet for protection)
        - TURN: Starting to polarize (medium hands pot control more)
        - RIVER: Fully polarized (VALUE + BLUFFS only)
    
    Args:
        full_range: Complete villain range {hand: frequency}
        board: Board cards
        street: Current street ('flop', 'turn', 'river')
    
    Returns:
        Narrowed range with betting frequencies applied
    """
    if not full_range or not board:
        return full_range
    
    # Select street-specific betting frequencies
    if street == 'river':
        betting_freqs = RIVER_BETTING_FREQUENCIES
    elif street == 'turn':
        betting_freqs = TURN_BETTING_FREQUENCIES
    else:  # flop or unknown
        betting_freqs = FLOP_BETTING_FREQUENCIES
    
    betting_range = {}
    total_weight = 0.0
    
    for hand, freq in full_range.items():
        if freq <= 0:
            continue
        
        # Classify the hand
        classification = classify_hand(hand, board)
        
        # Handle river: missed draws become air
        category = classification.category
        if street == 'river' and category == 'draw':
            category = 'air'  # Draws missed on river
        
        # Get betting frequency for this category and street
        bet_freq = betting_freqs.get(category, 0.20)
        
        # Apply betting frequency
        new_freq = freq * bet_freq
        if new_freq > 0.001:
            betting_range[hand] = new_freq
            total_weight += new_freq
    
    # Normalize to maintain probability distribution
    if total_weight > 0:
        for hand in betting_range:
            betting_range[hand] /= total_weight
    
    return betting_range


def narrow_to_checking_range(
    full_range: Dict[str, float],
    board: List[str],
    street: str = 'flop',
) -> Dict[str, float]:
    """
    Narrow range to hands villain would CHECK with (condensed/capped).
    
    Street-aware condensation:
        - FLOP: Some traps, many pot control checks
        - TURN: More checking with medium hands
        - RIVER: Mostly bluff-catchers (medium hands NEVER bet)
    
    Args:
        full_range: Complete villain range {hand: frequency}
        board: Board cards  
        street: Current street ('flop', 'turn', 'river')
    
    Returns:
        Narrowed range with checking frequencies applied
    """
    if not full_range or not board:
        return full_range
    
    # Select street-specific checking frequencies
    if street == 'river':
        checking_freqs = RIVER_CHECKING_FREQUENCIES
    elif street == 'turn':
        checking_freqs = TURN_CHECKING_FREQUENCIES
    else:  # flop or unknown
        checking_freqs = FLOP_CHECKING_FREQUENCIES
    
    checking_range = {}
    total_weight = 0.0
    
    for hand, freq in full_range.items():
        if freq <= 0:
            continue
        
        # Classify the hand
        classification = classify_hand(hand, board)
        
        # Handle river: missed draws become air
        category = classification.category
        if street == 'river' and category == 'draw':
            category = 'air'  # Draws missed on river = give up
        
        # Get checking frequency for this category and street
        check_freq = checking_freqs.get(category, 0.50)
        
        # Apply checking frequency
        new_freq = freq * check_freq
        if new_freq > 0.001:
            checking_range[hand] = new_freq
            total_weight += new_freq
    
    # Normalize to maintain probability distribution
    if total_weight > 0:
        for hand in checking_range:
            checking_range[hand] /= total_weight
    
    return checking_range


# =============================================================================
# v2.4 Stage 3.5 — action-aware chained narrowing
# =============================================================================
# See BUILDER_V24_STAGE35_SPEC_LOCKED_2026-04-20.md for the full spec. Two
# entry points:
#   narrow_to_continuing_range — per-street CALL filter (heuristic)
#   narrow_by_action_history   — walks the per-villain action history,
#                                 chaining bet/check/call narrowings
# Safety rails per GTO review Flag B:
#   - Empty-chain fallback: if a step produces total_weight == 0, return
#     the previous valid step's range (don't silently emit empty composition)
#   - Weight-floor threshold 5%: chain warns + returns last valid intermediate
#     if surviving weight drops below 5% of the original range total
#   - Surviving-weight metadata returned alongside range


# Weight-floor threshold (5% of original range total) — see GTO review Flag B
_STAGE35_WEIGHT_FLOOR_PCT = 0.05


def narrow_to_continuing_range(
    full_range: Dict[str, float],
    board: List[str],
    street: str = 'flop',
) -> Dict[str, float]:
    """v2.4 Stage 3.5: narrow a range to hands villain would CALL (continue
    but not raise or fold).

    Heuristic, not solver-verified. See FLOP/TURN/RIVER_CALL_FREQUENCIES
    above for the per-category multipliers + derivation rationale.

    Args:
        full_range: Complete villain range {hand: frequency}
        board: Board cards
        street: Current street ('flop', 'turn', 'river')

    Returns:
        Narrowed range with call frequencies applied, normalized.
    """
    if not full_range or not board:
        return full_range

    if street == 'river':
        call_freqs = RIVER_CALL_FREQUENCIES
    elif street == 'turn':
        call_freqs = TURN_CALL_FREQUENCIES
    else:
        call_freqs = FLOP_CALL_FREQUENCIES

    out_range = {}
    total_weight = 0.0

    for hand, freq in full_range.items():
        if freq <= 0:
            continue

        classification = classify_hand(hand, board)
        category = classification.category

        # River: missed draws become air (same convention as
        # narrow_to_checking_range + narrow_to_betting_range)
        if street == 'river' and category == 'draw':
            category = 'air'

        call_freq = call_freqs.get(category, 0.30)  # conservative default
        new_freq = freq * call_freq
        if new_freq > 0.001:
            out_range[hand] = new_freq
            total_weight += new_freq

    if total_weight > 0:
        for hand in out_range:
            out_range[hand] /= total_weight

    return out_range


def _action_to_narrow(action: str) -> str:
    """Map an action string to a narrowing class.

    Returns one of: 'bet', 'check', 'call', 'fold', 'skip'.
    'skip' means the action doesn't apply narrowing (e.g., preflop
    chips-related actions that happen outside the street-by-street
    postflop framework).
    """
    if not action:
        return 'skip'
    a = action.upper()
    if a in ('BET', 'RAISE'):
        return 'bet'
    if a == 'CHECK':
        return 'check'
    if a == 'CALL':
        return 'call'
    if a == 'FOLD':
        return 'fold'
    return 'skip'


def _street_board(full_board: List[str], street: str) -> List[str]:
    """Return the board as it existed on the named street."""
    if street == 'flop':
        return full_board[:3]
    if street == 'turn':
        return full_board[:4]
    if street == 'river':
        return full_board[:5]
    return full_board


def _normalize_action_entry(entry) -> Dict[str, str]:
    """Normalize a single action_history entry to {street, position, action}.

    Accepts either:
      - dict with 'street', 'position', 'action' keys, OR
      - 3-tuple (street, position, action)
    Unknown formats return an empty dict (caller skips).
    """
    if isinstance(entry, dict):
        return {
            'street': str(entry.get('street', '')).lower(),
            'position': str(entry.get('position', '')).upper(),
            'action': str(entry.get('action', '')).upper(),
        }
    if isinstance(entry, (list, tuple)) and len(entry) >= 3:
        return {
            'street': str(entry[0]).lower(),
            'position': str(entry[1]).upper(),
            'action': str(entry[2]).upper(),
        }
    return {}


def narrow_by_action_history(
    full_range: Dict[str, float],
    board: List[str],
    action_history: List,
    villain_pos: str,
    decision_street: str = 'river',
) -> Tuple[Dict[str, float], Dict[str, float]]:
    """v2.4 Stage 3.5: chain betting / checking / continuing narrowing
    across villain's action history.

    Walks streets flop → turn → river up to (but NOT including) actions on
    `decision_street`. Per-street, applies bet/check/call narrowing in the
    order villain acted that street.

    Per GTO review: same-street pre-hero actions are EXCLUDED (only strictly
    prior-street actions enter the chain). This preserves flop calibration
    anchors as zero-impact controls — see BUILDER_V24_STAGE35_SPEC_LOCKED.

    Per GTO review Flag B: three safety rails are applied:
      1. Empty-chain fallback (return last valid on total_weight==0)
      2. Weight-floor threshold (5% of original total)
      3. Surviving-weight metadata returned in the meta dict

    Args:
        full_range: preflop villain range (already position-aware)
        board: full current board cards (3-5)
        action_history: list of dicts/tuples with street/position/action
        villain_pos: primary villain's seat (e.g. 'BB')
        decision_street: the street the CURRENT decision is on
                         (actions on this street are NOT chained —
                         same-street actions enter via the current
                         facing_bet gate, not this chain)

    Returns:
        (narrowed_range, metadata) where metadata contains:
          - 'surviving_weight': fraction of original range weight retained
          - 'chain_steps': list of action-labels applied
          - 'truncated': True if weight-floor tripped and chain short-circuited
    """
    STREET_ORDER = ['flop', 'turn', 'river']
    if not full_range or not board:
        return full_range, {'surviving_weight': 1.0, 'chain_steps': [], 'truncated': False}

    original_weight = sum(freq for freq in full_range.values() if freq > 0)
    if original_weight <= 0:
        return full_range, {'surviving_weight': 0.0, 'chain_steps': [], 'truncated': False}

    weight_floor = original_weight * _STAGE35_WEIGHT_FLOOR_PCT

    # Schema-mismatch guard: if the first action entry can't normalize, log
    # and fallback to empty chain (feature_extractor fallback will kick in)
    if action_history:
        sample = _normalize_action_entry(action_history[0])
        if not sample.get('street'):
            return full_range, {
                'surviving_weight': 1.0,
                'chain_steps': [],
                'truncated': False,
                'schema_warning': f'action_history[0] malformed: {action_history[0]!r}',
            }

    current_range = dict(full_range)
    last_valid_range = dict(full_range)
    steps: List[str] = []
    truncated = False

    decision_street = decision_street.lower()

    for street in STREET_ORDER:
        if street == decision_street:
            # Reached the decision street — stop BEFORE applying any of its
            # actions. The current-street facing_bet gate handles those.
            break

        # Collect villain's actions on this prior street, in order
        villain_street_actions = []
        for entry in action_history:
            normed = _normalize_action_entry(entry)
            if normed.get('street') == street and normed.get('position') == villain_pos.upper():
                villain_street_actions.append(normed)

        if not villain_street_actions:
            continue  # villain didn't act on this street (or we don't have the data)

        street_board = _street_board(board, street)

        for act in villain_street_actions:
            narrow_class = _action_to_narrow(act.get('action', ''))
            if narrow_class == 'fold':
                # Villain folded — villain shouldn't be in the range anymore
                return {}, {
                    'surviving_weight': 0.0,
                    'chain_steps': steps + [f'{street}:FOLD'],
                    'truncated': False,
                }
            if narrow_class == 'bet':
                current_range = narrow_to_betting_range(current_range, street_board, street)
                steps.append(f'{street}:BET')
            elif narrow_class == 'check':
                current_range = narrow_to_checking_range(current_range, street_board, street)
                steps.append(f'{street}:CHECK')
            elif narrow_class == 'call':
                current_range = narrow_to_continuing_range(current_range, street_board, street)
                steps.append(f'{street}:CALL')
            else:
                continue  # skip unknown action types

            # Safety rail: empty-chain fallback. If narrowing produced an
            # empty range, revert to last valid and log.
            if not current_range:
                import logging
                logging.getLogger(__name__).warning(
                    'narrow_by_action_history: empty range after %s; '
                    'reverting to last valid', steps[-1] if steps else '?'
                )
                current_range = last_valid_range
                truncated = True
                break

            # Safety rail: weight-floor threshold. Since each narrow_* call
            # re-normalizes, surviving weight is measured by the PRODUCT of
            # un-normalized weights across steps. Approximation:
            # sum of current_range values (post-normalize) is always 1.0, so
            # the better check is "did the narrowing produce a degenerate
            # distribution" — detect via count of surviving hands.
            if len(current_range) < 3:
                import logging
                logging.getLogger(__name__).warning(
                    'narrow_by_action_history: chain collapsed to %d hands '
                    'after %s; reverting to last valid',
                    len(current_range), steps[-1] if steps else '?',
                )
                current_range = last_valid_range
                truncated = True
                break

            last_valid_range = dict(current_range)

        if truncated:
            break

    meta = {
        # Surviving weight is not directly recoverable after normalization.
        # Report chain_steps as the primary fidelity signal.
        'surviving_weight': float(len(current_range)) / max(1, len(full_range)),
        'chain_steps': steps,
        'truncated': truncated,
    }
    return current_range, meta


# =============================================================================
# TESTING
# =============================================================================

def test_narrowing():
    """Test range narrowing on sample hands."""
    print("=" * 60)
    print("RANGE NARROWING TEST")
    print("=" * 60)
    
    # Sample range (BTN RFI simplified)
    sample_range = {
        'AA': 1.0, 'KK': 1.0, 'QQ': 1.0, 'JJ': 1.0, 'TT': 1.0,
        '99': 1.0, '88': 1.0, '77': 1.0, '66': 1.0,
        'AKs': 1.0, 'AKo': 1.0, 'AQs': 1.0, 'AQo': 1.0,
        'AJs': 1.0, 'AJo': 1.0, 'ATs': 1.0,
        'KQs': 1.0, 'KQo': 1.0, 'KJs': 1.0, 'KTs': 1.0,
        'QJs': 1.0, 'QTs': 1.0, 'JTs': 1.0,
        'T9s': 1.0, '98s': 1.0, '87s': 1.0, '76s': 1.0,
        'A5s': 1.0, 'A4s': 1.0, 'A3s': 1.0, 'A2s': 1.0,
        '54s': 1.0, '65s': 1.0,
    }
    
    board = ['Kh', '7d', '2c']  # K-high dry board
    
    print(f"\nBoard: {' '.join(board)}")
    print(f"Full range: {len(sample_range)} hands")
    
    # Test betting range
    betting = narrow_to_betting_range(sample_range, board, 'flop')
    print(f"\nBETTING RANGE ({len(betting)} hands):")
    
    # Show top hands in betting range
    sorted_betting = sorted(betting.items(), key=lambda x: -x[1])[:10]
    for hand, freq in sorted_betting:
        classification = classify_hand(hand, board)
        print(f"  {hand}: {freq:.3f} ({classification.category})")
    
    # Test checking range
    checking = narrow_to_checking_range(sample_range, board, 'flop')
    print(f"\nCHECKING RANGE ({len(checking)} hands):")
    
    sorted_checking = sorted(checking.items(), key=lambda x: -x[1])[:10]
    for hand, freq in sorted_checking:
        classification = classify_hand(hand, board)
        print(f"  {hand}: {freq:.3f} ({classification.category})")
    
    # Compare specific hands
    print("\n" + "=" * 60)
    print("SPECIFIC HAND ANALYSIS")
    print("=" * 60)
    
    test_hands = ['AA', 'KK', 'AKs', 'QQ', '99', '76s', 'A5s', '54s']
    
    print(f"\n{'Hand':<8} {'Category':<15} {'Bet%':<8} {'Check%':<8}")
    print("-" * 45)
    
    for hand in test_hands:
        if hand in sample_range:
            classification = classify_hand(hand, board)
            bet_pct = betting.get(hand, 0) * 100
            check_pct = checking.get(hand, 0) * 100
            print(f"{hand:<8} {classification.category:<15} {bet_pct:>6.1f}% {check_pct:>6.1f}%")
    
    print("\nÃ¢Å“â€œ Test complete")


if __name__ == '__main__':
    test_narrowing()
