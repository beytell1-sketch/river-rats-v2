"""
Range Manager - GTO Position-Based Poker Ranges
================================================================================

Manages preflop and postflop poker ranges for all positions in 6-max games.
Provides GTO-based ranges derived from solver outputs (GTO Wizard, PioSOLVER).

Core Functionality:
    1. Preflop Ranges: RFI, 3-bet, and calling ranges by position
    2. Postflop Ranges: Combined ranges for PFR and defenders
    3. Hand Percentiles: Calculate where a specific hand ranks within a range
    4. Board-Aware Evaluation: Adjust percentiles based on board texture

Key Features:
    - Position-specific ranges (UTG, HJ, CO, BTN, SB, BB)
    - Frequency-based ranges (0.0 = never, 1.0 = always)
    - Board-relative percentiles (considers made hands, draws, blockers)
    - Combo counting with card removal effects

Architecture:
    - RangeManager: Main class for range operations
    - Static range data: RFI, THREEBET, CALL dictionaries
    - Hand notation: Uses shared hand_categories module

Performance:
    - Ranges pre-loaded at initialization (O(1) lookups)
    - Percentile calculation: O(n) where n = combos in range (~100-300)
    - Thread-safe: Read-only operations after initialization

Usage:
    Basic range lookup:
        >>> rm = RangeManager()
        >>> rfi_range = rm.get_rfi_range('BTN')
        >>> rfi_range['AKs']  # 1.0 (always raise)
    
    Percentile calculation:
        >>> from hand_categories import cards_to_notation
        >>> hand = cards_to_notation('Ah', 'Kd')  # 'AKo'
        >>> hero_range = rm.get_postflop_range('BTN', is_pfr=True)
        >>> percentile = rm.get_hand_percentile(hand, hero_range, board=['Ks', '7h', '2d'])
        >>> percentile  # 0.85 = "top 15% of my range"
    
    Villain range construction:
        >>> villain_range = rm.get_postflop_range('BB', is_pfr=False, villain_pos='BTN')
        >>> # Returns defender range for BB vs BTN

Notes:
    - All ranges based on 100bb 6-max cash games
    - Frequencies represent GTO mixing strategies
    - Ranges simplified for mobile performance (vs full solver grids)
    - Use VillainRangeUpdater for postflop range narrowing

See Also:
    - hand_categories.py: Hand notation and category definitions
    - gto_preflop_ranges.py: Additional preflop range data
    - range_updater_v2.py: Postflop range narrowing based on actions
"""

from typing import Dict, List, Optional, Tuple, TypeAlias, Final

# Import shared constants and functions from hand_categories
from hand_categories import (
    # Constants
    RANKS,
    RANK_VALUES,
    CATEGORY_BASE,
    CATEGORY_MARGIN,
    # Functions
    normalize_hand,
    cards_to_notation,
    check_straight,
    has_straight_draw,
    lexicographic_tiebreaker,
    combo_count,
    count_combos_with_blockers,
)



# =============================================================================
# TYPE DEFINITIONS
# =============================================================================

# Type aliases for better code readability
HandNotation: TypeAlias = str  # e.g., 'AKs', 'QQ', 'T9o'
RangeDict: TypeAlias = Dict[HandNotation, float]  # hand -> frequency [0, 1]
Position: TypeAlias = str  # e.g., 'BTN', 'BB', 'CO'
BoardCards: TypeAlias = List[str]  # e.g., ['Ks', '7h', '2d']

# =============================================================================
# POSITION CONSTANTS
# =============================================================================

IP_POSITIONS = {'BTN', 'CO', 'HJ'}
OOP_POSITIONS = {'UTG', 'SB', 'BB'}


# =============================================================================
# RFI RANGES (Raise First In)
# =============================================================================
# Position-based opening ranges for 100bb 6-max cash games.
#
# Format: HandNotation -> Frequency
#   - HandNotation: 'AKs', 'QQ', 'T9o', etc. (from hand_categories)
#   - Frequency: 0.0 to 1.0 (0 = never open, 1.0 = always open)
#
# Data Source: GTO Wizard / PioSOLVER outputs (simplified for mobile)
# Stack Size: 100bb effective
# Game Type: 6-max cash
#
# Position Ranges (tightest to loosest):
#   1. UTG: ~15% of hands (tightest)
#   2. HJ:  ~20% of hands
#   3. CO:  ~27% of hands
#   4. BTN: ~45% of hands (loosest)
#   5. SB:  ~35% of hands (vs BB)
#   6. BB:  N/A (already posted blind)
#
# Notes:
#   - Frequencies < 1.0 represent GTO mixing strategies
#   - Actual play should use RNG to mix based on these frequencies
#   - Simplified from full solver grids for mobile performance
# =============================================================================
# Format: hand -> frequency (0.0-1.0)
# Based on GTO solver outputs for 100bb 6-max

RFI = {
    'UTG': {
        "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 1.0, "TT": 1.0,
        "99": 1.0, "88": 1.0, "77": 0.75, "66": 0.5, "55": 0.25,
        "AKs": 1.0, "AQs": 1.0, "AJs": 1.0, "ATs": 0.75,
        "KQs": 1.0, "KJs": 0.75, "KTs": 0.5,
        "QJs": 0.75, "QTs": 0.25,
        "JTs": 0.5,
        "AKo": 1.0, "AQo": 1.0, "AJo": 0.75, "ATo": 0.25,
        "KQo": 0.75, "KJo": 0.25,
        "A5s": 0.5, "A4s": 0.25,
    },
    
    'HJ': {
        "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 1.0, "TT": 1.0,
        "99": 1.0, "88": 1.0, "77": 1.0, "66": 0.75, "55": 0.5, "44": 0.25,
        "AKs": 1.0, "AQs": 1.0, "AJs": 1.0, "ATs": 1.0, "A9s": 0.5,
        "KQs": 1.0, "KJs": 1.0, "KTs": 0.75,
        "QJs": 1.0, "QTs": 0.5,
        "JTs": 0.75, "J9s": 0.25,
        "T9s": 0.5,
        "AKo": 1.0, "AQo": 1.0, "AJo": 1.0, "ATo": 0.5,
        "KQo": 1.0, "KJo": 0.5, "KTo": 0.25,
        "QJo": 0.25,
        "A5s": 0.75, "A4s": 0.5, "A3s": 0.25, "A2s": 0.25,
    },
    
    'CO': {
        "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 1.0, "TT": 1.0,
        "99": 1.0, "88": 1.0, "77": 1.0, "66": 1.0, "55": 0.75, "44": 0.5, "33": 0.25, "22": 0.25,
        "AKs": 1.0, "AQs": 1.0, "AJs": 1.0, "ATs": 1.0, "A9s": 0.75, "A8s": 0.5,
        "KQs": 1.0, "KJs": 1.0, "KTs": 1.0, "K9s": 0.5,
        "QJs": 1.0, "QTs": 1.0, "Q9s": 0.5,
        "JTs": 1.0, "J9s": 0.75,
        "T9s": 1.0, "T8s": 0.5,
        "98s": 0.75, "97s": 0.25,
        "87s": 0.75, "86s": 0.25,
        "76s": 0.5, "75s": 0.25,
        "65s": 0.5,
        "54s": 0.25,
        "AKo": 1.0, "AQo": 1.0, "AJo": 1.0, "ATo": 1.0, "A9o": 0.5,
        "KQo": 1.0, "KJo": 1.0, "KTo": 0.5,
        "QJo": 0.75, "QTo": 0.25,
        "JTo": 0.5,
        "A5s": 1.0, "A4s": 1.0, "A3s": 0.75, "A2s": 0.5,
    },
    
    'BTN': {
        "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 1.0, "TT": 1.0,
        "99": 1.0, "88": 1.0, "77": 1.0, "66": 1.0, "55": 1.0, "44": 1.0, "33": 0.75, "22": 0.75,
        "AKs": 1.0, "AQs": 1.0, "AJs": 1.0, "ATs": 1.0, "A9s": 1.0, "A8s": 1.0, "A7s": 0.75, "A6s": 0.75,
        "A5s": 1.0, "A4s": 1.0, "A3s": 1.0, "A2s": 1.0,
        "KQs": 1.0, "KJs": 1.0, "KTs": 1.0, "K9s": 1.0, "K8s": 0.75, "K7s": 0.5, "K6s": 0.5,
        "K5s": 0.5, "K4s": 0.25, "K3s": 0.25, "K2s": 0.25,
        "QJs": 1.0, "QTs": 1.0, "Q9s": 1.0, "Q8s": 0.75, "Q7s": 0.5, "Q6s": 0.25,
        "JTs": 1.0, "J9s": 1.0, "J8s": 0.75, "J7s": 0.5,
        "T9s": 1.0, "T8s": 1.0, "T7s": 0.5,
        "98s": 1.0, "97s": 0.75, "96s": 0.5,
        "87s": 1.0, "86s": 0.75, "85s": 0.25,
        "76s": 1.0, "75s": 0.5,
        "65s": 1.0, "64s": 0.25,
        "54s": 1.0, "53s": 0.25,
        "43s": 0.5,
        "AKo": 1.0, "AQo": 1.0, "AJo": 1.0, "ATo": 1.0, "A9o": 1.0, "A8o": 0.75, "A7o": 0.5,
        "A6o": 0.25, "A5o": 0.5, "A4o": 0.25, "A3o": 0.25, "A2o": 0.25,
        "KQo": 1.0, "KJo": 1.0, "KTo": 1.0, "K9o": 0.75, "K8o": 0.25,
        "QJo": 1.0, "QTo": 1.0, "Q9o": 0.5,
        "JTo": 1.0, "J9o": 0.5,
        "T9o": 0.75, "T8o": 0.25,
        "98o": 0.5,
        "87o": 0.25,
    },
    
    'SB': {
        "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 1.0, "TT": 1.0,
        "99": 1.0, "88": 1.0, "77": 1.0, "66": 1.0, "55": 0.75, "44": 0.5, "33": 0.5, "22": 0.5,
        "AKs": 1.0, "AQs": 1.0, "AJs": 1.0, "ATs": 1.0, "A9s": 1.0, "A8s": 0.75, "A7s": 0.5, "A6s": 0.5,
        "A5s": 1.0, "A4s": 1.0, "A3s": 0.75, "A2s": 0.75,
        "KQs": 1.0, "KJs": 1.0, "KTs": 1.0, "K9s": 0.75, "K8s": 0.5, "K7s": 0.25, "K6s": 0.25, "K5s": 0.25,
        "QJs": 1.0, "QTs": 1.0, "Q9s": 0.75, "Q8s": 0.5,
        "JTs": 1.0, "J9s": 0.75, "J8s": 0.5,
        "T9s": 1.0, "T8s": 0.75,
        "98s": 1.0, "97s": 0.5,
        "87s": 1.0, "86s": 0.5,
        "76s": 0.75, "75s": 0.25,
        "65s": 0.75,
        "54s": 0.5,
        "AKo": 1.0, "AQo": 1.0, "AJo": 1.0, "ATo": 1.0, "A9o": 0.75, "A8o": 0.5, "A7o": 0.25,
        "KQo": 1.0, "KJo": 1.0, "KTo": 0.75, "K9o": 0.5,
        "QJo": 1.0, "QTo": 0.75,
        "JTo": 0.75,
        "T9o": 0.5,
    },
}

