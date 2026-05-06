---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #218 — BATCH2 MW-25 graduation update (Decision 2α; doc + memory edits) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #218

PR #218: `programmer/batch2-mw25-graduation-update-2026-05-06`. Builder report at `review/comms/BUILDER_REPORT_BATCH2_MW25_GRADUATION_2026-05-06.md`. 4 files edited + 1 report (5 in diff). Cost: $0 (text edits). Continues `MAIN_TERMINAL_PR213_DECISIONS_AND_DISPATCH_2026-05-06.md` § "LEAD-PROGRAMMER — Step 1".

## Audit class — TC-X-OWNER-SCOPE-DISCIPLINE (NEW; first formal use)

This is the first PR formalized under the new TC-X-OWNER-SCOPE-DISCIPLINE class observed in QC's PR #213 audit (where it noted "Worth promoting to a standing TC-X test class for any data PR that surfaces graduation evidence"). Reference-set updates are owner-scope per `feedback_orchestrator_decides_not_recommends.md`; this audit verifies the diff stays strictly within the orchestrator-authorized scope.

## Audit scope (4 items)

1. **Diff scope strict** — exactly these 4 files (+ 1 builder report):
   - `design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md` (canonical reference label location per `reference_evaluator._parse_gto_table`)
   - `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` (annotation + redirect note; canonical label lives in RANGE_ANALYSIS.md)
   - `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` (new "Empirically Corrected Reference Labels" section + MW-25 entry)
   - `review/RESTART_PROMPT_V9_3WAY.md` (stay-wrong list 5→4; MW-25 row removed; MW-40 annotated as graduation candidate)
   
   **Verify NOT touched:** `prompts/gto_labeller_v3.4.md`, any `data/corpus_*.jsonl`, any `river-rats-core/` source, any v3.x prompt files. Anything outside scope → BLOCKER per TC-X-OWNER-SCOPE-DISCIPLINE.

2. **Citation existence** — BATCH2_8_RANGE_ANALYSIS.md MW-25 entry's new reasoning cites the 4 evidence sources (PR #208 / PR #209 / PR #213 / v3.4 protocol traces) by PR # and confidence level. reference_corrections.md entry follows the existing format (table row + detail block) consistent with the solver-corrected section above it.

3. **Canonical label correctness** — verify the new MW-25 label in BATCH2_8_RANGE_ANALYSIS.md is `CHECK HIGH` (not just CHECK; HIGH confidence preserved per Opus + 30/30 unanimous). Verify the GTO Action Table row at line 27 matches the detail section at line 383 (no inconsistency between summary and detail).

4. **Stay-wrong list integrity** — verify RESTART_PROMPT_V9_3WAY.md:
   - MW-25 entry removed from "5 True Remaining Failures" table
   - Header updated to "4 True Remaining Failures"
   - Graduation note added with date + evidence link
   - MW-40 entry annotated as "graduation candidate per Decision 3β (12.5I-MW40-VERIFICATION queued)"
   - No other stay-wrong entries silently modified

## QC routing

Standalone stream (`~/river-rats-qc/`) per `feedback_qc_routing_when_standalone_active.md`. Pre-merge audit (this is a milestone owner-scope reference-set update). Expected duration: ~5-10 min (small diff, focused scope).

## Output

QC writes `review/comms/REVIEW_QC_BATCH2_MW25_GRADUATION_2026-05-06.md` on `qc/pr218-batch2-mw25-review-2026-05-06` branch. PR opens. Verdict: PASS / ISSUES FOUND / FAIL.

## What gates on this audit

- PR #218 merge → on QC PASS (no Opus tier-up needed; doc + memory update, not training-data per `feedback_pilot_first_for_long_jobs.md` sub-rule)
- 12.5I-D corpus QC dispatch → on PR #218 merge
- 12.5I-MW40-VERIFICATION-A design dispatch → on PR #218 merge (sequenced after 12.5I-D in builder serial)
- 12.5J-D-pre test-guard deflake → tail of queue

## What you do NOT do

- Do NOT make GTO judgments on whether the new CHECK HIGH label is correct (4-source convergence + Opus HIGH already established in PR #209 + PR #213; QC verifies *evidence chain integrity*, not GTO truth)
- Do NOT modify any file (review-only)
- Do NOT recommend further reference-set changes (those are owner-scope; orchestrator surfaces if needed)

## References

- PR #213 (12.5I-C labelling, 30/30 T8'-r CHECK evidence): master `994ae67`
- PR #215 (QC PASS verdict on PR #213): master `c2021e7`
- PR #209 (Opus 4.7 MW-25 re-eval): master `077c168`
- PR #208 (12.5I-C pilot 5/5 CHECK): master `52e5164`
- PR #217 (orchestrator decisions + Step 1 dispatch): master `d6912ad`
- PR #216 (BORDERLINE-17 HALT comm with 3 decisions): master `8f92223`
- BATCH2 reference (canonical label location): `design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md`
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_spec_vs_infrastructure_code_drift.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_explicit_action_trigger.md`

**Status: QC stream — fire now on PR #218. Standalone audit, pre-merge, owner-scope-discipline class. ~5-10 min.**
