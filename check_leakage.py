"""
Leakage / duplication check: batch2 situations vs existing 348 training rows.

Definitions
-----------
DIRECT DUPLICATE : same (hero_cards_sorted, board_sorted, hero_position, street)
BOARD OVERLAP    : same (board_sorted, hero_position, street), different hero_cards
NEAR MATCH       : Euclidean distance < 0.1 on min-max-normalised numerical features

Read-only — writes nothing to training-data/.
"""

import json
import re
import math
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE           = Path("/home/rupertbeytell/river-rats-v2/training-data")
BATCH2_PATH    = BASE / "factory_batch2_situations.jsonl"
EXISTING_JSONL = BASE / "3way_combined_350.jsonl"

# ---------------------------------------------------------------------------
# Card normalisation helpers
# ---------------------------------------------------------------------------

def norm_cards(card_str: str) -> frozenset:
    """Return a frozenset of card tokens from a 2-card string like 'AsQs'."""
    tokens = re.findall(r'[2-9TJQKAtjqka][shdcSHDC]', card_str)
    return frozenset(t[0].upper() + t[1].lower() for t in tokens)

def norm_board_list(board_list) -> tuple:
    """Normalise a list of card strings to a sorted tuple."""
    cards = []
    for c in board_list:
        tokens = re.findall(r'[2-9TJQKAtjqka][shdcSHDC]', c.strip())
        cards.extend(t[0].upper() + t[1].lower() for t in tokens)
    return tuple(sorted(cards))

def norm_board_str(board_str: str) -> tuple:
    """Normalise a concatenated board string like '8c6c6d4c8s'."""
    tokens = re.findall(r'[2-9TJQKAtjqka][shdcSHDC]', board_str.strip())
    return tuple(sorted(t[0].upper() + t[1].lower() for t in tokens))

# Street name → integer mapping
STREET_NAME_TO_INT = {
    "flop": 0, "turn": 1, "river": 2,
    "f": 0, "t": 1, "r": 2,
}

# Position name → integer mapping
POS_NAME_TO_INT = {
    "UTG": 0, "HJ": 1, "CO": 2, "BTN": 3, "SB": 4, "BB": 5,
    "utg": 0, "hj": 1, "co": 2, "btn": 3, "sb": 4, "bb": 5,
}

def pos_to_int(p):
    if isinstance(p, int):
        return p
    return POS_NAME_TO_INT.get(str(p).strip(), -1)

def street_to_int(s):
    if isinstance(s, int):
        return s
    return STREET_NAME_TO_INT.get(str(s).strip().lower(), -1)

# ---------------------------------------------------------------------------
# Feature columns used for near-match distance check
# (shared between the feat_dict in JSONL and top-level fields in batch2)
# ---------------------------------------------------------------------------
NUMERICAL_FEATURES = [
    "street", "facing_bet", "pot_size", "to_call", "pot_odds", "bet_to_pot",
    "hero_position", "villain_position", "is_ip",
    "hand_category", "hand_rank",
    "is_made_hand", "is_strong_made", "is_monster",
    "has_flush_draw", "has_straight_draw", "draw_outs",
    "is_monotone", "is_two_tone", "is_rainbow",
    "is_paired", "is_double_paired",
    "connectivity_score", "high_card_rank",
    "danger_score", "flush_danger", "straight_danger",
    "raw_equity", "equity_vs_range",
    "better_hand_pct", "worse_hand_pct", "equity_margin",
    "spr", "is_3bet_pot",
    "villain_aggression_count", "villain_checked_back", "villain_call_count",
    "num_opponents",
    "villain_top_pair_plus_pct", "villain_draw_pct", "villain_air_pct",
    "villain_range_capped", "board_favour",
    "num_callers_to_bet", "facing_raise",
]

# ---------------------------------------------------------------------------
# Load batch2
# ---------------------------------------------------------------------------

