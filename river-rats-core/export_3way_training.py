#!/usr/bin/env python3
"""Export labelled 3-way situations to training CSV.

Reads the labelled JSONL, excludes LOW confidence labels, writes
a 45-column CSV compatible with train_model.py.

Usage:
    python3 export_3way_training.py
    python3 export_3way_training.py --input path/to/labelled.jsonl --output path/to/csv
"""
import argparse
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from gto_model import FEATURE_COLUMNS


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'training-data')


def export_training_csv(input_path: str, output_path: str):
    """Convert labelled JSONL to training CSV, excluding LOW confidence."""

    rows = []
    excluded = 0
    confidence_counts = {}

    with open(input_path) as f:
        for line in f:
            entry = json.loads(line)
            conf = entry.get('expert_confidence', 'UNKNOWN')
            confidence_counts[conf] = confidence_counts.get(conf, 0) + 1

            if conf == 'LOW':
                excluded += 1
                continue

            expert_action = entry.get('expert_action', '')
            if not expert_action:
                excluded += 1
                continue

            feat_dict = entry.get('feat_dict', {})
            row = {col: feat_dict.get(col, 0.0) for col in FEATURE_COLUMNS}

            # Preserve 5-class expert labels as-is.
            # Vocabulary: {CHECK, BET, CALL, FOLD, RAISE}.
            # Mapping to 3-class is handled at inference time in the oracle/router.
            action = expert_action.upper()
            facing = entry.get('facing_bet', False)
            assert not (facing and action == 'CHECK'), \
                f"CHECK while facing bet: {entry.get('situation_id')}"
            assert not (not facing and action == 'CALL'), \
                f"CALL while not facing bet: {entry.get('situation_id')}"

            row['action'] = action
            rows.append(row)

    # Write CSV
    fieldnames = list(FEATURE_COLUMNS) + ['action']
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Report
    print(f"Exported {len(rows)} training rows to {output_path}")
    print(f"  Excluded: {excluded} (LOW confidence or missing label)")
    print(f"  Confidence distribution: {confidence_counts}")

    # Action distribution
    action_counts = {}
    for r in rows:
        a = r['action']
        action_counts[a] = action_counts.get(a, 0) + 1
    print(f"  Action distribution: {action_counts}")

    # Stratification
    street_counts = {}
    for r in rows:
        s = r.get('street', 0)
        # street is encoded as 0=flop, 1=turn, 2=river
        label = {0: 'flop', 0.0: 'flop', 1: 'turn', 1.0: 'turn', 2: 'river', 2.0: 'river'}.get(s, f'street_{s}')
        street_counts[label] = street_counts.get(label, 0) + 1
    print(f"  By street: {street_counts}")

    if len(rows) < 180:
        print(f"\n  WARNING: Only {len(rows)} rows — below 180 minimum.")
        print(f"  Relabel ambiguous spots or generate more situations.")

    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export labelled 3-way data to CSV')
    parser.add_argument('--input', type=str,
                        default=os.path.join(DATA_DIR, '3way_labelled.jsonl'))
    parser.add_argument('--output', type=str,
                        default=os.path.join(DATA_DIR, 'train_3way_45.csv'))
    args = parser.parse_args()

    export_training_csv(args.input, args.output)
