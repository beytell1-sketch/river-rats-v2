---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #261 — 12.5K-A Lever A more-seeds (20-seed mean 33.10/40 ± 0.30; variance-bound finding confirmed) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #261

PR #261: `programmer/phase125k-a-more-seeds-2026-05-06`. Builder report at `review/comms/BUILDER_REPORT_PHASE125K_A_MORE_SEEDS_2026-05-06.md` (in branch). Per dispatch `MAIN_TERMINAL_PR257_RESOLUTION_AND_125KA_DISPATCH_2026-05-06.md` (master `44089bb`, PR #260).

**Empirical result**: 20-seed aggregate (5 existing seeds 0-4 from PR #253 + 15 new seeds 5-19 from this PR) → **mean 33.10/40 ± 0.30 solver-corrected** vs baseline 34/40. Tighter std than the 5-seed pilot (0.30 vs 0.40). Per outcome matrix: **variance-bound finding** (mean stays ≈ 33.20/40 ± 0.40 within tighter envelope; not at-or-above baseline within 1-σ). On QC PASS, orchestrator proceeds to Lever B (hyperparameter sweep).

## Audit scope (8 items per dispatch; mirror PR #253 audit)

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — expected:
   - 15 new model artifacts in `river-rats-core/models/125k_a/v9_3way_125k_a_seed_5..19.json`
   - Inference output (e.g., `data/inference_125k_a_reference_predictions_2026-05-06.jsonl`)
   - `review/comms/BUILDER_REPORT_PHASE125K_A_MORE_SEEDS_2026-05-06.md`
   - Optionally minor training-orchestration script (per CLAUDE.md provenance)
   
   Verify NOT touched: v3.x prompts, BATCH2, training-data corpora (READ-only training inputs), unrelated `river-rats-core/`, plan/comm files, memory.

2. **Provenance integrity** — 15 new model artifacts each have commit-hash-to-artifact docstring link per CLAUDE.md addendum.

3. **Pilot 2-seed gate executed** — builder report shows 2-seed pilot (Seeds 5+6) result + gate decision before scaling to remaining 13 (Seeds 7-19).

4. **20-seed aggregation correctness** — math correct:
   - 20 per-seed solver-corrected scores
   - Mean computation correct (claim: 33.10/40)
   - Std computation correct (claim: ±0.30)
   - 20-seed claim verifies against per-seed values

5. **Reference set spot-check completeness** — 40 hands × 20 seeds = 800 predictions. All 4 stay-wrong hands (MW-17, MW-40, MW-45, MW-47) have detailed per-seed breakdowns. Verify any seed flips any stay-wrong (per builder claim "All 4 stay-wrong continue to diverge across all 20 seeds at the model layer").

6. **Variance characterization conclusion** — builder report's conclusion section maps the empirical result to the 3-case outcome matrix (PROMOTE / variance-bound / negative). Builder's "variance-bound" call should be backed by:
   - Mean (33.10) < baseline (34) by ≥ 1-σ (0.30 std × 1 = 0.30; 33.10 + 0.30 = 33.40 < 34) → not at-or-above baseline within 1-σ → variance-bound (not PROMOTE)
   - Mean ≥ 33.0 (not negative) → not negative
   - Therefore: variance-bound is correct call

7. **TC-X-OWNER-SCOPE-DISCIPLINE** — BATCH2 unchanged; reference labels NOT updated; hyperparameters unchanged from PR #253; warm-start anchor unchanged (gto_model_v9_3way_v2.2.json).

8. **TC-X-DISPATCH-COMPLIANCE (9th formal exercise)** — pilot 2-seed gate executed; 15 new seeds (no fewer; not skipped); same config as PR #253 (no hyperparameter drift; no warm-start change); 20-seed aggregate vs baseline reported; orchestrator-scope decision route preserved (builder did NOT auto-promote).

## Critical audit emphasis

Items 2 (provenance) + 4 (20-seed aggregation math) gate orchestrator confidence in the empirical conclusion. The variance-bound finding has implications for Lever B/C dispatch sequencing — if the math is wrong, the wrong lever fires next.

## QC routing

Standalone stream (`~/river-rats-qc/`). Pre-merge audit. ~15-20 min.

## Output

QC writes `review/comms/REVIEW_QC_PHASE125K_A_MORE_SEEDS_2026-05-06.md` on `qc/pr261-125ka-review-2026-05-06`.

## What gates on this audit

- PR #261 merge → on QC PASS
- 12.5K-B Lever B (hyperparameter sweep) dispatch → on PR #261 merge AND variance-bound outcome confirmed by QC math (item 4 + item 6)
- (PROMOTE outcome would dispatch 12.5L gate eval directly; not the case here)

## What you do NOT do

- Do NOT make GTO judgments on whether the model SHOULD have promoted (orchestrator-scope; "variance-bound" empirical reading is what matters; the math is fixed)
- Do NOT modify any file (review-only)
- Do NOT recommend a different lever sequence (orchestrator-scope; per dispatch §"Sequencing")
- Do NOT run additional inference

## References

- 12.5K-A dispatch (Lever A; 15 new seeds; 2-seed pilot gate): `MAIN_TERMINAL_PR257_RESOLUTION_AND_125KA_DISPATCH_2026-05-06.md` (master `44089bb`, PR #260)
- PR #253 (12.5J-E source data; 5-seed mean 33.20/40 ± 0.40): master `2b6aa02`
- 12.5K master plan §3 (Lever A spec + outcome matrix): `review/comms/PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md` (PR #257 master `9798007`)
- v9-3way-v2.2 baseline: 34/40 solver-corrected (CLAUDE.md project state)
- CLAUDE.md "Training provenance" addendum: `review/comms/PLAN_CONSOLIDATED_2026-04-15.md` §5.1
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: QC stream — fire now on PR #261. Standalone audit, pre-merge, 8-item training-output scope. Items 2 + 4 + 6 are the critical audits. ~15-20 min.**
