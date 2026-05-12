#!/usr/bin/env python3
"""Phase 2-E FULL — 700-hand 4-way lookalike generator.

Per dispatch PR #424. Generates 700 unique 4-way lookalike spots by
applying systematic variations to the existing anchor sets:
- 50-hand pilot subset (PR #421 frozen)
- 35-hand reference set (PR #409 frozen)
- 29-hand calibration set (PR #413 frozen)

Total anchors: 114. Variants per anchor: ~6 (700/114 ≈ 6.1) across these dims:
  V1: hero suit-swap (preserves rank composition + board-texture interaction)
  V2: board-runout-brick swap (preserves texture class but changes specifics)
  V3: hero rank-substitution within hand-class (e.g., KJs → KQs for TPGK)
  V4: villain position rotation (preserves range-asymmetry pattern)
  V5: stack-depth variant (100bb default → 75bb or 150bb)
  V6: action-history micro-variant (e.g., HJ flat vs HJ folds)

Distribution target per dispatch (axis weights):
  4-way 3-bet/4-bet:    140
  Multiway-cooler:       70
  Closing-action:       125
  Range-asymmetry:      125
  MW-40/45/47:          100
  Standard 4-way SRP:   140
  Total:                700

Outputs `data/4way_lookalikes_700hand_full_2026-05-12.jsonl`.

CLI: python3 scripts/generate_4way_lookalikes_700.py
"""
from __future__ import annotations

import copy
import json
import os
import random
import sys
from collections import Counter, defaultdict


ANCHOR_FILES = [
    'data/4way_lookalikes_50hand_pilot_2026-05-11.jsonl',
    'data/4way_reference_35hand_2026-05-11.jsonl',
    'data/4way_calibration_29hand_2026-05-11.jsonl',
]

OUTPUT = 'data/4way_lookalikes_700hand_full_2026-05-12.jsonl'

TARGET_PER_AXIS = {
    '4-way-3-bet-pot': 140,
    'multiway-cooler': 70,
    'closing-action-variants': 125,
    'range-asymmetry': 125,
    'MW-axis': 100,  # combined MW-40 + MW-45 + MW-47 + combo
    '4-way-SRP-standard': 140,
}

RANKS = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
SUITS = ['c','d','h','s']
SUIT_ROTATIONS = [
    {'c':'h','h':'c','d':'s','s':'d'},  # rot1
    {'c':'d','d':'c','h':'s','s':'h'},  # rot2
    {'c':'s','s':'c','d':'h','h':'d'},  # rot3
]
POSITION_ROTATIONS = {
    'UTG': 'EP', 'EP': 'UTG',
    'HJ': 'MP', 'MP': 'HJ',
    'CO': 'CO',
    'BTN': 'BTN',
    'SB': 'SB',
    'BB': 'BB',
}
STACK_VARIANTS = [75, 100, 100, 100, 150, 200]


def load_anchors():
    anchors = []
    for path in ANCHOR_FILES:
        if not os.path.exists(path):
            print(f'WARN: anchor file missing: {path}', file=sys.stderr)
            continue
        for line in open(path):
            d = json.loads(line)
            d['_source'] = path
            anchors.append(d)
    return anchors


def normalize_axis(axis_str):
    """Map specific axis labels to the 6-family bucketing."""
    a = (axis_str or '').lower()
    if '3-bet' in a or '4-bet' in a or '3bet' in a or '4bet' in a:
        return '4-way-3-bet-pot'
    if 'cooler' in a:
        return 'multiway-cooler'
    if 'closing' in a or 'close' in a:
        return 'closing-action-variants'
    if 'asym' in a or 'asymmetry' in a:
        return 'range-asymmetry'
    if 'mw-' in a or 'mw40' in a or 'mw45' in a or 'mw47' in a or 'mw-combo' in a:
        return 'MW-axis'
    if 'srp' in a:
        return '4-way-SRP-standard'
    return '4-way-SRP-standard'


def rotate_suits(card_str, suit_map):
    """Apply suit rotation to a card string."""
    if not card_str:
        return card_str
    # Card string like 'AhKs' or '8c5h2d' — pairs of (rank, suit)
    out = []
    i = 0
    while i < len(card_str):
        if i + 1 < len(card_str):
            rank, suit = card_str[i], card_str[i+1]
            out.append(rank + suit_map.get(suit, suit))
            i += 2
        else:
            out.append(card_str[i])
            i += 1
    return ''.join(out)


