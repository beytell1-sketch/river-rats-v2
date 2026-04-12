# Review: Facing-Bet 3-Way Test Set (40 Situations)

**Date:** 2026-04-12
**Reviewer:** Independent Reviewer
**Files reviewed:**
- `review/comms/ML_ARCHITECT_FACING_BET_TEST_SET_2026-04-12.md`
- `review/comms/GTO_EXPERT_AGENT1_FB01_FB10_2026-04-12.md`
- `review/comms/GTO_EXPERT_AGENT2_FB11_FB20_2026-04-12.md`
- `review/comms/GTO_EXPERT_AGENT3_FB21_FB30_2026-04-12.md`
- `review/comms/GTO_EXPERT_AGENT4_FB31_FB40_2026-04-12.md`

---

## Audit Summary

| Check | Result | Issues found |
|---|---|---|
| Card conflicts | PASS | 0 |
| Action consistency | PASS | 0 |
| Batch 4 overlap | PASS | 0 |
| Reference set overlap | PASS | 0 |
| Axis coverage | FAIL | 2 deviations (street distribution, position distribution) |
| Label quality | FAIL | 2 issues |
| Poker red flags | FAIL | 1 critical, 1 minor |
| Cross-agent consistency | FAIL | 2 issues |

---

## Check 1: Card Conflicts

All 40 situations verified. Every hero card pair was checked against its board for exact suit+rank match. No conflicts found.

**Result: PASS**

---

## Check 2: Action Consistency

All 40 situations have `facing_bet=True` with a live bet in the action history. Every FOLD has a bet to fold to, every CALL has a bet to call, every RAISE has a bet to raise over. Action histories are consistent with the stated pot/bet/call amounts.

**Result: PASS**

---

## Check 3: Batch 4 Overlap

All 13 boards verified against the 25 Batch 4 boards listed in the ML architect spec. No 3-card flop match found.

**Result: PASS**

---

## Check 4: Reference Set Overlap

All 13 boards verified against MW-11 through MW-50 boards listed in the ML architect spec. No match found.

**Result: PASS**

---

## Check 5: Axis Coverage

### Street Distribution

| Street | Target | Actual | Deviation |
|--------|--------|--------|-----------|
| Flop | 20 (50%) | 26 (65%) | +6 over target |
| Turn | 12 (30%) | 8 (20%) | -4 under target |
| River | 8 (20%) | 6 (15%) | -2 under target |

Actual flop situations: FB-01 through FB-16, FB-22, FB-27 through FB-34, FB-40 = 26.
Actual turn situations: FB-17 through FB-21, FB-35 through FB-37 = 8.
Actual river situations: FB-23 through FB-26, FB-38, FB-39 = 6.

The flop is significantly overweight at 65% vs the 50% target. Turn and river are both underweight. This skews the test set toward flop decisions and underrepresents later-street situations where accumulated action signals and narrowed ranges test different model capabilities.

### Position Distribution

| Position | Target | Actual | Deviation |
|----------|--------|--------|-----------|
| OOP (non-sandwich) | 18 (45%) | 15 (37.5%) | -3 |
| IP (closing action) | 14 (35%) | 11 (27.5%) | -3 |
| Sandwich | 8 (20%) | 14 (35%) | +6 over target |

Sandwich situations (hero with a player yet to act behind): FB-01, FB-04, FB-06, FB-07, FB-08, FB-10, FB-13, FB-15, FB-17, FB-27, FB-29, FB-35, FB-38, FB-40 = 14.

Sandwich is overweight by 75% relative to target (14 vs 8). While the architect spec noted sandwich gets "disproportionate coverage," 35% is nearly double the 20% target and comes at the expense of both OOP and IP coverage.

**Result: FAIL — street and position distributions deviate significantly from target.**

**Recommended fix:** Either (a) acknowledge the deviation as intentional and update the target spec to match, or (b) reassign 4-6 situations to turn/river and rebalance sandwich/IP/OOP counts. Option (a) is acceptable if the rationale is documented — the overweight sandwich coverage is defensible as a stress-test. The flop overweight is harder to justify since the spec explicitly weighted turn/river to test "accumulated action signals."

---

## Check 6: Label Quality

### Label Distribution (acceptable)

| Label | Count |
|-------|-------|
| CALL | 17 |
| FOLD | 15 |
| RAISE | 8 |

Good variety across all three actions.

### Issues Found

#### FB-37 — Confused reasoning process

