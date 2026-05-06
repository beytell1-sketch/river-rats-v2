---
date: 2026-05-06
from: QC stream (relaying owner directive)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · QC stream
re: 5-minute /loop discipline across all 3 terminals; orchestrator owns sequencing; no idle terminals; slow-steady-quality cadence
status: OWNER DIRECTIVE — ACK + propagate to all streams
authority: owner directive 2026-05-06 ~20:10 SAST (delivered to QC terminal)
---

# Cross-stream /loop discipline — 5-min cadence

## Owner directive (verbatim)

> please creat loop betwween orchestrator, builder and qc with 5 minute checks for pushed, ticks or updates. orchestrator in charge to make sure there is proper sequencing and no confusion, no idle terminals and slow sterady and quality focused progress. always

## Discipline (effective immediately)

All 3 River Rats v2 terminals run a `/loop 5m <tick-prompt>` self-check, with these standing roles:

| Terminal | Tick action | Trigger to AUTHOR | Idle behaviour |
|---|---|---|---|
| **Main terminal (orchestrator)** | `git fetch` v2 → `ls -lt review/comms/` → `gh pr list` → check for builder reports / QC verdicts that need decisions, dispatch directives, merge actions, queue advancement | new BUILDER_REPORT_* / REVIEW_QC_* / open PR awaiting merge / sequence gate cleared | silent tick (no spam comm) |
| **LEAD-PROGRAMMER (builder)** | `git fetch` v2 → check for active `MAIN_TERMINAL_*` directive naming LEAD-PROGRAMMER → confirm own state vs comms history before executing | named-author directive with status `fire now` / `DIRECTIVE` → AUTHOR per `feedback_named_author_builds_not_polls.md` | silent tick |
| **QC** | `git fetch` v2 → `ls -lt review/comms/` → `gh pr list` → scan for `MAIN_TERMINAL_*_TRIGGER_*` / `MAIN_TERMINAL_*_FIRE_*` naming QC stream that lacks a corresponding `REVIEW_QC_*` / `QC_*` response | active fire-now QC directive → AUTHOR audit immediately per `feedback_no_double_authorization.md` | silent tick |

## Orchestrator authority (per `feedback_orchestrator_decides_not_recommends.md`)

Orchestrator is in charge of sequencing. Per owner directive:
- **No idle terminals.** When orchestrator's tick detects an idle builder or idle QC AND there is queued work for them, orchestrator writes a `MAIN_TERMINAL_*` directive that fires the idle terminal on the next tick.
- **Proper sequencing, no confusion.** Orchestrator's tick reconciles state every 5 min: which PRs are open, which dispatches are in flight, which gates are cleared. If two streams have started overlapping work, orchestrator writes a HALT directive to one and resumes after disambiguation.
- **Slow-steady-quality.** Per `feedback_quality_default_no_ask.md`, orchestrator always picks the slow-quality path. Cadence is for *visibility*, not for forcing speed.

## Hard rules across all 3 terminals

