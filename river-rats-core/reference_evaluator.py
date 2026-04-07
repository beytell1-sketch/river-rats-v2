"""Reference set evaluator — test variants against expert GTO labels.

Parses the 40-hand expert reference set (MW-11 to MW-50), runs each
hand through the feature pipeline + oracle + adjuster for each variant,
and compares to expert-labelled GTO actions.

No opponents needed — features in → action out → compare to label.

Usage:
    from reference_evaluator import evaluate_variants, format_eval_report

    results = evaluate_variants(
        variants=[baseline, draw_fix, loose_draws_oop],
        oracle_path="models/gto_model_v8_38feat.json",
    )
    print(format_eval_report(results))
"""
from __future__ import annotations
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
    'MW-42': (2, 1, 1, 0, 0),  # River. CO: bet flop, checked+called turn, checks river.
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
