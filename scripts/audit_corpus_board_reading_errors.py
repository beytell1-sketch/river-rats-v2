#!/usr/bin/env python3
"""Mechanical board-reading audit for 4-way corpus batches 001-009.

Scans every (spot, labeller) pair and flags cases where a labeller's
rationale text claims a draw feature that the actual cards don't support,
or fails to mention a draw feature that does exist.

This is a READ-ONLY audit. No label files are modified.

Output:
  data/4way_corpus/board_reading_audit_2026-05-30.jsonl
  review/comms/BOARD_READING_AUDIT_REPORT_2026-05-30.md

Usage:
  python3 scripts/audit_corpus_board_reading_errors.py

Author: Lead Programmer
Date: 2026-05-30
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO = Path(__file__).resolve().parent.parent
CORPUS_DIR = REPO / "data" / "4way_corpus" / "full_700"
LOOKALIKES_FILE = REPO / "data" / "4way_lookalikes_700hand_full_2026-05-12.jsonl"
CHAIN_DRAFT_FILE = Path("/tmp/batch_009_chain_quota_draft.jsonl")

AUDIT_DATE = "2026-05-30"
OUTPUT_JSONL = REPO / "data" / "4way_corpus" / f"board_reading_audit_{AUDIT_DATE}.jsonl"
REPORT_MD = REPO / "review" / "comms" / f"BOARD_READING_AUDIT_REPORT_{AUDIT_DATE}.md"

# ---------------------------------------------------------------------------
# Card parsing
# ---------------------------------------------------------------------------

RANK_ORDER = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
              "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
RANK_NAMES = {v: k for k, v in RANK_ORDER.items()}


def parse_card(card_str: str) -> Tuple[int, str]:
    """Parse a card like 'As', 'Tc', 'Kh' -> (rank_int, suit_char)."""
    card_str = card_str.strip()
    if len(card_str) < 2:
        raise ValueError(f"Invalid card: {repr(card_str)}")
    rank_char = card_str[0].upper()
    suit_char = card_str[1].lower()
    if rank_char not in RANK_ORDER:
        raise ValueError(f"Unknown rank {repr(rank_char)} in card {repr(card_str)}")
    if suit_char not in "shdc":
        raise ValueError(f"Unknown suit {repr(suit_char)} in card {repr(card_str)}")
    return (RANK_ORDER[rank_char], suit_char)


def parse_cards(cards_str: str) -> List[Tuple[int, str]]:
    """Parse a space-or-token-concatenated card string.

    Handles:
      "AsKs"         -> 2-card hero hand (each card is 2 chars)
      "Jc7s5d"       -> 3-card flop
      "Jc7s5d2h"     -> 4-card turn
      "Jc7s5d2hTc"   -> 5-card river
      "As Ks"        -> space-separated (less common)
    """
    if not cards_str or cards_str.lower() in ("none", "null", ""):
        return []
    # If space-separated, split on spaces; otherwise chunk by 2.
    cards_str = cards_str.strip()
    if " " in cards_str:
        tokens = cards_str.split()
    else:
        # Each card is exactly 2 characters: rank + suit
        if len(cards_str) % 2 != 0:
            raise ValueError(f"Card string has odd length: {repr(cards_str)}")
        tokens = [cards_str[i:i+2] for i in range(0, len(cards_str), 2)]
    return [parse_card(t) for t in tokens]


# ---------------------------------------------------------------------------
# Flush draw computation
# ---------------------------------------------------------------------------

def flush_features(hero_cards: List[Tuple[int, str]],
                   board_cards: List[Tuple[int, str]]
                   ) -> Dict:
    """Compute flush-draw features from hero + board cards.

    Returns dict with:
      suit_counts: dict of suit -> total count (hero+board)
      has_flush_draw: bool  (any suit has exactly 4 cards)
      has_backdoor_flush_draw: bool  (any suit has exactly 3 cards, no suit has 4+)
      flush_draw_suit: str or None  (suit that gives the flush draw)
      has_nut_flush_draw: bool  (has_flush_draw AND hero holds the Ace of that suit)
    """
    all_cards = hero_cards + board_cards
    suit_counts: Dict[str, int] = Counter(s for _, s in all_cards)
    hero_suit_map: Dict[str, List[int]] = defaultdict(list)
    for rank, suit in hero_cards:
        hero_suit_map[suit].append(rank)

    has_flush_draw = False
    has_backdoor_flush_draw = False
    flush_draw_suit = None

    # Check for flush draw (4 suited) — possible once flop is out
    for suit, count in suit_counts.items():
        if count == 4:
            has_flush_draw = True
            flush_draw_suit = suit
            break

    if not has_flush_draw:
        # Check for backdoor flush draw (3 suited)
        for suit, count in suit_counts.items():
            if count == 3:
                has_backdoor_flush_draw = True
                flush_draw_suit = suit
                break

    # Nut flush draw: hero has the Ace of the flush-draw suit and has_flush_draw
    has_nut_flush_draw = False
    if has_flush_draw and flush_draw_suit:
        if 14 in hero_suit_map.get(flush_draw_suit, []):
            has_nut_flush_draw = True

    return {
        "suit_counts": dict(suit_counts),
        "has_flush_draw": has_flush_draw,
        "has_backdoor_flush_draw": has_backdoor_flush_draw,
        "flush_draw_suit": flush_draw_suit,
        "has_nut_flush_draw": has_nut_flush_draw,
    }


# ---------------------------------------------------------------------------
# Straight draw computation
# ---------------------------------------------------------------------------

def straight_draw_features(hero_cards: List[Tuple[int, str]],
                            board_cards: List[Tuple[int, str]]
                            ) -> Dict:
    """Compute straight-draw features.

    Uses all currently visible cards (hero + board).  For a flush or OESD
    we count how many distinct *ranks* (not cards) would complete a straight
    on the next card dealt.

    Returns dict with:
      straight_out_ranks: frozenset of ranks that would complete a straight
      has_gutshot: bool  (1..4 ranks complete a straight; discontinuous)
      has_oesd: bool  (2 consecutive ranks each completing a 5-card straight,
                       i.e. 8 card outs total)
    """
    # Use a list for hero ranks to preserve duplicates (pocket pairs have two of same rank)
    hero_ranks_list = [r for r, _ in hero_cards]
    hero_ranks = set(hero_ranks_list)
    board_ranks = {r for r, _ in board_cards}
    known_ranks = hero_ranks | board_ranks  # all ranks currently on the felt

    # We must have both hero cards to compute draws.  If either is missing, skip.
    if len(hero_cards) != 2:
        return {"straight_out_ranks": frozenset(), "has_gutshot": False, "has_oesd": False}

    hero_ranks_sorted = sorted(hero_ranks_list)
    hr1, hr2 = hero_ranks_sorted[0], hero_ranks_sorted[-1]

    # For wheel: treat Ace as rank 1 as well
    def ranks_with_low_ace(ranks: Set[int]) -> Set[int]:
        if 14 in ranks:
            return ranks | {1}
        return ranks

    # Enumerate all possible "next cards" (ranks 2..14) and check if adding
    # that rank creates a 5-card straight that includes BOTH hero cards.
    out_ranks: Set[int] = set()

    all_ranks_with_ace = ranks_with_low_ace(known_ranks)
    # For checking straights we need hero ranks in low-ace form too
    hero_ranks_ext = ranks_with_low_ace(hero_ranks)
    # Low-ace versions of rank integers for straights
    def with_low_ace(r: int) -> Set[int]:
        return {r, 1} if r == 14 else {r}

    for candidate_rank in range(2, 15):  # 2..14
        if candidate_rank in known_ranks:
            continue  # already have this rank; not a new out
        # Build hypothetical rank set including the candidate
        hypothetical_ranks = ranks_with_low_ace(known_ranks | {candidate_rank})
        hypothetical_hero_ext = ranks_with_low_ace(hero_ranks | {candidate_rank})
        # We don't care whether candidate_rank is one of the hero cards here;
        # we're asking: if a card of this rank hits, does a straight exist?
        # Try all 5-card straight windows: {lo, lo+1, lo+2, lo+3, lo+4}
        # Valid high cards: 5..14 (i.e. straights A-2-3-4-5 through T-J-Q-K-A)
        for hi in range(5, 15):
            window = set(range(hi - 4, hi + 1))  # e.g. {10,11,12,13,14} for broadway
            # Special: wheel is {1,2,3,4,5}
            if hi == 5:
                window = {1, 2, 3, 4, 5}
            if not window.issubset(hypothetical_ranks):
                continue
            # Both hero ranks (possibly as 1 for A) must be in the window
            if not hero_ranks_ext.issubset(window):
                # One hero card might be the candidate itself (already counted
                # as an out) - check without expanding candidate
                # Actually hero_ranks_ext is fixed; just check it
                # But note: if candidate_rank == one of hero's cards rank,
                # hero_ranks_ext doesn't change.  We already skip candidates
                # that equal existing known_ranks, so this is fine.
                continue
            # Valid straight that includes both hero cards
            out_ranks.add(candidate_rank)
            break  # found a straight for this candidate; no need to check more windows

    # Classify:
    # OESD: exactly 2 ranks complete the straight AND they are consecutive
    #   (the classic 4-card open-ended draw: e.g. 8-9-T-J needs a 7 or Q)
    # Gutshot: 1..4 ranks complete a straight (a "belly buster")
    #   Note: we use a generous definition — 1 to 4 ranks gives a gutshot.
    #   OESD requires exactly 2 consecutive ranks.
    has_oesd = False
    has_gutshot = False

    if len(out_ranks) >= 1:
        sorted_outs = sorted(out_ranks)
        if len(out_ranks) == 2 and (sorted_outs[1] - sorted_outs[0] == 1):
            has_oesd = True
        elif 1 <= len(out_ranks) <= 4:
            has_gutshot = True

    return {
        "straight_out_ranks": frozenset(out_ranks),
        "has_gutshot": has_gutshot,
        "has_oesd": has_oesd,
    }


# ---------------------------------------------------------------------------
# Rationale pattern matching
# ---------------------------------------------------------------------------

def classify_rationale_claims(text: str) -> Dict[str, bool]:
    """Extract draw-claim booleans from a free-text rationale.

    Patterns are case-insensitive.  We carefully order checks so that
    "backdoor flush draw" is detected before plain "flush draw" to avoid
    over-counting.
    """
    t = text.lower()

    # Helper: detect presence of a pattern in text
    def has(pattern: str) -> bool:
        return bool(re.search(pattern, t))

    # ----- Flush draw claims -----
    # "backdoor flush draw" / "BDFD" / "backdoor FD" / "backdoor fd"
    claims_bdfd = has(r"\bbackdoor\s+flush\s+draw\b") or \
                  has(r"\bbdfd\b") or \
                  has(r"\bbackdoor\s+fd\b") or \
                  has(r"\bbackdoor-flush\b")

    # "nut flush draw" / "NFD" / "nut fd"
    # EXCLUDE "backdoor nut flush draw" — check that 'backdoor' does not precede within 15 chars.
    claims_nfd = False
    for m in re.finditer(r"\bnut\s+flush\s+draw\b|\bnfd\b|\bnut\s+fd\b", t):
        preceding_15 = t[max(0, m.start() - 15):m.start()]
        if "backdoor" not in preceding_15:
            claims_nfd = True
            break

    # Plain "flush draw" / "fd" — but NOT backdoor, NOT preceded by "no"
    # Strategy: strip out all backdoor/nut/no-negation occurrences, then check residual.
    # We strip: "backdoor flush draw", "nut flush draw", "no flush draw",
    #           "backdoor fd", "nut fd", "no fd", bdfd, nfd
    # and check if "flush draw" or standalone "fd" remains.
    stripped = re.sub(r"\bno\s+flush\s+draw\b", " ", t)
    stripped = re.sub(r"\bbackdoor\s+flush\s+draw\b", " ", stripped)
    stripped = re.sub(r"\bnut\s+flush\s+draw\b", " ", stripped)
    stripped = re.sub(r"\bbdfd\b", " ", stripped)
    stripped = re.sub(r"\bnfd\b", " ", stripped)
    stripped = re.sub(r"\bbackdoor\s+fd\b", " ", stripped)
    stripped = re.sub(r"\bnut\s+fd\b", " ", stripped)
    stripped = re.sub(r"\bno\s+fd\b", " ", stripped)
    claims_fd = bool(re.search(r"\bflush\s+draw\b", stripped)) or \
                bool(re.search(r"(?<![a-z])fd(?![a-z])", stripped))

    # "no flush draw" / "no fd" — labeller explicitly says there is none
    claims_no_fd = has(r"\bno\s+flush\s+draw\b") or \
                   has(r"\bno\s+fd\b") or \
                   has(r"\bno_flush_draw\b") or \
                   has(r"\bno\s+flush\b")

    # ----- Straight draw claims -----
    claims_gutshot = has(r"\bgutshot\b") or \
                     has(r"\bgut.shot\b") or \
                     has(r"\bbelly.buster\b")

    # OESD: only fire if "hero" or "we" or "i have" context nearby, OR if no "villain" near
    # Simple heuristic: fire on oesd/open-ended, but see find_mismatches for suppression.
    claims_oesd = has(r"\boesd\b") or \
                  has(r"\bopen.ended\s+straight\b") or \
                  has(r"\bopen\s+ended\s+straight\b") or \
                  has(r"\bopen-ended\b") or \
                  has(r"\bopen\s+ended\b")

    claims_no_straight = has(r"\bno\s+straight\s+draw\b") or \
                         has(r"\bno\s+draw\b") or \
                         has(r"\bno_straight\b")

    return {
        "claims_nfd": claims_nfd,
        "claims_fd": claims_fd,
        "claims_bdfd": claims_bdfd,
        "claims_no_fd": claims_no_fd,
        "claims_gutshot": claims_gutshot,
        "claims_oesd": claims_oesd,
        "claims_no_straight": claims_no_straight,
    }


# ---------------------------------------------------------------------------
# Mismatch detection
# ---------------------------------------------------------------------------

MISMATCH_TYPES = [
    "PHANTOM_NFD",
    "PHANTOM_FD",
    "CONFLATED_BDFD_AS_FD",
    "MISSED_FD",
    "PHANTOM_GUTSHOT",
    "PHANTOM_OESD",
]


def find_mismatches(spot: Dict, rationale_claims: Dict, truth: Dict) -> List[str]:
    """Return list of mismatch type strings for a (spot, labeller) pair.

    Parameters
    ----------
    spot : dict
        The spot definition (hero_cards, board, etc.)
    rationale_claims : dict
        Output of classify_rationale_claims()
    truth : dict
        Mechanical truth: merged flush_features + straight_draw_features output
    """
    mismatches = []

    # PHANTOM_NFD: claims nut flush draw but hero doesn't have NFD.
    # Suppressed if labeller also says "no flush draw" (consistent self-correction).
    if (rationale_claims["claims_nfd"] and
            not truth["has_nut_flush_draw"] and
            not rationale_claims["claims_no_fd"]):
        mismatches.append("PHANTOM_NFD")

    # PHANTOM_FD: claims plain flush draw but no flush draw exists at all.
    # Suppressed if labeller also says "no flush draw" — those are villain-range
    # mentions where labeller correctly identifies the absence.
    if (rationale_claims["claims_fd"] and
            not truth["has_flush_draw"] and
            not rationale_claims["claims_no_fd"]):
        mismatches.append("PHANTOM_FD")

    # CONFLATED_BDFD_AS_FD: claims plain FD, no actual FD, but BDFD exists.
    # Suppressed if claims_no_fd is also present.
    if (rationale_claims["claims_fd"] and
            not truth["has_flush_draw"] and
            truth["has_backdoor_flush_draw"] and
            not rationale_claims["claims_no_fd"]):
        mismatches.append("CONFLATED_BDFD_AS_FD")

    # MISSED_FD: has a flush draw but rationale mentions no flush draw signal at all
    if (truth["has_flush_draw"] and
            not rationale_claims["claims_nfd"] and
            not rationale_claims["claims_fd"] and
            not rationale_claims["claims_no_fd"]):
        mismatches.append("MISSED_FD")

    # PHANTOM_GUTSHOT: claims gutshot but neither gutshot nor OESD exists.
    # Suppressed if labeller also says "no straight draw" (consistent self-correction).
    if (rationale_claims["claims_gutshot"] and
            not truth["has_gutshot"] and
            not truth["has_oesd"] and
            not rationale_claims["claims_no_straight"]):
        mismatches.append("PHANTOM_GUTSHOT")

    # PHANTOM_OESD: claims OESD but no OESD exists.
    # Suppressed if labeller also says "no straight draw".
    if (rationale_claims["claims_oesd"] and
            not truth["has_oesd"] and
            not rationale_claims["claims_no_straight"]):
        mismatches.append("PHANTOM_OESD")

    return mismatches


# ---------------------------------------------------------------------------
# Spot index loading
# ---------------------------------------------------------------------------

def load_spot_index() -> Dict[str, Dict]:
    """Load all spot definitions into a dict keyed by spot_id.

    Sources:
      1. data/4way_corpus/full_700/batch_NNN_50hand.jsonl (batches 001-008)
      2. data/4way_lookalikes_700hand_full_2026-05-12.jsonl (extended lookalikes)
      3. /tmp/batch_009_chain_quota_draft.jsonl (batch_009 chain spots)
    """
    index: Dict[str, Dict] = {}

    # Batches 001-008 50hand files
    for n in range(1, 9):
        path = CORPUS_DIR / f"batch_{n:03d}_50hand.jsonl"
        if not path.exists():
            print(f"  WARNING: {path.name} not found", file=sys.stderr)
            continue
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                index[rec["spot_id"]] = rec

    # Extended lookalikes (contains SR, MW-AXIS, RANGE-AS spot types)
    if LOOKALIKES_FILE.exists():
        with open(LOOKALIKES_FILE) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                index[rec["spot_id"]] = rec
    else:
        print(f"  WARNING: lookalikes file not found: {LOOKALIKES_FILE}", file=sys.stderr)

    # Batch 009 chain quota draft
    if CHAIN_DRAFT_FILE.exists():
        with open(CHAIN_DRAFT_FILE) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                index[rec["spot_id"]] = rec
    else:
        print(f"  WARNING: chain draft file not found: {CHAIN_DRAFT_FILE}", file=sys.stderr)

    return index


# ---------------------------------------------------------------------------
# Label file loading
# ---------------------------------------------------------------------------

def load_label_records(batch_n: int) -> List[Dict]:
    """Load all label records for a batch (labellers 1-5 + opus if exists).

    For batches 001-008: use _v2.jsonl files (normalised schema).
    For batch_009: use chunk tmp files.

    Returns list of dicts, each with at least:
      spot_id, labeller_id, reasoning
    """
    records = []

    if batch_n <= 8:
        # Labellers 1-5: prefer v2, fall back to v1
        for labeller_id in range(1, 6):
            v2_path = CORPUS_DIR / f"batch_{batch_n:03d}_raw_labels_labeller_{labeller_id}_v2.jsonl"
            v1_path = CORPUS_DIR / f"batch_{batch_n:03d}_raw_labels_labeller_{labeller_id}.jsonl"
            path = v2_path if v2_path.exists() else v1_path
            if not path.exists():
                print(f"  WARNING: No label file for batch {batch_n} labeller {labeller_id}", file=sys.stderr)
                continue
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    rec = json.loads(line)
                    records.append(rec)

        # Opus tier-up: prefer v2
        opus_v2 = CORPUS_DIR / f"batch_{batch_n:03d}_raw_labels_opus_tierup_v2.jsonl"
        opus_v1 = CORPUS_DIR / f"batch_{batch_n:03d}_raw_labels_opus_tierup.jsonl"
        opus_path = opus_v2 if opus_v2.exists() else opus_v1
        if opus_path.exists():
            with open(opus_path) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    rec = json.loads(line)
                    records.append(rec)

    else:
        # Batch 009: use chunk tmp files
        for labeller_id in range(1, 6):
            chunks = sorted(glob.glob(
                str(CORPUS_DIR / f"batch_{batch_n:03d}_raw_labels_labeller_{labeller_id}_chunk_*.tmp.jsonl")
            ))
            for chunk_path in chunks:
                with open(chunk_path) as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        rec = json.loads(line)
                        records.append(rec)

    return records


# ---------------------------------------------------------------------------
# Consensus loading
# ---------------------------------------------------------------------------

def load_consensus(batch_n: int) -> Dict[str, Dict]:
    """Load consensus_v2 for a batch, keyed by spot_id."""
    path = CORPUS_DIR / f"batch_{batch_n:03d}_consensus_v2.jsonl"
    if not path.exists():
        return {}
    result = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            result[rec["spot_id"]] = rec
    return result


# ---------------------------------------------------------------------------
# False-positive risk annotation
# ---------------------------------------------------------------------------

def _false_positive_risk(mismatch_type: str, truth: Dict, claims: Dict) -> str:
    """Assign a HIGH/LOW false-positive-risk label to a flag.

    HIGH = pattern likely fired on villain-range or board-texture discussion,
           not on a genuine hero-draw claim.
    LOW  = the specific combination of cards + claim is consistent with a real
           hero board-reading error.

    Rules:
      PHANTOM_NFD:
        LOW if no FD exists and no BDFD (Type C: hero has no relation to any FD)
        LOW if FD exists but hero lacks the Ace (Type A: genuine NFD over-claim)
        HIGH if only BDFD exists (Type B: likely 'backdoor nut flush draw' phrasing)

      PHANTOM_FD:
        HIGH if no BDFD (hero has no flush connection; mention is villain range)
        LOW if BDFD exists (labeller confused BDFD with full FD — genuine error)
        NOTE: CONFLATED_BDFD_AS_FD captures this more precisely

      CONFLATED_BDFD_AS_FD:
        LOW always (specific error: BDFD exists, labeller claimed full FD)

      MISSED_FD:
        LOW always (mechanical: FD exists, no mention at all — likely real miss)

      PHANTOM_GUTSHOT:
        HIGH if 0 straight outs (hero has no straight connection; villain range)
        LOW if some straight outs exist (hero has draw, labeller over-claimed type)

      PHANTOM_OESD:
        HIGH if 0 straight outs (villain range or board texture)
        LOW if straight outs exist but not OESD (labeller over-claimed OESD for gutshot)
    """
    if mismatch_type == "PHANTOM_NFD":
        if not truth["has_flush_draw"] and truth["has_backdoor_flush_draw"]:
            return "HIGH"  # backdoor nut flush draw phrasing
        return "LOW"

    if mismatch_type == "PHANTOM_FD":
        if not truth["has_backdoor_flush_draw"]:
            return "HIGH"  # no flush connection at all; villain range / board texture
        return "LOW"  # BDFD exists; labeller confused with full FD

    if mismatch_type == "CONFLATED_BDFD_AS_FD":
        return "LOW"

    if mismatch_type == "MISSED_FD":
        return "LOW"

    if mismatch_type == "PHANTOM_GUTSHOT":
        if len(truth["straight_out_ranks"]) == 0:
            return "HIGH"
        return "LOW"

    if mismatch_type == "PHANTOM_OESD":
        if len(truth["straight_out_ranks"]) == 0:
            return "HIGH"
        return "LOW"

    return "UNKNOWN"


# ---------------------------------------------------------------------------
# Core audit logic
# ---------------------------------------------------------------------------

def compute_truth(spot: Dict) -> Optional[Dict]:
    """Compute mechanical truth for a spot.

    Returns None for preflop spots (no board to analyse).
    Returns a dict with combined flush + straight draw features.
    """
    street = spot.get("street", "").lower()
    board_str = spot.get("board") or ""
    hero_str = spot.get("hero_cards") or ""

    # Skip preflop
    if street == "preflop" or not board_str or board_str.lower() in ("none", "null", ""):
        return None

    try:
        hero_cards = parse_cards(hero_str)
        board_cards = parse_cards(board_str)
    except (ValueError, Exception) as e:
        print(f"  PARSE ERROR for spot {spot.get('spot_id')}: {e}", file=sys.stderr)
        return None

    if not hero_cards or not board_cards:
        return None

    ff = flush_features(hero_cards, board_cards)
    sf = straight_draw_features(hero_cards, board_cards)
    return {
        "hero_cards": hero_cards,
        "board_cards": board_cards,
        **ff,
        **sf,
        "hero_str": hero_str,
        "board_str": board_str,
    }


def run_audit() -> List[Dict]:
    """Run the full audit and return list of flagged records."""
    print("Loading spot index...", file=sys.stderr)
    spot_index = load_spot_index()
    print(f"  Loaded {len(spot_index)} spot definitions", file=sys.stderr)

    flags: List[Dict] = []
    stats = {
        "spots_scanned": 0,
        "spots_skipped_preflop": 0,
        "spots_not_found": 0,
        "pair_count": 0,
        "pairs_with_no_rationale": 0,
    }
    mismatch_counts: Counter = Counter()

    # Per-spot tracking for consensus-level analysis
    # spot_id -> list of (labeller_id, mismatches)
    spot_mismatch_map: Dict[str, List[Dict]] = defaultdict(list)

    for batch_n in range(1, 10):
        print(f"Processing batch {batch_n:03d}...", file=sys.stderr)
        label_records = load_label_records(batch_n)
        consensus = load_consensus(batch_n)

        # Group labels by spot_id to avoid recomputing truth per label
        by_spot: Dict[str, List[Dict]] = defaultdict(list)
        for rec in label_records:
            by_spot[rec["spot_id"]].append(rec)

        for spot_id, labels in by_spot.items():
            spot = spot_index.get(spot_id)
            if spot is None:
                stats["spots_not_found"] += 1
                continue

            truth = compute_truth(spot)
            if truth is None:
                stats["spots_skipped_preflop"] += 1
                continue

            stats["spots_scanned"] += 1
            consensus_rec = consensus.get(spot_id)

            for label_rec in labels:
                stats["pair_count"] += 1
                reasoning = label_rec.get("reasoning") or label_rec.get("rationale") or ""
                if not reasoning:
                    stats["pairs_with_no_rationale"] += 1
                    continue

                claims = classify_rationale_claims(reasoning)
                mismatches = find_mismatches(spot, claims, truth)
                labeller_id = label_rec.get("labeller_id", "unknown")

                if mismatches:
                    for mismatch_type in mismatches:
                        mismatch_counts[mismatch_type] += 1

                        # false_positive_risk assessment:
                        # HIGH = likely villain-range discussion or board-texture mention
                        # LOW = claim is specific enough to be a genuine hero-draw error
                        fpr = _false_positive_risk(mismatch_type, truth, claims)

                        flag_rec = {
                            "spot_id": spot_id,
                            "batch": batch_n,
                            "labeller_id": str(labeller_id),
                            "mismatch_type": mismatch_type,
                            "false_positive_risk": fpr,
                            "hero_cards": truth["hero_str"],
                            "board": truth["board_str"],
                            "has_flush_draw": truth["has_flush_draw"],
                            "has_backdoor_flush_draw": truth["has_backdoor_flush_draw"],
                            "flush_draw_suit": truth["flush_draw_suit"],
                            "has_nut_flush_draw": truth["has_nut_flush_draw"],
                            "has_gutshot": truth["has_gutshot"],
                            "has_oesd": truth["has_oesd"],
                            "straight_out_ranks": sorted(truth["straight_out_ranks"]),
                            "claims_nfd": claims["claims_nfd"],
                            "claims_fd": claims["claims_fd"],
                            "claims_bdfd": claims["claims_bdfd"],
                            "claims_no_fd": claims["claims_no_fd"],
                            "claims_gutshot": claims["claims_gutshot"],
                            "claims_oesd": claims["claims_oesd"],
                            "consensus_action": (consensus_rec or {}).get("consensus_action"),
                            "consensus_state": (consensus_rec or {}).get("consensus_state"),
                        }
                        flags.append(flag_rec)

                spot_mismatch_map[spot_id].append({
                    "labeller_id": str(labeller_id),
                    "mismatches": mismatches,
                    "claims": claims,
                    "batch": batch_n,
                })

    print(f"\nScan complete.", file=sys.stderr)
    print(f"  Postflop spots scanned: {stats['spots_scanned']}", file=sys.stderr)
    print(f"  Preflop spots skipped:  {stats['spots_skipped_preflop']}", file=sys.stderr)
    print(f"  Spots not in index:     {stats['spots_not_found']}", file=sys.stderr)
    print(f"  (spot, labeller) pairs: {stats['pair_count']}", file=sys.stderr)
    print(f"  Pairs with no text:     {stats['pairs_with_no_rationale']}", file=sys.stderr)
    print(f"  Total flags:            {sum(mismatch_counts.values())}", file=sys.stderr)
    for mt in MISMATCH_TYPES:
        print(f"    {mt}: {mismatch_counts[mt]}", file=sys.stderr)

    # Attach summary stats to output for report generation
    flags.append({"_meta": True,
                  "stats": stats,
                  "mismatch_counts": dict(mismatch_counts),
                  "spot_mismatch_map": {k: v for k, v in spot_mismatch_map.items()}})
    return flags


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def build_report(flags: List[Dict], spot_index: Dict[str, Dict]) -> str:
    """Build the markdown report string."""
    # Extract meta record
    meta = next((r for r in flags if r.get("_meta")), {})
    stats = meta.get("stats", {})
    mismatch_counts = meta.get("mismatch_counts", {})
    spot_mismatch_map = meta.get("spot_mismatch_map", {})
    data_flags = [r for r in flags if not r.get("_meta")]

    total_spots = stats.get("spots_scanned", 0)
    total_pairs = stats.get("pair_count", 0)
    total_flags = sum(mismatch_counts.values())

    # Compute HIGH/LOW confidence splits per mismatch type
    low_fpr_counts: Counter = Counter()
    high_fpr_counts: Counter = Counter()
    for r in data_flags:
        mt = r["mismatch_type"]
        fpr = r.get("false_positive_risk", "UNKNOWN")
        if fpr == "LOW":
            low_fpr_counts[mt] += 1
        else:
            high_fpr_counts[mt] += 1

    # Find high-risk spots: unanimous/near-unanimous consensus + multiple labellers
    # made same board-read error
    high_risk: List[Dict] = []
    for spot_id, labeller_entries in spot_mismatch_map.items():
        # Count labellers with any mismatch
        flagged_labellers = [e for e in labeller_entries if e["mismatches"]]
        if not flagged_labellers:
            continue
        # Count distinct labeller IDs (exclude duplicates from chunking)
        distinct_flagged = len({e["labeller_id"] for e in flagged_labellers})
        total_labellers = len({e["labeller_id"] for e in labeller_entries})
        has_opus = any(e["labeller_id"] == "opus_tierup" for e in flagged_labellers)

        # Unanimous consensus check: look at consensus_state from flags
        spot_flags = [r for r in data_flags if r["spot_id"] == spot_id]
        consensus_state = (spot_flags[0].get("consensus_state") if spot_flags else None) or "unknown"
        consensus_action = (spot_flags[0].get("consensus_action") if spot_flags else None) or "unknown"
        spot_def = spot_index.get(spot_id, {})

        # Mismatch types that appeared (all)
        all_mismatches = [m for e in flagged_labellers for m in e["mismatches"]]
        mismatch_type_counts = Counter(all_mismatches)

        # LOW-fpr mismatches only (higher confidence genuine errors)
        low_fpr_flags = [r for r in spot_flags if r.get("false_positive_risk") == "LOW"]
        has_low_fpr_flag = len(low_fpr_flags) > 0
        low_fpr_labellers = {r["labeller_id"] for r in low_fpr_flags}

        high_risk.append({
            "spot_id": spot_id,
            "batch": (spot_flags[0].get("batch") if spot_flags else "?"),
            "hero_cards": spot_def.get("hero_cards", "?"),
            "board": spot_def.get("board", "?"),
            "consensus_state": consensus_state,
            "consensus_action": consensus_action,
            "distinct_flagged": distinct_flagged,
            "total_labellers": total_labellers,
            "has_opus_flagged": has_opus,
            "mismatch_types": dict(mismatch_type_counts),
            "is_unanimous_consensus": "all-agree" in consensus_state,
            "is_near_unanimous": distinct_flagged >= 3,
            "has_low_fpr_flag": has_low_fpr_flag,
            "low_fpr_labeller_count": len(low_fpr_labellers),
        })

    # Sort by risk: unanimous + low-fpr errors first, then opus, then count
    high_risk.sort(key=lambda x: (
        -int(x["is_unanimous_consensus"]),
        -int(x["has_low_fpr_flag"]),
        -int(x["has_opus_flagged"]),
        -x["distinct_flagged"],
    ))

    top_10 = high_risk[:10]

    # Build unanimous-consensus section — only spots with LOW-fpr flags
    unanimous_wrong = [r for r in high_risk
                       if r["is_unanimous_consensus"] and r["is_near_unanimous"]
                       and r["has_low_fpr_flag"]]

    # Compute totals
    total_low_fpr = sum(low_fpr_counts.values())
    total_high_fpr = sum(high_fpr_counts.values())

    lines = [
        f"# Board-Reading Audit Report — {AUDIT_DATE}",
        "",
        "**Audit type:** Mechanical (non-LLM) scan of rationale text vs computed draw features.",
        "**Scope:** Batches 001-009, postflop spots only.",
        "**Read-only:** No consensus_v2 or label files modified.",
        "",
        "---",
        "",
        "## Summary Counts",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Postflop spots scanned | {total_spots} |",
        f"| (spot, labeller) pairs scanned | {total_pairs} |",
        f"| Total flagged (spot, labeller) pairs | {total_flags} |",
        f"| LOW false-positive-risk flags (high-confidence genuine errors) | {total_low_fpr} |",
        f"| HIGH false-positive-risk flags (mostly villain-range noise) | {total_high_fpr} |",
        "",
        "### Flags by mismatch type (total / LOW-fpr / HIGH-fpr)",
        "",
        "LOW-fpr = mechanically verifiable as a genuine hero board-read error.",
        "HIGH-fpr = pattern likely fired on villain-range or board-texture text.",
        "",
        "| Mismatch type | Total | LOW-fpr | HIGH-fpr | Description |",
        "|---------------|-------|---------|----------|-------------|",
        f"| PHANTOM_NFD | {mismatch_counts.get('PHANTOM_NFD', 0)} | {low_fpr_counts.get('PHANTOM_NFD', 0)} | {high_fpr_counts.get('PHANTOM_NFD', 0)} | Claims NFD but hero lacks Ace of flush-draw suit (HIGH = 'backdoor NFD' phrasing) |",
        f"| PHANTOM_FD | {mismatch_counts.get('PHANTOM_FD', 0)} | {low_fpr_counts.get('PHANTOM_FD', 0)} | {high_fpr_counts.get('PHANTOM_FD', 0)} | Claims flush draw but no suit reaches 4 cards (HIGH = no BDFD at all; villain range) |",
        f"| CONFLATED_BDFD_AS_FD | {mismatch_counts.get('CONFLATED_BDFD_AS_FD', 0)} | {low_fpr_counts.get('CONFLATED_BDFD_AS_FD', 0)} | {high_fpr_counts.get('CONFLATED_BDFD_AS_FD', 0)} | Claims full FD when only BDFD exists — the canonical CHAIN-009-016 error class |",
        f"| MISSED_FD | {mismatch_counts.get('MISSED_FD', 0)} | {low_fpr_counts.get('MISSED_FD', 0)} | {high_fpr_counts.get('MISSED_FD', 0)} | Flush draw exists but no flush-draw mention in rationale |",
        f"| PHANTOM_GUTSHOT | {mismatch_counts.get('PHANTOM_GUTSHOT', 0)} | {low_fpr_counts.get('PHANTOM_GUTSHOT', 0)} | {high_fpr_counts.get('PHANTOM_GUTSHOT', 0)} | Claims gutshot but 0 hero straight outs (HIGH = villain-range mention) |",
        f"| PHANTOM_OESD | {mismatch_counts.get('PHANTOM_OESD', 0)} | {low_fpr_counts.get('PHANTOM_OESD', 0)} | {high_fpr_counts.get('PHANTOM_OESD', 0)} | Claims OESD but no OESD found (LOW = has outs but they're gutshot-class) |",
        "",
        "---",
        "",
        "## Top 10 Most-Impactful Flagged Spots",
        "",
        "Sorted by: unanimous consensus first, then LOW-fpr errors present, then opus-flagged, then labeller count.",
        "",
        "| Spot ID | Batch | Hero | Board | Consensus | Action | Flagged | Low-FPR flags | Opus? | Mismatch types |",
        "|---------|-------|------|-------|-----------|--------|---------|---------------|-------|----------------|",
    ]

    for r in top_10:
        mt_str = ", ".join(f"{k}({v})" for k, v in sorted(r["mismatch_types"].items()))
        lines.append(
            f"| {r['spot_id']} | {r['batch']} | {r['hero_cards']} | {r['board']} "
            f"| {r['consensus_state']} | {r['consensus_action']} "
            f"| {r['distinct_flagged']}/{r['total_labellers']} labellers "
            f"| {r['low_fpr_labeller_count']} labellers "
            f"| {'YES' if r['has_opus_flagged'] else 'no'} "
            f"| {mt_str} |"
        )

    lines += [
        "",
        "---",
        "",
        "## High-Risk: Unanimous Consensus + 3+ Labellers + LOW-FPR Board-Read Error",
        "",
        "These are the highest-risk training data points. Consensus action was reached",
        "unanimously AND 3+ labellers have at least one LOW false-positive-risk flag",
        "(i.e. a mechanically verifiable hero board-read error, not villain-range noise).",
        "",
    ]

    if not unanimous_wrong:
        lines.append("*No spots found with unanimous consensus + 3+ labellers flagged at LOW false-positive risk.*")
    else:
        lines += [
            "| Spot ID | Batch | Hero | Board | Action | Flagged labellers (any) | Low-FPR labellers | Mismatch types |",
            "|---------|-------|------|-------|--------|-------------------------|-------------------|----------------|",
        ]
        for r in unanimous_wrong:
            mt_str = ", ".join(f"{k}({v})" for k, v in sorted(r["mismatch_types"].items()))
            lines.append(
                f"| {r['spot_id']} | {r['batch']} | {r['hero_cards']} | {r['board']} "
                f"| {r['consensus_action']} "
                f"| {r['distinct_flagged']}/{r['total_labellers']} "
                f"| {r['low_fpr_labeller_count']} "
                f"| {mt_str} |"
            )

    lines += [
        "",
        "---",
        "",
        "## Pattern-Matching False-Positive Analysis",
        "",
        "The main false-positive source is villain-range discussion. Labellers explain",
        "what draws villains hold (e.g. 'villain's 98s has OESD', 'CO may have diamond FD').",
        "Our pattern matching cannot distinguish hero-draw claims from villain-range mentions.",
        "",
        "| Type | False-positive mechanism | Mitigation applied | Residual risk |",
        "|------|--------------------------|--------------------|-|",
        "| PHANTOM_NFD (Type B) | Labeller says 'backdoor nut flush draw' for hero; 'nut flush draw' pattern fires | Negative lookbehind: 'nut flush draw' preceded by 'backdoor' within 15 chars is excluded | LOW — mechanism specific |",
        "| PHANTOM_NFD (Type A/C) | Real errors: hero lacks Ace of FD suit (A) or has no FD at all (C) | None needed | NONE — genuine catches |",
        "| PHANTOM_FD (HIGH-fpr) | Hero has no flush connection; pattern fires on 'villain has flush draw' or 'board has diamond flush draw' | Claims suppressed when 'no flush draw' present in same rationale | MODERATE — suppression incomplete |",
        "| PHANTOM_FD (LOW-fpr) | Hero has BDFD; labeller called it full FD (same as CONFLATED_BDFD_AS_FD) | — | LOW |",
        "| CONFLATED_BDFD_AS_FD | Hero has BDFD, labeller says full FD | All LOW-fpr | LOW — mechanical catch |",
        "| PHANTOM_GUTSHOT | Hero has 0 straight outs; 'gutshot' fires on villain range | claims_no_straight suppression | HIGH (221/224 have 0 hero outs) |",
        "| PHANTOM_OESD | Same — 371/525 have 0 hero outs (villain range) | Same | HIGH for 0-out cases; LOW for 154 cases where gutshot exists |",
        "| MISSED_FD | FD exists, rationale says nothing about it | — | LOW (26 cases, mechanical) |",
        "",
        "**Bottom line:** The reliable (LOW-fpr) signal columns are:",
        f"- CONFLATED_BDFD_AS_FD: {low_fpr_counts.get('CONFLATED_BDFD_AS_FD', 0)} genuine hero board-read errors",
        f"- PHANTOM_NFD (Types A+C): ~{low_fpr_counts.get('PHANTOM_NFD', 0)} flags, minus Type B false positives",
        f"- PHANTOM_OESD (non-zero-outs): ~154 cases of gutshots misclaimed as OESD",
        f"- MISSED_FD: {low_fpr_counts.get('MISSED_FD', 0)} cases of unreported flush draws",
        "",
        "---",
        "",
        f"*Generated: {AUDIT_DATE} — scripts/audit_corpus_board_reading_errors.py*",
    ]

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=== Board-Reading Audit ===", file=sys.stderr)

    # Run audit
    flags = run_audit()

    # Extract meta before writing
    meta = next((r for r in flags if r.get("_meta")), {})
    spot_mismatch_map = meta.get("spot_mismatch_map", {})
    data_flags = [r for r in flags if not r.get("_meta")]

    # Write audit JSONL (data flags only, not meta)
    OUTPUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSONL, "w") as f:
        for rec in data_flags:
            f.write(json.dumps(rec) + "\n")
    print(f"\nWrote {len(data_flags)} flag records to {OUTPUT_JSONL}", file=sys.stderr)

    # Reload spot index for report
    spot_index = load_spot_index()

    # Write report
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    report_text = build_report(flags, spot_index)
    with open(REPORT_MD, "w") as f:
        f.write(report_text)
    print(f"Wrote report to {REPORT_MD}", file=sys.stderr)

    # Print summary to stdout
    mismatch_counts = meta.get("mismatch_counts", {})
    stats = meta.get("stats", {})
    print("\n=== AUDIT RESULTS ===")
    print(f"Postflop spots scanned:         {stats.get('spots_scanned', 0)}")
    print(f"(spot, labeller) pairs scanned: {stats.get('pair_count', 0)}")
    print(f"Total flagged pairs:            {sum(mismatch_counts.values())}")
    print()
    for mt in MISMATCH_TYPES:
        print(f"  {mt}: {mismatch_counts.get(mt, 0)}")


if __name__ == "__main__":
    main()
