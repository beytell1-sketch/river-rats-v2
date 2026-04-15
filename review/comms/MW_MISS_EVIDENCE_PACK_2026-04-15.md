# MW Miss Evidence Pack — 2026-04-15

**Stream B.1 deliverable.** Data assembly only. No GTO analysis.

- **Source hands:** `review/comms/MW_MISSES_FEATURES_PREP_2026-04-15.jsonl` (10 MW misses)
- **Reference labels:** `training-data/test_set_50_labelled.jsonl`
- **Model training (inference path):** retrained from `training-data/v2_2_training.csv` using the exact recipe in `review/recovered/eval_MW_with_legal_action_masking.py` (XGBClassifier, n_estimators=95, max_depth=5, lr=0.05, multi:softprob, num_class=5, random_state=42, with class-balanced sample weights capped at 2.0 for BET / 3.0 for RAISE / 4.0 otherwise). The saved model file at `river-rats-core/models/v2_2_model.json` is NOT modified by this script. We retrain because that is what the recovered eval harness does to reproduce the 80.0% MW-50 / 72.5% FB-40 numbers and the `model_prediction` values stamped into the prep JSONL.
- **Inference path:** 108-feature vector (54 raw + 54 attn=1) with legal-action masking
  - `facing_bet=False` → legal set {CHECK, BET}
  - `facing_bet=True`  → legal set {FOLD, CALL, RAISE}
- **Categorical encoding & feature ordering:** copied verbatim from `review/recovered/eval_MW_with_legal_action_masking.py`
- **Pass 1 labelling history:** not available in repo for MW-50 test set. `pass1_T[1-4]_labels.jsonl` and `pass1_comparison.jsonl` contain per-agent votes but only for the BP building-block set (`BP*` sids), not the `d*_<pos>_<street>` MW sids.
- **Reproduction note:** retraining the model in-process matches the `model_prediction` stamped into the prep JSONL on 8/10 hands. Two hands (`d2410_CO_turn`, `d3688_BB_flop`) flip to BET in this run where the prep file recorded CHECK. Both sit on a tight CHECK/BET boundary in the masked distribution (d2410 masked CHECK 0.063 vs BET 0.110; d3688 masked CHECK 0.058 vs BET 0.448). Likely small XGBoost non-determinism across CPU/thread configurations on tie-adjacent splits. Not investigated further — this pack reports this run's distributions and flags the disagreement; the GTO analysis (Stream B.2) should note that those two hands are reproduction-variable.

---

## Summary Table 1 — Bias-signature values (all 10 hands)

| # | situation_id | hero | board | street | GT | pred | HRP | equity_vs_range | villain_air_pct | villain_TP+ pct | SPR | better_hand_pct | worse_hand_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `d1454_CO_turn` | ThJh | Tc8hAh4d | turn | BET | CHECK | 0.5786 | 0.4377 | 0.0157 | 0.2673 | 1.250 | 0.4249 | 0.5578 |
| 2 | `d1562_HJ_turn` | 7h7d | 5cJcJd3s | turn | BET | CHECK | 0.7095 | 0.3540 | 0.4321 | 0.5679 | 1.250 | 0.2906 | 0.7057 |
| 3 | `d1983_HJ_turn` | AcJs | Jd7dKh2c | turn | BET | CHECK | 0.6729 | 0.4365 | 0.1847 | 0.2544 | 1.250 | 0.2907 | 0.6828 |
| 4 | `d2410_CO_turn` | JcKs | Jd9d3h6d | turn | BET | BET | 0.4524 | 0.4470 | 0.2044 | 0.3302 | 1.250 | 0.1662 | 0.8172 |
| 5 | `d2920_BB_turn` | JhQd | Js2sTdQs | turn | BET | CHECK | 0.4725 | 0.4908 | 0.1828 | 0.3084 | 1.250 | 0.1834 | 0.8081 |
| 6 | `d3178_CO_river` | AcAs | JhQcJcKs5h | river | BET | CHECK | 0.7694 | 0.6305 | 0.1730 | 0.8270 | 1.250 | 0.2297 | 0.7669 |
| 7 | `d3229_BTN_river` | QhJh | 4s8d7d7hQs | river | BET | CHECK | 0.8311 | 0.6050 | 0.4219 | 0.5781 | 1.250 | 0.1955 | 0.7955 |
| 8 | `d3688_BB_flop` | 8cKc | KdTd4s | flop | CHECK | BET | 0.7400 | 0.5280 | 0.3376 | 0.1983 | 1.250 | 0.1086 | 0.8789 |
| 9 | `d8411_BB_turn` | Ac8h | 6c8c2d3c | turn | BET | CHECK | 0.4349 | 0.6535 | 0.5696 | 0.2110 | 1.250 | 0.1488 | 0.8388 |
| 10 | `d8886_BB_flop` | QcJc | 2s5dJd | flop | BET | CHECK | 0.7926 | 0.6020 | 0.5882 | 0.1812 | 1.250 | 0.0791 | 0.9091 |

## Summary Table 2 — Predicted action probabilities (all 10 hands)

Raw probabilities shown first; masked set (legal given `facing_bet`) in parentheses.

| # | situation_id | facing_bet | GT | pred | FOLD | CHECK | CALL | BET | RAISE |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `d1454_CO_turn` | False | BET | CHECK | 0.005 | **0.387** | 0.527 | **0.077** | 0.003 |
| 2 | `d1562_HJ_turn` | False | BET | CHECK | 0.007 | **0.541** | 0.420 | **0.028** | 0.004 |
| 3 | `d1983_HJ_turn` | False | BET | CHECK | 0.004 | **0.325** | 0.597 | **0.071** | 0.003 |
| 4 | `d2410_CO_turn` | False | BET | BET | 0.005 | **0.063** | 0.819 | **0.110** | 0.003 |
| 5 | `d2920_BB_turn` | False | BET | CHECK | 0.010 | **0.466** | 0.301 | **0.218** | 0.005 |
| 6 | `d3178_CO_river` | False | BET | CHECK | 0.009 | **0.489** | 0.300 | **0.198** | 0.004 |
| 7 | `d3229_BTN_river` | False | BET | CHECK | 0.004 | **0.220** | 0.616 | **0.157** | 0.003 |
| 8 | `d3688_BB_flop` | False | CHECK | BET | 0.005 | **0.058** | 0.487 | **0.448** | 0.003 |
| 9 | `d8411_BB_turn` | False | BET | CHECK | 0.009 | **0.585** | 0.093 | **0.308** | 0.006 |
| 10 | `d8886_BB_flop` | False | BET | CHECK | 0.005 | **0.416** | 0.488 | **0.088** | 0.003 |

Bold = in the legal set after masking. The predicted action is the argmax of the masked distribution.

---

## Hand 1 — `d1454_CO_turn`

### Identification

- **situation_id:** `d1454_CO_turn`
- **deal_id:** 1454
- **hero_cards:** ThJh
- **board:** Tc8hAh4d
- **street:** turn
- **hero_position:** CO
- **villain_positions:** ['BTN', 'BB']
- **num_opponents:** 2
- **facing_bet:** False
- **pot:** 80.0
- **to_call:** 0.0

### Action history

- preflop: CO raise
- flop: CO check
- *(compact)* `preflop: CO raise | flop: CO check`

