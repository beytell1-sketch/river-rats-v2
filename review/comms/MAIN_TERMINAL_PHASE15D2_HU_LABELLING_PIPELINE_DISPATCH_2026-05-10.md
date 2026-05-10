---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous)
to: LEAD-PROGRAMMER (architect-hat lead; 5-labeller-per-hand × pilot 5 + full 25 = 150 labeller invocations + 1 Opus tier-up cross-check + reviewer per `docs/PROCESS_GUIDE.md`) · QC stream (FYI; standalone audit on PR open) · Owner (notice)
re: Phase 1.5-D.2 — HU labelling pipeline (pilot 5 → tier-up gate → full 25); 5-labeller consensus per Stage 4 plan + Sonnet→Opus tier-up sub-rule
status: DIRECTIVE — fires LEAD-PROGRAMMER (orchestrator-hat for pipeline; architect-hat for spot setup; gto-expert-labeller-hat for individual labellers via fresh-agent dispatches) — fire now
---

# Phase 1.5-D.2 — HU labelling pipeline dispatch

## Context (state at this dispatch)

Phase 1.5-D.1 merged at master `7e89d8d`:
- Builder PR #328 `7e89d8d`: 30 HU postflop reference spots × 6 axes (HU-1..HU-6); 18 close + 12 canonical; reviewer-approved + fixer-applied; orchestrator emergency authorship + builder review/adoption appended
- QC verdict PR #330 `79a98e9`: PASS · 0/0/0 (45th solo cycle)
- Reference set deliverables in master at `design/hu_reference_set/HU_30_HAND_DESIGNS.md` + per-axis breakouts

This dispatch fires Phase 1.5-D.2 as the SECOND sub-sub-phase of Phase 1.5-D (HU re-train cascade): label the 30 HU spots through the 5-labeller consensus pipeline per architect's design memo §4.3 (in master).

## LEAD-PROGRAMMER — fire now

You are authorized to fire Phase 1.5-D.2 per design memo §4.3 (in master since 1.5-A merge). Architect-hat sets up the pipeline; 5 fresh labeller agents per hand (no shared state) dispatched in batches per `docs/PROCESS_GUIDE.md` §1.1; 1 Opus tier-up cross-check on non-unanimous Sonnet hands; 1 reviewer for compliance audit. Estimated $-spend per design memo §5 cost forecast (HU labelling row); ~2-4h wall-clock for pilot + full batches.

### Single committed scope: design memo §4.3 in master

The architect's §4.3 IS the binding spec. Do not re-design; execute.

- **Labeller version**: `prompts/gto_labeller_v3.4.md` (or current at fire time; architect commits to v3.4 unless updated)
- **5-labeller consensus per hand**: each labeller is a fresh agent with NO shared state
- **BLIND calibration mandatory** per `docs/PROCESS_GUIDE.md` §2.1: 20/24 minimum on calibration exam + ALL 3 GTO-reversal hands correct. Agent must NOT have access to `river-rats-core/calibration_exam.py` or any answer key during the exam.
- **Bucket-first labelling** per `feedback_bucket_first_labelling.md`: NO equity thresholds in labelling prompt; thresholds live in `river-rats-core/coaching/spot_classifier.py` and applied AFTER labelling
- **Solver-vs-labels separation** per `feedback_solver_vs_expert_labels.md`: solver verifies disagreements + informs research; solver output is NEVER a training label

### Consensus rule (binding)

- ≥ 4 of 5 labellers agree on action → consensus action; confidence = labeller-count / 5
- 3-2 split → solver verification (single solver run on the spot); solver answer = research finding; consensus action = 3-of-5 majority labeller answer (or owner-arbitrated if research contradicts majority)
- 2-2-1 or worse → owner-arbitrated; surface in 1.5-D.2 builder report

### Tier-up gate (binding per `feedback_pilot_first_for_long_jobs.md` sub-rule)

- All training-data outputs require Sonnet → Opus cross-check on a SAMPLE
- Sample = all hands where Sonnet 5-labeller consensus is below 5-of-5 (i.e., any non-unanimous hand)
- 1 Opus labeller runs on the sample; agreement with Sonnet majority is reported
- **Disagreement on > 10% of sampled hands triggers full Opus re-label of the disagreeing hands** (~5-8 hands typically)

