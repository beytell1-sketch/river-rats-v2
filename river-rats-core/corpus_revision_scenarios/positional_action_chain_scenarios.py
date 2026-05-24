"""Positional action-chain scenario specs (Module 10).

Generates SituationSpec instances matching enumerated chain fingerprints for
the Phase 2-F1 corpus expansion (batches 009-014).

Blueprint:  review/comms/DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-13.md
Ratified:   review/comms/RATIFICATION_A1_POSITIONAL_CHAIN_2026-05-22.md
Directive:  review/comms/MAIN_TERMINAL_PHASE2F1_B1_FIRE_NOW_2026-05-22.md

24-spec per-batch quota allocation (RATIFICATION_A1 §Per-batch slot allocation):
  - 12 top-12 chain anchors (one per rank from v1 §5.1)
  -  6 facing-raise expansion (BET_RAISE / CHECK_RAISE)
  -  4 river expansion
  -  2 sandwich enforcement (hero positionally between two villain actors)

The 24 templates below satisfy all 5 A1 mandatory floors (facing-raise ≥10,
river ≥5, position-balance ≥1 each of {BTN, CO, MP, UTG, SB, BB} as
scorecard-class hero_pos, top-12 ≥1 each, sandwich ≥4) — with deliberate
overlap (some river templates are also facing-raise; sandwich templates use
{UTG, HJ}/MP-class hero positions to satisfy position-balance).
"""
from __future__ import annotations

import os
import random
import sys
from typing import List, NamedTuple, Optional, Set, Tuple

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from situation_factory import SituationSpec


class ChainFingerprint(NamedTuple):
    """7-tuple chain fingerprint per blueprint §2.1.

    callers_chain is ORDERED (not sorted) — preserves seat-order of callers
    between aggressor and hero on the decision street.
    """
    street: str
    hero_pos: str
    aggressor_pos: str
    callers_chain: Tuple[str, ...]
    raiser_pos: str
    raise_target_pos: str
    chain_shape: str


# =============================================================================
# Top-12 chain anchors (v1 §5.1, accepted per RATIFICATION_A1)
# =============================================================================
# Ranks 1..12 in v1's predicted natural-frequency order. The per-batch quota
# reserves 1 slot per rank; absolute frequency is reweighted in Phase 2-F2.

_TOP_12_CHAINS: List[ChainFingerprint] = [
    # Rank 1 — flop IP-closing single c-bet
    ChainFingerprint('flop', 'BTN', 'CO', (), 'NONE', 'NONE', 'BET'),
    # Rank 2 — flop OOP-early bet+call (hero BB, CO bets, BTN calls)
    ChainFingerprint('flop', 'BB', 'CO', ('BTN',), 'NONE', 'NONE', 'BET_CALL'),
    # Rank 3 — flop OOP-early single bet (BB folded)
    ChainFingerprint('flop', 'SB', 'CO', (), 'NONE', 'NONE', 'BET'),
    # Rank 4 — flop IP-closing bet+call (UTG bets, CO calls)
    ChainFingerprint('flop', 'BTN', 'UTG', ('CO',), 'NONE', 'NONE', 'BET_CALL'),
    # Rank 5 — flop OOP-early bet+2call (UTG bets, HJ + CO call)
    ChainFingerprint('flop', 'BB', 'UTG', ('HJ', 'CO'), 'NONE', 'NONE', 'BET_CALL_CALL'),
    # Rank 6 — flop OOP-early OPEN (would-be aggressor)
    ChainFingerprint('flop', 'BB', 'NONE', (), 'NONE', 'NONE', 'OPEN'),
    # Rank 7 — flop OOP-middle bet+call (CO hero, UTG bets, HJ calls)
    ChainFingerprint('flop', 'CO', 'UTG', ('HJ',), 'NONE', 'NONE', 'BET_CALL'),
    # Rank 8 — turn IP-closing single bet
    ChainFingerprint('turn', 'BTN', 'CO', (), 'NONE', 'NONE', 'BET'),
    # Rank 9 — flop OOP-early facing IP raise (CO bets, BTN raises)
    ChainFingerprint('flop', 'BB', 'CO', (), 'BTN', 'CO', 'BET_RAISE'),
    # Rank 10 — turn OOP-early bet+call (CO bets, BTN calls)
    ChainFingerprint('turn', 'BB', 'CO', ('BTN',), 'NONE', 'NONE', 'BET_CALL'),
    # Rank 11 — river IP single bet
    ChainFingerprint('river', 'BTN', 'CO', (), 'NONE', 'NONE', 'BET'),
    # Rank 12 — flop OOP-middle facing BB-donk
    ChainFingerprint('flop', 'SB', 'BB', (), 'NONE', 'NONE', 'BET'),
]


