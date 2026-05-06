#!/usr/bin/env python3
"""Phase 12.5I-MW40-VERIFICATION-D Opus 4.7 tier-up orchestration.

Per `MAIN_TERMINAL_PR241_RESOLUTION_AND_MW40D_DISPATCH_2026-05-06.md`
(master `966fcbd`, PR #244). Mirrors PR #209's MW-25 Opus 4.7 tier-up
precedent: 1 Opus 4.7 call labels the 5 pilot hands using the same v3.4
production prompt the Sonnet pilot used (PR #241).

Phase A — prepare brief (this script):
  python3 scripts/run_125i_mw40_verif_opus_tierup.py prepare

Phase B — dispatch Opus 4.7 (builder, this Claude session):
  Builder spawns 1 Agent tool call with model="opus" reading the brief
  generated in phase A; the Opus subagent applies v3.4 verbatim and
  writes its 5 labels to `labels_v3_4_labeller_1.json` at the path
  declared in the brief.

Phase C — collect (this script):
  python3 scripts/run_125i_mw40_verif_opus_tierup.py collect
  → produces `data/corpus_revision_125i_mw40_verif_labels_opus_tierup_*.jsonl`
  with 5 records (one per hand) tagged model=claude-opus-4-7.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "scripts"))

from dispatch_mass_labelling import prepare as _dispatch_prepare  # noqa: E402

CORPUS_PATH = os.path.join(_REPO, "data",
                           "corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl")
PROTOCOL_PATH = os.path.join(_REPO, "prompts", "gto_labeller_v3.4.md")
OUTPUT_DIR = os.path.join(_REPO, "review", "mass_labelling_mw40v_2026-05-06", "opus_tierup")

# Same 5 pilot hand ids as the Sonnet pilot (PR #241).
PILOT_REF_IDS = [
    "PILOT_MW40_VERIF_001",
    "PILOT_MW40_VERIF_011",
    "PILOT_MW40_VERIF_016",
    "PILOT_MW40_VERIF_025",
    "PILOT_MW40_VERIF_026",
]


def _load_corpus() -> List[Dict[str, Any]]:
    with open(CORPUS_PATH) as f:
        return [json.loads(line) for line in f if line.strip()]


def cmd_prepare(_args: argparse.Namespace) -> int:
    records = _load_corpus()
    pilot_set = set(PILOT_REF_IDS)
    subset = [r for r in records if r.get("pilot_hand_id") in pilot_set]
    if len(subset) != 5:
        print(f"ERROR: expected 5 pilot records, got {len(subset)}", file=sys.stderr)
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    subset_path = os.path.join(OUTPUT_DIR, "corpus_subset_opus_tierup.jsonl")
    with open(subset_path, "w") as f:
        for r in subset:
            f.write(json.dumps(r) + "\n")
    print(f"[ok] wrote 5 pilot corpus records → {os.path.relpath(subset_path, _REPO)}")

    _dispatch_prepare(
        corpus_path=subset_path,
        protocol_path=PROTOCOL_PATH,
        num_labellers=1,  # single Opus tier-up labeller per dispatch §"Mirror PR #209 pattern"
        output_dir=OUTPUT_DIR,
    )
    print(f"[ok] Opus tier-up brief → {os.path.relpath(OUTPUT_DIR, _REPO)}/labeller_1_brief.md")
    return 0


def cmd_collect(_args: argparse.Namespace) -> int:
    in_path = os.path.join(OUTPUT_DIR, "labels_v3_4_labeller_1.json")
    if not os.path.exists(in_path):
        print(f"ERROR: missing {in_path}", file=sys.stderr)
        return 1
    with open(in_path) as f:
        d = json.load(f)
    out_path = os.path.join(_REPO, "data",
                            "corpus_revision_125i_mw40_verif_labels_opus_tierup_2026-05-06.jsonl")
    rows: List[Dict[str, Any]] = []
    for lab in d.get("labels", []):
        rid = lab.get("ref_id") or lab.get("pilot_hand_id")
        rows.append({
            "pilot_hand_id": rid,
            "labeller_id": "opus_tierup",
            "model": "claude-opus-4-7",
            "protocol_version": d.get("protocol_version", "v3.4"),
            "action": lab.get("action"),
            "confidence": lab.get("confidence"),
            "reasoning": lab.get("reasoning", ""),
        })
    with open(out_path, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"[ok] wrote {len(rows)} Opus tier-up records → {os.path.relpath(out_path, _REPO)}")

    print("\n=== Sonnet pilot vs Opus tier-up side-by-side ===")
    print(f"{'ref_id':<28} {'Sonnet':<10} {'Opus':<10} {'match':<8}")
    sonnet_path = os.path.join(_REPO, "data",
                               "corpus_revision_125i_mw40_verif_labels_pilot_raw_2026-05-06.jsonl")
    sonnet_consensus: Dict[str, str] = {}
    with open(sonnet_path) as f:
        from collections import Counter
        all_labels: List[Dict[str, Any]] = [json.loads(l) for l in f]
        by_hand: Dict[str, List[str]] = {}
        for lr in all_labels:
            by_hand.setdefault(lr["pilot_hand_id"], []).append(lr["action"])
        for rid, votes in by_hand.items():
            top, _ = Counter(votes).most_common(1)[0]
            sonnet_consensus[rid] = top
    n_match = 0
    for r in rows:
        rid = r["pilot_hand_id"]
        s = sonnet_consensus.get(rid, "?")
        o = r["action"]
        match = "✓" if s == o else "DIVERGE"
        if s == o:
            n_match += 1
        print(f"{rid:<28} {s:<10} {o:<10} {match:<8}")
    print(f"\nAggregate Sonnet-Opus consensus: {n_match}/{len(rows)} match")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    p_prep = sub.add_parser("prepare")
    p_prep.set_defaults(func=cmd_prepare)
    p_coll = sub.add_parser("collect")
    p_coll.set_defaults(func=cmd_collect)
    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
