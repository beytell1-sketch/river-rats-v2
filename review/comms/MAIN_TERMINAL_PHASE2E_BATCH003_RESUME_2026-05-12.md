---
date: 2026-05-12
from: Main terminal (orchestrator; standing-directive autonomous; quality default)
to: LEAD-PROGRAMMER (spawns 5 Sonnet labeller subagents + 1 Opus tier-up subagent at 50-hand BATCH-003 scale)
re: Phase 2-E FULL BATCH-003 — continue FULL ~700-hand labelling pipeline with PATCHED brief on next 50 hands; per QC PASS on BATCH-002 (PR #433 + #435 merged at master 745fb43)
status: RESUME — fire BATCH-003 now (under existing FULL ~700-hand owner-authorization PR #424; orchestrator-decided HOW)
---

# Phase 2-E FULL BATCH-003 — resume directive

## Continuation of BATCH-001 → BATCH-002 → BATCH-003

Owner-authorized FULL ~700 scope (PR #424). Brief PATCHED + validated (PR #429+#431). BATCH-002 cleared QC PASS (PR #433+#435) at master `745fb43` with bit-exact regression-watch hold: 0/250 illegal votes; 98% consensus; 1 substantive arb. Resume BATCH-003 per established pattern.

## What BATCH-003 builds

Mirror of BATCH-002 dispatch with the next 50 hands.

### Task 1 — Select BATCH-003 50-hand subset

From `data/4way_lookalikes_700hand_full_2026-05-12.jsonl`:
- Slice the next 50 hands NOT in:
  - `data/4way_corpus/full_700/batch_001_50hand.jsonl` (50 hands)
  - `data/4way_corpus/full_700/batch_002_50hand.jsonl` (50 hands)
  - `data/4way_corpus/mini_pilot_2e01/mini_pilot_10hand_2026-05-12.jsonl` (10 hands)
- 700 − 110 = 590 remaining; pick first 50 per builder's existing batch slicer
- Persist as `data/4way_corpus/full_700/batch_003_50hand.jsonl`

### Task 2 — 5 fresh Sonnet labeller subagents + Opus tier-up

Same pattern:
- Each labeller reads **PATCHED** `data/4way_labeller_brief.md` + `data/4way_calibration_29hand_2026-05-11.jsonl` + the 50-hand JSONL
- Each produces 50 labels with full reasoning chains
- Output: `data/4way_corpus/full_700/batch_003_raw_labels_labeller_<N>.jsonl` for N ∈ {1,2,3,4,5}
- Opus tier-up on disputed (3-2) Sonnet spots
- Outputs: `data/4way_corpus/full_700/batch_003_consensus.jsonl` + `batch_003_owner_arb_queue.jsonl`

### Task 3 — Regression-watch sentinel (continues)

**0 illegal action votes** across all 5 Sonnet labellers — STOP IMMEDIATELY if ≥1.

### Task 4 — BATCH-003 builder report

`review/comms/BUILDER_REPORT_PHASE2E_FULL_BATCH003_2026-05-12.md`:
- 250 Sonnet + Opus tier-up labels delivered
- Consensus rate (vs BATCH-001 92% / BATCH-002 98%)
- Owner-arb queue size + per-spot detail
- Illegal action vote count (target 0; sentinel for brief-patch regression)
- FL4 + FL5 drift check
- Per-axis label distribution
- Solver-verify queue additions
- Standing comparison vs BATCH-001 + BATCH-002

## STOP-IMMEDIATELY conditions (carried forward)

- ≥1 illegal action vote (sentinel) → STOP / REPORT
- FL4-style rule-based labels → STOP / REPORT
- Consensus collapse >15% → STOP / REPORT
- Owner-arb rate >25% → STOP / REPORT
- Wall-clock >3h → REPORT
- TC-23 EXISTENCE: all output JSONL + builder report git-tracked

## What BATCH-003 does NOT do

- ❌ Does NOT touch river-rats-core/ code
- ❌ Does NOT touch oracle_router / model files / inference path / FEATURE_COLUMNS
- ❌ Does NOT retrain models
- ❌ Does NOT modify brief (frozen at master 8f7a7d0); calibration; 35-ref; 50-pilot; 10-mini-pilot; BATCH-001 + BATCH-002 outputs
- ❌ Does NOT drain solver-verification queue (58 spots HOLD per §6.4)
- ❌ Does NOT modify driver script
- ❌ Does NOT generate new lookalike subset

## After BATCH-003 PASS

Builder pushes → orchestrator QC trigger → merge → BATCH-004 resume directive. Repeat through BATCH-014. Final 750-hand corpus assembly at BATCH-014 → 2-F (3-way retrain) + 2-G (4-way retrain on 750-corpus) + 2-H (production swap).

## Pre-push checks

- HEAD vs `origin/master` at `git checkout -b`: MATCH `745fb43` ✓
- Diff vs master: 1 file (this directive)
- Log vs master: 1 commit

## References

- BATCH-002 + QC PASS: master `745fb43` (PR #433 + #435)
- BATCH-002 resume directive: master `1e528dc` (PR #432)
- 2-E.0.1 mini-pilot + QC PASS (brief patch): master `8f7a7d0` (PR #429 + #431)
- Phase 2-E FULL BATCH-001 + QC PASS: master `b9e723f` (PR #425 + #427)
- Phase 2-E FULL dispatch (FULL ~700 scope authorization): master `1d5503e` (PR #424)
- 4-way labeller brief (PATCHED): `data/4way_labeller_brief.md`
- 29-hand calibration: `data/4way_calibration_29hand_2026-05-11.jsonl`
- 700-hand subset: `data/4way_lookalikes_700hand_full_2026-05-12.jsonl`
- Non-overlap targets: `data/4way_corpus/full_700/batch_001_50hand.jsonl`, `batch_002_50hand.jsonl`, `data/4way_corpus/mini_pilot_2e01/mini_pilot_10hand_2026-05-12.jsonl`
- Memory: `feedback_orchestrator_decides_not_recommends.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_solver_verification_queue.md`, `feedback_orchestrator_branch_base_verification.md`

**Status: Phase 2-E FULL BATCH-003 resume — orchestrator HOW continuation under FULL ~700 owner-authorization. Builder slices next 50 hands (NOT in BATCH-001/002 or mini-pilot), spawns 5 Sonnet + Opus tier-up with PATCHED brief, regression-watch sentinel (0 illegal). After QC PASS → BATCH-004 resume. 12 batches remaining (BATCH-003..014).**
