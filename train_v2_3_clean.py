#!/usr/bin/env python3
"""
Train v2.3-clean model — NO class weighting.

Uses the same XGBoost architecture as train_model_v2_2.py but
WITHOUT sample_weight or scale_pos_weight.
"""

import csv
import json
import logging
import os
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'river-rats-core'))

from train_model import _preflight_schema_check
from train_model_v2_2 import (
    ACTION_TO_INT, INT_TO_ACTION, encode, split_feature_columns, build_matrix,
)

logger = logging.getLogger("train_v2_3_clean")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    )
    import xgboost as xgb
    from sklearn.metrics import accuracy_score, classification_report
    from sklearn.model_selection import StratifiedKFold, train_test_split

    csv_path = "training-data/v2_3_clean_training.csv"
    out_model = "river-rats-core/models/v2_3_clean_model.json"
    report_path = "river-rats-core/models/v2_3_clean_training_report.json"

    # Preflight
    _preflight_schema_check(csv_path=csv_path)
    logger.info("Preflight PASSED")

    # Load data
    with open(csv_path, newline="") as f:
        rows = list(csv.DictReader(f))
    logger.info("Loaded %d rows from %s", len(rows), csv_path)

    raw_features, attn_features = split_feature_columns(list(rows[0].keys()))
    feature_order = raw_features + attn_features
    logger.info("Features: %d raw + %d attn = %d total",
                len(raw_features), len(attn_features), len(feature_order))

    X, y = build_matrix(rows, feature_order)
    dist = {INT_TO_ACTION[int(i)]: int(n) for i, n in Counter(y).items()}
    logger.info("Class distribution: %s", dist)

    # 80/20 split
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y,
    )
    logger.info("Train: %d, Test: %d", X_tr.shape[0], X_te.shape[0])

    # Train — NO sample_weight, NO scale_pos_weight
    model = xgb.XGBClassifier(
        n_estimators=800, max_depth=5, learning_rate=0.05,
        objective="multi:softprob", num_class=5,
        eval_metric="mlogloss", use_label_encoder=False,
        random_state=42, early_stopping_rounds=50, verbosity=0,
    )
    model.fit(X_tr, y_tr, eval_set=[(X_te, y_te)], verbose=False)
    best_iter = int(model.best_iteration)
    logger.info("Best iteration: %d", best_iter)

    y_pred = model.predict(X_te)
    test_acc = float(accuracy_score(y_te, y_pred))
    logger.info("Holdout accuracy: %.4f", test_acc)
    logger.info("Per-class:\n%s",
                classification_report(
                    y_te, y_pred,
                    target_names=[INT_TO_ACTION[i] for i in sorted(set(y))],
                    zero_division=0,
                ))

    # 5-fold CV at best_iter, NO weights
    logger.info("--- 5-fold stratified CV (no weights) ---")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_accs = []
    for fold, (tr_idx, te_idx) in enumerate(cv.split(X, y)):
        m = xgb.XGBClassifier(
            n_estimators=best_iter, max_depth=5, learning_rate=0.05,
            objective="multi:softprob", num_class=5, random_state=42,
            verbosity=0, eval_metric="mlogloss",
        )
        m.fit(X[tr_idx], y[tr_idx], verbose=False)
        a = float(accuracy_score(y[te_idx], m.predict(X[te_idx])))
        cv_accs.append(a)
        logger.info("  Fold %d: %.4f", fold + 1, a)
    cv_mean = float(np.mean(cv_accs))
    cv_std = float(np.std(cv_accs))
    logger.info("  Mean CV: %.4f +/- %.4f", cv_mean, cv_std)

    # Save model
    os.makedirs(os.path.dirname(out_model), exist_ok=True)
    model.save_model(out_model)
    logger.info("Saved model: %s", out_model)

    # Save report
    report = {
        "model_version": "v2_3_clean",
        "csv_path": csv_path,
        "out_model_path": out_model,
        "class_weighting": "NONE",
        "n_samples": len(rows),
        "n_features": int(X.shape[1]),
        "class_distribution": dist,
        "best_iteration": best_iter,
        "holdout_test_accuracy": test_acc,
        "cv_accuracies": [float(a) for a in cv_accs],
        "cv_mean": cv_mean,
        "cv_std": cv_std,
    }
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    logger.info("Saved report: %s", report_path)


if __name__ == "__main__":
    main()
