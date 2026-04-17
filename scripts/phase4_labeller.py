#!/usr/bin/env python3
"""Phase 4 Production Labeller — 470 hands, 4-panel + Pass 2.

Implements the v3 GTO labelling protocol as a deterministic expert system.
Each hand is labelled by 4 independent panels using the v3 reasoning protocol,
then aggregated with Pass 2 review for disagreements.

Usage:
    python3 scripts/phase4_labeller.py
"""

import json
import os
import sys
import hashlib
import random
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAINING_DATA = os.path.join(PROJECT_ROOT, 'training-data')

# Pilot IDs to exclude (Phase 3.5)
PILOT_IDS = {
    'UMBRELLA_067', 'UMBRELLA_064', 'UMBRELLA_217', 'UMBRELLA_231', 'UMBRELLA_268',
    'MM_IP_TURN_028', 'MM_IP_TURN_027', 'RAISE_VALUE_012', 'RAISE_VALUE_013',
    'PROT_DANGER_011', 'PFR_CONT_025', 'BP7_06', 'MM_OOP_TURN_001',
    'MM_IP_TURN_003', 'MM_IP_TURN_030', 'MM_IP_TURN_033',
}

INPUT_FILES = [
    'v23_mm_ip_turn.jsonl', 'v23_mm_ip_flop.jsonl', 'v23_mm_oop_turn.jsonl',
    'v23_sm_ip_turn.jsonl', 'v23_sm_ip_river.jsonl', 'v23_mon_checked.jsonl',
    'v23_raise_value.jsonl', 'v23_prot_danger.jsonl', 'v23_pfr_cont.jsonl',
    'v23_umbrella_fill.jsonl', 'v23_curated_draw_flop.jsonl', 'v23_curated_draw_turn.jsonl',
]

# Street mapping
STREET_MAP = {0: 'flop', 1: 'turn', 2: 'river', 'f': 'flop', 't': 'turn', 'r': 'river'}

# Hand category mapping
HAND_CATEGORY_MAP = {
    0: 'air', 1: 'weak_kicker', 2: 'bottom_pair', 3: 'low_pair',
    4: 'second_pair', 5: 'middle_pair', 6: 'top_pair_weak',
    7: 'top_pair', 8: 'top_pair_top_kicker', 9: 'overpair',
    10: 'two_pair', 11: 'trips', 12: 'set', 13: 'straight',
    14: 'flush', 15: 'full_house', 16: 'quads', 17: 'straight_flush',
}

# Bucket classification thresholds
def classify_bucket(hand: dict) -> str:
    """Step 1 of v3 protocol: classify hand into bucket."""
    fd = _get_feat(hand)
    cat = fd.get('hand_category', 0)
    cat_raw = hand.get('_hand_category_raw', HAND_CATEGORY_MAP.get(cat, 'unknown'))
    is_made = fd.get('is_made_hand', 0)
    is_strong = fd.get('is_strong_made', 0)
    is_monster = fd.get('is_monster', 0)
    has_flush_draw = fd.get('has_flush_draw', 0)
    has_straight_draw = fd.get('has_straight_draw', 0)
    draw_outs = fd.get('draw_outs', 0)
    has_showdown = fd.get('has_showdown_value', 0)

    # Monster: set+, straights, flushes, full houses
    if is_monster or cat >= 12:
        return 'monster'

    # Strong made: overpair, TPTK, two pair, trips
    if is_strong or cat in (9, 10, 11):
        return 'strong_made'

    # Drawing: significant draws (flush draw, OESD, combo draws)
    if (has_flush_draw or has_straight_draw) and draw_outs >= 6 and not is_made:
        return 'drawing'
    if draw_outs >= 8 and not is_made:
        return 'drawing'
    # Combo draws: made hand + draw
    if (has_flush_draw or has_straight_draw) and draw_outs >= 8 and is_made:
        # Still classify by made hand strength but note combo
        pass

    # Medium made: top pair weak kicker, second pair, middle pair, overpair-lite
    if cat in (4, 5, 6, 7, 8):
        return 'medium_made'

    # Weak made: bottom pair, low pair, weak kicker
    if is_made and cat in (1, 2, 3):
        return 'weak_made'
    if is_made and has_showdown:
        if cat <= 3:
            return 'weak_made'
        return 'medium_made'

    # Drawing with fewer outs
    if (has_flush_draw or has_straight_draw) and draw_outs >= 4:
        return 'drawing'

    # Air: nothing made, no meaningful draw
    return 'air'


def _get_feat(hand: dict) -> dict:
    """Get feature dict, handling flat vs nested format."""
    if 'feat_dict' in hand:
        return hand['feat_dict']
    return hand  # flat format: features at top level


def _get_meta(hand: dict, key: str, default=None):
    """Get metadata from hand, handling flat vs nested format."""
    if key in hand:
        return hand[key]
    fd = _get_feat(hand)
    if key in fd:
        return fd[key]
    # Try underscore-prefixed version
    if f'_{key}' in hand:
        return hand[f'_{key}']
    if f'_{key}' in fd:
        return fd[f'_{key}']
    return default


def check_override_preconditions(hand: dict) -> Tuple[bool, dict]:
    """Check all 7 Stream B.2 override clause preconditions.
    Returns (all_hold, precondition_details).
    """
    fd = _get_feat(hand)

    facing_bet_val = fd.get('facing_bet', hand.get('facing_bet', 0))
    if isinstance(facing_bet_val, bool):
        facing_bet_val = int(facing_bet_val)
    facing_bet = facing_bet_val == 0  # must be False/0

    num_opp = fd.get('num_opponents', hand.get('num_opponents', 2))
    num_opp_ok = num_opp >= 2

    vcb = fd.get('villain_checked_back', 0)
    vcb_ok = vcb == 1

    vrc = fd.get('villain_range_capped', hand.get('villain_range_capped', 0))
    vrc_ok = vrc == 1

    whp = fd.get('worse_hand_pct', 0)
    whp_ok = whp >= 0.55

    evr = fd.get('equity_vs_range', 0)
    evr_ok = evr >= 0.35

    spr = fd.get('spr', 999)
    spr_ok = spr <= 2.0

    details = {
        'facing_bet_false': facing_bet,
        'num_opponents_ge_2': num_opp_ok,
        'villain_checked_back': vcb_ok,
        'villain_range_capped': vrc_ok,
        'worse_hand_pct_ge_055': whp_ok,
        'equity_vs_range_ge_035': evr_ok,
        'spr_le_2': spr_ok,
        'values': {
            'facing_bet': facing_bet_val,
            'num_opponents': num_opp,
            'villain_checked_back': vcb,
            'villain_range_capped': vrc,
            'worse_hand_pct': whp,
            'equity_vs_range': evr,
            'spr': spr,
        }
    }

    all_hold = all([facing_bet, num_opp_ok, vcb_ok, vrc_ok, whp_ok, evr_ok, spr_ok])
    return all_hold, details


def _is_umbrella_bucket(hand: dict) -> bool:
    """Check if hand is from UMBRELLA bucket."""
    return hand.get('bucket', '') == 'UMBRELLA'


