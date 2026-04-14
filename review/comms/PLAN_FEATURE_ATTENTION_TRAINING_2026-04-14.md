---
date: 2026-04-14
from: ML Architect
to: Owner (Rupert)
re: Feature attention training experiment — plan for all 4 experiments
status: FOR OWNER REVIEW
prerequisite: PILOT_V2_REPORT_2026-04-14.md (20 pilot hands complete)
blocks: Blueprint (Step 3), Build (Step 5)
---

# Feature Attention Training Experiment — Plan

## Summary Table

| Exp | Name | Mechanism | Independent? | Agent-calls to build |
|-----|------|-----------|-------------|---------------------|
| 0 | Baseline | Raw 54 features, no attention | Yes (runs first, others compare against it) | 0.5 (part of E1 script) |
| 1 | Per-sample masking | Zero out untagged features per row | Independent | 0.5 |
| 2 | Attention weighting | Multiply feature values by level weights | Independent | 0.5 |
| 3 | Auxiliary attention flags | Add 54 binary attention-flag columns | Independent | 0.5 |
| 4 | Intention prediction (Model 2) | Multi-label XGBoost: features → intentions | Independent | 1 (separate model) |

**Experiments 1, 2, 3 are fully independent and can run in parallel.**
**Experiment 4 is independent of 1-3 but uses the same assembled data.**
**Baseline (Exp 0) is embedded in the Exp 1 script — it runs first, then Exp 1 modifies the data and re-trains.**
**Total: 1 Programmer agent-call to implement and run all 4 experiments.**

---

## Data Assembly — How to Extract the 20 Pilot Hands

This is the first task the Programmer must complete before any experiment runs.

### Source

The 20 pilot hand labels live in agent comms files in `review/comms/`. Based on the pilot reports, the union output per hand includes:
- The 54-feature vector (numeric values, same columns as `training-data/train_3way_v3_combined.csv`)
- The consensus action label (FOLD, CHECK, CALL, BET, RAISE)
- The `feature_attention` dict per team (PRIMARY, CONFIRMED, DISCOVERED per feature name)
- The union feature attention (highest level across all 6 teams)
- The intention tags (1-3 per hand from consensus)

The enriched output JSON per hand follows the schema in `prompts/gto_labeller_v2.md` lines 451-507. The `feature_attention` field is a dict mapping feature names (matching `FEATURE_COLUMNS` in `train_model.py`) to level strings.

### Assembly output: three files

The Programmer produces three CSV files. All share the same 20-row index (one row per hand):

**File 1: `training-data/pilot_20_base.csv`**
54 feature columns (matching `FEATURE_COLUMNS` order exactly) + `label` column.
This is the raw features file with no attention modification. Used for Baseline and Exp 3.

**File 2: `training-data/pilot_20_attention.csv`**
Same 54 feature columns + `label` + 54 attention-flag columns named `attn_{feature_name}`.
Attention flags: 1 if the feature appears in the union feature attention for that hand (at any level), 0 otherwise.
Used for Exp 3 (auxiliary features).

**File 3: `training-data/pilot_20_attention_levels.csv`**
Same 54 feature columns + `label` + 54 attention-level columns named `level_{feature_name}`.
Level encoding: PRIMARY=1.0, CONFIRMED=0.7, DISCOVERED=0.5, Untagged=0.1.
Used for Exp 2 (attention weighting).

**File 4: `training-data/pilot_20_intentions.csv`**
54 feature columns + one binary column per unique intention tag observed across all 20 hands.
Each cell is 1 if the hand has that intention tag, 0 otherwise.
No `label` column — this is the Exp 4 target file.
Column names: `intent_{tag_name}` (e.g., `intent_value_thin`, `intent_deny_equity`).

### Assembly process

The Programmer writes a script `river-rats-core/assemble_pilot_data.py` that:
1. Reads the pilot union report (or the individual labeller outputs) to extract feature vectors, labels, union attention tags, and intention tags per hand
2. Verifies all 54 feature column names exactly match `FEATURE_COLUMNS` in `gto_model.py`
3. Verifies all 20 hands are present, no duplicates
4. Verifies label column uses exactly the strings in `ACTION_CLASSES`
5. Writes the four CSV files above
6. Prints a verification summary: 20 rows, correct column counts, label distribution, attention coverage stats

**The Programmer must NOT proceed to any experiment until all four files are verified.**

### Where the pilot feature vectors actually live

