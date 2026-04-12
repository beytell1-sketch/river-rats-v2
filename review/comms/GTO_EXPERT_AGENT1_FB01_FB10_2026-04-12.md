# GTO Expert Labels: FB-01 through FB-10
**Date:** 2026-04-12
**Author:** GTO Expert Agent 1
**Knowledge base:** knowledge/three_way_gto.md (v1.3)
**Status:** AWAITING REVIEW

---

### FB-01

**Board:** Ah 6d 2c
**Street:** Flop
**Hero position:** BB (OOP, sandwich -- BTN yet to act behind)
**Hero cards:** Kd 6s
**Pot:** 90 | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (90 + 30 + 30) = 20.0%

**GTO Action:** FOLD -- Confidence: HIGH

**Reasoning:** Hero has middle pair (sixes) with a king kicker on an ace-high dry rainbow board. This board strongly favours the CO's opening range, which contains all Ax combos, AK, AQ, and overpairs. Hero's middle pair has roughly 25-30% equity 3-way against CO's c-betting range, which superficially exceeds pot odds. However, hero is in the sandwich seat with BTN yet to act behind. The sandwich position requires tightening the continuing range by 15-20% per the KB (Section 2, Factor 2). Middle pair on an A-high board is a textbook marginal holding that does not improve on most runouts -- hero has only 2 outs to trips and backdoor straight draws at best. Even if BTN folds, hero must navigate two more streets OOP with a hand that is dominated by any Ax, overpair, or even A-high that floats. The combination of sandwich position, A-high board favouring the raiser, and a hand class that is "pot control at best" (DO NOT Rule #5: top pair is medium-strength 3-way, so middle pair is firmly weak) makes this a clear fold.

**Solver verification needed:** NO

---

### FB-02

**Board:** Ah 6d 2c
**Street:** Flop
**Hero position:** BTN (IP, closing action -- CO already folded)
**Hero cards:** Ac 9d
**Pot:** 90 | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (90 + 30 + 30) = 20.0%

**GTO Action:** CALL -- Confidence: HIGH

**Reasoning:** Hero holds top pair with a nine kicker facing a BB donk bet of 33% pot. BB donk-betting into the PFA on an A-high dry rainbow board is a polarising and rare line -- BB's donking range is typically thin, containing some slow-played strong hands (A6s for two pair, sets of 22/66) alongside some thin value (Ax weak kicker) and occasional bluffs. Hero has top pair, which beats the bulk of BB's thin value range. With closing action (IP, no player behind) and a dry rainbow board where equity is stable across runouts, hero's TPMK (top pair medium kicker) has roughly 60-65% equity against BB's donking range. Pot odds require only 20%, and hero's hand comfortably exceeds this. Raising is unnecessary -- it would fold out BB's bluffs and worse Ax hands while only getting action from better (two pair, sets). Calling keeps BB's range wide and extracts value from worse holdings across future streets with positional advantage.

**Solver verification needed:** NO

---

### FB-03

**Board:** Ah 6d 2c
**Street:** Flop
**Hero position:** BB (OOP, facing bet-and-call)
**Hero cards:** 7s 7d
**Pot:** 90 | **Bet:** 30 | **BTN called:** pot now 150 | **To call:** 30
**Pot odds:** 30 / (150 + 30) = 16.7%

**GTO Action:** FOLD -- Confidence: HIGH

**Reasoning:** Hero holds pocket sevens -- a small underpair on an A-high dry board -- facing a bet-and-call sequence. The bet-and-call is the strongest action signal in multiway poker (KB Section 2, Factor 5). CO's bet into three players on an A-high board represents Ax or better at high frequency. BTN's cold-call of that bet confirms a hand strong enough to continue against both the bettor and hero -- likely Ax, pocket pairs above 77 (88-TT that set-mine but also call with overcards to the 6-2), or the occasional slow-played monster. Hero's pocket sevens have approximately 20-25% equity against these narrowed ranges, which is only marginally above the 16.7% pot odds. But critically, hero is OOP and must navigate two more streets with an underpair that never improves to best hand on most runouts (only 2 outs to a set). The equity realization penalty for OOP play (60-80% EQR per KB Section 1.5) means hero's realized equity drops below pot odds. Combined with reverse implied odds when an overcard hits and hero cannot distinguish whether it helped opponents, this is a disciplined fold despite the cheap price.

