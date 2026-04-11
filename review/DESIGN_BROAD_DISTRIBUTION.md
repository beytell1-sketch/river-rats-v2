# Design: Broad Distribution Situations for v9-3way

**Date:** 7 April 2026
**Status:** DESIGN — awaiting review before labelling
**Purpose:** General coverage across the full 3-way decision space. Prevents
overfitting to targeted categories (semi-bluff, flush-blocking, overcards,
thin value). Insurance against axis bias.
**Budget:** 73 situations across 9 boards

---

## Design Principles

1. **No axis targeting.** These boards are not designed to activate any
   specific feature or teach any specific lesson. They sample the natural
   distribution of 3-way postflop decisions.
2. **Board diversity:** dry, wet, paired, ace-high, low, middling, monotone.
   Each board is distinct from all other category designs.
3. **Street distribution:** 80% turn/river (7 of 9 boards). Compensates
   for semi-bluff category's flop-heavy weighting.
4. **Position diversity:** mix of IP, OOP, sandwich.
5. **Action diversity:** facing bet, not facing bet, facing raise,
   multi-street aggression.
6. **Hand diversity:** every hand category represented across the batch.
7. ~8 hands per board.

---

## Board BD1: Ac Kd 7h (Flop) — Ace-High Dry, Standard 3-Way Flop

**Board:** Ac Kd 7h
**Street:** Flop
**Hero position:** CO (IP, opener)
**Villain positions:** BTN (cold-caller), BB (defender)
**Pot:** 90
**To call:** 0 (hero first to act postflop as opener)
**Facing bet:** No
**Action history:** CO (hero) opens, BTN calls, BB defends.

AK-high dry board favours opener's range heavily. Standard c-bet spot.

| # | Hero Hand | Category | Equity Est. | Notes |
|---|-----------|----------|-------------|-------|
| 1 | Ah Qh | top_pair (6) | ~0.65 | TP + strong kicker. C-bet for value |
| 2 | Kc Jc | middle_pair (5) | ~0.45 | Second pair. C-bet or pot control? |
| 3 | Td Ts | underpair (4) | ~0.35 | Underpair to board. Check or small c-bet? |
| 4 | Qd Jd | high_card (0) | ~0.20 | Two overcards to 7 but under A/K. Gutshot (T-J-Q) |
| 5 | 9h 8h | high_card (0) | ~0.15 | Backdoor draws only. Give up or small stab? |
| 6 | Ad 7d | two_pair (10) | ~0.75 | Top two pair. Bet for value + protection |
| 7 | 7c 7d | set (12) | ~0.85 | Bottom set. Bet or slowplay? |
| 8 | 6h 5h | high_card (0) | ~0.08 | Complete air. Check behind |

**8 situations.**

---

## Board BD2: 5d 5c 9h Jd (Turn) — Paired Board, Turn Action

**Board:** 5d 5c 9h Jd
**Street:** Turn
**Hero position:** BTN (IP)
**Villain positions:** CO (opener, bettor), BB (defender)
**Pot:** 200 (90 preflop, CO bet 33 flop, BB called, BTN called. Turn pot ~200)
**To call:** 70 (CO bets 70 into 200)
**Facing bet:** Yes
**Action history:** CO opens, BTN (hero) calls, BB defends. Flop 5d 5c 9h:
CO bets 33, BB calls, BTN calls. Turn Jd: CO bets 70. BB folds.

Paired board. CO double-barrel on a paired + J board. Only trips+ beats
the pair. Tests hero's response to aggression on a dry paired texture.

| # | Hero Hand | Category | Equity Est. | Notes |
|---|-----------|----------|-------------|-------|
| 1 | Jh Th | top_pair (6) | ~0.55 | Turned TP on paired board. Call or fold? |
| 2 | 9c 8c | middle_pair (5) | ~0.30 | Pair of 9s. Weaker — fold to double barrel? |
| 3 | Ah Ad | overpair (9) | ~0.65 | AA on paired board. Call confidently |
| 4 | Kh Kd | overpair (9) | ~0.60 | KK — strong but J on turn worries |
| 5 | 5h 4h | trips (11) | ~0.80 | Trips. Raise or slowplay the double barrel? |
| 6 | Qd Td | high_card (0) | ~0.15 | Gutshot (8-9-T-J-Q). Speculative call or fold? |
| 7 | Ac 5s | trips (11) | ~0.85 | A5 trips with top kicker. Raise for value |
| 8 | 7c 6c | high_card (0) | ~0.10 | Air with gutshot potential. Fold |

