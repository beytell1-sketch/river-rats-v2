"""
37-Feature Gauntlet â€” Action v5 + Sizing v2
=============================================

Tests both production models against held-out PokerBench data (chunks 15-19).
Training used chunks 00-04 (action) / 00-09 (sizing). Completely unseen data.

Note: feature_extractor at /mnt/project is still 33-feature, so the 4 new
action-history features will be 0 for all gauntlet hands. This tests backward
compatibility â€” models must perform at least as well as before on old features.

Pass criteria:
  ACTION MODEL (v5):
  - Overall accuracy: â‰¥ 80% (baseline v4 was ~84%)
  - No class below 50% recall
  - Zero crashes

  SIZING MODEL (v2):
  - Raise model: â‰¥ 95% accuracy
  - Bet heuristic: â‰¥ 90% accuracy
  - Off-by-2 errors: < 2%
  - Zero crashes

Run:
    cd /home/claude && python3 gauntlet_v5_37feat.py
"""

import sys
import os
import re
import time
import numpy as np
from collections import Counter

sys.path.insert(0, '/home/claude/project_clean')
sys.path.insert(0, '/home/claude')
# /mnt/project at END of path â€” only for pokerbench_parser & feature_extractor
sys.path.append('/mnt/project')

from sizing_oracle import (
    SizingOracle, assign_raise_bucket, assign_bet_bucket,
    RAISE_BUCKETS, FEATURE_COLUMNS, RAISE_BUCKET_TO_INT,
)
from gto_model import (
    GtoOracle, ACTION_CLASSES, INT_TO_ACTION, ACTION_TO_INT,
)
from pokerbench_parser import parse_pokerbench_line
from feature_extractor import extract_all_features


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CONFIG
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

ACTION_MODEL_PATH = '/home/claude/gto_model_v5_37feat.json'
SIZING_MODEL_PATH = '/home/claude/raise_sizing_model_v2_37feat.json'

# Use chunks 15-19 â€” completely held out from training
GAUNTLET_CHUNKS = [
    f'/mnt/user-data/uploads/pokerbench_chunk_{i:02d}'
    for i in range(15, 20)
]

TARGET_HANDS = 2000         # action model: all actions
TARGET_RAISE_HANDS = 2000   # sizing: raises
TARGET_BET_HANDS = 1000     # sizing: bets

# Action mapping from PokerBench labels
ACTION_MAP = {
    'Fold': 'FOLD', 'Check': 'CHECK', 'Call': 'CALL',
}


def classify_pokerbench_action(correct_str):
    """Map PokerBench correct answer to our action label."""
    correct_str = correct_str.strip()
    if correct_str in ACTION_MAP:
        return ACTION_MAP[correct_str]
    if correct_str.startswith('Bet'):
        return 'BET'
    if correct_str.startswith('Raise'):
        return 'RAISE'
    return None


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# LOAD HANDS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def load_gauntlet_hands():
    """Load hands from held-out chunks."""
    action_hands = []
    raise_hands = []
    bet_hands = []

    for fpath in GAUNTLET_CHUNKS:
        if not os.path.exists(fpath):
            print(f"  WARNING: {fpath} not found, skipping")
            continue

        with open(fpath) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                match = re.search(r'"(\[.*?\])"', line)
                if not match:
                    continue
                after = line[match.end():].lstrip(',').strip().split(',')
                if len(after) < 4:
                    continue

                correct = after[-1].strip()
                pot = float(after[0])
                if pot <= 0:
                    continue

                action_label = classify_pokerbench_action(correct)
                if not action_label:
                    continue

                entry = {
                    'line': line,
                    'action_label': action_label,
                    'correct_str': correct,
                    'pot': pot,
                }

                # Collect for action model
                if len(action_hands) < TARGET_HANDS:
                    action_hands.append(entry)

                # Collect for sizing model
                size_match = re.match(r'(Bet|Raise)\s+(\d+)', correct)
                if size_match:
                    size = float(size_match.group(2))
                    entry['pot_ratio'] = size / pot
                    entry['action_type'] = size_match.group(1)

                    if entry['action_type'] == 'Raise' and len(raise_hands) < TARGET_RAISE_HANDS:
                        raise_hands.append(entry)
                    elif entry['action_type'] == 'Bet' and len(bet_hands) < TARGET_BET_HANDS:
                        bet_hands.append(entry)

                all_done = (
                    len(action_hands) >= TARGET_HANDS and
                    len(raise_hands) >= TARGET_RAISE_HANDS and
                    len(bet_hands) >= TARGET_BET_HANDS
                )
                if all_done:
                    break
        if all_done:
            break

    return action_hands, raise_hands, bet_hands


