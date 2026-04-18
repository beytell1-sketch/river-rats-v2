#!/usr/bin/env python3
"""v2.3.1 self-play diagnostic — 2000 deals, all metrics + anomaly watches.

Adapted from review/run_v23_selfplay_diagnostic.py (commit 1ffe688) for
v2.3.1's 110-feature schema (55 raw + 55 attn=1.0). Layer 1 added
`board_adjusted_hrp` as feature 55; Layer 2 added 40 air-CHECK 3-way
counter-examples.

Per REVIEW_V231_TRAIN_EVAL post-sweep directive, watches for:
  - Facing-bet count: should match/improve v2.3's 1269 (not collapse
    toward v2.2's ~0)
  - Action distribution: BET/RAISE share healthy; CHECK shouldn't spike
    above v2.3 baseline (over-correction signal from air-CHECK counter-
    examples)
  - board_adjusted_hrp artifacts: bet-sizing degeneracy not directly
    observable with this model (action-only), but we report bah
    distribution + position asymmetry in the action breakdown as a
    proxy signal.

Outputs:
  review/v231_selfplay_raw.json

Usage (run AFTER commit of this script):
    python3 review/run_v231_selfplay_diagnostic.py
"""
import sys
import os
import json
import statistics

CORE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                        'river-rats-core')
sys.path.insert(0, CORE_DIR)

import numpy as np
from self_play import SelfPlayRunner, Variant
from multiway_adjuster import get_default_params
from gto_model import GtoOracle, FEATURE_COLUMNS, OraclePrediction, ACTION_CLASSES
from train_model_v2_2 import encode

MODEL_PATH = os.path.join(CORE_DIR, 'models', 'v2_3_1_model.json')
NUM_DEALS = 2000
SEED = 42

# v2.3.1: 55 raw features (board_adjusted_hrp added as #55)
N_RAW = len(FEATURE_COLUMNS)
N_ATTN = N_RAW
N_TOTAL = N_RAW + N_ATTN  # 110

# v2.3 baseline (commit 4d81c08 report) — for comparison reporting
V23_BASELINE = {
    'check_to_hero_low_bet_pct': 0.0,
    'facing_bet_3way_count': 1269,
    'threeway_postflop_yield_pct': 5.7,
    'total_postflop_decisions': 2772,
    'bet_prob_median': 0.7289,
    'bet_prob_mean': 0.6966,
}
# v2.2 baseline (same report) — for comparison
V22_BASELINE = {
    'check_to_hero_low_bet_pct': 63.0,  # passive-loop signature
    'facing_bet_3way_count': 0,          # ~0
    'threeway_postflop_yield_pct': 3.7,
}


class V231Oracle:
    """Wrap GtoOracle to produce 110-feature vectors for v2.3.1.

    Pads 55-raw from extractor → 55-raw + 55 ones (attn=1.0 inference
    strategy).
    """

    def __init__(self, model_path: str):
        import xgboost as xgb
        self._model = xgb.XGBClassifier()
        self._model.load_model(model_path)
        assert self._model.n_features_in_ == N_TOTAL, (
            f"Expected {N_TOTAL} features, got {self._model.n_features_in_}"
        )
        self._action_map = {i: a for i, a in enumerate(ACTION_CLASSES)}

    def predict(self, features: np.ndarray) -> OraclePrediction:
        if features.ndim == 1:
            if len(features) <= N_RAW:
                features = np.concatenate(
                    [features, np.ones(N_ATTN, dtype=np.float32)]
                )
            X = features.reshape(1, -1)
        else:
            if features.shape[1] <= N_RAW:
                pad = np.ones((features.shape[0], N_ATTN), dtype=np.float32)
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
        """Build N_RAW-feature array using CAT_MAPS encoding (matches training)."""
        arr = np.zeros(N_RAW, dtype=np.float32)
        for i, col in enumerate(FEATURE_COLUMNS):
            arr[i] = encode(feat_dict, col)
        return arr

    @property
    def action_probs(self):
        return None


