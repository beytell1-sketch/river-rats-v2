#!/usr/bin/env python3
"""Stage 3.5 M5 — pre-retrain diagnostic on v2.3.1 model.

Re-runs the v2.3.1 model on 3 β-panel HIGH-impact anchors
(d2410_CO_turn + two sibling TPTK-turn-after-flop-check shape hands)
with the NEW (action-aware chained) feature values.

Per spec lock:
- BET restored on d2410 → Stage 3.5 ALONE fixes the class.
  Stage 4 re-label becomes additive insurance.
- Still CHECK on d2410 → diagnosis is Stage 4 (class imbalance), NOT
  feature correctness.

Both outcomes inform Stage 4 scope. Cheap, fast diagnostic.

Writes report to review/comms/BUILDER_V24_STAGE35_M5_DIAGNOSTIC_2026-04-20.md
"""
from __future__ import annotations

import csv
import json
import os
import sys

import numpy as np

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_CORE = os.path.join(_REPO, 'river-rats-core')
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)
os.chdir(_CORE)

from situation_factory import SituationSpec, build_situation  # noqa: E402
from train_model_v2_2 import (  # noqa: E402
    ACTION_TO_INT, INT_TO_ACTION, encode, split_feature_columns,
)


MODEL_PATH = os.path.join(_CORE, 'models', 'v2_3_1_model.json')
CSV_PATH = os.path.join(_REPO, 'training-data', 'v2_3_1_training.csv')


def _anchor_specs():
    """The 3 HIGH-impact anchors. All are turn decisions after villain
    checked the flop (canonical Stage 3.5 target class).

    d0182/d8411 details from test_set_50_labelled.jsonl — same shape as
    d2410 (flop-check leading into turn decision).
    """
    return [
        {
            'anchor_id': 'd2410_CO_turn',
            'expected': 'BET',
            'hero_cards': ['Jc', 'Ks'],
            'board_cards': ['Jd', '9d', '3h', '6d'],
            'hero_pos': 'CO',
            'villain_positions': ['BTN', 'BB'],
            'street': 'turn',
            'facing_bet': False,
            'to_call': 0.0,
            'pot': 80.0,
            'action_history': [
                ('preflop', 'CO', 'raise'),
                ('preflop', 'BTN', 'call'),
                ('preflop', 'BB', 'call'),
                ('flop', 'BB', 'check'),
                ('flop', 'CO', 'check'),
                ('flop', 'BTN', 'check'),
                ('turn', 'BB', 'check'),
            ],
            'opener_position': 'CO',
        },
        {
            'anchor_id': 'd0182_BTN_turn',
            'expected': 'BET',
            'hero_cards': ['Ac', 'Jc'],
            'board_cards': ['9s', 'Ad', '3s', '4c'],
            'hero_pos': 'BTN',
            'villain_positions': ['CO', 'BB'],
            'street': 'turn',
            'facing_bet': False,
            'to_call': 0.0,
            'pot': 80.0,
            'action_history': [
                ('preflop', 'CO', 'raise'),
                ('preflop', 'BTN', 'call'),
                ('preflop', 'BB', 'call'),
                ('flop', 'BB', 'check'),
                ('flop', 'CO', 'check'),
                ('flop', 'BTN', 'check'),
                ('turn', 'BB', 'check'),
                ('turn', 'CO', 'check'),
            ],
            'opener_position': 'CO',
        },
        {
            'anchor_id': 'd8411_BB_turn',
            'expected': 'BET',
            'hero_cards': ['Ac', '8h'],
            'board_cards': ['6c', '8c', '2d', '3c'],
            'hero_pos': 'BB',
            'villain_positions': ['CO', 'BTN'],
            'street': 'turn',
            'facing_bet': False,
            'to_call': 0.0,
            'pot': 80.0,
            'action_history': [
                ('preflop', 'CO', 'raise'),
                ('preflop', 'BTN', 'call'),
                ('preflop', 'BB', 'call'),
                ('flop', 'BB', 'check'),
                ('flop', 'CO', 'check'),
                ('flop', 'BTN', 'check'),
            ],
            'opener_position': 'CO',
        },
    ]


def _build_spec(a):
    return SituationSpec(
        hero_cards=list(a['hero_cards']),
        board_cards=list(a['board_cards']),
        hero_pos=a['hero_pos'],
        villain_positions=list(a['villain_positions']),
        pot=a['pot'],
        to_call=a['to_call'],
        street=a['street'],
        action_history=list(a['action_history']),
        opener_position=a['opener_position'],
        effective_stack=100.0,
        current_bet=0.0,
        num_opponents=len(a['villain_positions']),
    )


def _feat_dict_to_X(feat_dict, feature_order):
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


def _predict(model, X, facing_bet):
    probs = model.predict_proba(X.reshape(1, -1))[0]
    action_probs = {INT_TO_ACTION[i]: float(probs[i]) for i in range(len(probs))}
    legal_actions = ['FOLD', 'CALL', 'RAISE'] if facing_bet else ['CHECK', 'BET']
    legal_best = max(
        ((a, action_probs[a]) for a in legal_actions),
        key=lambda kv: kv[1],
    )[0]
    return legal_best, action_probs