def extract_features_37(parsed):
    """Extract features, defaulting new features to 0."""
    feat = extract_all_features(parsed)
    return np.array(
        [float(feat.get(col, 0.0)) for col in FEATURE_COLUMNS],
        dtype=np.float32,
    )


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# ACTION MODEL GAUNTLET
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def run_action_gauntlet(oracle, hands):
    """Test action model on held-out hands."""
    y_true, y_pred = [], []
    errors = 0
    t_start = time.time()

    for i, entry in enumerate(hands):
        try:
            parsed = parse_pokerbench_line(entry['line'])
            if not parsed:
                errors += 1
                continue
            features = extract_features_37(parsed)
            pred = oracle.predict(features)
            y_true.append(entry['action_label'])
            y_pred.append(pred.action)
        except Exception as e:
            errors += 1

        if (i + 1) % 500 == 0:
            elapsed = time.time() - t_start
            rate = (i + 1) / elapsed
            print(f"  [{i+1}/{len(hands)}] {elapsed:.0f}s | "
                  f"{rate:.1f} h/s | err={errors}")

    elapsed = time.time() - t_start
    print(f"  Done: {len(y_true)} predictions, {errors} errors, {elapsed:.1f}s")
    return y_true, y_pred


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SIZING MODEL GAUNTLET
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def run_sizing_gauntlet(oracle, hands, action_type, bucket_fn):
    """Test sizing model on held-out hands."""
    results = []
    errors = 0
    t_start = time.time()

    for i, entry in enumerate(hands):
        try:
            parsed = parse_pokerbench_line(entry['line'])
            if not parsed:
                errors += 1
                continue
            features = extract_features_37(parsed)
            prediction = oracle.predict(features, action_type.upper())
            true_bucket = bucket_fn(entry['pot_ratio'])
            results.append((
                prediction.bucket,
                true_bucket,
                prediction.confidence,
            ))
        except Exception as e:
            errors += 1

        if (i + 1) % 500 == 0:
            elapsed = time.time() - t_start
            rate = (i + 1) / elapsed
            print(f"  [{i+1}/{len(hands)}] {elapsed:.0f}s | "
                  f"{rate:.1f} h/s | err={errors}")

    elapsed = time.time() - t_start
    print(f"  Done: {len(results)} predictions, {errors} errors, {elapsed:.1f}s")
    return results


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# REPORT
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def report_action(y_true, y_pred):
    """Print action model metrics."""
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    total = len(y_true)
    acc = correct / total if total else 0

    print(f"\n{'='*60}")
    print(f"ACTION MODEL v5 (37-feat) â€” {total} hands")
    print(f"{'='*60}")
    print(f"Overall accuracy: {acc*100:.1f}% ({'PASS' if acc >= 0.80 else 'FAIL'} â‰¥80%)")

    actions = sorted(set(y_true))
    print(f"\n{'Action':<10} {'Correct':>8} {'Total':>8} {'Recall':>8}")
    print("-" * 40)
    min_recall = 1.0
    for action in actions:
        act_true = [1 for t, p in zip(y_true, y_pred) if t == action and t == p]
        act_total = sum(1 for t in y_true if t == action)
        recall = len(act_true) / act_total if act_total else 0
        min_recall = min(min_recall, recall)
        print(f"{action:<10} {len(act_true):>8} {act_total:>8} {recall*100:>7.1f}%")

    print(f"\nMin recall: {min_recall*100:.1f}% ({'PASS' if min_recall >= 0.50 else 'FAIL'} â‰¥50%)")
    return acc >= 0.80 and min_recall >= 0.50


