"""Shared utilities for corpus revision scenario generators.

Blueprint: review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3_2026-04-27.md
"""
from __future__ import annotations

import os
import sys
from typing import List, Optional, Set, Tuple

# Ensure river-rats-core is importable
_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from situation_factory import SituationSpec, build_situation, normalise_situation
from gto_model import FEATURE_COLUMNS
from feature_keys import F

# 59-feature contract = FEATURE_COLUMNS (55) + 4 v2.4 P1 blockers
V24_P1_BLOCKER_FEATURES = (
    F.NUT_FLUSH_BLOCK,
    F.FLUSH_DRAW_BLOCK_PCT,
    F.STRAIGHT_DRAW_BLOCK_PCT,
    F.NUT_MADE_BLOCK_PCT,
)
EXPECTED_59_KEYS = list(FEATURE_COLUMNS) + list(V24_P1_BLOCKER_FEATURES)
assert len(EXPECTED_59_KEYS) == 59, (
    f"59-feature contract check failed: got {len(EXPECTED_59_KEYS)}"
)


def fingerprint(hero_cards: str, board: str) -> Tuple[str, str]:
    """Card-equivalence fingerprint compatible with build_pilot_corpus_100_hand.py."""
    def _cards(s: str) -> list:
        return [s[i:i+2] for i in range(0, len(s), 2)]
    return (
        "".join(sorted(_cards(hero_cards))),
        "".join(sorted(_cards(board))),
    )


def record_fingerprint(record: dict) -> Tuple[str, str]:
    """Get fingerprint from a record dict."""
    return fingerprint(
        record.get('hero_cards', ''),
        record.get('board', ''),
    )


def build_record_from_spec(
    spec: SituationSpec,
    situation_id: str,
    generation_source: str,
) -> dict:
    """Build a pool record from a SituationSpec.

    Calls SituationFactory, extracts the 59-feature dict, and returns
    a record dict matching the pool schema.

    Returns None and prints a warning if build_situation() fails.
    """
    try:
        feat_dict_full = build_situation(spec)
    except Exception as e:
        print(f"[WARN] build_situation failed for {situation_id}: {e}",
              flush=True)
        return None

    # Extract 59-feature contract
    feat_dict_59 = {}
    for k in EXPECTED_59_KEYS:
        v = feat_dict_full.get(k)
        if v is None:
            feat_dict_59[k] = 0  # default for missing features
        elif isinstance(v, float):
            feat_dict_59[k] = round(v, 6)
        elif isinstance(v, bool):
            feat_dict_59[k] = int(v)
        else:
            feat_dict_59[k] = v

    hero_cards_str = ''.join(spec.hero_cards)
    board_str = ''.join(spec.board_cards)

    record = {
        'situation_id': situation_id,
        'hero_cards': hero_cards_str,
        'board': board_str,
        'street': spec.street,
        'hero_position': spec.hero_pos,
        'villain_positions': list(spec.villain_positions),
        'pot': spec.pot,
        'to_call': spec.to_call,
        'facing_bet': spec.to_call > 0,
        'num_opponents': len(spec.villain_positions),
        'prior_actions': _build_prior_actions(spec),
        'feat_dict': feat_dict_59,
        'generation_source': generation_source,
        'opener_position': spec.opener_position,
    }
    return record


def _build_prior_actions(spec: SituationSpec) -> List[str]:
    """Build prior_actions list from the spec's action_history.

    Format: "preflop: CO raise" (street: position action)
    Only hero's own actions are included (matching the existing pool format).
    """
    prior = []
    for street, pos, action in spec.action_history:
        if pos == spec.hero_pos:
            prior.append(f"{street}: {pos} {action}")
    return prior


def is_duplicate(
    hero_cards: str,
    board: str,
    forbidden_fingerprints: Set[Tuple[str, str]],
) -> bool:
    """Check if this hero/board combination is in the forbidden set."""
    fp = fingerprint(hero_cards, board)
    return fp in forbidden_fingerprints


def add_to_forbidden(
    records: List[dict],
    forbidden_fingerprints: Set[Tuple[str, str]],
) -> None:
    """Add fingerprints of all records to the forbidden set (in-place)."""
    for r in records:
        fp = record_fingerprint(r)
        forbidden_fingerprints.add(fp)
