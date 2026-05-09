---
date: 2026-05-09
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER (programmer-hat with architect-hat STOP-condition consult) · QC stream (FYI; standalone audit on PR open) · Owner (notice; fire-now to merge gates dispatch + execution PR + verdict)
re: Phase 1.5-B — feature-prune mechanical execution (988-corpus → 59-surface re-extract; bit-equality binding gate)
status: DIRECTIVE — fires LEAD-PROGRAMMER programmer-hat — fire now
---

# Phase 1.5-B — feature-prune mechanical execution dispatch

## Context (state at this dispatch)

Phase 1.5-A merged at master `465e6fa` (sequence: PR #307 architect memo `f16b317` → PR #311 rev-1 verdict `d31dac2` → PR #313 rev-2 verdict `465e6fa`). Architect's design memo `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` is now in master and IS the spec for this and all subsequent Phase 1.5 sub-phases.

QC delta-audit on PR #307 rev 2 was PASS · 0/0/0 (zero findings). Path A+ amend (SHOULD_FIX-1 + NIT-1 closed; new α/β owner-scope item flagged correctly) carries forward. The α/β decision (commit v8 artifacts vs re-anchor on v9-3way-on-59) is owner-scope and resolves before 1.5-D.1 fires — it does NOT block Phase 1.5-B or 1.5-C.

This dispatch fires Phase 1.5-B as the FIRST execution sub-phase: feature-prune mechanical migration of the 988-corpus from 61-surface → 59-surface. Sub-phases 1.5-C / 1.5-D / 1.5-E will be dispatched separately on each predecessor's merge.

## LEAD-PROGRAMMER (programmer-hat) — fire now

You are authorized to fire Phase 1.5-B. Programmer-hat executes the mechanical migration; architect-hat is on call for any STOP condition per §2.2. ~$0 LLM spend; ~30-60 min wall-clock estimate.

### Single committed scope: design memo §2 in master

The architect's §2 IS the binding spec. Do not re-design; execute it.

- **Migration philosophy** (§2.1): re-extract from raw situations, NOT column-drop. Architect's reasoning (future-proofing + quality discipline + provenance clarity) is committed. Bit-equality verification of §2.3 is an additional safeguard, not a substitute.
- **Re-extraction protocol** (§2.2): the 4-step sequence (source mutation → extractor self-test → re-extract → labels copy) is committed. Execute in that order.
- **Determinism guarantee + verification** (§2.3): the bit-equality verification command is committed. Empty diff = PASS; non-empty diff = STOP CONDITION per CLAUDE.md §5.
- **Output artifact spec** (§2.4): committed (path + size + keys + checksum + labels-copy convention).
- **Invariant tests scope** (§2.5): committed (`tests/test_train_model_v9_student.py` IN scope; `check_leakage.py` + `train_v2_3_clean.py` OUT of scope at root; legacy v2.3 frozen).

### 4-step execution sequence (mirror of §2.2)

**Step 1 — Source mutation** (single PR, single commit on the PR's first commit):
- Delete `feature_extractor.py:1613-1619` (Step 18 column block).
- Delete `feature_extractor.py:2136-2171` (`compute_nut_blocker_overcard_count`).
- Delete `feature_extractor.py:2174-…` through end of `compute_bet_call_multiway_oop_raise_pressure_index` body. Architect-hat in 1.5-B identifies the exact closing line; per architect's pre-commitment in §2.2, function body ends at the return statement following the body in the file as it exists at master `465e6fa`.
- Delete `feature_extractor.py:2645-2663` (the two call-site assignments inside `extract_all_features`).
- Delete `feature_keys.py:94-101` block (the comment + 2 keys; trim surrounding blank lines).
- Update `train_model_v9_student.py:97-122` (assert 59 + tail-position assertions per memo §1.3.3).
- Update `train_model_v9_student.py:127` (`_N_FEATURES_STUDENT = 59`).
- Update `train_model_v9_student.py:1-30` docstring "61" → "59".
- Delete `tests/test_features_125j.py`.
- Update `tests/test_train_model_v9_student.py` surface-size assertions 61 → 59 (architect identifies exact lines per §2.2).
- Update active scripts (`scripts/generate_lever_c_situations.py`); freeze-note historical scripts (`scripts/build_corpus_revision_125i_mw40_verif_situations.py`, `scripts/assemble_125i_d_788.py`).

**Step 2 — Extractor self-test:**
- Run `python -m pytest river-rats-core/tests/` — must PASS with 59-surface assertions.
- Smoke test: a single hand from `data/corpus_combined_988_2026-05-07.jsonl` through modified `extract_all_features`. Verify output dict has exactly 59 keys matching `FEATURE_COLUMNS` (post-drop) and bit-equals the 988-corpus's `feat_dict[k]` for all `k ∈ 59-keys`. Any mismatch = STOP per CLAUDE.md §5.

**Step 3 — Re-extract 988 → 59 surface:**
- Inputs: 988 raw situations from 988-corpus (`prior_actions` / `board` / `hero_cards` / etc.).
- Output: `data/corpus_combined_988_on_59_2026-05-09.jsonl` (date matches PR open day).
- Preserve all non-feature row keys verbatim per §2.4.
- Each row's `feat_dict` has exactly 59 keys.

**Step 4 — Labels copy:**
- Copy `data/corpus_combined_988_labels_2026-05-07.jsonl` verbatim to `data/corpus_combined_988_on_59_labels_2026-05-09.jsonl`. Content-identical SHA-256 (date suffix only differs).
- Verify per §2.4: "If 1.5-B discovers an embedded feat_dict in labels per row, that's a STOP condition per CLAUDE.md §5; report and re-decompose."

### BINDING gate (must pass before PR merge)

Run §2.3 bit-equality verification command (the full bash block in design memo). Diff between (column-dropped reference) and (re-extracted artifact) MUST be empty.

- Empty diff → PASS → proceed to PR open.
- Non-empty diff → STOP per CLAUDE.md §5. Architect-hat in 1.5-B writes a diagnostic comm explaining the drift and requests scope-expansion authorization from orchestrator BEFORE proceeding. Do NOT improvise a fix.

### Deliverables (PR diff)

In-repo (force-add the .jsonl per `*.json` / `*.jsonl` ignore — quality discipline: corpus artifact must be git-tracked per `feedback_tc23_existence_must_be_git_tracked.md` for downstream 1.5-C reproducibility):

1. Source diff per Step 1 (single commit).
2. `data/corpus_combined_988_on_59_2026-05-09.jsonl` (force-add).
3. `data/corpus_combined_988_on_59_labels_2026-05-09.jsonl` (force-add).
4. `review/comms/BUILDER_REPORT_PHASE15B_2026-05-09.md` — execution log: each of the 4 steps with output / checksums / pytest pass count / smoke test result / bit-equality diff (empty); any deviations from §2 spec flagged with reasoning.

### Methodology constraints (binding)

- **Single committed path** per `feedback_quality_default_no_ask.md`: no menus; commit to one execution and report. STOP conditions go to architect-hat consult, NOT improvise.
- **Stop conditions** per CLAUDE.md §5: file-not-where-expected / function-renamed / unexplained-test-fail / line-numbers-mismatch / output-contradicts-expected / bit-equality-diff-non-empty → STOP and report BLOCKED. Improvising is worse than stopping (per CLAUDE.md anti-patterns).
- **Verify-own-output** per CLAUDE.md §7: PR description includes pytest pass/fail counts, smoke test output, bit-equality diff (must be empty), checksums of new artifacts. "It looks right" is not verification.
- **Test-first NOT applicable here** — this is a mechanical migration, not new feature; existing tests cover the surface assertion. Update them per §1.3.3, don't author new ones.
- **river-rats-core/ is sacred** per CLAUDE.md §6: only reviewed-approved-passing code enters. PR sits in review/ via PR until QC PASS + owner fire-now → merge.
- **No deadlines** per `feedback_no_deadlines.md`: forecast is ~30-60 min; quality path beats schedule.

### What this PR does NOT do (mandatory negative scope)

- ❌ Does NOT modify any feature definitions OTHER than dropping the 2 J-B features per §2.2 Step 1.
- ❌ Does NOT modify v3.x prompts / BATCH2 / labelling pipeline / 40-hand reference set / model files (other than the corpus artifact + labels copy).
- ❌ Does NOT execute 1.5-C 3-way verification (separate sub-phase; fires post 1.5-B merge).
- ❌ Does NOT pre-empt α/β owner-scope decision (separate gate; resolves before 1.5-D.1).
- ❌ Does NOT create `tools/check_leakage_v9_59.py` (architect's §2.5 says "if a future leakage check on 59-surface is needed, commission separately"; not in 1.5-B scope).
- ❌ Does NOT improvise on STOP conditions — escalate to architect-hat consult.

## QC stream — what you audit (post-PR; standalone, ~15-20 min)

Routing per `feedback_qc_routing_when_standalone_active.md`. NOT milestone-class (mechanical migration), but the bit-equality + force-add corpus artifact warrant pre-merge QC per `feedback_qc_required_before_approval.md` (first execution sub-phase of Phase 1.5; sets the surface for 1.5-C/D).

8-item audit:

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): expected files only — source diffs per §2.2 Step 1; 2 corpus jsonl files (force-added); 1 builder report. NO unrelated edits / no model files / no prompt files.
2. **Source mutation matches §2.2 Step 1**: verify each listed deletion / update lands at the cited line numbers in the source diff. Any deviation must be flagged + reasoned in builder report.
3. **TC-23 EXISTENCE git-tracked check** per `feedback_tc23_existence_must_be_git_tracked.md`: corpus jsonl files MUST be git-tracked in PR (force-added with `git add -f`). Verify via `git ls-files data/corpus_combined_988_on_59_*.jsonl` returns non-empty in PR's branch.
4. **Bit-equality verification PASS**: builder report includes the §2.3 verification command output and shows empty diff. QC re-runs the command on a fresh checkout of the PR branch as independent verification.
5. **Output artifact spec compliance** (§2.4): 988 rows; each `feat_dict` has exactly 59 keys; non-feature keys preserved verbatim. QC samples a few rows to spot-check.
6. **Pytest PASS**: `python -m pytest river-rats-core/tests/` PASS count matches builder report.
7. **Labels file convention** (§2.4): content-identical SHA-256 between `corpus_combined_988_labels_2026-05-07.jsonl` and `corpus_combined_988_on_59_labels_2026-05-09.jsonl` (date suffix only differs).
8. **TC-X-DISPATCH-COMPLIANCE**: this dispatch's 4 steps + STOP conditions + negative scope all honored. No scope creep.

QC writes finding to `~/river-rats-qc/findings/2026-05-09-pr<n>-phase15b-execution.md` + cross-posts `review/comms/REVIEW_QC_PHASE15B_EXECUTION_2026-05-09.md` + heartbeat sync to current master per `project_qc_heartbeat_convention.md`.

## Owner — what you gate

- **This dispatch PR merge** → on owner explicit `fire now` (going-forward rule)
- **1.5-B execution PR merge** (after QC PASS) → on owner explicit `fire now`
- **α/β decision** (separate, non-blocking; resolves before 1.5-D.1 fires)

After 1.5-B merges, orchestrator dispatches Phase 1.5-C (3-way verification at 59-surface) per design memo §3.

## Loop status

Loop CONTINUES through 1.5-B authorship + QC + merge → 1.5-C dispatch → 1.5-C execution + QC + merge → 1.5-D.1 (HU reference set; α/β decision needed before fire) → 1.5-D.2/3/4 → 1.5-E → Phase 2 D5.

## What's blocked / what's queued

**Cleared by this dispatch:**
- LEAD-PROGRAMMER programmer-hat fires Phase 1.5-B execution.

**Newly queued (post 1.5-B merge):**
- Phase 1.5-C 3-way verification dispatch per design memo §3.

**Held independently (not blocking 1.5-B/C):**
- α/β decision (owner-scope; resolves before 1.5-D.1).

**Re-queued (post Phase 1.5 ship):**
- Phase 2 D5 per blueprint.

## References

- Phase 1.5-A merged: master `465e6fa` (PR #307 architect memo at `f16b317`; PR #311 rev-1 verdict at `d31dac2`; PR #313 rev-2 verdict at `465e6fa`)
- Architect's design memo (now in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Phase 1.5-A dispatch: `MAIN_TERMINAL_PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` (master `5863f13`, PR #306)
- Phase 1.5 queue + retrain-ordering pre-commitment: `MAIN_TERMINAL_SHIP_A_FIRE_AND_PHASE15_QUEUE_2026-05-07.md` (master `a382fa2`, PR #302)
- 988-corpus source: `data/corpus_combined_988_2026-05-07.jsonl` + `data/corpus_combined_988_labels_2026-05-07.jsonl`
- Source files in scope: `river-rats-core/feature_extractor.py`, `river-rats-core/feature_keys.py`, `train_model_v9_student.py`, `tests/test_train_model_v9_student.py`, `tests/test_features_125j.py`, `scripts/generate_lever_c_situations.py`
- Memory rules: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_no_deadlines.md`, `feedback_explicit_action_trigger.md`, `feedback_qc_required_before_approval.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_orchestrator_branch_base_verification.md`, `project_qc_heartbeat_convention.md`, `feedback_solver_findings.md`

**Status: LEAD-PROGRAMMER (programmer-hat) fires Phase 1.5-B on this comm merge. Single committed path per design memo §2; ~$0; ~30-60 min wall-clock to PR open. BINDING gate: §2.3 bit-equality empty diff. STOP conditions per CLAUDE.md §5 escalate to architect-hat consult — no improvisation. QC standalone audit on PR open. Owner gates this dispatch merge + 1.5-B execution PR merge. Loop CONTINUES.**
