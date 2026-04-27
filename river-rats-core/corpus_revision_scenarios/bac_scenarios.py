"""Bet-and-call (BAC) sandwich scenario specs (MW-30 pattern).

Hero faces a bet that has already been called by another player.
num_callers_to_bet >= 1.

Blueprint Q2 Gap 4 / Q6 BAC scenarios.
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

# BAC scenario templates:
# Structure: BTN bets, SB calls, hero (BB) faces bet-and-call
# OR: CO bets, BTN calls, hero (BB or SB) faces bet-and-call

_BAC_TEMPLATES: List[dict] = [
    # ─── BAC-1: BTN c-bets, SB calls, hero (BB) faces on flop ───
    {'hero_pos': 'BB', 'villain_positions': ['SB', 'BTN'],
     'opener_position': 'BTN',
     'board': ['Ks', '7d', '2c'],
     'hero_cards': ['Qh', 'Jd'],   # air on K-high
     'pot': 20.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'SB', 'check'), ('flop', 'BB', 'check'),
         ('flop', 'BTN', 'bet'), ('flop', 'SB', 'call'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['SB', 'BTN'],
     'opener_position': 'BTN',
     'board': ['Jh', '8c', '3d'],
     'hero_cards': ['Kd', 'Qs'],   # overcards (two live)
     'pot': 20.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'SB', 'check'), ('flop', 'BB', 'check'),
         ('flop', 'BTN', 'bet'), ('flop', 'SB', 'call'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['SB', 'BTN'],
     'opener_position': 'BTN',
     'board': ['9h', '8c', '4d'],
     'hero_cards': ['Th', '7d'],   # OESD (open-ended straight draw)
     'pot': 20.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'SB', 'check'), ('flop', 'BB', 'check'),
         ('flop', 'BTN', 'bet'), ('flop', 'SB', 'call'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['SB', 'BTN'],
     'opener_position': 'BTN',
     'board': ['As', '6c', '2d'],
     'hero_cards': ['Ac', '4h'],   # top pair weak kicker
     'pot': 20.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'SB', 'check'), ('flop', 'BB', 'check'),
         ('flop', 'BTN', 'bet'), ('flop', 'SB', 'call'),
     ]},

    # ─── BAC-2: Same structure on the turn ───
    {'hero_pos': 'BB', 'villain_positions': ['SB', 'BTN'],
     'opener_position': 'BTN',
     'board': ['Kd', '7s', '2h', 'Tc'],
     'hero_cards': ['Qc', 'Jh'],   # straight draw on turn
     'pot': 35.0, 'to_call': 10.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
         ('turn', 'SB', 'check'), ('turn', 'BB', 'check'),
         ('turn', 'BTN', 'bet'), ('turn', 'SB', 'call'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['SB', 'BTN'],
     'opener_position': 'BTN',
     'board': ['Ah', '9c', '3d', '8s'],
     'hero_cards': ['Tc', '7h'],   # gutshot straight draw
     'pot': 36.0, 'to_call': 10.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
         ('turn', 'SB', 'check'), ('turn', 'BB', 'check'),
         ('turn', 'BTN', 'bet'), ('turn', 'SB', 'call'),
     ]},

    # ─── BAC-3: With prior aggression (villain_aggression_count >= 1) ───
    {'hero_pos': 'BB', 'villain_positions': ['SB', 'BTN'],
     'opener_position': 'BTN',
     'board': ['Jc', '8h', '3d', 'Ks'],
     'hero_cards': ['9d', '7s'],   # air
     'pot': 45.0, 'to_call': 14.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'SB', 'check'), ('flop', 'BB', 'check'),
         ('flop', 'BTN', 'bet'), ('flop', 'SB', 'call'), ('flop', 'BB', 'call'),
         ('turn', 'SB', 'check'), ('turn', 'BB', 'check'),
         ('turn', 'BTN', 'bet'), ('turn', 'SB', 'call'),
     ]},
    {'hero_pos': 'BB', 'villain_positions': ['SB', 'BTN'],
     'opener_position': 'BTN',
     'board': ['Qh', '7c', '2s', '5d'],
     'hero_cards': ['Ad', 'Kh'],  # overcards / air
     'pot': 46.0, 'to_call': 14.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'SB', 'check'), ('flop', 'BB', 'check'),
         ('flop', 'BTN', 'bet'), ('flop', 'SB', 'call'), ('flop', 'BB', 'call'),
         ('turn', 'SB', 'check'), ('turn', 'BB', 'check'),
         ('turn', 'BTN', 'bet'), ('turn', 'SB', 'call'),
     ]},

    # ─── CO bets, BTN calls, hero (SB) faces sandwich ───
    # NOTE: BB folded preflop, so BB is NOT in villain_positions.
    # Active players postflop: SB (hero), BTN, CO.
    # villain_positions: CO is LAST (bettor); BTN is the caller.
    # Bridge: last in villain_positions = bettor; BTN (not last, not hero) = caller.
    {'hero_pos': 'SB', 'villain_positions': ['BTN', 'CO'],
     'opener_position': 'CO',
     'board': ['Td', '6h', '2c'],
     'hero_cards': ['8s', '7d'],  # gutshot
     'pot': 24.0, 'to_call': 7.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'),
         ('flop', 'CO', 'bet'), ('flop', 'BTN', 'call'),
     ]},
]


def generate_scenarios(forbidden_fingerprints: Set[Tuple[str, str]]) -> List[dict]:
    """Generate bet-and-call sandwich scenario records.

    All records must have num_callers_to_bet >= 1.
    """
    records = []

    for i, tmpl in enumerate(_BAC_TEMPLATES):
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

        sit_id = f"bac_{i:03d}"
        record = build_record_from_spec(spec, sit_id, 'bac_scenarios')
        if record is None:
            continue

        # Verify num_callers_to_bet >= 1
        callers = record['feat_dict'].get('num_callers_to_bet', 0)
        if callers < 1:
            print(f"[WARN] BAC scenario {sit_id} has num_callers_to_bet={callers} "
                  f"(expected >= 1), skipping", flush=True)
            continue

        records.append(record)
        forbidden_fingerprints.add(fp)

    return records
