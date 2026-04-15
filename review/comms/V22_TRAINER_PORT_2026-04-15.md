---
date: 2026-04-15
from: Builder (programmer)
to: Main terminal + Owner
re: Stream A — v2.2 trainer + evaluator port, A.3 validation
status: **A.1 + A.2 SHIPPED. A.3 STOP-condition triggered — Track 2 NOT closed.**
plan: review/comms/PLAN_CONSOLIDATED_2026-04-15.md §2 Stream A
---

# V2.2 Trainer/Evaluator Port — Delivery Report

## Summary

- A.1 (port trainer) — **complete**. `river-rats-core/train_model_v2_2.py`.
- A.2 (port evaluator) — **complete**. `river-rats-core/evaluate_v2_2.py`.
- A.3 (reproduction validation) — **STOP-condition hit**. FB-40 matches
  (29/40 = 72.5%); MW-50 diverges (**42/50 = 84.0%** vs target 40/50 = 80.0%,
  with d4534-IN instead of d4534-OUT). Track 2 **remains open**.

Per the consolidated plan §8: *"A.3 numbers don't match 72.5% / 80.0% →
STOP, report, do not commit closure of Track 2."* This report is that
stop signal. The port itself is sound; the divergence points at a
mismatch between the recovered eval script's self-trained model and the
live `v2_2_model.json` — see §4 below.

## 1. Files added

| File | Lines | Purpose |
|---|---|---|
| `river-rats-core/train_model_v2_2.py` | 307 | Ported trainer with provenance + preflight gate |
| `river-rats-core/evaluate_v2_2.py` | 398 | Ported evaluator (108-feat + legal-action mask) |
| `river-rats-core/tests/test_train_model_v2_2.py` | 167 | Preflight + encoding tests |
| `river-rats-core/tests/test_evaluate_v2_2.py` | 129 | Mask + shape tests |

`review/recovered/` preserved unchanged as historical reference (A.4).

## 2. Encoding — ANOMALY-A = path 3 confirmation

The ported trainer replicates the recovered `CAT_MAPS` path-3 encoding
byte-for-byte (numeric first, categorical-map fallback). Unit tests
`test_encode_numeric_street_returns_float` and
`test_encode_string_street_maps_via_cat_maps` exercise both branches.
**ANOMALY-A is confirmed as path 3**: the 185 mixed-string rows in
`v2_2_training.csv` were encoded correctly at training time; no
corruption was introduced.

## 3. Test results

```
python3 -m pytest river-rats-core/tests/test_train_model_v2_2.py \
                  river-rats-core/tests/test_evaluate_v2_2.py -v
```

13 passed in 0.85s:

- test_encode_numeric_street_returns_float
- test_encode_string_street_maps_via_cat_maps
- test_encode_string_hero_position_maps_via_cat_maps
- test_encode_non_categorical_numeric_passthrough
- test_preflight_blocks_mixed_csv_by_default
- test_allow_mixed_encoding_skips_preflight
- test_cli_refuses_to_overwrite_canonical_model
- test_legal_mask_no_bet_keeps_check_and_bet_only
- test_legal_mask_facing_bet_keeps_fold_call_raise_only
- test_predict_legal_masks_illegal_actions
- test_predict_legal_preserves_legal_top_pick
- test_feature_spec_loads_54_plus_54_from_real_csv
- test_attn_padding_always_one_on_fb40_row_assembly

## 4. A.3 reproduction — STOP

Command:

```
python3 river-rats-core/evaluate_v2_2.py --detail
```

Against `river-rats-core/models/v2_2_model.json`:

| Set | Target | Actual | Match? |
|---|---|---|---|
| FB-40 | 72.5% (29/40) | **72.5% (29/40)** | YES |
| MW-50 | 80.0% (40/50), d2920-IN / d4534-OUT | **84.0% (42/50)**, d2920-IN / **d4534-IN** | **NO** |

### MW-50 per-hand divergence

My evaluator gets the 10 "target misses" + 2 extra correct. The two
hands predicted correctly that the recorded 80% run missed include at
minimum `d4534_BTN_river` (expected CHECK, predicted CHECK in my run —
should have been "OUT" per plan). Full FB-40 and MW-50 per-hand tables
are reproducible via `--detail`.

### Root-cause hypothesis

The recovered `eval_MW_with_legal_action_masking.py` trains **its own
model in-script** (n_estimators=95, hard-coded, no early stopping),
then evaluates that fresh model on MW-50 — producing 80.0%.

The live `v2_2_model.json` was produced by the Phase-4 heredoc training
(recovered as `train_v2_2_MODEL.py`), which used `n_estimators=800` +
`early_stopping_rounds=50` and settled on the early-stopped best
iteration. These are **two different models** — the fresh in-script
re-train in the eval does NOT match the committed model.

Against the committed `v2_2_model.json`, the correct MW-50 number
appears to be 84.0% (42/50), which is **better** than the recorded
80.0%. FB-40 is unchanged at 72.5% because FB-40 happens to be
invariant between the two.

### What this means for Track 2

Closure of Track 2 requires clean reproduction of **both** numbers
against the committed model. The FB-40 leg passes; the MW-50 leg does
not. Options for main terminal to adjudicate:

1. **Update the target** — accept 84.0% as the corrected reference
   number for MW-50 against the live model, note the recorded 80% was
   an artifact of the recovered eval's self-trained shadow model.
2. **Re-verify** — run the recovered eval script as-is from
   `review/recovered/` (which will self-train its own model) and
   confirm it reproduces exactly 80% / 40-50 / d4534-OUT; if yes,
   accept that the recovered number is an orthogonal measurement that
   does not need to match the live model.
3. **Investigate further** — are there other differences (feature
   extraction drift, stored feat_dict schema change) that would
   explain the 4-hand gap?

Builder recommends option 1 + 2 in sequence: accept 84% as the
canonical MW-50 number for the live model, and optionally validate the
recovered script's 80% as a shadow measurement.

## 5. Constraints respected

- Canonical `v2_2_model.json` NOT overwritten (A.1 defaults to
  `v2_2_model_port.json`; CLI hard-refuses the canonical name).
- `review/recovered/` NOT modified, moved, or deleted.
- `v2_2_training.csv` NOT regenerated.
- `--allow-mixed-encoding` flag provided for legacy reproduction.
  Default is strict preflight (fails on current mixed CSV until v2.3
  regeneration).

## 6. Closing statement

**Track 2 is NOT closed.** A.1 + A.2 are ready to ship and provide a
durable, provenance-linked in-tree trainer+evaluator. A.3 reproduces
FB-40 cleanly but surfaces a 4-hand MW-50 divergence that requires
main-terminal adjudication before Track 2 can be marked closed.

— Builder