# Aliases
RFI['MP'] = RFI['HJ']
RFI['EP'] = RFI['UTG']


# =============================================================================
# 3-BET RANGES (vs Open) - GTO Solver Data
# =============================================================================
# Polarized 3bet: Value (premiums) + Bluffs (blockers)
# Based on GTO Wizard / solver data for 100bb 6-max cash

THREE_BET = {
    'BB': {
        'vs_BTN': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.85, "TT": 0.70, "AQs": 1.0, "AQo": 0.75, "AJs": 0.60,
            "A5s": 0.80, "A4s": 0.70, "A3s": 0.50, "A2s": 0.40,
            "K5s": 0.40, "K4s": 0.30,
            "76s": 0.25, "65s": 0.20, "54s": 0.15,
        },
        'vs_CO': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.75, "TT": 0.50, "AQs": 1.0, "AQo": 0.60, "AJs": 0.40,
            "A5s": 0.60, "A4s": 0.50, "A3s": 0.30, "K5s": 0.25,
        },
        'vs_HJ': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.60, "TT": 0.30, "AQs": 0.90, "AQo": 0.40,
            "A5s": 0.40, "A4s": 0.30,
        },
        'vs_UTG': {
            "AA": 1.0, "KK": 1.0, "QQ": 0.90, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.40, "AQs": 0.60, "A5s": 0.25,
        },
    },
    'SB': {
        'vs_BTN': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 1.0, "TT": 0.90, "99": 0.40,
            "AQs": 1.0, "AQo": 1.0, "AJs": 1.0, "ATs": 0.70,
            "A5s": 1.0, "A4s": 0.80, "A3s": 0.50, "A2s": 0.30,
            "KQs": 0.70, "KJs": 0.40, "K5s": 0.50, "K4s": 0.30,
            "76s": 0.30, "65s": 0.25,
        },
        'vs_CO': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 1.0, "TT": 0.70,
            "AQs": 1.0, "AQo": 0.80, "AJs": 0.80, "ATs": 0.40,
            "A5s": 0.70, "A4s": 0.50, "KQs": 0.50, "K5s": 0.30,
        },
        'vs_HJ': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.90, "TT": 0.50,
            "AQs": 1.0, "AQo": 0.60, "AJs": 0.50,
            "A5s": 0.50, "A4s": 0.30,
        },
        'vs_UTG': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.70, "TT": 0.30, "AQs": 0.80, "A5s": 0.30,
        },
    },
    'BTN': {
        'vs_CO': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.70, "TT": 0.40,
            "AQs": 0.80, "AQo": 0.50, "AJs": 0.40,
            "A5s": 0.70, "A4s": 0.50, "K5s": 0.30,
            "76s": 0.20, "65s": 0.15,
        },
        'vs_HJ': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.60, "TT": 0.30,
            "AQs": 0.70, "AQo": 0.40, "A5s": 0.50, "A4s": 0.30,
        },
        'vs_UTG': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.40, "AQs": 0.50, "A5s": 0.30,
        },
    },
    'CO': {
        'vs_HJ': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.50, "TT": 0.25, "AQs": 0.60, "AQo": 0.30, "A5s": 0.40,
        },
        'vs_UTG': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.30, "AQs": 0.40,
        },
    },
    'HJ': {
        'vs_UTG': {
            "AA": 1.0, "KK": 1.0, "QQ": 0.90, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.20,
        },
    },
}

# BB vs SB 3-bet range (new — SB opens ~35%, BB plays back with ~12% of hands)
# Value: premiums + strong broadways. Bluffs: suited A-x blockers, some suited connectors.
THREE_BET['BB']['vs_SB'] = {
    "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 1.0, "TT": 0.8,
    "99": 0.2, "88": 0.1,
    "AKs": 1.0, "AKo": 1.0, "AQs": 1.0, "AQo": 0.8,
    "AJs": 0.6, "KQs": 0.5,
    "A5s": 0.9, "A4s": 0.8, "A3s": 0.6, "A2s": 0.5,
    "K5s": 0.5, "K4s": 0.3,
    "76s": 0.3, "65s": 0.3, "54s": 0.2,
}

# 3BET aliases
THREE_BET['BB']['vs_MP'] = THREE_BET['BB']['vs_HJ']
THREE_BET['BB']['vs_EP'] = THREE_BET['BB']['vs_UTG']
THREE_BET['SB']['vs_MP'] = THREE_BET['SB']['vs_HJ']
THREE_BET['SB']['vs_EP'] = THREE_BET['SB']['vs_UTG']
THREE_BET['BTN']['vs_MP'] = THREE_BET['BTN']['vs_HJ']
THREE_BET['BTN']['vs_EP'] = THREE_BET['BTN']['vs_UTG']
THREE_BET['CO']['vs_EP'] = THREE_BET['CO']['vs_UTG']


# =============================================================================
# CALL RANGES (vs Open - Flat Call) - GTO Solver Data
# =============================================================================
# Linear call range: Medium strength hands with playability
# Based on GTO Wizard / solver data for 100bb 6-max cash

