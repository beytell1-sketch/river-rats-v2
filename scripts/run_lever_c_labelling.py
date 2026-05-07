#!/usr/bin/env python3
"""Phase 12.5K-C-C Lever C labelling-round orchestration helper.

Per `MAIN_TERMINAL_PR273_RESOLUTION_AND_125KCC_DISPATCH_2026-05-07.md`
(master `6fab0d7`, PR #276). Mirrors prior 12.5I-C / MW-40-VERIFICATION-C
labelling-round patterns, adapted for 4-axis per-axis pilot-first gate.

R1 special case (per merged plan §3): MW-40 axis re-uses 30 already-labelled
hands from MW-40-VERIFICATION-B; only the 20 fresh hands need -C labelling.
Pilot pick for MW-40 is from the fresh 20 (PILOT_LEVER_C_MW40_031..035).

Phases:
  PHASE A — pilot (this script's `prepare_pilot` subcommand):
    20 hands (5 per axis × 4 axes) × 5 labellers = 100 pilot labels;
    ~$5-8 LLM; ~5-10 min wall clock.

  PHASE B — full (after per-axis pilot gate clears):
    150 hands (45 MW-17 + 15 MW-40 + 45 MW-45 + 45 MW-47) × 5 labellers
    = 750 labels; ~$30-40 LLM; ~25-35 min wall clock.

  Collect: aggregate per-axis consensus + per-axis CHECK/CALL/RAISE/BET
    distribution.

Usage:
    python3 scripts/run_lever_c_labelling.py prepare_pilot
    # builder spawns 5 Sonnet Agent calls
    python3 scripts/run_lever_c_labelling.py collect_pilot
    # if per-axis gate passes: prepare_full + 5 more Agent calls + collect_full
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Tuple

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "scripts"))

from dispatch_mass_labelling import prepare as _dispatch_prepare  # noqa: E402

CORPUS_PATH = os.path.join(_REPO, "data", "corpus_lever_c_situations_2026-05-07.jsonl")
PROTOCOL_PATH = os.path.join(_REPO, "prompts", "gto_labeller_v3.4.md")
OUTPUT_BASE = os.path.join(_REPO, "review", "mass_labelling_lever_c_2026-05-07")
NUM_LABELLERS = 5

# Per-axis pilot picks (5 hands each; first 5 of each axis's labelling-needed range).
# MW-40 axis: skip the 30 re-used (PILOT_LEVER_C_MW40_001..030); pilot from fresh 031..035.
PILOT_REF_IDS = {
    "MW-17": [f"PILOT_LEVER_C_MW17_{i:03d}" for i in range(1, 6)],
    "MW-40": [f"PILOT_LEVER_C_MW40_{i:03d}" for i in range(31, 36)],
    "MW-45": [f"PILOT_LEVER_C_MW45_{i:03d}" for i in range(1, 6)],
    "MW-47": [f"PILOT_LEVER_C_MW47_{i:03d}" for i in range(1, 6)],
}
ALL_PILOT_IDS = set(rid for ids in PILOT_REF_IDS.values() for rid in ids)

# Per-axis FULL-batch ref_ids (everything needing labelling minus pilot).
# MW-40: PILOT_LEVER_C_MW40_036..050 (15 fresh; skip pilot 031..035 + skip re-used 001..030)
FULL_REF_IDS = {
    "MW-17": [f"PILOT_LEVER_C_MW17_{i:03d}" for i in range(6, 51)],
    "MW-40": [f"PILOT_LEVER_C_MW40_{i:03d}" for i in range(36, 51)],
    "MW-45": [f"PILOT_LEVER_C_MW45_{i:03d}" for i in range(6, 51)],
    "MW-47": [f"PILOT_LEVER_C_MW47_{i:03d}" for i in range(6, 51)],
}

# Per-axis target action (for consensus gate evaluation)
AXIS_TARGET = {
    "MW-17": "CALL",
    "MW-40": "BET",
    "MW-45": "RAISE",
    "MW-47": "RAISE",
}


def _load_corpus() -> List[Dict[str, Any]]:
    with open(CORPUS_PATH) as f:
        return [json.loads(line) for line in f if line.strip()]


def cmd_prepare_pilot(_args: argparse.Namespace) -> int:
    records = _load_corpus()
    subset = [r for r in records if r.get("pilot_hand_id") in ALL_PILOT_IDS]
    if len(subset) != 20:
        print(f"ERROR: expected 20 pilot records, got {len(subset)}", file=sys.stderr)
        return 1

    out_dir = os.path.join(OUTPUT_BASE, "pilot")
    os.makedirs(out_dir, exist_ok=True)
    subset_path = os.path.join(out_dir, "corpus_subset_pilot.jsonl")
    with open(subset_path, "w") as f:
        for r in subset:
            f.write(json.dumps(r) + "\n")
    print(f"[ok] wrote {len(subset)} pilot corpus records → "
          f"{os.path.relpath(subset_path, _REPO)}")
    _dispatch_prepare(corpus_path=subset_path, protocol_path=PROTOCOL_PATH,
                      num_labellers=NUM_LABELLERS, output_dir=out_dir)
    print(f"[ok] {NUM_LABELLERS} pilot briefs at {os.path.relpath(out_dir, _REPO)}")
    return 0


def cmd_prepare_full(args: argparse.Namespace) -> int:
    """Prepare full-batch briefs for axes that passed pilot.
    `--axes` is a comma-separated list of axes that passed (e.g., MW-17,MW-45,MW-47)."""
    records = _load_corpus()
    passing_axes = [a.strip() for a in args.axes.split(",")]
    target_ids: set = set()
    for axis in passing_axes:
        if axis not in FULL_REF_IDS:
            print(f"ERROR: unknown axis {axis}", file=sys.stderr)
            return 1
        target_ids.update(FULL_REF_IDS[axis])

    subset = [r for r in records if r.get("pilot_hand_id") in target_ids]
    if not subset:
        print(f"ERROR: no records matching axes {passing_axes}", file=sys.stderr)
        return 1
    print(f"[ok] {len(subset)} full-batch records across axes {passing_axes}")

    out_dir = os.path.join(OUTPUT_BASE, "full")
    os.makedirs(out_dir, exist_ok=True)
    subset_path = os.path.join(out_dir, "corpus_subset_full.jsonl")
    with open(subset_path, "w") as f:
        for r in subset:
            f.write(json.dumps(r) + "\n")
    _dispatch_prepare(corpus_path=subset_path, protocol_path=PROTOCOL_PATH,
                      num_labellers=NUM_LABELLERS, output_dir=out_dir)
    return 0


def _read_labeller_outputs(phase: str) -> List[Dict[str, Any]]:
    phase_dir = os.path.join(OUTPUT_BASE, phase)
    out: List[Dict[str, Any]] = []
    for n in range(1, NUM_LABELLERS + 1):
        path = os.path.join(phase_dir, f"labels_v3_4_labeller_{n}.json")
        if not os.path.exists(path):
            print(f"WARNING: missing {path}", file=sys.stderr)
            continue
        with open(path) as f:
            d = json.load(f)
        for lab in d.get("labels", []):
            ref = lab.get("ref_id") or lab.get("pilot_hand_id")
            out.append({
                "pilot_hand_id": ref,
                "labeller_id": n,
                "model": d.get("model", "claude-sonnet-4-6"),
                "protocol_version": d.get("protocol_version", "v3.4"),
                "action": lab.get("action"),
                "confidence": lab.get("confidence"),
                "reasoning": lab.get("reasoning", ""),
            })
    return out


def cmd_collect_pilot(_args: argparse.Namespace) -> int:
    labels = _read_labeller_outputs("pilot")
    if not labels:
        print("ERROR: no pilot labels found", file=sys.stderr)
        return 1
    out_path = os.path.join(_REPO, "data",
                            "corpus_lever_c_pilot_labels_raw_2026-05-07.jsonl")
    with open(out_path, "w") as f:
        for r in labels:
            f.write(json.dumps(r) + "\n")
    print(f"[ok] wrote {len(labels)} pilot labels → {os.path.relpath(out_path, _REPO)}")

    # Per-axis consensus + gate
    from collections import Counter
    by_axis: Dict[str, Dict[str, List[str]]] = {a: {} for a in AXIS_TARGET}
    for lab in labels:
        rid = lab["pilot_hand_id"]
        for axis, ids in PILOT_REF_IDS.items():
            if rid in ids:
                by_axis[axis].setdefault(rid, []).append(lab["action"])
                break

    print("\n=== Per-axis pilot consensus (target actions: MW-17=CALL, MW-40=BET, MW-45=RAISE, MW-47=RAISE) ===")
    passing_axes: List[str] = []
    failing_axes: List[str] = []
    for axis in ("MW-17", "MW-40", "MW-45", "MW-47"):
        target = AXIS_TARGET[axis]
        per_hand_consensus = []
        for rid, votes in sorted(by_axis[axis].items()):
            cnt = Counter(votes)
            top, top_n = cnt.most_common(1)[0]
            n_total = len(votes)
            consensus = top_n / n_total
            per_hand_consensus.append((rid, votes, top, consensus))
            print(f"  {rid}: votes={','.join(f'{a}:{c}' for a,c in cnt.most_common())} "
                  f"→ {top} ({top_n}/{n_total} = {consensus:.0%})")
        n_target = sum(1 for _, _, top, _ in per_hand_consensus if top == target)
        n_4_5_consensus = sum(1 for _, votes, _, _ in per_hand_consensus
                               if max(Counter(votes).values()) >= 4)
        target_consensus_count = sum(
            1 for _, votes, _, _ in per_hand_consensus
            if Counter(votes).get(target, 0) >= 4
        )
        gate = "PASS" if target_consensus_count >= 4 else "FAIL"
        if gate == "PASS":
            passing_axes.append(axis)
        else:
            failing_axes.append(axis)
        print(f"  Axis {axis}: target={target}; "
              f"{target_consensus_count}/5 hands have ≥4/5 {target} consensus → {gate}")
    print(f"\nPassing axes: {passing_axes}")
    print(f"Failing axes: {failing_axes}")
    if failing_axes:
        print("\n** Per-axis off-ramp: dropped axes for full run; route to orchestrator **")
    return 0


def cmd_collect_full(_args: argparse.Namespace) -> int:
    labels = _read_labeller_outputs("full")
    if not labels:
        print("ERROR: no full labels found", file=sys.stderr)
        return 1
    out_path = os.path.join(_REPO, "data",
                            "corpus_lever_c_full_labels_raw_2026-05-07.jsonl")
    with open(out_path, "w") as f:
        for r in labels:
            f.write(json.dumps(r) + "\n")
    print(f"[ok] wrote {len(labels)} full labels → {os.path.relpath(out_path, _REPO)}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    p_pp = sub.add_parser("prepare_pilot")
    p_pp.set_defaults(func=cmd_prepare_pilot)
    p_pf = sub.add_parser("prepare_full")
    p_pf.add_argument("--axes", required=True,
                      help="comma-separated passing axes (e.g., MW-17,MW-45,MW-47)")
    p_pf.set_defaults(func=cmd_prepare_full)
    p_cp = sub.add_parser("collect_pilot")
    p_cp.set_defaults(func=cmd_collect_pilot)
    p_cf = sub.add_parser("collect_full")
    p_cf.set_defaults(func=cmd_collect_full)
    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
