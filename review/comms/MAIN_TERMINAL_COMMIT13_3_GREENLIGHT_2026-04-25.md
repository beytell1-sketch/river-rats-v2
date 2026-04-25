---
date: 2026-04-25
from: Main terminal (orchestrator)
to: Logic builder · Owner
re: Commit 13.3 greenlight — ~130-entry full lift authorised; per-batch sub-PRs on stage3.5/commit-13-3-N; per-batch GTO review on each PR thread; standing PR + STOP discipline reaffirmed
status: DIRECTIVE — full-lift authorisation; sub-batch structure mandatory; orchestrator gates each sub-PR merge; commit 14 prep handoff at end
---

# Commit 13.3 — Full-Lift Greenlight

## Authorisation

**~130-entry full lift authorised.** Builder may begin authoring
on the new feature branch shape:

```
stage3.5/commit-13-3-1   # batch 1 of ~5
stage3.5/commit-13-3-2   # batch 2
stage3.5/commit-13-3-3   # batch 3
stage3.5/commit-13-3-4   # batch 4
stage3.5/commit-13-3-5   # batch 5 (final)
```

Each batch = its own PR to `master`. Per-batch GTO review on the PR
thread before merge. `--merge` (not `--squash`), `--delete-branch`
on completion, per `MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md`.

Sub-commits: `Stage 3.5 commit 13.3.<n>/16` in commit messages.

## Why sub-batches (mandatory, not optional)

Per push-policy directive default: "one PR per ~25-entry batch with
per-batch GTO reviews on each PR." Confirming that as the directive
shape for 13.3.

Three reasons:

1. **Catch systematic errors at batch 2, not batch 5.** A 130-entry
   single PR has the same systematic-error blast radius as the
   single-dry-run option (A) we already declined back in `cb45c15`.
   Sub-batches are the same quality argument applied at a lower
   level: if batch 1's classifier-routing is wrong, we catch it
   in 25 entries, not 130.
2. **GTO reviewer review pacing.** The general-purpose-with-gto-
   expert-persona dispatch path is owner-authorised but slower per
   review than a dedicated subagent. ~25-entry batches keep each
   review session bounded; ~130-entry single review is unbounded.
3. **Roll-back surface.** If batch 3 reveals a systematic problem,
   we revert one sub-PR and re-author 25 entries, not gut the
   whole 13.3 effort.

## Recommended batch composition

Group by shape category, not random partition. Reasoning: a
systematic authoring error usually hits all entries of the same
shape; grouping by shape concentrates the error surface in one
batch.

Per `MAIN_TERMINAL_COMMIT13_DECISION_2ND_DRYRUN_2026-04-24.md` and
prior batch outputs, the remaining ~75 reference slots split:

- **38 FB-* (HU)** entries: FB-01..16, FB-18..22, FB-24..40 (minus
  FB-17 / FB-23, already in dry-runs)
- **37 MW-* (multiway)** entries: MW-12..14, MW-16..29, MW-31..50
  (minus MW-11 / MW-15 / MW-30, already in dry-runs)
- Plus calibration mirrors and any remaining synthetic SYN-* entries
  to round out the ~130 total

Suggested batch shape (builder may adjust within this envelope):

| Batch | Branch | Approx. content | Approx. count |
|---|---|---|---|
| 13.3.1 | `stage3.5/commit-13-3-1` | FB-01..20 (HU shapes 1st half) + their calibration mirrors | ~25 |
| 13.3.2 | `stage3.5/commit-13-3-2` | FB-21..40 minus FB-23 + their calibration mirrors | ~25 |
| 13.3.3 | `stage3.5/commit-13-3-3` | MW-12..30 minus MW-15 / MW-30 + calibration mirrors | ~25 |
| 13.3.4 | `stage3.5/commit-13-3-4` | MW-31..50 + calibration mirrors | ~25 |
| 13.3.5 | `stage3.5/commit-13-3-5` | Remaining synthetics + any sweep cleanup | ~10-25 |

Builder may re-shape the batch boundaries based on shape-category
clustering or workflow ergonomics. The constraint is `~25 entries
per PR, ~5 PRs total`. If shape category boundaries argue for
unequal splits (e.g. one shape category needs all 30 entries
together to validate a cross-pattern invariant), adjust the table
and note the rationale in the first batch's PR description.

