"""
Raw Equity Calculator - Smart Dispatch (Enumeration + Monte Carlo)
===================================================================

Unified equity calculation with configurable accuracy/speed tradeoff.

Modes:
- 'auto' (default): Best balance of speed and accuracy
- 'fast': Monte Carlo for all streets (fastest, ~50ms)
- 'exact': Full enumeration for postflop (slowest, most accurate)

Street-specific methods:
- Preflop: Always Monte Carlo (too many unknowns)
- Flop: Monte Carlo (fast) or Enumeration (exact)
- Turn: Enumeration (46 runouts, fast enough)
- River: Direct evaluation (instant)

Performance:
    Mode    | Flop   | Turn  | River | Total
    --------|--------|-------|-------|-------
    fast    | ~50ms  | ~10ms | ~2ms  | ~62ms
    auto    | ~50ms  | ~10ms | ~2ms  | ~62ms  
    exact   | ~800ms | ~10ms | ~2ms  | ~812ms

GTO Theory:
    Raw equity = probability of winning if we run out all remaining cards.
    
    Complete enumeration gives exact answers but is slow for flop.
    Monte Carlo sampling is fast with acceptable accuracy (~1% variance).

References:
    - PokerCruncher: "Complete enumeration for postflop scenarios"
    - Equilab: "Enumerate All vs Monte Carlo"
    - "Mathematics of Poker" (Chen, Ankenman, 2006)
"""

import sys
sys.path.insert(0, '/mnt/project')

from typing import Dict, List, Optional, Tuple
import random
import eval7
from equity_types import RawEquity
from hand_categories import RANKS, SUITS


# ============================================================================
# Fast Hand Evaluation Helpers (using eval7 Cython library)
# ============================================================================

def _to_eval7_cards(card_strings: List[str]) -> List[eval7.Card]:
    """Convert card strings like ['As', 'Kd'] to eval7.Card objects."""
    return [eval7.Card(c) for c in card_strings]


def _compare_hands_fast(
    hero_hand: List[str],
    villain_hand: List[str], 
    board: List[str],
    board_cards_cached: Optional[List[eval7.Card]] = None
) -> int:
    """
    Fast hand comparison using eval7 (22x faster than hand_evaluator.py).
    
    Args:
        hero_hand: Hero's hole cards
        villain_hand: Villain's hole cards
        board: Board cards
        board_cards_cached: Pre-converted board cards (performance optimization)
    
    Returns:
        1 if hero wins, 0 if tie, -1 if villain wins
    
    Performance: 0.54ÃŽÂ¼s vs 11.8ÃŽÂ¼s (hand_evaluator.py)
    """
    if board_cards_cached is None:
        board_cards_cached = _to_eval7_cards(board)
    
    hero_hole = _to_eval7_cards(hero_hand)
    villain_hole = _to_eval7_cards(villain_hand)
    
    hero_value = eval7.evaluate(hero_hole + board_cards_cached)
    villain_value = eval7.evaluate(villain_hole + board_cards_cached)
    
    # eval7 uses HIGHER values for BETTER hands
    if hero_value > villain_value:
        return 1  # Hero wins
    elif hero_value < villain_value:
        return -1  # Villain wins
    else:
        return 0  # Tie


# ============================================================================
# Main Calculator Class
# ============================================================================

