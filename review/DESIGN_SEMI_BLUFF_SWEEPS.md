# Design: Board-Anchored Semi-Bluff Sweeps for v9-3way

**Date:** 6 April 2026
**Status:** DESIGN -- awaiting owner review before labelling
**Knowledge base:** Section 1.7 (Semi-Bluff Conditions), Section 1.8
(Blocker Effects), Worked Example 9

---

## Purpose

The v9-3way model has no training data for the CALL-to-RAISE boundary
on draws, and no data distinguishing blocker-holding nut draws (RAISE)
from non-blocker nut draws (CALL) from non-nut draws (CHECK/CALL).
Section 1.7 established solver-verified conditions for semi-bluffing
3-way. This design produces 54 situations across 6 boards, all
targeting the semi-bluff decision spectrum in 3-way pots.

## The semi-bluff spectrum (from Section 1.7)

The blocker is the key differentiator. Same draw, different action:

| Draw type | Blocker? | Side equity? | Expected action |
|-----------|----------|-------------|-----------------|
| Nut flush draw | YES (As on spade board) | Yes | RAISE |
| Nut flush draw | NO (8s7s for nut flush) | Yes | CALL |
| Non-nut flush draw | No | Any | CHECK/CALL |
| Combo draw (flush + straight) | Varies | Built-in | Context-dependent |
| OESD only | No | No | CALL (with odds) |
| Gutshot only | No | No | CHECK/FOLD |
| Made hand + draw | N/A | Yes | Context-dependent |
| Pure made hand, no draw | N/A | No | CHECK or BET (not semi-bluff) |

## Design principles

1. **Boards 1-2:** Facing bet (semi-bluff RAISE decision). Two-tone flops.
2. **Board 3:** NOT facing bet (semi-bluff BET decision). Two-tone flop.
3. **Board 4:** Turn card completes draw texture. Facing second barrel.
4. **Board 5:** Monotone board (3 flush cards). Made flush territory.
5. **Board 6:** Connected board, straight draws dominate over flush draws.
6. **Mix IP and OOP heroes** across the 6 boards.

## Encoding reference

Position: UTG=0, HJ=1, CO=2, BTN=3, SB=4, BB=5
Street: flop=0, turn=1, river=2

---

## Board 1: Ks Jd 5s (Flop) -- Facing Bet OOP, Nut Flush Draw Board

**Board:** Ks Jd 5s
**Street:** Flop
**Hero position:** SB (OOP)
**Villain positions:** CO (opener, bettor), BTN (cold-caller, behind)
**Pot:** 90 (CO opens 3bb, BTN calls, SB calls)
**To call:** 30 (CO bets 30 into 90)
**Facing bet:** Yes
**Action history:** CO opens, BTN calls, SB (hero) calls. Flop Ks Jd 5s:
CO bets 30 into 90. BTN still to act behind hero.

This is the Example 9 board from the knowledge base. Two spades, high
cards favour CO's opening range. The nut flush draw is spades. The As
is the critical blocker -- it removes AsXs combos from villain ranges.

| # | Hero Hand | Category | Equity Est. | Draw Outs | FD | SD | Notes |
|---|-----------|----------|-------------|-----------|----|----|-------|
| 1 | As Qs | overcards (2) | ~0.44 | 9+6+4 | 1 | 0 | NFD + As blocker + 2 overs + gutshot |
| 2 | As 4s | high_card (0) | ~0.34 | 9 | 1 | 0 | NFD + As blocker, no side equity |
| 3 | 8s 7s | high_card (0) | ~0.36 | 9+4 | 1 | 1 | NFD, NO blocker + gutshot |
| 4 | Qs Ts | high_card (0) | ~0.32 | 9 | 1 | 0 | NFD, NO blocker, one overcard |
| 5 | Ts 9s | high_card (0) | ~0.30 | 9 | 1 | 0 | Non-nut FD (2nd nut), no blocker |
| 6 | 9s 8s | high_card (0) | ~0.28 | 9 | 1 | 0 | Non-nut FD (3rd nut), no blocker |
| 7 | Qh Th | overcards (2) | ~0.22 | 8 | 0 | 1 | OESD only, no flush draw |
| 8 | 7h 6h | high_card (0) | ~0.10 | 4 | 0 | 0 | Gutshot only (4-8) |
| 9 | Kd Td | top_pair (6) | ~0.52 | 0 | 0 | 0 | Made hand, no draw (contrast) |

