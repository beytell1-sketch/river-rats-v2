# Training Plan: v9-3way-v3

**Date:** 7 April 2026
**Author:** ML-architect agent
**Status:** AWAITING OWNER REVIEW -- nothing runs until approved

---

## 0. Leakage Gate (Process Guide 2.2) — PASSED

Leakage check completed before training. 5 rows removed:
- 1 from batch 2: SB_Board1_h1 (AsQs = MW-47)
- 4 from base: CALL_Board1_h4 (MW-18), CALL_Board1_h6 (MW-17),
  CALL_Board5_h5 (MW-29/30), CALL_Board8_h2 (MW-46)
- 37 board-only overlaps reviewed and accepted (different hero cards)
- 0 near-matches (minimum feature distance 0.38)

## 1. Dataset Summary

| Property | Value |
|----------|-------|
| File | `training-data/train_3way_v3_combined.csv` |
| Rows | 604 (344 base + 260 batch 2 factory) |
| Features | 48 |
| Label column | `label` |
| Classes | CHECK 190 (31.5%), CALL 145 (24.0%), BET 118 (19.5%), FOLD 117 (19.4%), RAISE 34 (5.6%) |

Row count breakdown: base v3_48 had 349 rows, 5 leaked rows removed
= 344. Batch 2 had 261 situations, 1 leaked row removed = 260.
Total: 344 + 260 = 604.

Compared to v2.2: +260 rows (344 to 604), +3 features (45 to 48).

### 3 New Features (45 to 48)

| # | Feature | Type | Description |
|---|---------|------|-------------|
| 46 | `flush_block_pct` | float 0.0-1.0 | Fraction of villain's flush combos hero blocks |
| 47 | `overcard_outs` | int 0/3/6 | Hero overcards above highest board card, x3 outs |
| 48 | `improvement_probability` | float 0.0-1.0 | Fraction of unseen cards improving hero to two-pair+ |

These features address known v2.1 failure modes: over-calling (blocker
awareness) and residual passivity (improvement/outs awareness). They
require no special encoding -- all numeric, no categoricals.

---

## 2. Bug Fix Required Before Training

**CRITICAL:** The label column in the CSV is `label`, but `load_csv()`
at line 65 of `train_model.py` reads `row.get('action') or row.get('action_label')`.
This will return `None` and crash with a `KeyError` on `ACTION_TO_INT[None]`.

**Fix:** Detect the label column from the CSV header at load time, then
use it consistently. At the top of `load_csv()`:

```python
# Detect label column from header
label_col = None
for candidate in ['label', 'action', 'action_label']:
    if candidate in reader.fieldnames:
        label_col = candidate
        break
if label_col is None:
    raise ValueError(f"No label column found. Headers: {reader.fieldnames}")
```

Then use `row[label_col]` instead of `row.get('action')`. This is
self-documenting and fails loudly if the format changes.

---

## 3. Code Changes Required in `train_model.py`

### 3.1 Label column fix (Section 2 above)

### 3.2 FEATURE_COLUMNS already correct

The `FEATURE_COLUMNS` list (lines 28-48) already includes all 48
features including the 3 new ones (`flush_block_pct`, `overcard_outs`,
`improvement_probability`). No change needed.

### 3.3 Output path and versioning

The current `train_and_evaluate()` has:
- Hardcoded output directory: `/home/rupertbeytell/river-rats/river-rats-complete`
  (old path, does not exist in v2 repo)
- Version detection via string matching on CSV path (lines 217-222)

Changes needed:
- Output directory should be `river-rats-core/models/`
- Model version should be `v9_3way_v3` (not auto-detected from path)
- Default CSV path (line 266) should point to the new training CSV

### 3.4 Class weighting (new -- see Section 5)

Add `sample_weight` computation to the training loop.

### 3.5 Warm-start comparison (new -- see Section 6)

Add optional warm-start path to compare against from-scratch.

---

## 4. Hyperparameters

### 4.1 Base configuration (from-scratch)

| Parameter | v2.1 value | v3 proposed | Rationale |
|-----------|-----------|-------------|-----------|
| `n_estimators` | 500 | 800 | More data (604 vs 348) supports more trees |
| `max_depth` | 6 | 5 | Reduce depth slightly -- 604 rows is still small, avoid overfitting |
| `learning_rate` | 0.1 | 0.05 | Lower LR with more trees for smoother convergence |
| `subsample` | 0.8 | 0.8 | Keep same |
| `colsample_bytree` | 0.8 | 0.75 | Slightly lower -- 48 features means each tree still sees 36 |
| `min_child_weight` | 3 | 5 | Increase to protect RAISE class from being split too aggressively |
| `gamma` | 0.1 | 0.2 | Slightly more conservative splits |
| `reg_alpha` | 0.1 | 0.1 | Keep same |
| `reg_lambda` | 1.0 | 1.0 | Keep same |
| `objective` | `multi:softprob` | `multi:softprob` | Keep same |
| `num_class` | 5 | 5 | Keep same |
| `eval_metric` | `mlogloss` | `mlogloss` | Keep same |
| `early_stopping_rounds` | 30 | 50 | More patience with lower LR |

