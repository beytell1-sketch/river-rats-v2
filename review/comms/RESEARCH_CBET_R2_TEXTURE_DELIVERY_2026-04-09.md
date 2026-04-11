# Research Delivery: C-Bet Texture Effects (Round 2)

**Date:** 2026-04-09
**From:** GTO Research Agent (board texture topic)
**To:** Reviewer / parent agent

## Delivery confirmation

Research file written to:
`review/RESEARCH_CBET_R2_TEXTURE.md`

## What is in the file

Full research on how board texture affects PFA c-bet frequency in 3-way pots.
18 sources cited (8 GTO Wizard solver-based, 4 Upswing solver-informed, 2 poker.pro
solver-based, Phil Galfond solver-based, SplitSuit solver-informed, Cardquant
solver-informed, 888poker theoretical, MyPokerCoaching theoretical/solver-informed).

Covers all 7 research questions:
1. Which textures have highest c-bet frequency — answered (A-high dry 60-70%, paired
   boards 55-65%, K-high dry 50-60%)
2. Which textures suppress c-betting — answered (low connected 20-30%, monotone 20-30%,
   mid connected 30-40%)
3. Flush danger effect — answered (two-tone: -5 to -10pp; monotone: -15 to -25pp)
4. Straight danger / connectivity effect — answered (gradient table provided)
5. Paired boards — answered (higher than non-paired; PFA overpairs dominate)
6. High card vs low card — answered (~20-30pp frequency difference)
7. Texture x hand class interaction — answered for air, draws, top pair, two-pair/sets

## Key new content vs existing KB

The existing KB (three_way_gto.md Section 4, 3way_ranges_boards_research.md Section 4-6)
covers board texture directionally but does not provide:
- Tiered frequency estimates by specific texture type
- A structured 4-tier c-bet decision tree by texture
- Flush danger quantified as a frequency delta
- Straight danger gradient table
- Hand class x texture interaction matrix
- Contradictions/gaps documented

## Status

COMPLETE. Ready for reviewer to read and approve before KB integration.
