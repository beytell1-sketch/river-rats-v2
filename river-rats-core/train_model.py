"""
GTO Oracle V3 â€” Model Training Pipeline
========================================

Trains XGBoost multiclass classifier on extracted poker features.
Predicts: FOLD / CHECK / CALL / BET / RAISE

Usage:
    python3 train_model.py              # Train on features_2000.csv
    python3 train_model.py --full       # Train on features_25000.csv
"""

import sys
import os
import json
import csv
import numpy as np
from collections import Counter

# =============================================================================
# Configuration
# =============================================================================

ACTION_CLASSES = ['FOLD', 'CHECK', 'CALL', 'BET', 'RAISE']
ACTION_TO_INT = {a: i for i, a in enumerate(ACTION_CLASSES)}
INT_TO_ACTION = {i: a for i, a in enumerate(ACTION_CLASSES)}

FEATURE_COLUMNS = [
    'street', 'facing_bet', 'pot_size', 'to_call', 'pot_odds', 'bet_to_pot',
    'hero_position', 'villain_position', 'is_ip',
    'hand_category', 'hand_rank', 'is_made_hand', 'is_strong_made',
    'is_monster', 'has_flush_draw', 'has_straight_draw', 'draw_outs',
    'is_monotone', 'is_two_tone', 'is_rainbow', 'is_paired',
    'is_double_paired', 'connectivity_score', 'high_card_rank',
    'danger_score', 'flush_danger', 'straight_danger',
    'raw_equity', 'equity_vs_range',
    'better_hand_pct', 'worse_hand_pct',
    'equity_margin', 'spr',
    'is_3bet_pot', 'villain_aggression_count',
    'villain_checked_back', 'villain_call_count',
    'num_opponents',
    # v9 features (38->45): range composition + current-street action
    'villain_top_pair_plus_pct', 'villain_draw_pct', 'villain_air_pct',
    'villain_range_capped', 'board_favour',
    'num_callers_to_bet', 'facing_raise',
    # v9 features (45->48): blocker + outs + improvement
    'flush_block_pct', 'overcard_outs', 'improvement_probability',
]


# =============================================================================
# Data Loading
# =============================================================================

def load_csv(filepath: str):
    """Load feature CSV into numpy arrays."""
    X_rows = []
    y_rows = []

    with open(filepath) as f:
        reader = csv.DictReader(f)
        # Detect label column from header — fail loudly if not found
        label_col = None
        for candidate in ['label', 'action', 'action_label']:
            if candidate in reader.fieldnames:
                label_col = candidate
                break
        if label_col is None:
            raise ValueError(f"No label column found. Headers: {reader.fieldnames}")
        for row in reader:
            features = [float(row[col]) for col in FEATURE_COLUMNS]
            X_rows.append(features)
            y_rows.append(ACTION_TO_INT[row[label_col]])

    X = np.array(X_rows, dtype=np.float32)
    y = np.array(y_rows, dtype=np.int32)

    print(f"  Loaded {X.shape[0]} samples Ã— {X.shape[1]} features")
    print(f"  Action distribution: {dict(Counter(INT_TO_ACTION[i] for i in y))}")

    return X, y


# =============================================================================
# Training
# =============================================================================

