---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #401 — Phase 2-C cleanup (surface 63→61; 2 winners retained; NEW inference_path_61 module) — fire audit now (pre-merge milestone)
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #401 (Phase 2-C cleanup)

PR #401: `builder-phase2-c-cleanup-2026-05-11`. Head per push `origin/builder-phase2-c-cleanup-2026-05-11`. Title: "Builder Phase 2-C cleanup — surface 63→61; 2 winners retained; NEW inference_path_61 module".

Builder Phase 2-C cleanup per dispatch (PR #400, owner-ratified Option B) — dropped 2 absorbed features (nut_fd + broadway); retained 2 winners (players_to_act + tpmk_kicker_rank); surface 63→61; NEW `inference_path_61.py` for production-surface dispatch.

Per builder report TL;DR: all 8 dispatch tasks honored; 38 tests pass + 1 skipped; no scope leak beyond Tasks 1-8.

## Diff summary (per builder report §"Files in this PR")

7 files net change (6 modified/created + 1 removed):

- `river-rats-core/feature_extractor.py` — Step 18 reduced (4 features → 2); FEATURE_COLUMNS 63→61
- `river-rats-core/feature_keys.py` — 4 F constants → 2
- `river-rats-core/inference_path_61.py` (NEW, ~120 lines) — production-surface module modeled on inference_path_59
- `river-rats-core/tests/test_phase2b_pilot_features.py` — rewritten (10 tests; was 17)
- `river-rats-core/tests/test_inference_path_61.py` (NEW) — 10 tests with regression check
- `river-rats-core/train_pilot_2b.py` (REMOVED) — pilot trainer; evidence preserved in earlier comms
- `review/comms/BUILDER_REPORT_PHASE2C_CLEANUP_2026-05-11.md` (NEW) — this PR's report

## Audit scope (~20-30 min — pre-merge milestone; 7-file PR)

Per dispatch (PR #400) §"QC stream — what you audit":

### Part A — Diff scope (TC-23)

1. **All 7 PR files match builder report list.** No additional files.
2. **TC-23 EXISTENCE**: `git ls-files river-rats-core/inference_path_61.py` returns the path; same for `tests/test_inference_path_61.py`.
3. **Removed file**: `git ls-files river-rats-core/train_pilot_2b.py` returns nothing (file removed from index).
4. **No oracle_router.py edits**.
5. **No inference_path_59.py edits**: canonical 59 frozen tuple UNCHANGED.
6. **No train_model_v9_student.py edits**: UNCHANGED per builder claim.
7. **No corpus / data / model-file edits**.

### Part B — Surface size attestation

8. **`len(feature_extractor.FEATURE_COLUMNS) == 61`** (was 63 in re-pilot; was 65 in v1 pilot).
9. **Indices 0-58**: unchanged canonical 59-feature production surface (regression check vs master pre-2-C).
10. **Index 59**: `players_to_act_after_hero`.
11. **Index 60**: `tpmk_kicker_rank`.
12. **Verify**: `nut_fd_blocker_multiway` + `broadway_pressure_multiway_facing` NOT in FEATURE_COLUMNS.

### Part C — inference_path_61 behavior verification

13. `inference_path_61.FEATURE_COLUMNS_61` is frozen tuple of length 61.
14. First 59 elements == `inference_path_59.FEATURE_COLUMNS_59` (byte-for-byte).
15. Last 2 elements are `('players_to_act_after_hero', 'tpmk_kicker_rank')`.
16. `features_from_dict_61(feat_dict)` returns numpy array of length 61.
17. **Bit-for-bit regression check**: for sample feat_dict, `features_from_dict_61(d)[:59] == features_from_dict_59(d)` per builder's `test_first_59_elements_match_59_path`.
18. Module-load assertion FIRES if first-59 don't match canonical (test by mutation).

### Part D — Test verification

19. Independently run `pytest river-rats-core/tests/test_phase2b_pilot_features.py`. Verify **10/10 PASS**.
20. Independently run `pytest river-rats-core/tests/test_inference_path_61.py`. Verify **10/10 PASS**.
21. Independently run `pytest river-rats-core/tests/test_inference_path_59.py`. Verify **12/13 PASS, 1 SKIPPED** (no regression; 59-path behavior preserved).
22. Independently run `pytest river-rats-core/tests/test_board_adjusted_hrp.py`. Verify **6/6 PASS** (canonical surface guard preserved).

### Part E — Non-NaN/Inf on 988-corpus

23. Independently spot-check 5-10 rows: all 61 features extract to numeric scalars (no NaN/Inf). Verify against builder's "988/988 finite" claim.

### Part F — Process discipline

24. **TC-X-DISPATCH-COMPLIANCE per PR #400**: all 8 tasks honored.
    - ✓ Task 1 Step 18 cleanup
    - ✓ Task 2 F constants
    - ✓ Task 3 tests cleanup
    - ✓ Task 4 inference_path_61
    - ✓ Task 4b test_inference_path_61
    - ✓ Task 5 train_pilot_2b (architect chose REMOVE; legitimate per dispatch "architect picks the cleaner option")
    - ✓ Task 6 inference_path_59 UNCHANGED
    - ✓ Task 7 oracle_router UNCHANGED
    - ✓ Task 8 builder report

25. **TC-X-OWNER-SCOPE-DISCIPLINE**: NO deviation from owner-ratified Option B; no features re-added; only Tasks 1-8 files touched.

### Part G — Scope-discipline note verification

26. **Builder explicit scope-discipline note** (§"Scope-discipline note"): 15 design-memo §4 candidates remain UNTESTED + deferred; architect did NOT re-introduce them. QC verifies feature_extractor.py contains NO additional features beyond the 2 winners.

## What this PR does NOT change

- ❌ Production code path (river-rats-core/ inference behavior unchanged for 59-path; new 61-path added but NOT yet routed via oracle_router)
- ❌ Models, corpus, training data (no production artifact production)
- ❌ Phase 1.5 ship state (vNext-HU-59 still in production via `oracle_router.py:34`)
- ❌ Solver-verification queue (48 spots HOLD-with-accepted-risk per owner-ratified §6.4)
- ❌ Phase 2-D / E / F / G / H scope

## What gates next (post-QC-PASS orchestrator sequence)

1. Orchestrator merges PR #401 on QC PASS
2. Orchestrator dispatches 2-D (4-way reference set design; 35 hands street-weighted per AMENDMENT 1 51/31/11/6)

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~20-30 min wall-clock (7-file PR; mostly straightforward verifications). QC writes:
- `~/river-rats-qc/findings/2026-05-11-pr401-phase2c-cleanup.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2C_CLEANUP_2026-05-11.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## SHOULD_FIX / BLOCKER classification guidance

- **BLOCKER**: surface size != 61; first-59 entries changed; inference_path_61 first-59 assertion fails OR doesn't validate canonical; bit-for-bit regression check fails; any test in test_inference_path_61 / test_phase2b_pilot_features fails; oracle_router / inference_path_59 / train_model_v9_student modified
- **SHOULD_FIX-substantive**: any of 15 design-memo candidates re-introduced; missing scope-discipline note; importance attribution missing
- **SHOULD_FIX-process**: minor docstring / wording / typo issues
- **PASS**: implementation sound + all attestations verified + dispatch compliance verified

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `bbda9d9` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 2-C dispatch: master `bbda9d9` (PR #400)
- Phase 2-B RE-PILOT builder: master `59978c5` (PR #397)
- Phase 2-B RE-PILOT QC PASS: master `36726d9` (PR #399)
- Phase 2-B PILOT v1 builder: master `fa0ea24` (PR #393)
- Phase 2-B PILOT v1 QC PASS: master `cfadc34` (PR #395)
- Phase 2-A design memo: master `0e5f91f` (PR #388) + QC PASS `a221a9b` (PR #391)
- Builder Phase 2-C report: `review/comms/BUILDER_REPORT_PHASE2C_CLEANUP_2026-05-11.md`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_spec_vs_infrastructure_code_drift.md`

**Status: QC stream — fire audit now on PR #401 Phase 2-C cleanup. ~20-30 min wall-clock. 26-item audit covering surface size (61) + first-59 canonical preservation + inference_path_61 behavior + 10/10 unit tests + bit-for-bit regression + non-NaN/Inf on 988-corpus + dispatch compliance + scope discipline. Builder explicitly claims compliance with all 8 dispatch tasks + scope-discipline note. After QC PASS + merge → orchestrator dispatches 2-D (4-way reference set design).**
