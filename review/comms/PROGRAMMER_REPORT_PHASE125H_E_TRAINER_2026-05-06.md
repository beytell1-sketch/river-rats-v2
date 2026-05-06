---
date: 2026-05-06
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · Owner · ML-ARCHITECT (advisory) · GTO-EXPERT (review) · QC stream
re: Phase 12.5H-E — v9 student trainer run (hybrid weighting; combined corpus)
status: BUILDER BLOCKED — 12.5H-E implementation + 5-seed run complete; gate did not promote; model NOT promoted
---

# Phase 12.5H-E — v9 student trainer report (hybrid weighting)

12.5H-E RUN COMPLETE; median seed below v9-3way-v2.2 baseline. Per dispatch gate threshold the model was NOT promoted. Section E quantifies the delta vs 12.5D baseline.

Master HEAD at run time: `bacce1d216107f37908f0d50c2875bc0bfb98427`. Run timestamp (UTC): `2026-05-06T03:45:07Z`.

## Section A — training metadata

- Corpus: `data/corpus_combined_694_2026-05-06.jsonl` (joined rows: 694)
- Labels: `data/corpus_combined_694_labels_2026-05-06.jsonl`
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

- FOLD: 79
- CHECK: 295
- CALL: 79
- BET: 137
- RAISE: 104

### Confidence histogram (full corpus)

- 1.0: 462
- 0.8: 137
- 0.6: 90
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
prepad: bumped num_feature 45 → 59 → /tmp/prepad_v9_o_ekuion.json
```

### Schema discoveries surfaced during 12.5D

1. **Join key**: blueprint §6 + ml-architect §12 cited `corpus.source_situation_id == labels.ref_id` as the join key, verified on row 1. Subsequent rows (cohort 2, indices 100-493) have `situation_id` instead of `source_situation_id`, and `labels.ref_id` is heterogeneous (mix of `d####_POS_street` and `PILOT_###` IDs). The universally-populated canonical key is `pilot_hand_id` (494/494 in both files). Trainer joins on `pilot_hand_id`. Spec INTENT (494-hand training) is preserved.

2. **Path Y inference boundary**: `reference_evaluator.evaluate_variants` builds inference arrays via `gto_model.GtoOracle.features_from_dict` which iterates `gto_model.FEATURE_COLUMNS` (length 55). The student model expects 59 features. Path Y forbids extending `gto_model.FEATURE_COLUMNS`, so the student's reference-set evaluation uses an in-module 59-feature inference helper (`_StudentInference` + `_evaluate_student_one_hand`) that mirrors `reference_evaluator._evaluate_one_hand` logic with STUDENT_FEATURE_COLUMNS_V9. Baselines (38/45 features) continue to use `evaluate_variants` as-is.

### Per-seed training summary

|seed|train|test|acc|acc(weighted)|rounds|gate23 drop check|gate23 overfit check|
|---|---|---|---|---|---|---|---|
|0|555|139|0.914|0.931|900|WARN|WARN|
|1|555|139|0.935|0.963|700|WARN|PASS|
|2|555|139|0.914|0.950|671|WARN|PASS|
|3|555|139|0.942|0.967|914|WARN|PASS|
|4|555|139|0.928|0.958|469|WARN|PASS|
|mean|—|—|0.927±0.012|0.954±0.013|—|—|—|

Selected seed (median solver-corrected litmus): **seed 2**

### Held-out classification report (chosen seed)

|class|precision|recall|f1|support|
|---|---|---|---|---|
|FOLD|1.000|0.938|0.968|16|
|CHECK|0.962|0.864|0.911|59|
|CALL|0.889|1.000|0.941|16|
|BET|0.758|0.926|0.833|27|
|RAISE|1.000|0.952|0.976|21|

### Held-out confusion matrix (chosen seed; rows=true, cols=pred; class order = ACTION_CLASSES)

```
          FOLD  CHECK   CALL    BET  RAISE
  FOLD      15      0      1      0      0
 CHECK       0     51      0      8      0
  CALL       0      0     16      0      0
   BET       0      2      0     25      0
 RAISE       0      0      1      0     20
```

