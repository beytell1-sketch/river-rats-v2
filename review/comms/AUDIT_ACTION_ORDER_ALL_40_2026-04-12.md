# Action Order Audit — FB-01 through FB-40
**Date:** 2026-04-12
**Author:** Auditor (Architecture Expert)
**Status:** FINAL
**Scope:** All 40 facing-bet situations from the FB test set

---

## Methodology

For each situation, the following rule was applied:

**Postflop action order:** SB → BB → UTG → HJ → CO → BTN (left of dealer first, dealer last). After any player bets, remaining players respond in the SAME positional order, continuing clockwise from the bettor and wrapping around.

**Key implication for all three-way pots:** When BTN bets in a BB/CO/BTN or BB/CO/BTN structure, the action going clockwise from BTN hits BB first, then CO. Therefore CO is LAST (closing action) — not sandwiched. The error described in the brief is the reverse: BB is classified as closing action when it is actually sandwiched, or CO is classified as sandwiched when it is actually last.

For each situation, I traced:
1. The preflop positions and opener (determines postflop seat order)
2. The action sequence on the relevant street
3. After the bet: who acts first, who acts second (clockwise from bettor)
4. Whether hero's stated position in the sequence matches reality

---

## Summary Table

| FB | Hero | Bettor | Positions | Claimed classification | Actual classification | Action order correct? | Sandwich correct? | Label impact |
|----|------|--------|-----------|----------------------|---------------------|----------------------|-------------------|--------------|
| FB-01 | BB | CO | BB/CO/BTN | Sandwich (BTN behind) | Sandwich (BTN behind) | YES | YES | — |
| FB-02 | BTN | BB | BB/CO/BTN | Closing action | Closing action | YES | YES | — |
| FB-03 | BB | CO | BB/CO/BTN | Closing (bet-and-call) | Closing (bet-and-call) | YES | YES | — |
| FB-04 | BB | CO | BB/CO/BTN | Sandwich (BTN behind) | Sandwich (BTN behind) | YES | YES | — |
| FB-05 | BTN | CO | BB/CO/BTN | Closing action | Closing action | YES | YES | — |
| FB-06 | BB | CO | BB/CO/BTN | Sandwich (BTN behind) | Sandwich (BTN behind) | YES | YES | — |
| FB-07 | CO | BB | BB/CO/BTN | Sandwich (BTN behind) | Sandwich (BTN behind) | YES | YES | — |
| FB-08 | CO | BB | BB/CO/BTN | Sandwich (BTN behind) | Sandwich (BTN behind) | YES | YES | — |
| FB-09 | BTN | CO | BB/CO/BTN | Closing action | Closing action | YES | YES | — |
| FB-10 | BB | CO | BB/CO/BTN | Sandwich (BTN behind) | Sandwich (BTN behind) | YES | YES | — |
| FB-11 | BTN | BB | BB/CO/BTN | Closing action | Closing action | YES | YES | — |
| FB-12 | BB | BTN | BB/CO/BTN | Closing action | Closing action | YES | YES | — |
| **FB-13** | **CO** | **BTN** | **BB/CO/BTN** | **Sandwich (BB behind)** | **Closing action** | **NO** | **NO** | LOW |
| FB-14 | BTN | BB | BB/CO/BTN | Closing action | Closing action | YES | YES | — |
| FB-15 | BB | CO | BB/CO/BTN | Sandwich (BTN behind) | Sandwich (BTN behind) | YES | YES | — |
| FB-16 | BB | CO | BB/CO/BTN | Closing (bet-and-call) | Closing (bet-and-call) | YES | YES | — |
| FB-17 | BB | CO | BB/CO/BTN | Sandwich (BTN behind) | Sandwich (BTN behind) | YES | YES | — |
| FB-18 | BTN | CO | BB/CO/BTN | Closing action | Closing action | YES | YES | — |
| **FB-19** | **BB** | **BTN** | **BB/CO/BTN** | **Closing action** | **Sandwich (CO behind)** | **NO** | **NO** | NONE |
| FB-20 | CO | BTN | BB/CO/BTN | Closing action (BB out) | Closing action (BB out) | YES | YES | — |
| **FB-21** | **BB** | **CO** | **BB/CO/BTN** | **Closing action** | **Sandwich (BTN behind)** | **NO** | **NO** | NONE |
| FB-22 | CO | BTN | BB/CO/BTN | Closing (bet-and-call) | Closing (bet-and-call) | YES | YES | — |
| FB-23 | BB | CO | BB/CO/BTN | Closing action (BTN out) | Closing action (BTN out) | YES | YES | — |
| FB-24 | BTN | BB | BB/CO/BTN | Closing action (CO out) | Closing action (CO out) | YES | YES | — |
| FB-25 | BB | CO | BB/CO (2-way) | Closing action (2-way) | Closing action (2-way) | YES | YES | — |
| FB-26 | BTN | BB | BB/CO/BTN | Closing action (CO out) | Closing action (CO out) | YES | YES | — |
| FB-27 | BB | CO | BB/CO/BTN | Sandwich (BTN behind) | Sandwich (BTN behind) | YES | YES | — |
| FB-28 | BB | CO | BB/CO/BTN | Closing (bet-and-call) | Closing (bet-and-call) | YES | YES | — |
| FB-29 | CO | BB | BB/CO/BTN | Sandwich (BTN behind) | Sandwich (BTN behind) | YES | YES | — |
| FB-30 | BTN | CO | BB/CO/BTN | Closing action (BB out) | Closing action (BB out) | YES | YES | — |
| FB-31 | BTN | BB | BB/CO/BTN | Closing action (CO out) | Closing action (CO out) | YES | YES | — |
| FB-32 | BTN | CO | BB/CO/BTN | Closing (bet-and-call) | Closing (bet-and-call) | YES | YES | — |
| FB-33 | BB | BTN | BB/CO/BTN | Closing (bet-and-call) | Closing (bet-and-call) | YES | YES | — |
| FB-34 | BB | BTN | BB/CO/BTN | Closing (bet-and-call) | Closing (bet-and-call) | YES | YES | — |
| **FB-35** | **CO** | **BTN** | **BB/CO/BTN** | **Sandwich (BB behind)** | **Closing action** | **NO** | **NO** | LOW |
| FB-36 | CO | BTN | BB/CO/BTN | Closing action (BB out) | Closing action (BB out) | YES | YES | — |
| FB-37 | CO | BTN | BB/CO/BTN | Closing action | Closing action | YES | YES | — |
| FB-38 | CO | BB | BB/CO/BTN | Sandwich (BTN behind) | Sandwich (BTN behind) | YES | YES | — |
| **FB-39** | **BB** | **BTN** | **BB/CO/BTN** | **Closing action** | **Sandwich (CO behind)** | **NO** | **NO** | LOW |
| FB-40 | BB | BTN | BB/CO/BTN | Sandwich (CO behind) | Sandwich (CO behind) | YES | YES | — |

