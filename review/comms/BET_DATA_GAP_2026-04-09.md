---
date: 2026-04-09
from: Builder
re: BET tree data gap — factory wasn't designed for c-bet scenarios
---

## Finding

The recalibrated BET tree thresholds are correct. The problem is the
training data. Of 146 not-facing-bet situations:

- 138 are OOP (95%) — mostly BB/SB defenders
- 8 are IP — none are PFA
- 25 are PFA — all OOP
- villain_air_pct for PFA spots: clusters at 0.16 and 0.30 (never reaches 0.40)
- villain_aggression_count: always >= 1 for Step 6 candidates

The factory was designed for RAISE contexts (facing a bet). The BET
tree's core steps (3A IP PFA value, 4A-D PFA semi-bluff, 5 thin value
IP) need situations that don't exist in the current data.

## What the BET tree NEEDS that the data LACKS

| Tree step | Requires | Data has |
|-----------|----------|----------|
| 3A | IP PFA, made hand, high board | 0 IP PFA situations |
| 3B | OOP PFA, villain_air >= 0.40 | 0 PFA with air >= 0.40 |
| 4A-D | PFA, no made hand, draws | 6 candidates, all OOP + suppressed |
| 5 | IP, non-PFA, made hand | 0 IP with hand_category >= 7 |
| 6 | OOP, high equity, passive villain | 8 candidates, all villain_aggr >= 1 |

## Options

**A. Design additional BET-context factory situations (recommended)**
Add ~80-100 situations specifically for BET/CHECK decisions:
- 30+ IP PFA situations on varied boards (A/K/Q high, dry/wet)
- 20+ OOP PFA situations with passive villain profiles
- 20+ IP non-PFA thin value situations
- 10+ OOP value exception situations with villain_aggr == 0
This is a new factory batch (batch 4) requiring board allocation +
hero hand design. Estimated: 1-2 sessions.

**B. Accept current data, train without BET tree coverage**
The model trains on 563 situations with ~1.6% BET labels (all
monster protection). BET/CHECK decisions rely on the model's
general learning, not tree-guided labels. BET performance will be
weak but not blocking — the model can still learn CHECK vs BET
from the feature patterns. Defer proper BET training to v3.2.

**C. Use LLM agents for BET labels only**
Run the deterministic script for RAISE/CALL/FOLD (where it works).
Use LLM labelling agents for the 146 BET situations only (15 agents
at 10 each). The LLM agents apply poker judgment instead of the
tree, producing BET labels where the tree can't fire due to data
limitations. Risk: LLM bias, inconsistency.

## My recommendation: Option A

The owner invested a full research round (5 agents + 3 reviewers)
in c-bet research, and identified the PFA bluff scenario as a real
feature gap worth feature 53. Building factory data for BET contexts
completes the investment. Training without BET coverage wastes the
research and the feature.

Option A is ~80-100 new situations. The board allocation infrastructure
exists (we can reuse some batch 3 boards that have to_call=0 variants).
The BET tree is ready. The work is factory design, not research.

## Timeline impact

Option A adds 1-2 sessions before labelling. But labelling with
proper BET coverage produces a model that handles all 5 actions,
not just RAISE/CALL/FOLD + monster-BET.