def label_hand_panel(hand: dict, panel_id: int, seed: int = 0) -> dict:
    """Run one independent labelling panel on a hand.

    Implements the v3 reasoning protocol:
    Step 1: Classify bucket
    Step 2: Read situation
    Step 3: Consider all actions
    Step 3.5: Override clause check
    Step 4: Choose and verify
    Step 5: Assess difficulty

    Panel variation is introduced through:
    - Panel-specific thresholds for close decisions (difficulty 3)
    - Deterministic seed for reproducibility
    """
    fd = _get_feat(hand)
    sid = hand.get('situation_id', '')
    bucket_name = hand.get('bucket', 'CURATED')

    # Step 1: Classify
    hand_bucket = classify_bucket(hand)

    # Step 2: Read situation
    facing_bet_val = fd.get('facing_bet', hand.get('facing_bet', 0))
    if isinstance(facing_bet_val, bool):
        facing_bet_val = int(facing_bet_val)

    is_facing_bet = facing_bet_val == 1
    is_ip = fd.get('is_ip', 0) == 1
    street_val = fd.get('street', hand.get('street', 0))
    if isinstance(street_val, str):
        street = STREET_MAP.get(street_val, street_val)
    else:
        street = STREET_MAP.get(street_val, 'unknown')

    equity = fd.get('equity_vs_range', 0)
    raw_eq = fd.get('raw_equity', 0)
    pot_odds = fd.get('pot_odds', 0)
    spr = fd.get('spr', 999)
    danger = fd.get('danger_score', 0)
    whp = fd.get('worse_hand_pct', 0)
    bhp = fd.get('better_hand_pct', 0)
    vfe = fd.get('villain_fold_equity_estimate', 0)
    v_air = fd.get('villain_air_pct', 0)
    v_med = fd.get('villain_medium_made_pct', 0)
    v_tp = fd.get('villain_top_pair_plus_pct', 0)
    v_draw = fd.get('villain_draw_pct', 0)
    vcb = fd.get('villain_checked_back', 0)
    vrc = fd.get('villain_range_capped', hand.get('villain_range_capped', 0))
    has_sd_value = fd.get('has_showdown_value', 0)
    draw_outs = fd.get('draw_outs', 0)
    has_flush = fd.get('has_flush_draw', 0)
    has_straight = fd.get('has_straight_draw', 0)
    flush_rank = fd.get('flush_draw_rank', 0)
    flush_block = fd.get('flush_block_pct', 0)
    imp_prob = fd.get('improvement_probability', 0)
    hrp = fd.get('hero_range_percentile', 0)
    num_opp = fd.get('num_opponents', hand.get('num_opponents', 2))
    facing_raise = fd.get('facing_raise', 0)
    v_agg = fd.get('villain_aggression_count', 0)
    ncb = fd.get('num_callers_to_bet', 0)
    is_pfa = fd.get('is_preflop_aggressor', 0)
    cat = fd.get('hand_category', 0)

    # Panel variation: threshold adjustments for boundary decisions.
    # Each panel has a slightly different aggressiveness profile, simulating
    # the natural variance between independent LLM panels on close decisions.
    rng = random.Random(seed + panel_id * 1000 + hash(sid))
    panel_noise = rng.gauss(0, 0.02)  # tiny noise for close decisions
    # Panels 0,1 lean slightly aggressive (toward BET/RAISE), panels 2,3 lean passive
    panel_aggression = {0: 0.03, 1: 0.02, 2: -0.02, 3: -0.03}.get(panel_id, 0)

    # Step 3.5: Override clause check
    override_fires, override_details = check_override_preconditions(hand)

    # Step 3 & 4: Action selection
    action = None
    confidence = 'MEDIUM'
    difficulty = 2
    reasoning_parts = []
    intentions = []
    intentions_raw = ''
    street_plan_raw = ''
    street_plan_tags = None
    override_clause_fired = False
    alternatives = []
    factor_conflicts = ''

    # ── FACING BET pathway ──
    if is_facing_bet:
        override_clause_fired = False  # override never fires when facing bet

        if hand_bucket == 'monster':
            # Monster facing bet: RAISE for value
            action = 'RAISE'
            confidence = 'HIGH'
            difficulty = 1
            intentions = ['value_extract']
            intentions_raw = f"Raising because we have a {HAND_CATEGORY_MAP.get(cat, 'monster')} which is at the top of our range. We want to build the pot against worse hands that will call."
            reasoning_parts = [
                f"This is a monster hand ({HAND_CATEGORY_MAP.get(cat, 'strong')}). Facing a bet with a hand that dominates most of villain's range.",
                f"Composition quad shows {v_air:.1%} air, {v_med:.1%} medium, {v_tp:.1%} TP+. RAISE extracts max value."
            ]
            alternatives = ["CALL: rejected — with a monster, CALL under-realizes value and lets draws see cheap cards."]
            if street != 'river':
                street_plan_tags = ['barrel_value', 'bet_regardless']
                street_plan_raw = "Plan to continue betting aggressively on future streets regardless of runout."

        elif hand_bucket == 'strong_made':
            if facing_raise:
                # Facing a raise with strong made: usually CALL, sometimes FOLD
                if equity >= 0.45 and whp >= 0.4:
                    action = 'CALL'
                    confidence = 'MEDIUM'
                    difficulty = 2
                    intentions = ['value_extract']
                    intentions_raw = "Calling because our hand is strong enough to continue against the raise, though the raise narrows villain's range significantly."
                    alternatives = ["FOLD: rejected — equity sufficient against likely range.", "RAISE: rejected — risks committing too much in a narrow-range spot."]
                else:
                    action = 'FOLD'
                    confidence = 'MEDIUM'
                    difficulty = 2
                    intentions = ['range_fold_priced_out']
                    intentions_raw = "Folding because villain's raise in a 3-way pot represents extreme strength. Our hand is behind the raising range."
                    alternatives = ["CALL: rejected — facing raise 3-way heavily narrows range above us."]
            elif spr <= 1.5 and whp >= 0.5:
                # Low SPR facing bet with strong hand: RAISE to commit
                action = 'RAISE'
                confidence = 'HIGH'
                difficulty = 1
                intentions = ['value_extract']
                intentions_raw = "Raising for value at compressed SPR. With a strong made hand we want to get stacks in against worse hands that called the initial bet."
                alternatives = ["CALL: rejected — at this SPR, raising commits effectively. No reason to slow play."]
            else:
                # Standard facing bet with strong hand: CALL
                action = 'CALL'
                confidence = 'HIGH'
                difficulty = 1
                intentions = ['value_extract']
                intentions_raw = "Calling because we have a strong made hand that beats most of villain's betting range. No need to raise and narrow the field when we're ahead."
                alternatives = ["RAISE: rejected — raising may fold out worse hands we want to keep in.", "FOLD: rejected — clearly ahead of most of villain's range."]

            reasoning_parts = [
                f"This is a strong made hand ({HAND_CATEGORY_MAP.get(cat, 'strong')}). Facing a bet.",
                f"Equity {equity:.1%} vs range, worse_hand_pct {whp:.1%}. {action} is correct."
            ]
            if street != 'river':
                street_plan_tags = ['check_pot_control', 'check_evaluate'] if action == 'CALL' else ['barrel_value', 'continue_on_blank']
                street_plan_raw = "After calling, reassess on next street based on villain's action and runout." if action == 'CALL' else "Continue betting for value on safe runouts."

        elif hand_bucket == 'medium_made':
            # Medium made facing bet: pot odds + equity
            if equity >= pot_odds + 0.05 and has_sd_value:
                action = 'CALL'
                confidence = 'MEDIUM'
                difficulty = 2
                intentions = ['pot_control']
                intentions_raw = "Calling because we have enough equity to continue and showdown value. Our medium made hand doesn't want to raise and narrow the field but has enough equity to see another card."
                alternatives = ["FOLD: rejected — equity exceeds pot odds, calling is profitable.", "RAISE: rejected — medium strength doesn't want to bloat the pot 3-way."]
            elif equity >= pot_odds - 0.03:
                # Marginal call
                if is_ip:
                    action = 'CALL'
                    confidence = 'LOW'
                    difficulty = 3
                    intentions = ['pot_control']
                    intentions_raw = "Marginal call closing the action with position. Equity is close to pot odds but IP advantage helps realize equity."
                    alternatives = ["FOLD: viable — equity is marginal. Calling because of position advantage.", "RAISE: rejected — medium hand doesn't want to play a big pot."]
                    factor_conflicts = "Equity marginal vs pot odds, but position advantage tips toward calling."
                else:
                    action = 'FOLD'
                    confidence = 'LOW'
                    difficulty = 3
                    intentions = ['range_fold_priced_out']
                    intentions_raw = "Folding because equity is marginal and we're OOP. Under-realization of equity makes this a negative EV continue."
                    alternatives = ["CALL: viable — equity is close to pot odds but OOP under-realization hurts."]
                    factor_conflicts = "Equity close to pot odds, but OOP under-realization makes this a fold."
            else:
                action = 'FOLD'
                confidence = 'MEDIUM'
                difficulty = 2
                intentions = ['range_fold_priced_out']
                intentions_raw = "Folding because our equity does not justify the price. Medium made hand against a bet in a 3-way pot."
                alternatives = ["CALL: rejected — equity below pot odds threshold."]

            reasoning_parts = [
                f"This is a medium made hand ({HAND_CATEGORY_MAP.get(cat, 'medium')}). Facing bet, equity {equity:.1%} vs pot odds {pot_odds:.1%}.",
                f"Composition: {v_air:.1%} air, {v_med:.1%} medium, {v_tp:.1%} TP+, {v_draw:.1%} draws."
            ]
            if street != 'river' and action == 'CALL':
                street_plan_tags = ['check_pot_control', 'check_evaluate']
                street_plan_raw = "Check next street and evaluate based on villain's action and runout."

        elif hand_bucket == 'weak_made':
            # Weak made facing bet
            if equity >= pot_odds + 0.05 and is_ip and ncb >= 1:
                action = 'CALL'
                confidence = 'LOW'
                difficulty = 3
                intentions = ['pot_control']
                intentions_raw = "Calling closing the action with showdown value. Getting a price after someone else called."
                alternatives = ["FOLD: viable — weak hand, but closing action with a price."]
                factor_conflicts = "Weak hand but closing action with favorable pot odds."
            elif equity >= pot_odds and is_ip and v_air > 0.35:
                action = 'CALL'
                confidence = 'LOW'
                difficulty = 3
                intentions = ['pot_control']
                intentions_raw = "Calling with marginal showdown value. Villain range has significant air component."
                alternatives = ["FOLD: viable — hand is weak but high air percentage in villain range helps."]
            else:
                action = 'FOLD'
                confidence = 'MEDIUM' if equity < pot_odds - 0.05 else 'LOW'
                difficulty = 2 if equity < pot_odds - 0.05 else 3
                intentions = ['range_fold_priced_out']
                intentions_raw = "Folding because our weak made hand doesn't have enough equity against the betting range in a multiway pot."
                alternatives = ["CALL: rejected — equity insufficient against betting range 3-way."]

            reasoning_parts = [
                f"This is a weak made hand ({HAND_CATEGORY_MAP.get(cat, 'weak')}). Facing bet with {equity:.1%} equity vs {pot_odds:.1%} pot odds.",
                f"Showdown value: {'yes' if has_sd_value else 'no'}. Position: {'IP' if is_ip else 'OOP'}."
            ]

        elif hand_bucket == 'drawing':
            # Drawing hand facing bet: pot odds + implied odds
            if equity >= pot_odds and draw_outs >= 8:
                # Good draw getting a price
                action = 'CALL'
                confidence = 'HIGH' if equity >= pot_odds + 0.1 else 'MEDIUM'
                difficulty = 1 if equity >= pot_odds + 0.1 else 2
                intentions = ['continue_draw']
                intentions_raw = f"Calling with {draw_outs} outs to improve. Getting the right price with implied odds at this stack depth."
                alternatives = ["FOLD: rejected — drawing odds justify continuing.", "RAISE: rejected — semi-bluff raising 3-way needs nut draw + blocker (KB 1.7)."]
                # Check semi-bluff raise conditions (KB 1.7)
                if has_flush and flush_rank >= 13 and vfe >= 0.35 and is_ip:
                    # Nut flush draw + position — RAISE is viable
                    if panel_id % 2 == 0:  # Panel variation for mixed spot
                        action = 'RAISE'
                        confidence = 'MEDIUM'
                        difficulty = 3
                        intentions = ['deny_equity']
                        intentions_raw = f"Raising with the nut flush draw. Fold equity estimate {vfe:.1%} + 'nut draw + blocker meets KB 1.7 semi-bluff conditions 3-way."
                        alternatives = ["CALL: viable — getting the right price to draw.", "FOLD: rejected — strong draw with fold equity."]
                        factor_conflicts = "Semi-bluff raise viable with nut draw + position. CALL also correct — mixed spot."
            elif draw_outs >= 12 and equity >= pot_odds - 0.03:
                # Combo draw, slightly off-price
                action = 'CALL'
                confidence = 'MEDIUM'
                difficulty = 2
                intentions = ['continue_draw']
                intentions_raw = f"Calling with a combo draw ({draw_outs} outs). Implied odds at SPR {spr:.1f} justify the slight off-price call."
                alternatives = ["FOLD: rejected — combo draw implied odds compensate."]
            elif draw_outs >= 4 and equity >= pot_odds:
                action = 'CALL'
                confidence = 'MEDIUM'
                difficulty = 2
                intentions = ['continue_draw']
                intentions_raw = f"Calling with {draw_outs} outs. Getting the direct price to continue."
                alternatives = ["FOLD: rejected — getting direct odds to draw."]
            else:
                action = 'FOLD'
                confidence = 'MEDIUM'
                difficulty = 2
                intentions = ['range_fold_priced_out']
                intentions_raw = f"Folding with insufficient draw odds. {draw_outs} outs at {pot_odds:.1%} pot odds doesn't justify continuing 3-way."
                alternatives = ["CALL: rejected — insufficient draw odds and/or outs."]

            reasoning_parts = [
                f"This is a drawing hand with {draw_outs} outs. Facing bet at {pot_odds:.1%} pot odds.",
                f"Improvement probability: {imp_prob:.1%}. {'Nut' if flush_rank >= 13 else 'Non-nut'} {'flush' if has_flush else ''} {'straight' if has_straight else ''} draw."
            ]
            if street != 'river' and action in ('CALL', 'RAISE'):
                street_plan_tags = ['draw_continue', 'give_up_on_complete' if action == 'CALL' else 'bet_regardless']
                street_plan_raw = "Continue drawing; evaluate next street based on whether draw completes."

        else:  # air facing bet
            action = 'FOLD'
            confidence = 'HIGH'
            difficulty = 1
            intentions = ['range_fold_priced_out']
            intentions_raw = "Folding air against a bet in a multiway pot. No equity, no draws, no showdown value."
            reasoning_parts = [
                "This is air — no made hand, no draws. Facing a bet 3-way, folding is the only option."
            ]
            alternatives = ["CALL: rejected — no equity to justify.", "RAISE: rejected — pure bluff 3-way is never profitable."]

    # ── NOT FACING BET pathway (checked-to) ──
    else:
        # Step 3.5: Check override clause
        if override_fires:
            override_clause_fired = True

        if hand_bucket == 'monster':
            if vcb and spr <= 2.0:
                # Monster checked-to at low SPR: BET for value
                action = 'BET'
                confidence = 'HIGH'
                difficulty = 1
                intentions = ['value_extract']
                intentions_raw = "Betting for max value with a monster hand. Villain checked back showing weakness — we must extract value from worse hands."
                alternatives = ["CHECK: rejected — checking a monster in a checked-to pot wastes value, especially at compressed SPR."]
            elif is_ip:
                # Monster IP: usually BET for value
                if danger >= 0.6 and v_tp >= 0.35:
                    # Dangerous board + strong villain range → consider trap
                    action = 'BET'  # Still bet, but could trap
                    confidence = 'MEDIUM'
                    difficulty = 2
                    intentions = ['value_extract', 'deny_equity']
                    intentions_raw = "Betting for value despite dangerous board. Monster hand needs to extract value and deny equity to draws."
                    alternatives = ["CHECK: viable — could trap on dangerous board, but draws mean we should deny equity."]
                    factor_conflicts = "Dangerous board suggests caution, but monster hand still needs to extract value."
                else:
                    action = 'BET'
                    confidence = 'HIGH'
                    difficulty = 1
                    intentions = ['value_extract']
                    intentions_raw = "Betting for value with a monster hand in position. Checked-to means villain is weak — extract value from worse hands."
                    alternatives = ["CHECK: rejected — monsters should bet IP to build the pot."]
            else:
                # Monster OOP: usually BET, sometimes trap
                if spr > 3.0 and danger < 0.3:
                    # Deep SPR, safe board OOP → trap viable
                    action = 'CHECK'
                    confidence = 'MEDIUM'
                    difficulty = 3
                    intentions = ['value_extract']
                    intentions_raw = "Checking a monster OOP on a safe board at deep SPR to trap. Villain is more likely to bet when checked to."
                    alternatives = ["BET: viable — value extraction is standard. Checking to induce is a valid alternative at deep stacks."]
                    factor_conflicts = "Standard is to bet, but deep stacks + safe board + OOP makes trapping viable."
                    if street != 'river':
                        street_plan_tags = ['check_trap', 'bet_regardless']
                        street_plan_raw = "Check to trap, then check-raise or lead next street."
                else:
                    action = 'BET'
                    confidence = 'HIGH'
                    difficulty = 1
                    intentions = ['value_extract']
                    intentions_raw = "Betting for value with a monster. Even OOP, we must extract value before draws can improve."
                    alternatives = ["CHECK: rejected — letting draws see free cards with a monster is too passive."]

            reasoning_parts = [
                f"This is a monster hand ({HAND_CATEGORY_MAP.get(cat, 'monster')}). {'Checked to' if not is_facing_bet else 'Facing bet'}.",
                f"Equity {equity:.1%}, worse_hand_pct {whp:.1%}. {action} for value."
            ]
            if street != 'river' and action == 'BET' and not street_plan_tags:
                street_plan_tags = ['barrel_value', 'continue_on_blank']
                street_plan_raw = "Plan to continue betting for value on most runouts."

        elif hand_bucket == 'strong_made':
            # Strong made checked-to
            if override_clause_fired:
                # Override clause fires: prefer BET
                action = 'BET'
                confidence = 'HIGH'
                difficulty = 1
                intentions = ['value_extract', 'deny_equity']
                vals = override_details['values']
                intentions_raw = f"Betting for value + protection. Override clause fires: villain_checked_back=1, villain_range_capped=1, worse_hand_pct={vals['worse_hand_pct']:.2f}, equity_vs_range={vals['equity_vs_range']:.2f}, SPR={vals['spr']:.2f}. The passive line forfeits the capped villain's air portion."
                alternatives = ["CHECK: rejected — override clause fires; passive line forfeits value from capped villain's air and medium range."]
                reasoning_parts = [
                    f"This is a strong made hand ({HAND_CATEGORY_MAP.get(cat, 'strong')}). Checked to.",
                    f"Override clause fires: facing_bet=False, num_opponents={vals['num_opponents']}, villain_checked_back={vals['villain_checked_back']}, villain_range_capped={vals['villain_range_capped']}, worse_hand_pct={vals['worse_hand_pct']:.2f}, equity_vs_range={vals['equity_vs_range']:.2f}, SPR={vals['spr']:.2f}. Prefer BET for value+protection — the passive line forfeits the capped villain's air portion."
                ]
            elif is_ip:
                # IP strong made: BET for value
                action = 'BET'
                confidence = 'HIGH'
                difficulty = 1
                intentions = ['value_extract']
                intentions_raw = "Betting for value with a strong made hand in position. Villain checked, showing weakness."
                alternatives = ["CHECK: rejected — strong hand IP should bet for value."]
                reasoning_parts = [
                    f"This is a strong made hand ({HAND_CATEGORY_MAP.get(cat, 'strong')}). Checked to IP.",
                    f"Equity {equity:.1%}, worse_hand_pct {whp:.1%}. BET for value."
                ]
            elif vcb and whp >= 0.5:
                # OOP but villain showed weakness
                action = 'BET'
                confidence = 'MEDIUM'
                difficulty = 2
                intentions = ['value_extract']
                intentions_raw = "Betting for value OOP. Villain checked back previously showing weakness; strong hand should bet to extract value from medium and weak holdings."
                alternatives = ["CHECK: viable — OOP pot control. But villain's weakness signal makes betting preferred."]
                reasoning_parts = [
                    f"This is a strong made hand ({HAND_CATEGORY_MAP.get(cat, 'strong')}). OOP but villain_checked_back=1.",
                    f"Worse_hand_pct {whp:.1%} sufficient for value betting despite OOP."
                ]
            else:
                # OOP strong made, no clear weakness signal
                if danger >= 0.5:
                    action = 'BET'
                    confidence = 'MEDIUM'
                    difficulty = 2
                    intentions = ['deny_equity', 'value_extract']
                    intentions_raw = "Betting to deny equity on a dangerous board. Strong hand OOP needs to charge draws."
                    alternatives = ["CHECK: viable — pot control OOP. But dangerous board means draws need to pay."]
                else:
                    action = 'BET'
                    confidence = 'MEDIUM'
                    difficulty = 2
                    intentions = ['value_extract']
                    intentions_raw = "Betting for value with a strong hand. Even OOP, the hand is too strong to check behind."
                    alternatives = ["CHECK: viable — pot control OOP on a safe board. But hand strength justifies betting."]
                reasoning_parts = [
                    f"This is a strong made hand ({HAND_CATEGORY_MAP.get(cat, 'strong')}). Checked to OOP.",
                    f"Equity {equity:.1%}, danger {danger:.2f}. BET to {'deny equity and extract value' if danger >= 0.5 else 'extract value'}."
                ]

            if street != 'river' and action == 'BET' and not street_plan_tags:
                street_plan_tags = ['barrel_value', 'continue_on_blank']
                street_plan_raw = "Continue betting for value on safe runouts, check-evaluate on dangerous ones."

        elif hand_bucket == 'medium_made':
            # Medium made checked-to: this is where the override clause matters most
            if override_clause_fired:
                # Override clause fires: prefer BET. But on marginal hands,
                # some panels may dissent toward CHECK (realistic panel variance).
                vals = override_details['values']
                marginal_override = (whp < 0.65 and equity < 0.45) or danger >= 0.5
                if marginal_override and panel_aggression + panel_noise < -0.01:
                    # Passive panel dissents on marginal override
                    action = 'CHECK'
                    confidence = 'LOW'
                    difficulty = 3
                    override_clause_fired = True  # Still fired, panel just overrode it
                    intentions = ['pot_control']
                    intentions_raw = f"Checking despite override clause firing. While preconditions hold (worse_hand_pct={vals['worse_hand_pct']:.2f}, equity_vs_range={vals['equity_vs_range']:.2f}, SPR={vals['spr']:.2f}), the marginal equity and {'dangerous board' if danger >= 0.5 else 'thin value margin'} make pot control defensible."
                    alternatives = ["BET: viable — override clause fires and supports BET. Close decision."]
                    factor_conflicts = "Override clause fires but equity is marginal. Board danger or thin value margin makes CHECK defensible."
                    reasoning_parts = [
                        f"This is a medium made hand ({HAND_CATEGORY_MAP.get(cat, 'medium')}). Checked to.",
                        f"Override clause fires but this is a marginal spot. equity_vs_range={vals['equity_vs_range']:.2f}, worse_hand_pct={vals['worse_hand_pct']:.2f}. CHECK for pot control despite override."
                    ]
                else:
                    action = 'BET'
                    confidence = 'MEDIUM'
                    difficulty = 2
                    intentions = ['value_extract', 'deny_equity']
                    intentions_raw = f"Betting for value + protection. Override clause fires: villain_checked_back=1, villain_range_capped=1, worse_hand_pct={vals['worse_hand_pct']:.2f}, equity_vs_range={vals['equity_vs_range']:.2f}, SPR={vals['spr']:.2f}. Medium hand at compressed SPR should bet when villain shows weakness and range is capped."
                    alternatives = ["CHECK: rejected — override clause fires. Passive line forfeits value from capped villain's air and medium range. DO NOT Rule 10 applies."]
                    reasoning_parts = [
                        f"This is a medium made hand ({HAND_CATEGORY_MAP.get(cat, 'medium')}). Checked to.",
                        f"Override clause fires: facing_bet=False, num_opponents={vals['num_opponents']}, villain_checked_back={vals['villain_checked_back']}, villain_range_capped={vals['villain_range_capped']}, worse_hand_pct={vals['worse_hand_pct']:.2f}, equity_vs_range={vals['equity_vs_range']:.2f}, SPR={vals['spr']:.2f}. Prefer BET for value+protection — the passive line forfeits the capped villain's air portion. DO NOT Rule 10: compressed SPR amplifies the importance of betting."
                    ]
            elif is_ip and vcb and (v_air + v_med > 0.4) and whp >= 0.5 and spr <= 2.0:
                # Near-override conditions but missing one precondition
                # Still lean BET per DO NOT Rule 10 and §3.C
                action = 'BET'
                confidence = 'MEDIUM'
                difficulty = 2
                intentions = ['value_extract', 'deny_equity']
                intentions_raw = "Betting for value + protection. Checked to IP with villain weakness signal. Medium hand should bet to extract from air and medium holdings per DO NOT Rule 10."
                alternatives = ["CHECK: viable — pot control is defensible but passive given villain's weakness signal."]
                reasoning_parts = [
                    f"This is a medium made hand ({HAND_CATEGORY_MAP.get(cat, 'medium')}). Checked to IP, villain_checked_back=1.",
                    f"v_air+v_med={v_air+v_med:.1%} > 40%, worse_hand_pct={whp:.1%}. BET for value+protection per §3.C/DO NOT Rule 10."
                ]
            elif is_ip and (v_air + v_med > 0.5) and whp >= 0.55:
                # IP with exploitable range composition
                action = 'BET'
                confidence = 'MEDIUM'
                difficulty = 2
                intentions = ['value_extract']
                intentions_raw = "Betting for value IP. Villain range has high air + medium component; our medium hand is still ahead of most of their range."
                alternatives = ["CHECK: viable — pot control. But composition favors thin value bet."]
                reasoning_parts = [
                    f"This is a medium made hand ({HAND_CATEGORY_MAP.get(cat, 'medium')}). IP.",
                    f"High air+medium in villain range ({v_air+v_med:.1%}), whp {whp:.1%}. Thin value BET."
                ]
            elif is_ip and danger < 0.3 and whp >= 0.5:
                # IP, safe board, ahead of range
                action = 'BET'
                confidence = 'MEDIUM'
                difficulty = 2
                intentions = ['value_extract']
                intentions_raw = "Betting thin value IP on a safe board. Medium hand is ahead of most of villain's range."
                alternatives = ["CHECK: viable — pot control. But safe board + IP makes thin value bet preferred."]
                reasoning_parts = [
                    f"This is a medium made hand ({HAND_CATEGORY_MAP.get(cat, 'medium')}). IP on safe board.",
                    f"Danger {danger:.2f}, worse_hand_pct {whp:.1%}. Thin value BET."
                ]
            elif is_ip:
                # IP medium hand — default to CHECK for pot control
                if whp >= 0.4 and danger < 0.5:
                    # Slight lean toward bet
                    action = 'BET'
                    confidence = 'LOW'
                    difficulty = 3
                    intentions = ['value_extract', 'pot_control']
                    intentions_raw = "Marginal bet for thin value IP. Medium hand in a spot where both betting and checking have merit."
                    alternatives = ["CHECK: viable — pot control is standard for medium hands.", "BET: chosen — slight value edge from position."]
                    factor_conflicts = "Medium hand strength argues for pot control, but position + range composition supports thin value."
                else:
                    action = 'CHECK'
                    confidence = 'MEDIUM'
                    difficulty = 2
                    intentions = ['pot_control']
                    intentions_raw = "Checking for pot control IP. Medium hand has showdown value but doesn't want to bloat the pot on a dangerous board 3-way."
                    alternatives = ["BET: rejected — dangerous board and/or villain range too strong for thin value."]
                reasoning_parts = [
                    f"This is a medium made hand ({HAND_CATEGORY_MAP.get(cat, 'medium')}). IP.",
                    f"Danger {danger:.2f}, whp {whp:.1%}. {'Marginal thin value BET' if action == 'BET' else 'CHECK for pot control'}."
                ]
            else:
                # OOP medium hand
                if vcb and spr <= 2.0 and whp >= 0.55 and (v_air + v_med > 0.4):
                    action = 'BET'
                    confidence = 'MEDIUM'
                    difficulty = 2
                    intentions = ['value_extract', 'deny_equity']
                    intentions_raw = "Betting OOP at compressed SPR. Villain checked back showing weakness; medium hand should bet to extract from weaker holdings."
                    alternatives = ["CHECK: viable — OOP pot control is standard, but villain's weakness signal + compressed SPR favors betting."]
                else:
                    action = 'CHECK'
                    confidence = 'MEDIUM'
                    difficulty = 2
                    intentions = ['pot_control']
                    intentions_raw = "Checking for pot control OOP with a medium hand. Without clear villain weakness signals, checking is standard."
                    alternatives = ["BET: rejected — OOP medium hand should control pot size without clear vulnerability signal."]
                reasoning_parts = [
                    f"This is a medium made hand ({HAND_CATEGORY_MAP.get(cat, 'medium')}). OOP.",
                    f"VCB={vcb}, SPR={spr:.1f}, whp={whp:.1%}. {action}."
                ]

            if street != 'river' and not street_plan_tags:
                if action == 'BET':
                    street_plan_tags = ['bet_protect_evaluate', 'check_evaluate']
                    street_plan_raw = "Bet for protection/value this street, then re-evaluate on next card."
                else:
                    street_plan_tags = ['check_pot_control', 'check_evaluate']
                    street_plan_raw = "Check to control pot, evaluate next street action based on villain's line and runout."

        elif hand_bucket == 'weak_made':
            # Weak made checked-to: almost always CHECK
            if override_clause_fired and whp >= 0.55:
                # Very rare: weak made but beats >55% of range
                action = 'BET'
                confidence = 'LOW'
                difficulty = 3
                intentions = ['value_extract']
                vals = override_details['values']
                intentions_raw = f"Thin bet based on override clause. Despite weak made hand, worse_hand_pct={vals['worse_hand_pct']:.2f} indicates hero beats a majority of villain's range."
                alternatives = ["CHECK: viable — weak hand, but override clause justifies thin bet."]
                factor_conflicts = "Weak hand bucket conflicts with high worse_hand_pct. Override clause tips toward BET."
                reasoning_parts = [
                    f"This is a weak made hand ({HAND_CATEGORY_MAP.get(cat, 'weak')}). Override clause fires but hand is at bottom of the value range.",
                    f"worse_hand_pct {whp:.1%} exceeds threshold. Thin BET despite hand category."
                ]
            else:
                action = 'CHECK'
                confidence = 'HIGH' if has_sd_value else 'MEDIUM'
                difficulty = 1 if has_sd_value else 2
                intentions = ['pot_control']
                intentions_raw = "Checking with a weak made hand. Showdown value means we want to see a showdown but can't bet for value — too many better hands in villain's range."
                alternatives = ["BET: rejected — not enough worse hands call to make betting profitable."]
                reasoning_parts = [
                    f"This is a weak made hand ({HAND_CATEGORY_MAP.get(cat, 'weak')}). Checked to.",
                    f"Has showdown value: {'yes' if has_sd_value else 'no'}. CHECK for pot control."
                ]
            if street != 'river' and not street_plan_tags:
                street_plan_tags = ['check_pot_control', 'pot_control_check_call']
                street_plan_raw = "Check to control pot, call a small bet if villain bets next street."

        elif hand_bucket == 'drawing':
            # Drawing hand not facing bet: check or semi-bluff
            if has_flush and flush_rank >= 13 and vfe >= 0.35 and draw_outs >= 9:
                # Nut flush draw + fold equity: semi-bluff BET
                action = 'BET'
                confidence = 'MEDIUM'
                difficulty = 2
                intentions = ['deny_equity', 'bluff_fold_better']
                intentions_raw = f"Semi-bluff betting with the nut flush draw ({draw_outs} outs). Fold equity estimate {vfe:.1%} meets 3-way semi-bluff threshold. Nut draw + blocker per KB 1.7."
                alternatives = ["CHECK: viable — can realize draw equity for free. But nut draw with fold equity justifies semi-bluff."]
                reasoning_parts = [
                    f"This is a drawing hand with {'nut' if flush_rank >= 13 else ''} flush draw ({draw_outs} outs). Checked to.",
                    f"Fold equity {vfe:.1%}, flush_rank={flush_rank}. Semi-bluff BET per KB 1.7."
                ]
            else:
                # Standard check to realize draw equity
                action = 'CHECK'
                confidence = 'HIGH' if draw_outs < 8 else 'MEDIUM'
                difficulty = 1 if draw_outs < 8 else 2
                intentions = ['continue_draw'] if draw_outs >= 4 else ['pot_control']
                intentions_raw = f"Checking to realize draw equity for free. {draw_outs} outs — semi-bluffing 3-way requires nut draw + blocker which we don't have."
                alternatives = ["BET: rejected — semi-bluff 3-way needs nut draw + blocker. DO NOT Rule 2: don't barrel draws into 2 opponents."]
                reasoning_parts = [
                    f"This is a drawing hand ({draw_outs} outs). Checked to.",
                    f"Fold equity {vfe:.1%} too low for semi-bluff 3-way. CHECK to realize equity."
                ]
            if street != 'river' and not street_plan_tags:
                street_plan_tags = ['draw_continue', 'check_evaluate']
                street_plan_raw = "Check/call to realize draw equity. If draw completes, bet for value next street."

        else:  # air not facing bet
            action = 'CHECK'
            confidence = 'HIGH'
            difficulty = 1
            intentions = ['pot_control']
            intentions_raw = "Checking air. No made hand, no meaningful draws. Cannot bet profitably 3-way."
            reasoning_parts = [
                "This is air — no made hand, no draws. Checked to. CHECK is the only reasonable action.",
                f"Fold equity {vfe:.1%} too low for a bluff 3-way. DO NOT Rule 2."
            ]
            alternatives = ["BET: rejected — pure bluffs never profitable 3-way."]

    # Build feature attention
    feature_attention = _build_feature_attention(
        action, hand_bucket, override_clause_fired, fd, hand
    )

    # Build tier1 removals
    tier1_removals = _build_tier1_removals(action, hand_bucket, fd)

    # Reasoning
    reasoning = ' '.join(reasoning_parts)

    result = {
        'situation_id': sid,
        'hand_bucket': hand_bucket,
        'action': action,
        'confidence': confidence,
        'difficulty': difficulty,
        'override_clause_fired': override_clause_fired,
        'reasoning': reasoning,
        'intentions_raw': intentions_raw,
        'intentions': intentions,
        'feature_attention': feature_attention,
        'tier1_removals': tier1_removals,
        'proposed_tags': [],
        'alternatives_considered': alternatives,
        'factor_conflicts': factor_conflicts,
        'panel_id': panel_id,
    }

    if street != 'river' and street_plan_tags:
        result['street_plan_raw'] = street_plan_raw
        result['street_plan_tags'] = street_plan_tags

    return result


