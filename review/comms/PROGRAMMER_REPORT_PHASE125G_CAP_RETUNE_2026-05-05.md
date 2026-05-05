---
date: 2026-05-05
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · Owner · ML-ARCHITECT (advisory) · GTO-EXPERT (review) · QC stream
re: Phase 12.5G — v9 student trainer run (hybrid weighting; combined corpus)
status: BUILDER BLOCKED — 12.5G implementation + 5-seed run complete; gate did not promote; model NOT promoted
---

# Phase 12.5G — v9 student trainer report (hybrid weighting)

12.5G RUN COMPLETE; median seed below v9-3way-v2.2 baseline. Per dispatch gate threshold the model was NOT promoted. Section E quantifies the delta vs 12.5D baseline.

Master HEAD at run time: `1bd464e511ded3d240828befae15d5777340680a`. Run timestamp (UTC): `2026-05-05T21:01:59Z`.

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
- Class-weight cap (hybrid): `4.0`
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
prepad: bumped num_feature 45 → 59 → /tmp/prepad_v9_adjhvh3m.json
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

Selected seed (median solver-corrected litmus): **seed 3**

### Held-out classification report (chosen seed)

|class|precision|recall|f1|support|
|---|---|---|---|---|
|FOLD|1.000|1.000|1.000|15|
|CHECK|0.980|0.889|0.932|54|
|CALL|0.929|0.929|0.929|14|
|BET|0.793|0.958|0.868|24|
|RAISE|0.929|0.929|0.929|14|

### Held-out confusion matrix (chosen seed; rows=true, cols=pred; class order = ACTION_CLASSES)

```
          FOLD  CHECK   CALL    BET  RAISE
  FOLD      15      0      0      0      0
 CHECK       0     48      0      6      0
  CALL       0      0     13      0      1
   BET       0      1      0     23      0
 RAISE       0      0      1      0     13
```

## Section B — reference-evaluator results (Gate 2.4)

Solver-correction overlay: applied to ['MW-30', 'MW-46', 'MW-47'] per `memory/reference_corrections.md`. MW-31, MW-50 NOT applied (unverified per blueprint §5.3).

### Per-seed student litmus (solver-corrected) — full sweep

|seed|raw|solver-corrected|
|---|---|---|
|0|32/40|31/40|
|1|34/40|33/40|
|2|34/40|33/40|
|3|33/40|32/40|
|4|33/40|32/40|
|mean|—|32.20/40 (std 0.75)|

### Chosen seed (3) cross-model litmus

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
|`nut_flush_block`|0.0054|YES — FLAG|
|`flush_draw_block_pct`|0.0161|no|
|`straight_draw_block_pct`|0.0034|YES — FLAG|
|`nut_made_block_pct`|0.0065|YES — FLAG|

### Top 15 features by importance (chosen seed)

|feature|importance|
|---|---|
|`flush_draw_rank`|0.2485|
|`has_flush_draw`|0.1597|
|`facing_bet`|0.0466|
|`equity_margin`|0.0419|
|`to_call`|0.0320|
|`raw_equity`|0.0299|
|`is_monster`|0.0279|
|`flush_block_pct`|0.0260|
|`better_hand_pct`|0.0237|
|`equity_vs_range`|0.0197|
|`improvement_probability`|0.0190|
|`num_opponents`|0.0176|
|`flush_draw_block_pct`|0.0161|
|`hand_category`|0.0156|
|`is_paired`|0.0150|

### Below-1% drop list (chosen seed)

|feature|importance|
|---|---|
|`villain_checked_back`|0.0099|
|`villain_draw_pct`|0.0095|
|`villain_air_pct`|0.0093|
|`hero_position`|0.0090|
|`bet_to_pot`|0.0088|
|`hero_range_percentile`|0.0082|
|`villain_medium_made_pct`|0.0082|
|`villain_position`|0.0078|
|`danger_score`|0.0073|
|`pot_size`|0.0072|
|`board_adjusted_hrp`|0.0065|
|`nut_made_block_pct`|0.0065|
|`draw_outs`|0.0064|
|`board_favour`|0.0061|
|`villain_fold_equity_estimate`|0.0058|
|`spr`|0.0056|
|`high_card_rank`|0.0054|
|`nut_flush_block`|0.0054|
|`villain_aggression_count`|0.0052|
|`overcard_outs`|0.0047|
|`villain_range_capped`|0.0036|
|`is_preflop_aggressor`|0.0034|
|`straight_draw_block_pct`|0.0034|
|`straight_danger`|0.0033|
|`street`|0.0032|
|`flush_danger`|0.0027|
|`villain_call_count`|0.0027|
|`is_rainbow`|0.0026|
|`connectivity_score`|0.0025|
|`is_made_hand`|0.0000|
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
|0|31/40|31/40|0|
|1|30/40|33/40|+3|
|2|30/40|33/40|+3|
|3|31/40|32/40|+1|
|4|31/40|32/40|+1|
|**median**|**31/40**|**32/40**|**+1**|

