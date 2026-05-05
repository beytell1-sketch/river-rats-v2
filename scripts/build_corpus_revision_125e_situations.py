#!/usr/bin/env python3
"""Phase 12.5E-B situation generator — 110 new hands across 8 templates.

Implements ml-architect 12.5E-A design comm
(`review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md`, master `bad1396`)
per Phase 12.5E-B dispatch (`review/comms/MAIN_TERMINAL_PHASE125E_DISPATCH_2026-05-04.md`,
master `bad1396`).

Two-track sourcing per design §5.1:
- Track A (this file): parametric situation factory for templates T1-T8
- Track B (separate file): 14 manual canonical hand designs for GTO-EXPERT review

Templates per design §3:
- T1 (12 BET):  monotone-flop FD-with-overcard checked-through 4-way (MW-25 family)
- T2 (10 BET):  TP medium kicker IP 4-way after PFR check (MW-40 family)
- T3 (10 BET):  river thin-value TPTK after villain check-call-check (MW-42 family)
- T4 (12 RAISE): slowplay set into turn lead 4-way (MW-45 family)
- T5 (12 RAISE): NFD+gutshot semi-bluff RAISE OOP into bet+call multiway (MW-47 family) — H-FEAT primary test
- T6 (8 RAISE):  monster delayed-aggression patterns (MW-33-adjacent)
- T7 (10 CALL):  NFD+overcards CALL under pot odds (MW-17 family)
- T8 (36 mixed): control hands across 5 buckets (drift detection at 12.5E-D G4)

Output schema mirrors data/corpus_revision_500_hand_2026-04-27.jsonl cohort 2:
  situation_id, pilot_hand_id, hero_cards, board, street, hero_position,
  villain_positions, pot, to_call, facing_bet, num_opponents, prior_actions,
  generation_source, opener_position, feat_dict (59-key)

pilot_hand_id sequence: PILOT_495..PILOT_604 (continues 12.5D corpus 1..494).

Usage:
    python3 scripts/build_corpus_revision_125e_situations.py \\
        --output data/corpus_revision_125e_situations_2026-05-04.jsonl

Self-checks (G1-G3 per design §7) print to stderr after generation.
Run with --strict to exit non-zero on any G1-G3 failure.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Tuple

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CORE = os.path.join(_REPO, "river-rats-core")
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from feature_extractor import extract_all_features, FEATURE_COLUMNS  # noqa: E402
from feature_keys import F  # noqa: E402

# pilot_hand_id sequence — continues the 12.5D corpus's PILOT_001..PILOT_494.
# Parametric file occupies PILOT_495..PILOT_590 (96 hands).
# Manual file occupies PILOT_591..PILOT_604 (14 hands), authored separately
# in `scripts/build_corpus_revision_125e_manual_canonicals.py`.
PILOT_ID_START = 495
PILOT_PARAMETRIC_END = 590  # inclusive ⇒ 96 parametric hands
PILOT_ID_END = 604  # inclusive ⇒ 110 hands incl 14 manuals

# Street code mapping used inside extract_all_features's hand_dict.
_STREET_CODE = {"flop": "f", "turn": "t", "river": "r"}


# ─── Schema-canonical row builder ─────────────────────────────────────


def build_hand_dict(
    *,
    hero_cards: str,
    board: str,
    street: str,
    hero_position: str,
    villain_position: str,
    pot: float,
    to_call: float,
    facing_bet: bool,
    num_opponents: int,
    opener_position: Optional[str],
    bettor_position: Optional[str],
    villain_aggression_count: int,
    villain_checked_back: int,
    villain_call_count: int,
    num_callers_to_bet: int,
    facing_raise: int,
    action_history: List,
) -> Dict[str, Any]:
    """Construct the hand_dict that extract_all_features() consumes.

    Mirrors the hand_dict shape used in
    `reference_evaluator._evaluate_one_hand` and
    `train_model_v9_student._evaluate_student_one_hand` — same schema for
    both training corpus generation and runtime inference.
    """
    return {
        "h": hero_cards,
        "b": board,
        "pos": hero_position,
        "vp": villain_position,
        "pot": pot,
        "tc": to_call,
        "st": _STREET_CODE[street],
        "fb": int(facing_bet),
        "exp": "C",
        F.META_NUM_OPPONENTS: num_opponents,
        F.META_NUM_RAISES: 0,
        F.META_OPENER_POSITION: opener_position,
        F.META_BETTOR_POSITION: bettor_position,
        "_villain_aggression_count": villain_aggression_count,
        "_villain_checked_back": villain_checked_back,
        "_villain_call_count": villain_call_count,
        "_num_callers_to_bet": num_callers_to_bet,
        "_facing_raise": facing_raise,
        "_action_history": action_history,
    }


def _hero_only_prior_actions(
    prior_actions: List[str], hero_position: str,
) -> List[str]:
    """Filter prior_actions to hero-only entries.

    Existing 494-row corpus convention (verified empirically by gto-expert
    in 12.5E-B review and re-confirmed at amendment time): each entry's
    actor must equal hero_position. Format: 'street: ACTOR action [size]'.
    Non-hero actions are dropped from the output row's prior_actions.
    The full multi-actor sequence still flows through `action_history`
    (which extract_all_features consumes for chain narrowing).
    """
    out: List[str] = []
    for entry in prior_actions:
        # Format: 'street: ACTOR action ...'
        parts = entry.split(":", 1)
        if len(parts) != 2:
            out.append(entry)
            continue
        rest = parts[1].strip().split()
        if not rest:
            out.append(entry)
            continue
        actor = rest[0]
        if actor == hero_position:
            out.append(entry)
    return out


def emit_row(
    *,
    situation_id: str,
    pilot_hand_id: str,
    hero_cards: str,
    board: str,
    street: str,
    hero_position: str,
    villain_positions: List[str],
    pot: float,
    to_call: float,
    facing_bet: bool,
    num_opponents: int,
    prior_actions: List[str],
    generation_source: str,
    opener_position: Optional[str],
    bettor_position: Optional[str],
    villain_aggression_count: int,
    villain_checked_back: int,
    villain_call_count: int,
    num_callers_to_bet: int,
    facing_raise: int,
    action_history: List,
) -> Dict[str, Any]:
    """Emit one canonical corpus row with feat_dict via extract_all_features.

    Output shape matches data/corpus_revision_500_hand_2026-04-27.jsonl
    cohort 2 (rows 100-493). prior_actions is filtered to hero-only per
    the existing-494 convention; action_history (consumed by
    extract_all_features) preserves the full multi-actor sequence.
    """
    prior_actions = _hero_only_prior_actions(prior_actions, hero_position)
    primary_villain = villain_positions[0] if villain_positions else "BB"
    hd = build_hand_dict(
        hero_cards=hero_cards,
        board=board,
        street=street,
        hero_position=hero_position,
        villain_position=primary_villain,
        pot=pot,
        to_call=to_call,
        facing_bet=facing_bet,
        num_opponents=num_opponents,
        opener_position=opener_position,
        bettor_position=bettor_position,
        villain_aggression_count=villain_aggression_count,
        villain_checked_back=villain_checked_back,
        villain_call_count=villain_call_count,
        num_callers_to_bet=num_callers_to_bet,
        facing_raise=facing_raise,
        action_history=action_history,
    )
    feat_dict = extract_all_features(hd)
    # Trim to the 59 keys gate-relevant for the trainer (extract_all_features
    # also computes intermediate / debug keys; the trainer only consumes
    # feature_extractor.FEATURE_COLUMNS).
    feat_dict = {k: feat_dict[k] for k in FEATURE_COLUMNS if k in feat_dict}
    return {
        "situation_id": situation_id,
        "hero_cards": hero_cards,
        "board": board,
        "street": street,
        "hero_position": hero_position,
        "villain_positions": villain_positions,
        "pot": pot,
        "to_call": to_call,
        "facing_bet": facing_bet,
        "num_opponents": num_opponents,
        "prior_actions": prior_actions,
        "feat_dict": feat_dict,
        "generation_source": generation_source,
        "opener_position": opener_position,
        "pilot_hand_id": pilot_hand_id,
    }


# ─── Card helpers ─────────────────────────────────────────────────────

_RANKS = "23456789TJQKA"
_SUITS = "shdc"


def _card(rank: str, suit: str) -> str:
    return rank + suit


def _board_str(cards: List[str]) -> str:
    return "".join(cards)


def _hero_str(cards: List[str]) -> str:
    return "".join(cards)


def _board_cards(board: str) -> List[str]:
    return [board[i : i + 2] for i in range(0, len(board), 2)]


def _hero_cards(hero: str) -> List[str]:
    return [hero[i : i + 2] for i in range(0, len(hero), 2)]


def _all_cards_unique(*cardlists: List[str]) -> bool:
    """Check no card appears twice across any of the given card lists."""
    seen = set()
    for cl in cardlists:
        for c in cl:
            if c in seen:
                return False
            seen.add(c)
    return True


# ─── Per-template generator base class ────────────────────────────────


@dataclass
class GeneratedSituation:
    """Container yielded by each template's generator."""
    situation_id: str
    row: Dict[str, Any]


