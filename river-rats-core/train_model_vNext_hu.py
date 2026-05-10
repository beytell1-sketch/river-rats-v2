"""vNext HU trainer — 59-feature, 5-class XGBoost, FROM-SCRATCH on 746-hand HU corpus.

Provenance
----------
Phase 1.5-D.4 trainer per dispatch (PR #364) §"Trainer" + AMENDMENT (PR #366).
Adapted from `river-rats-core/train_model_v9_student.py` with HU-specific
deviations:
  - From-scratch (no `xgb_model=` warm-start arg)
  - HU-only corpus (746 hands; pilot_50_v2 + full_HU2_HU6)
  - 59-feature surface (matches v9-3way-on-59 production)
  - Hyperparameters identical to v9_student (same regularization regime
    suitable for ~750-corpus 5-class XGBoost)
  - Smoke = 1-seed run; full = 5-seed run
  - Confidence weighting derived from consensus_kind:
      5-of-5/4-of-5 → 1.0/0.8 (HIGH); 3-2-tier-up-agree → 0.6;
      3-2-tier-up-disagree (owner-arb) / 2-2-1 (owner-arb) → 0.4 (MEDIUM)

Produces
--------
`models/gto_model_vNext_hu_59feat_seed{N}.json` (per-seed) +
`models/gto_model_vNext_hu_59feat.json` (canonical 5-seed median artifact).

Training data
-------------
`data/corpus_hu_746_2026-05-10.jsonl` (746 rows, 59-key feat_dict +
consensus_action + confidence per row).

CLI
---
Smoke (1-seed):
  python3 river-rats-core/train_model_vNext_hu.py \
      --corpus data/corpus_hu_746_2026-05-10.jsonl \
      --seeds 42 \
      --output models/gto_model_vNext_hu_59feat_seed42_smoke.json

Full (5-seed):
  python3 river-rats-core/train_model_vNext_hu.py \
      --corpus data/corpus_hu_746_2026-05-10.jsonl \
      --seeds 0,1,2,3,4 \
      --output models/gto_model_vNext_hu_59feat.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split

# Make river-rats-core importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feature_extractor import FEATURE_COLUMNS as STUDENT_FEATURE_COLUMNS_V9
from gto_model import (
    ACTION_CLASSES, ACTION_TO_INT, INT_TO_ACTION, N_CLASSES,
)


# ─── Module-load assertions ───────────────────────────────────────────

assert len(STUDENT_FEATURE_COLUMNS_V9) == 59, (
    f"vNext-HU requires 59-feature surface; "
    f"feature_extractor.FEATURE_COLUMNS is {len(STUDENT_FEATURE_COLUMNS_V9)}."
)
assert N_CLASSES == 5

_N_FEATURES = 59


# ─── Hyperparameters (identical to v9_student per dispatch) ───────────

_HYPERPARAMETERS: Dict = dict(
    n_estimators=800,
    max_depth=5,
    learning_rate=0.05,
    early_stopping_rounds=50,
    subsample=0.8,
    colsample_bytree=0.75,
    min_child_weight=5,
    gamma=0.2,
    reg_alpha=0.1,
    reg_lambda=1.0,
    objective="multi:softprob",
    num_class=5,
    eval_metric="mlogloss",
    n_jobs=-1,
)

_TEST_SIZE_DEFAULT = 0.2
_CLASS_WEIGHT_CAP = 3.0


# ─── Corpus loading ───────────────────────────────────────────────────

@dataclass
class TrainInputs:
    X: np.ndarray
    y: np.ndarray
    sample_weight: np.ndarray
    spot_ids: List[str]
    n_features: int
    n_samples: int


def load_corpus(path: str) -> TrainInputs:
    """Load combined HU corpus JSONL. Each row has feat_dict (59 keys),
    consensus_action, and confidence."""
    spot_ids = []
    X_rows = []
    y_rows = []
    sw_rows = []
    valid_actions = set(ACTION_CLASSES)
    with open(path) as f:
        for line_no, line in enumerate(f, 1):
            row = json.loads(line)
            sid = row.get('spot_id')
            if not sid:
                raise ValueError(f"row {line_no} missing spot_id")
            feat = row.get('feat_dict')
            if not isinstance(feat, dict):
                raise ValueError(f"row {line_no} ({sid}) missing feat_dict")
            missing = [k for k in STUDENT_FEATURE_COLUMNS_V9 if k not in feat]
            if missing:
                raise ValueError(
                    f"row {line_no} ({sid}) feat_dict missing {len(missing)}/59 keys: "
                    f"{missing[:3]}..."
                )
            action = row.get('consensus_action')
            if action not in valid_actions:
                raise ValueError(
                    f"row {line_no} ({sid}) invalid consensus_action={action!r}; "
                    f"expected one of {valid_actions}"
                )
            confidence = float(row.get('confidence', 0.6))

            spot_ids.append(sid)
            X_rows.append([float(feat[k]) for k in STUDENT_FEATURE_COLUMNS_V9])
            y_rows.append(ACTION_TO_INT[action])
            sw_rows.append(confidence)

    X = np.array(X_rows, dtype=np.float32)
    y = np.array(y_rows, dtype=np.int64)
    sw = np.array(sw_rows, dtype=np.float32)

    return TrainInputs(
        X=X, y=y, sample_weight=sw,
        spot_ids=spot_ids,
        n_features=X.shape[1],
        n_samples=X.shape[0],
    )


# ─── Per-seed training ────────────────────────────────────────────────

@dataclass
class SeedResult:
    seed: int
    train_size: int
    test_size: int
    held_out_metrics: Dict
    n_boosted_rounds: int
    model_path: str


def train_one_seed(
    inputs: TrainInputs,
    *,
    seed: int,
    output_path: str,
    test_size: float = _TEST_SIZE_DEFAULT,
    hyperparameters: Optional[Dict] = None,
    verbose: bool = False,
) -> SeedResult:
    hp = hyperparameters or _HYPERPARAMETERS

    X_train, X_test, y_train, y_test, conf_train, conf_test = train_test_split(
        inputs.X, inputs.y, inputs.sample_weight,
        test_size=test_size,
        random_state=seed,
        stratify=inputs.y,
    )

    # Hybrid weighting per ml-architect 12.5D Q3 (closes class-prior collapse).
    class_counts = np.bincount(y_train, minlength=N_CLASSES)
    mean_class_count = class_counts.mean()
    class_weights = {
        c: min(_CLASS_WEIGHT_CAP, mean_class_count / max(class_counts[c], 1))
        for c in range(N_CLASSES)
    }
    sw_train = conf_train * np.array([class_weights[c] for c in y_train], dtype=np.float32)
    sw_test = conf_test * np.array([class_weights[c] for c in y_test], dtype=np.float32)

    clf = xgb.XGBClassifier(**hp, random_state=seed)
    clf.fit(
        X_train, y_train,
        sample_weight=sw_train,
        eval_set=[(X_test, y_test)],
        sample_weight_eval_set=[sw_test],
        # NB: no xgb_model= → from-scratch per dispatch
        verbose=verbose,
    )

    # Held-out evaluation
    y_pred = clf.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))
    acc_w = float(accuracy_score(y_test, y_pred, sample_weight=sw_test))
    report = classification_report(
        y_test, y_pred,
        labels=list(range(N_CLASSES)),
        target_names=list(ACTION_CLASSES),
        output_dict=True,
        zero_division=0,
    )
    cm = confusion_matrix(y_test, y_pred, labels=list(range(N_CLASSES))).tolist()

    held_out = {
        'accuracy': acc,
        'accuracy_weighted': acc_w,
        'classification_report': report,
        'confusion_matrix': cm,
    }

    # Persist
    clf.save_model(output_path)

    return SeedResult(
        seed=seed,
        train_size=int(len(X_train)),
        test_size=int(len(X_test)),
        held_out_metrics=held_out,
        n_boosted_rounds=int(clf.get_booster().num_boosted_rounds()),
        model_path=output_path,
    )


# ─── 5-seed median selection ──────────────────────────────────────────

def select_median_seed(seed_results: List[SeedResult]) -> SeedResult:
    """Pick the seed whose held-out accuracy is the median (or just-below).
    Avoids best-seed cherry-picking; gives robust deployment artifact."""
    sorted_results = sorted(seed_results, key=lambda r: r.held_out_metrics['accuracy'])
    median_idx = len(sorted_results) // 2
    return sorted_results[median_idx]


# ─── CLI ──────────────────────────────────────────────────────────────

def parse_seeds(s: str) -> List[int]:
    return [int(x.strip()) for x in s.split(',') if x.strip()]


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="vNext HU trainer (Phase 1.5-D.4)")
    p.add_argument('--corpus', required=True, help='HU corpus JSONL path')
    p.add_argument('--seeds', default='0,1,2,3,4',
                   help='Comma-separated seed list (e.g., "42" for smoke; "0,1,2,3,4" for full)')
    p.add_argument('--output', required=True,
                   help='Output model path (canonical artifact for full run; smoke artifact for 1-seed)')
    p.add_argument('--test-size', type=float, default=_TEST_SIZE_DEFAULT)
    p.add_argument('--report-out', default=None,
                   help='Optional JSON report path')
    args = p.parse_args(argv)

    print(f"[load] reading {args.corpus}...")
    inputs = load_corpus(args.corpus)
    print(f"[load] {inputs.n_samples} samples × {inputs.n_features} features")
    # Action distribution
    from collections import Counter
    action_dist = Counter(int(y) for y in inputs.y)
    print(f"[load] action distribution: "
          f"{ {INT_TO_ACTION[k]: v for k,v in sorted(action_dist.items())} }")

    seeds = parse_seeds(args.seeds)
    print(f"[train] seeds: {seeds}")
    seed_results = []
    for seed in seeds:
        # Per-seed output path
        if len(seeds) == 1:
            out_path = args.output
        else:
            base, ext = os.path.splitext(args.output)
            out_path = f"{base}_seed{seed}{ext}"
        print(f"\n[train] seed={seed} → {out_path}")
        result = train_one_seed(inputs, seed=seed, output_path=out_path,
                                test_size=args.test_size)
        print(f"[train] seed={seed} acc={result.held_out_metrics['accuracy']:.3f} "
              f"(weighted {result.held_out_metrics['accuracy_weighted']:.3f}); "
              f"{result.n_boosted_rounds} rounds")
        seed_results.append(result)

    # If 5-seed: select median + write canonical artifact
    if len(seed_results) >= 3:
        median = select_median_seed(seed_results)
        print(f"\n[5-seed] median seed = {median.seed} "
              f"(acc={median.held_out_metrics['accuracy']:.3f})")
        # Copy median model to canonical output path
        import shutil
        shutil.copy(median.model_path, args.output)
        print(f"[5-seed] canonical artifact at {args.output}")

    # Report
    if args.report_out:
        report_data = {
            'corpus_path': args.corpus,
            'n_samples': inputs.n_samples,
            'n_features': inputs.n_features,
            'seeds': seeds,
            'output_path': args.output,
            'hyperparameters': {k: v for k, v in _HYPERPARAMETERS.items()},
            'per_seed': [
                {
                    'seed': r.seed,
                    'train_size': r.train_size,
                    'test_size': r.test_size,
                    'accuracy': r.held_out_metrics['accuracy'],
                    'accuracy_weighted': r.held_out_metrics['accuracy_weighted'],
                    'n_boosted_rounds': r.n_boosted_rounds,
                    'model_path': r.model_path,
                }
                for r in seed_results
            ],
        }
        with open(args.report_out, 'w') as f:
            json.dump(report_data, f, indent=2)
        print(f"[report] wrote {args.report_out}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
