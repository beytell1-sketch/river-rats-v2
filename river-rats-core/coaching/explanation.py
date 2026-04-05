"""
Explanation — v3 coaching output dataclass.

Field names preserved for API compatibility.
Semantics updated: headline is the decision report,
supporting is situation observations (not signal topics).
"""

from dataclasses import dataclass
from typing import Optional, Tuple

from coaching.levels import PlayerLevel


@dataclass(frozen=True)
class Explanation:
    """
    Complete coaching output for one hand at one player level.

    headline:   Decision report. "GTO bets here."
    supporting: Situation observations. ("You have top pair...", "The board is dry...")
    qualifier:  Tightness sentence + optional causal bridge. None if SILENCE + no bridge.
    is_mixed:   True when top-two-gap < 0.20 (TOSS-UP).
    action:     "FOLD" / "CHECK" / "CALL" / "BET" / "RAISE"
    confidence: Oracle confidence 0.0-1.0.
    """
    headline: str
    supporting: Tuple[str, ...]
    qualifier: Optional[str]
    is_mixed: bool
    action: str
    confidence: float
    sizing_bucket: Optional[str] = None
    sizing_pot_ratio: Optional[float] = None
    multiway_adjusted: bool = False
    level: PlayerLevel = PlayerLevel.L1_PERCEPTION
