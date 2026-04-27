"""Donk-bet defence scenario specs (Module 8).

Hero is IP (BTN or CO) facing an OOP donk lead from the BB.
Hero position is specified explicitly per sub-scenario (C3 fix).

Sub-scenarios 8a-8e per blueprint v3 Q6 Module 8 spec.

gto-expert N4: BB's donk range is polarised — strong (sets, two-pair, top pair on
specific boards), strong semi-bluffs (nut flush draws, combo draws on 2-flush boards),
OR air. Not just value and air poles.

gto-expert Pattern D: At least 5 hands on 2-flush boards where hero holds one card
of the flush suit (flush_draw_block_pct > 0).
"""
from __future__ import annotations

import sys
import os
from typing import List, Set, Tuple

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from situation_factory import SituationSpec
from corpus_revision_scenarios._scenario_utils import (
    build_record_from_spec,
    fingerprint,
)

# Sub-scenario 8a: Hero CO, PFA = HJ. CO faces BB donk first (num_callers_to_bet=0).
# Sub-scenario 8b: Hero BTN, PFA = CO. CO either folds or calls before BTN.
# Sub-scenario 8c: Hero CO, PFA = CO (hero is PFA). CO faces BB donk (is_preflop_aggressor=1).
# Sub-scenario 8d: Hero BTN, PFA = BTN (hero is PFA, HU vs BB). is_preflop_aggressor=1.
# Sub-scenario 8e: Hero CO, PFA = CO (sandwich). BTN live behind CO.