Rationale for changes: The dataset nearly doubled in size, so we can
afford more trees at a lower learning rate. The depth reduction and
higher min_child_weight compensate for the still-modest sample count,
especially protecting the 34-sample RAISE class from overfitting.

---

## 5. Class Weighting Strategy

### The RAISE problem

34 RAISE samples out of 604 = 5.6%. Without weighting, the model can
achieve 94.4% "accuracy" on RAISE by never predicting it. The v2.1
model already struggled here (1 RAISE failure in reference set).

### Recommendation: inverse-frequency sample weights

Use `sample_weight` computed as inverse class frequency, normalized so
the majority class (CHECK) has weight 1.0:

| Class | Count | Raw weight (190/count) | Capped weight |
|-------|-------|----------------------|---------------|
| CHECK | 190 | 1.00 | 1.00 |
| CALL | 145 | 1.31 | 1.31 |
| BET | 118 | 1.61 | 1.61 |
| FOLD | 117 | 1.62 | 1.62 |
| RAISE | 34 | 5.59 | 3.00 |

**Cap RAISE weight at 3.0** (not full 5.59). Full inverse-frequency
weighting would make each RAISE sample worth 5.59 CHECK samples,
which risks overfitting to RAISE noise. A cap of 3.0 still gives RAISE
3x attention vs CHECK while limiting overfitting risk.

### Why not SMOTE?

SMOTE (synthetic minority oversampling) generates synthetic RAISE
samples by interpolating between existing ones. With only 34 RAISE
samples in a 48-dimensional feature space, the interpolated points are
unreliable -- they may represent poker situations that are physically
impossible or GTO-incorrect. Sample weighting is safer.

### Why not `scale_pos_weight`?

`scale_pos_weight` is for binary classification. For multiclass, use
`sample_weight` passed to `model.fit()`.

---

## 6. Warm-Start vs From-Scratch

### Project history

v2.1 review states: "From-scratch beats warm-start when base model
domain differs from specialist (HU to 3way)." This is established.

However, v3 is NOT a domain change -- it is the same 3-way domain
with more data and 3 additional features. Warm-start from v2.1 should
be evaluated.

### The 45-to-48 feature problem

XGBoost models are tied to their feature count. The v2.1 model was
trained on 45 features. The v3 data has 48 features. You cannot
directly warm-start an XGBoost model with a different feature count.

**Options:**

1. **From-scratch only (recommended).** Train fresh on all 604 rows
   with 48 features. The 73% more data (604 vs 348) makes from-scratch
   viable. The 3 new features cannot be learned via warm-start anyway.

2. **Feature-padded warm-start.** Train v2.1 checkpoint on 45
   features, then retrain with 48 features using the v2.1 tree
   structure as initialization. XGBoost's `process_type='update'`
   mode could theoretically do this, but it does not support adding
   features. Not practical.

3. **Two-phase training.** Train from-scratch on 45 features (604
   rows), compare to v2.1. Then train from-scratch on 48 features
   (604 rows). If 48-feature model is better, ship it. If not,
   investigate which new features are hurting.

### Recommendation

**From-scratch on 48 features** as the primary run. Also train a
**from-scratch 45-feature** variant as a diagnostic comparison -- if
the 48-feature model underperforms the 45-feature model, the new
features are hurting and should be investigated.

---

## 7. Cross-Validation Strategy

### 7.1 Primary: Stratified 5-Fold CV

