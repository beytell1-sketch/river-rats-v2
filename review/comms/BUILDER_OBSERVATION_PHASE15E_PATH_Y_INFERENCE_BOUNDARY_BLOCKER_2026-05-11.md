---
date: 2026-05-11
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · Owner (informational)
re: Phase 1.5-E dispatch (PR #376) — surface STOP-condition: oracle_router.predict() crashes on vNext-HU-59 model with feature-shape mismatch (gto_model.FEATURE_COLUMNS=55 vs vNext expected 59); production swap blocked at integration boundary
status: STOP-CONDITION SURFACED per dispatch §"STOP conditions" + CLAUDE.md §5; reverted local changes; awaits orchestrator decision on integration approach
---

# Phase 1.5-E — STOP-condition: Path Y inference boundary blocker

## Observation

Per dispatch §"(b) Change oracle_router.py filename pointer" + §"(c) Run coaching-pipeline tests": builder executed steps (a)-(c) locally; **`oracle_router.predict()` crashes on vNext-HU-59 model** with `ValueError: Feature shape mismatch, expected: 59, got 55`.

Per dispatch §"STOP conditions": "oracle_router.load_model(1) crashes on vNext model → STOP / REPORT; possibly format-incompatibility or 3-class→5-class transition gap" — same spirit applies (load succeeds; predict fails on the SAME boundary).

Per CLAUDE.md §5 STOP > improvise: surfacing for orchestrator decision rather than improvising the integration approach.

## Root cause (verified by source read)

**Production-runtime path uses `gto_model.FEATURE_COLUMNS` (55 features); vNext-HU-59 expects 59 features.**

- `river-rats-core/oracle_router.py:125`: `features = GtoOracle.features_from_dict(feat_dict)`
- `river-rats-core/gto_model.py:177-209`: `features_from_dict` builds numpy array from `FEATURE_COLUMNS` (55-tuple defined at line 33)
- `river-rats-core/gto_model.py:128-131`: `predict()` truncates input down to `_n_features` for backwards-compat (38 for v8-HU; 45 for v9-3way; 55 for upper bound)
- vNext-HU-59 has `n_features_in_=59`; runtime path passes 55-feature array → `inplace_predict` raises `ValueError: Feature shape mismatch, expected: 59, got 55`

This is a **known architectural design boundary** documented in `river-rats-core/train_model_v9_student.py` lines 582-661:

> "Path Y inference boundary: gto_model.FEATURE_COLUMNS (length 55 on master). The v9-student model expects 59 features. Path Y forbids extending gto_model.FEATURE_COLUMNS"

The v9-student trainer included its own private 59-feature inference path (`_StudentInference`) that bypasses `gto_model.features_from_dict`. The router does NOT have a corresponding 59-feature inference path; it's stuck on the 55-feature ceiling.

## Test evidence

Ran `tests/test_oracle_router.py` after applying the production swap locally:

```
FAILED tests/test_oracle_router.py::TestRouterDispatch::test_hu_gets_v8
  AssertionError: assert label == 'gto_model_v8_hu.json'  (now 'gto_model_vNext_hu_59feat.json')
FAILED tests/test_oracle_router.py::TestRouterDispatch::test_3way_falls_back_to_hu
  Same assertion (downstream fallback target changed)
FAILED tests/test_oracle_router.py::TestRouterPredict::test_predict_returns_oracle_prediction
  ValueError: Feature shape mismatch, expected: 59, got 55
FAILED tests/test_oracle_router.py::TestRouterPredict::test_predict_works_for_all_opponent_counts
  ValueError: Feature shape mismatch, expected: 59, got 55
```

The first 2 failures are test-fixture references to the old filename (mechanical update). The last 2 are the architectural boundary blocker.

## What builder did

Per CLAUDE.md §5 "Stop > improvise":

1. Copied vNext-HU model to `river-rats-core/models/gto_model_vNext_hu_59feat.json`
2. Edited `oracle_router.py:34` (1-line filename change)
3. Smoke-tested router init: vNext model loads at position 1, classes=5, n_features=59 ✓ (load doesn't crash)
4. Ran `tests/test_oracle_router.py` → 4 failures (2 mechanical fixture, 2 architectural blocker)
5. **Reverted local changes** (oracle_router.py reset; vNext model copy removed from `river-rats-core/models/`)
6. Did NOT push any PR; surfaced this observation instead

## Builder recommendations (orchestrator decides)

**Option A — Extend `gto_model.FEATURE_COLUMNS` to 59 features.** Update the runtime FEATURE_COLUMNS tuple to match feature_extractor's 59-key surface. Risk: per `train_model_v9_student.py` Path Y comment, the architect explicitly forbade this in the v9-student work. Reasoning was that gto_model is shared with multiple inference paths and extending it could regress other consumers. May need architect re-review.

**Option B — Build a router-side 59-feature inference path** (analog to `_StudentInference` in v9_student trainer). Modifies oracle_router.py to extract features from feat_dict using a 59-key tuple imported from feature_extractor (instead of via gto_model.features_from_dict). Smaller blast radius but introduces a parallel inference path in production code. Out of dispatch §"only line 34 changes" scope.

**Option C — Architect dispatch (1.5-E-prep) to design the production inference path** for vNext-HU before 1.5-E ships. Decouples ship-action from architectural boundary work; preserves quality-default per `feedback_quality_default_no_ask.md`. Wall-clock add: ~2-4 hr.

**Option D — Wrap vNext-HU in a 55→59 padding shim** in oracle_router (e.g., zero-pad feat_dict to 59 features at predict time, if vNext expects 4 zero-padded features at the tail). Risk: only works if those 4 features are at the tail of the surface AND can be safely zero-padded; otherwise produces silently-wrong predictions. Need verification of which 4 features differ between gto_model.FEATURE_COLUMNS (55) and feature_extractor.FEATURE_COLUMNS (59) and whether they can be zeroed.

**Builder recommendation (architect-hat)**: **Option C** (architect dispatch) per `feedback_quality_default_no_ask.md` slow/quality path. The Path Y boundary is architectural, not mechanical; an off-the-cuff fix risks the same silent-fallback patterns the boundary was designed to prevent. Architect should design the production-inference path explicitly before swap.

If orchestrator prefers velocity: **Option B** with explicit caveats — tested router-side 59-feature path; 2 fixture-only test updates; preserves blast-radius minimization.

## What gates next

- WAIT for orchestrator decision (Option A / B / C / D / Other)
- Per `feedback_named_author_builds_not_polls.md`: builder named in 1.5-E dispatch but the actionable HOW depends on the inference-path scope question
- Per `feedback_dont_surface_terminal_liveness_to_owner.md`: this surface goes to orchestrator, NOT owner

## TC-X-OPERATIONAL-DEVIATION-ASSESSMENT

1. **STOP-condition activation per dispatch §STOP**: format-incompatibility (vNext expects 59; runtime path provides 55) confirmed by test execution. Builder did NOT improvise integration approach.
2. **Local artifacts cleaned**: oracle_router.py reverted; vNext model removed from `river-rats-core/models/`. Repo state matches origin/master cleanly.
3. **v8-HU is also untracked but file exists at `river-rats-core/models/gto_model_v8_hu.json`** (preserved per dispatch §(d) Option B intent — "v8-HU stays on disk untracked as runtime fallback"). Not a regression.

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `70077cd` ✓ (1.5-E dispatch merged)
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-E dispatch (PR #376): master `70077cd`
- 1.5-D.4 PR 2 5-SEED FULL merged (SHIP GATE PASS): master `3f854a8` (PR #373)
- Architect's design memo §4.6 (1.5-E ship-action amendment): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Path Y boundary documentation: `river-rats-core/train_model_v9_student.py` lines 582-661
- Production-runtime feature surface: `river-rats-core/gto_model.py:33-63` (FEATURE_COLUMNS, 55 keys)
- Trainer-side feature surface: `river-rats-core/feature_extractor.py:FEATURE_COLUMNS` (59 keys)
- Production HU oracle pointer: `river-rats-core/oracle_router.py:34` (currently `gto_model_v8_hu.json`)
- vNext-HU canonical artifact (local only; gitignored): `models/gto_model_vNext_hu_59feat.json`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_named_author_builds_not_polls.md`, `feedback_explicit_action_trigger.md`, `feedback_verify_source_not_plan.md`, `feedback_dont_surface_terminal_liveness_to_owner.md`

**Status: BLOCKED-on-Path-Y-inference-boundary-design per CLAUDE.md §5 STOP > improvise. Builder verified failure mode (test_oracle_router 2 architectural failures + 2 fixture failures); reverted local changes; awaits orchestrator selection of Option A/B/C/D/Other before retrying 1.5-E ship.**
