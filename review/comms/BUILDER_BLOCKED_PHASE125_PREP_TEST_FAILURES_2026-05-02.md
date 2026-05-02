---
date: 2026-05-02
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · ML-ARCHITECT (advisory) · QC stream · Owner
re: Phase 12.5-prep — BLOCKED on stop conditions #1 + #2; FEATURE_COLUMNS=55 contract is enforced at 5 test files + 2 source files; scope wider than directive modelled
status: BUILDER BLOCKED — patch implemented locally, 12 existing tests fail; reverted; reporting per CLAUDE.md §5
---

# Phase 12.5-prep — BLOCKED

## Why

Per `MAIN_TERMINAL_PHASE125_PREP_TIGHT_2026-05-02.md` (master `f85a9ea`)
§"Stop conditions":
> "*Existing test fails after patch → STOP, report*"
> "*Anything other than `gto_model.py` + new test file needs editing → STOP, report*"

Both fire. Patch as directed (4 string append + comment update + new
test file) breaks **12 pre-existing tests across 5 test files**. The
55-feature contract is enforced at multiple layers; `gto_model.py` alone
is not the canonical source. Expanding to 59 in only `gto_model.py`
violates the cross-consistency assertions the test suite already encodes.

## What I did

1. Pulled master to `f85a9ea` (tight directive HEAD)
2. Created worktree at `/tmp/builder-prep-wt`
3. Switched to `programmer/phase125-prep-feature-columns-59-2026-05-02`
4. Applied the directed patch:
   - `gto_model.py:FEATURE_COLUMNS` extended to 59 (4 strings appended in directive order)
   - `gto_model.py:64` comment `# 55` → `# 59`
   - New file `river-rats-core/tests/test_feature_columns_v24_p1.py` with 2 assertions per directive (count + blocker membership) — used `from gto_model import ...` import style mirroring `test_blocker_features.py:18, test_attention_experiments.py:20`
5. Smoke test: `python3 -c "from gto_model import FEATURE_COLUMNS, N_FEATURES; print(len(FEATURE_COLUMNS), N_FEATURES)"` → `59 59` ✅
6. New regression tests: 2/2 PASS ✅
7. Full pre-existing test suite: **12 failures** (see §"Failure inventory")
8. Per stop condition: **discarded patch + new test file**, switched to a fresh `programmer/builder-blocked-...` branch, authoring this report
9. Did **not** commit the patch on the prep branch; prep branch remains at `f85a9ea` (master HEAD), no commits

## Failure inventory

`pytest river-rats-core/tests/test_attention_experiments.py
river-rats-core/tests/test_board_adjusted_hrp.py
river-rats-core/tests/test_new_features.py
river-rats-core/tests/test_sizing_oracle.py
river-rats-core/tests/test_multiway_features.py`
→ **12 failed, 109 passed, 52 skipped** (in 9.59s)

### Category A — Direct `gto_model.FEATURE_COLUMNS == 55` assertions (3)

| Test | Source | Assertion |
|------|--------|-----------|
| `test_attention_experiments.py::test_feature_columns_count` | line 65 | `assert len(FEATURE_COLUMNS) == 55` (imports `from gto_model`) |
| `test_board_adjusted_hrp.py::TestFeatureCountIs55::test_gto_model_feature_count_is_55` | lines 89-93 | `from gto_model import FEATURE_COLUMNS as GTO_COLS; assert len(GTO_COLS) == 55` |
| `test_new_features.py::TestIntegration::test_gto_model_feature_columns_count` | lines 311-315 | `from gto_model import FEATURE_COLUMNS as GTO_COLS; assert len(GTO_COLS) == 55` |

### Category B — Cross-consistency: `gto_model == feature_extractor == sizing` (4)

