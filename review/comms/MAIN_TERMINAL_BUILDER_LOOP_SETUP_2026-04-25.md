---
date: 2026-04-25
from: Main terminal (orchestrator)
to: Logic builder · Owner
re: Activate /loop on builder side — dynamic-pacing, mirror orchestrator's read-only sweep pattern; reduces manual relay; no auto-merge / no auto-author / surface-only
status: DIRECTIVE — builder runs /loop with self-pacing prompt below; wakes on cross-stream changes during wait-windows; identical discipline to orchestrator's loop (read-only, surface to user, no autonomous state-changing actions)
---

# Builder /loop Setup — Dynamic Pacing Sweep

## Why activate /loop on builder side

Owner has activated /loop on orchestrator terminal (this side polls
master for new builder activity). Symmetric setup on builder side
catches:

1. Orchestrator merge-confirmation comms landing (signal that
   batch N has merged → batch N+1 can begin)
2. Orchestrator greenlight comms (e.g.
   `MAIN_TERMINAL_PR_<n>_MERGED_<date>.md`,
   `MAIN_TERMINAL_COMMIT13_<n>_GREENLIGHT_<date>.md`)
3. Cross-stream signals (commit 14 deadline, teaching unblock
   triggers, etc.)
4. Owner-direct directives written to comms during wait-windows

Reduces manual relay between terminals. Owner can issue a comms
directive on either side; both sides surface it on next tick.

## Activation invocation

Paste the following into the builder terminal:

```
/loop Check master + open PRs + comms folder for orchestrator activity since my last builder action.

Per-tick checklist:
1. `cd ~/river-rats-v2 && git fetch --quiet && git log --oneline origin/master -8` — note new MAIN_TERMINAL_*.md, GTO_REVIEW_*, BUILDER_* commits
2. `gh pr view <my-current-PR> --json state,mergeable,mergeStateStatus` if a PR is open under my authorship — catch state transitions (especially CLEAN → DIRTY indicating someone pushed to master)
3. `ls -lt review/comms/ | head -5` — surface most recent comms docs
4. Compare against my last builder-authored commit on origin/master — anything newer from orchestrator is "new since last sweep"

Decision rules:
- If orchestrator has merged my PR: confirm merge, sync local with `git pull --ff-only`, surface the merge-confirmation comms doc, and stand by for greenlight (which usually arrives within 1-2 commits of the merge)
- If orchestrator has issued a greenlight on next batch: read the directive carefully, confirm batch envelope (entries + branch name), but DO NOT auto-start batch authoring — surface to user with "ready to start batch X on branch Y, confirm?" and wait for go-ahead
- If a cross-stream comms doc has landed (TEACHING_*.md or GAME_*.md from another terminal): note it, don't act
- If a new MAIN_TERMINAL_*.md directive has landed addressed to builder: read fully, summarise required action, wait for user confirmation before executing
- If nothing new: one-line "still quiet, last orchestrator activity at <SHA> <time-ago>; my last action at <SHA>"

Cadence guidance:
- If my PR is open and awaiting orchestrator merge: tick every 5-10 min (270-600s)
- If I'm mid-batch-authoring: tick every 30-60 min (1800-3600s) — I'm actively producing, less need to poll
- If I'm in wait-window between merge and next greenlight: tick every 5-10 min (270-600s)
- If everything held / I'm idle: tick every 30 min (1800s)

Per memory feedback_quality_default_no_ask.md, feedback_check_comms_before_wait.md, and feedback_github_is_state_not_local.md: GitHub is the state authority, sweep before assuming local state matches; surface every change to user; never auto-merge / auto-author / auto-greenlight.

Discipline:
- Loop is read-only sweeping. No git commits, no PR creation, no agent dispatches in the loop body itself.
- Loop SURFACES findings; user authorises any state-changing action.
- If a STOP-protocol condition triggers (e.g. PR-state mismatch, unexpected output, contract violation), surface BLOCKED to user and pause — don't continue ticking through a broken state.
```

## Cadence harmony with orchestrator side