---

## Detailed Findings for Each Error

---

### FB-13 — CO wrongly classified as sandwich

**Positions:** BTN opens, CO (hero) calls, BB calls.
**Postflop seat order:** BB → CO → BTN.

**Claimed action sequence (from spec):**
> "BB checks, BTN bets 45 into 90. Hero (CO) faces bet, BB yet to act."

**Why this is wrong:**
In the postflop order BB → CO → BTN, BTN acts last. For BTN to bet, both BB and CO must have already acted (checked). The spec says BB checks but omits CO checking — BTN cannot bet before CO has had their turn.

**Correct action sequence:**
> BB checks, CO checks, BTN bets 45 into 90. BB responds to bet (next clockwise from BTN = BB). Then CO responds.

After BTN bets, action proceeds clockwise: BTN → BB → CO. BB acts before CO. CO is the LAST player to act on this bet.

**Hero's actual position:** Closing action (CO is last to act, not sandwiched). BB acts first in response to BTN's bet, then CO.

**Sandwich or closing?** Closing action. The situation should be labelled as hero closing action (same as FB-12 which correctly identifies BB as closing action in a BTN-opens-CO-calls-BB-calls pot).

**Does the GTO label need to change?**
- Hero cards: 9c8c (gutshot + backdoor flush draw) on Th-Td-7c paired board.
- Labelled: FOLD (HIGH confidence)
- The fold reasoning cited equity of 15-18% against the 25% pot odds, plus the sandwich penalty. Without the sandwich, equity is still 15-18% vs 25% required — hero is below pot odds regardless.
- **Label verdict: FOLD stands. Confidence upgrades from implied-sandwich reasoning to simple equity-insufficient reasoning. Label unchanged, reasoning improves.**
- **Impact: LOW** — the label is correct but the stated reasoning (sandwich tightening) was partially wrong. The primary reason to fold is insufficient equity, which holds independently.

