---
date: 2026-05-09
from: Main terminal (orchestrator; standing-directive autonomous)
to: LEAD-PROGRAMMER (programmer-hat with ml-architect-hat consult on STOP) · QC stream (FYI; standalone audit on PR open) · Owner (notice; ratifies sub-phase execution per standing directive)
re: Phase 1.5-C — 3-way verification at 59-surface (5-seed re-train; pre-pad warm-start 45→59; PASS gate ≥ 33.00/40 mean)
status: DIRECTIVE — fires LEAD-PROGRAMMER programmer-hat — fire now
---

# Phase 1.5-C — 3-way verification at 59-surface execution dispatch

## Context (state at this dispatch)

Phase 1.5-B execution merged at master `521bf36` (sequence: 1.5-B execution PR #315 `8349a0b` → QC verdict PR #319 `521bf36`). QC verdict: PASS-WITH-FINDINGS · 0 BLOCKER · 0 SHOULD_FIX · 1 NIT (Step 4 labels file embedded-feat_dict procedural note; output correct; no fix-forward debt).

Outputs now in master:
- `data/corpus_combined_988_on_59_2026-05-09.jsonl` (988 rows × 59 keys; force-added)
- `data/corpus_combined_988_on_59_labels_2026-05-09.jsonl` (988 rows; force-added)
- `feature_extractor.py` / `feature_keys.py` / `train_model_v9_student.py` updated to 59-surface
- `tests/test_features_125j.py` deleted; `tests/test_train_model_v9_student.py` updated

This dispatch fires Phase 1.5-C as the SECOND execution sub-phase: re-train v9-3way student on 988-on-59-surface corpus and verify aggregate ceiling holds at PASS gate ≥ 33.00/40 mean across 5 seeds.

Owner ratified Path A direction (current execution path); Path C deferred for possibly later. α/β decision (§4.2 close-hand-anchor) standing directive lean β (architect-recommended); resolves before 1.5-D.1; non-blocking for 1.5-C.

## LEAD-PROGRAMMER (programmer-hat) — fire now

You are authorized to fire Phase 1.5-C per architect's design memo §3 (in master at `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`). Programmer-hat executes the re-train + verification; ml-architect-hat is on call for any STOP condition (e.g., warm-start failure modes per §3.3) or PASS-gate adjudication per §3.4 decision matrix. ~$0 LLM spend; ~30-60 min wall-clock estimate (1-seed smoke + 5-seed full).

### Single committed scope: design memo §3 in master

The architect's §3 IS the binding spec. Do not re-design; execute it.

- **Scope** (§3.1): re-train v9-3way student on 988-on-59 corpus; verification (NOT improvement); hypothesis being tested is "removing the 2 sub-1% J-B features does not regress 3-way aggregate".
- **N-seed commitment** (§3.2): N = 5 seeds (0,1,2,3,4). Mirrors PR #293 12.5K-C-E precedent.
- **Warm-start strategy** (§3.3): pre-pad from `models/gto_model_v9_3way_v2.2.json` (45-feat) bumped to 59 via existing `prepad_baseline_booster` mechanism in `train_model_v9_student.py:409-437`. Single committed path; NO from-scratch alternative; NO env-var overrides.
- **Hyperparameters** (§3.3): inherit verbatim from `train_model_v9_student.py:139-154` `_HYPERPARAMETERS` (n_estimators=800, max_depth=5, learning_rate=0.05, early_stopping_rounds=50, subsample=0.8, colsample_bytree=0.75, min_child_weight=5, gamma=0.2, reg_alpha=0.1, reg_lambda=1.0, multi:softprob, num_class=5, eval_metric=mlogloss). Confidence weighting `pure`. Class-weight cap 3.0.
- **Warm-start canonicality**: `is_git_tracked('river-rats-core/models/gto_model_v9_3way_v2.2.json')` MUST return True at run time per `train_model_v9_student.py:196-220`.
- **PASS gate** (§3.4): mean across 5 seeds ≥ 33.00/40 on `mw_11_50` reference set. Median seed promoted to canonical at `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json`.
- **STOP/REPORT** (§3.4): mean ∈ [32.00, 33.00) — surface to orchestrator; no auto-promote.
- **HALT/INVESTIGATE** (§3.4): mean < 32.00 — halt 1.5 workstream; trigger root-cause investigation comm before 1.5-D fires.
- **Failure-direction classification** (§3.4): per `feedback_failure_direction_classification.md` — per-hand miss table with under-aggress / over-aggress / class-collapse axis. Direction-skewed regression (e.g., 5+ new under-aggress misses) is STOP/REPORT trigger even if aggregate clears 33.00.
- **Pilot-first analog** (§3.5): 1-seed smoke run BEFORE 5-seed run, gating on "run completes without crash + produces model on disk + scores within 5 points of median 12.5K-C-E result on 40-hand reference". Failure → halt + report. ~10-min spend.

### 6-step execution sequence

**Step 1 — Pre-flight TC-23 EXISTENCE checks** (per `feedback_tc23_existence_must_be_git_tracked.md`):
- `git ls-files river-rats-core/models/gto_model_v9_3way_v2.2.json` returns non-empty
- `git ls-files data/corpus_combined_988_on_59_2026-05-09.jsonl` returns non-empty
- `git ls-files data/corpus_combined_988_on_59_labels_2026-05-09.jsonl` returns non-empty
- `train_model_v9_student.py:139-154` (`_HYPERPARAMETERS`) + `:409-437` (`prepad_baseline_booster`) + `:196-220` (`is_git_tracked` warm-start canonicality) all exist at master `521bf36`

**Step 2 — 1-seed smoke run** (pilot-first analog):
- Seed 0; pre-pad warm-start; full hyperparameters
- Verify completes without crash; model on disk; score on 40-hand reference within 5 points of median 12.5K-C-E
- Failure → STOP; halt + report; do NOT proceed to Step 3

**Step 3 — 5-seed full run**:
- Seeds 0,1,2,3,4 (Seed 0 may re-use smoke if identical config)
- Per-seed model on disk; per-seed score on `mw_11_50` 40-hand reference
- Aggregate: mean, median, std-dev across 5 seeds

**Step 4 — Apply §3.4 PASS gate**:
- Mean ≥ 33.00 → PASS; promote median seed to `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` (force-add)
- Mean ∈ [32.00, 33.00) → STOP/REPORT to orchestrator; do NOT promote
- Mean < 32.00 → HALT/INVESTIGATE; do NOT promote; root-cause comm before any 1.5-D work

**Step 5 — Failure-direction classification**:
- Per-hand miss table for median seed (where it differs from solver-corrected expert per `memory/reference_corrections.md`)
- Direction summary: U=N over X total miss; O=N; C=N
- Direction-skewed regression (5+ new under-aggress misses) → STOP/REPORT trigger even if aggregate cleared

**Step 6 — Builder report**:
- `review/comms/BUILDER_REPORT_PHASE15C_2026-05-09.md` per dispatch §"Deliverables" below

### Deliverables (PR diff)

In-repo (force-add the new model artifact per `feedback_tc23_existence_must_be_git_tracked.md` for downstream 1.5-D reproducibility):

1. `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` (force-add the median-seed canonical model; do NOT include other seed artifacts in PR — keep diff minimal)
2. `review/comms/BUILDER_REPORT_PHASE15C_2026-05-09.md` — execution log: §3.1-§3.5 compliance evidence; per-seed scores; mean/median/std-dev; failure-direction classification table for median seed; SHA-256 of promoted model; pytest pass count; pilot smoke result.
3. (Optional) Training metadata pointing at `corpus_combined_988_on_59_2026-05-09.jsonl` SHA-256 per design memo §2.4.

### BINDING gate (must pass before PR merge)

§3.4 PASS gate: mean ≥ 33.00/40 across 5 seeds.
- Mean ≥ 33.00 → PR PASS; ready for QC.
- Mean ∈ [32.00, 33.00) → STOP/REPORT in PR description; do NOT promote model; surface to orchestrator for owner gate.
- Mean < 32.00 → HALT; do NOT open PR with model; author root-cause investigation comm + open PR with comm only.

### Methodology constraints (binding)

- **Single committed path** per `feedback_quality_default_no_ask.md`: no menus; STOP conditions escalate to ml-architect-hat consult, NOT improvise.
- **STOP conditions** per CLAUDE.md §5: warm-start failure / pytest fail / pilot smoke crash / non-empty pilot diff > 5pts / pre-flight TC-23 RED → STOP and report BLOCKED.
- **Verify-own-output** per CLAUDE.md §7: PR description includes per-seed scores, mean/median/std-dev, failure-direction table, model SHA-256, pytest counts, pilot smoke result. "It looks right" is not verification.
- **No deadlines** per `feedback_no_deadlines.md`: forecast ~30-60 min; quality path beats schedule.
- **No improvisation** on STOP conditions — escalate to ml-architect-hat consult.

### What this PR does NOT do (mandatory negative scope)

- ❌ Does NOT modify `feature_extractor.py` / `feature_keys.py` / source code (those landed in 1.5-B; sealed at master `521bf36`).
- ❌ Does NOT modify the 988-on-59 corpus / labels artifacts (sealed in 1.5-B).
- ❌ Does NOT modify v3.x prompts / BATCH2 / 40-hand reference set / model files OTHER than the new `v9_3way_v22_on_59` canonical.
- ❌ Does NOT execute 1.5-D HU work (separate sub-phase).
- ❌ Does NOT pre-empt α/β owner-scope decision (separate gate; resolves before 1.5-D.1).
- ❌ Does NOT improvise on STOP/HALT outcomes — escalate to architect-hat consult per §3.4 decision matrix.
- ❌ Does NOT include other seed artifacts in PR diff — only the median-seed canonical promoted file.

## QC stream — what you audit (post-PR; standalone, ~15-20 min)

Routing per `feedback_qc_routing_when_standalone_active.md`. Pre-merge QC required per `feedback_qc_required_before_approval.md` (verification result feeds 1.5-D HU retrain decisions; milestone-class).

10-item audit:

1. **Diff scope strict**: 1-2 PR files (model jsonl + builder report). NO source / data / prompt edits.
2. **TC-23 EXISTENCE**: `git ls-files river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` returns non-empty. Other cited paths (corpus, warm-start, hyperparameters) exist at master HEAD post-merge.
3. **§3.4 PASS gate adjudication**: builder report's mean ≥ 33.00 across 5 seeds; QC verifies the per-seed scores + the mean.
4. **Failure-direction classification format compliance** (§3.4 + `feedback_failure_direction_classification.md`): per-hand miss table present with U/O/C axis; direction summary present; direction-skewed regression check applied.
5. **Pre-pad warm-start canonicality**: builder report shows `is_git_tracked('models/gto_model_v9_3way_v2.2.json')` returned True at run time; warm-start booster path correct.
6. **Hyperparameter inheritance compliance**: builder report shows `_HYPERPARAMETERS` from `train_model_v9_student.py:139-154` used verbatim; no env-var overrides.
7. **Pilot smoke result**: builder report includes 1-seed smoke completion + score within 5 points of median 12.5K-C-E precedent.
8. **Promoted model spec**: median seed identified; SHA-256 logged; force-added to git per `feedback_tc23_existence_must_be_git_tracked.md`.
9. **TC-X-DISPATCH-COMPLIANCE**: 6-step sequence + STOP conditions + negative scope all honored.
10. **Methodology rule cross-check**: failure-direction per `feedback_failure_direction_classification.md`; postflop-composition per `feedback_preflop_geometry_vs_postflop_composition.md`; close-hand selection per `feedback_close_hand_selection.md`; solver-vs-labels per `feedback_solver_vs_expert_labels.md` (no solver labels in training).

QC writes finding to `~/river-rats-qc/findings/2026-05-09-pr<n>-phase15c-execution.md` + cross-posts `review/comms/REVIEW_QC_PHASE15C_EXECUTION_2026-05-09.md` + heartbeat sync to current master per `project_qc_heartbeat_convention.md`.

## Owner — what you gate

- This dispatch PR merge → orchestrator autonomous per standing directive (orchestrator dispatch class)
- 1.5-C execution PR merge (after QC PASS) → orchestrator autonomous per standing directive
- α/β decision (§4.2 close-hand-anchor) → resolves before 1.5-D.1; standing directive lean β; non-blocking for 1.5-C

After 1.5-C merges, orchestrator dispatches Phase 1.5-D.1 (HU reference set design) per design memo §4.2 + α=β decision.

## Loop status

Loop CONTINUES through 1.5-C authorship + execution + QC + merge → 1.5-D.1 dispatch (with α=β decided) → 1.5-D.2 / 1.5-D.3 / 1.5-D.4 → 1.5-E → Phase 2 D5.

## What's blocked / what's queued

**Cleared by this dispatch:**
- LEAD-PROGRAMMER programmer-hat fires Phase 1.5-C execution.

**Newly queued (post 1.5-C merge):**
- Phase 1.5-D.1 dispatch (HU reference set design) per design memo §4.2 with α=β.
- 2 memory rule additions (deferred from 1.5-B merge sequence; will commit alongside 1.5-C close-out comm):
  - bit-equality verification on RNG-dependent features requires RNG-seed-preservation infrastructure
  - append-only-end-of-pipeline verification for column-drop migrations

**Re-queued (post Phase 1.5 ship):**
- Phase 2 D5 per blueprint.

## References

- 1.5-B execution merged: master `8349a0b` (PR #315); QC PASS: `521bf36` (PR #319; PASS-WITH-FINDINGS · 0/0/1 NIT — procedural NIT, no fix required)
- 1.5-B Path α auth: master `29ebe1f` (PR #316)
- 1.5-B execution dispatch: master `9491965` (PR #314)
- Architect's design memo (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` (§3 spec; §3.1-§3.5)
- 988-on-59 corpus + labels (in master): `data/corpus_combined_988_on_59_2026-05-09.jsonl`, `data/corpus_combined_988_on_59_labels_2026-05-09.jsonl`
- Warm-start: `river-rats-core/models/gto_model_v9_3way_v2.2.json` (git-tracked; canonical at runtime per `train_model_v9_student.py:196-220`)
- 12.5K-C-E precedent: `BUILDER_REPORT_PHASE125K_C_E_CORPUS_AND_RETRAIN_2026-05-07.md` (988-corpus 5-seed mean 33.00/40 ± 0.00; pilot smoke target ±5pts)
- Reference set: `river-rats-core/reference_evaluator.py` (`mw_11_50`; 40 hands)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_no_deadlines.md`, `feedback_explicit_action_trigger.md`, `feedback_qc_required_before_approval.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_failure_direction_classification.md`, `feedback_preflop_geometry_vs_postflop_composition.md`, `feedback_close_hand_selection.md`, `feedback_solver_vs_expert_labels.md`, `project_qc_heartbeat_convention.md`

**Status: LEAD-PROGRAMMER (programmer-hat) fires Phase 1.5-C on this comm merge. Single committed path per design memo §3; ~$0; ~30-60 min wall-clock to PR open. BINDING gate: §3.4 PASS gate ≥ 33.00/40 mean. STOP conditions per §3.4 + CLAUDE.md §5 escalate to ml-architect-hat consult — no improvisation. QC standalone audit on PR open. Orchestrator merges PR autonomously per standing directive on QC PASS. Loop CONTINUES.**
