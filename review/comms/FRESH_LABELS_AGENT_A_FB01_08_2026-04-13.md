# Fresh Labels — Agent A — FB-01 through FB-08
**Date:** 2026-04-13
**Author:** GTO Expert Agent A
**Scope:** 8 facing-bet 3-way postflop situations (FB-01 to FB-08)
**Sources:** PHASE1_GATE_VALIDATION (validated action strings), REDESIGN_12 (corrected specs for FB-01/04/06), ML_ARCHITECT_FACING_BET_TEST_SET (board details), knowledge/three_way_gto.md (GTO reasoning framework)

---

## Labels

### FB-01
**Board:** Ah 6d 2c | **Street:** Flop
**Hero:** BB — CLOSING ACTION (CO bet, BTN folded, BB last to act)
**Hero cards:** 7s 6s
**Pot:** 90 | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (90 + 30 + 30) = 20%

**GTO Action:** FOLD — Confidence: HIGH
**Reasoning:** Hero holds middle pair sixes with a weak kicker on an Ace-high dry rainbow board. Against CO's c-bet range on Ah 6d 2c, CO's continuing range is heavily weighted toward Ax hands, overpairs, and broadways that dominate or are ahead of 6x. Hero's equity is approximately 15-20% — roughly at the pot odds threshold of 20%, but OOP equity realisation (60-80% per KB Section 1.5) drops realised equity to approximately 12-16%, well below what is needed to continue. The board heavily favours CO's opening range (A-high dry is the classic PFA-advantage texture per KB Section 4, Factor 4), and hero has no draw to improve. Even though BTN has folded and hero closes action, middle pair weak kicker OOP against CO's A-high board c-bet is a standard fold.
**Solver verification:** NO

---

### FB-02
**Board:** Ah 6d 2c | **Street:** Flop
**Hero:** BTN — IP CLOSING ACTION (BB donk bet, CO folded)
**Hero cards:** Kd Qs
**Pot:** 90 | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (90 + 30 + 30) = 20%

**GTO Action:** CALL — Confidence: HIGH
**Reasoning:** Hero holds two overcards (KQ) against a BB donk bet on Ah 6d 2c. BB's donk-betting range into the PFA on an A-high board is polarised: either a strong Ax hand or a bluff/probe with a hand that does not want to check-call. Hero has approximately 25-30% equity from six overcard outs (three Kings, three Queens give top pair top kicker or second pair top kicker), plus some backdoor straight potential. This exceeds the 20% pot odds threshold. Hero is IP closing action, so equity realisation is excellent (105-120% per KB Section 1.5). The small sizing (33% pot) gives hero an attractive price, and position allows hero to control the pot on later streets. Folding KQ IP to a min-donk at 20% pot odds discards too much equity. Raising is premature with no made hand yet.
**Solver verification:** NO

---

### FB-03
**Board:** Ah 6d 2c | **Street:** Flop
**Hero:** BB — FACING BET-AND-CALL (CO bet, BTN called, BB last)
**Hero cards:** Jd Td
**Pot:** 90 | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (90 + 30 + 30 + 30) = 30 / 180 = 16.7%

**GTO Action:** FOLD — Confidence: HIGH
**Reasoning:** Hero holds JT offsuit with no made hand and no draw on an Ah 6d 2c dry rainbow board. Hero has approximately 10-15% equity — two overcards that are not top pair if they hit, with no flush draw and only a backdoor gutshot. The bet-and-call sequence from CO and BTN signals that both opponents have connected with this A-high board: CO's c-bet on an A-high board represents strong range advantage, and BTN's cold-call confirms at least an Ace or a pocket pair (per KB Section 2, Factor 5: the bet-and-call signal narrows both ranges). Hero's JT has almost no equity against two narrowed, connected ranges. Even at the attractive 16.7% pot odds, hero's pure air holding with no draw cannot profitably continue. The OOP position further reduces any marginal equity realisation.
**Solver verification:** NO

---

### FB-04
**Board:** Kc 8c 4d | **Street:** Flop
**Hero:** BB — CLOSING ACTION (CO bet, BTN folded, BB last)
**Hero cards:** Ac 5c
**Pot:** 90 | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25%

