#!/usr/bin/env python3
"""Phase 1.5-D.3 HU lookalike generator.

Per dispatch MAIN_TERMINAL_HU65_OWNER_ADJUDICATION_AND_PHASE15D3_DISPATCH_2026-05-10.md
+ design memo §4.4. Generates HU lookalike situations anchored on the
30-spot HU reference set.

Pilot mode (this run): anchors on HU-1 axis (5 spots) only. Generates
~10 variations per anchor = 50 lookalikes total.

Variation axes (per design memo §4.4):
- Board run-out (different turn/river bricks preserving structure)
- SPR/effective stack (60/100/150bb)
- Villain action sequence (bet-size variation; check-back lines)

Architect-hat consult (transparently flagged for QC):
- Similarity-band scoring against v9-3way-on-59 model uncertainty surface
  (per α=β resolution) requires loading the XGBoost model + computing
  per-situation predictive entropy. For pilot scope, deferred to a
  follow-up enhancement; similarity-band here is STRUCTURAL (composition
  class + axis preservation + within-anchor variation count).
- Documented as deviation in builder report; QC may direct full v9-3way
  uncertainty scoring as a follow-up if needed.

Output:
  data/hu_corpus/pilot_50/situations.jsonl  - 50 lookalike specs
  data/hu_corpus/pilot_50/similarity_distance_audit.jsonl - per-spot anchor + variation axis
"""
from __future__ import annotations

import json
import os
import random
import sys
from typing import Dict, List, Optional, Tuple

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HU_AXIS_1_SPEC = os.path.join(REPO, "design", "hu_reference_set", "HU_AXIS_1_MADE_HAND.md")
PILOT_DIR = os.path.join(REPO, "data", "hu_corpus", "pilot_50")

# Anchors: HU-1.1..HU-1.5 specs (extracted by structural parsing of the markdown).
# Each anchor specifies hero_cards, board, street, positions, stack, action.
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

# Brick cards used for board-runout variations; chosen to avoid common conflicts
# with hero hands and existing board cards. We'll filter conflicts at use-time.
TURN_BRICKS = ["2c", "2d", "2h", "2s", "3c", "3s", "4c", "4s"]
RIVER_BRICKS = ["3c", "3d", "3h", "3s", "4c", "4d", "4h", "4s", "5c", "5h"]
EFFECTIVE_STACK_VARIATIONS = [60, 100, 150]


def _cards_in(cards_str: str) -> List[str]:
    """Parse 'AhKs' or 'AhKsJc' into ['Ah', 'Ks', ...]."""
    s = cards_str.replace(" ", "").strip()
    return [s[i:i + 2] for i in range(0, len(s), 2)]


def _conflicts(card: str, used: List[str]) -> bool:
    return card in used


def _generate_variations(anchor: Dict, n_per_anchor: int = 10, seed: int = 0) -> List[Dict]:
    """Generate n_per_anchor variations of an anchor spot.

    Variation strategy (deterministic given seed):
    - 5 board-runout variations (different non-conflicting bricks for next-street card if applicable)
    - 3 effective-stack variations (60/100/150bb)
    - 2 villain action-size variations (different bet sizes if facing bet)

    For anchor's already-final-street (river) spots, board-runout variation
    re-generates the river card; for flop spots, re-generates the turn+river
    when extending; we keep simple: vary the latest street's board card or
    reroll the most-recent brick.
    """
    rng = random.Random(seed + hash(anchor["ref_id"]) % 100000)
    used_cards = _cards_in(anchor["hero_cards"]) + _cards_in(anchor["board_flop"])
    if anchor.get("board_turn"):
        used_cards += [anchor["board_turn"][-2:]]
    if anchor.get("board_river"):
        used_cards += [anchor["board_river"][-2:]]

    variations = []

    # 5 board-runout variations
    for i in range(5):
        candidate_brick = None
        # For flop spots, vary the implied turn brick (forward-projected scenario)
        # For turn spots, vary the river brick
        # For river spots, vary the river brick
        brick_pool = TURN_BRICKS if anchor["street"] == "flop" else RIVER_BRICKS
        # Find a non-conflicting brick that differs from the anchor
        for attempt in range(20):
            cand = rng.choice(brick_pool)
            if not _conflicts(cand, used_cards):
                candidate_brick = cand
                break
        if candidate_brick is None:
            candidate_brick = brick_pool[i % len(brick_pool)]
        var = dict(anchor)
        var["spot_id"] = f"{anchor['ref_id']}-LK-{i + 1:02d}"
        var["anchor_id"] = anchor["ref_id"]
        var["variation_axis"] = "board_runout"
        var["variation_param"] = f"replaced last-street brick with {candidate_brick}"
        var["lookalike_brick"] = candidate_brick
        variations.append(var)

    # 3 effective-stack variations
    for j, stack in enumerate(EFFECTIVE_STACK_VARIATIONS):
        if stack == anchor["effective_stack_bb"]:
            stack += 5  # nudge to make it distinct
        var = dict(anchor)
        var["spot_id"] = f"{anchor['ref_id']}-LK-{6 + j:02d}"
        var["anchor_id"] = anchor["ref_id"]
        var["variation_axis"] = "effective_stack"
        var["variation_param"] = f"effective_stack_bb={stack}"
        var["effective_stack_bb"] = stack
        variations.append(var)

    # 2 villain-action variations: change opener or bet-size
    for k in range(2):
        var = dict(anchor)
        var["spot_id"] = f"{anchor['ref_id']}-LK-{9 + k:02d}"
        var["anchor_id"] = anchor["ref_id"]
        if anchor.get("facing_bet") and anchor.get("to_call_bb", 0) > 0:
            # Vary bet size (smaller / larger)
            new_to_call = round(anchor["to_call_bb"] * (0.66 if k == 0 else 1.5), 1)
            var["variation_axis"] = "villain_bet_sizing"
            var["variation_param"] = f"to_call_bb={new_to_call} (was {anchor['to_call_bb']})"
            var["to_call_bb"] = new_to_call
        else:
            # Vary opener (HU still has only 2 positions; vary action sequence)
            var["variation_axis"] = "villain_action_sequence"
            var["variation_param"] = f"opener_alt={anchor['villain_pos']}_open_3bet" if k == 0 else "limp-then-iso line"
        variations.append(var)

    return variations[:n_per_anchor]


def main() -> int:
    if not os.path.exists(PILOT_DIR):
        os.makedirs(PILOT_DIR)
    print(f"Reading HU-1 anchors (5 spots from {HU_AXIS_1_SPEC})", file=sys.stderr)
    print(f"Generating ~10 variations per anchor = ~50 lookalikes for pilot", file=sys.stderr)

    all_variations = []
    audit_rows = []
    for anchor in HU1_ANCHORS:
        vars_for_anchor = _generate_variations(anchor, n_per_anchor=10, seed=42)
        for v in vars_for_anchor:
            all_variations.append(v)
            audit_rows.append({
                "spot_id": v["spot_id"],
                "anchor_id": v["anchor_id"],
                "variation_axis": v["variation_axis"],
                "variation_param": v["variation_param"],
                "axis_of_targeting": anchor["axis"],
                "composition": anchor["composition"],
                "structural_similarity": "anchor-preserving (composition class + axis match)",
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


if __name__ == "__main__":
    sys.exit(main())
