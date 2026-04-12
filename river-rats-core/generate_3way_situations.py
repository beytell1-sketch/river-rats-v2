#!/usr/bin/env python3
"""Generate 3-way postflop situations from 6-seated self-play.

All 6 seats use oracle callbacks (no heuristic AI). This produces
realistic preflop ranges and natural multiway pots. Captures 3-way
postflop decisions from ALL players (not just the designated hero),
giving ~5-6x more situations per deal.

The GTO Expert labels situations based on board/ranges/position/pot,
not on what the oracle chose — so every player's perspective is
equally valid training data.

Usage:
    python3 generate_3way_situations.py --deals 3000 --seed 100
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from self_play import SelfPlayRunner, Variant
from multiway_adjuster import get_default_params
from gto_model import FEATURE_COLUMNS


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'training-data')


def _extract_3way_decisions(decisions, deal_id):
    """Extract 3-way postflop decisions from a list of HeroDecision records."""
    situations = []
    for i, dec in enumerate(decisions):
        if dec.is_preflop:
            continue
        if dec.num_opponents != 2:
            continue
        if dec.feat_dict is None:
            continue
        # Oracle can predict FOLD on a check-or-bet street (facing_bet=False).
        # This is a model error — folding for free is illegal in real poker and
        # produces corrupted training data (FOLD with no bet to face). Skip it.
        if dec.oracle_action.upper() == 'FOLD' and not dec.facing_bet:
            continue

        pos = dec.player_position
        prior = []
        for prev in decisions[:i]:
            prior.append(f"{prev.street}: {pos} {prev.action}")

        sit = {
            'situation_id': f"d{deal_id:04d}_{pos}_{dec.street}",
            'deal_id': deal_id,
            'hero_cards': dec.hero_cards,
            'board': dec.board,
            'street': dec.street,
            'hero_position': pos,
            'villain_positions': dec.villain_positions,
            'pot': dec.pot,
            'to_call': dec.to_call,
            'facing_bet': dec.facing_bet,
            'num_opponents': dec.num_opponents,
            'prior_actions': prior,
            'feat_dict': {k: (round(float(v), 6) if isinstance(v, float)
                              else int(v) if isinstance(v, (int, bool))
                              else str(v))
                          for k, v in dec.feat_dict.items()
                          if k in set(FEATURE_COLUMNS)},
            'oracle_action': dec.oracle_action.upper(),
            'adjusted_action': dec.action.upper(),
            'equity': round(dec.equity, 4),
        }
        situations.append(sit)
    return situations


def generate_situations(num_deals: int, seed: int, output_path: str):
    """Run all-oracle self-play and extract 3-way postflop decisions."""

    print(f"Running self-play: {num_deals} deals, seed={seed}")
    print(f"  All 6 seats use oracle callbacks (all-player logging)")
    variant = Variant("baseline", get_default_params())
    runner = SelfPlayRunner([variant], num_deals=num_deals, seed=seed,
                            log_all_multiway=True, single_position='UTG')
    result = runner.run_round(round_id=1)

    print(f"  Total games: {result.num_games}")

    # Extract 3-way postflop decisions from hero AND all other players.
    # Each opponent has its own decision list (keyed by position) so
    # prior_actions are per-player, not cross-contaminated.
    situations = []
    seen_ids = set()
    for game in result.game_results:
        # Hero decisions
        for sit in _extract_3way_decisions(game.hero_decisions, game.deal_id):
            if sit['situation_id'] not in seen_ids:
                seen_ids.add(sit['situation_id'])
                situations.append(sit)

        # Per-opponent decisions (when log_all_multiway=True)
        for pos, dec_list in game.opponent_decisions.items():
            for sit in _extract_3way_decisions(dec_list, game.deal_id):
                if sit['situation_id'] not in seen_ids:
                    seen_ids.add(sit['situation_id'])
                    situations.append(sit)

    # Stratification report
    by_street = {}
    by_position = {}
    by_facing = {'facing_bet': 0, 'not_facing': 0}
    by_action = {}
    for s in situations:
        by_street[s['street']] = by_street.get(s['street'], 0) + 1
        pos_type = 'IP' if s['feat_dict'].get('is_ip', 0) > 0.5 else 'OOP'
        by_position[pos_type] = by_position.get(pos_type, 0) + 1
        if s['facing_bet']:
            by_facing['facing_bet'] += 1
        else:
            by_facing['not_facing'] += 1
        a = s['oracle_action']
        by_action[a] = by_action.get(a, 0) + 1

    print(f"\n  3-way postflop decisions: {len(situations)}")
    print(f"  By street: {by_street}")
    print(f"  By position: {by_position}")
    print(f"  Facing bet: {by_facing}")
    print(f"  Oracle action distribution: {by_action}")
    print(f"  Yield: {len(situations)}/{result.num_games} = "
          f"{100*len(situations)/result.num_games:.2f}% of games")

    # Write JSONL
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        for sit in situations:
            f.write(json.dumps(sit) + '\n')

    print(f"\n  Written to: {output_path}")
    return situations


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate 3-way situations')
    parser.add_argument('--deals', type=int, default=3000)
    parser.add_argument('--seed', type=int, default=100)
    parser.add_argument('--output', type=str,
                        default=os.path.join(OUTPUT_DIR, '3way_situations.jsonl'))
    args = parser.parse_args()

    generate_situations(args.deals, args.seed, args.output)
