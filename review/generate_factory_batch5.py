"""
Generate all ~185 Phase 2B situations (BP1-BP7) through SituationFactory,
validate each, and write results to:
  training-data/factory_batch5_situations.jsonl

Source documents consumed:
  review/comms/PHASE2A_SITUATION_ALLOCATION_2026-04-13.md  (allocation spec)
  review/BOARD_ALLOCATION_V4_BET.md                        (board texture reference)
  review/generate_factory_batch3.py                        (format reference)

DO NOT RUN until reviewed. See review/comms/ for delivery note.

Run from any directory:
    python3 /home/rupertbeytell/river-rats-v2/review/generate_factory_batch5.py

Situation IDs: BP1_01 ... BP7_18 (unique per batch pattern).

Sizing conventions (solver-aligned):
  Flop bets:  25% pot = 0.25 * pot, 66% pot = 0.66 * pot
  Turn bets:  33% pot = 0.33 * pot, 75% pot = 0.75 * pot
  River bets: 33% pot = 0.33 * pot, 75% pot = 0.75 * pot

Standard 3-way pot: preflop raise 3bb, 2 callers => pot=90, eff_stack=450, SPR=5.0
"""

import sys
import os
import json

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_CORE = os.path.join(_REPO, 'river-rats-core')
sys.path.insert(0, _CORE)
os.chdir(_CORE)

from situation_factory import SituationSpec, build_situation, validate_situation, normalise_situation

OUTPUT_PATH = os.path.join(_REPO, 'training-data', 'factory_batch5_situations.jsonl')

# =============================================================================
# BOARD BASES
#
# Standard 3-way structure unless noted:
#   pot=90, eff_stack=450, SPR=5.0
#   preflop: raiser raises, 2 callers
#
# Facing-bet boards: to_call > 0, last villain in villain_positions is bettor.
# Not-facing-bet boards: to_call=0, hero acts without a bet to face.
#
# Flop facing-bet sizing: 30 = 33% of 90 (approx 25% of 120 total)
#   25% of 90 = 22.5 => use 23 (rounded) OR use exact 30 = 33%
#   For simplicity: flop_bet_small=23 (25%), flop_bet_large=59 (66%)
#   Turn/river pots depend on flop action.
#
# Exact solver-aligned amounts used throughout:
#   Flop 25% bet on 90-pot: 23 chips  (to_call=23, pot post-bet=113)
#   Flop 66% bet on 90-pot: 59 chips  (to_call=59, pot post-bet=149)
#   Flop 33% bet on 90-pot: 30 chips  (to_call=30, pot post-bet=120)
#     [batch3 used 30; we keep 30 for consistency on facing_bet flop boards]
# =============================================================================

# ---------------------------------------------------------------------------
# FACING-BET FLOP BOARDS (BP1, BP2, BP3 flop situations)
# 3-way, pot=90, standard eff_stack=450
# ---------------------------------------------------------------------------

# FB5_01: Two-tone spades, T-high flop. Hero BTN, villains SB+BB, BB bets 30 (33% pot).
FB5_01 = dict(
    board_cards=['Ts', '6s', '3d'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# FB5_02: Two-tone hearts, Q-high flop. Hero BB, villains HJ+BTN, BTN bets 30.
FB5_02 = dict(
    board_cards=['Qh', '8h', '4d'],
    hero_pos='BB',
    villain_positions=['HJ', 'BTN'],
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'HJ', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'HJ', 'check'), ('flop', 'BTN', 'bet'),
    ],
    opener_position='HJ',
    effective_stack=450.0,
)

