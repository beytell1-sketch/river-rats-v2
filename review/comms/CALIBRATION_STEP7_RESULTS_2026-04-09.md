---
date: 2026-04-09
from: Builder (grading process)
re: Step 7 calibration exam — GATE PASSED
---

## Calibration Results

**Score: 24/24 (100%)**
**Gate (20/24): PASS**
**Gate (reversals 3/3): PASS**

## Process compliance

- Exam: 24 blind situations generated from calibration_exam.py harness
- Agents: 3 labelling agents (8 hands each), parallel, blind
- Agent access: prompts/gto_labeller_v1.md + knowledge/three_way_gto.md ONLY
- Agents did NOT have access to: calibration_exam.py, answer key, BATCH2_8_RANGE_ANALYSIS.md
- Grading: separate Python process comparing answers against _parse_gto_table()
- Answer key: MW-30 updated to CALL before exam (solver-verified correction)

## Reversal hands

| Hand | Expert | Agent | Status |
|------|--------|-------|--------|
| MW-30 | CALL (corrected) | CALL | PASS |
| MW-33 | RAISE | RAISE | PASS |
| MW-50 | FOLD | FOLD | PASS |

## Confidence distribution

- HIGH: 19/19 (100%)
- MEDIUM: 5/5 (100%)

## Bias check

No failures to analyze. The over-fold bias documented in v3 calibration
(CALIBRATION_GRADING_V3.md) did not manifest — all CALL/FOLD boundaries
were handled correctly including MW-30 (the corrected hand) and MW-50
(the thin-margin hand).

## Verdict

Calibration gate passed. Labelling agents are cleared to proceed
with Step 7 relabelling of 557 situations.

## Evidence files

- review/blind_calibration_exam_step7.json (24 situations, no answers)
- review/calibration_batch_1.json, _2.json, _3.json (8 each)
- review/calibration_answers_batch_1.md, _2.md, _3.md (agent answers)
- This grading report
