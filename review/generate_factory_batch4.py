"""
Generate all 104 BET-context situations from design agent outputs through
SituationFactory, validate each, and write results to:
  training-data/factory_batch4_situations.jsonl

Source documents consumed:
  BOARD_ALLOCATION_V4_BET.md  (25 board definitions — B4_01 through B4_25)
  DESIGN_AGENT_A_BP1_BP2.md   (BP1 x30, BP2 x12)
  DESIGN_AGENT_B_BP3_BP4.md   (BP3 x20 designed, reduced to 19 after fixes; BP4 x15)
  DESIGN_AGENT_C_BP5_BP6.md   (BP5 x12, BP6 x15)
  comms/BATCH4_DESIGN_ISSUES_CONSOLIDATED_2026-04-09.md (fixes applied inline)

Critical fixes incorporated from consolidation doc:
  1. B4_24 corrected to ['6c', '3d', '2h'] (rainbow) — was ['6s', '3d', '2s']
  2. BP3 sits 1-2, 6 (B4_07, rainbow hcr=11) reassigned to two-tone Q+ boards
  3. BP3 sits 3, 7 (B4_08, rainbow hcr=10) reassigned to two-tone Q+ boards
  4. BP3 4A ALL situations moved to two-tone boards (draw_outs>=12 requires FD+SD)
  5. BP3 sit 18 (villain_air=0.38, fails 4D gate) moved to BP6-H (sit 16)
  6. BP6 total becomes 16; BP3 total becomes 19; overall total stays 104

All situations: to_call = 0.0 (defining feature of BET-context batch).

DO NOT RUN until reviewed. See review/comms/ for delivery note.

Run from any directory:
    python3 /home/rupertbeytell/river-rats-v2/review/generate_factory_batch4.py
"""

import sys
import os
import json

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_CORE = os.path.join(_REPO, 'river-rats-core')
sys.path.insert(0, _CORE)
os.chdir(_CORE)

from situation_factory import SituationSpec, build_situation, validate_situation, normalise_situation

OUTPUT_PATH = os.path.join(_REPO, 'training-data', 'factory_batch4_situations.jsonl')

# =============================================================================
# BOARD BASES (B4_01 – B4_25)
#
# All boards: to_call=0.0 (hero acts without facing a bet — check/bet decision).
#
# villain_positions: all active opponents. None are bettors (to_call=0).
# For OOP hero: hero_pos is listed first in postflop order (e.g. BB, SB).
# For IP hero: hero_pos is BTN or CO (acts last).
#
# opener_position: preflop raiser. For is_preflop_aggressor=1 hero, this is
#   hero_pos. For non-PFA hero, this is the villain opener.
#
# SPR notes (per BOARD_ALLOCATION_V4_BET.md Section 3 SPR table):
#   Flop standard:    pot=90, effective_stack=970, SPR=10.8
#   Turn BP1/BP2:     pot=90, effective_stack=540, SPR=6.0  (B4_13 uses 495/5.5 per sit)
#   Turn BP1 B4_16:   pot=90, effective_stack=495, SPR=5.5
#   Turn BP1 B4_14:   pot=90, effective_stack=495, SPR=5.5
#   Turn BP3/BP4 B4_14/B4_16: pot=90, effective_stack=540, SPR=6.0
#   Turn BP4 B4_15:   pot=90, effective_stack=585, SPR=6.5
#   Turn BP5 B4_17:   pot=90, effective_stack=630, SPR=7.0
#   River BP6-C B4_20: pot=270, effective_stack=700, SPR=2.6
# =============================================================================

# ---------------------------------------------------------------------------
# FLOP BOARDS — IP PFA (BP1 / BP2 / BP3 / BP4)
# ---------------------------------------------------------------------------

B4_01 = dict(
    board_cards=['Ad', 'Tc', '4h'],
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
    effective_stack=970.0,
)

B4_02 = dict(
    board_cards=['Ks', 'Jh', '3c'],
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
    effective_stack=970.0,
)

# B4_02 OOP variant — used for BP2: HJ opener, CO cold-calls. HJ acts first (OOP).
B4_02_OOP = dict(
    board_cards=['Ks', 'Jh', '3c'],
    hero_pos='HJ',
    villain_positions=['CO'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'),
        ('flop', 'HJ', 'check'),
    ],
    opener_position='HJ',
    effective_stack=970.0,
)

# B4_03 — OOP only (CO opens, BTN cold-calls, BB calls; CO acts after BB on flop)
B4_03 = dict(
    board_cards=['Ah', '8s', '3d'],
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
    effective_stack=970.0,
)

B4_04 = dict(
    board_cards=['Kd', '6c', '2s'],
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
    effective_stack=970.0,
)

# B4_04 OOP variant — CO opens, BTN cold-calls. CO acts first (OOP).
B4_04_OOP = dict(
    board_cards=['Kd', '6c', '2s'],
    hero_pos='CO',
    villain_positions=['BTN'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
        ('flop', 'CO', 'check'),
    ],
    opener_position='CO',
    effective_stack=970.0,
)

B4_05 = dict(
    board_cards=['Qs', '9c', '5h'],
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
    effective_stack=970.0,
)

# B4_05 non-PFA variant — BTN opens, CO cold-calls. CO hero acts after BTN check.
# Used for BP4 sits 10-11.
B4_05_NPFA = dict(
    board_cards=['Qs', '9c', '5h'],
    hero_pos='CO',
    villain_positions=['BB', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'BTN', 'check'),
    ],
    opener_position='BTN',
    effective_stack=970.0,
)

B4_06 = dict(
    board_cards=['Qd', 'Jd', '5c'],
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
    effective_stack=970.0,
)

# B4_07 — Rainbow J-high. NOTE: used for BP1 only.
# BP3 4A sits that were designed for B4_07 are REASSIGNED to two-tone boards below
# because B4_07 hcr=11 < 12 (fails Step 4 gate) AND rainbow boards cannot produce
# frontdoor flush draws (draw_outs >= 12 requires FD + OESD combo).
B4_07 = dict(
    board_cards=['Jc', '9h', '7s'],
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
    effective_stack=970.0,
)

# B4_08 — Rainbow T-high. Used for BP1 Tier 3 only.
# BP3 4A sits originally designed for B4_08 are REASSIGNED — hcr=10 < 12 gate.
B4_08 = dict(
    board_cards=['Tc', '8h', '5s'],
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
    effective_stack=970.0,
)

# B4_09 — Two-tone spades (Ks 7s 6d). Primary board for BP3 4B/4C NFD semi-bluff.
# hcr=13 satisfies Step 4 gate. Flush suit = spades.
B4_09 = dict(
    board_cards=['Ks', '7s', '6d'],
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
    effective_stack=970.0,
)

# B4_10 — Two-tone hearts (Qh 9s 8h). Primary board for BP3 4A combo draw.
# hcr=12 satisfies Step 4 gate. Flush suit = hearts.
B4_10 = dict(
    board_cards=['Qh', '9s', '8h'],
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
    effective_stack=970.0,
)

# ---------------------------------------------------------------------------
# FLOP BOARDS — OOP non-PFA (BP5)
# ---------------------------------------------------------------------------

B4_11 = dict(
    board_cards=['8c', '4s', '2d'],
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
    effective_stack=970.0,
)

B4_12 = dict(
    board_cards=['9d', '5s', '2c'],
    hero_pos='BB',
    villain_positions=['HJ', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'HJ', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'),
    ],
    opener_position='HJ',
    effective_stack=970.0,
)

# ---------------------------------------------------------------------------
# TURN BOARDS (B4_13 – B4_17)
# ---------------------------------------------------------------------------

# B4_13 — Turn: Ad 7c 2s Kh. IP PFA (BTN) or OOP PFA (CO) depending on variant.
# BP1 turn: BTN hero, SPR 6.0, effective_stack=540.
# BP6-H turn (OOP CO): CO hero, SPR 6.0.
B4_13_BTN = dict(
    board_cards=['Ad', '7c', '2s', 'Kh'],
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
    effective_stack=540.0,   # SPR 6.0 — turn depth
)

# B4_13 OOP variant — CO opens, BTN cold-calls. CO is OOP to BTN on turn.
# Used for BP6-H (villain_air=0.38 near-miss on Step 3B).
B4_13_CO_OOP = dict(
    board_cards=['Ad', '7c', '2s', 'Kh'],
    hero_pos='CO',
    villain_positions=['BTN'],
    pot=90.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
        ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'CO', 'check'),
    ],
    opener_position='CO',
    effective_stack=540.0,   # SPR 6.0
)

# B4_14 — Two-tone spades (Kc 9s 4c Qs). Turn. IP BTN. BP3 4B/4C + BP1.
B4_14 = dict(
    board_cards=['Kc', '9s', '4c', 'Qs'],
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
    effective_stack=495.0,   # SPR 5.5 — turn depth for BP1/BP3
)

# B4_14 BP3-specific: same cards, effective_stack=540 for SPR=6.0 (BP3 turn semi-bluff)
B4_14_BP3 = dict(
    board_cards=['Kc', '9s', '4c', 'Qs'],
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
    effective_stack=540.0,   # SPR 6.0 — BP3 semi-bluff uses 6.0
)

# B4_15 — Two-tone spades (Js 6s 2d 8c). Turn. IP BTN / CO non-PFA (BP4).
# BTN hero cold-called CO; villain is BB.
B4_15_BTN = dict(
    board_cards=['Js', '6s', '2d', '8c'],
    hero_pos='BTN',
    villain_positions=['BB', 'CO'],
    pot=90.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'BB', 'check'), ('turn', 'CO', 'check'),
    ],
    opener_position='CO',
    effective_stack=585.0,   # SPR 6.5
)

