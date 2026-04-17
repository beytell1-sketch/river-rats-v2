---
date: 2026-04-17
from: Programmer
to: Owner
re: v2.3 iter2 execution report -- STOP triggered
status: STOP -- MW-50 regression (54.0% vs 84.0% baseline), FB-40 regression (70.0% vs 72.5% baseline), CHECK discrimination NOT restored
---

# v2.3 iter2 Report

## Phase 5: Assembly

- **Row count**: 688 (385 v2.2 re-encoded + 287 pass1-filtered + 16 pilot)
  - Pass1 breakdown: 80 pruned UMBRELLA + 207 non-UMBRELLA
  - Note: task estimated ~699 assuming 3 curated hands were separate; d5620 and d1983 are already in pass1, BP7_06 is already in pilot. No double-counting.
- **Schema preflight**: PASS (zero string-encoded values, no `--allow-mixed-encoding`)
- **Output**: `training-data/v2_3_iter2_training.csv`

### Pruning method

UMBRELLA 268 → 80 by Euclidean distance from centroid of 6 bias-signature features (`worse_hand_pct`, `equity_vs_range`, `hero_range_percentile`, `spr`, `villain_checked_back`, `villain_range_capped`). Max distance in kept set: 0.1465. One hand (UMBRELLA_268) was in the fill file but not in pass1_final_labels; replaced with next-closest.

### Action distribution

| Action | v2.2 (385) | iter1 (871) | iter2 (688) |
|--------|-----------|-------------|-------------|
| BET    | 99 (25.7%) | 547 (62.8%) | 367 (53.3%) |
| CHECK  | 131 (34.0%) | 144 (16.5%) | 141 (20.5%) |
| CALL   | 57 (14.8%) | 57 (6.5%) | 57 (8.3%) |
| FOLD   | 75 (19.5%) | 75 (8.6%) | 75 (10.9%) |
| RAISE  | 23 (6.0%) | 48 (5.5%) | 48 (7.0%) |

BET% dropped from 62.8% (iter1) to 53.3% (iter2). Target was 50-55%. Within range.

---

## Phase 6: Training

| Metric | v2.2 | iter1 | iter2 |
|--------|------|-------|-------|
| CV accuracy | 93.0% ± 3.5% | 94.95% ± 1.60% | 95.35% ± 1.09% |
| Holdout accuracy | 88.3% | 94.29% | 92.03% |
| Best iteration | -- | 103 | 92 |
| Training rows | 385 | 871 | 688 |

Model saved: `river-rats-core/models/v2_3_iter2_model.json`

Class weights: BET=1.0, CHECK=2.59, FOLD=4.0, CALL=4.0, RAISE=3.0

---

## Phase 7: Evaluation -- STOP

### FB-40

| Model | Correct | Total | Accuracy |
|-------|---------|-------|----------|
| v2.2 | 29 | 40 | 72.5% |
| iter1 | 25 | 40 | 62.5% |
| **iter2** | **28** | **40** | **70.0%** |

**STOP: FB-40 = 70.0% < 72.5% threshold (-2.5pp vs v2.2)**

iter2 recovers 3 hands vs iter1 but still 1 hand below v2.2 baseline.

### MW-50

| Model | Correct | Total | Accuracy |
|-------|---------|-------|----------|
| v2.2 | 42 | 50 | 84.0% |
| iter1 | 30 | 50 | 60.0% |
| **iter2** | **27** | **50** | **54.0%** |

**STOP: MW-50 = 54.0% < 84.0% threshold (-30.0pp vs v2.2)**

iter2 is WORSE than iter1 on MW-50 by 3 hands despite better BET balance.

### MW-50 by expected action

| Expected | v2.2 | iter1 | iter2 |
|----------|------|-------|-------|
| BET (13) | 9/13 | 13/13 | 13/13 |
| CHECK (37) | 33/37 | 17/37 | 14/37 |

BET-expected: perfect (13/13) across both iters. But CHECK discrimination is WORSE in iter2 (14/37) than iter1 (17/37). The pruning made CHECK accuracy worse, not better.

---

## 3-Way Per-Hand Comparison: FB-40

