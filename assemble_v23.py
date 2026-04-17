#!/usr/bin/env python3
"""
Phase 5: Assemble v2.3 training CSV from three sources.

1. v2.2 base (385 hands) - re-encoded through CAT_MAPS
2. Phase 4 labels (470 hands) - from pass1_final_labels_v23.jsonl
3. Pilot labels (16 hands) - from v23_pilot_labelled.jsonl

Output: training-data/v2_3_training.csv (871 rows)
"""

import csv
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'river-rats-core'))

from train_model_v2_2 import CAT_MAPS, encode
from gto_model import FEATURE_COLUMNS

# --------------------------------------------------------------------------
# Column schema (matches v2_2_training.csv header exactly)
# --------------------------------------------------------------------------
RAW_FEATURES = list(FEATURE_COLUMNS)  # 54 columns
ATTN_FEATURES = [f"attn_{c}" for c in RAW_FEATURES]  # 54 columns
META_COLS = ["situation_id", "label", "label_source"]
HEADER = ["situation_id"] + RAW_FEATURES + ATTN_FEATURES + ["label", "label_source"]

# Street/position encoding maps (same as CAT_MAPS but for raw values)
STREET_TO_NUM = {"flop": 0, "turn": 1, "river": 2, "f": 0, "t": 1, "r": 2}
POS_TO_NUM = {"UTG": 0, "HJ": 1, "CO": 2, "BTN": 3, "SB": 4, "BB": 5}

# Solver-enqueued label sources that get tagged as provisional
SOLVER_PENDING_SOURCES = {"pass2_review", "pass2_override"}


def encode_numeric(val, col):
    """Ensure a value is numeric for a feature column."""
    if col == "street":
        if isinstance(val, str):
            return STREET_TO_NUM.get(val.lower(), 0)
        return float(val)
    if col == "hero_position":
        if isinstance(val, str):
            return POS_TO_NUM.get(val, 0)
        return float(val)
    if col == "villain_position":
        if isinstance(val, str):
            return POS_TO_NUM.get(val, 0)
        return float(val)
    if isinstance(val, bool):
        return int(val)
    if val is None or val == "":
        return 0.0
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0


