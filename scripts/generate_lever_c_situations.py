#!/usr/bin/env python3
"""Phase 12.5K-C-B Lever C situation generator — 200 J-on-board variants
across 4 stay-wrong axes (MW-17 / MW-40 / MW-45 / MW-47).

Per `MAIN_TERMINAL_PR269_RESOLUTION_AND_125KCB_DISPATCH_2026-05-07.md`
(master `adee95d`, PR #272). Mirrors PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md
spec; per-axis pilot-first 4-check pre-flight on first 5 emitted situations
per axis (Hybrid pilot-first per PR #228 SHOULD_FIX-1 Path 3 precedent).

Re-uses:
- `scripts/build_corpus_revision_125e_situations.py` emit_row primitives
- 12.5I-MW40-VERIFICATION-B factory pattern from
  `scripts/build_corpus_revision_125i_mw40_verif_situations.py`

For MW-40 axis: per plan §3 R1 special case, re-use 30 already-labelled
situations from `data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl`
(re-tagged with PILOT_LEVER_C_MW40_001..030 namespace) + emit 20 fresh
J-on-board variants (PILOT_LEVER_C_MW40_031..050).

Usage:
    python3 scripts/generate_lever_c_situations.py
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Tuple

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CORE = os.path.join(_REPO, "river-rats-core")
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)
sys.path.insert(0, os.path.join(_REPO, "scripts"))

from build_corpus_revision_125e_situations import emit_row  # noqa: E402

OUT_PATH = os.path.join(_REPO, "data",
                        "corpus_lever_c_situations_2026-05-07.jsonl")
MW40_REUSE_PATH = os.path.join(
    _REPO, "data",
    "corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl",
)
PER_AXIS = 50
TOTAL = 4 * PER_AXIS  # 200


# ─── Axis MW-17 — CALL on nut FD facing CO bet 3-way ──────────────────
# Hero: AKs/AQs (with ♠ for spade-suited boards) — nut FD + overcards
# Board: J-high or T-high two-tone (FD suit + 2 other ranks); CO bet 33%
# Action: CO opens, BTN calls, BB(hero) calls; flop CO bets 33% pot

def _mw17_configs() -> List[Tuple[str, str]]:
    """50 (hero, board) tuples. Hero holds nut FD + overcards.
    Boards are two-tone (FD suit + 2 off-suits); J-high or T-high or 9-high.
    """
    cfgs: List[Tuple[str, str]] = []
    # Sub-axis A1 (Jx-high spade two-tone; ~20):
    # Hero AKs/AQs spade; board Jx-spade + 2 off-suits.
    A1 = [
        ("AsKh", "Js8s5d"), ("AsQh", "Js8s5d"),  # AK/AQ on Js8s5d
        ("AsKh", "Js7s4c"), ("AsQh", "Js7s4c"),
        ("AsKc", "Js9s3h"), ("AsQc", "Js9s3h"),
        ("AsKd", "Js6s2c"), ("AsQd", "Js6s2c"),
        ("AsKh", "Jc8c3d"), ("AsQh", "Jc8c3d"),  # club FD variants
        ("AcKh", "Jc8c3d"), ("AcQh", "Jc8c3d"),
        ("AhKd", "Jh7h3c"), ("AhQd", "Jh7h3c"),  # heart FD
        ("AhKs", "Jh9h4c"), ("AhQs", "Jh9h4c"),
        ("AdKc", "Jd8d3h"), ("AdQc", "Jd8d3h"),  # diamond FD
        ("AdKh", "Jd6d2c"), ("AdQh", "Jd6d2c"),
    ]
    cfgs.extend(A1[:20])
    # Sub-axis A2 (Tx-high or 9x-high two-tone; ~15):
    A2 = [
        ("AsKh", "Ts8s4d"), ("AsQh", "Ts7s3c"),
        ("AsKc", "Ts6s2h"), ("AcKh", "Tc9c4d"),
        ("AcQh", "Tc8c3d"), ("AhKd", "Th9h2c"),
        ("AhKs", "Th7h4c"), ("AdKc", "Td8d3h"),
        ("AsKh", "9s8s4d"), ("AsQh", "9s7s2c"),
        ("AcKh", "9c8c3d"), ("AhKd", "9h6h2c"),
        ("AdKc", "9d7d3h"), ("AsKc", "9s6s2c"),
        ("AhKc", "9h5h2d"),
    ]
    cfgs.extend(A2[:15])
    # Sub-axis A3 (paired-board two-tone; ~10):
    A3 = [
        ("AsKh", "Js8s8d"), ("AsQh", "JsJc6s"),
        ("AsQc", "Ts8s8d"), ("AsKd", "9s8s8h"),
        ("AcKh", "JcTd6c"), ("AcKh", "Jc7c7d"),
        ("AhKd", "Th9h9c"), ("AhKs", "Jh4h4d"),
        ("AdKc", "Jd6d6h"), ("AdQs", "Td9d9c"),
    ]
    cfgs.extend(A3[:10])
    # Sub-axis A4 (rainbow with backdoor nut FD; ~5; control):
    A4 = [
        ("AsKh", "Jh8d4c"), ("AsKd", "Jc7s2h"),
        ("AsQh", "Th8d3c"), ("AcKh", "Jd9s2c"),
        ("AhKs", "Tc7d3h"),
    ]
    cfgs.extend(A4[:5])
    return cfgs[:50]


# ─── Axis MW-40 — BET on TPMK 4-way checked-through ──────────────────
# Hero: TJ off-suit; board: J-on-board; matches MW-40-VERIFICATION-B
# Re-use 30 already-labelled + 20 fresh per plan §3 R1 special case.

def _mw40_fresh_configs() -> List[Tuple[str, str]]:
    """20 fresh J-on-board variants distinct from MW-40-VERIFICATION-B's 30."""
    return [
        ("TdJh", "Js8c2d"),  # F1
        ("TcJd", "Js5h3c"),
        ("ThJd", "Js9c2h"),
        ("TdJc", "Js6h3d"),
        ("ThJc", "Js7d4h"),
        ("TcJh", "Js6c4d"),
        ("TdJh", "Jc9d3s"),
        ("ThJc", "Jh8s2d"),
        ("TsJh", "Jc9d4s"),
        ("TdJc", "Jh7s2d"),
        ("ThJd", "Jc8s5h"),
        ("TsJd", "Jh9c2s"),
        ("TcJh", "Jd6c3s"),
        ("ThJd", "Jc7s4h"),
        ("TdJc", "Jh8d2s"),
        ("TsJc", "Jh5d2s"),
        ("ThJs", "Jc9d4h"),
        ("TdJs", "Jh8c3d"),
        ("TcJs", "Jh6d4c"),
        ("TsJh", "Jc7d3s"),
    ]


