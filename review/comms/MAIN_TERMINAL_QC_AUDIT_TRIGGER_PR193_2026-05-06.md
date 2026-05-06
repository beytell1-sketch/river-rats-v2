---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #193 (12.5I-pre diagnostic; 3→12.5I, 2→12.5J; MW-25/47 reference re-eval question) at commit c7ca55c — audit-now trigger
status: TRIGGER — fire now
---

# QC pre-merge audit on PR #193 — fire now

LEAD-PROGRAMMER opened PR #193 at commit `c7ca55c` (12.5I-pre diagnostic deliverable). 1 file: per-hand diagnostic report classifying MW-17/25/40/45/47 residual types.

PR title flags 3 hands → 12.5I (D corpus), 2 hands → 12.5J (C feature engineering), plus a reference re-eval question on MW-25/MW-47.

**Audit scope:** 3 audits per `MAIN_TERMINAL_PHASE125I_PRE_DIAGNOSTIC_2026-05-06.md` (master `d366aee`, PR #192) §"QC stream — what you audit":

1. **Diff scope** — exactly 1-2 files; analysis-only; no `river-rats-core/` touches; no corpus / labels / prompt edits
2. **Citation existence** — every file:line in diagnostic report exists at master HEAD
3. **NEW: Per-hand verdict completeness** — verify all 5 hands classified with primary residual type + supporting evidence (Step 3 importance + Step 4 counterfactual at minimum) per dispatch protocol

**Audit subject:** PR #193, branch `programmer/phase125i-pre-diagnostic-2026-05-06`, commit `c7ca55c`.

Post `REVIEW_QC_PHASE125I_PRE_DIAGNOSTIC_*.md`. APPROVE or HOLD.

## Sequencing on QC verdict

- APPROVE → orchestrator merges PR #193; reads diagnostic in detail; **dispatches 12.5I (D — corpus expansion) + 12.5J (C — feature engineering) IN PARALLEL** based on per-hand verdicts
- The "MW-25/47 reference re-eval question" surfaced by builder will be incorporated into either 12.5I or 12.5J dispatch (or escalated for owner WHAT decision if the question is reference-set authority — out of orchestrator scope)
- HOLD → route findings to LEAD-PROGRAMMER for amendment

## What's blocked / what's queued

**Blocked:**
- PR #193 merge → on QC APPROVE
- 12.5I + 12.5J parallel dispatch → on PR #193 merge + orchestrator reading diagnostic

**Queued:**
- 12.5K combined re-train (after 12.5I + 12.5J ship)
- 12.5L gate evaluation (median ≥33 = PROMOTE)
- All other prior queue items

## References

- 12.5I-pre dispatch: master `d366aee` (PR #192)
- 12.5H-F synthesis: master `ea642ed` (PR #191)
- Memory: `feedback_explicit_action_trigger.md`

**Status: QC trigger posted. PR #193 ready for 3-audit sweep.**