The pilot hand situations come from two sources:
- Reconstructed hands (d4534_BB_flop etc.): feature vectors in the factory JSONL files in `training-data/`
- Factory hands (BP1_22 etc.): feature vectors in `training-data/factory_batch*.jsonl` files

The labeller outputs add the `feature_attention`, `action`, and `intentions` fields on top. The Programmer must join these sources: feature vector from the JSONL, enriched fields from the pilot comms outputs.

**Risk flag:** The pilot report shows agent outputs in comms markdown files, not in a structured JSONL. The Programmer must parse the JSON blocks from those files carefully. If the feature vectors are not present in the pilot outputs, they must be retrieved from the original situation files by matching `situation_id`. This join must be verified before assembly completes.

---

## Baseline Model (Experiment 0)

The baseline is not a separate experiment — it is the comparison point for Experiments 1-3. It trains on `pilot_20_base.csv` with no attention modification.

### Training config

Use a reduced XGBoost config appropriate for 20 samples. The production config in `train_model.py` (n_estimators=800, max_depth=5, min_child_weight=5) is tuned for thousands of samples and will massively overfit 20 rows.

**Recommended config for all pilot experiments:**
```
n_estimators: 50
max_depth: 2
learning_rate: 0.1
subsample: 1.0
colsample_bytree: 1.0
min_child_weight: 1
gamma: 0.0
reg_alpha: 0.0
reg_lambda: 1.0
objective: multi:softprob
num_class: 5
```

This is intentionally shallow. The goal is mechanical verification that the pipeline runs and produces output — not model quality. Deep trees on 20 samples will memorise the training set and produce meaningless comparisons between experiments.

Do not use sample_weight (inverse-frequency weighting) for these experiments. With 20 samples and 5 classes, some classes may have 1-2 samples. Inverse weighting will distort comparison across experiments. Use uniform weights.

### Cross-validation strategy

**Do not use the production 80/20 split.** With 20 samples, an 80/20 split gives 16 train / 4 test. That is statistically meaningless and will produce different results on every random seed.

**Use leave-one-out (LOO) cross-validation.** With 20 samples, LOO trains on 19, tests on 1, repeats 20 times. This uses all data for training signal and all data for evaluation. sklearn's `LeaveOneOut` implements this directly.

Is LOO meaningful with 20 samples? For accuracy measurement: no. The confidence interval on 20 LOO predictions is enormous — a single correctly or incorrectly predicted sample moves accuracy by 5 percentage points. Do not report LOO accuracy as a quality metric.

For mechanical verification: yes. LOO is meaningful because it confirms the model trains and predicts without errors across all 20 folds. If LOO completes without crashing, the pipeline is mechanically sound.

**What LOO produces that matters:**
- Confirmation that the model runs on all 20 train/test splits without error
- LOO predictions for all 20 hands — compare these across Exp 0, 1, 2, 3 to see if the modification changes predictions at all
- Feature importance (from the full-data model, not LOO) — compare across experiments

**Additional CV consideration:** With 20 samples and 5 classes, some LOO folds may have only 1 sample from a given class in train. This can cause XGBoost to error if a class is missing from training. The Programmer must handle this: catch the error, log which fold failed, continue. Expect 0-2 fold failures out of 20.

### Baseline output

- LOO predictions for all 20 hands
- Feature importance (top 20 by gain, from full-data model)
- A `results/pilot_exp0_baseline.json` report with: n_samples, n_features, action_distribution, loo_predictions, feature_importance

All four experiments write analogous JSON reports.

---

## Experiment 1: Per-Sample Feature Masking

### What it tests

Whether XGBoost trains and predicts when features are zeroed out on a per-row basis. Each row in the training data has a different set of features zeroed out (those not tagged by any expert for that hand).

### Input data

`pilot_20_base.csv` — read into a numpy array X of shape (20, 54).

### Transformation

For each row i:
1. Look up the union attention set for hand i (the set of feature names tagged by any team at any level)
2. For each feature j not in the attention set: set X[i, j] = 0.0
3. For features in the attention set: leave the value unchanged

Result: a numpy array of shape (20, 54) where each row is partially zeroed. Column count is unchanged — XGBoost still sees 54 features. There is no sparsity in the XGBoost sense; zeroing is just setting numeric values to 0.