class RawEquityCalculator:
    """
    Smart equity calculator with configurable accuracy/speed tradeoff.
    
    Modes:
        'auto': Best balance (Monte Carlo for flop, enumeration for turn/river)
        'fast': Monte Carlo everywhere (fastest)
        'exact': Full enumeration (most accurate, slowest for flop)
    
    Usage:
        calc = RawEquityCalculator()  # Default 'auto' mode
        calc = RawEquityCalculator(mode='fast')  # Fastest
        calc = RawEquityCalculator(mode='exact')  # Most accurate
        
        equity = calc.calculate(hero_hand, villain_range, board)
    """
    
    def __init__(self, mode: str = 'auto'):
        """
        Initialize calculator with specified mode.
        
        Args:
            mode: 'auto', 'fast', or 'exact'
        """
        if mode not in ('auto', 'fast', 'exact'):
            raise ValueError(f"Invalid mode '{mode}'. Use 'auto', 'fast', or 'exact'.")
        self.mode = mode
    
    def calculate(
        self,
        hero_hand: List[str],
        villain_range: Dict[str, float],
        board: List[str],
        trials: int = 500,
    ) -> RawEquity:
        """
        Calculate raw equity using optimal method for current street and mode.
        
        Smart dispatch:
        - River (5 cards): Direct evaluation (all modes)
        - Turn (4 cards): Enumerate 46 rivers (all modes)
        - Flop (3 cards): Monte Carlo (auto/fast) or Enumeration (exact)
        - Preflop (0 cards): Monte Carlo (all modes)
        
        Args:
            hero_hand: Hero's hole cards ['As', 'Kd']
            villain_range: Villain's range {hand: frequency}
            board: Board cards (0-5 cards)
            trials: Number of Monte Carlo trials
        
        Returns:
            RawEquity with win/tie/lose rates
        """
        num_board_cards = len(board)
        
        if num_board_cards >= 5:
            # River - direct evaluation (instant)
            return self._calculate_river_equity(hero_hand, villain_range, board)
        
        elif num_board_cards == 4:
            # Turn - enumerate 46 possible rivers (fast enough for all modes)
            return self._calculate_turn_equity_enum(hero_hand, villain_range, board)
        
        elif num_board_cards == 3:
            # Flop - method depends on mode
            if self.mode == 'exact':
                return self._calculate_flop_equity_enum(hero_hand, villain_range, board)
            else:
                # 'auto' and 'fast' use Monte Carlo for flop
                return self._calculate_flop_equity_mc(hero_hand, villain_range, board, trials)
        
        else:
            # Preflop - Monte Carlo (too many combos to enumerate)
            return self._calculate_preflop_equity_mc(hero_hand, villain_range, board, trials)
    
    # ========================================================================
    # River: Direct Evaluation
    # ========================================================================
    
    def _calculate_river_equity(
        self,
        hero_hand: List[str],
        villain_range: Dict[str, float],
        board: List[str],
    ) -> RawEquity:
        """Calculate river equity by direct evaluation against all villain hands."""
        hero_set = set(hero_hand)
        board_set = set(board)
        used_cards = hero_set | board_set
        
        board_cached = _to_eval7_cards(board)
        
        wins = 0.0
        ties = 0.0
        total = 0.0
        
        for hand_str, freq in villain_range.items():
            if freq <= 0:
                continue
            
            combos = self._get_valid_combos(hand_str, used_cards)
            for v_combo in combos:
                result = _compare_hands_fast(hero_hand, v_combo, board, board_cached)
                
                if result == 1:
                    wins += freq
                elif result == 0:
                    ties += freq
                total += freq
        
        if total > 0:
            win_rate = wins / total
            tie_rate = ties / total
            lose_rate = 1.0 - win_rate - tie_rate
            equity = win_rate + tie_rate / 2.0
        else:
            win_rate, tie_rate, lose_rate, equity = 0.5, 0.0, 0.5, 0.5
        
        return RawEquity(
            equity=max(0.0, min(1.0, equity)),
            win_rate=max(0.0, min(1.0, win_rate)),
            tie_rate=max(0.0, min(1.0, tie_rate)),
            lose_rate=max(0.0, min(1.0, lose_rate)),
            method='exact',
            samples=1,
            villain_combos=len(villain_range),
        )
    
    # ========================================================================
    # Turn: Enumeration (46 rivers)
    # ========================================================================
    
    def _calculate_turn_equity_enum(
        self,
        hero_hand: List[str],
        villain_range: Dict[str, float],
        board: List[str],
    ) -> RawEquity:
        """Calculate turn equity by enumerating all 46 possible rivers."""
        hero_set = set(hero_hand)
        board_set = set(board)
        used_cards = hero_set | board_set
        
        all_cards = [f"{rank}{suit}" for rank in RANKS for suit in SUITS]
        remaining_deck = [c for c in all_cards if c not in used_cards]
        
        # Pre-filter villain range
        valid_villain = self._prefilter_villain_range(villain_range, used_cards)
        
        if not valid_villain:
            return RawEquity(
                equity=0.50, win_rate=0.50, tie_rate=0.0, lose_rate=0.50,
                method='fallback', samples=0, villain_combos=0
            )
        
        total_wins = 0.0
        total_ties = 0.0
        total_weight = 0.0
        
        # Enumerate all 46 possible rivers
        for river in remaining_deck:
            final_board = board + [river]
            board_cached = _to_eval7_cards(final_board)
            river_set = {river}
            
            runout_wins = 0.0
            runout_ties = 0.0
            runout_weight = 0.0
            
            for hand_str, freq, combos in valid_villain:
                valid_count = 0
                combo_wins = 0
                combo_ties = 0
                
                for v_combo in combos:
                    if set(v_combo) & river_set:
                        continue
                    
                    valid_count += 1
                    result = _compare_hands_fast(hero_hand, v_combo, final_board, board_cached)
                    
                    if result == 1:
                        combo_wins += 1
                    elif result == 0:
                        combo_ties += 1
                
                if valid_count > 0:
                    combo_weight = freq * valid_count
                    runout_wins += (combo_wins / valid_count) * combo_weight
                    runout_ties += (combo_ties / valid_count) * combo_weight
                    runout_weight += combo_weight
            
            if runout_weight > 0:
                total_wins += runout_wins / runout_weight
                total_ties += runout_ties / runout_weight
                total_weight += 1
        
        if total_weight > 0:
            win_rate = total_wins / total_weight
            tie_rate = total_ties / total_weight
            lose_rate = 1.0 - win_rate - tie_rate
            equity = win_rate + tie_rate / 2.0
        else:
            win_rate, tie_rate, lose_rate, equity = 0.5, 0.0, 0.5, 0.5
        
        return RawEquity(
            equity=max(0.0, min(1.0, equity)),
            win_rate=max(0.0, min(1.0, win_rate)),
            tie_rate=max(0.0, min(1.0, tie_rate)),
            lose_rate=max(0.0, min(1.0, lose_rate)),
            method='enumeration',
            samples=len(remaining_deck),
            villain_combos=len(valid_villain),
        )
    
    # ========================================================================
    # Flop: Monte Carlo (fast mode)
    # ========================================================================
    
    def _calculate_flop_equity_mc(
        self,
        hero_hand: List[str],
        villain_range: Dict[str, float],
        board: List[str],
        trials: int,
    ) -> RawEquity:
        """
        Calculate flop equity using Monte Carlo sampling of runouts.
        
        Sample runouts but evaluate against FULL villain range.
        With 150 runout samples Ãƒâ€” full range = ~50ms (vs ~800ms enumeration)
        """
        hero_set = set(hero_hand)
        board_set = set(board)
        used_cards = hero_set | board_set
        
        all_cards = [f"{rank}{suit}" for rank in RANKS for suit in SUITS]
        remaining_deck = [c for c in all_cards if c not in used_cards]
        
        # Pre-filter villain range
        valid_villain_hands = self._prefilter_villain_range(villain_range, used_cards)
        
        if not valid_villain_hands:
            return RawEquity(
                equity=0.50, win_rate=0.50, tie_rate=0.0, lose_rate=0.50,
                method='fallback', samples=0, villain_combos=0
            )
        
        # Sample runouts but evaluate against FULL range
        num_runouts = min(trials, 150)
        
        total_wins = 0.0
        total_ties = 0.0
        total_samples = 0
        
        for _ in range(num_runouts):
            # Sample random turn + river
            runout = random.sample(remaining_deck, 2)
            runout_set = set(runout)
            final_board = board + runout
            board_cached = _to_eval7_cards(final_board)
            
            # Evaluate against FULL villain range
            runout_wins = 0.0
            runout_ties = 0.0
            runout_weight = 0.0
            
            for hand_str, freq, combos in valid_villain_hands:
                valid_count = 0
                combo_wins = 0
                combo_ties = 0
                
                for v_combo in combos:
                    if set(v_combo) & runout_set:
                        continue
                    
                    valid_count += 1
                    result = _compare_hands_fast(hero_hand, v_combo, final_board, board_cached)
                    
                    if result == 1:
                        combo_wins += 1
                    elif result == 0:
                        combo_ties += 1
                
                if valid_count > 0:
                    combo_weight = freq * valid_count
                    runout_wins += (combo_wins / valid_count) * combo_weight
                    runout_ties += (combo_ties / valid_count) * combo_weight
                    runout_weight += combo_weight
            
            if runout_weight > 0:
                total_wins += runout_wins / runout_weight
                total_ties += runout_ties / runout_weight
                total_samples += 1
        
        if total_samples > 0:
            win_rate = total_wins / total_samples
            tie_rate = total_ties / total_samples
            lose_rate = 1.0 - win_rate - tie_rate
            equity = win_rate + tie_rate / 2.0
        else:
            win_rate, tie_rate, lose_rate, equity = 0.5, 0.0, 0.5, 0.5
        
        return RawEquity(
            equity=max(0.0, min(1.0, equity)),
            win_rate=max(0.0, min(1.0, win_rate)),
            tie_rate=max(0.0, min(1.0, tie_rate)),
            lose_rate=max(0.0, min(1.0, lose_rate)),
            method='monte_carlo',
            samples=total_samples,
            villain_combos=len(valid_villain_hands),
        )
    
    # ========================================================================
    # Flop: Full Enumeration (exact mode)
    # ========================================================================
    
    def _calculate_flop_equity_enum(
        self,
        hero_hand: List[str],
        villain_range: Dict[str, float],
        board: List[str],
    ) -> RawEquity:
        """
        Calculate flop equity by enumerating ALL turn/river combinations.
        
        Flop enumeration:
        - 47 unknown cards remain
        - C(47, 2) = 1,081 possible turn/river combinations
        - For each combo: evaluate vs all villain hands
        
        Slow (~800ms) but 100% accurate.
        """
        hero_set = set(hero_hand)
        board_set = set(board)
        used_cards = hero_set | board_set
        
        all_cards = [f"{rank}{suit}" for rank in RANKS for suit in SUITS]
        remaining_deck = [c for c in all_cards if c not in used_cards]
        
        # Pre-filter villain range
        valid_villain_combos = self._prefilter_villain_range(villain_range, used_cards)
        
        if not valid_villain_combos:
            return RawEquity(
                equity=0.50, win_rate=0.50, tie_rate=0.0, lose_rate=0.50,
                method='fallback', samples=0, villain_combos=0
            )
        
        total_wins = 0.0
        total_ties = 0.0
        total_weight = 0.0
        runout_count = 0
        
        # Enumerate all turn/river combinations
        for i, turn in enumerate(remaining_deck):
            for river in remaining_deck[i+1:]:
                runout_count += 1
                final_board = board + [turn, river]
                board_cached = _to_eval7_cards(final_board)
                runout_set = {turn, river}
                
                runout_wins = 0.0
                runout_ties = 0.0
                runout_weight = 0.0
                
                for hand_str, freq, combos in valid_villain_combos:
                    valid_count = 0
                    combo_wins = 0
                    combo_ties = 0
                    
                    for v_combo in combos:
                        if set(v_combo) & runout_set:
                            continue
                        
                        valid_count += 1
                        result = _compare_hands_fast(hero_hand, v_combo, final_board, board_cached)
                        
                        if result == 1:
                            combo_wins += 1
                        elif result == 0:
                            combo_ties += 1
                    
                    if valid_count > 0:
                        combo_weight = freq * valid_count
                        runout_wins += (combo_wins / valid_count) * combo_weight
                        runout_ties += (combo_ties / valid_count) * combo_weight
                        runout_weight += combo_weight
                
                if runout_weight > 0:
                    total_wins += runout_wins / runout_weight
                    total_ties += runout_ties / runout_weight
                    total_weight += 1
        
        if total_weight > 0:
            win_rate = total_wins / total_weight
            tie_rate = total_ties / total_weight
            lose_rate = 1.0 - win_rate - tie_rate
            equity = win_rate + tie_rate / 2.0
        else:
            win_rate, tie_rate, lose_rate, equity = 0.5, 0.0, 0.5, 0.5
        
        return RawEquity(
            equity=max(0.0, min(1.0, equity)),
            win_rate=max(0.0, min(1.0, win_rate)),
            tie_rate=max(0.0, min(1.0, tie_rate)),
            lose_rate=max(0.0, min(1.0, lose_rate)),
            method='enumeration',
            samples=runout_count,
            villain_combos=len(valid_villain_combos),
        )
    
    # ========================================================================
    # Preflop: Monte Carlo
    # ========================================================================
    
    def _calculate_preflop_equity_mc(
        self,
        hero_hand: List[str],
        villain_range: Dict[str, float],
        board: List[str],
        trials: int,
    ) -> RawEquity:
        """Monte Carlo for preflop equity."""
        hero_set = set(hero_hand)
        all_cards = [f"{rank}{suit}" for rank in RANKS for suit in SUITS]
        remaining_deck = [c for c in all_cards if c not in hero_set]
        
        # Pre-filter villain range
        valid_villain_hands = []
        total_weight = 0.0
        
        for hand_str, freq in villain_range.items():
            if freq <= 0:
                continue
            combos = self._get_valid_combos(hand_str, hero_set)
            if combos:
                valid_villain_hands.append((hand_str, freq, combos))
                total_weight += freq * len(combos)
        
        if not valid_villain_hands:
            return RawEquity(
                equity=0.50, win_rate=0.50, tie_rate=0.0, lose_rate=0.50,
                method='fallback', samples=0, villain_combos=0
            )
        
        wins = 0.0
        ties = 0.0
        samples = 0
        
        for _ in range(trials):
            # Random 5-card board
            runout = random.sample(remaining_deck, 5)
            runout_set = set(runout)
            board_cached = _to_eval7_cards(runout)
            
            # Sample villain hand
            villain_hand = self._sample_villain_hand(valid_villain_hands, total_weight, runout_set)
            if villain_hand is None:
                continue
            
            result = _compare_hands_fast(hero_hand, villain_hand, runout, board_cached)
            samples += 1
            
            if result == 1:
                wins += 1
            elif result == 0:
                ties += 1
        
        if samples > 0:
            win_rate = wins / samples
            tie_rate = ties / samples
            lose_rate = 1.0 - win_rate - tie_rate
            equity = win_rate + tie_rate / 2.0
        else:
            win_rate, tie_rate, lose_rate, equity = 0.5, 0.0, 0.5, 0.5
        
        return RawEquity(
            equity=max(0.0, min(1.0, equity)),
            win_rate=max(0.0, min(1.0, win_rate)),
            tie_rate=max(0.0, min(1.0, tie_rate)),
            lose_rate=max(0.0, min(1.0, lose_rate)),
            method='monte_carlo',
            samples=samples,
            villain_combos=len(valid_villain_hands),
        )
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def _sample_villain_hand(
        self,
        valid_hands: List[Tuple[str, float, List]],
        total_weight: float,
        avoid_cards: set,
    ) -> Optional[List[str]]:
        """Sample a random villain hand, avoiding card collisions."""
        for _ in range(10):  # Up to 10 attempts
            r = random.random() * total_weight
            cumulative = 0.0
            
            for hand_str, freq, combos in valid_hands:
                weight = freq * len(combos)
                cumulative += weight
                if cumulative >= r:
                    valid_combos = [c for c in combos if not (set(c) & avoid_cards)]
                    if valid_combos:
                        return random.choice(valid_combos)
                    break
        
        return None
    
    def _prefilter_villain_range(
        self,
        villain_range: Dict[str, float],
        used_cards: set,
    ) -> List[Tuple[str, float, List[List[str]]]]:
        """Pre-filter villain range to remove impossible combos."""
        filtered = []
        
        for v_hand, freq in villain_range.items():
            if freq <= 0:
                continue
            
            combos = self._get_valid_combos(v_hand, used_cards)
            if combos:
                filtered.append((v_hand, freq, combos))
        
        return filtered
    
    def _get_valid_combos(self, hand: str, used_cards: set) -> List[List[str]]:
        """Get all valid card combinations for a hand notation."""
        if len(hand) < 2:
            return []
        
        rank1 = hand[0]
        rank2 = hand[1]
        used_lower = {c.lower() for c in used_cards}
        
        combos = []
        
        if rank1 == rank2:
            # Pair - 6 combos max
            for i, s1 in enumerate(SUITS):
                for s2 in SUITS[i+1:]:
                    c1, c2 = f"{rank1}{s1}", f"{rank2}{s2}"
                    if c1.lower() not in used_lower and c2.lower() not in used_lower:
                        combos.append([c1, c2])
        
        elif len(hand) >= 3 and hand[2].lower() == 's':
            # Suited - 4 combos max
            for s in SUITS:
                c1, c2 = f"{rank1}{s}", f"{rank2}{s}"
                if c1.lower() not in used_lower and c2.lower() not in used_lower:
                    combos.append([c1, c2])
        
        else:
            # Offsuit - 12 combos max
            for s1 in SUITS:
                for s2 in SUITS:
                    if s1 != s2:
                        c1, c2 = f"{rank1}{s1}", f"{rank2}{s2}"
                        if c1.lower() not in used_lower and c2.lower() not in used_lower:
                            combos.append([c1, c2])
        
        return combos


