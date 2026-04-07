# SPEC: SituationFactory

## Purpose

Build valid feature vectors for the 45-feature pipeline without running a
live PokerGame. A SituationSpec describes a decision point; `build_situation`
constructs the minimal stubs the bridge needs and calls
`build_features_from_game_state`, returning a feat_dict ready for
`GtoOracle.predict()`.

---

## 1. Exact Fields the Bridge Reads

Tracing every attribute access in `game_state_bridge.py`:

### From `player` (the Player object)

| Field | Type | Bridge line | Note |
|---|---|---|---|
| `player.hole_cards` | `List[Card]` | 58 | Iterable of objects with `__str__` returning `'Rr'` e.g. `'Ah'` |
| `player.position` | `str` | 148 | Seat name: `'UTG'`, `'HJ'`, `'CO'`, `'BTN'`, `'SB'`, `'BB'` |

### From `game` (the PokerGame object)

| Field | Type | Bridge line | Note |
|---|---|---|---|
| `game.community_cards` | `List[Card]` | 59 | Iterable of Card-like objects with `__str__` |
| `game.opener_position` | `str \| None` | 94 | `getattr` with `''` fallback; `None` is fine |
| `game.raises_this_street` | `int` | 97 | `getattr` with `0` fallback |
| `game.street_actions` | `dict` | 108, 127, 141 | `{street_name: [(name, pos, action), ...]}` — `getattr` with `{}` fallback |

### From `context` (plain dict)

| Key | Type | Bridge line | Default |
|---|---|---|---|
| `'street'` | `str` | 50 | `'flop'` — must NOT be `'preflop'` (raises) |
| `'active_opponents'` | `list` | 63 | `[]` — list of opponent stub objects |
| `'facing_bet'` | `bool` | 66 | `False` |
| `'current_bet'` | `float` | 73 | `0` — used to identify who bet |
| `'pot'` | `float` | 150 | `0` |
| `'to_call'` | `float` | 151 | `0` |
| `'num_raises_this_street'` | `int` | 97 | falls back to `game.raises_this_street` |
| `'opener_position'` | `str \| None` | 94 | `None` |

### From opponent stubs in `context['active_opponents']`

| Field | Type | Bridge line | Note |
|---|---|---|---|
| `opp.is_folded` | `bool` | 64, 84 | whether seat has folded |
| `opp.bet_this_street` | `float` | 73 | compared to `current_bet` to find bettor |
| `opp.position` | `str` | 76 | seat name |
| `opp.stack` | `int \| float` | 84 | used to pick largest-stack villain |

---

## 2. Minimal Stub Classes

```python
from dataclasses import dataclass, field
from typing import List


class CardStub:
    """Minimal Card replacement — bridge only needs str(card) == 'Rr'."""
    __slots__ = ('_s',)

    def __init__(self, card_str: str):
        # Accept '2h', 'Th', 'Ah', etc.
        if len(card_str) != 2:
            raise ValueError(f"CardStub expects 2-char string, got '{card_str}'")
        self._s = card_str

    def __str__(self) -> str:
        return self._s

    def __repr__(self) -> str:
        return f"CardStub('{self._s}')"


@dataclass
class OpponentStub:
    """Minimal opponent object for context['active_opponents']."""
    position: str
    is_folded: bool = False
    bet_this_street: float = 0.0
    stack: float = 100.0


@dataclass
class PlayerStub:
    """Minimal hero Player replacement.

    Bridge reads:
      player.hole_cards  — list of card-like objects
      player.position    — seat name string
    """
    position: str
    hole_cards: List[CardStub] = field(default_factory=list)


@dataclass
class GameStub:
    """Minimal PokerGame replacement.

    Bridge reads via getattr with fallbacks:
      game.community_cards    — list of card-like objects
      game.opener_position    — str | None
      game.raises_this_street — int
      game.street_actions     — dict {street: [(name, pos, action), ...]}
    """
    community_cards: List[CardStub] = field(default_factory=list)
    opener_position: str = None
    raises_this_street: int = 0
    street_actions: dict = field(default_factory=dict)
```

---

## 3. SituationSpec Dataclass

