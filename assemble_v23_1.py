#!/usr/bin/env python3
"""Assemble v2.3.1 training CSV (Layer 1 feature + Layer 2 counter-examples).

Sources — mirrors assemble_v23_clean.py + adds air-CHECK 3-way:
  1. v2.2 base (~385 rows) — re-encoded via CAT_MAPS
  2. Phase 4 labels (non-UMBRELLA, ~207 rows) — pass1_final_labels_v23.jsonl
  3. Pilot labels (~16 rows) — v23_pilot_labelled.jsonl
  4. CALL supplement (~32 rows) — pass1_final_labels_v23_call.jsonl
  5. [NEW] air-CHECK 3-way (40 rows) — v23_air_check_3way_labelled.jsonl

Feature schema: 55-col raw + 55-col attn = 110 total.
Layer 1 added `board_adjusted_hrp` (hrp * equity_vs_range); legacy
rows get it backfilled at assembly time.

Output: training-data/v2_3_1_training.csv

Per CLAUDE.md §5.1: this script's commit is the provenance record for
`river-rats-core/models/v2_3_1_model.json`. See also
`BUILDER_LABELLING_RESULTS_AIR_CHECK_2026-04-18.md`.
"""

import csv
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'river-rats-core'))

from gto_model import FEATURE_COLUMNS  # 55 cols post-Layer-1

RAW_FEATURES = list(FEATURE_COLUMNS)
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


def _backfill_board_adjusted_hrp(row):
    """If board_adjusted_hrp is missing/zero and we have hrp + equity,
    compute it. Matches feature_extractor Step 16 semantics."""
    bah = row.get("board_adjusted_hrp", 0.0)
    try:
        bah = float(bah) if bah not in (None, "") else 0.0
    except (TypeError, ValueError):
        bah = 0.0
    if bah == 0.0:
        hrp = encode_numeric(row.get("hero_range_percentile", 0.0),
                             "hero_range_percentile")
        eq = encode_numeric(row.get("equity_vs_range", 0.0), "equity_vs_range")
        row["board_adjusted_hrp"] = round(hrp * eq, 6)