### Per-class held-out metrics delta (chosen seed: 12.5D=4 vs 12.5D'=3)

|class|12.5D precision/recall/f1|12.5D' precision/recall/f1|recall Δ|
|---|---|---|---|
|FOLD|0.938/1.000/0.968|1.000/1.000/1.000|+0.000|
|CHECK|0.939/0.939/0.939|0.980/0.889/0.932|-0.050|
|CALL|0.769/0.833/0.800|0.929/0.929/0.929|+0.096|
|BET|0.824/0.824/0.824|0.793/0.958/0.868|+0.134|
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
|`nut_flush_block`|0.0000|0.0054|+0.0054|
|`flush_draw_block_pct`|0.0107|0.0161|+0.0054|
|`straight_draw_block_pct`|0.0071|0.0034|-0.0037|
|`nut_made_block_pct`|0.0056|0.0065|+0.0009|

### Interpretation hints (reviewer-scope)

- **Gate threshold (dispatch):** ≥33 promote, 31-32 STOP/owner-tie-gate, <31 STOP+flag-Q3-wrong
- **This run:** median 32/40 → falls in 31-32 owner-tie-gate
- gto-expert prediction was 7 shared flip + 2 distinct stay-wrong (predicted student → 36-38/40 range). Empirical: 2/7 shared flipped, 0/2 distinct flipped

## Section D — provenance hashes

- Repo HEAD SHA: `1bd464e511ded3d240828befae15d5777340680a`
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

