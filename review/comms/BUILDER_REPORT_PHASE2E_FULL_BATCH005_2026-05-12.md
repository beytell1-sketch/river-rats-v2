---
date: 2026-05-12
from: BUILDER
to: Main terminal (orchestrator) + Owner
re: Phase 2-E FULL BATCH-005 — 50/700 (cooler + closing-action mix); 96% consensus; 0/250 illegal
status: BATCH-005 COMPLETE — 250/700 cumulative (35.7%)
---

# Phase 2-E FULL BATCH-005 builder report

## TL;DR

BATCH-005 (50 hands; 7 cooler + 43 closing-action): **48/50 consensus (96%)** • **0/250 illegal votes** • 2 owner-arb.

## Cumulative tally (250/700 = 35.7%)

| Batch | Axis | Consensus | Illegal | Owner-arb |
|-------|------|-----------|---------|-----------|
| 001 | 3-bet | 92% | 3 (pre-patch) | 4 |
| 002 | 3-bet | 98% | 0 | 1 |
| 003 | 3-bet + cooler | 98% | 0 | 1 |
| 004 | cooler | 98% | 0 | 1 |
| 005 | cooler + closing | 96% | **0** | 2 |

**5 consecutive batches with 0 illegal votes post-patch.**

## Consensus
38 all-agree + 7 4-of-5 + 3 3-2+opus-agree + 2 owner-arb = 48/50.

## Action distribution
CALL 21 / RAISE 12 / BET 7 / CHECK 5 / FOLD 3. CALL-heavier than prior batches (closing-action axis facing-bet decisions skew CALL/RAISE).

## Per-labeller summary

| Labeller | BET | CHECK | CALL | RAISE | FOLD | Illegal | HIGH | MED |
|----------|-----|-------|------|-------|------|---------|------|-----|
| FL1 | 8 | 5 | 21 | 13 | 3 | 0 | n/r | 0 |
| FL2 | 7 | 6 | 23 | 12 | 2 | 0 | 46 | 4 |
| FL3 | 8 | 5 | 19 | 14 | 4 | 0 | 48 | 2 |
| FL4 | 8 | 5 | 21 | 12 | 4 | 0 | 42 | 7 |
| FL5 | 7 | 6 | 28 | 5 | 4 | 0 | n/r | n/r |

## Opus tier-up (5 disputed)

| spot_id | Sonnet | Opus | Outcome |
|---------|--------|------|---------|
| 214 | CALL ×3 | CALL LOW | Consensus CALL |
| 216 | CALL ×3 / RAISE ×2 | CALL LOW | Consensus CALL |
| 240 | FOLD ×3 / CALL ×2 | FOLD LOW | Consensus FOLD |
| 249 | FOLD ×3 / CALL ×2 | **CALL** LOW | **Owner-arb** (60/40 mix; closing-position implicit equity) |
| 209 | BET ×3 / CHECK ×2 | **CHECK** LOW | **Owner-arb** (capped MP donk dominated on 876dd) |

## Solver-verify queue
18 (prior) + 5 (all BATCH-005 disputed spots LOW conf) = **23 total**.

## STOP-conditions: all green
- Illegal: 0/250 ✓
- FL4-drift: 0 ✓
- Consensus collapse: 4% ✓
- Owner-arb rate: 4% ✓

## Files
batch_005_50hand + 5×raw_labels + opus_tierup + consensus + owner_arb_queue + this report (9 files).

## What gates next
QC trigger → BATCH-006 (9 batches × 50 = 450 hands remaining).

## References
- Dispatch: PR #444 master `c7aa372`
- BATCH-004: PR #441 + #443