**8 situations.**

---

## Board BD3: Td 8c 3h 6s (Turn) — Medium Wet Board, Not Facing Bet

**Board:** Td 8c 3h 6s
**Street:** Turn
**Hero position:** BB (OOP)
**Villain positions:** CO (opener), BTN (cold-caller)
**Pot:** 180 (90 preflop, CO bet 30 flop, BTN called, BB called. Turn 6s:
CO checks, BTN checks.)
**To call:** 0 (both opponents checked)
**Facing bet:** No
**Action history:** CO opens, BTN calls, BB (hero) defends. Flop Td 8c 3h:
CO bets 30, BTN calls, BB calls. Turn 6s: CO checks, BTN checks.

Medium board, both opponents showed weakness on turn. Hero OOP but has
closing action (opponent checks in front). Bet or check?

| # | Hero Hand | Category | Equity Est. | Notes |
|---|-----------|----------|-------------|-------|
| 1 | Td 9d | top_pair (6) | ~0.55 | TP decent kicker. Bet the weakness or check? |
| 2 | 8h 7h | middle_pair (5) | ~0.40 | Second pair + gutshot. Check or value bet? |
| 3 | Jc 9c | high_card (0) | ~0.25 | OESD (7-8-9-T-J). Bet as semi-bluff? |
| 4 | 3c 2c | bottom_pair (3) | ~0.18 | Bottom pair. Pure check, showdown value |
| 5 | 6d 6c | set (12) | ~0.85 | Turned set. Bet for value + protection |
| 6 | Ah Kh | overcards (2) | ~0.22 | Two overcards. Bluff the weakness? |
| 7 | 5c 4c | high_card (0) | ~0.20 | OESD (3-4-5-6-7). Bet or realize equity? |
| 8 | Tc 8d | two_pair (10) | ~0.70 | Top two pair. Clear value bet |

**8 situations.**

---

## Board BD4: Kh 9d 4c 2s Jc (River) — Dry Board, River Decision Facing Bet

**Board:** Kh 9d 4c 2s Jc
**Street:** River
**Hero position:** SB (OOP)
**Villain positions:** CO (opener, bettor), BTN (cold-caller)
**Pot:** 300 (90 preflop, CO bet 30 flop, BTN called, SB called = 180.
Turn: all check = 180. River Jc: CO bets 120 into 180.)
**To call:** 120
**Facing bet:** Yes
**Action history:** CO opens, BTN calls, SB (hero) calls. Flop Kh 9d 4c:
CO bets 30, BTN calls, SB calls. Turn 2s: all check. River Jc: CO bets
120 into 180. BTN folds.

CO bet flop, checked turn, then fired big on river J. J is a card that
helps CO's range (KJ, QJ, JT). Hero OOP facing a big river bet after
checked turn. Call/fold decision.

| # | Hero Hand | Category | Equity Est. | Notes |
|---|-----------|----------|-------------|-------|
| 1 | Kd Qd | top_pair (6) | ~0.45 | TPSK. Big river bet after turn check — call or fold? |
| 2 | Kc Tc | top_pair (6) | ~0.35 | TPWK. Facing big bet — likely fold? |
| 3 | 9h 8h | middle_pair (5) | ~0.20 | Second pair. Fold to big river bet |
| 4 | Jd Td | middle_pair (5) | ~0.40 | Rivered pair of J. Call — villain could be bluffing |
| 5 | Ah Ad | overpair (9) | ~0.55 | AA. River J doesn't complete any draw — call |
| 6 | Kh Jh | two_pair (10) | ~0.70 | Rivered top two. Easy call |
| 7 | Ac 5c | high_card (0) | ~0.08 | Air + backdoor club miss. Fold |
| 8 | Qd Td | high_card (0) | ~0.10 | QT — rivered gutshot? No, Q-T-J is 3 cards. Fold |

**8 situations.**

---

## Board BD5: 7h 4d 2c Qd 9s (River) — Low Flop, Q Turn, Brick River

