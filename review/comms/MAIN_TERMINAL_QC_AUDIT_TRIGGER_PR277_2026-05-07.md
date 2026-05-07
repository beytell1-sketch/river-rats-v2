---
date: 2026-05-07
from: Main terminal (orchestrator)
to: QC stream
re: PR #277 — 12.5K-C-C Lever C labelling pilot HALT (2/4 axes PASS; 2/4 FAIL on factory FD-suit configuration) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #277

PR #277: `programmer/phase125k-c-c-labelling-2026-05-07`. Builder report at `review/comms/BUILDER_REPORT_PHASE125K_C_C_LABELLING_PILOT_HALT_2026-05-07.md` (in branch). Per dispatch `MAIN_TERMINAL_PR273_RESOLUTION_AND_125KCC_DISPATCH_2026-05-07.md` (master `6fab0d7`, PR #276).

**Empirical result**: Per-axis pilot 5-hand × 5-Sonnet:
- MW-40 (target BET): 5/5 unanimous BET → PASS
- MW-45 (target RAISE): 5/5 unanimous RAISE → PASS
- MW-17 (target CALL): 0/5 ≥4/5 CALL → FAIL (4/5 hands FOLD)
- MW-47 (target RAISE): 0/5 ≥4/5 RAISE → FAIL (mix CALL/FOLD)

**Builder diagnosis**: MW-17 + MW-47 factory boards have only 1 FD-suit board card (`has_flush_draw=0` per labelling pipeline; requires 2 board cards of FD suit). KB §1.7 nut-FD carve-out doesn't trigger; labellers default to FOLD/CALL on equity-vs-pot-odds. **This is a factory configuration bug**, NOT a labelling pipeline divergence.

Cost saved by HALT: ~$30-40 (full run skipped on all 4 axes).

## Audit scope (8 items HALT-partial format)

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — expected 3 files (script + 100 pilot labels + report). Verify NOT touched: v3.x prompts, BATCH2, river-rats-core/, training-data, corpus_lever_c_situations, plan/comm/memory.

2. **Pilot label integrity** — 100 labels (5 hands × 4 axes × 5 labellers) well-formed; reasoning text per label.

3. **Reasoning convergence per axis** — for the 2 PASS axes (MW-40, MW-45): convergent reasoning citing v3.4 protocol. For the 2 FAIL axes (MW-17, MW-47): convergent FOLD/CALL reasoning citing equity-vs-pot-odds + `has_flush_draw=0` (NOT mode collapse; the divergence from prediction is consistent with builder's factory-bug diagnosis).

4. **Factory FD-suit diagnosis verification** — verify builder's claim: inspect 5 pilot situations from MW-17 + MW-47 axes; confirm board has only 1 FD-suit card; confirm `has_flush_draw=0` in feat_dict. If diagnosis correct → factory bug confirmed; not a labelling pipeline issue.

5. **No solver-as-labels** — labels cite v3.4 protocol rules.

6. **Per-hand consensus computation** — per-axis aggregate: 5 hands × 5 labellers = 25 per axis × 4 = 100 total. Math correct.

7. **TC-X-OWNER-SCOPE-DISCIPLINE** — no v3.x / BATCH2 / corpus_lever_c_situations / plan / memory edits.

8. **TC-X-DISPATCH-COMPLIANCE 13th formal exercise** — per-axis pilot-first executed; per-axis gate decisions documented; no auto-fix on FAIL axes; orchestrator-scope decision route preserved (Path 1 / 2 / 3 surfaced for orchestrator).

## Critical audit emphasis

Item 4 (factory FD-suit diagnosis) is the critical audit item. If builder's diagnosis is wrong, the partial HALT might mask a deeper labelling pipeline issue. QC's verification of the diagnosis gates the orchestrator's path decision.

## QC routing

Standalone stream. Pre-merge audit. ~10-15 min.

## Output

QC writes `review/comms/REVIEW_QC_PHASE125K_C_C_LABELLING_PILOT_HALT_2026-05-07.md` on `qc/pr277-125kcc-pilot-review-2026-05-07`.

## What gates on this audit

- PR #277 merge → on QC PASS
- Path 1 / 2 / 3 selection → on QC PASS + diagnosis confirmation

## What you do NOT do

- Do NOT make GTO judgments on whether 4/5 FOLD on MW-17 is "correct" (the empirical result is what it is; the question is WHY it diverged from prediction)
- Do NOT modify any file
- Do NOT recommend specific path (orchestrator-scope; QC verifies diagnosis only)

## References

- 12.5K-C-C dispatch: `MAIN_TERMINAL_PR273_RESOLUTION_AND_125KCC_DISPATCH_2026-05-07.md` (master `6fab0d7`, PR #276)
- v3.4 KB §1.7 (nut-FD carve-out): `prompts/gto_labeller_v3.4.md`
- 12.5I-MW40-VERIFICATION-C precedent (HALT pattern): `BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_C_PILOT_HALT_2026-05-06.md`

**Status: QC stream — fire now on PR #277. HALT-partial audit, ~10-15 min. Critical: item 4 (factory diagnosis verification).**
