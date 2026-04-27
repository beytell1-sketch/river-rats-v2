#!/usr/bin/env python3
"""Workaround driver for Mode A pool generation with multiple hero positions.

Per MAIN_TERMINAL_BUILD_EXECUTE_DIRECTIVE_2026-04-27.md (master `b39126b`)
+ ORCHESTRATION_STATE_2026-04-27.md (master `46818f5`):

  > "Mode A self-play with `single_position='UTG'` yields 0 records (UTG folds
  > preflop). Use CO/BTN/BB. If the script has no `--positions` flag, write a
  > small driver in `scripts/` for that — but flag it for orchestrator review
  > before merging."

`river-rats-core/generate_corpus_revision_pool.py` `_generate_mode_a()` line 90
hardcodes `single_position='UTG'` and has no `--positions` CLI flag. Per the
directive's "Do NOT add the flag yourself; that's a code change requiring its
own review cycle" + "the workaround is to invoke the underlying `generate_pool`
function directly (or write a small driver script in `scripts/`)" — this driver
implements the workaround.

USAGE:
    python3 scripts/run_mode_a_pool_with_positions.py \\
        --positions CO,BTN,BB \\
        --deals 1000 \\
        --seed 20260427 \\
        --output data/corpus_revision_pool_mode_a_2026-04-27.jsonl

MECHANISM:
  Monkey-patches `SelfPlayRunner.__init__` to override the `single_position`
  kwarg per iteration, then calls `_generate_mode_a(...)` from the production
  module 3 times (once per requested position). Forbidden fingerprints are
  threaded across iterations to enforce inter-position disjointness. Combined
  records written to a single JSONL output.

  No production code modified. Production module `generate_corpus_revision_pool`
  imported and used as-is. Patch is module-local to this driver process and
  reverted after final iteration.

REVIEW FLAG:
  This driver is a workaround for a known missing feature (`--positions` flag).
  Orchestrator: please dispatch a code-change PR to add the flag properly,
  after which this driver can be deprecated. This driver IS NOT a permanent
  artifact; it lives only as long as the `--positions` flag is missing.
"""
import argparse
import json
import os
import sys
from typing import List, Set, Tuple

# Make river-rats-core importable
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_BASE, 'river-rats-core'))

import generate_corpus_revision_pool as gcrp
from self_play import SelfPlayRunner


def _patched_runner_init_factory(target_position: str):
    """Return a patched __init__ that overrides single_position kwarg."""
    _orig_init = SelfPlayRunner.__init__

    def _patched_init(self, *args, **kwargs):
        kwargs['single_position'] = target_position
        _orig_init(self, *args, **kwargs)

    return _orig_init, _patched_init


def main():
    parser = argparse.ArgumentParser(
        description='Mode A pool generation with multiple hero positions (workaround)'
    )
    parser.add_argument(
        '--positions', type=str, default='CO,BTN,BB',
        help='Comma-separated hero positions (default: CO,BTN,BB)'
    )
    parser.add_argument(
        '--deals', type=int, default=1000,
        help='Number of self-play deals per position (default: 1000)'
    )
    parser.add_argument(
        '--seed', type=int, default=20260427,
        help='Base RNG seed (each position uses seed + offset)'
    )
    parser.add_argument(
        '--output', type=str,
        default='data/corpus_revision_pool_mode_a_2026-04-27.jsonl',
        help='Combined output JSONL path'
    )
    args = parser.parse_args()

    positions = [p.strip().upper() for p in args.positions.split(',')]
    print(f"[driver] positions: {positions}")
    print(f"[driver] deals/position: {args.deals}")
    print(f"[driver] base seed: {args.seed}")
    print(f"[driver] output: {args.output}")

    forbidden_fingerprints: Set[Tuple] = set()
    all_records: List[dict] = []
    per_position_counts = {}

    for i, pos in enumerate(positions):
        print(f"\n[driver] === Iteration {i+1}/{len(positions)}: position={pos} ===")
        # Patch SelfPlayRunner to override single_position for this iteration
        orig_init, patched_init = _patched_runner_init_factory(pos)
        SelfPlayRunner.__init__ = patched_init
        try:
            records = gcrp._generate_mode_a(
                num_deals=args.deals,
                seed=args.seed + i,  # different seed per position
                forbidden_fingerprints=forbidden_fingerprints,
            )
        finally:
            # Always restore original
            SelfPlayRunner.__init__ = orig_init

        per_position_counts[pos] = len(records)
        all_records.extend(records)
        print(f"[driver]   {pos}: {len(records)} records")

    # Write combined output
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        for r in all_records:
            f.write(json.dumps(r) + '\n')

    # Compute hash for attestation
    import hashlib
    with open(args.output, 'rb') as f:
        sha = hashlib.sha256(f.read()).hexdigest()

    print(f"\n[driver] === Combined output ===")
    print(f"[driver] Per-position counts: {per_position_counts}")
    print(f"[driver] Total records: {len(all_records)}")
    print(f"[driver] Output: {args.output}")
    print(f"[driver] SHA256: {sha}")
    print(f"[driver] Disjointness: {len(forbidden_fingerprints)} unique fingerprints (no within-driver duplicates)")


if __name__ == '__main__':
    main()
