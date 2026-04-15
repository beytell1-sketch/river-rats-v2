---
date: 2026-04-15
from: Builder
to: Main terminal
re: Track 3.5 follow-up — v2.2 feature-importance cross-check
status: COMPLETE — Branch C → defaults to Branch B
model: river-rats-core/models/v2_2_model.json (108 features, 62 used, best_iteration=95)
---

# V2.2 Feature-Importance Cross-Check

## Method

- Loaded `river-rats-core/models/v2_2_model.json` via `xgboost.Booster.load_model` (xgb 3.2.0).
- Model was serialised without `feature_names` (empty in learner JSON), so features are indexed `f0..f107`.
- Reconstructed the name mapping from the training CSV header (`training-data/v2_2_training.csv`):
  columns `[1:-2]` (drop `situation_id`, `label`, `label_source`) → 108 features in order.
  Verified: `f0=street`, `f6=hero_position`, `f54=attn_street`, `f60=attn_hero_position`.
- `v2_2_training_report.json` does NOT contain pre-computed importance, so no comparison
  to report values was possible (no disagreement to flag).
- Computed `get_score` for `gain`, `weight`, `cover`. Missing features (46 of 108) treated as 0.
- Total gain across all trees = **75.6921**; total splits = **3791**.

## Top 10 features by gain

| rank | feature                              |    gain | % of total | splits | cover   |
|-----:|--------------------------------------|--------:|-----------:|-------:|--------:|
|    1 | equity_margin                        | 11.3635 |     15.01% |    584 | 41.298  |
|    2 | attn_pot_odds                        |  9.8459 |     13.01% |    133 | 53.018  |
|    3 | facing_bet                           |  7.3887 |      9.76% |    384 | 34.239  |
|    4 | attn_villain_fold_equity_estimate    |  4.6249 |      6.11% |     12 | 34.384  |
|    5 | raw_equity                           |  4.5633 |      6.03% |    261 | 22.749  |
|    6 | better_hand_pct                      |  4.4433 |      5.87% |    300 | 19.633  |
|    7 | attn_has_showdown_value              |  2.8070 |      3.71% |    213 | 19.216  |
|    8 | facing_raise                         |  2.3728 |      3.13% |     45 | 73.661  |
|    9 | flush_draw_rank                      |  2.1102 |      2.79% |     59 | 21.503  |
|   10 | attn_better_hand_pct                 |  1.9336 |      2.55% |      4 |  3.603  |

Top-10 sanity check: usual suspects are at the top (equity_margin, raw_equity,
better_hand_pct, facing_bet/raise, attn_pot_odds). Matches expectation.

## Target features

| feature              | rank (by gain) |    gain | % of total | splits | cover |
|----------------------|---------------:|--------:|-----------:|-------:|------:|
| street               |    **20** /108 | 0.7139  |    0.943%  |     95 | 4.612 |
| hero_position        |    **44** /108 | 0.2398  |    0.317%  |     56 | 5.868 |
| attn_street          |    **84** /108 | 0.0000  |    0.000%  |      0 | 0.000 |
| attn_hero_position   |    **87** /108 | 0.0000  |    0.000%  |      0 | 0.000 |

- **Combined `street` + `hero_position` gain share: 1.260% of total.**
- Attention mirrors `attn_street` / `attn_hero_position` were never split on — the
  model learned nothing from them. No unusual pattern — they are simply dead weight
  (consistent with the mixed-encoding question only affecting the raw columns, not
  their attention doubles, or the attention gating zeroing them out upstream).
- Notable: `street` has 95 splits but only 0.94% of gain — the tree used it often
  for low-information partitions (gain-per-split = 0.0075, vs top-10 range 0.004
  to 0.164). Consistent with street acting as a coarse partition feature rather
  than a high-signal one.

## Branch decision

Thresholds from `MAIN_TERMINAL_UPDATE_2026-04-15-c.md` §4:

- Branch A (LOW-IMPACT): combined < 5% **AND** neither in top 20.
  - Combined 1.26% < 5% ✓
  - `street` is at rank **20** → in top 20 (inclusive). ✗
  - **Does not qualify.**
- Branch B (NON-TRIVIAL): either in top 20 **OR** combined > 5%.
  - `street` rank 20 qualifies. ✓
- Branch C (AMBIGUOUS): rank **15-25**, or combined **3-5%**.
  - `street` rank 20 is in 15-25 band. ✓
  - Combined 1.26% is below 3-5% band.

`street` at rank 20 with gain fraction 0.94% sits inside Branch C's rank band
(15-25) despite the combined gain being well under 3%. Per §4 Branch C rule,
**"Default to Branch B. Quality-focused; we are not in a rush."**

**Chosen branch: C → defaults to B (NON-TRIVIAL).**

Rationale (one line): street is rank 20/108 (Branch C band) — per directive,
borderline defaults to Branch B, so trainer recovery runs before Track 4.

## Next step

Start trainer recovery per §4 Branch B: search for the v2.2 training script
(local machines, shell history, notebooks) or rewrite
`river-rats-core/train_model_v2_2.py` from the training report + CSV schema,
then verify CV 93.0% ± 3.5% / holdout 88.3%.
Deliverable: `review/comms/V22_TRAINER_RECOVERY_2026-04-15.md`.

Track 4 remains held until trainer recovery lands.