**9 situations.**

---

## Board 2: Qh 8d 3h (Flop) -- Facing Bet IP, Hearts Flush Draw

**Board:** Qh 8d 3h
**Street:** Flop
**Hero position:** BTN (IP)
**Villain positions:** CO (opener), BB (defender, bettor)
**Pot:** 90 (CO opens 3bb, BTN calls, BB defends)
**To call:** 30 (BB leads 30 into 90)
**Facing bet:** Yes
**Action history:** CO opens, BTN (hero) calls, BB defends. Flop Qh 8d 3h:
BB donk-bets 30 into 90. CO folds. Hero faces 30.

Hero is IP against a single donk-bettor from the BB. BB donk range is
polarised: strong hands (sets, two pair) and semi-bluffs (flush draws).
Hero's IP position amplifies draw equity realization. The Ah is the
critical blocker on this board.

| # | Hero Hand | Category | Equity Est. | Draw Outs | FD | SD | Notes |
|---|-----------|----------|-------------|-----------|----|----|-------|
| 1 | Ah Kh | overcards (2) | ~0.48 | 9+3 | 1 | 0 | NFD + Ah blocker + overcard |
| 2 | Ah 5h | high_card (0) | ~0.36 | 9 | 1 | 0 | NFD + Ah blocker, minimal side equity |
| 3 | Kh Jh | one_overcard (1) | ~0.34 | 9 | 1 | 0 | NFD, NO blocker, one overcard |
| 4 | Jh Th | high_card (0) | ~0.34 | 9+4 | 1 | 1 | NFD, NO blocker + gutshot |
| 5 | 9h 7h | high_card (0) | ~0.28 | 9 | 1 | 0 | Non-nut FD (low), no blocker |
| 6 | Jc Ts | high_card (0) | ~0.18 | 8 | 0 | 1 | OESD only (9-T-J-Q), no flush draw |
| 7 | 6s 5s | high_card (0) | ~0.08 | 4 | 0 | 0 | Gutshot only (4-5-6-7) |
| 8 | 8h 7c | middle_pair (5) | ~0.40 | 9 | 1 | 0 | Made hand + flush draw (pair + FD) |
| 9 | Qc Jd | top_pair (6) | ~0.55 | 0 | 0 | 0 | Pure made hand, no draw (contrast) |

**9 situations.**

---

## Board 3: Td 7d 2c (Flop) -- NOT Facing Bet OOP, Semi-Bluff Lead Decision

**Board:** Td 7d 2c
**Street:** Flop
**Hero position:** BB (OOP)
**Villain positions:** CO (opener), BTN (cold-caller)
**Pot:** 90 (CO opens 3bb, BTN calls, BB defends)
**To call:** 0 (not facing bet -- both opponents check)
**Facing bet:** No
**Action history:** CO opens, BTN calls, BB (hero) defends. Flop Td 7d 2c:
CO checks, BTN checks. Hero last to act (checked around to BB).

Both opponents checked, showing weakness. Hero's semi-bluff lead decision:
should hero bet with a draw to deny equity and pick up the pot? The Ad
is the critical blocker. Board favours BTN's cold-call range (connected,
middling). CO checking on a board that does not favour them is expected.

| # | Hero Hand | Category | Equity Est. | Draw Outs | FD | SD | Notes |
|---|-----------|----------|-------------|-----------|----|----|-------|
| 1 | Ad Qd | one_overcard (1) | ~0.42 | 9+3 | 1 | 0 | NFD + Ad blocker + overcard |
| 2 | Ad 3d | high_card (0) | ~0.34 | 9 | 1 | 0 | NFD + Ad blocker, no side equity |
| 3 | Kd Jd | one_overcard (1) | ~0.32 | 9 | 1 | 0 | NFD, NO blocker, one overcard |
| 4 | 9d 8d | high_card (0) | ~0.40 | 9+8 | 1 | 1 | Combo draw: NFD + OESD (6-7-8-9-T) |
| 5 | 6d 5d | high_card (0) | ~0.30 | 9+4 | 1 | 0 | Non-nut FD + gutshot (only) |
| 6 | 9c 8c | high_card (0) | ~0.28 | 8 | 0 | 1 | OESD only, no flush draw |
| 7 | Jc 9c | high_card (0) | ~0.14 | 4 | 0 | 0 | Gutshot only (8-9-T-J) |
| 8 | 7h 6h | middle_pair (5) | ~0.35 | 4 | 0 | 0 | Made pair + gutshot |
| 9 | Th Kc | top_pair (6) | ~0.55 | 0 | 0 | 0 | Pure made hand, no draw (contrast) |

