# Design: Flush-Blocking Situations for v9-3way

**Date:** 7 April 2026
**Status:** DESIGN — awaiting review before labelling
**Purpose:** Activate `flush_block_pct` feature (currently 0% importance at 349 samples)
**Budget:** 45 situations across 5 boards

---

## Feature Background

`flush_block_pct` (0.0-1.0) measures what fraction of villain's flush
draw combos hero blocks by holding cards of the flush suit. At 349
samples it showed no signal. Needs 600+ samples with variance in the
feature value. These situations deliberately vary hero's flush-suit
holdings from 0 to 2 cards of the relevant suit.

## Design Principles

1. Each board has a flush draw possible (two-tone or monotone)
2. Hero hands vary from 0 flush-suit cards to 2 flush-suit cards
3. Mix of streets: 1 flop, 2 turn, 2 river (80% turn/river)
4. Mix of positions: IP and OOP
5. Include both facing-bet and not-facing-bet
6. Boards chosen to be distinct from semi-bluff sweep boards

---

## Board F1: Jh 7h 2c (Flop) — Heart Flush Draw Board, Hero Blocking Variance

**Board:** Jh 7h 2c
**Street:** Flop
**Hero position:** CO (IP, opener)
**Villain positions:** BTN (cold-caller), BB (defender, bettor)
**Pot:** 90 (CO opens 3bb, BTN calls, BB defends)
**To call:** 25 (BB leads 25 into 90)
**Facing bet:** Yes
**Action history:** CO (hero) opens, BTN calls, BB defends. Flop Jh 7h 2c:
BB donk-bets 25 into 90. BTN folds. Hero faces 25.

Heart draw board. Hero's heart holdings determine flush_block_pct.

| # | Hero Hand | flush_block_pct | Category | Equity Est. | Notes |
|---|-----------|----------------|----------|-------------|-------|
| 1 | Ah Kh | 0 (has FD) | flush_draw | ~0.40 | 2 hearts = hero HAS the flush draw, not blocking it. Contrast hand: flush_block_pct=0 because hero holds the draw |
| 2 | Ah Qc | ~0.18 | overcards (2) | ~0.32 | 1 heart (Ah) — partial block. Overcards |
| 3 | Kh Td | ~0.12 | high_card (0) | ~0.22 | 1 heart (Kh) — partial block, non-nut |
| 4 | Jc 9c | top_pair (6) | ~0.52 | 0 hearts — no blocking. Top pair |
| 5 | Jd Ts | top_pair (6) | ~0.50 | 0 hearts — no blocking. TP + gutshot |
| 6 | Qh 9h | ~0.25 | high_card (0) | ~0.30 | 2 hearts — high blocking. Non-nut FD |
| 7 | 8h 6h | ~0.20 | high_card (0) | ~0.28 | 2 hearts — mid blocking. Low FD + gutshot |
| 8 | Ac Kd | overcards (2) | ~0.28 | 0 hearts — zero blocking. AK no flush involvement |
| 9 | 7d 6d | middle_pair (5) | ~0.35 | 0 hearts — zero blocking. Pair + gutshot |

**9 situations.**

---

## Board F2: Kc 9c 5d 3c (Turn) — Club Flush Completed, Blocking Matters for Calls

**Board:** Kc 9c 5d 3c
**Street:** Turn
**Hero position:** BB (OOP)
**Villain positions:** CO (opener, bettor), BTN (cold-caller)
**Pot:** 200 (90 preflop, CO bet 33 flop, BTN called, BB called. Turn pot ~200)
**To call:** 80 (CO bets 80 into 200)
**Facing bet:** Yes
**Action history:** CO opens, BTN calls, BB (hero) defends. Flop Kc 9c 5d:
CO bets 33, BTN calls, BB calls. Turn 3c: CO bets 80. BTN still behind.

Third club on turn — flush is now made. Hero's club holdings affect
whether villain is likely to hold the made flush. High flush_block_pct
= villain less likely to have a flush = safer to call with made hands.

