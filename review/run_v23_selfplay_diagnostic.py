#!/usr/bin/env python3
"""v2.3 self-play diagnostic — 2000 deals, all metrics.

The v2.3 model was trained with 108 features (54 raw + 54 attn_* all=1.0).
self_play.py uses GtoOracle which only passes 54 raw features to predict().
GtoOracle.predict() slices features[:self._n_features] where n_features=108,
causing a shape mismatch.

This wrapper creates a V23Oracle that pads the 54-feature vector with 54
attention features (all 1.0) and also applies the CAT_MAPS encoding for
street/hero_position/villain_position to match training-time encoding.

Usage:
    cd river-rats-core && python3 ../review/run_v23_selfplay_diagnostic.py
"""
import sys
import os
import json
import statistics

# Add river-rats-core to path
CORE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'river-rats-core')
sys.path.insert(0, CORE_DIR)

import numpy as np
from self_play import SelfPlayRunner, Variant
from multiway_adjuster import get_default_params
from gto_model import GtoOracle, FEATURE_COLUMNS, OraclePrediction, ACTION_CLASSES
from train_model_v2_2 import encode, CAT_MAPS

MODEL_PATH = os.path.join(CORE_DIR, 'models', 'v2_3_model_shipped.json')
NUM_DEALS = 2000
SEED = 42

# The 54 attention column names (in training CSV order)
ATTN_COLUMNS = [f"attn_{c}" for c in FEATURE_COLUMNS]


class V23Oracle:
    """Wraps GtoOracle to produce 108-feature vectors for the v2.3 model.

    The v2.3 model expects 54 raw features (CAT_MAPS-encoded) + 54 attn_*
    features (all 1.0 at inference). This class:
    1. Intercepts predict(features_54) calls
    2. Pads with 54 ones to create a 108-element vector
    3. Delegates to the underlying XGBoost model

    Also provides features_from_dict() that applies CAT_MAPS encoding
    (the same path-3 logic used during training) so that categorical
    columns (street, hero_position, villain_position) are encoded as
    integers, not left as strings.
    """

    def __init__(self, model_path: str):
        import xgboost as xgb
        self._model = xgb.XGBClassifier()
        self._model.load_model(model_path)
        assert self._model.n_features_in_ == 108, (
            f"Expected 108 features, got {self._model.n_features_in_}"
        )
        self._action_map = {i: a for i, a in enumerate(ACTION_CLASSES)}

    def predict(self, features: np.ndarray) -> OraclePrediction:
        """Predict with 108 features (auto-pad if 54 provided)."""
        if features.ndim == 1:
            if len(features) <= 54:
                features = np.concatenate([features, np.ones(54, dtype=np.float32)])
            X = features.reshape(1, -1)
        else:
            if features.shape[1] <= 54:
                pad = np.ones((features.shape[0], 54), dtype=np.float32)
                features = np.concatenate([features, pad], axis=1)
            X = features

        probs = self._model.predict_proba(X)[0]
        action_idx = int(np.argmax(probs))
        action = self._action_map[action_idx]
        confidence = float(probs[action_idx])

        return OraclePrediction(
            action=action,
            action_idx=action_idx,
            confidence=confidence,
            probs={a: float(probs[i]) for i, a in enumerate(ACTION_CLASSES)},
            prob_array=probs,
        )

    @staticmethod
    def features_from_dict(feat_dict):
        """Build 54-feature array using CAT_MAPS encoding (matches training)."""
        arr = np.zeros(len(FEATURE_COLUMNS), dtype=np.float32)
        for i, col in enumerate(FEATURE_COLUMNS):
            arr[i] = encode(feat_dict, col)
        return arr

    @property
    def action_probs(self):
        """Compatibility shim."""
        return None


