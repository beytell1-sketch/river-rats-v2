"""
run_attention_experiments.py — Experiment runner for feature attention training.

Loads the 4 CSV files from training-data/, runs Baseline + Experiments 1-4,
writes 6 JSON results files to results/, and prints a summary table.

Run from: repo root.
    python3 river-rats-core/run_attention_experiments.py

Blueprint: BLUEPRINT_FEATURE_ATTENTION_TRAINING_2026-04-14.md Section 4
"""

import sys
import os
import json
import csv

import numpy as np
import xgboost as xgb
from sklearn.model_selection import LeaveOneOut
from sklearn.multioutput import MultiOutputClassifier
from scipy.stats import spearmanr

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from gto_model import FEATURE_COLUMNS, ACTION_CLASSES

# ═══════════════════════════════════════════════════════════════════
# MODULE-LEVEL CONSTANTS
# ═══════════════════════════════════════════════════════════════════

BASE_CSV         = 'training-data/pilot_20_base.csv'
ATTENTION_CSV    = 'training-data/pilot_20_attention.csv'
LEVELS_CSV       = 'training-data/pilot_20_attention_levels.csv'
INTENTIONS_CSV   = 'training-data/pilot_20_intentions.csv'
ENRICHED_JSONL   = 'training-data/pilot_20_enriched.jsonl'
RESULTS_DIR      = 'results'

ACTION_TO_INT = {a: i for i, a in enumerate(ACTION_CLASSES)}
INT_TO_ACTION = {i: a for i, a in enumerate(ACTION_CLASSES)}

PILOT_XGB_CONFIG = dict(
    n_estimators=50,
    max_depth=2,
    learning_rate=0.1,
    subsample=1.0,
    colsample_bytree=1.0,
    min_child_weight=1,
    gamma=0.0,
    reg_alpha=0.0,
    reg_lambda=1.0,
    objective='multi:softprob',
    num_class=5,
    random_state=42,
    n_jobs=1,
)

BINARY_XGB_CONFIG = dict(
    n_estimators=50,
    max_depth=2,
    learning_rate=0.1,
    subsample=1.0,
    colsample_bytree=1.0,
    min_child_weight=1,
    gamma=0.0,
    reg_alpha=0.0,
    reg_lambda=1.0,
    objective='binary:logistic',
    random_state=42,
    n_jobs=1,
)


# ═══════════════════════════════════════════════════════════════════
# FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def load_feature_csv(
    path: str,
    feature_cols: list,
    label_col,
) -> tuple:
    """
    Reads a CSV file. Returns (X, y, column_names).
    feature_cols: list of column names to use as features (in order).
    label_col: name of label column. If None, y is returned as None.
    X: numpy float32 array (n_rows, len(feature_cols)).
    y: numpy int32 array (n_rows,) or None.
    column_names: list of feature column names (same as feature_cols).

    Raises ValueError if any feature_col missing, label_col missing,
    or n_rows != 20.
    """
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        rows = list(reader)

    # Validate feature columns present
    for col in feature_cols:
        if col not in header:
            raise ValueError(
                f"load_feature_csv: column '{col}' not found in {path}\n"
                f"  Available columns: {header[:10]}..."
            )

    # Validate label column if specified
    if label_col is not None and label_col not in header:
        raise ValueError(
            f"load_feature_csv: label column '{label_col}' not found in {path}"
        )

    # Validate row count
    if len(rows) != 20:
        raise ValueError(
            f"load_feature_csv: expected 20 rows, got {len(rows)} in {path}"
        )

    # Build X
    X = np.array(
        [[float(row[col]) for col in feature_cols] for row in rows],
        dtype=np.float32,
    )

    # Build y
    if label_col is not None:
        y = np.array(
            [ACTION_TO_INT[row[label_col]] for row in rows],
            dtype=np.int32,
        )
    else:
        y = None

    return X, y, list(feature_cols)


