---
date: 2026-04-17
from: Builder
to: Main terminal / Owner
re: STOP — v2.3 model fails ship gate (bias reversal)
status: BLOCKED — needs architectural decision before iterating
---

# Builder Status #8 — Phase 7 STOP

## What happened

Phases 5→6→7.1/7.2 ran end-to-end per owner directive.

| Phase | Commit | Result |
|---|---|---|
| 5 Assembly | `cd730d0` | ✅ 871 rows, preflight clean |
| 6 Training | `cd730d0` | ✅ CV 94.95% ±1.60%, holdout 94.29% |
| 7.1 Evaluation | `cd730d0` | ❌ **STOP** |

## The failure

| Set | v2.2 | v2.3 | Delta |
|---|---|---|---|
| FB-40 | 72.5% (29/40) | **62.5% (25/40)** | **-4 hands** |
| MW-50 | 84.0% (42/50) | **60.0% (30/50)** | **-12 hands** |

v2.3 model is worse than v2.2 on both test sets. Ship gate FAIL.

## Root cause — bias reversal

v2.3 training data is **62.8% BET** (up from v2.2's 25.7%). The
supplement was 92.6% BET-labelled (by design — fixing the CHECK
bias). But the class imbalance flipped the model:

- **BET hands (MW-50):** 9/13 → **13/13** (perfect). The old
  CHECK-bias miss is gone.
- **CHECK hands (MW-50):** 33/37 → **17/37** (collapsed). Model now
  over-bets, predicting BET on 16 hands that should be CHECK.

The model "learned" the bias fix but lost CHECK discrimination.
CV/holdout look fine (94.95%) because the training set itself is
now BET-heavy — the model aces its own distribution but can't
generalise to the balanced test sets.

## What this means

The v2.3 scope correctly identified WHAT to fix (defensive
multiway-checked-through CHECK bias). But the supplementation
approach (pure BET injection without balancing) created an inverse
problem. The 400-hand supplement was ~8× the target bucket and
overwhelmed the existing CHECK signal.

## Options for owner

This needs an architectural decision, not a parameter tweak:

1. **Class-balanced supplementation** — add ~200-300 CHECK-labelled
   hands to restore balance (v2.3b target: BET ≈40-45%, not 62.8%).
   This preserves the BET signal but restores CHECK discrimination.

2. **Class weighting in XGBoost** — apply `scale_pos_weight` or
   `sample_weight` to down-weight the supplement BET rows during
   training. Same data, different emphasis. Faster than sourcing
   new hands but less interpretable.

3. **Targeted supplement pruning** — reduce the UMBRELLA bucket
   from 268 to ~100-150, keeping only the most predicate-
   concentrated hands. This lowers BET% without losing the
   bias-fix signal.

4. **Hybrid** — option 2 (class weighting) as quick validation
   of whether balance is the root cause, then option 1 or 3 for
   the production fix.

Builder recommends option 4: run a quick class-weighted retrain
(Phase 6 only, ~20 min) to confirm balance is the issue. If
FB-40 + MW-50 recover, commit to option 1 or 3 for the clean fix.

## Phase grid

| Phase | Status |
|---|---|
| 5 Assembly | ✅ 871 rows, clean |
| 6 Training | ✅ model trained |
| 7.1/7.2 Evaluation | ❌ **FAIL — bias reversal** |
| 7.3 Solver validation | ⏸️ not reached |

## Awaiting

Owner architectural direction on options 1-4 above. Builder
standing by — no autonomous iteration without direction.

Full report at `review/comms/PHASE_567_REPORT_2026-04-17.md`.
