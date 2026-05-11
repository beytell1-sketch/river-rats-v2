---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #397 — Phase 2-B RE-PILOT 4-feature re-engineered (Option A); 2/4 gate-pass + tpmk_kicker_rank breakthrough 9.18% — fire audit now (pre-merge milestone)
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #397 (Phase 2-B RE-PILOT 4-feature implementation)

PR #397: `builder-phase2-b-repilot-2026-05-11`. Head per push `origin/builder-phase2-b-repilot-2026-05-11`. Title: "Builder Phase 2-B RE-PILOT — 4 re-engineered (Option A); 2/4 gate-pass; tpmk_kicker_rank breakthrough 9.18%".

Builder Phase 2-B re-pilot per dispatch (PR #396, owner-ratified Option A) — kept 1 proven feature (`players_to_act_after_hero`), re-engineered 3 failed encodings, dropped 2 redundant. **Re-pilot gate result: 2/4 features pass.** Builder explicitly flags "Orchestrator-owner decision required" per dispatch §"2/4 row" REPORT.

This is the re-pilot evidence-gathering step. Per dispatch outcome table for 2/4 row: orchestrator triages → may surface to owner. The QC audit on this PR is about implementation + evidence-capture quality, NOT about whether all gates pass.

## Diff summary (per builder report §"Files in this PR")

6 files / net change (Step 18 4 features instead of 6; 17 tests instead of 21; train_pilot_2b rewritten for 63-feat surface):

- `river-rats-core/feature_extractor.py` — Step 18 replaced (4 features in order)
- `river-rats-core/feature_keys.py` — 4 F constants (was 6)
- `river-rats-core/tests/test_phase2b_pilot_features.py` — rewritten (17 tests; 4 feature classes + surface-aggregate)
- `river-rats-core/train_pilot_2b.py` — rewritten for 63-feature surface + 4-feature gates
- `review/comms/PILOT_2B_REPILOT_FEATURE_IMPORTANCE_2026-05-11.json` (NEW) — full importance dump
- `review/comms/BUILDER_REPORT_PHASE2B_REPILOT_2026-05-11.md` (NEW, ~175 lines) — re-pilot report

## Audit scope (~25-35 min — pre-merge milestone; 6-file PR)

Per dispatch (PR #396) §"QC stream — what you audit":

### Part A — Diff scope (TC-23)

1. **All 6 PR files match builder report list.** No additional files.
2. **TC-23 EXISTENCE**: `git ls-files` returns all 6 new/modified paths.
3. **No corpus / data / model-file edits** in PR.
4. **No oracle_router.py edits**.
5. **No inference_path_59.py edits**: canonical 59 frozen tuple UNCHANGED.
6. **No train_model_v9_student.py edits**: UNCHANGED per builder claim.

### Part B — Surface size attestation

7. **`len(FEATURE_COLUMNS) == 63`** in `feature_extractor.py`.
8. **Last 4 entries** are the 4 re-pilot features in dispatched order (players_to_act → tpmk_kicker_rank → broadway_pressure_multiway_facing → nut_fd_blocker_multiway; or builder's chosen Step 18 order; verify intentional).
9. **First 59 entries unchanged** vs master (production-surface integrity).
10. **Verify `test_first_59_match_canonical` passes** (builder claim).

### Part C — Per-feature unit test verification

11. Independently run `pytest river-rats-core/tests/test_phase2b_pilot_features.py`. Verify **17/17 PASS**.
12. Spot-check 2-3 unit tests for correctness of re-engineered features:
    - `tpmk_kicker_rank`: returns kicker rank int (2-14) when hand_category==TPMK; 0 otherwise
    - `nut_fd_blocker_multiway`: drops `facing_bet` gate vs v1; nonzero in CHECK spots with hand+blocker+MW
    - `broadway_pressure_multiway_facing`: composite at decision boundary; nonzero rate ~13%

### Part D — Re-engineering semantic verification (CRITICAL)

13. Each re-engineered candidate IS semantically different from PILOT v1 predecessor:
    - **tpmk_kicker_rank**: NEW encoding = `hand_category == TPMK ? kicker_rank : 0` (numeric kicker 2-14); NOT v1's `hand_category × J-high × hand_rank/10`
    - **nut_fd_blocker_multiway**: NEW encoding = `has_FD × nut_block × multiway` (NO facing_bet gate); v1 had `× facing_bet`
    - **broadway_pressure_multiway_facing**: NEW encoding = `broadway_turn × multiway × facing_bet` (composite at decision boundary); v1 was `count(broadway cards on board) if turn else 0`
14. Step 18 docstring records v1→v2 delta (builder claim) — verify docstrings exist.

### Part E — Non-NaN/Inf on 988-corpus

15. Independently spot-check 5-10 rows: all 63 features extract to numeric scalars (no NaN/Inf). Verify against builder's "988/988 finite" claim.

### Part F — Re-pilot trainer report verification

16. **Importance values match JSON exactly** to BUILDER_REPORT table:
    - tpmk_kicker_rank: 9.18% rank #2
    - players_to_act_after_hero: 3.36% rank #10 (regression: was 3.58% v1; ±1% gate ✓)
    - nut_fd_blocker_multiway: 1.87% rank #16 (was 1.53% v1; +22% but below 2% gate)
    - broadway_pressure_multiway_facing: 0.26% rank #41 (was 0.00% v1; below gate)
17. **Re-pilot gate evidence honestly reported**: 2/4 pass; builder did NOT mis-report.
18. **`players_to_act_after_hero` regression check**: 3.36% vs v1 3.58% = -0.22% (within ±1% gate ✓).

### Part G — Process discipline

19. **TC-X-DISPATCH-COMPLIANCE per PR #396**: builder honored all 14 dispatch directives (builder report §"Compliance with dispatch" checklist).
    - ✓ Owner-ratified Option A respected
    - ✓ 4 candidates (1 KEEP + 3 RE-ENG; 2 DROP) matches dispatch
    - ✓ Surface 65→63 ✓
    - ✓ First 59 unchanged
    - ✓ inference_path_59 + train_model_v9_student NOT touched
    - ✓ No oracle_router / data / models edits
    - ✓ STOP-condition compliance: did NOT improvise Option A2

20. **Builder explicitly STOP'd at 2/4 gate-pass row**. Per CLAUDE.md §5: hitting STOP-implication scenario + REPORT-not-improvise = HONORED. ✓

## Special audit consideration: 2/4 gate-pass is NOT a QC FAIL

Per dispatch §"Re-pilot gate outcome dispatching":
- "2/4 pass (2 re-engineered fail) → REPORT; likely further owner-direction needed"

2/4 gate-pass is a triage-trigger, NOT a QC FAIL. Builder produced honest evidence; tpmk_kicker_rank breakthrough validates Option A direction. The QC audit assesses implementation + evidence-capture quality only.

If implementation sound + evidence honestly captured → PASS (orchestrator merges + sequences owner-direction next).

## What this PR does NOT change

- ❌ Production code path (river-rats-core/ inference behavior unchanged)
- ❌ Models, corpus, training data (no production artifact production)
- ❌ Phase 1.5 ship state (vNext-HU-59 still in production via `oracle_router.py:34`)
- ❌ Solver-verification queue (48 spots HOLD-with-accepted-risk per owner-ratified §6.4)
- ❌ Phase 2-C / 2-D scope (this is 2-B re-pilot only)

## What gates next (post-QC-PASS orchestrator sequence)

1. Orchestrator merges PR #397 on QC PASS
2. Orchestrator surfaces the 3 builder-offered options to owner for direction:
   - **Option A2 — Third iteration** on 2 sub-threshold features (3-5h). Builder leans against for broadway (fundamentally absorbed); leans for nut_fd (real but absorbed).
   - **Option B — Partial-proceed with 2 winners** (Builder + orchestrator lean per quality default + scope discipline): promote `players_to_act_after_hero` + `tpmk_kicker_rank` to 2-C/D; drop `nut_fd_blocker_multiway` + `broadway_pressure_multiway_facing`; surface lands at 61.
   - **Option C — Mixed**: ship 2 winners + 1-2h third iteration ONLY on nut_fd; drop broadway permanently; surface lands at 62 or 63.
3. Owner decides → orchestrator dispatches 2-C (full feature impl scope) with the agreed feature subset

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~25-35 min wall-clock. QC writes:
- `~/river-rats-qc/findings/2026-05-11-pr397-phase2b-repilot.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2B_REPILOT_2026-05-11.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## SHOULD_FIX / BLOCKER classification guidance

- **BLOCKER**: importance values disagree with the JSON; non-NaN/Inf claim is false; FEATURE_COLUMNS first-59 changed; oracle_router touched; inference_path_59 canonical-59 tuple changed; re-engineered features semantically identical to PILOT v1 predecessors (no real re-engineering done); pilot gate evidence misrepresented; test_phase2b_pilot_features.py fails some tests
- **SHOULD_FIX-substantive**: missing per-feature gate evidence; importance JSON malformed; train_pilot_2b logic errors invalidating importance signal
- **SHOULD_FIX-process**: docstrings missing v1→v2 delta; minor wording / typo issues
- **PASS**: implementation sound + evidence honestly captured + dispatch compliance verified

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `a668002` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 2-B RE-PILOT dispatch: master `a668002` (PR #396)
- Phase 2-B PILOT v1 builder: master `fa0ea24` (PR #393)
- Phase 2-B PILOT v1 QC PASS: master `cfadc34` (PR #395)
- Phase 2-A design memo: master `0e5f91f` (PR #388) + QC PASS `a221a9b` (PR #391)
- PILOT v1 builder report: `review/comms/BUILDER_REPORT_PHASE2B_PILOT_2026-05-11.md`
- Pilot data: `data/corpus_combined_988_on_59_*_2026-05-09.jsonl`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`

**Status: QC stream — fire audit now on PR #397 Phase 2-B RE-PILOT 4-feature implementation. ~25-35 min wall-clock. 20-item audit. 2/4 gate-pass is EXPECTED triage-trigger per dispatch — audit assesses implementation + evidence-capture quality. tpmk_kicker_rank 9.18% breakthrough validates Option A re-engineering direction. After QC PASS + merge → orchestrator surfaces 3 options (A2 third iteration / B partial-proceed-2 / C mixed) for owner direction.**