class TemplateGenerator:
    """Base class for the 8 template generators.

    Subclasses override `generate(target_count)` to yield exactly
    `target_count` GeneratedSituation objects. Each call must be
    deterministic (same parameter sweep each time) so runs are
    reproducible.
    """

    template_name: str = ""
    generation_source: str = ""

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        raise NotImplementedError


# ─── T1 — monotone-flop FD-with-overcard checked-through 4-way (12 BET) ──


class T1MonotoneFDCheckedThrough(TemplateGenerator):
    """MW-25 family. Discriminative axis: is_monotone=1, has_flush_draw=1,
    num_opponents>=3, villain_aggression_count=0, is_paired=0.

    Parametric sweep: 4 board high cards × 3 hero overcard variants ×
    suits = 12 distinct hands. Hero holds two same-suit cards on board's
    suit, with one or two overcards relative to the board.
    """

    template_name = "T1"
    generation_source = "t1_monotone_fd_checked_through_4way"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # Parametric: (board_top, board_mid, board_low) × hero_overcard
        # Boards are monotone (all spades). Hero has 2 spades for FD.
        # Use 4 distinct flop boards × 3 hero hands per board = 12 total.
        # Monotone board (3 spades) + hero with EXACTLY 1 spade + 1 non-spade
        # overcard ⇒ 4 total spades (FD) + 1-2 overcards relative to board.
        # If hero held 2 spades the result would be a flopped flush, not a FD.
        configs = [
            # (board_high, board_mid, board_low, hero_cards) — hero has 1 spade
            ("Js", "8s", "5s", ["As", "Kh"]),  # NFD + 1 overcard (K)
            ("Js", "8s", "5s", ["Qs", "Kc"]),  # 2nd-nut FD + 1 overcard
            ("Js", "8s", "5s", ["Ks", "Qh"]),  # K FD + 1 overcard
            ("Ts", "7s", "4s", ["As", "Jh"]),  # NFD + 2 overcards (A+J)
            ("Ts", "7s", "4s", ["Ks", "Qd"]),  # KQ FD + overcards
            ("Ts", "7s", "4s", ["As", "Kc"]),  # NFD + 2 overcards
            ("9s", "6s", "3s", ["As", "Kh"]),  # NFD over the world
            ("9s", "6s", "3s", ["Ks", "Qh"]),  # KQ FD over flop
            ("9s", "6s", "3s", ["As", "Td"]),  # NFD + 1 overcard
            ("Qs", "8s", "4s", ["As", "Kh"]),  # NFD + 1 overcard
            ("Qs", "8s", "4s", ["As", "Jc"]),  # NFD + 1 overcard
            ("Qs", "8s", "4s", ["Ks", "Jh"]),  # 2nd-nut FD + 1 overcard
        ]
        out: List[GeneratedSituation] = []
        for i, (bh, bm, bl, hero) in enumerate(configs[:target_count], start=1):
            board = bh + bm + bl
            hero_str = "".join(hero)
            # 4-way pot: HJ opens 2.5BB, CO calls, BTN calls, hero BB calls
            # Flop checked through to hero.
            sit_id = f"t1_monotone_fd_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",  # filled by caller
                hero_cards=hero_str,
                board=board,
                street="flop",
                hero_position="BTN",
                villain_positions=["HJ", "CO", "BB"],
                pot=10.5,  # 4-way preflop limped-style
                to_call=0.0,
                facing_bet=False,
                num_opponents=3,
                prior_actions=[
                    "preflop: HJ raise 2.5",
                    "preflop: CO call",
                    "preflop: BTN call",
                    "preflop: BB call",
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
                    {"street": "flop", "actor": "HJ", "action": "check"},
                    {"street": "flop", "actor": "CO", "action": "check"},
                ],
            )
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        return out


# ─── T2 — TP medium-kicker IP 4-way after PFR check (10 BET) ──────────


class T2TPMediumKickerAfterPFRCheck(TemplateGenerator):
    """MW-40 family. Discriminative axis: is_strong_made=1, is_rainbow=1,
    villain_checked_back=1, num_opponents>=2.

    Hero on BTN has TP medium kicker on rainbow A-high or K-high; HJ
    PFR has checked back; CO + BB also checked.
    """

    template_name = "T2"
    generation_source = "t2_tp_medium_kicker_pfr_check_4way"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # 5 rainbow boards (A-high or K-high) × 2 hero kickers = 10
        configs = [
            # (board, hero_cards) — A-high boards
            ("As7d3c", "AhTs"),
            ("As7d3c", "AhJs"),
            ("Ad8c4s", "AhTs"),
            ("Ad8c4s", "AhJs"),
            # K-high boards
            ("Ks6d2c", "KhTs"),
            ("Ks6d2c", "KhJs"),
            ("Kc9s3d", "KhTd"),
            ("Kc9s3d", "KhJd"),
            # Two more A-high variants
            ("Ah6c2s", "AdTd"),
            ("Ah6c2s", "AdJh"),
        ]
        out: List[GeneratedSituation] = []
        for i, (board, hero) in enumerate(configs[:target_count], start=1):
            sit_id = f"t2_tp_med_kicker_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=board,
                street="flop",
                hero_position="BTN",
                villain_positions=["HJ", "CO", "BB"],
                pot=11.0,  # PFR raise + 3 callers
                to_call=0.0,
                facing_bet=False,
                num_opponents=3,
                prior_actions=[
                    "preflop: HJ raise 2.5",
                    "preflop: CO call",
                    "preflop: BTN call",
                    "preflop: BB call",
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
                    {"street": "flop", "actor": "HJ", "action": "check"},
                    {"street": "flop", "actor": "CO", "action": "check"},
                ],
            )
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        return out


# ─── T3 — river thin-value TPTK after villain check-call-check (10 BET) ──