**GTO Action:** RAISE — Confidence: HIGH
**Reasoning:** Hero holds Ac 5c — the nut flush draw on a two-tone club board (Kc 8c 4d). This hand meets all four semi-bluff carve-out conditions from KB Section 1.7: (1) nut draw (nut flush draw with Ac), (2) blocker to opponent's continuing range (Ac blocks any opponent nut flush draw combos and AK combos), (3) side equity from overcard Ace giving top pair if an Ace hits plus a backdoor wheel gutshot. Hero has approximately 35-40% equity (9 flush outs plus 3 Ace outs minus overlap). At 25% pot odds, calling is also profitable, but the raise is preferred because the Ac blocker significantly increases fold equity against CO's c-bet range, and hero closes action with no BTN behind to cold-call the raise. The KB explicitly references the AsQs example on a flush board as a solver-verified RAISE; Ac5c on Kc 8c 4d is structurally identical (nut flush draw + blocker + overcard equity).
**Solver verification:** YES — RAISE action always flagged per rules

---

### FB-05
**Board:** Kc 8c 4d | **Street:** Flop
**Hero:** BTN — FIRST RESPONDER (CO bet, BB still to act after hero)
**Hero cards:** Js Jh
**Pot:** 90 | **Bet:** 60 | **To call:** 60
**Pot odds:** 60 / (90 + 60 + 60) = 28.6%

