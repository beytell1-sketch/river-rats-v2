---
date: 2026-05-06
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · Owner · ML-ARCHITECT (advisory) · GTO-EXPERT (review) · QC stream
re: Phase 12.5K-A — v9 student trainer run (hybrid weighting; combined corpus)
status: IMPLEMENTATION + RUN COMPLETE — model promoted; awaiting QC + reviews
---

# Phase 12.5K-A — v9 student trainer report (hybrid weighting)

12.5K-A RUN COMPLETE; median-litmus seed promoted to canonical (cleared v9-3way-v2.2 baseline).

Master HEAD at run time: `44089bb873480cb81818becb00acf2c98f267cd8`. Run timestamp (UTC): `2026-05-06T23:30:08Z`.

## Section A — training metadata

- Corpus: `data/corpus_combined_788_2026-05-06.jsonl` (joined rows: 788)
- Labels: `data/corpus_combined_788_labels_2026-05-06.jsonl`
- Warm-start requested: `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- Warm-start resolution: requested path IS git-tracked
- Warm-start resolved: `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- Pre-pad mode: `metadata_bump` (blueprint §4)
- Test size: 0.2
- Seeds: 7,8,9,10,11,12,13,14,15,16,17,18,19
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
prepad: bumped num_feature 45 → 61 → /tmp/prepad_v9_27yjev04.json
```

### Schema discoveries surfaced during 12.5D

1. **Join key**: blueprint §6 + ml-architect §12 cited `corpus.source_situation_id == labels.ref_id` as the join key, verified on row 1. Subsequent rows (cohort 2, indices 100-493) have `situation_id` instead of `source_situation_id`, and `labels.ref_id` is heterogeneous (mix of `d####_POS_street` and `PILOT_###` IDs). The universally-populated canonical key is `pilot_hand_id` (494/494 in both files). Trainer joins on `pilot_hand_id`. Spec INTENT (494-hand training) is preserved.

2. **Path Y inference boundary**: `reference_evaluator.evaluate_variants` builds inference arrays via `gto_model.GtoOracle.features_from_dict` which iterates `gto_model.FEATURE_COLUMNS` (length 55). The student model expects 59 features. Path Y forbids extending `gto_model.FEATURE_COLUMNS`, so the student's reference-set evaluation uses an in-module 59-feature inference helper (`_StudentInference` + `_evaluate_student_one_hand`) that mirrors `reference_evaluator._evaluate_one_hand` logic with STUDENT_FEATURE_COLUMNS_V9. Baselines (38/45 features) continue to use `evaluate_variants` as-is.

### Per-seed training summary

|seed|train|test|acc|acc(weighted)|rounds|gate23 drop check|gate23 overfit check|
|---|---|---|---|---|---|---|---|
|7|630|158|0.943|0.952|761|WARN|PASS|
|8|630|158|0.956|0.968|812|WARN|PASS|
|9|630|158|0.949|0.955|552|WARN|PASS|
|10|630|158|0.968|0.977|424|WARN|PASS|
|11|630|158|0.956|0.966|469|WARN|PASS|
|12|630|158|0.924|0.921|515|WARN|WARN|
|13|630|158|0.937|0.947|564|WARN|PASS|
|14|630|158|0.924|0.954|706|WARN|PASS|
|15|630|158|0.949|0.974|681|WARN|PASS|
|16|630|158|0.949|0.962|425|WARN|PASS|
|17|630|158|0.956|0.964|585|WARN|PASS|
|18|630|158|0.937|0.945|929|WARN|PASS|
|19|630|158|0.937|0.944|483|WARN|PASS|
|mean|—|—|0.945±0.013|0.956±0.014|—|—|—|

Selected seed (median solver-corrected litmus): **seed 12**

### Held-out classification report (chosen seed)

|class|precision|recall|f1|support|
|---|---|---|---|---|
|FOLD|0.938|0.938|0.938|16|
|CHECK|0.969|0.939|0.954|66|
|CALL|0.917|0.688|0.786|16|
|BET|0.889|0.941|0.914|34|
|RAISE|0.867|1.000|0.929|26|

