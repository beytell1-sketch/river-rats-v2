#!/usr/bin/env python3
"""GTO Expert labeller for 3-way postflop situations.

Reads situations JSONL, applies poker reasoning to label each with
the correct GTO action + confidence + reasoning.

The labelling logic uses the 45-feature vector to make decisions:
- Range composition (villain_top_pair_plus_pct, air_pct, etc.)
- Equity (raw_equity, equity_vs_range, equity_margin)
- Hand strength (hand_category, is_made_hand, is_strong_made, is_monster)
- Board texture (danger_score, flush_danger, straight_danger)
- Position (is_ip)
- Pot geometry (pot_odds, spr, bet_to_pot)
- Action context (facing_bet, facing_raise, num_callers_to_bet)

Usage:
    python3 label_3way_situations.py
    python3 label_3way_situations.py --input path/to/situations.jsonl
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from gto_model import FEATURE_COLUMNS


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'training-data')


def label_situation(sit: dict) -> dict:
    """Apply GTO Expert reasoning to label one situation.

    Returns the situation dict with added fields:
        expert_action: FOLD/CHECK/CALL/BET/RAISE
        expert_confidence: HIGH/MEDIUM/LOW
        expert_reasoning: 1-2 sentence explanation
    """
    fd = sit.get('feat_dict', {})

    # Extract key features
    equity = fd.get('raw_equity', 0.0)
    eq_vs_range = fd.get('equity_vs_range', equity)
    eq_margin = fd.get('equity_margin', 0.0)
    pot_odds = fd.get('pot_odds', 0.0)
    spr = fd.get('spr', 10.0)
    is_ip = fd.get('is_ip', 0) > 0.5
    facing_bet = sit.get('facing_bet', False)
    facing_raise = fd.get('facing_raise', 0) > 0.5
    num_callers = fd.get('num_callers_to_bet', 0)
    to_call = fd.get('to_call', 0)

    # Hand strength
    hand_cat = fd.get('hand_category', 0)
    is_made = fd.get('is_made_hand', 0) > 0.5
    is_strong = fd.get('is_strong_made', 0) > 0.5
    is_monster = fd.get('is_monster', 0) > 0.5
    has_flush_draw = fd.get('has_flush_draw', 0) > 0.5
    has_straight_draw = fd.get('has_straight_draw', 0) > 0.5
    draw_outs = fd.get('draw_outs', 0)

    # Range composition
    v_tp_plus = fd.get('villain_top_pair_plus_pct', 0.0)
    v_air = fd.get('villain_air_pct', 0.0)
    v_draw = fd.get('villain_draw_pct', 0.0)
    v_capped = fd.get('villain_range_capped', 0) > 0.5
    board_favour = fd.get('board_favour', 0.0)

    # Board danger
    danger = fd.get('danger_score', 0.0)
    better_pct = fd.get('better_hand_pct', 0.0)
    worse_pct = fd.get('worse_hand_pct', 0.0)

    # Villain aggression context
    v_agg = fd.get('villain_aggression_count', 0)
    v_checked = fd.get('villain_checked_back', 0) > 0.5

    action = None
    confidence = 'MEDIUM'
    reasoning = ''

    # ── FACING BET OR RAISE ──────────────────────────────────────

    if facing_bet:

        # Facing raise = extreme strength signal in multiway
        if facing_raise:
            if is_monster:
                action = 'RAISE'
                confidence = 'HIGH'
                reasoning = f"Monster ({hand_cat}) facing raise — re-raise for value."
            elif is_strong and equity > 0.60:
                action = 'CALL'
                confidence = 'MEDIUM'
                reasoning = f"Strong hand (eq={equity:.2f}) facing raise — call, reassess next street."
            elif draw_outs >= 10 and pot_odds < 0.30:
                action = 'CALL'
                confidence = 'MEDIUM'
                reasoning = f"Big draw ({draw_outs} outs) with pot odds {pot_odds:.2f} — call."
            else:
                action = 'FOLD'
                confidence = 'HIGH'
                reasoning = f"Facing raise in 3-way with eq={equity:.2f} — range is strong, fold."

        # Facing bet with caller(s) behind = bet-and-call, strong signal
        elif num_callers >= 1:
            if is_monster:
                action = 'RAISE'
                confidence = 'HIGH'
                reasoning = f"Monster vs bet+call — raise for value against two ranges."
            elif is_strong and equity > 0.55:
                action = 'CALL'
                confidence = 'MEDIUM'
                reasoning = f"Strong hand vs bet+call (eq={equity:.2f}) — flat, pot control."
            elif draw_outs >= 9 and pot_odds < 0.25:
                action = 'CALL'
                confidence = 'MEDIUM'
                reasoning = f"Draw ({draw_outs} outs) with multiway pot odds — call."
            elif equity < pot_odds + 0.05:
                action = 'FOLD'
                confidence = 'HIGH'
                reasoning = f"Equity {equity:.2f} < pot odds {pot_odds:.2f} vs bet+call — fold."
            else:
                action = 'CALL'
                confidence = 'LOW'
                reasoning = f"Marginal (eq={equity:.2f} vs pot_odds={pot_odds:.2f}) — borderline call."

        # Standard facing bet
        else:
            if is_monster:
                action = 'RAISE'
                confidence = 'HIGH'
                reasoning = f"Monster facing bet — raise for value."
            elif equity > pot_odds + 0.15 and is_strong:
                action = 'RAISE'
                confidence = 'MEDIUM'
                reasoning = f"Strong hand (eq={equity:.2f}) well above pot odds — raise for value."
            elif equity > pot_odds + 0.05:
                if is_made or draw_outs >= 6:
                    action = 'CALL'
                    confidence = 'HIGH'
                    reasoning = f"Equity {equity:.2f} above pot odds {pot_odds:.2f} — call."
                else:
                    action = 'CALL'
                    confidence = 'MEDIUM'
                    reasoning = f"Marginal equity above pot odds — call."
            elif draw_outs >= 9 and pot_odds < 0.28:
                action = 'CALL'
                confidence = 'MEDIUM'
                reasoning = f"Draw with {draw_outs} outs, pot odds {pot_odds:.2f} — draw to improve."
            elif equity < pot_odds - 0.05 and not (draw_outs >= 8):
                action = 'FOLD'
                confidence = 'HIGH'
                reasoning = f"Equity {equity:.2f} below pot odds {pot_odds:.2f}, weak hand — fold."
            else:
                action = 'FOLD'
                confidence = 'MEDIUM'
                reasoning = f"Insufficient equity ({equity:.2f}) vs bet — fold."

    # ── NOT FACING BET (checked to hero) ─────────────────────────

    else:

        # Monster: bet for value
        if is_monster:
            action = 'BET'
            confidence = 'HIGH'
            reasoning = f"Monster hand checked to — bet for value."

        # Strong made hand: usually bet, but check on very dangerous boards
        elif is_strong:
            if danger > 0.7 and not is_ip:
                action = 'CHECK'
                confidence = 'MEDIUM'
                reasoning = f"Strong but danger={danger:.2f} OOP — pot control."
            elif v_tp_plus > 0.40 and not is_ip:
                action = 'CHECK'
                confidence = 'MEDIUM'
                reasoning = f"Strong but villain range heavy (TP+={v_tp_plus:.2f}) OOP — pot control."
            else:
                action = 'BET'
                confidence = 'HIGH'
                reasoning = f"Strong hand (eq={equity:.2f}), checked to — bet for value."

        # Made hand (not strong): position-dependent
        elif is_made:
            if is_ip and v_air > 0.20 and equity > 0.45:
                action = 'BET'
                confidence = 'MEDIUM'
                reasoning = f"Made hand IP, villain has air ({v_air:.2f}) — thin value bet."
            elif is_ip and v_capped and equity > 0.40:
                action = 'BET'
                confidence = 'MEDIUM'
                reasoning = f"Made hand IP vs capped range — bet for thin value."
            elif equity > 0.55 and worse_pct > 0.40:
                action = 'BET'
                confidence = 'MEDIUM'
                reasoning = f"Made hand with {worse_pct:.0%} worse hands — value bet."
            else:
                action = 'CHECK'
                confidence = 'MEDIUM'
                reasoning = f"Made hand but marginal (eq={equity:.2f}) — check, showdown value."

        # Drawing hand: bet as semi-bluff IP, check OOP
        elif draw_outs >= 8:
            if is_ip and v_air > 0.15:
                action = 'BET'
                confidence = 'MEDIUM'
                reasoning = f"Draw ({draw_outs} outs) IP — semi-bluff, fold out villain's air."
            elif is_ip and equity > 0.40:
                action = 'BET'
                confidence = 'LOW'
                reasoning = f"Draw IP with decent equity — semi-bluff."
            else:
                action = 'CHECK'
                confidence = 'HIGH'
                reasoning = f"Draw OOP — check, realize equity."

        # Air: bluff only IP with right conditions
        elif not is_made and draw_outs < 4:
            if is_ip and v_air > 0.30 and board_favour > 0.05 and spr > 3:
                action = 'BET'
                confidence = 'LOW'
                reasoning = f"Air IP, high villain air ({v_air:.2f}), board favours — bluff."
            else:
                action = 'CHECK'
                confidence = 'HIGH'
                reasoning = f"Weak hand 3-way — check, give up."

        # Weak draw (4-7 outs)
        elif draw_outs >= 4:
            action = 'CHECK'
            confidence = 'HIGH'
            reasoning = f"Weak draw ({draw_outs} outs) — check, hope to improve cheaply."

        # Default
        else:
            action = 'CHECK'
            confidence = 'MEDIUM'
            reasoning = f"No clear value or draw — check."

    # Ensure we always have an action
    if action is None:
        action = 'CHECK' if not facing_bet else 'FOLD'
        confidence = 'LOW'
        reasoning = 'Fallback — no rule matched.'

    sit['expert_action'] = action
    sit['expert_confidence'] = confidence
    sit['expert_reasoning'] = reasoning
    return sit


def label_all(input_path: str, output_path: str):
    """Label all situations and write labelled JSONL."""

    situations = []
    with open(input_path) as f:
        for line in f:
            situations.append(json.loads(line))

    print(f"Labelling {len(situations)} situations...")

    labelled = []
    for sit in situations:
        labelled.append(label_situation(sit))

    # Report
    action_counts = {}
    conf_counts = {}
    for s in labelled:
        a = s['expert_action']
        c = s['expert_confidence']
        action_counts[a] = action_counts.get(a, 0) + 1
        conf_counts[c] = conf_counts.get(c, 0) + 1

    total = len(labelled)
    print(f"\n  Labelled: {total}")
    print(f"  Actions: {action_counts}")
    print(f"  Confidence: {conf_counts}")

    low_pct = conf_counts.get('LOW', 0) / total * 100 if total > 0 else 0
    if low_pct > 15:
        print(f"\n  WARNING: LOW confidence is {low_pct:.1f}% (> 15% target).")
        print(f"  Consider regenerating with different seed or more deals.")

    # Agreement with oracle
    agree = sum(1 for s in labelled if s['expert_action'] == s.get('oracle_action', '').upper())
    print(f"  Expert agrees with oracle: {agree}/{total} ({100*agree/total:.1f}%)")

    # Write
    with open(output_path, 'w') as f:
        for s in labelled:
            f.write(json.dumps(s) + '\n')

    print(f"\n  Written to: {output_path}")
    return labelled


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Label 3-way situations')
    parser.add_argument('--input', type=str,
                        default=os.path.join(DATA_DIR, '3way_situations.jsonl'))
    parser.add_argument('--output', type=str,
                        default=os.path.join(DATA_DIR, '3way_labelled.jsonl'))
    args = parser.parse_args()

    label_all(args.input, args.output)
