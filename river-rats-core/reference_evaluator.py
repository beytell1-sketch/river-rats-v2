"""Reference set evaluator — test variants against expert GTO labels.

Parses the 40-hand expert reference set (MW-11 to MW-50), runs each
hand through the feature pipeline + oracle + adjuster for each variant,
and compares to expert-labelled GTO actions.

Also provides evaluate_facing_bet_test_set() for the 40-hand facing-bet
test set (FB-01 to FB-40).

No opponents needed — features in → action out → compare to label.

Usage:
    from reference_evaluator import evaluate_variants, format_eval_report

    results = evaluate_variants(
        variants=[baseline, draw_fix, loose_draws_oop],
        oracle_path="models/gto_model_v8_38feat.json",
    )
    print(format_eval_report(results))

    # Facing-bet test set:
    fb_results = evaluate_facing_bet_test_set()
    print(f"Score: {fb_results['correct']}/{fb_results['total']}")
"""
from __future__ import annotations
import argparse
import json
import os
import re
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

from feature_keys import F
from feature_extractor import extract_all_features
from gto_model import GtoOracle
from multiway_adjuster import adjust, get_default_params
from self_play import Variant


# ── Reference hand parsing ──────────────────────────────────────────

STREET_MAP = {'Flop': 'f', 'Turn': 't', 'River': 'r'}


@dataclass
class ReferenceHand:
    """A parsed expert-labelled reference hand."""
    ref_id: str           # e.g. "MW-11"
    axis: str
    hero_cards: str       # e.g. "5h4h"
    board: str            # e.g. "Qd7c2s"
    street: str           # "flop", "turn", "river"
    hero_position: str    # e.g. "BB"
    villain_position: str # e.g. "CO"
    num_opponents: int
    pot: float
    facing_bet: bool
    to_call: float
    opener_position: str
    bettor_position: Optional[str]
    expert_action: str    # "CHECK", "CALL", "FOLD", "BET", "RAISE"
    expert_confidence: str  # "HIGH", "MEDIUM", "LOW"
    equity: float         # from the GTO action table
    villain_aggression_count: int = 0   # prior streets villain bet/raised
    villain_checked_back: int = 0       # 1 if villain checked any prior street
    villain_call_count: int = 0         # prior streets villain flat-called
    num_callers_to_bet: int = 0         # opponents who cold-called current-street bet
    facing_raise: int = 0              # 1 if hero faces a raise (not just initial bet)
    action_string: str = ''            # validated current-street action sequence


