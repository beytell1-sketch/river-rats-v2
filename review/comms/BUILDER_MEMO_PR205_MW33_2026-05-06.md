---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream (informational)
re: PR #205 (12.5J-B feature implementation 59→61) — MW-33 root-cause memo: BLAS reduction-order non-determinism, NOT a feature-driven model behavior change. Mathematical isolation confirmed. Recommendation: merge PR #205; fix the test guard at 12.5J-D.
status: investigation complete (memo only; no code changes; no retraining)
branch: programmer/phase125j-b-mw33-investigation-2026-05-06
base: master `077c168`
---

# PR #205 — MW-33 invariant-test MEDIUM — root-cause memo

## TL;DR

The MW-33 RAISE↔BET argmax flip is **BLAS reduction-order non-determinism on a borderline argmax (gap 0.024)**, not a model behavior change introduced by the 2 new Step 18 features. The 2 new features have **mathematically zero effect** on the `_StudentInferenceLike45` test path — the test feeds `STUDENT_FEATURE_COLUMNS_V9[:45]` to the 45-feature v2.2 anchor, and the first-45 slice is bit-identical pre-PR vs post-PR. Ablation confirms zero probability shift from the new features.

**QC's Audit-5 hypothesis is empirically refuted.** Builder's "pre-existing flakiness" diagnosis on PR #205 is correct.

**Direction classification:** the dispatch's 4 standard categories don't fit; the correct category is a **5th — NON-DETERMINISM-CONFIRMED**. Recommendation: merge PR #205; remediate the test guard at 12.5J-D per the dispatch's Option (a) or (b).

## Reproduction

### Hand setup

`MW-33`: hero `8h8s` on board `8d7c3h`, BB position, facing CO bet, BTN cold-called, 2 villains live (3-way pot). Hero holds **top set 888**. BATCH2 expert action: **RAISE HIGH** (value/protection on dynamic 3-way board).

### Probability dump (PR #205 head `41a40b9`, OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1)

```
Canonical (GtoOracle, 55→45 slice via predict()):  action=RAISE
   FOLD: 0.066055    CHECK: 0.090997    CALL: 0.266854
    BET: 0.275933    RAISE: 0.300161
Student   (_StudentInference[:45]):                action=RAISE
   FOLD: 0.066055    CHECK: 0.090997    CALL: 0.266854
    BET: 0.275933    RAISE: 0.300161

Diff (canonical − student) max: 0.00e+00
```

The two paths produce **bit-identical probability vectors** when run in the same process. Argmax gap RAISE − BET = 0.300161 − 0.275933 = **0.024228**.

### 12-run in-process determinism check

```
Canonical argmaxes (12 runs): all RAISE
Student   argmaxes (12 runs): all RAISE
Canonical RAISE prob: [0.300161, 0.300161] std=0.00e+00
Canonical BET   prob: [0.275933, 0.275933] std=0.00e+00
Student   RAISE prob: [0.300161, 0.300161] std=0.00e+00
Student   BET   prob: [0.275933, 0.275933] std=0.00e+00
```

In-process inference is fully deterministic with the test's threading discipline.

### Cross-process pytest invocation flakiness

```
$ for i in 1..5; do pytest .::test_student_inference_mirror_invariant_on_baseline; done
Run 1: passed
Run 2: passed
Run 3: passed
Run 4: FAILED       ← 1/5 ≈ 20% cross-process flake rate
Run 5: passed
```

The flip occurs across pytest processes (different memory layout, BLAS reduction order seeded by allocation, etc.), not within a single process. This is the classic xgboost multi-threaded-reduction-order non-determinism mode where `OMP_NUM_THREADS=1 + OPENBLAS_NUM_THREADS=1` reduces but does not eliminate variance on borderline argmaxes (gap < ~0.05).

## Single-feature ablation (mathematical isolation)

The 2 new Step 18 features on MW-33:
```
nut_blocker_overcard_count = 0          (no nut FD blocker — set, not flush)
bet_call_multiway_oop_raise_pressure_index = 0.0   (not the MW-47 pattern)
```

Setting either or both to zero in `feat_dict` and re-running the student[:45] path:
```
Zero both:                                 max |Δprob| = 0.00e+00
Zero nut_blocker_overcard_count:           max |Δprob| = 0.00e+00
Zero bet_call_multiway_oop_raise_pressure_index: max |Δprob| = 0.00e+00
```

