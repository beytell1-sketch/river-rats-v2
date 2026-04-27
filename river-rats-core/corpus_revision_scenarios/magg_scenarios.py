"""Multi-street aggression (MAGG) scenario specs (MW-50 pattern).

CORRECTED (R3 fix): All scenarios use RIVER decision points so that
villain_aggression_count=2 (villain bet BOTH flop and turn as prior streets).

Blueprint Q2 Gap 3 / Q6 MAGG scenarios.
All records: villain_aggression_count==2, street='river'.
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

# All MAGG templates are RIVER decisions.
# CRITICAL: villain_aggression_count counts PRIOR STREET bets by the primary villain.
# The primary villain is determined by the bridge: when facing a bet, it's the last villain
# in the villain_positions list; otherwise the first.
#
# The bridge also counts PREFLOP raises as aggression if the villain is the preflop aggressor.
# To get exactly villain_aggression_count=2 at the river:
# - Villain must be the CALLER preflop (NOT the raiser) — so preflop doesn't add to count
# - Villain must bet on EXACTLY 2 prior streets (e.g. flop + turn)
# Pattern: hero opens, villain (BB) calls preflop; BB bets flop + turn = aggression=2 at river.

_MAGG_TEMPLATES: List[dict] = [
    # ─── MAGG-1: BB (villain) bets flop + turn; hero is CO (opener) faces river ───
    # Hero CO = opener; BB = caller preflop; BB bets flop + bets turn => aggression=2 at river
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Kd', '7s', '2c', '5h', 'Jd'],
     'hero_cards': ['Ah', 'Tc'],  # air on river
     'pot': 50.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Qs', '8h', '3c', 'Td', '6s'],
     'hero_cards': ['Jh', '9d'],  # busted straight draw
     'pot': 52.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},

    # ─── MAGG-2: Same pattern — different board textures ───
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Jh', 'Td', '4c', '8s', '2h'],
     'hero_cards': ['Kd', '7c'],  # medium-made (K-high)
     'pot': 55.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Ah', '9c', '4d', '2s', 'Kh'],
     'hero_cards': ['Tc', '8d'],  # air
     'pot': 50.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},

    # ─── MAGG-3: BB check-raises flop (aggression=1) + bets turn (aggression=2) ───
    # CO hero faces river after calling both
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['9h', '6c', '2s', 'Td', '5d'],
     'hero_cards': ['Qc', 'Jc'],  # air
     'pot': 80.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'CO', 'check'), ('flop', 'BB', 'check'),  # CO checks (OOP-first on flop)
         # Wait: CO is OOP to BB postflop? No - CO acts before BTN, but SB acts before BB.
         # Postflop order: SB < BB < CO < BTN. So CO acts AFTER BB.
         # With CO + BB 2-way: BB acts first (OOP), then CO (IP).
         # To have BB check-raise, BB must check, CO bets, BB raises.
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
         ('flop', 'BB', 'raise'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['8s', '5c', '2h', 'Jd', '4s'],
     'hero_cards': ['Ad', 'Kc'],  # air (missed overcards)
     'pot': 75.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
         ('flop', 'BB', 'raise'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},

    # ─── Hero facing river bet after calling two streets (BB bets into hero) ───
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Kc', '9d', '3h', '7s', 'Qc'],
     'hero_cards': ['Js', 'Ts'],  # medium-made: turned straight draw, missed
     'pot': 60.0, 'to_call': 20.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
         ('river', 'BB', 'bet'),
     ]},
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Ah', '8c', '4d', '6s', '2h'],
     'hero_cards': ['Kd', 'Qh'],  # air (missed overcards)
     'pot': 58.0, 'to_call': 18.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
         ('river', 'BB', 'bet'),
     ]},

    # ─── Medium-made hand facing aggression (FOLD candidate) ───
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Ks', '8d', '3c', 'Jh', '9s'],
     'hero_cards': ['Kh', '6d'],  # top pair (mediocre kicker) — possible fold vs 3-barrel
     'pot': 65.0, 'to_call': 22.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
         ('river', 'BB', 'bet'),
     ]},
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Qd', '7h', '2c', 'Tc', '5d'],
     'hero_cards': ['Qc', '5s'],  # two pair Q5
     'pot': 62.0, 'to_call': 20.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
         ('river', 'BB', 'bet'),
     ]},
]


def generate_scenarios(forbidden_fingerprints: Set[Tuple[str, str]]) -> List[dict]:
    """Generate multi-street aggression scenario records.

    CRITICAL: All records must have villain_aggression_count==2 at RIVER decision.
    Any record with villain_aggression_count != 2 is filtered out with a warning.
    """
    records = []

    for i, tmpl in enumerate(_MAGG_TEMPLATES):
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

        sit_id = f"magg_{i:03d}"
        record = build_record_from_spec(spec, sit_id, 'magg_scenarios')
        if record is None:
            continue

        # CRITICAL: villain_aggression_count MUST be 2
        agg = record['feat_dict'].get('villain_aggression_count', 0)
        if agg != 2:
            print(f"[WARN] MAGG scenario {sit_id} has villain_aggression_count={agg} "
                  f"(expected 2). Action history may be truncated. Skipping.",
                  flush=True)
            continue

        records.append(record)
        forbidden_fingerprints.add(fp)

    return records
