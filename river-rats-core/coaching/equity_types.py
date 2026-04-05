"""
Equity Type Definitions
=======================

Defines the four equity types required for GTO poker decision making.

GTO Theory Foundation:
    1. Raw Equity - Win probability vs full villain range
    2. Realized Equity - Adjusted for position, texture, playability
    3. Equity vs Calling Range - Win probability vs hands that call
    4. Fold Equity - Probability villain folds to our bet

These four types serve distinct purposes:
    - Raw Equity: Baseline assessment
    - Realized Equity: Used for calling decisions
    - Equity vs Calling: Used for value betting decisions
    - Fold Equity: Used for bluffing decisions

References:
    - "Applications of NLHE" (Janda, 2013) - Equity Realization
    - "Mathematics of Poker" (Chen, Ankenman, 2006) - Fold Equity
    - GTO Wizard / PioSOLVER - Modern solver approaches
"""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class RawEquity:
    """
    Type 1: Raw Equity
    
    Win probability vs villain's full range if we ran out all cards.
    This is the baseline equity calculation (Monte Carlo simulation).
    
    Attributes:
        equity: Combined win + tie/2 probability (0-1)
        win_rate: Pure win probability (0-1)
        tie_rate: Tie probability (0-1)
        lose_rate: Lose probability (0-1)
        method: Calculation method ('monte_carlo' or 'exact')
        samples: Number of trials/combinations
        villain_combos: Number of villain hand combos
        confidence_interval: 95% CI (lower, upper) if monte carlo
    
    Example:
        RawEquity(
            equity=0.72,
            win_rate=0.70,
            tie_rate=0.04,
            lose_rate=0.26,
            method='monte_carlo',
            samples=1000,
            villain_combos=142,
            confidence_interval=(0.68, 0.76)
        )
    """
    equity: float
    win_rate: float
    tie_rate: float
    lose_rate: float
    method: str
    samples: int
    villain_combos: int
    confidence_interval: Optional[Tuple[float, float]] = None
    
    def __post_init__(self):
        """Validate equity components sum to 1.0."""
        total = self.win_rate + self.tie_rate + self.lose_rate
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Equity rates must sum to 1.0, got {total}")


@dataclass(frozen=True)
class RealizedEquity:
    """
    Type 2: Realized Equity
    
    Raw equity adjusted for:
    - Position (IP realizes more, OOP realizes less)
    - Board texture (scary boards reduce realization)
    - Hand type (draws vs made hands)
    - Stack depth (SPR affects realization)
    
    Used for calling decisions: "Do I have equity to call?"
    
    Attributes:
        equity: Realized equity after adjustments (0-1)
        raw_equity: Original raw equity before adjustments
        position_factor: Position multiplier applied (0.80-1.15)
        texture_factor: Board texture multiplier (0.75-1.00)
        hand_type_factor: Hand type multiplier (0.85-1.00)
        spr_factor: SPR multiplier (0.90-1.05)
        
    GTO Theory:
        - IP realizes 105-115% of raw equity (can force folds, control pot)
        - OOP realizes 80-90% of raw equity (faces difficult decisions)
        - Scary boards reduce realization (vulnerable to bluffs)
        - Made hands realize more than draws (draws can miss)
    
    Example:
        RealizedEquity(
            equity=0.58,           # Final realized equity
            raw_equity=0.72,       # Started with 72% raw
            position_factor=0.88,  # OOP discount (ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Ã‚Â0.88)
            texture_factor=0.95,   # Dry board (ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Ã‚Â0.95)
            hand_type_factor=0.92, # Top pair weak kicker (ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Ã‚Â0.92)
            spr_factor=1.00,       # Normal SPR (ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Ã‚Â1.00)
        )
        # 0.72 ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Ã‚Â 0.88 ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Ã‚Â 0.95 ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Ã‚Â 0.92 ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Ã‚Â 1.00 = 0.552 ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â°ÃƒÆ’Ã¢â‚¬Â¹ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â  0.58
    """
    equity: float
    raw_equity: float
    position_factor: float
    texture_factor: float
    hand_type_factor: float
    spr_factor: float
    
    def __post_init__(self):
        """Validate factors are reasonable."""
        if not (0.60 <= self.position_factor <= 1.20):
            raise ValueError(f"Position factor out of range: {self.position_factor}")
        if not (0.70 <= self.texture_factor <= 1.05):
            raise ValueError(f"Texture factor out of range: {self.texture_factor}")


