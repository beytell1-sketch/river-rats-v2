---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #257 — 12.5K combined re-train DESIGN (architect-hat; 3-lever analysis A → B → C; ~$85/~9.5h capped) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #257

PR #257: `programmer/phase125k-combined-retrain-design-2026-05-06`. Plan: `review/comms/PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md` (in branch). Per dispatch `MAIN_TERMINAL_PR253_RESOLUTION_AND_125K_DESIGN_DISPATCH_2026-05-06.md` (master `4e55ff4`, PR #256).

Builder reports total budget ~$85 / ~9.5h — well under the ~$300/~30h auto-approval cap. Sequence proposed: Lever A (more seeds) → Lever B (hyperparameters) → Lever C (augmented data). Architect-hat design phase; no execution.

## Audit scope (7 items per dispatch)

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — exactly 1 file (`PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md`) + optional supporting analysis files in `review/comms/`. Verify NOT touched: v3.x prompts, BATCH2, river-rats-core/, training-data, existing corpora, models. Anything outside scope → BLOCKER per TC-X-OWNER-SCOPE-DISCIPLINE.

2. **All 3 levers analyzed** — Lever A (more seeds; variance characterization) + Lever B (hyperparameters; CV-driven sweep) + Lever C (augmented data; further labelling) each have dedicated analysis section per dispatch §3-§5. Single-lever-only plan = SHOULD_FIX (mirror PR #228 SHOULD_FIX-1 pattern).

3. **Sequenced recommendation present** — plan §6 explicitly sequences levers with gates between them. Single-lever-only or no-sequencing plan = SHOULD_FIX. Builder's PR title indicates A → B → C sequence; QC verifies the plan body backs that with reasoning + per-lever gate criteria.

4. **Pilot-first gates per lever** — each lever has explicit pilot-first scope. Per dispatch §3-§5 builder must specify "2-3 configs/seeds/hands first, gate, then scale to remaining" per lever. Missing pilot-first plan for any lever = SHOULD_FIX.

5. **Cost + time budget realistic** — per-lever sub-totals add to plan total; total ≤$300 LLM / ≤30h wall clock auto-approved. Builder's claim ~$85 / ~9.5h ≪ caps → automatic. Verify the math: per-lever sub-totals reasonable, no hidden costs.

6. **TC-X-OWNER-SCOPE-DISCIPLINE + solver-as-labels prohibition** — plan does NOT recommend training against reference set; plan does NOT propose solver-as-labels for any new labelling round; plan does NOT propose BATCH2/v3.x edits. Reference-set labels treated as IMMUTABLE ground truth (not training target). Solver may be cited descriptively but never as label-source.

7. **TC-X-DISPATCH-COMPLIANCE (8th formal exercise)** — verify:
   - Design-only (no execution code, no model training, no factory output)
   - 1 file in PR (+ optional analysis)
   - Methodology rules cited (cross-seed importance, cap-binding, tier-up, pilot-first, hero-only if applicable, pre-flight join-cardinality)
   - Stop conditions per dispatch listed
   - "What this PR does NOT do" section per dispatch
   - Risks + open questions for orchestrator section per `feedback_orchestrator_decides_not_recommends.md`

## Critical audit emphasis

This is a strategic design phase. Items 2 (all-3-levers analyzed) + 3 (sequenced recommendation with gates) + 4 (pilot-first per lever) gate orchestrator confidence in dispatching 12.5K-A execution. If any of these are weak, the empirical 12.5K work risks pursuing the wrong lever sequence.

## QC routing

Standalone stream (`~/river-rats-qc/`). Pre-merge audit. ~10-15 min.

## Output

QC writes `review/comms/REVIEW_QC_PHASE125K_COMBINED_RETRAIN_DESIGN_2026-05-06.md` on `qc/pr257-125k-design-review-2026-05-06`.

## What gates on this audit

- PR #257 merge → on QC PASS
- 12.5K-A execution dispatch (specific lever per builder's recommended sequence; likely Lever A more-seeds first) → on PR #257 merge
- Subsequent 12.5K-B / -C / -D / -E execution → each fires on prior lever gate per builder's plan
- 12.5L gate evaluation → on full 12.5K sweep complete

## What you do NOT do

- Do NOT make GTO judgments or strategic-design judgments on which lever is "best" — that's the architect-hat builder's call; QC verifies the plan structure is sound
- Do NOT modify any file (review-only)
- Do NOT recommend a different lever sequence (orchestrator-scope)
- Do NOT run additional inference

## References

- 12.5K design dispatch: `MAIN_TERMINAL_PR253_RESOLUTION_AND_125K_DESIGN_DISPATCH_2026-05-06.md` (master `4e55ff4`, PR #256)
- 12.5J master plan: `review/comms/PLAN_PHASE125J_FEATURE_ENGINEERING_2026-05-06.md`
- 12.5I-A design precedent: `review/comms/PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md`
- 12.5J-E source data (the empirical neutral result): PR #253 (master `2b6aa02`)
- v9-3way-v2.2 baseline (34/40 solver-corrected): CLAUDE.md project state
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_quality_default_no_ask.md`

**Status: QC stream — fire now on PR #257. Standalone audit, pre-merge, 7-item design-phase scope. ~10-15 min.**
