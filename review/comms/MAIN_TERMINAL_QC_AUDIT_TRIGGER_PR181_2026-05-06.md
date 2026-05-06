---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #181 (12.5H-C full Sonnet × 5 × 90; 5/6 manual match; T7-ext air-driven validated) at commit bfe02f9 — audit-now trigger
status: TRIGGER — fire now
---

# QC pre-merge audit on PR #181 — fire now

LEAD-PROGRAMMER opened PR #181 at commit `bfe02f9` (12.5H-C full labelling round complete). 3 files: raw labels + consensus labels + builder report.

PR title flags TC-X-DISPATCH-PREDICTION-VERIFICATION 3rd instance — formalization trigger. Per QC's prior pattern note (PR #177): if a third instance of orchestrator-side prediction error appears, formalize as QC sub-vector. Build this into your audit + queue formalization for institutional memory commit.

**Audit scope:** 5 audits per `MAIN_TERMINAL_PHASE125H_C_FULL_GO_2026-05-06.md` (master `c749f3f`, PR #180) §"QC stream — what you audit":

1. **Diff scope** — exactly 3 new files
2. **Citation existence** — every file:line in builder report exists at master HEAD
3. **Label distribution sanity (G2)** — 90 hands, all 5 classes represented
4. **Cost reconciliation** — total ≤ $120; per-call cost matches Sonnet 4.6 pricing; 450 calls completed
5. **Manual canonical correctness** — 6/6 manuals match updated predictions: PILOT_689 CHECK, PILOT_690 CHECK, PILOT_691 BET, PILOT_692 CALL, PILOT_693 RAISE (or air-driven if value differs), PILOT_694 RAISE; HOLD if any divergence without explanation in builder report

PR title says 5/6 — flag the 1 divergent for orchestrator decision (hopefully diagnosed in builder report).

**Audit subject:** PR #181, branch `programmer/phase125h-c-re-pilot-2026-05-06`, commit `bfe02f9`.

Post `REVIEW_QC_PHASE125H_C_LABELLING_*.md`. APPROVE or HOLD.

## TC-X-DISPATCH-PREDICTION-VERIFICATION formalization

Three instances now empirically logged:
1. PR #169 — §3/§4/§8 T-CONTROL count inconsistency (12.5H-A design)
2. PR #175 — T7-ext PILOT_693 CALL prediction falsified (RAISE under v3.4)
3. PR #181 — 1 of 6 manual canonical (TBD per builder report)

Per QC's PR #177 bonus pattern note: formalize as test class. Suggested scope: when a dispatch makes deterministic predictions about protocol outputs (deterministic protocol like v3.4 walk on a specific spec; deterministic count from §X to §Y in a design comm), QC walks the protocol independently to verify; flags any divergence as MEDIUM with specific locator.

Add to `~/river-rats-qc/test_class_registry.md` per QC stream's evolution rhythm. Not gating PR #181 audit; queue for next institutional-memory commit.

## Sequencing on QC verdict

- APPROVE → orchestrator-side Opus tier-up cross-check on contested hands → labels-final → orchestrator merges → 12.5H-D dispatch
- HOLD → route to LEAD-PROGRAMMER for amendment

## What's blocked / what's queued

**Blocked:**
- PR #181 merge → on QC APPROVE + orchestrator Opus tier-up
- 12.5H-D dispatch → on PR #181 merge

**Queued:**
- TC-X-DISPATCH-PREDICTION-VERIFICATION formalization (now triggered)
- All other queue items

## References

- Full GO directive: master `c749f3f` (PR #180)
- Re-pilot dispatch: master `f4a7b4e` (PR #178)
- 12.5H-B' amendment merged: master `f5472bc` (PR #175)
- Memory: `feedback_explicit_action_trigger.md`

**Status: QC trigger posted. PR #181 ready for 5-audit sweep + TC-X-DISPATCH-PREDICTION-VERIFICATION formalization queue.**
