# Review: Semi-Bluff Sweeps Design (54 Situations)

**Reviewer:** Independent reviewer agent
**Date:** 6 April 2026
**Status:** CHANGES REQUESTED

---

## 1. Card Conflicts

**One hand category error (not a card conflict, but a data error):**
Board 5 (7s 6s 5d), Hand 3: 9s 8s is labelled "middle_pair (5)" at ~0.52 equity. Hero actually has a made straight (9-8-7-6-5). This must be corrected to "straight" with equity ~0.85+. As written, this hand trains the model that a flopped straight is a marginal semi-bluff candidate, which is dangerous.

No card-on-card conflicts found. All 54 hero holdings are clean against their respective boards.

## 2. Board Diversity

Good coverage of two-tone (Boards 1, 2, 3), monotone-on-turn (Board 4), connected (Board 5), and dual-draw (Board 6). However, the design explicitly excludes paired boards (citing Section 1.7). The research finding that "SPR < 1.0 collapses semi-bluff frequency" is also unrepresented. No board tests the SPR-collapsed scenario where hero holds a nut draw but the correct action shifts from RAISE to CALL/FOLD due to commitment math. This is a gap worth one board.

## 3. Hand Spectrum Quality

Strong. Each board includes the blocker/no-blocker contrast (e.g., Board 1: AsQs vs 8s7s), nut/non-nut ladder (Board 1: AsQs > Qs Ts > Ts9s > 9s8s), and made-hand contrast anchors. The IP/OOP split (2 IP boards, 4 OOP) matches the research finding that IP raises 3x more -- the model needs more OOP examples to learn the tighter threshold. Board 6 testing dual-suit blockers (Ah vs Ad) is a strong design choice grounded in Section 1.8.

## 4. Missing Spots

- **SPR-collapsed semi-bluff.** The researcher flagged SPR < 1.0 as collapsing semi-bluff frequency. No board tests this. Recommend adding one turn board with ~0.8 SPR where hero has a nut flush draw + blocker but the correct action is CALL (not RAISE) due to pot commitment.
- **Paired two-tone board.** The design excludes these per Section 1.7, which is defensible. However, one paired board where the model must learn NOT to semi-bluff (all draws demoted to check/call) would be valuable negative training data.

## 5. Overlap with Existing 348

Board 1 (Ks Jd 5s) with AsQs is identical to Worked Example 9, which was already used in the knowledge base and likely in the existing training set. If that exact board+hand exists in the 348, Hand 1 of Board 1 is a duplicate. The remaining 53 situations appear to use novel board textures. Verify Board 1 Hand 1 against the training CSV before export.

## 6. Integration with 260-Situation Plan

54 semi-bluff spots vs 50 budgeted = 4 over budget. Minor, but if the Board 5 Hand 3 correction removes a "semi-bluff" (it is a made hand), the count drops to 53, closer to target. The remaining 206 slots (45 flush-blocking + 40 overcard + 35 thin value + 90 general) have adequate room. The ML Architect's 73% turn/river target is not met by this sub-batch (only 2 of 6 boards are turn), but the other categories can compensate. The 10% RAISE rebalancing target is achievable -- roughly 5-6 of these 54 should label as RAISE (the blocker+nut draw hands), which is ~11%.

## Verdict

Fix the Board 5 Hand 3 category error. Consider adding one SPR-collapsed board. Verify Board 1 Hand 1 against existing training data. Otherwise, this is a well-structured design that faithfully implements Section 1.7 and 1.8.