# B4_15 CO variant — HJ opens, CO cold-calls, SB calls. CO is IP to SB.
B4_15_CO = dict(
    board_cards=['Js', '6s', '2d', '8c'],
    hero_pos='CO',
    villain_positions=['SB', 'HJ'],
    pot=90.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'HJ', 'check'), ('flop', 'CO', 'check'),
        ('turn', 'SB', 'check'), ('turn', 'HJ', 'check'),
    ],
    opener_position='HJ',
    effective_stack=585.0,   # SPR 6.5
)

# B4_16 — Two-tone diamonds (Qc 7d 3h Kd). Turn. BP4 CO non-PFA / BP1 BTN PFA variant.
# BP4 sits 7-9: CO cold-called HJ; BB capped defender.
B4_16_CO = dict(
    board_cards=['Qc', '7d', '3h', 'Kd'],
    hero_pos='CO',
    villain_positions=['BB', 'HJ'],
    pot=90.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'HJ', 'check'), ('flop', 'CO', 'check'),
        ('turn', 'BB', 'check'), ('turn', 'HJ', 'check'),
    ],
    opener_position='HJ',
    effective_stack=540.0,   # SPR 6.0
)

# B4_16 BTN variant — CO opens, BTN cold-calls, SB calls. BP4 sits 14-15.
B4_16_BTN = dict(
    board_cards=['Qc', '7d', '3h', 'Kd'],
    hero_pos='BTN',
    villain_positions=['SB', 'CO'],
    pot=90.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'SB', 'call'),
        ('flop', 'SB', 'check'), ('flop', 'CO', 'check'), ('flop', 'BTN', 'check'),
        ('turn', 'SB', 'check'), ('turn', 'CO', 'check'),
    ],
    opener_position='CO',
    effective_stack=540.0,   # SPR 6.0
)

# B4_16 as IP PFA — for BP1 sits 23-24. Hero is the HJ opener, acting last on turn.
# HJ opens, CO cold-calls, BB calls. HJ is OOP... wait: per allocation table,
# BP1_23/24 use B4_16 with hero as CO (PFA acting last).
# BOARD_ALLOCATION doc: B4_16 opener_position=HJ, hero=CO cold-caller for BP4.
# BP1 uses B4_16 with hero_pos=CO as PFA? No: BP1 requires is_preflop_aggressor=1.
# Design agent A uses Kc Qh and Ks Jc on B4_16 — hero is CO (PFA) turn c-bet.
# But CO cold-calls HJ in BP4. For BP1: must use a structure where CO IS the opener.
# Use: CO opens, BTN calls, BB calls. CO acts last among checked-through positions.
B4_16_CO_PFA = dict(
    board_cards=['Qc', '7d', '3h', 'Kd'],
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
    effective_stack=495.0,   # SPR 5.5 — BP1 turn
)

# B4_16 for BP6-H (sits 14-15): CO cold-called HJ, villain_air=0.29 near-miss.
# Same structure as B4_16_CO but effective_stack=540 (SPR=6.0).
B4_16_BP6H = dict(
    board_cards=['Qc', '7d', '3h', 'Kd'],
    hero_pos='CO',
    villain_positions=['BB', 'HJ'],
    pot=90.0,
    to_call=0.0,
    street='turn',
    action_history=[
        ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'HJ', 'check'), ('flop', 'CO', 'check'),
        ('turn', 'BB', 'check'), ('turn', 'HJ', 'check'),
    ],
    opener_position='HJ',
    effective_stack=540.0,   # SPR 6.0
)

# B4_17 — Rainbow low turn (8d 4h 2s 9c). OOP SB non-PFA. BP5 turn.
B4_17 = dict(
    board_cards=['8d', '4h', '2s', '9c'],
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
    effective_stack=630.0,   # SPR 7.0 — BP5 turn
)

# ---------------------------------------------------------------------------
# BP6 DEDICATED BOARDS
# ---------------------------------------------------------------------------

# B4_18 — Two-tone hearts (Th 9d 8h). Tier 4 connectivity=9. BP6-A, BP6-D only.
B4_18 = dict(
    board_cards=['Th', '9d', '8h'],
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
    effective_stack=970.0,
)

# B4_18 CO variant — for BP6-D sit 9 (CO hero, IP, TPTK still fails Tier 4).
B4_18_CO = dict(
    board_cards=['Th', '9d', '8h'],
    hero_pos='CO',
    villain_positions=['BB', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'check'),
    ],
    opener_position='CO',
    effective_stack=970.0,
)

# B4_19 — Rainbow very low (5h 3c 2d). BP6-B only.
B4_19 = dict(
    board_cards=['5h', '3c', '2d'],
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
    effective_stack=970.0,
)

# B4_20 — River board (Kc Jh 7d 3s 9s). BP6-C only. Multi-street action.
B4_20 = dict(
    board_cards=['Kc', 'Jh', '7d', '3s', '9s'],
    hero_pos='BB',
    villain_positions=['CO', 'BTN'],
    pot=270.0,
    to_call=0.0,
    street='river',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BTN', 'call'), ('flop', 'BB', 'call'),
        ('turn', 'BB', 'check'), ('turn', 'CO', 'bet'), ('turn', 'BTN', 'call'), ('turn', 'BB', 'call'),
        ('river', 'BB', 'check'),
    ],
    opener_position='CO',
    effective_stack=700.0,   # SPR 2.6
)

# B4_21 — Rainbow J-high (Jc 8d 4h). BP6-E (OOP PFA) and BP6-F (IP non-PFA).
# BP6-E: CO opens (OOP to BTN), danger_score~0.38-0.42
B4_21_OOP = dict(
    board_cards=['Jc', '8d', '4h'],
    hero_pos='CO',
    villain_positions=['BB', 'BTN'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'check'),
    ],
    opener_position='CO',
    effective_stack=970.0,
)

# BP6-F: BTN cold-called CO. BTN is IP.
B4_21_BTN = dict(
    board_cards=['Jc', '8d', '4h'],
    hero_pos='BTN',
    villain_positions=['BB', 'CO'],
    pot=90.0,
    to_call=0.0,
    street='flop',
    action_history=[
        ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
        ('flop', 'BB', 'check'), ('flop', 'CO', 'check'),
    ],
    opener_position='CO',
    effective_stack=970.0,
)

# B4_22 — Rainbow very low (7c 4h 2s). BP5 only.
B4_22 = dict(
    board_cards=['7c', '4h', '2s'],
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
    effective_stack=970.0,
)

# B4_23 — Paired fives, A-high (5c 5d Ah). BP1 only.
B4_23 = dict(
    board_cards=['5c', '5d', 'Ah'],
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
    effective_stack=970.0,
)

# B4_24 — Rainbow very low (6c 3d 2h). BP5 (4th board).
# NOTE: corrected from ['6s','3d','2s'] (two-tone) to ['6c','3d','2h'] (rainbow)
# per BATCH4_DESIGN_ISSUES_CONSOLIDATED_2026-04-09.md issue #1.
B4_24 = dict(
    board_cards=['6c', '3d', '2h'],
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
    effective_stack=970.0,
)

# B4_25 — Rainbow very low (6h 2c 4s). BP6-G only. Dedicated monster trap board.
B4_25 = dict(
    board_cards=['6h', '2c', '4s'],
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
    effective_stack=970.0,
)

# =============================================================================
# SITUATIONS LIST
#
# Format: (board_base_dict, hero_cards, description, sub_pattern)
#
# Sub-pattern codes: BP1, BP2, BP3, BP4, BP5, BP6
# All situations: label = BET (sub-patterns BP1-BP5) or CHECK (BP6).
# The label is encoded in the description and sub_pattern for downstream labelling.
# =============================================================================

SITUATIONS = []

# ---------------------------------------------------------------------------
# BP1: IP PFA Value C-Bet (30 situations — BET label)
# is_preflop_aggressor=1, is_ip=1, is_made_hand=1, to_call=0
# Decision tree: Step 3A fires.
# Source: DESIGN_AGENT_A_BP1_BP2.md, sits BP1_01 through BP1_30
# ---------------------------------------------------------------------------

