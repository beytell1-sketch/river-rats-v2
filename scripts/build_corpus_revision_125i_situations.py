#!/usr/bin/env python3
"""Phase 12.5I-B situation generator — ~96 new hands across 3 redesigned templates.

Implements 12.5I-A design (`review/comms/PLAN_PHASE125I_CORPUS_EXPANSION_2026-05-06.md`,
master `d045b03`) per Phase 12.5I-B dispatch
(`review/comms/MAIN_TERMINAL_PHASE125I_B_DISPATCH_2026-05-06.md`,
master `3b31f2a`).

Re-uses helpers from `scripts/build_corpus_revision_125e_situations.py`
(master `858b032`) — `emit_row`, `build_hand_dict`,
`_hero_only_prior_actions`, `TemplateGenerator`, `GeneratedSituation`.

Templates per 12.5I-A §3:
- T8'-redesigned (30 = ~28 factory + 2 manual): non-nut FD on board where
  hero does NOT hold the on-board top card; 4-way checked through; BTN IP
  (MW-25 family — addresses corpus underpowering identified in 12.5I-pre)
- T9'-expanded (33 = ~32 factory + 1 manual): TP-medium-kicker IP 4-way
  after PFR check (MW-40 family — 2.3× scale-up from 12.5H T9'=14)
- T10'-redesigned (31 = ~30 factory + 1 manual): bottom-or-middle set on
  rainbow flop with broadway-completed turn (MW-45 family — addresses
  isomorph-mismatch identified in 12.5I-pre)

Total: 90 factory + 4 manual = 94 hands. pilot_hand_id range
PILOT_695..PILOT_788.

Output schema mirrors 12.5H-B factory + combined corpus.

Usage:
    python3 scripts/build_corpus_revision_125i_situations.py
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CORE = os.path.join(_REPO, "river-rats-core")
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)
sys.path.insert(0, os.path.join(_REPO, "scripts"))

from build_corpus_revision_125e_situations import (  # noqa: E402
    GeneratedSituation,
    TemplateGenerator,
    emit_row,
)

PILOT_ID_START = 695  # continues PILOT_001..PILOT_694
PILOT_PARAMETRIC_END = 784  # 695..784 = 90 parametric hands
PILOT_ID_END = 788  # 785..788 = 4 manual canonicals; total 94

PARAMETRIC_TOTAL = 90
MANUAL_TOTAL = 4
GRAND_TOTAL = 94


# ─── T8'-redesigned — non-nut FD checked-through 4-way (MW-25 family) ──


class T8PrimeRedesigned(TemplateGenerator):
    """MW-25 family — REDESIGNED at 12.5I-B per per-hand diagnostic verdict
    (E-DIST underpowered + protocol-design constraint).

    12.5H T8' put the As ON the monotone board → hero K-spade was dominated
    by every villain holding any spade → corpus produced CHECK labels
    uniformly (matching model "wrong" prediction rather than reference BET).

    T8'-redesigned constraint: hero does NOT hold the on-board top card
    AND does NOT hold the nut blocker. Hero has FD via 1-2 hole cards on
    a two-tone or monotone board where Ace of FD suit is NOT on the board.
    Discriminative axis: has_flush_draw=1, nut_flush_block=0, 4-way checked
    through, BTN IP. Predicted v3.4 output: BET (target — uncertain;
    pilot phase verifies).

    28 factory hands; 2 manual canonicals.
    """

    template_name = "T8primeR"
    generation_source = "t8prime_redesigned_non_nut_fd_checked_through_4way"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # Two-tone-clubs / hearts / spades / diamonds boards with hero
        # holding 2 of the FD suit (non-nut FD; no Ace of FD suit). Board
        # high card is K/Q/J/T (NOT Ace; avoid the As-public collapse).
        configs = [
            # 2-tone clubs (10 hands; Kx-club / Qx-club / Jx-club mix):
            ("9c8c", "Kh4c2c"),
            ("Tc9c", "Jh5c3c"),
            ("Tc8c", "Kd6c2c"),
            ("Jc9c", "Th4c3c"),
            ("Tc6c", "Kh4c3c"),
            ("8c7c", "Js5c4c"),
            ("Jc8c", "Th5c2c"),
            ("9c7c", "Kd6c2c"),
            ("Tc7c", "Jh4c3c"),
            ("Jc6c", "Th5c3c"),
            # 2-tone hearts (10 hands; suit-rotated mirror):
            ("9h8h", "Kc4h2h"),
            ("Th9h", "Jc5h3h"),
            ("Th8h", "Kd6h2h"),
            ("Jh9h", "Tc4h3h"),
            ("Th6h", "Kc4h3h"),
            ("8h7h", "Js5h4h"),
            ("Jh8h", "Tc5h2h"),
            ("9h7h", "Kd6h2h"),
            ("Th7h", "Jc4h3h"),
            ("Jh6h", "Tc5h3h"),
            # 2-tone spades + diamonds (8 hands):
            ("9s8s", "Kc4s2s"),
            ("Ts9s", "Jc5s3s"),
            ("Td9d", "Jc5d3d"),
            ("9d8d", "Kc4d2d"),
            ("Js9s", "Tc4s3s"),
            ("Jd9d", "Tc4d3d"),
            ("Ts7s", "Jc4s3s"),
            ("Td7d", "Jc4d3d"),
        ]
        out: List[GeneratedSituation] = []
        for i, (hero, board) in enumerate(configs[:target_count], start=1):
            sit_id = f"t8primeR_non_nut_fd_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=board,
                street="flop",
                hero_position="BTN",
                villain_positions=["HJ", "CO", "BB"],
                pot=10.5,
                to_call=0.0,
                facing_bet=False,
                num_opponents=3,
                prior_actions=[
                    "preflop: HJ raise 2.5",
                    "preflop: CO call",
                    "preflop: BTN call",
                    "preflop: BB call",
                    "flop: BB check",
                    "flop: HJ check",
                    "flop: CO check",
                ],
                generation_source=self.generation_source,
                opener_position="HJ",
                bettor_position=None,
                villain_aggression_count=0,
                villain_checked_back=1,
                villain_call_count=0,
                num_callers_to_bet=0,
                facing_raise=0,
                action_history=[
                    {"street": "flop", "actor": "BB", "action": "check"},
                    {"street": "flop", "actor": "HJ", "action": "check"},
                    {"street": "flop", "actor": "CO", "action": "check"},
                ],
            )
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        return out


# ─── T9'-expanded — TP-medium-kicker IP 4-way after PFR check (MW-40) ──


class T9PrimeExpanded(TemplateGenerator):
    """MW-40 family — 2.3× SCALE-UP from 12.5H T9' (14 → 32 hands).

    Same template structure; just more diverse parametric variants
    (different boards, different villain ranges, different opener positions).
    Discriminative axis (unchanged): is_made_hand=1, hand_category=6 (TP
    medium kicker), is_rainbow=1, villain_checked_back=1, num_opponents>=3.

    Predicted v3.4 output: BET unanimous (per existing 12.5H T9' precedent).

    32 factory hands; 1 manual canonical (MW-40 exact replica).
    """

    template_name = "T9primeE"
    generation_source = "t9prime_expanded_tp_medium_kicker_pfr_check_4way"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # NEW A-high and K-high rainbow boards distinct from 12.5H T9'
        # (which used As6c2d, As7d3c, Ad7s3h, Ad8c4s, Ah4d2c, Ah6c2s,
        # As9c4d, Kd7s2c, Kc8d3h, Kh8c2d, Kc9s3d, Ks6d2c).
        configs = [
            # A-high rainbow + T or J kicker (16 hands):
            ("AhTd", "Ac6s4d"),
            ("AhJd", "Ac6s4d"),
            ("AhTd", "As7c2d"),
            ("AhJd", "As7c2d"),
            ("AdTh", "Ac8s3d"),
            ("AdJh", "Ac8s3d"),
            ("AsTh", "Ad9c2s"),
            ("AsJh", "Ad9c2s"),
            ("AcTh", "Ad8s4c"),
            ("AcJh", "Ad8s4c"),
            ("AhTd", "Ac8s5d"),
            ("AhJd", "Ac9s2d"),
            ("AhTd", "As4c2d"),
            ("AhJd", "As9c4d"),
            ("AhTd", "Ad7c2s"),
            ("AhJd", "Ad8c3s"),
            # K-high rainbow + T or J kicker (16 hands):
            ("KhTd", "Kc6s4d"),
            ("KhJd", "Kc6s4d"),
            ("KhTd", "Ks7c2d"),
            ("KhJd", "Ks7c2d"),
            ("KdTh", "Kc8s3d"),
            ("KdJh", "Kc8s3d"),
            ("KsTh", "Kd9c2s"),
            ("KsJh", "Kd9c2s"),
            ("KcTh", "Kd8s4c"),
            ("KcJh", "Kd8s4c"),
            ("KhTd", "Kc8s5d"),
            ("KhJd", "Kc9s2d"),
            ("KhTd", "Ks4c2d"),
            ("KhJd", "Ks9c4d"),
            ("KhTd", "Kd7c2s"),
            ("KhJd", "Kd8c3s"),
        ]
        out: List[GeneratedSituation] = []
        for i, (hero, board) in enumerate(configs[:target_count], start=1):
            sit_id = f"t9primeE_tp_med_kicker_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=board,
                street="flop",
                hero_position="BTN",
                villain_positions=["HJ", "CO", "BB"],
                pot=11.0,
                to_call=0.0,
                facing_bet=False,
                num_opponents=3,
                prior_actions=[
                    "preflop: HJ raise 2.5",
                    "preflop: CO call",
                    "preflop: BTN call",
                    "preflop: BB call",
                    "flop: BB check",
                    "flop: HJ check",
                    "flop: CO check",
                ],
                generation_source=self.generation_source,
                opener_position="HJ",
                bettor_position=None,
                villain_aggression_count=0,
                villain_checked_back=1,
                villain_call_count=0,
                num_callers_to_bet=0,
                facing_raise=0,
                action_history=[
                    {"street": "flop", "actor": "BB", "action": "check"},
                    {"street": "flop", "actor": "HJ", "action": "check"},
                    {"street": "flop", "actor": "CO", "action": "check"},
                ],
            )
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        return out


# ─── T10'-redesigned — slowplay set + broadway-completed turn (MW-45) ──


class T10PrimeRedesigned(TemplateGenerator):
    """MW-45 family — REDESIGNED at 12.5I-B per per-hand diagnostic verdict
    (isomorph-mismatch + E-DIST secondary).

    12.5H T10' parametric used non-broadway-completed turn cards (Td/Tc/Js/
    Jd/Qc) — they don't match MW-45's specific AKQx broadway-completed
    pattern. Model didn't transfer.

    T10'-redesigned constraint: turn card BROADWAY-COMPLETING (Q on AK6
    flop; J on AKQ/AK6 flop; etc.). Bottom-set or middle-set on rainbow
    flop with broadway-rich textures.

    Discriminative axis: hand_category=12 (set), is_monster=1, street=turn,
    villain_aggression_count=1, num_callers_to_bet>=1, num_opponents>=2,
    turn brings broadway-straight or broadway-completing card.

    30 factory hands; 1 manual canonical (MW-45 exact replica).
    """

    template_name = "T10primeR"
    generation_source = "t10prime_redesigned_slowplay_set_broadway_turn_4way"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # Each entry: (hero, flop, turn, leader_pos, lead_size)
        configs = [
            # Bottom-set on AK6 flop + Q broadway turn (8 hands):
            ("6c6d", "AcKd6h", "Qs", "CO", 12.0),
            ("6c6s", "AcKd6h", "Qs", "CO", 12.0),
            ("6d6s", "AcKd6h", "Qs", "CO", 12.0),
            ("6h6d", "AcKh6c", "Qs", "CO", 12.0),
            ("6h6s", "AcKh6c", "Qs", "CO", 12.0),
            ("6d6s", "AcKh6c", "Qs", "CO", 12.0),
            ("6c6d", "AsKh6s", "Qc", "CO", 14.0),
            ("6c6h", "AsKh6s", "Qc", "CO", 14.0),
            # Bottom-set on AK5 flop + Q turn (extension; 4 hands):
            ("5c5d", "AcKd5h", "Qs", "CO", 12.0),
            ("5c5s", "AcKd5h", "Qs", "CO", 12.0),
            ("5h5d", "AcKh5s", "Qc", "CO", 12.0),
            ("5h5s", "AsKd5c", "Qh", "CO", 12.0),
            # Bottom-set on KQ6 flop + J broadway turn (6 hands):
            ("6c6d", "KsQd6h", "Jc", "CO", 12.0),
            ("6c6s", "KsQd6h", "Jc", "CO", 12.0),
            ("6d6s", "KsQd6h", "Jc", "CO", 12.0),
            ("6h6d", "KsQc6s", "Jh", "CO", 12.0),
            ("6h6c", "KsQc6s", "Jh", "CO", 12.0),
            ("6c6d", "KdQs6h", "Jc", "CO", 14.0),
            # Middle-set on AKx flop + broadway turn (6 hands):
            ("7d7c", "AcKd7h", "Qs", "CO", 14.0),
            ("7d7s", "AcKd7h", "Qs", "CO", 14.0),
            ("7c7s", "AcKd7h", "Qs", "CO", 14.0),
            ("8c8d", "AcKh8s", "Qd", "CO", 14.0),
            ("8c8h", "AcKh8s", "Qd", "CO", 14.0),
            ("8d8h", "AcKh8s", "Qd", "CO", 14.0),
            # Middle-set on KQx flop + broadway turn (4 hands):
            ("9c9d", "KsQd9h", "Jc", "CO", 14.0),
            ("9c9h", "KsQd9h", "Jc", "CO", 14.0),
            ("9d9h", "KsQd9h", "Jc", "CO", 14.0),
            ("8c8d", "KsQd8h", "Jc", "HJ", 14.0),
            # Bottom-set on KQ7 flop + J broadway turn (2 hands):
            ("7c7d", "KsQd7h", "Jc", "CO", 14.0),
            ("7c7s", "KsQd7h", "Jc", "CO", 14.0),
        ]
        out: List[GeneratedSituation] = []
        for i, (hero, flop, turn, leader, size) in enumerate(configs[:target_count], start=1):
            board = flop + turn
            sit_id = f"t10primeR_slowplay_set_broadway_{i:02d}"
            other_caller = "CO" if leader != "CO" else "HJ"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=board,
                street="turn",
                hero_position="BB",
                villain_positions=[leader, other_caller, "BTN"],
                pot=10.5 + size + size,
                to_call=size,
                facing_bet=True,
                num_opponents=3,
                prior_actions=[
                    f"preflop: {leader} raise 2.5",
                    f"preflop: {other_caller} call",
                    "preflop: BTN call",
                    "preflop: BB call",
                    f"flop: {leader} check",
                    f"flop: {other_caller} check",
                    "flop: BTN check",
                    "flop: BB check",
                    f"turn: {leader} bet {size:g}",
                    f"turn: {other_caller} fold",
                    "turn: BTN call",
                ],
                generation_source=self.generation_source,
                opener_position=leader,
                bettor_position=leader,
                villain_aggression_count=1,
                villain_checked_back=0,
                villain_call_count=1,
                num_callers_to_bet=1,
                facing_raise=0,
                action_history=[
                    {"street": "flop", "actor": leader, "action": "check"},
                    {"street": "flop", "actor": other_caller, "action": "check"},
                    {"street": "flop", "actor": "BTN", "action": "check"},
                    {"street": "flop", "actor": "BB", "action": "check"},
                    {"street": "turn", "actor": leader, "action": "bet", "size": size},
                    {"street": "turn", "actor": other_caller, "action": "fold"},
                    {"street": "turn", "actor": "BTN", "action": "call"},
                ],
            )
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        return out


# ─── 4 manual canonicals (Track B per design §5) ──────────────────────


PILOT_ID_START_MANUAL = 785  # 785..788 = 4 manual canonicals


_MANUALS: List[Dict[str, Any]] = [
    # T8'-redesigned canonical 01 — MW-25 EXACT REPLICA
    {
        "template": "T8primeR",
        "situation_id": "t8primeR_manual_canonical_01_mw25_exact",
        "author_design_note": (
            "MW-25 EXACT replica per BATCH2 reference set: hero Ks7s on As9s5d "
            "monotone-spade flop with As public, BTN IP 4-way checked through. "
            "BATCH2 expert says BET (denial + thin value despite hero K-FD "
            "dominated by villain's spades). v3.4 + 12.5H T8' corpus + model "
            "all align on CHECK on this pattern (per 12.5I-pre §'Cross-hand "
            "patterns'). This canonical is the protocol-vs-reference disagreement "
            "anchor; pilot phase MUST verify which prediction wins. If labellers "
            "produce CHECK consensus, route to orchestrator with BATCH2 reference "
            "re-evaluation question (the open question raised in 12.5I-A §9)."
        ),
        "kwargs": dict(
            hero_cards="Ks7s", board="As9s5d", street="flop", hero_position="BTN",
            villain_positions=["HJ", "CO", "BB"], pot=10.5, to_call=0.0,
            facing_bet=False, num_opponents=3,
            prior_actions=["preflop: HJ raise 2.5", "preflop: CO call",
                           "preflop: BTN call", "preflop: BB call",
                           "flop: BB check", "flop: HJ check", "flop: CO check"],
            generation_source="t8primeR_manual_canonical_mw25_exact",
            opener_position="HJ", bettor_position=None,
            villain_aggression_count=0, villain_checked_back=1,
            villain_call_count=0, num_callers_to_bet=0, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "HJ", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "check"},
            ],
        ),
    },
    # T8'-redesigned canonical 02 — non-nut-FD contrast variant
    {
        "template": "T8primeR",
        "situation_id": "t8primeR_manual_canonical_02_non_nut_fd",
        "author_design_note": (
            "Contrast variant for T8'-redesigned: hero Tc9c on Qh5c3c two-tone "
            "clubs, BTN IP 4-way checked through. Q-high two-tone flop with "
            "hero as broadway-connector + non-nut clubs FD (no nut blocker, no "
            "on-board overcards above the T). v3.4 prediction: BET (denial + "
            "thin value via fold equity from three checks). This is the "
            "cleanest non-nut-FD-with-no-As-public configuration; pilot label "
            "informs whether v3.4 routes such hands to BET (target) or CHECK "
            "(concerning). Board chosen distinct from any T8'-redesigned "
            "parametric to avoid fingerprint collision."
        ),
        "kwargs": dict(
            hero_cards="Tc9c", board="Qh5c3c", street="flop", hero_position="BTN",
            villain_positions=["HJ", "CO", "BB"], pot=10.5, to_call=0.0,
            facing_bet=False, num_opponents=3,
            prior_actions=["preflop: HJ raise 2.5", "preflop: CO call",
                           "preflop: BTN call", "preflop: BB call",
                           "flop: BB check", "flop: HJ check", "flop: CO check"],
            generation_source="t8primeR_manual_canonical_non_nut_fd",
            opener_position="HJ", bettor_position=None,
            villain_aggression_count=0, villain_checked_back=1,
            villain_call_count=0, num_callers_to_bet=0, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "HJ", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "check"},
            ],
        ),
    },
    # T9'-expanded canonical — MW-40 EXACT REPLICA
    {
        "template": "T9primeE",
        "situation_id": "t9primeE_manual_canonical_01_mw40_exact",
        "author_design_note": (
            "MW-40 EXACT replica per BATCH2 reference set: hero AhTs on AdJc5h "
            "RAINBOW (note: 12.5H PILOT_691 used AcJc5d which is 2-tone clubs; "
            "this 12.5I canonical fixes to true rainbow per MW-40 spec), BTN IP "
            "4-way checked through 200bb deep. Expert: BET MEDIUM (TPGK on "
            "rainbow A-high after 4-way check-through; protect + thin value at "
            "high SPR multiway). Predicted v3.4: BET (per existing T9' family "
            "pattern; PILOT_691 was BET 4/5 in 12.5H-C)."
        ),
        "kwargs": dict(
            hero_cards="AhTs", board="AdJc5h", street="flop", hero_position="BTN",
            villain_positions=["HJ", "CO", "BB"], pot=11.0, to_call=0.0,
            facing_bet=False, num_opponents=3,
            prior_actions=["preflop: HJ raise 2.5", "preflop: CO call",
                           "preflop: BTN call", "preflop: BB call",
                           "flop: BB check", "flop: HJ check", "flop: CO check"],
            generation_source="t9primeE_manual_canonical_mw40_exact",
            opener_position="HJ", bettor_position=None,
            villain_aggression_count=0, villain_checked_back=1,
            villain_call_count=0, num_callers_to_bet=0, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "HJ", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "check"},
            ],
        ),
    },
    # T10'-redesigned canonical — MW-45-adjacent (suit-rotated)
    # Note: MW-45 exact replica (6d6c on AcKd6hQs) is already in the combined
    # corpus as 12.5H PILOT_692 (RAISE 5/5 in 12.5H-C). Re-using exact replica
    # would be a fingerprint duplicate. This canonical is suit-rotated to
    # preserve the AKx-broadway-completed-turn axis with a unique fingerprint.
    {
        "template": "T10primeR",
        "situation_id": "t10primeR_manual_canonical_01_mw45_adjacent",
        "author_design_note": (
            "MW-45 family canonical (suit-rotated; the EXACT replica 6d6c on "
            "AcKd6hQs is already PILOT_692 in 12.5H corpus). This canonical is "
            "6d6s on AsKh6cQd: bottom set on rainbow A-K-6 flop; turn Q "
            "completes broadway. Same MW-45 family axis; same expert RAISE "
            "reasoning (set + protect vs straight-completed range; MW-33 anchor "
            "applies). v3.4 prediction: RAISE (per existing T10' family in 12.5H). "
            "Suit rotation chosen specifically to differ from PILOT_692's exact "
            "fingerprint while preserving discriminative axis."
        ),
        "kwargs": dict(
            hero_cards="6d6s", board="AsKh6cQd", street="turn", hero_position="BB",
            villain_positions=["CO", "BTN", "SB"], pot=35.0, to_call=12.0,
            facing_bet=True, num_opponents=3,
            prior_actions=["preflop: CO raise 2.5", "preflop: BTN call",
                           "preflop: SB call", "preflop: BB call",
                           "flop: SB check", "flop: BB check",
                           "flop: CO check", "flop: BTN check",
                           "turn: SB check", "turn: BB check",
                           "turn: CO bet 12", "turn: BTN call", "turn: SB fold"],
            generation_source="t10primeR_manual_canonical_mw45_exact",
            opener_position="CO", bettor_position="CO",
            villain_aggression_count=1, villain_checked_back=0,
            villain_call_count=1, num_callers_to_bet=1, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "SB", "action": "check"},
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "check"},
                {"street": "flop", "actor": "BTN", "action": "check"},
                {"street": "turn", "actor": "SB", "action": "check"},
                {"street": "turn", "actor": "BB", "action": "check"},
                {"street": "turn", "actor": "CO", "action": "bet", "size": 12.0},
                {"street": "turn", "actor": "BTN", "action": "call"},
                {"street": "turn", "actor": "SB", "action": "fold"},
            ],
        ),
    },
]


def generate_manuals() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    pid = PILOT_ID_START_MANUAL
    for m in _MANUALS:
        kwargs = dict(m["kwargs"])
        kwargs["situation_id"] = m["situation_id"]
        kwargs["pilot_hand_id"] = f"PILOT_{pid:03d}"
        row = emit_row(**kwargs)
        row["author_design_note"] = m["author_design_note"]
        row["template"] = m["template"]
        rows.append(row)
        pid += 1
    if pid - 1 != PILOT_ID_END:
        raise RuntimeError(
            f"Expected last manual pilot_hand_id = PILOT_{PILOT_ID_END:03d}; "
            f"got PILOT_{(pid - 1):03d}"
        )
    return rows


# ─── Generation harness ───────────────────────────────────────────────


_TEMPLATES = [
    ("T8primeR", T8PrimeRedesigned(), 28),
    ("T9primeE", T9PrimeExpanded(), 32),
    ("T10primeR", T10PrimeRedesigned(), 30),
]


def generate_all_parametric() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    pid = PILOT_ID_START
    for tname, gen, count in _TEMPLATES:
        produced = gen.generate(count)
        if len(produced) != count:
            raise RuntimeError(
                f"Template {tname} produced {len(produced)}/{count} situations"
            )
        for s in produced:
            s.row["pilot_hand_id"] = f"PILOT_{pid:03d}"
            pid += 1
            rows.append(s.row)
    if pid - 1 != PILOT_PARAMETRIC_END:
        raise RuntimeError(
            f"Expected last parametric pilot_hand_id = PILOT_{PILOT_PARAMETRIC_END:03d}; "
            f"got PILOT_{(pid - 1):03d}"
        )
    return rows


# ─── G1-G3 self-checks ────────────────────────────────────────────────


def g1_join_cardinality(new_rows: List[Dict[str, Any]], existing_corpus_path: str):
    new_ids = [r["pilot_hand_id"] for r in new_rows]
    if len(set(new_ids)) != len(new_ids):
        from collections import Counter
        dups = [k for k, v in Counter(new_ids).items() if v > 1]
        return False, f"G1 FAIL: dup pilot_hand_ids: {dups[:5]}"
    if len(new_ids) != GRAND_TOTAL:
        return False, f"G1 FAIL: expected {GRAND_TOTAL} new rows; got {len(new_ids)}"
    if not os.path.exists(existing_corpus_path):
        return True, "G1 PARTIAL: existing corpus not found"
    existing_ids = set()
    with open(existing_corpus_path) as f:
        for line in f:
            if line.strip():
                existing_ids.add(json.loads(line).get("pilot_hand_id"))
    collision = set(new_ids) & existing_ids
    if collision:
        return False, f"G1 FAIL: pilot_hand_id collision: {sorted(collision)[:5]}"
    return True, f"G1 PASS: {len(new_ids)} unique; 0 collisions vs existing {len(existing_ids)}"


def g2_distribution(new_rows):
    targets = {"T8primeR": 30, "T9primeE": 33, "T10primeR": 31}
    def _tkey(sid: str) -> str:
        if sid.startswith("t8primeR"): return "T8primeR"
        if sid.startswith("t9primeE"): return "T9primeE"
        if sid.startswith("t10primeR"): return "T10primeR"
        return "?"
    found = {k: 0 for k in targets}
    for r in new_rows:
        k = _tkey(r["situation_id"])
        if k in found:
            found[k] += 1
    deviations = []
    for tname, want in targets.items():
        got = found[tname]
        if abs(got - want) > 2:
            deviations.append(f"{tname}: {got}/{want} (Δ{got - want:+d})")
    if deviations:
        return False, f"G2 FAIL: {', '.join(deviations)}"
    deltas = ", ".join(f"{t}={found[t]}/{targets[t]}" for t in targets)
    return True, f"G2 PASS: {deltas}"


def g3_duplicate_detection(new_rows, existing_corpus_path):
    def _fingerprint(r):
        return (
            r.get("board"),
            r.get("hero_cards"),
            r.get("hero_position"),
            tuple(r.get("prior_actions") or []),
        )
    new_fps = [_fingerprint(r) for r in new_rows]
    seen = {}
    internal_dups = []
    for r, fp in zip(new_rows, new_fps):
        if fp in seen:
            internal_dups.append((seen[fp], r["pilot_hand_id"]))
        else:
            seen[fp] = r["pilot_hand_id"]
    if internal_dups:
        return False, f"G3 FAIL (internal): {internal_dups[:3]}"
    if not os.path.exists(existing_corpus_path):
        return True, "G3 PARTIAL: existing corpus not found"
    existing_fps = set()
    with open(existing_corpus_path) as f:
        for line in f:
            if line.strip():
                existing_fps.add(_fingerprint(json.loads(line)))
    matches = [r["pilot_hand_id"] for r in new_rows if _fingerprint(r) in existing_fps]
    if matches:
        return False, f"G3 FAIL: {len(matches)} dup vs existing 694: {matches[:5]}"
    return True, f"G3 PASS: 0 (board, hero, position, prior_actions) duplicates vs existing 694; 0 internal duplicates"


# ─── CLI ──────────────────────────────────────────────────────────────


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Phase 12.5I-B situation generator (~94 hands across 3 redesigned templates)"
    )
    p.add_argument(
        "--output",
        default="data/corpus_revision_125i_situations_2026-05-06.jsonl",
    )
    p.add_argument(
        "--manual-output",
        default="data/corpus_revision_125i_manual_canonicals_2026-05-06.jsonl",
    )
    p.add_argument(
        "--existing-corpus",
        default="data/corpus_combined_694_2026-05-06.jsonl",
        help="Existing 694-hand combined corpus path (G1 + G3 reference)",
    )
    p.add_argument("--strict", action="store_true",
        help="Exit non-zero if any G1-G3 self-check fails")
    args = p.parse_args(argv)

    out_abs = args.output if os.path.isabs(args.output) else os.path.join(_REPO, args.output)
    manual_abs = args.manual_output if os.path.isabs(args.manual_output) else os.path.join(_REPO, args.manual_output)
    existing_abs = args.existing_corpus if os.path.isabs(args.existing_corpus) else os.path.join(_REPO, args.existing_corpus)

    print(f"[gen] generating {PARAMETRIC_TOTAL} parametric situations ...", file=sys.stderr)
    parametric_rows = generate_all_parametric()
    print(f"[gen] generated {len(parametric_rows)} parametric rows", file=sys.stderr)

    print(f"[gen] generating {MANUAL_TOTAL} manual canonical hands ...", file=sys.stderr)
    manual_rows = generate_manuals()
    print(f"[gen] generated {len(manual_rows)} manual rows", file=sys.stderr)

    combined = parametric_rows + manual_rows

    print(f"[gen] running G1-G3 self-checks (combined {len(combined)} rows) ...", file=sys.stderr)
    g1_ok, g1_msg = g1_join_cardinality(combined, existing_abs)
    g2_ok, g2_msg = g2_distribution(combined)
    g3_ok, g3_msg = g3_duplicate_detection(combined, existing_abs)
    print(f"  {g1_msg}", file=sys.stderr)
    print(f"  {g2_msg}", file=sys.stderr)
    print(f"  {g3_msg}", file=sys.stderr)

    os.makedirs(os.path.dirname(out_abs), exist_ok=True)
    with open(out_abs, "w") as f:
        for r in parametric_rows:
            f.write(json.dumps(r) + "\n")
    print(f"[gen] wrote {out_abs}", file=sys.stderr)

    os.makedirs(os.path.dirname(manual_abs), exist_ok=True)
    with open(manual_abs, "w") as f:
        for r in manual_rows:
            f.write(json.dumps(r) + "\n")
    print(f"[gen] wrote {manual_abs}", file=sys.stderr)

    if args.strict and not (g1_ok and g2_ok and g3_ok):
        print("[gen] STRICT mode: G1-G3 failure(s) → exiting non-zero", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
