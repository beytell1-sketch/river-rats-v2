"""Phase 2-B RE-PILOT trainer — 63-feature smoke (59 baseline + 4 re-pilot).

Provenance
----------
Per dispatch PR #396 (owner-ratified Option A; supersedes PR #392). Trains
a single-seed XGBoost classifier on the 988-on-59 combined corpus with the
4 re-pilot features appended (surface size 63) and reports per-feature
importance scores.

PILOT v1 (PR #393) → RE-PILOT (this script):
  KEEP:           players_to_act_after_hero (3.58% v1; verify regression)
  RE-ENGINEERED:  tpmk_kicker_rank                  (was tpmk_position_with_kicker_strength)
                  broadway_pressure_multiway_facing (was broadway_density_completed_on_turn)
                  nut_fd_blocker_multiway           (was nut_fd_multiway_pressure_with_blocker)
  DROPPED:        multiway_equity_realization_factor + closing_action (collinear w/ baseline)

Gates (per design memo §3.4 + §3.Y.4):
  players_to_act_after_hero (regression check): 2.58% ≤ x ≤ 4.58% (v1 3.58% ±1%)
  3 re-engineered: each ≥2% importance + ≥1 stay-wrong graduation

Training data
-------------
`data/corpus_combined_988_on_59_2026-05-09.jsonl` (situations: board,
hero_cards, 59-key feat_dict) joined with
`data/corpus_combined_988_on_59_labels_2026-05-09.jsonl` (consensus_action,
consensus_confidence) on pilot_hand_id.

The 4 re-pilot features are computed inline by replicating Step 18 logic
from `feature_extractor.py` over each row's existing feat_dict + board +
hero_cards. This mirrors the production extractor exactly.

CLI
---
  python3 river-rats-core/train_pilot_2b.py \\
      --situations data/corpus_combined_988_on_59_2026-05-09.jsonl \\
      --labels data/corpus_combined_988_on_59_labels_2026-05-09.jsonl \\
      --seed 42 \\
      --output review/comms/PILOT_2B_REPILOT_FEATURE_IMPORTANCE_2026-05-11.json
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


# 4 re-pilot features (last 4 of 63-feature surface)
PILOT_FEATURES = (
    'players_to_act_after_hero',
    'tpmk_kicker_rank',
    'broadway_pressure_multiway_facing',
    'nut_fd_blocker_multiway',
)

# v1 features that were dropped/renamed in re-pilot (sanity guard for legacy state)
PILOT_V1_RENAMED = (
    'tpmk_position_with_kicker_strength',
    'broadway_density_completed_on_turn',
    'nut_fd_multiway_pressure_with_blocker',
)
PILOT_V1_DROPPED = (
    'multiway_equity_realization_factor',
    'closing_action',
)

assert len(FEATURE_COLUMNS) == 63, (
    f"Re-pilot trainer requires 63-feature surface; "
    f"feature_extractor.FEATURE_COLUMNS is {len(FEATURE_COLUMNS)}."
)
assert tuple(FEATURE_COLUMNS[-4:]) == PILOT_FEATURES


_RANK_MAP = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,
             'T':10,'J':11,'Q':12,'K':13,'A':14}


def _card_rank(c: str) -> int:
    if not c:
        return 0
    return _RANK_MAP.get(c[0].upper(), 0)


def _split_cards(s: str) -> List[str]:
    """Split '7h7s' or '4c7d5s' into list of 2-char tokens."""
    if not s:
        return []
    return [s[i:i+2] for i in range(0, len(s), 2)]


def augment_with_pilot_features(feat_dict: Dict[str, float],
                                board_str: str,
                                hero_cards_str: str,
                                street_int: int) -> Dict[str, float]:
    """Compute the 4 re-pilot features from feat_dict + board + hero_cards.

    Mirrors `feature_extractor.extract_all_features` Step 18 logic exactly.
    """
    out = dict(feat_dict)
    num_opp = int(out.get('num_opponents', 1))
    is_ip = int(out.get('is_ip', 0))
    multiway = 1.0 if num_opp >= 2 else 0.0

    # 18.1 players_to_act_after_hero (KEEP)
    out['players_to_act_after_hero'] = 0.0 if is_ip else float(num_opp)

    # 18.2 tpmk_kicker_rank (RE-ENGINEERED)
    hc = out.get('hand_category', 0)
    if hc in (6, 7, 8):
        hero_cards = _split_cards(hero_cards_str)
        high_card_rank = int(out.get('high_card_rank', 0))
        if len(hero_cards) == 2:
            h_ranks = [_card_rank(c) for c in hero_cards]
            if h_ranks[0] == high_card_rank and h_ranks[1] != high_card_rank:
                kicker = h_ranks[1]
            elif h_ranks[1] == high_card_rank and h_ranks[0] != high_card_rank:
                kicker = h_ranks[0]
            else:
                kicker = max(h_ranks) if h_ranks else 0
            out['tpmk_kicker_rank'] = float(kicker)
        else:
            out['tpmk_kicker_rank'] = 0.0
    else:
        out['tpmk_kicker_rank'] = 0.0

    # 18.3 broadway_pressure_multiway_facing (RE-ENGINEERED)
    if street_int == 1:  # turn
        cards = _split_cards(board_str)
        broadway_count = sum(1 for c in cards if _card_rank(c) >= 10)
    else:
        broadway_count = 0
    facing = float(out.get('facing_bet', 0))
    out['broadway_pressure_multiway_facing'] = round(
        float(broadway_count) * multiway * facing, 6
    )

    # 18.4 nut_fd_blocker_multiway (RE-ENGINEERED, no facing_bet gate)
    has_fd = float(out.get('has_flush_draw', 0))
    nfb = float(out.get('nut_flush_block', 0))
    out['nut_fd_blocker_multiway'] = round(has_fd * nfb * multiway, 6)

    return out


_STREET_TO_INT = {'preflop': -1, 'flop': 0, 'turn': 1, 'river': 2}


def load_corpus(situations_path: str, labels_path: str) -> Tuple[List[Dict], List[str]]:
    """Load + join situations + labels on pilot_hand_id."""
    sits = {}
    with open(situations_path) as f:
        for line in f:
            d = json.loads(line)
            sits[d['pilot_hand_id']] = d
    rows = []
    actions = []
    for line in open(labels_path):
        d = json.loads(line)
        phi = d['pilot_hand_id']
        if phi not in sits:
            continue
        sit = sits[phi]
        feat_dict = d['feat_dict']
        board = sit.get('board', '')
        hero_cards = sit.get('hero_cards', '')
        street_str = sit.get('street', 'flop')
        street_int = _STREET_TO_INT.get(street_str, 0)
        augmented = augment_with_pilot_features(
            feat_dict, board, hero_cards, street_int
        )
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
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    print('[repilot-2b] loading corpus...')
    rows, actions = load_corpus(args.situations, args.labels)
    print(f'[repilot-2b] {len(rows)} rows joined')
    print(f'[repilot-2b] action distribution: {Counter(actions)}')

    X, y = build_xy(rows, actions)
    print(f'[repilot-2b] X shape: {X.shape}; y shape: {y.shape}')

    # Sanity on the 4 re-pilot features
    pilot_idx = [FEATURE_COLUMNS.index(k) for k in PILOT_FEATURES]
    for k, idx in zip(PILOT_FEATURES, pilot_idx):
        col = X[:, idx]
        nan_inf = int(np.sum(~np.isfinite(col)))
        nonzero = int(np.sum(col != 0))
        print(f'[repilot-2b]   {k:42s} idx={idx} '
              f'nonzero={nonzero}/{len(col)} mean={col.mean():.4f} '
              f'min={col.min():.4f} max={col.max():.4f} nan_inf={nan_inf}')
        assert nan_inf == 0, f'NaN/Inf in {k}'

    # Train 1-seed XGBoost (same hyperparams as v1 PILOT trainer)
    print(f'[repilot-2b] training XGBoost (seed={args.seed})...')
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
    print(f'[repilot-2b] train accuracy (overfit-baseline): {train_acc:.4f}')

    importances = clf.feature_importances_
    paired = list(zip(FEATURE_COLUMNS, importances.tolist()))
    paired.sort(key=lambda kv: kv[1], reverse=True)

    print('\n[repilot-2b] top 20 features by importance:')
    for k, v in paired[:20]:
        marker = ' ← RE-PILOT' if k in PILOT_FEATURES else ''
        print(f'  {k:42s} {v*100:6.2f}%{marker}')

    print('\n[repilot-2b] RE-PILOT features specifically:')
    pilot_imp = {}
    for k in PILOT_FEATURES:
        idx = FEATURE_COLUMNS.index(k)
        v = float(importances[idx])
        pilot_imp[k] = v
        rank = next((i for i, (kk, _) in enumerate(paired, 1) if kk == k), -1)
        print(f'  {k:42s} {v*100:6.2f}%  rank #{rank}/63')

    # Gate evidence (dispatch §"Re-pilot gate criteria")
    kept_2pct = 0.025 <= pilot_imp['players_to_act_after_hero']  # regression: v1 was 3.58%
    regression_ok = (
        0.0258 <= pilot_imp['players_to_act_after_hero'] <= 0.0458
    )  # v1 3.58% ±1%
    d5_re = (
        'tpmk_kicker_rank',
        'broadway_pressure_multiway_facing',
        'nut_fd_blocker_multiway',
    )
    d5_passing = [k for k in d5_re if pilot_imp[k] >= 0.02]
    n_pass_total = (1 if kept_2pct else 0) + len(d5_passing)

    print('\n[repilot-2b] GATE EVIDENCE:')
    print(f'  KEEP players_to_act_after_hero ≥2.5%: {pilot_imp["players_to_act_after_hero"]*100:.2f}% — {"PASS" if kept_2pct else "FAIL"}')
    print(f'  KEEP regression check (3.58% ±1%):    {"PASS" if regression_ok else "FAIL"}')
    print(f'  RE-ENGINEERED ≥2%:                    {len(d5_passing)}/3 passing — {d5_passing}')
    print(f'  TOTAL features passing gate:          {n_pass_total}/4')

    out = {
        'seed': args.seed,
        'n_rows': len(rows),
        'n_features': len(FEATURE_COLUMNS),
        'train_accuracy_overfit_baseline': train_acc,
        'action_distribution': dict(Counter(actions)),
        'all_feature_importance': dict(zip(FEATURE_COLUMNS, importances.tolist())),
        'pilot_feature_importance': pilot_imp,
        'gate_evidence': {
            'kept_passing_25pct': bool(kept_2pct),
            'kept_regression_within_1pct': bool(regression_ok),
            'd5_re_engineered_passing_2pct': d5_passing,
            'total_passing': n_pass_total,
        },
        'top_20_by_importance': [{'feature': k, 'importance': v} for k, v in paired[:20]],
    }
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'[repilot-2b] wrote {args.output}')


if __name__ == '__main__':
    main()
