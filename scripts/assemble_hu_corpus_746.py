"""Assemble 746-hand HU corpus from pilot_50_v2 + full_HU2_HU6.

Output: data/corpus_hu_746_2026-05-10.jsonl

Per Phase 1.5-D.4 dispatch §"Corpus assembly":
  - Inputs:
      - data/hu_corpus/pilot_50_v2/situations.jsonl + consensus.jsonl (50 rows)
      - data/hu_corpus/full_HU2_HU6/situations.jsonl + consensus.jsonl (696 rows)
  - Output single combined file with feat_dict (59 features) + consensus_action.

Each row: {spot_id, anchor_id, feat_dict, consensus_action, consensus_kind, confidence}.
"""
from __future__ import annotations

import json
import os
import sys
from typing import Dict

# Make river-rats-core importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'river-rats-core'))

from feature_extractor import FEATURE_COLUMNS, extract_all_features
from feature_keys import F


STREET_MAP = {'preflop': 'p', 'flop': 'f', 'turn': 't', 'river': 'r'}

# Confidence weights per consensus_kind. Mirrors v9_student's 1.0/0.8/0.6/0.4 schema.
CONFIDENCE_FROM_KIND = {
    '5-of-5': 1.0,
    '4-of-5': 0.8,
    '3-2-tier-up-agree': 0.6,
    '3-2-tier-up-disagree': 0.4,    # owner-arb adjudicated; lower confidence
    '2-2-1': 0.4,                   # owner-arb adjudicated; lower confidence
}


def _build_hand_dict(sit: Dict) -> Dict:
    """Construct hand dict for feature extraction from situations.jsonl row."""
    street_code = STREET_MAP.get(sit['street'].lower(), 'f')
    # Determine the active board (the latest street we've reached)
    if sit['street'] == 'river':
        board = sit.get('board_river') or ''
    elif sit['street'] == 'turn':
        board = sit.get('board_turn') or ''
    else:
        board = sit.get('board_flop') or ''
    villain_aggression = 1 if sit['facing_bet'] else 0
    return {
        'h': sit['hero_cards'],
        'b': board,
        'pos': sit['hero_pos'],
        'vp': sit['villain_pos'],
        'pot': sit['pot_bb'],
        'tc': sit['to_call_bb'],
        'st': street_code,
        'fb': int(sit['facing_bet']),
        'exp': 'C',
        F.META_NUM_OPPONENTS: 1,
        F.META_NUM_RAISES: 0,
        F.META_OPENER_POSITION: sit.get('opener'),
        F.META_BETTOR_POSITION: sit.get('bettor'),
        '_villain_aggression_count': villain_aggression,
        '_villain_checked_back': 0,
        '_villain_call_count': 0,
        '_num_callers_to_bet': 0,
        '_facing_raise': 0,
        '_action_history': [],
    }


def assemble(situations_paths, consensus_paths, output_path) -> int:
    """Merge situations + consensus by spot_id; extract features; write corpus."""
    # Load all situations
    situations: Dict[str, Dict] = {}
    for sp in situations_paths:
        with open(sp) as f:
            for line in f:
                rec = json.loads(line)
                situations[rec['spot_id']] = rec
    # Load all consensus
    consensus: Dict[str, Dict] = {}
    for cp in consensus_paths:
        with open(cp) as f:
            for line in f:
                rec = json.loads(line)
                consensus[rec['spot_id']] = rec

    # Sanity check
    sit_ids = set(situations.keys())
    cons_ids = set(consensus.keys())
    common = sit_ids & cons_ids
    print(f"situations={len(sit_ids)}, consensus={len(cons_ids)}, common={len(common)}")
    if sit_ids != cons_ids:
        only_sit = sit_ids - cons_ids
        only_cons = cons_ids - sit_ids
        print(f"WARNING: sit-only={len(only_sit)} (sample {list(only_sit)[:3]}); "
              f"cons-only={len(only_cons)} (sample {list(only_cons)[:3]})")

    # Extract features + write corpus
    out_count = 0
    skipped = []
    with open(output_path, 'w') as f:
        for spot_id in sorted(common):
            sit = situations[spot_id]
            cons = consensus[spot_id]
            consensus_action = cons.get('consensus_action')
            if consensus_action is None:
                skipped.append((spot_id, 'consensus_action is null'))
                continue
            consensus_kind = cons.get('consensus_kind', '5-of-5')
            confidence = CONFIDENCE_FROM_KIND.get(consensus_kind, 0.6)

            try:
                hand_dict = _build_hand_dict(sit)
                feat_dict = extract_all_features(hand_dict)
                # Validate: all 59 keys present
                missing = [k for k in FEATURE_COLUMNS if k not in feat_dict]
                if missing:
                    skipped.append((spot_id, f'feat_dict missing {len(missing)} keys: {missing[:3]}'))
                    continue
                # Filter feat_dict to ONLY the FEATURE_COLUMNS keys (drop helpers)
                clean_feat = {k: float(feat_dict[k]) for k in FEATURE_COLUMNS}
                # Assert all numeric
                for k, v in clean_feat.items():
                    if not isinstance(v, (int, float)):
                        raise ValueError(f"non-numeric feature {k}={v!r}")
            except Exception as e:
                skipped.append((spot_id, f'feature extraction error: {e}'))
                continue

            row_out = {
                'spot_id': spot_id,
                'anchor_id': sit.get('anchor_id'),
                'feat_dict': clean_feat,
                'consensus_action': consensus_action,
                'consensus_kind': consensus_kind,
                'confidence': confidence,
                'owner_arb': cons.get('owner_arb', False),
            }
            f.write(json.dumps(row_out) + '\n')
            out_count += 1

    print(f"Wrote {out_count} rows to {output_path}")
    if skipped:
        print(f"Skipped {len(skipped)}:")
        for sid, reason in skipped[:10]:
            print(f"  {sid}: {reason}")
        if len(skipped) > 10:
            print(f"  ... + {len(skipped) - 10} more")
    return out_count


def main():
    # Project root
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    print(f"cwd: {os.getcwd()}")

    situations_paths = [
        'data/hu_corpus/pilot_50_v2/situations.jsonl',
        'data/hu_corpus/full_HU2_HU6/situations.jsonl',
    ]
    consensus_paths = [
        'data/hu_corpus/pilot_50_v2/consensus.jsonl',
        'data/hu_corpus/full_HU2_HU6/consensus.jsonl',
    ]
    output_path = 'data/corpus_hu_746_2026-05-10.jsonl'

    n = assemble(situations_paths, consensus_paths, output_path)
    if n != 746:
        print(f"WARNING: expected 746 rows, got {n}")


if __name__ == '__main__':
    main()
