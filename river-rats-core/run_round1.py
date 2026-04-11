#!/usr/bin/env python3
"""Run Round 1 of the self-play oracle tournament.

Loads hypotheses from docs/hypotheses.json, runs the tournament,
saves results, and prints a summary report.

Usage:
    python3 run_round1.py [--deals N] [--seed S]
"""
import json
import os
import sys
import time

# Ensure imports work
sys.path.insert(0, os.path.dirname(__file__))

from self_play import SelfPlayRunner, Variant
from decision_comparator import compare_decisions, format_divergence_report
from convergence_checker import check_convergence, format_convergence_report


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Self-play Round 1")
    parser.add_argument('--deals', type=int, default=100,
                        help='Number of deals per round (default 100)')
    parser.add_argument('--seed', type=int, default=1,
                        help='Random seed (default 1)')
    args = parser.parse_args()

    # Load hypotheses
    hyp_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'hypotheses.json')
    with open(hyp_path) as f:
        hypotheses = json.load(f)

    variants = [Variant.from_hypothesis(h) for h in hypotheses]
    print(f"Loaded {len(variants)} variants: {[v.name for v in variants]}")

    # Oracle path
    oracle_path = os.path.join(os.path.dirname(__file__), 'models', 'gto_model_v8_38feat.json')
    if not os.path.exists(oracle_path):
        print(f"ERROR: Model not found at {oracle_path}")
        sys.exit(1)

    # Run
    total_games = args.deals * 6 * len(variants)
    print(f"\nRunning Round 1: {args.deals} deals × 6 positions × {len(variants)} variants = {total_games} games")
    print(f"Seed: {args.seed}")
    print()

    runner = SelfPlayRunner(
        variants=variants,
        num_deals=args.deals,
        seed=args.seed,
        oracle_path=oracle_path,
    )

    start = time.time()
    result = runner.run_round(round_id=1)
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

    # Convergence (first round — just establishes baseline)
    print()
    conv = check_convergence(result)
    print(format_convergence_report(conv))

    # Save results
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    runner.save_results(result, output_dir)
    print(f"\nResults saved to {output_dir}/round_1.json")


if __name__ == '__main__':
    main()