Agent 4's reasoning for FB-37 (Qh Ts on Ac Jh 5d Ks) contains a visible stream-of-consciousness working-through where the agent initially questions whether hero has a straight, talks itself in circles ("hero needs a specific card — no wait"), and eventually arrives at the correct conclusion (hero has the nut Broadway straight AKQJT). While the final answer is correct, the published reasoning reads as uncertain and unpolished. A test set label should present clean, confident reasoning. The internal debate should be resolved before the label is written, not visible in the final output.

**Recommended fix:** Rewrite FB-37 reasoning to state cleanly that hero has the nut straight (A-K-Q-J-T: Q and T from hand, A-K-J from board) and then justify the CALL vs RAISE decision without the visible working process.

#### FB-15 — Folding the nut flush draw in sandwich needs stronger justification

Agent 2 folds Ad3h (nut flush draw with the Ad) on 9d 7d 2c from the sandwich seat. The reasoning acknowledges equity (~28-32%) exceeds pot odds (25% by their formula) by more than 5pp but folds based on OOP sandwich EQR discount. This is a defensible but aggressive fold. The agent correctly flags it for solver verification. The issue is that the reasoning does not quantify the EQR discount precisely enough to justify folding a hand where raw equity exceeds pot odds by 3-7pp. The KB says EQR is "60-80%" for OOP — at the worst case (60% EQR), realized equity would be 0.60 * 30% = 18%, which is below 25% pot odds. This math should be shown explicitly.

**Recommended fix:** Add explicit EQR math to FB-15 reasoning: "Even at 30% raw equity, OOP-sandwich EQR of ~60% yields ~18% realized equity, below the 25% pot odds threshold."

**Result: FAIL — 2 issues requiring fixes.**

---

## Check 7: Poker Red Flags

### FB-34 — CRITICAL: Agent misidentifies nut flush as second-nut flush

Hero holds Ks 6s on board As 9s 4s (monotone spades). Agent 4 states: "Hero holds the second-nut flush (Ks-high flush)" and "only beaten by As-Xs (nut flush)."

This is wrong. The As is ON THE BOARD. No opponent can hold the As. Hero's Ks is the highest possible spade any player can hold. Hero has the NUT flush (As-Ks-9s-6s-4s), not the second-nut flush. No hand in any opponent's range can beat hero's flush except a full house (44, 99) or quads (impossible).

The label (RAISE) is still correct — raising is even more clearly right with the nut flush than the second-nut flush. But the reasoning is fundamentally flawed. If this label is used to evaluate a model, the reasoning would mislead any human auditor or future reference.

**Recommended fix:** Rewrite FB-34 reasoning. Hero has the NUT flush. Remove all references to "second-nut" and "only beaten by As-Xs." Update the reasoning to note that hero is beaten only by full houses (44 = 3 combos, 99 = 3 combos) and adjust equity estimate upward. The RAISE label remains correct.

### FB-32 — Minor: "heart backdoor that cannot materialize on a rainbow board"

Agent 4 says hero (Ah 4h) has a "heart backdoor that cannot materialize on a rainbow board" on Jd 8s 6h. The board has 6h — one heart. A backdoor flush draw (two running hearts) is technically possible, though extremely unlikely. The phrasing is slightly inaccurate but the fold is clearly correct regardless. This is cosmetic.

**Recommended fix:** Change to "heart backdoor requiring two running hearts, providing negligible equity."

**Result: FAIL — 1 critical error (FB-34), 1 minor (FB-32).**

---

## Check 8: Cross-Agent Consistency

### Issue 1: Pot odds formula inconsistency between Agent 3 and Agents 1/2/4

Agents 1, 2, and 4 consistently use the formula: `call / (pot + bet + call)`.
Agent 3 consistently uses: `call / (pot + bet)`.

Examples:
- FB-21 (Agent 3): 45/(90+45) = 33%, vs Agents 1/2/4 formula: 45/(90+45+45) = 25%
- FB-27 (Agent 3): 30/(90+30) = 25%, vs other formula: 30/(90+30+30) = 20%
- FB-29 (Agent 3): 45/(90+45) = 33%, vs other formula: 45/(90+45+45) = 25%
- FB-30 (Agent 3): 60/(90+60) = 40%, vs other formula: 60/(90+60+60) = 28.6%

