"""SB-as-hero sandwich scenario specs (Module 9).

Hero is the SB, sandwiched between an earlier-position aggressor and a later-position
caller. SB's tighter MDF (~20% vs BB's ~33%) means higher fold rates.

Blueprint Q6 Module 9 spec.
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

# SB-hero templates:
# Structure: CO opens, BTN calls, SB calls, BB folds; flop CO bets into SB (and BTN).
# Hero (SB) faces c-bet with BTN behind.
# Variants: BTN folded already, BTN called, or BTN still to act (pure sandwich).

_SB_HERO_TEMPLATES: List[dict] = [
    # NOTE: BB folded preflop in all scenarios below, so BB is NOT in villain_positions.
    # Acting order postflop (without BB): SB < CO < BTN (or SB < BTN for 2-way).
    # SB must act first (check/bet), then CO can bet, then BTN.

    # ─── SB faces CO c-bet with BTN still to act (pure sandwich) ───
    # 3-way: CO + BTN as villains (BB folded preflop)
    {'hero_pos': 'SB', 'villain_positions': ['CO', 'BTN'],
     'opener_position': 'CO',
     'board': ['Kh', '7d', '2s'],
     'hero_cards': ['Qc', 'Jh'],  # air on K-high
     'pot': 20.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    {'hero_pos': 'SB', 'villain_positions': ['CO', 'BTN'],
     'opener_position': 'CO',
     'board': ['Jc', '8h', '3d'],
     'hero_cards': ['Tc', '9s'],  # open-ended straight draw
     'pot': 20.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    {'hero_pos': 'SB', 'villain_positions': ['CO', 'BTN'],
     'opener_position': 'CO',
     'board': ['Ah', '5c', '2d'],
     'hero_cards': ['Kd', 'Qh'],  # overcards on A-high (air)
     'pot': 20.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    {'hero_pos': 'SB', 'villain_positions': ['CO', 'BTN'],
     'opener_position': 'CO',
     'board': ['9s', '8d', '3h'],
     'hero_cards': ['7c', '6d'],  # OESD (6-7 on 8-9 board)
     'pot': 20.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'bet'),
     ]},

    # ─── SB faces CO c-bet; BTN has called (bet-and-call sandwich) ───
    {'hero_pos': 'SB', 'villain_positions': ['CO', 'BTN'],
     'opener_position': 'CO',
     'board': ['Qs', '7h', '2c'],
     'hero_cards': ['Jd', 'Th'],  # air (OOP sandwich)
     'pot': 32.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BTN', 'call'),
     ]},
    {'hero_pos': 'SB', 'villain_positions': ['CO', 'BTN'],
     'opener_position': 'CO',
     'board': ['Tc', '6d', '2s'],
     'hero_cards': ['8h', '7c'],  # gutshot on low board
     'pot': 32.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BTN', 'call'),
     ]},

    # ─── SB faces BTN c-bet (2-way: SB + BTN, BB folded preflop) ───
    {'hero_pos': 'SB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Kc', '9h', '4d'],
     'hero_cards': ['Ac', '5s'],  # top pair weak kicker
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    {'hero_pos': 'SB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['8s', '5d', '2h'],
     'hero_cards': ['9c', '7d'],  # OESD on low board
     'pot': 17.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'BTN', 'bet'),
     ]},

    # ─── SB medium-made hand (potential call or fold) ───
    {'hero_pos': 'SB', 'villain_positions': ['CO', 'BTN'],
     'opener_position': 'CO',
     'board': ['Js', '7c', '2d'],
     'hero_cards': ['Jh', '5s'],  # top pair weak kicker (SB position = tighter MDF)
     'pot': 20.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    {'hero_pos': 'SB', 'villain_positions': ['CO', 'BTN'],
     'opener_position': 'CO',
     'board': ['Td', '8h', '3s'],
     'hero_cards': ['Th', '4c'],  # top pair very weak kicker
     'pot': 20.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'bet'),
     ]},

    # ─── SB turn decision facing aggression ───
    {'hero_pos': 'SB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Ks', '7d', '2c', '9h'],
     'hero_cards': ['Qc', 'Jh'],  # gutshot (turned)
     'pot': 35.0, 'to_call': 10.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'check'),
         ('turn', 'SB', 'check'), ('turn', 'CO', 'bet'),
     ]},
    {'hero_pos': 'SB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Ah', '8c', '3d', 'Ks'],
     'hero_cards': ['Jd', '9s'],  # air
     'pot': 35.0, 'to_call': 10.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'check'),
         ('turn', 'SB', 'check'), ('turn', 'CO', 'bet'),
     ]},

    # ─────────────────────────────────────────────────────────────────
    # SB-N (Phase 6 expansion v3.5): 7 new templates.
    # 4 flop (pot 18-20 BB, spr_std) + 3 turn (pot 32-36 BB, spr_med).
    # All hero=SB, BB folded preflop → BB NOT in villain_positions.
    # ─────────────────────────────────────────────────────────────────
    # SB-N-01: 3-way sandwich, CO+BTN villains
    {'hero_pos': 'SB', 'villain_positions': ['CO', 'BTN'],
     'opener_position': 'CO',
     'board': ['6d', '4s', '2h'],
     'hero_cards': ['Kh', 'Qc'],  # air
     'pot': 20.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # SB-N-02: 3-way sandwich
    {'hero_pos': 'SB', 'villain_positions': ['CO', 'BTN'],
     'opener_position': 'CO',
     'board': ['Qd', '5h', '3s'],
     'hero_cards': ['Jd', 'Tc'],  # air
     'pot': 20.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # SB-N-03: 2-way (BTN villain only, BB folded)
    {'hero_pos': 'SB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['9h', '6d', '3c'],
     'hero_cards': ['Ah', '8d'],  # air
     'pot': 18.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'),
         ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # SB-N-04: 3-way sandwich
    {'hero_pos': 'SB', 'villain_positions': ['CO', 'BTN'],
     'opener_position': 'CO',
     'board': ['Kc', '8d', '4h'],
     'hero_cards': ['Qd', 'Jh'],  # air
     'pot': 20.0, 'to_call': 6.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # SB-N-05: TURN spr_med (pot 34 → SPR 2.94)
    {'hero_pos': 'SB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Th', '7c', '2s', '6d'],
     'hero_cards': ['Kd', 'Qh'],  # air
     'pot': 34.0, 'to_call': 10.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'),
         ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'check'),
         ('turn', 'SB', 'check'), ('turn', 'CO', 'bet'),
     ]},
    # SB-N-06: TURN spr_med (pot 36 → SPR 2.78)
    {'hero_pos': 'SB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['As', '4d', '2c', '8h'],
     'hero_cards': ['Jh', 'Td'],  # air
     'pot': 36.0, 'to_call': 12.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'),
         ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'CO', 'check'),
         ('turn', 'SB', 'check'), ('turn', 'CO', 'bet'),
     ]},
    # SB-N-07: TURN spr_med (pot 32 → SPR 3.13)
    {'hero_pos': 'SB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Jd', '9s', '5h', '3c'],
     'hero_cards': ['Kc', 'Qd'],  # air
     'pot': 32.0, 'to_call': 10.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'),
         ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'BTN', 'check'),
         ('turn', 'SB', 'check'), ('turn', 'BTN', 'bet'),
     ]},
    # SB-N-08 (Phase 8 v3.6): 2-way SB vs BTN, pot 17 → SPR 5.88 (spr_std).
    # Distinct from existing SB boards. {sb, spr_std} → routes sb (1.05 > 0.39).
    {'hero_pos': 'SB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Qs', '6c', '2d'],
     'hero_cards': ['8h', '7h'],  # backdoor straight
     'pot': 17.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
         ('flop', 'SB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
]


def generate_scenarios(forbidden_fingerprints: Set[Tuple[str, str]]) -> List[dict]:
    """Generate SB-as-hero sandwich scenario records.

    All records must have hero_position='SB'.
    gto-expert N5 advisory: expect FOLD rate > 30% in labelled results.
    """
    records = []

    for i, tmpl in enumerate(_SB_HERO_TEMPLATES):
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

        sit_id = f"sb_hero_{i:03d}"
        record = build_record_from_spec(spec, sit_id, 'sb_hero_scenarios')
        if record is None:
            continue

        # Verify hero_position='SB'
        if record.get('hero_position') != 'SB':
            print(f"[WARN] SB-hero scenario {sit_id} has hero_position="
                  f"{record.get('hero_position')} (expected SB), skipping",
                  flush=True)
            continue

        records.append(record)
        forbidden_fingerprints.add(fp)

    return records
