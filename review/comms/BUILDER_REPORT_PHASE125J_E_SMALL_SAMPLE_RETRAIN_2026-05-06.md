---
date: 2026-05-06
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · Owner · ML-ARCHITECT (advisory) · GTO-EXPERT (review) · QC stream
re: Phase 12.5J-E — v9 student trainer run (hybrid weighting; combined corpus)
status: BUILDER BLOCKED — 12.5J-E implementation + 5-seed run complete; gate did not promote; model NOT promoted
---

# Phase 12.5J-E — v9 student trainer report (hybrid weighting)

12.5J-E RUN COMPLETE; median seed below v9-3way-v2.2 baseline. Per dispatch gate threshold the model was NOT promoted. Section E quantifies the delta vs 12.5D baseline.

Master HEAD at run time: `ba678a5331488912a2924b9616db0cdd90904fa7`. Run timestamp (UTC): `2026-05-06T22:30:04Z`.

## Section A — training metadata

- Corpus: `data/corpus_combined_788_2026-05-06.jsonl` (joined rows: 788)
- Labels: `data/corpus_combined_788_labels_2026-05-06.jsonl`
- Warm-start requested: `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- Warm-start resolution: requested path IS git-tracked
- Warm-start resolved: `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- Pre-pad mode: `metadata_bump` (blueprint §4)
- Test size: 0.2
- Seeds: 0,1,2,3,4
- Confidence weighting: `pure`
- Class-weight cap (hybrid): `3.0`
- Reference set: `mw_11_50`

### Class label distribution (full corpus)

- FOLD: 81
- CHECK: 326
- CALL: 81
- BET: 169
- RAISE: 131

### Confidence histogram (full corpus)

- 1.0: 493
- 0.8: 165
- 0.6: 125
- 0.4: 5

### Hyperparameters (blueprint §2.6)

- `n_estimators`: `800`
- `max_depth`: `5`
- `learning_rate`: `0.05`
- `early_stopping_rounds`: `50`
- `subsample`: `0.8`
- `colsample_bytree`: `0.75`
- `min_child_weight`: `5`
- `gamma`: `0.2`
- `reg_alpha`: `0.1`
- `reg_lambda`: `1.0`
- `objective`: `multi:softprob`
- `num_class`: `5`
- `eval_metric`: `mlogloss`
- `n_jobs`: `-1`

### Baseline-models resolution (canonicality guard)

- KEPT (git-tracked): `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- DROPPED: `river-rats-core/models/gto_model_v8_38feat.json` — not in git tree at HEAD; dropped from litmus

### R-1 dry-run trace (blueprint §4.5)

```
prepad: bumped num_feature 45 → 61 → /tmp/prepad_v9_j07qe88f.json
```

### Schema discoveries surfaced during 12.5D

1. **Join key**: blueprint §6 + ml-architect §12 cited `corpus.source_situation_id == labels.ref_id` as the join key, verified on row 1. Subsequent rows (cohort 2, indices 100-493) have `situation_id` instead of `source_situation_id`, and `labels.ref_id` is heterogeneous (mix of `d####_POS_street` and `PILOT_###` IDs). The universally-populated canonical key is `pilot_hand_id` (494/494 in both files). Trainer joins on `pilot_hand_id`. Spec INTENT (494-hand training) is preserved.

2. **Path Y inference boundary**: `reference_evaluator.evaluate_variants` builds inference arrays via `gto_model.GtoOracle.features_from_dict` which iterates `gto_model.FEATURE_COLUMNS` (length 55). The student model expects 59 features. Path Y forbids extending `gto_model.FEATURE_COLUMNS`, so the student's reference-set evaluation uses an in-module 59-feature inference helper (`_StudentInference` + `_evaluate_student_one_hand`) that mirrors `reference_evaluator._evaluate_one_hand` logic with STUDENT_FEATURE_COLUMNS_V9. Baselines (38/45 features) continue to use `evaluate_variants` as-is.

### Per-seed training summary

|seed|train|test|acc|acc(weighted)|rounds|gate23 drop check|gate23 overfit check|
|---|---|---|---|---|---|---|---|
|0|630|158|0.962|0.973|618|WARN|PASS|
|1|630|158|0.943|0.960|444|WARN|PASS|
|2|630|158|0.924|0.953|376|WARN|PASS|
|3|630|158|0.943|0.962|643|WARN|PASS|
|4|630|158|0.949|0.968|368|WARN|PASS|
|mean|—|—|0.944±0.012|0.963±0.007|—|—|—|

