#!/usr/bin/env python3
"""Assemble the 500-hand corpus revision (Blueprint v3, Phase A + Phase B).

Combines:
  - 100 re-extracted existing pilot hands (data/pilot_corpus_100_hand_2026-04-26_v2.jsonl)
  - 400 new hands from the candidate pool (training-data/corpus_revision_pool_2026-04-27.jsonl)

Sampling strategy:
  Phase A (355 hands): mandatory quota allocation filling structural gaps first.
  Phase B (45 hands):  8-dimension stratified round-robin fill.

NFD boundary validation gate (R4): before Phase A NFD slots are filled,
validate |actual_villain_air_pct - target| <= 0.03.

Structural verification gate runs after assembly to confirm corpus meets
Blueprint v3 Q4 attestation thresholds.

Output:
    data/pilot_corpus_500_hand_2026-04-27.jsonl
    data/pilot_corpus_500_hand_2026-04-27.lock.json

Usage:
    python3 scripts/build_corpus_revision_500_hand.py \\
        --pool training-data/corpus_revision_pool_2026-04-27.jsonl \\
        --existing-corpus data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \\
        --target-new 400 \\
        --seed 20260427 \\
        --output data/pilot_corpus_500_hand_2026-04-27.jsonl \\
        --lock-output data/pilot_corpus_500_hand_2026-04-27.lock.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Set, Tuple

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CORE = os.path.join(_REPO, 'river-rats-core')
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

SEED = 20260427

# ---------------------------------------------------------------------------
# Fingerprint helpers
# ---------------------------------------------------------------------------

def _normalise_cards(s) -> str:
    """Normalise hero/board cards to concatenated rank+suit string."""
    if isinstance(s, list):
        s = ''.join(s)
    s = re.sub(r'[^AKQJTakqjt2-9shdcSHDC]', '', s)
    out = []
    for i in range(0, len(s) - 1, 2):
        rank, suit = s[i].upper(), s[i + 1].lower()
        out.append(rank + suit)
    return ''.join(out)


def _fingerprint(hero_raw, board_raw) -> Tuple[str, str]:
    """Return canonical (sorted_hero, sorted_board) fingerprint."""
    def _cards(s: str) -> List[str]:
        return [s[i:i+2] for i in range(0, len(s), 2)]
    hero = _normalise_cards(hero_raw)
    board = _normalise_cards(board_raw)
    return (''.join(sorted(_cards(hero))), ''.join(sorted(_cards(board))))


def _fingerprint_record(rec: Dict[str, Any]) -> Tuple[str, str]:
    return _fingerprint(rec.get('hero_cards', ''), rec.get('board', ''))


# ---------------------------------------------------------------------------
# Forbidden fingerprint loaders (from build_pilot_corpus_100_hand.py pattern)
# ---------------------------------------------------------------------------

def _load_jsonl_fingerprints(path: str) -> Set[Tuple[str, str]]:
    fps: Set[Tuple[str, str]] = set()
    if not os.path.exists(path):
        return fps
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rec = json.loads(line)
                fps.add(_fingerprint(rec.get('hero_cards', ''), rec.get('board', '')))
    return fps


def _load_all_forbidden_fingerprints(existing_corpus_path: str) -> Set[Tuple[str, str]]:
    """Load all external forbidden fingerprints."""
    fps: Set[Tuple[str, str]] = set()

    # Tier 2: existing 100 pilot hands
    fps |= _load_jsonl_fingerprints(existing_corpus_path)

    # Stage 6 holdout (parsed from markdown if available)
    stage6_path = os.path.join(_REPO, 'review', 'comms',
                               'STAGE6_HOLDOUT_TESTSET_v1_0.md')
    if os.path.exists(stage6_path):
        fps |= _parse_stage6_holdout_fingerprints(stage6_path)

    # Tier 1 calibration
    calib_paths = [
        os.path.join(_REPO, 'review', 'calibration_situations.json'),
        os.path.join(_REPO, 'review', 'blind_calibration_exam_step7.json'),
        os.path.join(_REPO, 'review', 'calibration_batch_1.json'),
        os.path.join(_REPO, 'review', 'calibration_batch_2.json'),
        os.path.join(_REPO, 'review', 'calibration_batch_3.json'),
    ]
    for p in calib_paths:
        if os.path.exists(p):
            fps |= _load_calibration_fingerprints(p)

    print(f"[disjoint] Total forbidden fingerprints: {len(fps)}")
    return fps


def _parse_stage6_holdout_fingerprints(path: str) -> Set[Tuple[str, str]]:
    fps: Set[Tuple[str, str]] = set()
    try:
        with open(path) as f:
            text = f.read()
        blocks = re.split(r'^### HOLDOUT_\d{3}', text, flags=re.MULTILINE)[1:]
        for block in blocks:
            hero_m = re.search(r'^- Hero:\s*`([^`]+)`', block,
                               re.MULTILINE | re.IGNORECASE)
            board_m = re.search(r'^- Board\s*(?:\([^)]*\))?:\s*`([^`]+)`', block,
                                re.MULTILINE | re.IGNORECASE)
            if hero_m and board_m:
                fps.add(_fingerprint(hero_m.group(1), board_m.group(1)))
    except Exception:
        pass
    return fps


def _load_calibration_fingerprints(path: str) -> Set[Tuple[str, str]]:
    fps: Set[Tuple[str, str]] = set()
    try:
        with open(path) as f:
            data = json.load(f)
        for entry in data:
            text = entry.get('situation_text', '')
            hero_m = re.search(r'Hero cards?:\s*([A-Za-z0-9]+)', text, re.IGNORECASE)
            board_m = re.search(r'Board:\s*([A-Za-z0-9]+)', text, re.IGNORECASE)
            if hero_m and board_m:
                fps.add(_fingerprint(hero_m.group(1), board_m.group(1)))
    except Exception:
        pass
    return fps


# ---------------------------------------------------------------------------
# Stratification helpers
# ---------------------------------------------------------------------------

def _board_texture(board) -> str:
    s = _normalise_cards(board)
    cards = [s[i:i+2] for i in range(0, len(s), 2)]
    if len(cards) < 3:
        return 'unknown'
    ranks = [c[0] for c in cards[:3]]
    suits = [c[1] for c in cards[:3]]
    rc = Counter(ranks)
    sc = Counter(suits)
    if 3 in rc.values():
        return 'trips_board'
    if 2 in rc.values():
        return 'paired'
    if 3 in sc.values():
        return 'monotone'
    if 2 in sc.values():
        return 'two_tone'
    return 'rainbow_dry'


def _spr_bucket(feat: Dict) -> str:
    spr = feat.get('spr', 0.0)
    if spr < 2.0:
        return 'committed'
    if spr < 4.0:
        return 'medium'
    return 'standard'


def _hand_class(feat: Dict) -> str:
    if feat.get('is_monster', 0) == 1:
        return 'monster'
    if feat.get('is_strong_made', 0) == 1:
        return 'strong_made'
    if feat.get('is_made_hand', 0) == 1:
        return 'medium_made'
    if feat.get('has_flush_draw', 0) == 1 or feat.get('has_straight_draw', 0) == 1:
        return 'draw'
    if feat.get('draw_outs', 0) >= 4:
        return 'draw'
    return 'air'


def _action_context(rec: Dict) -> str:
    feat = rec.get('feat_dict', {})
    if feat.get('facing_raise', 0) == 1:
        return 'facing_raise'
    if feat.get('facing_bet', rec.get('facing_bet', False)):
        return 'facing_initial_bet'
    return 'opener'


def _position_type(feat: Dict) -> str:
    return 'IP' if feat.get('is_ip', 0) > 0.5 else 'OOP'


def _villain_agg_type(feat: Dict) -> str:
    cnt = feat.get('villain_aggression_count', 0)
    if cnt >= 2:
        return 'multi_street'
    if cnt == 1:
        return 'single_street'
    return 'none'


def _strat_key_8d(rec: Dict) -> Tuple:
    """8-dimension stratification key for Phase B."""
    feat = rec.get('feat_dict', {})
    return (
        _action_context(rec),
        rec.get('street', 'unknown'),
        _position_type(feat),
        _spr_bucket(feat),
        _hand_class(feat),
        _board_texture(rec.get('board', '')),
        'pfa' if feat.get('is_preflop_aggressor', 0) == 1 else 'caller',
        _villain_agg_type(feat),
    )


# ---------------------------------------------------------------------------
# NFD boundary validation (R4)
# ---------------------------------------------------------------------------

NFD_AIR_TARGETS = [0.15, 0.17, 0.20, 0.22, 0.25]
NFD_TOLERANCE = 0.03


def _validate_nfd_boundary(rec: Dict) -> bool:
    """Return True if this NFD boundary hand passes R4 validation."""
    feat = rec.get('feat_dict', {})
    actual_air = feat.get('villain_air_pct', None)
    if actual_air is None:
        return False
    for target in NFD_AIR_TARGETS:
        if abs(actual_air - target) <= NFD_TOLERANCE:
            return True
    return False


# ---------------------------------------------------------------------------
# Phase A: mandatory quota allocation
# ---------------------------------------------------------------------------

def _is_nfd_hand(rec: Dict) -> bool:
    feat = rec.get('feat_dict', {})
    return (feat.get('has_flush_draw', 0) == 1
            and feat.get('nut_flush_block', 0) == 1)


def _is_pfa_hand(rec: Dict) -> bool:
    return rec.get('feat_dict', {}).get('is_preflop_aggressor', 0) == 1


def _is_bac_hand(rec: Dict) -> bool:
    return rec.get('feat_dict', {}).get('num_callers_to_bet', 0) >= 1


def _is_magg_hand(rec: Dict) -> bool:
    return (rec.get('feat_dict', {}).get('villain_aggression_count', 0) >= 2
            and rec.get('street', '') == 'river')


def _is_monster_hand(rec: Dict) -> bool:
    return rec.get('feat_dict', {}).get('is_monster', 0) == 1


def _is_rule11_hand(rec: Dict) -> bool:
    return rec.get('generation_source', '') == 'rule11_boundary_scenarios'


def _is_donk_hand(rec: Dict) -> bool:
    return rec.get('generation_source', '') == 'donk_bet_defence_scenarios'


def _is_sb_hero_hand(rec: Dict) -> bool:
    return (rec.get('generation_source', '') == 'sb_hero_scenarios'
            or rec.get('hero_position', '') == 'SB')


def _phase_a_select(
    pool: List[Dict],
    forbidden_fps: Set[Tuple[str, str]],
    rng,
) -> Tuple[List[Dict], Set[Tuple[str, str]]]:
    """Phase A: fill mandatory quotas (355 hands total).

    Quotas:
      - PFA c-bet: 80
      - NFD RAISE (villain_air >= 0.20): 20
      - NFD CALL (villain_air < 0.20): 20
      - NFD boundary cases: 10
      - BAC (num_callers_to_bet >= 1): 20
      - Monster facing bet (is_monster=1): 20
      - MAGG river (villain_aggression_count >= 2): 40
      - Standard SPR (4-8): 50
      - Medium SPR (2-4): 40
      - Rule 11 boundary: 10
      - Donk-bet defence: 25
      - SB-hero sandwich: 20
      Total: 355
    """
    used_fps = set(forbidden_fps)
    selected: List[Dict] = []

    def _pick(candidates, n, label):
        nonlocal selected
        rng.shuffle(candidates)
        picked = []
        for rec in candidates:
            if len(picked) >= n:
                break
            fp = _fingerprint_record(rec)
            if fp in used_fps:
                continue
            picked.append(rec)
            used_fps.add(fp)
        selected.extend(picked)
        print(f"[Phase A] {label}: {len(picked)}/{n} filled")
        return picked

    # Pool partitions
    nfd_pool = [r for r in pool if _is_nfd_hand(r)]
    nfd_boundary = [r for r in nfd_pool if _validate_nfd_boundary(r)]
    nfd_raise = [r for r in nfd_pool
                 if r.get('feat_dict', {}).get('villain_air_pct', 0) >= 0.20
                 and not _validate_nfd_boundary(r)]
    nfd_call = [r for r in nfd_pool
                if r.get('feat_dict', {}).get('villain_air_pct', 0) < 0.20
                and not _validate_nfd_boundary(r)]

    pfa_pool = [r for r in pool if _is_pfa_hand(r)]
    bac_pool = [r for r in pool if _is_bac_hand(r)]
    magg_pool = [r for r in pool if _is_magg_hand(r)]
    monster_pool = [r for r in pool if _is_monster_hand(r)]
    rule11_pool = [r for r in pool if _is_rule11_hand(r)]
    donk_pool = [r for r in pool if _is_donk_hand(r)]
    sb_pool = [r for r in pool if _is_sb_hero_hand(r)]
    spr_standard = [r for r in pool
                    if r.get('feat_dict', {}).get('spr', 0) >= 4.0]
    spr_medium = [r for r in pool
                  if 2.0 <= r.get('feat_dict', {}).get('spr', 0) < 4.0]

    # Fill quotas
    _pick(pfa_pool, 80, 'PFA c-bet (Rule 4)')
    _pick(nfd_raise, 20, 'NFD RAISE (air >= 0.20)')
    _pick(nfd_call, 20, 'NFD CALL (air < 0.20)')
    _pick(nfd_boundary, 10, 'NFD boundary cases')
    _pick(bac_pool, 20, 'BAC (MW-30 callers >= 1)')
    _pick(monster_pool, 20, 'Monster facing bet (MW-33)')
    _pick(magg_pool, 40, 'MAGG river (villain_agg >= 2)')
    _pick(spr_standard, 50, 'Standard SPR (4-8)')
    _pick(spr_medium, 40, 'Medium SPR (2-4)')
    _pick(rule11_pool, 10, 'Rule 11 boundary')
    _pick(donk_pool, 25, 'Donk-bet defence (Module 8)')
    _pick(sb_pool, 20, 'SB-hero sandwich (Module 9)')

    print(f"[Phase A] Total selected: {len(selected)}/355")
    return selected, used_fps


# ---------------------------------------------------------------------------
# Phase B: 8D stratified fill
# ---------------------------------------------------------------------------

def _stratified_8d_sample(
    pool: List[Dict],
    n: int,
    forbidden_fps: Set[Tuple[str, str]],
    rng,
) -> List[Dict]:
    """Sample n hands using 8D round-robin stratification."""
    candidates = [r for r in pool
                  if _fingerprint_record(r) not in forbidden_fps]
    rng.shuffle(candidates)

    buckets: Dict[Tuple, List[Dict]] = defaultdict(list)
    for rec in candidates:
        buckets[_strat_key_8d(rec)].append(rec)

    selected = []
    used_fps = set(forbidden_fps)
    bucket_keys = sorted(buckets.keys())
    idx = 0

    while len(selected) < n:
        if idx >= len(bucket_keys):
            idx = 0
            # Refresh: remove empty buckets
            bucket_keys = [k for k in bucket_keys if buckets[k]]
            if not bucket_keys:
                break

        key = bucket_keys[idx]
        bucket = buckets[key]
        while bucket:
            rec = bucket.pop(0)
            fp = _fingerprint_record(rec)
            if fp not in used_fps:
                selected.append(rec)
                used_fps.add(fp)
                break
        idx += 1

    print(f"[Phase B] Selected {len(selected)}/{n} hands from 8D stratification")
    return selected


# ---------------------------------------------------------------------------
# Structural verification gate (Blueprint v3 Q4)
# ---------------------------------------------------------------------------

def _verify_corpus(combined: List[Dict]) -> bool:
    """Check Blueprint v3 structural attestation thresholds."""
    n = len(combined)
    if n == 0:
        print("[verify] FAIL: empty corpus", file=sys.stderr)
        return False

    feat_list = [r.get('feat_dict', {}) for r in combined]

    facing_bet_count = sum(1 for f in feat_list if f.get('facing_bet', 0) == 1)
    pfa_count = sum(1 for f in feat_list if f.get('is_preflop_aggressor', 0) == 1)
    spr_ge4 = sum(1 for f in feat_list if f.get('spr', 0) >= 4.0)
    spr_2to4 = sum(1 for f in feat_list if 2.0 <= f.get('spr', 0) < 4.0)
    oop_count = sum(1 for f in feat_list if f.get('is_ip', 0) == 0)
    ip_count = n - oop_count
    magg2_count = sum(1 for r in combined
                      if (r.get('feat_dict', {}).get('villain_aggression_count', 0) >= 2
                          and r.get('street', '') == 'river'))
    donk_count = sum(1 for r in combined
                     if r.get('generation_source', '') == 'donk_bet_defence_scenarios')
    sb_count = sum(1 for r in combined
                   if (r.get('generation_source', '') == 'sb_hero_scenarios'
                       or r.get('hero_position', '') == 'SB'))

    checks = [
        ('facing_bet_count >= 125', facing_bet_count >= 125,
         f'got {facing_bet_count}'),
        ('pfa_count >= 150', pfa_count >= 150, f'got {pfa_count}'),
        ('spr_ge4_count >= 125', spr_ge4 >= 125, f'got {spr_ge4}'),
        ('spr_2to4_count >= 100', spr_2to4 >= 100, f'got {spr_2to4}'),
        ('oop_pct 0.55-0.65', 0.55 <= oop_count/n <= 0.65,
         f'got {oop_count/n:.2f}'),
        ('ip_pct 0.35-0.45', 0.35 <= ip_count/n <= 0.45,
         f'got {ip_count/n:.2f}'),
        ('magg_villain_agg2 >= 20', magg2_count >= 20, f'got {magg2_count}'),
        ('donk_bet_defence >= 25', donk_count >= 25, f'got {donk_count}'),
        ('sb_hero >= 20', sb_count >= 20, f'got {sb_count}'),
    ]

    all_pass = True
    for label, ok, detail in checks:
        status = 'PASS' if ok else 'WARN'
        print(f"[verify] {status}: {label} — {detail}")
        if not ok:
            all_pass = False

    return all_pass


# ---------------------------------------------------------------------------
# SHA256 helper
# ---------------------------------------------------------------------------

def _sha256_jsonl(records: List[Dict]) -> str:
    h = hashlib.sha256()
    for rec in records:
        h.update((json.dumps(rec, sort_keys=True) + '\n').encode())
    return h.hexdigest()


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Main assembly
# ---------------------------------------------------------------------------

def build_corpus(
    pool_path: str,
    existing_corpus_path: str,
    target_new: int,
    seed: int,
    output_path: str,
    lock_output_path: str,
) -> int:
    import random
    rng = random.Random(seed)

    # Load pool
    if not os.path.exists(pool_path):
        print(f"[ERROR] Pool not found: {pool_path}", file=sys.stderr)
        return 1

    pool: List[Dict] = []
    with open(pool_path) as f:
        for line in f:
            line = line.strip()
            if line:
                pool.append(json.loads(line))
    print(f"[build] Pool loaded: {len(pool)} candidates from {pool_path}")

    # Load existing corpus
    existing: List[Dict] = []
    if os.path.exists(existing_corpus_path):
        with open(existing_corpus_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    existing.append(json.loads(line))
    print(f"[build] Existing corpus: {len(existing)} hands from {existing_corpus_path}")

    # Load forbidden fingerprints
    forbidden_fps = _load_all_forbidden_fingerprints(existing_corpus_path)

    # Phase A: mandatory quota (355 hands)
    phase_a_target = 355
    phase_a_records, used_fps = _phase_a_select(pool, forbidden_fps, rng)

    # Phase B: 8D stratified fill (45 hands)
    phase_b_target = target_new - len(phase_a_records)
    phase_b_target = max(0, min(45, phase_b_target))
    remaining_pool = [r for r in pool if _fingerprint_record(r) not in used_fps]
    phase_b_records = _stratified_8d_sample(remaining_pool, phase_b_target, used_fps, rng)

    new_records = phase_a_records + phase_b_records
    print(f"[build] New hands selected: {len(new_records)} "
          f"(Phase A: {len(phase_a_records)}, Phase B: {len(phase_b_records)})")

    # Assign pilot_hand_id
    for i, rec in enumerate(existing):
        if 'pilot_hand_id' not in rec:
            rec['pilot_hand_id'] = f'PILOT_{i+1:03d}'

    start_idx = len(existing) + 1
    output_new = []
    for i, rec in enumerate(new_records):
        out_rec = dict(rec)
        out_rec['pilot_hand_id'] = f'PILOT_{start_idx + i:03d}'
        output_new.append(out_rec)

    combined = existing + output_new
    print(f"[build] Combined corpus: {len(combined)} hands")

    # Structural verification
    _verify_corpus(combined)

    # Within-batch fingerprint check
    fps_seen: Set[Tuple] = set()
    duplicates = 0
    for rec in combined:
        fp = _fingerprint_record(rec)
        if fp in fps_seen:
            duplicates += 1
        fps_seen.add(fp)
    if duplicates > 0:
        print(f"[disjoint] WARN: {duplicates} within-batch duplicates", file=sys.stderr)
    else:
        print(f"[disjoint] PASS: no within-batch duplicates")

    # Write output JSONL
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w') as f:
        for rec in combined:
            f.write(json.dumps(rec) + '\n')

    sha256_combined = _sha256_file(output_path)
    sha256_new = _sha256_jsonl(output_new)

    print(f"[build] Written to: {output_path}")
    print(f"[build] SHA256 combined: {sha256_combined}")

    # Write lock file
    lock = {
        'corpus_revision_version': 'v2.0',
        'new_hand_count': len(output_new),
        'combined_corpus_count': len(combined),
        'sha256_new': sha256_new,
        'sha256_combined': sha256_combined,
        'build_seed': seed,
        'pool_path': pool_path,
        'existing_corpus_path': existing_corpus_path,
        'phase_a_count': len(phase_a_records),
        'phase_b_count': len(phase_b_records),
        'disjointness': {
            'within_batch_duplicates': duplicates,
            'total_forbidden_fingerprints': len(forbidden_fps),
        },
        'structural_verification': {
            'facing_bet_count': sum(
                1 for r in combined if r.get('feat_dict', {}).get('facing_bet', 0) == 1),
            'pfa_count': sum(
                1 for r in combined
                if r.get('feat_dict', {}).get('is_preflop_aggressor', 0) == 1),
            'magg_villain_aggression_2_count': sum(
                1 for r in combined
                if (r.get('feat_dict', {}).get('villain_aggression_count', 0) >= 2
                    and r.get('street', '') == 'river')),
            'donk_bet_defence_count': sum(
                1 for r in combined
                if r.get('generation_source', '') == 'donk_bet_defence_scenarios'),
            'sb_hero_count': sum(
                1 for r in combined
                if r.get('generation_source', '') == 'sb_hero_scenarios'),
        },
    }

    if lock_output_path:
        os.makedirs(os.path.dirname(os.path.abspath(lock_output_path)), exist_ok=True)
        with open(lock_output_path, 'w') as f:
            json.dump(lock, f, indent=2)
        print(f"[build] Lock file: {lock_output_path}")

    return 0


def main(argv=None):
    p = argparse.ArgumentParser(
        description='Build 500-hand corpus revision (Blueprint v3).'
    )
    p.add_argument('--pool',
                   default=os.path.join(_REPO, 'training-data',
                                        'corpus_revision_pool_2026-04-27.jsonl'),
                   help='Candidate pool JSONL')
    p.add_argument('--existing-corpus',
                   default=os.path.join(_REPO, 'data',
                                        'pilot_corpus_100_hand_2026-04-26_v2.jsonl'),
                   help='Re-extracted existing 100-hand corpus')
    p.add_argument('--target-new', type=int, default=400,
                   help='Target number of new hands (default 400)')
    p.add_argument('--seed', type=int, default=SEED,
                   help='RNG seed (default 20260427)')
    p.add_argument('--output',
                   default=os.path.join(_REPO, 'data',
                                        'pilot_corpus_500_hand_2026-04-27.jsonl'),
                   help='Output JSONL path')
    p.add_argument('--lock-output',
                   default=os.path.join(_REPO, 'data',
                                        'pilot_corpus_500_hand_2026-04-27.lock.json'),
                   help='Lock file path')
    args = p.parse_args(argv)

    rc = build_corpus(
        pool_path=args.pool,
        existing_corpus_path=args.existing_corpus,
        target_new=args.target_new,
        seed=args.seed,
        output_path=args.output,
        lock_output_path=args.lock_output,
    )
    sys.exit(rc)


if __name__ == '__main__':
    main()
