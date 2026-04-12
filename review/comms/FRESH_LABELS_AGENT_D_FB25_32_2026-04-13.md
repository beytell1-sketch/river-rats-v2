# Fresh GTO Expert Labels — Agent D (FB-25 through FB-32)
**Date:** 2026-04-13
**Author:** GTO Expert Agent D
**Scope:** 8 facing-bet situations: FB-25, FB-26, FB-27, FB-28, FB-29, FB-30, FB-31, FB-32
**Sources:** PHASE1_GATE_VALIDATION, ML_ARCHITECT spec, REDESIGN_12 (FB-27), REDESIGN_5 (FB-32), three_way_gto.md

---

## Situation FB-25

**Board:** Qd 8d 4c 7s Jh (FB-B12)
**Street:** River
**Hero position:** BB (OOP, closes action — 2-way, BTN folded earlier)
**Bettor:** CO (third barrel — bet flop, bet turn, bet river)
**Pot / Bet / To call:** 240 / 90 / 90
**Pot odds:** 90 / (240 + 90 + 90) = 90 / 420 = 21.4%
**Action string:** `BB check, CO bet 90, BB ???`

**Hero cards:** Qh 9c

**Hand analysis:**
Hero holds top pair (queens) with a 9 kicker on Qd 8d 4c 7s Jh. CO has triple-barreled through all three streets into a pot that started 3-way. The river Jh completes no flush (diamonds missed) but puts a second broadway card on board.

**Factor 1 — Equity:** Top pair on the river is a made hand. Against CO's triple-barrel range, Q9 beats bluffs, missed draws (diamond draws), and some weaker Qx that CO may barrel for thin value. CO's triple-barrel value range includes QJ (now two pair), QT+, overpairs (AA, KK), and sets. Q9 loses to all of those but beats missed flush draws (which CO could barrel all three streets with nut diamond draws) and pure bluffs. Equity is approximately 35-40% against the polarized triple-barrel range.

**Factor 2 — Position:** OOP but closing action (2-way). No squeeze risk.

**Factor 3 — Range composition:** CO's triple-barrel range is polarized on the river. Value: QJ, overpairs, sets. Bluffs: missed diamond draws (Ad Xd, Kd Xd), some missed straight draws. The river Jh is a card that improves some of CO's value range (QJ got there) but also completes nothing for the draws. CO should have a meaningful bluff frequency given the missed diamond draw combos.

**Factor 4 — Board texture:** Two-tone (diamonds missed), connected. The Jh river is a scare card that could represent a bluff from CO using a jack as a blocker, but it also makes two pair for QJ.

**Factor 5 — Action history:** CO has bet all three streets — a strong line. But at 90 into 240 (37.5% pot), the river sizing is small relative to the pot, which is more consistent with thin value or a blocking bet-style sizing than a polar river bomb. Small river bets demand less equity to call.

**Pot odds analysis:** Hero needs 21.4% equity. Top pair with a decent kicker on a board where the flush missed should have enough equity against CO's polarized range. CO's bluff combos (diamond draws that missed) are numerous — at least 10-15 combos of suited diamond hands that barrel three streets. Hero's Q blocks some of CO's value (QJ, QT), reducing value combos.

**Decision:** CALL
**Confidence:** HIGH
**Solver flag:** No

---

## Situation FB-26

**Board:** Qd 8d 4c 7s Jh (FB-B12)
**Street:** River
**Hero position:** BTN (IP, closes action — CO folded)
**Bettor:** BB (OOP donk bet on river after check-call flop, check-through turn)
**Pot / Bet / To call:** 150 / 90 / 90
**Pot odds:** 90 / (150 + 90 + 90) = 90 / 330 = 27.3%
**Action string:** `BB bet 90, CO fold, BTN ???`

**Hero cards:** Tc 9h

