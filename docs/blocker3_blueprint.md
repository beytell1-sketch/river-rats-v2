# Blocker 3 Blueprint: build_features_from_game_state()

## Purpose

Bridge live game state (a `Game` and `Player` instance plus the `context` dict
from Blocker 2) to the `hand` dict format that `extract_all_features()` in
`feature_extractor.py` expects. The result is a complete 38-key feature dict
that can be passed directly to `GtoOracle.features_from_dict()` and then to
`GtoOracle.predict()`.

This function must NOT call `run_coaching()`, `engine.explain()`, or anything
in the coaching pipeline. It calls the feature extraction pipeline directly.

---

## File Location

New file: `/home/rupertbeytell/river-rats-v2/river-rats-core/game_state_bridge.py`

Reasons for a new file rather than adding to an existing one:
- `poker_game.py` already imports from `feature_extractor.py`; adding the
  bridge there would create a circular dependency risk.
- `feature_extractor.py` knows nothing about `Player` or `Game` — keeping it
  that way preserves the pipeline's independence from game logic.
- The bridge is a seam between two subsystems; it belongs in its own module.

---

## Exact Function Signature

```python
def build_features_from_game_state(
    player: "Player",
    game: "Game",
    context: dict,
) -> dict:
```

### Returns
A complete feature dict as returned by `extract_all_features(hand)`. All 38
model keys are present plus all underscore-prefixed metadata keys. The dict
is ready for `GtoOracle.features_from_dict()` without further transformation.

### Does NOT return
A numpy array. The caller is responsible for converting via
`GtoOracle.features_from_dict(feat_dict)` if a numpy array is needed.

---

## The hand Dict Contract

`extract_all_features(hand: Dict)` in `feature_extractor.py` reads the
following keys from the raw `hand` dict (verified by reading
`extract_zero_compute_features`, `extract_features_step1_through_5`, and
`extract_all_features`):

| hand dict key           | Type           | Required | Description |
|-------------------------|----------------|----------|-------------|
| `'h'`                   | str            | Yes      | Hero hole cards concatenated, e.g. `'AhKs'` |
| `'b'`                   | str            | Yes      | Board cards concatenated, e.g. `'4s4h3h'`; empty string `''` for preflop |
| `'pos'`                 | str            | Yes      | Hero position, e.g. `'BTN'` |
| `'vp'`                  | str or None    | Yes      | Villain position for range analysis |
| `'pot'`                 | float          | Yes      | Current pot size in chips |
| `'tc'`                  | float          | Yes      | Amount to call (0 if not facing bet) |
| `'st'`                  | str            | Yes      | Street code: `'p'` preflop, `'f'` flop, `'t'` turn, `'r'` river |
| `'fb'`                  | int (0/1)      | Yes      | 1 if facing a bet/raise, 0 otherwise |
| `'exp'`                 | str            | Yes      | GTO label; set to `'C'` (call placeholder) — not used by prediction path |
| `'_num_opponents'`      | int            | Yes      | Active non-folded opponents (minimum 1) |
| `'_num_raises_this_street'` | int        | Yes      | Raise count this street (for squeeze detection) |
| `'_opener_position'`    | str or None    | Yes      | Position of preflop raiser; None if no raise yet |
| `'_bettor_position'`    | str or None    | Yes      | Position of villain who made the current bet; None if not facing bet |
| `'_is_3bet_pot'`        | int (0/1)      | Yes      | 1 if raises_this_street >= 2 on preflop |
| `'_villain_aggression_count'` | int      | Yes      | Streets where villain bet/raised prior to this decision |
| `'_villain_checked_back'` | int (0/1)    | Yes      | 1 if villain checked any prior street |
| `'_villain_call_count'` | int            | Yes      | Streets where villain flat-called prior to this decision |

---

## Source Mapping: Game State Field → hand Dict Key

### From `context` dict (set in `_ai_turn` and `_hero_turn`)