**Board:** 7h 4d 2c Qd 9s
**Street:** River
**Hero position:** CO (IP, opener)
**Villain positions:** BTN (cold-caller), BB (defender, bettor)
**Pot:** 280 (90 preflop, CO checked flop, BTN checked, BB bet 40, CO called,
BTN folded = 170. Turn Qd: BB bet 55, CO called = 280. River 9s: BB checks.)
**To call:** 0 (BB checked river)
**Facing bet:** No
**Action history:** CO (hero) opens, BTN calls, BB defends. Flop 7h 4d 2c:
CO checks, BTN checks, BB bets 40, CO calls, BTN folds. Turn Qd: BB bets
55, CO calls. River 9s: BB checks.

BB led two streets then checked river. Hero IP with closing action. BB's
check could be a trap or giving up. Bet/check decision with information
from multi-street aggression pattern.

| # | Hero Hand | Category | Equity Est. | Notes |
|---|-----------|----------|-------------|-------|
| 1 | Qh Jh | top_pair (6) | ~0.55 | Paired Q on turn. BB checked river — value bet? |
| 2 | 7c 6c | middle_pair (5) | ~0.25 | Pair of 7s. BB's range stronger — check behind |
| 3 | Ad Kd | high_card (0) | ~0.20 | Two overcards + diamond backdoor. Bluff river? |
| 4 | Ah Qc | top_pair (6) | ~0.60 | TPGK (Q). Value bet river after BB checks |
| 5 | 9c 8c | middle_pair (5) | ~0.35 | Rivered pair of 9. Thin value or check? |
| 6 | Kh Kc | overpair (9) | ~0.50 | KK — overcalled by Q on turn, held up? Bet thin? |
| 7 | 5d 3d | high_card (0) | ~0.15 | OESD hit? No — 5-3 doesn't make straight. Air |
| 8 | Ac 2c | bottom_pair (3) | ~0.18 | Bottom pair (2s). Check behind for showdown |

**8 situations.**

---

## Board BD6: 9c 7c 2d Kh (Turn) — Facing Raise, 3-Way Pot

