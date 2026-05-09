---
date: 2026-05-09
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #315 — Phase 1.5-B execution (Path α column-drop per PR #316 auth) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #315

PR #315: `programmer/phase15b-feature-prune-2026-05-09`. Head `8847f85827146ead14d440040d196b64fc8d44de`. Title: "Builder Phase 1.5-B (Path α column-drop per orchestrator PR #316): Steps 1-4 + §2.3 PASS; ready for QC re-audit".

Builder fired Phase 1.5-B execution per dispatch `MAIN_TERMINAL_PHASE15B_EXECUTION_DISPATCH_2026-05-09.md` (master `9491965`, PR #314), with Path α column-drop deviation authorized via `MAIN_TERMINAL_PHASE15B_STOP_RESOLUTION_PATH_ALPHA_2026-05-09.md` (master `29ebe1f`, PR #316).

**Diff summary** (from PR open at master `cbd839b`):
- 12 files / +2360 / -397
- Source mutations: `feature_extractor.py` -117 (Step 18 + 2 J-B compute fns); `feature_keys.py` -9 (J-B keys); `tests/test_features_125j.py` -196 (deleted); `tests/test_train_model_v9_student.py` +27/-30 (59-surface assertions); `train_model_v9_student.py` +16/-23 (surface size 61→59)
- Scripts: `scripts/generate_lever_c_situations.py` +4/-22 (active update); `scripts/assemble_125i_d_788.py` +17 (freeze-note); `scripts/build_corpus_revision_125i_mw40_verif_situations.py` +15 (freeze-note)
- Output artifacts (force-added): `data/corpus_combined_988_on_59_2026-05-09.jsonl` (988 rows); `data/corpus_combined_988_on_59_labels_2026-05-09.jsonl` (988 rows)
- Comms: `review/comms/BUILDER_REPORT_PHASE15B_2026-05-09.md` (+197); `review/comms/BUILDER_DIAGNOSTIC_PHASE15B_RNG_DETERMINISM_BLOCKER_2026-05-09.md` (+108; the original BLOCKED diagnostic preserved as audit trail)

**First execution sub-phase of Phase 1.5** → milestone-class for forward-binding (sets the 59-surface for 1.5-C/D). Pre-merge QC required per `feedback_qc_required_before_approval.md`.

## Audit scope (~15-20 min; 8-item base + Path α adjustments)

Per dispatch `MAIN_TERMINAL_PHASE15B_EXECUTION_DISPATCH_2026-05-09.md` §"QC stream — what you audit" + Path α adjustments per `MAIN_TERMINAL_PHASE15B_STOP_RESOLUTION_PATH_ALPHA_2026-05-09.md` §"QC stream — what you audit".

### Items 1-8 (per original dispatch + Path α adjustments)

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): expected files only — source diffs per §2.2 Step 1; 2 corpus jsonl files (force-added); builder report + diagnostic comm (preserved). NO unrelated edits / no model files / no prompt files.
2. **Source mutation matches §2.2 Step 1**: each listed deletion / update lands at the cited line numbers in the source diff. Any deviation flagged in builder report.
3. **TC-23 EXISTENCE git-tracked check** per `feedback_tc23_existence_must_be_git_tracked.md`: `git ls-files data/corpus_combined_988_on_59_*.jsonl` returns non-empty in PR's branch (force-added, NOT .gitignored).
4. **Bit-equality verification under Path α** (re-interpreted from original dispatch): both sides of §2.3 diff are produced by column-drop (left = column-drop reference; right = builder's output via column-drop); empty diff = trivial PASS + sanity check (verifies no inadvertent extra column drop). QC re-runs the §2.3 command on a fresh checkout.
5. **Output artifact spec compliance** (§2.4): 988 rows; each `feat_dict` has exactly 59 keys; non-feature keys preserved verbatim. QC samples a few rows.
6. **Pytest PASS**: `python -m pytest river-rats-core/tests/` PASS count matches builder report.
7. **Labels file convention** (§2.4): content-identical SHA-256 between source `corpus_combined_988_labels_2026-05-07.jsonl` and `corpus_combined_988_on_59_labels_2026-05-09.jsonl` (date suffix only differs; content unchanged because labels are feature-free).
8. **TC-X-DISPATCH-COMPLIANCE**: 4-step sequence + STOP conditions + negative scope all honored. No scope creep beyond Path α deviation.

### Path α adjustments (NEW Items 9, 10 from PR #316)

9. **Path α deviation justification chain** (per PR #316 §"QC stream"): builder report §"Path α deviation" cites PR #316 + original diagnostic; reasoning chain (J-B append-only-end-of-pipeline → column-drop bit-equivalent for this migration → no MC-derived drift) is sound.
10. **J-B append-only-end-of-pipeline independent verification**: QC verifies `feature_extractor.py:2645-2663` at master HEAD pre-PR-merge shows the J-B compute fns reading only existing feature values + no downstream Step 19+ reads. (Re-confirms architect's claim justifying column-drop for THIS migration.)

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~15-20 min wall-clock. QC writes:
- `~/river-rats-qc/findings/2026-05-09-pr315-phase15b-execution.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15B_EXECUTION_2026-05-09.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha` to current master per `project_qc_heartbeat_convention.md`

## What gates

- PR #315 merge → on QC PASS (orchestrator merges autonomously per standing directive while owner asleep — owner has ratified Path A direction)
- After PR #315 + verdict comm merge → orchestrator authors Phase 1.5-C dispatch per design memo §3 (5-seed re-train at 59-surface; pre-pad warm-start 45→59 via `prepad_baseline_booster`; PASS gate ≥ 33.00/40 mean across 5 seeds; output `models/v9_3way_v22_on_59/v9_3way_v22_on_59.json`) + merges autonomously
- 2 memory rule additions queued post-1.5-B-merge:
  - bit-equality verification on RNG-dependent features requires RNG-seed-preservation infrastructure
  - append-only-end-of-pipeline verification for column-drop migrations
- α/β decision (§4.2 close-hand-anchor) — owner-scope; resolves before 1.5-D.1 fires; standing directive lean β; non-blocking for 1.5-B/C
- LOOP CONTINUES

## Background — owner direction

Owner ratified Path A direction (current execution) and deferred Path C (drop v8-HU-38 dependency) for possibly later. Path α (column-drop) is in master + builder executed accordingly. No orchestration change.

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `cbd839b` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-B execution dispatch: master `9491965` (PR #314)
- Path α STOP resolution authorization: master `29ebe1f` (PR #316)
- Builder PR #315 head: `8847f85827146ead14d440040d196b64fc8d44de`
- Builder diagnostic (preserved as audit trail in PR): `BUILDER_DIAGNOSTIC_PHASE15B_RNG_DETERMINISM_BLOCKER_2026-05-09.md`
- Architect's design memo (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` (§2 spec; §2.3 verification; §2.4 output spec; §2.5 invariant tests scope)
- Wake-note: master `cbd839b` (PR #317; for owner-on-wake audit trail)

**Status: QC stream — fire audit now on PR #315. ~15-20 min wall-clock. 8-item + 2 Path α items audit. Heartbeat sync to current master at end of tick. Orchestrator merges PR #315 + QC verdict autonomously on PASS per standing directive.**
