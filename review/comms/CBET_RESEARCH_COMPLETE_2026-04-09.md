---
date: 2026-04-09
from: Builder
re: C-bet research Phase B complete — ready for BET tree synthesis
---

## Research delivered (5 agents, 3 reviewers)

| Agent | Topic | File | Verdict |
|-------|-------|------|---------|
| R1 | Frequency | RESEARCH_CBET_R1_FREQUENCY.md | PASS |
| R2 | Texture | RESEARCH_CBET_R2_TEXTURE.md | PASS |
| R3 | Sizing/SPR | RESEARCH_CBET_R3_SIZING_SPR.md | PASS |
| R4 | Check-back | RESEARCH_CBET_R4_CHECKBACK.md | PASS |
| R5 | Blockers | RESEARCH_CBET_R5_BLOCKERS.md | PASS |

Reviews: REVIEW_CBET_R1_R2.md, REVIEW_CBET_R3_R4.md, REVIEW_CBET_R5_AND_CROSS.md

## Key findings for BET tree design

- PFA c-bets 43% 3-way (IP 38-45%, OOP 22-30%)
- Board texture is the primary gate: A/K-high dry 60-70%, low connected 20-30%
- Pure bluffs near-unprofitable 3-way (need 87% per-opponent fold rate)
- PFA checks 57% of flops — checking is the majority action
- Nut flush blocker adds 6-10pp combined fold equity
- Feature 53 (is_preflop_aggressor) is critical for the PFA bluff scenario
- Three feature gaps identified (backdoor draws, made-hand nut blocking, straight blockers) — defer to v3.2

## Must-reconcile before tree

1. KB Factor 2 ceiling language (30-45% is mean, not ceiling)
2. R2 texture tables: annotate IP PFA
3. R3/R4 MDF framing conflict
4. R4 unsourced check-fold rate

## Next: Phase C

GTO Expert synthesises all 5 research docs into a BET decision tree
(like RAISE_DECISION_TREE_V2.md but for BET/CHECK decisions when
not facing a bet). Must use feature 53. Independent review + owner
approval before labelling.
