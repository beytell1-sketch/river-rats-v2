---
date: 2026-04-17
from: Programmer + GTO Expert
to: Owner
re: FB-40 3-miss investigation + full ship-gate table for v2.3 weighted model
status: SYSTEMATIC -- RAISE over-prediction across facing-bet CALL spots
---

# FB-40 Miss Investigation + Ship Gate Table

## Section 1: FB-40 Miss Investigation

### Evaluation baseline

All evaluations use `evaluate_v2_2.py` with `--csv training-data/v2_3_training.csv` (column order source) and legal-action masking enabled.

- **v2.2 model:** 29/40 = 72.5%
- **Weighted model:** 28/40 = 70.0%

The weighted model has **5 new misses** vs v2.2 (FB-07, FB-22, FB-29, FB-33, FB-34) and **4 recoveries** (FB-03, FB-24, FB-28, FB-40). Net: -1 hand. The 4 CALL->RAISE misses (FB-22, FB-29, FB-33, FB-34) share a single error pattern and are investigated below. FB-07 (FOLD->CALL) is a separate error type not covered here.

---

### Hand 1: FB-22

| Field | Value |
|-------|-------|
| **Situation ID** | FB-22 |
| **Hero cards** | JcTc |
| **Board** | Ts8c4h (flop) |
| **Street** | Flop |
| **Hero position** | CO (sandwich -- BB and BTN are opponents) |
| **Action history** | BB check, CO check, BTN bet 30, BB call 30, CO ??? |
| **Pot** | 150 (after BB call) |
| **To call** | 30 |
| **Expected action** | CALL (solver-verified, HIGH confidence) |
| **v2.2 prediction** | CALL (correct, 90.0% masked probability) |
| **Weighted prediction** | RAISE (wrong, 79.9% masked probability) |

**Probability distribution (weighted, masked & normalized):**

| FOLD | CALL | RAISE |
|------|------|-------|
| 9.4% | 10.7% | **79.9%** |

**Key features:** equity_vs_range=0.569, pot_odds=0.167, SPR=0.667, hand_cat=6 (top pair), hero_range_pct=0.768

**GTO analysis:** Hero has top pair (tens) with a ten-high flush draw blocker. BTN's small bet (20% pot) into two opponents after both checked represents a wide range -- often a stab. BB's call caps BB's range. Hero's JcTc is ahead of most of this action but facing two opponents with position disadvantage. The correct play is CALL: raising isolates against only better hands (overpairs, two pair), and the small bet size gives excellent pot odds. GTO does not raise top pair good kicker multiway with this SPR and this sizing.

**Verdict: SYSTEMATIC.** Model was confidently wrong (69.2% margin). This is a clear GTO call that the model predicts RAISE at 80%.

---

### Hand 2: FB-29

| Field | Value |
|-------|-------|
| **Situation ID** | FB-29 |
| **Hero cards** | AsKd |
| **Board** | 8s5s3d (flop) |
| **Street** | Flop |
| **Hero position** | CO |
| **Action history** | BB bet 45, CO ??? |
| **Pot** | 90 |
| **To call** | 45 |
| **Expected action** | CALL (solver-verified, MEDIUM confidence) |
| **v2.2 prediction** | CALL (correct, 58.5% masked probability) |
| **Weighted prediction** | RAISE (wrong, 69.9% masked probability) |

**Probability distribution (weighted, masked & normalized):**

| FOLD | CALL | RAISE |
|------|------|-------|
| 1.0% | 29.1% | **69.9%** |

**Key features:** equity_vs_range=0.460, pot_odds=0.333, SPR=1.111, hand_cat=2 (overcards), hero_range_pct=0.361

**GTO analysis:** Hero has AKo (no pair, no draw) on a low-connected board. BB's half-pot donk bet into the field is unusual but represents range advantage on low boards. Hero has two overcards with backdoor spade draw (As). Equity is ~46% which clears the 33% pot-odds threshold for a call. Raising accomplishes nothing -- hero has no made hand to protect, folds out worse, and gets called by better. The solver's MEDIUM confidence acknowledges this is closer to a fold than a raise. Calling is correct; raising is the worst of three options.

