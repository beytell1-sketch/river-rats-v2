#!/usr/bin/env python3
"""Re-extract features for the 100-hand pilot corpus (R1 fix, Blueprint v3).

Corrects two structural deficits in pilot_corpus_100_hand_2026-04-26.jsonl:
  1. is_preflop_aggressor=0 for all 100 hands (opener_position never captured)
  2. spr=1.25 for 94% of hands (pot in chip units instead of BB units)

Algorithm (per Blueprint v3 Q6):
  - Reconstruct _opener_position from prior_actions (hero's own preflop actions)
  - Edge case guard: is_3bet_pot=1 → _opener_pos=None (C4 correction)
  - Convert pot from chip units to BB units: pot_bb = pot_chips / BB_CHIP_SIZE
  - Re-extract all 59 features with corrected inputs
  - Write updated JSONL; labels unchanged; fingerprints unchanged

Usage:
    python3 scripts/reextract_pilot_100_features.py \\
        --input data/pilot_corpus_100_hand_2026-04-26.jsonl \\
        --output data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \\
        --bb-chip-size 10 \\
        --verify
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from typing import Any, Dict, List, Optional

# Ensure river-rats-core is importable
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CORE = os.path.join(_REPO, 'river-rats-core')
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from feature_extractor import extract_all_features  # noqa: E402
from gto_model import FEATURE_COLUMNS  # noqa: E402
from feature_keys import F  # noqa: E402

V24_P1_BLOCKER_FEATURES = (
    F.NUT_FLUSH_BLOCK,
    F.FLUSH_DRAW_BLOCK_PCT,
    F.STRAIGHT_DRAW_BLOCK_PCT,
    F.NUT_MADE_BLOCK_PCT,
)
EXPECTED_FEAT_KEYS = list(FEATURE_COLUMNS) + list(V24_P1_BLOCKER_FEATURES)
assert len(EXPECTED_FEAT_KEYS) == 59, (
    f"59-feature contract broken: {len(EXPECTED_FEAT_KEYS)}"
)


def _reconstruct_opener_position(
    hand: Dict[str, Any],
    hero_position: str,
    is_3bet_pot: int,
) -> Optional[str]:
    """Reconstruct _opener_position from prior_actions.

    prior_actions stores hero's own preflop decisions only, formatted as
    "preflop: <position> <action>". If hero raised preflop, hero IS the opener.

    C4 edge case: if is_3bet_pot=1, opener cannot be reliably inferred
    from prior_actions alone (3-bettor ≠ original opener). Return None.
    """
    # C4 correction: 3-bet pots — default IS_PFA=0
    if is_3bet_pot == 1:
        return None

    prior_actions = hand.get('prior_actions', [])
    for action_str in prior_actions:
        action_lower = action_str.lower()
        if ('preflop' in action_lower and 'raise' in action_lower
                and hero_position.lower() in action_lower):
            return hero_position

    return None


def reextract_record(
    hand: Dict[str, Any],
    bb_chip_size: int,
) -> Dict[str, Any]:
    """Re-extract 59 features for a single pilot hand record.

    Corrects pot (chip→BB) and _opener_position reconstruction.
    Returns the corrected record with updated feat_dict.
    """
    hero_position = hand.get('hero_position', '')
    src_feat = hand.get('feat_dict', {})
    is_3bet_pot = int(src_feat.get('is_3bet_pot', 0))

    # --- R1 fix 1: reconstruct opener position ---
    opener_pos = _reconstruct_opener_position(hand, hero_position, is_3bet_pot)

    # --- R1 fix 2: convert pot to BB units ---
    pot_chips = float(hand.get('pot', 0))
    pot_bb = round(pot_chips / bb_chip_size, 4)
    to_call_chips = float(hand.get('to_call', 0))
    to_call_bb = round(to_call_chips / bb_chip_size, 4)

    villain_positions = hand.get('villain_positions', []) or ['BB']

    hand_dict = {
        'pos': hero_position,
        'fb': int(hand.get('facing_bet', False)),
        'pot': pot_bb,                   # BB units — fixes SPR
        'tc': to_call_bb,
        'st': hand.get('street', 'f')[0],
        'vp': villain_positions[0],
        'h': hand.get('hero_cards', []),
        'b': hand.get('board', []),
        'exp': 'X',
        'id': hand.get('pilot_hand_id', hand.get('source_situation_id', 'unknown')),
        '_num_opponents': hand.get('num_opponents', 1),
        '_villain_aggression_count': src_feat.get('villain_aggression_count', 0),
        '_villain_checked_back': src_feat.get('villain_checked_back', 0),
        '_villain_call_count': src_feat.get('villain_call_count', 0),
        '_num_callers_to_bet': src_feat.get('num_callers_to_bet', 0),
        '_facing_raise': src_feat.get('facing_raise', 0),
        '_is_3bet_pot': is_3bet_pot,
        '_opener_position': opener_pos,  # None if caller or 3-bet pot
    }

    full_feats = extract_all_features(hand_dict)

    feat_dict_59: Dict[str, Any] = {}
    for k in EXPECTED_FEAT_KEYS:
        v = full_feats.get(k)
        if v is None:
            feat_dict_59[k] = 0
        elif isinstance(v, float):
            feat_dict_59[k] = round(v, 6)
        elif isinstance(v, bool):
            feat_dict_59[k] = int(v)
        else:
            feat_dict_59[k] = v

    updated = dict(hand)
    updated['feat_dict'] = feat_dict_59
    # Overwrite pot fields with BB-unit values
    updated['pot'] = pot_bb
    updated['to_call'] = to_call_bb
    return updated


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def _verify(records: List[Dict[str, Any]]) -> bool:
    """Post-extraction verification per Blueprint v3 Q6.

    Asserts:
    - >= 30/100 records have is_preflop_aggressor=1 (opener reconstruction worked)
    - mean(spr) between 5.0 and 15.0 (SPR fix applied)
    """
    pfa_count = sum(
        1 for r in records
        if r['feat_dict'].get('is_preflop_aggressor', 0) == 1
    )
    spr_values = [r['feat_dict'].get('spr', 0.0) for r in records]
    mean_spr = sum(spr_values) / len(spr_values) if spr_values else 0.0

    print(f"[verify] is_preflop_aggressor=1: {pfa_count}/{len(records)}")
    print(f"[verify] mean(spr): {mean_spr:.3f}")

    ok = True
    if pfa_count < 30:
        print(f"[verify] FAIL: expected >= 30 PFA hands, got {pfa_count}",
              file=sys.stderr)
        ok = False
    else:
        print(f"[verify] PASS: PFA count {pfa_count} >= 30")

    if not (5.0 <= mean_spr <= 15.0):
        print(f"[verify] FAIL: mean(spr)={mean_spr:.3f} outside [5.0, 15.0]",
              file=sys.stderr)
        ok = False
    else:
        print(f"[verify] PASS: mean(spr)={mean_spr:.3f} in [5.0, 15.0]")

    return ok


def main(argv=None):
    p = argparse.ArgumentParser(
        description='Re-extract pilot 100-hand corpus features (R1 fix).'
    )
    p.add_argument('--input', default=os.path.join(
        _REPO, 'data', 'pilot_corpus_100_hand_2026-04-26.jsonl'),
        help='Input JSONL path')
    p.add_argument('--output', default=os.path.join(
        _REPO, 'data', 'pilot_corpus_100_hand_2026-04-26_v2.jsonl'),
        help='Output JSONL path')
    p.add_argument('--bb-chip-size', type=int, default=10,
                   help='Chip-to-BB conversion: BB_CHIP_SIZE (default 10)')
    p.add_argument('--verify', action='store_true',
                   help='Run post-extraction verification assertions')
    args = p.parse_args(argv)

    if not os.path.exists(args.input):
        print(f"[ERROR] Input not found: {args.input}", file=sys.stderr)
        return 1

    # Load
    records = []
    with open(args.input) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    print(f"[reextract] Loaded {len(records)} records from {args.input}")

    # Re-extract
    updated_records = []
    errors = 0
    for i, hand in enumerate(records):
        hand_id = hand.get('pilot_hand_id', f'record_{i}')
        try:
            updated = reextract_record(hand, args.bb_chip_size)
            updated_records.append(updated)
        except Exception as exc:
            print(f"[ERROR] {hand_id}: {exc}", file=sys.stderr)
            errors += 1

    print(f"[reextract] Re-extracted {len(updated_records)} records "
          f"({errors} errors)")

    if errors > 0:
        print(f"[ERROR] {errors} records failed re-extraction", file=sys.stderr)
        return 1

    # Verify
    if args.verify:
        ok = _verify(updated_records)
        if not ok:
            print("[ERROR] Verification failed", file=sys.stderr)
            return 1

    # Write output
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, 'w') as f:
        for rec in updated_records:
            f.write(json.dumps(rec) + '\n')

    out_sha = _sha256_file(args.output)
    print(f"[reextract] Written to: {args.output}")
    print(f"[reextract] SHA256: {out_sha}")

    # Update lock file if it exists
    lock_path = args.input.replace('.jsonl', '.lock.json')
    if os.path.exists(lock_path):
        with open(lock_path) as f:
            lock = json.load(f)
        lock['reextracted_v2_path'] = args.output
        lock['reextracted_v2_sha256'] = out_sha
        lock['reextracted_v2_bb_chip_size'] = args.bb_chip_size
        with open(lock_path, 'w') as f:
            json.dump(lock, f, indent=2)
        print(f"[reextract] Lock file updated: {lock_path}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
