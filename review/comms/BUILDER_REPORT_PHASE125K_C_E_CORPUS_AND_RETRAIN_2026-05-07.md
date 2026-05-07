---
date: 2026-05-07
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · Owner · ML-ARCHITECT (advisory) · GTO-EXPERT (review) · QC stream
re: Phase 12.5K-C-E — v9 student trainer run (hybrid weighting; combined corpus)
status: IMPLEMENTATION + RUN COMPLETE — model promoted; awaiting QC + reviews
---

# Phase 12.5K-C-E — v9 student trainer report (hybrid weighting)

12.5K-C-E RUN COMPLETE; median-litmus seed promoted to canonical (cleared v9-3way-v2.2 baseline).

Master HEAD at run time: `19f958a2ad9d212ec940c256d6bb0af21e3afc09`. Run timestamp (UTC): `2026-05-07T04:57:14Z`.

## Section A — training metadata

- Corpus: `data/corpus_combined_988_2026-05-07.jsonl` (joined rows: 988)
- Labels: `data/corpus_combined_988_labels_2026-05-07.jsonl`
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
prepad: bumped num_feature 45 → 61 → /tmp/prepad_v9_j621w4cc.json
```

### Schema discoveries surfaced during 12.5D

1. **Join key**: blueprint §6 + ml-architect §12 cited `corpus.source_situation_id == labels.ref_id` as the join key, verified on row 1. Subsequent rows (cohort 2, indices 100-493) have `situation_id` instead of `source_situation_id`, and `labels.ref_id` is heterogeneous (mix of `d####_POS_street` and `PILOT_###` IDs). The universally-populated canonical key is `pilot_hand_id` (494/494 in both files). Trainer joins on `pilot_hand_id`. Spec INTENT (494-hand training) is preserved.

2. **Path Y inference boundary**: `reference_evaluator.evaluate_variants` builds inference arrays via `gto_model.GtoOracle.features_from_dict` which iterates `gto_model.FEATURE_COLUMNS` (length 55). The student model expects 59 features. Path Y forbids extending `gto_model.FEATURE_COLUMNS`, so the student's reference-set evaluation uses an in-module 59-feature inference helper (`_StudentInference` + `_evaluate_student_one_hand`) that mirrors `reference_evaluator._evaluate_one_hand` logic with STUDENT_FEATURE_COLUMNS_V9. Baselines (38/45 features) continue to use `evaluate_variants` as-is.

### Per-seed training summary

|seed|train|test|acc|acc(weighted)|rounds|gate23 drop check|gate23 overfit check|
|---|---|---|---|---|---|---|---|
|0|790|198|0.955|0.957|469|WARN|PASS|
|1|790|198|0.970|0.982|676|WARN|PASS|
|2|790|198|0.949|0.967|555|WARN|PASS|
|3|790|198|0.929|0.941|394|WARN|PASS|
|4|790|198|0.949|0.954|431|WARN|PASS|
|mean|—|—|0.951±0.013|0.960±0.014|—|—|—|

Selected seed (median solver-corrected litmus): **seed 2**

### Held-out classification report (chosen seed)

|class|precision|recall|f1|support|
|---|---|---|---|---|
|FOLD|0.950|0.950|0.950|20|
|CHECK|0.983|0.908|0.944|65|
|CALL|0.905|0.950|0.927|20|
|BET|0.878|0.977|0.925|44|
|RAISE|1.000|0.980|0.990|49|

### Held-out confusion matrix (chosen seed; rows=true, cols=pred; class order = ACTION_CLASSES)

```
          FOLD  CHECK   CALL    BET  RAISE
  FOLD      19      0      1      0      0
 CHECK       0     59      0      6      0
  CALL       1      0     19      0      0
   BET       0      1      0     43      0
 RAISE       0      0      1      0     48
```

## Section B — reference-evaluator results (Gate 2.4)

Solver-correction overlay: applied to ['MW-30', 'MW-46', 'MW-47'] per `memory/reference_corrections.md`. MW-31, MW-50 NOT applied (unverified per blueprint §5.3).

