---
date: 2026-04-20
from: Builder
to: Main terminal / Owner
re: v2.4 Stage 3.5 M5 — pre-retrain diagnostic (v2.3.1 model on β-panel anchors)
status: DIAGNOSTIC COMPLETE
---

# Stage 3.5 M5 — Pre-Retrain Diagnostic

Ran v2.3.1 model inference on 3 β-panel HIGH-impact anchors with
the NEW action-aware chained feature values. Model weights
UNCHANGED from v2.3.1 — only the feature inputs shift.

**Result: 3/3 anchors predict BET (expected action).**

## Per-anchor results

### d2410_CO_turn

✅ PASS — expected **BET**, predicted **BET**

- Probabilities: BET 0.976, CHECK 0.017
- Chain steps: `['flop:CHECK']`
- Villain composition (post-chain):
  - TP+: 0.193
  - medium_made: 0.392
  - draw: 0.148
  - air: 0.267

### d0182_BTN_turn

✅ PASS — expected **BET**, predicted **BET**

- Probabilities: BET 0.984, CHECK 0.010
- Chain steps: `['flop:CHECK']`
- Villain composition (post-chain):
  - TP+: 0.101
  - medium_made: 0.414
  - draw: 0.000
  - air: 0.486

### d8411_BB_turn

✅ PASS — expected **BET**, predicted **BET**

- Probabilities: BET 0.589, CHECK 0.391
- Chain steps: `['flop:CHECK']`
- Villain composition (post-chain):
  - TP+: 0.107
  - medium_made: 0.231
  - draw: 0.030
  - air: 0.632

## Interpretation

Per spec lock (a4cab83) M5:

- **3/3 anchors predict BET after Stage 3.5.** Stage 3.5
  feature correctness is sufficient to fix the class; Stage 4 re-label is additive insurance.

If d2410 in particular is BET at high confidence: the
calibration-anchor regression v2.3.2 introduced is fixable by
feature correctness alone. Stage 4 re-label becomes class-balance
insurance, not a correctness necessity.

If d2410 still misses: Stage 4 re-label is required to close the
class-balance gap.

## Chain steps captured

All 3 anchors have villain CHECKING the flop before the turn
decision. Stage 3.5 chain should fire at least:
`['flop:CHECK']` on each.

If chain_steps is empty on any anchor, the bridge → feature
extraction wiring isn't reaching that anchor — investigate.
