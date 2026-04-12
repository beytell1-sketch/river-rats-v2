"""
SituationFactory — construct valid feature vectors without live game simulation.

Takes a SituationSpec (board, hero cards, positions, pot, action history) and
produces a feat_dict by running the real feature extraction pipeline via
build_features_from_game_state().

Usage
-----
    from situation_factory import SituationSpec, build_situation, validate_situation

    spec = SituationSpec(
        hero_cards=['Ah', 'Kd'],
        board_cards=['Jh', '8c', '2s'],
        hero_pos='BTN',
        villain_positions=['BB'],
        pot=12.0,
        to_call=6.0,
        street='flop',
        action_history=[
            ('preflop', 'BTN', 'raise'),
            ('preflop', 'BB', 'call'),
            ('flop', 'BB', 'bet'),
        ],
        opener_position='BTN',
    )

    feat_dict = build_situation(spec)
    errors = validate_situation(spec, feat_dict)
    if errors:
        for e in errors:
            print(e)
"""

from __future__ import annotations

import sys
import os
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

# Ensure river-rats-core is importable regardless of cwd
_CORE = os.path.dirname(os.path.abspath(__file__))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from game_state_bridge import build_features_from_game_state
from hand_sequence_validator import validate_action_string as _hsv_validate_action_string

# Postflop acting order — SB first (OOP), BTN last (IP).
# Used by validate_action_sequence().
_POSTFLOP_ORDER = {
    'SB': 0, 'BB': 1,
    'UTG': 2, 'EP': 2,
    'HJ': 3, 'MP': 3,
    'CO': 4,
    'BTN': 5,
}


# =============================================================================
# Stub Classes
# =============================================================================

class CardStub:
    """
    Minimal Card replacement.

    The bridge concatenates str(card) for each card in player.hole_cards and
    game.community_cards (lines 58-59). We only need __str__ to return the
    2-character card string.
    """
    __slots__ = ('_s',)

    def __init__(self, card_str: str):
        if len(card_str) != 2:
            raise ValueError(
                f"CardStub expects 2-char string like 'Ah', got '{card_str}'"
            )
        self._s = card_str

    def __str__(self) -> str:
        return self._s

    def __repr__(self) -> str:
        return f"CardStub('{self._s}')"


@dataclass
class OpponentStub:
    """
    Minimal opponent object for context['active_opponents'].

    Bridge reads: is_folded (lines 64, 84), bet_this_street (line 73),
    position (line 76), stack (line 84).
    """
    position: str
    is_folded: bool = False
    bet_this_street: float = 0.0
    stack: float = 100.0


@dataclass
class PlayerStub:
    """
    Minimal hero Player replacement.

    Bridge reads: hole_cards (line 58), position (line 148).
    """
    position: str
    hole_cards: List[CardStub] = field(default_factory=list)


@dataclass
class GameStub:
    """
    Minimal PokerGame replacement.

    Bridge reads all fields via getattr with fallbacks, so missing attributes
    return safe defaults. We set them explicitly for clarity.

    Bridge reads:
      community_cards    (line 59)
      opener_position    (line 94, getattr fallback '')
      raises_this_street (line 97, getattr fallback 0)
      street_actions     (lines 108, 127, 141, getattr fallback {})
    """
    community_cards: List[CardStub] = field(default_factory=list)
    opener_position: Optional[str] = None
    raises_this_street: int = 0
    street_actions: dict = field(default_factory=dict)


# =============================================================================
# SituationSpec
# =============================================================================

@dataclass
class SituationSpec:
    """
    Human-readable description of a single postflop decision point.

    hero_cards : List[str]
        Exactly 2 card strings e.g. ['Ah', 'Kd'].

    board_cards : List[str]
        3 cards (flop), 4 (turn), or 5 (river).

    hero_pos : str
        'UTG', 'HJ', 'CO', 'BTN', 'SB', or 'BB'.

    villain_positions : List[str]
        Active (non-folded) opponent seats. Single element = heads-up.
        Last position in list is assumed to be the bettor when facing_bet.

    pot : float
        Pot size in chips BEFORE this decision.

    to_call : float
        Chips hero must call. 0 = not facing a bet (check/bet situation).

    street : str
        'flop', 'turn', or 'river'. 'preflop' raises ValueError.

    action_history : List[Tuple[str, str, str]]
        All actions so far as (street, position, action) triples.
        street: 'preflop', 'flop', 'turn', 'river'
        position: seat name
        action: 'bet', 'raise', 'call', 'check', 'fold'
        Include all streets up to and including current street (pre-hero action).

    opener_position : Optional[str]
        Preflop raiser's seat for range accuracy. None = PREFLOP_ORDER heuristic.

    effective_stack : float
        Hero's effective stack (stored for context; not read by current bridge).

    current_bet : float
        The bet amount placed by the bettor. Defaults to to_call when 0.
        Only matters when to_call != current_bet (re-raise situations).
    """
    hero_cards: List[str]
    board_cards: List[str]
    hero_pos: str
    villain_positions: List[str]
    pot: float
    to_call: float
    street: str
    action_history: List[Tuple[str, str, str]] = field(default_factory=list)
    opener_position: Optional[str] = None
    effective_stack: float = 100.0
    current_bet: float = 0.0


