#!/usr/bin/env python3
"""Phase 1.5-D.3 HU lookalike generator (v2 — board-field-mutating fix).

Per dispatch MAIN_TERMINAL_HU65_OWNER_ADJUDICATION_AND_PHASE15D3_DISPATCH_2026-05-10.md
+ design memo §4.4. Generates HU lookalike situations anchored on the
30-spot HU reference set.

Pilot v2 mode (this run): anchors on HU-1 axis (5 spots) only. Generates
~10 variations per anchor = 50 lookalikes total. Output: pilot_50_v2/.

v2 fix (per MAIN_TERMINAL_HU15LK10_ADJUDICATION_AND_GENERATOR_FIX_DISPATCH_2026-05-10.md):
the prior v1 generator described board-runout mutations in `variation_param`
prose but did NOT actually mutate `board_flop`/`board_turn`/`board_river`
fields. v2 actually mutates board fields per `variation_param` semantics
and asserts post-generation that EITHER variation_param describes a non-board
mutation AND board fields equal anchor, OR variation_param describes a board
mutation AND at least one board field differs from anchor.

Variation axes (per design memo §4.4):
- Board run-out: replace lowest-rank flop card (flop spots) or turn/river brick (turn/river spots), suit-preserving where structural draw matters
- SPR/effective stack (60/100/150bb)
- Villain action sequence (bet-size variation; check-back lines)

Output:
  data/hu_corpus/pilot_50_v2/situations.jsonl  - 50 lookalike specs
  data/hu_corpus/pilot_50_v2/similarity_distance_audit.jsonl - per-spot anchor + variation axis
"""
from __future__ import annotations

import json
import os
import random
import sys
from typing import Dict, List, Optional, Tuple

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HU_AXIS_1_SPEC = os.path.join(REPO, "design", "hu_reference_set", "HU_AXIS_1_MADE_HAND.md")
PILOT_DIR = os.path.join(REPO, "data", "hu_corpus", "pilot_50_v2")
FULL_DIR = os.path.join(REPO, "data", "hu_corpus", "full_HU2_HU6")

# Phase 1.5-D.3 FULL anchors (HU-2..HU-6; 24 anchors; HU-6.5 excluded — already adjudicated CALL by owner per PR #338)
# Imported from sibling module to keep this file readable.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hu_anchors_axes_2_6 import ALL_HU2_HU6_ANCHORS  # noqa: E402

