"""
Generate all 151 RAISE/CALL situations from design agent outputs through
SituationFactory, validate each, and write results to:
  training-data/factory_batch3_situations.jsonl

Source documents consumed:
  BOARD_ALLOCATION_V3_FINAL.md  (33 board definitions)
  DESIGN_AGENT_1_SP5_SP6.md     (SP5 x28, SP6 x13)
  DESIGN_AGENT_2_SP1_SP2_SP3_SP4.md  (SP1 x18, SP2 x10, SP3 x12, SP4 x6)
  DESIGN_AGENT_3_SP7_SP10.md    (SP7 x25, SP10 x13)
  DESIGN_AGENT_4_SP8_SP9.md     (SP8 x16, SP9 x10)

DO NOT RUN until reviewed. See review/comms/ for delivery note.

Run from any directory:
    python3 /home/rupertbeytell/river-rats-v2/review/generate_factory_batch3.py
"""

import sys
import os
import json

sys.path.insert(0, '/home/rupertbeytell/river-rats-v2/river-rats-core')
os.chdir('/home/rupertbeytell/river-rats-v2/river-rats-core')

from situation_factory import SituationSpec, build_situation, validate_situation

OUTPUT_PATH = '/home/rupertbeytell/river-rats-v2/training-data/factory_batch3_situations.jsonl'

# =============================================================================
# BOARD BASES (B01 – B33 + B10_LOW, B17_LOW)
#
# Naming convention:
#   B10     = baseline effective_stack=810 (SP10 usage, SPR=9.0)
#   B10_LOW = effective_stack=135, SPR=1.5 (SP2 usage)
#   B17     = baseline effective_stack=540 (SP3/SP7/SP9 usage, SPR=3.0)
#   B17_LOW = effective_stack=270, SPR=1.5 (SP2 usage)
#
# villain_positions: non-bettors first, bettor LAST.
# to_call=0 means hero leads (check/bet decision).
# =============================================================================

B01 = dict(
    board_cards=['2c', 'Tc', '6d'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],  # BB is bettor
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

B02 = dict(
    board_cards=['Kh', '7h', '3d'],
    hero_pos='BB',
    villain_positions=['HJ', 'BTN'],  # BTN is bettor
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

B03 = dict(
    board_cards=['As', '5d', '2c'],
    hero_pos='CO',
    villain_positions=['SB', 'BB'],  # BB is bettor (donk)
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=810.0,
)

B04 = dict(
    board_cards=['Jd', '9d', '4s'],
    hero_pos='SB',
    villain_positions=['CO', 'BTN'],  # BTN is bettor
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=405.0,
)

B05 = dict(
    board_cards=['6s', '4s', 'Qs'],
    hero_pos='BTN',
    villain_positions=['BB', 'CO'],  # CO is bettor
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=530.0,  # SPR=5.89 — see BOARD_ALLOCATION_V3_FINAL FIX note
)

B06 = dict(
    board_cards=['8c', '8h', '3d'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],  # BTN is bettor
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=495.0,
)

B07 = dict(
    board_cards=['5h', '6c', '7d'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],  # BB is bettor
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'),
    ],
    opener_position='BTN',
    effective_stack=810.0,
)

B08 = dict(
    board_cards=['Qc', '5c', '9h'],
    hero_pos='BB',
    villain_positions=['HJ', 'BTN'],  # BTN is bettor
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

B09 = dict(
    board_cards=['Ah', '4h', '8c'],
    hero_pos='CO',
    villain_positions=['SB', 'BB'],  # BB is bettor (donk)
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=720.0,
)

# B10 baseline (SPR=9.0) — used by SP10 sit#2
B10 = dict(
    board_cards=['Kc', '4d', '2h'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],  # no bettor — hero leads, to_call=0
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
    ],
    opener_position='CO',
    effective_stack=810.0,
)

# B10 low-stack override (SPR=1.5) — used by SP2 sits 1-2
B10_LOW = dict(
    board_cards=['Kc', '4d', '2h'],
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
    effective_stack=135.0,  # SPR = 135/90 = 1.5
)

B11r = dict(
    board_cards=['Ts', '8s', '4h'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],  # BB is bettor
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

B12 = dict(
    board_cards=['7c', '2d', 'Kc', 'Ac'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],  # BTN is bettor
    pot=210.0,
    to_call=70.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'), ('turn', 'CO', 'check'), ('turn', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=630.0,
)

B13 = dict(
    board_cards=['Qd', '6h', '2s', 'Jc'],
    hero_pos='SB',
    villain_positions=['CO', 'BTN'],  # BTN is bettor
    pot=200.0,
    to_call=70.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'SB', 'check'), ('turn', 'CO', 'check'), ('turn', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=1680.0,
)

B14 = dict(
    board_cards=['3s', 'Js', '9h', '4d'],
    hero_pos='CO',
    villain_positions=['SB', 'BB'],  # BB is bettor (donk turn)
    pot=180.0,
    to_call=60.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'CO', 'check'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=540.0,
)

B15 = dict(
    board_cards=['Tc', '3d', '9h', '9s'],
    hero_pos='BB',
    villain_positions=['HJ', 'BTN'],  # BTN is bettor
    pot=200.0,
    to_call=65.0,
    street='turn',
    action_history=[
        ('preflop', 'HJ', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'HJ', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'BB', 'check'), ('turn', 'HJ', 'check'), ('turn', 'BTN', 'bet'),
    ],
    opener_position='HJ',
    effective_stack=520.0,
)

B16 = dict(
    board_cards=['5h', 'Kd', '2h', '8c'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],  # BB is bettor
    pot=180.0,
    to_call=60.0,
    street='turn',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'bet'),
    ],
    opener_position='BTN',
    effective_stack=720.0,
)

# B17 baseline (SPR=3.0) — used by SP3, SP7, SP9
B17 = dict(
    board_cards=['Ad', '7s', '3c', '2h'],
    hero_pos='SB',
    villain_positions=['BTN', 'BB'],  # no bettor — hero leads, to_call=0
    pot=180.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'SB', 'check'),
    ],
    opener_position='BTN',
    effective_stack=540.0,
)

# B17 low-stack override (SPR=1.5) — used by SP2 sits 3-4
B17_LOW = dict(
    board_cards=['Ad', '7s', '3c', '2h'],
    hero_pos='SB',
    villain_positions=['BTN', 'BB'],
    pot=180.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'SB', 'check'),
    ],
    opener_position='BTN',
    effective_stack=270.0,  # SPR = 270/180 = 1.5
)

B18 = dict(
    board_cards=['4d', '8d', 'Kh', '5c'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],  # CO is bettor
    pot=190.0,
    to_call=65.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'), ('turn', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=760.0,
)

B19 = dict(
    board_cards=['4c', '6h', '8s', '7d'],
    hero_pos='BTN',
    villain_positions=['BB', 'SB'],  # SB is bettor (donk)
    pot=180.0,
    to_call=55.0,
    street='turn',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'SB', 'bet'),
    ],
    opener_position='BTN',
    effective_stack=360.0,
)

B20 = dict(
    board_cards=['2c', '9c', 'Qh', '6s'],
    hero_pos='CO',
    villain_positions=['SB', 'BB'],  # BB is bettor
    pot=200.0,
    to_call=80.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'), ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=280.0,
)

B21 = dict(
    board_cards=['3h', '3d', '9s', 'Kc'],
    hero_pos='SB',
    villain_positions=['CO', 'BTN'],  # BTN is bettor
    pot=190.0,
    to_call=65.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'SB', 'check'), ('turn', 'CO', 'check'), ('turn', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=570.0,
)