class T3RiverThinValueTPTK(TemplateGenerator):
    """MW-42 family. Discriminative axis: street=river, hand_category
    strong_made/TPTK, villain check-called turn (call_count moderate),
    river check.

    E-FEATURE risk per design §3 T3 — full discrimination requires
    multi-street action narrowing. The factory populates the action
    counters; whether the booster can find a stable split is empirical.
    """

    template_name = "T3"
    generation_source = "t3_river_thin_value_tptk"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # 5 board run-outs (rainbow A or K-high; turn brick; river brick)
        # × 2 villain positions = 10
        configs = [
            # (board, hero_cards, villain_pos)
            ("As7d2cThKh", "AhKs", "CO"),  # AK on AT-board
            ("As7d2cThKh", "AcQs", "HJ"),  # AQ on AT-board, board pair K
            ("Ks8c4d2sQh", "KhQs", "CO"),  # KQ on KQx board
            ("Ks8c4d2sQh", "KdJs", "BTN"), # KJ TP-good kicker
            ("Ad6s3cTd5h", "AcKs", "CO"),  # AK on AT-rag river
            ("Ad6s3cTd5h", "AhJd", "HJ"),  # AJ TPGK
            ("Kc7d5s2h9c", "KsQc", "CO"),  # KQ on K-low board
            ("Kc7d5s2h9c", "KhJs", "BTN"), # KJ
            ("As9c5d4h2s", "AhKd", "CO"),  # AK rags
            ("As9c5d4h2s", "AcQh", "HJ"),  # AQ rags
        ]
        out: List[GeneratedSituation] = []
        for i, (board, hero, vp) in enumerate(configs[:target_count], start=1):
            sit_id = f"t3_river_tptk_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=board,
                street="river",
                hero_position="BTN",
                villain_positions=[vp],
                pot=42.0,  # bet+call flop, check+check turn
                to_call=0.0,
                facing_bet=False,
                num_opponents=1,
                prior_actions=[
                    f"preflop: {vp} raise 2.5",
                    "preflop: BTN call",
                    f"flop: {vp} bet 6",
                    "flop: BTN call",
                    f"turn: {vp} check",
                    "turn: BTN check",
                    f"river: {vp} check",
                ],
                generation_source=self.generation_source,
                opener_position=vp,
                bettor_position=vp,  # last bettor in trace
                villain_aggression_count=1,  # bet flop
                villain_checked_back=0,
                villain_call_count=1,  # called BTN flop bet implicitly via flop bet+call dynamic
                num_callers_to_bet=0,
                facing_raise=0,
                action_history=[
                    {"street": "flop", "actor": vp, "action": "bet", "size": 6},
                    {"street": "flop", "actor": "BTN", "action": "call"},
                    {"street": "turn", "actor": vp, "action": "check"},
                    {"street": "turn", "actor": "BTN", "action": "check"},
                    {"street": "river", "actor": vp, "action": "check"},
                ],
            )
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        return out


# ─── T4 — slowplayed set into turn lead 4-way (12 RAISE) ──────────────


class T4SlowplaySetTurnLead(TemplateGenerator):
    """MW-45 family. Discriminative axis: hand_category=set, street=turn,
    villain just bet, num_opponents>=2.

    Hero in BB calls preflop with pocket pair, flops set; flop checks
    through 4-way; turn villain leads.
    """

    template_name = "T4"
    generation_source = "t4_slowplay_set_turn_lead_4way"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # 12 distinct (hero pocket pair, flop containing set, turn card, leader)
        configs = [
            # (hero, flop, turn, leader_pos, lead_size)
            ("9s9c", "9d6h2c", "Jd", "CO", 12.0),
            ("8d8h", "8s5c2d", "Td", "HJ", 14.0),
            ("7c7s", "7h4d2c", "Qs", "CO", 16.0),
            ("6h6s", "6c3d2h", "Js", "BTN", 12.0),
            ("5d5c", "5h4c2s", "Tc", "CO", 14.0),
            ("9h9d", "9s5c4h", "Qd", "HJ", 16.0),
            ("8s8c", "8d6c3s", "Js", "CO", 14.0),
            ("4h4s", "4d3c2h", "Ts", "BTN", 12.0),
            ("3c3d", "3s5h2d", "Js", "CO", 14.0),
            ("9c9s", "9h7c2s", "Qd", "BTN", 16.0),
            ("7d7h", "7s6d2c", "Js", "HJ", 14.0),
            ("6c6d", "6s4h2c", "Tc", "CO", 12.0),
        ]
        out: List[GeneratedSituation] = []
        for i, (hero, flop, turn, leader, size) in enumerate(configs[:target_count], start=1):
            board = flop + turn
            sit_id = f"t4_slowplay_set_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=board,
                street="turn",
                hero_position="BB",
                villain_positions=[leader, "CO" if leader != "CO" else "HJ", "BTN"],
                pot=10.5 + size,  # flop check-through pot + turn lead size
                to_call=size,
                facing_bet=True,
                num_opponents=3,
                prior_actions=[
                    f"preflop: {leader} raise 2.5",
                    "preflop: CO call" if leader != "CO" else "preflop: HJ call",
                    "preflop: BTN call",
                    "preflop: BB call",
                    f"flop: {leader} check",
                    "flop: CO check" if leader != "CO" else "flop: HJ check",
                    "flop: BTN check",
                    "flop: BB check",
                    f"turn: {leader} bet {size:g}",
                ],
                generation_source=self.generation_source,
                opener_position=leader,
                bettor_position=leader,
                villain_aggression_count=1,  # leader just bet turn
                villain_checked_back=0,  # they bet, not checked
                villain_call_count=0,
                num_callers_to_bet=0,
                facing_raise=0,
                action_history=[
                    {"street": "flop", "actor": leader, "action": "check"},
                    {"street": "flop", "actor": "CO" if leader != "CO" else "HJ", "action": "check"},
                    {"street": "flop", "actor": "BTN", "action": "check"},
                    {"street": "flop", "actor": "BB", "action": "check"},
                    {"street": "turn", "actor": leader, "action": "bet", "size": size},
                ],
            )
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        return out


# ─── T5 — NFD+gutshot semi-bluff RAISE OOP into bet+call multiway (12 RAISE) ──


class T5NFDGutshotRaiseOOP(TemplateGenerator):
    """MW-47 family. PRIMARY H-FEAT TEST.

    Discriminative axis: nut_flush_block=1, has_flush_draw=1,
    draw_outs>=9, villain just bet, num_callers_to_bet>=1, is_ip=0.

    Hero in BB or SB has Ax+Tx-Jx-Qs of one suit forming nut-flush
    blocker + gutshot. PFR opens, BTN calls, CO bets flop, hero faces
    bet+call OOP.
    """

    template_name = "T5"
    generation_source = "t5_nfd_gutshot_raise_oop_bet_call"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # Two-tone board (2 same suit) + hero with 2 same suit (one being As) ⇒
        # 4 total of that suit = flush draw with nut blocker. Plus the broadway
        # texture gives a gutshot to the missing rank.
        # Verify: (board has 2 spades) + (hero has 2 spades incl As) = 4 spades.
        configs = [
            # (hero, flop, bet_size) — board = 2 spades + 1 off-suit
            ("AsQs", "KsJs5c", 6.0),  # 2 board + 2 hero spades (As+Qs); gutshot to T
            ("AsTs", "KsQs5c", 6.0),  # 2 board + 2 hero spades; gutshot to J
            ("AsKs", "QsJs5c", 7.0),  # As+Ks hero; OE flush + gutshot
            ("AhQh", "KhJh5c", 6.0),  # hearts variant
            ("AhTh", "KhQh5c", 6.0),
            ("AhKh", "QhJh5c", 7.0),
            ("AdQd", "KdJd5c", 6.0),  # diamonds variant
            ("AdTd", "KdQd5c", 6.0),
            ("AdKd", "QdJd5c", 7.0),
            ("AcQc", "KcJc5d", 6.0),  # clubs variant
            ("AcTc", "KcQc5d", 6.0),
            ("AcKc", "QcJc5d", 7.0),
        ]
        out: List[GeneratedSituation] = []
        for i, (hero, flop, bet_size) in enumerate(configs[:target_count], start=1):
            sit_id = f"t5_nfd_gutshot_raise_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=flop,
                street="flop",
                hero_position="BB",
                villain_positions=["HJ", "CO", "BTN"],
                pot=10.5 + bet_size + bet_size,  # PFR + 2 calls preflop, then bet+call flop
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
                villain_aggression_count=1,  # CO just bet
                villain_checked_back=0,
                villain_call_count=1,  # BTN just called
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


# ─── T6 — monster delayed-aggression patterns (8 RAISE) ───────────────