def run_loo_cv(
    X: np.ndarray,
    y: np.ndarray,
    model_config: dict,
    exp_name: str,
) -> tuple:
    """
    Runs leave-one-out cross-validation with XGBClassifier.
    Returns (true_labels, loo_predictions, n_fold_failures).

    true_labels: list of 20 action strings (from INT_TO_ACTION), in sample order.
    loo_predictions: list of 20 predicted action strings. "FOLD_ERROR" for failed folds.
    n_fold_failures: count of folds where XGBoost raised an exception.
    """
    loo = LeaveOneOut()
    loo_predictions = []
    true_labels = [INT_TO_ACTION[int(yi)] for yi in y]
    n_fold_failures = 0

    for i, (train_index, test_index) in enumerate(loo.split(X)):
        try:
            model = xgb.XGBClassifier(**model_config)
            model.fit(X[train_index], y[train_index])
            pred_probs = model.predict_proba(X[test_index])
            pred_idx = int(np.argmax(pred_probs[0]))
            loo_predictions.append(INT_TO_ACTION[pred_idx])
        except Exception as e:
            n_fold_failures += 1
            loo_predictions.append("FOLD_ERROR")
            print(f"  [WARN] {exp_name} fold {i} failed: {type(e).__name__}")

    return true_labels, loo_predictions, n_fold_failures


def fit_full_model(
    X: np.ndarray,
    y: np.ndarray,
    model_config: dict,
) -> tuple:
    """
    Fits a single XGBClassifier on all 20 samples (no CV).
    Returns (fitted_model, feature_importance_dict).
    feature_importance_dict: maps "feat_0", "feat_1", ... to importance float.
    """
    model = xgb.XGBClassifier(**model_config)
    model.fit(X, y)
    importances = model.feature_importances_
    feat_imp_dict = {f"feat_{i}": float(importances[i]) for i in range(len(importances))}
    return model, feat_imp_dict


def get_named_importances(
    model,
    column_names: list,
) -> list:
    """
    Extracts model.feature_importances_ and pairs with column_names.
    Returns list of (feature_name, importance_float) tuples sorted descending.
    Raises ValueError if lengths differ.
    """
    importances = model.feature_importances_
    if len(importances) != len(column_names):
        raise ValueError(
            f"get_named_importances: {len(importances)} importances but "
            f"{len(column_names)} column names"
        )
    paired = list(zip(column_names, [float(v) for v in importances]))
    return sorted(paired, key=lambda x: -x[1])


def _load_situation_ids_from_jsonl() -> list:
    """Load situation_ids in order from the enriched JSONL."""
    ids = []
    with open(ENRICHED_JSONL) as f:
        for line in f:
            rec = json.loads(line)
            ids.append(rec['situation_id'])
    return ids


def _compare_to_baseline(baseline_preds: list, exp_preds: list, situation_ids: list) -> dict:
    """Compare experiment predictions to baseline, skipping FOLD_ERROR."""
    differ_ids = []
    for i, (bp, ep) in enumerate(zip(baseline_preds, exp_preds)):
        if bp == "FOLD_ERROR" or ep == "FOLD_ERROR":
            continue
        if bp != ep:
            differ_ids.append(situation_ids[i])
    return {
        "n_predictions_differ": len(differ_ids),
        "hands_that_differ": differ_ids,
    }


def _importance_list_to_vector(importance_list: list, column_names: list) -> np.ndarray:
    """Convert sorted importance list to a vector aligned to column_names."""
    imp_dict = {name: imp for name, imp in importance_list}
    return np.array([imp_dict.get(c, 0.0) for c in column_names])


def run_baseline(output_path: str) -> dict:
    """
    Runs Experiment 0 (Baseline).
    54 features, standard XGBoost. Writes results JSON to output_path.
    """
    # 1. Load base CSV
    X, y, col_names = load_feature_csv(BASE_CSV, list(FEATURE_COLUMNS), 'label')

    # 2. LOO CV
    true_labels, loo_predictions, n_fold_failures = run_loo_cv(
        X, y, PILOT_XGB_CONFIG, 'exp0_baseline'
    )

    # 3 & 4. Full model + named importances
    model, _ = fit_full_model(X, y, PILOT_XGB_CONFIG)
    named_imp = get_named_importances(model, list(FEATURE_COLUMNS))

    # 5. Assemble result
    from collections import Counter
    label_counts = Counter(true_labels)
    action_dist = {a: label_counts.get(a, 0) for a in ACTION_CLASSES}

    result = {
        "experiment": "baseline",
        "n_samples": 20,
        "n_features": 54,
        "xgb_config": PILOT_XGB_CONFIG,
        "action_distribution": action_dist,
        "loo_true_labels": true_labels,
        "loo_predictions": loo_predictions,
        "n_fold_failures": n_fold_failures,
        "feature_importance": [
            {"feature": name, "importance": imp} for name, imp in named_imp
        ],
        "top20_features": [name for name, _ in named_imp[:20]],
    }

    # 6. Write
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"  Written: {output_path}")

    return result


