---
date: 2026-04-25
from: Main terminal (orchestrator)
to: Logic builder · Owner
re: Push-policy resolution for unpushed commits bf4b24e + c4ab27e — Option B (feature-branch + PR)
status: DIRECTIVE — builder pushes to feature branch and opens PR; per-batch review pattern continues via PR review thread; owner endorsed quality option 2026-04-25
---

# Stage 3.5 Push-Policy Decision — Option B (Feature-Branch + PR)

## Decision

**Option B: feature-branch + PR.** Builder pushes the two unpushed
commits (`bf4b24e`, `c4ab27e`) to a new branch and opens a PR to
master. Owner endorsed the quality-focused option 2026-04-25;
orchestrator dispatches without re-asking per
`feedback_quality_default_no_ask.md`.

This becomes the standing pattern for all remaining Stage 3.5 commits
(13.3, 14, 15, 16, M4, M5) and for any subsequent multi-commit batch.

## Why B over A and C

**(A) Restore direct-push permission.** Speed option. Direct-to-master
was tightened deliberately mid-session — undoing it gives up the
discipline the tightening was meant to enforce. Quality default says
lean into the constraint, don't route around it.

**(C) Owner runs push from owner's terminal.** Technically lands the
commits but bypasses the same gate by switching terminals. No
structured review surface, no PR audit trail, and it normalises
"ask owner to push when blocked" as the relief valve — that erodes
the policy from the inside.

**(B) Feature-branch + PR.** What the policy is shaped for:

- PR diff view gives GTO reviewer / V3 reviewer / orchestrator a
  structured surface to comment on hunks (line-anchored review threads
  instead of free-text comms docs)
- Per-batch GTO review pattern already running for commits 13 / 13.2 /
  13.2.5 maps cleanly onto PR review threads
- Merge timing becomes orchestrator-greenlit explicitly (PR merge
  button) rather than implicit-on-push — same property teaching gets
  from PRE-VERIFICATION HOLD on its SHIP REPORT, now mirrored on the
  logic side
- Audit trail lives on GitHub natively; commit→review→merge linkage
  is queryable via `gh pr` rather than scattered across `review/comms/`

Cost: ~5 min per commit overhead (branch push + `gh pr create` +
merge after approval). Trivial vs. the 5–6 days of authoring work in
commits 13.3 / 14 / 16 that this path will gate.

## Concrete steps for the existing block (13.2.5)

From current `master` HEAD (`c4ab27e`):

```
git checkout -b stage3.5/commit-13-2-5
git push -u origin stage3.5/commit-13-2-5
```

Then open the PR:

```
gh pr create \
  --base master \
  --head stage3.5/commit-13-2-5 \
  --title "Stage 3.5 commit 13.2.5/16: GTO fix-forward on 2nd dry-run batch" \
  --body "<see body spec below>"
```

PR body should include:

1. Reference to the GTO reviewer APPROVE_WITH_FIXES verdict on
   329ecf7 that drove this fix-forward (link or paste the verdict)
2. The FIX #1–#5 list from `BUILDER_V24_STAGE35_COMMIT_13_2_5_LANDED_2026-04-21.md`
3. Test results: `test_commit13_sidecar_dryrun.py` 11/11 PASS, broader
   suite 1332 passed / 11 pre-existing failures (none are 13.2.5
   regressions)
4. Note that `c4ab27e` is the comms-doc companion — intentionally a
   separate commit for audit-trail reasons; do NOT squash on merge
5. Cross-stream impact: clears nothing on the teaching side directly;
   unblocks GTO re-review of 13.2.5 + commit 13.3 authorisation

After PR is open: builder pings orchestrator with the PR URL via a
short comms doc `BUILDER_PR_<num>_LANDED_2026-04-25.md`. From that
point, all review traffic for this commit lives on the PR, not in
`review/comms/`.

## Merge mechanics

On orchestrator + GTO reviewer both APPROVE on the PR:

```
gh pr merge <num> --merge --delete-branch
```

**Use `--merge` (merge commit), NOT `--squash`.** The two commits
(`bf4b24e` code + `c4ab27e` comms) are intentionally separate — the
GTO review verdict references the commit SHA pair, and Stage 3.5's
audit trail relies on per-commit SHAs surviving the merge. Squash
would collapse them and break the SHA references in
`BUILDER_V24_STAGE35_COMMIT_13_2_5_LANDED_2026-04-21.md` §4 and
elsewhere.

