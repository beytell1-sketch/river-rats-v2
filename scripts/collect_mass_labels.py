#!/usr/bin/env python3
"""Mass-labelling result aggregator (Phase 11A).

Per `MAIN_TERMINAL_MASS_LABELLING_RESOLUTION_2026-04-27.md`
(master `feb6652`): aggregates the 5 per-labeller JSON files produced
by sonnet subagents into a single flat JSONL keyed by ``ref_id`` with
plurality consensus across the 5 votes.

Output schema (one row per hand)::

    {
      "ref_id": "<unique hand id>",
      "pilot_hand_id": "<original PILOT_xxx if present, else null>",
      "labels": [
        {"labeller_id": 1, "action": "BET",   "confidence": "HIGH",
         "reasoning": "..."},
        {"labeller_id": 2, "action": "BET",   "confidence": "MEDIUM",
         "reasoning": "..."},
        {"labeller_id": 3, "action": "CHECK", "confidence": "LOW",
         "reasoning": "..."},
        {"labeller_id": 4, "action": null,    "confidence": "LOW",
         "reasoning": "refusal"},
        {"labeller_id": 5, "action": "BET",   "confidence": "HIGH",
         "reasoning": "..."}
      ],
      "consensus_action": "BET",
      "consensus_confidence": 0.6,    // count_max / total_non_null
      "vote_count": 5,                // number of labels received
      "valid_vote_count": 4,          // non-null votes
      "feat_dict": {...}              // copied from the corpus record
    }

Usage::

    python3 scripts/collect_mass_labels.py \\
        --corpus data/corpus_revision_500_hand_2026-04-27.jsonl \\
        --labels-dir review/mass_labelling_2026-04-27/ \\
        --output data/corpus_revision_500_hand_labels_2026-04-27.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from typing import Any, Dict, List, Optional

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dispatch_mass_labelling import compute_ref_id  # noqa: E402


_VALID_ACTIONS = {'BET', 'RAISE', 'CALL', 'CHECK', 'FOLD'}
_VALID_CONFIDENCES = {'HIGH', 'MEDIUM', 'LOW'}


def consensus(votes: List[Optional[str]]) -> Dict[str, Any]:
    """Compute plurality consensus across labeller votes.

    Null votes (refusals) are excluded from the tally; the consensus
    confidence is ``count_max / count_non_null``. With zero non-null
    votes, returns consensus_action = None and confidence = 0.0.

    On a tie, returns the alphabetically first action (deterministic).
    """
    non_null = [v for v in votes if v is not None]
    valid_count = len(non_null)
    total_count = len(votes)

    if valid_count == 0:
        return {
            'consensus_action': None,
            'consensus_confidence': 0.0,
            'vote_count': total_count,
            'valid_vote_count': 0,
        }

    counter = Counter(non_null)
    top_count = max(counter.values())
    tied = sorted(a for a, c in counter.items() if c == top_count)
    consensus_action = tied[0]

    return {
        'consensus_action': consensus_action,
        'consensus_confidence': round(top_count / valid_count, 4),
        'vote_count': total_count,
        'valid_vote_count': valid_count,
    }


def _load_labeller_file(path: str) -> Dict[str, Dict[str, Any]]:
    """Read a per-labeller JSON file and return labels keyed by ref_id.

    Validates each entry's shape but does not reject the whole file on
    individual bad entries; bad entries are surfaced via stderr and
    skipped so the rest of the labels are still aggregated.
    """
    with open(path) as f:
        payload = json.load(f)
    labels = payload.get('labels', [])
    if not isinstance(labels, list):
        raise ValueError(f"{path}: 'labels' is not a list")

    out: Dict[str, Dict[str, Any]] = {}
    for i, entry in enumerate(labels):
        ref_id = entry.get('ref_id')
        if not ref_id:
            print(f"[collect] {path} entry {i}: missing ref_id; skipped",
                  file=sys.stderr)
            continue
        action = entry.get('action')
        if action is not None:
            action = str(action).upper()
            if action not in _VALID_ACTIONS:
                print(f"[collect] {path} entry {ref_id}: invalid action "
                      f"{action!r}; coerced to null", file=sys.stderr)
                action = None
        confidence = str(entry.get('confidence', 'LOW')).upper()
        if confidence not in _VALID_CONFIDENCES:
            confidence = 'LOW'
        out[ref_id] = {
            'action': action,
            'confidence': confidence,
            'reasoning': entry.get('reasoning', ''),
        }
    return out


def collect(
    corpus_path: str,
    labels_dir: str,
    output_path: str,
    num_labellers: int = 5,
) -> Dict[str, Any]:
    """Aggregate per-labeller files into the consensus JSONL output.

    Returns a stats dict for reporting.
    """
    if not os.path.exists(corpus_path):
        raise FileNotFoundError(f"corpus not found: {corpus_path}")

    with open(corpus_path) as f:
        records = [json.loads(line) for line in f if line.strip()]
    print(f"[collect] loaded {len(records)} records from {corpus_path}")

    labeller_files = []
    import glob as _glob
    for n in range(1, num_labellers + 1):
        # Glob for any protocol version (e.g. labels_v3_2_labeller_1.json
        # OR labels_v3_3_labeller_1.json — generalised at 12.5E-C amendment).
        pattern = os.path.join(labels_dir, f"labels_v*_labeller_{n}.json")
        matches = sorted(_glob.glob(pattern))
        if not matches:
            print(f"[collect] WARNING: no labeller file matching {pattern}",
                  file=sys.stderr)
            labeller_files.append({})
        else:
            if len(matches) > 1:
                print(f"[collect] WARNING: multiple labeller files match "
                      f"{pattern}; using {matches[0]}", file=sys.stderr)
            path = matches[0]
            labeller_files.append(_load_labeller_file(path))
            print(f"[collect] loaded labeller {n}: "
                  f"{len(labeller_files[-1])} labels (from {os.path.basename(path)})")

    rows = []
    missing_per_labeller = [0] * num_labellers
    refusals_per_labeller = [0] * num_labellers
    refusals_total = 0

    for record in records:
        ref_id = compute_ref_id(record)
        labels: List[Dict[str, Any]] = []
        for n, labeller_map in enumerate(labeller_files, start=1):
            entry = labeller_map.get(ref_id)
            if entry is None:
                missing_per_labeller[n - 1] += 1
                continue
            if entry['action'] is None:
                refusals_per_labeller[n - 1] += 1
                refusals_total += 1
            labels.append({
                'labeller_id': n,
                'action': entry['action'],
                'confidence': entry['confidence'],
                'reasoning': entry['reasoning'],
            })

        votes = [lab['action'] for lab in labels]
        cons = consensus(votes)

        row = {
            'ref_id': ref_id,
            'pilot_hand_id': record.get('pilot_hand_id'),
            'labels': labels,
            **cons,
            'feat_dict': record.get('feat_dict', {}),
        }
        rows.append(row)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w') as f:
        for row in rows:
            f.write(json.dumps(row) + '\n')

    action_counter: Counter = Counter()
    for row in rows:
        action_counter[row['consensus_action']] += 1
    no_consensus = action_counter.get(None, 0)
    refusal_rate = refusals_total / (len(records) * num_labellers) if records else 0.0

    print(f"[collect] wrote {len(rows)} rows to {output_path}")
    print(f"[collect] consensus action distribution: {dict(action_counter)}")
    print(f"[collect] hands with no consensus (all 5 refused): {no_consensus}")
    print(f"[collect] missing per labeller: {missing_per_labeller}")
    print(f"[collect] refusals per labeller: {refusals_per_labeller}")
    print(f"[collect] global refusal rate: "
          f"{refusal_rate * 100:.2f}% ({refusals_total}/{len(records) * num_labellers})")
    if refusal_rate > 0.05:
        print(f"[collect] WARN: refusal rate above 5%% target", file=sys.stderr)

    return {
        'rows': len(rows),
        'consensus_distribution': dict(action_counter),
        'no_consensus': no_consensus,
        'missing_per_labeller': missing_per_labeller,
        'refusals_per_labeller': refusals_per_labeller,
        'refusal_rate': refusal_rate,
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description='Aggregate 5 per-labeller JSON files into consensus JSONL'
    )
    parser.add_argument('--corpus', required=True, help='Corpus JSONL path')
    parser.add_argument('--labels-dir', required=True,
                        help='Directory with labels_v*_labeller_<N>.json files (any protocol version)')
    parser.add_argument('--output', required=True, help='Output JSONL path')
    parser.add_argument('--num-labellers', type=int, default=5)

    args = parser.parse_args(argv)
    collect(
        corpus_path=args.corpus,
        labels_dir=args.labels_dir,
        output_path=args.output,
        num_labellers=args.num_labellers,
    )
    return 0


if __name__ == '__main__':
    sys.exit(main())
