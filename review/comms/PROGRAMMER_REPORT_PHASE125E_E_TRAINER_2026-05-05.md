---
date: 2026-05-05
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · Owner · ML-ARCHITECT (advisory) · GTO-EXPERT (review) · QC stream
re: Phase 12.5E — v9 student trainer run (hybrid weighting; combined corpus)
status: BUILDER BLOCKED — 12.5E implementation + 5-seed run complete; gate did not promote; model NOT promoted
---

# Phase 12.5E — v9 student trainer report (hybrid weighting)

12.5E RUN COMPLETE; median seed below v9-3way-v2.2 baseline. Per dispatch gate threshold the model was NOT promoted. Section E quantifies the delta vs 12.5D baseline.

Master HEAD at run time: `31f2f7409fa860dd68008a9e13dba2dbd6efbeed`. Run timestamp (UTC): `2026-05-05T18:43:36Z`.

## Section A — training metadata

- Corpus: `data/corpus_combined_604_2026-05-05.jsonl` (joined rows: 604)
- Labels: `data/corpus_combined_604_labels_2026-05-05.jsonl`
- Warm-start requested: `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- Warm-start resolution: requested path IS git-tracked
- Warm-start resolved: `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- Pre-pad mode: `metadata_bump` (blueprint §4)
- Test size: 0.2
- Seeds: 0,1,2,3,4
- Confidence weighting: `pure`
- Reference set: `mw_11_50`

### Class label distribution (full corpus)

- FOLD: 75
- CHECK: 271
- CALL: 72
- BET: 118
- RAISE: 68

### Confidence histogram (full corpus)

- 1.0: 392
- 0.8: 125
- 0.6: 82
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
prepad: bumped num_feature 45 → 59 → /tmp/prepad_v9_272y5m29.json
```

### Schema discoveries surfaced during 12.5D

1. **Join key**: blueprint §6 + ml-architect §12 cited `corpus.source_situation_id == labels.ref_id` as the join key, verified on row 1. Subsequent rows (cohort 2, indices 100-493) have `situation_id` instead of `source_situation_id`, and `labels.ref_id` is heterogeneous (mix of `d####_POS_street` and `PILOT_###` IDs). The universally-populated canonical key is `pilot_hand_id` (494/494 in both files). Trainer joins on `pilot_hand_id`. Spec INTENT (494-hand training) is preserved.

2. **Path Y inference boundary**: `reference_evaluator.evaluate_variants` builds inference arrays via `gto_model.GtoOracle.features_from_dict` which iterates `gto_model.FEATURE_COLUMNS` (length 55). The student model expects 59 features. Path Y forbids extending `gto_model.FEATURE_COLUMNS`, so the student's reference-set evaluation uses an in-module 59-feature inference helper (`_StudentInference` + `_evaluate_student_one_hand`) that mirrors `reference_evaluator._evaluate_one_hand` logic with STUDENT_FEATURE_COLUMNS_V9. Baselines (38/45 features) continue to use `evaluate_variants` as-is.

### Per-seed training summary

|seed|train|test|acc|acc(weighted)|rounds|gate23 drop check|gate23 overfit check|
|---|---|---|---|---|---|---|---|
|0|483|121|0.942|0.968|589|WARN|PASS|
|1|483|121|0.893|0.931|812|WARN|PASS|
|2|483|121|0.893|0.939|405|WARN|PASS|
|3|483|121|0.926|0.954|718|WARN|PASS|
|4|483|121|0.901|0.926|720|WARN|PASS|
|mean|—|—|0.911±0.020|0.944±0.015|—|—|—|

Selected seed (median solver-corrected litmus): **seed 2**

### Held-out classification report (chosen seed)

|class|precision|recall|f1|support|
|---|---|---|---|---|
|FOLD|1.000|0.933|0.966|15|
|CHECK|1.000|0.815|0.898|54|
|CALL|0.867|0.929|0.897|14|
|BET|0.706|1.000|0.828|24|
|RAISE|0.929|0.929|0.929|14|

### Held-out confusion matrix (chosen seed; rows=true, cols=pred; class order = ACTION_CLASSES)

```
          FOLD  CHECK   CALL    BET  RAISE
  FOLD      14      0      1      0      0
 CHECK       0     44      0     10      0
  CALL       0      0     13      0      1
   BET       0      0      0     24      0
 RAISE       0      0      1      0     13
```

