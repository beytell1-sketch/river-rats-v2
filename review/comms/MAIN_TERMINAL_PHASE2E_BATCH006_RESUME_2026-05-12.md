---
date: 2026-05-12
from: Main terminal (orchestrator; standing-directive autonomous; quality default)
to: LEAD-PROGRAMMER (spawns 5 Sonnet labeller subagents + 1 Opus tier-up at 50-hand BATCH-006 scale)
re: Phase 2-E FULL BATCH-006 — continue FULL ~700-hand labelling pipeline with PATCHED brief on next 50 hands; per QC PASS on BATCH-005 (PR #445 + #447 merged at master 8b8ef41)
status: RESUME — fire BATCH-006 now (under existing FULL ~700-hand owner-authorization PR #424)
---

# Phase 2-E FULL BATCH-006 — resume directive

## Continuation

BATCH-005 cleared QC PASS at master `8b8ef41`. Running tally: 250/700 (35.7%); 4 consecutive batches at 0/250 illegal sentinel; consensus 92→98→98→98→96% (slight dip in BATCH-005 due to CALL-heavy composition; well above 85% target).

## What BATCH-006 builds

### Task 1 — Subset
Slice next 50 hands NOT in BATCH-001/002/003/004/005 + mini-pilot (260 excluded; 440 remaining). Persist `batch_006_50hand.jsonl`.

### Task 2 — 5 Sonnet + Opus tier-up
Same pipeline. Output: `batch_006_raw_labels_labeller_<N>.jsonl` + `batch_006_raw_labels_opus_tierup.jsonl` + `batch_006_consensus.jsonl` + `batch_006_owner_arb_queue.jsonl`.

### Task 3 — Regression-watch sentinel
**0 illegal action votes** — STOP if ≥1.

### Task 4 — BATCH-006 builder report with standing comparison vs BATCH-001/002/003/004/005.

## STOP-IMMEDIATELY conditions
Same as prior batches.

## What BATCH-006 does NOT do
Same exclusions.

## After PASS
QC trigger + merge → BATCH-007 resume. 8 batches remain after BATCH-006.

## Pre-push checks
HEAD vs `origin/master` MATCH `8b8ef41` ✓; 1 file; 1 commit.

## References
- BATCH-005 + QC PASS: master `8b8ef41` (PR #445 + #447)
- BATCH-004 + QC PASS: PR #441 + #443
- BATCH-003 + QC PASS: PR #437 + #439
- BATCH-002 + QC PASS: PR #433 + #435
- BATCH-001 + QC PASS: PR #425 + #427
- Mini-pilot brief patch: PR #429 + #431
- FULL-scope: PR #424
- Brief (PATCHED): `data/4way_labeller_brief.md`
- 700-hand subset: `data/4way_lookalikes_700hand_full_2026-05-12.jsonl`
- Non-overlap: BATCH-001..005 + mini-pilot

**Status: Phase 2-E FULL BATCH-006 resume. Builder slices next 50 hands, 5 Sonnet + Opus with PATCHED brief, regression-watch sentinel. After QC PASS → BATCH-007 resume. 9 batches remain (BATCH-006..014).**
