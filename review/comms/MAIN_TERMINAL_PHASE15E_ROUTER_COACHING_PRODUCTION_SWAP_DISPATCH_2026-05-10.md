---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous)
to: LEAD-PROGRAMMER (builder)
re: Phase 1.5-E — router/coaching alignment + production HU oracle swap (per design memo §4.6 amendment); Phase 1.5 SHIP boundary
status: DISPATCH — fire now
---

# Phase 1.5-E — router/coaching alignment + production swap

## Context

Phase 1.5-D.4 SHIP GATE COMPLETE: vNext-HU-59 canonical model at 28/30 (exactly architect-committed gate); 5-seed mean 28.2/30; ALL 5 seeds ≥28/30; v8-HU baseline +10 absolute pts (60% → 93.3%). Per dispatch §"After PASS: orchestrator authorizes 1.5-E (router/coaching alignment + production swap per §4.6)" → 1.5-E AUTHORIZED.

Solver-verification queue: 48 spots; HOLD-with-accepted-risk per owner (2026-05-10 21:13 SAST); verify-and-retrain-if-needed is post-ship recovery.

## Scope (per design memo §4.6 amendment)

Total ship action per design memo §4.6 (verbatim):
> "(1) train HU model in 1.5-D.4; (2) at 1.5-E, `git add -f` the new HU model file + change `oracle_router.py:34` filename pointer + run coaching-pipeline tests + commit + open 1.5-E PR."

Step (1) complete (PR #373 + QC PR #375 PASS · 0/0/0; master `3f854a8`). Step (2) is this dispatch.

## Builder deliverables

### (a) Force-add new HU model file to git

- Locate canonical 5-seed model artifact: `models/gto_model_vNext_hu_59feat.json` (currently at top-level `./models/` per smoke/full PR; gitignored).
- Move/copy to production location: `river-rats-core/models/gto_model_vNext_hu_59feat.json` (matches v8-HU-38 location pattern).
- `git add -f river-rats-core/models/gto_model_vNext_hu_59feat.json` (force-add to bypass .gitignore per design memo §4.6 amendment; pattern matches `gto_model_v9_3way_v2.2.json` precedent).
- Verify file is git-tracked: `git ls-files river-rats-core/models/gto_model_vNext_hu_59feat.json` returns the path (per `feedback_tc23_existence_must_be_git_tracked.md`).

### (b) Change oracle_router.py filename pointer

- Edit `river-rats-core/oracle_router.py` line ~34 in `_MODEL_FILES` dict:
  - **From:** `1: 'gto_model_v8_hu.json',`
  - **To:** `1: 'gto_model_vNext_hu_59feat.json',`
- Position 1 is the HU oracle (num_opponents=1 routing); only the HU entry changes; positions 2/3/4 (3-way/4-way/5-way) stay unchanged.
- Verify routing still loads correctly: `python3 -c "from oracle_router import load_model; m = load_model(num_opponents=1); print(m.num_class)"` (or equivalent smoke test); should report 5 classes (vNext-HU is 5-class) without crash.

### (c) Run coaching-pipeline tests

- Run full test suite for `river-rats-core/tests/`. All existing tests must PASS (no regression in 3-way/multiway pipelines from HU swap).
- Specifically verify any tests that exercise `oracle_router.load_model(num_opponents=1)` produce expected outputs with the new model.
- If any test fails: STOP / REPORT; investigate before merging. Common causes: (1) model artifact format-incompatibility (vNext is 5-class; v8-HU was 3-class — caller code may need update); (2) feature surface assertion mismatch (callers expect 38 features for HU; vNext is 59).

### (d) v8-HU-38 disposition

- v8-HU-38 file (`river-rats-core/models/gto_model_v8_hu.json`) is currently runtime-only-not-git-tracked (per design memo §1.2 RED entries). Action options:
  - Option A: leave on disk untracked (preserves runtime fallback if rollback needed; matches §1.2 status quo)
  - Option B: also force-add for git provenance (formalizes runtime artifact + provides rollback safety net)
- **Orchestrator picks Option B** per quality-default + `feedback_tc23_existence_must_be_git_tracked.md` lesson learned: untracked production artifacts created the §1.2 attestation gap; force-add closes the gap symmetrically.
- Builder: `git add -f river-rats-core/models/gto_model_v8_hu.json` alongside the new model.
- Both files in PR; oracle_router.py points to vNext; v8 stays available as runtime artifact + rollback target.

### (e) Builder report

- `review/comms/BUILDER_REPORT_PHASE15E_ROUTER_COACHING_2026-05-10.md`:
  - Force-add summary (both files; `git ls-files` verification)
  - oracle_router.py:34 diff (verbatim before/after)
  - Coaching-pipeline test results (per-test PASS/FAIL; total counts)
  - Smoke test: `oracle_router.load_model(num_opponents=1)` returns vNext model + does basic predict on 1 hand without crash
  - Confirmation that 3-way/4-way/5-way routing UNCHANGED + tests still pass

### Negative scope (TC-X-OWNER-SCOPE-DISCIPLINE)

- ❌ Does NOT modify `river-rats-core/hu_reference_evaluator.py` (PR 0 deliverable)
- ❌ Does NOT modify `river-rats-core/train_model_vNext_hu.py` (PR 1 deliverable)
- ❌ Does NOT modify corpus_hu_746 or any data/ files
- ❌ Does NOT modify multiway routing (positions 2/3/4 in _MODEL_FILES)
- ❌ Does NOT solver-verify queue spots (HOLD-with-accepted-risk per owner)
- ❌ Does NOT change ship gate threshold or design memo §4.6 (already committed)
- ❌ Does NOT trigger retrain (1.5-D.4 already shipped)

### STOP conditions (per CLAUDE.md §5)

- Coaching-pipeline test FAIL → STOP / REPORT; investigate root cause before merging
- `oracle_router.load_model(1)` crashes on vNext model → STOP / REPORT; possibly format-incompatibility or 3-class→5-class transition gap
- `git ls-files` does NOT confirm force-added files → STOP / REPORT; .gitignore pattern may need adjustment
- Multi-way tests fail (positions 2/3/4) → STOP / REPORT; HU swap should NOT affect them; investigate

## QC stream — what you audit (post-PR)

~15-20 min audit:

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): files in PR are limited to:
   - `river-rats-core/models/gto_model_vNext_hu_59feat.json` (NEW; force-added)
   - `river-rats-core/models/gto_model_v8_hu.json` (NEW; force-added; v8-HU-38 runtime artifact)
   - `river-rats-core/oracle_router.py` (1-line change to _MODEL_FILES dict position 1)
   - `review/comms/BUILDER_REPORT_PHASE15E_ROUTER_COACHING_2026-05-10.md`
   - NO other source code edits; NO data/ edits; NO design memo edits

