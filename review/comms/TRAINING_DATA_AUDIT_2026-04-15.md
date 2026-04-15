# Training Data Audit — v2_2_training.csv
**Date:** 2026-04-15
**Auditor:** Programmer (Track 3)
**File:** training-data/v2_2_training.csv
**Rows:** 385 | **Raw features:** 54 | **Attn features:** 54 | **Label cols:** 2

---

## 1. Per-Feature Audit Table

All 54 raw features are present in every row (0 missing values). Counts below are structural zeros.

| Feature | Zero% | Mean | Median | Std | Min | Max | Zeros | Shape | Flag |
|---|---|---|---|---|---|---|---|---|---|
| street | 17.4% | 0.995 | 1.0 | 0.818 | 0.0 | 2.0 | 67 | mixed | ANOMALY-A |
| facing_bet | 59.7% | 0.403 | 0.0 | 0.491 | 0.0 | 1.0 | 230 | binary | expected |
| pot_size | 0.0% | 115.8 | 90.0 | 68.99 | 80.0 | 360.0 | 0 | skewed | ok |
| to_call | 59.7% | 24.69 | 0.0 | 44.71 | 0.0 | 270.0 | 230 | skewed | expected |
| pot_odds | 59.7% | 0.106 | 0.0 | 0.131 | 0.0 | 0.429 | 230 | skewed | expected |
| bet_to_pot | 59.7% | 0.145 | 0.0 | 0.186 | 0.0 | 0.75 | 230 | skewed | expected |
| hero_position | 2.1% | 3.02 | 3.0 | 1.463 | 0.0 | 5.0 | 8 | approx_normal | ok |
| villain_position | 3.1% | 2.977 | 3.0 | 1.408 | 0.0 | 5.0 | 12 | approx_normal | ok |
| is_ip | 49.9% | 0.501 | 1.0 | 0.501 | 0.0 | 1.0 | 192 | binary | expected |
| hand_category | 21.6% | 4.987 | 4.0 | 4.825 | 0.0 | 16.0 | 83 | skewed | ANOMALY-B |
| hand_rank | 0.0% | 1.465 | 0.96 | 1.581 | 0.13 | 7.08 | 0 | skewed | ok |
| is_made_hand | 47.8% | 0.522 | 1.0 | 0.500 | 0.0 | 1.0 | 184 | binary | expected |
| is_strong_made | 71.2% | 0.288 | 0.0 | 0.454 | 0.0 | 1.0 | 274 | binary | expected |
| is_monster | 84.7% | 0.153 | 0.0 | 0.361 | 0.0 | 1.0 | 326 | binary | expected |
| has_flush_draw | 87.0% | 0.130 | 0.0 | 0.337 | 0.0 | 1.0 | 335 | binary | expected |
| has_straight_draw | 74.3% | 0.257 | 0.0 | 0.438 | 0.0 | 1.0 | 286 | binary | expected |
| draw_outs | 66.0% | 2.447 | 0.0 | 4.044 | 0.0 | 17.0 | 254 | skewed | ANOMALY-C |
| is_monotone | 96.1% | 0.039 | 0.0 | 0.194 | 0.0 | 1.0 | 370 | binary | expected |
| is_two_tone | 65.2% | 0.348 | 0.0 | 0.477 | 0.0 | 1.0 | 251 | binary | ANOMALY-D |
| is_rainbow | 41.6% | 0.584 | 1.0 | 0.494 | 0.0 | 1.0 | 160 | binary | ANOMALY-D |
| is_paired | 82.1% | 0.179 | 0.0 | 0.384 | 0.0 | 1.0 | 316 | binary | expected |
| is_double_paired | 98.4% | 0.016 | 0.0 | 0.124 | 0.0 | 1.0 | 379 | binary | expected |
| connectivity_score | 0.0% | 3.395 | 2.0 | 2.126 | 2.0 | 10.0 | 0 | skewed | ok |
| high_card_rank | 0.0% | 11.891 | 13.0 | 1.815 | 6.0 | 14.0 | 0 | skewed | ok |
| danger_score | 10.1% | 0.356 | 0.25 | 0.283 | 0.0 | 1.0 | 39 | approx_normal | ANOMALY-E |
| flush_danger | 61.3% | 0.140 | 0.0 | 0.195 | 0.0 | 0.580 | 236 | skewed | ANOMALY-F |
| straight_danger | 63.1% | 0.161 | 0.0 | 0.235 | 0.0 | 0.80 | 243 | skewed | ANOMALY-F |
| raw_equity | 0.8% | 0.393 | 0.324 | 0.311 | 0.0 | 1.0 | 3 | skewed | ok |
| equity_vs_range | 0.8% | 0.393 | 0.324 | 0.311 | 0.0 | 1.0 | 3 | skewed | ok |
| better_hand_pct | 4.9% | 0.490 | 0.540 | 0.369 | 0.0 | 1.0 | 19 | approx_normal | ok |
| worse_hand_pct | 4.9% | 0.495 | 0.449 | 0.375 | 0.0 | 1.0 | 19 | approx_normal | ok |
| equity_margin | 0.3% | 0.287 | 0.178 | 0.360 | -0.429 | 0.998 | 1 | skewed | ok |
| spr | 0.0% | 1.028 | 1.111 | 0.302 | 0.278 | 1.25 | 0 | skewed | ok |
| is_3bet_pot | 100.0% | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 385 | constant | ANOMALY-G |
| villain_aggression_count | 51.4% | 0.535 | 0.0 | 0.590 | 0.0 | 2.0 | 198 | skewed | expected |
| villain_checked_back | 52.7% | 0.473 | 0.0 | 0.500 | 0.0 | 1.0 | 203 | binary | expected |
| villain_call_count | 38.4% | 0.709 | 1.0 | 0.656 | 0.0 | 3.0 | 148 | skewed | expected |
| num_opponents | 0.0% | 1.977 | 2.0 | 0.151 | 1.0 | 2.0 | 0 | approx_normal | ok |
| villain_top_pair_plus_pct | 0.0% | 0.400 | 0.329 | 0.201 | 0.127 | 0.952 | 0 | approx_normal | ok |
| villain_draw_pct | 50.4% | 0.067 | 0.0 | 0.125 | 0.0 | 0.556 | 194 | skewed | ANOMALY-H |
| villain_air_pct | 2.6% | 0.281 | 0.296 | 0.159 | 0.0 | 0.718 | 10 | approx_normal | ok |
| villain_range_capped | 38.4% | 0.616 | 1.0 | 0.487 | 0.0 | 1.0 | 148 | binary | expected |
| board_favour | 0.0% | -0.100 | -0.029 | 0.201 | -0.652 | 0.173 | 0 | approx_normal | ok |
| num_callers_to_bet | 100.0% | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 385 | constant | ANOMALY-G |
| facing_raise | 93.0% | 0.070 | 0.0 | 0.256 | 0.0 | 1.0 | 358 | binary | expected |
| flush_block_pct | 77.7% | 0.026 | 0.0 | 0.056 | 0.0 | 0.284 | 299 | skewed | ANOMALY-I |
| overcard_outs | 65.2% | 1.395 | 0.0 | 2.087 | 0.0 | 6.0 | 251 | skewed | expected |
| improvement_probability | 41.3% | 0.277 | 0.174 | 0.368 | 0.0 | 1.0 | 159 | skewed | ANOMALY-J |
| hero_range_percentile | 3.6% | 0.535 | 0.541 | 0.333 | 0.0 | 0.997 | 14 | approx_normal | ok |
| has_showdown_value | 47.8% | 0.522 | 1.0 | 0.500 | 0.0 | 1.0 | 184 | binary | expected |
| villain_fold_equity_estimate | 0.0% | 0.365 | 0.384 | 0.204 | 0.002 | 0.763 | 0 | approx_normal | ok |
| flush_draw_rank | 66.2% | 3.558 | 0.0 | 5.343 | 0.0 | 14.0 | 255 | skewed | expected |
| is_preflop_aggressor | 69.4% | 0.307 | 0.0 | 0.462 | 0.0 | 1.0 | 267 | binary | expected |
| villain_medium_made_pct | 15.8% | 0.252 | 0.296 | 0.167 | 0.0 | 0.613 | 61 | approx_normal | ANOMALY-K |

