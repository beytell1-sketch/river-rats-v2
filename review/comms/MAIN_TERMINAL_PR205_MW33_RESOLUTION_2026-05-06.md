---
date: 2026-05-06
from: Main terminal (orchestrator)
to: Owner · LEAD-PROGRAMMER · QC stream
re: PR #205 (12.5J-B feature implementation 59→61) — MW-33 MEDIUM resolved as pre-existing BLAS non-determinism; merge PR #205; queue 12.5J-D-pre test-guard deflake
status: DIRECTIVE — merges PR #212 (memo record) + PR #205 (feature impl); queues 12.5J-D-pre
---

# PR #205 MW-33 MEDIUM — resolution

Builder PR #212 memo (`BUILDER_MEMO_PR205_MW33_2026-05-06.md`): the MW-33 RAISE↔BET argmax flip is BLAS reduction-order non-determinism on a borderline argmax (gap 0.024), NOT a feature-driven model behavior change. The 2 new Step 18 features at positions 60-61 are mathematically excluded from the test path (`_StudentInferenceLike45` slices `STUDENT_FEATURE_COLUMNS_V9[:45]`).

## Orchestrator verification of memo evidence

Per `feedback_verify_source_not_plan.md`, I checked the load-bearing claims:

| Claim | Evidence in memo | Verdict |
|---|---|---|
| Bit-identical canonical vs student[:45] within process | Δ=0.00e+00 across 12 runs; std=0 on all 4 columns | Strong |
| Ablation: zeroing new features changes nothing | max\|Δprob\|=0.00e+00 (zero one, zero both) | Strong |
| Test slice [:45] excludes features at positions 60-61 | `STUDENT_FEATURE_COLUMNS_V9[:45]` slice; new features at 59-60 by Step 18 design | Strong |
| Cross-process flake rate ≈20% pre-existing | 1/5 pytest runs failed; argmax gap 0.024 < ~0.05 BLAS-noise threshold | Strong |
| QC's "OMP=1 → no non-determinism" premise is false for xgboost predict_proba reduction stages | Direct contradiction by 1/5 cross-process flake at fixed thread count | Strong |

All five evidence chains are independently testable and consistent. Memo finding stands.

## Direction classification — 5th category recognized: NON-DETERMINISM-CONFIRMED

The MW-33 dispatch enumerated 4 directions (IMPROVEMENT / REGRESSION / WASH / REFERENCE-SUSPECT). The memo correctly identifies a 5th — **NON-DETERMINISM-CONFIRMED** — where the apparent change is fully attributable to a stochastic test-execution artifact unrelated to the PR's diff.

For the merge framework: NON-DETERMINISM-CONFIRMED maps closest to **WASH-equivalent** (no real model behavior change introduced by the PR). Per the dispatch's WASH branch: "merge with note; MW-33 unchanged from quality standpoint." Slow-quality default applies because the underlying flake is a separable concern remediated at 12.5J-D (test-guard fix), not a property of the PR #205 features.

## Orchestrator decision

1. **PR #212 (memo record) merges** as record. The memo is the operational artifact for the resolution.

2. **PR #205 (12.5J-B feature implementation 59→61) merges.** QC APPROVE stands; the 1 MEDIUM is reclassified as pre-existing BLAS borderline-argmax flake on the test path, not feature-driven. The 2 new features ship into the 61-feature surface for 12.5K combined re-train.

3. **12.5J-D-pre dispatch queued** — test-guard deflake before any further 12.5J work. Options per memo §"Recommendation":
   - Option (a): whitelist BET on MW-33 (accepts the borderline flake; documents tolerance)
   - Option (b): widen tier-2 invariant to Δ-tolerance (e.g., assert argmax stable OR top-2 prob gap < 0.05; passes both RAISE and BET on this borderline)
   - Option (c): seed reduction-order via xgboost `predictor='cpu_predictor'` with single-threaded reduction discipline (eliminates BLAS variance entirely; possibly slower)

   ml-architect-hat decision per slow-quality default favors **Option (b)** (least invasive; preserves test signal for non-borderline regressions; codifies the borderline-argmax tolerance as project policy). Owner can override.

4. **12.5J-C dispatch (next phase: 12.5J retrain on 61-feature surface)** stays gated on 12.5J-D-pre completion + 12.5I-C merge + Opus tier-up.

## LEAD-PROGRAMMER — what you do NEXT (after PR #205/#212 merge)

This directive does NOT yet fire 12.5J-D-pre — that ships as a separate dispatch once 12.5I-C lands (the labelling round is the long-pole; 12.5J-D-pre is a small CI-only fix that can interleave). Queue check only:

- After 12.5I-C PR #213 merges + Opus tier-up clears: I dispatch 12.5J-D-pre with explicit Option (b) implementation brief.
- No action on 12.5J branches until that dispatch.

## QC stream — what you do

- This resolution requires no QC audit (memo + orchestrator review + verification cycle complete).
- Continue with PR #213 audit per `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR213_2026-05-06.md` (this PR #211 sibling).

## Owner — what's surfaced (informational; no decision required)

- PR #205 merging on slow-quality grounds: the MEDIUM is reclassified, not waived. The flake's separable; the deflake ships at 12.5J-D-pre.
- Owner WHAT decision unchanged: BATCH2 MW-25 update α/β still pending (now with 4-source + 30-hand convergence backing α). MW-40 graduation candidate flagged on PR #213 builder report — orchestrator will run Opus tier-up post-QC-verdict (mirrors MW-25 PR #209 pattern; ~$5).
- If owner wants to override the slow-quality merge call (e.g., hold PR #205 until deflake ships first): say so before 12.5J-D-pre dispatches.

## What's blocked / what's queued

**Cleared by this directive:**
- PR #212 merge (memo record)
- PR #205 merge (feature impl 59→61)

**Newly queued (not blocking):**
- 12.5J-D-pre test-guard deflake dispatch (after 12.5I-C merges)

**Still in flight (independent):**
- PR #213 (12.5I-C labelling round) — QC audit firing per sibling PR #211 directive
- MW-40 Opus tier-up — orchestrator runs after PR #213 QC verdict

## References

- PR #212: `programmer/phase125j-b-mw33-investigation-2026-05-06` (memo)
- PR #205: `programmer/phase125j-b-feature-implementation-2026-05-06` (commit `41a40b9`)
- PR #210: QC verdict on PR #205 (REVIEW_QC §"Audit 5") — master `b75424e`
- MW-33 investigation dispatch: master `cef0c61` (PR #211)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_failure_direction_classification.md`, `feedback_qc_required_before_approval.md`, `feedback_verify_source_not_plan.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: PR #212 + PR #205 cleared for merge. 12.5J-D-pre queued. PR #213 audit in flight (sibling directive).**
