"""
generate_v23_call_supplement.py — CALL supplement for v2.3-clean assembly.

Produces ~25-30 facing-bet spots where CALL is GTO-correct:

Sub-patterns:
  CALL_POT_ODDS    (10): Drawing hand (FD/OESD), small bet (bet_to_pot ≤ 0.5),
                         pot odds justify call. Turn or river. Multiway (num_opponents=2).
  CALL_MEDIUM_STR  (10): Medium-made hand (2nd pair, 3rd pair, weak TP),
                         facing bet, not strong enough to raise, too strong to fold.
                         Flop or turn.
  CALL_TRAP_FLAT   (5):  Monster/strong hand, facing bet, flatting to trap
                         (not raising). Flop or turn.

All specs: num_opponents=2 (3-way), normalised via normalise_situation().

Run:
    python3 review/generate_v23_call_supplement.py
"""

from __future__ import annotations

import sys
import os
import json
from typing import Callable, Dict, List, Tuple

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_CORE = os.path.join(_REPO, 'river-rats-core')
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)
os.chdir(_CORE)

from situation_factory import (
    SituationSpec,
    build_situation,
    validate_situation,
    normalise_situation,
    _POSTFLOP_ORDER as _PFO,
)
from hand_evaluator import evaluate_hand

OUTPUT_DIR = os.path.join(_REPO, 'training-data')

# ---------------------------------------------------------------------------
# Sizing — 3-way pot, pot=90, eff_stack=450
# ---------------------------------------------------------------------------
STD_POT = 90.0
STD_STACK = 450.0
SMALL_BET = 30.0    # 33% of 90-pot (bet_to_pot ~ 0.33)
MEDIUM_BET = 45.0   # 50% of 90-pot (bet_to_pot ~ 0.50)

# ---------------------------------------------------------------------------
# Board templates (reused from batch6)
# ---------------------------------------------------------------------------
DRY_BOARDS = [
    ['Kh', '9d', '3c'], ['Kd', '7c', '2s'], ['Ks', '8c', '3d'],
    ['Qh', '7d', '2c'], ['Qc', '8d', '3s'], ['Qs', '6d', '2h'],
    ['Jd', '8c', '3s'], ['Jh', '7c', '2d'], ['Js', '6d', '2c'],
    ['Ah', '9d', '3c'], ['Ac', '7d', '2s'], ['As', '8d', '3h'],
    ['Td', '6c', '2s'], ['Th', '7d', '3c'],
    ['9d', '5c', '2s'], ['9h', '4c', '2d'],
]

TWO_TONE_BOARDS = [
    ['Ts', '6s', '3d'], ['Js', '7s', '2d'], ['Qs', '8s', '3d'],
    ['Ks', '8s', '4h'],
    ['Qh', '8h', '4d'], ['Th', '6h', '2d'], ['Jh', '7h', '3c'],
    ['9h', '5h', '2c'],
    ['Jc', '7c', '2d'], ['Qc', '9c', '5h'], ['Tc', '6c', '3d'],
    ['Kc', '8c', '4d'],
    ['Ad', '5d', '2c'], ['Kd', '9d', '3c'], ['Qd', '7d', '2h'],
]

CONNECTED_TWO_TONE_BOARDS = [
    ['Th', '9s', '6s'], ['Js', 'Ts', '7h'], ['Td', '9c', '8c'],
    ['9s', '8s', '5d'], ['Qc', 'Tc', '8d'], ['Jd', '9d', '8s'],
    ['8h', '7h', '5c'], ['9d', '8d', '6c'], ['Qh', 'Th', '9s'],
    ['Kh', 'Jh', '9c'],
]

# ---------------------------------------------------------------------------
# Archetypes
# ---------------------------------------------------------------------------
ARCHETYPES_IP = [
    ('BTN', ['SB', 'BB'], 'BTN'),
    ('BTN', ['HJ', 'BB'], 'BTN'),
    ('CO',  ['SB', 'BB'], 'CO'),
    ('CO',  ['HJ', 'BB'], 'CO'),
]
ARCHETYPES_IP = [
    (h, v, o) for (h, v, o) in ARCHETYPES_IP
    if all(_PFO[h] > _PFO[vp] for vp in v)
]