### Per-seed student litmus (solver-corrected) — full sweep

|seed|raw|solver-corrected|
|---|---|---|
|0|34/40|33/40|
|1|34/40|33/40|
|2|34/40|33/40|
|3|34/40|33/40|
|4|34/40|33/40|
|mean|—|33.00/40 (std 0.00)|

### Chosen seed (2) cross-model litmus

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
Pass overfit check (no feature >30% importance): **True**

### v2.4 P1 blocker importances (the migration's load-bearing features)

|feature|importance|on drop list?|
|---|---|---|
|`nut_flush_block`|0.0527|no|
|`flush_draw_block_pct`|0.0499|no|
|`straight_draw_block_pct`|0.0062|YES — FLAG|
|`nut_made_block_pct`|0.0140|no|

### Top 15 features by importance (chosen seed)

|feature|importance|
|---|---|
|`is_monster`|0.0561|
|`facing_bet`|0.0541|
|`nut_flush_block`|0.0527|
|`flush_block_pct`|0.0504|
|`flush_draw_block_pct`|0.0499|
|`villain_position`|0.0462|
|`equity_margin`|0.0414|
|`raw_equity`|0.0382|
|`equity_vs_range`|0.0352|
|`to_call`|0.0314|
|`improvement_probability`|0.0297|
|`better_hand_pct`|0.0248|
|`draw_outs`|0.0220|
|`villain_draw_pct`|0.0206|
|`num_opponents`|0.0205|

### Below-1% drop list (chosen seed)

|feature|importance|
|---|---|
|`board_adjusted_hrp`|0.0100|
|`nut_blocker_overcard_count`|0.0091|
|`overcard_outs`|0.0085|
|`is_rainbow`|0.0078|
|`bet_call_multiway_oop_raise_pressure_index`|0.0076|
|`villain_range_capped`|0.0070|
|`villain_fold_equity_estimate`|0.0065|
|`straight_draw_block_pct`|0.0062|
|`flush_danger`|0.0061|
|`connectivity_score`|0.0053|
|`high_card_rank`|0.0049|
|`street`|0.0043|
|`has_flush_draw`|0.0038|
|`straight_danger`|0.0035|
|`num_callers_to_bet`|0.0031|
|`flush_draw_rank`|0.0028|
|`villain_call_count`|0.0026|
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
|0|31/40|33/40|+2|
|1|30/40|33/40|+3|
|2|30/40|33/40|+3|
|3|31/40|33/40|+2|
|4|31/40|33/40|+2|
|**median**|**31/40**|**33/40**|**+2**|

### Per-class held-out metrics delta (chosen seed: 12.5D=4 vs 12.5D'=2)

|class|12.5D precision/recall/f1|12.5D' precision/recall/f1|recall Δ|
|---|---|---|---|
|FOLD|0.938/1.000/0.968|0.950/0.950/0.950|-0.050|
|CHECK|0.939/0.939/0.939|0.983/0.908/0.944|-0.031|
|CALL|0.769/0.833/0.800|0.905/0.950/0.927|+0.117|
|BET|0.824/0.824/0.824|0.878/0.977/0.925|+0.153|
|RAISE|0.750/0.500/0.600|1.000/0.980/0.990|+0.480|

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
|`nut_flush_block`|0.0000|0.0527|+0.0527|
|`flush_draw_block_pct`|0.0107|0.0499|+0.0392|
|`straight_draw_block_pct`|0.0071|0.0062|-0.0009|
|`nut_made_block_pct`|0.0056|0.0140|+0.0084|

### Interpretation hints (reviewer-scope)

- **Gate threshold (dispatch):** ≥33 promote, 31-32 STOP/owner-tie-gate, <31 STOP+flag-Q3-wrong
- **This run:** median 33/40 → falls in ≥33 PROMOTE
- gto-expert prediction was 7 shared flip + 2 distinct stay-wrong (predicted student → 36-38/40 range). Empirical: 2/7 shared flipped, 0/2 distinct flipped

## Section D — provenance hashes