SITUATIONS += [
    # --- Tier 1: B4_01 (Ad Tc 4h) — 5 situations ---
    (B4_01, ['Ah', 'Kc'],
     'BP1_01: TPTK (Ah-Kc) on Ad-Tc-4h. Tier 1 rainbow A-high. IP PFA. '
     'hcat=8, villain_aggr=0, villain_air=0.38, SPR=10.8. Step 3A fires. BET.',
     'BP1'),

    (B4_01, ['As', '5c'],
     'BP1_02: TP weak kicker (As-5c) on Ad-Tc-4h. Tier 1 rainbow A-high. IP PFA. '
     'hcat=6, villain_aggr=0, villain_air=0.38, SPR=10.8. Step 3A fires. BET.',
     'BP1'),

    (B4_01, ['Kh', 'Ks'],
     'BP1_03: Overpair KK on Ad-Tc-4h. Tier 1 rainbow A-high. IP PFA. '
     'hcat=9 (functional OP per allocation table), villain_aggr=1, villain_air=0.38, SPR=10.8. BET.',
     'BP1'),

    (B4_01, ['Ac', 'Jd'],
     'BP1_07: TPTK (Ac-Jd) on Ad-Tc-4h. Tier 1. IP PFA. Reassigned from B4_03 per R2-1. '
     'hcat=8, villain_aggr=0, villain_air=0.38, SPR=10.8. BET.',
     'BP1'),

    (B4_01, ['Ah', 'Ts'],
     'BP1_08: Two pair A-T (Ah-Ts) on Ad-Tc-4h. Tier 1. IP PFA. Reassigned from B4_03 per R2-1. '
     'hcat=10, villain_aggr=0, villain_air=0.38, SPR=10.8. BET.',
     'BP1'),

    # --- Tier 1: B4_02 (Ks Jh 3c) — 3 situations ---
    (B4_02, ['Kh', 'Qc'],
     'BP1_04: TPTK (Kh-Qc) on Ks-Jh-3c. Tier 1 rainbow K-high. IP PFA. '
     'hcat=8, villain_aggr=0, villain_air=0.41, SPR=10.8. BET.',
     'BP1'),

    (B4_02, ['Kd', 'Tc'],
     'BP1_05: TPGK (Kd-Tc) on Ks-Jh-3c. Tier 1. IP PFA. '
     'hcat=7, villain_aggr=0, villain_air=0.41, SPR=10.8. BET.',
     'BP1'),

    (B4_02, ['Kc', '6s'],
     'BP1_06: TP weak kicker (Kc-6s) on Ks-Jh-3c. Tier 1. IP PFA. '
     'hcat=6, villain_aggr=1, villain_air=0.41, SPR=10.8. BET.',
     'BP1'),

    # --- Tier 1: B4_04 (Kd 6c 2s) — 3 situations ---
    (B4_04, ['Kh', 'Qd'],
     'BP1_09: TPTK (Kh-Qd) on Kd-6c-2s. Tier 1 rainbow K-high very dry. IP PFA. '
     'hcat=8, villain_aggr=0, villain_air=0.44, SPR=10.8. BET.',
     'BP1'),

    (B4_04, ['Kc', '8h'],
     'BP1_10: TP weak kicker (Kc-8h) on Kd-6c-2s. Tier 1. IP PFA. '
     'hcat=6, villain_aggr=0, villain_air=0.44, SPR=10.8. BET.',
     'BP1'),

    (B4_04, ['As', 'Ad'],
     'BP1_11: Overpair AA on Kd-6c-2s. Tier 1. IP PFA. '
     'hcat=9, villain_aggr=1, villain_air=0.44, SPR=10.8. BET.',
     'BP1'),

    # --- Tier 1: B4_13 (Ad 7c 2s Kh — turn) — 3 situations ---
    (B4_13_BTN, ['Ac', 'Js'],
     'BP1_12: TPTK (Ac-Js) on Ad-7c-2s-Kh (turn). Tier 1 rainbow A-high dry turn. IP PFA. '
     'hcat=8, villain_aggr=0, villain_air=0.37, SPR=6.0. Step 3A fires. BET.',
     'BP1'),

    (B4_13_BTN, ['Ah', '6d'],
     'BP1_13: TP weak kicker (Ah-6d) on Ad-7c-2s-Kh (turn). Tier 1. IP PFA. '
     'hcat=6, villain_aggr=0, villain_air=0.37, SPR=6.0. BET.',
     'BP1'),

    (B4_13_BTN, ['Kc', 'Ks'],
     'BP1_14: Overpair KK on Ad-7c-2s-Kh (turn). Tier 1. IP PFA. '
     'hcat=9 (functional OP per allocation table), villain_aggr=0, villain_air=0.37, SPR=6.0. BET.',
     'BP1'),

    # --- Tier 2: B4_05 (Qs 9c 5h) — 2 situations ---
    (B4_05, ['Qh', 'Jd'],
     'BP1_15: TPGK (Qh-Jd) on Qs-9c-5h. Tier 2 rainbow Q-high. IP PFA. '
     'hcat=7, villain_aggr=0, villain_air=0.30, SPR=10.8. Step 3A Tier 2 fires. BET.',
     'BP1'),

    (B4_05, ['Kc', 'Ks'],
     'BP1_16: Overpair KK on Qs-9c-5h. Tier 2. IP PFA. '
     'hcat=9, villain_aggr=1, villain_air=0.30, SPR=10.8. BET.',
     'BP1'),

    # --- Tier 2: B4_06 (Qd Jd 5c) — 3 situations ---
    (B4_06, ['Qc', 'Ks'],
     'BP1_17: TPTK (Qc-Ks) on Qd-Jd-5c. Tier 2 two-tone diamonds Q-high. IP PFA. '
     'hcat=8, villain_aggr=0, villain_air=0.32, SPR=10.8. BET.',
     'BP1'),

    (B4_06, ['Qh', 'Ts'],
     'BP1_18: TPGK (Qh-Ts) on Qd-Jd-5c. Tier 2 two-tone. IP PFA. '
     'hcat=7, villain_aggr=0, villain_air=0.32, SPR=10.8. BET.',
     'BP1'),

    (B4_06, ['Ah', 'As'],
     'BP1_19: Overpair AA on Qd-Jd-5c. Tier 2 two-tone. IP PFA. '
     'hcat=9, villain_aggr=1, villain_air=0.32, SPR=10.8. BET.',
     'BP1'),

    # --- Tier 2: B4_07 (Jc 9h 7s) — 3 situations ---
    (B4_07, ['Jd', 'Ts'],
     'BP1_20: TPGK (Jd-Ts) on Jc-9h-7s. Tier 2 rainbow J-high connected. IP PFA. '
     'hcat=7, villain_aggr=0, villain_air=0.30, SPR=10.8. Step 3A connectivity<=6. BET.',
     'BP1'),

    (B4_07, ['Jh', 'Qc'],
     'BP1_21: TPTK (Jh-Qc) on Jc-9h-7s. Tier 2. IP PFA. '
     'hcat=8, villain_aggr=1, villain_air=0.30, SPR=10.8. BET.',
     'BP1'),

    (B4_07, ['Js', '9d'],
     'BP1_22: Two pair J-9 (Js-9d) on Jc-9h-7s. Tier 2/3. IP PFA. '
     'hcat=10, villain_aggr=0, villain_air=0.30, SPR=10.8. BET.',
     'BP1'),

    # --- Tier 2: B4_16 (Qc 7d 3h Kd — turn) — 2 situations ---
    (B4_16_CO_PFA, ['Kc', 'Qh'],
     'BP1_23: TPTK (Kc-Qh) on Qc-7d-3h-Kd (turn). Tier 2 two-tone diamonds K-high. IP PFA. '
     'hcat=8, villain_aggr=0, villain_air=0.38, SPR=5.5. BET.',
     'BP1'),

    (B4_16_CO_PFA, ['Ks', 'Jc'],
     'BP1_24: TPTK (Ks-Jc) on Qc-7d-3h-Kd (turn). Tier 2. IP PFA. '
     'hcat=8, villain_aggr=1, villain_air=0.38, SPR=5.5. BET.',
     'BP1'),

    # --- Tier 3: B4_08 (Tc 8h 5s) — 3 situations ---
    (B4_08, ['Ts', '8d'],
     'BP1_25: Two pair T-8 top (Ts-8d) on Tc-8h-5s. Tier 3 rainbow T-high connected. IP PFA. '
     'hcat=10, villain_aggr=0, villain_air=0.28, SPR=10.8. Step 3A Tier 3: hcat>=10. BET.',
     'BP1'),

    (B4_08, ['Td', '8c'],
     'BP1_26: Two pair T-8 mid (Td-8c) on Tc-8h-5s. Tier 3. IP PFA. '
     'hcat=10, villain_aggr=1, villain_air=0.28, SPR=10.8. BET.',
     'BP1'),

    (B4_08, ['8s', '5d'],
     'BP1_27: Two pair 8-5 bottom (8s-5d) on Tc-8h-5s. Tier 3. IP PFA. '
     'hcat=10, villain_aggr=0, villain_air=0.28, SPR=10.8. BET.',
     'BP1'),

    # --- Tier 2/3: B4_10 (Qh 9s 8h) — 3 situations ---
    (B4_10, ['Qs', '9d'],
     'BP1_28: Two pair Q-9 top (Qs-9d) on Qh-9s-8h. Tier 2/3 two-tone hearts Q-high. IP PFA. '
     'hcat=10, villain_aggr=0, villain_air=0.32, SPR=10.8. BET.',
     'BP1'),

    (B4_10, ['Qd', '8s'],
     'BP1_29: Two pair Q-8 (Qd-8s) on Qh-9s-8h. Tier 2/3. IP PFA. '
     'hcat=10, villain_aggr=1, villain_air=0.32, SPR=10.8. BET.',
     'BP1'),

    (B4_10, ['Qc', 'Jd'],
     'BP1_25b: TPTK (Qc-Jd) on Qh-9s-8h. Tier 2 top pair. IP PFA. '
     'hcat=8, villain_aggr=0, villain_air=0.32, SPR=10.8. BET.',
     'BP1'),

    # --- Tier 1: B4_14 (Kc 9s 4c Qs — turn) — 1 situation ---
    (B4_14, ['Kh', 'Jd'],
     'BP1_29b: TPGK (Kh-Jd) on Kc-9s-4c-Qs (turn). Tier 1/2 two-tone spades. IP PFA. '
     'hcat=7, villain_aggr=0, villain_air=0.38, SPR=5.5. BET.',
     'BP1'),

    # --- Tier 1 paired: B4_23 (5c 5d Ah) — 1 situation ---
    (B4_23, ['Ac', 'Kd'],
     'BP1_30: TPTK (Ac-Kd) on 5c-5d-Ah (paired board). Tier 1 A-high. IP PFA. '
     'hcat=8, villain_aggr=0, villain_air=0.40, SPR=10.8. '
     'Paired board: monster protection dynamics — villain rarely holds 5x. BET.',
     'BP1'),
]

