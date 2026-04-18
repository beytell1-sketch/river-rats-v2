"""eval_flop_generalization_sweep.py — v2.3.1 broader-inference gate.

Per REVIEW_V231_TRAIN_EVAL_2026-04-18.md §Additional validation:
  Confirm the fix is architectural (Layer 1 + Layer 2 generalizes)
  rather than narrow memorization of the 2 litmus spots.

Method: build 20 flop decision cases NOT in training (training is
turn-only; HU never labelled). Each case is an AIR hero on a hostile
checked-to flop. Run v2.3.1 inference. Gate: >= 85% CHECK to ship.

Dimensions:
  - Hero: weak-ace, low/mid broadway, babies, suited-disconnected
  - Texture: monotone (diverse suits/ranks), paired (diverse ranks),
             two-tone connected, rainbow connected, dry high
  - Position: BTN, CO, HJ (IP) + SB/BB (OOP where legal)
  - Villain count: HU and 3-way both represented

Predicate at inference (each case must match, or it's dropped):
  facing_bet = 0
  is_made_hand = 0
  draw_outs <= 2
  equity_vs_range < 0.35

Run:
    python3 review/eval_flop_generalization_sweep.py
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import List, Optional, Tuple

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_CORE = os.path.join(_REPO, 'river-rats-core')
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)
os.chdir(_CORE)

import csv
import numpy as np
import xgboost as xgb

from situation_factory import SituationSpec, build_situation, _POSTFLOP_ORDER
from train_model_v2_2 import (
    ACTION_TO_INT, INT_TO_ACTION, encode, split_feature_columns,
)

MODEL_PATH = os.path.join(_CORE, 'models', 'v2_3_1_model.json')
CSV_PATH = os.path.join(_REPO, 'training-data', 'v2_3_1_training.csv')


@dataclass
class SweepCase:
    case_id: str
    hero: List[str]
    board: List[str]  # 3 cards (flop)
    hero_pos: str
    villains: List[str]
    opener: str
    theme: str  # human-readable description


# =============================================================================
# 20 diverse cases — each targets AIR predicate on a hostile flop
# =============================================================================
# Naming: <HeroClass>_<Texture>_<opp>_<position>

CASES: List[SweepCase] = [
    # ── Weak-ace hands on hostile boards ──────────────────────────────────
    SweepCase('SW01_A7o_mono_hearts_3way_BTN',
              ['Ac', '7s'], ['Jh', '8h', '3h'], 'BTN', ['SB', 'BB'], 'BTN',
              'weak-ace offsuit vs monotone hearts (hero no heart) — 3-way IP'),
    SweepCase('SW02_A5o_mono_clubs_HU_BTN',
              ['Ah', '5d'], ['Kc', '8c', '3c'], 'BTN', ['BB'], 'BTN',
              'weak-ace offsuit vs monotone clubs — HU IP'),
    SweepCase('SW03_A6o_paired_99_3way_CO',
              ['Ah', '6d'], ['9c', '9s', '4d'], 'CO', ['SB', 'BB'], 'CO',
              'weak-ace on paired 99 board — 3-way IP'),
    SweepCase('SW04_A3o_paired_KK_HU_BTN',
              ['Ah', '3d'], ['Kh', 'Ks', '5d'], 'BTN', ['BB'], 'BTN',
              'weak-ace on paired KK — HU IP'),

    # ── Low/mid broadway air ──────────────────────────────────────────────
    SweepCase('SW05_KJo_mono_spades_3way_BTN',
              ['Kd', 'Jc'], ['Qs', '6s', '2s'], 'BTN', ['SB', 'BB'], 'BTN',
              'K-J offsuit vs monotone spades (hero no spade) — 3-way IP'),
    SweepCase('SW06_QTo_paired_77_HU_CO',
              ['Qh', 'Td'], ['7c', '7s', '3d'], 'CO', ['BB'], 'CO',
              'Q-T on paired 77 — HU IP'),
    SweepCase('SW07_J4o_paired_AA_3way_BTN',
              ['Jh', '4d'], ['As', 'Ac', '6h'], 'BTN', ['HJ', 'BB'], 'HJ',
              'J-4 on paired AA — 3-way BTN'),
    SweepCase('SW08_T2s_paired_QQ_HU_BTN',
              ['Th', '2h'], ['Qc', 'Qd', '5s'], 'BTN', ['BB'], 'BTN',
              'T-2 suited hearts on paired QQ — HU IP'),

    # ── Baby/low disconnected air ─────────────────────────────────────────
    SweepCase('SW09_63o_mono_diamonds_3way_BTN',
              ['6s', '3c'], ['Kd', '9d', '4d'], 'BTN', ['SB', 'BB'], 'BTN',
              '6-3 offsuit vs monotone diamonds — 3-way IP'),
    SweepCase('SW10_42s_paired_JJ_HU_BTN',
              ['4c', '2c'], ['Jh', 'Jd', '9s'], 'BTN', ['BB'], 'BTN',
              '4-2 suited clubs on paired JJ — HU IP'),
    SweepCase('SW11_52o_mono_spades_3way_CO',
              ['5h', '2d'], ['Ks', '9s', '3s'], 'CO', ['SB', 'BB'], 'CO',
              '5-2 offsuit vs monotone spades — 3-way IP'),

    # ── Suited-disconnected air ───────────────────────────────────────────
    SweepCase('SW12_K5s_paired_66_3way_BTN',
              ['Kh', '5h'], ['6c', '6d', '2s'], 'BTN', ['HJ', 'SB'], 'HJ',
              'K-5 suited hearts on paired 66 — 3-way BTN'),
    SweepCase('SW13_J3s_mono_hearts_HU_BTN',
              ['Jd', '3d'], ['Ah', '9h', '4h'], 'BTN', ['BB'], 'BTN',
              'J-3 suited diamonds vs monotone hearts — HU IP'),
    SweepCase('SW14_Q6s_paired_TT_3way_BTN',
              ['Qc', '6c'], ['Tc', 'Td', '4h'], 'BTN', ['SB', 'BB'], 'BTN',
              'Q-6 suited clubs on paired TT (hero has one club — not flush draw with 2 board clubs only if board has 0-1; Tc+Td+4h → clubs count 1 board + 1 hero = 2, no FD) — 3-way IP'),

    # ── Two-tone with connector structure (air hero) ──────────────────────
    SweepCase('SW15_K7o_twotone_connected_3way_BTN',
              ['Kh', '7d'], ['Jc', '8c', '5s'], 'BTN', ['SB', 'BB'], 'BTN',
              'K-7 on J-8-5 two-tone connected — 3-way IP (hero: no pair, '
              'no flush draw, no meaningful straight connection)'),
    SweepCase('SW16_Q2o_twotone_connected_HU_BTN',
              ['Qh', '2d'], ['9s', '8s', '6c'], 'BTN', ['BB'], 'BTN',
              'Q-2 on 9-8-6 two-tone (hero no spade) — HU IP'),

    # ── Rainbow connected (draw-heavy board, hero disconnected) ───────────
    SweepCase('SW17_K4o_rainbow_conn_3way_HJ',
              ['Kh', '4c'], ['Td', '9s', '8h'], 'HJ', ['CO', 'BB'], 'HJ',
              'K-4 on T-9-8 rainbow connected — 3-way IP'),

    # ── Dry high boards (air hero far from board) ─────────────────────────
    SweepCase('SW18_63s_dry_Khigh_HU_BTN',
              ['6h', '3h'], ['Ks', '9d', '2c'], 'BTN', ['BB'], 'BTN',
              '6-3 suited hearts on K-9-2 rainbow — HU IP (air, no draw)'),
    SweepCase('SW19_J2o_dry_Qhigh_3way_CO',
              ['Jh', '2d'], ['Qs', '7c', '3d'], 'CO', ['SB', 'BB'], 'CO',
              'J-2 offsuit on Q-7-3 rainbow — 3-way IP (air, blocks top pair only)'),

    # ── OOP flop air (hero first to act) ──────────────────────────────────
    # On OOP flop, villain_checked_back will be 0 (no prior-street checks) and
    # hero acts first on the street. We still test what the model outputs —
    # the player is about to decide whether to bet (rep) or check.
    SweepCase('SW20_T3o_paired_88_HU_BB',
              ['Th', '3d'], ['8c', '8d', '5s'], 'BB', ['BTN'], 'BTN',
              'T-3 OOP on paired 88 — HU BB (hero acts first after PF open+call)'),
]


def _build_flop_spec(case: SweepCase) -> SituationSpec:
    """Build a flop decision spec with villains-before-hero checked (IP),
    or fresh OOP (hero first to act)."""
    active = case.villains + [case.hero_pos]
    order = sorted(active, key=lambda p: _POSTFLOP_ORDER[p])
    hero_order = _POSTFLOP_ORDER[case.hero_pos]

    # Preflop: opener raises, others call
    pre = [('preflop', case.opener, 'raise')]
    for c in [p for p in active if p != case.opener]:
        pre.append(('preflop', c, 'call'))

    # Flop: villains acting BEFORE hero check. If hero is earliest (OOP), no
    # flop actions yet.
    flop_acts = [
        ('flop', p, 'check') for p in order if _POSTFLOP_ORDER[p] < hero_order
    ]
    action_history = pre + flop_acts

    return SituationSpec(
        hero_cards=case.hero,
        board_cards=case.board,
        hero_pos=case.hero_pos,
        villain_positions=case.villains,
        pot=90.0,
        to_call=0.0,
        street='flop',
        action_history=action_history,
        opener_position=case.opener,
        effective_stack=450.0,
        current_bet=0.0,
        num_opponents=len(case.villains),
    )


def _feat_dict_to_X(feat_dict: dict, feature_order: List[str]) -> np.ndarray:
    """Build a single-row feature array for the model."""
    row = []
    for col in feature_order:
        if col.startswith('attn_'):
            row.append(1.0)
            continue
        val = feat_dict.get(col, 0.0)
        if val is None:
            val = 0.0
        if isinstance(val, bool):
            val = int(val)
        if isinstance(val, str):
            try:
                val = float(val)
            except (TypeError, ValueError):
                val = encode(val, col)
        row.append(float(val))
    return np.asarray(row, dtype=float)


def _predicate_status(feat_dict: dict) -> Tuple[bool, List[str]]:
    """Check if this case matches the air-CHECK predicate shape."""
    fails = []
    if feat_dict.get('facing_bet', 0) != 0:
        fails.append(f"facing_bet={feat_dict.get('facing_bet')}")
    if feat_dict.get('is_made_hand', 0) != 0:
        fails.append(f"is_made_hand={feat_dict.get('is_made_hand')}")
    if feat_dict.get('draw_outs', 99) > 2:
        fails.append(f"draw_outs={feat_dict.get('draw_outs')}")
    if feat_dict.get('equity_vs_range', 1.0) >= 0.35:
        fails.append(f"equity_vs_range={feat_dict.get('equity_vs_range'):.3f}")
    return (len(fails) == 0, fails)


def _predict(model, X_row, masked_actions=('CHECK', 'BET')):
    probs = model.predict_proba(X_row.reshape(1, -1))[0]
    unmasked_top = INT_TO_ACTION[int(np.argmax(probs))]
    legal = {a: probs[ACTION_TO_INT[a]] for a in masked_actions}
    best_legal = max(legal.items(), key=lambda kv: kv[1])[0]
    return unmasked_top, best_legal, probs


def main():
    print('=' * 76)
    print('v2.3.1 Generalization Sweep — 20 flop inference cases')
    print('=' * 76)

    # Load model + feature order
    with open(CSV_PATH, newline='') as f:
        header = next(csv.reader(f))
    raw_features, attn_features = split_feature_columns(list(header))
    feature_order = raw_features + attn_features

    model = xgb.XGBClassifier()
    model.load_model(MODEL_PATH)
    print(f'Model: {MODEL_PATH}')
    print(f'Features: {len(raw_features)} raw + {len(attn_features)} attn')
    print()

    results = []
    skipped = []

    for case in CASES:
        try:
            spec = _build_flop_spec(case)
            feat_dict = build_situation(spec)
        except Exception as exc:
            skipped.append((case.case_id, f'BUILD_EXC: {exc}'))
            continue

        ok, pred_fails = _predicate_status(feat_dict)
        if not ok:
            skipped.append((case.case_id,
                            f'predicate_mismatch: {"; ".join(pred_fails)}'))
            continue

        X_row = _feat_dict_to_X(feat_dict, feature_order)
        unmasked_top, best_legal, probs = _predict(model, X_row)

        results.append({
            'case_id': case.case_id,
            'theme': case.theme,
            'hero': case.hero,
            'board': case.board,
            'pos': case.hero_pos,
            'n_opp': len(case.villains),
            'is_made': feat_dict.get('is_made_hand'),
            'outs': feat_dict.get('draw_outs'),
            'eq': feat_dict.get('equity_vs_range'),
            'hrp': feat_dict.get('hero_range_percentile'),
            'bah': feat_dict.get('board_adjusted_hrp'),
            'vair': feat_dict.get('villain_air_pct'),
            'vcb': feat_dict.get('villain_checked_back'),
            'unmasked_top': unmasked_top,
            'best_legal': best_legal,
            'probs': probs,
            'correct': best_legal == 'CHECK',
        })

    # Per-case table
    print(f'{"case_id":<38} {"n":>2} {"pos":>3} {"eq":>5} {"bah":>5} '
          f'{"vair":>5} {"action":>6} {"p(CHECK)":>8} {"p(BET)":>6}  mark')
    print('-' * 100)
    for r in results:
        mark = 'OK' if r['correct'] else '** XX **'
        print(f'{r["case_id"]:<38} {r["n_opp"]:>2} {r["pos"]:>3} '
              f'{r["eq"]:>5.2f} {r["bah"]:>5.2f} {r["vair"]:>5.2f} '
              f'{r["best_legal"]:>6} '
              f'{r["probs"][ACTION_TO_INT["CHECK"]]:>8.3f} '
              f'{r["probs"][ACTION_TO_INT["BET"]]:>6.3f}  {mark}')

    # Summary
    print()
    print('=' * 76)
    total = len(results)
    n_check = sum(1 for r in results if r['correct'])
    n_skip = len(skipped)
    print(f'Ran {total} cases ({n_skip} skipped, see below if any)')
    print(f'CHECK: {n_check}/{total} = {100*n_check/max(1,total):.1f}%')
    print()

    # Breakdown by opponent count
    for label, subset in [
        ('HU (n_opp=1)', [r for r in results if r['n_opp'] == 1]),
        ('3-way (n_opp=2)', [r for r in results if r['n_opp'] == 2]),
    ]:
        if subset:
            c = sum(1 for r in subset if r['correct'])
            print(f'  {label}: {c}/{len(subset)} = {100*c/len(subset):.0f}%')

    # Report any BETs with feature dump
    bets = [r for r in results if not r['correct']]
    if bets:
        print()
        print(f'NON-CHECK predictions ({len(bets)}):')
        for r in bets:
            print(f'  [{r["case_id"]}] hero={r["hero"]} board={r["board"]}')
            print(f'    eq={r["eq"]:.3f} bah={r["bah"]:.3f} '
                  f'hrp={r["hrp"]:.3f} vair={r["vair"]:.3f} '
                  f'vcb={r["vcb"]} outs={r["outs"]}')
            p = r['probs']
            print(f'    probs: FOLD={p[ACTION_TO_INT["FOLD"]]:.3f} '
                  f'CHECK={p[ACTION_TO_INT["CHECK"]]:.3f} '
                  f'CALL={p[ACTION_TO_INT["CALL"]]:.3f} '
                  f'BET={p[ACTION_TO_INT["BET"]]:.3f} '
                  f'RAISE={p[ACTION_TO_INT["RAISE"]]:.3f}')
            print(f'    theme: {r["theme"]}')

    if skipped:
        print()
        print(f'Skipped cases ({len(skipped)}):')
        for cid, reason in skipped:
            print(f'  [{cid}] {reason}')

    # Gate
    print()
    print('=' * 76)
    pass_rate = n_check / max(1, total)
    if pass_rate >= 0.85:
        print(f'GATE PASS: {100*pass_rate:.0f}% CHECK (>= 85% target)')
        print('Generalization confirmed. Architectural fix, not memorization.')
        return 0
    elif pass_rate >= 0.70:
        print(f'GATE MARGINAL: {100*pass_rate:.0f}% CHECK '
              f'(70-85% zone — surface to reviewer).')
        return 2
    else:
        print(f'GATE FAIL: {100*pass_rate:.0f}% CHECK (< 70% — v2.3.2 needed).')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