## Section B — reference-evaluator results (Gate 2.4)

Solver-correction overlay: applied to ['MW-30', 'MW-46', 'MW-47'] per `memory/reference_corrections.md`. MW-31, MW-50 NOT applied (unverified per blueprint §5.3).

### Per-seed student litmus (solver-corrected) — full sweep

|seed|raw|solver-corrected|
|---|---|---|
|0|33/40|32/40|
|1|33/40|32/40|
|2|33/40|32/40|
|3|33/40|32/40|
|4|33/40|32/40|
|mean|—|32.00/40 (std 0.00)|

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
|`nut_flush_block`|0.0496|no|
|`flush_draw_block_pct`|0.0528|no|
|`straight_draw_block_pct`|0.0055|YES — FLAG|
|`nut_made_block_pct`|0.0151|no|

### Top 15 features by importance (chosen seed)

|feature|importance|
|---|---|
|`facing_bet`|0.0726|
|`equity_margin`|0.0592|
|`to_call`|0.0532|
|`flush_draw_block_pct`|0.0528|
|`nut_flush_block`|0.0496|
|`flush_block_pct`|0.0458|
|`raw_equity`|0.0447|
|`is_monster`|0.0416|
|`equity_vs_range`|0.0361|
|`better_hand_pct`|0.0321|
|`has_straight_draw`|0.0310|
|`num_opponents`|0.0308|
|`improvement_probability`|0.0264|
|`villain_draw_pct`|0.0226|
|`worse_hand_pct`|0.0198|

### Below-1% drop list (chosen seed)

|feature|importance|
|---|---|
|`danger_score`|0.0086|
|`villain_medium_made_pct`|0.0083|
|`villain_fold_equity_estimate`|0.0082|
|`draw_outs`|0.0070|
|`connectivity_score`|0.0062|
|`villain_range_capped`|0.0059|
|`straight_draw_block_pct`|0.0055|
|`street`|0.0054|
|`is_paired`|0.0053|
|`high_card_rank`|0.0051|
|`straight_danger`|0.0050|
|`num_callers_to_bet`|0.0042|
|`villain_call_count`|0.0041|
|`villain_aggression_count`|0.0036|
|`flush_danger`|0.0035|
|`is_rainbow`|0.0030|
|`is_made_hand`|0.0000|
|`has_flush_draw`|0.0000|
|`is_monotone`|0.0000|
|`is_two_tone`|0.0000|
|`is_double_paired`|0.0000|
|`is_3bet_pot`|0.0000|
|`facing_raise`|0.0000|
|`has_showdown_value`|0.0000|
|`flush_draw_rank`|0.0000|

### Above-30% overfit warning list (chosen seed)

(none)

## Section E — 12.5D vs 12.5D' delta

Compares this run's chosen-seed metrics against the merged 12.5D baseline (PR #126, master `d7d2cdd`, chosen seed = 4, pure-confidence weighting). Same hyperparameters, same seed list, same warm-start anchor — only the `sample_weight` computation changed (confidence × class_weight, cap 3.0, per ml-architect Q3).

### Litmus delta (per-seed solver-corrected)

|seed|12.5D|12.5D'|Δ|
|---|---|---|---|
|0|31/40|32/40|+1|
|1|30/40|32/40|+2|
|2|30/40|32/40|+2|
|3|31/40|32/40|+1|
|4|31/40|32/40|+1|
|**median**|**31/40**|**32/40**|**+1**|

### Per-class held-out metrics delta (chosen seed: 12.5D=4 vs 12.5D'=2)

|class|12.5D precision/recall/f1|12.5D' precision/recall/f1|recall Δ|
|---|---|---|---|
|FOLD|0.938/1.000/0.968|1.000/0.938/0.968|-0.062|
|CHECK|0.939/0.939/0.939|0.962/0.864/0.911|-0.075|
|CALL|0.769/0.833/0.800|0.889/1.000/0.941|+0.167|
|BET|0.824/0.824/0.824|0.758/0.926/0.833|+0.102|
|RAISE|0.750/0.500/0.600|1.000/0.952/0.976|+0.452|

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
|`nut_flush_block`|0.0000|0.0496|+0.0496|
|`flush_draw_block_pct`|0.0107|0.0528|+0.0421|
|`straight_draw_block_pct`|0.0071|0.0055|-0.0016|
|`nut_made_block_pct`|0.0056|0.0151|+0.0095|