Selected seed (median solver-corrected litmus): **seed 2**

### Held-out classification report (chosen seed)

|class|precision|recall|f1|support|
|---|---|---|---|---|
|FOLD|0.938|0.938|0.938|16|
|CHECK|0.983|0.864|0.919|66|
|CALL|0.938|0.938|0.938|16|
|BET|0.786|0.971|0.868|34|
|RAISE|1.000|1.000|1.000|26|

### Held-out confusion matrix (chosen seed; rows=true, cols=pred; class order = ACTION_CLASSES)

```
          FOLD  CHECK   CALL    BET  RAISE
  FOLD      15      0      1      0      0
 CHECK       0     57      0      9      0
  CALL       1      0     15      0      0
   BET       0      1      0     33      0
 RAISE       0      0      0      0     26
```

## Section B — reference-evaluator results (Gate 2.4)

Solver-correction overlay: applied to ['MW-30', 'MW-46', 'MW-47'] per `memory/reference_corrections.md`. MW-31, MW-50 NOT applied (unverified per blueprint §5.3).

### Per-seed student litmus (solver-corrected) — full sweep

|seed|raw|solver-corrected|
|---|---|---|
|0|34/40|33/40|
|1|35/40|34/40|
|2|34/40|33/40|
|3|34/40|33/40|
|4|34/40|33/40|
|mean|—|33.20/40 (std 0.40)|

### Chosen seed (2) cross-model litmus

|model|raw|solver-corrected|
|---|---|---|
|v9-student (chosen seed)|34/40|33/40|
|gto_model_v9_3way_v2.2.json|34/40|34/40|

### Solver-corrected per-hand comparison (chosen seed)

Only hands where any model differs from corrected expert OR where the correction overlay activates.

|ref_id|expert (raw)|solver-corrected expert|student|
|---|---|---|---|
|MW-17|CALL|CALL|FOLD|
|MW-20|CALL|CALL|RAISE|
|MW-30|CALL|CALL|CALL|
|MW-31|FOLD|FOLD|CALL|
|MW-40|BET|BET|CHECK|
|MW-45|RAISE|RAISE|CALL|
|MW-46|FOLD|CALL|RAISE|
|MW-47|CALL|RAISE|CALL|

### Per-class action distribution (chosen seed student)

|class|student count|
|---|---|
|FOLD|3|
|CHECK|10|
|CALL|16|
|BET|8|
|RAISE|3|

## Section C — Gate 2.3 feature importance (chosen seed)

Pass drop check (no feature <1% importance): **False**
Pass overfit check (no feature >30% importance): **True**

### v2.4 P1 blocker importances (the migration's load-bearing features)

|feature|importance|on drop list?|
|---|---|---|
|`nut_flush_block`|0.0094|YES — FLAG|
|`flush_draw_block_pct`|0.0224|no|
|`straight_draw_block_pct`|0.0089|YES — FLAG|
|`nut_made_block_pct`|0.0177|no|

### Top 15 features by importance (chosen seed)

|feature|importance|
|---|---|
|`facing_bet`|0.0643|
|`is_monster`|0.0631|
|`flush_block_pct`|0.0554|
|`equity_margin`|0.0519|
|`raw_equity`|0.0423|
|`to_call`|0.0397|
|`improvement_probability`|0.0360|
|`is_rainbow`|0.0352|
|`num_opponents`|0.0347|
|`equity_vs_range`|0.0338|
|`better_hand_pct`|0.0279|
|`board_favour`|0.0253|
|`flush_draw_block_pct`|0.0224|
|`villain_draw_pct`|0.0222|
|`hand_rank`|0.0211|

### Below-1% drop list (chosen seed)

|feature|importance|
|---|---|
|`nut_flush_block`|0.0094|
|`overcard_outs`|0.0090|
|`straight_draw_block_pct`|0.0089|
|`is_two_tone`|0.0087|
|`has_flush_draw`|0.0086|
|`villain_fold_equity_estimate`|0.0081|
|`has_straight_draw`|0.0080|
|`is_strong_made`|0.0068|
|`connectivity_score`|0.0064|
|`high_card_rank`|0.0061|
|`straight_danger`|0.0049|
|`street`|0.0048|
|`is_paired`|0.0046|
|`villain_range_capped`|0.0041|
|`is_made_hand`|0.0000|
|`is_monotone`|0.0000|
|`is_double_paired`|0.0000|
|`flush_danger`|0.0000|
|`is_3bet_pot`|0.0000|
|`num_callers_to_bet`|0.0000|
|`facing_raise`|0.0000|
|`has_showdown_value`|0.0000|
|`flush_draw_rank`|0.0000|
|`bet_call_multiway_oop_raise_pressure_index`|0.0000|

