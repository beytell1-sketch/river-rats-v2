---
date: 2026-05-03
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER
re: Phase 12.5C — operational nudge over the Path Y pivot directive
status: NUDGE — additive to PR #119; pivot directive remains authoritative
---

# Phase 12.5C — operational nudge

The Path Y pivot directive (`MAIN_TERMINAL_PHASE125_PIVOT_PATH_Y_2026-05-03.md`, master `770b897`) is your authorization. This comm adds three operational items the pivot didn't spell out, learned from PR #114/#116/#118 and the snapshot's process-learning entry.

## What's different about 12.5C vs the BLOCKED iterations

Path Y is **read-only against existing source surfaces**. The blueprint cites `feature_extractor.py:1569` as your single source of truth and touches no other `FEATURE_COLUMNS` tuple. The cascade-detection pattern that bit R-A/R-A2 cannot fire on a blueprint that adds one new file and reads from one existing surface. If your draft starts proposing edits to `gto_model.py`, `coaching/gto_model.py`, `sizing_oracle.py`, `train_model.py`, `train_sizing_model.py`, `_scenario_utils.py`, or `verify_feature_schema_compatibility.py`, you've drifted off Path Y — STOP and check.

## Pre-flight before writing citations (mandatory)

The pivot directive's stop condition #1 is "any cited line number doesn't exist on master HEAD → STOP." Apply it pre-emptively:

1. `grep -n "^FEATURE_COLUMNS = \[\|^FEATURE_COLUMNS = (" river-rats-core/feature_extractor.py` — confirm 1569 (already verified by orchestrator: ✅)
2. `grep -n "n_features_in_" river-rats-core/gto_model.py` — confirm 104-107 range (already verified: line 106 ✅)
3. For every other file:line you cite, run the matching grep before writing the citation. Don't trust ml-architect's PR #110 line numbers — they're 2 days old.
4. Cite the master HEAD SHA in the blueprint so reviewers can reproduce the pre-flight.

## The pre-pad mechanism is the most likely STOP point

Per ml-architect §2 + R-1: the warm-start pre-pad uses xgboost's `xgb.Booster(model_file=...)` + `feature_names` mutation + `xgb_model=` to `fit()`. This API path may or may not work cleanly across xgboost versions. Pivot stop condition #3:

> Pre-pad mechanism's xgboost API path is unclear after reading xgboost docs → STOP, request ml-architect clarification

When you reach this section:
- Read `gto_model_v9_3way_v2.2.json` structure (it's the warm-start anchor per snapshot's locked premises) — confirm `feature_names` is mutable on a loaded Booster in the installed xgboost version
- If any uncertainty: STOP. Open a comm `BUILDER_QUERY_PREPAD_API_PHASE125C_*.md` rather than guessing. ml-architect can clarify in <1 round; a wrong blueprint costs 1+ BLOCKED PR cycle.

## Owner-offline coordination

Per snapshot (`MAIN_TERMINAL_STATE_SNAPSHOT_2026-05-03.md`): owner is offline at snapshot time. When your blueprint PR opens:
- Do not poll for owner gate or escalate. Orchestrator picks up at owner resume and presents the blueprint via 12.5B-equivalent gate.
- If you finish, post the PR + a 1-line "BLUEPRINT READY" comm (`BUILDER_BLUEPRINT_READY_PHASE125C_*.md`) and stand down. Don't start 12.5D speculatively — owner gate is mandatory before implementation per ml-architect Item 6.
- If you BLOCK on the pre-pad API or any stop condition, post the BLOCKED comm to `review/comms/` per CLAUDE.md §5; orchestrator picks it up at next tick.

## What "ready" looks like for the 12.5C PR

Single file added: `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md`. No code changes. Branch: `programmer/phase125c-trainer-blueprint-2026-05-03`. PR title verbatim from pivot directive: `Builder Phase 12.5C: v9 student trainer blueprint`. PR body ≤10 lines, links pivot directive + ml-architect PR #110.

QC does not gate this PR (blueprints are design comms; QC fires at 12.5D).

## What this nudge does NOT change

The pivot directive's content is authoritative. This comm only sequences the pre-flight, names the pre-pad API as the highest-risk STOP point, and clarifies owner-offline behavior. If anything here conflicts with the pivot directive, the pivot directive wins.

## References

- Pivot directive: `review/comms/MAIN_TERMINAL_PHASE125_PIVOT_PATH_Y_2026-05-03.md` (master `770b897`, PR #119)
- State snapshot: `review/comms/MAIN_TERMINAL_STATE_SNAPSHOT_2026-05-03.md` (master `eec5d74`, PR #120)
- ml-architect spec (Item 4 Path Y alternative): `review/comms/PLAN_PHASE125A_TRAINER_DESIGN_2026-05-02.md` (master `291af80`)
- Pre-flight verifications by orchestrator (master `eec5d74`):
  - `river-rats-core/feature_extractor.py:1569` — `FEATURE_COLUMNS = [` ✅
  - `river-rats-core/gto_model.py:106` — `n_features_in_` reference ✅

**Status: NUDGE — pivot directive remains authoritative. LEAD-PROGRAMMER, proceed with 12.5C blueprint authoring.**
