---
date: 2026-05-30
from: Orchestrator (multi-viewpoint debate panel)
to: Owner (Rupert), QC, Builder
re: batch_009 PILOT 3 owner-arb spots — debate panel adjudication COMPLETE
status: ADJUDICATED + applied to consensus_v2
authorization: owner accepted panel verdicts ("yes please, make sure to use opus 4.8 on there difficult spots")
---

# batch_009 owner-arb adjudication via multi-viewpoint debate panel

## Architecture

3 independent reviewer subagents per spot, each with a distinct framework:
- **GTO Theoretician** — solver-aligned baseline, equity-realization math, pure GTO mixing logic, anti-exploit
- **Multiway Specialist** — per-villain range chains, MW equity realization, range-cap dynamics, sandwich position
- **Range-Construction Analyst** — hand's role in the range, blocker effects, frequency anchoring

Two-round debate protocol:
- Round 1: independent verdicts, no peer access
- Round 2: peer Round-1 outputs + 5 Sonnet labels + Opus tier-up label visible → revised verdict + critique

## Final verdicts

| Spot | Final | Sonnet majority | Opus tier-up | Panel call |
|---|---|---|---|---|
| 4WF-CHAIN-009-004 | **FOLD** | CALL (3-2) | FOLD | panel UNANIMOUS FOLD, aligns with Opus, rejects Sonnet majority |
| 4WF-CHAIN-009-016 | **FOLD** | FOLD (3-2) | CALL | panel 2-of-3 FOLD after board-correction; Opus CALL was WRONG (phantom NFD) |
| 4WF-RANGE-AS-457 | **CALL** | CALL (3-2) | RAISE | panel UNANIMOUS CALL HIGH, rejects Opus RAISE (inflated equity + CO-sandwich miss) |

## Key findings

### Opus tier-up was WRONG on 2 of 3 contested spots

- **CHAIN-009-016 (Jc7s5d2h, hero AsKs):** Opus tier-up CALL built on "NFD + As-blocker" reasoning. Verified board has only 1 spade (the 7s). Hero has BACKDOOR FD, not NFD. Without the NFD, hero has ~15-18% raw equity vs 39% pot odds → FOLD is structurally clear. Range-Construction R1 + GTO R2 + 2 of 5 Sonnet labellers + Opus tier-up all made the same board-reading error.
- **RANGE-AS-457 (QhJc9d, hero AdKd):** Opus tier-up RAISE built on ~48-52% equity claim + "raise folds CO's capped range." Panel found joint MP×CO continuing range puts AdKd at ~30-35% raw; CO has already called and CO's capped range densely hits QJ9. AdKo blockers are wrong-direction for raise (block folding hands AQ/AJ, don't block continuing cluster). Better raise candidates are KTs/T9s/JTs with made-equity.

### Sonnet labellers exhibited multiple board-reading errors

- CHAIN-004 CALL voters (labellers 1, 2, 3): false BDFD on rainbow board + false gutshot AJ on T64
- CHAIN-016 CALL voters (labellers 3, 5): phantom NFD on 1-spade board

These errors propagated into Opus tier-up reasoning where Opus repeated the board-misread.

## Implication for v9-4way pipeline

**Single-Opus tier-up is insufficient as final arbiter on contested spots.** The 67% Opus error rate on this 3-spot sample (n=3, small) is consistent with the architecture limitation: a single model arbitrating without peer-debate cannot self-catch board-reading errors when the error originates from the same model family.

**Standing rule going forward (owner-confirmed):**
- Multi-viewpoint debate panel becomes standard arbitration tier for contested (3-2 + Opus-disagree) spots in future batches
- Top-tier Opus on difficult debate-panel spots
- Replaces single-Opus tier-up as final arbiter for contested spots; Opus tier-up still runs as a panel input but is no longer the final word

## Files

- `data/4way_corpus/full_700/batch_009_consensus_v2.jsonl` — 3 spots updated, consensus_state="debate-panel-adjudicated"
- `data/4way_corpus/full_700/batch_009_owner_arb_queue_normalizer.jsonl` — emptied
- `data/4way_corpus/full_700/batch_009_debate_round1_*.json` — 9 Round-1 reviewer files
- `data/4way_corpus/full_700/batch_009_debate_round2_*.json` — 9 Round-2 reviewer files
- `scripts/apply_batch009_debate_adjudication.py` — applies the 3 labels

## Batch_009 PILOT status

| | |
|---|---|
| Total spots | 50 |
| Consensus (initial pipeline) | 47/50 |
| Owner-arb adjudicated via debate panel | 3/3 |
| **Total final-labelled** | **50/50** |
| Cumulative corpus | 400 + 50 = **450/700 = 64.3%** |

PILOT gate is now CLEARED. Owner can authorize batches 010-014.

## Next decisions for owner

1. **Batches 010-014 architecture choice** — same Option-A orchestrator-direct workflow, or build a CLI labeller harness, or pivot to Phase 2-F2 first
2. **PR #467 (5-way reference set design)** — owner-verification still pending since 2026-05-22
3. **Solver-verify queue** — ~38 owner-arbitrated spots accumulated, queue must drain before 1.5-D.4 retrain ships