ARCHETYPES_OOP = [
    ('SB', ['CO', 'BTN'], 'CO'),
    ('BB', ['HJ', 'BTN'], 'HJ'),
    ('BB', ['CO', 'BTN'], 'CO'),
]

# ---------------------------------------------------------------------------
# Card utilities
# ---------------------------------------------------------------------------
SUITS = ['h', 'd', 'c', 's']
ALL_RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']


def _all_cards():
    return [r + s for r in ALL_RANKS for s in SUITS]


def _safe_turn_card(board_flop, hero_cards):
    dead = set(board_flop) | set(hero_cards)
    pool = ['2h', '3c', '4d', '5s', '6h', '7c', '8d', '9s', 'Tc', 'Jd', 'Qh', 'Kc', 'Ad']
    for c in pool:
        if c not in dead:
            return c
    for c in _all_cards():
        if c not in dead:
            return c
    raise RuntimeError("no turn card available")


def _safe_river_card(board4, hero_cards):
    dead = set(board4) | set(hero_cards)
    pool = ['2h', '3c', '4d', '5s', '6h', '7c', '8d', '9s', 'Tc', 'Jd', 'Qh', 'Kc', 'Ad']
    for c in pool:
        if c not in dead:
            return c
    for c in _all_cards():
        if c not in dead:
            return c
    raise RuntimeError("no river card available")


# ---------------------------------------------------------------------------
# Preflop history
# ---------------------------------------------------------------------------
def _preflop_history(opener, callers):
    acts = [('preflop', opener, 'raise')]
    for c in callers:
        acts.append(('preflop', c, 'call'))
    return acts


# ---------------------------------------------------------------------------
# Hand-strength classifiers
# ---------------------------------------------------------------------------
MONSTER_CATS = {
    'straight_flush', 'quads', 'full_house', 'flush', 'straight',
    'set', 'trips',
}
STRONG_CATS = {
    'two_pair', 'overpair', 'top_pair_top_kicker', 'top_pair_good_kicker',
}
MEDIUM_CATS = {
    'top_pair', 'mid_pair', 'middle_pair',
    'low_pair', 'bottom_pair', 'pair', 'underpair',
}
DRAW_CATS = {'flush_draw', 'straight_draw', 'draw'}
# The hand evaluator often classifies drawing hands as overcards/high_card.
# For pot-odds CALL spots, we want weak hands that are "drawing" — overcards
# on two-tone boards (implicit flush draw) or connected boards (straight draw).
WEAK_DRAWING_CATS = {'overcards', 'one_overcard', 'high_card', 'flush_draw', 'straight_draw', 'draw'}


def _category_of(hero_cards, board):
    return evaluate_hand(hero_cards, board).category


def _is_draw(hero_cards, board):
    """Drawing hand: either evaluator says draw, or overcards/high_card
    with at least one suited card matching the board suit (implicit FD)
    or connected to board ranks (implicit straight draw)."""
    cat = _category_of(hero_cards, board)
    return cat in WEAK_DRAWING_CATS


def _is_medium(hero_cards, board):
    return _category_of(hero_cards, board) in MEDIUM_CATS


def _is_monster(hero_cards, board):
    return _category_of(hero_cards, board) in MONSTER_CATS


def _is_strong(hero_cards, board):
    return _category_of(hero_cards, board) in STRONG_CATS


def _is_monster_or_strong(hero_cards, board):
    cat = _category_of(hero_cards, board)
    return cat in MONSTER_CATS | STRONG_CATS


def _pick_hole_cards(board, want_fn, max_hands, used):
    dead = set(board) | used
    available = [c for c in _all_cards() if c not in dead]
    found = []
    for i in range(len(available)):
        for j in range(i + 1, len(available)):
            cards = [available[i], available[j]]
            try:
                if want_fn(cards, board):
                    found.append(cards)
                    if len(found) >= max_hands:
                        return found
            except Exception:
                continue
    return found


