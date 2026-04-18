---
date: 2026-04-18
from: Builder (programmer)
to: Main terminal (reviewer/orchestrator)
re: Self-play diagnostic — v2.3 vs v2.2 baseline
status: COMPLETE
---

# Self-Play Diagnostic: v2.3

## Configuration

- Model: `v2_3_model_shipped.json` (108 features: 54 raw + 54 attn=1.0)
- Deals: 2000 (full run, not extrapolated)
- Seed: 42
- Position: BTN (single_position mode, log_all_multiway=True)
- All 6 seats use oracle callbacks (same as v2.2 setup)
- Runtime: 310.7s (~5.2 min)

### Implementation note

self_play.py expects v8/v9 models (38-45 features). The v2.3 model
uses 108 features (54 raw + 54 attention). A thin wrapper
(`run_self_play_v23.py`) monkey-patches `GtoOracle.predict` to pad
the 54-feature vector with 54 ones (the attention-all-ones inference
strategy documented in `evaluate_v2_2.py`). self_play.py itself was
not modified.

## Comparison Table

| Metric | v2.2 | v2.3 | Delta |
|---|---|---|---|
| Check-to-hero BET prob < 0.05 | 63% | **0.0%** | -63pp |
| Facing-bet situations / 2000 deals | ~0 | **1269** | +1269 |
| 3-way postflop yield | 3.7% | **5.7%** | +2.0pp |
| Total postflop decisions | — | 2772 | — |
| BET/RAISE actions (all seats) | — | 1258 | — |

## BET Probability Distribution (check-to-hero spots, N=86)

| Percentile | BET prob |
|---|---|
| p10 | 0.2366 |
| p25 | 0.4904 |
| p50 (median) | 0.7289 |
| p75 | 0.9363 |
| p90 | 0.9880 |
| Mean | 0.6966 |
| % below 0.05 | 0.0% |

v2.2 had 63% of check-to-hero spots with BET prob < 0.05 (the
passive-loop signature). v2.3 has **zero** spots below 0.05. The
median BET probability is 0.73 — the model actively wants to bet
in most checked-to spots.

## Facing-Bet Count

- **1269 facing-bet decisions** across all seats in 2000 deals
- v2.2 produced approximately **zero**
- This means ~63% of all postflop decisions (1269/2772) involve
  facing a bet — a realistic game dynamic

## Per-Street Action Breakdown

| Street | BET | CALL | CHECK | FOLD | RAISE |
|---|---|---|---|---|---|
| Flop | 520 | 360 | 199 | 165 | 15 |
| Turn | 378 | 321 | 51 | 61 | 14 |
| River | 321 | 228 | 34 | 95 | 10 |

Action frequencies look healthy: bet is the most common action on
every street, with a reasonable fold rate that increases on the river
(13.8%) vs flop (13.1%). CHECK frequency decreases from flop (15.8%)
to river (4.9%) — players bet more as the hand progresses, which is
consistent with polarizing ranges.

## Passive-Loop Verdict

**The passive loop is broken.**

v2.2 self-play exhibited a degenerate equilibrium: all 6 oracle
seats checked through, producing zero facing-bet situations. The
bias-corrected v2.3 model generates 1269 facing-bet situations in
2000 deals — a complete reversal.

Key evidence:
1. Zero check-to-hero spots with BET prob < 0.05 (was 63%)
2. 1269 facing-bet situations (was ~0)
3. BET/RAISE actions outnumber CHECK actions 4.4:1
4. Every street shows active betting, not passive checking

## Implications for v2.4

Self-play with v2.3 generates realistic game situations with actual
betting action. This opens the self-play-to-expert-labelling pipeline
described in MAIN_TERMINAL_UPDATE_2026-04-18-c.md: self-play
generates situations, expert panels label them, avoiding both
factory-generation artificiality and oracle-labels-its-own-data
reinforcement.

Rough count of "interesting" situations for potential expert
labelling: 1269 facing-bet decisions + 86 check-to-hero spots =
1355 postflop decision points from a single 2000-deal run.
