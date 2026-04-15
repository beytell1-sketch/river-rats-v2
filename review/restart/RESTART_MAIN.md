# Restart Prompt — Main Terminal (Reviewer / Orchestrator)

Copy the block below into a fresh Claude Code session as your
first message.

---

```
I'm restarting the River Rats v2 project. You are the main
reviewer/orchestrator terminal.

Please start by reading these files from the repo at
/home/rupertbeytell/river-rats-v2/ in order:

1. review/comms/SESSION_STATE_2026-04-15.md
2. review/comms/HRP_INVESTIGATION_2026-04-15.md
3. review/comms/PHASE_4_TRAINING_REPORT_2026-04-15.md
4. review/comms/DIRECTIVE_POST_HRP_PARALLEL_TRACKS_2026-04-15.md
5. review/comms/REVIEW_PARALLEL_TRACKS_2026-04-15.md

Also read:
- CLAUDE.md for project conventions
- Your memory index at ~/.claude/projects/-home-rupertbeytell/memory/MEMORY.md

Current state summary:
- v2.2 model trained, Gate 7 pending
- FB-40 passed (72.5% vs 70% target)
- MW reference missed target by 2.5pp (80% vs 82.5%)
- Owner awaiting solver time for 10 MW misses
- 6 parallel tracks in flight per directive
- Builder stopped responding mid-directive

When builder comes back online, your role:
- Review incoming artifacts from builder
- Write reviews to review/comms/ without asking
- Commit and push your reviews to GitHub as we go
  (repo: https://github.com/beytell1-sketch/river-rats-v2.git)
- Track parallel tracks against the directive
- Flag any drift from the established plan

Owner context:
- Prefers slow/deliberate quality work
- Solver time is labour-intensive, not unlimited
- Values independence between agents — prompt-only, no plan
  leakage to labellers

Confirm you've read the files and summarize the current state
in 3-4 sentences. Then wait for owner direction.
```

---

## Notes

- The main terminal wrote almost all the owner-facing comms docs
- It has memory feedback rules already loaded (see MEMORY.md)
- Continue reading all comms files that come in — catch builder
  drops
- Always push reviews to GitHub when committed

## Links

- [SESSION_STATE_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/SESSION_STATE_2026-04-15.md)
- [All comms](https://github.com/beytell1-sketch/river-rats-v2/tree/master/review/comms)