def _mw40_load_reused() -> List[Dict[str, Any]]:
    """Load and re-tag the 30 already-labelled MW-40-VERIFICATION-B rows."""
    rows: List[Dict[str, Any]] = []
    if not os.path.exists(MW40_REUSE_PATH):
        return rows
    with open(MW40_REUSE_PATH) as f:
        for line in f:
            d = json.loads(line)
            rows.append(d)
    return rows[:30]


# ─── Axis MW-45 — RAISE slowplay-set + broadway-completed turn ──────
# Hero: small-set (5x5x or 6x6x); flop: AKx or AK5/AK6; turn: Q or J broadway
# Action: hero OOP CO leads turn → hero raise spot

def _mw45_configs() -> List[Tuple[str, str]]:
    """50 (hero, board) tuples with TURN included.
    Format: hero=NN; board=AAB-T (4 cards: flop3 + turn1).
    """
    cfgs: List[Tuple[str, str]] = []
    # Sub-axis MW45-1 (bottom-set 5x + broadway-Q turn; 20):
    # Pattern: A?K?5?-Q? with 4 distinct suits across the 4 board cards;
    # hero pair-rank-5 in 2 suits not occupied by the board's 5.
    M1 = [
        ("5c5d", "AhKs5h-Qc"), ("5c5s", "AhKs5h-Qc"), ("5d5s", "AhKs5h-Qc"),
        ("5c5d", "AsKh5s-Qd"), ("5c5h", "AsKh5s-Qd"), ("5d5h", "AsKh5s-Qd"),
        ("5c5h", "AdKc5d-Qh"), ("5c5s", "AdKc5d-Qh"), ("5h5s", "AdKc5d-Qh"),
        ("5d5h", "AcKd5c-Qs"), ("5d5s", "AcKd5c-Qs"), ("5h5s", "AcKd5c-Qs"),
        # 6x set extension:
        ("6c6d", "AhKs6h-Qc"), ("6c6s", "AhKs6h-Qc"), ("6d6s", "AhKs6h-Qc"),
        ("6c6d", "AsKh6s-Qd"), ("6c6h", "AsKh6s-Qd"), ("6d6h", "AsKh6s-Qd"),
        # 4x set:
        ("4c4d", "AhKs4h-Qc"), ("4c4s", "AhKs4h-Qc"),
    ]
    cfgs.extend(M1[:20])
    # Sub-axis MW45-2 (bottom-set + J broadway turn; 15):
    M2 = [
        ("5c5d", "AhKs5h-Jc"), ("5c5s", "AhKs5h-Jc"), ("5d5s", "AhKs5h-Jc"),
        ("5c5d", "AsKh5s-Jd"), ("5c5h", "AsKh5s-Jd"), ("5d5h", "AsKh5s-Jd"),
        ("5c5h", "AdKc5d-Jh"), ("5c5s", "AdKc5d-Jh"), ("5h5s", "AdKc5d-Jh"),
        ("6c6d", "AhKs6h-Jc"), ("6c6s", "AhKs6h-Jc"), ("6d6s", "AhKs6h-Jc"),
        ("4c4d", "AhKs4h-Jc"), ("4c4s", "AhKs4h-Jc"),
        ("7c7d", "AhKs7h-Jc"),
    ]
    cfgs.extend(M2[:15])
    # Sub-axis MW45-3 (middle-set + broadway turn; 10):
    M3 = [
        ("8c8d", "Ah8s5d-Qc"), ("8c8h", "Ah8s5d-Qc"),
        ("9c9d", "Ah9s5d-Qc"), ("9c9h", "Ah9s5d-Qc"),
        ("8c8d", "Ah8s5d-Jc"), ("8c8h", "Ah8s5d-Jc"),
        ("9c9d", "Ah9s5d-Jc"), ("9c9h", "Ah9s5d-Jc"),
        ("7c7d", "Ah7s5d-Qc"), ("7c7h", "Ah7s5d-Qc"),
    ]
    cfgs.extend(M3[:10])
    # Sub-axis MW45-4 (top-set + broadway turn; 5; control):
    M4 = [
        ("AcAd", "AhKs5c-Qd"), ("AcAs", "AhKs5c-Qd"),
        ("AcAd", "AhKs6c-Jd"), ("AcAs", "AhKs6c-Jd"),
        ("KcKd", "AhKs5h-Qc"),
    ]
    cfgs.extend(M4[:5])
    return cfgs[:50]


