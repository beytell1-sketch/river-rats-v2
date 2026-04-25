---
date: 2026-04-25
from: Logic builder
to: Owner · Main terminal (orchestrator) · any future builder session
re: Restart-after-power-failure protocol — where state lives, how to recover, where to look for latest comms
status: PROTOCOL — canonical reference for state persistence + restart procedure across sessions and across power events
---

# Builder Restart Protocol

This document is the canonical answer to "if I lose this session
or there's a power failure, where is everything and how do I pick
back up?"

Per `feedback_github_is_state_not_local.md`: **GitHub origin is the
authoritative state.** Local working tree may be ahead, behind, or
in-flight. If in doubt, trust origin.

---

## 1. State map — where every kind of file lives

| Artifact | Location | Persistence guarantee |
|---|---|---|
| **Code & tests** (`river-rats-core/**`) | Authored on feature branches; merged to `master` via PR | After PR merge: on `origin/master`. Pre-merge: on `origin/stage3.5/commit-<n>` (pushed immediately after each commit). |
| **Comms docs** (`review/comms/*.md`) | Direct-pushed to `master` (NOT on feature branches) | Pushed to `origin/master` within seconds of being written. Push-policy parent directive allows direct-push for comms (PR-pattern is for code only). |
| **GTO verdict docs** (`review/comms/GTO_REVIEW_VERDICT_*.md`) | Direct-pushed to `master` | Same as comms docs. Verdict-on-PR-thread comment is a separate copy on GitHub PR thread. |
| **Diff staging files** (`/tmp/<branch>.patch`) | Local-only, ephemeral | Regenerable: `git show <SHA> --no-color > /tmp/<file>.patch`. Lost on power failure but trivially recreated. |
| **Memory (cross-session)** | `~/.claude/projects/-home-rupertbeytell/memory/` | Persists across builder sessions. Indexed via `MEMORY.md`. |
| **GitHub PR state** (open/merged/closed/comments) | `github.com/beytell1-sketch/river-rats-v2/pulls` | Authoritative; survives all local events. Query via `gh pr view <N>` or `gh pr list`. |
| **Working-tree edits** (uncommitted) | Local working tree on whatever branch is checked out | **NOT push-protected.** Lost only if the local filesystem dies. Survives session restart, survives shell crash. Standard `git status` + `git diff` shows what's uncommitted. |
| **Staged but uncommitted edits** | Local index | Survives session/shell restart, lost on filesystem death. `git status` shows. |

---

## 2. "Always-committed" discipline (what builder does per output)

Per the cadence I follow:

1. **After each batch of related edits** (typically 1-3 files for a focused change), I run `git add` + `git commit` + `git push` as a single Bash chain. Not per-file edit; per-logical-change.
2. **Comms docs are committed and pushed in the same Bash call** as their creation. They never sit uncommitted on local for more than the duration of one Bash call.
3. **Feature branches are pushed to `origin` with `-u` immediately after `git checkout -b`** so even an empty branch is recoverable.
4. **PR creation (`gh pr create`)** registers the branch state on GitHub instantly.

**What this means for power-failure recovery:** the maximum amount of work that can be lost is whatever was in flight in a single Bash call. In practice that's seconds to minutes of edits, not hours.

**What this DOESN'T cover:** in-flight edits between Bash calls. If I'm 6 Edit operations into a batch and power dies, those 6 edits are on disk but uncommitted. `git status` + `git diff` on restart shows them; you can either continue from there or `git restore` to discard.

---

## 3. Restart procedure (run these commands in order)

After power failure, network glitch, session crash, or any "where am I?" moment:

### Step 1 — Sync with origin (truth-source)
```bash
cd ~/river-rats-v2
git fetch --all --prune
git status -b
```
This shows the current branch, ahead/behind status vs origin, and any local commits that haven't been pushed.

### Step 2 — Check for in-flight uncommitted work
```bash
git status --short
git diff
git diff --cached
```
If anything appears: the previous session was mid-batch. Decide whether to continue (rare — usually safer to discard) or finish the batch by committing.

### Step 3 — Read recent comms (where the conversation was)
```bash
ls -lt review/comms/ | head -10
```
Most recent files at top. The newest 2-3 files describe the current state of play. Look for filenames like:
- `BUILDER_*` — what builder did / surfaced
- `MAIN_TERMINAL_*` — what orchestrator decided / directed
- `GTO_REVIEW_VERDICT_*` — review verdicts that drove fix-forwards or merges

### Step 4 — Check open PRs and PR state
```bash
gh pr list --state open
gh pr list --state merged --limit 5
```
Open PRs = work in-flight awaiting orchestrator merge.
Recent merged PRs = what just landed.

### Step 5 — Read the most recent orchestrator directive
The newest `MAIN_TERMINAL_*` doc tells you what the next action is. Look for the `## Action` section near the bottom — it spells out builder/orchestrator/owner responsibilities.

### Step 6 — Confirm git identity (rare, if first time on this machine)
```bash
git config user.name
git config user.email
```
Should match the recent commit authorship: `beytell1-sketch <beytell1-sketch@users.noreply.github.com>`. If missing, set repo-locally per `feedback_commit_autonomy.md`.

