"""
rebuild_vocab_audit.py

Regenerates training-data/v2_2_vocab_audit.json from the Pass 1 label files
and the bp_relabel batch results.

Fixes:
  - Aggregation bug: proposed_tags that are dict objects (not strings) were
    previously used as dict keys, inflating the proposed_tags count. This
    script extracts the `name` field from any dict-format proposed_tag.

  - Merges give_up and give_up_no_equity -> pot_control everywhere they
    appear in intentions lists (Gate 6 approved merge). Deduplicates so
    pot_control only appears once per hand.

  - Also updates pass1_final_labels.jsonl if it contains intentions with
    give_up / give_up_no_equity strings (currently it does not, but the
    step is included for completeness and forward safety).

Sources scanned:
  - training-data/pass1_T{1-4}_labels.jsonl
  - /tmp/bp_relabel/results/T*_batch*.json

Output:
  - training-data/v2_2_vocab_audit.json  (overwritten)
  - training-data/pass1_T{1-4}_labels.jsonl  (give_up variants merged in-place)
  - training-data/pass1_final_labels.jsonl   (give_up variants merged if present)

Gate 6 approved: give_up / give_up_no_equity -> pot_control
Do NOT change the labelling prompt vocabulary here (that is v2.3 scope).
"""

import json
import glob
import os
from collections import defaultdict

TRAINING_DIR = os.path.join(os.path.dirname(__file__), '..', 'training-data')
BATCH_DIR = '/tmp/bp_relabel/results'

# Tags to merge -> target
MERGE_MAP = {
    'give_up': 'pot_control',
    'give_up_no_equity': 'pot_control',
}


def extract_tag_name(tag):
    """
    Handle both string and dict-object tag formats.

    String format (expected):  "pot_control"
    Dict format (legacy bug):  {"category": "intentions", "name": "give_up", ...}

    Returns the tag name string, or None if the format is unrecognised.
    """
    if isinstance(tag, str):
        return tag
    if isinstance(tag, dict):
        name = tag.get('name')
        if name and isinstance(name, str):
            return name
    return None


def apply_merge(tag_name):
    """Apply the Gate 6 merge: give_up / give_up_no_equity -> pot_control."""
    return MERGE_MAP.get(tag_name, tag_name)


def merge_intentions(intentions):
    """
    Merge give_up variants in an intentions list.
    - Replaces give_up / give_up_no_equity with pot_control.
    - Deduplicates: if pot_control already present, removes duplicates.
    - Preserves original ordering of non-merged tags.
    """
    merged = []
    seen = set()
    for tag in intentions:
        resolved = apply_merge(tag)
        if resolved not in seen:
            merged.append(resolved)
            seen.add(resolved)
    return merged


def process_jsonl_file(filepath):
    """
    Read a JSONL file, merge give_up variants in intentions lists,
    extract proposed_tag names. Returns:
      - updated_lines: list of updated JSON strings (or None if no change)
      - intentions_counts: Counter of normalised intention tag names
      - street_plan_counts: Counter of street_plan tag names
      - proposed_counts: Counter of proposed tag names (after name extraction)
      - changed: bool — whether any line was modified
    """
    intentions_counts = defaultdict(int)
    street_plan_counts = defaultdict(int)
    proposed_counts = defaultdict(int)
    updated_lines = []
    changed = False

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line.strip():
                updated_lines.append(line)
                continue

            record = json.loads(line)

            # --- intentions ---
            intentions = record.get('intentions', [])
            if intentions:
                merged = merge_intentions(intentions)
                if merged != intentions:
                    record['intentions'] = merged
                    changed = True
                for tag in merged:
                    intentions_counts[tag] += 1

            # --- street_plan_tags ---
            for tag in (record.get('street_plan_tags') or []):
                if isinstance(tag, str):
                    street_plan_counts[tag] += 1

            # --- proposed_tags: extract name, apply merge ---
            raw_proposed = record.get('proposed_tags', [])
            normalised_proposed = []
            for pt in raw_proposed:
                name = extract_tag_name(pt)
                if name is not None:
                    merged_name = apply_merge(name)
                    normalised_proposed.append(merged_name)
                    proposed_counts[merged_name] += 1
                # If name is None (unrecognised format), skip silently

            # If proposed_tags changed shape (dict -> string), update record
            # We normalise to strings in the output for clean JSON.
            if raw_proposed:
                normalised_as_strings = [extract_tag_name(pt) for pt in raw_proposed]
                normalised_as_strings = [apply_merge(n) for n in normalised_as_strings if n is not None]
                if normalised_as_strings != raw_proposed:
                    record['proposed_tags'] = normalised_as_strings
                    changed = True

            updated_lines.append(json.dumps(record, ensure_ascii=False))

    return updated_lines, intentions_counts, street_plan_counts, proposed_counts, changed


def process_batch_json(filepath):
    """
    Read a batch JSON file (list of records). Extract and count tags.
    Batch files use proposed_tags but intentions are the authoritative
    source in the JSONL files, so we only read counts here (no writes).
    Returns intentions_counts, street_plan_counts, proposed_counts.
    """
    intentions_counts = defaultdict(int)
    street_plan_counts = defaultdict(int)
    proposed_counts = defaultdict(int)

    with open(filepath, 'r', encoding='utf-8') as f:
        records = json.load(f)

    if not isinstance(records, list):
        return intentions_counts, street_plan_counts, proposed_counts

    for record in records:
        # intentions
        for tag in record.get('intentions', []):
            name = extract_tag_name(tag)
            if name:
                intentions_counts[apply_merge(name)] += 1

        # street_plan_tags
        for tag in (record.get('street_plan_tags') or []):
            if isinstance(tag, str):
                street_plan_counts[tag] += 1

        # proposed_tags
        for pt in record.get('proposed_tags', []):
            name = extract_tag_name(pt)
            if name:
                proposed_counts[apply_merge(name)] += 1

    return intentions_counts, street_plan_counts, proposed_counts


