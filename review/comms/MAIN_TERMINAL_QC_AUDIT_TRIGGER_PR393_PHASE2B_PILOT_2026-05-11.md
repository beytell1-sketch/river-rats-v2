---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #393 — Phase 2-B PILOT 6-feature implementation (59→65 surface; 1/6 importance gate-pass; production-surface integrity guard added) — fire audit now (pre-merge milestone)
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #393 (Phase 2-B PILOT 6-feature implementation)

PR #393: `builder-phase2-b-pilot-2026-05-11`. Head per push `origin/builder-phase2-b-pilot-2026-05-11`. Title: "Builder Phase 2-B PILOT — 6-feature impl + 1-seed importance evidence (1/6 gate-pass)".

Builder Phase 2-B pilot per dispatch (PR #392) — 6 candidate features implemented + tested + 1-seed pilot-trained against existing 988-corpus. **Pilot gate result: 1/6 features pass (broad FAIL per dispatch pilot-gate-outcome table).** Builder explicitly flags "Orchestrator-owner decision required" before 2-C/D fires.

This is the pilot evidence-gathering step. Pilot result (FAIL or PASS) is itself the deliverable; QC audits the IMPLEMENTATION + EVIDENCE-CAPTURE quality, not whether gates pass. Owner-direction is sequenced post-merge.

## Diff summary (per builder report §"Files in this PR")

10 files / +600-700 lines net:

- `river-rats-core/feature_extractor.py` (+86) — Step 18 with 6 new pilot features
- `river-rats-core/feature_keys.py` (+10) — 6 F-class constants
- `river-rats-core/inference_path_59.py` (~40 net) — **production-surface integrity guard refactor (was dispatch-excluded; see §Scope-deviation below)**
- `river-rats-core/train_model_v9_student.py` (~6) — **import source change (was dispatch-excluded; see §Scope-deviation below)**
- `river-rats-core/tests/test_board_adjusted_hrp.py` (~30 net) — pre-existing technical-debt `TestFeatureCountIs55` rename/update
- `river-rats-core/tests/test_inference_path_59.py` (~5) — first-59 assertion adjustment
- `river-rats-core/tests/test_phase2b_pilot_features.py` (NEW, ~250) — 21 unit tests
- `river-rats-core/train_pilot_2b.py` (NEW, ~230) — pilot trainer
- `review/comms/PILOT_2B_FEATURE_IMPORTANCE_2026-05-11.json` (NEW) — importance dump
- `review/comms/BUILDER_REPORT_PHASE2B_PILOT_2026-05-11.md` (NEW, ~220 lines) — this PR's report

## Audit scope (~25-35 min — pre-merge milestone; 10-file PR)

Per dispatch (PR #392) §"QC stream — what you audit":

### Part A — Diff scope (TC-23)

1. **All 10 PR files match builder report list.** No additional files.
2. **TC-23 EXISTENCE**: `git ls-files` returns all 10 new/modified paths.
3. **No corpus / data / model-file edits** in PR (architect-only feature work in this pilot).
4. **No oracle_router.py edits**.

### Part B — Surface size attestation

5. **`len(FEATURE_COLUMNS) == 65`** in `feature_extractor.py`.
6. **Last 6 entries** are the 6 pilot features in the order builder reported (tpmk → broadway → nut_fd → players_to_act → realization → closing_action).
7. **First 59 entries unchanged** vs master (production-surface integrity).

### Part C — Per-feature unit test verification

8. Independently run `pytest river-rats-core/tests/test_phase2b_pilot_features.py`. Verify **21/21 PASS**.
9. Spot-check 2-3 unit tests for correctness (e.g., `realization` lookup HU=1.0, 3w=0.85, 4w=0.75, 5w=0.70; `closing_action` HU-IP=1, HU-OOP=0, MW-OOP=0).

### Part D — Non-NaN/Inf on 988-corpus

10. Independently spot-check 5-10 rows: all 65 features extract to numeric scalars (no NaN/Inf). Verify against builder's "988/988 finite, no NaN/Inf" claim.

### Part E — Pilot trainer report verification

11. Per-feature importance scores numeric + non-NaN; **match `PILOT_2B_FEATURE_IMPORTANCE_2026-05-11.json` exactly** to BUILDER_REPORT table:
    - players_to_act_after_hero: 3.58% rank #10
    - nut_fd_multiway_pressure_with_blocker: 1.53% rank #17
    - tpmk_position_with_kicker_strength: 0.00% rank #62
    - broadway_density_completed_on_turn: 0.00% rank #63
    - multiway_equity_realization_factor: 0.00% rank #64
    - closing_action: 0.00% rank #65
12. **Pilot gate evidence honestly reported**: 1/6 pass (broad FAIL); builder did NOT mis-report; no skipping of importance values.

### Part F — Scope-deviation assessment (CRITICAL)

13. **`inference_path_59.py` change** — dispatch §"What Phase 2-B does NOT do": "Does NOT touch inference path 59 module".
    - Builder justification: "Refactored to pin canonical 59-feature production surface explicitly (frozen tuple `_CANONICAL_FEATURE_COLUMNS_59`) so that Phase 2-B PILOT extension to 65 features does NOT trip the assertion. Any reorder/rename/drop of the FIRST 59 entries DOES trip the assertion. Production HU + 3-way models continue to build 59-element arrays in canonical order. Load-time guard change; no inference-path behavior change."
    - **QC classification**: necessary engineering to preserve production-surface integrity when FEATURE_COLUMNS expands 59→65; without this change, the load-time assertion would break + the pilot trainer would crash on the existing v8/vNext production models. Builder chose correctness over strict scope-adherence.
    - **QC verdict**: SHOULD_FIX-process (dispatch should have allowed this; orchestrator notes for future dispatches) BUT NOT BLOCKER if behavior is verifiably unchanged.
    - **Independent verification needed**: confirm inference_path_59 BEHAVIOR (not just code) is preserved — sample-run `inference_path_59.features_from_dict_59()` on a known-good feat_dict; expect identical output to pre-change.

14. **`train_model_v9_student.py` change** — dispatch §"What Phase 2-B does NOT do": NOT-explicitly-excluded but spirit-of-dispatch excludes trainer changes.
    - Builder justification: "v9 student trainer frozen on 59-feature surface (Phase 1.5-B). Changed import source from `feature_extractor.FEATURE_COLUMNS` (now 65) to `inference_path_59.FEATURE_COLUMNS_59` (canonical 59). Trainer behavior unchanged."
    - **QC classification**: necessary engineering to preserve trainer-on-59-baseline when FEATURE_COLUMNS expands; failure to do this would have caused the v9 trainer to silently switch to 65-feat surface (very bad).
    - **QC verdict**: SHOULD_FIX-process; NOT BLOCKER if behavior is verifiably unchanged.
    - **Independent verification needed**: confirm v9 student trainer would produce IDENTICAL output bit-for-bit if rerun with this import change vs the prior master state (read the diff; confirm no semantic change to trainer behavior).

### Part G — Test-suite stability

15. Per builder: "Pre-existing test-suite SIGABRT instability: not caused by these changes; unrelated to feature work. Reproducible on master pre-pilot."
    - QC reproduces on master pre-pilot (sample-run a passing-on-master test suite subset; confirm SIGABRT pre-existing).
    - If reproducible on master: NOT a pilot blocker; note as separate existing-debt observation.
    - If NEW from pilot: BLOCKER.

### Part H — Process discipline

16. **TC-X-DISPATCH-COMPLIANCE**: builder honored 9-of-10 dispatch directives:
    - ✅ 6-candidate pilot (3 D5 + 2 4-way + 1 re-raise) ✓
    - ✅ feature_extractor.py + feature_keys.py + unit tests ✓
    - ✅ 1-seed pilot trainer ✓
    - ✅ pilot gate evidence honestly reported (FAIL) ✓
    - ✅ NO oracle_router edits ✓
    - ✅ NO data/corpus edits ✓
    - ✅ NO model artifact production ✓
    - ✅ NO solver-queue drain ✓
    - ✅ Surface size attestation (65) ✓
    - ⚠️ Inference_path_59 + train_model_v9_student touched (SHOULD_FIX-process; see Part F)

17. **STOP-condition compliance**: builder hit a STOP-implication scenario (pilot gate fail) and explicitly STOP'd to report + did NOT improvise re-engineering ("Not improvising re-engineering without explicit direction"). Honored CLAUDE.md §5 + dispatch §"STOP conditions". ✓

## Special audit consideration: pilot gate FAIL is NOT a QC FAIL

Per dispatch §"Pilot gate outcome dispatching":
- "<3 of 6 clear (broad fail) → HALT 2-C; escalate to 'is the issue elsewhere' investigation"

Pilot gate FAIL is **expected** per pilot-first standing rule + design memo §2.3 + §3.4. The pilot's job IS to fail when encoding is wrong. The QC audit on this PR is about implementation + evidence-capture quality, NOT about whether the gate passes.

If implementation is sound + evidence is honestly captured → PASS (orchestrator merges + sequences owner-direction next).

## What this PR does NOT change

- ❌ Production code path (river-rats-core/ inference behavior unchanged)
- ❌ Models, corpus, training data (no production artifact production)
- ❌ Phase 1.5 ship state (vNext-HU-59 still in production via `oracle_router.py:34`)
- ❌ Solver-verification queue (48 spots HOLD-with-accepted-risk per owner-ratified §6.4)
- ❌ Phase 2-C / 2-D scope (this is 2-B pilot only)

## What gates next (post-QC-PASS orchestrator sequence)

1. Orchestrator merges PR #393 on QC PASS
2. Orchestrator surfaces the 3 builder-offered options to owner for direction:
   - **Option A — Re-engineer + re-pilot** (3-5h): keep players_to_act, redesign 3 failed encodings, drop 2 redundant. Builder + orchestrator lean per quality default.
   - **Option B — Partial-gate proceed**: promote only players_to_act_after_hero to 2-C/D; surface lands at 60. Save 5-8h.
   - **Option C — Defer to Phase 3 / replan**: park Phase 2 build; redesign surface from scratch with importance evidence.
3. Owner decides → orchestrator dispatches next direction (re-pilot, partial-proceed-2-C, or Phase-3-park)

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~25-35 min wall-clock (10-file pre-merge milestone). QC writes:
- `~/river-rats-qc/findings/2026-05-11-pr393-phase2b-pilot.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2B_PILOT_2026-05-11.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## SHOULD_FIX / BLOCKER classification guidance

- **BLOCKER**: importance values disagree with the JSON; non-NaN/Inf claim is false; FEATURE_COLUMNS first-59 changed; oracle_router touched; pilot gate evidence misrepresented; test_phase2b_pilot_features.py fails some tests; inference_path_59 behavior verifiably changed (not just refactored)
- **SHOULD_FIX-substantive**: pilot gate evidence missing or incomplete for any candidate; importance dump JSON malformed; train_pilot_2b.py logic errors invalidating the importance signal; pre-existing test SIGABRT turns out to be caused by this PR
- **SHOULD_FIX-process**: inference_path_59 + train_model_v9_student dispatch-deviation (necessary engineering but should be acknowledged); orchestrator notes for future dispatches that "production-surface integrity guard maintenance" is implicitly allowed scope
- **PASS**: implementation sound + evidence honestly captured + scope-deviation justified

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `e69c724` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 2-B dispatch: master `e69c724` (PR #392)
- Phase 2-A design memo: master `0e5f91f` (PR #388) + QC PASS `a221a9b` (PR #391)
- D5 blueprint analog: `review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md`
- Pilot data: `data/corpus_combined_988_on_59_*_2026-05-09.jsonl`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_spec_vs_infrastructure_code_drift.md`

**Status: QC stream — fire audit now on PR #393 Phase 2-B PILOT 6-feature implementation. ~25-35 min wall-clock. 17-item audit. Pilot gate FAIL is EXPECTED — audit assesses implementation + evidence-capture quality. Scope-deviation (inference_path_59 + train_model_v9_student) is necessary engineering per builder justification + likely SHOULD_FIX-process not BLOCKER. After QC PASS + merge → orchestrator surfaces 3 builder options (Re-engineer+re-pilot / Partial-proceed / Phase-3-defer) for owner direction.**