**This is not true sparse input.** XGBoost handles truly missing values (NaN) differently from zeros. Setting untagged features to 0.0 treats 0 as a signal value, not as "missing." The implication: XGBoost will learn that 0 means "unattended by experts," which conflates structural zero values (e.g., `is_3bet_pot=0`, `facing_bet=0`) with expert-masked features. This is a known limitation and is acceptable for a mechanical test. Note it in the results.

### Training config

Same reduced config as Baseline.

### Cross-validation

Same LOO strategy.

### Output

- `results/pilot_exp1_masking.json` with: loo_predictions, feature_importance, comparison_to_baseline (how many of 20 LOO predictions differ from Exp 0)
- Print: count of features zeroed per row (average, min, max)

### Mechanical success criteria

**Success:** XGBoost trains on all 20 LOO folds without error. LOO predictions are produced for all 20 hands. At least 1 of the 20 predictions differs from the Baseline (masking has some effect on output).

**Failure:** XGBoost throws an error on the masked input. OR all 20 predictions are identical to Baseline (masking has zero effect — possible if the masked features were already low-signal and zeroing them changes no splits).

**Partial result:** Masking causes 0 prediction differences from Baseline. This is not a mechanical failure — it means zero-masking is too weak a signal for trees at this depth with 20 samples. Flag it and note: weighting (Exp 2) or auxiliary flags (Exp 3) may be more effective.

### Risks

1. **Zero conflation:** Many features have structural zero values (e.g., `has_flush_draw=0`, `is_3bet_pot=0`). Zeroing non-attention features will set some of these to 0 when they are already 0, which is correct, and will set others to 0 when their real value is non-zero, which introduces a different kind of noise. For 20 samples this does not matter mechanically but must be documented.

2. **20 samples cannot detect attention effects:** With 20 rows and many zeroed features, the model may find it impossible to split on features that are zero in most rows. Expect feature importance to shift toward the small number of features that are non-zero across many rows (the mandatory composition features, which are tagged for all BET/RAISE/CALL/FOLD hands). This is expected behaviour, not a failure.

3. **LOO instability:** With 19 train samples per fold and per-row masking, the feature importance will vary significantly across folds. Do not report per-fold importance — report importance from the full 20-sample fit only.

---

## Experiment 2: Attention-Weighted Features

### What it tests

Whether multiplying feature values by attention-level weights shifts feature importance toward expert-tagged features.

### Input data

`pilot_20_attention_levels.csv` — the level encoding per feature per hand (PRIMARY=1.0, CONFIRMED=0.7, DISCOVERED=0.5, Untagged=0.1).

### Transformation

For each row i and each feature j:
`X_weighted[i, j] = X_original[i, j] * level_weight[i, j]`

Where `level_weight[i, j]` comes from the `level_{feature_name}` columns in `pilot_20_attention_levels.csv`.

Result: numpy array of shape (20, 54) with original values scaled by attention weights. All untagged features are attenuated to 10% of their original value; PRIMARY features are unchanged.

**Known XGBoost limitation:** XGBoost uses threshold splits on feature values (`feature_j > threshold`). Multiplying by 0.1 shifts the feature values down but does not change the rank-ordering of samples on that feature. If feature j has values [0.1, 0.3, 0.8] in the original data, after multiplying by 0.1 the values become [0.01, 0.03, 0.08] — the split threshold moves, but the same samples fall on the same side of any split. For continuous features with many distinct values across samples, attention weighting effectively does nothing to tree structure because XGBoost splits are based on relative ordering, not absolute values.

**Where it does matter:** For binary features (0/1), multiplying by 0.1 makes the "1" value become 0.1, which may fall below thresholds that other features create. This is a minor effect. The honest expectation is that Experiment 2 produces the weakest differentiation from Baseline among Experiments 1-3.

Despite this limitation, run the experiment. The mechanical test is whether it runs. The conceptual test is whether importance shifts. Document the XGBoost limitation in the results regardless of outcome.

### Training config

Same reduced config as Baseline. Use the weighted feature matrix X_weighted as input; no separate sample_weight parameter.

### Cross-validation

Same LOO strategy applied to X_weighted.

### Output

- `results/pilot_exp2_weighting.json` with: loo_predictions, feature_importance, comparison_to_baseline
- Side-by-side feature importance table: Baseline vs Exp 2, sorted by Exp 2 importance
- Flag: are the top-10 features in Exp 2 a subset of the union attention set? (This is the meaningful check — if yes, weighting is working in the right direction.)

### Mechanical success criteria