# ---------------------------------------------------------------------------
# BP2: OOP PFA Value C-Bet (12 situations — BET label)
# is_preflop_aggressor=1, is_ip=0, is_made_hand=1, to_call=0,
# villain_aggression_count=0
# Decision tree: Step 3B fires.
# Boards: B4_02 (HJ opener OOP), B4_03 (CO opener OOP), B4_04 (CO opener OOP)
# Source: DESIGN_AGENT_A_BP1_BP2.md, sits BP2_01 through BP2_12
# ---------------------------------------------------------------------------

SITUATIONS += [
    # --- B4_02_OOP (Ks Jh 3c — HJ opens, CO cold-calls) — 3 situations ---
    (B4_02_OOP, ['Kd', 'Ac'],
     'BP2_01: TPTK (Kd-Ac) on Ks-Jh-3c. OOP PFA (HJ). Tier 1 K-high rainbow. '
     'hcat=8, villain_air=0.43, hero_range_pct=0.82, villain_aggr=0, SPR=10.8. '
     'Step 3B: all gates satisfied. BET.',
     'BP2'),

    (B4_02_OOP, ['Kc', 'Qh'],
     'BP2_02: TPGK (Kc-Qh) on Ks-Jh-3c. OOP PFA (HJ). Tier 1. '
     'hcat=7, villain_air=0.43, hero_range_pct=0.76, villain_aggr=0, SPR=10.8. BET.',
     'BP2'),

    (B4_02_OOP, ['Kh', 'Jd'],
     'BP2_03: Two pair K-J (Kh-Jd) on Ks-Jh-3c. OOP PFA (HJ). Tier 1. '
     'hcat=10, villain_air=0.43, hero_range_pct=0.85, villain_aggr=0, SPR=10.8. BET.',
     'BP2'),

    # --- B4_03 (Ah 8s 3d — CO opens, BTN cold-calls) — 4 situations ---
    (B4_03, ['As', 'Kd'],
     'BP2_04: TPTK (As-Kd) on Ah-8s-3d. OOP PFA (CO). Tier 1 A-high rainbow. '
     'hcat=8, villain_air=0.42, hero_range_pct=0.84, villain_aggr=0, SPR=10.8. BET.',
     'BP2'),

    (B4_03, ['Ac', 'Qd'],
     'BP2_05: TPGK (Ac-Qd) on Ah-8s-3d. OOP PFA (CO). Tier 1. '
     'hcat=7, villain_air=0.42, hero_range_pct=0.74, villain_aggr=0, SPR=10.8. BET.',
     'BP2'),

    (B4_03, ['As', '8d'],
     'BP2_06: Two pair A-8 (As-8d) on Ah-8s-3d. OOP PFA (CO). Tier 1. '
     'hcat=10, villain_air=0.42, hero_range_pct=0.86, villain_aggr=0, SPR=10.8. BET.',
     'BP2'),

    (B4_03, ['Kh', 'Kc'],
     'BP2_07: Overpair KK on Ah-8s-3d. OOP PFA (CO). Tier 1. '
     'hcat=9 (functional OP per allocation table), villain_air=0.42, hero_range_pct=0.78, '
     'villain_aggr=0, SPR=10.8. BET.',
     'BP2'),

    # --- B4_04_OOP (Kd 6c 2s — CO opens, BTN cold-calls) — 5 situations ---
    (B4_04_OOP, ['Kh', 'As'],
     'BP2_08: TPTK (Kh-As) on Kd-6c-2s. OOP PFA (CO). Tier 1 K-high rainbow very dry. '
     'hcat=8, villain_air=0.46, hero_range_pct=0.83, villain_aggr=0, SPR=10.8. BET.',
     'BP2'),

    (B4_04_OOP, ['Kc', 'Qd'],
     'BP2_09: TPGK (Kc-Qd) on Kd-6c-2s. OOP PFA (CO). Tier 1. '
     'hcat=7, villain_air=0.46, hero_range_pct=0.75, villain_aggr=0, SPR=10.8. BET.',
     'BP2'),

    (B4_04_OOP, ['Kc', '6h'],
     'BP2_10: Two pair K-6 (Kc-6h) on Kd-6c-2s. OOP PFA (CO). Tier 1. '
     'hcat=10, villain_air=0.46, hero_range_pct=0.87, villain_aggr=0, SPR=10.8. BET.',
     'BP2'),

    (B4_04_OOP, ['Ah', 'Ad'],
     'BP2_11: Overpair AA on Kd-6c-2s. OOP PFA (CO). Tier 1. '
     'hcat=9, villain_air=0.46, hero_range_pct=0.79, villain_aggr=0, SPR=10.8. BET.',
     'BP2'),

    (B4_04_OOP, ['Ks', 'Jh'],
     'BP2_12: TPTK (Ks-Jh) on Kd-6c-2s. OOP PFA (CO). Tier 1. High villain_air variant. '
     'hcat=8, villain_air=0.50, hero_range_pct=0.80, villain_aggr=0, SPR=10.8. BET.',
     'BP2'),
]

# ---------------------------------------------------------------------------
# BP3: PFA Semi-Bluff C-Bet (19 situations — BET label after fixes)
# is_preflop_aggressor=1, is_made_hand=0, to_call=0
# Decision tree: Step 4 (sub-conditions 4A, 4B, 4C, 4D) fires.
# Source: DESIGN_AGENT_B_BP3_BP4.md + consolidated fixes
#
# FIXES APPLIED:
#   - Sits 1-2, 6 (originally B4_07 — rainbow hcr=11) → reassigned to two-tone
#     Q+ boards with new flush-draw hero hands.
#   - Sits 3, 7 (originally B4_08 — rainbow hcr=10) → reassigned to two-tone
#     Q+ boards with new flush-draw hero hands.
#   - All 4A situations must now use two-tone boards (FD required for draw_outs>=12).
#   - Sit 18 (4D, villain_air=0.38 fails Step 4D gate) moved to BP6-H as sit 16.
#   - BP3 total: 19 situations (8x4A + 6x4B + 3x4C + 2x4D remaining).
#
# Board reassignment for originally B4_07/B4_08 4A sits:
#   Sits 1-2, 6 (B4_07 → B4_10): Qh-9s-8h two-tone hearts, hcr=12. Hero draws in hearts.
#   Sits 3, 7   (B4_08 → B4_06): Qd-Jd-5c two-tone diamonds, hcr=12. Hero draws in diamonds.
#   New hero cards designed below to avoid made-hand conflicts on new boards.
# ---------------------------------------------------------------------------