# Action-history annotations for each reference hand.
# Derived from the prose action history in BATCH2_8_HAND_DESIGNS.md.
# Tuple: (villain_agg, villain_checked, villain_call, num_callers_to_bet, facing_raise)
# First 3: prior streets only, primary villain. Last 2: current-street action context.
_ACTION_HISTORY = {
    # Batch 2: Bluff Compression (MW-11 to MW-16)
    'MW-11': (1, 0, 0, 0, 0),  # Flop. CO opens, checks to hero. No bet to call.
    'MW-12': (0, 0, 1, 0, 0),  # Flop. BB calls pf, checks to hero.
    'MW-13': (1, 0, 0, 0, 0),  # Flop. BTN opens, hero first to act.
    'MW-14': (1, 0, 0, 0, 0),  # Flop. CO bets, hero faces bet. No callers between.
    'MW-15': (0, 1, 1, 0, 0),  # River. BB called pf, checked flop+turn. Checks to hero.
    'MW-16': (0, 0, 1, 0, 0),  # Flop. BB calls pf, checks to hero (4-way).
    # Batch 3: Nut Potential (MW-17 to MW-22)
    'MW-17': (1, 0, 0, 0, 0),  # Flop. CO bets into hero. No callers between.
    'MW-18': (1, 0, 0, 0, 0),  # Flop. CO bets into hero. No callers between.
    'MW-19': (0, 0, 1, 0, 0),  # Flop. Checks to hero (BTN).
    'MW-20': (0, 0, 1, 0, 0),  # Flop. BB leads 40 into 110. Hero faces bet.
    'MW-21': (1, 0, 0, 0, 0),  # Flop. CO bets, hero faces bet.
    'MW-22': (1, 0, 0, 0, 0),  # Flop. Hero first to act OOP 4-way.
    # Batch 4: Position Amplification (MW-23 to MW-28)
    'MW-23': (0, 0, 1, 0, 0),  # Flop. Checks to hero (BTN).
    'MW-24': (1, 0, 0, 0, 0),  # Flop. Hero first to act OOP.
    'MW-25': (0, 0, 1, 0, 0),  # Flop. Checks to hero (BTN).
    'MW-26': (1, 0, 0, 0, 0),  # Flop. Hero first to act OOP.
    'MW-27': (0, 0, 1, 0, 0),  # Flop. Checks to hero (BTN).
    'MW-28': (1, 0, 0, 0, 0),  # Flop. Hero first to act OOP.
    # Batch 5: Aggression Respect (MW-29 to MW-34)
    'MW-29': (1, 0, 0, 0, 0),  # Flop. CO bets, hero faces bet.
    'MW-30': (1, 0, 0, 1, 0),  # Flop. CO bets, BTN CALLS, hero faces bet+call. Key hand.
    'MW-31': (1, 0, 0, 0, 1),  # Flop. Hero bet, CO CHECK-RAISES. facing_raise=1. Key hand.
    'MW-32': (2, 0, 0, 0, 0),  # Turn. CO double-barrels. Hero faces bet.
    'MW-33': (1, 0, 0, 1, 0),  # Flop. CO bets, BTN calls, SB folds. Hero faces bet+call.
    'MW-34': (0, 0, 1, 0, 0),  # Flop. Checks to hero (CO). Hero acts.
    # Batch 6: SPR Interaction (MW-35 to MW-40)
    'MW-35': (1, 0, 0, 0, 0),  # Flop. CO bets into hero (low SPR).
    'MW-36': (1, 0, 0, 0, 0),  # Flop. CO bets into hero (mid SPR).
    'MW-37': (1, 0, 0, 0, 0),  # Flop. CO bets into hero (high SPR).
    'MW-38': (0, 0, 1, 0, 0),  # Flop. BB leads into hero.
    'MW-39': (1, 0, 0, 0, 0),  # Flop. CO bets into hero (deep SPR).
    'MW-40': (0, 0, 1, 0, 0),  # Flop. Checks to hero (BTN, deep).
    # Batch 7: Range Narrowing (MW-41 to MW-46)
    'MW-41': (2, 0, 0, 0, 0),  # Turn. CO double-barrels. Hero faces bet.
    'MW-42': (1, 1, 1, 0, 0),  # River. CO: bet flop (agg=1), checked+called turn (check=1, call=1), checks river.
    'MW-43': (1, 1, 0, 0, 0),  # River. CO: checked flop+turn, now bets river.
    'MW-44': (1, 0, 1, 0, 0),  # Turn. BB: called pf, donk-bet flop, leads turn again.
    'MW-45': (1, 1, 0, 0, 0),  # Turn. CO: opened pf, checked flop, now bets turn.
    'MW-46': (1, 1, 2, 0, 1),  # River. CO: bet flop, check-called turn, CHECK-RAISES river. Key hand.
    # Batch 8: Combined Axes (MW-47 to MW-50)
    'MW-47': (1, 0, 0, 1, 0),  # Flop. CO bets, BTN calls. Hero (SB) faces bet+call OOP.
    'MW-48': (1, 0, 0, 0, 0),  # Flop. Hero first to act OOP (low SPR).
    'MW-49': (0, 0, 2, 0, 0),  # Turn. BB: called pf, called flop. Checks to hero.
    'MW-50': (1, 0, 1, 0, 0),  # Turn. BTN raised flop. CO calls. BTN bets turn (bet, not raise).
}


# Validated action strings for each reference hand (current street only).
# Reconstructed from _ACTION_HISTORY prose comments + hand design metadata.
# Each string validated through hand_sequence_validator (40/40 pass, 2026-04-13).
_ACTION_STRINGS = {
    'MW-11': 'SB check, BB ???',
    'MW-12': 'BB check, BTN ???',
    'MW-13': 'SB ???',
    'MW-14': 'BB check, CO bet 30, BB ???',
    'MW-15': 'BB check, BTN ???',
    'MW-16': 'BB check, BTN ???',
    'MW-17': 'BB check, CO bet 30, BB ???',
    'MW-18': 'BB check, CO bet 30, BB ???',
    'MW-19': 'BB check, BTN ???',
    'MW-20': 'BB bet 40, CO fold, BTN ???',
    'MW-21': 'BB check, CO bet 30, BTN fold, BB ???',
    'MW-22': 'BB ???',
    'MW-23': 'BB check, BTN ???',
    'MW-24': 'SB ???',
    'MW-25': 'BB check, CO check, BTN ???',
    'MW-26': 'SB ???',
    'MW-27': 'BB check, BTN ???',
    'MW-28': 'SB ???',
    'MW-29': 'BB check, CO bet 30, BTN fold, BB ???',
    'MW-30': 'BB check, CO bet 35, BTN call 35, BB ???',
    'MW-31': 'CO check, BTN bet, CO raise, BTN ???',
    'MW-32': 'CO bet 60, BTN ???',
    'MW-33': 'BB check, CO bet 40, BTN call 40, BB ???',
    'MW-34': 'BB check, CO ???',
    'MW-35': 'CO bet 30, BTN ???',
    'MW-36': 'CO bet 40, BTN ???',
    'MW-37': 'CO bet 30, BTN ???',
    'MW-38': 'BB bet 40, CO fold, BTN ???',
    'MW-39': 'CO bet 30, BTN ???',
    'MW-40': 'BB check, CO check, BTN ???',
    'MW-41': 'CO bet 90, BTN ???',
    'MW-42': 'CO check, BTN ???',
    'MW-43': 'BB check, CO bet 60, BTN fold, BB ???',
    'MW-44': 'BB bet 60, CO fold, BTN ???',
    'MW-45': 'BB check, CO bet 60, BTN fold, BB ???',
    'MW-46': 'CO check, BTN bet, CO raise, BTN ???',
    'MW-47': 'SB check, BB check, CO bet 30, BTN call 30, SB ???',
    'MW-48': 'BB ???',
    'MW-49': 'BB check, BTN ???',
    'MW-50': 'BB check, CO check, BTN bet 90, BB ???',
}


