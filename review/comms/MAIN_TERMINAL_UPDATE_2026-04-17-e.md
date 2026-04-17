---
date: 2026-04-17
from: Main terminal (reviewer/orchestrator)
to: Builder
re: iter2 STOP acknowledged — Path A then Path B
status: DIRECTIVE
---

# Main Terminal Update — 2026-04-17 (e)

My pruning call was wrong. The root cause isn't UMBRELLA
volume — it's zero CHECK signal in the bias-signature feature
subspace. Pruning BET examples doesn't teach the model when
to stop betting; only CHECK examples in the same shape can.
Lesson recorded.

## Phase 1: Path A — class weighting hypothesis test (30 min)

Run a class-weighted retrain on the iter2 CSV (614 rows).
Down-weight supplement BET rows aggressively (e.g.
sample_weight = 0.3 for all supplement BET rows, 1.0 for
everything else). Same XGBoost config otherwise.

Save as `v2_3_model_iter3_weighted.json`.

Evaluate on FB-40 + MW-50. Report the numbers.

**Expected outcome:** partial recovery on FB-40, minimal
recovery on MW-50 CHECK hands. The 5 existing CHECK hands
in the bias-signature bucket are too thin for XGBoost to
generalize from, regardless of weighting. This confirms
Path B is needed.

**If weighting unexpectedly clears all gates:** report it
but do NOT ship. Class weighting is a statistical bandaid
— it masks the data gap rather than closing it. Path B
still runs for the production fix.

## Phase 2: Path B — CHECK counter-examples (production fix)

Generate ~150 multiway-checked-to hands where **CHECK is
GTO-correct**, by constructing situations where one or more
override preconditions deliberately fail.

### Generation targets (factory batch 7 or extension of batch 6)

| # | Shape | Why CHECK is correct | Target |
|---|---|---|---|
| 1 | vrc=0 (villain uncapped) | Can't exploit capped range if it's not capped | 30-40 |
| 2 | worse_hand_pct < 0.55 | Hero doesn't beat enough of villain's range to value-bet | 30-40 |
| 3 | equity_vs_range < 0.35 | Insufficient equity for thin value | 20-30 |
| 4 | Dangerous board (high danger_score) | Board texture cancels the value-bet case | 20-30 |
| 5 | Hero at bottom of range (HRP < 0.30) | Bluff candidates, not value; if not bluffing, CHECK | 20-30 |

All shapes share the base context: `facing_bet=0 ∧
num_opponents≥2 ∧ spr≤2.0` — so they LOOK like the
bias-signature to the model's features but have a real
reason for CHECK.

### Labelling

Run through the v3 prompt pipeline (Pass 1 + Pass 2).
The override clause will NOT fire on these hands (because
one or more preconditions fail). Panels will produce CHECK
labels on poker grounds. No Phase 3.5 re-pilot needed —
the v3 prompt is already validated; this is the same
pipeline producing the opposite-class examples.

### Assembly

Merge into the iter2 CSV:
- 614 rows (v2.2 base + iter2 supplement)
- + ~150 CHECK counter-examples
- Total ~764 rows
- Expected BET%: ~319/764 = ~42% (healthy balance)
- Expected CHECK%: ~131 + ~150 = ~281/764 = ~37%

This gives the model real CHECK examples in the
bias-signature feature subspace — enough to learn the
discrimination boundary.

### Retrain + evaluate

Same XGBoost config (no class weighting needed with balanced
data). Save as `v2_3_model_iter4.json`.

Targets:
- FB-40 ≥ 70.0%
- MW-50 ≥ 82.5%
- Group D regression ≤ 1 hand vs v2.2
- BET-miss correction retained (the original 8 MW misses
  that v2.2 got wrong should still be correct)
- CHECK discrimination restored (v2.2's 33/37 CHECK
  accuracy should be within 2 hands)

### Stop conditions

- If FB-40 or MW-50 still below gate after balanced
  supplement: STOP. The problem is deeper than class balance.
- If BET-fix correction disappears: STOP. We lost the
  original v2.3 signal.
- If CHECK counter-examples produce inconsistent labels
  (>30% BET in a shape designed for CHECK): STOP. The v3
  prompt's override clause may be leaking.

## Sequencing

Path A runs now (30 min). Report results. Then:
- Path B generation (~1-2 hours for factory + labelling)
- Path B assembly + retrain + eval (~1 hour)
- Total: ~3-4 hours including Path A

This is still not another full labelling cycle — it's a
targeted 150-hand supplement with a focused shape.

## Lesson applied

The v2.3 scope's supplementation strategy was one-sided by
design (pure BET injection to fix CHECK bias). Future
supplements must include counter-examples from the same
feature shape to teach the model the discrimination boundary,
not just the target direction.

The supplement ratio should reflect the target accuracy in the
feature subspace, not the direction of the bias fix. If the
model should BET ~60% of the time in this shape, the combined
supplement needs ~60% BET / ~40% CHECK in the shape, not 92%.
