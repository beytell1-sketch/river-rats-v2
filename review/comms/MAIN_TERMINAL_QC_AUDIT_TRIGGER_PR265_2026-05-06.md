---
date: 2026-05-07
from: Main terminal (orchestrator)
to: QC stream
re: PR #265 — 12.5K-B Lever B pilot 3-config sweep (hyperparameter-bound finding; spread 0.20 hands; outcome matrix row 3 → Lever C) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #265

PR #265: `programmer/phase125k-b-hyperparameter-sweep-2026-05-06`. Builder report: `review/comms/BUILDER_REPORT_PHASE125K_B_HYPERPARAMETER_SWEEP_2026-05-06.md` (in branch). Per dispatch `MAIN_TERMINAL_PR261_RESOLUTION_AND_125KB_DISPATCH_2026-05-06.md` (master `bc7d08b`, PR #264).

**Empirical result**: Builder ran the pilot 2-3 config sweep and observed spread 0.20 hands across the configs — falling within the dispatch's pilot gate REPORT condition ("All 2-3 pilot configs show CV mean within 0.2 hand of baseline → REPORT (not STOP); orchestrator decides whether sweep is worth scaling"). Builder correctly halted at pilot gate, surfaced for orchestrator decision. Per outcome matrix row 3 (no improvement / hyperparameter-bound) → **proceed to Lever C (augmented data)** without scaling Lever B further.

**Quality-default rationale**: spread of 0.20 hands across 3 representative configs is well below the threshold of meaningful improvement. Scaling to 50-200 configs would consume ~10-15 hours at this signal level — disproportionate cost for unlikely lift. Halting at pilot is the slow-quality choice (don't waste budget on diminishing returns).

## Audit scope (8 items per dispatch; HALT-format)

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — expected files (HALT-format; partial sweep):
   - `river-rats-core/sweep_125k_b_hyperparameter.py` (sweep orchestration script with provenance)
   - `data/sweep_125k_b_pilot_results_2026-05-06.jsonl` (pilot 3-config CV results; partial sweep only)
   - `river-rats-core/models/125k_b/pilot_*.json` (3 pilot model artifacts × CV folds)
   - `review/comms/BUILDER_REPORT_PHASE125K_B_HYPERPARAMETER_SWEEP_2026-05-06.md`
   
   Verify NOT touched: v3.x prompts, BATCH2, training-data corpora (READ-only), unrelated `river-rats-core/`, plan/comm files, memory.

2. **Provenance integrity** — sweep script + 3 pilot configs each have commit-hash docstring link.

3. **Pilot 2-3 config gate executed correctly** — builder ran 3 configs (per dispatch §"Pilot-first 2-3 configs gate"); evaluated spread; gate decision documented. NO scaling to full sweep occurred (per builder's halt-at-pilot decision).

4. **CV discipline correct** — 5-fold stratified CV INTERNAL to 788-corpus (NOT against reference set). Per-config 5 fold measurements aggregated.

5. **No reference-set training** — sweep used CV folds INTERNAL only; reference set untouched as training target.

6. **No solver-as-labels** — sweep evaluation does not cite solver outputs as label authority.

7. **Outcome interpretation correct** — builder's "hyperparameter-bound" call should be backed by:
   - Spread across 3 configs = 0.20 hands (per builder claim)
   - Per dispatch outcome matrix row 3 ("No improvement / hyperparameter-bound"): "Mean ≈ 33.10/40 ± 0.30 (no improvement vs Lever A)"
   - Builder's call is consistent with the matrix
   - Orchestrator-scope decision route preserved (builder did NOT auto-decide Lever C dispatch; surfaces for orchestrator)

8. **TC-X-DISPATCH-COMPLIANCE (10th formal exercise)** — pilot-first executed; halt-at-pilot decision is per dispatch ("REPORT, not STOP"); orchestrator-scope outcome decision preserved; no auto-scaling to full sweep.

## QC routing

Standalone stream (`~/river-rats-qc/`). Pre-merge audit. ~10-15 min (HALT-format with partial sweep is shorter than full-sweep audit).

## Output

QC writes `review/comms/REVIEW_QC_PHASE125K_B_HYPERPARAMETER_SWEEP_2026-05-06.md` on `qc/pr265-125kb-review-2026-05-06`.

## What gates on this audit

- PR #265 merge → on QC PASS
- 12.5K-C Lever C (augmented data) dispatch → on PR #265 merge AND hyperparameter-bound finding confirmed by QC (item 7)

## What you do NOT do

- Do NOT make GTO judgments
- Do NOT modify any file (review-only)
- Do NOT recommend scaling the sweep further (orchestrator-scope; per quality-default the halt-at-pilot is correct)
- Do NOT run additional inference

## References

- 12.5K-B dispatch: `MAIN_TERMINAL_PR261_RESOLUTION_AND_125KB_DISPATCH_2026-05-06.md` (master `bc7d08b`, PR #264)
- 12.5K master plan §4 (Lever B spec): `review/comms/PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md`
- PR #261 (Lever A 20-seed mean 33.10/40 ± 0.30; baseline for B comparison): master `edf04a6`
- v9-3way-v2.2 baseline: 34/40 solver-corrected
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md` (halt-at-pilot is slow-quality), `feedback_solver_vs_expert_labels.md`

**Status: QC stream — fire now on PR #265. Standalone audit, pre-merge, 8-item HALT-format scope. ~10-15 min.**