**9 situations.**

---

## Board 4: Jc 8s 4c 9c (Turn) -- Facing Second Barrel, 3 Clubs on Turn

**Board:** Jc 8s 4c 9c
**Street:** Turn
**Hero position:** BB (OOP)
**Villain positions:** CO (opener, bettor), BTN (cold-caller, called flop)
**Pot:** 200 (90 preflop, CO bet 33 on flop, BTN called, BB called, turn pot ~200)
**To call:** 80 (CO bets 80 into 200)
**Facing bet:** Yes
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Jc 8s 4c:
CO bets 33, BTN calls, BB calls. Turn 9c: CO bets 80 into 200. BTN folds.

Turn brings the third club, completing flush draws. This is the transition
from "draw territory" to "made flush territory." Hands that were drawing
on the flop have either gotten there or are now drawing dead to the flush.
CO double-barrelling into multiway = strong range (Section 1.2:
villain_aggression_count=2). The Ac is the critical blocker here.

| # | Hero Hand | Category | Equity Est. | Draw Outs | FD | SD | Notes |
|---|-----------|----------|-------------|-----------|----|----|-------|
| 1 | Ac Kc | flush (14) | ~0.80 | 0 | 0 | 0 | Nut flush, made hand (not a draw) |
| 2 | Ac 5d | one_overcard (1) | ~0.28 | 0 | 0 | 0 | Ac blocker only, no flush, no draw |
| 3 | Qc Tc | flush (14) | ~0.70 | 0 | 0 | 0 | 2nd nut flush, made hand |
| 4 | 7c 6c | flush (14) | ~0.60 | 0 | 0 | 0 | Low flush, made hand (vulnerable) |
| 5 | Kc 3d | high_card (0) | ~0.15 | 0 | 0 | 0 | Single club, no flush, Kc partial blocker |
| 6 | Qh Ts | middle_pair (5) | ~0.22 | 8 | 0 | 1 | OESD (7-8-9-T-J-Q) no club |
| 7 | 5h 3h | high_card (0) | ~0.05 | 0 | 0 | 0 | Complete air, no draw, no blocker |
| 8 | Jh Tc | top_pair (6) | ~0.40 | 0 | 0 | 0 | TP + club (one club, not a flush) |
| 9 | 9d 8d | two_pair (10) | ~0.45 | 0 | 0 | 0 | Two pair, no club, no draw |

**9 situations.**

---

## Board 5: 7s 6s 5d (Flop) -- Connected Board, Straight Draws Dominate

**Board:** 7s 6s 5d
**Street:** Flop
**Hero position:** BTN (IP)
**Villain positions:** HJ (opener), BB (defender, bettor)
**Pot:** 90 (HJ opens 3bb, BTN calls, BB defends)
**To call:** 45 (BB leads 45 into 90)
**Facing bet:** Yes
**Action history:** HJ opens, BTN (hero) calls, BB defends. Flop 7s 6s 5d:
BB donk-bets 45 into 90. HJ folds. Hero faces 45.

Highly connected board. BB's donk range hits this board hard (suited
connectors, small pairs for sets). Straight draws and combo draws are
abundant. The As is the flush draw blocker on this board. This tests
whether the model can distinguish straight draws from flush draws as
semi-bluff candidates.

