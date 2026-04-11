# Review: v9-3way Model Training

**Date:** 6 April 2026
**Status:** REVIEW — model trained, awaiting gate check

---

## What Was Done

### 1. Vocabulary mapping (blocker fix)

`export_3way_training.py` now maps expert 5-action labels to oracle
3-action vocabulary before export:
- CHECK → FOLD (passive, not facing bet)
- BET → RAISE (aggressive, not facing bet)
- FOLD, CALL, RAISE → unchanged

199 rows exported (1 LOW excluded).

### 2. Model training

Trained XGBoost 3-class classifier on 199 expert-labelled 3-way
situations. Hyperparameters tuned for small dataset (max_depth=4,
learning_rate=0.05, min_child_weight=5, higher regularization).

### 3. GtoOracle 3-class support

`gto_model.py` now auto-detects 3-class vs 5-class models:
- 5-class: FOLD, CHECK, CALL, BET, RAISE (v8, v9-baseline)
- 3-class: FOLD, CALL, RAISE (v9-3way specialist)

Both model types load and predict correctly through the same API.

## Training Results

| Metric | Value |
|--------|-------|
| Training samples | 199 |
| Features | 45 |
| Classes | 3 (FOLD, CALL, RAISE) |
| **Test accuracy (80/20)** | **95.0%** |
| **5-fold CV accuracy** | **89.9%** |
| Best iteration | 213 of 300 |

### Per-class performance (5-fold CV)

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| FOLD | 0.900 | 0.947 | 0.923 | 114 |
| CALL | 1.000 | 0.364 | 0.533 | 11 |
| RAISE | 0.893 | 0.905 | 0.899 | 74 |

CALL recall is weak (36.4%) — expected with only 11 samples.
FOLD and RAISE are solid.

### Top 10 features

| Feature | Importance |
|---------|-----------|
| worse_hand_pct | 0.119 |
| equity_margin | 0.110 |
| facing_bet | 0.097 |
| better_hand_pct | 0.089 |
| raw_equity | 0.082 |
| bet_to_pot | 0.075 |
| pot_odds | 0.063 |
| equity_vs_range | 0.051 |
| villain_top_pair_plus_pct | 0.034 |
| hand_category | 0.028 |

The model learned from equity and relative hand strength —
exactly the features that should drive multiway decisions.

## Files Changed

| File | Change |
|------|--------|
| `export_3way_training.py` | Added CHECK→FOLD, BET→RAISE mapping |
| `gto_model.py` | Auto-detect 3-class models, use instance action map |
| `models/gto_model_v9_3way.json` | New — 3-class specialist |
| `models/gto_model_v9_3way_45feat.json` | New — same model, explicit name |
| `models/training_report_v9_3way.json` | New — training report |

## Test Results

864 passed, 7 failed (all pre-existing). Zero regressions.

## Next: Gate Check

The reference evaluator needs to compare v9-3way against v8 on
the 40-hand multiway reference set. The oracle router should now
route 3-way predictions to v9-3way automatically.

## Known Limitations

- CALL class has only 11 training samples — low recall expected
- UTG has only 8 training situations — UTG 3-way performance
  will be weak
- SB has 0 training situations (no SB in 3-way data)
- Model is 3-class; the multiway adjuster downstream may need
  to handle the vocabulary difference