def parse_reference_hands(designs_path: str, analysis_path: str) -> List[ReferenceHand]:
    """Parse hand designs and GTO action labels into ReferenceHand objects."""
    # Parse GTO actions from the analysis table
    actions = _parse_gto_table(analysis_path)

    # Parse hand designs
    hands = _parse_hand_designs(designs_path)

    # Merge
    result = []
    for h in hands:
        if h.ref_id in actions:
            h.expert_action = actions[h.ref_id]['action']
            h.expert_confidence = actions[h.ref_id]['confidence']
            h.equity = actions[h.ref_id]['equity']
            result.append(h)

    return result


def _parse_gto_table(path: str) -> Dict[str, dict]:
    """Parse the GTO Action Table from BATCH2_8_RANGE_ANALYSIS.md."""
    with open(path) as f:
        content = f.read()

    actions = {}
    # Match table rows: | MW-XX | axis | equity | pot_odds | ACTION | CONFIDENCE |
    pattern = r'\|\s*(MW-\d+)\s*\|\s*\S+\s*\|\s*([\d.]+)\s*\|\s*[\d.]+\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|'
    for m in re.finditer(pattern, content):
        ref_id = m.group(1)
        actions[ref_id] = {
            'equity': float(m.group(2)),
            'action': m.group(3).upper(),
            'confidence': m.group(4).upper(),
        }
    return actions


def _parse_hand_designs(path: str) -> List[ReferenceHand]:
    """Parse hand designs from BATCH2_8_HAND_DESIGNS.md."""
    with open(path) as f:
        content = f.read()

    hands = []
    # Split by hand headers
    sections = re.split(r'### (MW-\d+):', content)

    for i in range(1, len(sections), 2):
        ref_id = sections[i]
        block = sections[i + 1]

        hand = _parse_one_hand(ref_id, block)
        if hand:
            hands.append(hand)

    return hands


def _parse_one_hand(ref_id: str, block: str) -> Optional[ReferenceHand]:
    """Parse a single hand design block."""
    def _get(pattern, default=''):
        m = re.search(pattern, block)
        return m.group(1).strip() if m else default

    hero_cards_raw = _get(r'\*\*Hero cards:\*\*\s*(.+)')
    # Convert "5h/4h" or "5h 4h" to "5h4h"
    hero_cards = re.sub(r'[/ ]', '', hero_cards_raw)

    board_raw = _get(r'\*\*Board:\*\*\s*(.+)')
    # Convert "Qd 7c 2s" to "Qd7c2s"
    board = re.sub(r'\s+', '', board_raw)

    street = _get(r'\*\*Street:\*\*\s*(\w+)').lower()

    hero_pos = _get(r'\*\*Hero position:\*\*\s*(\w+)')
    villain_pos = _get(r'\*\*Primary villain position:\*\*\s*(\w+)')

    num_opp_str = _get(r'\*\*Num opponents:\*\*\s*(\d+)', '1')
    num_opponents = int(num_opp_str)

    pot_str = _get(r'\*\*Pot:\*\*\s*(\d+)', '0')
    pot = float(pot_str)

    facing_bet_str = _get(r'\*\*Facing bet:\*\*\s*(\w+)', 'No')
    facing_bet = facing_bet_str.lower() == 'yes'

    to_call_str = _get(r'\*\*To call:\*\*\s*(\d+)', '0')
    to_call = float(to_call_str)

    opener = _get(r'\*\*Opener position:\*\*\s*(\w+)', '')
    bettor = _get(r'\*\*Bettor position:\*\*\s*(\w+)', '')
    if bettor.lower() == 'none':
        bettor = ''

    if not hero_cards or not board:
        return None

    # Look up action-history annotations
    ah = _ACTION_HISTORY.get(ref_id, (0, 0, 0, 0, 0))

    return ReferenceHand(
        ref_id=ref_id,
        axis='',
        hero_cards=hero_cards,
        board=board,
        street=street,
        hero_position=hero_pos,
        villain_position=villain_pos,
        num_opponents=num_opponents,
        pot=pot,
        facing_bet=facing_bet,
        to_call=to_call,
        opener_position=opener,
        bettor_position=bettor or None,
        expert_action='',
        expert_confidence='',
        equity=0.0,
        villain_aggression_count=ah[0],
        villain_checked_back=ah[1],
        villain_call_count=ah[2],
        num_callers_to_bet=ah[3],
        facing_raise=ah[4],
        action_string=_ACTION_STRINGS.get(ref_id, ''),
    )


