---
date: 2026-04-09
from: Builder
re: Step 7 labelling approach — deterministic tree vs 57 LLM agents
---

## The question

The v2 decision tree is a deterministic flowchart with explicit
thresholds on named features from the 52-feature vector. Every
branch is:
- Step 1: if feature_X >= threshold AND feature_Y == value → CALL
- Step 2: if is_monster == 1 AND no suppressor fires → RAISE
- etc.

Should we label 563 situations with 57 LLM agents (per §1.1),
or write a deterministic script that applies the tree mechanically?

## Recommendation: deterministic script + LLM reviewer sample

**Why deterministic is better here:**

1. The tree was PURPOSE-BUILT to be feature-only and machine-evaluable.
   Every condition references a specific feature name and threshold.
   There are no judgment calls — the tree is an if/elif chain.

2. LLM labelling agents introduce the exact biases the calibration
   grading documented (over-fold, under-bet OOP). A deterministic
   script has zero bias — it applies the tree exactly as written.

3. 57 LLM agents at ≤10 hands each will produce inconsistent boundary
   decisions (e.g., one agent calls fold_equity=0.44 "close enough to
   0.45" while another doesn't). The tree has hard thresholds — a
   script respects them exactly.

4. The tree's preamble says: "Every branch must be explainable using
   ONLY the 52-feature vector." This is a machine specification,
   not a judgment prompt.

**The LLM role shifts to REVIEW:**

- Write the deterministic labelling script
- Apply it to all 563 situations
- LLM reviewers spot-check a stratified sample (~60 situations, ~10%)
  to verify the script implements the tree correctly
- Any discrepancy between script label and reviewer judgment gets
  flagged for manual resolution

**What this changes:**

| Original plan | Revised plan |
|---------------|-------------|
| 57 LLM labelling agents | 1 deterministic script |
| 29 LLM reviewers (all 563) | 6 LLM reviewers (60-sample) |
| Risk: LLM bias, inconsistency | Risk: script bug (mitigated by review) |
| ~3-4 hours | ~30 minutes |

**What this does NOT change:**

- The tree is still the labelling authority
- Reviewers still check the output
- Any script bug that mislabels a class is caught by the sample review
- The process guide's intent (quality labels) is served better by
  deterministic application than by LLM interpretation

## For owner awareness

This changes the team structure from §1.1's "≤10 hands per GTO agent"
to a programmer + reviewer model. The spirit of §1.1 is to prevent
quality degradation from context overload — a deterministic script
doesn't have context, so the rule doesn't apply. The reviewers still
follow §1.1 (≤15 hands per reviewer, 6 reviewers × 10 = 60 sample).
