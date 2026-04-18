"""train_v2_3_2.py — v2.3.2 model training.

Provenance (CLAUDE.md §5.1)
---------------------------
This script's commit is the provenance record for
``river-rats-core/models/v2_3_2_model.json``. See:

- ``assemble_v23_2.py`` (repo root) — upstream assembly
- ``review/generate_value_bet_v232.py`` — Layer 2-mirror generator
- ``review/comms/MAIN_TERMINAL_DIRECTIVE_2026-04-18-o.md`` — Path C scope
- ``review/comms/MAIN_TERMINAL_TO_BUILDER_2026-04-18-p.md`` — plan answers
- ``review/comms/MAIN_TERMINAL_DIRECTIVE_2026-04-18-q.md`` — Path A
  (accept all 39 labels) ruling on red-flag triage

Architecture
------------
Ports train_v2_3_1.py verbatim for hyperparameters (no class
weighting, same XGBoost config). Only differences: input CSV, output
model/manifest paths.

Run:
    python3 river-rats-core/train_v2_3_2.py
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

logger = logging.getLogger("train_v2_3_2")


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
    csv_path = os.path.join(repo_root, "training-data/v2_3_2_training.csv")
    out_model = os.path.join(_THIS_DIR, "models/v2_3_2_model.json")
    report_path = os.path.join(_THIS_DIR, "models/v2_3_2_training_report.json")
    manifest_path = os.path.join(_THIS_DIR, "models/v2_3_2_manifest.json")

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
    logger.info(
        "Per-class:\n%s",
        classification_report(
            y_te, y_pred,
            target_names=[INT_TO_ACTION[i] for i in sorted(set(y))],
            zero_division=0,
        ),
    )

    # Per-class metrics for manifest
    from sklearn.metrics import precision_recall_fscore_support
    labels_sorted = sorted(set(y))
    prec, rec, f1, supp = precision_recall_fscore_support(
        y_te, y_pred, labels=labels_sorted, zero_division=0,
    )
    per_class = {
        INT_TO_ACTION[labels_sorted[i]]: {
            "precision": float(prec[i]),
            "recall": float(rec[i]),
            "f1": float(f1[i]),
            "support": int(supp[i]),
        }
        for i in range(len(labels_sorted))
    }

    logger.info("--- 5-fold stratified CV ---")
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
        "model_version": "v2_3_2",
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
        "per_class": per_class,
    }
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    logger.info("Saved report: %s", report_path)

    manifest = {
        "model_version": "v2.3.2",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_head_sha": _git_rev(),
        "training_script": os.path.relpath(__file__, repo_root),
        "assembly_script": "assemble_v23_2.py",
        "csv_path": os.path.relpath(csv_path, repo_root),
        "csv_sha256": _file_sha256(csv_path),
        "model_artifact": os.path.relpath(out_model, repo_root),
        "report_artifact": os.path.relpath(report_path, repo_root),
        "feature_vector": {
            "raw_count": len(raw_features),
            "attn_count": len(attn_features),
            "total_count": len(feature_order),
            "new_features_vs_v2_3_1": [],
        },
        "data_sources": {
            "v2_2_base": "training-data/v2_2_training.csv",
            "phase4_labels": "training-data/pass1_final_labels_v23.jsonl (UMBRELLA excluded)",
            "pilot_labels": "training-data/v23_pilot_labelled.jsonl",
            "call_supplement": "training-data/pass1_final_labels_v23_call.jsonl",
            "air_check_3way_v231": (
                "training-data/v23_air_check_3way_labelled.jsonl "
                "(40 rows from v2.3.1 Layer 2)"
            ),
            "value_bet_3way_v232": (
                "training-data/v23_2_value_bet_3way_labelled.jsonl "
                "(39 rows NEW for v2.3.2 Layer 2-mirror)"
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
        "per_class_metrics": per_class,
        "related_commits": {
            "layer_1_board_adjusted_hrp": "80197cd",
            "layer_2a_override_audit": "1526dbf",
            "layer_2b_v3_1_prompt": "4a2d28c",
            "layer_2_air_check_generator": "ad806ba",
            "layer_2_mirror_value_bet_generator": "4630606",
            "v2_3_1_stop_selfplay": "a3ce395",
            "directive_o_path_c": "6022bb5",
            "directive_p_three_answers": "29dc412",
            "directive_q_accept_all_39": "663ca9a",
        },
        "layer_2_balance_review_thread": [
            "review/comms/MAIN_TERMINAL_UPDATE_2026-04-18-g.md",
            "review/comms/MAIN_TERMINAL_DECISION_2026-04-18-h.md",
            "review/comms/BUILDER_V231_SELFPLAY_STOP_2026-04-18.md",
            "review/comms/MAIN_TERMINAL_DIRECTIVE_2026-04-18-o.md",
            "review/comms/BUILDER_V232_PLAN_2026-04-18.md",
            "review/comms/MAIN_TERMINAL_TO_BUILDER_2026-04-18-p.md",
            "review/comms/BUILDER_V232_LABELLING_RED_FLAG_2026-04-18.md",
            "review/comms/MAIN_TERMINAL_DIRECTIVE_2026-04-18-q.md",
        ],
        "future_work_v24_note": (
            "Factory predicate gap flagged: is_made=1 AND eq>=0.55 captures "
            "hand strength but not texture-specific vulnerability (e.g. "
            "overpair-no-blocker on monotone at compressed SPR). 4 of 39 "
            "value-BET factory rows labelled CHECK by v3.1 panels on this "
            "texture — panels honest, factory predicate coarse. Consider "
            "stricter texture-blocker predicate in v2.4."
        ),
    }
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    logger.info("Saved manifest: %s", manifest_path)


if __name__ == "__main__":
    main()