def main():
    print('=' * 72)
    print('Stage 3.5 M5 — v2.3.1 model re-inference on 3 β-panel anchors')
    print('=' * 72)

    import xgboost as xgb
    model = xgb.XGBClassifier()
    model.load_model(MODEL_PATH)
    with open(CSV_PATH, newline='') as f:
        header = next(csv.reader(f))
    raw, attn = split_feature_columns(list(header))
    feature_order = raw + attn

    results = []
    for a in _anchor_specs():
        spec = _build_spec(a)
        try:
            feat = build_situation(spec)
        except Exception as exc:
            results.append({
                'anchor_id': a['anchor_id'],
                'expected': a['expected'],
                'error': str(exc),
            })
            continue
        X = _feat_dict_to_X(feat, feature_order)
        predicted, probs = _predict(model, X, facing_bet=False)
        results.append({
            'anchor_id': a['anchor_id'],
            'expected': a['expected'],
            'predicted': predicted,
            'p_bet': probs['BET'],
            'p_check': probs['CHECK'],
            'chain_steps': feat.get('_villain_range_chain_steps', []),
            'v_tp_plus': feat.get('villain_top_pair_plus_pct', 0.0),
            'v_medium': feat.get('villain_medium_made_pct', 0.0),
            'v_draw': feat.get('villain_draw_pct', 0.0),
            'v_air': feat.get('villain_air_pct', 0.0),
            'passed': predicted == a['expected'],
        })

    # Print results
    for r in results:
        print()
        print(f'{r["anchor_id"]} (expected {r["expected"]}):')
        if 'error' in r:
            print(f'  ERROR: {r["error"]}')
            continue
        mark = 'PASS' if r['passed'] else 'FAIL'
        print(f'  [{mark}] predicted={r["predicted"]}  p(BET)={r["p_bet"]:.3f}  p(CHECK)={r["p_check"]:.3f}')
        print(f'  chain_steps: {r["chain_steps"]}')
        print(f'  villain composition: TP+={r["v_tp_plus"]:.3f} med={r["v_medium"]:.3f} '
              f'draw={r["v_draw"]:.3f} air={r["v_air"]:.3f}')

    # Write report
    passed = sum(1 for r in results if r.get('passed'))
    total = len(results)
    report_path = os.path.join(
        _REPO, 'review', 'comms',
        'BUILDER_V24_STAGE35_M5_DIAGNOSTIC_2026-04-20.md',
    )
    with open(report_path, 'w') as f:
        f.write(f"""---
date: 2026-04-20
from: Builder
to: Main terminal / Owner
re: v2.4 Stage 3.5 M5 — pre-retrain diagnostic (v2.3.1 model on β-panel anchors)
status: DIAGNOSTIC COMPLETE
---

# Stage 3.5 M5 — Pre-Retrain Diagnostic

Ran v2.3.1 model inference on 3 β-panel HIGH-impact anchors with
the NEW action-aware chained feature values. Model weights
UNCHANGED from v2.3.1 — only the feature inputs shift.

**Result: {passed}/{total} anchors predict BET (expected action).**

## Per-anchor results

""")
        for r in results:
            if 'error' in r:
                f.write(f'### {r["anchor_id"]}\n\nError: {r["error"]}\n\n')
                continue
            mark = '✅ PASS' if r['passed'] else '❌ FAIL'
            f.write(f"""### {r['anchor_id']}

{mark} — expected **{r['expected']}**, predicted **{r['predicted']}**

- Probabilities: BET {r['p_bet']:.3f}, CHECK {r['p_check']:.3f}
- Chain steps: `{r['chain_steps']}`
- Villain composition (post-chain):
  - TP+: {r['v_tp_plus']:.3f}
  - medium_made: {r['v_medium']:.3f}
  - draw: {r['v_draw']:.3f}
  - air: {r['v_air']:.3f}

""")

        f.write(f"""## Interpretation

Per spec lock (a4cab83) M5:

- **{passed}/{total} anchors predict BET after Stage 3.5.** Stage 3.5
  feature correctness is {'sufficient to fix the class' if passed == total else 'partially sufficient'}; Stage 4 re-label {'is additive insurance' if passed == total else 'is needed for the anchors that still miss'}.

If d2410 in particular is BET at high confidence: the
calibration-anchor regression v2.3.2 introduced is fixable by
feature correctness alone. Stage 4 re-label becomes class-balance
insurance, not a correctness necessity.

If d2410 still misses: Stage 4 re-label is required to close the
class-balance gap.

## Chain steps captured

All 3 anchors have villain CHECKING the flop before the turn
decision. Stage 3.5 chain should fire at least:
`['flop:CHECK']` on each.

If chain_steps is empty on any anchor, the bridge → feature
extraction wiring isn't reaching that anchor — investigate.
""")

    print(f'\nReport written: {report_path}')
    print()
    print('=' * 72)
    print(f'M5 DIAGNOSTIC: {passed}/{total} anchors predict expected action')
    return 0 if passed == total else 1


if __name__ == '__main__':
    raise SystemExit(main())