def load_batch2(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            hero_cards   = norm_cards(d["_hero_cards"])
            board        = norm_board_list(d["_board_cards"])
            hero_pos     = d["hero_position"]   # already int
            street       = d["street"]          # already int
            situation_id = d.get("_situation_id", "?")
            feat_vec = []
            for k in NUMERICAL_FEATURES:
                try:
                    feat_vec.append(float(d[k]))
                except (KeyError, TypeError, ValueError):
                    feat_vec.append(float("nan"))
            rows.append({
                "hero_cards":      hero_cards,
                "hero_cards_raw":  d.get("_hero_cards", ""),
                "board":           board,
                "hero_pos":        hero_pos,
                "street":          street,
                "id":              situation_id,
                "feat":            feat_vec,
            })
    return rows

# ---------------------------------------------------------------------------
# Load existing labelled data from JSONL
# ---------------------------------------------------------------------------

def load_existing_jsonl(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            hero_cards   = norm_cards(d["hero_cards"])
            raw_board    = d["board"]
            if isinstance(raw_board, list):
                board = norm_board_list(raw_board)
            else:
                board = norm_board_str(raw_board)
            hero_pos     = pos_to_int(d["hero_position"])
            street       = street_to_int(d["street"])
            situation_id = d.get("situation_id", "?")
            fd = d.get("feat_dict", {})
            feat_vec = []
            for k in NUMERICAL_FEATURES:
                try:
                    feat_vec.append(float(fd[k]))
                except (KeyError, TypeError, ValueError):
                    feat_vec.append(float("nan"))
            rows.append({
                "hero_cards":      hero_cards,
                "hero_cards_raw":  d.get("hero_cards", ""),
                "board":           board,
                "board_raw":       d.get("board", ""),
                "hero_pos":        hero_pos,
                "street":          street,
                "id":              situation_id,
                "feat":            feat_vec,
            })
    return rows

# ---------------------------------------------------------------------------
# Min-max normalise feature matrix (all rows pooled)
# ---------------------------------------------------------------------------

def normalise_features(all_vecs):
    n_cols = len(NUMERICAL_FEATURES)
    mins = [float("inf")]  * n_cols
    maxs = [float("-inf")] * n_cols
    for vec in all_vecs:
        for j, v in enumerate(vec):
            if not math.isnan(v):
                if v < mins[j]: mins[j] = v
                if v > maxs[j]: maxs[j] = v
    normed = []
    for vec in all_vecs:
        nv = []
        for j, v in enumerate(vec):
            lo, hi = mins[j], maxs[j]
            if math.isnan(v) or lo == hi or lo == float("inf"):
                nv.append(0.0)
            else:
                nv.append((v - lo) / (hi - lo))
        normed.append(nv)
    return normed

def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Loading files...")
    batch2   = load_batch2(BATCH2_PATH)
    existing = load_existing_jsonl(EXISTING_JSONL)

    print(f"  Batch2 situations : {len(batch2)}")
    print(f"  Existing (JSONL)  : {len(existing)}")
    print()

    # -----------------------------------------------------------------------
    # 1. Build lookup for existing rows
    # -----------------------------------------------------------------------
    exact_key_map = defaultdict(list)   # (hero_cards, board, pos, street) → rows
    board_key_map = defaultdict(list)   # (board, pos, street) → rows

    for row in existing:
        ek = (row["hero_cards"], row["board"], row["hero_pos"], row["street"])
        bk = (row["board"], row["hero_pos"], row["street"])
        exact_key_map[ek].append(row)
        board_key_map[bk].append(row)

    # -----------------------------------------------------------------------
    # 2. Compare batch2 against existing
    # -----------------------------------------------------------------------
    direct_duplicates = []
    board_overlaps    = []

    for b2 in batch2:
        ek = (b2["hero_cards"], b2["board"], b2["hero_pos"], b2["street"])
        bk = (b2["board"], b2["hero_pos"], b2["street"])

        if ek in exact_key_map:
            for match in exact_key_map[ek]:
                direct_duplicates.append({
                    "batch2_id":      b2["id"],
                    "existing_id":    match["id"],
                    "hero_cards_raw": b2["hero_cards_raw"],
                    "board":          list(b2["board"]),
                    "hero_pos":       b2["hero_pos"],
                    "street":         b2["street"],
                })
        elif bk in board_key_map:
            for match in board_key_map[bk]:
                board_overlaps.append({
                    "batch2_id":       b2["id"],
                    "batch2_cards":    b2["hero_cards_raw"],
                    "existing_id":     match["id"],
                    "existing_cards":  match["hero_cards_raw"],
                    "board":           list(b2["board"]),
                    "hero_pos":        b2["hero_pos"],
                    "street":          b2["street"],
                })

    # -----------------------------------------------------------------------
    # 3. Near-match feature distance check
    # -----------------------------------------------------------------------
    NEAR_THRESHOLD = 0.1

    all_vecs = [r["feat"] for r in batch2] + [r["feat"] for r in existing]
    normed   = normalise_features(all_vecs)

    n_b2      = len(batch2)
    b2_normed = normed[:n_b2]
    ex_normed = normed[n_b2:]

    # Build set of batch2 IDs that are direct duplicates (skip those in near-match)
    dup_ids = {d["batch2_id"] for d in direct_duplicates}

    near_matches = []
    for i, b2 in enumerate(batch2):
        if b2["id"] in dup_ids:
            continue
        for j, ex in enumerate(existing):
            dist = euclidean(b2_normed[i], ex_normed[j])
            if dist < NEAR_THRESHOLD:
                near_matches.append({
                    "batch2_id":        b2["id"],
                    "existing_id":      ex["id"],
                    "distance":         round(dist, 5),
                    "batch2_cards":     b2["hero_cards_raw"],
                    "existing_cards":   ex["hero_cards_raw"],
                    "batch2_board":     list(b2["board"]),
                    "existing_board":   list(ex["board"]),
                    "batch2_street":    b2["street"],
                    "existing_street":  ex["street"],
                    "batch2_pos":       b2["hero_pos"],
                    "existing_pos":     ex["hero_pos"],
                })

    near_matches.sort(key=lambda x: x["distance"])

    # -----------------------------------------------------------------------
    # 4. Batch2 internal duplicates
    # -----------------------------------------------------------------------
    b2_exact_seen = defaultdict(list)
    for b2 in batch2:
        ek = (b2["hero_cards"], b2["board"], b2["hero_pos"], b2["street"])
        b2_exact_seen[ek].append(b2["id"])
    b2_internal_dups = {k: v for k, v in b2_exact_seen.items() if len(v) > 1}

    # -----------------------------------------------------------------------
    # 5. Distribution summary
    # -----------------------------------------------------------------------
    b2_boards = set(b2["board"] for b2 in batch2)
    ex_boards = set(ex["board"] for ex in existing)
    shared_boards = b2_boards & ex_boards

    b2_streets = defaultdict(int)
    ex_streets = defaultdict(int)
    for b2 in batch2:   b2_streets[b2["street"]] += 1
    for ex in existing: ex_streets[ex["street"]] += 1

    street_label = {0: "flop", 1: "turn", 2: "river"}

    # -----------------------------------------------------------------------
    # 6. Report
    # -----------------------------------------------------------------------
    print("=" * 70)
    print("LEAKAGE CHECK RESULTS")
    print("=" * 70)

    # --- Direct duplicates ---
    print(f"\n--- DIRECT DUPLICATES (same hero_cards + board + position + street) ---")
    print(f"Count: {len(direct_duplicates)}")
    for d in direct_duplicates:
        print(f"  Batch2   : {d['batch2_id']}")
        print(f"  Existing : {d['existing_id']}")
        print(f"  Key      : cards={d['hero_cards_raw']}  board={d['board']}  "
              f"pos={d['hero_pos']}  street={street_label.get(d['street'], d['street'])}")
        print()
    if not direct_duplicates:
        print("  NONE — no exact matches found.")

    # --- Board overlaps ---
    print(f"\n--- BOARD OVERLAPS (same board+position+street, different hero_cards) ---")
    print(f"Count: {len(board_overlaps)}")

    # Group by unique board key
    board_overlap_grouped = defaultdict(list)
    for bo in board_overlaps:
        k = (tuple(bo["board"]), bo["hero_pos"], bo["street"])
        board_overlap_grouped[k].append(bo)

    for k, pairs in sorted(board_overlap_grouped.items(), key=lambda x: -len(x[1])):
        board_tuple, pos, st = k
        print(f"\n  Board {list(board_tuple)}  pos={pos}  "
              f"street={street_label.get(st, st)}  "
              f"({len(pairs)} batch2-vs-existing pair(s))")
        for p in pairs[:5]:
            print(f"    batch2={p['batch2_id']} cards={p['batch2_cards']}")
            print(f"    existing={p['existing_id']} cards={p['existing_cards']}")
        if len(pairs) > 5:
            print(f"    ... and {len(pairs)-5} more pairs on this board")

    if not board_overlaps:
        print("  NONE — no training board matches an existing board at same position+street.")

    # --- Batch2 internal duplicates ---
    print(f"\n--- BATCH2 INTERNAL DUPLICATES ---")
    print(f"Count: {len(b2_internal_dups)}")
    for ek, ids in b2_internal_dups.items():
        print(f"  Key={ek}  IDs={ids}")
    if not b2_internal_dups:
        print("  NONE")

    # --- Near matches ---
    print(f"\n--- NEAR-MATCHES (Euclidean distance < {NEAR_THRESHOLD} on normalised features) ---")
    print(f"Count: {len(near_matches)}")
    if near_matches:
        print(f"\nTop 30 closest pairs:")
        for nm in near_matches[:30]:
            print(f"  dist={nm['distance']:.5f}")
            print(f"    batch2   : {nm['batch2_id']}  cards={nm['batch2_cards']}"
                  f"  board={nm['batch2_board']}  pos={nm['batch2_pos']}"
                  f"  street={street_label.get(nm['batch2_street'], nm['batch2_street'])}")
            print(f"    existing : {nm['existing_id']}  cards={nm['existing_cards']}"
                  f"  board={nm['existing_board']}  pos={nm['existing_pos']}"
                  f"  street={street_label.get(nm['existing_street'], nm['existing_street'])}")

        # Histogram of distance buckets
        print(f"\nDistance distribution (all {len(near_matches)} near-matches):")
        buckets = [0] * 10
        for nm in near_matches:
            bucket = min(int(nm["distance"] / 0.01), 9)
            buckets[bucket] += 1
        for i, cnt in enumerate(buckets):
            lo = i * 0.01
            hi = lo + 0.01
            print(f"  [{lo:.2f}, {hi:.2f}) : {cnt}")

    # --- Distribution summary ---
    print(f"\n--- DISTRIBUTION SUMMARY ---")
    print(f"Street breakdown:")
    print(f"  Batch2   : {' | '.join(f'{street_label[s]}={n}' for s,n in sorted(b2_streets.items()))}")
    print(f"  Existing : {' | '.join(f'{street_label[s]}={n}' for s,n in sorted(ex_streets.items()))}")
    print(f"\nUnique boards:")
    print(f"  Batch2   : {len(b2_boards)}")
    print(f"  Existing : {len(ex_boards)}")
    print(f"  Shared   : {len(shared_boards)}")
    if shared_boards:
        print("  Shared board card sets:")
        for b in sorted(shared_boards):
            print(f"    {list(b)}")

    # --- Verdict ---
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    if direct_duplicates:
        print(f"  DIRECT LEAKAGE: {len(direct_duplicates)} situation(s) are exact duplicates.")
        print("  ACTION REQUIRED: remove these from batch2 before training.")
    else:
        print("  No direct leakage found.")

    if board_overlaps:
        unique_boards_affected = len(board_overlap_grouped)
        print(f"  BOARD OVERLAP: {unique_boards_affected} distinct board(s) appear in both datasets.")
        print("  The model will see the same board texture at train time and test time.")
        print("  Severity depends on whether those boards appear in the evaluation gate.")
    else:
        print("  No board overlaps found.")

    if near_matches:
        very_close = [nm for nm in near_matches if nm["distance"] < 0.03]
        print(f"  NEAR MATCHES: {len(near_matches)} pairs within distance 0.10, "
              f"{len(very_close)} within 0.03.")
        print("  Very close pairs (< 0.03) may indicate near-identical situations "
              "despite different cards/boards.")
    else:
        print("  No near-matches found (all pairs > 0.10).")

    print()

if __name__ == "__main__":
    main()
