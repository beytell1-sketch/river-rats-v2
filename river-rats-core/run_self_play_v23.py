"""Thin wrapper: run self_play.py with the v2.3 (108-feature) model.

The v2.3 model expects 108 features (54 raw + 54 attn_* = all 1.0 at
inference).  self_play.py calls GtoOracle.features_from_dict() which
returns 54 features.  This wrapper monkey-patches GtoOracle.predict to
pad the 54-feature vector with 54 ones before scoring.

Usage:
    python run_self_play_v23.py [--deals 2000] [--seed 42]
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
from collections import Counter

import numpy as np

# Ensure river-rats-core is on path
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS_DIR)

from gto_model import GtoOracle, OraclePrediction  # noqa: E402
from self_play import SelfPlayRunner, Variant  # noqa: E402
from multiway_adjuster import get_default_params  # noqa: E402


# ---------------------------------------------------------------------------
# Monkey-patch: pad 54 → 108 with attn=1.0
# ---------------------------------------------------------------------------
_original_predict = GtoOracle.predict


def _patched_predict(self, features: np.ndarray) -> OraclePrediction:
    """Pad 54-feature vector to 108 with attn=1.0, then call original."""
    if features.ndim == 1 and features.shape[0] < self._n_features:
        pad = np.ones(self._n_features - features.shape[0], dtype=features.dtype)
        features = np.concatenate([features, pad])
    elif features.ndim == 2 and features.shape[1] < self._n_features:
        pad = np.ones((features.shape[0], self._n_features - features.shape[1]),
                      dtype=features.dtype)
        features = np.concatenate([features, pad], axis=1)
    return _original_predict(self, features)


GtoOracle.predict = _patched_predict


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="v2.3 self-play diagnostic")
    parser.add_argument("--deals", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    model_path = os.path.join(_THIS_DIR, "models", "v2_3_model_shipped.json")
    assert os.path.exists(model_path), f"Model not found: {model_path}"

    variant = Variant("v2.3", get_default_params())
    runner = SelfPlayRunner(
        [variant],
        num_deals=args.deals,
        seed=args.seed,
        oracle_path=model_path,
        log_all_multiway=True,
        single_position="BTN",
    )

    print(f"Running {args.deals} deals with v2.3 model (seed={args.seed}) ...")
    t0 = time.time()
    result = runner.run_round()
    elapsed = time.time() - t0
    print(f"Done in {elapsed:.1f}s  ({result.num_games} games)")

    # --- Collect metrics ---
    all_postflop_hero = []
    all_postflop_opp = []
    facing_bet_situations = []
    bet_probs_check_to_hero = []

    for gr in result.game_results:
        for d in gr.hero_decisions:
            if d.is_preflop:
                continue
            all_postflop_hero.append(d)
            if d.facing_bet:
                facing_bet_situations.append(d)
        for pos, decs in gr.opponent_decisions.items():
            for d in decs:
                if d.is_preflop:
                    continue
                all_postflop_opp.append(d)
                if d.facing_bet:
                    facing_bet_situations.append(d)

    all_postflop = all_postflop_hero + all_postflop_opp

    # BET probability in check-to-hero spots
    # "Check to hero" = hero faces no bet (facing_bet=False) and can bet
    check_to_hero = [d for d in all_postflop_hero if not d.facing_bet]
    for d in check_to_hero:
        if d.feat_dict:
            bet_probs_check_to_hero.append(
                float(d.feat_dict.get("_bet_prob", 0))
                if "_bet_prob" in d.feat_dict
                else None
            )

    # Action distribution
    action_counts = Counter()
    street_action_counts: dict = {}
    for d in all_postflop:
        action_counts[d.action] += 1
        key = (d.street, d.action)
        street_action_counts[key] = street_action_counts.get(key, 0) + 1

    # BET probability from oracle for check-to-hero (need to re-extract)
    # Actually let's get it from the oracle predictions stored in feat_dict
    # The feat_dict doesn't store oracle probs. Let me compute BET prob
    # by re-running oracle on check-to-hero spots.
    oracle = GtoOracle(model_path)
    from gto_model import FEATURE_COLUMNS
    bet_probs = []
    for d in check_to_hero:
        if d.feat_dict:
            try:
                feats = GtoOracle.features_from_dict(d.feat_dict)
                pred = oracle.predict(feats)
                bet_probs.append(pred.probs.get("BET", 0.0))
            except Exception:
                pass

    # Stats
    n_check_to_hero = len(check_to_hero)
    n_bet_prob_low = sum(1 for p in bet_probs if p < 0.05)
    pct_bet_low = (n_bet_prob_low / len(bet_probs) * 100) if bet_probs else 0

    # 3-way postflop yield
    total_deals = args.deals
    three_way_postflop = sum(1 for d in all_postflop if d.num_opponents >= 2)
    three_way_yield = three_way_postflop / total_deals * 100 if total_deals else 0

    bet_raise_actions = sum(1 for d in all_postflop if d.action in ("bet", "raise"))

    # BET prob percentiles
    if bet_probs:
        bp = sorted(bet_probs)
        p10 = bp[int(len(bp)*0.10)]
        p25 = bp[int(len(bp)*0.25)]
        p50 = bp[int(len(bp)*0.50)]
        p75 = bp[int(len(bp)*0.75)]
        p90 = bp[min(int(len(bp)*0.90), len(bp)-1)]
        mean_bp = sum(bp) / len(bp)
    else:
        p10 = p25 = p50 = p75 = p90 = mean_bp = 0

    # Print report
    print("\n" + "="*60)
    print("SELF-PLAY DIAGNOSTIC: v2.3 vs v2.2 baseline")
    print("="*60)
    print(f"Deals: {total_deals}  |  Elapsed: {elapsed:.1f}s")
    print(f"Total postflop decisions: {len(all_postflop)}")
    print(f"  Hero postflop: {len(all_postflop_hero)}")
    print(f"  Opponent postflop: {len(all_postflop_opp)}")
    print()
    print(f"Check-to-hero spots: {n_check_to_hero}")
    print(f"  BET prob < 0.05: {n_bet_prob_low}/{len(bet_probs)} = {pct_bet_low:.1f}%  (v2.2: 63%)")
    print(f"  BET prob mean: {mean_bp:.4f}")
    print(f"  BET prob percentiles: p10={p10:.4f} p25={p25:.4f} p50={p50:.4f} p75={p75:.4f} p90={p90:.4f}")
    print()
    print(f"Facing-bet situations (all seats): {len(facing_bet_situations)}  (v2.2: ~0)")
    print(f"3-way postflop decisions: {three_way_postflop}")
    print(f"3-way postflop yield: {three_way_yield:.1f}%  (v2.2: 3.7%)")
    print(f"BET/RAISE actions (all seats): {bet_raise_actions}")
    print()
    print("Action distribution (postflop, all seats):")
    for action in sorted(action_counts.keys()):
        print(f"  {action}: {action_counts[action]}")
    print()
    print("Per-street breakdown:")
    for (street, action), count in sorted(street_action_counts.items()):
        print(f"  {street:10s} {action:8s}: {count}")

    # Save raw data for the report
    report_data = {
        "deals": total_deals,
        "elapsed_s": round(elapsed, 1),
        "total_postflop": len(all_postflop),
        "hero_postflop": len(all_postflop_hero),
        "opp_postflop": len(all_postflop_opp),
        "check_to_hero_spots": n_check_to_hero,
        "bet_prob_lt_005_pct": round(pct_bet_low, 1),
        "bet_prob_mean": round(mean_bp, 4),
        "bet_prob_percentiles": {
            "p10": round(p10, 4), "p25": round(p25, 4),
            "p50": round(p50, 4), "p75": round(p75, 4),
            "p90": round(p90, 4),
        },
        "facing_bet_total": len(facing_bet_situations),
        "three_way_postflop": three_way_postflop,
        "three_way_yield_pct": round(three_way_yield, 1),
        "bet_raise_actions": bet_raise_actions,
        "action_distribution": dict(action_counts),
        "street_actions": {f"{s}_{a}": c for (s,a), c in street_action_counts.items()},
    }
    out_path = os.path.join(_THIS_DIR, "..", "review", "comms",
                            "self_play_v23_raw.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(report_data, f, indent=2)
    print(f"\nRaw data saved to {out_path}")


if __name__ == "__main__":
    main()
