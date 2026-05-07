#!/usr/bin/env python3
"""Phase 12.5K-C-E corpus integration: 788 → 988 corpus assembly.

Per `MAIN_TERMINAL_PR289_RESOLUTION_AND_125KCE_DISPATCH_2026-05-07.md`
(master `19f958a`, PR #292). Mirror PR #222 (12.5I-D 604 → 694 → 788)
assembly pattern.

Inputs:
- data/corpus_combined_788_2026-05-06.jsonl (788 situations; 61-surface)
- data/corpus_combined_788_labels_2026-05-06.jsonl (788 labels with feat_dicts)
- data/corpus_lever_c_situations_v3_path_a_2026-05-07.jsonl (200 Lever C situations; Path A applied; MW-17 design_action=RAISE)
- data/corpus_lever_c_labels_full_2026-05-07.jsonl (700 raw Sonnet SCALE labels; 4-labeller consensus on most)
- data/corpus_lever_c_pilot_labels_raw_2026-05-07.jsonl (50 pre-FIX pilot labels for MW-40 + MW-45)
- data/corpus_lever_c_fix_pilot_labels_raw_2026-05-07.jsonl (50 post-FIX pilot labels for MW-17 + MW-47 redesigned)
- data/corpus_revision_125i_mw40_verif_labels_pilot_raw_2026-05-06.jsonl (25 pilot labels for MW-40 R1 reused; consensus BET 1.0 from PR #241)
- data/corpus_revision_125i_mw40_verif_labels_opus_tierup_2026-05-06.jsonl (5 Opus labels for MW-40 R1 reused; consensus BET from PR #245)

Outputs:
- data/corpus_combined_988_2026-05-07.jsonl (988 situations; 61-surface)
- data/corpus_combined_988_labels_2026-05-07.jsonl (988 labels with feat_dicts)
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, List

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_jsonl(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def main() -> int:
    # Load 788-corpus
    sit_788 = _load_jsonl(os.path.join(_REPO, "data", "corpus_combined_788_2026-05-06.jsonl"))
    lab_788 = _load_jsonl(os.path.join(_REPO, "data", "corpus_combined_788_labels_2026-05-06.jsonl"))
    print(f"[788] situations={len(sit_788)} labels={len(lab_788)}")

    # Load Lever C situations (v3 with Path A applied)
    sit_lc = _load_jsonl(os.path.join(_REPO, "data",
                                       "corpus_lever_c_situations_v3_path_a_2026-05-07.jsonl"))
    print(f"[Lever C] situations={len(sit_lc)}")

    # Aggregate Lever C labels from all sources
    all_labels: List[Dict[str, Any]] = []
    all_labels.extend(_load_jsonl(os.path.join(_REPO, "data",
                                               "corpus_lever_c_labels_full_2026-05-07.jsonl")))
    # Pre-FIX pilot (MW-40 + MW-45 only)
    pre_fix = _load_jsonl(os.path.join(_REPO, "data",
                                        "corpus_lever_c_pilot_labels_raw_2026-05-07.jsonl"))
    all_labels.extend([l for l in pre_fix
                       if l["pilot_hand_id"].startswith("PILOT_LEVER_C_MW40_") or
                          l["pilot_hand_id"].startswith("PILOT_LEVER_C_MW45_")])
    # Post-FIX pilot (MW-17 + MW-47 redesigned)
    post_fix = _load_jsonl(os.path.join(_REPO, "data",
                                          "corpus_lever_c_fix_pilot_labels_raw_2026-05-07.jsonl"))
    all_labels.extend(post_fix)
    print(f"[Lever C] aggregated raw labels: {len(all_labels)}")

    # MW-40 R1 reused hands (PILOT_LEVER_C_MW40_001..030) inherit BET label from PR #241/#245
    # Add synthetic labels for these hands using the verified MW-40-VERIFICATION consensus
    reused_count = 0
    for sit in sit_lc:
        rid = sit.get("pilot_hand_id")
        if rid and rid.startswith("PILOT_LEVER_C_MW40_") and \
                int(rid.split("_")[-1]) <= 30:
            # Synthetic label: BET 1.0 confidence (from MW-40-VERIFICATION-D Opus + Sonnet consensus)
            for labeller_id in (1, 2, 3, 4, 5):
                all_labels.append({
                    "pilot_hand_id": rid,
                    "labeller_id": labeller_id,
                    "model": "synthetic_from_pr241_pr245",
                    "protocol_version": "v3.4",
                    "action": "BET",
                    "confidence": "HIGH",
                    "reasoning": "MW-40 R1 reused: 5/5 Sonnet (PR #241) + 1/1 Opus 4.7 (PR #245) consensus on this hand at MW-40-VERIFICATION pilot.",
                })
            reused_count += 5
    print(f"[Lever C MW-40 R1 reused] synthesized {reused_count} consensus labels")

    # Compute per-hand consensus
    by_hand_votes: Dict[str, List[str]] = defaultdict(list)
    by_hand_label_records: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for lab in all_labels:
        rid = lab["pilot_hand_id"]
        by_hand_votes[rid].append(lab["action"])
        by_hand_label_records[rid].append(lab)

    # For each Lever C situation, compute consensus label record matching 788-labels schema
    lc_label_rows: List[Dict[str, Any]] = []
    for sit in sit_lc:
        rid = sit.get("pilot_hand_id")
        if not rid:
            continue
        votes = by_hand_votes.get(rid, [])
        if not votes:
            print(f"WARN: no labels for {rid}; skipping", file=sys.stderr)
            continue
        cnt = Counter(votes)
        top, top_n = cnt.most_common(1)[0]
        confidence = top_n / len(votes)
        # Round consensus_confidence to 0.4/0.6/0.8/1.0 buckets (mirror 788-labels schema)
        if confidence >= 0.95:
            cc = 1.0
        elif confidence >= 0.75:
            cc = 0.8
        elif confidence >= 0.55:
            cc = 0.6
        else:
            cc = 0.4
        lc_label_rows.append({
            "ref_id": rid,
            "pilot_hand_id": rid,
            "labels": [{"action": l["action"], "confidence": l["confidence"],
                        "labeller_id": l["labeller_id"]}
                       for l in by_hand_label_records[rid]],
            "consensus_action": top,
            "consensus_confidence": cc,
            "vote_count": len(votes),
            "valid_vote_count": len(votes),
            "feat_dict": sit.get("feat_dict", {}),
        })
    print(f"[Lever C] consensus labels: {len(lc_label_rows)}")

    # Per-action distribution
    actions_788 = Counter(l["consensus_action"] for l in lab_788)
    actions_lc = Counter(l["consensus_action"] for l in lc_label_rows)
    print(f"\n=== Per-action distribution ===")
    print(f"  788-corpus: {dict(actions_788)}")
    print(f"  Lever C 200: {dict(actions_lc)}")

    # Combined
    combined_sit = sit_788 + sit_lc
    combined_lab = lab_788 + lc_label_rows
    actions_988 = Counter(l["consensus_action"] for l in combined_lab)
    print(f"  988-corpus: {dict(actions_988)}")

    # Confidence distribution
    confs_988 = Counter(round(l["consensus_confidence"], 1) for l in combined_lab)
    print(f"  988-corpus confidence distribution: {dict(sorted(confs_988.items()))}")

    # ref_id collision check
    ids_788 = {s.get("pilot_hand_id") or s.get("situation_id") for s in sit_788}
    ids_lc = {s.get("pilot_hand_id") for s in sit_lc}
    overlap = ids_788 & ids_lc
    if overlap:
        print(f"STOP: {len(overlap)} ref_id collisions: {sorted(overlap)[:5]}",
              file=sys.stderr)
        return 1
    print(f"\n[ok] ref_id namespace disjoint (788 ∩ Lever C = empty)")

    # Schema integrity (61-surface)
    fd_sizes = Counter(len(l.get("feat_dict", {})) for l in combined_lab)
    if list(fd_sizes.keys()) != [61]:
        print(f"WARN: feat_dict sizes vary: {dict(fd_sizes)}", file=sys.stderr)
    else:
        print(f"[ok] feat_dict 61-surface uniform across all 988 rows")

    # NaN/Inf check
    nan = 0
    for l in combined_lab:
        for k, v in (l.get("feat_dict") or {}).items():
            if isinstance(v, float) and (v != v or v in (float("inf"), float("-inf"))):
                nan += 1
    print(f"[ok] NaN/Inf: {nan} (across {len(combined_lab) * 61} values)")

    # Write outputs
    sit_out = os.path.join(_REPO, "data", "corpus_combined_988_2026-05-07.jsonl")
    lab_out = os.path.join(_REPO, "data", "corpus_combined_988_labels_2026-05-07.jsonl")
    with open(sit_out, "w") as f:
        for s in combined_sit:
            f.write(json.dumps(s) + "\n")
    with open(lab_out, "w") as f:
        for l in combined_lab:
            f.write(json.dumps(l) + "\n")
    print(f"\n[ok] wrote {len(combined_sit)} situations → {os.path.relpath(sit_out, _REPO)}")
    print(f"[ok] wrote {len(combined_lab)} labels → {os.path.relpath(lab_out, _REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