def main():
    print(f"Loading model: {MODEL_PATH}")
    oracle = V231Oracle(MODEL_PATH)
    print(f"Model loaded ({N_TOTAL}-feature v2.3.1, raw={N_RAW} attn={N_ATTN}).")

    # Monkey-patch GtoOracle.features_from_dict to use CAT_MAPS encoding.
    GtoOracle.features_from_dict = staticmethod(V231Oracle.features_from_dict)

    variants = [Variant("v2.3.1", get_default_params())]
    runner = SelfPlayRunner(
        variants=variants,
        num_deals=NUM_DEALS,
        seed=SEED,
        oracle=oracle,
        log_all_multiway=True,
    )

    print(f"Running {NUM_DEALS} deals, seed={SEED}, 6 positions per deal...")
    print(f"Total games: {NUM_DEALS} × 6 × 1 variant = {NUM_DEALS * 6}")
    result = runner.run_round()
    print(f"Run complete: {result.num_games} games played")

    # Collect decisions
    all_postflop = []
    all_preflop = []
    hero_postflop = []
    for gr in result.game_results:
        for d in gr.hero_decisions:
            (all_preflop if d.is_preflop else all_postflop).append(d)
            if not d.is_preflop:
                hero_postflop.append(d)
        for pos, decs in gr.opponent_decisions.items():
            for d in decs:
                (all_preflop if d.is_preflop else all_postflop).append(d)

    print(f"\nTotal postflop decisions: {len(all_postflop)}")
    print(f"  Hero postflop: {len(hero_postflop)}")
    print(f"  Opponent postflop: {len(all_postflop) - len(hero_postflop)}")
    print(f"Total preflop decisions: {len(all_preflop)}")

    if len(all_postflop) == 0:
        print("\n*** STOP: Zero postflop decisions. Something is wrong. ***")
        sys.exit(1)

    # ── Metric 1: Check-to-hero BET probability < 0.05 (passive-loop signature)
    check_to_hero = [
        d for d in all_postflop
        if not d.facing_bet and d.num_opponents >= 2
    ]
    print("\nRe-running oracle on check-to-hero spots...")
    bet_probs = []
    for d in check_to_hero:
        if d.feat_dict:
            features = V231Oracle.features_from_dict(d.feat_dict)
            pred = oracle.predict(features)
            bet_prob = pred.probs.get('BET', 0.0) + pred.probs.get('RAISE', 0.0)
            bet_probs.append(bet_prob)

    pct_low_bet = None
    if bet_probs:
        low_bet = sum(1 for p in bet_probs if p < 0.05)
        pct_low_bet = low_bet / len(bet_probs) * 100
        print(f"\nCheck-to-hero 3-way+ spots: {len(check_to_hero)}")
        print(f"  With BET prob < 0.05: {low_bet} ({pct_low_bet:.1f}%)")
        print(f"  BET prob distribution:")
        sorted_probs = sorted(bet_probs)
        n = len(sorted_probs)
        pct_map = {}
        for pct_label, idx in [("p10", int(n*0.1)), ("p25", int(n*0.25)),
                                ("p50", int(n*0.5)), ("p75", int(n*0.75)),
                                ("p90", int(n*0.9))]:
            idx = min(idx, n-1)
            pct_map[pct_label] = sorted_probs[idx]
            print(f"    {pct_label}: {sorted_probs[idx]:.4f}")
        mean_bet = statistics.mean(bet_probs)
        print(f"    mean: {mean_bet:.4f}")

    # ── Metric 2: Facing-bet situations (3-way+)
    facing_bet_3way = [
        d for d in all_postflop if d.facing_bet and d.num_opponents >= 2
    ]
    print(f"\nFacing-bet 3-way+ situations: {len(facing_bet_3way)}")

    # ── Metric 3: 3-way postflop yield
    threeway_postflop = [d for d in all_postflop if d.num_opponents >= 2]
    total_postflop = len(all_postflop)
    threeway_yield = (len(threeway_postflop) / total_postflop * 100
                      if total_postflop else 0)
    print(f"\n3-way+ postflop: {len(threeway_postflop)}/{total_postflop} "
          f"= {threeway_yield:.1f}%")

    # ── Metric 4: BET/RAISE actions per 1000 deals
    bet_actions = [d for d in all_postflop if d.action in ('bet', 'raise')]
    bet_per_1000 = len(bet_actions) / NUM_DEALS * 1000
    print(f"\nBET/RAISE actions (postflop): {len(bet_actions)} "
          f"({bet_per_1000:.1f} per 1000 deals)")

    # ── Per-street action breakdown
    print("\n-- Per-street action breakdown --")
    street_actions = {}
    for d in all_preflop + all_postflop:
        street = d.street if not d.is_preflop else 'preflop'
        action = d.action.upper()
        key = (street, action)
        street_actions[key] = street_actions.get(key, 0) + 1

    streets_order = ['preflop', 'flop', 'turn', 'river']
    actions_order = ['FOLD', 'CHECK', 'CALL', 'BET', 'RAISE']
    print(f"{'Street':<10} " + " ".join(f"{a:<8}" for a in actions_order)
          + " TOTAL")
    for street in streets_order:
        counts = [street_actions.get((street, a), 0) for a in actions_order]
        total = sum(counts)
        if total > 0:
            print(f"{street:<10} " + " ".join(f"{c:<8}" for c in counts)
                  + f" {total}")

    # ── ANOMALY WATCH: postflop CHECK share (over-correction from Layer 2)
    postflop_totals = {a: 0 for a in actions_order}
    for d in all_postflop:
        postflop_totals[d.action.upper()] = (
            postflop_totals.get(d.action.upper(), 0) + 1
        )
    postflop_total = sum(postflop_totals.values())
    print("\n-- Postflop action shares (% of all postflop decisions) --")
    share_by_action = {}
    for a in actions_order:
        pct = 100 * postflop_totals[a] / max(1, postflop_total)
        share_by_action[a] = pct
        print(f"  {a:<6}: {postflop_totals[a]:>4} ({pct:>5.1f}%)")

    # ── ANOMALY WATCH: position asymmetry (board_adjusted_hrp interaction check)
    # Break down postflop actions by hero_position.
    pos_action = {}
    for d in all_postflop:
        pos = d.player_position
        a = d.action.upper()
        pos_action.setdefault(pos, {aa: 0 for aa in actions_order})
        pos_action[pos][a] += 1
    print("\n-- Postflop action distribution by position --")
    print(f"{'pos':<6} " + " ".join(f"{a:<8}" for a in actions_order)
          + "  TOTAL")
    for pos in sorted(pos_action.keys()):
        row = pos_action[pos]
        tot = sum(row.values())
        print(f"{pos:<6} "
              + " ".join(f"{row[a]:>4}({100*row[a]/max(1,tot):>4.1f}%)"
                         for a in actions_order)
              + f"   {tot}")

    # ── ANOMALY WATCH: board_adjusted_hrp distribution on hero postflop
    bah_values = []
    for d in hero_postflop:
        if d.feat_dict:
            bah = d.feat_dict.get('board_adjusted_hrp', 0.0)
            try:
                bah_values.append(float(bah))
            except (TypeError, ValueError):
                pass
    print("\n-- board_adjusted_hrp distribution (hero postflop) --")
    if bah_values:
        sb = sorted(bah_values)
        n = len(sb)
        pcts = {}
        for lbl, idx in [("min", 0), ("p25", int(n*0.25)),
                         ("p50", int(n*0.5)), ("p75", int(n*0.75)),
                         ("p90", int(n*0.9)), ("max", n-1)]:
            pcts[lbl] = sb[min(idx, n-1)]
        print(f"  n={n}  "
              f"mean={statistics.mean(bah_values):.3f}  "
              f"min={pcts['min']:.3f}  p25={pcts['p25']:.3f}  "
              f"p50={pcts['p50']:.3f}  p75={pcts['p75']:.3f}  "
              f"p90={pcts['p90']:.3f}  max={pcts['max']:.3f}")
        # How many hero postflop decisions had bah > 0?
        nonzero = sum(1 for v in bah_values if v > 0)
        print(f"  non-zero: {nonzero}/{n} ({100*nonzero/n:.1f}%)")
    else:
        print("  No hero-postflop feat_dict values for bah.")

    # ── Assessment vs v2.3 / v2.2 baselines
    print("\n" + "=" * 60)
    print("COMPARISON vs v2.2 / v2.3")
    print("=" * 60)
    print(f"{'Metric':<38} {'v2.2':>10} {'v2.3':>10} {'v2.3.1':>10}")
    print("-" * 70)
    metrics_table = [
        ("Check-to-hero BET prob < 0.05 (%)",
         V22_BASELINE['check_to_hero_low_bet_pct'],
         V23_BASELINE['check_to_hero_low_bet_pct'],
         pct_low_bet),
        ("Facing-bet 3-way+ count",
         V22_BASELINE['facing_bet_3way_count'],
         V23_BASELINE['facing_bet_3way_count'],
         len(facing_bet_3way)),
        ("3-way postflop yield (%)",
         V22_BASELINE['threeway_postflop_yield_pct'],
         V23_BASELINE['threeway_postflop_yield_pct'],
         round(threeway_yield, 1)),
        ("Total postflop decisions",
         None,
         V23_BASELINE['total_postflop_decisions'],
         total_postflop),
        ("BET prob median (check-to-hero)",
         None,
         V23_BASELINE['bet_prob_median'],
         round(statistics.median(bet_probs), 4) if bet_probs else None),
        ("BET prob mean (check-to-hero)",
         None,
         V23_BASELINE['bet_prob_mean'],
         round(statistics.mean(bet_probs), 4) if bet_probs else None),
    ]
    for name, v22, v23, v231 in metrics_table:
        f = lambda v: "—" if v is None else (f"{v:.4f}" if isinstance(v, float) else str(v))
        print(f"{name:<38} {f(v22):>10} {f(v23):>10} {f(v231):>10}")

    # ── Verdict signals
    print("\n-- Anomaly watch --")
    anomalies = []
    passive_loop_broken = len(facing_bet_3way) > 0
    if not passive_loop_broken:
        anomalies.append("Passive loop re-emerged (facing_bet_3way=0)")
    # Collapse check: facing-bet drops > 30% vs v2.3
    if (V23_BASELINE['facing_bet_3way_count'] > 0
            and len(facing_bet_3way) < V23_BASELINE['facing_bet_3way_count'] * 0.70):
        anomalies.append(
            f"Facing-bet count collapsed: {len(facing_bet_3way)} "
            f"< 0.7×1269 = {int(V23_BASELINE['facing_bet_3way_count']*0.7)}"
        )
    # CHECK-share over-correction: if postflop CHECK > 25% it's a spike
    # (v2.3's per-street showed CHECK share 7-16% ish; 25%+ at postflop
    # total level is the over-correction signal)
    check_share = share_by_action.get('CHECK', 0)
    if check_share > 25:
        anomalies.append(
            f"CHECK share spike at postflop: {check_share:.1f}% > 25% threshold"
        )
    if pct_low_bet is not None and pct_low_bet > 5:
        anomalies.append(
            f"Check-to-hero low-BET spots resurgent: {pct_low_bet:.1f}% > 5%"
        )

    if anomalies:
        print("  **ANOMALIES DETECTED** — stop-and-report discipline:")
        for a in anomalies:
            print(f"    - {a}")
    else:
        print("  No anomalies on any watch. Clean run.")

    # ── Save structured output
    output = {
        'config': {
            'model': 'v2_3_1_model.json',
            'num_deals': NUM_DEALS,
            'seed': SEED,
            'total_games': result.num_games,
            'n_features_total': N_TOTAL,
            'n_features_raw': N_RAW,
        },
        'metrics': {
            'check_to_hero_low_bet_pct': (
                round(pct_low_bet, 1) if pct_low_bet is not None else None
            ),
            'facing_bet_3way_count': len(facing_bet_3way),
            'threeway_postflop_yield_pct': round(threeway_yield, 1),
            'total_postflop_decisions': total_postflop,
            'bet_actions_per_1000_deals': round(bet_per_1000, 1),
            'passive_loop_broken': passive_loop_broken,
            'check_to_hero_n_spots': len(check_to_hero),
        },
        'bet_prob_distribution': {
            'count': len(bet_probs) if bet_probs else 0,
            'percentiles': pct_map if bet_probs else {},
            'mean': round(statistics.mean(bet_probs), 4) if bet_probs else None,
            'median': round(statistics.median(bet_probs), 4) if bet_probs else None,
        },
        'postflop_action_shares_pct': share_by_action,
        'position_action_breakdown': {
            pos: {a: pos_action[pos][a] for a in actions_order}
            for pos in pos_action
        },
        'board_adjusted_hrp_stats': (
            {
                'n': len(bah_values),
                'mean': round(statistics.mean(bah_values), 4),
                'median': round(statistics.median(bah_values), 4),
                'nonzero_pct': (
                    round(100 * sum(1 for v in bah_values if v > 0) /
                          max(1, len(bah_values)), 1)
                ),
            }
            if bah_values else None
        ),
        'street_actions': {
            f"{s}_{a}": street_actions.get((s, a), 0)
            for s in streets_order for a in actions_order
        },
        'baselines': {'v2_2': V22_BASELINE, 'v2_3': V23_BASELINE},
        'anomalies': anomalies,
    }

    output_path = os.path.join(
        CORE_DIR, '..', 'review', 'v231_selfplay_raw.json'
    )
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nRaw output saved to: {output_path}")

    if anomalies:
        print("\n**STOP CONDITION: anomalies detected. Reporting, not shipping.**")
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
