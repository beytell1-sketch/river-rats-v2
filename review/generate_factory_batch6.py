"""
generate_factory_batch6.py — v2.3 supplement situation generator.

Produces the 10 factory-sourced buckets for Section 1 rows 1-5, 8, 9, 10, 12, U
of review/comms/V23_HAND_GENERATION_PLAN_2026-04-16.md §1.2.

Buckets (bucket tag, action, street, BP net, OS overshoot):
    MM_IP_TURN    BET   turn        30  / 38
    MM_IP_FLOP    BET   flop        15  / 19
    MM_OOP_TURN   BET   turn        20  / 25
    SM_IP_TURN    BET   turn        20  / 25
    SM_IP_RIVER   BET   river       15  / 19
    MON_CHECKED   BET   flop/turn   15  / 19
    RAISE_VALUE   RAISE flop/turn   20  / 25
    PROT_DANGER   BET   flop        16  / 20
    PFR_CONT      BET   flop        20  / 25
    UMBRELLA      BET/CHECK any     214 / 268

All specs set num_opponents=2 (3-way context). Every record is piped
through normalise_situation() at write time per §1.3. One JSONL per
bucket: training-data/v23_<bucket>.jsonl.

Rows 6, 7 = curated track (not this generator).
Row 11 = solver-sourced (not this generator).

Run:
    python3 review/generate_factory_batch6.py
"""

from __future__ import annotations

import sys
import os
import json
from typing import Callable, Dict, List, Tuple

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_CORE = os.path.join(_REPO, 'river-rats-core')
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)
# Switch cwd so the range data and model assets load correctly.
os.chdir(_CORE)

from situation_factory import (  # noqa: E402
    SituationSpec,
    build_situation,
    validate_situation,
    normalise_situation,
)
from hand_evaluator import evaluate_hand  # noqa: E402


OUTPUT_DIR = os.path.join(_REPO, 'training-data')

# -----------------------------------------------------------------------------
# Sizing conventions (matches batch5 — 3-way, pot=90, eff_stack=450, SPR≈1.11)
# -----------------------------------------------------------------------------
# Flop bets in 90-pot:  30 chips = 33% pot
# Turn bets in 90-pot:  30 chips = 33% pot  (flop check-through keeps pot at 90)
# River bets in 90-pot: 30 chips = 33% pot  (flop + turn check-through)
#
# feature_extractor uses DEFAULT_EFFECTIVE_STACK=100 chips for SPR, so pot=90
# yields SPR ≈ 1.11 — within plan target of SPR 1-2.
# -----------------------------------------------------------------------------

FLOP_BET_SMALL = 30.0  # 33% of 90-pot
TURN_BET_SMALL = 30.0
RIVER_BET_SMALL = 30.0
STD_POT = 90.0
STD_STACK = 450.0

# =============================================================================
# BOARD TEMPLATES
# =============================================================================
# Each board dict is keyed by postflop acting-order archetype:
#   IP_BTN_SB_BB   : hero BTN, villains SB+BB, flop order SB→BB→BTN
#   IP_BTN_HJ_BB   : hero BTN, villains HJ+BB, flop order BB→HJ→BTN
#   IP_CO_SB_BB    : hero CO,  villains SB+BB, flop order SB→BB→CO
#   OOP_SB_CO_BTN  : hero SB,  villains CO+BTN, flop order SB→CO→BTN
#   OOP_BB_HJ_BTN  : hero BB,  villains HJ+BTN, flop order BB→HJ→BTN
#   OOP_BB_CO_BTN  : hero BB,  villains CO+BTN, flop order BB→CO→BTN
#
# "Dry" boards: rainbow, disconnected, one broadway.
# "Dynamic/drawy" boards: two-tone or connected.
# "Wet" boards: two-tone + connected (used sparingly).
# =============================================================================

DRY_BOARDS = [
    # K-high rainbow, disconnected
    ['Kh', '9d', '3c'],
    ['Kd', '7c', '2s'],
    ['Ks', '8c', '3d'],
    # Q-high rainbow disconnected
    ['Qh', '7d', '2c'],
    ['Qc', '8d', '3s'],
    ['Qs', '6d', '2h'],
    # J-high rainbow disconnected
    ['Jd', '8c', '3s'],
    ['Jh', '7c', '2d'],
    ['Js', '6d', '2c'],
    # A-high rainbow disconnected
    ['Ah', '9d', '3c'],
    ['Ac', '7d', '2s'],
    ['As', '8d', '3h'],
    # T-high rainbow disconnected
    ['Td', '6c', '2s'],
    ['Th', '7d', '3c'],
    # 9-high rainbow disconnected
    ['9d', '5c', '2s'],
    ['9h', '4c', '2d'],
]

TWO_TONE_BOARDS = [
    # Two-tone spades
    ['Ts', '6s', '3d'],
    ['Js', '7s', '2d'],
    ['Qs', '8s', '3d'],
    ['Ks', '8s', '4h'],
    # Two-tone hearts
    ['Qh', '8h', '4d'],
    ['Th', '6h', '2d'],
    ['Jh', '7h', '3c'],
    ['9h', '5h', '2c'],
    # Two-tone clubs
    ['Jc', '7c', '2d'],
    ['Qc', '9c', '5h'],
    ['Tc', '6c', '3d'],
    ['Kc', '8c', '4d'],
    # Two-tone diamonds
    ['Ad', '5d', '2c'],
    ['Kd', '9d', '3c'],
    ['Qd', '7d', '2h'],
]

CONNECTED_TWO_TONE_BOARDS = [
    # Drawy / protection-worthy
    ['Th', '9s', '6s'],   # straight draws + FD
    ['Js', 'Ts', '7h'],
    ['Td', '9c', '8c'],
    ['9s', '8s', '5d'],
    ['Qc', 'Tc', '8d'],
    ['Jd', '9d', '8s'],
    ['8h', '7h', '5c'],
    ['9d', '8d', '6c'],
    ['Qh', 'Th', '9s'],
    ['Kh', 'Jh', '9c'],
]

# =============================================================================
# Preflop history templates
# =============================================================================
# Returns action_history with preflop-only actions for the given archetype.
# Always: opener raises 3bb, others call. 3-way pot, not-3bet (is_3bet=0).
# Preflop order uses the standard 6-max PREFLOP_ORDER: UTG/HJ/CO/BTN/SB/BB.