CALL_VS_OPEN = {
    'BB': {
        'vs_BTN': {
            "99": 1.0, "88": 1.0, "77": 1.0, "66": 1.0, "55": 0.80, "44": 0.60, "33": 0.40, "22": 0.40,
            "JJ": 0.15, "TT": 0.30,
            "AJs": 0.40, "ATs": 1.0, "A9s": 1.0, "A8s": 1.0, "A7s": 0.80, "A6s": 0.60,
            "KQs": 1.0, "KJs": 1.0, "KTs": 1.0, "K9s": 1.0, "K8s": 0.70, "K7s": 0.40,
            "QJs": 1.0, "QTs": 1.0, "Q9s": 1.0, "Q8s": 0.50,
            "JTs": 1.0, "J9s": 1.0, "J8s": 0.70,
            "T9s": 1.0, "T8s": 1.0, "T7s": 0.40,
            "98s": 1.0, "97s": 0.70,
            "87s": 1.0, "86s": 0.50,
            "76s": 0.75, "75s": 0.25,
            "65s": 0.80, "54s": 0.60,
            "AQo": 0.25, "AJo": 1.0, "ATo": 1.0, "A9o": 0.60,
            "KQo": 1.0, "KJo": 0.70, "KTo": 0.40,
            "QJo": 0.60, "QTo": 0.25, "JTo": 0.40,
        },
        'vs_CO': {
            "99": 1.0, "88": 1.0, "77": 1.0, "66": 0.70, "55": 0.50, "44": 0.30,
            "JJ": 0.25, "TT": 0.50,
            "AJs": 0.60, "ATs": 1.0, "A9s": 1.0, "A8s": 0.70, "A7s": 0.40,
            "KQs": 1.0, "KJs": 1.0, "KTs": 1.0, "K9s": 0.70,
            "QJs": 1.0, "QTs": 1.0, "Q9s": 0.70,
            "JTs": 1.0, "J9s": 0.70,
            "T9s": 1.0, "T8s": 0.70,
            "98s": 1.0, "97s": 0.50,
            "87s": 1.0, "76s": 0.70, "65s": 0.60, "54s": 0.40,
            "AQo": 0.40, "AJo": 1.0, "ATo": 0.70,
            "KQo": 1.0, "KJo": 0.50, "QJo": 0.40,
        },
        'vs_HJ': {
            "99": 1.0, "88": 0.80, "77": 0.60, "66": 0.30,
            "JJ": 0.40, "TT": 0.70,
            "AJs": 1.0, "ATs": 1.0, "A9s": 0.50,
            "KQs": 1.0, "KJs": 0.80, "KTs": 0.50,
            "QJs": 0.80, "QTs": 0.50, "JTs": 0.80,
            "T9s": 0.60, "98s": 0.50, "87s": 0.30,
            "AQo": 0.60, "AJo": 0.80, "KQo": 0.60,
        },
        'vs_UTG': {
            "99": 0.80, "88": 0.60, "77": 0.30,
            "JJ": 0.60, "TT": 1.0, "QQ": 0.10,
            "AQs": 0.40, "AJs": 0.80, "ATs": 0.50,
            "KQs": 0.80, "KJs": 0.50, "QJs": 0.50, "JTs": 0.50, "T9s": 0.30,
            "AQo": 0.25, "AJo": 0.30, "KQo": 0.30,
        },
    },
    'SB': {
        'vs_BTN': {"99": 0.20, "88": 0.20, "77": 0.10},  # SB mostly 3bets or folds
        'vs_CO': {}, 'vs_HJ': {}, 'vs_UTG': {},
    },
    'BTN': {
        'vs_CO': {
            "99": 1.0, "88": 1.0, "77": 1.0, "66": 0.70, "55": 0.50,
            "JJ": 0.30, "TT": 0.60,
            "AQs": 0.20, "AJs": 0.60, "ATs": 1.0, "A9s": 1.0, "A8s": 0.70,
            "KQs": 1.0, "KJs": 1.0, "KTs": 1.0, "K9s": 0.70,
            "QJs": 1.0, "QTs": 1.0, "Q9s": 0.50,
            "JTs": 1.0, "J9s": 0.70,
            "T9s": 1.0, "T8s": 0.50, "98s": 1.0, "87s": 0.80, "76s": 0.60, "65s": 0.50,
            "AQo": 0.50, "AJo": 1.0, "ATo": 0.70,
            "KQo": 1.0, "KJo": 0.50, "QJo": 0.50,
        },
        'vs_HJ': {
            "99": 1.0, "88": 0.80, "77": 0.50, "66": 0.30,
            "JJ": 0.40, "TT": 0.70,
            "AQs": 0.30, "AJs": 0.60, "ATs": 1.0, "A9s": 0.70,
            "KQs": 1.0, "KJs": 0.80, "KTs": 0.50,
            "QJs": 0.80, "QTs": 0.50, "JTs": 0.80, "T9s": 0.60, "98s": 0.50,
            "AQo": 0.60, "AJo": 0.80, "KQo": 0.80,
        },
        'vs_UTG': {
            "99": 0.80, "88": 0.50, "77": 0.30,
            "JJ": 0.60, "TT": 0.70,
            "AQs": 0.50, "AJs": 0.50, "ATs": 0.30,
            "KQs": 0.60, "KJs": 0.40, "QJs": 0.40, "JTs": 0.40,
            "AQo": 0.30, "AJo": 0.30,
        },
    },
    'CO': {
        'vs_HJ': {
            "99": 1.0, "88": 0.80, "77": 0.50,
            "JJ": 0.50, "TT": 0.75,
            "AQs": 0.40, "AJs": 1.0, "ATs": 0.70,
            "KQs": 1.0, "KJs": 0.80, "QJs": 0.80, "JTs": 0.80, "T9s": 0.50,
            "AQo": 0.70, "AJo": 0.60, "KQo": 0.60,
        },
        'vs_UTG': {
            "99": 0.80, "88": 0.50,
            "JJ": 0.70, "TT": 1.0,
            "AQs": 0.60, "AJs": 0.60,
            "KQs": 0.80, "KJs": 0.50, "QJs": 0.50, "JTs": 0.50,
            "AQo": 0.30,
        },
    },
    'HJ': {
        'vs_UTG': {
            "99": 0.50, "88": 0.30,
            "JJ": 0.80, "TT": 1.0, "QQ": 0.10,
            "AQs": 0.50, "AJs": 0.40, "KQs": 0.50, "QJs": 0.30,
        },
    },
}

# BB vs SB call range (new — SB opens ~35%, BB defends very wide, ~45% of hands)
# AA/KK are excluded here (3-bet only). Wide range: pairs, broadways, suited connectors.
CALL_VS_OPEN['BB']['vs_SB'] = {
    "AA": 0.0,  # 3-bet only
    "KK": 0.0,  # 3-bet only
    "77": 1.0, "66": 1.0, "55": 1.0, "44": 0.8, "33": 0.6, "22": 0.6,
    "88": 1.0, "99": 0.8,  # some call, some 3-bet
    "AJs": 0.5, "ATs": 1.0, "A9s": 1.0, "A8s": 1.0, "A7s": 0.8,
    "A6s": 0.6, "A5s": 0.4,  # A5s mostly 3-bets
    "KQs": 0.4, "KJs": 1.0, "KTs": 1.0, "K9s": 1.0,
    "QJs": 1.0, "QTs": 1.0, "Q9s": 0.8,
    "JTs": 1.0, "J9s": 0.8,
    "T9s": 1.0, "T8s": 0.7,
    "98s": 1.0, "87s": 0.8, "76s": 0.7, "65s": 0.6, "54s": 0.5,
    "AJo": 1.0, "ATo": 1.0, "A9o": 0.6,
    "KQo": 1.0, "KJo": 0.8, "KTo": 0.5,
    "QJo": 0.8, "JTo": 0.5,
}

# CALL aliases
CALL_VS_OPEN['BB']['vs_MP'] = CALL_VS_OPEN['BB']['vs_HJ']
CALL_VS_OPEN['BB']['vs_EP'] = CALL_VS_OPEN['BB']['vs_UTG']
CALL_VS_OPEN['SB']['vs_MP'] = CALL_VS_OPEN['SB'].get('vs_HJ', {})
CALL_VS_OPEN['SB']['vs_EP'] = CALL_VS_OPEN['SB'].get('vs_UTG', {})
CALL_VS_OPEN['BTN']['vs_MP'] = CALL_VS_OPEN['BTN']['vs_HJ']
CALL_VS_OPEN['BTN']['vs_EP'] = CALL_VS_OPEN['BTN']['vs_UTG']
CALL_VS_OPEN['CO']['vs_MP'] = CALL_VS_OPEN['CO']['vs_HJ']
CALL_VS_OPEN['CO']['vs_EP'] = CALL_VS_OPEN['CO']['vs_UTG']
CALL_VS_OPEN['HJ'] = {'vs_UTG': CALL_VS_OPEN['HJ']['vs_UTG'], 'vs_MP': CALL_VS_OPEN['HJ']['vs_UTG'], 'vs_EP': CALL_VS_OPEN['HJ']['vs_UTG']}


# =============================================================================
# CALL_VS_3BET — Hero opened, villain 3-bet, hero calls (not 4-bets, not folds)
# =============================================================================
# When hero raises and faces a 3-bet, most of the range 4-bets (premiums) or folds.
# The call range is the middle: hands strong enough to continue but not ideal 4-bets.
# UTG/HJ open tight so their call range vs 3-bets is narrow.
# BTN/CO open wider so they call 3-bets with a larger piece of their range.
#
# UTG and HJ: JJ calls ~60%, TT calls ~70% (4-betting TT from UTG too thin vs strong 3-bets),
# AQs calls (4-betting AQs from UTG is often dominated by AK).
# BTN/CO: wider call range because their opening range is wider and 3-bet ranges are more polar.

CALL_VS_3BET = {
    'UTG': {
        # UTG faces 3-bets mostly from BTN, CO, and the blinds.
        # Opening range is tight so the call range is very narrow.
        # JJ: 4-bets ~40%, calls ~60%. TT: calls rather than 4-bets (dominated too often).
        # 99: marginal call vs wide 3-bets only, fold vs tight ones. AQs: strong call,
        # 4-betting AQs from UTG is too thin (dominated by AK). AJs: borderline, folds
        # vs most 3-bets. KQs: calls vs wide 3-bet ranges only.
        'vs_BTN': {"JJ": 0.6, "TT": 0.7, "99": 0.3, "AQs": 0.7, "AJs": 0.3, "KQs": 0.4},
        'vs_CO':  {"JJ": 0.5, "TT": 0.6, "99": 0.2, "AQs": 0.6, "AJs": 0.2},
        'vs_BB':  {"JJ": 0.6, "TT": 0.7, "99": 0.3, "AQs": 0.7, "AJs": 0.3, "KQs": 0.3},
        'vs_SB':  {"JJ": 0.5, "TT": 0.6, "AQs": 0.6},
    },
    'HJ': {
        # HJ opens slightly wider than UTG (~18-20%). Faces 3-bets from BTN, CO, and blinds.
        # Call range is marginally wider than UTG: TT calls at higher frequency, 99 more
        # viable, AJs and KQs become reasonable calls vs wide 3-bets (BTN in particular).
        # 88 is a speculative call only vs very wide BTN 3-bets with deep implied odds.
        # QJs: marginal, call rarely vs wide ranges only.
        'vs_BTN': {"JJ": 0.7, "TT": 0.8, "99": 0.4, "88": 0.2, "AQs": 0.8, "AJs": 0.5, "KQs": 0.5, "QJs": 0.2},
        'vs_CO':  {"JJ": 0.6, "TT": 0.7, "99": 0.3, "AQs": 0.7, "AJs": 0.4, "KQs": 0.4},
        'vs_BB':  {"JJ": 0.7, "TT": 0.8, "99": 0.4, "AQs": 0.8, "AJs": 0.5, "KQs": 0.5},
        'vs_SB':  {"JJ": 0.6, "TT": 0.7, "99": 0.3, "AQs": 0.7, "AJs": 0.3},
    },
    'CO': {
        'vs_BB':  {"TT": 0.7, "99": 0.5, "AQs": 0.6, "AJs": 0.4, "KQs": 0.4},
        'vs_SB':  {"TT": 0.5, "99": 0.3, "AQs": 0.4},
        'vs_BTN': {"TT": 0.6, "99": 0.4, "AQs": 0.5},
    },
    'BTN': {
        'vs_BB': {"TT": 0.9, "99": 0.7, "88": 0.3, "AQs": 0.8, "AJs": 0.6,
                  "KQs": 0.5, "QJs": 0.3, "JTs": 0.3},
        'vs_SB': {"JJ": 0.3, "TT": 0.8, "99": 0.5, "88": 0.3,
                  "AQs": 0.7, "AJs": 0.5, "KQs": 0.4},
        'vs_CO': {"JJ": 0.3, "TT": 0.5, "99": 0.3, "AQs": 0.5, "AJs": 0.3},
    },
    'SB': {
        'vs_BB': {"JJ": 0.4, "TT": 0.5, "99": 0.3, "AQs": 0.5},
    },
    'BB': {
        # BB rarely opens (only isolation vs limpers), so rarely faces 3-bets as the opener.
        # Included for completeness (squeeze scenarios where BB squeezed and then faces 4-bet).
        'vs_BTN': {"JJ": 0.5, "TT": 0.6, "AQs": 0.6},
        'vs_CO':  {"JJ": 0.4, "TT": 0.5, "AQs": 0.5},
        'vs_SB':  {"JJ": 0.5, "TT": 0.6, "AQs": 0.6},
    },
}