| # | Hero Hand | Category | Equity Est. | Draw Outs | FD | SD | Notes |
|---|-----------|----------|-------------|-----------|----|----|-------|
| 1 | As 9s | high_card (0) | ~0.40 | 9+4 | 1 | 0 | NFD + As blocker + gutshot (6-7-8-9) |
| 2 | Ks Qs | high_card (0) | ~0.30 | 9 | 1 | 0 | NFD, NO blocker, no straight equity |
| 3 | 9s 8s | straight (13) | ~0.85 | 0 | 1 | 0 | Flopped straight (9-8-7-6-5) + NFD redraw (contrast: made monster, not a semi-bluff) |
| 4 | 9h 8h | high_card (0) | ~0.40 | 8+4 | 0 | 1 | OESD (5-6-7-8-9) + gutshot, NO flush |
| 5 | 9c 4c | high_card (0) | ~0.18 | 4 | 0 | 0 | Gutshot only (5-6-7-8-9, bottom) |
| 6 | Th 8h | high_card (0) | ~0.30 | 8 | 0 | 1 | OESD (5-6-7-8 or 7-8-9-T), no flush |
| 7 | 4s 3s | high_card (0) | ~0.28 | 9+4 | 1 | 0 | Non-nut FD + gutshot (3-4-5-6-7) |
| 8 | 7h 8d | top_pair (6) | ~0.45 | 4 | 0 | 0 | Top pair + gutshot (5-6-7-8-9) |
| 9 | Ac Ad | overpair (9) | ~0.60 | 0 | 0 | 0 | Pure made hand, overpair, no draw (contrast) |

**9 situations.**

---

## Board 6: 9h 6h 2d Kd (Turn) -- Facing Bet OOP, Turn Brings Second Flush Draw

**Board:** 9h 6h 2d Kd
**Street:** Turn
**Hero position:** SB (OOP)
**Villain positions:** CO (opener, bettor), BTN (cold-caller)
**Pot:** 180 (90 preflop, CO bet 30 on flop, BTN called, SB called, turn pot ~180)
**To call:** 60 (CO bets 60 into 180)
**Facing bet:** Yes
**Action history:** CO opens, BTN calls, SB (hero) calls. Flop 9h 6h 2d:
CO bets 30, BTN calls, SB calls. Turn Kd: CO bets 60 into 180. BTN
still to act behind.

Turn brings the Kd creating a second flush draw (diamonds alongside
hearts). The K is a scare card that favours CO's range. Hero is OOP
in the sandwich -- worst seat. Two distinct flush draws are live. The
Ah is the blocker for the heart draw; the Ad is the blocker for the
diamond draw. This tests blocker specificity: which suit blocker
matters on a board with two possible flush draws?

| # | Hero Hand | Category | Equity Est. | Draw Outs | FD | SD | Notes |
|---|-----------|----------|-------------|-----------|----|----|-------|
| 1 | Ah Qh | one_overcard (1) | ~0.38 | 9 | 1 | 0 | NFD hearts + Ah blocker + overcard |
| 2 | Ah 3c | high_card (0) | ~0.18 | 0 | 0 | 0 | Ah blocker only, no flush draw |
| 3 | Qh Jh | high_card (0) | ~0.28 | 9 | 1 | 0 | NFD hearts, NO Ah blocker |
| 4 | Th 8h | high_card (0) | ~0.32 | 9+4 | 1 | 0 | Non-nut FD hearts + gutshot (7-8-9-T) |
| 5 | Ad Td | high_card (0) | ~0.30 | 9 | 1 | 0 | NFD diamonds + Ad blocker (back-door became front-door) |
| 6 | 8s 7s | high_card (0) | ~0.20 | 8 | 0 | 1 | OESD (6-7-8-9) only, no flush draw |
| 7 | 5c 4c | high_card (0) | ~0.08 | 4 | 0 | 0 | Gutshot only (3-4-5-6) |
| 8 | 9d 8d | middle_pair (5) | ~0.35 | 9 | 1 | 0 | Made pair + diamond flush draw |
| 9 | Kh Jc | top_pair (6) | ~0.50 | 0 | 0 | 0 | Top pair + Kh (single heart), no draw |

**9 situations.**

---

## Board 7: Ah 9c 4h Th (Turn) -- SPR-Collapsed, Nut Draw + Blocker but CALL not RAISE

**Board:** Ah 9c 4h Th
**Street:** Turn
**Hero position:** BB (OOP)
**Villain positions:** CO (opener, bettor)
**Pot:** 350 (90 preflop, CO bet 60 flop, BB called, CO bet 140 turn into ~270)
**To call:** 140
**Facing bet:** Yes
**Effective stack:** 180 (hero has ~180 behind after calling)
**SPR after call:** ~0.5 (180 remaining / 350+140 pot)
**Action history:** CO opens, BTN folds, BB (hero) defends. Flop Ah 9c 4h:
CO bets 60, BB calls. Turn Th: CO bets 140. BTN folded preflop (now HU).