def _preflop_history(opener: str, callers: List[str]) -> List[Tuple[str, str, str]]:
    acts = [('preflop', opener, 'raise')]
    for c in callers:
        acts.append(('preflop', c, 'call'))
    return acts


# -----------------------------------------------------------------------------
# Archetype → (hero_pos, villain_positions, opener, preflop_callers_after_opener)
# -----------------------------------------------------------------------------
#
# For IP-hero archetypes, hero must be last to act postflop.
# For OOP-hero archetypes, hero must act first (SB or BB).

ARCHETYPES_IP = [
    # (hero_pos, villains, opener, postflop_order)
    # Postflop order per _POSTFLOP_ORDER: SB=0, BB=1, HJ=3, CO=4, BTN=5
    ('BTN', ['SB', 'BB'], 'BTN'),   # flop: SB→BB→BTN
    ('BTN', ['HJ', 'BB'], 'BTN'),   # flop: BB→HJ→BTN
    ('BTN', ['CO', 'SB'], 'CO'),    # flop: SB→CO→BTN
    ('CO',  ['SB', 'BB'], 'CO'),    # flop: SB→BB→CO
    ('CO',  ['HJ', 'BB'], 'CO'),    # flop: BB→HJ→CO
    ('CO',  ['SB', 'BTN'], 'BTN'),  # NOT IP vs BTN — skip
]
# Filter out invalid IP archetypes (hero must be last)
from situation_factory import _POSTFLOP_ORDER as _PFO  # noqa: E402
ARCHETYPES_IP = [
    (h, v, o) for (h, v, o) in ARCHETYPES_IP
    if all(_PFO[h] > _PFO[vp] for vp in v)
]

ARCHETYPES_OOP = [
    ('SB', ['CO', 'BTN'], 'CO'),
    ('SB', ['HJ', 'BTN'], 'HJ'),
    ('BB', ['HJ', 'BTN'], 'HJ'),
    ('BB', ['CO', 'BTN'], 'CO'),
    ('BB', ['HJ', 'CO'],  'HJ'),
]


# =============================================================================
# Heroine card catalogues by target hand strength on a given board
# =============================================================================
# We generate hero hands by ASKING the hand_evaluator what category a candidate
# hand makes on a given board, then filtering to the target stratum.
# This is the "canonical definition" anchor per the plan.

# Hand_category tiers per hand_categories.HAND_CATEGORY_VALUES:
#   monster         = trips / set / full_house / quads / straight / flush / straight_flush
#   strong_made     = two_pair / overpair / top_pair_top_kicker / top_pair_good_kicker
#   medium_made     = top_pair (weak kicker) / mid_pair / middle_pair / low_pair / bottom_pair / underpair
#   draw            = flush_draw / straight_draw (no made hand)
#   air             = high_card / overcards / one_overcard / nothing


MONSTER_CATS = {
    'straight_flush', 'quads', 'full_house', 'flush', 'straight',
    'set', 'trips',
}
STRONG_CATS = {
    'two_pair', 'overpair', 'top_pair_top_kicker', 'top_pair_good_kicker',
}
# "Medium made" per plan: pair < top_pair+good_kicker, i.e. weak top pair,
# second pair, third pair, bottom pair, underpair.
MEDIUM_CATS = {
    'top_pair',          # weak-kicker top pair
    'mid_pair', 'middle_pair',
    'low_pair', 'bottom_pair', 'pair',
    'underpair',
}


def _category_of(hero_cards: List[str], board: List[str]) -> str:
    """Return the canonical evaluate_hand category string for hero on board."""
    return evaluate_hand(hero_cards, board).category


def _is_medium(hero_cards, board) -> bool:
    return _category_of(hero_cards, board) in MEDIUM_CATS


def _is_strong(hero_cards, board) -> bool:
    return _category_of(hero_cards, board) in STRONG_CATS


def _is_monster(hero_cards, board) -> bool:
    return _category_of(hero_cards, board) in MONSTER_CATS


# =============================================================================
# Card-pool utilities
# =============================================================================
RANKS_HI = ['A', 'K', 'Q', 'J', 'T']
RANKS_MID = ['9', '8', '7', '6']
RANKS_LO = ['5', '4', '3', '2']
SUITS = ['h', 'd', 'c', 's']


def _all_cards() -> List[str]:
    return [r + s for r in RANKS_HI + RANKS_MID + RANKS_LO for s in SUITS]


def _board_set(board: List[str]) -> set:
    return set(board)


def _pick_hole_cards_of_category(
    board: List[str],
    want: Callable[[List[str], List[str]], bool],
    max_hands: int,
    used: set,
) -> List[List[str]]:
    """
    Return up to max_hands unique 2-card hero hands (not using board cards,
    not duplicating `used`) that satisfy `want(hero_cards, board) == True`.
    """
    dead = _board_set(board) | used
    available = [c for c in _all_cards() if c not in dead]
    found: List[List[str]] = []
    # Deterministic sweep for reproducibility. Deals with both orderings.
    for i in range(len(available)):
        for j in range(i + 1, len(available)):
            cards = [available[i], available[j]]
            try:
                if want(cards, board):
                    found.append(cards)
                    if len(found) >= max_hands:
                        return found
            except Exception:
                continue
    return found


# =============================================================================
# Per-bucket builders
# =============================================================================
#
# Each builder returns a list of tuples:
#   (SituationSpec, description_str)
# where SituationSpec has num_opponents=2 baked in.
# =============================================================================


def _make_spec(
    hero_cards: List[str],
    board: List[str],
    hero_pos: str,
    villain_positions: List[str],
    pot: float,
    to_call: float,
    street: str,
    action_history: List[Tuple[str, str, str]],
    opener_position: str,
    effective_stack: float = STD_STACK,
    current_bet: float = 0.0,
) -> SituationSpec:
    return SituationSpec(
        hero_cards=hero_cards,
        board_cards=board,
        hero_pos=hero_pos,
        villain_positions=villain_positions,
        pot=pot,
        to_call=to_call,
        street=street,
        action_history=action_history,
        opener_position=opener_position,
        effective_stack=effective_stack,
        current_bet=current_bet,
        num_opponents=2,
    )


