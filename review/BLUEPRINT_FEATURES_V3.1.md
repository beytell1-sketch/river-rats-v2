# Blueprint: Features V3.1 — 4 New Features, 1 Bug Fix, 1 Validator

**Status:** Ready for programmer implementation
**Target files:** feature_extractor.py, feature_keys.py, gto_model.py, situation_factory.py
**Feature count change:** 48 → 52

---

## Pre-implementation checks

Before touching any file, programmer must verify:

1. `feature_extractor.py` line 1040 ends with `'flush_block_pct', 'overcard_outs', 'improvement_probability',`
2. `gto_model.py` line 52 ends with `"flush_block_pct", "overcard_outs", "improvement_probability",`
3. `feature_keys.py` line 70 is `IMPROVEMENT_PROBABILITY = 'improvement_probability'`
4. `range_manager.py` line 1718 signature is `def get_hand_percentile(self, hand: str, range_dict: Dict[str, float], board: List[str], blocker_aware: bool = True) -> float:`
5. `situation_factory.py` line 295 is `def validate_situation(spec: SituationSpec, feat_dict: dict) -> List[str]:`
6. `feature_extractor.py` line 1258 is `    if len(hero_flush_suit_cards) >= 2:`
7. `feature_extractor.py` line 1259 is `        return 0.0`

If any of these do not match, STOP and report BLOCKED.

---

## Change 1: Feature #49 — hero_range_percentile

**What it does:** Calls `_range_manager.get_hand_percentile()` with hero's hand notation
and hero's own preflop range to produce a [0.0, 1.0] score showing where this specific
hand sits within hero's range on this board. 1.0 = top of range.

**How get_hand_percentile works (range_manager.py lines 1718-1781):**
- Takes `hand` as a notation string (e.g. 'AKo', 'JJ'), NOT specific cards
- Takes `range_dict` as the range to compare within (hero's own range, not villain's)
- Takes `board` as the board card list
- Converts the hand to notation internally, computes strength of each combo in the range,
  and returns `(worse_count + equal_count * 0.5) / total`
- Input hand must be in standard notation — use `cards_to_notation()` to convert
  from specific hole cards

**Converting hole cards to notation:** `cards_to_notation` is imported from
`hand_categories` in `range_manager.py`. It is NOT currently imported in
`feature_extractor.py`. The programmer must add this import.

`cards_to_notation` is already imported in `poker_game.py` as:
`from hand_categories import cards_to_notation`

**Hero's range:** Call `_range_manager.get_postflop_range(hero_pos, is_pfr)`. The
`is_pfr` flag should default to `True` since the oracle is always in opened pots. For
correctness, derive it from `opener_pos`: hero is PFR when their position matches the
opener. When `opener_pos` is None, default to `True`.

### 1a. feature_keys.py — add constant

File: `/home/rupertbeytell/river-rats-v2/river-rats-core/feature_keys.py`

```
old_string:
    # Step 12: new features 46-48
    FLUSH_BLOCK_PCT = 'flush_block_pct'
    OVERCARD_OUTS = 'overcard_outs'
    IMPROVEMENT_PROBABILITY = 'improvement_probability'

new_string:
    # Step 12: new features 46-48
    FLUSH_BLOCK_PCT = 'flush_block_pct'
    OVERCARD_OUTS = 'overcard_outs'
    IMPROVEMENT_PROBABILITY = 'improvement_probability'

    # Step 13: new features 49-52
    HERO_RANGE_PERCENTILE = 'hero_range_percentile'
    HAS_SHOWDOWN_VALUE = 'has_showdown_value'
    VILLAIN_FOLD_EQUITY_ESTIMATE = 'villain_fold_equity_estimate'
    FLUSH_DRAW_RANK = 'flush_draw_rank'
```

### 1b. feature_extractor.py — consolidate imports and add cards_to_notation

File: `/home/rupertbeytell/river-rats-v2/river-rats-core/feature_extractor.py`

**Two edits required.** First, add cards_to_notation to the line 324 import:
```
old_string:
from hand_categories import RANKS

new_string:
from hand_categories import RANKS, cards_to_notation
```

Then remove the duplicate SUITS import at line 336 and consolidate:
```
old_string:
from hand_categories import SUITS

new_string:
# SUITS already available via hand_categories — consolidated with RANKS import above
```

Note: After this edit, add SUITS to the line 324 import if any code below uses SUITS directly:
```
from hand_categories import RANKS, SUITS, cards_to_notation
```