B22 = dict(
    board_cards=['Jh', '4c', '2h', 'Td'],
    hero_pos='BB',
    villain_positions=['HJ', 'BTN'],  # HJ is bettor
    pot=200.0,
    to_call=70.0,
    street='turn',
    action_history=[
        ('preflop', 'HJ', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'HJ', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'), ('turn', 'HJ', 'bet'),
    ],
    opener_position='HJ',
    effective_stack=280.0,
)

B23 = dict(
    board_cards=['Kd', '7c', '2s', '5h', 'Jh'],
    hero_pos='BTN',
    villain_positions=['BB'],  # BB is bettor; SB folded on turn
    pot=400.0,
    to_call=120.0,
    street='river',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
        ('flop', 'SB', 'call'), ('flop', 'BB', 'call'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'check'), ('turn', 'BTN', 'bet'),
        ('turn', 'SB', 'fold'), ('turn', 'BB', 'call'),
        ('river', 'BB', 'bet'),
    ],
    opener_position='BTN',
    effective_stack=360.0,
)

B24 = dict(
    board_cards=['9s', '4h', 'Ks', '2d', '7c'],
    hero_pos='SB',
    villain_positions=['CO', 'BTN'],  # BTN is bettor
    pot=380.0,
    to_call=110.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'), ('turn', 'CO', 'check'), ('turn', 'BTN', 'check'),
        ('river', 'SB', 'check'), ('river', 'CO', 'check'), ('river', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=330.0,
)

B25 = dict(
    board_cards=['As', '6d', '2h', 'Tc', '4s'],
    hero_pos='CO',
    villain_positions=['BB'],  # BB is bettor; SB folded on flop
    pot=360.0,
    to_call=100.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
        ('flop', 'SB', 'fold'), ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'), ('turn', 'CO', 'bet'), ('turn', 'BB', 'call'),
        ('river', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=320.0,
)

B26 = dict(
    board_cards=['Kh', '5c', '2h', '9d', 'Qh'],
    hero_pos='BB',
    villain_positions=['CO'],  # CO is bettor; BTN folded on flop
    pot=370.0,
    to_call=110.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BTN', 'fold'), ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'), ('turn', 'CO', 'bet'), ('turn', 'BB', 'call'),
        ('river', 'BB', 'check'), ('river', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=300.0,
)

B27 = dict(
    board_cards=['4d', '8h', '2c', '6s', 'Jd'],
    hero_pos='BTN',
    villain_positions=['SB'],  # SB is bettor; BB folded on flop
    pot=350.0,
    to_call=100.0,
    street='river',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'BTN', 'bet'),
        ('flop', 'SB', 'call'), ('flop', 'BB', 'fold'),
        ('turn', 'SB', 'check'), ('turn', 'BTN', 'check'),
        ('river', 'SB', 'bet'),
    ],
    opener_position='BTN',
    effective_stack=315.0,
)

B28 = dict(
    board_cards=['3s', '7h', 'Ks', '2c', 'Ts'],
    hero_pos='CO',
    villain_positions=['SB', 'BB'],  # BB is bettor
    pot=400.0,
    to_call=120.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'),
        ('flop', 'SB', 'call'), ('flop', 'BB', 'call'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'check'), ('turn', 'CO', 'check'),
        ('river', 'SB', 'check'), ('river', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=360.0,
)

B29 = dict(
    board_cards=['Qc', '6s', '2d', '9h', '4c'],
    hero_pos='BB',
    villain_positions=['HJ', 'BTN'],  # BTN is bettor
    pot=380.0,
    to_call=120.0,
    street='river',
    action_history=[
        ('preflop', 'HJ', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'HJ', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'BB', 'check'), ('turn', 'HJ', 'bet'), ('turn', 'BTN', 'call'), ('turn', 'BB', 'call'),
        ('river', 'BB', 'check'), ('river', 'HJ', 'check'), ('river', 'BTN', 'bet'),
    ],
    opener_position='HJ',
    effective_stack=340.0,
)

B30 = dict(
    board_cards=['5c', '3d', '2s'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],  # BB is bettor
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'bet'),
    ],
    opener_position='BTN',
    effective_stack=90.0,
)

B31 = dict(
    board_cards=['7d', '2c', 'Ks', '4h'],
    hero_pos='CO',
    villain_positions=['SB', 'BB'],  # BB is bettor
    pot=180.0,
    to_call=60.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'BB', 'check'), ('flop', 'CO', 'check'),
        ('turn', 'SB', 'check'), ('turn', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=252.0,
)

# B32 is in the board inventory but carries zero situation assignments (FIX 1).
# Not defined here to avoid accidental use.

B33 = dict(
    board_cards=['Qh', 'Qd', '7h'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],  # BTN is bettor
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=495.0,
)

# =============================================================================
# SITUATIONS
#
# Each tuple: (board_base_dict, hero_cards, description, sub_pattern)
# Ordered by sub-pattern, then by sit number within each sub-pattern.
# =============================================================================

SITUATIONS = []

# ---------------------------------------------------------------------------
# SP1: Monster + wet board + low SPR (18 RAISE situations)
# Design source: DESIGN_AGENT_2_SP1_SP2_SP3_SP4.md
# ---------------------------------------------------------------------------

SITUATIONS += [
    (B05, ['Qh', 'Qd'],
     'SP1_01: Set of queens on monotone spade board (6s 4s Qs). SPR=5.89, IP (BTN). '
     'flush_danger=0.90, hand_category=12. S4 boundary at SPR~6 — labeller to confirm RAISE.',
     'SP1'),
    (B05, ['Qh', '6h'],
     'SP1_02: Two pair queens and sixes on monotone spade board. SPR=5.89, IP (BTN). '
     'flush_danger=0.90, hand_category=10. S4 boundary note applies.',
     'SP1'),
    (B05, ['6h', '6d'],
     'SP1_03: Set of sixes on monotone spade board. SPR=5.89, IP (BTN). '
     'flush_danger=0.90, hand_category=12.',
     'SP1'),
    (B11r, ['Th', 'Td'],
     'SP1_04: Set of tens on two-tone spade board (Ts 8s 4h). SPR=5.0, IP (BTN). '
     'flush_danger=0.55, hand_category=12. No suppressors.',
     'SP1'),
    (B11r, ['Th', '8h'],
     'SP1_05: Two pair tens and eights on two-tone spade board. SPR=5.0, IP (BTN). '
     'flush_danger=0.55, hand_category=10.',
     'SP1'),
    (B02, ['Kc', 'Kd'],
     'SP1_06: Set of kings on two-tone heart flop (Kh 7h 3d). SPR=5.0, OOP (BB). '
     'flush_danger=0.45, hand_category=12.',
     'SP1'),
    (B02, ['Kc', '7d'],
     'SP1_07: Two pair kings and sevens on two-tone heart flop. SPR=5.0, OOP (BB). '
     'flush_danger=0.45, hand_category=10.',
     'SP1'),
    (B08, ['Qh', 'Qd'],
     'SP1_08: Set of queens on two-tone club flop (Qc 5c 9h). SPR=5.0, OOP (BB). '
     'flush_danger=0.50, hand_category=12.',
     'SP1'),
    (B12, ['Kh', 'Kd'],
     'SP1_09: Set of kings on three-club turn (7c 2d Kc Ac). SPR=3.0, OOP (BB). '
     'flush_danger=0.75, hand_category=12.',
     'SP1'),
    (B12, ['Kh', '7h'],
     'SP1_10: Two pair kings and sevens on three-club turn. SPR=3.0, OOP (BB). '
     'flush_danger=0.75, hand_category=10.',
     'SP1'),
    (B22, ['Jc', 'Jd'],
     'SP1_11: Set of jacks on two-tone heart turn (Jh 4c 2h Td). SPR=1.4, OOP (BB). '
     'flush_danger=0.55, hand_category=12.',
     'SP1'),
    (B22, ['Jc', '4h'],
     'SP1_12: Two pair jacks and fours on two-tone heart turn. SPR=1.4, OOP (BB). '
     'flush_danger=0.55, hand_category=10.',
     'SP1'),
    (B16, ['Kh', 'Kc'],
     'SP1_13: Set of kings on two-tone heart turn (5h Kd 2h 8c). SPR=4.0, IP (BTN). '
     'flush_danger=0.45, hand_category=12.',
     'SP1'),
    (B16, ['Kh', '8d'],
     'SP1_14: Two pair kings and eights on two-tone heart turn. SPR=4.0, IP (BTN). '
     'flush_danger=0.45, hand_category=10.',
     'SP1'),
    (B20, ['Qc', 'Qd'],
     'SP1_15: Set of queens on two-tone club turn (2c 9c Qh 6s). SPR=1.4, IP (CO). '
     'flush_danger=0.50, hand_category=12. SP1 context — no S5 suppressor here.',
     'SP1'),
    (B20, ['Qd', '9h'],
     'SP1_16: Two pair queens and nines on two-tone club turn. SPR=1.4, IP (CO). '
     'flush_danger=0.50, hand_category=10.',
     'SP1'),
    (B01, ['Th', 'Td'],
     'SP1_17: Set of tens on two-tone club flop (2c Tc 6d). SPR=5.0, IP (BTN). '
     'flush_danger=0.40, hand_category=12.',
     'SP1'),
    (B08, ['Qh', '5d'],
     'SP1_18: Two pair queens and fives on two-tone club flop (Qc 5c 9h). SPR=5.0, OOP (BB). '
     'flush_danger=0.50, hand_category=10.',
     'SP1'),
]

