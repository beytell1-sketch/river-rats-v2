---
date: 2026-05-11
from: LEAD-PROGRAMMER (builder; architect-hat for inference-path design)
to: Main terminal (orchestrator) · QC stream · Owner (informational)
re: Phase 1.5-E PR-A — 59-feature production inference path implemented; oracle_router surface-size dispatch in place; vNext-HU now production-runnable; legacy 38/55-feature path unchanged
status: DELIVERY — PR-A ready; PR-B (production swap) authorized after PR-A merge + QC PASS
---

# Phase 1.5-E PR-A — 59-feature production inference path

## Summary

Per AMENDMENT (PR #378) Option C: builder-architect designs + implements production 59-feature inference path before swap (PR-B).

**Deliverables (4 files / +233):**
- `river-rats-core/inference_path_59.py` — NEW public 59-feature feature-extraction module (89 lines)
- `river-rats-core/oracle_router.py` — extended with surface-size dispatch in `predict()` (lines 26 + 114-135 modified)
- `river-rats-core/tests/test_inference_path_59.py` — NEW unit tests (12 tests; 145 lines)
- `review/comms/BUILDER_REPORT_PHASE15E_PR_A_INFERENCE_PATH_2026-05-11.md` — this report

**Test results: 23/23 PASS** (12 NEW inference-path tests + 11 existing oracle_router tests including the 4 previously-failing).

**No production swap in PR-A** — `oracle_router.py:34` `_MODEL_FILES[1]` UNCHANGED (still `'gto_model_v8_hu.json'`). PR-B handles the swap.

## §1 — Design

### Problem (from PR #377 STOP-condition)

- `oracle_router.py:125` → `GtoOracle.features_from_dict(feat_dict)` → 55-feature numpy array via `gto_model.FEATURE_COLUMNS` (length 55)
- vNext-HU-59 expects 59 features; predict raises `ValueError: Feature shape mismatch, expected: 59, got 55`
- Per `train_model_v9_student.py` lines 582-661 Path Y boundary: extending `gto_model.FEATURE_COLUMNS` is forbidden because it's shared with multiple legacy inference paths

### How v9-student handles this today (private path)

`train_model_v9_student.py:596-655` defines `_StudentInference` — a private 59-feature analog of `GtoOracle` used by the trainer + its evaluation harness. It's marked private (underscore prefix) and not exported. PR-A makes the public production analog.

### PR-A solution: parallel public 59-feature path with surface-size dispatch

**`inference_path_59.py`** (NEW; 89 lines):
- Public surface size constant `N_FEATURES_59 = 59`
- Public `FEATURE_COLUMNS_59` tuple (= `feature_extractor.FEATURE_COLUMNS`)
- Public `features_from_dict_59(feat_dict) -> np.ndarray` (parallel to `GtoOracle.features_from_dict`)
- Module-load assertion guards against silent breakage if `feature_extractor.FEATURE_COLUMNS` grows beyond 59 in future

**`oracle_router.py`** (extended; +1 import, +5 lines in `predict`):
- Imports `features_from_dict_59` + `N_FEATURES_59`
- `predict()` now dispatches based on `oracle._n_features`:
  - `>= 59` → `features_from_dict_59(feat_dict)` (modern surface; 59-array)
  - `< 59` → `GtoOracle.features_from_dict(feat_dict)` (legacy 55-array; auto-truncates to 38/45 inside `oracle.predict`)

**Backward compat preserved:**
- v8-HU-38 (`_n_features == 38`) → 55-path → truncate-to-38 → predict (unchanged behavior)
- v9-3way-on-45 (`_n_features == 45`) → 55-path → truncate-to-45 → predict (unchanged behavior)
- v9-3way-on-59 + vNext-HU-59 (`_n_features == 59`) → 59-path → predict (NEW, no truncation needed)

## §2 — Implementation summary

### Files NEW
- `river-rats-core/inference_path_59.py` (89 lines): module + helper function + module-load guard
- `river-rats-core/tests/test_inference_path_59.py` (145 lines): 12 unit tests across 3 test classes

### Files MODIFIED
- `river-rats-core/oracle_router.py`:
  - Line 26: added `from inference_path_59 import features_from_dict_59, N_FEATURES_59`
  - Lines 114-135: extended `predict()` docstring + added surface-size dispatch (3-line if/else)
  - **Line 34 (`_MODEL_FILES[1]`) UNCHANGED** per dispatch §"NO production swap in PR-A"

### Files NOT modified (per dispatch negative scope)
- `river-rats-core/gto_model.py` (FEATURE_COLUMNS=55 unchanged; Path Y boundary preserved)
- `river-rats-core/feature_extractor.py` (FEATURE_COLUMNS=59 unchanged)
- `river-rats-core/train_model_vNext_hu.py` (PR 1 deliverable, not touched)
- `river-rats-core/hu_reference_evaluator.py` (PR 0 deliverable, not touched)
- All training-data + corpus files
- Any v8-HU-38 model files (still on disk untracked; PR-B addresses)

## §3 — Test results

### NEW tests (12; all PASS)

`tests/test_inference_path_59.py`:

```
TestFeatureColumns59:
  test_count_is_59 ✓
  test_matches_feature_extractor ✓
  test_extends_legacy_55 ✓

TestFeaturesFromDict59:
  test_returns_numpy_array_of_correct_shape ✓
  test_deterministic ✓
  test_raises_keyerror_on_missing_keys ✓
  test_ordered_consistent_with_FEATURE_COLUMNS_59 ✓

(module-level smoke tests):
  test_vnext_hu_loads_via_gto_oracle ✓
  test_vnext_hu_predict_via_59_path ✓
  test_legacy_v8_hu_still_works_via_55_path ✓
  test_router_dispatches_legacy_to_55_path ✓
  test_router_dispatches_59_path_when_loaded ✓
```

### Regression tests (11; all PASS — previously 4 failing)

`tests/test_oracle_router.py`:

```
TestRouterInit (3 PASS) — unchanged
TestRouterDispatch (4 PASS — previously: 2 FAILED on v8-HU filename references)
TestRouterPredict (4 PASS — previously: 2 FAILED on Feature shape mismatch)
```

The previously-failing 4 oracle_router tests are now PASSING because:
- 2 fixture tests: oracle_router.py:34 unchanged (still v8-HU); fixture references to `gto_model_v8_hu.json` still match
- 2 predict tests: surface-size dispatch routes legacy to 55-path; v8-HU still receives 55-array → truncate-to-38 → predict OK

**Total: 23/23 PASS in 3.96s.**

### Smoke verification (per dispatch §"PR-A verification" item 5)

`test_router_dispatches_59_path_when_loaded`:
- Builds temp models dir containing ONLY vNext-HU-59 (saved as `gto_model_v8_hu.json` filename to slot into position 1 without modifying `_MODEL_FILES`)
- Instantiates `OracleRouter(models_dir=tmp)` — loads vNext at position 1
- Asserts loaded oracle has `_n_features == 59`
- Calls `router.predict(feat_dict, num_opponents=1)` → no crash
- Asserts `pred.action in {FOLD, CHECK, CALL, BET, RAISE}` + valid confidence

This proves the 59-feature path works through the router; PR-B can swap `_MODEL_FILES[1]` filename without further inference-path work.

## §4 — Routing logic verification

### Decision tree (per `oracle_router.predict`)

```
def predict(feat_dict, num_opponents):
    oracle = self._get_oracle(num_opponents)
    if oracle._n_features >= 59:
        features = features_from_dict_59(feat_dict)   # 59-array
    else:
        features = GtoOracle.features_from_dict(feat_dict)  # 55-array
    return oracle.predict(features)  # truncates if 55-array on smaller model
```

### Per-model behavior

| Model | `_n_features` | Path taken | features.shape | predict outcome |
|-------|--------------|------------|----------------|-----------------|
| v8-HU-38 | 38 | 55-path | (55,) | predict truncates to (38,) ✓ |
| v9-3way-on-45 | 45 | 55-path | (55,) | predict truncates to (45,) ✓ |
| v9-3way-on-55 (hypothetical) | 55 | 55-path | (55,) | predict uses all 55 ✓ |
| v9-3way-on-59 | 59 | 59-path | (59,) | predict uses all 59 ✓ NEW |
| vNext-HU-59 | 59 | 59-path | (59,) | predict uses all 59 ✓ NEW |

## §5 — TC-X-OPERATIONAL-DEVIATION-ASSESSMENT

1. **NEW module (vs extending gto_model)**: per dispatch §"Why Option C" + Path Y reference — extending `gto_model.FEATURE_COLUMNS` is architect-forbidden; parallel module preserves boundary cleanly. Module-load guard ensures the parallel surface stays aligned with `feature_extractor.FEATURE_COLUMNS` (asserts ==59).
2. **Surface-size dispatch in `predict` (vs separate predict methods)**: clean 3-line if/else; no API changes for callers; backward-compat preserved.
3. **Smoke test method**: dispatch §"PR-A verification" item 5 says "oracle_router.load_model(num_opponents=1) returns vNext-HU-59 + does basic predict" — but `oracle_router.py:34` is locked unchanged in PR-A. Builder used a temp-models-dir test (`test_router_dispatches_59_path_when_loaded`) to exercise the dispatch through the router with vNext loaded under v8's filename slot. Equivalent verification without code-path changes.

## §6 — QC stream — what you audit (PR-A)

Per dispatch §"QC stream — what you audit (PR-A)" 6-item:

- [ ] Diff scope: NEW `inference_path_59.py` + extended `oracle_router.py` + NEW tests + builder report; NO production swap edits in PR-A
- [ ] Inference path correctness: sample-check 59-feature extraction matches expectations from v9-student `_StudentInference` (cross-reference); `test_ordered_consistent_with_FEATURE_COLUMNS_59` verifies determinism + ordering
- [ ] Surface-size detection logic: oracle_router correctly identifies model surface size + routes (`oracle._n_features >= N_FEATURES_59` is the dispatch boundary); backward compat with 38/55-feature legacy verified by `test_legacy_v8_hu_still_works_via_55_path`
- [ ] Test coverage: 12 NEW + 11 existing = 23/23 PASS in 3.96s
- [ ] vNext-HU smoke: `test_router_dispatches_59_path_when_loaded` verifies vNext loadable + predict works via NEW path
- [ ] TC-X-DISPATCH-COMPLIANCE: PR-A scope only; PR-B scope deferred (no `_MODEL_FILES` edit; no force-add)

## §7 — What gates next (PR-B)

Per dispatch §"PR-B: Production swap":
- After PR-A merged + QC PASS:
  - Force-add new HU model: `git add -f river-rats-core/models/gto_model_vNext_hu_59feat.json`
  - Force-add v8-HU-38: `git add -f river-rats-core/models/gto_model_v8_hu.json`
  - oracle_router.py:34 swap: position 1 from `gto_model_v8_hu.json` → `gto_model_vNext_hu_59feat.json`
  - Coaching-pipeline tests pass (with PR-A inference path in place)
  - Builder report: `BUILDER_REPORT_PHASE15E_PR_B_PRODUCTION_SWAP_2026-05-11.md`

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `d6a07bb` ✓ (AMENDMENT merged)
- Diff vs master: 4 files (NEW inference_path_59 + extended oracle_router + NEW tests + this report)
- Log vs master: 1 commit
- vNext-HU model file in `river-rats-core/models/` is NOT staged (still gitignored; PR-B force-adds it)

## References

- AMENDMENT (PR #378; Option C): master `d6a07bb`
- Builder STOP observation (PR #377): master `7c6e845`
- 1.5-E original dispatch (PR #376): master `70077cd`
- 1.5-D.4 SHIP GATE PASS (PR #375): master `3f854a8`
- v9-student `_StudentInference` reference: `river-rats-core/train_model_v9_student.py:596-655`
- Path Y boundary documentation: `river-rats-core/train_model_v9_student.py:582-590`
- Production HU oracle pointer: `river-rats-core/oracle_router.py:34` (UNCHANGED in PR-A)
- vNext-HU canonical artifact (local; gitignored; PR-B force-adds): `models/gto_model_vNext_hu_59feat.json`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_named_author_builds_not_polls.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`, `feedback_tc23_existence_must_be_git_tracked.md`

**Status: Phase 1.5-E PR-A complete. 59-feature production inference path implemented + tested + verified backward-compatible. 23/23 tests PASS. Awaits QC + orchestrator merge → PR-B (production swap) authorized.**