**Verdict: SYSTEMATIC.** Model was confidently wrong (40.8% margin). Hero has no made hand -- raising with air into a donk bet is anti-GTO.

---

### Hand 3: FB-33

| Field | Value |
|-------|-------|
| **Situation ID** | FB-33 |
| **Hero cards** | JcJd |
| **Board** | ThTd7c (flop) |
| **Street** | Flop |
| **Hero position** | CO (sandwich) |
| **Action history** | BB check, CO check, BTN bet 60, BB call 60, CO ??? |
| **Pot** | 210 |
| **To call** | 60 |
| **Expected action** | CALL (HIGH confidence) |
| **v2.2 prediction** | CALL (correct, 87.6% masked probability) |
| **Weighted prediction** | RAISE (wrong, 65.1% masked probability) |

**Probability distribution (weighted, masked & normalized):**

| FOLD | CALL | RAISE |
|------|------|-------|
| 14.0% | 20.9% | **65.1%** |

**Key features:** equity_vs_range=0.634, pot_odds=0.222, SPR=0.476, hand_cat=10 (overpair/strong made), hero_range_pct=0.806, is_strong_made=1

**GTO analysis:** JJ on TTx is effectively an overpair -- strong but vulnerable. BTN bets into two opponents and BB calls, creating a scenario where at least one opponent likely has a ten or a draw. Hero's JJ beats most of the field but loses to any Tx, TT, 77. With SPR=0.48 (very shallow), calling keeps the pot controlled and avoids committing the remaining stack against a range that is heavily weighted toward trips or better after the bet-and-call action. Raising forces action against hands that dominate hero. Classic pot-control call.

**Verdict: SYSTEMATIC.** Model was confidently wrong (44.2% margin). Pot control with an overpair on a paired board at low SPR is standard GTO.

---

### Hand 4: FB-34

| Field | Value |
|-------|-------|
| **Situation ID** | FB-34 |
| **Hero cards** | Ks6d |
| **Board** | As9s4s (flop) |
| **Street** | Flop |
| **Hero position** | CO (sandwich) |
| **Action history** | BB check, CO check, BTN bet 22, BB call 22, CO ??? |
| **Pot** | 134 |
| **To call** | 22 |
| **Expected action** | CALL (HIGH confidence) |
| **v2.2 prediction** | CALL (correct, 97.4% masked probability) |
| **Weighted prediction** | RAISE (wrong, 75.4% masked probability) |

**Probability distribution (weighted, masked & normalized):**

| FOLD | CALL | RAISE |
|------|------|-------|
| 9.7% | 15.0% | **75.4%** |

**Key features:** equity_vs_range=0.441, pot_odds=0.141, SPR=0.746, hand_cat=0 (no made hand), draw_outs=9, has_flush_draw=1, hero_range_pct=0.106, danger_score=0.580

**GTO analysis:** Hero has a bare Ks (king-high flush draw, NOT the nut flush draw because As is on board). On a monotone flop with Ace, raising a small bet with a non-nut flush draw is a major mistake: hero loses to As-x flush draws (which are common in BTN/BB ranges), can't fold out made flushes, and folds out all the hands hero has equity against. The correct play is calling for implied odds -- if the turn brings a spade, hero has the second-nut flush. Getting raised off a non-nut draw multiway is a disaster.

**Verdict: SYSTEMATIC.** Model was confidently wrong (60.4% margin). Raising a non-nut flush draw on a monotone board multiway is a fundamental error.

---

### Cross-Hand Pattern Analysis

| Feature | FB-22 | FB-29 | FB-33 | FB-34 |
|---------|-------|-------|-------|-------|
| Position | CO (sandwich) | CO | CO (sandwich) | CO (sandwich) |
| Facing small bet | Yes (20% pot) | Yes (50% pot) | Yes (29% pot) | Yes (16% pot) |
| SPR | 0.67 | 1.11 | 0.48 | 0.75 |
| Weighted RAISE prob | 79.9% | 69.9% | 65.1% | 75.4% |
| Margin | 69.2% | 40.8% | 44.2% | 60.4% |
| v2.2 CALL prob | 90.0% | 58.5% | 87.6% | 97.4% |