# ─── Axis MW-47 — RAISE nut FD+OESD facing bet+call ──────────────────
# Hero: AsQs/AsJs (nut FD + overcards + gutshot OESD); board: KsJ5 spade/heart
# Action: CO opens, BTN calls, BB(hero) calls; flop CO bets 50%, BTN calls,
# hero raise spot

def _mw47_configs() -> List[Tuple[str, str]]:
    cfgs: List[Tuple[str, str]] = []
    # Sub-axis MW47-1 (nut FD + 2 overcards + gutshot; ~20):
    N1 = [
        ("AsQs", "KsJh5d"), ("AsQs", "KsJc5h"),
        ("AsJs", "KsTh5d"), ("AsJs", "KsTc5h"),
        ("AsKs", "QsJh5d"), ("AsKs", "QsJc5h"),
        ("AhQh", "KhJs5d"), ("AhQh", "KhJc5s"),
        ("AhJh", "KhTs5d"), ("AhJh", "KhTc5s"),
        ("AhKh", "QhJs5d"), ("AhKh", "QhJc5s"),
        ("AcQc", "KcJs5d"), ("AcQc", "KcJh5s"),
        ("AcJc", "KcTs5d"), ("AcJc", "KcTh5s"),
        ("AdQd", "KdJs5c"), ("AdQd", "KdJh5c"),
        ("AdJd", "KdTs5c"), ("AdJd", "KdTh5c"),
    ]
    cfgs.extend(N1[:20])
    # Sub-axis MW47-2 (nut FD + 2 overcards no gutshot; ~15):
    N2 = [
        ("AsKs", "Qs8h3d"), ("AsKs", "Qs7c2d"),
        ("AsQs", "Js8h3d"), ("AsQs", "Js7c2d"),
        ("AhKh", "Qh8s3d"), ("AhKh", "Qh7c2s"),
        ("AhQh", "Jh8s3d"), ("AhQh", "Jh7c2s"),
        ("AcKc", "Qc8s3d"), ("AcKc", "Qc7h2d"),
        ("AcQc", "Jc8s3d"), ("AcQc", "Jc7h2d"),
        ("AdKd", "Qd8s3c"), ("AdKd", "Qd7h2s"),
        ("AdQd", "Jd8s3c"),
    ]
    cfgs.extend(N2[:15])
    # Sub-axis MW47-3 (nut FD + 1 overcard + gutshot; ~10):
    N3 = [
        ("As9s", "QsJh5d"), ("As9s", "QsJc5h"),
        ("Ah9h", "QhJs5d"), ("Ah9h", "QhJc5s"),
        ("Ac9c", "QcJs5d"), ("Ac9c", "QcJh5s"),
        ("Ad9d", "QdJs5c"), ("Ad9d", "QdJh5c"),
        ("As8s", "QsJh5d"), ("Ah8h", "QhJs5d"),
    ]
    cfgs.extend(N3[:10])
    # Sub-axis MW47-4 (non-nut FD + overcards + gutshot; ~5; control):
    N4 = [
        ("KsQs", "JsTc4d"), ("KhQh", "JhTs4d"),
        ("KcQc", "JcTs4d"), ("KdQd", "JdTs4c"),
        ("QsJs", "TsT9c4d"[:6] if len("TsT9c4d") < 7 else "Ts9c4d"),
    ]
    cfgs.extend(N4[:5])
    return cfgs[:50]


