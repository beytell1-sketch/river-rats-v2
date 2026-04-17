---
date: 2026-04-17
from: Builder
to: Main terminal / Owner
re: STOP — v2.3 iter2 also fails (UMBRELLA pruning insufficient)
status: BLOCKED — root cause is supplement design, not volume
---

# Builder Status #9 — iter2 STOP

## Results

| Metric | v2.2 | iter1 (268 UMB) | iter2 (80 UMB) |
|---|---|---|---|
| Training rows | 385 | 871 | 688 |
| BET% | 25.7% | 62.8% | 53.3% |
| CV | 93.0% ±3.5% | 94.95% ±1.60% | 95.35% ±1.09% |
| Holdout | 88.3% | 94.29% | 92.03% |
| **FB-40** | **72.5%** | **62.5%** | **70.0%** |
| **MW-50** | **84.0%** | **60.0%** | **54.0%** |

**Both test sets still below v2.2. iter2 is worse than iter1 on MW-50.**

## What happened

Pruning UMBRELLA from 268→80 moved BET% from 62.8%→53.3% (in target
range). But:

- **MW-50 CHECK hands:** 33/37 (v2.2) → 17/37 (iter1) → **14/37 (iter2)**
  — CHECK discrimination got WORSE, not better
- **MW-50 BET hands:** 9/13 (v2.2) → 13/13 (iter1) → 13/13 (iter2)
  — BET fix retained
- **BET-miss correction retained:** YES (4/4 target misses still correct)
- **CHECK restoration:** NO (1/17 of iter1-broken hands restored)

## Root cause — clear now

UMBRELLA pruning cannot fix the bias because:

1. **The entire Phase 4 supplement is 92.5% BET** (435/470 hands).
   Reducing UMBRELLA volume reduces BET count but doesn't add any
   CHECK signal.
2. Even at 53.3% BET, the model learns "multiway checked-to = BET"
   because the supplement is overwhelmingly BET in the precondition
   shape. No CHECK-labelled hands exist to teach the model WHERE to
   stop betting.
3. CV/holdout look great because they're drawn from the same
   BET-dominated distribution. The test sets (FB-40, MW-50) are
   balanced → model can't generalise.

**This is a supplement DESIGN issue, not a volume issue.** Option 3
(pruning) was the wrong lever. Options 1 or 2 from Builder Status #8
address the actual root cause.

## What would fix it

The model needs **CHECK-labelled multiway hands in the bias-signature
shape** so it learns the decision boundary, not just one side of it.

Two viable paths:

### Path A — class weighting (fast, ~30 min)
Apply `scale_pos_weight` or per-sample weights in XGBoost to
down-weight the BET-heavy supplement during training. Same data,
different emphasis. Verify the model recovers CHECK discrimination
without losing BET-fix signal.

**Pros:** No new labelling. Fast iteration.
**Cons:** Less interpretable. Harder to tune weights precisely.

### Path B — balanced supplementation (slower, ~2-4 hours)
Add ~100-150 CHECK-labelled hands in the same precondition shape
(multiway, checked-to, capped villain, low SPR) where CHECK is
GTO-correct. Source from v2.2's existing CHECK-labelled hands in
the near-bias bucket (Stream C found 24 rows with 79.2% BET / 20.8%
CHECK — the 5 CHECK rows are a starting point but not enough).

**Pros:** Clean training signal. Interpretable. Stable.
**Cons:** Requires sourcing + labelling more hands (but could use
curated-from-existing-pool approach).

### Builder recommendation

**Path A first** (30 min, validates the hypothesis). If class
weighting recovers FB-40 + MW-50, we know the model CAN learn the
boundary from this data — then commit to Path B for the production
fix (clean signal > weight hacks).

If class weighting doesn't recover, the supplement composition is
fundamentally wrong and we need Path B regardless.

## Commits

- `9769aa9` — pruned UMBRELLA + reassembled CSV
- `56a121f` — iter2 model trained
- `f40bea5` — iter2 eval report (STOP)

## Awaiting

Owner direction: Path A (class weighting, fast) / Path B (balanced
supplementation, slower) / hybrid / other.

Standing by.
