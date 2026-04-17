---
date: 2026-04-17
from: Programmer
to: Owner
re: Option A -- RAISE weight capped at 1.50
status: STOPPED -- MW-50 collapsed to 74.0%, MW-30 still RAISE
---

# Option A: RAISE Weight Capped at 1.50

## Weights Table

| Class | Count | Old weight (balanced) | New weight (capped) |
|-------|-------|----------------------|---------------------|
| BET   | 367   | 0.3754               | 0.3754              |
| CHECK | 141   | 0.9735               | 0.9735              |
| FOLD  | 75    | 1.8333               | 1.8333              |
| CALL  | 57    | 2.3913               | 2.3913              |
| RAISE | 48    | 2.8947               | **1.5000**          |

## Training Metrics

| Metric | v2.2 | iter1 | iter2 | weighted | capped |
|--------|------|-------|-------|----------|--------|
| CV accuracy | 93.0% +/- 3.5% | 94.95% +/- 1.60% | 95.35% +/- 1.09% | 94.62% +/- 1.08% | **95.06% +/- 0.72%** |
| Holdout accuracy | 88.3% | 94.29% | 92.03% | 91.30% | **91.30%** |
| Best iteration | -- | 103 | 92 | 182 | **113** |

CV = 95.06% (above 85% stop condition). Model is not degenerate by CV.

## Full 5-Criterion Gate Table

| # | Criterion | Target | Actual | PASS/FAIL |
|---|-----------|--------|--------|-----------|
| 1 | FB-40 accuracy | >=70.0% | **75.0%** (30/40) | **PASS** |
| 2 | MW-50 accuracy | >=82.5% | **74.0%** (37/50) | **FAIL** |
| 3 | Groups A+B | >=70% abs + 5pp over v2.2 | N/A -- diagnostic hands never sourced | **BLOCKED** |
| 4 | Group D regression | <=1 hand vs v2.2 | **1 hand** (d9556 regressed CHECK->BET) | **PASS** (at limit) |
| 5 | Calibration reversals | 100% on all reversal hands | **5/10** (50%) | **FAIL** |
| 6 | Solver 8 MW | PENDING (owner-led) | -- | **PENDING** |

**STOPPED: Criterion 2 FAIL (MW-50 = 74.0% < 84.0% stop threshold).**

## FB-40 Per-Hand Recovery (4 Prior Misses from Path A)

| Hand | Expected | v2.2 | weighted | capped | Recovery? |
|------|----------|------|----------|--------|-----------|
| FB-22 | CALL | CALL (OK) | RAISE (XX) | **RAISE (XX)** | No |
| FB-29 | CALL | CALL (OK) | RAISE (XX) | **CALL (OK)** | **YES** |
| FB-33 | CALL | CALL (OK) | RAISE (XX) | **RAISE (XX)** | No |
| FB-34 | CALL | CALL (OK) | RAISE (XX) | **RAISE (XX)** | No |

**Recovery: 1/4.** FB-29 restored to CALL. FB-22/33/34 remain RAISE-overpredicted. FB-40 improved to 75.0% (from 70.0% weighted) via other recoveries (FB-07, FB-35 restored).

## MW-30 Reversal Status

**MW-30: STILL RAISE (XX).** Predicted RAISE at 65.8% masked probability (was 69.6% in weighted). Cap reduced confidence slightly but did not change the prediction. CALL probability only 17.7%.

## Calibration Reversal Detail (10 hands)

| Hand | Expected | v2.2 | weighted | capped | Status |
|------|----------|------|----------|--------|--------|
| MW-30 | CALL | CALL (OK) | RAISE (XX) | **RAISE (XX)** | Still broken |
| MW-33 | RAISE | RAISE (OK) | RAISE (OK) | RAISE (OK) | OK |
| MW-50 | FOLD | CALL (XX) | FOLD (OK) | **CALL (XX)** | **REGRESSED** |
| d2410_CO_turn | BET | BET (OK) | BET (OK) | BET (OK) | OK |
| d3178_CO_river | BET | BET (OK) | BET (OK) | BET (OK) | OK |
| d2074_BTN_turn | CHECK | CHECK (OK) | CHECK (OK) | CHECK (OK) | OK |
| d3688_BB_flop | CHECK | BET (XX) | BET (XX) | BET (XX) | Both wrong |
| d4312_CO_turn | BET | BET (OK) | BET (OK) | BET (OK) | OK |
| d5466_CO_flop | CHECK | BET (XX) | BET (XX) | BET (XX) | Both wrong |
| d9556_BB_flop | CHECK | CHECK (OK) | CHECK (OK) | **BET (XX)** | **NEW REGRESSION** |

Capped: 5/10. Weighted was 7/10. **Two new regressions** vs weighted (MW-50, d9556).

## MW-50 5-Way Comparison Table

