---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #253 — 12.5J-E small-sample re-train (5 seeds × 788-corpus 61-surface; mean 33.20/40 ± 0.40 solver-corrected; no-promote per builder) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #253

PR #253: `programmer/phase125j-e-small-sample-retrain-2026-05-06`. Builder report: `review/comms/BUILDER_REPORT_PHASE125J_E_SMALL_SAMPLE_RETRAIN_2026-05-06.md` (in branch). Per dispatch `MAIN_TERMINAL_PR249_RESOLUTION_AND_125JE_DISPATCH_2026-05-06.md` (master `ba678a5`, PR #252).

**Empirical result**: 5-seed sweep on 788-corpus 61-surface produces mean **33.20/40 ± 0.40 solver-corrected** vs v9-3way-v2.2 baseline **34/40** (median 33/40; 1-of-5 seed at 34/40 baseline; -1 to -0 regression range). Builder's call: NO PROMOTE per quality-default (don't ship regression). Orchestrator will accept this call on QC PASS — proceed to 12.5K design.

## Audit scope (8 items per dispatch)

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — expected files (training-output format):
   - `river-rats-core/train_*.py` or similar (training script per CLAUDE.md "Training provenance" addendum) — IF builder added a new script
   - `river-rats-core/models/v9_3way_125j_e_seed_*.json` (5 model artifacts; OR similar naming)
   - `data/inference_125j_e_reference_predictions_2026-05-06.jsonl` (or similar inference output)
   - `review/comms/BUILDER_REPORT_PHASE125J_E_SMALL_SAMPLE_RETRAIN_2026-05-06.md`
   - `review/comms/PILOT_REPORT_PHASE125J_E_2026-05-06.md` (intermediate pilot record; carry-forward audit trail)
   
   Verify NOT touched: v3.x prompts (`prompts/`), BATCH2 reference, training-data corpora (existing 788-corpus + 94-revision are READ-only training inputs; not modified), unrelated `river-rats-core/` files, plan/comm files (the merged plan stays as-is), memory files. Anything outside scope → BLOCKER per TC-X-OWNER-SCOPE-DISCIPLINE.

2. **Provenance integrity** (per CLAUDE.md "Training provenance" addendum 2026-04-15) — verify:
   - Training script docstring links the commit hash producing each model artifact
   - 5 model artifacts each have an identifiable commit-hash-to-artifact link
   - Training script lives in `river-rats-core/` (not heredoc / not inline)
   - Critical for reproducibility — any provenance gap → BLOCKER

