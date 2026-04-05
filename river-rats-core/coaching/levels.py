"""
PlayerLevel — teaching progression enum.

Canonical location for the 5-level player model.
All coaching modules import PlayerLevel from here.
"""

from enum import Enum


class PlayerLevel(Enum):
    """Player comprehension level (5-level teaching progression)."""
    L1_PERCEPTION = "L1"       # See the situation
    L2_CAUSE_EFFECT = "L2"     # Understand why it matters
    L3_ARCHITECTURE = "L3"     # See the invisible structure
    L4_MEASUREMENT = "L4"      # Put numbers on the intuition
    L5_SYSTEMS = "L5"          # Think in ranges and balance


# Ordered index for level comparisons (>= L3, etc.)
_LEVEL_ORDER = [
    PlayerLevel.L1_PERCEPTION,
    PlayerLevel.L2_CAUSE_EFFECT,
    PlayerLevel.L3_ARCHITECTURE,
    PlayerLevel.L4_MEASUREMENT,
    PlayerLevel.L5_SYSTEMS,
]


def level_index(level: PlayerLevel) -> int:
    """Return 0-based index for level comparisons. L1=0, L5=4."""
    return _LEVEL_ORDER.index(level)


def level_gte(level: PlayerLevel, threshold: PlayerLevel) -> bool:
    """True if level is at or above threshold."""
    return level_index(level) >= level_index(threshold)
