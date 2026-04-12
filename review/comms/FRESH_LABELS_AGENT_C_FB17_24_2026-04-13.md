# Fresh Labels — Agent C — FB-17 through FB-24
**Date:** 2026-04-13
**Author:** GTO Expert (Agent C)
**Scope:** FB-17, FB-18, FB-19, FB-20, FB-21, FB-22, FB-23, FB-24
**Target distribution:** 3 CALL / 3 FOLD / 2 RAISE

---

## FB-17 — CALL

**Board:** Ac Jh 5d Ks (turn)
**Validated action:** `BB check, CO bet 60, BTN fold, BB ???`
**Hero:** BB — OOP-CLOSING (REDESIGN_12: BTN folds before hero)
**Bettor:** CO (delayed c-bet, checked flop)
**Pot:** 90 | **Bet:** 60 | **To call:** 60 | **Pot odds:** 60/(90+60+60) = 29%

**Hero cards:** Kc Jd

**Hand strength:** Two pair (Kings and Jacks). Ks on the turn gives hero top two pair on A-K-J-5. This is a strong made hand.

**Reasoning:**
- Hero flopped second pair (Jacks) with Kc Jd and checked through on an A-high flop where CO (the PFA) also checked, signaling CO likely does not have a strong Ace.
- Turn Ks gives hero Kings and Jacks — two pair on A-K-J-5.
- CO's delayed c-bet on the Ks turn is consistent with: Kx hands that just improved, AQ/AT that decided to bet, or some missed draws taking a stab. CO's range is NOT heavily weighted toward AK (would likely have bet flop).
- Hero's equity with two pair is approximately 70-80% against CO's delayed c-bet range.
- Pot odds require 29%. Hero far exceeds this.
- RAISE consideration: Two pair is strong but on a dry A-K-J-5 board, raising folds out worse hands and gets called mainly by AK (which beats hero) or sets. The board is static — no draws to protect against. Calling keeps CO's bluffs and thin value bets in.
- OOP-closing means no squeeze risk from BTN.

**Label:** CALL
**Confidence:** HIGH

**Solver flags:** None.

---

## FB-18 — FOLD

**Board:** Ac Jh 5d Ks (turn)
**Validated action:** `BB check, CO bet 60, BTN ???`
**Hero:** BTN — first responder (BB acts after hero)
**Bettor:** CO (delayed c-bet)
**Pot:** 90 | **Bet:** 60 | **To call:** 60 | **Pot odds:** 60/(90+60+60) = 29%

**Hero cards:** 8h 7h

**Hand strength:** Air. No pair, no draw, no connection to A-K-J-5 board. Complete whiff.

**Reasoning:**
- Hero holds 8h 7h on Ac Jh 5d Ks — zero equity outside runner-runner. No straight draw, no flush draw (only one heart on the flop, two total on A-K-J-5 but hero needs three hearts on board for a backdoor and that ship has sailed on the turn).
- Equity is approximately 3-5% against any range CO would bet.
- Pot odds require 29%. Hero is nowhere close.
- BB still acts after hero, adding further risk if hero calls (BB could raise).
- Textbook fold with pure air on a board that completely missed hero's range.

**Label:** FOLD
**Confidence:** HIGH

**Solver flags:** None.

---

## FB-19 — FOLD