# =============================================================================
# FOURBET — Hero's 4-bet range after opening and facing a 3-bet
# =============================================================================
# value + bluff 4-bets. A5s/A4s as blocker (bluff) 4-bets included.
# Value 4-bets: AA, KK (always), QQ/JJ (position-dependent frequency).
# Bluff 4-bets: A5s/A4s — block AA/AK combos, playable if called.
# Tighter positions (UTG/HJ) have narrower 4-bet ranges; looser positions (BTN) are wider.

FOURBET = {
    'UTG': {"AA": 1.0, "KK": 1.0, "AKs": 1.0, "AKo": 1.0},
    'HJ':  {"AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0},
    'CO':  {"AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.2, "AQs": 0.2},
    'BTN': {"AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.3, "AQs": 0.3, "A5s": 0.5, "A4s": 0.3},
    'SB':  {"AA": 1.0, "KK": 1.0, "QQ": 1.0, "AKs": 1.0, "AKo": 1.0,
            "JJ": 0.5, "TT": 0.3, "AQs": 0.4, "A5s": 0.6},
    'BB':  {"AA": 1.0, "KK": 1.0, "QQ": 0.8, "AKs": 1.0, "AKo": 0.9,
            "JJ": 0.2, "A5s": 0.3},
}


# =============================================================================
# DEFEND RANGES (vs Open) - Legacy Combined Ranges
# =============================================================================
# Combined call + 3bet ranges (kept for backward compatibility)

DEFEND = {
    'BB': {
        'vs_BTN': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 0.75, "TT": 0.5,
            "99": 1.0, "88": 1.0, "77": 1.0, "66": 1.0, "55": 0.75, "44": 0.5, "33": 0.25, "22": 0.25,
            "AKs": 1.0, "AQs": 1.0, "AJs": 0.75, "ATs": 0.5, "A9s": 1.0, "A8s": 1.0, "A7s": 0.75,
            "A6s": 0.5, "A5s": 0.75, "A4s": 0.5, "A3s": 0.75, "A2s": 1.0,
            "AKo": 1.0, "AQo": 0.75, "AJo": 1.0, "ATo": 1.0, "A9o": 0.75, "A8o": 0.5,
            "KQs": 0.5, "KJs": 0.75, "KTs": 1.0, "K9s": 1.0, "K8s": 0.75, "K7s": 0.5, "K6s": 0.25,
            "K5s": 0.25, "K4s": 0.25,
            "KQo": 1.0, "KJo": 0.75, "KTo": 0.5,
            "QJs": 1.0, "QTs": 1.0, "Q9s": 1.0, "Q8s": 0.5,
            "QJo": 0.75, "QTo": 0.25,
            "JTs": 1.0, "J9s": 1.0, "J8s": 0.75,
            "JTo": 0.5,
            "T9s": 1.0, "T8s": 1.0, "T7s": 0.5,
            "98s": 1.0, "97s": 0.75,
            "87s": 1.0, "86s": 0.5,
            "76s": 1.0, "75s": 0.25,
            "65s": 1.0,
            "54s": 0.75,
        },
        'vs_CO': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 0.5, "TT": 0.75,
            "99": 1.0, "88": 1.0, "77": 1.0, "66": 0.75, "55": 0.5, "44": 0.25,
            "AKs": 1.0, "AQs": 1.0, "AJs": 0.5, "ATs": 1.0, "A9s": 1.0, "A8s": 0.75, "A7s": 0.5,
            "A6s": 0.25, "A5s": 0.5, "A4s": 0.75, "A3s": 0.75, "A2s": 0.75,
            "AKo": 1.0, "AQo": 0.5, "AJo": 1.0, "ATo": 0.75,
            "KQs": 1.0, "KJs": 1.0, "KTs": 1.0, "K9s": 0.75,
            "KQo": 1.0, "KJo": 0.5,
            "QJs": 1.0, "QTs": 1.0, "Q9s": 0.75,
            "JTs": 1.0, "J9s": 0.75,
            "T9s": 1.0, "T8s": 0.75,
            "98s": 1.0, "97s": 0.5,
            "87s": 1.0,
            "76s": 0.75,
            "65s": 0.75,
            "54s": 0.5,
        },
        'vs_HJ': {
            "AA": 1.0, "KK": 1.0, "QQ": 0.75, "JJ": 0.75, "TT": 1.0,
            "99": 1.0, "88": 0.75, "77": 0.5, "66": 0.25,
            "AKs": 1.0, "AQs": 0.5, "AJs": 1.0, "ATs": 1.0, "A9s": 0.5,
            "A5s": 0.75, "A4s": 0.75, "A3s": 0.5, "A2s": 0.5,
            "AKo": 1.0, "AQo": 1.0, "AJo": 0.75,
            "KQs": 1.0, "KJs": 0.75, "KTs": 0.5,
            "KQo": 0.5,
            "QJs": 0.75, "QTs": 0.5,
            "JTs": 0.75,
            "T9s": 0.5,
            "98s": 0.5,
            "87s": 0.25,
        },
        'vs_UTG': {
            "AA": 1.0, "KK": 1.0, "QQ": 0.5, "JJ": 1.0, "TT": 1.0,
            "99": 0.75, "88": 0.5, "77": 0.25,
            "AKs": 1.0, "AQs": 1.0, "AJs": 0.75, "ATs": 0.5,
            "A5s": 0.5, "A4s": 0.5,
            "AKo": 0.75, "AQo": 0.75, "AJo": 0.25,
            "KQs": 0.75, "KJs": 0.5,
            "QJs": 0.5,
            "JTs": 0.5,
            "T9s": 0.25,
        },
    },
    
    'SB': {
        'vs_BTN': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 1.0, "TT": 1.0,
            "99": 0.5, "88": 0.5, "77": 0.25,
            "AKs": 1.0, "AQs": 1.0, "AJs": 1.0, "ATs": 1.0, "A9s": 0.5,
            "A5s": 1.0, "A4s": 0.75, "A3s": 0.5,
            "AKo": 1.0, "AQo": 1.0, "AJo": 0.5,
            "KQs": 1.0, "KJs": 1.0, "KTs": 0.75,
            "QJs": 0.5, "QTs": 0.5,
            "JTs": 0.75,
            "T9s": 0.5,
            "98s": 0.5,
        },
        'vs_CO': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 1.0, "TT": 1.0,
            "99": 0.5,
            "AKs": 1.0, "AQs": 1.0, "AJs": 1.0, "ATs": 0.5,
            "A5s": 0.75, "A4s": 0.5,
            "AKo": 1.0, "AQo": 0.75,
            "KQs": 0.75, "KJs": 0.5, "KTs": 0.5,
            "QJs": 0.5,
            "JTs": 0.5,
        },
    },
    
    'BTN': {
        'vs_CO': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 1.0, "TT": 1.0,
            "99": 1.0, "88": 1.0, "77": 1.0, "66": 0.75, "55": 0.5,
            "AKs": 1.0, "AQs": 1.0, "AJs": 1.0, "ATs": 1.0, "A9s": 1.0, "A8s": 0.75, "A7s": 0.5,
            "A6s": 0.25, "A5s": 1.0, "A4s": 1.0, "A3s": 0.5, "A2s": 0.5,
            "AKo": 1.0, "AQo": 1.0, "AJo": 1.0, "ATo": 0.75,
            "KQs": 1.0, "KJs": 1.0, "KTs": 1.0, "K9s": 0.75,
            "KQo": 1.0, "KJo": 0.5,
            "QJs": 1.0, "QTs": 1.0, "Q9s": 0.5,
            "JTs": 1.0, "J9s": 0.75,
            "T9s": 1.0, "T8s": 0.5,
            "98s": 1.0,
            "87s": 0.75,
            "76s": 0.5,
            "65s": 0.5,
        },
        'vs_HJ': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 1.0, "TT": 1.0,
            "99": 1.0, "88": 0.75, "77": 0.5, "66": 0.25,
            "AKs": 1.0, "AQs": 1.0, "AJs": 1.0, "ATs": 1.0, "A9s": 0.75,
            "A5s": 1.0, "A4s": 0.5,
            "AKo": 1.0, "AQo": 1.0, "AJo": 0.75,
            "KQs": 1.0, "KJs": 0.75, "KTs": 0.5,
            "KQo": 0.75,
            "QJs": 0.75, "QTs": 0.5,
            "JTs": 0.75,
            "T9s": 0.5,
            "98s": 0.5,
        },
    },
    
    'CO': {
        'vs_HJ': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 1.0, "TT": 1.0,
            "99": 1.0, "88": 0.75, "77": 0.5,
            "AKs": 1.0, "AQs": 1.0, "AJs": 1.0, "ATs": 0.75,
            "A5s": 1.0, "A4s": 0.5,
            "AKo": 1.0, "AQo": 1.0, "AJo": 0.5,
            "KQs": 1.0, "KJs": 0.75,
            "KQo": 0.5,
            "QJs": 0.75,
            "JTs": 0.75,
            "T9s": 0.5,
        },
        'vs_UTG': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 1.0, "TT": 1.0,
            "99": 0.75, "88": 0.5,
            "AKs": 1.0, "AQs": 1.0, "AJs": 0.75, "ATs": 0.5,
            "AKo": 1.0, "AQo": 0.75,
            "KQs": 0.75, "KJs": 0.5,
            "QJs": 0.5,
            "JTs": 0.5,
        },
    },
}

