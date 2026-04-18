---
date: 2026-04-18
from: Builder
to: Main terminal / Owner
re: v2.3.1 retrain + evaluation — ALL GATES CLEAR
status: MODEL READY — awaiting ship approval (Teaching Layer 3 is parallel dep)
---

# v2.3.1 Retrain + Evaluation Results

## TL;DR

**All v2.3.1 gates PASS.** Model is shippable from the logic side.
Layer 3 (teaching value_extract air guard) remains a parallel
dependency; game stays on v2.2 until both land.

## Gates

| Gate | Floor / Expected | Actual | Status |
|---|---|---|---|
| FB-40 accuracy | ≥ 72.5% (v2.2 baseline) | **77.5%** (31/40) | ✅ PASS |
| MW-50 accuracy | ≥ 84.0% (v2.2 baseline) | **84.0%** (42/50) | ✅ PASS |
| A4d/Qs5s7s **flop** → CHECK | CHECK | CHECK (p=0.935) | ✅ PASS |
| T5h/JJ2 **flop** → CHECK | CHECK | CHECK (p=0.983) | ✅ PASS |
| 5-fold stratified CV | — | 0.944 ± 0.016 | clean |
| Holdout accuracy | — | 0.912 (124/136) | clean |

## Flop-litmus inference — the money shot

Training has TURN versions of these spots (Layer 2 counter-examples).
Inference tests the ORIGINAL flop playtest spots, where v2.3
predicted BET at 98.6% (A4d) and 72% (T5h). v2.3.1 result:

```
A4d on Qs5s7s (flop, BTN IP, villains checked):
  FOLD:  0.009   CHECK: 0.935   CALL: 0.008
  BET:   0.043   RAISE: 0.005
  → CHECK at 93.5% confidence (vs v2.3's BET at 98.6%)
  key features: is_made=0, outs=0, eq=0.099,
                hrp=0.956, board_adjusted_hrp=0.095
  Layer 1's board_adjusted_hrp (0.095 vs raw hrp 0.956)
  carried the "hero is weak despite high preflop rank" signal.

T5h on JJ2 (flop, BTN IP, villains checked):
  FOLD:  0.002   CHECK: 0.983   CALL: 0.003
  BET:   0.011   RAISE: 0.002
  → CHECK at 98.3% confidence (vs v2.3's BET at 72%)
  key features: is_made=0, outs=0, eq=0.164,
                hrp=0.148, board_adjusted_hrp=0.024
  Both Layer 1 (board_adjusted_hrp=0.024) and the model's
  broader "air + checked context → CHECK" learning from
  Layer 2 counter-examples contribute.
```

**Clean generalization.** Layer 2's turn training transferred to
flop inference, as hoped. No override used, no flop memorization
needed.

## Training run summary

```
Script:      river-rats-core/train_v2_3_1.py
CSV:         training-data/v2_3_1_training.csv (677 rows)
Features:    55 raw + 55 attn = 110 total
Class dist:  BET 288 (42.5%), CHECK 177 (26.1%), CALL 89 (13.1%),
             FOLD 75 (11.1%), RAISE 48 (7.1%)
Hyperparams: n_est=800, max_depth=5, lr=0.05, no class weighting,
             early_stopping=50
Best iter:   100
Holdout:     0.9118
5-fold CV:   0.9439 ± 0.0158
```

### Per-class holdout

```
FOLD   : precision 1.00  recall 1.00  f1 1.00 (15)
CHECK  : precision 0.97  recall 0.86  f1 0.91 (35)
CALL   : precision 0.80  recall 0.89  f1 0.84 (18)
BET    : precision 0.92  recall 0.98  f1 0.95 (58)
RAISE  : precision 0.75  recall 0.60  f1 0.67 (10)
```

RAISE is weakest by recall (0.60) but consistent with v2.3 clean
baseline (RAISE is the sparsest class at 7.1% of training data).
Not a v2.3.1 regression.

## Sources composing v2_3_1_training.csv

| Source | Rows |
|---|---|
| v2.2 base (`v2_2_training.csv`) | 385 |
| Phase 4 labels (no UMBRELLA) | 207 |
| Pilot labels (`v23_pilot_labelled.jsonl`) | 16 |
| CALL supplement | 32 |
| **Air-CHECK 3-way (v2.3.1 Layer 2)** | **40** |
| Deduped | -3 |
| **Total** | **677** |

`board_adjusted_hrp` (Layer 1) backfilled on-load for legacy rows
(`hero_range_percentile × equity_vs_range`, matching feature_extractor
Step 16 semantics). 97% non-zero coverage in final CSV.

## Provenance (CLAUDE.md §5.1)

Training manifest saved alongside the model:
`river-rats-core/models/v2_3_1_manifest.json`

Captures: git HEAD SHA, training/assembly script paths, CSV
sha256, hyperparameters, train/test split, holdout + CV results,
class distribution, source breakdown, and a trail of review-comms
commits for the Layer 2 decision thread.

## Artifacts this commit

**Training infrastructure:**
- `assemble_v23_1.py` (repo root) — extends `assemble_v23_clean.py`
  with `load_air_check_labels()` and legacy-row `board_adjusted_hrp`
  backfill.
- `river-rats-core/train_v2_3_1.py` — ports v2.3-clean hyperparams;
  writes model + report + provenance manifest.
- `review/eval_flop_litmus_v231.py` — flop-decision litmus inference
  (tests the playtest spots at the original street, against the
  turn-trained model).

**Model artifacts:**
- `river-rats-core/models/v2_3_1_model.json` — XGBoost model
- `river-rats-core/models/v2_3_1_training_report.json`
- `river-rats-core/models/v2_3_1_manifest.json`

**Training data:**
- `training-data/v2_3_1_training.csv` (677 rows, 110 features)

## Standard eval command (for reproducibility)

```bash
python3 river-rats-core/evaluate_v2_2.py \
    --model river-rats-core/models/v2_3_1_model.json \
    --csv   training-data/v2_3_1_training.csv \
    --only  both

python3 review/eval_flop_litmus_v231.py
```

## What's next

**Blockers for v2.3.1 ship:**
- [x] Layer 1: `board_adjusted_hrp` — DONE (80197cd)
- [x] Layer 2: air-CHECK counter-examples — DONE (this commit)
- [x] Retrain + evaluate — DONE (this commit, all gates PASS)
- [ ] Layer 3: teaching `value_extract` air guard — **parallel
      dependency on teaching terminal**

**When Layer 3 lands:**
- Game prototype swaps from v2.2 → v2.3.1
- HU set (`v23_air_check_hu.jsonl`, 30 rows unlabelled) remains
  in place for v2.4 with v3.2 prompt derivation

**Deferred items noted in review thread:**
- Dry-board weak-showdown class (if v2.3.1 generalizes poorly at
  playtest) → v2.3.2 if needed
- `check_give_up` vocab proposal → teaching terminal / v3.2 prompt
- 28 solver-enqueued hands from Phase 4 → owner-paced

Standing by for ship approval once Layer 3 lands.