def make_variant_v1(anchor, rot_idx=0):
    """V1: Suit rotation (preserves rank composition + texture relationships)."""
    suit_map = SUIT_ROTATIONS[rot_idx % len(SUIT_ROTATIONS)]
    v = copy.deepcopy(anchor)
    if v.get('hero_cards'):
        v['hero_cards'] = rotate_suits(v['hero_cards'], suit_map)
    if v.get('board'):
        v['board'] = rotate_suits(v['board'], suit_map)
    return v


def make_variant_v2(anchor, rng):
    """V2: Board brick swap (replace last board card with similar-rank brick)."""
    v = copy.deepcopy(anchor)
    if not v.get('board') or len(v['board']) < 6:
        return None  # preflop or empty board
    # Replace last card if board has 4+ cards (turn or river)
    # OR replace one of flop cards if only 3
    board = v['board']
    # Pick a low brick card (2-6) to swap in if not already present in board/hero
    used = set()
    for i in range(0, len(board), 2):
        used.add(board[i:i+2])
    if v.get('hero_cards'):
        for i in range(0, len(v['hero_cards']), 2):
            used.add(v['hero_cards'][i:i+2])
    # Build candidates
    candidates = [r + s for r in '23456' for s in SUITS if (r + s) not in used]
    if not candidates:
        return None
    new_card = rng.choice(candidates)
    # Replace one card (random non-overcard position)
    if len(board) >= 6:
        # Pick a random position to swap
        positions = list(range(0, len(board), 2))
        pos = rng.choice(positions)
        new_board = board[:pos] + new_card + board[pos+2:]
        v['board'] = new_board
    return v


def make_variant_v3(anchor, rng):
    """V3: Hero kicker rank substitution (within same hand-class tier)."""
    v = copy.deepcopy(anchor)
    if not v.get('hero_cards') or len(v['hero_cards']) != 4:
        return None
    h = v['hero_cards']
    # Substitute the second hero card's rank with a same-tier rank
    r0, s0 = h[0], h[1]
    r1, s1 = h[2], h[3]
    # Avoid creating pairs/sets that change hand class drastically
    tier_swaps = {
        'A': ['K', 'Q'], 'K': ['Q', 'J'], 'Q': ['J', 'T'], 'J': ['T', '9'],
        'T': ['9', '8'], '9': ['8', '7'], '8': ['7', '6'],
        '7': ['6', '5'], '6': ['5', '4'], '5': ['4', '3'],
        '4': ['3', '2'], '3': ['2', '4'], '2': ['3', '4'],
    }
    candidates = tier_swaps.get(r1, ['7'])
    new_r1 = rng.choice(candidates)
    if new_r1 == r0:  # avoid making pocket pair if not already
        return None
    # Also check not in board
    if v.get('board'):
        board_cards = {v['board'][i:i+2] for i in range(0, len(v['board']), 2)}
        if (new_r1 + s1) in board_cards:
            return None
    v['hero_cards'] = r0 + s0 + new_r1 + s1
    return v


def make_variant_v4(anchor, rng):
    """V4: Position rotation (UTG↔EP, HJ↔MP — equivalent ranges)."""
    v = copy.deepcopy(anchor)
    hp = v.get('hero_position', '')
    if hp in POSITION_ROTATIONS and POSITION_ROTATIONS[hp] != hp:
        v['hero_position'] = POSITION_ROTATIONS[hp]
    return v


def make_variant_v5(anchor, rng):
    """V5: Stack-depth variant."""
    v = copy.deepcopy(anchor)
    v['stack_size_bb'] = rng.choice(STACK_VARIANTS)
    return v


def make_variant_v6(anchor, rng):
    """V6: Action-history micro-variant (modify one element)."""
    v = copy.deepcopy(anchor)
    pa = v.get('preflop_action', '')
    if not pa:
        return None
    # Simple variant: swap "calls" → "flats" wording (semantic equivalent)
    # OR add/remove an irrelevant fold mention
    # For deterministic generation, append a "(stack-depth-{N}bb)" marker
    v['preflop_action'] = pa  # no real change for V6; rely on stack variant for differentiation
    # Actually create a more meaningful variant: change a fold-out player
    if 'HJ folds' in pa and 'CO calls' in pa:
        v['preflop_action'] = pa.replace('HJ folds', 'HJ calls').replace('CO calls', 'CO folds')
    return v


