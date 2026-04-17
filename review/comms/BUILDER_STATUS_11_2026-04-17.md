---
date: 2026-04-17
from: Builder
to: Main terminal / Owner
re: Option A capped FAILED — weight redistribution problem; need a different approach
status: BLOCKED — class weighting cannot be tuned to pass all gates simultaneously
---

# Builder Status #11 — Option A Capped Results

## Result — FAIL

| # | Criterion | Weighted (2.89×) | Capped (1.50×) |
|---|---|---|---|
| 1 | FB-40 ≥70% | 70.0% PASS | **75.0% PASS** |
| 2 | MW-50 ≥82.5% | 88.0% PASS | **74.0% FAIL** |
| 4 | Group D ≤1 | 0 PASS | 1 PASS |
| 5 | Reversals 100% | 7/10 FAIL | **5/10 FAIL** |

Capping RAISE fixed FB-40 (+5pp) but **collapsed MW-50** from 88%
to 74%. Calibration reversals got worse (7/10 → 5/10). MW-30 still
RAISE.

## Root cause — weight redistribution

XGBoost's softmax redistributes probability mass globally across
all 5 classes. Capping RAISE weight didn't redirect mass to CALL —
it redirected to BET (the dominant class). This re-introduced the
BET over-prediction that iter1/iter2 had.

**The fundamental issue:** class weighting is a global knob. We
need to fix CALL/RAISE discrimination in facing-bet spots WITHOUT
breaking BET/CHECK discrimination in checked-to spots. A single
set of class weights cannot do both — tuning in one direction
regresses the other.

## Where we are

| Configuration | FB-40 | MW-50 | Reversals | Shippable? |
|---|---|---|---|---|
| v2.2 (baseline) | 72.5% | 84.0% | — | ✅ shipped |
| iter1 (full UMB) | 62.5% | 60.0% | — | ❌ |
| iter2 (pruned UMB) | 70.0% | 54.0% | — | ❌ |
| weighted (RAISE 2.89) | 70.0% | **88.0%** | 7/10 | ❌ reversal |
| capped (RAISE 1.50) | **75.0%** | 74.0% | 5/10 | ❌ both |

The weighted model at RAISE=2.89 had the best MW-50 (88%) but
failed on reversals. Capping RAISE lost MW-50 without fixing
reversals. There is no class-weight configuration that passes
all gates simultaneously on this data.

## What would actually fix this

The problem is that BET/CHECK and CALL/RAISE operate in completely
different feature subspaces (checked-to vs facing-bet), but class
weighting treats them as a single global distribution.

### Option 1 — Situation-aware weighting
Weight by situation type, not class. Facing-bet rows get higher
CALL weight; checked-to rows get lower BET weight. Requires a
custom `sample_weight` vector, not sklearn's `balanced` formula.

### Option 2 — Binary decomposition
Train two models: one for checked-to spots (BET vs CHECK), one for
facing-bet spots (CALL vs RAISE vs FOLD). The oracle router picks
which model to invoke based on `facing_bet`. This separates the
two discrimination problems entirely.

### Option 3 — Targeted CALL/RAISE supplement (20-30 hands)
Add facing-bet CALL hands to the training data — the supplement
was almost 100% BET/RAISE, with near-zero CALL. Adding 20-30
explicit CALL examples at the right feature shape fixes the
CALL/RAISE confusion without affecting BET/CHECK at all.

### Option 4 — Return to v2.2 + targeted BET supplement only
Keep v2.2's 385 rows as base. Add ONLY the Section 1 rows 1-12
(targeted BET supplement, ~215 hands) WITHOUT the UMBRELLA bucket.
No class weighting. The UMBRELLA was the source of BET flood; the
targeted rows are more concentrated and less likely to overwhelm.

**Builder recommendation:** Option 3 (fastest, most targeted — 
adds the missing CALL signal without touching the working BET/CHECK
fix) OR Option 4 (cleanest — avoids the weight-tuning trap entirely
by using a smaller, focused supplement).

## Awaiting

Owner direction on Options 1-4. The weight-tuning approach has hit
a wall — the next step is either data composition or model
architecture, not another weight experiment.
