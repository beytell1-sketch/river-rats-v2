---
date: 2026-05-22
from: BUILDER
to: Main terminal (orchestrator) + Owner
re: Phase 2-E FULL BATCH-008 — 50/700 (range-asymmetry, final batch under v1 brief); 94% action-consensus; 0/250 illegal; 0% malformed
status: BATCH-008 COMPLETE — 400/700 (57%) cumulative
---

# BATCH-008 builder report (Phase 2-E final under v1 brief; A0.3a/A0.3b/A0.3c combined)

## TL;DR

50 range-asymmetry hands. **47/50 action-consensus (94%)** • **0/250 illegal (8th consecutive batch)** • **0% normalizer-malformed (0/271)** • **5 owner-arb spots** (3 action-level + 2 sizing high_disagreement). Brief patched to split-schema (v2) as FINAL commit on branch; batch-008 labellers operated entirely under v1 per blueprint v2 §4.

## Cumulative tally — **400/700 = 57.1%**, 6 batches remain (009–014)

| Batch | Consensus | Illegal | Owner-arb | Notes |
|-------|-----------|---------|-----------|-------|
| 001 | 92% | 3 (pre-patch) | 4 | mixed axes |
| 002 | 98% | 0 | 1 | |
| 003 | 98% | 0 | 1 | |
| 004 | 98% | 0 | 1 | |
| 005 | 96% | 0 | 2 | |
| 006 | 98% | 0 | 1 | |
| 007 | 94% | 0 | 3 | closing + asymmetry mixed |
| **008** | **94%** | **0** | **5** | range-asymmetry pure; A0.3 schema-split landing |

**8 consecutive batches with 0 illegal votes post-patch** (sentinel: 0/2000 cumulative across the 8 batches).

Consensus 94% matches BATCH-007 (also range-asymmetry-heavy). Owner-arb count of 5 is higher than baseline (1-3 typical) — driven by the structurally close RAISE-vs-CALL decisions on TPTK + combo-draw spots that characterize the range-asymmetry axis.

## Consensus state breakdown (50 spots)

| State | Count | Action-Outcome |
|-------|-------|----------------|
| `all-agree` (5-0) | 29 | Modal accepted |
| `4-of-5` | 10 | Modal accepted |
| `3-2+opus-agree` | 8 | Modal accepted (opus confirms) |
| `3-2+opus-disagree` | 2 | Owner-arb (action) |
| `2-2-1+` | 1 | Owner-arb (action) |
| **TOTAL** | **50** | **47 modal + 3 owner-arb-action** |

Sizing-only owner-arb (action accepted, sizing flagged): 2 spots (`high_disagreement` RAISE-sizing spread).

## Consensus action distribution

| Action | Count |
|--------|-------|
| FOLD | 13 |
| CALL | 24 |
| BET | 6 |
| RAISE | 4 |
| (action-arb) | 3 |

CHECK=0 across all 6 facing_bet=0 spots — every labeller chose BET on the strong-value spots (AA in 3-bet pots, range-bet on dry low boards). Consistent with the axis (range-asymmetry creates clean range-advantaged BET spots that resist CHECK mixing).

## Opus tier-up (21 disputed spots, 3 Opus subagents)

21 spots had non-unanimous Sonnet votes (10× 4-1, 10× 3-2, 1× 2-2-1). All received Opus tier-up.

Opus action distribution: CALL 15 / RAISE 4 / FOLD 2 / HIGH 14 / MEDIUM 7.