```python
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class SituationSpec:
    """
    Human-readable description of a single decision point.

    Fields
    ------
    hero_cards : List[str]
        Exactly 2 card strings, e.g. ['Ah', 'Kd'].

    board_cards : List[str]
        3, 4, or 5 card strings. Must match street
        (flop=3, turn=4, river=5).

    hero_pos : str
        Hero's seat: 'UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB'.

    villain_positions : List[str]
        Active (non-folded) opponent seat names.
        Single element = heads-up; multiple = multiway.

    pot : float
        Total chips in the pot BEFORE any action this decision.

    to_call : float
        Amount hero must call (0 if not facing a bet).

    street : str
        'flop', 'turn', or 'river'. NOT 'preflop' — bridge raises.

    action_history : List[Tuple[str, str, str]]
        Prior actions as (street, position, action) triples.
        street: 'preflop', 'flop', 'turn', 'river'
        position: seat name, e.g. 'BTN'
        action: 'bet', 'raise', 'call', 'check', 'fold'
        Include ALL streets including current street (pre-hero action).
        Used to populate game.street_actions and derive is_3bet_pot.

    opener_position : Optional[str]
        Preflop opener's seat (for range accuracy). None = heuristic fallback.

    effective_stack : float
        Hero's effective stack in chips (used for SPR calculation context,
        NOT currently read by the bridge — stored for future use).

    current_bet : float
        The current bet amount on this street (same as to_call for a simple
        bet; may differ in a re-raise situation). Used by bridge line 73 to
        identify the bettor among opponents.
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
```

---

## 4. build_situation() — The Factory Function

```python
import sys
import os

# Ensure river-rats-core is importable
_CORE = '/home/rupertbeytell/river-rats-v2/river-rats-core'
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from game_state_bridge import build_features_from_game_state


def _parse_cards(card_strings: List[str]) -> List[CardStub]:
    return [CardStub(c) for c in card_strings]


def _build_street_actions(
    action_history: List[Tuple[str, str, str]]
) -> dict:
    """
    Convert flat action_history list into the dict format game.street_actions
    uses: {street_name: [(name, pos, action), ...]}.

    'name' is unused by the bridge for logic — it only reads pos and action.
    We use pos as a stand-in for name (harmless).
    """
    result: dict = {}
    for street, pos, action in action_history:
        result.setdefault(street, []).append((pos, pos, action))
    return result


def _count_raises_this_street(
    action_history: List[Tuple[str, str, str]],
    street: str,
) -> int:
    """Count bet/raise actions on the current street from action_history."""
    return sum(
        1 for s, pos, act in action_history
        if s == street and act in ('bet', 'raise')
    )


def build_situation(spec: SituationSpec) -> dict:
    """
    Construct PlayerStub, GameStub, and context dict from a SituationSpec,
    then call build_features_from_game_state() and return the feat_dict.

    Parameters
    ----------
    spec : SituationSpec
        The situation description.

    Returns
    -------
    dict
        Complete 45-feature dict, identical in structure to what the live
        game produces. Ready for GtoOracle.features_from_dict().

    Raises
    ------
    ValueError
        If spec.street is 'preflop' (bridge raises for preflop inputs).
    ValueError
        If hero_cards or board_cards are malformed.
    """
    if spec.street == 'preflop':
        raise ValueError(
            "SituationFactory is postflop-only — bridge raises on preflop. "
            "Use preflop_engine.decide_preflop() for preflop decisions."
        )

    # --- Build hero (PlayerStub) ---
    hero = PlayerStub(
        position=spec.hero_pos,
        hole_cards=_parse_cards(spec.hero_cards),
    )

    # --- Build game (GameStub) ---
    street_actions = _build_street_actions(spec.action_history)
    raises_this_street = _count_raises_this_street(
        spec.action_history, spec.street
    )
    game = GameStub(
        community_cards=_parse_cards(spec.board_cards),
        opener_position=spec.opener_position,
        raises_this_street=raises_this_street,
        street_actions=street_actions,
    )

    # --- Build opponent stubs ---
    # Bridge line 73: identifies bettor as opponent whose bet_this_street
    # == context['current_bet']. We set current_bet on the LAST villain
    # in the list when facing a bet (most common: one bettor). Callers
    # get bet_this_street=0 so they don't false-match.
    facing_bet = spec.to_call > 0
    current_bet = spec.current_bet if spec.current_bet > 0 else spec.to_call

    opponents = []
    for i, pos in enumerate(spec.villain_positions):
        # Heuristic: last villain in the list is the bettor when facing_bet.
        # Caller can override by setting current_bet explicitly on SituationSpec
        # and ordering villain_positions with bettor last.
        is_bettor = facing_bet and (i == len(spec.villain_positions) - 1)
        opponents.append(OpponentStub(
            position=pos,
            is_folded=False,
            bet_this_street=current_bet if is_bettor else 0.0,
            stack=spec.effective_stack,
        ))

    # --- Build context dict ---
    context = {
        'street': spec.street,
        'active_opponents': opponents,
        'facing_bet': facing_bet,
        'current_bet': current_bet,
        'pot': spec.pot,
        'to_call': spec.to_call,
        'opener_position': spec.opener_position,
        # num_raises_this_street: let game.raises_this_street handle it
        # (bridge line 97 checks context first, then falls back to game attr)
    }

    return build_features_from_game_state(hero, game, context)
```