SITUATIONS += [
    # ---
    # 4A: Combo Draw — draw_outs >= 12 (FD + straight draw). 8 situations.
    # ALL on two-tone boards: B4_10 (hearts), B4_09 (spades), B4_06 (diamonds).
    # ---

    # Sit 1 (originally B4_07 → REASSIGNED to B4_10 Qh-9s-8h):
    # Hero: Jh-7d. FD (Jh+Qh+8h = 3 hearts = frontdoor FD). Gutshot to T (7-8-9-T-J needs T).
    # draw_outs ~ 13 (9 FD + 4 gutshot - overlaps). is_made_hand=0: J+7 on Q-9-8 board, no pair.
    # ip=1 (BTN PFA, IP). hcr=12 satisfies Step 4 gate.
    (B4_10, ['Jh', '7d'],
     'BP3_4A_01: Combo draw (Jh-7d) on Qh-9s-8h. FD (hearts: Jh+Qh+8h) + gutshot (7-8-9-T-J needs T). '
     'draw_outs~13, flush_draw_rank=11. is_made_hand=0 (J+7 no pair on Q-9-8). IP PFA. '
     'hcr=12 satisfies Step 4 gate. REASSIGNED from B4_07 (hcr=11). '
     'villain_aggr=0, villain_air=0.40, SPR=10.8. Step 4A fires. BET.',
     'BP3'),

    # Sit 2 (originally B4_07 → REASSIGNED to B4_10 Qh-9s-8h):
    # Hero: Ah-Th. FD (Ah+Th+Qh+8h = 4 hearts). Gutshot: T-9-8 with A on board... actually
    # board has Qh-9s-8h: A+T in hand, board has 8-9-Q. 8-9-T is 3 sequential; need J or 7
    # for a straight. With T in hand and 8-9 on board: T-9-8-7 needs 7 (OESD down-end).
    # T-J-Q-K-A needs J,K,A (too many). J-T-9-8-7 needs J and 7 — too many for hero's hand.
    # Actually OESD: Q-J-T-9-8 (needs J). Hero holds T; board has Q-9-8. J fills Q-J-T-9-8.
    # draw_outs = 9 FD + 4 (to J for Q-J-T-9-8) - 1 Jh overlap = 12.
    (B4_10, ['Ah', 'Th'],
     'BP3_4A_02: Combo draw (Ah-Th) on Qh-9s-8h. FD (hearts: Ah+Th+Qh+8h = 4 hearts, 9 outs) '
     '+ gutshot (Q-J-T-9-8 needs J, 3 non-heart J outs = 3 extra). draw_outs=12. '
     'is_made_hand=0 (A+T no pair on Q-9-8). IP PFA. villain_aggr=1, villain_air=0.40, SPR=10.8. '
     'REASSIGNED from B4_07 (hcr=11). Step 4A fires. BET.',
     'BP3'),

    # Sit 3 (originally B4_08 → REASSIGNED to B4_06 Qd-Jd-5c):
    # Hero: Kd-Tc. FD (Kd+Qd+Jd = 3 diamonds = frontdoor FD, 9 outs).
    # Straight: K+T on Q-J-5 board. K-Q-J-T-9 needs 9 (gutshot). draw_outs = 9 FD + 4 gutshot - overlaps = ~12.
    # is_made_hand=0: K+T no pair on Q-J-5.
    (B4_06, ['Kd', 'Tc'],
     'BP3_4A_03: Combo draw (Kd-Tc) on Qd-Jd-5c. FD (diamonds: Kd+Qd+Jd, 9 outs) '
     '+ gutshot (K-Q-J-T-9 needs 9, 4 outs). draw_outs~12. is_made_hand=0. IP PFA. '
     'REASSIGNED from B4_08 (hcr=10). villain_aggr=0, villain_air=0.35, SPR=10.8. Step 4A fires. BET.',
     'BP3'),

    # Sit 4 (B4_10 original): Jh-7d (same as reassigned sit 1, same board).
    # Design agent B assigned this to B4_10 — already correct. Same hero works.
    # To keep hero cards distinct from sit 1, use Jh-6d instead.
    # Jh: not on board (Qh, 8h on board, no Jh). 6d: not on board. No pair on Q-9-8. is_made_hand=0.
    # FD: Jh+Qh+8h = 3 hearts (frontdoor). Gutshot: 6-7-8-9-J needs 7 (4 outs). draw_outs~13.
    (B4_10, ['Jh', '6d'],
     'BP3_4A_04: Combo draw (Jh-6d) on Qh-9s-8h. FD (hearts: Jh+Qh+8h) + gutshot (6-7-8-9-J needs 7). '
     'draw_outs~13. is_made_hand=0 (J+6 no pair on Q-9-8). IP PFA. '
     'villain_aggr=0, villain_air=0.40, SPR=10.8. Step 4A fires. BET.',
     'BP3'),

    # Sit 5 (B4_10 original): Ah-Th — same as reassigned sit 2. Use distinct hand.
    # Kh-Tc: Kh not on board (Qh, 8h on board). Tc not on board. K+T on Q-9-8: no pair. is_made_hand=0.
    # FD: Kh+Qh+8h = 3 hearts (frontdoor, 9 outs). Straight: K-Q-J-T-9 needs J (4 outs).
    # draw_outs = 9 + 3 (non-heart Js) = 12.
    (B4_10, ['Kh', 'Tc'],
     'BP3_4A_05: Combo draw (Kh-Tc) on Qh-9s-8h. FD (hearts: Kh+Qh+8h, 9 outs) '
     '+ gutshot (K-Q-J-T-9 needs J, ~3 non-heart outs). draw_outs~12. '
     'is_made_hand=0 (K+T no pair on Q-9-8). IP PFA. villain_aggr=1, villain_air=0.40, SPR=10.8. BET.',
     'BP3'),

    # Sit 6 (originally B4_07 OOP → REASSIGNED to B4_10 OOP):
    # OOP hero: HJ opens, CO cold-calls. HJ is OOP to CO. Same board B4_10, same draw structure.
    # Hero: Jh-7d (same as sit 1 IP version — same board, different positional structure is valid).
    # OOP semi-bluff: is_preflop_aggressor=1, is_ip=0.
    (B4_10, ['Jh', '7d'],
     'BP3_4A_06: Combo draw (Jh-7d) on Qh-9s-8h. OOP PFA (HJ opener, CO cold-calls). '
     'FD (hearts) + gutshot. draw_outs~13. is_made_hand=0. REASSIGNED from B4_07 (hcr=11, rainbow). '
     'villain_aggr=0, villain_air=0.40, SPR=10.8. Step 4A fires. BET.',
     'BP3'),

    # Sit 7 (originally B4_08 OOP → REASSIGNED to B4_06 OOP):
    # OOP hero: HJ opens, CO cold-calls. HJ is OOP. Board B4_06 Qd-Jd-5c.
    # Hero: Ad-Tc. FD (Ad+Qd+Jd = 3 diamonds, nut draw, 9 outs). Straight: A-K-Q-J-T-9 needs K+T path...
    # A+T on Q-J-5: A-K-Q-J-T needs K (gutshot to K: 4 outs). draw_outs = 9 + 3 (non-diamond Ks) = 12.
    # is_made_hand=0: A+T no pair on Q-J-5. Not a straight (need K for A-K-Q-J-T).
    (B4_06, ['Ad', 'Tc'],
     'BP3_4A_07: Combo draw (Ad-Tc) on Qd-Jd-5c. OOP PFA (HJ opener, CO cold-calls). '
     'FD (diamonds: Ad+Qd+Jd, 9 outs) + gutshot (A-K-Q-J-T needs K, ~3 non-diamond outs). '
     'draw_outs~12. is_made_hand=0 (A+T no pair on Q-J-5). '
     'REASSIGNED from B4_08 (hcr=10, rainbow). villain_aggr=0, villain_air=0.35, SPR=10.8. BET.',
     'BP3'),

    # Sit 8 (B4_10 OOP original): Jh-Td on Qh-9s-8h OOP.
    # CONFLICT CHECK: J+T on Q-9-8 board: 8-9-T-J-Q = ALL FIVE PRESENT = FLOPPED STRAIGHT.
    # is_made_hand=1. INVALID for BP3. Use Jh-6d (same as sit 4 hero) on OOP structure.
    # Different positional structure makes sit 8 distinct from sit 4.
    (B4_10, ['Jh', '6d'],
     'BP3_4A_08: Combo draw (Jh-6d) on Qh-9s-8h. OOP PFA (HJ opener, CO cold-calls). '
     'FD (hearts: Jh+Qh+8h) + gutshot (6-7-8-9-J needs 7). draw_outs~13. '
     'is_made_hand=0. villain_aggr=0, villain_air=0.40, SPR=10.8. Step 4A fires. BET.',
     'BP3'),

    # ---
    # 4B: NFD + Blocker — draw_outs >= 9, flush_draw_rank >= 12. 6 situations. IP only.
    # Boards: B4_06 (diamonds), B4_09 (spades), B4_14 (spades turn)
    # ---

    (B4_06, ['Kd', 'Tc'],
     'BP3_4B_09: NFD+blocker (Kd-Tc) on Qd-Jd-5c. FD (Kd+Qd+Jd, 9 outs). '
     'flush_draw_rank=13 (K). flush_block_pct>0 (Kd blocks KdXd villain combos). '
     'is_made_hand=0 (K+T no pair on Q-J-5). IP PFA. villain_aggr=0, villain_air=0.35, SPR=10.8. BET.',
     'BP3'),

    (B4_06, ['Ad', 'Th'],
     'BP3_4B_10: NFD+blocker (Ad-Th) on Qd-Jd-5c. FD (Ad+Qd+Jd, 9 outs). '
     'flush_draw_rank=14 (A). flush_block_pct>0 (Ad blocks AdXd villain combos). '
     'is_made_hand=0 (A+T no pair on Q-J-5). IP PFA. villain_aggr=1, villain_air=0.38, SPR=10.8. BET.',
     'BP3'),

    (B4_09, ['As', 'Tc'],
     'BP3_4B_11: NFD+blocker (As-Tc) on Ks-7s-6d. FD (As+Ks+7s, 9 outs). '
     'flush_draw_rank=14 (A). flush_block_pct>0 (As blocks AsXs villain combos). '
     'is_made_hand=0 (A+T no pair on K-7-6). IP PFA. villain_aggr=0, villain_air=0.40, SPR=10.8. BET.',
     'BP3'),

    (B4_09, ['Qs', 'Jh'],
     'BP3_4B_12: NFD+blocker (Qs-Jh) on Ks-7s-6d. FD (Qs+Ks+7s, 9 outs). '
     'flush_draw_rank=12 (Q). flush_block_pct>0 (Qs blocks QsXs villain combos). '
     'draw_outs~13 (9 FD + gutshot K-Q-J-T needs T). is_made_hand=0. IP PFA. '
     'villain_aggr=1, villain_air=0.38, SPR=10.8. BET.',
     'BP3'),

    (B4_14_BP3, ['As', 'Jh'],
     'BP3_4B_13: NFD+blocker (As-Jh) on Kc-9s-4c-Qs (turn). FD (As+9s+Qs, 9 outs). '
     'flush_draw_rank=14 (A). flush_block_pct>0 (As blocks AsXs villain combos). '
     'draw_outs~12 (9 FD + 3 non-spade T outs for K-Q-J-T-9). is_made_hand=0. IP PFA. '
     'villain_aggr=0, villain_air=0.40, SPR=6.0. BET.',
     'BP3'),

    (B4_14_BP3, ['As', 'Jc'],
     'BP3_4B_14: NFD+blocker (As-Jc) on Kc-9s-4c-Qs (turn). FD (As+9s+Qs, 9 outs). '
     'flush_draw_rank=14 (A). flush_block_pct>0 (As blocks AsXs; Jc also blocks JcXc combos). '
     'draw_outs~12. is_made_hand=0. IP PFA. villain_aggr=1, villain_air=0.40, SPR=6.0. BET.',
     'BP3'),

    # ---
    # 4C: Nut Draw + Board Favour — draw_outs >= 9, flush_draw_rank >= 13. 3 situations. IP only.
    # ---

    (B4_09, ['As', '9h'],
     'BP3_4C_15: Nut draw + board_favour (As-9h) on Ks-7s-6d. FD (As+Ks+7s, 9 outs). '
     'flush_draw_rank=14 (A). board_favour=0.38 (BTN PFA range advantage on K-high). '
     'is_made_hand=0 (A+9 no pair on K-7-6). IP PFA. villain_aggr=0, villain_air=0.40, SPR=10.8. BET.',
     'BP3'),

    (B4_14_BP3, ['As', 'Jh'],
     'BP3_4C_16: Nut draw + board_favour (As-Jh) on Kc-9s-4c-Qs (turn). FD (As+9s+Qs, 9 outs). '
     'flush_draw_rank=14 (A). board_favour=0.35. is_made_hand=0. IP PFA. '
     'villain_aggr=0, villain_air=0.40, SPR=6.0. '
     'NOTE: same hero cards as 4B sit 13 — distinct sub-condition (board_favour discriminates). BET.',
     'BP3'),

    (B4_06, ['Ad', 'Th'],
     'BP3_4C_17: Nut draw + board_favour (Ad-Th) on Qd-Jd-5c. FD (Ad+Qd+Jd, 9 outs). '
     'flush_draw_rank=14 (A). board_favour=0.32. is_made_hand=0 (A+T no pair on Q-J-5). IP PFA. '
     'villain_aggr=0, villain_air=0.38, SPR=10.8. '
     'NOTE: same hero as 4B sit 10 — distinct sub-condition (board_favour). BET.',
     'BP3'),

    # ---
    # 4D: Blocker + Weak Draw — 2 situations remaining (sit 18 moved to BP6-H).
    # flush_block_pct > 0, draw_outs >= 4 (gutshot). villain_air >= 0.40.
    # ip=1, high_card_rank >= 13, is_rainbow=1. All flop IP.
    # ---

    (B4_04, ['Ah', 'Qd'],
     'BP3_4D_19: Blocker+weak draw (Ah-Qd) on Kd-6c-2s. Ah blocks Ax combos (flush_block_pct>0). '
     'Gutshot: A-K-Q-J-T needs J (4 outs). is_made_hand=0 (A+Q no pair on K-6-2). '
     'is_rainbow=1, hcr=13. IP PFA. villain_aggr=0, villain_air=0.44, SPR=10.8. Step 4D fires. BET.',
     'BP3'),

    (B4_03, ['Kh', 'Jd'],
     'BP3_4D_20: Blocker+weak draw (Kh-Jd) on Ah-8s-3d. Kh blocks KhXh combos (flush_block_pct>0). '
     'Gutshot: A-K-Q-J-T needs Q (4 outs). is_made_hand=0 (K+J no pair on A-8-3). '
     'is_rainbow=1, hcr=14. IP PFA. villain_aggr=0, villain_air=0.40, SPR=10.8. Step 4D fires. BET.',
     'BP3'),
]