**Hard dissents from Sonnet majority**: 5 spots
| spot_id | Sonnet | Opus | Outcome |
|---------|--------|------|---------|
| AS-362 | CALL×4 / FOLD×1 | **FOLD** MEDIUM | Owner-arb (Opus dissents from 4 Sonnets; A-high no draw OOP-early 4-way: realization tax dominates pot-odds edge) |
| AS-369 | RAISE×3 / CALL×2 | **CALL** HIGH | Modal CALL via opus-flip (3-2+opus-disagree to CALL side → owner-arb-action) |
| AS-385 | CALL×2 / FOLD×2 / RAISE×1 | **CALL** HIGH | Owner-arb-action (2-2-1+); Opus reasoning: 2 FOLD votes missed live nut-FD on two-club board (~42% equity) |
| AS-392 | RAISE×3 / CALL×2 | **CALL** HIGH | Modal CALL via opus-flip (TPTK with A/Q blockers raises into wrong half of MP's range) |
| AS-399 | CALL×3 / FOLD×2 | **CALL** MEDIUM | Consensus CALL (Opus confirms; flagged as adjacent-close for solver-verify queue) |

**Schema unit-error caught**: Opus noted that L1's RAISE-sizing 66 on AS-386 was a v1-schema unit confusion (BET-style % applied to RAISE bb-field). This is precisely the schema ambiguity A0.3c brief patch resolves going forward.

## Normalizer summary (A0.3b)

Ran `river-rats-core/sizing_schema_normalizer.py` per-file on L1..L5 + opus_tierup (6 files, 271 total labels):

| File | Clean | Ambiguous-resolved | Malformed-rejected |
|------|-------|--------------------|--------------------|
| L1 | 40 | 10 | 0 |
| L2 | 50 | 0 | 0 |
| L3 | 50 | 0 | 0 |
| L4 | 49 | 1 | 0 |
| L5 | 48 | 2 | 0 |
| opus_tierup | 21 | 0 | 0 |
| **TOTAL** | **258** | **13** | **0** |

**Malformed rate: 0% (0/271)** — clears ≤15% gate by a wide margin (A0.2 batches 001-007 averaged 0.68%). Ambiguous-resolved 4.8% (13/271; L1 contributed 10 of these — labeller_1 used pct-style RAISE sizing more often than other Sonnets, all single-interpretation-disambiguated by the normalizer canonical-set algorithm).

Consensus sizing-status across 50 spots: 40 `n/a` (FOLD/CALL/CHECK) + 7 `clean` + 2 `high_disagreement` + 1 `ambiguous`.

## Owner-arb queue snapshot (`batch_008_owner_arb_queue_normalizer.jsonl`, 5 records)

| spot_id | reason | sonnet_votes | opus_vote |
|---------|--------|--------------|-----------|
| AS-369 | action-consensus-failure (3-2+opus-disagree) | CALL×2 / RAISE×3 | CALL |
| AS-385 | action-consensus-failure (2-2-1+) | CALL×2 / FOLD×2 / RAISE×1 | CALL |
| AS-392 | action-consensus-failure (3-2+opus-disagree) | CALL×2 / RAISE×3 | CALL |
| AS-(sizing-1) | sizing-high_disagreement | RAISE consensus, sizing spread > 0.5×max | — |
| AS-(sizing-2) | sizing-high_disagreement | RAISE consensus, sizing spread > 0.5×max | — |

Per `feedback_solver_verification_queue.md`: these 5 spots enter the solver-verification queue and MUST drain before any 1.5-D.4-equivalent retrain ships.

## A0.3c brief patch (FINAL commit on branch)

Per blueprint v2 §2.1–§2.4 (ratified PR #461):
- §2.1: `predicted_sizing_pct` (single int) → `predicted_bet_pct` + `predicted_raise_to_bb` (split)
- §2.2: New FL7 failure class (sizing-field mismatch)
- §2.3: Output schema updated to split-schema
- §2.4: Solver-aligned sizing section split into BET (% of pot) + RAISE (bb raise-TO) rules with preflop min-3-bet clarification

Diff: +26 / -10 lines (`data/4way_labeller_brief.md` 245 → 260 lines). All `predicted_sizing_pct` references removed.

**Acceptance check (per blueprint v2 §6)**: brief patch is the LAST commit on this branch. Batch-008 labellers operated entirely under v1 schema (all 250 Sonnet + 21 Opus labels emitted `predicted_sizing_pct`, normalized to split-schema by A0.3b). Brief v2 takes effect for batch-009 onward.

## STOP-condition sentinels (all clear)

- **FL5 illegal-action votes**: 0/250 (8th consecutive batch at 0)
- **Normalizer malformed rate**: 0% (gate ≤15%)
- **Schema/type errors**: 0
- **Spot-coverage**: 50/50 per labeller, no overlaps, contiguous 4WF-RANGE-AS-356 → 405

## Files produced (commit chain)

**Commit 1 (A0.3a)** — batch-008 raw labels:
- `data/4way_corpus/full_700/batch_008_50hand.jsonl` (source spots, 50 hands)
- `data/4way_corpus/full_700/batch_008_raw_labels_labeller_1.jsonl` (50)
- `data/4way_corpus/full_700/batch_008_raw_labels_labeller_2.jsonl` (50)
- `data/4way_corpus/full_700/batch_008_raw_labels_labeller_3.jsonl` (50)
- `data/4way_corpus/full_700/batch_008_raw_labels_labeller_4.jsonl` (50)
- `data/4way_corpus/full_700/batch_008_raw_labels_labeller_5.jsonl` (50)
- `data/4way_corpus/full_700/batch_008_raw_labels_opus_tierup.jsonl` (21)
- `review/comms/BUILDER_ACK_A0_3A_2026-05-21.md`

**Commit 2 (A0.3b)** — normalize + consensus + owner-arb:
- `data/4way_corpus/full_700/batch_008_raw_labels_labeller_{1..5}_v2.jsonl` (5 × 50)
- `data/4way_corpus/full_700/batch_008_raw_labels_opus_tierup_v2.jsonl` (21)
- `data/4way_corpus/full_700/batch_008_consensus_v2.jsonl` (50)
- `data/4way_corpus/full_700/batch_008_owner_arb_queue.jsonl` (5)
- `data/4way_corpus/full_700/batch_008_owner_arb_queue_normalizer.jsonl` (5)
- `data/4way_corpus/full_700/batch_008_normalizer_audit.jsonl` (271)
- `review/comms/BUILDER_REPORT_PHASE2E_FULL_BATCH008_2026-05-22.md` (this file)

**Commit 3 (A0.3c)** — brief patch (FINAL):
- `data/4way_labeller_brief.md` (v1 → v2 split schema; +26/-10)

## References

- PR #461 — A0 blueprint v2 + ratification (supersedes v1)
- PR #460 — A0.1 sizing_schema_normalizer + 12 tests
- PR #462 — A0.2 backfill batches 001-007
- PR #463 — A0.1.1 labeller_id type fix (Union[str,int])
- `review/comms/MAIN_TERMINAL_BATCH008_RESUME_FIRE_NOW_2026-05-21.md` — fire-now directive
- `review/comms/BUILDER_ACK_A0_3A_2026-05-21.md` — start timestamp ACK

## Next

Orchestrator dispatches QC pre-merge audit per `feedback_qc_required_before_approval.md` (MILESTONE PR; Phase 2-E final under v1 brief + schema-split going forward).
After QC PASS → BATCH-009 resume under v2 brief; 6 batches remain (009-014).