def enumerate_top_12_chains() -> List[ChainFingerprint]:
    """Return the 12 chain fingerprints from v1 §5.1 in rank order."""
    return list(_TOP_12_CHAINS)


# =============================================================================
# 24 template specs (one per slot in the per-batch quota)
# =============================================================================
# Each template is a dict with keys:
#   hero_pos, villain_positions, opener_position, board, hero_cards,
#   pot, to_call, street, action_history, chain_fingerprint
#
# Templates 0-11: top-12 anchors (T1..T12 in rank order, indices 0..11).
# Templates 12-17: 6 facing-raise expansion (BET_RAISE / CHECK_RAISE / MULTI_AGGR).
# Templates 18-21: 4 river expansion (some overlap with facing-raise).
# Templates 22-23: 2 sandwich enforcement (UTG- and HJ-hero per position-balance).

_CHAIN_FINGERPRINT_TEMPLATES: List[dict] = [
    # ─────────────────────────────────────────────────────────────────────
    # T0 — RANK 1: flop IP-closing single c-bet
    {
        'hero_pos': 'BTN',
        'villain_positions': ['CO', 'SB', 'BB'],
        'opener_position': 'CO',
        'board': ['Ks', '7d', '2c'],
        'hero_cards': ['Ah', 'Jh'],
        'pot': 18.0,
        'to_call': 4.5,
        'street': 'flop',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'call'),
            ('preflop', 'BB', 'call'),
            ('flop', 'SB', 'check'),
            ('flop', 'BB', 'check'),
            ('flop', 'CO', 'bet'),
        ],
        'chain_fingerprint': _TOP_12_CHAINS[0],
    },
    # T1 — RANK 2: flop OOP-early bet+call (hero BB)
    {
        'hero_pos': 'BB',
        'villain_positions': ['CO', 'BTN', 'SB'],
        'opener_position': 'CO',
        'board': ['Jc', '8h', '3d'],
        'hero_cards': ['Tc', '9s'],
        'pot': 24.0,
        'to_call': 6.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'call'),
            ('preflop', 'BB', 'call'),
            ('flop', 'SB', 'check'),
            ('flop', 'BB', 'check'),
            ('flop', 'CO', 'bet'),
            ('flop', 'BTN', 'call'),
        ],
        'chain_fingerprint': _TOP_12_CHAINS[1],
    },
    # T2 — RANK 3: flop OOP-early single bet (BB folded preflop)
    {
        'hero_pos': 'SB',
        'villain_positions': ['CO'],
        'opener_position': 'CO',
        'board': ['Qd', '5h', '2s'],
        'hero_cards': ['Ad', 'Kc'],
        'pot': 11.5,
        'to_call': 3.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'SB', 'call'),
            ('preflop', 'BB', 'fold'),
            ('flop', 'SB', 'check'),
            ('flop', 'CO', 'bet'),
        ],
        'chain_fingerprint': _TOP_12_CHAINS[2],
    },
    # T3 — RANK 4: flop IP-closing bet+call (UTG bets, CO calls)
    {
        'hero_pos': 'BTN',
        'villain_positions': ['UTG', 'CO', 'BB'],
        'opener_position': 'UTG',
        'board': ['9h', '6c', '3s'],
        'hero_cards': ['Ks', 'Qs'],
        'pot': 22.0,
        'to_call': 5.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'UTG', 'raise'),
            ('preflop', 'CO', 'call'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'call'),
            ('flop', 'BB', 'check'),
            ('flop', 'UTG', 'bet'),
            ('flop', 'CO', 'call'),
        ],
        'chain_fingerprint': _TOP_12_CHAINS[3],
    },
    # T4 — RANK 5: flop OOP-early bet+2call (UTG bets, HJ + CO call)
    {
        'hero_pos': 'BB',
        'villain_positions': ['UTG', 'HJ', 'CO'],
        'opener_position': 'UTG',
        'board': ['Th', '6d', '4c'],
        'hero_cards': ['Ad', 'Jh'],
        'pot': 27.0,
        'to_call': 6.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'UTG', 'raise'),
            ('preflop', 'HJ', 'call'),
            ('preflop', 'CO', 'call'),
            ('preflop', 'BTN', 'fold'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'call'),
            ('flop', 'BB', 'check'),
            ('flop', 'UTG', 'bet'),
            ('flop', 'HJ', 'call'),
            ('flop', 'CO', 'call'),
        ],
        'chain_fingerprint': _TOP_12_CHAINS[4],
    },
    # T5 — RANK 6: flop OOP-early OPEN (would-be aggressor; checks to hero)
    {
        'hero_pos': 'BB',
        'villain_positions': ['CO', 'BTN'],
        'opener_position': 'CO',
        'board': ['7c', '5d', '2h'],
        'hero_cards': ['Qh', 'Jc'],
        'pot': 12.0,
        'to_call': 0.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'call'),
            ('flop', 'BB', 'check'),
            ('flop', 'CO', 'check'),
            ('flop', 'BTN', 'check'),
        ],
        'chain_fingerprint': _TOP_12_CHAINS[5],
    },
    # T6 — RANK 7: flop OOP-middle bet+call (CO hero, UTG bets, HJ calls)
    {
        'hero_pos': 'CO',
        'villain_positions': ['UTG', 'HJ', 'BTN'],
        'opener_position': 'UTG',
        'board': ['Ad', '8s', '3c'],
        'hero_cards': ['Kc', 'Qd'],
        'pot': 22.0,
        'to_call': 5.5,
        'street': 'flop',
        'action_history': [
            ('preflop', 'UTG', 'raise'),
            ('preflop', 'HJ', 'call'),
            ('preflop', 'CO', 'call'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'fold'),
            ('flop', 'UTG', 'bet'),
            ('flop', 'HJ', 'call'),
        ],
        'chain_fingerprint': _TOP_12_CHAINS[6],
    },
    # T7 — RANK 8: turn IP-closing single bet (board 4 cards)
    {
        'hero_pos': 'BTN',
        'villain_positions': ['CO', 'SB'],
        'opener_position': 'CO',
        'board': ['Ts', '6h', '3c', '9d'],
        'hero_cards': ['Ah', 'Th'],
        'pot': 32.0,
        'to_call': 9.0,
        'street': 'turn',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'call'),
            ('preflop', 'BB', 'fold'),
            ('flop', 'SB', 'check'),
            ('flop', 'CO', 'bet'),
            ('flop', 'BTN', 'call'),
            ('flop', 'SB', 'call'),
            ('turn', 'SB', 'check'),
            ('turn', 'CO', 'bet'),
        ],
        'chain_fingerprint': _TOP_12_CHAINS[7],
    },
    # T8 — RANK 9: flop OOP-early facing IP raise (CO bets, BTN raises)
    {
        'hero_pos': 'BB',
        'villain_positions': ['CO', 'BTN'],
        'opener_position': 'CO',
        'board': ['Js', '7s', '2d'],
        'hero_cards': ['Tc', 'Td'],
        'pot': 14.0,
        'to_call': 12.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'call'),
            ('flop', 'BB', 'check'),
            ('flop', 'CO', 'bet'),
            ('flop', 'BTN', 'raise'),
        ],
        'chain_fingerprint': _TOP_12_CHAINS[8],
    },
    # T9 — RANK 10: turn OOP-early bet+call (CO bets, BTN calls)
    {
        'hero_pos': 'BB',
        'villain_positions': ['CO', 'BTN'],
        'opener_position': 'CO',
        'board': ['Qh', '8d', '4c', '2s'],
        'hero_cards': ['Ad', 'Qc'],
        'pot': 28.0,
        'to_call': 9.0,
        'street': 'turn',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'call'),
            ('flop', 'BB', 'check'),
            ('flop', 'CO', 'bet'),
            ('flop', 'BTN', 'call'),
            ('flop', 'BB', 'call'),
            ('turn', 'BB', 'check'),
            ('turn', 'CO', 'bet'),
            ('turn', 'BTN', 'call'),
        ],
        'chain_fingerprint': _TOP_12_CHAINS[9],
    },
    # T10 — RANK 11: river IP single bet (board 5 cards)
    {
        'hero_pos': 'BTN',
        'villain_positions': ['CO'],
        'opener_position': 'CO',
        'board': ['Kd', '8c', '4h', '2s', '7d'],
        'hero_cards': ['Ah', 'Kc'],
        'pot': 36.0,
        'to_call': 12.0,
        'street': 'river',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'fold'),
            ('flop', 'CO', 'bet'),
            ('flop', 'BTN', 'call'),
            ('turn', 'CO', 'bet'),
            ('turn', 'BTN', 'call'),
            ('river', 'CO', 'bet'),
        ],
        'chain_fingerprint': _TOP_12_CHAINS[10],
    },
    # T11 — RANK 12: flop OOP-middle facing BB-donk (SB pre-checked, BB donks)
    {
        'hero_pos': 'SB',
        'villain_positions': ['CO', 'BB', 'BTN'],
        'opener_position': 'CO',
        'board': ['9s', '6c', '4d'],
        'hero_cards': ['As', 'Th'],
        'pot': 22.0,
        'to_call': 5.5,
        'street': 'flop',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'call'),
            ('preflop', 'BB', 'call'),
            ('flop', 'SB', 'check'),
            ('flop', 'BB', 'bet'),
        ],
        'chain_fingerprint': _TOP_12_CHAINS[11],
    },
    # ─────────────────────────────────────────────────────────────────────
    # FACING-RAISE EXPANSION (T12..T17) — 6 templates BET_RAISE / CHECK_RAISE
    # ─────────────────────────────────────────────────────────────────────
    # T12 — flop BTN facing UTG-bet + CO-raise (IP-closing facing raise)
    {
        'hero_pos': 'BTN',
        'villain_positions': ['UTG', 'CO', 'BB'],
        'opener_position': 'UTG',
        'board': ['Qc', '8h', '3d'],
        'hero_cards': ['Ad', 'Qh'],
        'pot': 22.0,
        'to_call': 16.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'UTG', 'raise'),
            ('preflop', 'CO', 'call'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'call'),
            ('flop', 'BB', 'check'),
            ('flop', 'UTG', 'bet'),
            ('flop', 'CO', 'raise'),
        ],
        'chain_fingerprint': ChainFingerprint(
            'flop', 'BTN', 'UTG', (), 'CO', 'UTG', 'BET_RAISE'),
    },
    # T13 — flop SB facing CHECK_RAISE (BB checks, CO bets, BB raises)
    {
        'hero_pos': 'SB',
        'villain_positions': ['CO', 'BB'],
        'opener_position': 'CO',
        'board': ['9c', '7d', '5h'],
        'hero_cards': ['Ah', 'Ac'],
        'pot': 17.0,
        'to_call': 14.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'fold'),
            ('preflop', 'SB', 'call'),
            ('preflop', 'BB', 'call'),
            ('flop', 'SB', 'check'),
            ('flop', 'BB', 'check'),
            ('flop', 'CO', 'bet'),
            ('flop', 'BB', 'raise'),
        ],
        'chain_fingerprint': ChainFingerprint(
            'flop', 'SB', 'CO', (), 'BB', 'CO', 'CHECK_RAISE'),
    },
    # T14 — flop CO facing UTG-bet + HJ-raise (OOP-middle facing raise)
    {
        'hero_pos': 'CO',
        'villain_positions': ['UTG', 'HJ', 'BTN'],
        'opener_position': 'UTG',
        'board': ['Ts', '8d', '6c'],
        'hero_cards': ['Ad', 'As'],
        'pot': 24.0,
        'to_call': 14.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'UTG', 'raise'),
            ('preflop', 'HJ', 'call'),
            ('preflop', 'CO', 'call'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'fold'),
            ('flop', 'UTG', 'bet'),
            ('flop', 'HJ', 'raise'),
        ],
        'chain_fingerprint': ChainFingerprint(
            'flop', 'CO', 'UTG', (), 'HJ', 'UTG', 'BET_RAISE'),
    },
    # T15 — turn BTN facing CHECK_RAISE (BB checks-bets, CO raises)
    {
        'hero_pos': 'BTN',
        'villain_positions': ['CO', 'BB'],
        'opener_position': 'CO',
        'board': ['Ks', '8h', '4d', '9c'],
        'hero_cards': ['Ah', 'Kd'],
        'pot': 32.0,
        'to_call': 24.0,
        'street': 'turn',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'call'),
            ('flop', 'BB', 'check'),
            ('flop', 'CO', 'bet'),
            ('flop', 'BTN', 'call'),
            ('flop', 'BB', 'call'),
            ('turn', 'BB', 'check'),
            ('turn', 'CO', 'bet'),
            ('turn', 'BB', 'raise'),
        ],
        'chain_fingerprint': ChainFingerprint(
            'turn', 'BTN', 'CO', (), 'BB', 'CO', 'CHECK_RAISE'),
    },
    # T16 — turn BB facing CO-bet + BTN-raise (OOP-early facing IP raise)
    {
        'hero_pos': 'BB',
        'villain_positions': ['CO', 'BTN'],
        'opener_position': 'CO',
        'board': ['Jc', '7s', '5d', '2h'],
        'hero_cards': ['As', 'Ks'],
        'pot': 28.0,
        'to_call': 18.0,
        'street': 'turn',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'call'),
            ('flop', 'BB', 'check'),
            ('flop', 'CO', 'bet'),
            ('flop', 'BTN', 'call'),
            ('flop', 'BB', 'call'),
            ('turn', 'BB', 'check'),
            ('turn', 'CO', 'bet'),
            ('turn', 'BTN', 'raise'),
        ],
        'chain_fingerprint': ChainFingerprint(
            'turn', 'BB', 'CO', (), 'BTN', 'CO', 'BET_RAISE'),
    },
    # T17 — flop SB facing CO-bet + BTN-raise (OOP-early facing IP raise, parallel to rank 9 but hero=SB)
    {
        'hero_pos': 'SB',
        'villain_positions': ['CO', 'BTN'],
        'opener_position': 'CO',
        'board': ['Td', '8c', '3h'],
        'hero_cards': ['Ah', 'Kc'],
        'pot': 14.5,
        'to_call': 12.5,
        'street': 'flop',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'call'),
            ('preflop', 'BB', 'fold'),
            ('flop', 'SB', 'check'),
            ('flop', 'CO', 'bet'),
            ('flop', 'BTN', 'raise'),
        ],
        'chain_fingerprint': ChainFingerprint(
            'flop', 'SB', 'CO', (), 'BTN', 'CO', 'BET_RAISE'),
    },
    # ─────────────────────────────────────────────────────────────────────
    # RIVER EXPANSION (T18..T21) — 4 templates river street; 2 overlap facing-raise
    # ─────────────────────────────────────────────────────────────────────
    # T18 — river BB facing CO-bet + BTN-call (OOP-early bet+call)
    {
        'hero_pos': 'BB',
        'villain_positions': ['CO', 'BTN'],
        'opener_position': 'CO',
        'board': ['Qd', '8h', '4s', '2c', '7d'],
        'hero_cards': ['Ah', 'Qh'],
        'pot': 42.0,
        'to_call': 14.0,
        'street': 'river',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'call'),
            ('flop', 'BB', 'check'),
            ('flop', 'CO', 'bet'),
            ('flop', 'BTN', 'call'),
            ('flop', 'BB', 'call'),
            ('turn', 'BB', 'check'),
            ('turn', 'CO', 'check'),
            ('turn', 'BTN', 'check'),
            ('river', 'BB', 'check'),
            ('river', 'CO', 'bet'),
            ('river', 'BTN', 'call'),
        ],
        'chain_fingerprint': ChainFingerprint(
            'river', 'BB', 'CO', ('BTN',), 'NONE', 'NONE', 'BET_CALL'),
    },
    # T19 — river SB facing CO-bet (BB folded; HU at river)
    {
        'hero_pos': 'SB',
        'villain_positions': ['CO'],
        'opener_position': 'CO',
        'board': ['Th', '6c', '3d', '8s', 'Kc'],
        'hero_cards': ['As', 'Ts'],
        'pot': 24.0,
        'to_call': 8.0,
        'street': 'river',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'fold'),
            ('preflop', 'SB', 'call'),
            ('preflop', 'BB', 'fold'),
            ('flop', 'SB', 'check'),
            ('flop', 'CO', 'bet'),
            ('flop', 'SB', 'call'),
            ('turn', 'SB', 'check'),
            ('turn', 'CO', 'bet'),
            ('turn', 'SB', 'call'),
            ('river', 'SB', 'check'),
            ('river', 'CO', 'bet'),
        ],
        'chain_fingerprint': ChainFingerprint(
            'river', 'SB', 'CO', (), 'NONE', 'NONE', 'BET'),
    },
    # T20 — river BTN facing CHECK_RAISE (BB checks-bets-raises CO's bet; rare but reachable)
    # Use BET_RAISE pattern: CO bets river, BB raises
    {
        'hero_pos': 'BTN',
        'villain_positions': ['CO', 'BB'],
        'opener_position': 'CO',
        'board': ['Js', '8h', '4d', '2c', 'Qd'],
        'hero_cards': ['Ah', 'Js'],
        'pot': 48.0,
        'to_call': 36.0,
        'street': 'river',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'call'),
            ('flop', 'BB', 'check'),
            ('flop', 'CO', 'bet'),
            ('flop', 'BTN', 'call'),
            ('flop', 'BB', 'call'),
            ('turn', 'BB', 'check'),
            ('turn', 'CO', 'bet'),
            ('turn', 'BTN', 'call'),
            ('turn', 'BB', 'call'),
            ('river', 'BB', 'check'),
            ('river', 'CO', 'bet'),
            ('river', 'BB', 'raise'),
        ],
        'chain_fingerprint': ChainFingerprint(
            'river', 'BTN', 'CO', (), 'BB', 'CO', 'CHECK_RAISE'),
    },
    # T21 — river CO facing BTN-bet + BB-check-raise (hero pre-checked river)
    # Postflop seat order on river (SB/UTG/HJ folded earlier): BB, CO, BTN.
    # Sequence: BB checks → CO (hero) checks → BTN bets → BB check-raises →
    # action returns to CO for decision. Both BB and BTN acted before hero's
    # decision moment; the raiser (BB) had a prior check on the street, so the
    # canonical chain_shape is CHECK_RAISE (per blueprint §3 and the algorithm
    # in _scenario_utils.compute_chain_fingerprint). CHECK_RAISE ∈ facing-raise
    # set, so this still satisfies the facing-raise quota floor.
    #
    # B1.1: declared chain_shape was 'BET_RAISE' prior to the QC SHOULD_FIX-1
    # finding (`findings/2026-05-23-pr468-b1-positional-chain-scenarios.md`);
    # corrected here to match the action_history's computed fingerprint.
    {
        'hero_pos': 'CO',
        'villain_positions': ['BB', 'BTN'],
        'opener_position': 'CO',
        'board': ['9d', '7c', '5h', '2s', '8d'],
        'hero_cards': ['Ad', 'Ac'],
        'pot': 32.0,
        'to_call': 26.0,
        'street': 'river',
        'action_history': [
            ('preflop', 'CO', 'raise'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'call'),
            ('flop', 'BB', 'check'),
            ('flop', 'CO', 'bet'),
            ('flop', 'BTN', 'call'),
            ('flop', 'BB', 'call'),
            ('turn', 'BB', 'check'),
            ('turn', 'CO', 'check'),
            ('turn', 'BTN', 'check'),
            ('river', 'BB', 'check'),
            ('river', 'CO', 'check'),
            ('river', 'BTN', 'bet'),
            ('river', 'BB', 'raise'),
        ],
        'chain_fingerprint': ChainFingerprint(
            'river', 'CO', 'BTN', (), 'BB', 'BTN', 'CHECK_RAISE'),
    },
    # ─────────────────────────────────────────────────────────────────────
    # SANDWICH ENFORCEMENT + POSITION BALANCE (T22..T23) — UTG and HJ heroes
    # ─────────────────────────────────────────────────────────────────────
    # T22 — flop UTG hero facing SB-donk + BB-raise; sandwich (CO+BTN behind UTG)
    # Position-balance: UTG hero (UTG scorecard class).
    # Also satisfies facing-raise floor (BET_RAISE).
    {
        'hero_pos': 'UTG',
        'villain_positions': ['CO', 'BTN', 'SB', 'BB'],
        'opener_position': 'UTG',
        'board': ['Tc', '7d', '4s'],
        'hero_cards': ['Ad', 'Ks'],
        'pot': 22.0,
        'to_call': 16.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'UTG', 'raise'),
            ('preflop', 'HJ', 'fold'),
            ('preflop', 'CO', 'call'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'call'),
            ('preflop', 'BB', 'call'),
            ('flop', 'SB', 'bet'),
            ('flop', 'BB', 'raise'),
        ],
        'chain_fingerprint': ChainFingerprint(
            'flop', 'UTG', 'SB', (), 'BB', 'SB', 'BET_RAISE'),
    },
    # T23 — flop HJ hero facing UTG-bet; sandwich (CO+BTN behind HJ; MP-class position balance)
    {
        'hero_pos': 'HJ',
        'villain_positions': ['UTG', 'CO', 'BTN', 'BB'],
        'opener_position': 'UTG',
        'board': ['Kc', '9h', '4d'],
        'hero_cards': ['Qs', 'Qc'],
        'pot': 22.0,
        'to_call': 5.5,
        'street': 'flop',
        'action_history': [
            ('preflop', 'UTG', 'raise'),
            ('preflop', 'HJ', 'call'),
            ('preflop', 'CO', 'call'),
            ('preflop', 'BTN', 'call'),
            ('preflop', 'SB', 'fold'),
            ('preflop', 'BB', 'call'),
            ('flop', 'BB', 'check'),
            ('flop', 'UTG', 'bet'),
        ],
        'chain_fingerprint': ChainFingerprint(
            'flop', 'HJ', 'UTG', (), 'NONE', 'NONE', 'BET'),
    },
]

