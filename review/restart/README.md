# River Rats Restart Pack

**Date:** 2026-04-15

This folder holds everything needed to restart the River Rats
project in new terminals. Every link is a GitHub link so you
can open them from any browser or terminal.

## Quick links

- **Repo root:** https://github.com/beytell1-sketch/river-rats-v2
- **This folder:** https://github.com/beytell1-sketch/river-rats-v2/tree/master/review/restart

## Files in this folder

| File | Purpose |
|---|---|
| `README.md` | This file — index |
| `RESTART_MAIN.md` | Prompt for the main reviewer/orchestrator terminal |
| `RESTART_BUILDER.md` | Prompt for the builder terminal |
| `RESTART_TEACHING.md` | Prompt for the teaching terminal |
| `LINKS.md` | Every GitHub link you need, grouped by purpose |

## How to use

1. Open a new terminal (Claude Code session)
2. Copy the contents of the relevant RESTART_* file
3. Paste as the first message to that session
4. The session will pick up exactly where the previous one
   stopped

## Current project state (summary)

- **Gate 7 PENDING.** v2.2 model trained. FB-40 passed
  (72.5% vs 70% target). MW reference missed by 2.5pp
  (80% vs 82.5% target). Owner needs to solver-verify
  10 MW misses to decide ship vs iterate.
- **6 parallel tracks in flight** while waiting on solver
  (see `DIRECTIVE_POST_HRP_PARALLEL_TRACKS_2026-04-15.md`
  for details).
- **Builder stopped responding** mid-directive. Restart
  should resume Tier 1 tracks.
- **Teaching team unblocked** — has enriched label export,
  can start L3 Phase 2 quality validation.

See the RESTART_* files for specific instructions per terminal.
