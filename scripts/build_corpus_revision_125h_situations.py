#!/usr/bin/env python3
"""Phase 12.5H-B situation generator — 90 new hands across 6 templates.

Implements 12.5H-A design (`review/comms/PLAN_PHASE125H_CORPUS_EXPANSION_2026-05-06.md`,
master `858b032`) per Phase 12.5H-B dispatch
(`review/comms/MAIN_TERMINAL_PHASE125H_B_DISPATCH_2026-05-06.md`,
master `8c90649`).

Re-uses helpers from `scripts/build_corpus_revision_125e_situations.py`
(master `858b032`) — `emit_row`, `build_hand_dict`,
`_hero_only_prior_actions`, `TemplateGenerator`, `GeneratedSituation`,
G1-G3 self-checks. Dispatch §"Methodology rules" item 1: hero-only
convention applies uniformly. Item 3: T-CONTROL hands include explicit
`design_action` field per QC's TC-X T8 schema gap fix.

Templates per design §3:
- T8' (18 = 16 factory + 2 manual): monotone-flop FD checked-through 4-way (MW-25)
- T9' (14 = 13 + 1): TP-medium-kicker IP 4-way after PFR check (MW-40)
- T10' (14 = 13 + 1): slowplayed set into turn lead 4-way (MW-45)
- T7-ext (12 = 11 + 1): NFD+overcards CALL implied-odds (MW-17)
- T-RAISE-stabilize (12 = 11 + 1): bet+call multiway villain_air ≥0.05 (MW-47 + 60/40 fix)
- T-CONTROL (20 factory): mixed bucket controls + design_action

Total: 84 factory + 6 manual = 90 hands. pilot_hand_id range
PILOT_605..PILOT_694.

Output schema mirrors data/corpus_combined_604_2026-05-05.jsonl (cohort 2
plus 12.5E-B columns). T-CONTROL rows additionally include `design_action`.

Usage:
    python3 scripts/build_corpus_revision_125h_situations.py
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

# Re-use 12.5E-B factory's helpers (master 858b032) verbatim — they
# implement the canonical row schema, hero-only convention filter,
# and emit_row pipeline. This keeps 12.5H-B focused on new templates.
from build_corpus_revision_125e_situations import (  # noqa: E402
    GeneratedSituation,
    TemplateGenerator,
    emit_row,
)

PILOT_ID_START = 605  # continues PILOT_001..PILOT_604
PILOT_PARAMETRIC_END = 688  # 605..688 = 84 parametric hands
PILOT_ID_END = 694  # 689..694 = 6 manual canonicals; total 90

PARAMETRIC_TOTAL = 84
MANUAL_TOTAL = 6
GRAND_TOTAL = 90


# ─── T8' — monotone-flop FD checked-through 4-way (MW-25 family) ──────


class T8PrimeMonotoneFDCheckedThrough(TemplateGenerator):
    """MW-25 family expansion. Discriminative axis: is_monotone=1,
    has_flush_draw=1, num_opponents>=3, villain_aggression_count=0,
    is_paired=0. Includes K-high FD (not just nut FD) per design §3.

    16 factory hands; 2 manual canonicals authored separately.
    """

    template_name = "T8prime"
    generation_source = "t8prime_monotone_fd_checked_through_4way"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # 12.5E-B's t1_monotone_fd_checked_through_4way (PILOT_495..506) used
        # monotone-spades boards Js8s5s, Ts7s4s, 9s6s3s, Qs8s4s with NFD+K/Q
        # overcard heros. T8' expands the family with NEW boards (different
        # spade textures + suit-rotated equivalents on hearts/diamonds/clubs)
        # so labellers see the discriminative axis on a wider corpus.
        configs = [
            # NEW spade-monotone boards (texture variants):
            ("Js", "9s", "4s", ["Ks", "Qh"]),  # K-high FD + Q overcard
            ("Js", "9s", "4s", ["As", "Tc"]),  # NFD + T (board high J → T not over)
            ("Ts", "8s", "4s", ["Ks", "Jh"]),  # K-high FD + J overcard
            ("Ts", "8s", "4s", ["As", "Kd"]),  # NFD + K overcard
            ("9s", "7s", "3s", ["As", "Jh"]),  # NFD + J overcard
            ("9s", "7s", "3s", ["Ks", "Qc"]),  # K-high FD + Q overcard
            ("Qs", "7s", "3s", ["Ks", "Th"]),  # K-high FD + T overcard
            ("Qs", "7s", "3s", ["As", "Jd"]),  # NFD + J overcard
            # Suit-rotated hearts variants (monotone hearts):
            ("Jh", "8h", "5h", ["Ah", "Kc"]),  # NFD hearts + K overcard
            ("Jh", "8h", "5h", ["Kh", "Qc"]),  # K-high heart FD + Q overcard
            ("Th", "7h", "4h", ["Ah", "Jc"]),  # NFD hearts + J overcard
            ("Th", "7h", "4h", ["Kh", "Jc"]),  # K-high heart FD + J overcard
            ("9h", "6h", "3h", ["Ah", "Kc"]),  # NFD hearts over-the-world
            # Suit-rotated diamonds variants (monotone diamonds):
            ("Jd", "8d", "5d", ["Ad", "Kc"]),  # NFD diamonds + K overcard
            ("Jd", "8d", "5d", ["Kd", "Qc"]),  # K-high diamond FD + Q overcard
            ("9d", "6d", "3d", ["Ad", "Jc"]),  # NFD diamonds + J overcard
        ]
        out: List[GeneratedSituation] = []
        for i, (bh, bm, bl, hero) in enumerate(configs[:target_count], start=1):
            board = bh + bm + bl
            hero_str = "".join(hero)
            sit_id = f"t8prime_monotone_fd_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero_str,
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


# ─── T9' — TP-medium-kicker IP 4-way after PFR check (MW-40 family) ───


class T9PrimeTPMediumKickerAfterPFRCheck(TemplateGenerator):
    """MW-40 family expansion. Discriminative axis: is_made_hand=1,
    is_rainbow=1, villain_checked_back=1, num_opponents>=2.

    13 factory hands; 1 manual canonical.
    """

    template_name = "T9prime"
    generation_source = "t9prime_tp_medium_kicker_pfr_check_4way"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # 12.5E-B's t2_tp_medium_kicker_pfr_check_4way (PILOT_507..516) used
        # boards As7d3c, Ad8c4s, Ks6d2c, Kc9s3d, Ah6c2s with AhTs/AhJs/etc
        # heros. MW-40 exact replica (AhTs on AcJc5d) is the manual canonical
        # PILOT_691. T9' parametric covers NEW A-high and K-high rainbow
        # boards with TP T/J kicker heros.
        configs = [
            # NEW A-high rainbow boards:
            ("As6c2d", "AhTd"),  # A-high, T kicker
            ("As6c2d", "AhJh"),  # A-high, J kicker
            ("Ad7s3h", "AcTs"),  # A-high, T kicker
            ("Ad7s3h", "AcJh"),  # A-high, J kicker
            ("Ah4d2c", "AsTh"),  # A-high low texture, T kicker
            ("Ah4d2c", "AsJh"),  # A-high low texture, J kicker
            ("As9c4d", "AhTs"),  # A-high mid 9, T kicker
            ("As9c4d", "AhJs"),  # A-high mid 9, J kicker
            # NEW K-high rainbow boards:
            ("Kd7s2c", "KsTh"),  # K-high, T kicker
            ("Kd7s2c", "KsJh"),  # K-high, J kicker
            ("Kc8d3h", "KdTc"),  # K-high mid 8, T kicker
            ("Kc8d3h", "KdJc"),  # K-high mid 8, J kicker
            ("Kh8c2d", "KsTh"),  # K-high low texture, T kicker
        ]
        out: List[GeneratedSituation] = []
        for i, (board, hero) in enumerate(configs[:target_count], start=1):
            sit_id = f"t9prime_tp_med_kicker_{i:02d}"
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


# ─── T10' — slowplayed set into turn lead 4-way (MW-45 family) ────────


class T10PrimeSlowplaySetTurnLead(TemplateGenerator):
    """MW-45 family expansion. Discriminative axis: hand_category=set,
    street=turn, villain just bet, num_opponents>=2. Slowplay-then-raise
    on turn-lead pattern.

    13 factory hands; 1 manual canonical (66 set on AcKd6h-Q exact replica).
    """

    template_name = "T10prime"
    generation_source = "t10prime_slowplay_set_turn_lead_4way"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # 12.5E-B's t4_slowplay_set_turn_lead_4way (PILOT_527..538) covered set
        # ranks 33-99 on rainbow flops with various broadway turns. MW-45 exact
        # replica (6d6c on AcKd6hQs) is the manual canonical PILOT_692. T10'
        # parametric uses NEW (hero, flop, turn) combinations distinct from
        # the existing 12 and the MW-45 board.
        # Each entry: (hero, flop, turn, leader_pos, lead_size)
        configs = [
            # Set-rank variations on NEW flop+turn combinations:
            ("9s9c", "9h6c2s", "Td", "CO", 12.0),  # different flop suits + turn
            ("8s8d", "8c4h2s", "Js", "HJ", 14.0),  # different flop+turn
            ("7d7c", "7s4h2d", "Tc", "CO", 16.0),  # different flop+turn
            ("6s6c", "6d4h2s", "Td", "CO", 12.0),  # MW-45-adjacent rank, different texture
            ("5d5h", "5s4c2h", "Js", "CO", 14.0),  # different flop+turn
            ("4c4d", "4s5h2c", "Js", "BTN", 12.0),  # different flop+turn
            ("3s3d", "3h4c2d", "Qc", "CO", 14.0),  # different flop+turn
            ("9s9d", "9c5h2s", "Jd", "CO", 14.0),  # different texture
            ("8d8c", "8h7s3c", "Td", "HJ", 14.0),  # different texture
            ("7s7c", "7h5d2c", "Jd", "CO", 14.0),  # different texture
            ("6h6d", "6s5c2h", "Tc", "CO", 12.0),  # different from PILOT_530/538
            ("9h9c", "9d8s4h", "Tc", "HJ", 14.0),  # different texture from PILOT_532
            ("5h5c", "5d6c2s", "Tc", "CO", 14.0),  # different texture from PILOT_531
        ]
        out: List[GeneratedSituation] = []
        for i, (hero, flop, turn, leader, size) in enumerate(configs[:target_count], start=1):
            board = flop + turn
            sit_id = f"t10prime_slowplay_set_{i:02d}"
            other_caller = "CO" if leader != "CO" else "HJ"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=board,
                street="turn",
                hero_position="BB",
                villain_positions=[leader, other_caller, "BTN"],
                # 4-way preflop pot 10.5; flop checked through; turn lead = size
                # Hero (BB) faces CO bet + BTN call + (need to add) other-caller
                # action — for cleanliness assume BTN calls; SB folded; hero next.
                pot=10.5 + size + size,  # hero faces bet + 1 caller's call
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
                villain_aggression_count=1,  # leader just bet turn
                villain_checked_back=0,
                villain_call_count=1,  # BTN just called
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


# ─── T7-ext — NFD+overcards CALL under pot odds (MW-17 family) ────────


class T7ExtNFDOvercardsCall(TemplateGenerator):
    """MW-17 family expansion. Discriminative axis: has_flush_draw=1
    (or nut blocker w/o FD) + 1-2 overcards + is_ip=0 + num_opponents=2
    (single-bet 3-way).

    11 factory hands; 1 manual canonical.
    """

    template_name = "T7ext"
    generation_source = "t7ext_nfd_overcards_call_pot_odds"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # 12.5E T7 hands all had Ah/Ad/As/Ac + matching FD-suit hole cards.
        # T7-ext expands with: (a) MW-17-exact replica AdKs on Jd8d4c-style
        # board (NFD + K overcard, OOP facing single bet 3-way); (b) variant
        # boards covering implied-odds range; (c) blocker-without-FD variants
        # so labellers reason from composition not just pot odds.
        configs = [
            # MW-17 exact-replica is the manual canonical PILOT_693 (AdKs on
            # Jd8d4c). Parametric set covers adjacent NFD+overcard variants on
            # broadway 2-tone boards across all four suits + slight texture
            # variations, leaving the literal MW-17 board for the canonical.
            ("AcKd", "Jc8c4d", 5.0),  # NFD clubs + K overcard
            ("AhKc", "Jh8h4d", 5.0),  # NFD hearts + K overcard
            ("AsKd", "Js8s4d", 5.0),  # NFD spades + K overcard
            # Q-overcard variants:
            ("AhQs", "Th8h4d", 5.0),
            ("AdQc", "Td8d4c", 5.0),
            # AJ + nut-FD on Q-high 2-tone (J overcard for second pair potential):
            ("AhJs", "Qh8h4d", 5.0),
            ("AdJh", "Qd8d4c", 5.0),
            # Different implied-odds price points (slightly larger bet):
            ("AhKs", "Jh8h3c", 6.0),  # bigger bet = tighter pot odds
            ("AdQs", "Td8d3c", 6.0),
            # Blocker-only variants (no FD; pure overcard + nut blocker reasoning):
            ("AdKs", "Jh8h4c", 5.0),  # Ad on J-high heart 2-tone — nut diamond blocker but no FD
            ("AsQd", "Th8h4c", 5.0),  # As on T-high heart 2-tone — nut spade blocker, no FD
        ]
        out: List[GeneratedSituation] = []
        for i, (hero, flop, bet_size) in enumerate(configs[:target_count], start=1):
            sit_id = f"t7ext_nfd_overcards_call_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=flop,
                street="flop",
                hero_position="BB",
                villain_positions=["CO", "BTN"],
                pot=8.0 + bet_size,
                to_call=bet_size,
                facing_bet=True,
                num_opponents=2,
                prior_actions=[
                    "preflop: CO raise 2.5",
                    "preflop: BTN call",
                    "preflop: BB call",
                    "flop: BB check",
                    f"flop: CO bet {bet_size:g}",
                    "flop: BTN fold",
                ],
                generation_source=self.generation_source,
                opener_position="CO",
                bettor_position="CO",
                villain_aggression_count=1,
                villain_checked_back=0,
                villain_call_count=0,
                num_callers_to_bet=0,
                facing_raise=0,
                action_history=[
                    {"street": "flop", "actor": "BB", "action": "check"},
                    {"street": "flop", "actor": "CO", "action": "bet", "size": bet_size},
                    {"street": "flop", "actor": "BTN", "action": "fold"},
                ],
            )
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        return out


# ─── T-RAISE-stabilize — bet+call multiway, villain_air ≥0.05 ─────────


class TRaiseStabilize(TemplateGenerator):
    """MW-47 family + 12.5H-pre 60/40 bimodal seed-volatility fix.
    Discriminative axis: nut_flush_block=1, has_flush_draw=1,
    num_callers_to_bet>=1, villain_aggression_count==1, is_ip=0,
    villain_air_pct >= 0.05 (clause-e satisfied per v3.4 carve-out).

    11 factory hands; 1 manual canonical (MW-47 exact AsQs on KsJd5s).

    Per design §3 T-RAISE-stabilize: prefer spades/diamonds/clubs
    variants over heart-suit broadway-saturated boards (heart variants
    in 12.5E-C produced villain_air ≈ 0.01-0.02; clause-e fails).
    """

    template_name = "TRaiseStabilize"
    generation_source = "traise_stabilize_bet_call_multiway"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # 12.5E-B's t5_nfd_gutshot_raise_oop_bet_call (PILOT_539..550) used
        # bricks 5c/5d on broadway boards. T-RAISE-stabilize parametric uses
        # NEW brick ranks (6/7/8) on the same NFD-with-broadway-gutshot
        # template to expand the corpus signal without colliding with the
        # existing 12. The MW-47 spades canonical (AsQs on KsJd5s mixed-suit)
        # is the manual PILOT_694; here we use pure FD-suit bricks ≥ 6.
        configs = [
            # Spades variants with bigger bricks:
            ("AsQs", "KsJs8c", 6.0),  # NFD + gutshot (Q→T) + 8 brick (avoids t5_manual_canonical KsJs6c)
            ("AsKs", "QsJs7c", 7.0),  # OE+NFD (T+) + 7 brick
            ("AsTs", "KsQs7c", 6.0),  # NFD + gutshot (T→J) + 7 brick
            ("AsJs", "KsTs6c", 7.0),  # NFD + OE (Q+) + 6 brick
            # Diamonds variants with bigger bricks:
            ("AdQd", "KdJd6c", 6.0),
            ("AdKd", "QdJd7c", 7.0),
            ("AdTd", "KdQd7c", 6.0),
            # Clubs variants with bigger bricks (use heart brick to avoid 5c/5d):
            ("AcQc", "KcJc6h", 6.0),
            ("AcKc", "QcJc7h", 7.0),
            # Mid-board variants (lower second card, still NFD + clause-e):
            ("AsQs", "Ks9s4c", 6.0),  # K-9-4 spades
            ("AdKd", "Qd8d3c", 7.0),  # Q-8-3 diamonds
        ]
        out: List[GeneratedSituation] = []
        for i, (hero, flop, bet_size) in enumerate(configs[:target_count], start=1):
            sit_id = f"traise_stabilize_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=flop,
                street="flop",
                hero_position="BB",
                villain_positions=["HJ", "CO", "BTN"],
                pot=10.5 + bet_size + bet_size,
                to_call=bet_size,
                facing_bet=True,
                num_opponents=3,
                prior_actions=[
                    "preflop: HJ raise 2.5",
                    "preflop: CO call",
                    "preflop: BTN call",
                    "preflop: BB call",
                    "flop: BB check",
                    "flop: HJ check",
                    f"flop: CO bet {bet_size:g}",
                    "flop: BTN call",
                ],
                generation_source=self.generation_source,
                opener_position="HJ",
                bettor_position="CO",
                villain_aggression_count=1,
                villain_checked_back=0,
                villain_call_count=1,
                num_callers_to_bet=1,
                facing_raise=0,
                action_history=[
                    {"street": "flop", "actor": "BB", "action": "check"},
                    {"street": "flop", "actor": "HJ", "action": "check"},
                    {"street": "flop", "actor": "CO", "action": "bet", "size": bet_size},
                    {"street": "flop", "actor": "BTN", "action": "call"},
                ],
            )
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        return out


# ─── T-CONTROL — drift detection + design_action per hand ─────────────


class TControl(TemplateGenerator):
    """20 control hands across 5 buckets for G4 drift detection at
    12.5H-D. Per dispatch §"Methodology rules" item 3 + QC's TC-X T8
    schema gap fix: each row includes explicit `design_action` field
    so G4 can do exact same-action match against 494/110-hand corpus
    near-equivalents.

    Distribution per design §4: 6 CHECK + 5 BET + 4 FOLD + 3 CALL +
    2 RAISE = 20 hands. Patterns chosen to mirror common cohort-2
    generation_sources (monster_*, nfd_*, magg_*, donk_*, facing_*) so
    matched-pair drift detection is meaningful.
    """

    template_name = "TControl"
    generation_source = "tcontrol"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # 12.5E-B's t8_controls (PILOT_569..590) covered classic air-OOP
        # check patterns and TP/2P/set bet patterns; T-CONTROL parametric
        # uses NEW hero+board combinations to avoid collision while preserving
        # the bucket-distribution invariant for 12.5H-D drift detection.
        # All-check OOP air patterns → CHECK
        check_configs = [
            ("5c2h", "Ad9c4h", "BB", 2),
            ("6h3c", "Kd8s2h", "BB", 2),
            ("4d2c", "Qh9c5d", "BB", 2),
            ("7s3d", "As6h2s", "BB", 2),
            ("8c3s", "Kc9d4h", "BB", 2),
            ("9h2s", "Qd8c5h", "BB", 2),
        ]
        # OOP first-to-act value bets → BET
        bet_configs = [
            ("AhJs", "AcJd6h", "BB", 2),  # top two pair (A+J)
            ("KsTs", "KhTc5d", "BB", 2),  # top two pair (K+T)
            ("QhJh", "QcJd6s", "BB", 2),  # top two pair (Q+J)
            ("7c7d", "7h5s2c", "BB", 2),  # set of 7s first to act
            ("6h6s", "6c4d2h", "BB", 2),  # set of 6s first to act
        ]
        # Facing aggression with weak holdings → FOLD
        fold_configs = [
            ("7d4s", "AcKh9c", "BB", 1, 5.0),
            ("8h2c", "KdQc6s", "BB", 1, 6.0),
            ("Th5d", "KsJh8c", "BB", 1, 5.0),
            ("6c3h", "AdQs9d", "BB", 1, 7.0),
        ]
        # TP+ value catchers facing single bet → CALL
        call_configs = [
            ("AdJh", "AsKd8c", "BB", 1, 5.0),  # TP-J-kicker on A-high
            ("KhQs", "KsJd5c", "BB", 1, 5.0),  # TPGK on K-high
            ("AsTd", "Tc8d3s", "BB", 1, 5.0),  # TPTK on T-high
        ]
        # Flopped monsters facing aggression → RAISE
        raise_configs = [
            ("5s5d", "5h4c2s", "BB", 1, 6.0),  # set of 5s facing CB
            ("4c4h", "4s3c2d", "BB", 1, 7.0),  # set of 4s facing CB
        ]

        out: List[GeneratedSituation] = []
        i = 0
        for hero, flop, pos, num_opp in check_configs:
            i += 1
            sit_id = f"tcontrol_check_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=flop,
                street="flop",
                hero_position=pos,
                villain_positions=["CO", "BTN"][:num_opp],
                pot=10.5,
                to_call=0.0,
                facing_bet=False,
                num_opponents=num_opp,
                prior_actions=[
                    "preflop: CO raise 2.5",
                ] + (["preflop: BTN call"] if num_opp >= 2 else []) + [
                    "preflop: BB call",
                ],
                generation_source=self.generation_source,
                opener_position="CO",
                bettor_position=None,
                villain_aggression_count=0,
                villain_checked_back=0,
                villain_call_count=0,
                num_callers_to_bet=0,
                facing_raise=0,
                action_history=[],
            )
            row["design_action"] = "CHECK"
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        i = 0
        for hero, flop, pos, num_opp in bet_configs:
            i += 1
            sit_id = f"tcontrol_bet_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=flop,
                street="flop",
                hero_position=pos,
                villain_positions=["CO", "BTN"][:num_opp],
                pot=10.5,
                to_call=0.0,
                facing_bet=False,
                num_opponents=num_opp,
                prior_actions=[
                    "preflop: CO raise 2.5",
                ] + (["preflop: BTN call"] if num_opp >= 2 else []) + [
                    "preflop: BB call",
                ],
                generation_source=self.generation_source,
                opener_position="CO",
                bettor_position=None,
                villain_aggression_count=0,
                villain_checked_back=0,
                villain_call_count=0,
                num_callers_to_bet=0,
                facing_raise=0,
                action_history=[],
            )
            row["design_action"] = "BET"
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        i = 0
        for hero, flop, pos, num_opp, bet_size in fold_configs:
            i += 1
            sit_id = f"tcontrol_fold_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=flop,
                street="flop",
                hero_position=pos,
                villain_positions=["CO"],
                pot=8.0 + bet_size,
                to_call=bet_size,
                facing_bet=True,
                num_opponents=num_opp,
                prior_actions=[
                    "preflop: CO raise 2.5",
                    "preflop: BB call",
                    "flop: BB check",
                    f"flop: CO bet {bet_size:g}",
                ],
                generation_source=self.generation_source,
                opener_position="CO",
                bettor_position="CO",
                villain_aggression_count=1,
                villain_checked_back=0,
                villain_call_count=0,
                num_callers_to_bet=0,
                facing_raise=0,
                action_history=[
                    {"street": "flop", "actor": "BB", "action": "check"},
                    {"street": "flop", "actor": "CO", "action": "bet", "size": bet_size},
                ],
            )
            row["design_action"] = "FOLD"
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        i = 0
        for hero, flop, pos, num_opp, bet_size in call_configs:
            i += 1
            sit_id = f"tcontrol_call_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=flop,
                street="flop",
                hero_position=pos,
                villain_positions=["CO"],
                pot=8.0 + bet_size,
                to_call=bet_size,
                facing_bet=True,
                num_opponents=num_opp,
                prior_actions=[
                    "preflop: CO raise 2.5",
                    "preflop: BB call",
                    "flop: BB check",
                    f"flop: CO bet {bet_size:g}",
                ],
                generation_source=self.generation_source,
                opener_position="CO",
                bettor_position="CO",
                villain_aggression_count=1,
                villain_checked_back=0,
                villain_call_count=0,
                num_callers_to_bet=0,
                facing_raise=0,
                action_history=[
                    {"street": "flop", "actor": "BB", "action": "check"},
                    {"street": "flop", "actor": "CO", "action": "bet", "size": bet_size},
                ],
            )
            row["design_action"] = "CALL"
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        i = 0
        for hero, flop, pos, num_opp, bet_size in raise_configs:
            i += 1
            sit_id = f"tcontrol_raise_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=flop,
                street="flop",
                hero_position=pos,
                villain_positions=["CO"],
                pot=8.0 + bet_size,
                to_call=bet_size,
                facing_bet=True,
                num_opponents=num_opp,
                prior_actions=[
                    "preflop: CO raise 2.5",
                    "preflop: BB call",
                    "flop: BB check",
                    f"flop: CO bet {bet_size:g}",
                ],
                generation_source=self.generation_source,
                opener_position="CO",
                bettor_position="CO",
                villain_aggression_count=1,
                villain_checked_back=0,
                villain_call_count=0,
                num_callers_to_bet=0,
                facing_raise=0,
                action_history=[
                    {"street": "flop", "actor": "BB", "action": "check"},
                    {"street": "flop", "actor": "CO", "action": "bet", "size": bet_size},
                ],
            )
            row["design_action"] = "RAISE"
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        return out[:target_count]


# ─── 6 manual canonicals (Track B per design §5.1) ────────────────────


PILOT_ID_START_MANUAL = 689  # 689..694 = 6 manual canonicals


_MANUALS: List[Dict[str, Any]] = [
    # T8' MW-25 family canonical (1 of 2) — monotone-board adaptation
    {
        "template": "T8prime",
        "situation_id": "t8prime_manual_canonical_01",
        "author_design_note": (
            "MW-25 family adaptation to T8' monotone variant. MW-25 itself is "
            "Ks/7s on As9s5d two-tone — hero has K-high FD + 2 board spades. This "
            "canonical adapts to the T8' monotone template (As9s5s) by giving hero "
            "Ks7h: 1 spade hole card + 3 board spades = K-high FD (NOT made flush; "
            "would be Ks7s on monotone). Same drawing-bucket BET 50% pot reasoning "
            "for fold equity + equity denial + protection 4-way checked-through. "
            "Kicker suit changed from spade to heart to preserve FD axis on monotone."
        ),
        "kwargs": dict(
            hero_cards="Ks7h", board="As9s5s", street="flop", hero_position="BTN",
            villain_positions=["HJ", "CO", "BB"], pot=10.5, to_call=0.0,
            facing_bet=False, num_opponents=3,
            prior_actions=["preflop: HJ raise 2.5", "preflop: CO call",
                           "preflop: BTN call", "preflop: BB call",
                           "flop: BB check", "flop: HJ check", "flop: CO check"],
            generation_source="t8prime_manual_canonical", opener_position="HJ",
            bettor_position=None, villain_aggression_count=0,
            villain_checked_back=1, villain_call_count=0,
            num_callers_to_bet=0, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "HJ", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "check"},
            ],
        ),
    },
    # T8' second manual (NFD variant for diversity)
    {
        "template": "T8prime",
        "situation_id": "t8prime_manual_canonical_02",
        "author_design_note": (
            "MW-25-adjacent NFD variant: hero AsKh on Js9s3s monotone. NFD + 2 over. "
            "Same family as MW-25 but with NFD instead of K-high FD. Provides the "
            "labelling round with a contrast pair (K-high FD canonical vs NFD canonical) "
            "for booster generalization. Board chosen as Js9s3s (not Js9s4s) to avoid "
            "collision with 12.5E-B t1_manual_canonical PILOT_591 which used Js9s4s."
        ),
        "kwargs": dict(
            hero_cards="AsKh", board="Js9s3s", street="flop", hero_position="BTN",
            villain_positions=["HJ", "CO", "BB"], pot=10.5, to_call=0.0,
            facing_bet=False, num_opponents=3,
            prior_actions=["preflop: HJ raise 2.5", "preflop: CO call",
                           "preflop: BTN call", "preflop: BB call",
                           "flop: BB check", "flop: HJ check", "flop: CO check"],
            generation_source="t8prime_manual_canonical", opener_position="HJ",
            bettor_position=None, villain_aggression_count=0,
            villain_checked_back=1, villain_call_count=0,
            num_callers_to_bet=0, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "HJ", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "check"},
            ],
        ),
    },
    # T9' MW-40 exact replica
    {
        "template": "T9prime",
        "situation_id": "t9prime_manual_canonical_01",
        "author_design_note": (
            "MW-40 exact-replica: hero AhTs on Ac Jc 5d (rainbow A-J-5; AJ5r), BTN after "
            "HJ PFR check + CO check + BB check 4-way. PFR check-back on Ax in 4-way "
            "condenses HJ's range to weak Jx, broadways without A, air. AT TP-T-kicker is "
            "thin value + protection + equity denial. Strong-made-bucket BET. The literal "
            "MW-40 pattern."
        ),
        "kwargs": dict(
            hero_cards="AhTs", board="AcJc5d", street="flop", hero_position="BTN",
            villain_positions=["HJ", "CO", "BB"], pot=11.0, to_call=0.0,
            facing_bet=False, num_opponents=3,
            prior_actions=["preflop: HJ raise 2.5", "preflop: CO call",
                           "preflop: BTN call", "preflop: BB call",
                           "flop: BB check", "flop: HJ check", "flop: CO check"],
            generation_source="t9prime_manual_canonical", opener_position="HJ",
            bettor_position=None, villain_aggression_count=0,
            villain_checked_back=1, villain_call_count=0,
            num_callers_to_bet=0, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "HJ", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "check"},
            ],
        ),
    },
    # T10' MW-45 exact replica
    {
        "template": "T10prime",
        "situation_id": "t10prime_manual_canonical_01",
        "author_design_note": (
            "MW-45 exact-replica: hero 6d6c on AcKd6h-Q turn 4-way slowplay then face "
            "CO turn lead. Hero set on rainbow A-K-6 flop (slowplay opportunity); turn "
            "Q connects broadway. CO's lead represents AK-strong, AQ, KQ, QQ. RAISE for "
            "value + protection vs draws. The literal MW-45 pattern."
        ),
        "kwargs": dict(
            hero_cards="6d6c", board="AcKd6hQs", street="turn", hero_position="BB",
            villain_positions=["CO", "BTN", "SB"], pot=35.0, to_call=12.0,
            facing_bet=True, num_opponents=3,
            prior_actions=["preflop: CO raise 2.5", "preflop: BTN call",
                           "preflop: SB call", "preflop: BB call",
                           "flop: SB check", "flop: BB check",
                           "flop: CO check", "flop: BTN check",
                           "turn: SB check", "turn: BB check",
                           "turn: CO bet 12", "turn: BTN call", "turn: SB fold"],
            generation_source="t10prime_manual_canonical", opener_position="CO",
            bettor_position="CO", villain_aggression_count=1,
            villain_checked_back=0, villain_call_count=1,
            num_callers_to_bet=1, facing_raise=0,
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
    # T7-ext MW-17 exact-replica
    {
        "template": "T7ext",
        "situation_id": "t7ext_manual_canonical_01",
        "author_design_note": (
            "MW-17 exact-replica: hero AdKs on Jd8d4c facing CO single bet 3-way (PFR "
            "opens, BTN calls, BB calls; flop CO bets, BTN folds, hero faces single bet). "
            "Hero AdKs = NFD (diamond) + K overcard with nut blocker. Composition (NFD + "
            "overcards) + nut blocker against CO range + implied odds make CALL profitable. "
            "Pure drawing-bucket reasoning anchor; NOT threshold-based per "
            "feedback_bucket_first_labelling.md."
        ),
        "kwargs": dict(
            hero_cards="AdKs", board="Jd8d4c", street="flop", hero_position="BB",
            villain_positions=["CO", "BTN"], pot=13.0, to_call=5.0,
            facing_bet=True, num_opponents=2,
            prior_actions=["preflop: CO raise 2.5", "preflop: BTN call",
                           "preflop: BB call", "flop: BB check",
                           "flop: CO bet 5", "flop: BTN fold"],
            generation_source="t7ext_manual_canonical", opener_position="CO",
            bettor_position="CO", villain_aggression_count=1,
            villain_checked_back=0, villain_call_count=0,
            num_callers_to_bet=0, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "bet", "size": 5.0},
                {"street": "flop", "actor": "BTN", "action": "fold"},
            ],
        ),
    },
    # T-RAISE-stabilize MW-47 exact-replica (canonical NFD-blocker bet+call OOP)
    {
        "template": "TRaiseStabilize",
        "situation_id": "traise_stabilize_manual_canonical_01",
        "author_design_note": (
            "MW-47 exact-replica analog: hero AsQs on KsJd5s 4-way bet+call OOP (PFR "
            "opens, CO bets, BTN calls, hero faces bet+call in BB). Hero NFD + gutshot "
            "(combo draw) + As nut blocker. v3.4 Fix 2.1.1 clauses (a-e) all satisfied "
            "(villain_air_pct expected ≥0.05 on this spades-board-with-Jd-Bricks "
            "structure; NOT the heart-suit broadway-saturated pattern that produced "
            "near-zero air in 12.5E-C). Drawing-bucket RAISE for combined value/semi-bluff."
        ),
        "kwargs": dict(
            hero_cards="AsQs", board="KsJd5s", street="flop", hero_position="BB",
            villain_positions=["HJ", "CO", "BTN"], pot=22.5, to_call=6.0,
            facing_bet=True, num_opponents=3,
            prior_actions=["preflop: HJ raise 2.5", "preflop: CO call",
                           "preflop: BTN call", "preflop: BB call",
                           "flop: BB check", "flop: HJ check",
                           "flop: CO bet 6", "flop: BTN call"],
            generation_source="traise_stabilize_manual_canonical",
            opener_position="HJ", bettor_position="CO",
            villain_aggression_count=1, villain_checked_back=0,
            villain_call_count=1, num_callers_to_bet=1, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "HJ", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "bet", "size": 6.0},
                {"street": "flop", "actor": "BTN", "action": "call"},
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
    ("T8prime", T8PrimeMonotoneFDCheckedThrough(), 16),
    ("T9prime", T9PrimeTPMediumKickerAfterPFRCheck(), 13),
    ("T10prime", T10PrimeSlowplaySetTurnLead(), 13),
    ("T7ext", T7ExtNFDOvercardsCall(), 11),
    ("TRaiseStabilize", TRaiseStabilize(), 11),
    ("TControl", TControl(), 20),
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


def g1_join_cardinality(
    new_rows: List[Dict[str, Any]],
    existing_corpus_path: str,
):
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
    targets = {
        "T8PRIME": 18, "T9PRIME": 14, "T10PRIME": 14,
        "T7EXT": 12, "TRAISE": 12, "TCONTROL": 20,
    }

    def _tkey(sid: str) -> str:
        # Map situation_id prefix to template key
        if sid.startswith("t8prime"):
            return "T8PRIME"
        if sid.startswith("t9prime"):
            return "T9PRIME"
        if sid.startswith("t10prime"):
            return "T10PRIME"
        if sid.startswith("t7ext"):
            return "T7EXT"
        if sid.startswith("traise_stabilize"):
            return "TRAISE"
        if sid.startswith("tcontrol"):
            return "TCONTROL"
        return "?"

    found = {k: 0 for k in targets}
    for r in new_rows:
        k = _tkey(r["situation_id"])
        if k in found:
            found[k] += 1
    deviations = []
    for tname, want in targets.items():
        got = found[tname]
        if abs(got - want) > 1:
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
        return False, f"G3 FAIL: {len(matches)} dup vs existing 604: {matches[:5]}"
    return True, f"G3 PASS: 0 (board, hero, position, prior_actions) duplicates vs existing 604; 0 internal duplicates"


# ─── CLI ──────────────────────────────────────────────────────────────


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Phase 12.5H-B situation generator (90 hands across 6 templates)"
    )
    p.add_argument(
        "--output",
        default="data/corpus_revision_125h_situations_2026-05-06.jsonl",
        help="Output JSONL path for the 84 parametric situations",
    )
    p.add_argument(
        "--manual-output",
        default="data/corpus_revision_125h_manual_canonicals_2026-05-06.jsonl",
        help="Output JSONL path for the 6 manual canonical hands",
    )
    p.add_argument(
        "--existing-corpus",
        default="data/corpus_combined_604_2026-05-05.jsonl",
        help="Existing 604-hand corpus path (G1 + G3 reference)",
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
