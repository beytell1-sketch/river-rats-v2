#!/usr/bin/env python3
"""Phase 12.5I-MW40-VERIFICATION-B situation generator — 30 J-on-board variants.

----------------------------------------------------------------------
FROZEN as of Phase 1.5-B (2026-05-09; master post PR #314).

This script targets the 61-surface that existed pre-Phase-1.5-B and
references J-B Step-18 features (`nut_blocker_overcard_count` +
`bet_call_multiway_oop_raise_pressure_index`) that were deleted in
Phase 1.5-B (J-B drop).

RETAINED for provenance of the 12.5I MW-40 verification artifacts
(see `data/corpus_revision_125i_mw40_verif_*`); NO LONGER RE-RUNNABLE
on the post-Phase-1.5-B codebase. Per `feedback_solver_findings.md` +
CLAUDE.md §6: do not mutate in-place; fork to a new variant if a
re-run on the 59-surface is needed.
----------------------------------------------------------------------

Implements amended spec from `MAIN_TERMINAL_PR236_MW40B_RESOLUTION_2026-05-06.md`
(master `42460ae`, PR #237) — Path γ' resolution of plan §4 contradiction:
- Sub-axis A (J-high, 7-9 secondary): 15 hands (10 from plan §4 + 5 fresh)
- Sub-axis B: DROPPED
- Sub-axis C (J-medium / set-of-Js paired-J boundary): 15 hands (10 from plan §4 + 5 fresh)
- Hero TJ uniform (off-suit) across all 30
- design_action = CHECK uniform per plan §3 prediction
- ref_id namespace: PILOT_MW40_VERIF_001..030 (disjoint from 788-corpus)

Hybrid pilot-first 4-check pre-flight on first 5 emitted situations
(binding per PR #228 SHOULD_FIX-1 Path 3 resolution): schema parity,
Step-18 plausibility, ref_id namespace integrity, top-level structural
fields. Pre-flight failure halts emission before reaching 30.

Re-uses helpers from `scripts/build_corpus_revision_125e_situations.py`
(via `scripts/build_corpus_revision_125i_situations.py` precedent).

Usage:
    python3 scripts/build_corpus_revision_125i_mw40_verif_situations.py
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

PILOT_ID_START = 1  # PILOT_MW40_VERIF_001
PILOT_ID_END = 30   # PILOT_MW40_VERIF_030
TARGET_TOTAL = 30
SUB_AXIS_A_COUNT = 15
SUB_AXIS_C_COUNT = 15

OUT_PATH = os.path.join(_REPO, "data",
                        "corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl")


# ─── Board × hero hand specifications ─────────────────────────────────

# Sub-axis A: J-high flop (J as highest card); rainbow; secondary in 7-9
# (with 1 plan-§4 carry-over Js6d4s where secondary=6 — orchestrator
# confirmed all 10 plan boards in PR #237 resolution).
#
# Hero TJ off-suit. Convention: hero T_suit = a suit not on the board
# when possible; hero J_suit = any non-spade suit != board J's suit and
# != hero T's suit; verify all cards unique.

SUB_AXIS_A_CONFIGS: List[Tuple[str, str]] = [
    # 10 from plan §4 (orchestrator-confirmed in PR #237):
    ("TdJc", "Js9c5h"),  # A01 — board s/c/h; T=d (4th suit), J=c (≠s)
    ("ThJc", "Js7d3c"),  # A02 — board s/d/c; T=h (4th), J=c (≠s); Jc ≠ 3c (different ranks)
    ("TcJh", "Js8h4d"),  # A03 — board s/h/d; T=c (4th), J=h (≠s); Jh ≠ 8h
    ("ThJc", "Js9d2c"),  # A04 — board s/d/c; T=h (4th), J=c (≠s); Jc ≠ 2c
    ("TdJh", "Js8c4h"),  # A05 — board s/c/h; T=d (4th), J=h (≠s); Jh ≠ 4h
    ("TcJh", "Js7h2d"),  # A06 — board s/h/d; T=c (4th), J=h (≠s)
    ("TdJc", "Js9h3c"),  # A07 — board s/h/c; T=d (4th), J=c (≠s); Jc ≠ 3c
    ("ThJc", "Js6d4s"),  # A08 — board s/d/s (2 spades; not rainbow); T=h, J=c (≠s); plan-§4 carry
    ("ThJd", "Js9c3d"),  # A09 — board s/c/d; T=h (4th), J=d (≠s); Jd ≠ 3d
    ("ThJd", "Js7c5d"),  # A10 — board s/c/d; T=h (4th), J=d (≠s); Jd ≠ 5d
    # 5 fresh selected per dispatch §"Sub-axis B board-list expansion":
    ("TcJd", "Js8d3h"),  # A11 — board s/d/h; T=c (4th), J=d (≠s); Jd ≠ 8d
    ("ThJc", "Js9c4d"),  # A12 — board s/c/d; T=h (4th), J=c (≠s)
    ("ThJc", "Js7c4d"),  # A13 — board s/c/d; T=h (4th), J=c (≠s); Jc ≠ 7c
    ("TdJc", "Js9h6c"),  # A14 — board s/h/c; T=d (4th), J=c (≠s); Jc ≠ 6c
    ("ThJc", "Js8d2c"),  # A15 — board s/d/c; T=h (4th), J=c (≠s); Jc ≠ 2c
]

# Sub-axis C: J middle-rank board (J highest among A/K/Q/J anchors;
# secondary 4-9); rainbow; ≤2 paired-J variants. Hero TJ off-suit.

SUB_AXIS_C_CONFIGS: List[Tuple[str, str]] = [
    # 10 from plan §4 (orchestrator-confirmed in PR #237):
    ("TsJc", "Jh5c2d"),  # C01 — board h/c/d; T=s (4th), J=c (≠h)
    ("TdJh", "Jc8h3s"),  # C02 — board c/h/s; T=d (4th), J=h (≠c); Jh ≠ 8h
    ("TsJc", "Jd9c4h"),  # C03 — board d/c/h; T=s (4th), J=c (≠d); Jc ≠ 9c
    ("TdJc", "Jh6s3c"),  # C04 — board h/s/c; T=d (4th), J=c (≠h); Jc ≠ 3c
    ("ThJd", "Jc7d2s"),  # C05 — board c/d/s; T=h (4th), J=d (≠c); Jd ≠ 7d
    ("TsJc", "Jd8c5h"),  # C06 — board d/c/h; T=s (4th), J=c (≠d); Jc ≠ 8c
    ("TdJc", "Jh4c2s"),  # C07 — board h/c/s; T=d (4th), J=c (≠h); Jc ≠ 4c
    ("TsJd", "Jc9h6d"),  # C08 — board c/h/d; T=s (4th), J=d (≠c); Jd ≠ 6d
    ("TsJc", "Jd7h3c"),  # C09 — board d/h/c; T=s (4th), J=c (≠d); Jc ≠ 3c
    ("ThJd", "JcJh4s"),  # C10 — paired-J boundary (Jc+Jh on board); T=h, J=d. Both Th and Jd not on board. Off-suit. ✓
    # 5 fresh selected (J highest on flop; rainbow; non-paired); hero TJ off-suit:
    ("TcJd", "Jh7s3d"),  # C11 — board h/s/d; T=c (4th), J=d (≠h); Jd ≠ 3d (different rank). Off-suit ✓
    ("TsJh", "Jc8d4h"),  # C12 — board c/d/h; T=s (4th), J=h (≠c); Jh ≠ 4h. Off-suit ✓
    ("TsJd", "Jh6d2c"),  # C13 — board h/d/c; T=s (4th), J=d (≠h); Jd ≠ 6d. Off-suit ✓
    ("TsJh", "Jd5h3c"),  # C14 — board d/h/c; T=s (4th), J=h (≠d); Jh ≠ 5h. Off-suit ✓
    ("TsJd", "Jc7h4d"),  # C15 — board c/h/d; T=s (4th), J=d (≠c); Jd ≠ 4d. Off-suit ✓
]


# ─── Card uniqueness sanity helper (run at script-load time) ──────────


def _card_list(s: str) -> List[str]:
    return [s[i:i+2] for i in range(0, len(s), 2)]


def _validate_unique_cards(hero: str, board: str) -> None:
    cards = _card_list(hero) + _card_list(board)
    if len(set(cards)) != len(cards):
        dups = [c for c in cards if cards.count(c) > 1]
        raise ValueError(
            f"Card collision in (hero={hero}, board={board}): {sorted(set(dups))}"
        )


# ─── Pre-flight 4-check (Hybrid pilot-first per PR #228 SHOULD_FIX-1) ──


_PLAN_S3_CONSTRAINT_FIELDS = {
    # Top-level structural fields per plan §3 — check 5 of them on the
    # emitted row. The factory hardcodes hero_seat=BTN, hero is non-PFA
    # (caller; opener=HJ), num_opponents=3, street=flop, no facing bet.
    "hero_position": "BTN",
    "street": "flop",
    "num_opponents": 3,
    "facing_bet": False,
    "to_call": 0.0,
}


def _preflight_4check(rows: List[Dict[str, Any]],
                      existing_ref_ids: set) -> Tuple[bool, List[str]]:
    """Pre-flight 4-check on first 5 emitted situations.

    Returns (passed, messages). On failure, messages explain which check
    failed and why; no further situations should be emitted.
    """
    msgs: List[str] = []
    if len(rows) != 5:
        return False, [f"Pre-flight expects exactly 5 rows; got {len(rows)}"]

    # Check 1 — schema parity: every feat_dict has 61 keys, 0 NaN, 0 Inf
    expected_n = None
    for r in rows:
        fd = r.get("feat_dict") or {}
        n = len(fd)
        if expected_n is None:
            expected_n = n
        elif n != expected_n:
            msgs.append(f"Check 1 FAIL: feat_dict size drift "
                        f"({r.get('pilot_hand_id')}: {n} vs first row {expected_n})")
        for k, v in fd.items():
            if isinstance(v, float):
                if v != v or v in (float('inf'), float('-inf')):
                    msgs.append(f"Check 1 FAIL: NaN/Inf in {r.get('pilot_hand_id')}.{k}={v}")
    if expected_n != 61:
        msgs.append(f"Check 1 FAIL: feat_dict size {expected_n} != 61 (post-PR #205 surface)")
    if any("Check 1" in m for m in msgs):
        return False, msgs
    msgs.append(f"Check 1 PASS: 5 rows × {expected_n} keys; 0 NaN/Inf")

    # Check 2 — Step-18 feature plausibility. Per plan §5 prediction:
    # `nut_blocker_overcard_count` ≈ 0 across all (hero IP, no nut-FD
    # blocker semantics on J-on-board); `bet_call_multiway_oop_raise_
    # pressure_index` ≈ 0 (hero IP not OOP). REPORT only — not a halt
    # per amended dispatch §"Stop conditions".
    s18a_active = sum(1 for r in rows
                      if (r.get("feat_dict") or {}).get("nut_blocker_overcard_count", 0) > 0)
    s18b_active = sum(1 for r in rows
                      if (r.get("feat_dict") or {}).get(
                          "bet_call_multiway_oop_raise_pressure_index", 0) > 0)
    msgs.append(f"Check 2 REPORT: Step-18 activations on first 5 — "
                f"nut_blocker_overcard_count={s18a_active}/5, "
                f"bet_call_multiway_oop_raise_pressure_index={s18b_active}/5 "
                f"(plan §5 predicted ≈0 for both)")

    # Check 3 — ref_id namespace integrity
    seen = set()
    for r in rows:
        rid = r.get("pilot_hand_id")
        if not rid or not rid.startswith("PILOT_MW40_VERIF_"):
            msgs.append(f"Check 3 FAIL: ref_id {rid!r} not in PILOT_MW40_VERIF_* namespace")
        if rid in seen:
            msgs.append(f"Check 3 FAIL: duplicate ref_id within first 5: {rid}")
        seen.add(rid)
        if rid in existing_ref_ids:
            msgs.append(f"Check 3 FAIL: ref_id collision with 788-corpus or prior 125i: {rid}")
    if any("Check 3 FAIL" in m for m in msgs):
        return False, msgs
    msgs.append(f"Check 3 PASS: 5 ref_ids in PILOT_MW40_VERIF_* namespace; 0 collisions")

    # Check 4 — top-level structural fields on all 5
    for r in rows:
        rid = r.get("pilot_hand_id")
        for field, expected in _PLAN_S3_CONSTRAINT_FIELDS.items():
            actual = r.get(field)
            if actual != expected:
                msgs.append(f"Check 4 FAIL: {rid}.{field}={actual!r} != expected {expected!r}")
    if any("Check 4 FAIL" in m for m in msgs):
        return False, msgs
    msgs.append(f"Check 4 PASS: 5 rows × {len(_PLAN_S3_CONSTRAINT_FIELDS)} structural fields all match plan §3")

    return True, msgs


# ─── Existing-ref_id loader (for collision check) ─────────────────────


def _load_existing_ref_ids() -> set:
    """Load all ref_ids / pilot_hand_ids from existing 788-corpus and
    prior 12.5I situations to verify the new namespace is disjoint.
    """
    paths = [
        os.path.join(_REPO, "data", "corpus_combined_788_2026-05-06.jsonl"),
        os.path.join(_REPO, "data", "corpus_revision_125i_situations_2026-05-06.jsonl"),
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


# ─── Row builder (one situation per (hero, board) tuple) ──────────────


def _build_situation(hero: str, board: str, sub_axis: str, idx: int,
                     pilot_n: int) -> Dict[str, Any]:
    """Emit one canonical 4-way SRP checked-through situation per the
    constraints in plan §3 + amended dispatch §"Sub-axis distribution".
    """
    _validate_unique_cards(hero, board)
    sit_id = f"t11mw40v_{sub_axis}_{idx:02d}"
    pilot_hand_id = f"PILOT_MW40_VERIF_{pilot_n:03d}"
    row = emit_row(
        situation_id=sit_id,
        pilot_hand_id=pilot_hand_id,
        hero_cards=hero,
        board=board,
        street="flop",
        hero_position="BTN",
        villain_positions=["HJ", "CO", "BB"],
        pot=11.0,  # 4-way SRP at 200bb stacks; matches T9'-expanded precedent
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
        generation_source="t11_mw40_verification_j_on_board_tpmk_4way_checked_through",
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
    # Path γ' metadata — uniform across all 30
    row["template_id"] = "T11_MW40V"
    row["sub_axis"] = sub_axis
    row["blocker_variant"] = "with_J_blocker"  # uniform per Path γ' (hero TJ → 1 J in hand)
    row["design_action"] = "CHECK"
    return row


# ─── Main ─────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true",
                        help="Exit non-zero on any stop-condition trigger.")
    args = parser.parse_args()

    # Pre-flight: validate uniqueness on every (hero, board) tuple
    for hero, board in SUB_AXIS_A_CONFIGS + SUB_AXIS_C_CONFIGS:
        _validate_unique_cards(hero, board)

    if len(SUB_AXIS_A_CONFIGS) != SUB_AXIS_A_COUNT:
        print(f"STOP: sub-axis A count {len(SUB_AXIS_A_CONFIGS)} != {SUB_AXIS_A_COUNT}",
              file=sys.stderr)
        return 1
    if len(SUB_AXIS_C_CONFIGS) != SUB_AXIS_C_COUNT:
        print(f"STOP: sub-axis C count {len(SUB_AXIS_C_CONFIGS)} != {SUB_AXIS_C_COUNT}",
              file=sys.stderr)
        return 1

    existing_ref_ids = _load_existing_ref_ids()
    print(f"[info] loaded {len(existing_ref_ids)} existing ref_ids for collision check",
          file=sys.stderr)

    # Build first 5 situations (sub-axis A, indices 1-5)
    first5: List[Dict[str, Any]] = []
    for i, (hero, board) in enumerate(SUB_AXIS_A_CONFIGS[:5], start=1):
        first5.append(_build_situation(hero, board, "A", i, pilot_n=i))

    passed, msgs = _preflight_4check(first5, existing_ref_ids)
    print("\n=== Hybrid pilot-first 4-check pre-flight on first 5 emitted ===",
          file=sys.stderr)
    for m in msgs:
        print(f"  {m}", file=sys.stderr)
    if not passed:
        print("\nSTOP: pre-flight 4-check failed; no further situations emitted.",
              file=sys.stderr)
        return 1
    print("=== Pre-flight PASS — proceeding with remaining 25 situations ===\n",
          file=sys.stderr)

    # Continue emission with sub-axis A indices 6..15 + sub-axis C 1..15
    rows: List[Dict[str, Any]] = list(first5)
    pilot_n = 5
    for i, (hero, board) in enumerate(SUB_AXIS_A_CONFIGS[5:], start=6):
        pilot_n += 1
        rows.append(_build_situation(hero, board, "A", i, pilot_n=pilot_n))
    for i, (hero, board) in enumerate(SUB_AXIS_C_CONFIGS, start=1):
        pilot_n += 1
        rows.append(_build_situation(hero, board, "C", i, pilot_n=pilot_n))

    if len(rows) != TARGET_TOTAL:
        print(f"STOP: emitted {len(rows)} rows; expected {TARGET_TOTAL}",
              file=sys.stderr)
        return 1

    # Post-emission stop condition checks
    a_count = sum(1 for r in rows if r["sub_axis"] == "A")
    c_count = sum(1 for r in rows if r["sub_axis"] == "C")
    if a_count != SUB_AXIS_A_COUNT or c_count != SUB_AXIS_C_COUNT:
        print(f"STOP: sub-axis split = A:{a_count}/C:{c_count}; "
              f"expected A:{SUB_AXIS_A_COUNT}/C:{SUB_AXIS_C_COUNT}",
              file=sys.stderr)
        return 1

    blocker_uniform = all(r["blocker_variant"] == "with_J_blocker" for r in rows)
    if not blocker_uniform:
        print("STOP: blocker_variant not uniform with_J_blocker; Path γ' violated",
              file=sys.stderr)
        return 1

    # ref_id collision check on full 30
    new_ids = [r["pilot_hand_id"] for r in rows]
    if len(set(new_ids)) != len(new_ids):
        print("STOP: duplicate ref_ids within new 30", file=sys.stderr)
        return 1
    collisions = [rid for rid in new_ids if rid in existing_ref_ids]
    if collisions:
        print(f"STOP: {len(collisions)} ref_id collision(s) with existing corpus: "
              f"{collisions[:5]}", file=sys.stderr)
        return 1

    # NaN/Inf check across full 30
    nan_count = 0
    for r in rows:
        for k, v in (r.get("feat_dict") or {}).items():
            if isinstance(v, float) and (v != v or v in (float('inf'), float('-inf'))):
                nan_count += 1
    nan_pct = nan_count / max(len(rows) * 61, 1) * 100
    if nan_pct >= 1.0:
        print(f"STOP: NaN/Inf rate {nan_pct:.2f}% >= 1% threshold "
              f"({nan_count} of {len(rows) * 61} values)",
              file=sys.stderr)
        return 1

    # design_action discipline
    bad_action = [r["pilot_hand_id"] for r in rows if r["design_action"] != "CHECK"]
    if bad_action:
        print(f"STOP: design_action != CHECK on {len(bad_action)} rows: "
              f"{bad_action[:5]}", file=sys.stderr)
        return 1

    # Step-18 activation report (REPORT, not STOP)
    s18a_active = sum(1 for r in rows
                      if (r.get("feat_dict") or {}).get("nut_blocker_overcard_count", 0) > 0)
    s18b_active = sum(1 for r in rows
                      if (r.get("feat_dict") or {}).get(
                          "bet_call_multiway_oop_raise_pressure_index", 0) > 0)

    # Distribution stats
    print("\n=== Distribution ===", file=sys.stderr)
    print(f"  Total: {len(rows)}", file=sys.stderr)
    print(f"  Sub-axis A (J-high): {a_count}", file=sys.stderr)
    print(f"  Sub-axis C (J-medium / set-of-Js): {c_count}", file=sys.stderr)
    print(f"  Blocker (uniform with_J_blocker): {sum(1 for r in rows if r['blocker_variant']=='with_J_blocker')}", file=sys.stderr)
    print(f"  ref_id range: {new_ids[0]} ... {new_ids[-1]}", file=sys.stderr)
    print(f"  NaN/Inf: {nan_count} of {len(rows) * 61} values ({nan_pct:.4f}%)",
          file=sys.stderr)
    print(f"  Step-18 nut_blocker_overcard_count > 0: {s18a_active}/{len(rows)} "
          f"(plan §5 predicted ≈0)", file=sys.stderr)
    print(f"  Step-18 bet_call_multiway_oop_raise_pressure_index > 0: {s18b_active}/{len(rows)} "
          f"(plan §5 predicted ≈0)", file=sys.stderr)

    # Write output
    with open(OUT_PATH, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"\n[ok] wrote {len(rows)} situations → {os.path.relpath(OUT_PATH, _REPO)}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