# ── Evaluation ──────────────────────────────────────────────────────

@dataclass
class HandResult:
    """Result of evaluating one hand with one variant."""
    ref_id: str
    variant_name: str
    expert_action: str
    expert_confidence: str
    oracle_action: str       # raw oracle prediction
    adjusted_action: str     # after adjuster
    was_adjusted: bool
    correct: bool            # adjusted_action matches expert_action
    axis: str
    equity: float


@dataclass
class VariantEvalResult:
    """Aggregate evaluation result for one variant."""
    variant_name: str
    total: int
    correct: int
    accuracy: float
    by_confidence: Dict[str, Tuple[int, int]]  # {conf: (correct, total)}
    by_axis: Dict[str, Tuple[int, int]]
    failures: List[HandResult]                   # incorrect hands
    hand_results: List[HandResult]


@dataclass
class EvalReport:
    """Complete evaluation report across all variants."""
    num_hands: int
    variants: List[VariantEvalResult]


def evaluate_variants(variants: List[Variant],
                      oracle_path: str = None,
                      designs_path: str = None,
                      analysis_path: str = None) -> EvalReport:
    """Evaluate all variants against the expert reference set.

    Args:
        variants: List of Variant objects to evaluate.
        oracle_path: Path to the XGBoost model.
        designs_path: Path to BATCH2_8_HAND_DESIGNS.md.
        analysis_path: Path to BATCH2_8_RANGE_ANALYSIS.md.

    Returns:
        EvalReport with per-variant accuracy and failure analysis.
    """
    base = os.path.dirname(__file__)
    if oracle_path is None:
        oracle_path = os.path.join(base, 'models', 'gto_model_v8_38feat.json')
    if designs_path is None:
        designs_path = os.path.join(base, '..', 'design', 'multiway_reference_set',
                                    'BATCH2_8_HAND_DESIGNS.md')
    if analysis_path is None:
        analysis_path = os.path.join(base, '..', 'design', 'multiway_reference_set',
                                     'BATCH2_8_RANGE_ANALYSIS.md')

    oracle = GtoOracle(oracle_path)
    hands = parse_reference_hands(designs_path, analysis_path)

    variant_results = []
    for variant in variants:
        vr = _evaluate_one_variant(variant, hands, oracle)
        variant_results.append(vr)

    return EvalReport(num_hands=len(hands), variants=variant_results)


def _evaluate_one_variant(variant: Variant, hands: List[ReferenceHand],
                          oracle: GtoOracle) -> VariantEvalResult:
    """Evaluate a single variant against all reference hands."""
    results = []

    for hand in hands:
        hr = _evaluate_one_hand(variant, hand, oracle)
        results.append(hr)

    correct = sum(1 for r in results if r.correct)
    total = len(results)

    # By confidence
    by_conf: Dict[str, Tuple[int, int]] = {}
    for r in results:
        conf = r.expert_confidence
        if conf not in by_conf:
            by_conf[conf] = (0, 0)
        c, t = by_conf[conf]
        by_conf[conf] = (c + (1 if r.correct else 0), t + 1)

    # By axis
    by_axis: Dict[str, Tuple[int, int]] = {}
    for r in results:
        axis = r.axis
        if axis not in by_axis:
            by_axis[axis] = (0, 0)
        c, t = by_axis[axis]
        by_axis[axis] = (c + (1 if r.correct else 0), t + 1)

    failures = [r for r in results if not r.correct]

    return VariantEvalResult(
        variant_name=variant.name,
        total=total,
        correct=correct,
        accuracy=correct / total if total > 0 else 0.0,
        by_confidence=by_conf,
        by_axis=by_axis,
        failures=failures,
        hand_results=results,
    )


