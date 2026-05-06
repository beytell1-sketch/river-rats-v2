---
date: 2026-05-06
from: LEAD-PROGRAMMER (Builder)
to: Owner · Main terminal (orchestrator) · QC stream
re: ACK + arm — 5-min /loop discipline (owner directive 2026-05-06 ~20:10 SAST, relayed via PR #225)
status: ACK — armed
---

# Builder /loop discipline ACK

Owner directive received via PR #225 (`qc/loop-discipline-owner-auth-2026-05-06`). Builder terminal armed `/loop 5m` per owner spec.

## Arm record

| Field | Value |
|---|---|
| Cron job ID | `ed150994` |
| Cadence | every 5 min (`*/5 * * * *`) |
| Lifetime | session-only, 7-day auto-expire |
| Armed at | 2026-05-06 ~20:13 SAST (tick 0 fired on arming) |
| First non-trivial event observed | tick 1 caught QC PR #224 PASS (0/0/0) on PR #222 |

## Standing tick prompt (this terminal)

Per PR #225 spec for Builder (LEAD-PROGRAMMER):

1. `git fetch && git log --oneline origin/master -5 && gh pr list --limit 5` — surface push/PR-state changes
2. `ls -lt review/comms/ | head -8` — surface new comms (per `feedback_check_comms_before_wait`)
3. Scan newest unread comms naming LEAD-PROGRAMMER / Builder for an active `MAIN_TERMINAL_*_FIRE` / `_DISPATCH` directive (per `feedback_explicit_action_trigger` + `feedback_listen_to_orchestrator_always` + `feedback_optional_is_not_authorized`)
4. If fire-now dispatch addressed to me → AUTHOR (not poll) per `feedback_named_author_builds_not_polls`; ground in source + comms first per `feedback_builder_grounds_before_executing`; pilot-first for long jobs per `feedback_pilot_first_for_long_jobs`
5. If `REVIEW_QC_*` BLOCKER/SHOULD_FIX on a builder PR → ground, prepare fix-forward branch, AWAIT orchestrator merge+next-dispatch comm; do NOT auto-fix
6. If no trigger → one-line idle status only; do NOT author plans/comms speculatively (orchestrator owns sequencing per `feedback_orchestrator_decides_not_recommends`)

Owner-facing reply each tick: SHORT (3-8 lines, owner-actionable) per `feedback_orchestrator_output_structure_per_party`.

## Hard rules consolidated (per PR #225)

1. No double authorization — TRIGGER/DISPATCH naming the terminal IS authorization (`feedback_no_double_authorization` if present in memory; else strict `feedback_explicit_action_trigger`)
2. No spam comms on idle ticks — silent verification is default
3. Cross-stream queries route to orchestrator via `review/comms/<STREAM>_<topic>_<date>.md` (`feedback_queries_to_orchestrator`)
4. Pre-flight `git status` + `git diff --cached` before commit (`feedback_shared_tree_commit_hygiene`)
5. `git fetch --all --prune` at start of every tick (`feedback_github_is_state_not_local`)

## Current builder state (snapshot)

| Item | State |
|---|---|
| PR #222 (12.5I-D corpus 788-row) | MERGED (master `48084c3`) |
| PR #224 (QC PASS 0/0/0 on PR #222) | MERGED (master `4d8fcf8`) |
| Fire-now dispatch addressed to builder | NONE — awaiting orchestrator next dispatch |
| Queued post-PR-#222-merge per dispatch `MAIN_TERMINAL_PR218_MERGE_AND_125ID_DISPATCH` | 12.5I-MW40-VERIFICATION-A design + 12.5J-D-pre test-guard deflake (sequential) |
| Posture | WAIT for orchestrator MAIN_TERMINAL_*_DISPATCH naming LEAD-PROGRAMMER |

## ACK chain status (per PR #225 test plan)

- [x] QC armed (cron `bdae35c6`)
- [ ] Orchestrator armed + ACKs via `MAIN_TERMINAL_LOOP_DISCIPLINE_ACK_2026-05-06.md`
- [x] **Builder armed + ACKs (this comm; cron `ed150994`)**

## What I did NOT do

- Did NOT auto-fire on next-phase queue (12.5I-MW40-VERIFICATION-A) — that's orchestrator-scope to dispatch
- Did NOT modify `river-rats-core/`
- Did NOT touch v3.x prompts, BATCH2 reference, or training data
- Did NOT auto-fix PR #224 NIT (none — clean PASS)

## References

- PR #225 (owner directive relay): `qc/loop-discipline-owner-auth-2026-05-06`
- Owner directive originated: 2026-05-06 ~20:10 SAST in builder terminal session
- Memory: `feedback_check_comms_before_wait`, `feedback_explicit_action_trigger`, `feedback_listen_to_orchestrator_always`, `feedback_optional_is_not_authorized`, `feedback_named_author_builds_not_polls`, `feedback_builder_grounds_before_executing`, `feedback_orchestrator_decides_not_recommends`, `feedback_orchestrator_output_structure_per_party`, `feedback_pilot_first_for_long_jobs`, `feedback_no_deadlines`, `feedback_quality_default_no_ask`, `feedback_shared_tree_commit_hygiene`, `feedback_github_is_state_not_local`, `feedback_queries_to_orchestrator`

**Status: Builder /loop armed (cron `ed150994`, 5-min cadence). ACK chain advances builder checkbox. Posture: WAIT for orchestrator dispatch.**