@dataclass(frozen=True)
class CallingRangeEquity:
    """
    Type 3: Equity vs Calling Range (ENHANCED)
    
    Win probability vs hands that call, with partition analysis.
    
    Critical for value betting: "Do I beat what CALLS me?"
    
    PARALLEL TO FOLD EQUITY:
        Fold equity cares about BETTER hands folding
        Value betting cares about WORSE hands calling
    
    The calling range consists of:
    - Worse hands calling (we beat) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ GOOD (we get value!)
    - Better hands calling (beat us) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ BAD (we lose money!)
    
    Just like fold equity, we partition to understand composition.
    
    Attributes:
        equity: Win probability vs calling range (0-1)
        raw_equity: Original equity vs full range
        calling_range_size: Fraction of range that calls (0-1)
        calling_range: Full calling range dict {hand: freq}
        bet_size_frac: Bet size that induced this calling range
        
        # ENHANCED: Calling range partition
        worse_hands_calling: Hands we beat that call {hand: freq}
        better_hands_calling: Hands that beat us that call {hand: freq}
        
        # ENHANCED: Value metrics
        value_density: % of calling range we beat (0-1)
        ev_vs_worse: EV from worse hands calling (in bb)
        ev_vs_better: EV from better hands calling (in bb)
        net_ev: Total expected value of bet (in bb)
        
        # ENHANCED: Bet sizing
        pot_size: Pot size used for EV calculation
        
    GTO Principle:
        Value bet when equity_vs_calling > 0.50
        (This is correct - partition is for diagnostics & sizing)
    
    Example - Pure Value:
        # KK on K94 (pure value)
        CallingRangeEquity(
            equity=0.92,
            raw_equity=0.95,
            calling_range={'KJ': 0.3, 'K9': 0.2, '99': 0.15},
            
            worse_hands_calling={'KJ': 0.3, 'K9': 0.2, '99': 0.15},  # All worse!
            better_hands_calling={},  # No better hands call
            
            value_density=1.00,  # 100% of calling range we beat
            ev_vs_worse=+5.2bb,
            ev_vs_better=0.0bb,
            net_ev=+5.2bb,  # Pure value!
        )
    
    Example - Thin Value:
        # KQ on K94 (thin value)
        CallingRangeEquity(
            equity=0.52,
            raw_equity=0.68,
            calling_range={'AK': 0.3, 'KJ': 0.2, 'K9': 0.15},
            
            worse_hands_calling={'KJ': 0.2, 'K9': 0.15},  # 35% of calling range
            better_hands_calling={'AK': 0.3},  # 30% of calling range
            
            value_density=0.54,  # 54% worse (thin)
            ev_vs_worse=+3.5bb,
            ev_vs_better=-2.8bb,
            net_ev=+0.7bb,  # Thin, but profitable
        )
    
    Example - The Trap:
        # K7 on K94 (trap - don't bet!)
        CallingRangeEquity(
            equity=0.38,
            raw_equity=0.72,
            calling_range={'AK': 0.3, 'KQ': 0.25, 'KJ': 0.2, 'K9': 0.15},
            
            worse_hands_calling={'A7': 0.02},  # Almost nothing!
            better_hands_calling={'AK': 0.3, 'KQ': 0.25, 'KJ': 0.2, 'K9': 0.15},
            
            value_density=0.02,  # Only 2% worse (terrible!)
            ev_vs_worse=+0.3bb,
            ev_vs_better=-6.5bb,
            net_ev=-6.2bb,  # HUGE LOSS!
        )
        # DO NOT VALUE BET: net_ev < 0 and equity < 0.50
    """
    # Core metrics
    equity: float
    raw_equity: float
    calling_range_size: float
    calling_range: dict
    bet_size_frac: float
    
    # Partition analysis (NEW)
    worse_hands_calling: dict
    better_hands_calling: dict
    
    # Value metrics (NEW)
    value_density: float
    ev_vs_worse: float
    ev_vs_better: float
    net_ev: float
    
    # Context (NEW)
    pot_size: float
    
    def __post_init__(self):
        """Validate calling range equity makes sense."""
        if self.equity > self.raw_equity + 0.05:
            raise ValueError(
                f"Calling equity {self.equity} > raw equity {self.raw_equity}. "
                "Calling range equity should be ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â°ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¤ raw equity (villain folds weak hands)."
            )
        
        if not (0 <= self.value_density <= 1):
            raise ValueError(f"Value density must be 0-1, got {self.value_density}")
    
    def is_pure_value(self) -> bool:
        """Is this pure value (no better hands call)?"""
        return self.value_density > 0.85
    
    def is_thin_value(self) -> bool:
        """Is this thin value (some better hands call)?"""
        return 0.50 < self.value_density <= 0.85
    
    def is_marginal(self) -> bool:
        """Is this marginal (close to 50/50)?"""
        return 0.45 <= self.value_density <= 0.55
    
    def get_value_type(self) -> str:
        """Get descriptive value type."""
        if self.value_density > 0.85:
            return "pure_value"
        elif self.value_density > 0.65:
            return "strong_value"
        elif self.value_density > 0.50:
            return "thin_value"
        elif self.value_density > 0.40:
            return "marginal"
        else:
            return "trap"