VARIANT_FNS = [
    ('v1-suit', make_variant_v1),
    ('v2-brick', make_variant_v2),
    ('v3-kicker', make_variant_v3),
    ('v4-pos', make_variant_v4),
    ('v5-stack', make_variant_v5),
    ('v6-action', make_variant_v6),
]


def generate_variant(anchor, variant_name, fn, rng, attempt=0):
    """Generate a variant; if None or duplicate, return None for caller to retry."""
    if variant_name == 'v1-suit':
        return fn(anchor, rot_idx=attempt)
    return fn(anchor, rng)


def signature(spot):
    """Compute uniqueness signature (cards + board + position + action)."""
    return (
        spot.get('hero_cards'),
        spot.get('board'),
        spot.get('hero_position'),
        spot.get('preflop_action'),
        spot.get('street'),
        spot.get('num_opponents_at_decision'),
    )


def main():
    rng = random.Random(42)
    anchors = load_anchors()
    print(f'[gen] Loaded {len(anchors)} anchors from {len(ANCHOR_FILES)} files')

    # Per-axis target counts
    print(f'[gen] Target per axis: {TARGET_PER_AXIS}')

    # Bucket anchors by axis-family
    anchors_by_axis = defaultdict(list)
    for a in anchors:
        axis = normalize_axis(a.get('axis') or a.get('primary_axis', ''))
        anchors_by_axis[axis].append(a)
    print(f'[gen] Anchors by axis: {dict((k, len(v)) for k,v in anchors_by_axis.items())}')

    # Build seen-signatures set (anchors are already "seen")
    seen = set()
    for a in anchors:
        seen.add(signature(a))

    # Generate variants per axis
    out_rows = []
    spot_counter = 1
    for target_axis, target_count in TARGET_PER_AXIS.items():
        axis_anchors = anchors_by_axis.get(target_axis, [])
        if not axis_anchors:
            print(f'[gen] WARN: no anchors for {target_axis}', file=sys.stderr)
            continue
        n_produced = 0
        rotation_per_anchor = defaultdict(int)
        max_attempts = target_count * 15  # bumped from x3
        attempt_count = 0
        while n_produced < target_count and attempt_count < max_attempts:
            attempt_count += 1
            anchor = axis_anchors[attempt_count % len(axis_anchors)]
            # Apply COMPOUND variants: stack of 1-2 variant fns to expand
            # the unique-signature space substantially.
            n_compound = rng.choice([1, 1, 2, 2, 3])  # most 1-2, some 3-dim
            variant = anchor
            rot_idx = rotation_per_anchor[id(anchor)]
            rotation_per_anchor[id(anchor)] += 1
            for layer in range(n_compound):
                variant_name, fn = rng.choice(VARIANT_FNS)
                v = generate_variant(variant, variant_name, fn, rng, attempt=rot_idx + layer)
                if v is None:
                    continue
                variant = v
            if variant is anchor:  # no variant applied
                continue
            sig = signature(variant)
            if sig in seen:
                continue
            seen.add(sig)
            # Rewrite spot_id
            anchor_id = anchor.get('spot_id', anchor.get('hand_id', f'A{attempt_count}'))
            new_id = f'4WF-{target_axis.upper()[:8]}-{spot_counter:03d}'
            variant['spot_id'] = new_id
            variant['source_anchor'] = anchor.get('spot_id') or anchor.get('hand_id')
            variant['variant_type'] = variant_name
            variant['primary_axis'] = anchor.get('primary_axis', anchor.get('axis', target_axis))
            variant['axis'] = target_axis
            # Drop _source field if present
            variant.pop('_source', None)
            variant.pop('expected_action', None)  # we're labelling fresh
            variant.pop('expected_size_bb', None)
            variant.pop('rationale_summary', None)
            variant.pop('bucket', None)
            out_rows.append(variant)
            spot_counter += 1
            n_produced += 1
        print(f'[gen] {target_axis}: produced {n_produced}/{target_count}')

    # Write output
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w') as f:
        for r in out_rows:
            f.write(json.dumps(r) + '\n')
    print(f'[gen] Wrote {len(out_rows)} lookalikes to {OUTPUT}')

    # Final distribution check
    dist = Counter(r['axis'] for r in out_rows)
    print(f'[gen] Final distribution: {dict(dist)}')
    streets = Counter(r.get('street', 'unknown') for r in out_rows)
    print(f'[gen] Streets: {dict(streets)}')


if __name__ == '__main__':
    main()