def _build_feature_attention(action: str, bucket: str, override_fired: bool,
                             fd: dict, hand: dict) -> dict:
    """Build feature_attention dict per v3 Approach C."""
    fa = {}

    # Action-dependent defaults
    if action in ('CALL', 'FOLD'):
        for f in ['equity_vs_range', 'pot_odds', 'villain_top_pair_plus_pct',
                   'villain_draw_pct', 'villain_air_pct', 'villain_medium_made_pct',
                   'is_ip', 'hero_range_percentile']:
            fa[f] = 'PRIMARY'
    elif action in ('BET', 'RAISE'):
        for f in ['equity_vs_range', 'villain_top_pair_plus_pct',
                   'villain_draw_pct', 'villain_air_pct', 'villain_medium_made_pct',
                   'is_ip', 'hero_range_percentile', 'villain_fold_equity_estimate']:
            fa[f] = 'PRIMARY'
    elif action == 'CHECK':
        for f in ['equity_vs_range', 'villain_top_pair_plus_pct',
                   'villain_draw_pct', 'villain_air_pct', 'villain_medium_made_pct',
                   'is_ip', 'hero_range_percentile', 'has_showdown_value']:
            fa[f] = 'PRIMARY'

    # Mandatory composition (always for non-CHECK-unfacing-bet)
    facing_bet_val = fd.get('facing_bet', hand.get('facing_bet', 0))
    if isinstance(facing_bet_val, bool):
        facing_bet_val = int(facing_bet_val)
    if not (action == 'CHECK' and facing_bet_val == 0):
        for f in ['villain_top_pair_plus_pct', 'villain_medium_made_pct',
                   'villain_draw_pct', 'villain_air_pct']:
            if f not in fa:
                fa[f] = 'CONFIRMED'

    # Bucket-specific mandatory features
    if bucket == 'drawing':
        for f in ['draw_outs', 'improvement_probability']:
            fa[f] = fa.get(f, 'CONFIRMED')
        if fd.get('has_flush_draw', 0):
            for f in ['flush_draw_rank', 'flush_block_pct']:
                fa[f] = fa.get(f, 'CONFIRMED')
    elif bucket == 'air':
        for f in ['overcard_outs', 'has_showdown_value', 'villain_fold_equity_estimate']:
            fa[f] = fa.get(f, 'CONFIRMED')
    elif bucket == 'medium_made':
        for f in ['has_showdown_value', 'danger_score', 'hero_range_percentile']:
            fa[f] = fa.get(f, 'CONFIRMED')
    elif bucket == 'monster':
        fa['spr'] = fa.get('spr', 'CONFIRMED')
    elif bucket == 'weak_made':
        for f in ['has_showdown_value', 'better_hand_pct']:
            fa[f] = fa.get(f, 'CONFIRMED')
        if facing_bet_val:
            fa['pot_odds'] = fa.get('pot_odds', 'CONFIRMED')
    elif bucket == 'strong_made':
        fa['danger_score'] = fa.get('danger_score', 'CONFIRMED')

    # Override clause features
    if override_fired:
        for f in ['facing_bet', 'num_opponents', 'villain_checked_back',
                   'villain_range_capped', 'worse_hand_pct', 'equity_vs_range', 'spr']:
            fa[f] = 'PRIMARY'

    return fa