SPR is collapsed (~0.5 after calling). Hero holds nut flush draws with
blockers — the same hands that would RAISE at normal SPR. But at SPR < 1.0,
raising commits hero's remaining stack (~180 into 490+), turning a semi-bluff
into a pure gamble with no fold equity (villain is pot-committed and will
call any raise). The correct action shifts from RAISE to CALL or FOLD
depending on equity vs pot odds. This board teaches the stack-depth boundary
of the semi-bluff carve-out.

| # | Hero Hand | Category | Equity Est. | Draw Outs | FD | SD | Notes |
|---|-----------|----------|-------------|-----------|----|----|-------|
| 1 | Kh Qh | flush_draw | ~0.36 | 9 | 1 | 0 | NFD + Kh blocker. At normal SPR = RAISE. At SPR 0.5 = CALL (no fold equity) |
| 2 | Kh 5h | flush_draw | ~0.28 | 9 | 1 | 0 | NFD + Kh blocker, no side equity. SPR collapse = CALL or FOLD |
| 3 | Qh Jh | flush_draw | ~0.34 | 9+4 | 1 | 0 | NFD, no ace blocker + gutshot (J-Q-K). CALL territory |
| 4 | 8h 7h | flush_draw | ~0.26 | 9 | 1 | 0 | Non-nut FD (low), no blocker. SPR collapse = likely FOLD |
| 5 | Jc 8c | high_card (0) | ~0.15 | 4 | 0 | 0 | Gutshot only (7-8-9-T-J). No flush. FOLD |
| 6 | 9h 8h | middle_pair (5) | ~0.35 | 9 | 1 | 0 | Pair + flush draw. SPR collapse makes raise pointless — CALL |
| 7 | Th 9d | two_pair (10) | ~0.55 | 0 | 0 | 0 | Two pair, no draw. Contrast: call/raise for value, not semi-bluff |
| 8 | Kd Qd | high_card (0) | ~0.18 | 0 | 0 | 0 | Two overcards, no flush draw. SPR collapse = FOLD |
| 9 | Ah Kc | top_pair (6) | ~0.60 | 0 | 0 | 0 | TPTK + Ah (single heart). Contrast: made hand at low SPR |

**9 situations.**

---

## Board 8: Qs 8s 3d 5c Jh (River) -- Bricked Flush Draw, Ace Blocker Paradox

**Board:** Qs 8s 3d 5c Jh
**Street:** River
**Hero position:** SB (OOP)
**Villain positions:** CO (opener), BTN (cold-caller, bettor)
**Pot:** 280 (90 preflop, CO bet 30 flop, BTN called, SB called = 180.
Turn checked around = 180. River: BTN bets 100 into 180.)
**To call:** 100
**Facing bet:** Yes
**Action history:** CO opens, BTN calls, SB (hero) defends. Flop Qs 8s 3d:
CO bets 30, BTN calls, SB calls. Turn 5c: all check. River Jh: CO checks,
BTN bets 100 into 180. Hero faces 100.

The spade flush draw bricked. Hero was drawing to a flush and missed. This
is the Ace blocker paradox: on flop/turn, As was the BEST card for
semi-bluff raising (blocked villain's nut flush draw combos in their
continuing range). Now on the river, As is the WORST bluffing card — it
blocks villain's busted flush draws (AsXs combos that would FOLD to a
raise). Hero holding As means fewer busted draws in villain's range, so
villain's range is STRONGER, making a bluff less profitable.

The river question is: call, fold, or bluff-raise? The answer depends on
residual equity (pair, showdown value) and whether hero blocks villain's
value or bluff range.

