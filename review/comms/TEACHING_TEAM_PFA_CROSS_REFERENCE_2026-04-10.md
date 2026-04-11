---
date: 2026-04-10
from: Process reviewer (via owner)
re: Teaching team PFA finding — cross-reference with v3.1 feature 53
---

## Teaching team finding

The teaching team flagged that the 45-feature model (v2.2) cannot
track whether hero was the preflop aggressor. Their teaching
templates fall back to position-based inference (e.g., "BB is
always the defender"). They correctly identified this as a
structural gap.

## Cross-reference with v3.1

This gap was independently identified by the GTO Expert during
BET tree design on 9 April. Feature 53 (`is_preflop_aggressor`)
was added to resolve it. Computation:

```
is_preflop_aggressor = int(hero_position == opener_position)
```

Present in feature_keys.py line 79. All 3 factory batches were
regenerated with it. The BET decision tree uses it as a gate in
Steps 3 and 4.

## What this means

**For v2.2 (production):** The teaching team's finding stands.
The 45-feature model has no PFA feature. Their position-based
fallback is the correct workaround.

**For v3.1 (in progress):** The feature exists. Teaching templates
built against v3.1 can state "you are the preflop raiser"
directly from the feature value instead of inferring from
position. The BET tree's Step 3 (PFA value c-bet) and Step 4
(PFA bluff c-bet) both gate on this feature.

## Action for the builder

1. Notify the teaching team that v3.1 will have the feature
2. Ask if they want to update their templates to use it when
   v3.1 ships, or keep position-based inference for compatibility
3. Confirm the teaching system can consume 53-feature input when
   v3.1 is released (currently built for 45 features)
4. This is not a blocker for anything — just coordination

## Process note

The gap was found by two independent teams (teaching team + GTO
Expert). Both arrived at the same conclusion. This is a good
signal that the feature addition was correct.
