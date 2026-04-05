"""
Raise Sizing Model â€” Production Training Pipeline
===================================================

Trains XGBoost 3-class classifier on raise hands from PokerBench.
Predicts: SMALL / STANDARD / LARGE raise sizing bucket.

Uses the same 37 features as the action model â€” no new features
beyond what the feature extractor provides.

Usage:
    python3 train_sizing_model.py                   # 5k hands (quick)
    python3 train_sizing_model.py --full             # all chunks (~37k raises)
    python3 train_sizing_model.py --full --export    # train + export for production

Output:
    raise_sizing_model.json   â€” serialized XGBoost model
    sizing_training_report.json â€” accuracy metrics and feature importance

Bucket definitions (from data analysis on 250k PokerBench hands):
    SMALL:    pot_ratio < 1.00   (~31% of raises â€” small sizing, ~2x-2.2x)
    STANDARD: 1.00 â‰¤ ratio < 1.40 (~47% â€” standard sizing, ~2.5x)
    LARGE:    ratio â‰¥ 1.40       (~22% â€” pot-sized or bigger, 3x+)
"""

import sys
import os
import json
import time
import re
import csv
import numpy as np
from collections import Counter

sys.path.insert(0, '/mnt/project')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CONSTANTS (shared with sizing_oracle.py)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

RAISE_BUCKETS = ("SMALL", "STANDARD", "LARGE")
RAISE_BUCKET_TO_INT = {b: i for i, b in enumerate(RAISE_BUCKETS)}
INT_TO_RAISE_BUCKET = {i: b for i, b in enumerate(RAISE_BUCKETS)}
N_RAISE_CLASSES = len(RAISE_BUCKETS)

# Bucket boundaries (pot-ratio thresholds)
RAISE_SMALL_UPPER = 1.00    # < 100% pot = SMALL
RAISE_STANDARD_UPPER = 1.40 # 100-140% pot = STANDARD
                              # >= 140% pot = LARGE

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


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# BUCKET ASSIGNMENT
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def assign_raise_bucket(pot_ratio: float) -> str:
    """Assign a raise pot-ratio to SMALL / STANDARD / LARGE."""
    if pot_ratio < RAISE_SMALL_UPPER:
        return "SMALL"
    elif pot_ratio < RAISE_STANDARD_UPPER:
        return "STANDARD"
    else:
        return "LARGE"


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# DATA LOADING (from pre-extracted CSV or live extraction)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def load_from_csv(filepath: str):
    """Load pre-extracted features from CSV."""
    X_rows, y_rows = [], []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            features = [float(row[col]) for col in FEATURE_COLUMNS]
            X_rows.append(features)
            y_rows.append(RAISE_BUCKET_TO_INT[row['size_bucket']])

    X = np.array(X_rows, dtype=np.float32)
    y = np.array(y_rows, dtype=np.int32)
    return X, y


def extract_from_pokerbench(chunk_files, max_hands=None):
    """
    Extract features from PokerBench files for raise hands.

    Runs the full foundation pipeline per hand (~50 hands/sec).
    Returns X, y numpy arrays ready for training.
    """
    from pokerbench_parser import load_raise_hands, assign_raise_bucket
    from feature_extractor import extract_all_features

    print(f"\n--- Loading raise hands ---")
    hands = load_raise_hands(chunk_files, max_hands=max_hands)
    if not hands:
        raise ValueError("No raise hands found")

    print(f"\n--- Extracting features ({len(hands)} hands) ---")
    X_rows, y_rows = [], []
    errors = 0
    t_start = time.time()

    for i, hand in enumerate(hands):
        try:
            feat = extract_all_features(hand)
            row = [float(feat[col]) for col in FEATURE_COLUMNS]
            bucket = assign_raise_bucket(hand['_pot_ratio'])
            X_rows.append(row)
            y_rows.append(RAISE_BUCKET_TO_INT[bucket])
        except Exception:
            errors += 1

        if (i + 1) % 500 == 0:
            elapsed = time.time() - t_start
            rate = (i + 1) / elapsed
            remaining = (len(hands) - i - 1) / rate
            print(f"  [{i+1}/{len(hands)}] {elapsed:.0f}s | "
                  f"{rate:.1f} h/s | ~{remaining:.0f}s left | err={errors}")

    elapsed = time.time() - t_start
    print(f"  Done: {len(X_rows)} extracted, {errors} errors, {elapsed:.1f}s")

    X = np.array(X_rows, dtype=np.float32)
    y = np.array(y_rows, dtype=np.int32)
    return X, y