**Hand analysis:**
Hero holds T9 offsuit — a rivered straight (T-J-Q with 8-9-T on the low end... wait: board is Q-8-4-7-J. Hero has T9. Straight check: 7-8-9-T-J = yes! Hero has the second nut straight (only QT makes the higher straight Q-J-T-9-8... no. Let me re-check: the board is Qd 8d 4c 7s Jh. Possible straights: T-9 makes 7-8-9-T-J = straight to the jack. The nut straight would be T-9 for the same straight, or K-T for 8-9-T-J-Q? No: 8-9-T-J-Q needs a T and either... wait. Board cards: Q, 8, 4, 7, J. With T9 in hand: 7, 8, 9, T, J = straight. With KT: 8, 9(?), no — need 9 on the board but 9 isn't on the board. So only T9 makes a straight here (7-8-9-T-J). With T6: 4, 6, 7, 8... no. With T9, hero has the NUT straight — there's no higher 5-card straight possible on this board).

Hero has the nut straight. BB's donk bet on the river after a passive line (check-call flop, check turn) represents either a slow-played strong hand that improved on the river (Jh gave BB two pair or a straight) or a bluff/thin value bet. BB could also hold T9 for a chop.

**Decision:** RAISE
**Confidence:** HIGH
**Reasoning:** Hero has the nut straight. BB leads 90 into 150 (60% pot). Hero should raise for value. BB's donk range includes two pair (QJ, J8, J7), sets, worse straights (none possible besides T9 for a chop), and some bluffs. Raising extracts maximum value from BB's value donks (two pair, sets) that will call a raise. Flatting risks losing value from BB's two-pair hands that would call a raise but won't bet again.

**Solver flag:** No

---

## Situation FB-27

**Board:** 8s 5s 3d (FB-B13)
**Street:** Flop
**Hero position:** BB (OOP, CLOSING — per REDESIGN_12, BTN folded)
**Bettor:** CO (c-bet 33% pot)
**Third player:** BTN (already folded)
**Pot / Bet / To call:** 90 / 30 / 30
**Pot odds:** 30 / (90 + 30 + 30) = 30 / 150 = 20%
**Action string:** `BB check, CO bet 30, BTN fold, BB ???`

**Hero cards:** 7s 6s

**Hand analysis:**
Hero holds 7s6s on 8s 5s 3d — a flush draw (two spades) plus an open-ended straight draw (4-5-6-7-8, needs a 4 or 9 for straight). This is a monster combo draw with approximately 15 outs (9 flush + 6 non-spade straight cards) giving roughly 54% equity against CO's c-bet range.

**Factor 1 — Equity:** ~54% raw equity with the combo draw. Massively exceeds the 20% pot odds.

**Factor 2 — Position:** OOP but closing action (BTN folded). Heads-up against CO.

**Factor 3 — Range composition:** CO's 33% c-bet on a low two-tone board is a wide continuation range. This board favors BB's defending range (low connected, two-tone). CO's range contains many overcards that miss this board.

**Factor 4 — Board texture:** Low, two-tone (spades), semi-connected. Strongly favors BB's overcalling range. CO's c-bet frequency should be lower on boards like this.

**Factor 5 — Semi-bluff conditions (KB Section 1.7):** Hero has a near-nut flush draw (7-high flush, not the nut, but the As is not on board so the nut draw holder isn't certain), plus an OESD giving massive side equity. However, 7-high flush is NOT the nut flush draw — As, Ks, Qs, Js, Ts, 9s all make higher flushes. Per KB Section 1.7, non-nut flush draws should call, not raise. But the OESD side equity is enormous and the combined draw equity (~54%) is exceptional.

**Decision:** CALL
**Confidence:** HIGH
**Reasoning:** Despite the massive equity, hero's flush draw is non-nut (7-high flush). Per KB Section 1.7, the semi-bluff raise carve-out requires a NUT draw. 7s6s does not qualify — if hero raises and gets called, the flush draw can still lose to any higher flush. The correct play is to call and realize equity on the turn cheaply. At 20% pot odds with ~54% equity, calling is extremely profitable. Raising risks a 3-bet from CO when CO happens to hold a higher spade draw (As Xs), and hero's non-nut flush draw would be in a dominated spot.

**Solver flag:** No

---

## Situation FB-28

**Board:** 8s 5s 3d (FB-B13)
**Street:** Flop
**Hero position:** BB (OOP, faces bet-and-call)
**Bettor:** CO (c-bet 33% pot)
**Third player:** BTN (already called — bet-and-call)
**Pot / Bet / To call:** Pot 90 + CO bet 30 + BTN call 30 = 150 in pot when hero acts | To call: 30
**Pot odds:** 30 / (150 + 30) = 30 / 180 = 16.7%
**Action string:** `BB check, CO bet 30, BTN call 30, BB ???`

**Hero cards:** Kh Jc

**Hand analysis:**
Hero holds KJ offsuit — two overcards with no pair, no draw, and no spade. Board is 8s 5s 3d — a low, two-tone board that completely misses hero's hand.

**Factor 1 — Equity:** Two overcards with no pair and no draw give approximately 20-25% equity against two opponents' continuing ranges. However, this is raw equity against wide ranges — against the bet-and-call narrowed ranges, equity drops significantly.

**Factor 2 — Position:** OOP, facing bet-and-call. Both opponents have shown strength/interest.

**Factor 3 — Range composition:** CO's c-bet on a low board and BTN's cold-call both suggest made hands or draws. BTN's call is particularly concerning — BTN is calling with hands that connect with this low two-tone board (pairs, spade draws, combo draws). This board smashes cold-caller ranges (suited connectors, small pairs for sets). The bet-and-call signal narrows both ranges.

**Factor 4 — Board texture:** Low, two-tone, semi-connected. This is a board that favors defenders and cold-callers, not the BB's overcards.

**Factor 5 — Action history:** Bet-and-call is a strong confirming signal. Both opponents have hands that want to continue on this texture.

**Decision:** FOLD
**Confidence:** HIGH
**Reasoning:** KJ has no pair, no draw, no spade, and no connection to this board. Two overcards on a low board against bet-and-call is pure air. Even if hero hits a K or J on the turn, the low board means opponents likely have sets, two pairs, or flush draws that dominate. The 16.7% pot odds are generous, but hero has approximately 10-15% equity against the narrowed bet-and-call ranges (only 6 clean overcard outs, many of which are tainted by straight/flush possibilities for opponents). Clear fold.

**Solver flag:** No

---

## Situation FB-29

**Board:** 8s 5s 3d (FB-B13)
**Street:** Flop
**Hero position:** CO (sandwich — BTN behind)
**Bettor:** BB (OOP donk bet 50% pot)
**Third player:** BTN (yet to act behind hero)
**Pot / Bet / To call:** 90 / 45 / 45
**Pot odds:** 45 / (90 + 45 + 45) = 45 / 180 = 25%
**Action string:** `BB bet 45, CO ???`

**Hero cards:** As Kd

**Hand analysis:**
Hero holds AKo with the As — two overcards, the nut flush draw (one spade with the As on a two-spade board), and the ace blocker.

**Factor 1 — Equity:** AK with the As has approximately 50-55% equity against BB's donk range on this board. The nut flush draw alone gives ~35% equity; the overcards add another ~12%.

**Factor 2 — Position:** CO is sandwiched with BTN behind. This is the worst position — must worry about BTN cold-calling or raising behind.

**Factor 3 — Range composition:** BB's donk bet on 8s 5s 3d represents hands that connect with this low board: sets (33, 55, 88), two pair (85, 53), strong draws (spade draws, 67 for OESD), and some semi-bluffs. BB's donk into the preflop raiser is polarized — strong made hands or draws. But BB's range is wide from the BB defend, and this board hits BB's range hard.

**Factor 4 — Board texture:** Low, two-tone (spades), semi-connected. BB-favoring texture. CO's opening range mostly misses this board except for overpairs.

**Factor 5 — Semi-bluff raise conditions (KB Section 1.7):** Hero has: (1) nut flush draw (As) — YES; (2) blocker to opponent's continuing range (As blocks opponent nut flush combos) — YES; (3) side equity (two overcards A and K) — YES. All three conditions met. But hero is in the SANDWICH position with BTN behind. KB Section 1.1 notes sandwich player faces ~80% fold rate from the closing player, but BTN cold-calling a raise behind is a real risk that compresses hero's equity realization.

**Decision:** CALL
**Confidence:** MEDIUM
**Reasoning:** While hero meets all semi-bluff raise criteria from KB Section 1.7, the sandwich position with BTN behind is a critical constraint. If hero raises, BTN can cold-call or 3-bet with hands that smash this board (sets, two pair, strong spade draws). The sandwich penalty (KB Section 1.5) means hero's EQR is significantly reduced. A raise risks building a pot multiway where hero's non-made draw (even the nut flush draw) faces compressed equity realization. Calling preserves hero's excellent pot odds (25%) with ~50%+ equity and avoids bloating the pot in the worst position. Turn card provides more information before committing more chips.

**Solver flag:** YES — MEDIUM confidence CALL where semi-bluff raise criteria are met but sandwich position constrains. Raise vs call is a genuine solver question.

---

## Situation FB-30

**Board:** 8s 5s 3d (FB-B13)
**Street:** Flop
**Hero position:** BTN (first responder to CO bet; BB acts after hero)
**Bettor:** CO (c-bet 66% pot)
**Third player:** BB (still to act after hero)
**Pot / Bet / To call:** 90 / 60 / 60
**Pot odds:** 60 / (90 + 60 + 60) = 60 / 210 = 28.6%
**Action string:** `BB check, CO bet 60, BTN ???`

**Hero cards:** 4h 4d

**Hand analysis:**
Hero holds pocket fours — a set of fours on 8s 5s 3d. This is the bottom set on a low, two-tone board.

**Factor 1 — Equity:** Set of fours has approximately 70-75% equity against CO's c-bet range and BB's continuing range. Bottom set is vulnerable to flush draws and straight draws on this texture but is currently the third-best possible hand (behind set of 8s and set of 5s).

**Factor 2 — Position:** BTN is first responder with BB behind. Not closing action — BB still to act. However, hero has a monster.

**Factor 3 — Board texture:** Low, two-tone (spades), semi-connected. Flush draws and straight draws are abundant. Board will change frequently on the turn — any spade, 2, 4, 6, 7, 9, T could shift equities. Hero's set needs protection.

**Factor 4 — Action history:** CO's 66% pot c-bet is a large sizing for 3-way, suggesting a strong/polarized range. CO likely has overpairs, top pair, or is semi-bluffing with a strong draw.

**Factor 5 — Raise conditions:** Per KB Section 1.17 default: sets are labelled RAISE. Bottom set on a draw-heavy board needs to raise for protection — there are many turn cards that could complete draws and kill hero's equity. If hero flatcalls, BB may also call, creating a multiway pot where hero's set is increasingly vulnerable. Raising charges draws, potentially folds BB's marginal holdings, and defines hero's hand for future streets.

**Decision:** RAISE
**Confidence:** HIGH
**Reasoning:** Sets are pure raises per KB guidance. Bottom set on a draw-heavy two-tone board is especially urgent to raise for protection. CO's large c-bet suggests strength, which means CO may call the raise with overpairs/top pair — giving hero excellent value. BB behind is a concern, but hero's set is strong enough to raise through a live player. If BB cold-calls the raise, hero still has the best hand the vast majority of the time. Flatcalling with bottom set on this texture is too passive — draws are too numerous and the turn could be catastrophic.

**Solver flag:** No

---

## Situation FB-31

**Board:** Jd 8s 6h (FB-B03)
**Street:** Flop
**Hero position:** BTN (IP, closes action — CO already folded)
**Bettor:** BB (OOP donk bet 66% pot)
**Third player:** CO (already folded)
**Pot / Bet / To call:** 90 / 60 / 60
**Pot odds:** 60 / (90 + 60 + 60) = 60 / 210 = 28.6%
**Action string:** `BB bet 60, CO fold, BTN ???`

**Hero cards:** Ac 5c

**Hand analysis:**
Hero holds A5 suited (clubs) — no pair, no draw on this rainbow board (Jd 8s 6h). One overcard (Ace) and a backdoor club flush draw that requires runner-runner.

**Factor 1 — Equity:** A5 suited has approximately 18-22% equity against BB's donk range. The ace provides 3 outs to top pair (but would still have a weak kicker vs hands like AJ, A8). The backdoor flush draw needs two running clubs — worth approximately 1-2% extra equity. Total equity is close to or slightly below pot odds of 28.6%.

**Factor 2 — Position:** IP, closing action. This is the best position — hero can see a free turn if they call and BB checks. Positional advantage increases equity realization.

**Factor 3 — Range composition:** BB's 66% pot donk bet on a connected rainbow board (J-8-6) is a strong line. BB's donk range on this board includes top pair (Jx), two pair (J8, J6, 86), sets (JJ, 88, 66), straights (T9, 97, 75), and strong draws (T7, 95 for OESDs). This board smashes BB's defending range. The large sizing (66% pot) suggests BB is betting for value/protection, not as a weak lead.

**Factor 4 — Board texture:** Rainbow, connected (J-8-6 has multiple straight possibilities). No flush draw possible. Pure straight-draw and pair territory.

**Factor 5 — Action history:** BB's donk into the preflop raiser with a large sizing is a polarizing line that represents strength.

**Decision:** FOLD
**Confidence:** HIGH
**Reasoning:** A5 suited has no pair, no meaningful draw (rainbow board kills flush draw), and only one overcard on a connected board where BB's donk range is strong. Equity (~20%) is below pot odds (28.6%). Even accounting for IP equity realization boost, hero's hand has no way to improve enough to justify continuing. Calling with ace-high and a backdoor on a connected rainbow board against a 66% pot donk is lighting money on fire. The Ace overcard is largely cosmetic — if hero hits an A, BB's range still contains AJ, A8, and sets that dominate.

**Solver flag:** No

---

## Situation FB-32

**Board:** Jd 8s 6h (FB-B03)
**Street:** Flop
**Hero position:** BB (OOP, CLOSING — per REDESIGN_5, BTN already called)
**Bettor:** CO (c-bet 66% pot)
**Third player:** BTN (already called — bet-and-call)
**Pot / Bet / To call:** Pot after BTN call = 210 | To call: 60
**Pot odds:** 60 / (210 + 60) = 60 / 270 = 22.2%
**Action string:** `BB check, CO bet 60, BTN call 60, BB ???`

**Hero cards:** Ks 2s

**Hand analysis:**
Hero holds K2 suited (spades) — no pair, no draw on a rainbow board (Jd 8s 6h). One overcard (King) and no flush draw (board is rainbow). No straight draw.

**Factor 1 — Equity:** K2s has approximately 12-15% equity against two opponents who have both shown interest in this pot (CO bet, BTN called). Hero has one overcard and nothing else. Even the K overcard is weak — if hero hits a K, it could still lose to KJ, K8, etc.

**Factor 2 — Position:** OOP, closing action. Hero is last to act which is normally positive, but the hand is too weak to benefit from positional closing.

**Factor 3 — Range composition:** Facing bet-and-call on J-8-6 rainbow. CO's c-bet on a connected board and BTN's cold-call both represent hands that connect: pairs, straight draws (T9, 97, 75), two pair, sets. BTN's call is especially concerning — BTN is calling a 66% pot bet on a connected board, indicating genuine strength or a strong draw.

**Factor 4 — Board texture:** Rainbow, connected. This board hits both CO's and BTN's ranges. No flush draw possible means all equity comes from pairs and straights.

**Factor 5 — Action history:** Bet-and-call is the strongest multiway signal. Both opponents have hands that want to continue on this texture.

**Decision:** FOLD
**Confidence:** HIGH
**Reasoning:** K2s has no pair, no draw, no flush possibility (rainbow board), and only one overcard facing bet-and-call on a highly connected board. Equity (~12-15%) is well below pot odds (22.2%). The bet-and-call signal from CO and BTN confirms that both opponents connect with J-8-6. Even the 3 king outs are tainted — K on the turn doesn't guarantee hero the best hand when both opponents' ranges are filled with made hands and strong draws. Unambiguous fold.

**Solver flag:** No

---

## Card Conflict Check

| Situation | Board | Hero cards | Conflict? |
|---|---|---|---|
| FB-25 | Qd 8d 4c 7s Jh | Qh 9c | No (Qh ≠ Qd) |
| FB-26 | Qd 8d 4c 7s Jh | Tc 9h | No |
| FB-27 | 8s 5s 3d | 7s 6s | No |
| FB-28 | 8s 5s 3d | Kh Jc | No |
| FB-29 | 8s 5s 3d | As Kd | No |
| FB-30 | 8s 5s 3d | 4h 4d | No (4 not on board) |
| FB-31 | Jd 8s 6h | Ac 5c | No |
| FB-32 | Jd 8s 6h | Ks 2s | No |

**Intra-board hero card conflicts (same board, different situations):**
- FB-B12 (FB-25 & FB-26): Qh,9c vs Tc,9h — no overlap. 9c ≠ 9h. OK.
- FB-B13 (FB-27, FB-28, FB-29, FB-30): 7s,6s vs Kh,Jc vs As,Kd vs 4h,4d — no overlap. Note: Kh in FB-28 and Kd in FB-29 are different suits. OK.
- FB-B03 (FB-31 & FB-32): Ac,5c vs Ks,2s — no overlap. OK.
- FB-B03 also used by Agent A's FB-06 (Tc 9c per REDESIGN_12) and FB-07 — hero cards Ac,5c and Ks,2s do not conflict with Tc,9c.

---

## Summary Table

| FB | Board | Street | Hero | Hero Cards | Pot | Bet | Pot Odds | Action | Confidence | Solver Flag |
|---|---|---|---|---|---|---|---|---|---|---|
| FB-25 | Qd 8d 4c 7s Jh | River | BB (closing, 2-way) | Qh 9c | 240 | 90 | 21.4% | **CALL** | HIGH | No |
| FB-26 | Qd 8d 4c 7s Jh | River | BTN (IP, closing) | Tc 9h | 150 | 90 | 27.3% | **RAISE** | HIGH | No |
| FB-27 | 8s 5s 3d | Flop | BB (closing, HU) | 7s 6s | 90 | 30 | 20.0% | **CALL** | HIGH | No |
| FB-28 | 8s 5s 3d | Flop | BB (bet-and-call) | Kh Jc | 150 | 30 | 16.7% | **FOLD** | HIGH | No |
| FB-29 | 8s 5s 3d | Flop | CO (sandwich) | As Kd | 90 | 45 | 25.0% | **CALL** | MEDIUM | YES |
| FB-30 | 8s 5s 3d | Flop | BTN (1st resp.) | 4h 4d | 90 | 60 | 28.6% | **RAISE** | HIGH | No |
| FB-31 | Jd 8s 6h | Flop | BTN (IP, closing) | Ac 5c | 90 | 60 | 28.6% | **FOLD** | HIGH | No |
| FB-32 | Jd 8s 6h | Flop | BB (bet-and-call) | Ks 2s | 210 | 60 | 22.2% | **FOLD** | HIGH | No |

**Distribution:** 3 CALL, 3 FOLD, 2 RAISE — target met.
**Solver flags:** 1 (FB-29: MEDIUM CALL where raise criteria met but sandwich constrains)