### Pilot+full split (binding)

- **Pilot batch: 5 hands = HU-1 axis (HU-1.1, HU-1.2, HU-1.3, HU-1.4, HU-1.5)** per design memo §4.2 pilot designation
- **Full batch: 25 hands = axes HU-2..HU-6** (HU-2.{1..5}, HU-3.{1..5}, HU-4.{1..5}, HU-5.{1..5}, HU-6.{1..5})
- **Full batch fires ONLY after pilot clears the gate per §4.2:**
  - Inter-labeller agreement ≥ 80% (4 of 5 labellers consensus on ≥ 4 of 5 hands)
  - Sonnet → Opus tier-up cross-check on disagreements yields ≤ 1 changed action
  - If pilot fails: HALT and report; do NOT dispatch the remaining 25 hands

### Output (in PR diff — pilot first, then full after gate)

Pilot batch (1.5-D.2-pilot PR):
1. `data/hu_labelling/pilot_HU1/raw_labels.jsonl` — 5 labellers × 5 hands = 25 labeller outputs
2. `data/hu_labelling/pilot_HU1/consensus.jsonl` — 5 hands × consensus action + confidence
3. `data/hu_labelling/pilot_HU1/calibration_results.jsonl` — 5 labellers × calibration exam scores
4. `data/hu_labelling/pilot_HU1/opus_tier_up.jsonl` — 1 Opus labeller × non-unanimous hands
5. `review/comms/BUILDER_REPORT_PHASE15D2_PILOT_2026-05-10.md` — execution log + gate result + tier-up findings + 3-2/2-2-1 splits surfaced

Full batch (1.5-D.2-full PR; ONLY after pilot gate clears):
6. `data/hu_labelling/full_HU2_HU6/raw_labels.jsonl` — 5 labellers × 25 hands = 125 outputs
7. `data/hu_labelling/full_HU2_HU6/consensus.jsonl` — 25 hands × consensus + confidence
8. `data/hu_labelling/full_HU2_HU6/calibration_results.jsonl` — 5 labellers × calibration exam scores (re-validated)
9. `data/hu_labelling/full_HU2_HU6/opus_tier_up.jsonl` — Opus tier-up on non-unanimous hands
10. `review/comms/BUILDER_REPORT_PHASE15D2_FULL_2026-05-10.md` — execution log + 3-2/2-2-1 splits + per-axis confidence summary

### Methodology constraints (binding)

- **Single committed path** per `feedback_quality_default_no_ask.md`: no menus; commit to one config; no "Option A vs B" specs
- **Pilot-first** per `feedback_pilot_first_for_long_jobs.md`: ENFORCED via gate above; full batch holds until pilot PASSES
- **No deadlines** per `feedback_no_deadlines.md`: forecast ~2-4h; quality path beats schedule
- **Calibration is mandatory** per `docs/PROCESS_GUIDE.md` §2.1: failed calibration = labeller does NOT participate; replace with another fresh agent
- **STOP conditions** per CLAUDE.md §5: labeller failure-mode (e.g., refuses to label, gives non-action output, contradicts itself within hand) → STOP and report. Do NOT improvise.
- **Verify own output** per CLAUDE.md §7: builder report includes per-hand consensus, per-labeller calibration scores, tier-up disagreement rate, owner-arbitrated splits enumerated

### What this PR does NOT do (mandatory negative scope)

- ❌ Does NOT execute 1.5-D.3 corpus assembly (separate sub-sub-phase)
- ❌ Does NOT execute 1.5-D.4 retrain (separate)
- ❌ Does NOT modify any source / data / prompt / model files outside `data/hu_labelling/`
- ❌ Does NOT pre-empt §4.4 corpus assembly protocol
- ❌ Does NOT use solver output as training label (solver is for verification only per `feedback_solver_vs_expert_labels.md`)
- ❌ Does NOT relax calibration gate (20/24 + 3 GTO-reversal correct is binding)
- ❌ Does NOT improvise on STOP conditions

## QC stream — what you audit (post-PR; standalone, ~15-20 min per PR — pilot then full)