### Interpretation hints (reviewer-scope)

- **Gate threshold (dispatch):** ≥33 promote, 31-32 STOP/owner-tie-gate, <31 STOP+flag-Q3-wrong
- **This run:** median 32/40 → falls in 31-32 owner-tie-gate
- gto-expert prediction was 7 shared flip + 2 distinct stay-wrong (predicted student → 36-38/40 range). Empirical: 2/7 shared flipped, 0/2 distinct flipped

## Section D — provenance hashes

- Repo HEAD SHA: `bacce1d216107f37908f0d50c2875bc0bfb98427`
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

## Section F — 12.5E-E vs 12.5H-E delta (per dispatch §"Step 5")

Compares this 12.5H-E re-train (corpus 694 = 604 + 90; chosen seed 2) against the merged 12.5E-E baseline (corpus 604; chosen seed 2; PR #152, master `b51e525`). Same hyperparameters (cap=3.0; pre-pad metadata-only; 5 seeds 0-4; warm-start v9-3way-v2.2). Only the corpus changed.

### Per-seed solver-corrected litmus delta

| seed | 12.5E-E | 12.5H-E | Δ |
|---|---:|---:|:---:|
| 0 | 32/40 | 32/40 | 0 |
| 1 | 33/40 | 32/40 | -1 |
| 2 | 32/40 | 32/40 | 0 |
| 3 | 32/40 | 32/40 | 0 |
| 4 | 32/40 | 32/40 | 0 |
| **median** | **32/40** | **32/40** | **0** |
| **mean (std)** | **32.20 (0.40)** | **32.00 (0.00)** | **-0.20 (lower variance)** |

**Median UNCHANGED** at 32/40. 12.5H-E shows lower variance (std 0.0 vs 0.4) — suggests the 90-hand expansion stabilized seed-to-seed reproducibility but did not move the gate. Per dispatch stop condition "5-seed median < 32 → STOP, route to orchestrator", 32 = threshold; not a STOP. Per trainer's auto rule "median < v9-3way-v2.2 baseline 33/40 → no promotion", 32 < 33 → no model promotion.

### Per-hand outcomes on chosen seed (12.5E-E vs 12.5H-E)

| ref_id | 12.5E-E student | 12.5H-E student | solver-corrected expert | outcome |
|---|---|---|---|---|
| MW-17 | FOLD | FOLD | CALL | STAYED-WRONG (no change) |
| MW-20 | RAISE | RAISE | CALL | STAYED-WRONG (no change) |
| MW-25 | CHECK | CHECK | BET | STAYED-WRONG (no change) |
| MW-30 | CALL | CALL | CALL | CORRECT (no change) |
| MW-31 | CALL | CALL | FOLD | STAYED-WRONG (no change) |
| MW-40 | CHECK | CHECK | BET | STAYED-WRONG (no change) |
| MW-45 | CALL | CALL | RAISE | STAYED-WRONG (no change) |
| MW-46 | RAISE | RAISE | CALL (corrected) | STAYED-WRONG (no change) |
| MW-47 | CALL | CALL | RAISE (corrected) | STAYED-WRONG (no change) |

**0 newly-correct, 0 newly-broken.** 12.5H-E student's per-hand predictions are IDENTICAL to 12.5E-E on all 9 differential hands.

### 12.5H-targeted stay-wrong outcomes (the 5 hands the 90-hand corpus expansion specifically targeted)

| target | template | 12.5E-E | 12.5H-E | solver-corrected | outcome |
|---|---|---|---|---|---|
| MW-17 | T7-ext (path-c SUITED) | FOLD | FOLD | CALL | STAYED-WRONG (predicted by orchestrator's "Honest implication of (c)") |
| MW-25 | T8' (monotone-FD) | CHECK | CHECK | BET | STAYED-WRONG |
| MW-40 | T9' (TP-medium-kicker) | CHECK | CHECK | BET | STAYED-WRONG |
| MW-45 | T10' (slowplay set turn lead) | CALL | CALL | RAISE | STAYED-WRONG |
| MW-47 | T-RAISE-stabilize (NFD bet+call multiway) | CALL | CALL | RAISE | STAYED-WRONG |

**0 of 5 targeted stay-wrong hands flipped to correct.** All 5 remain unchanged.

### Per-hand failure direction classification (per `feedback_failure_direction_classification.md`)

Action aggression order: FOLD < CHECK < CALL < BET < RAISE.

| ref_id | 12.5H-E student | corrected expert | direction |
|---|---|---|---|
| MW-17 | FOLD | CALL | **under-aggress** (1 step down) |
| MW-20 | RAISE | CALL | **over-aggress** (2 steps up) |
| MW-25 | CHECK | BET | **under-aggress** (2 steps down) |
| MW-31 | CALL | FOLD | **over-aggress** (2 steps up) |
| MW-40 | CHECK | BET | **under-aggress** (2 steps down) |
| MW-45 | CALL | RAISE | **under-aggress** (2 steps down) |
| MW-46 | RAISE | CALL | **over-aggress** (2 steps up) |
| MW-47 | CALL | RAISE | **under-aggress** (2 steps down) |

**Direction tally:**
- Under-aggress: **5** (MW-17, 25, 40, 45, 47 — ALL 5 = the 12.5H-targeted set)
- Over-aggress: **3** (MW-20, 31, 46)
- Class-collapse: **0**

**Pattern:** the 12.5H-targeted hands are uniformly under-aggressive failures (model is too passive on hands where the GTO-correct action is to bet/raise/call). The 12.5H corpus expansion teaches the corresponding bucket reasoning correctly on the 90 new training hands (per 12.5H-D corpus QC sweep + 100% T-CONTROL design_action match) but fails to transfer that reasoning to the specific reference hands' contexts. This is consistent with gto-expert's 12.5D' E-FEATURE-primary diagnosis for these patterns.

### Cross-seed feature importance (per TC-X-CROSS-SEED-IMPORTANCE; dispatch §"Step 5 Section C")

Importance computed across 5 seeds (0-4) with the same hyperparameters. Per ml-architect Q4 H-FEAT prediction watchpoint: `nut_flush_block` is the load-bearing feature for the H-FEAT primary diagnosis.

| feature | median | mean | std | min | max | % seeds ≥ 0.02 floor |
|---|---:|---:|---:|---:|---:|---:|
| `nut_flush_block` | **0.0496** | 0.0465 | 0.0430 | 0.0000 | 0.0910 | **60%** |
| `has_flush_draw` | 0.0180 | 0.0273 | 0.0300 | 0.0000 | 0.0780 | 40% |
| `raw_equity` | 0.0389 | 0.0389 | 0.0065 | 0.0317 | 0.0461 | 100% |
| `better_hand_pct` | 0.0258 | 0.0252 | 0.0050 | 0.0191 | 0.0321 | 80% |
| `villain_air_pct` | 0.0117 | 0.0116 | 0.0030 | 0.0073 | 0.0146 | 0% |
| `pot_odds` | 0.0155 | 0.0144 | 0.0027 | 0.0113 | 0.0167 | 0% |
| `is_made_hand` | 0.0000 | 0.0036 | 0.0080 | 0.0000 | 0.0178 | 0% |
| `hand_category` | 0.0109 | 0.0126 | 0.0035 | 0.0092 | 0.0165 | 0% |
| `num_opponents` | 0.0308 | 0.0270 | 0.0059 | 0.0184 | 0.0319 | 80% |
| `is_monotone` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0% |
| `is_preflop_aggressor` | 0.0074 | 0.0085 | 0.0033 | 0.0057 | 0.0142 | 0% |
| `villain_aggression_count` | 0.0036 | 0.0055 | 0.0035 | 0.0024 | 0.0105 | 0% |
| `villain_checked_back` | 0.0125 | 0.0118 | 0.0024 | 0.0093 | 0.0147 | 0% |

### nut_flush_block H-FEAT validation status

12.5H-pre cross-seed median (corpus 604): **0.0268** (validated H-FEAT but bimodal 60/40)
12.5H-E cross-seed median (corpus 694): **0.0496** (+85% relative, +0.023 absolute)

**H-FEAT primary continues to validate; cross-seed median ALMOST DOUBLED from 12.5H-pre to 12.5H-E.** The 12.5H corpus expansion (especially T-RAISE-stabilize 12 hands targeting bet+call multiway with v3.4 Fix 2.1.1 clause-e + SUITED T7-ext 12 hands with `nut_flush_block=1`) successfully strengthened the H-FEAT primary signal. Stability remains bimodal (60% above 0.02 floor, std 0.043) — the seed-volatility issue identified at 12.5H-pre is REDUCED but not eliminated. The 0.0000-0.0910 range across seeds shows the booster's path-dependence on the warm-start anchor's pre-pad initialization.

### 12.5H-E summary

- **Median 32/40** (= 12.5E-E baseline; no improvement on reference set)
- **0 of 5 targeted stay-wrong hands flipped to correct**
- **All 5 stay-wrong remain under-aggressive failures** (FOLD/CHECK/CALL where GTO is CALL/BET/RAISE)
- **Cross-seed `nut_flush_block` median +85% vs 12.5H-pre** (corpus expansion strengthened H-FEAT primary)
- **Lower seed-to-seed variance** (std 0.0 vs 12.5E-E's 0.4 — corpus-stabilized)
- **Model NOT promoted** (median == baseline; auto-gate at "< 33" triggers no-promote)

**Implication for 12.5H-F gate:** the 12.5H corpus expansion has run its course on Path Y (E-DIST-of-corpus). The 5 targeted stay-wrong hands (especially MW-17 per orchestrator's "Honest implication of (c)") are E-FEATURE primary per gto-expert 12.5D' diagnosis and require feature engineering (Path C / Direction-X-retro) to fix. Per dispatch §"Queued": "12.5G' or feature-engineering escalation (only if 12.5H-F gate fails on MW-17 / E-FEATURE residuals)" — this empirical result triggers that queue at 12.5H-F decision time.

## References

- Dispatch directive: `review/comms/MAIN_TERMINAL_PHASE125H_E_DISPATCH_2026-05-06.md` (PR #187, master `bacce1d`)
- 12.5E-E precedent: `review/comms/PROGRAMMER_REPORT_PHASE125E_E_TRAINER_2026-05-05.md` (PR #152, master `b51e525`)
- 12.5H-D APPROVE: master `a554d71` (PR #186)
- 12.5H-C labels final: master `690ca8f` (PR #184)
- 12.5H-pre cross-seed analysis: master `edd5556` (PR #161)
- Blueprint: `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` (PR #122, master `1e4e47e`)
- ml-architect 12.5D' Q4 H-FEAT prediction: `/tmp/ml_architect_125d_prime_findings.md`
- gto-expert 12.5D' per-hand classification (MW-17 = E-FEATURE primary): `/tmp/gto_expert_125d_prime_findings.md`
- Solver corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`
- Memory: `feedback_failure_direction_classification.md` (per-hand classification rule), `feedback_pilot_first_for_long_jobs.md` (pilot 1-seed before full), `feedback_quality_default_no_ask.md`

**Status: 12.5H-E RUN COMPLETE; model NOT promoted (median 32/40 = 12.5E-E baseline; gate < 33). H-FEAT primary continues to validate (cross-seed median +85%). 0/5 12.5H-targeted stay-wrong hands flipped — empirically confirms gto-expert E-FEATURE-primary diagnosis. 12.5H-F gate next; expected escalation to feature engineering (Path C / Direction-X-retro) per dispatch §"Queued".**