### Held-out confusion matrix (chosen seed; rows=true, cols=pred; class order = ACTION_CLASSES)

```
          FOLD  CHECK   CALL    BET  RAISE
  FOLD      15      0      1      0      0
 CHECK       0     62      0      4      0
  CALL       1      0     11      0      4
   BET       0      2      0     32      0
 RAISE       0      0      0      0     26
```

## Section B — reference-evaluator results (Gate 2.4)

Solver-correction overlay: applied to ['MW-30', 'MW-46', 'MW-47'] per `memory/reference_corrections.md`. MW-31, MW-50 NOT applied (unverified per blueprint §5.3).

### Per-seed student litmus (solver-corrected) — full sweep

|seed|raw|solver-corrected|
|---|---|---|
|7|34/40|33/40|
|8|34/40|33/40|
|9|34/40|33/40|
|10|34/40|33/40|
|11|34/40|33/40|
|12|34/40|33/40|
|13|34/40|33/40|
|14|34/40|33/40|
|15|34/40|33/40|
|16|34/40|33/40|
|17|35/40|34/40|
|18|34/40|33/40|
|19|34/40|33/40|
|mean|—|33.08/40 (std 0.27)|

### Chosen seed (12) cross-model litmus

|model|raw|solver-corrected|
|---|---|---|
|v9-student (chosen seed)|34/40|33/40|
|gto_model_v9_3way_v2.2.json|34/40|33/40|

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
Pass overfit check (no feature >30% importance): **False**

### v2.4 P1 blocker importances (the migration's load-bearing features)

|feature|importance|on drop list?|
|---|---|---|
|`nut_flush_block`|0.0036|YES — FLAG|
|`flush_draw_block_pct`|0.0219|no|
|`straight_draw_block_pct`|0.0026|YES — FLAG|
|`nut_made_block_pct`|0.0076|YES — FLAG|

### Top 15 features by importance (chosen seed)

|feature|importance|
|---|---|
|`flush_draw_rank`|0.4194|
|`is_monster`|0.0572|
|`has_flush_draw`|0.0431|
|`facing_bet`|0.0324|
|`num_opponents`|0.0317|
|`equity_margin`|0.0291|
|`nut_blocker_overcard_count`|0.0246|
|`raw_equity`|0.0231|
|`flush_draw_block_pct`|0.0219|
|`to_call`|0.0186|
|`equity_vs_range`|0.0171|
|`is_paired`|0.0157|
|`better_hand_pct`|0.0151|
|`improvement_probability`|0.0149|
|`flush_block_pct`|0.0127|

### Below-1% drop list (chosen seed)

|feature|importance|
|---|---|
|`pot_odds`|0.0099|
|`bet_to_pot`|0.0099|
|`hand_rank`|0.0095|
|`worse_hand_pct`|0.0092|
|`villain_top_pair_plus_pct`|0.0092|
|`is_strong_made`|0.0088|
|`hand_category`|0.0086|
|`villain_draw_pct`|0.0080|
|`is_ip`|0.0078|
|`nut_made_block_pct`|0.0076|
|`hero_range_percentile`|0.0076|
|`board_favour`|0.0074|
|`pot_size`|0.0072|
|`hero_position`|0.0071|
|`danger_score`|0.0067|
|`is_preflop_aggressor`|0.0067|
|`villain_medium_made_pct`|0.0065|
|`villain_aggression_count`|0.0065|
|`villain_checked_back`|0.0064|
|`villain_air_pct`|0.0062|
|`spr`|0.0058|
|`is_rainbow`|0.0049|
|`has_straight_draw`|0.0049|
|`board_adjusted_hrp`|0.0048|
|`draw_outs`|0.0047|
|`flush_danger`|0.0046|
|`overcard_outs`|0.0044|
|`villain_range_capped`|0.0042|
|`villain_position`|0.0041|
|`connectivity_score`|0.0037|
|`nut_flush_block`|0.0036|
|`villain_call_count`|0.0034|
|`high_card_rank`|0.0032|
|`villain_fold_equity_estimate`|0.0028|
|`straight_draw_block_pct`|0.0026|
|`straight_danger`|0.0026|
|`street`|0.0025|
|`is_made_hand`|0.0000|
|`is_monotone`|0.0000|
|`is_two_tone`|0.0000|
|`is_double_paired`|0.0000|
|`is_3bet_pot`|0.0000|
|`num_callers_to_bet`|0.0000|
|`facing_raise`|0.0000|
|`has_showdown_value`|0.0000|
|`bet_call_multiway_oop_raise_pressure_index`|0.0000|