Routing per `feedback_qc_routing_when_standalone_active.md`. Pre-merge QC required per `feedback_qc_required_before_approval.md` (1.5-D.2 produces the labels that feed 1.5-D.3 corpus + 1.5-D.4 retrain — milestone-class).

10-item audit (per pilot PR + per full PR):

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): pilot = 4 data files in `data/hu_labelling/pilot_HU1/` + 1 builder report. Full = 4 data files in `data/hu_labelling/full_HU2_HU6/` + 1 builder report. NO source/prompt/model edits.
2. **5 labellers per hand**: raw_labels.jsonl shows 5 distinct labeller IDs × N hands; verify count.
3. **Calibration compliance**: every labeller in calibration_results.jsonl has ≥ 20/24 + all 3 GTO-reversal correct; failed labellers are NOT in raw_labels.jsonl.
4. **Bucket-first compliance** per `feedback_bucket_first_labelling.md`: labelling prompt does NOT contain equity thresholds; spot_classifier.py applies thresholds AFTER (verify via cross-reference).
5. **Solver-vs-labels separation** per `feedback_solver_vs_expert_labels.md`: solver outputs (if any 3-2 splits) are research findings, NOT promoted to training labels.
6. **Consensus rule applied**: ≥4-of-5 → consensus; 3-2 → solver verification + majority; 2-2-1 → owner-arbitrated. Verify per-hand application.
7. **Tier-up gate compliance** (pilot only): non-unanimous hands sampled by 1 Opus labeller; disagreement-rate report present; if > 10%, full Opus re-label on disagreers documented.
8. **Pilot gate verification** (pilot PR): inter-labeller agreement ≥ 80% (4-of-5 on ≥ 4-of-5 hands); tier-up cross-check ≤ 1 changed action.
9. **Per-axis confidence summary** (full PR): builder report shows 5-of-5 vs 4-of-5 vs 3-2 vs 2-2-1 distribution per axis HU-2..HU-6.
10. **TC-X-DISPATCH-COMPLIANCE**: §4.3 spec + pilot+full split + consensus rule + tier-up rule + negative scope items honored.

QC writes per PR:
- `~/river-rats-qc/findings/2026-05-10-pr<n>-phase15d2-{pilot|full}.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15D2_{PILOT|FULL}_2026-05-10.md`
- Heartbeat sync to current master

## Owner — what you gate (informational)

- Standing directive: orchestrator merges this dispatch + builder PRs (pilot then full) + QC verdicts autonomously per quality default
- Owner-arbitrated splits (2-2-1 or worse) surface to owner gate via builder report; orchestrator HOLDs awaiting owner judgment per `feedback_orchestrator_decides_not_recommends.md`
- After 1.5-D.2 full batch + verdict merge: orchestrator dispatches **Phase 1.5-D.3** (HU corpus assembly; ~600-900 labelled situations target) per design memo §4.4

## Loop status

Loop CONTINUES through 1.5-D.2 pilot → tier-up gate → full → QC → 1.5-D.3 dispatch → 1.5-D.4 retrain → 1.5-E (router/coaching) → Phase 2 D5 deferred per blueprint.

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `79a98e9` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.1 merged: master `7e89d8d` (PR #328 builder) + `79a98e9` (PR #330 QC verdict PASS · 0/0/0)
- HU reference set in master: `design/hu_reference_set/HU_30_HAND_DESIGNS.md` + per-axis breakouts (HU-1..HU-6)
- Architect's design memo (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` §4.3
- Labeller prompt: `prompts/gto_labeller_v3.4.md`
- Calibration exam: `river-rats-core/calibration_exam.py` (NEVER given to labellers during exam)
- Spot classifier (post-labelling thresholds): `river-rats-core/coaching/spot_classifier.py`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_no_deadlines.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_explicit_action_trigger.md`, `project_qc_heartbeat_convention.md`

**Status: LEAD-PROGRAMMER fires Phase 1.5-D.2 pilot (HU-1 5 hands × 5-labeller consensus + Opus tier-up cross-check) on this comm merge. Pilot gate PASS gates full batch (HU-2..HU-6 25 hands). STOP > improvise on anomalies. Orchestrator merges pilot PR + QC verdict + full PR + QC verdict autonomously per standing directive on PASS. Loop CONTINUES through 1.5-D.3 dispatch post-full-merge.**
