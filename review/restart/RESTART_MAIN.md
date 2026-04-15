# Restart Prompt — Main Terminal (Reviewer / Orchestrator, GitHub-first)

Copy the block below into a fresh Claude Code session as your
first message.

---

```
I'm restarting the River Rats v2 main reviewer/orchestrator
terminal on a new machine. You can only access GitHub (no local
filesystem from prior session).

STEP 1: Clone the repo if it doesn't exist locally.

Check if you have a local clone of
https://github.com/beytell1-sketch/river-rats-v2.git
with a `.git` directory. If not, clone it to a writable path:

  git clone https://github.com/beytell1-sketch/river-rats-v2.git \
    ~/river-rats-v2

cd into the clone and confirm `git status` shows a clean tree
on master. This is your working directory.

STEP 2: Read these files from the cloned repo:

1. review/restart/ORCHESTRATOR_UPDATE_2026-04-15.md ← LATEST HANDOFF (read first)
2. review/comms/SESSION_STATE_2026-04-15.md
3. review/comms/HRP_INVESTIGATION_2026-04-15.md
4. review/comms/TRAINING_DATA_AUDIT_2026-04-15.md
5. review/comms/MAIN_TERMINAL_UPDATE_2026-04-15.md
6. review/comms/PHASE_4_TRAINING_REPORT_2026-04-15.md
7. review/comms/DIRECTIVE_POST_HRP_PARALLEL_TRACKS_2026-04-15.md
8. review/comms/REVIEW_PARALLEL_TRACKS_2026-04-15.md
9. CLAUDE.md for project conventions

If you have access to the owner's memory at
~/.claude/projects/-home-rupertbeytell/memory/MEMORY.md,
read that too. If not, the key feedback rules are:
- Reviewer writes to review/comms/ without asking
- Commit autonomously with descriptive messages
- Before declaring a wait state, check `ls -lt review/comms/
  | head -5` for late drops
- Verify source files before asserting claims
- Slow and deliberate — quality over speed

STEP 3: Current state summary.

- v2.2 model trained, Gate 7 pending solver verification
- FB-40 passed (72.5% vs 70% target)
- MW reference missed target by 2.5pp (80% vs 82.5%)
- Owner awaiting solver time for 10 MW misses
- 6 parallel tracks in flight per directive
- Previous builder session stopped responding

STEP 4: Your role when builder comes back online.

- Review incoming artifacts from builder
- Write reviews to review/comms/ without asking
- Commit and push your reviews to GitHub as we go (repo:
  https://github.com/beytell1-sketch/river-rats-v2.git)
- Track parallel tracks against the directive
- Flag any drift from the established plan

STEP 5: Commit protocol.

- Use `git commit` with a HEREDOC co-author line
- Push to origin/master after each meaningful review or
  directive
- If `git push` needs credentials, report BLOCKED and request
  credentials from owner

Confirm you've read the files and summarize the current state
in 3-4 sentences. Then wait for owner direction.
```

---

## Notes

- The main terminal owns owner-facing reviews and directives
- It does NOT write code — only comms documents
- All paths in referenced docs are relative to the repo root,
  so they work in any clone
- `git push` requires auth. If it fails, report BLOCKED.

## Links

- [Repo root](https://github.com/beytell1-sketch/river-rats-v2)
- [SESSION_STATE_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/SESSION_STATE_2026-04-15.md)
- [All comms](https://github.com/beytell1-sketch/river-rats-v2/tree/master/review/comms)