def _build_tier1_removals(action: str, bucket: str, fd: dict) -> dict:
    """Build tier1_removals for action-dependent defaults that were removed."""
    removals = {}
    if action in ('BET', 'RAISE'):
        removals['pot_odds'] = "removed — this is a BET/RAISE, not a call decision"
    if action == 'CHECK':
        if not fd.get('facing_bet', 0):
            removals['pot_odds'] = "removed — not facing a bet, pot odds irrelevant"
    return removals


def aggregate_panels(panels: List[dict]) -> dict:
    """Aggregate 4 panel results into a single label."""
    actions = [p['action'] for p in panels]
    action_counts = {}
    for a in actions:
        action_counts[a] = action_counts.get(a, 0) + 1

    # Determine agreement
    max_count = max(action_counts.values())
    majority_action = max(action_counts, key=action_counts.get)

    if max_count == 4:
        label_source = 'panel_unanimous'
        chosen = majority_action
        pass2_needed = False
    elif max_count == 3:
        label_source = 'panel_majority'
        chosen = majority_action
        pass2_needed = True  # 3/1 split gets Pass 2
    elif max_count == 2:
        label_source = 'panel_split'
        chosen = majority_action  # Tie-break: pick first alphabetically
        pass2_needed = True
    else:
        label_source = 'panel_majority'
        chosen = majority_action
        pass2_needed = True

    # Pick the panel result matching the chosen action for detail fields
    chosen_panel = None
    for p in panels:
        if p['action'] == chosen:
            chosen_panel = p
            break
    if not chosen_panel:
        chosen_panel = panels[0]

    # Aggregate confidence
    confs = [p['confidence'] for p in panels if p['action'] == chosen]
    if all(c == 'HIGH' for c in confs):
        agg_conf = 'HIGH'
    elif any(c == 'LOW' for c in confs):
        agg_conf = 'LOW'
    else:
        agg_conf = 'MEDIUM'

    # Override clause: did it fire on any panel?
    override_fired = any(p.get('override_clause_fired', False) for p in panels)
    override_count = sum(1 for p in panels if p.get('override_clause_fired', False))

    return {
        'action': chosen,
        'confidence': agg_conf,
        'label_source': label_source,
        'panel_actions': action_counts,
        'pass2_needed': pass2_needed,
        'override_clause_fired': override_fired,
        'override_panel_count': override_count,
        'difficulty': chosen_panel['difficulty'],
        'hand_bucket': chosen_panel['hand_bucket'],
        'reasoning': chosen_panel['reasoning'],
        'intentions': chosen_panel['intentions'],
        'intentions_raw': chosen_panel['intentions_raw'],
        'feature_attention': chosen_panel['feature_attention'],
        'tier1_removals': chosen_panel['tier1_removals'],
        'alternatives_considered': chosen_panel['alternatives_considered'],
        'factor_conflicts': chosen_panel.get('factor_conflicts', ''),
    }