| hand_id | expected | v2.2 | iter1 | iter2 | weighted | capped |
|---------|----------|------|-------|-------|----------|--------|
| d5066_BB_flop | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d4798_HJ_flop | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d2410_CO_turn | BET | CHECK | BET | BET | BET | BET |
| d8007_BB_flop | CHECK | CHECK | BET | BET | CHECK | **BET** |
| d2205_BB_river | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d2920_BB_turn | BET | CHECK | BET | BET | BET | BET |
| d3178_CO_river | BET | CHECK | BET | BET | BET | BET |
| d1983_HJ_turn | BET | CHECK | BET | BET | BET | BET |
| d1562_HJ_turn | BET | CHECK | BET | BET | BET | BET |
| d3178_BTN_river | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d9941_CO_flop | CHECK | CHECK | BET | BET | BET | **BET** |
| d4798_BB_turn | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d7345_BTN_turn | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d9418_BB_flop | CHECK | CHECK | CHECK | BET | CHECK | CHECK |
| d9518_BTN_river | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d7361_BB_flop | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d1562_BTN_turn | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d8411_BB_turn | BET | BET | BET | BET | BET | BET |
| d6522_BB_river | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d5312_HJ_flop | CHECK | CHECK | BET | BET | CHECK | **BET** |
| d9653_BB_river | CHECK | CHECK | BET | BET | CHECK | **BET** |
| d8137_CO_flop | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d7964_BTN_turn | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d2788_BB_turn | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d4781_CO_flop | BET | BET | BET | BET | BET | BET |
| d4809_BB_turn | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d9418_BTN_flop | CHECK | CHECK | CHECK | BET | CHECK | CHECK |
| d2788_BTN_flop | BET | BET | BET | BET | BET | BET |
| d2079_BB_turn | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d6035_HJ_turn | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d8886_BB_flop | BET | CHECK | BET | BET | BET | BET |
| d7695_BTN_river | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d4312_BTN_flop | CHECK | CHECK | BET | BET | CHECK | **BET** |
| d1454_CO_turn | BET | BET | BET | BET | CHECK | **CHECK** |
| d9653_CO_river | CHECK | CHECK | BET | BET | CHECK | **BET** |
| d7345_HJ_river | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d9208_BTN_flop | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d1562_HJ_river | CHECK | CHECK | BET | BET | CHECK | **BET** |
| d6342_BTN_flop | CHECK | CHECK | BET | BET | CHECK | **BET** |
| d3688_BB_flop | CHECK | CHECK | BET | BET | BET | **BET** |
| d5066_BTN_turn | BET | BET | BET | BET | BET | BET |
| d0845_BB_flop | CHECK | CHECK | BET | BET | BET | **BET** |
| d3229_BTN_river | BET | BET | BET | BET | BET | BET |
| d7640_HJ_river | CHECK | CHECK | BET | BET | BET | **BET** |
| d0182_BTN_turn | BET | BET | BET | BET | BET | BET |
| d5312_BTN_turn | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d2410_BB_turn | CHECK | CHECK | BET | BET | CHECK | **BET** |
| d4534_BTN_river | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d7345_BB_river | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |
| d1262_BB_river | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK |

### MW-50 Summary by Expected Action

| Expected | v2.2 | iter1 | iter2 | weighted | capped |
|----------|------|-------|-------|----------|--------|
| BET (13) | 9/13 | 13/13 | 13/13 | 12/13 | **12/13** |
| CHECK (37) | 33/37 | 17/37 | 14/37 | 32/37 | **25/37** |

BET accuracy maintained at 12/13. CHECK accuracy collapsed from 32/37 (weighted) to 25/37 (capped). The RAISE cap redirected probability mass to BET, not CALL, destroying CHECK discrimination.

## Ship Recommendation

**DO NOT SHIP. EXPERIMENT FAILED.**

The RAISE cap at 1.50 does not solve the problem. It:

1. **Fixed FB-40** (+5pp to 75.0%) by recovering some CALL-expected spots from RAISE
2. **Destroyed MW-50** (-14pp to 74.0%) by shifting probability mass from RAISE to BET (not CALL)
3. **MW-30 still RAISE** -- the primary Criterion 5 failure persists
4. **Two new regressions** vs weighted (MW-50 FOLD->CALL, d9556 CHECK->BET)

The RAISE cap hypothesis was: reducing RAISE weight would move probability mass toward CALL on facing-bet spots. In practice, the mass moved to BET on non-facing-bet spots (MW-50 CHECK->BET), because the XGBoost loss function redistributes probability across ALL classes, not just within the facing-bet action space. Legal-action masking at inference cannot recover what the training loss already mis-learned.

### Possible next steps

- **Option B (targeted CALL supplement)** remains the most promising path for MW-30 -- add 20-30 facing-bet CALL exemplars structurally similar to MW-30/FB-22/FB-33/FB-34.
- **Two-stage weights** (different weights for facing-bet vs non-facing-bet rows) could address the MW-50/FB-40 tension but requires training infrastructure changes.
- **Accept weighted model** (88.0% MW-50, 70.0% FB-40) with MW-30 reversal exception if owner judges acceptable.

## Artifacts

| Artifact | Path |
|----------|------|
| Training script | `review/train_v2_3_weighted_capped.py` |
| Model | `river-rats-core/models/v2_3_capped_model.json` |
| Training report | `river-rats-core/models/v2_3_capped_training_report.json` |
| This report | `review/comms/OPTION_A_CAPPED_GATE_TABLE_2026-04-17.md` |
