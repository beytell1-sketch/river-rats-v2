---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #382 — Phase 1.5-E PR-B (production swap — vNext-HU-59 in production via oracle_router.py:34; v8-HU force-added rollback safety; 22/22 coaching-pipeline tests PASS; Phase 1.5 SHIPS on merge) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #382 (1.5-E PR-B PRODUCTION SWAP)

PR #382: `builder-phase15e-pr-b-production-swap-2026-05-11`. Head `09da54ef690028f000afae92b4a048721bccf23c`. Title: "Builder Phase 1.5-E PR-B: production swap — vNext-HU-59 in production; Phase 1.5 SHIPS".

Builder fired PR-B per AMENDMENT (PR #378) Option C §"PR-B: Production swap" + original 1.5-E dispatch (PR #376) §"Builder deliverables (a)-(e)", after PR-A inference path cleared (PR #379 + QC PR #381 PASS · 0/0/0).

**This is the SHIP PR for Phase 1.5.** On merge: Phase 1.5 SHIPS (vNext-HU-59 production HU oracle; 3-way + multiway routing unchanged).

## Diff at oracle_router.py:34 (per builder report)

```diff
 _MODEL_FILES = {
-    1: 'gto_model_v8_hu.json',
+    1: 'gto_model_vNext_hu_59feat.json',
     2: 'gto_model_v9_3way.json',
     3: 'gto_model_v9_4way.json',
     4: 'gto_model_v9_5way.json',
 }
```

## Coaching-pipeline tests: 22/22 PASS (1 skip)

Skipped test = legacy-55-path-via-default-router (no longer applicable post-swap; coverage preserved via `test_legacy_v8_hu_still_works_via_55_path` which loads v8 directly).

## Smoke verified (per builder report)

`OracleRouter().predict(feat_dict, num_opponents=1)` on AhKs/Ad8c3h flop:
- HU n_features: 59
- classes: 5
- action=BET confidence=0.996
- Matches HU-1.1 anchor (canonical TPTK c-bet)

**Diff summary** (per `gh pr view 382`): 6 files / +200 / -16:
- `river-rats-core/models/gto_model_vNext_hu_59feat.json` — NEW (force-added; production HU oracle; +1 line metadata in git ls; ~5-15 MB binary)
- `river-rats-core/models/gto_model_v8_hu.json` — NEW (force-added; rollback safety net per Option B; closes §1.2 attestation gap symmetrically; +1 line metadata)
- `river-rats-core/oracle_router.py` (+1/-1) — 1-line swap at line 34
- `river-rats-core/tests/test_oracle_router.py` (+9/-6) — 2 fixture updates (post-swap alignment)
- `river-rats-core/tests/test_inference_path_59.py` (+8/-9) — 1 fixture update (uses `_MODEL_FILES[1]` post-swap filename)
- `review/comms/BUILDER_REPORT_PHASE15E_PR_B_PRODUCTION_SWAP_2026-05-11.md` (+180) — full delivery report

## Audit scope (~15-20 min)

Per AMENDMENT (PR #378) §"QC stream — what you audit (For PR-B)":

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): 6 PR files. NO other source/data edits beyond:
   - 2 force-added model files
   - oracle_router.py 1-line swap
   - 2 test fixture updates (necessary for post-swap fixtures)
   - 1 builder report
   - NO design memo edits; NO data/ edits; NO trainer/corpus edits; NO inference_path_59 edits (already merged in PR-A)

2. **Force-add verification:** independently run `git ls-files river-rats-core/models/gto_model_vNext_hu_59feat.json` AND `git ls-files river-rats-core/models/gto_model_v8_hu.json` — both should return the path (per `feedback_tc23_existence_must_be_git_tracked.md`). File sizes reasonable (vNext ~5-15 MB; v8 ~12 MB).

3. **oracle_router.py:34 diff verification:** read the diff. Verify:
   - ONLY line 34 changed (`_MODEL_FILES[1]` swap from v8 → vNext)
   - Positions 2/3/4 (3-way/4-way/5-way) UNCHANGED
   - Legacy filename comments preserved (if present)

4. **Coaching-pipeline tests: 22/22 PASS verified:** independently sample-run 2-3 tests; confirm PASS. Verify the 1 skip is legitimate (legacy-55-path-via-default-router not applicable post-swap; coverage preserved via direct-load test).

5. **Smoke load test verification:** independently run `OracleRouter().predict(feat_dict, num_opponents=1)` on a sample input; verify:
   - vNext model loaded at position 1
   - `_n_features == 59` (uses NEW 59-path from PR-A)
   - Predict returns valid 5-class output (no crash; no garbage)

6. **Multi-way regression:** sample-run a 3-way test (`num_opponents=2` or `num_opponents=3`) and a multiway test (`num_opponents=4`); confirm positions 2/3/4 still load + predict correctly.

7. **Provenance link:** `gto_model_vNext_hu_59feat.json` provenance docstring (in `train_model_vNext_hu.py` from PR 1 of 1.5-D.4) traceable from this PR; commit chain links model artifact to its training script per §5.1.

8. **TC-X-DISPATCH-COMPLIANCE per AMENDMENT (PR #378) + original (PR #376):** all dispatch requirements honored:
   - ❌ Does NOT modify trained model artifacts (loaded as-is from disk) ✓
   - ❌ Does NOT touch corpus/data files ✓
   - ❌ Does NOT solver-verify queue spots ✓
   - ❌ Does NOT change ship gate ✓ (already PASSED in 1.5-D.4)
   - ❌ Does NOT trigger retrain ✓
   - ✅ Does swap production HU oracle from v8 → vNext (the whole point of PR-B)

## Special audit consideration: this is the SHIP PR

This PR-B merge SHIPS Phase 1.5. After merge:
- Production HU oracle = vNext-HU-59 (28/30 ship-gate-clear; +10 over v8-HU-38)
- 3-way oracle = v9-3way-on-59 (unchanged; was already in production)
- Multiway routing = unchanged (positions 2/3/4 in `_MODEL_FILES`)
- Phase 1.5 SHIP boundary = MET

Post-ship items (out of 1.5-E scope; for future dispatches):
- Solver-verification queue (48 spots) drain when solver online; retrain delta if disagreements (per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`)
- Design memo §4.6 footnote amendment (acknowledge actual v8-HU baseline 18/30 vs projected 26-28/30)
- HU-6.5 corpus-exclusion-gap design refinement (consider including HU-6.5 lookalikes in next retrain corpus)
- Phase 2 D5 (deferred per blueprint memo per `project_v9_3way_ceiling.md`)

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~15-20 min wall-clock. QC writes:
- `~/river-rats-qc/findings/2026-05-11-pr382-phase15e-pr-b-production-swap.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15E_PR_B_PRODUCTION_SWAP_2026-05-11.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha` to current master

## What gates

- PR #382 merge → on QC PASS, orchestrator merges autonomously per standing directive
- After merge → **Phase 1.5 SHIPS** (vNext-HU-59 production HU oracle; 3-way + multiway routing unchanged)
- Post-ship items deferred to future dispatches (solver-queue drain, design memo amendments, Phase 2 D5)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `6a09235` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-E PR-A INFERENCE PATH merged: master `6a09235` (PR #379 + QC PR #381 PASS · 0/0/0; Path Y avoided; oracle_router.py:34 UNCHANGED in PR-A)
- 1.5-E AMENDMENT Option C: master `d6a07bb` (PR #378)
- Builder PR #377 STOP-condition observation merged: master `7c6e845`
- 1.5-E original dispatch: master `70077cd` (PR #376)
- 1.5-D.4 SHIP GATE PASS: master `3f854a8` (PR #373 + QC PR #375 PASS · 0/0/0; canonical 28/30 + mean 28.2/30 + all 5 seeds ≥28/30; +10 over v8-HU baseline 18/30)
- 1.5-D.4 PR 0 EVAL INFRA merged: master `3fcf7f1` (PR #367 + QC PR #369 PASS; v8-HU baseline 18/30)
- Architect's design memo §4.5 + §4.6 (ship-gate ≥28/30 + 1.5-E ship-action amendment): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Path Y reference: `river-rats-core/train_model_v9_student.py` lines 582-661
- Production HU oracle pointer (post-swap): `river-rats-core/oracle_router.py:34` → `gto_model_vNext_hu_59feat.json`
- Force-add precedent: `river-rats-core/models/gto_model_v9_3way_v2.2.json` (3-way model; force-added per analogous pattern)
- 59-feature inference path: `river-rats-core/inference_path_59.py` (merged PR #379)
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_solver_verification_queue.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_tc23_existence_must_be_git_tracked.md`

**Status: QC stream — fire audit now on PR #382 PR-B PRODUCTION SWAP. ~15-20 min wall-clock. 8-item audit + smoke load test + multi-way regression. Orchestrator merges PR #382 + verdict autonomously on PASS. After merge → PHASE 1.5 SHIPS.**