class T6MonsterDelayedAggression(TemplateGenerator):
    """MW-33-adjacent. Reinforcement template: hero set on rainbow
    paired-low or low-connector flop; turn delayed action sequence.

    Prevents corpus from overfitting to monster⇒RAISE-iff-first-to-act.
    """

    template_name = "T6"
    generation_source = "t6_monster_delayed_aggression"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        configs = [
            # (hero, flop, turn, sequence_type)
            ("8d8h", "8s5c2d", "Tc", "facing_turn_lead"),    # set faces turn lead
            ("7s7h", "7c4d2s", "Js", "facing_turn_raise"),   # set faces turn check-raise
            ("6c6d", "6s3h2c", "Td", "facing_turn_lead"),
            ("5h5c", "5s4d2h", "Js", "facing_turn_lead"),
            ("9d9c", "9s7h2d", "Tc", "facing_turn_raise"),
            ("4s4h", "4c3d2s", "Td", "facing_turn_lead"),
            ("3d3c", "3s2h5d", "Tc", "facing_turn_lead"),
            ("8c8s", "8d6h2c", "Qs", "facing_turn_raise"),
        ]
        out: List[GeneratedSituation] = []
        for i, (hero, flop, turn, seq) in enumerate(configs[:target_count], start=1):
            board = flop + turn
            sit_id = f"t6_monster_delayed_{i:02d}"
            if seq == "facing_turn_lead":
                # Flop checks through; turn villain leads
                priors = [
                    "preflop: CO raise 2.5",
                    "preflop: BTN call",
                    "preflop: BB call",
                    "flop: BB check",
                    "flop: CO check",
                    "flop: BTN check",
                    "turn: BB check",
                    "turn: CO bet 12",
                ]
                ah = [
                    {"street": "flop", "actor": "BB", "action": "check"},
                    {"street": "flop", "actor": "CO", "action": "check"},
                    {"street": "flop", "actor": "BTN", "action": "check"},
                    {"street": "turn", "actor": "BB", "action": "check"},
                    {"street": "turn", "actor": "CO", "action": "bet", "size": 12.0},
                ]
                vac = 1
                ncb = 0
                pot, tc = 10.5 + 12, 12.0
            else:  # facing_turn_raise
                priors = [
                    "preflop: CO raise 2.5",
                    "preflop: BTN call",
                    "preflop: BB call",
                    "flop: BB check",
                    "flop: CO bet 5",
                    "flop: BTN call",
                    "flop: BB call",
                    "turn: BB check",
                    "turn: CO bet 18",
                ]
                ah = [
                    {"street": "flop", "actor": "BB", "action": "check"},
                    {"street": "flop", "actor": "CO", "action": "bet", "size": 5.0},
                    {"street": "flop", "actor": "BTN", "action": "call"},
                    {"street": "flop", "actor": "BB", "action": "call"},
                    {"street": "turn", "actor": "BB", "action": "check"},
                    {"street": "turn", "actor": "CO", "action": "bet", "size": 18.0},
                ]
                vac = 2  # bet flop + bet turn
                ncb = 1  # BTN called flop bet
                pot, tc = 25.5 + 18, 18.0
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=board,
                street="turn",
                hero_position="BB",
                villain_positions=["CO", "BTN"],
                pot=pot,
                to_call=tc,
                facing_bet=True,
                num_opponents=2,
                prior_actions=priors,
                generation_source=self.generation_source,
                opener_position="CO",
                bettor_position="CO",
                villain_aggression_count=vac,
                villain_checked_back=0,
                villain_call_count=0,
                num_callers_to_bet=ncb,
                facing_raise=0,
                action_history=ah,
            )
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        return out


# ─── T7 — NFD+overcards CALL under pot odds (10 CALL) ─────────────────


class T7NFDOvercardsCall(TemplateGenerator):
    """MW-17 family. Discriminative axis: has_flush_draw=1,
    nut_flush_block=1, overcard_outs>=4, is_ip=0, num_opponents=2
    (single-bet 3-way).

    Hero in BB has Ah+broadway with flush-draw and overcards facing
    CO single bet 3-way. Reasoning: nut-FD blocker against CO range +
    implied odds + overcard outs — CALL even if direct pot odds tight.
    """

    template_name = "T7"
    generation_source = "t7_nfd_overcards_call_pot_odds"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # Two-tone board (2 hearts/spades/etc) + hero AhKh / AhQh / AhJh
        # (2 same suit incl As/Ah for nut blocker) ⇒ 4 same suit total = FD
        # with nut blocker + 1-2 overcards. Bet size targets pot odds 24-30%.
        configs = [
            # (hero, flop, bet_size)
            ("AhKh", "Jh8h4d", 5.0),  # 2 board hearts + 2 hero hearts incl Ah
            ("AhQh", "Jh8h4d", 5.0),
            ("AhJh", "Th8h4d", 5.0),  # Ah + 1 overcard pairing
            ("AhTh", "Qh9h4d", 5.0),
            ("AdKd", "Jd8d4h", 5.0),  # diamonds
            ("AdQd", "Td8d4h", 5.0),
            ("AsKs", "Js8s4d", 5.0),  # spades
            ("AsQs", "Ts8s4h", 5.0),
            ("AcKc", "Tc8c4d", 5.0),  # clubs
            ("KhQh", "Th8h4d", 5.0),  # K-high FD + Q overcard (no nut blocker)
        ]
        out: List[GeneratedSituation] = []
        for i, (hero, flop, bet_size) in enumerate(configs[:target_count], start=1):
            sit_id = f"t7_nfd_overcards_call_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=flop,
                street="flop",
                hero_position="BB",
                villain_positions=["CO", "BTN"],
                pot=8.0 + bet_size,  # PFR raise 2.5 + 2 calls + BB call → 10.5 → CO bets 5 → pot=15.5
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
                villain_aggression_count=1,  # CO just bet
                villain_checked_back=0,
                villain_call_count=0,
                num_callers_to_bet=0,  # BTN folded, so 0 callers between bet and hero
                facing_raise=0,
                action_history=[
                    {"street": "flop", "actor": "BB", "action": "check"},
                    {"street": "flop", "actor": "CO", "action": "bet", "size": bet_size},
                    {"street": "flop", "actor": "BTN", "action": "fold"},
                ],
            )
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        return out


# ─── T8 — control hands across 5 buckets (36 mixed) ───────────────────