| # | Hero Hand | flush_block_pct | Category | Equity Est. | Notes |
|---|-----------|----------------|----------|-------------|-------|
| 1 | Ac Jc | ~0.40 | flush (14) | ~0.80 | Nut flush made. Max blocking irrelevant (hero has it) |
| 2 | Kd Jd | top_pair (6) | ~0.35 | 0 clubs — zero blocking. TP facing 3-flush board |
| 3 | Kh Jc | top_pair (6) | ~0.40 | 1 club (Jc) — partial block. Same hand, club changes call EV |
| 4 | 9d 8d | middle_pair (5) | ~0.22 | 0 clubs — zero blocking. Second pair, vulnerable |
| 5 | 9h 8c | middle_pair (5) | ~0.26 | 1 club (8c) — partial block. Same pair, club helps |
| 6 | Ac 4d | high_card (0) | ~0.18 | 1 club (Ac) — blocks NFD. No made hand, just blocker |
| 7 | Qc Tc | flush (14) | ~0.65 | 2nd nut flush. High blocking built-in |
| 8 | 5h 4h | bottom_pair (3) | ~0.12 | 0 clubs — zero blocking. Bottom pair on 3-flush board |
| 9 | Ah Qh | high_card (0) | ~0.15 | 0 clubs — zero blocking. Overcards, no flush involvement |

**9 situations.**

---

## Board F3: Td 6d 2s 8h (Turn) — Diamond Flush Draw Still Live

**Board:** Td 6d 2s 8h
**Street:** Turn
**Hero position:** BTN (IP)
**Villain positions:** CO (opener), BB (defender, bettor)
**Pot:** 180 (90 preflop, BB checked flop, CO checked, BTN checked. Turn: BB bets 45 into 90+)
**To call:** 45 (BB leads 45 into 180)
**Facing bet:** Yes
**Action history:** CO opens, BTN (hero) calls, BB defends. Flop Td 6d 2s:
all check. Turn 8h: BB bets 45 into 180. CO folds.

Two diamonds — flush draw still live. Hero is IP against BB lead after
flop checked through. Hero's diamond holdings determine blocking.

| # | Hero Hand | flush_block_pct | Category | Equity Est. | Notes |
|---|-----------|----------------|----------|-------------|-------|
| 1 | Ad Kd | ~0.35 | overcards (2) | ~0.50 | 2 diamonds — max blocking. NFD + overcards |
| 2 | Ad 9c | one_overcard (1) | ~0.30 | 1 diamond (Ad) — blocks NFD specifically |
| 3 | Kd Jc | one_overcard (1) | ~0.25 | 1 diamond (Kd) — partial block, non-nut |
| 4 | Th Jh | top_pair (6) | ~0.50 | 0 diamonds — zero blocking. TP |
| 5 | Td 9d | top_pair (6) | ~0.55 | 2 diamonds — high blocking + TP. TP with NFD redraw |
| 6 | 8d 7d | middle_pair (5) | ~0.40 | 2 diamonds — pair + FD. Mid blocking |
| 7 | 9c 7c | high_card (0) | ~0.20 | 0 diamonds — OESD only, no blocking |
| 8 | Qd 5d | ~0.22 | high_card (0) | ~0.30 | 2 diamonds — FD but non-nut. High blocking |
| 9 | Ac Kc | overcards (2) | ~0.25 | 0 diamonds — zero blocking. AK off-suit for diamonds |

**9 situations.**

---

## Board F4: As 7s 3c Ks 9d (River) — Spade Flush Completed on Turn, River Decision

**Board:** As 7s 3c Ks 9d
**Street:** River
**Hero position:** CO (IP, opener)
**Villain positions:** BTN (cold-caller), BB (defender, bettor)
**Pot:** 300 (90 preflop, CO bet 30 flop, BTN called, BB called = 180.
Turn: CO bet 60, BB called, BTN folded = 300. River: BB bets 100.)
**To call:** 100
**Facing bet:** Yes
**Action history:** CO (hero) opens, BTN calls, BB defends. Flop As 7s 3c:
CO bets 30, BTN calls, BB calls. Turn Ks: CO bets 60, BB calls, BTN folds.
River 9d: BB bets 100 into 300.

Spade flush completed on turn (3 spades). River is a brick. BB bet river
after calling turn — could have made flush on turn or is now value-betting
a strong made hand. Hero's spade holdings block villain's flush combos.

| # | Hero Hand | flush_block_pct | Category | Equity Est. | Notes |
|---|-----------|----------------|----------|-------------|-------|
| 1 | Qs Js | ~0.30 | high_card (0) | ~0.20 | 2 spades — busted draw. High blocking but no hand |
| 2 | Ts 8s | ~0.22 | high_card (0) | ~0.15 | 2 spades — busted draw. Mid blocking |
| 3 | Ad Qd | top_pair (6) | ~0.50 | 0 spades — zero blocking. Top pair A |
| 4 | Ad Qs | top_pair (6) | ~0.55 | 1 spade (Qs) — partial block. Same top pair, spade helps |
| 5 | Kd Qd | top_pair (6) | ~0.40 | 0 spades — zero blocking. Second pair K |
| 6 | Kh Qs | top_pair (6) | ~0.45 | 1 spade (Qs) — partial block. K pair + spade block |
| 7 | 9s 8c | middle_pair (5) | ~0.25 | 1 spade (9s) — minor block. Rivered pair |
| 8 | Jh Tc | high_card (0) | ~0.10 | 0 spades — zero blocking. No pair, no block |
| 9 | Ah 7h | two_pair (10) | ~0.60 | 0 spades — zero blocking. Two pair, strong made hand |

