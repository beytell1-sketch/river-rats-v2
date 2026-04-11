"""Personality profiles for AI opponents.

Each profile defines thresholds and frequencies that control
how the heuristic AI makes decisions in ai_decision().
"""
from dataclasses import dataclass


@dataclass
class PersonalityProfile:
    """Defines an AI opponent's playing tendencies."""
    name: str = "default"
    # Strength thresholds
    strong_threshold: float = 0.65
    medium_threshold: float = 0.45
    # Strong hand frequencies
    strong_bet_freq: float = 0.70
    strong_raise_freq: float = 0.30
    # Medium hand frequencies
    medium_check_freq: float = 0.80
    medium_bet_freq: float = 0.20
    medium_fold_to_bet: float = 0.20
    # Weak hand frequencies
    weak_bluff_freq: float = 0.10
    weak_fold_to_bet: float = 0.65
    weak_call_freq: float = 0.15
    # Bet sizing (fraction of pot)
    bet_size_min: float = 0.50
    bet_size_max: float = 0.75


# Preset profiles
TAG = PersonalityProfile(
    name="TAG",
    strong_threshold=0.60, medium_threshold=0.45,
    strong_bet_freq=0.80, strong_raise_freq=0.40,
    medium_check_freq=0.70, medium_bet_freq=0.30,
    medium_fold_to_bet=0.30,
    weak_bluff_freq=0.08, weak_fold_to_bet=0.75, weak_call_freq=0.10,
    bet_size_min=0.55, bet_size_max=0.75,
)

LAG = PersonalityProfile(
    name="LAG",
    strong_threshold=0.55, medium_threshold=0.40,
    strong_bet_freq=0.85, strong_raise_freq=0.50,
    medium_check_freq=0.50, medium_bet_freq=0.50,
    medium_fold_to_bet=0.15,
    weak_bluff_freq=0.25, weak_fold_to_bet=0.45, weak_call_freq=0.20,
    bet_size_min=0.60, bet_size_max=0.90,
)

NIT = PersonalityProfile(
    name="NIT",
    strong_threshold=0.70, medium_threshold=0.55,
    strong_bet_freq=0.60, strong_raise_freq=0.20,
    medium_check_freq=0.90, medium_bet_freq=0.10,
    medium_fold_to_bet=0.40,
    weak_bluff_freq=0.02, weak_fold_to_bet=0.85, weak_call_freq=0.08,
    bet_size_min=0.40, bet_size_max=0.60,
)

CALLING_STATION = PersonalityProfile(
    name="CALLING_STATION",
    strong_threshold=0.60, medium_threshold=0.35,
    strong_bet_freq=0.50, strong_raise_freq=0.15,
    medium_check_freq=0.60, medium_bet_freq=0.10,
    medium_fold_to_bet=0.05,
    weak_bluff_freq=0.05, weak_fold_to_bet=0.20, weak_call_freq=0.50,
    bet_size_min=0.40, bet_size_max=0.60,
)

MANIAC = PersonalityProfile(
    name="MANIAC",
    strong_threshold=0.50, medium_threshold=0.30,
    strong_bet_freq=0.90, strong_raise_freq=0.60,
    medium_check_freq=0.30, medium_bet_freq=0.70,
    medium_fold_to_bet=0.10,
    weak_bluff_freq=0.40, weak_fold_to_bet=0.30, weak_call_freq=0.20,
    bet_size_min=0.70, bet_size_max=1.00,
)

FISH = PersonalityProfile(
    name="FISH",
    strong_threshold=0.55, medium_threshold=0.35,
    strong_bet_freq=0.50, strong_raise_freq=0.20,
    medium_check_freq=0.60, medium_bet_freq=0.15,
    medium_fold_to_bet=0.15,
    weak_bluff_freq=0.15, weak_fold_to_bet=0.40, weak_call_freq=0.30,
    bet_size_min=0.30, bet_size_max=0.90,
)