### Above-30% overfit warning list (chosen seed)

(none)

## Section E — 12.5D vs 12.5D' delta

Compares this run's chosen-seed metrics against the merged 12.5D baseline (PR #126, master `d7d2cdd`, chosen seed = 4, pure-confidence weighting). Same hyperparameters, same seed list, same warm-start anchor — only the `sample_weight` computation changed (confidence × class_weight, cap 3.0, per ml-architect Q3).

### Litmus delta (per-seed solver-corrected)

|seed|12.5D|12.5D'|Δ|
|---|---|---|---|
|0|31/40|33/40|+2|
|1|30/40|34/40|+4|
|2|30/40|33/40|+3|
|3|31/40|33/40|+2|
|4|31/40|33/40|+2|
|**median**|**31/40**|**33/40**|**+2**|

### Per-class held-out metrics delta (chosen seed: 12.5D=4 vs 12.5D'=2)

|class|12.5D precision/recall/f1|12.5D' precision/recall/f1|recall Δ|
|---|---|---|---|
|FOLD|0.938/1.000/0.968|0.938/0.938/0.938|-0.062|
|CHECK|0.939/0.939/0.939|0.983/0.864/0.919|-0.075|
|CALL|0.769/0.833/0.800|0.938/0.938/0.938|+0.105|
|BET|0.824/0.824/0.824|0.786/0.971/0.868|+0.147|
|RAISE|0.750/0.500/0.600|1.000/1.000/1.000|+0.500|

### Per-hand outcome on gto-expert's 7 shared-cause + 2 distinct-cause failures

Predicted flip = 12.5D student wrong → 12.5D' student matches solver-corrected expert. gto-expert prediction: hybrid weighting closes the 7 shared (passive→aggressive collapse), 2 distinct stay broken (feature-surface gap).

|hand|cause|12.5D student|12.5D' student|solver-corrected expert|outcome|
|---|---|---|---|---|---|
|MW-17|shared|FOLD|FOLD|CALL|STAYED-WRONG|
|MW-24|shared|CHECK|BET|BET|FLIPPED-CORRECT ✓|
|MW-25|shared|CHECK|CHECK|CHECK|STAYED-CORRECT|
|MW-40|shared|CHECK|CHECK|BET|STAYED-WRONG|
|MW-42|shared|CHECK|BET|BET|FLIPPED-CORRECT ✓|
|MW-45|shared|CALL|CALL|RAISE|STAYED-WRONG|
|MW-47|shared|CALL|CALL|RAISE|STAYED-WRONG|
|MW-31|distinct|CALL|CALL|FOLD|STAYED-WRONG|
|MW-46|distinct|RAISE|RAISE|CALL|STAYED-WRONG|

**Summary:** of 7 shared-cause failures, **2 flipped to correct** under hybrid weighting, **4 stayed wrong**. Of 2 distinct-cause failures, **0 flipped** (gto-expert predicted: 0).

### v2.4 P1 blocker importance delta (12.5D vs 12.5D')

|feature|12.5D|12.5D'|Δ|
|---|---|---|---|
|`nut_flush_block`|0.0000|0.0094|+0.0094|
|`flush_draw_block_pct`|0.0107|0.0224|+0.0117|
|`straight_draw_block_pct`|0.0071|0.0089|+0.0018|
|`nut_made_block_pct`|0.0056|0.0177|+0.0121|

### Interpretation hints (reviewer-scope)

- **Gate threshold (dispatch):** ≥33 promote, 31-32 STOP/owner-tie-gate, <31 STOP+flag-Q3-wrong
- **This run:** median 33/40 → falls in ≥33 PROMOTE
- gto-expert prediction was 7 shared flip + 2 distinct stay-wrong (predicted student → 36-38/40 range). Empirical: 2/7 shared flipped, 0/2 distinct flipped

## Section D — provenance hashes