# Anchors: HU-1.1..HU-1.5 specs (extracted by structural parsing of the markdown).
HU1_ANCHORS = [
    {
        "ref_id": "HU-1.1",
        "marker": "CANONICAL",
        "hero_cards": "AhKs",
        "board_flop": "Ad8c3h",
        "street": "flop",
        "hero_pos": "BTN",
        "villain_pos": "BB",
        "pot_bb": 5.5,
        "facing_bet": False,
        "to_call_bb": 0,
        "effective_stack_bb": 100,
        "opener": "BTN",
        "bettor": None,
        "composition": "TP+ (TPTK on dry A-high)",
        "axis": "value-bet on dry A-high range-c-bet",
        "action_summary": "BTN opens 2.5bb, BB calls. Flop Ad8c3h rainbow. BB checks. Hero acts.",
    },
    {
        "ref_id": "HU-1.2",
        "marker": "CANONICAL",
        "hero_cards": "9d9c",
        "board_flop": "9h7s2c",
        "board_turn": "9h7s2c4d",
        "board_river": "9h7s2c4dJh",
        "street": "river",
        "hero_pos": "BTN",
        "villain_pos": "BB",
        "pot_bb": 30,
        "facing_bet": False,
        "to_call_bb": 0,
        "effective_stack_bb": 100,
        "opener": "BTN",
        "bettor": None,
        "composition": "TP+ (set of nines; thin-value river)",
        "axis": "thin-value river bet on safe runout",
        "action_summary": "BTN opens 2.5bb, BB calls. Flop 9h7s2c BB-checks-BTN-bets-25%-BB-calls. Turn 4d BB-checks-BTN-bets-25%-BB-calls. River Jh. BB checks. Hero acts.",
    },
    {
        "ref_id": "HU-1.3",
        "marker": "CLOSE",
        "hero_cards": "KhQd",
        "board_flop": "KcTc6d",
        "street": "flop",
        "hero_pos": "BTN",
        "villain_pos": "BB",
        "pot_bb": 5.5,
        "facing_bet": False,
        "to_call_bb": 0,
        "effective_stack_bb": 100,
        "opener": "BTN",
        "bettor": None,
        "composition": "TP+ (TPGK on wet two-tone draw-heavy)",
        "axis": "value-bet sizing on draw-heavy texture",
        "action_summary": "BTN opens 2.5bb, BB calls. Flop KcTc6d two-tone draw-heavy. BB checks. Hero acts.",
    },
    {
        "ref_id": "HU-1.4",
        "marker": "CLOSE",
        "hero_cards": "TsTd",
        "board_flop": "8h5c2d",
        "board_turn": "8h5c2dTc",
        "street": "turn",
        "hero_pos": "SB",
        "villain_pos": "BB",
        "pot_bb": 12,
        "facing_bet": True,
        "to_call_bb": 4,
        "effective_stack_bb": 60,
        "opener": "SB",
        "bettor": "BB",
        "composition": "TP+ (set of tens; turned set on rainbow)",
        "axis": "set vs IP probe; raise-vs-call EV split at compressed SPR",
        "action_summary": "SB opens 3bb, BB calls. Flop 8h5c2d. SB checks, BB checks. Turn Tc rainbow no FD. SB checks, BB bets 4bb (33% pot). Hero acts.",
    },
    {
        "ref_id": "HU-1.5",
        "marker": "CLOSE",
        "hero_cards": "AhJh",
        "board_flop": "Jc9c5d",
        "board_turn": "Jc9c5d2s",
        "board_river": "Jc9c5d2sQd",
        "street": "river",
        "hero_pos": "BB",
        "villain_pos": "BTN",
        "pot_bb": 50,
        "facing_bet": True,
        "to_call_bb": 37.5,
        "effective_stack_bb": 150,
        "opener": "BTN",
        "bettor": "BTN",
        "composition": "TP+ (TPGK with A-blocker; bluff-catch threshold)",
        "axis": "polarised 75% river bluff-catch with blocker",
        "action_summary": "BTN opens 2.5bb, BB calls. Flop Jc9c5d two-tone. BB-checks-BTN-bets-25%-BB-calls. Turn 2s brick. BB-checks-BTN-bets-33%-BB-calls. River Qd. BTN bets 37.5bb (75% pot). Hero acts.",
    },
]

EFFECTIVE_STACK_VARIATIONS = [60, 100, 150]
EFFECTIVE_STACK_VARIATIONS_FULL = [40, 60, 80, 100, 125, 150, 200, 300]
RANK_ORDER = "23456789TJQKA"


def _cards_in(cards_str: str) -> List[str]:
    """Parse 'AhKs' or 'AhKsJc' into ['Ah', 'Ks', ...]."""
    s = cards_str.replace(" ", "").strip()
    return [s[i:i + 2] for i in range(0, len(s), 2)]


def _all_used_cards(anchor: Dict) -> List[str]:
    """Return all cards already present in the anchor (hero + full board)."""
    used = list(_cards_in(anchor["hero_cards"]))
    used += _cards_in(anchor["board_flop"])
    if anchor.get("board_turn"):
        used += [anchor["board_turn"][-2:]]
    if anchor.get("board_river"):
        used += [anchor["board_river"][-2:]]
    return used


def _lowest_rank_idx(board_str: str) -> int:
    """Return the index (0-based, 2-char chunks) of the lowest-rank card on a board."""
    cards = _cards_in(board_str)
    return min(range(len(cards)), key=lambda i: RANK_ORDER.index(cards[i][0]))


def _replace_card_at_index(board_str: str, idx: int, new_card: str) -> str:
    """Replace the 2-char card at chunk index idx in board_str."""
    cards = _cards_in(board_str)
    cards[idx] = new_card
    return "".join(cards)


def _replace_last_card(board_str: str, new_card: str) -> str:
    """Replace the trailing 2-char card in board_str."""
    return board_str[:-2] + new_card