## Section B — reference-evaluator results (Gate 2.4)

Solver-correction overlay: applied to ['MW-30', 'MW-46', 'MW-47'] per `memory/reference_corrections.md`. MW-31, MW-50 NOT applied (unverified per blueprint §5.3).

### Per-seed student litmus (solver-corrected) — full sweep

|seed|raw|solver-corrected|
|---|---|---|
|0|33/40|32/40|
|1|34/40|33/40|
|2|33/40|32/40|
|3|33/40|32/40|
|4|33/40|32/40|
|mean|—|32.20/40 (std 0.40)|

### Chosen seed (2) cross-model litmus

|model|raw|solver-corrected|
|---|---|---|
|v9-student (chosen seed)|33/40|32/40|
|gto_model_v9_3way_v2.2.json|33/40|33/40|

### Solver-corrected per-hand comparison (chosen seed)

Only hands where any model differs from corrected expert OR where the correction overlay activates.

|ref_id|expert (raw)|solver-corrected expert|student|
|---|---|---|---|
|MW-17|CALL|CALL|FOLD|
|MW-20|CALL|CALL|RAISE|
|MW-25|BET|BET|CHECK|
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
|`nut_flush_block`|0.0268|no|
|`flush_draw_block_pct`|0.0143|no|
|`straight_draw_block_pct`|0.0056|YES — FLAG|
|`nut_made_block_pct`|0.0095|YES — FLAG|

### Top 15 features by importance (chosen seed)

|feature|importance|
|---|---|
|`flush_draw_rank`|0.2523|
|`facing_bet`|0.0526|
|`equity_margin`|0.0459|
|`flush_block_pct`|0.0387|
|`is_monster`|0.0369|
|`num_opponents`|0.0368|
|`raw_equity`|0.0344|
|`to_call`|0.0327|
|`better_hand_pct`|0.0270|
|`nut_flush_block`|0.0268|
|`equity_vs_range`|0.0257|
|`is_strong_made`|0.0245|
|`improvement_probability`|0.0214|
|`is_ip`|0.0200|
|`board_favour`|0.0178|

### Below-1% drop list (chosen seed)

|feature|importance|
|---|---|
|`villain_draw_pct`|0.0100|
|`nut_made_block_pct`|0.0095|
|`pot_size`|0.0094|
|`board_adjusted_hrp`|0.0086|
|`hero_position`|0.0085|
|`hero_range_percentile`|0.0081|
|`danger_score`|0.0080|
|`is_preflop_aggressor`|0.0079|
|`spr`|0.0077|
|`villain_medium_made_pct`|0.0075|
|`num_callers_to_bet`|0.0072|
|`overcard_outs`|0.0060|
|`villain_position`|0.0058|
|`straight_draw_block_pct`|0.0056|
|`villain_fold_equity_estimate`|0.0056|
|`street`|0.0052|
|`flush_danger`|0.0051|
|`high_card_rank`|0.0049|
|`villain_call_count`|0.0047|
|`straight_danger`|0.0042|
|`is_paired`|0.0040|
|`connectivity_score`|0.0038|
|`villain_range_capped`|0.0032|
|`villain_aggression_count`|0.0031|
|`is_rainbow`|0.0022|
|`is_made_hand`|0.0000|
|`has_flush_draw`|0.0000|
|`is_monotone`|0.0000|
|`is_two_tone`|0.0000|
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
|0|31/40|32/40|+1|
|1|30/40|33/40|+3|
|2|30/40|32/40|+2|
|3|31/40|32/40|+1|
|4|31/40|32/40|+1|
|**median**|**31/40**|**32/40**|**+1**|

### Per-class held-out metrics delta (chosen seed: 12.5D=4 vs 12.5D'=2)

|class|12.5D precision/recall/f1|12.5D' precision/recall/f1|recall Δ|
|---|---|---|---|
|FOLD|0.938/1.000/0.968|1.000/0.933/0.966|-0.067|
|CHECK|0.939/0.939/0.939|1.000/0.815/0.898|-0.124|
|CALL|0.769/0.833/0.800|0.867/0.929/0.897|+0.096|
|BET|0.824/0.824/0.824|0.706/1.000/0.828|+0.176|
|RAISE|0.750/0.500/0.600|0.929/0.929/0.929|+0.429|

