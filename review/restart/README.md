# River Rats Restart Pack

**Date:** 2026-04-15
**Last updated:** GitHub-first prompts for remote machines

This folder holds everything needed to restart the River Rats
project in new terminals **on machines that can only access
GitHub** (not the owner's local filesystem).

## Quick links

- **Logic repo:** https://github.com/beytell1-sketch/river-rats-v2
- **Teaching repo:** no GitHub remote yet (local only)
- **This folder:** https://github.com/beytell1-sketch/river-rats-v2/tree/master/review/restart

## Files in this folder

| File | Purpose |
|---|---|
| `README.md` | This file — index |
| `RESTART_MAIN.md` | Prompt for the main reviewer/orchestrator terminal |
| `RESTART_BUILDER.md` | Prompt for the builder terminal |
| `RESTART_TEACHING.md` | Prompt for the teaching terminal (blocked until teaching repo is on GitHub) |
| `LINKS.md` | Every GitHub link you need, grouped by purpose |

## How to use

1. Open a new terminal (Claude Code session) on the target
   machine
2. Open the relevant RESTART_* file on GitHub via the link below
3. Copy the prompt block inside the file
4. Paste as the first message in the fresh Claude Code session
5. The session will clone the repo from GitHub and read the
   state files

## Direct links to the restart prompts

- [RESTART_MAIN.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/restart/RESTART_MAIN.md)
- [RESTART_BUILDER.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/restart/RESTART_BUILDER.md)
- [RESTART_TEACHING.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/restart/RESTART_TEACHING.md)
- [LINKS.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/restart/LINKS.md)

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
  can start L3 Phase 2 quality validation (if teaching repo
  is pushed to GitHub).

## Important: GitHub auth on the new machine

The builder needs to `git push` back to the logic repo. This
requires GitHub credentials on the new machine (PAT or SSH key).

If `git push` fails:
- The builder will report BLOCKED
- Owner sets up auth via GitHub CLI (`gh auth login`) or
  configures an SSH key before continuing

## Teaching repo bootstrap (if you want teaching on GitHub)

From your local `/home/rupertbeytell/river-rats-teaching/`
directory, run:

```
gh repo create river-rats-teaching --private --source=. \
  --remote=origin --push
```

Then add the resulting URL to `RESTART_TEACHING.md` Step 1.