def main():
    print(f"Loading model: {MODEL_PATH}")
    oracle = V23Oracle(MODEL_PATH)
    print("Model loaded successfully (108-feature v2.3 with attn padding)")

    # Monkey-patch GtoOracle.features_from_dict to use CAT_MAPS encoding
    GtoOracle.features_from_dict = staticmethod(V23Oracle.features_from_dict)

    # Single variant — baseline params with v2.3 model
    variants = [Variant("v2.3_shipped", get_default_params())]

    # Run with log_all_multiway=True to capture all seats' decisions
    runner = SelfPlayRunner(
        variants=variants,
        num_deals=NUM_DEALS,
        seed=SEED,
        oracle=oracle,
        log_all_multiway=True,
    )

    print(f"Running {NUM_DEALS} deals, seed={SEED}, all 6 positions per deal...")
    print(f"Total games: {NUM_DEALS} x 6 positions x 1 variant = {NUM_DEALS * 6}")
    result = runner.run_round()
    print(f"Run complete: {result.num_games} games played")

    # Collect ALL postflop decisions (hero + opponents from all games)
    all_postflop = []
    all_preflop = []
    hero_postflop = []

    for gr in result.game_results:
        for d in gr.hero_decisions:
            if d.is_preflop:
                all_preflop.append(d)
            else:
                all_postflop.append(d)
                hero_postflop.append(d)
        for pos, decs in gr.opponent_decisions.items():
            for d in decs:
                if d.is_preflop:
                    all_preflop.append(d)
                else:
                    all_postflop.append(d)

    print(f"\nTotal postflop decisions: {len(all_postflop)}")
    print(f"  Hero postflop: {len(hero_postflop)}")
    print(f"  Opponent postflop: {len(all_postflop) - len(hero_postflop)}")
    print(f"Total preflop decisions: {len(all_preflop)}")

    if len(all_postflop) == 0:
        print("\n*** STOP: Zero postflop decisions. Something is fundamentally wrong. ***")
        sys.exit(1)

    # ── Metric 1: Check-to-hero BET probability < 0.05 ──
    # "Check-to-hero" = postflop spots where player is NOT facing a bet, multiway (2+ opponents)
    check_to_hero = [d for d in all_postflop if not d.facing_bet and d.num_opponents >= 2]

    print("\nRe-running oracle on check-to-hero spots to extract BET probabilities...")
    bet_probs = []
    for d in check_to_hero:
        if d.feat_dict:
            features = V23Oracle.features_from_dict(d.feat_dict)
            pred = oracle.predict(features)
            bet_prob = pred.probs.get('BET', 0.0) + pred.probs.get('RAISE', 0.0)
            bet_probs.append(bet_prob)

    if bet_probs:
        low_bet = sum(1 for p in bet_probs if p < 0.05)
        pct_low_bet = low_bet / len(bet_probs) * 100
        print(f"\nCheck-to-hero 3-way+ spots: {len(check_to_hero)}")
        print(f"  With BET prob < 0.05: {low_bet} ({pct_low_bet:.1f}%)")
        print(f"  BET prob distribution:")
        sorted_probs = sorted(bet_probs)
        n = len(sorted_probs)
        for pct_label, idx in [("p10", int(n*0.1)), ("p25", int(n*0.25)),
                                ("p50", int(n*0.5)), ("p75", int(n*0.75)),
                                ("p90", int(n*0.9))]:
            idx = min(idx, n-1)
            print(f"    {pct_label}: {sorted_probs[idx]:.4f}")
        print(f"    mean: {statistics.mean(bet_probs):.4f}")
    else:
        pct_low_bet = None
        print("\nNo check-to-hero 3-way+ spots found (unexpected)")

    # ── Metric 2: Facing-bet situations (3-way+) ──
    facing_bet_3way = [d for d in all_postflop if d.facing_bet and d.num_opponents >= 2]
    print(f"\nFacing-bet 3-way+ situations: {len(facing_bet_3way)}")

    if facing_bet_3way:
        print(f"\n  First 20 facing-bet 3-way situations:")
        for i, d in enumerate(facing_bet_3way[:20]):
            print(f"    [{i+1:2d}] street={d.street:<6s} pos={d.player_position:<4s} "
                  f"action={d.action:<6s} pot={d.pot:>4d} to_call={d.to_call:>3d} "
                  f"eq={d.equity:.3f} opp={d.num_opponents} "
                  f"cards={d.hero_cards} board={d.board}")

    # ── Metric 3: 3-way postflop yield ──
    threeway_postflop = [d for d in all_postflop if d.num_opponents >= 2]
    total_postflop = len(all_postflop)
    threeway_yield = len(threeway_postflop) / total_postflop * 100 if total_postflop else 0
    print(f"\n3-way+ postflop decisions: {len(threeway_postflop)} / {total_postflop} = {threeway_yield:.1f}%")

    # ── Metric 4: BET actions per 1000 deals ──
    bet_actions = [d for d in all_postflop if d.action in ('bet', 'raise')]
    bet_per_1000 = len(bet_actions) / NUM_DEALS * 1000
    print(f"\nBET/RAISE actions (postflop): {len(bet_actions)} ({bet_per_1000:.1f} per 1000 deals)")

    # ── Metric 5: Average pot size ──
    pot_sizes = []
    for gr in result.game_results:
        hr = gr.hand_record
        if isinstance(hr, dict):
            pot = hr.get('pot_at_end') or hr.get('final_pot')
            if pot:
                pot_sizes.append(pot)

    if pot_sizes:
        avg_pot = statistics.mean(pot_sizes)
        print(f"\nAverage pot size at end: {avg_pot:.1f} chips ({len(pot_sizes)} hands with data)")
    else:
        avg_pot = None
        print("\nNo pot size data available from hand records")

    # ── Per-street action breakdown ──
    print("\n-- Per-street action breakdown --")
    street_actions = {}
    for d in all_preflop + all_postflop:
        street = d.street if not d.is_preflop else 'preflop'
        action = d.action.upper()
        key = (street, action)
        street_actions[key] = street_actions.get(key, 0) + 1

    streets_order = ['preflop', 'flop', 'turn', 'river']
    actions_order = ['FOLD', 'CHECK', 'CALL', 'BET', 'RAISE']
    print(f"{'Street':<10} " + " ".join(f"{a:<8}" for a in actions_order) + " TOTAL")
    for street in streets_order:
        counts = [street_actions.get((street, a), 0) for a in actions_order]
        total = sum(counts)
        if total > 0:
            print(f"{street:<10} " + " ".join(f"{c:<8}" for c in counts) + f" {total}")

    # ── Facing-bet (any number of opponents) ──
    facing_bet_all = [d for d in all_postflop if d.facing_bet]
    print(f"\nFacing-bet situations (any # opponents): {len(facing_bet_all)}")
    if facing_bet_all:
        by_opp = {}
        for d in facing_bet_all:
            by_opp[d.num_opponents] = by_opp.get(d.num_opponents, 0) + 1
        for k in sorted(by_opp):
            print(f"  {k} opponents: {by_opp[k]}")

    # ── Assessment ──
    print("\n" + "="*60)
    print("ASSESSMENT")
    print("="*60)
    passive_loop_broken = len(facing_bet_3way) > 0
    if passive_loop_broken:
        print(f"PASSIVE LOOP: BROKEN -- {len(facing_bet_3way)} facing-bet 3-way situations generated")
        print(f"  v2.2 baseline: ~0")
        print(f"  v2.3: {len(facing_bet_3way)}")
        interesting = [d for d in facing_bet_3way
                       if d.equity > 0.15 and d.equity < 0.85 and d.pot > 30]
        print(f"  'Interesting' for v2.4 labelling: {len(interesting)} "
              f"(equity 0.15-0.85, pot > 30)")
    else:
        print("PASSIVE LOOP: PERSISTS -- zero facing-bet 3-way situations")
        print("  The bias correction does NOT generalize to dynamic play.")

    # ── Save structured output ──
    output = {
        'config': {
            'model': 'v2_3_model_shipped.json',
            'num_deals': NUM_DEALS,
            'seed': SEED,
            'total_games': result.num_games,
        },
        'metrics': {
            'check_to_hero_low_bet_pct': round(pct_low_bet, 1) if pct_low_bet is not None else None,
            'facing_bet_3way_count': len(facing_bet_3way),
            'threeway_postflop_yield_pct': round(threeway_yield, 1),
            'total_postflop_decisions': total_postflop,
            'bet_actions_per_1000_deals': round(bet_per_1000, 1),
            'avg_pot_size': round(avg_pot, 1) if avg_pot else None,
            'passive_loop_broken': passive_loop_broken,
        },
        'bet_prob_distribution': {
            'count': len(bet_probs) if bet_probs else 0,
            'percentiles': {},
        },
        'facing_bet_3way_examples': [],
        'street_actions': {f"{s}_{a}": street_actions.get((s, a), 0)
                          for s in streets_order for a in actions_order},
    }

    if bet_probs:
        sorted_probs = sorted(bet_probs)
        n = len(sorted_probs)
        for pct_label, idx in [("p10", int(n*0.1)), ("p25", int(n*0.25)),
                                ("p50", int(n*0.5)), ("p75", int(n*0.75)),
                                ("p90", int(n*0.9))]:
            idx = min(idx, n-1)
            output['bet_prob_distribution']['percentiles'][pct_label] = round(sorted_probs[idx], 4)
        output['bet_prob_distribution']['mean'] = round(statistics.mean(bet_probs), 4)

    for d in facing_bet_3way[:20]:
        output['facing_bet_3way_examples'].append({
            'street': d.street, 'position': d.player_position,
            'action': d.action, 'pot': d.pot, 'to_call': d.to_call,
            'equity': round(d.equity, 3), 'num_opponents': d.num_opponents,
            'hero_cards': d.hero_cards, 'board': d.board,
            'was_adjusted': d.was_adjusted,
        })

    interesting_all = [d for d in facing_bet_3way
                       if d.feat_dict and d.equity > 0.15 and d.equity < 0.85 and d.pot > 30]
    output['interesting_for_v24'] = len(interesting_all)

    # Facing-bet by opponent count
    if facing_bet_all:
        output['facing_bet_by_opponents'] = {}
        for d in facing_bet_all:
            key = str(d.num_opponents)
            output['facing_bet_by_opponents'][key] = output['facing_bet_by_opponents'].get(key, 0) + 1

    output_path = os.path.join(CORE_DIR, '..', 'review', 'v23_selfplay_raw.json')
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nRaw output saved to: {output_path}")


if __name__ == '__main__':
    main()
