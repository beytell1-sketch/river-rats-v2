# Fresh GTO Expert Labels: FB-09 through FB-16
**Date:** 2026-04-13
**Author:** GTO Expert Agent B
**Knowledge base:** knowledge/three_way_gto.md (v1.3)
**Status:** AWAITING REVIEW

**Boards in scope:**
- FB-B04: Qh 7h 3s (two-tone hearts, Q-high)
- FB-B05: As 9s 4s (monotone spades, A-high)
- FB-B06: Th Td 7c (paired tens, rainbow)
- FB-B07: 9d 7d 2c (two-tone diamonds, 9-high)

**Action sources:** PHASE1_GATE_VALIDATION_2026-04-13.md (validated action strings). For FB-10, FB-13, FB-15: REDESIGN versions per REDESIGN_12_AFFECTED_SITUATIONS_2026-04-12.md.

**Target distribution:** 3 CALL / 3 FOLD / 2 RAISE

---

### FB-09

**Board:** Qh 7h 3s
**Street:** Flop
**Hero position:** BTN (first responder to CO's bet; BB still to act after hero)
**Hero cards:** Kh Jh
**Pot:** 90 | **Bet:** 90 (pot-sized) | **To call:** 90
**Pot odds:** 90 / (90 + 90 + 90) = 33.3%
**Validated action:** `BB check, CO bet 90, BTN ???`

**Card conflict check:** Kh, Jh vs board Qh 7h 3s -- no conflicts. No conflict with BB/CO holdings (cards not assigned to them).

**GTO Action:** CALL -- Confidence: HIGH

**Reasoning:** Hero holds Kh Jh -- a nut flush draw (king-high flush draw with Kh on a two-heart board) plus two overcards (K, J) and a gutshot to Broadway (needs a T). This gives hero approximately 12-15 clean outs: 9 flush outs + 3 overcard outs (Kx or Jx that don't duplicate hearts) plus the gutshot. Raw equity is roughly 45-50% against CO's pot-sized betting range, which is polarised on this texture -- strong Qx hands (AQ, KQ), overpairs (AA, KK minus Kh which hero holds), and some semi-bluffs with hearts.

CO's pot-sized bet on a two-tone Q-high board is a polarising sizing. Pot odds require 33.3%. Hero's equity exceeds this comfortably. The question is CALL vs RAISE. Hero does NOT meet the semi-bluff raise criteria cleanly: while Kh blocks some of villain's flush combos, hero is not the nut flush draw (Ah would be the nut), and BB is still alive behind hero. With a live player behind, raising a non-nut flush draw risks getting squeezed by BB or 3-bet by CO holding a set or two pair. The correct play is to call, realise equity across streets, and re-evaluate on the turn. Hero has strong implied odds -- flush completion on the turn or river against CO's polarised range will often win a large pot.

**Solver verification needed:** NO

---

### FB-10

**Board:** As 9s 4s
**Street:** Flop
**Hero position:** BB (OOP, closing action -- BTN folded)
**Hero cards:** Ks Ts
**Pot:** 90 | **Bet:** 30 (33% pot) | **To call:** 30
**Pot odds:** 30 / (90 + 30 + 30) = 20.0%
**Validated action:** `BB check, CO bet 30, BTN fold, BB ???`

**Card conflict check:** Ks, Ts vs board As 9s 4s -- no conflicts (Ks and Ts are spades but not on the board). No conflict with CO/BTN.

**GTO Action:** RAISE -- Confidence: HIGH

**Reasoning:** Hero holds Ks Ts -- a flopped second-nut flush (king-high flush) on a monotone As 9s 4s board. This is an extremely strong made hand on a board where flush-over-flush scenarios are the primary risk, and only As Xs (specifically As with a second spade) beats hero.

Hero's hand meets the raise criteria for strong made hands: (1) Hero has a near-nut flush -- only the ace-high flush beats it. (2) Hero's Ks blocks the most dangerous combos -- villain cannot hold Ks Xs, which removes many strong flush combos from CO's range. (3) With BTN already folded, hero is heads-up against CO and closes action -- no squeeze risk. (4) CO's small 33% pot c-bet on a monotone board is often a range bet or a probe with Ax-no-spade hands; it does not represent overwhelming strength.

Calling is suboptimal because: (a) the board is extremely wet and any non-spade turn card gives hero no additional equity while potentially scaring CO into checking back, denying hero value; (b) hero's flush is already made and vulnerable to As-holder catching up if hero slow-plays; (c) a raise builds the pot while hero has a near-lock on the current board. CO will continue with As Xs (which hero blocks heavily), overpairs, and some stubborn Ax-no-spade hands, all of which hero crushes. The raise extracts maximum value.

**Solver verification needed:** YES -- RAISE with flopped second-nut flush on monotone board, confirm raise > call EV

---

### FB-11

**Board:** As 9s 4s
**Street:** Flop
**Hero position:** BTN (IP, closing action -- CO already folded)
**Hero cards:** Jd 8d
**Pot:** 90 | **Bet:** 45 (50% pot) | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25.0%
**Validated action:** `BB bet 45, CO fold, BTN ???`

**Card conflict check:** Jd, 8d vs board As 9s 4s -- no conflicts. No spade conflicts.

**GTO Action:** FOLD -- Confidence: HIGH

**Reasoning:** Hero holds Jd 8d -- complete air on a monotone spade board. Hero has no spade, no pair, no meaningful draw. On As 9s 4s, any opponent with a single spade has a flush draw with ~35% equity, and any opponent with two spades has a made flush. BB's donk bet of 50% pot into this monotone board is a strong signal -- BB is representing at minimum a spade draw, and more likely a made flush or strong pair-plus-draw. BB's donking range on a monotone A-high board from the BB (which defends wide with suited hands) is heavily weighted toward spade-containing hands.

Hero's equity with Jd 8d against BB's donking range is roughly 10-15% -- hero needs runner-runner to make a relevant hand (backdoor straight via 7-T or 6-7, or running pair outs that still lose to flushes). Pot odds require 25%. Hero's equity is catastrophically below this threshold. Even with IP closing action, there is zero compensation: hero has no draw, no blocker, no implied odds (even if hero makes two pair, any spade on a later street means hero loses to a flush). Clear fold.

**Solver verification needed:** NO

---

### FB-12

**Board:** Th Td 7c
**Street:** Flop
**Hero position:** BB (OOP, first responder to BTN's bet; CO still to act after hero)
**Hero cards:** Jc Js
**Pot:** 90 | **Bet:** 45 (50% pot) | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25.0%
**Validated action:** `BB check, CO check, BTN bet 45, BB ???`

**Card conflict check:** Jc, Js vs board Th Td 7c -- no conflicts. Hero has no T, no 7.

**GTO Action:** CALL -- Confidence: HIGH

**Reasoning:** Hero holds Jc Js -- an overpair to the board on Th Td 7c. This is a strong made hand on a paired board. Hero beats all single-pair hands (Tx for trips excluded), all underpairs (99, 88, 77 for a full house excluded), and all air/draws. The key question is whether hero's overpair is strong enough to continue or whether the paired board makes trips/full houses too likely.

BTN's c-bet on a paired T-T-7 board after both opponents checked is standard -- BTN bets with a polarised range of trip tens (AT, KT, JT, T9, T8), overpairs (QQ+), and air/backdoor draws that take a stab at the unclaimed pot. Against this range, JJ has roughly 55-60% equity: hero loses to trip tens and QQ+ but beats everything else. Pot odds require only 25%, so hero's equity far exceeds the threshold.

Why call and not raise? (1) CO is still alive behind hero -- raising into BTN with CO behind risks getting squeezed by CO holding a T or 77 for a full house. (2) On a paired board, raising polarises hero's range and tells both opponents hero is strong, folding out all the air/marginal hands hero beats. (3) JJ is a classic pot-control hand on a paired board -- strong enough to continue profitably but not strong enough to stack off against the value portion of BTN's range. Calling keeps CO's weaker holdings in the pot and allows hero to re-evaluate on the turn.

**Solver verification needed:** NO

---

### FB-13

**Board:** Th Td 7c
**Street:** Flop
**Hero position:** CO (closing action -- BB folded)
**Hero cards:** 5h 4h
**Pot:** 90 | **Bet:** 45 (50% pot) | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25.0%
**Validated action:** `BB check, CO check, BTN bet 45, BB fold, CO ???`

**Card conflict check:** 5h, 4h vs board Th Td 7c -- no conflicts.

**GTO Action:** FOLD -- Confidence: HIGH

**Reasoning:** Hero holds 5h 4h -- pure air on a paired T-T-7 rainbow board. Hero has no pair, no draw (the only straight draw would be 8-6-5 needing runner-runner, and the backdoor flush in hearts requires two running hearts which is negligible equity). Hero's equity against BTN's c-betting range on this texture is approximately 8-12%. Pot odds require 25%.

The paired board amplifies reverse implied odds: even if hero somehow makes a pair on the turn (5 or 4), it would be bottom pair on a T-T-7-x board -- completely dominated by any Tx, any 7x, any overpair, and vulnerable to CO's entire continuing range. There is no implied odds story here: hero cannot make a hand strong enough to win a significant pot.

Even though hero closes action (BB has folded), which removes squeeze risk, the fundamental equity deficit is too severe. Closing action improves hero's equity realization but cannot overcome a ~15pp shortfall below pot odds with a hand that has virtually no outs. Clear fold.

**Solver verification needed:** NO

---

### FB-14

**Board:** 9d 7d 2c
**Street:** Flop
**Hero position:** BTN (IP, closing action -- CO already folded)
**Hero cards:** Td 8d
**Pot:** 90 | **Bet:** 30 (33% pot) | **To call:** 30
**Pot odds:** 30 / (90 + 30 + 30) = 20.0%
**Validated action:** `BB bet 30, CO fold, BTN ???`

**Card conflict check:** Td, 8d vs board 9d 7d 2c -- no conflicts (Td and 8d are diamonds but not 9d or 7d).

**GTO Action:** RAISE -- Confidence: HIGH

**Reasoning:** Hero holds Td 8d on 9d 7d 2c -- a monster combo draw with a flush draw (non-nut but strong: T-high flush draw with two diamonds on board), an open-ended straight draw (T-9-8-7, needs a 6 or a J), and an overcard (T). Hero's equity is approximately 55-60% against BB's donking range -- this is actually a favourite against most of BB's range.

Hero meets the semi-bluff raise criteria with adaptation: (1) Near-nut draw -- while not the absolute nut flush draw (Ad would be), Td is a strong flush draw and hero blocks the Td from villain's range. Combined with the OESD, hero has 15+ outs (9 flush + 6 straight minus overlaps ~= 14-15 clean outs). (2) Blocker value -- Td removes T-high flush combos from BB's range and 8d removes another diamond combo. (3) Side equity -- the T is an overcard that pairs to top pair, and the 8 pairs to middle pair on this board. (4) IP closing action -- hero has maximum equity realization and no player behind.

BB's small donk bet of 33% pot into a low two-tone board from the BB is a weak-to-medium strength signal. BB's donking range on 9-7-2 hits BB's wide defending range well (7x, 9x, low pairs, suited connectors), but the small sizing suggests thin value or a probe, not a monster. Hero's combo draw with IP position and closing action is a clear raise: it builds the pot for when hero hits (frequent, ~55-60% by river), generates fold equity against BB's weaker made hands (low pairs, weak 9x), and denies BB free equity realization.

**Solver verification needed:** YES -- RAISE with combo draw (flush draw + OESD) IP vs BB donk bet

---

### FB-15

**Board:** 9d 7d 2c
**Street:** Flop
**Hero position:** BB (OOP, closing action -- BTN folded)
**Hero cards:** Kd 5d
**Pot:** 90 | **Bet:** 45 (50% pot) | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25.0%
**Validated action:** `BB check, CO bet 45, BTN fold, BB ???`

**Card conflict check:** Kd, 5d vs board 9d 7d 2c -- no conflicts (Kd and 5d are diamonds not on the board).

**GTO Action:** CALL -- Confidence: MEDIUM

**Reasoning:** Hero holds Kd 5d -- a flush draw (K-high, third-nut flush draw) with an overcard (K) on a low two-tone board. Hero has 9 flush outs plus 3 king outs for top pair = approximately 12 outs, giving roughly 40-45% raw equity against CO's c-betting range on this low board.

Pot odds require 25%. Hero's raw equity (~40-45%) exceeds this by a wide margin. The question is whether OOP equity realization discounts this enough to fold. With BTN folded, hero closes action heads-up against CO. The OOP-closing EQR is approximately 70-80% (KB Section 1.5), not the harsher 60% sandwich discount. At 75% EQR: 42% raw x 75% = 31.5% realised equity, still comfortably above the 25% pot odds.

Why not raise? Hero's draw is strong but NOT the nut flush draw -- Ad Xd beats hero. The semi-bluff raise carve-out (KB Section 1.7) requires the nut draw, which hero does not have. Kd does block some villain flush combos but is not the ace blocker that the carve-out demands. Additionally, hero has no straight draw component. Calling preserves hero's equity while keeping the pot manageable for a non-nut draw OOP.

Confidence is MEDIUM rather than HIGH because: (a) CO's 50% pot bet on a board that favours BB's range is somewhat unusual and could represent a strong hand, (b) the K-high flush draw will lose to Ad-high flush if both complete, creating some reverse implied odds. However, the equity margin above pot odds is large enough that folding would be a clear error.

**Solver verification needed:** YES -- MEDIUM confidence CALL, verify K-high flush draw OOP-closing vs 50% pot c-bet is a call and not a raise

---

### FB-16

**Board:** 9d 7d 2c
**Street:** Flop
**Hero position:** BB (OOP, facing bet-and-call)
**Hero cards:** 6c 6s
**Pot:** 90 | **Bet:** 45 | **BTN called:** pot now 180 | **To call:** 45
**Pot odds:** 45 / (180 + 45) = 20.0%
**Validated action:** `BB check, CO bet 45, BTN call 45, BB ???`

**Card conflict check:** 6c, 6s vs board 9d 7d 2c -- no conflicts.

**GTO Action:** FOLD -- Confidence: HIGH

**Reasoning:** Hero holds 6c 6s -- a small underpair (sixes) on 9d 7d 2c, facing a bet-and-call sequence. The bet-and-call is the strongest action signal in multiway poker (KB Section 2, Factor 5). CO has bet 50% pot into two opponents on a low two-tone board, and BTN has called -- confirming that BTN holds a hand strong enough to continue against both CO's bet and hero's potential action.

Hero's pocket sixes are an underpair to both the 9 and the 7 on this board. Hero has only 2 outs to a set (the two remaining sixes). Against the narrowed bet-and-call ranges: CO's betting range on 9-7-2 two-tone includes overpairs (TT+), top pair (A9, K9), middle pair with draws (7x with a diamond), and some flush draws. BTN's calling range confirms at minimum a pair or a draw (9x, 7x, diamond draws, or pocket pairs 77+). Hero's 66 has roughly 15-18% equity against these combined continuing ranges.

Pot odds require 20%. Hero's equity is below this threshold, and critically: (1) Hero is OOP and must navigate two more streets with a hand that only improves by spiking a set (4.3% per street). (2) The bet-and-call signal means both opponents have strong enough hands to continue, so hero's already-thin equity will not improve through opponent folds. (3) Even if hero spikes a set on the turn, the two-tone board means a diamond completing could create a flush that beats hero's set. (4) OOP equity realization with an underpair facing two confirmed ranges is at the bottom of the EQR scale. Clear fold.

**Solver verification needed:** NO

---

## Summary Table

| FB | Board | Hero | Hero Cards | Pot Odds | Action | Confidence | Solver Flag | Reasoning Summary |
|---|---|---|---|---|---|---|---|---|
| FB-09 | Qh 7h 3s | BTN (1st resp, BB behind) | Kh Jh | 33.3% | CALL | HIGH | NO | K-high flush draw + overcards + gutshot vs pot-sized bet; non-nut draw with BB behind prevents raise |
| FB-10 | As 9s 4s | BB (closing) | Ks Ts | 20.0% | RAISE | HIGH | YES | Flopped 2nd-nut flush on monotone; Ks blocker; heads-up closing action; raise for value |
| FB-11 | As 9s 4s | BTN (closing) | Jd 8d | 25.0% | FOLD | HIGH | NO | Pure air, no spade, no draw on monotone board; ~10-15% equity vs 25% pot odds |
| FB-12 | Th Td 7c | BB (1st resp, CO behind) | Jc Js | 25.0% | CALL | HIGH | NO | Overpair on paired board; strong vs BTN c-bet range; CO behind prevents raise |
| FB-13 | Th Td 7c | CO (closing) | 5h 4h | 25.0% | FOLD | HIGH | NO | Pure air on paired rainbow board; ~8-12% equity vs 25% pot odds; no outs |
| FB-14 | 9d 7d 2c | BTN (closing) | Td 8d | 20.0% | RAISE | HIGH | YES | Combo draw (flush + OESD + overcard); ~55% equity; IP closing; fold equity vs BB donk |
| FB-15 | 9d 7d 2c | BB (closing) | Kd 5d | 25.0% | CALL | MEDIUM | YES | K-high flush draw + overcard; ~42% raw equity vs 25% pot odds; non-nut prevents raise |
| FB-16 | 9d 7d 2c | BB (bet-and-call) | 6c 6s | 20.0% | FOLD | HIGH | NO | Underpair facing bet-and-call; ~15-18% equity vs 20% pot odds; OOP, no draw |

**Distribution check:** 3 CALL (FB-09, FB-12, FB-15) / 3 FOLD (FB-11, FB-13, FB-16) / 2 RAISE (FB-10, FB-14) -- target met.

**Board consistency check:**
- FB-B05 (As 9s 4s): FB-10 RAISE (flopped flush, closing), FB-11 FOLD (air, closing). Consistent -- same board, vastly different hand strength, opposite actions are correct.
- FB-B06 (Th Td 7c): FB-12 CALL (overpair, CO behind), FB-13 FOLD (air, closing). Consistent -- paired board correctly punishes air and supports overpair continuation.
- FB-B07 (9d 7d 2c): FB-14 RAISE (combo draw, IP closing), FB-15 CALL (flush draw, OOP closing), FB-16 FOLD (underpair, bet-and-call). Consistent -- three different hand strengths on the same board produce three different actions, all aligned with GTO principles. The draw-heavy board rewards draws (RAISE when IP with combo draw, CALL when OOP with non-nut) and punishes marginal made hands facing confirmed ranges.

**Solver verification flags:** 3 situations flagged (FB-10 RAISE, FB-14 RAISE, FB-15 MEDIUM CALL).