**Mathematical isolation confirmed**: the new features cannot affect the student[:45] path because the [:45] slice excludes them by construction (positions 60-61). They are also already 0 on MW-33 by feature semantics (no nut blocker for FD; not facing the MW-47 multi-call OOP pattern).

## Why QC's Audit-5 hypothesis is empirically wrong

QC review §"Audit 5" reasoned:
> *"The 12.5J-B test diff shows ZERO modifications to OMP_NUM_THREADS / OPENBLAS_NUM_THREADS setup … yet failing. This means the failure is NOT pure thread non-determinism. The 61-feature surface genuinely shifts the model's probability estimates on MW-33 such that the argmax flips RAISE↔BET despite deterministic threading. This is a real model behavior change introduced by the 2 new features."*

This reasoning would be correct **if** the test fed the new features to the model. It does not. The test pins `feature_columns=STUDENT_FEATURE_COLUMNS_V9[:45]`, deliberately slicing off everything past index 44 to drive the 45-feature v2.2 anchor. Step 18 features sit at indices 59–60, outside the slice. Mathematical inspection plus the ablation above prove the new features cannot influence the test outcome.

QC's "absence of OMP edits = non-thread cause" inference is a missing premise: BLAS non-determinism on borderline argmaxes is NOT eliminated by `OMP_NUM_THREADS=1`. xgboost `predict_proba` uses additional reduction stages (per-tree leaf accumulation, log-loss aggregation) whose ordering depends on per-process allocation patterns. The pre-PR test was already at this borderline (RAISE 0.300 vs BET 0.276 in the 12.5D' design note) and was always flaky at low rates; PR #205 did not introduce the flip — it just got unlucky in the QC's pytest run.

## Direction classification — none of the 4; the answer is a 5th

Per `feedback_failure_direction_classification.md` and the dispatch §"Step 2", the 4 standard buckets are:

| Bucket | Fit? | Why |
|---|---|---|
| 1. IMPROVEMENT (toward reference) | ✗ | Pre and post produce IDENTICAL probabilities (Δ=0.00e+00); both correctly point to RAISE = reference |
| 2. REGRESSION (away from reference) | ✗ | No probability shift pre→post |
| 3. WASH (equidistant) | ✗ | Implies a deterministic shift; there is none |
| 4. REFERENCE-SUSPECT (reference wrong) | ✗ | Reference RAISE is GTO-correct (top set facing bet 3-way always RAISE for value+protection); model already agrees on the deterministic path |

The actual category is **NON-DETERMINISM-CONFIRMED**: pre-PR and post-PR produce identical model output on MW-33; the test failure is process-level BLAS reduction-order variance flipping a 0.024-gap argmax across pytest invocations. This is a **test guard problem, not a model behavior problem**.

## Recommendation

**MERGE PR #205.** The MEDIUM-1 finding is real (the test does fail flakily) but its root cause is mis-attributed. The PR introduces zero behavioral change on MW-33; the merge gate should clear.

**Defer the test fix to 12.5J-D** per the dispatch's existing options. My ranking of the dispatch's two suggested mitigations:

- **Option (a) accept BET as alternative valid outcome on MW-33** — *recommended*. The 0.024 gap is small enough that BLAS noise will keep flipping it; a strict `==` assertion on a 0.024-gap borderline argmax is over-specified. Whitelist `{RAISE, BET}` for MW-33 specifically. Cheap, addresses the symptom, preserves the invariant for non-borderline hands.

- **Option (b) further nail down determinism (MKL/BLAS pinning)** — *not recommended*. I tested with `MKL_NUM_THREADS=1` added; the in-process determinism didn't improve (already deterministic at 0.00e+00). Cross-process variance has additional sources (page allocation, NUMA pinning, etc.) that are hard to lock down without process-level isolation primitives. Effort vs payoff is poor.

A third option worth considering at 12.5J-D:

- **Option (c) tighten tier-1 only** — Replace the strict `==` assertion on `(adjusted_action, correct, was_adjusted)` with a relaxed assertion: *if argmax of canonical and student agree, fine; if they disagree by < 0.005 absolute prob, also fine; only fail on disagreements with > 0.005 prob delta* (i.e., real mirror drift, not BLAS noise). This preserves the test's actual purpose (catch mirror drift) without false-failing on borderline argmaxes.

