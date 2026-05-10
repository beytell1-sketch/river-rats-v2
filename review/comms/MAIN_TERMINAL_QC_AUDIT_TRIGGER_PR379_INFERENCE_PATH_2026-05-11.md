---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #379 — Phase 1.5-E PR-A (59-feature production inference path; NEW inference_path_59 module + oracle_router surface-size dispatch + 12 NEW tests; 23/23 PASS) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #379 (1.5-E PR-A INFERENCE PATH)

PR #379: `builder-phase15e-pr-a-inference-path-2026-05-11`. Head `f1728035df5ee3c6a787c407f1c8bf60032469d8`. Title: "Builder Phase 1.5-E PR-A: 59-feature production inference path (oracle_router surface-size dispatch + tests)".

Builder built PR-A per AMENDMENT (PR #378) Option C: 59-feature production inference path implemented BEFORE production swap (PR-B).

**Diff summary** (per `gh pr view 379`): 4 files / +496 / -1:
- `river-rats-core/inference_path_59.py` (+106) — NEW public `features_from_dict_59()` + `FEATURE_COLUMNS_59` (= `feature_extractor.FEATURE_COLUMNS`); module-load guard
- `river-rats-core/oracle_router.py` (+11/-1) — extended `predict()` with surface-size dispatch (oracle._n_features >= 59 → 59-path; else → 55-path); **`_MODEL_FILES[1]` UNCHANGED** per PR-A scope
- `river-rats-core/tests/test_inference_path_59.py` (+180) — 12 NEW unit tests
- `review/comms/BUILDER_REPORT_PHASE15E_PR_A_INFERENCE_PATH_2026-05-11.md` (+199) — full delivery report

**Test results: 23/23 PASS** (12 NEW inference-path + 11 existing oracle_router tests including the 4 previously-failing).

## Backward compat (per builder report)

| Model | n_features | Path | Result |
|-------|-----------|------|--------|
| v8-HU-38 | 38 | 55-path → truncate-to-38 | unchanged ✓ |
| v9-3way-on-45 | 45 | 55-path → truncate-to-45 | unchanged ✓ |
| vNext-HU-59 / v9-3way-on-59 | 59 | NEW 59-path (no truncation) | now production-runnable ✓ |

## Smoke verification (per builder report)

`test_router_dispatches_59_path_when_loaded`: writes vNext-HU to a temp models dir under v8-HU's filename slot (so OracleRouter loads it at position 1 without modifying `_MODEL_FILES`); asserts `_n_features==59`; `router.predict(feat_dict, num_opponents=1)` returns valid prediction. End-to-end dispatch logic verified ahead of PR-B swap.

## Audit scope (~20-25 min)

Per AMENDMENT (PR #378) §"QC stream — what you audit (For PR-A)":

1. **Diff scope** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): 4 PR files. NEW inference_path_59 module + extended oracle_router (4 lines added in predict + 1 import) + NEW tests + builder report. **NO production swap edits in PR-A:** verify `oracle_router.py:34` `_MODEL_FILES[1]` still reads `'gto_model_v8_hu.json'`.

2. **Inference path correctness**: read `river-rats-core/inference_path_59.py`. Verify:
   - `features_from_dict_59()` is PUBLIC + uses `feature_extractor.FEATURE_COLUMNS` (the canonical 59-feature ordering, NOT a duplicate)
   - `FEATURE_COLUMNS_59` exported as alias to `feature_extractor.FEATURE_COLUMNS`
   - Returns 59-element numpy array in canonical order (sample-check 1 hand input → expected 59 floats)
   - Module-load guard handles import errors cleanly
   - NO duplication of feature extraction logic (single-source-of-truth principle)

3. **Surface-size detection logic**: `oracle_router.py:predict()`:
   - Read the new dispatch logic (oracle._n_features >= 59 → 59-path; else → 55-path)
   - Verify dispatch is on `_n_features` (model attribute, not external assumption)
   - Verify 55-path code path UNCHANGED for legacy 38/55-feature models
   - Verify 59-path code path uses `inference_path_59.features_from_dict_59()` (not extends FEATURE_COLUMNS)
   - Backward compat: legacy callers don't break

4. **Test coverage**: 12 NEW + 11 existing = 23/23 PASS:
   - Builder report claims 4 previously-failing oracle_router tests now PASS — verify by sample-running 1 of those 4 independently
   - 12 NEW tests cover: 59-feature extraction shape, ordering, determinism, surface-size dispatch, vNext-HU end-to-end smoke
   - QC sample-runs 2 NEW tests independently to verify

5. **vNext-HU smoke (end-to-end)**: builder's `test_router_dispatches_59_path_when_loaded` test:
   - Verify temp-dir technique correctly tests dispatch without polluting `_MODEL_FILES` constant
   - vNext-HU `_n_features == 59` confirmed
   - `router.predict(feat_dict, num_opponents=1)` returns valid prediction (5-class softmax probabilities or argmax action)
   - No silent error / no garbage output

6. **TC-X-DISPATCH-COMPLIANCE per AMENDMENT (PR #378)**: PR-A scope only:
   - ❌ NOT extended `gto_model.FEATURE_COLUMNS` (architect-forbidden Path Y) ✓
   - ❌ NOT 55→59 padding shim (silently-wrong-prediction risk) ✓
   - ❌ NOT modified trained model artifacts ✓
   - ❌ NOT touched corpus/data files ✓
   - ❌ NOT solver-verify queue spots ✓

## Special audit consideration: dispatch-boundary correctness

Builder chose `_n_features >= 59` as the dispatch boundary (not `== 59`). Implication: any future 60+ feature model would also use the 59-path. QC assesses:
- Is `>= 59` defensible (forward-compat for 60-feature models)? OR should it be `== 59` (strict; force future models through new dispatch decision)?
- For now, `>= 59` is acceptable since we have no 60+ models and `inference_path_59.features_from_dict_59()` returns exactly 59 features (so a 60-feature model would CRASH on call, not silently misbehave). Surface for QC awareness, not blocking.

## Special audit consideration: temp-dir test technique

Builder's smoke test loads vNext-HU into a temp dir at v8-HU's filename slot to test dispatch without modifying `_MODEL_FILES`. QC verifies:
- Test cleanup is proper (temp dir removed after test)
- Test isolation (doesn't pollute production models dir)
- Test technique transferable to PR-B (where actual swap will happen)

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~20-25 min wall-clock. QC writes:
- `~/river-rats-qc/findings/2026-05-11-pr379-phase15e-pr-a-inference-path.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15E_PR_A_INFERENCE_PATH_2026-05-11.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha` to current master

## What gates

- PR #379 merge → on QC PASS, orchestrator merges autonomously
- After merge → builder fires PR-B (production swap) per AMENDMENT §"PR-B Production swap":
  - Force-add vNext-HU-59 + v8-HU-38 model files (`git add -f`)
  - oracle_router.py:34 swap (`_MODEL_FILES[1]` from `gto_model_v8_hu.json` → `gto_model_vNext_hu_59feat.json`)
  - Coaching-pipeline tests + smoke
  - Phase 1.5 SHIPS

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `d6a07bb` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-E AMENDMENT Option C: master `d6a07bb` (PR #378)
- Builder PR #377 STOP-condition observation merged: master `7c6e845`
- 1.5-E original dispatch: master `70077cd` (PR #376)
- 1.5-D.4 SHIP GATE PASS: master `3f854a8` (PR #373 + QC PR #375 PASS · 0/0/0)
- Builder PR #379 head: `f172803`
- Architect's design memo §4.6 (production swap; ship-action amendment): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Path Y reference (architect-forbidden gto_model.FEATURE_COLUMNS extension): `river-rats-core/train_model_v9_student.py` lines 582-661
- Production HU oracle pointer: `river-rats-core/oracle_router.py:34` (still `gto_model_v8_hu.json` per PR-A scope)
- vNext-HU-59 canonical artifact: `models/gto_model_vNext_hu_59feat.json`
- v9-3way-on-59 reference (also 59-feature, will use NEW path): `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_solver_verification_queue.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_tc23_existence_must_be_git_tracked.md`

**Status: QC stream — fire audit now on PR #379 PR-A INFERENCE PATH. ~20-25 min wall-clock. 6-item audit + dispatch-boundary correctness + temp-dir technique assessments. Orchestrator merges PR #379 + verdict autonomously on PASS. After merge → builder fires PR-B (production swap; force-add + oracle_router.py:34 swap + coaching tests). Phase 1.5 SHIPS after PR-B + QC PASS.**
