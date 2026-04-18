"""train_v2_3_1.py — v2.3.1 model training.

Provenance (CLAUDE.md §5.1)
---------------------------
This script's commit is the provenance record for
``river-rats-core/models/v2_3_1_model.json``. See also:

- ``assemble_v23_1.py`` (repo root) — upstream assembly script
- ``review/comms/BUILDER_YIELD_STATS_AIR_CHECK_2026-04-18.md``
- ``review/comms/BUILDER_LABELLING_RESULTS_AIR_CHECK_2026-04-18.md``
- ``review/comms/MAIN_TERMINAL_UPDATE_2026-04-18-g.md`` (scope directive)
- ``review/comms/MAIN_TERMINAL_DECISION_2026-04-18-h.md`` (blocker resolutions)
- ``review/comms/REVIEW_LABELS_AIR_CHECK_2026-04-18.md`` (retrain approval)

Architecture
------------
Ports train_v2_3_clean.py verbatim for the XGBoost hyperparameters
(n_estimators=800, max_depth=5, lr=0.05, no class weighting, 80/20
stratified holdout, 5-fold CV at best_iter). Only differences:

- CSV input: training-data/v2_3_1_training.csv (677 rows, 55 raw +
  55 attn = 110 features post-Layer-1)
- Model output: river-rats-core/models/v2_3_1_model.json
- Report output: river-rats-core/models/v2_3_1_training_report.json
- Manifest output: river-rats-core/models/v2_3_1_manifest.json

Run:
    python3 river-rats-core/train_v2_3_1.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import logging
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS_DIR)

from train_model import _preflight_schema_check  # noqa: E402
from train_model_v2_2 import (  # noqa: E402
    ACTION_TO_INT, INT_TO_ACTION, encode, split_feature_columns, build_matrix,
)

logger = logging.getLogger("train_v2_3_1")


def _git_rev() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=os.path.join(_THIS_DIR, '..'),
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        return out
    except Exception:
        return "unknown"


def _file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    )
    import xgboost as xgb
    from sklearn.metrics import accuracy_score, classification_report
    from sklearn.model_selection import StratifiedKFold, train_test_split

    repo_root = os.path.join(_THIS_DIR, '..')
    csv_path = os.path.join(repo_root, "training-data/v2_3_1_training.csv")
    out_model = os.path.join(_THIS_DIR, "models/v2_3_1_model.json")
    report_path = os.path.join(_THIS_DIR, "models/v2_3_1_training_report.json")
    manifest_path = os.path.join(_THIS_DIR, "models/v2_3_1_manifest.json")

    _preflight_schema_check(csv_path=csv_path)
    logger.info("Preflight PASSED on %s", csv_path)

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

    source_counter = Counter(r.get("label_source", "unknown") for r in rows)

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y,
    )
    logger.info("Train: %d, Test: %d", X_tr.shape[0], X_te.shape[0])

    hyperparams = dict(
        n_estimators=800, max_depth=5, learning_rate=0.05,
        objective="multi:softprob", num_class=5,
        eval_metric="mlogloss", use_label_encoder=False,
        random_state=42, early_stopping_rounds=50, verbosity=0,
    )
    model = xgb.XGBClassifier(**hyperparams)
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

    logger.info("--- 5-fold stratified CV (no weights) ---")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_accs = []
    cv_hyperparams = dict(hyperparams)
    cv_hyperparams.pop("early_stopping_rounds", None)
    cv_hyperparams["n_estimators"] = best_iter
    for fold, (tr_idx, te_idx) in enumerate(cv.split(X, y)):
        m = xgb.XGBClassifier(**cv_hyperparams)
        m.fit(X[tr_idx], y[tr_idx], verbose=False)
        a = float(accuracy_score(y[te_idx], m.predict(X[te_idx])))
        cv_accs.append(a)
        logger.info("  Fold %d: %.4f", fold + 1, a)
    cv_mean = float(np.mean(cv_accs))
    cv_std = float(np.std(cv_accs))
    logger.info("  Mean CV: %.4f +/- %.4f", cv_mean, cv_std)

    os.makedirs(os.path.dirname(out_model), exist_ok=True)
    model.save_model(out_model)
    logger.info("Saved model: %s", out_model)

    report = {
        "model_version": "v2_3_1",
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
        "hyperparameters": hyperparams,
    }
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    logger.info("Saved report: %s", report_path)

    # Training manifest per CLAUDE.md §5.1 provenance requirement.
    manifest = {
        "model_version": "v2.3.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_head_sha": _git_rev(),
        "training_script": os.path.relpath(__file__, repo_root),
        "assembly_script": "assemble_v23_1.py",
        "csv_path": os.path.relpath(csv_path, repo_root),
        "csv_sha256": _file_sha256(csv_path),
        "model_artifact": os.path.relpath(out_model, repo_root),
        "report_artifact": os.path.relpath(report_path, repo_root),
        "feature_vector": {
            "raw_count": len(raw_features),
            "attn_count": len(attn_features),
            "total_count": len(feature_order),
            "new_feature_vs_v2_3": "board_adjusted_hrp",
        },
        "data_sources": {
            "v2_2_base": "training-data/v2_2_training.csv",
            "phase4_labels": "training-data/pass1_final_labels_v23.jsonl (UMBRELLA excluded)",
            "pilot_labels": "training-data/v23_pilot_labelled.jsonl",
            "call_supplement": "training-data/pass1_final_labels_v23_call.jsonl",
            "air_check_3way_v231": (
                "training-data/v23_air_check_3way_labelled.jsonl "
                "(NEW for v2.3.1 Layer 2)"
            ),
        },
        "source_row_counts": dict(source_counter),
        "class_distribution": dist,
        "hyperparameters": hyperparams,
        "train_test_split": {"test_size": 0.20, "stratified": True, "seed": 42},
        "best_iteration": best_iter,
        "holdout_test_accuracy": test_acc,
        "cv_mean": cv_mean,
        "cv_std": cv_std,
        "related_commits": {
            "layer_1_board_adjusted_hrp": "80197cd",
            "layer_2a_override_audit": "1526dbf",
            "layer_2b_v3_1_prompt": "4a2d28c",
            "self_play_diagnostic": "4d81c08",
        },
        "layer_2_review_thread": [
            "review/comms/MAIN_TERMINAL_UPDATE_2026-04-18-g.md",
            "review/comms/BUILDER_AIR_CHECK_PLAN_2026-04-18.md",
            "review/comms/REVIEW_BUILDER_AIR_CHECK_PLAN_2026-04-18.md",
            "review/comms/BUILDER_HU_LABELLING_QUERY_2026-04-18.md",
            "review/comms/BUILDER_BLOCKER_LITMUS_BRIDGE_SEMANTICS_2026-04-18.md",
            "review/comms/MAIN_TERMINAL_DECISION_2026-04-18-h.md",
            "review/comms/BUILDER_YIELD_STATS_AIR_CHECK_2026-04-18.md",
            "review/comms/REVIEW_YIELD_STATS_AIR_CHECK_2026-04-18.md",
            "review/comms/BUILDER_LABELLING_RESULTS_AIR_CHECK_2026-04-18.md",
            "review/comms/REVIEW_LABELS_AIR_CHECK_2026-04-18.md",
        ],
    }
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    logger.info("Saved manifest: %s", manifest_path)


if __name__ == "__main__":
    main()
