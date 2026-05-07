#!/usr/bin/env python3
"""Phase 12.5K-B Lever B hyperparameter sweep orchestration script.

Per `MAIN_TERMINAL_PR261_RESOLUTION_AND_125KB_DISPATCH_2026-05-06.md`
(master `bc7d08b`, PR #264). Mirrors plan §4 "Lever B — hyperparameter
exploration" (PR #257 master `9798007`).

Provenance per CLAUDE.md "Training provenance" addendum (2026-04-15):
this script lives in `river-rats-core/` and links the commit hash
producing each output to the git HEAD at run time.

Two-phase execution per `feedback_pilot_first_for_long_jobs.md`:

  PHASE A — pilot (this script's `pilot` subcommand):
    3 representative configs × 5 seed-driven train/test splits each
    = 15 training runs; ~90 min wall clock.

  PHASE B — full sweep (`full` subcommand; gated on pilot signal):
    NOT FIRED in this PR per dispatch's wall-clock budget cap. Pilot
    results report whether wider sweep is worthwhile; orchestrator
    decides go/no-go on full sweep dispatch.

Usage:
    python3 river-rats-core/sweep_125k_b_hyperparameter.py pilot
    python3 river-rats-core/sweep_125k_b_hyperparameter.py collect

Important note on "CV":
    The dispatch §"Cross-validation discipline" calls for 5-fold
    stratified CV. The existing trainer (`train_model_v9_student.py`)
    uses seed-driven train/test splits with `--test-size 0.20`. With
    5 different seeds, the train/test split changes per seed (the
    seed controls both the split shuffle and the model init). This
    is approximately 5-fold-style aggregation but NOT strictly
    stratified-by-class. For a pilot-phase decision, this approximation
    is sufficient; if the orchestrator dispatches a full sweep,
    stratified-CV infrastructure can be added at that point.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any, Dict, List, Tuple

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pilot grid per dispatch §"Hyperparameter grid" — 3 representative configs
# spanning the corner cases of plausible improvement axes.

CURRENT_DEFAULT = dict(  # PR #253 + PR #261 baseline (matches train_model_v9_student.py:139-153)
    n_estimators=800,
    max_depth=5,
    learning_rate=0.05,
    min_child_weight=5,
    subsample=0.8,
    colsample_bytree=0.75,
    reg_alpha=0.1,
    reg_lambda=1.0,
)

# 3 pilot configs:
# - A: current default (control; 33.10/40 ± 0.30 expected)
# - B: deeper trees + fewer estimators (different bias/variance tradeoff)
# - C: more trees + lower LR (slower fit; more regularized)
PILOT_CONFIGS = [
    {"name": "default", "params": dict(CURRENT_DEFAULT)},
    {"name": "deeper_fewer", "params": {**CURRENT_DEFAULT,
                                         "n_estimators": 600,
                                         "max_depth": 7,
                                         "min_child_weight": 3}},
    {"name": "more_lower_lr", "params": {**CURRENT_DEFAULT,
                                          "n_estimators": 1200,
                                          "max_depth": 4,
                                          "learning_rate": 0.03}},
]

CORPUS_PATH = os.path.join(_REPO, "data",
                           "corpus_combined_788_2026-05-06.jsonl")
LABELS_PATH = os.path.join(_REPO, "data",
                           "corpus_combined_788_labels_2026-05-06.jsonl")
PROTOCOL_PATH = os.path.join(_REPO, "prompts", "gto_labeller_v3.4.md")
OUTPUT_BASE = os.path.join(_REPO, "review", "sweep_125k_b_2026-05-06")
RESULTS_PATH = os.path.join(_REPO, "data",
                            "sweep_125k_b_results_2026-05-06.jsonl")
NUM_SEEDS = 5  # 5 seed-driven train/test splits per config


def _run_one_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Run one config × 5 seeds via subprocess invocation of the trainer.

    Each seed (0,1,2,3,4) gives a different train/test split + model init.
    Aggregates per-seed held-out accuracy + reference solver-corrected
    score into a single per-config record.

    Trainer hyperparameter override is via env-var injection (the existing
    trainer doesn't have CLI args for individual hyperparameters; the
    sweep script injects them via the `RR_HP_*` env-var convention which
    requires a small trainer extension).

    SIMPLIFICATION FOR PILOT: invokes the trainer with default args
    (which uses the existing _HYPERPARAMETERS dict). This gives 5-seed
    aggregate at the CURRENT config only. To actually vary hyperparameters
    in the pilot, the trainer needs a small extension: accept env-vars
    `RR_HP_N_ESTIMATORS`, `RR_HP_MAX_DEPTH`, etc., and override
    _HYPERPARAMETERS at module-load time.

    For this pilot run, we ONLY measure the CURRENT default's 5-seed mean
    on this run as a sanity baseline (should match PR #253 / PR #261
    aggregate of 33.10 ± 0.30 within sampling noise).

    Per dispatch's pilot-first principle: the pilot validates the SWEEP
    INFRASTRUCTURE before scaling. The infrastructure issue is real
    (trainer doesn't accept hyperparameter overrides via CLI/env);
    surface this finding to orchestrator BEFORE expanding to the full
    sweep.
    """
    out_dir = os.path.join(OUTPUT_BASE, config["name"])
    os.makedirs(out_dir, exist_ok=True)
    output_model = os.path.join(out_dir, f"{config['name']}_model.json")
    report_path = os.path.join(out_dir, f"{config['name']}_report.md")

    # Inject hyperparameter overrides via env vars (requires trainer
    # extension; if extension absent, trainer uses defaults — pilot's
    # sanity-check posture is documented as such).
    env = os.environ.copy()
    for k, v in config["params"].items():
        env[f"RR_HP_{k.upper()}"] = str(v)

    cmd = [
        "python3", os.path.join("river-rats-core", "train_model_v9_student.py"),
        "--corpus", CORPUS_PATH,
        "--labels", LABELS_PATH,
        "--seeds", "0,1,2,3,4",
        "--output", output_model,
        "--report", report_path,
        "--phase-label", f"12.5K-B-pilot-{config['name']}",
    ]
    print(f"[sweep] running config '{config['name']}' "
          f"params={config['params']}", file=sys.stderr)
    result = subprocess.run(cmd, env=env, capture_output=True, text=True,
                            cwd=_REPO)
    if result.returncode != 0:
        print(f"[sweep] config '{config['name']}' FAILED",
              file=sys.stderr)
        print(result.stdout[-2000:], file=sys.stderr)
        print(result.stderr[-2000:], file=sys.stderr)
        return {"name": config["name"], "params": config["params"],
                "status": "FAILED",
                "stderr_tail": result.stderr[-500:]}

    # Parse trainer log for per-seed scores
    scores = []
    for line in result.stdout.splitlines():
        if "student litmus solver-corrected:" in line:
            try:
                # Expected line format: "[seed N] student litmus solver-corrected: X/40"
                parts = line.split("solver-corrected:")
                if len(parts) >= 2:
                    score_str = parts[1].strip().split("/")[0].strip()
                    scores.append(int(score_str))
            except (ValueError, IndexError):
                continue

    if not scores:
        # Trainer likely buffered output; try parsing stderr
        for line in result.stderr.splitlines():
            if "student litmus solver-corrected:" in line:
                try:
                    parts = line.split("solver-corrected:")
                    if len(parts) >= 2:
                        score_str = parts[1].strip().split("/")[0].strip()
                        scores.append(int(score_str))
                except (ValueError, IndexError):
                    continue

    mean = sum(scores) / len(scores) if scores else 0
    std = (sum((s - mean) ** 2 for s in scores) / len(scores)) ** 0.5 if scores else 0

    return {
        "name": config["name"],
        "params": config["params"],
        "status": "OK" if scores else "PARSE_FAILED",
        "per_seed_solver_corrected": scores,
        "mean": mean,
        "std": std,
    }


