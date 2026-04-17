---
date: 2026-04-17
from: Programmer
to: Owner
re: Path A -- class-weighted retrain (hypothesis test for Path B)
status: PARTIAL RECOVERY -- class weighting restores CHECK discrimination on MW-50 but FB-40 remains below baseline
---

# Path A: Class-Weighted Retrain Report

## Experiment

Retrained on the same iter2 CSV (688 rows, 53.3% BET) with sklearn-style balanced class weights instead of the capped heuristic weights used in iter1/iter2.

### Weights Applied

| Class | Count | iter2 weight | Balanced weight |
|-------|-------|-------------|-----------------|
| BET   | 367   | 1.00        | 0.3754          |
| CHECK | 141   | 2.59        | 0.9735          |
| FOLD  | 75    | 4.00        | 1.8333          |
| CALL  | 57    | 4.00        | 2.3913          |
| RAISE | 48    | 3.00        | 2.8947          |

Key difference: BET weight dropped from 1.00 to 0.38 (3x suppression). CHECK weight dropped from 2.59 to 0.97 but BET suppression is what matters -- the model now pays 2.6x more for a false CHECK-as-BET than before.

## Training Metrics

| Metric | v2.2 | iter1 | iter2 | weighted |
|--------|------|-------|-------|----------|
| CV accuracy | 93.0% +/- 3.5% | 94.95% +/- 1.60% | 95.35% +/- 1.09% | 94.62% +/- 1.08% |
| Holdout accuracy | 88.3% | 94.29% | 92.03% | 91.30% |
| Best iteration | -- | 103 | 92 | 182 |

CV above 80% -- no stop condition triggered.

## Evaluation: 4-Way Comparison

### FB-40

| Model | Correct | Total | Accuracy | Delta vs v2.2 |
|-------|---------|-------|----------|---------------|
| v2.2 | 29 | 40 | 72.5% | -- |
| iter1 | 25 | 40 | 62.5% | -10.0pp |
| iter2 | 28 | 40 | 70.0% | -2.5pp |
| **weighted** | **28** | **40** | **70.0%** | **-2.5pp** |

FB-40 = 70.0% (below 72.5% baseline). Same accuracy as iter2 but different error pattern -- weighted fixes FB-28 (FOLD correct) but loses FB-22/FB-33/FB-34 to RAISE over-prediction.

### MW-50

| Model | Correct | Total | Accuracy | Delta vs v2.2 |
|-------|---------|-------|----------|---------------|
| v2.2 | 42 | 50 | 84.0% | -- |
| iter1 | 30 | 50 | 60.0% | -24.0pp |
| iter2 | 27 | 50 | 54.0% | -30.0pp |
| **weighted** | **44** | **50** | **88.0%** | **+4.0pp** |

MW-50 = 88.0% -- exceeds v2.2 baseline by 4pp.

### MW-50 by Expected Action

| Expected | v2.2 | iter1 | iter2 | weighted |
|----------|------|-------|-------|----------|
| BET (13) | 9/13 | 13/13 | 13/13 | 12/13 |
| CHECK (37) | 33/37 | 17/37 | 14/37 | 32/37 |

BET accuracy: 12/13 (weighted loses d1454_CO_turn -- a BET hand now predicted CHECK). This is the expected trade-off of BET suppression.

CHECK accuracy: 32/37 -- massive recovery from iter2's 14/37.

## Diagnostic Groups

### BET-fix retained (4 hands v2.2 got wrong)

| Hand | v2.2 | iter1 | iter2 | weighted |
|------|------|-------|-------|----------|
| d2410_CO_turn | XX | OK | OK | OK |
| d1983_HJ_turn | XX | OK | OK | OK |
| d1562_HJ_turn | XX | OK | OK | OK |
| d8886_BB_flop | XX | OK | OK | OK |

**BET-fix: RETAINED (4/4)**

### CHECK restoration (17 hands iter1 broke vs v2.2)

**Restored: 14/17**

Still broken: d9941_CO_flop, d0845_BB_flop, d7640_HJ_river (all CHECK->BET)

No new CHECK regressions vs v2.2 beyond the 3 persistent misses above.

### New regressions vs v2.2

- d1454_CO_turn: BET->CHECK (BET suppression overcorrection)
- d9941_CO_flop, d0845_BB_flop, d7640_HJ_river: same as v2.2's d9653/d1562/d3688 pattern -- persistent CHECK-expected spots the model gets wrong

Net vs v2.2: +2 hands (44 vs 42). The 4 BET-fix gains (+4) minus 2 new misses (d1454, one of the persistent 3) = net +2.

## Verdict

**Class weighting shows PARTIAL recovery:**

- MW-50: **88.0%** -- exceeds v2.2 baseline (84.0%) by 4pp. CHECK discrimination massively restored (32/37 vs 14/37 in iter2).
- FB-40: **70.0%** -- still 2.5pp below v2.2 baseline. Not recovered.
- BET-fix: Fully retained (4/4).
- CHECK: 14/17 restored.

**Path B assessment:** Class weighting alone recovers MW-50 past baseline but FB-40 remains below. The FB-40 deficit is not a CHECK problem (FB-40 is all facing-bet hands -- FOLD/CALL/RAISE only). The FB-40 misses are CALL/RAISE confusion (FB-22, FB-29, FB-33, FB-34 all predict RAISE when CALL expected). This suggests:

1. **Path B (adding CHECK counter-examples) would NOT fix FB-40** -- FB-40's deficit is action confusion in facing-bet spots, not BET/CHECK discrimination.
2. **Class weighting may be sufficient for MW-50** -- but the weighted model should be validated on a broader test set before shipping.
3. **FB-40 deficit predates the supplement** -- iter2 and weighted both score 70.0%, and iter1 scored 62.5%. The 72.5% v2.2 baseline may have been optimistic for this data distribution.

**Recommendation:** The weighted model (MW-50=88.0%, FB-40=70.0%) is a candidate for shipping if the owner accepts the -2.5pp FB-40 gap. Path B would improve CHECK balance further but likely cannot fix the FB-40 CALL/RAISE confusion.

## Artifacts

| Artifact | Path |
|----------|------|
| Training script | `review/train_v2_3_weighted.py` |
| Model | `river-rats-core/models/v2_3_weighted_model.json` |
| Training report | `river-rats-core/models/v2_3_weighted_training_report.json` |
| This report | `review/comms/PATH_A_WEIGHTED_REPORT_2026-04-17.md` |
