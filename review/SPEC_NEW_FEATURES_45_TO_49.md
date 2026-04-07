# Spec: New Features 46–49 (Features after current 45)

**Date:** 2026-04-06
**Author:** Architecture Expert
**Status:** AWAITING REVIEW — no code written yet

---

## Summary

Four new features are proposed. This document identifies exact insertion
points in each file, describes what data is already available at each
point, provides exact Python for each computation, and flags
dependencies and open questions.

The current pipeline has 45 model features. These features would bring
the count to 49. They are numbered 46–49 in pipeline order.

---

## Existing infrastructure that the new features can reuse

### In `extract_board_features()` (feature_extractor.py line 281)

`analyze_board_cached()` returns a `BoardAnalysis` object. That object
already contains:

- `analysis.suit_counts` — `Dict[str, int]` mapping suit char to count
  (e.g. `{'h': 2, 's': 1}`)
- `analysis.max_suit_count` — `int`, highest suit count across all suits
- `analysis.flush_suit` — `Optional[str]`, the suit with 3+ cards (None
  if no flush possible)
- `analysis.high_card_rank` — `int`, highest board card rank (14=A,
  13=K, etc.)
- `analysis.ranks` — `List[int]`, all board card ranks

The `BoardAnalysis` object is currently thrown away after
`extract_board_features()` returns its dict. None of these fields are
passed downstream.

### In `extract_all_features()` (feature_extractor.py line 1211)

By the time Step 12 would run, the following are already in `features`:

- `features['_hero_cards']` — `List[str]`, e.g. `['Ah', 'Kd']`
- `features['_board_cards']` — `List[str]`, e.g. `['Jh', '8h', '2c']`
- `features['hand_category']` — encoded int (0–17 scale)
- `features['_hand_category_raw']` — raw string, e.g. `'top_pair'`
- `features['has_flush_draw']` — 0/1
- `features['is_monotone']`, `features['is_two_tone']` — 0/1 each
- `features['high_card_rank']` — int (board high card rank, 14=A)
- `features['raw_equity']` — float already computed

### In `hand_categories.py`

```python
RANKS = "AKQJT98765432"
```

Rank index maps to numeric value: `A=14, K=13, Q=12, J=11, T=10, ...`
The mapping used in `hand_evaluator.py` is `RANK_VALUES` (imported
there), which is `{rank_char: int}`.

---

## Problem: `BoardAnalysis` is not passed between steps

`extract_board_features()` currently creates the `BoardAnalysis` object
internally and discards it after extracting the 10 fields it needs. The
suit-level detail (`suit_counts`, `flush_suit`) is lost.

Features 46 and 47 require per-suit counts matched against hero cards.
This data is not in the current `features` dict. Two options:

**Option A (recommended):** Expose `_board_suit_counts` and
`_board_flush_suit` as metadata fields from `extract_board_features()`.
These get added to `features` and are available downstream.

**Option B:** Re-derive suit data from `features['_board_cards']` inline
in Step 12 (simple loop, no extra import needed).

Option B avoids touching `extract_board_features()` and keeps the
change self-contained. It is preferred for this spec because it
minimises blast radius.

---

## Feature 46: `blocks_flush_draw` (binary 0/1)

**Definition:** Hero holds a card matching the suit with exactly 2 cards
on board. Only set when `max_suit_count == 2` (draw territory — not a
completed flush).

### Where to insert

File: `feature_extractor.py`
Location: inside `extract_all_features()`, as a new Step 12 block,
after line 1271 (the current last line before `return features`).

### Data available at that point

- `features['_hero_cards']` — e.g. `['Ah', 'Kd']`
- `features['_board_cards']` — e.g. `['Jh', '8h', '2c']`
- `features['is_two_tone']` — 0/1 (board has exactly 2 of one suit on
  flop, or exactly 3 on turn/river — see note below)

