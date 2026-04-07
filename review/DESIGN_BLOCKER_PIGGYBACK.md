# Flush Blocker Piggyback — Architecture Findings

**Date:** 2026-04-06
**Scope:** Can flush-blocker computation piggyback on the existing range-composition loop?

---

## 1. How the existing loop works

`extract_range_composition()` lives at line 1090 of
`river-rats-core/feature_extractor.py`.

It does the following in sequence:

1. Calls `get_villain_range(hero_pos, villain_pos, opener_pos)` to get
   villain's preflop range as `{hand_notation: frequency}` where keys
   are **GTO range notation** — `'AKs'`, `'QQ'`, `'T9o'`, etc. (not
   specific card combos).
2. Optionally narrows to the betting range via
   `narrow_to_betting_range(v_range, board_cards, street_name)`.
3. Iterates once over every `(hand_notation, freq)` pair in the range.
4. For each entry calls `classify_hand(hand_notation, board_cards)`,
   which internally uses `_parse_hand_to_cards()` to pick **one
   representative combo** for that notation before evaluating.
5. Accumulates `top_pair_plus_weight`, `draw_weight`, `air_weight`
   against `total_weight`, then computes percentages.

The loop is the only range iteration in this step. There is no second
pass, no memoisation, and no pre-expanded combo list.

---

## 2. How villain_pos and hero_pos reach the loop

`extract_all_features()` (line 1211) reads `_hero_pos_raw` and
`_villain_pos_raw` from the feature dict, which were stored there by
`extract_zero_compute_features()` (line 165) at extraction time.
Both come directly from `hand['pos']` and `hand.get('vp')`.

Hero's hole cards are also stored at that step as `_hero_cards` (a
list of specific card strings, e.g. `['Ah', 'Kh']`).

The call site for `extract_range_composition` at line 1250 passes
`board_cards=features.get('_board_cards', [])` but does **not** pass
`hero_cards`. That parameter does not currently exist on
`extract_range_composition`.

---

## 3. What villain_draw_pct already captures

`villain_draw_pct` counts the fraction of villain's range whose
`classify_hand()` category is `'draw'`. That category maps to hands
with a flush draw or straight draw with 8+ outs (see `range_narrowing.py`
line 231). Weaker draws (gutshots, backdoors) fall into `'bluff'`.

So `villain_draw_pct` already identifies which hands in villain's range
are strong draws — but it does NOT record which specific suits those
draws are in, and it does NOT check whether hero holds any of those
suit cards.

---

## 4. The blocker piggyback problem — range notation vs. combo expansion

This is the critical constraint.

The range dict keys are **notation strings** (`'AKs'`, `'QQ'`), not
specific combos. A single key like `'AhKh'` would exist only if the
input range was already combo-expanded, which it is not — the RFI and
defend ranges from `RangeManager` store notation-level keys (confirmed
at `range_manager.py` line 85: `HandNotation: TypeAlias = str`).

When `classify_hand('AKs', board)` runs, `_parse_hand_to_cards`
(in `range_narrowing.py` line 270) picks **one** suited combo by
scanning suits in order and returning the first available one. It does
not enumerate all four suited combos. This is explicitly documented as
the "single fixed-suit combo" problem that was fixed for range
partitioning (Step 5 of feature extraction, line 345).

Step 5 — `get_valid_combos()` at line 339 — already has the fixed
version: it enumerates all valid combos for a notation given the
used-card set. For suited hands it generates up to 4 combos, for
offsuit hands up to 12, for pairs up to 6.

**Consequence for flush blockers:**

To count "how many of villain's flush-draw combos does hero block,"
you need to operate at the **combo level**, not the notation level.
For `'AKs'` on a two-tone heart board:
- `AhKh` — hero blocks this if hero holds `Ah` or `Kh`
- `AdKd`, `AcKc`, `AsKs` — these are not the flush draw suit

`classify_hand('AKs', board)` returns the classification for one
arbitrarily chosen combo. If it happens to pick `AhKh`, it flags
a draw; if it picks `AsKs` on a heart board, it does not.

---

## 5. What "piggybacking" actually requires

**If you want a correct flush-blocker count, you cannot piggyback on
the existing classify_hand loop as-is.** You would need to replace the
notation-level iteration with a combo-level iteration using
`get_valid_combos()`.

The change is contained inside `extract_range_composition` only. The
interface and all callers stay the same.

The revised inner loop would look like:

