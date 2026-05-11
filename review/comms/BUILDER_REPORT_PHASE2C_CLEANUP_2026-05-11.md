---
date: 2026-05-11
from: BUILDER (lead-programmer + architect-hat)
to: Main terminal (orchestrator) + Owner
re: Phase 2-C cleanup report — Step 18 reduced to 2 winners; surface 63→61; inference_path_61 module added per owner-ratified Option B
status: PHASE 2-C COMPLETE — all 8 dispatch tasks honored; awaiting QC trigger
---

# Phase 2-C cleanup report

## TL;DR

Per dispatch PR #400 (owner-ratified Option B): cleanup Step 18 to retain only the 2 re-pilot winners; surface 63→61; new `inference_path_61.py` for production-surface dispatch. No new features implemented; no scope leak beyond Tasks 1-8.

## Surface state

- `feature_extractor.FEATURE_COLUMNS`: **61 features** (was 63)
- Indices 0..58: unchanged canonical 59-feature production surface
- Index 59: `players_to_act_after_hero` (re-pilot 3.36%, rank #10/63)
- Index 60: `tpmk_kicker_rank` (re-pilot 9.18%, rank #2/63 — MW-40 breakthrough)
- Dropped (re-pilot evidence): `broadway_pressure_multiway_facing` (0.26%) + `nut_fd_blocker_multiway` (1.87% absorbed)

## What changed (dispatch tasks 1-8)

| # | Task | Status |
|---|------|--------|
| 1 | Step 18 cleanup in `feature_extractor.py` — drop 2 features, keep 2 | ✓ |
| 2 | `feature_keys.py` — drop 2 F constants, keep 2 | ✓ |
| 3 | Tests in `test_phase2b_pilot_features.py` — drop 2 test classes; update surface assertion 63→61 | ✓ |
| 4 | NEW `inference_path_61.py` — 61-feature production-surface module | ✓ |
| 4b | NEW `tests/test_inference_path_61.py` — mirrors `test_inference_path_59.py` + regression check | ✓ |
| 5 | `train_pilot_2b.py` — REMOVED (pilot evidence captured in builder reports + importance JSONs; no production-runtime role) | ✓ |
| 6 | `inference_path_59.py` UNCHANGED | ✓ |
| 7 | `oracle_router.py` UNCHANGED (2-H scope) | ✓ |
| 8 | Builder report (this file) | ✓ |

## Test results

- `tests/test_phase2b_pilot_features.py`: **10/10 PASS** (2 feature classes + surface-aggregate class; 5 dropped pilot names asserted ABSENT)
- `tests/test_inference_path_61.py`: **10/10 PASS** (count/canonical/dispatch/array shape/determinism/KeyError/regression-vs-59-path)
- `tests/test_inference_path_59.py`: **12/13 PASS, 1 SKIPPED** (no regressions; 59-path behavior preserved)
- `tests/test_board_adjusted_hrp.py`: **6/6 PASS** (canonical surface guard preserved)
- **Total: 38 passed, 1 skipped**

## Production-surface integrity attestation

- `inference_path_59.FEATURE_COLUMNS_59` UNCHANGED (canonical 59-tuple intact)
- `inference_path_61.FEATURE_COLUMNS_61` = `FEATURE_COLUMNS_59 + ('players_to_act_after_hero', 'tpmk_kicker_rank')`
- Module-load assertion on `inference_path_61` validates BOTH (a) first 59 of `feature_extractor.FEATURE_COLUMNS` match canonical, AND (b) indices 59-60 match the 2 canonical pilot winners
- `train_model_v9_student.py` UNCHANGED (still imports `STUDENT_FEATURE_COLUMNS_V9` from `inference_path_59`; trainer behavior bit-for-bit preserved)
- **`features_from_dict_61(d)[:59] == features_from_dict_59(d)` verified bit-for-bit via `test_first_59_elements_match_59_path`**

## Non-NaN/Inf attestation

988/988 rows from `data/corpus_combined_988_on_59_*_2026-05-09.jsonl` produce finite numeric 61-element float32 arrays via `features_from_dict_61` (with inline Step 18 augmentation mirroring the production extractor). No NaN/Inf encountered.

## Compliance with dispatch §STOP

- ✅ `inference_path_61.py` first-59 assertion validates canonical match
- ✅ `feature_extractor.FEATURE_COLUMNS` is exactly 61 elements after cleanup
- ✅ All tests in `test_phase2b_pilot_features.py` + `test_inference_path_61.py` PASS
- ✅ TC-23 EXISTENCE: `inference_path_61.py` + `test_inference_path_61.py` will be `git ls-files`-visible post-commit
- ✅ TC-X-OWNER-SCOPE-DISCIPLINE: NO deviation from Option B; no features added back; only Tasks 1-8 files touched

## Files in this PR

- `river-rats-core/feature_extractor.py` — Step 18 reduced from 4 features to 2; FEATURE_COLUMNS 63→61
- `river-rats-core/feature_keys.py` — 4 F constants → 2
- `river-rats-core/inference_path_61.py` — NEW (~120 lines; modeled on inference_path_59.py)
- `river-rats-core/tests/test_phase2b_pilot_features.py` — rewritten (10 tests; was 17)
- `river-rats-core/tests/test_inference_path_61.py` — NEW (10 tests including regression check)
- `river-rats-core/train_pilot_2b.py` — REMOVED (pilot trainer; evidence preserved in builder reports + importance JSONs)
- `review/comms/BUILDER_REPORT_PHASE2C_CLEANUP_2026-05-11.md` — this report

## Scope-discipline note

Per `feedback_pilot_first_for_long_jobs.md` STANDING RULE + owner-ratified Option B: 15 additional design-memo candidates remain UNTESTED and are deferred from Phase 2 scope. Architect did NOT re-introduce them in this PR. They are recoverable from `PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md` §4 if owner direction in a future phase warrants new evidence-gathering.

## Pre-push checks

- HEAD vs `origin/master` at `git checkout -b`: MATCH `bbda9d9` ✓
- Diff scope: 7 files (6 modified/created + 1 removed) — matches Tasks 1-8 above
- Test suite green on related modules: 38 passed, 1 skipped
- No `oracle_router.py` / data / model-file / `inference_path_59.py` (canonical-59) / `train_model_v9_student.py` edits

## What gates next

Per dispatch §"What gates":
- QC trigger when this PR is pushed
- On QC PASS → orchestrator merges + dispatches 2-D (4-way reference set design)
- On QC SHOULD_FIX → amend + re-fire
- On QC BLOCKER → hold + redo

## References

- Dispatch (Option B cleanup): `MAIN_TERMINAL_PHASE2C_CLEANUP_DISPATCH_2026-05-11.md` (master `bbda9d9`, PR #400)
- Re-pilot builder PR (Option A): master `59978c5` (PR #397)
- Re-pilot QC PASS: master `36726d9` (PR #399)
- Pilot v1 builder PR: master `fa0ea24` (PR #393)
- Pilot v1 QC PASS: master `cfadc34` (PR #395)
- Design memo: `PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md` (PR #388)
- AMENDMENTS 1+2+3 folded
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`