def save_features_csv(X, y, filepath):
    """Save extracted features to CSV for reproducibility."""
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        header = FEATURE_COLUMNS + ['size_bucket']
        writer.writerow(header)
        for i in range(len(y)):
            row = list(X[i]) + [INT_TO_RAISE_BUCKET[y[i]]]
            writer.writerow(row)
    print(f"  Saved {len(y)} rows to {filepath}")


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TRAINING
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def train_and_evaluate(X, y, output_dir='/home/claude', export=False):
    """
    Train XGBoost 3-class raise sizing model.

    Args:
        X: (n_samples, 37) feature array
        y: (n_samples,) labels [0=SMALL, 1=STANDARD, 2=LARGE]
        output_dir: Where to save model and report
        export: If True, save model JSON for production use

    Returns:
        (model, report_dict)
    """
    from sklearn.model_selection import (
        StratifiedKFold, cross_val_predict, train_test_split,
    )
    from sklearn.metrics import (
        accuracy_score, classification_report, confusion_matrix,
    )
    import xgboost as xgb

    print(f"\n{'=' * 60}")
    print(f"RAISE SIZING MODEL â€” Training")
    print(f"{'=' * 60}")
    print(f"  Samples: {X.shape[0]}, Features: {X.shape[1]}")

    dist = Counter(y)
    for bucket, idx in RAISE_BUCKET_TO_INT.items():
        count = dist.get(idx, 0)
        print(f"    {bucket:>10}: {count:5d} ({count / len(y) * 100:.1f}%)")

    # â”€â”€ 80/20 split â”€â”€
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y,
    )
    print(f"\n  Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")

    # â”€â”€ Train â”€â”€
    print(f"  Training XGBoost...")
    model = xgb.XGBClassifier(
        n_estimators=500,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=5,
        gamma=0.1,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective='multi:softprob',
        num_class=N_RAISE_CLASSES,
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
    best_iter = model.best_iteration
    print(f"  Best iteration: {best_iter}")

    # â”€â”€ Test set â”€â”€
    y_pred = model.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    print(f"\n  Test Accuracy: {test_acc:.4f} ({test_acc:.1%})")

    print(f"\n  Classification Report:")
    print(classification_report(
        y_test, y_pred, target_names=list(RAISE_BUCKETS), digits=3,
    ))

    print(f"  Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    header = "           " + "  ".join(f"{b:>10}" for b in RAISE_BUCKETS)
    print(header)
    for i, row in enumerate(cm):
        print(f"  {RAISE_BUCKETS[i]:>10} " +
              "  ".join(f"{v:10d}" for v in row))

    # â”€â”€ Error severity â”€â”€
    print(f"\n  Error Severity:")
    errs = Counter(abs(int(t) - int(p)) for t, p in zip(y_test, y_pred))
    for edist in sorted(errs.keys()):
        label = "exact" if edist == 0 else f"off-by-{edist}"
        count = errs[edist]
        print(f"    {label}: {count:5d} ({count / len(y_test) * 100:.1f}%)")

    # â”€â”€ 5-fold CV â”€â”€
    print(f"\n  Running 5-fold CV...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_model = xgb.XGBClassifier(
        n_estimators=best_iter,
        max_depth=5, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8, min_child_weight=5,
        gamma=0.1, reg_alpha=0.1, reg_lambda=1.0,
        objective='multi:softprob', num_class=N_RAISE_CLASSES,
        eval_metric='mlogloss', random_state=42, n_jobs=-1,
    )
    y_cv = cross_val_predict(cv_model, X, y, cv=cv)
    cv_acc = accuracy_score(y, y_cv)
    print(f"  5-Fold CV Accuracy: {cv_acc:.4f} ({cv_acc:.1%})")

    # â”€â”€ Feature importance â”€â”€
    importances = model.feature_importances_
    feat_imp = sorted(
        zip(FEATURE_COLUMNS, importances),
        key=lambda x: x[1], reverse=True,
    )
    print(f"\n  Feature Importance (top 10):")
    for name, imp in feat_imp[:10]:
        bar = "â–ˆ" * int(imp * 150)
        print(f"    {name:>22}: {imp:.4f} {bar}")

    # â”€â”€ Export â”€â”€
    model_path = None
    model_size = 0
    if export:
        model_path = os.path.join(output_dir, 'raise_sizing_model.json')
        model.save_model(model_path)
        model_size = os.path.getsize(model_path)
        print(f"\n  Model exported: {model_path} ({model_size / 1024:.1f} KB)")

    # â”€â”€ Report â”€â”€
    report = {
        'model': 'raise_sizing_v1',
        'n_samples': int(X.shape[0]),
        'n_features': int(X.shape[1]),
        'n_classes': N_RAISE_CLASSES,
        'classes': list(RAISE_BUCKETS),
        'bucket_thresholds': {
            'SMALL': f'pot_ratio < {RAISE_SMALL_UPPER}',
            'STANDARD': f'{RAISE_SMALL_UPPER} <= pot_ratio < {RAISE_STANDARD_UPPER}',
            'LARGE': f'pot_ratio >= {RAISE_STANDARD_UPPER}',
        },
        'test_accuracy': round(float(test_acc), 4),
        'cv_accuracy': round(float(cv_acc), 4),
        'best_iteration': int(best_iter),
        'model_size_kb': round(model_size / 1024, 1) if model_path else None,
        'feature_importance': {n: round(float(v), 4) for n, v in feat_imp},
        'class_distribution': {
            INT_TO_RAISE_BUCKET[idx]: int(cnt)
            for idx, cnt in sorted(dist.items())
        },
    }

    report_path = os.path.join(output_dir, 'sizing_training_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"  Report: {report_path}")

    # â”€â”€ Summary â”€â”€
    majority_acc = max(dist.values()) / len(y)
    print(f"\n{'=' * 60}")
    print(f"SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Majority baseline: {majority_acc:.1%}")
    print(f"  Test accuracy:     {test_acc:.1%}")
    print(f"  5-Fold CV:         {cv_acc:.1%}")
    print(f"  Lift:              +{(cv_acc - majority_acc) * 100:.1f}pp")
    print(f"{'=' * 60}")

    return model, report


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# MAIN
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

if __name__ == '__main__':
    chunk_dir = '/mnt/user-data/uploads'
    chunk_files = [
        os.path.join(chunk_dir, f'pokerbench_chunk_{i:02d}')
        for i in range(20)
    ]

    full_mode = '--full' in sys.argv
    do_export = '--export' in sys.argv
    max_hands = None if full_mode else 5000

    mode_label = "FULL" if full_mode else "QUICK (5k)"
    print(f"Raise Sizing Training â€” {mode_label}")

    # Check for pre-extracted CSV
    csv_path = '/home/claude/raise_features.csv'
    if os.path.exists(csv_path) and '--reextract' not in sys.argv:
        print(f"  Loading from cached CSV: {csv_path}")
        X, y = load_from_csv(csv_path)
    else:
        X, y = extract_from_pokerbench(chunk_files, max_hands=max_hands)
        save_features_csv(X, y, csv_path)

    output_dir = '/home/claude'
    model, report = train_and_evaluate(X, y, output_dir, export=do_export)
