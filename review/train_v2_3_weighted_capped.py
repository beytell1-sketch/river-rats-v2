"""
Option A: Class-weighted retrain with RAISE weight capped at 1.50.

Same as Path A balanced weights (BET=0.38, CHECK=0.97, FOLD=1.83,
CALL=2.39) but RAISE capped from 2.89 to 1.50 to suppress the
systematic RAISE over-prediction on facing-bet CALL spots documented
in FB40_MISS_INVESTIGATION_AND_GATE_TABLE_2026-04-17.md.

Output: river-rats-core/models/v2_3_capped_model.json
"""

from __future__ import annotations

import csv
import json
import logging
import os
import sys
from collections import Counter

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_THIS_DIR)
_CORE = os.path.join(_ROOT, "river-rats-core")
sys.path.insert(0, _CORE)

from train_model_v2_2 import (  # noqa: E402
    ACTION_TO_INT, INT_TO_ACTION, encode, split_feature_columns, build_matrix,
)
from train_model import _preflight_schema_check  # noqa: E402

logger = logging.getLogger("train_v2_3_weighted_capped")

# Cap: RAISE weight clamped to this ceiling.
_RAISE_WEIGHT_CAP = 1.50


def _balanced_class_weights_capped(y: np.ndarray) -> dict:
    """sklearn-style balanced weights with RAISE capped at _RAISE_WEIGHT_CAP.

    All other classes get uncapped balanced weights. RAISE (class 4) is
    clamped to min(balanced, _RAISE_WEIGHT_CAP).
    """
    cnt = Counter(int(v) for v in y)
    n_samples = len(y)
    n_classes = len(cnt)
    weights = {c: n_samples / (n_classes * n) for c, n in cnt.items()}
    # ACTION_TO_INT: RAISE=4
    raise_idx = ACTION_TO_INT["RAISE"]
    if raise_idx in weights:
        weights[raise_idx] = min(weights[raise_idx], _RAISE_WEIGHT_CAP)
    return weights


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    )

    csv_path = os.path.join(_ROOT, "training-data", "v2_3_iter2_training.csv")
    out_model = os.path.join(_CORE, "models", "v2_3_capped_model.json")
    report_path = os.path.join(_CORE, "models", "v2_3_capped_training_report.json")

    # Preflight
    _preflight_schema_check(csv_path=csv_path)

    import xgboost as xgb
    from sklearn.metrics import accuracy_score, classification_report
    from sklearn.model_selection import StratifiedKFold, train_test_split

    logger.info("Loading CSV: %s", csv_path)
    with open(csv_path, newline="") as f:
        rows = list(csv.DictReader(f))
    logger.info("Loaded %d rows", len(rows))

    raw_features, attn_features = split_feature_columns(list(rows[0].keys()))
    feature_order = raw_features + attn_features
    logger.info("Features: %d raw + %d attn = %d total",
                len(raw_features), len(attn_features), len(feature_order))

    X, y = build_matrix(rows, feature_order)
    dist = {INT_TO_ACTION[int(i)]: int(n) for i, n in Counter(y).items()}
    logger.info("Class distribution: %s", dist)

    # 80/20 holdout
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    logger.info("Train: %d, Test: %d", X_tr.shape[0], X_te.shape[0])

    # Balanced class weights with RAISE capped at 1.50
    raw_w = _balanced_class_weights_capped(y_tr)
    sw_tr = np.array([raw_w[int(v)] for v in y_tr], dtype=np.float32)

    weight_table = {INT_TO_ACTION[c]: round(w, 4) for c, w in sorted(raw_w.items())}
    logger.info("Capped class weights (RAISE cap=%.2f): %s",
                _RAISE_WEIGHT_CAP, weight_table)

    model = xgb.XGBClassifier(
        n_estimators=800, max_depth=5, learning_rate=0.05,
        objective="multi:softprob", num_class=5,
        eval_metric="mlogloss", use_label_encoder=False,
        random_state=42, early_stopping_rounds=50, verbosity=0,
    )
    model.fit(
        X_tr, y_tr, sample_weight=sw_tr,
        eval_set=[(X_te, y_te)], verbose=False,
    )
    best_iter = int(model.best_iteration)
    logger.info("Best iteration: %d", best_iter)

    y_pred = model.predict(X_te)
    test_acc = float(accuracy_score(y_te, y_pred))
    logger.info("Holdout test accuracy: %.4f", test_acc)
    logger.info("Per-class:\n%s",
                classification_report(
                    y_te, y_pred,
                    target_names=[INT_TO_ACTION[i] for i in sorted(set(y))],
                    zero_division=0,
                ))

    # 5-fold stratified CV
    logger.info("--- 5-fold stratified CV ---")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_accs = []
    for fold, (tr_idx, te_idx) in enumerate(cv.split(X, y)):
        w = _balanced_class_weights_capped(y[tr_idx])
        sw = np.array([w[int(v)] for v in y[tr_idx]], dtype=np.float32)
        m = xgb.XGBClassifier(
            n_estimators=best_iter, max_depth=5, learning_rate=0.05,
            objective="multi:softprob", num_class=5, random_state=42,
            verbosity=0, eval_metric="mlogloss",
        )
        m.fit(X[tr_idx], y[tr_idx], sample_weight=sw, verbose=False)
        a = float(accuracy_score(y[te_idx], m.predict(X[te_idx])))
        cv_accs.append(a)
        logger.info("  Fold %d: %.4f", fold + 1, a)
    cv_mean = float(np.mean(cv_accs))
    cv_std = float(np.std(cv_accs))
    logger.info("  Mean CV: %.4f +/- %.4f", cv_mean, cv_std)

    # Stop condition: CV < 85%
    if cv_mean < 0.85:
        logger.error("STOP: CV accuracy %.4f < 85%% threshold. Model is degenerate.", cv_mean)
        return

    os.makedirs(os.path.dirname(out_model), exist_ok=True)
    model.save_model(out_model)
    logger.info("Saved model: %s", out_model)

    report = {
        "model_version": "v2_3_capped",
        "experiment": "Option A — RAISE weight capped at 1.50",
        "csv_path": csv_path,
        "out_model_path": out_model,
        "n_samples": len(rows),
        "n_features": int(X.shape[1]),
        "class_distribution": dist,
        "class_weights_balanced": weight_table,
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