**Board:** 9c 7c 2d Kh
**Street:** Turn
**Hero position:** CO (IP, opener)
**Villain positions:** BB (defender), BTN (cold-caller, raiser)
**Pot:** 300 (90 preflop, CO bet 30 flop, BTN called, BB called = 180.
Turn Kh: CO bets 60, BB calls, BTN raises to 180. Hero faces 120 more.)
**To call:** 120 (BTN raised CO's bet, BB already called)
**Facing bet:** Yes (facing raise specifically)
**Action history:** CO (hero) opens, BTN calls, BB defends. Flop 9c 7c 2d:
CO bets 30, BTN calls, BB calls. Turn Kh: CO bets 60, BB calls, BTN raises
to 180.

Hero faces a RAISE on the turn in a 3-way pot. BTN raising after BB
called = very strong signal. Tests facing_raise feature and hero response
to turn aggression.

| # | Hero Hand | Category | Equity Est. | Notes |
|---|-----------|----------|-------------|-------|
| 1 | Kd Qd | top_pair (6) | ~0.35 | Turned TP. BTN raise = very strong. Fold? |
| 2 | Kc Jc | top_pair (6) | ~0.40 | TP + club FD redraw. Call the raise? |
| 3 | 9d 9h | set (12) | ~0.75 | Set of 9s. Re-raise or call and trap? |
| 4 | Ah Ac | overpair (9) | ~0.45 | AA facing turn raise. Call reluctantly? |
| 5 | Ac 8c | high_card (0) | ~0.30 | NFD + Ac blocker. Call draw odds or fold? |
| 6 | 7d 6d | middle_pair (5) | ~0.15 | Second pair. Fold to turn raise |
| 7 | Kh 9d | two_pair (10) | ~0.65 | Turned top two. Call or re-raise? |
| 8 | Td 8d | high_card (0) | ~0.22 | OESD (6-7-8-9-T). Paying to draw vs raise |

**8 situations.**

---

## Board BD7: Jh 8d 5c Qc 4h (River) — Medium Board, River Call/Fold

**Board:** Jh 8d 5c Qc 4h
**Street:** River
**Hero position:** BTN (IP)
**Villain positions:** HJ (opener, bettor), BB (defender)
**Pot:** 350 (90 preflop, HJ bet 33 flop, BB called, BTN called = 200.
Turn Qc: HJ bet 75, BB folded, BTN called = 350. River 4h: HJ bets 100.)
**To call:** 100
**Facing bet:** Yes
**Action history:** HJ opens, BTN (hero) calls, BB defends. Flop Jh 8d 5c:
HJ bets 33, BB calls, BTN calls. Turn Qc: HJ bets 75, BB folds, BTN calls.
River 4h: HJ bets 100 into 350.

HJ triple-barrelled. River 4h is a blank. Hero called two streets —
has showdown value to evaluate. Third barrel = strong or bluff?

| # | Hero Hand | Category | Equity Est. | Notes |
|---|-----------|----------|-------------|-------|
| 1 | Jc Tc | middle_pair (5) | ~0.35 | Pair of J, was TP on flop. Call 3rd barrel? |
| 2 | Qh Jd | two_pair (10) | ~0.65 | Two pair Q+J. Turned top pair. Call easily |
| 3 | 8c 7c | middle_pair (5) | ~0.20 | Pair of 8. Fold to triple barrel |
| 4 | Ah Jh | middle_pair (5) | ~0.40 | AJ — good kicker on J. Call the river? |
| 5 | 9h 7h | high_card (0) | ~0.15 | Busted straight draw (5-6-7-8-9 missed). Fold |
| 6 | Qd Td | top_pair (6) | ~0.50 | Turned TP (Q). Hero call or fold 3rd barrel? |
| 7 | 5d 5h | set (12) | ~0.80 | Bottom set. Easy call, consider raise |
| 8 | Kh Kd | overpair (9) | ~0.45 | KK. Q on turn was scary — call 3rd barrel? |

**8 situations.**

---

## Board BD8: 6h 3d 2h 9c Ks (River) — Low Flop, Scary Runout, River Check

**Board:** 6h 3d 2h 9c Ks
**Street:** River
**Hero position:** BB (OOP)
**Villain positions:** CO (opener), BTN (cold-caller)
**Pot:** 180 (90 preflop, all checked flop. Turn 9c: BB bet 45, CO called,
BTN folded = 180. River Ks: hero to act.)
**To call:** 0 (not facing bet — hero to act first)
**Facing bet:** No
**Action history:** CO opens, BTN calls, BB (hero) defends. Flop 6h 3d 2h:
all check. Turn 9c: BB bets 45, CO calls, BTN folds. River Ks: hero first.

Hero led turn, CO called. River K is a scare card for CO's range. Hero
OOP on river — bet again or check? CO calling turn could be floating or
have a pair.

| # | Hero Hand | Category | Equity Est. | Notes |
|---|-----------|----------|-------------|-------|
| 1 | 6c 5c | middle_pair (5) | ~0.30 | Pair of 6. Was value on turn — river K scary. Check? |
| 2 | 9h 8h | top_pair (6) | ~0.45 | Pair of 9. Turn top pair, river K scares. Bet or check? |
| 3 | Ah 4h | high_card (0) | ~0.20 | NFD missed (hearts). Busted draw. Bluff river K? |
| 4 | Kd Jd | top_pair (6) | ~0.55 | Rivered TP (K). Value bet the river? |
| 5 | 2c 2d | set (12) | ~0.75 | Bottom set. River K changes nothing — value bet |
| 6 | 7h 5h | high_card (0) | ~0.15 | Busted FD + gutshot. River bluff? |
| 7 | 9d Td | top_pair (6) | ~0.42 | Pair of 9 + T kicker. Bet again or check-call? |
| 8 | Qc Jc | high_card (0) | ~0.12 | Overcards. River K = give up or bluff? |

**8 situations.**

---

## Board BD9: Qh 9h 4d Th (Turn) — Flush Completed, Action-Heavy

**Board:** Qh 9h 4d Th
**Street:** Turn
**Hero position:** SB (OOP, sandwich)
**Villain positions:** CO (opener), BTN (cold-caller, bettor)
**Pot:** 180 (90 preflop, all checked flop. Turn Th: CO checks, BTN bets 45.)
**To call:** 45
**Facing bet:** Yes
**Action history:** CO opens, BTN calls, SB (hero) calls. Flop Qh 9h 4d:
all check. Turn Th: CO checks, BTN bets 45 into 90+.

Three hearts on turn — flush completed. BTN bets after flop checked
through. Hero is in the sandwich (OOP, CO still behind). Tests sandwich
position decisions on a scary board.

| # | Hero Hand | Category | Equity Est. | Notes |
|---|-----------|----------|-------------|-------|
| 1 | Ah Kh | flush (14) | ~0.85 | Nut flush. Raise or slowplay the turn bet? |
| 2 | Kh Jh | flush (14) | ~0.75 | 2nd nut flush. Raise or call? |
| 3 | Qd Jd | top_pair (6) | ~0.30 | TP on flush board. Call or fold in sandwich? |
| 4 | 9c 8c | middle_pair (5) | ~0.15 | Second pair on scary board. Fold |
| 5 | Jh 8h | flush (14) | ~0.65 | Low flush. Call — raise risks being dominated |
| 6 | Ad Kd | high_card (0) | ~0.18 | AK no hearts. Overcards but flush-heavy board |
| 7 | Tc 9d | two_pair (10) | ~0.40 | Turned two pair. But flush board — call or fold? |
| 8 | 7h 6h | flush (14) | ~0.55 | Bottom flush. Vulnerable — call |
| 9 | Ah 5d | high_card (0) | ~0.15 | Ah single heart. Blocker to nut flush — bluff raise? |

**9 situations.**

---

## Summary

| Board | Street | Texture | Hero Pos | Facing Bet? | Hands | Key Scenario |
|-------|--------|---------|----------|-------------|-------|-------------|
| BD1 | Flop | Ac Kd 7h (A-high dry) | CO (IP) | No | 8 | Standard c-bet on AK board |
| BD2 | Turn | 5d 5c 9h Jd (paired) | BTN (IP) | Yes | 8 | Paired board + double barrel |
| BD3 | Turn | Td 8c 3h 6s (medium) | BB (OOP) | No | 8 | Both checked, bet or check |
| BD4 | River | Kh 9d 4c 2s Jc (dry) | SB (OOP) | Yes | 8 | Big river bet after turn check |
| BD5 | River | 7h 4d 2c Qd 9s (low) | CO (IP) | No | 8 | Two-barrel then check, bet/check |
| BD6 | Turn | 9c 7c 2d Kh (two-tone) | CO (IP) | Yes (raise) | 8 | Facing turn RAISE |
| BD7 | River | Jh 8d 5c Qc 4h (medium) | BTN (IP) | Yes | 8 | Triple barrel call/fold |
| BD8 | River | 6h 3d 2h 9c Ks (low) | BB (OOP) | No | 8 | River scare card, bet/check |
| BD9 | Turn | Qh 9h 4d Th (3-flush) | SB (OOP) | Yes | 9 | Flush board, sandwich position |

**Total: 73 situations across 9 boards.**
**Turn/River: 8 of 9 boards (89%).**

## Coverage checklist

- [x] Dry boards (BD1, BD4)
- [x] Wet/connected boards (BD3, BD6, BD7)
- [x] Paired boards (BD2)
- [x] Flush-completed boards (BD9)
- [x] Low boards (BD5, BD8)
- [x] Ace-high boards (BD1)
- [x] Scare card runouts (BD4 J river, BD5 Q turn, BD8 K river)
- [x] Facing bet (BD2, BD4, BD6, BD7, BD9)
- [x] Not facing bet (BD1, BD3, BD5, BD8)
- [x] Facing RAISE specifically (BD6)
- [x] Triple barrel (BD7)
- [x] IP hero (BD1, BD2, BD5, BD6, BD7)
- [x] OOP hero (BD3, BD4, BD8, BD9)
- [x] Sandwich position (BD9)
- [x] All hand categories represented: high_card, bottom_pair, middle_pair, top_pair, underpair, overpair, two_pair, trips, set, flush
- [x] Flop (1 board), Turn (4 boards), River (4 boards)

## What this does NOT include

- No expected labels. The GTO Expert labels every situation fresh.
- No axis targeting — these are deliberately non-thematic.
- No board overlap with other category designs.
