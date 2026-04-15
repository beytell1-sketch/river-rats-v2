#!/usr/bin/env python3
"""LLM-based labelling agent for 3-way postflop situations.

Provides the infrastructure to label situations via Claude Code
subagents. Each hand is labelled independently.

Two modes:
1. prepare_batches() — splits situations into batch files ready
   for parallel agent dispatch
2. collect_results() — parses agent output and writes labelled JSONL

Usage:
    # Step 1: Prepare
    python3 labelling_agent.py prepare --input 3way_situations.jsonl --batch-size 10

    # Step 2: Dispatch agents (done in Claude Code conversation)

    # Step 3: Collect
    python3 labelling_agent.py collect --output 3way_labelled.jsonl
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))

from calibration_exam import (
    load_agent_context, reference_hand_to_situation,
    format_situation_for_agent,
)
from gto_model import FEATURE_COLUMNS


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'training-data')
BATCH_DIR = os.path.join(os.path.dirname(__file__), '..', 'review', 'label_batches')

# Known top-level metadata keys for flat BP-series records (no nested feat_dict).
_FLAT_METADATA_KEYS = {
    'situation_id', 'hero_cards', 'board_cards', 'hero_position',
    'villain_positions', 'street', 'pot', 'to_call', 'facing_bet',
    'num_opponents', 'action_string', 'description',
}


def _normalise_flat_situation(sit: dict) -> dict:
    """Convert a flat factory_batch5 record into the nested format expected
    by prepare_batches() and format_situation_for_agent().

    Flat records (BP-series) store all features and metadata at the same
    level. Nested records (d-series) have a 'feat_dict' sub-dict for
    features and metadata at the top level.

    This adapter splits known metadata keys to the top level and puts all
    remaining keys into 'feat_dict', ensuring villain_positions (the full
    list) is used rather than the single-valued _villain_pos_raw field.
    """
    nested = {}
    feat_dict = {}
    for key, value in sit.items():
        if key in _FLAT_METADATA_KEYS:
            nested[key] = value
        else:
            feat_dict[key] = value
    nested['feat_dict'] = feat_dict
    return nested


def prepare_batches(input_path: str, batch_size: int = 10):
    """Split situations JSONL into batch files for agent dispatch.

    Each batch file contains the situation text for batch_size hands.
    The agent context (prompt + knowledge base) is saved separately.
    """
    # Load and validate context
    context = load_agent_context()
    print(f"Agent context loaded ({len(context)} chars)")

    # Load situations
    situations = []
    with open(input_path) as f:
        for line in f:
            situations.append(json.loads(line))
    print(f"Loaded {len(situations)} situations")

    # Save context
    os.makedirs(BATCH_DIR, exist_ok=True)
    context_path = os.path.join(BATCH_DIR, 'agent_context.txt')
    with open(context_path, 'w') as f:
        f.write(context)

    # Split into batches
    batches = []
    for i in range(0, len(situations), batch_size):
        batch = situations[i:i + batch_size]
        batch_id = i // batch_size + 1
        batch_path = os.path.join(BATCH_DIR, f'batch_{batch_id:02d}.txt')

        with open(batch_path, 'w') as f:
            for sit in batch:
                # Normalise flat BP records to nested format if feat_dict is absent.
                if 'feat_dict' not in sit:
                    sit = _normalise_flat_situation(sit)
                f.write(f"--- HAND: {sit['situation_id']} ---\n")
                # Format key fields for the agent
                fd = sit.get('feat_dict', {})
                lines = [
                    f"Situation ID: {sit['situation_id']}",
                    f"Hero cards: {sit.get('hero_cards', '')}",
                    f"Board: {sit.get('board', '')}",
                    f"Street: {sit.get('street', '')}",
                    f"Hero position: {sit.get('hero_position', '')}",
                    f"Villain positions: {', '.join(sit.get('villain_positions', []))}",
                    f"Num opponents: {sit.get('num_opponents', 2)}",
                    f"Pot: {sit.get('pot', 0)}",
                    f"To call: {sit.get('to_call', 0)}",
                    f"Facing bet: {sit.get('facing_bet', False)}",
                    f"Action history: {sit.get('action_history', 'N/A')}",
                    "",
                    "Key features:",
                ]
                # Add all feature values
                for feat in ['raw_equity', 'equity_vs_range', 'pot_odds',
                             'is_ip', 'hand_category', 'is_made_hand',
                             'is_strong_made', 'is_monster', 'draw_outs',
                             'has_flush_draw', 'has_straight_draw',
                             'danger_score', 'spr',
                             'villain_top_pair_plus_pct', 'villain_air_pct',
                             'villain_range_capped', 'board_favour',
                             'num_callers_to_bet', 'facing_raise',
                             'villain_aggression_count', 'villain_checked_back',
                             'better_hand_pct', 'worse_hand_pct']:
                    val = fd.get(feat, 0)
                    if isinstance(val, float):
                        lines.append(f"  {feat}: {val:.4f}")
                    else:
                        lines.append(f"  {feat}: {val}")

                f.write('\n'.join(lines) + '\n\n')

        # Save batch metadata
        batch_meta = {
            'batch_id': batch_id,
            'situation_ids': [s['situation_id'] for s in batch],
            'count': len(batch),
        }
        batches.append(batch_meta)
        print(f"  Batch {batch_id}: {len(batch)} hands → {batch_path}")

    # Save master index
    index_path = os.path.join(BATCH_DIR, 'batch_index.json')
    with open(index_path, 'w') as f:
        json.dump({
            'total_situations': len(situations),
            'batch_size': batch_size,
            'num_batches': len(batches),
            'batches': batches,
        }, f, indent=2)

    print(f"\n  {len(batches)} batches prepared in {BATCH_DIR}")
    print(f"  Agent context: {context_path}")
    print(f"  Index: {index_path}")
    print(f"\n  Dispatch each batch as a subagent with the context file.")
    return batches


def parse_agent_output(text: str) -> list:
    """Extract JSON objects from agent output text.

    Handles JSON in code blocks or bare JSON objects.
    Returns a list of parsed dicts.
    """
    results = []

    # Try to find JSON blocks (```json ... ```)
    json_blocks = re.findall(r'```json\s*\n(.*?)```', text, re.DOTALL)
    if json_blocks:
        for block in json_blocks:
            try:
                results.append(json.loads(block.strip()))
            except json.JSONDecodeError:
                pass
        if results:
            return results

    # Try bare JSON objects
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start is not None:
                try:
                    obj = json.loads(text[start:i + 1])
                    results.append(obj)
                except json.JSONDecodeError:
                    pass
                start = None

    return results


def collect_results(situations_path: str, output_path: str):
    """Collect agent outputs from batch result files and merge with situations.

    Expects result files at: BATCH_DIR/batch_XX_result.txt
    """
    # Load original situations for feat_dict
    situations_by_id = {}
    with open(situations_path) as f:
        for line in f:
            sit = json.loads(line)
            situations_by_id[sit['situation_id']] = sit

    # Load batch index
    index_path = os.path.join(BATCH_DIR, 'batch_index.json')
    with open(index_path) as f:
        index = json.load(f)

    # Collect results
    labelled = []
    missing = []
    parse_errors = []

    for batch_meta in index['batches']:
        batch_id = batch_meta['batch_id']
        result_path = os.path.join(BATCH_DIR, f'batch_{batch_id:02d}_result.txt')

        if not os.path.exists(result_path):
            missing.extend(batch_meta['situation_ids'])
            continue

        with open(result_path) as f:
            text = f.read()

        labels = parse_agent_output(text)

        # Match labels to situation IDs
        for label in labels:
            sit_id = label.get('situation_id', '')
            if sit_id in situations_by_id:
                # Merge label with original situation
                original = situations_by_id[sit_id]
                merged = {**original}
                merged['expert_action'] = label.get('action', '').upper()
                merged['expert_confidence'] = label.get('confidence', 'MEDIUM').upper()
                merged['expert_reasoning'] = label.get('reasoning', '')
                merged['difficulty'] = label.get('difficulty', 2)
                merged['key_factors'] = label.get('key_factors', [])
                merged['factor_conflicts'] = label.get('factor_conflicts', '')
                merged['alternatives_considered'] = label.get('alternatives_considered', [])
                labelled.append(merged)
            else:
                parse_errors.append(f"Unknown situation_id: {sit_id}")

    # Write output
    with open(output_path, 'w') as f:
        for entry in labelled:
            f.write(json.dumps(entry) + '\n')

    # Report
    print(f"\nCollected {len(labelled)} labels")
    if missing:
        print(f"  Missing batch results for: {missing}")
    if parse_errors:
        print(f"  Parse errors: {parse_errors}")

    # Stats
    action_counts = {}
    conf_counts = {}
    for entry in labelled:
        a = entry.get('expert_action', 'UNKNOWN')
        c = entry.get('expert_confidence', 'UNKNOWN')
        action_counts[a] = action_counts.get(a, 0) + 1
        conf_counts[c] = conf_counts.get(c, 0) + 1

    print(f"  Actions: {action_counts}")
    print(f"  Confidence: {conf_counts}")

    low_count = conf_counts.get('LOW', 0)
    total = len(labelled)
    if total > 0 and low_count / total > 0.15:
        print(f"\n  WARNING: LOW confidence is {100*low_count/total:.1f}% (> 15% target)")

    print(f"\n  Written to: {output_path}")
    return labelled


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='3-way labelling agent')
    sub = parser.add_subparsers(dest='command')

    prep = sub.add_parser('prepare', help='Prepare batch files for agent dispatch')
    prep.add_argument('--input', type=str,
                      default=os.path.join(DATA_DIR, '3way_situations.jsonl'))
    prep.add_argument('--batch-size', type=int, default=10)

    coll = sub.add_parser('collect', help='Collect agent results into labelled JSONL')
    coll.add_argument('--situations', type=str,
                      default=os.path.join(DATA_DIR, '3way_situations.jsonl'))
    coll.add_argument('--output', type=str,
                      default=os.path.join(DATA_DIR, '3way_labelled.jsonl'))

    args = parser.parse_args()

    if args.command == 'prepare':
        prepare_batches(args.input, args.batch_size)
    elif args.command == 'collect':
        collect_results(args.situations, args.output)
    else:
        parser.print_help()