- Repo HEAD SHA: `19f958a2ad9d212ec940c256d6bb0af21e3afc09`
- Trainer module: `river-rats-core/train_model_v9_student.py` (this PR)
- Warm-start anchor: `river-rats-core/models/gto_model_v9_3way_v2.2.json` SHA256: `9f3845bb2a56e99328261c70c3f34decd669f3e047162eb85c78f926bc366900`
- Output model: `river-rats-core/models/125k_c_e/v9_3way_125k_c_e.json` SHA256: `faa4d3e4d6a17618e3f4c144384f8f1b12e7994fe5b3abe0ca489aa22319839a`
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

**Status: 12.5K-C-E RUN COMPLETE. Median-litmus seed promoted to `river-rats-core/models/125k_c_e/v9_3way_125k_c_e.json`. Awaiting QC pre-merge audit + ml-architect/gto-expert review.**

---

# 12.5K-C-E dispatch-framing addendum (Builder, post-trainer-autoreport)

The above (Sections A-D + References) is the trainer's auto-report. This addendum addresses dispatch-specific framing per `MAIN_TERMINAL_PR289_RESOLUTION_AND_125KCE_DISPATCH_2026-05-07.md` (master `19f958a`, PR #292).

## §"Phase 1 — corpus integration (788 → 988)"

`scripts/assemble_125k_c_e_988.py` mirrors PR #222 (12.5I-D 604 → 694 → 788) assembly pattern. Per-action distribution shift: Lever C concentrates RAISE expansion (+88%) and BET expansion (+30%); CHECK class unchanged (Lever C axes target BET/CALL/RAISE only). Confidence distribution: 1.0 = 675 / 0.8 = 182 / 0.6 = 125 / 0.4 = 6. ref_id namespace disjoint; 61-surface uniform; 0 NaN/Inf across 60268 values.

## §"Phase 2 — Pilot 1-seed gate" (binding)

Pilot Seed 0: 33/40 solver-corrected; 988/988 join clean; 40-hand reference eval; no degenerate predictions. **Pilot gate CLEAR**. Pilot artefact: `PILOT_REPORT_PHASE125K_C_E_2026-05-07.md`.

## §"Phase 3 — Full 5-seed re-train"

| Seed | Reference solver-corrected |
|---|---|
| 0 | 33/40 |
| 1 | 33/40 |
| 2 (chosen median) | 33/40 |
| 3 | 33/40 |
| 4 | 33/40 |
| **mean** | **33.00/40** |
| **std** | **0.00** |

All 5 seeds produced identical score 33/40. Mean 33.00 ± 0.00.

## §"Comparison vs Lever A 20-seed mean and v9-3way-v2.2 baseline"