def _evaluate_one_hand(variant: Variant, hand: ReferenceHand,
                       oracle: GtoOracle) -> HandResult:
    """Evaluate a single hand with a single variant."""
    # Build the hand dict for the feature pipeline
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

    # Run feature extraction
    feat_dict = extract_all_features(hand_dict)

    # Oracle prediction
    features = GtoOracle.features_from_dict(feat_dict)
    pred = oracle.predict(features)

    # Adjuster
    adjusted = adjust(pred, feat_dict, hand.num_opponents, params=variant.params)

    # Compare model output against expert labels.
    # Older models (v8) output FOLD/RAISE for not-facing-bet spots where
    # the expert vocabulary uses CHECK/BET. Normalize both sides to handle
    # this: CHECK↔FOLD and BET↔RAISE are equivalent when not facing a bet.
    oracle_action = pred.action.upper()
    adjusted_action = adjusted.adjusted_action.upper()
    expert_action = hand.expert_action.upper()

    def _normalize(action):
        """Collapse CHECK/FOLD and BET/RAISE for not-facing-bet comparison."""
        if action == 'CHECK': return 'FOLD'
        if action == 'BET': return 'RAISE'
        return action

    correct = (_normalize(adjusted_action) == _normalize(expert_action))

    return HandResult(
        ref_id=hand.ref_id,
        variant_name=variant.name,
        expert_action=expert_action,
        expert_confidence=hand.expert_confidence,
        oracle_action=oracle_action,
        adjusted_action=adjusted_action,
        was_adjusted=adjusted.was_adjusted,
        correct=correct,
        axis=hand.axis or _infer_axis(hand.ref_id),
        equity=hand.equity,
    )


def _infer_axis(ref_id: str) -> str:
    """Infer the axis from the reference ID number."""
    num = int(ref_id.split('-')[1])
    if 11 <= num <= 16: return 'bluff_compression'
    if 17 <= num <= 22: return 'nut_potential'
    if 23 <= num <= 28: return 'position_amplification'
    if 29 <= num <= 34: return 'aggression_respect'
    if 35 <= num <= 40: return 'spr_interaction'
    if 41 <= num <= 46: return 'range_narrowing'
    if 47 <= num <= 50: return 'combined'
    return 'unknown'


# ── Reporting ───────────────────────────────────────────────────────

def format_eval_report(report: EvalReport) -> str:
    """Format a human-readable evaluation report."""
    lines = [
        f"Reference Set Evaluation — {report.num_hands} Expert-Labelled Hands",
        "=" * 65,
        "",
        f"{'Variant':<30} {'Correct':>8} {'Total':>6} {'Accuracy':>10}",
        "-" * 65,
    ]

    for vr in sorted(report.variants, key=lambda v: -v.accuracy):
        lines.append(
            f"  {vr.variant_name:<28} {vr.correct:>8} {vr.total:>6} "
            f"{vr.accuracy:>9.1%}"
        )

    lines.append("=" * 65)

    # Winner details
    best = max(report.variants, key=lambda v: v.accuracy)
    lines.append(f"\nBest: {best.variant_name} ({best.accuracy:.1%})")

    # By confidence for the best variant
    lines.append(f"\n  By confidence:")
    for conf in ['HIGH', 'MEDIUM', 'LOW']:
        if conf in best.by_confidence:
            c, t = best.by_confidence[conf]
            pct = c / t if t > 0 else 0
            lines.append(f"    {conf}: {c}/{t} ({pct:.0%})")

    # By axis for the best variant
    lines.append(f"\n  By axis:")
    for axis, (c, t) in sorted(best.by_axis.items()):
        pct = c / t if t > 0 else 0
        lines.append(f"    {axis}: {c}/{t} ({pct:.0%})")

    # Failures for each variant
    for vr in report.variants:
        if vr.failures:
            lines.append(f"\n  {vr.variant_name} failures ({len(vr.failures)}):")
            for f in vr.failures:
                adj_note = f" (adj from {f.oracle_action})" if f.was_adjusted else ""
                lines.append(
                    f"    {f.ref_id} [{f.expert_confidence}]: "
                    f"expert={f.expert_action}, got={f.adjusted_action}{adj_note} "
                    f"(eq={f.equity:.3f})"
                )

    return "\n".join(lines)


# ── Facing-Bet Test Set Evaluation ──────────────────────────────────

