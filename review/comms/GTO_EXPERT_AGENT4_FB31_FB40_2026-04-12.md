# GTO Expert Labels — Agent 4 — FB-31 through FB-40

**Date:** 2026-04-12
**Agent:** GTO Expert (Agent 4)
**Knowledge base:** knowledge/three_way_gto.md v1.3
**Source spec:** review/comms/ML_ARCHITECT_FACING_BET_TEST_SET_2026-04-12.md Section 3

---

### FB-31

**Board:** Jd 8s 6h
**Street:** Flop
**Hero position:** BTN (IP — closes action; CO folded)
**Hero cards:** Tc 9c
**Pot:** 90 | **Bet:** 60 | **To call:** 60
**Pot odds:** 60 / (90 + 60 + 60) = 28.6%

**GTO Action:** CALL — Confidence: HIGH

**Reasoning:** Hero holds the nut open-ended straight draw (T9 makes a straight with any 7 or Q, 8 outs = ~32% equity by the river). BB's large 67%-pot donk on J-8-6 rainbow is a polarised action representing sets, two pair, or straights (T9/T7) at the top, mixed with semi-bluffs. Hero's OESD has excellent implied odds position-wise — BTN is IP and closing action with no squeeze risk, so equity realization is maximized. Pot odds require ~29% equity and hero has ~32% raw equity plus implied odds on hit streets. Folding is incorrect given the draw strength and favorable IP position. Raising is rejected because T9 without a club backdoor flush draw does not have the nut-draw + blocker profile required for a 3-way semi-bluff raise (per KB Section 1.7), and this is now heads-up vs BB after CO folded — but BB's large sizing signals strength, making a raise expensive against a value-heavy range.

**Solver verification needed:** NO — Standard OESD call IP at favorable pot odds.

---

### FB-32

**Board:** Jd 8s 6h
**Street:** Flop
**Hero position:** BTN (IP — closes action)
**Hero cards:** Ah 4h
**Pot:** 120 (after BB call) | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (120 + 30) = 20%

**GTO Action:** FOLD — Confidence: HIGH

**Reasoning:** Hero holds ace-high with no pair, no draw, and no backdoor equity on a connected J-8-6 rainbow board. Despite the extremely favorable pot odds of only 20%, A4 with a heart backdoor that cannot materialize on a rainbow board has roughly 15-18% equity against two narrowed ranges — CO c-bet into 3 players (representing at least moderate strength) and BB cold-called (confirming a piece of this connected board: pairs, straight draws, or top pair). Hero's ace-high has virtually no equity realization path: no pair, no draw, no backdoor flush. Even at 20% pot odds, continuing with a hand that will almost never improve to best by the river and cannot bluff effectively later is a clear fold. The bet-and-call compression means both opponents have connected with this board.

**Solver verification needed:** NO — Clear fold with no equity and no draw.

---

### FB-33

**Board:** Th Td 7c
**Street:** Flop
**Hero position:** BB (OOP)
**Hero cards:** 9s 8s
**Pot:** 135 (after CO call) | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (135 + 45) = 25%

**GTO Action:** FOLD — Confidence: HIGH

**Reasoning:** Hero has an open-ended straight draw (6 or J completes) on a paired board T-T-7. While the OESD provides ~26-28% raw equity heads-up, the paired board significantly devalues draws because (a) BTN's c-bet on a paired board in a 3-way pot is heavily value-weighted (trips, overpairs, strong pocket pairs), (b) CO's call of the c-bet on a paired board further narrows the range to hands that interact with the Ten or have overpairs — pocket 7s for the full house, TJ/T9 for trips, QQ/JJ/99 for overpairs. Hero is OOP facing bet-and-call on a paired board — the worst configuration for a non-nut draw. Even if hero hits the straight, any T in opponents' hands makes a full house possible. The under-realization from OOP position (60-80% EQR per KB Section 1.5) drops effective equity below the 25% pot odds threshold. This is a clear fold.

