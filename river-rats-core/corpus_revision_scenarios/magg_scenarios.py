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

    # ─────────────────────────────────────────────────────────────────
    # MAGG-A Group (Phase 6 expansion v3.5): pot 50-75 BB, fills magg quota.
    # All match {magg, pfa}; assigned to magg (scarcity higher).
    # 30 templates: BB bets flop+turn (some + river), or BB check-raise + turn bet.
    # Hero=CO or BTN opener; villain=BB caller (Bug 1 compliant).
    # ─────────────────────────────────────────────────────────────────
    # MAGG-A-01: BB bets flop+turn; hero CO checks river
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['7c', '4h', '2s', '9d', 'Jc'],
     'hero_cards': ['Ah', 'Qd'],  # air missed
     'pot': 55.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-A-02
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['6s', '3d', '2h', '8s', 'Kd'],
     'hero_cards': ['Jc', 'Tc'],  # busted
     'pot': 52.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-A-03
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Qc', '5d', '3h', '7c', '2s'],
     'hero_cards': ['Kd', 'Jh'],  # air
     'pot': 58.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-A-04 (Phase 8 v3.6: pot 50→52 to remove spr_med eligibility; SPR 1.923)
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Th', '4d', '2c', '6h', 'Ac'],
     'hero_cards': ['9s', '8d'],  # busted
     'pot': 52.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-A-05
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Jd', '8c', '3s', '5h', '2d'],
     'hero_cards': ['Kh', 'Qc'],  # air
     'pot': 60.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-A-06: faces river bet
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['9c', '6h', '2d', 'Ks', 'Ts'],
     'hero_cards': ['Ad', '7c'],  # air
     'pot': 55.0, 'to_call': 18.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
         ('river', 'BB', 'bet'),
     ]},
    # MAGG-A-07
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['As', '7d', '3c', 'Jh', '5s'],
     'hero_cards': ['Qh', 'Tc'],  # air
     'pot': 62.0, 'to_call': 20.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
         ('river', 'BB', 'bet'),
     ]},
    # MAGG-A-08: BB check-raises flop, bets turn
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Kh', '5c', '2d', '8h', '4s'],
     'hero_cards': ['Jd', '9s'],  # air
     'pot': 58.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
         ('flop', 'BB', 'raise'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-A-09
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['8d', '6s', '3h', 'Qc', 'Th'],
     'hero_cards': ['Ah', '7d'],  # air
     'pot': 65.0, 'to_call': 22.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
         ('river', 'BB', 'bet'),
     ]},
    # MAGG-A-10
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Td', '9c', '5h', '3s', '7d'],
     'hero_cards': ['Ks', 'Qh'],  # air
     'pot': 54.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-A-11
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Jh', '6d', '4c', '2h', '9s'],
     'hero_cards': ['Ac', '8s'],  # air
     'pot': 60.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-A-12
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Qh', '4s', '2d', '6c', 'Kh'],
     'hero_cards': ['Tc', '8d'],  # air
     'pot': 57.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-A-13
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['7s', '5h', '2c', 'Ah', '3d'],
     'hero_cards': ['Kd', 'Jc'],  # air
     'pot': 63.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-A-14: faces river bet (Phase 8 v3.6: pot 50→52 to remove spr_med eligibility; SPR 1.923)
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Kc', '8h', '4d', '2s', 'Qd'],
     'hero_cards': ['Jh', '9s'],  # air
     'pot': 52.0, 'to_call': 17.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
         ('river', 'BB', 'bet'),
     ]},
    # MAGG-A-15: BB check-raises flop
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Ac', '6h', '3s', '9d', '5h'],
     'hero_cards': ['Ks', 'Qd'],  # air
     'pot': 68.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
         ('flop', 'BB', 'raise'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-A-16
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Js', '9d', '4c', '2h', '6s'],
     'hero_cards': ['Ah', 'Kc'],  # air
     'pot': 55.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-A-17: faces river bet, two pair
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['5d', '3h', '2c', 'Jc', '8h'],
     'hero_cards': ['Qd', 'Qh'],  # overpair
     'pot': 70.0, 'to_call': 23.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
         ('river', 'BB', 'bet'),
     ]},
    # MAGG-A-18
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Th', '7s', '3d', 'Qc', '2h'],
     'hero_cards': ['Kd', '9c'],  # air
     'pot': 52.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-A-19
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['9s', '6d', '2h', '4c', 'Ks'],
     'hero_cards': ['Jh', 'Td'],  # air
     'pot': 60.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-A-20
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['As', '3c', '2d', '7h', 'Jd'],
     'hero_cards': ['9h', '8c'],  # air
     'pot': 53.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-A-21: faces river bet
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Qd', '8h', '5s', '3d', 'Ah'],
     'hero_cards': ['Kc', 'Jd'],  # air
     'pot': 56.0, 'to_call': 19.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
         ('river', 'BB', 'bet'),
     ]},
    # MAGG-A-22: BB check-raises flop
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['6h', '4d', '3s', 'Tc', '9h'],
     'hero_cards': ['Ad', 'Ks'],  # air
     'pot': 65.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
         ('flop', 'BB', 'raise'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-A-23
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Kh', '7c', '4d', '2s', '8d'],
     'hero_cards': ['Qs', 'Jh'],  # air
     'pot': 58.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-A-24
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Jc', '5h', '2d', '9s', 'Kd'],
     'hero_cards': ['Ac', 'Td'],  # air
     'pot': 55.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-A-25
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['8h', '5d', '3c', '6s', 'Qs'],
     'hero_cards': ['Ah', '7s'],  # air
     'pot': 62.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-A-26 (Phase 8 v3.6: pot 50→53 to remove spr_med eligibility; SPR 1.887)
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Qc', '9h', '6d', '3s', 'Td'],
     'hero_cards': ['Kh', 'Jd'],  # air
     'pot': 53.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-A-27: faces river bet
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['7h', '4s', '2d', '5c', 'Jh'],
     'hero_cards': ['Kc', 'Qs'],  # air
     'pot': 60.0, 'to_call': 20.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
         ('river', 'BB', 'bet'),
     ]},
    # MAGG-A-28
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Ah', '8d', '3s', '6c', '2h'],
     'hero_cards': ['Js', '9d'],  # air
     'pot': 54.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-A-29
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Th', '6c', '3d', '4h', 'Qs'],
     'hero_cards': ['Kd', 'Jh'],  # air
     'pot': 57.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-A-30: faces river bet
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['9d', '5s', '2c', '8h', 'Kc'],
     'hero_cards': ['Ah', 'Qd'],  # air
     'pot': 63.0, 'to_call': 21.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
         ('river', 'BB', 'bet'),
     ]},

    # ─────────────────────────────────────────────────────────────────
    # MAGG-B Group (Phase 6 expansion v3.5): pot 26-45 BB → SPR 2.22-3.85.
    # Overflow to spr_med after magg fills (40/40).
    # 22 templates with same structural patterns.
    # ─────────────────────────────────────────────────────────────────
    # MAGG-B-01
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['7d', '3h', '2c', '5s', 'Tc'],
     'hero_cards': ['Ah', 'Kd'],  # air
     'pot': 32.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-B-02
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['6c', '4s', '2d', '8h', 'Js'],
     'hero_cards': ['Kd', 'Qh'],  # air
     'pot': 28.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-B-03: faces river bet
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Jd', '7c', '3s', '5h', 'Ah'],
     'hero_cards': ['Qs', 'Td'],  # air
     'pot': 35.0, 'to_call': 12.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
         ('river', 'BB', 'bet'),
     ]},
    # MAGG-B-04
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Tc', '8s', '2h', '4d', '6c'],
     'hero_cards': ['Kh', 'Jd'],  # air
     'pot': 30.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-B-05
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['9s', '5d', '2c', '7h', 'Kd'],
     'hero_cards': ['Ac', 'Jh'],  # air
     'pot': 40.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-B-06: BB check-raises flop
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Qs', '6h', '3d', '2c', '8s'],
     'hero_cards': ['Th', '9c'],  # air
     'pot': 33.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
         ('flop', 'BB', 'raise'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-B-07
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['8c', '4h', '2s', '6d', 'Jc'],
     'hero_cards': ['Kd', 'Qs'],  # air
     'pot': 27.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-B-08: faces river bet
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Kd', '5s', '3h', '9c', '2d'],
     'hero_cards': ['Ah', 'Jc'],  # air
     'pot': 38.0, 'to_call': 13.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
         ('river', 'BB', 'bet'),
     ]},
    # MAGG-B-09
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Ts', '7h', '4c', '2d', '8s'],
     'hero_cards': ['Qd', 'Jh'],  # air
     'pot': 32.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-B-10: faces river bet
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['5c', '3s', '2h', '9d', 'Ks'],
     'hero_cards': ['Ad', 'Tc'],  # air
     'pot': 45.0, 'to_call': 15.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
         ('river', 'BB', 'bet'),
     ]},
    # MAGG-B-11
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Jh', '8d', '5s', '3c', 'Qs'],
     'hero_cards': ['Kc', '9h'],  # air
     'pot': 30.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-B-12: BB check-raises flop
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Ac', '7s', '4h', '2d', '6c'],
     'hero_cards': ['Kd', 'Jh'],  # air
     'pot': 35.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
         ('flop', 'BB', 'raise'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-B-13
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['9h', '6c', '3d', '5s', 'Td'],
     'hero_cards': ['Qs', 'Jc'],  # air
     'pot': 28.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-B-14: faces river bet
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Kh', '4d', '2c', '7s', 'Jh'],
     'hero_cards': ['Ah', 'Qc'],  # air
     'pot': 40.0, 'to_call': 14.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
         ('river', 'BB', 'bet'),
     ]},
    # MAGG-B-15
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['7s', '5c', '2h', '4d', 'Qs'],
     'hero_cards': ['Kh', 'Jd'],  # air
     'pot': 32.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-B-16
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Qd', '8c', '3s', '6h', '2d'],
     'hero_cards': ['Ac', 'Td'],  # air
     'pot': 27.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-B-17
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['8s', '6d', '3h', '5c', 'Kc'],
     'hero_cards': ['Jd', '9h'],  # air
     'pot': 36.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-B-18: faces river bet
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['As', '5h', '3d', '7c', '2s'],
     'hero_cards': ['Ks', 'Jd'],  # air
     'pot': 42.0, 'to_call': 14.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
         ('river', 'BB', 'bet'),
     ]},
    # MAGG-B-19
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Jc', '7d', '4s', '2h', 'Qs'],
     'hero_cards': ['Kh', 'Td'],  # air
     'pot': 30.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-B-20: BB check-raises flop
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['9c', '4h', '2s', '6d', 'Ah'],
     'hero_cards': ['Ks', 'Qd'],  # air
     'pot': 34.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
         ('flop', 'BB', 'raise'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
     ]},
    # MAGG-B-21
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['Th', '8s', '3c', '5d', 'Kd'],
     'hero_cards': ['Ac', 'Jh'],  # air
     'pot': 38.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-B-22: faces river bet
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['Qs', '6s', '4d', '2c', '7h'],
     'hero_cards': ['Kd', 'Jc'],  # air
     'pot': 44.0, 'to_call': 15.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
         ('river', 'BB', 'bet'),
     ]},

    # ─────────────────────────────────────────────────────────────────
    # MAGG-NEW Group (Phase 8 v3.6): 2 pure-magg templates with pot > 50.
    # SPR < 2.0 → no spr_med eligibility. {magg, pfa} routing → magg.
    # ─────────────────────────────────────────────────────────────────
    # MAGG-NEW-01: CO opener, pot 54 → SPR 1.852
    {'hero_pos': 'CO', 'villain_positions': ['BB'],
     'opener_position': 'CO',
     'board': ['3c', '2h', '7d', 'Ks', 'Td'],
     'hero_cards': ['Ac', 'Jh'],  # air on river
     'pot': 54.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'),
     ]},
    # MAGG-NEW-02: BTN opener, pot 56 → SPR 1.786
    {'hero_pos': 'BTN', 'villain_positions': ['BB'],
     'opener_position': 'BTN',
     'board': ['5h', '2c', '9s', 'Qd', '4h'],
     'hero_cards': ['Kd', '8c'],  # air on river
     'pot': 56.0, 'to_call': 0.0, 'street': 'river',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'),
         ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'),
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
