---
date: 2026-04-25
from: Main terminal (orchestrator)
to: Logic builder · Owner
re: GTO dispatch block resolution — Option 1 (restart builder session from ~/river-rats-v2/); STOP protocol affirmed; resume protocol below
status: DIRECTIVE — Option 1 chosen; owner action required (terminal restart); builder pre-staged materials preserved; same discipline as push-policy decision (lean into the constraint)
---

# GTO Dispatch Block — Resolution: Restart Builder Session

## Decision

**Option 1: restart the builder session from cwd `~/river-rats-v2/`.**

Owner action required. Quality default per
`feedback_quality_default_no_ask.md` chosen without re-asking owner.

Option 2 (general-purpose with gto-expert persona) declined.

## STOP protocol affirmed

Builder correctly invoked CLAUDE.md §5 ("Output contradicts expected
result"). Not improvising and not falling back to a different agent
type without authorisation is the right call. This is the kind of
discipline that prevents 13.3's ~130-entry per-batch GTO review from
silently degrading to a non-dedicated agent and corrupting the audit
trail at scale.

The orchestrator's `MAIN_TERMINAL_GTO_DISPATCH_AUTHORITY_2026-04-25.md`
asserted the runtime model wrong: I claimed *"That agent is
dispatchable only from a terminal with cwd inside `~/river-rats-v2/`"*
implying cwd-at-invocation suffices. Builder's empirical test showed
subagent availability is set at **session-launch** cwd, not at
invocation cwd. Correction acknowledged.

## Why Option 1 over Option 2

**Option 2 (general-purpose with gto-expert persona embedded in brief)**
is the speed option. Trade-offs:

- Verdict header would honestly read *"from: General-purpose subagent
  acting as GTO reviewer"* — that's an audit-trail degradation
- Sets the precedent that when a dedicated subagent isn't available,
  fall back to a generic with a persona prompt. Erodes the
  discipline that says "use the dedicated agent's tuned context"
- Commit 13.3's ~130-entry full lift will run per-batch GTO reviews
  ~5–25 times. Even one batch reviewed via the wrong dispatch path
  is a verifiable audit-trail leak; ~5–25 batches is a structural
  problem
- Same shape as the push-policy decision: when a constraint exists,
  lean into it rather than route around. Restart is a one-time
  cost; persona-fallback is a recurring debt

**Option 1 (restart builder session from v2 cwd)** trade-offs:

- Owner has to exit the current builder terminal and re-launch. ~30s
  cost, one-time.
- Builder loses in-session conversation context. Comms docs are
  designed for cross-session continuity; the BLOCKED notice
  (`2a8bc17`) + dispatch-authority directive (`21f16e6`) + this
  directive are sufficient for the new session to resume.
- After restart, builder verifies dispatch path works BEFORE doing
  the actual 13.2.5 review (small smoke test) — that way 13.3's
  scale doesn't surprise us with a different blocker.

## Owner action

Exit the current builder terminal session. Re-launch Claude Code
with cwd inside `~/river-rats-v2/`:

```
cd ~/river-rats-v2
claude
```

(or whatever the launch invocation is for this environment).

The new session should report `gto-expert` (and `programmer`,
`architect`, `ml-architect`, `reviewer`, `tester`) in its available
subagent list. If it doesn't, that's a deeper config issue —
builder reports BLOCKED again with the new available-agents list and
we look at session-config files in `~/.claude/` or v2-local config.

## Resume protocol for builder (post-restart)

Read these in order to re-orient:

1. `review/comms/BUILDER_GTO_DISPATCH_BLOCKED_2026-04-25.md`
   (`2a8bc17`) — the block report; describes runtime model finding
2. `review/comms/MAIN_TERMINAL_GTO_DISPATCH_RESOLUTION_2026-04-25.md`
   (this doc) — the decision and resume steps
3. `review/comms/MAIN_TERMINAL_GTO_DISPATCH_AUTHORITY_2026-04-25.md`
   (`21f16e6`) — the original authority + scope
4. `review/comms/BUILDER_V24_STAGE35_COMMIT_13_2_5_LANDED_2026-04-21.md`
   — FIX list under review

Pre-staged materials (preserved across restart — `/tmp` survives
session restart):

- `/tmp/bf4b24e_full.patch` — 397-line diff (verify exists with
  `ls -la /tmp/bf4b24e_full.patch`; if missing, regenerate with
  `git show bf4b24e --no-color > /tmp/bf4b24e_full.patch`)
- Self-contained dispatch brief draft (rebuild from the BLOCKED
  comms doc + builder's prior status report)
- Output target: `review/comms/GTO_REVIEW_VERDICT_13_2_5_2026-04-25.md`

### Smoke test before the actual dispatch

Before invoking gto-expert on the full 13.2.5 brief, do a 30-second
smoke test:

1. List available subagents (Agent tool's `subagent_type` enum
   should now include `gto-expert`)
2. Optionally invoke gto-expert with a trivial brief ("read /tmp/x
   and confirm receipt") to verify the agent loads and responds

This catches any second-order config issue before committing the
full review brief to a possibly-broken dispatch path.

If smoke test passes: dispatch the real 13.2.5 review with the
pre-staged brief.

If smoke test fails: STOP again, report BLOCKED with new
available-agents list and any error output, do not improvise.

## Forward-looking implication for teaching

Teaching builds the same protocol applies. When teaching dispatches
its own V3 compliance reviewer (and any other v2-local subagent
teaching uses), teaching's session must be launched from cwd inside
`~/river-rats-teaching/` (or wherever its v2-local agents live —
verify on next teaching session).

Teaching is currently held with no dispatch needed today. But when
teaching unholds post-commit-14 to run V3 review on C5.2 + C7,
teaching should pre-flight the same dispatch path (smoke test
before the real review). Teaching is hereby pre-notified of this
runtime constraint via this directive (cross-stream awareness).

## Cross-stream impact

| Item | Effect |
|---|---|
| Logic | 13.2.5 verdict held until builder restart + smoke test + dispatch; 13.3 still gated on APPROVE |
| Teaching | No immediate effect; pre-notified of the same constraint for post-commit-14 V3 dispatch |
| Game | No effect; game's stream uses no v2-local subagents |
| Cross-stream HOLD register | Unchanged; the block is dispatch-path-only, not a content/architecture issue |

## Standing pattern update — corrected runtime model

The dispatcher table in
`MAIN_TERMINAL_GTO_DISPATCH_AUTHORITY_2026-04-25.md` should be read
with this correction:

- **Logic builder** dispatches v2-local subagents (gto-expert, etc.)
  — session must be launched from `~/river-rats-v2/`
- **Teaching builder** dispatches teaching-local subagents (V3 compl.
  reviewer, etc.) — session must be launched from
  `~/river-rats-teaching/`
- **Orchestrator** never dispatches project-local subagents from
  `~/` — same runtime constraint, same direction

If a builder session is found launched from the wrong cwd, restart
is the resolution, not fallback.

## Reference

- `BUILDER_GTO_DISPATCH_BLOCKED_2026-04-25.md` (`2a8bc17`) — block
  report
- `MAIN_TERMINAL_GTO_DISPATCH_AUTHORITY_2026-04-25.md` (`21f16e6`) —
  prior authority + the corrected runtime claim
- `MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md` — the
  "lean into the constraint" precedent
- `feedback_quality_default_no_ask.md` — quality option chosen
  without re-asking owner
- CLAUDE.md §5 — STOP protocol; builder applied correctly

## Action

**Owner:**

1. Exit the current builder Claude Code session
2. `cd ~/river-rats-v2 && claude` (or local equivalent launch
   invocation)
3. Confirm new session is running and ready to resume

**Builder (post-restart):**

1. Read the resume protocol §"Resume protocol for builder"
2. Smoke-test gto-expert availability (Agent tool subagent_type
   includes `gto-expert`; trivial invocation succeeds)
3. On smoke-test PASS: dispatch real 13.2.5 review with pre-staged
   brief
4. Write verdict to `review/comms/GTO_REVIEW_VERDICT_13_2_5_2026-04-25.md`
5. Notify orchestrator via brief comms note when verdict lands
6. On smoke-test FAIL: STOP again, BLOCKED comms with new error
   output, do not improvise

**Orchestrator (me):**

1. Read GTO verdict when builder posts it
2. On APPROVE: write `MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_<date>.md`
3. On APPROVE_WITH_FIXES / REWORK: appropriate gating per
   `MAIN_TERMINAL_GTO_DISPATCH_AUTHORITY_2026-04-25.md` table
4. Pre-notify teaching of the same runtime constraint (this doc
   serves that purpose; teaching reads when unholding post-commit-14)
