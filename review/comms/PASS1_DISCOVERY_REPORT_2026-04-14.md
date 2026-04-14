# Pass 1 Discovery Report (T5-T6) — 2026-04-14

## Scope

- 78 discovery agents (39 batches × 2 teams)
- Bottom-up scan of the 54 features per hand, starting from feature 54
- Excluded from discovery (already covered globally by T1-T4 protocol): equity_vs_range, villain_top_pair_plus_pct, villain_medium_made_pct, villain_draw_pct, villain_air_pct, is_ip, hero_range_percentile, pot_odds (8 features)

## Summary statistics

| Metric | Value |
|---|---|
| Hands | 385 |
| Features tagged per hand (T1-T4 avg) | 13.1 |
| Features added per hand (T5-T6 discovery avg) | 9.5 |
| Union size per hand (avg) | 22.6 |
| Union size per hand (avg, out of 46 non-excluded) | 22.6 / 46 |

## Most-discovered features (T5-T6 found on >=30% of hands beyond T1-T4)

These are the biggest gaps in T1-T4 coverage. The union of T1-T4 + T5-T6 fills them.

| Feature | Added by T5-T6 | T1-T4 baseline | Union total |
|---|---|---|---|
| hand_category | 337 (87.5%) | 7 (1.8%) | 344 (89.4%) |
| raw_equity | 309 (80.3%) | 0 (0.0%) | 309 (80.3%) |
| is_made_hand | 279 (72.5%) | 0 (0.0%) | 279 (72.5%) |
| hand_rank | 260 (67.5%) | 0 (0.0%) | 260 (67.5%) |
| villain_range_capped | 222 (57.7%) | 2 (0.5%) | 224 (58.2%) |
| bet_to_pot | 199 (51.7%) | 9 (2.3%) | 208 (54.0%) |
| worse_hand_pct | 177 (46.0%) | 98 (25.5%) | 275 (71.4%) |
| board_favour | 153 (39.7%) | 36 (9.4%) | 189 (49.1%) |
| connectivity_score | 126 (32.7%) | 6 (1.6%) | 132 (34.3%) |
| spr | 121 (31.4%) | 163 (42.3%) | 284 (73.8%) |

## Features fully untagged — present in vector but never load-bearing per any of 6 teams

These features were untagged on >=90% of hands, suggesting low per-hand salience OR recurring blind spots:

| Feature | Untagged count | Interpretation |
|---|---|---|
| villain_position | 385 (100.0%) | Aggregate position (opener/bettor) covered indirectly by hero_position + action history |
| pot_size | 384 (99.7%) | Always implicit in bet_to_pot / pot_odds / spr |
| is_3bet_pot | 382 (99.2%) | Rarely present in this dataset (no 3bet pots) |
| to_call | 381 (99.0%) | Covered by pot_odds and bet_to_pot |
| hero_position | 378 (98.2%) | Covered implicitly via range_percentile and action history |
| is_double_paired | 378 (98.2%) | Rare board texture, only triggered on 2 paired boards |
| is_monotone | 370 (96.1%) | Rare board texture (3 of same suit at time of decision) |
| num_callers_to_bet | 364 (94.5%) | Typically 0 in this set |
| facing_raise | 358 (93.0%) | Boolean covered by action_history parsing |
| street | 344 (89.4%) |  |
| is_rainbow | 338 (87.8%) | Dominant/default texture; only noteworthy when absent |
| has_flush_draw | 330 (85.7%) |  |
| villain_call_count | 324 (84.2%) |  |
| is_monster | 322 (83.6%) | Boolean rollup of hand_category |
| villain_aggression_count | 315 (81.8%) |  |
| is_paired | 312 (81.0%) | Only interesting on paired boards |
| is_two_tone | 308 (80.0%) | Dominant texture; only noteworthy for flush_danger |
| has_straight_draw | 305 (79.2%) |  |
| high_card_rank | 303 (78.7%) |  |
| flush_draw_rank | 299 (77.7%) |  |

## Coverage completeness

- Features fully covered (0 untagged hands): 0 / 46
- Features mostly covered (untagged on <=10% of hands): 0 / 46
- Avg per-hand untagged: 23.4 features

## Training implications (Exp 3 auxiliary flags)

- 54 binary attn_* columns will be added: attn_{feature} = 1 if any of T1-T6 tagged it on that hand, else 0.
- T5-T6 meaningfully expanded coverage: +9.5 features per hand on average.
- The 7 features found on >=50% of hands by T5-T6 (hand_category, raw_equity, is_made_hand, hand_rank, villain_range_capped, bet_to_pot, worse_hand_pct) are the most load-bearing discoveries — they will now get attn=1 on most hands in training.

## Artefacts

- Per-hand union + untagged JSONL: `training-data/pass1_discovery_union.jsonl` (385 records)
- Raw T5-T6 discovery files: `/tmp/pass1_discovery_results/T{5,6}_batch{00-38}.json` (78 files)

## Next steps

1. Pass 2 targeted review on 40 STRONG + 13 MAJORITY + 24 HARD/CONTESTED + 1 CONFIDENT_SPLIT hands
2. Solver verification on flagged hands (14+ mandatory)
3. Vocabulary review (merge synonyms, reject noise)
4. Final label assembly with Exp 3 attn_* columns → v2.2 model training