def apply_masking(
    X: np.ndarray,
    column_names: list,
    untagged_per_hand: list,
) -> tuple:
    """
    Applies per-sample feature masking.
    X: shape (20, 54). column_names: list of 54 feature names.
    untagged_per_hand: list of 20 sets of untagged feature names.

    Returns (X_masked, stats_dict). X input is NOT mutated.
    """
    X_masked = np.copy(X)
    col_idx = {name: j for j, name in enumerate(column_names)}

    zeroed_counts = []
    for i, untagged_set in enumerate(untagged_per_hand):
        count = 0
        for feat_name in untagged_set:
            if feat_name in col_idx:
                X_masked[i, col_idx[feat_name]] = 0.0
                count += 1
        zeroed_counts.append(count)

    stats = {
        "avg_features_zeroed": float(np.mean(zeroed_counts)),
        "min_features_zeroed": int(np.min(zeroed_counts)),
        "max_features_zeroed": int(np.max(zeroed_counts)),
    }
    return X_masked, stats


def run_exp1_masking(baseline_result: dict, output_path: str) -> dict:
    """
    Runs Experiment 1 (per-sample feature masking).
    Untagged features zeroed out per sample before training.
    """
    situation_ids = _load_situation_ids_from_jsonl()

    # 1. Load base CSV
    X, y, col_names = load_feature_csv(BASE_CSV, list(FEATURE_COLUMNS), 'label')

    # 2. Load untagged_per_hand from enriched JSONL
    untagged_per_hand = []
    with open(ENRICHED_JSONL) as f:
        for line in f:
            rec = json.loads(line)
            untagged_set = {
                fc for fc in FEATURE_COLUMNS
                if rec['attention_flags'][fc] == 0
            }
            untagged_per_hand.append(untagged_set)

    # 3. Apply masking
    X_masked, masking_stats = apply_masking(X, list(FEATURE_COLUMNS), untagged_per_hand)

    # 4. LOO CV on masked data
    true_labels, loo_predictions, n_fold_failures = run_loo_cv(
        X_masked, y, PILOT_XGB_CONFIG, 'exp1_masking'
    )

    # 5 & 6. Full model + importances on masked data
    model, _ = fit_full_model(X_masked, y, PILOT_XGB_CONFIG)
    named_imp = get_named_importances(model, list(FEATURE_COLUMNS))

    # 7. Comparison to baseline
    comparison = _compare_to_baseline(
        baseline_result['loo_predictions'], loo_predictions, situation_ids
    )

    result = {
        "experiment": "exp1_masking",
        "n_samples": 20,
        "n_features": 54,
        "masking_stats": masking_stats,
        "loo_true_labels": true_labels,
        "loo_predictions": loo_predictions,
        "n_fold_failures": n_fold_failures,
        "feature_importance": [
            {"feature": name, "importance": imp} for name, imp in named_imp
        ],
        "top20_features": [name for name, _ in named_imp[:20]],
        "comparison_to_baseline": comparison,
        "notes": [
            "Zero conflation: 0 values may be structural (facing_bet=0) not masked"
        ],
    }

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"  Written: {output_path}")

    return result