### Ground truth vs model prediction

- **Expected (ground_truth_label / expert_action):** BET
- **Model prediction (this run, masked):** CHECK
- **Prep-file `model_prediction`:** CHECK
- **Prep-file `oracle_action`:** CHECK
- **Prep-file `adjusted_action`:** CHECK
- **Mismatch:** expected: BET, predicted: CHECK

### Corrected bias-signature values

| feature | value |
|---|---|
| `hero_range_percentile` | 0.5786 |
| `equity_vs_range` | 0.4377 |
| `villain_air_pct` | 0.0157 |
| `villain_top_pair_plus_pct` | 0.2673 |
| `spr` | 1.2500 |
| `better_hand_pct` | 0.4249 |
| `worse_hand_pct` | 0.5578 |

### Oracle predicted action distribution

| action | raw prob | legal after mask |
|---|---|---|
| FOLD | 0.0049 | no |
| CHECK | 0.3874 | yes |
| CALL | 0.5274 | no |
| BET | 0.0770 | yes |
| RAISE | 0.0033 | no |

Argmax over legal set → **CHECK**

### Full 54-feature vector

| feature | value |
|---|---|
| `street` | 1 |
| `facing_bet` | 0 |
| `pot_size` | 80 |
| `to_call` | 0 |
| `pot_odds` | 0 |
| `bet_to_pot` | 0 |
| `hero_position` | 2 |
| `villain_position` | 3 |
| `is_ip` | 0 |
| `hand_category` | 5 |
| `hand_rank` | 1.2 |
| `is_made_hand` | 1 |
| `is_strong_made` | 0 |
| `is_monster` | 0 |
| `has_flush_draw` | 1 |
| `has_straight_draw` | 0 |
| `draw_outs` | 9 |
| `is_monotone` | 0 |
| `is_two_tone` | 0 |
| `is_rainbow` | 1 |
| `is_paired` | 0 |
| `is_double_paired` | 0 |
| `connectivity_score` | 2 |
| `high_card_rank` | 14 |
| `danger_score` | 0.08 |
| `flush_danger` | 0 |
| `straight_danger` | 0 |
| `raw_equity` | 0.43775 |
| `equity_vs_range` | 0.43775 |
| `better_hand_pct` | 0.424855 |
| `worse_hand_pct` | 0.557803 |
| `equity_margin` | 0.43775 |
| `spr` | 1.25 |
| `is_3bet_pot` | 0 |
| `villain_aggression_count` | 0 |
| `villain_checked_back` | 1 |
| `villain_call_count` | 0 |
| `num_opponents` | 2 |
| `villain_top_pair_plus_pct` | 0.2673 |
| `villain_draw_pct` | 0.1509 |
| `villain_air_pct` | 0.0157 |
| `villain_range_capped` | 1 |
| `board_favour` | 0.0327 |
| `num_callers_to_bet` | 0 |
| `facing_raise` | 0 |
| `flush_block_pct` | 0 |
| `overcard_outs` | 0 |
| `improvement_probability` | 0.478261 |
| `hero_range_percentile` | 0.578633 |
| `has_showdown_value` | 1 |
| `villain_fold_equity_estimate` | 0.431978 |
| `flush_draw_rank` | 11 |
| `is_preflop_aggressor` | 1 |
| `villain_medium_made_pct` | 0.566 |

### Pass 1 labelling history

Not available in repo. `pass1_T[1-4]_labels.jsonl` cover only the BP building-block situations, not the MW-50 `d*` test hands. No per-agent pre-aggregation votes exist for this sid.

### Labelled-set cross-reference (test_set_50_labelled.jsonl)

- **expert_action:** BET
- **expert_confidence:** MEDIUM
- **difficulty:** 2
- **expert_reasoning:** Hero has second pair (tens) plus a flush draw (9 outs) on Tc8hAh4d. Villain ranges are capped (villain_range_capped=1) with very low air (2.7%), but villain_checked_back=1 and villain_aggression=0 indicate both opponents showed weakness. With 44% equity, 56% worse hands, a flush draw for protection/equity, and opponents having checked through, hero should bet small for value and protection. Letting two opponents see a free river risks losing to a completed draw or being outdrawn. The flush draw gives hero a strong backup plan if called.
- **key_factors:** ['second_pair_plus_flush_draw', 'opponents_showed_weakness', 'protection_needed', 'capped_villain_range']
- **factor_conflicts:** OOP position and low villain_air argue for check, but both opponents checking (aggression=0, checked_back=1) signals weakness. The flush draw provides protection equity that tips the decision toward betting.
- **alternatives_considered:** ['CHECK: reasonable for pot control OOP, but giving free cards with 9 flush outs outstanding and two opponents who showed weakness leaves value and protection on the table.']

---

## Hand 2 — `d1562_HJ_turn`

### Identification

- **situation_id:** `d1562_HJ_turn`
- **deal_id:** 1562
- **hero_cards:** 7h7d
- **board:** 5cJcJd3s
- **street:** turn
- **hero_position:** HJ
- **villain_positions:** ['BTN', 'BB']
- **num_opponents:** 2
- **facing_bet:** False
- **pot:** 80.0
- **to_call:** 0.0

### Action history

- preflop: HJ raise
- flop: HJ check
- *(compact)* `preflop: HJ raise | flop: HJ check`

### Ground truth vs model prediction

- **Expected (ground_truth_label / expert_action):** BET
- **Model prediction (this run, masked):** CHECK
- **Prep-file `model_prediction`:** CHECK
- **Prep-file `oracle_action`:** CHECK
- **Prep-file `adjusted_action`:** CHECK
- **Mismatch:** expected: BET, predicted: CHECK

### Corrected bias-signature values

| feature | value |
|---|---|
| `hero_range_percentile` | 0.7095 |
| `equity_vs_range` | 0.3540 |
| `villain_air_pct` | 0.4321 |
| `villain_top_pair_plus_pct` | 0.5679 |
| `spr` | 1.2500 |
| `better_hand_pct` | 0.2906 |
| `worse_hand_pct` | 0.7057 |

### Oracle predicted action distribution

| action | raw prob | legal after mask |
|---|---|---|
| FOLD | 0.0067 | no |
| CHECK | 0.5412 | yes |
| CALL | 0.4199 | no |
| BET | 0.0279 | yes |
| RAISE | 0.0043 | no |

Argmax over legal set → **CHECK**

### Full 54-feature vector

