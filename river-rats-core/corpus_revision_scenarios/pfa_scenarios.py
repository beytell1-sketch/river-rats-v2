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

    # ─────────────────────────────────────────────────────────────────
    # SPR-MED Group (Phase 8 v3.6): 8 templates routing to spr_med category.
    # Pot 28-45 BB → SPR 2.22-3.57 (in spr_med band 2.0 <= SPR < 4.0).
    # Hero CO or BTN (NOT SB), flop decisions, villain_aggression_count=0.
    # Category set: {pfa, spr_med}; spr_med scarcity (0.83) > pfa (0.58) → routes spr_med.
    # ─────────────────────────────────────────────────────────────────
    # SPR-MED-01: CO opener, BTN+BB callers, pot 30 → SPR 3.333
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Kh', '8s', '3d'],
     'hero_cards': ['Ac', 'Jc'],
     'pot': 30.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'SPR-MED-01'},
    # SPR-MED-02: BTN opener, SB+BB callers, pot 28 → SPR 3.571
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['Qd', '7c', '4h'],
     'hero_cards': ['Kh', 'Kd'],  # overpair
     'pot': 28.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'SPR-MED-02'},
    # SPR-MED-03: CO opener, pot 32 → SPR 3.125
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Jc', '5s', '2d'],
     'hero_cards': ['Qd', 'Qh'],  # overpair
     'pot': 32.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'SPR-MED-03'},
    # SPR-MED-04: BTN opener, SB+BB callers, pot 35 → SPR 2.857
    # NIT-1 fix (round 8): blueprint had typo extra apostrophe in villain_positions key.
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['As', '6c', '3h'],
     'hero_cards': ['Th', 'Td'],  # underpair
     'pot': 35.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'SPR-MED-04'},
    # SPR-MED-05: CO opener, pot 38 → SPR 2.632
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Td', '4s', '2c'],
     'hero_cards': ['Ah', 'Qs'],  # overcards
     'pot': 38.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'SPR-MED-05'},
    # SPR-MED-06: BTN opener, SB+BB callers, pot 40 → SPR 2.500
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['8c', '6d', '3s'],
     'hero_cards': ['Jh', 'Jd'],  # overpair
     'pot': 40.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'SPR-MED-06'},
    # SPR-MED-07: CO opener, pot 43 → SPR 2.326
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['9h', '4d', '2s'],
     'hero_cards': ['Kc', 'Kh'],  # overpair
     'pot': 43.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'SPR-MED-07'},
    # SPR-MED-08: BTN opener, SB+BB callers, pot 45 → SPR 2.222
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['7d', '5h', '3c'],
     'hero_cards': ['Ad', 'Kc'],  # overcards
     'pot': 45.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'SPR-MED-08'},

    # ─────────────────────────────────────────────────────────────────
    # SPR-MED v3.6.1 supplement (Phase 8): 3 ADDITIONAL spr_med templates.
    # Per ml-architect round 8 CHANGES_REQUESTED material accounting fix:
    # 3 MAGG-A pot=50 records were filling spr_med pre-adjustment; raising
    # their pot REMOVES them from spr_med pool (costs 3 fills, doesn't free
    # 3 slots). Net spr_med gain = 32 - 3 + 8 = 37; need 3 more for 40.
    # Pattern matches SPR-MED-01..08; novel boards.
    # ─────────────────────────────────────────────────────────────────
    # SPR-MED-09: CO opener, pot 36 → SPR 2.778
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Jh', '7s', '3c'],
     'hero_cards': ['Ac', 'Kd'],  # overcards
     'pot': 36.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'SPR-MED-09'},
    # SPR-MED-10: BTN opener, SB+BB callers, pot 39 → SPR 2.564
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['9d', '7c', '2h'],
     'hero_cards': ['Ah', 'Ad'],  # overpair (AA)
     'pot': 39.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'SPR-MED-10'},
    # SPR-MED-11: CO opener, pot 42 → SPR 2.381
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Th', '6d', '4s'],
     'hero_cards': ['Ks', 'Qc'],  # overcards
     'pot': 42.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'SPR-MED-11'},

    # ─────────────────────────────────────────────────────────────────
    # PFA-9 Group (Phase 8 v3.6): 18 pure-pfa templates routing to pfa.
    # Pot 14-20 BB → SPR 5.0-7.14 (spr_std band).
    # Flop decisions, villain_aggression_count=0 (no magg eligibility).
    # Category set: {pfa, spr_std}; pfa scarcity (0.58) > spr_std (~0.39) → routes pfa.
    # ─────────────────────────────────────────────────────────────────
    # PFA-9a: HJ opener, BTN+BB callers, pot 14 → SPR 7.14
    {'hero_pos': 'HJ', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'HJ',
     'board': ['Ad', '5c', '3h'],
     'hero_cards': ['Kh', 'Ks'],  # overpair
     'pot': 14.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9a'},
    # PFA-9b: BTN opener, SB+BB callers, pot 15 → SPR 6.67
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['Kc', '6h', '2s'],
     'hero_cards': ['Qs', 'Qd'],  # overpair
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9b'},
    # PFA-9c: CO opener, BTN+BB callers, pot 16 → SPR 6.25
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Th', '8d', '4c'],
     'hero_cards': ['Jc', 'Js'],  # overpair
     'pot': 16.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9c'},
    # PFA-9d: HJ opener, CO+BB callers, pot 15 → SPR 6.67
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['7h', '6c', '2d'],
     'hero_cards': ['As', 'Ah'],  # overpair (AA)
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9d'},
    # PFA-9e: BTN opener, CO+SB callers, BB folds, pot 20 → SPR 5.0 (PFA-7 convention)
    {'hero_pos': 'BTN', 'villain_positions': ['CO', 'SB'],
     'opener_position': 'BTN',
     'board': ['Qc', '4d', '2h'],
     'hero_cards': ['Kd', 'Jh'],  # overcards
     'pot': 20.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'CO', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
     ],
     'label': 'PFA-9e'},
    # PFA-9f: CO opener, pot 14 → SPR 7.14
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['8s', '7d', '3c'],
     'hero_cards': ['Ac', 'Kh'],  # overcards
     'pot': 14.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9f'},
    # PFA-9g: HJ opener, CO+BB callers, pot 15 → SPR 6.67
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['6d', '4s', '2c'],
     'hero_cards': ['Qs', 'Jh'],  # overcards
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9g'},
    # PFA-9h: BTN opener, SB+BB callers, pot 16 → SPR 6.25
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['Ah', '9d', '5s'],
     'hero_cards': ['Kc', 'Qh'],  # overcards
     'pot': 16.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9h'},
    # PFA-9i: CO opener, pot 15 → SPR 6.67
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Jh', '4d', '2c'],
     'hero_cards': ['Th', 'Tc'],  # underpair
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9i'},
    # PFA-9j: HJ opener, BTN+BB callers, pot 14 → SPR 7.14
    {'hero_pos': 'HJ', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'HJ',
     'board': ['Kd', '5h', '3c'],
     'hero_cards': ['Ah', 'Jd'],  # overcards
     'pot': 14.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9j'},
    # PFA-9k: BTN opener, CO+SB callers, BB folds, pot 20 → SPR 5.0 (PFA-7 convention)
    {'hero_pos': 'BTN', 'villain_positions': ['CO', 'SB'],
     'opener_position': 'BTN',
     'board': ['5s', '3d', '2h'],
     'hero_cards': ['Kh', 'Ks'],  # overpair
     'pot': 20.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'CO', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
     ],
     'label': 'PFA-9k'},
    # PFA-9l: CO opener, pot 16 → SPR 6.25
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['Qh', '3s', '2d'],
     'hero_cards': ['Ac', 'Ks'],  # overcards
     'pot': 16.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9l'},
    # PFA-9m: HJ opener, CO+BB callers, pot 15 → SPR 6.67
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['Tc', '9d', '4h'],
     'hero_cards': ['Ks', 'Kd'],  # overpair
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9m'},
    # PFA-9n: BTN opener, SB+BB callers, pot 15 → SPR 6.67
    {'hero_pos': 'BTN', 'villain_positions': ['SB', 'BB'],
     'opener_position': 'BTN',
     'board': ['7c', '5d', '2h'],
     'hero_cards': ['Jh', 'Jd'],  # overpair
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9n'},
    # PFA-9o: CO opener, pot 14 → SPR 7.14
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['9s', '7h', '4d'],
     'hero_cards': ['Ah', 'Qd'],  # overcards
     'pot': 14.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9o'},
    # PFA-9p: HJ opener, CO+BB callers, pot 14 → SPR 7.14
    {'hero_pos': 'HJ', 'villain_positions': ['CO', 'BB'],
     'opener_position': 'HJ',
     'board': ['4h', '3c', '2d'],
     'hero_cards': ['Kd', 'Qh'],  # overcards
     'pot': 14.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9p'},
    # PFA-9q: BTN opener, CO+SB callers, BB folds, pot 20 → SPR 5.0 (PFA-7 convention)
    {'hero_pos': 'BTN', 'villain_positions': ['CO', 'SB'],
     'opener_position': 'BTN',
     'board': ['Jd', '8c', '3h'],
     'hero_cards': ['Ah', 'Ac'],  # overpair (AA)
     'pot': 20.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'CO', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
     ],
     'label': 'PFA-9q'},
    # PFA-9r: CO opener, pot 15 → SPR 6.67
    {'hero_pos': 'CO', 'villain_positions': ['BTN', 'BB'],
     'opener_position': 'CO',
     'board': ['6c', '5h', '2s'],
     'hero_cards': ['Kd', 'Qs'],  # overcards
     'pot': 15.0, 'to_call': 0.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
     ],
     'label': 'PFA-9r'},
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