**Success:** XGBoost trains and predicts on X_weighted without error. Feature importance is produced. The top-10 features by importance in Exp 2 have higher average attention level than the top-10 features in Baseline.

**Failure:** XGBoost errors on the weighted input (unexpected — floats are floats). OR feature importance in Exp 2 is identical to Baseline (the rank-ordering limitation confirmed in practice).

**Partial result (expected):** Importance ordering changes slightly but not dramatically. Document the rank-ordering limitation. This outcome does not mean the mechanism is wrong — it means attention weighting is not a natural fit for gradient boosted trees. Exp 3 (binary flags) is a cleaner mechanism for trees.

### Risks

1. **Rank-ordering invariance:** Described above. This is the primary risk. The experiment may show that attention weighting is theoretically sound but mechanically inert for XGBoost. That is a valid finding.

2. **Binary feature distortion:** Multiplying `is_made_hand=1` by 0.1 gives 0.1. Multiplying by PRIMARY weight 1.0 gives 1.0. These are the same binary feature at different scales — XGBoost may split on 0.1 vs 1.0 thresholds inconsistently. Document any features where the weight interaction with binary values creates counter-intuitive importance.

---

## Experiment 3: Auxiliary Attention Flags

### What it tests

Whether adding 54 binary columns (one per feature, 1=tagged by any expert, 0=not tagged) allows XGBoost to learn feature-attention interactions. The model sees 108 columns: 54 original features + 54 binary flags.

### Input data

`pilot_20_attention.csv` — 54 feature columns + 54 `attn_{feature_name}` binary columns + `label` column.

### Transformation

No transformation needed beyond what was done in assembly. The CSV already has the 108-column format.

### Training config

Same reduced config as Baseline but with n_features=108. Note: `colsample_bytree=1.0` in the reduced config ensures all columns are eligible at each split — do not reduce this or the attention flag columns may be systematically excluded.

### Cross-validation

Same LOO strategy.

### Output

- `results/pilot_exp3_auxiliary.json` with: loo_predictions, feature_importance (108 features), comparison_to_baseline
- Separate importance table for: original 54 features vs attention flag 54 features
- Key metric: do any `attn_*` columns appear in the top-20 by importance? If yes, Exp 3 is a clear mechanical success.

### Mechanical success criteria

**Success:** XGBoost trains on the 108-column input without error. At least one `attn_*` flag column has non-zero feature importance. LOO predictions are produced for all 20 hands.

**Failure:** XGBoost errors on 108-column input (not expected). OR all 54 `attn_*` columns have zero importance (the model ignores them entirely, which is possible if the 54 original features already explain all the variance in the labels).

**Why Exp 3 is the strongest of the three mechanisms for trees:** Binary flags are naturally split-able by XGBoost. A split on `attn_equity_vs_range=1` is a direct interaction: "for rows where the expert flagged this feature, the split on equity_vs_range applies differently." This is a clean, non-destructive augmentation — the original feature values are unchanged. If any attention signal is learnable from 20 samples, this experiment is most likely to find it.

### Risks

1. **20 samples cannot learn 108-column interactions.** With only 20 training samples and 108 features, the model is massively underdetermined. XGBoost will find splits on whichever features best separate the labels in the training set, which may bear no relation to which features experts attended to. With max_depth=2, the model can only use 2-3 features per tree — the attention flags will only appear if they happen to split the 20 samples well. Expect low attention flag importance.

2. **Collinearity between original feature and its flag.** `equity_vs_range` is almost always tagged (mandatory composition). So `attn_equity_vs_range=1` for ~17 of 20 rows. This makes the flag near-constant — XGBoost will assign it low or zero importance because a near-constant feature creates no useful split. The flags for features tagged in only a few hands (3-5 out of 20) will have more discriminative power as binary columns.

3. **Unintended interaction:** If a specific feature is always tagged on RAISE hands and never tagged on CHECK hands, the `attn_*` flag will correlate with the label — but this is a confound, not a useful attention signal. At 385 hands this correlation would wash out. At 20 hands it may inflate flag importance for the wrong reason. The results report must flag this risk.

---

## Experiment 4: Intention Prediction (Model 2)

### What it tests

Whether a multi-label XGBoost model can predict intention tags (1-3 per hand) from the 54 raw features. This is a separate model from the action predictor — it predicts WHY, not WHAT.

### Input data