def load_v22_base():
    rows = []
    with open("training-data/v2_2_training.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Backfill board_adjusted_hrp for legacy rows.
            _backfill_board_adjusted_hrp(row)
            out = {"situation_id": row["situation_id"]}
            for col in RAW_FEATURES:
                out[col] = encode_numeric(row.get(col, ""), col)
            for col in ATTN_FEATURES:
                out[col] = float(row.get(col, 1.0) or 1.0)
            # Ensure attn_board_adjusted_hrp gets default 1.0 (new column)
            if "attn_board_adjusted_hrp" in ATTN_FEATURES and \
               not row.get("attn_board_adjusted_hrp"):
                out["attn_board_adjusted_hrp"] = 1.0
            out["label"] = row["label"]
            out["label_source"] = row["label_source"]
            rows.append(out)
    return rows


def _flat_feat_dict(d):
    """For flat JSONL records (features at top level), just use d.
    For nested records with feat_dict, merge."""
    if "feat_dict" in d and isinstance(d["feat_dict"], dict):
        merged = {**d, **d["feat_dict"]}
        return merged
    return d


def load_pass1_labels_no_umbrella():
    rows = []
    with open("training-data/pass1_final_labels_v23.jsonl") as f:
        for line in f:
            d = json.loads(line)
            sid = d["situation_id"]
            if sid.startswith("UMBRELLA_"):
                continue
            d = _flat_feat_dict(d)
            _backfill_board_adjusted_hrp(d)
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
                out["label_source"] = src or "phase4"
            rows.append(out)
    return rows


def load_pilot_labels():
    rows = []
    with open("training-data/v23_pilot_labelled.jsonl") as f:
        for line in f:
            d = json.loads(line)
            feat_dict = d.get("feat_dict", {})
            merged = {**d, **feat_dict}
            _backfill_board_adjusted_hrp(merged)
            out = {"situation_id": d["situation_id"]}
            for col in RAW_FEATURES:
                if col in feat_dict:
                    val = feat_dict[col]
                elif col in merged:
                    val = merged[col]
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
            d = _flat_feat_dict(d)
            _backfill_board_adjusted_hrp(d)
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


def load_air_check_labels():
    """NEW — v2.3.1 Layer 2: 40 AIR-CHECK counter-examples."""
    rows = []
    src = "training-data/v23_air_check_3way_labelled.jsonl"
    with open(src) as f:
        for line in f:
            d = json.loads(line)
            d = _flat_feat_dict(d)
            _backfill_board_adjusted_hrp(d)
            out = {"situation_id": d["situation_id"]}
            for col in RAW_FEATURES:
                val = d.get(col, 0.0)
                if val is None:
                    val = 0.0
                out[col] = encode_numeric(val, col)
            for col in ATTN_FEATURES:
                out[col] = 1.0
            out["label"] = d["expert_action"]
            out["label_source"] = "factory_air_check_v231"
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
    print("=" * 70)
    print("v2.3.1: Assembling training CSV")
    print("  Layer 1: board_adjusted_hrp (backfilled for legacy rows)")
    print("  Layer 2: +40 air-CHECK 3-way counter-examples")
    print("=" * 70)

    print(f"\nFEATURE_COLUMNS count: {len(RAW_FEATURES)} "
          f"(expected 55 post-Layer-1)")
    if len(RAW_FEATURES) != 55:
        print(f"\n**STOP**: FEATURE_COLUMNS count is {len(RAW_FEATURES)}, "
              f"expected 55. Layer 1 not applied or Layer changed.")
        sys.exit(1)
    if "board_adjusted_hrp" not in RAW_FEATURES:
        print("\n**STOP**: 'board_adjusted_hrp' not in FEATURE_COLUMNS.")
        sys.exit(1)

    print("\n1. v2.2 base...")
    v22 = load_v22_base()
    print(f"   {len(v22)} rows")

    print("\n2. Phase 4 labels (excluding UMBRELLA)...")
    p4 = load_pass1_labels_no_umbrella()
    print(f"   {len(p4)} rows")

    print("\n3. Pilot labels...")
    pilot = load_pilot_labels()
    print(f"   {len(pilot)} rows")

    print("\n4. CALL supplement...")
    call_sup = load_call_supplement()
    print(f"   {len(call_sup)} rows")

    print("\n5. Air-CHECK 3-way (v2.3.1 Layer 2)...")
    air_check = load_air_check_labels()
    print(f"   {len(air_check)} rows")

    all_rows = v22 + p4 + pilot + call_sup + air_check
    total = len(all_rows)
    sids = [r["situation_id"] for r in all_rows]
    unique_sids = set(sids)
    dupes = total - len(unique_sids)
    print(f"\nTotal rows: {total} "
          f"(unique sids: {len(unique_sids)}, dupes: {dupes})")

    if dupes > 0:
        # Keep last occurrence — later sources override earlier.
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

    print("\n6. Verifying no string-encoded feature values...")
    errors = verify_no_strings(all_rows)
    if errors:
        print(f"**STOP**: {len(errors)} string-encoded values:")
        for e in errors[:20]:
            print(f"   {e}")
        sys.exit(1)
    print("   PASS")

    actions = Counter(row["label"] for row in all_rows)
    print(f"\n7. Action distribution:")
    for act in sorted(actions.keys()):
        pct = 100.0 * actions[act] / total
        print(f"   {act:<6}: {actions[act]:>4} ({pct:>5.1f}%)")

    source_counter = Counter(row["label_source"] for row in all_rows)
    print(f"\n8. Source distribution:")
    for src, n in source_counter.most_common():
        print(f"   {src:<40}: {n}")

    # v2.3 clean was 637 rows. Adding 40 air-CHECK → expect ~675-680.
    if total < 610 or total > 750:
        print(f"\n**STOP**: Row count {total} is off bounds (610-750).")
        sys.exit(1)

    # board_adjusted_hrp coverage check
    nonzero_bah = sum(
        1 for r in all_rows if float(r.get("board_adjusted_hrp", 0.0)) != 0.0
    )
    print(f"\n9. board_adjusted_hrp non-zero: {nonzero_bah}/{total} "
          f"({100*nonzero_bah/total:.0f}%)")

    out_path = "training-data/v2_3_1_training.csv"
    print(f"\n10. Writing {out_path}...")
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)
    print(f"    Written {total} rows")

    print("\n11. Verifying written CSV round-trip...")
    with open(out_path, newline="") as f:
        verify = list(csv.DictReader(f))
    print(f"    Read back {len(verify)} rows")
    str_issues = 0
    for row in verify:
        for col in RAW_FEATURES:
            try:
                float(row[col])
            except (ValueError, TypeError):
                str_issues += 1
    if str_issues:
        print(f"**STOP**: {str_issues} non-numeric values in output")
        sys.exit(1)
    print("    PASS")

    print(f"\n{'=' * 70}")
    print(f"ASSEMBLY COMPLETE")
    print(f"  Rows: {total} ({len(v22)} v2.2 + {len(p4)} Phase4 + "
          f"{len(pilot)} pilot + {len(call_sup)} CALL + "
          f"{len(air_check)} air-CHECK)")
    print(f"  Features: {len(RAW_FEATURES)} raw + {len(ATTN_FEATURES)} attn")
    print(f"  Output: {out_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