# ---------------------------------------------------------------------------
# SP2: Monster + dry board + low SPR commit (10 RAISE situations)
# B10_LOW and B17_LOW override effective_stack to achieve SPR=1.5.
# ---------------------------------------------------------------------------

SITUATIONS += [
    (B10_LOW, ['Kh', 'Kd'],
     'SP2_01: Set of kings on dry rainbow flop (Kc 4d 2h). SPR=1.5 (eff_stack=135), OOP (BB) leads. '
     'hand_category=12, flush_danger=0, range_pct=0.95. Step 3 fires.',
     'SP2'),
    (B10_LOW, ['Kh', '4h'],
     'SP2_02: Two pair kings and fours on dry rainbow flop. SPR=1.5, OOP (BB) leads. '
     'hand_category=10, flush_danger=0, range_pct=0.91. Step 3 fires.',
     'SP2'),
    (B17_LOW, ['Ah', 'Ac'],
     'SP2_03: Set of aces on dry rainbow ace-high turn (Ad 7s 3c 2h). SPR=1.5 (eff_stack=270), '
     'OOP (SB) leads. hand_category=12, flush_danger=0, range_pct=0.97. Step 3 fires.',
     'SP2'),
    (B17_LOW, ['Ah', '7h'],
     'SP2_04: Two pair aces and sevens on dry rainbow ace-high turn. SPR=1.5, OOP (SB) leads. '
     'hand_category=10, flush_danger=0, range_pct=0.92. Step 3 fires.',
     'SP2'),
    (B30, ['5h', '5d'],
     'SP2_05: Set of fives on very dry rainbow flop (5c 3d 2s). SPR=1.0, IP (BTN). '
     'hand_category=12, flush_danger=0, range_pct=0.98. Step 3 fires.',
     'SP2'),
    (B30, ['5h', '3h'],
     'SP2_06: Two pair fives and threes on very dry rainbow flop. SPR=1.0, IP (BTN). '
     'hand_category=10, flush_danger=0, range_pct=0.93. Step 3 fires.',
     'SP2'),
    (B31, ['Kh', 'Kd'],
     'SP2_07: Set of kings on dry rainbow turn (7d 2c Ks 4h). SPR=1.4, IP (CO). '
     'hand_category=12, flush_danger=0, range_pct=0.96. Step 3 fires.',
     'SP2'),
    (B31, ['Kh', '7h'],
     'SP2_08: Two pair kings and sevens on dry rainbow turn. SPR=1.4, IP (CO). '
     'hand_category=10, flush_danger=0, range_pct=0.90. Step 3 fires.',
     'SP2'),
    (B20, ['Qc', 'Qd'],
     'SP2_09: Set of queens on club turn (2c 9c Qh 6s). SPR=1.4, IP (CO). '
     'flush_danger=0.0 (VERIFIED). hand_category=12, range_pct=0.98. Step 3 fires.',
     'SP2'),
    (B20, ['Qd', '9h'],
     'SP2_10: Two pair queens and nines on club turn. SPR=1.4, IP (CO). '
     'flush_danger=0.0 (VERIFIED). hand_category=10, range_pct=0.94. Step 3 fires.',
     'SP2'),
]

# ---------------------------------------------------------------------------
# SP3: Monster + OOP check-raise (12 RAISE situations)
# Note SP3_10 (B17): to_call=0 — hero leads, not check-raises. See design flag.
# ---------------------------------------------------------------------------

SITUATIONS += [
    (B02, ['Kc', 'Kd'],
     'SP3_01: Set of kings OOP check-raise on two-tone heart flop (Kh 7h 3d). SPR=5.0, BB. '
     'hand_category=12, range_pct=0.95, is_ip=0. No suppressors.',
     'SP3'),
    (B02, ['Kc', '7d'],
     'SP3_02: Two pair kings and sevens OOP check-raise on two-tone heart flop. SPR=5.0, BB. '
     'hand_category=10, range_pct=0.92, is_ip=0.',
     'SP3'),
    (B06, ['8d', '3h'],
     'SP3_03: Full house eights full of threes OOP on paired rainbow flop (8c 8h 3d). SPR=5.5, BB. '
     'hand_category=14, range_pct=0.97, is_ip=0.',
     'SP3'),
    (B06, ['8s', '3c'],
     'SP3_04: Full house eights full of threes — alt suits — on paired flop. SPR=5.5, BB. '
     'hand_category=14, range_pct=0.99, is_ip=0.',
     'SP3'),
    (B08, ['Qh', 'Qd'],
     'SP3_05: Set of queens OOP check-raise on two-tone club flop (Qc 5c 9h). SPR=5.0, BB. '
     'hand_category=12, range_pct=0.93, is_ip=0.',
     'SP3'),
    (B13, ['Qh', 'Qc'],
     'SP3_06: Set of queens OOP check-raise on rainbow turn (Qd 6h 2s Jc). SPR=8.4, SB. '
     'hand_category=12, range_pct=0.91, is_ip=0. S4 does not fire (hero is OOP).',
     'SP3'),
    (B12, ['Kh', 'Kd'],
     'SP3_07: Set of kings OOP check-raise on flush-danger turn (7c 2d Kc Ac). SPR=3.0, BB. '
     'hand_category=12, range_pct=0.96, is_ip=0.',
     'SP3'),
    (B13, ['Qh', 'Jh'],
     'SP3_08: Two pair queens and jacks OOP on rainbow turn (Qd 6h 2s Jc). SPR=8.4, SB. '
     'hand_category=10, range_pct=0.94, is_ip=0.',
     'SP3'),
    (B15, ['Th', '9c'],
     'SP3_09: Full house nines full of tens OOP on paired turn (Tc 3d 9h 9s). SPR=2.6, BB. '
     'hand_category=14, range_pct=0.98, is_ip=0.',
     'SP3'),
    (B17, ['Ah', 'Ac'],
     'SP3_10: Set of aces OOP leading on dry rainbow turn (Ad 7s 3c 2h). SPR=3.0, SB. '
     'to_call=0 — hero leads for value (not check-raise). hand_category=12, range_pct=0.90, is_ip=0. '
     'DESIGN FLAG: to_call=0 — confirm this leading action qualifies as SP3 Step 2 value raise.',
     'SP3'),
    (B21, ['3c', 'Kh'],
     'SP3_11: Full house threes full of kings OOP on paired turn (3h 3d 9s Kc). SPR=3.0, SB. '
     'hand_category=14, range_pct=0.95, is_ip=0.',
     'SP3'),
    (B21, ['9h', '9d'],
     'SP3_12: Full house nines full of threes OOP on paired turn (3h 3d 9s Kc). SPR=3.0, SB. '
     'hand_category=14, range_pct=0.99, is_ip=0.',
     'SP3'),
]

