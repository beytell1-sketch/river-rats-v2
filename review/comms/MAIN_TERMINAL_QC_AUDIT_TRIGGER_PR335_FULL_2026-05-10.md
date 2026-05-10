---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #335 — Phase 1.5-D.2 FULL (HU-2..HU-6 25 hands × 5 labellers + Opus tier-up; 24 consensus + 1 owner-arbitrated split HU-6.5) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #335 (FULL)

PR #335: `programmer/phase15d2-full-2026-05-10`. Head `f01e5cba964020b2523cf222f8318c27950e46e5`. Title: "Builder Phase 1.5-D.2 FULL: HU-2..HU-6 25 hands × 5 labellers + Opus tier-up — 24 consensus + 1 owner-arbitrated (HU-6.5: 3-2 Sonnet CALL vs Opus FOLD)".

Builder fired Phase 1.5-D.2 full per dispatch + pilot gate clearance (PR #332 5/5 unanimous + PR #334 QC PASS · 0/0/0).

**Diff summary** (per `gh pr view 335`): 6 files / +442:
- `data/hu_labelling/full_HU2_HU6/calibration_results.jsonl` — 5 labellers re-validated calibration
- `data/hu_labelling/full_HU2_HU6/consensus.jsonl` — 25 hands consensus + confidence
- `data/hu_labelling/full_HU2_HU6/labeller_brief.md` — labeller brief used
- `data/hu_labelling/full_HU2_HU6/opus_tier_up.jsonl` — Opus tier-up sample (6 entries; non-unanimous Sonnet hands)
- `data/hu_labelling/full_HU2_HU6/raw_labels.jsonl` — 5 labellers × 25 hands = 125 outputs
- `review/comms/BUILDER_REPORT_PHASE15D2_FULL_2026-05-10.md` — execution log (203 lines)

**Title claim**: 24/25 consensus; 1 owner-arbitrated split at HU-6.5 (3-2 Sonnet CALL vs Opus FOLD on tier-up disagreement).

Pre-merge QC required per `feedback_qc_required_before_approval.md` (1.5-D.2 produces labels feeding 1.5-D.3 corpus + 1.5-D.4 retrain — milestone-class).

## Audit scope (~15-20 min; 10-item per dispatch §"QC stream — what you audit")

Per dispatch `MAIN_TERMINAL_PHASE15D2_HU_LABELLING_PIPELINE_DISPATCH_2026-05-10.md`:

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): 6 PR files in `data/hu_labelling/full_HU2_HU6/` + 1 builder report. NO source / prompt / model edits.
2. **5 labellers per hand**: raw_labels.jsonl shows 5 distinct labeller IDs × 25 hands = 125 entries; verify count.
3. **Calibration compliance**: every labeller in calibration_results.jsonl has ≥ 20/24 + all 3 GTO-reversal correct; failed labellers NOT in raw_labels.jsonl.
4. **Bucket-first compliance** per `feedback_bucket_first_labelling.md`: labelling prompt does NOT contain equity thresholds.
5. **Solver-vs-labels separation** per `feedback_solver_vs_expert_labels.md`: 3-2 splits → solver verification → research finding only (NOT training label). Verify HU-6.5 consensus is the 3-of-5 majority labeller answer (CALL), not the Opus FOLD.
6. **Consensus rule applied**: ≥4-of-5 → consensus; 3-2 → solver verification + majority; 2-2-1 or worse → owner-arbitrated. Verify per-hand application across 25 hands.
7. **Tier-up gate compliance**: non-unanimous Sonnet hands sampled by 1 Opus labeller; disagreement-rate report present. Title implies 6 non-unanimous → Opus tier-up sample of 6. Disagreement: 1 of 6 = 16.7% > 10% → triggers full Opus re-label of disagreeing hands per dispatch §"Tier-up rule"; verify whether builder ran the re-label or escalated.
8. **Per-axis confidence summary**: builder report shows 5/5 vs 4/5 vs 3-2 distribution per axis HU-2..HU-6.
9. **Owner-arbitration surface (HU-6.5)**: builder report explicitly surfaces HU-6.5 with both Sonnet CALL majority + Opus FOLD; documents what owner needs to decide. Verify the spec is sufficient for owner judgment without re-running pipeline.
10. **TC-X-DISPATCH-COMPLIANCE**: §4.3 spec + consensus rule + tier-up rule + negative scope items honored.

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~15-20 min. QC writes:
- `~/river-rats-qc/findings/2026-05-10-pr335-phase15d2-full.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15D2_FULL_2026-05-10.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## What gates

- PR #335 merge → on QC PASS, orchestrator merges autonomously (data labels are committed; HU-6.5 split is documented for owner judgment downstream)
- HU-6.5 owner-arbitration → orchestrator surfaces to owner via direct message; HOLDs 1.5-D.3 dispatch until owner adjudicates per `feedback_orchestrator_decides_not_recommends.md`
- After owner adjudication on HU-6.5 → orchestrator dispatches Phase 1.5-D.3 (HU corpus assembly) per design memo §4.4

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `1a644ea` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.2 dispatch: master `2ca9431` (PR #331)
- Pilot merged: master `bed7368` (PR #332 builder) + `1a644ea` (PR #334 QC PASS · 0/0/0)
- Builder PR #335 head: `f01e5cb`
- Architect's design memo §4.3 (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `project_qc_heartbeat_convention.md`

**Status: QC stream — fire audit now on PR #335 FULL. ~15-20 min wall-clock. 10-item audit. Heartbeat sync to current master at end of tick. Orchestrator merges PR #335 + QC verdict autonomously on QC PASS per standing directive. Orchestrator surfaces HU-6.5 owner-arbitration separately + HOLDs 1.5-D.3 dispatch until owner adjudicates.**