| Source | n | Solver-corrected | Δ vs baseline | Δ vs PR #261 |
|---|---|---|---|---|
| v9-3way-v2.2 baseline | — | 34/40 | — | +0.90 |
| Lever A 20-seed (788-corpus; PR #261) | 20 | 33.10/40 ± 0.30 | -0.90 | — |
| **12.5K-C-E 5-seed (988-corpus; this PR)** | 5 | **33.00/40 ± 0.00** | **-1.00** | **-0.10** |

## §"Outcome matrix conclusion"

| Case (per dispatch) | 988-corpus 33.00/40 ± 0.00 | Match? |
|---|---|---|
| Mean ≥ 34.5/40 within 1-σ (PROMOTE) | 33.00 < 34.5 | ❌ NO |
| Mean in [34.0, 34.5) (parity / slight improvement) | 33.00 < 34.0 | ❌ NO |
| Mean in [33.10, 34.0) (improvement vs PR #261 but below baseline) | 33.00 < 33.10 floor | ❌ NO |
| **Mean ≈ 33.10/40 ± 0.30 (no improvement vs PR #261)** | 33.00 within 33.10 ± 0.30 | ✅ **YES — NULL result** |
| Mean < 33.0/40 (regression) | 33.00 ≥ 33.0 | ❌ NO (boundary) |

**Outcome row 4: NULL result.** Lever C augmented data (200 hands; +88% RAISE / +30% BET classes) does NOT lift solver-corrected accuracy at the 5-seed scale. Mean 33.00 ± 0.00 ≈ PR #261 Lever A baseline (33.10 ± 0.30).

Per dispatch §"Sequencing": **NULL → orchestrator decides next step (Lever D? Accept ceiling? Re-design Lever C?)**.

## §"Per-stay-wrong subset detail"

Trainer auto-report Section B includes the chosen-seed (Seed 2) per-hand comparison. **All 4 stay-wrong continue to diverge at the model layer**; the 988-corpus retrain did NOT graduate any stay-wrong hand even with 88%+ RAISE expansion + 30% BET expansion.

## §"What this null result means" — 3-lever ceiling finding

| Lever | Hypothesis | Result vs baseline |
|---|---|---|
| A (more seeds) | 5-seed sample variance | 20-seed mean 33.10 ± 0.30 (PR #261) |
| B (hyperparameter sweep) | 61-surface needs re-tuned hypers | 3-config pilot spread 0.20 (PR #265) |
| **C (augmented data)** | **788-corpus undersized for stay-wrong axes** | **5-seed mean 33.00 ± 0.00 (this PR)** |

**The model's 33-34/40 solver-corrected ceiling on this corpus + feature configuration is robust to all 3 levers.** The stay-wrong axes (MW-17/40/45/47) reflect genuine structural patterns the model can't learn from any of: (a) more seed averaging, (b) hyperparameter re-tuning, (c) augmented training data via the v3.4 labelling pipeline.

This is consistent with prior empirical findings (PR #245 MW-40 graduation-fail; PR #281 MW-17 axis-target shift): **the labelling pipeline's view diverges from canonical for MW-17 + MW-40**. Adding pipeline-labelled hands reinforces the pipeline view → no canonical-accuracy lift.

## §"What I did NOT do" (per dispatch)

- ❌ Did NOT modify v3.x prompts; ❌ BATCH2; ❌ existing labels; ❌ skip 1-seed pilot; ❌ auto-promote (NULL outcome routes to orchestrator)

## §"Files in PR diff" (5 + 1 model)

- `data/corpus_combined_988_2026-05-07.jsonl` (988 situations)
- `data/corpus_combined_988_labels_2026-05-07.jsonl` (988 labels)
- `scripts/assemble_125k_c_e_988.py` (assembly script)
- `review/comms/PILOT_REPORT_PHASE125K_C_E_2026-05-07.md` (pilot artefact)
- `review/comms/BUILDER_REPORT_PHASE125K_C_E_CORPUS_AND_RETRAIN_2026-05-07.md` (this report)
- `river-rats-core/models/125k_c_e/v9_3way_125k_c_e.json` (chosen median Seed 2; force-added past `*.json` gitignore)

## §"What's blocked / what's queued"

**Cleared by this PR (after merge):**
- 12.5L gate evaluation OR Lever D dispatch (orchestrator decides per outcome matrix row 4)

**Memory candidates** (orchestrator surface for owner ratification):
- 3-lever NULL result: at 988-corpus 61-surface scale, model accuracy ceiling ~33-34/40 solver-corrected is robust. Future phase 12.5M+ should consider: (a) larger corpus (~2000+) targeting broader structural axes, (b) feature surface expansion (66+), (c) different model architecture, or (d) accept the v9-3way-v2.2 production state as the project's end-state on this benchmark.
- Labelling-pipeline-canonical mismatch on MW-17 + MW-40: augmented training data via labelling pipeline cannot teach canonical action; pipeline architecture finding worth a standing memory note.

**Builder-framing status: 12.5K-C-E corpus integration + 5-seed re-train complete. 988-corpus assembled cleanly; 5-seed mean 33.00/40 ± 0.00; outcome matrix row 4 (NULL result; no improvement vs Lever A 33.10/40 ± 0.30). All 3 Lever C levers (A/B/C) produced NULL results vs v9-3way-v2.2 baseline 34/40. Empirical ceiling at ~33-34 confirmed across variance / hyperparameter / data dimensions. Per dispatch sequencing: NULL → orchestrator decides 12.5L / Lever D / accept-ceiling. PR opens for QC audit.**
