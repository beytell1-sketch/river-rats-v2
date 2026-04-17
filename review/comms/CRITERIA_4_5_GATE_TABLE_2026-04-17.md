# Criteria 4+5 Gate Evaluation — v2.3 Clean Model

**Model:** `river-rats-core/models/v2_3_clean_model.json` (commit `6d7eef5`)
**Base:** v2.2 + Section 1 + CALL supplement, no UMBRELLA, no class weighting
**Date:** 2026-04-17
**Evaluator:** Automated (evaluate_v2_2.py inference path, legal-action masking)

---

## Criterion 4 — Group D Reversal Regression (gate: <=1 hand)

| Hand | Expected | v2.2 | v2.3 | Regression? |
|------|----------|------|------|-------------|
| d2074_BTN_turn | CHECK | CHECK | BET | **YES** |
| d3688_BB_flop | CHECK | BET | BET | no (v2.2 also wrong) |
| d4312_CO_turn | BET | BET | BET | no |
| d5466_CO_flop | CHECK | BET | BET | no (v2.2 also wrong) |
| d9556_BB_flop | CHECK | CHECK | CHECK | no |

**Regressions: 1** (d2074_BTN_turn: v2.2 correct CHECK, v2.3 wrong BET)

**Criterion 4 verdict: PASS** (1 <= 1)

---

## Criterion 5 — Calibration Reversals (gate: 100%)

| Hand | Expected | v2.3 | Status |
|------|----------|------|--------|
| MW-30 | CALL | CALL | PASS |
| MW-33 | RAISE | RAISE | PASS |
| MW-50 | FOLD | CALL | **FAIL** |
| d2074_BTN_turn | CHECK | BET | **FAIL** |
| d2410_CO_turn | BET | BET | PASS |
| d3178_CO_river | BET | BET | PASS |
| d3688_BB_flop | CHECK | BET | **FAIL** |
| d4312_CO_turn | BET | BET | PASS |
| d5466_CO_flop | CHECK | BET | **FAIL** |
| d9556_BB_flop | CHECK | CHECK | PASS |

**Correct: 6/10**

**Criterion 5 verdict: FAIL** (6/10, gate requires 100%)

### MW-30 Critical Check

MW-30 predicts **CALL** on the clean model (expected CALL). The CALL->RAISE regression seen in the weighted model does NOT occur here. **MW-30: PASS.**

### Failure Analysis

- **MW-50** (FOLD expected, CALL predicted): Pre-existing. Also wrong on v2.2. Not a regression.
- **d2074_BTN_turn** (CHECK expected, BET predicted): Regression vs v2.2.
- **d3688_BB_flop** (CHECK expected, BET predicted): Pre-existing. Also wrong on v2.2.
- **d5466_CO_flop** (CHECK expected, BET predicted): Pre-existing. Also wrong on v2.2.

Of 4 failures: 1 is a new regression (d2074), 3 are pre-existing v2.2 failures.

---

## Full Gate Table (updated)

| # | Criterion | Target | Actual | Status |
|---|-----------|--------|--------|--------|
| 1 | FB-40 accuracy | >=70.0% | 72.5% | **PASS** |
| 2 | MW-50 accuracy (recalibrated) | >=82.0% | 82.0% | **PASS** |
| 3 | Groups A+B | >=70% + 5pp | N/A | BLOCKED |
| 4 | Group D regression | <=1 hand | 1 | **PASS** |
| 5 | Calibration reversals | 100% | 60% (6/10) | **FAIL** |
| 6 | Solver 8 MW | >=6/8 | PENDING | -- |

---

## Ship Recommendation

**DO NOT SHIP.** Criterion 5 fails at 6/10 (100% required). However, 3 of 4 failures are pre-existing v2.2 defects (MW-50, d3688, d5466) — the model did not regress on these. The sole new failure is d2074_BTN_turn.

If the owner elects to redefine the reversal gate to exclude pre-existing v2.2 failures, Criterion 5 would be 6/7 non-pre-existing = still fails on d2074.

Next steps are owner's call: accept d2074 regression within Criterion 4's 1-hand budget (already counted there as PASS), or require supplemental training to fix d2074.