assert len(_CHAIN_FINGERPRINT_TEMPLATES) == 24, (
    f"_CHAIN_FINGERPRINT_TEMPLATES must have exactly 24 entries; "
    f"got {len(_CHAIN_FINGERPRINT_TEMPLATES)}"
)


# =============================================================================
# Spec materialization
# =============================================================================


def _spec_from_template(tmpl: dict) -> SituationSpec:
    """Build a SituationSpec from a template dict."""
    return SituationSpec(
        hero_cards=list(tmpl['hero_cards']),
        board_cards=list(tmpl['board']),
        hero_pos=tmpl['hero_pos'],
        villain_positions=list(tmpl['villain_positions']),
        pot=tmpl['pot'],
        to_call=tmpl['to_call'],
        street=tmpl['street'],
        action_history=list(tmpl['action_history']),
        opener_position=tmpl.get('opener_position'),
    )


def generate_chain_scenarios(
    chain_fp: ChainFingerprint,
    count: int,
    *,
    rng_seed: int,
    forbidden_fingerprints: Set[Tuple[str, str]],
) -> List[SituationSpec]:
    """Generate `count` SituationSpec instances matching `chain_fp`.

    For B1 scope, draws from `_CHAIN_FINGERPRINT_TEMPLATES`. When `count`
    exceeds available templates for `chain_fp`, returns all matching
    templates (deterministically sorted via rng_seed).

    Args:
        chain_fp: target chain fingerprint.
        count: number of scenarios to produce.
        rng_seed: deterministic seed; affects template order when multiple
                  templates match.
        forbidden_fingerprints: card-equivalence fingerprints to skip.

    Returns:
        List of SituationSpec, up to `count` entries.

    Raises:
        ValueError: if `chain_fp` is structurally unreachable (validated
                    against postflop seat-order constraints).
    """
    _validate_chain_reachability(chain_fp)

    matches = [
        tmpl for tmpl in _CHAIN_FINGERPRINT_TEMPLATES
        if tmpl['chain_fingerprint'] == chain_fp
    ]
    if not matches:
        return []

    rng = random.Random(rng_seed)
    rng.shuffle(matches)

    from corpus_revision_scenarios._scenario_utils import fingerprint as _card_fp

    out: List[SituationSpec] = []
    for tmpl in matches:
        if len(out) >= count:
            break
        hero_cards_str = ''.join(tmpl['hero_cards'])
        board_str = ''.join(tmpl['board'])
        cfp = _card_fp(hero_cards_str, board_str)
        if cfp in forbidden_fingerprints:
            continue
        out.append(_spec_from_template(tmpl))
    return out


