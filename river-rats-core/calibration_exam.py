#!/usr/bin/env python3
"""Calibration exam for the 3-way GTO labelling agent.

Feeds the 24 three-way reference hands to the labelling agent,
compares labels to known expert actions, and reports accuracy.

Gate: 20/24 (83%) overall + ALL 3 GTO-reversal hands correct.
If gate fails, the agent must not label training data.

Usage:
    python3 calibration_exam.py
    python3 calibration_exam.py --prompt prompts/gto_labeller_v1.md
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import re

from reference_evaluator import (
    parse_reference_hands, ReferenceHand, _ACTION_HISTORY,
    STREET_MAP,
)
from feature_extractor import extract_all_features
from feature_keys import F
from gto_model import FEATURE_COLUMNS


# The 3 GTO-reversal hands that MUST be correct
GTO_REVERSAL_HANDS = {'MW-30', 'MW-33', 'MW-50'}

# Paths
_BASE = os.path.dirname(__file__)
_DESIGNS = os.path.join(_BASE, '..', 'design', 'multiway_reference_set',
                        'BATCH2_8_HAND_DESIGNS.md')
_ANALYSIS = os.path.join(_BASE, '..', 'design', 'multiway_reference_set',
                         'BATCH2_8_RANGE_ANALYSIS.md')
_PROMPT = os.path.join(_BASE, '..', 'prompts', 'gto_labeller_v1.md')
_KNOWLEDGE = os.path.join(_BASE, '..', 'knowledge', 'three_way_gto.md')


def _parse_action_history_prose() -> dict:
    """Extract action history prose from hand designs by ref_id."""
    with open(_DESIGNS) as f:
        content = f.read()

    # Split by hand headers, then find Action history in each block
    result = {}
    sections = re.split(r'### (MW-\d+):', content)
    for i in range(1, len(sections), 2):
        ref_id = sections[i]
        block = sections[i + 1]
        m = re.search(r'\*\*Action history:\*\*\s*(.+)', block)
        if m:
            result[ref_id] = m.group(1).strip()
    return result


def load_3way_reference_hands() -> list:
    """Load and filter to the 24 three-way reference hands."""
    all_hands = parse_reference_hands(_DESIGNS, _ANALYSIS)
    three_way = [h for h in all_hands if h.num_opponents == 2]
    return three_way


_ACTION_PROSE = None  # lazy-loaded


def _get_action_prose() -> dict:
    global _ACTION_PROSE
    if _ACTION_PROSE is None:
        _ACTION_PROSE = _parse_action_history_prose()
    return _ACTION_PROSE


def reference_hand_to_situation(hand: ReferenceHand) -> dict:
    """Convert a ReferenceHand to the situation format the labelling agent expects."""
    street_code = STREET_MAP.get(hand.street.capitalize(), 'f')

    hand_dict = {
        'h': hand.hero_cards,
        'b': hand.board,
        'pos': hand.hero_position,
        'vp': hand.villain_position,
        'pot': hand.pot,
        'tc': hand.to_call,
        'st': street_code,
        'fb': int(hand.facing_bet),
        'exp': 'C',
        F.META_NUM_OPPONENTS: hand.num_opponents,
        F.META_NUM_RAISES: 0,
        F.META_OPENER_POSITION: hand.opener_position or None,
        F.META_BETTOR_POSITION: hand.bettor_position,
        '_villain_aggression_count': hand.villain_aggression_count,
        '_villain_checked_back': hand.villain_checked_back,
        '_villain_call_count': hand.villain_call_count,
        '_num_callers_to_bet': hand.num_callers_to_bet,
        '_facing_raise': hand.facing_raise,
    }

    feat_dict = extract_all_features(hand_dict)

    # Build the situation dict the agent receives
    action_prose = _get_action_prose().get(hand.ref_id, '')
    situation = {
        'situation_id': hand.ref_id,
        'hero_cards': hand.hero_cards,
        'board': hand.board,
        'street': hand.street,
        'hero_position': hand.hero_position,
        'villain_positions': [hand.villain_position],
        'pot': hand.pot,
        'to_call': hand.to_call,
        'facing_bet': hand.facing_bet,
        'num_opponents': hand.num_opponents,
        'equity': hand.equity,
        'action_history': action_prose,
        'feat_dict': {k: (round(float(v), 6) if isinstance(v, float)
                          else int(v) if isinstance(v, (int, bool))
                          else str(v))
                      for k, v in feat_dict.items()
                      if k in set(FEATURE_COLUMNS)},
    }
    return situation


def format_situation_for_agent(situation: dict) -> str:
    """Format one situation as the text block the agent receives."""
    fd = situation['feat_dict']
    lines = [
        f"Situation ID: {situation['situation_id']}",
        f"Hero cards: {situation['hero_cards']}",
        f"Board: {situation['board']}",
        f"Street: {situation['street']}",
        f"Hero position: {situation['hero_position']}",
        f"Villain positions: {', '.join(situation['villain_positions'])}",
        f"Num opponents: {situation['num_opponents']}",
        f"Pot: {situation['pot']}",
        f"To call: {situation['to_call']}",
        f"Facing bet: {situation['facing_bet']}",
        f"Action history: {situation.get('action_history', 'N/A')}",
        f"",
        f"Key features:",
        f"  raw_equity: {fd.get('raw_equity', 0):.4f}",
        f"  equity_vs_range: {fd.get('equity_vs_range', 0):.4f}",
        f"  pot_odds: {fd.get('pot_odds', 0):.4f}",
        f"  is_ip: {fd.get('is_ip', 0)}",
        f"  hand_category: {fd.get('hand_category', 0)}",
        f"  is_made_hand: {fd.get('is_made_hand', 0)}",
        f"  is_strong_made: {fd.get('is_strong_made', 0)}",
        f"  is_monster: {fd.get('is_monster', 0)}",
        f"  draw_outs: {fd.get('draw_outs', 0)}",
        f"  has_flush_draw: {fd.get('has_flush_draw', 0)}",
        f"  has_straight_draw: {fd.get('has_straight_draw', 0)}",
        f"  danger_score: {fd.get('danger_score', 0):.4f}",
        f"  spr: {fd.get('spr', 0):.2f}",
        f"  villain_top_pair_plus_pct: {fd.get('villain_top_pair_plus_pct', 0):.4f}",
        f"  villain_air_pct: {fd.get('villain_air_pct', 0):.4f}",
        f"  villain_range_capped: {fd.get('villain_range_capped', 0)}",
        f"  board_favour: {fd.get('board_favour', 0):.4f}",
        f"  num_callers_to_bet: {fd.get('num_callers_to_bet', 0)}",
        f"  facing_raise: {fd.get('facing_raise', 0)}",
        f"  villain_aggression_count: {fd.get('villain_aggression_count', 0)}",
        f"  villain_checked_back: {fd.get('villain_checked_back', 0)}",
        f"  better_hand_pct: {fd.get('better_hand_pct', 0):.4f}",
        f"  worse_hand_pct: {fd.get('worse_hand_pct', 0):.4f}",
    ]
    return '\n'.join(lines)


def load_agent_context(prompt_path: str = None, knowledge_path: str = None) -> str:
    """Load and concatenate prompt + knowledge base."""
    prompt_path = prompt_path or _PROMPT
    knowledge_path = knowledge_path or _KNOWLEDGE

    with open(prompt_path) as f:
        prompt = f.read()
    with open(knowledge_path) as f:
        knowledge = f.read()

    # Fail-fast assertions
    assert "DO NOT" in prompt, "Prompt file missing DO NOT rules section"
    assert "Worked Examples" in knowledge, \
        "Knowledge base missing Worked Examples section — agent will be blind to case law"

    return prompt + "\n\n---\n\n" + knowledge


def score_results(results: list) -> dict:
    """Score calibration results and check gate criteria."""
    total = len(results)
    correct = sum(1 for r in results if r['correct'])
    accuracy = correct / total if total > 0 else 0.0

    # GTO-reversal check
    reversal_results = [r for r in results if r['ref_id'] in GTO_REVERSAL_HANDS]
    reversal_correct = sum(1 for r in reversal_results if r['correct'])
    reversal_total = len(reversal_results)

    # By confidence
    by_conf = {}
    for r in results:
        conf = r.get('agent_confidence', 'UNKNOWN')
        if conf not in by_conf:
            by_conf[conf] = {'correct': 0, 'total': 0}
        by_conf[conf]['total'] += 1
        if r['correct']:
            by_conf[conf]['correct'] += 1

    # Gate check
    gate_overall = correct >= 20  # 20/24
    gate_reversals = reversal_correct == reversal_total  # all 3
    gate_passed = gate_overall and gate_reversals

    return {
        'total': total,
        'correct': correct,
        'accuracy': accuracy,
        'gate_passed': gate_passed,
        'gate_overall': f"{correct}/24 >= 20 → {'PASS' if gate_overall else 'FAIL'}",
        'gate_reversals': f"{reversal_correct}/{reversal_total} → {'PASS' if gate_reversals else 'FAIL'}",
        'reversal_details': reversal_results,
        'by_confidence': by_conf,
        'failures': [r for r in results if not r['correct']],
    }


def print_report(scores: dict):
    """Print a human-readable calibration report."""
    print("=" * 60)
    print("CALIBRATION EXAM — 3-Way Labelling Agent")
    print("=" * 60)
    print(f"\n  Overall: {scores['correct']}/{scores['total']} "
          f"({scores['accuracy']:.1%})")
    print(f"  Gate (20/24): {scores['gate_overall']}")
    print(f"  Gate (reversals): {scores['gate_reversals']}")
    print(f"\n  GATE: {'PASSED' if scores['gate_passed'] else 'FAILED'}")

    if scores['by_confidence']:
        print(f"\n  By agent confidence:")
        for conf in ['HIGH', 'MEDIUM', 'LOW']:
            if conf in scores['by_confidence']:
                c = scores['by_confidence'][conf]
                pct = c['correct'] / c['total'] if c['total'] > 0 else 0
                print(f"    {conf}: {c['correct']}/{c['total']} ({pct:.0%})")

    if scores['failures']:
        print(f"\n  Failures ({len(scores['failures'])}):")
        for f in scores['failures']:
            rev = " [REVERSAL]" if f['ref_id'] in GTO_REVERSAL_HANDS else ""
            print(f"    {f['ref_id']}: expert={f['expert_action']}, "
                  f"agent={f['agent_action']}{rev}")
            if f.get('agent_reasoning'):
                print(f"      Reasoning: {f['agent_reasoning'][:100]}...")

    print("=" * 60)


def run_calibration(label_fn, prompt_path: str = None,
                    knowledge_path: str = None) -> dict:
    """Run the full calibration exam.

    Args:
        label_fn: Callable that takes (situation_text, agent_context) and
                  returns a dict with at least 'action' key. This is the
                  interface to the actual LLM agent.
        prompt_path: Path to prompt file.
        knowledge_path: Path to knowledge base.

    Returns:
        Score dict from score_results().
    """
    # Load agent context
    agent_context = load_agent_context(prompt_path, knowledge_path)

    # Load reference hands
    hands = load_3way_reference_hands()
    print(f"Loaded {len(hands)} three-way reference hands")

    # Run exam
    results = []
    for hand in hands:
        situation = reference_hand_to_situation(hand)
        situation_text = format_situation_for_agent(situation)

        # Call the labelling function
        label = label_fn(situation_text, agent_context)

        agent_action = label.get('action', '').upper()
        expert_action = hand.expert_action.upper()
        correct = agent_action == expert_action

        results.append({
            'ref_id': hand.ref_id,
            'expert_action': expert_action,
            'agent_action': agent_action,
            'agent_confidence': label.get('confidence', 'UNKNOWN'),
            'agent_reasoning': label.get('reasoning', ''),
            'correct': correct,
            'equity': hand.equity,
        })

    # Score
    scores = score_results(results)
    print_report(scores)

    return scores


# ── Standalone test with a dummy labeller ────────────────────────

def _dummy_labeller(situation_text: str, agent_context: str) -> dict:
    """Placeholder — always returns CHECK. For testing the exam harness."""
    return {
        'action': 'CHECK',
        'confidence': 'LOW',
        'reasoning': 'Dummy labeller — always checks.',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run calibration exam')
    parser.add_argument('--prompt', type=str, default=_PROMPT)
    parser.add_argument('--knowledge', type=str, default=_KNOWLEDGE)
    parser.add_argument('--dummy', action='store_true',
                        help='Run with dummy labeller (tests the harness)')
    args = parser.parse_args()

    if args.dummy:
        print("Running with DUMMY labeller (tests harness only)\n")
        run_calibration(_dummy_labeller, args.prompt, args.knowledge)
    else:
        print("No labeller connected. Use --dummy to test harness,")
        print("or import run_calibration() and pass your label_fn.")
