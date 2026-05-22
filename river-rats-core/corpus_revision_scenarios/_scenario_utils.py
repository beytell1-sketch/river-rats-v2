"""Shared utilities for corpus revision scenario generators.

Blueprint: review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3_2026-04-27.md
"""
from __future__ import annotations

import os
import sys
from typing import List, Optional, Set, Tuple, TYPE_CHECKING

# Ensure river-rats-core is importable
_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from situation_factory import SituationSpec, build_situation, normalise_situation
from gto_model import FEATURE_COLUMNS
from feature_keys import F

if TYPE_CHECKING:
    from corpus_revision_scenarios.positional_action_chain_scenarios import (
        ChainFingerprint,
    )

# Postflop seat order — referenced by compute_chain_fingerprint
POSTFLOP_SEAT_ORDER = ['SB', 'BB', 'UTG', 'HJ', 'CO', 'BTN']

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


def _normalize_position(pos: str) -> str:
    """6-max canonical position. Collapse EP→UTG, MP→HJ for seat-order math.

    Returns 'NONE' unchanged.
    """
    if pos == 'EP':
        return 'UTG'
    if pos == 'MP':
        return 'HJ'
    return pos


def compute_chain_fingerprint(spec: SituationSpec) -> 'ChainFingerprint':
    """Walk spec.action_history and reconstruct the 7-tuple ChainFingerprint
    per blueprint §2.1.

    Algorithm (action-order, not seat-order):
      1. Filter action_history to the current decision street (spec.street).
      2. First non-fold aggressive action ('bet') on the street → aggressor_pos.
         If no aggressor exists → chain_shape = OPEN (and callers_chain empty,
         raiser/raise_target = NONE).
      3. After aggressor's bet, walk further actions until action returns to
         hero (i.e., until a hero action appears, or actions end):
           - 'call' actions enter callers_chain in action order.
           - First 'raise' action → raiser_pos; raise_target_pos = aggressor_pos.
           - On 'raise', stop accumulating callers_chain.
      4. chain_shape determination:
           - aggressor == 'NONE'                                       → OPEN
           - raiser exists, aggressor had a prior 'check' on street    → CHECK_RAISE
           - raiser exists, no aggressor pre-check                     → BET_RAISE
           - 2+ raises by distinct positions detected                  → MULTI_AGGR
           - raiser none, callers count == 0                           → BET
           - raiser none, callers count == 1                           → BET_CALL
           - raiser none, callers count >= 2                           → BET_CALL_CALL

    Returns a ChainFingerprint NamedTuple.
    """
    # Local import to avoid circular dependency at module load time.
    from corpus_revision_scenarios.positional_action_chain_scenarios import (
        ChainFingerprint,
    )

    street = spec.street
    hero_pos = _normalize_position(spec.hero_pos)

    actions_on_street = [
        (_normalize_position(pos), action)
        for (s, pos, action) in spec.action_history
        if s == street
    ]

    aggressor = 'NONE'
    callers_chain: List[str] = []
    raisers: List[str] = []
    raise_target = 'NONE'

    # Track positions that checked on the street before the FIRST bet.
    # Canonical CHECK_RAISE = the raiser had a pre-bet check on the same street
    # (e.g., BB checks → CO bets → BB raises; raiser = BB, aggressor = CO).
    checks_before_bet: set = set()

    for pos, action in actions_on_street:
        if aggressor == 'NONE':
            if action == 'check':
                checks_before_bet.add(pos)
            elif action == 'bet':
                aggressor = pos
                continue
            elif action == 'fold':
                pass
        else:
            # Aggressor has bet; collect callers / raisers until hero acts again
            if pos == hero_pos:
                # Action returned to hero — decision moment
                break
            if action == 'call':
                callers_chain.append(pos)
            elif action == 'raise':
                if not raisers:
                    raise_target = aggressor
                raisers.append(pos)
                # Reset callers_chain — per blueprint §4.2 BET_RAISE note,
                # we collapse inter-caller positions in BET_RAISE.
                callers_chain = []
                # Continue walking in case of multi-raise (MULTI_AGGR)
            elif action == 'fold':
                pass
            elif action == 'check':
                # Should not happen after a bet, but ignore gracefully
                pass

    if aggressor == 'NONE':
        chain_shape = 'OPEN'
        raiser_pos = 'NONE'
        raise_target_pos = 'NONE'
    elif len(raisers) >= 2:
        chain_shape = 'MULTI_AGGR'
        raiser_pos = raisers[0]
        raise_target_pos = raise_target
    elif raisers:
        # CHECK_RAISE: raiser had a check on the street before the bet
        raiser_pre_check = raisers[0] in checks_before_bet
        chain_shape = 'CHECK_RAISE' if raiser_pre_check else 'BET_RAISE'
        raiser_pos = raisers[0]
        raise_target_pos = raise_target
    else:
        if len(callers_chain) == 0:
            chain_shape = 'BET'
        elif len(callers_chain) == 1:
            chain_shape = 'BET_CALL'
        else:
            chain_shape = 'BET_CALL_CALL'
        raiser_pos = 'NONE'
        raise_target_pos = 'NONE'

    return ChainFingerprint(
        street=street,
        hero_pos=hero_pos,
        aggressor_pos=aggressor,
        callers_chain=tuple(callers_chain),
        raiser_pos=raiser_pos,
        raise_target_pos=raise_target_pos,
        chain_shape=chain_shape,
    )