@dataclass(frozen=True)
class FoldEquity:
    """
    Type 4: Fold Equity (CORRECTED)
    
    Equity gained from BETTER hands folding.
    
    CRITICAL INSIGHT:
        Fold equity only comes from hands that BEAT us folding.
        When worse hands fold, we LOSE value (we wanted them to call).
    
    Used for bluffing decisions: "Is bluff EV > 0?"
    
    Fold equity depends on:
    - Bet size (larger bets = more folds)
    - Board texture (scary boards = more folds from better hands)
    - Hand strength (weak top pair folds more than strong top pair)
    - Street (river = tighter calling ranges)
    
    Attributes:
        fold_probability: % of BETTER hands that fold (0-1)
        bet_size_frac: Bet size as fraction of pot
        fold_range: Better hands that fold {hand: freq}
        fold_range_size: % of total range that folds
        board_texture: Board texture type
        
        # Detailed analysis fields
        better_hands_range: All hands that beat us
        worse_hands_range: All hands we beat (don't want folding!)
        equity_before: Equity vs full range before bet
        equity_after: Equity vs remaining range after folds
        equity_gain: Equity increase from folds
        bluff_ev: Expected value of bluff (in bb)
        pot_size: Pot size
        cost: Bet cost
        
    GTO Bluff Formula:
        EV = (FE ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Ã‚Â Pot) + ((1 - FE) ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Ã‚Â Equity_vs_Calling ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Ã‚Â Total_Pot) - Cost
        Profitable if EV > 0
    
    Example:
        # 76s on QÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â JÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â 2ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â£, bet 2/3 pot
        FoldEquity(
            fold_probability=0.32,     # 32% of BETTER hands fold
            bet_size_frac=0.66,        # 2/3 pot bet
            fold_range={'99': 0.09, 'AQ': 0.04},  # Better hands that fold
            better_hands_range={'AQ': 0.20, 'KQ': 0.16, '99': 0.10},
            worse_hands_range={'A7': 0.03},  # Don't want folding!
            equity_before=0.28,
            equity_after=0.36,
            equity_gain=0.08,          # +8% from folds
            bluff_ev=+1.2,             # +1.2bb (profitable!)
        )
    """
    fold_probability: float  # Of BETTER hands only
    bet_size_frac: float
    fold_range: dict  # Better hands that fold
    fold_range_size: float  # % of total range
    board_texture: str
    
    # Detailed analysis
    better_hands_range: dict
    worse_hands_range: dict
    equity_before: float
    equity_after: float
    equity_gain: float
    bluff_ev: float
    pot_size: float
    cost: float
    
    def __post_init__(self):
        """Validate fold equity makes sense."""
        if not (0 <= self.fold_probability <= 1):
            raise ValueError(f"Fold probability must be 0-1, got {self.fold_probability}")
        if not (0 <= self.equity_gain <= 1):
            raise ValueError(f"Equity gain must be 0-1, got {self.equity_gain}")
    
    def is_profitable_bluff(self) -> bool:
        """Is this a profitable bluff?"""
        return self.bluff_ev > 0


