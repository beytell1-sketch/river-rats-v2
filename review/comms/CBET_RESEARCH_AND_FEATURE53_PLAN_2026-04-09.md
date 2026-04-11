---
date: 2026-04-09
from: Builder
re: Pre-labelling scope — feature 53 + c-bet research
---

## Owner direction

1. Add is_preflop_aggressor as feature 53 before labelling
2. Research continuation betting in 3-way pots before labelling
   BET/bluff situations — the owner's poker intuition is the
   starting point for research, not a directive

## Owner's starting observations (for research team)

- PFA on dry board, missed → can c-bet bluff (villain respects range)
- PFA on wet board vs 2 opponents, no outs/blockers → can't bluff
- PFA on wet board WITH outs or flush blocker → can still bluff
- C-betting deserves the same treatment RAISE got: full research
  team, ≥8 sources, decision tree, independent review

## What this means for the pipeline

We currently have:
- RAISE decision tree v2 (approved) — covers RAISE/CALL when facing bet
- No BET decision tree — BET labels are currently GTO agent judgment

The owner is saying: BET labels need the same rigour as RAISE labels.
Before we label 563 situations, we need:

### Phase A: Feature 53 (is_preflop_aggressor)
1. Add to feature_extractor.py + feature_keys.py + gto_model.py
2. Regenerate all 3 factory batches with 53 features
3. Verify no existing features changed (data consistency check)

### Phase B: C-bet research (per §3.1)
1. Research team: ≥2 research agents + 1 reviewer
2. Minimum 8 sources on 3-way c-betting (GTO Wizard, Upswing,
   Galfond, PioSolver, academic)
3. Topics: c-bet frequency by PFA vs defender, board texture effects,
   multiway c-bet sizing, when to check back, blocker effects
4. Output: research synthesis document in review/

### Phase C: BET decision tree
1. GTO Expert synthesises research into a BET decision tree
   (like RAISE_DECISION_TREE_V2.md but for BET/CHECK decisions)
2. Must use feature 53 (is_preflop_aggressor) + existing 52 features
3. Independent review of the tree
4. Owner approval

### Phase D: Updated calibration
1. Update calibration exam with 53-feature situations
2. Re-run calibration (KB may need c-bet section added)
3. Gate must pass before labelling

### Phase E: Labelling (Step 7 revised)
1. Deterministic script applies BOTH trees:
   - RAISE tree for situations facing a bet
   - BET tree for situations not facing a bet
2. LLM reviewer sample checks both tree applications
3. Output: 563 labelled situations

## Timeline impact

This adds Phases A-D before labelling. Estimate:
- Phase A: 1 session (feature + regeneration)
- Phase B: 1 session (research)
- Phase C: 1 session (tree design + review)
- Phase D: same session as C (calibration)

## What doesn't change

- The RAISE decision tree v2 is approved and doesn't need changes
  (except possibly adding is_preflop_aggressor to an existing branch)
- The factory situations are designed and allocated
- The board allocation is final

## Recommendation

Start with Phase A (feature 53) in this session — it's mechanical.
Phase B (c-bet research) is the next session's primary task.