_DONK_TEMPLATES: List[dict] = [
    # ─── Sub-scenario 8a: Hero CO, PFA=HJ, CO faces BB donk first ───
    {'sub_scenario': '8a',
     'hero_pos': 'CO', 'villain_positions': ['BB', 'BTN'],
     'opener_position': 'HJ',
     'board': ['Kc', '7h', '2d'],
     'hero_cards': ['Ac', 'Jd'],  # overcards facing donk
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),  # BB donks; CO (hero) faces first
     ]},
    {'sub_scenario': '8a',
     'hero_pos': 'CO', 'villain_positions': ['BB', 'BTN'],
     'opener_position': 'HJ',
     'board': ['9d', '6c', '2h'],
     'hero_cards': ['Tc', 'Td'],  # overpair facing donk on low board
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},

    # ─── Sub-scenario 8b (CO calls first): Hero BTN, PFA=CO, CO calls donk ───
    {'sub_scenario': '8b_co_calls',
     'hero_pos': 'BTN', 'villain_positions': ['BB', 'CO'],
     'opener_position': 'CO',
     'board': ['Jh', '8d', '3s'],
     'hero_cards': ['Qc', 'Jd'],  # top pair facing call+donk
     'pot': 30.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),  # CO calls; BTN faces callers=1
     ]},
    {'sub_scenario': '8b_co_calls',
     'hero_pos': 'BTN', 'villain_positions': ['BB', 'CO'],
     'opener_position': 'CO',
     'board': ['Ks', '5c', '2d'],
     'hero_cards': ['Kd', 'Qh'],  # strong top pair (BTN sandwiched)
     'pot': 30.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
     ]},

    # ─── Sub-scenario 8b (CO folds): Hero BTN, num_callers_to_bet=0 ───
    # CO folded preflop action is not in action_history because CO is not
    # active postflop. villain_positions=['BB'] reflects the post-fold state.
    # The fold action is omitted from action_history since it would fail
    # the validator (CO not in active positions list).
    {'sub_scenario': '8b_co_folds',
     'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Td', '6h', '2c'],
     'hero_cards': ['As', 'Kc'],  # overcards (BTN faces HU vs BB donk)
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
         # CO folded on flop (before BTN); represented by villain_positions=['BB']
     ]},

    # ─── Sub-scenario 8c: Hero CO (PFA=CO), BB donks into hero ───
    {'sub_scenario': '8c',
     'hero_pos': 'CO', 'villain_positions': ['BB', 'BTN'],
     'opener_position': 'CO',
     'board': ['8s', '5d', '2c'],
     'hero_cards': ['Ac', 'Kh'],  # PFA with overcards
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),  # BB donks into PFA CO; CO faces first
     ]},
    {'sub_scenario': '8c',
     'hero_pos': 'CO', 'villain_positions': ['BB', 'BTN'],
     'opener_position': 'CO',
     'board': ['Qd', '7s', '3h'],
     'hero_cards': ['Kc', 'Kh'],  # overpair (KK) facing donk on Qd-7s-3h board
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},

    # ─── Sub-scenario 8d: Hero BTN (PFA=BTN), HU vs BB after SB fold ───
    {'sub_scenario': '8d',
     'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Jc', '8h', '3d'],
     'hero_cards': ['Ah', 'Kd'],  # PFA facing HU donk
     'pot': 15.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'fold'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},
    {'sub_scenario': '8d',
     'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['9s', '6c', '2h'],
     'hero_cards': ['Qs', 'Qd'],  # overpair facing donk HU
     'pot': 15.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'fold'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},

    # ─── Sub-scenario 8e: Hero CO (PFA=CO, sandwich, BTN live behind) ───
    {'sub_scenario': '8e',
     'hero_pos': 'CO', 'villain_positions': ['BB', 'BTN'],
     'opener_position': 'CO',
     'board': ['Tc', '7d', '4s'],
     'hero_cards': ['As', 'Ts'],  # top pair facing donk with BTN behind
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},

    # ─── Pattern D: 2-flush boards, hero holds one card of flush suit ───
    # (gto-expert N4/Pattern D: flush_draw_block_pct > 0)
    {'sub_scenario': '8a',
     'hero_pos': 'CO', 'villain_positions': ['BB', 'BTN'],
     'opener_position': 'HJ',
     'board': ['Kd', '8d', '3c'],  # 2-flush diamonds
     'hero_cards': ['Qd', 'Jc'],  # hero has Qd = blocks diamond flush
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},
    {'sub_scenario': '8b_co_calls',
     'hero_pos': 'BTN', 'villain_positions': ['BB', 'CO'],
     'opener_position': 'CO',
     'board': ['Jh', '7h', '2c'],  # 2-flush hearts
     'hero_cards': ['Th', 'Kd'],  # hero has Th = partial flush blocker
     'pot': 30.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
     ]},
    {'sub_scenario': '8c',
     'hero_pos': 'CO', 'villain_positions': ['BB', 'BTN'],
     'opener_position': 'CO',
     'board': ['Qs', '9s', '3d'],  # 2-flush spades
     'hero_cards': ['Ks', 'Ah'],  # hero has Ks = blocks spade flush
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},
    {'sub_scenario': '8d',
     'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Th', '5h', '2d'],  # 2-flush hearts
     'hero_cards': ['Ah', 'Kc'],  # PFA with Ah = nut flush blocker
     'pot': 15.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'fold'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},
    {'sub_scenario': '8e',
     'hero_pos': 'CO', 'villain_positions': ['BB', 'BTN'],
     'opener_position': 'CO',
     'board': ['8c', '4c', '2h'],  # 2-flush clubs
     'hero_cards': ['Ac', 'Jd'],  # hero has Ac = nut flush blocker on clubs
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},

    # ─────────────────────────────────────────────────────────────────
    # DK-N (Phase 6 expansion v3.5): 10 new templates.
    # 6 sub-8c/8d (hero=PFA, donk+pfa overlap) + 4 pure donk (8a/8b).
    # ─────────────────────────────────────────────────────────────────
    # DK-N-01: 8c CO PFA, BB donks, BTN behind
    {'sub_scenario': '8c',
     'hero_pos': 'CO', 'villain_positions': ['BB', 'BTN'],
     'opener_position': 'CO',
     'board': ['Kd', '5d', '2h'],
     'hero_cards': ['Ac', 'Kh'],  # top pair top kicker
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},
    # DK-N-02: 8c CO PFA on low connected board
    {'sub_scenario': '8c',
     'hero_pos': 'CO', 'villain_positions': ['BB', 'BTN'],
     'opener_position': 'CO',
     'board': ['7h', '5s', '3d'],
     'hero_cards': ['Kh', 'Kd'],  # overpair
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},
    # DK-N-03: 8d BTN PFA HU vs BB after SB fold
    {'sub_scenario': '8d',
     'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Ah', '6c', '3s'],
     'hero_cards': ['Kd', 'Kh'],  # overpair
     'pot': 15.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'fold'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},
    # DK-N-04: 8d BTN PFA HU
    {'sub_scenario': '8d',
     'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Qs', '4h', '2d'],
     'hero_cards': ['Jd', 'Jh'],  # overpair to board
     'pot': 15.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'fold'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},
    # DK-N-05: 8c CO PFA on J-high
    {'sub_scenario': '8c',
     'hero_pos': 'CO', 'villain_positions': ['BB', 'BTN'],
     'opener_position': 'CO',
     'board': ['Jd', '4s', '2c'],
     'hero_cards': ['Ah', 'Qd'],  # overcards facing donk
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},
    # DK-N-06: 8a CO (PFA=HJ), BB donks, BTN behind.
    # CORRECTION 4 (v3.5.1): action_history must include BTN preflop call between
    # CO call and BB call so that villain_positions=['BB','BTN'] is consistent
    # with active postflop player set.
    {'sub_scenario': '8a',
     'hero_pos': 'CO', 'villain_positions': ['BB', 'BTN'],
     'opener_position': 'HJ',
     'board': ['Th', '8s', '5d'],
     'hero_cards': ['Kc', 'Qs'],  # air on connected mid board
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'),
         ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},
    # DK-N-07: 8a CO (PFA=HJ). CORRECTION 4 applied (BTN call inserted).
    {'sub_scenario': '8a',
     'hero_pos': 'CO', 'villain_positions': ['BB', 'BTN'],
     'opener_position': 'HJ',
     'board': ['6d', '4c', '2h'],
     'hero_cards': ['Ac', '8d'],  # air-ish
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'),
         ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},
    # DK-N-08: 8b_co_calls BTN, PFA=CO, CO calls donk first
    {'sub_scenario': '8b_co_calls',
     'hero_pos': 'BTN', 'villain_positions': ['BB', 'CO'],
     'opener_position': 'CO',
     'board': ['Ks', '7d', '3h'],
     'hero_cards': ['Qd', 'Jc'],  # air
     'pot': 30.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
     ]},
    # DK-N-09: 8b_co_calls BTN, PFA=CO
    {'sub_scenario': '8b_co_calls',
     'hero_pos': 'BTN', 'villain_positions': ['BB', 'CO'],
     'opener_position': 'CO',
     'board': ['Ah', '5c', '4d'],
     'hero_cards': ['Tc', '8s'],  # air
     'pot': 30.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
     ]},
    # DK-N-10: 8e CO PFA, BTN behind
    {'sub_scenario': '8e',
     'hero_pos': 'CO', 'villain_positions': ['BB', 'BTN'],
     'opener_position': 'CO',
     'board': ['Jh', '7c', '4d'],
     'hero_cards': ['Ac', 'Qh'],  # overcards
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},
]