1. **No double authorization.** A `TRIGGER` / `fire now` comm naming the terminal IS authorization (per `feedback_no_double_authorization.md`, written 2026-05-06 after PR #222 cycle). Do not ask owner for a "nod" on top of a directive comm.
2. **No spam comms on idle ticks.** Silent verification is the default. Only escalate when QC found a finding, builder hit a stop condition, or orchestrator needs to advance a queue.
3. **Cross-stream queries route to orchestrator.** Per `feedback_queries_to_orchestrator.md`, scope clarifications / directive conflicts / multi-expert divergence go to `review/comms/<STREAM>_<topic>_<date>.md` for orchestrator's next tick. AskUser is reserved for owner-preference decisions only.
4. **Pre-flight before commit.** Per `feedback_shared_tree_commit_hygiene.md`, every terminal runs `git status` + `git diff --cached` before commit, since multiple terminals may share tree state.
5. **GitHub is the state authority.** Per `feedback_github_is_state_not_local.md`, every tick begins with `git fetch --all --prune`.

## Cache discipline (advisory)

Every 5 min = 300s = exactly the 5-min prompt-cache TTL boundary. Each tick is a cache miss. This is the cost of the cadence the owner specified — accepted explicitly. If quieter periods recur (e.g. owner away overnight), orchestrator may pause its own loop for a defined window via `MAIN_TERMINAL_LOOP_PAUSE_*` and resume when work returns; QC + builder follow the same window.

## Loop authority + lifetime

- Local Claude REPL `/loop` jobs are session-scoped: they die when each terminal closes. Each terminal restarts its loop on session resume.
- 7-day cron auto-expiry: each terminal re-arms `/loop 5m` weekly. (Cloud `/schedule` is an option for durable cross-session cadence — owner has not requested this.)
- Pause / resume: any terminal can pause its own loop with `CronDelete <job_id>` and re-arm with `/loop 5m`. Orchestrator coordinates pauses across streams via `MAIN_TERMINAL_LOOP_*` directive comms.

## Acknowledgement chain

- **QC**: ACK + loop armed (cron job `bdae35c6` on this terminal) at 2026-05-06 ~20:10 SAST. Tick 1 fired immediately on arming; idle (no new triggers since PR #222 audit at 20:00 SAST; PR #224 awaiting orchestrator merge decision).
- **Orchestrator**: ACK pending. On next session resume, expected to arm own `/loop 5m` with the orchestrator-side tick prompt above.
- **Builder**: ACK pending. On next session resume, expected to arm own `/loop 5m` with the builder-side tick prompt above.

## Current sequence state (orchestrator's queue, for context)

Per `MAIN_TERMINAL_PR218_MERGE_AND_125ID_DISPATCH_2026-05-06.md` §"Sequencing — what fires after 12.5I-D merges":

| State | Item | Gates on |
|---|---|---|
| OPEN | PR #222 (12.5I-D corpus assemble) | QC PASS (cleared via PR #224) → orchestrator merge |
| OPEN | PR #224 (QC verdict on PR #222) | orchestrator review + merge |
| QUEUED | 12.5I-MW40-VERIFICATION-A design dispatch | PR #222 merge |
| QUEUED | 12.5J-D-pre test-guard deflake dispatch | PR #222 merge (sequential after MW-40-A) |
| QUEUED | BATCH2 NIT-1 fix-forward (citation form) | folds into MW-40 update PR |
| LATER | 12.5I-MW40-VERIFICATION-B/C/D/E | sequential after A |
| LATER | 12.5J-C / 12.5J-D / 12.5J-E | post-deflake feature work |
| LATER | 12.5K combined re-train | gates on 12.5I-E + 12.5J-E |
| LATER | 12.5L gate eval | gates on 12.5K |

## What orchestrator does on first tick after this comm

1. Read this comm + verify QC PR #224 (PASS verdict on PR #222) is mergeable
2. Merge PR #222 + PR #224 (per dispatch §"Gates")
3. Dispatch 12.5I-MW40-VERIFICATION-A design via new `MAIN_TERMINAL_*` directive naming LEAD-PROGRAMMER
4. Arm `/loop 5m` if not already armed
5. ACK this discipline comm via `MAIN_TERMINAL_LOOP_DISCIPLINE_ACK_2026-05-06.md`

## What builder does on first tick after orchestrator's MW-40-A dispatch

1. Read MAIN_TERMINAL dispatch + ground in core source per `feedback_builder_grounds_before_executing.md`
2. AUTHOR per `feedback_named_author_builds_not_polls.md` (no nod-asking)
3. Arm `/loop 5m` if not already armed
4. ACK this discipline comm via `BUILDER_LOOP_DISCIPLINE_ACK_2026-05-06.md`

## References

- Owner directive: 2026-05-06 ~20:10 SAST (in QC terminal)
- Memory: `feedback_orchestrator_decides_not_recommends.md`, `feedback_no_double_authorization.md`, `feedback_named_author_builds_not_polls.md`, `feedback_queries_to_orchestrator.md`, `feedback_shared_tree_commit_hygiene.md`, `feedback_github_is_state_not_local.md`, `feedback_quality_default_no_ask.md`, `feedback_check_comms_before_wait.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`
- Restart protocol: `BUILDER_RESTART_PROTOCOL_2026-04-25.md`
- Process guide: `docs/PROCESS_GUIDE.md`

**Status: QC armed (cron `bdae35c6`). Awaiting orchestrator + builder ACK + arm on their next session resume.**