def load_v22_base():
    """Load and re-encode v2.2 training data through CAT_MAPS."""
    rows = []
    with open("training-data/v2_2_training.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            out = {}
            out["situation_id"] = row["situation_id"]
            for col in RAW_FEATURES:
                out[col] = encode_numeric(row.get(col, ""), col)
            for col in ATTN_FEATURES:
                out[col] = float(row.get(col, 0))
            out["label"] = row["label"]
            out["label_source"] = row["label_source"]
            rows.append(out)
    return rows


def load_pass1_labels():
    """Load Phase 4 labels from pass1_final_labels_v23.jsonl."""
    rows = []
    with open("training-data/pass1_final_labels_v23.jsonl") as f:
        for line in f:
            d = json.loads(line)
            out = {}
            out["situation_id"] = d["situation_id"]

            # Features are at top level in this file
            for col in RAW_FEATURES:
                val = d.get(col)
                if val is None:
                    val = 0.0
                out[col] = encode_numeric(val, col)

            # attn_* all set to 1.0
            for col in ATTN_FEATURES:
                out[col] = 1.0

            out["label"] = d["expert_action"]

            # Tag solver-pending hands
            src = d.get("label_source", "")
            if src in SOLVER_PENDING_SOURCES:
                out["label_source"] = "provisional_solver_pending"
            else:
                out["label_source"] = src

            rows.append(out)
    return rows


def load_pilot_labels():
    """Load pilot labels from v23_pilot_labelled.jsonl."""
    rows = []
    with open("training-data/v23_pilot_labelled.jsonl") as f:
        for line in f:
            d = json.loads(line)
            feat_dict = d.get("feat_dict", {})
            out = {}
            out["situation_id"] = d["situation_id"]

            for col in RAW_FEATURES:
                # Some features at top level, most in feat_dict
                if col in feat_dict:
                    val = feat_dict[col]
                elif col in d:
                    val = d[col]
                else:
                    val = 0.0
                out[col] = encode_numeric(val, col)

            # attn_* all set to 1.0
            for col in ATTN_FEATURES:
                out[col] = 1.0

            out["label"] = d["final_action"]
            out["label_source"] = "pilot_v23"

            rows.append(out)
    return rows


def verify_no_strings(rows):
    """Verify zero string values in any feature column."""
    errors = []
    for i, row in enumerate(rows):
        for col in RAW_FEATURES + ATTN_FEATURES:
            val = row[col]
            if isinstance(val, str):
                errors.append(f"Row {i} ({row['situation_id']}): {col}={val!r} is string")
    return errors


def main():
    print("=" * 60)
    print("Phase 5: Assembling v2.3 training CSV")
    print("=" * 60)

    # Load all sources
    print("\n1. Loading v2.2 base (re-encoding through CAT_MAPS)...")
    v22 = load_v22_base()
    print(f"   Loaded {len(v22)} rows")

    print("\n2. Loading Phase 4 labels...")
    p4 = load_pass1_labels()
    print(f"   Loaded {len(p4)} rows")
    solver_pending = sum(1 for r in p4 if r["label_source"] == "provisional_solver_pending")
    print(f"   Tagged {solver_pending} as provisional_solver_pending")

    print("\n3. Loading pilot labels...")
    pilot = load_pilot_labels()
    print(f"   Loaded {len(pilot)} rows")

    # Combine
    all_rows = v22 + p4 + pilot
    total = len(all_rows)
    print(f"\nTotal rows: {total}")

    if total != 871:
        print(f"STOP: Expected 871 rows, got {total}")
        sys.exit(1)

    # Verify no string values in feature columns
    print("\n4. Verifying no string-encoded feature values...")
    errors = verify_no_strings(all_rows)
    if errors:
        print(f"STOP: Found {len(errors)} string-encoded values:")
        for e in errors[:20]:
            print(f"   {e}")
        sys.exit(1)
    print("   PASS: Zero string-encoded feature values")

    # Verify street and hero_position are numeric
    streets = set(row["street"] for row in all_rows)
    heros = set(row["hero_position"] for row in all_rows)
    print(f"   street values: {sorted(streets)}")
    print(f"   hero_position values: {sorted(heros)}")
    for s in streets:
        assert isinstance(s, (int, float)), f"street={s!r} is not numeric"
    for h in heros:
        assert isinstance(h, (int, float)), f"hero_position={h!r} is not numeric"
    print("   PASS: street and hero_position are all numeric")

    # Action distribution
    from collections import Counter
    actions = Counter(row["label"] for row in all_rows)
    print(f"\n5. Action distribution: {dict(sorted(actions.items()))}")

    # Write CSV
    out_path = "training-data/v2_3_training.csv"
    print(f"\n6. Writing {out_path}...")
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)
    print(f"   Written {total} rows")

    # Verify written CSV
    print("\n7. Verifying written CSV...")
    with open(out_path, newline="") as f:
        reader = csv.DictReader(f)
        verify_rows = list(reader)
    print(f"   Read back {len(verify_rows)} rows")

    # Check for any string-encoded feature values in the written CSV
    str_issues = 0
    for row in verify_rows:
        for col in RAW_FEATURES:
            v = row[col]
            try:
                float(v)
            except (ValueError, TypeError):
                str_issues += 1
                print(f"   STRING ISSUE: {row['situation_id']}.{col}={v!r}")
    if str_issues:
        print(f"STOP: {str_issues} string-encoded values in output CSV")
        sys.exit(1)
    print("   PASS: All feature values are numeric in written CSV")

    print("\n" + "=" * 60)
    print("Phase 5 COMPLETE")
    print(f"  Rows: {total} (385 v2.2 + 470 Phase 4 + 16 pilot)")
    print(f"  Solver-pending: {solver_pending}")
    print(f"  Output: {out_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
