---
date: 2026-05-12
from: BUILDER
to: Main terminal (orchestrator) + Owner
re: Phase 2-E FULL BATCH-007 — 50/700 (closing + asymmetry); 94% consensus; 0/250 illegal
status: BATCH-007 COMPLETE — 350/700 (50%) — halfway mark
---

# BATCH-007 builder report

## TL;DR
50 hands (30 closing-action + 20 range-asymmetry). **47/50 consensus (94%)** • **0/250 illegal** • 3 owner-arb (Opus dissents on 3 spots).

## Cumulative tally — **350/700 = 50%, halfway mark reached**

| Batch | Consensus | Illegal | Owner-arb |
|-------|-----------|---------|-----------|
| 001 | 92% | 3 (pre-patch) | 4 |
| 002 | 98% | 0 | 1 |
| 003 | 98% | 0 | 1 |
| 004 | 98% | 0 | 1 |
| 005 | 96% | 0 | 2 |
| 006 | 98% | 0 | 1 |
| 007 | 94% | 0 | 3 |

**7 consecutive batches with 0 illegal votes post-patch.**

## Consensus
36 all-agree + 9 4-of-5 + 2 3-2+opus-agree + 3 owner-arb = 47/50.

## Action distribution
RAISE 13 / CALL 14 / FOLD 8 / BET 7 / CHECK 5.

## Opus tier-up (5 disputed)

| spot_id | Sonnet | Opus | Outcome |
|---------|--------|------|---------|
| 312 | RAISE×3 / CALL×2 | **CALL** LOW | Owner-arb (Opus dissents; squeeze-pressure favors CALL over RAISE) |
| 323 | CALL×3 / RAISE×2 | **FOLD** LOW | Owner-arb (Opus aligns with neither faction; kicker-dominator over-realization) |
| 336 | CALL×3 / FOLD×2 | CALL MED | Consensus CALL (Opus agrees) |
| 348 | FOLD×3 / CALL×2 | FOLD LOW | Consensus FOLD (Opus agrees) |
| 352 | RAISE×3 / CALL×2 | **CALL** LOW | Owner-arb (Opus dissents; A-blocker keeps bluffs in) |

Notable: BATCH-007 has 3 spots where Opus dissents from Sonnet majority — uptick from prior batches (typically 0-1 dissents). All 5 disputed spots LOW/MEDIUM confidence, all 5 queued for solver-verify.

## Solver-verify queue
23 (prior) + 5 (BATCH-007) = **28 total**.

## STOP-conditions
All green:
- Illegal: 0/250 ✓
- FL4-drift: 0 ✓
- Consensus collapse: 6% ✓ (under 15% threshold)
- Owner-arb rate: 6% ✓ (under 25% threshold)

## Halfway milestone
350/700 hands labelled. Combined with pilot 50 + mini-pilot 10 = 410 spots in 4-way corpus. Final target 750.

## What gates next
QC trigger → BATCH-008 (7 batches × 50 = 350 hands remaining).

## References
- Dispatch: PR #452 master `703f04c`
- BATCH-006: PR #449 + #451
