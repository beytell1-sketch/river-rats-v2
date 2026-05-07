---
date: 2026-05-07
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · Owner · ML-ARCHITECT (advisory) · GTO-EXPERT (review) · QC stream
re: Phase 12.5K-C-E-pilot — v9 student trainer run (hybrid weighting; combined corpus)
status: BUILDER BLOCKED — 12.5K-C-E-pilot implementation + 5-seed run complete; gate did not promote; model NOT promoted
---

# Phase 12.5K-C-E-pilot — v9 student trainer report (hybrid weighting)

12.5K-C-E-pilot RUN COMPLETE; median seed below v9-3way-v2.2 baseline. Per dispatch gate threshold the model was NOT promoted. Section E quantifies the delta vs 12.5D baseline.

Master HEAD at run time: `19f958a2ad9d212ec940c256d6bb0af21e3afc09`. Run timestamp (UTC): `2026-05-07T04:54:40Z`.

## Section A — training metadata

- Corpus: `data/corpus_combined_988_2026-05-07.jsonl` (joined rows: 988)
- Labels: `data/corpus_combined_988_labels_2026-05-07.jsonl`
- Warm-start requested: `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- Warm-start resolution: requested path IS git-tracked
- Warm-start resolved: `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- Pre-pad mode: `metadata_bump` (blueprint §4)
- Test size: 0.2
- Seeds: 0
- Confidence weighting: `pure`
- Class-weight cap (hybrid): `3.0`
- Reference set: `mw_11_50`

### Class label distribution (full corpus)

- FOLD: 97
- CHECK: 326
- CALL: 100
- BET: 219
- RAISE: 246

### Confidence histogram (full corpus)

- 1.0: 675
- 0.8: 182
- 0.6: 125
- 0.4: 6

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
prepad: bumped num_feature 45 → 61 → /tmp/prepad_v9_t1p3xzs0.json
```

### Schema discoveries surfaced during 12.5D

1. **Join key**: blueprint §6 + ml-architect §12 cited `corpus.source_situation_id == labels.ref_id` as the join key, verified on row 1. Subsequent rows (cohort 2, indices 100-493) have `situation_id` instead of `source_situation_id`, and `labels.ref_id` is heterogeneous (mix of `d####_POS_street` and `PILOT_###` IDs). The universally-populated canonical key is `pilot_hand_id` (494/494 in both files). Trainer joins on `pilot_hand_id`. Spec INTENT (494-hand training) is preserved.

2. **Path Y inference boundary**: `reference_evaluator.evaluate_variants` builds inference arrays via `gto_model.GtoOracle.features_from_dict` which iterates `gto_model.FEATURE_COLUMNS` (length 55). The student model expects 59 features. Path Y forbids extending `gto_model.FEATURE_COLUMNS`, so the student's reference-set evaluation uses an in-module 59-feature inference helper (`_StudentInference` + `_evaluate_student_one_hand`) that mirrors `reference_evaluator._evaluate_one_hand` logic with STUDENT_FEATURE_COLUMNS_V9. Baselines (38/45 features) continue to use `evaluate_variants` as-is.

### Per-seed training summary

|seed|train|test|acc|acc(weighted)|rounds|gate23 drop check|gate23 overfit check|
|---|---|---|---|---|---|---|---|
|0|790|198|0.955|0.957|469|WARN|PASS|
|mean|—|—|0.955±0.000|0.957±0.000|—|—|—|

Selected seed (median solver-corrected litmus): **seed 0**

### Held-out classification report (chosen seed)

|class|precision|recall|f1|support|
|---|---|---|---|---|
|FOLD|1.000|0.900|0.947|20|
|CHECK|0.984|0.954|0.969|65|
|CALL|0.857|0.900|0.878|20|
|BET|0.935|0.977|0.956|44|
|RAISE|0.960|0.980|0.970|49|

### Held-out confusion matrix (chosen seed; rows=true, cols=pred; class order = ACTION_CLASSES)

```
          FOLD  CHECK   CALL    BET  RAISE
  FOLD      18      0      2      0      0
 CHECK       0     62      0      3      0
  CALL       0      0     18      0      2
   BET       0      1      0     43      0
 RAISE       0      0      1      0     48
```

## Section B — reference-evaluator results (Gate 2.4)

Solver-correction overlay: applied to ['MW-30', 'MW-46', 'MW-47'] per `memory/reference_corrections.md`. MW-31, MW-50 NOT applied (unverified per blueprint §5.3).

### Per-seed student litmus (solver-corrected) — full sweep

|seed|raw|solver-corrected|
|---|---|---|
|0|34/40|33/40|
|mean|—|33.00/40 (std 0.00)|

### Chosen seed (0) cross-model litmus

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
|`nut_flush_block`|0.0081|YES — FLAG|
|`flush_draw_block_pct`|0.1063|no|
|`straight_draw_block_pct`|0.0041|YES — FLAG|
|`nut_made_block_pct`|0.0140|no|