## Per-batch protocol

For each batch (1..5):

1. **Author** the batch on its branch, including:
   - Reference entries with full action-history sidecars
   - Calibration mirror entries
   - Any new tests (regression guards on shape-routing)
   - Validator + solver-verify stub runs (clean exit before pushing)
2. **Push** the branch to origin, **open the PR** to master with
   description including: shape categories covered, entry-count
   table, validator output, test results, classifier predicate
   compatibility check, links to upstream verdicts (PR #1's
   APPROVE provenance is the inheritable baseline)
3. **Re-check PR state immediately after creation** with
   `gh pr view <N> --json state` — per the BUILDER_PR_1_MERGED
   lesson, the create→view→dispatch→merge interval is where
   silent state transitions can stall a PR
4. **Dispatch GTO reviewer** on the batch with PR-thread-as-review-
   surface; pre-stage the diff (`git show <head> --no-color > /tmp/<branch>.patch`)
   and brief the reviewer with FIX-list inheritance from prior
   batches (each batch's review explicitly checks for regressions
   on prior fix-forward content like the position-aware classifier)
5. **Post verdict comment** on the PR thread with link to the
   `GTO_REVIEW_VERDICT_PR_<N>_<date>.md` audit-trail doc
6. **Re-check PR state** before merge (`gh pr view <N> --json state`)
7. **On APPROVE:** orchestrator merges via `gh pr merge <N> --merge --delete-branch`
8. **On APPROVE_WITH_FIXES:** builder fix-forwards on a 13.3.<n>.<m>
   sub-sub-PR (mirror of the 13.2.5 → 13.2.6 path); orchestrator
   greenlights merge of the fix-forward sub-sub-PR
9. **On REWORK:** builder reworks the batch on the same branch
   (force-push allowed only on the unmerged feature branch), GTO
   re-reviews, repeat

Build pacing: don't start batch N+1 until batch N has merged.
Reasoning: each merge updates origin/master; batch N+1 should be
authored against the post-batch-N state to catch shape-routing
interactions across batches early.

## STOP protocol — reaffirmed and extended

CLAUDE.md §5 conditions still trigger STOP. Builder applied this
correctly in the GTO-dispatch-blocked incident (`2a8bc17`) — same
discipline holds across the 13.3 sub-batches.

New addition per the BUILDER_PR_1_MERGED lesson:

- **State-mismatch between local expectation and GitHub PR state**
  is now a STOP condition. If `gh pr view <N> --json state` returns
  anything other than the expected state at any of the four
  checkpoints (post-create, pre-GTO-dispatch, post-verdict-comment,
  pre-merge), STOP and report BLOCKED. Don't merge based on a
  cached belief about PR state; verify against GitHub each time.

This addition will be folded into the next CLAUDE.md update window
(orchestrator will edit during the post-13.3 stabilisation pass);
treat it as canonical from this directive forward.

## GTO dispatch provenance — owner-authorised fallback

Owner authorised general-purpose subagent with gto-expert persona
embedded as the dispatch fallback while the dedicated subagent
session-config is unresolved. Each verdict comms doc must record
provenance honestly per the 13.2.6 example
(`GTO_REVIEW_VERDICT_13_2_5_2026-04-25.md` /
`GTO_REVIEW_VERDICT_PR_1_<date>.md`):

> **Reviewer provenance:** General-purpose subagent invoked with
> gto-expert persona embedded in brief. Owner authorised this
> fallback in-session due to dedicated gto-expert subagent not
> being registered in the current builder session; see
> `MAIN_TERMINAL_GTO_DISPATCH_RESOLUTION_2026-04-25.md` for the
> standing context.

Continues for every 13.3 batch verdict. The provenance discipline
is what protects the audit trail from quiet degradation; do not
drop the line because it's repetitive.

If at any point the dedicated gto-expert dispatch becomes available
(builder restarts session from `~/river-rats-v2/`, or session-config
gets fixed), switch back immediately and note the switchover in the
verdict doc. Don't continue with the fallback once the dedicated
agent is available.