class T8Controls(TemplateGenerator):
    """Per design §3 T8 + §7 G4. Distribution target: 12 CHECK + 8 BET
    + 8 FOLD + 6 CALL + 2 RAISE = 36.

    ≥18 of these must have near-equivalents in the 494 corpus on
    (bucket × board family × facing_bet) for G4 labeller-drift detection
    at 12.5E-D. The factory chooses control patterns that mirror common
    cohort-2 generation_sources (monster_*, nfd_*, magg_*, donk_*,
    facing_*).
    """

    template_name = "T8"
    generation_source = "t8_controls"

    def generate(self, target_count: int) -> List[GeneratedSituation]:
        # 12 CHECK + 8 BET + 8 FOLD + 6 CALL + 2 RAISE = 36
        # All-check 4-way air patterns (cohort-2 monster_air style → CHECK):
        check_configs = [
            # (hero, flop, generation_kind)
            ("7c2d", "Ah8c5d", "air_oop"),
            ("8d3h", "Kh7c4d", "air_oop"),
            ("9c4h", "Ah6c2d", "air_oop"),
            ("7d2c", "Ad9c5h", "air_oop"),
            ("6s4d", "Ks7d2c", "air_oop"),
            ("5h2c", "Qc8d3s", "air_oop"),
            ("6c3d", "As6d2c", "weak_pair"),  # weak pair check
            ("7h4s", "9h7c4d", "two_pair_low"),  # two pair on bad board
            ("8s5d", "8h5c2d", "two_pair_check"),
            ("9d4c", "9c8d2h", "tp_weak_kicker"),
            ("Ts7c", "Td8c2h", "tp_weak"),
            ("8h4d", "Ah8c2d", "weak_tp"),
        ]
        # 8 BET — strong made hands first to act
        bet_configs = [
            ("AsKs", "AhKc7d", "two_pair_bet"),
            ("AhQs", "AcQd5h", "two_pair_bet"),
            ("KsQd", "KhQc6s", "two_pair_bet"),
            ("AhJh", "AcJd4c", "two_pair_bet"),
            ("AsKd", "Ah6c2d", "tptk_bet"),
            ("KsQh", "Kc8d3s", "tptk_bet"),
            ("9c9d", "9h6c2d", "set_bet_first"),  # set first to act
            ("8s8d", "8h7c2d", "set_bet_first"),
        ]
        # 8 FOLD — facing aggression with weak holdings
        fold_configs = [
            ("7c2d", "AhKc8s", 5.0),
            ("9d3h", "KhQc8s", 6.0),
            ("8s4c", "AhJh6c", 7.0),
            ("Tc4h", "KhQs8d", 5.0),
            ("9h2d", "AhQc7s", 8.0),
            ("8d3c", "KhJs6d", 6.0),
            ("7s4h", "AsTc6d", 5.0),
            ("9c5d", "KhTs7c", 7.0),
        ]
        # 6 CALL — TP+ value catchers facing single bet
        call_configs = [
            ("AhJs", "AcKd6c", 5.0),
            ("KhQs", "KcJd5h", 5.0),
            ("Th9c", "Tc8d3h", 5.0),
            ("Js9c", "Jc7d3h", 5.0),
            ("AhTd", "AsKc4d", 5.0),
            ("KhJs", "KcQd4h", 5.0),
        ]
        # 2 RAISE — flopped monsters facing aggression in standard spots
        raise_configs = [
            ("9s9c", "9h6c2d", 6.0),  # set facing CB
            ("8d8h", "8c5d2s", 7.0),  # set facing CB
        ]

        out: List[GeneratedSituation] = []
        i = 0
        for hero, flop, kind in check_configs:
            i += 1
            sit_id = f"t8_check_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=flop,
                street="flop",
                hero_position="BB",
                villain_positions=["CO", "BTN"],
                pot=10.5,
                to_call=0.0,
                facing_bet=False,
                num_opponents=2,
                prior_actions=[
                    "preflop: CO raise 2.5",
                    "preflop: BTN call",
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
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        i = 0
        for hero, flop, kind in bet_configs:
            i += 1
            sit_id = f"t8_bet_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=flop,
                street="flop",
                hero_position="BB",
                villain_positions=["CO", "BTN"],
                pot=10.5,
                to_call=0.0,
                facing_bet=False,
                num_opponents=2,
                prior_actions=[
                    "preflop: CO raise 2.5",
                    "preflop: BTN call",
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
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        i = 0
        for hero, flop, bet_size in fold_configs:
            i += 1
            sit_id = f"t8_fold_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=flop,
                street="flop",
                hero_position="BB",
                villain_positions=["CO"],
                pot=8.0 + bet_size,
                to_call=bet_size,
                facing_bet=True,
                num_opponents=1,
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
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        i = 0
        for hero, flop, bet_size in call_configs:
            i += 1
            sit_id = f"t8_call_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=flop,
                street="flop",
                hero_position="BB",
                villain_positions=["CO"],
                pot=8.0 + bet_size,
                to_call=bet_size,
                facing_bet=True,
                num_opponents=1,
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
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        i = 0
        for hero, flop, bet_size in raise_configs:
            i += 1
            sit_id = f"t8_raise_{i:02d}"
            row = emit_row(
                situation_id=sit_id,
                pilot_hand_id="",
                hero_cards=hero,
                board=flop,
                street="flop",
                hero_position="BB",
                villain_positions=["CO"],
                pot=8.0 + bet_size,
                to_call=bet_size,
                facing_bet=True,
                num_opponents=1,
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
            out.append(GeneratedSituation(situation_id=sit_id, row=row))
        return out[:target_count]


# ─── Generation harness ───────────────────────────────────────────────


# Per dispatch §"Deliverable for 12.5E-B": parametric file = 96 hands
# (12+10+10+12+12+8+10+22 = 96). The remaining 14 hands are authored as
# manual canonicals (2 per T1-T7) in a separate file
# (data/corpus_revision_125e_manual_canonicals_*.jsonl); together the
# parametric + manual files produce 110 hands satisfying design §3 totals.
_TEMPLATES: List[Tuple[str, TemplateGenerator, int]] = [
    ("T1", T1MonotoneFDCheckedThrough(), 12),
    ("T2", T2TPMediumKickerAfterPFRCheck(), 10),
    ("T3", T3RiverThinValueTPTK(), 10),
    ("T4", T4SlowplaySetTurnLead(), 12),
    ("T5", T5NFDGutshotRaiseOOP(), 12),
    ("T6", T6MonsterDelayedAggression(), 8),
    ("T7", T7NFDOvercardsCall(), 10),
    ("T8", T8Controls(), 22),
]
PARAMETRIC_TOTAL = 96  # 12+10+10+12+12+8+10+22
MANUAL_TOTAL = 14
GRAND_TOTAL = 110


def generate_all() -> List[Dict[str, Any]]:
    """Generate all 110 parametric situations.

    Each row's `pilot_hand_id` is assigned sequentially PILOT_495..PILOT_604
    in template order T1, T2, T3, T4, T5, T6, T7, T8.
    """
    rows: List[Dict[str, Any]] = []
    pid = PILOT_ID_START
    for tname, gen, count in _TEMPLATES:
        produced = gen.generate(count)
        if len(produced) != count:
            raise RuntimeError(
                f"Template {tname} produced {len(produced)}/{count} situations; "
                f"STOP per dispatch §'Stop conditions'"
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


# ─── G1-G3 self-checks (per design §7) ────────────────────────────────


def g1_join_cardinality(
    new_rows: List[Dict[str, Any]],
    existing_corpus_path: str,
) -> Tuple[bool, str]:
    """G1: pilot_hand_id 110/110 unique on new rows + zero collision with
    existing 494 rows' pilot_hand_id set.
    """
    new_ids = [r["pilot_hand_id"] for r in new_rows]
    if len(set(new_ids)) != len(new_ids):
        dups = [pid for pid in new_ids if new_ids.count(pid) > 1]
        return False, f"G1 FAIL: duplicate pilot_hand_ids in new rows: {dups[:5]}"
    if len(new_ids) != GRAND_TOTAL:
        return False, f"G1 FAIL: expected {GRAND_TOTAL} new rows (combined factory + manual), got {len(new_ids)}"
    if not os.path.exists(existing_corpus_path):
        return True, "G1 PARTIAL: existing corpus not found; skipping collision check"
    existing_ids = set()
    with open(existing_corpus_path) as f:
        for line in f:
            if line.strip():
                existing_ids.add(json.loads(line).get("pilot_hand_id"))
    collision = set(new_ids) & existing_ids
    if collision:
        return False, f"G1 FAIL: pilot_hand_id collision with existing 494: {sorted(collision)[:5]}"
    return True, f"G1 PASS: {len(new_ids)} unique pilot_hand_ids; zero collision with existing {len(existing_ids)}"


def g2_distribution(new_rows: List[Dict[str, Any]]) -> Tuple[bool, str]:
    """G2: per-template counts within ±1 of design §3 combined target.

    Combined targets = parametric (12+10+10+12+12+8+10+22) + manual (2 per
    T1-T7) ⇒ T1=14, T2=12, T3=12, T4=14, T5=14, T6=10, T7=12, T8=22.
    """
    factory_targets = {tname: count for tname, _, count in _TEMPLATES}
    # Manual canonicals add 2 per T1-T7 (none for T8).
    manual_per_template = {"T1": 2, "T2": 2, "T3": 2, "T4": 2,
                           "T5": 2, "T6": 2, "T7": 2, "T8": 0}
    combined_targets = {t: factory_targets[t] + manual_per_template.get(t, 0)
                        for t in factory_targets}
    found: Dict[str, int] = {tname: 0 for tname in combined_targets}
    for r in new_rows:
        sid = r["situation_id"]
        prefix = sid.split("_")[0].upper()  # 't1' → 'T1'
        if prefix in found:
            found[prefix] += 1
    deviations: List[str] = []
    for tname, want in combined_targets.items():
        got = found[tname]
        if abs(got - want) > 1:
            deviations.append(f"{tname}: {got}/{want} (Δ{got - want:+d})")
    if deviations:
        return False, f"G2 FAIL (>±1 hand off): {', '.join(deviations)}"
    deltas = ", ".join(f"{t}={found[t]}/{combined_targets[t]}" for t in combined_targets)
    return True, f"G2 PASS: {deltas}"


def g3_duplicate_detection(
    new_rows: List[Dict[str, Any]],
    existing_corpus_path: str,
) -> Tuple[bool, str]:
    """G3: zero (board, hero_cards, hero_position, prior_actions) tuple
    match against existing 494, AND zero internal duplicates among new rows.
    """
    def _fingerprint(r: Dict[str, Any]) -> Tuple:
        return (
            r.get("board"),
            r.get("hero_cards"),
            r.get("hero_position"),
            tuple(r.get("prior_actions") or []),
        )

    # Internal duplicate check (factory + manual)
    new_fps = [_fingerprint(r) for r in new_rows]
    seen: Dict[Tuple, str] = {}
    internal_dups: List[Tuple[str, str]] = []
    for r, fp in zip(new_rows, new_fps):
        if fp in seen:
            internal_dups.append((seen[fp], r["pilot_hand_id"]))
        else:
            seen[fp] = r["pilot_hand_id"]
    if internal_dups:
        return False, f"G3 FAIL (internal): {len(internal_dups)} duplicate fingerprint(s) within new rows: {internal_dups[:3]}"

    if not os.path.exists(existing_corpus_path):
        return True, "G3 PARTIAL: existing corpus not found; internal dedup PASS"

    existing_fps = set()
    with open(existing_corpus_path) as f:
        for line in f:
            if line.strip():
                existing_fps.add(_fingerprint(json.loads(line)))
    matches: List[str] = []
    for r in new_rows:
        if _fingerprint(r) in existing_fps:
            matches.append(r["pilot_hand_id"])
    if matches:
        return False, f"G3 FAIL: {len(matches)} rows duplicate existing 494: {matches[:5]}"
    return True, f"G3 PASS: 0 (board, hero, position, prior_actions) duplicates vs existing 494; 0 internal duplicates"


# ─── Track B — 14 manual canonical hand designs (2 per T1-T7) ─────────
#
# Per design §5.1: hand-authored canonicals matching BATCH2 reference-set
# quality bar. Each carries `author_design_note` for gto-expert review;
# the labeller prompt does NOT see the note (per
# `feedback_bucket_first_labelling.md` — the labeller reads the hand cold
# and reasons from features + composition + board + action history).
#
# pilot_hand_id range: PILOT_591..PILOT_604 (14 hands; immediately after
# parametric file end at PILOT_590).


PILOT_ID_START_MANUAL = 591


_MANUALS: List[Dict[str, Any]] = [
    # ─── T1 (MW-25 family) — monotone-flop FD checked-through 4-way ──
    {
        "template": "T1",
        "situation_id": "t1_manual_canonical_01",
        "author_design_note": (
            "Js9s4s monotone with hero AsKh: NFD + 2 over (A+K). 4-way after PFR check-through "
            "condenses villain ranges to weak Jx + air. BET 50% pot for fold equity + equity "
            "denial + protection. Drawing-bucket BET."
        ),
        "kwargs": dict(
            hero_cards="AsKh", board="Js9s4s", street="flop", hero_position="BTN",
            villain_positions=["HJ", "CO", "BB"], pot=11.0, to_call=0.0,
            facing_bet=False, num_opponents=3,
            # Amendment 2026-05-05 fix #7: insert missing `flop: BB check`
            # before `flop: HJ check` to complete the postflop sequence
            # (BB acts first; then PFR/HJ; then CO; then hero/BTN).
            prior_actions=["preflop: HJ raise 2.5", "preflop: CO call",
                           "preflop: BTN call", "preflop: BB call",
                           "flop: BB check",
                           "flop: HJ check", "flop: CO check"],
            generation_source="t1_manual_canonical", opener_position="HJ",
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
    {
        "template": "T1",
        "situation_id": "t1_manual_canonical_02",
        "author_design_note": (
            "Th7h3h monotone with hero AhQc: NFD + 1 over (A). MW-25 family with lower-board "
            "flush + 1 overcard. Drawing-bucket BET via fold equity + 9 NFD outs + Q overcard "
            "outs + position amplification."
        ),
        "kwargs": dict(
            hero_cards="AhQc", board="Th7h3h", street="flop", hero_position="BTN",
            villain_positions=["HJ", "CO", "BB"], pot=11.0, to_call=0.0,
            facing_bet=False, num_opponents=3,
            # Amendment 2026-05-05 fix #7: insert missing `flop: BB check`.
            prior_actions=["preflop: HJ raise 2.5", "preflop: CO call",
                           "preflop: BTN call", "preflop: BB call",
                           "flop: BB check",
                           "flop: HJ check", "flop: CO check"],
            generation_source="t1_manual_canonical", opener_position="HJ",
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
    # ─── T2 (MW-40 family) — TP medium kicker IP after PFR check ─────
    {
        "template": "T2",
        "situation_id": "t2_manual_canonical_01",
        "author_design_note": (
            "AhTd on Ac8s3d rainbow, BTN after HJ PFR check + CO check + BB check. PFR check-back "
            "on Ax in 4-way condenses HJ's range to weak Jx, broadways-no-A, air. AT TP-T-kicker "
            "is thin value + protection + equity denial. Strong-made-bucket BET."
        ),
        "kwargs": dict(
            hero_cards="AhTd", board="Ac8s3d", street="flop", hero_position="BTN",
            villain_positions=["HJ", "CO", "BB"], pot=11.0, to_call=0.0,
            facing_bet=False, num_opponents=3,
            # Amendment 2026-05-05 fix #7: insert missing `flop: BB check`.
            prior_actions=["preflop: HJ raise 2.5", "preflop: CO call",
                           "preflop: BTN call", "preflop: BB call",
                           "flop: BB check",
                           "flop: HJ check", "flop: CO check"],
            generation_source="t2_manual_canonical", opener_position="HJ",
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
    {
        "template": "T2",
        "situation_id": "t2_manual_canonical_02",
        "author_design_note": (
            "KhJc on Kc7d2s rainbow K-high. Same condensing logic as the AT/Ax variant: PFR (HJ) "
            "check-back ⇒ doesn't have Kx-strong; KJ TP-J-kicker is thin value vs Kx-weak + "
            "pocket pairs + air. Strong-made-bucket BET."
        ),
        "kwargs": dict(
            hero_cards="KhJc", board="Kc7d2s", street="flop", hero_position="BTN",
            villain_positions=["HJ", "CO", "BB"], pot=11.0, to_call=0.0,
            facing_bet=False, num_opponents=3,
            # Amendment 2026-05-05 fix #7: insert missing `flop: BB check`.
            prior_actions=["preflop: HJ raise 2.5", "preflop: CO call",
                           "preflop: BTN call", "preflop: BB call",
                           "flop: BB check",
                           "flop: HJ check", "flop: CO check"],
            generation_source="t2_manual_canonical", opener_position="HJ",
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
    # ─── T3 (MW-42 family) — river thin-value TPTK ───────────────────
    {
        "template": "T3",
        "situation_id": "t3_manual_canonical_01",
        "author_design_note": (
            "Ad8c2sQhKh river. Hero AsKs TPTK + nut blocker on river. CO opens HJ, BTN (hero) "
            "calls, BB calls preflop. Flop CO bet 5, BTN call, BB fold. Turn Q: CO check, BTN "
            "check. River K: CO check; hero (BTN, IP) faces a fresh river decision. CO's "
            "check-call-check line caps to one-pair + missed draws; thin value BET targeting "
            "weak Kx + Ax-mid kicker. Amendment 2026-05-05 fix #1: re-authored as BTN IP "
            "(matching PILOT_596 structure); fresh river decision (no hero-side or villain-side "
            "check on the river yet)."
        ),
        "kwargs": dict(
            hero_cards="AsKs", board="Ad8c2sQhKh", street="river", hero_position="BTN",
            villain_positions=["CO"], pot=22.0, to_call=0.0,
            facing_bet=False, num_opponents=1,
            prior_actions=["preflop: CO raise 2.5", "preflop: BTN call",
                           "preflop: BB call",
                           "flop: BB check", "flop: CO bet 5",
                           "flop: BTN call", "flop: BB fold",
                           "turn: CO check", "turn: BTN check",
                           "river: CO check"],
            generation_source="t3_manual_canonical", opener_position="CO",
            bettor_position="CO", villain_aggression_count=1,
            villain_checked_back=1, villain_call_count=0,
            num_callers_to_bet=0, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "bet", "size": 5.0},
                {"street": "flop", "actor": "BTN", "action": "call"},
                {"street": "flop", "actor": "BB", "action": "fold"},
                {"street": "turn", "actor": "CO", "action": "check"},
                {"street": "turn", "actor": "BTN", "action": "check"},
                {"street": "river", "actor": "CO", "action": "check"},
            ],
        ),
    },
    {
        "template": "T3",
        "situation_id": "t3_manual_canonical_02",
        "author_design_note": (
            "Ks7d3c5h2s river. Hero KhQc TPTK. CO bet flop, hero call, brick-brick run-out, CO "
            "checks turn + river. CO's check-call-check on dry K-high run-out caps to weak Kx + "
            "pocket pairs + missed broadways. Thin value BET targets Kx-weak + 9x-Tx-Jx-Qx pairs."
        ),
        "kwargs": dict(
            hero_cards="KhQc", board="Ks7d3c5h2s", street="river", hero_position="BTN",
            villain_positions=["CO"], pot=22.0, to_call=0.0,
            facing_bet=False, num_opponents=1,
            prior_actions=["preflop: CO raise 2.5", "preflop: BTN call",
                           "flop: CO bet 5", "flop: BTN call",
                           "turn: CO check", "turn: BTN check",
                           "river: CO check"],
            generation_source="t3_manual_canonical", opener_position="CO",
            bettor_position="CO", villain_aggression_count=1,
            villain_checked_back=1, villain_call_count=0,
            num_callers_to_bet=0, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "CO", "action": "bet", "size": 5.0},
                {"street": "flop", "actor": "BTN", "action": "call"},
                {"street": "turn", "actor": "CO", "action": "check"},
                {"street": "turn", "actor": "BTN", "action": "check"},
                {"street": "river", "actor": "CO", "action": "check"},
            ],
        ),
    },
    # ─── T4 (MW-45 family) — slowplayed set into turn lead 4-way ─────
    {
        "template": "T4",
        "situation_id": "t4_manual_canonical_01",
        "author_design_note": (
            "Hero 9c9d on 9h6s2cJh turn. Slowplay-set RAISE for value vs AJ/JJ + AK + KJ + "
            "protection vs draw completions. The literal MW-45 pattern (slowplayed set + "
            "turn-lead RAISE 4-way). Amendment 2026-05-05 fix #2: added `turn: BTN call` + "
            "`turn: SB fold` after CO turn bet so hero (BB, last to act) genuinely faces a "
            "decision in turn — facing CO bet + BTN call (1 caller behind committed) + SB folded."
        ),
        "kwargs": dict(
            hero_cards="9c9d", board="9h6s2cJh", street="turn", hero_position="BB",
            villain_positions=["CO", "BTN", "SB"], pot=35.0, to_call=12.0,
            facing_bet=True, num_opponents=3,
            prior_actions=["preflop: CO raise 2.5", "preflop: BTN call",
                           "preflop: SB call", "preflop: BB call",
                           "flop: SB check", "flop: BB check",
                           "flop: CO check", "flop: BTN check",
                           "turn: SB check", "turn: BB check",
                           "turn: CO bet 12", "turn: BTN call", "turn: SB fold"],
            generation_source="t4_manual_canonical", opener_position="CO",
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
    {
        "template": "T4",
        "situation_id": "t4_manual_canonical_02",
        "author_design_note": (
            "Hero 7s7d on 7h4c2sQs turn. Lower set rank + turn overcard Q. Slowplay-set RAISE for "
            "value vs AQ/KQ/QJ/QT + sets-of-Qs + occasional 2-pair; folds out air. Tests bucket "
            "uniformity across set rank. Amendment 2026-05-05 fix #3: added `turn: BTN call` + "
            "`turn: SB fold` so hero (BB) genuinely faces a decision after CO turn bet."
        ),
        "kwargs": dict(
            hero_cards="7s7d", board="7h4c2sQs", street="turn", hero_position="BB",
            villain_positions=["CO", "BTN", "SB"], pot=38.0, to_call=14.0,
            facing_bet=True, num_opponents=3,
            prior_actions=["preflop: CO raise 2.5", "preflop: BTN call",
                           "preflop: SB call", "preflop: BB call",
                           "flop: SB check", "flop: BB check",
                           "flop: CO check", "flop: BTN check",
                           "turn: SB check", "turn: BB check",
                           "turn: CO bet 14", "turn: BTN call", "turn: SB fold"],
            generation_source="t4_manual_canonical", opener_position="CO",
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
                {"street": "turn", "actor": "CO", "action": "bet", "size": 14.0},
                {"street": "turn", "actor": "BTN", "action": "call"},
                {"street": "turn", "actor": "SB", "action": "fold"},
            ],
        ),
    },
    # ─── T5 (MW-47 family) — NFD+gutshot semi-bluff RAISE OOP ────────
    # PRIMARY H-FEAT TEST. The two most canonical NFD-blocker hands.
    {
        "template": "T5",
        "situation_id": "t5_manual_canonical_01",
        "author_design_note": (
            "MW-47 6-low variant: hero AsQs on KsJs6c (two-tone spades + low brick distinct from "
            "factory's KsJs5c). Hero = NFD + gutshot to T. PFR opens, CO bets, BTN calls, hero "
            "OOP in BB. Combined Axes 3+4+5: position amplification (RAISE OOP folds out CO+BTN "
            "medium ranges); nut-FD blocker against CO bet+call range; equity denial vs broadway "
            "over-card realisation; 9 NFD outs + 4 broadway outs with fold equity."
        ),
        "kwargs": dict(
            hero_cards="AsQs", board="KsJs6c", street="flop", hero_position="BB",
            villain_positions=["HJ", "CO", "BTN"], pot=22.5, to_call=6.0,
            facing_bet=True, num_opponents=3,
            prior_actions=["preflop: HJ raise 2.5", "preflop: CO call",
                           "preflop: BTN call", "preflop: BB call",
                           "flop: BB check", "flop: HJ check",
                           "flop: CO bet 6", "flop: BTN call"],
            generation_source="t5_manual_canonical", opener_position="HJ",
            bettor_position="CO", villain_aggression_count=1,
            villain_checked_back=0, villain_call_count=1,
            num_callers_to_bet=1, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "HJ", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "bet", "size": 6.0},
                {"street": "flop", "actor": "BTN", "action": "call"},
            ],
        ),
    },
    {
        "template": "T5",
        "situation_id": "t5_manual_canonical_02",
        "author_design_note": (
            "Hero AhKh on JhTh5c (NFD + open-ender with nut blocker). Stronger draw equity "
            "(15 outs: 9 NFD + 6 OE = OE+NFD combo). Easier RAISE motivation than gutshot variant; "
            "tests booster's nut-blocker treatment across draw strengths."
        ),
        "kwargs": dict(
            hero_cards="AhKh", board="JhTh5c", street="flop", hero_position="BB",
            villain_positions=["HJ", "CO", "BTN"], pot=22.5, to_call=6.0,
            facing_bet=True, num_opponents=3,
            prior_actions=["preflop: HJ raise 2.5", "preflop: CO call",
                           "preflop: BTN call", "preflop: BB call",
                           "flop: BB check", "flop: HJ check",
                           "flop: CO bet 6", "flop: BTN call"],
            generation_source="t5_manual_canonical", opener_position="HJ",
            bettor_position="CO", villain_aggression_count=1,
            villain_checked_back=0, villain_call_count=1,
            num_callers_to_bet=1, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "HJ", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "bet", "size": 6.0},
                {"street": "flop", "actor": "BTN", "action": "call"},
            ],
        ),
    },
    # ─── T6 (MW-33-adjacent) — monster delayed-aggression ────────────
    {
        "template": "T6",
        "situation_id": "t6_manual_canonical_01",
        "author_design_note": (
            "Hero 8s8d on 8h6c2dQs turn. Flop bet+call (hero call). Turn Q: BB check, CO bets 18, "
            "BTN calls. Hero (BB, last to act) faces bet+call decision. Raises set for value vs "
            "over-pair + AQ + KQ + occasional bluffs. Amendment 2026-05-05 fix #4: added "
            "`turn: BTN call` so hero is genuinely next-to-act."
        ),
        "kwargs": dict(
            hero_cards="8s8d", board="8h6c2dQs", street="turn", hero_position="BB",
            villain_positions=["CO", "BTN"], pot=61.5, to_call=18.0,
            facing_bet=True, num_opponents=2,
            prior_actions=["preflop: CO raise 2.5", "preflop: BTN call",
                           "preflop: BB call", "flop: BB check", "flop: CO bet 5",
                           "flop: BTN call", "flop: BB call",
                           "turn: BB check", "turn: CO bet 18", "turn: BTN call"],
            generation_source="t6_manual_canonical", opener_position="CO",
            bettor_position="CO", villain_aggression_count=2,
            villain_checked_back=0, villain_call_count=1,
            num_callers_to_bet=1, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "bet", "size": 5.0},
                {"street": "flop", "actor": "BTN", "action": "call"},
                {"street": "flop", "actor": "BB", "action": "call"},
                {"street": "turn", "actor": "BB", "action": "check"},
                {"street": "turn", "actor": "CO", "action": "bet", "size": 18.0},
                {"street": "turn", "actor": "BTN", "action": "call"},
            ],
        ),
    },
    {
        "template": "T6",
        "situation_id": "t6_manual_canonical_02",
        "author_design_note": (
            "Hero 6c6d on 6s4h2cJd turn lead 3-way. Set on coordinated low + connected J turn. "
            "Hero (BB) faces CO bet + BTN call → RAISE for value vs JJ-overpair, AJ, KJ + "
            "protection vs draws. Tests booster generalisation across set ranks AND post-flop "
            "sequences. Amendment 2026-05-05 fix #5: added `turn: BTN call`."
        ),
        "kwargs": dict(
            hero_cards="6c6d", board="6s4h2cJd", street="turn", hero_position="BB",
            villain_positions=["CO", "BTN"], pot=34.5, to_call=12.0,
            facing_bet=True, num_opponents=2,
            prior_actions=["preflop: CO raise 2.5", "preflop: BTN call",
                           "preflop: BB call", "flop: BB check", "flop: CO check",
                           "flop: BTN check", "turn: BB check",
                           "turn: CO bet 12", "turn: BTN call"],
            generation_source="t6_manual_canonical", opener_position="CO",
            bettor_position="CO", villain_aggression_count=1,
            villain_checked_back=0, villain_call_count=1,
            num_callers_to_bet=1, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "check"},
                {"street": "flop", "actor": "BTN", "action": "check"},
                {"street": "turn", "actor": "BB", "action": "check"},
                {"street": "turn", "actor": "CO", "action": "bet", "size": 12.0},
                {"street": "turn", "actor": "BTN", "action": "call"},
            ],
        ),
    },
    # ─── T7 (MW-17 family) — NFD+overcards CALL under pot odds ───────
    {
        "template": "T7",
        "situation_id": "t7_manual_canonical_01",
        "author_design_note": (
            "MW-17 pattern: hero AhKh on Jh7h4d (board distinct from factory T7's Jh8h4d to "
            "avoid fingerprint duplicate), BB facing CO single bet 3-way (PFR opens, BTN "
            "calls, BB calls; flop CO bets, BTN folds, hero faces single bet). Hero AhKh = NFD + "
            "K overcard with nut-FD blocker (Ah). PURE drawing bucket (no top pair — board J "
            "high, hero K is overcard but no pair). Composition (NFD + overcards) + nut-FD "
            "blocker against CO range + implied odds make CALL profitable. Amendment 2026-05-05 "
            "fix #6: changed hero from AhJh (TPTK + NFD = strong_made bucket) to AhKh on a "
            "distinct board per gto-expert + ml-architect — restores MW-17's pure-draw template."
        ),
        "kwargs": dict(
            hero_cards="AhKh", board="Jh7h4d", street="flop", hero_position="BB",
            villain_positions=["CO", "BTN"], pot=13.0, to_call=5.0,
            facing_bet=True, num_opponents=2,
            prior_actions=["preflop: CO raise 2.5", "preflop: BTN call",
                           "preflop: BB call", "flop: BB check",
                           "flop: CO bet 5", "flop: BTN fold"],
            generation_source="t7_manual_canonical", opener_position="CO",
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
    {
        "template": "T7",
        "situation_id": "t7_manual_canonical_02",
        "author_design_note": (
            "Hero AdQh on Td9d4c, BB facing CO single bet (PFR opens, BTN folds preflop, BB "
            "calls). Hero overcards + back-door FD + back-door straight via QJT9 connectors. "
            "Pure draw-bucket CALL via implied odds on Q + A spikes + back-door equity. Tests "
            "MW-17 family without NFD specifically — ensures booster generalises."
        ),
        "kwargs": dict(
            hero_cards="AdQh", board="Td9d4c", street="flop", hero_position="BB",
            villain_positions=["CO"], pot=8.0, to_call=3.0,
            facing_bet=True, num_opponents=1,
            prior_actions=["preflop: CO raise 2.5", "preflop: BB call",
                           "flop: BB check", "flop: CO bet 3"],
            generation_source="t7_manual_canonical", opener_position="CO",
            bettor_position="CO", villain_aggression_count=1,
            villain_checked_back=0, villain_call_count=0,
            num_callers_to_bet=0, facing_raise=0,
            action_history=[
                {"street": "flop", "actor": "BB", "action": "check"},
                {"street": "flop", "actor": "CO", "action": "bet", "size": 3.0},
            ],
        ),
    },
]


def generate_manuals() -> List[Dict[str, Any]]:
    """Build the 14 manual canonical rows. Each carries `author_design_note`
    + `template` for gto-expert review (NOT consumed by labeller / trainer).
    """
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


# ─── CLI ──────────────────────────────────────────────────────────────


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="Phase 12.5E-B situation generator (110 hands across 8 templates)"
    )
    p.add_argument(
        "--output",
        default="data/corpus_revision_125e_situations_2026-05-04.jsonl",
        help="Output JSONL path for the 96 parametric situations",
    )
    p.add_argument(
        "--manual-output",
        default="data/corpus_revision_125e_manual_canonicals_2026-05-04.jsonl",
        help="Output JSONL path for the 14 manual canonical hands",
    )
    p.add_argument(
        "--existing-corpus",
        default="data/corpus_revision_500_hand_2026-04-27.jsonl",
        help="Existing 494-hand corpus path (G1 + G3 reference)",
    )
    p.add_argument("--strict", action="store_true",
        help="Exit non-zero if any G1-G3 self-check fails")
    args = p.parse_args(argv)

    out_abs = args.output if os.path.isabs(args.output) else os.path.join(_REPO, args.output)
    manual_abs = args.manual_output if os.path.isabs(args.manual_output) else os.path.join(_REPO, args.manual_output)
    existing_abs = args.existing_corpus if os.path.isabs(args.existing_corpus) else os.path.join(_REPO, args.existing_corpus)

    print(f"[gen] generating {PARAMETRIC_TOTAL} parametric situations ...", file=sys.stderr)
    parametric_rows = generate_all()
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