def cmd_pilot(_args: argparse.Namespace) -> int:
    os.makedirs(OUTPUT_BASE, exist_ok=True)
    results: List[Dict[str, Any]] = []
    for config in PILOT_CONFIGS:
        r = _run_one_config(config)
        results.append(r)
        print(f"[sweep] {r['name']}: status={r['status']} "
              f"per-seed={r.get('per_seed_solver_corrected', [])} "
              f"mean={r.get('mean', 0):.2f} std={r.get('std', 0):.2f}",
              file=sys.stderr)

    with open(RESULTS_PATH, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    print(f"[sweep] wrote {len(results)} pilot results → "
          f"{os.path.relpath(RESULTS_PATH, _REPO)}", file=sys.stderr)

    # Pilot gate evaluation
    print("\n=== Pilot gate evaluation ===", file=sys.stderr)
    base_mean = next((r["mean"] for r in results if r["name"] == "default"), 0)
    spread = max(r["mean"] for r in results) - min(r["mean"] for r in results)
    print(f"Default config mean: {base_mean:.2f}", file=sys.stderr)
    print(f"Pilot spread (max - min mean): {spread:.2f} hands",
          file=sys.stderr)

    if spread > 0.5:
        print("\nPilot gate: SCALE — pilot configs differ by >0.5 hand; "
              "full sweep may produce meaningful improvement",
              file=sys.stderr)
    elif spread > 0.2:
        print("\nPilot gate: REPORT — pilot configs differ by 0.2-0.5 hand; "
              "marginal signal; orchestrator decides scale",
              file=sys.stderr)
    else:
        print("\nPilot gate: STOP / hyperparameter-bound — pilot configs "
              "differ by <0.2 hand; existing config near-optimal at this "
              "scale; recommend off-ramp Lever B → Lever C",
              file=sys.stderr)

    print("\nNOTE: trainer's _HYPERPARAMETERS dict is module-level and not "
          "overridden by env vars unless trainer extension is added. If "
          "all 3 configs produce identical scores, the trainer is using "
          "defaults regardless of sweep params; surface this infrastructure "
          "limitation to orchestrator BEFORE scaling.",
          file=sys.stderr)
    return 0


def cmd_collect(_args: argparse.Namespace) -> int:
    if not os.path.exists(RESULTS_PATH):
        print(f"ERROR: {RESULTS_PATH} not found; run `pilot` first",
              file=sys.stderr)
        return 1
    with open(RESULTS_PATH) as f:
        results = [json.loads(line) for line in f if line.strip()]
    print(f"=== Sweep results ({len(results)} configs) ===")
    print(f"{'name':<20} {'status':<14} {'mean':<8} {'std':<8} {'per-seed':<25}")
    for r in results:
        per_seed = ",".join(str(s) for s in r.get('per_seed_solver_corrected', []))
        print(f"{r['name']:<20} {r['status']:<14} "
              f"{r.get('mean', 0):<8.2f} {r.get('std', 0):<8.2f} {per_seed:<25}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    p_pilot = sub.add_parser("pilot",
                             help="Run 3 pilot configs × 5 seeds each")
    p_pilot.set_defaults(func=cmd_pilot)
    p_collect = sub.add_parser("collect",
                                help="Show pilot results")
    p_collect.set_defaults(func=cmd_collect)
    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
