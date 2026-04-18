"""eval_flop_litmus_v231.py — v2.3.1 flop-decision litmus inference.

Tests the v2.3.1 model on the ORIGINAL playtest spots as flop decisions
(training has turn versions; this tests generalization across street).

Per REVIEW_LABELS_AIR_CHECK_2026-04-18.md §Evaluation gates:
  - A4d/Qs5s7s (FLOP decision) must predict CHECK
  - T5h/JJ2 (FLOP decision) must predict CHECK

If either fails: Layer 1 alone wasn't enough. Report, do NOT add override.

Run:
    python3 review/eval_flop_litmus_v231.py
"""
from __future__ import annotations

import os
import sys

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_CORE = os.path.join(_REPO, 'river-rats-core')
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)
os.chdir(_CORE)

import csv
import numpy as np
import xgboost as xgb

from situation_factory import SituationSpec, build_situation
from train_model_v2_2 import (
    ACTION_TO_INT, INT_TO_ACTION, encode, split_feature_columns,
)


MODEL_PATH = os.path.join(_CORE, 'models', 'v2_3_1_model.json')
CSV_PATH = os.path.join(_REPO, 'training-data', 'v2_3_1_training.csv')


def _build_flop_spec(hero_cards, board_flop, hero_pos, villains, opener):
    """Build a flop decision spec with villains-before-hero checked (IP)."""
    from situation_factory import _POSTFLOP_ORDER
    active = villains + [hero_pos]
    order = sorted(active, key=lambda p: _POSTFLOP_ORDER[p])
    hero_order = _POSTFLOP_ORDER[hero_pos]
    pre = [('preflop', opener, 'raise')]
    for c in [p for p in active if p != opener]:
        pre.append(('preflop', c, 'call'))
    flop_acts = [('flop', p, 'check') for p in order if _POSTFLOP_ORDER[p] < hero_order]
    action_history = pre + flop_acts
    return SituationSpec(
        hero_cards=hero_cards,
        board_cards=board_flop,
        hero_pos=hero_pos,
        villain_positions=villains,
        pot=90.0,
        to_call=0.0,
        street='flop',
        action_history=action_history,
        opener_position=opener,
        effective_stack=450.0,
        current_bet=0.0,
        num_opponents=len(villains),
    )


def _feat_dict_to_row(feat_dict, feature_order):
    """Build a single-row CSV dict suitable for build_matrix."""
    row = {}
    for col in feature_order:
        if col.startswith('attn_'):
            row[col] = 1.0
        else:
            val = feat_dict.get(col, 0.0)
            if val is None:
                val = 0.0
            if isinstance(val, bool):
                val = int(val)
            if isinstance(val, str):
                # Let encode handle string → numeric (street/position)
                try:
                    row[col] = float(val)
                    continue
                except (TypeError, ValueError):
                    pass
                row[col] = encode(val, col)
                continue
            row[col] = float(val)
    row['label'] = 'CHECK'  # placeholder; not used for prediction
    return row


def _predict(model, X_row, feature_order):
    """Predict action + probabilities + legal-action-masked action."""
    probs = model.predict_proba(X_row.reshape(1, -1))[0]
    top_action = INT_TO_ACTION[int(np.argmax(probs))]
    # Legal mask: facing_bet=0 → {CHECK, BET}
    legal_idx = [ACTION_TO_INT['CHECK'], ACTION_TO_INT['BET']]
    legal_probs = {a: probs[ACTION_TO_INT[a]] for a in ['CHECK', 'BET']}
    best_legal = max(legal_probs.items(), key=lambda kv: kv[1])[0]
    return top_action, best_legal, probs


def main():
    print('=' * 72)
    print('v2.3.1 Flop Litmus Inference')
    print('=' * 72)

    # Load column order from training CSV
    with open(CSV_PATH, newline='') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
    raw_features, attn_features = split_feature_columns(list(header))
    feature_order = raw_features + attn_features
    print(f'Feature order: {len(raw_features)} raw + {len(attn_features)} attn '
          f'= {len(feature_order)} total')

    # Load model
    model = xgb.XGBClassifier()
    model.load_model(MODEL_PATH)
    print(f'Loaded model: {MODEL_PATH}')

    # Build the two litmus specs (FLOP versions of the playtest spots)
    litmus_specs = [
        ('A4d_on_Qs5s7s_flop',
         _build_flop_spec(['Ad', '4d'], ['Qs', '5s', '7s'],
                          'BTN', ['SB', 'BB'], 'BTN')),
        ('T5h_on_JJ2_flop',
         _build_flop_spec(['Th', '5h'], ['Jc', 'Jd', '2h'],
                          'BTN', ['SB', 'BB'], 'BTN')),
    ]

    results = []
    for sid, spec in litmus_specs:
        print(f'\n--- {sid} ---')
        feat_dict = build_situation(spec)
        row = _feat_dict_to_row(feat_dict, feature_order)
        X_row = np.array([row[c] for c in feature_order], dtype=float)

        top, best_legal, probs = _predict(model, X_row, feature_order)
        print(f'  hero={spec.hero_cards} board={spec.board_cards} '
              f'pos={spec.hero_pos}')
        print(f'  key features:')
        print(f'    is_made_hand={feat_dict.get("is_made_hand")} '
              f'draw_outs={feat_dict.get("draw_outs")} '
              f'equity_vs_range={feat_dict.get("equity_vs_range"):.3f}')
        print(f'    hrp={feat_dict.get("hero_range_percentile"):.3f} '
              f'board_adjusted_hrp={feat_dict.get("board_adjusted_hrp"):.4f}')
        print(f'    villain_air_pct={feat_dict.get("villain_air_pct"):.3f} '
              f'villain_checked_back={feat_dict.get("villain_checked_back")}')
        print(f'  probabilities:')
        for a in ['FOLD', 'CHECK', 'CALL', 'BET', 'RAISE']:
            print(f'    {a}: {probs[ACTION_TO_INT[a]]:.3f}')
        print(f'  top action (unmasked): {top}')
        print(f'  best legal (masked to {{CHECK,BET}}): {best_legal}')
        passed = (best_legal == 'CHECK')
        results.append((sid, best_legal, passed, probs))
        mark = 'PASS' if passed else 'FAIL'
        print(f'  → {mark} (expected CHECK, got {best_legal})')

    # Summary
    print('\n' + '=' * 72)
    print('LITMUS SUMMARY')
    print('=' * 72)
    all_pass = all(r[2] for r in results)
    for sid, action, passed, _ in results:
        mark = 'PASS' if passed else 'FAIL'
        print(f'  [{mark}] {sid}: predicted {action}')
    print()
    if all_pass:
        print('BOTH FLOP LITMUS TESTS PASS — v2.3.1 clears litmus gate.')
        return 0
    else:
        print('ONE OR BOTH LITMUS FAILED — Layer 1 board_adjusted_hrp alone '
              'was not sufficient.')
        print('Per review directive: do NOT paper over with override. '
              'Consider Path A (flop memorization specs) as v2.3.2.')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
