---
date: 2026-05-09
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #322 — Phase 1.5-C execution (5-seed re-train at 59-surface; §3.4 PASS gate cleared) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #322

PR #322: `programmer/phase15c-3way-verification-2026-05-09`. Head `45a5afb4a34c01435fe7d8f4ea7e54ca22b0ca03`. Title: "Builder Phase 1.5-C: 3-way verification at 59-surface — §3.4 PASS gate cleared (mean 33.00/40 ± 0.00; J-B drop verified non-regressive)".

Builder fired Phase 1.5-C per dispatch `MAIN_TERMINAL_PHASE15C_EXECUTION_DISPATCH_2026-05-09.md` (master `c8138a1`, PR #320) + re-poke `MAIN_TERMINAL_BUILDER_FIRE_NOW_REPOKE_PR320_2026-05-09.md` (master `aa26ae4`, PR #321).

**Diff summary** (per `gh pr view 322`): 2 files / +286:
- `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` — median seed canonical model (force-added)
- `review/comms/BUILDER_REPORT_PHASE15C_2026-05-09.md` — execution log + per-seed scores + PASS gate decision + failure-direction classification

**Title claim**: §3.4 PASS gate cleared at mean 33.00/40 ± 0.00 (matches PR #293 12.5K-C-E precedent exactly; J-B drop verified non-regressive).

Pre-merge QC required per `feedback_qc_required_before_approval.md` (verification result feeds 1.5-D HU retrain decisions; milestone-class).

## Audit scope (~15-20 min; 10-item per dispatch §"QC stream")

Per dispatch `MAIN_TERMINAL_PHASE15C_EXECUTION_DISPATCH_2026-05-09.md` §"QC stream — what you audit":

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): 2 PR files only — model jsonl + builder report. NO source / data / prompt edits.
2. **TC-23 EXISTENCE git-tracked check** per `feedback_tc23_existence_must_be_git_tracked.md`: `git ls-files river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` returns non-empty (force-added, NOT .gitignored). Other cited paths (corpus, warm-start, hyperparameters) exist at master HEAD pre-merge.
3. **§3.4 PASS gate adjudication**: builder report's mean ≥ 33.00 across 5 seeds; QC verifies the per-seed scores + the mean. Title claims 33.00 ± 0.00 — verify per-seed scores actually match this aggregate.
4. **Failure-direction classification format compliance** (§3.4 + `feedback_failure_direction_classification.md`): per-hand miss table with U/O/C axis present; direction summary present; direction-skewed regression check applied. Title says "J-B drop verified non-regressive" — verify the failure-direction analysis substantiates this against 12.5K-C-E precedent's stay-wrong taxonomy MW-17/40/45/47.
5. **Pre-pad warm-start canonicality**: builder report shows `is_git_tracked('models/gto_model_v9_3way_v2.2.json')` returned True at run time; warm-start booster path correct.
6. **Hyperparameter inheritance compliance**: builder report shows `_HYPERPARAMETERS` from `train_model_v9_student.py:139-154` used verbatim; no env-var overrides (`RR_HP_*` unset); confidence weighting `pure`; class-weight cap 3.0.
7. **Pilot smoke result**: builder report includes 1-seed smoke completion + score within 5 points of 12.5K-C-E precedent.
8. **Promoted model spec**: median seed identified; SHA-256 logged; force-added to git per `feedback_tc23_existence_must_be_git_tracked.md`.
9. **TC-X-DISPATCH-COMPLIANCE**: 6-step sequence + STOP conditions + negative scope all honored.
10. **Methodology rule cross-check**: failure-direction per `feedback_failure_direction_classification.md`; postflop-composition per `feedback_preflop_geometry_vs_postflop_composition.md`; close-hand selection per `feedback_close_hand_selection.md`; solver-vs-labels per `feedback_solver_vs_expert_labels.md` (no solver labels in training).

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~15-20 min wall-clock. QC writes:
- `~/river-rats-qc/findings/2026-05-09-pr322-phase15c-execution.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15C_EXECUTION_2026-05-09.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha` to current master per `project_qc_heartbeat_convention.md`

## What gates

- PR #322 merge → on QC PASS, orchestrator merges autonomously per standing directive (owner asleep; quality default; merge orchestrator dispatch + QC PASS PRs autonomously)
- After PR #322 + verdict comm merge → orchestrator authors Phase 1.5-D.1 dispatch (HU reference set design) per design memo §4.2 with α=β decided (architect-recommended; standing directive lean β)
- LOOP CONTINUES through 1.5-D.1 → 1.5-D.2 (HU labelling) → 1.5-D.3 (HU corpus) → 1.5-D.4 (HU retrain on 59) → 1.5-E (router/coaching) → Phase 2 D5

## Background

Owner ratified Path A direction (current execution path); Path C deferred for possibly later. Path α (column-drop) was authorized at 1.5-B; 988-on-59 corpus + labels + canonical model now in master after this PR merges.

PASS gate clearance at exactly 33.00/40 ± 0.00 mirrors PR #293 12.5K-C-E precedent (988-corpus 5-seed mean 33.00 ± 0.00) — strong signal that the 2 J-B feature drop did not regress 3-way aggregate ceiling, supporting the Phase 1 INTERIM v9-3way-v2.2 framing under the new 59-surface.

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `aa26ae4` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-C dispatch: master `c8138a1` (PR #320)
- Re-poke fire-now: master `aa26ae4` (PR #321)
- Builder PR #322 head: `45a5afb4`
- Architect's design memo (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` §3
- 1.5-B execution merged: master `8349a0b` (PR #315) + QC verdict `521bf36` (PR #319)
- 12.5K-C-E precedent: `BUILDER_REPORT_PHASE125K_C_E_CORPUS_AND_RETRAIN_2026-05-07.md` (5-seed mean 33.00 ± 0.00)
- 988-on-59 corpus: `data/corpus_combined_988_on_59_2026-05-09.jsonl` + labels
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_failure_direction_classification.md`, `feedback_orchestrator_branch_base_verification.md`, `project_qc_heartbeat_convention.md`

**Status: QC stream — fire audit now on PR #322. ~15-20 min wall-clock. 10-item audit. Heartbeat sync to current master at end of tick. Orchestrator merges PR #322 + QC verdict autonomously on PASS per standing directive.**
