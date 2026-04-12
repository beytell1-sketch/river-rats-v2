# Fresh Labels — Agent E — FB-33 through FB-40
**Date:** 2026-04-13
**Author:** GTO Expert Agent E
**Scope:** 8 facing-bet 3-way postflop situations (FB-33 to FB-40)
**Sources:** PHASE1_GATE_VALIDATION (validated action strings), REDESIGN_5 (corrected specs for FB-33/34/37), REDESIGN_12 (corrected specs for FB-35/39), ML_ARCHITECT_FACING_BET_TEST_SET (board details), knowledge/three_way_gto.md (GTO reasoning framework)

---

## Labels

### FB-33
**Board:** Th Td 7c | **Street:** Flop
**Hero:** CO — CLOSING ACTION (BTN bet, BB called, CO last to act)
**Hero cards:** Jc Jd
**Pot (before action):** 90 | **Bet:** 60 | **BB call:** 60 | **Pot after BB call:** 210 | **To call:** 60
**Pot odds:** 60 / (210 + 60) = 60 / 270 = 22%

**GTO Action:** CALL — Confidence: HIGH
**Reasoning:** Hero holds pocket Jacks — an overpair on Th Td 7c. The paired board creates reverse implied odds (trip tens dominate hero), but the bet-and-call sequence must be interpreted carefully. BTN opened and c-bet 66% pot on a paired board; BB cold-called. BB's call on T-T-7 paired board represents a range that includes: pocket pairs (77 for a full house, 88-99 for underpairs with showdown value, QQ-AA for overpairs), some Tx hands (but these are less likely given the pair on board uses two T's — only two remaining T combos exist), and speculative floats. BTN's betting range is wide given IP position on a board where opponents rarely connect strongly. Hero's JJ has approximately 55-65% equity against the combined ranges — JJ beats all non-T holdings below QQ, all bluffs, and all speculative calls. At 22% pot odds, hero has a massive equity surplus of 30+ percentage points. The bet-and-call signal narrows ranges per KB Section 2 Factor 5, but the MW-30 correction applies: when equity exceeds pot odds by this margin with a made hand (overpair), the action-implied narrowing is insufficient to flip the decision. JJ is firmly in CO's continuing range. Raising is rejected: on a paired board, non-set made hands default to CALL per KB Section 1.7 (any draw on a paired board = call at best; the same logic extends to non-trip overpairs where a raise folds out worse and gets called/raised only by better).
**Solver verification:** NO

---

### FB-34
**Board:** As 9s 4s | **Street:** Flop
**Hero:** CO — CLOSING ACTION (BTN bet, BB called, CO last to act)
**Hero cards:** Ks 6d
**Pot (before action):** 90 | **Bet:** 22 | **BB call:** 22 | **Pot after BB call:** 134 | **To call:** 22
**Pot odds:** 22 / (134 + 22) = 22 / 156 = 14%

**GTO Action:** CALL — Confidence: HIGH
**Reasoning:** Hero holds Ks 6d — the second-nut flush draw on a monotone spade board (As 9s 4s). CO is the preflop aggressor who opened and now faces a small BTN bet after checking. The Ks gives hero the second-nut flush draw (9 spade outs minus the As, 8s, 5s on board and in villain ranges = effectively 8-9 clean outs for a King-high flush). At 14% pot odds, hero needs only ~14% equity to continue. Hero's flush draw alone provides approximately 35% equity on the flop (two cards to come with ~9 outs = 35% by the rule of 4). This is a trivial call — equity exceeds pot odds by over 20 percentage points. The bet-and-call on a monotone board signals that both opponents likely hold at least one spade, but hero's Ks is the second-best flush card available, meaning hero's flush will beat any flush except the nut (As, which is on the board — so hero actually holds the nut flush draw among the players). Even factoring in the monotone texture where made flushes already exist in villain ranges, hero's draw to the nut flush at this price is an automatic continue. Raising is rejected because hero has no made hand yet and the bet-and-call sequence suggests at least one villain has a flush or strong spade draw; raising folds out air and gets called/raised by made flushes and better draws.
**Solver verification:** NO

