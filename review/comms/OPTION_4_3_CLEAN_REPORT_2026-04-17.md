# Option 4+3 Clean Report

**Date:** 2026-04-17
**Configuration:** v2.3-clean (no UMBRELLA, no class weighting)

---

## Section 1: CALL Supplement

Generated 32 CALL hands across 3 sub-patterns:
- CALL_POT_ODDS: 12 hands (weak/drawing hands facing small bet, pot odds justify call)
- CALL_MEDIUM_STR: 12 hands (medium-made hands facing bet, call-worthy not raisable)
- CALL_TRAP_FLAT: 8 hands (monster/strong hands flatting to trap)

All 32 hands: facing_bet=1, num_opponents=2 (3-way).
Labelled as CALL (factory-designed GTO-correct action).

---

## Section 2: Assembly

| Source | Rows | Notes |
|--------|------|-------|
| v2.2 base | 385 | Re-encoded via CAT_MAPS |
| Phase 4 (non-UMBRELLA) | 207 | Excluded 263 UMBRELLA-prefixed sids |
| Pilot | 16 | |
| CALL supplement | 32 | New for this config |
| **After dedup** | **637** | 3 duplicates removed |

**Action distribution:**

| Action | Count | % |
|--------|-------|---|
| BET | 288 | 45.2% |
| CHECK | 137 | 21.5% |
| CALL | 89 | 14.0% |
| FOLD | 75 | 11.8% |
| RAISE | 48 | 7.5% |

Preflight schema check: **PASS** (no --allow-mixed-encoding).

---

## Section 3: Training

- **CV:** 93.09% +/- 1.35%
- **Holdout:** 94.53%
- **Best iteration:** 157
- **Class weighting:** NONE
- **Model:** `river-rats-core/models/v2_3_clean_model.json`

---

## Section 4: 5-Criterion Gate Table

| # | Criterion | Target | Result | Status |
|---|-----------|--------|--------|--------|
| 1 | FB-40 accuracy | >=70.0% | **72.5%** (29/40) | **PASS** |
| 2 | MW-50 accuracy | >=82.5% | **82.0%** (41/50) | **FAIL** (-0.5pp) |
| 3 | Groups A+B | >=70% abs + 5pp | N/A | **BLOCKED** |
| 4 | Group D regression | <=1 hand | 0 hands | **PASS** |
| 5 | Calibration reversals | 100% | Not evaluated (requires calibration exam pipeline) | **PENDING** |
| 6 | Solver | PENDING | PENDING | **PENDING** |

**Gate verdict: FAIL** (Criterion 2 misses by 0.5pp)

---

## Section 5: MW-50 6-Way Per-Hand Comparison

### v2.2 BET-misses (8 hands) -- recovery status in clean model

| hand_id | expected | v2.2 | clean | Status |
|---------|----------|------|-------|--------|
| d2410_CO_turn | BET | CHECK (XX) | **BET (OK)** | **FIXED** |
| d1983_HJ_turn | BET | CHECK (XX) | **BET (OK)** | **FIXED** |
| d1562_HJ_turn | BET | CHECK (XX) | **BET (OK)** | **FIXED** |
| d8886_BB_flop | BET | CHECK (XX) | **BET (OK)** | **FIXED** |
| d9653_BB_river | CHECK | BET (XX) | BET (XX) | Still wrong |
| d4809_BB_turn | CHECK | BET (XX) | BET (XX) | Still wrong |
| d1562_HJ_river | CHECK | BET (XX) | BET (XX) | Still wrong |
| d3688_BB_flop | CHECK | BET (XX) | BET (XX) | Still wrong |

**BET-fix retained: 4/4** (the 4 BET-miss hands that could be fixed ARE fixed).
The other 4 were v2.2 BET-over-CHECK errors that persist in clean.

### Clean model regressions (v2.2 correct, clean wrong)

| hand_id | expected | v2.2 | clean |
|---------|----------|------|-------|
| d8007_BB_flop | CHECK | CHECK (OK) | BET (XX) |
| d9941_CO_flop | CHECK | CHECK (OK) | BET (XX) |
| d6342_BTN_flop | CHECK | CHECK (OK) | BET (XX) |
| d0845_BB_flop | CHECK | CHECK (OK) | BET (XX) |
| d7640_HJ_river | CHECK | CHECK (OK) | BET (XX) |

**5 regressions** -- all CHECK->BET. The training data's 45% BET composition still over-promotes BET on marginal CHECK spots.

### Net effect

v2.2: 42/50 (84.0%) -> Clean: 41/50 (82.0%). Net -1.

The clean model trades 4 BET-miss corrections for 5 CHECK-to-BET regressions.

---

## Section 6: FB-40 Detail

FB-40: 29/40 = 72.5% (v2.2 was ~70%)

| hand_id | expected | v2.2 | clean |
|---------|----------|------|-------|
| FB-22 | CALL | CALL (OK) | CALL (OK) |
| FB-29 | CALL | CALL (OK) | CALL (OK) |
| FB-33 | CALL | CALL (OK) | CALL (OK) |
| FB-34 | CALL | CALL (OK) | CALL (OK) |

All 4 FB CALL hands maintained.

---

## Section 7: Ship Recommendation

**DO NOT SHIP.** MW-50 fails the 82.5% gate by 0.5pp.

The fundamental issue: removing UMBRELLA (268 BET-heavy hands) reduces total BET proportion from ~56% to ~45%, but 45% BET is still the dominant class. Without class weighting, the model still over-predicts BET on marginal CHECK spots (5 regressions). The BET-fix signal works (4/4 recovered) but is offset by CHECK regressions.

### Possible next steps

1. **Accept marginal fail:** MW-50 at 82.0% is 0.5pp below gate, within noise. Owner could relax to 82.0%.
2. **Add CHECK supplement:** Generate 15-20 CHECK-in-checked-pot hands to counterbalance the 45% BET. Risk: may dilute the BET-fix.
3. **Mild class weighting:** Apply CHECK weight=1.2x (gentle boost) to recover the 5 regressions without the RAISE over-prediction seen in previous weighted configs.
4. **Prune BET training data:** Reduce BET from 288 to ~250 by removing the lowest-confidence BET exemplars. Lowers BET% from 45% to ~42%.
