---
date: 2026-05-12
from: Main terminal (orchestrator; standing-directive autonomous; quality default)
to: LEAD-PROGRAMMER (spawns 5 Sonnet labeller subagents + 1 Opus tier-up at 50-hand BATCH-004 scale)
re: Phase 2-E FULL BATCH-004 — continue FULL ~700-hand labelling pipeline with PATCHED brief on next 50 hands; per QC PASS on BATCH-003 (PR #437 + #439 merged at master ee85bce)
status: RESUME — fire BATCH-004 now (under existing FULL ~700-hand owner-authorization PR #424)
---

# Phase 2-E FULL BATCH-004 — resume directive

## Continuation

BATCH-003 cleared QC PASS at master `ee85bce`. Running tally: 150/700 (21.4% complete); 2 consecutive batches at 0/250 illegal sentinel; consensus stable at 98%. Resume BATCH-004.

## What BATCH-004 builds

### Task 1 — Select BATCH-004 50-hand subset

From `data/4way_lookalikes_700hand_full_2026-05-12.jsonl`:
- Slice next 50 hands NOT in:
  - `data/4way_corpus/full_700/batch_001_50hand.jsonl` (50)
  - `data/4way_corpus/full_700/batch_002_50hand.jsonl` (50)
  - `data/4way_corpus/full_700/batch_003_50hand.jsonl` (50)
  - `data/4way_corpus/mini_pilot_2e01/mini_pilot_10hand_2026-05-12.jsonl` (10)
- 700 − 160 = 540 remaining; pick first 50
- Persist as `data/4way_corpus/full_700/batch_004_50hand.jsonl`

### Task 2 — 5 Sonnet labellers + Opus tier-up
Same pipeline. PATCHED brief frozen at `data/4way_labeller_brief.md`. Output: `batch_004_raw_labels_labeller_<N>.jsonl` + `batch_004_raw_labels_opus_tierup.jsonl` + `batch_004_consensus.jsonl` + `batch_004_owner_arb_queue.jsonl`.

### Task 3 — Regression-watch sentinel
**0 illegal action votes** across 5 Sonnet labellers — STOP IMMEDIATELY if ≥1.

### Task 4 — BATCH-004 builder report
`review/comms/BUILDER_REPORT_PHASE2E_FULL_BATCH004_2026-05-12.md` with standing comparison vs BATCH-001/002/003.

## STOP-IMMEDIATELY conditions
- ≥1 illegal vote → STOP
- FL4-style labels → STOP
- Consensus collapse >15% → STOP
- Owner-arb rate >25% → STOP
- Wall-clock >3h → REPORT
- TC-23 EXISTENCE: all output git-tracked

## What BATCH-004 does NOT do
- ❌ river-rats-core/, brief, calibration, prior batches/pilot/mini-pilot/ref/subset
- ❌ Models, retrain, production swap
- ❌ Drain solver-verify queue (62 HOLD)

## After PASS
Builder pushes → QC trigger + merge → BATCH-005 resume. 10 batches remain after BATCH-004.

## Pre-push checks
- HEAD vs `origin/master` MATCH `ee85bce` ✓
- 1 file; 1 commit

## References
- BATCH-003 + QC PASS: master `ee85bce` (PR #437 + #439)
- BATCH-002 + QC PASS: PR #433 + #435
- BATCH-001 + QC PASS: PR #425 + #427
- Mini-pilot brief patch: PR #429 + #431
- FULL-scope: PR #424
- Brief (PATCHED): `data/4way_labeller_brief.md`
- 700-hand subset: `data/4way_lookalikes_700hand_full_2026-05-12.jsonl`
- Non-overlap targets: `batch_001_50hand.jsonl`, `batch_002_50hand.jsonl`, `batch_003_50hand.jsonl`, `mini_pilot_10hand_2026-05-12.jsonl`

**Status: Phase 2-E FULL BATCH-004 resume. Builder slices next 50 hands, 5 Sonnet + Opus tier-up with PATCHED brief, regression-watch sentinel. After QC PASS → BATCH-005 resume. 11 batches remain (BATCH-004..014).**