| # | Hero Hand | Category | Equity Est. | Draw Outs | FD | SD | Notes |
|---|-----------|----------|-------------|-----------|----|----|-------|
| 1 | As Ks | high_card (0) | ~0.15 | 0 | 0 | 0 | Busted NFD + As blocker. As BLOCKS villain's folds (busted draws). Bluff-raise is worst here |
| 2 | As 4s | high_card (0) | ~0.10 | 0 | 0 | 0 | Busted NFD + As, no pair. Same paradox: As blocks folds. FOLD likely |
| 3 | Ks Ts | high_card (0) | ~0.12 | 0 | 0 | 0 | Busted NFD, NO As. Ks blocks some value (KQ). Better bluff candidate than As hands |
| 4 | 9s 7s | high_card (0) | ~0.08 | 0 | 0 | 0 | Busted low FD. No blocker to value or folds. Pure FOLD |
| 5 | As Td | high_card (0) | ~0.18 | 0 | 0 | 0 | As (single spade) + no flush draw. As blocks busted draws even without having drawn |
| 6 | Qd Ts | top_pair (6) | ~0.45 | 0 | 0 | 0 | Busted FD but paired Q on flop. Showdown value — CALL likely |
| 7 | Jd 9d | middle_pair (5) | ~0.30 | 0 | 0 | 0 | Rivered pair of jacks, no flush involvement. CALL territory |
| 8 | Kh Qh | top_pair (6) | ~0.50 | 0 | 0 | 0 | No spade involvement, paired Q on flop. Pure made-hand call decision |
| 9 | 6s 5s | bottom_pair (3) | ~0.15 | 0 | 0 | 0 | Busted FD + bottom pair. Weak showdown + no blocker value |

**9 situations.**

---

## Summary

| Board | Street | Texture | Hero Pos | Facing Bet? | Hands | Key Axis |
|-------|--------|---------|----------|-------------|-------|----------|
| 1 | Flop | Ks Jd 5s (two-tone) | SB (OOP) | Yes | 9 | NFD blocker vs no-blocker (Example 9 board) |
| 2 | Flop | Qh 8d 3h (two-tone) | BTN (IP) | Yes | 9 | IP semi-bluff raise, donk-bet scenario |
| 3 | Flop | Td 7d 2c (two-tone) | BB (OOP) | No | 9 | Semi-bluff LEAD decision (no bet to face) |
| 4 | Turn | Jc 8s 4c 9c (monotone turn) | BB (OOP) | Yes | 9 | Made flush vs blocker-only vs nothing |
| 5 | Flop | 7s 6s 5d (connected) | BTN (IP) | Yes | 9 | Straight draws vs flush draws as semi-bluffs |
| 6 | Turn | 9h 6h 2d Kd (two flush draws) | SB (OOP) | Yes | 9 | Dual flush draw board, blocker specificity |
| 7 | Turn | Ah 9c 4h Th (SPR-collapsed) | BB (OOP) | Yes | 9 | SPR < 1.0 kills semi-bluff raise (stack-depth boundary) |
| 8 | River | Qs 8s 3d 5c Jh (bricked flush) | SB (OOP) | Yes | 9 | Ace blocker paradox: As strong early, weak on river |

**Total: 72 situations across 8 boards.**

## Coverage checklist

- [x] Nut flush draw WITH blocker (Boards 1, 2, 3, 5, 6, 7)
- [x] Nut flush draw WITHOUT blocker (Boards 1, 2, 3, 6, 7)
- [x] Non-nut flush draw (Boards 1, 5, 6, 7)
- [x] Combo draw -- flush + straight (Boards 3, 5)
- [x] OESD only (Boards 1, 2, 3, 5, 6)
- [x] Gutshot only (Boards 1, 2, 3, 5, 6, 7)
- [x] Made hand + draw (Boards 2, 3, 5, 6, 7)
- [x] Pure made hand no draw (Boards 1, 2, 3, 4, 5, 7, 8)
- [x] Facing bet -- raise decision (Boards 1, 2, 4, 5, 6, 7, 8)
- [x] NOT facing bet -- lead decision (Board 3)
- [x] Hero IP (Boards 2, 5)
- [x] Hero OOP (Boards 1, 3, 4, 6, 7, 8)
- [x] Monotone/3-flush board (Board 4)
- [x] Connected board (Board 5)
- [x] SPR-collapsed (Board 7)
- [x] River bricked draw (Board 8)
- [x] Ace blocker paradox — early street vs river (Boards 1-3 vs Board 8)
- [x] Turn decisions (Boards 4, 6, 7)
- [x] Flop decisions (Boards 1, 2, 3, 5)
- [x] River decisions (Board 8)

## What this does NOT include

- No expected labels. The GTO Expert labels every situation fresh using
  the knowledge base reasoning framework.
- No paired boards. Section 1.7 explicitly excludes draws on paired
  boards (set-over-set risk makes semi-bluffing negative EV).
