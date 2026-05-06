---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream
re: Phase 12.5J-D-pre test-guard deflake (Option b: tier-2 Δ-tolerance) — MW-33 RAISE↔BET argmax flip neutralised; flake rate 20%→0%; 0 regressions in test suite
status: complete; PR opens for QC audit
branch: programmer/phase125j-d-pre-test-guard-deflake-2026-05-06
base: master `e44ed59` (post-PR #228 + #230 + #231 merge)
---

# Phase 12.5J-D-pre — test-guard deflake (Option b)

## Headline

| Step | Result |
|---|---|
| Locate failing test | ✅ `river-rats-core/tests/test_train_model_v9_student.py::test_student_inference_mirror_invariant_on_baseline` (the "Two-tier assertion" test on the 45-feature anchor; tier-2 strict equality on `(adjusted_action, correct, was_adjusted)` was the flaking layer) |
| Δ-tolerance implementation | ✅ Two-tier check: tier-1 `np.allclose(canonical_probs, student_probs, atol=1e-5)` catches real mirror drift; tier-2 `min(top_gap_canonical, top_gap_student) < 0.05` accepts borderline-argmax BLAS flips |
| Δ-tolerance constant | ✅ `TIER2_BORDERLINE_ARGMAX_TOLERANCE = 0.05` + `BLAS_NOISE_PROB_ATOL = 1e-5` at module level (no `test_constants.py` exists; inlined per dispatch fallback) |
| Flake rate before | ✅ 2/10 FAIL = **20%** (matches PR #212 memo + dispatch estimate) |
| Flake rate after | ✅ 0/10 FAIL = **0%** |
| Regression check (full file) | ✅ 18/18 tests pass post-fix; 0 regressions |
| Stop conditions | ✅ none triggered |

**Cost:** ~$0 (no LLM calls; CI test-guard fix only). **Time:** ~35 min builder including before/after measurement + report.

## §"Files edited"

```
 review/comms/BUILDER_REPORT_PHASE125J_D_PRE_TEST_GUARD_DEFLAKE_2026-05-06.md | (new)
 river-rats-core/tests/test_train_model_v9_student.py                        | +91 -7
```

Single test-file edit + builder report. No production-source modification (`reference_evaluator.py`, `train_model_v9_student.py`, `feature_extractor.py`, `gto_model.py` all untouched). No prompts, no BATCH2, no model files, no training-data.

## §"Δ-tolerance implementation"

### Failure mode (verified empirically)

Verbose capture of one of the baseline failures:

```
AssertionError: Mirror drift between reference_evaluator and _StudentInference on
1 of 40 hands: [{'ref_id': 'MW-33', 'canonical': ('RAISE', True, False),
                 'student':   ('BET',   True, False)}]
```

Both paths produce `correct=True` (because `_evaluate_one_hand`'s `_normalize` collapses `BET↔RAISE` for not-facing-bet spots — see `reference_evaluator.py:629-633`); the strict-equality check on raw `adjusted_action` is what triggers the flake. Top-2 probability gap on MW-33 ≈ 0.024 < 0.05 BLAS-noise threshold per PR #212 memo.

### Constant (module-level in test file)

```python
# 12.5J-D-pre tier-2 invariant Δ-tolerance constants (PR #228 SHOULD_FIX-1
# Path 3 Hybrid resolution; PR #212 memo: BLAS reduction-order non-determinism
# observed gap ≈0.024 on MW-33 with strict argmax-equality flaking ~20%).
# Tier-1 (np.allclose) catches real mirror drift; Tier-2 (top-gap < tolerance)
# accepts borderline argmax flips driven by BLAS noise. Do NOT widen beyond
# 0.05 — that's the empirical BLAS-noise threshold per memo; loosening further
# would hide real regressions.
TIER2_BORDERLINE_ARGMAX_TOLERANCE = 0.05
BLAS_NOISE_PROB_ATOL = 1e-5
```

### Test-loop logic (replaces strict equality)

When the original strict-equality check fires (action drift between canonical and student), the new logic:

1. **Tier-1 check** — recover probability vectors via a closure `_probs_for_hand(h)` that mirrors the helper functions' `hand_dict` + `extract_all_features` construction (no production-source change). If `not np.allclose(cp, sp, atol=1e-5)` → real mirror drift (different model / features / feat_dict construction). Record with `reason="tier1_prob_drift"` + `max_prob_diff`. **This is a NEW failure mode that the previous strict-action assertion never exercised.**

2. **Tier-2 borderline check** — if both probability vectors are np.allclose AND `min(canonical_top_gap, student_top_gap) < TIER2_BORDERLINE_ARGMAX_TOLERANCE` → accept. BLAS reduction-order can flip argmax when the top-2 gap is below the BLAS-noise threshold; this is the deflake the dispatch sanctions.

3. **Tier-2 non-borderline check** — if probs are np.allclose AND both top-gaps ≥ tolerance, an argmax flip is mathematically anomalous (small allclose deviations cannot tip a non-borderline gap). Record with `reason="tier2_nonborderline_argmax_flip"` + both top-gaps.

The original strict-equality semantics are preserved for the COMMON case (no action drift): the new code only fires when the original assertion would have failed; otherwise behavior is identical.

### Why no production-source change

Dispatch §"Deliverable scope" expected files: test edit + (optional) constants file + builder report. The probability vectors are needed for the Δ-tolerance check but `_evaluate_one_hand` and `_evaluate_student_one_hand` don't return them. Two options:

- **A.** Modify `HandResult` dataclass + both helpers to return `prob_array`. Touches `reference_evaluator.py` + `train_model_v9_student.py` (production source).
- **B.** Reproduce the inference inline in the test via a closure. Test-only change; ~30 lines of feat_dict construction duplication contained in the test function.

Chose B per dispatch's "small + CI-only" framing. Duplication is mitigated by the closure being scoped to the single test function; if the canonical helpers' `hand_dict` shape evolves, the test will surface the divergence via tier-1 prob_drift before the closure stale-syncs (every existing tier-1-fail message includes ref_id + max_prob_diff, leaving a fast diagnostic trail).

## §"Flake rate before/after"

### 10-run measurement, MW-33 mirror-invariant test only (deterministic test infra: `OMP_NUM_THREADS=1 + OPENBLAS_NUM_THREADS=1 + n_jobs=1` set inside the test as before; not changed)

| Run | Pre-fix (master `e44ed59`) | Post-fix (this PR) |
|---|---|---|
| 1 | FAIL (28s) | PASS (28s) |
| 2 | PASS (28s) | PASS (27s) |
| 3 | FAIL (28s) | PASS (28s) |
| 4 | PASS (28s) | PASS (28s) |
| 5 | PASS (28s) | PASS (28s) |
| 6 | PASS (28s) | PASS (28s) |
| 7 | PASS (28s) | PASS (28s) |
| 8 | PASS (27s) | PASS (27s) |
| 9 | PASS (28s) | PASS (28s) |
| 10 | PASS (29s) | PASS (30s) |
| **Flake rate** | **2/10 = 20%** | **0/10 = 0%** |

Pre-fix flake rate exactly matches the dispatch's "~20%" estimate from PR #212 memo. Post-fix: 10 consecutive PASS. The Δ-tolerance approach succeeds at neutralising the BLAS reduction-order argmax flip on MW-33 without inventing a hand whitelist (Option a, prohibited per dispatch) and without touching xgboost predictor configuration (Option c, prohibited per dispatch).

### Verbose failure capture (run 1 of pre-fix sequence)

```
=== Failure ===
AssertionError: Mirror drift between reference_evaluator and _StudentInference on
1 of 40 hands: [{'ref_id': 'MW-33', 'canonical': ('RAISE', True, False),
                 'student':   ('BET',   True, False)}]
```

Confirms: only MW-33 flips, only argmax-of-probs differs, both paths' `correct` and `was_adjusted` are `True` and `False` respectively (not bug-causal), and the 39 other reference hands never drift across runs. The flake is exactly the borderline-argmax pattern the dispatch describes.

## §"Regression check"

Full test file run on the post-fix code:

```
$ pytest tests/test_train_model_v9_student.py --tb=short -q
..................                                                       [100%]
18 passed in 28.06s
```

18 of 18 tests pass. Specifically, the other 17 tests in this file (module-load assertions, loaders, joins, prepad-baseline-booster round-trip, solver-overlay arithmetic, warm-start canonicality, baseline-models filter, select_median_litmus_seed) do not interact with the mirror-invariant test's probabilistic assertion path; the new constants (`TIER2_BORDERLINE_ARGMAX_TOLERANCE`, `BLAS_NOISE_PROB_ATOL`) are unreferenced by them and have no module-import side effects. **0 regressions.**

The fix's logic only widens the pass criteria (allows borderline argmax flips that previously would have failed); it never narrows the pass criteria. There is no logical path by which a previously-passing hand could now fail Δ-tolerance — that would require either (a) probs differing materially (which would have been a real mirror drift the strict assertion ALSO caught conceptually but couldn't measure) or (b) non-borderline argmax disagreement under bit-identical probs (mathematically impossible).

## §"Stop conditions" (full record)

Per dispatch §"Stop conditions":

| Condition | Triggered? | Evidence |
|---|---|---|
| Flake rate after fix > 5% on MW-33 | NO | 0/10 = 0% (well below 5%) |
| Any non-MW-33 hand passing strict argmax now fails Δ-tolerance | NO | Full-file regression check 18/18 PASS |
| Δ-tolerance breaks unrelated tier-2 logic | NO | Other 17 tests untouched in behavior |

No stop conditions triggered. No route to orchestrator for Option (c) needed.

## §"What I did NOT do" (per dispatch §"What you do NOT do")

- ❌ Did NOT widen tolerance beyond 0.05 (kept at the BLAS-noise empirical threshold)
- ❌ Did NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md` untouched)
- ❌ Did NOT modify any model file or training-data file
- ❌ Did NOT touch BATCH2 reference (`design/multiway_reference_set/BATCH2_*` untouched)
- ❌ Did NOT modify `feature_extractor.py` or any feature-side code
- ❌ Did NOT modify `reference_evaluator.py` or `train_model_v9_student.py` production source (closure pattern in test avoids this)
- ❌ Did NOT add Option (a) MW-33 whitelist as a parallel guard (Option b makes it unnecessary)
- ❌ Did NOT add Option (c) `predictor='cpu_predictor'` configuration (separate dispatch if needed; not in scope)

## What's blocked / what's queued

**Cleared by this PR (after merge):**
- 12.5I-MW40-VERIFICATION-B situation generation dispatch (Hybrid pilot-first clause baked into dispatch per PR #228 SHOULD_FIX-1 Path 3 resolution)
- NIT-1 + NIT-2 fix-forward (folded into the next BATCH2 / design-comm touch by orchestrator-scope)

**Awaiting orchestrator dispatch:**
- 12.5I-MW40-VERIFICATION-B (next builder fire-now after this PR merges)
- 12.5J-C trainer integration test on 61-surface (later, post-12.5J-D-pre)

## References

- Dispatch (fire trigger): `MAIN_TERMINAL_PR228_RESOLUTION_AND_JDPRE_DISPATCH_2026-05-06.md` (master `e44ed59`, PR #231)
- PR #228 (MW-40-VERIFICATION-A design): master `e0e0304`
- PR #230 (QC verdict on PR #228): master `e5dceb2`
- PR #212 memo (MW-33 BLAS non-determinism root-cause): master `5da3533`
- 12.5J-D-pre Option (b) source: `MAIN_TERMINAL_PR205_MW33_RESOLUTION_2026-05-06.md`
- Test file modified: `river-rats-core/tests/test_train_model_v9_student.py` (lines 46-58 constants; lines ~380-470 closure + Δ-tolerance loop)
- Memory: `feedback_quality_default_no_ask.md` (slow-quality default; no widening beyond 0.05), `feedback_explicit_action_trigger.md` (named-author execution per dispatch), `feedback_listen_to_orchestrator_always.md` (dispatch authoritative wording followed exactly), `feedback_named_author_builds_not_polls.md` (next-tick AUTHOR), `feedback_builder_grounds_before_executing.md` (read source + verbose-failure capture before edit), `feedback_verify_source_not_plan.md` (source files cross-checked against the dispatch's pseudocode)

**Status: 12.5J-D-pre test-guard deflake (Option b) complete. PR opens for QC audit per dispatch §"QC stream". Builder ready for 12.5I-MW40-VERIFICATION-B dispatch on this PR's merge (Hybrid pilot-first clause baked in per PR #228 SHOULD_FIX-1 Path 3 resolution).**
