# Restart Prompt — Main Terminal / Orchestrator (2026-04-18)

Copy into a fresh Claude Code session.

---

```
I'm restarting the River Rats v2 main reviewer/orchestrator
terminal.

Clone if not present:
  git clone https://github.com/beytell1-sketch/river-rats-v2.git ~/river-rats-v2
  git clone https://github.com/beytell1-sketch/river-rats-teaching.git ~/river-rats-teaching

Also check ~/river-rats-game/ for game builder state (local,
not on GitHub).

Read these files in order:
1. ~/river-rats-v2/CLAUDE.md
2. ~/river-rats-v2/review/restart/SESSION_STATE_2026-04-18.md
3. ~/river-rats-v2/review/comms/MAIN_TERMINAL_UPDATE_2026-04-18-g.md
4. ~/.claude/projects/-home-rupert-river-rats-v2/memory/MEMORY.md
   (then read each referenced memory file)

Your role:
- Review incoming artifacts from all three builder terminals
- Write reviews to review/comms/ without asking
- Commit and push autonomously with descriptive messages
- Make recommendations, don't defer decisions to owner
- Track parallel streams against directives
- Flag drift from established plan

Three parallel streams active:
1. v2 core: v2.3.1 (air-CHECK counter-examples → retrain)
2. Teaching: value_extract air guard + standby for playtest
3. Game: F.4 real oracle+teaching adapters → playtest bundle

Owner preferences (from memory):
- Slow/deliberate quality, no rush
- Recommend, don't defer
- No static overrides anywhere — fix with features + examples
- Teaching highlights context, never explains why
- L3 must be playtested before L2/L1
- Range-based thinking is central
- board_adjusted_hrp replaces preflop HRP as postflop signal

Key pending items:
- v2.3.1 litmus tests: A4d/Qs5s7s + T5/JJ2 must CHECK
- Self-play diagnostic (post v2.3.1 ship)
- Solver on 8 MW misses (owner-paced)
- L3 playtest in game prototype → findings → L2/L1 unlocks

Confirm you've read the files and summarize current state
in 3-4 sentences. Then wait for owner direction or builder
drops.
```
