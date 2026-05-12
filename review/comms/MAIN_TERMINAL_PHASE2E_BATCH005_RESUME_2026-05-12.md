---
date: 2026-05-12
from: Main terminal (orchestrator; standing-directive autonomous; quality default)
to: LEAD-PROGRAMMER (spawns 5 Sonnet labeller subagents + 1 Opus tier-up at 50-hand BATCH-005 scale)
re: Phase 2-E FULL BATCH-005 — continue FULL ~700-hand labelling pipeline with PATCHED brief on next 50 hands; per QC PASS on BATCH-004 (PR #441 + #443 merged at master 7d6fdaf)
status: RESUME — fire BATCH-005 now (under existing FULL ~700-hand owner-authorization PR #424)
---

# Phase 2-E FULL BATCH-005 — resume directive

## Continuation

BATCH-004 cleared QC PASS at master `7d6fdaf`. Running tally: 200/700 (28.6%); 3 consecutive batches at 0/250 illegal sentinel; consensus stable at 98%.

## What BATCH-005 builds

### Task 1 — Subset
Slice next 50 hands NOT in BATCH-001/002/003/004 + mini-pilot (210 excluded; 490 remaining). Persist `batch_005_50hand.jsonl`.

### Task 2 — 5 Sonnet + Opus tier-up
Same pipeline. Output: `batch_005_raw_labels_labeller_<N>.jsonl` + `batch_005_raw_labels_opus_tierup.jsonl` + `batch_005_consensus.jsonl` + `batch_005_owner_arb_queue.jsonl`.

### Task 3 — Regression-watch sentinel
**0 illegal action votes** — STOP if ≥1.

### Task 4 — BATCH-005 builder report with standing comparison vs BATCH-001/002/003/004.

## STOP-IMMEDIATELY conditions
Same as prior batches (≥1 illegal / FL4 / consensus collapse >15% / arb rate >25% / wall-clock >3h / TC-23).

## What BATCH-005 does NOT do
Same exclusions (no source / brief / calibration / prior batches / models / queue drain).

## After PASS
QC trigger + merge → BATCH-006 resume. 9 batches remain after BATCH-005.

## Pre-push checks
HEAD vs `origin/master` MATCH `7d6fdaf` ✓; 1 file; 1 commit.

## References
- BATCH-004 + QC PASS: master `7d6fdaf` (PR #441 + #443)
- BATCH-003 + QC PASS: PR #437 + #439
- BATCH-002 + QC PASS: PR #433 + #435
- BATCH-001 + QC PASS: PR #425 + #427
- Mini-pilot brief patch: PR #429 + #431
- FULL-scope: PR #424
- Brief (PATCHED): `data/4way_labeller_brief.md`
- 700-hand subset: `data/4way_lookalikes_700hand_full_2026-05-12.jsonl`
- Non-overlap: `batch_001_50hand.jsonl`, `batch_002_50hand.jsonl`, `batch_003_50hand.jsonl`, `batch_004_50hand.jsonl`, `mini_pilot_10hand_2026-05-12.jsonl`

**Status: Phase 2-E FULL BATCH-005 resume. Builder slices next 50 hands, 5 Sonnet + Opus with PATCHED brief, regression-watch sentinel. After QC PASS → BATCH-006 resume. 10 batches remain (BATCH-005..014).**