# _opener_position inference: for each FB situation the preflop opener
# is CO (standard 3-way CO-open pot) unless the action string shows BB
# leading the betting (donk), in which case CO is still the PF opener.
# FB-20 and FB-36 are 2-way (BB folded), CO/BTN pot — opener is BTN or CO
# depending on the situation.  The opener is only used as a metadata hint
# by range features; it does not affect correctness.
_FB_OPENER_POSITION = {
    # BB,CO,BTN pots — CO opened preflop
    'FB-01': 'CO', 'FB-02': 'CO', 'FB-03': 'CO', 'FB-04': 'CO',
    'FB-05': 'CO', 'FB-06': 'CO', 'FB-07': 'CO', 'FB-08': 'CO',
    'FB-09': 'CO', 'FB-10': 'CO', 'FB-11': 'CO', 'FB-12': 'BTN',
    'FB-13': 'BTN', 'FB-14': 'CO', 'FB-15': 'CO', 'FB-16': 'CO',
    'FB-17': 'CO', 'FB-18': 'CO', 'FB-19': 'BTN', 'FB-21': 'CO',
    'FB-22': 'BTN', 'FB-23': 'CO', 'FB-24': 'CO', 'FB-25': 'CO',
    'FB-26': 'CO', 'FB-27': 'CO', 'FB-28': 'CO', 'FB-29': 'CO',
    'FB-30': 'CO', 'FB-31': 'CO', 'FB-32': 'CO', 'FB-33': 'BTN',
    'FB-34': 'BTN', 'FB-35': 'BTN', 'FB-37': 'BTN', 'FB-38': 'CO',
    'FB-39': 'BTN', 'FB-40': 'BTN',
    # 2-way pots
    'FB-20': 'BTN',   # CO vs BTN, BTN opened
    'FB-36': 'BTN',   # CO vs BTN, BTN opened
}

# villain_aggression_count for the facing-bet test set.
# For flop situations: 1 if CO c-bet the flop (normal), 0 if BB led (donk).
# For turn situations: reflects prior-street aggression.
# For river situations: reflects cumulative prior aggression.
_FB_ACTION_HISTORY = {
    # (villain_agg, villain_checked, villain_call, num_callers_to_bet, facing_raise)
    'FB-01': (1, 0, 0, 0, 0),  # Flop. CO c-bet; BTN folded; hero faces HU bet.
    'FB-02': (0, 0, 0, 0, 0),  # Flop. BB donk bet; CO folded; BTN faces HU bet.
    'FB-03': (1, 0, 0, 1, 0),  # Flop. CO bet, BTN called; hero faces bet+call.
    'FB-04': (1, 0, 0, 0, 0),  # Flop. CO c-bet; BTN folded; hero faces HU bet.
    'FB-05': (1, 0, 0, 0, 0),  # Flop. CO c-bet 66% pot; BTN first responder.
    'FB-06': (1, 0, 0, 0, 0),  # Flop. CO c-bet; BTN folded; hero faces HU bet.
    'FB-07': (0, 0, 0, 0, 0),  # Flop. BB donk; CO sandwiched; BTN behind.
    'FB-08': (0, 0, 0, 0, 0),  # Flop. BB donk; CO sandwiched; BTN behind.
    'FB-09': (1, 0, 0, 0, 0),  # Flop. CO pot-bet; BTN first responder; BB behind.
    'FB-10': (1, 0, 0, 0, 0),  # Flop. CO c-bet 33%; BTN folded; hero closes HU.
    'FB-11': (0, 0, 0, 0, 0),  # Flop. BB donk 50%; CO folded; BTN closes HU.
    'FB-12': (0, 0, 0, 0, 0),  # Flop. BTN c-bet after CO check; BB first resp; CO behind.
    'FB-13': (0, 0, 0, 1, 0),  # Flop. BTN bet, BB folded; CO closes HU vs BTN bet-and-call.
    'FB-14': (0, 0, 0, 0, 0),  # Flop. BB donk 33%; CO folded; BTN closes HU.
    'FB-15': (1, 0, 0, 0, 0),  # Flop. CO c-bet 50%; BTN folded; hero closes HU.
    'FB-16': (1, 0, 0, 1, 0),  # Flop. CO bet, BTN called; hero faces bet+call.
    'FB-17': (1, 1, 0, 0, 0),  # Turn. CO checked flop, delayed c-bet turn; BTN folded.
    'FB-18': (1, 1, 0, 0, 0),  # Turn. CO delayed c-bet; BTN first responder; BB behind.
    'FB-19': (0, 0, 1, 0, 0),  # Turn. BTN called flop c-bet, now bets turn; BB sandwich.
    'FB-20': (0, 0, 1, 0, 0),  # Turn. BB folded flop; CO called BTN flop bet, faces turn bet.
    'FB-21': (1, 1, 0, 0, 0),  # Turn. CO checked flop, delayed c-bet turn; BTN folded.
    'FB-22': (0, 0, 0, 1, 0),  # Flop. BTN c-bet, BB called; CO faces bet+call.
    'FB-23': (0, 0, 0, 0, 0),  # River. All checked flop+turn; CO first bet on river; BTN folded.
    'FB-24': (0, 0, 0, 0, 0),  # River. All checked flop+turn; BB donk river; CO folded.
    'FB-25': (2, 0, 0, 0, 0),  # River. CO triple-barrel; BTN folded earlier; hero faces HU.
    'FB-26': (0, 0, 0, 0, 0),  # River. All checked through; BB donk river; CO folded.
    'FB-27': (1, 0, 0, 0, 0),  # Flop. CO c-bet 33%; BTN folded; hero closes HU.
    'FB-28': (1, 0, 0, 1, 0),  # Flop. CO bet, BTN called; hero faces bet+call.
    'FB-29': (0, 0, 0, 0, 0),  # Flop. BB donk 50%; CO sandwiched; BTN behind.
    'FB-30': (1, 0, 0, 0, 0),  # Flop. CO c-bet 66%; BTN first responder; BB behind.
    'FB-31': (0, 0, 0, 0, 0),  # Flop. BB donk 66%; CO folded; BTN closes HU.
    'FB-32': (1, 0, 0, 1, 0),  # Flop. CO bet, BTN called; hero faces bet+call.
    'FB-33': (0, 0, 0, 1, 0),  # Flop. BTN bet, BB called; CO faces bet+call.
    'FB-34': (0, 0, 0, 1, 0),  # Flop. BTN bet 25%, BB called; CO faces bet+call.
    'FB-35': (0, 0, 1, 0, 0),  # Turn. BB folded; CO called BTN flop bet; BTN bets turn.
    'FB-36': (0, 0, 1, 0, 0),  # Turn. BB folded flop; CO called BTN flop bet; BTN bets turn.
    'FB-37': (0, 0, 0, 0, 0),  # Turn. All checked flop; BTN delayed bet; BB folded.
    'FB-38': (0, 0, 0, 0, 0),  # River. All checked flop+turn; BB pot-bet river; CO sandwich.
    'FB-39': (0, 1, 0, 0, 0),  # River. BTN checked back turn; BB faces BTN river bet; CO behind.
    'FB-40': (0, 0, 0, 0, 0),  # Flop. BTN c-bet 33%; BB sandwiched; CO behind.
}