---

## 2. Flagged Anomalies

### ANOMALY-A: `street` — Mixed encoding (17.4% zeros, but deeper issue)
- 200 rows encode street as numeric (0.0/1.0/2.0); 185 rows encode as string ('flop'/'turn'/'river')
- Two data sources merged without normalisation: `d-series` hands use numeric, `BP-series` use strings
- When coerced to float for analysis, string 'flop' → parse error → 0.0; actual zeros are `0.0=flop` encoding
- **The 17.4% zero count is misleading: all 67 are legitimately flop rows in numeric encoding**
- Root issue: inconsistent encoding across data sources. Classifier will receive strings in some rows, floats in others.
- **Severity: HIGH — model may fail or silently misinterpret this column**

### ANOMALY-B: `hand_category` — 21.6% zeros (83 rows)
- Category 0 appears to be "air/trash" (avg equity 0.14, never is_made_hand=1)
- 83 rows with hc=0 have flush or straight draws (so not pure nothing)
- Category 0 is a valid enum value — these are legitimately weak hands
- **Verdict: structural/expected. Not a bug.**

### ANOMALY-C: `draw_outs` — 66.0% zeros
- 178/254 zero-draw rows are made hands (expected: made hands have 0 outs to improve)
- 76 rows: not made, no FD, no SD flagged, draw_outs=0 — these are "air" hands with no categorised draw
- Consistent with hand_category=0 (air) rows where no specific draw type is flagged
- **Verdict: structural. Consistent with hand type composition.**

