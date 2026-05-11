---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous on owner-direction)
to: LEAD-PROGRAMMER (architect-hat + ml-architect-hat + gto-expert-hat)
re: Phase 2-C — cleanup Step 18 to retain only 2 confirmed winners; surface 63→61; production-surface prep — per owner-ratified Option B
status: DISPATCH — fire now (Phase 2-B re-pilot merged at master 36726d9; PR #397 + #399 PASS; owner ratified Option B 2026-05-11 ~08:10 SAST)
---

# Phase 2-C cleanup dispatch — retain 2 winners; surface 61; production prep

## Owner ratification record (2026-05-11 ~08:10 SAST)

Owner answered AskUserQuestion "Re-pilot got 2/4 pass with tpmk_kicker_rank breakthrough — how to proceed?" with:

**"B — Partial-proceed with 2 winners (Recommended)"**

Locks the following direction:
- PROMOTE `players_to_act_after_hero` (3.36% importance; AMENDMENT 1 validated; stable across pilots)
- PROMOTE `tpmk_kicker_rank` (9.18% importance, rank #2/63; D5 MW-40 breakthrough via numeric kicker encoding)
- DROP `nut_fd_blocker_multiway` (1.87% real but absorbed by `nut_made_block_pct` + `flush_draw_block_pct` baseline)
- DROP `broadway_pressure_multiway_facing` (0.26% fundamentally absorbed by `high_card_rank` + `danger_score` + `is_paired` baseline)
- Surface lands at **61 features** (59 baseline + 2 confirmed winners)
- 15 additional candidates from design memo §4 (8 D5 + 4 4-way + 3 re-raise; never piloted) are DROPPED from Phase 2 scope per quality-default + scope-discipline; can be revisited in future phase if new evidence demands

## Phase 2 scope reduction summary

Per owner-ratified Option B, Phase 2 ambition narrows substantively:
- **Original Phase 2-A design memo** (PR #388, owner-ratified all 9 owner-scope items): 21 candidates → 74-80 surface; 12 sub-phase candidates remaining for 2-C
- **Post-pilot reality** (PR #393): 1/6 pass; only `players_to_act` survives  
- **Post-re-pilot reality** (PR #397): 2/4 pass; `players_to_act` + `tpmk_kicker_rank` survive
- **Phase 2-C scope-reduced**: NO new features to implement (the 2 winners are already in Step 18); CLEANUP + production prep only

This is the empirical pilot-first standing rule at work — surface 61 reflects what the evidence supports, not what the original architect ambition projected.

## What Phase 2-C does (cleanup + production-surface prep)

### Task 1 — Step 18 cleanup in `feature_extractor.py`

- DROP `nut_fd_blocker_multiway` from Step 18 (lines for this feature)
- DROP `broadway_pressure_multiway_facing` from Step 18 (lines for this feature)
- KEEP `players_to_act_after_hero` (unchanged)
- KEEP `tpmk_kicker_rank` (unchanged)
- `FEATURE_COLUMNS` shrinks 63 → 61 (canonical order preserved; last 2 entries are the 2 winners)

### Task 2 — `feature_keys.py` F-class constants

- DROP 2 F constants for the 2 dropped features
- KEEP 2 F constants for the 2 retained features (unchanged)

### Task 3 — Tests cleanup in `tests/test_phase2b_pilot_features.py`

- DROP test classes for `nut_fd_blocker_multiway` + `broadway_pressure_multiway_facing`
- KEEP test classes for `players_to_act_after_hero` + `tpmk_kicker_rank` (unchanged)
- UPDATE `test_surface_size_is_63` to `test_surface_size_is_61` (assertion 63→61)
- UPDATE the "last N entries" assertion for re-pilot features (last 2)

### Task 4 — Production-surface dispatch prep — NEW `inference_path_61.py`

Per design memo §4.3 Option (b) — preserve 59-path as middle tier; add NEW `inference_path_61.py` for the new surface size. Modeled on `inference_path_59.py`:

- Public `features_from_dict_61(feat_dict)` returns 61-element numpy array in canonical FEATURE_COLUMNS_61 order
- Public `FEATURE_COLUMNS_61` alias (frozen tuple)
- Module-load assertion: `len(FEATURE_COLUMNS_61) == 61` AND first-59 entries == `FEATURE_COLUMNS_59` AND last-2 entries are the 2 winners in canonical order
- Tests in `tests/test_inference_path_61.py` mirroring `test_inference_path_59.py`

### Task 5 — Trainer compatibility

- `train_model_v9_student.py` UNCHANGED (already on `inference_path_59.FEATURE_COLUMNS_59`; production trainer remains on 59-feat baseline until 2-F retrain on the new 61-feat surface)
- `train_pilot_2b.py` — RENAME to `train_pilot_2b_legacy.py` and add module-header docstring noting it's the re-pilot trainer (historical reference; not used in production); OR remove entirely if no provenance value
- Architect picks the cleaner option

### Task 6 — `inference_path_59.py` UNCHANGED

- Canonical 59 frozen tuple UNCHANGED
- Module-load assertion behavior UNCHANGED
- Production HU + 3-way models continue to build 59-element arrays from this module

### Task 7 — `oracle_router.py` UNCHANGED in 2-C

- Router swap to 61-feat dispatch happens in **2-H** (production swap PR after 2-F + 2-G retrains complete)
- Phase 2-C does NOT modify oracle_router

### Task 8 — Phase 2-C report

`review/comms/BUILDER_REPORT_PHASE2C_CLEANUP_2026-05-11.md` — concise (50-100 lines) covering:
- Step 18 + FEATURE_COLUMNS state (61 features, last 2 are winners)
- Tests state (all PASS; reduced from 17 to ~10 for the 2 retained features)
- `inference_path_61` module behavior (load-time assertions; FEATURE_COLUMNS_61 frozen)
- Trainer compat verified (v9 student trainer still on 59-baseline)
- Per-feature non-NaN/Inf on 988-corpus
- Scope of Phase 2-C: cleanup + production prep ONLY; NO 2-D/E/F/G/H scope leak

## What Phase 2-C does NOT do

Per design memo §5 + §7 + owner-ratified Option B + `feedback_pilot_first_for_long_jobs.md`:

- ❌ Does NOT implement the other 15 design-memo candidates (deferred indefinitely per Option B; owner can revisit in future phase)
- ❌ Does NOT touch `oracle_router.py` (2-H scope)
- ❌ Does NOT build the 4-way reference set (2-D scope)
- ❌ Does NOT generate or label corpus (2-E scope; 2-E.0 labeller readiness gate first)
- ❌ Does NOT retrain production models (2-F + 2-G)
- ❌ Does NOT modify `inference_path_59.py` canonical 59 tuple
- ❌ Does NOT drain solver-verification queue (HOLD per owner-ratified §6.4)
- ❌ Does NOT touch v8-HU / vNext-HU production model files

## STOP conditions (per CLAUDE.md §5)

- `inference_path_61.py` first-59 assertion fails (first-59 entries don't match `FEATURE_COLUMNS_59`) → STOP / REPORT
- `feature_extractor.FEATURE_COLUMNS` not exactly 61 elements after cleanup → STOP / REPORT
- Any test failure in test_phase2b_pilot_features.py OR test_inference_path_61.py → STOP / REPORT
- TC-23 EXISTENCE on new `inference_path_61.py`: must be `git ls-files`-visible after commit
- TC-X-OWNER-SCOPE-DISCIPLINE: NO deviation from owner-ratified Option B; e.g., do NOT introduce additional features even if they appear "obvious"; do NOT touch any other files outside Tasks 1-8 above

## QC stream — what you audit (pre-merge milestone)

Per `feedback_qc_required_before_approval.md`:

1. **Diff scope** (TC-23):
   - `river-rats-core/feature_extractor.py` — Step 18 cleanup
   - `river-rats-core/feature_keys.py` — F constant drops
   - `river-rats-core/tests/test_phase2b_pilot_features.py` — test class drops + surface size assertion update
   - `river-rats-core/inference_path_61.py` (NEW) — production-surface module
   - `river-rats-core/tests/test_inference_path_61.py` (NEW) — module tests
   - `river-rats-core/train_pilot_2b.py` — rename or removal (architect call)
   - `review/comms/BUILDER_REPORT_PHASE2C_CLEANUP_2026-05-11.md` (NEW)
   - NO oracle_router / data / model-file / inference_path_59 (canonical-59) / train_model_v9_student edits

2. **Surface size attestation**:
   - `len(FEATURE_COLUMNS) == 61` in feature_extractor.py
   - `len(FEATURE_COLUMNS_61) == 61` in inference_path_61.py
   - First 59 entries unchanged (match canonical FEATURE_COLUMNS_59)
   - Last 2 entries in agreed order: `players_to_act_after_hero` + `tpmk_kicker_rank` (or architect's chosen order if different; verify intentional)

3. **inference_path_61 behavior verification**:
   - `features_from_dict_61(feat_dict)` returns numpy array of length 61
   - First-59 elements match `inference_path_59.features_from_dict_59(feat_dict)` output bit-for-bit
   - Last-2 elements are the 2 winners' values per feat_dict
   - Load-time assertion FIRES if first-59 don't match canonical (test by mutation)

4. **Test verification**:
   - `pytest tests/test_phase2b_pilot_features.py` → all PASS for retained 2 features
   - `pytest tests/test_inference_path_61.py` → all PASS
   - `pytest tests/test_inference_path_59.py` → all PASS (regression — must not break)

5. **Non-NaN/Inf on 988-corpus** for retained features.

6. **Production trainer compatibility**: `train_model_v9_student.py` still imports from `inference_path_59` (canonical 59); trainer behavior verifiably unchanged.

7. **TC-X-DISPATCH-COMPLIANCE**: all 8 tasks honored; no scope leak; no Option-B-deviation features added back.

## What gates

- Builder Phase 2-C PR → QC trigger when pushed
- On QC PASS → orchestrator merges autonomously + dispatches 2-D (4-way reference set design) OR awaits owner direction if 2-D scope needs revisit
- On QC SHOULD_FIX → amend + re-fire
- On QC BLOCKER → hold + redo
- STOP condition → REPORT; orchestrator triages

## Phase 2 sub-phase sequence post-2-C (per design memo §5)

After 2-C clears:
- **2-D** — 4-way reference set design (35 hands street-weighted per AMENDMENT 1 51/31/11/6)
- **2-E.0** — 4-way labeller readiness (5-hand pilot validation per AMENDMENT 3)
- **2-E** — 4-way labelling pipeline (~750 lookalikes)
- **2-F** — 3-way re-extract + retrain on 61-feat surface (D5 path; gate ≥36/40)
- **2-G** — 4-way retrain on 61-feat surface + new 4-way corpus (gate ≥28/35 street-weighted)
- **2-H** — Production swap (force-add new 3-way + 4-way models; oracle_router updates; inference_path_61 in production)

Note: with only 2 features (instead of 15-17), the D5 hypothesis test in 2-F is on a much narrower surface than the design memo's original ≥36/40 gate calibration. Architect may surface this as a SHOULD_FIX-substantive concern at 2-F dispatch time (gate may need recalibration for the smaller surface delta).

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `36726d9` ✓
- Diff vs master: 1 file (this dispatch)
- Log vs master: 1 commit

## References

- Phase 2-B RE-PILOT builder PR: master `59978c5` (PR #397)
- Phase 2-B RE-PILOT QC PASS: master `36726d9` (PR #399)
- Phase 2-B RE-PILOT dispatch (Option A): master `a668002` (PR #396)
- Phase 2-B PILOT v1 builder: master `fa0ea24` (PR #393)
- Phase 2-B PILOT v1 QC PASS: master `cfadc34` (PR #395)
- Phase 2-A design memo: master `0e5f91f` (PR #388) + QC PASS `a221a9b` (PR #391)
- Design memo §4.3 inference path versioning: `review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md` lines 535-541
- Design memo §5 sub-phase decomposition: lines 543-585
- Re-pilot builder report: `review/comms/BUILDER_REPORT_PHASE2B_REPILOT_2026-05-11.md`
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_qc_required_before_approval.md`

**Status: Phase 2-C dispatch per owner-ratified Option B. Cleanup Step 18 to retain only 2 winners (players_to_act + tpmk_kicker_rank); surface 63→61; NEW inference_path_61.py module for production-surface dispatch. Scope-reduced from design memo §4's original 12-candidate ambition to 0-candidate cleanup (15 untested candidates deferred per Option B). After 2-C QC PASS + merge → 2-D dispatch (4-way reference set design).**