# ─── Card uniqueness sanity helper ────────────────────────────────────


def _card_list(s: str) -> List[str]:
    # Strip dashes (used in board strings with turn)
    s2 = s.replace("-", "")
    return [s2[i:i+2] for i in range(0, len(s2), 2)]


def _validate_unique_cards(hero: str, board: str) -> None:
    cards = _card_list(hero) + _card_list(board)
    if len(set(cards)) != len(cards):
        dups = [c for c in cards if cards.count(c) > 1]
        raise ValueError(
            f"Card collision in (hero={hero}, board={board}): {sorted(set(dups))}"
        )


# ─── Per-axis row builders ────────────────────────────────────────────


def _build_mw17_row(hero: str, board: str, idx: int) -> Dict[str, Any]:
    """MW-17 axis: hero 3-way OOP facing CO bet on flop (50% pot)."""
    _validate_unique_cards(hero, board)
    sit_id = f"lever_c_mw17_{idx:03d}"
    pilot_hand_id = f"PILOT_LEVER_C_MW17_{idx:03d}"
    row = emit_row(
        situation_id=sit_id, pilot_hand_id=pilot_hand_id,
        hero_cards=hero, board=board, street="flop",
        hero_position="BB", villain_positions=["CO", "BTN"],
        pot=15.0,  # 3-way SRP + CO bet 50% of 10bb
        to_call=5.0, facing_bet=True, num_opponents=2,
        prior_actions=[
            "preflop: CO raise 2.5", "preflop: BTN call",
            "preflop: BB call", "flop: CO bet 5",
        ],
        generation_source="lever_c_mw17_nut_fd_facing_co_bet_3way",
        opener_position="CO", bettor_position="CO",
        villain_aggression_count=1, villain_checked_back=0,
        villain_call_count=0, num_callers_to_bet=0, facing_raise=0,
        action_history=[
            {"street": "flop", "actor": "CO", "action": "bet", "size": 5.0},
        ],
    )
    row.update({"axis": "MW-17", "design_action": "CALL",
                "lever_c_round": "2026-05-07"})
    return row


def _build_mw40_row_fresh(hero: str, board: str, idx: int) -> Dict[str, Any]:
    """MW-40 axis fresh variants 31..50: J-on-board TPMK 4-way checked."""
    _validate_unique_cards(hero, board)
    sit_id = f"lever_c_mw40_{idx:03d}"
    pilot_hand_id = f"PILOT_LEVER_C_MW40_{idx:03d}"
    row = emit_row(
        situation_id=sit_id, pilot_hand_id=pilot_hand_id,
        hero_cards=hero, board=board, street="flop",
        hero_position="BTN", villain_positions=["HJ", "CO", "BB"],
        pot=11.0, to_call=0.0, facing_bet=False, num_opponents=3,
        prior_actions=[
            "preflop: HJ raise 2.5", "preflop: CO call",
            "preflop: BTN call", "preflop: BB call",
            "flop: BB check", "flop: HJ check", "flop: CO check",
        ],
        generation_source="lever_c_mw40_tpmk_4way_checked_through_fresh",
        opener_position="HJ", bettor_position=None,
        villain_aggression_count=0, villain_checked_back=1,
        villain_call_count=0, num_callers_to_bet=0, facing_raise=0,
        action_history=[
            {"street": "flop", "actor": "BB", "action": "check"},
            {"street": "flop", "actor": "HJ", "action": "check"},
            {"street": "flop", "actor": "CO", "action": "check"},
        ],
    )
    row.update({"axis": "MW-40", "design_action": "BET",
                "lever_c_round": "2026-05-07"})
    return row