# ============================================================================
# Backward Compatibility Alias
# ============================================================================

# For any code that imported RawEquityCalculatorFast
RawEquityCalculatorFast = RawEquityCalculator


# ============================================================================
# Testing
# ============================================================================

if __name__ == "__main__":
    import time
    
    print("=" * 70)
    print("RAW EQUITY CALCULATOR - UNIFIED VERSION")
    print("=" * 70)
    
    # Import test data
    from range_manager import RangeManager
    range_mgr = RangeManager()
    villain_range = range_mgr.get_rfi_range('BTN')
    
    # Test cases
    test_cases = [
        (['As', 'Ah'], ['Ks', '7h', '2d'], 'Flop'),
        (['As', 'Kd'], ['Ks', '7h', '2d', 'Jc'], 'Turn'),
        (['9s', '9h'], ['Ks', '7h', '2d', '3c', '8h'], 'River'),
    ]
    
    # Test each mode
    for mode in ['auto', 'fast', 'exact']:
        print(f"\n{'='*70}")
        print(f"MODE: {mode.upper()}")
        print(f"{'='*70}")
        
        calc = RawEquityCalculator(mode=mode)
        
        for hero, board, street in test_cases:
            times = []
            result = None
            
            for _ in range(3):
                start = time.time()
                result = calc.calculate(hero, villain_range, board, trials=500)
                elapsed = (time.time() - start) * 1000
                times.append(elapsed)
            
            avg_time = sum(times) / len(times)
            print(f"\n{street}: {hero[0]}{hero[1]} on {'-'.join(board)}")
            print(f"  Equity: {result.equity:.1%}")
            print(f"  Method: {result.method}")
            print(f"  Time: {avg_time:.1f}ms")
    
    # Performance comparison
    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON - FLOP EQUITY")
    print("=" * 70)
    
    hero = ['As', 'Ah']
    board = ['Ks', '7h', '2d']
    
    for mode in ['fast', 'exact']:
        calc = RawEquityCalculator(mode=mode)
        
        times = []
        for _ in range(3):
            start = time.time()
            result = calc.calculate(hero, villain_range, board)
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
        
        avg = sum(times) / len(times)
        print(f"\n{mode.upper():6} mode:")
        print(f"  Time: {avg:.0f}ms")
        print(f"  Equity: {result.equity:.3f}")
        print(f"  Method: {result.method}")
    
    print("\n" + "=" * 70)
    print("Ã¢Å“â€œ Unified raw_equity.py working!")
    print("=" * 70)