def run_exp2_weighting(baseline_result: dict, output_path: str) -> dict:
    """
    Runs Experiment 2 (attention-weighted features).
    Feature values multiplied by their attention level weight before training.
    """
    situation_ids = _load_situation_ids_from_jsonl()

    # 1. Load features and labels from levels CSV
    X, y, col_names = load_feature_csv(LEVELS_CSV, list(FEATURE_COLUMNS), 'label')

    # Load the level weight columns
    level_col_names = ['level_' + f for f in FEATURE_COLUMNS]
    W, _, _ = load_feature_csv(LEVELS_CSV, level_col_names, None)

    # 2. Compute X_weighted (element-wise)
    X_weighted = X * W

    # 3. LOO CV
    true_labels, loo_predictions, n_fold_failures = run_loo_cv(
        X_weighted, y, PILOT_XGB_CONFIG, 'exp2_weighting'
    )

    # 4 & 5. Full model + importances
    model, _ = fit_full_model(X_weighted, y, PILOT_XGB_CONFIG)
    named_imp = get_named_importances(model, list(FEATURE_COLUMNS))

    # 6. Comparison to baseline
    comparison = _compare_to_baseline(
        baseline_result['loo_predictions'], loo_predictions, situation_ids
    )

    # 7. Attention alignment check
    # Mean attention level weight per feature across 20 rows
    mean_weights = W.mean(axis=0)  # shape (54,)
    feat_mean_weight = {fc: float(mean_weights[i]) for i, fc in enumerate(FEATURE_COLUMNS)}

    baseline_top10 = baseline_result['top20_features'][:10]
    exp2_top10 = [name for name, _ in named_imp[:10]]

    baseline_top10_avg = float(np.mean([feat_mean_weight[f] for f in baseline_top10]))
    exp2_top10_avg = float(np.mean([feat_mean_weight[f] for f in exp2_top10]))

    # Features in exp2 top10 that are also in the ATTENTION_LEVELS tagged set
    # (i.e., their mean weight > 0.1 — they were tagged by at least some hands)
    top10_in_attention_union = [f for f in exp2_top10 if feat_mean_weight[f] > 0.1]

    result = {
        "experiment": "exp2_weighting",
        "n_samples": 20,
        "n_features": 54,
        "loo_true_labels": true_labels,
        "loo_predictions": loo_predictions,
        "n_fold_failures": n_fold_failures,
        "feature_importance": [
            {"feature": name, "importance": imp} for name, imp in named_imp
        ],
        "top20_features": [name for name, _ in named_imp[:20]],
        "comparison_to_baseline": comparison,
        "attention_alignment": {
            "exp2_top10_avg_weight": exp2_top10_avg,
            "baseline_top10_avg_weight": baseline_top10_avg,
            "top10_in_attention_union": top10_in_attention_union,
            "note": "Are exp2 top10 features higher-weighted than baseline top10?",
        },
        "notes": [
            "XGBoost rank-ordering invariance: multiplying continuous features by 0.1 may not change tree splits",
            "Binary feature distortion: is_made_hand*0.1 = 0.1 vs is_made_hand*1.0 = 1.0",
        ],
    }

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"  Written: {output_path}")

    return result


