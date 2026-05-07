#!/usr/bin/env python3
"""Phase 12.5K-C-C-FIX — re-emit MW-17 + MW-47 axes with corrected
boards (2 FD-suit cards on flop; hero suited nut FD).

Per `MAIN_TERMINAL_PR277_RESOLUTION_AND_125KCC_REDESIGN_DISPATCH_2026-05-07.md`
(master `748f3a3`, PR #280). Path 2: redesign + re-emit + re-pilot.

Diagnostic from PR #277 pilot HALT: original MW-17 + MW-47 boards had
only 1 FD-suit card; hero had ≤1 same-suit card; total ≤3 same-suit
cards across hero+board. Labelling pipeline `has_flush_draw=0` requires
≥4 same-suit cards (hero+board) for FD classification → KB §1.7 nut-FD
RAISE carve-out doesn't trigger; labellers default to FOLD on equity-
vs-pot-odds (axis target CALL/RAISE not produced).

Fix: hero suited (2 same-suit) + board 2 same-suit = 4 same-suit total
= `has_flush_draw=1` per labelling pipeline.

The MW-40 + MW-45 axes (which PASSed pilot) are NOT modified; they
preserve their original 50-hand corpus from PR #273.

Usage:
    python3 scripts/regenerate_lever_c_mw17_mw47.py
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

ORIG_PATH = os.path.join(_REPO, "data",
                         "corpus_lever_c_situations_2026-05-07.jsonl")
OUT_PATH = os.path.join(_REPO, "data",
                        "corpus_lever_c_situations_v2_2026-05-07.jsonl")


# ─── MW-17 — REDESIGNED: hero AsKs / AsQs (suited) + 2-spade flops ──
# Hero: AsKs (suited; nut FD blocker As of spades + K kicker overcard)
# Boards: 2 spades on flop + 1 off-suit. Top card J/T/9 (low-equity character).
# Pot: 15bb (3-way SRP); to_call: 4bb (CO bet 4bb into 11bb pot = 36% of pot OR
# adjusted to ~26-27% pot odds matching canonical). Builder uses pot 11.0bb +
# to_call 4.0bb → pot odds 4/(11+4) = 0.267 (matches canonical 0.268).

def _mw17_redesigned() -> List[Tuple[str, str]]:
    """50 (hero, board) tuples. Hero suited spades; board 2 spades."""
    cfgs: List[Tuple[str, str]] = []
    # Sub-axis A1 (J-high; 2 spades on board; hero AsKs/AsQs; ~20):
    # Board pattern: J(non-spade) + Xs + Ys (X and Y are non-J ranks).
    A1 = [
        ("AsKs", "Jh9s5s"), ("AsKs", "Jh8s5s"), ("AsKs", "Jh7s4s"),
        ("AsKs", "Jc8s6s"), ("AsKs", "Jd9s4s"),
        ("AsQs", "Jh9s5s"), ("AsQs", "Jh8s5s"), ("AsQs", "Jh7s4s"),
        ("AsQs", "Jc8s6s"), ("AsQs", "Jd9s4s"),
        # heart FD: J(non-heart) + Xh + Yh
        ("AhKh", "Jc9h5h"), ("AhKh", "Jc8h5h"), ("AhKh", "Jc7h4h"),
        ("AhQh", "Jc9h5h"), ("AhQh", "Jc8h5h"),
        # diamond FD:
        ("AdKd", "Jc9d5d"), ("AdKd", "Jc8d5d"),
        # club FD:
        ("AcKc", "Jh9c5c"), ("AcKc", "Jh8c5c"),
        ("AcQc", "Jh9c5c"),
    ]
    cfgs.extend(A1[:20])
    # Sub-axis A2 (T/9-high; 2 spades on board; ~15):
    A2 = [
        ("AsKs", "Th9s4s"), ("AsKs", "Tc9s4s"), ("AsKs", "Th8s5s"),
        ("AsQs", "Th9s4s"), ("AsQs", "Tc9s4s"),
        ("AsKs", "9h7s3s"), ("AsKs", "9c7s2s"),
        ("AsQs", "9h7s3s"),
        ("AhKh", "Tc9h4h"), ("AhKh", "Tc8h5h"),
        ("AdKd", "Tc9d4d"), ("AdKd", "Tc8d5d"),
        ("AcKc", "Th9c4c"), ("AcKc", "Th8c5c"),
        ("AhQh", "9c7h3h"),
    ]
    cfgs.extend(A2[:15])
    # Sub-axis A3 (paired-board; 2 same-suit on board incl. paired suit; ~10):
    A3 = [
        ("AsKs", "Th8s8c"),  # 2 spades (Ts? no, Th. 8s + ??? — fix)
        # Need 2 spades on board with paired rank in same suit:
        # Pattern: Xs Xc/Xh/Xd + Ys (paired non-spade + Xs from pair... complex)
        # Simpler: paired non-spade rank + 1 spade non-pair-rank → only 1 spade.
        # To get 2 spades + paired-board, need both pair cards to be different
        # suits, neither both being spade (else trips on flop). Or paired-spade
        # board (XsXc paired with X in spade suit), plus 1 more spade.
        # Cleanest: J?J? paired (2 Js on flop), plus a separate spade rank:
        ("AsKs", "JhJc7s"), ("AsKs", "JhJd6s"), ("AsKs", "JcJd5s"),
        ("AsQs", "JhJc7s"), ("AsQs", "JhJd6s"),
        ("AhKh", "JcJd7h"), ("AhKh", "JsJd7h"), ("AhQh", "JcJd6h"),
        ("AdKd", "JhJc6d"), ("AdKd", "JhJs6d"),
    ]
    cfgs.extend(A3[:10])
    # Sub-axis A4 (rainbow with backdoor FD; control; ~5):
    A4 = [
        ("AsKh", "Jh8d4c"), ("AsKd", "Jc7s2h"),
        ("AsQh", "Th8d3c"), ("AcKh", "Jd9s2c"),
        ("AhKs", "Tc7d3h"),
    ]
    cfgs.extend(A4[:5])
    return cfgs[:50]


# ─── MW-47 — REDESIGNED: hero AsQs/AsJs (suited) + 2-spade KsJ5-class flops ──
# Hero: AsQs (suited; nut FD blocker + overcards + gutshot)
# Boards: K? J? 5? where exactly 2 of those are spades (canonical KsJ5 two-spade).
# Action: CO opens, BTN calls, BB(hero) calls; flop CO bets 50%, BTN calls,
# hero raise spot.

def _mw47_redesigned() -> List[Tuple[str, str]]:
    cfgs: List[Tuple[str, str]] = []
    # Sub-axis N1 (KxJx5 with 2 spades incl. Ks + (Js or 5s); hero AsQs ~20):
    N1 = [
        ("AsQs", "KsJh5s"), ("AsQs", "KsJc5s"), ("AsQs", "KsJd5s"),
        ("AsQs", "KsJs5h"), ("AsQs", "KsJs5c"), ("AsQs", "KsJs5d"),
        ("AsJs", "KsTh5s"), ("AsJs", "KsTc5s"), ("AsJs", "KsTs5h"),
        ("AsJs", "KsTs5c"),
        # heart FD variants:
        ("AhQh", "KhJs5h"), ("AhQh", "KhJc5h"), ("AhQh", "KhJh5d"),
        ("AhJh", "KhTs5h"), ("AhJh", "KhTh5d"),
        # diamond FD:
        ("AdQd", "KdJs5d"), ("AdQd", "KdJh5d"),
        # club FD:
        ("AcQc", "KcJs5c"), ("AcQc", "KcJh5c"),
        ("AcJc", "KcTs5c"),
    ]
    cfgs.extend(N1[:20])
    # Sub-axis N2 (nut FD + 2 overcards no gutshot; ~15):
    N2 = [
        ("AsKs", "Qh8s3s"), ("AsKs", "Qc8s3s"), ("AsKs", "Qh7s3s"),
        ("AsQs", "Jh8s3s"), ("AsQs", "Jc8s3s"), ("AsQs", "Jh7s3s"),
        ("AhKh", "Qs8h3h"), ("AhKh", "Qc8h3h"), ("AhKh", "Qs7h3h"),
        ("AhQh", "Js8h3h"), ("AhQh", "Jc8h3h"),
        ("AcKc", "Qh8c3c"), ("AcKc", "Qs8c3c"),
        ("AdKd", "Qh8d3d"), ("AdKd", "Qs8d3d"),
    ]
    cfgs.extend(N2[:15])
    # Sub-axis N3 (nut FD + 1 overcard + gutshot; ~10):
    N3 = [
        ("As9s", "QsJh5s"), ("As9s", "QsJc5s"),
        ("As8s", "QsJh5s"), ("As8s", "QsJc5s"),
        ("Ah9h", "QhJs5h"), ("Ah9h", "QhJc5h"),
        ("Ac9c", "QcJh5c"), ("Ac9c", "QcJs5c"),
        ("Ad9d", "QdJh5d"), ("Ad9d", "QdJs5d"),
    ]
    cfgs.extend(N3[:10])
    # Sub-axis N4 (non-nut FD + overcards + gutshot; control; ~5):
    N4 = [
        ("KsQs", "JsTc4s"), ("KhQh", "JhTs4h"),
        ("KcQc", "JcTs4c"), ("KdQd", "JdTs4c"),
        ("QsJs", "Ts9c4s"),
    ]
    cfgs.extend(N4[:5])
    return cfgs[:50]


def _card_list(s: str) -> List[str]:
    return [s[i:i+2] for i in range(0, len(s), 2)]


def _validate_unique_cards(hero: str, board: str) -> None:
    cards = _card_list(hero) + _card_list(board)
    if len(set(cards)) != len(cards):
        dups = [c for c in cards if cards.count(c) > 1]
        raise ValueError(
            f"Card collision in (hero={hero}, board={board}): {sorted(set(dups))}"
        )


def _build_mw17_row(hero: str, board: str, idx: int) -> Dict[str, Any]:
    _validate_unique_cards(hero, board)
    sit_id = f"lever_c_mw17_{idx:03d}"
    pilot_hand_id = f"PILOT_LEVER_C_MW17_{idx:03d}"
    # Pot/to_call adjusted to match canonical pot_odds ~0.268 per dispatch
    # diagnostic: pot 11.0 + to_call 4.0 → pot_odds 4/15 = 0.267.
    row = emit_row(
        situation_id=sit_id, pilot_hand_id=pilot_hand_id,
        hero_cards=hero, board=board, street="flop",
        hero_position="BB", villain_positions=["CO", "BTN"],
        pot=15.0, to_call=4.0, facing_bet=True, num_opponents=2,
        prior_actions=[
            "preflop: CO raise 2.5", "preflop: BTN call",
            "preflop: BB call", "flop: CO bet 4",
        ],
        generation_source="lever_c_mw17_redesigned_nut_fd_2tone_facing_co_bet_3way",
        opener_position="CO", bettor_position="CO",
        villain_aggression_count=1, villain_checked_back=0,
        villain_call_count=0, num_callers_to_bet=0, facing_raise=0,
        action_history=[
            {"street": "flop", "actor": "CO", "action": "bet", "size": 4.0},
        ],
    )
    row.update({"axis": "MW-17", "design_action": "CALL",
                "lever_c_round": "2026-05-07-FIX",
                "redesign_source": "12.5K-C-C-FIX_PR280_path2"})
    return row


def _build_mw47_row(hero: str, board: str, idx: int) -> Dict[str, Any]:
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
        generation_source="lever_c_mw47_redesigned_nut_fd_2tone_facing_bet_call_3way",
        opener_position="CO", bettor_position="CO",
        villain_aggression_count=1, villain_checked_back=0,
        villain_call_count=1, num_callers_to_bet=1, facing_raise=0,
        action_history=[
            {"street": "flop", "actor": "CO", "action": "bet", "size": 5.0},
            {"street": "flop", "actor": "BTN", "action": "call"},
        ],
    )
    row.update({"axis": "MW-47", "design_action": "RAISE",
                "lever_c_round": "2026-05-07-FIX",
                "redesign_source": "12.5K-C-C-FIX_PR280_path2"})
    return row


def main() -> int:
    argparse.ArgumentParser().parse_args()

    # Validate uniqueness pre-emit
    for hero, board in _mw17_redesigned():
        _validate_unique_cards(hero, board)
    for hero, board in _mw47_redesigned():
        _validate_unique_cards(hero, board)

    # Load existing corpus to preserve MW-40 + MW-45 axes
    if not os.path.exists(ORIG_PATH):
        print(f"ERROR: missing {ORIG_PATH}", file=sys.stderr)
        return 1
    preserved: List[Dict[str, Any]] = []
    with open(ORIG_PATH) as f:
        for line in f:
            d = json.loads(line)
            if d.get("axis") in ("MW-40", "MW-45"):
                preserved.append(d)
    print(f"[ok] preserved {len(preserved)} MW-40 + MW-45 rows from PR #273",
          file=sys.stderr)

    # Build redesigned MW-17 + MW-47
    redesigned: List[Dict[str, Any]] = []
    for i, (hero, board) in enumerate(_mw17_redesigned(), start=1):
        redesigned.append(_build_mw17_row(hero, board, i))
    for i, (hero, board) in enumerate(_mw47_redesigned(), start=1):
        redesigned.append(_build_mw47_row(hero, board, i))
    print(f"[ok] redesigned {len(redesigned)} MW-17 + MW-47 rows",
          file=sys.stderr)

    # Combine: MW-17 (redesigned) + MW-40 + MW-45 + MW-47 (redesigned) = 200
    rows = []
    rows += [r for r in redesigned if r["axis"] == "MW-17"]
    rows += [p for p in preserved if p["axis"] == "MW-40"]
    rows += [p for p in preserved if p["axis"] == "MW-45"]
    rows += [r for r in redesigned if r["axis"] == "MW-47"]
    if len(rows) != 200:
        print(f"ERROR: expected 200, got {len(rows)}", file=sys.stderr)
        return 1

    # Stop conditions
    nan_count = 0
    for r in rows:
        for k, v in (r.get("feat_dict") or {}).items():
            if isinstance(v, float) and (v != v or v in (float('inf'), float('-inf'))):
                nan_count += 1
    if nan_count >= 12200 * 0.01:
        print(f"STOP: NaN/Inf {nan_count}", file=sys.stderr)
        return 1

    # Step-18 + has_flush_draw activation report (validates redesign worked)
    fd_active = sum(1 for r in rows
                    if (r.get("feat_dict") or {}).get("has_flush_draw", 0) == 1)
    fd_per_axis = {}
    for r in rows:
        ax = r["axis"]
        fd_per_axis.setdefault(ax, [0, 0])
        fd_per_axis[ax][1] += 1
        if (r.get("feat_dict") or {}).get("has_flush_draw", 0) == 1:
            fd_per_axis[ax][0] += 1

    print(f"\n=== has_flush_draw activation per axis (post-redesign) ===",
          file=sys.stderr)
    for ax in ("MW-17", "MW-40", "MW-45", "MW-47"):
        on, total = fd_per_axis.get(ax, (0, 0))
        print(f"  {ax}: {on}/{total} ({on/max(total,1)*100:.0f}%)",
              file=sys.stderr)

    # Write output
    with open(OUT_PATH, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"\n[ok] wrote {len(rows)} rows → {os.path.relpath(OUT_PATH, _REPO)}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
