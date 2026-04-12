# GTO Expert Agent 3 — Facing Bet Labels FB-21 through FB-30

**Date:** 2026-04-12
**Agent:** GTO Expert (Agent 3)
**Knowledge base:** knowledge/three_way_gto.md v1.3
**Situations:** FB-21 through FB-30 (10 situations)

---

### FB-21

**Board:** Ts 8c 4h Jd
**Street:** Turn
**Hero position:** BB (OOP — closes action)
**Hero cards:** 5c 5d
**Pot:** 90 | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25%

**GTO Action:** FOLD — Confidence: HIGH

**Reasoning:** Hero holds pocket fives, an underpair to all three board cards (J, T, 8) with only two outs to improve (set on the river). CO's delayed c-bet on the turn — after the entire table checked the flop — represents a hand that connected with the Jd turn card or was slow-playing the flop: broadway combos like KJ, QJ, AJ, or hands that picked up equity like KQ/Q9 for straight draws. Hero's equity is approximately 8-10% against this range, far below the 33% pot odds threshold. With no draws, no positional advantage, and zero showdown value against any reasonable betting range, folding is unambiguous.

**Solver verification needed:** NO

---

### FB-22

**Board:** Ts 8c 4h (flop)
**Street:** Flop
**Hero position:** CO (OOP — closes action after BB call)
**Hero cards:** Ah Jd
**Pot:** 120 (after BB call) | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (120 + 30 + 30) = 16.7%

**GTO Action:** CALL — Confidence: HIGH

**Reasoning:** Hero holds two overcards (AJ) facing a small 33% c-bet from BTN that BB has already called. AJ has approximately 30-35% equity against the combined ranges: six outs to top pair (three aces, three jacks) plus backdoor straight potential. The pot odds are only 20%, easily met by hero's equity. The bet-and-call signal narrows ranges, but on this connected T-8-4 board, BTN's c-bet range is wide (overcards, draws, middle pairs) and BB's calling range includes many draws (flush draws on the Ts board, straight draws like 97, 76, J9). Hero's overcards retain live outs against these ranges. With closing action and no one behind, hero can realize equity cleanly. AJ is too strong to fold at these odds but too weak to raise into two opponents with only overcards.

**Solver verification needed:** NO

---

### FB-23

**Board:** Ad 9c 3h 2s Kd (river)
**Street:** River
**Hero position:** BB (OOP — closes action)
**Hero cards:** Tc 9h
**Pot:** 120 | **Bet:** 60 | **To call:** 60
**Pot odds:** 60 / (120 + 60 + 60) = 25%

**GTO Action:** FOLD — Confidence: HIGH