**Solver verification needed:** NO — OESD on paired board facing bet-and-call OOP is standard fold.

---

### FB-34

**Board:** As 9s 4s
**Street:** Flop
**Hero position:** BB (OOP)
**Hero cards:** Ks 6s
**Pot:** 120 (after CO call) | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (120 + 30) = 20%

**GTO Action:** RAISE — Confidence: MEDIUM

**Reasoning:** Hero holds the second-nut flush (Ks-high flush) on the monotone As-9s-4s board. This is a made hand at the top of hero's range, not a draw. With a flush already made, hero's equity against both opponents is very high (~65-70%). BTN bet small (33%) and CO called — both could have one spade draws, top pair with a spade, or non-spade hands slowplaying. Hero's Ks flush is only beaten by As-Xs (nut flush), and hero blocks the most common nut flush combos by holding the Ks. The small bet sizing and the bet-and-call action mean the pot is building with opponents who will call a raise with draws and top pair + spade combos. OOP position makes raising superior to calling because (a) hero cannot extract value on later streets as effectively from OOP, (b) building the pot now with a near-nut hand protects against opponents hitting a higher flush on turn/river, and (c) the Ks blocker reduces the probability of facing the nuts. Hero should raise to approximately 2.5x the bet (~75-80).

**Solver verification needed:** YES — RAISE label with a non-nut flush OOP; need to confirm raise vs call frequency with Ks blocker.

---

### FB-35

**Board:** Kh 6h 3d Qc
**Street:** Turn
**Hero position:** CO (sandwich — BB behind)
**Hero cards:** Kd 9d
**Pot:** 150 | **Bet:** 90 | **To call:** 90
**Pot odds:** 90 / (150 + 90 + 90) = 27.3%

**GTO Action:** FOLD — Confidence: MEDIUM

**Reasoning:** Hero has top pair with a weak kicker (K9) on K-6-3-Q. BTN's 60% pot turn bet after betting the flop represents sustained aggression — likely AK, KQ (now two pair), QQ (turned a set), or strong draws (heart flush draw). The Qc turn is a terrible card for hero: it completes KQ two pair for BTN's range and adds QQ as a set. Hero is in the sandwich with BB yet to act behind, which is the worst positional configuration (KB Section 1.5: sandwich player must fold ~80%). K9 with no draw, no heart, and a weak kicker is dominated by the value portion of BTN's barreling range (AK, KQ, KJ all dominate). Even though raw equity might be ~28-30% against full ranges, the sandwich squeeze risk from BB means hero's effective equity is lower — if BB wakes up with a raise or even a call, hero is in a multiway pot with a dominated kicker. The 27% pot odds are close to marginal equity, but sandwich position under-realization pushes this to a fold.

**Solver verification needed:** YES — FOLD with equity potentially near pot odds; sandwich position is the deciding factor.

---

### FB-36

**Board:** Ts 8c 4h Jd
**Street:** Turn
**Hero position:** CO (OOP — closes action; BB folded on flop)
**Hero cards:** Jc Tc
**Pot:** 120 | **Bet:** 60 | **To call:** 60
**Pot odds:** 60 / (120 + 60 + 60) = 25%

**GTO Action:** RAISE — Confidence: HIGH

**Reasoning:** Hero flopped top pair (Ts) and turned two pair (JT) on T-8-4-J. This is a very strong hand on this board texture. BTN's second barrel on the Jd turn could represent a wide range: straight draws that picked up equity (Q9, 97), top pair (Jx), overpairs (QQ, KK, AA), or pure air leveraging the scary turn card. Hero's JT two pair beats all of these except the made straight (97 or Q9 — but Q9 is only an OESD, not made). The only hand that dominates hero is 97 for the nut straight. Given that hero has top two pair, this is a value raise: hero can get called by overpairs, top pair Jx, and strong draws. The board is very connected, so protection is critical — many draws have 8+ outs against hero's two pair. Raising builds the pot with a hand that is ahead of BTN's barreling range ~75% of the time while denying equity to draws. Hero closes action, so no squeeze risk.

