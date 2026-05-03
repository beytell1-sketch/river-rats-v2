---
date: 2026-05-03
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · ML-ARCHITECT (advisory) · GTO-EXPERT (review)
re: Phase 12.5D — implement + run v9 student trainer per approved 12.5C blueprint
status: DIRECTIVE — owner approved 12.5C blueprint; 12.5D dispatched
---

# Phase 12.5D — implement + run v9 student trainer

Owner approved the 12.5C blueprint. Master HEAD now `1c14a9d` includes:

- `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` (PR #122)
- `review/comms/BUILDER_BLUEPRINT_READY_PHASE125C_2026-05-03.md` (PR #123)

The metadata-only pre-pad realization (blueprint §4) is approved as the dispatch baseline. ml-architect's "stub-trees" framing is no longer the implementation target. If ml-architect later prefers a revert to literal stub-trees for a property the blueprint hasn't surfaced, that becomes a 12.5D-internal substitution per blueprint §4.3 — does not gate this dispatch.

## LEAD-PROGRAMMER

Branch: `programmer/phase125d-trainer-impl-2026-05-XX` (XX = your start date)

### Authority chain (highest to lowest precedence)

1. This dispatch directive (operational scope, sequencing, stop conditions)
2. Blueprint PR #122 §2-§8 (module skeleton, signatures, pre-pad mechanism, ref-evaluator integration, deliverable spec) — **verbatim implementation target**
3. ml-architect PR #110 (training methodology, hyperparameters, gates) — defers to blueprint where they conflict (per pivot directive §"What stays from ml-architect's design")
4. CLAUDE.md §6 (sacred core) + §6 addendum (training provenance)

### Deliverable — exactly 4 new files in the diff

Per blueprint §8.6 Path Y discipline:

1. `river-rats-core/train_model_v9_student.py` — implementation per blueprint §2.1-§2.6 + §4 + §5
2. `river-rats-core/tests/test_train_model_v9_student.py` — per blueprint §8.2 (corpus/labels join yield + pre-pad bumped-JSON round-trip + gate_23/gate_24 hooks + solver-overlay arithmetic)
3. `river-rats-core/models/gto_model_v9_student.json` — produced model artifact from successful 5-seed run
4. `review/comms/PROGRAMMER_REPORT_PHASE125D_TRAINER_2026-05-XX.md` — trainer report per blueprint §2.4 `write_report` contract (Section A: training metadata; Section B: reference-evaluator results raw + solver-corrected per `memory/reference_corrections.md`; Section C: gate 23 feature-importance below-1% drop list; Section D: provenance hashes)

`git diff --stat` against master must show exactly these 4 files. Any edit to existing source surfaces (`gto_model.py`, `coaching/gto_model.py`, `sizing_oracle.py`, `train_model.py`, `train_sizing_model.py`, `feature_extractor.py`, `_scenario_utils.py`, `verify_feature_schema_compatibility.py`, any test file other than the new one) → **STOP** per blueprint §3 and §8.6.

### Sequencing — mandatory order

1. **Pre-flight (5 min):** verify the 22 §6 citations still hold against current master HEAD `1c14a9d`. If any drifted since `1fb0dea` was pinned by the blueprint, STOP and report. (Orchestrator already re-verified at `1fb0dea`; this is a guard against intervening commits.)
2. **Implement** trainer + tests per blueprint §2-§5. Tests must pass before any training run.
3. **R-1 dry-run (mandatory gate before 5-seed):** `python3 river-rats-core/train_model_v9_student.py --no-write-model` per blueprint §8.3. Captures the xgboost trace and verifies the metadata-only pre-pad path succeeds against the actual `gto_model_v9_3way_v2.2.json` artifact.
   - **If pre-pad succeeds:** proceed to step 4
   - **If pre-pad fails:** fall back to curriculum 45→59 per blueprint §4.4 (R-1). Re-run dry-run. Log both xgboost traces in the trainer report Section A. **Do NOT improvise a third path.**
4. **5-seed training run:** seeds 0-4, 80/20 stratified split, `multi:softprob`, hyperparameters per blueprint §2.6. Emit `gto_model_v9_student.json` from the seed with median Section B litmus score (per ml-architect §8 ensembling decision).
5. **Reference-evaluator gate:** run `gate_24_reference_evaluation` per blueprint §5.2 with baselines `[gto_model_v8_38feat.json, gto_model_v9_3way_v2.2.json]`. Apply solver-correction overlay (MW-30 CALL, MW-46 CALL, MW-47 RAISE) per `memory/reference_corrections.md`; do NOT include MW-31 / MW-50 (unverified per blueprint §5.3).
6. **Write trainer report** per blueprint §2.4 `write_report` contract.
7. **Open 12.5D PR** with the 4 files; PR title `Builder Phase 12.5D: v9 student trainer implementation + run`; PR body ≤15 lines linking blueprint PR #122, this directive, ml-architect PR #110.

### Warm-start anchor resolution — defensive guard (orchestrator addition)

Per gate-prep PR #124: `gto_model_v9_baseline_45feat.json` exists on local disk as untracked artifact (#PSH-01) but is NOT in the git-tracked tree at master HEAD `1c14a9d`. The blueprint's R-3 substitution path (default warm-start = `gto_model_v9_3way_v2.2.json`) must hold under both local-developer and CI invocation.

In `train_one_seed` warm-start anchor resolution: do NOT use `os.path.exists(baseline_45feat_path)` to decide between baseline_45feat and v9-3way-v2.2. Use a `git ls-files river-rats-core/models/gto_model_v9_baseline_45feat.json` check (or equivalent: open the file under git's tree) so an untracked local artifact does NOT silently change which warm-start anchor is used. The test in `tests/test_train_model_v9_student.py` should cover this: simulate untracked-but-on-disk; assert R-3 substitution still picks v9-3way-v2.2.

This is the only addition beyond blueprint §8 — call it the "warm-start canonicality guard."

### Stop conditions

- Any blueprint §6 citation has drifted since `1fb0dea` → STOP, report
- Pre-pad metadata-only path fails AND curriculum fallback also fails → STOP, report (this is novel territory; do NOT guess a third realization)
- 5-seed training emits any seed that fails reference-evaluator gate (`gate_24_reference_evaluation` returns < ml-architect §10 threshold for v9-3way-v2.2 baseline) → STOP, do NOT promote, report
- Any source file outside the 4-file deliverable list needs editing → STOP per blueprint §3 + §8.6
- `git diff --stat` shows >4 changed files at PR open → STOP, revert extras

### What you do NOT do

- Do NOT extend `reference_evaluator.evaluate_variants` (blueprint §5.1 — multi-call same-session aggregation only)
- Do NOT mutate `BATCH2_8_HAND_DESIGNS.md` (blueprint §5.3 — solver overlay is module-local)
- Do NOT add stub trees to the warm-start anchor (blueprint §4.1 — metadata-only is the approved realization)
- Do NOT auto-promote the model (blueprint §8 step 5 — committed but not promoted; promotion is at 12.5F owner ship gate)

## QC

**QC pre-merge audit FIRES on the 12.5D PR.** Per pivot directive §"QC". TC-23 sub-vector applies (spec-vs-infrastructure code drift) per `feedback_spec_vs_infrastructure_code_drift.md`.

Three checks:

1. **Diff scope** — exactly the 4 files listed above. Nothing else.
2. **Citation existence** — every file:line citation in the trainer module + tests + report exists on master HEAD at the time of audit (CONTENT drift + EXISTENCE drift sub-vectors, both).
3. **Provenance** — `train_model_v9_student.py:1-N` provenance docstring matches the model artifact's training metadata (CLAUDE.md §6 addendum).

Post `REVIEW_QC_PHASE125D_TRAINER_*.md`. APPROVE or HOLD.

## ML-ARCHITECT (advisory)

The 12.5D PR will surface the actual xgboost trace from the R-1 dry-run + the seed-by-seed training metadata + the reference-evaluator deltas. Read for:

- Pre-pad metadata-only realization in production (any unexpected `feature_importances_` artifacts vs blueprint §4.3 expectation)
- 5-seed variance in Section B litmus score (ml-architect §8 hyperparameter envelope still appropriate?)
- Whether the R-1 fallback fired (informs future trainer designs)

No gate vote required from ml-architect at 12.5D PR — your gate was at 12.5A (PR #110/#111). 12.5F owner ship gate is the next decision point you may be polled for.

## GTO-EXPERT (review)

12.5D PR review chain (round 12): apply your normal review pattern to the trainer report Section B (reference-evaluator results). Specifically watch for:

- Solver-correction overlay arithmetic (MW-30, MW-46, MW-47 corrections applied; MW-31, MW-50 NOT applied)
- Per-class action distribution in the v9 student vs v9-3way-v2.2 (if the new student over-folds or over-bets relative to baseline despite higher headline score, FLAG)
- Gate 23 feature-importance below-1% drop list — if any of the 4 v2.4 P1 blockers (`nut_flush_block`, `flush_draw_block_pct`, `straight_draw_block_pct`, `nut_made_block_pct`) is on the drop list, FLAG (the entire migration's value rides on these features being load-bearing)

## After 12.5D PR opens

1. QC pre-merge audit fires → APPROVE or HOLD comm
2. ml-architect + gto-expert reviews land
3. If all clear: orchestrator presents to owner for 12.5F ship gate
4. On owner ship-gate APPROVE: model is promoted to canonical (router updated, downstream consumers cut over per ml-architect §10 rollout)

## What this directive supersedes

Nothing. Pivot directive PR #119 + nudge PR #121 + blueprint PR #122 + this dispatch are the active authority chain for 12.5D.

## References

- Approved blueprint: `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` (master `1e4e47e`, PR #122)
- Pivot directive: PR #119 (master `770b897`)
- Builder nudge: PR #121 (master `1fb0dea`)
- Gate prep: PR #124 (master `aa65524`)
- ml-architect spec: PR #110 (master `291af80`); orchestrator review PR #111 (master `88e5b38`)
- Snapshot: PR #120 (master `eec5d74`) — locked premises still hold

**Status: 12.5D DISPATCHED. LEAD-PROGRAMMER named author. Branch `programmer/phase125d-trainer-impl-2026-05-XX`. Path Y discipline: 4 files exactly. Owner ship gate at 12.5F.**