After merge: builder runs `git checkout master && git pull` to sync
local master, then proceeds to commit 13.3 authoring on a new feature
branch.

## Pattern for subsequent commits

Same shape. Branch naming: `stage3.5/commit-<n>` (e.g.
`stage3.5/commit-14`, `stage3.5/commit-16-m4-m5`).

**Commit 13.3** (~130-entry full lift): may be split into per-batch
PRs if GTO review pacing requires it. Orchestrator will decide the
split when 13.3 design lands; default assumption is one PR per
~25-entry batch with per-batch GTO reviews on each PR.

**Commit 14** (Finding B resolution): PR title must explicitly cite
Finding B. PR body must include:

- The 3-line promotion diff folding `_per_villain_folded`,
  `_per_villain_composition`, `_per_villain_overflowed` from
  `chain_meta` into the features dict
- The 4 new tests (`test_must46_per_villain_*_promoted_in_multiway`
  + HU-empty-dict regression)
- An explicit "unblocks teaching HOLD #5" line so the cross-stream
  trail is queryable from the PR alone

**Commits 15 / 16 / M4 / M5**: PR per logical commit, same pattern.
M4 and M5 audits may share one PR if they're authored together.

## Cross-stream impact when 13.2.5 PR merges

| Stream | Effect |
|---|---|
| Logic | GTO re-review of 13.2.5 unblocks (origin carries fix-forward); commit 13.3 authorisation issuable |
| Teaching HOLD #1 | Still pending — waits on commit 16 + M4/M5 clean |
| Teaching HOLD #3 / #5 | Still pending — wait on commit 14's multiway field promotion |
| Teaching HOLD #4 | Still pending — orchestrator pre-Stage-6 gate runs after #1, #3, #5 all clear |

No teaching-side action triggered by 13.2.5 alone. Teaching stays at
PRE-VERIFICATION HOLD on its SHIP REPORT.

## Standing discipline

No shortcut to merge. PR sits open until orchestrator + GTO reviewer
both signal APPROVE. STOP protocol still stands: any unexpected output
or failed assumption → builder reports BLOCKED on the PR thread, does
not improvise. Per-batch GTO review on commit 13.3 authoring continues;
no skipping. SHA-stable audit trail is now a PR property; preserve it
by avoiding force-pushes to merged feature branches.

If the orchestrator or reviewer comms docs themselves get caught by
the same direct-push policy (uncertain — the block has only been
observed on builder commits so far), they will follow the same flow:
short-lived feature branch + PR. We do not have a "comms is exempt"
carve-out.

## Reference

- `BUILDER_V24_STAGE35_COMMIT_13_2_5_LANDED_2026-04-21.md` — original
  push-block report with options A / B / C
- `MAIN_TERMINAL_CROSS_STREAM_FINDINGS_RESOLUTION_2026-04-24.md` —
  Finding B resolution and commit 14 spec
- `MAIN_TERMINAL_COMMIT13_DECISION_2ND_DRYRUN_2026-04-24.md` — the
  cb45c15 quality-default precedent for this kind of decision
- `feedback_quality_default_no_ask.md` — memory rule strengthened
  2026-04-24, applied here

## Action

**Builder:**

1. Push `bf4b24e` + `c4ab27e` to `stage3.5/commit-13-2-5`
2. Open PR to master per body spec above
3. Drop a one-line comms note (`BUILDER_PR_<num>_LANDED_2026-04-25.md`)
   with the PR URL
4. Wait for orchestrator + GTO reviewer APPROVE on the PR
5. Merge with `--merge` (not `--squash`), `--delete-branch`
6. `git pull` master locally, then proceed to commit 13.3 authoring
   on a new feature branch

**Orchestrator (me):**

1. Dispatch GTO reviewer re-review on 13.2.5 once the PR is open (the
   PR diff is the review surface, not the local SHA)
2. Approve PR on completion of GTO review + my own protocol-compliance
   check
3. Greenlight commit 13.3 authoring after 13.2.5 PR merges
4. Apply the same pattern to commits 14 / 15 / 16 / M4 / M5

**Owner:** no action required; briefed via this doc.
