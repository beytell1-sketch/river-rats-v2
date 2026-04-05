"""
SpotObservation -- the single source of truth for teaching content.

Built once per hand by an ObservationBuilder. Read by the LevelRenderer
at Beginner, Intermediate, or Advanced to produce 2-3 sentences.

All three levels read the SAME SpotObservation. They cannot disagree
on facts because they share the same data. They differ only in which
fields they render and what vocabulary they use.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Tuple


@dataclass(frozen=True)
class SpotObservation:
    """Everything the renderer needs to produce teaching text."""

    # -- Identity --
    action: str                          # CHECK, BET, CALL, FOLD, RAISE
    strategic_role: str                  # pot_control, semi_bluff, value_bet, etc.
    hand_bucket: str                     # monster, strong_made, medium_made, weak_made, drawing, air

    # -- Hand strength --
    hand_description: str                # "top pair, top kicker"
    hand_description_cap: str            # "Top pair, top kicker"
    equity: float                        # 0-1
    worse_hand_pct: float                # 0-1 (what % of villain's range hero beats)
    better_hand_pct: float               # 0-1 (what % beats hero)

    # -- Board context --
    board_texture_label: str             # "dry", "moderate", "dangerous"
    danger_score: float                  # 0-1

    # -- Draw info --
    has_draw: bool
    draw_outs: int                       # 0-15
    draw_description: str                # "flush draw", "straight draw", ""
    draw_equity: float                   # 0-1

    # -- Pot odds --
    pot_odds_pct: float                  # Correct pot odds (0-100)
    equity_margin: float                 # equity - pot_odds (can be negative)
    facing_bet: bool

    # -- Position --
    is_ip: bool
    hero_position: str                   # "BTN", "BB", etc.
    villain_position: str                # "UTG", "CO", etc.
    opponent_phrase: str                 # "your opponent" / "your opponents"

    # -- Multiway --
    num_opponents: int
    is_multiway: bool                    # num_opponents > 1

    # -- Range decomposition (Advanced only, may be None) --
    value_target_pct: float = 0.0        # % of calling range that's worse
    top_threats: str = ""                # "nut flush (3%), sets (2%)"
    hero_label: str = ""                 # "J-high flush" from RangeBreakdown


    # -- Blocker info (Advanced only) --
    blocker_description: str = ""        # "Your cards block villain's value hands"

    # -- Villain range state (Decision A) --
    villain_range_state: Optional[str] = None    # "capped", "polar", "value_weighted", etc.
    villain_range_confidence: float = 0.0         # 0-1 from classifier

    # -- Villain composition (Decision B -- from range_decomposition) --
    villain_tp_plus_pct: float = 0.0     # % of villain range TP+
    villain_draw_pct: float = 0.0        # % of villain range with draws
    villain_air_pct: float = 0.0         # % of villain range with air

    # -- Strategic context --
    spr: float = 10.0
    is_3bet_pot: bool = False

    # -- Counterintuitive handling --
    is_counterintuitive: bool = False    # True when action contradicts hand strength
    counterintuitive_reason: str = ""    # "thin_value_target", "fold_equity_draw", etc.

    # -- Tightness --
    tightness: str = "SILENCE"           # TOSS_UP, CLOSE, SILENCE
    confidence: float = 0.0             # Oracle confidence 0-1

    # -- Sprint 2: Multiway data fields --
    is_nut_draw: bool = False                # Hero holds Ace of flush suit (flush draw) or draw to nut straight
    villain_aggression_streets: int = 0      # 0-3, streets where villain bet/raised (street-level, not action-level)
    facing_bet_and_call: bool = False        # Heuristic: facing_bet AND villain_call_count > 0 AND num_opponents >= 2.
                                             # Call may be from a prior street, not necessarily this street.
    facing_check_raise: bool = False         # Heuristic: facing_bet AND num_raises_this_street >= 1.
                                             # May fire on bet-raise sequences, not only true check-raises.
    was_drawing_previous_street: bool = False # Inferred from board reconstruction on river hands
    players_behind_count: int = 0            # IP → 0; OOP → num_opponents (positional approximation)

    # -- Preflop --
    is_preflop: bool = False
    preflop_scenario: Optional[str] = None  # "rfi", "defend_call", "defend_3bet", "squeeze", "bb_option"
    preflop_range_frequency: float = 0.0    # Raw GTO frequency (0-1) for teaching
    preflop_opener_position: str = ""       # Who opened (for defend/3bet scenarios)
    preflop_action_label: str = ""          # "open", "3-bet", "4-bet", "call", "fold"