def _candidate_bricks(used_cards: List[str], n: int, suit_pref: Optional[str] = None,
                      max_rank: str = "T") -> List[str]:
    """Pick up to n distinct cards not in used_cards. Prefers the suit_pref suit if provided
    (to preserve flush-draw structure for board-runout variations on draw-heavy textures).
    Restricts to ranks 2..max_rank to keep "brick" semantics."""
    candidates: List[str] = []
    rank_window = RANK_ORDER[:RANK_ORDER.index(max_rank) + 1]
    suits_ordered = ([suit_pref] + [s for s in "cdhs" if s != suit_pref]) if suit_pref else list("cdhs")
    for s in suits_ordered:
        for r in rank_window:
            cand = f"{r}{s}"
            if cand in used_cards or cand in candidates:
                continue
            candidates.append(cand)
            if len(candidates) >= n:
                return candidates
    return candidates


def _generate_board_runout_variations(anchor: Dict, n: int = 5) -> List[Dict]:
    """Generate n board-runout variations that ACTUALLY mutate the relevant board field.

    For flop spots: replace the lowest-rank flop card with a same-suit, lower-rank brick
                    (preserves draw structure on draw-heavy textures; preserves rainbow/paint).
    For turn spots: replace the turn brick (last card of board_turn) with a non-conflicting brick.
    For river spots: replace the river brick (last card of board_river) with a non-conflicting brick.

    Returns variation dicts with board fields actually updated (variation_param prose matches).
    """
    used = _all_used_cards(anchor)
    variations: List[Dict] = []

    if anchor["street"] == "flop":
        brick_idx = _lowest_rank_idx(anchor["board_flop"])
        old_brick = _cards_in(anchor["board_flop"])[brick_idx]
        # Suit-preserving: pick same-suit cards of different rank (preserves flush-draw structure)
        # Used set includes the old brick itself; new bricks must differ.
        candidates = _candidate_bricks(used + [old_brick], n=n, suit_pref=old_brick[1], max_rank="T")
        # If suit-preserving doesn't yield enough, allow off-suit (texture may shift; labelers will judge)
        if len(candidates) < n:
            candidates += _candidate_bricks(used + [old_brick] + candidates, n=n - len(candidates), max_rank="T")
        for i in range(n):
            new_card = candidates[i % len(candidates)] if candidates else None
            if new_card is None:
                raise RuntimeError(f"No candidate bricks for {anchor['ref_id']} flop variation")
            var = dict(anchor)
            var["board_flop"] = _replace_card_at_index(anchor["board_flop"], brick_idx, new_card)
            var["variation_axis"] = "board_runout"
            var["variation_param"] = f"replaced flop brick: {old_brick} -> {new_card}"
            var["lookalike_brick"] = new_card
            variations.append(var)
        return variations

    if anchor["street"] == "turn":
        old_brick = anchor["board_turn"][-2:]
        # No suit constraint required for turn brick (flop-fixed structure already established)
        candidates = _candidate_bricks(used + [old_brick], n=n, suit_pref=None, max_rank="T")
        for i in range(n):
            new_card = candidates[i % len(candidates)] if candidates else None
            if new_card is None:
                raise RuntimeError(f"No candidate bricks for {anchor['ref_id']} turn variation")
            var = dict(anchor)
            var["board_turn"] = _replace_last_card(anchor["board_turn"], new_card)
            var["variation_axis"] = "board_runout"
            var["variation_param"] = f"replaced turn brick: {old_brick} -> {new_card}"
            var["lookalike_brick"] = new_card
            variations.append(var)
        return variations

    if anchor["street"] == "river":
        old_brick = anchor["board_river"][-2:]
        candidates = _candidate_bricks(used + [old_brick], n=n, suit_pref=None, max_rank="T")
        for i in range(n):
            new_card = candidates[i % len(candidates)] if candidates else None
            if new_card is None:
                raise RuntimeError(f"No candidate bricks for {anchor['ref_id']} river variation")
            var = dict(anchor)
            var["board_river"] = _replace_last_card(anchor["board_river"], new_card)
            var["variation_axis"] = "board_runout"
            var["variation_param"] = f"replaced river brick: {old_brick} -> {new_card}"
            var["lookalike_brick"] = new_card
            variations.append(var)
        return variations

    raise ValueError(f"Unknown street '{anchor['street']}' for anchor {anchor['ref_id']}")


