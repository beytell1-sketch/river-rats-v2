---
date: 2026-05-04
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · Owner · ML-ARCHITECT (advisory) · GTO-EXPERT (review) · QC stream
re: Phase 12.5D' — v9 student trainer hybrid weighting (C') run
status: BUILDER BLOCKED — 12.5D' implementation + 5-seed run complete; gate did not promote; model NOT promoted
---

# Phase 12.5D' — v9 student trainer report (hybrid weighting)

12.5D' RUN COMPLETE; median seed below v9-3way-v2.2 baseline. Per dispatch gate threshold the model was NOT promoted. Section E quantifies the delta vs 12.5D baseline.

Master HEAD at run time: `1b95648a2df9bc3f3908b22c08c2841a7c9fb933`. Run timestamp (UTC): `2026-05-04T02:55:35Z`.

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
prepad: bumped num_feature 45 → 59 → /tmp/prepad_v9_4adkfrq1.json
```

### Schema discoveries surfaced during 12.5D'

1. **Join key**: blueprint §6 + ml-architect §12 cited `corpus.source_situation_id == labels.ref_id` as the join key, verified on row 1. Subsequent rows (cohort 2, indices 100-493) have `situation_id` instead of `source_situation_id`, and `labels.ref_id` is heterogeneous (mix of `d####_POS_street` and `PILOT_###` IDs). The universally-populated canonical key is `pilot_hand_id` (494/494 in both files). Trainer joins on `pilot_hand_id`. Spec INTENT (494-hand training) is preserved.

2. **Path Y inference boundary**: `reference_evaluator.evaluate_variants` builds inference arrays via `gto_model.GtoOracle.features_from_dict` which iterates `gto_model.FEATURE_COLUMNS` (length 55). The student model expects 59 features. Path Y forbids extending `gto_model.FEATURE_COLUMNS`, so the student's reference-set evaluation uses an in-module 59-feature inference helper (`_StudentInference` + `_evaluate_student_one_hand`) that mirrors `reference_evaluator._evaluate_one_hand` logic with STUDENT_FEATURE_COLUMNS_V9. Baselines (38/45 features) continue to use `evaluate_variants` as-is.

### Per-seed training summary

|seed|train|test|acc|acc(weighted)|rounds|gate23 drop check|gate23 overfit check|
|---|---|---|---|---|---|---|---|
|0|395|99|0.909|0.918|352|WARN|PASS|
|1|395|99|0.889|0.911|434|WARN|PASS|
|2|395|99|0.909|0.953|663|WARN|PASS|
|3|395|99|0.919|0.939|287|WARN|PASS|
|4|395|99|0.919|0.911|281|WARN|PASS|
|mean|—|—|0.909±0.011|0.926±0.017|—|—|—|

Selected seed (median solver-corrected litmus): **seed 4**

### Held-out classification report (chosen seed)

|class|precision|recall|f1|support|
|---|---|---|---|---|
|FOLD|0.938|1.000|0.968|15|
|CHECK|1.000|0.918|0.957|49|
|CALL|0.833|0.833|0.833|12|
|BET|0.810|1.000|0.895|17|
|RAISE|0.800|0.667|0.727|6|

### Held-out confusion matrix (chosen seed; rows=true, cols=pred; class order = ACTION_CLASSES)