| Builder state | Builder cadence | Orchestrator cadence | Net latency |
|---|---|---|---|
| Builder PR open, awaiting orchestrator merge | 5-10 min | 5-10 min | ~5 min round trip |
| Builder mid-authoring | 30-60 min | 15-20 min (waiting for PR open) | orchestrator catches PR open within 15-20 min |
| Builder in wait-window post-merge, pre-greenlight | 5-10 min | (orchestrator just wrote greenlight) | greenlight visible within 5-10 min |
| Everything held | 30 min | 30-60 min | up to ~1 hour for cross-stream changes |

Both loops self-pace based on their own observed state; no
synchronisation primitive needed. Both wake on the same channel
(origin/master fetch).

## What this does NOT change

- Per-batch protocol from `MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_2026-04-25.md`
- STOP protocol extensions from `MAIN_TERMINAL_PR_4_MERGED_2026-04-25.md`
- GTO dispatch protocol (still general-purpose + persona until
  dedicated `gto-expert` available)
- Any cross-stream HOLD / unblock states
- Stage 4 plan at `ee3d9f5`

The loop is a comms-channel polling mechanism, not a workflow change.

## Action

**Owner:**
1. Paste the loop activation block (above) into the builder terminal
2. Builder will run the first sweep + schedule next wakeup
3. Both sides now poll origin/master autonomously

**Builder (after activation):**
1. First /loop tick runs the sweep + reports
2. Subsequent ticks self-pace based on observed state
3. Surface anything new; do not auto-act on state-changing items
4. If STOP-protocol condition triggers: surface BLOCKED + pause loop

**Orchestrator (me):**
1. This directive committed to v2 origin/master per standing
   comms pattern
2. My loop continues running (currently every ~10 min while PR #5
   is open)
3. When builder loop activates, I'll see builder's BUILDER_*.md
   posts on my next tick — symmetric

## Reference

- `MAIN_TERMINAL_PR_4_MERGED_2026-04-25.md` — PR-state STOP rule
- `MAIN_TERMINAL_GTO_DISPATCH_RESOLUTION_2026-04-25.md` — agent
  dispatch path (loop does NOT dispatch agents; loop is the
  surface mechanism, agents are dispatched in foreground)
- `feedback_check_comms_before_wait.md` — sweep before assuming
  state
- `feedback_github_is_state_not_local.md` — GitHub is state
  authority

## Owner: paste this into the builder terminal

```
/loop Check master + open PRs + comms folder for orchestrator activity since my last builder action.

Per-tick checklist:
1. `cd ~/river-rats-v2 && git fetch --quiet && git log --oneline origin/master -8` — note new MAIN_TERMINAL_*.md, GTO_REVIEW_*, BUILDER_* commits
2. `gh pr view <my-current-PR> --json state,mergeable,mergeStateStatus` if a PR is open under my authorship — catch state transitions
3. `ls -lt review/comms/ | head -5` — surface most recent comms docs
4. Compare against my last builder-authored commit on origin/master — anything newer from orchestrator is "new since last sweep"

Decision rules:
- If orchestrator has merged my PR: confirm merge, sync local with git pull --ff-only, surface merge-confirmation comms doc, stand by for greenlight
- If orchestrator has issued a greenlight on next batch: read directive, confirm batch envelope, DO NOT auto-start authoring — surface to user with "ready to start batch X on branch Y, confirm?" and wait
- If cross-stream comms (TEACHING_*.md or GAME_*.md) has landed: note it, don't act
- If new MAIN_TERMINAL_*.md addressed to builder: read fully, summarise required action, wait for user confirmation
- If nothing new: one-line "still quiet, last orchestrator at <SHA> <time-ago>; my last action at <SHA>"

Cadence:
- PR open awaiting merge: every 5-10 min (270-600s)
- Mid-batch-authoring: every 30-60 min (1800-3600s)
- Wait-window post-merge pre-greenlight: every 5-10 min (270-600s)
- Idle/held: every 30 min (1800s)

Per memory feedback_quality_default_no_ask.md, feedback_check_comms_before_wait.md, feedback_github_is_state_not_local.md.

Discipline: read-only sweeping. No commits, no PR creation, no agent dispatches in loop body. Surface to user; user authorises state-changing actions. STOP protocol triggers: surface BLOCKED + pause.
```
