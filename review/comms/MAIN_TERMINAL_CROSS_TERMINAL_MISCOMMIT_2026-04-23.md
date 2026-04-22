---
date: 2026-04-23
from: Main terminal (orchestrator)
to: Builder · Owner
re: Cross-terminal miscommit — 0c3e0ec accidentally bundled commit-8 deletions
status: INCIDENT — deletions landed correctly on origin but under wrong commit title; no corruption; path forward documented
---

# Cross-Terminal Miscommit — 0c3e0ec

## What happened

Orchestrator pushed `0c3e0ec` with intended scope:
- NEW: `review/comms/TICKET_MUST64_OPP_POSITIONS_ORDERING_2026-04-23.md`
- MODIFIED: `RELEASE_MANIFEST.yaml`

Actual landed scope per `git show --stat 0c3e0ec`:
- NEW: TICKET_MUST64_...md ✓ (intended)
- MODIFIED: RELEASE_MANIFEST.yaml ✓ (intended)
- **DELETED: river-rats-core/coaching/feature_extractor.py** (UNINTENDED — builder's commit-8 scope)
- **DELETED: river-rats-core/coaching/range_narrowing.py** (UNINTENDED — builder's commit-8 scope)

## Root cause

Shared working tree across terminals (`~/river-rats-v2/`). Builder was
drafting commit 8 (MUST #8 partial-delete + MUST #37 sys.path audit)
in parallel with orchestrator writing the teaching-v4.1-approval +
MUST #64 ticket.

Builder had `git rm`'d the two coaching duplicates (staging the
deletions to the git index) before writing the commit-8 test file.
Orchestrator ran `git add <ticket> <manifest> && git commit` —
`git commit` includes ALL staged changes by default, not just those
explicitly added in the same invocation.

This is the exact class of cross-terminal contamination risk flagged
in `feedback_github_is_state_not_local.md` + the owner's earlier
direction about shared filesystem. Orchestrator should have run
`git status --porcelain` before committing to catch staged deletions
from other terminals' work.

## Damage assessment

- **Deletions are correct.** The two files were slated for deletion
  in commit 8 per MUST #8 partial-delete scope. They're now gone from
  origin as intended.
- **Attribution is wrong.** The deletions are in commit `0c3e0ec`
  titled "Teaching v4.1 plan APPROVED" rather than a properly-scoped
  commit-8 commit. `git blame` on the deleted files' absence will
  surface a confusing trail.
- **Test file untracked.** `river-rats-core/tests/test_commit8_must8_37.py`
  sits in working tree but not committed. Builder's commit-8 work is
  incomplete.
- **MUST #37 sys.path audit.** Not yet landed. Must be in commit 8
  properly before Stage 4 work can proceed with confidence that
  surviving coaching/* modules are safe post-deletion.

No model code was broken. No tests should have regressed (commit 8
was going to land the deletions anyway). Pure attribution + commit-
hygiene issue.

## Path forward

Commit 8 scope is now REDUCED to:

1. **Test file** `test_commit8_must8_37.py` (NEW) — add + commit
2. **MUST #37 sys.path audit** — audit surviving coaching/* modules
   for dependency on the deleted files' sys.path side-effects; fix
   any breakage
3. **Commit message** cites both the test + audit + notes:
   > "File deletions (coaching/feature_extractor.py + coaching/
   > range_narrowing.py) landed prematurely in orchestrator commit
   > 0c3e0ec due to cross-terminal shared-tree contamination.
   > This commit completes the commit-8 scope: test coverage + MUST
   > #37 sys.path audit results."

Builder proceeds per this reduced scope. Single-architect reviewer
pass still applies.

## Discipline rule addition

New rule for orchestrator + builders operating in shared working tree:

**Before `git commit`, ALWAYS run `git status` and verify the staged
changes match EXACTLY the intended scope.** If unexpected staged
changes appear (from another terminal's in-progress work), either
(a) stash them, commit intended scope, un-stash, OR (b) pause the
commit and coordinate with the other terminal on attribution.

Orchestrator should also run `git diff --cached` pre-commit on any
multi-terminal shared tree to see the full staged diff before
finalising.

Adding to memory at `feedback_shared_tree_commit_hygiene.md`
(next memory entry).

## Non-impact on Stage 3.5 trajectory

- Commit sequence unchanged (commit 8 just has reduced scope)
- Remaining commits (9-16) unaffected
- Teaching v4.1 C1 authorisation unaffected — the orchestrator intent
  in 0c3e0ec is preserved; teaching proceeds
- MUST #64 ticket filed correctly
- Manifest v1.11 updated correctly

## Action

- Builder: commit 8 per reduced scope above (test file + sys.path
  audit + commit message note). Orchestrator single-architect
  reviewer pass follows.
- Orchestrator: saving shared-tree commit-hygiene memory rule.
- Owner: aware; no action needed unless they want me to revert
  0c3e0ec + re-split (not recommended; force-push on main + history
  churn > attribution confusion).

## Reference

- `git show --stat 0c3e0ec` shows the actual landed diff
- `feedback_github_is_state_not_local.md` (existing memory) — the rule
  that prompted the catch
- Cumulative state: origin HEAD 0c3e0ec; commit 8 work pending at
  reduced scope