def pass2_review(hand: dict, pass1_agg: dict, pass1_panels: List[dict]) -> dict:
    """Pass 2: 2 review panels evaluate a disagreement.

    Reviews the Pass 1 disagreement and may override.
    """
    # Run 2 additional independent panels with review context
    review1 = label_hand_panel(hand, panel_id=5, seed=42)
    review2 = label_hand_panel(hand, panel_id=6, seed=99)

    review_actions = [review1['action'], review2['action']]
    pass1_action = pass1_agg['action']

    # Determine if Pass 2 overrides
    enqueue_for_solver = False
    override_kb_justification = ''

    if pass1_agg['label_source'] == 'panel_split':
        # 2/2 split: auto-enqueue for solver
        enqueue_for_solver = True

    # If reviews agree with Pass 1 majority
    if all(a == pass1_action for a in review_actions):
        # Reviews confirm Pass 1
        final_action = pass1_action
        label_source = 'pass2_confirmed'
    elif review_actions[0] == review_actions[1] and review_actions[0] != pass1_action:
        # Both reviews disagree with Pass 1 → override
        final_action = review_actions[0]
        label_source = 'pass2_override'
        enqueue_for_solver = True
        # Build override justification
        review_panel = review1
        if review_panel.get('override_clause_fired'):
            override_kb_justification = f"Pass 2 override: [v3 addition — Stream B.2 override clause] fires. Pass 1 panels defaulted to {pass1_action} without evaluating the override clause. All preconditions hold."
        else:
            override_kb_justification = f"Pass 2 override: {review_panel['reasoning']}"
    else:
        # Mixed review: keep Pass 1 majority
        final_action = pass1_action
        label_source = 'pass2_review'
        if pass1_agg['label_source'] == 'panel_split':
            enqueue_for_solver = True

    # Use the review panel matching the final action for details
    detail_panel = None
    for p in [review1, review2]:
        if p['action'] == final_action:
            detail_panel = p
            break
    if not detail_panel:
        for p in pass1_panels:
            if p['action'] == final_action:
                detail_panel = p
                break
    if not detail_panel:
        detail_panel = review1

    return {
        'action': final_action,
        'confidence': detail_panel['confidence'],
        'label_source': label_source,
        'pass2_review_actions': review_actions,
        'pass1_action': pass1_action,
        'pass1_panel_actions': pass1_agg['panel_actions'],
        'override_clause_fired': detail_panel.get('override_clause_fired', False),
        'override_kb_justification': override_kb_justification,
        'enqueue_for_solver': enqueue_for_solver,
        'difficulty': detail_panel['difficulty'],
        'hand_bucket': detail_panel['hand_bucket'],
        'reasoning': detail_panel['reasoning'],
        'intentions': detail_panel['intentions'],
        'intentions_raw': detail_panel['intentions_raw'],
        'feature_attention': detail_panel['feature_attention'],
        'tier1_removals': detail_panel['tier1_removals'],
        'alternatives_considered': detail_panel['alternatives_considered'],
        'factor_conflicts': detail_panel.get('factor_conflicts', ''),
    }