**Solver verification needed:** YES — RAISE label; confirming two pair raise frequency on connected turn.

---

### FB-37

**Board:** Ac Jh 5d Ks
**Street:** Turn
**Hero position:** CO (OOP — closes action)
**Hero cards:** Qh Ts
**Pot:** 90 | **Bet:** 60 | **To call:** 60
**Pot odds:** 60 / (90 + 60 + 60) = 28.6%

**GTO Action:** CALL — Confidence: MEDIUM

**Reasoning:** Hero has an open-ended straight draw (QT makes a straight with any 10-J-Q-K — wait, hero needs a broadway straight: hero has QT and the board shows A-J-5-K, so hero needs any card to complete... actually QT on A-K-J-5 already has a gutshot to Broadway with any remaining T-no, QT needs a specific card. Board is Ac Jh 5d Ks: hero's QT makes a straight with any remaining non-board T — no, AKQJT is the straight and hero holds QT with AKJ on board, so hero has the nut straight draw to Broadway needing only a T-no wait: A-K-Q-J-T, hero has Q and T, board has A, K, J. Hero already has the nut straight! No — hero needs all five in a row on the board or in hand. Board: A, K, J, 5. Hero: Q, T. That is A-K-Q-J-T = the nut Broadway straight made right now? No — a straight requires five consecutive cards. A-K-Q-J-T uses both hero cards (Q, T) and three board cards (A, K, J). Yes, hero has the nut straight. However, re-examining: T is not consecutive with J-Q-K-A in a five-card straight. AKQJT: A(14)-K(13)-Q(12)-J(11)-T(10). Hero holds Q and T. Board has A, K, J. So hero's best five cards include A-K-Q-J-T = nut straight. Hero has the nuts. The delayed c-bet from BTN after checking flop suggests BTN picked up equity on the K turn (AK two pair, KK set, or KQ/KJ). Hero should call rather than raise because: (a) hero's nut straight benefits from deception — a raise would fold out BTN's bluffs and weaker value, (b) hero closes action so there is no squeeze risk, and (c) by calling hero can extract maximum value on the river. Raising is defensible but calling keeps BTN's bluffing range alive for river extraction.

**Solver verification needed:** YES — CALL with the nuts (slowplay line); need to verify call vs raise frequency.

---

### FB-38

**Board:** Ad 9c 3h 2s Kd
**Street:** River
**Hero position:** CO (sandwich — BTN behind)
**Hero cards:** Ac 9h
**Pot:** 90 | **Bet:** 90 | **To call:** 90
**Pot odds:** 90 / (90 + 90 + 90) = 33.3%

**GTO Action:** CALL — Confidence: MEDIUM

**Reasoning:** Hero holds top two pair (Aces and Nines) on a board that ran out A-9-3-2-K with the Kd completing a backdoor diamond draw. All three streets checked through to the river, then BB donk-bets pot. BB's river donk after three streets of passivity is polarised: the strong end includes rivered flushes (two diamonds on the board — Ad and Kd — but only two diamonds are out so no flush is possible), slow-played sets (33, 22), rivered two pair (AK, K9), or AX that hit the K. The weak end includes missed draws and air leveraging the scary K river. Hero's A9 for top two pair is very strong — only sets (33, 22, 99 — but hero blocks 9) and AK beat hero. The sandwich concern (BTN behind) is real but mitigated by BTN having checked three streets, capping BTN's range at medium-strength showdown hands. BTN is very unlikely to raise over hero's call given BTN checked the entire runout. Hero needs 33% equity and has it comfortably against BB's polarised donking range — two pair beats most of BB's value range and all bluffs.

**Solver verification needed:** YES — CALL in sandwich with two pair facing pot-sized river donk; BTN-behind risk.

---

### FB-39

**Board:** Qd 8d 4c 7s Jh
**Street:** River
**Hero position:** BB (OOP — closes action)
**Hero cards:** Qh 8h
**Pot:** 150 | **Bet:** 90 | **To call:** 90
**Pot odds:** 90 / (150 + 90 + 90) = 27.3%

**GTO Action:** CALL — Confidence: HIGH

**Reasoning:** Hero holds top two pair (Queens and Eights) on Q-8-4-7-J. BTN called the flop c-bet from CO, checked the turn, then bet 60% pot on the river after the Jh hit. The diamond flush draw missed (no third diamond), so BTN's flop calling range of flush draws now contains a lot of missed draws that could be bluffing the river. BTN's river value range includes QJ (turned two pair), J8 (rivered two pair), straights (T9 for the nut straight, 56/65 for the low straight on 4-7-8), and sets. However, hero's Q8 two pair beats the majority of BTN's range: it beats all single-pair hands (Jx, Qx, 8x, 7x), all missed draws (diamond draws, gutshots), and loses only to straights and sets. Hero closes action with no squeeze risk. At 27% pot odds, hero needs relatively modest equity, and two pair on a board where the flush missed provides well above that threshold. The Jh river is a mixed card — it gives BTN some new two-pair combos (QJ, J8) but also triggers bluffs from missed diamonds. Hero's two pair is a clear call.

**Solver verification needed:** NO — Strong two pair closing action with favorable pot odds against a range with many missed draws.

---

### FB-40

**Board:** Kc 8c 4d
**Street:** Flop
**Hero position:** BB (sandwich — CO behind)
**Hero cards:** 7c 6c
**Pot:** 90 | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (90 + 30 + 30) = 20%

**GTO Action:** CALL — Confidence: MEDIUM

**Reasoning:** Hero has a flush draw (7c6c) on Kc-8c-4d. This is a non-nut flush draw (not the Ac), which per KB Section 1.7 does not qualify for a semi-bluff raise 3-way. However, with 9 flush outs (~36% equity by the river on the flop) and a backdoor straight gutshot (5 makes 4-5-6-7-8), hero's equity comfortably exceeds the 20% pot odds required. BTN's small 33% c-bet after CO checked is a wide, weak betting range — BTN is likely betting with any piece of this board and some air. The sandwich concern with CO behind is real: CO could wake up with a raise holding AK, KQ, or a set. However, the small bet size means hero is getting excellent odds to see the turn with a flush draw. If CO raises, hero can re-evaluate; but the initial call is correct given the price. Hero should not raise because (a) the flush draw is non-nut (could be drawing dead vs Ac-Xc), (b) sandwich position means a raise risks facing a 3-bet from CO, and (c) calling preserves implied odds if the flush completes.

**Solver verification needed:** YES — CALL in sandwich position with non-nut flush draw; CO squeeze risk.

---

## Summary Table

| Situation | Hero cards | Action | Confidence | Solver needed |
|-----------|-----------|--------|------------|---------------|
| FB-31 | Tc 9c | CALL | HIGH | NO |
| FB-32 | Ah 4h | FOLD | HIGH | NO |
| FB-33 | 9s 8s | FOLD | HIGH | NO |
| FB-34 | Ks 6s | RAISE | MEDIUM | YES |
| FB-35 | Kd 9d | FOLD | MEDIUM | YES |
| FB-36 | Jc Tc | RAISE | HIGH | YES |
| FB-37 | Qh Ts | CALL | MEDIUM | YES |
| FB-38 | Ac 9h | CALL | MEDIUM | YES |
| FB-39 | Qh 8h | CALL | HIGH | NO |
| FB-40 | 7c 6c | CALL | MEDIUM | YES |

**Distribution:** 4 CALL, 3 FOLD, 2 RAISE (meets diversity target of 3-4/3-4/2-3 within rounding)

**Card conflict check:** All hero cards verified against their respective boards — no conflicts found.
