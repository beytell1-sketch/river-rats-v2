---
date: 2026-04-25
from: Main terminal (orchestrator)
to: Teaching builder · Owner
re: Activate /loop on teaching side — slow cadence while held; primary trigger is commit 14 landing on v2 origin/master + orchestrator cross-stream notification; surfaces unblock signal so teaching can start C5.2 fixture swap when it's time
status: DIRECTIVE — teaching runs /loop with self-pacing prompt below; held-state default cadence 30 min; accelerates on commit 14 detection; read-only sweep, no auto-start of C5.2 / C7
---

# Teaching /loop Setup — Held-State Polling for Commit-14 Unblock

## Why activate /loop on teaching side

Teaching is held at PRE-VERIFICATION on v4.1 SHIP REPORT. The
unblock signals are:

1. **Commit 14 lands on v2 origin/master** (Finding B fold-in:
   promotes `_per_villain_folded` / `_per_villain_composition` /
   `_per_villain_overflowed` from `chain_meta` onto features dict).
   Recognisable by commit message "Stage 3.5 commit 14/16:" + the
   Finding B citation in PR title/body.

2. **Orchestrator cross-stream notification** (e.g.
   `MAIN_TERMINAL_TEACHING_COMMIT14_LANDED_<date>.md`) — the
   formal trigger to begin C5.2 fixture swap. Teaching does NOT
   start C5.2 just because commit 14 lands; orchestrator's
   notification is the gate.

3. **Other cross-stream pings** addressed to teaching during the
   wait window (rare; included for completeness).

Without /loop, teaching has to manually `git fetch && git log` to
detect either signal. With /loop, both surface within ~30 min of
landing without manual sweeping.

## Session-launch cwd reminder

Per `MAIN_TERMINAL_GTO_DISPATCH_RESOLUTION_2026-04-25.md`: subagent
availability is set at session-launch cwd, not at invocation cwd.
For teaching to dispatch the V3 compliance reviewer (and any other
teaching-local subagents) when C5.2 / C7 begins, the teaching
session MUST be launched from `~/river-rats-teaching/`.

If teaching's current session was launched from `~/` or elsewhere:
exit and re-launch from `~/river-rats-teaching/` BEFORE activating
/loop. The loop itself doesn't need teaching-local subagents
(read-only sweep), but C5.2 / C7 execution will need them as soon
as commit 14 unblocks. Better to fix session-launch cwd now than
hit a dispatch-block at unblock time.

Smoke-test on session start: confirm V3-compliance-reviewer is in
the available subagent list before /loop activation.

## Activation invocation

After confirming session is launched from `~/river-rats-teaching/`,
paste the following into the teaching terminal:

```
/loop Watch v2 origin/master for commit 14 (Finding B fold-in) + cross-stream notifications addressed to teaching during the v4.1 PRE-VERIFICATION HOLD.

Per-tick checklist:
1. `cd ~/river-rats-v2 && git fetch --quiet && git log --oneline origin/master -10` — scan for "Stage 3.5 commit 14" or "Finding B" in commit messages; scan for new MAIN_TERMINAL_TEACHING_*.md or MAIN_TERMINAL_*.md addressed to teaching
2. `cd ~/river-rats-teaching && git fetch --quiet && git log --oneline origin/teaching/v4-1-nan-render -3` — held branch should be quiet at 0b6d4d3; surface any unexpected change
3. `ls -lt ~/river-rats-v2/review/comms/MAIN_TERMINAL_TEACHING_*.md 2>/dev/null | head -3` — most recent teaching-addressed directives

Decision rules:
- If commit 14 is detected on v2 origin/master AND orchestrator has issued a cross-stream notification (MAIN_TERMINAL_TEACHING_COMMIT14_LANDED_*.md or similar): surface BOTH facts to user, summarise C5.2 plan from MAIN_TERMINAL_TEACHING_C7_HOLD_2026-04-25.md, ASK user to confirm "begin C5.2 fixture swap?" — DO NOT auto-start
- If commit 14 is detected but orchestrator notification has NOT landed: surface "commit 14 detected at <SHA>, awaiting orchestrator cross-stream notification before C5.2 begins" — accelerate cadence to 5-10 min so I catch the notification quickly
- If a new MAIN_TERMINAL_TEACHING_*.md directive lands (other than the commit-14 trigger): read fully, summarise required action, wait for user confirmation
- If a cross-stream comms doc lands that affects teaching (e.g. commit 14 design changes, F3/F4 fixture-spec amendments): note it, surface to user
- If nothing new: one-line "still held, last v2 master at <SHA>, my last action at 0b6d4d3 (held)"

Cadence guidance:
- If commit 14 detected + awaiting orchestrator notification: every 5-10 min (270-600s)
- If commit 14 detected + orchestrator notification landed (active C5.2 unblock state): every 5-10 min until user decides; transition to active-batch cadence post-confirmation
- If teaching is mid-C5.2 / mid-C7 (post-unblock): every 10-15 min (600-900s) to catch orchestrator review feedback
- If everything held + commit 14 not detected (default state): every 30 min (1800s)
- If commit 14 won't land soon (signal: latest v2 commit is still <13.3.5): every 60 min (3600s)

Per memory feedback_quality_default_no_ask.md, feedback_check_comms_before_wait.md, feedback_github_is_state_not_local.md, feedback_orchestrator_controls_parallel_timing.md — slower stream sets pace, orchestrator gates merges, no stream ships just because it finished its own commits.

Discipline:
- Loop is read-only sweeping. No git commits, no PR creation, no agent dispatches in loop body itself.
- Loop SURFACES findings; user authorises any state-changing action including C5.2 start.
- C5.2 start specifically requires BOTH (a) commit 14 on v2 master AND (b) orchestrator cross-stream notification AND (c) explicit user confirmation. Three gates, not one.
- If a STOP-protocol condition triggers: surface BLOCKED to user, pause loop.
```

## Cadence harmony with orchestrator + builder loops

| Stream | Held cadence | Active-PR cadence | Unblock-wait cadence |
|---|---|---|---|
| Orchestrator | 30-60 min | 5-10 min | n/a (orchestrator drives unblock signal) |
| Logic builder | 30 min idle | 5-10 min PR-pending | 5-10 min post-merge waiting for greenlight |
| Teaching | **30 min default** | n/a (no PR open during hold) | **5-10 min when commit 14 detected, awaiting orch notification** |

Teaching's natural cadence is the slowest because they're held. When
commit 14 lands on origin/master, orchestrator's loop catches it on
their tick and writes the cross-stream notification within minutes.
Teaching's loop catches the notification within 5-10 min of it
landing (accelerated cadence kicks in once commit 14 is detected).
Total latency from commit-14-merge to teaching-user-prompt:
~10-20 min worst case.

## What teaching's loop does NOT do

- Does NOT auto-start C5.2 (requires user confirmation)
- Does NOT dispatch V3 reviewer in loop body (V3 reviewer is
  dispatched in foreground when C5.2 + C7 are authored)
- Does NOT pull / merge / push anything
- Does NOT modify v4.1 SHIP REPORT
- Does NOT make cross-stream decisions (those route via comms doc
  per `feedback_queries_to_orchestrator.md`)

It's a polling mechanism that surfaces orchestrator's unblock
signal. The actual C5.2 execution is foreground work after user
confirms.

## Reference

- `MAIN_TERMINAL_TEACHING_C7_HOLD_2026-04-25.md` — defines the
  unblock sequence (commit 14 → C5.2 → V3 review → C7 → V3 review
  → SHIP REPORT update → pre-Stage-6 gate → merge greenlight)
- `MAIN_TERMINAL_TEACHING_C5_1_QUALITY_DIRECTIVE_2026-04-24.md` —
  HOLD register and SHIP REPORT discipline
- `MAIN_TERMINAL_GTO_DISPATCH_RESOLUTION_2026-04-25.md` — runtime
  constraint on session-launch cwd for project-local subagents
- `MAIN_TERMINAL_BUILDER_LOOP_SETUP_2026-04-25.md` — symmetric loop
  setup on logic builder side
- `feedback_orchestrator_controls_parallel_timing.md` — slower
  stream sets pace; faster stream HOLDs

## Action

**Owner:**
1. Confirm teaching session is launched from `~/river-rats-teaching/`
   (smoke-test V3-compliance-reviewer in subagent list); if not,
   exit and re-launch from there before pasting the loop activation
