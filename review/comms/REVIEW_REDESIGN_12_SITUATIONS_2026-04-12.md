# Review: 12 Redesigned Facing-Bet Situations

**Date:** 2026-04-12
**Reviewer:** Independent Reviewer
**File reviewed:** `review/comms/REDESIGN_12_AFFECTED_SITUATIONS_2026-04-12.md`

---

## Summary

| FB | Action order correct? | Classification correct? | Math correct? | Label assessment OK? | Card conflicts? |
|----|----------------------|------------------------|---------------|---------------------|----------------|
| FB-01 | YES | YES (OOP-closing) | YES | YES | NONE |
| FB-04 | YES | YES (OOP-closing) | YES | YES | NONE |
| FB-06 | YES | YES (OOP-closing) | YES | YES | NONE |
| FB-10 | YES | YES (OOP-closing) | YES | YES | NONE |
| FB-13 | YES | YES (OOP-closing) | YES | YES | NONE |
| FB-15 | YES | YES (OOP-closing) | YES | YES (re-eval flagged) | NONE |
| FB-17 | YES | YES (OOP-closing) | YES | YES | NONE |
| FB-19 | YES | YES (Sandwich, CO behind) | YES | YES | NONE |
| FB-21 | **NO** | **NO** | YES | YES (but moot) | NONE |
| FB-27 | YES | YES (OOP-closing) | YES | YES | NONE |
| FB-35 | YES | YES (OOP-closing) | YES | YES (re-eval flagged) | NONE |
| FB-39 | YES | YES (Sandwich, CO behind) | YES | YES | NONE |

---

## Issues Found

### FB-21 -- CRITICAL: BB classified as sandwich but should be closing action

FB-21 is a CO-opens, BTN-calls, BB-calls pot. The redesign corrects the impossible original sequence ("BB checks, BTN checks, CO bets") to "BB checks, CO bets 45." It then classifies BB as sandwiched with BTN behind.

This is wrong. Apply the ground truth rule: **after CO bets, action proceeds clockwise from the bettor: BTN (next clockwise) then BB (wraps).** BTN responds to CO's bet first. BB is LAST to act. BB closes action -- BB is not sandwiched.

The redesign's own Part 1 states the rule correctly for the seven BB-closing fixes (FB-01 etc.): "After CO bets, action wraps clockwise from CO: the next player clockwise is BTN, then BB." FB-21 has the identical structure (CO bets in a BB/CO/BTN pot) yet reaches the opposite conclusion. This is an internal contradiction.

The audit appendix (line 290) also confirms: "after CO bets: BTN acts, then BB (BB is last = closes action)."

**Fix required:** FB-21 classification must change from "Sandwich (BTN behind)" to "OOP-closing." The FOLD label (pocket fives, ~8-10% equity vs 25% pot odds) survives regardless -- equity is far below threshold in either classification.

**Impact on axis counts:** The redesign's net sandwich count drops by 1 further. Remaining sandwich situations from the 12 fixes: FB-19 and FB-39 only (not FB-21).

### No other errors found

The remaining 11 redesigns are correct on all five verification criteria. The seven BB-closing corrections (FB-01, 04, 06, 10, 15, 17, 27) and the two CO-closing corrections (FB-13, FB-35) correctly apply the clockwise-from-bettor rule. The two BTN-bets-sandwich corrections (FB-19, FB-39) correctly identify BB as first responder with CO behind.

---

## Verdict

**APPROVED WITH FIXES**

1 situation (FB-21) has an incorrect classification that contradicts the redesign's own stated rule. Fix FB-21 from sandwich to OOP-closing. The FOLD label is unaffected. All other 11 redesigns are correct. After this single fix, all 12 are clear to ship.