## Cross-stream impact

| Stream | Effect of 13.3 lift |
|---|---|
| Logic | 13.3.1..13.3.5 sub-batches, then commit 14 (Finding B fold-in) is next |
| Teaching HOLD #1 | Still pending (waits on commit 16 + M4/M5); 13.3 progress bring this closer but doesn't clear it |
| Teaching HOLD #3 / #5 | Still pending — wait on commit 14, not 13.3 |
| Teaching HOLD #4 | Still pending — orchestrator pre-Stage-6 gate runs after #1 + #3 + #5 all clear |
| Game per-villain range bars | Same blocker as teaching #5 — clears with commit 14 |
| Game range_position_desc rename | Same blocker as teaching Path B |

Teaching and game streams continue to hold; no notification needed
on 13.3 progress until commit 14 lands.

## Commit 14 prep handoff (pre-position)

When 13.3.5 merges to master, **commit 14 is the next critical-path
item.** Builder should pre-prepare the commit 14 brief in scratch
(NOT committed) during the 13.3 sub-batches:

- 3-line promotion in `extract_range_composition`'s return dict:
  `_per_villain_folded`, `_per_villain_composition`,
  `_per_villain_overflowed` from `chain_meta`
- 4 new tests: `test_must46_per_villain_*_promoted_in_multiway`
  family + HU-empty-dict regression
- Branch: `stage3.5/commit-14`
- PR title MUST cite Finding B
- PR body MUST include "unblocks teaching HOLD #5" and "unblocks
  game per-villain range bars" (cross-stream traceability)
- Per-batch GTO review on the PR thread

Standing pattern for 14 / 15 / 16 / M4 / M5 unchanged — same PR
shape as 13.3 sub-batches.

## Reference

- `MAIN_TERMINAL_COMMIT13_DECISION_2ND_DRYRUN_2026-04-24.md` (`cb45c15`)
  — original ~130-entry envelope and shape category enumeration
- `MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md` (`b6c1ade`) +
  `MAIN_TERMINAL_PUSH_POLICY_ADDENDUM_2026-04-25.md` (`0bb91ef`) —
  PR pattern baseline
- `MAIN_TERMINAL_GTO_DISPATCH_AUTHORITY_2026-04-25.md` (`21f16e6`)
  + `MAIN_TERMINAL_GTO_DISPATCH_RESOLUTION_2026-04-25.md` (`15f7b07`)
  — dispatcher protocol and runtime constraint
- `BUILDER_V24_STAGE35_BLUEPRINT_V2_2026-04-22.md` (referenced by
  builder for MUST # cross-references)
- `feedback_quality_default_no_ask.md`,
  `feedback_github_is_state_not_local.md`,
  `feedback_shared_tree_commit_hygiene.md`

## Action

**Builder:**

1. Begin batch 13.3.1 on `stage3.5/commit-13-3-1`
2. Pre-stage diff path before each GTO dispatch
   (`/tmp/<branch>.patch`)
3. Re-check `gh pr view <N> --json state` at all four checkpoints
   (post-create, pre-dispatch, post-verdict-comment, pre-merge);
   STOP on state mismatch
4. Each verdict comms doc records dispatch provenance honestly
5. Don't start batch N+1 until batch N has merged
6. Pre-prepare commit 14 brief in scratch during 13.3 sub-batches
7. Surface anything unexpected via `BUILDER_*` comms doc

**Orchestrator (me):**

1. Read each batch's GTO verdict + PR description
2. Run my own protocol-compliance check before approving merge
   (PR state, branch naming, --merge not --squash, verdict
   provenance line present)
3. Merge each approved batch via
   `gh pr merge <N> --merge --delete-branch`
4. Issue commit 14 greenlight comms doc when batch 13.3.5 merges
5. Trigger pre-Stage-6 gate after commit 16 + M4/M5 clean
6. Notify teaching + game when commit 14 merges (cross-stream
   unblock signals)

**Owner:** no action required; briefed via this doc.

Standing pattern: orchestrator merges; builder authors + dispatches.
Teaching and game streams continue to hold. No deadlines (per
`feedback_no_deadlines.md`).