**IMPORTANT:** `is_two_tone` does not directly map to
`max_suit_count == 2`. On the turn `is_two_tone` means
`max_suit_count == 3` (three-card flush draw, not two-card). On the
river `is_two_tone` also means `max_suit_count == 3`. Only on the flop
does `is_two_tone` mean exactly 2 cards of one suit.

Do NOT use `is_two_tone` as a proxy for this feature. Derive suit counts
directly from `_board_cards`.

### Exact Python

```python
# Step 12: Blocker features
# -----------------------------------------------------------------------
# Derive board suit counts from raw board cards (not BoardAnalysis, which
# is not threaded through). Simple loop — no extra import needed.
_b_suit_counts: Dict[str, int] = {}
for _c in features['_board_cards']:
    _s = _c[1]  # card string is rank+suit, e.g. 'Ah' -> 'h'
    _b_suit_counts[_s] = _b_suit_counts.get(_s, 0) + 1

_max_b_suit = max(_b_suit_counts.values()) if _b_suit_counts else 0

# 46. blocks_flush_draw
# Hero holds a card of the suit with exactly 2 board cards.
# Only meaningful when max_suit_count == 2 (early draw, not completed flush).
if _max_b_suit == 2:
    _draw_suit = max(_b_suit_counts, key=_b_suit_counts.get)
    features['blocks_flush_draw'] = int(
        any(_c[1] == _draw_suit for _c in features['_hero_cards'])
    )
else:
    features['blocks_flush_draw'] = 0
```

### Dependencies

None beyond what is already imported. `Dict` is already imported from
`typing`. `features['_board_cards']` and `features['_hero_cards']` are
both `List[str]`.

### `situation_factory.py` changes needed

None. `_hero_cards` and `_board_cards` are populated by
`extract_zero_compute_features()` from the `hand['h']` and `hand['b']`
strings that the bridge already constructs correctly.

---

## Feature 47: `blocks_made_flush` (binary 0/1)

**Definition:** Hero holds an Ace or King of the suit with 3+ cards on
board. Only set when a flush is possible (`max_suit_count >= 3`).

### Where to insert

File: `feature_extractor.py`
Location: immediately after Feature 46 code in the same Step 12 block.

### Data available at that point

Same as Feature 46. `_b_suit_counts` and `_max_b_suit` already computed
by the Feature 46 block.

### Exact Python

```python
# 47. blocks_made_flush
# Hero holds an A or K of the flush suit (3+ board cards of that suit).
_HIGH_RANKS = {'A', 'K'}
if _max_b_suit >= 3:
    _flush_suit = max(_b_suit_counts, key=_b_suit_counts.get)
    features['blocks_made_flush'] = int(
        any(_c[1] == _flush_suit and _c[0] in _HIGH_RANKS
            for _c in features['_hero_cards'])
    )
else:
    features['blocks_made_flush'] = 0
```

### Dependencies

None. `_b_suit_counts` and `_max_b_suit` come from the Feature 46 block
in the same Step 12. `_HIGH_RANKS` is a local constant defined inline.

### Note on interaction with `blocks_flush_draw`

The two features are mutually exclusive by design:
- `blocks_flush_draw` only fires when `_max_b_suit == 2`
- `blocks_made_flush` only fires when `_max_b_suit >= 3`

They cannot both be 1 simultaneously.

### `situation_factory.py` changes needed

None.

---

## Feature 48: `overcard_outs` (integer 0, 3, or 6)

**Definition:** Count of hero hole cards that rank strictly above the
highest board card. Each overcard = 3 outs. Result is 0, 3, or 6.

### Where to insert

File: `feature_extractor.py`
Location: immediately after Feature 47 code in the same Step 12 block.

### Data available at that point

- `features['high_card_rank']` — this is the board high card rank as an
  int (14=A, 13=K, etc.), set by `extract_board_features()` from
  `analysis.high_card_rank`. It is already in `features`.
