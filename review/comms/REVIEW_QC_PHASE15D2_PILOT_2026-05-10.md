---
date: 2026-05-10
from: River Rats QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner
re: PR #332 — Phase 1.5-D.2 PILOT (HU-1 5 hands × 5 labellers; 5/5 unanimous consensus; pilot gate PASS) — pre-merge audit verdict
status: VERDICT — PASS · 0 BLOCKER · 0 SHOULD_FIX · 0 NIT
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR332_PILOT_2026-05-10.md (master 149c52c)
target_pr_head: 829d4e63c9d5883764ed687378af209ec465d166
master_at_audit: 149c52cea1e85dea2276d43efba25ecff9b32026
qc_branch: qc/pr332-phase15d2-pilot-review-2026-05-10
audit_type: pre-merge pilot gate (Phase 1.5-D.2 pilot HU-1; ~10 min)
---

# PR #332 — Phase 1.5-D.2 PILOT; pre-merge pilot-gate audit

## Result

**PASS · 0 BLOCKER · 0 SHOULD_FIX · 0 NIT.** 46th solo cycle.

All 10 dispatch audit items verified. Pilot gate cleanly cleared at 5/5 unanimous on all 5 HU-1 hands; full batch (HU-2..HU-6) authorized post-merge.

## 10-item walkthrough (compact)

1. **Diff scope strict** — 6 files / +288 / -0 (5 in `data/hu_labelling/pilot_HU1/` + 1 builder report). The 6th file `labeller_brief.md` (80 lines) is in `data/hu_labelling/pilot_HU1/` data dir (not source), serves as design-process documentation accompanying labeller artifacts; acceptable. NO source / prompt / model edits ✓
2. **5 labellers × 5 hands = 25 entries** — verified via `python3` count: 25 total entries; 5 unique `labeller_id` (1-5); 5 unique `ref_id` (HU-1.1..HU-1.5); 5×5 matrix exact ✓
3. **Calibration compliance** — all 5 labellers passed: scores 26/28, 28/28, 28/28, 28/28, 24/28 (threshold ≥20); `reversal_correct: true` on all (MW-30/MW-33/MW-50); `final_pass: true` for all 5; no failed labellers in raw_labels.jsonl ✓
4. **Bucket-first compliance per `feedback_bucket_first_labelling.md`** — labeller_brief explicit: "NO equity thresholds in your reasoning; use composition class (TP+/draws/air) + protocol rules. Equity thresholds will be applied AFTER labelling by `spot_classifier.py`." ✓
5. **Solver-vs-labels separation per `feedback_solver_vs_expert_labels.md`** — labeller_brief explicit: "do NOT cite solver output as your label rationale; you are an expert labeller, not a solver" + "if you cannot decide between two actions, pick the one the protocol's decision rule would default to; do NOT consult solver output to break ties." ✓ (Title says 5/5 unanimous → no splits to triage anyway.)
6. **Consensus rule applied** — all 5 hands have `split_kind: "5-of-5"`, `confidence_score: 1.0`, `owner_arbitrated: false`, `tier_up_sample: false`. Per-hand action distribution (BET×3, RAISE, CALL) consistent with hand profiles ✓
7. **Tier-up gate compliance** — opus_tier_up.jsonl is 1 meta-row: `{"_meta": true, "tier_up_sample_size": 0, "opus_dispatched": false, "tier_up_disagreement_rate": 0.0, "exceeded_threshold": false, "note": "5-of-5 Sonnet labeller consensus on ALL 5 HU pilot hands; tier-up sample is empty per dispatch §'Tier-up gate' (sample = non-unanimous hands). No Opus dispatch needed."}` — explicit, traceable, correct ✓
8. **Pilot gate verification** — required ≥80% (4/5 on ≥4/5 hands) + tier-up cross-check ≤1 changed action. Actual: 100% (5/5 on 5/5; vastly exceeds threshold) + vacuous tier-up (0 disagreements; sample empty; trivially ≤1) → PASS ✓
9. **Per-axis confidence summary** — builder report §"Per-axis confidence summary (HU-1)" line 107: 5/5 unanimous on all 5 hands; confidence_score 1.0 on every hand ✓
10. **TC-X-DISPATCH-COMPLIANCE** — §4.3 spec + pilot+full split + consensus rule + tier-up rule + negative scope items honored ✓