Same as v2.1. `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.

With 34 RAISE samples across 5 folds = ~6-7 RAISE per fold. This is
marginal but workable. Going to fewer folds (3) would give more RAISE
per fold but less reliable CV estimates.

### 7.2 Per-class metrics mandatory

Report precision, recall, F1 for each class separately. Overall
accuracy can mask RAISE problems. The classification report already
does this.

### 7.3 RAISE-specific validation

After CV, report RAISE confusion specifically:
- How many RAISE samples were predicted correctly?
- What were RAISE samples misclassified as? (CALL is the most likely
  confusion class)
- What were false RAISE predictions? (non-RAISE predicted as RAISE)

---

## 8. Training Runs

Run these in order. Each run produces a model file and training report.

### Run 1: From-scratch, 48 features (primary)

- Config: Section 4 hyperparameters + Section 5 class weights
- Data: all 604 rows, 48 features
- Output: `gto_model_v9_3way_v3.json`

### Run 2: From-scratch, 45 features (diagnostic)

- Config: same hyperparameters, same class weights
- Data: all 604 rows, first 45 features only (drop `flush_block_pct`,
  `overcard_outs`, `improvement_probability`)
- Output: `gto_model_v9_3way_v3_45feat.json`
- Purpose: isolate whether the 3 new features help or hurt

### Comparison table to produce

| Model | 5-Fold CV | RAISE recall | RAISE precision |
|-------|-----------|-------------|----------------|
| Run 1 (48 feat) | ? | ? | ? |
| Run 2 (45 feat) | ? | ? | ? |
| v2.1 baseline | 51.8% | ? | ? |

---

## 9. Feature Importance Gate (Process Guide 2.3)

After training, check:

1. **Every new feature's importance.** If `flush_block_pct`,
   `overcard_outs`, or `improvement_probability` have <1% importance,
   drop them and retrain. Note why they were dropped.

2. **Top feature dominance.** If any single feature exceeds 30%
   importance, investigate for overfitting. In v2.1 the top feature
   was `bet_to_pot` at 10.7% -- healthy distribution.

3. **Compare CV log-loss.** Same folds, same seed, 48-feat vs
   45-feat. If 48-feat has higher log-loss, new features are adding
   noise.

---

## 10. Reference Gate (Process Guide 2.4)

After training, run the 40-hand reference set evaluation. Requirements:

1. **All baselines in same session:** v8, v2.1, v3 evaluated by the
   same `reference_evaluator.py` in one run.
2. **Apply solver corrections** per `memory/reference_corrections.md`:
   MW-30 CALL, MW-46 CALL, MW-47 RAISE.
3. **Report raw AND solver-corrected scores.**
4. **No regression** below v2.1 on any axis.

### Success criteria

| Metric | v2.1 baseline | Minimum for v3 | Target for v3 |
|--------|--------------|----------------|---------------|
| Reference (solver-corrected) | 33/40 (82.5%) | 33/40 (82.5%) | 35/40 (87.5%) |
| RAISE recall (reference) | varies | no regression | improvement |
| 5-Fold CV accuracy | 51.8% | 55% | 60%+ |

**Ship-it threshold:** 33/40 solver-corrected with no regression on
any axis vs v2.1. Below 33/40 = do not ship, investigate regressions.

**Stretch goal:** 35/40 would represent closing 2 of the 7 remaining
failures from v2.1.

---

## 11. Early Stopping Configuration

- **Eval set:** 80/20 stratified train/test split (same as v2.1)
- **Metric:** `mlogloss`
- **Patience:** 50 rounds (increased from 30 due to lower learning rate)
- **Best iteration** from early stopping used as `n_estimators` for
  the CV model (same pattern as current code)

---

## 12. Summary of Code Changes for Architect Blueprint

| File | Change | Lines |
|------|--------|-------|
| `train_model.py` | Add `label` to label column lookup | Line 65 |
| `train_model.py` | Update output directory to `river-rats-core/models/` | Line 81 |
| `train_model.py` | Add sample_weight computation and pass to `model.fit()` | Lines 107-136 |
| `train_model.py` | Update default CSV path | Line 266 |
| `train_model.py` | Add 45-feature comparison run option | New function or CLI flag |
| `train_model.py` | Update version detection for v3 | Lines 217-222 |
| `train_model.py` | Update hyperparameters per Section 4 table | Lines 114-131 |

---

## 13. Open Questions for Owner

1. **RAISE weight cap:** I propose capping RAISE sample weight at 3.0
   (not full inverse-frequency of 5.59). Higher cap = more RAISE
   recall but more RAISE false positives. Lower cap = more
   conservative RAISE predictions. Is 3.0 acceptable, or do you
   prefer a different value?

2. **45-feature diagnostic run:** Is it worth the compute to run a
   45-feature comparison (Run 2), or should we just train 48 features
   and check feature importance? The diagnostic run costs one
   additional training cycle but gives a clean A/B comparison.

3. **CV fold count:** 5-fold gives ~7 RAISE per fold. An alternative
   is 3-fold (~11 RAISE per fold, more stable per-fold estimates but
   less reliable overall CV). Recommendation is 5-fold. Acceptable?

4. **Hyperparameter search:** The proposed config is a single
   informed starting point, not a grid search. Should we run a
   small grid search over `max_depth` (4, 5, 6) and `learning_rate`
   (0.03, 0.05, 0.1) = 9 combinations? This adds compute time but
   may find a better config. Or should we train the proposed config
   first and only grid-search if results are below target?

5. **v2.1 CV baseline:** The v2.1 training report shows CV accuracy
   of 51.8%, which is surprisingly low vs. the 82.5% reference score.
   This gap suggests the reference set is easier than the average
   training sample (expected -- reference set was curated). Should we
   set the CV success threshold relative to v2.1 CV (e.g. >55%) or
   only gate on reference accuracy?