| context key               | hand dict key            | Notes |
|---------------------------|--------------------------|-------|
| `context['pot']`          | `'pot'`                  | Direct |
| `context['to_call']`      | `'tc'`                   | Direct |
| `context['street']`       | maps to `'st'`           | Needs STREET_CODE translation (see below) |
| `context['facing_bet']`   | `'fb'`                   | Cast to int |
| `context['opener_position']` | `'_opener_position'`  | May be None |
| `context['num_raises_this_street']` | `'_num_raises_this_street'` | Direct |
| `context['active_opponents']` | used to count `'_num_opponents'` | Filter `not p.is_folded` |

`villain_position` is in `context` for the hero path (`_hero_turn`). It is
NOT in the AI path (`_ai_turn`) context. See the villain position section below.

### From `player` directly

| player attribute          | hand dict key            | Notes |
|---------------------------|--------------------------|-------|
| `player.hole_cards`       | `'h'`                    | `''.join(str(c) for c in player.hole_cards)` |
| `player.position`         | `'pos'`                  | Direct |
| `player.stack`            | used for `spr` gap only  | See gaps section |

### From `game` directly

| game attribute            | hand dict key            | Notes |
|---------------------------|--------------------------|-------|
| `game.community_cards`    | `'b'`                    | `''.join(str(c) for c in game.community_cards)` |
| `game.raises_this_street` | `'_num_raises_this_street'` | Use `getattr(game, 'raises_this_street', 0)` |
| `game.opener_position`    | `'_opener_position'`     | `game.opener_position or None` |

### Street code translation

`poker_game.py` defines `STREET_CODE = {'flop': 'f', 'turn': 't', 'river': 'r'}`.
Preflop is absent from this dict. The feature extractor's `STREET_ENCODING`
maps `'p'` to preflop. The bridge must map:

```python
_STREET_CODE = {'preflop': 'p', 'flop': 'f', 'turn': 't', 'river': 'r'}
```

### Villain position selection

The bridge must replicate the logic in `run_coaching()`:

```python
if context['facing_bet'] and context.get('villain_position'):
    vp = context['villain_position']
elif context['facing_bet'] and context.get('bettor_position'):
    vp = context['bettor_position']
else:
    villains = [p for p in context['active_opponents']
                if not p.is_folded]
    vp = max(villains, key=lambda p: p.stack).position if villains else 'BB'
```

Note: `villain_position` is present in the hero path context (`_hero_turn`)
but not in the AI path context (`_ai_turn`). The AI path uses
`context.get('villain_position', '')` — the bridge must handle both cases.

### Action history features

The game does not currently track per-street villain action history
(`_villain_aggression_count`, `_villain_checked_back`, `_villain_call_count`,
`_is_3bet_pot`). This is the primary gap — see the Gaps section.

For the initial implementation, set these to their safe defaults:

```python
'_is_3bet_pot': 1 if getattr(game, 'raises_this_street', 0) >= 2
                    and game.street == 'preflop' else 0,
'_villain_aggression_count': 0,
'_villain_checked_back': 0,
'_villain_call_count': 0,
```

`_is_3bet_pot` can be derived from `raises_this_street >= 2` on preflop. The
other three require a postflop action log that does not exist yet on `Game`.

---

## Complete Implementation

