---
date: 2026-04-09
from: Process reviewer (on behalf of owner)
re: Phased labelling — 100 first, compare, then continue
---

## Owner direction (supersedes DUAL_LABELLING note)

Do NOT launch all 57 agents at once. Phase the labelling:

### Phase 1: Pilot (100 situations)
- Run deterministic script on all 563 (fast, do this first)
- 10 LLM labelling agents × 10 hands = 100 situations
- Compare LLM labels against script labels for those 100
- Review all disagreements
- Assess: is the briefing working? Is the bias showing up?
  Are the trees correct? Does the approach need adjustment?

### Gate: Owner reviews Phase 1 comparison before proceeding

### Phase 2-N: Remaining situations in batches
- Batch size and briefing adjusted based on Phase 1 findings
- Continue until all 563 are dual-labelled

## Why phased

- If agents fail or show bias, we catch it at 100 not 563
- If the trees have gaps, disagreements in 100 hands surface them
- Adjusting the briefing after 100 is cheap; after 563 is waste
- Same principle as testing yield with 10 deals before 10,000

## Allocation for Phase 1

- 10 labelling agents (≤10 hands each) per §1.1
- ≥5 reviewers (reviewer count ≥ labeller count ÷ 2) per §1.2
- Calibration must pass first (§2.1)
- Reviewer brief must include over-fold bias warning

## Stratification

The 100 situations should be stratified across sub-patterns and
batches, not just the first 100 in sequence. The builder should
select ~10 from each major category (SP1-SP10 proportional) plus
a sample from the self-play and original factory batches. This
ensures Phase 1 covers the full decision space.