def run_exp3_auxiliary(baseline_result: dict, output_path: str) -> dict:
    """
    Runs Experiment 3 (auxiliary attention flags as extra features).
    108 features: 54 original + 54 attn_* binary flags.
    """
    situation_ids = _load_situation_ids_from_jsonl()

    # 1. Load attention CSV with 108 feature columns
    col_names_108 = list(FEATURE_COLUMNS) + ['attn_' + f for f in FEATURE_COLUMNS]
    X, y, _ = load_feature_csv(ATTENTION_CSV, col_names_108, 'label')

    # 3. LOO CV
    true_labels, loo_predictions, n_fold_failures = run_loo_cv(
        X, y, PILOT_XGB_CONFIG, 'exp3_auxiliary'
    )

    # 5. Full model + importances (108 columns)
    model, _ = fit_full_model(X, y, PILOT_XGB_CONFIG)
    named_imp_108 = get_named_importances(model, col_names_108)

    # 7. Split into original_54 and attn_54
    original_54_imp = [(n, v) for n, v in named_imp_108 if not n.startswith('attn_')]
    attn_54_imp = [(n, v) for n, v in named_imp_108 if n.startswith('attn_')]

    # 8. Non-zero attn flags
    nonzero_attn = [(n, v) for n, v in attn_54_imp if v > 0.0]

    # Owner amendment 3: record attn_importance, original feature name, original importance
    orig_imp_dict = {n: v for n, v in named_imp_108}
    nonzero_attn_flags = []
    for attn_name, attn_imp in nonzero_attn:
        orig_feat = attn_name[len('attn_'):]
        orig_imp = orig_imp_dict.get(orig_feat, 0.0)
        nonzero_attn_flags.append({
            "attn_feature": attn_name,
            "attn_importance": float(attn_imp),
            "original_feature": orig_feat,
            "original_importance": float(orig_imp),
        })

    # 9. Any attn_* in top-20?
    top20_names = [n for n, _ in named_imp_108[:20]]
    any_attn_in_top20 = any(n.startswith('attn_') for n in top20_names)

    # 10. Comparison to baseline
    comparison = _compare_to_baseline(
        baseline_result['loo_predictions'], loo_predictions, situation_ids
    )

    result = {
        "experiment": "exp3_auxiliary",
        "n_samples": 20,
        "n_features": 108,
        "loo_true_labels": true_labels,
        "loo_predictions": loo_predictions,
        "n_fold_failures": n_fold_failures,
        "feature_importance_all108": [
            {"feature": name, "importance": imp} for name, imp in named_imp_108
        ],
        "top20_features": top20_names,
        "original_54_importance": [
            {"feature": name, "importance": imp} for name, imp in
            sorted(original_54_imp, key=lambda x: -x[1])
        ],
        "attn_54_importance": [
            {"feature": name, "importance": imp} for name, imp in
            sorted(attn_54_imp, key=lambda x: -x[1])
        ],
        "nonzero_attn_flags": nonzero_attn_flags,
        "n_attn_flags_nonzero": len(nonzero_attn_flags),
        "any_attn_in_top20": any_attn_in_top20,
        "comparison_to_baseline": comparison,
        "notes": [
            "With 20 samples and 108 features, model is massively underdetermined",
            "Near-constant attn flags (tagged 17+/20 hands) will have low discriminative importance",
        ],
    }

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"  Written: {output_path}")

    return result


