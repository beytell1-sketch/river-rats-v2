"""
Hand Evaluator - Absolute Hand Strength Analysis
================================================================================

Evaluates made hands and draws on a given board.

Determines what poker hand we have (pair, two pair, straight, etc.) and
calculates absolute hand strength. Complements range-based analysis by
providing concrete hand strength evaluation.

GTO Requires BOTH:
    1. Range-relative position (where in our range?) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ range_manager.py
    2. Absolute hand strength (what do we have?) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ THIS MODULE

Core Functionality:
    - Hand Category: High card, pair, two pair, trips, etc.
    - Hand Rank: Numeric strength score [0, 8+]
    - Made Hand Detection: Do we have showdown value?
    - Draw Detection: Flush draws, straight draws, combo draws
    - Nut Status: Do we have the best possible hand?

Hand Rankings (0-8):
    0 = High card (worst)
    1 = Pair
    2 = Two pair
    3 = Trips/Set
    4 = Straight
    5 = Flush
    6 = Full house
    7 = Quads
    8 = Straight flush (best)

Architecture:
    - HandEvaluation dataclass: Complete evaluation result
    - evaluate_hand(): Main entry point
    - Helper functions: Pair detection, draw detection, nut evaluation

Performance:
    - Fast: O(n) where n = cards (2 hole + board)
    - Cached: Results can be memoized per hand/board combo
    - Mobile-ready: < 1ms per evaluation

Usage:
    >>> from hand_evaluator import evaluate_hand
    >>> hole_cards = ['Qs', 'Js']
    >>> board = ['Ts', '9h', '8d']
    >>> eval = evaluate_hand(hole_cards, board)
    >>> eval.category  # 'straight'
    >>> eval.rank  # 4.0 (straight rank)
    >>> eval.is_monster  # True (trips+)
    >>> eval.made_hand_strength  # 0.85 (normalized strength)

Output:
    HandEvaluation dataclass containing:
        - category: 'pair', 'two_pair', 'straight', etc.
        - rank: Numeric rank [0, 8+]
        - description: Human-readable description
        - made_hand_strength: Normalized strength [0, 1]
        - is_made_hand: Have pair or better?
        - is_strong_made: Have two pair or better?
        - is_monster: Have trips or better?
        - has_flush_draw: Flush draw present?
        - has_straight_draw: Straight draw present?
        - draw_outs: Number of outs to improve
        - draw_equity: Estimated equity from draws

Applications:
    - Value betting: Strong made hands bet for value
    - Bluff catching: Decent made hands call down
    - Draw play: Semi-bluff with strong draws
    - Pot control: Check back marginal made hands

Notes:
    - Uses shared hand_categories module for consistency
    - Considers kicker strength for pairs
    - Evaluates nut potential (best possible hand)
    - Integrated throughout Oracle decision logic

See Also:
    - hand_categories.py: Hand classification utilities
    - range_manager.py: Range-relative percentiles
    - board_analyzer.py: Board texture analysis
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass

# Import shared constants and functions from hand_categories
from hand_categories import (
    RANK_VALUES,
    CATEGORY_BASE,
    HAND_CATEGORY_VALUES,
    check_straight,
    rank_name,
    is_monster as category_is_monster,
    is_strong_made as category_is_strong_made,
    is_made_hand as category_is_made_hand,
)


@dataclass
class HandEvaluation:
    """Complete hand evaluation result."""
    category: str              # e.g., "flush", "top_pair", "straight"
    rank: float               # 0-8+ scale
    description: str          # Human readable
    made_hand_strength: float # 0-1 normalized strength
    
    # Components
    is_made_hand: bool        # Do we have pair or better?
    is_strong_made: bool      # Do we have two pair or better?
    is_monster: bool          # Do we have trips or better?
    
    # Draw info
    has_flush_draw: bool
    has_straight_draw: bool
    draw_outs: int
    draw_equity: float
    
    def to_dict(self) -> dict:
        """Convert to minimal dict for Oracle diagnostics."""
        return {
            "category": self.category,
            "strength": self.made_hand_strength,
            "is_made": self.is_made_hand,
            "is_strong": self.is_strong_made,
            "is_monster": self.is_monster,
            "draw_outs": self.draw_outs,
            "draw_equity": self.draw_equity,
        }


def evaluate_hand(hole_cards: List[str], board: List[str]) -> HandEvaluation:
    """
    Evaluate a hand on a board.
    
    Args:
        hole_cards: Specific cards like ["Qs", "Js"]
        board: Board cards like ["Ts", "9h", "8d", "5c", "2s"]
    
    Returns:
        HandEvaluation with complete analysis
    """
    if not board:
        return _evaluate_preflop(hole_cards)
    
    all_cards = hole_cards + board
    
    # Parse cards
    hole_ranks = [RANK_VALUES.get(c[0].upper(), 0) for c in hole_cards]
    hole_suits = [c[1].lower() for c in hole_cards]
    board_ranks = [RANK_VALUES.get(c[0].upper(), 0) for c in board]
    board_suits = [c[1].lower() for c in board]
    all_ranks = hole_ranks + board_ranks
    all_suits = hole_suits + board_suits
    
    # Count ranks and suits
    rank_counts = {}
    for r in all_ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1
    
    suit_counts = {}
    for s in all_suits:
        suit_counts[s] = suit_counts.get(s, 0) + 1
    
    # Check for flush
    flush_suit = None
    for s, count in suit_counts.items():
        if count >= 5:
            flush_suit = s
            break
    
    # Check if WE have the flush
    we_have_flush = False
    our_flush_cards = []
    if flush_suit:
        our_flush_cards = [RANK_VALUES.get(c[0].upper(), 0) for c in hole_cards if c[1].lower() == flush_suit]
        we_have_flush = len(our_flush_cards) >= 1 and suit_counts[flush_suit] >= 5
    
    # Check for straight using shared function
    unique_ranks = sorted(set(all_ranks), reverse=True)
    straight_high = check_straight(all_ranks)
    
    # Check if WE make the straight
    we_have_straight = False
    if straight_high:
        straight_ranks = set(range(straight_high - 4, straight_high + 1))
        if straight_high == 5:  # Wheel
            straight_ranks = {14, 2, 3, 4, 5}
        our_contribution = sum(1 for r in hole_ranks if r in straight_ranks or (r == 14 and 1 in straight_ranks))
        we_have_straight = our_contribution >= 1
    
    # =========================================================================
    # EARLY DRAW DETECTION (Bug Fix: combo draws were ignored for made hands)
    # Calculate draws BEFORE evaluating made hands so we can include them
    # =========================================================================
    has_fd, fd_outs = _check_flush_draw(hole_cards, board)
    has_sd, sd_outs = _check_straight_draw(hole_ranks, board_ranks)
    total_draw_outs = fd_outs + sd_outs
    # Cap draw equity at 45% (roughly 20 outs)
    total_draw_equity = min(0.45, total_draw_outs * 0.02)
    
    # Straight flush
    if flush_suit and straight_high:
        flush_ranks = sorted([RANK_VALUES.get(c[0].upper(), 0) for c in all_cards if c[1].lower() == flush_suit], reverse=True)
        sf_high = check_straight(flush_ranks)
        if sf_high and we_have_flush:
            return HandEvaluation(
                category='straight_flush', rank=8.0 + sf_high / 100,
                description=f"Straight flush, {rank_name(sf_high)} high",
                made_hand_strength=0.99,
                is_made_hand=True, is_strong_made=True, is_monster=True,
                has_flush_draw=False, has_straight_draw=False, draw_outs=0, draw_equity=0
            )
    
    # Quads
    quads = [r for r, c in rank_counts.items() if c == 4]
    if quads:
        we_have_quads = any(r in hole_ranks for r in quads)
        if we_have_quads:
            return HandEvaluation(
                category='quads', rank=7.0 + quads[0] / 100,
                description=f"Quad {rank_name(quads[0])}s",
                made_hand_strength=0.98,
                is_made_hand=True, is_strong_made=True, is_monster=True,
                has_flush_draw=False, has_straight_draw=False, draw_outs=0, draw_equity=0
            )
    
    # Full house
    trips = [r for r, c in rank_counts.items() if c >= 3]
    pairs = [r for r, c in rank_counts.items() if c == 2]
    
    if trips and (pairs or len(trips) > 1):
        trip_rank = max(trips)
        pair_rank = max([r for r in pairs + trips if r != trip_rank], default=0)
        we_have_trips_part = hole_ranks.count(trip_rank) >= 1 or (hole_ranks[0] == hole_ranks[1] and hole_ranks[0] == trip_rank)
        
        if we_have_trips_part:
            return HandEvaluation(
                category='full_house', rank=6.0 + trip_rank / 20 + pair_rank / 400,
                description=f"Full house, {rank_name(trip_rank)}s full of {rank_name(pair_rank)}s",
                made_hand_strength=0.95,
                is_made_hand=True, is_strong_made=True, is_monster=True,
                has_flush_draw=False, has_straight_draw=False, draw_outs=0, draw_equity=0
            )
    
    # Flush
    if we_have_flush:
        high_flush_card = max(our_flush_cards)
        is_nut = high_flush_card == 14
        
        # FIX: Check if flush is actually a monster
        # Count flush cards on board (dangerous if 4+)
        board_flush_count = sum(1 for c in board if c[1].lower() == flush_suit)
        
        # Check if board is paired (full house possible)
        board_rank_counts = {}
        for r in board_ranks:
            board_rank_counts[r] = board_rank_counts.get(r, 0) + 1
        board_is_paired = any(c >= 2 for c in board_rank_counts.values())
        
        # Determine if this flush is actually a monster:
        # - NOT monster if board has 4+ flush cards (too easy to beat)
        # - NOT monster if our high card is J or lower (weak flush)
        # - Downgrade if board is paired (full house possible)
        # - Monster only if Q+ high flush on 3-flush board
        
        if board_flush_count >= 4:
            # 4-flush board: only nut flush is monster
            is_monster = is_nut
            is_strong = high_flush_card >= 12  # Q+ is still strong
            strength = 0.92 if is_nut else (0.82 if high_flush_card >= 12 else 0.70)
        elif board_is_paired:
            # Paired board: flush loses to full house
            is_monster = is_nut  # Only nut flush is monster
            is_strong = True
            strength = 0.88 if is_nut else 0.80
        else:
            # Normal 3-flush board
            is_monster = high_flush_card >= 12  # Q+ high is monster
            is_strong = True
            strength = 0.90 if is_nut else (0.85 if high_flush_card >= 12 else 0.78)
        
        return HandEvaluation(
            category='flush', rank=5.0 + high_flush_card / 100,
            description=f"Flush, {rank_name(high_flush_card)} high" + (" (nut)" if is_nut else ""),
            made_hand_strength=strength,
            is_made_hand=True, is_strong_made=is_strong, is_monster=is_monster,
            has_flush_draw=False, has_straight_draw=False, draw_outs=0, draw_equity=0
        )
    
    # Straight
    if we_have_straight:
        is_nut = straight_high == max(unique_ranks) or straight_high == 14
        return HandEvaluation(
            category='straight', rank=4.0 + straight_high / 100,
            description=f"Straight, {rank_name(straight_high)} high",
            made_hand_strength=0.82 if is_nut else 0.78,
            is_made_hand=True, is_strong_made=True, is_monster=True,
            has_flush_draw=False, has_straight_draw=False, draw_outs=0, draw_equity=0
        )
    
    # Set/Trips
    if trips:
        trip_rank = max(trips)
        we_have_set = hole_ranks[0] == hole_ranks[1] and hole_ranks[0] == trip_rank
        we_have_trips = not we_have_set and trip_rank in hole_ranks
        
        if we_have_set:
            return HandEvaluation(
                category='set', rank=3.5 + trip_rank / 100,
                description=f"Set of {rank_name(trip_rank)}s",
                made_hand_strength=0.80,
                is_made_hand=True, is_strong_made=True, is_monster=True,
                has_flush_draw=has_fd, has_straight_draw=has_sd,
                draw_outs=total_draw_outs, draw_equity=total_draw_equity
            )
        elif we_have_trips:
            return HandEvaluation(
                category='trips', rank=3.0 + trip_rank / 100,
                description=f"Trip {rank_name(trip_rank)}s",
                made_hand_strength=0.75,
                is_made_hand=True, is_strong_made=True, is_monster=True,
                has_flush_draw=has_fd, has_straight_draw=has_sd,
                draw_outs=total_draw_outs, draw_equity=total_draw_equity
            )
    
    # Two pair
    all_pairs = [r for r, c in rank_counts.items() if c >= 2]
    if len(all_pairs) >= 2:
        top_pairs = sorted(all_pairs, reverse=True)[:2]
        
        # FIX: Hero must actually contribute to TWO pairs, not just match one
        # Case 1: Hero has pocket pair that's one of the pairs, AND board has another pair
        # Case 2: Hero's two cards each pair with the board (both hole cards contribute)
        
        is_pocket_pair = hole_ranks[0] == hole_ranks[1]
        
        if is_pocket_pair:
            # Pocket pair + board pair = two pair only if our pair is one of top 2
            if hole_ranks[0] in top_pairs:
                # Check there's a BOARD pair (not our pocket pair creating both)
                board_pairs = [r for r, c in {r: board_ranks.count(r) for r in board_ranks}.items() if c >= 2]
                if board_pairs:
                    we_contribute = True
                else:
                    we_contribute = False
            else:
                we_contribute = False
        else:
            # Two unpaired hole cards
            # Count board pairs BEFORE adding hole cards
            board_pairs = [r for r, c in {r: board_ranks.count(r) for r in board_ranks}.items() if c >= 2]
            
            # Count how many hole cards pair with board
            hole_cards_that_pair = [r for r in hole_ranks if r in board_ranks]
            
            if board_pairs:
                # Board has >=1 pair: any hole card pairing with board gives us two pair
                we_contribute = len(hole_cards_that_pair) >= 1
            else:
                # Board has no pairs: need BOTH hole cards to pair with board
                we_contribute = len(hole_cards_that_pair) >= 2
        
        if we_contribute:
            return HandEvaluation(
                category='two_pair', rank=2.0 + top_pairs[0] / 20 + top_pairs[1] / 400,
                description=f"Two pair, {rank_name(top_pairs[0])}s and {rank_name(top_pairs[1])}s",
                made_hand_strength=0.68,
                is_made_hand=True, is_strong_made=True, is_monster=False,
                has_flush_draw=has_fd, has_straight_draw=has_sd,
                draw_outs=total_draw_outs, draw_equity=total_draw_equity
            )
    
    # One pair
    if all_pairs:
        board_max = max(board_ranks)
        board_min = min(board_ranks)
        is_pocket_pair = hole_ranks[0] == hole_ranks[1]
        
        # FIX: Find the pair WE actually make, not just the max pair
        # Check if we have a pocket pair that forms a pair
        if is_pocket_pair and hole_ranks[0] in all_pairs:
            pair_rank = hole_ranks[0]
            if pair_rank > board_max:
                return HandEvaluation(
                    category='overpair', rank=1.5 + pair_rank / 100,
                    description=f"Overpair, {rank_name(pair_rank)}s",
                    made_hand_strength=0.70,
                    is_made_hand=True, is_strong_made=False, is_monster=False,
                    has_flush_draw=has_fd, has_straight_draw=has_sd,
                    draw_outs=total_draw_outs, draw_equity=total_draw_equity
                )
            else:
                return HandEvaluation(
                    category='underpair', rank=0.9 + pair_rank / 100,
                    description=f"Underpair, {rank_name(pair_rank)}s",
                    made_hand_strength=0.40,
                    is_made_hand=True, is_strong_made=False, is_monster=False,
                    has_flush_draw=has_fd, has_straight_draw=has_sd,
                    draw_outs=total_draw_outs, draw_equity=total_draw_equity
                )
        
        # Check if one of our hole cards pairs with the board
        our_pairs = [r for r in hole_ranks if r in all_pairs and board_ranks.count(r) >= 1]
        if our_pairs and not is_pocket_pair:
            # Use the highest pair we actually make
            pair_rank = max(our_pairs)
            kicker = max([r for r in hole_ranks if r != pair_rank], default=0)
            
            if pair_rank == board_max:
                if kicker >= 12:
                    cat = 'top_pair_top_kicker' if kicker == 14 else 'top_pair_good_kicker'
                    strength = 0.65 if kicker == 14 else 0.60
                else:
                    cat = 'top_pair'
                    strength = 0.55
                return HandEvaluation(
                    category=cat, rank=1.2 + pair_rank / 100 + kicker / 1000,
                    description=f"Top pair {rank_name(pair_rank)}s, {rank_name(kicker)} kicker",
                    made_hand_strength=strength,
                    is_made_hand=True, is_strong_made=False, is_monster=False,
                    has_flush_draw=has_fd, has_straight_draw=has_sd,
                    draw_outs=total_draw_outs, draw_equity=total_draw_equity
                )
            elif pair_rank == board_min:
                return HandEvaluation(
                    category='bottom_pair', rank=1.0 + pair_rank / 100,
                    description=f"Bottom pair {rank_name(pair_rank)}s",
                    made_hand_strength=0.35,
                    is_made_hand=True, is_strong_made=False, is_monster=False,
                    has_flush_draw=has_fd, has_straight_draw=has_sd,
                    draw_outs=total_draw_outs, draw_equity=total_draw_equity
                )
            else:
                return HandEvaluation(
                    category='middle_pair', rank=1.1 + pair_rank / 100,
                    description=f"Middle pair {rank_name(pair_rank)}s",
                    made_hand_strength=0.40,
                    is_made_hand=True, is_strong_made=False, is_monster=False,
                    has_flush_draw=has_fd, has_straight_draw=has_sd,
                    draw_outs=total_draw_outs, draw_equity=total_draw_equity
                )
    
    # No made hand - use early-calculated draw values
    board_max = max(board_ranks)
    if hole_ranks[0] > board_max and hole_ranks[1] > board_max:
        return HandEvaluation(
            category='overcards', rank=0.3 + max(hole_ranks) / 100,
            description=f"Overcards {rank_name(hole_ranks[0])}{rank_name(hole_ranks[1])}",
            made_hand_strength=0.20,
            is_made_hand=False, is_strong_made=False, is_monster=False,
            has_flush_draw=has_fd, has_straight_draw=has_sd,
            draw_outs=total_draw_outs, draw_equity=total_draw_equity
        )
    elif hole_ranks[0] > board_max or hole_ranks[1] > board_max:
        return HandEvaluation(
            category='one_overcard', rank=0.2 + max(hole_ranks) / 100,
            description=f"One overcard",
            made_hand_strength=0.15,
            is_made_hand=False, is_strong_made=False, is_monster=False,
            has_flush_draw=has_fd, has_straight_draw=has_sd,
            draw_outs=total_draw_outs, draw_equity=total_draw_equity
        )
    else:
        return HandEvaluation(
            category='high_card', rank=0.1 + max(hole_ranks) / 100,
            description=f"High card {rank_name(max(hole_ranks))}",
            made_hand_strength=0.10,
            is_made_hand=False, is_strong_made=False, is_monster=False,
            has_flush_draw=has_fd, has_straight_draw=has_sd,
            draw_outs=total_draw_outs, draw_equity=total_draw_equity
        )


def _check_flush_draw(hole_cards: List[str], board: List[str]) -> Tuple[bool, int]:
    """Check for flush draw."""
    if len(board) >= 5:
        return False, 0
    
    all_suits = [c[1].lower() for c in hole_cards + board]
    suit_counts = {}
    for s in all_suits:
        suit_counts[s] = suit_counts.get(s, 0) + 1
    
    for s, count in suit_counts.items():
        if count == 4:
            our_suited = sum(1 for c in hole_cards if c[1].lower() == s)
            if our_suited >= 1:
                return True, 9
    return False, 0


def _check_straight_draw(hole_ranks: List[int], board_ranks: List[int]) -> Tuple[bool, int]:
    """Check for straight draw."""
    all_ranks = sorted(set(hole_ranks + board_ranks))
    if 14 in all_ranks:
        all_ranks = [1] + all_ranks
    
    for i in range(len(all_ranks)):
        for j in range(i + 1, min(i + 5, len(all_ranks))):
            window = all_ranks[i:j+1]
            if len(window) >= 4:
                span = window[-1] - window[0]
                if span == 3 and len(window) == 4:
                    return True, 8  # OESD
                elif span == 4 and len(window) == 4:
                    return True, 4  # Gutshot
    return False, 0


def _evaluate_preflop(hole_cards: List[str]) -> HandEvaluation:
    """Evaluate preflop hand."""
    ranks = [RANK_VALUES.get(c[0].upper(), 0) for c in hole_cards]
    suited = hole_cards[0][1].lower() == hole_cards[1][1].lower()
    high, low = max(ranks), min(ranks)
    
    if ranks[0] == ranks[1]:
        return HandEvaluation(
            category='pocket_pair', rank=1.0 + high / 100,
            description=f"Pocket {rank_name(high)}s",
            made_hand_strength=0.5 + high / 30,
            is_made_hand=True, is_strong_made=False, is_monster=high >= 10,
            has_flush_draw=False, has_straight_draw=False, draw_outs=0, draw_equity=0
        )
    else:
        desc = f"{rank_name(high)}{rank_name(low)}{'s' if suited else 'o'}"
        strength = (high + low) / 28 + (0.05 if suited else 0)
        return HandEvaluation(
            category='unpaired', rank=0.1 + high / 100,
            description=desc, made_hand_strength=strength,
            is_made_hand=False, is_strong_made=False, is_monster=False,
            has_flush_draw=False, has_straight_draw=False, draw_outs=0, draw_equity=0
        )


def get_hand_strength(hole_cards: List[str], board: List[str]) -> float:
    """Get normalized hand strength 0-1."""
    return evaluate_hand(hole_cards, board).made_hand_strength


if __name__ == "__main__":
    print("=== Hand Evaluator Tests ===\n")
    
    test_cases = [
        (["Qs", "Js"], ["Ts", "9h", "8d"], "straight"),
        (["As", "5s"], ["Ks", "7s", "2s"], "flush"),
        (["9s", "9h"], ["9d", "5c", "2h"], "set"),
        (["Ah", "Kd"], ["Kh", "7s", "2c"], "top_pair"),
        (["Ah", "Ad"], ["Ks", "7h", "2d"], "overpair"),
    ]
    
    for hole, board, expected in test_cases:
        result = evaluate_hand(hole, board)
        status = "ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“" if expected in result.category else "ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Ã‚Â"
        print(f"{status} {hole} on {board} ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ {result.category} ({result.description})")