| hand_id | expected | v2.2 | iter1 | iter2 | v2.2 | iter1 | iter2 |
|---------|----------|------|-------|-------|------|-------|-------|
| FB-01 | FOLD | CALL | CALL | CALL | XX | XX | XX |
| FB-02 | CALL | CALL | CALL | CALL | OK | OK | OK |
| FB-03 | FOLD | FOLD | FOLD | FOLD | OK | OK | OK |
| FB-04 | RAISE | CALL | CALL | CALL | XX | XX | XX |
| FB-05 | CALL | CALL | CALL | CALL | OK | OK | OK |
| FB-06 | CALL | CALL | CALL | CALL | OK | OK | OK |
| FB-07 | FOLD | CALL | CALL | CALL | XX | XX | XX |
| FB-08 | CALL | CALL | RAISE | CALL | OK | XX | OK |
| FB-09 | CALL | CALL | CALL | CALL | OK | OK | OK |
| FB-10 | RAISE | RAISE | RAISE | RAISE | OK | OK | OK |
| FB-11 | FOLD | FOLD | FOLD | FOLD | OK | OK | OK |
| FB-12 | CALL | CALL | CALL | CALL | OK | OK | OK |
| FB-13 | FOLD | FOLD | FOLD | FOLD | OK | OK | OK |
| FB-14 | RAISE | CALL | CALL | CALL | XX | XX | XX |
| FB-15 | FOLD | CALL | CALL | CALL | XX | XX | XX |
| FB-16 | FOLD | CALL | RAISE | RAISE | XX | XX | XX |
| FB-17 | CALL | CALL | RAISE | CALL | OK | XX | OK |
| FB-18 | FOLD | FOLD | FOLD | FOLD | OK | OK | OK |
| FB-19 | FOLD | FOLD | FOLD | FOLD | OK | OK | OK |
| FB-20 | CALL | CALL | CALL | CALL | OK | OK | OK |
| FB-21 | RAISE | RAISE | RAISE | RAISE | OK | OK | OK |
| FB-22 | CALL | CALL | RAISE | RAISE | OK | XX | XX |
| FB-23 | FOLD | FOLD | FOLD | FOLD | OK | OK | OK |
| FB-24 | RAISE | CALL | RAISE | RAISE | XX | OK | OK |
| FB-25 | CALL | CALL | CALL | CALL | OK | OK | OK |
| FB-26 | RAISE | RAISE | RAISE | RAISE | OK | OK | OK |
| FB-27 | CALL | CALL | CALL | CALL | OK | OK | OK |
| FB-28 | FOLD | CALL | RAISE | FOLD | XX | XX | OK |
| FB-29 | CALL | CALL | CALL | RAISE | OK | OK | XX |
| FB-30 | RAISE | FOLD | FOLD | CALL | XX | XX | XX |
| FB-31 | FOLD | FOLD | FOLD | FOLD | OK | OK | OK |
| FB-32 | FOLD | FOLD | FOLD | FOLD | OK | OK | OK |
| FB-33 | CALL | CALL | RAISE | RAISE | OK | XX | XX |
| FB-34 | CALL | CALL | RAISE | RAISE | OK | XX | XX |
| FB-35 | CALL | FOLD | FOLD | FOLD | XX | XX | XX |
| FB-36 | RAISE | RAISE | RAISE | RAISE | OK | OK | OK |
| FB-37 | CALL | CALL | RAISE | CALL | OK | XX | OK |
| FB-38 | FOLD | FOLD | FOLD | FOLD | OK | OK | OK |
| FB-39 | RAISE | RAISE | RAISE | RAISE | OK | OK | OK |
| FB-40 | FOLD | CALL | FOLD | FOLD | XX | OK | OK |

**FB-40 movement**: iter2 gained FB-08, FB-17, FB-28, FB-37, FB-40 vs iter1 (+5), lost FB-22, FB-29, FB-33, FB-34 vs v2.2 (-4 new misses). Net: +3 vs iter1, -1 vs v2.2.

---

## 3-Way Per-Hand Comparison: MW-50

