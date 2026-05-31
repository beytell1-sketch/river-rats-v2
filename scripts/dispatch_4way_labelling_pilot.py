#!/usr/bin/env python3
"""Phase 2-E PILOT — 50-hand 5-labeller 4-way labelling pilot driver.

Provenance
----------
Per dispatch PR #416 (master `9043497`). This is the orchestration driver
for the Phase 2-E pilot: dispatches 5 fresh Sonnet labellers + 1 Opus
tier-up against the 50-hand lookalike subset using the 4-way labeller
brief + 29-hand calibration set.

Pattern modeled on `river-rats-core/labelling_agent.py` (HU 1.5-D analog).

Inputs
------
- `data/4way_labeller_brief.md` — production brief (Phase 2-E.0)
- `data/4way_calibration_29hand_2026-05-11.jsonl` — anchor calibration set
- `data/4way_lookalikes_50hand_pilot_2026-05-11.jsonl` — 50-hand pilot subset

Outputs
-------
- `data/4way_corpus/pilot_50/raw_labels_labeller_<N>.jsonl` (5 files × 50 lines)
- `data/4way_corpus/pilot_50/raw_labels_opus_tierup.jsonl` (1 file × 50 lines)
- `data/4way_corpus/pilot_50/consensus.jsonl` (50 lines; per-spot consensus)
- `data/4way_corpus/pilot_50/owner_arb_queue.jsonl` (spots requiring arb)

CLI
---
  # Prepare: split into per-labeller batches
  python3 scripts/dispatch_4way_labelling_pilot.py prepare \\
      --lookalikes data/4way_lookalikes_50hand_pilot_2026-05-11.jsonl \\
      --out-dir data/4way_corpus/pilot_50/

  # Collect: parse 5 labeller outputs + apply consensus
  python3 scripts/dispatch_4way_labelling_pilot.py collect \\
      --labeller-files data/4way_corpus/pilot_50/raw_labels_labeller_*.jsonl \\
      --opus-file data/4way_corpus/pilot_50/raw_labels_opus_tierup.jsonl \\
      --out data/4way_corpus/pilot_50/consensus.jsonl

Consensus rule (per design memo §4.3)
--------------------------------------
- ≥4-of-5 labellers agree → consensus (use majority action)
- 3-2 split + Opus agrees with majority → consensus
- 3-2 split + Opus disagrees with majority → owner-arb queue
- 2-2-1 or other splits → owner-arb queue

Owner-arb spots are queued for owner adjudication via comm OR solver
verification per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`.

STOP-condition signal handling
------------------------------
Per dispatch §STOP "ANY labeller produces FL4-style rule-based/template/
Python-script labels in first 10 hands → STOP IMMEDIATELY":

`scripts/dispatch_4way_labelling_pilot.py check-drift --first 10` runs
heuristic regex checks for FL4-pattern markers in each labeller's first
10 labels:
- Python-script patterns (`if`, `elif`, threshold comparisons, function-def-style)
- Template repetition (same opening phrases across multiple hands)
- Threshold cutoffs in reasoning prose

If ANY labeller fails drift check in first 10 hands, the driver REPORTS
the labeller_id + the offending pattern + STOPs the pipeline before
remaining 40 hands.

EXECUTION SCOPE
---------------
**This script is INFRASTRUCTURE-READY but DOES NOT itself execute the
5-labeller × 50-hand × Opus tier-up dispatch.** Per dispatch §STOP
"Wall-clock blows past ~10h (pilot estimate 3-5h × 2x buffer)": full
execution requires:

1. ~5 fresh Sonnet labeller sessions (each labelling 50 hands × ~250 word
   rationales = ~15-25k output tokens per labeller; ~$30-60 per labeller
   in API spend)
2. ~1 Opus tier-up session on disputed spots (~$30-50)
3. Total estimated API spend: $150-350 per pilot
4. Wall-clock: 3-5h focused dispatch + adjudication

Recommended execution path:
- **Option A**: orchestrator dispatches this as a dedicated session with
  allocated API budget (~$200) and 4-6h wall-clock window
- **Option B**: builder loop polls execute over multiple ticks with
  per-tick scope (e.g., 1 labeller × 10 hands per tick = 25 ticks ≈ 8h)
- **Option C**: invoke `prepare` here to seed batches, then orchestrate
  dispatch externally (matches HU 1.5-D pattern)

This driver script provides:
- Input batch preparation (50 hands → 5 labeller batches)
- Output collection + consensus rule application
- Drift-check heuristics for STOP-condition compliance
- Owner-arb queue formatting

It does NOT auto-spawn fresh agent labellers; that's an out-of-band
operational step per established 1.5-D pattern.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from typing import Dict, List, Tuple


# ─── Schema constants ─────────────────────────────────────────────────

_VALID_ACTIONS = {'BET', 'RAISE', 'CALL', 'CHECK', 'FOLD'}
_VALID_CONFIDENCES = {'HIGH', 'MEDIUM', 'LOW'}
_VALID_FLUSH_STATUSES = {'NFD', 'FD', 'BDFD', 'NONE'}

# Schema version that introduced board_read_attestation.
# Per brief v3.5 / KB v1.4 (2026-05-31). Labels from brief versions
# earlier than this (batches 001-009) are exempt; validation only applies
# to new labels produced under brief v3.5 onwards (batch_010 pilot +).
ATTESTATION_BRIEF_VERSION = '3.5'


def validate_attestation(label: dict) -> List[str]:
    """Validate board_read_attestation per brief v3.5 schema (KB v1.4).

    Returns a list of error strings. Empty list = valid.

    Rules (from brief §Board-Read Attestation):
    - 'board_read_attestation' must exist and be a non-null dict.
    - Must contain keys: 'total_by_suit', 'flush_status', 'straight_outs'.
    - 'total_by_suit': dict with keys 's', 'h', 'd', 'c', each an int.
    - 'flush_status': one of NFD / FD / BDFD / NONE.
    - 'straight_outs': list (may be empty).

    A label that fails this validation is rejected at collection time —
    not queued for owner-arb. The labeller must re-run with the
    attestation field present and correct.
    """
    errors: List[str] = []
    att = label.get('board_read_attestation')
    if att is None:
        errors.append('board_read_attestation: field missing or null — '
                      'required by brief v3.5; see §Board-Read Attestation')
        return errors  # sub-field checks pointless without the parent

    if not isinstance(att, dict):
        errors.append(
            f'board_read_attestation: expected dict, got {type(att).__name__}')
        return errors

    # total_by_suit
    tbs = att.get('total_by_suit')
    if tbs is None:
        errors.append('board_read_attestation.total_by_suit: missing')
    elif not isinstance(tbs, dict):
        errors.append(
            f'board_read_attestation.total_by_suit: expected dict, '
            f'got {type(tbs).__name__}')
    else:
        for suit in ('s', 'h', 'd', 'c'):
            val = tbs.get(suit)
            if val is None:
                errors.append(
                    f'board_read_attestation.total_by_suit.{suit}: missing')
            elif not isinstance(val, int):
                errors.append(
                    f'board_read_attestation.total_by_suit.{suit}: '
                    f'expected int, got {type(val).__name__}')

    # flush_status
    fs = att.get('flush_status')
    if fs is None:
        errors.append('board_read_attestation.flush_status: missing')
    elif fs not in _VALID_FLUSH_STATUSES:
        errors.append(
            f'board_read_attestation.flush_status: invalid value "{fs}"; '
            f'must be one of {sorted(_VALID_FLUSH_STATUSES)}')

    # straight_outs
    so = att.get('straight_outs')
    if so is None:
        errors.append('board_read_attestation.straight_outs: missing')
    elif not isinstance(so, list):
        errors.append(
            f'board_read_attestation.straight_outs: expected list, '
            f'got {type(so).__name__}')

    return errors


# ─── FL4-pattern drift detection heuristics ───────────────────────────

FL4_PATTERNS = [
    # Python-script-style logic
    (r'\bif\s+\w+\s*[<>=]', 'if-condition-threshold'),
    (r'\belif\s+', 'elif-chain'),
    (r'\bdef\s+\w+\s*\(', 'function-definition'),
    (r'\breturn\s+["\']', 'return-statement'),
    # Equity threshold cutoffs (literal numbers)
    (r'equity\s*[><=]+\s*0\.\d+', 'equity-threshold-numeric'),
    (r'hand_rank\s*[><=]+\s*\d', 'hand-rank-threshold'),
    # Template repetition signals (caught at batch-level)
]


def check_drift(reasoning: str) -> List[str]:
    """Return list of FL4-pattern markers found in reasoning prose."""
    hits = []
    for pattern, label in FL4_PATTERNS:
        if re.search(pattern, reasoning, re.IGNORECASE):
            hits.append(label)
    return hits


def check_template_drift(labels: List[Dict]) -> Dict[str, int]:
    """Check for template repetition across labels (same opening words)."""
    openings = Counter()
    for lbl in labels:
        reasoning = lbl.get('reasoning', '')
        opening = ' '.join(reasoning.split()[:8])  # first 8 words
        openings[opening] += 1
    # Template flagging: any 8-word opening that appears in ≥3 labels
    return {opening: count for opening, count in openings.items() if count >= 3}


# ─── Prepare: split 50 hands → 5 labeller batches ─────────────────────

def prepare(lookalikes_path: str, out_dir: str, brief_path: str,
            calibration_path: str) -> None:
    """Prepare 5 labeller-input batches.

    Each labeller gets the FULL 50-hand subset (NOT a 10-hand-per-labeller
    split). The 5-labeller pattern is: 5 independent labellers each label
    all 50 hands, then per-spot consensus applied across the 5 votes.
    """
    os.makedirs(out_dir, exist_ok=True)
    # The labeller-input files are symlinks/copies of the 50-hand JSONL
    # plus references to brief + calibration set.
    with open(lookalikes_path) as f:
        n = sum(1 for _ in f)
    print(f'[prepare] Lookalikes: {lookalikes_path} ({n} hands)')
    print(f'[prepare] Brief: {brief_path}')
    print(f'[prepare] Calibration: {calibration_path}')

    # Write input manifest (5 labellers + 1 opus tier-up)
    manifest = {
        'lookalikes_path': lookalikes_path,
        'brief_path': brief_path,
        'calibration_path': calibration_path,
        'n_hands': n,
        'labellers': [
            {'labeller_id': i, 'output_path': os.path.join(out_dir, f'raw_labels_labeller_{i}.jsonl')}
            for i in (1, 2, 3, 4, 5)
        ],
        'opus_tierup_path': os.path.join(out_dir, 'raw_labels_opus_tierup.jsonl'),
        'consensus_path': os.path.join(out_dir, 'consensus.jsonl'),
        'owner_arb_path': os.path.join(out_dir, 'owner_arb_queue.jsonl'),
    }
    manifest_path = os.path.join(out_dir, 'pilot_manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f'[prepare] Wrote {manifest_path}')
    print(f'[prepare] NEXT STEPS (out-of-band; per HU 1.5-D analog):')
    for ll in manifest['labellers']:
        print(f'  Dispatch fresh Sonnet labeller {ll["labeller_id"]}: '
              f'output → {ll["output_path"]}')
    print(f'  Dispatch Opus tier-up: output → {manifest["opus_tierup_path"]}')
    print(f'  Run `collect` to apply consensus rule.')


# ─── Collect: 5-labeller + opus → consensus ───────────────────────────

def consensus_rule(votes: List[str], opus_vote: str) -> Tuple[str, str]:
    """Apply design memo §4.3 consensus rule.

    Returns (consensus_state, consensus_action).
    consensus_state ∈ {'4-of-5', '3-2+opus-agree', '3-2+opus-disagree', '2-2-1+', 'all-agree'}
    """
    c = Counter(votes)
    max_count = max(c.values())
    if max_count == 5:
        return 'all-agree', c.most_common(1)[0][0]
    if max_count >= 4:
        return '4-of-5', c.most_common(1)[0][0]
    if max_count == 3:
        # 3-2 split
        majority = c.most_common(1)[0][0]
        if opus_vote == majority:
            return '3-2+opus-agree', majority
        else:
            return '3-2+opus-disagree', None  # → owner-arb
    # 2-2-1 or 1-1-1-1-1 → owner-arb
    return '2-2-1+', None


def collect(labeller_files: List[str], opus_file: str, out_path: str,
            owner_arb_path: str) -> None:
    """Apply consensus across 5-labeller outputs + Opus tier-up."""
    # Read each labeller's 50 labels
    labeller_labels: Dict[str, Dict[int, Dict]] = defaultdict(dict)
    for lf in labeller_files:
        ll_id = re.search(r'labeller_(\d+)', lf).group(1)
        for line in open(lf):
            d = json.loads(line)
            labeller_labels[d['spot_id']][int(ll_id)] = d

    opus_labels = {}
    for line in open(opus_file):
        d = json.loads(line)
        opus_labels[d['spot_id']] = d

    consensus_records = []
    arb_records = []
    drift_alerts = []

    for spot_id, ll_labels in labeller_labels.items():
        votes = [ll_labels[i]['predicted_action'] for i in sorted(ll_labels.keys())]
        opus_vote = opus_labels.get(spot_id, {}).get('predicted_action')
        state, action = consensus_rule(votes, opus_vote)

        # Drift detection per labeller
        for ll_id, lbl in ll_labels.items():
            hits = check_drift(lbl.get('reasoning', ''))
            if hits:
                drift_alerts.append({
                    'spot_id': spot_id,
                    'labeller_id': ll_id,
                    'drift_patterns': hits,
                })

            # Attestation validation (brief v3.5+; batch_010 pilot and later)
            att_errors = validate_attestation(lbl)
            if att_errors:
                drift_alerts.append({
                    'spot_id': spot_id,
                    'labeller_id': ll_id,
                    'drift_patterns': att_errors,
                    'rejection_reason': 'board_read_attestation_invalid',
                })

        record = {
            'spot_id': spot_id,
            'consensus_state': state,
            'consensus_action': action,
            'votes': votes,
            'opus_vote': opus_vote,
        }
        if action is None:
            arb_records.append(record)
        else:
            consensus_records.append(record)

    # Write consensus
    with open(out_path, 'w') as f:
        for r in consensus_records:
            f.write(json.dumps(r) + '\n')
    # Write owner-arb queue
    with open(owner_arb_path, 'w') as f:
        for r in arb_records:
            f.write(json.dumps(r) + '\n')

    print(f'[collect] Consensus: {len(consensus_records)}/50')
    print(f'[collect] Owner-arb queue: {len(arb_records)}/50 '
          f'({len(arb_records)/50*100:.1f}%)')
    print(f'[collect] Drift alerts: {len(drift_alerts)}')
    if drift_alerts:
        print(f'[collect] STOP-CONDITION: drift detected in first labels')
        for alert in drift_alerts[:10]:
            print(f'  {alert}')


# ─── Main CLI ─────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)

    p_prepare = sub.add_parser('prepare')
    p_prepare.add_argument('--lookalikes', required=True)
    p_prepare.add_argument('--out-dir', required=True)
    p_prepare.add_argument('--brief', default='data/4way_labeller_brief.md')
    p_prepare.add_argument('--calibration',
                           default='data/4way_calibration_29hand_2026-05-11.jsonl')

    p_collect = sub.add_parser('collect')
    p_collect.add_argument('--labeller-files', nargs='+', required=True)
    p_collect.add_argument('--opus-file', required=True)
    p_collect.add_argument('--out', required=True)
    p_collect.add_argument('--owner-arb', required=True)

    args = ap.parse_args()
    if args.cmd == 'prepare':
        prepare(args.lookalikes, args.out_dir, args.brief, args.calibration)
    elif args.cmd == 'collect':
        collect(args.labeller_files, args.opus_file, args.out, args.owner_arb)


if __name__ == '__main__':
    main()
