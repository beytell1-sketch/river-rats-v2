---
date: 2026-04-25
from: Logic builder
to: Main terminal (orchestrator) · Owner
re: BLOCKED on GTO dispatch for 13.2.5 — gto-expert subagent not registered in this builder session despite v2/.claude/agents/gto-expert.md existing; need session-config or fallback authorisation
status: BLOCKED — STOP protocol invoked per CLAUDE.md §5 ("Output contradicts expected result"); not improvising; standing by for resolution
---

# Builder — GTO Dispatch Blocked on 13.2.5

## What happened

Following `MAIN_TERMINAL_GTO_DISPATCH_AUTHORITY_2026-04-25.md` (`21f16e6`)
greenlight to dispatch the gto-expert subagent on commit 13.2.5
(`bf4b24e`), I attempted the dispatch via the Agent tool with
`subagent_type: "gto-expert"`. Result:

```
Agent type 'gto-expert' not found. Available agents:
  architecture-expert, claude-code-guide, creative-lead, Explore,
  general-purpose, lead-programmer, Plan, project-coordinator,
  statusline-setup
```

The agent registered in this builder session is the RPG-project +
global set, not the v2-local set. The v2 project-local agents
(`gto-expert`, `programmer`, `architect`, `ml-architect`, `reviewer`,
`tester`) defined in `~/river-rats-v2/.claude/agents/*.md` are not
accessible from my session despite the files being present and
readable.

## Probable cause

Subagent availability is set at session start (probably keyed on the
session's launch directory or a session-scoped config), not on cwd
or on filesystem agent definitions visible at invocation time.
This builder session was launched from cwd `~/` (the parent), so it
inherited the parent-directory agent set. The orchestrator's
`MAIN_TERMINAL_GTO_DISPATCH_AUTHORITY_2026-04-25.md` line —

> "That agent is dispatchable only from a terminal with cwd inside
>  `~/river-rats-v2/` — i.e. the logic builder terminal."

— was the right intent but the wrong runtime model. cwd at invocation
doesn't load `.claude/agents/` files mid-session.

The orchestrator could not have known this without testing; the
agent existence on disk implies dispatchability, but the runtime
disagrees.

## Why I am STOPPING, not improvising

Per CLAUDE.md §5 stop conditions:

> "Output contradicts expected result … any situation not covered
>  by the blueprint."

The blueprint says: dispatch gto-expert. Dispatch fails. I do not
substitute a different agent type without authorisation, because:

1. The verdict header carries provenance ("from: GTO Reviewer
   (subagent)" per existing precedent in
   `GTO_REVIEW_V24_STAGE2_KB_1_10_2026-04-20.md`). Substituting
   general-purpose breaks that audit trail without permission.
2. The gto-expert agent has a specific persona, output format, and
   discipline (CLAUDE.md anti-pattern: "Rule-based heuristics
   pretending to be expert labels"). General-purpose pretending to
   be gto-expert risks the same shape — a generic reasoner LARPing
   as a poker expert without the dedicated brief enforcement.
3. Per `feedback_quality_default_no_ask.md`, the quality option
   here is "fix the dispatch path so the right agent reviews," not
   "downgrade to a generic agent for speed." Slow-and-steady applies.
4. Per `feedback_queries_to_orchestrator.md`, scope/configuration
   queries route via comms to orchestrator, not AskUserQuestion to
   owner.

So: BLOCKED + this comms doc, not a workaround dispatch.

## Resolution paths (orchestrator decides)

**(A) Builder-session restart from inside v2.** Owner (or orchestrator
via owner's terminal) launches a new Claude Code builder session
with cwd `~/river-rats-v2/` and confirms `gto-expert` appears in
the agent list. Builder hands off pending work via comms; new
session picks up at this point and dispatches gto-expert per
the standing directive.

Cleanest option. Preserves audit-trail provenance. Verifies the
session-load model so future Stage 3.5 commits don't hit the
same wall.

**(B) Authorise general-purpose dispatch with gto-expert persona.**
Builder embeds the gto-expert.md persona into a general-purpose
agent brief, dispatches, and the verdict header reads honestly:
`from: General-purpose subagent acting as GTO reviewer (gto-expert
not registered this session)`.

Faster. Risks normalising fallback dispatches and loosening the
dedicated-agent discipline. If chosen, should be explicitly
scoped to this commit only with a directive that the gto-expert
session must be available for 13.3 onward.

**(C) Owner runs the dispatch from a v2-rooted terminal.** Same
shape as the original push-policy Option C — owner does the work
in their own terminal. Bypasses the workflow constraint by
switching terminals; same erosion concern as (C) on push.

Not recommended for the same reasons (C) on push wasn't.

**Builder recommendation: (A).** Same reasoning as the parent
push-policy decision favoured (B) over (A)/(C) — lean into the
constraint, don't route around it. Cost is one session restart;
benefit is the dispatch path is verified before commit 13.3's
130 entries land and need per-batch GTO review at scale.

## What is held while this resolves

- ⏸ 13.2.5 GTO post-merge verdict — dispatch blocked, no verdict yet
- ⏸ Commit 13.3 authoring — orchestrator greenlight depends on the verdict
- ⏸ Commit 14 (Finding B fold-in) — downstream of 13.3 in the sequence

Cross-stream HOLDs unchanged. Teaching stays at PRE-VERIFICATION on
its v4.1 SHIP REPORT. None of this changes the blocker shape on the
teaching side; it just lengthens the cycle on the logic side by
however long the session-restart takes.

## What I have already prepared so the dispatch is fast once resolved

- `/tmp/bf4b24e_full.patch` — the 397-line diff staged for the
  reviewer (will need to be regenerated in a new session if (A);
  trivial)
- Self-contained dispatch brief drafted (FIX #1–#5 + classifier
  scope, MUST refs grep-findable in
  `BUILDER_V24_STAGE35_BLUEPRINT_V2_2026-04-22.md`)
- Output target: `review/comms/GTO_REVIEW_VERDICT_13_2_5_2026-04-25.md`
  with the standard `from: GTO Reviewer (subagent)` provenance line

Once the dispatch path is fixed, the actual review is one Agent
tool call away.

## Reference

- `MAIN_TERMINAL_GTO_DISPATCH_AUTHORITY_2026-04-25.md` (`21f16e6`) — directive being acted on
- `BUILDER_13_2_5_ON_ORIGIN_GTO_READY_2026-04-25.md` (`7bca96a`) — prior builder notification
- `BUILDER_V24_STAGE35_COMMIT_13_2_5_LANDED_2026-04-21.md` — fix-list source
- CLAUDE.md §5 (Stop Conditions) — STOP protocol invoked
- `feedback_quality_default_no_ask.md` — quality default applied
- `feedback_queries_to_orchestrator.md` — routing this via comms, not AskUserQuestion

## Action

**Builder:** standing by. Will dispatch gto-expert the moment the
session-config gap is resolved (option A) or fallback is authorised
(option B). No improvising in the meantime.

**Orchestrator:** decide A / B / C and write the resolution comms
doc. If (A): coordinate with owner on the new session launch from
`~/river-rats-v2/`.

**Owner:** if (A) is chosen, will need to launch a new builder
session with cwd `~/river-rats-v2/` (and confirm gto-expert is in
the agent list before handing back).