def generate_phase_2f_chain_quota(
    *,
    rng_seed: int,
    forbidden_fingerprints: Set[Tuple[str, str]],
) -> List[SituationSpec]:
    """Generate the 24-spec per-batch enumerated chain quota.

    Per RATIFICATION_A1 §Per-batch slot allocation: 24 SituationSpec instances
    covering all 5 A1 mandatory floors (facing-raise ≥10, river ≥5,
    position-balance ≥1 each of {BTN, CO, MP, UTG, SB, BB}, top-12 ≥1 each,
    sandwich ≥4).

    Args:
        rng_seed: deterministic seed (same seed → same 24 spots).
        forbidden_fingerprints: card-equivalence fingerprints to skip.

    Returns:
        List of exactly 24 SituationSpec instances (in template order;
        rng_seed currently unused for ordering as the quota is canonical).
    """
    from corpus_revision_scenarios._scenario_utils import fingerprint as _card_fp

    rng = random.Random(rng_seed)
    _ = rng.random()  # advance state (kept for forward-compat)

    out: List[SituationSpec] = []
    for tmpl in _CHAIN_FINGERPRINT_TEMPLATES:
        hero_cards_str = ''.join(tmpl['hero_cards'])
        board_str = ''.join(tmpl['board'])
        cfp = _card_fp(hero_cards_str, board_str)
        if cfp in forbidden_fingerprints:
            continue
        out.append(_spec_from_template(tmpl))
    return out