def _build_mw45_row(hero: str, board_with_turn: str, idx: int) -> Dict[str, Any]:
    """MW-45 axis: hero 3-way IP (BTN); flop checks; turn CO leads;
    hero raise spot. Board format: 'AhKs5h-Qc' (flop + turn)."""
    flop, turn = board_with_turn.split("-")
    full_board = flop + turn  # e.g., AhKs5hQc
    _validate_unique_cards(hero, full_board)
    sit_id = f"lever_c_mw45_{idx:03d}"
    pilot_hand_id = f"PILOT_LEVER_C_MW45_{idx:03d}"
    row = emit_row(
        situation_id=sit_id, pilot_hand_id=pilot_hand_id,
        hero_cards=hero, board=full_board, street="turn",
        hero_position="BTN", villain_positions=["CO", "BB"],
        pot=20.0, to_call=12.0, facing_bet=True, num_opponents=2,
        prior_actions=[
            "preflop: CO raise 2.5", "preflop: BTN call",
            "preflop: BB call", "flop: BB check", "flop: CO check",
            "flop: BTN check", "turn: BB check",
            "turn: CO bet 12",
        ],
        generation_source="lever_c_mw45_slowplay_set_broadway_turn_facing_lead",
        opener_position="CO", bettor_position="CO",
        villain_aggression_count=1, villain_checked_back=0,
        villain_call_count=0, num_callers_to_bet=0, facing_raise=0,
        action_history=[
            {"street": "flop", "actor": "BB", "action": "check"},
            {"street": "flop", "actor": "CO", "action": "check"},
            {"street": "flop", "actor": "BTN", "action": "check"},
            {"street": "turn", "actor": "BB", "action": "check"},
            {"street": "turn", "actor": "CO", "action": "bet", "size": 12.0},
        ],
    )
    row.update({"axis": "MW-45", "design_action": "RAISE",
                "lever_c_round": "2026-05-07"})
    return row


def _build_mw47_row(hero: str, board: str, idx: int) -> Dict[str, Any]:
    """MW-47 axis: hero BB (3-way); CO opens, BTN calls, hero calls;
    flop CO bets, BTN calls, hero raise spot."""
    _validate_unique_cards(hero, board)
    sit_id = f"lever_c_mw47_{idx:03d}"
    pilot_hand_id = f"PILOT_LEVER_C_MW47_{idx:03d}"
    row = emit_row(
        situation_id=sit_id, pilot_hand_id=pilot_hand_id,
        hero_cards=hero, board=board, street="flop",
        hero_position="BB", villain_positions=["CO", "BTN"],
        pot=20.0, to_call=10.0, facing_bet=True, num_opponents=2,
        prior_actions=[
            "preflop: CO raise 2.5", "preflop: BTN call",
            "preflop: BB call", "flop: CO bet 5",
            "flop: BTN call",
        ],
        generation_source="lever_c_mw47_nut_fd_facing_bet_call_3way",
        opener_position="CO", bettor_position="CO",
        villain_aggression_count=1, villain_checked_back=0,
        villain_call_count=1, num_callers_to_bet=1, facing_raise=0,
        action_history=[
            {"street": "flop", "actor": "CO", "action": "bet", "size": 5.0},
            {"street": "flop", "actor": "BTN", "action": "call"},
        ],
    )
    row.update({"axis": "MW-47", "design_action": "RAISE",
                "lever_c_round": "2026-05-07"})
    return row


# ─── Pre-flight 4-check on first 5 per axis ──────────────────────────


