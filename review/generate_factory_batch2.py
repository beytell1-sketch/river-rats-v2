"""
Generate all 261 situations from the 5 Factory Batch 2 design documents:
  - DESIGN_SEMI_BLUFF_SWEEPS.md   (8 boards, 72 situations)  → prefix SB_
  - DESIGN_FLUSH_BLOCKING.md      (5 boards, 45 situations)  → prefix FB_
  - DESIGN_OVERCARD_SPOTS.md      (4 boards, 35 situations)  → prefix OC_
  - DESIGN_THIN_VALUE_RAISE.md    (4 boards, 36 situations)  → prefix TV_
  - DESIGN_BROAD_DISTRIBUTION.md  (9 boards, 73 situations)  → prefix BD_

Run from any directory:
    python3 /home/rupertbeytell/river-rats-v2/review/generate_factory_batch2.py
"""

import sys
import os
import json

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_CORE = os.path.join(_REPO, 'river-rats-core')
sys.path.insert(0, _CORE)
os.chdir(_CORE)

from situation_factory import SituationSpec, build_situation, validate_situation, normalise_situation

OUTPUT_PATH = os.path.join(_REPO, 'training-data', 'factory_batch2_situations.jsonl')

# =============================================================================
# SEMI-BLUFF SWEEP (SB) BOARDS — 72 situations across 8 boards
# =============================================================================

