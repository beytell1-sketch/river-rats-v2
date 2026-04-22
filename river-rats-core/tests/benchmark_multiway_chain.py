"""MUST #52 — benchmark multiway chain perf.

Runs N representative multiway hands from v2.3.1 training CSV under both
MULTIWAY_CHAIN_MODE values. Reports median + p95 per-hand
extract_all_features wall time.

Gate decision tree (Q36 resolution):
  - Both modes median < 500ms → ship with 'per_villain' default
  - 'per_villain' 500-750ms AND 'primary_only' < 500ms → orchestrator
    review; likely ship 'per_villain' with perf follow-up
  - 'per_villain' > 750ms → hard fallback: default 'primary_only'; file
    v2.5 ticket for per-villain perf optimisation

Usage:
    python3 river-rats-core/tests/benchmark_multiway_chain.py \\
        [--csv training-data/v2_3_1_training.csv] [--n 100]

MUST #67 (deferred): future version bins results by num_opponents ∈
{2, 3, 4, 5} and trips gate on worst bin.
"""
import argparse
import csv
import os
import statistics
import sys
import time
from pathlib import Path

_CORE = Path(__file__).resolve().parent.parent
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))


def _load_multiway_hands(csv_path: str, n: int) -> list:
    """Sample N multiway hands from v2.3.1 training CSV."""
    if not os.path.exists(csv_path):
        print(f"CSV not found: {csv_path}; using synthetic hands.")
        return _synthetic_multiway_hands(n)

    hands = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                num_opp = int(float(row.get('num_opponents', 1)))
            except (TypeError, ValueError):
                continue
            if num_opp >= 2:
                hands.append(row)
            if len(hands) >= n:
                break
    if not hands:
        print(f"No multiway hands in {csv_path}; using synthetic.")
        return _synthetic_multiway_hands(n)
    return hands


def _synthetic_multiway_hands(n: int) -> list:
    """Fallback when CSV unavailable — synthetic multiway hand payloads."""
    hands = []
    for i in range(n):
        hands.append({
            'h': 'AsKs',
            'b': 'Qh7d2c',
            'pos': 'BTN',
            'vp': 'BB',
            'pot': 90.0,
            'tc': 0.0,
            'st': 'f',
            'fb': 0,
            'exp': 'C',
            '_num_opponents': 2,
            '_opener_position': 'BTN',
            '_action_history': [
                {'street': 'preflop', 'position': 'BTN', 'action': 'RAISE'},
                {'street': 'preflop', 'position': 'CO', 'action': 'CALL'},
                {'street': 'preflop', 'position': 'BB', 'action': 'CALL'},
                {'street': 'flop', 'position': 'BB', 'action': 'CHECK'},
                {'street': 'flop', 'position': 'CO', 'action': 'CHECK'},
            ],
        })
    return hands


def _bench_mode(mode: str, hands: list) -> tuple:
    """Run extract_all_features on every hand under given mode; return (median_ms, p95_ms)."""
    os.environ['MULTIWAY_CHAIN_MODE'] = mode
    # Import inside function so env is read at call time
    from feature_extractor import extract_all_features

    times = []
    errors = 0
    for hand in hands:
        t0 = time.time()
        try:
            extract_all_features(hand)
        except Exception:
            errors += 1
            continue
        times.append(time.time() - t0)

    if not times:
        return (float('nan'), float('nan'), errors)

    times.sort()
    n = len(times)
    median_ms = statistics.median(times) * 1000.0
    p95_idx = min(n - 1, int(n * 0.95))
    p95_ms = times[p95_idx] * 1000.0
    return (median_ms, p95_ms, errors)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', default='training-data/v2_3_1_training.csv')
    parser.add_argument('--n', type=int, default=100)
    args = parser.parse_args()

    hands = _load_multiway_hands(args.csv, args.n)
    print(f"Loaded {len(hands)} multiway hands from {args.csv}")

    results = {}
    for mode in ('per_villain', 'primary_only'):
        median_ms, p95_ms, errors = _bench_mode(mode, hands)
        results[mode] = (median_ms, p95_ms, errors)
        print(f"  {mode:15s}: median={median_ms:.1f}ms  p95={p95_ms:.1f}ms  errors={errors}")

    # Gate evaluation (Q36 resolution)
    pv_median = results['per_villain'][0]
    pv_p95 = results['per_villain'][1]

    print()
    if pv_median < 500.0 and pv_p95 < 750.0:
        print(f"GATE: PASS — 'per_villain' median {pv_median:.1f}ms < 500ms; "
              f"p95 {pv_p95:.1f}ms < 750ms. Ship with per_villain default.")
        return 0
    elif pv_median < 750.0:
        print(f"GATE: REVIEW — 'per_villain' median {pv_median:.1f}ms in "
              f"500-750ms zone. Orchestrator review required; likely ship.")
        return 1
    else:
        print(f"GATE: FALLBACK — 'per_villain' median {pv_median:.1f}ms >= 750ms. "
              f"Hard fallback to 'primary_only' default; v2.5 perf ticket.")
        return 2


if __name__ == '__main__':
    sys.exit(main())
