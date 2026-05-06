#!/usr/bin/env python3
"""Phase 12.5I-MW40-VERIFICATION-C labelling-round orchestration helper.

Per `MAIN_TERMINAL_PR236_RATIFY_AND_MW40C_DISPATCH_2026-05-06.md`
(master `3927024`, PR #240). Mirrors the prior 12.5I-C labelling-round
pattern but parameterised for the MW-40-VERIFICATION corpus.

Builder runs this script in TWO phases per `feedback_pilot_first_for_long_jobs.md`:

  1. PILOT (5 hands × 5 labellers): pre-flight gate before scaling.
     `python3 scripts/run_125i_mw40_verif_labelling.py prepare --pilot`

  2. FULL (after pilot gate clear): remaining 25 hands × 5 labellers.
     `python3 scripts/run_125i_mw40_verif_labelling.py prepare --full`

Each phase generates per-labeller briefs in
`review/mass_labelling_mw40v_2026-05-06/{pilot,full}/`. Builder dispatches
5 sonnet Agent calls per phase pointing at those briefs (the Agent tool is
session-scoped and not invokable from this script — see
`scripts/dispatch_mass_labelling.py` docstring for the canonical pattern).

After all 5 labellers complete a phase, builder runs:
  `python3 scripts/run_125i_mw40_verif_labelling.py collect --phase {pilot|full|combined}`
to merge per-labeller JSONs into a single per-hand label-record JSONL.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "scripts"))

from dispatch_mass_labelling import prepare as _dispatch_prepare  # noqa: E402

CORPUS_PATH = os.path.join(_REPO, "data",
                           "corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl")
PROTOCOL_PATH = os.path.join(_REPO, "prompts", "gto_labeller_v3.4.md")
OUTPUT_BASE = os.path.join(_REPO, "review", "mass_labelling_mw40v_2026-05-06")
NUM_LABELLERS = 5

# Pilot hand selection per dispatch §"Pick the 5 pilot hands":
# 2 sub-axis A + 2 sub-axis C standard + 1 boundary JcJh4s
PILOT_REF_IDS = [
    "PILOT_MW40_VERIF_001",  # sub-axis A; Js9c5h, TdJc; plan §4 carry
    "PILOT_MW40_VERIF_011",  # sub-axis A; Js8d3h, TcJd; builder-added in -B
    "PILOT_MW40_VERIF_016",  # sub-axis C; Jh5c2d, TsJc; plan §4 carry
    "PILOT_MW40_VERIF_025",  # sub-axis C; JcJh4s, ThJd; paired-J boundary case
    "PILOT_MW40_VERIF_026",  # sub-axis C; Jh7s3d, TcJd; builder-added in -B
]


def _load_corpus() -> List[Dict[str, Any]]:
    with open(CORPUS_PATH) as f:
        return [json.loads(line) for line in f if line.strip()]


def _ref_id(record: Dict[str, Any]) -> str:
    # MW-40-VERIF corpus uses pilot_hand_id as the canonical ref.
    return record.get("pilot_hand_id") or record.get("situation_id") or ""


def cmd_prepare(args: argparse.Namespace) -> int:
    """Subset the 30-hand corpus to pilot or full and prepare briefs."""
    records = _load_corpus()
    if len(records) != 30:
        print(f"ERROR: expected 30 corpus records, got {len(records)}", file=sys.stderr)
        return 1

    pilot_set = set(PILOT_REF_IDS)
    if args.pilot:
        subset = [r for r in records if _ref_id(r) in pilot_set]
        phase = "pilot"
        if len(subset) != 5:
            print(f"ERROR: expected 5 pilot records, got {len(subset)}: "
                  f"{[_ref_id(r) for r in subset]}", file=sys.stderr)
            return 1
    elif args.full:
        subset = [r for r in records if _ref_id(r) not in pilot_set]
        phase = "full"
        if len(subset) != 25:
            print(f"ERROR: expected 25 full-batch records, got {len(subset)}",
                  file=sys.stderr)
            return 1
    else:
        print("ERROR: must specify --pilot or --full", file=sys.stderr)
        return 1

    out_dir = os.path.join(OUTPUT_BASE, phase)
    os.makedirs(out_dir, exist_ok=True)

    # Write subset corpus to disk so dispatch_mass_labelling can read it.
    subset_path = os.path.join(out_dir, f"corpus_subset_{phase}.jsonl")
    with open(subset_path, "w") as f:
        for r in subset:
            f.write(json.dumps(r) + "\n")
    print(f"[ok] wrote {len(subset)} {phase} corpus records → {os.path.relpath(subset_path, _REPO)}")

    manifest = _dispatch_prepare(
        corpus_path=subset_path,
        protocol_path=PROTOCOL_PATH,
        num_labellers=NUM_LABELLERS,
        output_dir=out_dir,
    )
    manifest_path = os.path.join(out_dir, "manifest.json")
    print(f"[ok] manifest written → {os.path.relpath(manifest_path, _REPO)}")
    print(f"[ok] {NUM_LABELLERS} labeller briefs → {os.path.relpath(out_dir, _REPO)}/brief_labeller_*.md")
    print()
    print("Builder must now dispatch 5 sonnet Agent calls in parallel, each reading "
          f"one brief and writing its output to the path declared in the brief's "
          "Output contract section.")
    return 0


def cmd_collect(args: argparse.Namespace) -> int:
    """Collect 5 per-labeller JSONs into a single label-record JSONL.

    Output schema mirrors `data/corpus_revision_125i_labels_raw_*.jsonl`
    (one record per (hand × labeller); fields: pilot_hand_id, labeller_id,
    model, protocol_version, action, confidence, reasoning).
    """
    phase = args.phase
    if phase == "combined":
        # Merge pilot + full
        labels = _read_phase_labels("pilot") + _read_phase_labels("full")
        out_path = os.path.join(_REPO, "data",
                                "corpus_revision_125i_mw40_verif_labels_raw_2026-05-06.jsonl")
    else:
        labels = _read_phase_labels(phase)
        out_path = os.path.join(_REPO, "data",
                                f"corpus_revision_125i_mw40_verif_labels_{phase}_raw_2026-05-06.jsonl")

    # De-dup safety
    seen = set()
    dedup = []
    for lr in labels:
        key = (lr["pilot_hand_id"], lr["labeller_id"])
        if key in seen:
            print(f"WARNING: duplicate {key}; dropping", file=sys.stderr)
            continue
        seen.add(key)
        dedup.append(lr)

    with open(out_path, "w") as f:
        for lr in dedup:
            f.write(json.dumps(lr) + "\n")
    print(f"[ok] wrote {len(dedup)} label records → {os.path.relpath(out_path, _REPO)}")

    # Per-hand consensus summary
    by_hand: Dict[str, List[Dict[str, Any]]] = {}
    for lr in dedup:
        by_hand.setdefault(lr["pilot_hand_id"], []).append(lr)

    print(f"\n=== Per-hand consensus ({phase}) ===")
    print(f"{'ref_id':<28} {'votes':<25} {'consensus':<10} {'conf':<6}")
    for rid in sorted(by_hand.keys()):
        votes = [lr["action"] for lr in by_hand[rid]]
        from collections import Counter
        cnt = Counter(votes)
        top_action, top_n = cnt.most_common(1)[0]
        n_total = len(votes)
        confidence = top_n / n_total
        votes_str = ",".join(f"{a}:{c}" for a, c in cnt.most_common())
        print(f"{rid:<28} {votes_str:<25} {top_action:<10} {confidence:.2f} ({top_n}/{n_total})")

    return 0


def _read_phase_labels(phase: str) -> List[Dict[str, Any]]:
    phase_dir = os.path.join(OUTPUT_BASE, phase)
    out: List[Dict[str, Any]] = []
    # Find labels_v3_4_labeller_*.json
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


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    p_prepare = sub.add_parser("prepare", help="Generate per-labeller briefs for pilot or full phase")
    g = p_prepare.add_mutually_exclusive_group(required=True)
    g.add_argument("--pilot", action="store_true",
                   help="Subset to 5 pilot hands per dispatch §'Pick the 5 pilot hands'")
    g.add_argument("--full", action="store_true",
                   help="Subset to 25 remaining (non-pilot) hands")
    p_prepare.set_defaults(func=cmd_prepare)
    p_collect = sub.add_parser("collect", help="Collect per-labeller JSONs into label-record JSONL")
    p_collect.add_argument("--phase", choices=["pilot", "full", "combined"], required=True)
    p_collect.set_defaults(func=cmd_collect)
    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
