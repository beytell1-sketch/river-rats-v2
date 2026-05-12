---
date: 2026-05-12
from: Main terminal (orchestrator; standing-directive autonomous; quality default)
to: LEAD-PROGRAMMER
re: Phase 2-E FULL BATCH-007 — resume per QC PASS on BATCH-006 (PR #449 + #451 merged at master 9b77cb2)
status: RESUME — fire BATCH-007 now (under existing FULL ~700 owner-authorization PR #424)
---

# Phase 2-E FULL BATCH-007 — resume directive

## Continuation

BATCH-006 cleared QC PASS at master `9b77cb2`. Running tally: 300/700 (42.9%); 5 consecutive batches at 0/250 illegal sentinel (6 if mini-pilot counted); consensus stable 92→98→98→98→96→98%. Notable QC finding (PR #451): Opus tier-up caught Sonnet combinatorial miscount on spot 305 — demonstrates Opus mathematical-verification value beyond consensus-tie-breaking.

## What BATCH-007 builds

### Task 1 — Subset
Slice next 50 hands NOT in BATCH-001..006 + mini-pilot (310 excluded; 390 remaining). Persist `batch_007_50hand.jsonl`.

### Task 2 — 5 Sonnet + Opus tier-up
Same pipeline. Outputs: `batch_007_raw_labels_labeller_<N>.jsonl` + `batch_007_raw_labels_opus_tierup.jsonl` + `batch_007_consensus.jsonl` + `batch_007_owner_arb_queue.jsonl`.

### Task 3 — Regression-watch sentinel
**0 illegal action votes** — STOP if ≥1.

### Task 4 — BATCH-007 builder report with standing comparison vs BATCH-001..006.

## STOP-IMMEDIATELY conditions
Same as prior batches.

## After PASS
QC trigger + merge → BATCH-008 resume. 7 batches remain after BATCH-007.

## Pre-push checks
HEAD vs `origin/master` MATCH `9b77cb2` ✓; 1 file; 1 commit.

## References
- BATCH-006 + QC PASS: master `9b77cb2` (PR #449 + #451)
- BATCH-005 + QC PASS: PR #445 + #447
- BATCH-004 + QC PASS: PR #441 + #443
- BATCH-003 + QC PASS: PR #437 + #439
- BATCH-002 + QC PASS: PR #433 + #435
- BATCH-001 + QC PASS: PR #425 + #427
- Mini-pilot brief patch: PR #429 + #431
- FULL-scope: PR #424
- Brief (PATCHED): `data/4way_labeller_brief.md`

**Status: Phase 2-E FULL BATCH-007 resume. Builder slices next 50 hands, 5 Sonnet + Opus with PATCHED brief, regression-watch sentinel. After QC PASS → BATCH-008 resume. 8 batches remain (BATCH-007..014).**