# =============================================================================
# Internal Helpers
# =============================================================================

def _parse_cards(card_strings: List[str]) -> List[CardStub]:
    return [CardStub(c) for c in card_strings]


def _build_street_actions(
    action_history: List[Tuple[str, str, str]],
) -> dict:
    """
    Convert flat action_history into game.street_actions format.

    game.street_actions format: {street_name: [(name, pos, action), ...]}
    Bridge only reads `pos` (index 1) and `action` (index 2) from each tuple.
    We use pos as a stand-in for name (index 0) — bridge ignores index 0.
    """
    result: dict = {}
    for s, pos, action in action_history:
        result.setdefault(s, []).append((pos, pos, action))
    return result


def _count_raises_this_street(
    action_history: List[Tuple[str, str, str]],
    street: str,
) -> int:
    """Count raises on current street (not the initial bet).

    The first aggressive action on a street is a BET, not a raise.
    Only subsequent aggressive actions (raise over a bet, re-raise)
    count as raises. This matches poker_game.py's logic.
    """
    aggressive = [
        act for s, pos, act in action_history
        if s == street and act in ('bet', 'raise')
    ]
    # First aggressive action is the opening bet — not a raise
    return max(0, len(aggressive) - 1)


# =============================================================================
# Factory Function
# =============================================================================

def build_situation(spec: SituationSpec) -> dict:
    """
    Construct stubs from spec and call build_features_from_game_state().

    Returns a complete 45-feature dict. Raises ValueError for preflop specs
    or malformed card strings.
    """
    if spec.street == 'preflop':
        raise ValueError(
            "SituationFactory is postflop-only. "
            "Use preflop_engine.decide_preflop() for preflop decisions."
        )

    # Hero
    hero = PlayerStub(
        position=spec.hero_pos,
        hole_cards=_parse_cards(spec.hero_cards),
    )

    # Game
    street_actions = _build_street_actions(spec.action_history)
    raises_this_street = _count_raises_this_street(spec.action_history, spec.street)
    game = GameStub(
        community_cards=_parse_cards(spec.board_cards),
        opener_position=spec.opener_position,
        raises_this_street=raises_this_street,
        street_actions=street_actions,
    )

    # Opponents
    facing_bet = spec.to_call > 0
    current_bet = spec.current_bet if spec.current_bet > 0 else spec.to_call

    opponents: List[OpponentStub] = []
    for i, pos in enumerate(spec.villain_positions):
        # Last villain in list is the bettor (caller gets bet_this_street=0).
        # Bridge line 73: finds bettor by matching bet_this_street == current_bet.
        is_bettor = facing_bet and (i == len(spec.villain_positions) - 1)
        opponents.append(OpponentStub(
            position=pos,
            is_folded=False,
            bet_this_street=current_bet if is_bettor else 0.0,
            stack=spec.effective_stack,
        ))

    # Context
    context: dict = {
        'street': spec.street,
        'active_opponents': opponents,
        'facing_bet': facing_bet,
        'current_bet': current_bet,
        'pot': spec.pot,
        'to_call': spec.to_call,
        'opener_position': spec.opener_position,
        # num_raises_this_street not set here — bridge line 97 falls back to
        # game.raises_this_street, which we set from action_history above.
    }

    return build_features_from_game_state(hero, game, context)


# =============================================================================
# Validation
# =============================================================================