### 1c. feature_extractor.py — add computation function

File: `/home/rupertbeytell/river-rats-v2/river-rats-core/feature_extractor.py`

Insert immediately after the closing of `compute_improvement_probability` (find the
function's final `return` line, which ends the function body around line ~1430). The
insertion anchor is the blank line that precedes the next section header.

```
old_string:

def extract_all_features(hand: Dict) -> Dict:

new_string:
def compute_hero_range_percentile(
    hero_cards: List[str],
    board_cards: List[str],
    hero_pos: str,
    opener_pos: Optional[str],
) -> float:
    """
    Feature 49: Where does hero's hand sit within their own range on this board?

    Calls _range_manager.get_hand_percentile() with hero's preflop range.
    Returns 0.0-1.0 where 1.0 = top of hero's range.

    Args:
        hero_cards: e.g. ['Ah', 'Kd']
        board_cards: e.g. ['Jh', '8c', '2s']
        hero_pos: e.g. 'BTN'
        opener_pos: Preflop raiser's position, or None.

    Returns:
        Float [0.0, 1.0]
    """
    if not hero_cards or len(hero_cards) < 2 or not board_cards:
        return 0.5

    hand_notation = cards_to_notation(hero_cards[0], hero_cards[1])

    # Hero is PFR when opener_pos matches hero_pos or when opener_pos is unknown.
    is_pfr = (
        opener_pos is None
        or opener_pos.upper() == hero_pos.upper()
    )
    hero_range = _range_manager.get_postflop_range(hero_pos, is_pfr=is_pfr)
    if not hero_range:
        return 0.5

    return round(
        _range_manager.get_hand_percentile(hand_notation, hero_range, board_cards),
        6,
    )


def extract_all_features(hand: Dict) -> Dict:
```

### 1d. feature_extractor.py — add to FEATURE_COLUMNS

File: `/home/rupertbeytell/river-rats-v2/river-rats-core/feature_extractor.py`

```
old_string:
    # Step 12: new features 46-48
    'flush_block_pct', 'overcard_outs', 'improvement_probability',
]

new_string:
    # Step 12: new features 46-48
    'flush_block_pct', 'overcard_outs', 'improvement_probability',
    # Step 13: new features 49-52
    'hero_range_percentile', 'has_showdown_value',
    'villain_fold_equity_estimate', 'flush_draw_rank',
]
```

### 1e. feature_extractor.py — wire into extract_all_features

File: `/home/rupertbeytell/river-rats-v2/river-rats-core/feature_extractor.py`

```
old_string:
    features[F.IMPROVEMENT_PROBABILITY] = compute_improvement_probability(
        hero_cards, board_cards, features.get('hand_category', 0)
    )

    return features

new_string:
    features[F.IMPROVEMENT_PROBABILITY] = compute_improvement_probability(
        hero_cards, board_cards, features.get('hand_category', 0)
    )

    # Step 13: New features 49-52
    _s13_opener_pos = hand.get('_opener_position', None)
    features[F.HERO_RANGE_PERCENTILE] = compute_hero_range_percentile(
        hero_cards, board_cards,
        features.get('_hero_pos_raw', 'BTN'),
        _s13_opener_pos,
    )
    features[F.HAS_SHOWDOWN_VALUE] = int(
        features.get('is_made_hand', 0) == 1
        and features.get('hand_category', 0) >= 3
    )
    _vtp = features.get(F.VILLAIN_TOP_PAIR_PLUS_PCT, 0.0)
    _vdp = features.get(F.VILLAIN_DRAW_PCT, 0.0)
    _num_opp = features.get(F.NUM_OPPONENTS, 1)
    _per_opp_fold = 1.0 - (_vtp + 0.5 * _vdp)
    _per_opp_fold = max(0.0, min(1.0, _per_opp_fold))
    features[F.VILLAIN_FOLD_EQUITY_ESTIMATE] = round(
        _per_opp_fold ** _num_opp, 6
    )
    features[F.FLUSH_DRAW_RANK] = compute_flush_draw_rank(
        hero_cards, board_cards
    )

    return features
```

### 1f. gto_model.py — add to FEATURE_COLUMNS

File: `/home/rupertbeytell/river-rats-v2/river-rats-core/gto_model.py`

```
old_string:
    # v9 features (45→48): blocker + outs + improvement
    "flush_block_pct", "overcard_outs", "improvement_probability",
)

new_string:
    # v9 features (45→48): blocker + outs + improvement
    "flush_block_pct", "overcard_outs", "improvement_probability",
    # v9 features (48→52): range percentile, showdown value, fold equity, flush draw rank
    "hero_range_percentile", "has_showdown_value",
    "villain_fold_equity_estimate", "flush_draw_rank",
)
```

---

## Change 2: Feature #50 — has_showdown_value

This feature is a derived boolean: `int(is_made_hand == 1 and hand_category >= 3)`.

`hand_category >= 3` corresponds to `bottom_pair` (3) or better in
`HAND_CATEGORY_ENCODING`. This is the threshold for "has showdown value" —
bottom pair is the weakest hand worth seeing a showdown with.

This feature is wired into `extract_all_features` in Change 1e above (the Step 13 block).
No separate function is needed — the expression is inline.

All registration (feature_keys.py, FEATURE_COLUMNS in both files) is covered in
Changes 1a, 1d, and 1f above.

---

## Change 3: Feature #51 — villain_fold_equity_estimate

This feature estimates the probability all opponents fold to a bet, using villain
range composition features that are already computed earlier in `extract_all_features`.

Formula:
```
per_opp_fold = 1.0 - (villain_top_pair_plus_pct + 0.5 * villain_draw_pct)
per_opp_fold = max(0.0, min(1.0, per_opp_fold))
fold_equity = per_opp_fold ** num_opponents
```

This is wired into `extract_all_features` in Change 1e above (the Step 13 block).
It reads `F.VILLAIN_TOP_PAIR_PLUS_PCT`, `F.VILLAIN_DRAW_PCT`, and `F.NUM_OPPONENTS`,
which are all populated earlier in Steps 8 and 10.

All registration is covered in Changes 1a, 1d, and 1f.

---

## Change 4: Feature #52 — flush_draw_rank

**What it does:** Returns the rank (2-14) of hero's highest-ranked card that matches
the board's flush suit. Returns 0 if hero has no card of that suit.

The "flush suit" is the suit with the most board cards (must have >= 2 to matter).
Use the same flush-suit detection logic already present in `compute_flush_block_pct`
(lines 1244-1252 of feature_extractor.py).

### 4a. feature_extractor.py — add computation function

Insert immediately before `compute_hero_range_percentile` (inserted in Change 1c).
That means inserting between the end of `compute_improvement_probability` and the
start of the `compute_hero_range_percentile` function.

The anchor for this insertion is the `old_string` from Change 1c. Replace it as follows
(this subsumes Change 1c — the programmer should apply this single edit instead of
applying 1c first and then inserting again):

```
old_string:

def extract_all_features(hand: Dict) -> Dict:

new_string:
def compute_flush_draw_rank(
    hero_cards: List[str],
    board_cards: List[str],
) -> int:
    """
    Feature 52: Rank of hero's highest card in the board's flush suit.

    Returns 2-14 (using RANK_VALUES: A=14, K=13, ..., 2=2).
    Returns 0 if hero has no card of the flush suit, or if there is no flush
    suit (no suit appears 2+ times on the board).

    Args:
        hero_cards: e.g. ['Jh', '9s']
        board_cards: e.g. ['Ah', '7h', '2d']

    Returns:
        Integer rank 0-14.
    """
    if not board_cards or not hero_cards:
        return 0

    # Find flush suit: suit with highest count on board (>= 2 required)
    board_suit_counts: Dict[str, int] = {}
    for card in board_cards:
        s = card[1].lower()
        board_suit_counts[s] = board_suit_counts.get(s, 0) + 1

    flush_suit = None
    max_count = 0
    for suit, count in board_suit_counts.items():
        if count > max_count:
            max_count = count
            flush_suit = suit
    if flush_suit is None or max_count < 2:
        return 0

    # Inline rank map (same as compute_overcard_outs)
    rank_map = {
        'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
        '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2,
    }

    best_rank = 0
    for card in hero_cards:
        if card[1].lower() == flush_suit:
            r = rank_map.get(card[0].upper(), 0)
            if r > best_rank:
                best_rank = r

    return best_rank


def compute_hero_range_percentile(
    hero_cards: List[str],
    board_cards: List[str],
    hero_pos: str,
    opener_pos: Optional[str],
) -> float:
    """
    Feature 49: Where does hero's hand sit within their own range on this board?

    Calls _range_manager.get_hand_percentile() with hero's preflop range.
    Returns 0.0-1.0 where 1.0 = top of hero's range.

    Args:
        hero_cards: e.g. ['Ah', 'Kd']
        board_cards: e.g. ['Jh', '8c', '2s']
        hero_pos: e.g. 'BTN'
        opener_pos: Preflop raiser's position, or None.

    Returns:
        Float [0.0, 1.0]
    """
    if not hero_cards or len(hero_cards) < 2 or not board_cards:
        return 0.5

    hand_notation = cards_to_notation(hero_cards[0], hero_cards[1])

    # Hero is PFR when opener_pos matches hero_pos or when opener_pos is unknown.
    is_pfr = (
        opener_pos is None
        or opener_pos.upper() == hero_pos.upper()
    )
    hero_range = _range_manager.get_postflop_range(hero_pos, is_pfr=is_pfr)
    if not hero_range:
        return 0.5

    return round(
        _range_manager.get_hand_percentile(hand_notation, hero_range, board_cards),
        6,
    )


def extract_all_features(hand: Dict) -> Dict:
```

NOTE: Change 1c is superseded by this edit. Do NOT apply Change 1c separately.
Apply only this single edit in Change 4a.

---

## Change 5: Bug fix — flush_block_pct (feature 46)

**File:** `/home/rupertbeytell/river-rats-v2/river-rats-core/feature_extractor.py`

**The bug:** `compute_flush_block_pct` (line ~1258) returns 0.0 when hero holds 2+
cards of the flush suit. The docstring says "hero has the draw, not a blocker" — but
this is wrong. When hero holds two cards of the flush suit, those two specific cards
remove combos from villain's range just as powerfully as (or more than) holding one.
The blocking effect is maximally informative in this case.

The fix: remove the early-return guard for `len(hero_flush_suit_cards) >= 2` and let
the existing combo-checking loop run unchanged. The loop at lines ~1270-1343 already
correctly identifies which villain combos contain the flush suit and whether hero's
specific cards would appear in them. It does not need to change.

```
old_string:
    # If hero has 2+ cards of the suit, hero HAS the draw — not a blocker
    if len(hero_flush_suit_cards) >= 2:
        return 0.0

    # Build set of used cards (hero + board) for combo validity

new_string:
    # Build set of used cards (hero + board) for combo validity
```

**Why this is safe:** The combo loop below already uses `get_valid_combos(hand_notation, used_cards)`
where `used_cards` includes all of hero's cards. When hero holds two flush-suit cards,
both are in `used_cards`, so `get_valid_combos` will naturally exclude any villain combo
that contains either of hero's cards. The `hero_blocks` check at line ~1308 correctly
fires when hero's specific rank+suit would have appeared in a combo. The arithmetic
is unchanged — blocked combos / total flush combos — just with a richer numerator.

---

## Change 6: Action sequence validator in situation_factory.py

**File:** `/home/rupertbeytell/river-rats-v2/river-rats-core/situation_factory.py`

### 6a. Add POSTFLOP_ORDER constant

The validator needs to know postflop acting order (SB first, then BB, UTG/EP, HJ/MP, CO, BTN).
Rather than importing from feature_extractor.py (circular-risk), define it locally in
situation_factory.py.

```
old_string:
from game_state_bridge import build_features_from_game_state

new_string:
from game_state_bridge import build_features_from_game_state

# Postflop acting order — SB first (OOP), BTN last (IP).
# Used by validate_action_sequence().
_POSTFLOP_ORDER = {
    'SB': 0, 'BB': 1,
    'UTG': 2, 'EP': 2,
    'HJ': 3, 'MP': 3,
    'CO': 4,
    'BTN': 5,
}
```

### 6b. Add validate_action_sequence() function

Insert the new function immediately before `validate_situation`. The anchor is the
section header comment above `validate_situation`:

```
old_string:
# =============================================================================
# Validation
# =============================================================================

def validate_situation(spec: SituationSpec, feat_dict: dict) -> List[str]:

new_string:
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
```

### 6c. Call validate_action_sequence from validate_situation

```
old_string:
    errors: List[str] = []

    # 1. Equity sanity

new_string:
    errors: List[str] = []

    # 0. Action sequence structural validation
    errors.extend(validate_action_sequence(spec))

    # 1. Equity sanity
```

---

## Implementation order

Apply changes in this order to avoid broken intermediate states:

1. `feature_keys.py` — Change 1a (add 4 constants)
2. `gto_model.py` — Change 1f (extend FEATURE_COLUMNS tuple)
3. `feature_extractor.py` — Change 1b (add cards_to_notation import)
4. `feature_extractor.py` — Change 1d (extend FEATURE_COLUMNS list)
5. `feature_extractor.py` — Change 4a (add compute_flush_draw_rank + compute_hero_range_percentile before `def extract_all_features`)
6. `feature_extractor.py` — Change 5 (remove flush_block_pct early-return guard)
7. `feature_extractor.py` — Change 1e (wire Step 13 into extract_all_features)
8. `situation_factory.py` — Change 6a (add _POSTFLOP_ORDER constant)
9. `situation_factory.py` — Change 6b (add validate_action_sequence function)
10. `situation_factory.py` — Change 6c (call validator from validate_situation)

---

## Invariants the programmer must not break

- `N_FEATURES` in `gto_model.py` is set to `len(FEATURE_COLUMNS)` — it will auto-update
  to 52 when the tuple is extended. Do not hardcode 52.
- The `extract_all_features` Step 13 block reads `F.VILLAIN_TOP_PAIR_PLUS_PCT` and
  `F.VILLAIN_DRAW_PCT` — these are promoted in Step 10 which runs before Step 12/13.
  Do not reorder the steps in `extract_all_features`.
- `compute_flush_draw_rank` uses an inline rank_map (same as `compute_overcard_outs`)
  rather than importing RANK_VALUES, to keep it self-contained. Do not change this
  to import-based.
- `validate_action_sequence` uses `_POSTFLOP_ORDER` defined at module level in
  situation_factory.py. Do not move this dict into the function body (it will be
  re-created on every call for no reason).

---

## Expected N_FEATURES after all changes

`gto_model.py`: `N_FEATURES = len(FEATURE_COLUMNS)` = 52
`feature_extractor.py`: `FEATURE_COLUMNS` list length = 52

Both must agree. If they differ after implementation, there is a missing or duplicate
entry — find it before declaring done.

---

## Test cases the tester must write before implementation runs

### Feature #49 — hero_range_percentile
- BTN hero with AA on K72r board should return > 0.8 (AA is top of BTN range)
- BB hero with 72o on K72r board should return < 0.2 (72o is bottom of BB range)
- Board = [] should return 0.5 (fallback, no board)

### Feature #50 — has_showdown_value
- hand_category=3 (bottom_pair), is_made_hand=1 → 1
- hand_category=2 (overcards), is_made_hand=0 → 0
- hand_category=8 (overpair), is_made_hand=1 → 1
- hand_category=0, is_made_hand=1 → 0 (edge: made hand below threshold)

### Feature #51 — villain_fold_equity_estimate
- villain_top_pair_plus_pct=0.0, villain_draw_pct=0.0, num_opponents=1 → 1.0
- villain_top_pair_plus_pct=0.5, villain_draw_pct=0.0, num_opponents=1 → 0.5
- villain_top_pair_plus_pct=0.0, villain_draw_pct=1.0, num_opponents=2 → 0.25
- villain_top_pair_plus_pct=0.7, villain_draw_pct=0.5, num_opponents=1 → 0.0 (clamped)

### Feature #52 — flush_draw_rank
- hero=['Jh', '9s'], board=['Ah', '7h', '2d'] → 11 (J=11 is hero's heart card)
- hero=['Jh', '9h'], board=['Ah', '7h', '2d'] → 11 (highest of J=11 and 9=9)
- hero=['Js', '9s'], board=['Ah', '7h', '2d'] → 0 (hero has no hearts)
- hero=['Ah', '9h'], board=['7c', '2d', '3s'] → 0 (no flush suit, max board count=1)

### Bug fix — flush_block_pct
- hero=['Jh', '9h'], board=['Ah', '7h', '2d'] — should now return > 0.0
  (hero blocks JhXh and 9hXh combos from villain's range)
- hero=['Jh', '9s'], board=['Ah', '7h', '2d'] — should still return > 0.0
  (one-card blocker, existing behavior unchanged)
- hero=['Ts', '9s'], board=['Kd', '7c', '2h'] — should return 0.0
  (max board suit count = 1, no flush suit)

### Validator — validate_action_sequence
- BTN acts before BB on flop → error containing "ACTION_ORDER"
- BB skipped between SB and CO on turn → error containing "MISSING_ACTION"
- Valid SB→BB→CO sequence → no errors
- Preflop-only action_history → no errors (preflop not validated)