# Board 1: Ks Jd 5s (Flop) — Facing Bet OOP, Nut Flush Draw Board
# Hero SB (OOP). CO opens, BTN calls, SB calls. CO bets 30 into 90.
# villain_positions: BTN (cold-caller, non-bettor) then CO (bettor, LAST)
SB_BOARD_1_BASE = dict(
    board_cards=['Ks', 'Jd', '5s'],
    hero_pos='SB',
    villain_positions=['BTN', 'CO'],   # CO is bettor (last in list)
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'),
        ('flop', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

SB_BOARD_1_HANDS = [
    (['As', 'Qs'], 'NFD + As blocker + 2 overs + gutshot', 0.44),
    (['As', '4s'], 'NFD + As blocker, no side equity', 0.34),
    (['8s', '7s'], 'NFD, NO blocker + gutshot', 0.36),
    (['Qs', 'Ts'], 'NFD, NO blocker, one overcard', 0.32),
    (['Ts', '9s'], 'Non-nut FD (2nd nut), no blocker', 0.30),
    (['9s', '8s'], 'Non-nut FD (3rd nut), no blocker', 0.28),
    (['Qh', 'Th'], 'OESD only, no flush draw', 0.22),
    (['7h', '6h'], 'Gutshot only (4-8)', 0.10),
    (['Kd', 'Td'], 'Made hand, no draw (contrast)', 0.52),
]

# Board 2: Qh 8d 3h (Flop) — Facing Bet IP, Hearts Flush Draw
# Hero BTN (IP). CO opens, BTN calls, BB defends. BB donk-bets 30. CO folds.
# villain_positions: CO (non-bettor) then BB (bettor, LAST)
SB_BOARD_2_BASE = dict(
    board_cards=['Qh', '8d', '3h'],
    hero_pos='BTN',
    villain_positions=['CO', 'BB'],   # BB is bettor (last in list)
    pot=90.0,
    to_call=30.0,
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

SB_BOARD_2_HANDS = [
    (['Ah', 'Kh'], 'NFD + Ah blocker + overcard', 0.48),
    (['Ah', '5h'], 'NFD + Ah blocker, minimal side equity', 0.36),
    (['Kh', 'Jh'], 'NFD, NO blocker, one overcard', 0.34),
    (['Jh', 'Th'], 'NFD, NO blocker + gutshot', 0.34),
    (['9h', '7h'], 'Non-nut FD (low), no blocker', 0.28),
    (['Jc', 'Ts'], 'OESD only, no flush draw', 0.18),
    (['6s', '5s'], 'Gutshot only (4-5-6-7)', 0.08),
    (['8h', '7c'], 'Made hand + flush draw (pair + FD)', 0.40),
    (['Qc', 'Jd'], 'Pure made hand, no draw (contrast)', 0.55),
]

# Board 3: Td 7d 2c (Flop) — NOT Facing Bet OOP, Semi-Bluff Lead Decision
# Hero BB (OOP). CO opens, BTN calls, BB defends. CO checks, BTN checks.
SB_BOARD_3_BASE = dict(
    board_cards=['Td', '7d', '2c'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'check'),
        ('flop', 'BTN', 'check'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

SB_BOARD_3_HANDS = [
    (['Ad', 'Qd'], 'NFD + Ad blocker + overcard', 0.42),
    (['Ad', '3d'], 'NFD + Ad blocker, no side equity', 0.34),
    (['Kd', 'Jd'], 'NFD, NO blocker, one overcard', 0.32),
    (['9d', '8d'], 'Combo draw: NFD + OESD (6-7-8-9-T)', 0.40),
    (['6d', '5d'], 'Non-nut FD + gutshot (only)', 0.30),
    (['9c', '8c'], 'OESD only, no flush draw', 0.28),
    (['Jc', '9c'], 'Gutshot only (8-9-T-J)', 0.14),
    (['7h', '6h'], 'Made pair + gutshot', 0.35),
    (['Th', 'Kc'], 'Pure made hand, no draw (contrast)', 0.55),
]

# Board 4: Jc 8s 4c 9c (Turn) — Facing Second Barrel, 3 Clubs on Turn
# Hero BB (OOP). CO opens, BTN calls, BB calls. Flop Jc 8s 4c: CO bets 33,
# BTN calls, BB calls. Turn 9c: CO bets 80. BTN folds.
# villain_positions: BTN (non-bettor) then CO (bettor, LAST)
SB_BOARD_4_BASE = dict(
    board_cards=['Jc', '8s', '4c', '9c'],
    hero_pos='BB',
    villain_positions=['BTN', 'CO'],   # CO is bettor (last in list)
    pot=200.0,
    to_call=80.0,
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
        ('turn', 'CO', 'bet'),
        ('turn', 'BTN', 'fold'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

SB_BOARD_4_HANDS = [
    (['Ac', 'Kc'], 'Nut flush, made hand (not a draw)', 0.80),
    (['Ac', '5d'], 'Ac blocker only, no flush, no draw', 0.28),
    (['Qc', 'Tc'], '2nd nut flush, made hand', 0.70),
    (['7c', '6c'], 'Low flush, made hand (vulnerable)', 0.60),
    (['Kc', '3d'], 'Single club, no flush, Kc partial blocker', 0.15),
    (['Qh', 'Ts'], 'OESD (7-8-9-T-J-Q) no club', 0.22),
    (['5h', '3h'], 'Complete air, no draw, no blocker', 0.05),
    (['Jh', 'Tc'], 'TP + club (one club, not a flush)', 0.40),
    (['9d', '8d'], 'Two pair, no club, no draw', 0.45),
]

# Board 5: 7s 6s 5d (Flop) — Connected Board, Straight Draws Dominate
# Hero BTN (IP). HJ opens, BTN calls, BB defends. BB donk-bets 45. HJ folds.
# villain_positions: HJ (non-bettor) then BB (bettor, LAST)
SB_BOARD_5_BASE = dict(
    board_cards=['7s', '6s', '5d'],
    hero_pos='BTN',
    villain_positions=['HJ', 'BB'],   # BB is bettor (last in list)
    pot=90.0,
    to_call=45.0,
    street='flop',
    action_history=[
        ('preflop', 'HJ', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'bet'),
        ('flop', 'HJ', 'fold'),
    ],
    opener_position='HJ',
    effective_stack=100.0,
)

SB_BOARD_5_HANDS = [
    (['As', '9s'], 'NFD + As blocker + gutshot (6-7-8-9)', 0.40),
    (['Ks', 'Qs'], 'NFD, NO blocker, no straight equity', 0.30),
    (['9s', '8s'], 'Flopped straight (9-8-7-6-5) + NFD redraw (contrast)', 0.85),
    (['9h', '8h'], 'OESD (5-6-7-8-9) + gutshot, NO flush', 0.40),
    (['9c', '4c'], 'Gutshot only (5-6-7-8-9, bottom)', 0.18),
    (['Th', '8h'], 'OESD (5-6-7-8 or 7-8-9-T), no flush', 0.30),
    (['4s', '3s'], 'Non-nut FD + gutshot (3-4-5-6-7)', 0.28),
    (['7h', '8d'], 'Top pair + gutshot (5-6-7-8-9)', 0.45),
    (['Ac', 'Ad'], 'Pure made hand, overpair, no draw (contrast)', 0.60),
]

# Board 6: 9h 6h 2d Kd (Turn) — Facing Bet OOP, Turn Brings Second Flush Draw
# Hero SB (OOP). CO opens, BTN calls, SB calls. Flop 9h 6h 2d: CO bets 30,
# BTN calls, SB calls. Turn Kd: CO bets 60. BTN still to act behind.
# villain_positions: BTN (non-bettor, behind) then CO (bettor, LAST)
SB_BOARD_6_BASE = dict(
    board_cards=['9h', '6h', '2d', 'Kd'],
    hero_pos='SB',
    villain_positions=['BTN', 'CO'],   # CO is bettor (last in list)
    pot=180.0,
    to_call=60.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BTN', 'call'),
        ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'),
        ('turn', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

SB_BOARD_6_HANDS = [
    (['Ah', 'Qh'], 'NFD hearts + Ah blocker + overcard', 0.38),
    (['Ah', '3c'], 'Ah blocker only, no flush draw', 0.18),
    (['Qh', 'Jh'], 'NFD hearts, NO Ah blocker', 0.28),
    (['Th', '8h'], 'Non-nut FD hearts + gutshot (7-8-9-T)', 0.32),
    (['Ad', 'Td'], 'NFD diamonds + Ad blocker (back-door became front-door)', 0.30),
    (['8s', '7s'], 'OESD (6-7-8-9) only, no flush draw', 0.20),
    (['5c', '4c'], 'Gutshot only (3-4-5-6)', 0.08),
    (['9d', '8d'], 'Made pair + diamond flush draw', 0.35),
    (['Kh', 'Jc'], 'Top pair + Kh (single heart), no draw', 0.50),
]

# Board 7: Ah 9c 4h Th (Turn) — SPR-Collapsed, effective_stack=180
# Hero BB (OOP). CO opens, BTN folds, BB defends. HU. Flop Ah 9c 4h:
# CO bets 60, BB calls. Turn Th: CO bets 140.
# villain_positions: CO only (HU)
SB_BOARD_7_BASE = dict(
    board_cards=['Ah', '9c', '4h', 'Th'],
    hero_pos='BB',
    villain_positions=['CO'],   # CO is bettor, HU
    pot=350.0,
    to_call=140.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'fold'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'),
        ('turn', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=180.0,
)

SB_BOARD_7_HANDS = [
    (['Kh', 'Qh'], 'NFD + Kh blocker. SPR 0.5 = CALL (no fold equity)', 0.36),
    (['Kh', '5h'], 'NFD + Kh blocker, no side equity. SPR collapse = CALL or FOLD', 0.28),
    (['Qh', 'Jh'], 'NFD, no ace blocker + gutshot (J-Q-K). CALL territory', 0.34),
    (['8h', '7h'], 'Non-nut FD (low), no blocker. SPR collapse = likely FOLD', 0.26),
    (['Jc', '8c'], 'Gutshot only (7-8-9-T-J). No flush. FOLD', 0.15),
    (['9h', '8h'], 'Pair + flush draw. SPR collapse = CALL', 0.35),
    (['Th', '9d'], 'Two pair, no draw. Contrast: call/raise for value', 0.55),
    (['Kd', 'Qd'], 'Two overcards, no flush draw. SPR collapse = FOLD', 0.18),
    (['Ah', 'Kc'], 'TPTK + Ah (single heart). Contrast: made hand at low SPR', 0.60),
]

# Board 8: Qs 8s 3d 5c Jh (River) — Bricked Flush Draw, Ace Blocker Paradox
# Hero SB (OOP). CO opens, BTN calls, SB defends. Flop Qs 8s 3d: CO bets 30,
# BTN calls, SB calls. Turn 5c: all check. River Jh: CO checks, BTN bets 100.
# villain_positions: CO (non-bettor) then BTN (bettor, LAST)
SB_BOARD_8_BASE = dict(
    board_cards=['Qs', '8s', '3d', '5c', 'Jh'],
    hero_pos='SB',
    villain_positions=['CO', 'BTN'],   # BTN is bettor (last in list)
    pot=280.0,
    to_call=100.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BTN', 'call'),
        ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'),
        ('turn', 'CO', 'check'),
        ('turn', 'BTN', 'check'),
        ('river', 'SB', 'check'),
        ('river', 'CO', 'check'),
        ('river', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

SB_BOARD_8_HANDS = [
    (['As', 'Ks'], 'Busted NFD + As blocker. As BLOCKS villain\'s folds. Bluff-raise worst', 0.15),
    (['As', '4s'], 'Busted NFD + As, no pair. As blocks folds. FOLD likely', 0.10),
    (['Ks', 'Ts'], 'Busted NFD, NO As. Ks blocks some value (KQ). Better bluff candidate', 0.12),
    (['9s', '7s'], 'Busted low FD. No blocker to value or folds. Pure FOLD', 0.08),
    (['As', 'Td'], 'As single spade + no flush draw. As blocks busted draws', 0.18),
    (['Qd', 'Ts'], 'Busted FD but paired Q on flop. Showdown value', 0.45),
    (['Jd', '9d'], 'Rivered pair of jacks, no flush involvement. CALL territory', 0.30),
    (['Kh', 'Qh'], 'No spade involvement, paired Q on flop. Pure made-hand call', 0.50),
    (['6s', '5s'], 'Busted FD + bottom pair. Weak showdown + no blocker value', 0.15),
]

SB_BOARDS = [
    (SB_BOARD_1_BASE, SB_BOARD_1_HANDS, 'SB_Board1_KsJd5s'),
    (SB_BOARD_2_BASE, SB_BOARD_2_HANDS, 'SB_Board2_Qh8d3h'),
    (SB_BOARD_3_BASE, SB_BOARD_3_HANDS, 'SB_Board3_Td7d2c'),
    (SB_BOARD_4_BASE, SB_BOARD_4_HANDS, 'SB_Board4_Jc8s4c9c'),
    (SB_BOARD_5_BASE, SB_BOARD_5_HANDS, 'SB_Board5_7s6s5d'),
    (SB_BOARD_6_BASE, SB_BOARD_6_HANDS, 'SB_Board6_9h6h2dKd'),
    (SB_BOARD_7_BASE, SB_BOARD_7_HANDS, 'SB_Board7_Ah9c4hTh'),
    (SB_BOARD_8_BASE, SB_BOARD_8_HANDS, 'SB_Board8_Qs8s3d5cJh'),
]


# =============================================================================
# FLUSH BLOCKING (FB) BOARDS — 45 situations across 5 boards
# =============================================================================

# Board F1: Jh 7h 2c (Flop) — Heart Flush Draw Board, Hero Blocking Variance
# Hero CO (IP, opener). CO opens, BTN calls, BB defends. BB donk-bets 25. BTN folds.
# villain_positions: BTN (non-bettor) then BB (bettor, LAST)
FB_BOARD_1_BASE = dict(
    board_cards=['Jh', '7h', '2c'],
    hero_pos='CO',
    villain_positions=['BTN', 'BB'],   # BB is bettor (last in list)
    pot=90.0,
    to_call=25.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'bet'),
        ('flop', 'BTN', 'fold'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

FB_BOARD_1_HANDS = [
    (['Ah', 'Kh'], '2 hearts = hero HAS flush draw. flush_block_pct=0 (holds draw)', 0.40),
    (['Ah', 'Qc'], '1 heart (Ah) partial block. Overcards', 0.32),
    (['Kh', 'Td'], '1 heart (Kh) partial block, non-nut', 0.22),
    (['Jc', '9c'], '0 hearts, no blocking. Top pair', 0.52),
    (['Jd', 'Ts'], '0 hearts, no blocking. TP + gutshot', 0.50),
    (['Qh', '9h'], '2 hearts, high blocking. Non-nut FD', 0.30),
    (['8h', '6h'], '2 hearts, mid blocking. Low FD + gutshot', 0.28),
    (['Ac', 'Kd'], '0 hearts, zero blocking. AK no flush involvement', 0.28),
    (['7d', '6d'], '0 hearts, zero blocking. Pair + gutshot', 0.35),
]

# Board F2: Kc 9c 5d 3c (Turn) — Club Flush Completed, Blocking Matters for Calls
# Hero BB (OOP). CO opens, BTN calls, BB defends. Flop Kc 9c 5d: CO bets 33,
# BTN calls, BB calls. Turn 3c: CO bets 80. BTN still behind.
# villain_positions: BTN (non-bettor) then CO (bettor, LAST)
FB_BOARD_2_BASE = dict(
    board_cards=['Kc', '9c', '5d', '3c'],
    hero_pos='BB',
    villain_positions=['BTN', 'CO'],   # CO is bettor (last in list)
    pot=200.0,
    to_call=80.0,
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
        ('turn', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

FB_BOARD_2_HANDS = [
    (['Ac', 'Jc'], 'Nut flush made. Max blocking irrelevant (hero has it)', 0.80),
    (['Kd', 'Jd'], '0 clubs, zero blocking. TP facing 3-flush board', 0.35),
    (['Kh', 'Jc'], '1 club (Jc) partial block. Same hand, club changes call EV', 0.40),
    (['9d', '8d'], '0 clubs, zero blocking. Second pair, vulnerable', 0.22),
    (['9h', '8c'], '1 club (8c) partial block. Same pair, club helps', 0.26),
    (['Ac', '4d'], '1 club (Ac) blocks NFD. No made hand, just blocker', 0.18),
    (['Qc', 'Tc'], '2nd nut flush. High blocking built-in', 0.65),
    (['5h', '4h'], '0 clubs, zero blocking. Bottom pair on 3-flush board', 0.12),
    (['Ah', 'Qh'], '0 clubs, zero blocking. Overcards, no flush involvement', 0.15),
]

# Board F3: Td 6d 2s 8h (Turn) — Diamond Flush Draw Still Live
# Hero BTN (IP). CO opens, BTN calls, BB defends. Flop Td 6d 2s: all check.
# Turn 8h: BB bets 45 into 180. CO folds.
# villain_positions: CO (non-bettor) then BB (bettor, LAST)
FB_BOARD_3_BASE = dict(
    board_cards=['Td', '6d', '2s', '8h'],
    hero_pos='BTN',
    villain_positions=['CO', 'BB'],   # BB is bettor (last in list)
    pot=180.0,
    to_call=45.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'check'),
        ('flop', 'BTN', 'check'),
        ('turn', 'BB', 'bet'),
        ('turn', 'CO', 'fold'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

FB_BOARD_3_HANDS = [
    (['Ad', 'Kd'], '2 diamonds, max blocking. NFD + overcards', 0.50),
    (['Ad', '9c'], '1 diamond (Ad) blocks NFD specifically', 0.30),
    (['Kd', 'Jc'], '1 diamond (Kd) partial block, non-nut', 0.25),
    (['Th', 'Jh'], '0 diamonds, zero blocking. TP', 0.50),
    (['Td', '9d'], '2 diamonds, high blocking + TP. TP with NFD redraw', 0.55),
    (['8d', '7d'], '2 diamonds, pair + FD. Mid blocking', 0.40),
    (['9c', '7c'], '0 diamonds, OESD only, no blocking', 0.20),
    (['Qd', '5d'], '2 diamonds, FD but non-nut. High blocking', 0.30),
    (['Ac', 'Kc'], '0 diamonds, zero blocking. AK off-suit for diamonds', 0.25),
]

# Board F4: As 7s 3c Ks 9d (River) — Spade Flush Completed on Turn, River Decision
# Hero CO (IP, opener). CO opens, BTN calls, BB defends. Flop As 7s 3c:
# CO bets 30, BTN calls, BB calls. Turn Ks: CO bets 60, BB calls, BTN folds.
# River 9d: BB bets 100 into 300.
# villain_positions: BTN (folded preflop/on turn) then BB (bettor, LAST)
# Note: BTN folded on turn. BB is sole remaining villain and bettor.
FB_BOARD_4_BASE = dict(
    board_cards=['As', '7s', '3c', 'Ks', '9d'],
    hero_pos='CO',
    villain_positions=['BTN', 'BB'],   # BB is bettor (last in list)
    pot=300.0,
    to_call=100.0,
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
        ('turn', 'CO', 'bet'),
        ('turn', 'BTN', 'fold'),
        ('turn', 'BB', 'call'),
        ('river', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

FB_BOARD_4_HANDS = [
    (['Qs', 'Js'], '2 spades, busted draw. High blocking but no hand', 0.20),
    (['Ts', '8s'], '2 spades, busted draw. Mid blocking', 0.15),
    (['Ad', 'Qd'], '0 spades, zero blocking. Top pair A', 0.50),
    (['Ad', 'Qs'], '1 spade (Qs) partial block. Same top pair, spade helps', 0.55),
    (['Kd', 'Qd'], '0 spades, zero blocking. Second pair K', 0.40),
    (['Kh', 'Qs'], '1 spade (Qs) partial block. K pair + spade block', 0.45),
    (['9s', '8c'], '1 spade (9s) minor block. Rivered pair', 0.25),
    (['Jh', 'Tc'], '0 spades, zero blocking. No pair, no block', 0.10),
    (['Ah', '7h'], '0 spades, zero blocking. Two pair, strong made hand', 0.60),
]

# Board F5: 8h 5h 2d Qh Jc (River) — Heart Flush Completed, River Value/Bluff
# Hero BB (OOP). HU vs CO. CO opens, BTN folds, BB defends. Flop 8h 5h 2d:
# CO bets 30, BB calls. Turn Qh: CO bets 60, BB calls. River Jc: CO checks.
# villain_positions: CO only (HU, not betting)
FB_BOARD_5_BASE = dict(
    board_cards=['8h', '5h', '2d', 'Qh', 'Jc'],
    hero_pos='BB',
    villain_positions=['CO'],   # CO is sole villain, not betting
    pot=240.0,
    to_call=0.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'fold'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'),
        ('turn', 'CO', 'bet'),
        ('turn', 'BB', 'call'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

FB_BOARD_5_HANDS = [
    (['Ah', 'Kh'], 'Nut flush made. Bet for value', 0.85),
    (['Ah', '9c'], '1 heart (Ah) blocks NFD. Bluff candidate?', 0.20),
    (['Kh', '9c'], '1 heart (Kh) partial block. Worse bluff than Ah', 0.15),
    (['9h', '7h'], 'Low flush made. Bet thin value?', 0.65),
    (['Th', '6h'], 'Low flush made. Thin value territory', 0.60),
    (['Qd', 'Jd'], '0 hearts, zero blocking. Rivered two pair', 0.45),
    (['8c', '7c'], '0 hearts, zero blocking. Second pair, check behind?', 0.20),
    (['Kd', 'Td'], '0 hearts, zero blocking. No pair, no flush', 0.10),
    (['5d', '4d'], '0 hearts, zero blocking. Bottom pair, give up?', 0.12),
]

FB_BOARDS = [
    (FB_BOARD_1_BASE, FB_BOARD_1_HANDS, 'FB_Board1_Jh7h2c'),
    (FB_BOARD_2_BASE, FB_BOARD_2_HANDS, 'FB_Board2_Kc9c5d3c'),
    (FB_BOARD_3_BASE, FB_BOARD_3_HANDS, 'FB_Board3_Td6d2s8h'),
    (FB_BOARD_4_BASE, FB_BOARD_4_HANDS, 'FB_Board4_As7s3cKs9d'),
    (FB_BOARD_5_BASE, FB_BOARD_5_HANDS, 'FB_Board5_8h5h2dQhJc'),
]


# =============================================================================
# OVERCARD SPOTS (OC) BOARDS — 35 situations across 4 boards
# =============================================================================

# Board O1: 9c 6h 3d (Flop) — Low Board, Overcard Call Decision
# Hero BTN (IP). CO opens, BTN calls, BB defends. Flop 9c 6h 3d:
# CO bets 30. BB folds. Hero faces 30.
# villain_positions: BB (non-bettor) then CO (bettor, LAST)
OC_BOARD_1_BASE = dict(
    board_cards=['9c', '6h', '3d'],
    hero_pos='BTN',
    villain_positions=['BB', 'CO'],   # CO is bettor (last in list)
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BB', 'fold'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

OC_BOARD_1_HANDS = [
    (['Ah', 'Kh'], '2 overcards (6 outs to TPTK). Best overcard hand', 0.28),
    (['Ah', 'Qd'], '2 overcards. AQ slightly less value than AK', 0.26),
    (['Kh', 'Jd'], '2 overcards. KJ weaker kicker value if hit', 0.24),
    (['Ah', '8c'], '1 overcard (A only). A8 ace overcard + weak kicker', 0.22),
    (['Kh', '5c'], '1 overcard (K only). K5 king overcard, weak', 0.18),
    (['Th', '8h'], '1 overcard (T over 9) + gutshot + backdoor FD', 0.25),
    (['7h', '5h'], '0 overcards. Gutshot only (4-5-6-7-8)', 0.15),
    (['4c', '2c'], '0 overcards. Complete air, no draws', 0.08),
    (['9d', 'Td'], '1 overcard (T) but also TP. Contrast: made hand', 0.55),
]

# Board O2: 8d 5c 2h Jh (Turn) — Turn Overcard Arrived, Facing Second Barrel
# Hero BB (OOP). CO opens, BTN calls, BB defends. Flop 8d 5c 2h:
# CO bets 33, BTN calls, BB calls. Turn Jh: CO bets 70. BTN still behind.
# villain_positions: BTN (non-bettor) then CO (bettor, LAST)
OC_BOARD_2_BASE = dict(
    board_cards=['8d', '5c', '2h', 'Jh'],
    hero_pos='BB',
    villain_positions=['BTN', 'CO'],   # CO is bettor (last in list)
    pot=200.0,
    to_call=70.0,
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
        ('turn', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

OC_BOARD_2_HANDS = [
    (['Ah', 'Kc'], '2 overcards (A, K). Double barrel + 3-way = tight spot', 0.25),
    (['Ah', 'Qd'], '2 overcards. AQ facing double barrel', 0.23),
    (['Kc', 'Qd'], '2 overcards (K, Q). Weakest 2-overcard holding', 0.20),
    (['Ah', '7c'], '1 overcard (A). A7 one overcard facing aggression', 0.18),
    (['Qd', '9c'], '1 overcard (Q) + middle pair on flop. J turn improves villain', 0.20),
    (['Td', '9d'], '0 overcards (T < J). OESD (7-8-9-T-J) helps', 0.15),
    (['6c', '4c'], '0 overcards. Gutshot (3-4-5-6-7)', 0.10),
    (['Jd', 'Td'], '0 (has TP). Contrast: J gave hero top pair', 0.45),
    (['8c', '7c'], '0 overcards. Second pair + gutshot facing barrel', 0.22),
]

# Board O3: 7c 4d 2s 9h Tc (River) — River Brick, Overcards Never Improved
# Hero CO (IP, opener). CO opens, BTN calls, BB defends. Flop 7c 4d 2s:
# all check. Turn 9h: BB bets 40, CO calls, BTN folds. River Tc: BB bets 80.
# villain_positions: BTN (folded) then BB (bettor, LAST)
OC_BOARD_3_BASE = dict(
    board_cards=['7c', '4d', '2s', '9h', 'Tc'],
    hero_pos='CO',
    villain_positions=['BTN', 'BB'],   # BB is bettor (last in list)
    pot=250.0,
    to_call=80.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'check'),
        ('flop', 'BTN', 'check'),
        ('turn', 'BB', 'bet'),
        ('turn', 'CO', 'call'),
        ('turn', 'BTN', 'fold'),
        ('river', 'BB', 'bet'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

OC_BOARD_3_HANDS = [
    (['Ah', 'Kh'], '2 overcards (A, K). Never improved. Fold or hero call?', 0.20),
    (['Ah', 'Qd'], '2 overcards. AQ river missed everything', 0.18),
    (['Kd', 'Qd'], '2 overcards. KQ weakest high cards, no pair', 0.15),
    (['Ah', '6c'], '1 overcard (A). A6 with bottom-pair-ish equity', 0.14),
    (['Kd', '8c'], '1 overcard (K). K8, one overcard remaining', 0.12),
    (['Jd', '8d'], '0 overcards now (J < board cards). J not an overcard', 0.10),
    (['5c', '3c'], '0 overcards. Complete air, gutshot missed', 0.05),
    (['Tc', '8c'], '0 (has TP). Rivered top pair. Contrast: call easily', 0.50),
    (['Qd', 'Jd'], '1 overcard (Q). QJ missed J no longer an overcard', 0.12),
]

# Board O4: 6s 3h 2c Ts (Turn) — Low Board, Not Facing Bet, Overcard Bet Decision
# Hero BTN (IP). CO opens, BTN calls, BB defends. Flop 6s 3h 2c: all check.
# Turn Ts: CO checks, BB checks. Hero closing action.
OC_BOARD_4_BASE = dict(
    board_cards=['6s', '3h', '2c', 'Ts'],
    hero_pos='BTN',
    villain_positions=['CO', 'BB'],
    pot=90.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'check'),
        ('flop', 'BTN', 'check'),
        ('turn', 'BB', 'check'),
        ('turn', 'CO', 'check'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

OC_BOARD_4_HANDS = [
    (['Ah', 'Kh'], '2 overcards. Opponents weak, bet thin?', 0.35),
    (['Kd', 'Qd'], '2 overcards. KQ bet or check behind?', 0.30),
    (['Ah', '5c'], '1 overcard (A) + gutshot (2-3-4-5). Bet candidate', 0.25),
    (['Qd', '9c'], '1 overcard (Q). Weak, check or stab?', 0.22),
    (['Jc', '9c'], '0 overcards (J < T? No — J > T). Actually 1 overcard', 0.18),
    (['8h', '7h'], '0 overcards. Gutshot (4-5-6-7-8)', 0.15),
    (['4d', '4c'], '0 overcards. Pocket pair below board', 0.40),
    (['Ah', 'Jd'], '2 overcards (A, J). AJ on low board, bet?', 0.33),
]

OC_BOARDS = [
    (OC_BOARD_1_BASE, OC_BOARD_1_HANDS, 'OC_Board1_9c6h3d'),
    (OC_BOARD_2_BASE, OC_BOARD_2_HANDS, 'OC_Board2_8d5c2hJh'),
    (OC_BOARD_3_BASE, OC_BOARD_3_HANDS, 'OC_Board3_7c4d2s9hTc'),
    (OC_BOARD_4_BASE, OC_BOARD_4_HANDS, 'OC_Board4_6s3h2cTs'),
]


# =============================================================================
# THIN VALUE / RAISE (TV) BOARDS — 36 situations across 4 boards
# =============================================================================

# Board TV1: Qc 8d 4s 2h (Turn) — Capped Villain, Thin Value Bet OOP
# Hero BB (OOP). CO opens, BTN calls, BB defends. Flop Qc 8d 4s:
# CO bets 30, BTN calls, BB calls. Turn 2h: CO checks, BTN checks.
TV_BOARD_1_BASE = dict(
    board_cards=['Qc', '8d', '4s', '2h'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=180.0,
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
    ],
    opener_position='CO',
    effective_stack=100.0,
)

TV_BOARD_1_HANDS = [
    (['Qd', '7d'], 'TPWK. Both opponents weak, bet thin for value?', 0.58),
    (['Qh', '5h'], 'TP worst kicker. Even weaker, still thin value?', 0.55),
    (['8c', '7c'], 'Second pair. Too thin to bet? Or value vs air?', 0.35),
    (['4h', '3h'], 'Bottom pair. Check for showdown value?', 0.22),
    (['Ah', 'Kh'], 'Two overcards, no pair. Bet as bluff or check?', 0.30),
    (['Jd', 'Td'], 'Overcards + gutshot (7-8-9-T-J). Semi-bluff?', 0.18),
    (['Qc', 'Jc'], 'TPGK. Clear value, how does sizing change?', 0.62),
    (['Kd', 'Qd'], 'TPSK. Strongest TP, bet for value OOP', 0.65),
    (['9c', '9d'], 'Underpair to Q but overpair to board. Thin value?', 0.52),
]

# Board TV2: Jd 7c 3s Ah (Turn) — Scare Card, Thin Value Against Scared Ranges
# Hero CO (IP, opener). CO opens, BTN calls, BB defends. Flop Jd 7c 3s:
# CO bets 30, BTN calls, BB calls. Turn Ah: hero to act.
TV_BOARD_2_BASE = dict(
    board_cards=['Jd', '7c', '3s', 'Ah'],
    hero_pos='CO',
    villain_positions=['BTN', 'BB'],
    pot=180.0,
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
    ],
    opener_position='CO',
    effective_stack=100.0,
)

TV_BOARD_2_HANDS = [
    (['Ac', '9c'], 'Turned TP with A. Value bet the scare card?', 0.60),
    (['Ah', '5h'], 'Turned TP weak kicker. Thin value on scary turn?', 0.55),
    (['Jh', 'Th'], 'Was TP on flop, now 2nd pair. Check or barrel?', 0.30),
    (['Jc', '9c'], 'Was TPWK, now 2nd pair weaker. Turn check?', 0.28),
    (['Kc', 'Kd'], 'KK A on turn is nightmare card. Still value?', 0.45),
    (['7h', '6h'], 'Second pair (7s). Check for showdown?', 0.20),
    (['Qd', 'Qc'], 'QQ same dilemma as KK. Ace scares hero too', 0.42),
    (['Ac', 'Kc'], 'TPTK. Clear value but how big?', 0.70),
    (['5d', '4d'], 'Air. Bluff the scare card? Or give up?', 0.10),
]

# Board TV3: Kd 9s 5h 2c Qh (River) — River Raise Boundary, Value Raise vs Call
# Hero BTN (IP). CO opens, BTN calls, BB defends. Flop Kd 9s 5h:
# CO bets 30, BTN calls, BB calls. Turn 2c: CO bets 60, BB folds, BTN calls.
# River Qh: CO bets 50. BB folded on turn.
# villain_positions: BB (folded) then CO (bettor, LAST)
TV_BOARD_3_BASE = dict(
    board_cards=['Kd', '9s', '5h', '2c', 'Qh'],
    hero_pos='BTN',
    villain_positions=['CO'],   # BB folded on turn; CO is sole remaining villain and bettor
    pot=350.0,
    to_call=50.0,
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
        ('turn', 'CO', 'bet'),
        ('turn', 'BB', 'fold'),
        ('turn', 'BTN', 'call'),
        ('river', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

TV_BOARD_3_HANDS = [
    (['Kc', 'Qc'], 'Rivered top two. Raise for value or call (trap)?', 0.75),
    (['Kh', 'Jh'], 'TPGK. Call the small bet, too thin to raise', 0.55),
    (['Kd', '8d'], 'TPWK. Marginal call vs small bet', 0.45),
    (['9c', '8c'], 'Second pair. Call or fold small river bet?', 0.30),
    (['Qd', 'Jd'], 'Rivered pair of Q. Was drawing, now marginal made', 0.40),
    (['Ah', 'Ad'], 'AA call. Too thin to raise river (only better calls)', 0.60),
    (['5c', '5d'], 'Set of 5s. Raise for value, sets are the raise threshold', 0.85),
    (['7h', '6h'], 'Air. Bluff-raise the small bet?', 0.08),
    (['Kc', '9c'], 'K9 two pair. Raise or call?', 0.70),
]

# Board TV4: Tc 7d 4c 8s (Turn) — Raise Boundary, Equity + Fold Equity
# Hero SB (OOP). CO opens, BTN calls, SB calls. Flop Tc 7d 4c:
# CO bets 33, BTN calls, SB calls. Turn 8s: CO bets 70. BTN still behind.
# villain_positions: BTN (non-bettor) then CO (bettor, LAST)
TV_BOARD_4_BASE = dict(
    board_cards=['Tc', '7d', '4c', '8s'],
    hero_pos='SB',
    villain_positions=['BTN', 'CO'],   # CO is bettor (last in list)
    pot=200.0,
    to_call=70.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BTN', 'call'),
        ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'),
        ('turn', 'CO', 'bet'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

TV_BOARD_4_HANDS = [
    (['Ac', '9c'], 'NFD + OESD (6-7-8-9-T) + Ac blocker. Raise candidate?', 0.38),
    (['9c', '6c'], 'NFD + OESD. No Ac blocker, call instead?', 0.35),
    (['Jh', '9h'], 'OESD only (7-8-9-T-J). No flush. Call with odds?', 0.30),
    (['9d', '6d'], 'OESD (6-7-8-9). No flush. Weaker straight draw', 0.25),
    (['Th', '9h'], 'TP + OESD. Strong combo, raise or call?', 0.50),
    (['Tc', 'Jc'], 'TP + NFD redraw + OESD. Monster combo, raise?', 0.55),
    (['8d', '7c'], 'Turned two pair. Raise for protection or call?', 0.60),
    (['4d', '4h'], 'Set of 4s. Clear raise territory', 0.80),
    (['Kd', 'Qd'], 'Two overcards, no draws. Fold facing barrel', 0.15),
]

TV_BOARDS = [
    (TV_BOARD_1_BASE, TV_BOARD_1_HANDS, 'TV_Board1_Qc8d4s2h'),
    (TV_BOARD_2_BASE, TV_BOARD_2_HANDS, 'TV_Board2_Jd7c3sAh'),
    (TV_BOARD_3_BASE, TV_BOARD_3_HANDS, 'TV_Board3_Kd9s5h2cQh'),
    (TV_BOARD_4_BASE, TV_BOARD_4_HANDS, 'TV_Board4_Tc7d4c8s'),
]


# =============================================================================
# BROAD DISTRIBUTION (BD) BOARDS — 73 situations across 9 boards
# =============================================================================

# Board BD1: Ac Kd 7h (Flop) — Ace-High Dry, Standard 3-Way Flop
# Hero CO (IP, opener). CO opens, BTN calls, BB defends. Hero first to act.
BD_BOARD_1_BASE = dict(
    board_cards=['Ac', 'Kd', '7h'],
    hero_pos='CO',
    villain_positions=['BTN', 'BB'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

BD_BOARD_1_HANDS = [
    (['Ah', 'Qh'], 'TP + strong kicker. C-bet for value', 0.65),
    (['Kc', 'Jc'], 'Second pair. C-bet or pot control?', 0.45),
    (['Td', 'Ts'], 'Underpair to board. Check or small c-bet?', 0.35),
    (['Qd', 'Jd'], 'Two overcards to 7 but under A/K. Gutshot (T-J-Q)', 0.20),
    (['9h', '8h'], 'Backdoor draws only. Give up or small stab?', 0.15),
    (['Ad', '7d'], 'Top two pair. Bet for value + protection', 0.75),
    (['7c', '7d'], 'Bottom set. Bet or slowplay?', 0.85),
    (['6h', '5h'], 'Complete air. Check behind', 0.08),
]

# Board BD2: 5d 5c 9h Jd (Turn) — Paired Board, Turn Action
# Hero BTN (IP). CO opens, BTN calls, BB defends. Flop 5d 5c 9h:
# CO bets 33, BB calls, BTN calls. Turn Jd: CO bets 70. BB folds.
# villain_positions: BB (folded) then CO (bettor, LAST)
BD_BOARD_2_BASE = dict(
    board_cards=['5d', '5c', '9h', 'Jd'],
    hero_pos='BTN',
    villain_positions=['BB', 'CO'],   # CO is bettor (last in list)
    pot=200.0,
    to_call=70.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BB', 'call'),
        ('flop', 'BTN', 'call'),
        ('turn', 'BB', 'check'),
        ('turn', 'CO', 'bet'),
        ('turn', 'BB', 'fold'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

BD_BOARD_2_HANDS = [
    (['Jh', 'Th'], 'Turned TP on paired board. Call or fold?', 0.55),
    (['9c', '8c'], 'Pair of 9s. Weaker, fold to double barrel?', 0.30),
    (['Ah', 'Ad'], 'AA on paired board. Call confidently', 0.65),
    (['Kh', 'Kd'], 'KK strong but J on turn worries', 0.60),
    (['5h', '4h'], 'Trips. Raise or slowplay the double barrel?', 0.80),
    (['Qd', 'Td'], 'Gutshot (8-9-T-J-Q). Speculative call or fold?', 0.15),
    (['Ac', '5s'], 'A5 trips with top kicker. Raise for value', 0.85),
    (['7c', '6c'], 'Air with gutshot potential. Fold', 0.10),
]

# Board BD3: Td 8c 3h 6s (Turn) — Medium Wet Board, Not Facing Bet
# Hero BB (OOP). CO opens, BTN calls, BB defends. Flop Td 8c 3h:
# CO bets 30, BTN calls, BB calls. Turn 6s: CO checks, BTN checks.
BD_BOARD_3_BASE = dict(
    board_cards=['Td', '8c', '3h', '6s'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=180.0,
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
    ],
    opener_position='CO',
    effective_stack=100.0,
)

BD_BOARD_3_HANDS = [
    (['Td', '9d'], 'TP decent kicker. Bet the weakness or check?', 0.55),
    (['8h', '7h'], 'Second pair + gutshot. Check or value bet?', 0.40),
    (['Jc', '9c'], 'OESD (7-8-9-T-J). Bet as semi-bluff?', 0.25),
    (['3c', '2c'], 'Bottom pair. Pure check, showdown value', 0.18),
    (['6d', '6c'], 'Turned set. Bet for value + protection', 0.85),
    (['Ah', 'Kh'], 'Two overcards. Bluff the weakness?', 0.22),
    (['5c', '4c'], 'OESD (3-4-5-6-7). Bet or realize equity?', 0.20),
    (['Tc', '8d'], 'Top two pair. Clear value bet', 0.70),
]

# Board BD4: Kh 9d 4c 2s Jc (River) — Dry Board, River Decision Facing Bet
# Hero SB (OOP). CO opens, BTN calls, SB calls. Flop Kh 9d 4c:
# CO bets 30, BTN calls, SB calls. Turn 2s: all check. River Jc: CO bets
# 120. BTN folds.
# villain_positions: BTN (folded) then CO (bettor, LAST)
BD_BOARD_4_BASE = dict(
    board_cards=['Kh', '9d', '4c', '2s', 'Jc'],
    hero_pos='SB',
    villain_positions=['BTN', 'CO'],   # CO is bettor (last in list)
    pot=300.0,
    to_call=120.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'),
        ('flop', 'CO', 'bet'),
        ('flop', 'BTN', 'call'),
        ('flop', 'SB', 'call'),
        ('turn', 'SB', 'check'),
        ('turn', 'CO', 'check'),
        ('turn', 'BTN', 'check'),
        ('river', 'SB', 'check'),
        ('river', 'CO', 'bet'),
        ('river', 'BTN', 'fold'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

BD_BOARD_4_HANDS = [
    (['Kd', 'Qd'], 'TPSK. Big river bet after turn check, call or fold?', 0.45),
    (['Kc', 'Tc'], 'TPWK. Facing big bet, likely fold?', 0.35),
    (['9h', '8h'], 'Second pair. Fold to big river bet', 0.20),
    (['Jd', 'Td'], 'Rivered pair of J. Call, villain could be bluffing', 0.40),
    (['Ah', 'Ad'], 'AA. River J doesn\'t complete any draw, call', 0.55),
    (['Kh', 'Jh'], 'Rivered top two. Easy call', 0.70),
    (['Ac', '5c'], 'Air + backdoor club miss. Fold', 0.08),
    (['Qd', 'Td'], 'QT no pair, riveted gutshot missed. Fold', 0.10),
]

# Board BD5: 7h 4d 2c Qd 9s (River) — Low Flop, Q Turn, Brick River
# Hero CO (IP, opener). CO opens, BTN calls, BB defends. Flop 7h 4d 2c:
# CO checks, BTN checks, BB bets 40, CO calls, BTN folds. Turn Qd:
# BB bets 55, CO calls. River 9s: BB checks.
# villain_positions: BTN (folded) then BB (present, checked river)
BD_BOARD_5_BASE = dict(
    board_cards=['7h', '4d', '2c', 'Qd', '9s'],
    hero_pos='CO',
    villain_positions=['BTN', 'BB'],   # BB is primary villain (last in list)
    pot=280.0,
    to_call=0.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'bet'),
        ('flop', 'CO', 'call'),
        ('flop', 'BTN', 'fold'),
        ('turn', 'BB', 'bet'),
        ('turn', 'CO', 'call'),
        ('river', 'BB', 'check'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

BD_BOARD_5_HANDS = [
    (['Qh', 'Jh'], 'Paired Q on turn. BB checked river, value bet?', 0.55),
    (['7c', '6c'], 'Pair of 7s. BB range stronger, check behind', 0.25),
    (['Ad', 'Kd'], 'Two overcards + diamond backdoor. Bluff river?', 0.20),
    (['Ah', 'Qc'], 'TPGK (Q). Value bet river after BB checks', 0.60),
    (['9c', '8c'], 'Rivered pair of 9. Thin value or check?', 0.35),
    (['Kh', 'Kc'], 'KK overcalled by Q on turn, held up? Bet thin?', 0.50),
    (['5d', '3d'], 'OESD missed. Air', 0.15),
    (['Ac', '2c'], 'Bottom pair (2s). Check behind for showdown', 0.18),
]

# Board BD6: 9c 7c 2d Kh (Turn) — Facing Raise, 3-Way Pot
# Hero CO (IP, opener). CO opens, BTN calls, BB defends. Flop 9c 7c 2d:
# CO bets 30, BTN calls, BB calls. Turn Kh: CO bets 60, BB calls, BTN
# raises to 180. Hero faces 120 more.
# villain_positions: BB (non-raiser) then BTN (raiser, LAST)
BD_BOARD_6_BASE = dict(
    board_cards=['9c', '7c', '2d', 'Kh'],
    hero_pos='CO',
    villain_positions=['BB', 'BTN'],   # BTN is raiser (last in list)
    pot=300.0,
    to_call=120.0,
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
        ('turn', 'CO', 'bet'),
        ('turn', 'BB', 'call'),
        ('turn', 'BTN', 'raise'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

BD_BOARD_6_HANDS = [
    (['Kd', 'Qd'], 'Turned TP. BTN raise = very strong. Fold?', 0.35),
    (['Kc', 'Jc'], 'TP + club FD redraw. Call the raise?', 0.40),
    (['9d', '9h'], 'Set of 9s. Re-raise or call and trap?', 0.75),
    (['Ah', 'Ac'], 'AA facing turn raise. Call reluctantly?', 0.45),
    (['Ac', '8c'], 'NFD + Ac blocker. Call draw odds or fold?', 0.30),
    (['7d', '6d'], 'Second pair. Fold to turn raise', 0.15),
    (['Kh', '9d'], 'Turned top two. Call or re-raise?', 0.65),
    (['Td', '8d'], 'OESD (6-7-8-9-T). Paying to draw vs raise', 0.22),
]

# Board BD7: Jh 8d 5c Qc 4h (River) — Medium Board, River Call/Fold
# Hero BTN (IP). HJ opens, BTN calls, BB defends. Flop Jh 8d 5c:
# HJ bets 33, BB calls, BTN calls. Turn Qc: HJ bets 75, BB folds, BTN calls.
# River 4h: HJ bets 100.
# villain_positions: BB (folded) then HJ (bettor, LAST)
BD_BOARD_7_BASE = dict(
    board_cards=['Jh', '8d', '5c', 'Qc', '4h'],
    hero_pos='BTN',
    villain_positions=['HJ'],   # BB folded on turn; HJ is sole remaining villain and bettor
    pot=350.0,
    to_call=100.0,
    street='river',
    action_history=[
        ('preflop', 'HJ', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'HJ', 'bet'),
        ('flop', 'BB', 'call'),
        ('flop', 'BTN', 'call'),
        ('turn', 'BB', 'check'),
        ('turn', 'HJ', 'bet'),
        ('turn', 'BB', 'fold'),
        ('turn', 'BTN', 'call'),
        ('river', 'HJ', 'bet'),
    ],
    opener_position='HJ',
    effective_stack=100.0,
)

BD_BOARD_7_HANDS = [
    (['Jc', 'Tc'], 'Pair of J, was TP on flop. Call 3rd barrel?', 0.35),
    (['Qh', 'Jd'], 'Two pair Q+J. Turned top pair. Call easily', 0.65),
    (['8c', '7c'], 'Pair of 8. Fold to triple barrel', 0.20),
    (['Ah', 'Jh'], 'AJ good kicker on J. Call the river?', 0.40),
    (['9h', '7h'], 'Busted straight draw (5-6-7-8-9 missed). Fold', 0.15),
    (['Qd', 'Td'], 'Turned TP (Q). Hero call or fold 3rd barrel?', 0.50),
    (['5d', '5h'], 'Bottom set. Easy call, consider raise', 0.80),
    (['Kh', 'Kd'], 'KK. Q on turn was scary, call 3rd barrel?', 0.45),
]

# Board BD8: 6h 3d 2h 9c Ks (River) — Low Flop, Scary Runout, River Check
# Hero BB (OOP). CO opens, BTN calls, BB defends. Flop 6h 3d 2h: all check.
# Turn 9c: BB bets 45, CO calls, BTN folds. River Ks: hero to act first.
BD_BOARD_8_BASE = dict(
    board_cards=['6h', '3d', '2h', '9c', 'Ks'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=180.0,
    to_call=0.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
        ('flop', 'CO', 'check'),
        ('flop', 'BTN', 'check'),
        ('turn', 'BB', 'bet'),
        ('turn', 'CO', 'call'),
        ('turn', 'BTN', 'fold'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

BD_BOARD_8_HANDS = [
    (['6c', '5c'], 'Pair of 6. Was value on turn, river K scary. Check?', 0.30),
    (['9h', '8h'], 'Pair of 9. Turn top pair, river K scares. Bet or check?', 0.45),
    (['Ah', '4h'], 'NFD missed (hearts). Busted draw. Bluff river K?', 0.20),
    (['Kd', 'Jd'], 'Rivered TP (K). Value bet the river?', 0.55),
    (['2c', '2d'], 'Bottom set. River K changes nothing, value bet', 0.75),
    (['7h', '5h'], 'Busted FD + gutshot. River bluff?', 0.15),
    (['9d', 'Td'], 'Pair of 9 + T kicker. Bet again or check-call?', 0.42),
    (['Qc', 'Jc'], 'Overcards. River K = give up or bluff?', 0.12),
]

# Board BD9: Qh 9h 4d Th (Turn) — Flush Completed, Action-Heavy
# Hero SB (OOP, sandwich). CO opens, BTN calls, SB calls. Flop Qh 9h 4d:
# all check. Turn Th: CO checks, BTN bets 45.
# villain_positions: CO (non-bettor) then BTN (bettor, LAST)
BD_BOARD_9_BASE = dict(
    board_cards=['Qh', '9h', '4d', 'Th'],
    hero_pos='SB',
    villain_positions=['CO', 'BTN'],   # BTN is bettor (last in list)
    pot=180.0,
    to_call=45.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'),
        ('preflop', 'BTN', 'call'),
        ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'),
        ('flop', 'CO', 'check'),
        ('flop', 'BTN', 'check'),
        ('turn', 'SB', 'check'),
        ('turn', 'CO', 'check'),
        ('turn', 'BTN', 'bet'),
    ],
    opener_position='CO',
    effective_stack=100.0,
)

BD_BOARD_9_HANDS = [
    (['Ah', 'Kh'], 'Nut flush. Raise or slowplay the turn bet?', 0.85),
    (['Kh', 'Jh'], '2nd nut flush. Raise or call?', 0.75),
    (['Qd', 'Jd'], 'TP on flush board. Call or fold in sandwich?', 0.30),
    (['9c', '8c'], 'Second pair on scary board. Fold', 0.15),
    (['Jh', '8h'], 'Low flush. Call, raise risks being dominated', 0.65),
    (['Ad', 'Kd'], 'AK no hearts. Overcards but flush-heavy board', 0.18),
    (['Tc', '9d'], 'Turned two pair. But flush board, call or fold?', 0.40),
    (['7h', '6h'], 'Bottom flush. Vulnerable, call', 0.55),
    (['Ah', '5d'], 'Ah single heart. Blocker to nut flush, bluff raise?', 0.15),
]

BD_BOARDS = [
    (BD_BOARD_1_BASE, BD_BOARD_1_HANDS, 'BD_Board1_AcKd7h'),
    (BD_BOARD_2_BASE, BD_BOARD_2_HANDS, 'BD_Board2_5d5c9hJd'),
    (BD_BOARD_3_BASE, BD_BOARD_3_HANDS, 'BD_Board3_Td8c3h6s'),
    (BD_BOARD_4_BASE, BD_BOARD_4_HANDS, 'BD_Board4_Kh9d4c2sJc'),
    (BD_BOARD_5_BASE, BD_BOARD_5_HANDS, 'BD_Board5_7h4d2cQd9s'),
    (BD_BOARD_6_BASE, BD_BOARD_6_HANDS, 'BD_Board6_9c7c2dKh'),
    (BD_BOARD_7_BASE, BD_BOARD_7_HANDS, 'BD_Board7_Jh8d5cQc4h'),
    (BD_BOARD_8_BASE, BD_BOARD_8_HANDS, 'BD_Board8_6h3d2h9cKs'),
    (BD_BOARD_9_BASE, BD_BOARD_9_HANDS, 'BD_Board9_Qh9h4dTh'),
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
    for base, hands, board_id in SB_BOARDS:
        all_boards.append((base, hands, board_id, 'SB'))
    for base, hands, board_id in FB_BOARDS:
        all_boards.append((base, hands, board_id, 'FB'))
    for base, hands, board_id in OC_BOARDS:
        all_boards.append((base, hands, board_id, 'OC'))
    for base, hands, board_id in TV_BOARDS:
        all_boards.append((base, hands, board_id, 'TV'))
    for base, hands, board_id in BD_BOARDS:
        all_boards.append((base, hands, board_id, 'BD'))

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
            # River hands with no pair can legitimately have raw_equity=0.0
            # (high card vs two opponents' ranges). The SUSPICIOUS check is
            # for catching invalid seat names, not for rejecting air on river.
            if errors:
                is_river_zero_equity = (
                    spec.street == 'river'
                    and feat_dict.get('raw_equity', -1) == 0.0
                    and all('SUSPICIOUS: raw_equity=0.0' in e for e in errors)
                )
                if is_river_zero_equity:
                    print(f"  WARN  h{i+1} {cards}: river zero-equity (accepted)")
                else:
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
            # ANOMALY-A fix: normalise street/hero_position at serialisation.
            f.write(json.dumps(normalise_situation(sit)) + '\n')

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
