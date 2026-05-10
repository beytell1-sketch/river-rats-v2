---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #332 — Phase 1.5-D.2 PILOT (HU-1 5 hands × 5 labellers; unanimous 5/5 consensus on all hands; pilot gate PASS) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #332 (PILOT)

PR #332: `programmer/phase15d2-pilot-hu1-2026-05-10`. Head `829d4e63c9d5883764ed687378af209ec465d166`. Title: "Builder Phase 1.5-D.2 PILOT: HU-1 5 hands × 5 labellers — 5/5 unanimous consensus on all hands; pilot gate PASS; full batch authorized".

Builder fired Phase 1.5-D.2 pilot per dispatch `MAIN_TERMINAL_PHASE15D2_HU_LABELLING_PIPELINE_DISPATCH_2026-05-10.md` (master `2ca9431`, PR #331).

**Diff summary** (per `gh pr view 332`): 6 files / +288:
- `data/hu_labelling/pilot_HU1/calibration_results.jsonl` — 5 labellers × calibration exam scores
- `data/hu_labelling/pilot_HU1/consensus.jsonl` — 5 hands × consensus action + confidence
- `data/hu_labelling/pilot_HU1/raw_labels.jsonl` — 5 labellers × 5 hands = 25 labeller outputs
- `data/hu_labelling/pilot_HU1/opus_tier_up.jsonl` — 1 Opus labeller × non-unanimous hands (likely empty since 5/5 unanimous)
- `data/hu_labelling/pilot_HU1/labeller_brief.md` — labeller brief used (80 lines)
- `review/comms/BUILDER_REPORT_PHASE15D2_PILOT_2026-05-10.md` — execution log + gate result

**Title claim**: 5/5 unanimous on all 5 hands; pilot gate PASS; full batch authorized.

Pre-merge QC required per `feedback_qc_required_before_approval.md` (1.5-D.2 produces labels feeding 1.5-D.3 corpus + 1.5-D.4 retrain — milestone-class).

## Audit scope (~15-20 min; 10-item per dispatch §"QC stream — what you audit")

Per dispatch `MAIN_TERMINAL_PHASE15D2_HU_LABELLING_PIPELINE_DISPATCH_2026-05-10.md` §"QC stream — what you audit":

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): 6 PR files in `data/hu_labelling/pilot_HU1/` + 1 builder report. NO source / prompt / model edits. (Note: builder added a 6th file `labeller_brief.md` — assess whether this is acceptable design-process documentation or scope creep.)
2. **5 labellers per hand**: raw_labels.jsonl shows 5 distinct labeller IDs × 5 hands; verify count.
3. **Calibration compliance**: every labeller in calibration_results.jsonl has ≥ 20/24 + all 3 GTO-reversal correct; failed labellers NOT in raw_labels.jsonl.
4. **Bucket-first compliance** per `feedback_bucket_first_labelling.md`: labelling prompt does NOT contain equity thresholds; thresholds in `spot_classifier.py` post-labelling.
5. **Solver-vs-labels separation** per `feedback_solver_vs_expert_labels.md`: any 3-2 splits → solver verification → research finding only (NOT training label). Title says 5/5 unanimous → likely no splits to triage.
6. **Consensus rule applied**: ≥4-of-5 → consensus; 3-2 → solver verification + majority; 2-2-1 → owner-arbitrated. Verify per-hand application.
7. **Tier-up gate compliance**: non-unanimous hands sampled by 1 Opus labeller; disagreement-rate report present. With 5/5 unanimous on all 5 hands, the sample is empty — verify opus_tier_up.jsonl is empty + builder report explains.
8. **Pilot gate verification**: inter-labeller agreement ≥ 80% (4-of-5 on ≥ 4-of-5 hands) — title says all 5/5, easily clears. Tier-up cross-check ≤ 1 changed action — N/A with empty sample.
9. **Per-axis confidence summary**: builder report shows 5/5 distribution for HU-1 axis.
10. **TC-X-DISPATCH-COMPLIANCE**: §4.3 spec + pilot+full split + consensus rule + tier-up rule + negative scope items honored.

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~15-20 min wall-clock. QC writes:
- `~/river-rats-qc/findings/2026-05-10-pr332-phase15d2-pilot.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15D2_PILOT_2026-05-10.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha` to current master

## What gates

- PR #332 merge → on QC PASS, orchestrator merges autonomously per standing directive
- After PR #332 + QC verdict merge → builder fires full batch (HU-2..HU-6 25 hands × 5 labellers + Opus tier-up)
- After full PR + QC PASS → orchestrator dispatches Phase 1.5-D.3 (HU corpus assembly)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `2ca9431` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.2 dispatch: master `2ca9431` (PR #331)
- Builder PR #332 head: `829d4e6`
- 1.5-D.1 merged: master `7e89d8d` (PR #328 builder) + `79a98e9` (PR #330 QC PASS · 0/0/0)
- HU reference set in master: `design/hu_reference_set/HU_30_HAND_DESIGNS.md` + per-axis breakouts
- Architect's design memo (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` §4.3
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_orchestrator_branch_base_verification.md`, `project_qc_heartbeat_convention.md`

**Status: QC stream — fire audit now on PR #332 PILOT. ~15-20 min wall-clock. 10-item audit. Heartbeat sync to current master at end of tick. Orchestrator merges PR #332 + QC verdict autonomously on PASS per standing directive. Then builder fires full batch (HU-2..HU-6).**