- `features['_hero_cards']` — `List[str]`

### Rank parsing

Hero card rank chars map to ints. The mapping already exists in
`hand_categories.py` as an import in `hand_evaluator.py`. Rather than
adding a new import, define the rank map inline (it is a trivial 13-entry
dict and is already defined as `RANK_VALUES` in `hand_categories.py`).

**Option:** Import `RANK_VALUES` from `hand_categories` — it is already
imported at line 324 of `feature_extractor.py` (`from hand_categories
import RANKS`). Adding `RANK_VALUES` to that import is one character
change.

Check: `feature_extractor.py` line 324:
```python
from hand_categories import RANKS
```

Change to:
```python
from hand_categories import RANKS, RANK_VALUES
```

Verify `RANK_VALUES` exists in `hand_categories.py`. Grep confirmed:
`RANKS = "AKQJT98765432"` and the comment `# A=14, K=13, Q=12, ...2=2`
are both present. Check whether the dict is exported:

```
Grep: RANK_VALUES in hand_categories.py
```

This needs to be confirmed before implementation. If `RANK_VALUES` is
not exported, use the inline dict below instead.

### Exact Python (safe inline version — no new import needed)

```python
# 48. overcard_outs
# Rank lookup for hero card ranks (A=14 down to 2=2).
# Inline to avoid import dependency uncertainty.
_RANK_INT = {
    'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
    '9': 9, '8': 8, '7': 7, '6': 6, '5': 5,
    '4': 4, '3': 3, '2': 2,
}
_board_high = features['high_card_rank']  # already int, e.g. 14 for Ace
_overcard_count = sum(
    1 for _c in features['_hero_cards']
    if _RANK_INT.get(_c[0], 0) > _board_high
)
features['overcard_outs'] = _overcard_count * 3  # 0, 3, or 6
```

### Dependencies

`features['high_card_rank']` — confirmed set by `extract_board_features()`
at line 303:
```python
'high_card_rank': analysis.high_card_rank,
```
`analysis.high_card_rank` is the `int` from `BoardAnalysis`, confirmed
at board_analyzer.py line 264: `high_card_rank: int`.

### `situation_factory.py` changes needed

None. `high_card_rank` is produced by the existing board analysis step.

---

## Feature 49: `improvement_probability` (float 0.0–1.0)

**Definition:** Fraction of unseen cards that improve hero's hand
category to two-pair or better. "Two-pair or better" = `hand_category
>= 10` in the existing `HAND_CATEGORY_ENCODING` (line 139 of
feature_extractor.py: `'two_pair': 10`).

### Design constraint

The spec says this should "piggyback on existing equity/evaluation code."
The existing code is:
- `evaluate_hand(hero_cards, board_cards)` from `hand_evaluator.py` —
  already imported at line 239. Returns `HandEvaluation` with
  `.category` string.
- `HAND_CATEGORY_ENCODING` — already defined at line 139 of
  feature_extractor.py.

### Algorithm

1. Identify unseen cards: deck minus hero cards minus board cards.
2. For each unseen card, form `board + [card]` (simulates turn/river
   runout one card at a time).
3. Call `evaluate_hand(hero_cards, extended_board)`.
4. Check if the resulting category is two-pair or better.
5. `improvement_probability = count_improving / total_unseen`.

**Street handling:**
- Flop (3 board cards): 52 − 2 − 3 = 47 unseen cards, each added as
  turn. Board becomes 4 cards.
- Turn (4 board cards): 52 − 2 − 4 = 46 unseen cards, each added as
  river. Board becomes 5 cards.
- River (5 board cards): no unseen cards to try. Return 0.0 (or
  alternatively the current hand's value as a degenerate case, but
  0.0 is cleaner and the model can learn from context).

**Performance:** This calls `evaluate_hand()` up to 47 times per hand.
`evaluate_hand` contains no I/O and is pure Python arithmetic —
empirically fast. For batch training this adds ~47 × N calls. Acceptable
for the pipeline but worth noting.