# -----------------------------------------------------------------------------
# Helper: deal a turn / river card not conflicting with board + hero
# -----------------------------------------------------------------------------

_TURN_CARDS_POOL = ['2h', '3c', '4d', '5s', '6h', '7c', '8d', '9s',
                    'Tc', 'Jd', 'Qh', 'Kc', 'Ad']


def _safe_turn_card(board_flop: List[str], hero_cards: List[str]) -> str:
    dead = set(board_flop) | set(hero_cards)
    for c in _TURN_CARDS_POOL:
        if c not in dead:
            return c
    # Fallback — exhaustive scan
    for c in _all_cards():
        if c not in dead:
            return c
    raise RuntimeError("no turn card available")


def _safe_river_card(board4: List[str], hero_cards: List[str]) -> str:
    dead = set(board4) | set(hero_cards)
    for c in _TURN_CARDS_POOL:
        if c not in dead:
            return c
    for c in _all_cards():
        if c not in dead:
            return c
    raise RuntimeError("no river card available")


# -----------------------------------------------------------------------------
# 1. MM_IP_TURN — medium made, IP, checked-to (turn), SPR 1-2.
#    Preflop raise + callers.  Flop checks through.  Turn: villain(s) check
#    to hero.  Hero has medium made (weak TP / 2nd pair / underpair).
# -----------------------------------------------------------------------------

