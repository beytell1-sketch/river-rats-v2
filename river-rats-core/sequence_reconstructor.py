#!/usr/bin/env python3
"""Sequence reconstructor — rebuilds action strings from feature counters.

Takes a self-play situation record (hero cards, board, positions, street,
prior_actions, and feature counters) and reconstructs the current-street
action sequence. Validates each candidate through hand_sequence_validator.

Classifications:
  CERTAIN   — exactly 1 valid sequence consistent with features
  AMBIGUOUS — multiple valid sequences (all consistent with features)
  CORRUPT   — zero valid sequences consistent with features

The SUSPECT classification is applied later (Phase 1C) when re-extracted
features don't match originals.

Usage:
    from sequence_reconstructor import reconstruct_sequence, ReconResult

    result = reconstruct_sequence(situation_record)
    print(result.classification)  # CERTAIN, AMBIGUOUS, or CORRUPT
    print(result.action_string)   # best sequence or None
"""
import json
import sys
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from itertools import product

from hand_sequence_validator import validate_action_string

# Postflop position order (same as hand_sequence_validator)
POSTFLOP_ORDER = {
    'SB': 0, 'BB': 1, 'UTG': 2, 'EP': 2,
    'HJ': 3, 'MP': 3, 'CO': 4, 'BTN': 5,
}


@dataclass
class ReconResult:
    """Result of reconstructing a situation's action sequence."""
    situation_id: str
    classification: str   # CERTAIN, AMBIGUOUS, CORRUPT
    action_string: Optional[str]   # selected sequence (or None if CORRUPT)
    num_valid: int                 # how many valid sequences found
    all_valid: List[str]           # all valid sequences
    notes: str = ''


def _sorted_positions(positions: List[str]) -> List[str]:
    """Sort positions in postflop order (SB first, BTN last)."""
    return sorted(positions, key=lambda p: POSTFLOP_ORDER.get(p.upper(), 99))


def _parse_prior_actions(prior_actions: List[str], current_street: str) -> List[str]:
    """Extract hero's actions on the current street from prior_actions.

    prior_actions format: ["preflop: CO raise", "flop: CO check", ...]
    Returns list of hero actions on current_street (e.g. ["check"]).
    """
    street_map = {'f': 'flop', 't': 'turn', 'r': 'river',
                  'flop': 'flop', 'turn': 'turn', 'river': 'river'}
    target = street_map.get(current_street, current_street)

    hero_acts = []
    for pa in prior_actions:
        if ':' not in pa:
            continue
        street_part, action_part = pa.split(':', 1)
        street_part = street_part.strip().lower()
        action_part = action_part.strip().lower()
        if street_part == target:
            # Extract just the action word (last token)
            tokens = action_part.split()
            if len(tokens) >= 2:
                hero_acts.append(tokens[-1])  # "co check" -> "check"
    return hero_acts