def train_and_evaluate(csv_path: str, output_dir: str = 'river-rats-core/models'):
    """
    Train XGBoost, run cross-validation, report results.

    Args:
        csv_path: Path to features CSV
        output_dir: Where to save model and reports
    """
    from sklearn.model_selection import (
        StratifiedKFold, cross_val_predict, train_test_split
    )
    from sklearn.metrics import (
        accuracy_score, classification_report, confusion_matrix
    )
    import xgboost as xgb

    print("=" * 60)
    print("GTO Oracle V3 â€” Model Training")
    print("=" * 60)

    # Load data
    print("\n--- Loading data ---")
    X, y = load_csv(csv_path)

    # ---- 80/20 Train/Test Split ----
    print("\n--- 80/20 Train/Test Split ---")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"  Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")

    # ---- Train XGBoost ----
    print("\n--- Training XGBoost ---")
    model = xgb.XGBClassifier(
        n_estimators=800,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.75,
        min_child_weight=5,
        gamma=0.2,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective='multi:softprob',
        num_class=5,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1,
        early_stopping_rounds=50,
    )

    # Inverse-frequency sample weights — RAISE capped at 3.0 (see training plan Section 5)
    class_counts = Counter(y_train)
    majority_count = float(class_counts[ACTION_TO_INT['CHECK']])
    raw_weights = {cls: majority_count / count for cls, count in class_counts.items()}
    RAISE_IDX = ACTION_TO_INT['RAISE']
    raw_weights[RAISE_IDX] = min(raw_weights[RAISE_IDX], 3.0)
    sample_weight_train = np.array([raw_weights[label] for label in y_train], dtype=np.float32)

    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        sample_weight=sample_weight_train,
        verbose=False,
    )
    best_iteration = model.best_iteration
    print(f"  Best iteration: {best_iteration}")

    # ---- Evaluate on test set ----
    print("\n--- Test Set Evaluation ---")
    y_pred = model.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    print(f"  Test Accuracy: {test_acc:.4f} ({test_acc:.1%})")

    print("\n  Classification Report:")
    report = classification_report(
        y_test, y_pred,
        target_names=ACTION_CLASSES,
        digits=3,
    )
    print(report)

    print("  Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    # Pretty print
    header = "       " + "  ".join(f"{a:>5}" for a in ACTION_CLASSES)
    print(header)
    for i, row in enumerate(cm):
        row_str = "  ".join(f"{v:5d}" for v in row)
        print(f"  {ACTION_CLASSES[i]:>5} {row_str}")

    # ---- 5-Fold Cross-Validation ----
    print("\n--- 5-Fold Cross-Validation ---")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Train a fresh model for CV (no early stopping on external test set)
    cv_model = xgb.XGBClassifier(
        n_estimators=best_iteration,  # Use best iteration from above
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.75,
        min_child_weight=5,
        gamma=0.2,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective='multi:softprob',
        num_class=5,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1,
    )

    # Sample weights for CV must match the shipped model's weighting
    cv_class_counts = Counter(y)
    cv_majority = float(cv_class_counts[ACTION_TO_INT['CHECK']])
    cv_weights = {cls: cv_majority / count for cls, count in cv_class_counts.items()}
    cv_weights[ACTION_TO_INT['RAISE']] = min(cv_weights[ACTION_TO_INT['RAISE']], 3.0)
    sample_weight_all = np.array([cv_weights[label] for label in y], dtype=np.float32)
    y_cv_pred = cross_val_predict(cv_model, X, y, cv=cv, params={'sample_weight': sample_weight_all})
    cv_acc = accuracy_score(y, y_cv_pred)
    print(f"  5-Fold CV Accuracy: {cv_acc:.4f} ({cv_acc:.1%})")

    print("\n  CV Classification Report:")
    cv_report = classification_report(
        y, y_cv_pred,
        target_names=ACTION_CLASSES,
        digits=3,
    )
    print(cv_report)

    print("  CV Confusion Matrix:")
    cv_cm = confusion_matrix(y, y_cv_pred)
    print(header)
    for i, row in enumerate(cv_cm):
        row_str = "  ".join(f"{v:5d}" for v in row)
        print(f"  {ACTION_CLASSES[i]:>5} {row_str}")

    # ---- Feature Importance ----
    print("\n--- Feature Importance (top 15) ---")
    importances = model.feature_importances_
    feat_imp = sorted(
        zip(FEATURE_COLUMNS, importances),
        key=lambda x: x[1],
        reverse=True,
    )
    for name, imp in feat_imp[:15]:
        bar = "â–ˆ" * int(imp * 200)
        print(f"  {name:>22}: {imp:.4f} {bar}")

    # ---- Version (explicit — not derived from path) ----
    model_version = 'v9_3way_v3'

    # ---- Export Model as JSON ----
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, f'gto_model_{model_version}.json')
    model.save_model(model_path)
    model_size = os.path.getsize(model_path)
    print(f"\n--- Model Exported ---")
    print(f"  Path: {model_path}")
    print(f"  Size: {model_size / 1024:.1f} KB")

    # ---- Save report ----
    report_data = {
        'dataset': csv_path,
        'n_samples': int(X.shape[0]),
        'n_features': int(X.shape[1]),
        'test_accuracy': round(float(test_acc), 4),
        'cv_accuracy': round(float(cv_acc), 4),
        'best_iteration': int(best_iteration),
        'model_size_kb': round(model_size / 1024, 1),
        'feature_importance': {name: round(float(imp), 4)
                               for name, imp in feat_imp},
        'v2_baseline': 0.62,
    }
    report_path = os.path.join(output_dir, f'training_report_{model_version}.json')
    with open(report_path, 'w') as f:
        json.dump(report_data, f, indent=2)
    print(f"  Report: {report_path}")

    # ---- Summary ----
    print(f"\n{'=' * 60}")
    print(f"SUMMARY")
    print(f"{'=' * 60}")
    print(f"  V2 Baseline:        62.0%")
    print(f"  V3 Test Accuracy:   {test_acc:.1%}")
    print(f"  V3 5-Fold CV:       {cv_acc:.1%}")
    improvement = (cv_acc - 0.62) * 100
    print(f"  Improvement:        +{improvement:.1f} percentage points")
    print(f"  Model size:         {model_size / 1024:.1f} KB")
    print(f"{'=' * 60}")

    return model, report_data