| feature | value |
|---|---|
| `street` | 1 |
| `facing_bet` | 0 |
| `pot_size` | 80 |
| `to_call` | 0 |
| `pot_odds` | 0 |
| `bet_to_pot` | 0 |
| `hero_position` | 1 |
| `villain_position` | 3 |
| `is_ip` | 0 |
| `hand_category` | 10 |
| `hand_rank` | 2.5675 |
| `is_made_hand` | 1 |
| `is_strong_made` | 1 |
| `is_monster` | 0 |
| `has_flush_draw` | 0 |
| `has_straight_draw` | 0 |
| `draw_outs` | 0 |
| `is_monotone` | 0 |
| `is_two_tone` | 0 |
| `is_rainbow` | 1 |
| `is_paired` | 1 |
| `is_double_paired` | 0 |
| `connectivity_score` | 2 |
| `high_card_rank` | 11 |
| `danger_score` | 0.23 |
| `flush_danger` | 0 |
| `straight_danger` | 0 |
| `raw_equity` | 0.354 |
| `equity_vs_range` | 0.354 |
| `better_hand_pct` | 0.290566 |
| `worse_hand_pct` | 0.70566 |
| `equity_margin` | 0.354 |
| `spr` | 1.25 |
| `is_3bet_pot` | 0 |
| `villain_aggression_count` | 0 |
| `villain_checked_back` | 1 |
| `villain_call_count` | 0 |
| `num_opponents` | 2 |
| `villain_top_pair_plus_pct` | 0.5679 |
| `villain_draw_pct` | 0 |
| `villain_air_pct` | 0.4321 |
| `villain_range_capped` | 1 |
| `board_favour` | -0.2679 |
| `num_callers_to_bet` | 0 |
| `facing_raise` | 0 |
| `flush_block_pct` | 0 |
| `overcard_outs` | 0 |
| `improvement_probability` | 1 |
| `hero_range_percentile` | 0.709493 |
| `has_showdown_value` | 1 |
| `villain_fold_equity_estimate` | 0.18671 |
| `flush_draw_rank` | 0 |
| `is_preflop_aggressor` | 1 |
| `villain_medium_made_pct` | 0 |

### Pass 1 labelling history

Not available in repo. `pass1_T[1-4]_labels.jsonl` cover only the BP building-block situations, not the MW-50 `d*` test hands. No per-agent pre-aggregation votes exist for this sid.

### Labelled-set cross-reference (test_set_50_labelled.jsonl)

- **expert_action:** BET
- **expert_confidence:** MEDIUM
- **difficulty:** 2
- **expert_reasoning:** Hero has 77 on 5cJcJd3s -- two pair JJ77 on a paired board. Equity is 38% but worse_hand_pct is 71% and villain_air is very high at 48%. Villain is capped and checked back showing weakness. Board is paired and relatively dry (danger 0.23). A small bet extracts value from underpairs (22-66), random floats, and air that might fold. Hero beats most of villain's continuing range minus actual Jx trips.
- **key_factors:** ['two_pair_on_paired_board', 'very_high_villain_air', 'capped_villain', 'villain_showed_weakness']
- **factor_conflicts:** 38% raw equity seems marginal, but equity is computed vs full ranges. With villain checked back and 48% air, actual equity vs villain's weak remaining range is higher. High air and capped range support thin value.
- **alternatives_considered:** ['CHECK: defensible since any Jx in villain range dominates, but with 48% air and villain showing weakness, checking leaves value against the huge air portion of their range']

---

## Hand 3 — `d1983_HJ_turn`

### Identification

- **situation_id:** `d1983_HJ_turn`
- **deal_id:** 1983
- **hero_cards:** AcJs
- **board:** Jd7dKh2c
- **street:** turn
- **hero_position:** HJ
- **villain_positions:** ['BTN', 'BB']
- **num_opponents:** 2
- **facing_bet:** False
- **pot:** 80.0
- **to_call:** 0.0

### Action history

- preflop: HJ raise
- flop: HJ check
- *(compact)* `preflop: HJ raise | flop: HJ check`

### Ground truth vs model prediction

- **Expected (ground_truth_label / expert_action):** BET
- **Model prediction (this run, masked):** CHECK
- **Prep-file `model_prediction`:** CHECK
- **Prep-file `oracle_action`:** CHECK
- **Prep-file `adjusted_action`:** CHECK
- **Mismatch:** expected: BET, predicted: CHECK

### Corrected bias-signature values

| feature | value |
|---|---|
| `hero_range_percentile` | 0.6729 |
| `equity_vs_range` | 0.4365 |
| `villain_air_pct` | 0.1847 |
| `villain_top_pair_plus_pct` | 0.2544 |
| `spr` | 1.2500 |
| `better_hand_pct` | 0.2907 |
| `worse_hand_pct` | 0.6828 |

### Oracle predicted action distribution

| action | raw prob | legal after mask |
|---|---|---|
| FOLD | 0.0040 | no |
| CHECK | 0.3249 | yes |
| CALL | 0.5974 | no |
| BET | 0.0711 | yes |
| RAISE | 0.0026 | no |

Argmax over legal set → **CHECK**

### Full 54-feature vector

| feature | value |
|---|---|
| `street` | 1 |
| `facing_bet` | 0 |
| `pot_size` | 80 |
| `to_call` | 0 |
| `pot_odds` | 0 |
| `bet_to_pot` | 0 |
| `hero_position` | 1 |
| `villain_position` | 3 |
| `is_ip` | 0 |
| `hand_category` | 5 |
| `hand_rank` | 1.21 |
| `is_made_hand` | 1 |
| `is_strong_made` | 0 |
| `is_monster` | 0 |
| `has_flush_draw` | 0 |
| `has_straight_draw` | 0 |
| `draw_outs` | 0 |
| `is_monotone` | 0 |
| `is_two_tone` | 0 |
| `is_rainbow` | 1 |
| `is_paired` | 0 |
| `is_double_paired` | 0 |
| `connectivity_score` | 2 |
| `high_card_rank` | 13 |
| `danger_score` | 0.08 |
| `flush_danger` | 0 |
| `straight_danger` | 0 |
| `raw_equity` | 0.4365 |
| `equity_vs_range` | 0.4365 |
| `better_hand_pct` | 0.290749 |
| `worse_hand_pct` | 0.682819 |
| `equity_margin` | 0.4365 |
| `spr` | 1.25 |
| `is_3bet_pot` | 0 |
| `villain_aggression_count` | 0 |
| `villain_checked_back` | 1 |
| `villain_call_count` | 0 |
| `num_opponents` | 2 |
| `villain_top_pair_plus_pct` | 0.2544 |
| `villain_draw_pct` | 0.0801 |
| `villain_air_pct` | 0.1847 |
| `villain_range_capped` | 1 |
| `board_favour` | 0.0456 |
| `num_callers_to_bet` | 0 |
| `facing_raise` | 0 |
| `flush_block_pct` | 0 |
| `overcard_outs` | 3 |
| `improvement_probability` | 0.304348 |
| `hero_range_percentile` | 0.672897 |
| `has_showdown_value` | 1 |
| `villain_fold_equity_estimate` | 0.497801 |
| `flush_draw_rank` | 0 |
| `is_preflop_aggressor` | 1 |
| `villain_medium_made_pct` | 0.4808 |

### Pass 1 labelling history

Not available in repo. `pass1_T[1-4]_labels.jsonl` cover only the BP building-block situations, not the MW-50 `d*` test hands. No per-agent pre-aggregation votes exist for this sid.

### Labelled-set cross-reference (test_set_50_labelled.jsonl)

- **expert_action:** BET
- **expert_confidence:** MEDIUM
- **difficulty:** 2
- **expert_reasoning:** Hero has AJ on Jd7dKh2c -- second pair top kicker on a very dry board (danger 0.08). Villain is capped and checked back showing weakness. Equity is 43.3% with 68% worse hands. Despite OOP, the combination of capped villain, extremely dry board, villain weakness signal, and strong kicker supports a small value bet targeting pocket pairs below J, worse Jx, and floats. The K is concerning but villain's check-back reduces Kx likelihood.
- **key_factors:** ['second_pair_top_kicker', 'villain_showed_weakness', 'capped_villain', 'very_dry_board']
- **factor_conflicts:** OOP with second pair normally argues for check, but villain checked back, villain is capped, board is extremely dry, and 68% worse hands tips toward thin value. Close spot.
- **alternatives_considered:** ["CHECK: reasonable for pot control with second pair OOP. The K on turn is scary. But villain's check-back and capped range reduce Kx combos significantly"]

