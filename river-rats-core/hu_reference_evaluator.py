"""HU reference evaluator — Phase 1.5-D.4 PR 0.

Evaluates a trained model artifact against the 30-hand HU reference set
(`design/hu_reference_set/hu_30_hand_reference.jsonl`). Returns aggregate
correct/30 + per-hand predicted-vs-expected results.

Provenance
----------
Built per Phase 1.5-D.4 AMENDMENT (Option B; PR #366) at master `b49f73a`.
Eval infrastructure prerequisite for 1.5-D.4 smoke + 5-seed full ship gate
(≥28/30 per design memo §4.6).

Compatible with both v8-HU-38 and vNext-HU-59 model artifacts via
`gto_model.GtoOracle` auto-detect feature truncation.

Usage (CLI):
    python3 river-rats-core/hu_reference_evaluator.py \
        --model models/gto_model_v8_hu.json \
        --reference design/hu_reference_set/hu_30_hand_reference.jsonl \
        --output data/hu_reference_v8_hu_baseline_2026-05-10.jsonl

Usage (import):
    from hu_reference_evaluator import parse_hu_reference_hands, evaluate_hu_reference
    hands = parse_hu_reference_hands('design/hu_reference_set/hu_30_hand_reference.jsonl')
    result = evaluate_hu_reference(hands, 'models/gto_model_vNext_hu_59feat.json')
    print(f"Score: {result['correct']}/{result['total']}")
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# Make river-rats-core importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feature_extractor import FEATURE_COLUMNS, extract_all_features
from feature_keys import F
from gto_model import GtoOracle


STREET_MAP = {
    'preflop': 'p', 'flop': 'f', 'turn': 't', 'river': 'r',
}


@dataclass
class HuReferenceHand:
    spot_id: str
    axis: str
    marker: str
    hero_cards: str
    board_flop: Optional[str]
    board_turn: Optional[str]
    board_river: Optional[str]
    street: str
    hero_pos: str
    villain_pos: str
    pot_bb: float
    facing_bet: bool
    to_call_bb: float
    effective_stack_bb: float
    opener: Optional[str]
    bettor: Optional[str]
    composition: str
    axis_label: str
    action_summary: str
    expected_action: str
    expected_source: str

    @property
    def board(self) -> str:
        if self.street == 'river':
            return self.board_river or ''
        if self.street == 'turn':
            return self.board_turn or ''
        return self.board_flop or ''


def parse_hu_reference_hands(path: str) -> List[HuReferenceHand]:
    """Load the 30-hand HU reference set from JSONL."""
    hands: List[HuReferenceHand] = []
    with open(path) as f:
        for line in f:
            rec = json.loads(line)
            hands.append(HuReferenceHand(
                spot_id=rec['spot_id'],
                axis=rec['axis'],
                marker=rec['marker'],
                hero_cards=rec['hero_cards'],
                board_flop=rec.get('board_flop'),
                board_turn=rec.get('board_turn'),
                board_river=rec.get('board_river'),
                street=rec['street'],
                hero_pos=rec['hero_pos'],
                villain_pos=rec['villain_pos'],
                pot_bb=rec['pot_bb'],
                facing_bet=rec['facing_bet'],
                to_call_bb=rec['to_call_bb'],
                effective_stack_bb=rec['effective_stack_bb'],
                opener=rec.get('opener'),
                bettor=rec.get('bettor'),
                composition=rec['composition'],
                axis_label=rec['axis_label'],
                action_summary=rec['action_summary'],
                expected_action=rec['expected_action'],
                expected_source=rec.get('expected_source', ''),
            ))
    return hands


def _build_hand_dict(hand: HuReferenceHand) -> Dict:
    """Construct the hand dict for feature extraction."""
    street_code = STREET_MAP.get(hand.street.lower(), 'f')
    villain_aggression = 1 if hand.facing_bet else 0
    return {
        'h': hand.hero_cards,
        'b': hand.board,
        'pos': hand.hero_pos,
        'vp': hand.villain_pos,
        'pot': hand.pot_bb,
        'tc': hand.to_call_bb,
        'st': street_code,
        'fb': int(hand.facing_bet),
        'exp': 'C',
        F.META_NUM_OPPONENTS: 1,
        F.META_NUM_RAISES: 0,
        F.META_OPENER_POSITION: hand.opener,
        F.META_BETTOR_POSITION: hand.bettor,
        '_villain_aggression_count': villain_aggression,
        '_villain_checked_back': 0,
        '_villain_call_count': 0,
        '_num_callers_to_bet': 0,
        '_facing_raise': 0,
        '_action_history': [],
    }


def _normalize_action(action: str, facing_bet: bool) -> str:
    """Collapse v8-style FOLD/RAISE → CHECK/BET when not facing a bet.

    Matches `reference_evaluator._evaluate_one_hand` normalization rule:
    older v8 models output FOLD/RAISE for not-facing-bet spots where the
    expert vocabulary uses CHECK/BET.
    """
    a = action.upper()
    if not facing_bet:
        if a == 'FOLD':
            return 'CHECK'
        if a == 'RAISE':
            return 'BET'
    return a


def evaluate_hu_reference(hands: List[HuReferenceHand], model_path: str) -> Dict:
    """Score a model against the HU reference hands.

    Returns:
        {
          'model_path': str,
          'total': int,
          'correct': int,
          'accuracy': float,
          'per_hand': [
            {'spot_id', 'expected', 'predicted', 'predicted_normalized', 'correct': bool, ...}
          ],
        }
    """
    oracle = GtoOracle(model_path)
    per_hand = []
    correct_count = 0

    for hand in hands:
        hand_dict = _build_hand_dict(hand)
        feat_dict = extract_all_features(hand_dict)
        # Use feature_extractor.FEATURE_COLUMNS (59 features); GtoOracle truncates for v8.
        import numpy as np
        try:
            features = np.array([float(feat_dict[k]) for k in FEATURE_COLUMNS],
                                dtype=np.float32).reshape(1, -1)
        except KeyError as e:
            raise RuntimeError(
                f"Feature extraction missing key {e} for hand {hand.spot_id}; "
                f"feat_dict keys: {list(feat_dict.keys())[:10]}..."
            )
        pred = oracle.predict(features.flatten())
        predicted_raw = pred.action.upper()
        predicted = _normalize_action(predicted_raw, hand.facing_bet)
        expected = _normalize_action(hand.expected_action, hand.facing_bet)
        is_correct = (predicted == expected)
        if is_correct:
            correct_count += 1
        per_hand.append({
            'spot_id': hand.spot_id,
            'axis': hand.axis,
            'marker': hand.marker,
            'street': hand.street,
            'expected': expected,
            'expected_raw': hand.expected_action,
            'expected_source': hand.expected_source,
            'predicted': predicted,
            'predicted_raw': predicted_raw,
            'confidence': float(pred.confidence),
            'correct': is_correct,
        })

    return {
        'model_path': model_path,
        'model_n_features': oracle._n_features,
        'total': len(hands),
        'correct': correct_count,
        'accuracy': correct_count / max(1, len(hands)),
        'per_hand': per_hand,
    }


def _format_report(result: Dict) -> str:
    """Human-readable evaluation summary."""
    lines = []
    lines.append(f"Model: {result['model_path']} (n_features={result['model_n_features']})")
    lines.append(f"Score: {result['correct']}/{result['total']} ({result['accuracy']*100:.1f}%)")
    lines.append("")
    # Per-axis breakdown
    from collections import defaultdict
    axis_correct = defaultdict(lambda: [0, 0])
    for h in result['per_hand']:
        axis_correct[h['axis']][1] += 1
        if h['correct']:
            axis_correct[h['axis']][0] += 1
    lines.append("Per-axis:")
    for axis in sorted(axis_correct.keys()):
        c, t = axis_correct[axis]
        lines.append(f"  {axis}: {c}/{t} ({c/max(1,t)*100:.0f}%)")
    lines.append("")
    lines.append("Per-hand misses:")
    for h in result['per_hand']:
        if not h['correct']:
            lines.append(f"  {h['spot_id']} [{h['marker']}] {h['street']}: "
                         f"expected={h['expected']} predicted={h['predicted']} "
                         f"(raw={h['predicted_raw']} conf={h['confidence']:.2f})")
    return '\n'.join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description='Evaluate model against 30-hand HU reference set.')
    p.add_argument('--model', required=True, help='Model JSON path')
    p.add_argument('--reference', default='design/hu_reference_set/hu_30_hand_reference.jsonl',
                   help='30-hand reference JSONL path')
    p.add_argument('--output', help='Optional per-hand JSONL output path')
    args = p.parse_args(argv)

    hands = parse_hu_reference_hands(args.reference)
    print(f"Loaded {len(hands)} reference hands")
    result = evaluate_hu_reference(hands, args.model)
    print(_format_report(result))

    if args.output:
        with open(args.output, 'w') as f:
            for h in result['per_hand']:
                f.write(json.dumps(h) + '\n')
        print(f"\nWrote per-hand results to {args.output}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
