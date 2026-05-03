---
date: 2026-05-03
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · ML-ARCHITECT (advisory) · QC stream · Owner
re: Phase 12.5-prep R-A2 — post-patch test run finds 4 more out-of-scope files that need editing; R-A3 scope amendment recommended
status: BUILDER BLOCKED — R-A2 patch applied locally, targeted suite clean, broader suite has 4 root-cause regressions outside the 11-file scope; reverted; reporting per CLAUDE.md §5
---

# Phase 12.5-prep R-A2 — BLOCKED

R-A2 patch applied verbatim per directive (master `dc467c1`). Targeted suite (5 R-A2 test files + new test file) is clean: **1 failed (the carved-out pre-existing `test_assemble_produces_correct_files`), 122 passed, 52 skipped.**

But broader suite reveals **4 out-of-scope files** that hardcode the 55-feature contract or the "55+4=59" arithmetic and break post-patch. Per Stop Condition #3 ("Anything outside the 11 listed files needs editing → STOP"), reverted patch and reporting.

## Targeted suite result (R-A2's 5 test files + new test file)

```
1 failed, 122 passed, 52 skipped, 1 warning in 9.56s
FAILED test_attention_experiments.py::test_assemble_produces_correct_files (carve-out)
```

All 15 directed test assertion updates verified. All 5 directed source extensions verified. New test file passes. **R-A2's listed scope works as designed.**

## Broader suite result (full `river-rats-core/tests/`) — 4 new categories of regressions

### Category A — `corpus_revision_scenarios/_scenario_utils.py:28` import-time assert (cascading)

**Single root cause** for all **22** `test_corpus_revision_v3.py` failures (pre-existing on master: 0 failures, 59 passed; post-patch: 22 failures).

`river-rats-core/corpus_revision_scenarios/_scenario_utils.py:21-30`:
```python
from gto_model import FEATURE_COLUMNS
from feature_keys import F

# 59-feature contract = FEATURE_COLUMNS (55) + 4 v2.4 P1 blockers
V24_P1_BLOCKER_FEATURES = (
    F.NUT_FLUSH_BLOCK,
    F.FLUSH_DRAW_BLOCK_PCT,
    F.STRAIGHT_DRAW_BLOCK_PCT,
    F.NUT_MADE_BLOCK_PCT,
)
EXPECTED_59_KEYS = list(FEATURE_COLUMNS) + list(V24_P1_BLOCKER_FEATURES)
assert len(EXPECTED_59_KEYS) == 59, (
    f"59-feature contract check failed: got {len(EXPECTED_59_KEYS)}"
)
```

After R-A2 patch: `len(FEATURE_COLUMNS) = 59` (extended) + 4 blockers = **63**, fails the `assert == 59` at module import time. Every test that imports anything from `corpus_revision_scenarios/` cascades a `FAILED at import` error.

The fix is **not** updating the assertion — the duplicate-blockers logic is now wrong. The correct refactor:
```python
# After R-A2: gto_model.FEATURE_COLUMNS already contains the 4 blockers
EXPECTED_59_KEYS = list(FEATURE_COLUMNS)
assert len(EXPECTED_59_KEYS) == 59
```

OR: remove the `V24_P1_BLOCKER_FEATURES` tuple entirely + simplify. Out-of-scope per directive.

### Category B — `scripts/verify_feature_schema_compatibility.py:33-42` same pattern

```python
V24_P1_BLOCKER_FEATURES = (
    F.NUT_FLUSH_BLOCK,
    F.FLUSH_DRAW_BLOCK_PCT,
    F.STRAIGHT_DRAW_BLOCK_PCT,
    F.NUT_MADE_BLOCK_PCT,
)
CORPUS_59_FEATURES: List[str] = list(FEATURE_COLUMNS) + list(V24_P1_BLOCKER_FEATURES)
assert len(CORPUS_59_FEATURES) == 59, (
    f"59-feature corpus contract broken: got {len(CORPUS_59_FEATURES)}"
)
```

Same arithmetic problem post-patch (would compute 63, assert fails). Same fix shape: remove the manual blocker addition since `FEATURE_COLUMNS` already contains them post-R-A2.

This script is not auto-run by pytest, so it doesn't show up in the test failure list — but it would break Phase 12.5C/D pre-flight when invoked.

### Category C — `tests/test_harness_feature_completeness.py:84, 276` shape assertions

Both lines: `assert arr.shape == (55,)`. After R-A2: `features_from_dict()` returns shape `(59,)` (because gto_model.FEATURE_COLUMNS is now 59).

Pre-existing on master: 1 failure (`test_feature_columns_match_gto_model`). Post-patch: 2 failures (one new from the shape assertion plus the pre-existing).