def _generate_variations(anchor: Dict, n_per_anchor: int = 10, seed: int = 0,
                         n_runout: int = 5, n_stack: int = 3, n_action: int = 2,
                         stack_pool: Optional[List[int]] = None) -> List[Dict]:
    """Generate n_per_anchor variations of an anchor spot.

    Strategy (deterministic):
    - n_runout board-runout variations (board fields actually mutated per variation_param semantics)
    - n_stack effective-stack variations (drawn from stack_pool; nudged if equal to anchor)
    - n_action villain action-size variations (bet-size multipliers if facing bet; sequence variants otherwise)

    Default n_per_anchor=10 keeps PILOT V2 backwards-compat. For Phase 1.5-D.3 FULL,
    n_runout=10/n_stack=8/n_action=11 produces ~29 variations per anchor (24 anchors × 29 = 696 ≈ 700).
    """
    if stack_pool is None:
        stack_pool = EFFECTIVE_STACK_VARIATIONS

    variations: List[Dict] = []

    # Board-runout variations
    runouts = _generate_board_runout_variations(anchor, n=n_runout)
    for i, var in enumerate(runouts):
        var["spot_id"] = f"{anchor['ref_id']}-LK-{i + 1:02d}"
        var["anchor_id"] = anchor["ref_id"]
        variations.append(var)

    # Effective-stack variations
    stack_idx_offset = n_runout + 1
    stacks_chosen: List[int] = []
    for stack in stack_pool:
        if stack == anchor["effective_stack_bb"]:
            stack += 5
        if stack in stacks_chosen:
            continue
        stacks_chosen.append(stack)
        if len(stacks_chosen) >= n_stack:
            break
    for j, stack in enumerate(stacks_chosen):
        var = dict(anchor)
        var["spot_id"] = f"{anchor['ref_id']}-LK-{stack_idx_offset + j:02d}"
        var["anchor_id"] = anchor["ref_id"]
        var["variation_axis"] = "effective_stack"
        var["variation_param"] = f"effective_stack_bb={stack}"
        var["effective_stack_bb"] = stack
        variations.append(var)

    # Villain-action variations
    action_idx_offset = stack_idx_offset + len(stacks_chosen)
    if anchor.get("facing_bet") and anchor.get("to_call_bb", 0) > 0:
        # Bet-sizing variations: multipliers spanning small probe to large overbet
        # Mirrors solver-aligned sizing tiers (25/33/50/66/75/100/125/150% etc.)
        sizing_multipliers = [0.5, 0.66, 0.75, 0.9, 1.1, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0]
        for k in range(min(n_action, len(sizing_multipliers))):
            mult = sizing_multipliers[k]
            new_to_call = round(anchor["to_call_bb"] * mult, 1)
            if new_to_call <= 0:
                continue
            var = dict(anchor)
            var["spot_id"] = f"{anchor['ref_id']}-LK-{action_idx_offset + k:02d}"
            var["anchor_id"] = anchor["ref_id"]
            var["variation_axis"] = "villain_bet_sizing"
            var["variation_param"] = f"to_call_bb={new_to_call} (was {anchor['to_call_bb']}; mult={mult}x)"
            var["to_call_bb"] = new_to_call
            variations.append(var)
    else:
        # Action-sequence variations: alternate opener/limp/3bet/check-back patterns
        sequence_variants = [
            ("opener_alt", f"opener_alt={anchor['villain_pos']}_open_3bet"),
            ("limp_iso", "limp-then-iso line"),
            ("checkback", "PFA flop check-back leading to delayed action"),
            ("3bet_call", "preflop 3bet-call dynamic; pot inflated"),
            ("4bet_call", "preflop 4bet-call dynamic; deep SPR"),
            ("limp_check", "limped-pot multistreet check-flow"),
            ("openraise_squeeze", "openraise vs squeeze-call dynamic"),
            ("turn_donk", "OOP turn-donk leading to adjusted ranges"),
            ("flop_xr", "flop check-raise dynamic in opponent range"),
            ("turn_xr", "turn check-raise dynamic in opponent range"),
            ("river_donk", "OOP river-donk leading sequence"),
        ]
        for k in range(min(n_action, len(sequence_variants))):
            tag, desc = sequence_variants[k]
            var = dict(anchor)
            var["spot_id"] = f"{anchor['ref_id']}-LK-{action_idx_offset + k:02d}"
            var["anchor_id"] = anchor["ref_id"]
            var["variation_axis"] = "villain_action_sequence"
            var["variation_param"] = f"{tag}: {desc}"
            variations.append(var)

    return variations[:n_per_anchor]