---

### FB-35
**Board:** Kh 6h 3d Qc | **Street:** Turn
**Hero:** CO — CLOSING ACTION (BTN bet, BB folded, CO last to act)
**Hero cards:** Ah 9h
**Pot (before action):** 150 | **Bet:** 90 | **To call:** 90
**Pot odds:** 90 / (150 + 90 + 90) = 90 / 330 = 27%

**GTO Action:** FOLD — Confidence: MEDIUM
**Reasoning:** Hero holds Ah 9h — the nut heart flush draw on Kh 6h 3d Qc. With one card to come on the turn, hero has 9 flush outs for approximately 18% equity from the flush draw alone, plus ~3 outs for an Ace giving top pair (but this would be bottom of the top-pair range on a K-Q board) for roughly 6% additional equity, totalling approximately 24% raw equity. At 27% pot odds, hero's raw equity falls short by approximately 3 percentage points. Hero is closing action (BB folded), which removes squeeze risk and provides some equity realisation benefit. However, OOP equity realisation even in a closing-action scenario is approximately 75-80% (KB Section 1.5), and 24% x 80% = 19.2% realised equity — significantly below the 27% pot odds threshold. BTN's second barrel of 60% pot on a K-Q board after betting the flop represents a strong range: KQ two pair, Kx strong kicker, QQ, or overpairs. BTN is unlikely to be bluffing at this frequency after already investing on the flop. Hero's nut flush draw would normally qualify for a semi-bluff raise (KB Section 1.7 conditions met: nut draw with Ah blocker), but the turn-only equity of ~24% with a single card to come makes raising more of a commit-or-fold decision at compressed SPR. The equity shortfall relative to pot odds, even accounting for closing-action EQR, tips this to a fold — a narrow fold, which is why confidence is MEDIUM.
**Solver verification:** YES — high-equity FOLD flagged (hero equity within 5pp of pot odds with nut draw)

---

### FB-36
**Board:** Ts 8c 4h Jd | **Street:** Turn
**Hero:** CO — CLOSING ACTION (2-way, BB folded on flop; CO vs BTN heads-up)
**Hero cards:** 9d 7d
**Pot:** 120 | **Bet:** 60 | **To call:** 60
**Pot odds:** 60 / (120 + 60 + 60) = 60 / 240 = 25%