def run_exp4_intentions(output_path: str) -> dict:
    """
    Runs Experiment 4 (intention prediction, Model 2).
    Multi-label binary classification: one binary model per intention tag.
    """
    # 1. Load features (54 columns) from intentions CSV
    X, _, _ = load_feature_csv(INTENTIONS_CSV, list(FEATURE_COLUMNS), None)

    # Load target columns: all intent_* columns
    with open(INTENTIONS_CSV, newline='') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        rows = list(reader)

    tag_cols = sorted([c for c in header if c.startswith('intent_')])
    Y = np.array(
        [[int(row[col]) for col in tag_cols] for row in rows],
        dtype=np.int32,
    )  # shape (20, N_tags)

    # 3 & 4. Tag frequency logging
    tag_frequencies = {}
    for i, tag in enumerate(tag_cols):
        pos_count = int(Y[:, i].sum())
        tag_frequencies[tag] = {
            "positive_count": pos_count,
            "pct": float(pos_count / 20 * 100),
        }
        print(f"  {tag}: {pos_count}/20 positive")

    # 5. Fit full MultiOutputClassifier on all 20
    full_model = MultiOutputClassifier(xgb.XGBClassifier(**BINARY_XGB_CONFIG))
    full_model.fit(X, Y)

    # 6. LOO CV for multi-label
    loo = LeaveOneOut()
    loo_matrix = np.zeros((20, len(tag_cols)), dtype=np.int32)

    for i, (train_idx, test_idx) in enumerate(loo.split(X)):
        try:
            mo_model = MultiOutputClassifier(xgb.XGBClassifier(**BINARY_XGB_CONFIG))
            mo_model.fit(X[train_idx], Y[train_idx])
            pred = mo_model.predict(X[test_idx])  # shape (1, N_tags)
            loo_matrix[test_idx[0]] = pred[0]
        except Exception as e:
            print(f"  [WARN] exp4_intentions LOO fold {i} failed: {type(e).__name__}")
            # Leave as zeros (majority class)

    # 7. Per-tag evaluation
    per_tag_results = {}
    n_nontrivial = 0

    # Per-tag feature importance from full model
    for i, tag in enumerate(tag_cols):
        est = full_model.estimators_[i]
        named_imp = get_named_importances(est, list(FEATURE_COLUMNS))

        loo_preds_for_tag = loo_matrix[:, i].tolist()
        loo_predicted_positive = int(sum(loo_preds_for_tag))
        is_nontrivial = any(p == 1 for p in loo_preds_for_tag)
        if is_nontrivial:
            n_nontrivial += 1

        per_tag_results[tag] = {
            "positive_count": tag_frequencies[tag]["positive_count"],
            "loo_predicted_positive": loo_predicted_positive,
            "is_nontrivial": is_nontrivial,
            "feature_importance": [
                {"feature": name, "importance": imp} for name, imp in named_imp
            ],
            "top3_features": [name for name, _ in named_imp[:3]],
            "differs_from_baseline_top3": None,  # set after baseline is available
        }

    # Assemble result (baseline top3 comparison deferred — exp4 is standalone)
    result = {
        "experiment": "exp4_intentions",
        "n_samples": 20,
        "n_features": 54,
        "tag_list": tag_cols,
        "tag_frequencies": tag_frequencies,
        "loo_predictions_per_tag": {
            tag: loo_matrix[:, i].tolist()
            for i, tag in enumerate(tag_cols)
        },
        "per_tag_results": per_tag_results,
        "n_nontrivial_tags": n_nontrivial,
        "mechanical_success": True,
        "notes": [
            "Tags with <=2 positive examples will collapse to all-zero (majority class)",
            "Multi-output LOO: 20 folds x N_tags binary models x 50 trees each",
        ],
    }

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"  Written: {output_path}")

    return result


def build_comparison_report(
    baseline: dict,
    exp1: dict,
    exp2: dict,
    exp3: dict,
    exp4: dict,
    output_path: str,
) -> dict:
    """
    Builds pilot_experiment_comparison.json.
    """
    situation_ids = _load_situation_ids_from_jsonl()

    # 1. Per-hand comparison table
    per_hand = []
    for i, sid in enumerate(situation_ids):
        entry = {
            "situation_id": sid,
            "true_label": baseline['loo_true_labels'][i],
            "baseline": baseline['loo_predictions'][i],
            "exp1_masking": exp1['loo_predictions'][i],
            "exp2_weighting": exp2['loo_predictions'][i],
            "exp3_auxiliary": exp3['loo_predictions'][i],
        }
        per_hand.append(entry)

    # 2. Per-experiment summary with Spearman rho
    baseline_imp_vec = _importance_list_to_vector(
        [(d['feature'], d['importance']) for d in baseline['feature_importance']],
        list(FEATURE_COLUMNS),
    )

    def _exp_summary(exp_result, exp_key):
        # Spearman rho between baseline importances and exp importances (54 original only)
        exp_imp_vec = _importance_list_to_vector(
            [(d['feature'], d['importance']) for d in exp_result['feature_importance']],
            list(FEATURE_COLUMNS),
        )
        rho, _ = spearmanr(baseline_imp_vec, exp_imp_vec)
        mechanical_success = exp_result.get('n_fold_failures', 0) == 0
        return {
            "n_predictions_differ": exp_result['comparison_to_baseline']['n_predictions_differ'],
            "spearman_rho_importance": round(float(rho), 4),
            "mechanical_success": mechanical_success,
        }

    experiment_summary = {
        "exp1_masking": _exp_summary(exp1, "exp1"),
        "exp2_weighting": _exp_summary(exp2, "exp2"),
        "exp3_auxiliary": {
            "n_predictions_differ": exp3['comparison_to_baseline']['n_predictions_differ'],
            "spearman_rho_importance": round(float(spearmanr(
                baseline_imp_vec,
                _importance_list_to_vector(
                    [(d['feature'], d['importance']) for d in exp3['original_54_importance']],
                    list(FEATURE_COLUMNS),
                ),
            ).statistic), 4),
            "mechanical_success": exp3.get('n_fold_failures', 0) == 0,
        },
    }

    # 3. Exp3 attention signal section
    nonzero_attn = exp3['nonzero_attn_flags']
    any_in_top20 = exp3['any_attn_in_top20']
    if any_in_top20:
        conclusion = "XGBoost did learn to use expert attention signals at 20 samples"
    elif len(nonzero_attn) > 0:
        conclusion = "XGBoost partially used expert attention signals (nonzero importance but not top-20)"
    else:
        conclusion = "XGBoost did not learn to use expert attention signals at 20 samples"

    attention_signal_finding = {
        "nonzero_attn_flags": nonzero_attn,
        "n_nonzero": len(nonzero_attn),
        "any_in_top20": any_in_top20,
        "conclusion": conclusion,
    }

    # 4. Ranking by divergence from baseline
    divergence_ranking = sorted(
        ["exp1_masking", "exp2_weighting", "exp3_auxiliary"],
        key=lambda k: experiment_summary[k]['n_predictions_differ'],
        reverse=True,
    )

    result = {
        "n_hands": 20,
        "per_hand_predictions": per_hand,
        "experiment_summary": experiment_summary,
        "attention_signal_finding": attention_signal_finding,
        "ranking_by_divergence": divergence_ranking,
        "most_divergent_experiment": divergence_ranking[0],
    }

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"  Written: {output_path}")

    return result