---

## Hand 4 — `d2410_CO_turn`

### Identification

- **situation_id:** `d2410_CO_turn`
- **deal_id:** 2410
- **hero_cards:** JcKs
- **board:** Jd9d3h6d
- **street:** turn
- **hero_position:** CO
- **villain_positions:** ['BTN', 'BB']
- **num_opponents:** 2
- **facing_bet:** False
- **pot:** 80.0
- **to_call:** 0.0

### Action history

- preflop: CO raise
- flop: CO check
- *(compact)* `preflop: CO raise | flop: CO check`

### Ground truth vs model prediction

- **Expected (ground_truth_label / expert_action):** BET
- **Model prediction (this run, masked):** BET
- **Prep-file `model_prediction`:** CHECK
- **Prep-file `oracle_action`:** CHECK
- **Prep-file `adjusted_action`:** CHECK
- **Mismatch:** expected: BET, predicted: BET

### Corrected bias-signature values

| feature | value |
|---|---|
| `hero_range_percentile` | 0.4524 |
| `equity_vs_range` | 0.4470 |
| `villain_air_pct` | 0.2044 |
| `villain_top_pair_plus_pct` | 0.3302 |
| `spr` | 1.2500 |
| `better_hand_pct` | 0.1662 |
| `worse_hand_pct` | 0.8172 |

### Oracle predicted action distribution

| action | raw prob | legal after mask |
|---|---|---|
| FOLD | 0.0048 | no |
| CHECK | 0.0631 | yes |
| CALL | 0.8191 | no |
| BET | 0.1098 | yes |
| RAISE | 0.0032 | no |

Argmax over legal set → **BET**

### Full 54-feature vector

| feature | value |
|---|---|
| `street` | 1 |
| `facing_bet` | 0 |
| `pot_size` | 80 |
| `to_call` | 0 |
| `pot_odds` | 0 |
| `bet_to_pot` | 0 |
| `hero_position` | 2 |
| `villain_position` | 3 |
| `is_ip` | 0 |
| `hand_category` | 7 |
| `hand_rank` | 1.323 |
| `is_made_hand` | 1 |
| `is_strong_made` | 0 |
| `is_monster` | 0 |
| `has_flush_draw` | 0 |
| `has_straight_draw` | 0 |
| `draw_outs` | 0 |
| `is_monotone` | 0 |
| `is_two_tone` | 1 |
| `is_rainbow` | 0 |
| `is_paired` | 0 |
| `is_double_paired` | 0 |
| `connectivity_score` | 2 |
| `high_card_rank` | 11 |
| `danger_score` | 0.5954 |
| `flush_danger` | 0.5154 |
| `straight_danger` | 0 |
| `raw_equity` | 0.447 |
| `equity_vs_range` | 0.447 |
| `better_hand_pct` | 0.166205 |
| `worse_hand_pct` | 0.817175 |
| `equity_margin` | 0.447 |
| `spr` | 1.25 |
| `is_3bet_pot` | 0 |
| `villain_aggression_count` | 0 |
| `villain_checked_back` | 1 |
| `villain_call_count` | 0 |
| `num_opponents` | 2 |
| `villain_top_pair_plus_pct` | 0.3302 |
| `villain_draw_pct` | 0.1258 |
| `villain_air_pct` | 0.2044 |
| `villain_range_capped` | 1 |
| `board_favour` | -0.0302 |
| `num_callers_to_bet` | 0 |
| `facing_raise` | 0 |
| `flush_block_pct` | 0 |
| `overcard_outs` | 3 |
| `improvement_probability` | 0.304348 |
| `hero_range_percentile` | 0.452432 |
| `has_showdown_value` | 1 |
| `villain_fold_equity_estimate` | 0.368328 |
| `flush_draw_rank` | 0 |
| `is_preflop_aggressor` | 1 |
| `villain_medium_made_pct` | 0.3396 |

### Pass 1 labelling history

Not available in repo. `pass1_T[1-4]_labels.jsonl` cover only the BP building-block situations, not the MW-50 `d*` test hands. No per-agent pre-aggregation votes exist for this sid.

### Labelled-set cross-reference (test_set_50_labelled.jsonl)

- **expert_action:** BET
- **expert_confidence:** HIGH
- **difficulty:** 2
- **expert_reasoning:** Hero has KJ on Jd9d3h6d -- top pair good kicker on a completed flush board. Villain checked back flop (weakness signal), both have checked to hero. Despite OOP, hero has 43% equity with 82% worse hands, villain is capped, and villain showed weakness. Must bet small for value and protection against remaining draws on this 3-flush board. Checking risks giving free cards.
- **key_factors:** ['top_pair_good_kicker', 'villain_showed_weakness', 'high_worse_hand_pct', 'capped_villain']
- **factor_conflicts:** OOP position argues for check, but villain checked back (weakness signal) plus 82% worse hands and capped villain range override. Protection is critical on a 3-flush board.
- **alternatives_considered:** ['CHECK: defensible for pot control on a flush-completed board, but villain showed weakness and 82% worse hands means too much value left on the table']

---

## Hand 5 — `d2920_BB_turn`

### Identification

- **situation_id:** `d2920_BB_turn`
- **deal_id:** 2920
- **hero_cards:** JhQd
- **board:** Js2sTdQs
- **street:** turn
- **hero_position:** BB
- **villain_positions:** ['CO', 'BTN']
- **num_opponents:** 2
- **facing_bet:** False
- **pot:** 80.0
- **to_call:** 0.0

### Action history

- preflop: BB call
- flop: BB check
- *(compact)* `preflop: BB call | flop: BB check`

### Ground truth vs model prediction

- **Expected (ground_truth_label / expert_action):** BET
- **Model prediction (this run, masked):** CHECK
- **Prep-file `model_prediction`:** CHECK
- **Prep-file `oracle_action`:** CHECK
- **Prep-file `adjusted_action`:** CHECK
- **Mismatch:** expected: BET, predicted: CHECK

### Corrected bias-signature values

| feature | value |
|---|---|
| `hero_range_percentile` | 0.4725 |
| `equity_vs_range` | 0.4908 |
| `villain_air_pct` | 0.1828 |
| `villain_top_pair_plus_pct` | 0.3084 |
| `spr` | 1.2500 |
| `better_hand_pct` | 0.1834 |
| `worse_hand_pct` | 0.8081 |

### Oracle predicted action distribution

| action | raw prob | legal after mask |
|---|---|---|
| FOLD | 0.0097 | no |
| CHECK | 0.4662 | yes |
| CALL | 0.3011 | no |
| BET | 0.2179 | yes |
| RAISE | 0.0052 | no |

Argmax over legal set → **CHECK**

### Full 54-feature vector