# Aliases for positional lookups
DEFEND['BB']['vs_MP'] = DEFEND['BB']['vs_HJ']
DEFEND['BB']['vs_EP'] = DEFEND['BB']['vs_UTG']
DEFEND['SB']['vs_HJ'] = DEFEND['SB']['vs_CO']
DEFEND['SB']['vs_UTG'] = DEFEND['SB']['vs_CO']
DEFEND['BTN']['vs_UTG'] = DEFEND['BTN']['vs_HJ']
DEFEND['CO']['vs_EP'] = DEFEND['CO']['vs_UTG']


# =============================================================================
# 3BET RANGES (Preflop Re-raise)
# =============================================================================
# 3bet ranges from each position vs each opener
# Key insight: BB/SB 3bet ranges are POLARIZED (premiums + suited blockers)
# BTN/CO 3bet ranges are more LINEAR (continuous value)
# Based on GTO solver outputs (GTO Wizard, MonkerSolver) for 100bb 6-max

THREEB = {
    # BB 3bet ranges - POLARIZED (value + bluffs with blockers)
    'BB': {
        'vs_BTN': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 0.75, "TT": 0.5,
            "AKs": 1.0, "AKo": 1.0, "AQs": 1.0, "AQo": 0.5,
            "AJs": 0.5, "KQs": 0.5,
            "A5s": 0.75, "A4s": 0.75, "A3s": 0.5, "A2s": 0.5,
            "K5s": 0.25, "K4s": 0.25,
            "76s": 0.25, "65s": 0.25, "54s": 0.25,
        },
        'vs_CO': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 0.5, "TT": 0.25,
            "AKs": 1.0, "AKo": 1.0, "AQs": 0.75, "AQo": 0.25,
            "AJs": 0.25, "KQs": 0.25,
            "A5s": 0.5, "A4s": 0.5, "A3s": 0.25,
            "K5s": 0.25,
        },
        'vs_HJ': {
            "AA": 1.0, "KK": 1.0, "QQ": 0.75, "JJ": 0.25,
            "AKs": 1.0, "AKo": 1.0, "AQs": 0.5,
            "A5s": 0.25, "A4s": 0.25,
        },
        'vs_UTG': {
            "AA": 1.0, "KK": 1.0, "QQ": 0.5,
            "AKs": 1.0, "AKo": 0.75,
            "A5s": 0.25,
        },
    },
    
    # SB 3bet ranges - POLARIZED, wider than BB (will have position on BB)
    'SB': {
        'vs_BTN': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 1.0, "TT": 0.75,
            "99": 0.25,
            "AKs": 1.0, "AKo": 1.0, "AQs": 1.0, "AQo": 0.75,
            "AJs": 0.75, "ATs": 0.25,
            "KQs": 0.75, "KJs": 0.25,
            "A5s": 1.0, "A4s": 0.75, "A3s": 0.5, "A2s": 0.5,
            "K5s": 0.5, "K4s": 0.25,
            "76s": 0.25, "65s": 0.25,
        },
        'vs_CO': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 0.75, "TT": 0.5,
            "AKs": 1.0, "AKo": 1.0, "AQs": 1.0, "AQo": 0.5,
            "AJs": 0.5, "KQs": 0.5,
            "A5s": 0.75, "A4s": 0.5, "A3s": 0.25,
        },
        'vs_HJ': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 0.5,
            "AKs": 1.0, "AKo": 1.0, "AQs": 0.75,
            "KQs": 0.25,
            "A5s": 0.5, "A4s": 0.25,
        },
        'vs_UTG': {
            "AA": 1.0, "KK": 1.0, "QQ": 0.75,
            "AKs": 1.0, "AKo": 0.75,
            "A5s": 0.25,
        },
    },
    
    # BTN 3bet ranges - LINEAR (will have position postflop)
    'BTN': {
        'vs_CO': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 1.0, "TT": 0.75,
            "99": 0.5, "88": 0.25,
            "AKs": 1.0, "AKo": 1.0, "AQs": 1.0, "AQo": 1.0,
            "AJs": 1.0, "ATs": 0.75, "A9s": 0.25,
            "KQs": 1.0, "KQo": 0.75, "KJs": 0.75, "KTs": 0.5,
            "QJs": 0.5, "QTs": 0.25,
            "JTs": 0.25,
            "A5s": 1.0, "A4s": 0.75, "A3s": 0.5, "A2s": 0.5,
        },
        'vs_HJ': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 0.75, "TT": 0.5,
            "99": 0.25,
            "AKs": 1.0, "AKo": 1.0, "AQs": 1.0, "AQo": 0.75,
            "AJs": 0.75, "ATs": 0.5,
            "KQs": 0.75, "KJs": 0.5,
            "A5s": 0.75, "A4s": 0.5,
        },
        'vs_UTG': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 0.5,
            "AKs": 1.0, "AKo": 1.0, "AQs": 0.75,
            "KQs": 0.25,
            "A5s": 0.5,
        },
    },
    
    # CO 3bet ranges
    'CO': {
        'vs_HJ': {
            "AA": 1.0, "KK": 1.0, "QQ": 1.0, "JJ": 0.75, "TT": 0.5,
            "AKs": 1.0, "AKo": 1.0, "AQs": 1.0, "AQo": 0.5,
            "AJs": 0.5, "KQs": 0.5,
            "A5s": 0.5, "A4s": 0.25,
        },
        'vs_UTG': {
            "AA": 1.0, "KK": 1.0, "QQ": 0.75, "JJ": 0.25,
            "AKs": 1.0, "AKo": 1.0, "AQs": 0.5,
            "A5s": 0.25,
        },
    },
    
    # HJ 3bet ranges
    'HJ': {
        'vs_UTG': {
            "AA": 1.0, "KK": 1.0, "QQ": 0.5,
            "AKs": 1.0, "AKo": 0.75,
        },
    },
}

# 3bet aliases
THREEB['BB']['vs_MP'] = THREEB['BB']['vs_HJ']
THREEB['BB']['vs_EP'] = THREEB['BB']['vs_UTG']
THREEB['SB']['vs_MP'] = THREEB['SB']['vs_HJ']
THREEB['SB']['vs_EP'] = THREEB['SB']['vs_UTG']
THREEB['BTN']['vs_MP'] = THREEB['BTN']['vs_HJ']
THREEB['BTN']['vs_EP'] = THREEB['BTN']['vs_UTG']
THREEB['CO']['vs_MP'] = THREEB['CO']['vs_HJ']
THREEB['CO']['vs_EP'] = THREEB['CO']['vs_UTG']


# =============================================================================
# CALL RANGES (Flat vs Open)
# =============================================================================
# Call ranges are CONDENSED/LINEAR - hands too good to fold, not good enough to 3bet
# Based on GTO solver outputs for 100bb 6-max

