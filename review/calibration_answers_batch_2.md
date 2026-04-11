# Calibration Batch 2 — GTO Labelling Answers

**Agent:** GTO Labelling Agent v1.2
**Date:** 2026-04-09
**Reference material:** prompts/gto_labeller_v1.md, knowledge/three_way_gto.md v1.2

---

REF_ID: MW-24
ACTION: BET
CONFIDENCE: HIGH
REASONING: Hero holds QsJd (top pair second kicker) OOP on a dry, rainbow Q83 board. Equity is 63.95% — well above the 3-way TPTK reference range of 50-55% — with villain_air_pct 0.52 and worse_hand_pct 0.92, meaning 92% of villain hands lose to hero. Better_hand_pct is only 0.07, indicating minimal domination risk. This situation matches Worked Example 6 exactly: when equity exceeds 60%, villain air is high, and the board is dry/static, the OOP penalty is insufficient to override the value argument and a small bet (25-33% pot) is correct.

---

REF_ID: MW-27
ACTION: BET
CONFIDENCE: MEDIUM
REASONING: Hero holds JhJc (overpair) IP as BTN cold-caller on a dry 962r board. Both opponents have checked, signalling weakness — villain_air_pct is 0.51 (high) and villain_aggression_count is 0. Worse_hand_pct is 0.93, and villain_range_capped is 1 (BTN flat range is capped, CO checked rather than c-betting). IP position with both opponents weak and a high-air villain range supports a thin value bet at 25-33% pot; equity at 48.55% is on the margin but the combination of IP position, both opponents showing weakness, and 93% worse hands tips to BET rather than check-behind.

---

REF_ID: MW-28
ACTION: BET
CONFIDENCE: MEDIUM
REASONING: Hero holds JhJd (overpair) OOP as SB on the same 962r board. Equity is 60.65%, villain_air_pct is 0.57 (very high), and better_hand_pct is only 0.05 — only sets and higher overpairs from BTN's uncapped range beat hero. The OOP penalty normally argues for pot control, but at 60% equity with 94% worse hands and 57% villain air on a completely static dry board, the calculus from Worked Example 6 applies: when equity is strong, villain air is very high, and the board is dry, OOP position alone does not override the value of betting. A small bet (25-33% pot) is correct.

---

REF_ID: MW-30
ACTION: CALL
CONFIDENCE: HIGH
REASONING: This is the solver-corrected MW-30 reference hand. KcTh on KdJc6s facing a bet-and-call carries 44.05% equity against 18.42% pot odds — an equity surplus of more than 25 percentage points. The solver (GTO Wizard, April 2026) shows KT on KJ6 facing bet-and-call is a pure CALL: while the bet-and-call signal narrows both opponents' ranges, KT still beats significant portions of those narrowed ranges (worse Kx, middle pairs, draws), and the equity surplus is too large for folding to be correct. The "bet-and-call overrides equity" pattern applies only when hero's equity is genuinely close to break-even AND the holding is dominated — neither condition is met here.

---

REF_ID: MW-33
ACTION: RAISE
CONFIDENCE: HIGH
REASONING: This is the MW-33 calibration reference hand. Hero holds 8h8s (top set) on 8d7c3h facing a bet from CO and a cold-call from BTN. With 90.5% equity, better_hand_pct of 0.00 (nothing in the combined range beats top set on this board), and SPR of 0.50 (stacks are near-committed), hero must raise to get all the money in immediately. Sets must never slowplay 3-way — two opponents in the field means the combined draw range is wide (any 9/6/5/4 makes straights, plus pair+draw combos), and the SPR means a raise simply completes the stack commitment that calling would also effectively produce anyway. RAISE is the unambiguous action.

---

REF_ID: MW-34
ACTION: BET
CONFIDENCE: HIGH
REASONING: Hero holds AcAd (overpair) IP as CO opener on a dry J94r board. Both opponents checked — villain_aggression_count is 0 and villain_checked_back applies — with villain_air_pct 0.44 (high) and villain_range_capped 1 (both callers are capped, no premium overpairs in their ranges). Equity is 66.80% with better_hand_pct only 0.05 (only sets of JJ/99/44 beat hero). IP position, both opponents showing weakness, capped villain ranges, high air, near-nut equity, and a dry static board all align to support a value bet; no factors conflict and the decision is clear.

---

REF_ID: MW-35
ACTION: CALL
CONFIDENCE: HIGH
REASONING: Hero holds QcJd (top pair second kicker) IP as BTN facing a single CO bet of 9 into 27 (pot odds 25%). Equity is 53.33% — substantially above the 25% pot odds — and villain_range_capped is 0 (CO is uncapped and can have AQ, KQ, QQ that dominate), making raising thin. With SPR 3.70 there are meaningful streets ahead; calling preserves position and pot control without over-committing with TPSK against an uncapped range that includes dominating hands. No bet-and-call signal is present (num_callers_to_bet 0), so the range-narrowing override does not apply and equity comfortably clears the pot odds threshold.

---

REF_ID: MW-36
ACTION: CALL
CONFIDENCE: MEDIUM
REASONING: Hero holds QcJd (top pair second kicker) IP as BTN facing a CO bet of 33 into 90 (pot odds 26.83%) with SPR 1.11. Equity at 52.82% comfortably exceeds pot odds, and no bet-and-call signal is present (num_callers_to_bet 0), so range-narrowing override does not apply. The compressed SPR means that raising is effectively a stack-off with TPSK against CO's uncapped range — too aggressive with a medium-strength hand. Calling is the correct line: equity clears pot odds with position intact, and the low SPR means the decision resolves quickly on the turn without further difficult decisions on multiple streets.