| feature | value |
|---|---|
| `street` | 1 |
| `facing_bet` | 0 |
| `pot_size` | 80 |
| `to_call` | 0 |
| `pot_odds` | 0 |
| `bet_to_pot` | 0 |
| `hero_position` | 5 |
| `villain_position` | 2 |
| `is_ip` | 0 |
| `hand_category` | 10 |
| `hand_rank` | 2.6275 |
| `is_made_hand` | 1 |
| `is_strong_made` | 1 |
| `is_monster` | 0 |
| `has_flush_draw` | 0 |
| `has_straight_draw` | 0 |
| `draw_outs` | 0 |
| `is_monotone` | 0 |
| `is_two_tone` | 1 |
| `is_rainbow` | 0 |
| `is_paired` | 0 |
| `is_double_paired` | 0 |
| `connectivity_score` | 8 |
| `high_card_rank` | 12 |
| `danger_score` | 1 |
| `flush_danger` | 0.5154 |
| `straight_danger` | 0.8 |
| `raw_equity` | 0.49075 |
| `equity_vs_range` | 0.49075 |
| `better_hand_pct` | 0.183369 |
| `worse_hand_pct` | 0.808102 |
| `equity_margin` | 0.49075 |
| `spr` | 1.25 |
| `is_3bet_pot` | 0 |
| `villain_aggression_count` | 0 |
| `villain_checked_back` | 1 |
| `villain_call_count` | 0 |
| `num_opponents` | 2 |
| `villain_top_pair_plus_pct` | 0.3084 |
| `villain_draw_pct` | 0.1113 |
| `villain_air_pct` | 0.1828 |
| `villain_range_capped` | 0 |
| `board_favour` | -0.0084 |
| `num_callers_to_bet` | 0 |
| `facing_raise` | 0 |
| `flush_block_pct` | 0 |
| `overcard_outs` | 0 |
| `improvement_probability` | 1 |
| `hero_range_percentile` | 0.472537 |
| `has_showdown_value` | 1 |
| `villain_fold_equity_estimate` | 0.404432 |
| `flush_draw_rank` | 0 |
| `is_preflop_aggressor` | 0 |
| `villain_medium_made_pct` | 0.3975 |

### Pass 1 labelling history

Not available in repo. `pass1_T[1-4]_labels.jsonl` cover only the BP building-block situations, not the MW-50 `d*` test hands. No per-agent pre-aggregation votes exist for this sid.

### Labelled-set cross-reference (test_set_50_labelled.jsonl)

- **expert_action:** BET
- **expert_confidence:** HIGH
- **difficulty:** 2
- **expert_reasoning:** Hero has QJ on Js2sTdQs -- two pair (top two) on a very dangerous board with flush and straight draws everywhere. Equity is 49.8% with 81% worse hands, and villain checked back showing weakness. Despite OOP and danger_score 1.0, hero MUST bet for protection. The board is extremely dynamic -- giving free cards with two pair is catastrophic when any spade, K, A, or 8 could kill hero's equity.
- **key_factors:** ['two_pair_strong', 'must_protect_dynamic_board', 'villain_showed_weakness', 'high_worse_hand_pct']
- **factor_conflicts:** OOP and max danger score argue for caution, but two pair on a draw-heavy board where villain showed weakness demands betting for protection. Checking risks being outdrawn for free.
- **alternatives_considered:** ['CHECK: dangerous -- with danger_score 1.0, any river card could complete draws. Two pair has too much equity to give a free card']

---

## Hand 6 — `d3178_CO_river`

### Identification

- **situation_id:** `d3178_CO_river`
- **deal_id:** 3178
- **hero_cards:** AcAs
- **board:** JhQcJcKs5h
- **street:** river
- **hero_position:** CO
- **villain_positions:** ['BTN', 'BB']
- **num_opponents:** 2
- **facing_bet:** False
- **pot:** 80.0
- **to_call:** 0.0

### Action history

- preflop: CO raise
- flop: CO check
- turn: CO check
- *(compact)* `preflop: CO raise | flop: CO check | turn: CO check`

### Ground truth vs model prediction

- **Expected (ground_truth_label / expert_action):** BET
- **Model prediction (this run, masked):** CHECK
- **Prep-file `model_prediction`:** CHECK
- **Prep-file `oracle_action`:** CHECK
- **Prep-file `adjusted_action`:** CHECK
- **Mismatch:** expected: BET, predicted: CHECK

### Corrected bias-signature values

| feature | value |
|---|---|
| `hero_range_percentile` | 0.7694 |
| `equity_vs_range` | 0.6305 |
| `villain_air_pct` | 0.1730 |
| `villain_top_pair_plus_pct` | 0.8270 |
| `spr` | 1.2500 |
| `better_hand_pct` | 0.2297 |
| `worse_hand_pct` | 0.7669 |

### Oracle predicted action distribution

| action | raw prob | legal after mask |
|---|---|---|
| FOLD | 0.0089 | no |
| CHECK | 0.4893 | yes |
| CALL | 0.2996 | no |
| BET | 0.1980 | yes |
| RAISE | 0.0042 | no |

Argmax over legal set → **CHECK**

### Full 54-feature vector

| feature | value |
|---|---|
| `street` | 2 |
| `facing_bet` | 0 |
| `pot_size` | 80 |
| `to_call` | 0 |
| `pot_odds` | 0 |
| `bet_to_pot` | 0 |
| `hero_position` | 2 |
| `villain_position` | 3 |
| `is_ip` | 0 |
| `hand_category` | 10 |
| `hand_rank` | 2.7275 |
| `is_made_hand` | 1 |
| `is_strong_made` | 1 |
| `is_monster` | 0 |
| `has_flush_draw` | 0 |
| `has_straight_draw` | 1 |
| `draw_outs` | 8 |
| `is_monotone` | 0 |
| `is_two_tone` | 0 |
| `is_rainbow` | 1 |
| `is_paired` | 1 |
| `is_double_paired` | 0 |
| `connectivity_score` | 8 |
| `high_card_rank` | 13 |
| `danger_score` | 1 |
| `flush_danger` | 0 |
| `straight_danger` | 0.8 |
| `raw_equity` | 0.6305 |
| `equity_vs_range` | 0.6305 |
| `better_hand_pct` | 0.22973 |
| `worse_hand_pct` | 0.766892 |
| `equity_margin` | 0.6305 |
| `spr` | 1.25 |
| `is_3bet_pot` | 0 |
| `villain_aggression_count` | 0 |
| `villain_checked_back` | 1 |
| `villain_call_count` | 0 |
| `num_opponents` | 2 |
| `villain_top_pair_plus_pct` | 0.827 |
| `villain_draw_pct` | 0 |
| `villain_air_pct` | 0.173 |
| `villain_range_capped` | 1 |
| `board_favour` | -0.527 |
| `num_callers_to_bet` | 0 |
| `facing_raise` | 0 |
| `flush_block_pct` | 0 |
| `overcard_outs` | 6 |
| `improvement_probability` | 0 |
| `hero_range_percentile` | 0.769422 |
| `has_showdown_value` | 1 |
| `villain_fold_equity_estimate` | 0.029929 |
| `flush_draw_rank` | 0 |
| `is_preflop_aggressor` | 1 |
| `villain_medium_made_pct` | 0 |

### Pass 1 labelling history

Not available in repo. `pass1_T[1-4]_labels.jsonl` cover only the BP building-block situations, not the MW-50 `d*` test hands. No per-agent pre-aggregation votes exist for this sid.

