---
date: 2026-05-03
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · Owner · ML-ARCHITECT (advisory) · GTO-EXPERT (review) · QC stream
re: Phase 12.5D — v9 student trainer implementation + 5-seed run
status: BUILDER BLOCKED — implementation + 5-seed run complete; gate FAILED; model NOT promoted
---

# Phase 12.5D — v9 student trainer report

12.5D RUN COMPLETE BUT GATE FAILED. Median seed solver-corrected score is below v9-3way-v2.2 baseline; per dispatch stop condition the model was NOT promoted. Orchestrator decides next steps.

Master HEAD at run time: `e3c0dfcfd669099b29b1690b74d4e926a08e26f5`. Run timestamp (UTC): `2026-05-03T20:19:41Z`.

## Section A — training metadata

- Corpus: `data/corpus_revision_500_hand_2026-04-27.jsonl` (joined rows: 494)
- Labels: `data/corpus_revision_500_hand_labels_2026-04-27.jsonl`
- Warm-start requested: `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- Warm-start resolution: requested path IS git-tracked
- Warm-start resolved: `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- Pre-pad mode: `metadata_bump` (blueprint §4)
- Test size: 0.2
- Seeds: 0,1,2,3,4
- Confidence weighting: `pure`
- Reference set: `mw_11_50`

### Class label distribution (full corpus)

- FOLD: 72
- CHECK: 245
- CALL: 62
- BET: 86
- RAISE: 29

### Confidence histogram (full corpus)

- 1.0: 309
- 0.8: 109
- 0.6: 71
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
prepad: bumped num_feature 45 → 59 → /tmp/prepad_v9__ix1409b.json
```

### Schema discoveries surfaced during 12.5D

1. **Join key**: blueprint §6 + ml-architect §12 cited `corpus.source_situation_id == labels.ref_id` as the join key, verified on row 1. Subsequent rows (cohort 2, indices 100-493) have `situation_id` instead of `source_situation_id`, and `labels.ref_id` is heterogeneous (mix of `d####_POS_street` and `PILOT_###` IDs). The universally-populated canonical key is `pilot_hand_id` (494/494 in both files). Trainer joins on `pilot_hand_id`. Spec INTENT (494-hand training) is preserved.

2. **Path Y inference boundary**: `reference_evaluator.evaluate_variants` builds inference arrays via `gto_model.GtoOracle.features_from_dict` which iterates `gto_model.FEATURE_COLUMNS` (length 55). The student model expects 59 features. Path Y forbids extending `gto_model.FEATURE_COLUMNS`, so the student's reference-set evaluation uses an in-module 59-feature inference helper (`_StudentInference` + `_evaluate_student_one_hand`) that mirrors `reference_evaluator._evaluate_one_hand` logic with STUDENT_FEATURE_COLUMNS_V9. Baselines (38/45 features) continue to use `evaluate_variants` as-is.

### Per-seed training summary

|seed|train|test|acc|acc(weighted)|rounds|gate23 drop check|gate23 overfit check|
|---|---|---|---|---|---|---|---|
|0|395|99|0.919|0.932|434|WARN|PASS|
|1|395|99|0.889|0.910|929|WARN|PASS|
|2|395|99|0.899|0.915|793|WARN|PASS|
|3|395|99|0.919|0.932|267|WARN|PASS|
|4|395|99|0.889|0.915|279|WARN|PASS|
|mean|—|—|0.903±0.014|0.921±0.009|—|—|—|

Selected seed (median solver-corrected litmus): **seed 4**

### Held-out classification report (chosen seed)

|class|precision|recall|f1|support|
|---|---|---|---|---|
|FOLD|0.938|1.000|0.968|15|
|CHECK|0.939|0.939|0.939|49|
|CALL|0.769|0.833|0.800|12|
|BET|0.824|0.824|0.824|17|
|RAISE|0.750|0.500|0.600|6|

### Held-out confusion matrix (chosen seed; rows=true, cols=pred; class order = ACTION_CLASSES)

```
          FOLD  CHECK   CALL    BET  RAISE
  FOLD      15      0      0      0      0
 CHECK       0     46      0      3      0
  CALL       1      0     10      0      1
   BET       0      3      0     14      0
 RAISE       0      0      3      0      3
```

## Section B — reference-evaluator results (Gate 2.4)

Solver-correction overlay: applied to ['MW-30', 'MW-46', 'MW-47'] per `memory/reference_corrections.md`. MW-31, MW-50 NOT applied (unverified per blueprint §5.3).

### Per-seed student litmus (solver-corrected) — full sweep

|seed|raw|solver-corrected|
|---|---|---|
|0|32/40|31/40|
|1|31/40|30/40|
|2|31/40|30/40|
|3|32/40|31/40|
|4|32/40|31/40|
|mean|—|30.60/40 (std 0.49)|

### Chosen seed (4) cross-model litmus

|model|raw|solver-corrected|
|---|---|---|
|v9-student (chosen seed)|32/40|31/40|
|gto_model_v9_3way_v2.2.json|33/40|33/40|

### Solver-corrected per-hand comparison (chosen seed)

Only hands where any model differs from corrected expert OR where the correction overlay activates.