---

### FB-19 — BB wrongly classified as closing action

**Positions:** CO opens, BTN calls, BB (hero) calls.
**Postflop seat order:** BB → CO → BTN.

**Claimed action sequence (from spec):**
> "Turn Qc: BB checks, CO checks, BTN bets 90 into 150."
> Classification: "third player (CO) already checked" — implying CO is done.

**Why this is wrong:**
CO checking before BTN bets is CO's initial action in the checking order (BB → CO → BTN all checked). Once BTN bets, CO has NOT yet responded to that bet. Checking is not equivalent to folding — a player who checks can still call, raise, or fold when a later player bets. After BTN bets, the remaining players must act in clockwise order from BTN: BB first, then CO. CO is still live and acts after BB.

**Correct action sequence:**
> Turn: BB checks, CO checks, BTN bets 90. Action to BB (hero) — then action to CO (who has only checked, not acted on this bet).

After BTN bets: BTN → BB(hero) → CO. BB acts first, CO acts after.

**Hero's actual position:** Sandwich (CO is behind and must act after hero).

**Does the GTO label need to change?**
- Hero cards: 7h5h (7-high flush draw, two hearts on Kh-6h-3d-Qc turn).
- Labelled: FOLD (HIGH confidence)
- Reasoning: 9 flush outs → ~18% equity on one card, pot odds require 27%, equity below pot odds. Fold is correct before any positional discount.
- Even if hero is sandwiched, the fold is correct: equity is below pot odds, the draw is non-nut (7-high flush loses to any opponent with a higher heart), and OOP position further discounts realization.
- **Label verdict: FOLD stands. Impact: NONE.** The label is correct regardless of position classification.

---

### FB-21 — BB wrongly classified as closing action (impossible action sequence)

**Positions:** CO opens, BTN calls, BB (hero) calls.
**Postflop seat order:** BB → CO → BTN.

**Claimed action sequence (from spec's Revised note):**
> "Turn Jd: BB checks, BTN checks, CO bets 45. Hero faces bet, closes action."

**Why this is wrong:**
In a CO-opens, BTN-calls, BB-calls pot, the postflop order is BB → CO → BTN. CO acts between BB and BTN. The sequence "BB checks, BTN checks, CO bets" is impossible — BTN cannot act before CO in this positional order. The spec has the turn action sequence inverted for CO and BTN.

**Correct action sequence:**
Option A (CO bets and BTN still to act):
> Turn: BB checks, CO bets 45. BTN has not yet acted. Hero (BB) is sandwiched with BTN behind.

Option B (CO bets after everyone checks):
> Turn: BB checks, CO checks, BTN checks... but then CO would not be the bettor.

If CO is the bettor and BB has not yet responded to the bet, the only valid sequence for BB to close action is if BTN folds after CO bets. The spec did not specify BTN folding — it said "BTN already checked" which is positionally impossible before CO's bet.

**Hero's actual position:** Sandwich (BTN behind, in the correct sequence where CO bets and BTN hasn't yet acted). If the spec intends CO to be the bettor, BTN is still to act after CO bets, and BB is sandwiched.

**Does the GTO label need to change?**
- Hero cards: 5c5d (pocket fives, underpair on Ts-8c-4h-Jd board).
- Labelled: FOLD (HIGH confidence)
- Reasoning: ~8-10% equity against CO's delayed c-bet range representing hands that connected with the J turn. Pot odds require 25%.
- Being sandwiched or closing makes no difference — hero's equity is catastrophically below pot odds. No action change.
- **Label verdict: FOLD stands. Impact: NONE.**