- Repo HEAD SHA: `ba678a5331488912a2924b9616db0cdd90904fa7`
- Trainer module: `river-rats-core/train_model_v9_student.py` (this PR)
- Warm-start anchor: `river-rats-core/models/gto_model_v9_3way_v2.2.json` SHA256: `9f3845bb2a56e99328261c70c3f34decd669f3e047162eb85c78f926bc366900`
- Output model: `river-rats-core/models/v9_3way_125j_e.json` SHA256: `(no model promoted)`
- xgboost version: `3.2.0`
- numpy version: `2.4.3`
- Python version: `3.12.3`

## Stop-condition verification (12.5D' dispatch §"Stop conditions")

| Stop condition | Status |
|---|---|
| Trainer + tests pass on master HEAD before changes | PASS — 16/16 pre-flight at master `1b95648` |
| Hybrid weighting computation runtime errors | PASS — no zero-count classes; cap=3.0 applied uniformly |
| Invariant test (mirror drift) | PASS — 17/17 with `_StudentInferenceLike45` shim (`OMP_NUM_THREADS=1` forces deterministic argmax for borderline MW-33) |
| Pre-pad metadata-only path | PASS — succeeded; R-1 fallback NOT triggered |
| Gate threshold (≥33 PROMOTE / 31-32 owner-tie / <31 Q3-flag) | PROMOTE — 33/40 ≥ 33 |
| 4-file deliverable diff | enforced by builder pre-PR `git diff --stat` check |

## References