|ref_id|expert (raw)|solver-corrected expert|student|
|---|---|---|---|
|MW-17|CALL|CALL|FOLD|
|MW-24|BET|BET|CHECK|
|MW-25|BET|BET|CHECK|
|MW-30|CALL|CALL|CALL|
|MW-31|FOLD|FOLD|CALL|
|MW-40|BET|BET|CHECK|
|MW-42|BET|BET|CHECK|
|MW-45|RAISE|RAISE|CALL|
|MW-46|FOLD|CALL|RAISE|
|MW-47|CALL|RAISE|CALL|

### Per-class action distribution (chosen seed student)

|class|student count|
|---|---|
|FOLD|3|
|CHECK|12|
|CALL|17|
|BET|6|
|RAISE|2|

## Section C — Gate 2.3 feature importance (chosen seed)

Pass drop check (no feature <1% importance): **False**
Pass overfit check (no feature >30% importance): **True**

### v2.4 P1 blocker importances (the migration's load-bearing features)

|feature|importance|on drop list?|
|---|---|---|
|`nut_flush_block`|0.0000|YES — FLAG|
|`flush_draw_block_pct`|0.0107|no|
|`straight_draw_block_pct`|0.0071|YES — FLAG|
|`nut_made_block_pct`|0.0056|YES — FLAG|

### Top 15 features by importance (chosen seed)

|feature|importance|
|---|---|
|`facing_bet`|0.0828|
|`equity_margin`|0.0716|
|`is_paired`|0.0653|
|`raw_equity`|0.0617|
|`to_call`|0.0584|
|`is_monster`|0.0489|
|`equity_vs_range`|0.0460|
|`better_hand_pct`|0.0376|
|`is_strong_made`|0.0365|
|`bet_to_pot`|0.0362|
|`pot_odds`|0.0290|
|`hand_category`|0.0256|
|`villain_medium_made_pct`|0.0253|
|`worse_hand_pct`|0.0250|
|`is_ip`|0.0248|

### Below-1% drop list (chosen seed)

|feature|importance|
|---|---|
|`flush_block_pct`|0.0099|
|`num_opponents`|0.0099|
|`danger_score`|0.0096|
|`board_adjusted_hrp`|0.0087|
|`draw_outs`|0.0083|
|`straight_danger`|0.0082|
|`villain_draw_pct`|0.0081|
|`villain_fold_equity_estimate`|0.0079|
|`villain_aggression_count`|0.0075|
|`street`|0.0074|
|`high_card_rank`|0.0073|
|`straight_draw_block_pct`|0.0071|
|`is_rainbow`|0.0066|
|`connectivity_score`|0.0066|
|`is_two_tone`|0.0056|
|`nut_made_block_pct`|0.0056|
|`villain_position`|0.0047|
|`flush_draw_rank`|0.0034|
|`is_preflop_aggressor`|0.0032|
|`is_made_hand`|0.0000|
|`has_flush_draw`|0.0000|
|`has_straight_draw`|0.0000|
|`is_monotone`|0.0000|
|`is_double_paired`|0.0000|
|`is_3bet_pot`|0.0000|
|`villain_call_count`|0.0000|
|`villain_range_capped`|0.0000|
|`num_callers_to_bet`|0.0000|
|`facing_raise`|0.0000|
|`has_showdown_value`|0.0000|
|`nut_flush_block`|0.0000|

### Above-30% overfit warning list (chosen seed)

(none)

## Section D — provenance hashes

- Repo HEAD SHA: `e3c0dfcfd669099b29b1690b74d4e926a08e26f5`
- Trainer module: `river-rats-core/train_model_v9_student.py` (this PR)
- Warm-start anchor: `river-rats-core/models/gto_model_v9_3way_v2.2.json` SHA256: `9f3845bb2a56e99328261c70c3f34decd669f3e047162eb85c78f926bc366900`
- Output model: `river-rats-core/models/gto_model_v9_student.json` SHA256: `(no model promoted)`
- xgboost version: `3.2.0`
- numpy version: `2.4.3`
- Python version: `3.12.3`

## Stop-condition verification (dispatch §"Stop conditions")

| Stop condition | Status |
|---|---|
| Citation drift since blueprint pin `1fb0dea` | None (only comm files changed; verified pre-flight) |
| Pre-pad mechanism failure | NOT TRIGGERED — metadata-only succeeded |
| Median seed solver-corrected ≥ v9-3way-v2.2 | FAIL (31/40 vs 33/40) |
| 4-file deliverable diff | enforced by builder pre-PR `git diff --stat` check |

## References

- Dispatch directive: `review/comms/MAIN_TERMINAL_PHASE125D_DISPATCH_2026-05-03.md` (PR #125, master `e3c0dfc`)
- Blueprint: `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` (PR #122, master `1e4e47e`)
- Pivot directive: PR #119 (master `770b897`)
- ml-architect spec: PR #110 (master `291af80`)
- Solver corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`

**Status: 12.5D RUN COMPLETE. Median-litmus seed promoted to `/tmp/builder-12.5D-wt/river-rats-core/models/gto_model_v9_student.json`. Awaiting QC pre-merge audit + ml-architect/gto-expert review.**