**9 situations.**

---

## Board F5: 8h 5h 2d Qh Jc (River) — Heart Flush Completed, River Value/Bluff

**Board:** 8h 5h 2d Qh Jc
**Street:** River
**Hero position:** BB (OOP)
**Villain positions:** CO (opener, bettor)
**Pot:** 240 (90 preflop, CO bet 30 flop, BB called. Turn Qh: CO bet 60,
BB called. River Jc: CO checks. Pot 240.)
**To call:** 0 (not facing bet — CO checked river)
**Facing bet:** No
**Action history:** CO opens, BTN folds, BB (hero) defends. Flop 8h 5h 2d:
CO bets 30, BB calls. Turn Qh: CO bets 60, BB calls. River Jc: CO checks.

Heart flush completed on turn. CO double-barrelled then checked river —
either gave up or is trapping. Hero's heart holdings determine blocking
for bet/check decision. This is a NOT-facing-bet board for variety.

| # | Hero Hand | flush_block_pct | Category | Equity Est. | Notes |
|---|-----------|----------------|----------|-------------|-------|
| 1 | Ah Kh | flush (14) | ~0.85 | Nut flush made. Bet for value |
| 2 | Ah 9c | high_card (0) | ~0.20 | 1 heart (Ah) — blocks NFD. Bluff candidate? |
| 3 | Kh 9c | high_card (0) | ~0.15 | 1 heart (Kh) — partial block. Worse bluff than Ah |
| 4 | 9h 7h | flush (14) | ~0.65 | Low flush made. Bet thin value? |
| 5 | Th 6h | flush (14) | ~0.60 | Low flush made. Thin value territory |
| 6 | Qd Jd | two_pair (10) | ~0.45 | 0 hearts — zero blocking. Rivered two pair |
| 7 | 8c 7c | middle_pair (5) | ~0.20 | 0 hearts — zero blocking. Second pair, check behind? |
| 8 | Kd Td | high_card (0) | ~0.10 | 0 hearts — zero blocking. No pair, no flush |
| 9 | 5d 4d | bottom_pair (3) | ~0.12 | 0 hearts — zero blocking. Bottom pair, give up? |

**9 situations.**

---

## Summary

| Board | Street | Texture | Hero Pos | Facing Bet? | Hands | Key Axis |
|-------|--------|---------|----------|-------------|-------|----------|
| F1 | Flop | Jh 7h 2c (two-tone) | CO (IP) | Yes | 9 | Blocking variance: 0, 1, 2 hearts |
| F2 | Turn | Kc 9c 5d 3c (3-flush) | BB (OOP) | Yes | 9 | 3-flush board: blocking affects call safety |
| F3 | Turn | Td 6d 2s 8h (two-tone) | BTN (IP) | Yes | 9 | Live draw board: blocking affects draw reads |
| F4 | River | As 7s 3c Ks 9d (3-spade) | CO (IP) | Yes | 9 | Completed flush: block affects river call |
| F5 | River | 8h 5h 2d Qh Jc (3-heart) | BB (OOP) | No | 9 | Completed flush: block affects bet/check |

**Total: 45 situations across 5 boards.**
**Turn/River: 4 of 5 boards (80%).**

## Coverage checklist

- [x] flush_block_pct = 0 (no suit cards): F1-H4/H5/H8, F2-H2/H4/H8/H9, F3-H4/H7/H9, F4-H3/H5/H8, F5-H6/H7/H8/H9
- [x] flush_block_pct = low-mid (1 suit card): F1-H2/H3, F2-H3/H5/H6, F3-H2/H3, F4-H4/H6/H7, F5-H2/H3
- [x] flush_block_pct = high (2 suit cards): F1-H1/H6/H7, F2-H1/H7, F3-H1/H5/H6/H8, F4-H1/H2, F5-H1/H4/H5
- [x] Made flush hands (contrast): F2-H1/H7, F5-H1/H4/H5
- [x] Top pair with/without blocking (paired comparison): F2 H2 vs H3, F4 H3 vs H4
- [x] IP and OOP heroes
- [x] Facing bet and not facing bet
- [x] Flop, turn, and river decisions

## What this does NOT include

- No expected labels. The GTO Expert labels every situation fresh.
- No duplicate boards from semi-bluff sweeps.
