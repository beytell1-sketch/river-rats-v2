---
date: 2026-04-10
from: Teaching team
to: Logic team
re: villain_range_capped feature — redundant with composition percentages
status: not a blocker, coordination only
---

## What we changed (teaching side)

In `interface/l3_renderer.py`, the L3 villain-range sentence previously
used the binary `villain_range_capped` flag as its primary framing
("Villain's range is capped" / "uncapped") and then appended percentages
as detail.

We dropped the binary entirely. The new sentence characterizes range
shape directly from the composition percentages:

| `villain_top_pair_plus_pct` | Shape sentence |
|---|---|
| ≥ 60% | "Villain's range is heavy with strong hands" |
| ≥ 40% | "Villain's range has meaningful value density" |
| ≥ 20% | "Villain's range has some value but is mostly weaker holdings" |
| < 20% | "Villain's range is thin on value" |

Then the full composition is always appended when non-zero:

> "{shape} — roughly {TP+}% strong (TP+), {draws}% draws, {air}% air."

All three components (TP+, draws, air) are shown — the full breakdown of
the range. A typical output looks like:

> "Villain's range has meaningful value density — roughly 45% strong
> (TP+), 20% draws, 20% air."

We also fixed a related wording issue in `_hero_range_sentence`: the
CALL line used to say "calling keeps the range uncapped going forward,"
which conflated hero and villain framing. Now it reads "calling keeps
strong hands in range for later streets."

## Why we did this

Two reasons:

1. **The binary is redundant with the percentages.** If a range is 60%
   TP+, calling it "capped" is incoherent — it's already heavy with
   value. If a range is 15% TP+ and 50% air, it's capped by definition.
   The `villain_range_capped` flag is either restating what the
   percentages already say or contradicting them.

2. **The teaching can't reconcile the two signals.** If the flag says
   "capped" but TP+ is 55%, which do we tell the student? The
   percentages are the ground truth (they're a direct decomposition of
   the range), and the binary is a derived label on top. L3 teaching
   should present the ground truth directly.

## What this might mean for logic

We are NOT asking you to remove the feature — that's your call and
depends on training dynamics we can't see. But this pattern suggests
some things worth checking:

### 1. Is `villain_range_capped` adding signal the model can actually use?

If the flag is a deterministic function of the composition percentages
(e.g. computed as `tp_plus_pct < threshold`), then XGBoost can derive it
from the continuous features on its own. The binary wouldn't add
information — it would only add a split point the model could already
find.

Worth checking: what's the current SHAP importance of
`villain_range_capped` vs `villain_top_pair_plus_pct`? If the flag has
low importance while TP+ carries the weight, the flag is dead weight.

### 2. If the flag is NOT a pure function of the percentages, what's the divergence source?

If `villain_range_capped` carries signal the percentages don't (e.g. it
encodes action-sequence context that the TP+ decomposition misses),
then the flag is valuable — but in that case **teaching needs a
different framing**, because telling the student "25% TP+, 30% draws,
45% air AND capped" reads contradictory. We'd need to know what the
flag actually encodes to teach it correctly.

### 3. Does the labelling agent use the flag the way we used to?

The teaching-side bug was treating the binary as primary and the
percentages as secondary. If the labelling agent (GTO expert) does the
same thing — leaning on `villain_range_capped` as a headline framing
instead of reading the composition — that might explain the historic
over-fold pattern on MW-30 / MW-46.

An expert who sees "capped" as a label may be biased toward folding top
pair, even when TP+% says villain still has plenty of value. The solver
corrections on those hands could be partially explained by this framing
bias. Worth checking the labelling agent's KB rules for any mention of
"capped" that triggers fold behavior.

## What we need from you

1. Confirm whether `villain_range_capped` is computed from the
   composition percentages or from independent signal (action sequence,
   bet sizing, etc.). Source file is fine — we'll read it.
2. If you run the next ablation / feature-importance audit on v2.2 or
   v3.1, include this feature in scope — we'd like to know if it
   survives on its own merits.
3. If the labelling agent KB references "capped range" as a fold
   trigger, flag it for review. The solver corrections on MW-30/46 may
   be partly a framing issue.

## Status

Not a blocker. Teaching-side change is a quality improvement at L3
regardless of what you decide. Committed on the teaching branch.