**Shared pattern:** All 4 hands are CO facing a bet with at least one other opponent remaining. All have low SPR. The weighted model pushes 65-80% RAISE probability where v2.2 gave 58-97% CALL probability. The class-weight rebalancing (RAISE weight increased from 3.00 to 2.89, BET weight crushed from 1.00 to 0.38) appears to have shifted probability mass broadly toward RAISE across all facing-bet decisions.

**Corroborating evidence:** MW-30 (KcTh top pair on KJ6, facing bet, expected CALL) also flipped from CALL (v2.2 at 90.5%) to RAISE (weighted at 69.6%). This is the same pattern leaking into the calibration reversal set.

### Overall FB-40 Verdict: SYSTEMATIC

All 4 CALL->RAISE misses share a single root cause: the balanced class weighting over-promoted RAISE relative to CALL on facing-bet spots. The model is confidently wrong (40-69% margin) on all 4. v2.2 was confidently correct (58-97% CALL probability) on all 4.

This is **not noise** -- it is a systematic shift in the CALL/RAISE decision boundary caused by class-weight rebalancing. However, the fix is non-trivial: a targeted CALL supplement risks shifting the boundary back and losing the RAISE hands the weighted model gets right (FB-10, FB-21, FB-24, FB-26, FB-36, FB-39). The owner should decide whether the MW-50 gains (+4pp) justify the FB-40 cost (-2.5pp).

---

## Section 2: Ship Gate Table

| # | Criterion | Target | Actual | PASS/FAIL |
|---|-----------|--------|--------|-----------|
| 1 | FB-40 accuracy | >=70.0% | **70.0%** (28/40) | **PASS** (at floor) |
| 2 | MW-50 accuracy | >=82.5% | **88.0%** (44/50) | **PASS** |
| 3 | Groups A+B absolute accuracy | >=70% abs + 5pp over v2.2 | **N/A** -- diagnostic hands never sourced | **BLOCKED** |
| 4 | Group D regression | <=1 hand regression vs v2.2 | **0 hands** regressed | **PASS** |
| 5 | Calibration reversals | 100% on all reversal hands | **7/10** (70%) | **FAIL** |
| 6 | Solver 8 MW misses | >=6/8 corrected | PENDING (owner-led) | **PENDING** |

### Criterion detail

**Criterion 1 -- FB-40 (PASS at floor):** 28/40 = 70.0%, exactly at the >=70.0% target. This is the floor, not comfortable margin. Using `v2_3_training.csv` for column order.

**Criterion 2 -- MW-50 (PASS):** 44/50 = 88.0%, exceeds 82.5% target by 5.5pp. Strong pass. MW-50 misses: d9941 (CHECK->BET), d1454 (BET->CHECK), d1562_HJ_river (CHECK->BET), d3688 (CHECK->BET), d0845 (CHECK->BET), d7640 (CHECK->BET).

**Criterion 3 -- Groups A+B (BLOCKED):** The diagnostic test set design document (`PLAN_V23_DIAGNOSTIC_TEST_SET_2026-04-15.md`) defines Groups A (mixed-zone) and B (BP-pattern) conceptually, but the actual hands were never sourced. Group B requires Track B (BP generator fix) to complete first. No hands exist to evaluate. This criterion cannot be assessed.

**Criterion 4 -- Group D regression (PASS):** 5 Group D reversal hands evaluated:

| Hand | v2.2 | Weighted | Regression? |
|------|------|----------|-------------|
| d2074_BTN_turn | CHECK (OK) | CHECK (OK) | No |
| d3688_BB_flop | BET (XX) | BET (XX) | No (both wrong) |
| d4312_CO_turn | BET (OK) | BET (OK) | No |
| d5466_CO_flop | BET (XX) | BET (XX) | No (both wrong) |
| d9556_BB_flop | CHECK (OK) | CHECK (OK) | No |

