---
date: 2026-05-12
from: Main terminal (orchestrator; standing-directive autonomous on owner-authorization)
to: LEAD-PROGRAMMER (multi-agent: spawns 5 Sonnet labeller subagents + 1 Opus tier-up subagent; orchestrates collect/consensus/arb-queue at 700-hand scale)
re: Phase 2-E FULL — ~700-hand 5-labeller + Opus tier-up dispatch per owner-authorized Option A (2026-05-12 AskUserQuestion); completes 750-hand 4-way corpus per owner-ratified §6.3
status: DISPATCH — fire now (Phase 2-E pilot execution merged at master 8e57307; PR #421 PASS; 50/50 PROCEED gate cleared; pilot brief + driver + consensus pipeline validated at scale 50)
---

# Phase 2-E FULL dispatch — ~700-hand 5-labeller production pipeline

## Owner authorization record (2026-05-12 ~08:54 SAST)

Owner answered AskUserQuestion "Authorize Phase 2-E full — ~700-hand 5-labeller + Opus tier-up production dispatch?" with:

**"A — Authorize full ~700-hand dispatch (Recommended)"**

Locks: production-scale 5-labeller × ~700-hand × Opus tier-up dispatch; same pipeline + brief validated at pilot scale; ~25-40h wall-clock authorized; expected owner-arb 35-105 spots queued for solver-verify per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md` + owner-ratified §6.4.

## Context

Phase 2-E pilot (50-hand) PROCEED gate cleared with:
- 86% Sonnet consensus rate; 7 Opus tier-up disputes all resolved
- 0 owner-arb (Opus closed everything); 0 FL4-drift; 3 solver-verify queue items
- Brief + 29-hand calibration + 50-hand subset + driver + consensus + arb pipeline all validated end-to-end

Phase 2-E full = scale-up of the same pipeline to ~700 additional hands. Target: completes 750-hand 4-way corpus per owner-ratified §6.3 (pilot 50 + full 700 = 750 lookalikes for 2-G retrain).

## What Phase 2-E full builds

### Task 1 — ~700-hand lookalike subset

- Source: same as pilot (PokerBench-multiway filtered to 4-way at decision moment OR analog per architect's Task 2 from PR #417)
- Sample ~700 additional hands NOT in pilot 50 nor in 35-hand reference set nor in 29-hand calibration set
- **Distribution** per design memo §3.X.2 + §6.3 (street-weighted 51/31/11/6; axis coverage):
  - 4-way 3-bet/4-bet pots: ~140 hands
  - Multiway-cooler: ~70 hands
  - Closing-action variants: ~125 hands
  - Range-asymmetry: ~125 hands
  - MW-40/45/47 axis: ~100 hands
  - Standard 4-way SRP: ~140 hands
  - Total: 700 (architect adjusts ±5% per source-data availability)
- Persisted as `data/4way_lookalikes_700hand_full_2026-05-12.jsonl` (or analog naming)

### Task 2 — 5 fresh Sonnet labeller subagents (FL1-FL5)

Same pattern as pilot (PR #421 production execution):
- Each labeller reads `data/4way_labeller_brief.md` + `data/4way_calibration_29hand_2026-05-11.jsonl` + the new 700-hand JSONL
- Each produces ~700 labels with full reasoning chains (~250-word rationale per hand)
- Output: `data/4way_corpus/full_700/raw_labels_labeller_<N>.jsonl` for N ∈ {1,2,3,4,5}
- Anti-rule-based discipline holds (brief boilerplate + driver FL4-drift detection)

**Builder spawning strategy options** (architect picks per scale-management):
- Option X1: spawn 5 labellers simultaneously; each labels all 700 hands in one shot
- Option X2: split 700 into N batches (e.g., 5 × 140-hand batches); spawn labellers per batch; rolling consensus
- Option X3: hybrid (spawn 5 simultaneously; consensus at 100/200/400/700 checkpoints; FL4-drift STOP-trip remains active)

### Task 3 — Opus tier-up

After 5 Sonnet labellers complete each batch (or end-to-end):
- Identify spots with 3-2 split OR 2-2-1+ patterns (per design memo §4.3)
- Opus reads the spots + 5 Sonnet outputs + brief; produces independent labels especially focused on contested spots
- Output: `data/4way_corpus/full_700/raw_labels_opus_tierup.jsonl`
- Expected disputed-spot count: ~10-15% × 700 = 70-105 spots (per HU 1.5-D analog + pilot evidence)

### Task 4 — Consensus rule + owner-arb queue

Driver script (existing `scripts/dispatch_4way_labelling_pilot.py`):
- Apply consensus rule per design memo §4.3 (same as pilot)
- Outputs: `data/4way_corpus/full_700/consensus.jsonl` + `owner_arb_queue.jsonl` + `drift_alerts.log`
- Expected owner-arb rate: 5-15% per HU 1.5-D analog → 35-105 spots

### Task 5 — Owner-arb queue handling strategy

Per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md` + owner-ratified §6.4:
- Owner-arb queue spots are QUEUED for solver-verify later (when solver online)
- Orchestrator may PICK per quality/GTO theory (orchestrator-decides path) for spots where:
  - Action is clear per design memo + brief
  - Consensus is 3-2 with Opus tier-up agreement on majority
- Orchestrator does NOT unilaterally adjudicate spots with 2-2-1+ fragmentation; those genuinely need solver
- This dispatch's BUILDER does NOT adjudicate — surface raw queue to orchestrator in builder report

### Task 6 — Final corpus assembly

Combine pilot 50 (from PR #421) + full 700 = 750-hand 4-way corpus:
- `data/4way_corpus/full_750/consensus.jsonl` (master corpus for 2-G retrain)
- All consensus-state spots + orchestrator-adjudicated arb spots = final training data
- `data/4way_corpus/full_750/solver_verify_queue.jsonl` (combined pilot's 3 + full's solver-verify items)

### Task 7 — Final pilot+full evidence report

`review/comms/BUILDER_REPORT_PHASE2E_FULL_2026-05-12.md`:
- 700/700 labels delivered (across 5 Sonnet + Opus tier-up)
- Consensus rate (target ≥85% per pilot benchmark)
- Owner-arb queue size + per-spot detail
- FL4-drift detection outcome
- Per-axis label distribution
- Solver-verify queue (full+pilot combined)
- 750-hand final corpus integrity check

## STOP-IMMEDIATELY conditions (per pilot pattern; scaled)

- ANY labeller produces FL4-style rule-based/template/Python-script labels in first 50 hands → STOP IMMEDIATELY (saves substantial token spend); REPORT
- Consensus collapse rate >10% on first 100 hands → STOP / REPORT
- Owner-arb rate >25% on first 200 hands (vs pilot 0%; substantial deviation) → STOP / REPORT
- Wall-clock >50h (vs 25-40h estimate) → REPORT
- TC-23 EXISTENCE: all output JSONL files + builder report git-tracked

## Builder STOP-surface pattern (per HU 1.5-D + pilot analog)

Per the 2-E pilot pattern (PR #417 → owner-authorize → PR #420 → PR #421):
- Builder MAY split into infrastructure PR + production-execution PR if scale-management requires it
- Builder MAY checkpoint at 100/200/400/700 hand boundaries with intermediate reports
- These splits are operational; the orchestrator-owner authorization is for the full 700-hand scope

If builder hits scale-management STOP, surface for orchestrator triage (NOT re-authorization since owner already authorized full scope).

## What Phase 2-E full does NOT do

- ❌ Does NOT touch river-rats-core/ code
- ❌ Does NOT touch oracle_router / model files / inference path / FEATURE_COLUMNS
- ❌ Does NOT retrain models (2-F / 2-G scope)
- ❌ Does NOT drain solver-verification queue (HOLD per owner-ratified §6.4; this dispatch ADDS items to queue)
- ❌ Does NOT modify pilot 50 corpus (read-only; combines into 750)
- ❌ Does NOT modify brief / calibration / reference set (all frozen)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `8e57307` ✓
- Diff vs master: 1 file (this dispatch)
- Log vs master: 1 commit

## References

- Phase 2-E pilot execution (PASS 50/50): master `8e57307` (PR #421)
- Phase 2-E pilot production execution dispatch: master `7a45640` (PR #420)
- Phase 2-E pilot infrastructure + QC PASS: PR #417 + #419
- Phase 2-E.0 labeller readiness + QC PASS: PR #413 + #415
- Phase 2-A design memo §6.3 (owner-ratified 4-way corpus origin): `review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md`
- 4-way labeller brief: `data/4way_labeller_brief.md`
- 29-hand calibration: `data/4way_calibration_29hand_2026-05-11.jsonl`
- Pilot 50-hand lookalikes: `data/4way_lookalikes_50hand_pilot_2026-05-11.jsonl`
- Pilot corpus output: `data/4way_corpus/pilot_50/`
- Driver script: `scripts/dispatch_4way_labelling_pilot.py`
- HU 1.5-D analog: `river-rats-core/labelling_agent.py`
- FL4 incident: `review/comms/BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md`
- Pilot QC verdict (local; PASS 0/0/0): `~/river-rats-qc/findings/2026-05-12-pr421-phase2e-pilot-execution.md`
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_solver_verification_queue.md`, `feedback_bucket_first_labelling.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_qc_required_before_approval.md`

**Status: Phase 2-E FULL dispatch — owner-authorized Option A "Authorize full ~700-hand dispatch". Builder spawns 5 Sonnet labellers + Opus tier-up + consensus + arb queue at 14× pilot scale. Same brief + calibration + driver + consensus rule. Same FL4-drift STOP-trip. Builder may split infrastructure + production-execution PRs per pilot pattern; owner-authorization extends to full 700-hand scope. After execution PASS → 750-hand corpus complete → 2-F (3-way retrain on 61-feat) + 2-G (4-way retrain on 750-corpus) → 2-H (production swap).**
