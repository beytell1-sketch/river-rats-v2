#!/usr/bin/env python3
"""Calibration exam for the 3-way GTO labelling agent — v2.3.

Feeds the 28 three-way reference hands (24 MW + 4 new hard anchors) to
the labelling agent, compares labels to known expert actions, and reports
accuracy. Optionally extended with Group-D reversal hands from the
diagnostic test set.

Gate (v2.3, per review/comms/PLAN_V23_SCOPE_2026-04-15.md §5 and
review/comms/V23_HAND_GENERATION_PLAN_2026-04-16.md §3.1):
    - 23/28 standard-exam threshold (up from 20/24) AND
    - 100% on reversal hands (any single reversal failure = FAIL).

Reversal set (100%-must-pass):
    - MW-30, MW-33, MW-50 (original reversal anchors)
    - d2410_CO_turn, d3178_CO_river (predicate-matching new anchors)
    - Any hand registered in GROUP_D_REVERSAL_HANDS (diagnostic set)

Standard new anchors (count toward 23/28 but not 100%-must-pass):
    - d8886_BB_flop, d8963_HJ_turn (mixed-zone spots)

If gate fails, the agent must not label training data.

Usage:
    python3 calibration_exam.py
    python3 calibration_exam.py --prompt prompts/gto_labeller_v3.md
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


# ── v2.3 exam structure ───────────────────────────────────────────

# Standard exam size: 24 existing MW reference hands + 4 new hard anchors.
# Group-D reversal hands, when registered, EXTEND the total but do NOT
# change STANDARD_PASS_THRESHOLD — reversals are enforced via the 100%
# rule, not the 23/28 rule.
STANDARD_EXAM_SIZE = 28
STANDARD_PASS_THRESHOLD = 23  # v2.3 (was 20 in v2.2)


# The 4 new hard-anchor calibration candidates (per Scope §5 / Build
# Plan §3.1). Each is sourced from the canonical labelled JSONL —
# never hardcoded from memory.
_NEW_HARD_ANCHOR_IDS = (
    'd8886_BB_flop',    # mixed-zone (solver 50/50, our combo bets)
    'd2410_CO_turn',    # predicate-matching (villain_checked_back=1)
    'd8963_HJ_turn',    # mixed-zone (solver 50/50, our combo bets)
    'd3178_CO_river',   # predicate-matching / trap-lean (AA on paired river)
)


# Group-D calibration reversals (from PLAN_V23_DIAGNOSTIC_TEST_SET §2.D).
# d3688_BB_flop is the one confirmed reversal at time of writing
# (v2.2 BET, expert CHECK on KT4 flush board with second villain).
# Additional Group-D hands are extended into this registry as the
# diagnostic set is finalized. Hands registered here are AUTOMATICALLY
# ingested into GTO_REVERSAL_HANDS and become 100%-must-pass.
GROUP_D_REVERSAL_HANDS = {
    'd3688_BB_flop',
    'd4312_CO_turn',    # Owner pick 2026-04-16: solver-confirmed CHECK (Source B gold-standard)
    'd9556_BB_flop',    # Owner pick 2026-04-16: Pass 2 solver-confirmed CHECK (Source B)
    'd2074_BTN_turn',   # Owner pick 2026-04-16: near-bias CHECK label (Source A)
    'd5466_CO_flop',    # Owner pick 2026-04-16: near-bias CHECK label (Source A)
}


# The predicate-matching new anchors are reversals in the Group-D sense
# (villain_checked_back=1, capped villain range, CHECK→BET override
# required per Stream B.2 bias analysis).
_PREDICATE_REVERSAL_ANCHORS = {
    'd2410_CO_turn',
    'd3178_CO_river',
}


# The 100%-must-pass reversal set = original MW reversals + predicate
# new anchors + registered Group-D hands.
GTO_REVERSAL_HANDS = (
    {'MW-30', 'MW-33', 'MW-50'}
    | _PREDICATE_REVERSAL_ANCHORS
    | GROUP_D_REVERSAL_HANDS
)


# Paths
_BASE = os.path.dirname(__file__)
_DESIGNS = os.path.join(_BASE, '..', 'design', 'multiway_reference_set',
                        'BATCH2_8_HAND_DESIGNS.md')
_ANALYSIS = os.path.join(_BASE, '..', 'design', 'multiway_reference_set',
                         'BATCH2_8_RANGE_ANALYSIS.md')
_PROMPT = os.path.join(_BASE, '..', 'prompts', 'gto_labeller_v3.md')
_KNOWLEDGE = os.path.join(_BASE, '..', 'knowledge', 'three_way_gto.md')
_TEST_SET_50 = os.path.join(_BASE, '..', 'training-data',
                            'test_set_50_labelled.jsonl')
_3WAY_COMBINED = os.path.join(_BASE, '..', 'training-data',
                              '3way_combined_350.jsonl')


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
    """Load and filter to the 24 three-way MW reference hands."""
    all_hands = parse_reference_hands(_DESIGNS, _ANALYSIS)
    three_way = [h for h in all_hands if h.num_opponents == 2]
    return three_way


def _load_labelled_record(sid: str) -> dict:
    """Find a situation by id across the canonical labelled JSONL sources.

    Search order: test_set_50_labelled.jsonl (primary labelled set),
    then 3way_combined_350.jsonl. Raises KeyError if not found.
    """
    for path in (_TEST_SET_50, _3WAY_COMBINED):
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for line in f:
                r = json.loads(line)
                if r.get('situation_id') == sid:
                    return r
    raise KeyError(
        f"{sid} not found in canonical labelled JSONL sources: "
        f"{_TEST_SET_50} or {_3WAY_COMBINED}"
    )


def _labelled_record_to_reference_hand(record: dict) -> ReferenceHand:
    """Convert a canonical labelled JSONL record into a ReferenceHand.

    All fields are sourced from the record — nothing is hardcoded. This
    is how the 4 new hard anchors (and any Group-D hands living in the
    labelled JSONL) enter the exam.
    """
    sid = record['situation_id']
    feat = record.get('feat_dict', {})
    villain_positions = record.get('villain_positions') or []
    villain_pos = villain_positions[0] if villain_positions else ''

    return ReferenceHand(
        ref_id=sid,
        axis='v2.3-hard-anchor',
        hero_cards=record['hero_cards'],
        board=record['board'],
        street=str(record.get('street', '')).capitalize(),
        hero_position=record['hero_position'],
        villain_position=villain_pos,
        num_opponents=int(record.get('num_opponents', 2)),
        pot=float(record.get('pot', 0)),
        facing_bet=bool(record.get('facing_bet', False)),
        to_call=float(record.get('to_call', 0)),
        opener_position='',
        bettor_position=None,
        expert_action=record['expert_action'],
        expert_confidence=record.get('expert_confidence', 'MEDIUM'),
        equity=float(record.get('equity', 0.0)),
        villain_aggression_count=int(feat.get('villain_aggression_count', 0)),
        villain_checked_back=int(feat.get('villain_checked_back', 0)),
        villain_call_count=int(feat.get('villain_call_count', 0)),
        num_callers_to_bet=int(feat.get('num_callers_to_bet', 0)),
        facing_raise=int(feat.get('facing_raise', 0)),
        action_string='',
    )


def load_new_hard_anchors() -> list:
    """Load the 4 new v2.3 hard anchors from the canonical labelled JSONL.

    These are the spots that specifically exercise the defensive
    multiway-checked-through CHECK bias the v2.3 supplement is correcting.
    Returns a list of ReferenceHand objects sourced — never hardcoded.
    """
    return [
        _labelled_record_to_reference_hand(_load_labelled_record(sid))
        for sid in _NEW_HARD_ANCHOR_IDS
    ]


def load_group_d_reversals() -> list:
    """Load any Group-D reversal hands registered in the diagnostic set.

    Hands in GROUP_D_REVERSAL_HANDS are looked up in the canonical
    labelled JSONL. Silently skips hands that are not yet in the
    labelled set (the diagnostic-set is still under owner review; see
    PLAN_V23_DIAGNOSTIC_TEST_SET_2026-04-15.md §2.D). Registered hands
    that ARE present in the canonical set are ingested.
    """
    loaded = []
    for sid in sorted(GROUP_D_REVERSAL_HANDS):
        try:
            record = _load_labelled_record(sid)
        except KeyError:
            # Not yet in canonical labelled set. The enforcement rule
            # still applies if the exam ever scores a hand with this
            # ref_id — we just can't auto-ingest the situation data yet.
            continue
        loaded.append(_labelled_record_to_reference_hand(record))
    return loaded


def load_all_calibration_hands() -> list:
    """Return the v2.3 base calibration-exam hand list.

    Composition (STANDARD_EXAM_SIZE = 28):
        - 24 MW reference hands (existing)
        - 4 new hard anchors (d8886/d2410/d8963/d3178)

    Does NOT include Group-D reversal extensions — see
    load_all_calibration_hands_with_group_d() for the extended set used
    by run_calibration().
    """
    hands = list(load_3way_reference_hands())
    hands.extend(load_new_hard_anchors())
    return hands


def load_all_calibration_hands_with_group_d() -> list:
    """Return the base exam + Group-D reversal extensions.

    Extensions from GROUP_D_REVERSAL_HANDS that are present in the
    canonical labelled JSONL are appended. This INCREASES the exam
    beyond STANDARD_EXAM_SIZE. The 23/28 threshold still applies to
    the full scoring tally (i.e. additional Group-D hands are bonus
    enforcement on top of the base threshold).
    """
    hands = load_all_calibration_hands()
    already = {h.ref_id for h in hands}
    for h in load_group_d_reversals():
        if h.ref_id not in already:
            hands.append(h)
            already.add(h.ref_id)
    return hands


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
    """Score calibration results and check v2.3 gate criteria.

    Gate (v2.3):
        - standard-exam threshold: STANDARD_PASS_THRESHOLD correct out of
          STANDARD_EXAM_SIZE hands (23/28)
        - reversal gate: 100% on every hand in GTO_REVERSAL_HANDS
          (MW-30/33/50 + predicate anchors + Group-D hands)

    A single reversal failure fails the exam regardless of the overall
    count. Reversal hands count BOTH toward the standard tally and the
    reversal tally — they are a subset of the full exam.
    """
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

    # Gate check (v2.3: 23/28 + 100% reversals)
    gate_overall = correct >= STANDARD_PASS_THRESHOLD
    gate_reversals = (reversal_total > 0 and
                      reversal_correct == reversal_total)
    gate_passed = gate_overall and gate_reversals

    return {
        'total': total,
        'correct': correct,
        'accuracy': accuracy,
        'gate_passed': gate_passed,
        'gate_overall': (
            f"{correct}/{total} >= {STANDARD_PASS_THRESHOLD} "
            f"→ {'PASS' if gate_overall else 'FAIL'}"
        ),
        'gate_reversals': (
            f"{reversal_correct}/{reversal_total} (100% required) "
            f"→ {'PASS' if gate_reversals else 'FAIL'}"
        ),
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
    print(f"  Gate ({STANDARD_PASS_THRESHOLD}/{STANDARD_EXAM_SIZE}): "
          f"{scores['gate_overall']}")
    print(f"  Gate (reversals, 100%): {scores['gate_reversals']}")
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

    # Load the full v2.3 calibration set: 24 MW + 4 new anchors (+ any
    # registered Group-D reversal hands).
    hands = load_all_calibration_hands_with_group_d()
    print(f"Loaded {len(hands)} calibration hands "
          f"(base: {STANDARD_EXAM_SIZE}, +{len(hands) - STANDARD_EXAM_SIZE} "
          f"Group-D extensions)")

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