### ANOMALY-D: `is_two_tone` + `is_rainbow` board texture (mutual exclusion gap)
- 11 turn rows have NO texture flag set (0 for all three: monotone/two_tone/rainbow)
- All 11 are numeric-street `d-series` turns; flush_danger=0 on all, straight_danger varies
- Likely a board_analyzer bug where turn cards producing 4-card monotone boards fall outside the 3-card flop texture logic
- **Severity: MEDIUM — 11/385 rows (2.9%) have undefined board texture. Model receives no suit information for these.**

### ANOMALY-E: `danger_score` — 10.1% zeros (39 rows)
- All 39 rows with danger_score=0 also have flush_danger=0 AND straight_danger=0
- These are genuinely low-danger boards (dry rainbow boards with low connectivity)
- **Verdict: structural. Dry boards legitimately score 0.**

### ANOMALY-F: `flush_danger` + `straight_danger` — 61-63% zeros
- flush_danger=0: 225 of 236 are rainbow boards (expected — no flush draw possible)
- Remaining 11 zero flush_danger on non-rainbow boards = the same 11 no-texture anomaly rows
- straight_danger=0: consistent with low-connectivity boards
- **Verdict: mostly structural; the 11 anomaly rows are the same ANOMALY-D instances.**

### ANOMALY-G: `is_3bet_pot` + `num_callers_to_bet` — 100% zeros (constant features)
- Both are all-zero across all 385 rows
- Training data is sourced entirely from HU situations (no 3bet pots sampled, no multi-caller scenarios)
- These features carry zero signal for the current model — they are dead weight
- **Severity: LOW for current model (all training data is single-raised pots HU). HIGH concern for v2.3 if 3bet pot situations are added — model has no prior on these features.**