### Per-hand outcome on gto-expert's 7 shared-cause + 2 distinct-cause failures

Predicted flip = 12.5D student wrong → 12.5D' student matches solver-corrected expert. gto-expert prediction: hybrid weighting closes the 7 shared (passive→aggressive collapse), 2 distinct stay broken (feature-surface gap).

|hand|cause|12.5D student|12.5D' student|solver-corrected expert|outcome|
|---|---|---|---|---|---|
|MW-17|shared|FOLD|FOLD|CALL|STAYED-WRONG|
|MW-24|shared|CHECK|BET|BET|FLIPPED-CORRECT ✓|
|MW-25|shared|CHECK|CHECK|BET|STAYED-WRONG|
|MW-40|shared|CHECK|CHECK|BET|STAYED-WRONG|
|MW-42|shared|CHECK|BET|BET|FLIPPED-CORRECT ✓|
|MW-45|shared|CALL|CALL|RAISE|STAYED-WRONG|
|MW-47|shared|CALL|CALL|RAISE|STAYED-WRONG|
|MW-31|distinct|CALL|CALL|FOLD|STAYED-WRONG|
|MW-46|distinct|RAISE|RAISE|CALL|STAYED-WRONG|

**Summary:** of 7 shared-cause failures, **2 flipped to correct** under hybrid weighting, **5 stayed wrong**. Of 2 distinct-cause failures, **0 flipped** (gto-expert predicted: 0).

### v2.4 P1 blocker importance delta (12.5D vs 12.5D')

|feature|12.5D|12.5D'|Δ|
|---|---|---|---|
|`nut_flush_block`|0.0000|0.0268|+0.0268|
|`flush_draw_block_pct`|0.0107|0.0143|+0.0036|
|`straight_draw_block_pct`|0.0071|0.0056|-0.0015|
|`nut_made_block_pct`|0.0056|0.0095|+0.0039|

### Interpretation hints (reviewer-scope)

- **Gate threshold (dispatch):** ≥33 promote, 31-32 STOP/owner-tie-gate, <31 STOP+flag-Q3-wrong
- **This run:** median 32/40 → falls in 31-32 owner-tie-gate
- gto-expert prediction was 7 shared flip + 2 distinct stay-wrong (predicted student → 36-38/40 range). Empirical: 2/7 shared flipped, 0/2 distinct flipped

## Section D — provenance hashes

- Repo HEAD SHA: `31f2f7409fa860dd68008a9e13dba2dbd6efbeed`
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
| Gate threshold (≥33 PROMOTE / 31-32 owner-tie / <31 Q3-flag) | STOP / owner-tie-gate — 32/40 in 31-32 band |
| 4-file deliverable diff | enforced by builder pre-PR `git diff --stat` check |

## References