**GTO Action:** CALL — Confidence: MEDIUM
**Reasoning:** Hero holds pocket Jacks — an overpair to the 8 and 4 but an underpair to the King on Kc 8c 4d. Against CO's 66% pot c-bet range on a K-high two-tone board, CO frequently holds Kx (AK, KQ, KJ, KTs), overpairs (QQ, AA), and club draws. Hero's JJ has approximately 35-45% equity depending on CO's exact range — JJ beats all of CO's unpaired hands, middle pairs, and club draws, but loses to any Kx and higher overpairs. This exceeds the 28.6% pot odds, making a call profitable. However, hero is the first responder with BB still to act behind, which means BB could raise (though BB's range after checking to CO is typically weak on K-high boards). The large sizing (66% pot) narrows CO's range toward value, which makes JJ more marginal, but the equity surplus over pot odds (approximately +7-15pp) is sufficient to continue. Raising would be too aggressive without a draw or the nuts.
**Solver verification:** YES — MEDIUM-confidence CALL flagged per rules

---

### FB-06
**Board:** Jd 8s 6h | **Street:** Flop
**Hero:** BB — CLOSING ACTION (CO bet, BTN folded, BB last)
**Hero cards:** 9c 7c
**Pot:** 90 | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (90 + 30 + 30) = 20%

**GTO Action:** CALL — Confidence: HIGH
**Reasoning:** Hero holds 9c 7c — an open-ended straight draw (any T or 5 completes the straight, 8 outs) on a connected rainbow board Jd 8s 6h. Hero's raw equity is approximately 32% from 8 straight outs (roughly 4% per out on the flop with two cards to come). This comfortably exceeds the 20% pot odds threshold by 12 percentage points. Hero closes action with BTN already folded, so there is no squeeze risk behind. The small bet sizing (33% pot) gives hero an excellent price to continue drawing. The rainbow texture means no flush draws compete for outs, and hero's straight draw is to the effective nuts (T-high straight on J-8-6 is only beaten by a QT straight which needs a T to complete as well). Raising is not justified per KB Section 1.7: hero has no flush draw blocker and the board is rainbow, so the semi-bluff conditions are not met. A clean call captures full draw equity at a cheap price.
**Solver verification:** NO

---

### FB-07
**Board:** Jd 8s 6h | **Street:** Flop
**Hero:** CO — SANDWICH (BB donk bet, BTN still behind hero)
**Hero cards:** As Kc
**Pot:** 90 | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25%

**GTO Action:** FOLD — Confidence: HIGH
**Reasoning:** Hero holds AK offsuit — two overcards with no made hand and no draw on Jd 8s 6h, a connected rainbow board. Hero has approximately 18-22% equity (six overcard outs, but many are tainted because an A or K on the turn merely gives top pair with reverse implied odds against BB's donk-bet range which connects heavily with this middling connected texture). BB's donk bet into the PFA on J-8-6 represents a range rich in top pairs (Jx), two pairs (J8, 86), sets, and straight draws (T9, 97, 75) — this board smashes the BB defending range far more than the CO opening range. Hero is in the sandwich position with BTN still behind (per KB Section 1.5, sandwich must fold approximately 80%), and AK has zero draw equity on a rainbow board with no backdoor flush potential through the club suit alone. Even without the sandwich penalty, raw equity (~20%) barely meets pot odds (25%) and OOP equity realisation (60-80%) pushes realised equity well below threshold. This is a clear fold.
**Solver verification:** NO

---

### FB-08
**Board:** Qh 7h 3s | **Street:** Flop
**Hero:** CO — SANDWICH (BB donk bet, BTN still behind hero)
**Hero cards:** Ah Jh
**Pot:** 90 | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25%

**GTO Action:** RAISE — Confidence: MEDIUM
**Reasoning:** Hero holds Ah Jh — the nut flush draw on a two-tone heart board (Qh 7h 3s) with an overcard Ace and a backdoor straight component. This hand meets the semi-bluff carve-out conditions from KB Section 1.7: (1) nut draw (nut flush draw via Ah), (2) blocker effect (Ah blocks opponent nut flush draw holdings), (3) substantial side equity from the Ace overcard (~3 additional outs for top pair) and the Jack as a high kicker. Hero's total equity is approximately 40-45% (9 flush outs + 3 Ace outs minus overlap, plus some backdoor equity). Although hero is in the sandwich position with BTN behind, the KB states that position can be "any (even OOP)" when the blocker and draw equity conditions are met. The Ah blocker is particularly powerful here: it removes the most dangerous nut flush combos from both BB's and BTN's ranges, increasing fold equity substantially. BB's donk bet on Qh 7h 3s likely represents a polarised range (Qx value hands or flush draws), and hero's raise with the nut blocker puts maximum pressure on both opponents. The medium confidence reflects the sandwich risk from BTN potentially holding a strong heart draw or made hand.
**Solver verification:** YES — RAISE action flagged; also MEDIUM confidence in sandwich position

---

## Card Conflict Check

| Board | Cards | Situations | Hero cards | Conflict? |
|-------|-------|------------|------------|-----------|
| FB-B01 (Ah 6d 2c) | Ah, 6d, 2c | FB-01: 7s 6s | No (6s != 6d) -- WAIT: 6s has rank 6, board has 6d. Different suits, OK. | NO |
| FB-B01 (Ah 6d 2c) | Ah, 6d, 2c | FB-02: Kd Qs | | NO |
| FB-B01 (Ah 6d 2c) | Ah, 6d, 2c | FB-03: Jd Td | | NO |
| FB-B02 (Kc 8c 4d) | Kc, 8c, 4d | FB-04: Ac 5c | | NO |
| FB-B02 (Kc 8c 4d) | Kc, 8c, 4d | FB-05: Js Jh | | NO |
| FB-B03 (Jd 8s 6h) | Jd, 8s, 6h | FB-06: 9c 7c | | NO |
| FB-B03 (Jd 8s 6h) | Jd, 8s, 6h | FB-07: As Kc | | NO |
| FB-B04 (Qh 7h 3s) | Qh, 7h, 3s | FB-08: Ah Jh | | NO |

All hero cards verified: no card appears on its board.

---

## Summary Table

| FB | Board | Hero Pos | Hero Role | Hero Cards | Pot Odds | GTO Action | Confidence | Solver Flag |
|----|-------|----------|-----------|------------|----------|------------|------------|-------------|
| FB-01 | Ah 6d 2c | BB | Closing | 7s 6s | 20% | FOLD | HIGH | NO |
| FB-02 | Ah 6d 2c | BTN | IP Closing | Kd Qs | 20% | CALL | HIGH | NO |
| FB-03 | Ah 6d 2c | BB | Bet-and-call | Jd Td | 16.7% | FOLD | HIGH | NO |
| FB-04 | Kc 8c 4d | BB | Closing | Ac 5c | 25% | RAISE | HIGH | YES |
| FB-05 | Kc 8c 4d | BTN | First resp. | Js Jh | 28.6% | CALL | MEDIUM | YES |
| FB-06 | Jd 8s 6h | BB | Closing | 9c 7c | 20% | CALL | HIGH | NO |
| FB-07 | Jd 8s 6h | CO | Sandwich | As Kc | 25% | FOLD | HIGH | NO |
| FB-08 | Qh 7h 3s | CO | Sandwich | Ah Jh | 25% | RAISE | MEDIUM | YES |

**Action distribution:** 3 CALL, 3 FOLD, 2 RAISE (target met)
**Solver flags:** 3 situations (FB-04, FB-05, FB-08)