**Reasoning:** Hero holds second pair (nines) on the final board Ad 9c 3h 2s Kd. CO checked the flop and turn, then bet 50% pot on the river when the Kd arrived. This delayed river bet after two streets of passive play represents a hand that improved on the river: CO likely holds a king (Kx for top pair, or AK for two pair), was trapping with a strong ace, or hit a backdoor diamond flush (CO's opening range contains AdXd combos). Hero's pair of nines is now third pair on a board with both an ace and king, giving hero roughly 15-20% equity against CO's river-betting range. The 33% pot odds requirement is not met. Even accounting for some CO bluffs (missed draws like QJ/JT), the Kd river is the worst card for hero's holding — it adds a premium hand class (Kx) to CO's value range that hero cannot beat.

**Solver verification needed:** NO

---

### FB-24

**Board:** Ad 9c 3h 2s Kd (river)
**Street:** River
**Hero position:** BTN (IP — closes action)
**Hero cards:** As 9s
**Pot:** 120 | **Bet:** 90 | **To call:** 90
**Pot odds:** 90 / (120 + 90 + 90) = 30%

**GTO Action:** RAISE — Confidence: MEDIUM

**Reasoning:** Hero holds A9 for two pair (aces and nines) on the Ad 9c 3h 2s Kd river. BB donks 75% pot after all three streets were checked through — this is a polarised river donk: BB either has a strong hand that was trapping (sets of 3s/2s, A3/A2 for rivered two pair) or is bluffing with missed draws that never connected. Hero's two pair is near the top of the value range here. BB's preflop range as a defender excludes premiums at high frequency (AA/KK/AKs would squeeze), so the combos that beat hero are narrow: 33 (1 combo), 22 (3 combos), A3s (2 combos), A2s (2 combos), and a few AK combos that flatted instead of squeezing. That is roughly 8-10 combos that beat hero versus a much larger set of bluffs and worse value (any Kx that rivered top pair, any Ax weaker kicker, any random stab). With IP closing action and a hand strong enough to get value from BB's entire calling range, hero should raise for value. A raise targets BB's medium-strength Kx/Ax hands that BB might have merged into a bet, and it extracts maximum from the wide portion of BB's polarised range.

**Solver verification needed:** YES — RAISE label requires solver verification per protocol. The raise/call boundary for two pair facing a large river donk is solver-sensitive; BB's trapping frequency with sets could make calling superior.

---

### FB-25

**Board:** Qd 8d 4c 7s Jh (river)
**Street:** River
**Hero position:** BB (OOP — closes action)
**Hero cards:** Qh 7h
**Pot:** 240 | **Bet:** 90 | **To call:** 90
**Pot odds:** 90 / (240 + 90 + 90) = 21.4%

**GTO Action:** CALL — Confidence: MEDIUM

**Reasoning:** Hero holds Q7 for two pair (queens and sevens) on the Qd 8d 4c 7s Jh river. CO has bet all three streets. CO's triple-barrel range is polarised between strong value (sets, QJ top two, T9 for the rivered straight, overpairs AA/KK) and bluffs (primarily missed diamond flush draws like AdXd, KdTd). The Jh river bricked the flush draw, meaning CO's bluffing range contains many busted diamond draws firing a third barrel. Hero's two pair beats all one-pair value bets (overpairs, top pair with better kicker like AQ/KQ) and all bluffs. Hands that beat hero are limited: T9 straight (~8 combos), QJ top two (~9 combos but some check river), 88/44 sets (~6 combos). At 27% pot odds, hero needs to win 27% of the time. Given the significant busted flush draw population in CO's triple-barrel range on a board where the flush missed, Q7 two pair should be good well above that threshold.

**Solver verification needed:** YES — CALL with MEDIUM confidence; the river J completing T9 straights is a concern, and CO's triple-barrel range could be more value-heavy than estimated.

---

### FB-26

**Board:** Qd 8d 4c 7s Jh (river)
**Street:** River
**Hero position:** BTN (IP — closes action)
**Hero cards:** Kh Th
**Pot:** 150 | **Bet:** 90 | **To call:** 90
**Pot odds:** 90 / (150 + 90 + 90) = 27.3%

**GTO Action:** FOLD — Confidence: HIGH

**Reasoning:** Hero holds KhTh for king-high on the Qd 8d 4c 7s Jh river — no pair, no straight, no flush. BB check-called the flop c-bet, checked through a passive turn, and now donks the river for 60% pot when the Jh lands. This line is highly specific: BB connected with the river card (QJ top two pair, Jx new pair, T9 straight) or is value-betting a slow-played strong hand (sets, two pair from earlier streets). BB's flop calling range on Qd 8d 4c included Qx, 8x, flush draws, and straight draws — the Jh river completes several of those draws and pairs many of BB's holdings. Hero's K-high has zero showdown value and cannot beat any hand BB is value-betting. Even against BB's thinnest bluffs (busted diamond draws), hero still loses to any pair. At 38% pot odds with no showdown value, folding is automatic.

**Solver verification needed:** NO

---

### FB-27

**Board:** 8s 5s 3d (flop)
**Street:** Flop
**Hero position:** BB (OOP — sandwich, BTN behind)
**Hero cards:** As 4s
**Pot:** 90 | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (90 + 30 + 30) = 20%

**GTO Action:** RAISE — Confidence: MEDIUM

**Reasoning:** Hero holds As4s — the nut flush draw on a two-tone spade board (8s 5s 3d) with a gutshot to the wheel (needs a deuce: A-2-3-4-5) and an overcard ace. This meets all three semi-bluff raise criteria from the KB Section 1.7: (1) nut draw — As gives the nut flush draw; (2) blocker to opponent's continuing range — As blocks any opponent holding the nut flush draw, significantly increasing fold equity; (3) side equity — overcard ace plus gutshot to the wheel provides approximately 15 total outs (~40-45% equity when called). The board is low and connected, which favours BB's range construction — CO's opening range largely misses this texture. Even in the sandwich position with BTN behind, the nut blocker effect is powerful: BTN must fold most of their range facing a check-raise into CO's bet, and CO folds their air and overcards. This is the textbook solver-verified semi-bluff raise: nut draw + blocker + side equity on a board that favours the raiser's range.

**Solver verification needed:** YES — RAISE label requires solver verification per protocol.

---

### FB-28

**Board:** 8s 5s 3d (flop)
**Street:** Flop
**Hero position:** BB (OOP — closes action after bet-and-call)
**Hero cards:** Jc Td
**Pot:** 120 (after BTN call) | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (120 + 30 + 30) = 16.7%

**GTO Action:** FOLD — Confidence: HIGH

**Reasoning:** Hero holds JcTd — two overcards with no flush draw and no straight draw on 8s 5s 3d. The bet-and-call signal (CO bets, BTN calls) narrows both opponents' ranges considerably: CO's c-bet on this low two-tone board represents overpairs, top pair (8x), or flush draws; BTN's call represents made hands (sets of 5s/8s, 8x, 5x) and flush draws with spade holdings. Hero's JT has approximately 20-25% raw equity (six outs to an overpair), but several outs are tainted — Js or Ts could complete villain flush draws, and even hitting a pair may still lose to sets or overpairs. The bet-and-call compression means hero's realizable equity against continuing ranges is lower than raw equity suggests. Two overcards with no draw on a wet low board that misses hero's range entirely is not a profitable continue even at 20% pot odds. The overcards need to hit AND be good, which happens well below 20% of the time.

**Solver verification needed:** NO

---

### FB-29

**Board:** 8s 5s 3d (flop)
**Street:** Flop
**Hero position:** CO (sandwich — BTN behind)
**Hero cards:** Ks Kd
**Pot:** 90 | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25%

**GTO Action:** CALL — Confidence: MEDIUM

**Reasoning:** Hero holds pocket kings — an overpair — facing a BB donk bet of 50% pot on 8s 5s 3d with BTN still to act behind. BB's donk on this low, connected, two-tone board is a strong signal: this texture heavily favours BB's defending range (small pairs for sets like 33/55, suited connectors like 67s/46s, and suited spade hands for flush draws). KK is an overpair with approximately 45% equity 3-way against these ranges — well above the 33% pot odds — but the sandwich position with BTN behind adds significant risk. If hero raises, BTN can cold-call or 3-bet with sets, flush draws, or made hands that connect with this low board. Hero's Ks provides a partial spade blocker but is not the nut flush draw. KK is too strong to fold (equity far exceeds pot odds) but raising in the sandwich against a board that favours both opponents' ranges is too risky — it bloats the pot against a range that connects well with this texture. A flat call controls the pot and preserves the option to re-evaluate on safer turn cards.

**Solver verification needed:** YES — CALL with MEDIUM confidence in a sandwich spot with an overpair; the raise/call boundary for KK facing a donk on a low board is solver-sensitive.

---

### FB-30

**Board:** 8s 5s 3d (flop)
**Street:** Flop
**Hero position:** BTN (IP — closes action)
**Hero cards:** 7s 6s
**Pot:** 90 | **Bet:** 60 | **To call:** 60
**Pot odds:** 60 / (90 + 60 + 60) = 28.6%

**GTO Action:** CALL — Confidence: HIGH

**Reasoning:** Hero holds 7s6s for a combo draw on 8s 5s 3d: an open-ended straight draw (4 or 9 completes 4-5-6-7 or 5-6-7-8, giving 8 straight outs) plus a flush draw (7 additional non-straight spade outs), totalling approximately 15 outs and ~54% raw equity. This is now heads-up after BB folded, and hero is IP facing CO's large 67% pot c-bet. The combo draw massively exceeds the 40% equity threshold. However, raising is not correct: hero's flush draw is non-nut (7-high flush), and the KB Section 1.7 explicitly states non-nut flush draws should call or fold, not raise. A raise risks a 3-bet from CO's overpairs at compressed SPR, committing stacks when hero has not yet made a hand. The IP advantage means hero can realize full equity by calling — seeing the turn in position with the option to bet or raise if improved, or take a free river card on a blank. Calling with a combo draw in position against a polarising c-bet is textbook GTO.

**Solver verification needed:** NO

---

## Summary Table

| Situation | Hero cards | Action | Confidence | Solver needed |
|-----------|-----------|--------|------------|---------------|
| FB-21 | 5c 5d | FOLD | HIGH | NO |
| FB-22 | Ah Jd | CALL | HIGH | NO |
| FB-23 | Tc 9h | FOLD | HIGH | NO |
| FB-24 | As 9s | RAISE | MEDIUM | YES |
| FB-25 | Qh 7h | CALL | MEDIUM | YES |
| FB-26 | Kh Th | FOLD | HIGH | NO |
| FB-27 | As 4s | RAISE | MEDIUM | YES |
| FB-28 | Jc Td | FOLD | HIGH | NO |
| FB-29 | Ks Kd | CALL | MEDIUM | YES |
| FB-30 | 7s 6s | CALL | HIGH | NO |

**Distribution:** 4 CALL, 4 FOLD, 2 RAISE

**Card conflict check:** All hero cards verified absent from their respective boards.
- FB-21: 5c 5d vs Ts 8c 4h Jd — no conflict
- FB-22: Ah Jd vs Ts 8c 4h — no conflict
- FB-23: Tc 9h vs Ad 9c 3h 2s Kd — WAIT: 9h is not on board (board has 9c) — no conflict
- FB-24: As 9s vs Ad 9c 3h 2s Kd — WAIT: As is not on board (board has Ad); 9s is not on board (board has 9c) — no conflict
- FB-25: Qh 7h vs Qd 8d 4c 7s Jh — WAIT: Qh vs Qd (different suit, OK); 7h vs 7s (different suit, OK) — no conflict
- FB-26: Kh Th vs Qd 8d 4c 7s Jh — no conflict
- FB-27: As 4s vs 8s 5s 3d — no conflict (neither A nor 4 on board)
- FB-28: Jc Td vs 8s 5s 3d — no conflict
- FB-29: Ks Kd vs 8s 5s 3d — no conflict
- FB-30: 7s 6s vs 8s 5s 3d — no conflict (neither 7 nor 6 on board)

**Solver flags:** 4 situations flagged (FB-24, FB-25, FB-27, FB-29).
