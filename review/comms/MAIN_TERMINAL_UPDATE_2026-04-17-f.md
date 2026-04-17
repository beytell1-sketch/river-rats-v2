---
date: 2026-04-17
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Path A surprising — investigate 3 FB-40 misses + report full gate criteria
status: DIRECTIVE
---

# Main Terminal Update — 2026-04-17 (f)

MW-50 at 88% is excellent. BET-fix retained, CHECK
discrimination restored. Class weighting is a legitimate
production technique (v2.2 itself used class weights), not
a bandaid — the earlier memory note was in the context of
trying to compensate for a data gap; here the data is
adequate and the weighting amplifies the existing signal
appropriately.

But I can't call ship on partial numbers. Two things needed.

## 1. Investigate the 3 FB-40 misses (30 min)

FB-40 at 70.0% is exactly on the gate floor — one hand from
failure. The -2.5pp vs v2.2 is reportedly CALL/RAISE
confusion, not BET/CHECK.

For each of the 3 hands that v2.2 got right and the weighted
model gets wrong:

- situation_id, street, hero cards, board
- v2.2 prediction vs weighted prediction vs label
- What action the weighted model predicted (CALL when should
  be RAISE? RAISE when should be CALL?)
- Probability distribution over all 5 actions (is it a
  close call or a confident wrong answer?)
- One-line poker read: is this a systematic gap or noise?

Report in `review/comms/FB40_MISS_ANALYSIS_2026-04-17.md`.

If the 3 misses are:
- **Noise** (close probability splits, model is near-correct):
  → ship the weighted model. Random variance on 3 hands is
  not fixable without overfitting.
- **Systematic** (model consistently confuses CALL/RAISE in a
  specific shape): → a small targeted supplement (~20-30
  CALL/RAISE examples in the shape) would fix it cheaply.
  Worth doing before ship.

## 2. Report the remaining gate criteria

The weighted model needs ALL 5 ship-gate criteria reported:

| Criterion | Target | Status |
|---|---|---|
| FB-40 | ≥ 70.0% | 70.0% (reported) |
| MW-50 | ≥ 82.5% | 88.0% (reported) |
| Group D regression | ≤ 1 hand vs v2.2 | **? (not reported)** |
| Groups A+B absolute | ≥ 70% | **? (not reported)** |
| Calibration reversals | all correct on v2.3 | **? (not reported)** |

Run the diagnostic test set evaluation on the weighted model
and report all 5 rows. This is a single evaluator call.

## 3. Path B status

**Defer Path B.** The weighted model demonstrates the boundary
is learnable from existing data with appropriate weighting.
Adding 150 CHECK counter-examples is production-cleanliness
work — worth doing post-ship if the weighted approach proves
fragile over time, but not gating.

If investigation (§1) reveals a systematic CALL/RAISE gap,
the supplement should include targeted CALL/RAISE examples
for that shape — not 150 CHECK counter-examples aimed at
a different problem.

## 4. On class weighting as a production technique

To be clear: v2.2 used class weights (BET ≤ 2.0, RAISE ≤ 3.0,
others ≤ 4.0). The weighted v2.3 model uses rebalanced weights
(BET=0.38, CHECK=0.97, FOLD=1.83, CALL=2.39, RAISE=2.89).
This is the same technique with calibrated values for a
different training distribution. It is not a bandaid.

The weights are derivable from the training distribution and
should be documented in the model provenance (same as v2.2).

## Deliverables

- `review/comms/FB40_MISS_ANALYSIS_2026-04-17.md`
- Full 5-criterion gate table for the weighted model
- Both in one commit, push immediately