def _assert_variation_param_matches_board_state(var: Dict, anchor: Dict) -> None:
    """Generator-side invariant per dispatch §"Binding spec" item 1d.

    For each output row, EITHER:
    (a) variation_param describes a non-board mutation (effective_stack / to_call_bb / opener)
        AND board fields equal anchor's board fields, OR
    (b) variation_param describes a board mutation
        AND at least one board field differs from anchor's board fields.

    Raises AssertionError on violation.
    """
    is_board_mutation = (
        var["variation_axis"] == "board_runout"
        or var["variation_param"].startswith("replaced")
    )
    board_differs = (
        var.get("board_flop") != anchor.get("board_flop")
        or var.get("board_turn") != anchor.get("board_turn")
        or var.get("board_river") != anchor.get("board_river")
    )
    if is_board_mutation and not board_differs:
        raise AssertionError(
            f"BUG (was the v1 issue): {var['spot_id']} variation_param='{var['variation_param']}' "
            f"describes a board mutation but no board field differs from anchor {anchor['ref_id']}"
        )
    if (not is_board_mutation) and board_differs:
        raise AssertionError(
            f"INCONSISTENCY: {var['spot_id']} variation_param='{var['variation_param']}' "
            f"describes a non-board mutation but board fields differ from anchor {anchor['ref_id']}"
        )


def main() -> int:
    if not os.path.exists(PILOT_DIR):
        os.makedirs(PILOT_DIR)
    print(f"Reading HU-1 anchors (5 spots from {HU_AXIS_1_SPEC})", file=sys.stderr)
    print(f"Generating ~10 variations per anchor = ~50 lookalikes for pilot v2 (board-mutating)", file=sys.stderr)

    all_variations: List[Dict] = []
    audit_rows: List[Dict] = []
    for anchor in HU1_ANCHORS:
        vars_for_anchor = _generate_variations(anchor, n_per_anchor=10, seed=42)
        for v in vars_for_anchor:
            _assert_variation_param_matches_board_state(v, anchor)
            all_variations.append(v)
            audit_rows.append({
                "spot_id": v["spot_id"],
                "anchor_id": v["anchor_id"],
                "variation_axis": v["variation_axis"],
                "variation_param": v["variation_param"],
                "axis_of_targeting": anchor["axis"],
                "composition": anchor["composition"],
                "structural_similarity": "anchor-preserving (composition class + axis match; board mutated where variation_axis=board_runout)",
                "board_flop_anchor": anchor.get("board_flop"),
                "board_flop_lookalike": v.get("board_flop"),
                "board_turn_anchor": anchor.get("board_turn"),
                "board_turn_lookalike": v.get("board_turn"),
                "board_river_anchor": anchor.get("board_river"),
                "board_river_lookalike": v.get("board_river"),
                "v9_3way_uncertainty_score": None,
                "v9_3way_uncertainty_threshold": None,
                "v9_3way_uncertainty_within_band": None,
                "deferred": "v9-3way model uncertainty scoring deferred per architect-hat consult; structural similarity used as filter",
            })

    sit_path = os.path.join(PILOT_DIR, "situations.jsonl")
    with open(sit_path, "w") as f:
        for v in all_variations:
            f.write(json.dumps(v) + "\n")
    print(f"Wrote {sit_path} ({len(all_variations)} situations)", file=sys.stderr)

    audit_path = os.path.join(PILOT_DIR, "similarity_distance_audit.jsonl")
    with open(audit_path, "w") as f:
        for row in audit_rows:
            f.write(json.dumps(row) + "\n")
    print(f"Wrote {audit_path} ({len(audit_rows)} rows)", file=sys.stderr)
    return 0