def _preflight_4check_axis(rows: List[Dict[str, Any]],
                            axis: str,
                            existing_ref_ids: set) -> Tuple[bool, List[str]]:
    msgs: List[str] = []
    if len(rows) != 5:
        return False, [f"Pre-flight expects 5 rows for axis {axis}; got {len(rows)}"]
    expected_n = None
    for r in rows:
        fd = r.get("feat_dict") or {}
        n = len(fd)
        if expected_n is None:
            expected_n = n
        elif n != expected_n:
            msgs.append(f"Check 1 FAIL [{axis}]: feat_dict size drift "
                        f"({r.get('pilot_hand_id')}: {n} vs {expected_n})")
        for k, v in fd.items():
            if isinstance(v, float) and (v != v or v in (float('inf'), float('-inf'))):
                msgs.append(f"Check 1 FAIL [{axis}]: NaN/Inf "
                            f"{r.get('pilot_hand_id')}.{k}={v}")
    if expected_n != 59:
        msgs.append(f"Check 1 FAIL [{axis}]: feat_dict size {expected_n} != 59")
    if any("Check 1 FAIL" in m for m in msgs):
        return False, msgs
    msgs.append(f"Check 1 PASS [{axis}]: 5 rows × 59 keys; 0 NaN/Inf")

    seen = set()
    expected_prefix = f"PILOT_LEVER_C_{axis.replace('-', '')}_"
    for r in rows:
        rid = r.get("pilot_hand_id")
        if not rid or not rid.startswith(expected_prefix):
            msgs.append(f"Check 3 FAIL [{axis}]: ref_id {rid!r} not in "
                        f"{expected_prefix}* namespace")
        if rid in seen:
            msgs.append(f"Check 3 FAIL [{axis}]: duplicate ref_id: {rid}")
        seen.add(rid)
        if rid in existing_ref_ids:
            msgs.append(f"Check 3 FAIL [{axis}]: collision with existing: {rid}")
    if any("Check 3 FAIL" in m for m in msgs):
        return False, msgs
    msgs.append(f"Check 3 PASS [{axis}]: 5 ref_ids in {expected_prefix}*; "
                f"0 collisions")

    expected_action = {"MW-17": "CALL", "MW-40": "BET",
                       "MW-45": "RAISE", "MW-47": "RAISE"}[axis]
    for r in rows:
        if r.get("design_action") != expected_action:
            msgs.append(f"Check 4 FAIL [{axis}]: {r.get('pilot_hand_id')} "
                        f"design_action={r.get('design_action')!r} != {expected_action!r}")
    if any("Check 4 FAIL" in m for m in msgs):
        return False, msgs
    msgs.append(f"Check 4 PASS [{axis}]: 5 rows × design_action={expected_action}")
    return True, msgs


# ─── Existing-ref_id loader ──────────────────────────────────────────


def _load_existing_ref_ids() -> set:
    paths = [
        os.path.join(_REPO, "data", "corpus_combined_788_2026-05-06.jsonl"),
        os.path.join(_REPO, "data",
                     "corpus_revision_125i_situations_2026-05-06.jsonl"),
        os.path.join(_REPO, "data",
                     "corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl"),
    ]
    ids: set = set()
    for p in paths:
        if not os.path.exists(p):
            continue
        with open(p) as f:
            for line in f:
                d = json.loads(line)
                phid = d.get("pilot_hand_id")
                if phid:
                    ids.add(phid)
                sid = d.get("situation_id")
                if sid:
                    ids.add(sid)
    return ids