### Step 7 — Confirm gh auth (rare, if PAT expired)
```bash
gh auth status
```
Should show "Logged in to github.com account beytell1-sketch (keyring)".

---

## 4. Where to find the latest comms (sort order)

`review/comms/` filenames embed the date as `*_YYYY-MM-DD.md`. Two sort patterns to know:

**By modification time (chronological — recommended for restart):**
```bash
ls -lt review/comms/ | head -20
```

**By filename (alphabetical — useful for finding all docs of a type):**
```bash
ls review/comms/ | sort | grep BUILDER | tail -10
ls review/comms/ | sort | grep MAIN_TERMINAL | tail -10
ls review/comms/ | sort | grep GTO_REVIEW_VERDICT | tail -10
```

Filename prefix conventions:
- `BUILDER_*` — builder side (me)
- `MAIN_TERMINAL_*` — orchestrator side
- `GTO_REVIEW_VERDICT_PR_<N>_*` — per-PR GTO verdict
- `GTO_REVIEW_VERDICT_<commit>_*` — per-commit GTO verdict (used pre-PR-pattern)
- `TICKET_*` — cross-stream tickets
- `FEEDBACK_*` — process feedback
- `TEACHING_*` — teaching-stream comms (rare on logic side; mostly cross-stream relays)

---

## 5. Owner sanity-check commands

If you (owner) want to know "where is everything?" without bothering builder:

```bash
cd ~/river-rats-v2
git fetch --all --prune --quiet
git log --oneline -10                       # latest 10 commits on current branch
git log --oneline origin/master -10         # latest 10 commits on master
git status -b                               # any uncommitted/unpushed work?
gh pr list --state all --limit 5            # latest PR activity
ls -lt review/comms/ | head -10             # latest 10 comms docs by mtime
```

If any of these surprises you, ask builder. If everything looks expected, builder is mid-flow on whatever the latest `BUILDER_*` doc describes.

---

## 6. What's NOT covered

- **Long-running computations / model training:** none in flight currently. If they were, they'd live in `results/` or `training-data/` and need their own checkpointing.
- **Owner's working tree at `~/`:** orchestrator session lives there, not in `~/river-rats-v2/`. Orchestrator's local state is its own concern.
- **Teaching stream at `~/river-rats-teaching/`:** separate repo, separate session, separate restart procedure. This protocol is logic-stream only.

---

## 7. Discipline guarantees this protocol relies on

These are commitments builder makes per-output:

1. **Never leave uncommitted code on local for more than one tool-call duration.** If I edit 3 files for a logical change, the next Bash call commits and pushes them.
2. **Always push immediately after commit.** `git commit` and `git push` go in the same Bash chain.
3. **Comms docs commit-and-push in the same Bash call as their creation.** Never write-then-defer.
4. **Feature branches push-with-tracking on creation.** `git checkout -b … && git push -u origin …` is one chain.
5. **PR create registers immediately on GitHub.** `gh pr create` is the registration point.
6. **STOP protocol on any state mismatch.** Per CLAUDE.md §5 + the 4-checkpoint extension from `MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_2026-04-25.md`. Don't proceed if `gh pr view <N> --json state` doesn't match expectation.

If any of these guarantees slips in practice, surface it as a `BUILDER_*` comms doc and adjust the protocol.

---

## 8. If the restart procedure surfaces something unexpected

- **Local commits ahead of origin:** `git push` to publish. Check why they didn't push originally (network blip, hook failure, etc.).
- **Local working tree dirty after restart:** `git diff` to see what. Likely mid-batch edits from before the crash. Either complete the batch (commit + push) or `git restore` to discard.
- **Open PR with no recent comms doc explaining state:** check PR with `gh pr view <N>` and the `gh pr view <N> --comments`. The comments will show whether GTO review ran. If verdict is missing, dispatch GTO and finish the batch.
- **Feature branch on local but not on origin:** push it. `git push -u origin <branch>`.
- **Comms doc on local but not on origin:** commit + push. The push-policy parent directive allows direct-push for comms.
- **Untracked files I don't recognise:** investigate before deleting. Per CLAUDE.md "Don't take destructive actions as a shortcut." Could be owner-side work or another session's draft.

---

## 9. Reference

- `feedback_github_is_state_not_local.md` — origin is authoritative
- `feedback_commit_autonomy.md` — commit autonomously; set repo-local git identity if missing
- `feedback_shared_tree_commit_hygiene.md` — git status + git diff --cached before commit
- `feedback_check_comms_before_wait.md` — before declaring wait, recheck comms
- `MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_2026-04-25.md` — 4-checkpoint PR-state STOP discipline (`e87f371`)
- `MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md` — PR pattern for code; direct-push for comms (`b6c1ade`)
- CLAUDE.md §5 — STOP protocol conditions

---

## 10. One-line summary

**If anything goes wrong: `cd ~/river-rats-v2 && git fetch --all --prune && git status -b && ls -lt review/comms/ | head -10 && gh pr list --state open` — the answer to "where am I" is in those four commands.**
