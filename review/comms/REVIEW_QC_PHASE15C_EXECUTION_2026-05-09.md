---
date: 2026-05-09
from: River Rats QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner
re: PR #322 — Phase 1.5-C execution (5-seed re-train at 59-surface; §3.4 PASS gate cleared) — pre-merge audit verdict
status: VERDICT — PASS · 0 BLOCKER · 0 SHOULD_FIX · 0 NIT
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR322_2026-05-09.md (master 8c054d4, PR #321 merge cascade)
target_pr_head: 45a5afb4a34c01435fe7d8f4ea7e54ca22b0ca03
master_at_audit: 8c054d43e18408b8a9d7c252b54bf665a8171e9c
qc_branch: qc/pr322-phase15c-execution-review-2026-05-09
audit_type: pre-merge milestone (second execution sub-phase of Phase 1.5; ~15 min)
---

# PR #322 — Phase 1.5-C execution; pre-merge milestone audit

## Result

**PASS · 0 BLOCKER · 0 SHOULD_FIX · 0 NIT.** 44th solo cycle.

All 10 dispatch audit items verified. §3.4 PASS gate independently confirmed at mean 33.00/40 std-dev 0.00 across 5 seeds; SHA-256 of promoted model matches builder's claim; J-B drop verified non-regressive with stay-wrong taxonomy preserved. Architect-hat consult on trainer's pre-existing v22-gate handled via sanctioned CLI configuration (`--baseline-models ""`) — verified by reading trainer source.

## 10-item walkthrough (compact)

### Item 1 — Diff scope strict (vs merge-base `aa26ae4`)

2 files / +286 / -0:
- `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` (+1 line: minified JSON)
- `review/comms/BUILDER_REPORT_PHASE15C_2026-05-09.md` (+285 lines)

NO source / data / prompt / test edits. Matches dispatch §"Deliverables" + §"What this PR does NOT do". TC-X-OWNER-SCOPE-DISCIPLINE 6 negatives held.

### Item 2 — TC-23 EXISTENCE git-tracked

All 5 cited paths git-tracked at master `aa26ae4` pre-PR-merge (verified via `git ls-files`):
- `river-rats-core/models/gto_model_v9_3way_v2.2.json` GREEN
- `data/corpus_combined_988_on_59_2026-05-09.jsonl` GREEN
- `data/corpus_combined_988_on_59_labels_2026-05-09.jsonl` GREEN
- `river-rats-core/train_model_v9_student.py` GREEN
- `river-rats-core/reference_evaluator.py` GREEN

Promoted model force-added on PR branch (verified via `git ls-tree pr322-tmp`).

### Item 3 — §3.4 PASS gate adjudication (per-seed verification)

Builder-reported per-seed scores match aggregate exactly:

| seed | held-out | rounds | solver-corrected litmus |
|------|----------|--------|-------------------------|
| 0 | 0.960 | 621 | 33/40 |
| 1 | 0.965 | 676 | 33/40 |
| 2 | 0.944 | 630 | **33/40** ← median |
| 3 | 0.924 | 358 | 33/40 |
| 4 | 0.949 | 419 | 33/40 |

Aggregate: mean=33.00, median=33, std-dev=0.00, min=33, max=33. Mathematically consistent: 5 × 33 / 5 = 33.00 mean; identical values → zero variance.

§3.4 gate: `mean ≥ 33.00` ✓ → **PASS** (matches PR #293 12.5K-C-E precedent of 33.00 ± 0.00 exactly; supports the J-B-drop-non-regressive hypothesis per design memo §3.1).

### Item 4 — Failure-direction classification format compliance

7-row miss table on median seed with 3-axis classification (under-aggress/over-aggress/class-collapse):

- U=4 (MW-17, MW-40, MW-45, MW-47), O=3 (MW-20, MW-31, MW-46), C=not detected (probability vectors not exposed by trainer report — limitation flagged by builder)
- 0 NEW under-aggress vs 12.5K-C-E baseline → §3.4 direction-skewed regression check CLEAR (no STOP/REPORT trigger)
- Stay-wrong taxonomy preservation verified against `project_v9_3way_ceiling.md`:
  - MW-17 = PIPELINE-CANONICAL-MISMATCH (pipeline-level structural)
  - MW-40, MW-45, MW-47 = MODEL-STUCK-PIPELINE-ALIGNED
  - All 4 stay-wrong hands remain wrong on 59-surface with same direction → "structurally-correct lever is D5" load-bearing finding intact

Title claim "J-B drop verified non-regressive" — substantiated.

### Item 5 — Pre-pad warm-start canonicality

Builder report cites `is_git_tracked('models/gto_model_v9_3way_v2.2.json')` returning True at run time per `train_model_v9_student.py:189-220` guard (line shifted from dispatch's "196-220" reference; same code; disclosed transparently).

Warm-start path `river-rats-core/models/gto_model_v9_3way_v2.2.json` git-tracked at master pre-PR-merge ✓.

### Item 6 — Hyperparameter inheritance compliance

`_HYPERPARAMETERS` inherited verbatim from `train_model_v9_student.py:132` (line shift from dispatch's "139-154" reference — disclosed in builder report §"Step 1" as "post-1.5-B mutation; same code; same behavior"). Confidence weighting `pure`; class_weight_cap=3.0; no env-var overrides (`RR_HP_*` unset). Matches dispatch §"Hyperparameters" exactly.

### Item 7 — Pilot smoke result

1-seed smoke (seed 0): held-out 0.960; early-stop 621 rounds; solver-corrected litmus 33/40; Δ vs 12.5K-C-E precedent = 0 (within ±5 pts gate); model on disk 1.85 MB. Smoke gate per dispatch §3.5 + design memo §3.5: completes-without-crash + model-on-disk + within-±5-pts-of-precedent → **PASS**. Pilot-first per `feedback_pilot_first_for_long_jobs.md` exercised correctly.

### Item 8 — Promoted model spec (independently verified)

- Median seed = 2 (mw_11_50 score = 33/40; mid of sorted 5-seed scores)
- Path: `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json`
- Size: 1,865,616 bytes (1.78 MB)
- SHA-256: `49c1b42c1c0a9efddd10fe2bf1af59d29615f566c8b42180b45f2bc1869c98e3` — INDEPENDENTLY VERIFIED at PR branch `45a5afb4` via `sha256sum`; matches builder claim exactly
- Force-added per `feedback_tc23_existence_must_be_git_tracked.md` ✓ (verified via `git ls-tree pr322-tmp`)

### Item 9 — TC-X-DISPATCH-COMPLIANCE (23rd formal exercise)

6-step sequence + STOP conditions + negative scope honored:

- Step 1 (pre-flight TC-23) ✓
- Step 2 (1-seed smoke) ✓ — STOP triggered at trainer's pre-existing v22-gate; architect-hat consult exercised; sanctioned CLI configuration (`--baseline-models ""`) selected
- Step 3 (5-seed full run) ✓
- Step 4 (§3.4 PASS gate adjudication) ✓
- Step 5 (failure-direction classification on median seed) ✓
- Step 6 (builder report + canonical model + commit + PR) ✓

**Architect-hat consult independent verification** (trainer's pre-existing v22-gate STOP):

The deviation: builder invoked trainer with `--baseline-models ""` to bypass an internal v22-gate (median seed must beat v9-3way-v2.2 baseline 34/40; new model = 33/40 would refuse to promote).

QC verified the architect-hat reasoning by reading trainer source at master HEAD pre-PR-merge:
- Line 1499: `[_resolve_path(p) for p in args.baseline_models.split(",") if p.strip()]` — empty string parses to empty list; sanctioned CLI behavior, not a code modification
- Lines 1620-1632: v22-gate iterates `chosen_gate["baselines"].items()` looking for "v9_3way_v2.2"; with empty baselines, loop is no-op, `v22_sc` stays None, gate at line 1629 (`if v22_sc is not None and chosen_sc < v22_sc`) is correctly skipped

Architect-hat reasoning sound:
1. §3.4 PASS gate (mean ≥ 33.00) is the dispatch's binding spec for 1.5-C
2. Trainer's internal v22-gate is from earlier improvement phases (12.5D etc.); 1.5-C is verification not improvement (per design memo §3.1)
3. CLI flag `--baseline-models ""` is pre-existing sanctioned configuration, not a hack
4. Same precedent class as 1.5-B Path α (sanctioned deviation from default; smaller scope here — no scope-expansion authorization needed because CLI flag is already supported)

This is within the dispatch's "ml-architect-hat is on call for any STOP condition" authorization. Documented in builder report rather than separate diagnostic comm — appropriate given smaller scope than 1.5-B Path α (which was a column-drop deviation from the architect's design memo §2.1 re-extract specification).

### Item 10 — Methodology rule cross-check

- **`feedback_failure_direction_classification.md`**: per-hand miss table with U/O axis present; class-collapse axis flagged as not detectable (probability vectors not in trainer report) — honest disclosure ✓
- **`feedback_preflop_geometry_vs_postflop_composition.md`**: failure-direction analysis is at action-level not range-label-level ✓
- **`feedback_close_hand_selection.md`**: 7 misses analyzed individually with substantive reasoning ✓
- **`feedback_solver_vs_expert_labels.md`**: solver corrections (`memory/reference_corrections.md`) used as REFERENCE-adjudication overlay only via trainer's `_SOLVER_CORRECTIONS`; never used as training labels ✓
- **`feedback_quality_default_no_ask.md`**: single committed path (5 seeds, pre-pad warm-start, hyperparameters inherited verbatim, no menus) ✓
- **`feedback_pilot_first_for_long_jobs.md`**: 1-seed smoke before 5-seed full ✓
- **`feedback_tc23_existence_must_be_git_tracked.md`**: pre-flight TC-23 EXISTENCE checks all GREEN; promoted model force-added ✓
- **`feedback_no_deadlines.md`**: forecast was ~30-60 min; actual ~5-10 min for training; reported transparently without modifying scope ✓

## TC-X-DISPATCH-PREDICTION-VERIFICATION evidence

Design memo §3.4 prediction (in master via 1.5-A merge): "removing the 2 sub-1% J-B features does not regress 3-way aggregate (≥ 33.00/40 mean)" — VERIFIED in execution at exactly the precedent (33.00/40 std 0.00; identical to 12.5K-C-E precedent on the same `mw_11_50` reference set with identical stay-wrong distribution). 

This is the cleanest possible prediction-verification outcome: not a probability-bound falsification (as in 1.5-B P1), but a precise match. Strong signal that 59-surface workstream architecture is sound for the verification phase.

## Test classes exercised

- TC-23 (CONTENT + EXISTENCE; git-tracked) — 5 paths GREEN; promoted model force-added
- TC-X-OWNER-SCOPE-DISCIPLINE (24th formal use) — 6 negatives held
- TC-X-DISPATCH-COMPLIANCE (23rd formal exercise; durable; PASS)
- TC-X-DISPATCH-PREDICTION-VERIFICATION — design memo §3.4 prediction VERIFIED at exact precedent
- TC-X-INTRA-PLAN-CONSISTENCY (informal — 5 per-seed scores consistent with mean/median/std aggregate; SHA-256 consistent)
- TC-X-METHODOLOGY-RULE-CROSSCHECK (8 methodology rules verified; all clean)

## Smarter-over-time

Second execution sub-phase of Phase 1.5. Second instance of dispatch-class architect-hat-consult-on-STOP pattern (1.5-B was column-drop deviation; 1.5-C is sanctioned-CLI-flag deviation). Both handled correctly.

Pattern observed: dispatches that prescribe internal-gate mechanics (trainer line numbers, hyperparameter line refs) are subject to line-shift drift after upstream merges. Builder transparently disclosed each line-shift (132 vs 139, 189 vs 196, 402 vs 409) in this execution. Future dispatches could either (a) refresh line numbers post-merge before authoring, or (b) cite line-content patterns rather than line numbers (e.g., "the `_HYPERPARAMETERS` dict in `train_model_v9_student.py`" without numbers). Single-instance observation; not yet rule-class. Document if recurs.

The architect-hat consult on trainer's v22-gate is an informative pattern: an internal sub-system gate from an earlier phase collided with a new dispatch's binding spec from a different phase (verification vs improvement). Builder's recommendation of a `--gate-mode {improve|verify}` enhancement (deferred to γ extraction-determinism workstream per builder report §"Architect-hat consult") is sound future-work; appropriate to NOT pull into 1.5-C scope.

## Gates

PR #322 cleared. Per dispatch + standing-directive autonomous merge: orchestrator may merge PR #322 + this verdict comm autonomously while owner asleep. After PR #322 merge, orchestrator authors **Phase 1.5-D.1 dispatch** (HU reference set design) per design memo §4.2 with α=β decided (architect-recommended; standing directive lean β); resolves the 988-corpus α/β gate before 1.5-D.1 fires. **LOOP CONTINUES** through 1.5-D.1 → 1.5-D.2 (HU labelling) → 1.5-D.3 (HU corpus) → 1.5-D.4 (HU retrain on 59) → 1.5-E (router/coaching) → Phase 2 D5.

## Cycle stats

- 44th solo QC cycle.
- Wall clock: ~15 min (matches dispatch heads-up).
- LLM cost: $0.

## References

- Builder PR #322 head: `45a5afb4a34c01435fe7d8f4ea7e54ca22b0ca03`
- 1.5-C dispatch: master `c8138a1` (PR #320)
- Re-poke fire-now: master `aa26ae4` (PR #321)
- Architect's design memo §3 (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- 12.5K-C-E precedent: `BUILDER_REPORT_PHASE125K_C_E_CORPUS_AND_RETRAIN_2026-05-07.md` (5-seed mean 33.00 ± 0.00)
- 1.5-B execution: master `8349a0b` (PR #315) + QC verdict `521bf36` (PR #319; PASS-WITH-FINDINGS · 0/0/1)
- Stay-wrong taxonomy: `project_v9_3way_ceiling.md` (memory)
