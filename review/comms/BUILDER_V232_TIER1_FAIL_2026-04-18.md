---
date: 2026-04-18
from: Builder
to: Main terminal / Owner
re: v2.3.2 retrain — Tier 1 STOP (standard gates regressed below v2.2 floors)
status: BLOCKED — retrain complete, FB-40/MW-50 below floor; reviewer scope needed
---

# v2.3.2 Retrain — Tier 1 STOP

Retrain executed on 716-row CSV (all 39 value-BET labels accepted per
directive-q). Tier 1 and Tier 2 ran. Tier 3 ran for additional context.
Tier 4 (self-play, ~30 min) HELD pending reviewer decision.

## Gate scoreboard

| Tier | Gate | Floor | v2.3.1 | v2.3.2 | Status |
|---|---|---|---|---|---|
| 1 | FB-40 | ≥ 72.5% | 77.5% | **70.0%** | **FAIL** (-7.5pp) |
| 1 | MW-50 | ≥ 84.0% | 84.0% | **78.0%** | **FAIL** (-6.0pp) |
| 2 | A4d/Qs5s7s flop | CHECK | CHECK 0.935 | CHECK 0.958 | **PASS** |
| 2 | T5h/JJ2 flop | CHECK | CHECK 0.983 | CHECK 0.984 | **PASS** |
| 3 | AA/7h5d2c flop | BET | — | BET 0.995 | **PASS** |
| 3 | KQ/KsTs3h flop | BET | — | BET 0.993 | **PASS** |
| 4 | Self-play systemic | — | FAIL (v2.3.1) | **NOT RUN** | held |

## What worked

**Target subspace is balanced.** Both litmus classes pass at high
confidence:
- Air class CHECK (protected): A4d 95.8%, T5h 98.4%
- Value class BET (restored): AA 99.5%, KQ 99.3%

This is exactly the Path C intent — bidirectional counter-examples in
the same feature subspace teach both sides of the boundary.

## What broke — standard holdouts

FB-40 dropped from 77.5% to 70.0% (8 hands wrong → 12 hands wrong,
3 newly wrong). MW-50 dropped from 84.0% to 78.0% (8 → 11 wrong,
3 newly wrong).

### Hypothesis

Adding 39 value-BET training rows with specific shape features
(is_made=1 + checked-through + vcb=1 on turn) has shifted the global
decision boundary toward BET in shapes FB-40/MW-50 contain. Both
test sets include hands where CHECK-correct is the expected label
AND some features overlap with the newly-trained BET subspace
(high hrp, checked-through context, non-trivial equity).

The holdouts aren't re-labelled — they still encode the v2.2 labeller
expectations. A model that's moved toward BET in those shapes now
disagrees with the v2.2 labels on some edge cases.

Without per-hand diff analysis of which 3 hands flipped in each
holdout, the hypothesis is directional. Can produce that detail if
reviewer wants it as part of scope decision.

## Training metadata

```
Holdout accuracy:     0.9028   (v2.3.1: 0.9118)
5-fold CV:            0.9414 ± 0.0232   (v2.3.1: 0.9439 ± 0.0158)
Best iteration:       109

Per-class holdout:
  FOLD   prec 0.94  recall 1.00  f1 0.97  (15)
  CHECK  prec 0.97  recall 0.83  f1 0.90  (36)
  CALL   prec 0.76  recall 0.89  f1 0.82  (18)
  BET    prec 0.91  recall 0.98  f1 0.95  (65)
  RAISE  prec 0.83  recall 0.50  f1 0.62  (10)

Class distribution (716 rows):
  BET    323 (45.1%)
  CHECK  176 (24.6%)
  CALL   88  (12.3%)
  FOLD   77  (10.8%)
  RAISE  52  (7.3%)
```

Class distribution sensible (45% BET vs v2.3.1's 42.5% — small shift
consistent with adding ~40 BET rows). CHECK share slightly down
(26.1% → 24.6%) — also consistent.

RAISE recall dropped from 0.60 → 0.50 on same support (10). Small-n
noise. Not the driver of the FB-40/MW-50 regression.

## Artifacts committed in this cycle

- `assemble_v23_2.py` — extends v2.3.1 assembly with value-BET loader
- `river-rats-core/train_v2_3_2.py` — per §5.1 provenance, inherits
  v2.3.1 hyperparameters
- `training-data/v2_3_2_training.csv` — 716 rows
- `river-rats-core/models/v2_3_2_model.json` + report + manifest

Manifest includes a `future_work_v24_note` documenting the factory
predicate gap on monotone-no-blocker textures (directive-q ack).

## Four paths for reviewer to scope

### Path α — Run Tier 4 self-play first; decide based on full data

Tier 1 fail is concerning but may be noise on small test sets (3
newly-wrong hands each). If Tier 4 self-play passes (facing_bet ≥
888, CHECK ≤ 25%, low-BET ≤ 5%), v2.3.2 may be *systemically*
healthy even with marginal holdout regression. If Tier 4 also
fails, triangulation confirms Path C didn't land.

~30 min self-play run. Still stops at Tier 4 fail without paper-
over — same discipline as v2.3.1.

### Path β — Per-hand diff analysis on FB-40/MW-50 flipped hands

Identify which 3 hands flipped in each set. If flipped hands are
CHECK→BET in value-looking shapes, the regression is the expected
cost of Path C's rebalancing — holdouts' labels are still v2.2-era
and may themselves be suboptimal on the value-in-checked-through
shape. Reviewer judges whether the holdout labels are the ground
truth or whether v2.3.2's prediction is actually correct.

### Path γ — Stop v2.3.2; rethink Path C with tighter shape isolation

v2.3.2's 39 value-BET rows may have influenced too broad a feature
subspace. Options:
- Add v2.3.1's 40 air-CHECK with sample_weight 1.2, 39 value-BET
  with 0.8 (favors the air correction that was working standalone)
- Drop one class, iterate — but this veers back toward v2.3.1
  or v2.3 shape

I don't recommend γ — it unwinds the Path C architectural decision
already made.

### Path δ — Accept v2.3.2 as the model (below floor but target fix
  works), document the delta, ship with explicit holdout-regression
  caveat

Requires owner sign-off on missing the FB-40/MW-50 floors. Not
recommended without additional data (α or β).

## Builder recommendation

**Path α — run Tier 4 self-play.** The Path C thesis was that
bidirectional counter-examples fix the systemic imbalance self-play
caught in v2.3.1. Tier 1 is a necessary but not sufficient gate;
the real question is whether v2.3.2 is systemically balanced. A
30-minute investment gives us the complete data picture.

If Tier 4 passes cleanly (all 3 self-play watches OK), Path β
follow-up becomes meaningful — we can judge whether the FB-40/MW-50
"regressions" are artifacts of holdout labels drifting out of
sync with the corrected boundary.

If Tier 4 fails, we have full triangulation and Path γ/δ scope.

## Cross-stream status

- Game: v2.2 (unchanged)
- Teaching: Path B continues independent

**No ship.** Reviewer decision needed on Path α/β/γ/δ.