2. Paste the loop activation block (above) into the teaching
   terminal
3. Teaching loop runs first sweep + schedules next wakeup at 30 min
   (default held cadence)
4. When commit 14 lands + orchestrator writes cross-stream
   notification: teaching loop surfaces, owner confirms C5.2 start

**Teaching (after activation):**
1. First /loop tick: confirm held-state, report last v2 master
   commit, schedule next wakeup at 30 min
2. Subsequent ticks: hold at 30 min cadence until commit 14 detected
3. On commit 14 detection: accelerate to 5-10 min, surface to user
4. On orchestrator cross-stream notification landing: surface BOTH,
   ASK to begin C5.2 — wait for confirmation
5. On confirmation: foreground C5.2 fixture swap → V3 review →
   C7 → V3 review → SHIP REPORT update (loop continues at active-
   batch cadence)

**Orchestrator (me):**
1. This directive committed to v2 origin/master per standing comms
   pattern
2. Continue Stage 3.5 PR-merge cadence (PR #5 currently ready)
3. When commit 14 lands on master: write
   `MAIN_TERMINAL_TEACHING_COMMIT14_LANDED_<date>.md` cross-stream
   notification — teaching's loop catches it and surfaces to owner

## Owner: paste this into the teaching terminal (after confirming cwd)

```
/loop Watch v2 origin/master for commit 14 (Finding B fold-in) + cross-stream notifications addressed to teaching during the v4.1 PRE-VERIFICATION HOLD.

Per-tick checklist:
1. `cd ~/river-rats-v2 && git fetch --quiet && git log --oneline origin/master -10` — scan for "Stage 3.5 commit 14" or "Finding B" in commit messages; scan for new MAIN_TERMINAL_TEACHING_*.md or MAIN_TERMINAL_*.md addressed to teaching
2. `cd ~/river-rats-teaching && git fetch --quiet && git log --oneline origin/teaching/v4-1-nan-render -3` — held branch should be quiet at 0b6d4d3; surface any unexpected change
3. `ls -lt ~/river-rats-v2/review/comms/MAIN_TERMINAL_TEACHING_*.md 2>/dev/null | head -3` — most recent teaching-addressed directives

Decision rules:
- If commit 14 is detected on v2 origin/master AND orchestrator has issued a cross-stream notification (MAIN_TERMINAL_TEACHING_COMMIT14_LANDED_*.md or similar): surface BOTH facts to user, summarise C5.2 plan from MAIN_TERMINAL_TEACHING_C7_HOLD_2026-04-25.md, ASK user to confirm "begin C5.2 fixture swap?" — DO NOT auto-start
- If commit 14 is detected but orchestrator notification has NOT landed: surface "commit 14 detected at <SHA>, awaiting orchestrator cross-stream notification before C5.2 begins" — accelerate cadence to 5-10 min so I catch the notification quickly
- If a new MAIN_TERMINAL_TEACHING_*.md directive lands (other than the commit-14 trigger): read fully, summarise required action, wait for user confirmation
- If a cross-stream comms doc lands that affects teaching (e.g. commit 14 design changes, F3/F4 fixture-spec amendments): note it, surface to user
- If nothing new: one-line "still held, last v2 master at <SHA>, my last action at 0b6d4d3 (held)"

Cadence guidance:
- If commit 14 detected + awaiting orchestrator notification: every 5-10 min (270-600s)
- If commit 14 detected + orchestrator notification landed (active C5.2 unblock state): every 5-10 min until user decides
- If teaching is mid-C5.2 / mid-C7 (post-unblock): every 10-15 min (600-900s) to catch orchestrator review feedback
- If everything held + commit 14 not detected (default state): every 30 min (1800s)
- If commit 14 won't land soon (latest v2 commit is still <13.3.5): every 60 min (3600s)

Per memory feedback_quality_default_no_ask.md, feedback_check_comms_before_wait.md, feedback_github_is_state_not_local.md, feedback_orchestrator_controls_parallel_timing.md.

Discipline: read-only sweeping. No commits, no PR creation, no agent dispatches in loop body. C5.2 start requires THREE gates: (a) commit 14 on v2 master (b) orchestrator cross-stream notification (c) explicit user confirmation. STOP-protocol triggers pause the loop.
```