```
          FOLD  CHECK   CALL    BET  RAISE
  FOLD      15      0      0      0      0
 CHECK       0     45      0      4      0
  CALL       1      0     10      0      1
   BET       0      0      0     17      0
 RAISE       0      0      2      0      4
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
|MW-25|BET|BET|CHECK|
|MW-30|CALL|CALL|CALL|
|MW-31|FOLD|FOLD|CALL|
|MW-40|BET|BET|CHECK|
|MW-42|BET|BET|CHECK|
|MW-45|RAISE|RAISE|CALL|
|MW-46|FOLD|CALL|RAISE|
|MW-47|CALL|RAISE|CALL|
|MW-49|BET|BET|CHECK|

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
|`flush_draw_block_pct`|0.0040|YES — FLAG|
|`straight_draw_block_pct`|0.0086|YES — FLAG|
|`nut_made_block_pct`|0.0095|YES — FLAG|

### Top 15 features by importance (chosen seed)

|feature|importance|
|---|---|
|`equity_margin`|0.0690|
|`facing_bet`|0.0672|
|`raw_equity`|0.0558|
|`to_call`|0.0454|
|`has_flush_draw`|0.0447|
|`equity_vs_range`|0.0433|
|`pot_odds`|0.0420|
|`is_paired`|0.0418|
|`is_strong_made`|0.0330|
|`bet_to_pot`|0.0309|
|`better_hand_pct`|0.0307|
|`flush_block_pct`|0.0298|
|`improvement_probability`|0.0280|
|`is_rainbow`|0.0254|
|`hand_category`|0.0246|

### Below-1% drop list (chosen seed)

|feature|importance|
|---|---|
|`draw_outs`|0.0098|
|`hero_position`|0.0097|
|`nut_made_block_pct`|0.0095|
|`spr`|0.0094|
|`danger_score`|0.0094|
|`straight_draw_block_pct`|0.0086|
|`num_opponents`|0.0084|
|`flush_draw_rank`|0.0069|
|`villain_aggression_count`|0.0067|
|`villain_draw_pct`|0.0066|
|`street`|0.0065|
|`connectivity_score`|0.0057|
|`is_preflop_aggressor`|0.0056|
|`flush_draw_block_pct`|0.0040|
|`straight_danger`|0.0039|
|`villain_position`|0.0031|
|`is_made_hand`|0.0000|
|`has_straight_draw`|0.0000|
|`is_monotone`|0.0000|
|`is_double_paired`|0.0000|
|`flush_danger`|0.0000|
|`is_3bet_pot`|0.0000|
|`villain_call_count`|0.0000|
|`villain_range_capped`|0.0000|
|`num_callers_to_bet`|0.0000|
|`facing_raise`|0.0000|
|`has_showdown_value`|0.0000|
|`nut_flush_block`|0.0000|

### Above-30% overfit warning list (chosen seed)

(none)

## Section E — 12.5D vs 12.5D' delta

Compares this run's chosen-seed metrics against the merged 12.5D baseline (PR #126, master `d7d2cdd`, chosen seed = 4, pure-confidence weighting). Same hyperparameters, same seed list, same warm-start anchor — only the `sample_weight` computation changed (confidence × class_weight, cap 3.0, per ml-architect Q3).

### Litmus delta (per-seed solver-corrected)

|seed|12.5D|12.5D'|Δ|
|---|---|---|---|
|0|31/40|31/40|0|
|1|30/40|30/40|0|
|2|30/40|30/40|0|
|3|31/40|31/40|0|
|4|31/40|31/40|0|
|**median**|**31/40**|**31/40**|**0**|

### Per-class held-out metrics delta (chosen seed: 12.5D=4 vs 12.5D'=4)

|class|12.5D precision/recall/f1|12.5D' precision/recall/f1|recall Δ|
|---|---|---|---|
|FOLD|0.938/1.000/0.968|0.938/1.000/0.968|+0.000|
|CHECK|0.939/0.939/0.939|1.000/0.918/0.957|-0.021|
|CALL|0.769/0.833/0.800|0.833/0.833/0.833|+0.000|
|BET|0.824/0.824/0.824|0.810/1.000/0.895|+0.176|
|RAISE|0.750/0.500/0.600|0.800/0.667/0.727|+0.167|

### Per-hand outcome on gto-expert's 7 shared-cause + 2 distinct-cause failures

Predicted flip = 12.5D student wrong → 12.5D' student matches solver-corrected expert. gto-expert prediction: hybrid weighting closes the 7 shared (passive→aggressive collapse), 2 distinct stay broken (feature-surface gap).

|hand|cause|12.5D student|12.5D' student|solver-corrected expert|outcome|
|---|---|---|---|---|---|
|MW-17|shared|FOLD|FOLD|CALL|STAYED-WRONG|
|MW-24|shared|CHECK|BET|BET|FLIPPED-CORRECT ✓|
|MW-25|shared|CHECK|CHECK|BET|STAYED-WRONG|
|MW-40|shared|CHECK|CHECK|BET|STAYED-WRONG|
|MW-42|shared|CHECK|CHECK|BET|STAYED-WRONG|
|MW-45|shared|CALL|CALL|RAISE|STAYED-WRONG|
|MW-47|shared|CALL|CALL|RAISE|STAYED-WRONG|
|MW-31|distinct|CALL|CALL|FOLD|STAYED-WRONG|
|MW-46|distinct|RAISE|RAISE|CALL|STAYED-WRONG|

**Summary:** of 7 shared-cause failures, **1 flipped to correct** under hybrid weighting, **6 stayed wrong**. Of 2 distinct-cause failures, **0 flipped** (gto-expert predicted: 0).

### v2.4 P1 blocker importance delta (12.5D vs 12.5D')

|feature|12.5D|12.5D'|Δ|
|---|---|---|---|
|`nut_flush_block`|0.0000|0.0000|+0.0000|
|`flush_draw_block_pct`|0.0107|0.0040|-0.0067|
|`straight_draw_block_pct`|0.0071|0.0086|+0.0015|
|`nut_made_block_pct`|0.0056|0.0095|+0.0039|

### Interpretation hints (reviewer-scope)

- **Gate threshold (dispatch):** ≥33 promote, 31-32 STOP/owner-tie-gate, <31 STOP+flag-Q3-wrong
- **This run:** median 31/40 → falls in 31-32 owner-tie-gate
- gto-expert prediction was 7 shared flip + 2 distinct stay-wrong (predicted student → 36-38/40 range). Empirical: 1/7 shared flipped, 0/2 distinct flipped

## Section D — provenance hashes

- Repo HEAD SHA: `1b95648a2df9bc3f3908b22c08c2841a7c9fb933`
- Trainer module: `river-rats-core/train_model_v9_student.py` (this PR)
- Warm-start anchor: `river-rats-core/models/gto_model_v9_3way_v2.2.json` SHA256: `9f3845bb2a56e99328261c70c3f34decd669f3e047162eb85c78f926bc366900`
- Output model: `river-rats-core/models/gto_model_v9_student.json` SHA256: `(no model promoted)`
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
| Gate threshold (≥33 PROMOTE / 31-32 owner-tie / <31 Q3-flag) | STOP / owner-tie-gate — 31/40 in 31-32 band |
| 4-file deliverable diff (3 deliverables + 1 BLOCKED comm; cleanup matched actual 4-file PR diff at PR #131 open time) | enforced by builder pre-PR `git diff --stat` check |

## References

- 12.5D' dispatch directive (this run's actual dispatch): `review/comms/MAIN_TERMINAL_PHASE125D_PRIME_DISPATCH_2026-05-04.md` (PR #130, master `1b95648`)
- 12.5D dispatch directive (predecessor; original v9-student dispatch): `review/comms/MAIN_TERMINAL_PHASE125D_DISPATCH_2026-05-03.md` (PR #125, master `e3c0dfc`)
- Blueprint: `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` (PR #122, master `1e4e47e`)
- Pivot directive: PR #119 (master `770b897`)
- ml-architect spec: PR #110 (master `291af80`)
- Solver corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`

**Status: 12.5D' RUN COMPLETE; model NOT promoted (median seed below v9-3way-v2.2 baseline). 12.5D' synthesis owner gate decided next direction (Direction D — corpus expansion at 12.5E). Cleanup applied at 12.5E-E per dispatch §"Step 4" — original trainer-written status incorrectly read "12.5D RUN COMPLETE. Median-litmus seed promoted to `..._wt/...`" which conflated 12.5D vs 12.5D' phase + falsely claimed promotion + leaked builder worktree path.**