```python
"""
game_state_bridge.py

Bridges live PokerGame state to the feature extraction pipeline.

Usage:
    from game_state_bridge import build_features_from_game_state
    from gto_model import GtoOracle
    import numpy as np

    feat_dict = build_features_from_game_state(player, game, context)
    feature_array = GtoOracle.features_from_dict(feat_dict)
    prediction = oracle.predict(feature_array)
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from poker_game import Player, Game

from feature_extractor import extract_all_features

_STREET_CODE = {'preflop': 'p', 'flop': 'f', 'turn': 't', 'river': 'r'}


def build_features_from_game_state(
    player: "Player",
    game: "Game",
    context: dict,
) -> Dict:
    """
    Convert live game state to a 38-feature dict for GtoOracle.predict().

    Args:
        player: The player making the decision. Must have hole_cards and
                position set.
        game:   The Game instance. Used for community_cards, raises_this_street,
                opener_position.
        context: The context dict passed to decision_callback() by _ai_turn()
                 or hero_callback by _hero_turn(). Must contain at minimum:
                 'pot', 'to_call', 'street', 'facing_bet',
                 'active_opponents', 'num_raises_this_street',
                 'opener_position'.

    Returns:
        Complete feature dict from extract_all_features(). Contains all 38
        model keys and all underscore-prefixed metadata keys.
        Pass to GtoOracle.features_from_dict() to get a numpy array.
    """
    street_name: str = context['street']
    facing_bet: bool = bool(context['facing_bet'])
    to_call: float = float(context['to_call'])
    pot: float = float(context['pot'])
    active_opponents = context['active_opponents']

    # Hero cards: 'AhKs'
    hero_card_str = ''.join(str(c) for c in player.hole_cards)

    # Board cards: 'AhKs3d' or '' preflop
    board_str = ''.join(str(c) for c in game.community_cards)

    # Street code: 'p', 'f', 't', 'r'
    street_code = _STREET_CODE.get(street_name, 'f')

    # Villain position
    villain_pos = _resolve_villain_position(context, active_opponents)

    # Active opponent count (exclude folded; minimum 1)
    num_opponents = max(1, sum(
        1 for p in active_opponents if not p.is_folded
    ))

    # Opener position (first preflop raiser)
    opener_position = context.get('opener_position') or game.opener_position or None

    # Bettor position (who made the current bet/raise we are facing)
    bettor_position = context.get('villain_position') or None
    if not bettor_position and facing_bet:
        bettor_position = villain_pos

    # 3-bet pot detection: preflop with >= 2 raises
    raises_this_street = int(context.get(
        'num_raises_this_street',
        getattr(game, 'raises_this_street', 0),
    ))
    is_3bet_pot = 1 if (street_name == 'preflop' and raises_this_street >= 2) else 0

    hand = {
        'h':  hero_card_str,
        'b':  board_str,
        'pos': player.position,
        'vp':  villain_pos,
        'pot': pot,
        'tc':  to_call,
        'st':  street_code,
        'fb':  int(facing_bet),
        'exp': 'C',                           # placeholder label; not used by predict
        '_num_opponents':          num_opponents,
        '_num_raises_this_street': raises_this_street,
        '_opener_position':        opener_position,
        '_bettor_position':        bettor_position,
        '_is_3bet_pot':            is_3bet_pot,
        '_villain_aggression_count': 0,       # gap: no postflop action log yet
        '_villain_checked_back':     0,       # gap: no postflop action log yet
        '_villain_call_count':       0,       # gap: no postflop action log yet
    }

    return extract_all_features(hand)


def _resolve_villain_position(context: dict, active_opponents: list) -> str:
    """
    Pick the villain position for range analysis.

    Priority order mirrors run_coaching():
    1. context['villain_position'] — set by _hero_turn() when facing a bet.
    2. The opponent with the largest stack among non-folded opponents.
    3. 'BB' as last-resort fallback.
    """
    vp = context.get('villain_position', '')
    if vp:
        return vp

    villains = [p for p in active_opponents if not p.is_folded]
    if villains:
        return max(villains, key=lambda p: p.stack).position

    return 'BB'
```

---

## Imports Required in game_state_bridge.py

```python
from __future__ import annotations
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from poker_game import Player, Game   # avoid circular import at runtime

from feature_extractor import extract_all_features
```

`feature_keys.F` is not needed directly in the bridge — the string constants
are embedded in `feature_extractor.py` and the caller sees only the output
dict. If the caller needs to reference keys, they import from `feature_keys.py`
directly.

---

## Gaps: What Game State Does Not Provide

### Gap 1 — SPR uses hardcoded 100bb stack (medium severity)

`add_derived_features()` in `feature_extractor.py` computes:
```python
features['spr'] = round(DEFAULT_EFFECTIVE_STACK / pot, 4)
# DEFAULT_EFFECTIVE_STACK = 100.0
```

It ignores actual stack depth. The bridge cannot fix this without modifying
`feature_extractor.py`. The live game has `player.stack` available.

