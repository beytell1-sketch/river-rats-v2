"""PFA c-bet scenario specs (Rule 4 pattern).

Generates situations where hero is the preflop aggressor (IS_PFA=1) facing
a postflop decision. These are the c-bet decisions missing from the original pool
because the generator didn't capture opener_position.

Blueprint Q2 Gap 1 / Q6 Module spec.
Scenarios: PFA-1 (CO opener), PFA-2 (BTN opener), PFA-3 (HJ opener),
           PFA-4 (turn c-bet, capped at <=10 hands).
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
    is_duplicate,
    add_to_forbidden,
)

# PFA scenario specs: (hero_pos, villain_positions, opener_position, board, hero_cards,
#                      pot_bb, street, action_history_postflop)
#
# Blueprint: pot 12.5-25.0 BB for SPR 4-8 (standard early-street).
# All are flop decisions except PFA-4 (turn).

_PFA_TEMPLATES: List[dict] = [
    # ─────────────────────────────────────────────────────────────────
    # PFA-1: CO opener, BTN + BB callers (dry flop)
    # ─────────────────────────────────────────────────────────────────
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Ks', '7d', '2c'],  # dry rainbow
     'hero_cards': ['Ac', 'Qh'],
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-1a'},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Qh', '8d', '3s'],
     'hero_cards': ['Kd', 'Jc'],
     'pot': 16.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-1b'},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Jc', '6h', '2d'],  # low dry board
     'hero_cards': ['As', 'Kh'],
     'pot': 14.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-1c'},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Td', '7h', '2s'],
     'hero_cards': ['Kc', 'Qd'],
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-1d'},
    # Two-tone boards for CO opener
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Ah', '8h', '3c'],
     'hero_cards': ['Ks', 'Qd'],
     'pot': 16.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-1e'},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Kd', '9d', '4c'],
     'hero_cards': ['Ac', 'Jh'],
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-1f'},
    # Monster hands (CO opener)
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Ks', 'Kd', '4c'],
     'hero_cards': ['Kc', 'Qs'],  # trips
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-1g'},

    # ─────────────────────────────────────────────────────────────────
    # PFA-2: BTN opener, SB + BB callers
    # ─────────────────────────────────────────────────────────────────
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['Ac', '7h', '2d'],
     'hero_cards': ['Kh', 'Qd'],
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-2a'},
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['Th', '6s', '2c'],
     'hero_cards': ['Jd', 'Tc'],  # top pair top kicker
     'pot': 16.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-2b'},
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['Qd', '5s', '3h'],
     'hero_cards': ['As', 'Kc'],
     'pot': 14.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-2c'},
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['9h', '8c', '4d'],
     'hero_cards': ['Qc', 'Jd'],  # connected board with gutshot
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-2d'},
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['Jh', 'Td', '5c'],
     'hero_cards': ['Qs', 'Jd'],  # top pair + straight draw
     'pot': 16.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-2e'},

    # ─────────────────────────────────────────────────────────────────
    # PFA-3: HJ opener, CO + BB callers
    # ─────────────────────────────────────────────────────────────────
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['Kh', '9c', '3d'],
     'hero_cards': ['Ah', 'Kd'],  # top pair top kicker
     'pot': 14.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-3a'},
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['As', '4h', '2c'],
     'hero_cards': ['Jc', 'Jd'],  # overpair to board (JJ vs A-high)
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-3b'},
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['8d', '5s', '2h'],
     'hero_cards': ['Qs', 'Qc'],  # overpair (dry low board)
     'pot': 14.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-3c'},
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['Th', '6c', '2d'],
     'hero_cards': ['Kd', 'Kh'],  # overpair (big pair)
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-3d'},
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['7d', '4h', '2s'],
     'hero_cards': ['Ac', '7h'],  # top pair
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-3e'},

    # ─────────────────────────────────────────────────────────────────
    # PFA-4: Turn c-bet (capped at <=10 hands — PFA checked flop, leads turn)
    # SPR ~4-5 on the turn (pot ~20-25 BB after flop check-check)
    # ─────────────────────────────────────────────────────────────────
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Ks', '7d', '2c', 'Ah'],  # turn board
     'hero_cards': ['Ac', 'Qh'],  # now top pair
     'pot': 20.0, 'to_call': 0.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'), ('flop', 'BB', 'check'),
     ],
     'label': 'PFA-4a'},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Qh', '8d', '3s', 'Kc'],
     'hero_cards': ['Kd', 'Jc'],  # now top pair
     'pot': 21.0, 'to_call': 0.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'), ('flop', 'BB', 'check'),
     ],
     'label': 'PFA-4b'},
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['Ac', '7h', '2d', 'Js'],
     'hero_cards': ['Kh', 'Qd'],
     'pot': 20.0, 'to_call': 0.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
     ],
     'label': 'PFA-4c'},
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['Kh', '9c', '3d', 'Td'],
     'hero_cards': ['Ah', 'Kd'],
     'pot': 22.0, 'to_call': 0.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'HJ', 'check'), ('flop', 'CO', 'check'), ('flop', 'BB', 'check'),
     ],
     'label': 'PFA-4d'},
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['Th', '6s', '2c', '9d'],
     'hero_cards': ['Jd', 'Tc'],
     'pot': 20.0, 'to_call': 0.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
     ],
     'label': 'PFA-4e'},

    # ─────────────────────────────────────────────────────────────────
    # PFA-5 (Phase 6 expansion v3.5): HJ opener, CO+BB callers (8 templates)
    # New flop textures (paired, monotone, connected) not in PFA-3.
    # ─────────────────────────────────────────────────────────────────
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['Ac', '9s', '4d'],  # A-high dry
     'hero_cards': ['Kh', 'Qd'],
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-5a'},
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['Ks', '8c', '3h'],
     'hero_cards': ['Jc', 'Jd'],
     'pot': 14.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-5b'},
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['Qc', '6d', '2s'],
     'hero_cards': ['Ah', 'Kd'],
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-5c'},
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['Jd', '9s', '5c'],
     'hero_cards': ['Ks', 'Qh'],
     'pot': 14.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-5d'},
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['Tc', '4d', '2h'],
     'hero_cards': ['Ad', 'Qc'],
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-5e'},
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['8s', '8d', '3c'],  # paired flop
     'hero_cards': ['Ah', 'Kc'],
     'pot': 14.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-5f'},
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['Kd', '6c', '6s'],  # paired flop
     'hero_cards': ['Qs', 'Jd'],
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-5g'},
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['5h', '5d', '2c'],  # paired flop
     'hero_cards': ['Kc', 'Kd'],
     'pot': 14.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-5h'},

    # ─────────────────────────────────────────────────────────────────
    # PFA-6 (Phase 6): CO opener, BTN+BB callers (10 templates)
    # Dynamic and connected boards, vary hero hand types.
    # ─────────────────────────────────────────────────────────────────
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Ad', '6s', '3d'],
     'hero_cards': ['Kh', 'Jd'],
     'pot': 16.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-6a'},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Jc', '7s', '4h'],
     'hero_cards': ['Ac', '9c'],
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-6b'},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Qs', '9d', '8c'],  # connected
     'hero_cards': ['Kh', 'Kd'],
     'pot': 16.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-6c'},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Tc', '9s', '8d'],  # 3-connected
     'hero_cards': ['Jd', '7c'],
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-6d'},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Ah', '7c', '4s'],
     'hero_cards': ['Qd', 'Qs'],
     'pot': 16.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-6e'},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Kc', '5s', '3h'],
     'hero_cards': ['Ac', 'Jc'],
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-6f'},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['9h', '9c', '2d'],  # paired flop
     'hero_cards': ['Kd', 'Kh'],
     'pot': 16.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-6g'},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Qd', 'Jh', '5c'],  # broadway-heavy
     'hero_cards': ['As', 'Kh'],
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-6h'},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['8h', '6c', '4d'],  # connected low
     'hero_cards': ['Kc', 'Qd'],
     'pot': 16.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-6i'},
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['5c', '5s', '3d'],  # paired low
     'hero_cards': ['Ah', 'Qs'],
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-6j'},

    # ─────────────────────────────────────────────────────────────────
    # PFA-7 (Phase 6): BTN opener, CO+SB callers, BB folds (8 templates)
    # BB folded preflop → BB NOT in villain_positions.
    # ─────────────────────────────────────────────────────────────────
    {'hero_pos': 'BTN', 'villain_positions': ['CO', 'SB'],
     'opener_position': 'BTN',
     'board': ['Kd', '8s', '2h'],
     'hero_cards': ['Ah', 'Jd'],
     'pot': 20.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'CO', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
     ],
     'label': 'PFA-7a'},
    {'hero_pos': 'BTN', 'villain_positions': ['CO', 'SB'],
     'opener_position': 'BTN',
     'board': ['Qh', '7d', '4c'],
     'hero_cards': ['Kc', 'Ks'],
     'pot': 20.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'CO', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
     ],
     'label': 'PFA-7b'},
    {'hero_pos': 'BTN', 'villain_positions': ['CO', 'SB'],
     'opener_position': 'BTN',
     'board': ['Jd', '6s', '3c'],
     'hero_cards': ['Ac', 'Qd'],
     'pot': 20.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'CO', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
     ],
     'label': 'PFA-7c'},
    {'hero_pos': 'BTN', 'villain_positions': ['CO', 'SB'],
     'opener_position': 'BTN',
     'board': ['Th', '5d', '2s'],
     'hero_cards': ['Kh', 'Jc'],
     'pot': 20.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'CO', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
     ],
     'label': 'PFA-7d'},
    {'hero_pos': 'BTN', 'villain_positions': ['CO', 'SB'],
     'opener_position': 'BTN',
     'board': ['Ah', '4c', '2d'],
     'hero_cards': ['9h', '9d'],
     'pot': 20.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'CO', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
     ],
     'label': 'PFA-7e'},
    {'hero_pos': 'BTN', 'villain_positions': ['CO', 'SB'],
     'opener_position': 'BTN',
     'board': ['7s', '6d', '3h'],
     'hero_cards': ['Ks', 'Qc'],
     'pot': 20.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'CO', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
     ],
     'label': 'PFA-7f'},
    {'hero_pos': 'BTN', 'villain_positions': ['CO', 'SB'],
     'opener_position': 'BTN',
     'board': ['Qs', '5h', '2c'],
     'hero_cards': ['Ac', 'Kd'],
     'pot': 20.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'CO', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
     ],
     'label': 'PFA-7g'},
    {'hero_pos': 'BTN', 'villain_positions': ['CO', 'SB'],
     'opener_position': 'BTN',
     'board': ['9c', '8s', '4h'],
     'hero_cards': ['Jh', 'Jd'],
     'pot': 20.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'CO', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
     ],
     'label': 'PFA-7h'},

    # ─────────────────────────────────────────────────────────────────
    # PFA-8 (Phase 6): Turn c-bet (delayed) (8 templates)
    # Hero checks flop, all check, hero faces turn decision.
    # Postflop action order: SB < BB < UTG/HJ < CO < BTN.
    # ─────────────────────────────────────────────────────────────────
    # PFA-8a: CO opener, BTN+BB callers, turn c-bet
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Ks', '7d', '2c', 'Qh'],
     'hero_cards': ['Ah', 'Kd'],
     'pot': 22.0, 'to_call': 0.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
     ],
     'label': 'PFA-8a'},
    # PFA-8b: CO opener with different board
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Jc', '6h', '2d', 'Tc'],
     'hero_cards': ['As', 'Js'],
     'pot': 24.0, 'to_call': 0.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
     ],
     'label': 'PFA-8b'},
    # PFA-8c: HJ opener, CO+BB callers
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['Qd', '5s', '3h', '8d'],
     'hero_cards': ['Kh', 'Kd'],
     'pot': 22.0, 'to_call': 0.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'HJ', 'check'), ('flop', 'CO', 'check'),
     ],
     'label': 'PFA-8c'},
    # PFA-8d: BTN opener, SB+BB callers
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['Ah', '5c', '2d', '9s'],
     'hero_cards': ['Kh', 'Qd'],
     'pot': 23.0, 'to_call': 0.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
     ],
     'label': 'PFA-8d'},
    # PFA-8e: CO opener
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['9h', '8c', '4d', 'Jh'],
     'hero_cards': ['Kd', 'Qs'],
     'pot': 22.0, 'to_call': 0.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
     ],
     'label': 'PFA-8e'},
    # PFA-8f: BTN opener, SB+BB callers
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['Td', '6s', '2c', 'Ks'],
     'hero_cards': ['Jh', 'Jd'],
     'pot': 24.0, 'to_call': 0.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
     ],
     'label': 'PFA-8f'},
    # PFA-8g: HJ opener
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['8d', '5s', '2h', 'As'],
     'hero_cards': ['Kc', 'Qh'],
     'pot': 22.0, 'to_call': 0.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'HJ', 'check'), ('flop', 'CO', 'check'),
     ],
     'label': 'PFA-8g'},
    # PFA-8h: CO opener
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Qh', '7c', '3s', '5d'],
     'hero_cards': ['Ah', '9h'],
     'pot': 23.0, 'to_call': 0.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
     ],
     'label': 'PFA-8h'},
]


def generate_scenarios(forbidden_fingerprints: Set[Tuple[str, str]]) -> List[dict]:
    """Generate PFA c-bet scenario records.

    All records have is_preflop_aggressor=1 (hero is the preflop opener).
    Turn c-bet scenarios (PFA-4) capped at 10 records.
    """
    records = []
    turn_cbet_count = 0
    # Phase 6 expansion v3.5: PFA-4 (5 existing) + PFA-8 (8 new) = 13 turn c-bets.
    # Cap raised from 10 → 15 to accommodate full PFA-8 group.
    max_turn_cbets = 15

    for tmpl in _PFA_TEMPLATES:
        label = tmpl['label']
        is_turn = tmpl['street'] == 'turn'

        if is_turn and turn_cbet_count >= max_turn_cbets:
            continue

        hero_cards = tmpl['hero_cards']
        board = tmpl['board']
        hero_cards_str = ''.join(hero_cards)
        board_str = ''.join(board)

        if (hero_cards_str, board_str) in forbidden_fingerprints or \
           ("".join(sorted([hero_cards_str[i:i+2] for i in range(0, len(hero_cards_str), 2)])),
            "".join(sorted([board_str[i:i+2] for i in range(0, len(board_str), 2)]))) \
                in forbidden_fingerprints:
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
            opener_position=tmpl['opener_position'],
        )

        sit_id = f"pfa_{label.lower().replace('-', '_')}"
        record = build_record_from_spec(spec, sit_id, 'pfa_scenarios')
        if record is None:
            continue

        # Verify IS_PFA is 1 (critical constraint)
        if record['feat_dict'].get('is_preflop_aggressor') != 1:
            print(f"[WARN] PFA scenario {sit_id} has IS_PFA != 1, skipping",
                  flush=True)
            continue

        records.append(record)
        if is_turn:
            turn_cbet_count += 1

        # Update forbidden set (in-place)
        from corpus_revision_scenarios._scenario_utils import fingerprint
        fp = fingerprint(hero_cards_str, board_str)
        forbidden_fingerprints.add(fp)

    # Phase 6 v3.5.1 silent-failure assertion: every PFA record must have IS_PFA=1.
    # Catches malformed templates that pass build_situation but mis-classify downstream.
    assert all(r['feat_dict'].get('is_preflop_aggressor') == 1 for r in records), \
        "PFA module produced records without is_preflop_aggressor=1"

    return records