- 12.5E-E dispatch (this run's actual dispatch): `review/comms/MAIN_TERMINAL_PHASE125E_E_DISPATCH_2026-05-05.md` (PR #151, master `31f2f74`)
- 12.5E-D APPROVE (corpus QC): PR #150 (master `4070a11`)
- 12.5E-C LABELS FINAL: PR #146 (master `3914fea`)
- 12.5E-B Path B amendment merged: PR #136 (master `0eaac06`)
- 12.5D' dispatch directive (predecessor): `review/comms/MAIN_TERMINAL_PHASE125D_PRIME_DISPATCH_2026-05-04.md` (PR #130, master `1b95648`)
- 12.5D dispatch directive (predecessor²): `review/comms/MAIN_TERMINAL_PHASE125D_DISPATCH_2026-05-03.md` (PR #125, master `e3c0dfc`)
- Blueprint: `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` (PR #122, master `1e4e47e`)
- Pivot directive: PR #119 (master `770b897`)
- ml-architect spec: PR #110 (master `291af80`)
- Solver corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`

---

## Section E2 — 12.5D' vs 12.5E delta (added at 12.5E-E per dispatch §"Step 5")

The trainer-generated Section E above compares the current run vs the hardcoded 12.5D baseline (the original pure-confidence run). For 12.5E-E, the more relevant comparison is vs **12.5D'** (PR #131 / master `659c572`) — the immediate-predecessor run with cap=3.0 hybrid weighting on the 494-hand corpus. Section E2 captures that delta.

### Litmus delta (per-seed solver-corrected): 12.5D' vs 12.5E

| seed | 12.5D' | 12.5E | Δ |
|---|---|---|---|
| 0 | 31/40 | 32/40 | +1 |
| 1 | 30/40 | 33/40 | +3 |
| 2 | 30/40 | 32/40 | +2 |
| 3 | 31/40 | 32/40 | +1 |
| 4 | 31/40 | 32/40 | +1 |
| **median** | **31/40** | **32/40** | **+1** |

Mean 30.6 → 32.2 (+1.6 hands). Per-seed std 0.49 → 0.40 (modest stabilization).

### Per-hand outcome on 7 shared-cause + 2 distinct-cause failures + new findings

12.5D' chosen seed (4) per-hand vs 12.5E chosen seed (2) per-hand:

| ref_id | cause | 12.5D' student | 12.5E student | corrected expert | outcome |
|---|---|---|---|---|---|
| MW-17 | shared (E-FEATURE primary) | FOLD | FOLD | CALL | STAYED-WRONG |
| MW-24 | shared (E-DIST) | BET (✓ via hybrid) | (correct, not in failure list) | BET | STAYED-CORRECT |
| MW-25 | shared (E-DIST) | CHECK | CHECK | BET | STAYED-WRONG (under-aggress) |
| MW-40 | shared (E-DIST) | CHECK | CHECK | BET | STAYED-WRONG (under-aggress) |
| MW-42 | shared (E-FEATURE primary) | CHECK | (correct, not in failure list) | BET | **FLIPPED-CORRECT** ✓ |
| MW-45 | shared (E-DIST) | CALL | CALL | RAISE | STAYED-WRONG (under-aggress) |
| MW-47 | shared (E-DIST + E-FEATURE compound) | CALL | CALL | RAISE (corrected) | STAYED-WRONG (under-aggress) |
| MW-31 | distinct (no feature for villain check-raise credibility) | CALL | CALL | FOLD | STAYED-WRONG (over-aggress; feature-surface gap as predicted) |
| MW-46 | distinct (no feature for villain check-raise river credibility) | RAISE | RAISE | CALL (corrected) | STAYED-WRONG (over-aggress; feature-surface gap as predicted) |
| **MW-20** | **NEW miss in 12.5E** | (correct in 12.5D' per absence from failure list) | RAISE | CALL | **NEWLY-BROKEN** (over-aggress) |

**Summary**: of 7 shared-cause failures, **1 newly flipped to correct (MW-42)**; 5 stayed wrong; MW-24 carried over correct from 12.5D'. Of 2 distinct-cause failures, both stayed wrong as predicted. **1 newly-broken hand (MW-20)** is over-aggression — possibly downstream of the new RAISE-class corpus signal teaching the booster to fire RAISE more readily.

Net per-hand on the gto-expert tracked set: **+1 (MW-42) − 1 (MW-20) = 0 net**. The +1 gate movement (median 31 → 32) comes from non-tracked hands shifting.

### Per-class held-out metrics (12.5E chosen seed 2)

12.5E held-out accuracy: **0.893** unweighted (12.5D' chosen seed 4 was 0.889 — essentially unchanged). Per-class output distribution remains balanced (no class collapse — fixed since 12.5D' hybrid weighting and preserved by 12.5E corpus expansion).

### v2.4 P1 blocker importance delta (12.5D' vs 12.5E) — **THE LOAD-BEARING H-FEAT TEST**

| feature | 12.5D' | 12.5E | Δ | ml-architect Q4 prediction (≥0.02) |
|---|---|---|---|---|
| `nut_flush_block` | **0.0000** | **0.0268** | **+0.0268** | **✓ MET (target ≥0.02; exceeded)** |
| `flush_draw_block_pct` | 0.0040 | 0.0143 | +0.0103 | partial (target ≥0.02; not met) |
| `straight_draw_block_pct` | 0.0086 | 0.0056 | -0.0030 | not met (decreased) |
| `nut_made_block_pct` | 0.0095 | 0.0095 | +0.0000 | not met (unchanged) |

**The H-FEAT primary load-bearing test PASSED at the feature-importance layer.** `nut_flush_block` jumped from 0.0000 (booster never split on it under any 12.5D/12.5D' loss surface) to 0.0268 (now actively splits 2.7% of the time). The corpus expansion (T5 NFD-blocker situations + Path B v3.3/v3.4 RAISE labels for 10 of them) successfully activated the feature.

`flush_draw_block_pct` also moved positively (+260% relative), but didn't clear the 0.02 threshold. Other two blockers stayed flat or decreased.

`flush_draw_rank` unexpectedly jumped to 0.2523 (top feature by importance) — this is an EXISTING feature, not a migration target. Either the booster found it as a strong proxy for blocker reasoning, OR the corpus expansion's `flush_draw_rank` distribution unexpectedly correlates with the new RAISE labels. Worth ml-architect investigation but not a STOP signal.

### Trade-off assessment: feature activated but gate movement modest

The v3.3/v3.4 wording-fix at the labelling layer correctly partitions T5 hands (10 RAISE labels for high-air, 4 CALL labels for near-zero-air). The booster sees both signal types and learns the `nut_flush_block × villain_air_pct` interaction implicitly. But this learning translates to only +1 hand on the gate (median 31 → 32).

Possible reasons (no recommendation; orchestrator/ml-architect at 12.5E-F gate decides):
- Reference set's MW-25/40/45/47 failures are primarily **E-DIST** per gto-expert: adding 12 RAISE situations + 4 CALL situations of similar pattern teaches the booster the pattern but doesn't perfectly transfer to the specific reference hands
- MW-17 + MW-42 are **E-FEATURE**: the corpus expansion can't fully fix what the 59-feature surface doesn't encode (only MW-42 flipped — likely because its action-sequence narrowing is partially feature-encodable)
- The 110-hand expansion is at the conservative end (per design §4 "150 or 200 is the escalation point"); a larger expansion may move the gate further

### gto-expert-hat sanity check (per dispatch §"LEAD-PROGRAMMER (gto-expert hat)")

| Check | Outcome |
|---|---|
| Chosen-seed solver-corrected vs gate threshold (≥33 to clear, 31-32 = owner-tie-gate, <31 = STOP/regression) | **32/40 → 31-32 owner-tie-gate band** |
| P1 blocker importance moved from 0.0000 → ≥0.02 (ml-architect Q4) | **✓ for `nut_flush_block` (0.0268; cleared 0.02 floor)**; partial for other blockers |
| 7 shared-cause hands flipped count | 1 newly flipped (MW-42); 1 carryover correct (MW-24); 5 stayed wrong (MW-17/25/40/45/47) |
| MW-31, MW-46 distinct-cause stayed wrong (predicted: both) | **✓** both stayed wrong as predicted (feature-surface gap) |
| Newly-broken hands | 1 (MW-20 over-aggress; possibly downstream of stronger RAISE-class corpus signal) |
| 4 T5 CALL hands taught `nut_flush_block × villain_air` interaction | partially; `nut_flush_block` activation is empirical evidence |
| Trainer auto-STOP behavior | fired (chosen 32 < baseline 33); no model promoted; consistent with dispatch's 7-file fallback path |

### Failure direction classification (per `feedback_failure_direction_classification.md`)

12.5E ref-set failures classified by direction:
- **Under-aggression** (5): MW-17 (FOLD vs CALL), MW-25 (CHECK vs BET), MW-40 (CHECK vs BET), MW-45 (CALL vs RAISE), MW-47 (CALL vs RAISE corrected)
- **Over-aggression** (3): MW-31 (CALL vs FOLD), MW-46 (RAISE vs CALL corrected), MW-20 (RAISE vs CALL — newly broken)
- **Class-collapse**: NONE — student per-class distribution balanced (no class with 0 predictions on 40-hand reference set)

Consistent with v9-3way-v2.2's pattern (under-aggression dominates; class collapse fixed by hybrid weighting since 12.5D' and preserved by 12.5E). Corpus expansion did not introduce class-collapse regression.

---

**Status: 12.5E RUN COMPLETE; model NOT promoted (median 32/40 < v9-3way-v2.2 baseline 33/40). H-FEAT primary test PASSED at the feature-importance layer (`nut_flush_block` 0.0000 → 0.0268). Gate movement modest (+1 hand vs 12.5D'). 12.5E-F gate decides next direction (PROMOTE / owner-tie-gate / Path C escalation / 12.5G cap retuning). 7-file PR per dispatch's no-model-promotion fallback. Awaiting QC audit-now trigger from orchestrator per dispatch §"QC stream".**