**Solver verification needed:** NO

---

### FB-04

**Board:** Kc 8c 4d
**Street:** Flop
**Hero position:** BB (OOP, sandwich -- BTN yet to act)
**Hero cards:** Ac Tc
**Pot:** 90 | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25.0%

**GTO Action:** RAISE -- Confidence: HIGH

**Reasoning:** Hero holds the nut flush draw (Ac Tc, two clubs on board Kc 8c 4d) with a blocker (Ac blocks villain's nut flush combos) and side equity (overcard ace, backdoor straight via T). This hand meets ALL FOUR conditions from the KB semi-bluff carve-out (Section 1.7): (1) nut draw -- yes, Ac gives the nut flush draw; (2) blocker -- yes, Ac removes AcXc from villain's continuing range, increasing fold equity; (3) side equity -- yes, Ac is an overcard that makes TPTK if it hits, and Tc provides backdoor straight potential. Hero's raw equity is approximately 40-45% (9 flush outs + 3 ace outs + backdoor straight outs). Even from the sandwich seat with BTN behind, the Ac blocker compensates for the positional disadvantage. Per Worked Example 9 (AsQs on Ks Jd 5s), the solver verifies that nut flush draws with the ace blocker and side equity should RAISE even OOP in 3-way pots. Calling is not terrible since hero has odds, but it wastes the fold equity generated by the Ac blocker. Raising builds the pot for when the flush completes and pressures both opponents to fold marginal holdings.

**Solver verification needed:** YES -- RAISE label, confirm nut flush draw with Ac blocker raises on Kc 8c 4d texture

---

### FB-05

**Board:** Kc 8c 4d
**Street:** Flop
**Hero position:** BTN (IP, closing action -- BB already folded)
**Hero cards:** Jd Ts
**Pot:** 90 | **Bet:** 60 | **To call:** 60
**Pot odds:** 60 / (90 + 60 + 60) = 28.6%

**GTO Action:** FOLD -- Confidence: HIGH

**Reasoning:** Hero holds JT offsuit with no club (no flush draw) on a Kc 8c 4d board facing a large 67% pot bet from CO. Hero has zero made hand (no pair), a gutshot to a Q-high straight (needs a Q for QJT98, but that also puts a Q on board which could improve CO's AQ), and no flush draw since neither card is a club. Hero's equity is approximately 15-18% -- two overcards to the 8 and 4 but both under the K, plus a thin gutshot. This is well below the 28.6% pot odds required. The large sizing from CO signals a polarised range: strong made hands (Kx, overpairs, sets) and strong draws (flush draws with clubs). JT without the club draw is pure air on this board -- no meaningful draws, no made hand, no blocker to the flush. Even IP with closing action, hero cannot profitably continue. The hand has virtually no implied odds since hitting a J or T still leaves hero behind any Kx. This is a straightforward fold.

**Solver verification needed:** NO

---

### FB-06

**Board:** Jd 8s 6h
**Street:** Flop
**Hero position:** BB (OOP, sandwich -- BTN yet to act)
**Hero cards:** Tc 9c
**Pot:** 90 | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (90 + 30 + 30) = 20.0%

**GTO Action:** CALL -- Confidence: HIGH

**Reasoning:** Hero holds T9 offsuit on Jd 8s 6h -- an open-ended straight draw (any 7 or Q completes the straight, 8 outs). This is a connected rainbow board that favours the cold-caller (BTN) and BB defender ranges per KB Section 2, Factor 4. Hero's equity is approximately 32-35% with the OESD (8 clean outs to the nuts or near-nuts, ~32% by river). This significantly exceeds the 20% pot odds. The small bet sizing (33% pot) gives hero an excellent price. While hero is in the sandwich seat with BTN behind, the draw is strong enough that even if BTN raises, hero can continue profitably. Crucially, T9 does NOT meet the RAISE conditions from Section 1.7: it is not a nut draw with a blocker (no flush draw, no ace blocker). The straight draw is strong but raising would be a semi-bluff without blocker support, which the KB explicitly flags as unprofitable 3-way (DO NOT Rule #2). Calling realizes equity cheaply with excellent implied odds when the straight completes -- hero's made straight will often get paid off by opponents' top pair and overpair holdings.

**Solver verification needed:** NO

---

### FB-07

**Board:** Jd 8s 6h
**Street:** Flop
**Hero position:** CO (sandwich -- between BB donk and BTN yet to act)
**Hero cards:** Qd Qc
**Pot:** 90 | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25.0%

**GTO Action:** CALL -- Confidence: MEDIUM

**Reasoning:** Hero holds QQ (overpair) in the sandwich seat facing a BB donk bet of 50% pot on Jd 8s 6h. BB donk-betting on a connected middling board is a strong signal -- BB's range on this texture contains many connecting hands (J8, 86, 97, T9, 76s, sets of 88/66) that hit hard. However, QQ is an overpair above all board cards, giving hero approximately 55-60% equity against BB's donking range. This exceeds pot odds of 25% by a wide margin. The concern is the sandwich position with BTN still to act behind -- BTN's flat range is dense with suited connectors (T9s, 97s, 76s) that crush this board. But QQ beats all one-pair hands and most two-pair combinations on this texture. Per DO NOT Rule #5, top pair is medium-strength 3-way, but QQ as an overpair is one hand class above top pair. Raising risks folding out worse hands (Jx, draws) and only getting action from better (sets, two pair), while also exposing hero to a BTN 3-bet squeeze with a monster. Calling keeps the pot controlled, maintains the strength of hero's range, and allows hero to re-evaluate on the turn when BTN's action provides additional information.

**Solver verification needed:** YES -- CALL with MEDIUM confidence, overpair in sandwich on connected board is a close decision between call and raise

---

### FB-08

**Board:** Qh 7h 3s
**Street:** Flop
**Hero position:** CO (sandwich -- BTN yet to act behind)
**Hero cards:** Ah Kd
**Pot:** 90 | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25.0%

**GTO Action:** CALL -- Confidence: MEDIUM

**Reasoning:** Hero holds AK offsuit with Ah (one heart) on Qh 7h 3s facing a BB donk of 50% pot. Hero has no made hand (ace-high), but carries significant equity: backdoor nut flush draw via Ah, 6 overcard outs (3 aces + 3 kings) to likely TPTK, and the Ah acts as a partial blocker to opponent heart flush draws. Per KB Example 7 (AK on Jd 8d 4c), overcard outs represent "hidden equity" not fully captured in draw_outs features -- approximately 24% improvement probability by the river. Combined with the backdoor flush potential of Ah, hero's true equity is approximately 30-35%, exceeding the 25% pot odds. BB's donk-betting range on Qh 7h 3s is likely polarised between strong Qx hands and semi-bluffs with heart draws. Hero's Ah blocks some of BB's strongest flush draw combos. The sandwich concern (BTN behind) is mitigated by the fact that BTN's cold-call range misses this Q-high board at high frequency (BTN's suited connectors and middle pairs don't connect well here). However, confidence is MEDIUM because ace-high with no made hand in the sandwich seat is inherently vulnerable -- if BTN raises behind, hero faces a difficult decision.

**Solver verification needed:** YES -- CALL with MEDIUM confidence, AK with backdoor nut flush draw in sandwich facing donk bet

---

### FB-09

**Board:** Qh 7h 3s
**Street:** Flop
**Hero position:** BTN (IP, closing action -- BB already folded)
**Hero cards:** Kh Jh
**Pot:** 90 | **Bet:** 90 | **To call:** 90
**Pot odds:** 90 / (90 + 90 + 90) = 33.3%

**GTO Action:** RAISE -- Confidence: MEDIUM

**Reasoning:** Hero holds Kh Jh -- the second-nut flush draw (king-high hearts) with an overcard (K) and a gutshot to a broadway straight (needs a T for KQJT) -- facing a pot-sized bet from CO on Qh 7h 3s. Hero has approximately 40-45% equity: 9 flush outs (nut flush draw minus the Ah, but Kh-high flush beats all non-Ah flushes), 3 king outs for top pair, and a thin gutshot. The pot-sized bet from CO is polarising -- CO either has a strong made hand (QQ, Qx, overpairs) or is semi-bluffing with their own draws. Hero's Kh is a significant blocker: it removes KhXh combos from CO's range and blocks some of CO's strongest heart holdings. With IP closing action and no player behind, hero can leverage maximum fold equity. This is a close spot between CALL and RAISE. Calling has correct odds (33% needed, ~40-45% equity). But raising leverages the Kh blocker, fold equity against CO's marginal Qx holdings, and builds a pot hero wins at high frequency when the flush completes. The key concern is that Kh Jh is NOT the nut flush draw -- Ah is still out there. However, facing a single opponent (BB folded), the probability of CO holding the Ah flush draw is reduced. Per Section 1.7, nut draw with blocker and side equity should raise; Kh is near-nut with strong blocker properties, making this a raise in position.

**Solver verification needed:** YES -- RAISE label with non-nut (king-high) flush draw; confirm solver prefers raise over call IP vs pot-sized bet

---

### FB-10

**Board:** As 9s 4s
**Street:** Flop
**Hero position:** BB (OOP, sandwich -- BTN yet to act)
**Hero cards:** Jc 8d
**Pot:** 90 | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (90 + 30 + 30) = 20.0%

**GTO Action:** FOLD -- Confidence: HIGH

**Reasoning:** Hero holds J8 offsuit with no spade on a monotone As 9s 4s board. This is pure air: no pair, no flush draw (neither card is a spade), no meaningful straight draw (gutshot-only hands are check/folds per KB Section 1.7). Hero's equity is approximately 10-15% against ranges that include any single spade (which gives a flush draw) or made flushes. On a monotone board, any opponent with a single spade has at minimum a flush draw, and the CO's opening range contains many suited spade combos (AXs, KXs, QXs, suited connectors). Even at the cheap 20% pot odds price, hero's equity is well below what is needed. The sandwich position with BTN behind makes this even worse -- BTN's cold-call range contains suited connectors and suited aces that hit this monotone board hard. J8 offsuit has no backdoor draws, no overcards above the ace, and no path to improvement. Per the KB, gutshot-only or backdoor-only hands on monotone boards are clear folds. This is textbook air that should be released immediately.

**Solver verification needed:** NO

---

## Summary Table

| Situation | Hero cards | Action | Confidence | Solver needed |
|-----------|-----------|--------|------------|---------------|
| FB-01 | Kd 6s | FOLD | HIGH | NO |
| FB-02 | Ac 9d | CALL | HIGH | NO |
| FB-03 | 7s 7d | FOLD | HIGH | NO |
| FB-04 | Ac Tc | RAISE | HIGH | YES |
| FB-05 | Jd Ts | FOLD | HIGH | NO |
| FB-06 | Tc 9c | CALL | HIGH | NO |
| FB-07 | Qd Qc | CALL | MEDIUM | YES |
| FB-08 | Ah Kd | CALL | MEDIUM | YES |
| FB-09 | Kh Jh | RAISE | MEDIUM | YES |
| FB-10 | Jc 8d | FOLD | HIGH | NO |

**Distribution:** 4 CALL, 4 FOLD, 2 RAISE
**Solver verification flagged:** 4 situations (FB-04 RAISE, FB-07 MEDIUM CALL, FB-08 MEDIUM CALL, FB-09 RAISE)
**Card conflict check:** All hero cards verified clear of their respective boards.