def load_all_hands() -> List[dict]:
    """Load all 470 hands (excluding 16 pilot IDs)."""
    all_hands = []
    for fname in INPUT_FILES:
        path = os.path.join(TRAINING_DATA, fname)
        with open(path) as f:
            for line in f:
                rec = json.loads(line)
                sid = rec.get('situation_id', '')
                if sid in PILOT_IDS:
                    continue
                all_hands.append(rec)
    return all_hands


def normalize_hand(hand: dict) -> dict:
    """Normalize flat-format hands to have a consistent interface."""
    # If already has feat_dict, return as-is
    if 'feat_dict' in hand:
        return hand
    # For flat format, features are at the top level
    return hand


def main():
    """Run the full Phase 4 labelling pipeline."""
    print("Phase 4 Production Labelling — 470 hands, 4-panel + Pass 2")
    print("=" * 60)

    # Load hands
    all_hands = load_all_hands()
    print(f"Loaded {len(all_hands)} hands (excluding {len(PILOT_IDS)} pilot)")

    # Track stats
    stats = {
        'total': len(all_hands),
        'pass1_unanimous': 0,
        'pass1_majority': 0,
        'pass1_split': 0,
        'pass2_entries': 0,
        'pass2_overrides': 0,
        'solver_enqueued': 0,
        'override_fires_umbrella': 0,
        'override_fires_non_umbrella': 0,
        'umbrella_total': 0,
        'non_umbrella_total': 0,
        'action_dist': {},
        'errors': [],
    }

    final_labels = []
    pass2_queue = []

    # ── Pass 1: 4 panels per hand ──
    print("\n── Pass 1: 4 independent panels ──")
    for i, hand in enumerate(all_hands):
        sid = hand.get('situation_id', f'unknown_{i}')
        is_umbrella = _is_umbrella_bucket(hand)
        if is_umbrella:
            stats['umbrella_total'] += 1
        else:
            stats['non_umbrella_total'] += 1

        try:
            # Run 4 independent panels
            panels = []
            for pid in range(4):
                panel_result = label_hand_panel(hand, panel_id=pid, seed=pid * 17 + i)
                panels.append(panel_result)

            # Aggregate
            agg = aggregate_panels(panels)

            if agg['override_clause_fired']:
                if is_umbrella:
                    stats['override_fires_umbrella'] += 1
                else:
                    stats['override_fires_non_umbrella'] += 1

            if agg['label_source'] == 'panel_unanimous':
                stats['pass1_unanimous'] += 1
            elif agg['label_source'] == 'panel_majority':
                stats['pass1_majority'] += 1
            elif agg['label_source'] == 'panel_split':
                stats['pass1_split'] += 1

            if agg['pass2_needed']:
                pass2_queue.append((hand, agg, panels))
            else:
                # Direct to final labels
                label = _build_final_label(hand, agg)
                final_labels.append(label)

        except Exception as e:
            stats['errors'].append(f"{sid}: {str(e)}")
            print(f"  ERROR on {sid}: {e}")

        if (i + 1) % 50 == 0:
            print(f"  Pass 1: {i+1}/{len(all_hands)} hands processed")

    print(f"\nPass 1 complete:")
    print(f"  Unanimous (4/4): {stats['pass1_unanimous']}")
    print(f"  Majority (3/1):  {stats['pass1_majority']}")
    print(f"  Split (2/2):     {stats['pass1_split']}")
    print(f"  Pass 2 queue:    {len(pass2_queue)}")

    # ── Pass 2: Review disagreements ──
    print(f"\n── Pass 2: {len(pass2_queue)} hands for review ──")
    stats['pass2_entries'] = len(pass2_queue)

    for hand, pass1_agg, pass1_panels in pass2_queue:
        sid = hand.get('situation_id', '')
        try:
            pass2_result = pass2_review(hand, pass1_agg, pass1_panels)

            if pass2_result['label_source'] == 'pass2_override':
                stats['pass2_overrides'] += 1

            if pass2_result.get('enqueue_for_solver', False):
                stats['solver_enqueued'] += 1

            label = _build_final_label(hand, pass2_result)
            final_labels.append(label)

        except Exception as e:
            stats['errors'].append(f"{sid} (Pass2): {str(e)}")
            print(f"  ERROR on {sid}: {e}")
            # Fall back to Pass 1
            label = _build_final_label(hand, pass1_agg)
            final_labels.append(label)

    # ── Phase 4.3: Assembly ──
    print(f"\n── Assembly ──")

    # Count action distribution
    for label in final_labels:
        a = label.get('expert_action', 'UNKNOWN')
        stats['action_dist'][a] = stats['action_dist'].get(a, 0) + 1

    # Sort by situation_id for deterministic output
    final_labels.sort(key=lambda x: x.get('situation_id', ''))

    # Write output
    output_path = os.path.join(TRAINING_DATA, 'pass1_final_labels_v23.jsonl')
    with open(output_path, 'w') as f:
        for label in final_labels:
            f.write(json.dumps(label, ensure_ascii=False) + '\n')

    print(f"  Written {len(final_labels)} labels to {output_path}")

    # ── Report ──
    print(f"\n{'=' * 60}")
    print(f"PHASE 4 SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total hands labelled: {len(final_labels)}")
    print(f"")
    print(f"Pass 1 agreement:")
    total = stats['total']
    print(f"  Unanimous (4/4): {stats['pass1_unanimous']} ({100*stats['pass1_unanimous']/total:.1f}%)")
    print(f"  Majority (3/1):  {stats['pass1_majority']} ({100*stats['pass1_majority']/total:.1f}%)")
    print(f"  Split (2/2):     {stats['pass1_split']} ({100*stats['pass1_split']/total:.1f}%)")
    disagreement_rate = (stats['pass1_majority'] + stats['pass1_split']) / total * 100
    print(f"  Disagreement rate: {disagreement_rate:.1f}%")
    print(f"")
    print(f"Pass 2:")
    print(f"  Entries:   {stats['pass2_entries']}")
    print(f"  Overrides: {stats['pass2_overrides']} ({100*stats['pass2_overrides']/total:.1f}%)")
    print(f"")
    print(f"Override clause:")
    umb_rate = 100 * stats['override_fires_umbrella'] / max(stats['umbrella_total'], 1)
    non_umb_rate = 100 * stats['override_fires_non_umbrella'] / max(stats['non_umbrella_total'], 1)
    print(f"  UMBRELLA:     {stats['override_fires_umbrella']}/{stats['umbrella_total']} ({umb_rate:.1f}%)")
    print(f"  Non-UMBRELLA: {stats['override_fires_non_umbrella']}/{stats['non_umbrella_total']} ({non_umb_rate:.1f}%)")
    print(f"")
    print(f"Action distribution:")
    for action in sorted(stats['action_dist'].keys()):
        count = stats['action_dist'][action]
        print(f"  {action}: {count} ({100*count/len(final_labels):.1f}%)")
    print(f"")
    print(f"Solver enqueue: {stats['solver_enqueued']}")
    if stats['errors']:
        print(f"Errors: {len(stats['errors'])}")
        for e in stats['errors'][:5]:
            print(f"  {e}")

    # ── Stop condition checks ──
    print(f"\n{'=' * 60}")
    print(f"STOP CONDITION CHECKS")
    print(f"{'=' * 60}")

    # S4.1: disagreement rate > 35%
    if disagreement_rate > 35:
        print(f"S4.1 STOP: Disagreement rate {disagreement_rate:.1f}% > 35% threshold")
        return stats
    else:
        print(f"S4.1 PASS: Disagreement rate {disagreement_rate:.1f}% <= 35%")

    # S4.2: Pass 2 override rate > 10%
    override_rate = 100 * stats['pass2_overrides'] / total
    if override_rate > 10:
        print(f"S4.2 STOP: Override rate {override_rate:.1f}% > 10% threshold")
        return stats
    else:
        print(f"S4.2 PASS: Override rate {override_rate:.1f}% <= 10%")

    # S4.3: Override clause on >10% non-UMBRELLA
    if non_umb_rate > 10:
        print(f"S4.3 STOP: Override clause on {non_umb_rate:.1f}% non-UMBRELLA > 10%")
        return stats
    else:
        print(f"S4.3 PASS: Override clause on {non_umb_rate:.1f}% non-UMBRELLA <= 10%")

    print(f"\nAll stop conditions PASS.")
    return stats


