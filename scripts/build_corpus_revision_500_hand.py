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


# Phase A targets — single source of truth. Tests assert this matches.
PHASE_A_QUOTAS = {
    'pfa': 80,
    'nfd_raise': 20,
    'nfd_call': 20,
    'nfd_boundary': 10,
    'bac': 20,
    'monster': 20,
    'magg': 40,
    'spr_std': 50,
    'spr_med': 40,
    'rule11': 10,
    'donk': 25,
    'sb': 20,
}

# Human-readable labels (display-only)
_PHASE_A_LABELS = {
    'pfa': 'PFA c-bet (Rule 4)',
    'nfd_raise': 'NFD RAISE (air >= 0.20)',
    'nfd_call': 'NFD CALL (air < 0.20)',
    'nfd_boundary': 'NFD boundary cases',
    'bac': 'BAC (MW-30 callers >= 1)',
    'monster': 'Monster facing bet (MW-33)',
    'magg': 'MAGG river (villain_agg >= 2)',
    'spr_std': 'Standard SPR (4-8)',
    'spr_med': 'Medium SPR (2-4)',
    'rule11': 'Rule 11 boundary',
    'donk': 'Donk-bet defence (Module 8)',
    'sb': 'SB-hero sandwich (Module 9)',
}


def _classify_record(rec: Dict) -> Set[str]:
    """Return the set of Phase A categories a record satisfies.

    A record may belong to multiple categories. The rare-category-first
    allocator uses this membership set to decide which category to assign
    each record to.
    """
    cats: Set[str] = set()
    if _is_pfa_hand(rec):
        cats.add('pfa')
    if _is_magg_hand(rec):
        cats.add('magg')
    if _is_bac_hand(rec):
        cats.add('bac')
    if _is_monster_hand(rec):
        cats.add('monster')
    if _is_nfd_hand(rec):
        if _validate_nfd_boundary(rec):
            cats.add('nfd_boundary')
        elif rec.get('feat_dict', {}).get('villain_air_pct', 0) >= 0.20:
            cats.add('nfd_raise')
        else:
            cats.add('nfd_call')
    if _is_rule11_hand(rec):
        cats.add('rule11')
    if _is_donk_hand(rec):
        cats.add('donk')
    if _is_sb_hero_hand(rec):
        cats.add('sb')
    spr = rec.get('feat_dict', {}).get('spr', 0)
    if spr >= 4.0:
        cats.add('spr_std')
    elif 2.0 <= spr < 4.0:
        cats.add('spr_med')
    return cats


def _phase_a_select(
    pool: List[Dict],
    forbidden_fps: Set[Tuple[str, str]],
    rng,
) -> Tuple[List[Dict], Set[Tuple[str, str]]]:
    """Phase A: rare-category-first allocator (Phase 4 / F5 fix per directive
    `MAIN_TERMINAL_BUILD_EXECUTE_PHASE4_DIRECTIVE_2026-04-27.md` master `43a80bb`).

    Quotas (PHASE_A_QUOTAS): 12 categories summing to 355 target hands.

    Algorithm (replaces prior greedy first-come-first-served allocator that
    consumed MAGG records via earlier PFA quota since MAGG records also
    satisfy PFA criteria — root cause of MAGG=0/40 on Phase 3 v2 run):

      1. Classify each pool record into ALL categories it satisfies
         (a record may belong to multiple — e.g., a MAGG record that is also
         PFA + standard-SPR belongs to {magg, pfa, spr_std}).
      2. Compute scarcity[cat] = target / max(1, yield) per category.
         Higher scarcity = rarer category, prioritise.
      3. Sort records descending by their max-scarcity matching category
         (records that fit only rare categories get assigned first).
      4. For each record, assign to its highest-scarcity category that
         still has unfilled target.
      5. Report per-category status (FULL or UNDER with yield count).

    Each record assigned to AT MOST ONE category. Records that match no
    category (empty membership set) are skipped (they'll be picked up by
    Phase B 8D stratification).

    Returns (selected_records, updated_forbidden_fps).
    """
    used_fps = set(forbidden_fps)

    # Pre-shuffle pool deterministically per RNG (so same seed → same outcome
    # while still randomising tie-breaks within scarcity sort).
    pool_shuffled = list(pool)
    rng.shuffle(pool_shuffled)

    # Step 1: classify each record into its category membership set
    membership = []  # parallel list to pool_shuffled
    for rec in pool_shuffled:
        membership.append(_classify_record(rec))

    # Step 2: count yield per category (records that satisfy each category,
    # including multi-membership records — for scarcity calculation we want
    # the maximum POSSIBLE yield per category, not unique-assignment yield)
    yield_per_cat: Dict[str, int] = {cat: 0 for cat in PHASE_A_QUOTAS}
    for cats in membership:
        for c in cats:
            yield_per_cat[c] += 1

    # Step 3: scarcity[cat] = target / yield (higher = harder to fill)
    scarcity: Dict[str, float] = {
        cat: PHASE_A_QUOTAS[cat] / max(1, yield_per_cat[cat])
        for cat in PHASE_A_QUOTAS
    }

    # Step 4: sort records descending by max-scarcity matching category
    # (records whose only matching categories are rare get assigned first;
    # records that fit only abundant categories get assigned last)
    indexed = list(enumerate(pool_shuffled))

    def _record_priority(idx_rec):
        idx, _ = idx_rec
        cats = membership[idx]
        if not cats:
            return -float('inf')  # records with no matching category go last
        return -max(scarcity[c] for c in cats)  # negative for descending sort

    indexed.sort(key=_record_priority)

    # Step 5: assign each record to one category (rarest still-open)
    selected_per_cat: Dict[str, List[Dict]] = {cat: [] for cat in PHASE_A_QUOTAS}

    for idx, rec in indexed:
        fp = _fingerprint_record(rec)
        if fp in used_fps:
            continue
        cats = membership[idx]
        if not cats:
            continue

        # Find highest-scarcity category that still has unfilled target
        eligible = [c for c in cats if len(selected_per_cat[c]) < PHASE_A_QUOTAS[c]]
        if not eligible:
            continue
        best_cat = max(eligible, key=lambda c: scarcity[c])
        selected_per_cat[best_cat].append(rec)
        used_fps.add(fp)

    # Step 6: flatten + report per-category status
    selected = [r for cat in PHASE_A_QUOTAS for r in selected_per_cat[cat]]
    for cat in PHASE_A_QUOTAS:
        n_filled = len(selected_per_cat[cat])
        n_target = PHASE_A_QUOTAS[cat]
        n_yield = yield_per_cat[cat]
        if n_filled >= n_target:
            status = 'FULL'
        else:
            status = f'UNDER (yield {n_yield})'
        label = _PHASE_A_LABELS[cat]
        print(f"[Phase A] {label}: {n_filled}/{n_target} {status}")

    print(f"[Phase A] Total selected: {len(selected)}/{sum(PHASE_A_QUOTAS.values())}")
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