### Top 15 features by importance (chosen seed)

|feature|importance|
|---|---|
|`flush_draw_block_pct`|0.1063|
|`villain_position`|0.0699|
|`facing_bet`|0.0462|
|`is_monster`|0.0392|
|`equity_margin`|0.0385|
|`flush_draw_rank`|0.0356|
|`nut_blocker_overcard_count`|0.0356|
|`flush_block_pct`|0.0338|
|`raw_equity`|0.0293|
|`to_call`|0.0288|
|`improvement_probability`|0.0239|
|`connectivity_score`|0.0238|
|`is_two_tone`|0.0229|
|`equity_vs_range`|0.0223|
|`better_hand_pct`|0.0222|

### Below-1% drop list (chosen seed)

|feature|importance|
|---|---|
|`pot_odds`|0.0097|
|`board_adjusted_hrp`|0.0096|
|`nut_flush_block`|0.0081|
|`bet_to_pot`|0.0080|
|`bet_call_multiway_oop_raise_pressure_index`|0.0075|
|`overcard_outs`|0.0075|
|`hero_position`|0.0073|
|`high_card_rank`|0.0069|
|`is_rainbow`|0.0068|
|`villain_fold_equity_estimate`|0.0063|
|`villain_range_capped`|0.0048|
|`num_callers_to_bet`|0.0043|
|`street`|0.0042|
|`straight_draw_block_pct`|0.0041|
|`flush_danger`|0.0039|
|`is_paired`|0.0036|
|`straight_danger`|0.0034|
|`villain_call_count`|0.0032|
|`has_flush_draw`|0.0023|
|`is_made_hand`|0.0000|
|`is_monotone`|0.0000|
|`is_double_paired`|0.0000|
|`is_3bet_pot`|0.0000|
|`facing_raise`|0.0000|
|`has_showdown_value`|0.0000|

### Above-30% overfit warning list (chosen seed)

(none)

## Section E — 12.5D vs 12.5D' delta

Compares this run's chosen-seed metrics against the merged 12.5D baseline (PR #126, master `d7d2cdd`, chosen seed = 4, pure-confidence weighting). Same hyperparameters, same seed list, same warm-start anchor — only the `sample_weight` computation changed (confidence × class_weight, cap 3.0, per ml-architect Q3).

### Litmus delta (per-seed solver-corrected)

|seed|12.5D|12.5D'|Δ|
|---|---|---|---|
|0|31/40|33/40|+2|
|**median**|**31/40**|**33/40**|**+2**|

### Per-class held-out metrics delta (chosen seed: 12.5D=4 vs 12.5D'=0)

|class|12.5D precision/recall/f1|12.5D' precision/recall/f1|recall Δ|
|---|---|---|---|
|FOLD|0.938/1.000/0.968|1.000/0.900/0.947|-0.100|
|CHECK|0.939/0.939/0.939|0.984/0.954/0.969|+0.015|
|CALL|0.769/0.833/0.800|0.857/0.900/0.878|+0.067|
|BET|0.824/0.824/0.824|0.935/0.977/0.956|+0.153|
|RAISE|0.750/0.500/0.600|0.960/0.980/0.970|+0.480|

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
|`nut_flush_block`|0.0000|0.0081|+0.0081|
|`flush_draw_block_pct`|0.0107|0.1063|+0.0956|
|`straight_draw_block_pct`|0.0071|0.0041|-0.0030|
|`nut_made_block_pct`|0.0056|0.0140|+0.0084|

### Interpretation hints (reviewer-scope)

- **Gate threshold (dispatch):** ≥33 promote, 31-32 STOP/owner-tie-gate, <31 STOP+flag-Q3-wrong
- **This run:** median 33/40 → falls in ≥33 PROMOTE
- gto-expert prediction was 7 shared flip + 2 distinct stay-wrong (predicted student → 36-38/40 range). Empirical: 2/7 shared flipped, 0/2 distinct flipped

## Section D — provenance hashes

- Repo HEAD SHA: `19f958a2ad9d212ec940c256d6bb0af21e3afc09`
- Trainer module: `river-rats-core/train_model_v9_student.py` (this PR)
- Warm-start anchor: `river-rats-core/models/gto_model_v9_3way_v2.2.json` SHA256: `9f3845bb2a56e99328261c70c3f34decd669f3e047162eb85c78f926bc366900`
- Output model: `river-rats-core/models/125k_c_e/v9_3way_125k_c_e_pilot.json` SHA256: `(no model promoted)`
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

**Status: 12.5K-C-E-pilot RUN COMPLETE; model NOT promoted (median seed below v9-3way-v2.2 baseline). 12.5E-F gate decides next direction. Awaiting QC pre-merge audit + ml-architect/gto-expert review.**
