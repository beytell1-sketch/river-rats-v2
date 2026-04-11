---
date: 2026-04-09
from: Process reviewer (on behalf of owner)
re: Labelling approach — run BOTH deterministic and LLM, compare
---

## Owner direction

Run both labelling strategies independently on all 563 situations:

1. **Deterministic script** — applies all 3 decision trees
   mechanically to feature vectors. Produces labels based on
   thresholds only.

2. **LLM labelling agents** — per §1.1 (≤10 per agent), agents
   apply poker judgment using the labelling prompt + KB + trees
   as guidance. Produces labels based on reasoning.

Then compare the two sets. Disagreements are the signal —
they reveal:
- Script bugs (tree implemented wrong)
- Tree gaps (threshold doesn't capture the poker reality)
- LLM bias (agent deviated from tree due to known biases)

## What this changes

- Calibration IS still needed (LLM agents require it per §2.1)
- Agent allocation IS still needed (≥57 labellers + ≥29 reviewers
  per §1.1/§1.2)
- The deterministic script also runs (1 programmer task)
- A comparison step is added before final labels are approved

## Sequencing

1. Write and run deterministic script
2. Run calibration for LLM agents (53-feature situations)
3. Launch LLM labelling agents (≤10 per agent)
4. Compare outputs — flag all disagreements
5. Owner reviews disagreements and decides which label wins
6. Final label set approved

## Why this is valuable

Neither approach is perfect alone:
- Script is exact but only as good as the trees
- LLM agents bring poker reasoning but introduce bias
- Disagreements between them are where the learning happens
