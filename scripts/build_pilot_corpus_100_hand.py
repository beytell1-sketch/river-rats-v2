#!/usr/bin/env python3
"""Build the Stage 4 pilot 100-hand stratified corpus (Build C).

Per orchestrator directive `MAIN_TERMINAL_PR37_MERGE_ACK_BUILD_C_KICKOFF_2026-04-26.md`:

- 100 hands sampled from `training-data/3way_situations_10k.jsonl`
- Stratified across 5 dimensions:
    1. street (preflop / flop / turn / river)
    2. hero_position (BTN / CO / HJ / BB / SB)
    3. opponent_count (HU / 3-way / 4-way) — encoded num_opponents
    4. board_texture (dry / wet / paired / 3-flush / etc.)
    5. hero_range_placement (premium / value / draw / bluff)
- Disjoint from:
    * Stage 6 50-hand holdout (hash 65cfbf26... over 47652 bytes)
    * v2.3 calibration manifest (28 standard + 10 reversal = 38 hands)
- Hash-locked (SHA256 over the JSONL bytes)

Closes PRE-DISPATCH PREREQUISITES rows #2 + #3.

Output:
    data/pilot_corpus_100_hand_2026-04-26.jsonl
    data/pilot_corpus_100_hand_2026-04-26.lock.json
        (sidecar with hash + stratification report + disjointness report)

Determinism: SEED = 20260426 fixed.
"""
import hashlib
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict
from typing import Iterator

# Determinism. Date-stamped seed; will not change between reruns of this build.
SEED = 20260426
random.seed(SEED)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITUATIONS_PATH = os.path.join(REPO, "training-data", "3way_situations_10k.jsonl")
CALIBRATION_JSON = os.path.join(REPO, "review", "calibration_situations.json")
CALIBRATION_MIRRORS = [
    os.path.join(REPO, "review", "blind_calibration_exam_step7.json"),
    os.path.join(REPO, "review", "calibration_batch_1.json"),
    os.path.join(REPO, "review", "calibration_batch_2.json"),
    os.path.join(REPO, "review", "calibration_batch_3.json"),
]
STAGE6_SPEC = os.path.join(REPO, "review", "comms",
                            "STAGE6_HOLDOUT_TESTSET_v1_0.md")
OUTPUT_JSONL = os.path.join(REPO, "data",
                             "pilot_corpus_100_hand_2026-04-26.jsonl")
OUTPUT_LOCK = os.path.join(REPO, "data",
                            "pilot_corpus_100_hand_2026-04-26.lock.json")

# v2.3 calibration_exam.py constants — names per
# `river-rats-core/calibration_exam.py` v2.3.
GTO_REVERSAL_NEW_ANCHORS = (
    "d8886_BB_flop",
    "d2410_CO_turn",
    "d8963_HJ_turn",
    "d3178_CO_river",
)
GROUP_D_REVERSAL_HANDS = (
    "d3688_BB_flop",
    "d4312_CO_turn",
    "d9556_BB_flop",
    "d2074_BTN_turn",
    "d5466_CO_flop",
)

# ── fingerprint key (matches Stage 6 v1.0 method) ─────────────────


def _fingerprint(hero: str, board: str) -> tuple[str, str]:
    """Stage-6-compatible (sorted(hero), sorted(board)) fingerprint.

    Hero: "AhKd" → sorted card-pair as concatenated string.
    Board: "Ks7h6h" → sorted 3-card / 4-card / 5-card string.
    """
    def _cards(s: str) -> list[str]:
        return [s[i:i + 2] for i in range(0, len(s), 2)]

    return ("".join(sorted(_cards(hero))),
            "".join(sorted(_cards(board))))


# ── load forbidden fingerprints (Stage 6 holdout + v2.3 calibration) ──


