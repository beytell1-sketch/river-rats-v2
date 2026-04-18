---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder
re: v2.3.1 fix — board-adjusted HRP feature + targeted label cleanup
status: DIRECTIVE — execute both in sequence
supersedes: update-e §3 re-label scope (SUSPECT only, not all override-fired)
---

# v2.3.1 Fix — Two Layers

Both layers needed. Neither alone is sufficient.

## Layer 1 — Add `board_adjusted_hrp` derived feature

### What

One new derived feature in `feature_extractor.py`:

```python
board_adjusted_hrp = hero_range_percentile * equity_vs_range
```

Add this in `add_derived_features()` alongside the existing
derived features (equity_margin, spr).

### Why

`hero_range_percentile` is preflop-only — it measures where
the hand sits in the opening range regardless of board. On
Qs5s7s:
- A4d: HRP 0.96 × equity 0.30 = **0.29** (bottom third)
- A4s: HRP 0.96 × equity 0.85 = **0.82** (top of range)

Same preflop hand, different postflop reality. The derived
feature collapses HRP when the board didn't connect.

### Feature vector impact

This adds column 55 to the raw features (54 → 55). The
attn_* mirror adds column 110 (108 → 110). Total feature
count: 110.

**All downstream consumers must update:**
- `FEATURE_COLUMNS` list in `gto_model.py`
- `train_model_v2_2.py` (column count assertion)
- `evaluate_v2_2.py` (feature vector assembly)
- Any test that asserts feature count
- Assembly scripts that build training CSVs

This is a feature-vector contract change. Test-first:
write a test that asserts `board_adjusted_hrp` exists in
the output of `extract_all_features()` and equals
`hrp * equity_vs_range` within float tolerance.

### Do NOT remove original HRP

Keep `hero_range_percentile` in the feature vector. The
model can learn to use both — original HRP carries preflop
context (useful for preflop-aggressor reads), board-adjusted
carries postflop reality. XGBoost will learn the relative
importance.

## Layer 2 — Targeted label cleanup

### Step 1 — Override audit (30 min)

Query Phase 4 labels + pilot labels for all hands where
`override_clause_fired = true`.

Report per hand: situation_id, consensus_action, is_made_hand,
draw_outs, equity_vs_range, worse_hand_pct, hand_bucket,
hero_range_percentile, is_monotone, danger_score, Pass 1
vote split.

Deliverable: `review/comms/OVERRIDE_AUDIT_2026-04-18.md`

### Step 2 — Classify

**CLEAN** — keep label as-is:
- is_made_hand=1 OR draw_outs >= 4
- equity_vs_range >= 0.40
- worse_hand_pct >= 0.55
- BET is defensible on poker merits without the override

**SUSPECT** — re-label with v3.1 prompt:
- is_made_hand=0 AND draw_outs < 4
- equity_vs_range < 0.35 OR worse_hand_pct < 0.50
- OR is_monotone=1 with hero not holding board suit
- OR hand_bucket = air

**BORDERLINE** — flag for manual review.

### Step 3 — Create v3.1 prompt

v3 minus:
- Stream B.2 override clause (lines 294-383)
- §3.A (DO NOT Rule 10)
- §3.C (Step 3 enhancement)
- §3.D (Calibration notes)
- `override_clause_fired` output field

Keep: §3.B (HRP warning), Oracle's Read headers, draw-type
specificity, all v2 content.

### Step 4 — Re-label SUSPECT hands only

Run SUSPECT hands through v3.1 prompt pipeline (4 panels +
Pass 2). Keep whatever labels come back — honest labels.

### Step 5 — Reassemble training CSV

All sources:
- v2.2 base (385 rows) — re-extract with new feature
  (`board_adjusted_hrp` added)
- Section 1 supplement with cleaned labels — re-extract
- CALL supplement (25 rows) — re-extract
- New feature column present on all rows

The CSV must be re-extracted (not just patched) because
the feature vector changed (55 raw + 55 attn = 110).

Preflight must pass clean.

### Step 6 — Retrain + evaluate

Standard XGBoost config. No class weighting. Save as
`v2_3_1_model.json`.

Evaluate on:
- FB-40 ≥ 70%
- MW-50 ≥ 82% (recalibrated)
- Group D ≤ 1 regression
- Reversals: no new regressions
- **NEW: A4d on Qs5s7s must predict CHECK** (the specific
  hand that exposed the problem)

### Step 7 — Self-play diagnostic (if time)

If the self-play diagnostic from update-c hasn't run yet,
run it with the v2.3.1 model instead of v2.3. The board-
adjusted HRP may also improve self-play dynamics (model
less likely to bluff with air on hostile boards → more
realistic game flow).

## Sequencing

1. Add `board_adjusted_hrp` to feature extractor + tests
2. Override audit (can run in parallel with 1)
3. Create v3.1 prompt
4. Re-label SUSPECT hands
5. Re-extract all training data with new feature
6. Assemble + train + evaluate

Steps 1-3 are parallel. Steps 4-6 are sequential.
Estimated total: ~3-4 hours.

## Game builder — unchanged

Stay on v2.2 model for playtest. When v2.3.1 ships, swap
adapter path. The adapter will need to handle the new
feature column (110 features instead of 108) — flag this
in the adapter update.

## Teaching terminal — unchanged

Content API is stable. The `board_adjusted_hrp` value will
be available in `full_feature_vector` for templates to use
if desired. No template changes required — teaching already
shows "Air — no made hand — 3% equity" which is correct.