| hand_id | expected | v2.2 | iter1 | iter2 | v2.2 | iter1 | iter2 |
|---------|----------|------|-------|-------|------|-------|-------|
| d5066_BB_flop | CHECK | CHECK | BET | BET | OK | XX | XX |
| d4798_HJ_flop | CHECK | CHECK | CHECK | BET | OK | OK | XX |
| d2410_CO_turn | BET | CHECK | BET | BET | XX | OK | OK |
| d8007_BB_flop | CHECK | CHECK | BET | BET | OK | XX | XX |
| d2205_BB_river | CHECK | CHECK | CHECK | BET | OK | OK | XX |
| d2920_BB_turn | BET | BET | BET | BET | OK | OK | OK |
| d3178_CO_river | BET | BET | BET | BET | OK | OK | OK |
| d1983_HJ_turn | BET | CHECK | BET | BET | XX | OK | OK |
| d1562_HJ_turn | BET | CHECK | BET | BET | XX | OK | OK |
| d3178_BTN_river | CHECK | CHECK | BET | BET | OK | XX | XX |
| d9941_CO_flop | CHECK | CHECK | BET | BET | OK | XX | XX |
| d4798_BB_turn | CHECK | CHECK | CHECK | CHECK | OK | OK | OK |
| d7345_BTN_turn | CHECK | CHECK | CHECK | CHECK | OK | OK | OK |
| d9418_BB_flop | CHECK | CHECK | BET | CHECK | OK | XX | OK |
| d9518_BTN_river | CHECK | CHECK | CHECK | CHECK | OK | OK | OK |
| d7361_BB_flop | CHECK | CHECK | BET | BET | OK | XX | XX |
| d1562_BTN_turn | CHECK | CHECK | CHECK | CHECK | OK | OK | OK |
| d8411_BB_turn | BET | BET | BET | BET | OK | OK | OK |
| d6522_BB_river | CHECK | CHECK | CHECK | CHECK | OK | OK | OK |
| d5312_HJ_flop | CHECK | CHECK | BET | BET | OK | XX | XX |
| d9653_BB_river | CHECK | BET | BET | BET | XX | XX | XX |
| d8137_CO_flop | CHECK | CHECK | CHECK | BET | OK | OK | XX |
| d7964_BTN_turn | CHECK | CHECK | CHECK | CHECK | OK | OK | OK |
| d2788_BB_turn | CHECK | CHECK | CHECK | CHECK | OK | OK | OK |
| d4781_CO_flop | BET | BET | BET | BET | OK | OK | OK |
| d4809_BB_turn | CHECK | BET | CHECK | BET | XX | OK | XX |
| d9418_BTN_flop | CHECK | CHECK | CHECK | CHECK | OK | OK | OK |
| d2788_BTN_flop | BET | BET | BET | BET | OK | OK | OK |
| d2079_BB_turn | CHECK | CHECK | CHECK | CHECK | OK | OK | OK |
| d6035_HJ_turn | CHECK | CHECK | BET | BET | OK | XX | XX |
| d8886_BB_flop | BET | CHECK | BET | BET | XX | OK | OK |
| d7695_BTN_river | CHECK | CHECK | BET | BET | OK | XX | XX |
| d4312_BTN_flop | CHECK | CHECK | BET | BET | OK | XX | XX |
| d1454_CO_turn | BET | BET | BET | BET | OK | OK | OK |
| d9653_CO_river | CHECK | CHECK | BET | BET | OK | XX | XX |
| d7345_HJ_river | CHECK | CHECK | BET | BET | OK | XX | XX |
| d9208_BTN_flop | CHECK | CHECK | BET | BET | OK | XX | XX |
| d1562_HJ_river | CHECK | BET | BET | BET | XX | XX | XX |
| d6342_BTN_flop | CHECK | CHECK | BET | BET | OK | XX | XX |
| d3688_BB_flop | CHECK | BET | BET | BET | XX | XX | XX |
| d5066_BTN_turn | BET | BET | BET | BET | OK | OK | OK |
| d0845_BB_flop | CHECK | CHECK | BET | BET | OK | XX | XX |
| d3229_BTN_river | BET | BET | BET | BET | OK | OK | OK |
| d7640_HJ_river | CHECK | CHECK | BET | BET | OK | XX | XX |
| d0182_BTN_turn | BET | BET | BET | BET | OK | OK | OK |
| d5312_BTN_turn | CHECK | CHECK | CHECK | CHECK | OK | OK | OK |
| d2410_BB_turn | CHECK | CHECK | BET | BET | OK | XX | XX |
| d4534_BTN_river | CHECK | CHECK | CHECK | CHECK | OK | OK | OK |
| d7345_BB_river | CHECK | CHECK | CHECK | CHECK | OK | OK | OK |
| d1262_BB_river | CHECK | CHECK | CHECK | CHECK | OK | OK | OK |

---

## Diagnostic Groups

### BET-miss correction (Stream B.2 — 4 hands v2.2 got wrong)

| Hand | v2.2 | iter1 | iter2 |
|------|------|-------|-------|
| d2410_CO_turn | XX | OK | OK |
| d1983_HJ_turn | XX | OK | OK |
| d1562_HJ_turn | XX | OK | OK |
| d8886_BB_flop | XX | OK | OK |

**BET-fix signal: RETAINED (4/4)**

### CHECK discrimination (17 hands iter1 broke vs v2.2)