def main_full() -> int:
    """Phase 1.5-D.3 FULL generator: 24 HU-2..HU-6 anchors × ~29 variations = ~696 lookalikes.

    Per dispatch MAIN_TERMINAL_HU14_ADJUDICATION_AND_PHASE15D3_FULL_DISPATCH_2026-05-10.md §(b):
    - Anchors: HU-2..HU-6 (5 axes × 5 anchors each = 25 minus HU-6.5 = 24)
    - Target: ~700 lookalikes; 24 × 29 = 696 ≈ 700
    - Per-anchor: 10 board-runout + 8 stack + 11 villain-action = 29

    Architect-hat §(c.3) decision: PATH (b) — composition + action_summary fields are kept
    AS-IS from anchor for board_runout variations (NOT mutated alongside boards). Pilot V2 evidence
    (PR #344) demonstrated labellers correctly read structured board fields and ignored stale prose.
    Generator-correctness gap acknowledged; documented in BUILDER_REPORT_PHASE15D3_FULL.

    Architect-hat §(c.1) sanitization + §(c.2) throttle-aware batching are LABELLING-pipeline
    infrastructure (separate from generation) and are required before labelling fires.
    """
    if not os.path.exists(FULL_DIR):
        os.makedirs(FULL_DIR)
    print(f"Reading HU-2..HU-6 anchors (24 spots, HU-6.5 excluded)", file=sys.stderr)
    print(f"Generating ~29 variations per anchor = ~696 lookalikes for Phase 1.5-D.3 FULL", file=sys.stderr)

    all_variations: List[Dict] = []
    audit_rows: List[Dict] = []
    for anchor in ALL_HU2_HU6_ANCHORS:
        vars_for_anchor = _generate_variations(
            anchor,
            n_per_anchor=29,
            seed=42,
            n_runout=10,
            n_stack=8,
            n_action=11,
            stack_pool=EFFECTIVE_STACK_VARIATIONS_FULL,
        )
        for v in vars_for_anchor:
            _assert_variation_param_matches_board_state(v, anchor)
            all_variations.append(v)
            audit_rows.append({
                "spot_id": v["spot_id"],
                "anchor_id": v["anchor_id"],
                "variation_axis": v["variation_axis"],
                "variation_param": v["variation_param"],
                "axis_of_targeting": anchor["axis"],
                "composition": anchor["composition"],
                "structural_similarity": "anchor-preserving (composition class + axis match; board mutated where variation_axis=board_runout)",
                "board_flop_anchor": anchor.get("board_flop"),
                "board_flop_lookalike": v.get("board_flop"),
                "board_turn_anchor": anchor.get("board_turn"),
                "board_turn_lookalike": v.get("board_turn"),
                "board_river_anchor": anchor.get("board_river"),
                "board_river_lookalike": v.get("board_river"),
                "v9_3way_uncertainty_score": None,
                "v9_3way_uncertainty_threshold": None,
                "v9_3way_uncertainty_within_band": None,
                "deferred": "v9-3way model uncertainty scoring deferred per architect-hat consult; structural similarity used as filter",
            })

    sit_path = os.path.join(FULL_DIR, "situations.jsonl")
    with open(sit_path, "w") as f:
        for v in all_variations:
            f.write(json.dumps(v) + "\n")
    print(f"Wrote {sit_path} ({len(all_variations)} situations)", file=sys.stderr)

    audit_path = os.path.join(FULL_DIR, "similarity_distance_audit.jsonl")
    with open(audit_path, "w") as f:
        for row in audit_rows:
            f.write(json.dumps(row) + "\n")
    print(f"Wrote {audit_path} ({len(audit_rows)} rows)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "pilot_v2"
    if mode == "full":
        sys.exit(main_full())
    elif mode == "pilot_v2":
        sys.exit(main())
    else:
        print(f"Unknown mode: {mode}. Use 'pilot_v2' (default) or 'full'.", file=sys.stderr)
        sys.exit(2)