def _parse_stage6_holdout_fingerprints(path: str) -> set[tuple[str, str]]:
    """Extract (hero, board) fingerprints from Stage 6 v1.0.3 spec markdown.

    Stage 6 format is:
        - Hero: `Kh Tc`
        - Board (river): `Td 8c 5h 3s 6c`
    Cards are space-separated inside backticks; "Board (street):" has a
    parenthetical street label.
    """
    with open(path) as f:
        text = f.read()
    fingerprints: set[tuple[str, str]] = set()
    blocks = re.split(r"^### HOLDOUT_\d{3}", text, flags=re.MULTILINE)[1:]
    for block in blocks:
        hero_m = re.search(r"^- Hero:\s*`([^`]+)`",
                            block, re.MULTILINE | re.IGNORECASE)
        board_m = re.search(r"^- Board\s*(?:\([^)]*\))?:\s*`([^`]+)`",
                             block, re.MULTILINE | re.IGNORECASE)
        if hero_m and board_m:
            hero = _normalise_cards(hero_m.group(1))
            board = _normalise_cards(board_m.group(1))
            if hero and board:
                fingerprints.add(_fingerprint(hero, board))
    return fingerprints


def _normalise_cards(s: str) -> str:
    """Strip non-card glyphs and convert s/h/d/c suit letters to lowercase."""
    s = re.sub(r"[^AKQJT2-9shdcSHDC]", "", s)
    # Lowercase suit letters but keep rank case as-is (canonicalise A,K,Q,J,T uppercase).
    out = []
    for i in range(0, len(s) - 1, 2):
        rank, suit = s[i].upper(), s[i + 1].lower()
        out.append(rank + suit)
    return "".join(out)


def _parse_calibration_fingerprints() -> set[tuple[str, str]]:
    """Extract (hero, board) fingerprints from calibration_situations.json
    + mirror files. Each entry has a `situation_text` block with
    'Hero cards: ...' / 'Board: ...' lines.
    """
    fingerprints: set[tuple[str, str]] = set()
    paths = [CALIBRATION_JSON] + [p for p in CALIBRATION_MIRRORS
                                    if os.path.exists(p)]
    for p in paths:
        with open(p) as f:
            data = json.load(f)
        for entry in data:
            text = entry.get("situation_text", "")
            hero_m = re.search(r"Hero cards?:\s*([A-Za-z0-9]+)",
                                text, re.IGNORECASE)
            board_m = re.search(r"Board:\s*([A-Za-z0-9]+)",
                                 text, re.IGNORECASE)
            if hero_m and board_m:
                hero = _normalise_cards(hero_m.group(1))
                board = _normalise_cards(board_m.group(1))
                if hero and board:
                    fingerprints.add(_fingerprint(hero, board))
    return fingerprints


def _v23_anchor_fingerprints(situations: list[dict]) -> set[tuple[str, str]]:
    """v2.3 calibration_exam.py adds 4 hard anchors + 5 Group-D reversal
    hands. Look them up by `situation_id` in the source pool.
    """
    fingerprints: set[tuple[str, str]] = set()
    extra_ids = set(GTO_REVERSAL_NEW_ANCHORS) | set(GROUP_D_REVERSAL_HANDS)
    for s in situations:
        if s.get("situation_id") in extra_ids:
            hero = _normalise_cards(s.get("hero_cards", ""))
            board = _normalise_cards(s.get("board", ""))
            if hero and board:
                fingerprints.add(_fingerprint(hero, board))
    return fingerprints


# ── stratification ────────────────────────────────────────────────


def _board_texture(board: str) -> str:
    """Categorise board texture: dry / wet / paired / monotone / two-tone /
    three-flush.

    Heuristic — board parsed as 3+ cards. Returns one canonical bucket;
    composite boards (e.g. paired + monotone) take the most-restrictive.
    """
    cards = [board[i:i + 2] for i in range(0, len(board), 2)]
    if len(cards) < 3:
        return "preflop_or_unknown"
    ranks = [c[0] for c in cards[:3]]  # flop ranks for texture call
    suits = [c[1] for c in cards[:3]]
    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)
    if 3 in rank_counts.values():
        return "trips_board"
    if 2 in rank_counts.values():
        return "paired"
    if 3 in suit_counts.values():
        return "monotone"
    if 2 in suit_counts.values():
        return "two_tone"
    return "rainbow_dry"


