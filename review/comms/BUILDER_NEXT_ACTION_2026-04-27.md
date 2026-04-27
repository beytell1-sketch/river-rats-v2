---
date: 2026-04-27
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER (named author of next build cycle)
re: NEXT ACTION — execute build-execute directive; this is AUTHORING not polling
status: AUTHORING — open active build directive
---

# Builder — your next action

**You are the named author** of the corpus revision pipeline execution. Per memory `feedback_named_author_builds_not_polls.md`, your next /loop tick is **AUTHORING**, not polling.

## What to do (in this exact order)

```
cd ~/river-rats-v2 && git pull --ff-only origin master
```

Read in full: `review/comms/MAIN_TERMINAL_BUILD_EXECUTE_DIRECTIVE_2026-04-27.md` (master HEAD `b39126b`).

That directive specifies:
- E1: re-extract 100-hand pilot corpus (corrected SPR + IS_PFA reconstruction)
- E2-B: Mode B factory pool (111 records expected)
- E2-A: Mode A self-play pool (CO/BTN/BB positions — NOT UTG, your Phase 2 Q3)
- E3: schema compatibility verify
- C2: 500-hand corpus assembly

Each step has a verification gate. STOP on any gate failure.

## When done

1. Open data-only PR on branch `programmer/corpus-revision-execution-2026-04-27` with: new data files (`data/pilot_corpus_100_hand_2026-04-26_v2.jsonl`, `data/corpus_revision_pool_mode_*.jsonl`, `data/corpus_revision_500_hand_2026-04-27.jsonl`, lock file) + your report at `review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_2026-04-27.md`.
2. Comment on the PR with structural attestation summary.
3. Notify orchestrator (this terminal) by way of the PR being open + comm landing in `review/comms/`.

## Do NOT

- Do NOT run anything outside the directive's E1 → E2-B → E2-A → E3 → C2 sequence.
- Do NOT improvise on gate failures (STOP + report BLOCKED).
- Do NOT include code changes in the data PR (data-only).
- Do NOT push to master (PR workflow only; orchestrator + reviewer + owner gate).

## Why this is "authoring" not "polling"

Per `feedback_named_author_builds_not_polls.md`: "When /loop reads a comm naming YOU as the author of an active build directive, next tick is AUTHORING, not polling. /loop monitoring is for between-cycles only, not a substitute for your own active work."

This comm names you (LEAD-PROGRAMMER) as the author of an active build directive. The build directive is at master `b39126b`. The work has NOT been authored yet (no `programmer/corpus-revision-execution-2026-04-27` branch exists; no `PROGRAMMER_REPORT_BUILD_EXECUTE_2026-04-27.md` exists). So your next action is AUTHORING.

If you are reading this comm in a /loop tick: switch to authoring mode now.

**Status: BUILDER NEXT ACTION OPEN. Authoring required.**
