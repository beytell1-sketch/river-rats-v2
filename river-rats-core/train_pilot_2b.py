"""Phase 2-B PILOT trainer — 65-feature smoke (59 baseline + 6 pilot).

Provenance
----------
Per dispatch PR #392 + design memo PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md
§5 row 2-B + §3.4 + §3.Y.4. Trains a single-seed XGBoost classifier on
the 988-on-59 combined corpus with the 6 new pilot features appended
(surface size 65) and reports per-feature importance scores.

Purpose
-------
Pilot is an importance-evidence gate, not a ship candidate. We measure:
  D5 candidates (3): tpmk/broadway/nut_fd_mw — gate ≥2% importance
  4-way candidates (2): players_to_act/multiway_realization — gate ≥2%
  re-raise candidate (1): closing_action — gate ≥1%

Per `feedback_pilot_first_for_long_jobs.md` STANDING RULE: pilot proves
signal before full multi-seed train + full multiway corpus refresh.

Training data
-------------
`data/corpus_combined_988_on_59_2026-05-09.jsonl` (situations: board,
hero_cards, 59-key feat_dict) joined with
`data/corpus_combined_988_on_59_labels_2026-05-09.jsonl` (consensus_action,
consensus_confidence) on pilot_hand_id.

The 6 pilot features are computed inline by replicating Step 18 logic
from `feature_extractor.py` over each row's existing feat_dict + board.
This mirrors the production extractor exactly.

CLI
---
  python3 river-rats-core/train_pilot_2b.py \
      --situations data/corpus_combined_988_on_59_2026-05-09.jsonl \
      --labels data/corpus_combined_988_on_59_labels_2026-05-09.jsonl \
      --seed 42 \
      --output review/comms/PILOT_2B_FEATURE_IMPORTANCE_2026-05-11.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from typing import Dict, List, Tuple

import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feature_extractor import FEATURE_COLUMNS
from gto_model import ACTION_CLASSES, ACTION_TO_INT, N_CLASSES


PILOT_FEATURES = (
    'tpmk_position_with_kicker_strength',
    'broadway_density_completed_on_turn',
    'nut_fd_multiway_pressure_with_blocker',
    'players_to_act_after_hero',
    'multiway_equity_realization_factor',
    'closing_action',
)

assert len(FEATURE_COLUMNS) == 65, (
    f"Pilot trainer requires 65-feature surface; "
    f"feature_extractor.FEATURE_COLUMNS is {len(FEATURE_COLUMNS)}."
)
assert tuple(FEATURE_COLUMNS[-6:]) == PILOT_FEATURES


def _card_rank(c: str) -> int:
    if not c:
        return 0
    return {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,
            'T':10,'J':11,'Q':12,'K':13,'A':14}.get(c[0].upper(), 0)


def _split_board(board_str: str) -> List[str]:
    """Split '4c7d5s' into ['4c','7d','5s']."""
    if not board_str:
        return []
    return [board_str[i:i+2] for i in range(0, len(board_str), 2)]


def augment_with_pilot_features(feat_dict: Dict[str, float],
                                board_str: str,
                                street_int: int) -> Dict[str, float]:
    """Compute the 6 pilot features from feat_dict + board and return a new dict.

    Mirrors `feature_extractor.extract_all_features` Step 18 logic exactly.
    """
    out = dict(feat_dict)

    # 18.1 tpmk_position_with_kicker_strength
    hc = out.get('hand_category', 0)
    is_tpmk = 1.0 if hc in (6, 7) else 0.0
    is_j_high = 1.0 if out.get('high_card_rank', 0) == 11 else 0.0
    hand_rank_norm = max(0.0, min(1.0, float(out.get('hand_rank', 0.0)) / 10.0))
    out['tpmk_position_with_kicker_strength'] = round(
        is_tpmk * is_j_high * hand_rank_norm, 6
    )

    # 18.2 broadway_density_completed_on_turn
    if street_int == 1:  # turn
        cards = _split_board(board_str)
        broadway_count = sum(1 for c in cards if _card_rank(c) >= 10)
        out['broadway_density_completed_on_turn'] = float(broadway_count)
    else:
        out['broadway_density_completed_on_turn'] = 0.0

    # 18.3 nut_fd_multiway_pressure_with_blocker
    has_fd = float(out.get('has_flush_draw', 0))
    nfb = float(out.get('nut_flush_block', 0))
    multiway = 1.0 if out.get('num_opponents', 1) >= 2 else 0.0
    facing = float(out.get('facing_bet', 0))
    out['nut_fd_multiway_pressure_with_blocker'] = round(
        has_fd * nfb * multiway * facing, 6
    )

    # 18.4 players_to_act_after_hero
    num_opp = int(out.get('num_opponents', 1))
    is_ip = int(out.get('is_ip', 0))
    out['players_to_act_after_hero'] = 0.0 if is_ip else float(num_opp)

    # 18.5 multiway_equity_realization_factor
    lookup = {1: 1.0, 2: 0.85, 3: 0.75, 4: 0.70}
    out['multiway_equity_realization_factor'] = lookup.get(num_opp, 0.70)

    # 18.6 closing_action
    out['closing_action'] = 1.0 if (
        is_ip and out['players_to_act_after_hero'] == 0.0
    ) else 0.0

    return out


_STREET_TO_INT = {'preflop': 0, 'flop': 0, 'turn': 1, 'river': 2}


def load_corpus(situations_path: str, labels_path: str) -> Tuple[List[Dict], List[str]]:
    """Load + join situations + labels on pilot_hand_id."""
    sits = {}
    with open(situations_path) as f:
        for line in f:
            d = json.loads(line)
            sits[d['pilot_hand_id']] = d
    rows = []
    actions = []
    with open(labels_path) as f:
        for line in f:
            d = json.loads(line)
            phi = d['pilot_hand_id']
            if phi not in sits:
                continue
            sit = sits[phi]
            feat_dict = d['feat_dict']
            board = sit.get('board', '')
            street_str = sit.get('street', 'flop')
            # feat_dict's 'street' is integer-encoded; use original string for
            # broadway_density logic (turn = 1 in our encoding regardless)
            street_int = _STREET_TO_INT.get(street_str, 0)
            if street_str == 'preflop':
                street_int = -1  # not flop; not turn (broadway returns 0)
            augmented = augment_with_pilot_features(feat_dict, board, street_int)
            rows.append(augmented)
            actions.append(d['consensus_action'])
    return rows, actions


def build_xy(rows: List[Dict], actions: List[str]) -> Tuple[np.ndarray, np.ndarray]:
    X = np.empty((len(rows), len(FEATURE_COLUMNS)), dtype=np.float32)
    y = np.empty(len(rows), dtype=np.int32)
    for i, (feat, act) in enumerate(zip(rows, actions)):
        for j, k in enumerate(FEATURE_COLUMNS):
            X[i, j] = float(feat.get(k, 0.0))
        y[i] = ACTION_TO_INT[act]
    return X, y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--situations', required=True)
    ap.add_argument('--labels', required=True)
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--output', required=True,
                    help='Path to write per-feature importance JSON')
    args = ap.parse_args()

    print(f'[pilot-2b] loading corpus...')
    rows, actions = load_corpus(args.situations, args.labels)
    print(f'[pilot-2b] {len(rows)} rows joined')
    print(f'[pilot-2b] action distribution: {Counter(actions)}')

    X, y = build_xy(rows, actions)
    print(f'[pilot-2b] X shape: {X.shape}; y shape: {y.shape}')

    # Pilot features sanity
    pilot_idx = [FEATURE_COLUMNS.index(k) for k in PILOT_FEATURES]
    for k, idx in zip(PILOT_FEATURES, pilot_idx):
        col = X[:, idx]
        nan_inf = np.sum(~np.isfinite(col))
        nonzero = np.sum(col != 0)
        print(f'[pilot-2b]   {k:50s} idx={idx} '
              f'nonzero={nonzero}/{len(col)} mean={col.mean():.4f} '
              f'min={col.min():.4f} max={col.max():.4f} nan_inf={nan_inf}')
        assert nan_inf == 0, f'NaN/Inf in {k}'

    # Train 1-seed XGBoost. Hyperparams from v9_student (same regularization regime).
    print(f'[pilot-2b] training XGBoost (seed={args.seed})...')
    clf = xgb.XGBClassifier(
        objective='multi:softprob',
        num_class=N_CLASSES,
        max_depth=4,
        learning_rate=0.1,
        n_estimators=200,
        min_child_weight=3,
        reg_lambda=1.0,
        random_state=args.seed,
        use_label_encoder=False,
        eval_metric='mlogloss',
        verbosity=0,
    )
    clf.fit(X, y)

    train_pred = clf.predict(X)
    train_acc = accuracy_score(y, train_pred)
    print(f'[pilot-2b] train accuracy (overfit-baseline): {train_acc:.4f}')

    # Importances
    importances = clf.feature_importances_
    paired = list(zip(FEATURE_COLUMNS, importances.tolist()))
    paired.sort(key=lambda kv: kv[1], reverse=True)

    print(f'\n[pilot-2b] top 20 features by importance:')
    for k, v in paired[:20]:
        marker = ' ← PILOT' if k in PILOT_FEATURES else ''
        print(f'  {k:50s} {v*100:6.2f}%{marker}')

    print(f'\n[pilot-2b] PILOT features specifically:')
    pilot_imp = {}
    for k in PILOT_FEATURES:
        idx = FEATURE_COLUMNS.index(k)
        v = float(importances[idx])
        pilot_imp[k] = v
        rank = next((i for i, (kk, _) in enumerate(paired, 1) if kk == k), -1)
        print(f'  {k:50s} {v*100:6.2f}%  rank #{rank}/65')

    # Gate evidence
    d5_features = (
        'tpmk_position_with_kicker_strength',
        'broadway_density_completed_on_turn',
        'nut_fd_multiway_pressure_with_blocker',
    )
    fourway_features = (
        'players_to_act_after_hero',
        'multiway_equity_realization_factor',
    )
    reraise_features = ('closing_action',)

    d5_passing = [k for k in d5_features if pilot_imp[k] >= 0.02]
    fourway_passing = [k for k in fourway_features if pilot_imp[k] >= 0.02]
    reraise_passing = [k for k in reraise_features if pilot_imp[k] >= 0.01]

    print(f'\n[pilot-2b] GATE EVIDENCE:')
    print(f'  D5 ≥2% importance:       {len(d5_passing)}/3 passing — {d5_passing}')
    print(f'  4-way ≥2% importance:    {len(fourway_passing)}/2 passing — {fourway_passing}')
    print(f'  re-raise ≥1% importance: {len(reraise_passing)}/1 passing — {reraise_passing}')

    # Dump JSON for builder report
    out = {
        'seed': args.seed,
        'n_rows': len(rows),
        'n_features': len(FEATURE_COLUMNS),
        'train_accuracy_overfit_baseline': train_acc,
        'action_distribution': dict(Counter(actions)),
        'all_feature_importance': dict(zip(FEATURE_COLUMNS, importances.tolist())),
        'pilot_feature_importance': pilot_imp,
        'gate_evidence': {
            'd5_passing_2pct': d5_passing,
            'fourway_passing_2pct': fourway_passing,
            'reraise_passing_1pct': reraise_passing,
        },
        'top_20_by_importance': [{'feature': k, 'importance': v} for k, v in paired[:20]],
    }
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'[pilot-2b] wrote {args.output}')


if __name__ == '__main__':
    main()