# ---------------------------------------------------------------------------
# BP4: IP Thin Value Non-PFA (15 situations — BET label)
# is_preflop_aggressor=0, is_ip=1, is_made_hand=1
# villain_range_capped=1, danger_score<=0.35, villain_aggression_count<=1
# Decision tree: Step 5 fires.
# Boards: B4_05, B4_15, B4_16
# Source: DESIGN_AGENT_B_BP3_BP4.md, sits 1-15
# ---------------------------------------------------------------------------

SITUATIONS += [
    # --- B4_05 (Qs 9c 5h — Q-high rainbow flop). BTN cold-called CO. BB capped defender. ---
    (B4_05, ['Qh', 'Kd'],
     'BP4_01: TPGK (Qh-Kd) on Qs-9c-5h. IP non-PFA (BTN cold-called CO). '
     'villain_range_capped=1 (BB). hcat=7, danger_score=0.15, villain_top_pp_pct=0.22. '
     'villain_aggr=0, SPR=10.8. Step 5 fires. BET.',
     'BP4'),

    (B4_05, ['Qd', 'Ah'],
     'BP4_02: TPTK (Qd-Ah) on Qs-9c-5h. IP non-PFA (BTN cold-called CO). '
     'villain_range_capped=1. hcat=8, danger_score=0.15, villain_top_pp_pct=0.22. '
     'villain_aggr=0, SPR=10.8. BET.',
     'BP4'),

    (B4_05, ['Kh', 'Kc'],
     'BP4_03: Overpair KK on Qs-9c-5h. IP non-PFA (BTN cold-called CO). '
     'villain_range_capped=1. hcat=9, danger_score=0.15, villain_top_pp_pct=0.22. '
     'villain_aggr=1, SPR=10.8. BET.',
     'BP4'),

    # --- B4_15_BTN (Js 6s 2d 8c — J-high turn). BTN cold-called CO. BB capped. SPR=6.5 ---
    (B4_15_BTN, ['Jd', 'Th'],
     'BP4_04: TPGK (Jd-Th) on Js-6s-2d-8c (turn). IP non-PFA (BTN cold-called CO). '
     'villain_range_capped=1 (BB). hcat=7, danger_score=0.18, villain_top_pp_pct=0.20. '
     'villain_aggr=0, SPR=6.5. BET.',
     'BP4'),

    (B4_15_BTN, ['Jh', 'Ac'],
     'BP4_05: TPTK (Jh-Ac) on Js-6s-2d-8c (turn). IP non-PFA (BTN cold-called CO). '
     'villain_range_capped=1. hcat=8, danger_score=0.18, villain_top_pp_pct=0.20. '
     'villain_aggr=0, SPR=6.5. BET.',
     'BP4'),

    (B4_15_BTN, ['Jc', '8d'],
     'BP4_06: Two pair J-8 (Jc-8d) on Js-6s-2d-8c (turn). IP non-PFA (BTN cold-called CO). '
     'villain_range_capped=1. hcat=10, danger_score=0.18, villain_top_pp_pct=0.20. '
     'villain_aggr=1, SPR=6.5. BET.',
     'BP4'),

    # --- B4_16_CO (Qc 7d 3h Kd — K-high turn). CO cold-called HJ. BB capped. SPR=6.0 ---
    (B4_16_CO, ['Kh', 'Jc'],
     'BP4_07: TPGK (Kh-Jc) on Qc-7d-3h-Kd (turn). IP non-PFA (CO cold-called HJ). '
     'villain_range_capped=1 (BB). hcat=7, danger_score=0.10, villain_top_pp_pct=0.18. '
     'villain_aggr=0, SPR=6.0. BET.',
     'BP4'),

    (B4_16_CO, ['Ks', 'Ah'],
     'BP4_08: TPTK (Ks-Ah) on Qc-7d-3h-Kd (turn). IP non-PFA (CO cold-called HJ). '
     'villain_range_capped=1. hcat=8, danger_score=0.10, villain_top_pp_pct=0.18. '
     'villain_aggr=0, SPR=6.0. BET.',
     'BP4'),

    (B4_16_CO, ['Ac', 'Ad'],
     'BP4_09: Overpair AA on Qc-7d-3h-Kd (turn). IP non-PFA (CO cold-called HJ). '
     'villain_range_capped=1. hcat=9, danger_score=0.10, villain_top_pp_pct=0.18. '
     'villain_aggr=1, SPR=6.0. BET.',
     'BP4'),

    # --- B4_05_NPFA (Qs 9c 5h). CO cold-called BTN. HJ cold-call = capped villain. SPR=10.8 ---
    (B4_05_NPFA, ['Qc', 'Jd'],
     'BP4_10: TPGK (Qc-Jd) on Qs-9c-5h. IP non-PFA (CO cold-called BTN). '
     'villain_range_capped=1 (HJ). hcat=7, danger_score=0.15, villain_top_pp_pct=0.25. '
     'villain_aggr=0, SPR=10.8. BET.',
     'BP4'),

    (B4_05_NPFA, ['Qh', 'As'],
     'BP4_11: TPTK (Qh-As) on Qs-9c-5h. IP non-PFA (CO cold-called BTN). '
     'villain_range_capped=1 (HJ). hcat=8, danger_score=0.15, villain_top_pp_pct=0.25. '
     'villain_aggr=1, SPR=10.8. BET.',
     'BP4'),

    # --- B4_15_CO (Js 6s 2d 8c — turn). CO cold-called HJ. SB cold-call = capped. SPR=6.5 ---
    (B4_15_CO, ['Jd', 'Qh'],
     'BP4_12: TPGK (Jd-Qh) on Js-6s-2d-8c (turn). IP non-PFA (CO cold-called HJ). '
     'villain_range_capped=1 (SB). hcat=7, danger_score=0.22, villain_top_pp_pct=0.28. '
     'villain_aggr=0, SPR=6.5. BET.',
     'BP4'),

    (B4_15_CO, ['Jh', '8h'],
     'BP4_13: Two pair J-8 (Jh-8h) on Js-6s-2d-8c (turn). IP non-PFA (CO cold-called HJ). '
     'villain_range_capped=1 (SB). hcat=10, danger_score=0.22, villain_top_pp_pct=0.28. '
     'villain_aggr=1, SPR=6.5. BET.',
     'BP4'),

    # --- B4_16_BTN (Qc 7d 3h Kd — turn). BTN cold-called CO. SB cold-call = capped. SPR=6.0 ---
    (B4_16_BTN, ['Kc', 'Jh'],
     'BP4_14: TPGK (Kc-Jh) on Qc-7d-3h-Kd (turn). IP non-PFA (BTN cold-called CO). '
     'villain_range_capped=1 (SB). hcat=7, danger_score=0.12, villain_top_pp_pct=0.20. '
     'villain_aggr=0, SPR=6.0. BET.',
     'BP4'),

    (B4_16_BTN, ['Ah', 'As'],
     'BP4_15: Overpair AA on Qc-7d-3h-Kd (turn). IP non-PFA (BTN cold-called CO). '
     'villain_range_capped=1 (SB). hcat=9, danger_score=0.12, villain_top_pp_pct=0.20. '
     'villain_aggr=1, SPR=6.0. BET.',
     'BP4'),
]