Of 17 CHECK-expected hands that iter1 broke (v2.2 correct → iter1 wrong):
- **Restored in iter2: 1/17** (only d9418_BB_flop)
- **Still broken: 16/17**
- iter2 ADDED 2 new CHECK regressions vs v2.2: d4798_HJ_flop, d2205_BB_river
- iter2 ADDED 1 new CHECK regression vs iter1: d8137_CO_flop (iter1 had it right)
- iter2 REGRESSED d4809_BB_turn (v2.2 wrong, iter1 fixed, iter2 wrong again)

**CHECK restoration: FAILED (1/17)**

### Group D (reversal hands)

| Hand | Expected | v2.2 | iter1 | iter2 |
|------|----------|------|-------|-------|
| d3688_BB_flop | CHECK | BET | BET | BET |
| d4312_BTN_flop | CHECK | CHECK | BET | BET |

d4312_BTN_flop: regression vs v2.2 persists in iter2.
d3688_BB_flop: was already wrong in v2.2 — no regression.

**Group D regression: 1 hand (d4312_BTN_flop) -- BORDERLINE (threshold: >1)**

### Groups A+B (BET-expected proxy on MW-50)

BET-expected hands (13): iter2 = 13/13 = 100% (≥70% absolute -- PASS)
Improvement: +4 hands vs v2.2 = +30.8pp (≥5pp -- PASS)

Same caveat as iter1: this "improvement" is achieved by over-predicting BET.

---

## Ship Gate Summary

| Criterion | Result | Status |
|-----------|--------|--------|
| Row count within 5% | 688 (vs ~699 est = -1.6%) | PASS |
| Schema preflight clean | Clean | PASS |
| BET% in target range | 53.3% (target 50-55%) | PASS |
| CV ≥ 80% | 95.35% ± 1.09% | PASS |
| Holdout ≥ 80% | 92.03% | PASS |
| FB-40 ≥ 72.5% | **70.0%** | **FAIL -- STOP** |
| MW-50 ≥ 84.0% | **54.0%** | **FAIL -- STOP** |
| Groups A+B ≥ 70% | 100% (proxy) | PASS |
| Groups A+B ≥ +5pp vs v2.2 | +30.8pp | PASS |
| Group D regression ≤1 | 1 (d4312) | BORDERLINE |
| BET-fix signal retained | 4/4 | PASS |
| CHECK discrimination restored | **1/17** | **FAIL** |

**Overall: STOP. v2.3 iter2 model is not shippable.**

---

## Root Cause Analysis

Pruning UMBRELLA from 268 → 80 reduced the BET label volume (547 → 367) and improved BET% from 62.8% to 53.3%. However:

1. **CHECK discrimination is WORSE than iter1**, not better (14/37 vs 17/37 on MW-50 CHECK hands). The model still overwhelmingly predicts BET on multiway CHECK-expected spots.

2. **The UMBRELLA hands were all BET-labelled in pass1** (257 BET + 6 CHECK out of 263). Removing 183 of them removes BET labels but does NOT add CHECK signal. The remaining non-UMBRELLA Phase 4 hands are also 86% BET (178/207).

3. **The fundamental problem is not UMBRELLA volume -- it's the Phase 4 supplement composition.** 435/470 Phase 4 hands (92.5%) are BET-labelled. Pruning UMBRELLA changes the ratio but the Phase 4 component is still 92% BET. The model learns "multiway checked-to = BET" from the supplement regardless of UMBRELLA count.

4. **New regressions**: iter2 broke 2 additional CHECK hands that even iter1 got right (d4798_HJ_flop, d2205_BB_river, d8137_CO_flop). This suggests the pruning may have removed some edge-case UMBRELLA hands that were providing useful CHECK-adjacent signal.

### Recommended next step

The UMBRELLA pruning strategy does not work because the problem is not UMBRELLA-specific -- it's the entire Phase 4 supplement being 92.5% BET. To restore CHECK discrimination:

1. **Add CHECK-labelled multiway hands** to the supplement (target ~100-150 CHECK hands to bring BET% below 45%)
2. **OR stratified sub-sampling**: downsample the Phase 4 BET hands to ~120 (from 435) while keeping all 12 CHECK + 23 RAISE hands
3. **OR aggressive class weighting**: BET weight 0.3x, CHECK weight 6.0x (current CHECK weight 2.59x is insufficient)

---

## Artifacts

| Artifact | Path |
|----------|------|
| Pruned UMBRELLA | `training-data/v23_umbrella_fill_pruned_80.jsonl` |
| iter2 training CSV | `training-data/v2_3_iter2_training.csv` |
| iter2 model | `river-rats-core/models/v2_3_iter2_model.json` |
| This report | `review/comms/PHASE_567_ITER2_REPORT_2026-04-17.md` |
