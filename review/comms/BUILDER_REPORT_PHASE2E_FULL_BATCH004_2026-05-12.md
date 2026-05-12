---
date: 2026-05-12
from: BUILDER
to: Main terminal (orchestrator) + Owner
re: Phase 2-E FULL BATCH-004 — 50/700 (multiway-cooler axis); 98% consensus; 0/250 illegal votes
status: BATCH-004 COMPLETE — gate sentinels green; 200/700 labelled total
---

# Phase 2-E FULL BATCH-004 builder report

## TL;DR

Per dispatch PR #440. BATCH-004 (all 50 hands multiway-cooler axis) labelled. **49/50 consensus (98%)** • **0/250 illegal votes** • 1 owner-arb.

## Cumulative tally (200/700 = 28.6% complete)

| Batch | Axis | Consensus | Illegal | Owner-arb |
|-------|------|-----------|---------|-----------|
| 001 | 4-way-3-bet | 92% | 3 (pre-patch) | 4 |
| 002 | 4-way-3-bet | 98% | 0/250 | 1 |
| 003 | 3-bet + cooler | 98% | 0/250 | 1 |
| 004 | multiway-cooler | 98% | **0/250** | 1 |

Brief patch sentinel: 4 consecutive batches with 0 illegal post-patch.

## Consensus
- 34 all-agree + 12 4-of-5 + 3 3-2+opus-agree + 1 owner-arb = 49/50

## Action distribution (4-way-cooler axis-natural)
BET 19 / CHECK 13 / RAISE 13 / CALL 4 / FOLD 0 — RAISE-heavier than 3-bet pot axis (cooler spots are nut-vs-nut where RAISE for value/protection is common).

## Per-labeller summary

| Labeller | BET | CHECK | RAISE | CALL | FOLD | Illegal | HIGH | MED |
|----------|-----|-------|-------|------|------|---------|------|-----|
| FL1 | 19 | 13 | 13 | 5 | 0 | 0 | 48 | 2 |
| FL2 | 19 | 13 | 15 | 2 | 1 | 0 | 48 | 2 |
| FL3 | 19 | 13 | 11 | 5 | 2 | 0 | 44 | 6 |
| FL4 | 18 | 14 | 5 | 11 | 2 | 0 | 48 | 2 |
| FL5 | 19 | 13 | 10 | 8 | 0 | 0 | 44 | 6 |

**Notable**: L2 self-corrected 2 mid-run conflicts (facing_bet=0 / RAISE → rewrote as legal CHECK/BET). Brief discipline holding under labeller self-validation.

## Opus tier-up (4 disputed)

| spot_id | Sonnet | Opus | Outcome |
|---------|--------|------|---------|
| 162 | CALL ×3 / FOLD ×2 | CALL LOW | Consensus CALL (TPTK + nut-flush blocker on monotone turn; 25% sizing) |
| 171 | RAISE ×3 / CALL ×2 | RAISE 10bb MED | Consensus RAISE (nut straight + 2nd-nut FD on flop) |
| 177 | FOLD ×3 / CALL ×2 | **CALL** LOW | **Owner-arb**: Opus dissents FOLD majority; identical equity structure to 162 (sibling variant); Opus argues consistency requires CALL on both |
| 179 | RAISE ×3 / CALL ×2 | RAISE 10bb MED | Consensus RAISE (nut straight + nut FD on flop) |

## Owner-arb queue (1 spot)

**4WF-MULTIWAY-177**: monotone turn TPTK with nut-flush blocker. Opus flags inconsistency — sibling spot 162 reached CALL consensus on identical equity structure; 177 reached FOLD majority but Opus argues 162+177 should land same action under solver-aligned label discipline. Both flagged for joint solver verification.

## Solver-verify queue update
14 (prior) + 4 (BATCH-004: 162, 171, 177, 179) = **18 total**.

## Anti-rule attestation
All 250 Sonnet + 4 Opus labels verified clean. L2's mid-run self-correction is evidence of brief discipline working at the labeller-level (not just at consensus).

## STOP-conditions: all green
- Illegal votes: 0 ✓
- FL4-drift: 0 ✓
- Consensus collapse: 2% ✓
- Owner-arb rate: 2% ✓

## Files in this PR

- `data/4way_corpus/full_700/batch_004_50hand.jsonl`
- `data/4way_corpus/full_700/batch_004_raw_labels_labeller_{1..5}.jsonl`
- `data/4way_corpus/full_700/batch_004_raw_labels_opus_tierup.jsonl`
- `data/4way_corpus/full_700/batch_004_consensus.jsonl`
- `data/4way_corpus/full_700/batch_004_owner_arb_queue.jsonl`
- `review/comms/BUILDER_REPORT_PHASE2E_FULL_BATCH004_2026-05-12.md`

## What gates next
- QC trigger → on PASS → BATCH-005 (10 batches × 50 = 500 hands remaining)

## References
- Dispatch: PR #440 master `74cf18b`
- BATCH-003: PR #437 + #439
- Memory: same as prior batches
