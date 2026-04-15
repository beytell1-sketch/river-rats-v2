---
date: 2026-04-15
from: Builder
to: Owner
re: hero_range_percentile investigation — test harness bug found, Track A scope correction needed
---

# hero_range_percentile = 0.00 Investigation

## TL;DR

- **The `hrp = 0.00` on the 10 MW misses is a test-harness bug, not a feature pattern or model bias signature.**
- MW test_set_50 `feat_dict` is **missing 6 of the 54 required features** entirely (not a `feat_dict` written with zeros — the keys don't exist).
- My test-time evaluation used `try float(v) except 0.0` — missing keys silently defaulted to 0.
- After re-extracting features via `extract_all_features`, hrp ranges 0.024–0.899 across MW hands (healthy distribution).
- **The 80% MW accuracy remains unchanged** after the fix — so the Gate 7 miss is a real model bias, just not the one Track A described.

## Evidence

### 1. MW test_set_50 feat_dict completeness

`feat_dict` on all 50 MW hands has **48 keys**, not the required 54. Missing:
- `flush_draw_rank`
- `has_showdown_value`
- `hero_range_percentile` ← the flagged one
- `is_preflop_aggressor`
- `villain_fold_equity_estimate`
- `villain_medium_made_pct`

These 6 features were never written into the MW test set. Whatever pipeline produced `test_set_50_labelled.jsonl` used an older feature schema.

### 2. Training CSV is intact

`training-data/v2_2_training.csv` has hrp populated on 371/385 hands (96%), distribution mean 0.555, median 0.556, range 0.003–0.997. Only 14 hands have hrp=0.0 — genuine bottom-of-range cases (9 BP + 5 d-series).

### 3. Model trained correctly

The v2.2 model was trained on complete features. The bug is only in the **test harness** — my MW eval script encoded missing keys as 0.

### 4. Re-extracted MW evaluation

Running `extract_all_features()` on each MW hand to populate all 54 features:
- hrp range: 0.024–0.899 (was: all hrp=0.0)
- Accuracy: **80.0%** (unchanged)
- Miss count: 10 (was 10; 1 hand swap — d2920 now correct, d4534 now missing)

## Impact on Track A v2.3 scope

Section 2 of `PLAN_V23_SCOPE_2026-04-15.md` currently claims the CHECK-bias signature includes `hero_range_percentile = 0.00`. **This claim is wrong and must be removed.** The remaining signature elements (hero MIDDLE/OOP, checked-to, SPR 1.0-1.5, villain_checked_back=1) still hold.

**New corrected bias signature** (from the re-extracted MW misses):
| Feature | Old miss avg | Non-miss avg |
|---|---|---|
| hero_range_percentile | 0.641 | 0.443 |
| equity_vs_range | 0.656 | 0.431 |
| villain_air_pct | 0.320 | 0.280 |
| villain_top_pair_plus_pct | 0.371 | 0.425 |
| spr | 1.250 | 1.250 |
| better_hand_pct | 0.292 | 0.549 |
| worse_hand_pct | 0.697 | 0.428 |

## Actions taken

- Verified `extract_all_features` produces complete features for all 50 MW hands
- Confirmed 80% accuracy is the real model performance, not harness artifact
- Track A scope document needs a correction: remove the hrp=0.00 bullet from Section 2
- Flag: any future test set must run through `extract_all_features` at evaluation time, not rely on stored `feat_dict`

## Recommendations

1. **Correct Track A scope** — Section 2 CHECK-bias signature, drop hrp=0.00. I'll update in-place.
2. **Add test-harness guard** — evaluator should warn if any feat_dict is missing >0 of the 54 FEATURE_COLUMNS; fail fast.
3. **Gate 7 solver verification still needed** on the 10 MW misses — the bias is real (80% is 2.5pp short of 82.5% target), just not the hrp-shape described.
4. **v2.3 fix direction unchanged** — Pass 2 panel bias toward CHECK in mixed zones is still the target; the SPR 1.0–1.5 + checked-back + MIDDLE/OOP signature still applies.
