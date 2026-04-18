---
date: 2026-04-18
from: Builder
to: Main terminal / Owner
re: v2.3.2 joint α+β verdict — REVERT to v2.3.1 + root-cause Path C
status: BLOCKED — decision matrix → α FAIL × β regressions → revert+rootcause
---

# v2.3.2 Joint Verdict — α + β

Both investigations complete. Per the decision matrix from review-r:

| α | β | Ship? | Triggered |
|---|---|---|---|
| **FAIL** | — | **Revert to v2.3.1 baseline; root-cause** | **← this row** |

## α — Self-play diagnostic (v2.3.2)

Ran 2000 deals, seed=42, same config as v2.3.1 diagnostic. Script:
`review/run_v232_selfplay_diagnostic.py`. Raw:
`review/v232_selfplay_raw.json`.

**All three anomaly watches tripped. v2.3.2 systemically WORSE
than v2.3.1.**

| Metric | v2.2 | v2.3 | v2.3.1 | **v2.3.2** | Target |
|---|---|---|---|---|---|
| Facing-bet 3-way count | 0 | 1,269 | 145 | **148** | ≥ 888 |
| Check-to-hero BET prob < 0.05 | 63% | 0% | 48.8% | **49.2%** | ≤ 5% |
| Postflop CHECK share | — | ~10% | 36.2% | **40.3%** | ≤ 25% |
| Total postflop decisions | — | 2,772 | 17,478 | 17,820 | (informational) |
| BET prob median (check-to-hero) | — | 0.73 | 0.063 | 0.080 | informational |

Adding 39 value-BET rows did NOT correct the v2.3.1 systemic
over-CHECK. Global CHECK share went UP (+4pp), not down.

## β — Per-hand diff + v3.1 relabel

Panel subagent re-labelled all 9 hands that flipped between v2.3.1
and v2.3.2 on FB-40/MW-50. Full analysis:
`review/label_batches_flipped/batch_01_result.txt`.

```
Final count: 7 REGRESSIONS / 1 CORRECTION / 1 MIXED / 0 UNCLEAR
```

**Per-hand:**

| sid | holdout | v2.3.2 | v3.1 verdict | class |
|---|---|---|---|---|
| FB-04 | RAISE | CALL | mixed (KB 1.7) | MIXED |
| FB-24 | RAISE | CALL | CALL | **CORRECTION** |
| FB-35 | CALL | FOLD | CALL | REGRESSION |
| FB-40 | FOLD | CALL | FOLD | REGRESSION |
| d0182_BTN_turn | BET | CHECK | BET | REGRESSION |
| d2410_CO_turn [anchor] | BET | CHECK | BET | **REGRESSION (calibration-anchor hard failure)** |
| d2788_BTN_flop | BET | CHECK | BET | REGRESSION |
| d4781_CO_flop | BET | CHECK | BET | REGRESSION |
| d8411_BB_turn | BET | CHECK | BET | REGRESSION |

**Key finding from the β panel:**

> "5 of 7 regressions (d0182, d2410, d2788, d4781, d8411) cluster
> on one coherent class — strong-made hero (TPTK / TP+kicker-
> advantage / pair+nut-draw) checked to at compressed SPR ~1.25,
> worse_hand_pct 82-90%, villain composition air-heavy or draw-
> heavy. v2.3.2 systematically CHECKS where KB Examples 2/4/6 and
> the d2410 anchor all support BET. This is the exact class the
> calibration anchor was designed to protect."

**Calibration anchor violation:** `d2410_CO_turn` is named in the
v3.1 prompt's Calibration Notes (line ~678) as a solver-verified
BET. v2.3.2 predicts CHECK. That's a hard failure, not a close call.

## Root-cause analysis — why Path C didn't generalize

Path C's thesis was:
> "The model saw `air + villain_checked_back=1 → CHECK` 40 times.
> It saw the mirror shape (`value + villain_checked_back=1 → BET`)
> implicitly across the v2.2 base but not concentrated in the same
> feature subspace. Path C teaches both sides of the boundary in
> the same feature subspace."

What actually happened:

1. **The target litmus seeds passed at 99% confidence** (AA/7h5d2c
   BET 99.5%; KQ/KsTs3h BET 99.3%). Path C's narrow intent — "AA
   and KQ bet in checked-through spots" — worked.

2. **But the broader class did NOT generalize.** The v3.1 calibration-
   anchor pattern (d2410: TPGK on J-high turn, checked-to, SPR~1)
   is exactly the class Path C was supposed to strengthen. Yet
   v2.3.2 flips d2410 to CHECK. **The litmus was too narrow to
   protect the class.**

3. **Systemic self-play got worse, not better.** v2.3.2's CHECK share
   (40.3%) is higher than v2.3.1's (36.2%). The 4 CHECK labels in
   the value-BET training set (AA on Qs5s7s2h — directive-q
   accepted them as honest) + 40 air-CHECK rows + 35 "clean" BET
   rows produced a net CHECK-ward shift beyond what any single
   class diff predicted.