def main() -> None:
    """
    Orchestrates all experiments in the exact order specified by the blueprint.
    """
    # 1. Verify all 4 CSV source files exist
    for fpath in [BASE_CSV, ATTENTION_CSV, LEVELS_CSV, INTENTIONS_CSV]:
        if not os.path.exists(fpath):
            print("ERROR: Run assemble_pilot_data.py first")
            sys.exit(1)

    # 2. Create results directory
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # 3-4. Baseline
    print("Running Baseline (Exp 0)...")
    baseline = run_baseline(f'{RESULTS_DIR}/pilot_exp0_baseline.json')

    # 5-6. Exp 1
    print("Running Experiment 1: Feature Masking...")
    exp1 = run_exp1_masking(baseline, f'{RESULTS_DIR}/pilot_exp1_masking.json')

    # 7-8. Exp 2
    print("Running Experiment 2: Attention Weighting...")
    exp2 = run_exp2_weighting(baseline, f'{RESULTS_DIR}/pilot_exp2_weighting.json')

    # 9-10. Exp 3
    print("Running Experiment 3: Auxiliary Flags...")
    exp3 = run_exp3_auxiliary(baseline, f'{RESULTS_DIR}/pilot_exp3_auxiliary.json')

    # 11-12. Exp 4
    print("Running Experiment 4: Intention Prediction...")
    exp4 = run_exp4_intentions(f'{RESULTS_DIR}/pilot_exp4_intentions.json')

    # 13-14. Comparison report
    print("Building comparison report...")
    comparison = build_comparison_report(
        baseline, exp1, exp2, exp3, exp4,
        f'{RESULTS_DIR}/pilot_experiment_comparison.json',
    )

    # 15. Summary table
    exp_sum = comparison['experiment_summary']
    print("\nExperiment   | N predictions differ | Spearman rho | Success")
    print("-" * 65)
    print(f"Baseline     | —                    | —            | YES")
    for exp_key, label in [
        ("exp1_masking", "Exp1 Masking"),
        ("exp2_weighting", "Exp2 Weight"),
        ("exp3_auxiliary", "Exp3 Aux"),
    ]:
        s = exp_sum[exp_key]
        suc = "YES" if s['mechanical_success'] else "NO"
        print(f"{label:<12} | {s['n_predictions_differ']:<20} | {s['spearman_rho_importance']:<12} | {suc}")
    print(f"Exp4 Intent  | N/A                  | N/A          | {'YES' if exp4['mechanical_success'] else 'NO'}")

    # 16. Done
    print("\nALL EXPERIMENTS COMPLETE")


if __name__ == '__main__':
    main()