**GTO Action:** RAISE — Confidence: HIGH
**Reasoning:** Hero holds 9d 7d and has made a straight: 7-8-9-T-J. This is the second-nut straight (only Q-9 makes a higher straight with Q-J-T-9-8, but Q9 is unlikely in BTN's range on this board). Hero called BTN's flop bet on Ts 8c 4h with an open-ended straight draw (6-7-8-9 or 7-8-9-T), and the Jd turn completes the nuts. BTN fires a second barrel of 50% pot — BTN's range includes Jx (now top pair), JT (two pair), overpairs (QQ, KK, AA), and continued c-bets with AK/AQ. Hero's straight beats all of these except QT (which makes Q-J-T-9-8 — but this requires the specific Q-T combo and QT is a marginal BTN open at best). Hero has approximately 90%+ equity. The correct play is RAISE for value: hero's straight is disguised (called a small flop bet, turn completes a draw), and BTN's range is strong enough to call a raise with Jx, JT two pair, and overpairs. This is heads-up (BB folded), so hero is raising into a single opponent with a near-nut hand. Per KB Section 1.7, sets and the pure nuts are labelled RAISE — hero's straight qualifies as a nut hand.
**Solver verification:** YES — RAISE action always flagged per rules

---

### FB-37
**Board:** Ac Jh 5d Ks | **Street:** Turn
**Hero:** CO — CLOSING ACTION (BTN bet, BB folded, CO last to act)
**Hero cards:** Ah 5h
**Pot:** 90 | **Bet:** 68 | **To call:** 68
**Pot odds:** 68 / (90 + 68 + 68) = 68 / 226 = 30%

**GTO Action:** CALL — Confidence: HIGH
**Reasoning:** Hero holds Ah 5h — bottom two pair (Aces and Fives) on Ac Jh 5d Ks. All players checked the flop Ac Jh 5d, and BTN now fires a delayed c-bet of 75% pot on the Ks turn. BTN's delayed c-bet range includes: AK (now top two pair, which beats hero), KK (set of Kings — crushes hero), KQ/KJ (top pair or second pair that turned top pair), and some Kx hands that checked back the flop for pot control. BTN also has bluffs: QT (gutshot to Broadway), suited connectors that missed, and hands that are taking a stab after the passive flop. Hero's A5 two pair beats all single-pair hands (AJ, AQ, Kx, Jx), all bluffs, and all pocket pairs below two pair. Hero loses to AK (3 combos with one A and one K removed by board/hero), KK (1 combo remaining), and the unlikely A5s (hero blocks this). Against this range, hero has approximately 50-60% equity. At 30% pot odds, hero has a massive equity surplus. Raising is considered but rejected: raising folds out all the bluffs and worse hands that hero beats, and only gets called or re-raised by the hands that crush hero (AK, KK). Flat-calling preserves the bluffs in BTN's range and allows hero to check-call or value-bet the river. Two pair is a call, not a raise, in a spot where hero's raise range should be the pure nuts (sets, AK).
**Solver verification:** NO

---

### FB-38
**Board:** Ad 9c 3h 2s Kd | **Street:** River
**Hero:** CO — SANDWICH (BB bet, BTN yet to act behind hero)
**Hero cards:** Jd Tc
**Pot:** 90 | **Bet:** 90 | **To call:** 90
**Pot odds:** 90 / (90 + 90 + 90) = 90 / 270 = 33%

**GTO Action:** FOLD — Confidence: HIGH
**Reasoning:** Hero holds Jd Tc — complete air on Ad 9c 3h 2s Kd. Hero has no pair, no draw, and J-high is not a viable showdown hand on a board with an Ace and King. All three streets were checked through until BB donked pot on the river Kd. BB's pot-sized river donk after three streets of passive play is a highly polarised action: BB either has a strong hand slow-played (sets, two pair like A3/A2/K9, or a rivered King that improved a Kx hand to top pair on a board BB deemed too dangerous to lead before) or a pure bluff. Even against a polarised range, hero needs approximately 33% equity to call — and Jd Tc has 0% equity against BB's value range and approximately 100% against bluffs. BB's bluff frequency in a 3-way pot river donk is extremely low (KB Section 1.4: bluff-to-value ratio is approximately 1:4 or tighter 3-way). Additionally, hero is in the sandwich seat with BTN still to act behind. If hero calls, BTN could over-call or raise, compounding the risk. The sandwich penalty (KB Section 1.5: sandwich player must fold approximately 80%) further supports folding. J-high with no showdown value is a clear fold regardless of position — the sandwich merely reinforces it.
**Solver verification:** NO

---

### FB-39
**Board:** Qd 8d 4c 7s Jh | **Street:** River
**Hero:** BB — SANDWICH (BTN bet, CO still to act behind hero)
**Hero cards:** Ts 9s
**Pot:** 150 | **Bet:** 90 | **To call:** 90
**Pot odds:** 90 / (150 + 90 + 90) = 90 / 330 = 27%

**GTO Action:** RAISE — Confidence: HIGH
**Reasoning:** Hero holds Ts 9s — the stone-cold nut straight (7-8-9-T-J) on Qd 8d 4c 7s Jh. The board runout provides a five-card straight using hero's T-9. No higher straight is possible (Q-J-T-9-8 would require K or higher, and Q-T-9-8-7 uses the same T-9 with lower cards). Hero has the absolute nuts. BTN bets 60% pot on the river after a passive turn (BTN checked back the turn). BTN's river bet range includes: QJ (rivered two pair), Jx (rivered top pair), busted diamond draws using the diamond board cards, and thin value bets. CO acts behind hero but this is irrelevant with the nut hand — if CO calls or raises hero's raise, hero wins a bigger pot. The sandwich penalty does not apply to nut hands (KB: "pure bluffs are unprofitable 3-way" applies to bluffs, not to value raises with the nuts). Hero should raise for maximum value. BTN's river bet represents enough strength to call a raise with two pair and sets. CO's potential overcall or squeeze behind only adds to hero's profit. Flat-calling the nuts in a multiway pot forfeits significant value from both opponents.
**Solver verification:** YES — RAISE action always flagged per rules

---

### FB-40
**Board:** Kc 8c 4d | **Street:** Flop
**Hero:** BB — SANDWICH (BTN bet, CO yet to act behind hero)
**Hero cards:** 6s 5s
**Pot:** 90 | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (90 + 30 + 30) = 30 / 150 = 20%

**GTO Action:** FOLD — Confidence: HIGH
**Reasoning:** Hero holds 6s 5s — complete air on Kc 8c 4d. Hero has no pair, no flush draw (wrong suit — spades on a club two-tone board), and only a gutshot straight draw (needs a 7 for 4-5-6-7-8, which is 4 outs for approximately 8% equity on the flop, or roughly 16% across two streets). Even the optimistic two-street equity of 16% falls below the 20% pot odds threshold. Hero is in the sandwich position with CO (the preflop opener) still to act behind. CO checked to BTN but has not folded — CO could raise, and CO's checking range on a K-high board they opened still contains Kx, AK, and overpairs that chose to trap. The sandwich penalty (KB Section 1.5) requires tightening hero's continuing range by 15-20% versus HU cutoffs, which makes this gutshot-only hand deeply unprofitable. Per KB Section 1.7, gutshot-only and backdoor-only hands are check/folds 3-way. Hero has no blocker effect, no flush draw, and no overcards — pure air in the worst position.
**Solver verification:** NO

---

## Summary Table

| FB | Board | Street | Hero Pos | Hero Cards | Action | Confidence | Solver Flag |
|----|-------|--------|----------|------------|--------|------------|-------------|
| FB-33 | Th Td 7c | Flop | CO closing | Jc Jd | CALL | HIGH | NO |
| FB-34 | As 9s 4s | Flop | CO closing | Ks 6d | CALL | HIGH | NO |
| FB-35 | Kh 6h 3d Qc | Turn | CO closing | Ah 9h | FOLD | MEDIUM | YES |
| FB-36 | Ts 8c 4h Jd | Turn | CO closing | 9d 7d | RAISE | HIGH | YES |
| FB-37 | Ac Jh 5d Ks | Turn | CO closing | Ah 5h | CALL | HIGH | NO |
| FB-38 | Ad 9c 3h 2s Kd | River | CO sandwich | Jd Tc | FOLD | HIGH | NO |
| FB-39 | Qd 8d 4c 7s Jh | River | BB sandwich | Ts 9s | RAISE | HIGH | YES |
| FB-40 | Kc 8c 4d | Flop | BB sandwich | 6s 5s | FOLD | HIGH | NO |

**Distribution:** 3 CALL / 3 FOLD / 2 RAISE

**Card conflict check:** All hero cards verified clear of their respective board cards. No intra-batch conflicts. Agent A cards on shared board FB-B02 (Kc 8c 4d) checked: FB-04 uses Ac 5c, FB-05 uses Js Jh — no conflict with FB-40's 6s 5s.

**Solver verification flags:** FB-35 (high-equity FOLD with nut flush draw within 5pp of pot odds), FB-36 (RAISE), FB-39 (RAISE).