def _generate_candidates(
    hero_pos: str,
    villain_positions: List[str],
    facing_bet: int,
    villain_agg: int,
    villain_checked_back: int,
    villain_call_count: int,
    num_callers_to_bet: int,
    facing_raise: int,
    to_call: float,
    hero_prior_acts: List[str],
) -> List[str]:
    """Generate candidate action strings consistent with feature counters.

    The counters constrain what happened on the current street:
    - facing_bet: 1 if hero faces a live bet at decision point
    - villain_agg: total villain bets/raises across prior streets (not current)
    - villain_checked_back: 1 if any villain checked when they could bet (prior)
    - villain_call_count: villain flat-calls across prior streets
    - num_callers_to_bet: opponents who called current-street bet before hero
    - facing_raise: 1 if hero faces a raise (not initial bet)

    IMPORTANT: villain_aggression_count, villain_checked_back, and
    villain_call_count are CROSS-STREET counters from prior streets.
    They do NOT tell us what happened on the current street — only
    facing_bet, num_callers_to_bet, and facing_raise describe the
    current street.
    """
    all_positions = _sorted_positions([hero_pos] + list(villain_positions))
    hero_idx = all_positions.index(hero_pos)
    bet_amount = int(to_call) if to_call > 0 else 0

    candidates = []

    if facing_raise:
        # Hero faces a raise — complex scenario. Hero must have bet/raised,
        # then a villain raised over it. Not present in our data (all
        # facing_raise=0), but handle for completeness.
        return []

    if not facing_bet:
        # Hero is not facing a bet. All players before hero checked.
        # Hero will act (the ??? decision point).
        parts = []
        for pos in all_positions:
            if pos == hero_pos:
                # Check if hero already checked on this street
                if hero_prior_acts and hero_prior_acts[0] == 'check':
                    parts.append(f'{pos} check')
                    # After hero check, remaining villains may check or bet
                    remaining = [p for p in all_positions if p != pos
                                 and all_positions.index(p) > all_positions.index(pos)]
                    if remaining:
                        # All remaining checked (since facing_bet=0)
                        for rp in remaining:
                            parts.append(f'{rp} check')
                        parts.append(f'{hero_pos} ???')
                    else:
                        parts.append(f'{hero_pos} ???')
                else:
                    parts.append(f'{pos} ???')
                break
            else:
                parts.append(f'{pos} check')
        candidates.append(', '.join(parts))

    else:
        # Hero faces a bet. One villain bet, hero faces it.
        # num_callers_to_bet=0 means no other villain called between bettor and hero.
        # We need to figure out: which villain bet?

        # Identify who could have bet
        villains = [p for p in all_positions if p != hero_pos]

        for bettor in villains:
            parts = []
            bet_placed = False

            for pos in all_positions:
                if pos == hero_pos and not bet_placed:
                    # Hero acts before bettor — must check first
                    if hero_prior_acts and hero_prior_acts[0] == 'check':
                        parts.append(f'{pos} check')
                    else:
                        parts.append(f'{pos} check')
                    continue

                if pos == bettor and not bet_placed:
                    if bet_amount > 0:
                        parts.append(f'{pos} bet {bet_amount}')
                    else:
                        parts.append(f'{pos} bet')
                    bet_placed = True
                    continue

                if bet_placed and pos != hero_pos:
                    # Other villain after the bet
                    if num_callers_to_bet > 0:
                        if bet_amount > 0:
                            parts.append(f'{pos} call {bet_amount}')
                        else:
                            parts.append(f'{pos} call')
                    else:
                        parts.append(f'{pos} fold')
                    continue

                if pos == hero_pos:
                    parts.append(f'{pos} ???')
                    break

                # Before bettor, not hero
                parts.append(f'{pos} check')

            # Make sure hero ??? is at the end
            if not any('???' in p for p in parts):
                parts.append(f'{hero_pos} ???')

            candidates.append(', '.join(parts))

    return candidates


def _select_best(
    valid_sequences: List[str],
    hero_prior_acts: List[str],
    hero_pos: str,
) -> str:
    """Select the best sequence from multiple valid options.

    Decision rule (owner directive):
    1. Prefer sequence whose hero actions match prior_actions
    2. If still tied, prefer simplest (fewest total actions)
    """
    if len(valid_sequences) == 1:
        return valid_sequences[0]

    # Score by hero action match
    def hero_match_score(seq):
        """Count how many hero actions in seq match prior_actions."""
        parts = [p.strip() for p in seq.split(',')]
        hero_acts_in_seq = []
        for part in parts:
            tokens = part.split()
            if tokens[0].upper() == hero_pos.upper() and '???' not in part:
                hero_acts_in_seq.append(tokens[1].lower())
        matches = 0
        for i, act in enumerate(hero_acts_in_seq):
            if i < len(hero_prior_acts) and act == hero_prior_acts[i]:
                matches += 1
        return matches

    # Score by simplicity (fewer parts = simpler)
    def simplicity_score(seq):
        return -len(seq.split(','))

    scored = [(hero_match_score(s), simplicity_score(s), s) for s in valid_sequences]
    scored.sort(key=lambda x: (-x[0], -x[1]))  # best match first, then simplest
    return scored[0][2]