- Dispatch directive: `review/comms/MAIN_TERMINAL_PHASE125D_DISPATCH_2026-05-03.md` (PR #125, master `e3c0dfc`)
- Blueprint: `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` (PR #122, master `1e4e47e`)
- Pivot directive: PR #119 (master `770b897`)
- ml-architect spec: PR #110 (master `291af80`)
- Solver corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`

**Status: 12.5G RUN COMPLETE; model NOT promoted (median seed 32 < v9-3way-v2.2 baseline 33). See §"Section F" for 12.5E vs 12.5G cap delta and the cap-non-binding finding (load-bearing 12.5H input). Awaiting QC pre-merge audit per dispatch §"QC stream"; orchestrator to dispatch 12.5H per dispatch §"Sequencing" branch (median <33).**

---

## Section F — 12.5E vs 12.5G cap delta (per dispatch §"Step 4")

12.5G is the cap=4.0 retune (B-then-C step 1 per `MAIN_TERMINAL_PHASE125G_DISPATCH_2026-05-05.md`). Identical to 12.5E-E except `--class-weight-cap` parameterized from default 3.0 → 4.0 via the new CLI arg.

### Empirical conclusion: cap=4.0 ≈ cap=3.0 on the 604-hand corpus

**The cap is non-binding at both 3.0 and 4.0.** On the 604-hand combined corpus, the natural per-class inverse-frequency boosts (mean / class_count) are all below 3.0:

| class | count | uncapped boost | cap=3.0 active | cap=4.0 active |
|---|---|---|---|---|
| FOLD | 75 | 1.611 | NO (< 3.0) | NO (< 4.0) |
| CHECK | 271 | 0.446 | NO | NO |
| CALL | 72 | 1.678 | NO | NO |
| BET | 118 | 1.024 | NO | NO |
| **RAISE** | **68** | **1.776** | **NO (< 3.0)** | **NO (< 4.0)** |

(Per train_test_split's 80% train slice: counts ≈ 60/216/57/94/54; mean ≈ 96.6; max boost still ≈ 1.78× on RAISE. Cap=3.0 was binding in 12.5D'/12.5D on the 494 corpus where RAISE was 5.9% (mean/count ≈ 4.3); the 12.5E corpus expansion to 11.26% RAISE share dropped the natural boost below the 3.0 cap, making it non-binding.)

**Translation:** changing the cap from 3.0 → 4.0 is mathematically a no-op on this corpus. The actual sample weights in the trainer are identical between 12.5E-E (cap=3.0) and 12.5G (cap=4.0). Any difference in model outcomes is purely xgboost BLAS-reduction non-determinism on borderline argmax cases — same pattern observed in past phases.

### Litmus delta: 12.5E vs 12.5G

| seed | 12.5E (cap=3.0) | 12.5G (cap=4.0) | Δ |
|---|---|---|---|
| 0 | 32 | 31 | -1 |
| 1 | 33 | 33 | 0 |
| 2 | 32 | 33 | +1 |
| 3 | 32 | 32 | 0 |
| 4 | 32 | 32 | 0 |
| **median** | **32** | **32** | **0** |

Mean 32.2 → 32.4 (negligible; within noise floor). Per-seed std 0.40 → 0.75 (slight noise increase). **Median identical at 32.** Per-seed jiggle ±1 hand on a few seeds is xgboost BLAS variance, NOT a real cap effect.

### MW-47 outcome — Opus 30% prediction did not materialize

Per dispatch §"gto-expert hat":
> Verify MW-47 outcome (Opus prediction: MAY flip under cap=4.0 due to H-FEAT activation interacting with higher RAISE weight)

**Empirical: MW-47 did NOT flip.** Chosen seed (3) outputs CALL on MW-47 (corrected expert RAISE) — same as 12.5E-E chosen seed (2). The 30% Opus probability was over-optimistic given that cap=4.0 doesn't actually change the per-sample weighting in this corpus.

This is consistent with the cap-non-binding finding: if cap=4.0 produces the same sample weights as cap=3.0, the model has the same gradient signal; the same CALL decision on MW-47 is the expected outcome.

### MW-20 outcome — over-aggression persists

Per dispatch §"gto-expert hat":
> Verify MW-20 outcome (newly broken in 12.5E; cap=4.0 likely doesn't fix structural over-rotation but report behavior)

**Empirical: MW-20 still RAISE (over-aggression vs corrected expert CALL).** Same as 12.5E-E. Cap=4.0 didn't worsen it (was a concern under "if cap interacts with H-FEAT to over-fire RAISE"); also didn't fix it.

### Per-class held-out metrics — preserved

Held-out accuracy 0.926 (chosen seed 3) — within 12.5E-E's chosen-seed range (0.893-0.942). No catastrophic class-recall degradation. Cap=4.0 did not introduce class-collapse regression vs cap=3.0.

### Per-hand failure direction classification (per `feedback_failure_direction_classification.md`)

Same pattern as 12.5E-E:
- **Under-aggression** (5): MW-17, MW-25, MW-40, MW-45, MW-47
- **Over-aggression** (3): MW-20, MW-31, MW-46
- **Class-collapse**: NONE

Cap=4.0 doesn't shift the failure direction balance — consistent with cap being non-binding.

### `nut_flush_block` importance — seed-volatility surfaced

12.5G chosen seed (3): `nut_flush_block` = **0.0054** (BELOW 0.02 floor).
12.5E-E chosen seed (2): `nut_flush_block` = **0.0268** (above 0.02 floor).

The seed-to-seed variance on this feature's importance is large. The 12.5E-E "H-FEAT confirmed" reading was a single-seed snapshot; the cross-seed median importance may be lower. **Methodological observation:** feature-importance numbers should be reported as cross-seed median or median ± std, not chosen-seed only. Surfaced for ml-architect's attention; not a STOP signal but informs 12.5H design.

### gto-expert-hat sanity check (per dispatch §"LEAD-PROGRAMMER (gto-expert hat)")

| Check | Outcome |
|---|---|
| Median solver-corrected vs gate (≥33 PROMOTE; <33 → 12.5H) | **32/40 → 12.5H route** |
| MW-47 outcome (Opus prediction: MAY flip) | **NOT flipped** (CALL same as 12.5E-E) |
| MW-20 outcome (cap=4.0 likely doesn't fix structural over-rotation) | **NOT fixed** (RAISE same as 12.5E-E) |
| Held-out class metrics didn't catastrophically degrade | **PASS** (CHECK/CALL recalls preserved; chosen seed acc 0.926) |
| Trainer auto-STOP behavior | fired (chosen 32 < baseline 33); no model promoted; consistent with dispatch's no-promotion fallback |

### Load-bearing 12.5H input package (architect-hat output)

Per dispatch's outcome routing: median <33 → 12.5H corpus expansion with cap=4.0 evidence folded in. The cap=4.0 evidence is:

1. **Cap is non-binding at both 3.0 and 4.0** on the 604-hand corpus. The 12.5E corpus expansion (5.9% → 11.26% RAISE share) lifted the natural inverse-frequency boost below cap=3.0. Further cap increases (e.g., 5.0, 6.0) would also be no-ops on this corpus — same math.
2. **Cap-as-lever empirically refuted.** B's premise was "cap=4.0 may give RAISE the boost it needs to flip MW-47." But cap=4.0 doesn't actually change sample weights vs cap=3.0 here; the lever is structurally absent.
3. **For 12.5H, cap is no longer a meaningful lever on this corpus.** The remaining levers are (a) corpus expansion to add MORE situations of the specific patterns where MW-17/25/40/45/47 fail (E-DIST + E-FEATURE residuals); (b) feature engineering to add features distinguishing MW-31/46 distinct-cause spots (out of Path Y scope; would be 12.5H-prime or beyond); (c) hyperparameter tuning (depth, n_estimators, regularization) — locked at 12.5E-E.
4. **Methodology lesson:** future cap-as-lever decisions should pre-flight check whether the cap actually binds on the candidate corpus before committing to a sweep. The 12.5G dispatch's 30% Opus prediction was correct about the gate-clearing probability *conditional on cap mattering*, but didn't account for the cap being non-binding given the post-12.5E corpus class distribution. The pre-flight check (mean/min(class_count) vs cap) is a 1-line computation.

This package becomes the load-bearing input for 12.5H corpus expansion design (or whatever orchestrator dispatches next).