# ---------------------------------------------------------------------------
# SP4: Monster suppressors — CALL (6 situations)
# Each fires exactly one suppressor to produce CALL despite is_monster=1.
# ---------------------------------------------------------------------------

SITUATIONS += [
    (B33, ['7c', '7d'],
     'SP4_01: Set of sevens on paired two-tone flop (Qh Qd 7h). is_monster=1, hand_category=12. '
     'Suppressor S2 fires: flush_danger=0.65 >= 0.60 AND is_paired=1. CALL.',
     'SP4'),
    (B33, ['Qc', '7c'],
     'SP4_02: Full house queens full of sevens on paired two-tone flop (Qh Qd 7h). '
     'is_monster=1, hand_category=14. Suppressor S2 fires: flush_danger=0.65 AND is_paired=1. CALL.',
     'SP4'),
    (B12, ['Kh', 'Kd'],
     'SP4_03: Set of kings on flush-danger turn (7c 2d Kc Ac). is_monster=1, hand_category=12. '
     'Suppressor S3 fires: villain_aggression_count=2 (bet flop, bet turn). CALL.',
     'SP4'),
    (B26, ['Ah', 'Th'],
     'SP4_04: Ace-high flush on heart-completed river (Kh 5c 2h 9d Qh). is_monster=1, '
     'hand_category=13 (flush). Suppressor S3 fires: villain (CO) aggression_count=2. CALL.',
     'SP4'),
    (B09, ['As', 'Ac'],
     'SP4_05: Set of aces on two-tone heart flop (Ah 4h 8c). is_monster=1, hand_category=12. '
     'Suppressor S4 fires: spr=8.0 >= 6.0 AND is_ip=1 (hero=CO). CALL.',
     'SP4'),
    (B20, ['Qc', 'Qd'],
     'SP4_06: Set of queens on two-tone club turn (2c 9c Qh 6s). is_monster=1, hand_category=12. '
     'Suppressor S5 fires: num_callers_to_bet=1 (SB called BB flop bet) AND range_pct=0.88 < 0.92. CALL.',
     'SP4'),
]

# ---------------------------------------------------------------------------
# SP5: Semi-bluff raises (28 RAISE situations)
# Design source: DESIGN_AGENT_1_SP5_SP6.md
# All require: draw_outs >= 9, flush_draw_rank >= 12, flush_block_pct > 0,
# villain_fold_equity >= 0.45, villain_aggression_count <= 1, is_paired == 0.
# ---------------------------------------------------------------------------

SITUATIONS += [
    # B01 sits
    (B01, ['Ac', 'Kd'],
     'SP5_01: Nut club FD (Ac) + Kd overcard, IP BTN. flush_draw_rank=14, block=0.20, '
     'fold_eq=0.55, aggr=0. draw_outs=9.',
     'SP5'),
    (B01, ['Ac', 'Qh'],
     'SP5_02: Nut club FD (Ac) + Qh overcard, IP BTN. flush_draw_rank=14, block=0.25, '
     'fold_eq=0.65, aggr=1. draw_outs=9.',
     'SP5'),
    (B01, ['Kc', 'Jh'],
     'SP5_03: K-high club FD (Kc) + Jh overcard, IP BTN. flush_draw_rank=13, block=0.15, '
     'fold_eq=0.50, aggr=0. draw_outs=9.',
     'SP5'),
    # B04 sits
    (B04, ['Ad', 'Th'],
     'SP5_04: Nut diamond FD (Ad) + Th straight draw, OOP SB. flush_draw_rank=14, block=0.20, '
     'fold_eq=0.48, aggr=0. draw_outs>=9.',
     'SP5'),
    (B04, ['Kd', '8h'],
     'SP5_05: K-high diamond FD (Kd) + 8h connector, OOP SB. flush_draw_rank=13, block=0.15, '
     'fold_eq=0.60, aggr=1. draw_outs=9.',
     'SP5'),
    (B04, ['Qd', '7c'],
     'SP5_06: Q-high diamond FD (Qd), rank=12 boundary, OOP SB. flush_draw_rank=12, block=0.10, '
     'fold_eq=0.50, aggr=0. draw_outs=9.',
     'SP5'),
    # B08 sits
    (B08, ['Ac', 'Jh'],
     'SP5_07: Nut club FD (Ac) + Jh overcard, OOP BB. flush_draw_rank=14, block=0.25, '
     'fold_eq=0.58, aggr=0. Qc on board — Ac is highest available.',
     'SP5'),
    (B08, ['Kc', 'Th'],
     'SP5_08: K-high club FD (Kc) + Th connector, OOP BB. flush_draw_rank=13, block=0.18, '
     'fold_eq=0.47, aggr=1. draw_outs=9.',
     'SP5'),
    (B08, ['Ac', '8d'],
     'SP5_09: Nut club FD (Ac) + 8d connector variant, OOP BB. flush_draw_rank=14, block=0.12, '
     'fold_eq=0.55, aggr=0. Differentiated from SP5_07 by second card.',
     'SP5'),
    # B11r sits
    (B11r, ['As', 'Kh'],
     'SP5_10: Nut spade FD (As) + Kh overcard, IP BTN. flush_draw_rank=14, block=0.22, '
     'fold_eq=0.62, aggr=0. draw_outs=9.',
     'SP5'),
    (B11r, ['Ks', 'Jd'],
     'SP5_11: K-high spade FD (Ks) + Jd overcard, IP BTN. flush_draw_rank=13, block=0.16, '
     'fold_eq=0.50, aggr=1. draw_outs=9.',
     'SP5'),
    # B09 sits (Ah on board — highest available heart draw is Kh)
    (B09, ['Kh', 'Jd'],
     'SP5_12: K-high heart FD (Kh, Ah on board) + Jd overcard, IP CO. flush_draw_rank=13, '
     'block=0.20, fold_eq=0.68, aggr=0. draw_outs=9.',
     'SP5'),
    (B09, ['Kh', 'Qd'],
     'SP5_13: K-high heart FD (Kh) + Qd overcard, IP CO. flush_draw_rank=13, block=0.15, '
     'fold_eq=0.52, aggr=0. draw_outs=9.',
     'SP5'),
    # B14 sits
    (B14, ['As', 'Kd'],
     'SP5_14: Nut spade FD (As) + Kd overcard, IP CO. flush_draw_rank=14, block=0.20, '
     'fold_eq=0.58, aggr=0. draw_outs=9. Turn board.',
     'SP5'),
    (B14, ['Ks', 'Qh'],
     'SP5_15: K-high spade FD (Ks) + Qh overcard, IP CO. flush_draw_rank=13, block=0.15, '
     'fold_eq=0.46, aggr=1. Boundary fold_eq above 0.45 gate.',
     'SP5'),
    (B14, ['Qs', 'Ah'],
     'SP5_16: Q-high spade FD (Qs) + Ah overcard, IP CO. flush_draw_rank=12, block=0.10, '
     'fold_eq=0.55, aggr=0. draw_outs=9.',
     'SP5'),
    # B18 sits
    (B18, ['Ad', 'Jc'],
     'SP5_17: Nut diamond FD (Ad) + Jc overcard, OOP BB. flush_draw_rank=14, block=0.20, '
     'fold_eq=0.60, aggr=0. draw_outs=9. Turn board.',
     'SP5'),
    (B18, ['Kd', 'Qc'],
     'SP5_18: K-high diamond FD (Kd) + Qc overcard, OOP BB. flush_draw_rank=13, block=0.18, '
     'fold_eq=0.48, aggr=1. Kh on board — Kd is free.',
     'SP5'),
    (B18, ['Qd', 'Ac'],
     'SP5_19: Q-high diamond FD (Qd) + Ac overcard, OOP BB. flush_draw_rank=12, block=0.12, '
     'fold_eq=0.70, aggr=0. High fold_eq compensates minimum rank.',
     'SP5'),
    # B22 sits
    (B22, ['Ah', 'Kc'],
     'SP5_20: Nut heart FD (Ah) + Kc, OOP BB. flush_draw_rank=14, block=0.25, fold_eq=0.52, '
     'aggr=0. SPR=1.4 low. draw_outs=9.',
     'SP5'),
    (B22, ['Kh', 'Qc'],
     'SP5_21: K-high heart FD (Kh) + Qc, OOP BB. flush_draw_rank=13, block=0.20, fold_eq=0.45, '
     'aggr=1. fold_eq exactly at gate boundary.',
     'SP5'),
    # B16 sits
    (B16, ['Ah', 'Jd'],
     'SP5_22: Nut heart FD (Ah) + Jd overcard, IP BTN. flush_draw_rank=14, block=0.22, '
     'fold_eq=0.65, aggr=0. draw_outs>=9. Turn board.',
     'SP5'),
    (B16, ['Qh', 'Jc'],
     'SP5_23: Q-high heart FD (Qh) + Jc, IP BTN. flush_draw_rank=12, block=0.12, fold_eq=0.50, '
     'aggr=1. draw_outs=9. Turn board.',
     'SP5'),
    # B05 sits (monotone — hero needs exactly one spade of rank 12+)
    (B05, ['As', '7d'],
     'SP5_24: Monotone spades — As draw (rank=14) + 7d, IP BTN. block=0.30 (As on monotone), '
     'fold_eq=0.58, aggr=0. draw_outs=9.',
     'SP5'),
    (B05, ['Ks', '9d'],
     'SP5_25: Monotone spades — Ks draw (rank=13) + 9d, IP BTN. block=0.25, fold_eq=0.50, '
     'aggr=1. draw_outs=9.',
     'SP5'),
    # B01 additional sits
    (B01, ['Qc', 'Jd'],
     'SP5_26: Q-high club FD (Qc) + Jd, IP BTN. flush_draw_rank=12 boundary, block=0.10, '
     'fold_eq=0.46, aggr=0. draw_outs=9.',
     'SP5'),
    # B04 additional sit
    (B04, ['Ad', 'Kh'],
     'SP5_27: Nut diamond FD (Ad) + Kh, OOP SB. flush_draw_rank=14, block=0.35 (max), '
     'fold_eq=0.55, aggr=0. draw_outs=9.',
     'SP5'),
    # B11r additional sit
    (B11r, ['Qs', 'Jh'],
     'SP5_28: Q-high spade FD (Qs) + Jh, IP BTN. flush_draw_rank=12 boundary, block=0.08 (low), '
     'fold_eq=0.68, aggr=0. draw_outs=9.',
     'SP5'),
]

