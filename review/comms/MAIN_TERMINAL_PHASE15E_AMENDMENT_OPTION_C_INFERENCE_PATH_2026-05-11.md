---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous on quality-default)
to: LEAD-PROGRAMMER (builder; architect-hat for inference-path design)
re: AMENDMENT to Phase 1.5-E dispatch (PR #376) — Option C selected per `feedback_quality_default_no_ask.md` + builder STOP-condition (PR #377): builder-architect builds 59-feature production inference path FIRST (PR-A) before production swap (PR-B)
status: DISPATCH AMENDMENT — fire now (adds PR-A prefix; PR-B = original 1.5-E swap with corrected inference)
---

# Phase 1.5-E AMENDMENT — Option C inference-path

Builder PR #377 surfaced architectural STOP per dispatch §"STOP conditions": `oracle_router.predict()` crashes on vNext-HU-59 with `ValueError: Feature shape mismatch, expected: 59, got 55`.

**Root cause** (verified by builder):
- `oracle_router.py:125` → `GtoOracle.features_from_dict(feat_dict)` → 55-feature numpy array via `gto_model.FEATURE_COLUMNS`
- vNext-HU-59 expects 59 features (matches 3-way model on 59-surface)
- v8-HU-38 worked via downward truncation; vNext-HU requires upward extension which architect explicitly forbade in v9-student work
- v9-student trainer included its own private 59-feature inference path; router has no public 59-feature path

Per quality-default + `feedback_orchestrator_decides_not_recommends.md`: orchestrator selects **Option C** (builder-architect designs + implements production 59-feature inference path).

## Why Option C (vs A, B, D)

- **A (extend gto_model.FEATURE_COLUMNS):** architect explicitly FORBADE in v9-student work; would break Path Y assumption. REJECT.
- **B (router-side 59-feature path):** functionally equivalent to C but informal/scoped-narrowly; misses opportunity to design properly for both 3-way + HU 59-surface models. REJECT in favor of C.
- **D (55→59 padding shim):** SILENTLY-WRONG-PREDICTION risk; padding zeros for 4 missing features means model receives garbage input and produces nonsense; cannot ship. REJECT.
- **C (architect-dispatch inference path):** quality-default; designs proper architecture used by both 59-surface models (3-way + HU); future-proofs for any subsequent 59-surface models. SELECT.

## Phase 1.5-E AMENDED — PR-A (inference path) + PR-B (swap)

### PR-A: 59-feature production inference path

**Builder-architect deliverables:**

1. **Design summary** in builder report:
   - How v9-student's private 59-feature inference path works (current state)
   - How to extract it as a PUBLIC 59-feature inference path usable by `oracle_router` for both v9-3way-on-59 + vNext-HU-59 models
   - Where new feature-extraction module lives (e.g., `river-rats-core/feature_extractor_59.py`, or extension to existing `feature_extractor.py` with explicit 59-feature method)
   - How `oracle_router` switches between 38/55-feature legacy and 59-feature modern paths (per-model surface size detection)

2. **Implementation:**
   - NEW or extended feature-extraction module producing 59-feature numpy array compatible with vNext-HU-59 + v9-3way-on-59
   - `oracle_router.py` updated to detect model surface size + route to correct feature-extraction path
   - Backward compatibility: legacy 38/55-feature models still work via existing `gto_model.FEATURE_COLUMNS` path

3. **Verification:**
   - Unit tests for new 59-feature inference path (e.g., `tests/test_inference_path_59.py`); deterministic + correct shape on sample inputs
   - Existing tests still pass (no regression on legacy 38/55-feature path)
   - Smoke test: `oracle_router.load_model(num_opponents=1)` returns vNext-HU-59 + does basic predict on 1 hand without crash (proving the fix works ahead of PR-B swap)

4. **NO production swap in PR-A:** oracle_router.py:34 (`_MODEL_FILES` dict position 1) UNCHANGED in PR-A. Production HU oracle still v8-HU-38 (=runtime artifact; untracked still). PR-A is purely the inference-path infrastructure; PR-B is the swap.

5. **Builder report:** `review/comms/BUILDER_REPORT_PHASE15E_PR_A_INFERENCE_PATH_2026-05-11.md`
   - Design summary (how 3-way 59-feature inference works today; how PR-A extracts/extends)
   - Implementation summary (NEW files + modified files)
   - Test results (per-test PASS/FAIL; total counts; new tests + regression tests)
   - Verification: vNext-HU-59 model loadable + predict-runnable via NEW inference path without errors

### PR-B: Production swap (per original Phase 1.5-E dispatch)

After PR-A merged + QC PASS:

- **Force-add new HU model:** `git add -f river-rats-core/models/gto_model_vNext_hu_59feat.json`
- **Force-add v8-HU-38 (rollback safety, per original §(d)):** `git add -f river-rats-core/models/gto_model_v8_hu.json`
- **oracle_router.py:34 swap:** position 1 from `gto_model_v8_hu.json` → `gto_model_vNext_hu_59feat.json`
- **Coaching-pipeline tests pass:** with PR-A inference path in place, vNext-HU now works through router; tests should pass cleanly
- **Builder report:** `review/comms/BUILDER_REPORT_PHASE15E_PR_B_PRODUCTION_SWAP_2026-05-11.md`

This is the original Phase 1.5-E dispatch §"Builder deliverables" (a)/(b)/(c)/(d)/(e) deliverables, now corrected with PR-A inference-path infrastructure as prerequisite.

## STOP conditions (per CLAUDE.md §5)

- **PR-A:** new inference path test FAILS → STOP/REPORT before PR-B fires
- **PR-A:** existing tests REGRESS → STOP/REPORT; legacy path must remain functional
- **PR-A:** vNext-HU-59 model loads but predict crashes (different error) → STOP/REPORT; investigate
- **PR-B:** any test FAILS after swap → STOP/REPORT; rollback via `oracle_router.py:34` revert
- **PR-B:** force-add `git ls-files` doesn't show files → STOP/REPORT (gitignore pattern issue)
- Multi-way (positions 2/3/4) regression in PR-A or PR-B → STOP/REPORT

## Negative scope (TC-X-OWNER-SCOPE-DISCIPLINE)

- ❌ Does NOT extend `gto_model.FEATURE_COLUMNS` (architect-forbidden per Path Y)
- ❌ Does NOT add 55→59 padding shim (silently-wrong)
- ❌ Does NOT modify trained model artifacts (vNext-HU-59 loads as-is from disk)
- ❌ Does NOT modify v9-3way-on-59 model (PR-A makes it accessible via new path; doesn't change the model)
- ❌ Does NOT touch corpus_hu_746 or any data/ files
- ❌ Does NOT solver-verify queue spots (HOLD-with-accepted-risk per owner)
- ❌ Does NOT change ship gate (already PASSED in 1.5-D.4)

## QC stream — what you audit

**For PR-A (~20-25 min audit; new inference module + integration):**

1. **Diff scope:** new file (e.g., `feature_extractor_59.py` OR extension method) + `oracle_router.py` update + new tests + builder report. NO production swap edits in PR-A.
2. **Inference path correctness:** sample-check that 59-feature extraction matches expectations from v9-student private path (cross-reference). Independent run on 1 hand produces same 59-array.
3. **Surface-size detection logic:** verify `oracle_router` correctly identifies model surface size + routes to correct feature path; backward compat with 38/55-feature legacy.
4. **Test coverage:** new tests for 59-feature path; regression tests for legacy 38/55-feature path; all pass.
5. **vNext-HU smoke:** verify model loadable + predict works via new path (per builder report).
6. **TC-X-DISPATCH-COMPLIANCE:** PR-A scope only; PR-B scope deferred.

**For PR-B (~15-20 min audit; production swap with corrected inference):**

1. Diff scope: 2 force-added model files + oracle_router.py:34 swap + builder report.
2. Force-add verification: `git ls-files` confirms both model files tracked.
3. oracle_router.py:34 diff: only line 34 changed (vNext_hu_59feat replaces v8_hu).
4. Coaching tests pass: full test suite green with vNext-HU now in production routing slot.
5. Multi-way regression: positions 2/3/4 unchanged + still functional.
6. Smoke load test: `oracle_router.load_model(1)` returns vNext + predict works (now via PR-A inference path).
7. TC-X-DISPATCH-COMPLIANCE per original 1.5-E + this AMENDMENT.

## Owner — informational

- 1.5-E hit architectural STOP at production-swap (oracle_router 55-feat ≠ vNext 59-feat); builder correctly STOP'd + surfaced
- Quality-default path per memory: build proper 59-feature inference path FIRST (PR-A), then swap (PR-B)
- Adds ~2-4 hr to 1.5-E timeline; preserves quality of inference architecture; future-proofs for any 59-surface models
- Phase 1.5 SHIP boundary still after 1.5-E (now = PR-A + PR-B both merged)
- Solver-verification queue (48 spots) HOLD-with-accepted-risk per your direction; verify-and-retrain-if-needed is post-ship recovery (not blocking 1.5-E)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `7c6e845` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-E original dispatch: master `70077cd` (PR #376)
- Builder PR #377 STOP-condition observation merged: master `7c6e845`
- 1.5-D.4 SHIP GATE PASS: master `3f854a8` (PR #373 + QC PR #375 PASS · 0/0/0)
- Architect's design memo §4.6 (production swap; ship-action amendment): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Path Y reference (architect-forbidden gto_model.FEATURE_COLUMNS extension): `river-rats-core/train_model_v9_student.py` lines 582-661
- Production HU oracle pointer: `river-rats-core/oracle_router.py:34` (currently `gto_model_v8_hu.json`)
- vNext-HU-59 canonical artifact: `models/gto_model_vNext_hu_59feat.json`
- v9-3way-on-59 reference (also 59-feature): `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_solver_verification_queue.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`

**Status: Phase 1.5-E amended — Option C selected. Builder-architect fires PR-A (59-feature inference path) FIRST. PR-B (production swap) fires after PR-A + QC PASS. Phase 1.5 SHIPS after PR-B + QC PASS.**