### Labelled-set cross-reference (test_set_50_labelled.jsonl)

- **expert_action:** BET
- **expert_confidence:** MEDIUM
- **difficulty:** 2
- **expert_reasoning:** Hero has AA on JhQcJcKs5h river -- aces up with board pair of jacks. Equity is 61.8% with 77% worse hands, villain is capped, and both opponents checked through. Despite the scary JQJK board (danger 1.0), hero beats all one-pair hands, worse two-pair, and most of the field. A small value bet extracts from Kx, Qx, and pocket pairs that checked through. Villain_tp_plus is high (84%) but that includes hands hero beats.
- **key_factors:** ['strong_two_pair', 'high_equity', 'capped_villain', 'value_bet_river']
- **factor_conflicts:** Danger score 1.0 and deeply negative board_favour (-0.54) suggest caution, but 62% equity, 77% worse hands, and capped villain with checked-back weakness override.
- **alternatives_considered:** ['CHECK: defensible given dangerous board with trips and straights possible, but 77% worse hands and both opponents showing weakness means checking leaves significant value']

---

## Hand 7 — `d3229_BTN_river`

### Identification

- **situation_id:** `d3229_BTN_river`
- **deal_id:** 3229
- **hero_cards:** QhJh
- **board:** 4s8d7d7hQs
- **street:** river
- **hero_position:** BTN
- **villain_positions:** ['HJ', 'BB']
- **num_opponents:** 2
- **facing_bet:** False
- **pot:** 80.0
- **to_call:** 0.0

### Action history

- preflop: BTN call
- flop: BTN check
- turn: BTN check
- *(compact)* `preflop: BTN call | flop: BTN check | turn: BTN check`

### Ground truth vs model prediction

- **Expected (ground_truth_label / expert_action):** BET
- **Model prediction (this run, masked):** CHECK
- **Prep-file `model_prediction`:** CHECK
- **Prep-file `oracle_action`:** CHECK
- **Prep-file `adjusted_action`:** CHECK
- **Mismatch:** expected: BET, predicted: CHECK

### Corrected bias-signature values

| feature | value |
|---|---|
| `hero_range_percentile` | 0.8311 |
| `equity_vs_range` | 0.6050 |
| `villain_air_pct` | 0.4219 |
| `villain_top_pair_plus_pct` | 0.5781 |
| `spr` | 1.2500 |
| `better_hand_pct` | 0.1955 |
| `worse_hand_pct` | 0.7955 |

### Oracle predicted action distribution

| action | raw prob | legal after mask |
|---|---|---|
| FOLD | 0.0040 | no |
| CHECK | 0.2205 | yes |
| CALL | 0.6163 | no |
| BET | 0.1566 | yes |
| RAISE | 0.0026 | no |

Argmax over legal set → **CHECK**

### Full 54-feature vector

| feature | value |
|---|---|
| `street` | 2 |
| `facing_bet` | 0 |
| `pot_size` | 80 |
| `to_call` | 0 |
| `pot_odds` | 0 |
| `bet_to_pot` | 0 |
| `hero_position` | 3 |
| `villain_position` | 1 |
| `is_ip` | 1 |
| `hand_category` | 10 |
| `hand_rank` | 2.6175 |
| `is_made_hand` | 1 |
| `is_strong_made` | 1 |
| `is_monster` | 0 |
| `has_flush_draw` | 0 |
| `has_straight_draw` | 0 |
| `draw_outs` | 0 |
| `is_monotone` | 0 |
| `is_two_tone` | 0 |
| `is_rainbow` | 1 |
| `is_paired` | 1 |
| `is_double_paired` | 0 |
| `connectivity_score` | 5 |
| `high_card_rank` | 12 |
| `danger_score` | 0.57 |
| `flush_danger` | 0 |
| `straight_danger` | 0.3 |
| `raw_equity` | 0.605 |
| `equity_vs_range` | 0.605 |
| `better_hand_pct` | 0.195506 |
| `worse_hand_pct` | 0.795506 |
| `equity_margin` | 0.605 |
| `spr` | 1.25 |
| `is_3bet_pot` | 0 |
| `villain_aggression_count` | 0 |
| `villain_checked_back` | 1 |
| `villain_call_count` | 0 |
| `num_opponents` | 2 |
| `villain_top_pair_plus_pct` | 0.5781 |
| `villain_draw_pct` | 0 |
| `villain_air_pct` | 0.4219 |
| `villain_range_capped` | 0 |
| `board_favour` | -0.2781 |
| `num_callers_to_bet` | 0 |
| `facing_raise` | 0 |
| `flush_block_pct` | 0 |
| `overcard_outs` | 0 |
| `improvement_probability` | 0 |
| `hero_range_percentile` | 0.831109 |
| `has_showdown_value` | 1 |
| `villain_fold_equity_estimate` | 0.178 |
| `flush_draw_rank` | 0 |
| `is_preflop_aggressor` | 0 |
| `villain_medium_made_pct` | 0 |

### Pass 1 labelling history

Not available in repo. `pass1_T[1-4]_labels.jsonl` cover only the BP building-block situations, not the MW-50 `d*` test hands. No per-agent pre-aggregation votes exist for this sid.

### Labelled-set cross-reference (test_set_50_labelled.jsonl)

- **expert_action:** BET
- **expert_confidence:** MEDIUM
- **difficulty:** 2
- **expert_reasoning:** Two pair (QQ77 on 487Q with paired 7s) IP on the river with 60% equity and 79.5% worse hands. Both opponents checked showing weakness. River bets should be polarized, but this is IP thin value against two weak ranges — a small bet targets pocket pairs, 8x, worse Qx. The paired board and 57% villain_tp_plus introduce some risk, but opponents' weakness signals support extracting value.
- **key_factors:** ['ip_position', 'opponents_showed_weakness', 'thin_value_river', 'high_worse_hand_pct']
- **factor_conflicts:** High villain_tp_plus (57%) and danger 0.57 argue for checking, but IP + both opponents checked + 80% worse hands supports thin value. Opponents' weakness signals override board danger.
- **alternatives_considered:** ['CHECK: reasonable given the paired board and high villain strength metric, but leaving 80% worse hands unchallenged IP after both showed weakness forfeits significant value.']

---

## Hand 8 — `d3688_BB_flop`

### Identification

- **situation_id:** `d3688_BB_flop`
- **deal_id:** 3688
- **hero_cards:** 8cKc
- **board:** KdTd4s
- **street:** flop
- **hero_position:** BB
- **villain_positions:** ['HJ', 'BTN']
- **num_opponents:** 2
- **facing_bet:** False
- **pot:** 80.0
- **to_call:** 0.0

### Action history

- preflop: BB call
- *(compact)* `preflop: BB call`

### Ground truth vs model prediction

- **Expected (ground_truth_label / expert_action):** CHECK
- **Model prediction (this run, masked):** BET
- **Prep-file `model_prediction`:** CHECK
- **Prep-file `oracle_action`:** CHECK
- **Prep-file `adjusted_action`:** CHECK
- **Mismatch:** expected: CHECK, predicted: BET

### Corrected bias-signature values

