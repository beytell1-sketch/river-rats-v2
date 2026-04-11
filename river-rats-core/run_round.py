#!/usr/bin/env python3
"""Run a round of the self-play oracle tournament.

Usage:
    python3 run_round.py --round 2 --hypotheses ../docs/hypotheses_r2.json --deals 100
    python3 run_round.py --round 1 --deals 100  # defaults to hypotheses.json
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

from self_play import SelfPlayRunner, Variant
from decision_comparator import compare_decisions, format_divergence_report
from convergence_checker import check_convergence, format_convergence_report


def load_previous_result(results_dir, round_id):
    """Load a previous round's result for convergence checking."""
    prev_path = os.path.join(results_dir, f'round_{round_id}.json')
    if not os.path.exists(prev_path):
        return None
    # We need the full RoundResult, not just the JSON summary.
    # For now, convergence check against previous round requires
    # re-running with same seed, which the checker handles via
    # decision comparison. Return None for first-pass.
    return None


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Self-play tournament round")
    parser.add_argument('--round', type=int, required=True, help='Round number')
    parser.add_argument('--hypotheses', type=str, default=None,
                        help='Path to hypotheses JSON (default: docs/hypotheses.json)')
    parser.add_argument('--deals', type=int, default=100,
                        help='Number of deals (default 100)')
    parser.add_argument('--seed', type=int, default=None,
                        help='Random seed (default: round number)')
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else args.round

    # Load hypotheses
    if args.hypotheses:
        hyp_path = args.hypotheses
    else:
        hyp_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'hypotheses.json')

    if not os.path.exists(hyp_path):
        print(f"ERROR: Hypotheses file not found: {hyp_path}")
        sys.exit(1)

    with open(hyp_path) as f:
        hypotheses = json.load(f)

    variants = [Variant.from_hypothesis(h) for h in hypotheses]
    print(f"Round {args.round}: {len(variants)} variants: {[v.name for v in variants]}")

    # Oracle
    oracle_path = os.path.join(os.path.dirname(__file__), 'models', 'gto_model_v8_38feat.json')
    if not os.path.exists(oracle_path):
        print(f"ERROR: Model not found at {oracle_path}")
        sys.exit(1)

    total_games = args.deals * 6 * len(variants)
    print(f"{args.deals} deals × 6 positions × {len(variants)} variants = {total_games} games")
    print(f"Seed: {seed}")
    print()

    runner = SelfPlayRunner(
        variants=variants,
        num_deals=args.deals,
        seed=seed,
        oracle_path=oracle_path,
    )

    start = time.time()
    result = runner.run_round(round_id=args.round)
    elapsed = time.time() - start

    print(f"Completed in {elapsed:.1f}s ({total_games / elapsed:.0f} games/sec)")
    print()

    # Rankings
    ranked = sorted(
        result.variant_results.values(),
        key=lambda vs: vs.mbb_per_hand,
        reverse=True,
    )
    print("=" * 55)
    print(f"{'Variant':<25} {'mbb/hand':>10} {'Games':>8}")
    print("-" * 55)
    for vs in ranked:
        print(f"  {vs.name:<23} {vs.mbb_per_hand:>+10.1f} {vs.num_games:>8}")
    print("=" * 55)

    # Position breakdown for winner
    winner = ranked[0]
    print(f"\nWinner: {winner.name} ({winner.mbb_per_hand:+.1f} mbb/hand)")
    print(f"  By position:")
    for pos in ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']:
        chips = winner.games_by_position.get(pos, [])
        if chips:
            avg = sum(chips) / len(chips) / 10.0 * 1000.0
            print(f"    {pos}: {avg:+.1f} mbb/hand ({len(chips)} games)")

    # Decision comparisons
    print()
    summary = compare_decisions(result.game_results)
    print(format_divergence_report(summary))

    # Convergence
    print()
    conv = check_convergence(result)
    print(format_convergence_report(conv))

    # Save
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    runner.save_results(result, output_dir)
    print(f"\nResults saved to {output_dir}/round_{args.round}.json")


if __name__ == '__main__':
    main()