---

## 5. validate_situation() — Consistency Checker

```python
from typing import List as ListType


def validate_situation(spec: SituationSpec, feat_dict: dict) -> ListType[str]:
    """
    Verify that the feat_dict is internally consistent with the spec.

    Checks
    ------
    1. equity > 0 for hands that aren't pure air
       (high card with no draw on a completed board is the only pure-air case
       we flag; anything else getting 0 equity is suspicious)
    2. pot_odds matches pot and to_call arithmetic
    3. facing_bet matches to_call > 0
    4. action history features match spec.action_history
       - is_3bet_pot: true if preflop has 2+ bet/raise actions
       - villain_aggression_count: prior-street bet/raise count for primary villain
       - villain_checked_back: 1 if primary villain checked on any prior street
       - villain_call_count: prior-street call count for primary villain

    Returns
    -------
    List[str]
        Empty list means valid. Each entry is a human-readable error.
    """
    errors = []

    # --- 1. Equity sanity ---
    raw_equity = feat_dict.get('raw_equity', None)
    if raw_equity is None:
        errors.append("MISSING: 'raw_equity' not present in feat_dict")
    elif raw_equity == 0.0:
        # Pure air = high_card with no draws on a dry board.
        # We flag equity=0 only when the hand has some made strength OR a draw,
        # because the range math should always assign some positive equity.
        hand_category = feat_dict.get('hand_category', 0)
        has_draw = feat_dict.get('has_flush_draw', 0) or feat_dict.get('has_straight_draw', 0)
        if hand_category > 0 or has_draw:
            errors.append(
                f"SUSPICIOUS: raw_equity=0.0 but hand_category={hand_category}, "
                f"has_flush_draw={feat_dict.get('has_flush_draw')}, "
                f"has_straight_draw={feat_dict.get('has_straight_draw')}. "
                "Check that villain_positions are valid seat names."
            )

    # --- 2. pot_odds arithmetic ---
    pot = spec.pot
    to_call = spec.to_call
    expected_facing_bet = to_call > 0
    if expected_facing_bet and (pot + to_call) > 0:
        expected_pot_odds = round(to_call / (pot + to_call), 6)
    else:
        expected_pot_odds = 0.0

    actual_pot_odds = feat_dict.get('pot_odds', None)
    if actual_pot_odds is None:
        errors.append("MISSING: 'pot_odds' not present in feat_dict")
    else:
        if abs(actual_pot_odds - expected_pot_odds) > 0.0001:
            errors.append(
                f"POT_ODDS MISMATCH: spec gives pot={pot}, to_call={to_call} "
                f"=> expected pot_odds={expected_pot_odds:.6f}, "
                f"got {actual_pot_odds:.6f}"
            )

    # --- 3. facing_bet consistency ---
    actual_facing_bet = feat_dict.get('facing_bet', None)
    if actual_facing_bet is None:
        errors.append("MISSING: 'facing_bet' not present in feat_dict")
    elif bool(actual_facing_bet) != expected_facing_bet:
        errors.append(
            f"FACING_BET MISMATCH: spec.to_call={to_call} implies "
            f"facing_bet={expected_facing_bet}, feat_dict has {actual_facing_bet}"
        )

    # --- 4. Action history features ---
    # Derive expected values from spec.action_history using the same logic
    # as the bridge (lines 100-138).

    street_sequence = ['preflop', 'flop', 'turn', 'river']
    current_idx = street_sequence.index(spec.street) if spec.street in street_sequence else 1
    prior_streets = street_sequence[:current_idx]

    # Identify primary villain position (same heuristic as bridge lines 79-88:
    # bettor first, then largest stack, then 'BB').
    # In the factory, bettor = last villain when facing_bet.
    if spec.villain_positions:
        primary_vp = spec.villain_positions[-1] if expected_facing_bet else spec.villain_positions[0]
    else:
        primary_vp = 'BB'

    # is_3bet_pot: 2+ bet/raise in preflop actions
    pf_aggressive = sum(
        1 for s, pos, act in spec.action_history
        if s == 'preflop' and act in ('bet', 'raise')
    )
    expected_3bet = int(pf_aggressive >= 2)

    actual_3bet = feat_dict.get('is_3bet_pot', None)
    if actual_3bet is None:
        errors.append("MISSING: 'is_3bet_pot' not present in feat_dict")
    elif actual_3bet != expected_3bet:
        errors.append(
            f"IS_3BET_POT MISMATCH: expected {expected_3bet} "
            f"(preflop bets/raises={pf_aggressive}), got {actual_3bet}"
        )

    # villain_aggression_count, villain_checked_back, villain_call_count
    # computed over prior streets for primary_vp
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

    actual_aggression = feat_dict.get('villain_aggression_count', None)
    if actual_aggression is None:
        errors.append("MISSING: 'villain_aggression_count' not present in feat_dict")
    elif actual_aggression != expected_aggression:
        errors.append(
            f"VILLAIN_AGGRESSION_COUNT MISMATCH: expected {expected_aggression}, "
            f"got {actual_aggression} (primary_vp={primary_vp})"
        )

    actual_checked_back = feat_dict.get('villain_checked_back', None)
    if actual_checked_back is None:
        errors.append("MISSING: 'villain_checked_back' not present in feat_dict")
    elif actual_checked_back != expected_checked_back:
        errors.append(
            f"VILLAIN_CHECKED_BACK MISMATCH: expected {expected_checked_back}, "
            f"got {actual_checked_back} (primary_vp={primary_vp})"
        )

    actual_call_count = feat_dict.get('villain_call_count', None)
    if actual_call_count is None:
        errors.append("MISSING: 'villain_call_count' not present in feat_dict")
    elif actual_call_count != expected_call_count:
        errors.append(
            f"VILLAIN_CALL_COUNT MISMATCH: expected {expected_call_count}, "
            f"got {actual_call_count} (primary_vp={primary_vp})"
        )

    return errors
```

