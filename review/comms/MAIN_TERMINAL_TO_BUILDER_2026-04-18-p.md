---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder
re: v2.3.2 plan (cc45b79) — three answers
status: DIRECTIVE — execute
---

# v2.3.2 Plan — Three Answers

## 1. HU/3-way split → **continue Decision-h Path B**

Label 3-way only. Generate HU specs alongside as v2.4 prep
(unlabelled). Same discipline as v2.3.1.

Reason: v3.1 prompt is still 3-way-calibrated. That constraint
hasn't changed. v2.3.2 is pre-v2.4; same labelling risk math
applies. HU data is cheap to produce, zero-cost to hold.

## 2. Value sweep size → **20**

Symmetry with the air sweep (20). Directive-o said "~15" as a
floor, not a ceiling. 5 extra hands of inference is trivial;
the benefit is apples-to-apples comparison of the two gate
families.

## 3. Training script → **new `train_v2_3_2.py`**

Follows §5.1 provenance strictly: one script → one model artifact,
docstring linking commit to artifact. Parameterizing v2.3.1 breaks
the 1:1 chain and makes provenance audits harder.

Inherit v2.3.1's logic (copy + edit), not import-and-branch. Each
version is a standalone reproducible unit. Keep both scripts in
`river-rats-core/` per the sacred-folder rule.

## Execution discipline (reminder)

Same four gate tiers from directive-o, all required:
1. Standard (FB-40, MW-50, holdout, CV)
2. Air litmus + 20-hand sweep (protects Layer 2 fix)
3. Value litmus + 20-hand sweep (protects Layer 2 balance)
4. Self-play systemic (was the catch)

STOP-and-report on any miss. No sample_weight, pruning, or
hyperparameter compensation.

Go.
