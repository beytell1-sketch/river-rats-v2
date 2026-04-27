"""Facing-initial-bet scenario specs (CALL/RAISE/FOLD decisions).

Generates situations where hero faces an initial bet (not a raise) from villain.
These are the "normal c-bet situations" — villain bets first on a new street.

Blueprint Q2 Gap 4 / Q6 facing-initial-bet scenarios.
facing_bet=1 AND facing_raise=0 for all records.
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

# Templates: hero faces villain's INITIAL bet (no prior aggressive action on this street)
# Variety in hand strength, position, board texture, and street.

_FACING_BET_TEMPLATES: List[dict] = [
    # ─── FLOP: Hero OOP (BB) faces BTN c-bet ───
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Ks', '7h', '2c'],
     'hero_cards': ['Qd', 'Jc'],  # no pair (air on K-high)
     'pot': 15.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Ah', '5d', '2s'],
     'hero_cards': ['Td', '9h'],  # air on ace-high
     'pot': 14.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Jc', '8h', '3d'],
     'hero_cards': ['Jd', '5s'],  # top pair weak kicker
     'pot': 15.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Qh', 'Tc', '4d'],
     'hero_cards': ['Qs', '7h'],  # top pair
     'pot': 15.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Ts', '8s', '3c'],
     'hero_cards': ['7h', '6d'],  # open-ended straight draw
     'pot': 14.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},

    # ─── FLOP: Hero IP faces OOP check-bet (BB leads into IP) ───
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['9h', '6s', '2d'],
     'hero_cards': ['As', 'Kc'],  # overcards only
     'pot': 14.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['8d', '5c', '2h'],
     'hero_cards': ['Jc', 'Td'],  # overcards on low board
     'pot': 14.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},

    # ─── TURN: Hero OOP faces villain bet ───
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Kc', '7d', '2s', '5h'],
     'hero_cards': ['Kh', '4d'],  # top pair (turned)
     'pot': 25.0, 'to_call': 8.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
         ('turn', 'BB', 'check'), ('turn', 'BTN', 'bet'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Ah', '9c', '4d', 'Qh'],
     'hero_cards': ['8s', '7d'],  # air
     'pot': 26.0, 'to_call': 9.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'check'),
         ('turn', 'BB', 'check'), ('turn', 'CO', 'bet'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Ts', '8h', '3d', 'Jc'],
     'hero_cards': ['Qd', '9s'],  # straight (J-T-9-8-7... no wait QJ98T? Q9 = Q-high str8 draw, 7 outs... actually Q-9 = QJT-98 not quite; Q-9 on T-8-3-J has 7+4=... let's just use it as draw)
     'pot': 24.0, 'to_call': 8.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
         ('turn', 'BB', 'check'), ('turn', 'BTN', 'bet'),
     ]},

    # ─── RIVER: Hero OOP faces villain river bet ───
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Kd', '7s', '2h', '4c', '9d'],
     'hero_cards': ['Kh', '8c'],  # top pair on river
     'pot': 40.0, 'to_call': 12.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
         ('turn', 'BB', 'check'), ('turn', 'BTN', 'check'),
         ('river', 'BB', 'check'), ('river', 'BTN', 'bet'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Ac', '8h', '3s', 'Td', '6c'],
     'hero_cards': ['Js', '9d'],  # busted straight draw
     'pot': 38.0, 'to_call': 12.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'check'),
         ('turn', 'BB', 'check'), ('turn', 'CO', 'check'),
         ('river', 'BB', 'check'), ('river', 'CO', 'bet'),
     ]},

    # ─── 3-WAY: Hero faces bet in 3-way pot ───
    {'hero_pos': 'BB', 'villain_positions': ['CO', 'BTN'],
     'opener_position': 'CO',
     'board': ['Qd', '6s', '2c'],
     'hero_cards': ['9h', '8d'],  # air in 3-way
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['HJ', 'CO'],
     'opener_position': 'HJ',
     'board': ['Ks', 'Jc', '4h'],
     'hero_cards': ['Ac', '7d'],  # overcard with no pair
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'HJ', 'bet'),
     ]},

    # ─── Medium-made hand facing bet ───
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Th', '7d', '2s'],
     'hero_cards': ['Tc', '5h'],  # top pair weak kicker
     'pot': 15.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['9s', '8d', '3h'],
     'hero_cards': ['9d', 'Kc'],  # top pair mediocre kicker
     'pot': 14.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},
]


def generate_scenarios(forbidden_fingerprints: Set[Tuple[str, str]]) -> List[dict]:
    """Generate facing-initial-bet scenario records.

    All records have facing_bet=1 AND facing_raise=0.
    """
    records = []

    for i, tmpl in enumerate(_FACING_BET_TEMPLATES):
        hero_cards = tmpl['hero_cards']
        board = tmpl['board']
        hero_cards_str = ''.join(hero_cards)
        board_str = ''.join(board)

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

        sit_id = f"facing_bet_{i:03d}"
        record = build_record_from_spec(spec, sit_id, 'facing_initial_bet_scenarios')
        if record is None:
            continue

        # Verify facing_bet=1, facing_raise=0
        feat = record['feat_dict']
        if feat.get('facing_bet') != 1:
            print(f"[WARN] facing_bet scenario {sit_id} has facing_bet=0, skipping",
                  flush=True)
            continue
        if feat.get('facing_raise', 0) != 0:
            print(f"[WARN] facing_bet scenario {sit_id} has facing_raise=1 (unexpected), "
                  f"skipping", flush=True)
            continue

        records.append(record)
        forbidden_fingerprints.add(fp)

    return records
