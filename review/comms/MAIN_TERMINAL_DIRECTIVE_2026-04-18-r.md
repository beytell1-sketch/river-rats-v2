---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder
re: v2.3.2 Tier 1 FAIL triage — run α + β in parallel
status: DIRECTIVE — both in parallel; decision gated on joint signal
---

# Tier 1 FAIL Triage — α + β in parallel

## Decision

**Run Tier 4 self-play (α) AND per-hand diff (β) in parallel.**
Decision on v2.3.2 ship/reject gated on the joint signal from
both. Reject γ and δ — reasons below.

## Why both, not just α

**α alone** (self-play) gives systemic signal but doesn't tell
us WHICH hands flipped or WHY. If self-play passes, we still
don't know whether the 6 flipped holdout hands are legitimate
v2.3.2 corrections or real regressions.

**β alone** (per-hand diff) gives hand-level detail but lacks
systemic context. 3 hands flipped out of 40 could be noise or
real depending on the broader behavior.

**Together:** α tells us the systemic shape of the change; β
tells us the hand-level story. Joint analysis gives a confident
verdict in either direction.

Time cost: α is 30 min of compute, β is parallel analysis time.
Owner preference is slow+quality; both are quality signals. Run
them.

## Why reject γ (Rethink Path C)

Path C isn't wrong — target subspace is cleanly balanced (air
litmus 95.8%/98.4% CHECK, value litmus 99.5%/99.3% BET). The
architectural intent worked. Rethinking Path C without data
about what actually broke is premature.

If β reveals that the flipped hands are clear regressions (not
holdout-label-drift), we might revisit Path C. But not before.

## Why reject δ (Accept below-floor with owner sign-off)

This is the "paper over" pattern the hard rules explicitly
forbid. "It looks right" is not verification. 6-7pp below floor
without understanding why violates:

- `feedback_no_manual_overrides_in_labelling.md`: fix with data,
  not by lowering gates
- owner preference (`user_owner_style.md`): "Preference for
  catching a problem now over shipping and fixing later"

Owner sign-off doesn't convert "unexplained" into "safe to ship."

## Framing hypothesis for β

Your reasoning in the STOP report is sound: v2.2-era holdout
labels may not reflect current-truth for the precisely-marginal
hands near the decision boundary we deliberately shifted.

Test this hypothesis per flipped hand:
- What did v2.2 label it as?
- What does v2.3.2 predict?
- What would v3.1 prompt + current panels label it as TODAY?
- Is the flip a REGRESSION (model wrong on a hand it was right
  on) or a CORRECTION (model now-right on a hand the holdout
  mislabels)?

If 3+ of the 6 flipped hands are corrections → holdout-label-
drift is real, v2.3.2 is globally sound, gates need a label
refresh not a model change.

If 3+ of the 6 are regressions → real global-decision-surface
regression, revisit Path C or add further balancing.

Mixed (e.g., 3 corrections + 3 regressions) → partial fix
worked, minor additional data needed.

## Execution

**In parallel:**

1. **α — Tier 4 self-play** on v2.3.2 model (30 min compute)
   - Same script/harness as v2.3.1 self-play that caught the
     STOP
   - Same thresholds (facing-bet count ≥ 888, CHECK share ≤ 25%,
     etc.)
   - Report facing-bet count + action distribution + comparison
     to v2.2 / v2.3 / v2.3.1 baselines

2. **β — Per-hand diff on flipped holdout hands**
   - Isolate the 3 hands in FB-40 that flipped v2.3.1 → v2.3.2
   - Isolate the 3 hands in MW-50 that flipped v2.3.1 → v2.3.2
   - For each: cards, board, street, action_history, oracle
     probs under v2.3.1 vs v2.3.2, v2.2-era label, current
     v3.1-panel reasoning (spawn GTO reviewer subagent for each
     hand)
   - Categorize: REGRESSION / CORRECTION / MIXED / UNCLEAR

**Report both in a joint report:**
`BUILDER_V232_TIER1_TRIAGE_JOINT_2026-04-18.md`

## Decision matrix for ship

| α result | β result | Decision |
|---|---|---|
| PASS | 3+ corrections, 0-2 regressions | Ship v2.3.2; flag gates for label refresh |
| PASS | Mixed | Ship v2.3.2 with explicit note on holdout disagreements; solver on regression hands for v2.3.3 |
| PASS | 3+ regressions | Revisit Path C — scope widening or targeted additional data |
| FAIL (same kind as v2.3.1) | — | Revert to v2.3.1 baseline, v2.3.2 doesn't ship, root-cause the new systemic drift |
| FAIL (different kind) | — | β informs which direction to adjust; scope v2.3.3 |

## Cross-stream

- **Game:** stays v2.2 (unchanged)
- **Teaching:** Path B + blocker-bug + false-draw guard all
  continue independent
- **Owner:** no action needed; standing by for joint report

## Meta-principle (for memory potentially)

Standard accuracy gates assume stable label truth. When the
training data has deliberately shifted (counter-example
injection), gate regressions can reflect label-drift rather
than model-drift. Self-play + per-hand panel re-evaluation
are the more authoritative signals.

Gates are necessary (catch obvious breakage) but not sufficient
(can't distinguish label-drift from model-drift without
triangulation).

Go on both.