4. **Holdout regressions are real, not artifact.** β panel
   confirmed 7 of 9 flipped hands are v3.1-correct as holdout said.
   Only 1 was a CORRECTION (FB-24). Holdout labels are not
   drifted on this class.

## What this means for the Path C approach

The architectural thesis (balance both sides in the target
subspace) is not invalidated — the **AA/KQ subspace** is cleanly
balanced. But the **target subspace was mis-scoped**:

- We defined the subspace as `is_made=1 AND eq≥0.55 AND vcb=1`
- Reality: this captured AA/KQ overpair-two-pair on "safe"
  textures but NOT the compressed-SPR TPGK/TPTK class (d2410,
  d0182, d4781 et al.) where eq is lower (0.6-0.7) and texture
  interaction dominates
- The generator picked strong-equity hands (overpair/two-pair,
  mostly) which don't represent the mid-equity strong-made-checked-
  to class
- The model learned "very-high-equity value = BET" but didn't
  learn "medium-equity strong-made = BET" — that gap is what the
  5 calibration-class regressions hit

Additionally:

- The 4 CHECK labels in the value-BET training (monotone-no-
  blocker overpair per directive-q) acted as signal that "even
  strong made hands CHECK on wet boards" — amplifying CHECK-
  bias in exactly the texture classes where d2410/d4781 need
  BET. This was the honesty-carries-cost trade-off we took with
  directive-q, and it materially contributed to the regression.

## Per-decision matrix outcome

```
α FAIL → Revert to v2.3.1 baseline; root-cause
```

β confirms the revert instinct with per-hand data. 7 regressions
(including a calibration-anchor failure) ≫ 3-threshold.

## Recommended next steps

### Immediate — revert

- Roll ship candidate back to v2.3.1 (commit `e663c6f` for model;
  `92e6463` for labels).
- v2.3.2 artifacts stay in git history; model in `models/` stays
  (doesn't collide with v2.3.1).
- Game terminal stays on v2.2 (unchanged — wasn't going to swap
  pre-v2.3.2 anyway).
- Teaching Path B continues independent.

### Root-cause tickets (v2.4 scope)

1. **Scope-the-subspace correctly for counter-example generation.**
   Path C failed because `is_made=1 AND eq≥0.55` didn't capture
   the compressed-SPR TPGK class. Future counter-example work
   should identify target-class hands by the actual decision-
   boundary pattern the model fails on (e.g., `worse_hand_pct ≥ 0.80
   AND is_made=1 AND 0.55 ≤ eq < 0.75 AND vcb=1 AND spr ≤ 2`) —
   not by generic "strong" filters.

2. **Counter-example corpus rethink.** 40 rows on a 637-row base
   is ~6% of the dataset. Any shift at that concentration creates
   non-linear boundary effects. Options:
   - Larger counter-example set (100+ rows covering texture and
     position diversity)
   - Sampling from existing base (relabel boundary hands rather
     than inject new ones)
   - Solver-queried training data (v2.4 plan mentioned in memory)

3. **Calibration-anchor protection gate.** d2410 should have been
   in the eval harness as an explicit pre-flight check:
   "Before accepting any new model, confirm it agrees with ALL
   calibration anchors in v3.1 §Calibration Notes." Would have
   caught this regression immediately after training.

4. **The directive-q CHECK labels in v2.3.2.** Honest labels, real
   cost. The trade-off was correct in principle (don't reject
   honest labels) but the specific 4 rows were on a texture class
   that amplified CHECK-bias beyond anchor tolerance. Future
   counter-example generation should separate honest-CHECK labels
   into a distinct bucket with different sample-weight treatment
   (future feature, after the no-sample-weight directive relaxes
   for narrow cases).

## Ship-block status

**NO SHIP. Reverting to v2.3.1.**

- Game stays v2.2 (has been the whole time — no change)
- Teaching Path B continues independent
- Next pipeline action: pick up v2.4 scope with root-cause tickets
  above + the two existing tickets (`hand_evaluator` straight-draw,
  defensive blocker direction) + HU counter-examples

## Self-assessment

The β panel's decisiveness ("5 of 7 regressions cluster on one
coherent class — the exact class the calibration anchor was
designed to protect") is the signal the litmus gates missed. This
reinforces the meta-principle from directive-r: distribution-count
thresholds are orientation signals; panel-reasoning audit is the
authoritative test.

The calibration anchors (d2410, d8886, d8963, d3178, etc.) in the
v3.1 prompt's Calibration Notes ARE already the "anchor protection"
I'm now proposing as a gate — they just weren't wired into the eval
harness. Turning them into a mechanical gate is low-cost and
would have stopped v2.3.2 at training-report-review, before 45 min
of wasted self-play compute.

## Artifacts this commit

- `review/run_v232_selfplay_diagnostic.py` — adapted for v2.3.2
- `review/v232_selfplay_raw.json` — raw stats
- `review/label_batches_flipped/batch_01_result.txt` — β per-hand
  panel analysis
- `review/comms/BUILDER_V232_JOINT_VERDICT_2026-04-18.md` — this doc

No model / training-data changes. v2.3.2 model artifact stays in
git but is marked as failed ship-candidate in this doc.
