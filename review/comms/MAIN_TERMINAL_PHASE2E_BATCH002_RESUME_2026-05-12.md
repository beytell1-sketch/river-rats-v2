---
date: 2026-05-12
from: Main terminal (orchestrator; standing-directive autonomous; quality default)
to: LEAD-PROGRAMMER (spawns 5 Sonnet labeller subagents + 1 Opus tier-up subagent at 50-hand BATCH-002 scale)
re: Phase 2-E FULL BATCH-002 — resume FULL ~700-hand labelling pipeline with PATCHED brief on next 50 hands; per QC PASS on 2-E.0.1 mini-pilot (PR #429 + #431 merged at master 8f7a7d0)
status: RESUME — fire BATCH-002 now (under existing FULL ~700-hand owner-authorization PR #424; orchestrator-decided HOW per `feedback_orchestrator_decides_not_recommends.md`)
---

# Phase 2-E FULL BATCH-002 — resume directive

## Why this directive (not a new scope authorization)

Owner authorization for FULL ~700-hand 4-way labelling stands at PR #424 (master `1d5503e`; Option A "Authorize full ~700-hand dispatch"). Builder Option X2 batched approach is in effect (14 × 50-hand batches; BATCH-001 already complete + QC PASS at master `b9e723f`).

BATCH-001 surfaced a labeller-readiness signal on facing_bet=0 action-space discipline. Quality-default Path 3 mini-pilot 2-E.0.1 (PR #428) patched the brief with action-space discipline + FL5 boilerplate and validated at 10-hand scale (0/50 illegal votes; bit-exact QC PASS at PR #431). Brief is now production-ready for the remaining 13 batches.

This directive is an **orchestrator HOW continuation** within the already-authorized FULL scope per `feedback_orchestrator_decides_not_recommends.md` — not a new authorization.

## What BATCH-002 builds

Same pattern as BATCH-001 (PR #425), but with the PATCHED brief.

### Task 1 — Select BATCH-002 50-hand subset

From `data/4way_lookalikes_700hand_full_2026-05-12.jsonl`:
- Slice the next 50 hands NOT in:
  - `data/4way_corpus/full_700/batch_001_50hand.jsonl` (50 hands; already labelled)
  - `data/4way_corpus/mini_pilot_2e01/mini_pilot_10hand_2026-05-12.jsonl` (10 hands; already labelled with patched brief)
- 700 − 60 = 640 remaining hands; pick first 50 (deterministic or systematic axis-stratified per builder's existing batch slicer)
- Persist as `data/4way_corpus/full_700/batch_002_50hand.jsonl`

### Task 2 — 5 fresh Sonnet labeller subagents + Opus tier-up

Same pattern as PR #421 + PR #425 + PR #429:
- Each labeller reads **PATCHED** `data/4way_labeller_brief.md` (master `8f7a7d0`) + `data/4way_calibration_29hand_2026-05-11.jsonl` + the 50-hand JSONL
- Each produces 50 labels with full reasoning chains
- Output: `data/4way_corpus/full_700/batch_002_raw_labels_labeller_<N>.jsonl` for N ∈ {1,2,3,4,5}
- Opus tier-up on disputed (3-2) Sonnet spots
- Consensus per design memo §4.3
- Outputs: `data/4way_corpus/full_700/batch_002_consensus.jsonl` + `batch_002_owner_arb_queue.jsonl`

### Task 3 — Discipline-pass gate (carried forward from 2-E.0.1)

**Continuing gate criterion**: **0 illegal action votes** across all 5 Sonnet labellers on facing_bet=0 spots (if any). The 2-E.0.1 mini-pilot proved the patched brief eliminates FL5; BATCH-002 must continue to honor that.

If ≥1 illegal vote in BATCH-002 → STOP IMMEDIATELY and surface for triage. This is a regression-watch gate; not a hard PROCEED gate (since the patch is already validated), but a sentinel that the brief is holding under scale.

### Task 4 — BATCH-002 builder report

`review/comms/BUILDER_REPORT_PHASE2E_FULL_BATCH002_2026-05-12.md`:
- 250 Sonnet + Opus tier-up labels delivered
- Consensus rate (target ≥85% per BATCH-001's 92% baseline)
- Owner-arb queue size + per-spot detail
- **Illegal action vote count** (target 0; sentinel for brief-patch regression)
- FL4 + FL5 drift check
- Per-axis label distribution
- Solver-verify queue additions
- Standing comparison vs BATCH-001 (consensus rate; arb rate; illegal-vote rate)

## STOP-IMMEDIATELY conditions

- ≥1 illegal action vote across 5 labellers (sentinel for brief-patch regression) → STOP / REPORT
- ANY labeller produces FL4-style rule-based labels → STOP / REPORT
- Consensus collapse rate >15% on BATCH-002 (vs BATCH-001's 8%) → STOP / REPORT
- Owner-arb rate >25% → STOP / REPORT
- Wall-clock >3h for BATCH-002 (vs ~1.5h BATCH-001 baseline) → REPORT
- TC-23 EXISTENCE: all output JSONL + builder report git-tracked

## Builder STOP-surface pattern (carried forward from BATCH-001 pattern)

If builder encounters another labeller-readiness signal or unexpected pattern, STOP and surface to orchestrator. Do NOT improvise additional brief edits in-flight; surface for triage.

## What BATCH-002 does NOT do

- ❌ Does NOT touch river-rats-core/ code
- ❌ Does NOT touch oracle_router / model files / inference path / FEATURE_COLUMNS
- ❌ Does NOT retrain models
- ❌ Does NOT modify brief (frozen at master 8f7a7d0); calibration; 35-ref; 50-pilot; 10-mini-pilot; BATCH-001 outputs
- ❌ Does NOT drain solver-verification queue (57 spots HOLD per §6.4)
- ❌ Does NOT modify driver script `scripts/dispatch_4way_labelling_pilot.py` (frozen from PR #417)
- ❌ Does NOT generate new lookalike subset (uses existing 700-hand JSONL)

## After BATCH-002 PASS

Builder pushes BATCH-002 PR → orchestrator authors QC trigger + merges → orchestrator authors BATCH-003 resume directive. Continue through BATCH-014. After all 14 batches + QC PASS → assemble 750-hand corpus (pilot 50 + full 700) → dispatch 2-F (3-way retrain on 61-feat) + 2-G (4-way retrain on 750-corpus) → 2-H (production swap).

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `8f7a7d0` ✓
- Diff vs master: 1 file (this directive)
- Log vs master: 1 commit

## References

- Phase 2-E.0.1 mini-pilot + QC PASS (brief patch validated): master `8f7a7d0` (PR #429 + #431)
- Phase 2-E.0.1 dispatch (Path 3 quality-default): master `0dae2dd` (PR #428)
- Phase 2-E FULL BATCH-001 + QC PASS: master `b9e723f` (PR #425 + #427)
- Phase 2-E FULL dispatch (Option A authorized; FULL ~700 scope): master `1d5503e` (PR #424)
- Phase 2-E pilot execution + QC PASS: master `bac08e1` (PR #423)
- 4-way labeller brief (PATCHED; production state): `data/4way_labeller_brief.md`
- 29-hand calibration (frozen): `data/4way_calibration_29hand_2026-05-11.jsonl`
- 700-hand subset (frozen; BATCH-002 source): `data/4way_lookalikes_700hand_full_2026-05-12.jsonl`
- BATCH-001 subset (non-overlap target): `data/4way_corpus/full_700/batch_001_50hand.jsonl`
- 2-E.0.1 mini-pilot subset (non-overlap target): `data/4way_corpus/mini_pilot_2e01/mini_pilot_10hand_2026-05-12.jsonl`
- Driver script (reuse): `scripts/dispatch_4way_labelling_pilot.py`
- Memory: `feedback_orchestrator_decides_not_recommends.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_solver_verification_queue.md`, `feedback_bucket_first_labelling.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`

**Status: Phase 2-E FULL BATCH-002 resume directive — orchestrator HOW continuation under FULL ~700-hand owner-authorization (PR #424). Builder slices next 50 hands (NOT in BATCH-001 or 2-E.0.1 mini-pilot), spawns 5 Sonnet labellers + Opus tier-up with PATCHED brief (master 8f7a7d0), evaluates consensus + arb queue + sentinel illegal-vote count (regression-watch). Same pipeline as BATCH-001. After QC PASS → orchestrator authors BATCH-003 resume directive. Repeat through BATCH-014. Then 750-hand corpus assembly → 2-F + 2-G + 2-H.**