def generate_scenarios(forbidden_fingerprints: Set[Tuple[str, str]]) -> List[dict]:
    """Generate donk-bet defence scenario records (Module 8).

    Hero is IP (BTN or CO), villain is OOP (BB donk bettor).
    """
    records = []

    for i, tmpl in enumerate(_DONK_TEMPLATES):
        hero_cards = tmpl['hero_cards']
        board = tmpl['board']
        hero_cards_str = ''.join(hero_cards)
        board_str = ''.join(board)

        # Skip duplicate hero_cards if accidentally specified (e.g., 'Ks', 'Ks')
        if len(set(hero_cards)) != len(hero_cards):
            print(f"[WARN] Donk template {i} has duplicate hero cards: {hero_cards}, "
                  f"skipping", flush=True)
            continue

        fp = fingerprint(hero_cards_str, board_str)
        if fp in forbidden_fingerprints:
            continue

        spec = SituationSpec(
            hero_cards=hero_cards,
            board_cards=board,
            hero_pos=tmpl['hero_pos'],
            villain_positions=tmpl['villain_positions'],
            pot=tmpl['pot'],
            to_call=tmpl['to_call'],
            street=tmpl['street'],
            action_history=tmpl['action_history'],
            opener_position=tmpl.get('opener_position'),
        )

        sit_id = f"donk_{tmpl['sub_scenario']}_{i:03d}"
        record = build_record_from_spec(spec, sit_id, 'donk_bet_defence_scenarios')
        if record is None:
            continue

        # Verify hero is IP (BTN or CO)
        hero_pos = record.get('hero_position')
        if hero_pos not in ('BTN', 'CO'):
            print(f"[WARN] Donk scenario {sit_id} has hero_pos={hero_pos} "
                  f"(expected BTN or CO), skipping", flush=True)
            continue

        # Verify facing_bet=1
        if not record.get('facing_bet'):
            print(f"[WARN] Donk scenario {sit_id} has facing_bet=False, skipping",
                  flush=True)
            continue

        records.append(record)
        forbidden_fingerprints.add(fp)

    # Phase 6 v3.5.1 silent-failure assertion: every DONK record must have
    # facing_bet=1 (BB donk lead). Catches malformed templates that skip the
    # donk action history step.
    assert all(r['feat_dict'].get('facing_bet', 0) == 1 for r in records), \
        "DONK module produced records without facing_bet=1"

    return records