def reconstruct_sequence(sit: dict) -> ReconResult:
    """Reconstruct the current-street action string for a situation.

    Args:
        sit: A situation record from 3way_combined_350.jsonl

    Returns:
        ReconResult with classification, selected sequence, and metadata.
    """
    sid = sit.get('situation_id', '?')
    hero_pos = sit['hero_position']
    villain_positions = sit['villain_positions']
    street = sit.get('street', 'flop')
    prior_actions = sit.get('prior_actions', [])
    fd = sit.get('feat_dict', {})

    facing_bet = int(fd.get('facing_bet', 0))
    villain_agg = int(fd.get('villain_aggression_count', 0))
    villain_checked_back = int(fd.get('villain_checked_back', 0))
    villain_call_count = int(fd.get('villain_call_count', 0))
    num_callers_to_bet = int(fd.get('num_callers_to_bet', 0))
    facing_raise = int(fd.get('facing_raise', 0))
    to_call = float(fd.get('to_call', 0))

    hero_prior_acts = _parse_prior_actions(prior_actions, street)
    all_positions = _sorted_positions([hero_pos] + list(villain_positions))

    # Street name mapping for validator
    street_map = {'f': 'flop', 't': 'turn', 'r': 'river'}
    street_name = street_map.get(street, street)

    # Generate candidates
    candidates = _generate_candidates(
        hero_pos, villain_positions,
        facing_bet, villain_agg, villain_checked_back,
        villain_call_count, num_callers_to_bet, facing_raise,
        to_call, hero_prior_acts,
    )

    if not candidates:
        return ReconResult(
            situation_id=sid,
            classification='CORRUPT',
            action_string=None,
            num_valid=0,
            all_valid=[],
            notes='No candidate sequences generated (possibly facing_raise=1)',
        )

    # Validate each candidate
    valid = []
    for cand in candidates:
        errors = validate_action_string(all_positions, street_name, cand, hero_pos)
        if not errors:
            valid.append(cand)

    if not valid:
        return ReconResult(
            situation_id=sid,
            classification='CORRUPT',
            action_string=None,
            num_valid=0,
            all_valid=[],
            notes=f'0/{len(candidates)} candidates passed validation',
        )

    # Deduplicate
    valid = list(dict.fromkeys(valid))

    if len(valid) == 1:
        return ReconResult(
            situation_id=sid,
            classification='CERTAIN',
            action_string=valid[0],
            num_valid=1,
            all_valid=valid,
        )

    # Multiple valid — select best per owner decision rule
    selected = _select_best(valid, hero_prior_acts, hero_pos)
    return ReconResult(
        situation_id=sid,
        classification='AMBIGUOUS',
        action_string=selected,
        num_valid=len(valid),
        all_valid=valid,
        notes=f'Selected from {len(valid)} valid sequences (hero action match)',
    )


def reconstruct_batch(filepath: str) -> List[ReconResult]:
    """Reconstruct sequences for all self-play situations in a JSONL file.

    Skips factory situations (those without prior_actions).
    """
    results = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sit = json.loads(line)
            if not sit.get('prior_actions'):
                continue  # factory situation — skip
            results.append(reconstruct_sequence(sit))
    return results


# ── CLI ──────────────────────────────────────────────────────────────

def main():
    """Run reconstruction on a JSONL file and print summary."""
    if len(sys.argv) < 2:
        print("Usage: python3 sequence_reconstructor.py <jsonl_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    results = reconstruct_batch(filepath)

    # Summary
    from collections import Counter
    counts = Counter(r.classification for r in results)
    print(f"Reconstructed {len(results)} situations:")
    for cls in ['CERTAIN', 'AMBIGUOUS', 'CORRUPT']:
        print(f"  {cls}: {counts.get(cls, 0)}")

    # Detail for non-CERTAIN
    for r in results:
        if r.classification != 'CERTAIN':
            print(f"\n{r.situation_id}: {r.classification}")
            if r.action_string:
                print(f"  Selected: {r.action_string}")
            if r.notes:
                print(f"  Notes: {r.notes}")
            if r.all_valid and len(r.all_valid) > 1:
                for i, v in enumerate(r.all_valid):
                    print(f"  Option {i+1}: {v}")


if __name__ == '__main__':
    main()
