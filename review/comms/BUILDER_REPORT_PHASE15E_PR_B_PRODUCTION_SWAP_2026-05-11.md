---
date: 2026-05-11
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · QC stream · Owner (informational)
re: Phase 1.5-E PR-B — production swap complete; vNext-HU-59 now in production HU oracle slot; v8-HU-38 force-added as runtime artifact for rollback safety; coaching-pipeline tests PASS
status: DELIVERY — Phase 1.5-E PR-B ready; Phase 1.5 SHIPS after merge
---

# Phase 1.5-E PR-B — Production swap delivery

## Summary

Per AMENDMENT (PR #378) Option C §"PR-B: Production swap" + original 1.5-E dispatch (PR #376) §"Builder deliverables (a)-(e)".

**Production swap complete:**
- vNext-HU-59 now in production HU oracle slot (`oracle_router.py:34` `_MODEL_FILES[1]`)
- v8-HU-38 force-added as runtime artifact for rollback safety (per dispatch §(d) Option B)
- Both model files git-tracked (`git ls-files` verified)
- Coaching-pipeline tests **22/22 PASS** (1 skipped) post-swap

**After merge: Phase 1.5 SHIPS.** Production HU oracle = vNext-HU-59 (28/30 ship-gate-clear; +10 over v8-HU-38 baseline 18/30).

## §1 — Force-add summary

Both model files added via `git add -f` to bypass `*.json` gitignore pattern (per dispatch §(d) Option B precedent matching `gto_model_v9_3way_v2.2.json`).

| File | Size | Tracked? |
|------|------|----------|
| `river-rats-core/models/gto_model_vNext_hu_59feat.json` | 2.0 MB | ✓ (`git ls-files` confirmed) |
| `river-rats-core/models/gto_model_v8_hu.json` | 11.7 MB | ✓ (`git ls-files` confirmed; was untracked runtime-only before) |

`git ls-files` verification:
```
$ git ls-files --cached river-rats-core/models/gto_model_vNext_hu_59feat.json river-rats-core/models/gto_model_v8_hu.json
river-rats-core/models/gto_model_v8_hu.json
river-rats-core/models/gto_model_vNext_hu_59feat.json
```

Both files now satisfy `feedback_tc23_existence_must_be_git_tracked.md` (closes the §1.2 attestation gap symmetrically).

## §2 — `oracle_router.py:34` swap (verbatim diff)

```diff
 _MODEL_FILES = {
-    1: 'gto_model_v8_hu.json',
+    1: 'gto_model_vNext_hu_59feat.json',
     2: 'gto_model_v9_3way.json',
     3: 'gto_model_v9_4way.json',
     4: 'gto_model_v9_5way.json',  # 5-way handles 4+ opponents
 }
```

1-line change. Position 1 (HU) now points to vNext-HU-59. Positions 2/3/4 (3-way/4-way/5-way) UNCHANGED.

## §3 — Coaching-pipeline test results

### Tests run

`tests/test_inference_path_59.py` (12 tests; PR-A coverage) + `tests/test_oracle_router.py` (10 tests; router routing/dispatch/init).

```
$ python3 -m pytest tests/test_inference_path_59.py tests/test_oracle_router.py --tb=short -q
..........s............                                                  [100%]
22 passed, 1 skipped in 2.40s
```

**Result: 22/22 PASS (1 skipped).**

The skipped test is `test_router_dispatches_legacy_to_55_path` — it skips because the HU position now loads vNext-HU-59 (post-swap), so the "legacy 55-feature path" precondition no longer holds via the default router. This is expected post-swap behavior; the legacy 55-path is still TESTED via `test_legacy_v8_hu_still_works_via_55_path` which loads v8-HU directly (not via router).

### Test fixture updates (mechanical, per dispatch §"investigate before merging")

Three tests had hardcoded references to v8-HU as the production HU model. Updated to match post-swap reality:

1. **`test_oracle_router.py::TestRouterDispatch::test_hu_gets_vnext`** (renamed from `test_hu_gets_v8`):
   - Asserts position 1 loads model with `_n_features == 59` (was 38 pre-swap)
   - Updated docstring cites Phase 1.5-E PR-B
2. **`test_oracle_router.py::TestRouterDispatch::test_3way_falls_back_to_hu`**:
   - Updated assertion: 3-way fallback target now `_n_features == 59` (was 38 pre-swap)
   - Behavioral change: 3-way without specialist now falls back to vNext-HU-59 (more accurate than legacy v8-HU-38 fallback). Substantive improvement documented in §6.
3. **`test_inference_path_59.py::test_router_dispatches_59_path_when_loaded`**:
   - Updated to read `_MODEL_FILES[1]` (= post-swap filename) instead of hardcoding `'gto_model_v8_hu.json'`
   - Test still verifies vNext-HU loadable + predict via router

These are mechanical fixture updates aligning test labels to current implementation; no test loses coverage. Per dispatch §"Coaching-pipeline tests pass: with PR-A inference path in place, vNext-HU now works through router; tests should pass cleanly" — fixtures align to vNext as the production HU model.

## §4 — Smoke load test (per dispatch §(c)/(e))

```
$ python3 -c "
from oracle_router import OracleRouter
from feature_extractor import extract_all_features
from feature_keys import F
hand = {...}  # minimal HU hand_dict
feat_dict = extract_all_features(hand)
r = OracleRouter()
hu = r._oracles[1]
print(f'HU n_features: {hu._n_features} classes: {hu._model.n_classes_}')
pred = r.predict(feat_dict, num_opponents=1)
print(f'action={pred.action} confidence={pred.confidence:.3f}')
print(f'available_models: {r.available_models}')
"
HU n_features: 59 classes: 5
action=BET confidence=0.996
available_models: {1: 'gto_model_vNext_hu_59feat.json (59 features)'}
```

vNext-HU loads via OracleRouter; predict on AhKs/Ad8c3h flop returns BET with 99.6% confidence (canonical TPTK c-bet — matches design narrative for HU-1.1 anchor; consistent with vNext-HU getting HU-1.1 right in 30-hand reference at 28/30 ship-gate score).

## §5 — 3-way/4-way/5-way routing — UNCHANGED filename (substantively improved fallback)

`_MODEL_FILES` positions 2/3/4 UNCHANGED (still `gto_model_v9_3way.json`, `gto_model_v9_4way.json`, `gto_model_v9_5way.json`). Verified by line-level diff (only line 34 changed).

**Behavioral change in fallback (multiway models still 3-class on disk + auto-skip):**
Pre-swap, `OracleRouter._get_oracle(num_opponents=2/3/4)` fell back to position 1 (HU position) when no specialist available — got v8-HU-38 (5-class but trained on HU-only data). Post-swap: same fallback path, but now gets vNext-HU-59 (5-class, trained on HU corpus). Both are HU models used as multiway fallbacks; vNext is structurally better (28/30 vs 18/30 on 30-hand reference) so multiway-without-specialist scenarios now use the better fallback.

`test_3way_falls_back_to_hu` updated to reflect this; test still passes.

## §6 — TC-X-OPERATIONAL-DEVIATION-ASSESSMENT

1. **Test fixture updates (3 tests)**: dispatch §"Coaching-pipeline tests pass" implied tests should pass cleanly after PR-A inference path fix; in practice 3 tests had hardcoded v8-HU references requiring mechanical updates. Updates preserve coverage + align test labels to post-swap reality. NOT silent-fixing — investigated + documented.
2. **3-way/4-way/5-way fallback substantive improvement**: positions 2/3/4 fall back to position 1 when no specialist available; post-swap that fallback target is vNext-HU-59 instead of v8-HU-38 (improves quality of HU-as-multiway-fallback path). Multiway specialist models on disk are 3-class (auto-skipped) — known issue pre-existing this PR; not addressed in PR-B per negative scope.
3. **v8-HU-38 force-add (Option B per dispatch §(d))**: closes §1.2 attestation gap symmetrically; provides rollback safety net (revert oracle_router.py:34 to recover v8-HU oracle behavior). 11.7 MB blob added to repo; acceptable per design memo §4.6 amendment.

## §7 — QC stream — what you audit (PR-B)

Per dispatch §"QC stream — what you audit (post-PR)" 8-item:

- [ ] Diff scope: 5 files (NEW gto_model_vNext_hu_59feat.json + NEW gto_model_v8_hu.json + oracle_router.py 1-line + 2 test fixture updates + this report); NO other source code/data edits
- [ ] Force-add verification: both model files git-tracked per `git ls-files`
- [ ] oracle_router.py diff: only line 34 changed (vNext_hu_59feat replaces v8_hu); positions 2/3/4 unchanged
- [ ] Coaching-pipeline tests: 22/22 PASS (1 skip explained: legacy 55-path test no longer applicable through default router post-swap; coverage preserved via `test_legacy_v8_hu_still_works_via_55_path`)
- [ ] Smoke load test: documented; vNext loads at position 1, n_features=59, predict works
- [ ] Multi-way regression: positions 2/3/4 routing unchanged; substantive fallback improvement documented
- [ ] Provenance link: `gto_model_vNext_hu_59feat.json` provenance docstring (in `train_model_vNext_hu.py`) traceable from this commit hash
- [ ] TC-X-DISPATCH-COMPLIANCE: all negative-scope items honored; STOP conditions evaluated (no STOP triggered post-PR-A inference path)

## §8 — Phase 1.5 SHIP boundary

After PR-B merge + QC PASS: **Phase 1.5 SHIPS.**

- Production HU oracle = vNext-HU-59 (28/30 ship-gate-clear; +10 absolute pts over v8-HU baseline 18/30)
- 3-way + HU both at 59-surface canonical; production aligned
- Solver-verification queue (48 spots) HOLD-with-accepted-risk per owner direction (post-ship recovery)

Post-ship items (out of 1.5-E scope; for future dispatches):
- Solver-verification queue drain when solver online; retrain delta if disagreements
- Design memo §4.6 footnote: actual v8-HU baseline 18/30 vs projected 26-28/30
- HU-6.5 corpus-exclusion-gap (model-stuck on HU-6.5 anchor reference; consider including HU-6.5 lookalikes in next retrain corpus)
- Phase 2 D5 (deferred per blueprint)

## Files in this PR (5)

- `river-rats-core/models/gto_model_vNext_hu_59feat.json` (NEW; force-added)
- `river-rats-core/models/gto_model_v8_hu.json` (NEW; force-added; rollback safety net)
- `river-rats-core/oracle_router.py` (1-line change to `_MODEL_FILES[1]`)
- `river-rats-core/tests/test_oracle_router.py` (2 fixture updates)
- `river-rats-core/tests/test_inference_path_59.py` (1 fixture update)
- `review/comms/BUILDER_REPORT_PHASE15E_PR_B_PRODUCTION_SWAP_2026-05-11.md` (this report)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `6a09235` ✓ (PR #379 + #381 merged)
- Diff vs master: 6 files (2 force-added models + 1 router line + 2 test fixture updates + 1 report)
- Log vs master: 1 commit

## References

- AMENDMENT (PR #378; Option C): master `d6a07bb`
- PR-A inference path (PR #379) merged: master `6f61ba2`
- PR-A QC verdict (PR #381) merged: master `6a09235`
- 1.5-E original dispatch (PR #376): master `70077cd`
- Builder STOP observation (PR #377): master `7c6e845`
- 1.5-D.4 SHIP GATE PASS: master `3f854a8` (PR #373 + QC PR #375 PASS · 0/0/0)
- Architect's design memo §4.6 (production swap; ship-action amendment): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Force-add precedent: `river-rats-core/models/gto_model_v9_3way_v2.2.json` (3-way model; force-added per analogous pattern)
- vNext-HU canonical artifact (now in `river-rats-core/models/`): provenance docstring in `river-rats-core/train_model_vNext_hu.py`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`, `feedback_named_author_builds_not_polls.md`

**Status: Phase 1.5-E PR-B (production swap) complete. vNext-HU-59 in production HU slot; v8-HU-38 force-added for rollback safety; oracle_router.py:34 swap minimal (1 line); coaching tests 22/22 PASS. After merge → Phase 1.5 SHIPS.**
