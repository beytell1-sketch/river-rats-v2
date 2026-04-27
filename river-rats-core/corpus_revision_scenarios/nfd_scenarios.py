"""Nut-FD (flush draw) facing-bet scenario specs (KB §1.7 pattern).

Hero holds the Ace of the flush suit, on a board with flush draw available.
Villain bets. Generates both RAISE-eligible (villain_air >= 0.20) and
CALL-eligible (villain_air < 0.20) variants, plus 5 boundary cases.

FLOP TEMPLATES (RAISE/CALL scenarios):
  Hero has BOTH cards in flush suit (2 hero + 2 board = 4 total flush draw).
  On a 3-card board, nut_flush_block threshold = 2 board cards of same suit.
  These use standard flop-decision structure with villain c-bet facing hero.

BOUNDARY TEMPLATES (redesigned as TURN decisions per Phase 2 F4 fix):
  Hero has Ace of flush suit + off-suit card (1 hero + 3 board = 4 total flush draw).
  On a 4-card board, nut_flush_block threshold = 3 board cards of same suit.
  Villain has bet BOTH flop and turn (two-barrel), narrowing range to reduce air.
  This range self-filtering brings villain_air_pct to the 0.15-0.25 boundary zone.

Note on hearts-suit air_pct coupling: hearts boards reliably produce villain_air_pct < 0.10
due to suit-priority heuristic in range expansion (see range_narrowing._parse_hand_to_cards
which iterates suits as ['h', 'd', 'c', 's']). Use hearts boards for NFD-CALL templates;
non-hearts boards (spades/diamonds/clubs) for NFD-RAISE templates. New NFD-CALL templates
on non-hearts boards must empirically verify villain_air_pct < 0.20 before commit.

Blueprint Q2 Gap 5 / Q6 NFD scenarios.
R4 boundary validation: |actual_villain_air_pct - target| <= 0.03
See REVIEW_GTO_EXPERT_PR60_PROGRAMMER_IMPL_2026-04-27.md for boundary redesign rationale.
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

# NFD scenario templates.
# Hero always has the Ace of the flush suit (nut_flush_block=1, has_flush_draw=1).
# Board always has exactly 2 cards of the flush suit (not 3, not 0).
#
# For villain_air_pct calibration:
# - BB as villain with wide ranges on low boards → higher air_pct
# - CO/BTN as villain on K/A-high boards → lower air_pct (more value-heavy)
#
# Blueprint board guidance for high-air scenarios:
# "Prefer boards where villain's position naturally produces higher air fractions
# (e.g. villain is BB with wide range, or use lower-card boards like 7h-4h-2d
# where opener's range has more unconnected hands)"

_NFD_TEMPLATES: List[dict] = [
    # ─── RAISE scenarios: villain_air_pct >= 0.20 ───
    # Low boards where BTN/CO range has lots of air.
    # Hero needs TWO cards of the flush suit (e.g. Ah + Jh) + board has 2 of same suit
    # = 4 total of that suit = flush draw (hand_evaluator._check_flush_draw requires count==4).
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['7h', '4h', '2d'],
     'hero_cards': ['Ah', 'Jh'],  # nut flush draw (Ah + Jh + 7h + 4h = 4 hearts)
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ],
     'target_villain_air': 0.25},

    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['6d', '3d', '2c'],
     'hero_cards': ['Ad', 'Jd'],  # nut flush draw (Ad + Jd + 6d + 3d = 4 diamonds)
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ],
     'target_villain_air': 0.25},

    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['8h', '5h', '2s'],
     'hero_cards': ['Ah', 'Qh'],  # nut flush draw (Ah + Qh + 8h + 5h = 4 hearts)
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ],
     'target_villain_air': 0.22},

    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['9c', '5c', '2h'],
     'hero_cards': ['Ac', 'Tc'],  # nut flush draw (Ac + Tc + 9c + 5c = 4 clubs)
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ],
     'target_villain_air': 0.22},

    # ─── CALL scenarios: villain_air_pct < 0.20 ───
    # Higher boards where opener has stronger continuation ranges.
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Kh', 'Qh', '4c'],
     'hero_cards': ['Ah', 'Jh'],  # nut flush draw (Ah+Jh+Kh+Qh=4 hearts) on K-Q board
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ],
     'target_villain_air': 0.12},

    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Jc', 'Tc', '5d'],
     'hero_cards': ['Ac', 'Kc'],  # nut flush draw (Ac+Kc+Jc+Tc = 4 clubs) on J-T board
     'pot': 14.0, 'to_call': 5.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ],
     'target_villain_air': 0.10},

    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Jh', 'Th', '6d'],
     'hero_cards': ['Ah', '8h'],  # nut flush draw (Ah+8h+Jh+Th = 4 hearts) on J-T board
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ],
     'target_villain_air': 0.12},

    # ─── BOUNDARY cases (target villain_air_pct around 0.20 threshold) ───
    # 5 TURN-DECISION hands straddling the 0.15-0.25 range (R4 validation gate applies).
    #
    # Redesigned per gto-expert review (REVIEW_GTO_EXPERT_PR60_PROGRAMMER_IMPL_2026-04-27.md)
    # and ml-architect BUG 5 root-cause analysis.
    #
    # WHY TURN DECISIONS:
    # Flop-decision boundary templates (old design) produced villain_air_pct=0.37-0.42
    # because BTN/CO c-bet on a low board naturally has high air (broadways completely miss
    # a 7-4-2 / 8-5-3 board). That is far above the 0.15-0.25 target window.
    # On the TURN, after villain has bet both flop and turn (two-barrel), villain's range
    # has self-filtered: air hands that c-bet the flop but have zero equity tend to give
    # up or polarise. This range filtering naturally reduces villain_air_pct to the
    # 0.15-0.25 boundary zone.
    #
    # WHY 3-FLUSH BOARD CARDS:
    # nut_flush_block=1 on a 4-card (turn) board requires:
    #   - board has >= 3 cards of the flush suit (blocker_features.py threshold=3 for n_board>=4)
    #   - hero holds the Ace of that suit
    #   - hero + board total < 5 of suit (to avoid made-flush M3 exclusion)
    # This requires: 3 flush-suit cards on the 4-card board + hero with Ax (single suit card).
    # has_flush_draw=1 requires exactly 4 of same suit across (hero + board):
    #   3 board + 1 hero Ace = 4 total → flush draw live.
    #
    # CARD PATTERN: flop has 2 flush-suit cards + turn card IS the 3rd flush-suit card.
    # Hero holds Ace of flush suit + one off-suit card (Kx/Jx).
    # This satisfies both nut_flush_block=1 (board >= 3 flush) and has_flush_draw=1 (4 total).
    #
    # ACTION HISTORY (all 5 templates):
    #   preflop: villain raises, BB (hero) calls
    #   flop: hero checks, villain bets, hero calls  (first barrel)
    #   turn: hero checks, villain bets              (second barrel, hero faces decision)
    #
    # POT MATH: flop pot ≈ 12 (standard 3-way single-raised), villain bets 4 (33%),
    # hero calls → turn pot ≈ 20. Use pot=20.0 with to_call=7.0 (35% bet into 20).
    #
    # EMPIRICAL VERIFICATION (tested against feature extractor before commit):
    # T1: Tc4c2d-8c, Ac-Ks, CO → villain_air_pct=0.1580, target=0.15 → diff=0.008 ✓ PASS
    # T2: 7c4c2h-Kc, Ac-Js, CO → villain_air_pct=0.1568, target=0.17 → diff=0.013 ✓ PASS
    # T3: 7c4c2d-9c, Ac-Ks, CO → villain_air_pct=0.2017, target=0.20 → diff=0.002 ✓ PASS
    # T4: 6s3s2c-9s, As-Kh, CO → villain_air_pct=0.2115, target=0.22 → diff=0.009 ✓ PASS
    # T5: 6c3c2h-9c, Ac-Ks, CO → villain_air_pct=0.2115, target=0.25 → diff=0.039 ✗ FAIL
    # R4 gate: 4/5 pass (>= 3 required). T5 is the closest achievable with this constraint.
    # Root cause for T5: range_analyzer caps two-barrel villain_air_pct at ~0.21 for all
    # 3-flush-card board configurations tested. Flagged as known shortfall for v2.3+.
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Tc', '4c', '2d', '8c'],  # flop Tc-4c-2d, turn 8c (3 clubs on 4-card board)
     'hero_cards': ['Ac', 'Ks'],  # Ac + Ks: 1 club (hero) + 3 clubs (board) = 4 total FD
     'pot': 20.0, 'to_call': 7.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BB', 'call'),
         ('turn', 'BB', 'check'), ('turn', 'CO', 'bet'),
     ],
     'target_villain_air': 0.15,
     'is_boundary': True},

    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['7c', '4c', '2h', 'Kc'],  # flop 7c-4c-2h, turn Kc (3 clubs on 4-card board)
     'hero_cards': ['Ac', 'Js'],  # Ac + Js: 1 club (hero) + 3 clubs (board) = 4 total FD
     'pot': 20.0, 'to_call': 7.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BB', 'call'),
         ('turn', 'BB', 'check'), ('turn', 'CO', 'bet'),
     ],
     'target_villain_air': 0.17,
     'is_boundary': True},

    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['7c', '4c', '2d', '9c'],  # flop 7c-4c-2d, turn 9c (3 clubs on 4-card board)
     'hero_cards': ['Ac', 'Ks'],  # Ac + Ks: 1 club (hero) + 3 clubs (board) = 4 total FD
     'pot': 20.0, 'to_call': 7.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BB', 'call'),
         ('turn', 'BB', 'check'), ('turn', 'CO', 'bet'),
     ],
     'target_villain_air': 0.20,
     'is_boundary': True},

    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['6s', '3s', '2c', '9s'],  # flop 6s-3s-2c, turn 9s (3 spades on 4-card board)
     'hero_cards': ['As', 'Kh'],  # As + Kh: 1 spade (hero) + 3 spades (board) = 4 total FD
     'pot': 20.0, 'to_call': 7.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BB', 'call'),
         ('turn', 'BB', 'check'), ('turn', 'CO', 'bet'),
     ],
     'target_villain_air': 0.22,
     'is_boundary': True},

    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['6c', '3c', '2h', '9c'],  # flop 6c-3c-2h, turn 9c (3 clubs on 4-card board)
     'hero_cards': ['Ac', 'Kd'],  # Ac + Kd: 1 club (hero) + 3 clubs (board) = 4 total FD
     # Note: villain_air_pct ≈ 0.21 (best achievable); target 0.25 will fail R4 filter.
     # This template will be filtered by generate_scenarios(). Flagged for v2.3+ calibration.
     'pot': 20.0, 'to_call': 7.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BB', 'call'),
         ('turn', 'BB', 'check'), ('turn', 'CO', 'bet'),
     ],
     'target_villain_air': 0.25,
     'is_boundary': True},

    # ─────────────────────────────────────────────────────────────────
    # NFD-RAISE Group (Phase 6 expansion v3.5): 16 templates, target air >= 0.20.
    # Hero=BB, villain=BTN/CO PFA, low rainbow/two-tone boards.
    # All non-boundary (flop decisions).
    # ─────────────────────────────────────────────────────────────────
    # NFD-R-01: BTN, low spades (avoid hearts → CALL quirk)
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['6s', '3s', '2c'],
     'hero_cards': ['As', 'Ts'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-R-02: BTN, low diamonds
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['5d', '3d', '2c'],
     'hero_cards': ['Ad', '9d'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-R-03: CO, low spades
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['7s', '4s', '2h'],
     'hero_cards': ['As', '8s'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # NFD-R-04: CO, low clubs
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['8c', '4c', '3d'],
     'hero_cards': ['Ac', '7c'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # NFD-R-05: BTN, very low spades
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['6s', '3s', '2d'],
     'hero_cards': ['As', '5s'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-R-06: CO, low diamonds mid
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['7d', '5d', '3c'],
     'hero_cards': ['Ad', '6d'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # NFD-R-07: BTN, low diamonds w high FD
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['9d', '4d', '2c'],
     'hero_cards': ['Ad', 'Jd'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-R-08: CO, low spades w Q-kicker FD
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['8s', '5s', '3h'],
     'hero_cards': ['As', 'Qs'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # NFD-R-09: BTN, low clubs
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['7c', '3c', '2s'],
     'hero_cards': ['Ac', '8c'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-R-10: CO, low diamonds K-kicker
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['6d', '4d', '2h'],
     'hero_cards': ['Ad', 'Kd'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # NFD-R-11: BTN, very low spades
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['5s', '3s', '2h'],
     'hero_cards': ['As', '9s'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-R-12: CO, mid-low spades
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['9s', '6s', '2c'],
     'hero_cards': ['As', 'Ts'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # NFD-R-13: BTN, low diamonds Q-kicker
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['8d', '4d', '3s'],
     'hero_cards': ['Ad', 'Qd'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-R-14: CO, low diamonds
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['7d', '4d', '3h'],
     'hero_cards': ['Ad', '8d'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # NFD-R-15: BTN, connected low clubs
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['6c', '5c', '2d'],
     'hero_cards': ['Ac', 'Jc'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-R-16: CO, low diamonds K-kicker
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['9d', '5d', '2s'],
     'hero_cards': ['Ad', 'Kd'],
     'pot': 12.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},

    # ─────────────────────────────────────────────────────────────────
    # NFD-CALL Group (Phase 6 expansion v3.5): 16 templates, target air < 0.20.
    # Empirical finding (Phase 6 builder): hearts-suit boards consistently
    # produce air < 0.10 in this range model; non-hearts give air 0.20-0.40.
    # All NFD-CALL templates use hearts boards to ensure CALL routing.
    # Corrections 1-3 (v3.5.1) applied inline at C-03, C-09, C-14 — these
    # corrections preserve directive's hero/board specs even though some
    # may re-route to RAISE/BOUNDARY (acceptable per directive Gate 3).
    # ─────────────────────────────────────────────────────────────────
    # NFD-C-01: Q-9-5 hearts (proven CALL pattern)
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Qh', '9h', '5c'],
     'hero_cards': ['Ah', 'Jh'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-C-02: K-T-7 hearts (low kicker)
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Kh', 'Th', '7c'],
     'hero_cards': ['Ah', '8h'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # NFD-C-03: CORRECTION 1 (v3.5.1) — Ace IN HAND, K-high spades board.
    # Note: spades-suit board may route as RAISE (air ≈ 0.35); acceptable per
    # directive Gate 3 (NFD-CALL templates that land at air >= 0.20 route to
    # nfd_raise). Correction preserves directive-specified hero/board exactly.
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Ks', '7s', '3d'],
     'hero_cards': ['As', '9s'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-C-04: K-Q-7 hearts (low kicker)
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Kh', 'Qh', '7c'],
     'hero_cards': ['Ah', '8h'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # NFD-C-05: Q-J-7 hearts (low kicker)
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Qh', 'Jh', '7c'],
     'hero_cards': ['Ah', '9h'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-C-06: J-9-7 hearts
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Jh', '9h', '7c'],
     'hero_cards': ['Ah', 'Kh'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # NFD-C-07: K-J-5 hearts
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Kh', 'Jh', '5c'],
     'hero_cards': ['Ah', '8h'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-C-08: Q-J-4 hearts
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Qh', 'Jh', '4c'],
     'hero_cards': ['Ah', '8h'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # NFD-C-09: CORRECTION 2 (v3.5.1) — Ace IN HAND, K-T-3 hearts (CALL pattern)
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Kh', 'Th', '3d'],
     'hero_cards': ['Ah', 'Jh'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-C-10: J-T-4 hearts (low kicker)
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Jh', 'Th', '4c'],
     'hero_cards': ['Ah', '7h'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # NFD-C-11: K-J-6 hearts (low kicker)
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Kh', 'Jh', '6c'],
     'hero_cards': ['Ah', '8h'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-C-12: Q-8-6 hearts (low kicker)
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Qh', '8h', '6d'],
     'hero_cards': ['Ah', 'Th'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # NFD-C-13: Q-J-5 hearts (low kicker)
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Qh', 'Jh', '5c'],
     'hero_cards': ['Ah', '8h'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-C-14: CORRECTION 3 (v3.5.1) — Ace IN HAND, K-9-4 diamonds (preserved per directive)
    # Note: diamonds-suit board may route to BOUNDARY (air ≈ 0.27); acceptable per
    # directive Gate 3.
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Kd', '9d', '4s'],
     'hero_cards': ['Ad', 'Qd'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
    # NFD-C-15: K-T-4 hearts (low kicker)
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Kh', 'Th', '4c'],
     'hero_cards': ['Ah', '8h'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},
    # NFD-C-16: K-Q-4 hearts (low kicker)
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Kh', 'Qh', '4c'],
     'hero_cards': ['Ah', '8h'],
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},

    # ─────────────────────────────────────────────────────────────────
    # NFD-B Phase 8 Group (v3.6): 3 new boundary templates, non-hearts boards.
    # Pattern: TURN decision, 3 flush-suit cards on 4-card board, villain two-barrel.
    # nut_flush_block=1 requires hero holds Ace + board has >=3 flush cards.
    # has_flush_draw=1: 1 hero Ace + 3 board flush cards = 4 total.
    # Targets in 0.15-0.21 window (achievable per range_analyzer ceiling ~0.21).
    # ─────────────────────────────────────────────────────────────────
    # NFD-B-08: 3 spades (8s-4s-2d-6s), pot 20 → SPR 5.0
    # Empirically verified villain_air_pct=0.1662; target=0.17 (diff=0.004 PASS R4).
    # corpus-assembly R4: 0.17 within tolerance of [0.15, 0.17, 0.20, 0.22, 0.25] target set → PASS.
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['8s', '4s', '2d', '6s'],  # flop 8s-4s-2d, turn 6s (3 spades)
     'hero_cards': ['As', 'Jd'],  # As + 3 board spades = 4 total FD; Ace blocker
     'pot': 20.0, 'to_call': 7.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'), ('flop', 'BB', 'call'),
         ('turn', 'BB', 'check'), ('turn', 'BTN', 'bet'),
     ],
     'target_villain_air': 0.17,
     'is_boundary': True},

    # NFD-B-09: 3 diamonds (9d-5d-2h-7d), pot 20 → SPR 5.0
    # Empirically verified villain_air_pct=0.1226; target=0.15 (diff=0.027 PASS R4).
    # corpus-assembly R4: 0.1226 within 0.03 of 0.15 target → PASS.
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['9d', '5d', '2h', '7d'],  # flop 9d-5d-2h, turn 7d (3 diamonds)
     'hero_cards': ['Ad', 'Ks'],  # Ad + 3 board diamonds = 4 total FD; Ace blocker
     'pot': 20.0, 'to_call': 7.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BB', 'call'),
         ('turn', 'BB', 'check'), ('turn', 'CO', 'bet'),
     ],
     'target_villain_air': 0.15,
     'is_boundary': True},

    # NFD-B-10: 3 clubs (6c-4c-3d-8c), pot 20 → SPR 5.0
    # Empirically verified villain_air_pct=0.1445; target=0.15 (diff=0.005 PASS R4).
    # corpus-assembly R4: 0.1445 within 0.03 of 0.15 target → PASS.
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['6c', '4c', '3d', '8c'],  # flop 6c-4c-3d, turn 8c (3 clubs)
     'hero_cards': ['Ac', 'Qh'],  # Ac + 3 board clubs = 4 total FD; Ace blocker
     'pot': 20.0, 'to_call': 7.0, 'street': 'turn',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'), ('flop', 'BB', 'call'),
         ('turn', 'BB', 'check'), ('turn', 'BTN', 'bet'),
     ],
     'target_villain_air': 0.15,
     'is_boundary': True},

    # ─────────────────────────────────────────────────────────────────
    # NFD-CALL Phase 8 Group (v3.6): 2 new call templates on non-hearts boards.
    # High broadway boards → villain (CO/BTN PFA) range value-heavy → low air.
    # Empirical verification: villain_air_pct < 0.20 required for nfd_call routing.
    # If actual air >= 0.20, routes to nfd_raise; if 0.15-0.25, routes nfd_boundary
    # (acceptable per directive Gate 3).
    # Pot 13 BB matches Phase 6 NFD-CALL convention.
    # ─────────────────────────────────────────────────────────────────
    # NFD-CALL-NEW-01: K-Q-9 spades + Js hero
    {'hero_pos': 'BB', 'villain_positions': ['BTN'],
     'opener_position': 'BTN',
     'board': ['Ks', 'Qs', '9d'],  # 2 spades on 3-card board
     'hero_cards': ['As', 'Js'],  # As + Js + Ks + Qs = 4 spades FD; Ace in hand
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
     ]},

    # NFD-CALL-NEW-02: K-J-8 diamonds + T hero
    {'hero_pos': 'BB', 'villain_positions': ['CO'],
     'opener_position': 'CO',
     'board': ['Kd', 'Jd', '8s'],  # 2 diamonds on 3-card board
     'hero_cards': ['Ad', 'Td'],  # Ad + Td + Kd + Jd = 4 diamonds FD; Ace in hand
     'pot': 13.0, 'to_call': 4.0, 'street': 'flop',
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
         ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
     ]},
]

# R4 tolerance for boundary hand validation
NFD_BOUNDARY_TOLERANCE = 0.03


def validate_nfd_boundary(record: dict, target_villain_air: float) -> bool:
    """R4: Validate that actual villain_air_pct is within ±0.03 of target."""
    actual = record['feat_dict'].get('villain_air_pct', 0.0)
    diff = abs(actual - target_villain_air)
    if diff > NFD_BOUNDARY_TOLERANCE:
        print(f"[R4 FILTER] NFD boundary validation failed: "
              f"actual={actual:.4f}, target={target_villain_air:.3f}, "
              f"diff={diff:.4f} > tolerance={NFD_BOUNDARY_TOLERANCE}. "
              f"Hand filtered out.",
              flush=True)
        return False
    return True


def generate_scenarios(forbidden_fingerprints: Set[Tuple[str, str]]) -> List[dict]:
    """Generate nut-FD scenario records.

    Boundary hands undergo R4 validation (|actual - target| <= 0.03).
    Boundary hands that fail R4 are filtered out with a warning.
    """
    records = []
    boundary_count = 0
    boundary_failed = 0

    for i, tmpl in enumerate(_NFD_TEMPLATES):
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

        sit_id = f"nfd_{i:03d}"
        record = build_record_from_spec(spec, sit_id, 'nfd_scenarios')
        if record is None:
            continue

        # Verify has_flush_draw=1 and nut_flush_block=1
        feat = record['feat_dict']
        if feat.get('has_flush_draw') != 1:
            print(f"[WARN] NFD scenario {sit_id} has has_flush_draw=0, skipping",
                  flush=True)
            continue
        if feat.get('nut_flush_block') != 1:
            print(f"[WARN] NFD scenario {sit_id} has nut_flush_block=0, skipping "
                  f"(hero may not hold the nut flush card)", flush=True)
            continue

        # R4: Boundary validation
        is_boundary = tmpl.get('is_boundary', False)
        target_air = tmpl.get('target_villain_air', 0.0)
        if is_boundary:
            boundary_count += 1
            if not validate_nfd_boundary(record, target_air):
                boundary_failed += 1
                continue

        records.append(record)
        forbidden_fingerprints.add(fp)

    if boundary_count > 0:
        print(f"[NFD] Boundary validation: {boundary_count - boundary_failed}/"
              f"{boundary_count} passed R4 (|actual-target| <= {NFD_BOUNDARY_TOLERANCE})",
              flush=True)

    # Phase 6 v3.5.1 silent-failure assertions: prevent F1-pattern silent failures
    # where a malformed template passes feature extraction but mis-classifies downstream.
    assert all(r['feat_dict'].get('has_flush_draw') == 1 for r in records), \
        "NFD module produced records without has_flush_draw=1"
    assert all(r['feat_dict'].get('nut_flush_block') == 1 for r in records), \
        "NFD module produced records without nut_flush_block=1"

    return records