| Test | Source | Assertion (paraphrased) |
|------|--------|-------------------------|
| `test_multiway_features.py::TestFeatureContract::test_gto_model_matches_feature_extractor` | lines 44-50 | `len(GTO_COLS) == 55`; `list(GTO_COLS[:55]) == list(FEATURE_COLUMNS)`; index-position checks at 52/53/54 |
| `test_multiway_features.py::TestFeatureContract::test_sizing_feature_surface` | lines 53-58 | `len(SZ_COLS) == 55; len(TSM_COLS) == 55; list(FEATURE_COLUMNS) == list(SZ_COLS)` |
| `test_multiway_features.py::TestFeatureContract::test_n_features_consistent` | lines 62-63 | `assert GTO_N == 55; assert SZ_N == 55` |
| `test_sizing_oracle.py::test_feature_columns_match_gto_model` | lines 175-176 | `from coaching.gto_model import FEATURE_COLUMNS as GTO_FEATURES; assert tuple(FEATURE_COLUMNS) == tuple(GTO_FEATURES)` |

(Note: `test_sizing_oracle.py:175` imports from `coaching/gto_model.py` — a **second copy** of `gto_model.py` at `river-rats-core/coaching/gto_model.py` with its own `FEATURE_COLUMNS` and `N_FEATURES = 55` at line 64. Untouched by my patch — but the cross-equality assertion `tuple(sizing_oracle.FEATURE_COLUMNS) == tuple(coaching.gto_model.FEATURE_COLUMNS)` fails when the two diverge.)

### Category C — `feature_extractor.FEATURE_COLUMNS == 55` (3)

| Test | Source | Assertion |
|------|--------|-----------|
| `test_board_adjusted_hrp.py::TestFeatureCountIs55::test_feature_count_is_55` | lines 83-87 | `from feature_extractor import FEATURE_COLUMNS; assert len(FEATURE_COLUMNS) == 55` |
| `test_new_features.py::TestIntegration::test_feature_extractor_columns_count` | lines 304-308 | same shape |
| `test_multiway_features.py::TestFeatureContract::test_feature_extractor_has_55_columns` | line 36 | same shape |

These three would still fail even if I'd touched `gto_model.py` only, because they assert against `feature_extractor.FEATURE_COLUMNS` (a different module's tuple) — those tests fail mechanically because the test suite cross-checks both surfaces and `feature_extractor.FEATURE_COLUMNS` is at line 1569 in `feature_extractor.py` (untouched by my patch).

### Category D — Indirect failures (2)

| Test | Notes |
|------|-------|
| `test_attention_experiments.py::test_build_enriched_record_flags` | Likely consumes `assemble_pilot_data.py` which references `FEATURE_COLUMNS`; cascades from category A |
| `test_attention_experiments.py::test_load_feature_csv_shape` | Same |
| `test_attention_experiments.py::test_assemble_produces_correct_files` | Same |

(Truthful note: I did not deeply trace what these 3 do internally; the count-of-12 figure includes them and they are real failures, but the root cause is downstream of the same gto_model/feature_extractor 55-contract.)

## Source-code 55-contract enforcement points

`grep -rn "len(FEATURE_COLUMNS) == 55|N_FEATURES == 55|55 features|N_FEATURES.*55" river-rats-core/`:

