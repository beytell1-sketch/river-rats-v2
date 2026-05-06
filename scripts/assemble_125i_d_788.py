#!/usr/bin/env python3
"""Phase 12.5I-D corpus assemble — combine 694-corpus + 94-revision into 788.

Per `MAIN_TERMINAL_PR218_MERGE_AND_125ID_DISPATCH_2026-05-06.md`.

Mirrors the 12.5H-D precedent (604 → 694) for the next phase 694 → 788.

Inputs:
  - data/corpus_combined_694_2026-05-06.jsonl                (61-surface; PR #205-extracted)
  - data/corpus_combined_694_labels_2026-05-06.jsonl         (59-surface embedded feat_dict)
  - data/corpus_revision_125i_situations_2026-05-06.jsonl    (59-surface; 90 hands)
  - data/corpus_revision_125i_manual_canonicals_2026-05-06.jsonl (59-surface; 4 hands)
  - data/corpus_revision_125i_labels_2026-05-06.jsonl        (59-surface embedded feat_dict; 94 consensus rows)

Outputs:
  - data/corpus_combined_788_2026-05-06.jsonl                (788 rows, 61-surface)
  - data/corpus_combined_788_labels_2026-05-06.jsonl         (788 rows, 61-surface embedded feat_dict)

Backfill direction: 59-surface rows get the 2 Step-18 features computed and
appended. The 12.5I-B/C-generated rows + 694 labels file are 59-surface; the
694 situations file is already 61-surface per PR #205. We backfill ALL
59-surface rows to 61-surface for cross-corpus consistency.

Step-18 features (positions 60-61):
  - nut_blocker_overcard_count = compute_nut_blocker_overcard_count(
        hero_cards, high_card_rank, nut_flush_block)
  - bet_call_multiway_oop_raise_pressure_index =
      compute_bet_call_multiway_oop_raise_pressure_index(
        facing_bet, num_callers_to_bet, num_opponents, is_ip,
        nut_flush_block, has_flush_draw, raw_equity)

Both are deterministic from the existing 59-surface feat_dict (no NaN/Inf risk;
both functions return Python int/float with default-0 fallbacks).
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from typing import Any, Dict, List, Tuple

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "river-rats-core"))

# Read-only import from feature_extractor (no modifications).
from feature_extractor import (  # noqa: E402
    compute_nut_blocker_overcard_count,
    compute_bet_call_multiway_oop_raise_pressure_index,
)

STEP18_KEYS = (
    "nut_blocker_overcard_count",
    "bet_call_multiway_oop_raise_pressure_index",
)


def _read_jsonl(path: str) -> List[Dict[str, Any]]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def _write_jsonl(path: str, rows: List[Dict[str, Any]]) -> None:
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def _record_ref_id(rec: Dict[str, Any]) -> str:
    """Match `compute_ref_id` discipline: source_situation_id > deal_id-derived
    > pilot_hand_id."""
    ssi = rec.get("source_situation_id")
    if ssi:
        return ssi
    if "deal_id" in rec and rec["deal_id"] is not None:
        return f"d{rec['deal_id']}_{rec['hero_position']}_{rec['street']}"
    pid = rec.get("pilot_hand_id")
    if pid:
        return pid
    raise ValueError(f"record has no ref-key fields: {list(rec.keys())}")


def _backfill_step18(feat: Dict[str, Any], hero_cards_str: str) -> Tuple[int, float]:
    """Compute the 2 Step-18 feature values from an existing 59-surface
    feat_dict. Returns (nut_blocker_overcard_count, bet_call_pressure_index)."""
    # hero_cards: ['Ad', 'Ks'] format
    if isinstance(hero_cards_str, list):
        hero_cards = list(hero_cards_str)
    else:
        # "Ks7s" → ["Ks", "7s"]
        s = hero_cards_str
        hero_cards = [s[0:2], s[2:4]] if len(s) >= 4 else [s]
    nbc = compute_nut_blocker_overcard_count(
        hero_cards,
        feat.get("high_card_rank", 14),
        feat.get("nut_flush_block", 0),
    )
    pri = compute_bet_call_multiway_oop_raise_pressure_index(
        facing_bet=int(feat.get("facing_bet", 0)),
        num_callers_to_bet=int(feat.get("num_callers_to_bet", 0)),
        num_opponents=int(feat.get("num_opponents", 1)),
        is_ip=int(feat.get("is_ip", 0)),
        nut_flush_block=int(feat.get("nut_flush_block", 0) or 0),
        has_flush_draw=int(feat.get("has_flush_draw", 0)),
        raw_equity=float(feat.get("raw_equity", 0.0)),
    )
    return nbc, pri


def _ensure_step18(rec: Dict[str, Any], hero_cards_field: str = "hero_cards") -> Dict[str, Any]:
    """Mutate rec.feat_dict to include step-18 keys; preserve everything else.

    Idempotent: if both keys already present, no-op (preserves PR #205 values
    on 694-corpus rows that are already 61-surface).
    """
    feat = rec.get("feat_dict", {})
    if all(k in feat for k in STEP18_KEYS):
        return rec
    nbc, pri = _backfill_step18(feat, rec.get(hero_cards_field, ""))
    feat["nut_blocker_overcard_count"] = nbc
    feat["bet_call_multiway_oop_raise_pressure_index"] = pri
    rec["feat_dict"] = feat
    return rec


def assemble() -> Dict[str, Any]:
    repo_data = os.path.join(_REPO, "data")

    # ── Inputs ────────────────────────────────────────────────────────
    corpus_694 = _read_jsonl(os.path.join(repo_data, "corpus_combined_694_2026-05-06.jsonl"))
    labels_694 = _read_jsonl(os.path.join(repo_data, "corpus_combined_694_labels_2026-05-06.jsonl"))
    sit_125i_param = _read_jsonl(os.path.join(repo_data, "corpus_revision_125i_situations_2026-05-06.jsonl"))
    sit_125i_manuals = _read_jsonl(os.path.join(repo_data, "corpus_revision_125i_manual_canonicals_2026-05-06.jsonl"))
    labels_125i = _read_jsonl(os.path.join(repo_data, "corpus_revision_125i_labels_2026-05-06.jsonl"))

    print(f"[125i-d] inputs: 694-corpus={len(corpus_694)}, 694-labels={len(labels_694)}, "
          f"125i-param={len(sit_125i_param)}, 125i-manuals={len(sit_125i_manuals)}, "
          f"125i-labels={len(labels_125i)}")

    sit_125i_all = sit_125i_param + sit_125i_manuals
    assert len(sit_125i_all) == 94, f"125i situations should be 94; got {len(sit_125i_all)}"
    assert len(labels_125i) == 94, f"125i labels should be 94; got {len(labels_125i)}"

    # ── Schema validation ─────────────────────────────────────────────
    # Both 694-corpus and 125i situations need the same 59-surface keys
    # (existing labels) + 2 step-18 keys after backfill.
    fd_694_first = corpus_694[0]["feat_dict"]
    fd_125i_first = sit_125i_all[0]["feat_dict"]
    base_keys_694 = set(fd_694_first.keys())
    base_keys_125i = set(fd_125i_first.keys())
    keys_only_in_694 = base_keys_694 - base_keys_125i
    keys_only_in_125i = base_keys_125i - base_keys_694
    print(f"[125i-d] feat_dict size: 694={len(base_keys_694)}, 125i={len(base_keys_125i)}")
    print(f"[125i-d] keys only in 694: {sorted(keys_only_in_694)}")
    print(f"[125i-d] keys only in 125i: {sorted(keys_only_in_125i)}")
    if keys_only_in_125i:
        raise SystemExit(f"[125i-d] STOP: 125i has feat_dict keys not in 694: {keys_only_in_125i}")
    expected_extra = set(STEP18_KEYS)
    if keys_only_in_694 != expected_extra:
        raise SystemExit(
            f"[125i-d] STOP: 694 vs 125i feat_dict diff is not exactly the 2 step-18 keys; got: "
            f"{sorted(keys_only_in_694)}"
        )

    # ── Ref-id collision check ────────────────────────────────────────
    ids_694 = [_record_ref_id(r) for r in corpus_694]
    ids_125i = [_record_ref_id(r) for r in sit_125i_all]
    ids_694_set = set(ids_694)
    ids_125i_set = set(ids_125i)
    if len(ids_694_set) != len(ids_694):
        dups = [k for k, v in Counter(ids_694).items() if v > 1]
        raise SystemExit(f"[125i-d] STOP: 694 has duplicate ref_ids: {dups[:5]}")
    if len(ids_125i_set) != len(ids_125i):
        dups = [k for k, v in Counter(ids_125i).items() if v > 1]
        raise SystemExit(f"[125i-d] STOP: 125i has duplicate ref_ids: {dups[:5]}")
    overlap = ids_694_set & ids_125i_set
    if overlap:
        raise SystemExit(f"[125i-d] STOP: ref_id overlap between 694 and 125i: {sorted(overlap)[:5]}")
    print(f"[125i-d] ref_id integrity: 694={len(ids_694_set)}, 125i={len(ids_125i_set)}, "
          f"overlap=0 ✓")

    # ── Backfill 125i situations to 61-surface ────────────────────────
    nan_count_sit = 0
    for r in sit_125i_all:
        before = len(r["feat_dict"])
        _ensure_step18(r)
        after = len(r["feat_dict"])
        # Sanity: post-backfill should have exactly 61 keys
        assert after == 61, f"sit row after backfill has {after} keys; expected 61"
        for k in STEP18_KEYS:
            v = r["feat_dict"][k]
            if v is None or (isinstance(v, float) and (v != v or v == float("inf") or v == float("-inf"))):
                nan_count_sit += 1
    print(f"[125i-d] backfilled 125i situations to 61-surface; NaN/Inf count: {nan_count_sit}")

    # ── Output 1: 788-corpus (situations) ─────────────────────────────
    corpus_788 = corpus_694 + sit_125i_all
    assert len(corpus_788) == 788, f"corpus_788 should be 788; got {len(corpus_788)}"
    out_corpus = os.path.join(repo_data, "corpus_combined_788_2026-05-06.jsonl")
    _write_jsonl(out_corpus, corpus_788)
    print(f"[125i-d] wrote 788-corpus → {out_corpus}")

    # ── Output 2: 788-labels (consensus) ──────────────────────────────
    # Labels-file rows don't carry hero_cards at top level; we must look up
    # via ref_id against the corpus + situations files.
    hero_by_ref: Dict[str, str] = {}
    for c in corpus_694:
        hero_by_ref[_record_ref_id(c)] = c.get("hero_cards", "")
    for s in sit_125i_all:
        hero_by_ref[_record_ref_id(s)] = s.get("hero_cards", "")

    def _backfill_label_row(r: Dict[str, Any]) -> int:
        ref_id = r["ref_id"]
        feat = r["feat_dict"]
        if all(k in feat for k in STEP18_KEYS):
            return 0
        hc = hero_by_ref.get(ref_id)
        if not hc:
            raise SystemExit(f"[125i-d] STOP: ref_id {ref_id} has no hero_cards in corpus or 125i situations")
        nbc, pri = _backfill_step18(feat, hc)
        feat["nut_blocker_overcard_count"] = nbc
        feat["bet_call_multiway_oop_raise_pressure_index"] = pri
        r["feat_dict"] = feat
        nans = 0
        for k in STEP18_KEYS:
            v = feat[k]
            if v is None or (isinstance(v, float) and (v != v or v == float("inf") or v == float("-inf"))):
                nans += 1
        return nans

    nan_count_lbl = 0
    for r in labels_694:
        nan_count_lbl += _backfill_label_row(r)
    for r in labels_125i:
        nan_count_lbl += _backfill_label_row(r)

    print(f"[125i-d] backfilled label feat_dicts to 61-surface; NaN/Inf count: {nan_count_lbl}")

    labels_788 = labels_694 + labels_125i
    assert len(labels_788) == 788, f"labels_788 should be 788; got {len(labels_788)}"
    out_labels = os.path.join(repo_data, "corpus_combined_788_labels_2026-05-06.jsonl")
    _write_jsonl(out_labels, labels_788)
    print(f"[125i-d] wrote 788-labels → {out_labels}")

    # ── Distribution sanity ───────────────────────────────────────────
    actions = Counter(r.get("consensus_action") for r in labels_788)
    confs = Counter(round(r.get("consensus_confidence", 0.0), 1) for r in labels_788)
    print(f"[125i-d] action distribution (788): {dict(actions)}")
    print(f"[125i-d] confidence distribution (788, rounded): {dict(confs)}")

    # Per-source action distribution
    actions_694 = Counter(r.get("consensus_action") for r in labels_694)
    actions_125i = Counter(r.get("consensus_action") for r in labels_125i)
    print(f"[125i-d] action distribution (694): {dict(actions_694)}")
    print(f"[125i-d] action distribution (125i): {dict(actions_125i)}")

    # Step-18 nonzero spread
    nbc_nonzero_788 = sum(1 for r in corpus_788 if r["feat_dict"].get("nut_blocker_overcard_count", 0) > 0)
    pri_nonzero_788 = sum(1 for r in corpus_788
                          if r["feat_dict"].get("bet_call_multiway_oop_raise_pressure_index", 0.0) > 0)
    print(f"[125i-d] step-18 active counts (corpus): nbc>0 in {nbc_nonzero_788}/788; "
          f"pri>0 in {pri_nonzero_788}/788")

    return {
        "n_788_corpus": len(corpus_788),
        "n_788_labels": len(labels_788),
        "actions_788": dict(actions),
        "confs_788": dict(confs),
        "actions_694": dict(actions_694),
        "actions_125i": dict(actions_125i),
        "nbc_nonzero_788": nbc_nonzero_788,
        "pri_nonzero_788": pri_nonzero_788,
        "out_corpus": out_corpus,
        "out_labels": out_labels,
    }


if __name__ == "__main__":
    stats = assemble()
    print()
    print("[125i-d] OK; stats:")
    print(json.dumps(stats, indent=2))
