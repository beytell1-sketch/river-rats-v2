---
date: 2026-05-12
from: BUILDER
to: Main terminal (orchestrator) + Owner
re: Phase 2-E FULL BATCH-006 — 50/700 closing-action; 98% consensus; 0/250 illegal
status: BATCH-006 COMPLETE — 300/700 cumulative (42.9%)
---

# Phase 2-E FULL BATCH-006 builder report

## TL;DR

BATCH-006 (50 hands closing-action axis): **49/50 consensus (98%)** • **0/250 illegal votes** • 1 owner-arb (Opus diagnosed Sonnet miscount, not GTO ambiguity).

## Cumulative tally (300/700 = 42.9%)

| Batch | Axis | Consensus | Illegal | Owner-arb |
|-------|------|-----------|---------|-----------|
| 001 | 3-bet | 92% | 3 (pre-patch) | 4 |
| 002 | 3-bet | 98% | 0 | 1 |
| 003 | 3-bet + cooler | 98% | 0 | 1 |
| 004 | cooler | 98% | 0 | 1 |
| 005 | cooler + closing | 96% | 0 | 2 |
| 006 | closing-action | 98% | **0** | 1 |

**6 consecutive batches with 0 illegal votes post-patch.**

## Consensus
44 all-agree + 5 4-of-5 + 1 owner-arb = 49/50.

## Action distribution
CALL 19 / RAISE 11 / FOLD 8 / CHECK 8 / BET 3.

## Per-labeller summary

| Labeller | BET | CHECK | CALL | RAISE | FOLD | Illegal | HIGH | MED |
|----------|-----|-------|------|-------|------|---------|------|-----|
| FL1 | 3 | 8 | 19 | 11 | 9 | 0 | 48 | 2 |
| FL2 | 5 | 6 | 19 | 11 | 9 | 0 | 47 | 3 |
| FL3 | 3 | 8 | 18 | 12 | 9 | 0 | 47 | 3 |
| FL4 | 3 | 8 | 20 | 10 | 9 | 0 | 46 | 2 |
| FL5 | 3 | 8 | 20 | 11 | 8 | 0 | n/r | n/r |

## Opus tier-up (1 disputed)

| spot_id | Sonnet | Opus | Outcome |
|---------|--------|------|---------|
| 4WF-CLOSING--305 | FOLD ×3 / CALL ×2 | **CALL** HIGH | **Owner-arb**: Opus diagnosed Sonnet miscount (Ac9c+Jc=3 clubs=direct nut FD, not backdoor); 3/5 labellers mis-calculated equity. NOT GTO ambiguity — labeller arithmetic error. Owner-arb route allows orchestrator/owner to override to CALL consensus per Opus's diagnostic. |

## Solver-verify queue

23 (prior) + 0 (BATCH-006 305 is a labeller error not solver-uncertain) = **23 total**.

## STOP-conditions: all green
- Illegal: 0/250 ✓
- FL4-drift: 0 ✓
- Consensus collapse: 2% ✓
- Owner-arb rate: 2% ✓

## Notable
Spot 305 illustrates Opus's role beyond consensus arbitration: catches Sonnet arithmetic errors (miscounting clubs on flop). Brief discipline holding; Opus quality-control valuable beyond GTO-mix-point arbitration.

## Files
9 standard files. See standard BATCH report structure.

## What gates next
QC trigger → BATCH-007 (8 batches × 50 = 400 hands remaining).

## References
- Dispatch: PR #448 master `9a0bcba`
- BATCH-005: PR #445 + #447