2. **Force-add verification**: both model files git-tracked per `git ls-files`; sizes reasonable (vNext ~5-15 MB; v8 ~12 MB).

3. **oracle_router.py diff verification**: only line 34 changed (1: 'gto_model_v8_hu.json' → 1: 'gto_model_vNext_hu_59feat.json'); positions 2/3/4 unchanged; legacy filename comments preserved.

4. **Coaching-pipeline tests pass**: builder report documents all tests run + counts; QC sample-runs 1-2 tests independently to verify.

5. **Smoke load test**: builder report documents `oracle_router.load_model(num_opponents=1)` returns vNext + basic predict works.

6. **Multi-way regression**: builder report confirms positions 2/3/4 routing tests still pass + 3-way/multiway oracle behavior unchanged.

7. **Provenance link**: `gto_model_vNext_hu_59feat.json` provenance docstring (in `train_model_vNext_hu.py`) traceable from this PR (commit hash links to model artifact per §5.1 requirement).

8. **TC-X-DISPATCH-COMPLIANCE per this comm**: all negative scope items honored; STOP conditions evaluated.

## Phase 1.5 SHIP boundary

After 1.5-E PR + QC PASS + merge: **Phase 1.5 SHIPS.** Production HU oracle = vNext-HU-59 (28/30 ship-gate-clear; +10 over v8-HU-38). 3-way/multiway routing unchanged.

Post-ship items (out of 1.5-E scope; for future dispatches):
- Solver-verification queue (48 spots) drain when solver online; retrain delta if disagreements
- Design memo §4.6 footnote amendment (acknowledge actual v8-HU baseline 18/30 vs projected 26-28/30)
- HU-6.5 corpus-exclusion-gap design refinement (option to include HU-6.5 lookalikes in next retrain corpus; current model-stuck on HU-6.5 anchor reference is documented gap)
- Phase 2 D5 (deferred per blueprint memo per `project_v9_3way_ceiling.md`)

## Owner — informational

- Phase 1.5-D.4 SHIP GATE PASS at 28/30 canonical (5-seed mean 28.2/30; +10 over v8-HU baseline 18/30)
- This dispatch executes the production swap: HU oracle vNext-HU-59 replaces v8-HU-38 at runtime via oracle_router.py:34 filename pointer change
- Both model files force-added to git for provenance + rollback safety (closes §1.2 attestation gap symmetrically)
- After 1.5-E merge: **Phase 1.5 SHIPS** (3-way + HU both at 59-surface canonical; production aligned)
- Solver queue (48 spots) HOLD-with-accepted-risk per your direction; verify-and-retrain-if-needed is post-ship recovery (not blocking 1.5-E)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `3f854a8` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.4 PR 2 5-SEED FULL merged: master `3f854a8` (PR #373 + QC PR #375 PASS · 0/0/0; SHIP GATE PASS)
- 1.5-D.4 PR 1 SMOKE merged: master `77bbefb` (PR #370 + QC PR #372 PASS; smoke 27/30)
- 1.5-D.4 PR 0 EVAL INFRA merged: master `3fcf7f1` (PR #367 + QC PR #369 PASS; v8-HU baseline 18/30)
- 1.5-D.4 dispatch + AMENDMENT: master `3d5572b` (PR #366) + master `178fdaf` (PR #364)
- Architect's design memo §4.5 + §4.6 (ship-gate ≥28/30 + 1.5-E ship-action amendment): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Production HU oracle pointer: `river-rats-core/oracle_router.py` `_MODEL_FILES` dict position 1
- vNext-HU-59 canonical artifact: `models/gto_model_vNext_hu_59feat.json` (pre-1.5-E location; 1.5-E moves to `river-rats-core/models/`)
- v8-HU-38 runtime artifact: `river-rats-core/models/gto_model_v8_hu.json` (untracked; 1.5-E force-adds)
- Trainer provenance: `river-rats-core/train_model_vNext_hu.py` (provenance docstring per §5.1)
- Force-add precedent: `river-rats-core/models/gto_model_v9_3way_v2.2.json` (3-way model; force-added per analogous pattern)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_solver_verification_queue.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`

**Status: Phase 1.5-E fires LEAD-PROGRAMMER. Force-add new HU model + v8-HU-38 + oracle_router.py:34 swap + coaching-pipeline tests + builder report. After 1.5-E PR + QC PASS + merge → Phase 1.5 SHIPS. Solver-verification queue (48 spots) post-ship recovery per owner direction.**
