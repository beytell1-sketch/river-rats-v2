---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #232 — 12.5J-D-pre test-guard deflake (Option b; tier-2 Δ-tolerance; flake 20%→0%) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #232

PR #232: `programmer/phase125j-d-pre-test-guard-deflake-2026-05-06`. Builder report at `review/comms/BUILDER_REPORT_PHASE125J_D_PRE_TEST_GUARD_DEFLAKE_2026-05-06.md` (in branch). Per dispatch `MAIN_TERMINAL_PR228_RESOLUTION_AND_JDPRE_DISPATCH_2026-05-06.md` (master `e44ed59`, PR #231).

Engineering scope: tier-2 invariant Δ-tolerance widening (top-2 acceptance when top-prob gap < 0.05; strict argmax otherwise). PR title reports flake 20%→0% on MW-33. Per `feedback_pilot_first_for_long_jobs.md` sub-rule: no Opus tier-up needed (engineering test-guard fix; no labelling outputs).

## Audit scope (6 items per dispatch)

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — expected files:
   - `river-rats-core/tests/test_tier2_invariants.py` (or wherever tier-2 invariants live; locate via grep) — Δ-tolerance edit
   - `river-rats-core/test_constants.py` (or equivalent) — `TIER2_BORDERLINE_ARGMAX_TOLERANCE = 0.05` constant + docstring (IF a constants file exists; otherwise inline at top of test file)
   - `review/comms/BUILDER_REPORT_PHASE125J_D_PRE_TEST_GUARD_DEFLAKE_2026-05-06.md`
   
   Verify NOT touched: v3.x prompts (`prompts/`), BATCH2 reference (`design/multiway_reference_set/BATCH2_*`), `river-rats-core/feature_extractor.py` or any feature-side code, model files (`river-rats-core/models/`), training-data (`training-data/`), corpus files (`data/corpus_*.jsonl`), memory files. Anything outside scope → BLOCKER per TC-X-OWNER-SCOPE-DISCIPLINE.

2. **Δ-tolerance correctness** — verify the 0.05 threshold matches PR #212 memo's empirical BLAS-noise observation (gap 0.024 < threshold; 0.05 is the project policy). Verify the conditional logic:
   - `top_gap < 0.05` → top-2 acceptance: assert `EXPECTED_ACTION in top_2_action_indices(probs)`
   - `top_gap ≥ 0.05` → strict argmax: assert `argmax(probs) == EXPECTED_ACTION`
   - Tolerance constant cited via PR #212 memo in docstring/comment

3. **Flake-rate evidence** — verify builder ran 10-run test on MW-33 and reports 0/10 flakes after fix; verify pre-fix flake-rate baseline (~2/10) referenced. Builder report should include the actual command used + pass/fail counts for both pre- and post-fix runs.

4. **Regression check evidence** — verify full tier-2 invariant suite ran on all reference hands; 0 non-borderline regressions reported. Specifically: no hand previously passing strict argmax now fails Δ-tolerance (would only happen if both top-2 don't include EXPECTED_ACTION). Expected: 0 regressions; the tolerance widens pass criteria, never narrows.

5. **TC-X-OWNER-SCOPE-DISCIPLINE** — confirm no v3.x prompts, no BATCH2 edits, no `feature_extractor.py` touched, no model/training-data files touched.

6. **TC-X-DISPATCH-COMPLIANCE (provisional, until owner ratifies)** — cross-check builder's implementation against this dispatch's authoritative spec. Specifically:
   - Did builder implement Option (b) only, or did they ship Option (a) MW-33 whitelist or Option (c) `predictor='cpu_predictor'` hybrid? Per dispatch §"What you do NOT do": Option (b) only is permitted in this PR.
   - Δ-tolerance constant value is exactly `0.05` (not loosened beyond)
   - Prohibitions in §"What you do NOT do" all hold
   - Any unilateral deviation from dispatch spec → SHOULD_FIX (mirror SHOULD_FIX-1 pattern from PR #228 audit)

## QC routing

Standalone stream (`~/river-rats-qc/`) per `feedback_qc_routing_when_standalone_active.md`. Pre-merge audit (engineering scope, but tier-2 invariant test-suite changes touch core CI surface; counts as a milestone for QC). Expected duration: ~10-15 min (single-file edit + flake evidence + regression sweep).

## Output

QC writes `review/comms/REVIEW_QC_PHASE125J_D_PRE_TEST_GUARD_DEFLAKE_2026-05-06.md` on `qc/pr232-jdpre-test-guard-review-2026-05-06`. PR opens. Verdict: PASS / ISSUES FOUND / FAIL.

## What gates on this audit

- PR #232 merge → on QC PASS
- 12.5I-MW40-VERIFICATION-B situation generation dispatch → on PR #232 merge (Hybrid pilot-first clause baked in per PR #231 SHOULD_FIX-1 resolution)
- 12.5J-C trainer integration test on 61-surface → on PR #232 merge (sequential after MW-40-B in builder serial)
- 12.5K combined re-train design → on 12.5I-MW40-VERIFICATION-E + 12.5J-E ship

## What you do NOT do

- Do NOT make GTO judgments (engineering scope, not poker)
- Do NOT modify any file (review-only)
- Do NOT recommend tightening Δ-tolerance below 0.05 (PR #212 memo's empirical floor; below would re-introduce false-positive flake)
- Do NOT recommend loosening Δ-tolerance above 0.05 (would hide real regressions; dispatch prohibition)
- Do NOT run training or inference

## References

- 12.5J-D-pre dispatch: `MAIN_TERMINAL_PR228_RESOLUTION_AND_JDPRE_DISPATCH_2026-05-06.md` (master `e44ed59`, PR #231)
- Option (b) source: `MAIN_TERMINAL_PR205_MW33_RESOLUTION_2026-05-06.md`
- PR #212 memo (MW-33 BLAS non-determinism root-cause; gap 0.024 evidence): master `5da3533`
- PR #205 (12.5J-B feature impl 59→61; the implementation MW-33 flake exposes): master `0b77bdd`
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_spec_vs_infrastructure_code_drift.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: QC stream — fire now on PR #232. Standalone audit, pre-merge, 6-item scope. ~10-15 min.**