`pilot_20_intentions.csv` — 54 feature columns + binary columns for each unique intention tag observed across the 20 pilot hands.

### Expected intention tags from the pilot

From the pilot v2 report and the labeller vocabulary, the tags observed across 20 hands will be a subset of the seed vocabulary. Based on the hand mix (30% CHECK, 30% BET, 25% FOLD, 10% CALL, 15% RAISE), expect approximately 6-10 unique intention tags across 20 hands. Common ones: `value_thin`, `deny_equity`, `pot_control`, `fold_equity_bluff`, `protection`, `give_up`, `showdown_value`.

The exact tag list is not known until assembly completes — it depends on what the pilot agents produced. The Programmer must enumerate all unique tags found in the pilot outputs and create one binary column per tag.

### Multi-label classification approach

**Do not use XGBoost's native multi-label support.** XGBoost v1.6+ has `multi:multilabel` objective but it is experimental and has known instability with small datasets. Do not use it.

**Use the standard one-vs-rest (OVR) wrapper.** sklearn's `MultiOutputClassifier` wraps any binary classifier and trains one model per label. For each intention tag, train a separate binary `XGBClassifier(objective='binary:logistic')`. With 6-10 tags and 20 samples, this is 6-10 independent binary models.

**Training config for each binary classifier:**
```
n_estimators: 50
max_depth: 2
learning_rate: 0.1
subsample: 1.0
colsample_bytree: 1.0
min_child_weight: 1
gamma: 0.0
objective: binary:logistic
```

### Cross-validation

Same LOO strategy, applied to the multi-label output. For each LOO fold, `MultiOutputClassifier` trains all per-tag models on 19 samples and predicts on 1. This produces a binary prediction vector per held-out sample.

**Degenerate tag warning:** With 20 samples, some intention tags may appear in only 1-3 hands. A binary classifier trained on 19 samples where the positive class has 1-2 examples will almost certainly predict 0 for everything (majority-class collapse). This is expected and is itself a finding: sparse intention tags cannot be learned from 20 samples. The success criterion addresses this below.

### Output

- `results/pilot_exp4_intentions.json` with:
  - Tag list and positive-class frequency per tag
  - Per-tag: number of positive examples, LOO predictions, whether predictions are non-trivial (not all-zero)
  - Feature importance per tag (from full-data binary model for each tag)
  - Comparison: do features that drive intention prediction differ from features that drive action prediction (Baseline)?

### Mechanical success criteria

**Success:** `MultiOutputClassifier` trains and predicts without error. At least 1 of the intention tags produces non-trivial predictions (not all-zero) in LOO evaluation. Feature importance is produced for at least 1 tag.

**Failure:** The wrapper throws an error (not expected with sklearn OVR). OR every tag collapses to all-zero predictions (possible if all tags appear in <=2 hands, making every binary model a majority-class predictor).

**Partial result (likely):** Some tags with 5+ positive examples produce non-trivial predictions. Tags with 1-2 positive examples collapse to all-zero. This is the expected outcome and is a valid finding: with 20 samples, only frequent intention tags are learnable. This informs what minimum frequency is needed in the 385-hand production dataset for intention tags to be trainable.

### Risks

1. **Class imbalance at 20 samples is severe.** If `value_thin` appears in 12 of 20 hands, the binary model learns "almost always predict 1" — not useful. If it appears in 2 of 20, the model learns "always predict 0." The mechanically interesting range is 5-15 positive examples. The Programmer must report class frequency for each tag and flag which tags are in the degenerate range.

2. **Feature importance across tags may be identical.** With only 20 samples, all binary models may converge on the same 2-3 high-signal features (equity_vs_range, villain_top_pair_plus_pct, is_made_hand). If all tags produce identical feature importance, it means 20 samples cannot distinguish what drives different intentions — a valid finding.

3. **Intention tags from the pilot are not yet verified.** The pilot report shows intentions were tagged by each team, but the exact tag strings in the enriched output JSON are what matters. The Programmer must verify that intention strings exactly match the vocabulary in `training-data/tag_vocabulary.json` before building the binary columns. Misspelled or variant tag strings will fragment the binary columns incorrectly.

4. **Multi-output LOO is slow.** 20 folds × 6-10 binary models × 50 trees each = 6,000-10,000 trees total. At 20 samples this is milliseconds per fold. Not a real risk but worth noting for the 385-hand scale.

---

## Leave-One-Out CV Assessment

**Is LOO meaningful at 20 samples?**

