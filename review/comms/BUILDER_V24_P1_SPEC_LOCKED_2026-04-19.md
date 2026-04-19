---
date: 2026-04-19
from: Builder
to: Main terminal / Owner
re: v2.4 P1 — revised-plan LOCKED spec (split approved) + Stage 1 execution
status: SPEC LOCKED — 4 features, implementation + backfill audit in this cycle
---

# v2.4 P1 — Spec Locked (Post-Split)

Owner approved the split (13857e2). Feature count: **4**. Vector
target: 55 → 59 raw (118 total with attn). This doc captures the
final, review-modified, owner-approved spec. All 3 plan docs +
3 GTO reviews + consolidated verdict remain in history; this is the
build target.

## Final feature list

| # | Name | Type | Direction for hero |
|---|---|---|---|
| 56 | `nut_flush_block` | int 0/1 | Aggressor positive (KB §1.7 canonical semi-bluff-raise trigger) |
| 57 | `flush_draw_block_pct` | float [0,1] | Defender negative (densification: blocks villain's flush semi-bluffs) |
| 58 | `straight_draw_block_pct` | float [0,1] | Defender negative (densification: blocks villain's straight semi-bluffs) |
| 59 | `nut_made_block_pct` | float [0,1] | Defender positive (villain's nut-made value combos reduced) |

## Feature specs (post-mods)

### 56. `nut_flush_block` (int 0/1)

```
= 1 IFF:
  (street==flop AND one-suit-count on board >= 2)   OR
  (street in {turn, river} AND one-suit-count on board >= 3)
  AND hero holds A-of-that-suit
  AND hero does NOT already have a made flush
    (hero_suit_count + board_suit_count < 5 for the relevant suit)

Otherwise 0.
```

Mods applied:
- M1 threshold split: 2+ flop / 3+ turn+river (was 2+ everywhere)
- M2 paired boards: NOT gated here; downgrade via v3.2 prompt
- M3 made-flush exclusion: explicit in code (was only in plan text)
- M4 K-of-suit companion REJECTED — covered by `flush_draw_block_pct`

### 57. `flush_draw_block_pct` (float [0,1])

```
= (villain flush-draw combos hero blocks) / (total villain flush-draw combos)

Where flush-draw combos = subcategory in
  {nut_flush_draw, flush_draw, combo_draw}

combo_draw counted here AND in straight_draw_block_pct (covers both classes).

Returns 0.0 (not NaN) when villain has no flush-draw combos.
```

### 58. `straight_draw_block_pct` (float [0,1])

```
= (villain straight-draw combos hero blocks) / (total villain straight-draw combos)

Where straight-draw combos = subcategory in
  {oesd, gutshot, combo_draw}

Returns 0.0 (not NaN) when villain has no straight-draw combos.
```

### 59. `nut_made_block_pct` (float [0,1])

```
= (villain nut-made combos hero blocks) / (total villain nut-made combos)

Where nut-made subcategories include:
  BASE: straight_flush, quads, full_house, nut_flush, nut_straight, top_set
  CONDITIONAL: strong_flush — ONLY when A-of-suit is on the board AND
              there are 3+ of that suit on board (second-nut flush is
              effective nut). Per M1 critical carve-out.

Returns 0.0 (not NaN) when villain has no nut-made combos.
```

## Implementation choices

- **New module:** `river-rats-core/blocker_features.py` (keeps
  feature_extractor surface clean)
- **Inline combo iteration:** do NOT modify `range_decomposition.py`.
  Instead import `_classify_combo_subcategory` and iterate
  combos in the new module (per reviewer guidance).
- **Use existing `get_valid_combos` + `_to_eval7_cards`:** avoids
  re-implementing combo enumeration logic.
- **Feature_extractor wiring:** add one helper call at the same
  point `compute_flush_block_pct` is invoked (after villain range
  narrowing when facing_bet=1).

## Wired features / schema changes

`feature_keys.py`:
- Add constants `NUT_FLUSH_BLOCK`, `FLUSH_DRAW_BLOCK_PCT`,
  `STRAIGHT_DRAW_BLOCK_PCT`, `NUT_MADE_BLOCK_PCT`

`feature_extractor.py`:
- Append 4 names to `FEATURE_COLUMNS` (55 → 59 raw)
- In `extract_all_features`: compute the 4 values from
  `blocker_features.compute_*` helpers; set via `features[F.X] = v`

`flush_block_pct` stays as-is (retirement deferred per directive-x).

## Unit tests

`river-rats-core/tests/test_blocker_features.py`:
- `nut_flush_block`: hero As on 2-spade flop → 1; hero Ac on 2-spade
  flop → 0; hero Ah+5h on Qh7h2h (3-heart flop, hero has flush) → 0;
  hero Ad on 2-spade turn (not 3+) → 0.
- `flush_draw_block_pct`: mock villain range with known flush-draw
  combos; hero blocker → expected fraction.
- `straight_draw_block_pct`: same shape for straight class.
- `nut_made_block_pct`: base case (no A on board) uses base
  nut-subcat set; A-on-board test activates strong_flush.
- M4 taxonomy-drift guard: assert every subcat string in
  `_NUT_MADE_BASE` + {'strong_flush'} exists in
  `range_decomposition.SUBCATEGORY_ORDER`.

## Backfill audit (Stage 1 deliverable)

After implementation, run the existing training CSV through the
feature extractor to produce the 4 new columns. Report:

1. **Distribution** per feature (min, p25, median, p75, max, mean,
   fraction-non-zero)
2. **Sanity checks:**
   - `nut_flush_block == 1` only on boards with 2+ same suit (flop)
     or 3+ (turn+)
   - `flush_draw_block_pct > 0` implies hero has at least one
     flush-suit card
   - `nut_made_block_pct > 0` implies villain has at least one
     nut-made combo in range
3. **I1 ask from plan 1 reviewer** — defensive bucket
   `(flush_draw_rank == 0 AND nut_flush_block == 1)` ≥ 2% of rows?
   If below, flag for v2.4 Stage 4 augmentation.

## NOT in Stage 1 scope

Per directive-x 6-stage sequence, Stage 1 is feature code +
backfill audit only:

- No KB §1.9 update (Stage 2)
- No v3.2 prompt derivation (Stage 3)
- No re-labelling (Stage 4)
- No training (Stage 5)
- No ship (Stage 6)

## Stage 1 completion signal

This cycle commits:
- `river-rats-core/blocker_features.py` (new helpers)
- `river-rats-core/feature_keys.py` (+ 4 constants)
- `river-rats-core/feature_extractor.py` (+ 4 feature columns wired)
- `river-rats-core/tests/test_blocker_features.py` (unit tests)
- Backfill audit report (next doc)

Then Stage 1 is done; Stage 2 (KB §1.9) begins next cycle.
