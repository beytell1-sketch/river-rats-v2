# Critical Feedback: Solver Labels in Training Data

**Date:** 8 April 2026
**Status:** LOGGED — requires follow-up action

---

## The Problem

We corrected 3 RAISE→CALL labels in v2.1 based on solver data
(non-set hands mixing at SPR). Those corrections were sound because
the expert logic ALSO supported CALL — the solver just confirmed it.

But in the v3 labelling round, the KB v1.2 update (Section 1.7
semi-bluff carve-out, Section 1.8 blocker effects) was informed by
solver findings. The labelling agents read these solver-derived rules
and applied them to produce RAISE labels that the model's features
can't support. Example: Ah5h on Qh8d3h was labelled RAISE because
Section 1.7 says "nut draw + blocker = RAISE." But the solver's
reason for raising involves suit-specific fold equity calculations
that our features can't represent. The model learned "NFD + facing
bet + IP = RAISE" and over-applied it to MW-20.

## The Rule (going forward)

**Solver data is for VERIFICATION and RESEARCH only.**

- Solver verifies: "Is the expert label wrong?" → If yes, the expert
  relabels using their own logic. The solver doesn't provide the label.
- Solver researches: "What patterns exist?" → Informs KB updates and
  factory design. Does NOT directly produce training labels.
- Expert labels everything: The GTO Expert agent uses the 5-factor
  framework and features the model can see. If the expert can't explain
  a label using those features, the label is wrong FOR OUR MODEL even
  if it's correct poker.

**The test for any training label:** Can the expert explain this
decision using ONLY features in the 48-feature vector? If the
explanation requires "the Ah blocks villain's folding range" or
"the Kc removes club flush combos" — and those aren't features —
the label teaches something the model can't learn. It becomes noise.

## Action Items

1. **Audit all labels that were influenced by solver corrections.**
   Identify any where the expert label was changed TO match solver
   output rather than the expert independently reaching the same
   conclusion.

2. **Revert solver-influenced labels to expert judgment.** The expert
   relabels using only the 5-factor framework and feature-visible
   reasoning.

3. **Update KB v1.3:** Section 1.7's semi-bluff conditions should be
   framed as "when expert reasoning supports RAISE based on visible
   features" not "when solver shows RAISE." The blocker conditions
   should note that suit-specific effects are NOT captured by current
   features and should not drive labels.

4. **Update labelling prompt:** Add explicit instruction: "Do not
   label based on suit-specific blocker effects unless flush_block_pct
   or a similar feature captures the effect. Your reasoning must be
   explainable by the 48-feature vector."

5. **Process Guide update:** Add Section 5.4: "Solver outputs are
   verification tools, not label sources. Expert logic that maps to
   model features is the only valid basis for training labels."

## Why This Matters

Our oracle's competitive advantage is that it plays from a teachable,
feature-based logic system. Students can learn the same reasoning.
The solver plays from range calculations humans can't replicate in
real time. If we teach the model to play like a solver, we lose the
teachability — and the model can't actually replicate the solver
because it can't see the information the solver uses.

A model that plays 80% accuracy with explainable logic is more
valuable than a model that plays 82% accuracy with unexplainable
label noise.