For accuracy measurement: No. Each LOO evaluation has a standard error of approximately sqrt(p(1-p)/20) where p is the accuracy estimate. At 70% accuracy, SE ~ 10 percentage points. Experiments will not show statistically distinguishable accuracy differences. Do not compare experiments by LOO accuracy.

For mechanical verification: Yes, for the reasons stated in the Baseline section.

**Alternative to LOO:** A single full-data fit (no CV) would confirm the model runs but would produce overfit feature importance. LOO is better because it confirms the model runs on all 20 possible train/test splits — which means it runs under all data conditions, including the case where one class is absent from training (which LOO will hit for rare classes).

**Recommendation:** Use LOO as specified. Produce LOO predictions for comparison across experiments. Do not use LOO accuracy as the evaluation metric — use it only to confirm mechanical soundness and to generate predictions for cross-experiment comparison.

---

## Comparing Experiments

After all 4 experiments complete, the Programmer produces a summary comparison: `results/pilot_experiment_comparison.json`.

Contents:
- For each hand: Baseline prediction, Exp 1 prediction, Exp 2 prediction, Exp 3 prediction
- Count: how many hands differ from Baseline in each experiment
- Feature importance rank correlation between Baseline and each experiment (Spearman rho on the 54 feature importance scores)
- Binary verdict per experiment: mechanical success or failure

**The key comparison question:** Which mechanism (masking, weighting, auxiliary) causes the most prediction differences from Baseline? Not which is more accurate — which changes model behaviour the most. A mechanism that never changes predictions from Baseline is mechanically inert regardless of whether it is theoretically sound.

---

## File Structure for Implementation

The Programmer creates:
```
river-rats-core/
  assemble_pilot_data.py       — assembly script
  run_pilot_experiments.py     — runs all 4 experiments, writes results

training-data/
  pilot_20_base.csv            — 20 rows x 55 cols (54 features + label)
  pilot_20_attention.csv       — 20 rows x 109 cols (54 features + 54 attn flags + label)
  pilot_20_attention_levels.csv — 20 rows x 109 cols (54 features + 54 level cols + label)
  pilot_20_intentions.csv      — 20 rows x (54 + N_tags) cols

results/
  pilot_exp0_baseline.json
  pilot_exp1_masking.json
  pilot_exp2_weighting.json
  pilot_exp3_auxiliary.json
  pilot_exp4_intentions.json
  pilot_experiment_comparison.json
```

All results files go to `results/` (create the directory). Do NOT put results in `river-rats-core/models/` — that directory is for production models.

---

## Open Questions for Owner Review

1. **Pilot data location.** The assembly script must extract feature vectors from the pilot labeller outputs. The feature vectors for reconstructed hands (d4534_BB_flop etc.) live in the factory JSONL files, and the enriched outputs live in agent comms markdown. Is there a structured JSONL of the v2 pilot outputs, or must the Programmer extract JSON blocks from the comms markdown? This affects assembly difficulty.

2. **Intention tag list.** The exact intention tags produced by the pilot agents are not yet enumerated in this plan. The Programmer discovers them during assembly. If the tag list is very small (3-4 tags, all high-frequency), Exp 4 may be trivial. If tags are diverse, Exp 4 becomes more interesting. Flag to owner when assembly shows the tag distribution.

3. **Experiment 2 expectation setting.** Given the rank-ordering invariance of XGBoost tree splits, Experiment 2 (attention weighting) is likely to show the weakest effect. If the owner wants to know whether attention weighting works for tree models, the honest answer from theory is: probably not, for continuous features. The experiment confirms this empirically. Is this experiment worth running given this prior? Recommendation: yes, run it — the empirical confirmation is valuable before collecting 385 hands.

4. **Results destination.** Results are proposed to go to a new `results/` directory at the repo root. Confirm this is acceptable, or specify an alternative path.

---

## What Happens After This Plan

Per the directive:
1. Owner reviews this plan (Step 2)
2. Architect produces blueprint from approved plan (Step 3) — exact file modifications, function signatures, insertion points
3. Owner reviews blueprint (Step 4)
4. Programmer implements and runs all 4 experiments (Step 5)
5. Owner reviews results (Step 6) — determines whether Pass 1 proceeds with or without feature attention

This plan is the input to Step 3. The blueprint will specify exact function signatures, test cases, and insertion points. The Programmer does not write any code until the blueprint is approved.
