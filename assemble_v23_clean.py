#!/usr/bin/env python3
"""
Phase 5 (Option 4+3): Assemble v2.3-clean training CSV.

Sources (NO UMBRELLA, NO class weighting):
1. v2.2 base (385 rows) — re-encoded via CAT_MAPS
2. Phase 4 labels (non-UMBRELLA only, ~207 rows) — pass1_final_labels_v23.jsonl
3. Pilot labels (16 rows) — v23_pilot_labelled.jsonl
4. CALL supplement (~32 rows) — pass1_final_labels_v23_call.jsonl

Output: training-data/v2_3_clean_training.csv
"""

import csv
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'river-rats-core'))

from train_model_v2_2 import CAT_MAPS, encode
from gto_model import FEATURE_COLUMNS

# Column schema
RAW_FEATURES = list(FEATURE_COLUMNS)  # 54 columns
ATTN_FEATURES = [f"attn_{c}" for c in RAW_FEATURES]
HEADER = ["situation_id"] + RAW_FEATURES + ATTN_FEATURES + ["label", "label_source"]

STREET_TO_NUM = {"flop": 0, "turn": 1, "river": 2, "f": 0, "t": 1, "r": 2}
POS_TO_NUM = {"UTG": 0, "HJ": 1, "CO": 2, "BTN": 3, "SB": 4, "BB": 5}


def encode_numeric(val, col):
    if col == "street":
        if isinstance(val, str):
            return STREET_TO_NUM.get(val.lower(), 0)
        return float(val)
    if col in ("hero_position", "villain_position"):
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
    rows = []
    with open("training-data/v2_2_training.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            out = {"situation_id": row["situation_id"]}
            for col in RAW_FEATURES:
                out[col] = encode_numeric(row.get(col, ""), col)
            for col in ATTN_FEATURES:
                out[col] = float(row.get(col, 0))
            out["label"] = row["label"]
            out["label_source"] = row["label_source"]
            rows.append(out)
    return rows


def load_pass1_labels_no_umbrella():
    rows = []
    with open("training-data/pass1_final_labels_v23.jsonl") as f:
        for line in f:
            d = json.loads(line)
            sid = d["situation_id"]
            if sid.startswith("UMBRELLA_"):
                continue
            out = {"situation_id": sid}
            for col in RAW_FEATURES:
                val = d.get(col, 0.0)
                if val is None:
                    val = 0.0
                out[col] = encode_numeric(val, col)
            for col in ATTN_FEATURES:
                out[col] = 1.0
            out["label"] = d["expert_action"]
            src = d.get("label_source", "")
            if src in ("pass2_review", "pass2_override"):
                out["label_source"] = "provisional_solver_pending"
            else:
                out["label_source"] = src
            rows.append(out)
    return rows


def load_pilot_labels():
    rows = []
    with open("training-data/v23_pilot_labelled.jsonl") as f:
        for line in f:
            d = json.loads(line)
            feat_dict = d.get("feat_dict", {})
            out = {"situation_id": d["situation_id"]}
            for col in RAW_FEATURES:
                if col in feat_dict:
                    val = feat_dict[col]
                elif col in d:
                    val = d[col]
                else:
                    val = 0.0
                out[col] = encode_numeric(val, col)
            for col in ATTN_FEATURES:
                out[col] = 1.0
            out["label"] = d["final_action"]
            out["label_source"] = "pilot_v23"
            rows.append(out)
    return rows


def load_call_supplement():
    rows = []
    with open("training-data/pass1_final_labels_v23_call.jsonl") as f:
        for line in f:
            d = json.loads(line)
            out = {"situation_id": d["situation_id"]}
            for col in RAW_FEATURES:
                val = d.get(col, 0.0)
                if val is None:
                    val = 0.0
                out[col] = encode_numeric(val, col)
            for col in ATTN_FEATURES:
                out[col] = 1.0
            out["label"] = d["expert_action"]
            out["label_source"] = d.get("label_source", "factory_call_supplement")
            rows.append(out)
    return rows


def verify_no_strings(rows):
    errors = []
    for i, row in enumerate(rows):
        for col in RAW_FEATURES + ATTN_FEATURES:
            val = row[col]
            if isinstance(val, str):
                errors.append(f"Row {i} ({row['situation_id']}): {col}={val!r}")
    return errors


def main():
    print("=" * 60)
    print("Option 4+3: Assembling v2.3-clean training CSV")
    print("  NO UMBRELLA — NO class weighting")
    print("=" * 60)

    # 1. v2.2 base
    print("\n1. Loading v2.2 base...")
    v22 = load_v22_base()
    print(f"   {len(v22)} rows")

    # 2. Phase 4 labels (no UMBRELLA)
    print("\n2. Loading Phase 4 labels (excluding UMBRELLA)...")
    p4 = load_pass1_labels_no_umbrella()
    print(f"   {len(p4)} rows")

    # 3. Pilot
    print("\n3. Loading pilot labels...")
    pilot = load_pilot_labels()
    print(f"   {len(pilot)} rows")

    # 4. CALL supplement
    print("\n4. Loading CALL supplement...")
    call_sup = load_call_supplement()
    print(f"   {len(call_sup)} rows")

    # Combine — check for duplicates
    all_rows = v22 + p4 + pilot + call_sup
    total = len(all_rows)
    sids = [r["situation_id"] for r in all_rows]
    unique_sids = set(sids)
    dupes = total - len(unique_sids)
    print(f"\nTotal rows: {total} (unique sids: {len(unique_sids)}, dupes: {dupes})")

    # Deduplicate: keep last occurrence (later sources override earlier)
    if dupes > 0:
        seen = set()
        deduped = []
        for row in reversed(all_rows):
            if row["situation_id"] not in seen:
                seen.add(row["situation_id"])
                deduped.append(row)
        deduped.reverse()
        all_rows = deduped
        total = len(all_rows)
        print(f"   After dedup: {total} rows")

    # Verify no strings
    print("\n5. Verifying no string-encoded feature values...")
    errors = verify_no_strings(all_rows)
    if errors:
        print(f"STOP: {len(errors)} string-encoded values:")
        for e in errors[:20]:
            print(f"   {e}")
        sys.exit(1)
    print("   PASS")

    # Action distribution
    actions = Counter(row["label"] for row in all_rows)
    print(f"\n6. Action distribution:")
    for act in sorted(actions.keys()):
        pct = 100.0 * actions[act] / total
        print(f"   {act}: {actions[act]} ({pct:.1f}%)")

    # Stop condition: row count off by >10% from ~640
    if total < 576 or total > 704:
        print(f"\nSTOP: Row count {total} is off by >10% from ~640")
        sys.exit(1)

    # Write CSV
    out_path = "training-data/v2_3_clean_training.csv"
    print(f"\n7. Writing {out_path}...")
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)
    print(f"   Written {total} rows")

    # Verify readback
    print("\n8. Verifying written CSV...")
    with open(out_path, newline="") as f:
        verify = list(csv.DictReader(f))
    print(f"   Read back {len(verify)} rows")
    str_issues = 0
    for row in verify:
        for col in RAW_FEATURES:
            try:
                float(row[col])
            except (ValueError, TypeError):
                str_issues += 1
    if str_issues:
        print(f"STOP: {str_issues} non-numeric values in output")
        sys.exit(1)
    print("   PASS")

    print(f"\n{'=' * 60}")
    print(f"ASSEMBLY COMPLETE")
    print(f"  Rows: {total} ({len(v22)} v2.2 + {len(p4)} Phase4 + "
          f"{len(pilot)} pilot + {len(call_sup)} CALL)")
    print(f"  Output: {out_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