def _build_fb_hand_dict(record: dict) -> dict:
    """Build a hand dict for extract_all_features() from a FB JSONL record.

    Constructs the same dict shape that _evaluate_one_hand() uses for the
    MW reference set, so the feature pipeline sees a consistent interface.
    """
    sid = record['situation_id']

    # Primary villain: first entry in villain_positions
    primary_villain = record['villain_positions'][0] if record['villain_positions'] else 'CO'

    ah = _FB_ACTION_HISTORY.get(sid, (0, 0, 0, 0, 0))
    opener = _FB_OPENER_POSITION.get(sid, 'CO')

    # num_callers_to_bet: derived from villain_positions length when pot is
    # already enlarged (bet-and-call pattern has 2+ villains and pot > 90).
    # We use the pre-annotated value from _FB_ACTION_HISTORY (index 3).

    hand_dict = {
        'h': record['hero_cards'],
        'b': record['board'],
        'pos': record['hero_pos'],
        'vp': primary_villain,
        'pot': float(record['pot']),
        'tc': float(record['to_call']),
        'st': record['street'],
        'fb': int(record['facing_bet']),
        'exp': 'C',   # placeholder; not used during inference
        F.META_NUM_OPPONENTS: len(record['villain_positions']),
        F.META_NUM_RAISES: 0,
        F.META_OPENER_POSITION: opener,
        F.META_BETTOR_POSITION: primary_villain,
        '_villain_aggression_count': ah[0],
        '_villain_checked_back': ah[1],
        '_villain_call_count': ah[2],
        '_num_callers_to_bet': ah[3],
        '_facing_raise': ah[4],
    }
    return hand_dict