def validate_action_sequence(spec: 'SituationSpec') -> List[str]:
    """
    Check that action_history is internally consistent.

    Rules checked:
    1. On each postflop street, the first actor must be the player with the
       lowest postflop order among the active players (SB before BB before
       CO before BTN). Preflop order is not validated (preflop is out of scope).
    2. Before the first bet on a postflop street, every active player must
       act (check or bet) in order — no player may be silently skipped.
    3. No player listed in action_history (for a postflop street) may have
       an order value higher than a player who has not yet acted on that street.

    Args:
        spec: SituationSpec with hero_pos, villain_positions, and action_history.

    Returns:
        List of error strings. Empty list = valid.
    """
    errors: List[str] = []

    # Build the full set of active positions
    active_positions = {spec.hero_pos.upper()} | {
        v.upper() for v in spec.villain_positions
    }

    # Group actions by street
    actions_by_street: dict = {}
    for s, pos, act in spec.action_history:
        actions_by_street.setdefault(s, []).append((pos.upper(), act))

    postflop_streets = [s for s in actions_by_street if s != 'preflop']

    for street in postflop_streets:
        street_actions = actions_by_street[street]

        # 1. First actor must have the lowest order among active positions
        if street_actions:
            first_actor = street_actions[0][0]
            first_order = _POSTFLOP_ORDER.get(first_actor, 99)
            for pos in active_positions:
                pos_order = _POSTFLOP_ORDER.get(pos, 99)
                if pos_order < first_order:
                    errors.append(
                        f"ACTION_ORDER [{street}]: '{first_actor}' acted first "
                        f"but '{pos}' has earlier postflop order "
                        f"({pos_order} < {first_order}). "
                        f"SB/BB must act before CO/BTN postflop."
                    )
                    break  # One error per street is enough

        # 2 & 3. Before the opening bet, every active player must have acted
        # once (check or open-bet) in correct positional order.
        # After a bet, remaining players respond — we only validate pre-bet order.
        acted_so_far: List[str] = []
        bet_has_occurred = False
        for pos, act in street_actions:
            if bet_has_occurred:
                break  # Post-bet actions are responses; order rules differ

            # Check that this actor's order is >= all previous actors' orders
            current_order = _POSTFLOP_ORDER.get(pos, 99)
            for prior_pos in acted_so_far:
                prior_order = _POSTFLOP_ORDER.get(prior_pos, 99)
                if current_order < prior_order:
                    errors.append(
                        f"ACTION_ORDER [{street}]: '{pos}' (order={current_order}) "
                        f"acted after '{prior_pos}' (order={prior_order}) but has "
                        f"earlier position. Actions must proceed SB→BB→CO→BTN."
                    )

            # Check that no active player was skipped between prior actor and this one
            if acted_so_far:
                last_order = _POSTFLOP_ORDER.get(acted_so_far[-1], 99)
                for skipped in active_positions:
                    skipped_order = _POSTFLOP_ORDER.get(skipped, 99)
                    if (
                        last_order < skipped_order < current_order
                        and skipped not in acted_so_far
                        and skipped != pos
                    ):
                        errors.append(
                            f"MISSING_ACTION [{street}]: '{skipped}' "
                            f"(order={skipped_order}) was skipped between "
                            f"'{acted_so_far[-1]}' and '{pos}'. All active "
                            f"players must act on each street."
                        )

            acted_so_far.append(pos)
            if act in ('bet', 'raise'):
                bet_has_occurred = True

    return errors