Recommended fix (out of scope for Blocker 3, file a separate task):
Overwrite `spr` in the returned feature dict after `extract_all_features()`:
```python
features = extract_all_features(hand)
if pot > 0 and player.stack > 0:
    effective_stack = min(player.stack,
                          min(p.stack for p in active_opponents if not p.is_folded))
    features['spr'] = round(effective_stack / pot, 4)
return features
```
This is a one-line post-processing step the bridge can apply without touching
`feature_extractor.py`. Include it in the implementation if stack accuracy
matters for the GtoOracle at current stack depths.

### Gap 2 — villain_aggression_count, villain_checked_back, villain_call_count (high severity for postflop)

These three features track villain behaviour across prior streets:
- `villain_aggression_count`: how many streets villain bet or raised before now
- `villain_checked_back`: did villain ever check behind on a prior street
- `villain_call_count`: how many streets villain flat-called before now

The `Game` class does not record this per-player postflop action history.
`pokerbench_parser.py` builds these from a full hand history string. The
live game has no equivalent.

For Blocker 3 these default to 0, which is the same as gauntlet hands that
lack action history. The model was trained to treat 0 as neutral. Predictions
will be correct for the most common cases (first decision on a street, facing
a c-bet). They will be less accurate for delayed aggression and check-raise
situations on the turn and river.

Recommended fix (separate task, medium priority):
Add a `per_player_action_log: Dict[str, List[str]]` dict to `Game` that
records `'bet'`, `'raise'`, `'check'`, `'call'` per player per street.
The bridge reads this log at decision time and computes the three counts.
This is a `Game` class change, not a feature extractor change.

### Gap 3 — preflop board is empty string (low severity, by design)

When `street == 'preflop'`, `game.community_cards` is empty. The bridge
passes `'b': ''`. `parse_board('')` in `feature_extractor.py` returns `[]`.
All board-texture features (board_features step 3) will be 0 / defaults.
This is correct and intentional — the model handles preflop correctly
with an empty board.

### Gap 4 — 'exp' label field (no impact on prediction)

The `'exp'` key is the GTO action label used during training. In the
prediction path it is read only by `extract_zero_compute_features()` to
populate the `'action'` key in the feature dict. That `'action'` key is not
in `FEATURE_COLUMNS` and is not passed to the model. Setting `'exp': 'C'`
is correct and has no effect on prediction accuracy.

---

## Call Site Example

In a `decision_callback`:

```python
from game_state_bridge import build_features_from_game_state
from gto_model import GtoOracle

oracle = GtoOracle("/path/to/gto_model_v4_compact.json")

def my_callback(game, player, context):
    feat_dict = build_features_from_game_state(player, game, context)
    feature_array = GtoOracle.features_from_dict(feat_dict)
    prediction = oracle.predict(feature_array)
    # prediction.action is "FOLD", "CHECK", "CALL", "BET", or "RAISE"
    # prediction.confidence is 0.0-1.0
    return _map_oracle_action_to_game_action(prediction.action, context)
```

---

## Verification Checklist for Programmer

Before marking Blocker 3 done, the Programmer must verify:

1. `build_features_from_game_state()` returns a dict with all 38 keys in
   `gto_model.FEATURE_COLUMNS` present and non-None.

2. Calling `GtoOracle.features_from_dict(feat_dict)` on the result produces
   a numpy array of shape `(38,)` with no NaN values.

3. `oracle.predict(array)` returns an `OraclePrediction` without raising.

4. With a preflop hand (empty board), `features['street'] == 0` and all
   board texture features (`is_monotone`, `is_paired`, etc.) are 0.

5. With a postflop hand, `features['street']` is 1 (flop), 2 (turn), or
   3 (river) and `features['_board_cards']` has the correct length.

6. `features['_num_opponents']` matches the count of non-folded opponents
   in `context['active_opponents']`.

7. `features['_opener_position']` is None when no preflop raise has occurred
   and a non-None string after a raise.

Test file location: `/home/rupertbeytell/river-rats-v2/river-rats-core/tests/test_game_state_bridge.py`
