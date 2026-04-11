---
date: 2026-04-09
from: Builder
re: BET-context factory batch 4 — plan
---

## Scope

~80-100 new situations designed for BET/CHECK decisions.
Uses the approved BET Decision Tree v1 (recalibrated) as the
design spec. Same process as the RAISE batch (batch 3).

## What the data needs (from the gap analysis)

| Category | Count | Tree step | Key features |
|----------|-------|-----------|-------------|
| IP PFA value c-bet | 30+ | 3A | is_pfa=1, is_ip=1, made hand, high boards |
| OOP PFA value c-bet | 15+ | 3B | is_pfa=1, is_ip=0, passive villain, dry board |
| PFA semi-bluff c-bet | 20+ | 4A-D | is_pfa=1, no made hand, draws/blockers |
| IP thin value (non-PFA) | 15+ | 5 | is_pfa=0, is_ip=1, capped villain |
| OOP value exception | 10+ | 6 | is_ip=0, high equity, passive, dry |
| CHECK counterexamples | 10+ | Default | Situations that LOOK like bets but CHECK |

## Key design constraints

All situations must have to_call = 0 (not facing a bet).
Action histories: preflop action → postflop checks to hero (or hero
acts first OOP). No villain bet before hero's action.

For PFA situations: hero_pos == opener_position (hero raised preflop).
For non-PFA: hero defended/called preflop.

Boards must cover the BET tree's texture tiers:
- Tier 1 (A/K-high dry): IP PFA value + semi-bluff
- Tier 2 (Q/J-high moderate): IP PFA TPGK+ value
- Tier 3 (connected): two-pair+ only
- Tier 4 (monotone/very connected): CHECK counterexamples

## Diversity requirements

Same R1-R7 framework as batch 3, adapted:
- Min 15 unique boards
- Max 8 situations per board
- SPR distribution across 4 tiers
- Position: 55-65% IP (correcting the 95% OOP bias in current data)
- PFA: 65-75% of situations (this is a PFA-focused batch)
- villain_aggression_count: must include 0 values (currently all >= 1)
- villain_air_pct: must span 0.10-0.55 (currently degenerate)

## Sequencing

1. Factory brief (this session or next)
2. Board allocation (reuse some batch 3 boards where to_call=0 variant works)
3. Hero hand design (2-3 design agents)
4. Generate through factory with 53 features
5. Combine all 4 batches → ~660 total situations
6. Dual labelling (deterministic + LLM) on all 660

## Phase transition

This is §0 — needs team decomposition before building. The factory
brief is a design task (1 GTO expert + 1 reviewer). Board allocation
is an architecture task. Hero hands need 2-3 design agents.
