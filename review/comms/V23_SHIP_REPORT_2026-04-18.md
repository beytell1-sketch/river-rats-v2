---
date: 2026-04-18
from: Builder
to: Owner + Main terminal + Teaching terminal
re: v2.3 SHIPPED — training report + canonical model designation
status: SHIPPED — v2.3 replaces v2.2 as production model
directive: MAIN_TERMINAL_UPDATE_2026-04-18-b.md
---

# v2.3 Ship Report

## Model designation

**Production model:** `river-rats-core/models/v2_3_clean_model.json`
**Canonical copy:** `river-rats-core/models/v2_3_model_shipped.json`
(byte-identical to `v2_3_clean_model.json`; preserved for
provenance if the clean file is later overwritten by experiments)

**Supersedes:** `v2_2_model.json` (remains in `models/` for
reference; teaching team may still reference v2.2 export until
v2.3 handoff is built)

## Training configuration

| Parameter | Value |
|---|---|
| Training CSV | `training-data/v2_3_clean_training.csv` |
| Rows | 637 |
| Features | 108 (54 raw + 54 attn=1.0) |
| Class weighting | NONE |
| XGBoost n_estimators | 800 (early stopped at iter 157) |
| early_stopping_rounds | 50 |
| CV accuracy | 93.09% ± 1.35% |
| Holdout accuracy | 94.53% |
| Trainer script | `river-rats-core/train_model_v2_2.py` |
| Training report | `models/v2_3_clean_training_report.json` |

## Training data composition (Option 4+3)

| Source | Rows | BET% |
|---|---|---|
| v2.2 base (re-encoded via CAT_MAPS) | 385 | 25.7% |
| Section 1 rows 1-12 (no UMBRELLA) | 207 | ~92% |
| CALL supplement (factory, v3-labelled) | 32 | 0% (all CALL) |
| Pilot (v3-labelled) | 16 | mixed |
| Deduped | -3 | — |
| **Total** | **637** | **45.2%** |

Action distribution:
- BET: 288 (45.2%)
- CHECK: 137 (21.5%)
- CALL: 89 (14.0%)
- FOLD: 75 (11.8%)
- RAISE: 48 (7.5%)

## Evaluation results

| Set | v2.2 | v2.3 | Delta |
|---|---|---|---|
| FB-40 | 72.5% (29/40) | **72.5% (29/40)** | 0 (recovered) |
| MW-50 | 84.0% (42/50) | **82.0% (41/50)** | -1 hand |

### What improved (the bias fix)
- 4/4 MW BET-misses corrected (d2410, d1983, d1562, d8886)
- CALL/RAISE discrimination clean (FB-22/29/33/34 all correct)
- Group D: 1 regression (d2074), within ≤1 tolerance

### What traded
- 5 marginal CHECK spots on MW-50 shifted to BET (d8007, d9941,
  d6342, d0845, d7640) — decision-boundary trade-off for
  correcting the 4 systematic BET-misses
- Net: -1 hand on MW-50 (42→41)

### What was inherited (not new)
- d3688, d5466, MW-50 reversal failures existed in v2.2
- These were never fixed by the v2.3 supplement scope

## Ship gate (final, per owner recalibration)

| # | Criterion | Target | Actual | Status |
|---|---|---|---|---|
| 1 | FB-40 | ≥70% | 72.5% | ✅ PASS |
| 2 | MW-50 | ≥82% (recalibrated) | 82.0% | ✅ PASS |
| 3 | Groups A+B | ≥70%+5pp | N/A | WAIVED (build for v2.4) |
| 4 | Group D | ≤1 regression | 1 (d2074) | ✅ PASS |
| 5 | Reversals | No new beyond Crit 4 | 1 (d2074) | ✅ PASS (reframed) |
| 6 | Solver 8 MW | ≥6/8 | — | POST-SHIP |

## Iteration history

| Config | FB-40 | MW-50 | Shipped? | Why not |
|---|---|---|---|---|
| v2.2 (baseline) | 72.5% | 84.0% | ✅ shipped | — |
| iter1 (full UMBRELLA 268) | 62.5% | 60.0% | ❌ | BET flood |
| iter2 (pruned UMBRELLA 80) | 70.0% | 54.0% | ❌ | Still BET flood |
| weighted (RAISE 2.89×) | 70.0% | 88.0% | ❌ | RAISE over-prediction |
| capped (RAISE 1.50×) | 75.0% | 74.0% | ❌ | MW-50 collapsed |
| **clean (Option 4+3)** | **72.5%** | **82.0%** | **✅** | — |

## Post-ship items

- **Solver on 8 MW misses** (Phase 7.3) — owner-led, at-pace.
  Measures whether the bias correction worked on the exact spots
  that originally failed. High diagnostic value.
- **Self-play retest** — v2.3 fixes the passive loop that killed
  v2.2 self-play (63% BET prob <0.05 on check-to-hero spots).
  Re-running `self_play.py` with v2.3 validates the fix in
  dynamic play context.
- **Groups A+B diagnostic test set** — build for v2.4.
- **Teaching handoff** — teaching team needs a v2.3 export
  (same format as the v2.2 Track D handoff).
- **d2074 investigation** — the 1 Group D regression. Candidate
  for v2.4 targeted fix if solver confirms BET is wrong here.

## Experimental artifacts (preserved, not production)

| File | Purpose |
|---|---|
| `v2_3_model.json` | iter1 (full UMBRELLA, DO NOT USE) |
| `v2_3_iter2_model.json` | iter2 (pruned UMBRELLA) |
| `v2_3_weighted_model.json` | Path A class-weighted |
| `v2_3_capped_model.json` | Option A RAISE-capped |
| `v2_3_clean_model.json` | **PRODUCTION** (= `v2_3_model_shipped.json`) |

— Builder, 2026-04-18