CALL = {
    # BB call ranges - widest due to pot odds
    'BB': {
        'vs_BTN': {
            "JJ": 0.25, "TT": 0.5, "99": 1.0, "88": 1.0, "77": 1.0,
            "66": 1.0, "55": 0.75, "44": 0.5, "33": 0.25, "22": 0.25,
            "AQo": 0.5, "AJo": 1.0, "ATo": 1.0, "A9o": 0.75, "A8o": 0.5,
            "AJs": 0.5, "ATs": 0.5, "A9s": 1.0, "A8s": 1.0, "A7s": 0.75,
            "A6s": 0.5,
            "KQo": 1.0, "KJo": 0.75, "KTo": 0.5,
            "KQs": 0.5, "KJs": 0.75, "KTs": 1.0, "K9s": 1.0, "K8s": 0.75,
            "K7s": 0.5, "K6s": 0.25,
            "QJo": 0.75, "QTo": 0.25,
            "QJs": 1.0, "QTs": 1.0, "Q9s": 1.0, "Q8s": 0.5,
            "JTo": 0.5,
            "JTs": 1.0, "J9s": 1.0, "J8s": 0.75,
            "T9s": 1.0, "T8s": 1.0, "T7s": 0.5,
            "98s": 1.0, "97s": 0.75,
            "87s": 1.0, "86s": 0.5,
            "76s": 0.75, "75s": 0.25,
            "65s": 0.75,
            "54s": 0.5,
        },
        'vs_CO': {
            "TT": 0.75, "99": 1.0, "88": 1.0, "77": 1.0,
            "66": 0.75, "55": 0.5, "44": 0.25,
            "AQo": 0.75, "AJo": 1.0, "ATo": 0.75,
            "ATs": 0.75, "A9s": 1.0, "A8s": 0.75, "A7s": 0.5,
            "KQo": 1.0, "KJo": 0.5,
            "KJs": 1.0, "KTs": 1.0, "K9s": 0.75,
            "QJs": 1.0, "QTs": 1.0, "Q9s": 0.75,
            "JTs": 1.0, "J9s": 0.75,
            "T9s": 1.0, "T8s": 0.75,
            "98s": 1.0, "97s": 0.5,
            "87s": 1.0,
            "76s": 0.75,
            "65s": 0.75,
            "54s": 0.5,
        },
        'vs_HJ': {
            "TT": 1.0, "99": 1.0, "88": 0.75, "77": 0.5, "66": 0.25,
            "AQo": 1.0, "AJo": 0.75,
            "AJs": 1.0, "ATs": 1.0, "A9s": 0.5,
            "KQo": 0.5,
            "KJs": 0.75, "KTs": 0.5,
            "QJs": 0.75, "QTs": 0.5,
            "JTs": 0.75,
            "T9s": 0.5,
            "98s": 0.5,
            "87s": 0.25,
        },
        'vs_UTG': {
            "JJ": 1.0, "TT": 1.0, "99": 0.75, "88": 0.5, "77": 0.25,
            "AQo": 0.75, "AJo": 0.25,
            "AJs": 0.75, "ATs": 0.5,
            "KQs": 0.75, "KJs": 0.5,
            "QJs": 0.5,
            "JTs": 0.5,
            "T9s": 0.25,
        },
    },
    
    # SB call ranges - should rarely flat (OOP vs BB too)
    'SB': {
        'vs_BTN': {
            "TT": 0.25, "99": 0.5, "88": 0.5, "77": 0.25,
            "AJs": 0.25, "ATs": 0.5,
            "KQs": 0.25, "KJs": 0.5, "KTs": 0.5,
            "QJs": 0.5, "QTs": 0.5,
            "JTs": 0.75,
            "T9s": 0.5,
            "98s": 0.5,
        },
        'vs_CO': {
            "99": 0.5, "88": 0.25,
            "ATs": 0.5,
            "KJs": 0.5, "KTs": 0.5,
            "QJs": 0.5,
            "JTs": 0.5,
        },
        'vs_HJ': {
            "ATs": 0.25,
            "KJs": 0.25,
            "QJs": 0.25,
            "JTs": 0.25,
        },
        'vs_UTG': {
            "JTs": 0.25,
        },
    },
    
    # BTN call ranges - can flat with position
    'BTN': {
        'vs_CO': {
            "TT": 0.25, "99": 0.5, "88": 0.75, "77": 1.0,
            "66": 0.75, "55": 0.5,
            "AJo": 0.75, "ATo": 0.75,
            "ATs": 0.25, "A9s": 0.75, "A8s": 0.5, "A7s": 0.5,
            "KQo": 0.25, "KJo": 0.5,
            "KJs": 0.25, "KTs": 0.5, "K9s": 0.75,
            "QJo": 0.5,
            "QJs": 0.5, "QTs": 0.75, "Q9s": 0.5,
            "JTo": 0.5,
            "JTs": 0.75, "J9s": 0.75,
            "T9s": 1.0, "T8s": 0.5,
            "98s": 1.0,
            "87s": 0.75,
            "76s": 0.5,
            "65s": 0.5,
        },
        'vs_HJ': {
            "99": 0.5, "88": 0.75, "77": 0.75, "66": 0.5, "55": 0.25,
            "AJo": 0.5, "ATo": 0.5,
            "ATs": 0.5, "A9s": 0.75,
            "KJo": 0.25,
            "KJs": 0.5, "KTs": 0.5,
            "QJs": 0.5, "QTs": 0.5,
            "JTs": 0.75,
            "T9s": 0.75,
            "98s": 0.75,
            "87s": 0.5,
        },
        'vs_UTG': {
            "99": 0.5, "88": 0.5, "77": 0.5, "66": 0.25,
            "AJo": 0.25,
            "ATs": 0.5, "A9s": 0.5,
            "KJs": 0.25,
            "QJs": 0.25,
            "JTs": 0.5,
            "T9s": 0.5,
            "98s": 0.5,
        },
    },
    
    # CO call ranges
    'CO': {
        'vs_HJ': {
            "99": 0.5, "88": 0.5, "77": 0.5,
            "66": 0.25,
            "AJo": 0.5, "ATo": 0.25,
            "ATs": 0.5, "A9s": 0.5,
            "KJs": 0.5,
            "QJs": 0.5,
            "JTs": 0.75,
            "T9s": 0.5,
            "98s": 0.5,
        },
        'vs_UTG': {
            "99": 0.25, "88": 0.5, "77": 0.25,
            "ATs": 0.5,
            "KJs": 0.25,
            "QJs": 0.25,
            "JTs": 0.5,
            "T9s": 0.25,
        },
    },
    
    # HJ call ranges
    'HJ': {
        'vs_UTG': {
            "99": 0.25, "88": 0.25,
            "ATs": 0.25,
            "KJs": 0.25,
            "JTs": 0.25,
        },
    },
}

# Call aliases
CALL['BB']['vs_MP'] = CALL['BB']['vs_HJ']
CALL['BB']['vs_EP'] = CALL['BB']['vs_UTG']
CALL['SB']['vs_MP'] = CALL['SB']['vs_HJ']
CALL['SB']['vs_EP'] = CALL['SB']['vs_UTG']
CALL['BTN']['vs_MP'] = CALL['BTN']['vs_HJ']
CALL['BTN']['vs_EP'] = CALL['BTN']['vs_UTG']
CALL['CO']['vs_MP'] = CALL['CO']['vs_HJ']
CALL['CO']['vs_EP'] = CALL['CO']['vs_UTG']


# =============================================================================
# RANGE MANAGER
# =============================================================================