**Board:** Kh 6h 3d Qc (turn)
**Validated action:** `BB check, CO check, BTN bet 90, BB ???`
**Hero:** BB — SANDWICH (REDESIGN_12: CO still to act behind hero)
**Bettor:** BTN (turn bet after calling CO's flop c-bet)
**Pot:** 150 | **Bet:** 90 | **To call:** 90 | **Pot odds:** 90/(150+90+90) = 27%

**Flop action context:** CO opened, BTN called, BB called. Flop Kh 6h 3d: BB checked, CO bet 30, BTN called 30, BB called 30. Turn Qc: BB checks, CO checks, BTN bets 90 into 150.

**Hero cards:** Td 8d

**Hand strength:** Air. No pair, no draw on K-Q-6-3 two-tone (hearts). Hero holds diamonds — no flush draw on the heart board.

**Reasoning:**
- Hero has Td 8d on Kh 6h 3d Qc. No pair, no flush draw (wrong suit), no straight draw (T-8 needs a 9 and 7, but only a gutshot to 9 at best, and that's not present — T-9-8-7 needs 9 and 7 neither of which are on board; no open-ender).
- Equity is approximately 5-8% against BTN's turn betting range (BTN called a flop c-bet and now bets turn — strong line indicating Kx, Qx, flush draws, or two pair+).
- Pot odds require 27%. Hero is far below.
- SANDWICH position: CO is still live behind hero. Even if hero's equity were marginal, the sandwich EQR discount (~60% realization) would crush any borderline call.
- Clear fold with air in the worst positional spot.

**Label:** FOLD
**Confidence:** HIGH

**Solver flags:** None.

---

## FB-20 — CALL

**Board:** Kh 6h 3d Qc (turn)
**Validated action:** `CO check, BTN bet 90, CO ???`
**Hero:** CO — 2-way (BB folded earlier)
**Bettor:** BTN (turn bet)
**Pot:** 120 | **Bet:** 90 | **To call:** 90 | **Pot odds:** 90/(120+90+90) = 30%

**Action context:** BTN opens, CO (hero) calls, BB calls. Flop Kh 6h 3d: BB checks, CO checks, BTN bets 30, BB folds, CO calls. Turn Qc: CO checks, BTN bets 90 into 120.

**Hero cards:** Qd Jd

**Hand strength:** Second pair (Queens) with a Jack kicker on K-Q-6-3. Queen just arrived on the turn.

**Reasoning:**
- Hero called BTN's flop c-bet with overcards (QJ) and now turns second pair (Queens) on the Qc turn.
- Against BTN's double-barrel range: BTN's range includes Kx value (KT, KJ, KQ), AK, overpairs (AA), and some bluffs (missed suited connectors, heart draws). Hero beats all bluffs, Qx with worse kicker, and any remaining draws.
- Hero's equity is approximately 35-42% against BTN's turn barrel range. QJ is behind Kx hands but ahead of bluffs and heart draws that barrel.
- Pot odds require 30%. Hero's equity exceeds this threshold, especially heads-up with closing action.
- The Qc turn is a scare card that may slow BTN's bluff frequency, but BTN's continued aggression is consistent with a polarized range where hero's second pair is solidly in the calling range.
- RAISE is wrong: QJ second pair on a K-high board does not want to bloat the pot. Just calling realizes equity efficiently.

**Label:** CALL
**Confidence:** HIGH

**Solver flags:** None.

---

## FB-21 — RAISE

**Board:** Ts 8c 4h Jd (turn)
**Validated action:** `BB check, CO bet 45, BTN fold, BB ???`
**Hero:** BB — OOP-CLOSING (REDESIGN_12: BTN folds before hero)
**Bettor:** CO (delayed c-bet on turn after checked flop)
**Pot:** 90 | **Bet:** 45 | **To call:** 45 | **Pot odds:** 45/(90+45+45) = 25%

**Hero cards:** 9c 7c

**Hand strength:** The nuts. 9-7 makes a J-T-9-8-7 straight on the J turn. Stone cold nuts.

**Reasoning:**
- Hero holds 9c 7c on Ts 8c 4h Jd. The Jd turn completes the J-T-9-8-7 straight — the current nuts.
- CO's delayed c-bet on the Jd turn is consistent with: Jx that just paired, Tx that was trapping, overpairs, or AJ/KJ type hands. CO likely has a hand willing to put money in.
- With the nuts, hero must raise for value. The board has no flush draw (rainbow, four suits). If hero just calls, the river may bring a board pair (giving CO a full house if CO has a set) or another scare card. Raising now extracts maximum value.
- OOP-closing means no BTN squeeze risk behind — hero raises into CO heads-up.
- Section 1.7 default: "Only sets and the pure nuts are labelled RAISE" — hero has the pure nuts.

**Label:** RAISE
**Confidence:** HIGH

**Solver flags:** RAISE situation — flag for solver verification per protocol.

---

## FB-22 — CALL

**Board:** Ts 8c 4h (flop — FB-B10 flop portion only)
**Validated action:** `BB check, CO check, BTN bet 30, BB call 30, CO ???`
**Hero:** CO — CLOSING (bet-and-call pattern: BTN bet, BB called, CO acts last)
**Bettor:** BTN (IP c-bet on connected flop)
**Pot after BB call:** 150 (original 90 + BTN bet 30 + BB call 30) | **To call:** 30 | **Pot odds:** 30/(150+30) = 17%

**Action context:** BTN opens, CO (hero) calls, BB calls. Flop Ts 8c 4h: BB checks, CO checks, BTN bets 30, BB calls 30, CO faces bet-and-call.

**Hero cards:** Jc Tc

**Hand strength:** Top pair (Tens) with a Jack kicker on T-8-4 rainbow. Plus a backdoor club flush draw.

**Reasoning:**
- Hero holds Jc Tc — top pair with the second-best kicker possible (only AT is better). On a connected T-8-4 flop, this is a strong made hand.
- Bet-and-call pattern: BTN bet, BB called. BTN's range includes overpairs, Tx, 8x, draws (97, J9), and air. BB's calling range includes Tx, 8x, draws (97s, 65s), and some floats.
- Hero's top pair Jack kicker beats all 8x hands, all draws, and all Tx with worse kickers. Hero loses to overpairs (JJ+), sets (TT, 88, 44), and AT specifically.
- Equity is approximately 50-55% against the combined continuing ranges. Pot odds require only 17%. Hero easily exceeds this.
- The bet-and-call narrows ranges but hero's TPGK is firmly in the continuing range — this is the MW-30 pattern where equity far exceeds pot odds.
- RAISE consideration: JTcc has good equity but raising on a connected board inflates the pot and risks facing a 3-bet from BB's or BTN's strong holdings (sets, two pair). Section 1.7 default: non-set made hands default to CALL. The Jc provides no meaningful blocker to flush draws (rainbow board). CALL is correct.
- Hero closes action — no further players to worry about.

**Label:** CALL
**Confidence:** HIGH
**Flag:** MEDIUM confidence CALL (bet-and-call pattern with TPGK) — flag for solver per protocol.

---

## FB-23 — FOLD

**Board:** Ad 9c 3h 2s Kd (river)
**Validated action:** `BB check, CO bet 90, BTN fold, BB ???`
**Hero:** BB — CLOSING (REDESIGN_5: BTN folds to CO's river bet)
**Bettor:** CO (river bet after passive multi-street line)
**Pot:** 120 | **Bet:** 90 | **To call:** 90 | **Pot odds:** 90/(120+90+90) = 30%

**Action context:** CO opens, BTN calls, BB (hero) calls. Flop Ad 9c 3h: all check. Turn 2s: all check. River Kd: BB checks, CO bets 90 into 120. BTN folds. BB faces bet, closes action.

**Hero cards:** 7s 6s

**Hand strength:** Complete air. No pair, no draw (river — all draws are dead). 7-high on A-K-9-3-2 board.

**Reasoning:**
- Hero holds 7s 6s on Ad 9c 3h 2s Kd. Seven-high. No pair, no straight, no flush. Pure air on the river.
- CO bet 75% pot on the river after checking two streets. This is a delayed-aggression line consistent with: Kx that improved on river, Ax that was trapping/pot-controlling, slow-played two pair or set, or a polarized bluff. Regardless of CO's range composition, hero has 0% equity when called and cannot beat any value hand.
- Pot odds require 30%. Hero would need to believe CO is bluffing >30% of the time. Even if CO bluffs at a meaningful frequency on this passive line, hero has literally no showdown value — 7-high loses to every single hand in CO's range including other bluffs with a higher card.
- Closing action is irrelevant when hero has zero equity.

**Label:** FOLD
**Confidence:** HIGH

**Solver flags:** None.

---

## FB-24 — RAISE

**Board:** Ad 9c 3h 2s Kd (river)
**Validated action:** `BB bet 90, CO fold, BTN ???`
**Hero:** BTN — CLOSING (CO folded)
**Bettor:** BB (OOP river donk bet)
**Pot:** 120 | **Bet:** 90 | **To call:** 90 | **Pot odds:** 90/(120+90+90) = 30%

**Action context:** CO opens, BTN (hero) calls, BB calls. Flop Ad 9c 3h: all check. Turn 2s: all check. River Kd: BB donks 90 into 120. CO folds. Hero closes action.

**Hero cards:** Ad Kh

**Hand strength:** Top two pair (Aces and Kings) on A-K-9-3-2. The Kd river gives hero top two pair. This is a very strong hand on this runout.

**Reasoning:**
- Hero holds Ad Kh — flopped top pair (Aces) and rivered top two pair when the Kd hit. A-K on A-9-3-2-K is an extremely strong holding.
- BB's river donk bet into a pot that was checked through for two streets is a polarizing line. BB's range splits into: (a) slow-played monsters that finally bet (sets of 9s or 3s, A9, A3 two pair) and (b) bluffs or thin value (missed draws, weak Ax, random stabs after passive multi-street action).
- Hero's two pair beats all single-pair hands, all bluffs, and most of BB's value range (A9, A3). Hero only loses to 33 (set), 99 (set, unlikely — would have bet earlier), and the extremely rare A2 or 32 type hands.
- With top two pair, hero should raise for value. BB's donk-bet range includes enough Ax hands and bluffs that will either call a raise (Ax hands that think they're good) or be forced to fold (bluffs, giving hero the pot).
- IP closing action — raising is maximally effective in position with no players behind.
- Section 1.7: The nuts and near-nuts warrant RAISE. AK two pair is near-nuts on this board.

**Label:** RAISE
**Confidence:** HIGH

**Solver flags:** RAISE situation — flag for solver verification per protocol.

---

## Card Conflict Check

| FB | Board cards | Hero cards | Conflict? |
|---|---|---|---|
| FB-17 | Ac Jh 5d Ks | Kc Jd | No |
| FB-18 | Ac Jh 5d Ks | 8h 7h | No |
| FB-19 | Kh 6h 3d Qc | Td 8d | No |
| FB-20 | Kh 6h 3d Qc | Qd Jd | No |
| FB-21 | Ts 8c 4h Jd | 9c 7c | No |
| FB-22 | Ts 8c 4h | Jc Tc | No |
| FB-23 | Ad 9c 3h 2s Kd | 7s 6s | No |
| FB-24 | Ad 9c 3h 2s Kd | Ad Kh | CONFLICT — Ad on board and in hero hand |

**FB-24 correction required.** Ad is on the board. Replacing hero cards.

---

## FB-24 — RAISE (CORRECTED)

**Hero cards:** Ah Kc

**Hand strength:** Top two pair (Aces and Kings). Ah pairs the Ad on board (Aces), Kc pairs the Kd on board (Kings). Top two pair on A-K-9-3-2.

**Card conflict check:** Board is Ad 9c 3h 2s Kd. Hero holds Ah Kc. No conflicts.

All reasoning from above applies identically. Ah Kc gives the same top two pair and same strategic considerations. The Ad blocker is lost but Ah still blocks villain's Ax combos similarly. Label, confidence, and flags unchanged.

**Label:** RAISE
**Confidence:** HIGH

---

## Cross-Board Consistency Check

**FB-B08 (Ac Jh 5d Ks) — FB-17 and FB-18:**
- FB-17: Kc Jd (two pair) → CALL. Hero has a strong hand but the board is static; flatting extracts more.
- FB-18: 8h 7h (air) → FOLD. Complete miss on A-K high board.
- Consistent: strong hand calls, air folds on same board.

**FB-B09 (Kh 6h 3d Qc) — FB-19 and FB-20:**
- FB-19: Td 8d (air, sandwich) → FOLD. No connection, worst position.
- FB-20: Qd Jd (second pair, heads-up closing) → CALL. Turned second pair, good equity vs barrel range.
- Consistent: air folds, made hand calls. Different positions justify different outcomes.

**FB-B10 (Ts 8c 4h / Ts 8c 4h Jd) — FB-21 and FB-22:**
- FB-21: 9c 7c (nut straight on turn) → RAISE. Stone cold nuts.
- FB-22: Jc Tc (top pair on flop) → CALL. Strong but not nutted; bet-and-call pattern.
- Consistent: nuts raises, strong-but-vulnerable calls.

**FB-B11 (Ad 9c 3h 2s Kd) — FB-23 and FB-24:**
- FB-23: 7s 6s (air on river) → FOLD. Zero showdown value.
- FB-24: Ah Kc (top two pair on river) → RAISE. Near-nuts, value raise IP.
- Consistent: air folds, near-nuts raises on same runout.

---

## Summary Table

| FB | Board | Street | Hero | Position | Hero Cards | Action | Pot Odds | Label | Confidence | Solver Flag |
|---|---|---|---|---|---|---|---|---|---|---|
| FB-17 | Ac Jh 5d Ks | Turn | BB | OOP-closing | Kc Jd | CO bet 60, BTN fold | 29% | CALL | HIGH | — |
| FB-18 | Ac Jh 5d Ks | Turn | BTN | First resp. (BB behind) | 8h 7h | CO bet 60 | 29% | FOLD | HIGH | — |
| FB-19 | Kh 6h 3d Qc | Turn | BB | Sandwich (CO behind) | Td 8d | BTN bet 90 | 27% | FOLD | HIGH | — |
| FB-20 | Kh 6h 3d Qc | Turn | CO | Closing (2-way) | Qd Jd | BTN bet 90 | 30% | CALL | HIGH | — |
| FB-21 | Ts 8c 4h Jd | Turn | BB | OOP-closing | 9c 7c | CO bet 45, BTN fold | 25% | RAISE | HIGH | Yes (RAISE) |
| FB-22 | Ts 8c 4h | Flop | CO | Closing (bet+call) | Jc Tc | BTN bet 30, BB call | 17% | CALL | HIGH | Yes (MEDIUM CALL, bet-and-call) |
| FB-23 | Ad 9c 3h 2s Kd | River | BB | Closing | 7s 6s | CO bet 90, BTN fold | 30% | FOLD | HIGH | — |
| FB-24 | Ad 9c 3h 2s Kd | River | BTN | Closing | Ah Kc | BB bet 90, CO fold | 30% | RAISE | HIGH | Yes (RAISE) |

**Distribution: 3 CALL (FB-17, FB-20, FB-22) / 3 FOLD (FB-18, FB-19, FB-23) / 2 RAISE (FB-21, FB-24) — target met.**

**Solver flags: 3 situations flagged** (FB-21 RAISE, FB-22 MEDIUM CALL with bet-and-call, FB-24 RAISE).