# FB5_03: Two-tone clubs, J-high flop. Hero CO, villains SB+BB, BB bets 30 (donk).
FB5_03 = dict(
    board_cards=['Jc', '7c', '2d'],
    hero_pos='CO',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# FB5_04: Rainbow, K-high flop. Hero BTN, villains SB+BB, BB bets 30.
FB5_04 = dict(
    board_cards=['Kh', '9d', '3c'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# FB5_05: Two-tone diamonds, A-high flop. Hero SB, villains CO+BTN, BTN bets 30.
FB5_05 = dict(
    board_cards=['Ad', '5d', '2c'],
    hero_pos='SB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# FB5_06: Two-tone spades, K-high flop. Hero BB, villains CO+BTN, BTN bets 30.
FB5_06 = dict(
    board_cards=['Ks', '8s', '4h'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# FB5_07: Two-tone hearts, 9-high flop. Hero BTN, villains SB+BB, BB bets 30.
FB5_07 = dict(
    board_cards=['9h', '6h', '2c'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# FB5_08: Two-tone clubs, Q-high flop. Hero SB, villains HJ+BTN, BTN bets 30.
FB5_08 = dict(
    board_cards=['Qc', '9c', '5h'],
    hero_pos='SB',
    villain_positions=['HJ', 'BTN'],
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'HJ', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'HJ', 'check'), ('flop', 'BTN', 'bet'),
    ],
    opener_position='HJ',
    effective_stack=450.0,
)

# FB5_09: Rainbow, J-high flop. Hero CO, villains SB+BB, BB bets 30.
FB5_09 = dict(
    board_cards=['Jd', '8c', '3s'],
    hero_pos='CO',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# FB5_10: Two-tone spades, T-high connected flop. Hero BB, villains CO+BTN, BTN bets 30.
# Note: postflop order is BB(1)→CO(4)→BTN(5), so BTN is last to act and is the bettor.
FB5_10 = dict(
    board_cards=['Th', '8s', '6s'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# ---------------------------------------------------------------------------
# FACING-BET TURN BOARDS (BP1 strong two pair, BP2, BP3 turn situations)
# Pot after flop bet + calls: standard = 90 + 30*3 = 180. Turn bet 33% = 59.
# Or flop all-check then turn bet: pot stays 90, turn bet 30 (33%) or 68 (75%).
# ---------------------------------------------------------------------------

# TB5_01: Two-tone hearts, K-high turn. Flop action: all check. Turn: BB bets 30.
# pot=90 (no flop bet), hero CO, villains SB+BB, BB bets 30 on turn.
TB5_01 = dict(
    board_cards=['Kd', '7h', '3c', 'Th'],
    hero_pos='CO',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=30.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'CO', 'check'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# TB5_02: Two-tone spades, Q-high turn. Flop bet+calls => pot=180. Turn bet 59 (33% of 180).
TB5_02 = dict(
    board_cards=['Qs', '7d', '2c', 'Js'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=180.0,
    to_call=59.0,
    street='turn',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'bet'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# TB5_03: Rainbow, A-high turn. Flop all-check. Turn: BTN bets 30 (33% of 90).
TB5_03 = dict(
    board_cards=['Ah', '6c', '2s', '9d'],
    hero_pos='SB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=30.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'SB', 'check'), ('turn', 'CO', 'check'), ('turn', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# TB5_04: Two-tone clubs, J-high turn. Flop bet+calls => pot=180. Turn bet 59 (33%).
TB5_04 = dict(
    board_cards=['Jc', '8d', '3c', 'Ks'],
    hero_pos='BB',
    villain_positions=['HJ', 'BTN'],
    pot=180.0,
    to_call=59.0,
    street='turn',
    action_history=[
        ('preflop', 'HJ', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'HJ', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'), ('turn', 'HJ', 'bet'),
    ],
    opener_position='HJ',
    effective_stack=450.0,
)

# TB5_05: Two-tone diamonds, 9-high turn. Flop all-check. Turn CO bets 30.
TB5_05 = dict(
    board_cards=['9d', '5s', '2d', '7c'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=30.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'BB', 'check'), ('turn', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# ---------------------------------------------------------------------------
# FACING-BET RIVER BOARDS (BP2, BP3 river situations)
# After 2 streets of betting: pot ~360. River bet 33% = 119, or 75% = 270.
# Or: flop bet, turn check, river bet. Pot ~180 after flop action.
# ---------------------------------------------------------------------------

# RB5_01: Rainbow river. Flop bet+2calls => pot=180. Turn check. River BB bets 59 (33% of 180).
RB5_01 = dict(
    board_cards=['Kh', '7d', '2s', '9c', '4h'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=180.0,
    to_call=59.0,
    street='river',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'check'), ('turn', 'BTN', 'check'),
        ('river', 'SB', 'check'), ('river', 'BB', 'bet'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# RB5_02: Two-tone spades river. Flop bet+calls, turn bet+calls => pot=360. River BB bets 119 (33%).
RB5_02 = dict(
    board_cards=['Qs', '8d', '3s', 'Tc', '5h'],
    hero_pos='CO',
    villain_positions=['SB', 'BB'],
    pot=360.0,
    to_call=119.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'), ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'), ('turn', 'SB', 'call'),
        ('river', 'SB', 'check'), ('river', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# RB5_03: Rainbow river. Flop all-check. Turn bet+calls => pot=180. River BTN bets 59 (33%).
RB5_03 = dict(
    board_cards=['Jh', '6d', '2c', '8s', 'Kd'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=180.0,
    to_call=59.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'BB', 'check'), ('turn', 'CO', 'bet'), ('turn', 'BTN', 'call'), ('turn', 'BB', 'call'),
        ('river', 'BB', 'check'), ('river', 'CO', 'check'), ('river', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# RB5_04: Two-tone hearts river. Flop bet+calls, turn check, river CO bets 59 (33% of 180).
RB5_04 = dict(
    board_cards=['Ah', '5c', '2h', '9d', '7s'],
    hero_pos='SB',
    villain_positions=['CO', 'BTN'],
    pot=180.0,
    to_call=59.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'), ('turn', 'CO', 'check'), ('turn', 'BTN', 'check'),
        ('river', 'SB', 'check'), ('river', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# RB5_05: Rainbow river. Two streets of betting => pot=360. River BTN bets 270 (75%).
RB5_05 = dict(
    board_cards=['Kc', '9h', '4d', '6s', 'Jc'],
    hero_pos='BB',
    villain_positions=['HJ', 'BTN'],
    pot=360.0,
    to_call=270.0,
    street='river',
    action_history=[
        ('preflop', 'HJ', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'HJ', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'), ('turn', 'HJ', 'bet'), ('turn', 'BTN', 'call'), ('turn', 'BB', 'call'),
        ('river', 'BB', 'check'), ('river', 'HJ', 'check'), ('river', 'BTN', 'bet'),
    ],
    opener_position='HJ',
    effective_stack=450.0,
)

# ---------------------------------------------------------------------------
# NOT-FACING-BET FLOP BOARDS (BP4, BP5, BP6 flop situations)
# to_call=0, hero acts without a bet to face.
# ---------------------------------------------------------------------------

# NB5_01: Two-tone spades, A-high flop. BTN PFA, checks to hero (BTN).
NB5_01 = dict(
    board_cards=['As', '7s', '3d'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# NB5_02: Rainbow, K-high flop. BTN PFA, checks to hero (BTN).
NB5_02 = dict(
    board_cards=['Kc', '8h', '4d'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# NB5_03: Two-tone clubs, Q-high flop. CO PFA, hero CO acts OOP first.
NB5_03 = dict(
    board_cards=['Qc', '7c', '4h'],
    hero_pos='CO',
    villain_positions=['BB', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# NB5_04: Rainbow, J-high connected flop. BTN PFA, checks to BTN.
NB5_04 = dict(
    board_cards=['Jh', '9c', '6d'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# NB5_05: Two-tone hearts, T-high flop. BTN PFA, checks to BTN.
NB5_05 = dict(
    board_cards=['Th', '7h', '3s'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# NB5_06: Rainbow, K-high dry flop. BB OOP, checks to CO, CO hero leads.
NB5_06 = dict(
    board_cards=['Kd', '6s', '2c'],
    hero_pos='CO',
    villain_positions=['BB', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# NB5_07: Rainbow, low board. BB OOP, acts first (hero=BB).
NB5_07 = dict(
    board_cards=['8s', '4d', '2h'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# NB5_08: Two-tone spades, K-high. BB OOP, acts first (hero=BB).
NB5_08 = dict(
    board_cards=['Ks', '9s', '5d'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# ---------------------------------------------------------------------------
# NOT-FACING-BET TURN BOARDS (BP4 turn, BP7 semi-bluff)
# ---------------------------------------------------------------------------

# NT5_01: Rainbow turn. All checked flop. Hero BTN acts last on turn.
NT5_01 = dict(
    board_cards=['Kh', '8c', '3d', 'Qs'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'check'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# NT5_02: Two-tone diamonds turn. All checked flop. Hero CO acts OOP.
NT5_02 = dict(
    board_cards=['Jd', '6s', '2d', '9c'],
    hero_pos='CO',
    villain_positions=['BB', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'BB', 'check'), ('turn', 'CO', 'check'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# NT5_03: Two-tone hearts turn. Hero BB OOP, acts first on turn.
NT5_03 = dict(
    board_cards=['Th', '7d', '4h', '2s'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'BB', 'check'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# NT5_04: Rainbow turn. Hero SB OOP, acts first.
NT5_04 = dict(
    board_cards=['Ac', '6h', '3s', '8d'],
    hero_pos='SB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'SB', 'check'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# ---------------------------------------------------------------------------
# NOT-FACING-BET RIVER BOARDS (BP4 river, BP7 river bluff)
# ---------------------------------------------------------------------------

# NR5_01: Rainbow river. Hero BTN IP, checks to BTN.
NR5_01 = dict(
    board_cards=['Kd', '9s', '4c', 'Jh', '2d'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=180.0,
    to_call=0.0,
    street='river',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'check'), ('turn', 'BTN', 'check'),
        ('river', 'SB', 'check'), ('river', 'BB', 'check'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# NR5_02: Two-tone spades river. Hero BB OOP, acts first on river.
NR5_02 = dict(
    board_cards=['Qs', '8h', '3s', '6d', 'Tc'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=180.0,
    to_call=0.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'), ('turn', 'CO', 'check'), ('turn', 'BTN', 'check'),
        ('river', 'BB', 'check'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# ---------------------------------------------------------------------------
# MONOTONE FLOP BOARDS (BP6)
# ---------------------------------------------------------------------------

# MN5_01: Monotone spades flop, K-high. Hero BTN, facing bet.
MN5_01 = dict(
    board_cards=['Ks', '8s', '3s'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# MN5_02: Monotone hearts flop, Q-high. Hero BB OOP, facing bet from BTN.
MN5_02 = dict(
    board_cards=['Qh', '7h', '4h'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# MN5_03: Monotone clubs flop, J-high. Hero CO, villains SB+BB, BB bets.
MN5_03 = dict(
    board_cards=['Jc', '9c', '5c'],
    hero_pos='CO',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# MN5_04: Monotone spades flop, A-high. Hero BTN, not-facing-bet.
MN5_04 = dict(
    board_cards=['As', 'Ts', '4s'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# MN5_05: Monotone hearts flop, T-high. Hero BB OOP, not-facing-bet.
MN5_05 = dict(
    board_cards=['Th', '6h', '2h'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# ---------------------------------------------------------------------------
# FACING-BET TURN BOARDS FOR BP7 (draw semi-bluff / fold)
# ---------------------------------------------------------------------------

# TB5_06: Two-tone spades turn, connected. Facing bet. Hero BTN.
TB5_06 = dict(
    board_cards=['9s', '7c', '4s', 'Kd'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=180.0,
    to_call=59.0,
    street='turn',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'bet'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# TB5_07: Two-tone hearts turn, connected. Facing bet. Hero CO.
TB5_07 = dict(
    board_cards=['8h', '6d', '3h', 'Jc'],
    hero_pos='CO',
    villain_positions=['SB', 'BB'],
    pot=180.0,
    to_call=59.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'), ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# TB5_08: Two-tone clubs turn, J-high. Facing bet. Hero BB.
TB5_08 = dict(
    board_cards=['Jc', '8s', '5c', 'Ah'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=180.0,
    to_call=59.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'), ('turn', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# TB5_09: Two-tone spades turn. Not-facing-bet. Hero BTN. For BP7 semi-bluff.
TB5_09 = dict(
    board_cards=['Ts', '6s', '4d', '8c'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'check'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# TB5_10: Two-tone hearts turn. Not-facing-bet. Hero CO OOP (for BP7 semi-bluff OOP).
TB5_10 = dict(
    board_cards=['Qh', '9d', '5h', '7c'],
    hero_pos='CO',
    villain_positions=['BB', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'BB', 'check'), ('turn', 'CO', 'check'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# ---------------------------------------------------------------------------
# RIVER BOARDS FOR BP7 (bluff, draw call/fold)
# ---------------------------------------------------------------------------

# RB5_06: Rainbow river. Hero BTN facing bet (bricked draw).
# SB folded on turn — only BB remains as villain on river. villain_positions=['BB'] only.
RB5_06 = dict(
    board_cards=['Jh', '8d', '5c', 'Ks', '2h'],
    hero_pos='BTN',
    villain_positions=['BB'],
    pot=360.0,
    to_call=119.0,
    street='river',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'bet'), ('turn', 'BTN', 'call'), ('turn', 'SB', 'fold'),
        ('river', 'BB', 'bet'),
    ],
    opener_position='BTN',
    effective_stack=450.0,
)

# RB5_07: Two-tone spades river. Hero CO facing bet (bricked flush draw).
# SB folded on turn — only BB remains as villain on river. villain_positions=['BB'] only.
RB5_07 = dict(
    board_cards=['Ks', '9d', '4s', '7c', 'Jh'],
    hero_pos='CO',
    villain_positions=['BB'],
    pot=360.0,
    to_call=119.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'), ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'bet'), ('turn', 'CO', 'call'), ('turn', 'SB', 'fold'),
        ('river', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=450.0,
)

# =============================================================================
# SITUATIONS
#
# Each tuple: (board_base_dict, hero_cards, description, sub_pattern)
# situation_id = sub_pattern + "_" + zero-padded index within sub-pattern.
# =============================================================================

# NT5_09 is an alias for TB5_09 (not-facing-bet spade turn board).
# Must be defined before SITUATIONS list because BP4d references it.
NT5_09 = TB5_09

SITUATIONS = []

# =============================================================================
# BP1: Non-Monster RAISE (28 situations)
# All facing_bet=1.
#
# BP1a: Nut flush draw + blocker (8 situations)
#   Hero has the ace of the flush suit + one more flush suit card.
#   Example: board has two spades => hero holds As + Xs (nut FD).
#
# BP1b: Combo draw (flush + straight) (8 situations)
#   Hero has a flush draw + straight draw (9+ outs combined).
#
# BP1c: Strong two pair facing bet (4 situations)
#   Hero has two pair (both top two or top+middle) on a textured board.
#
# BP1d: CALL counterexamples (8 situations)
#   Non-nut draws, no blocker — should CALL not RAISE.
# =============================================================================

# BP1a: Nut flush draw + blocker (8 situations)
# Boards: two-tone suit present. Hero holds ace of that suit + another of same suit.

SITUATIONS += [
    # FB5_01: Ts 6s 3d. Hero holds As + another spade = nut spade flush draw.
    (FB5_01, ['As', '9s'],
     'BP1_01: As9s on Ts-6s-3d two-tone spade flop. Nut flush draw (9 outs) + ace blocker. '
     'Hero BTN IP facing BB bet 30 into 90-pot. Semi-bluff raise candidate.',
     'BP1'),
    (FB5_01, ['As', '4s'],
     'BP1_02: As4s on Ts-6s-3d two-tone spade flop. Nut flush draw + blocker. '
     'Hero BTN IP facing BB bet 30 into 90-pot. 9 flush outs.',
     'BP1'),
    # FB5_02: Qh 8h 4d. Hero holds Ah + another heart = nut heart flush draw.
    (FB5_02, ['Ah', '5h'],
     'BP1_03: Ah5h on Qh-8h-4d two-tone heart flop. Nut flush draw + blocker. '
     'Hero BB OOP facing BTN bet 30. 9 heart outs.',
     'BP1'),
    (FB5_02, ['Ah', '3h'],
     'BP1_04: Ah3h on Qh-8h-4d two-tone heart flop. Nut flush draw + ace blocker. '
     'Hero BB OOP facing BTN bet 30.',
     'BP1'),
    # FB5_03: Jc 7c 2d. Hero holds Ac + another club = nut club flush draw.
    (FB5_03, ['Ac', '6c'],
     'BP1_05: Ac6c on Jc-7c-2d two-tone club flop. Nut flush draw + blocker. '
     'Hero CO IP facing BB donk bet 30.',
     'BP1'),
    (FB5_03, ['Ac', '4c'],
     'BP1_06: Ac4c on Jc-7c-2d two-tone club flop. Nut flush draw + blocker. '
     'Hero CO IP facing BB donk bet 30.',
     'BP1'),
    # FB5_06: Ks 8s 4h. Hero holds As + another spade = nut spade flush draw.
    (FB5_06, ['As', '6s'],
     'BP1_07: As6s on Ks-8s-4h two-tone spade flop. Nut flush draw + ace blocker. '
     'Hero BB OOP facing BTN bet 30.',
     'BP1'),
    (FB5_06, ['As', '3s'],
     'BP1_08: As3s on Ks-8s-4h two-tone spade flop. Nut flush draw + blocker. '
     'Hero BB OOP facing BTN bet 30.',
     'BP1'),
]

# BP1b: Combo draw (flush + straight) (8 situations)

SITUATIONS += [
    # FB5_01: Ts 6s 3d. Hero holds 8s+7s = OESD (5-6-7-8-9 or 6-7-8-9-T) + flush draw.
    (FB5_01, ['8s', '7s'],
     'BP1_09: 8s7s on Ts-6s-3d. Combo draw: OESD (9 and 4 complete) + flush draw (9 outs). '
     '15 clean outs. Hero BTN facing BB bet 30.',
     'BP1'),
    # FB5_04: Kh 9d 3c. Hero holds Jh+Th = OESD (8-9-T-J-Q or 9-T-J-Q-K) + no flush draw on rainbow board.
    # Use FB5_07 which has hearts suit.
    # FB5_07: 9h 6h 2c. Hero holds 8h+7h = OESD + heart flush draw.
    (FB5_07, ['8h', '7h'],
     'BP1_10: 8h7h on 9h-6h-2c. Combo draw: OESD (5 or T completes) + heart flush draw. '
     '15 outs. Hero BTN facing BB bet 30.',
     'BP1'),
    (FB5_07, ['Th', '8h'],
     'BP1_11: Th8h on 9h-6h-2c. Combo draw: T-9-8-7 OESD (J or 7 completes) + heart flush draw. '
     '15 outs. Hero BTN facing BB bet 30.',
     'BP1'),
    # FB5_08: Qc 9c 5h. Hero holds Jc+Tc = OESD (8-9-T-J-Q or 9-T-J-Q-K) + club flush draw.
    (FB5_08, ['Jc', 'Tc'],
     'BP1_12: JcTc on Qc-9c-5h. Combo draw: J-T-9-8 OESD (K or 8 completes) + club flush draw. '
     '15 outs. Hero SB facing BTN bet 30.',
     'BP1'),
    (FB5_08, ['8c', '7c'],
     'BP1_13: 8c7c on Qc-9c-5h. Combo draw: 6-7-8-9-T OESD + club flush draw. '
     '15 outs. Hero SB facing BTN bet 30.',
     'BP1'),
    # TB5_01: Kd 7h 3c Th. Hero holds Jh+9h = OESD on turn (Q or 8) + heart flush draw.
    (TB5_01, ['Jh', '9h'],
     'BP1_14: Jh9h on Kd-7h-3c-Th. Combo draw on turn: OESD (Q or 8) + heart flush draw. '
     'Hero CO facing BB turn bet 30.',
     'BP1'),
    # TB5_02: Qs 7d 2c Js. Hero holds Ks+Ts = two spades (flush draw) + straight potential (K-Q-J-T-9).
    (TB5_02, ['Ks', 'Ts'],
     'BP1_15: KsTs on Qs-7d-2c-Js. Straight draw (A or 9) + spade flush draw. '
     'Hero BTN facing BB turn bet 59.',
     'BP1'),
    # FB5_10: Th 8s 6s. Hero holds 7s+5s = OESD (4-5-6-7-8 or 5-6-7-8-9) + spade flush draw.
    (FB5_10, ['7s', '5s'],
     'BP1_16: 7s5s on Th-8s-6s. Combo draw: OESD (9 or 4) + spade flush draw. '
     '15 outs. Hero BB facing BTN bet 30.',
     'BP1'),
]

# BP1c: Strong two pair facing bet (4 situations)

SITUATIONS += [
    # FB5_04: Kh 9d 3c. Hero has Kd+9c = top two pair.
    (FB5_04, ['Kd', '9c'],
     'BP1_17: KdKc... KdKc on Kh-9d-3c: actually top two pair = Kd+9c. '
     'Strong two pair (kings and nines) facing BB bet 30. Hero BTN IP.',
     'BP1'),
    # FB5_09: Jd 8c 3s. Hero has Jh+8d = top two pair.
    (FB5_09, ['Jh', '8d'],
     'BP1_18: Jh8d on Jd-8c-3s. Top two pair (jacks and eights). '
     'Hero CO facing BB donk bet 30. Strong two pair raise candidate.',
     'BP1'),
    # TB5_04: Jc 8d 3c Ks. Hero has Kh+Jd = top two pair on turn.
    (TB5_04, ['Kh', 'Jd'],
     'BP1_19: KhJd on Jc-8d-3c-Ks. Top two pair (kings and jacks) on turn. '
     'Hero BB OOP facing HJ turn bet 59.',
     'BP1'),
    # TB5_01: Kd 7h 3c Th. Hero has Kc+7d = two pair kings and sevens on turn.
    (TB5_01, ['Kc', '7d'],
     'BP1_20: Kc7d on Kd-7h-3c-Th. Two pair kings and sevens facing BB turn bet 30. '
     'Hero CO on textured two-tone turn.',
     'BP1'),
]

# BP1d: CALL counterexamples (8 situations) — non-nut draws, no blocker

SITUATIONS += [
    # Non-nut flush draw (not ace of suit)
    (FB5_01, ['Qs', '9s'],
     'BP1_21: Qs9s on Ts-6s-3d. Non-nut flush draw (Q-high FD). '
     'No ace blocker — CALL not RAISE. Hero BTN facing BB bet 30.',
     'BP1'),
    (FB5_01, ['Js', '7s'],
     'BP1_22: Js7s on Ts-6s-3d. Non-nut flush draw (J-high FD). '
     'No ace blocker — CALL not RAISE. Hero BTN facing BB bet 30.',
     'BP1'),
    (FB5_02, ['Kh', '5h'],
     'BP1_23: Kh5h on Qh-8h-4d. King-high flush draw (non-nut). '
     'CALL, not RAISE — no ace blocker. Hero BB OOP facing BTN bet 30.',
     'BP1'),
    (FB5_06, ['Js', '9s'],
     'BP1_24: Js9s on Ks-8s-4h. Non-nut spade flush draw (J-high). '
     'No ace blocker — CALL. Hero BB OOP facing BTN bet 30.',
     'BP1'),
    # OESD without flush draw — correct to CALL in 3-way
    (FB5_04, ['Jc', 'Th'],
     'BP1_25: JcTh on Kh-9d-3c. OESD (Q or 8 completes). '
     'No flush draw, 3-way — CALL not RAISE. Hero BTN facing BB bet 30.',
     'BP1'),
    (FB5_09, ['Th', '9c'],
     'BP1_26: Th9c on Jd-8c-3s. OESD (Q or 7 completes, rainbow board). '
     'Straight draw only, no flush component — CALL not RAISE. Hero CO facing BB donk bet.',
     'BP1'),
    # Weak made hand — should call not raise
    (FB5_05, ['Ah', '6d'],
     'BP1_27: Ah6d on Ad-5d-2c. Top pair weak kicker (ace-six). '
     'Kicker too weak to raise for value; CALL. Hero SB facing BTN bet 30.',
     'BP1'),
    (FB5_08, ['Qs', 'Td'],
     'BP1_28: QsTd on Qc-9c-5h. Top pair medium kicker (queen-ten). '
     'Non-nut FD board; top pair good kicker in 3-way prefers CALL. Hero SB facing BTN bet.',
     'BP1'),
]

# =============================================================================
# BP2: CALL facing bet (45 situations)
# All facing_bet=1.
#
# BP2a: Drawing hands with correct price (12)
# BP2b: Made hands in bet-and-call (10)
# BP2c: Medium made hands closing action (10)
# BP2d: Strong made hands not raising (6)
# BP2e: CALL counterexamples -> FOLD (7)
# =============================================================================

# BP2a: Drawing hands with correct price (12 situations)

SITUATIONS += [
    # Flush draws with pot odds >= equity needed
    (FB5_01, ['Qs', '8s'],
     'BP2_01: Qs8s on Ts-6s-3d. Non-nut flush draw (9 outs ~36% equity). '
     'Facing 30 into 90 (25% pot odds). Equity > price — CALL. Hero BTN.',
     'BP2'),
    (FB5_07, ['Kh', 'Jh'],
     'BP2_02: KhJh on 9h-6h-2c. King-high flush draw + overcards. '
     'Facing 30 into 90. Strong draw equity — CALL. Hero BTN.',
     'BP2'),
    (FB5_02, ['Jh', '6h'],
     'BP2_03: Jh6h on Qh-8h-4d. Jack-high flush draw (9 outs). '
     'Facing 30 into 90. Price is correct — CALL. Hero BB OOP.',
     'BP2'),
    (FB5_03, ['Kc', '8c'],
     'BP2_04: Kc8c on Jc-7c-2d. King-high flush draw + overcards. '
     'Facing 30 into 90 — CALL. Hero CO.',
     'BP2'),
    # OESD with good price
    (FB5_09, ['Th', '9c'],
     'BP2_05: Th9c on Jd-8c-3s. OESD (Q or 7, 8 outs ~32%). '
     'Facing 30 into 90 (25% price). Equity > price — CALL. Hero CO.',
     'BP2'),
    (FB5_04, ['Qd', 'Tc'],
     'BP2_06: QdTc on Kh-9d-3c. Gutshot (J, 4 outs) + two overcards. '
     'Facing 30 into 90. Combined equity sufficient — CALL. Hero BTN.',
     'BP2'),
    # Turn draws with price
    (TB5_01, ['9h', '8h'],
     'BP2_07: 9h8h on Kd-7h-3c-Th. Flush draw + OESD on turn (15 outs). '
     'Facing 30 into 90 (25% price, equity ~60%) — CALL. Hero CO.',
     'BP2'),
    (TB5_03, ['Jd', 'Tc'],
     'BP2_08: JdTc on Ah-6c-2s-9d. Gutshot + two overcards on turn. '
     'Facing 30 into 90 — CALL. Hero SB.',
     'BP2'),
    (TB5_02, ['8s', '6h'],
     'BP2_09: 8s6h on Qs-7d-2c-Js. Flush draw (spades) on turn. '
     'Facing 59 into 180 (25% price). Flush draw equity sufficient — CALL. Hero BTN.',
     'BP2'),
    # River draws that bricked — pot odds call with showdown value
    (RB5_01, ['9d', '8c'],
     'BP2_10: 9d8c on Kh-7d-2s-9c-4h. Pair of nines on river. '
     'Facing 59 into 180 (25% price). Pair has showdown value — CALL. Hero BTN.',
     'BP2'),
    (RB5_03, ['Jc', 'Td'],
     'BP2_11: JcTd on Jh-6d-2c-8s-Kd. Top pair jacks (medium kicker). '
     'Facing 59 into 180 (25% price) — CALL with one pair. Hero BB.',
     'BP2'),
    (RB5_04, ['9c', '8s'],
     'BP2_12: 9c8s on Ah-5c-2h-9d-7s. Middle pair nines on river. '
     'Facing 59 into 180. 25% price: call with showdown value — CALL. Hero SB.',
     'BP2'),
]

# BP2b: Made hands in bet-and-call (10 situations)
# Two villains have shown strength; hero has a made hand and calls.

SITUATIONS += [
    (RB5_02, ['Qd', 'Jd'],
     'BP2_13: QdJd on Qs-8d-3s-Tc-5h. Top pair queens (J kicker) on river. '
     'Two streets of villain aggression (bet-and-call context). Facing 119 into 360 — CALL. Hero CO.',
     'BP2'),
    (RB5_02, ['Ts', '9h'],
     'BP2_14: Ts9h on Qs-8d-3s-Tc-5h. Two pair tens and nines. '
     'Multi-street villain action. Facing 119 into 360 — CALL. Hero CO.',
     'BP2'),
    (RB5_05, ['Kd', 'Jh'],
     'BP2_15: KdJh on Kc-9h-4d-6s-Jc. Top pair kings (J kicker) on river. '
     'Two streets of villain aggression. Facing 270 into 360 (75%) — CALL. Hero BB.',
     'BP2'),
    (RB5_05, ['Kh', '9d'],
     'BP2_16: Kh9d on Kc-9h-4d-6s-Jc. Two pair kings and nines. '
     'Facing 270 into 360 (75% pot). Hero BB. Bet-and-call context — CALL.',
     'BP2'),
    (RB5_05, ['Ks', 'Jd'],
     'BP2_17x: KsJd on Kc-9h-4d-6s-Jc. Top pair kings (J kicker) + J pair on river. '
     'Facing 270 into 360 (75% pot). Bet-and-call context — CALL. Hero BB.',
     'BP2'),
    (TB5_04, ['Kd', 'Qh'],
     'BP2_17: KdQh on Jc-8d-3c-Ks. Top pair kings (Q kicker) on turn. '
     'Villain has shown aggression (HJ bet). Facing 59 into 180 — CALL. Hero BB.',
     'BP2'),
    (TB5_04, ['Jh', 'Tc'],
     'BP2_18: JhTc on Jc-8d-3c-Ks. Top pair jacks (T kicker) on turn. '
     'Villain aggression: HJ bet. Facing 59 into 180 — CALL. Hero BB.',
     'BP2'),
    (TB5_02, ['Qh', 'Jd'],
     'BP2_19: QhJd on Qs-7d-2c-Js. Top two pair (queens and jacks) on turn. '
     'Villain aggression: BB bet. Facing 59 into 180 — CALL (raise would over-rep). Hero BTN.',
     'BP2'),
    (TB5_02, ['Qd', 'Tc'],
     'BP2_20: QdTc on Qs-7d-2c-Js. Top pair queens (T kicker) on turn. '
     'Villain aggression (BB bet). Facing 59 into 180 — CALL. Hero BTN.',
     'BP2'),
    (RB5_01, ['Kc', 'Qd'],
     'BP2_21: KcQd on Kh-7d-2s-9c-4h. Top pair kings (Q kicker) on river. '
     'Villain showed strength (BB bet flop). Facing 59 into 180 — CALL. Hero BTN.',
     'BP2'),
    (RB5_04, ['As', 'Td'],
     'BP2_22: AsTd on Ah-5c-2h-9d-7s. Top pair aces (T kicker) on river. '
     'Villain multi-street aggression. Facing 59 into 180 — CALL. Hero SB.',
     'BP2'),
]

# BP2c: Medium made hands closing action (10 situations)
# Hero is last to act (closing action) with a marginal but correct call.

SITUATIONS += [
    (FB5_06, ['Kd', '7c'],
     'BP2_23: Kd7c on Ks-8s-4h. Top pair medium kicker (K-7). '
     'Hero BB closing action (checked BTN bet last). Facing 30 into 90 — CALL.',
     'BP2'),
    (FB5_06, ['Ah', '8d'],
     'BP2_24: Ah8d on Ks-8s-4h. Middle pair eights + overcard ace. '
     'Hero BB closing action. Facing 30 into 90 — CALL.',
     'BP2'),
    (FB5_04, ['9h', '8c'],
     'BP2_25: 9h8c on Kh-9d-3c. Middle pair nines (8 kicker). '
     'Hero BTN closing action. Facing 30 into 90 — CALL.',
     'BP2'),
    (FB5_04, ['Jd', '9s'],
     'BP2_26: Jd9s on Kh-9d-3c. Middle pair nines (J kicker). '
     'Hero BTN closing action. Facing 30 into 90 — CALL.',
     'BP2'),
    (FB5_08, ['9h', '8d'],
     'BP2_27: 9h8d on Qc-9c-5h. Middle pair nines (8 kicker). '
     'Hero SB closing action. Facing 30 into 90 — CALL.',
     'BP2'),
    (FB5_08, ['Kd', '9s'],
     'BP2_28: Kd9s on Qc-9c-5h. Middle pair nines (K overcard). '
     'Hero SB closing action. Facing 30 into 90 — CALL.',
     'BP2'),
    (TB5_01, ['Tc', 'Ks'],
     'BP2_29: TcKs on Kd-7h-3c-Th. Two pair kings and tens on turn. '
     'Hero CO closing action. Facing 30 into 90 — CALL (not raising 3-way).',
     'BP2'),
    (TB5_03, ['9c', '6d'],
     'BP2_30: 9c6d on Ah-6c-2s-9d. Two pair nines and sixes on turn. '
     'Hero SB closing action (BTN bet last). Facing 30 into 90 — CALL.',
     'BP2'),
    (RB5_03, ['8h', '6s'],
     'BP2_31: 8h6s on Jh-6d-2c-8s-Kd. Two pair eights and sixes on river. '
     'Hero BB closing action. Facing 59 into 180 — CALL.',
     'BP2'),
    (RB5_01, ['7c', '4d'],
     'BP2_32: 7c4d on Kh-7d-2s-9c-4h. Two pair sevens and fours on river. '
     'Hero BTN closing action. Facing 59 into 180 — CALL.',
     'BP2'),
]

# BP2d: Strong made hands not raising (6 situations)

SITUATIONS += [
    (FB5_04, ['Kc', 'Kd'],
     'BP2_33: KcKd on Kh-9d-3c. Set of kings (top set). '
     'Hero BTN. 3-way dynamic — CALL over raise to keep villains in. Facing 30 into 90.',
     'BP2'),
    (FB5_09, ['Jc', 'Js'],
     'BP2_35: JcJs on Jd-8c-3s. Set of jacks (top set). '
     'Hero CO. 3-way — CALL to keep range balanced/trap. Facing 30 into 90.',
     'BP2'),
    (TB5_02, ['Qh', 'Qc'],
     'BP2_36: QhQc on Qs-7d-2c-Js. Set of queens on turn. '
     'Hero BTN. Strong hand, flat board for raises in 3-way. Facing 59 into 180 — CALL.',
     'BP2'),
    (RB5_01, ['Ks', 'Kd'],
     'BP2_37: KsKd on Kh-7d-2s-9c-4h. Set of kings on river (boat potential). '
     'Hero BTN. Facing 59 into 180 — CALL (raise in 3-way commits too much). ',
     'BP2'),
    (RB5_03, ['Kh', 'Ks'],
     'BP2_38: KhKs on Jh-6d-2c-8s-Kd. Set of kings on river. '
     'Hero BB. Facing 59 into 180 — CALL to keep villain range wider.',
     'BP2'),
]

# BP2e: CALL counterexamples -> FOLD (7 situations)

SITUATIONS += [
    # Equity clearly below pot odds
    (FB5_07, ['4d', '3h'],
     'BP2_39: 4d3h on 9h-6h-2c. Weak gutshot (5) + no pair. '
     'Facing 30 into 90 (25% price). Equity ~15% — FOLD not CALL. Hero BTN.',
     'BP2'),
    (FB5_03, ['Kd', 'Qh'],
     'BP2_40: KdQh on Jc-7c-2d. Two overcards, no draw on two-tone board. '
     '3-way facing donk bet. Equity weak against BB range — FOLD. Hero CO.',
     'BP2'),
    (TB5_05, ['4h', '3d'],
     'BP2_41: 4h3d on 9d-5s-2d-7c. Gutshot (6) on diamond turn. '
     'Facing 30 into 90. Equity ~17%, 3-way — FOLD. Hero BB.',
     'BP2'),
    (RB5_04, ['Kd', 'Qh'],
     'BP2_42: KdQh on Ah-5c-2h-9d-7s. No pair, K-high on river. '
     'Facing 59 into 180. Bluff-catcher with no equity — FOLD. Hero SB.',
     'BP2'),
    (TB5_04, ['7d', '6h'],
     'BP2_43: 7d6h on Jc-8d-3c-Ks. Gutshot (9 or 4) but turn; facing bet. '
     '4 outs, 3-way, single gut shot — FOLD. Hero BB facing HJ bet 59.',
     'BP2'),
    (RB5_02, ['Ah', '2d'],
     'BP2_44: Ah2d on Qs-8d-3s-Tc-5h. A-high, no pair, pure air on river. '
     'Facing 119 into 360 — FOLD. Hero CO.',
     'BP2'),
    (RB5_05, ['7d', '6c'],
     'BP2_45: 7d6c on Kc-9h-4d-6s-Jc. Pair of sixes (bottom pair) on river. '
     'Facing 270 into 360 (75% pot). Reverse implied odds — FOLD. Hero BB.',
     'BP2'),
]

# =============================================================================
# BP3: FOLD facing bet (30 situations)
# All facing_bet=1.
#
# BP3a: Air facing bet (10)
# BP3b: Medium made vs multi-street aggression (8)
# BP3c: Drawing hands priced out (6)
# BP3d: Bet-and-call range fold (6)
# =============================================================================

# BP3a: Air facing bet (10 situations)

SITUATIONS += [
    (FB5_04, ['7h', '5c'],
     'BP3_01: 7h5c on Kh-9d-3c. Gutshot (6) only, no pair. '
     'Facing 30 into 90 — FOLD. Hero BTN, pure air against BB bet.',
     'BP3'),
    (FB5_04, ['Qh', 'Jd'],
     'BP3_02: QhJd on Kh-9d-3c. Two overcards, no flush draw, 3-way. '
     'Facing 30 into 90. Air against BB range — FOLD. Hero BTN.',
     'BP3'),
    (FB5_01, ['4h', '2d'],
     'BP3_03: 4h2d on Ts-6s-3d. Bottom pair twos + no draw. '
     'Facing 30 into 90. Weak made hand, 3-way — FOLD. Hero BTN.',
     'BP3'),
    (FB5_09, ['6c', '5h'],
     'BP3_04: 6c5h on Jd-8c-3s. Gutshot (7 or 4) only. '
     'Facing 30 into 90 — FOLD. Hero CO.',
     'BP3'),
    (FB5_09, ['Ks', 'Qc'],
     'BP3_05: KsQc on Jd-8c-3s. Two overcards, no draw. '
     'Facing 30 into 90. No pair, no draw — FOLD. Hero CO.',
     'BP3'),
    (FB5_02, ['6d', '5c'],
     'BP3_06: 6d5c on Qh-8h-4d. Gutshot (7) only. '
     'Facing 30 into 90. No flush draw, no pair — FOLD. Hero BB OOP.',
     'BP3'),
    (TB5_03, ['5d', '4c'],
     'BP3_07: 5d4c on Ah-6c-2s-9d. Bricked low straight draw (3 or 7), no pair. '
     'Facing 30 into 90 — FOLD. Hero SB.',
     'BP3'),
    (TB5_05, ['Kd', 'Qc'],
     'BP3_08: KdQc on 9d-5s-2d-7c. Two overcards, no pair. '
     'Facing 30 into 90. Air against CO range — FOLD. Hero BB.',
     'BP3'),
    (RB5_01, ['Qc', 'Jh'],
     'BP3_09: QcJh on Kh-7d-2s-9c-4h. Pure air (Q-J high, no pair). '
     'Facing 59 into 180. River air — FOLD. Hero BTN.',
     'BP3'),
    (RB5_03, ['Ah', '3c'],
     'BP3_10: Ah3c on Jh-6d-2c-8s-Kd. Pure air (A-high, no pair). '
     'Facing 59 into 180 — FOLD. Hero BB OOP.',
     'BP3'),
]

# BP3b: Medium made vs multi-street aggression (8 situations)

SITUATIONS += [
    (RB5_02, ['Ad', '3c'],
     'BP3_11: Ad3c on Qs-8d-3s-Tc-5h. A-high, no pair, pure air. '
     'Two streets of villain aggression (BB bet flop+turn). Facing 119 into 360 — FOLD. Hero CO.',
     'BP3'),
    (RB5_05, ['8h', '2c'],
     'BP3_13: 8h2c on Kc-9h-4d-6s-Jc. Pure air (8-high, no pair, no draw). '
     'Two streets of aggression. Facing 270 into 360 (75% pot). FOLD. Hero BB.',
     'BP3'),
    (TB5_04, ['9c', '6h'],
     'BP3_14: 9c6h on Jc-8d-3c-Ks. Middle pair nines on turn. '
     'HJ showed multi-street aggression. Facing 59 into 180 — FOLD. Hero BB.',
     'BP3'),
    (TB5_02, ['9h', '8d'],
     'BP3_16: 9h8d on Qs-7d-2c-Js. Middle pair nines (8 kicker) on turn. '
     'Villain showed strength (BB bet). Facing 59 into 180 — FOLD. Hero BTN.',
     'BP3'),
    (RB5_04, ['5h', '4c'],
     'BP3_17: 5h4c on Ah-5c-2h-9d-7s. Pair of fives (bottom pair) on river. '
     'Multi-street villain action. Facing 59 into 180 — FOLD. Hero SB.',
     'BP3'),
    (RB5_01, ['6d', '5s'],
     'BP3_18: 6d5s on Kh-7d-2s-9c-4h. Pair of fives (bottom). '
     'Villain BB showed strength on flop. Facing 59 into 180 — FOLD. Hero BTN.',
     'BP3'),
]

# BP3c: Drawing hands priced out (6 situations)

SITUATIONS += [
    # 4-out gutshot facing large bet
    (TB5_06, ['6c', '5d'],
     'BP3_19: 6c5d on 9s-7c-4s-Kd. Gutshot (8 or 3) — 4 outs (~17%). '
     'Facing 59 into 180 (25% price). Equity barely covers but 3-way — FOLD. Hero BTN.',
     'BP3'),
    (TB5_07, ['4d', '2c'],
     'BP3_20: 4d2c on 8h-6d-3h-Jc. Gutshot (5) only. '
     'Facing 59 into 180. 4 outs, 3-way villain range strong — FOLD. Hero CO.',
     'BP3'),
    # Flush draw facing overbet / 75% pot bet
    (RB5_05, ['Qs', 'Js'],
     'BP3_21: QsJs on Kc-9h-4d-6s-Jc. Pair of jacks + spade blocker. '
     'Facing 270 into 360 (75% river bet). Not enough equity — FOLD. Hero BB.',
     'BP3'),
    # Draw on river (missed)
    (RB5_07, ['Qs', 'Js'],
     'BP3_22: QsJs on Ks-9d-4s-7c-Jh. Pair of jacks + missed spade flush draw. '
     'Facing 119 into 360. River missed draw — FOLD. Hero CO.',
     'BP3'),
    (RB5_06, ['7s', '6s'],
     'BP3_23: 7s6s on Jh-8d-5c-Ks-2h. Bricked OESD + spade flush draw. '
     'Facing 119 into 360 — FOLD. Hero BTN.',
     'BP3'),
    (TB5_08, ['7d', '6h'],
     'BP3_24: 7d6h on Jc-8s-5c-Ah. Gutshot (9 or 4) — 4 outs. '
     'Facing 59 into 180 (25% price). In 3-way vs multi-villain aggression — FOLD. Hero BB.',
     'BP3'),
]

# BP3d: Bet-and-call range fold (6 situations)

SITUATIONS += [
    (RB5_02, ['Ah', '2d'],
     'BP3_25: Ah2d on Qs-8d-3s-Tc-5h. A-high, no pair, pure air. '
     'Both villains showed two streets of aggression. Facing 119 into 360 — FOLD. Hero CO.',
     'BP3'),
    (RB5_05, ['6h', '5d'],
     'BP3_26: 6h5d on Kc-9h-4d-6s-Jc. Pair of sixes (bottom) after two villain streets. '
     'Facing 270 into 360 — FOLD. Hero BB.',
     'BP3'),
    (RB5_02, ['4d', '3c'],
     'BP3_27: 4d3c on Qs-8d-3s-Tc-5h. Bottom pair threes. '
     'Two streets villain bet. Facing 119 into 360 — FOLD. Hero CO.',
     'BP3'),
    (TB5_04, ['5d', '4c'],
     'BP3_28: 5d4c on Jc-8d-3c-Ks. Two overcards only (no pair). '
     'Villain HJ showed aggression. Facing 59 into 180 — FOLD. Hero BB.',
     'BP3'),
    (TB5_06, ['3d', '2c'],
     'BP3_29: 3d2c on 9s-7c-4s-Kd. Pure air. '
     'Villain showed aggression. Facing 59 into 180 — FOLD. Hero BTN.',
     'BP3'),
    (TB5_07, ['Kd', 'Qh'],
     'BP3_30: KdQh on 8h-6d-3h-Jc. Two overcards, no draw. '
     'Facing 59 into 180 — FOLD. Hero CO.',
     'BP3'),
    # Two additional FOLD situations to reach count target
    (RB5_07, ['2d', '3h'],
     'BP3_31: 2d3h on Ks-9d-4s-7c-Jh. Pure air (3-high). '
     'Facing 119 into 360 — FOLD. Hero CO.',
     'BP3'),
    (TB5_08, ['2c', '3d'],
     'BP3_32: 2c3d on Jc-8s-5c-Ah. Pure air. '
     'Facing 59 into 180 — FOLD. Hero BB.',
     'BP3'),
]

# =============================================================================
# BP4: BET diverse contexts (35 situations)
# All facing_bet=0.
#
# BP4a: IP value bets non-PFA (10)
# BP4b: OOP value bets (8)
# BP4c: Semi-bluff bets (6)
# BP4d: Protection bets (5)
# BP4e: BET counterexamples -> CHECK (6)
# =============================================================================

# BP4a: IP value bets non-PFA (10 situations)

SITUATIONS += [
    (NB5_01, ['Ah', 'Kd'],
     'BP4_01: AhKd on As-7s-4d. Top pair top kicker (A-K). '
     'Hero BTN IP, PFA, checks to BTN. Value bet.',
     'BP4'),
    (NB5_01, ['Ah', 'Qc'],
     'BP4_02: AhQc on As-7s-4d. Top pair top kicker (A-Q). '
     'Hero BTN IP PFA. Value bet.',
     'BP4'),
    (NB5_02, ['Kd', 'Qs'],
     'BP4_03: KdQs on Kc-8h-4d. Top pair top kicker (K-Q). '
     'Hero BTN IP PFA. Value bet.',
     'BP4'),
    (NB5_02, ['Kd', 'Jh'],
     'BP4_04: KdJh on Kc-8h-4d. Top pair good kicker (K-J). '
     'Hero BTN IP PFA. Value bet.',
     'BP4'),
    (NT5_01, ['Kc', 'Qd'],
     'BP4_05: KcQd on Kh-8c-3d-Qs. Top two pair (K-Q) on turn. '
     'Hero BTN IP PFA. All checked to BTN on turn — value bet.',
     'BP4'),
    (NT5_01, ['Ks', 'Jd'],
     'BP4_06: KsJd on Kh-8c-3d-Qs. Top pair kings (J kicker) on turn. '
     'Hero BTN IP PFA. Value bet on turn.',
     'BP4'),
    (NB5_06, ['Kh', 'Qd'],
     'BP4_07: KhQd on Kd-6s-2c. Top pair top kicker (K-Q). '
     'Hero CO IP PFA, BB checked to CO. Value c-bet.',
     'BP4'),
    (NB5_06, ['Kh', 'Jc'],
     'BP4_08: KhJc on Kd-6s-2c. Top pair good kicker (K-J). '
     'Hero CO IP-ish (first to act after BB check). Value bet.',
     'BP4'),
    (NR5_01, ['Kh', 'Qs'],
     'BP4_09: KhQs on Kd-9s-4c-Jh-2d. Top pair kings (Q kicker) on river. '
     'Hero BTN IP. Checks to BTN — value bet river.',
     'BP4'),
    (NR5_01, ['Kc', 'Jd'],
     'BP4_10: KcJd on Kd-9s-4c-Jh-2d. Top two pair (K-J) on river. '
     'Hero BTN IP. Value bet river.',
     'BP4'),
]

# BP4b: OOP value bets (8 situations)

SITUATIONS += [
    (NB5_07, ['8d', '8c'],
     'BP4_11: 8d8c on 8s-4d-2h. Set of eights. '
     'Hero BB OOP, acts first. Strong enough to lead — value bet.',
     'BP4'),
    (NB5_07, ['8d', '4c'],
     'BP4_12: 8d4c on 8s-4d-2h. Top two pair (eights and fours). '
     'Hero BB OOP, acts first. Value lead.',
     'BP4'),
    (NB5_08, ['Kh', 'Kc'],
     'BP4_13: KhKc on Ks-9s-5d. Set of kings. '
     'Hero BB OOP. Value lead on K-high two-tone board.',
     'BP4'),
    (NB5_08, ['Kd', '9d'],
     'BP4_14: Kd9d on Ks-9s-5d. Top two pair (kings and nines). '
     'Hero BB OOP. Value lead.',
     'BP4'),
    (NT5_03, ['Tc', 'Ts'],
     'BP4_15: TcTs on Th-7d-4h-2s. Set of tens. '
     'Hero BB OOP, acts first on turn. Strong hand — value lead.',
     'BP4'),
    (NT5_03, ['Tc', '7c'],
     'BP4_16: Tc7c on Th-7d-4h-2s. Top two pair (tens and sevens). '
     'Hero BB OOP on turn. Value lead.',
     'BP4'),
    (NR5_02, ['Qd', 'Qc'],
     'BP4_17: QdQc on Qs-8h-3s-6d-Tc. Set of queens on river. '
     'Hero BB OOP. Acts first — value lead river.',
     'BP4'),
    (NR5_02, ['Qd', 'Th'],
     'BP4_18: QdTh on Qs-8h-3s-6d-Tc. Top two pair (queens and tens). '
     'Hero BB OOP. Value lead river.',
     'BP4'),
]

# BP4c: Semi-bluff bets (6 situations)

SITUATIONS += [
    (NB5_01, ['8s', '6s'],
     'BP4_19: 8s6s on As-7s-4d. Flush draw (spades) + gutshot. '
     'Hero BTN IP, all checked to BTN — semi-bluff bet.',
     'BP4'),
    (NB5_05, ['Jh', '9h'],
     'BP4_20: Jh9h on Th-7h-3s. Flush draw + OESD (J-T-9-8 or T-9-8-7). '
     'Hero BTN IP, all checked to BTN — semi-bluff bet.',
     'BP4'),
    (NB5_04, ['Kd', 'Qh'],
     'BP4_21: KdQh on Jh-9c-6d. Two overcards + gutshot (T). '
     'Hero BTN IP, all checked — semi-bluff bet on connected board.',
     'BP4'),
    (NT5_02, ['8d', '7h'],
     'BP4_22: 8d7h on Jd-6s-2d-9c. Flush draw (diamonds) + OESD (8-7-6 needs 5 or T). '
     'Hero CO on turn — semi-bluff bet.',
     'BP4'),
    (NT5_04, ['5h', '4h'],
     'BP4_23: 5h4h on Ac-6h-3s-8d. Straight draw (7 or 2) + backdoor flush. '
     'Hero SB OOP on turn — semi-bluff lead.',
     'BP4'),
    (NB5_03, ['Ad', '9d'],
     'BP4_24: Ad9d on Qc-7c-4h. Overcards + nut club blocker. '
     'Hero CO OOP — semi-bluff bet with fold equity on Q-high board.',
     'BP4'),
]

# BP4d: Protection bets (5 situations)

SITUATIONS += [
    (NB5_02, ['Kh', '8d'],
     'BP4_25: Kh8d on Kc-8h-4d. Top two pair (kings and eights). '
     'Hero BTN. Dynamic board (4 can come) — protection bet.',
     'BP4'),
    (NB5_04, ['Jc', 'Td'],
     'BP4_26: JcTd on Jh-9c-6d. Top pair jacks (T kicker) on connected board. '
     'Hero BTN. Board is T-9-8 / J-9-7 connected — protection bet to deny equity.',
     'BP4'),
    (NB5_05, ['Tc', '7d'],
     'BP4_27: Tc7d on Th-7h-3s. Top two pair (tens and sevens) on two-tone board. '
     'Hero BTN. Protection bet on draw-heavy board.',
     'BP4'),
    (NT5_01, ['Ks', '8h'],
     'BP4_28: Ks8h on Kh-8c-3d-Qs. Top two pair on turn with straight potential. '
     'Hero BTN. Protection bet — deny equity from draws.',
     'BP4'),
    (NT5_09, ['Td', '9d'],
     'BP4_29: Td9d on Ts-6s-4d-8c. Top pair tens (9 kicker) on spade turn. '
     'Hero BTN. Made hand on flush-draw board — protection bet.',
     'BP4'),
]

# BP4e: BET counterexamples -> CHECK (6 situations)

SITUATIONS += [
    (NB5_04, ['8s', '7d'],
     'BP4_30: 8s7d on Jh-9c-6d. Middle pair eights on connected board. '
     'Hero BTN. Bet looks natural but CHECK preferred — range advantage unclear on J-9-6.',
     'BP4'),
    (NB5_01, ['7c', '4d'],
     'BP4_31: 7c4d on As-7s-4d. Two pair sevens and fours. '
     'Hero BTN. Strong hand but CHECK — trap on A-high board where villain bets.',
     'BP4'),
    (NT5_01, ['9d', '7c'],
     'BP4_32: 9d7c on Kh-8c-3d-Qs. Middle pair nines on turn. '
     'Hero BTN. Marginal hand on dry turn — CHECK.',
     'BP4'),
    (NB5_03, ['Jd', 'Th'],
     'BP4_33: JdTh on Qc-7c-4h. Top pair jacks (T kicker). '
     'Hero CO OOP on two-tone board. Tempting to bet but villain range strong — CHECK.',
     'BP4'),
    (NR5_02, ['9d', '6h'],
     'BP4_34: 9d6h on Qs-8h-3s-6d-Tc. Pair of sixes on river. '
     'Hero BB OOP. Weak made hand river — CHECK not bet.',
     'BP4'),
    (NT5_02, ['Kh', 'Qd'],
     'BP4_35: KhQd on Jd-6s-2d-9c. Two overcards on turn. '
     'Hero CO. Tempting semi-bluff but villain range strong — CHECK.',
     'BP4'),
]

# =============================================================================
# BP5: CHECK counterexamples (17 situations)
# All facing_bet=0.
#
# BP5a: Trap with monster (6)
# BP5b: Pot control that should be thin value (5)
# BP5c: Air checking -> should bluff (6)
# =============================================================================

# BP5a: Trap consideration (6 situations)

SITUATIONS += [
    (NB5_07, ['4h', '2d'],
     'BP5_01: 4h2d on 8s-4d-2h. Bottom two pair (fours and twos). '
     'Hero BB OOP. Trap tempting — but 3-way thin value bet is correct on dry low board.',
     'BP5'),
    (NB5_08, ['9d', '9c'],
     'BP5_02: 9d9c on Ks-9s-5d. Set of nines. '
     'Hero BB OOP. Monster trap consideration — but value bet extracts more.',
     'BP5'),
    (NT5_01, ['Qd', 'Qc'],
     'BP5_03: QdQc on Kh-8c-3d-Qs. Set of queens on turn. '
     'Hero BTN IP. Strong hand — slowplay tempting but bet for value.',
     'BP5'),
    (NR5_01, ['Jc', 'Jd'],
     'BP5_04: JcJd on Kd-9s-4c-Jh-2d. Set of jacks on river. '
     'Hero BTN IP. Monster — trap consideration, but river value bet is best.',
     'BP5'),
    (NB5_03, ['Qd', 'Qh'],
     'BP5_05: QdQh on Qc-7c-4h. Set of queens on two-tone flop. '
     'Hero CO OOP. Trap tempting but bet extracts value in 3-way.',
     'BP5'),
    (NT5_03, ['4d', '2c'],
     'BP5_06: 4d2c on Th-7d-4h-2s. Bottom two pair (fours and twos). '
     'Hero BB OOP on turn. Slowplay tempting but leading extracts value.',
     'BP5'),
]

# BP5b: Pot control that should be thin value (5 situations)

SITUATIONS += [
    (NB5_02, ['Kh', 'Td'],
     'BP5_07: KhTd on Kc-8h-4d. Top pair medium kicker (K-T). '
     'Hero BTN IP. Pot control tempting, but thin value bet correct.',
     'BP5'),
    (NB5_06, ['Kh', '9s'],
     'BP5_08: Kh9s on Kd-6s-2c. Top pair medium kicker (K-9). '
     'Hero CO. Thin value bet — correct to bet not check on dry K-high board.',
     'BP5'),
    (NT5_04, ['Ah', 'Ks'],
     'BP5_10: AhKs on Ac-6h-3s-8d. Top pair top kicker on turn. '
     'Hero SB OOP. Pot control tempting but value lead correct.',
     'BP5'),
    (NR5_02, ['Qh', 'Jd'],
     'BP5_11: QhJd on Qs-8h-3s-6d-Tc. Top pair queens (J kicker) on river. '
     'Hero BB OOP. Pot control tempting — but thin river bet extracts value.',
     'BP5'),
]

# BP5c: Air checking -> should bluff (6 situations)

SITUATIONS += [
    (NB5_01, ['9d', '8c'],
     'BP5_12: 9d8c on As-7s-4d. Gutshot (T or 6) + no pair. '
     'Hero BTN IP. Air but fold equity on A-high board — bluff bet correct.',
     'BP5'),
    (NB5_06, ['Jc', 'Th'],
     'BP5_13: JcTh on Kd-6s-2c. Two overcards, dry board. '
     'Hero CO. Air but fold equity on K-6-2r — bluff beat correct.',
     'BP5'),
    (NT5_01, ['6h', '5d'],
     'BP5_14: 6h5d on Kh-8c-3d-Qs. Pure air. '
     'Hero BTN IP on turn. Board favours BTN range — bluff is correct.',
     'BP5'),
    (NT5_04, ['Jd', '2h'],
     'BP5_15: Jd2h on Ac-6h-3s-8d. Pure air (J-high, no draw). '
     'Hero SB OOP on turn. Bluff correct on A-high board favoring SB 3-bet range.',
     'BP5'),
    (NR5_01, ['6c', '5d'],
     'BP5_16: 6c5d on Kd-9s-4c-Jh-2d. Pure air (6-high). '
     'Hero BTN IP on river. Board favours BTN — bluff is correct.',
     'BP5'),
    (NT5_02, ['Ah', 'Qd'],
     'BP5_16x: AhQd on Jd-6s-2d-9c. Two overcards on diamond turn. '
     'Hero CO OOP. Air but fold equity on J-high — bluff lead is correct.',
     'BP5'),
    (NB5_04, ['Ac', 'Kd'],
     'BP5_17: AcKd on Jh-9c-6d. Two overcards on connected board. '
     'Hero BTN IP. Air but board favours BTN range — bluff bet is correct.',
     'BP5'),
]

# =============================================================================
# BP6: Monotone board situations (12 situations)
# Mixed facing_bet. Mixed streets.
#
# BP6a: Hero has flush draw on monotone (5)
# BP6b: Hero has made flush on monotone (4)
# BP6c: Hero has no flush card on monotone (3)
# =============================================================================

# BP6a: Flush draw on monotone (5 situations)

SITUATIONS += [
    (MN5_01, ['As', '4d'],
     'BP6_01: As4d on Ks-8s-3s monotone. Nut flush draw (As). '
     'Hero BTN IP facing BB bet 30. Flush draw on monotone board.',
     'BP6'),
    (MN5_01, ['Qs', '4d'],
     'BP6_02: Qs4d on Ks-8s-3s monotone. Q-high flush draw (non-nut). '
     'Hero BTN IP facing BB bet 30. Non-nut flush draw on monotone.',
     'BP6'),
    (MN5_02, ['Ah', '6d'],
     'BP6_03: Ah6d on Qh-7h-4h monotone. Nut flush draw (Ah). '
     'Hero BB OOP facing BTN bet 30. Flush draw on monotone.',
     'BP6'),
    (MN5_03, ['Ac', '7d'],
     'BP6_04: Ac7d on Jc-9c-5c monotone. Nut flush draw (Ac). '
     'Hero CO facing BB donk bet 30. Flush draw on monotone.',
     'BP6'),
    (MN5_04, ['Js', '5d'],
     'BP6_05: Js5d on As-Ts-4s monotone. Non-nut flush draw (Js). '
     'Hero BTN IP, not-facing-bet. Flush draw consideration on monotone.',
     'BP6'),
]

# BP6b: Made flush on monotone (4 situations)

SITUATIONS += [
    (MN5_01, ['As', 'Qs'],
     'BP6_06: AsQs on Ks-8s-3s monotone. Nut flush (A-Q-K-8-3). '
     'Hero BTN IP facing BB bet 30. Made flush value.',
     'BP6'),
    (MN5_02, ['Kh', 'Jh'],
     'BP6_07: KhJh on Qh-7h-4h monotone. Strong made flush (K-J). '
     'Hero BB OOP facing BTN bet 30. Made flush on monotone.',
     'BP6'),
    (MN5_03, ['Kc', 'Qc'],
     'BP6_08: KcQc on Jc-9c-5c. Strong made flush (K-Q-J-9-5). '
     'Hero CO facing BB donk bet 30. Value with made flush on monotone.',
     'BP6'),
]

# BP6c: No flush card on monotone (3 situations)

SITUATIONS += [
    (MN5_01, ['Ah', 'Kd'],
     'BP6_10: AhKd on Ks-8s-3s monotone. Top pair (K on board) + no spade. '
     'Hero BTN IP facing BB bet 30. Made hand without flush card — complex spot.',
     'BP6'),
    (MN5_05, ['Kd', 'Qh'],
     'BP6_11: KdQh on Th-6h-2h monotone. Two overcards, no heart. '
     'Hero BB OOP, not-facing-bet. Air on monotone — check.',
     'BP6'),
    (MN5_02, ['Ad', 'Kc'],
     'BP6_12: AdKc on Qh-7h-4h monotone. Two overcards, no heart. '
     'Hero BB OOP facing BTN bet 30. No flush equity — fold consideration.',
     'BP6'),
    (MN5_04, ['6d', '4c'],
     'BP6_13: 6d4c on As-Ts-4s monotone. No spade, bottom pair fours. '
     'Hero BTN IP not-facing-bet. Weak hand on monotone — check.',
     'BP6'),
]

# =============================================================================
# BP7: Drawing hand RAISE diversity (18 situations)
# Mixed facing_bet.
#
# BP7a: Turn semi-bluff raises (6)
# BP7b: River bluff raises (4)
# BP7c: Draws that should CALL not RAISE (5)
# BP7d: Draws that should FOLD not CALL (3)
# =============================================================================

# BP7a: Turn semi-bluff raises (6 situations) — facing bet, raise candidate

SITUATIONS += [
    (TB5_06, ['As', 'Js'],
     'BP7_01: AsJs on 9s-7c-4s-Kd. Nut flush draw + overcards on turn. '
     'Hero BTN facing BB bet 59. Semi-bluff raise candidate.',
     'BP7'),
    (TB5_06, ['8s', '6s'],
     'BP7_02: 8s6s on 9s-7c-4s-Kd. Flush draw + OESD (T or 5) — 15 outs. '
     'Hero BTN facing BB bet 59. Strong semi-bluff raise.',
     'BP7'),
    (TB5_07, ['Ah', '5h'],
     'BP7_03: Ah5h on 8h-6d-3h-Jc. Nut flush draw + overcard on turn. '
     'Hero CO facing BB bet 59. Semi-bluff raise candidate.',
     'BP7'),
    (TB5_07, ['9h', '7h'],
     'BP7_04: 9h7h on 8h-6d-3h-Jc. Flush draw + OESD (T-9-8-7-6 or 9-8-7-6-5). '
     '15 outs. Hero CO facing BB bet 59. Strong semi-bluff raise.',
     'BP7'),
    (TB5_09, ['9s', '7s'],
     'BP7_05: 9s7s on Ts-6s-4d-8c. Flush draw + OESD (J or 5). '
     'Hero BTN IP not-facing-bet — semi-bluff bet/raise.',
     'BP7'),
    (TB5_10, ['Ah', 'Jh'],
     'BP7_06: AhJh on Qh-9d-5h-7c. Nut flush draw + overcard on turn. '
     'Hero CO OOP not-facing-bet — semi-bluff lead.',
     'BP7'),
]

# BP7b: River bluff raises (4 situations)

SITUATIONS += [
    (RB5_06, ['9s', '8s'],
     'BP7_07: 9s8s on Jh-8d-5c-Ks-2h. Bricked OESD (T-9-8-7, needed 6 or Q on turn). '
     'River missed — bluff raise with fold equity. Hero BTN facing BB bet 119.',
     'BP7'),
    (RB5_06, ['7d', '6c'],
     'BP7_08: 7d6c on Jh-8d-5c-Ks-2h. Bricked OESD (6-7-8-9-T, needed 9 or 4). '
     'River missed. Hero BTN facing BB bet 119 — bluff raise.',
     'BP7'),
    (RB5_07, ['As', '2s'],
     'BP7_09: As2s on Ks-9d-4s-7c-Jh. Bricked nut flush draw (spades). '
     'Holding blocker As — river bluff raise candidate. Hero CO facing BB bet 119.',
     'BP7'),
    (RB5_07, ['Ac', 'Tc'],
     'BP7_10: AcTc on Ks-9d-4s-7c-Jh. Pure air (A-T, no pair). '
     'Hero CO facing BB bet 119 — river bluff raise.',
     'BP7'),
]

# BP7c: Draws that should CALL not RAISE (5 situations)

SITUATIONS += [
    (TB5_08, ['Ac', '8d'],
     'BP7_11: Ac8d on Jc-8s-5c-Ah. Top pair aces + club flush draw. '
     'Hero BB OOP facing CO bet 59. Strong hand — CALL over raise 3-way.',
     'BP7'),
    (TB5_06, ['Th', '8d'],
     'BP7_12: Th8d on 9s-7c-4s-Kd. OESD (J or 6) without flush draw. '
     'Hero BTN facing BB bet 59. 8 outs — CALL not raise in 3-way.',
     'BP7'),
    (TB5_07, ['7c', '5d'],
     'BP7_13: 7c5d on 8h-6d-3h-Jc. OESD (9 or 4) — 8 outs, no flush draw. '
     'Hero CO facing BB bet 59 — CALL not raise in 3-way.',
     'BP7'),
    (RB5_06, ['Qd', 'Th'],
     'BP7_14: QdTh on Jh-8d-5c-Ks-2h. One pair (tens)... actually T pairs board? '
     'No T on board. Pair of tens + missed OESD. Facing BB bet 119 — CALL.',
     'BP7'),
    (TB5_08, ['9d', '6c'],
     'BP7_15: 9d6c on Jc-8s-5c-Ah. OESD (T or 4) — 8 outs on turn. '
     'Hero BB facing CO bet 59 — CALL not raise in 3-way.',
     'BP7'),
]

# BP7d: Draws that should FOLD not CALL (3 situations)

SITUATIONS += [
    (TB5_06, ['5c', '3d'],
     'BP7_16: 5c3d on 9s-7c-4s-Kd. Gutshot (6 or 2) — 4 outs only. '
     'Facing 59 into 180. Not enough equity — FOLD. Hero BTN.',
     'BP7'),
    (TB5_07, ['4c', '2d'],
     'BP7_17: 4c2d on 8h-6d-3h-Jc. Gutshot (5 or 7 for straight)... '
     '4c2d: need 5 for 2-3-4-5-6 or 3-4-5-6-7. 4 outs. Facing 59 into 180 — FOLD. Hero CO.',
     'BP7'),
    (RB5_07, ['6d', '5h'],
     'BP7_18: 6d5h on Ks-9d-4s-7c-Jh. Bricked straight draw (6-5 needed 4-5-6-7-8 or 5-6-7-8-9). '
     'No pair, pure air. Facing 119 into 360 — FOLD. Hero CO.',
     'BP7'),
]

# =============================================================================
# VALIDATION: verify expected counts per batch pattern
# =============================================================================

_EXPECTED_COUNTS = {
    'BP1': 28,
    'BP2': 45,
    'BP3': 30,
    'BP4': 35,
    'BP5': 17,
    'BP6': 12,
    'BP7': 18,
}


def _check_situation_counts():
    from collections import Counter
    counts = Counter(sp for _, _, _, sp in SITUATIONS)
    errors = []
    for sp, expected in _EXPECTED_COUNTS.items():
        actual = counts.get(sp, 0)
        if actual != expected:
            errors.append(f"  {sp}: expected {expected}, got {actual}")
    if errors:
        print("SITUATION COUNT MISMATCHES:")
        for e in errors:
            print(e)
        return False
    total = sum(_EXPECTED_COUNTS.values())
    print(f"Situation count check PASSED — {total} total situations defined.")
    return True


# =============================================================================
# GENERATION + VALIDATION
# =============================================================================

def generate_all():
    """Build, validate, and collect all situations."""
    all_records = []
    total_generated = 0
    total_validated = 0
    error_log = []

    for idx, (board_base, hero_cards, description, sub_pattern) in enumerate(SITUATIONS):
        sp_situations = [s for s in SITUATIONS[:idx + 1] if s[3] == sub_pattern]
        sit_num = len(sp_situations)
        sit_id = f"{sub_pattern}_{sit_num:02d}"

        total_generated += 1

        spec_kwargs = dict(board_base)
        spec_kwargs['hero_cards'] = hero_cards
        spec = SituationSpec(**spec_kwargs)

        try:
            feat_dict = build_situation(spec)
        except Exception as exc:
            error_log.append((sit_id, 'BUILD_EXCEPTION', str(exc)))
            print(f"  SKIP  {sit_id} {hero_cards}: BUILD_EXCEPTION: {exc}")
            continue

        validation_errors = validate_situation(spec, feat_dict)

        hero_cards_str = ''.join(hero_cards)
        board_cards_str = ''.join(board_base['board_cards'])

        feat_dict['situation_id'] = sit_id
        feat_dict['sub_pattern'] = sub_pattern
        feat_dict['hero_cards'] = hero_cards_str
        feat_dict['board_cards'] = board_cards_str
        feat_dict['description'] = description
        feat_dict['action_string'] = spec.action_string
        feat_dict['hero_position'] = spec.hero_pos
        feat_dict['villain_positions'] = list(spec.villain_positions)
        feat_dict['street'] = spec.street

        if validation_errors:
            feat_dict['has_errors'] = True
            feat_dict['validation_errors'] = validation_errors
            error_log.append((sit_id, 'VALIDATION_ERRORS', '; '.join(validation_errors)))
            print(f"  WARN  {sit_id} {hero_cards}: {'; '.join(validation_errors)}")
        else:
            feat_dict['has_errors'] = False
            total_validated += 1
            print(f"  OK    {sit_id} {hero_cards}")

        all_records.append(feat_dict)

    return all_records, total_generated, total_validated, error_log


def main():
    print("=" * 60)
    print("FACTORY BATCH 5 — ~185-SITUATION PHASE 2B BATCH")
    print("=" * 60)

    if not _check_situation_counts():
        print("\nABORTING — fix count mismatches before running.")
        return False

    print(f"\nGenerating {len(SITUATIONS)} situations...")
    records, total_gen, total_valid, errors = generate_all()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        for record in records:
            # ANOMALY-A fix: normalise street/hero_position at serialisation.
            f.write(json.dumps(normalise_situation(record)) + '\n')

    print(f"\n{'=' * 60}")
    print("GENERATION COMPLETE")
    print(f"  Total defined:   {len(SITUATIONS)}")
    print(f"  Total generated: {total_gen}")
    print(f"  Total validated: {total_valid}  (no errors)")
    print(f"  Has errors:      {total_gen - total_valid}")
    print(f"  Written to:      {OUTPUT_PATH}")

    if errors:
        print(f"\nERROR LOG ({len(errors)} items):")
        for sit_id, error_type, detail in errors:
            print(f"  [{error_type}] {sit_id}: {detail}")
    else:
        print("\nNo errors logged.")

    return len(errors) == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
