---
date: 2026-04-26
from: Logic builder
to: Main terminal (orchestrator) · Owner
re: Builder scope reading + execution plan for Stage 4 prep tasks 1-5 per `MAIN_TERMINAL_BUILDER_STAGE4_PREP_TASKS_2026-04-26.md`
status: SCOPE-DOC + EXECUTION PLAN — proceeding with Task 1 (Protocol B) first; sequential per-task execution to manage context across the 5-task arc; per-task PR pattern intact
---

# Stage 4 Prep — Builder Scope + Execution Plan

## Acknowledgement

Read `MAIN_TERMINAL_BUILDER_STAGE4_PREP_TASKS_2026-04-26.md`. Five
Stage 4 prep tasks pre-authorised by locked Stage 4 plan §11 D4 +
D5 (`ee3d9f5`). Each task = author dispatch + reviewer dispatch +
PR cycle, producing v1.0 documents from v0.1 DRAFTs.

## Source-files verified

| Task | Source path | Lines |
|---|---|---|
| 1. Protocol B | `prompts/stage4_drafts/protocol_b_composition_first_v0_1_DRAFT.md` | ~351 |
| 2. Protocol C | `prompts/stage4_drafts/protocol_c_adversarial_elimination_v0_1_DRAFT.md` | ~342 |
| 3. Stage 5 retrain | `review/comms/STAGE5_RETRAIN_PROTOCOL_DRAFT_2026-04-26.md` | ~225 |
| 4. Stage 6 held-out | `review/comms/STAGE6_HOLDOUT_TESTSET_DRAFT_2026-04-26.md` | ~205 |
| 5. Pilot orchestration | `review/comms/STAGE4_PILOT_ORCHESTRATION_DRAFT_2026-04-26.md` | ~284 |

All present.

## Sequencing decision

The orchestrator's recommended Wave 1 (Tasks 1+2+4 in parallel) is
optimal under unbounded context. My context budget across the
5-task arc favours sequential execution with one task per loop
iteration:

- **This iteration: Task 1 (Protocol B)** — author + reviewer + PR
- **Next iteration: Task 2 (Protocol C)** — same pattern
- **Next iteration: Task 4 (Held-out test set)** — same pattern (this is the longest task — 50 hands authoring)
- **Wave 2 iterations: Tasks 3, 5** — sequential

Per `feedback_quality_default_no_ask.md` + `feedback_no_deadlines.md`:
sequential is the slow/quality option. Parallel risks shallow author
output if I'm dividing attention across 3 dispatches simultaneously.
Reviewer rigour also benefits from sequential — I can verify each
v1.0 lands clean before opening the next dispatch surface.

## Subagent dispatch — fallback note

The dedicated `gto-expert` / `ml-architect` subagents are NOT
available in this builder session (same issue as commit-14/15/16
GTO reviews). All dispatches use general-purpose with persona
embedded, per the directive's allowance: "owner-authorised
general-purpose-with-persona fallback if dedicated subagent
unavailable."

Author dispatches WILL write files (v1.0 outputs). Reviewer
dispatches stay read-only and return verdict text via message
body (builder writes verdict comms to `review/comms/`).

## Per-task PR pattern (5 PRs total, one per task)

Each task = same standing pattern as Stage 3.5 commits 13-16:

1. Branch: `stage4-prep/<task-name>-fill` per directive
2. Author dispatch → produces v1.0 file
3. Builder commits v1.0 to feature branch
4. Push branch + open PR
5. Reviewer dispatch (independent, same role) → returns verdict
6. Builder writes verdict to `review/comms/GTO_REVIEW_VERDICT_PR_<N>_2026-04-26.md` or `ML_ARCHITECT_REVIEW_VERDICT_PR_<N>_2026-04-26.md`
7. PR comment + 4-checkpoint state protocol
8. Stand by for orchestrator merge

## Owner-gate preservation

Tasks 1-5 produce v1.0 design artifacts. **NO pilot dispatch.** The
33-agent pilot run on 100 hands remains owner gate per locked Stage
4 plan. Tasks 1-5 are pre-authorised; they get the design specs
to v1.0 quality so when owner authorises pilot dispatch, the inputs
are clean.

## Rollback discipline

No code changes in any task — these are markdown documents.
Rollback = `git revert` per PR. Tag discipline still applies if a
substantive issue surfaces (unlikely for pure document work).

## Reference

- Directive: `review/comms/MAIN_TERMINAL_BUILDER_STAGE4_PREP_TASKS_2026-04-26.md`
- Locked Stage 4 plan: `review/comms/MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md` (`ee3d9f5`)
- Stage 3.5 closure: `review/comms/MAIN_TERMINAL_PRE_STAGE6_GATE_CLEARED_STAGE35_CLOSED_2026-04-26.md`
- 5 DRAFT v0.1 sources: see "Source-files verified" table

**Starting now: Task 1 (Protocol B) author dispatch.**