class RangeManager:
    """
    Minimal range manager for Oracle v3.
    
    Core functions:
    - get_postflop_range(): Build hero's range from position + PFR status
    - get_hand_percentile(): "Where am I in my range?"
    
    Uses shared hand_categories module for consistent scoring.
    """
    
    def get_rfi_range(self, position: str) -> Dict[str, float]:
        """Get RFI (raise first in) range for position."""
        pos = position.upper()
        if pos == 'MP':
            pos = 'HJ'
        elif pos == 'EP':
            pos = 'UTG'
        return RFI.get(pos, RFI['HJ']).copy()
    
    def get_defend_range(self, hero_pos: str, vs_position: str) -> Dict[str, float]:
        """Get defending range (call + 3bet combined) vs opener."""
        hero = hero_pos.upper()
        vs = vs_position.upper()
        
        if hero not in DEFEND:
            return DEFEND['BB']['vs_BTN'].copy()
        
        vs_key = f"vs_{vs}"
        if vs_key not in DEFEND[hero]:
            if vs in ('UTG', 'EP'):
                vs_key = 'vs_UTG' if 'vs_UTG' in DEFEND[hero] else 'vs_HJ'
            elif vs in ('HJ', 'MP'):
                vs_key = 'vs_HJ' if 'vs_HJ' in DEFEND[hero] else 'vs_CO'
            else:
                vs_key = 'vs_BTN' if 'vs_BTN' in DEFEND[hero] else 'vs_CO'
        
        if vs_key in DEFEND[hero]:
            return DEFEND[hero][vs_key].copy()
        
        return DEFEND['BB']['vs_BTN'].copy()
    
    def get_3bet_range(self, hero_pos: str, vs_position: str) -> Dict[str, float]:
        """
        Get 3bet range for hero position vs opener.
        
        Args:
            hero_pos: Hero's position (BB, SB, BTN, CO, HJ)
            vs_position: Opener's position (UTG, HJ, CO, BTN)
        
        Returns:
            Dict of {hand: frequency}
        """
        hero = hero_pos.upper()
        vs = vs_position.upper()
        
        # Normalize position names
        if vs == 'MP':
            vs = 'HJ'
        elif vs == 'EP':
            vs = 'UTG'
        
        # Get range
        if hero not in THREEB:
            return THREEB['BB']['vs_BTN'].copy()
        
        vs_key = f"vs_{vs}"
        if vs_key not in THREEB[hero]:
            # Find closest match
            if vs in ('UTG', 'EP'):
                vs_key = 'vs_UTG' if 'vs_UTG' in THREEB[hero] else list(THREEB[hero].keys())[0]
            elif vs in ('HJ', 'MP'):
                vs_key = 'vs_HJ' if 'vs_HJ' in THREEB[hero] else 'vs_CO'
            else:
                vs_key = 'vs_BTN' if 'vs_BTN' in THREEB[hero] else list(THREEB[hero].keys())[-1]
        
        if vs_key in THREEB[hero]:
            return THREEB[hero][vs_key].copy()
        
        return THREEB['BB']['vs_BTN'].copy()
    
    def get_call_range(self, hero_pos: str, vs_position: str) -> Dict[str, float]:
        """
        Get call range for hero position vs opener.
        
        Args:
            hero_pos: Hero's position (BB, SB, BTN, CO, HJ)
            vs_position: Opener's position (UTG, HJ, CO, BTN)
        
        Returns:
            Dict of {hand: frequency}
        """
        hero = hero_pos.upper()
        vs = vs_position.upper()
        
        # Normalize position names
        if vs == 'MP':
            vs = 'HJ'
        elif vs == 'EP':
            vs = 'UTG'
        
        # Get range
        if hero not in CALL:
            return CALL['BB']['vs_BTN'].copy()
        
        vs_key = f"vs_{vs}"
        if vs_key not in CALL[hero]:
            # Find closest match
            if vs in ('UTG', 'EP'):
                vs_key = 'vs_UTG' if 'vs_UTG' in CALL[hero] else list(CALL[hero].keys())[0]
            elif vs in ('HJ', 'MP'):
                vs_key = 'vs_HJ' if 'vs_HJ' in CALL[hero] else 'vs_CO'
            else:
                vs_key = 'vs_BTN' if 'vs_BTN' in CALL[hero] else list(CALL[hero].keys())[-1]
        
        if vs_key in CALL[hero]:
            return CALL[hero][vs_key].copy()
        
        return CALL['BB']['vs_BTN'].copy()
    
    def get_3bet_range(self, hero_pos: str, vs_position: str) -> Dict[str, float]:
        """
        Get 3-bet range for hero position vs opener position.
        
        Based on GTO solver data for 100bb 6-max cash game.
        Range is POLARIZED: Value (premiums) + Bluffs (blockers).
        
        Args:
            hero_pos: Hero's position (BB, SB, BTN, CO, HJ)
            vs_position: Opener's position (UTG, HJ, CO, BTN)
        
        Returns:
            Dict of {hand: frequency} for 3-betting
        """
        hero = hero_pos.upper()
        vs = vs_position.upper()
        
        if hero not in THREE_BET:
            return THREE_BET.get('BB', {}).get('vs_BTN', {}).copy()
        
        vs_key = f"vs_{vs}"
        if vs_key not in THREE_BET[hero]:
            if vs in ('UTG', 'EP'):
                vs_key = 'vs_UTG' if 'vs_UTG' in THREE_BET[hero] else 'vs_HJ'
            elif vs in ('HJ', 'MP'):
                vs_key = 'vs_HJ' if 'vs_HJ' in THREE_BET[hero] else 'vs_CO'
            else:
                vs_key = 'vs_BTN' if 'vs_BTN' in THREE_BET[hero] else 'vs_CO'
        
        if vs_key in THREE_BET[hero]:
            return THREE_BET[hero][vs_key].copy()
        
        return THREE_BET.get('BB', {}).get('vs_BTN', {}).copy()
    
    def get_call_vs_3bet_range(self, hero_pos: str, vs_position: str) -> Dict[str, float]:
        """
        Get hero's calling range when facing a 3-bet after opening.

        Used in the DEFEND_3BET scenario: hero opened, villain 3-bet, hero decides
        whether to 4-bet, call, or fold. This returns the hands hero flat-calls.

        Args:
            hero_pos: Hero's position (UTG, HJ, CO, BTN, SB, BB)
            vs_position: 3-bettor's position (BB, SB, BTN, CO, HJ, UTG)

        Returns:
            Dict of {hand: frequency} for calling a 3-bet. Empty dict means fold everything.
        """
        hero = hero_pos.upper()
        vs = vs_position.upper()

        if hero not in CALL_VS_3BET:
            return {}

        vs_key = f"vs_{vs}"
        if vs_key in CALL_VS_3BET[hero]:
            return CALL_VS_3BET[hero][vs_key].copy()

        # Fallback: tightest available key
        available = list(CALL_VS_3BET[hero].keys())
        if available:
            return CALL_VS_3BET[hero][available[0]].copy()
        return {}

    def get_fourbet_range(self, hero_pos: str) -> Dict[str, float]:
        """
        Get hero's 4-bet range after opening and facing a 3-bet.

        The 4-bet range is position-only (not opponent-specific) because 4-bet
        ranges don't vary much by opponent position — they're anchored to hero's
        position and opening range width.

        Args:
            hero_pos: Hero's position (UTG, HJ, CO, BTN, SB, BB)

        Returns:
            Dict of {hand: frequency} for 4-betting.
        """
        hero = hero_pos.upper()
        return FOURBET.get(hero, FOURBET.get('CO', {})).copy()

    def get_postflop_range(self, position: str, is_pfr: bool,
                           vs_position: Optional[str] = None) -> Dict[str, float]:
        """
        Get player's range entering postflop.
        
        Args:
            position: Player's position (BTN, CO, HJ, etc.)
            is_pfr: Was this player the preflop raiser?
            vs_position: If not PFR, who opened?
        
        Returns:
            Dict of {hand: frequency}
        """
        if is_pfr:
            return self.get_rfi_range(position)
        elif vs_position:
            return self.get_defend_range(position, vs_position)
        else:
            return self.get_defend_range(position, 'BTN')
    
    def get_hand_percentile(self, hand: str, range_dict: Dict[str, float],
                            board: List[str], blocker_aware: bool = True) -> float:
        """
        Get percentile of hand within range on this board.
        
        This is the critical "top of range" calculation.
        
        Args:
            hand: Hand notation (e.g., 'AKo', 'JJ')
            range_dict: Hero's range to evaluate against
            board: Board cards
            blocker_aware: If True, use exact combo counts minus blockers.
        
        Returns:
            Percentile 0.0-1.0 (1.0 = best in range)
        """
        hand = normalize_hand(hand)
        
        hero_strength = self._estimate_hand_strength(hand, board)
        
        in_range = hand in range_dict and range_dict[hand] > 0
        
        # Build blocker set from board
        blockers = set()
        for card in board:
            if len(card) >= 2:
                blockers.add((card[0].upper(), card[1].lower()))
        
        better_count = 0.0
        worse_count = 0.0
        equal_count = 0.0
        
        for other_hand, freq in range_dict.items():
            if freq <= 0:
                continue
            
            if blocker_aware and board:
                combos = count_combos_with_blockers(other_hand, blockers)
            else:
                combos = combo_count(other_hand)
            
            if combos <= 0:
                continue
            
            weight = freq * combos
            other_strength = self._estimate_hand_strength(other_hand, board)
            
            if other_strength > hero_strength:
                better_count += weight
            elif other_strength < hero_strength:
                worse_count += weight
            else:
                equal_count += weight
        
        total = better_count + worse_count + equal_count
        if total == 0:
            return 0.5
        
        percentile = (worse_count + equal_count * 0.5) / total
        
        if not in_range:
            percentile = percentile * 0.95
        
        return percentile
    
    def get_combo_count(self, hand_notation: str) -> int:
        """Get canonical combo count for hand notation."""
        return combo_count(hand_notation)
    
    def get_range_size(self, range_dict: Dict[str, float],
                       blockers: Optional[set] = None) -> float:
        """Get total weighted combo count for a range."""
        total = 0.0
        for hand, freq in range_dict.items():
            if freq <= 0:
                continue
            if blockers:
                combos = count_combos_with_blockers(hand, blockers)
            else:
                combos = combo_count(hand)
            total += freq * combos
        return total
    
    # =========================================================================
    # HAND STRENGTH ESTIMATION
    # =========================================================================
    
    def _estimate_hand_strength(self, hand: str, board: List[str]) -> float:
        """
        Compute deterministic hand strength for percentile ranking.
        
        Returns a score in [0.0, 1.0] using shared CATEGORY_BASE scoring.
        """
        hand = normalize_hand(hand)
        
        if not board:
            return self._preflop_strength(hand)
        
        # Parse hand and board
        h_ranks, h_suits = self._parse_hand(hand, board)
        b_ranks = [RANK_VALUES.get(c[0].upper(), 7) for c in board]
        b_suits = [c[1].lower() for c in board]
        
        # Detect hand category and compute tiebreaker
        category, tiebreaker = self._categorize_hand(h_ranks, h_suits, b_ranks, b_suits)
        
        # Compute final score using shared constants
        base = CATEGORY_BASE.get(category, 0.06)
        margin = CATEGORY_MARGIN.get(category, 0.05)
        
        tiebreaker = min(tiebreaker, margin - 0.001)
        tiebreaker = max(tiebreaker, 0.0)
        
        return base + tiebreaker
    
    def _preflop_strength(self, hand: str) -> float:
        """Compute preflop hand strength."""
        hand = normalize_hand(hand)
        
        if len(hand) >= 2 and hand[0] == hand[1]:
            rank = RANK_VALUES.get(hand[0], 7)
            return 0.50 + (rank - 2) / 24
        
        r1 = RANK_VALUES.get(hand[0], 7)
        r2 = RANK_VALUES.get(hand[1] if len(hand) > 1 else hand[0], 7)
        
        base = (r1 + r2 - 4) / 24
        
        if hand.endswith('s'):
            base += 0.04
        
        gap = abs(r1 - r2) - 1
        if gap == 0:
            base += 0.02
        elif gap == 1:
            base += 0.01
        
        return min(0.95, max(0.05, base))
    
    def _categorize_hand(self, h_ranks: List[int], h_suits: List[str],
                         b_ranks: List[int], b_suits: List[str]) -> Tuple[str, float]:
        """Categorize made hand and compute tiebreaker."""
        all_ranks = h_ranks + b_ranks
        all_suits = h_suits + b_suits
        max_board = max(b_ranks) if b_ranks else 7
        
        # Count suits for flush detection
        suit_counts = {}
        for s in all_suits:
            suit_counts[s] = suit_counts.get(s, 0) + 1
        
        # Count ranks for pair/set detection
        rank_counts = {}
        for r in all_ranks:
            rank_counts[r] = rank_counts.get(r, 0) + 1
        
        # Flush check
        flush_suit = None
        for s, count in suit_counts.items():
            if count >= 5:
                flush_suit = s
                break
        has_flush = flush_suit is not None
        
        # Straight check - use shared function
        straight_high = check_straight(all_ranks)
        has_straight = straight_high is not None
        
        # Straight flush
        if has_flush and has_straight:
            flush_ranks = []
            for i, s in enumerate(h_suits):
                if s == flush_suit:
                    flush_ranks.append(h_ranks[i])
            for i, s in enumerate(b_suits):
                if s == flush_suit:
                    flush_ranks.append(b_ranks[i])
            
            sf_high = check_straight(flush_ranks)
            if sf_high:
                tiebreaker = (sf_high - 5) / 9
                return ('straight_flush', tiebreaker * CATEGORY_MARGIN['straight_flush'])
        
        # Quads
        quads_rank = None
        for r, count in rank_counts.items():
            if count >= 4:
                quads_rank = r
                break
        
        if quads_rank:
            kickers = sorted([r for r in all_ranks if r != quads_rank], reverse=True)
            kicker = kickers[0] if kickers else 2
            tiebreaker = lexicographic_tiebreaker([quads_rank, kicker], 2)
            return ('quads', tiebreaker * CATEGORY_MARGIN['quads'])
        
        # Full house
        trips_ranks = [r for r, c in rank_counts.items() if c >= 3]
        pair_ranks = [r for r, c in rank_counts.items() if c >= 2]
        
        if trips_ranks and len(pair_ranks) >= 2:
            trips_rank = max(trips_ranks)
            pair_rank = max(r for r in pair_ranks if r != trips_rank)
            tiebreaker = lexicographic_tiebreaker([trips_rank, pair_rank], 2)
            return ('full_house', tiebreaker * CATEGORY_MARGIN['full_house'])
        
        # Flush
        if has_flush:
            flush_cards = []
            for i, s in enumerate(h_suits):
                if s == flush_suit:
                    flush_cards.append(h_ranks[i])
            for i, s in enumerate(b_suits):
                if s == flush_suit:
                    flush_cards.append(b_ranks[i])
            flush_cards = sorted(set(flush_cards), reverse=True)[:5]
            
            tiebreaker = 0.0
            for i, card in enumerate(flush_cards[:5]):
                tiebreaker += (card - 2) / (13 ** (i + 1))
            return ('flush', min(tiebreaker, 0.999) * CATEGORY_MARGIN['flush'])
        
        # Straight
        if has_straight:
            tiebreaker = (straight_high - 5) / 9
            return ('straight', tiebreaker * CATEGORY_MARGIN['straight'])
        
        # Three of a kind
        if trips_ranks:
            trips_rank = max(trips_ranks)
            is_set = (len(h_ranks) >= 2 and h_ranks[0] == h_ranks[1] == trips_rank)
            
            kickers = sorted([r for r in all_ranks if r != trips_rank], reverse=True)
            tiebreaker = lexicographic_tiebreaker([trips_rank] + kickers[:2], 3)
            
            if is_set:
                return ('set', tiebreaker * CATEGORY_MARGIN['set'])
            else:
                return ('trips', tiebreaker * CATEGORY_MARGIN['trips'])
        
        # Two pair
        pairs = sorted([r for r, c in rank_counts.items() if c >= 2], reverse=True)
        
        if len(pairs) >= 2:
            high_pair = pairs[0]
            low_pair = pairs[1]
            kickers = sorted([r for r in all_ranks if r not in [high_pair, low_pair]], reverse=True)
            kicker = kickers[0] if kickers else 2
            
            tiebreaker = lexicographic_tiebreaker([high_pair, low_pair, kicker], 3)
            return ('two_pair', tiebreaker * CATEGORY_MARGIN['two_pair'])
        
        # One pair
        if len(pairs) == 1:
            pair_rank = pairs[0]
            kickers = sorted([r for r in all_ranks if r != pair_rank], reverse=True)
            
            is_pocket_pair = (len(h_ranks) >= 2 and h_ranks[0] == h_ranks[1])
            
            if is_pocket_pair and pair_rank not in b_ranks:
                if pair_rank > max_board:
                    tiebreaker = lexicographic_tiebreaker([pair_rank] + kickers[:1], 2)
                    return ('overpair', tiebreaker * CATEGORY_MARGIN['overpair'])
                else:
                    tiebreaker = lexicographic_tiebreaker([pair_rank] + kickers[:2], 3)
                    return ('low_pair', tiebreaker * CATEGORY_MARGIN['low_pair'])
            
            if pair_rank in b_ranks:
                board_sorted = sorted(b_ranks, reverse=True)
                hero_kickers = sorted([r for r in h_ranks if r != pair_rank], reverse=True)
                kicker = hero_kickers[0] if hero_kickers else (kickers[0] if kickers else 2)
                
                if pair_rank == board_sorted[0]:
                    tiebreaker = lexicographic_tiebreaker([pair_rank, kicker], 2)
                    return ('top_pair', tiebreaker * CATEGORY_MARGIN['top_pair'])
                elif len(board_sorted) > 1 and pair_rank == board_sorted[1]:
                    tiebreaker = lexicographic_tiebreaker([pair_rank, kicker], 2)
                    return ('mid_pair', tiebreaker * CATEGORY_MARGIN['mid_pair'])
                else:
                    tiebreaker = lexicographic_tiebreaker([pair_rank, kicker], 2)
                    return ('low_pair', tiebreaker * CATEGORY_MARGIN['low_pair'])
            
            tiebreaker = lexicographic_tiebreaker([pair_rank] + kickers[:2], 3)
            return ('pair', tiebreaker * CATEGORY_MARGIN['pair'])
        
        # Draws - use shared function
        flush_draw = any(c == 4 for c in suit_counts.values())
        straight_draw = has_straight_draw(all_ranks)
        
        if flush_draw and straight_draw:
            tiebreaker = lexicographic_tiebreaker(sorted(h_ranks, reverse=True), 2)
            return ('flush_draw', tiebreaker * CATEGORY_MARGIN['flush_draw'])
        elif flush_draw:
            tiebreaker = lexicographic_tiebreaker(sorted(h_ranks, reverse=True), 2)
            return ('flush_draw', tiebreaker * CATEGORY_MARGIN['flush_draw'])
        elif straight_draw:
            tiebreaker = lexicographic_tiebreaker(sorted(h_ranks, reverse=True), 2)
            return ('straight_draw', tiebreaker * CATEGORY_MARGIN['straight_draw'])
        
        # High card / overcards
        if len(h_ranks) >= 2:
            if h_ranks[0] > max_board and h_ranks[1] > max_board:
                tiebreaker = lexicographic_tiebreaker(sorted(h_ranks, reverse=True), 2)
                return ('overcards', tiebreaker * CATEGORY_MARGIN['overcards'])
            elif h_ranks[0] > max_board or h_ranks[1] > max_board:
                tiebreaker = lexicographic_tiebreaker(sorted(h_ranks, reverse=True), 2)
                return ('high_card', tiebreaker * CATEGORY_MARGIN['high_card'])
        
        tiebreaker = lexicographic_tiebreaker(sorted(h_ranks, reverse=True), 2)
        return ('nothing', tiebreaker * CATEGORY_MARGIN['nothing'])
    
    def _parse_hand(self, hand: str, board: List[str]) -> Tuple[List[int], List[str]]:
        """Parse hand notation into ranks and suits."""
        hand = normalize_hand(hand)
        
        board_suits = [c[1].lower() for c in board]
        suit_counts = {}
        for s in board_suits:
            suit_counts[s] = suit_counts.get(s, 0) + 1
        
        flush_suit = None
        flush_count = 0
        for s, c in suit_counts.items():
            if c >= 3:
                flush_suit = s
                flush_count = c
                break
        
        if len(hand) == 2 and hand[0] == hand[1]:
            r = RANK_VALUES.get(hand[0], 7)
            if flush_suit:
                non_flush = [s for s in 'shdc' if s != flush_suit]
                return [r, r], [non_flush[0], non_flush[1]]
            return [r, r], ['s', 'h']
        
        r1 = RANK_VALUES.get(hand[0], 7)
        r2 = RANK_VALUES.get(hand[1], 7)
        
        if hand.endswith('s'):
            if flush_suit and flush_count >= 3:
                return [r1, r2], [flush_suit, flush_suit]
            else:
                for suit in 'shdc':
                    if suit_counts.get(suit, 0) >= 2:
                        return [r1, r2], [suit, suit]
                return [r1, r2], ['s', 's']
        else:
            if flush_suit and flush_count >= 4:
                non_flush = [s for s in 'shdc' if s != flush_suit]
                return [r1, r2], [non_flush[0], non_flush[1]]
            elif flush_suit and flush_count == 3:
                non_flush = [s for s in 'shdc' if s != flush_suit]
                return [r1, r2], [non_flush[0], flush_suit]
            else:
                return [r1, r2], ['s', 'h']
    
    def is_ip(self, position: str) -> bool:
        """Check if position is typically in position postflop."""
        return position.upper() in IP_POSITIONS