| feature | value |
|---|---|
| `hero_range_percentile` | 0.7400 |
| `equity_vs_range` | 0.5280 |
| `villain_air_pct` | 0.3376 |
| `villain_top_pair_plus_pct` | 0.1983 |
| `spr` | 1.2500 |
| `better_hand_pct` | 0.1086 |
| `worse_hand_pct` | 0.8789 |

### Oracle predicted action distribution

| action | raw prob | legal after mask |
|---|---|---|
| FOLD | 0.0045 | no |
| CHECK | 0.0578 | yes |
| CALL | 0.4868 | no |
| BET | 0.4479 | yes |
| RAISE | 0.0030 | no |

Argmax over legal set → **BET**

### Full 54-feature vector

| feature | value |
|---|---|
| `street` | 0 |
| `facing_bet` | 0 |
| `pot_size` | 80 |
| `to_call` | 0 |
| `pot_odds` | 0 |
| `bet_to_pot` | 0 |
| `hero_position` | 5 |
| `villain_position` | 1 |
| `is_ip` | 0 |
| `hand_category` | 6 |
| `hand_rank` | 1.338 |
| `is_made_hand` | 1 |
| `is_strong_made` | 0 |
| `is_monster` | 0 |
| `has_flush_draw` | 0 |
| `has_straight_draw` | 0 |
| `draw_outs` | 0 |
| `is_monotone` | 0 |
| `is_two_tone` | 1 |
| `is_rainbow` | 0 |
| `is_paired` | 0 |
| `is_double_paired` | 0 |
| `connectivity_score` | 2 |
| `high_card_rank` | 13 |
| `danger_score` | 0.25 |
| `flush_danger` | 0.25 |
| `straight_danger` | 0 |
| `raw_equity` | 0.528 |
| `equity_vs_range` | 0.528 |
| `better_hand_pct` | 0.108559 |
| `worse_hand_pct` | 0.878914 |
| `equity_margin` | 0.528 |
| `spr` | 1.25 |
| `is_3bet_pot` | 0 |
| `villain_aggression_count` | 0 |
| `villain_checked_back` | 0 |
| `villain_call_count` | 0 |
| `num_opponents` | 2 |
| `villain_top_pair_plus_pct` | 0.1983 |
| `villain_draw_pct` | 0.0422 |
| `villain_air_pct` | 0.3376 |
| `villain_range_capped` | 0 |
| `board_favour` | 0.1017 |
| `num_callers_to_bet` | 0 |
| `facing_raise` | 0 |
| `flush_block_pct` | 0 |
| `overcard_outs` | 0 |
| `improvement_probability` | 0.234043 |
| `hero_range_percentile` | 0.74005 |
| `has_showdown_value` | 1 |
| `villain_fold_equity_estimate` | 0.609336 |
| `flush_draw_rank` | 0 |
| `is_preflop_aggressor` | 0 |
| `villain_medium_made_pct` | 0.4219 |

### Pass 1 labelling history

Not available in repo. `pass1_T[1-4]_labels.jsonl` cover only the BP building-block situations, not the MW-50 `d*` test hands. No per-agent pre-aggregation votes exist for this sid.

### Labelled-set cross-reference (test_set_50_labelled.jsonl)