# =============================================================================
# Validation
# =============================================================================


_POSTFLOP_SEAT_ORDER = ['SB', 'BB', 'UTG', 'HJ', 'CO', 'BTN']


def _seat_index(pos: str) -> int:
    if pos == 'NONE':
        return -1
    if pos == 'EP':
        pos = 'UTG'
    if pos == 'MP':
        pos = 'HJ'
    return _POSTFLOP_SEAT_ORDER.index(pos)


def _validate_chain_reachability(chain_fp: ChainFingerprint) -> None:
    """Raise ValueError if the chain fingerprint violates postflop seat-order
    constraints (independent of any specific spec; applies to OPEN/BET shapes
    where hero has not pre-acted)."""
    if chain_fp.aggressor_pos == 'NONE':
        if chain_fp.callers_chain or chain_fp.raiser_pos != 'NONE':
            raise ValueError(
                f"chain_fp.aggressor_pos == 'NONE' but callers/raiser populated: {chain_fp}"
            )
        if chain_fp.chain_shape != 'OPEN':
            raise ValueError(
                f"aggressor_pos == 'NONE' requires chain_shape == 'OPEN'; got {chain_fp.chain_shape}"
            )
    # Further runtime reachability is checked per-spec in validate_chain_fingerprint.


def validate_chain_fingerprint(
    spec: SituationSpec,
    expected_chain: ChainFingerprint,
) -> bool:
    """Assert that a generated SituationSpec's action_history produces a
    decision moment matching `expected_chain`.

    Returns True if the spec's reconstructed fingerprint equals expected_chain.
    Raises AssertionError with a precise per-field diff on mismatch.
    """
    from corpus_revision_scenarios._scenario_utils import compute_chain_fingerprint

    computed = compute_chain_fingerprint(spec)
    if computed == expected_chain:
        return True

    # Build per-field diff
    diffs = []
    for field in ChainFingerprint._fields:
        expected_val = getattr(expected_chain, field)
        actual_val = getattr(computed, field)
        if expected_val != actual_val:
            diffs.append(f"  {field}: expected {expected_val!r}, got {actual_val!r}")
    diff_str = "\n".join(diffs)
    raise AssertionError(
        f"Chain fingerprint mismatch for spec "
        f"(hero_pos={spec.hero_pos}, street={spec.street}):\n"
        f"{diff_str}\n"
        f"action_history: {spec.action_history}"
    )
