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
        for row in reader:
            features = [float(row[col]) for col in FEATURE_COLUMNS]
            X_rows.append(features)
            action = row.get('action') or row.get('action_label')
            y_rows.append(ACTION_TO_INT[action])

    X = np.array(X_rows, dtype=np.float32)
    y = np.array(y_rows, dtype=np.int32)

    print(f"  Loaded {X.shape[0]} samples Ã— {X.shape[1]} features")
    print(f"  Action distribution: {dict(Counter(INT_TO_ACTION[i] for i in y))}")

    return X, y


# =============================================================================
# Training
# =============================================================================

def train_and_evaluate(csv_path: str, output_dir: str = '/home/rupertbeytell/river-rats/river-rats-complete'):
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
        n_estimators=500,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=3,
        gamma=0.1,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective='multi:softprob',
        num_class=5,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1,
        early_stopping_rounds=30,
    )

    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
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
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=3,
        gamma=0.1,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective='multi:softprob',
        num_class=5,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1,
    )

    y_cv_pred = cross_val_predict(cv_model, X, y, cv=cv)
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

    # ---- Determine version from data path ----
    if 'v3' in csv_path or '38feat_v3' in csv_path:
        model_version = 'v8'
    elif 'v2' in csv_path or '38feat_v2' in csv_path:
        model_version = 'v7'
    else:
        model_version = 'v6'

    # ---- Export Model as JSON ----
    model_path = os.path.join(output_dir, f'gto_model_{model_version}_38feat.json')
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


if __name__ == '__main__':
    csv_file = '/home/rupertbeytell/river-rats/training_data_38feat_v2/train_action_38.csv'
    if '--full' in sys.argv or '--v1' in sys.argv:
        csv_file = '/home/rupertbeytell/river-rats/training_data_38feat/train_action_38.csv'
    elif '--v3' in sys.argv:
        csv_file = '/home/rupertbeytell/river-rats/training_data_38feat_v3/train_action_38.csv'

    if not os.path.exists(csv_file):
        print(f"ERROR: {csv_file} not found. Run feature extraction first.")
        sys.exit(1)

    train_and_evaluate(csv_file)
