#!/usr/bin/env python3
"""Phase 1.5-D.3 FULL §(c.1) — sanitized JSONL calibration extracts.

Per dispatch MAIN_TERMINAL_HU14_ADJUDICATION_AND_PHASE15D3_FULL_DISPATCH_2026-05-10.md §(c.1):
strip `expert_action`, `expert_reasoning`, `oracle_action`, and other forward-leaking fields
from calibration source files BEFORE labellers grep them.

Pilot V2 contamination: L2 + L4 self-disclosed grep returning these fields. Sanitization
preserves transparency without blocking labellers' independent reasoning (per L1's clean
26/28 score).

Architect-hat HOW (per dispatch's commit-WHAT, builder-decides-HOW):
- Sanitization step lives PRE-EXTRACT (this script): produces clean JSONL files in a
  fresh directory; labellers point at the clean files via labeller_brief.
- Forbidden fields: `expert_action`, `expert_reasoning`, `oracle_action`,
  `is_correct_action`, `solver_action`, `solver_frequencies`, `gto_action`,
  `expected_label`, `correct_action`, `recommended_action` (defensive grep against any
  field name pattern that signals the answer).
- Verification: post-sanitize grep for each forbidden field returns ZERO matches in
  output files.

Usage:
    python3 scripts/sanitize_calibration_extracts.py --output data/hu_corpus/full_HU2_HU6/calibration_sources

Output files (per dispatch):
- {output}/test_set_50_labelled_SANITIZED.jsonl
- {output}/3way_combined_350_SANITIZED.jsonl
- {output}/BATCH2_8_HAND_DESIGNS_SANITIZED.md (markdown sanitization is best-effort
  prose-stripping; structured JSONL is the primary sanitization target)
- {output}/_sanitization_report.json (audit trail: source files, fields stripped,
  match counts post-sanitize)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Dict, List

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORBIDDEN_FIELDS = [
    "expert_action",
    "expert_reasoning",
    "oracle_action",
    "is_correct_action",
    "solver_action",
    "solver_frequencies",
    "gto_action",
    "expected_label",
    "correct_action",
    "recommended_action",
    "expert_confidence",
    "label",
    "answer",
]

JSONL_SOURCES = [
    ("training-data/test_set_50_labelled.jsonl", "test_set_50_labelled_SANITIZED.jsonl"),
    ("training-data/3way_combined_350.jsonl", "3way_combined_350_SANITIZED.jsonl"),
]


def _sanitize_jsonl(src_rel: str, out_path: str) -> Dict:
    """Read a JSONL file, strip forbidden fields from each row, write to out_path.

    Returns a per-file report dict: stripped counts per field, total rows.
    """
    src_path = os.path.join(REPO, src_rel)
    if not os.path.exists(src_path):
        print(f"WARN source missing: {src_path}", file=sys.stderr)
        return {"src": src_rel, "missing": True}

    stripped_counts = {f: 0 for f in FORBIDDEN_FIELDS}
    total_rows = 0
    with open(src_path) as f, open(out_path, "w") as out:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total_rows += 1
            row = json.loads(line)
            # Strip top-level forbidden fields
            for field in FORBIDDEN_FIELDS:
                if field in row:
                    del row[field]
                    stripped_counts[field] += 1
            # Recursively strip from nested dicts (e.g., feat_dict shouldn't leak)
            _strip_nested(row, stripped_counts)
            out.write(json.dumps(row) + "\n")

    # Verify: post-sanitize grep
    post_grep_matches = {}
    with open(out_path) as f:
        content = f.read()
    for field in FORBIDDEN_FIELDS:
        # Count occurrences as JSON keys (with quote)
        matches = content.count(f'"{field}"')
        post_grep_matches[field] = matches

    return {
        "src": src_rel,
        "out": out_path,
        "total_rows": total_rows,
        "stripped_counts": stripped_counts,
        "post_grep_matches": post_grep_matches,
    }


def _strip_nested(obj, stripped_counts: Dict):
    """Recursively strip forbidden fields from nested dicts/lists."""
    if isinstance(obj, dict):
        for field in FORBIDDEN_FIELDS:
            if field in obj:
                del obj[field]
                stripped_counts[field] += 1
        for value in obj.values():
            _strip_nested(value, stripped_counts)
    elif isinstance(obj, list):
        for item in obj:
            _strip_nested(item, stripped_counts)


def _sanitize_markdown(src_rel: str, out_path: str) -> Dict:
    """Sanitize a markdown reference-set file by stripping expert-action prose lines.

    Best-effort: for the BATCH2 hand designs file, strips lines that contain
    `Expert action:` or `Expert label:` or `Solver action:` or similar answer-leaking patterns.
    Preserves the rest of the file (situation specs, axis descriptions).
    """
    src_path = os.path.join(REPO, src_rel)
    if not os.path.exists(src_path):
        return {"src": src_rel, "missing": True}

    forbidden_patterns = [
        r"^\s*[\-\*]?\s*\*\*?Expert\s+action\*?\*?:.*$",
        r"^\s*[\-\*]?\s*\*\*?Expert\s+label\*?\*?:.*$",
        r"^\s*[\-\*]?\s*\*\*?Solver\s+action\*?\*?:.*$",
        r"^\s*[\-\*]?\s*\*\*?Recommended\s+action\*?\*?:.*$",
        r"^\s*[\-\*]?\s*\*\*?Correct\s+action\*?\*?:.*$",
        r"^\s*[\-\*]?\s*\*\*?Oracle\s+action\*?\*?:.*$",
        r"^\s*[\-\*]?\s*\*\*?Expert\s+reasoning\*?\*?:.*$",
        r"^\s*[\-\*]?\s*\*\*?GTO\s+action\*?\*?:.*$",
    ]
    pattern = re.compile("|".join(forbidden_patterns), re.IGNORECASE)

    stripped_lines = 0
    total_lines = 0
    with open(src_path) as f, open(out_path, "w") as out:
        for line in f:
            total_lines += 1
            if pattern.match(line):
                stripped_lines += 1
                continue  # skip this line
            out.write(line)

    return {
        "src": src_rel,
        "out": out_path,
        "total_lines": total_lines,
        "stripped_lines": stripped_lines,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 1.5-D.3 FULL §(c.1) sanitization")
    parser.add_argument("--output", required=True, help="Output directory for sanitized files")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    report = {"forbidden_fields": FORBIDDEN_FIELDS, "files": []}

    # Sanitize JSONL files
    for src_rel, out_name in JSONL_SOURCES:
        out_path = os.path.join(args.output, out_name)
        result = _sanitize_jsonl(src_rel, out_path)
        report["files"].append(result)
        if result.get("missing"):
            continue
        # Verify zero post-grep matches
        violations = {f: c for f, c in result["post_grep_matches"].items() if c > 0}
        if violations:
            print(f"FAIL post-sanitize grep found violations in {result['out']}: {violations}", file=sys.stderr)
            return 1
        print(
            f"  ✓ {result['out']}: {result['total_rows']} rows; stripped "
            f"{sum(result['stripped_counts'].values())} fields total",
            file=sys.stderr,
        )

    # Sanitize BATCH2 markdown
    md_src = "design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md"
    md_out = os.path.join(args.output, "BATCH2_8_HAND_DESIGNS_SANITIZED.md")
    md_result = _sanitize_markdown(md_src, md_out)
    report["files"].append(md_result)
    if not md_result.get("missing"):
        print(
            f"  ✓ {md_result['out']}: {md_result['total_lines']} lines; stripped "
            f"{md_result['stripped_lines']} answer-leaking lines",
            file=sys.stderr,
        )

    # Write audit report
    report_path = os.path.join(args.output, "_sanitization_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"  ✓ {report_path}: audit report written", file=sys.stderr)

    print(f"\nSanitization complete. Output: {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