# ---------------------------------------------------------------------------
# SP6: Semi-bluff suppressed — CALL (13 situations)
# Each fails at least one SP5 gate. Primary failure mode in description.
# ---------------------------------------------------------------------------

SITUATIONS += [
    # Failure Mode 1: fold_equity < 0.45
    (B04, ['Ad', '7s'],
     'SP6_01: Nut diamond FD (Ad) + 7s, OOP SB. FAILS fold_eq=0.35 < 0.45 gate. '
     'All other SP5 conditions met. CALL.',
     'SP6'),
    (B08, ['Ac', '7d'],
     'SP6_02: Nut club FD (Ac) + 7d, OOP BB. FAILS fold_eq=0.38 < 0.45 gate. '
     'Qc on board — Ac is nut available club. CALL.',
     'SP6'),
    (B01, ['Kc', '8d'],
     'SP6_03: K-high club FD (Kc), IP BTN. FAILS fold_eq=0.40 < 0.45 gate. '
     'draw_outs=9, aggr=0, is_paired=0. CALL.',
     'SP6'),
    # Failure Mode 2: villain_aggression_count >= 2
    (B22, ['Ah', '9c'],
     'SP6_04: Nut heart FD (Ah) + 9c, OOP BB. FAILS villain_aggression_count=2 '
     '(villain bet flop AND turn). All other SP5 conditions would pass. CALL.',
     'SP6'),
    (B18, ['Ad', '7c'],
     'SP6_05: Nut diamond FD (Ad) + 7c, OOP BB. FAILS villain_aggression_count=2 '
     '(villain bet flop AND turn). CALL.',
     'SP6'),
    # Failure Mode 3: is_paired == 1
    (B06, ['Ac', 'Kd'],
     'SP6_06: Ac Kd on paired board (8c 8h 3d). FAILS is_paired=1 suppressor. '
     'No flush draw (rainbow board). CALL.',
     'SP6'),
    (B15, ['Kc', 'Qd'],
     'SP6_07: Kc Qd on paired turn (Tc 3d 9h 9s). FAILS is_paired=1 suppressor. '
     'No flush draw (rainbow board). Overcards only. CALL.',
     'SP6'),
    # Failure Mode 4: draw_outs < 9
    (B04, ['Qh', 'Tc'],
     'SP6_08: Qh Tc on J-9-4 board. Gutshot only (4 outs). FAILS draw_outs < 9 gate. '
     'No flush draw in diamonds. CALL.',
     'SP6'),
    (B14, ['Ks', '7h'],
     'SP6_09: K-high spade draw (Ks) + 7h, IP CO. draw_outs=6 (dirty outs on turn board). '
     'FAILS draw_outs < 9 gate. CALL.',
     'SP6'),
    # Failure Mode 5: flush_draw_rank < 12
    (B11r, ['9s', '7d'],
     'SP6_10: 9s 7d on spade board (Ts 8s 4h). flush_draw_rank=9 (Ts on board — 9s is highest '
     'available below 12). FAILS flush_draw_rank < 12 gate. CALL.',
     'SP6'),
    (B14, ['Ts', '6c'],
     'SP6_11: Ts 6c on spade turn (3s Js 9h 4d). flush_draw_rank=10 (Ts, Js on board — Ts hero rank=10). '
     'FAILS flush_draw_rank < 12 gate. CALL.',
     'SP6'),
    # Failure Mode 6: flush_block_pct == 0 (reassigned — see design agent notes)
    (B14, ['As', 'Qh'],
     'SP6_12: Nut spade draw (As rank=14) + Qh, IP CO. FAILS fold_eq=0.38 < 0.45 gate. '
     'Originally designed as block=0 failure mode; reassigned — see FLUSH_BLOCK_FINDING. CALL.',
     'SP6'),
    (B04, ['8s', '7d'],
     'SP6_13: 8s 7d on diamond board (Jd 9d 4s). No nut diamond draw (no diamond in hand). '
     'flush_block_pct=0 (no diamonds). FAILS flush_draw_rank < 12 AND flush_block_pct=0. CALL.',
     'SP6'),
]

# ---------------------------------------------------------------------------
# SP7: OOP thin value check-raise (25 RAISE situations)
# Design source: DESIGN_AGENT_3_SP7_SP10.md
# All: range_pct 0.75-0.92, is_monster=0, is_ip=0, fold_eq >= 0.40,
# aggr <= 1, flush_danger <= 0.35, straight_danger <= 0.35.
# Note SP7_05 (B17): to_call=0 — hero leads. See design notes.
# ---------------------------------------------------------------------------