# ─── Main ─────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    existing_ids = _load_existing_ref_ids()
    print(f"[info] {len(existing_ids)} existing ref_ids for collision check",
          file=sys.stderr)

    # Validate per-axis card uniqueness BEFORE any feat_dict computation
    for hero, board in _mw17_configs():
        _validate_unique_cards(hero, board)
    for hero, board in _mw40_fresh_configs():
        _validate_unique_cards(hero, board)
    for hero, board in _mw45_configs():
        _validate_unique_cards(hero, board.replace("-", ""))
    for hero, board in _mw47_configs():
        _validate_unique_cards(hero, board)

    # Build all rows (per axis)
    rows: List[Dict[str, Any]] = []

    # MW-17: 50 fresh
    for i, (hero, board) in enumerate(_mw17_configs(), start=1):
        rows.append(_build_mw17_row(hero, board, i))

    # MW-40: 30 re-used + 20 fresh = 50
    reused = _mw40_load_reused()
    if len(reused) != 30:
        print(f"WARN: expected 30 MW-40 reused, got {len(reused)}",
              file=sys.stderr)
    for i, r in enumerate(reused, start=1):
        # Re-tag with PILOT_LEVER_C_MW40_NNN
        new_row = dict(r)
        new_row["situation_id"] = f"lever_c_mw40_{i:03d}_reused"
        new_row["pilot_hand_id"] = f"PILOT_LEVER_C_MW40_{i:03d}"
        new_row["axis"] = "MW-40"
        new_row["design_action"] = "BET"  # per MW-40 verification consensus
        new_row["lever_c_round"] = "2026-05-07"
        new_row["lever_c_source"] = "reused_from_mw40_verification_b_pr236"
        rows.append(new_row)
    for i, (hero, board) in enumerate(_mw40_fresh_configs(), start=31):
        rows.append(_build_mw40_row_fresh(hero, board, i))

    # MW-45: 50 fresh (with turn)
    for i, (hero, board_turn) in enumerate(_mw45_configs(), start=1):
        rows.append(_build_mw45_row(hero, board_turn, i))

    # MW-47: 50 fresh
    for i, (hero, board) in enumerate(_mw47_configs(), start=1):
        rows.append(_build_mw47_row(hero, board, i))

    # Pre-flight 4-check on first 5 of EACH axis
    print("\n=== Per-axis pre-flight 4-check (first 5 of each axis) ===",
          file=sys.stderr)
    overall_ok = True
    for axis in ("MW-17", "MW-40", "MW-45", "MW-47"):
        axis_rows = [r for r in rows if r.get("axis") == axis][:5]
        ok, msgs = _preflight_4check_axis(axis_rows, axis, existing_ids)
        for m in msgs:
            print(f"  {m}", file=sys.stderr)
        if not ok:
            overall_ok = False
    if not overall_ok:
        print("\nSTOP: pre-flight 4-check failed; no situations emitted.",
              file=sys.stderr)
        return 1

    # Post-emission stop conditions
    per_axis_count: Dict[str, int] = {}
    for r in rows:
        per_axis_count[r.get("axis")] = per_axis_count.get(r.get("axis"), 0) + 1
    for axis, count in per_axis_count.items():
        if count != PER_AXIS:
            print(f"STOP: axis {axis} count {count} != {PER_AXIS}",
                  file=sys.stderr)
            return 1

    new_ids = [r.get("pilot_hand_id") for r in rows]
    if len(set(new_ids)) != len(new_ids):
        print("STOP: duplicate ref_ids within new 200", file=sys.stderr)
        return 1
    collisions = [rid for rid in new_ids if rid in existing_ids]
    if collisions:
        print(f"STOP: {len(collisions)} ref_id collision(s): {collisions[:5]}",
              file=sys.stderr)
        return 1

    nan_count = 0
    for r in rows:
        for k, v in (r.get("feat_dict") or {}).items():
            if isinstance(v, float) and (v != v or v in (float('inf'), float('-inf'))):
                nan_count += 1
    nan_pct = nan_count / max(len(rows) * 61, 1) * 100
    if nan_pct >= 1.0:
        print(f"STOP: NaN/Inf {nan_pct:.2f}% >= 1%", file=sys.stderr)
        return 1

    bad_action = [r["pilot_hand_id"] for r in rows
                  if r["design_action"] not in ("CALL", "BET", "RAISE")]
    if bad_action:
        print(f"STOP: design_action invalid on {len(bad_action)} rows: {bad_action[:5]}",
              file=sys.stderr)
        return 1

    # Distribution stats
    print("\n=== Distribution ===", file=sys.stderr)
    print(f"  Total: {len(rows)}", file=sys.stderr)
    for axis in ("MW-17", "MW-40", "MW-45", "MW-47"):
        print(f"  {axis}: {per_axis_count.get(axis, 0)}", file=sys.stderr)
    print(f"  ref_id range MW-17: PILOT_LEVER_C_MW17_001..050", file=sys.stderr)
    print(f"  ref_id range MW-40: PILOT_LEVER_C_MW40_001..050 "
          f"(001-030 re-used; 031-050 fresh)", file=sys.stderr)
    print(f"  ref_id range MW-45: PILOT_LEVER_C_MW45_001..050", file=sys.stderr)
    print(f"  ref_id range MW-47: PILOT_LEVER_C_MW47_001..050", file=sys.stderr)
    print(f"  NaN/Inf: {nan_count} of {len(rows) * 59} values", file=sys.stderr)

    # Write output
    with open(OUT_PATH, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"\n[ok] wrote {len(rows)} situations → "
          f"{os.path.relpath(OUT_PATH, _REPO)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
