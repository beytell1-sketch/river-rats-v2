# Calibration Exam Grading — v3.1 Labelling Round

**Date:** 9 April 2026
**Exam file:** /tmp/blind_calibration_exam_v3.txt (24 hands)
**Answer key:** /tmp/calibration_answer_key_v3.json
**Results file:** review/calibration_exam_v3_results.txt

---

## Score: 23/24 (95.8%) — GATE PASSED (minimum 20/24)

## GTO Reversal Hands

The 3 GTO-reversal hands in the reference set are:
- **MW-30:** Expert key says FOLD. Agent said CALL.
- **MW-33:** Expert key says RAISE. Agent said RAISE. CORRECT.
- **MW-47:** Not in the 24-hand calibration exam (removed as leakage).

**MW-30 status:** The answer key has NOT been updated with Phase 2
corrections. Phase 2 audit confirmed MW-30's tuple is correct
(1,0,0,1,0). The owner has NOT yet re-reviewed MW-30 with the
verified action sequence. The solver correction (FOLD→CALL) is
SUSPENDED per Governing Principle 4. The agent answered CALL
citing the solver correction — technically wrong against the
current key, but the key itself may be stale.

**Impact on gate:** If MW-30 key is updated to CALL, score becomes
24/24 (100%). If MW-30 stays FOLD, score is 23/24 (95.8%). Either
way, the 20/24 gate is passed.

---

## Failure Analysis

### MW-30 (agent: CALL, key: FOLD)

The agent cited "solver-corrected MW-30 pattern — 44% equity vs
18.4% pot odds, 26pp surplus overrides bet-and-call signal." This
is the known disputed hand. The agent applied the v1.2 KB's
corrected Example 3, which frames MW-30 as a CALL. The answer key
was written before the correction.

**Resolution needed:** Owner must re-review MW-30 with the Phase 2
verified action sequence and decide the correct label. Until then,
the discrepancy is documented but does not block the gate.

---

## Bias Profile (for reviewer briefing)

### Known bias #1: Over-fold with "action narrows ranges" heuristic

The labelling agent shows a tendency to FOLD when facing bet-and-call
or multi-street aggression, even when equity significantly exceeds
pot odds. This was documented in the restart prompt as Labelling
Agent Known Bias #1.

**Where to watch for it in the 406 labels:**
- Any FOLD where equity > pot_odds + 5pp AND hero has a made hand
- Any FOLD citing "bet-and-call narrows ranges" or "multi-street
  aggression signals strength"
- Boards where villain_aggression_count >= 1 AND equity_margin > 0.10
  AND label is FOLD

**The corrected rule (from KB Example 3):** Fold only when BOTH:
1. Equity is near or below pot odds (within 5pp)
2. Hero's specific holding is dominated by the narrowed range

When equity exceeds pot odds by 20+ pp with a made hand, the action
signal is insufficient to override the equity surplus. Label CALL.

### Known bias #2: Under-betting OOP

The agent may CHECK hands that should BET when OOP, even when
equity is high and villain ranges are capped/weak. The KB Example 6
pattern (OOP value bet exception) requires 60%+ equity with 85%+
worse hands on a dry board.

**Where to watch:**
- Any CHECK where equity > 0.55 AND worse_hand_pct > 0.80 AND
  facing_bet = 0 AND villain_air_pct > 0.40

---

## Calibration Verdict

PASSED (23/24 or 24/24 depending on MW-30 resolution). The over-fold
bias is documented and will be included in the reviewer briefing.
Reviewers must specifically check for this pattern in the 406 labels.