def build_MM_IP_TURN_specs(target: int = 38) -> List[Tuple[SituationSpec, str]]:
    specs: List[Tuple[SituationSpec, str]] = []
    used: set = set()

    # Preferred boards: dry rainbows (easier to get weak-TP / 2nd pair cleanly)
    board_pool = DRY_BOARDS + TWO_TONE_BOARDS
    for hero_pos, villain_positions, opener in ARCHETYPES_IP:
        for flop in board_pool:
            if len(specs) >= target:
                break
            turn = _safe_turn_card(flop, [])
            board = flop + [turn]
            pre = _preflop_history(
                opener,
                [p for p in villain_positions + [hero_pos] if p != opener],
            )
            # Flop: all check (3-way).  Order is postflop: lowest → highest.
            active_order = sorted(
                villain_positions + [hero_pos],
                key=lambda p: _PFO[p],
            )
            flop_actions = [('flop', p, 'check') for p in active_order]
            # Turn: villains check to hero.  Hero acts last (IP).
            turn_actions = [
                ('turn', p, 'check') for p in active_order if p != hero_pos
            ]
            action_history = pre + flop_actions + turn_actions

            # Medium-made heroes
            heroes = _pick_hole_cards_of_category(
                board, _is_medium, max_hands=3, used=used,
            )
            for hero in heroes:
                if len(specs) >= target:
                    break
                spec = _make_spec(
                    hero_cards=hero,
                    board=board,
                    hero_pos=hero_pos,
                    villain_positions=villain_positions,
                    pot=STD_POT,
                    to_call=0.0,
                    street='turn',
                    action_history=action_history,
                    opener_position=opener,
                )
                desc = (
                    f'MM_IP_TURN: hero {hero_pos} medium made '
                    f'({_category_of(hero, board)}) on {"-".join(board)}; '
                    f'flop checked through, turn checked to hero IP.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
    return specs[:target]


# -----------------------------------------------------------------------------
# 2. MM_IP_FLOP — medium made, IP, flop, not yet acted; villains checked.
# -----------------------------------------------------------------------------

def build_MM_IP_FLOP_specs(target: int = 19) -> List[Tuple[SituationSpec, str]]:
    specs: List[Tuple[SituationSpec, str]] = []
    used: set = set()
    for hero_pos, villain_positions, opener in ARCHETYPES_IP:
        for flop in DRY_BOARDS + TWO_TONE_BOARDS:
            if len(specs) >= target:
                break
            pre = _preflop_history(
                opener,
                [p for p in villain_positions + [hero_pos] if p != opener],
            )
            active_order = sorted(
                villain_positions + [hero_pos],
                key=lambda p: _PFO[p],
            )
            flop_actions = [
                ('flop', p, 'check') for p in active_order if p != hero_pos
            ]
            action_history = pre + flop_actions

            heroes = _pick_hole_cards_of_category(
                flop, _is_medium, max_hands=2, used=used,
            )
            for hero in heroes:
                if len(specs) >= target:
                    break
                spec = _make_spec(
                    hero_cards=hero,
                    board=flop,
                    hero_pos=hero_pos,
                    villain_positions=villain_positions,
                    pot=STD_POT,
                    to_call=0.0,
                    street='flop',
                    action_history=action_history,
                    opener_position=opener,
                )
                desc = (
                    f'MM_IP_FLOP: hero {hero_pos} medium made '
                    f'({_category_of(hero, flop)}) on {"-".join(flop)}; '
                    f'villains checked to hero IP.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
    return specs[:target]


# -----------------------------------------------------------------------------
# 3. MM_OOP_TURN — medium made, OOP, checked-to.  Hero SB/BB, flop checks
#    through, turn: hero leads (first to act, check-to-us isn't literal
#    when hero is OOP, but "checked-to" context means no prior aggression —
#    flop check-through still gives villain_checked_back=1).
# -----------------------------------------------------------------------------

def build_MM_OOP_TURN_specs(target: int = 25) -> List[Tuple[SituationSpec, str]]:
    specs: List[Tuple[SituationSpec, str]] = []
    used: set = set()
    for hero_pos, villain_positions, opener in ARCHETYPES_OOP:
        for flop in DRY_BOARDS + TWO_TONE_BOARDS:
            if len(specs) >= target:
                break
            turn = _safe_turn_card(flop, [])
            board = flop + [turn]
            pre = _preflop_history(
                opener,
                [p for p in villain_positions + [hero_pos] if p != opener],
            )
            active_order = sorted(
                villain_positions + [hero_pos],
                key=lambda p: _PFO[p],
            )
            flop_actions = [('flop', p, 'check') for p in active_order]
            # Turn: hero acts first (OOP) — no turn actions yet.
            action_history = pre + flop_actions

            heroes = _pick_hole_cards_of_category(
                board, _is_medium, max_hands=3, used=used,
            )
            for hero in heroes:
                if len(specs) >= target:
                    break
                spec = _make_spec(
                    hero_cards=hero,
                    board=board,
                    hero_pos=hero_pos,
                    villain_positions=villain_positions,
                    pot=STD_POT,
                    to_call=0.0,
                    street='turn',
                    action_history=action_history,
                    opener_position=opener,
                )
                desc = (
                    f'MM_OOP_TURN: hero {hero_pos} medium made '
                    f'({_category_of(hero, board)}) on {"-".join(board)}; '
                    f'flop checked through, hero OOP leads turn.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
    return specs[:target]


# -----------------------------------------------------------------------------
# 4. SM_IP_TURN — strong made, IP, checked-to, low-danger board (rainbow +
#    disconnected).
# -----------------------------------------------------------------------------

def build_SM_IP_TURN_specs(target: int = 25) -> List[Tuple[SituationSpec, str]]:
    specs: List[Tuple[SituationSpec, str]] = []
    used: set = set()
    for hero_pos, villain_positions, opener in ARCHETYPES_IP:
        for flop in DRY_BOARDS:
            if len(specs) >= target:
                break
            turn = _safe_turn_card(flop, [])
            # Keep the turn safe too — avoid completing flushes (trivial on rainbow).
            board = flop + [turn]
            pre = _preflop_history(
                opener,
                [p for p in villain_positions + [hero_pos] if p != opener],
            )
            active_order = sorted(
                villain_positions + [hero_pos],
                key=lambda p: _PFO[p],
            )
            flop_actions = [('flop', p, 'check') for p in active_order]
            turn_actions = [
                ('turn', p, 'check') for p in active_order if p != hero_pos
            ]
            action_history = pre + flop_actions + turn_actions

            heroes = _pick_hole_cards_of_category(
                board, _is_strong, max_hands=3, used=used,
            )
            for hero in heroes:
                if len(specs) >= target:
                    break
                spec = _make_spec(
                    hero_cards=hero,
                    board=board,
                    hero_pos=hero_pos,
                    villain_positions=villain_positions,
                    pot=STD_POT,
                    to_call=0.0,
                    street='turn',
                    action_history=action_history,
                    opener_position=opener,
                )
                desc = (
                    f'SM_IP_TURN: hero {hero_pos} strong made '
                    f'({_category_of(hero, board)}) on {"-".join(board)}; '
                    f'low-danger dry board, checked-to IP.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
    return specs[:target]


# -----------------------------------------------------------------------------
# 5. SM_IP_RIVER — strong made, IP, checked-to, low-danger.
# -----------------------------------------------------------------------------

def build_SM_IP_RIVER_specs(target: int = 19) -> List[Tuple[SituationSpec, str]]:
    specs: List[Tuple[SituationSpec, str]] = []
    used: set = set()
    for hero_pos, villain_positions, opener in ARCHETYPES_IP:
        for flop in DRY_BOARDS:
            if len(specs) >= target:
                break
            turn = _safe_turn_card(flop, [])
            river = _safe_river_card(flop + [turn], [])
            board = flop + [turn, river]
            pre = _preflop_history(
                opener,
                [p for p in villain_positions + [hero_pos] if p != opener],
            )
            active_order = sorted(
                villain_positions + [hero_pos],
                key=lambda p: _PFO[p],
            )
            flop_actions = [('flop', p, 'check') for p in active_order]
            turn_actions = [('turn', p, 'check') for p in active_order]
            river_actions = [
                ('river', p, 'check') for p in active_order if p != hero_pos
            ]
            action_history = pre + flop_actions + turn_actions + river_actions

            heroes = _pick_hole_cards_of_category(
                board, _is_strong, max_hands=3, used=used,
            )
            for hero in heroes:
                if len(specs) >= target:
                    break
                spec = _make_spec(
                    hero_cards=hero,
                    board=board,
                    hero_pos=hero_pos,
                    villain_positions=villain_positions,
                    pot=STD_POT,
                    to_call=0.0,
                    street='river',
                    action_history=action_history,
                    opener_position=opener,
                )
                desc = (
                    f'SM_IP_RIVER: hero {hero_pos} strong made '
                    f'({_category_of(hero, board)}) on {"-".join(board)}; '
                    f'all streets checked, hero IP decides river.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
    return specs[:target]


# -----------------------------------------------------------------------------
# 8. MON_CHECKED — monster (trips+), any position, checked-to.
# -----------------------------------------------------------------------------

def build_MON_CHECKED_specs(target: int = 19) -> List[Tuple[SituationSpec, str]]:
    specs: List[Tuple[SituationSpec, str]] = []
    used: set = set()
    # Alternate flop / turn, mix IP and OOP.
    archetypes = ARCHETYPES_IP + ARCHETYPES_OOP
    for idx, (hero_pos, villain_positions, opener) in enumerate(archetypes):
        for flop in DRY_BOARDS + TWO_TONE_BOARDS:
            if len(specs) >= target:
                break
            # Alternate streets: flop vs. turn
            use_turn = (len(specs) % 2 == 1)
            if use_turn:
                turn = _safe_turn_card(flop, [])
                board = flop + [turn]
                street = 'turn'
            else:
                board = list(flop)
                street = 'flop'

            pre = _preflop_history(
                opener,
                [p for p in villain_positions + [hero_pos] if p != opener],
            )
            active_order = sorted(
                villain_positions + [hero_pos],
                key=lambda p: _PFO[p],
            )
            if street == 'flop':
                flop_actions = [
                    ('flop', p, 'check') for p in active_order if p != hero_pos
                ] if _PFO[hero_pos] >= _PFO[active_order[-1]] else [
                    ('flop', p, 'check') for p in active_order
                    if _PFO[p] < _PFO[hero_pos]
                ]
                action_history = pre + flop_actions
            else:
                flop_actions = [('flop', p, 'check') for p in active_order]
                turn_actions = [
                    ('turn', p, 'check') for p in active_order if p != hero_pos
                ] if _PFO[hero_pos] >= _PFO[active_order[-1]] else [
                    ('turn', p, 'check') for p in active_order
                    if _PFO[p] < _PFO[hero_pos]
                ]
                action_history = pre + flop_actions + turn_actions

            heroes = _pick_hole_cards_of_category(
                board, _is_monster, max_hands=2, used=used,
            )
            for hero in heroes:
                if len(specs) >= target:
                    break
                spec = _make_spec(
                    hero_cards=hero,
                    board=board,
                    hero_pos=hero_pos,
                    villain_positions=villain_positions,
                    pot=STD_POT,
                    to_call=0.0,
                    street=street,
                    action_history=action_history,
                    opener_position=opener,
                )
                desc = (
                    f'MON_CHECKED: hero {hero_pos} monster '
                    f'({_category_of(hero, board)}) on {"-".join(board)}; '
                    f'checked-to on {street}.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
    return specs[:target]


# -----------------------------------------------------------------------------
# 9. RAISE_VALUE — strong/monster hand facing a villain bet (flop or turn).
#    This is the ONLY facing-bet bucket.  Mixed IP/OOP for diversity.
# -----------------------------------------------------------------------------

def build_RAISE_VALUE_specs(target: int = 25) -> List[Tuple[SituationSpec, str]]:
    specs: List[Tuple[SituationSpec, str]] = []
    used: set = set()

    archetypes = ARCHETYPES_IP + ARCHETYPES_OOP
    for hero_pos, villain_positions, opener in archetypes:
        for flop in DRY_BOARDS + TWO_TONE_BOARDS:
            if len(specs) >= target:
                break
            use_turn = (len(specs) % 2 == 1)
            if use_turn:
                turn = _safe_turn_card(flop, [])
                board = flop + [turn]
                street = 'turn'
            else:
                board = list(flop)
                street = 'flop'

            pre = _preflop_history(
                opener,
                [p for p in villain_positions + [hero_pos] if p != opener],
            )
            active_order = sorted(
                villain_positions + [hero_pos],
                key=lambda p: _PFO[p],
            )

            # Identify a bettor: a villain that acts before hero on the
            # current street (so hero can raise).  For IP-hero, any villain
            # works.  For OOP-hero, we need a villain that acts BEFORE hero —
            # impossible with standard 3-max ordering since hero is earliest.
            # For OOP-hero we instead put the facing-bet on a LATER street
            # (turn check-raise pattern): flop all-check, turn hero checks,
            # villain bets, hero raises.
            is_hero_ip = (_PFO[hero_pos] == max(_PFO[p] for p in active_order))

            if is_hero_ip:
                # Villain(s) bet on current street before hero acts.
                # Pick the latest-acting non-hero seat as the bettor.
                non_hero_ordered = [
                    p for p in active_order if p != hero_pos
                ]
                bettor = non_hero_ordered[-1]
                other_villains = [p for p in non_hero_ordered if p != bettor]
                # Flop checks from earlier villains, then bettor bets.
                if street == 'flop':
                    cur_actions = (
                        [('flop', v, 'check') for v in other_villains]
                        + [('flop', bettor, 'bet')]
                    )
                    action_history = pre + cur_actions
                else:  # turn
                    flop_actions = [
                        ('flop', p, 'check') for p in active_order
                    ]
                    turn_actions = (
                        [('turn', v, 'check') for v in other_villains]
                        + [('turn', bettor, 'bet')]
                    )
                    action_history = pre + flop_actions + turn_actions
                to_call = (
                    FLOP_BET_SMALL if street == 'flop' else TURN_BET_SMALL
                )
                # villain_positions ordering: bettor LAST so the bridge
                # identifies them correctly.
                villains_ordered = other_villains + [bettor]
            else:
                # OOP hero: turn check-raise pattern.  Flop checks through,
                # turn hero checks, last villain bets — hero facing bet.
                if street == 'flop':
                    # For OOP flop, hero acts first — cannot face a bet before
                    # acting unless a donk from an even earlier position, but
                    # hero IS earliest (SB/BB).  Skip flop for OOP-hero.
                    continue
                flop_actions = [('flop', p, 'check') for p in active_order]
                non_hero_ordered = [
                    p for p in active_order if p != hero_pos
                ]
                bettor = non_hero_ordered[-1]
                other_villains = [p for p in non_hero_ordered if p != bettor]
                turn_actions = (
                    [('turn', hero_pos, 'check')]
                    + [('turn', v, 'check') for v in other_villains]
                    + [('turn', bettor, 'bet')]
                )
                action_history = pre + flop_actions + turn_actions
                to_call = TURN_BET_SMALL
                villains_ordered = other_villains + [bettor]

            # Need a pot post-bet for the spec.  The "pot" field in
            # SituationSpec is the pot BEFORE hero's decision — so
            # pot = STD_POT + bet_amount (after bettor commits).
            pot_with_bet = STD_POT + to_call

            heroes = _pick_hole_cards_of_category(
                board,
                lambda h, b: _is_strong(h, b) or _is_monster(h, b),
                max_hands=2,
                used=used,
            )
            for hero in heroes:
                if len(specs) >= target:
                    break
                spec = _make_spec(
                    hero_cards=hero,
                    board=board,
                    hero_pos=hero_pos,
                    villain_positions=villains_ordered,
                    pot=pot_with_bet,
                    to_call=to_call,
                    street=street,
                    action_history=action_history,
                    opener_position=opener,
                    current_bet=to_call,
                )
                desc = (
                    f'RAISE_VALUE: hero {hero_pos} strong/monster '
                    f'({_category_of(hero, board)}) on {"-".join(board)}; '
                    f'facing {street} bet from {bettor}.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
    return specs[:target]


# -----------------------------------------------------------------------------
# 10. PROT_DANGER — medium made on a dynamic/drawy board, flop, facing a
#     check (hero is about to bet for protection).
# -----------------------------------------------------------------------------

def build_PROT_DANGER_specs(target: int = 20) -> List[Tuple[SituationSpec, str]]:
    specs: List[Tuple[SituationSpec, str]] = []
    used: set = set()
    # Dynamic boards only — connected two-tone / connected or two-tone.
    danger_boards = CONNECTED_TWO_TONE_BOARDS + TWO_TONE_BOARDS
    archetypes = ARCHETYPES_IP + ARCHETYPES_OOP
    for hero_pos, villain_positions, opener in archetypes:
        for flop in danger_boards:
            if len(specs) >= target:
                break
            pre = _preflop_history(
                opener,
                [p for p in villain_positions + [hero_pos] if p != opener],
            )
            active_order = sorted(
                villain_positions + [hero_pos],
                key=lambda p: _PFO[p],
            )
            # Flop actions: everyone who acts before hero checks; hero
            # pending decision.
            hero_order = _PFO[hero_pos]
            flop_actions = [
                ('flop', p, 'check') for p in active_order
                if _PFO[p] < hero_order
            ]
            action_history = pre + flop_actions

            heroes = _pick_hole_cards_of_category(
                flop, _is_medium, max_hands=2, used=used,
            )
            for hero in heroes:
                if len(specs) >= target:
                    break
                spec = _make_spec(
                    hero_cards=hero,
                    board=flop,
                    hero_pos=hero_pos,
                    villain_positions=villain_positions,
                    pot=STD_POT,
                    to_call=0.0,
                    street='flop',
                    action_history=action_history,
                    opener_position=opener,
                )
                desc = (
                    f'PROT_DANGER: hero {hero_pos} medium made '
                    f'({_category_of(hero, flop)}) on drawy {"-".join(flop)}; '
                    f'checked-to, protection spot.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
    return specs[:target]


# -----------------------------------------------------------------------------
# 12. PFR_CONT — hero was preflop aggressor (PFR) on a dry flop, checked-to.
#     Hero must be the opener.
# -----------------------------------------------------------------------------

def build_PFR_CONT_specs(target: int = 25) -> List[Tuple[SituationSpec, str]]:
    specs: List[Tuple[SituationSpec, str]] = []
    used: set = set()
    # Archetypes where hero_pos == opener
    archetypes = [
        (h, v, o) for (h, v, o) in ARCHETYPES_IP + ARCHETYPES_OOP
        if h == o
    ]
    for hero_pos, villain_positions, opener in archetypes:
        for flop in DRY_BOARDS:
            if len(specs) >= target:
                break
            pre = _preflop_history(
                opener,
                [p for p in villain_positions + [hero_pos] if p != opener],
            )
            active_order = sorted(
                villain_positions + [hero_pos],
                key=lambda p: _PFO[p],
            )
            hero_order = _PFO[hero_pos]
            # All villains before hero check
            flop_actions = [
                ('flop', p, 'check') for p in active_order
                if _PFO[p] < hero_order
            ]
            action_history = pre + flop_actions

            # PFR cbet hand mix: TPTK-ish, overpair, or air cbet candidates.
            # We'll accept any hand — PFR cbets across the range.
            # But to keep the bucket cohesive, pick broadway/overpair-flavoured
            # hands (strong or medium made OR overcards).
            def _pfr_hand(h, b):
                cat = _category_of(h, b)
                return cat in STRONG_CATS | MEDIUM_CATS | {'overcards', 'one_overcard'}

            heroes = _pick_hole_cards_of_category(
                flop, _pfr_hand, max_hands=3, used=used,
            )
            for hero in heroes:
                if len(specs) >= target:
                    break
                spec = _make_spec(
                    hero_cards=hero,
                    board=flop,
                    hero_pos=hero_pos,
                    villain_positions=villain_positions,
                    pot=STD_POT,
                    to_call=0.0,
                    street='flop',
                    action_history=action_history,
                    opener_position=opener,
                )
                desc = (
                    f'PFR_CONT: hero {hero_pos} PFR cbet '
                    f'({_category_of(hero, flop)}) on dry {"-".join(flop)}; '
                    f'checked-to.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
    return specs[:target]


# -----------------------------------------------------------------------------
# U. UMBRELLA — any checked-to residual matching Section 2 predicate.
#    Predicate: facing_bet=False, num_opponents=2, villain_checked_back=1,
#               villain_range_capped=1, worse_hand_pct >= 0.55,
#               equity_vs_range >= 0.35, SPR <= 2.0.
#
#    We generate checked-to spots across all streets with a mix of hero
#    strengths; predicate compliance is verified post-facto (records that
#    fail the predicate are dropped).
# -----------------------------------------------------------------------------

def build_UMBRELLA_specs(target: int = 268) -> List[Tuple[SituationSpec, str]]:
    specs: List[Tuple[SituationSpec, str]] = []
    used: set = set()

    board_pool = DRY_BOARDS + TWO_TONE_BOARDS + CONNECTED_TWO_TONE_BOARDS

    # Predicate requires villain_checked_back=1 AND villain_range_capped=1.
    #
    # villain_checked_back=1 means the PRIMARY villain checked on a prior
    # street.  Primary villain (when not facing bet) = villain_positions[0]
    # (first in list, per bridge max(...) tie-break on equal stacks).
    # So: primary must have been present on a prior street and checked —
    # flop street CANNOT satisfy this (no prior streets).
    # UMBRELLA therefore uses TURN and RIVER only.
    #
    # villain_range_capped=1 requires not_3bet_pot AND primary villain is
    # NOT the opener.  So primary = non-opener.
    # We reorder villain_positions to put the non-opener FIRST.
    archetypes = []
    for (h, vs, o) in ARCHETYPES_IP + ARCHETYPES_OOP:
        if h == o:
            continue  # Hero is opener — different bucket (PFR_CONT).
        # Reorder villains: non-opener first (primary), opener last.
        non_openers = [p for p in vs if p != o]
        openers_in_list = [p for p in vs if p == o]
        if not non_openers:
            continue  # All villains are openers — impossible but safe.
        reordered = non_openers + openers_in_list
        archetypes.append((h, reordered, o))
    # Cycle streets (turn / river only — flop can't satisfy vcb=1).
    streets_cycle = ['turn', 'river']
    s_idx = 0

    for hero_pos, villain_positions, opener in archetypes:
        for flop in board_pool:
            if len(specs) >= target:
                break
            street = streets_cycle[s_idx % len(streets_cycle)]
            s_idx += 1

            if street == 'turn':
                board = flop + [_safe_turn_card(flop, [])]
            else:  # river
                turn = _safe_turn_card(flop, [])
                river = _safe_river_card(flop + [turn], [])
                board = flop + [turn, river]

            pre = _preflop_history(
                opener,
                [p for p in villain_positions + [hero_pos] if p != opener],
            )
            active_order = sorted(
                villain_positions + [hero_pos],
                key=lambda p: _PFO[p],
            )
            hero_order = _PFO[hero_pos]

            # Build action history for checked-through pattern.
            if street == 'turn':
                action_history = (
                    pre
                    + [('flop', p, 'check') for p in active_order]
                    + [
                        ('turn', p, 'check') for p in active_order
                        if _PFO[p] < hero_order
                    ]
                )
            else:  # river
                action_history = (
                    pre
                    + [('flop', p, 'check') for p in active_order]
                    + [('turn', p, 'check') for p in active_order]
                    + [
                        ('river', p, 'check') for p in active_order
                        if _PFO[p] < hero_order
                    ]
                )

            # Pick hero hands across the medium-to-strong range.  Predicate
            # (worse_hand_pct ≥ 0.55, equity_vs_range ≥ 0.35) will filter
            # the weakest ones out post-build.
            def _umbrella_hand(h, b):
                cat = _category_of(h, b)
                return cat in STRONG_CATS | MEDIUM_CATS | {'overpair'}

            heroes = _pick_hole_cards_of_category(
                board, _umbrella_hand, max_hands=4, used=used,
            )
            for hero in heroes:
                if len(specs) >= target:
                    break
                spec = _make_spec(
                    hero_cards=hero,
                    board=board,
                    hero_pos=hero_pos,
                    villain_positions=villain_positions,
                    pot=STD_POT,
                    to_call=0.0,
                    street=street,
                    action_history=action_history,
                    opener_position=opener,
                )
                desc = (
                    f'UMBRELLA: hero {hero_pos} '
                    f'({_category_of(hero, board)}) on {"-".join(board)}; '
                    f'street={street}, checked-to, capped villain.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
    return specs[:target]


# =============================================================================
# BUCKET REGISTRY
# =============================================================================
BUCKET_BUILDERS: Dict[str, Callable[[], List[Tuple[SituationSpec, str]]]] = {
    'MM_IP_TURN':  build_MM_IP_TURN_specs,
    'MM_IP_FLOP':  build_MM_IP_FLOP_specs,
    'MM_OOP_TURN': build_MM_OOP_TURN_specs,
    'SM_IP_TURN':  build_SM_IP_TURN_specs,
    'SM_IP_RIVER': build_SM_IP_RIVER_specs,
    'MON_CHECKED': build_MON_CHECKED_specs,
    'RAISE_VALUE': build_RAISE_VALUE_specs,
    'PROT_DANGER': build_PROT_DANGER_specs,
    'PFR_CONT':    build_PFR_CONT_specs,
    'UMBRELLA':    build_UMBRELLA_specs,
}

# Expected (BP net, OS overshoot, output JSONL filename) per bucket.
BUCKET_META: Dict[str, Tuple[int, int, str]] = {
    'MM_IP_TURN':  (30, 38, 'v23_mm_ip_turn.jsonl'),
    'MM_IP_FLOP':  (15, 19, 'v23_mm_ip_flop.jsonl'),
    'MM_OOP_TURN': (20, 25, 'v23_mm_oop_turn.jsonl'),
    'SM_IP_TURN':  (20, 25, 'v23_sm_ip_turn.jsonl'),
    'SM_IP_RIVER': (15, 19, 'v23_sm_ip_river.jsonl'),
    'MON_CHECKED': (15, 19, 'v23_mon_checked.jsonl'),
    'RAISE_VALUE': (20, 25, 'v23_raise_value.jsonl'),
    'PROT_DANGER': (16, 20, 'v23_prot_danger.jsonl'),
    'PFR_CONT':    (20, 25, 'v23_pfr_cont.jsonl'),
    'UMBRELLA':    (214, 268, 'v23_umbrella_fill.jsonl'),
}


# =============================================================================
# Predicate filter for UMBRELLA
# =============================================================================

def _umbrella_predicate_passes(feat_dict: dict) -> bool:
    """
    Verify that a UMBRELLA record satisfies the Section 2 predicate.
    Missing fields default to 0 (fails the predicate).
    """
    return (
        feat_dict.get('facing_bet', 0) == 0
        and feat_dict.get('num_opponents', 0) == 2
        and feat_dict.get('villain_checked_back', 0) == 1
        and feat_dict.get('villain_range_capped', 0) == 1
        and feat_dict.get('worse_hand_pct', 0.0) >= 0.55
        and feat_dict.get('equity_vs_range', 0.0) >= 0.35
        and feat_dict.get('spr', 99.0) <= 2.0
    )


# =============================================================================
# Per-bucket generation
# =============================================================================

def generate_one_bucket(bucket: str, verbose: bool = False) -> List[dict]:
    """
    Build all specs for `bucket`, run through build_situation + validate,
    enrich with metadata, and return the list of RAW (pre-normalisation)
    feat_dicts.  Records with validation errors are still returned, but
    tagged has_errors=True.
    """
    build_fn = BUCKET_BUILDERS[bucket]
    spec_tuples = build_fn()
    records: List[dict] = []

    for idx, (spec, description) in enumerate(spec_tuples):
        sit_id = f'{bucket}_{idx + 1:03d}'
        try:
            feat_dict = build_situation(spec)
        except Exception as exc:
            # Validator refusal — count but don't include in output.
            if verbose:
                print(f'  SKIP  {sit_id}: BUILD_EXCEPTION: {exc}')
            records.append({
                '_skip_reason': f'BUILD_EXCEPTION: {exc}',
                'situation_id': sit_id,
                'bucket': bucket,
                'has_errors': True,
                'validation_errors': [str(exc)],
                # Minimum metadata to avoid breakage in later serialisation:
                'villain_positions': list(spec.villain_positions),
                'hero_position': spec.hero_pos,
                'action_string': spec.action_string or '',
                'street': spec.street,
            })
            continue

        validation_errors = validate_situation(spec, feat_dict)

        feat_dict['situation_id'] = sit_id
        feat_dict['bucket'] = bucket
        feat_dict['sub_pattern'] = bucket
        feat_dict['hero_cards'] = ''.join(spec.hero_cards)
        feat_dict['board_cards'] = ''.join(spec.board_cards)
        feat_dict['description'] = description
        feat_dict['action_string'] = spec.action_string
        feat_dict['hero_position'] = spec.hero_pos
        feat_dict['villain_positions'] = list(spec.villain_positions)
        feat_dict['street'] = spec.street
        feat_dict['has_errors'] = bool(validation_errors)
        if validation_errors:
            feat_dict['validation_errors'] = validation_errors

        # UMBRELLA: verify Section 2 predicate
        if bucket == 'UMBRELLA':
            if not _umbrella_predicate_passes(feat_dict):
                feat_dict['_umbrella_predicate_fail'] = True
                feat_dict['has_errors'] = True
        records.append(feat_dict)

    return records


# =============================================================================
# Main
# =============================================================================

def _write_bucket_jsonl(bucket: str, records: List[dict]) -> Dict[str, int]:
    """
    Serialise the records for a single bucket to its JSONL, filtering out
    build exceptions and (for UMBRELLA) predicate-failing rows.

    Returns a stats dict with keys:
        generated, validated, build_failures, predicate_failures, written.
    """
    bp_target, os_target, filename = BUCKET_META[bucket]
    out_path = os.path.join(OUTPUT_DIR, filename)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    generated = len(records)
    build_failures = sum(1 for r in records if r.get('_skip_reason'))
    predicate_failures = sum(
        1 for r in records if r.get('_umbrella_predicate_fail')
    )
    write_rows = [
        r for r in records
        if not r.get('_skip_reason')
        and not r.get('_umbrella_predicate_fail')
    ]
    validated = sum(1 for r in write_rows if not r.get('has_errors'))

    with open(out_path, 'w') as f:
        for r in write_rows:
            f.write(json.dumps(normalise_situation(r)) + '\n')

    return {
        'bucket': bucket,
        'bp_target': bp_target,
        'os_target': os_target,
        'generated': generated,
        'build_failures': build_failures,
        'predicate_failures': predicate_failures,
        'written': len(write_rows),
        'validated_clean': validated,
        'out_path': out_path,
    }


def _preflight_schema_check_file(path: str) -> List[str]:
    """
    Stand-alone preflight: verify street and hero_position are numeric in a
    given JSONL.  Mirrors train_model._preflight_schema_check.
    """
    errors = []
    if not os.path.exists(path):
        return [f'{path}: MISSING']
    with open(path) as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            for col in ('street', 'hero_position'):
                v = rec.get(col)
                if v is None:
                    continue
                if not isinstance(v, (int, float)) or isinstance(v, bool):
                    errors.append(f'{path}:{col} line {i} = {v!r} (non-numeric)')
                    break
    return errors


def main():
    print('=' * 72)
    print('FACTORY BATCH 6 — v2.3 supplement generation')
    print('=' * 72)

    all_stats: List[Dict] = []
    all_preflight_errors: Dict[str, List[str]] = {}

    for bucket in BUCKET_BUILDERS.keys():
        bp_target, os_target, filename = BUCKET_META[bucket]
        print(f'\n[{bucket}] target BP={bp_target} OS={os_target} → {filename}')
        records = generate_one_bucket(bucket, verbose=False)
        stats = _write_bucket_jsonl(bucket, records)
        all_stats.append(stats)

        # Preflight schema check
        preflight_errors = _preflight_schema_check_file(stats['out_path'])
        all_preflight_errors[bucket] = preflight_errors

        print(f'  generated={stats["generated"]} '
              f'build_failures={stats["build_failures"]} '
              f'predicate_failures={stats["predicate_failures"]} '
              f'written={stats["written"]} '
              f'validated_clean={stats["validated_clean"]}')
        if preflight_errors:
            print(f'  PREFLIGHT ERRORS: {len(preflight_errors)}')
            for e in preflight_errors[:5]:
                print(f'    {e}')
        else:
            print(f'  preflight: PASS')

    # Summary table
    print('\n' + '=' * 72)
    print('SUMMARY')
    print('=' * 72)
    print(f"{'bucket':<14} {'BP':>4} {'OS':>4} {'gen':>5} {'bfail':>6} "
          f"{'pfail':>6} {'write':>6} {'clean':>6} {'meet_BP':>8}")
    total_written = 0
    total_clean = 0
    total_failures_pct = []
    for s in all_stats:
        met = 'YES' if s['validated_clean'] >= s['bp_target'] else 'NO'
        print(f"{s['bucket']:<14} {s['bp_target']:>4} {s['os_target']:>4} "
              f"{s['generated']:>5} {s['build_failures']:>6} "
              f"{s['predicate_failures']:>6} {s['written']:>6} "
              f"{s['validated_clean']:>6} {met:>8}")
        total_written += s['written']
        total_clean += s['validated_clean']
        if s['generated'] > 0:
            total_failures_pct.append(
                (s['build_failures'] / s['generated'])
            )
    print('-' * 72)
    print(f"TOTAL written={total_written} clean={total_clean}")

    # Stop-condition check: validator failure rate >25% per bucket
    for s in all_stats:
        if s['generated'] == 0:
            continue
        fail_rate = s['build_failures'] / s['generated']
        if fail_rate > 0.25:
            print(f'\n**STOP CONDITION TRIPPED**: {s["bucket"]} build failure '
                  f'rate = {fail_rate:.1%} > 25%.')
            return False

    # Stop-condition check: BP-under-10%-under-target
    for s in all_stats:
        if s['validated_clean'] < s['bp_target'] * 0.9:
            print(f'\n**WARNING**: {s["bucket"]} validated_clean={s["validated_clean"]} '
                  f'< BP_target * 0.9 = {s["bp_target"] * 0.9:.1f}.')
            # Don't hard-abort — the report will flag this and the orchestrator decides.

    # Preflight global
    any_preflight_errors = any(v for v in all_preflight_errors.values())
    if any_preflight_errors:
        print('\n**PREFLIGHT SCHEMA CHECK FAILED** on at least one bucket.')
        for b, errs in all_preflight_errors.items():
            if errs:
                print(f'  {b}: {len(errs)} errors (first 3):')
                for e in errs[:3]:
                    print(f'    {e}')
        return False
    else:
        print('\nPreflight schema check: ALL PASS')

    return True


if __name__ == '__main__':
    ok = main()
    sys.exit(0 if ok else 1)