SITUATIONS += [
    (B02, ['Kd', 'Qs'],
     'SP7_01: KdQs on Kh-7h-3d. Top pair top kicker (8), OOP BB. range_pct=0.76, fold_eq=0.42, '
     'aggr=0, flush_d=0.30. Band 0.75-0.80.',
     'SP7'),
    (B06, ['Ac', 'Ad'],
     'SP7_02: AcAd on 8c-8h-3d paired rainbow. Overpair (9), OOP BB. range_pct=0.78, fold_eq=0.45, '
     'aggr=1, flush_d=0.10. Band 0.75-0.80.',
     'SP7'),
    (B06, ['Kd', 'Ks'],
     'SP7_03: KdKs on 8c-8h-3d paired rainbow. Overpair (9), OOP BB. range_pct=0.78, fold_eq=0.43, '
     'aggr=0, flush_d=0.10. Band 0.75-0.80.',
     'SP7'),
    (B13, ['Qh', 'Ts'],
     'SP7_04: QhTs on Qd-6h-2s-Jc rainbow turn. Top pair good kicker (7), OOP SB. '
     'range_pct=0.75, fold_eq=0.55, aggr=1, flush_d=0.05. Band 0.75-0.80.',
     'SP7'),
    (B17, ['As', 'Jd'],
     'SP7_05: AsJd on Ad-7s-3c-2h dry rainbow turn. Top pair top kicker (8), OOP SB. '
     'to_call=0 — hero leads. range_pct=0.78, fold_eq=0.48, aggr=0, flush_d=0.05. Band 0.75-0.80.',
     'SP7'),
    (B21, ['Kh', 'Qs'],
     'SP7_06: KhQs on 3h-3d-9s-Kc paired turn. Top pair good kicker (7), OOP SB. '
     'range_pct=0.77, fold_eq=0.43, aggr=1, flush_d=0.10. Band 0.75-0.80.',
     'SP7'),
    (B02, ['Kc', 'Qd'],
     'SP7_07: KcQd on Kh-7h-3d. Top pair top kicker (8), OOP BB. range_pct=0.82, fold_eq=0.52, '
     'aggr=0, flush_d=0.30. Band 0.80-0.86.',
     'SP7'),
    (B08, ['Qd', 'Jh'],
     'SP7_08: QdJh on Qc-5c-9h two-tone clubs. Top pair good kicker (7), OOP BB. '
     'range_pct=0.83, fold_eq=0.58, aggr=1, flush_d=0.30. Band 0.80-0.86.',
     'SP7'),
    (B08, ['Qs', 'Td'],
     'SP7_09: QsTd on Qc-5c-9h two-tone clubs. Top pair good kicker (7), OOP BB. '
     'range_pct=0.82, fold_eq=0.50, aggr=1, flush_d=0.30. Band 0.80-0.86.',
     'SP7'),
    (B13, ['Qc', 'Ts'],
     'SP7_10: QcTs on Qd-6h-2s-Jc rainbow turn. Top pair good kicker (7), OOP SB. '
     'range_pct=0.84, fold_eq=0.45, aggr=0, flush_d=0.05. Band 0.80-0.86.',
     'SP7'),
    (B17, ['Ah', 'Qc'],
     'SP7_11: AhQc on Ad-7s-3c-2h rainbow turn. Top pair top kicker (8), OOP SB. '
     'to_call=0 — hero leads. range_pct=0.81, fold_eq=0.63, aggr=1, flush_d=0.05. Band 0.80-0.86.',
     'SP7'),
    (B21, ['Kd', 'Jc'],
     'SP7_12: KdJc on 3h-3d-9s-Kc paired turn. Top pair good kicker (7), OOP SB. '
     'range_pct=0.83, fold_eq=0.40 (lower bound), aggr=0, flush_d=0.10. Band 0.80-0.86.',
     'SP7'),
    (B15, ['Td', 'Ks'],
     'SP7_13: TdKs on Tc-3d-9h-9s paired turn. Top pair good kicker (7 — T top pair, K kicker), '
     'OOP BB. range_pct=0.84, fold_eq=0.55, aggr=1, flush_d=0.15. Band 0.80-0.86.',
     'SP7'),
    (B02, ['Ks', 'Ad'],
     'SP7_14: KsAd on Kh-7h-3d. Top pair top kicker (8 — AK on K-high), OOP BB. '
     'range_pct=0.88, fold_eq=0.65, aggr=0, flush_d=0.30. Band 0.86-0.92.',
     'SP7'),
    (B06, ['Qs', 'Qd'],
     'SP7_15: QsQd on 8c-8h-3d paired rainbow. Overpair (9), OOP BB. '
     'range_pct=0.87, fold_eq=0.60, aggr=1, flush_d=0.10. Band 0.86-0.92.',
     'SP7'),
    (B08, ['Qh', 'Ks'],
     'SP7_16: QhKs on Qc-5c-9h two-tone clubs. Top pair top kicker (8 — KQ), OOP BB. '
     'range_pct=0.90, fold_eq=0.55, aggr=0, flush_d=0.30. Band 0.86-0.92.',
     'SP7'),
    (B13, ['Qh', 'Ac'],
     'SP7_17: QhAc on Qd-6h-2s-Jc rainbow turn. Top pair top kicker (8 — AQ), OOP SB. '
     'range_pct=0.89, fold_eq=0.42, aggr=1, flush_d=0.05. Band 0.86-0.92.',
     'SP7'),
    (B17, ['Ac', 'Ks'],
     'SP7_18: AcKs on Ad-7s-3c-2h rainbow turn. Top pair top kicker (8 — AK), OOP SB. '
     'to_call=0 — hero leads. range_pct=0.88, fold_eq=0.65, aggr=0, flush_d=0.05. Band 0.86-0.92.',
     'SP7'),
    (B21, ['Ks', 'Qh'],
     'SP7_19: KsQh on 3h-3d-9s-Kc paired turn. Top pair top kicker (8), OOP SB. '
     'range_pct=0.91, fold_eq=0.50, aggr=1, flush_d=0.10. Band 0.86-0.92.',
     'SP7'),
    (B15, ['Th', 'As'],
     'SP7_20: ThAs on Tc-3d-9h-9s paired turn. Top pair top kicker (8 — T top pair, A kicker), '
     'OOP BB. range_pct=0.86, fold_eq=0.62, aggr=0, flush_d=0.15. Band 0.86-0.92.',
     'SP7'),
    (B02, ['Kd', 'Jc'],
     'SP7_21: KdJc on Kh-7h-3d. Top pair good kicker (7), OOP BB. range_pct=0.89, fold_eq=0.55, '
     'aggr=0, flush_d=0.30. Band 0.86-0.92. Fourth B02 sit — at per-board cap.',
     'SP7'),
    (B12, ['Ah', 'Jd'],
     'SP7_22: AhJd on 7c-2d-Kc-Ac three-club turn. Top pair good kicker (7 — A top pair), '
     'OOP BB. range_pct=0.76, fold_eq=0.55, aggr=0, flush_d=0.35. Band 0.75-0.80.',
     'SP7'),
    (B18, ['Ks', 'Qc'],
     'SP7_23: KsQc on 4d-8d-Kh-5c two-tone diamond turn. Top pair top kicker (8 — KQ), '
     'OOP BB. range_pct=0.79, fold_eq=0.60, aggr=1, flush_d=0.30. Band 0.75-0.80.',
     'SP7'),
    (B12, ['As', 'Qd'],
     'SP7_24: AsQd on 7c-2d-Kc-Ac three-club turn. Top pair top kicker (8 — AQ), '
     'OOP BB. range_pct=0.83, fold_eq=0.42, aggr=0, flush_d=0.35. Band 0.80-0.86.',
     'SP7'),
    (B18, ['Kc', 'As'],
     'SP7_25: KcAs on 4d-8d-Kh-5c two-tone diamond turn. Top pair top kicker (8 — AK), '
     'OOP BB. range_pct=0.90, fold_eq=0.65, aggr=0, flush_d=0.30. Band 0.86-0.92.',
     'SP7'),
]

# ---------------------------------------------------------------------------
# SP8: Bottom of range bluff raise — river only (16 RAISE situations)
# Design source: DESIGN_AGENT_4_SP8_SP9.md
# All: street=river, range_pct <= 0.20, fold_eq >= 0.50,
# villain_top_pair_plus_pct <= 0.35, num_callers=0, aggr=0.
# ---------------------------------------------------------------------------