---

### FB-35 — CO wrongly classified as sandwich

**Positions:** BTN opens, CO (hero) calls, BB calls.
**Postflop seat order:** BB → CO → BTN.

**Claimed action sequence (from spec):**
> "Turn Qc: BB checks, BTN bets 90 into 150. Hero (CO) faces bet, BB yet to act."

**Why this is wrong:**
Same structural error as FB-13. In a BTN-opens pot, postflop order is BB → CO → BTN. After BTN bets, the next player clockwise from BTN is BB. After BB acts, CO acts. CO is the last player to respond to BTN's bet.

The spec claims "BB yet to act behind hero" but in reality BB acts BEFORE CO in response to BTN's bet.

**Correct action sequence:**
> Turn: BB checks, CO checks, BTN bets 90 into 150. BB acts (next clockwise from BTN). CO acts after BB.

Hero (CO) is LAST to act. This is closing action, not a sandwich.

**Does the GTO label need to change?**
- Hero cards: Kd9d (top pair weak kicker K9 on Kh-6h-3d-Qc board).
- Labelled: FOLD (MEDIUM confidence)
- Stated reasoning heavily cited the sandwich penalty: "sandwich player must fold ~80%" per KB Section 1.5. The agent used sandwich position as the primary justification for tipping a marginal spot toward fold.
- **Without the sandwich:** Hero is closing action. BB has already checked (and will respond to BTN's bet before CO). If BB folds (likely against a 60%-pot bet from BTN after calling the flop), hero is now heads-up in position relative to BTN — but hero is OOP as CO facing BTN. K9 is top pair with weak kicker on K-Q board facing BTN's second barrel. This is still probably a fold against a strong range, but the confidence should be lower and the call could be defensible for a solver mix spot.
- **Label verdict: FOLD likely still correct but confidence should drop from MEDIUM to LOW. The primary justification (sandwich squeeze risk) was wrong. The hand might be a solver mix fold/call when hero closes action.**
- **Impact: LOW** — The label probably survives but the reasoning was substantially wrong and the confidence was inflated by the incorrect sandwich classification.

---

### FB-39 — BB wrongly classified as closing action

**Positions:** CO opens, BTN calls, BB (hero) calls.
**Postflop seat order:** BB → CO → BTN.

**Claimed action sequence (from spec):**
> "River Jh: BB checks, CO checks, BTN bets 90 into 150. Hero closes action."

**Why this is wrong:**
Same structural error as FB-19. CO checking before BTN bets is CO's initial pass in the checking sequence. It does not close CO's action. After BTN bets, action goes clockwise from BTN: BB (hero) acts first, CO acts second. CO is still to act after hero.

**Correct action sequence:**
> River: BB checks, CO checks, BTN bets 90. Hero (BB) acts — then CO acts.

After BTN bets: BTN → BB(hero) → CO. Hero is the first to respond, CO is behind.

**Hero's actual position:** Sandwich (CO behind, not closing action).

**Does the GTO label need to change?**
- Hero cards: Qh8h (top two pair, queens and eights) on Qd-8d-4c-7s-Jh river.
- Labelled: CALL (HIGH confidence)
- Reasoning: top two pair vs river bet with many missed diamond flush draws in BTN's range.
- If hero is sandwiched, CO could squeeze behind. However: (a) CO has checked twice through the turn and river with no initiative — CO's range is capped and very unlikely to squeeze, (b) even if CO calls, hero's two pair is still strong value in a multiway pot with a missed draw board, (c) top two pair is firmly in hero's calling range even with a player behind.
- **Label verdict: CALL stands. Impact: LOW.** The hand is strong enough that CO's ability to act behind does not change the decision. However, the stated reasoning (hero closes action, no squeeze risk) was wrong, and the confidence should note the sandwich factor.

---

## Statistics

| Metric | Count |
|--------|-------|
| Total situations audited | 40 |
| Situations with action order errors | 5 |
| Situations with sandwich misclassification | 5 |
| Labels that might need to change | 0 (NONE impact) to 3 (LOW impact) |
| Situations where label flips (HIGH impact) | 0 |
| Clean situations (no errors) | 35 |

**Breakdown of label impact:**
- NONE (label correct regardless): FB-19, FB-21 (2 situations)
- LOW (label probably correct, reasoning/confidence affected): FB-13, FB-35, FB-39 (3 situations)
- HIGH (label might flip): 0 situations

---

## Categorization of Errors

### Pattern A: CO wrongly claimed as sandwich when CO is actually last to act after BTN bets

In a BTN-opens (or any pot where BTN is the bettor), after BTN bets, the clockwise order is BTN → BB → CO. CO is last, not sandwiched. BB acts before CO.

- **FB-13:** BTN opens, CO calls, BB calls. BTN bets. Spec says "BB yet to act behind CO." Actual: BB acts before CO. CO is last.
- **FB-35:** BTN opens, CO calls, BB calls. BTN bets. Spec says "BB yet to act behind CO." Actual: BB acts before CO. CO is last.

### Pattern B: BB wrongly classified as closing action when BB is actually sandwich (CO behind after BTN bets)

In a CO-opens (or any pot where the postflop order is BB → CO → BTN), when BTN bets, action wraps: BB acts first, CO acts second. CO checking before the bet does not remove CO from the action. BB is sandwiched with CO behind.

- **FB-19:** CO opens, BTN calls, BB calls. BTN bets turn. Spec says "CO already checked, hero (BB) closes action." Actual: CO must respond to BTN's bet. BB is sandwiched, CO behind.
- **FB-39:** CO opens, BTN calls, BB calls. BTN bets river. Spec says "CO checked, hero (BB) closes action." Actual: same as FB-19. BB is sandwiched, CO behind.

### Pattern C: Impossible action sequence (sequence violates positional order)

- **FB-21:** CO opens, BTN calls, BB calls. Spec says "BB checks, BTN checks, CO bets." This is impossible — CO acts before BTN in this pot structure. The sequence has CO and BTN swapped.

### Pattern D: None

No additional error patterns observed.

---

## Root Cause Analysis

Patterns A and B share the same root cause: **the architect treated a player's "check" in the initial checking round as closing their action for the entire street.** It does not. A check only means the player declines to bet; they retain the right to call, raise, or fold when a subsequent player bets.

The specific confusion:
- In Pattern B, the spec notes "CO already checked" when describing the turn/river sequence before BTN bets, then concludes BB closes action. This conflates the pre-bet check with post-bet action.
- In Pattern A, the spec fails to realize that in a BTN-opens pot, after BTN bets, the action wraps to BB first (because BB is next clockwise after BTN), not to CO.

Pattern C is a transcription error — the action sequence in the spec note has CO and BTN's positions in the checking sequence reversed.

All 5 errors are design/spec errors, not labelling errors. The GTO Experts correctly applied the situation as described; the situations themselves were misspecified.

---

## Appendix: Correct Sandwich Logic Reference

For a three-way pot with positions BB, CO, BTN:

| Bettor | Clockwise order after bet | Who is sandwiched? |
|--------|--------------------------|-------------------|
| BB (donk bet) | CO responds, then BTN | CO is sandwiched (BTN behind) |
| CO (c-bet or delayed) | BTN responds, then BB wraps | BTN is sandwiched (BB behind)* |
| BTN (from position) | BB responds, then CO | BB is sandwiched (CO behind) |

*In practice BTN is rarely hero since BTN is the common bettor. But the structure holds.

**Summary for preflop openers:**
- CO opens, BTN calls, BB calls → order BB → CO → BTN → after CO bets: BTN acts, then BB (BB is last = closes action OR BB is sandwiched only if a fourth player exists)
- CO opens, BTN calls, BB calls → after BTN bets: BB acts, then CO (BB is sandwiched, CO is last)
- BTN opens, CO calls, BB calls → after BTN bets: BB acts, then CO (BB is sandwiched, CO is last)

**The counterintuitive case:** In a BTN-opens pot, BB is in the worst sandwich position (between BTN's bet and CO's response), not CO. The spec errors in FB-13 and FB-35 both incorrectly placed CO in the sandwich when CO is actually last.