# ---------------------------------------------------------------------------
# BP5: OOP Value Exception (12 situations — BET label)
# is_ip=0, raw_equity>=0.65, villain_air_pct>=0.45, is_rainbow=1,
# connectivity_score<=3, hand_category>=8, villain_aggression_count=0
# Decision tree: Step 6 fires.
# Boards: B4_11, B4_12, B4_17, B4_22, B4_24
# Source: DESIGN_AGENT_C_BP5_BP6.md, BP5 sits 1-12
# ---------------------------------------------------------------------------

SITUATIONS += [
    # --- B4_11 (8c 4s 2d — low rainbow flop). BB non-PFA. SPR=10.8 ---
    (B4_11, ['8h', '4d'],
     'BP5_01: Two pair 8-4 (8h-4d) on 8c-4s-2d. OOP non-PFA (BB). '
     'hcat=10, raw_equity=0.70, villain_air=0.48, villain_fold_eq=0.40. '
     'is_rainbow=1, connectivity=2. villain_aggr=0, SPR=10.8. Step 6 fires. BET.',
     'BP5'),

    (B4_11, ['8s', '2h'],
     'BP5_02: Two pair 8-2 (8s-2h) on 8c-4s-2d. OOP non-PFA (BB). '
     'hcat=10, raw_equity=0.68, villain_air=0.48, villain_fold_eq=0.38. '
     'is_rainbow=1, connectivity=2. villain_aggr=0, SPR=10.8. BET.',
     'BP5'),

    (B4_11, ['4c', '4d'],
     'BP5_03: Set of fours (4c-4d) on 8c-4s-2d. OOP non-PFA (BB). '
     'hcat=11 (trips/set), raw_equity=0.78, villain_air=0.48, villain_fold_eq=0.45. '
     'is_rainbow=1, connectivity=2. villain_aggr=0, SPR=10.8. BET.',
     'BP5'),

    # --- B4_12 (9d 5s 2c — low rainbow flop). BB non-PFA. SPR=10.8 ---
    (B4_12, ['9h', '5d'],
     'BP5_04: Two pair 9-5 (9h-5d) on 9d-5s-2c. OOP non-PFA (BB). '
     'hcat=10, raw_equity=0.71, villain_air=0.50, villain_fold_eq=0.42. '
     'is_rainbow=1, connectivity=2. villain_aggr=0, SPR=10.8. BET.',
     'BP5'),

    (B4_12, ['As', '9c'],
     'BP5_05: TPTK A-9 (As-9c) on 9d-5s-2c. OOP non-PFA (BB). '
     'hcat=8, raw_equity=0.66, villain_air=0.50, villain_fold_eq=0.37. '
     'is_rainbow=1, connectivity=2. villain_aggr=0, SPR=10.8. BET.',
     'BP5'),

    (B4_12, ['9s', '9h'],
     'BP5_06: Set of nines (9s-9h) on 9d-5s-2c. OOP non-PFA (BB). '
     'hcat=11 (trips/set), raw_equity=0.79, villain_air=0.50, villain_fold_eq=0.48. '
     'is_rainbow=1, connectivity=2. villain_aggr=0, SPR=10.8. BET.',
     'BP5'),

    # --- B4_17 (8d 4h 2s 9c — low rainbow turn). SB non-PFA. SPR=7.0 ---
    (B4_17, ['9h', '8s'],
     'BP5_07: Two pair 9-8 (9h-8s) on 8d-4h-2s-9c (turn). OOP non-PFA (SB). '
     'hcat=10, raw_equity=0.72, villain_air=0.47, villain_fold_eq=0.41. '
     'is_rainbow=1, connectivity=3. villain_aggr=0, SPR=7.0. BET.',
     'BP5'),

    (B4_17, ['Ac', '9d'],
     'BP5_08: TPTK A-9 (Ac-9d) on 8d-4h-2s-9c (turn). OOP non-PFA (SB). '
     'hcat=8, raw_equity=0.66, villain_air=0.47, villain_fold_eq=0.36. '
     'is_rainbow=1, connectivity=3. villain_aggr=0, SPR=7.0. BET.',
     'BP5'),

    # --- B4_22 (7c 4h 2s — very low rainbow flop). BB non-PFA. SPR=10.8 ---
    (B4_22, ['7d', '7h'],
     'BP5_09: Set of sevens (7d-7h) on 7c-4h-2s. OOP non-PFA (BB). '
     'hcat=12 (set), raw_equity=0.82, villain_air=0.55, villain_fold_eq=0.52. '
     'is_rainbow=1, connectivity=2. villain_aggr=0, SPR=10.8. '
     'Step 2 does NOT fire (danger_score~0 on 7-4-2 rainbow). Step 6 fires. BET.',
     'BP5'),

    (B4_22, ['7s', '4d'],
     'BP5_10: Two pair 7-4 (7s-4d) on 7c-4h-2s. OOP non-PFA (BB). '
     'hcat=10, raw_equity=0.73, villain_air=0.53, villain_fold_eq=0.47. '
     'is_rainbow=1, connectivity=2. villain_aggr=0, SPR=10.8. BET.',
     'BP5'),

    # --- B4_24 (6c 3d 2h — very low RAINBOW flop). BB non-PFA. SPR=10.8.
    # NOTE: B4_24 corrected to rainbow ['6c','3d','2h'] per consolidated fix #1. ---
    (B4_24, ['6d', '3h'],
     'BP5_11: Two pair 6-3 (6d-3h) on 6c-3d-2h. OOP non-PFA (BB). '
     'hcat=10, raw_equity=0.71, villain_air=0.55, villain_fold_eq=0.44. '
     'is_rainbow=1, connectivity=1. villain_aggr=0, SPR=10.8. '
     'B4_24 corrected to rainbow per fix. BET.',
     'BP5'),

    (B4_24, ['3c', '3s'],
     'BP5_12: Set of threes (3c-3s) on 6c-3d-2h. OOP non-PFA (BB). '
     'hcat=12 (set), raw_equity=0.80, villain_air=0.58, villain_fold_eq=0.50. '
     'is_rainbow=1, connectivity=1. villain_aggr=0, SPR=10.8. BET.',
     'BP5'),
]

# ---------------------------------------------------------------------------
# BP6: CHECK Counterexamples (16 situations — CHECK label)
# Each situation demonstrates exactly one failed gate that prevents BET.
# Source: DESIGN_AGENT_C_BP5_BP6.md + consolidated fix (sit 16 = former BP3 sit 18)
#
# BP6-A (2 sits): Wet board bluff suppressor (S1 fires)
# BP6-B (2 sits): OOP default suppressor (S2 fires)
# BP6-C (1 sit): Multi-street aggressor (S3 fires)
# BP6-D (2 sits): Tier 4 board — Step 3A exits
# BP6-E (1 sit): Step 3B fails (villain_air < 0.40, OOP PFA)
# BP6-F (1 sit): Step 5 fails (danger_score > 0.35, IP non-PFA)
# BP6-G (1 sit): Monster trap on dry board (Step 2 not met)
# BP6-H (6 sits): Near-miss villain_air (former BP2/BP3 borderline situations)
#   Sits 11-13: B4_13 turn, CO OOP, villain_air=0.38 (fails Step 3B gate 0.40)
#   Sits 14-15: B4_16 turn, CO IP, villain_air=0.29 (fails Step 4D gate 0.40)
#   Sit 16: B4_01 flop, BTN IP, villain_air=0.38 (fails Step 4D gate 0.40) — from BP3 sit 18
# ---------------------------------------------------------------------------