# =============================================================================
# SINGLETON
# =============================================================================

_manager = None

def get_range_manager() -> RangeManager:
    """Get singleton RangeManager instance."""
    global _manager
    if _manager is None:
        _manager = RangeManager()
    return _manager


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    rm = RangeManager()
    
    print("=== Range Manager v3 - Using Shared hand_categories ===\n")
    
    # Test 1: Verify shared constants are imported
    print("1. Shared constants imported from hand_categories:")
    print(f"  CATEGORY_BASE['flush'] = {CATEGORY_BASE['flush']}")
    print(f"  CATEGORY_BASE['straight'] = {CATEGORY_BASE['straight']}")
    print(f"  RANK_VALUES['A'] = {RANK_VALUES['A']}")
    
    # Test 2: Range sizes
    print("\n2. Range sizes:")
    for pos in ['UTG', 'CO', 'BTN']:
        rfi = rm.get_rfi_range(pos)
        size = rm.get_range_size(rfi)
        print(f"  {pos} RFI: {size:.1f} combos")
    
    # Test 3: Percentiles on board
    print("\n3. Percentiles on Ks-7h-2d (BTN RFI):")
    board = ['Ks', '7h', '2d']
    btn_range = rm.get_rfi_range('BTN')
    
    for hand in ['KK', 'AKo', 'KQs', '77', 'AA', '99', 'AQs']:
        pct = rm.get_hand_percentile(hand, btn_range, board)
        score = rm._estimate_hand_strength(hand, board)
        print(f"  {hand:<5}: score={score:.4f}, percentile={pct*100:5.1f}%")
    
    # Test 4: Shared function usage
    print("\n4. Shared function tests:")
    print(f"  check_straight([14,13,12,11,10]) = {check_straight([14,13,12,11,10])}")
    print(f"  has_straight_draw([9,8,7,6]) = {has_straight_draw([9,8,7,6])}")
    print(f"  cards_to_notation('Ah','Kd') = {cards_to_notation('Ah','Kd')}")
    print(f"  combo_count('AA') = {combo_count('AA')}")
    
    print("\n=== Tests Complete ===")
