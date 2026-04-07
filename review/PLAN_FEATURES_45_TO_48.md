# Plan: Feature Expansion 45 → 48

**Date:** 7 April 2026
**Status:** PLAN — awaiting review before building

---

## 3 New Features

### Feature 46: `flush_block_pct` (float 0.0-1.0)

**What:** Percentage of villain's flush combos that hero blocks.
**How:** Separate function, NOT inside extract_range_composition.
Iterates villain's range using `get_valid_combos()` for combo-level
expansion. Counts combos with at least 1 card of the flush suit.
Of those, counts combos where hero holds one of the flush-suit cards.
Returns blocked / total (frequency-weighted).

**Edge cases:**
- Hero has 2 cards of the suit → hero HAS the draw, not a blocker
  → return 0.0 (hero's draw equity is in raw_equity already)
- is_rainbow board → return 0.0 (no flush threat)
- is_monotone board → many combos have the suit, blocking is weaker
  → returns correct lower percentage naturally
- Narrowed range (villain's betting range) used, not full preflop range

**Does NOT touch:** extract_range_composition, villain_draw_pct,
villain_air_pct, or any existing feature computation.

### Feature 47: `overcard_outs` (int 0, 3, or 6)

**What:** Count of hero hole cards ranking above the highest board
card, multiplied by 3 (each overcard = 3 outs).
**How:** Compare hero card ranks to `features['high_card_rank']`
(already computed by board analyzer).

**Edge cases:**
- A-high board → always 0 (nothing overcards an Ace)
- Only count above HIGHEST board card, not second highest
- Inline rank parsing dict, no import dependency

### Feature 48: `improvement_probability` (float 0.0-1.0)

**What:** Fraction of unseen deck cards that improve hero's hand
to two-pair or better. Does NOT count top-pair improvement
(that's covered by overcard_outs).
**How:** Piggyback on existing `evaluate_hand()`. For each unseen
card, evaluate hero's hand with that card added to the board.
If hand category improves to two-pair+, count it.

**Edge cases:**
- River → return 0.0 (no cards to come)
- Hero already has two-pair+ → return 1.0 (already improved)
- Excludes cards that merely give hero top pair
- Cost: ~47 evaluate_hand() calls on flop, ~46 on turn

---

## What Does NOT Change

- `extract_range_composition` loop (stays notation-level)
- `villain_draw_pct`, `villain_air_pct`, `villain_top_pair_plus_pct`
- `game_state_bridge.py`
- `situation_factory.py` (features auto-propagate through bridge)
- `poker_game.py`
- Any existing feature values in training data

---

## Build Sequence

1. Write `compute_flush_block_pct()` as standalone function in
   feature_extractor.py. Unit test independently.
2. Write `compute_overcard_outs()` as standalone function.
   Unit test independently.
3. Write `compute_improvement_probability()` as standalone function.
   Unit test independently.
4. Add all three to `extract_all_features()` as new Step 12.
5. Add to FEATURE_COLUMNS in gto_model.py (45 → 48).
6. Add to feature_keys.py.
7. Run full test suite — no regressions.

## Validation Sequence

8. Re-extract features for all 348 training situations
   (only the 3 new features — existing 45 stay unchanged).
9. Re-extract features for 50 test situations.
10. 5-fold CV on 45 features (baseline) vs 48 features.
    Compare log-loss, not just accuracy.
11. Retrain v9-3way-v3 from scratch on 48 features.
12. Reference gate: must be >= 32/40.
13. Feature importance: drop any new feature below 1%.
14. Independent test: run on 50-hand unseen test set.
15. Leakage check.

## Risks

- `improvement_probability` may be redundant with `raw_equity`
  → validation gate catches this (step 13 drops it if < 1%)
- `flush_block_pct` needs villain's range → must pass villain
  position into the new function
  → already available in features dict
- Performance: flush_block_pct does its own combo-level pass
  → ~300 evals per call, sub-1ms, acceptable
- 48 features / 349 samples = 7.3:1 ratio
  → XGBoost regularization handles this; validation catches overfit

## Bookmarked for Later

- Upgrade extract_range_composition to combo-level (improves all
  range features but breaks data consistency — do in fresh cycle)
- Straight draw blocker (same principle, more complex, weaker signal)