def _hero_range_placement(s: dict) -> str:
    """Categorise hero hand strength: premium / value / draw / bluff.

    Uses feat_dict signals for robustness.
    """
    feat = s.get("feat_dict", {})
    if feat.get("is_monster") == 1:
        return "premium"
    if feat.get("is_strong_made") == 1 or feat.get("is_made_hand") == 1:
        return "value"
    if (feat.get("has_flush_draw") == 1 or feat.get("has_straight_draw") == 1
            or feat.get("draw_outs", 0) >= 4):
        return "draw"
    return "bluff"


def _opponent_count_bucket(s: dict) -> str:
    """HU (1 opponent) / 3-way (2 opp) / 4-way+ (3+ opp)."""
    n = s.get("num_opponents", 2)
    if n <= 1:
        return "hu"
    if n == 2:
        return "3way"
    return "4way+"


def _strat_key(s: dict) -> tuple[str, str, str, str, str]:
    """5-D stratification key per directive."""
    return (
        s.get("street", "unknown"),
        s.get("hero_position", "unknown"),
        _opponent_count_bucket(s),
        _board_texture(s.get("board", "")),
        _hero_range_placement(s),
    )


# ── stratified sampling ───────────────────────────────────────────


def _stratified_sample(pool: list[dict], n: int,
                        forbidden: set[tuple[str, str]]) -> list[dict]:
    """Sample n hands stratified across 5 dimensions, disjoint from forbidden.

    Strategy: greedy round-robin across stratum buckets, prioritizing
    least-filled buckets at each step. Each candidate must clear the
    disjointness check. Determinism via SEED.
    """
    # Filter forbidden up front.
    candidates = []
    for s in pool:
        hero = _normalise_cards(s.get("hero_cards", ""))
        board = _normalise_cards(s.get("board", ""))
        if not hero or not board:
            continue
        if _fingerprint(hero, board) in forbidden:
            continue
        candidates.append(s)
    print(f"[strat] {len(candidates)} candidate hands after disjointness filter "
          f"(removed {len(pool) - len(candidates)} from {len(pool)} total)",
          file=sys.stderr)

    # Bucket the candidates.
    buckets: dict[tuple, list[dict]] = defaultdict(list)
    for s in candidates:
        buckets[_strat_key(s)].append(s)
    print(f"[strat] {len(buckets)} unique 5-D stratum buckets observed",
          file=sys.stderr)

    # Shuffle within each bucket for determinism + variety.
    for k in buckets:
        random.shuffle(buckets[k])

    # Round-robin pick: at each step take least-filled non-empty bucket
    # (tie-break by current sample fingerprint diversity, then random).
    selected: list[dict] = []
    selected_fingerprints: set[tuple[str, str]] = set()
    bucket_keys = list(buckets.keys())
    random.shuffle(bucket_keys)
    take_count: dict[tuple, int] = {k: 0 for k in bucket_keys}
    while len(selected) < n:
        # Sort bucket_keys by (take_count asc, then keep current order).
        bucket_keys.sort(key=lambda k: take_count[k])
        progressed = False
        for k in bucket_keys:
            if not buckets[k]:
                continue
            cand = buckets[k].pop()
            fp = _fingerprint(_normalise_cards(cand["hero_cards"]),
                              _normalise_cards(cand["board"]))
            if fp in selected_fingerprints:
                continue  # within-pilot dedup
            selected.append(cand)
            selected_fingerprints.add(fp)
            take_count[k] += 1
            progressed = True
            if len(selected) >= n:
                break
        if not progressed:
            print(f"[strat] WARN: pool exhausted at {len(selected)}/{n}",
                  file=sys.stderr)
            break
    return selected


