---
date: 2026-05-07
from: Main terminal (orchestrator)
to: QC stream
re: PR #269 — 12.5K-C-A Lever C design (4-axis augmented data; per-axis pilot-first + off-ramp; ~$65-100 / ~4-6h capped) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #269

PR #269: `programmer/phase125k-c-a-augmented-data-design-2026-05-07`. Plan: `review/comms/PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md` (in branch). Per dispatch `MAIN_TERMINAL_PR265_RESOLUTION_AND_125KCA_DISPATCH_2026-05-07.md` (master `1292233`, PR #268).

Builder reports design complete in ~4 min (well under 30-45 min estimate); architect-hat plan for 4-axis augmented data labelling round (MW-17, MW-40, MW-45, MW-47) with per-axis pilot-first 5-hand gate + off-ramp.

## Audit scope (7 items per dispatch)

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — exactly 1 file (`PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md`) + optional analysis. Verify NOT touched: v3.x prompts, BATCH2, river-rats-core/, training-data, existing corpora, models, memory.

2. **All 4 stay-wrong axes covered** — MW-17 (under-calling) + MW-40 (under-CHECKing per BET MEDIUM canonical; verified via MW-40-VERIFICATION graduation-fail) + MW-45 (under-raising) + MW-47 (shared blind spot; solver-corrected RAISE). Missing axis = SHOULD_FIX.

3. **Per-axis pilot-first 5-hand gate specified** — each axis has explicit pilot-first scope with PASS/FAIL/REPORT criteria. Missing = SHOULD_FIX.

4. **Per-axis structural prediction documented** — pilot expected action per axis matches stay-wrong canonical/solver-corrected (CALL for MW-17; BET for MW-40; RAISE for MW-45 and MW-47). Verify alignment with PR #245 finding (MW-40 BET MEDIUM is the labelling-pipeline-empirical answer; not CHECK).

5. **Methodology rules cited** — all 7 standing per 12.5I-A precedent (cross-seed importance NOT applicable; cap-binding pre-flight; tier-up verification plan; pilot-first; hero-only convention; pre-flight join-cardinality; design_action per T-CONTROL).

6. **TC-X-OWNER-SCOPE-DISCIPLINE** — confirm no v3.x / BATCH2 / corpus / source / memory edits in scope.

7. **TC-X-DISPATCH-COMPLIANCE (11th formal exercise)** — design-only (no execution); 1 file; per-axis off-ramp specified per dispatch §"Per-axis pilot-first 5-hand gate"; ref_id namespace `PILOT_LEVER_C_<AXIS>_001..050` per axis; total cost/time within $300/30h cap.

## QC routing

Standalone stream (`~/river-rats-qc/`). Pre-merge audit. ~10-15 min.

## Output

QC writes `review/comms/REVIEW_QC_PHASE125K_C_A_LEVER_C_DESIGN_2026-05-07.md` on `qc/pr269-125kca-design-review-2026-05-07`.

## What gates on this audit

- PR #269 merge → on QC PASS
- 12.5K-C-B situation generation dispatch → on PR #269 merge

## What you do NOT do

- Do NOT make GTO judgments on which axis is "best"
- Do NOT modify any file (review-only)
- Do NOT recommend a different axis count or different per-axis hand count (orchestrator-scope)
- Do NOT run inference

## References

- 12.5K-C-A dispatch: `MAIN_TERMINAL_PR265_RESOLUTION_AND_125KCA_DISPATCH_2026-05-07.md` (master `1292233`, PR #268)
- 12.5K master plan §5 (Lever C high-level): `review/comms/PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md`
- 12.5I-MW40-VERIFICATION precedent (5-phase mini-pipeline pattern): `review/comms/PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md`
- PR #245 (MW-40 graduation-fail; BET MEDIUM canonical confirmed): master `877555a`
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_findings.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: QC stream — fire now on PR #269. Standalone audit, pre-merge, 7-item design-phase scope. ~10-15 min.**
