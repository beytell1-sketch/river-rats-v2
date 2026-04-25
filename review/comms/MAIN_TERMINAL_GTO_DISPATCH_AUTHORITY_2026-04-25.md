---
date: 2026-04-25
from: Main terminal (orchestrator)
to: Logic builder · Owner
re: GTO reviewer dispatch authority — corrects prior over-claim; builder dispatches own GTO reviews; greenlight to dispatch on 13.2.5 now
status: DIRECTIVE + CORRECTION — supersedes "Orchestrator dispatches GTO" line in MAIN_TERMINAL_PUSH_POLICY_ADDENDUM_2026-04-25.md §Action; builder dispatches per standing per-batch pattern; orchestrator authorises 13.3 on APPROVE
---

# GTO Dispatch Authority — Builder Owns Dispatch

## Correction

`MAIN_TERMINAL_PUSH_POLICY_ADDENDUM_2026-04-25.md` §Action stated:

> Orchestrator (me): 1. Dispatch GTO reviewer on 13.2.5 (post-merge audit verdict)

This was an over-claim. The orchestrator terminal runs from cwd `~/`
and does not have access to the project-local `gto-expert` subagent
defined in `~/river-rats-v2/.claude/agents/gto-expert.md`. That agent
is dispatchable only from a terminal with cwd inside `~/river-rats-v2/`
— i.e. the logic builder terminal.

Corrected protocol: **builder dispatches its own GTO reviews.** This
matches the prior pattern (per-batch GTO review on commits 13 and 13.2
were dispatched from the logic terminal, not orchestrator). It also
matches the teaching side, where teaching dispatches its own V3
per-commit reviews from the teaching terminal.

The orchestrator's role on review traffic is:

- **Greenlight** the dispatch (authorisation gate)
- **Read** the verdict
- **Greenlight** the next commit (13.3) on APPROVE, or direct
  fix-forward on APPROVE_WITH_FIXES / REWORK
- **Pre-Stage-6 gate** at end of stage

Not to dispatch the agent itself. Builder owns the dispatch, the
agent invocation, and the verdict report.

## Greenlight: dispatch GTO on 13.2.5 now

Builder is authorised to dispatch the per-batch GTO reviewer on
commit 13.2.5 (`bf4b24e`) immediately. Dispatch context:

- **What's under review:** the 5 FIX-forward entries on top of the
  329ecf7 dry-run, plus the classifier disambiguation
  (`hu_bet_x_call_bet` vs `hu_donk_x_bet`)
- **Audit shape:** post-merge verdict (commit is on origin/master,
  not in a PR). Verdict is for the audit trail and to greenlight
  commit 13.3 — not to gate a merge that's already happened.
- **Reviewer scope per `BUILDER_V24_STAGE35_COMMIT_13_2_5_LANDED_2026-04-21.md`:**
  FIX #1 (SYN-T_B05 header), FIX #2 (SYN-F5 chain comment), FIX #3
  (SYN-F7 entry authored), FIX #4 (board format docstring), FIX #5
  (validator AST check), plus the classifier predicate change
- **Reviewer focus suggestions** are in your `7bca96a` comms doc

When the verdict lands, builder writes it to v2 comms as
`GTO_REVIEW_VERDICT_13_2_5_<date>.md` (or similar — match your prior
naming pattern).

## Orchestrator gating after the verdict

| Verdict | Orchestrator action |
|---|---|
| APPROVE | Greenlight commit 13.3 authoring (~130-entry full lift) on the new PR-pattern branch `stage3.5/commit-13-3` |
| APPROVE_WITH_FIXES | Builder fix-forward to 13.2.6 on a PR (not direct push, per standing pattern from 13.3 onward — though 13.2.6 sits in a grey zone since it would be a fix to a pre-PR-pattern commit; default to PR for consistency) |
| REWORK | Halt 13.2.5 acceptance; builder re-authors per fix list; new PR for the rework |

On APPROVE: orchestrator issues an explicit greenlight comms doc
`MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_<date>.md` enumerating the
~130-entry batch authorisation parameters (entry list, per-batch
sub-PR cadence if 13.3 splits, GTO review pacing).

## Standing reviewer-dispatch pattern (corrected, going forward)

| Stream | Reviewer agent | Dispatcher | Surface |
|---|---|---|---|
| Logic | gto-expert | Logic builder (v2 cwd) | Comms doc until 13.2.5; PR review thread from 13.3 onward |
| Logic | reviewer (process) | Logic builder (v2 cwd) | Per ad hoc when needed; PR thread from 13.3 onward |
| Teaching | V3 compliance reviewer | Teaching builder (teaching cwd) | Comms doc per existing pattern; will mirror PR thread when teaching unholds |
| Teaching | GTO compliance reviewer | Teaching builder (teaching cwd) | Comms doc; one-off when poker-judgment cross-check needed |
| Cross-stream | Orchestrator | Orchestrator (~/ cwd) | Comms doc — greenlight, gate, and verdict-archival; never dispatches the project-local subagents |

Memory rule applies: `feedback_review_autosave.md` ("reviewer always
writes reviews to review/comms/ without asking") is dispatcher-side
(reviewer's own builder writes the verdict to its own comms folder).
Orchestrator only reads + greenlights.

## Reference

- `BUILDER_V24_STAGE35_COMMIT_13_2_5_LANDED_2026-04-21.md` — fix list
- `MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md` + addendum — PR
  pattern from 13.3 onward
- `feedback_quality_default_no_ask.md` — quality option chosen
  without re-asking owner
- `feedback_queries_to_orchestrator.md` — cross-stream queries route
  via comms

## Action

**Builder:**

1. Dispatch gto-expert subagent on `bf4b24e` per standing per-batch
   pattern; brief includes the FIX #1–#5 + classifier scope
2. Write GTO verdict to v2 comms when it lands
3. HOLD on 13.3 authoring until orchestrator greenlight comms doc
4. On APPROVE_WITH_FIXES or REWORK: fix-forward via PR pattern
   (`stage3.5/commit-13-2-6` if it goes that way)

**Orchestrator (me):**

1. Read the GTO verdict when builder posts it
2. On APPROVE: write `MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_<date>.md`
   authorising the full lift
3. Continue to NOT dispatch project-local subagents (gto-expert,
   programmer, architect, ml-architect, reviewer, tester) from this
   terminal — they're builder-dispatched

**Owner:** no action; briefed via this doc.
