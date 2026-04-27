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

    return records
