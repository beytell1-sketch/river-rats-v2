"""Monster facing initial bet scenario specs (MW-33 RAISE pattern).

Hero holds a set or better (is_monster=1). Villain bets first on the street
(facing_bet=1, facing_raise=0).

Blueprint Q2 Gap 6 / Q6 monster-facing-bet scenarios.
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

# Monster templates: hero has set (or better).
# 'Set' = three of a kind using both hole cards + one board card.
# e.g., hero has [Ks, Kd], board has K (trips using pocket pair + board).
# Or hero has [Kh, Kc], board has [Kd, ...] — flopped set.

_MONSTER_TEMPLATES: List[dict] = [
    # ─── Flopped sets vs initial bet ───
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Ks', '7d', '2c'],
     'hero_cards': ['Kh', 'Kc'],  # flopped top set
     'pot': 15.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Qh', '8d', '3s'],
     'hero_cards': ['Qd', 'Qc'],  # flopped set of Qs
     'pot': 14.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Jc', '5d', '2h'],
     'hero_cards': ['Jh', 'Jd'],  # flopped set of Js
     'pot': 14.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),  # donk bet
     ]},
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['9s', '6c', '2d'],
     'hero_cards': ['9d', '9h'],  # flopped middle set
     'pot': 14.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'),
     ]},

    # ─── Monster on various textures ───
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Th', 'Td', '4c'],
     'hero_cards': ['Tc', '8s'],  # trips with kicker
     'pot': 15.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['8d', '8h', '3s'],
     'hero_cards': ['8c', 'Ac'],  # trips A kicker
     'pot': 14.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},

    # ─── Sets on 2-tone and dynamic boards ───
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Kd', 'Jd', '4c'],
     'hero_cards': ['Ks', 'Kh'],  # flopped set on 2-tone board
     'pot': 15.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['9h', '8s', '7d'],
     'hero_cards': ['9c', '9d'],  # set on dynamic connected board (3-way)
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'check'),
         ('flop', 'BTN', 'bet'),
     ]},

    # ─── Turn and river monsters ───
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Kc', '7h', '2s', 'Ks'],
     'hero_cards': ['Kd', '5c'],  # flopped set, rivered trips again
     'pot': 30.0, 'to_call': 10.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
         ('turn', 'BB', 'check'), ('turn', 'BTN', 'bet'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Qd', '5s', '2c', 'Jh', 'Qh'],
     'hero_cards': ['Qs', 'Tc'],  # rivered trips with Q
     'pot': 45.0, 'to_call': 15.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'check'),
         ('turn', 'BB', 'check'), ('turn', 'CO', 'check'),
         ('river', 'BB', 'check'), ('river', 'CO', 'bet'),
     ]},
]


def generate_scenarios(forbidden_fingerprints: Set[Tuple[str, str]]) -> List[dict]:
    """Generate monster facing initial bet scenario records.

    All records must have is_monster=1 and facing_bet=1.
    """
    records = []

    for i, tmpl in enumerate(_MONSTER_TEMPLATES):
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

        sit_id = f"monster_{i:03d}"
        record = build_record_from_spec(spec, sit_id, 'monster_facing_bet_scenarios')
        if record is None:
            continue

        # Verify is_monster=1
        feat = record['feat_dict']
        if feat.get('is_monster') != 1:
            # Not a monster per feature extractor — warn but may still have strong hand
            print(f"[WARN] Monster scenario {sit_id} has is_monster=0 "
                  f"(hand_category={feat.get('hand_category')}, "
                  f"is_strong_made={feat.get('is_strong_made')}), skipping",
                  flush=True)
            continue

        records.append(record)
        forbidden_fingerprints.add(fp)

    return records