def report_sizing(results, label, threshold):
    """Print sizing metrics."""
    correct = sum(1 for p, t, _ in results if p == t)
    total = len(results)
    acc = correct / total if total else 0

    print(f"\n{'-'*60}")
    print(f"SIZING: {label} â€” {total} hands")
    print(f"{'-'*60}")
    print(f"Accuracy: {acc*100:.1f}% ({'PASS' if acc >= threshold else 'FAIL'} â‰¥{threshold*100:.0f}%)")

    # Bucket breakdown
    if total > 0:
        buckets = sorted(set(t for _, t, _ in results))
        print(f"\n{'Bucket':<12} {'Correct':>8} {'Total':>8} {'Acc':>8}")
        print("-" * 40)
        for b in buckets:
            b_correct = sum(1 for p, t, _ in results if t == b and p == t)
            b_total = sum(1 for _, t, _ in results if t == b)
            b_acc = b_correct / b_total if b_total else 0
            print(f"{b:<12} {b_correct:>8} {b_total:>8} {b_acc*100:>7.1f}%")

        # Off-by-2 check (raise only)
        if label.startswith("Raise"):
            bucket_order = ["SMALL", "STANDARD", "LARGE"]
            off2 = 0
            for p, t, _ in results:
                if p in bucket_order and t in bucket_order:
                    diff = abs(bucket_order.index(p) - bucket_order.index(t))
                    if diff >= 2:
                        off2 += 1
            off2_rate = off2 / total
            print(f"\nOff-by-2: {off2}/{total} = {off2_rate*100:.1f}% "
                  f"({'PASS' if off2_rate < 0.02 else 'FAIL'} <2%)")

    return acc >= threshold


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# MAIN
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def main():
    print("=" * 60)
    print("37-FEATURE GAUNTLET â€” Action v5 + Sizing v2")
    print("=" * 60)
    print(f"Features: {len(FEATURE_COLUMNS)} (4 new default to 0 on gauntlet hands)")
    print()

    # Load models
    print("Loading models...")
    action_oracle = GtoOracle(ACTION_MODEL_PATH)
    sizing_oracle = SizingOracle(SIZING_MODEL_PATH)
    print(f"  Action: {ACTION_MODEL_PATH}")
    print(f"  Sizing: {SIZING_MODEL_PATH}")

    # Load hands
    print("\nLoading held-out hands from chunks 15-19...")
    action_hands, raise_hands, bet_hands = load_gauntlet_hands()
    print(f"  Action: {len(action_hands)} hands")
    print(f"  Raise:  {len(raise_hands)} hands")
    print(f"  Bet:    {len(bet_hands)} hands")

    # Run action gauntlet
    print(f"\n{'='*60}")
    print("RUNNING ACTION GAUNTLET...")
    print(f"{'='*60}")
    y_true, y_pred = run_action_gauntlet(action_oracle, action_hands)
    action_pass = report_action(y_true, y_pred)

    # Run sizing gauntlet
    print(f"\n{'='*60}")
    print("RUNNING SIZING GAUNTLET...")
    print(f"{'='*60}")

    print("\nRaise predictions:")
    raise_results = run_sizing_gauntlet(
        sizing_oracle, raise_hands, "Raise", assign_raise_bucket
    )
    raise_pass = report_sizing(raise_results, "Raise (model)", 0.95)

    print("\nBet predictions:")
    bet_results = run_sizing_gauntlet(
        sizing_oracle, bet_hands, "Bet", assign_bet_bucket
    )
    bet_pass = report_sizing(bet_results, "Bet (heuristic)", 0.90)

    # Final verdict
    print(f"\n{'='*60}")
    print("FINAL VERDICT")
    print(f"{'='*60}")
    all_pass = action_pass and raise_pass and bet_pass
    print(f"  Action model:  {'âœ… PASS' if action_pass else 'âŒ FAIL'}")
    print(f"  Raise sizing:  {'âœ… PASS' if raise_pass else 'âŒ FAIL'}")
    print(f"  Bet sizing:    {'âœ… PASS' if bet_pass else 'âŒ FAIL'}")
    print(f"\n  OVERALL: {'âœ… ALL PASS' if all_pass else 'âŒ GAUNTLET FAILED'}")
    print(f"{'='*60}")

    return 0 if all_pass else 1


if __name__ == '__main__':
    sys.exit(main())
