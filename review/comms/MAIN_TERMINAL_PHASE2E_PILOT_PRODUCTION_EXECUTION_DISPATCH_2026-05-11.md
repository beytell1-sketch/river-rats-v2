---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous on owner-authorization)
to: LEAD-PROGRAMMER (multi-agent: spawns 5 Sonnet labeller subagents + 1 Opus tier-up subagent; orchestrates collect/consensus/arb-queue)
re: Phase 2-E PILOT production execution — owner authorized Option A "Authorize full pilot" via AskUserQuestion 2026-05-11 ~13:08 SAST
status: DISPATCH — fire now (Phase 2-E pilot infrastructure merged at master fedc617; PR #417 + #419 PASS; owner-authorized production scope)
---

# Phase 2-E PILOT production execution dispatch

## Owner authorization record (2026-05-11 ~13:08 SAST)

Owner answered AskUserQuestion "Authorize the production 5-labeller × 50-hand × Opus tier-up execution for Phase 2-E pilot?" with:

**"A — Authorize full pilot (Recommended)"**

Locks: production-scale 5-labeller × 50-hand × Opus tier-up dispatch; ~3-5h wall-clock authorized; FL4-drift detection STOP-trip remains active.

## Production execution scope (per HU 1.5-D analog)

The infrastructure (50-hand subset + driver script + consensus rule) is in place from PR #417. This dispatch executes the production pipeline:

### Task 1 — 5 fresh Sonnet labeller subagents

Spawn 5 INDEPENDENT Sonnet labeller subagents (FL1-FL5). Each labeller:
- Reads `data/4way_labeller_brief.md` (the operational brief)
- Reads `data/4way_calibration_29hand_2026-05-11.jsonl` (anchor reference)
- Reads `data/4way_lookalikes_50hand_pilot_2026-05-11.jsonl` (the 50 hands to label)
- Produces 50 labels with full reasoning chains (~250-word rationale per hand)
- Writes output: `data/4way_corpus/pilot_50/raw_labels_labeller_<N>.jsonl` for N ∈ {1,2,3,4,5}

**CRITICAL anti-rule-based**: each labeller MUST follow the brief's anti-rule-based boilerplate (no if/elif; no threshold-based; no template repetition). Driver script will run FL4-drift detection on first 10 hands per labeller — if ANY labeller fails drift check, STOP entire pipeline.

**Subagent spec**:
- Subagent type: lead-programmer (gto-expert-hat dominant) OR a dedicated labeller-type if exists
- Prompt: "Label 50 4-way poker spots per the 4-way labeller brief. Read brief + calibration + lookalikes. Produce 50 labels with 250-word reasoning per hand. NO rule-based shortcuts. Output to `data/4way_corpus/pilot_50/raw_labels_labeller_<N>.jsonl`."
- Each labeller gets distinct N + own output file

### Task 2 — Opus 4.7 tier-up subagent

After 5 Sonnet labellers complete + driver collects + consensus rule applied:
- Identify spots with 3-2 split OR 2-2-1+ patterns (per design memo §4.3)
- Spawn 1 Opus subagent: reads 50 hands + 5 Sonnet outputs + brief; produces independent labels especially for contested spots
- Output: `data/4way_corpus/pilot_50/raw_labels_opus_tierup.jsonl`

### Task 3 — Consensus application

Run `python3 scripts/dispatch_4way_labelling_pilot.py collect ...`:
- Apply consensus rule per design memo §4.3:
  - ≥4-of-5 agree → consensus (majority action)
  - 3-2 + Opus agrees → consensus
  - 3-2 + Opus disagrees → owner-arb queue
  - 2-2-1+ → owner-arb queue
- Outputs: `consensus.jsonl` + `owner_arb_queue.jsonl` + `drift_alerts.log`

### Task 4 — Owner-arb queue handling

For each owner-arb spot, per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`:
- Orchestrator (in NEXT dispatch after this one) surfaces to owner OR queues for solver verification
- This dispatch's builder does NOT unilaterally adjudicate
- Owner-arb queue size: target ≤15% (≤7-8 spots out of 50); >25% triggers STOP-condition triage

### Task 5 — Final pilot gate evidence report

`review/comms/BUILDER_REPORT_PHASE2E_PILOT_EXECUTION_2026-05-11.md`:
- 50/50 labels delivered (across 5 labellers + Opus tier-up)
- Consensus rate (target ≥85%)
- Owner-arb queue size + per-spot detail
- FL4-drift detection outcome (no drift / drift detected and stopped)
- Per-axis quality check (each axis has reasonable label distribution)
- Pilot gate verdict (50/50 / mixed / broad fail per dispatch PR #416 §gate)

## Pilot gate verdict criteria (recap from dispatch PR #416)

| Outcome | Action |
|---------|--------|
| 50/50 hands clear (no FL4 drift; consensus pattern healthy; owner-arb 5-20%) | PROCEED to 2-E full ~700 hands |
| Mixed signal (1-2 labellers showing drift; OR owner-arb rate 20-30%; OR consensus collapse on >5% of hands) | REPORT to orchestrator; orchestrator triages |
| Broad fail (rule-based drift; owner-arb >40%; FL4-style methodology violation) | HALT 2-E; brief revision needed |

## STOP-IMMEDIATELY conditions (per dispatch PR #416)

- ANY labeller produces FL4-style rule-based/template/Python-script labels in first 10 hands → STOP IMMEDIATELY (saves spend on bad labels); REPORT
- Consensus collapse rate >10% on first 20 hands → STOP / REPORT
- Owner-arb rate exceeds 30% on first 30 hands → STOP / REPORT
- Wall-clock >10h (vs 3-5h estimate) → REPORT

## What Phase 2-E pilot production execution does NOT do

- ❌ Does NOT touch river-rats-core/ code (this is pure data generation via subagents)
- ❌ Does NOT touch oracle_router / model files / inference path / FEATURE_COLUMNS
- ❌ Does NOT retrain models (2-F / 2-G scope)
- ❌ Does NOT unilaterally adjudicate owner-arb spots (orchestrator handles in next dispatch)
- ❌ Does NOT proceed to 2-E full ~700 hands (gates on this 50-hand pilot evidence)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `fedc617` ✓
- Diff vs master: 1 file (this dispatch)
- Log vs master: 1 commit

## References

- Phase 2-E pilot dispatch: master `9043497` (PR #416)
- Phase 2-E pilot infrastructure: master `e6ddf89` (PR #417) + QC PASS `fedc617` (PR #419)
- Phase 2-E.0 labeller readiness: master `1a6f6cb` (PR #413) + QC PASS `a2834c6` (PR #415)
- 4-way labeller brief: `data/4way_labeller_brief.md` (production-runtime)
- 29-hand calibration set: `data/4way_calibration_29hand_2026-05-11.jsonl`
- 50-hand lookalike subset: `data/4way_lookalikes_50hand_pilot_2026-05-11.jsonl`
- Driver script: `scripts/dispatch_4way_labelling_pilot.py`
- HU 1.5-D analog: `river-rats-core/labelling_agent.py`
- FL4 incident: `review/comms/BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md`
- Design memo §4.3 consensus rule: `review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md`
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_bucket_first_labelling.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_qc_required_before_approval.md`, `feedback_solver_verification_queue.md`

**Status: Phase 2-E PILOT production execution dispatch — owner-authorized Option A "Authorize full pilot". Builder spawns 5 Sonnet labeller subagents + 1 Opus tier-up subagent; runs consensus + drift detection + arb queue + final report. FL4-drift STOP-trip remains active (saves spend if drift). After execution PASS + 50/50 gate clear → 2-E full ~700-hand dispatch. Owner-arb queue handled by orchestrator in subsequent dispatch.**