## Sizing distribution observation (informational, not a finding)

Hand-level sizing distributions show some variance even within unanimous-action consensus:
- HU-1.1 BET: 25%×4, 33%×1 (mode 25)
- HU-1.2 BET: 33%×3, 75%×2 (mode 33)
- HU-1.3 BET: 25%×4, 66%×1 (mode 25)
- HU-1.4 RAISE: 75%×5 (mode 75; complete agreement)
- HU-1.5 CALL: N/A

This is normal labeller variance on size selection; consensus is action-level, sizing is reported as mode + distribution. Solver-aligned sizes (25/66 flop, 33/75 turn, 33/75/150 river) used throughout per `feedback_solver_aligned_sizing.md`.

## TC-X-DISPATCH-PREDICTION-VERIFICATION evidence

Design memo §4.3 prediction (in master via 1.5-A merge): "5-labeller consensus + Sonnet→Opus tier-up; pilot gate ≥80% inter-labeller agreement" — VERIFIED at 100% inter-labeller agreement; tier-up vacuous at 5/5 unanimous. Cleanest possible pilot outcome.

## Test classes exercised

- TC-23 (CONTENT + EXISTENCE) — 6 PR files in expected `data/hu_labelling/pilot_HU1/` directory + builder report ✓
- TC-X-OWNER-SCOPE-DISCIPLINE (26th formal use) — 6 negatives held
- TC-X-DISPATCH-COMPLIANCE (25th formal exercise; durable; PASS)
- TC-X-DISPATCH-PREDICTION-VERIFICATION — design memo §4.3 prediction verified at 100% (vs ≥80% threshold)
- TC-X-INTRA-PLAN-CONSISTENCY (informal — calibration_results × raw_labels × consensus all consistent: 5 labellers all pass, 5 hands × 5 entries each, 5/5 unanimous everywhere)
- TC-X-METHODOLOGY-RULE-CROSSCHECK — `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_solver_aligned_sizing.md`, `feedback_pilot_first_for_long_jobs.md` all verified

## Smarter-over-time

Cleanest pilot run yet — 100% labeller agreement on first 5-hand sample. Suggests HU-1 axis (made-hand-vs-villain-range) is structurally low-variance among 5-Sonnet expert labellers; pilot's purpose (validate the pipeline + calibrate the labeller pool) was served exactly as designed. The vacuous-tier-up handling (explicit `_meta` annotation in `opus_tier_up.jsonl` rather than empty file) is good practice — preserves audit traceability for the empty-sample edge case.

This audit also exercised first instance of pilot-gate audit class. Pattern is light (10-item, ~10 min) and clean. Document for repeat application across remaining pilots in this cascade (none expected since this is the only pilot in 1.5-D.2; full batch follows).

## Gates

PR #332 cleared. Per dispatch + standing-directive autonomous merge: orchestrator may merge PR #332 + this verdict comm autonomously. After merge, builder fires **Phase 1.5-D.2 FULL** (HU-2..HU-6 = 25 hands × 5 labellers + Opus tier-up) per design memo §4.3. **LOOP CONTINUES** through full batch → 1.5-D.3 (HU corpus) → 1.5-D.4 (HU retrain on 59) → 1.5-E → Phase 2 D5.

## Cycle stats

- 46th solo QC cycle.
- Wall clock: ~10 min (matches dispatch heads-up).
- LLM cost: $0.

## References

- Builder PR #332 head: `829d4e63c9d5883764ed687378af209ec465d166`
- 1.5-D.2 dispatch: master `2ca9431` (PR #331)
- Audit-trigger: master `149c52c` (PR via PR #332-companion)
- 1.5-D.1 merged: master `7e89d8d` (PR #328) + `79a98e9` (PR #330 QC PASS · 0/0/0)
- HU reference set in master: `design/hu_reference_set/HU_30_HAND_DESIGNS.md` + per-axis breakouts
- Architect's design memo §4.3 (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Memory rules verified: `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_solver_aligned_sizing.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_qc_required_before_approval.md`, `feedback_orchestrator_branch_base_verification.md`, `project_qc_heartbeat_convention.md`