### Above-30% overfit warning list (chosen seed)

|feature|importance|
|---|---|
|`flush_draw_rank`|0.4194|

## Section E — 12.5D vs 12.5D' delta

Compares this run's chosen-seed metrics against the merged 12.5D baseline (PR #126, master `d7d2cdd`, chosen seed = 4, pure-confidence weighting). Same hyperparameters, same seed list, same warm-start anchor — only the `sample_weight` computation changed (confidence × class_weight, cap 3.0, per ml-architect Q3).

### Litmus delta (per-seed solver-corrected)

|seed|12.5D|12.5D'|Δ|
|---|---|---|---|
|7|31/40|33/40|+2|
|8|30/40|33/40|+3|
|9|30/40|33/40|+3|
|10|31/40|33/40|+2|
|11|31/40|33/40|+2|
|12|None/40|33/40|—|
|13|None/40|33/40|—|
|14|None/40|33/40|—|
|15|None/40|33/40|—|
|16|None/40|33/40|—|
|17|None/40|34/40|—|
|18|None/40|33/40|—|
|19|None/40|33/40|—|
|**median**|**31/40**|**33/40**|**+2**|

### Per-class held-out metrics delta (chosen seed: 12.5D=4 vs 12.5D'=12)

|class|12.5D precision/recall/f1|12.5D' precision/recall/f1|recall Δ|
|---|---|---|---|
|FOLD|0.938/1.000/0.968|0.938/0.938/0.938|-0.062|
|CHECK|0.939/0.939/0.939|0.969/0.939/0.954|+0.000|
|CALL|0.769/0.833/0.800|0.917/0.688/0.786|-0.145|
|BET|0.824/0.824/0.824|0.889/0.941/0.914|+0.117|
|RAISE|0.750/0.500/0.600|0.867/1.000/0.929|+0.500|

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
|`nut_flush_block`|0.0000|0.0036|+0.0036|
|`flush_draw_block_pct`|0.0107|0.0219|+0.0112|
|`straight_draw_block_pct`|0.0071|0.0026|-0.0045|
|`nut_made_block_pct`|0.0056|0.0076|+0.0020|

### Interpretation hints (reviewer-scope)

- **Gate threshold (dispatch):** ≥33 promote, 31-32 STOP/owner-tie-gate, <31 STOP+flag-Q3-wrong
- **This run:** median 33/40 → falls in ≥33 PROMOTE
- gto-expert prediction was 7 shared flip + 2 distinct stay-wrong (predicted student → 36-38/40 range). Empirical: 2/7 shared flipped, 0/2 distinct flipped

## Section D — provenance hashes

- Repo HEAD SHA: `44089bb873480cb81818becb00acf2c98f267cd8`
- Trainer module: `river-rats-core/train_model_v9_student.py` (this PR)
- Warm-start anchor: `river-rats-core/models/gto_model_v9_3way_v2.2.json` SHA256: `9f3845bb2a56e99328261c70c3f34decd669f3e047162eb85c78f926bc366900`
- Output model: `river-rats-core/models/125k_a/v9_3way_125k_a_full.json` SHA256: `fd03779c46aadee83b25e73a67a1af062ea31759a2d79116fea8d234aef1d6cf`
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

**Status: 12.5K-A RUN COMPLETE. Median-litmus seed promoted to `river-rats-core/models/125k_a/v9_3way_125k_a_full.json`. Awaiting QC pre-merge audit + ml-architect/gto-expert review.**

---

# 12.5K-A dispatch-framing addendum (Builder, post-trainer-autoreport)

The above sections (A-D + Stop-condition + References) are the trainer's auto-generated report at run time. The sections below are appended by the builder to address dispatch-specific framing per `MAIN_TERMINAL_PR257_RESOLUTION_AND_125KA_DISPATCH_2026-05-06.md` (PR #260 merged at master `44089bb`).

