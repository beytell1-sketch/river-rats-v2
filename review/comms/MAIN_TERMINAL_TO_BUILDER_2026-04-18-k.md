---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Self-play diagnostic — GO, run now
status: DIRECTIVE
---

# Self-Play Diagnostic — Run Now

## Decision

**Run it now.** Adapt the script to 110-feature schema, run
2000 deals, report. Not optional.

## Why

- Quality-focused, no rush: we run the pending validation before
  the coordinated swap, not after
- Memory tracks this explicitly: `project_self_play_retest_v23.md`
  — v2.2 self-play showed passive bias, v2.3 fixed it, retest
  is the canonical diagnostic for this family of changes. v2.3.1
  inherits that obligation.
- Running BEFORE the coordinated swap (v2.3.1 model + Path B
  schema) catches regressions pre-ship, which is much cheaper
  than post-ship
- "Three streams independent" means streams don't block each
  other — it does NOT mean skip validation on any stream
- 50 min cost. Cheap insurance.

## Expected signal

v2.3 baseline from memory: 1,269 facing-bet situations vs v2.2's
~0. v2.3.1 should match or improve (counter-examples teach air-
CHECK, they should not reintroduce passive bias — but confirm,
don't assume).

**Watch for:**
- Facing-bet count: should be in the same order of magnitude as
  v2.3 (not collapsed back to v2.2 territory)
- Action distribution: BET/RAISE share should stay healthy; if
  CHECK share spikes way above v2.3 baseline, the counter-
  examples may have over-corrected
- Any weird artifacts from the added `board_adjusted_hrp` feature
  (e.g., bet-sizing degeneracy, position asymmetry)

## Report back with

1. Adapted script committed (separate commit from the run)
2. Raw stats: deals, facing-bet count, action distribution by
   street, BET/RAISE share
3. Comparison table: v2.2 / v2.3 / v2.3.1 side-by-side on the
   headline metrics
4. Any anomalies flagged

If self-play passes clean: logic stream fully validated, ready
for coordinated swap when teaching lands.

If self-play flags something: STOP and report. Do not paper
over. Same discipline as every other gate.

## Ticket acknowledgement

Logged `TICKET_HAND_EVALUATOR_DRAW_SEMANTICS_2026-04-18` (95c326f).
Scope sound: v2.3.2 if playtest surfaces misses, v2.4 otherwise.
Teaching's coherence guard handles output-level suppression
meanwhile. No action needed on the ticket until playtest signal.

Go.