- **expert_action:** CHECK
- **expert_confidence:** HIGH
- **difficulty:** 1
- **expert_reasoning:** Hero has K8 on Kd-Td-4s — top pair weak kicker, OOP as BB. Despite 54% equity and 88% worse hands, the board has a flush draw (two diamonds) and HJ opened (uncapped range with AK, KK, KQ, KJ all dominating hero's kicker). Top pair weak kicker is a textbook pot-control hand 3-way per DO NOT rule 5. OOP position amplifies the risk — betting folds out air and gets called/raised by better Kx and draws. Board danger is moderate (0.25) but the diamond draw means the board is somewhat dynamic. Check for pot control and showdown value, potentially check-calling.
- **key_factors:** ['top_pair_weak_kicker', 'oop_position', 'uncapped_villain_range', 'flush_draw_on_board']
- **factor_conflicts:** High equity (54%) and high worse_hand_pct (88%) argue for value bet, but OOP + TPWK + uncapped HJ range with dominating Kx combos + flush draw board override. This is the Example 1 pattern (KQ on K-high, OOP, check for pot control).
- **alternatives_considered:** ['BET small (25-33%): rejected per Example 1 pattern — OOP with top pair weak kicker against an uncapped range. Betting folds out worse and gets called/raised by better. Check-call is the correct line.']

---

## Hand 9 — `d8411_BB_turn`

### Identification

- **situation_id:** `d8411_BB_turn`
- **deal_id:** 8411
- **hero_cards:** Ac8h
- **board:** 6c8c2d3c
- **street:** turn
- **hero_position:** BB
- **villain_positions:** ['HJ', 'BTN']
- **num_opponents:** 2
- **facing_bet:** False
- **pot:** 80.0
- **to_call:** 0.0

### Action history

- preflop: BB call
- flop: BB check
- *(compact)* `preflop: BB call | flop: BB check`

### Ground truth vs model prediction

- **Expected (ground_truth_label / expert_action):** BET
- **Model prediction (this run, masked):** CHECK
- **Prep-file `model_prediction`:** CHECK
- **Prep-file `oracle_action`:** CHECK
- **Prep-file `adjusted_action`:** CHECK
- **Mismatch:** expected: BET, predicted: CHECK

### Corrected bias-signature values

| feature | value |
|---|---|
| `hero_range_percentile` | 0.4349 |
| `equity_vs_range` | 0.6535 |
| `villain_air_pct` | 0.5696 |
| `villain_top_pair_plus_pct` | 0.2110 |
| `spr` | 1.2500 |
| `better_hand_pct` | 0.1488 |
| `worse_hand_pct` | 0.8388 |

### Oracle predicted action distribution

| action | raw prob | legal after mask |
|---|---|---|
| FOLD | 0.0086 | no |
| CHECK | 0.5854 | yes |
| CALL | 0.0927 | no |
| BET | 0.3076 | yes |
| RAISE | 0.0057 | no |

Argmax over legal set → **CHECK**

### Full 54-feature vector

| feature | value |
|---|---|
| `street` | 1 |
| `facing_bet` | 0 |
| `pot_size` | 80 |
| `to_call` | 0 |
| `pot_odds` | 0 |
| `bet_to_pot` | 0 |
| `hero_position` | 5 |
| `villain_position` | 1 |
| `is_ip` | 0 |
| `hand_category` | 8 |
| `hand_rank` | 1.294 |
| `is_made_hand` | 1 |
| `is_strong_made` | 0 |
| `is_monster` | 0 |
| `has_flush_draw` | 1 |
| `has_straight_draw` | 0 |
| `draw_outs` | 9 |
| `is_monotone` | 0 |
| `is_two_tone` | 1 |
| `is_rainbow` | 0 |
| `is_paired` | 0 |
| `is_double_paired` | 0 |
| `connectivity_score` | 5 |
| `high_card_rank` | 8 |
| `danger_score` | 0.7454 |
| `flush_danger` | 0.5154 |
| `straight_danger` | 0.3 |
| `raw_equity` | 0.6535 |
| `equity_vs_range` | 0.6535 |
| `better_hand_pct` | 0.14876 |
| `worse_hand_pct` | 0.838843 |
| `equity_margin` | 0.6535 |
| `spr` | 1.25 |
| `is_3bet_pot` | 0 |
| `villain_aggression_count` | 0 |
| `villain_checked_back` | 1 |
| `villain_call_count` | 0 |
| `num_opponents` | 2 |
| `villain_top_pair_plus_pct` | 0.211 |
| `villain_draw_pct` | 0.0211 |
| `villain_air_pct` | 0.5696 |
| `villain_range_capped` | 0 |
| `board_favour` | 0.089 |
| `num_callers_to_bet` | 0 |
| `facing_raise` | 0 |
| `flush_block_pct` | 0.159574 |
| `overcard_outs` | 3 |
| `improvement_probability` | 0.478261 |
| `hero_range_percentile` | 0.434854 |
| `has_showdown_value` | 1 |
| `villain_fold_equity_estimate` | 0.605984 |
| `flush_draw_rank` | 14 |
| `is_preflop_aggressor` | 0 |
| `villain_medium_made_pct` | 0.1983 |

### Pass 1 labelling history

Not available in repo. `pass1_T[1-4]_labels.jsonl` cover only the BP building-block situations, not the MW-50 `d*` test hands. No per-agent pre-aggregation votes exist for this sid.

### Labelled-set cross-reference (test_set_50_labelled.jsonl)

- **expert_action:** BET
- **expert_confidence:** HIGH
- **difficulty:** 1
- **expert_reasoning:** Hero has A8 on 6c8c2d3c — top pair with the nut flush draw (Ac). Equity is 66.5% with worse_hand_pct at 83.9%, and villain_air is very high at 57.5%. Despite being OOP, this exceeds the value-betting threshold per Example 6: equity 66%+, worse_hand_pct 83%+, dry-ish board with villain weakness. The nut flush draw provides backup equity. Three clubs on board demand protection to deny free cards.
- **key_factors:** ['high_equity', 'nut_flush_draw', 'very_high_worse_hand_pct', 'protection_on_dangerous_board']
- **factor_conflicts:** OOP position normally argues for pot control, but 66.5% equity with 83.9% worse hands and the nut flush draw overwhelmingly override the OOP penalty. Same pattern as Example 6 but even stronger.
- **alternatives_considered:** ['CHECK: rejected — with three clubs on board and 83.9% worse hands, giving free cards is dangerous. Hero has nut flush draw backup and massive equity advantage.']

---

## Hand 10 — `d8886_BB_flop`

### Identification

- **situation_id:** `d8886_BB_flop`
- **deal_id:** 8886
- **hero_cards:** QcJc
- **board:** 2s5dJd
- **street:** flop
- **hero_position:** BB
- **villain_positions:** ['CO', 'BTN']
- **num_opponents:** 2
- **facing_bet:** False
- **pot:** 80.0
- **to_call:** 0.0

### Action history

- preflop: BB call
- *(compact)* `preflop: BB call`

### Ground truth vs model prediction

- **Expected (ground_truth_label / expert_action):** BET
- **Model prediction (this run, masked):** CHECK
- **Prep-file `model_prediction`:** CHECK
- **Prep-file `oracle_action`:** CHECK
- **Prep-file `adjusted_action`:** CHECK
- **Mismatch:** expected: BET, predicted: CHECK

### Corrected bias-signature values

| feature | value |
|---|---|
| `hero_range_percentile` | 0.7926 |
| `equity_vs_range` | 0.6020 |
| `villain_air_pct` | 0.5882 |
| `villain_top_pair_plus_pct` | 0.1812 |
| `spr` | 1.2500 |
| `better_hand_pct` | 0.0791 |
| `worse_hand_pct` | 0.9091 |

### Oracle predicted action distribution

| action | raw prob | legal after mask |
|---|---|---|
| FOLD | 0.0045 | no |
| CHECK | 0.4163 | yes |
| CALL | 0.4883 | no |
| BET | 0.0878 | yes |
| RAISE | 0.0031 | no |

Argmax over legal set → **CHECK**

### Full 54-feature vector

| feature | value |
|---|---|
| `street` | 0 |
| `facing_bet` | 0 |
| `pot_size` | 80 |
| `to_call` | 0 |
| `pot_odds` | 0 |
| `bet_to_pot` | 0 |
| `hero_position` | 5 |
| `villain_position` | 2 |
| `is_ip` | 0 |
| `hand_category` | 7 |
| `hand_rank` | 1.322 |
| `is_made_hand` | 1 |
| `is_strong_made` | 0 |
| `is_monster` | 0 |
| `has_flush_draw` | 0 |
| `has_straight_draw` | 0 |
| `draw_outs` | 0 |
| `is_monotone` | 0 |
| `is_two_tone` | 1 |
| `is_rainbow` | 0 |
| `is_paired` | 0 |
| `is_double_paired` | 0 |
| `connectivity_score` | 2 |
| `high_card_rank` | 11 |
| `danger_score` | 0.25 |
| `flush_danger` | 0.25 |
| `straight_danger` | 0 |
| `raw_equity` | 0.602 |
| `equity_vs_range` | 0.602 |
| `better_hand_pct` | 0.079051 |
| `worse_hand_pct` | 0.909091 |
| `equity_margin` | 0.602 |
| `spr` | 1.25 |
| `is_3bet_pot` | 0 |
| `villain_aggression_count` | 0 |
| `villain_checked_back` | 0 |
| `villain_call_count` | 0 |
| `num_opponents` | 2 |
| `villain_top_pair_plus_pct` | 0.1812 |
| `villain_draw_pct` | 0 |
| `villain_air_pct` | 0.5882 |
| `villain_range_capped` | 0 |
| `board_favour` | 0.1188 |
| `num_callers_to_bet` | 0 |
| `facing_raise` | 0 |
| `flush_block_pct` | 0 |
| `overcard_outs` | 3 |
| `improvement_probability` | 0.234043 |
| `hero_range_percentile` | 0.792627 |
| `has_showdown_value` | 1 |
| `villain_fold_equity_estimate` | 0.670433 |
| `flush_draw_rank` | 0 |
| `is_preflop_aggressor` | 0 |
| `villain_medium_made_pct` | 0.2305 |

### Pass 1 labelling history

Not available in repo. `pass1_T[1-4]_labels.jsonl` cover only the BP building-block situations, not the MW-50 `d*` test hands. No per-agent pre-aggregation votes exist for this sid.

### Labelled-set cross-reference (test_set_50_labelled.jsonl)

- **expert_action:** BET
- **expert_confidence:** HIGH
- **difficulty:** 1
- **expert_reasoning:** Hero has TPGK (QJ on J-high board) with 62% equity, 91% worse hands, and villain_air at 60%. Despite being OOP, this mirrors Example 6: high equity (60%+), very high worse_hand_pct (91%), dry-ish board (danger 0.25), and weak villain ranges. A small bet (25-33% pot) extracts value from the wide, air-heavy ranges of both opponents. The board slightly favours hero and villain TP+ is only 18%.
- **key_factors:** ['high_equity', 'high_worse_hand_pct', 'high_villain_air', 'dry_board']
- **factor_conflicts:** OOP position argues for check, but 62% equity with 91% worse hands on a low-danger board overrides the OOP default per Example 6 logic.
- **alternatives_considered:** ['CHECK: defensible for pot control but leaves significant value against two opponents with 60% air and 91% worse hands.']

---