SITUATIONS += [
    (B23, ['9c', '8d'],
     'SP8_01: Bricked straight draw (9-8 offsuit) on K-7-2-5-J rainbow river. '
     'range_pct=0.04, fold_eq=0.55, top_pair_pct=0.25, aggr=0.',
     'SP8'),
    (B23, ['Ac', '3c'],
     'SP8_02: Pure air (A-3 two clubs, no pair no draw) on K-7-2-5-J river. '
     'range_pct=0.15, fold_eq=0.60, top_pair_pct=0.30, aggr=0.',
     'SP8'),
    (B23, ['6h', '9h'],
     'SP8_03: Bricked heart flush draw (6h 9h, board has 5h Jh = 2 hearts) on K-7-2-5-J river. '
     'range_pct=0.08, fold_eq=0.65, top_pair_pct=0.20, aggr=0.',
     'SP8'),
    (B24, ['As', 'Js'],
     'SP8_04: Bricked spade flush draw (As Js, board has 9s Ks = 2 spades) on K-9-4-2-7 river. '
     'range_pct=0.05, fold_eq=0.52, top_pair_pct=0.15, aggr=0. OOP SB.',
     'SP8'),
    (B24, ['Qd', 'Th'],
     'SP8_05: Pure air (Q-T offsuit, no pair) on 9s-4h-Ks-2d-7c river. '
     'range_pct=0.18, fold_eq=0.58, top_pair_pct=0.28, aggr=0. OOP SB.',
     'SP8'),
    (B24, ['5c', '6h'],
     'SP8_06: Bricked straight draw (5-6 offsuit, missed 3-4-5-6-7) on 9s-4h-Ks-2d-7c river. '
     'range_pct=0.10, fold_eq=0.70, top_pair_pct=0.10, aggr=0. OOP SB.',
     'SP8'),
    (B25, ['Jh', '8d'],
     'SP8_07: Pure air (J-8 offsuit, no pair) on As-6d-2h-Tc-4s river. '
     'range_pct=0.03, fold_eq=0.55, top_pair_pct=0.22, aggr=0. IP CO.',
     'SP8'),
    (B25, ['Ks', '9s'],
     'SP8_08: Bricked spade flush draw (Ks 9s, board has As 4s = 2 spades) on As-6d-2h-Tc-4s river. '
     'range_pct=0.12, fold_eq=0.62, top_pair_pct=0.30, aggr=0. IP CO.',
     'SP8'),
    (B25, ['7c', '8h'],
     'SP8_09: Bricked straight draw (7-8, missed 4-5-6-7-8 or 6-7-8-9-T) on As-6d-2h-Tc-4s river. '
     'range_pct=0.19, fold_eq=0.50, top_pair_pct=0.35, aggr=0. Boundary fold_eq/top_pair_pct.',
     'SP8'),
    (B26, ['Jc', '8d'],
     'SP8_10: Bricked straight draw (J-8 gutshot to 8-9-T-J-Q, needed T) on Kh-5c-2h-9d-Qh river. '
     'Hearts flush completed — hero holds no hearts. range_pct=0.06, fold_eq=0.60, aggr=0. OOP BB.',
     'SP8'),
    (B26, ['7s', '4d'],
     'SP8_11: Pure air (7-4 offsuit, 7-high) on Kh-5c-2h-9d-Qh river. '
     'Hearts flush completed on board; hero pure air. range_pct=0.14, fold_eq=0.72, aggr=0. OOP BB.',
     'SP8'),
    (B27, ['Kd', 'Td'],
     'SP8_12: Bricked diamond flush draw (Kd Td, board has 4d Jd = 2 diamonds) on 4d-8h-2c-6s-Jd river. '
     'range_pct=0.04, fold_eq=0.55, top_pair_pct=0.25, aggr=0. IP BTN.',
     'SP8'),
    (B27, ['Ah', '3s'],
     'SP8_13: Pure air (A-3 offsuit, A-high) on 4d-8h-2c-6s-Jd river. '
     'range_pct=0.16, fold_eq=0.60, top_pair_pct=0.32, aggr=0. IP BTN.',
     'SP8'),
    (B28, ['Qh', '9h'],
     'SP8_14: Dead heart draw / pure air (Qh 9h, only 1 board heart = 7h) on 3s-7h-Ks-2c-Ts river. '
     'Spades flush completed on board. range_pct=0.07, fold_eq=0.65, top_pair_pct=0.20, aggr=0. IP CO.',
     'SP8'),
    (B28, ['Jh', '9c'],
     'SP8_15: Bricked straight draw (J-9, targeted 9-T-J-Q-K needing Q) on 3s-7h-Ks-2c-Ts river. '
     'range_pct=0.13, fold_eq=0.58, top_pair_pct=0.28, aggr=0. IP CO.',
     'SP8'),
    (B29, ['Ah', '5h'],
     'SP8_16: Pure air (A-5 of hearts, A-high, no pair) on Qc-6s-2d-9h-4c river. '
     'range_pct=0.02, fold_eq=0.55, top_pair_pct=0.25, aggr=0. OOP BB.',
     'SP8'),
]

# ---------------------------------------------------------------------------
# SP9: Flat spots — CALL only (10 situations)
# Design source: DESIGN_AGENT_4_SP8_SP9.md
# Each fires Trigger A (board_favour <= -0.30), B (aggr >= 2), or C (callers >= 1).
# ---------------------------------------------------------------------------

SITUATIONS += [
    (B07, ['9c', '9s'],
     'SP9_01: 9c9s overpair on 5h-6c-7d connected rainbow flop. Trigger A: board_favour=-0.45 '
     '(straight board favours BB range). IP BTN. range_pct=0.65, aggr=1. CALL.',
     'SP9'),
    (B07, ['Kh', 'Kd'],
     'SP9_02: KhKd premium overpair on 5h-6c-7d. Trigger A: board_favour=-0.50. '
     'Even KK calls — board tilted toward villain range. IP BTN. range_pct=0.78. CALL.',
     'SP9'),
    (B19, ['Jd', 'Jc'],
     'SP9_03: JdJc overpair on 4c-6h-8s-7d connected turn. Trigger A: board_favour=-0.55. '
     'Board is catastrophic for overpairs (straights, two-pair, sets). IP BTN. CALL.',
     'SP9'),
    (B23, ['Qd', 'Qc'],
     'SP9_04: QdQc overpair on Kd-7c-2s-5h-Jh river. Trigger A: board_favour=-0.35. '
     'K and J on board overcards to QQ; villain BB range heavy. IP BTN. CALL.',
     'SP9'),
    (B12, ['Kh', 'Ts'],
     'SP9_05: KhTs top pair (king-ten) on 7c-2d-Kc-Ac three-club turn. Trigger B: aggr=2 '
     '(CO bet flop, BTN bet turn). OOP BB. range_pct=0.62. CALL.',
     'SP9'),
    (B26, ['Ks', '9s'],
     'SP9_06: Ks9s two pair (kings and nines) on Kh-5c-2h-9d-Qh river. Trigger B: aggr=2 '
     '(CO bet flop and turn). Hearts flush completed — villain range flush-heavy. OOP BB. CALL.',
     'SP9'),
    (B29, ['Qh', '8h'],
     'SP9_07: Qh8h top pair (queen-8) on Qc-6s-2d-9h-4c river. Trigger B: aggr=3 '
     '(HJ bet turn, BTN called, BTN bets river). OOP BB. range_pct=0.60. CALL.',
     'SP9'),
    (B24, ['Kd', 'Jh'],
     'SP9_08: KdJh top pair (king-jack) on 9s-4h-Ks-2d-7c river. Trigger C: num_callers=1 '
     '(CO has called BTN bet; hero faces bet in sandwich). OOP SB. range_pct=0.67. CALL.',
     'SP9'),
    (B25, ['Ad', 'Th'],
     'SP9_09: AdTh two pair (aces and tens) on As-6d-2h-Tc-4s river. Trigger C: num_callers=1. '
     'Even two pair does not raise in bet-and-call spot. IP CO. range_pct=0.74. CALL.',
     'SP9'),
    (B17, ['Ah', '6c'],
     'SP9_10: Ah6c top pair weak kicker (ace-six) on Ad-7s-3c-2h turn. Trigger A: board_favour=-0.32 '
     '(BTN uncapped range). to_call=0 — hero leads. OOP SB. range_pct=0.63. CALL.',
     'SP9'),
]