### Where to insert

File: `feature_extractor.py`
Location: immediately after Feature 48 code in the same Step 12 block.

### Data available at that point

- `features['_hero_cards']` — `List[str]`
- `features['_board_cards']` — `List[str]`
- `features['_hand_category_raw']` — already-evaluated current category
  string (from Step 2). Use this to short-circuit: if current hand is
  already two-pair or better, `improvement_probability = 1.0`.
- `features['_street_raw']` — `'f'`, `'t'`, or `'r'` (already set by
  step 1 zero-compute features).

### Exact Python

```python
# 49. improvement_probability
# Fraction of unseen cards that improve hero to two-pair or better.
# TWO_PAIR threshold: hand_category encoded int >= 10.
_TWO_PAIR_THRESHOLD = 10  # matches HAND_CATEGORY_ENCODING['two_pair']

_current_cat_raw = features.get('_hand_category_raw', 'high_card')
_current_cat_enc = HAND_CATEGORY_ENCODING.get(_current_cat_raw, 0)

if _current_cat_enc >= _TWO_PAIR_THRESHOLD:
    # Already two-pair or better — trivially 1.0
    features['improvement_probability'] = 1.0
elif features.get('_street_raw', 'r') == 'r':
    # River: no more cards to come
    features['improvement_probability'] = 0.0
else:
    # Build the full deck and remove known cards
    _all_cards = [f"{_r}{_s}" for _r in RANKS for _s in 'shdc']
    _known = {_c.lower() for _c in features['_hero_cards']}
    _known.update(_c.lower() for _c in features['_board_cards'])
    _unseen = [_c for _c in _all_cards if _c.lower() not in _known]

    _improving = 0
    for _next_card in _unseen:
        _trial_board = features['_board_cards'] + [_next_card]
        try:
            _trial_eval = evaluate_hand(features['_hero_cards'], _trial_board)
            _trial_enc = HAND_CATEGORY_ENCODING.get(
                _trial_eval.category.lower(), 0
            )
            if _trial_enc >= _TWO_PAIR_THRESHOLD:
                _improving += 1
        except Exception:
            pass  # malformed board guard; should not occur in practice

    _total_unseen = len(_unseen)
    features['improvement_probability'] = (
        round(_improving / _total_unseen, 6) if _total_unseen > 0 else 0.0
    )
```

### Dependencies

- `evaluate_hand` — already imported at feature_extractor.py line 239.
- `HAND_CATEGORY_ENCODING` — already defined at line 139.
- `RANKS` — already imported at line 324 from `hand_categories`.
- `'shdc'` suits literal — matches `SUITS` constant in `hand_categories.py`.
  Can use `from hand_categories import SUITS` (already available in the
  module scope at line 336: `from hand_categories import SUITS`).
  Replace `'shdc'` with `SUITS` if preferred for consistency.

### `situation_factory.py` changes needed

None. All inputs come from the existing feature dict.

---

## Required changes to `feature_keys.py`

Add four new constants to the `F` class. Insert after line 63
(`FACING_RAISE = 'facing_raise'`):

```python
    BLOCKS_FLUSH_DRAW = 'blocks_flush_draw'
    BLOCKS_MADE_FLUSH = 'blocks_made_flush'
    OVERCARD_OUTS = 'overcard_outs'
    IMPROVEMENT_PROBABILITY = 'improvement_probability'
```

Use these constants in `feature_extractor.py` instead of raw strings
(e.g. `features[F.BLOCKS_FLUSH_DRAW] = ...`). This is optional for the
initial implementation but required before promotion to model features.

---

## Required changes to `gto_model.py`

If these features are promoted to model features (i.e. the model is
retrained on them), append to `FEATURE_COLUMNS` at line 50:

```python
    # Features 46-49: blocker + draw improvement features
    "blocks_flush_draw", "blocks_made_flush",
    "overcard_outs", "improvement_probability",
```

Update the comment at line 53: `N_FEATURES = len(FEATURE_COLUMNS)  # 49`

**Do not change `gto_model.py` until a new model is trained on these
features.** The current model was trained on exactly 45 features.
Changing `FEATURE_COLUMNS` before retraining will break
`GtoOracle.features_from_dict()`.

---

## Required changes to `feature_extractor.py` FEATURE_COLUMNS

Same caveat as `gto_model.py`. The local `FEATURE_COLUMNS` list at line
1012 controls CSV export. Append to it only when training data is being
regenerated:

```python
    # Step 12: blocker + improvement features (v10)
    'blocks_flush_draw', 'blocks_made_flush',
    'overcard_outs', 'improvement_probability',
```

---

## Changes to `game_state_bridge.py`

None required. The bridge calls `extract_all_features(hand)` and returns
whatever the extractor produces. New features added to Step 12 will
automatically appear in the returned dict.

---

## Changes to `situation_factory.py`

None required. The factory constructs hero/board/opponent stubs and
passes them through the bridge. It does not need to know about
individual features.

---

## Complete insertion point summary

| Feature | File | Insertion after line | Block |
|---|---|---|---|
| `blocks_flush_draw` | `feature_extractor.py` | 1271 (end of Step 11) | New Step 12 |
| `blocks_made_flush` | `feature_extractor.py` | After `blocks_flush_draw` | Same Step 12 |
| `overcard_outs` | `feature_extractor.py` | After `blocks_made_flush` | Same Step 12 |
| `improvement_probability` | `feature_extractor.py` | After `overcard_outs` | Same Step 12 |
| F.BLOCKS_FLUSH_DRAW etc. | `feature_keys.py` | Line 63 | After `FACING_RAISE` |
| FEATURE_COLUMNS additions | `gto_model.py` | Line 50 | After `facing_raise` |
| FEATURE_COLUMNS additions | `feature_extractor.py` | Line 1038 | After `facing_raise` |

---

## Open questions before implementation

1. **`RANK_VALUES` export:** Confirm whether `hand_categories.py` exports
   `RANK_VALUES` as a module-level name. If it does, replace the inline
   `_RANK_INT` dict in Feature 48 with an import. If it does not, keep
   the inline dict to avoid touching `hand_categories.py`.

2. **`improvement_probability` on river:** Returning 0.0 is defensible
   (no outs remain) but it means the model always sees 0.0 on the river
   regardless of hand strength. Confirm with the GTO Expert whether this
   is the intended semantic, or whether on the river the value should
   reflect the current made-hand quality instead (e.g. return 1.0 if
   already two-pair or better, 0.0 otherwise — which is what the
   short-circuit at the top of the block already does).

3. **Two-card draw threshold for `blocks_flush_draw`:** On the turn,
   `max_suit_count == 2` means two cards of one suit across four board
   cards — a weak, backdoor-level draw. Confirm whether the feature
   should only fire on the flop (where 2 suited board cards represent a
   real flush draw) or whether turn with 2 suited cards should also fire.
   The current spec says `exactly 2 cards of one suit on board` with no
   street restriction, which will fire on the turn with a backdoor draw.

4. **Performance budget:** `improvement_probability` calls `evaluate_hand`
   up to 47 times per hand. For a 10,000-hand training batch this is
   ~470,000 additional evaluations. Confirm this is acceptable before
   adding it to the batch pipeline. If not, consider approximating with
   the existing `draw_outs` and `has_flush_draw` signals instead.

---

## What does NOT need to change

- `poker_game.py` — no game-state changes needed
- `preflop_engine.py` — postflop-only features
- `range_manager.py` / `range_narrowing.py` — no range logic involved
- `oracle_router.py` — model selection by opponent count, not features
- Any test files — tests are written separately after this spec is approved
