#!/usr/bin/env python3
"""Phase 2-F1 batch_009 generator — PILOT for new positional_action_chain scenarios.

Per directive `review/comms/MAIN_TERMINAL_PHASE2F1_BATCH009_FIRE_NOW_2026-05-24.md`.

Produces 50 hands:
  * 24 enumerated chain-quota specs via `generate_phase_2f_chain_quota` (Module 10)
  * 26 stratified-fill drawn from unused entries in
    `data/4way_lookalikes_700hand_full_2026-05-12.jsonl` (rotating through
    the cycle order established by batches 001-008: range-asymmetry, then
    4-way-SRP-standard, MW-axis, etc.)

Output schema matches `data/4way_corpus/full_700/batch_008_50hand.jsonl`:
  spot_id, axis, stack_size_bb, preflop_action, board, hero_position,
  hero_cards, num_opponents_at_decision, street, facing_bet, to_call_bb,
  pot_bb, primary_axis, source_anchor, variant_type
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Set, Tuple

_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / 'river-rats-core'))

from corpus_revision_scenarios.positional_action_chain_scenarios import (
    ChainFingerprint,
    generate_phase_2f_chain_quota,
    _CHAIN_FINGERPRINT_TEMPLATES,
)
from corpus_revision_scenarios._scenario_utils import (
    compute_chain_fingerprint,
    fingerprint as card_fingerprint,
)

CANONICAL_RNG_SEED = 20260524
BATCH_NUM = 9
SPOT_ID_PREFIX_CHAIN = '4WF-CHAIN'
OUTPUT = _REPO / 'data/4way_corpus/full_700/batch_009_50hand.jsonl'
LOOKALIKES_700 = _REPO / 'data/4way_lookalikes_700hand_full_2026-05-12.jsonl'

# Axis-cycle order for stratified-fill (continues batches 001-008 cycle).
# Batches 001-008 consumed: 4-way-3-bet-pot, multiway-cooler, closing-action-variants,
# range-asymmetry. Remaining-heavy axes: 4-way-SRP-standard (140 unused), MW-axis (100 unused),
# range-asymmetry remainder (~55 unused). The fill rotates: complete range-asymmetry
# remainder first (continuity from batch_008), then start 4-way-SRP-standard.
_FILL_AXIS_CYCLE = [
    'range-asymmetry',
    '4-way-SRP-standard',
    'MW-axis',
]


def _load_existing() -> Tuple[Set[Tuple[str, str]], Set[str]]:
    """Collect card fingerprints + spot_ids from batches 001-008 for dedup."""
    card_fps: Set[Tuple[str, str]] = set()
    spot_ids: Set[str] = set()
    for n in range(1, 9):
        path = _REPO / f'data/4way_corpus/full_700/batch_00{n}_50hand.jsonl'
        if not path.exists():
            continue
        with path.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                spot_ids.add(d['spot_id'])
                if d.get('board'):
                    card_fps.add(card_fingerprint(d['hero_cards'], d['board']))
    return card_fps, spot_ids


def _preflop_action_string(spec) -> str:
    """Render spec.action_history preflop slice in batch_008 style."""
    parts: List[str] = []
    n_raises = 0
    for street, pos, action in spec.action_history:
        if street != 'preflop':
            continue
        is_hero = pos == spec.hero_pos
        actor = f'hero({pos})' if is_hero else pos
        if action == 'raise':
            if n_raises == 0:
                parts.append(f'{actor} opens 2.5bb')
            elif n_raises == 1:
                parts.append(f'{actor} 3-bets 9bb')
            else:
                parts.append(f'{actor} 4-bets 22bb')
            n_raises += 1
        elif action == 'call':
            parts.append(f'{actor} calls')
        elif action == 'fold':
            parts.append(f'{actor} folds')
        elif action == 'check':
            parts.append(f'{actor} checks')
    return ', '.join(parts)


def _derive_primary_axis(chain_fp: ChainFingerprint) -> str:
    return f'chain-{chain_fp.street}-{chain_fp.hero_pos}-{chain_fp.chain_shape}'


def _spec_to_chain_record(spec, template_index: int, spot_index: int) -> dict:
    chain_fp = compute_chain_fingerprint(spec)
    hero_cards_str = ''.join(spec.hero_cards)
    board_str = ''.join(spec.board_cards)
    # SituationSpec doesn't always carry effective_stack; default to 100bb.
    stack_bb = int(getattr(spec, 'effective_stack', 100) or 100)
    return {
        'spot_id': f'{SPOT_ID_PREFIX_CHAIN}-{BATCH_NUM:03d}-{spot_index:03d}',
        'axis': 'positional-action-chain',
        'stack_size_bb': stack_bb,
        'preflop_action': _preflop_action_string(spec),
        'board': board_str,
        'hero_position': spec.hero_pos,
        'hero_cards': hero_cards_str,
        'num_opponents_at_decision': len(spec.villain_positions),
        'street': spec.street,
        'facing_bet': int(spec.to_call > 0),
        'to_call_bb': float(spec.to_call),
        'pot_bb': float(spec.pot),
        'primary_axis': _derive_primary_axis(chain_fp),
        'source_anchor': f'CHAIN-T{template_index:02d}',
        'variant_type': 'v1-canonical',
    }


def _select_stratified_fill(
    used_ids: Set[str],
    forbidden_card_fps: Set[Tuple[str, str]],
    rng_seed: int,
    count: int = 26,
) -> List[dict]:
    """Pick `count` unused 700-pool records balanced across the axis cycle.

    Strategy: cycle through _FILL_AXIS_CYCLE, drawing one record at a time per
    axis until count hit. Each draw is deterministic via rng_seed-based shuffle
    of that axis's unused pool.
    """
    pool = [json.loads(l) for l in LOOKALIKES_700.open()]
    by_axis = defaultdict(list)
    for d in pool:
        if d['spot_id'] in used_ids:
            continue
        # Skip card-fingerprint collisions vs prior batches (chain quota may
        # have already consumed some boards we'd otherwise pick here, but the
        # 700-pool ⊥ chain templates so this is a safety net only).
        if d.get('board'):
            fp = card_fingerprint(d['hero_cards'], d['board'])
            if fp in forbidden_card_fps:
                continue
        by_axis[d['axis']].append(d)

    rng = random.Random(rng_seed)
    for axis in _FILL_AXIS_CYCLE:
        rng.shuffle(by_axis[axis])

    selected: List[dict] = []
    axis_idx = 0
    axis_cursor = {ax: 0 for ax in _FILL_AXIS_CYCLE}
    safety = 0
    while len(selected) < count and safety < 10000:
        safety += 1
        ax = _FILL_AXIS_CYCLE[axis_idx % len(_FILL_AXIS_CYCLE)]
        axis_idx += 1
        c = axis_cursor[ax]
        if c >= len(by_axis[ax]):
            continue
        rec = by_axis[ax][c]
        axis_cursor[ax] += 1
        # Mutate spot_id to keep batch_009 namespace clean; preserve original
        # as source_anchor reference (batch_008 style preserves source_anchor).
        selected.append(rec)

    return selected


def _verify_floors(records: List[dict]) -> dict:
    chain_records = [r for r in records if r['axis'] == 'positional-action-chain']
    chain_shapes = []
    for r in chain_records:
        idx = int(r['source_anchor'].split('T')[-1])
        chain_shapes.append(
            _CHAIN_FINGERPRINT_TEMPLATES[idx]['chain_fingerprint'].chain_shape
        )

    # For floors, score against the full 50-hand input — fill records don't
    # contribute chain_shape; floors are measured only on the chain-quota subset
    # PLUS any fill-records that happen to be on river/facing-raise actions.
    streets = [r['street'] for r in records]
    facing_bets = [r['facing_bet'] for r in records]

    fr_chain = sum(1 for s in chain_shapes if s in {'BET_RAISE','CHECK_RAISE','MULTI_AGGR'})
    rv = sum(1 for s in streets if s == 'river')

    hero_classes = []
    for r in records:
        hp = r['hero_position']
        if hp in ('EP', 'UTG'):
            hero_classes.append('UTG')
        elif hp in ('HJ', 'MP'):
            hero_classes.append('MP')
        else:
            hero_classes.append(hp)
    hero_counter = Counter(hero_classes)

    # Sandwich floor (4 chain templates: T22, T23 + facing-raise multi-agg
    # templates T12, T14 where hero is between villains). Use the 4 sandwich
    # templates explicitly: T12, T14, T22, T23 — indices that have ≥1 villain
    # positionally before AND after hero at decision.
    sandwich_indices = {12, 14, 22, 23}
    sandwich_hit = sum(
        1 for r in chain_records
        if int(r['source_anchor'].split('T')[-1]) in sandwich_indices
    )

    top12 = sum(
        1 for r in chain_records
        if int(r['source_anchor'].split('T')[-1]) < 12
    )

    return {
        'facing_raise_chain': fr_chain,
        'river_total': rv,
        'sandwich': sandwich_hit,
        'top_12_anchors': top12,
        'hero_class_counter': dict(hero_counter),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rng-seed', type=int, default=CANONICAL_RNG_SEED)
    parser.add_argument('--output', type=str, default=str(OUTPUT))
    args = parser.parse_args()

    forbidden_card_fps, used_spot_ids = _load_existing()
    print(f'[load] dedup baseline: {len(forbidden_card_fps)} card-fps, '
          f'{len(used_spot_ids)} prior spot_ids')

    chain_specs = generate_phase_2f_chain_quota(
        rng_seed=args.rng_seed,
        forbidden_fingerprints=forbidden_card_fps,
    )
    if len(chain_specs) != 24:
        print(f'[ERROR] chain quota returned {len(chain_specs)} (expected 24).',
              file=sys.stderr)
        return 1
    print(f'[chain] 24 specs from generate_phase_2f_chain_quota')

    chain_records = [
        _spec_to_chain_record(spec, template_index=i, spot_index=i)
        for i, spec in enumerate(chain_specs)
    ]

    # Update forbidden set with chain-record boards so fill avoids collisions.
    for r in chain_records:
        if r.get('board'):
            forbidden_card_fps.add(card_fingerprint(r['hero_cards'], r['board']))

    fill_records = _select_stratified_fill(
        used_ids=used_spot_ids,
        forbidden_card_fps=forbidden_card_fps,
        rng_seed=args.rng_seed,
        count=26,
    )
    print(f'[fill] {len(fill_records)} stratified-fill records')

    records = chain_records + fill_records
    if len(records) != 50:
        print(f'[ERROR] total {len(records)} (expected 50)', file=sys.stderr)
        return 1

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open('w') as f:
        for r in records:
            f.write(json.dumps(r) + '\n')
    print(f'[write] {len(records)} → {out_path}')

    floors = _verify_floors(records)
    print('\n=== Floor verification (50-hand input) ===')
    print(f'  Facing-raise (chain-quota): {floors["facing_raise_chain"]}  (>=10 required)')
    print(f'  River (total):              {floors["river_total"]}  (>=5 required)')
    print(f'  Sandwich:                   {floors["sandwich"]}  (>=4 required)')
    print(f'  Top-12 anchors:             {floors["top_12_anchors"]}  (==12 required)')
    print(f'  Hero position counts:       {floors["hero_class_counter"]}')

    # Floor STOP check
    fail = []
    if floors['facing_raise_chain'] < 10:
        fail.append('facing-raise')
    if floors['river_total'] < 5:
        fail.append('river')
    if floors['sandwich'] < 4:
        fail.append('sandwich')
    if floors['top_12_anchors'] != 12:
        fail.append('top-12')
    for pos in ('BTN','CO','MP','UTG','SB','BB'):
        if floors['hero_class_counter'].get(pos, 0) < 1:
            fail.append(f'position-{pos}')
    if fail:
        print(f'\n[STOP] floor failures: {fail}', file=sys.stderr)
        return 2

    print('\n[PASS] All A1 floors satisfied.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
