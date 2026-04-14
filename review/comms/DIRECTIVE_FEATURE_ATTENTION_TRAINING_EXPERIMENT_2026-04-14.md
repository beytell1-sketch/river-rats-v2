---
date: 2026-04-14
from: Owner (Rupert)
to: Builder team
re: Feature attention training experiment — can we train using tagged features?
status: DIRECTIVE — plan first, build second
prerequisite: 20 pilot v2 hands with full feature attention data
blocks: Pass 1 production labelling (do NOT start 385 hands until this experiment completes)
---

# Feature Attention Training Experiment

## Purpose

Before committing ~273 agents to label 385 hands with feature
attention data, verify that the feature attention data is
actually USABLE for training. No point collecting it at scale
if we can't consume it.

This is a mechanical test, not an accuracy test. 20 hands is
too few to measure model quality. The question is: does the
pipeline work? Can XGBoost consume attention-weighted data?
Does it change model behaviour in the expected direction?

## The experiments

Four experiments, each testing a different way to use feature
attention in training:

### Experiment 1: Per-sample feature masking

For each training row, zero out features that no expert tagged
(across the union of all 6 teams). The model only sees features
experts said mattered for that specific hand.

Questions:
- Does XGBoost handle sparse per-sample feature masking?
- Does the model still produce predictions?
- Do the predictions differ from a model trained on all 54
  features unmasked?

### Experiment 2: Attention-weighted features

Multiply each feature value by an attention weight based on
the expert tag level:

| Tag level | Weight |
|---|---|
| PRIMARY | 1.0 (full signal) |
| CONFIRMED | 0.7 |
| DISCOVERED | 0.5 |
| Untagged | 0.1 (attenuated, not zero) |

Train on weighted features. Questions:
- Does this shift feature importance toward expert-tagged
  features?
- Is the importance ordering closer to expert attention than
  a model trained on raw features?
- Does XGBoost handle the attenuated values correctly or does
  it treat them as naturally low values?

### Experiment 3: Attention as auxiliary features

Add 54 binary columns (one per feature) indicating whether
each feature was tagged by any expert for this hand. So the
model sees 108 columns: 54 original features + 54 attention
flags.

Questions:
- Does the model learn to weight features differently when
  the attention flag is 1 vs 0?
- Do the attention flag features appear in SHAP importance?
- Is this a cleaner mechanism than Experiment 2's multiplication?

### Experiment 4: Intention prediction (Model 2)

Train a separate multi-label classifier: 54 raw features →
intention tags. Each hand has 1-3 intention labels from the
pilot data.

Questions:
- Can XGBoost predict intention tags from features alone?
- Which features drive intention prediction vs action
  prediction? Are they different?
- Is multi-label XGBoost feasible at all, or does this need
  a different architecture?

## Process — MANDATORY

This experiment follows the standard process. No shortcuts.

### Step 1: PLAN

The ML Architect writes a plan for all 4 experiments:
- What data goes in (exact format, exact source files)
- What code needs to be written
- What output each experiment produces
- How to evaluate whether it "worked" (mechanical success
  criteria, not accuracy targets)
- What could go wrong (XGBoost limitations, data format
  issues, etc.)
- Which experiments are independent (can run in parallel)
  and which depend on each other

**Plan goes to review/comms/. Owner reviews.**

### Step 2: REVIEW PLAN

Owner reviews the plan. Questions:
- Are the experiments the right ones?
- Are the mechanical success criteria clear?
- Is anything missing?
- Any experiments to drop or add?

**Nothing proceeds until the plan is approved.**

### Step 3: BLUEPRINT

The Architect reads the plan and the source code. Produces
exact blueprints:
- Which files to create or modify
- Exact insertion points
- Exact function signatures
- Exact data formats
- Test cases to write BEFORE implementation

**Blueprint goes to review/. Owner reviews.**

### Step 4: REVIEW BLUEPRINT

Owner reviews the blueprint. Questions:
- Does it match the plan?
- Are the test cases sufficient?
- Any concerns about existing code being modified?

**Nothing proceeds until the blueprint is approved.**

### Step 5: BUILD

The Programmer implements from the blueprint. Tests first,
then implementation. Runs all 4 experiments on the 20 pilot
hands.

**Results go to review/comms/.**

### Step 6: REVIEW RESULTS

Owner reviews the results. Questions:
- Did each experiment work mechanically?
- Does the output make sense?
- Which mechanism (masking, weighting, auxiliary, Model 2)
  is most promising?
- Should we collect feature attention at scale (proceed to
  Pass 1) or simplify?

**This review determines whether Pass 1 labelling proceeds
with feature attention or without it.**

## What this blocks

Pass 1 production labelling (385 hands) does NOT start until
this experiment completes and the owner reviews results. If
feature attention data turns out to be mechanically unusable,
we simplify the labelling protocol before scaling.

## What this does NOT block

- Teaching team Phase 1 (templates + layout) — independent
- Any builder work on non-labelling tasks

## Agent allocation

| Step | Who | Agent-calls |
|---|---|---|
| Plan | ML Architect | 1 |
| Blueprint | Architect | 1 |
| Build + run | Programmer | 1 |
| **Total** | | **3** |

Plus owner reviews at Steps 2, 4, and 6.

## Timeline

| Step | Sessions |
|---|---|
| Plan + review | 0.5 |
| Blueprint + review | 0.5 |
| Build + run + review | 1 |
| **Total** | **~2 sessions** |

## Success criteria (mechanical, not accuracy)

| Experiment | Success = | Failure = |
|---|---|---|
| 1 (masking) | XGBoost trains and predicts with per-sample masked features. Predictions differ from unmasked. | XGBoost errors on sparse input, or predictions are identical (masking has no effect). |
| 2 (weighting) | Feature importance shifts toward expert-tagged features compared to raw training. | Importance ordering is unchanged (weighting has no effect on tree splits). |
| 3 (auxiliary) | Attention flag features appear in SHAP with non-zero importance. | Attention flags are ignored by the model (zero importance). |
| 4 (Model 2) | Multi-label XGBoost trains and produces intention predictions. Predictions are non-trivial (not all same class). | Multi-label doesn't work in XGBoost, or all predictions collapse to one class. |

---

**Builder: start with Step 1 — ML Architect writes the plan.
Send to review/comms/ for owner review. Do NOT skip to
blueprinting or building.**