# ── stratification report ─────────────────────────────────────────


def _stratification_report(selected: list[dict]) -> dict:
    """Report distribution across each of the 5 stratification dims."""
    by_street = Counter(s.get("street") for s in selected)
    by_position = Counter(s.get("hero_position") for s in selected)
    by_opponents = Counter(_opponent_count_bucket(s) for s in selected)
    by_texture = Counter(_board_texture(s.get("board", "")) for s in selected)
    by_placement = Counter(_hero_range_placement(s) for s in selected)
    return {
        "street": dict(by_street),
        "hero_position": dict(by_position),
        "opponent_count_bucket": dict(by_opponents),
        "board_texture": dict(by_texture),
        "hero_range_placement": dict(by_placement),
    }


# ── main ──────────────────────────────────────────────────────────


def main() -> int:
    print(f"[load] reading source pool from {SITUATIONS_PATH}", file=sys.stderr)
    with open(SITUATIONS_PATH) as f:
        pool = [json.loads(line) for line in f if line.strip()]
    print(f"[load] {len(pool)} source candidates loaded", file=sys.stderr)

    # Build forbidden set: Stage 6 holdout + v2.3 calibration.
    print("[disjoint] building forbidden fingerprints", file=sys.stderr)
    holdout_fp = _parse_stage6_holdout_fingerprints(STAGE6_SPEC)
    calib_fp = _parse_calibration_fingerprints()
    v23_anchor_fp = _v23_anchor_fingerprints(pool)
    forbidden = holdout_fp | calib_fp | v23_anchor_fp
    print(f"[disjoint] forbidden fingerprints: "
          f"holdout={len(holdout_fp)} + calib_24={len(calib_fp)} + "
          f"v23_anchors_9={len(v23_anchor_fp)} = "
          f"{len(forbidden)} total (deduplicated)", file=sys.stderr)

    # Stratified sample 100 hands.
    selected = _stratified_sample(pool, 100, forbidden)
    if len(selected) < 100:
        print(f"[ERROR] only {len(selected)} hands selected (target 100). "
              "Pool exhausted given stratification + disjointness constraints.",
              file=sys.stderr)
        return 1
    assert len(selected) == 100

    # Verify disjointness post-hoc.
    sel_fps = {
        _fingerprint(_normalise_cards(s["hero_cards"]),
                      _normalise_cards(s["board"]))
        for s in selected
    }
    overlap_holdout = sel_fps & holdout_fp
    overlap_calib = sel_fps & calib_fp
    overlap_anchor = sel_fps & v23_anchor_fp
    if overlap_holdout or overlap_calib or overlap_anchor:
        print(f"[ERROR] disjointness check FAILED: "
              f"holdout overlap {len(overlap_holdout)}, "
              f"calib overlap {len(overlap_calib)}, "
              f"anchor overlap {len(overlap_anchor)}", file=sys.stderr)
        return 1
    print(f"[disjoint] post-sample check PASS — 0 fingerprint overlaps",
          file=sys.stderr)

    # Within-pilot uniqueness.
    if len(sel_fps) != 100:
        print(f"[ERROR] within-pilot dedup failed: {len(sel_fps)} unique "
              "fingerprints from 100 selected", file=sys.stderr)
        return 1
    print("[disjoint] within-pilot uniqueness PASS — 100 unique fingerprints",
          file=sys.stderr)

    # Re-tag + serialise.
    output_records = []
    for i, s in enumerate(selected):
        rec = {
            "pilot_hand_id": f"PILOT_{i + 1:03d}",
            "source_situation_id": s.get("situation_id"),
            "deal_id": s.get("deal_id"),
            "hero_cards": s.get("hero_cards"),
            "board": s.get("board"),
            "street": s.get("street"),
            "hero_position": s.get("hero_position"),
            "villain_positions": s.get("villain_positions"),
            "pot": s.get("pot"),
            "to_call": s.get("to_call"),
            "facing_bet": s.get("facing_bet"),
            "num_opponents": s.get("num_opponents"),
            "prior_actions": s.get("prior_actions"),
            "feat_dict": s.get("feat_dict"),
        }
        output_records.append(rec)

    # Write JSONL.
    os.makedirs(os.path.dirname(OUTPUT_JSONL), exist_ok=True)
    with open(OUTPUT_JSONL, "w") as f:
        for rec in output_records:
            f.write(json.dumps(rec, sort_keys=True) + "\n")
    print(f"[write] wrote {len(output_records)} hands to {OUTPUT_JSONL}",
          file=sys.stderr)

    # Hash-lock.
    with open(OUTPUT_JSONL, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    file_size = os.path.getsize(OUTPUT_JSONL)
    print(f"[hash] sha256 = {sha} ({file_size} bytes)", file=sys.stderr)

    # Sidecar.
    lock = {
        "pilot_hand_count": 100,
        "sha256": sha,
        "byte_size": file_size,
        "build_seed": SEED,
        "source_pool": SITUATIONS_PATH.removeprefix(REPO + "/"),
        "source_pool_size": len(pool),
        "candidate_pool_size_post_disjointness": (
            len(pool) - (len(pool) - len([
                s for s in pool
                if _normalise_cards(s.get("hero_cards", ""))
                and _normalise_cards(s.get("board", ""))
                and _fingerprint(
                    _normalise_cards(s["hero_cards"]),
                    _normalise_cards(s["board"]),
                ) not in forbidden
            ]))
        ),
        "disjointness": {
            "stage6_holdout_fingerprints": len(holdout_fp),
            "v23_calibration_24hand_legacy_fingerprints": len(calib_fp),
            "v23_anchor_9hand_extension_fingerprints": len(v23_anchor_fp),
            "total_forbidden_fingerprints_deduplicated": len(forbidden),
            "post_sample_overlap_holdout": 0,
            "post_sample_overlap_calibration": 0,
            "post_sample_overlap_anchor": 0,
            "within_pilot_unique_fingerprints": 100,
        },
        "stratification_dimensions": [
            "street",
            "hero_position",
            "opponent_count_bucket",
            "board_texture",
            "hero_range_placement",
        ],
        "stratification_report": _stratification_report(output_records),
        "build_directive": "review/comms/MAIN_TERMINAL_PR37_MERGE_ACK_BUILD_C_KICKOFF_2026-04-26.md",
        "predecessor_directive": "review/comms/MAIN_TERMINAL_PILOT_HALT_ACK_BUILDS_ABC_DIRECTIVE_2026-04-26.md (3f9564e)",
        "stage6_holdout_reference_hash": "65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5",
        "v23_calibration_constants_reference": "river-rats-core/calibration_exam.py v2.3 — STANDARD_EXAM_SIZE=28, STANDARD_PASS_THRESHOLD=23, GTO_REVERSAL_HANDS, GROUP_D_REVERSAL_HANDS",
        "fingerprint_method": "(sorted(hero_cards), sorted(board_cards)) per Stage 6 v1.0 spec §Non-overlap verification (notes feature: card-class equivalence not enforced — see Stage 6 v1.0 reviewer flag)",
    }
    with open(OUTPUT_LOCK, "w") as f:
        json.dump(lock, f, indent=2, sort_keys=True)
    print(f"[lock] wrote sidecar to {OUTPUT_LOCK}", file=sys.stderr)

    print("[done] Build C complete. Artifacts:", file=sys.stderr)
    print(f"  - {OUTPUT_JSONL}", file=sys.stderr)
    print(f"  - {OUTPUT_LOCK}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