Both formulas are valid poker conventions (Agent 3's is the traditional "pot odds" ratio; Agents 1/2/4 use the "equity needed to call" ratio). However, using different conventions across the same test set creates confusion. When the ML architect spec lists pot odds, it uses Agent 3's convention (e.g., FB-01 spec says 25% while Agent 1 calculates 20%).

No decisions are changed by this — Agent 3's reasoning compares equity against their own stated threshold. But the inconsistency means the test set cannot be used to validate pot odds calculations without normalizing the formula first.

**Recommended fix:** Standardize all 40 situations to use one formula. Recommend `call / (pot + bet + call)` (the equity-needed-to-call formula) as it is the more common standard in solver-based GTO analysis. Recalculate Agent 3's pot odds (FB-21 through FB-30) and verify reasoning still holds.

### Issue 2: FB-17 vs FB-37 — Same hand, same board, different labels

FB-17 (Agent 2): Hero Qh Td on Ac Jh 5d Ks. BB (OOP, sandwich). Label: **RAISE**.
FB-37 (Agent 4): Hero Qh Ts on Ac Jh 5d Ks. CO (OOP, closes action). Label: **CALL**.

Both heroes have the nut Broadway straight. The hands are functionally identical (Td vs Ts is irrelevant on this board). The position difference (sandwich vs closes-action) is a legitimate reason for different actions. Agent 2 argues the nuts should always raise; Agent 4 argues for slowplay when closing action.

This is not necessarily wrong — solver output on nut hands does show mixed strategies in some spots. However, having two contradictory labels for the same hand on the same board in a test set creates an ambiguity: which is "correct"? If a model predicts RAISE on FB-37, is it wrong? If it predicts CALL on FB-17, is it wrong?

**Recommended fix:** Either (a) harmonize the labels (RAISE for both, since the standard GTO line with the nuts in a multiway pot is to raise for value and protection), or (b) explicitly document in the test set metadata that FB-17 and FB-37 represent a position-dependent split where both CALL and RAISE are acceptable, and model scoring should accept either on these two situations.

**Result: FAIL — 2 cross-agent consistency issues.**

---

## Per-Situation Findings

Only situations with issues are listed below. All others are CLEAN.

### FB-15 — LABEL QUALITY: Nut flush draw fold needs explicit EQR math
See Check 6 above. Add quantified EQR discount to justify folding when raw equity exceeds pot odds.

### FB-17 vs FB-37 — CROSS-AGENT: Same nut straight, contradictory labels
See Check 8, Issue 2. Harmonize or document as position-dependent acceptable split.

### FB-34 — CRITICAL POKER ERROR: Nut flush misidentified as second-nut
Hero has the nut flush (Ks on board with As already out). Agent 4 calls it "second-nut." Reasoning claims hero is "beaten by As-Xs" which is impossible since As is on the board. Rewrite reasoning entirely. Label (RAISE) is correct.

### FB-37 — LABEL QUALITY: Messy stream-of-consciousness reasoning
Agent 4 visibly works through whether hero has a straight in the published reasoning. Clean up to present confident, resolved analysis.

### FB-32 — MINOR: Inaccurate claim about backdoor impossibility
Board has 6h, so backdoor heart flush is possible (not impossible). Cosmetic fix.

---

## Systematic Issues (not per-situation)

### S1: Street distribution deviation
26 flop / 8 turn / 6 river vs target 20/12/8. Need 6 more turn and 2 more river situations, or spec update.

### S2: Position distribution deviation
14 sandwich / 11 IP / 15 OOP vs target 8/14/18. Sandwich is 75% over target.

### S3: Pot odds formula inconsistency
Agent 3 uses a different formula from Agents 1, 2, and 4. Standardize across all 40 situations.

---

## Verdict

**APPROVED WITH FIXES**

The test set is fundamentally sound: no card conflicts, no overlap with existing sets, good label variety (17 CALL / 15 FOLD / 8 RAISE), solid reasoning quality across 36 of 40 situations, and good board texture coverage. The four issues requiring fixes are:

1. **FB-34 reasoning rewrite (CRITICAL):** Nut flush, not second-nut. Must fix before use.
2. **FB-37 reasoning cleanup:** Remove stream-of-consciousness, present clean analysis.
3. **Pot odds formula standardization:** Pick one formula, apply across all 40 situations.
4. **FB-17/FB-37 label harmonization or documentation:** Resolve the contradictory labels for the same hand on the same board.

The axis coverage deviations (street and position) should be acknowledged in the test set metadata. The overweight sandwich coverage is defensible; the flop overweight less so. If adding 4 turn and 2 river situations is feasible, that would bring the set to 46 and fix the distribution. Otherwise, document the deviation and note it when interpreting model scores.

None of these issues block the test set from being used — they require targeted fixes that do not invalidate the broader design. After the 4 fixes above are applied, this test set is ready for deployment as the second evaluation axis.