## §"Pilot 2-seed gate" (per dispatch §"Pilot batch")

Pilot 2-seed (Seeds 5+6) executed in a SEPARATE trainer invocation BEFORE the full 13-seed run. Pilot artefact: `review/comms/PILOT_REPORT_PHASE125K_A_2026-05-06.md`.

| Seed | Reference solver-corrected |
|---|---|
| 5 | 33/40 |
| 6 | 33/40 |

7-seed aggregate (5 from PR #253 + 2 pilot): scores [33, 34, 33, 33, 33, 33, 33] → mean **33.14/40 ± 0.35**.

Pilot gate per dispatch §"Pilot gate":

| Gate criterion | Threshold | Observed | Result |
|---|---|---|---|
| Per-seed solver-corrected scores | Both pilot seeds in [32, 35] | Both at 33 | ✅ PASS |
| Schema integrity | 788/788 join clean; 61-surface; 40-hand reference eval | All present | ✅ PASS |
| 7-seed aggregate | mean ≥ 33.0 AND std ≤ 1.0 | 33.14 / 0.35 | ✅ PASS |

**Pilot gate CLEAR.** Proceeded to full run (Seeds 7-19; 13 additional seeds).

## §"Full 13-seed sweep + 20-seed aggregate" (per dispatch §"Full run")

Per-seed solver-corrected scores (extracted from trainer auto-report Section B table line 128-140):

| Seed | Solver-corrected | Source |
|---|---|---|
| 0 | 33 | PR #253 |
| 1 | **34** | PR #253 |
| 2 | 33 | PR #253 |
| 3 | 33 | PR #253 |
| 4 | 33 | PR #253 |
| 5 | 33 | 12.5K-A pilot |
| 6 | 33 | 12.5K-A pilot |
| 7 | 33 | 12.5K-A full |
| 8 | 33 | 12.5K-A full |
| 9 | 33 | 12.5K-A full |
| 10 | 33 | 12.5K-A full |
| 11 | 33 | 12.5K-A full |
| 12 (chosen median) | 33 | 12.5K-A full |
| 13 | 33 | 12.5K-A full |
| 14 | 33 | 12.5K-A full |
| 15 | 33 | 12.5K-A full |
| 16 | 33 | 12.5K-A full |
| 17 | **34** | 12.5K-A full |
| 18 | 33 | 12.5K-A full |
| 19 | 33 | 12.5K-A full |

### 20-seed aggregate stats

| Metric | Value |
|---|---|
| n (seeds) | 20 |
| seeds at 33/40 | 18 (90%) |
| seeds at 34/40 | 2 (10%; Seeds 1 + 17) |
| **mean** | (18×33 + 2×34)/20 = **33.10/40** |
| **std** | sqrt((2×0.81 + 18×0.01)/20) ≈ **0.30** |
| median | 33/40 |
| 1-σ upper bound | 33.40/40 |
| 1-σ lower bound | 32.80/40 |

### Comparison vs v9-3way-v2.2 baseline

| Quantity | v9-3way-v2.2 baseline | 20-seed (12.5K-A) | Δ |
|---|---|---|---|
| Reference solver-corrected (per trainer cross-model litmus on this run; line 148) | **33/40** | 33.10 ± 0.30 | +0.10 (essentially at-or-slightly-above; 1-σ upper 33.40) |
| Reference solver-corrected (per CLAUDE.md project state cite at design time) | 34/40 | 33.10 ± 0.30 | -0.90 (below; 1-σ upper 33.40 still < 34) |

**Note on baseline arithmetic:** the trainer's cross-model litmus on this run shows v2.2 baseline solver-corrected = 33/40, NOT 34/40 as cited in CLAUDE.md project state. This is a within-run delta (the same run computed both v2.2's score and student's score under the same solver-correction overlay). The trainer's "promoted" status comes from the chosen-seed (33/40) tying baseline (33/40) — the trainer's promotion gate accepts ties. Surface to orchestrator: which baseline number applies to dispatch outcome matrix? Conclusion below is robust to either interpretation.

## §"Variance characterization conclusion" (per dispatch outcome matrix)

| Case (per dispatch) | 20-seed observed | Match? |
|---|---|---|
| Mean ≥ 34.0/40 within 1-σ (PROMOTE; off-ramp B+C) | 33.10 ± 0.30 → 1-σ upper 33.40 < 34.0 | ❌ NO |
| **Mean ≈ 33.20/40 ± 0.40 (variance-bound; replicates 5-seed)** | 33.10 ± 0.30 (replicates PR #253; tighter CI) | ✅ **YES** |
| Mean < 33.0/40 (regression / negative) | 33.10 ≥ 33.0 | ❌ NO |

**Outcome row 2: Variance-bound finding confirmed.** The 20-seed empirical record tightens the 5-seed PR #253 result (33.20 ± 0.40 → 33.10 ± 0.30) without changing its qualitative interpretation: the 12.5J feature-engineering work + 788-corpus 61-surface + same hyperparameters does NOT lift solver-corrected accuracy above the dispatch-cited 34/40 baseline at the 20-seed scale.

Per dispatch §"Sequencing — what fires after 12.5K-A merges": **proceed to 12.5K-B Lever B (hyperparameter sweep) dispatch on this PR's merge.**

The trainer's "promoted" status (chosen seed ties on-run baseline 33/40) is permissive; the dispatch's outcome matrix is what the orchestrator uses to decide next-action. Builder does NOT make the PROMOTE decision per `feedback_orchestrator_decides_not_recommends.md`; orchestrator decides on this PR's review.

## §"Per-stay-wrong subset detail" (per dispatch §"Reference set spot-check")

The trainer's auto-report Section B includes the chosen-seed (Seed 12) per-hand comparison. All 4 stay-wrong continue to diverge at chosen seed:

| ref_id | expert (raw) | expert (solver-corrected) | student (Seed 12) | match? |
|---|---|---|---|---|
| MW-17 | CALL | CALL | FOLD | ❌ DIVERGE |
| MW-40 | BET | BET | CHECK | ❌ DIVERGE |
| MW-45 | RAISE | RAISE | CALL | ❌ DIVERGE |
| MW-47 | CALL | RAISE (corrected) | CALL | ❌ DIVERGE |

### Per-seed × stay-wrong limitation (carried from PR #253)

The trainer's auto-report does NOT externalize per-seed × per-hand predictions for ALL 20 seeds (only the chosen median seed). Per the PR #253 framing addendum's same observation: trainer doesn't save per-seed model artifacts when promotion gate refuses, AND doesn't surface per-seed × per-hand inference inline. This limits the per-stay-wrong cross-seed flip analysis the dispatch requested.

What CAN be inferred: 18/20 seeds at 33/40 means **at most 1 hand flips between the median seed (33) and Seeds 1+17 (34)**. The flip is on a non-stay-wrong hand or a stay-wrong hand offset by another flip. Without per-seed per-hand data, this is unresolvable from this run's outputs.

**Process-improvement candidate (carried from PR #253; non-blocking):** trainer should support `--save-all-seeds` flag OR externalize per-seed × per-hand inference inline. Surfacing for orchestrator/owner consideration.

## §"Provenance" (per CLAUDE.md "Training provenance" addendum)

| Item | Value |
|---|---|
| Trainer module | `river-rats-core/train_model_v9_student.py` (existing; reused) |
| Trainer commit (run-time HEAD) | `44089bb` (post-PR #260 merge) |
| Warm-start anchor | `river-rats-core/models/gto_model_v9_3way_v2.2.json` (git-tracked) |
| Output model artefact | `river-rats-core/models/125k_a/v9_3way_125k_a_full.json` (chosen median Seed 12; ~1.5 MB; SAVED) |
| Per-seed artefacts (Seeds 5-19) | NOT WRITTEN — trainer's design saves only chosen-median-seed model. Dispatch's "15 model artifacts" requirement not satisfied; surfaced as non-blocking process-improvement candidate (same as PR #253) |

## §"Stop conditions" (full record per dispatch §"Stop conditions")

| Condition | Triggered? | Evidence |
|---|---|---|
| Pilot gate fails | NO | All 3 gate criteria PASS |
| Trainer crash on any seed | NO | All 13 full-run seeds completed cleanly |
| Schema mismatch | NO | 788/788 joined cleanly; 61-surface uniform |
| Reference set inference fails on any 40-hand pass | NO | All 20 seeds produced full reference evaluations |
| Solver-as-labels appears | NO | Solver-correction overlay applied per `reference_corrections.md` (canonical use; not solver-as-labels) |
| 20-seed aggregate variance > 1.5 std (high training instability) | NO | std ≈ 0.30 (very tight; well below 1.5 threshold) |

No stop conditions triggered.

## §"What I did NOT do" (per dispatch §"What you do NOT do")

- ❌ Did NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md` UNCHANGED)
- ❌ Did NOT modify `river-rats-core/` source (trainer reused as-is)
- ❌ Did NOT modify BATCH2 reference
- ❌ Did NOT modify the 788-corpus or labels
- ❌ Did NOT change hyperparameters (same config as PR #253; pure variance characterization)
- ❌ Did NOT change warm-start anchor (same v9-3way-v2.2)
- ❌ Did NOT skip the 2-seed pilot gate (executed in separate trainer invocation BEFORE full run)
- ❌ Did NOT make the PROMOTE decision (orchestrator-scope; reports outcome row 2 = variance-bound; orchestrator decides)
- ❌ Did NOT auto-fire 12.5K-B (Lever B; gates on this PR's merge + orchestrator dispatch)

## §"What's blocked / what's queued"

**Cleared by this PR (after merge):**
- 12.5K-B Lever B (hyperparameter sweep) dispatch (variance-bound outcome routes to Lever B per dispatch §"Sequencing")

**Awaiting orchestrator dispatch:**
- 12.5K-B Lever B (next builder fire-now)

**Still queued (later):**
- 12.5K-C Lever C (augmented data; conditional on B outcome)
- 12.5L gate evaluation (gates on 12.5K full sweep complete)

## §"References" (dispatch-required addendum)

- Dispatch (fire trigger): `MAIN_TERMINAL_PR257_RESOLUTION_AND_125KA_DISPATCH_2026-05-06.md` (master `44089bb`, PR #260)
- Pilot artefact (separate trainer report): `review/comms/PILOT_REPORT_PHASE125K_A_2026-05-06.md`
- 12.5K design plan: `review/comms/PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md` (master `9798007`, PR #257)
- 12.5J-E source (5-seed mean 33.20/40): PR #253 master `2b6aa02`
- Source corpus: `data/corpus_combined_788_2026-05-06.jsonl` (master `48084c3`, PR #222)
- Source labels: `data/corpus_combined_788_labels_2026-05-06.jsonl` (master `48084c3`, PR #222)
- Warm-start anchor: `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- Trainer module: `river-rats-core/train_model_v9_student.py` (existing; reused per dispatch builder-discretion clause)
- v9-3way-v2.2 baseline: 34/40 raw / 33/40 solver-corrected (per trainer cross-model litmus on this run); CLAUDE.md project state cite was 34/40 — surface arithmetic delta to orchestrator
- CLAUDE.md "Training provenance" addendum: `review/comms/PLAN_CONSOLIDATED_2026-04-15.md` §5.1
- Memory: `feedback_pilot_first_for_long_jobs.md` (2-seed pilot gate executed in separate invocation; binding); `feedback_orchestrator_decides_not_recommends.md` (variance-bound outcome → orchestrator decides 12.5K-B fire); `feedback_quality_default_no_ask.md` (slow-quality A→B→C sequence honored); `feedback_solver_vs_expert_labels.md` (solver-correction overlay applied; not used as training labels)

**Builder-framing status: 12.5K-A Lever A complete. 20-seed mean 33.10/40 ± 0.30 (variance-bound finding confirmed; outcome matrix row 2). Per-seed × stay-wrong limitation persists (carry from PR #253). PR opens for QC audit per dispatch §"QC stream — what you audit"; builder ready for 12.5K-B Lever B dispatch on this PR's merge.**