---

## 6. Complete situation_factory.py

This is the exact file to write to `river-rats-core/situation_factory.py` after review.

```python
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
    """Count bet and raise actions on current street from action_history."""
    return sum(
        1 for s, pos, act in action_history
        if s == street and act in ('bet', 'raise')
    )


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

    return errors
```

---

## 7. Dependency Trace — What Is and Is Not Stubbed

### What the bridge builds (the `hand` dict, lines 145-165)

The bridge does NOT call any Player or PokerGame methods. It reads raw
attribute values and builds a plain `hand` dict, which it passes to
`extract_all_features(hand)`. The stubs only need to satisfy attribute
access — no method calls.

### extract_all_features() dependencies

All of these are real module calls, not game-object calls:

| Module | Called via | Stub needed? |
|---|---|---|
| `hand_evaluator.evaluate_hand()` | card strings from parsed `hand['h']` and `hand['b']` | No — takes string lists |
| `board_analyzer.analyze_board_cached()` | board card strings | No |
| `range_manager.RangeManager` | position strings | No |
| `range_narrowing.narrow_to_betting_range()` | range dict + board strings | No |
| `raw_equity.RawEquityCalculator` | card strings + range dict | No |
| `eval7.Card()` | 2-char card strings | No |
| `eval7.evaluate()` | eval7.Card lists | No |
| `range_narrowing.classify_hand()` | hand notation + board strings | No |

All downstream computation operates on plain strings and dicts derived from
the `hand` dict that the bridge builds. No PokerGame or Player methods are
called by any downstream module.

### Real Card objects — confirmed not required

`eval7.Card` is constructed from the 2-char card strings that come from
`str(card)` (bridge lines 58-59). CardStub's `__str__` returns the same
2-char string. The `eval7.Card` constructor receives a string — it never
receives a `poker_game.Card` object. This is safe to stub.

### Confirmed blockers — none

There are no hard blockers. Every path from the bridge into the feature
pipeline uses plain strings or dicts. The stubs satisfy all attribute
reads.

---

## 8. Known Limitations

**Bettor identification (bridge lines 70-76):** The bridge identifies the
bettor as the opponent whose `bet_this_street == context['current_bet']`.
The factory assigns this to the LAST villain in `spec.villain_positions`.
If the caller needs a specific villain to be identified as bettor (multiway
scenario where a non-last player bet), they should place the bettor last
in `villain_positions` or set `spec.current_bet` explicitly.

**SPR calculation:** The bridge does not read `effective_stack` from the
spec. SPR is computed inside `add_derived_features()` using
`DEFAULT_EFFECTIVE_STACK = 100.0` hardcoded in feature_extractor.py. The
`effective_stack` field on SituationSpec is stored but not injected — this
is a known gap in the current bridge contract.

**num_callers_to_bet:** Bridge line 129 counts `'call'` actions on the
current street from `game.street_actions` where `pos != player.position`
and `pos != bettor_position`. This works correctly as long as
`action_history` includes current-street call actions by non-hero, non-bettor
opponents (cold callers). If action_history only contains prior-street actions,
`num_callers_to_bet` will be 0 (which is often correct for a direct bet).

**validate_situation primary villain heuristic:** The validator mirrors the
bridge's villain resolution logic (bettor = last in list). If the bridge
resolves to a different villain (e.g. due to stack-size tiebreaking), the
action history checks will produce false mismatches. The validator is a
sanity check, not a guarantee.