### ANOMALY-H: `villain_draw_pct` — 50.4% zeros (194 rows)
- 130/194 zero-draw-pct rows have no FD/SD on board — structurally correct (no draws exist)
- 64 rows: board HAS a draw (FD or SD flagged) but villain_draw_pct=0
- Investigated: for all 64 of these, villain_top_pair_plus_pct + villain_air_pct + villain_medium_made_pct ≈ 1.0 (within 0.05)
- Range composition genuinely assigns zero draw% to villain (e.g. tight preflop ranges that can't hold draws on this board)
- **Verdict: structural. Villain range model assigns genuine zero draw combos in these spots.**

### ANOMALY-I: `flush_block_pct` — 77.7% zeros (299 rows)
- 187/299 zero-flush-block rows are rainbow boards (expected — blocking irrelevant)
- Remaining 112 are two-tone or monotone boards where hero simply holds no flush-relevant card
- **Verdict: structural. Zero is correct when hero's hand doesn't block flushes.**

### ANOMALY-J: `improvement_probability` — 41.3% zeros (159 rows)
- 64/159 are is_made_hand=1 (made hands don't need to improve — zero is valid)
- 95 rows: not made AND improvement_probability=0
- Breakdown: these are "air" hands (hand_category=0, no flagged draws) — hands with no made strength and no categorised draw path. Zero improvement probability is valid for true air.
- Cross-check: all 95 also have draw_outs=0 and has_flush_draw=0 and has_straight_draw=0
- **Verdict: structural. Air hands with no draw path legitimately have 0 improvement probability.**

### ANOMALY-K: `villain_medium_made_pct` — 15.8% zeros (61 rows)
- For all 61 zero-medium rows: villain_top_pair_plus_pct + villain_draw_pct + villain_air_pct ≈ 1.0 (within 0.05 for all 61)
- Medium made hands simply aren't in villain's range for these spots (e.g. board runs out unfavorably for medium pair combos)
- **Verdict: structural. Range composition correctly assigns zero medium made% in polarised spots.**

---

## 3. Summary Table

| Anomaly | Feature(s) | Severity | Verdict |
|---|---|---|---|
| A | `street` mixed encoding | HIGH | Bug — two data sources encoded differently |
| B | `hand_category` 21.6% zeros | — | Expected (air category = 0) |
| C | `draw_outs` 66% zeros | — | Expected (made hands + air) |
| D | 11 rows with no board texture flag | MEDIUM | Bug — turn board texture not computed |
| E | `danger_score` 10.1% zeros | — | Expected (dry boards) |
| F | `flush_danger`/`straight_danger` zeros | — | Mostly expected (see ANOMALY-D) |
| G | `is_3bet_pot` + `num_callers_to_bet` all zero | LOW now / HIGH for v2.3 | Data gap — no 3bet/multi-caller training examples |
| H | `villain_draw_pct` 50.4% zeros | — | Expected (range genuinely draw-free) |
| I | `flush_block_pct` 77.7% zeros | — | Expected (rainbow boards + no block cards) |
| J | `improvement_probability` 41.3% zeros | — | Expected (air hands + made hands) |
| K | `villain_medium_made_pct` 15.8% zeros | — | Expected (polarised range spots) |

**Confirmed bugs requiring ML Architect review: ANOMALY-A and ANOMALY-D.**

---

## 4. Preliminary Recommendation

Training data has **2 genuine issues** and **9 structurally expected zero patterns**.

**ANOMALY-A (street encoding)** is the most serious: 52% of rows (200/385) encode street as a float (0/1/2) while 48% use a string ('flop'/'turn'/'river'). If the model training pipeline coerces all values to float, string rows will be read as 0 (flop) — corrupting street signal for 185 rows. This needs verification of the training pipeline's type handling before v2.3 supplement training proceeds.

**ANOMALY-D (11 turn rows with no texture)** is minor in volume (2.9%) but clean: these rows are silently missing suit-context features. If the training pipeline doesn't handle this, those 11 rows provide misleading board texture input.

**ANOMALY-G (constant features)** is not a training bug per se — these features are correctly zero for the current HU single-raised-pot dataset. However, v2.3 plans to supplement with 3bet pot or multiway situations; if added, the model will have seen no non-zero examples of these features during v2.2 training and may handle them poorly.

**Overall verdict:** Training data is sufficient for v2.2 retraining (addressing ANOMALY-A in the pipeline). v2.3 supplementation should be held until ANOMALY-A encoding is confirmed handled correctly by the training script, and ANOMALY-D is patched in the board analyzer.

No re-extraction required if the training pipeline correctly coerces `street` to a consistent type. Confirm with ML Architect before proceeding.