| File:line | Statement |
|-----------|-----------|
| `river-rats-core/sizing_oracle.py:123` | `N_FEATURES = len(FEATURE_COLUMNS)  # 55` (separate module's tuple — `sizing_oracle` has its own `FEATURE_COLUMNS`) |
| `river-rats-core/coaching/gto_model.py:64` | `N_FEATURES = len(FEATURE_COLUMNS)  # 55` (a SECOND copy of `gto_model.py` with its own 55-entry FEATURE_COLUMNS — see `test_sizing_oracle.py:175`) |
| `river-rats-core/tests/test_attention_experiments.py:65` | hardcoded |
| `river-rats-core/tests/test_board_adjusted_hrp.py:84, 91` | hardcoded |
| `river-rats-core/tests/test_new_features.py:305, 313` | hardcoded |
| `river-rats-core/tests/test_sizing_oracle.py:171` | `assert N_FEATURES == 55` (sizing_oracle's N_FEATURES) |
| `river-rats-core/tests/test_multiway_features.py:36, 46, 52, 55, 62, 63` | hardcoded |

**Total: 12 hardcoded `== 55` lines across 5 test files + 2 separate `# 55` comments in 2 source files (`sizing_oracle.py`, `coaching/gto_model.py`).** Plus `feature_extractor.py:1569` `FEATURE_COLUMNS = [` (a third FEATURE_COLUMNS source — count not pre-counted-out by me but cross-asserted to 55 via the suite).

## Why the directive's "~6-line surgical patch" framing under-modeled scope

The directive cites only `gto_model.py:33-62, 64` as the patch surface. Source-verified state shows the 55-feature contract is enforced at FOUR layers:

1. **`gto_model.py:FEATURE_COLUMNS`** — directive's target, 55 entries (lines 33-62)
2. **`feature_extractor.py:FEATURE_COLUMNS`** — separate tuple at line 1569, must be inspected for current count (untouched by patch but tests cross-check it)
3. **`sizing_oracle.py:FEATURE_COLUMNS` + `:N_FEATURES = ... # 55`** (line 123) — separate module
4. **`coaching/gto_model.py:FEATURE_COLUMNS` + `:N_FEATURES = ... # 55`** (line 64) — a **duplicate of gto_model.py** living under `coaching/`

`test_multiway_features.py::test_gto_model_matches_feature_extractor` (lines 44-50) and `test_sizing_oracle.py::test_feature_columns_match_gto_model` (lines 175-176) actively assert these four surfaces are tuple-equal. Extending one to 59 without the others triggers the consistency assertions.

This matches **directive stop condition #2** verbatim:
> "*Anything other than `gto_model.py` + new test file needs editing → STOP, report — that's a sign the FEATURE_COLUMNS change has wider downstream impact than ml-architect modeled.*"

ml-architect's design (`PLAN_PHASE125A_TRAINER_DESIGN_2026-05-02.md` §5) cited only `gto_model.py:33-62, 64` and `_NAN_ALLOWLIST` (228-231) as touch points. It did not enumerate `feature_extractor.py`, `sizing_oracle.py`, `coaching/gto_model.py`, or the 5 test files. Path X as scoped is incomplete for the existing test contract.

## What did go right

- **The directed patch itself is functionally correct.** With only the 6-line edit, `gto_model.FEATURE_COLUMNS` extended to 59, smoke-test reports `59 59`, both new regression tests pass.
- **No improvisation.** I did not edit any of the 5 failing test files. I did not edit `feature_extractor.py`, `sizing_oracle.py`, or `coaching/gto_model.py` to chase consistency. I stopped on the first stop condition match per `CLAUDE.md` §5.
- **Worktree-isolated.** Per directive's referenced `feedback_shared_tree_commit_hygiene.md` advisory in PR #112, the entire build attempt happened in `/tmp/builder-prep-wt`. The main repo `~/river-rats-v2/` was never modified during the attempt.
- **Patch is reproducible.** The 6-line `gto_model.py` change is in this report's diff section; orchestrator/architect can recreate verbatim.

## The applied diff (for reference; reverted in worktree)

```diff
--- a/river-rats-core/gto_model.py
+++ b/river-rats-core/gto_model.py
@@ -59,9 +59,14 @@ FEATURE_COLUMNS = (
     "villain_medium_made_pct",
     # feature 55: board-adjusted hero range percentile
     "board_adjusted_hrp",
+    # v2.4 P1 features 56-59: blocker-direction features (per feature_keys.py:87-92)
+    "nut_flush_block",
+    "flush_draw_block_pct",
+    "straight_draw_block_pct",
+    "nut_made_block_pct",
 )

-N_FEATURES = len(FEATURE_COLUMNS)  # 55
+N_FEATURES = len(FEATURE_COLUMNS)  # 59
 N_CLASSES = len(ACTION_CLASSES)     # 5
```

(One non-essential explanatory comment line `# v2.4 P1 features 56-59...` was added to mirror the existing `# v9 features (38→45)...` comment style in the same tuple. Could be removed for a strict 6-line patch — orchestrator's call.)

The new test file `river-rats-core/tests/test_feature_columns_v24_p1.py` was 30 lines, 2 test functions, used `from gto_model import FEATURE_COLUMNS, N_FEATURES` (mirroring `test_blocker_features.py:18` style with the standard `_CORE = ...; sys.path.insert(0, _CORE)` shim).

## Recommended resolutions (in priority order)

### R-A (cleanest) — Amend Phase 12.5-prep scope to a contract-wide 55→59 migration

The 55-feature contract is enforced at 4 source-tuple sites + 5 test files. A clean migration covers all of them in one PR:

**Source edits (4 files):**
1. `river-rats-core/gto_model.py:33-62, 64` — directive's current target (4 strings + comment)
2. `river-rats-core/coaching/gto_model.py:33-62, 64` — duplicate gto_model under coaching/, same patch shape (4 strings + comment)
3. `river-rats-core/feature_extractor.py:1569+` — verify count, append matching 4 entries to `FEATURE_COLUMNS` if its tuple is also 55-long; pre-flight read needed
4. `river-rats-core/sizing_oracle.py:~120-123` — verify count + comment, append matching 4 entries (or document divergence rationale if sizing model intentionally stays at 55)

**Test edits (5 files, 12 assertions):**
- Replace `assert len(FEATURE_COLUMNS) == 55` → `== 59` in test_attention_experiments.py:65, test_board_adjusted_hrp.py:84, 91, test_new_features.py:305, 313, test_multiway_features.py:36, 46, 52, 55, 62, 63
- Update `test_sizing_oracle.py:171` `N_FEATURES == 55` → `== 59` IF sizing also moves to 59 (else delete or scope-narrow assertion)
- Update `test_multiway_features.py:46-50` index-position assertions for the new 56-59 features
- Add `river-rats-core/tests/test_feature_columns_v24_p1.py` per directive

**Trade-offs:**
- This is a milestone-class touch on sacred core (4 source files + 5 test files), not a "~6-line surgical patch"
- Sizing model surface (`sizing_oracle.py`) is separately argued in `test_multiway_features.py:55-58` to share the 55-feature surface with feature_extractor — extending it to 59 is a methodology question (does the v2 sizing model retain 55 features or also adopt 59?), arguably ml-architect-scope decision
- `coaching/gto_model.py` divergence vs `gto_model.py` divergence is a separate hygiene question — they were created as a divergent pair for some reason; conflating now may revive an old design tension

### R-B — Path Y resurrected: trainer-local FEATURE_COLUMNS=59

ml-architect's §5 alternative ("Path Y": new student trainer carries its own 59-tuple, leaves `gto_model.py` at 55) was rejected on dual-schema risk grounds. The current state shows the dual-schema risk was already real (4 separate FEATURE_COLUMNS sources). Path Y wouldn't introduce a NEW divergence — it would add to existing.

This sidesteps the test-suite scope entirely. Cost: the new student trainer's predict-side cannot use `gto_model.GtoOracle` directly — it would need a 59-aware sibling.

### R-C (defer) — Do prep PR for `gto_model.py` only, accept test breakage as a known regression

Update only `gto_model.py:FEATURE_COLUMNS` (directive's literal scope) and explicitly document that the 12 listed tests will fail until R-A's broader migration ships. This is a known regression, not a build error. CI would need to be told.

This contradicts the directive's stop conditions and `CLAUDE.md` §6's "river-rats-core/ is always deployable" discipline. Not recommended.

### R-D — Re-do ml-architect 12.5A on the wider scope

If R-A is the right answer, ml-architect should redesign the scope explicitly: which surfaces extend to 59 (`gto_model.py`, `coaching/gto_model.py`, `feature_extractor.py`, `sizing_oracle.py` — yes/no on each), which tests update, what the warm-start anchor's feature contract is. This becomes a Phase 12.5-prep redesign, not a tight patch directive.

## What I recommend (orchestrator's call)

**R-A** with ml-architect briefly confirming whether `sizing_oracle.py` should extend to 59 or stay at 55 (the only ambiguous methodology question). The other three source surfaces (`gto_model.py`, `coaching/gto_model.py`, `feature_extractor.py`) are clearly aligned to the same 55-feature semantic and should all extend to 59. The 12 test assertions are mechanical updates.

Estimated patch size: ~30-40 line edits across 4 source files + 5 test files + 1 new test file. Still well under the threshold for a single PR; just larger than the directive's "6-line" framing. QC TC-23-CONTENT audit applies to the wider diff in the same way.

## Process compliance

| Check | Status |
|-------|--------|
| Worked in isolated worktree (`/tmp/builder-prep-wt`) | ✅ |
| Read mandatory references (PLAN PR #110, REVIEW PR #111, gto_model.py:33-64, feature_keys.py:87-92, verify_feature_schema_compatibility.py:33-42) | ✅ |
| Applied patch exactly per directive | ✅ |
| Verified `python3 -c "from gto_model import FEATURE_COLUMNS, N_FEATURES; print(len(FEATURE_COLUMNS), N_FEATURES)"` → 59 59 | ✅ |
| Ran new regression tests — 2/2 PASS | ✅ |
| Ran existing test suite, found 12 failures | ✅ |
| Did **not** improvise edits to test files, `feature_extractor.py`, `sizing_oracle.py`, `coaching/gto_model.py` | ✅ |
| Discarded patch from worktree before reporting | ✅ |
| Reporting on a fresh branch (separate from prep branch) | ✅ |
| Following `feedback_verify_source_not_plan.md` (read source, found discrepancy, surfaced it) | ✅ |
| Following `feedback_queries_to_orchestrator.md` (route via review/comms/) | ✅ |
| Following `CLAUDE.md` §5 stop protocol (STOP, do not improvise) | ✅ |

## Adjacent finding (not part of this BLOCKED, surface for record)

The earlier `BUILDER_QUERY_PHASE125_PREP_NAN_ALLOWLIST_2026-05-02.md` on branch `programmer/builder-query-phase125-prep-nan-allowlist-2026-05-02` (commit `9b8aae0`, never opened as PR) is **moot** — the tight directive (PR #113) removed the `_NAN_ALLOWLIST` stop condition entirely. The `nut_flush_block` boolean correctly stays out of `_NAN_ALLOWLIST` per the "continuous only" comment design rule, and the patch attempt above did not require any allowlist change. The query branch can be left dormant or deleted at orchestrator's discretion.

## References

- Master HEAD: `f85a9ea` (PR #113, tight directive)
- Phase 12.5-prep tight directive: `review/comms/MAIN_TERMINAL_PHASE125_PREP_TIGHT_2026-05-02.md`
- Phase 12.5-prep verbose directive (superseded): `review/comms/MAIN_TERMINAL_PHASE125_PREP_DIRECTIVE_2026-05-02.md` (master `9de0bc3`, PR #112)
- ml-architect 12.5A design: `review/comms/PLAN_PHASE125A_TRAINER_DESIGN_2026-05-02.md` (master `291af80`, PR #110), §5 "Item 4 — 4-blocker FEATURE_COLUMNS integration"
- Failing tests cited above by file:line on master HEAD `f85a9ea`
- Verify-schema script: `scripts/verify_feature_schema_compatibility.py:33-42`
- Process: `CLAUDE.md` §5 (STOP protocol), §6 (sacred core); `docs/PROCESS_GUIDE.md` §6
- Memory: `feedback_listen_to_orchestrator_always.md`,
  `feedback_named_author_builds_not_polls.md`,
  `feedback_verify_source_not_plan.md`,
  `feedback_quality_default_no_ask.md`,
  `feedback_queries_to_orchestrator.md`,
  `feedback_shared_tree_commit_hygiene.md`,
  `feedback_spec_vs_infrastructure_code_drift.md`

**Status: BUILDER BLOCKED on stop conditions #1 + #2. Prep branch (`programmer/phase125-prep-feature-columns-59-2026-05-02`) at master HEAD `f85a9ea`, no commits, ready for re-attempt once scope is amended. Awaiting orchestrator decision on R-A / R-B / R-C / R-D + ml-architect's `sizing_oracle.py` 55-vs-59 call.**
