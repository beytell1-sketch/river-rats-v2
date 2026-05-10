#!/usr/bin/env python3
"""Unit tests for scripts/generate_hu_situations.py (v2 board-mutating fix).

Per dispatch MAIN_TERMINAL_HU15LK10_ADJUDICATION_AND_GENERATOR_FIX_DISPATCH_2026-05-10.md
§"Binding spec" item 1d: assert per-anchor unique flop count > 1 across multiple
board_runout lookalikes; assert variation_param/board-state invariant on every row.

Invocation:
    python3 scripts/test_generate_hu_situations.py
or via pytest:
    pytest scripts/test_generate_hu_situations.py -v
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from collections import defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN_SCRIPT = os.path.join(REPO, "scripts", "generate_hu_situations.py")

# Import the module under test for unit-level coverage
sys.path.insert(0, os.path.dirname(GEN_SCRIPT))
import generate_hu_situations as gen  # noqa: E402


def _generate_all() -> list:
    """Re-run the generator into a fresh tempdir; return parsed situations.jsonl rows."""
    with tempfile.TemporaryDirectory() as tmp:
        # Patch the module-level PILOT_DIR to write into tmp
        orig_dir = gen.PILOT_DIR
        gen.PILOT_DIR = tmp
        try:
            rc = gen.main()
            assert rc == 0, f"Generator returned non-zero: {rc}"
            sit_path = os.path.join(tmp, "situations.jsonl")
            with open(sit_path) as f:
                rows = [json.loads(line) for line in f if line.strip()]
        finally:
            gen.PILOT_DIR = orig_dir
    return rows


def test_total_count():
    """50 lookalikes total: 5 anchors x 10 each."""
    rows = _generate_all()
    assert len(rows) == 50, f"Expected 50 rows, got {len(rows)}"


def test_anchor_count():
    """5 distinct anchors, 10 lookalikes each."""
    rows = _generate_all()
    by_anchor = defaultdict(list)
    for r in rows:
        by_anchor[r["anchor_id"]].append(r)
    assert len(by_anchor) == 5, f"Expected 5 anchors, got {len(by_anchor)}"
    for anchor_id, anchor_rows in by_anchor.items():
        assert len(anchor_rows) == 10, f"{anchor_id}: expected 10 rows, got {len(anchor_rows)}"


def test_per_anchor_board_diversity_for_flop_anchors():
    """For board_runout variations on flop anchors, board_flop must vary across lookalikes.

    This is the v1-bug regression test: prior generator left board_flop unchanged across
    all 5 board-runout variations. v2 must produce >=2 unique board_flops per anchor's
    5 board-runout variations (ideally 5 unique).
    """
    rows = _generate_all()
    by_anchor = defaultdict(list)
    for r in rows:
        if r["variation_axis"] == "board_runout":
            by_anchor[r["anchor_id"]].append(r)

    for anchor_id, runouts in by_anchor.items():
        anchor_spec = next(a for a in gen.HU1_ANCHORS if a["ref_id"] == anchor_id)
        if anchor_spec["street"] == "flop":
            unique_flops = {r["board_flop"] for r in runouts}
            assert len(unique_flops) > 1, (
                f"{anchor_id} (flop spot): only {len(unique_flops)} unique board_flop across "
                f"{len(runouts)} board_runout lookalikes — v1 bug regression"
            )


def test_per_anchor_board_diversity_for_turn_anchors():
    """For board_runout variations on turn anchors, board_turn must vary across lookalikes."""
    rows = _generate_all()
    by_anchor = defaultdict(list)
    for r in rows:
        if r["variation_axis"] == "board_runout":
            by_anchor[r["anchor_id"]].append(r)

    for anchor_id, runouts in by_anchor.items():
        anchor_spec = next(a for a in gen.HU1_ANCHORS if a["ref_id"] == anchor_id)
        if anchor_spec["street"] == "turn":
            unique_turns = {r["board_turn"] for r in runouts}
            assert len(unique_turns) > 1, (
                f"{anchor_id} (turn spot): only {len(unique_turns)} unique board_turn across "
                f"{len(runouts)} board_runout lookalikes — v1 bug regression"
            )


def test_per_anchor_board_diversity_for_river_anchors():
    """For board_runout variations on river anchors, board_river must vary across lookalikes."""
    rows = _generate_all()
    by_anchor = defaultdict(list)
    for r in rows:
        if r["variation_axis"] == "board_runout":
            by_anchor[r["anchor_id"]].append(r)

    for anchor_id, runouts in by_anchor.items():
        anchor_spec = next(a for a in gen.HU1_ANCHORS if a["ref_id"] == anchor_id)
        if anchor_spec["street"] == "river":
            unique_rivers = {r["board_river"] for r in runouts}
            assert len(unique_rivers) > 1, (
                f"{anchor_id} (river spot): only {len(unique_rivers)} unique board_river across "
                f"{len(runouts)} board_runout lookalikes — v1 bug regression"
            )


def test_variation_param_matches_board_state_invariant():
    """Per dispatch §"Binding spec" item 1d: every row passes the
    _assert_variation_param_matches_board_state invariant against its anchor."""
    rows = _generate_all()
    anchor_by_id = {a["ref_id"]: a for a in gen.HU1_ANCHORS}
    for r in rows:
        anchor = anchor_by_id[r["anchor_id"]]
        gen._assert_variation_param_matches_board_state(r, anchor)


def test_no_card_conflicts_in_board_mutations():
    """Mutated board cards must not conflict with hero cards or other board cards."""
    rows = _generate_all()
    for r in rows:
        if r["variation_axis"] != "board_runout":
            continue
        hero = gen._cards_in(r["hero_cards"])
        board = gen._cards_in(r["board_flop"])
        if r.get("board_turn"):
            board.append(r["board_turn"][-2:])
        if r.get("board_river"):
            board.append(r["board_river"][-2:])
        all_cards = hero + board
        assert len(all_cards) == len(set(all_cards)), (
            f"{r['spot_id']} has duplicate cards: hero={hero}, board={board}"
        )


def test_non_board_variations_leave_board_unchanged():
    """effective_stack / villain_action variations must not mutate board fields."""
    rows = _generate_all()
    anchor_by_id = {a["ref_id"]: a for a in gen.HU1_ANCHORS}
    for r in rows:
        if r["variation_axis"] in ("effective_stack", "villain_bet_sizing", "villain_action_sequence"):
            anchor = anchor_by_id[r["anchor_id"]]
            assert r.get("board_flop") == anchor.get("board_flop"), (
                f"{r['spot_id']} ({r['variation_axis']}) mutated board_flop"
            )
            assert r.get("board_turn") == anchor.get("board_turn"), (
                f"{r['spot_id']} ({r['variation_axis']}) mutated board_turn"
            )
            assert r.get("board_river") == anchor.get("board_river"), (
                f"{r['spot_id']} ({r['variation_axis']}) mutated board_river"
            )


def main() -> int:
    """Run all tests sequentially. Returns 0 on success, 1 on any failure."""
    tests = [
        test_total_count,
        test_anchor_count,
        test_per_anchor_board_diversity_for_flop_anchors,
        test_per_anchor_board_diversity_for_turn_anchors,
        test_per_anchor_board_diversity_for_river_anchors,
        test_variation_param_matches_board_state_invariant,
        test_no_card_conflicts_in_board_mutations,
        test_non_board_variations_leave_board_unchanged,
    ]
    failed = []
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except AssertionError as e:
            print(f"FAIL {t.__name__}: {e}")
            failed.append(t.__name__)
        except Exception as e:
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
            failed.append(t.__name__)
    print(f"\n{len(tests) - len(failed)}/{len(tests)} passed")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