@dataclass(frozen=True)
class AllEquities:
    """
    Complete equity package - all four types together.
    
    This is what EquityEngine returns - everything needed for decisions.
    
    Attributes:
        raw: Type 1 - Raw equity vs full range
        realized: Type 2 - Adjusted for position/texture
        vs_calling: Type 3 - Equity vs calling range (optional, only if betting)
        fold: Type 4 - Fold equity (optional, only if betting)
    
    Decision Usage:
        - Calling decisions: Use realized.equity vs pot odds
        - Value betting: Use vs_calling.equity > 0.50
        - Bluffing: Use fold.fold_probability ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Ã‚Â pot > cost
        - Diagnostic: Compare raw vs realized vs vs_calling
    
    Example:
        AllEquities(
            raw=RawEquity(equity=0.72, ...),
            realized=RealizedEquity(equity=0.58, ...),
            vs_calling=CallingRangeEquity(equity=0.42, ...),
            fold=FoldEquity(
                fold_probability=0.32,  # 32% of BETTER hands fold
                bluff_ev=+1.2,  # +1.2bb EV
                better_hands_range={'AQ': 0.20, '99': 0.10},
                worse_hands_range={'A7': 0.03},
                ...
            ),
        )
        
        Decision Logic:
        - realized.equity (0.58) vs pot_odds (0.33) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ Can call
        - vs_calling.equity (0.42) < 0.50 ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ DON'T value bet
        - fold.bluff_ev (+1.2bb) > 0 ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ Profitable bluff!
        ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ DECISION: BLUFF (if better hands fold enough)
    """
    raw: RawEquity
    realized: RealizedEquity
    vs_calling: Optional[CallingRangeEquity] = None
    fold: Optional[FoldEquity] = None
    
    def __post_init__(self):
        """Validate equity consistency."""
        # Realized should be within reasonable range of raw
        if not (0.60 <= self.realized.equity / self.raw.equity <= 1.15):
            raise ValueError(
                f"Realized equity {self.realized.equity} too far from "
                f"raw equity {self.raw.equity}. Realization factor should be 0.60-1.15"
            )
    
    def to_dict(self) -> dict:
        """Convert to dictionary for logging/diagnostics."""
        return {
            'raw_equity': self.raw.equity,
            'realized_equity': self.realized.equity,
            'vs_calling_equity': self.vs_calling.equity if self.vs_calling else None,
            'fold_equity': self.fold.fold_probability if self.fold else None,
            'method': self.raw.method,
            'samples': self.raw.samples,
        }
    
    def __str__(self) -> str:
        """Human-readable summary."""
        parts = [
            f"Raw: {self.raw.equity:.1%}",
            f"Realized: {self.realized.equity:.1%}",
        ]
        if self.vs_calling:
            parts.append(f"vs Calling: {self.vs_calling.equity:.1%}")
        if self.fold:
            parts.append(f"Fold: {self.fold.fold_probability:.1%}")
        return " | ".join(parts)


# Type aliases for clarity
EquityResult = AllEquities  # For backward compatibility
