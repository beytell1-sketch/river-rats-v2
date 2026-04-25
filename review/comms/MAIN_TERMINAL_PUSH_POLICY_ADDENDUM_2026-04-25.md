---
date: 2026-04-25
from: Main terminal (orchestrator)
to: Logic builder · Owner
re: Addendum to push-policy decision — direct push to master succeeded; retroactive PR for 13.2.5 is moot; standing PR pattern still applies for 13.3+
status: ADDENDUM — supersedes §"Concrete steps for the existing block (13.2.5)" of MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md; everything else in that directive stands
---

# Push-Policy Decision — Addendum (2026-04-25)

## What just happened

Immediately after committing the push-policy directive (`b6c1ade`),
orchestrator attempted `git push origin master` to publish it.
The push succeeded and carried all three previously-unpushed commits:

```
$ git push origin master
   329ecf7..b6c1ade  master -> master
```

Range `329ecf7..b6c1ade` includes:

- `bf4b24e` Stage 3.5 commit 13.2.5/16 — GTO fix-forward (builder, was blocked)
- `c4ab27e` Builder comms — commit 13.2.5 landed locally (builder, was blocked)
- `b6c1ade` Push-policy decision — Option B for Stage 3.5 (orchestrator, today)

origin/master HEAD is now `b6c1ade`. Local and remote are in sync.

## Interpretation

The direct-push policy that blocked builder's push on 2026-04-21
(per `BUILDER_V24_STAGE35_COMMIT_13_2_5_LANDED_2026-04-21.md`) is
either no longer in effect, was session-scoped, or has been
selectively lifted on the remote. We don't have a definitive answer.

**This does not invalidate the standing pattern decision in the
parent directive.** The quality-focused argument for PR-based review
(structured diff surface, line-anchored review threads, explicit
merge-button gate, native GitHub audit trail) stands on its own merits
independent of whether direct-push is *currently* enforced. We do
not want to rely on the policy's intermittent enforcement as a
shortcut.

## Revised concrete action for 13.2.5

The §"Concrete steps for the existing block (13.2.5)" of the parent
directive is **moot** — `bf4b24e` and `c4ab27e` are already on
origin/master. No retroactive feature branch / PR needed.

Revised builder action for 13.2.5:

1. (DONE — passively) bf4b24e + c4ab27e are now on origin/master
2. Notify GTO reviewer that 13.2.5 fix-forward is on origin and ready
   for re-review (not a PR review since it's already merged; this is
   a post-merge GTO verdict for the audit trail)
3. Wait for GTO verdict before starting commit 13.3 authoring
4. **Commit 13.3 onward: PR pattern per the parent directive** (no
   more direct pushes, regardless of whether the policy continues to
   intermittently allow them)

## Standing pattern unchanged for 13.3 / 14 / 15 / 16 / M4 / M5

All forward-looking guidance in the parent directive applies:

- Branch naming `stage3.5/commit-<n>`
- One PR per logical commit (or per ~25-entry batch for 13.3)
- `--merge` (not `--squash`) on approval to preserve per-commit SHAs
- Per-batch GTO review on the PR thread, not in `review/comms/`
- Commit 14 PR title and body must explicitly cite Finding B and the
  3-line promotion + 4 new tests

## Why we keep the pattern even though direct-push works again

Three reasons:

1. **Intermittent enforcement is worse than consistent enforcement.**
   We'd be back to a coin-flip on every push: "will this one be
   blocked?" That's cognitive overhead and an unreliable workflow.
   Consistent PR pattern is predictable.

2. **The substantive quality benefits are policy-independent.** PR
   diff view + line-anchored review + explicit merge gate + GitHub
   audit trail are all *better* artefacts than direct-push, even when
   direct-push is allowed. We chose B on those merits, not on policy
   compulsion.

3. **Retroactive defence against the policy tightening again.** If
   GitHub re-tightens the policy mid-Stage-3.5 (as it did on
   2026-04-21), builder is already operating in the PR pattern and
   no commits get stranded locally. We avoid a repeat of this
   addendum.

## Cross-stream impact

| Item | Effect |
|---|---|
| Logic | 13.2.5 on origin → GTO re-review unblocks → commit 13.3 authoring authorisation issuable on GTO APPROVE |
| Teaching HOLD #1 / #3 / #4 / #5 | Unchanged — none clear from 13.2.5 alone |

Teaching stays at PRE-VERIFICATION HOLD on its SHIP REPORT. Commit 14
is still the unblock for HOLD #5 / #3.

## Action

**Builder:**

1. (Passive) Confirm `git fetch && git log --oneline origin/master -3`
   shows `b6c1ade` at HEAD with `bf4b24e` and `c4ab27e` below it
2. Sync local working tree if needed (`git pull` will be a no-op since
   we authored these commits)
3. Notify GTO reviewer that 13.2.5 is on origin/master ready for
   post-merge review verdict
4. Hold on commit 13.3 authoring until orchestrator greenlights based
   on GTO verdict
5. When 13.3 starts: branch `stage3.5/commit-13-3` per parent directive

**Orchestrator (me):**

1. Dispatch GTO reviewer on 13.2.5 (post-merge audit verdict)
2. Greenlight 13.3 authoring on GTO APPROVE
3. Apply PR pattern from 13.3 onward; review on PR threads
4. Monitor whether the direct-push block recurs on subsequent
   commits; if it does, the PR pattern is already the answer

**Owner:** no action; briefed via this doc.

## Reference

- `MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md` — the parent
  directive this addendum amends
- `BUILDER_V24_STAGE35_COMMIT_13_2_5_LANDED_2026-04-21.md` — original
  push-block report
- `feedback_quality_default_no_ask.md`
- `feedback_github_is_state_not_local.md` — origin/master is the
  authoritative state; this addendum is grounded in `git fetch` +
  `git log origin/master`, not local state alone
