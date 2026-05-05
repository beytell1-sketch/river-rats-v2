#!/usr/bin/env python3
"""Phase 12.5H-pre cross-seed feature-importance extractor.

Per `MAIN_TERMINAL_PHASE125H_PRE_CROSSSEED_2026-05-05.md` (PR #160,
master `2c52e6b`): the existing 12.5E-E + 12.5G trainer reports only
expose CHOSEN-SEED feature importance. To answer "was the 12.5E-E
H-FEAT validation real or single-seed noise?" we need cross-seed
importances for all 5 seeds × both cap configurations (3.0, 4.0) ⇒
10 data points.

Approach (Path 2 per dispatch §"Step 1"): re-uses the trainer's
`train_one_seed` helper directly via Python import, iterates seeds
0-4 × caps {3.0, 4.0}, captures `feature_importances_` per seed,
serializes a JSON for the analysis report.

This is **analysis-only**: no model artifacts written, no corpus
modified, no `river-rats-core/` files touched. Re-uses the existing
trainer module at master HEAD verbatim.

Cost: ~10-15 min runtime (10 train_one_seed calls × ~1 min each on
604-hand corpus). $0 API. xgboost BLAS non-determinism means re-runs
yield slightly different per-seed numbers (~±5-10% on importances)
but cross-seed pattern is stable.

Usage:
    python3 scripts/extract_cross_seed_importance.py \\
        --corpus data/corpus_combined_604_2026-05-05.jsonl \\
        --labels data/corpus_combined_604_labels_2026-05-05.jsonl \\
        --output /tmp/cross_seed_importance.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from typing import Any, Dict, List

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CORE = os.path.join(_REPO, "river-rats-core")
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

# Re-use trainer's helpers (no modification — analysis-only).
from train_model_v9_student import (  # noqa: E402
    _HYPERPARAMETERS,
    STUDENT_FEATURE_COLUMNS_V9,
    _V24_P1_BLOCKERS,
    join_on_ref_id,
    load_corpus,
    load_labels,
    prepad_baseline_booster,
    resolve_warm_start_anchor,
    train_one_seed,
)

import numpy as np  # noqa: E402


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Phase 12.5H-pre cross-seed feature-importance extractor"
    )
    p.add_argument("--corpus", required=True, help="Combined 604-hand corpus path")
    p.add_argument("--labels", required=True, help="Combined 604-hand labels path")
    p.add_argument(
        "--warm-start",
        default=os.path.join(_REPO, "river-rats-core/models/gto_model_v9_3way_v2.2.json"),
        help="Warm-start anchor path",
    )
    p.add_argument("--seeds", type=str, default="0,1,2,3,4")
    p.add_argument("--caps", type=str, default="3.0,4.0",
        help="Comma-separated cap values to sweep (default: 3.0,4.0 for "
             "12.5E-E + 12.5G coverage)")
    p.add_argument("--test-size", type=float, default=0.20)
    p.add_argument("--output", required=True,
        help="Output JSON path with per-seed × per-cap importances")
    args = p.parse_args(argv)

    corpus = load_corpus(args.corpus)
    labels = load_labels(args.labels)
    X, y, sw, ids = join_on_ref_id(corpus, labels)
    print(f"[xs] joined {len(ids)} rows; class distribution: "
          f"{dict(zip(*np.unique(y, return_counts=True)))}", file=sys.stderr)

    warm_start_anchor, _ = resolve_warm_start_anchor(args.warm_start)
    print(f"[xs] warm-start anchor: {warm_start_anchor}", file=sys.stderr)

    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    caps = [float(c) for c in args.caps.split(",") if c.strip()]

    # Pre-pad warm-start anchor (one tmp file per cap reuse since pre-pad
    # is cap-independent).
    padded_path = prepad_baseline_booster(warm_start_anchor, target_n_features=59)

    results: List[Dict[str, Any]] = []
    try:
        for cap in caps:
            for seed in seeds:
                print(f"[xs] cap={cap} seed={seed} training ...", file=sys.stderr)
                clf, sr = train_one_seed(
                    X, y, sw,
                    seed=seed,
                    test_size=args.test_size,
                    warm_start_padded_path=padded_path,
                    hyperparameters=_HYPERPARAMETERS,
                    class_weight_cap=cap,
                    verbose=False,
                )
                # feature_importances_ is in the same column order as
                # STUDENT_FEATURE_COLUMNS_V9 (the trainer fits on X = 59-col
                # ndarray built from STUDENT_FEATURE_COLUMNS_V9 via
                # join_on_ref_id).
                importances = clf.feature_importances_
                imp_by_name = {
                    name: float(importances[i])
                    for i, name in enumerate(STUDENT_FEATURE_COLUMNS_V9)
                }
                row = {
                    "cap": cap,
                    "seed": seed,
                    "n_boosted_rounds": int(sr.n_boosted_rounds),
                    "held_out_accuracy": float(sr.held_out_metrics["accuracy"]),
                    "p1_blocker_importance": {
                        b: imp_by_name[b] for b in _V24_P1_BLOCKERS
                    },
                    "all_importance": imp_by_name,
                }
                results.append(row)
                # Cleanup per-seed temp model artifact (we don't need it).
                try:
                    os.unlink(sr.model_temp_path)
                except OSError:
                    pass
                print(
                    f"[xs] cap={cap} seed={seed} "
                    f"nut_flush_block={imp_by_name['nut_flush_block']:.4f} "
                    f"flush_draw_block_pct={imp_by_name['flush_draw_block_pct']:.4f} "
                    f"acc={sr.held_out_metrics['accuracy']:.4f}",
                    file=sys.stderr,
                )
    finally:
        try:
            os.unlink(padded_path)
        except OSError:
            pass

    # Cross-seed aggregation per cap + combined
    def _stats(values: List[float]) -> Dict[str, float]:
        arr = np.array(values, dtype=np.float64)
        return {
            "median": float(np.median(arr)),
            "mean": float(np.mean(arr)),
            "std": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "n": len(arr),
            "pct_ge_002": float(100.0 * np.mean(arr >= 0.02)),
        }

    per_cap_summary: Dict[str, Dict[str, Dict[str, float]]] = {}
    for cap in caps:
        per_cap_summary[str(cap)] = {}
        for blocker in _V24_P1_BLOCKERS:
            vals = [r["p1_blocker_importance"][blocker]
                    for r in results if r["cap"] == cap]
            per_cap_summary[str(cap)][blocker] = _stats(vals)

    combined_summary: Dict[str, Dict[str, float]] = {}
    for blocker in _V24_P1_BLOCKERS:
        vals = [r["p1_blocker_importance"][blocker] for r in results]
        combined_summary[blocker] = _stats(vals)

    output = {
        "schema_version": "12.5H-pre-v1",
        "corpus": args.corpus,
        "labels": args.labels,
        "n_rows_joined": len(ids),
        "warm_start_anchor": warm_start_anchor,
        "hyperparameters": {k: v for k, v in _HYPERPARAMETERS.items()},
        "seeds_swept": seeds,
        "caps_swept": caps,
        "per_seed_results": results,
        "per_cap_summary": per_cap_summary,
        "combined_summary_10_seeds": combined_summary,
    }
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)
    print(f"[xs] wrote {args.output}", file=sys.stderr)

    # Quick console verdict
    nfb = combined_summary["nut_flush_block"]
    print(f"\n[xs] nut_flush_block cross-{nfb['n']}-seed: "
          f"median={nfb['median']:.4f} mean={nfb['mean']:.4f} "
          f"std={nfb['std']:.4f} range=[{nfb['min']:.4f}, {nfb['max']:.4f}] "
          f"pct_ge_0.02={nfb['pct_ge_002']:.0f}%", file=sys.stderr)
    if nfb["median"] >= 0.02:
        print("[xs] H-FEAT VERDICT: VALIDATED (cross-seed median ≥ 0.02)",
              file=sys.stderr)
    elif nfb["max"] >= 0.02:
        print("[xs] H-FEAT VERDICT: MARGINAL (median < 0.02 but max ≥ 0.02)",
              file=sys.stderr)
    else:
        print("[xs] H-FEAT VERDICT: NOT VALIDATED (max < 0.02)",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