def _make_spec(hero_cards, board, hero_pos, villain_positions,
               pot, to_call, street, action_history, opener_position,
               effective_stack=STD_STACK, current_bet=0.0):
    return SituationSpec(
        hero_cards=hero_cards,
        board_cards=board,
        hero_pos=hero_pos,
        villain_positions=villain_positions,
        pot=pot,
        to_call=to_call,
        street=street,
        action_history=action_history,
        opener_position=opener_position,
        effective_stack=effective_stack,
        current_bet=current_bet,
        num_opponents=2,
    )


# ==========================================================================
# Sub-pattern 1: CALL_POT_ODDS — drawing hand facing small bet
# Hero has flush draw or OESD on two-tone/connected board, facing small bet.
# Turn or river. Pot odds justify a call.
# ==========================================================================
def build_CALL_POT_ODDS_specs(target: int = 12) -> List[Tuple[SituationSpec, str]]:
    specs = []
    used = set()

    # Use two-tone boards so flush draws are possible
    board_pool = TWO_TONE_BOARDS + CONNECTED_TWO_TONE_BOARDS
    # Hero is IP (last to act), facing a bet from a villain
    for hero_pos, villain_positions, opener in ARCHETYPES_IP:
        for flop in board_pool:
            if len(specs) >= target:
                break
            turn = _safe_turn_card(flop, [])
            board = flop + [turn]
            pre = _preflop_history(
                opener,
                [p for p in villain_positions + [hero_pos] if p != opener],
            )
            active_order = sorted(
                villain_positions + [hero_pos],
                key=lambda p: _PFO[p],
            )
            # Flop: checks through
            flop_actions = [('flop', p, 'check') for p in active_order]
            # Turn: first villain bets, second villain calls or checks
            # The last villain in the list is the bettor per factory convention
            v_order = sorted(villain_positions, key=lambda p: _PFO[p])
            turn_actions = [
                ('turn', v_order[0], 'check'),
                ('turn', v_order[-1], 'bet'),
            ]
            action_history = pre + flop_actions + turn_actions

            heroes = _pick_hole_cards(board, _is_draw, max_hands=2, used=used)
            for hero in heroes:
                if len(specs) >= target:
                    break
                spec = _make_spec(
                    hero_cards=hero, board=board,
                    hero_pos=hero_pos, villain_positions=villain_positions,
                    pot=STD_POT + SMALL_BET,  # pot after villain bet
                    to_call=SMALL_BET,
                    street='turn',
                    action_history=action_history,
                    opener_position=opener,
                    current_bet=SMALL_BET,
                )
                desc = (
                    f'CALL_POT_ODDS: hero {hero_pos} draw '
                    f'({_category_of(hero, board)}) on {"-".join(board)}; '
                    f'facing small bet ({SMALL_BET}), pot odds justify call.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
    return specs[:target]


# ==========================================================================
# Sub-pattern 2: CALL_MEDIUM_STR — medium made hand facing bet
# Hero has 2nd pair / 3rd pair / weak TP, facing a bet. Not strong enough
# to raise, too strong to fold. Flop or turn.
# ==========================================================================
def build_CALL_MEDIUM_STR_specs(target: int = 12) -> List[Tuple[SituationSpec, str]]:
    specs = []
    used = set()

    board_pool = DRY_BOARDS + TWO_TONE_BOARDS
    # Mix of IP and OOP
    all_archs = ARCHETYPES_IP[:2] + ARCHETYPES_OOP[:2]

    for hero_pos, villain_positions, opener in all_archs:
        for flop in board_pool:
            if len(specs) >= target:
                break

            pre = _preflop_history(
                opener,
                [p for p in villain_positions + [hero_pos] if p != opener],
            )
            active_order = sorted(
                villain_positions + [hero_pos],
                key=lambda p: _PFO[p],
            )

            # Villain bets into hero on the flop
            v_order = sorted(villain_positions, key=lambda p: _PFO[p])

            # For IP hero: villains act first, last villain bets
            if _PFO[hero_pos] > max(_PFO[vp] for vp in villain_positions):
                flop_actions = [
                    ('flop', v_order[0], 'check'),
                    ('flop', v_order[-1], 'bet'),
                ]
            else:
                # OOP hero: first villain (after hero in order) bets
                flop_actions = [
                    ('flop', v_order[-1], 'bet'),
                ]
                # If there's a villain before hero, they check
                vills_before = [v for v in v_order if _PFO[v] < _PFO[hero_pos]]
                if vills_before:
                    flop_actions = [('flop', vills_before[0], 'check')] + flop_actions

            action_history = pre + flop_actions

            heroes = _pick_hole_cards(flop, _is_medium, max_hands=2, used=used)
            for hero in heroes:
                if len(specs) >= target:
                    break
                spec = _make_spec(
                    hero_cards=hero, board=flop,
                    hero_pos=hero_pos, villain_positions=villain_positions,
                    pot=STD_POT + MEDIUM_BET,
                    to_call=MEDIUM_BET,
                    street='flop',
                    action_history=action_history,
                    opener_position=opener,
                    current_bet=MEDIUM_BET,
                )
                desc = (
                    f'CALL_MEDIUM_STR: hero {hero_pos} medium '
                    f'({_category_of(hero, flop)}) on {"-".join(flop)}; '
                    f'facing bet ({MEDIUM_BET}), call-worthy but not raisable.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
    return specs[:target]


# ==========================================================================
# Sub-pattern 3: CALL_TRAP_FLAT — monster/strong hand, flat-calling to trap
# Hero has a set/trips/two-pair/overpair, facing a bet, flatting to keep
# villain in. Flop or turn.
# ==========================================================================
def build_CALL_TRAP_FLAT_specs(target: int = 8) -> List[Tuple[SituationSpec, str]]:
    specs = []
    used = set()

    board_pool = DRY_BOARDS[:10]
    for hero_pos, villain_positions, opener in ARCHETYPES_IP:
        for flop in board_pool:
            if len(specs) >= target:
                break
            pre = _preflop_history(
                opener,
                [p for p in villain_positions + [hero_pos] if p != opener],
            )
            v_order = sorted(villain_positions, key=lambda p: _PFO[p])
            # Villain bets, hero is IP
            flop_actions = [
                ('flop', v_order[0], 'check'),
                ('flop', v_order[-1], 'bet'),
            ]
            action_history = pre + flop_actions

            heroes = _pick_hole_cards(flop, _is_monster_or_strong, max_hands=2, used=used)
            for hero in heroes:
                if len(specs) >= target:
                    break
                spec = _make_spec(
                    hero_cards=hero, board=flop,
                    hero_pos=hero_pos, villain_positions=villain_positions,
                    pot=STD_POT + SMALL_BET,
                    to_call=SMALL_BET,
                    street='flop',
                    action_history=action_history,
                    opener_position=opener,
                    current_bet=SMALL_BET,
                )
                cat = _category_of(hero, flop)
                desc = (
                    f'CALL_TRAP_FLAT: hero {hero_pos} {cat} '
                    f'on {"-".join(flop)}; '
                    f'facing small bet ({SMALL_BET}), flat-calling to trap.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
    return specs[:target]


# ==========================================================================
# Bucket registry
# ==========================================================================
BUCKET_BUILDERS = {
    'CALL_POT_ODDS': build_CALL_POT_ODDS_specs,
    'CALL_MEDIUM_STR': build_CALL_MEDIUM_STR_specs,
    'CALL_TRAP_FLAT': build_CALL_TRAP_FLAT_specs,
}

BUCKET_META = {
    'CALL_POT_ODDS':  (10, 12, 'v23_call_pot_odds.jsonl'),
    'CALL_MEDIUM_STR': (10, 12, 'v23_call_medium_str.jsonl'),
    'CALL_TRAP_FLAT':  (5, 8, 'v23_call_trap_flat.jsonl'),
}


def generate_one_bucket(bucket, verbose=False):
    build_fn = BUCKET_BUILDERS[bucket]
    spec_tuples = build_fn()
    records = []
    for idx, (spec, description) in enumerate(spec_tuples):
        sit_id = f'{bucket}_{idx + 1:03d}'
        try:
            feat_dict = build_situation(spec)
        except Exception as exc:
            if verbose:
                print(f'  SKIP {sit_id}: BUILD_EXCEPTION: {exc}')
            records.append({
                '_skip_reason': f'BUILD_EXCEPTION: {exc}',
                'situation_id': sit_id,
                'bucket': bucket,
                'has_errors': True,
            })
            continue
        validation_errors = validate_situation(spec, feat_dict)
        feat_dict['situation_id'] = sit_id
        feat_dict['bucket'] = bucket
        feat_dict['sub_pattern'] = bucket
        feat_dict['hero_cards'] = ''.join(spec.hero_cards)
        feat_dict['board_cards'] = ''.join(spec.board_cards)
        feat_dict['description'] = description
        feat_dict['action_string'] = spec.action_string
        feat_dict['hero_position'] = spec.hero_pos
        feat_dict['villain_positions'] = list(spec.villain_positions)
        feat_dict['street'] = spec.street
        feat_dict['has_errors'] = bool(validation_errors)
        if validation_errors:
            feat_dict['validation_errors'] = validation_errors
        records.append(feat_dict)
    return records


def write_bucket(bucket, records):
    bp_target, os_target, filename = BUCKET_META[bucket]
    out_path = os.path.join(OUTPUT_DIR, filename)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated = len(records)
    build_failures = sum(1 for r in records if r.get('_skip_reason'))
    write_rows = [r for r in records if not r.get('_skip_reason')]
    validated = sum(1 for r in write_rows if not r.get('has_errors'))
    with open(out_path, 'w') as f:
        for r in write_rows:
            f.write(json.dumps(normalise_situation(r)) + '\n')
    return {
        'bucket': bucket,
        'bp_target': bp_target,
        'os_target': os_target,
        'generated': generated,
        'build_failures': build_failures,
        'written': len(write_rows),
        'validated_clean': validated,
        'out_path': out_path,
    }


def main():
    print('=' * 72)
    print('CALL SUPPLEMENT — v2.3-clean')
    print('=' * 72)

    # Generate all buckets, write to individual files
    all_records = []
    for bucket in BUCKET_BUILDERS:
        bp, os_t, fn = BUCKET_META[bucket]
        print(f'\n[{bucket}] target BP={bp} OS={os_t}')
        records = generate_one_bucket(bucket, verbose=True)
        stats = write_bucket(bucket, records)
        print(f'  generated={stats["generated"]} '
              f'build_failures={stats["build_failures"]} '
              f'written={stats["written"]} '
              f'validated_clean={stats["validated_clean"]}')
        # Collect clean records for combined output
        for r in records:
            if not r.get('_skip_reason'):
                all_records.append(r)

    # Write combined JSONL
    combined_path = os.path.join(OUTPUT_DIR, 'v23_call_supplement.jsonl')
    with open(combined_path, 'w') as f:
        for r in all_records:
            f.write(json.dumps(normalise_situation(r)) + '\n')

    print(f'\n{"=" * 72}')
    print(f'Combined output: {combined_path}')
    print(f'Total records: {len(all_records)}')

    # Verify facing_bet=1 on all records
    fb_check = sum(1 for r in all_records if r.get('facing_bet') == 1)
    print(f'facing_bet=1: {fb_check}/{len(all_records)}')
    if fb_check != len(all_records):
        print('WARNING: Some records do not have facing_bet=1!')
        for r in all_records:
            if r.get('facing_bet') != 1:
                print(f'  {r["situation_id"]}: facing_bet={r.get("facing_bet")}')
    print('=' * 72)
    return True


if __name__ == '__main__':
    ok = main()
    sys.exit(0 if ok else 1)
