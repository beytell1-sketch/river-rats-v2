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
    """Sample N multiway hands from v2.3.1 training CSV.

    H3 fix (commit 4.1): parses `_action_history` column (if present) as
    JSON/literal so synthetic benchmark hits the chained code path, not
    the non-chained fallback. Falls back to synthetic when CSV missing
    or lacks action_history column.
    """
    import ast
    import json

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
            if num_opp < 2:
                continue
            # H3: parse _action_history if stringified. Accept both JSON
            # and Python-literal forms (older CSVs may use either).
            ah_raw = row.get('_action_history', '')
            parsed_ah = None
            if isinstance(ah_raw, str) and ah_raw.strip():
                for parser in (json.loads, ast.literal_eval):
                    try:
                        parsed_ah = parser(ah_raw)
                        break
                    except (ValueError, SyntaxError):
                        continue
            if parsed_ah:
                row['_action_history'] = parsed_ah
            else:
                # No parseable action_history; benchmark on this row would
                # measure non-chained path. Skip so the gate tests chained
                # behavior only.
                continue
            hands.append(row)
            if len(hands) >= n:
                break
    if not hands:
        print(f"No chainable multiway hands in {csv_path}; using synthetic.")
        return _synthetic_multiway_hands(n)
    return hands


def _synthetic_multiway_hands(n: int) -> list:
    """Fallback when CSV unavailable — synthetic multiway hand payloads.

    H3 fix (commit 4.1): includes `h` (hero cards) + `b` (board) so
    extract_all_features can build a valid feat_dict. Pre-fix versions
    had only 'h' as 'AsKs' but missing other required keys; all hands
    errored out, producing NaN median.
    """
    hands = []
    for i in range(n):
        hands.append({
            'h': ['As', 'Ks'],
            'b': ['Qh', '7d', '2c'],
            'pos': 'BTN',
            'vp': 'BB',
            'pot': 90.0,
            'tc': 0.0,
            'st': 'f',
            'fb': 0,
            'exp': 'C',
            '_num_opponents': 2,
            '_opener_position': 'BTN',
            '_bettor_position': None,
            '_hero_cards': ['As', 'Ks'],
            '_board_cards': ['Qh', '7d', '2c'],
            '_hero_pos_raw': 'BTN',
            '_villain_pos_raw': 'BB',
            '_street_raw': 'f',
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
        # H3 fix: explicit error state, not NaN that silently compares False
        return (float('inf'), float('inf'), errors)

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

    # Gate evaluation (Q36 resolution). H3 fix: error-rate gate first.
    pv_median, pv_p95, pv_errors = results['per_villain']
    error_rate = pv_errors / len(hands) if hands else 1.0

    print()
    if error_rate > 0.10:
        print(f"GATE: ERROR — per_villain error rate {error_rate:.1%} > 10% "
              f"({pv_errors}/{len(hands)}). Benchmark inconclusive; fix "
              f"extraction errors before gate evaluation.")
        return 3
    # NaN-guard (H3): inf/nan medians signal no successful runs
    if pv_median == float('inf') or pv_median != pv_median:  # NaN check
        print(f"GATE: ERROR — per_villain median is inf/NaN "
              f"(all runs errored). Cannot evaluate gate.")
        return 3
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