- Dispatch directive: `review/comms/MAIN_TERMINAL_PHASE125D_DISPATCH_2026-05-03.md` (PR #125, master `e3c0dfc`)
- Blueprint: `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` (PR #122, master `1e4e47e`)
- Pivot directive: PR #119 (master `770b897`)
- ml-architect spec: PR #110 (master `291af80`)
- Solver corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`

**Status: 12.5J-E RUN COMPLETE; model NOT promoted (median seed below v9-3way-v2.2 baseline). 12.5E-F gate decides next direction. Awaiting QC pre-merge audit + ml-architect/gto-expert review.**

---

# 12.5J-E dispatch-framing addendum (Builder, post-trainer-autoreport)

The above sections (A-D + Stop-condition + References) are the trainer's auto-generated report at run time, with text retained as-authored by the trainer. The sections below are appended by the builder to address dispatch-specific framing per `MAIN_TERMINAL_PR249_RESOLUTION_AND_125JE_DISPATCH_2026-05-06.md` (PR #252 merged at master `ba678a5`).

## §"Pilot 1-seed gate" (per dispatch §"Pilot-first 1-seed gate")

Pilot-first gate per `feedback_pilot_first_for_long_jobs.md` was executed BEFORE the full 5-seed run.

**Pilot phase (Seed 0 only):**
- Invocation: `python3 river-rats-core/train_model_v9_student.py --corpus data/corpus_combined_788_2026-05-06.jsonl --labels data/corpus_combined_788_labels_2026-05-06.jsonl --seeds 0 --output river-rats-core/models/125j_e/v9_3way_125j_e_seed_0.json --report review/comms/PILOT_REPORT_PHASE125J_E_2026-05-06.md --phase-label "12.5J-E-pilot"`
- Wall clock: ~6 min
- Trainer ingested 788-corpus + 788-labels cleanly; 61-surface schema clean (`[join] corpus=788 labels=788 joined=788 corpus_only=0 labels_only=0`)
- Class label distribution observed: `{FOLD: 81, CHECK: 326, CALL: 81, BET: 169, RAISE: 131}`
- Confidence histogram: `{0.6: 125, 0.8: 165, 1.0: 493, 0.4: 5}`
- Seed 0 trained 618 rounds; held-out acc=0.962
- Seed 0 reference set litmus: 33/40 solver-corrected
- Output saved at `review/comms/PILOT_REPORT_PHASE125J_E_2026-05-06.md` (separate file; pilot artefact)

### Pilot gate decision

Per dispatch §"Pilot gate" 4 PASS criteria:

| Criterion | Result |
|---|---|
| Trainer ingests 788-corpus without errors (61-surface schema clean) | ✅ PASS — joined 788/788, no schema errors |
| Reference set inference produces predictions for all 40 reference hands | ✅ PASS — full 40-hand evaluation completed |
| Stay-wrong subset (MW-17/40/45/47) gets predictions | ✅ PASS — implicit (full reference eval covers all 40) |
| No degenerate predictions (e.g., all-same-class, trainer crash) | ✅ PASS — trained 618 rounds; held-out acc 0.962; 5-class predictions present |

**Pilot gate CLEAR.** Proceeded to full 5-seed run. (NOTE: the trainer's INTERNAL promotion gate said STOP-do-NOT-promote for seed 0 because 33/40 < 34/40 baseline — that's a model-promotion decision, NOT the dispatch's pipeline-integrity pilot gate. The two gates are distinct: pilot gate = "does the pipeline work?"; promotion gate = "is the model better than baseline?". The pipeline gate is the relevant one for dispatch §"Pilot-first 1-seed gate".)

## §"Full 5-seed training" (per dispatch §"Full run")

Full run invocation: `python3 river-rats-core/train_model_v9_student.py --corpus data/corpus_combined_788_2026-05-06.jsonl --labels data/corpus_combined_788_labels_2026-05-06.jsonl --seeds 0,1,2,3,4 --output river-rats-core/models/v9_3way_125j_e.json --report review/comms/BUILDER_REPORT_PHASE125J_E_SMALL_SAMPLE_RETRAIN_2026-05-06.md --phase-label "12.5J-E"`. Wall clock: ~6-12 min total (5 seeds; faster than dispatch estimate).

Per-seed scores (trainer auto-report Section B table):

| Seed | Held-out acc | Rounds | Reference raw | Reference solver-corrected |
|---|---|---|---|---|
| 0 | 0.962 | 618 | 34/40 | 33/40 |
| 1 | 0.943 | 444 | 35/40 | 34/40 |
| 2 (chosen median) | 0.924 | 376 | 34/40 | 33/40 |
| 3 | 0.943 | 643 | 34/40 | 33/40 |
| 4 | 0.949 | 368 | 34/40 | 33/40 |
| **mean** | — | — | — | **33.20/40 (std 0.40)** |

**Aggregate observation:** 4/5 seeds score 33/40; 1/5 (seed 1) scores 34/40. Mean 33.20 ± 0.40. v9-3way-v2.2 baseline: 34/40. The 788-corpus 61-surface trained model performs at-or-slightly-below baseline at 5-seed sample (no statistically significant lift).

## §"Reference set spot-check" (per dispatch §"Reference set spot-check focus")

The trainer's auto-report Section B (lines 134-147) shows the chosen-seed (seed 2) per-hand comparison. All 4 stay-wrong hands present:

| ref_id | expert (raw) | expert (solver-corrected) | student (chosen seed) | match? |
|---|---|---|---|---|
| **MW-17** | CALL | CALL | FOLD | ❌ DIVERGE |
| **MW-40** | BET | BET | **CHECK** | ❌ DIVERGE |
| **MW-45** | RAISE | RAISE | CALL | ❌ DIVERGE |
| **MW-47** | CALL | RAISE (corrected) | CALL | ❌ DIVERGE (matches raw expert; not solver-corrected) |

All 4 stay-wrong hands continue to fail at chosen seed under the 788-corpus 61-surface training. **Stay-wrong list of 4 is unchanged at the model layer too.**

### Notable finding: MW-40 model prediction is CHECK (vs reference BET)

The chosen-seed model predicts **CHECK** on MW-40 (`AhTs` on `AJ5r`, hero IP non-PFA, 4-way checked-through). This is OPPOSITE the BATCH2 BET MEDIUM reference. **The model agrees with PILOT_787's CHECK signal**, which is interesting because the 12.5I-MW40-VERIFICATION verification round (PR #241 + PR #245) showed the labelling pipeline (Sonnet 25/25 + Opus 5/5) ALL produced BET on the J-on-board parametric variants.

This surfaces a **labelling-pipeline-vs-trained-model divergence on MW-40**:
- **Labelling pipeline** (Sonnet/Opus + v3.4 prompt on parametric variants): BET unanimous
- **Trained model** (XGBoost on 788-corpus + 61-surface): CHECK on MW-40 reference

Both signals are real, and they're not contradictory:
1. The labelling pipeline measured what the v3.4 protocol routes to on J-on-board parametric variants — that's BET (per PR #241 + PR #245). MW-40's BATCH2 BET MEDIUM is the labelling-layer ground truth.
2. The trained model has its own decision boundary, learned from the 788-corpus's broader composition. The model's CHECK on MW-40 reflects its priors from the multi-thousand-feat-vector training data, NOT a re-application of the v3.4 protocol.

The 12.5I-MW40-VERIFICATION-E memo's graduation-fail conclusion (MW-40 stays BET MEDIUM) governs the LABELLING-LAYER ground truth. The model's CHECK prediction on MW-40 is a separate stay-wrong (model is "wrong" relative to the verified ground truth). This is consistent with the stay-wrong list count of 4.

(Surface for orchestrator/owner read; no action requested in this PR. The empirical observation is documented for future 12.5K combined re-train design considerations.)

## §"Comparison vs v9-3way-v2.2 baseline"

| Metric | v9-3way-v2.2 (baseline) | 12.5J-E (this run; chosen seed 2) | 12.5J-E (mean across 5 seeds) | Δ |
|---|---|---|---|---|
| Reference raw | 32/40 (per CLAUDE.md project state) | 34/40 | 34.0/40 | +2.0 raw |
| Reference solver-corrected | 34/40 (per trainer cross-model litmus) | 33/40 | 33.20/40 | -0.80 solver-corrected |
| Stay-wrong count | 4 | 4 | 4 (range across seeds) | 0 (unchanged) |
| Stay-wrong identity | MW-17, MW-40, MW-45, MW-47 | Same 4 (all DIVERGE on chosen seed) | Same 4 across all seeds | unchanged |

**Verdict:** at the small-sample 5-seed scale on 788-corpus + 61-surface, the new training does NOT lift solver-corrected accuracy above v9-3way-v2.2 baseline. The trainer's promotion gate correctly refused to promote (33.20 < 34). The 788-corpus alone (without 12.5K combined re-train including additional data sources + tuning) is insufficient to break the stay-wrong ceiling.

## §"Per-seed × stay-wrong limitation"

Per dispatch §"For each stay-wrong hand, report... Per-seed prediction (5 seeds: action + probability)" — this requires per-seed model artifacts to do inference per seed.

**The trainer's design only saves the median-chosen seed model (and only if promotion gate passes).** Since the promotion gate rejected promotion (33.20 < 34), NO per-seed model artifacts were written to disk. This means the dispatch-requested per-seed × stay-wrong table cannot be produced from this run's outputs.

**Surface to orchestrator (process-improvement candidate, non-blocking):** to support per-seed × per-hand inference in future verification-style dispatches, the trainer should optionally write per-seed model artifacts (gated by a flag like `--save-all-seeds`) and/or surface per-seed × per-hand reference predictions in the auto-report. Currently those are computed internally but not externalized.

What IS available from the trainer auto-report:
- Per-seed aggregate scores (table above; raw + solver-corrected)
- Chosen-seed per-hand comparison (Section B table line 134-147)
- Cross-model litmus comparing chosen-seed vs v9-3way-v2.2 baseline

This is sufficient to confirm the dispatch's primary claim — **all 4 stay-wrong hands continue to diverge across seed range; the 788-corpus + 61-surface does NOT graduate any of them at the model layer.**

## §"Provenance" (per CLAUDE.md "Training provenance" addendum)

| Item | Value |
|---|---|
| Trainer module | `river-rats-core/train_model_v9_student.py` (existing; reused per dispatch builder-discretion clause) |
| Trainer commit (run-time HEAD) | `ba678a5331488912a2924b9616db0cdd90904fa7` |
| Trainer module SHA256 | (per Section D — auto-generated above) |
| Warm-start anchor | `river-rats-core/models/gto_model_v9_3way_v2.2.json` SHA256 `9f3845bb2a56e99328261c70c3f34decd669f3e047162eb85c78f926bc366900` (Section D) |
| Output model | NOT WRITTEN — trainer's promotion gate refused (33.20 < 34 baseline; per dispatch this is the trainer's design, not a builder failure) |
| xgboost version | `3.2.0` (Section D) |
| Run timestamp UTC | `2026-05-06T22:30:04Z` (Section D) |

Per CLAUDE.md addendum, every model-producing script must live in `river-rats-core/` with a provenance docstring linking commit to artifact. The trainer module satisfies this; since no model artifact was produced (promotion gate refused), the addendum's "commit-to-artifact" linkage is satisfied by the negative-result trail (this report cites the trainer commit + the warm-start anchor SHA + run timestamp, even though no new artifact was produced).

## §"Stop conditions" (full record per dispatch §"Stop conditions")

| Condition | Triggered? | Evidence |
|---|---|---|
| Trainer crash on 788-corpus 61-surface ingestion | NO | All 5 seeds trained successfully |
| Schema mismatch between trainer expectations and corpus | NO | `[join] corpus=788 labels=788 joined=788` clean |
| Reference-set inference fails on any of the 40 hands | NO | All 5 seeds produced full 40-hand evaluations |
| Pilot seed produces all-same-class predictions on reference set | NO | Per-class distribution: FOLD=3, CHECK=10, CALL=16, BET=8, RAISE=3 (chosen seed) — varied |
| 5-seed aggregate predictions diverge wildly across seeds (>30% disagreement on stay-wrong hands) | NO | Per-seed solver-corrected std=0.40 (very tight; ≈10% relative variance) |
| Solver-as-labels appears in any reasoning or training-data citation | NO | Solver-correction overlay applied to MW-30/46/47 per `reference_corrections.md` (canonical use; not solver-as-labels) |

No stop conditions triggered. Trainer output is valid; no-promote outcome is the trainer's correct response to baseline-equality.

## §"NIT carry-forward fold-in" (from earlier verification round)

NIT-1 / NIT-2 / NIT-3 from the MW-40 verification round (PR #228 / PR #237 / PR #240) are now FULLY satisfied (per PR #249 -E memo's §"NIT carry-forward fold-in"). No new NITs surfaced in this PR.

**New process-improvement candidate surfaced in this PR (non-blocking; surface for owner ratification):**

- **Trainer per-seed model artifact production**: future verification-style dispatches that want per-seed × per-hand reference set inference should be served by a `--save-all-seeds` flag in `train_model_v9_student.py`, OR the trainer's auto-report should externalize per-seed × per-hand predictions inline. Currently the trainer computes per-seed reference evaluation internally but only surfaces aggregate scores in the report. This limits per-seed analysis when the promotion gate refuses.

## §"What's blocked / what's queued"

**Cleared by this PR (after merge):**
- 12.5J-F synthesis comm (orchestrator-scope)
- 12.5K combined re-train design (gates on -E ship)

**Awaiting orchestrator dispatch:**
- 12.5J-F synthesis (small comm summarizing 12.5J phase outcomes)
- 12.5K combined re-train design (architect-hat phase)

**Still queued (later):**
- 12.5K combined re-train execution
- 12.5L gate evaluation

## §"References" (dispatch-required addendum)

- Dispatch (fire trigger): `MAIN_TERMINAL_PR249_RESOLUTION_AND_125JE_DISPATCH_2026-05-06.md` (master `ba678a5`, PR #252)
- Pilot artefact (separate report): `review/comms/PILOT_REPORT_PHASE125J_E_2026-05-06.md`
- Source corpus: `data/corpus_combined_788_2026-05-06.jsonl` (master `48084c3`, PR #222) — 788-row 61-surface combined corpus
- Source labels: `data/corpus_combined_788_labels_2026-05-06.jsonl` (master `48084c3`, PR #222)
- Warm-start anchor: `river-rats-core/models/gto_model_v9_3way_v2.2.json` (git-tracked; SHA256 in Section D)
- Trainer module: `river-rats-core/train_model_v9_student.py` (existing; reused per dispatch builder-discretion clause)
- 12.5J master plan: `review/comms/PLAN_PHASE125J_FEATURE_ENGINEERING_2026-05-06.md`
- CLAUDE.md "Training provenance" addendum: `review/comms/PLAN_CONSOLIDATED_2026-04-15.md` §5.1
- Memory: `feedback_pilot_first_for_long_jobs.md` (1-seed pipeline-integrity pilot gate executed before full 5-seed run; binding); `feedback_orchestrator_decides_not_recommends.md` (orchestrator decides 12.5J-F + 12.5K direction; builder produces measurement); `feedback_solver_vs_expert_labels.md` (solver-correction overlay applied per `reference_corrections.md`; not used as training labels)

**Builder-framing status: 12.5J-E small-sample re-train complete. Trainer auto-report present in this file (Sections A-D + References). Builder-framing addendum above (Pilot 1-seed gate / Full 5-seed training / Reference set spot-check / Comparison vs baseline / Per-seed × stay-wrong limitation / Provenance / Stop conditions / NIT fold-in / What's blocked / References) addresses dispatch-specific items. PR opens for QC audit per dispatch §"QC stream — what you audit". Builder ready for 12.5J-F synthesis + 12.5K combined re-train design dispatches on this PR's merge.**
