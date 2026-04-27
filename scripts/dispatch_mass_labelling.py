#!/usr/bin/env python3
"""Mass-labelling preparation script (Phase 11A).

Per `MAIN_TERMINAL_MASS_LABELLING_RESOLUTION_2026-04-27.md`
(master `feb6652`): the dispatch model is **5 sonnet labellers, each
labelling all 494 hands of the corpus revision**, producing one
per-labeller JSON file matching the Phase B Protocol A schema on
master `4bce49f`.

Responsibilities of THIS script:
  1. Read corpus + v3.2 protocol
  2. Compute a unified ``ref_id`` per record
  3. Write 5 per-labeller dispatch briefs to disk; each brief contains
     the protocol verbatim, the full 494-hand summary, the output
     schema contract, and the file path the labeller must write to.
  4. Write a manifest summarising the 5 dispatch units so the builder
     (or a wrapper) can fan out one Agent tool call per unit.

THIS SCRIPT DOES NOT INVOKE THE AGENT TOOL. The Agent tool is
available only inside a Claude Code session, not from a Python
subprocess. The builder dispatches the 5 sonnet subagents from their
own session, pointing each at the corresponding brief file.

Usage:
    python3 scripts/dispatch_mass_labelling.py prepare \\
        --corpus data/corpus_revision_500_hand_2026-04-27.jsonl \\
        --protocol prompts/gto_labeller_v3.2.md \\
        --num-labellers 5 \\
        --output-dir review/mass_labelling_2026-04-27/

After preparation, the builder dispatches each labeller via the Agent
tool and the labeller writes its output to::

    review/mass_labelling_2026-04-27/labels_v3_2_labeller_<N>.json

per the schema contract embedded in the brief.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def compute_ref_id(record: Dict[str, Any]) -> str:
    """Construct a unified ref_id covering all corpus record schemas.

    Priority (matches Phase B Protocol A precedent on master ``4bce49f``):
      1. ``source_situation_id`` if present and non-null (pilot 100)
      2. ``d{deal_id}_{hero_position}_{street}`` if deal_id is present
         (Mode-A self-play 100)
      3. ``pilot_hand_id`` as fallback (Mode-B factory 294)

    Verified to yield 494 distinct ref_ids on the 494-hand corpus.
    """
    ssi = record.get('source_situation_id')
    if ssi:
        return ssi
    if 'deal_id' in record and record['deal_id'] is not None:
        return f"d{record['deal_id']}_{record['hero_position']}_{record['street']}"
    pilot_id = record.get('pilot_hand_id')
    if pilot_id:
        return pilot_id
    raise ValueError(
        f"Record has none of source_situation_id, deal_id, pilot_hand_id: "
        f"{list(record.keys())}"
    )


# Feature keys included in each hand summary. Matches the set
# `labelling_agent.py:135-149` uses for the legacy format. Kept as a
# tuple so future protocol updates can swap the projection without
# touching dispatch logic.
_HAND_FEATURE_KEYS = (
    'raw_equity', 'equity_vs_range', 'pot_odds',
    'is_ip', 'hand_category', 'is_made_hand',
    'is_strong_made', 'is_monster', 'draw_outs',
    'has_flush_draw', 'has_straight_draw',
    'danger_score', 'spr',
    'villain_top_pair_plus_pct', 'villain_air_pct',
    'villain_range_capped', 'board_favour',
    'num_callers_to_bet', 'facing_raise',
    'villain_aggression_count', 'villain_checked_back',
    'better_hand_pct', 'worse_hand_pct',
    'is_preflop_aggressor', 'villain_aggression_count',
    'is_3bet_pot', 'flush_block_pct', 'nut_flush_block',
    'straight_draw_block_pct', 'nut_made_block_pct',
)


def _format_hand_summary(record: Dict[str, Any]) -> str:
    """Render one hand as a concise multi-line block for the labeller."""
    fd = record.get('feat_dict', {}) or {}
    ref_id = compute_ref_id(record)

    lines = [
        f"--- HAND: {ref_id} ---",
        f"Hero cards: {record.get('hero_cards', '')}",
        f"Board: {record.get('board', '')}",
        f"Street: {record.get('street', '')}",
        f"Hero position: {record.get('hero_position', '')}",
        f"Villain positions: {', '.join(record.get('villain_positions', []) or [])}",
        f"Num opponents: {record.get('num_opponents', 2)}",
        f"Pot (BB): {record.get('pot', 0)}",
        f"To call (BB): {record.get('to_call', 0)}",
        f"Facing bet: {record.get('facing_bet', False)}",
        f"Action history: {record.get('prior_actions', [])}",
        "Key features:",
    ]
    seen_keys = set()
    for key in _HAND_FEATURE_KEYS:
        if key in seen_keys:
            continue
        seen_keys.add(key)
        val = fd.get(key, 0)
        if isinstance(val, float):
            lines.append(f"  {key}: {val:.4f}")
        else:
            lines.append(f"  {key}: {val}")
    return '\n'.join(lines)


def _build_brief(
    labeller_id: int,
    protocol_text: str,
    hand_summaries: List[str],
    output_path_relative: str,
    total_hands: int,
) -> str:
    """Compose the prompt brief that the dispatching builder feeds to the
    sonnet subagent for labeller_<id>.

    The brief is self-contained: the subagent reads it, applies the
    protocol, and writes labels_v3_2_labeller_<id>.json at the
    specified path.
    """
    head = (
        f"# Mass-labelling brief — labeller {labeller_id}/5\n\n"
        f"You are a v3.2 GTO poker labeller. Read the protocol below in "
        f"full BEFORE labelling. Then label each of the {total_hands} hands "
        f"in the corpus block. Apply the protocol verbatim — no "
        f"improvisation.\n\n"
        f"## Output contract\n\n"
        f"Write your labels to:\n\n"
        f"    {output_path_relative}\n\n"
        f"Schema (matches Phase B Protocol A on master 4bce49f):\n\n"
        f"```json\n"
        f"{{\n"
        f"  \"lane\": \"labeller_{labeller_id}\",\n"
        f"  \"model\": \"claude-sonnet-4-6\",\n"
        f"  \"protocol_version\": \"v3.2\",\n"
        f"  \"protocol\": \"prompts/gto_labeller_v3.2.md\",\n"
        f"  \"total_labels\": {total_hands},\n"
        f"  \"labels\": [\n"
        f"    {{\n"
        f"      \"ref_id\": \"<the HAND id from the corpus block>\",\n"
        f"      \"action\": \"BET|RAISE|CALL|CHECK|FOLD\",\n"
        f"      \"confidence\": \"HIGH|MEDIUM|LOW\",\n"
        f"      \"reasoning\": \"<one paragraph applying the v3.2 protocol>\"\n"
        f"    }},\n"
        f"    ...\n"
        f"  ]\n"
        f"}}\n"
        f"```\n\n"
        f"Hard requirements:\n"
        f"- One label per hand, exactly. No duplicates, no skips.\n"
        f"- ``ref_id`` must match the HAND id from the corpus block verbatim.\n"
        f"- ``action`` must be one of {{BET, RAISE, CALL, CHECK, FOLD}}, "
        f"uppercase.\n"
        f"- ``confidence`` must be one of {{HIGH, MEDIUM, LOW}}, uppercase.\n"
        f"- If you cannot determine an action with confidence, output\n"
        f"  ``\"action\": null`` and ``\"confidence\": \"LOW\"`` with the "
        f"reasoning explaining the refusal. Refusals must NOT exceed 5%% of "
        f"hands (<= 25 of {total_hands}).\n"
        f"- Output ONLY the JSON file at the path above. No markdown, no "
        f"chat-style prose around it.\n\n"
        f"## v3.2 protocol (verbatim)\n\n"
    )

    corpus_block = (
        f"\n\n## Corpus block ({total_hands} hands)\n\n"
        + '\n\n'.join(hand_summaries)
        + "\n"
    )

    return head + protocol_text + corpus_block


def prepare(
    corpus_path: str,
    protocol_path: str,
    num_labellers: int,
    output_dir: str,
) -> Dict[str, Any]:
    """Build the 5 per-labeller brief files + a manifest.

    Returns the manifest dict (also written to disk).
    """
    if not os.path.exists(corpus_path):
        raise FileNotFoundError(f"corpus not found: {corpus_path}")
    if not os.path.exists(protocol_path):
        raise FileNotFoundError(f"protocol not found: {protocol_path}")

    with open(corpus_path) as f:
        records = [json.loads(line) for line in f if line.strip()]
    print(f"[dispatch] loaded {len(records)} records from {corpus_path}")

    with open(protocol_path) as f:
        protocol_text = f.read()
    print(f"[dispatch] loaded protocol ({len(protocol_text)} chars)")

    ref_ids = [compute_ref_id(r) for r in records]
    if len(set(ref_ids)) != len(ref_ids):
        from collections import Counter
        dups = [k for k, v in Counter(ref_ids).items() if v > 1]
        raise RuntimeError(
            f"ref_id collisions ({len(dups)}): {dups[:5]}"
        )
    print(f"[dispatch] computed {len(ref_ids)} distinct ref_ids")

    summaries = [_format_hand_summary(r) for r in records]

    os.makedirs(output_dir, exist_ok=True)

    briefs = []
    for n in range(1, num_labellers + 1):
        out_filename = f"labels_v3_2_labeller_{n}.json"
        # Path relative to repo root for the subagent's Write call.
        out_relpath = os.path.join(
            os.path.relpath(output_dir, _REPO), out_filename
        )
        brief_text = _build_brief(
            labeller_id=n,
            protocol_text=protocol_text,
            hand_summaries=summaries,
            output_path_relative=out_relpath,
            total_hands=len(records),
        )
        brief_path = os.path.join(output_dir, f"labeller_{n}_brief.md")
        with open(brief_path, 'w') as f:
            f.write(brief_text)
        briefs.append({
            'labeller_id': n,
            'brief_path': os.path.relpath(brief_path, _REPO),
            'expected_output_path': out_relpath,
            'expected_label_count': len(records),
        })
        print(f"[dispatch] wrote brief: {brief_path} ({len(brief_text)} chars)")

    manifest = {
        'corpus_path': os.path.relpath(corpus_path, _REPO),
        'protocol_path': os.path.relpath(protocol_path, _REPO),
        'protocol_version': 'v3.2',
        'num_labellers': num_labellers,
        'total_hands': len(records),
        'output_dir': os.path.relpath(output_dir, _REPO),
        'briefs': briefs,
        'ref_ids': ref_ids,
    }
    manifest_path = os.path.join(output_dir, 'manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"[dispatch] manifest: {manifest_path}")
    print(f"[dispatch] PREPARE complete. Builder dispatches {num_labellers} "
          f"sonnet subagents — one per brief.")
    return manifest


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description='Mass labelling dispatch preparation (5 labellers × full corpus)'
    )
    sub = parser.add_subparsers(dest='command', required=True)

    p_prepare = sub.add_parser('prepare', help='Generate per-labeller briefs')
    p_prepare.add_argument(
        '--corpus', required=True,
        help='Corpus JSONL path (494-hand corpus revision)',
    )
    p_prepare.add_argument(
        '--protocol', required=True,
        help='v3.2 protocol path (prompts/gto_labeller_v3.2.md)',
    )
    p_prepare.add_argument(
        '--num-labellers', type=int, default=5,
        help='Number of sonnet labellers (default: 5)',
    )
    p_prepare.add_argument(
        '--output-dir', required=True,
        help='Output directory for briefs + manifest',
    )

    args = parser.parse_args(argv)

    if args.command == 'prepare':
        prepare(
            corpus_path=args.corpus,
            protocol_path=args.protocol,
            num_labellers=args.num_labellers,
            output_dir=args.output_dir,
        )
        return 0
    parser.print_help()
    return 1


if __name__ == '__main__':
    sys.exit(main())
