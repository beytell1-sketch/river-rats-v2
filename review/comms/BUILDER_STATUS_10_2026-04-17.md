---
date: 2026-04-17
from: Builder
to: Main terminal / Owner
re: Ship gate — DO NOT SHIP (Criterion 5 hard FAIL + systematic RAISE over-prediction)
status: BLOCKED — RAISE weight caused calibration reversal regression
---

# Builder Status #10 — Gate Table + FB-40 Investigation

## Gate table

| # | Criterion | Target | Actual | Result |
|---|---|---|---|---|
| 1 | FB-40 | ≥70.0% | 70.0% | PASS (at floor) |
| 2 | MW-50 | ≥82.5% | 88.0% | PASS |
| 3 | Groups A+B | ≥70% abs + 5pp | N/A | **BLOCKED** (test hands never sourced) |
| 4 | Group D regression | ≤1 hand | 0 | PASS |
| 5 | Calibration reversals | 100% | **7/10** | **FAIL** |
| 6 | Solver 8 MW | ≥6/8 corrected | — | PENDING (owner) |

**Criterion 5 is a HARD FAIL.** MW-30 (100%-must-pass reversal)
regressed from CALL → RAISE.

## FB-40 misses — SYSTEMATIC, not noise

4 misses (not 3 — count was corrected): FB-22, FB-29, FB-33, FB-34.
All share the same pattern:
- Expected: **CALL**
- Predicted: **RAISE** (65-80% probability, 40-69% margin)
- v2.2 predicted: CALL correctly (58-97% probability)
- Shape: CO facing small bet, low SPR, multiway

**Root cause:** balanced class weighting set RAISE weight to 2.89×
(highest class, smallest representation). This over-promoted RAISE
predictions systematically. The same over-prediction caused the
MW-30 calibration reversal regression (CALL → RAISE).

## What this means

The class-weighted approach successfully fixed the BET/CHECK boundary
(MW-50 BET-misses corrected, CHECK discrimination restored 14/17).
But it introduced a CALL→RAISE confusion as a side effect — the
RAISE weight was too aggressive.

## Fix options (quick, same data)

### Option A — Capped RAISE weight
Re-run class weighting with RAISE weight capped at ~1.5× (down from
2.89×). This preserves the BET down-weighting that fixed MW-50
while preventing RAISE over-prediction. Expected: MW-30 reversal
restores, FB-40 recovers 2-4 hands, MW-50 stays ≥84%.

### Option B — Per-class manual weights
Set weights manually: BET=0.40, CHECK=1.0, FOLD=1.5, CALL=1.5,
RAISE=1.5 (flat non-BET weighting). Simpler, less risk of
over-promoting any minority class.

### Option C — Sample weighting by source
Weight v2.2-base rows at 1.0, supplement rows at 0.5. This
dampens the entire supplement uniformly without class-specific
distortion.

**Builder recommends Option A or B** (fastest, most targeted). Both
are a 20-minute retrain with no new data, no new labelling. The
RAISE over-prediction is an artefact of the weighting formula, not
a data deficiency.

## Commits

- `4dbc747` — investigation + gate table report

## Awaiting

Owner direction on weighting fix (A / B / C / other). 20-minute
turnaround once directed.