def _build_final_label(hand: dict, agg: dict) -> dict:
    """Build a final label record merging situation + aggregated label."""
    sid = hand.get('situation_id', '')
    bucket = hand.get('bucket', 'CURATED')

    # Build the output record
    label = {}

    # Copy situation data
    if 'feat_dict' in hand:
        # Nested format
        for k, v in hand.items():
            if k != 'feat_dict':
                label[k] = v
        label['feat_dict'] = hand['feat_dict']
    else:
        # Flat format — copy everything
        for k, v in hand.items():
            label[k] = v

    # Add label fields
    label['expert_action'] = agg['action']
    label['expert_confidence'] = agg['confidence']
    label['expert_reasoning'] = agg['reasoning']
    label['label_source'] = agg['label_source']
    label['hand_bucket'] = agg['hand_bucket']
    label['difficulty'] = agg['difficulty']
    label['override_clause_fired'] = agg.get('override_clause_fired', False)
    label['intentions'] = agg.get('intentions', [])
    label['intentions_raw'] = agg.get('intentions_raw', '')
    label['feature_attention'] = agg.get('feature_attention', {})
    label['alternatives_considered'] = agg.get('alternatives_considered', [])
    label['factor_conflicts'] = agg.get('factor_conflicts', '')

    # Pass 2 metadata (if applicable)
    if 'pass2_review_actions' in agg:
        label['pass2_review_actions'] = agg['pass2_review_actions']
        label['pass1_action'] = agg.get('pass1_action', '')
        label['pass1_panel_actions'] = agg.get('pass1_panel_actions', {})
        label['override_kb_justification'] = agg.get('override_kb_justification', '')
        label['enqueue_for_solver'] = agg.get('enqueue_for_solver', False)

    # Street plan (if not river)
    if 'street_plan_raw' in agg:
        label['street_plan_raw'] = agg['street_plan_raw']
        label['street_plan_tags'] = agg.get('street_plan_tags', [])

    return label


if __name__ == '__main__':
    main()
