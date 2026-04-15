"""
v2.2 XGBoost Trainer — Ported from Recovered Heredoc
=====================================================

Provenance
----------
Original execution: inline ``python3 <<'EOF'`` heredoc during the v2.2
training session (session 81bf3fe7-5f95-4ea9-90fc-04263a5e8161,
Apr 15 2026). No script was committed at the time the live
``river-rats-core/models/v2_2_model.json`` artifact was produced.

Recovered from the session transcript and committed at commit
``4b08805`` as ``review/recovered/train_v2_2_MODEL.py``. This module
is the in-tree port of that recovered script — encoding logic is
byte-identical (``CAT_MAPS`` path 3: float-first-then-categorical-map
fallback). See:

- review/comms/ANOMALY_A_VERIFICATION_2026-04-15.md
- review/comms/PLAN_CONSOLIDATED_2026-04-15.md §2 Stream A

ANOMALY-A resolution summary: the 185 string rows in
``training-data/v2_2_training.csv`` were encoded correctly at train
time via ``CAT_MAPS`` (path 3). The live v2.2 model is sound; no
retrain is required for ANOMALY-A reasons.

Usage
-----
    # Default — preflight-gated, fails on mixed-encoding CSV.
    # Use for v2.3+ training on clean CSVs.
    python3 river-rats-core/train_model_v2_2.py

    # Reproducing v2.2 on the still-mixed CSV.
    python3 river-rats-core/train_model_v2_2.py --allow-mixed-encoding

    # Custom I/O.
    python3 river-rats-core/train_model_v2_2.py \\
        --csv training-data/v2_2_training.csv \\
        --out river-rats-core/models/v2_2_model_port.json

Rules
-----
- Default output path is ``models/v2_2_model_port.json`` — this
  module does NOT overwrite the canonical ``v2_2_model.json``.
- The 108-column contract (54 raw + 54 ``attn_*``) is a contract
  with ``evaluate_v2_2.py`` and with ``v2_2_model.json``. Do not
  reorder columns — encoding order is taken from the CSV header.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
from collections import Counter
from typing import Dict, List, Tuple

import numpy as np

# Reuse the canonical preflight gate so there is exactly one
# definition in the codebase.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from train_model import _preflight_schema_check  # noqa: E402


logger = logging.getLogger("train_model_v2_2")


# -----------------------------------------------------------------------------
# Encoding — matches the recovered trainer byte-for-byte (CAT_MAPS path 3).
# -----------------------------------------------------------------------------

ACTION_TO_INT: Dict[str, int] = {
    "FOLD": 0, "CHECK": 1, "CALL": 2, "BET": 3, "RAISE": 4,
}
INT_TO_ACTION: Dict[int, str] = {v: k for k, v in ACTION_TO_INT.items()}

CAT_MAPS: Dict[str, Dict[str, int]] = {
    "street": {"flop": 0, "turn": 1, "river": 2, "": 0},
    "hero_position": {
        "UTG": 0, "HJ": 1, "CO": 2, "BTN": 3, "SB": 4, "BB": 5, "": 0,
    },
    "villain_position": {
        "UTG": 0, "HJ": 1, "CO": 2, "BTN": 3, "SB": 4, "BB": 5, "": 0,
    },
}


def encode(row: Dict[str, str], col: str) -> float:
    """Encode one cell.

    Path 3: for categorical columns, try float() first (handles rows
    where the value is already encoded numerically), then fall back
    to the categorical map. For everything else, float() with 0.0
    fallback.
    """
    v = row.get(col, "")
    if col in CAT_MAPS:
        try:
            return float(v)
        except (TypeError, ValueError):
            return float(CAT_MAPS[col].get(v, 0))
    if v in ("", None):
        return 0.0
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def split_feature_columns(header: List[str]) -> Tuple[List[str], List[str]]:
    meta = ("situation_id", "label", "label_source")
    raw = [c for c in header if c not in meta and not c.startswith("attn_")]
    attn = [c for c in header if c.startswith("attn_")]
    return raw, attn


def build_matrix(
    rows: List[Dict[str, str]], feature_order: List[str]
) -> Tuple[np.ndarray, np.ndarray]:
    X = np.array(
        [[encode(r, c) for c in feature_order] for r in rows],
        dtype=np.float32,
    )
    y = np.array(
        [ACTION_TO_INT[r["label"]] for r in rows], dtype=np.int32
    )
    return X, y


def _class_weights(y: np.ndarray) -> Dict[int, float]:
    cnt = Counter(int(v) for v in y)
    mc = max(cnt.values())
    return {
        c: min(
            mc / n,
            3.0 if INT_TO_ACTION[c] == "RAISE"
            else (2.0 if INT_TO_ACTION[c] == "BET" else 4.0),
        )
        for c, n in cnt.items()
    }


def train(
    csv_path: str,
    out_model_path: str,
    report_path: str,
    allow_mixed_encoding: bool,
) -> Dict:
    """Run the v2.2 training pipeline.

    Returns the training-report dict (also written to disk).
    """
    # Preflight gate. Default = strict.
    if not allow_mixed_encoding:
        _preflight_schema_check()
    else:
        logger.warning(
            "--allow-mixed-encoding set: preflight schema check SKIPPED "
            "(only valid for reproducing v2.2 on the still-mixed CSV)."
        )

    # Late imports so unit tests can import this module without sklearn.
    import xgboost as xgb
    from sklearn.metrics import (
        accuracy_score, classification_report
    )
    from sklearn.model_selection import StratifiedKFold, train_test_split

    logger.info("Loading CSV: %s", csv_path)
    with open(csv_path, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise RuntimeError(f"No rows in {csv_path}")
    logger.info("Loaded %d rows", len(rows))

    raw_features, attn_features = split_feature_columns(list(rows[0].keys()))
    logger.info(
        "  Raw features: %d, Attn features: %d",
        len(raw_features), len(attn_features),
    )
    feature_order = raw_features + attn_features

    X, y = build_matrix(rows, feature_order)
    logger.info("X shape: %s, y shape: %s", X.shape, y.shape)
    dist = {INT_TO_ACTION[int(i)]: int(n) for i, n in Counter(y).items()}
    logger.info("Class distribution: %s", dist)

    # 80/20 split for holdout + early-stopping signal.
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    logger.info("Train: %d, Test: %d", X_tr.shape[0], X_te.shape[0])

    raw_w = _class_weights(y_tr)
    sw_tr = np.array([raw_w[int(v)] for v in y_tr], dtype=np.float32)
    logger.info(
        "Class weights: %s",
        {INT_TO_ACTION[c]: round(w, 2) for c, w in raw_w.items()},
    )

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
    logger.info(
        "Per-class:\n%s",
        classification_report(
            y_te, y_pred,
            target_names=[INT_TO_ACTION[i] for i in sorted(set(y))],
            zero_division=0,
        ),
    )

    # 5-fold stratified CV using best_iter from early stopping.
    logger.info("--- 5-fold stratified CV ---")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_accs = []
    for fold, (tr_idx, te_idx) in enumerate(cv.split(X, y)):
        w = _class_weights(y[tr_idx])
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
    logger.info(
        "  Mean CV: %.4f ± %.4f",
        float(np.mean(cv_accs)), float(np.std(cv_accs)),
    )

    os.makedirs(os.path.dirname(out_model_path), exist_ok=True)
    model.save_model(out_model_path)
    logger.info("Saved model: %s", out_model_path)

    report = {
        "model_version": "v2_2_port",
        "provenance": {
            "recovered_commit": "4b08805",
            "recovered_script": "review/recovered/train_v2_2_MODEL.py",
            "port_module": "river-rats-core/train_model_v2_2.py",
        },
        "csv_path": csv_path,
        "out_model_path": out_model_path,
        "allow_mixed_encoding": bool(allow_mixed_encoding),
        "n_samples": len(rows),
        "n_features": int(X.shape[1]),
        "features_raw": len(raw_features),
        "features_attn": len(attn_features),
        "class_distribution": dist,
        "class_weights": {
            INT_TO_ACTION[c]: float(w) for c, w in raw_w.items()
        },
        "best_iteration": best_iter,
        "holdout_test_accuracy": test_acc,
        "cv_accuracies": [float(a) for a in cv_accs],
        "cv_mean": float(np.mean(cv_accs)),
        "cv_std": float(np.std(cv_accs)),
        "hyperparameters": {
            "n_estimators": 800, "max_depth": 5, "learning_rate": 0.05,
        },
    }
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    logger.info("Saved report: %s", report_path)
    return report


def _parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="v2.2 XGBoost trainer (ported from recovered heredoc).",
    )
    p.add_argument(
        "--csv",
        default="training-data/v2_2_training.csv",
        help="Input training CSV.",
    )
    p.add_argument(
        "--out",
        default="river-rats-core/models/v2_2_model_port.json",
        help=("Output model path. Default is *_port.json; the canonical "
              "v2_2_model.json is never overwritten by this script."),
    )
    p.add_argument(
        "--report",
        default="river-rats-core/models/v2_2_training_report_port.json",
        help="Output training-report JSON path.",
    )
    p.add_argument(
        "--allow-mixed-encoding",
        action="store_true",
        help=("Skip the ANOMALY-A preflight schema gate. ONLY use this "
              "for reproducing v2.2 on the still-mixed CSV. v2.3+ "
              "training must run without this flag."),
    )
    return p.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    )
    args = _parse_args(argv if argv is not None else sys.argv[1:])
    if os.path.abspath(args.out).endswith("v2_2_model.json"):
        raise SystemExit(
            "Refusing to overwrite canonical v2_2_model.json. "
            "Use --out with a different filename (default: v2_2_model_port.json)."
        )
    train(
        csv_path=args.csv,
        out_model_path=args.out,
        report_path=args.report,
        allow_mixed_encoding=args.allow_mixed_encoding,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