This file is **outside** R-A2's listed 5 test files. Per Stop Condition #3: STOP.

### Category D — `tests/test_game_state_bridge.py:112` shape assertion

Single line: `assert arr.shape == (55,)`.

Pre-existing on master: 0 failures (8 passed, 1 skipped). Post-patch: 1 new failure.

Outside R-A2 scope.

## Pre-existing failures (NOT introduced by my patch)

For completeness, these were already failing on bare master HEAD `dc467c1` and remain failing after R-A2 patch — not regressions:

- `test_oracle_router.py` — 10 failed, 1 passed on master (pre-existing import/setup issue)
- `test_harness_feature_completeness.py::TestExtractAllFeaturesCompleteness::test_feature_columns_match_gto_model` — 1 pre-existing failure (different from the 2 new shape-assertion failures my patch introduces)
- `test_attention_experiments.py::test_assemble_produces_correct_files` — pre-existing, **explicitly carved out by R-A2 directive**

These should not block R-A3.

## Recommended R-A3 scope amendment

R-A2's 5 source files + 5 test files + new test file all stand. **Add 4 files to the scope:**

### Source files — refactor (2 NEW)

| File | Change | Effect |
|------|--------|--------|
| `scripts/verify_feature_schema_compatibility.py:33-42` | Remove `V24_P1_BLOCKER_FEATURES` manual addition; replace `CORPUS_59_FEATURES = list(FEATURE_COLUMNS) + list(V24_P1_BLOCKER_FEATURES)` with `CORPUS_59_FEATURES = list(FEATURE_COLUMNS)`; keep `assert len == 59` (now satisfied because gto_model has 59 natively) | Unblocks future Phase 12.5C/D pre-flight invocation |
| `river-rats-core/corpus_revision_scenarios/_scenario_utils.py:21-30` | Same shape: remove `V24_P1_BLOCKER_FEATURES` manual addition; replace `EXPECTED_59_KEYS = list(FEATURE_COLUMNS) + list(V24_P1_BLOCKER_FEATURES)` with `EXPECTED_59_KEYS = list(FEATURE_COLUMNS)`; keep `assert len == 59` | Unblocks all 22 cascading `test_corpus_revision_v3.py` failures |

### Test files — assertion updates (2 NEW)

| File | Lines | Change |
|------|-------|--------|
| `river-rats-core/tests/test_harness_feature_completeness.py` | 84, 276 | `(55,)` → `(59,)` |
| `river-rats-core/tests/test_game_state_bridge.py` | 112 | `(55,)` → `(59,)` |

### Total R-A3 scope

- **7 source files** (5 R-A2 extends + 2 new refactors)
- **7 test files** (5 R-A2 + 2 new assertion updates) + **1 new test file**
- **15 + 3 = 18 test assertion updates**
- **2 source-file refactors** (refactor pattern, not append)
- **Same carve-out:** `test_assemble_produces_correct_files`

This converges on a clean state. Once R-A3 lands, the 55→59 contract migration is complete: gto_model is canonical, all consumers (test fixtures, scenario utils, schema verifier) reference the canonical surface, no duplicate-blocker arithmetic anywhere.

## What I did and verified

1. **Pre-flight on R-A2's 5 source files:** all match (55 ending `board_adjusted_hrp`). ✅
2. **Verified attention-tagger logic** for `n_tagged 53 → 57`: `assemble_pilot_data.py:858-863` flags every `FEATURE_COLUMNS` entry except `untagged_features = {[0], [1]}`. Pre: 55-2=53. Post: 59-2=57. ✅
3. **Located `test_output_shape`:** `test_sizing_oracle.py:519-522`. Updated `(55,)` → `(59,)`. ✅
4. **Applied 5 source extensions:** gto_model.py, coaching/gto_model.py, sizing_oracle.py, train_model.py, train_sizing_model.py — append 4 blockers + comment update where present. ✅
5. **Applied 15 test assertion updates** across 5 test files. ✅
6. **Created new test file** `tests/test_feature_columns_v24_p1.py` with 3 assertions. ✅
7. **Targeted suite:** 1 carve-out failure + 122 passed + 52 skipped. ✅
8. **Diff scope verified:** exactly 11 files (5 source + 5 test + 1 new test), matching R-A2's "11 listed files" exactly. ✅
9. **Broader suite revealed** 4 out-of-scope regressions (Categories A/B/C/D above), traced to root causes by reading source.
10. **Reverted patch in worktree** + verified `N_FEATURES=55`. Worktree clean.
11. **Authoring this BLOCKED report** on a fresh branch (`programmer/builder-blocked-r-a2-incomplete-2026-05-03`).

## Process compliance