# ---------------------------------------------------------------------------
# SP10: Middle range CALL fill (13 situations)
# Design source: DESIGN_AGENT_3_SP7_SP10.md
# range_pct 0.40-0.80, draw_outs 0-8, pure CALL.
# ---------------------------------------------------------------------------

SITUATIONS += [
    (B07, ['6h', 'Kd'],
     'SP10_01: 6hKd middle pair (sixes) on 5h-6c-7d connected rainbow flop. IP BTN. '
     'range_pct=0.45, draw_outs=0. Step 4 fails (is_ip=1). Band 0.40-0.55. CALL.',
     'SP10'),
    (B10, ['Jc', '4s'],
     'SP10_02: Jc4s middle pair (fours) on Kc-4d-2h rainbow flop. OOP BB. to_call=0. '
     'range_pct=0.50, draw_outs=4 (gutshot). Band 0.40-0.55. CALL.',
     'SP10'),
    (B13, ['6d', '8c'],
     'SP10_03: 6d8c bottom pair (sixes) on Qd-6h-2s-Jc rainbow turn. OOP SB. '
     'range_pct=0.42, draw_outs=0. Band 0.40-0.55. CALL.',
     'SP10'),
    (B19, ['8h', 'Jd'],
     'SP10_04: 8hJd top pair (eights) on 4c-6h-8s-7d connected turn. IP BTN. '
     'range_pct=0.58, draw_outs=5. Band 0.55-0.65. CALL.',
     'SP10'),
    (B20, ['9h', 'Ts'],
     'SP10_05: 9hTs middle pair (nines) on 2c-9c-Qh-6s two-tone club turn. IP CO. '
     'range_pct=0.60, draw_outs=4. Club draw on board; hero holds no clubs. Band 0.55-0.65. CALL.',
     'SP10'),
    (B14, ['Jd', 'Th'],
     'SP10_06: JdTh top pair good kicker (jacks, ten kicker) on 3s-Js-9h-4d spade turn. IP CO. '
     'range_pct=0.55, draw_outs=6. Band 0.40-0.55. CALL.',
     'SP10'),
    (B16, ['Ks', 'Tc'],
     'SP10_07: KsTc top pair good kicker (kings, ten kicker) on 5h-Kd-2h-8c heart turn. IP BTN. '
     'range_pct=0.68, draw_outs=7. No hearts in hand. Band 0.65-0.75. CALL.',
     'SP10'),
    (B27, ['8s', 'Kc'],
     'SP10_08: 8sKc middle pair (eights) on 4d-8h-2c-6s-Jd rainbow river. IP BTN. '
     'range_pct=0.62, draw_outs=0. Showdown value only. Band 0.55-0.65. CALL.',
     'SP10'),
    (B28, ['Kd', 'Jh'],
     'SP10_09: KdJh top pair good kicker (kings, jack kicker) on 3s-7h-Ks-2c-Ts spade river. IP CO. '
     'Spades flush completed on board; hero holds no spades. range_pct=0.72, draw_outs=0. '
     'Band 0.65-0.75. CALL.',
     'SP10'),
    (B03, ['Kd', 'Qh'],
     'SP10_10: KdQh two overcards on As-5d-2c rainbow flop. IP CO. range_pct=0.75, draw_outs=6. '
     'Step 4 fails (is_ip=1). IP thin value contrast — CALL not RAISE. Band 0.75-0.80.',
     'SP10'),
    (B11r, ['Jd', '9c'],
     'SP10_11: Jd9c OESD (J-T-9-8, 7 outs) on Ts-8s-4h two-tone spade flop. IP BTN. '
     'range_pct=0.78, draw_outs=7. Step 5 fails (< 9 outs). Band 0.75-0.80. CALL.',
     'SP10'),
    (B21, ['9d', 'Th'],
     'SP10_12: 9dTh middle pair (nines) on 3h-3d-9s-Kc paired two-tone turn. OOP SB. '
     'range_pct=0.70, draw_outs=5. Step 4 fails (range_pct < 0.75). Band 0.65-0.75. CALL.',
     'SP10'),
    (B15, ['Ts', 'Qh'],
     'SP10_13: TsQh top pair good kicker (tens, queen kicker) on Tc-3d-9h-9s paired turn. OOP BB. '
     'range_pct=0.76, draw_outs=6. Step 3 fails (< 0.90), Step 5 fails (< 9 outs). '
     'Band 0.75-0.80. CALL.',
     'SP10'),
]

# =============================================================================
# VALIDATION: verify expected counts per sub-pattern
# =============================================================================

_EXPECTED_COUNTS = {
    'SP1': 18, 'SP2': 10, 'SP3': 12, 'SP4': 6,
    'SP5': 28, 'SP6': 13, 'SP7': 25, 'SP8': 16,
    'SP9': 10, 'SP10': 13,
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
        print("SITUATION COUNT MISMATCHES (must fix before running):")
        for e in errors:
            print(e)
        return False
    print(f"Situation count check PASSED — {len(SITUATIONS)} total situations defined.")
    return True


# =============================================================================
# GENERATION + VALIDATION
# =============================================================================

def generate_all():
    """Build, validate, and collect all 151 situations."""
    all_records = []
    total_generated = 0
    total_validated = 0
    error_log = []  # (sit_id, error_type, detail)

    for idx, (board_base, hero_cards, description, sub_pattern) in enumerate(SITUATIONS):
        # Derive situation_id: SPX_YY (1-indexed within sub-pattern)
        sp_situations = [s for s in SITUATIONS[:idx+1] if s[3] == sub_pattern]
        sit_num = len(sp_situations)
        sit_id = f"{sub_pattern}_{sit_num:02d}"

        total_generated += 1

        # Build SituationSpec — merge board base with hero cards
        spec_kwargs = dict(board_base)
        spec_kwargs['hero_cards'] = hero_cards
        spec = SituationSpec(**spec_kwargs)

        # Attempt build_situation()
        try:
            feat_dict = build_situation(spec)
        except Exception as exc:
            error_log.append((sit_id, 'BUILD_EXCEPTION', str(exc)))
            print(f"  SKIP  {sit_id} {hero_cards}: BUILD_EXCEPTION: {exc}")
            continue

        # Run validate_situation()
        validation_errors = validate_situation(spec, feat_dict)

        # Attach metadata
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
            print(f"  WARN  {sit_id} {hero_cards}: validation errors: {'; '.join(validation_errors)}")
        else:
            feat_dict['has_errors'] = False
            total_validated += 1
            print(f"  OK    {sit_id} {hero_cards}")

        all_records.append(feat_dict)

    return all_records, total_generated, total_validated, error_log


def main():
    print("=" * 60)
    print("FACTORY BATCH 3 — 151-SITUATION RAISE BATCH")
    print("=" * 60)

    # Pre-flight: verify expected situation counts
    if not _check_situation_counts():
        print("\nABORTING — fix count mismatches before running.")
        return False

    print(f"\nGenerating {len(SITUATIONS)} situations...")
    records, total_gen, total_valid, errors = generate_all()

    # Write JSONL — include all records (even those with validation errors)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        for record in records:
            f.write(json.dumps(record) + '\n')

    # Summary report
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
