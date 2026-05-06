---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER
re: PR #205 (12.5J-B feature implementation 59→61) — MW-33 invariant-test MEDIUM root-cause memo before merge
status: TRIGGER — fire now (parallel to 12.5I-C labelling Step 1; runs while Sonnet calls burn)
branch: programmer/phase125j-b-mw33-investigation-2026-05-06 (new short-lived branch)
base: master `077c168`
---

# PR #205 — MW-33 invariant-test MEDIUM — root-cause memo before merge

QC posted APPROVE + 1 MEDIUM on PR #205 at 08:27 (PR #210, REVIEW_QC_PHASE125J_B_FEATURE_IMPL_*.md): MW-33 borderline argmax flip RAISE↔BET classified as **real model behavior change, not non-determinism**. Per `feedback_quality_default_no_ask.md`: a 2-feature surface change (59→61) that perturbs an unrelated reference hand does NOT auto-merge on slow-quality default. Need direction classification before merge gate clears.

## LEAD-PROGRAMMER — what you do

Branch: `programmer/phase125j-b-mw33-investigation-2026-05-06` (new short-lived branch off master `077c168`).

### Step 1 — Reproduce the MW-33 flip

Re-run the invariant test on PR #205 commit (`41a40b9`) and on the prior model (the v9-3way-v2.2 baseline, last known clean reference). Capture:

- Pre-PR (59-feature surface) MW-33 argmax + per-class probabilities
- Post-PR (61-feature surface) MW-33 argmax + per-class probabilities
- Probability shift per class (RAISE / BET / CHECK / CALL / FOLD)
- Which of the 2 new features is doing the work (single-feature ablation: rebuild probabilities with each new feature individually zeroed, see which restores the flip)

### Step 2 — Direction classification

Per `feedback_failure_direction_classification.md` — classify the flip in 1 of 4 directions:

1. **IMPROVEMENT** — flipped TOWARD the BATCH2 MW-33 reference label (post-PR matches reference; pre-PR did not)
2. **REGRESSION** — flipped AWAY from the reference (pre-PR matched, post-PR does not)
3. **WASH** — both pre and post are equidistant from reference (e.g., both wrong in different directions)
4. **REFERENCE-SUSPECT** — flip is GTO-correct per gto-expert-hat reasoning + protocol traces, but the reference itself looks empirically wrong (the MW-25 pattern repeating; would require Opus tier-up like MW-25 got)

### Step 3 — Memo

Write `review/comms/BUILDER_MEMO_PR205_MW33_2026-05-06.md`:

- §"Reproduction" — pre/post probabilities + ablation showing which feature caused the flip
- §"Direction classification" — one of 4 above with reasoning
- §"Recommendation" — what the orchestrator should do:
  - IMPROVEMENT → merge PR #205, document MW-33 as ungraduated-improvement (not a stay-wrong, but a directional gain)
  - REGRESSION → do NOT merge; describe what would need to change (drop one of the 2 features, retrain with feature constraint, etc.)
  - WASH → merge with note; MW-33 unchanged from quality standpoint
  - REFERENCE-SUSPECT → do NOT auto-merge; route to orchestrator for Opus tier-up cross-check on MW-33 (MW-25 pattern)

### Constraints

- Investigation only. Do NOT modify river-rats-core/ feature_extractor.py or the trained model.
- Do NOT retrain. If REGRESSION, the memo describes the option; orchestrator decides next dispatch.
- $5 cost cap (probability dumps + ablation are inference-only, should be ~$0.10).
- Time cap: 45 minutes builder time. If reproduction fails or signals are noisy, STOP and report what you have.

### Stop conditions

- Cannot reproduce the flip (test was non-deterministic) → STOP; flag QC's "real model behavior" classification for re-check
- Ablation shows neither new feature explains the flip (it's something else entirely) → STOP, route to orchestrator
- $5 cap reached → STOP, partial memo

### Deliverable

1 file: `review/comms/BUILDER_MEMO_PR205_MW33_2026-05-06.md` on branch `programmer/phase125j-b-mw33-investigation-2026-05-06`. PR opens for orchestrator review (no QC audit needed — investigation memo, not corpus/feature change).

## What this memo gates

PR #205 merge. The QC APPROVE stands; the MEDIUM is the open question. Per `feedback_qc_required_before_approval.md` — milestone PRs (feature surface change is milestone) require QC pre-merge clearance. The MEDIUM is the unaddressed clearance item.

## Sequencing relative to 12.5I-C

This runs **parallel** to 12.5I-C labelling. LEAD-PROGRAMMER:
1. Dispatches 12.5I-C Step 1 (Sonnet calls — long-running)
2. While Sonnet runs, executes this MW-33 investigation
3. By the time 12.5I-C Step 1 finishes, MW-33 memo should be in comms

If LEAD-PROGRAMMER context fills before MW-33 investigation completes: prioritize 12.5I-C Step 2 (the labelling pipeline is the long pole); MW-33 memo can defer to next session.

## References

- PR #205: `programmer/phase125j-b-feature-implementation-2026-05-06` (commit `41a40b9`)
- PR #210: QC verdict (REVIEW_QC_PHASE125J_B_*.md) — APPROVE + 1 MEDIUM
- 12.5J-B builder report: `review/comms/PROGRAMMER_REPORT_PHASE125J_B_*.md` (in PR #205 diff)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_failure_direction_classification.md`, `feedback_qc_required_before_approval.md`, `feedback_explicit_action_trigger.md`

**Status: PR #205 merge HOLD. LEAD-PROGRAMMER fire MW-33 root-cause memo (parallel to 12.5I-C). Memo gates merge.**
