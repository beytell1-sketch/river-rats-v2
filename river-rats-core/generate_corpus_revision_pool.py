#!/usr/bin/env python3
"""Generate the ~2450-hand candidate pool for the 500-hand corpus revision.

Two modes:
  Mode A: All-oracle self-play with SPR fix and PFA capture.
           Converts pot from chip units to BB units (BB_CHIP_SIZE=10)
           and records opener_position per situation.
  Mode B: SituationFactory scenario expansion across 9 scenario families.
           Each family's generate_scenarios() receives the incrementally-
           updated forbidden_fingerprints set so no cross-family duplicates.

Blueprint v3 Q6 spec. Do NOT modify generate_3way_situations.py.

Usage:
    python3 generate_corpus_revision_pool.py --mode a --deals 1000 --seed 20260427
    python3 generate_corpus_revision_pool.py --mode b
    python3 generate_corpus_revision_pool.py --mode both --deals 1000 --seed 20260427

Output:
    training-data/corpus_revision_pool_2026-04-27.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Set, Tuple

# Ensure river-rats-core is importable
_CORE = os.path.dirname(os.path.abspath(__file__))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

# Chip-to-BB conversion constant (poker_game.py BIG_BLIND=10)
BB_CHIP_SIZE = 10

OUTPUT_DIR = os.path.join(_CORE, '..', 'training-data')
DEFAULT_OUTPUT = os.path.join(OUTPUT_DIR, 'corpus_revision_pool_2026-04-27.jsonl')


# ---------------------------------------------------------------------------
# Fingerprint helpers
# ---------------------------------------------------------------------------

def _fp(hero_cards_str: str, board_str: str) -> Tuple[str, str]:
    """Return a canonical fingerprint for deduplication."""
    hero = tuple(sorted(hero_cards_str[i:i+2] for i in range(0, len(hero_cards_str), 2)))
    board = tuple(sorted(board_str[i:i+2] for i in range(0, len(board_str), 2)))
    return (hero, board)


def _fp_from_record(rec: Dict[str, Any]) -> Tuple[str, str]:
    """Fingerprint a pool record dict."""
    hero_str = ''.join(rec['hero_cards']) if isinstance(rec['hero_cards'], list) else rec['hero_cards']
    board_str = ''.join(rec['board']) if isinstance(rec['board'], list) else rec['board']
    return _fp(hero_str, board_str)


# ---------------------------------------------------------------------------
# Mode A: Self-play with SPR fix and PFA capture
# ---------------------------------------------------------------------------

def _generate_mode_a(
    num_deals: int,
    seed: int,
    forbidden_fingerprints: Set[Tuple],
) -> List[Dict[str, Any]]:
    """Run all-oracle self-play and return corrected situation records.

    Key differences from generate_3way_situations.py:
    - pot stored in BB units (not chip units): pot_bb = pot_chips / BB_CHIP_SIZE
    - opener_position captured from game.opener_position per decision
    - 59-feature re-extraction with corrected pot and _opener_position
    - generation_source = 'self_play_v2'
    """
    from self_play import SelfPlayRunner, Variant
    from multiway_adjuster import get_default_params
    from gto_model import FEATURE_COLUMNS
    from feature_extractor import extract_all_features
    from feature_keys import F

    V24_P1_BLOCKERS = [F.NUT_FLUSH_BLOCK, F.FLUSH_DRAW_BLOCK_PCT,
                       F.STRAIGHT_DRAW_BLOCK_PCT, F.NUT_MADE_BLOCK_PCT]
    ALL_59_KEYS = set(FEATURE_COLUMNS) | set(V24_P1_BLOCKERS)

    print(f"[Mode A] Running self-play: {num_deals} deals, seed={seed}")
    variant = Variant("baseline", get_default_params())
    runner = SelfPlayRunner([variant], num_deals=num_deals, seed=seed,
                            log_all_multiway=True, single_position='UTG')
    result = runner.run_round(round_id=1)
    print(f"[Mode A]   Total games: {result.num_games}")

    records: List[Dict[str, Any]] = []
    seen_ids: Set[str] = set()

    def _process_decisions(decisions, deal_id):
        for i, dec in enumerate(decisions):
            if dec.is_preflop:
                continue
            if dec.num_opponents != 2:
                continue
            if dec.feat_dict is None:
                continue
            if dec.oracle_action.upper() == 'FOLD' and not dec.facing_bet:
                continue

            pos = dec.player_position
            sit_id = f"d{deal_id:04d}_{pos}_{dec.street}_v2"
            if sit_id in seen_ids:
                continue

            # --- SPR fix: convert chip-unit pot to BB units ---
            pot_bb = round(dec.pot / BB_CHIP_SIZE, 4)
            to_call_bb = round(dec.to_call / BB_CHIP_SIZE, 4)

            # --- PFA capture: opener_position from game context ---
            # dec.feat_dict is the 45-feature dict from game time;
            # opener_position may be in feat_dict metadata fields.
            opener_pos = dec.feat_dict.get('_opener_position') or dec.feat_dict.get('opener_position')

            # Build prior_actions for this player
            prior = []
            for prev in decisions[:i]:
                prior.append(f"{prev.street}: {pos} {prev.action}")

            # Build hand dict for 59-feature re-extraction with corrected inputs
            hand_dict = {
                'hero_cards': dec.hero_cards,
                'board': dec.board,
                'street': dec.street,
                'hero_position': pos,
                'villain_positions': dec.villain_positions,
                'pot': pot_bb,           # BB units — fixes SPR bug
                'to_call': to_call_bb,
                'facing_bet': dec.facing_bet,
                'num_opponents': dec.num_opponents,
                'prior_actions': prior,
                '_opener_position': opener_pos,  # fixes IS_PFA bug
                '_is_3bet_pot': int(dec.feat_dict.get('is_3bet_pot', 0)),
                'action_history': [],    # not available in this path
            }

            try:
                feat_59 = extract_all_features(hand_dict)
                feat_dict = {k: v for k, v in feat_59.items() if k in ALL_59_KEYS}
            except Exception:
                # Fall back to original 45-feature dict if re-extraction fails
                feat_dict = {k: v for k, v in dec.feat_dict.items()
                             if k in set(FEATURE_COLUMNS)}

            fp = _fp(''.join(dec.hero_cards), ''.join(dec.board))
            if fp in forbidden_fingerprints:
                continue

            rec = {
                'situation_id': sit_id,
                'deal_id': deal_id,
                'hero_cards': dec.hero_cards,
                'board': dec.board,
                'street': dec.street,
                'hero_position': pos,
                'villain_positions': dec.villain_positions,
                'pot': pot_bb,
                'to_call': to_call_bb,
                'facing_bet': dec.facing_bet,
                'num_opponents': dec.num_opponents,
                'prior_actions': prior,
                'feat_dict': feat_dict,
                'oracle_action': dec.oracle_action.upper(),
                'adjusted_action': dec.action.upper(),
                'equity': round(dec.equity, 4),
                'generation_source': 'self_play_v2',
                'opener_position': opener_pos,
            }
            seen_ids.add(sit_id)
            records.append(rec)
            forbidden_fingerprints.add(fp)

    for game in result.game_results:
        _process_decisions(game.hero_decisions, game.deal_id)
        for pos, dec_list in game.opponent_decisions.items():
            _process_decisions(dec_list, game.deal_id)

    print(f"[Mode A]   Situations produced: {len(records)}")
    return records


# ---------------------------------------------------------------------------
# Mode B: SituationFactory scenario expansion (9 families)
# ---------------------------------------------------------------------------

def _generate_mode_b(forbidden_fingerprints: Set[Tuple]) -> List[Dict[str, Any]]:
    """Generate factory scenarios across all 9 families.

    Forbidden fingerprints are threaded incrementally so that each family
    can see the fingerprints already committed by prior families.
    """
    from corpus_revision_scenarios.pfa_scenarios import (
        generate_scenarios as gen_pfa)
    from corpus_revision_scenarios.facing_initial_bet_scenarios import (
        generate_scenarios as gen_fib)
    from corpus_revision_scenarios.bac_scenarios import (
        generate_scenarios as gen_bac)
    from corpus_revision_scenarios.magg_scenarios import (
        generate_scenarios as gen_magg)
    from corpus_revision_scenarios.nfd_scenarios import (
        generate_scenarios as gen_nfd)
    from corpus_revision_scenarios.monster_facing_bet_scenarios import (
        generate_scenarios as gen_monster)
    from corpus_revision_scenarios.rule11_boundary_scenarios import (
        generate_scenarios as gen_rule11)
    from corpus_revision_scenarios.donk_bet_defence_scenarios import (
        generate_scenarios as gen_donk)
    from corpus_revision_scenarios.sb_hero_scenarios import (
        generate_scenarios as gen_sb)

    all_records: List[Dict[str, Any]] = []

    families = [
        ('pfa', gen_pfa),
        ('facing_initial_bet', gen_fib),
        ('bac', gen_bac),
        ('magg', gen_magg),
        ('nfd', gen_nfd),
        ('monster_facing_bet', gen_monster),
        ('rule11_boundary', gen_rule11),
        ('donk_bet_defence', gen_donk),
        ('sb_hero', gen_sb),
    ]

    for name, gen_fn in families:
        before = len(all_records)
        new_records = gen_fn(forbidden_fingerprints=forbidden_fingerprints)
        # Update forbidden_fingerprints incrementally
        for rec in new_records:
            fp = _fp_from_record(rec)
            forbidden_fingerprints.add(fp)
        all_records.extend(new_records)
        print(f"[Mode B]   {name}: {len(new_records)} records "
              f"(total so far: {len(all_records)})")

    return all_records


# ---------------------------------------------------------------------------
# Public entry point: generate_pool()
# ---------------------------------------------------------------------------

def generate_pool(
    mode: str = 'both',
    num_deals: int = 1000,
    seed: int = 20260427,
    output_path: str = DEFAULT_OUTPUT,
    forbidden_fingerprints: Set[Tuple] | None = None,
    write_output: bool = True,
) -> List[Dict[str, Any]]:
    """Generate the candidate pool for corpus revision.

    Args:
        mode: 'a' (self-play only), 'b' (factory only), or 'both'.
        num_deals: Number of self-play deals to run (Mode A only).
        seed: RNG seed for self-play (Mode A only).
        output_path: Where to write the JSONL pool file.
        forbidden_fingerprints: External fingerprint set to exclude.
            Updated in-place as records are generated.
        write_output: If True, write pool to output_path.

    Returns:
        List of pool record dicts.
    """
    if forbidden_fingerprints is None:
        forbidden_fingerprints = set()

    all_records: List[Dict[str, Any]] = []

    if mode in ('a', 'both'):
        mode_a_records = _generate_mode_a(num_deals, seed, forbidden_fingerprints)
        all_records.extend(mode_a_records)
        print(f"[Pool] Mode A complete: {len(mode_a_records)} records")

    if mode in ('b', 'both'):
        mode_b_records = _generate_mode_b(forbidden_fingerprints)
        all_records.extend(mode_b_records)
        print(f"[Pool] Mode B complete: {len(mode_b_records)} records")

    print(f"[Pool] Total candidate pool: {len(all_records)} records")

    if write_output and output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, 'w') as f:
            for rec in all_records:
                f.write(json.dumps(rec) + '\n')
        print(f"[Pool] Written to: {output_path}")

    return all_records


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description='Generate corpus revision candidate pool (~2450 hands).'
    )
    p.add_argument('--mode', choices=['a', 'b', 'both'], default='both',
                   help='Generation mode: a=self-play, b=factory, both=combined')
    p.add_argument('--deals', type=int, default=1000,
                   help='Number of self-play deals (Mode A; default 1000)')
    p.add_argument('--seed', type=int, default=20260427,
                   help='RNG seed for self-play (default 20260427)')
    p.add_argument('--output', default=DEFAULT_OUTPUT,
                   help='Output JSONL path')
    return p


if __name__ == '__main__':
    args = _build_parser().parse_args()
    generate_pool(
        mode=args.mode,
        num_deals=args.deals,
        seed=args.seed,
        output_path=args.output,
    )
