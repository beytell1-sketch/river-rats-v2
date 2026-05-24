---
date: 2026-05-25
from: Builder (via orchestrator autonomous loop, Option A direct dispatch)
to: Owner (Rupert), QC
re: Phase 2-F1 batch_009 PILOT — first batch with new positional_action_chain scenarios
status: SHIPPED — pending QC pre-merge audit
target_pr: river-rats-v2#473 (augmented from input-only to full pilot)
supersedes: original BLOCKED report (Steps 1-2 only)
---

# Builder Report — Phase 2-F1 batch_009 PILOT (FULL)

## Headline numbers

| | |
|---|---|
| Total spots | 50 |
| Consensus achieved | 48/50 (96%) |
| Owner-arb queue | 2 spots (Opus joined Sonnet minority on both) |
| FL5 illegal-action rate | 0/247 ✓ (9th consecutive batch sentinel) |
| FL7 sizing-field violations | 0/247 ✓ |
| Malformed (normalizer) | 0/247 ✓ |
| Cumulative corpus | 400 + 48 = 448/700 = 64.0% |

## File manifest

```
data/4way_corpus/full_700/batch_009_50hand.jsonl                                  (from PR #473 Steps 1-2)
data/4way_corpus/full_700/batch_009_raw_labels_labeller_{1..5}.jsonl              5 files / 247 records (deduped)
data/4way_corpus/full_700/batch_009_raw_labels_labeller_{1..5}_v2.jsonl           5 files (normalized)
data/4way_corpus/full_700/batch_009_raw_labels_opus_tierup.jsonl                  1 file / 18 records
data/4way_corpus/full_700/batch_009_raw_labels_opus_tierup_v2.jsonl               1 file (normalized)
data/4way_corpus/full_700/batch_009_consensus_v2.jsonl                            1 file / 50 records
data/4way_corpus/full_700/batch_009_normalizer_audit.jsonl                        1 file (18 no_op)
data/4way_corpus/full_700/batch_009_owner_arb_queue_normalizer.jsonl              1 file / 2 spots
```

## Consensus state breakdown

| State | Count |
|---|---|
| all-agree (5/5) | 30 |
| 3-2+opus-agree | 9 |
| 4-of-5 | 7 |
| 4-of-4-partial-coverage | 2 (chunk-slip but unanimous) |
| 3-2+opus-disagree | 2 (→ owner-arb) |

## Action distribution (consensus_v2 modal)

| Action | Count | % |
|---|---|---|
| CALL | 20 | 40% |
| FOLD | 15 | 30% |
| CHECK | 7 | 14% |
| BET | 3 | 6% |
| RAISE | 3 | 6% |

Compared to batches 001-008 aggregate (CALL 22% / FOLD 9% / BET 34% / CHECK 20% / RAISE 17%), batch_009 has **3× more FOLD and 5× less BET**. This reflects the new positional_action_chain scenarios — facing-raise + sandwich + multi-villain chains are more often defensive (FOLD/CALL) than aggressive (BET). EXPECTED OUTCOME of A1 quotas.

## Owner-arb queue (2 spots)

### 4WF-CHAIN-009-004
- Sonnet: 3 CALL / 2 FOLD
- Opus: FOLD (joins minority)
- Spot: 4-way SRP flop facing c-bet — genuinely close

### 4WF-RANGE-AS-452
- Sonnet: 3 CALL / 1 FOLD (L2 missed)
- Opus: FOLD (joins minority + 1 missing labeller)
- Spot: BTN AJ on Q83r 3-way with CO continuing — MEDIUM-confidence across labellers; Opus likely correct given squeeze pressure

## Quality gates

| Gate | Result |
|---|---|
| FL5 illegal-action sentinel | 0/247 PASS (9th consecutive batch) |
| FL7 sizing-field discipline | 0/247 PASS |
| Malformed-rejected rate | 0/247 PASS (≤15% threshold) |
| Consensus rate | 96% PASS (≥90% threshold) |
| Opus dissent rate | 11.1% (2/18 non-unanimous spots) |

## Anomalies for QC awareness

1. **3 spots with 4-vote coverage** (L2 missed 1, L5 missed 2 — chunk-boundary slips). 2 are unanimous 4/4 (consensus stands); 1 is in owner-arb. Orchestrator-dispatch coordination issue specific to Option-A direct dispatch, not labeller quality.

2. **Opus tier-up subagent latency**: 2+ hour queue wait, then 11 min compute. Loop HALTED then UN-HALTED. Documented in HALT_BATCH009_OPUS_TIERUP_STALLED_2026-05-25.md + PR #475 closing comment.

3. **Normalizer audit shows 18 no_op records**, no transitions. Labellers wrote v2 schema natively (no legacy `predicted_sizing_pct` references). A0.3 brief patch working as designed.

## Pilot ↔ batches 001-008 sentinel comparison

| Metric | 001-008 aggregate | 009 pilot | Verdict |
|---|---|---|---|
| Consensus rate | ~96% | 96% | flat ✓ |
| FL5 illegal | 0/2000 post-patch | 0/247 | flat ✓ |
| Malformed | 0.68% | 0.00% | improved |
| Owner-arb size | 23-28 | 2 | improved |
| Action mix | BET/CALL balanced | FOLD/CALL heavy | EXPECTED (new chain spots) |

## Next steps

1. Orchestrator dispatches QC pre-merge audit on augmented PR #473
2. On QC PASS: orchestrator HALTS per `feedback_pilot_first_for_long_jobs` — pilot result requires owner gate before batches 010-014
3. Owner adjudicates the 2 owner-arb spots
4. Owner decides: ship batch_009 to v9-4way training corpus, OR require revisions

## Operational notes

- Branch: `builder/phase2-f1-batch009-pilot-2026-05-24` (same as PR #473)
- All files appended via single commit "builder: A0.x batch_009 pipeline complete — full label set + consensus + owner-arb"
- Working tree restored on builder branch; orphan tmp.jsonl files left in place (can be cleaned in follow-up)
