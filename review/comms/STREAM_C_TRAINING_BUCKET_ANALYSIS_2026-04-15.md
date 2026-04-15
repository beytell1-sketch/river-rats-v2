# Stream C — Training CSV Bucket Label Spot-Check (2026-04-15)

**Goal:** Determine whether the defensive multiway-checked-through bias bucket is under-labelled (label conservatism) or correctly labelled (model-only failure), and recommend v2.3 supplement sizing per directive-f §3.2.

**Scope:** Analysis only. No code/CSV/model changes.

---

## 1. Encoding approach

Imported `encode` and `CAT_MAPS` directly from the ported trainer:

- File: `/home/rupert/river-rats-v2/river-rats-core/train_model_v2_2.py`
- Function: `encode(row, col)` — **CAT_MAPS path 3** (float-first, categorical-map fallback, numeric default `0.0`).

Every predicate feature was read through `encode()` so rows where categorical/int-like columns arrive as either raw strings (`"flop"`) or pre-encoded numerics (`"0"`, `"1.0"`) resolve identically.

Analysis script (non-repo): `/tmp/stream_c_analysis.py`.

## 2. Filter predicate (as written)

```
facing_bet == 0
AND num_opponents >= 2
AND villain_checked_back == 1
AND villain_range_capped == 1
AND worse_hand_pct >= 0.55
AND equity_vs_range >= 0.35
AND spr <= 2.0
```

## 3. Bucket size

- Overall CSV rows: **385** (header + 385 data rows; file wc = 386 lines).
- Bucket rows matching predicate: **24** (6.2% of corpus).

## 4. Action-label distribution

| Action | Count | %      |
|--------|-------|--------|
| FOLD   |     0 |   0.0% |
| CHECK  |     5 |  20.8% |
| CALL   |     0 |   0.0% |
| BET    |    19 |  79.2% |
| RAISE  |     0 |   0.0% |

Distribution is bimodal BET/CHECK only — no FOLD/CALL/RAISE contamination, so shape conforms to the three-branch verdict framework (not an unanticipated 4th shape).

## 5. Median bias-signature feature values in bucket

| Feature                  | Median |
|--------------------------|-------:|
| hero_range_percentile    |  0.884 |
| equity_vs_range          |  0.875 |
| worse_hand_pct           |  0.946 |
| spr                      |  1.250 |

Bucket interior is deep inside the precondition shape — not clustered on edges.

## 6. Override / label_source metadata

All 24 bucket rows carry a non-empty `label_source`. Breakdown:

| label_source                                                       | Action | Count |
|--------------------------------------------------------------------|--------|------:|
| Pass1+relabel consensus                                            | BET    | 19    |
| Pass1+relabel consensus                                            | CHECK  |  3    |
| Pass 2 + SOLVER override (was Pass 2 BET, solver said CHECK)       | CHECK  |  1    |
| Pass 2 — solver mixed (BET combo) but owner keeps CHECK            | CHECK  |  1    |

**Panel-reversal / solver-override rows counted separately: 2** (both CHECK, both moved the label away from BET toward CHECK — i.e. the *conservative* direction). 22 rows are Pass1+relabel consensus (the standard path).

Directionally: every explicit override in the bucket pushes BET → CHECK. If anything, the human/solver pipeline is already slightly biased *toward* CHECK in this shape, not away from it.

## 7. Verdict (directive-f §3.2 logic)

- Bucket CHECK fraction = **20.8% (≤ 30%)** → **label signal is healthy**. The training labels correctly identify this multiway-checked-through spot as predominantly a BET (79.2%), matching GTO value-extraction logic for hero_range_percentile 0.88, worse_hand_pct 0.95, SPR 1.25.
- Model failed to learn the BET signal despite correct labels → **model-only failure**, not label conservatism.

**Branch: ≤ 30% CHECK → Supplement lower end.**

## 8. Supplement-size recommendation

**400 hands.**

Rationale: labels are correct; the issue is representation/weighting in training, not label quality. A smaller, targeted supplement concentrated on this precondition shape should be sufficient to shift the model's decision boundary without the larger 800-hand bias-countering dose.

## 9. Caveats

1. **Bucket size (24) is only marginally above the <20 sparsity threshold.** Directive-f flags <20 as critical; 24 is close enough that training-data sparsity for this precondition shape is a *contributing* factor, even if not the primary one. The 400-hand supplement will simultaneously raise representation above any reasonable sparsity concern — this is a happy alignment, not a coincidence to ignore.
2. **Boundary sensitivity is low.** No rows sit on `worse_hand_pct ∈ [0.55, 0.60)` or `spr ∈ (1.8, 2.0]`; only 2 rows on `equity_vs_range ∈ [0.35, 0.40)`. Shifting the predicate thresholds ±0.05 would change the bucket by at most 2 rows. The verdict is robust to predicate-edge wobble.
3. **All 24 rows carry `label_source` metadata** (no blanks / no `"base"` default). The "non-default" override count of 24 in the analysis reflects that every row went through the Pass1+relabel pipeline; the *solver-reversal* count (true overrides beyond consensus) is **2**, both moving toward CHECK. This does not change the verdict.
4. **Bucket features (median equity_vs_range 0.875, worse_hand_pct 0.946) are deeper than the predicate floors** (0.35, 0.55). The bucket's actual hand strength is stronger than the bias-signature minimum, which is further evidence the 79% BET label rate is poker-correct and not label conservatism papering over marginal spots.

---

**Recommendation feeds Track 6 supplement-sizing commit: 400 hands, targeted at the bias-signature precondition shape.**