```python
used_cards = set(c.lower() for c in board_cards) | set(c.lower() for c in hero_cards)
hero_suits = {c[1].lower() for c in hero_cards}  # e.g. {'h', 'd'}

for hand_notation, freq in v_range.items():
    combos = get_valid_combos(hand_notation, used_cards)
    if not combos:
        continue
    per_combo_weight = freq / len(combos)

    for combo in combos:
        try:
            classification = classify_hand_from_combo(combo, board_cards)
        except Exception:
            continue

        category = classification.category
        if street_name == 'river' and category == 'draw':
            category = 'air'

        total_weight += per_combo_weight

        if category in _TOP_PAIR_PLUS:
            top_pair_plus_weight += per_combo_weight
        elif category in _DRAW_CATEGORIES:
            draw_weight += per_combo_weight
            # Blocker check — hero holds a card in this draw's suit
            draw_suit = _flush_draw_suit(combo, board_cards)
            if draw_suit and draw_suit in hero_suits:
                flush_blocker_draw_weight += per_combo_weight
        elif category in _AIR_CATEGORIES:
            air_weight += per_combo_weight
```

Where `_flush_draw_suit(combo, board_cards)` returns the suit of
the flush draw if the combo has one, else None.

**classify_hand_from_combo** would accept `[card1, card2]` directly
instead of going through `_parse_hand_to_cards`. That function already
exists conceptually — `classify_hand` calls `_parse_hand_to_cards` and
then `evaluate_hand`. You would skip the parse step and call
`evaluate_hand(combo, board_cards)` directly.

---

## 6. Performance cost

`get_valid_combos` is already used in Step 5 (range partitioning) for
every hand in the range, so it is not a new dependency. The combo
expansion loop replaces O(N) calls with O(N * avg_combos) calls where
avg_combos ≈ 4–6 across a typical range. That is a 4–6x increase in
`evaluate_hand` calls inside this step.

Step 9 (range composition) is currently called once per hand record.
The hand evaluator is fast (pure Python ranking, no eval7 in this
path). A typical villain range has ~50–80 notation entries, expanding
to ~250–400 combos. This is still well under 1ms per hand on a modern
machine.

**The key performance fact:** if the loop stays at the notation level,
adding a flush-blocker check is nearly free. But the notation-level
loop is architecturally incorrect for this use case — the blocker check
would fire or not fire based on which arbitrary suit `_parse_hand_to_cards`
happened to pick. That would produce a noisy, misleading feature.

The correct implementation requires combo expansion, which carries a
4–6x cost increase for this one step. That is acceptable.

---

## 7. What needs to be built

1. A helper `_flush_draw_suit(combo: List[str], board: List[str]) -> Optional[str]`
   that returns the draw suit if the combo is a flush draw on this board,
   else None. This is a simple suit-count check — no full hand evaluation
   needed.

2. Modify `extract_range_composition` to accept `hero_cards: List[str]`
   as a new parameter (currently not passed).

3. Replace the notation-level `classify_hand` loop with a combo-level
   expansion using `get_valid_combos`, distributing `freq` evenly across
   each combo (`per_combo_weight = freq / len(combos)`).

4. Inside the draw bucket, call `_flush_draw_suit` and check hero_suits
   to accumulate `flush_blocker_draw_weight`.

5. Return `_villain_flush_draw_blocked_pct` (= `flush_blocker_draw_weight /
   total_weight`) from `extract_range_composition`.

6. Update the call site at line 1250 to pass
   `hero_cards=features.get('_hero_cards', [])`.

The existing `villain_draw_pct` computation remains correct and
unchanged — it now just operates at combo granularity rather than
notation granularity, which is strictly more accurate.

---

## 8. What does NOT need to change

- `range_narrowing.py` — untouched. `narrow_to_betting_range` runs its
  own notation-level loop, which is correct for its purpose (frequency
  weighting, not suit-level blocker checking).
- `RangeManager` — untouched. Range data stays as notation-keyed dicts.
- All callers of `extract_range_composition` — only the call site in
  `extract_all_features` needs the new `hero_cards` argument.
- Feature keys for existing features — no renames, no removals.
- The model — `_villain_flush_draw_blocked_pct` would be a metadata
  field (underscore-prefixed) for the teaching pipeline, same as the
  other range composition fields. It does not need to be a model feature
  unless ML-Architect decides to promote it.

---

## Summary

The existing loop in `extract_range_composition` **does** iterate over
villain's range and **does** classify draw combos. The key constraint
is that it operates on **range notation, not specific combos**, so
flush-suit identity is ambiguous. Piggybacking a flush-blocker count
on the existing loop is not architecturally valid at the notation level.

The correct path is a contained rewrite of the loop inside
`extract_range_composition` to use `get_valid_combos` (already present
in the same file), which makes the blocker check precise and keeps all
existing percentages correct. The performance cost is a 4–6x increase
in hand evaluations for this one step — acceptable and still sub-1ms
per hand.

All other files are untouched. The change is self-contained.