| Check | Status |
|-------|--------|
| Worked in isolated worktree (`/tmp/builder-prep-wt`) | ✅ |
| Pre-flight on all 5 R-A2 sources before patching | ✅ |
| Followed directive's "read attention-tagger before changing" hint | ✅ |
| Did NOT touch `feature_extractor.py` (already 59) | ✅ |
| Did NOT touch `coaching/sizing_oracle.py` (45-feat legacy) | ✅ |
| Did NOT improvise edits to `_scenario_utils.py`, `verify_feature_schema_compatibility.py`, `test_harness_feature_completeness.py`, `test_game_state_bridge.py` (out of R-A2 scope) | ✅ — STOP per condition #3 |
| Reported pre-existing failures separately so orchestrator can distinguish regressions from baseline noise | ✅ |
| Reverted on first stop condition match | ✅ |
| Reporting on a fresh branch | ✅ |

## Process commentary (orchestrator-aware)

Each iteration of "tighten scope → patch → run tests → discover further out-of-scope files" has unblocked some surface area but kept finding more downstream effects. The pattern:

- PR #114: 12 tests fail. Scope = 1 file (`gto_model.py`). Required: 4 sources + 5 test files. → R-A.
- PR #116 (R-A BLOCKED): R-A's 4 sources insufficient. Required: 5 sources + 5 test files + 3 more assertions. → R-A2.
- PR #118 (R-A2 BLOCKED, this comm): R-A2's 11-file scope insufficient. Required: 7 sources + 7 test files + 18 assertions + 1 new test file = 15 listed files. → R-A3.

The convergence is real but each round has revealed +2-3 files. Recommendation: **at R-A3, broaden the verify-before-PR step to a full `pytest river-rats-core/tests/`** (filtering pre-existing master baseline failures) rather than just the listed test files — that catches the cascade effects in one round. The directive's targeted-suite verification has been undercounting downstream effects.

If orchestrator prefers, **R-B (Path Y)** sidesteps all this: keep gto_model et al at 55, give the new student trainer its own internal 59-surface. The contract-wide migration becomes a separate post-12.5 hygiene workstream. Trade-off: permanent dual-schema (which already exists between gto_model=55 and feature_extractor=59 on master HEAD), but no test breakage and no further round-trips.

## What I'm asking the orchestrator to decide

**S-1 (recommended for clean state):** Adopt **R-A3** — 7 sources + 7 test files + 1 new test file = 15 listed files. Two of the 7 sources need refactor (not append). Verify-before-PR widened to broader pytest with explicit pre-existing-failure baseline.

**S-2 (path of least resistance):** Adopt **R-B (Path Y)** — abandon contract-wide migration. New student trainer carries internal 59-schema. Sacred core stays mixed (gto_model=55, feature_extractor=59 — current master state). No test breakage, no further BLOCKED rounds.

**S-3 (pause):** Re-do ml-architect 12.5A on the corrected scope before any builder execution. Cleanest paper trail; most cycles.

Patch surface for R-A3 is fully reproducible from this report. Pre-existing failures clearly separated.

## References

- Master HEAD: `dc467c1` (PR #117, R-A2 directive)
- R-A2 directive: `review/comms/MAIN_TERMINAL_PHASE125_PREP_R_A2_2026-05-03.md`
- Previous BLOCKEDs: PR #114 (`9f5c22a`), PR #116 (`ddfc6a2`)
- ml-architect 12.5A: PR #110 (`291af80`)
- Verified source on master HEAD `dc467c1`:
  - `river-rats-core/corpus_revision_scenarios/_scenario_utils.py:21-30` — duplicate-blockers arithmetic
  - `scripts/verify_feature_schema_compatibility.py:33-42` — same pattern
  - `river-rats-core/tests/test_harness_feature_completeness.py:84, 276` — `(55,)` shape
  - `river-rats-core/tests/test_game_state_bridge.py:112` — `(55,)` shape
  - `river-rats-core/assemble_pilot_data.py:858-863` — attention-tagger logic confirms `n_tagged = len(FEATURE_COLUMNS) - len(untagged_features)`
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_verify_source_not_plan.md`, `feedback_quality_default_no_ask.md`, `feedback_queries_to_orchestrator.md`, `feedback_shared_tree_commit_hygiene.md`, `feedback_spec_vs_infrastructure_code_drift.md`, `feedback_check_comms_before_wait.md`

**Status: BUILDER BLOCKED on R-A2 stop condition #3. Prep branch (`programmer/phase125-prep-r-a2-2026-05-03`) at master HEAD `dc467c1`, no commits, ready for R-A3 / R-B / R-S3 re-attempt. Awaiting orchestrator decision.**
