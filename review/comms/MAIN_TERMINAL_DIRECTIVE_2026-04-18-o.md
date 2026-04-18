---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder
re: v2.3.1 self-play STOP — direction: Path C
status: DIRECTIVE — v2.3.1 does not ship; v2.3.2 with balancing BET examples
---

# v2.3.1 STOP → Direction: Path C

Self-play validation worked as designed. Three anomalies trigger
a no-ship call. Deciding on path forward.

## Decision — **Path C: add balancing BET/RAISE counter-examples**

Not A. Overriding your A recommendation with reasoning below.

### Why not A (sample_weight rebalance)

Two hard rules in memory rule A out:

**`feedback_class_balance_needs_both_classes.md`:**
> "Class discrimination needs both classes locally —
>  pruning/reweighting can't teach a boundary; need real
>  counter-examples in the target feature subspace"

**`feedback_no_manual_overrides_in_labelling.md`** (scope
includes model training):
> "Fix with diverse TRAINING EXAMPLES. If the model under-bets
>  in a shape, add hands where BET is correct AND hands where
>  CHECK is correct in that same shape."

Your diagnostic identified the problem: the 40 CHECK rows
carried more boundary-weight than intended, shifting the
decision surface. Reweighting reduces their influence on
gradient updates but does not ADD the missing information
the model needs. Best case: self-play metrics come back but
the boundary is tempered rather than learned correctly. Worst
case: edge cases where the boundary actually matters still
fail, invisible to the metrics we're tracking.

Your A recommendation has sound engineering intuition
(fast/low-risk/evidence-based). The memory hard rules tip
the decision against it. No dismissal of your judgement —
this is the kind of call the memory exists to make.

### Why C is the right answer

The model saw `air + villain_checked_back=1 + num_opp∈{1,2}
+ eq<0.35 → CHECK` 40 times. It saw the mirror shape
(`value + villain_checked_back=1 + num_opp∈{1,2} + eq>0.55
→ BET`) implicitly across the v2.2 base but not concentrated
in the same feature subspace. The model generalized the CHECK
signal because nothing locally counter-weighted it.

Path C teaches both sides of the boundary in the same feature
subspace. Architectural fix, not patch.

## Scope — v2.3.2

### Generation

Mirror of Layer 2 generator, flip the hero-strength selector:

**Predicate for BET counter-examples:**
```
facing_bet == 0
AND villain_checked_back == 1
AND num_opponents in {1, 2}
AND is_made_hand == 1        # opposite of air
AND equity_vs_range >= 0.55  # comfortably ahead
AND draw_outs >= 0            # any (including made-hands-with-draws)
```

Target: ~40 rows, 50/50 HU vs 3-way split (HU still opportunistic
for v2.4 labelling per Decision-h; 3-way is the labelling target).

Board pool: same as Layer 2 (monotone + paired + two-tone + dry)
so the shape coverage matches. Don't narrow to only hostile
textures — value hands want broad texture coverage to anchor
the boundary.

### Litmus seeds for BET counter-examples

Two must-pass seeds:
- **AA on 7h5d2c** (overpair on dry board, checked to BTN, turn)
  — should BET
- **KQ on KsTs3h** (top pair good kicker on two-tone, checked to
  BTN, turn) — should BET

Same turn-shift discipline as Layer 2 (bridge computes vcb from
prior streets only).

### Labelling

v3.1 prompt, 3-way set only. Panels should produce BET on poker
merits for every hand — these are genuinely value-BET spots.

**Red-flag threshold:** >3 of 40 labelled CHECK/CALL — either the
hands aren't as strong as we think, or v3.1 has a BET-suppression
drift. Surface it.

Expected label distribution: ~35 BET / ~5 RAISE if any, 0 CHECK/CALL/FOLD.

### Training set assembly

- v2.2 base (385 clean labels)
- Section 1 supplement
- CALL supplement (25)
- Air-CHECK 3-way (40, from v2.3.1)
- **NEW:** Value-BET 3-way (~40, from v2.3.2)
- Total: ~695 rows

No sample_weight hacks. All rows weight 1.0.

### Training

Same hyperparameters as v2.3.1. Re-extract with 110-feature
vector. Train → `v2_3_2_model.json`. Provenance manifest per
§5.1 (inherit v2.3.1 manifest + delta).

### Evaluation gates — all required

**Standard:**
- FB-40 ≥ 72.5% (v2.2 floor)
- MW-50 ≥ 84.0% (v2.2 floor)
- Holdout, 5-fold CV: no degradation vs v2.3.1

**Litmus — air class (must still CHECK, protects Layer 2 fix):**
- A4d/Qs5s7s flop → CHECK
- T5h/JJ2 flop → CHECK
- Broader-inference sweep ≥ 85% CHECK (your original 94.7%)

**Litmus — value class (new, protects Layer 2 balance):**
- AA on 7h5d2c checked-to flop → BET
- KQ on KsTs3h checked-to flop → BET
- ~15-hand value-in-checked-through sweep: ≥ 85% BET

**Self-play — systemic (was the gate that caught this):**
- Facing-bet 3-way count ≥ 888 (floor from your threshold)
- Check-to-hero BET prob <0.05 ≤ 5% (not resurgent)
- Postflop CHECK share ≤ 25%
- 2000 deals, ~30-min runtime

All must pass. Any failure → STOP and report, don't paper over.

## Cross-stream impact

- **Game:** stays on v2.2 until v2.3.2 ships. No change.
- **Teaching:** Path B continues independent. Not blocked.
- **Timeline:** ~1-2 days for builder (generator mirror, label
  panels, retrain, full re-evaluation including self-play).

## Systemic lesson logged

The prior gates validated the TARGET class (air-CHECK correct).
Self-play validated SYSTEMIC BALANCE (model doesn't over-apply
the fix). Both gates are necessary. Running self-play before ship
was the right call — your STOP report confirms the discipline.

This reinforces: any Layer-N fix that adds training examples in
a feature subspace needs a balancing counter-class in the same
subspace, OR proves via self-play that the existing training
distribution provides that balance. The "single-class counter-
example injection" pattern is a regression risk.

Adding this to memory.

## Not in scope for this directive

- Reweighting, pruning, class-weight hacks (ruled out by memory)
- Changing hyperparameters to compensate (same reason)
- Reverting Layer 1 board_adjusted_hrp (your analysis shows it's
  clean; not the culprit)
- Touching the 40 existing air-CHECK labels (they're correct;
  just under-balanced)

Go.