def validate_situation(spec: SituationSpec, feat_dict: dict) -> List[str]:
    """
    Verify internal consistency between spec and the returned feat_dict.

    Returns list of error strings. Empty list = valid.

    Checks
    ------
    1. raw_equity > 0 for any non-pure-air hand
       (pure air = high_card with no draws; anything else should have equity)
    2. pot_odds arithmetic matches spec.pot and spec.to_call
    3. facing_bet in feat_dict matches spec.to_call > 0
    4. Action history derived features match spec.action_history:
       is_3bet_pot, villain_aggression_count, villain_checked_back, villain_call_count
    """
    errors: List[str] = []

    # 0. Action sequence structural validation
    errors.extend(validate_action_sequence(spec))

    # 1. Equity sanity
    raw_equity = feat_dict.get('raw_equity')
    if raw_equity is None:
        errors.append("MISSING: 'raw_equity' not present in feat_dict")
    elif raw_equity == 0.0:
        hand_category = feat_dict.get('hand_category', 0)
        has_flush_draw = feat_dict.get('has_flush_draw', 0)
        has_straight_draw = feat_dict.get('has_straight_draw', 0)
        if hand_category > 0 or has_flush_draw or has_straight_draw:
            errors.append(
                f"SUSPICIOUS: raw_equity=0.0 but hand_category={hand_category}, "
                f"has_flush_draw={has_flush_draw}, "
                f"has_straight_draw={has_straight_draw}. "
                "Likely cause: villain_positions contains an invalid seat name."
            )

    # 2. pot_odds arithmetic
    pot = spec.pot
    to_call = spec.to_call
    facing_bet_expected = to_call > 0
    if facing_bet_expected and (pot + to_call) > 0:
        expected_pot_odds = round(to_call / (pot + to_call), 6)
    else:
        expected_pot_odds = 0.0

    actual_pot_odds = feat_dict.get('pot_odds')
    if actual_pot_odds is None:
        errors.append("MISSING: 'pot_odds' not present in feat_dict")
    elif abs(actual_pot_odds - expected_pot_odds) > 0.0001:
        errors.append(
            f"POT_ODDS MISMATCH: spec pot={pot}, to_call={to_call} "
            f"=> expected {expected_pot_odds:.6f}, got {actual_pot_odds:.6f}"
        )

    # 3. facing_bet
    actual_facing_bet = feat_dict.get('facing_bet')
    if actual_facing_bet is None:
        errors.append("MISSING: 'facing_bet' not present in feat_dict")
    elif bool(actual_facing_bet) != facing_bet_expected:
        errors.append(
            f"FACING_BET MISMATCH: to_call={to_call} implies "
            f"facing_bet={facing_bet_expected}, feat_dict has {actual_facing_bet}"
        )

    # 4. Action history features
    # Identify primary villain (same heuristic as bridge resolution):
    # bettor (last in list) when facing bet, else first villain.
    if spec.villain_positions:
        primary_vp = (
            spec.villain_positions[-1] if facing_bet_expected
            else spec.villain_positions[0]
        )
    else:
        primary_vp = 'BB'

    street_sequence = ['preflop', 'flop', 'turn', 'river']
    current_idx = (
        street_sequence.index(spec.street)
        if spec.street in street_sequence else 1
    )
    prior_streets = set(street_sequence[:current_idx])

    # is_3bet_pot: 2+ bet/raise in preflop
    pf_aggressive = sum(
        1 for s, pos, act in spec.action_history
        if s == 'preflop' and act in ('bet', 'raise')
    )
    expected_3bet = int(pf_aggressive >= 2)
    actual_3bet = feat_dict.get('is_3bet_pot')
    if actual_3bet is None:
        errors.append("MISSING: 'is_3bet_pot' not present in feat_dict")
    elif actual_3bet != expected_3bet:
        errors.append(
            f"IS_3BET_POT MISMATCH: expected {expected_3bet} "
            f"(preflop aggression count={pf_aggressive}), got {actual_3bet}"
        )

    # villain aggression / checked_back / call_count over prior streets
    v_acts_by_street: dict = {}
    for s, pos, act in spec.action_history:
        if s in prior_streets and pos == primary_vp:
            v_acts_by_street.setdefault(s, []).append(act)

    expected_aggression = 0
    expected_checked_back = 0
    expected_call_count = 0
    for s, acts in v_acts_by_street.items():
        if any(a in ('bet', 'raise') for a in acts):
            expected_aggression += 1
        if 'check' in acts:
            expected_checked_back = 1
        if any(a == 'call' for a in acts):
            expected_call_count += 1

    for key, expected, label in [
        ('villain_aggression_count', expected_aggression, 'VILLAIN_AGGRESSION_COUNT'),
        ('villain_checked_back', expected_checked_back, 'VILLAIN_CHECKED_BACK'),
        ('villain_call_count', expected_call_count, 'VILLAIN_CALL_COUNT'),
    ]:
        actual = feat_dict.get(key)
        if actual is None:
            errors.append(f"MISSING: '{key}' not present in feat_dict")
        elif actual != expected:
            errors.append(
                f"{label} MISMATCH: expected {expected}, got {actual} "
                f"(primary_vp={primary_vp})"
            )

    # 5. Hand sequence validator — deep structural check of the current-street
    #    postflop action sequence (ordering, bet legality, initiative round).
    #
    #    We reconstruct an action string from the current-street actions in
    #    spec.action_history.  The hero decision point is implied (not yet
    #    acted): we append "hero_pos ???" to let the validator know where hero
    #    will act.  Errors from this validator are prefixed HSV: so callers
    #    can distinguish them from the feature-level checks above.
    #
    #    NOTE: validate_action_sequence() already catches basic ordering on
    #    prior streets.  The HSV call below adds:
    #      - Bet-legality (fold/call/raise without a live bet)
    #      - Response ordering after a bet (clockwise from bettor)
    #      - Hero-action-index consistency
    current_street_acts = [
        (pos, act)
        for s, pos, act in spec.action_history
        if s == spec.street
    ]
    if current_street_acts:
        # Build comma-separated action string from current-street history,
        # then append the hero's pending decision as "HERO ???"
        parts = []
        for pos, act in current_street_acts:
            parts.append(f"{pos} {act}")
        parts.append(f"{spec.hero_pos} ???")
        action_string = ', '.join(parts)

        all_positions = [spec.hero_pos] + list(spec.villain_positions)
        hsv_errors = _hsv_validate_action_string(
            all_positions,
            spec.street,
            action_string,
            spec.hero_pos,
        )
        for e in hsv_errors:
            errors.append(f"HSV: {e}")

    return errors
