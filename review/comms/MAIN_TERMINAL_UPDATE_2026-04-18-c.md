---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Run v2.3 self-play diagnostic — does the bias correction hold in dynamic play?
status: DIRECTIVE — run now
---

# Self-Play Diagnostic with v2.3

v2.3 shipped. The defensive-multiway-checked-through CHECK
bias that killed v2.2 self-play is corrected. Time to test
whether the fix holds in dynamic play.

## Task

Run `self_play.py` with the shipped v2.3 model
(`river-rats-core/models/v2_3_model_shipped.json`).
2000 deals, same configuration as the v2.2 self-play
baseline documented in `SESSION_PROGRESS_2026-04-12.md`.

## Metrics to report

Compare v2.3 vs v2.2 baseline on:

| Metric | v2.2 baseline | v2.3 (measure) |
|---|---|---|
| Check-to-hero BET probability < 0.05 | 63% | ? |
| Facing-bet 3-way situations per 2000 deals | ~0 | ? |
| 3-way postflop yield | 3.7% | ? |
| Total postflop decisions logged | ? | ? |
| BET actions taken (any seat) per 1000 deals | ? | ? |
| Average pot size at showdown | ? | ? |

The critical number is **facing-bet situations**. If v2.3
self-play produces non-zero facing-bet situations where v2.2
produced zero, that's the strongest evidence the bias
correction works in dynamic play — not just on static test
sets.

## Configuration

- Model: `v2_3_model_shipped.json`
- Deals: 2000
- Seeds: same seed set as v2.2 baseline if documented;
  otherwise 6 seeds × ~334 deals each
- All 6 seats use oracle callbacks (same as v2.2 setup)
- Hero cycles through all positions per deal
- Log per-decision: position, street, action taken, BET
  probability, facing_bet flag, feature snapshot

## What NOT to do

- Do NOT modify self_play.py. Run it as-is with the new
  model.
- Do NOT use self-play output as training data yet. This is
  a diagnostic run.
- Do NOT adjust any oracle parameters. Standard inference
  with the shipped model.

## Deliverable

`review/comms/SELF_PLAY_DIAGNOSTIC_V23_2026-04-18.md` with:

- The comparison table above
- Distribution of BET probability in check-to-hero spots
  (histogram or percentile summary)
- Count and list of facing-bet situations generated (if any)
- Per-street breakdown of actions taken
- Assessment: is the passive loop broken?
- If facing-bet yield is non-zero: how many situations are
  "interesting" for potential v2.4 expert-labelling? (rough
  count, not a full curation)

## Why this matters

If self-play works with v2.3, it opens a new data source for
v2.4: self-play generates realistic game situations, expert
panels label them. This avoids both the factory-generation
artificiality problem AND the oracle-labels-its-own-data
reinforcement problem. Best of both worlds.

If self-play still shows the passive loop, the bias
correction doesn't generalize to dynamic play — that's a
finding that affects how we scope v2.4.

## Priority

Run after the v2.3 ship commit is pushed (447254d — already
done). This is a single programmer call, ~30-45 min including
the 2000-deal run + metrics extraction.
