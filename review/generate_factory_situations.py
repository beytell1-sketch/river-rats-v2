"""
Generate all 151 situations from DESIGN_POSITION_AMP_SWEEPS.md and
DESIGN_CALL_SWEEPS.md through SituationFactory, validate each, and
write valid situations to training-data/factory_situations.jsonl.

Run from any directory:
    python3 /home/rupertbeytell/river-rats-v2/review/generate_factory_situations.py
"""

import sys
import os
import json

sys.path.insert(0, '/home/rupertbeytell/river-rats-v2/river-rats-core')
os.chdir('/home/rupertbeytell/river-rats-v2/river-rats-core')

from situation_factory import SituationSpec, build_situation, validate_situation

OUTPUT_PATH = '/home/rupertbeytell/river-rats-v2/training-data/factory_situations.jsonl'

# =============================================================================
# POSITION AMP (PA) BOARDS — 79 situations
# =============================================================================

# Board 1: Dry A-high Rainbow — Flop, Lead Decision (facing_bet=False)
# BB defends vs CO open + BTN call. Hero first on Ac8d3s.
PA_BOARD_1_BASE = dict(
    board_cards=['Ac', '8d', '3s'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

PA_BOARD_1_HANDS = [
    (['5h', '4h'], 'Air (no pair, no draw)', 0.15),
    (['7s', '6s'], 'Gutshot only', 0.20),
    (['Kh', 'Qh'], 'Two overcards below A', 0.30),
    (['8h', '7h'], 'Middle pair weak kicker', 0.35),
    (['Ah', '4c'], 'Bottom pair + top pair weak', 0.50),
    (['Ah', '9c'], 'Top pair medium kicker', 0.55),
    (['Ah', 'Jd'], 'Top pair strong kicker', 0.60),
    (['Ah', 'Kc'], 'Top pair top kicker', 0.65),
    (['3d', '3c'], 'Bottom set', 0.80),
    (['8c', '8s'], 'Middle set', 0.85),
]

# Board 2: Low Connected Rainbow — Flop, Lead Decision
# SB calls BTN open. BB also in. Flop 9d6c2h.
PA_BOARD_2_BASE = dict(
    board_cards=['9d', '6c', '2h'],
    hero_pos='SB',
    villain_positions=['BTN', 'BB'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'),
        ('preflop', 'SB', 'call'),
        ('preflop', 'BB', 'call'),
    ],
    opener_position='BTN',
    effective_stack=100.0,
)

PA_BOARD_2_HANDS = [
    (['4h', '3h'], 'Air', 0.12),
    (['Ah', '5h'], 'Overcard + backdoor', 0.25),
    (['Kh', 'Qh'], 'Two overcards', 0.32),
    (['7s', '5s'], 'Gutshot', 0.22),
    (['6s', '5s'], 'Bottom pair weak kicker', 0.30),
    (['9c', '7c'], 'Top pair weak kicker', 0.50),
    (['9h', 'Th'], 'Top pair good kicker', 0.55),
    (['Jh', 'Jd'], 'Overpair (JJ)', 0.56),
    (['Qc', 'Qd'], 'Overpair (QQ)', 0.65),
    (['2d', '2c'], 'Bottom set', 0.82),
]

# Board 3: Monotone Wet Board — Flop, Lead Decision
# BB defends vs CO + BTN. Flop Jh8h4h.
PA_BOARD_3_BASE = dict(
    board_cards=['Jh', '8h', '4h'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

PA_BOARD_3_HANDS = [
    (['5c', '3c'], 'Air (no heart)', 0.08),
    (['Kd', 'Qd'], 'Overcards no heart', 0.18),
    (['6h', '5h'], 'Low flush (made)', 0.62),
    (['9d', '8d'], 'Middle pair no heart', 0.22),
    (['Jd', 'Tc'], 'Top pair no heart', 0.35),
    (['Ah', '3c'], 'Nut flush draw only', 0.40),
    (['Jc', 'Jd'], 'Set no heart', 0.55),
    (['Kh', '9h'], 'King-high flush', 0.78),
    (['Ah', 'Qh'], 'Nut flush', 0.88),
    (['Th', '9h'], 'Flush + OESD backup', 0.72),
]

# Board 4: Paired Dry Board — Flop, Lead Decision
# BB defends vs CO + BTN. Flop QcQd7s.
PA_BOARD_4_BASE = dict(
    board_cards=['Qc', 'Qd', '7s'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

PA_BOARD_4_HANDS = [
    (['5h', '4h'], 'Air', 0.15),
    (['Ah', '3h'], 'A-high', 0.30),
    (['8s', '8h'], 'Underpair (88)', 0.35),
    (['Ts', 'Td'], 'Underpair (TT)', 0.38),
    (['7h', '6h'], 'Middle pair (pair of 7s)', 0.42),
    (['Kh', 'Kd'], 'Overpair (KK)', 0.55),
    (['Ah', 'Ad'], 'Overpair (AA)', 0.60),
    (['Qh', '9c'], 'Trips medium kicker', 0.78),
    (['Qh', 'Jh'], 'Trips good kicker', 0.82),
    (['7d', '7c'], 'Full house (7s full)', 0.95),
]

# Board 5: Connected Wet Board — Turn, Lead Decision
# BB calls through flop. Turn 7h checks through to hero OOP.
PA_BOARD_5_BASE = dict(
    board_cards=['Ts', '9d', '5c', '7h'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=160.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BTN', 'call'),
        ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'),
        ('turn', 'CO', 'check'),
        ('turn', 'BTN', 'check'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

PA_BOARD_5_HANDS = [
    (['Ah', '2h'], 'Air (A-high)', 0.15),
    (['Kc', 'Qc'], 'Overcards', 0.20),
    (['Jh', '8h'], 'OESD (straight draw)', 0.30),
    (['5s', '4s'], 'Bottom pair', 0.22),
    (['9c', '8c'], 'Second pair + gutshot', 0.38),
    (['Tc', '8c'], 'Top pair + gutshot', 0.48),
    (['Tc', 'Jd'], 'Top pair good kicker', 0.50),
    (['8h', '6h'], 'Made straight', 0.75),
    (['Td', 'Tc'], 'Top set', 0.80),
    (['9s', '9h'], 'Middle set', 0.72),
]

# Board 6: A-high Two-Tone — Flop, Facing Bet (Raise Decision)
# BB faces CO bet + BTN call on Ad9d4c.
PA_BOARD_6_BASE = dict(
    board_cards=['Ad', '9d', '4c'],
    hero_pos='BB',
    villain_positions=['BTN', 'CO'],   # CO is bettor (last in list)
    pot=123.0,
    to_call=33.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BTN', 'call'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

PA_BOARD_6_HANDS = [
    (['7h', '6h'], 'Air', 0.10),
    (['Kh', 'Qh'], 'Overcards no diamond', 0.22),
    (['6d', '5d'], 'Low flush draw', 0.32),
    (['Kd', 'Td'], 'Flush draw + overcard', 0.38),
    (['9c', '8c'], 'Middle pair', 0.28),
    (['Ac', '5c'], 'Top pair weak kicker', 0.48),
    (['Ac', 'Jh'], 'Top pair good kicker', 0.55),
    (['Ah', 'Kc'], 'TPTK + backdoor nut FD', 0.65),
    (['4s', '4h'], 'Bottom set', 0.78),
    (['9d', '9c'], 'Middle set', 0.82),
]

# Board 7: Mid-Connected Two-Tone — Turn, Facing Bet (3-way throughout)
# FIXED: BB now calls the flop bet (stays in). Hero SB faces BTN bet in live 3-way pot.
# Pot recalculated: 90 (preflop) + 30 (BTN flop bet) + 30 (BB call) + 30 (SB call) = 180
# On turn, BTN bets 75 into 180.
PA_BOARD_7_BASE = dict(
    board_cards=['Jc', '8c', '5d', '2h'],
    hero_pos='SB',
    villain_positions=['BB', 'BTN'],   # BTN is bettor (last in list)
    pot=180.0,
    to_call=75.0,
    street='turn',
    action_history=[
        ('preflop', 'BTN', 'raise'),
        ('preflop', 'SB', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'),
        ('flop', 'BB', 'check'),
        ('flop', 'BTN', 'bet'),
        ('flop', 'BB', 'call'),
        ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'),
        ('turn', 'BB', 'check'),
    ],
    opener_position='BTN',
    effective_stack=100.0,
)

PA_BOARD_7_HANDS = [
    (['4h', '3h'], 'Air', 0.06),
    (['Kd', 'Qd'], 'Overcards', 0.20),
    (['Ac', 'Tc'], 'Nut flush draw', 0.35),
    (['9c', '7c'], 'Flush draw + gutshot', 0.38),
    (['5c', '4c'], 'Bottom pair + FD', 0.40),
    (['8h', '7h'], 'Second pair', 0.30),
    (['Jh', 'Td'], 'Top pair medium kicker', 0.50),
    (['Jh', 'Jd'], 'Top set', 0.85),
    (['8s', '8d'], 'Middle set', 0.80),
]

# Board 8: River Brick on Dry Board — River, Lead Decision
# Both opponents checked turn. BB leads river.
PA_BOARD_8_BASE = dict(
    board_cards=['Qc', '8d', '3s', '6h', '2c'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=200.0,
    to_call=0.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BTN', 'call'),
        ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'),
        ('turn', 'CO', 'check'),
        ('turn', 'BTN', 'check'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

PA_BOARD_8_HANDS = [
    (['5h', '4h'], 'Air (missed everything)', 0.05),
    (['Ah', '5h'], 'A-high', 0.25),
    (['Kh', 'Jh'], 'K-high', 0.20),
    (['8h', '7h'], 'Middle pair', 0.35),
    (['Qs', '5s'], 'Top pair bad kicker', 0.52),
    (['Qh', '9c'], 'Top pair medium kicker', 0.58),
    (['Qh', 'Jd'], 'Top pair good kicker', 0.62),
    (['Qh', 'Kc'], 'TPTK', 0.68),
    (['3d', '3c'], 'Set (bottom set)', 0.85),
    (['8c', '8s'], 'Set (middle set)', 0.88),
]

PA_BOARDS = [
    (PA_BOARD_1_BASE, PA_BOARD_1_HANDS, 'PA_Board1_Ac8d3s'),
    (PA_BOARD_2_BASE, PA_BOARD_2_HANDS, 'PA_Board2_9d6c2h'),
    (PA_BOARD_3_BASE, PA_BOARD_3_HANDS, 'PA_Board3_Jh8h4h'),
    (PA_BOARD_4_BASE, PA_BOARD_4_HANDS, 'PA_Board4_QcQd7s'),
    (PA_BOARD_5_BASE, PA_BOARD_5_HANDS, 'PA_Board5_Ts9d5c7h'),
    (PA_BOARD_6_BASE, PA_BOARD_6_HANDS, 'PA_Board6_Ad9d4c'),
    (PA_BOARD_7_BASE, PA_BOARD_7_HANDS, 'PA_Board7_Jc8c5d2h'),
    (PA_BOARD_8_BASE, PA_BOARD_8_HANDS, 'PA_Board8_Qc8d3s6h2c'),
]

# =============================================================================
# CALL BOARDS — 72 situations
# =============================================================================

# Board 1: Jd8d4c — Draw vs Made Hand Boundary
# FIXED: Td9d replaced with 7d6d (flush draw + gutshot, ~12 outs)
CALL_BOARD_1_BASE = dict(
    board_cards=['Jd', '8d', '4c'],
    hero_pos='BB',
    villain_positions=['BTN', 'CO'],   # CO is bettor (last in list)
    pot=90.0,
    to_call=33.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

CALL_BOARD_1_HANDS = [
    (['6s', '3c'], 'high_card: air', 0.04),
    (['Ts', '5s'], 'one_overcard: T with no draw', 0.09),
    (['9h', '7h'], 'high_card: OESD', 0.22),
    (['Qd', '3d'], 'one_overcard: FD', 0.36),
    (['7d', '6d'], 'high_card: FD + gutshot (~12 outs)', 0.38),  # FIXED from Td9d
    (['Ad', 'Ks'], 'overcards: AK no draw', 0.25),
    (['8c', '7c'], 'middle_pair: second pair + gutshot', 0.31),
    (['Jc', '5h'], 'top_pair: TP weak kicker', 0.47),
    (['Js', 'Th'], 'top_pair_good_kicker: TP good kicker', 0.52),
]

# Board 2: Ks9h5d — Bluff-Catcher Boundary IP
CALL_BOARD_2_BASE = dict(
    board_cards=['Ks', '9h', '5d'],
    hero_pos='BTN',
    villain_positions=['CO', 'BB'],   # BB is primary action (leads), last in list
    pot=90.0,
    to_call=45.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'bet'),
        ('flop', 'CO', 'fold'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

CALL_BOARD_2_HANDS = [
    (['7c', '2h'], 'high_card: air', 0.05),
    (['Qh', 'Jh'], 'overcards: QJ', 0.18),
    (['Th', '8h'], 'high_card: gutshot T8', 0.19),
    (['6d', '4d'], 'high_card: gutshot 64', 0.15),
    (['9c', 'Tc'], 'middle_pair: 9T', 0.33),
    (['9s', '8s'], 'middle_pair: 98', 0.31),
    (['Kc', '4c'], 'top_pair: K4', 0.52),
    (['Kh', 'Jd'], 'top_pair_good_kicker: KJ', 0.58),
    (['As', 'Ah'], 'overpair: AA', 0.68),
]

# Board 3: Qh7c2s5d — Turn Barrel Bluff-Catcher
# FIXED: 2c2d (set) replaced with QsJh (TPTGK — genuine CALL/FOLD boundary)
CALL_BOARD_3_BASE = dict(
    board_cards=['Qh', '7c', '2s', '5d'],
    hero_pos='BTN',
    villain_positions=['BB', 'CO'],   # CO is bettor (last in list)
    pot=156.0,
    to_call=60.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BTN', 'call'),
        ('flop', 'BB', 'fold'),
        ('turn', 'BB', 'check'),
        ('turn', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

CALL_BOARD_3_HANDS = [
    (['Jh', 'Th'], 'high_card: overcards + gutshot', 0.08),
    (['9h', '8h'], 'high_card: overcards + gutshot', 0.10),
    (['Ah', '3h'], 'one_overcard: A-high no draw', 0.14),
    (['5h', '5c'], 'set: 55 on turn', 0.91),
    (['Qd', 'Jd'], 'top_pair_good_kicker: QJ', 0.55),
    (['Qs', 'Ts'], 'top_pair: QT', 0.45),
    (['7d', '6d'], 'middle_pair: 76', 0.22),
    (['Qc', 'Kh'], 'top_pair_top_kicker: QK', 0.60),
    (['Qs', 'Jh'], 'top_pair_good_kicker: QsJh boundary hand', 0.48),  # FIXED from 2c2d
]

# Board 4: Ah9c3s6dTc — River Decision (Anti-Over-Call)
# BTN folded on flop — only CO is active. villain_positions = ['CO'] only.
CALL_BOARD_4_BASE = dict(
    board_cards=['Ah', '9c', '3s', '6d', 'Tc'],
    hero_pos='BB',
    villain_positions=['CO'],   # BTN folded on flop; CO only active villain
    pot=280.0,
    to_call=140.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BTN', 'fold'),
        ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'),
        ('turn', 'CO', 'check'),
        ('river', 'BB', 'check'),
        ('river', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

CALL_BOARD_4_HANDS = [
    (['Kd', 'Qd'], 'high_card: KQ no pair', 0.06),
    (['8s', '7s'], 'high_card: 87 no pair', 0.03),
    (['Jd', 'Jc'], 'underpair: JJ', 0.20),
    (['9d', '8d'], 'middle_pair: 98', 0.28),
    (['As', '5s'], 'top_pair: A5', 0.42),
    (['Ad', 'Jd'], 'top_pair_good_kicker: AJ', 0.52),
    (['Ac', 'Kc'], 'top_pair_top_kicker: AK', 0.60),
    (['Tc', '9c'], 'two_pair: T9', 0.75),
    (['3h', '3d'], 'set: 33', 0.90),
]

# Board 5: KdJc6s — Anti-Over-Call with Caller Behind (4-way pre, 3-way flop)
# NOTE: 4-way preflop (CO/BTN/SB/BB) becoming 3-way when SB folds on flop.
# action_history encodes SB fold before the CO bet.
CALL_BOARD_5_BASE = dict(
    board_cards=['Kd', 'Jc', '6s'],
    hero_pos='BB',
    villain_positions=['BTN', 'CO'],   # CO is bettor (last in list)
    pot=155.0,
    to_call=35.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'SB', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'fold'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BTN', 'call'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

CALL_BOARD_5_HANDS = [
    (['5h', '4h'], 'high_card: air', 0.03),
    (['Th', '9h'], 'high_card: gutshot T9', 0.12),
    (['Qc', 'Ts'], 'high_card: gutshot QT', 0.14),
    (['6c', '5c'], 'bottom_pair: 65', 0.15),
    (['Kc', 'Th'], 'top_pair: KT', 0.40),
    (['Kh', 'Qh'], 'top_pair_good_kicker: KQ', 0.48),
    (['Ks', 'Jd'], 'two_pair: KJ', 0.72),
    (['Jh', 'Ts'], 'middle_pair: J-middle', 0.25),
    (['Ac', 'Qc'], 'overcards: AQ', 0.20),
]

# Board 6: Ts8h3s — Wet Board Draw Equity OOP
CALL_BOARD_6_BASE = dict(
    board_cards=['Ts', '8h', '3s'],
    hero_pos='BB',
    villain_positions=['BTN', 'CO'],   # CO is bettor (last in list)
    pot=90.0,
    to_call=25.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

CALL_BOARD_6_HANDS = [
    (['Kd', '2d'], 'one_overcard: K2 no spade draw', 0.07),
    (['Qd', '4d'], 'one_overcard: Q4 no spade draw', 0.06),
    (['7s', '6s'], 'high_card: FD+OESD combo draw', 0.38),
    (['As', 'Kh'], 'one_overcard: nut flush draw', 0.30),
    (['9h', '7h'], 'high_card: OESD', 0.27),
    (['Jc', '9c'], 'high_card: gutshot', 0.23),
    (['3d', '3c'], 'set: bottom set', 0.89),
    (['Td', '7d'], 'top_pair: T7', 0.45),
    (['8d', '7d'], 'middle_pair: 87', 0.28),
]

# Board 7: AsQd5h — Facing Standard Raise (Anti-Over-Call)
# FIXED: terminology from "check-raise" to "standard raise" (CO raises hero's bet)
CALL_BOARD_7_BASE = dict(
    board_cards=['As', 'Qd', '5h'],
    hero_pos='BTN',
    villain_positions=['BB', 'CO'],   # CO is raiser (last in list)
    pot=210.0,
    to_call=60.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'check'),
        ('flop', 'BTN', 'bet'),
        ('flop', 'CO', 'raise'),
        ('flop', 'BB', 'fold'),
    ],
    opener_position='CO',
    effective_stack=100.0,
    current_bet=90.0,   # CO raised to 90 total; hero called 30 initially
)

CALL_BOARD_7_HANDS = [
    (['Kh', 'Jh'], 'high_card: KJ no pair', 0.12),
    (['Th', '9h'], 'high_card: T9 no pair', 0.06),
    (['5c', '4c'], 'bottom_pair: 54', 0.10),
    (['Qc', 'Jc'], 'middle_pair: QJ', 0.25),
    (['Ah', 'Jh'], 'top_pair: AJ', 0.42),
    (['Ac', 'Js'], 'top_pair_good_kicker: AJ offsuit', 0.48),
    (['Ac', 'Kc'], 'top_pair_top_kicker: AK', 0.55),
    (['Ad', 'Qd'], 'two_pair: AQ', 0.82),
    (['5s', '5d'], 'set: 55', 0.93),
]

# Board 8: 7h7d5s9cJs — Trips Facing Check-Raise (Extreme Anti-Over-Call)
CALL_BOARD_8_BASE = dict(
    board_cards=['7h', '7d', '5s', '9c', 'Js'],
    hero_pos='BTN',
    villain_positions=['HJ', 'CO'],   # CO is raiser (last in list)
    pot=500.0,
    to_call=200.0,
    street='river',
    action_history=[
        ('preflop', 'HJ', 'raise'),
        ('preflop', 'CO', 'call'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'HJ', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BTN', 'call'),
        ('flop', 'HJ', 'fold'),
        ('flop', 'BB', 'fold'),
        ('turn', 'HJ', 'check'),
        ('turn', 'CO', 'check'),
        ('turn', 'BTN', 'bet'),
        ('turn', 'CO', 'call'),
        ('river', 'HJ', 'check'),
        ('river', 'CO', 'check'),
        ('river', 'BTN', 'bet'),
        ('river', 'CO', 'raise'),
    ],
    opener_position='HJ',
    effective_stack=100.0,
    current_bet=400.0,  # CO raised to 400 total on river
)

CALL_BOARD_8_HANDS = [
    (['Ts', '8s'], 'straight: T8 straight', 0.55),
    (['Ks', '7c'], 'trips: K7 trips', 0.30),
    (['Jd', 'Jc'], 'full_house: JJ boat', 0.85),
    (['9s', '9h'], 'full_house: 99 boat', 0.78),
    (['Ad', 'Kd'], 'high_card: AK air', 0.02),
    (['As', '7s'], 'trips: A7 trips', 0.35),
    (['5c', '5h'], 'full_house: 55 boat', 0.72),
    (['7s', '5c'], 'full_house: 75 top boat', 0.95),
    (['Ac', 'Jh'], 'top_pair: AJ', 0.12),
]

CALL_BOARDS = [
    (CALL_BOARD_1_BASE, CALL_BOARD_1_HANDS, 'CALL_Board1_Jd8d4c'),
    (CALL_BOARD_2_BASE, CALL_BOARD_2_HANDS, 'CALL_Board2_Ks9h5d'),
    (CALL_BOARD_3_BASE, CALL_BOARD_3_HANDS, 'CALL_Board3_Qh7c2s5d'),
    (CALL_BOARD_4_BASE, CALL_BOARD_4_HANDS, 'CALL_Board4_Ah9c3s6dTc'),
    (CALL_BOARD_5_BASE, CALL_BOARD_5_HANDS, 'CALL_Board5_KdJc6s'),
    (CALL_BOARD_6_BASE, CALL_BOARD_6_HANDS, 'CALL_Board6_Ts8h3s'),
    (CALL_BOARD_7_BASE, CALL_BOARD_7_HANDS, 'CALL_Board7_AsQd5h'),
    (CALL_BOARD_8_BASE, CALL_BOARD_8_HANDS, 'CALL_Board8_775_9_J'),
]


# =============================================================================
# Generation + Validation
# =============================================================================

def generate_all():
    all_situations = []
    total_generated = 0
    total_valid = 0
    total_rejected = 0
    rejection_log = []

    all_boards = []
    for base, hands, board_id in PA_BOARDS:
        all_boards.append((base, hands, board_id, 'PA'))
    for base, hands, board_id in CALL_BOARDS:
        all_boards.append((base, hands, board_id, 'CALL'))

    for base, hands, board_id, design in all_boards:
        print(f"\n--- {board_id} ---")
        for i, (cards, label, equity_est) in enumerate(hands):
            total_generated += 1
            sit_id = f"{board_id}_h{i+1}"

            # Build spec
            spec_kwargs = dict(base)
            spec_kwargs['hero_cards'] = cards
            spec = SituationSpec(**spec_kwargs)

            try:
                feat_dict = build_situation(spec)
            except Exception as e:
                total_rejected += 1
                reason = f"BUILD_ERROR: {e}"
                rejection_log.append((sit_id, reason))
                print(f"  REJECTED h{i+1} {cards}: {reason}")
                continue

            errors = validate_situation(spec, feat_dict)
            if errors:
                total_rejected += 1
                reason = '; '.join(errors)
                rejection_log.append((sit_id, reason))
                print(f"  REJECTED h{i+1} {cards}: {reason}")
                continue

            # Valid — add metadata and append
            feat_dict['_situation_id'] = sit_id
            feat_dict['_board_id'] = board_id
            feat_dict['_design'] = design
            feat_dict['_hand_label'] = label
            feat_dict['_equity_est'] = equity_est
            feat_dict['_hero_cards'] = ''.join(cards)

            total_valid += 1
            all_situations.append(feat_dict)
            print(f"  OK    h{i+1} {cards}  equity~{equity_est}")

    return all_situations, total_generated, total_valid, total_rejected, rejection_log


def main():
    situations, total_gen, total_valid, total_rej, rejections = generate_all()

    # Write JSONL
    with open(OUTPUT_PATH, 'w') as f:
        for sit in situations:
            f.write(json.dumps(sit) + '\n')

    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE")
    print(f"  Total generated: {total_gen}")
    print(f"  Total valid:     {total_valid}")
    print(f"  Total rejected:  {total_rej}")
    print(f"  Output:          {OUTPUT_PATH}")

    if rejections:
        print(f"\nREJECTIONS:")
        for sit_id, reason in rejections:
            print(f"  {sit_id}: {reason}")

    return total_rej == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