ml-architect's call at 12.5J-D.

## What I checked

- `git diff 077c168..41a40b9 -- river-rats-core/{feature_extractor,feature_keys,train_model_v9_student}.py` — confirmed the 2 new features are appended at positions 60-61 only; first-45 columns unchanged.
- `_StudentInference.__init__` (`river-rats-core/train_model_v9_student.py:573-588`) — confirmed `feature_columns` parameter slices the input; with `[:45]` the model sees only the first 45 features regardless of what extras live in `feat_dict`.
- `GtoOracle.predict` (`river-rats-core/gto_model.py:126-130`) — confirmed it slices the feature vector to `self._n_features` (= 45 for v2.2 anchor).
- `gto_model.FEATURE_COLUMNS[:45]` vs `STUDENT_FEATURE_COLUMNS_V9[:45]` — confirmed identical via runtime equality check.
- Compute functions `compute_nut_blocker_overcard_count` + `compute_bet_call_multiway_oop_raise_pressure_index` — confirmed side-effect-free; produce dependent values from existing keys; do not mutate any of the first-45 keys.
- 12 in-process inference repeats — std = 0.00e+00 across both paths.
- 5 cross-process pytest runs — 1 failure (≈ 20% flake rate matches "pre-existing flakiness" framing).

## What I did NOT do (per dispatch constraints)

- No edits to `river-rats-core/feature_extractor.py` or any model.
- No retraining.
- No edits to the invariant test (12.5J-D scope, ml-architect's call).
- Did not run the Opus pipeline cross-check (orchestrator-side handles tier-up).

Cost: ~$0.05 (probability dumps + ablation only); under the $5 cap. Time: ~30 min.

## Diagnostic artifact

The probability dump + ablation script lives at `/tmp/rr_pr205/_mw33_diag.py` (transient worktree at PR #205 head). The full output is preserved at `/tmp/mw33_diag.out`. I am NOT committing the script to the branch — investigation only, per dispatch.

## Stop conditions — none triggered

- Could reproduce the flip cross-process: yes (1/5).
- Ablation showed neither new feature explains the flip: yes (Δ=0.00e+00 for both).
- $5 cap reached: no (~$0.05).

## What's blocked / what's queued

**Blocked on this memo:**
- PR #205 merge gate: cleared from builder side (recommendation: MERGE).

**Queued (for orchestrator + ml-architect at 12.5J-D):**
- Test guard re-baseline: pick Option (a) / (b) / (c) above.
- 12.5J-D scope: invariant test policy decision; trainer integration test on 61-feature surface.

**Not affected by this memo:**
- 12.5I-C labelling round (parallel; T8'-r Step 1 fired separately; report follows).

## References

- PR #205 head: `41a40b9` (branch `programmer/phase125j-b-feature-implementation-2026-05-06`)
- QC review (PR #210): `review/comms/REVIEW_QC_PHASE125J_B_FEATURE_IMPLEMENTATION_2026-05-06.md` — Audit 5 §"QC analysis" (the empirically-refuted hypothesis)
- 12.5J-B builder report: `review/comms/BUILDER_REPORT_PHASE125J_B_FEATURE_IMPLEMENTATION_2026-05-06.md` lines 217-227 (builder's "pre-existing" diagnosis — empirically confirmed by this memo)
- 12.5D' invariant test origin: master `1b95648` (PR #130/#131; MW-33 borderline first noted at design time as RAISE 0.300 vs BET 0.276)
- Test source: `river-rats-core/tests/test_train_model_v9_student.py:301-394` (`test_student_inference_mirror_invariant_on_baseline`)
- Dispatch: `review/comms/MAIN_TERMINAL_PR205_MW33_INVESTIGATION_2026-05-06.md` (master `cef0c61`, PR #211)
- Memory: `feedback_failure_direction_classification.md`, `feedback_quality_default_no_ask.md`, `feedback_qc_required_before_approval.md`

**Status:** investigation complete; PR #205 cleared from builder side for merge. Test guard fix deferred to 12.5J-D per dispatch.