Regression count: **0**. Target: <=1. Pass.

**Criterion 5 -- Calibration reversals (FAIL):** 10 reversal hands from `GTO_REVERSAL_HANDS` in `calibration_exam.py`:

| Hand | Expected | v2.2 | Weighted | Status |
|------|----------|------|----------|--------|
| MW-30 | CALL | CALL (OK) | **RAISE (XX)** | **NEW REGRESSION** |
| MW-33 | RAISE | RAISE (OK) | RAISE (OK) | OK |
| MW-50 | FOLD | CALL (XX) | **FOLD (OK)** | **RECOVERED** |
| d2410_CO_turn | BET | BET (OK) | BET (OK) | OK |
| d3178_CO_river | BET | BET (OK) | BET (OK) | OK |
| d2074_BTN_turn | CHECK | CHECK (OK) | CHECK (OK) | OK |
| d3688_BB_flop | CHECK | BET (XX) | BET (XX) | Both wrong |
| d4312_CO_turn | BET | BET (OK) | BET (OK) | OK |
| d5466_CO_flop | CHECK | BET (XX) | BET (XX) | Both wrong |
| d9556_BB_flop | CHECK | CHECK (OK) | CHECK (OK) | OK |

Weighted: 7/10 correct. v2.2: 8/10 correct. The weighted model **regressed** on MW-30 (CALL->RAISE, same RAISE over-prediction pattern as FB-40). Target is 100%. **Hard FAIL.**

Note: MW-30 is KcTh on KJ6 facing a bet -- exactly the same CALL/RAISE confusion pattern documented in the FB-40 investigation. The RAISE over-prediction is not confined to FB-40; it leaks into the calibration reversal set.

---

## Section 3: Overall Ship Recommendation

### Summary

| Criterion | Result |
|-----------|--------|
| 1. FB-40 | PASS (at floor, 70.0%) |
| 2. MW-50 | PASS (88.0%) |
| 3. Groups A+B | BLOCKED (no test data) |
| 4. Group D regression | PASS (0 regressions) |
| 5. Calibration reversals | **FAIL** (7/10, MW-30 regression) |
| 6. Solver validation | PENDING |

### Recommendation: DO NOT SHIP

The weighted model fails Criterion 5 (calibration reversals) with a **new regression** on MW-30 that was not present in v2.2. This regression stems from the same RAISE over-prediction pattern documented in the FB-40 investigation: the class-weight rebalancing shifted the CALL/RAISE decision boundary toward RAISE across all facing-bet spots.

The MW-50 improvement (+4pp over v2.2) is real and valuable. The BET-fix retention (4/4) is solid. But shipping a model that introduces a calibration reversal failure on a 100%-must-pass hand is below the quality bar defined in the scope document.

### Possible next steps (owner decision)

1. **Accept and ship:** If the owner judges that MW-30's CALL->RAISE shift is tolerable given the MW-50 gains, the reversal gate could be relaxed. Risk: sets precedent for eroding calibration standards.

2. **Targeted CALL supplement (20-30 hands):** Add 20-30 facing-bet CALL exemplars (structurally similar to FB-22/29/33/34/MW-30) to the training set and retrain with the same balanced weights. Risk: may regress MW-50 or RAISE accuracy. Estimated cost: 1 labelling session + 1 retrain.

3. **Hybrid weighting:** Adjust class weights to partially suppress RAISE (currently 2.89x -- highest of all classes) without fully reverting to iter2 weights. This is a middle ground between the current RAISE over-prediction and iter2's CHECK over-prediction. Risk: requires experimentation.

4. **Park and move to v3.0:** Accept that the v2.2->v2.3 supplement improved MW-50 but introduced a RAISE bias on facing-bet spots. Ship v2.2 as the stable baseline and incorporate lessons into v3.0 architecture.

---

*Investigation complete. No model files modified. No retraining performed.*