# Features to drop for the 45-feature diagnostic run (training plan Section 8 Run 2)
FEATURES_48_ONLY = ['flush_block_pct', 'overcard_outs', 'improvement_probability']


def train_45feat_diagnostic(csv_path: str, output_dir: str = 'river-rats-core/models'):
    """
    Diagnostic run on 45 features only (drops the 3 new v3 features).
    Compares directly against the 48-feature primary run.
    Output: gto_model_v9_3way_v3_45feat.json
    """
    import xgboost as xgb
    from sklearn.model_selection import (
        StratifiedKFold, cross_val_predict, train_test_split
    )
    from sklearn.metrics import accuracy_score, classification_report

    print("=" * 60)
    print("GTO Oracle V3 -- 45-Feature Diagnostic Run")
    print("=" * 60)

    feat_45 = [f for f in FEATURE_COLUMNS if f not in FEATURES_48_ONLY]
    feat_idx = [FEATURE_COLUMNS.index(f) for f in feat_45]

    X_full, y = load_csv(csv_path)
    X = X_full[:, feat_idx]
    print(f"  Using {X.shape[1]} features (dropped: {FEATURES_48_ONLY})")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    class_counts = Counter(y_train)
    majority_count = float(class_counts[ACTION_TO_INT['CHECK']])
    raw_weights = {cls: majority_count / count for cls, count in class_counts.items()}
    RAISE_IDX = ACTION_TO_INT['RAISE']
    raw_weights[RAISE_IDX] = min(raw_weights[RAISE_IDX], 3.0)
    sample_weight_train = np.array([raw_weights[label] for label in y_train], dtype=np.float32)

    model = xgb.XGBClassifier(
        n_estimators=800,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.75,
        min_child_weight=5,
        gamma=0.2,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective='multi:softprob',
        num_class=5,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1,
        early_stopping_rounds=50,
    )
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        sample_weight=sample_weight_train,
        verbose=False,
    )
    best_iteration = model.best_iteration
    print(f"  Best iteration: {best_iteration}")

    y_pred = model.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    print(f"  Test Accuracy: {test_acc:.4f} ({test_acc:.1%})")
    print(classification_report(y_test, y_pred, target_names=ACTION_CLASSES, digits=3))

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_model = xgb.XGBClassifier(
        n_estimators=best_iteration,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.75,
        min_child_weight=5,
        gamma=0.2,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective='multi:softprob',
        num_class=5,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1,
    )
    cv_class_counts = Counter(y)
    cv_majority = float(cv_class_counts[ACTION_TO_INT['CHECK']])
    cv_weights = {cls: cv_majority / count for cls, count in cv_class_counts.items()}
    cv_weights[ACTION_TO_INT['RAISE']] = min(cv_weights[ACTION_TO_INT['RAISE']], 3.0)
    sample_weight_all = np.array([cv_weights[label] for label in y], dtype=np.float32)
    y_cv_pred = cross_val_predict(cv_model, X, y, cv=cv, params={'sample_weight': sample_weight_all})
    cv_acc = accuracy_score(y, y_cv_pred)
    print(f"  5-Fold CV Accuracy: {cv_acc:.4f} ({cv_acc:.1%})")
    print(classification_report(y, y_cv_pred, target_names=ACTION_CLASSES, digits=3))

    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, 'gto_model_v9_3way_v3_45feat.json')
    model.save_model(model_path)
    print(f"\n  Model saved: {model_path}")
    return model


if __name__ == '__main__':
    csv_file = 'training-data/train_3way_v3_combined.csv'

    if not os.path.exists(csv_file):
        print(f"ERROR: {csv_file} not found.")
        sys.exit(1)

    if '--45feat' in sys.argv:
        # Run 2: diagnostic 45-feature comparison (training plan Section 8)
        train_45feat_diagnostic(csv_file)
    else:
        # Run 1: primary 48-feature training (training plan Section 8)
        os.makedirs('river-rats-core/models', exist_ok=True)
        train_and_evaluate(csv_file)