3. **Pilot-first gate executed** (per `feedback_pilot_first_for_long_jobs.md`) — verify builder report shows:
   - Pilot 1-seed result authored first (e.g., `PILOT_REPORT_PHASE125J_E_2026-05-06.md` exists)
   - Gate decision documented (PASS to scale or HALT to orchestrator)
   - Full 5-seed run executed AFTER pilot gate cleared (timestamps in reports should reflect this sequence)
   - If pilot-first was skipped or done concurrently with full run → SHOULD_FIX (mirror PR #228 SHOULD_FIX-1 pattern); not BLOCKER

4. **5-seed aggregation correctness** — verify:
   - Per-seed table has 5 rows (seeds 0-4)
   - Median computation correct (5 values; median is 3rd-rank)
   - Std dev computation correct (5 values; sample std)
   - Builder's claim "mean 33.20/40 ± 0.40" is computed correctly from per-seed values
   - Aggregate vs per-seed predictions consistent

5. **Reference set spot-check completeness** — verify:
   - All 40 reference hands have predictions per seed (40 × 5 = 200 prediction records OR 40 rows × 5 columns)
   - All 4 stay-wrong hands (MW-17, MW-40, MW-45, MW-47) have detailed per-seed breakdowns
   - Solver-corrected reference labels applied correctly (per `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`: MW-30 CALL, MW-46 CALL, MW-47 RAISE; MW-31, MW-50 unverified per blueprint §5.3 if cited)
   - Comparison vs v9-3way-v2.2 baseline (34/40) reported per-seed and aggregate

6. **Schema integrity** — verify:
   - 788-corpus ingested cleanly (788 rows; 61-surface uniform per PR #222)
   - Inference output schema consistent with prior reference predictions (e.g., `data/inference_*.jsonl` precedent if exists)
   - All 5 trained models load + predict on reference set without errors
   - 61-feature surface used uniformly (no 45/55 surface drift)

7. **TC-X-OWNER-SCOPE-DISCIPLINE** — confirm:
   - BATCH2 reference UNCHANGED (no graduation; no label edits)
   - Reference labels NOT updated based on model predictions (model performance is observed; ground truth is fixed)
   - v3.x prompts UNCHANGED
   - 788-corpus + label files UNCHANGED (these are training inputs; READ-only)
   - No memory edits

8. **TC-X-DISPATCH-COMPLIANCE (7th formal exercise)** — verify:
   - Pilot-first executed (1-seed pilot before full run; per dispatch §"Pilot-first 1-seed gate")
   - 5 seeds (no fewer; not skipped)
   - Reference set spot-check focuses on stay-wrong (MW-17/40/45/47) per dispatch §"Reference set spot-check focus"
   - Aggregate comparison vs v9-3way-v2.2 baseline reported per dispatch
   - Builder's "NO PROMOTE" call is documented; not auto-promoted; orchestrator-scope decision route preserved
   - Builder did NOT update BATCH2 / reference labels / v3.x prompts (per dispatch §"What you do NOT do")

## Critical audit emphasis: provenance + pilot-first sequence

Items 2 and 3 are the highest-risk audit items for training-output PRs:
- Provenance gaps (item 2) make the model artifact non-reproducible → BLOCKER if any gap
- Pilot-first sequence (item 3) is a process-discipline check; if violated, FUTURE training runs at higher seed counts (e.g., 12.5K with 10+ seeds) cannot rely on builder's pilot-first discipline → SHOULD_FIX with explicit fix-forward instruction for 12.5K dispatch

QC's verdict on these gates the orchestrator's confidence in (a) accepting the no-promote call and (b) proceeding to 12.5K design.

## QC routing

Standalone stream (`~/river-rats-qc/`). Pre-merge audit (training-output milestone). ~15-20 min.

## Output

QC writes `review/comms/REVIEW_QC_PHASE125J_E_SMALL_SAMPLE_RETRAIN_2026-05-06.md` on `qc/pr253-125je-retrain-review-2026-05-06`.

## What gates on this audit

- PR #253 merge → on QC PASS
- 12.5J-F synthesis (small comm; orchestrator-scope) → on PR #253 merge
- 12.5K combined re-train design dispatch → on 12.5J-F synthesis merge (architect-hat phase)

## What you do NOT do

- Do NOT make GTO judgments on whether the model SHOULD have promoted at 33.20/40 (orchestrator-scope; quality-default is "don't ship regression" so I'll accept builder's no-promote call on QC PASS)
- Do NOT modify any file (review-only)
- Do NOT recommend promoting the model contrary to builder's call (orchestrator-scope)
- Do NOT run additional training or inference

## References

- 12.5J-E dispatch (Path 1 retrain + pilot-first gate): `MAIN_TERMINAL_PR249_RESOLUTION_AND_125JE_DISPATCH_2026-05-06.md` (master `ba678a5`, PR #252)
- 12.5J master plan: `review/comms/PLAN_PHASE125J_FEATURE_ENGINEERING_2026-05-06.md`
- CLAUDE.md "Training provenance" addendum: `review/comms/PLAN_CONSOLIDATED_2026-04-15.md` §5.1
- v9-3way-v2.2 baseline (34/40 solver-corrected): CLAUDE.md project state
- 788-corpus 61-surface (training input): `data/corpus_combined_788_2026-05-06.jsonl` (PR #222 master `48084c3`)
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_quality_default_no_ask.md`

**Status: QC stream — fire now on PR #253. Standalone audit, pre-merge, 8-item training-output scope. Items 2 (provenance) and 3 (pilot-first sequence) are the critical audits. ~15-20 min.**
