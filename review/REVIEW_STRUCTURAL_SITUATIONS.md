# Structural Review: Situation Designs for v9-3way Training Data

**Reviewer:** GTO Structural Analyst
**Date:** 6 April 2026
**Scope:** DESIGN_POSITION_AMP_SWEEPS.md (79 sits) + DESIGN_CALL_SWEEPS.md (72 sits)

---

## 1. Board Selection Quality

**Position Amp (PA):** Good texture diversity — dry A-high, low connected, monotone, paired, connected wet, two-tone, river brick. All realistic 3-way textures. No unrealistic boards.

**CALL:** Also strong. Jd8d4c, Ks9h5d, Qh7c2s, AQ5r, paired 77x are all common textures. One gap: neither design includes a **Broadway-heavy board** (e.g., KQT, QJT). These boards create complex range interactions where CO's broadways dominate and callers have many draws. The model needs these — they produce the tightest CALL/FOLD boundaries.

**Missing from both:** No low monotone board (e.g., 7s4s2s). The knowledge base identifies these as BB-favoured textures. PA Board 3 is monotone but J-high, still somewhat raiser-favoured.

## 2. Hand Spectrum Quality

**PA strengths:** Each board spans air-to-nuts with 8-10 hands. The boundary zone (equity 0.35-0.55) is well-populated on most boards.

**PA Board 4 (QcQd7s):** Hand #5 (7h6h) is labelled "Trips kicker (middle pair)" — this is actually middle pair (sevens), not trips. The 7 makes a pair with the board 7s, not with a Q. Clarify the category. Also missing: an Ax without a Q (e.g., AhTc) — tests whether A-high bets or checks on a paired Q board where CO has all the Qx.

**PA Board 7 (Jc8c5d2h):** Only 9 hands and this became HU after BB folded on flop. This is no longer a 3-way situation. If the design targets 3-way learning, this board teaches a different decision geometry. Either replace with a board that stays 3-way or flag clearly that this is a 3-way-to-HU transition test.

**CALL Board 3 (Qh7c2s5d):** Includes two sets (5h5c, 2c2d) which are both clear RAISE hands. That is 2 of 9 situations producing RAISE labels, not CALL. For a CALL-focused design, replace one set with a hand closer to the CALL/RAISE boundary — e.g., QsJh (TPGK facing double barrel, genuine call/fold decision).

**CALL Board 1 (Jd8d4c):** Td9d at equity 0.53 with 17 draw outs — this is a flush draw + straight draw combo. With 17 outs this hand likely wants to check-raise, not call. It sits above the CALL boundary. Consider replacing with a weaker combo draw (e.g., 7d6d — flush draw + gutshot, ~12 outs) that genuinely tests FOLD vs CALL.

## 3. Boundary Coverage

**PA:** Well-placed. Hands in the 0.35-0.55 equity zone appear on every board. The CHECK/BET boundary is where the model fails, and these hands sit right on it.

**CALL:** The FOLD-to-CALL boundary is covered (Boards 1, 6). The anti-over-call boundary is strong (Boards 5, 7, 8). Weakness: the CALL-to-RAISE boundary has too many obvious RAISE hands (sets on Boards 3, 4) and not enough marginal raise/call decisions. Add hands like overpairs facing single bets on wet boards — these are the genuine CALL-vs-RAISE boundary hands.

## 4. Action History Plausibility

All action histories are realistic for 100bb 6-max. Pot sizes track correctly. One concern: **CALL Board 5 (KdJc6s)** has 4 players to the flop (CO opens, BTN calls, SB calls, BB calls) — this is a 4-way pot, not 3-way. The design says 3-way but the action is 4-way pre, becoming 3-way when SB folds on flop. Acceptable but should be flagged so the feature extractor encodes the correct initial player count.

**CALL Board 7 (AsQd5h):** Action says "BB checks, hero bets 30, CO raises to 90. BB folds." This is CO raising BTN's bet — a standard raise, not a check-raise. The description says "check-raise" but CO did not check first. Correct the terminology or the action sequence.

## 5. Missing Situations for Gate Failures

Given 33% position_amp and 36% CALL recall:

- **Turn CALL spots are underrepresented.** Only CALL Board 3 covers the turn. Add a board with a turn flush-completing card where hero must decide whether the draw hitting changes the call/fold calculus.
- **OOP CALL with pair + draw** (e.g., middle pair + flush draw) — a common spot where the model likely defaults to FOLD. CALL Board 6 has some but the draws are mostly naked. Add a paired-plus-draw hand.
- **Multistreet OOP value bet progression** is absent from PA. Board 8 is the only river spot. Add an OOP turn lead after flop check-through on a dynamic board — this is the purest position amplification test.

---

**Bottom line:** Both designs are structurally sound with good texture/spectrum coverage. Fix the 5 specific issues above (PA Board 7 HU transition, CALL Board 3 redundant sets, CALL Board 5 player count, CALL Board 7 terminology, Td9d too strong on CALL Board 1) and add Broadway-heavy and low-monotone boards to fill the remaining texture gaps.