SITUATIONS += [
    # --- BP6-D (2 sits): Tier 4 board. B4_18 (Th 9d 8h), connectivity=9. ---
    (B4_18, ['Td', 'Qs'],
     'BP6_01: BP6-D — Tier 4 board exit. TP with Q kicker (Td-Qs) on Th-9d-8h. '
     'connectivity=9: Step 3A exits before BET threshold. hcat=6. '
     'villain_aggr=0, SPR=10.8. Step 3A does not fire for Tier 4. CHECK.',
     'BP6'),

    # --- BP6-A (2 sits): S1 wet board suppressor. B4_18. ---
    (B4_18, ['Jh', '7s'],
     'BP6_02: BP6-A — S1 suppressor fires. OESD (Jh-7s on Th-9d-8h: J-T-9-8-7 needs Q or 6, '
     '8 outs). Also Jh = heart FD contribution but draw_outs < 12 after dedup. '
     'is_made_hand=0. straight_danger>=0.50 on T-9-8 ladder. S1 fires. CHECK.',
     'BP6'),

    # --- BP6-B (2 sits): S2 OOP default suppressor. B4_19 (5h 3c 2d). ---
    (B4_19, ['5s', '9d'],
     'BP6_03: BP6-B — S2 OOP suppressor fires. TP fives weak kicker (5s-9d) on 5h-3c-2d. '
     'OOP BB. hcat=6. hero_range_pct=0.58 (<0.72), raw_equity=0.54 (<0.60). '
     'villain_aggr=0, SPR=10.8. S2 fires. CHECK.',
     'BP6'),

    (B4_19, ['3d', '7h'],
     'BP6_04: BP6-B — S2 OOP suppressor fires. Middle pair threes (3d-7h) on 5h-3c-2d. '
     'OOP BB. hcat=5 (middle pair). hero_range_pct=0.45, raw_equity well below 0.60. '
     'villain_aggr=0, SPR=10.8. S2 fires hard. CHECK.',
     'BP6'),

    # --- BP6-C (1 sit): S3 multi-street aggressor. B4_20 river. ---
    (B4_20, ['Kh', 'Jd'],
     'BP6_05: BP6-C — S3 multi-street aggressor fires. Two pair K-J (Kh-Jd) on '
     'Kc-Jh-7d-3s-9s (river). OOP BB. villain_aggr=2 (CO bet flop AND turn). '
     'hero_range_pct=0.80 (<0.85 gate). S3 fires. CHECK.',
     'BP6'),

    # --- BP6-E (1 sit): Step 3B fails. B4_21 OOP PFA. ---
    (B4_21_OOP, ['Jh', 'Ks'],
     'BP6_06: BP6-E — Step 3B near-miss villain_air. TPGK (Jh-Ks) on Jc-8d-4h. '
     'OOP PFA (CO). hcat=7. hero_range_pct=0.75. villain_air=0.32 (<0.40 gate). '
     'villain_aggr=0, SPR=10.8. Step 3B gate fails on villain_air. CHECK.',
     'BP6'),

    # --- BP6-F (1 sit): Step 5 fails. B4_21 BTN IP non-PFA. ---
    (B4_21_BTN, ['Js', 'Qd'],
     'BP6_07: BP6-F — Step 5 danger_score gate fails. TPGK (Js-Qd) on Jc-8d-4h. '
     'IP non-PFA (BTN cold-called CO). hcat=7. villain_range_capped=1. '
     'danger_score=0.40 (>0.35 gate). villain_aggr=0, SPR=10.8. Step 5 fails. CHECK.',
     'BP6'),

    # --- BP6-G (1 sit): Monster trap on dry board. B4_25 (6h 2c 4s). ---
    (B4_25, ['6d', '6c'],
     'BP6_08: BP6-G — Monster trap on dry board. Set of sixes (6d-6c) on 6h-2c-4s. '
     'OOP non-PFA (BB). is_monster=1, hcat=12. danger_score=0.10 (<0.45): Step 2 does not fire. '
     'No other step applies (OOP non-PFA). Trap slowplay: villain has no draws. '
     'villain_aggr=0, SPR=10.8. CHECK.',
     'BP6'),

    # --- BP6-D sit 9: Tier 4 board, TPTK still insufficient. B4_18 CO. ---
    (B4_18_CO, ['Tc', 'Ad'],
     'BP6_09: BP6-D — Tier 4 board exit, TPTK insufficient. TPTK (Tc-Ad) on Th-9d-8h. '
     'IP CO. connectivity=9: Tier 4 means Step 3A exits regardless of hcat. '
     'hcat=8 (TPTK), but Tier 4 has no c-bet threshold — exits at connectivity check. '
     'villain_aggr=0, SPR=10.8. CHECK.',
     'BP6'),

    # --- BP6-A sit 10: S1 suppressor, different hero. B4_18. ---
    (B4_18, ['6c', '5s'],
     'BP6_10: BP6-A — S1 suppressor fires. OESD (6c-5s on Th-9d-8h: 6-7-8-9-T needs 7 or J, '
     '8 outs). is_made_hand=0. straight_danger~0.70 on T-9-8 ladder. '
     'draw_outs=8 (<12). S1 fires. villain_aggr=1, SPR=10.8. CHECK.',
     'BP6'),

    # --- BP6-H (6 sits): Near-miss villain_air counterexamples ---

    # Sits 11-13: B4_13 turn, CO OOP PFA. villain_air=0.38 fails Step 3B gate (0.40).
    (B4_13_CO_OOP, ['Ah', 'Kd'],
     'BP6_11: BP6-H — Near-miss villain_air. TPTK (Ah-Kd) on Ad-7c-2s-Kh (turn). '
     'OOP PFA (CO). hcat=8. villain_air=0.38 (<0.40 Step 3B gate). '
     'All other 3B conditions pass (hero_range_pct>=0.72, hcr>=13). '
     'villain_aggr=0, SPR=6.0. CHECK.',
     'BP6'),

    (B4_13_CO_OOP, ['As', '8h'],
     'BP6_12: BP6-H — Near-miss villain_air. TPTK (As-8h) on Ad-7c-2s-Kh (turn). '
     'OOP PFA (CO). hcat=8. villain_air=0.38 (<0.40 Step 3B gate). '
     'villain_aggr=0, SPR=6.0. CHECK.',
     'BP6'),

    (B4_13_CO_OOP, ['Ah', '7h'],
     'BP6_13: BP6-H — Near-miss villain_air. Two pair A-7 (Ah-7h) on Ad-7c-2s-Kh (turn). '
     'OOP PFA (CO). hcat=10. villain_air=0.38 (<0.40 Step 3B gate). '
     'villain_aggr=0, SPR=6.0. CHECK.',
     'BP6'),

    # Sits 14-15: B4_16 turn, CO IP non-PFA. villain_air=0.29 fails Step 4D gate (0.40).
    (B4_16_BP6H, ['Ad', '6d'],
     'BP6_14: BP6-H — Near-miss villain_air. Blocker+draw (Ad-6d) on Qc-7d-3h-Kd (turn). '
     'IP non-PFA (CO). Ad blocks nut diamond flush draw (flush_block_pct>0). '
     'draw_outs=4 (gutshot credit). villain_air=0.29 (<0.40 Step 4D gate). '
     'villain_aggr=0, SPR=6.0. CHECK.',
     'BP6'),

    (B4_16_BP6H, ['Jd', 'Tc'],
     'BP6_15: BP6-H — Near-miss villain_air. Blocker+draw (Jd-Tc) on Qc-7d-3h-Kd (turn). '
     'IP non-PFA (CO). Jd: diamond blocker (flush_block_pct>0). '
     'Gutshot: A-K-Q-J-T needs T for broadway (4 outs). villain_air=0.29 (<0.40 Step 4D gate). '
     'villain_aggr=1, SPR=6.0. CHECK.',
     'BP6'),

    # Sit 16: MOVED FROM BP3 sit 18. B4_01 flop, BTN IP PFA.
    # villain_air=0.38 fails Step 4D gate (0.40). Former BP3_4D_18.
    (B4_01, ['Kh', 'Js'],
     'BP6_16: BP6-H — Near-miss villain_air. Former BP3 sit 18 moved here per consolidation fix. '
     'Blocker+weak draw (Kh-Js) on Ad-Tc-4h. IP PFA. Kh blocks KhXh backdoor combos. '
     'Gutshot: K-Q-J-T needs Q (4 outs). villain_air=0.38 (<0.40 Step 4D gate). '
     'is_rainbow=1, hcr=14. villain_aggr=0, SPR=10.8. Step 4D gate fails on villain_air. CHECK.',
     'BP6'),
]

# =============================================================================
# VALIDATION: verify expected counts per sub-pattern
# =============================================================================

# Revised counts per consolidated fix doc:
#   BP3: 19 (was 20, sit 18 moved to BP6)
#   BP6: 16 (was 15, gained sit 18 as sit 16)
#   Total: 104 (unchanged)

_EXPECTED_COUNTS = {
    'BP1': 30,
    'BP2': 12,
    'BP3': 19,
    'BP4': 15,
    'BP5': 12,
    'BP6': 16,
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
    total = len(SITUATIONS)
    print(
        f"Situation count check PASSED — {total} total situations defined "
        f"(BP1={counts['BP1']}, BP2={counts['BP2']}, BP3={counts['BP3']}, "
        f"BP4={counts['BP4']}, BP5={counts['BP5']}, BP6={counts['BP6']})."
    )
    return True


# =============================================================================
# GENERATION + VALIDATION
# =============================================================================

def generate_all():
    """Build, validate, and collect all 104 situations."""
    all_records = []
    total_generated = 0
    total_validated = 0
    error_log = []  # (sit_id, error_type, detail)

    for idx, (board_base, hero_cards, description, sub_pattern) in enumerate(SITUATIONS):
        # Derive situation_id: BPX_YY (1-indexed within sub-pattern)
        sp_situations = [s for s in SITUATIONS[:idx + 1] if s[3] == sub_pattern]
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
            print(f"  WARN  {sit_id} {hero_cards}: {'; '.join(validation_errors)}")
        else:
            feat_dict['has_errors'] = False
            total_validated += 1
            print(f"  OK    {sit_id} {hero_cards}")

        all_records.append(feat_dict)

    return all_records, total_generated, total_validated, error_log


def main():
    print("=" * 60)
    print("FACTORY BATCH 4 — 104-SITUATION BET CONTEXT BATCH")
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
            # ANOMALY-A fix: normalise street/hero_position at serialisation.
            f.write(json.dumps(normalise_situation(record)) + '\n')

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