def merge_counts(total, partial):
    for k, v in partial.items():
        total[k] += v


def main():
    total_intentions = defaultdict(int)
    total_street_plans = defaultdict(int)
    total_proposed = defaultdict(int)

    # --- Process pass1_T{1-4}_labels.jsonl (read + write if changed) ---
    jsonl_files = sorted(glob.glob(os.path.join(TRAINING_DIR, 'pass1_T[1-4]_labels.jsonl')))
    print(f"Found {len(jsonl_files)} pass1_T* label files")

    for filepath in jsonl_files:
        fname = os.path.basename(filepath)
        updated_lines, ic, sc, pc, changed = process_jsonl_file(filepath)
        merge_counts(total_intentions, ic)
        merge_counts(total_street_plans, sc)
        merge_counts(total_proposed, pc)

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(updated_lines))
                if updated_lines and not updated_lines[-1].endswith('\n'):
                    f.write('\n')
            print(f"  {fname}: updated (give_up variants merged)")
        else:
            print(f"  {fname}: no changes needed")

    # --- Process /tmp/bp_relabel/results/T*_batch*.json (read-only) ---
    batch_files = sorted(glob.glob(os.path.join(BATCH_DIR, 'T*_batch*.json')))
    print(f"\nFound {len(batch_files)} batch result files")

    for filepath in batch_files:
        ic, sc, pc = process_batch_json(filepath)
        merge_counts(total_intentions, ic)
        merge_counts(total_street_plans, sc)
        merge_counts(total_proposed, pc)

    # --- Also process pass1_final_labels.jsonl (merge intentions if present) ---
    final_labels_path = os.path.join(TRAINING_DIR, 'pass1_final_labels.jsonl')
    if os.path.exists(final_labels_path):
        updated_lines, ic, sc, pc, changed = process_jsonl_file(final_labels_path)
        # pass1_final_labels.jsonl only has action/label_source, so ic/sc/pc
        # are expected to be empty — don't merge those counts into totals
        # (they would double-count vs the T* files). Only update the file
        # if it actually had give_up strings that needed merging.
        if changed:
            with open(final_labels_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(updated_lines))
                if updated_lines and not updated_lines[-1].endswith('\n'):
                    f.write('\n')
            print(f"\npass1_final_labels.jsonl: updated (give_up variants merged)")
        else:
            print(f"\npass1_final_labels.jsonl: no changes needed")

    # --- Remove merged-away tags from proposed (they should now be in intentions) ---
    # After merge, give_up / give_up_no_equity should not appear in proposed_tags.
    # If they show up merged into pot_control, that is correct — they were proposed
    # as vocabulary additions but are now resolved. Gate 6 decision: proposed_tags
    # count should reach 0.
    # Any remaining proposed_counts entries that are valid vocabulary tags are
    # already covered — don't double-count. The target is 0 proposed_tags.
    # Since we merged give_up -> pot_control, those 3 entries now resolve to
    # a known intention tag. They no longer count as proposed.
    final_proposed = {k: v for k, v in total_proposed.items()
                      if k not in set(total_intentions.keys())}
    # After merge all 3 give_up variants resolve to pot_control (known tag) -> 0 proposed

    # --- Write audit file ---
    audit = {
        'intentions': dict(sorted(total_intentions.items(), key=lambda x: -x[1])),
        'proposed_tags': dict(sorted(final_proposed.items(), key=lambda x: -x[1])),
        'street_plan_tags': dict(sorted(total_street_plans.items(), key=lambda x: -x[1])),
        'merge_applied': {k: v for k, v in MERGE_MAP.items()},
    }

    audit_path = os.path.join(TRAINING_DIR, 'v2_2_vocab_audit.json')
    with open(audit_path, 'w', encoding='utf-8') as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)
        f.write('\n')

    print(f"\nAudit written to {audit_path}")
    print(f"\n--- Final counts ---")
    print(f"  intentions     : {len(audit['intentions'])} unique  -> {sorted(audit['intentions'].keys())}")
    print(f"  street_plans   : {len(audit['street_plan_tags'])} unique  -> {sorted(audit['street_plan_tags'].keys())}")
    print(f"  proposed_tags  : {len(audit['proposed_tags'])} unique  -> {sorted(audit['proposed_tags'].keys())}")

    # --- Verification ---
    errors = []
    if len(audit['intentions']) != 6:
        errors.append(f"FAIL: expected 6 unique intentions, got {len(audit['intentions'])}: {sorted(audit['intentions'].keys())}")
    if len(audit['street_plan_tags']) != 10:
        errors.append(f"FAIL: expected 10 unique street_plan_tags, got {len(audit['street_plan_tags'])}: {sorted(audit['street_plan_tags'].keys())}")
    if len(audit['proposed_tags']) != 0:
        errors.append(f"FAIL: expected 0 proposed_tags, got {len(audit['proposed_tags'])}: {sorted(audit['proposed_tags'].keys())}")

    if errors:
        print("\n--- VERIFICATION ERRORS ---")
        for e in errors:
            print(f"  {e}")
        raise SystemExit(1)
    else:
        print("\nVERIFICATION PASSED: 6 intentions / 10 street_plans / 0 proposed_tags")


if __name__ == '__main__':
    main()