def evaluate_facing_bet_test_set(
    oracle_path: str = None,
    jsonl_path: str = None,
) -> dict:
    """Evaluate the facing-bet test set (FB-01 to FB-40) against the oracle.

    Loads the JSONL file, extracts features for each situation, runs the
    oracle, and compares against the expected action.  If accept_alternative
    is set on a record, the oracle picking that alternative action also counts
    as correct.

    The oracle prediction step is wrapped in a try/except so a missing model
    file causes a graceful skip rather than a hard crash — useful for smoke
    testing the data pipeline without a trained model.

    Args:
        oracle_path: Path to the XGBoost model JSON.  Defaults to the same
                     model used by evaluate_variants().
        jsonl_path:  Path to facing_bet_test_set_40.jsonl.  Defaults to
                     training-data/ relative to the repo root.

    Returns:
        dict with keys:
            correct       (int)
            total         (int)
            accuracy      (float)
            by_action     (dict: action → {'correct': int, 'total': int})
            failures      (list of dicts with situation_id, expected, got)
            skipped       (list of situation_ids where oracle errored)
    """
    base = os.path.dirname(__file__)

    if oracle_path is None:
        oracle_path = os.path.join(base, 'models', 'gto_model_v8_38feat.json')

    if jsonl_path is None:
        jsonl_path = os.path.join(base, '..', 'training-data',
                                  'facing_bet_test_set_40.jsonl')

    jsonl_path = os.path.normpath(jsonl_path)

    # Load test records
    records = []
    with open(jsonl_path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    # Load oracle — may fail if model file is absent
    oracle = None
    oracle_load_error = None
    try:
        oracle = GtoOracle(oracle_path)
    except Exception as e:
        oracle_load_error = str(e)

    correct = 0
    total = len(records)
    failures = []
    skipped = []

    # Per-action tracking: CALL, FOLD, RAISE
    by_action: Dict[str, Dict[str, int]] = {}
    for action in ('CALL', 'FOLD', 'RAISE'):
        by_action[action] = {'correct': 0, 'total': 0}

    for record in records:
        sid = record['situation_id']
        expected = record['expected_action'].upper()
        alternative = (record.get('accept_alternative') or '').upper() or None

        # Track total per expected action
        if expected in by_action:
            by_action[expected]['total'] += 1

        # Build hand dict and extract features
        try:
            hand_dict = _build_fb_hand_dict(record)
            feat_dict = extract_all_features(hand_dict)
        except Exception as e:
            skipped.append({'situation_id': sid, 'error': f'feature extraction: {e}'})
            continue

        # Oracle prediction — skip gracefully if model absent
        if oracle is None:
            skipped.append({'situation_id': sid,
                            'error': f'oracle not loaded: {oracle_load_error}'})
            continue

        try:
            features = GtoOracle.features_from_dict(feat_dict)
            pred = oracle.predict(features)
            got = pred.action.upper()
        except Exception as e:
            skipped.append({'situation_id': sid, 'error': f'oracle predict: {e}'})
            continue

        # Correctness: exact match OR acceptable alternative
        is_correct = (got == expected) or (alternative is not None and got == alternative)

        if is_correct:
            correct += 1
            if expected in by_action:
                by_action[expected]['correct'] += 1
        else:
            failures.append({
                'situation_id': sid,
                'expected': expected,
                'accept_alternative': alternative,
                'got': got,
                'confidence': record.get('confidence', ''),
                'solver_verified': record.get('solver_verified', False),
            })

    accuracy = correct / total if total > 0 else 0.0

    return {
        'correct': correct,
        'total': total,
        'accuracy': accuracy,
        'by_action': by_action,
        'failures': failures,
        'skipped': skipped,
    }


# ── CLI entry point ──────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Reference set evaluator for River Rats GTO oracle.'
    )
    parser.add_argument(
        '--facing-bet',
        action='store_true',
        help='Evaluate the facing-bet test set (FB-01 to FB-40).',
    )
    args = parser.parse_args()

    if args.facing_bet:
        results = evaluate_facing_bet_test_set()
        print(f"Facing-Bet Test Set — FB-01 to FB-40")
        print(f"Score: {results['correct']}/{results['total']} "
              f"({results['accuracy']:.1%})")
        print()
        print("By action:")
        for action in ('CALL', 'FOLD', 'RAISE'):
            d = results['by_action'][action]
            c, t = d['correct'], d['total']
            pct = c / t if t > 0 else 0.0
            print(f"  {action}: {c}/{t} ({pct:.0%})")
        if results['failures']:
            print(f"\nFailures ({len(results['failures'])}):")
            for f in results['failures']:
                alt = f"  [alt={f['accept_alternative']}]" if f['accept_alternative'] else ''
                sv = ' [solver]' if f['solver_verified'] else ''
                print(f"  {f['situation_id']} [{f['confidence']}]{sv}: "
                      f"expected={f['expected']}{alt}, got={f['got']}")
        if results['skipped']:
            print(f"\nSkipped ({len(results['skipped'])}):")
            for s in results['skipped']:
                print(f"  {s['situation_id']}: {s['error']}")
    else:
        print("No evaluation mode selected. Use --facing-bet to evaluate the "
              "facing-bet test set.")
        print("For the MW reference set, import evaluate_variants() directly.")
