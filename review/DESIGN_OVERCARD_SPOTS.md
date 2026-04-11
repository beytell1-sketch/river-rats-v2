# Design: Overcard Situations for v9-3way

**Date:** 7 April 2026
**Status:** DESIGN — awaiting review before labelling
**Purpose:** Activate `overcard_outs` feature (0/3/6 values, currently insufficient variance)
**Budget:** 35 situations across 4 boards (+1 shared with broad distribution)

---

## Feature Background

`overcard_outs` counts hero's overcards × 3 (each overcard is ~3 outs
to top pair). Values: 0 (no overcards), 3 (one overcard), 6 (two
overcards). At 349 samples the feature showed minimal signal. These
situations deliberately vary overcard count and pair it with different
board textures and action contexts to give the model variance.

The knowledge base Example 7 (AK on J84) established that overcard outs
are "hidden equity" not captured by draw_outs. The model needs to learn
that unpaired high cards on low/medium boards have value beyond what
raw equity alone suggests.

## Design Principles

1. All boards are low-to-medium (highest card ≤ T) so hero's broadway cards are overcards
2. Hero hands systematically vary: 0 overcards, 1 overcard, 2 overcards
3. Paired with facing-bet (call/fold decisions) and not-facing-bet (bet/check)
4. Turn/river weighted (3 of 4 boards)
5. Boards distinct from other category designs

---

## Board O1: 9c 6h 3d (Flop) — Low Board, Overcard Call Decision

**Board:** 9c 6h 3d
**Street:** Flop
**Hero position:** BTN (IP)
**Villain positions:** CO (opener, bettor), BB (defender)
**Pot:** 90 (CO opens 3bb, BTN calls, BB defends)
**To call:** 30 (CO bets 30 into 90)
**Facing bet:** Yes
**Action history:** CO opens, BTN (hero) calls, BB defends. Flop 9c 6h 3d:
CO bets 30 into 90. BB folds. Hero faces 30.

Dry, low board. CO c-bet is standard on a board that favours the opener's
range. Hero's overcards determine hidden equity for calling.

| # | Hero Hand | overcard_outs | Category | Equity Est. | Notes |
|---|-----------|--------------|----------|-------------|-------|
| 1 | Ah Kh | 6 | overcards (2) | ~0.28 | 2 overcards (6 outs to TPTK). Best overcard hand |
| 2 | Ah Qd | 6 | overcards (2) | ~0.26 | 2 overcards. AQ slightly less value than AK |
| 3 | Kh Jd | 6 | overcards (2) | ~0.24 | 2 overcards. KJ — weaker kicker value if hit |
| 4 | Ah 8c | 3 | one_overcard (1) | ~0.22 | 1 overcard (A only). A8 — ace overcard + weak kicker |
| 5 | Kh 5c | 3 | one_overcard (1) | ~0.18 | 1 overcard (K only). K5 — king overcard, weak |
| 6 | Th 8h | 3 | one_overcard (1) | ~0.25 | 1 overcard (T over 9 — marginal; hitting T gives only TPWK). + gutshot + backdoor FD |
| 7 | 7h 5h | 0 | high_card (0) | ~0.15 | 0 overcards. Gutshot only (4-5-6-7-8) |
| 8 | 4c 2c | 0 | high_card (0) | ~0.08 | 0 overcards. Complete air, no draws |
| 9 | 9d Td | top_pair (6) | ~0.55 | 1 overcard (T) but also TP. Contrast: made hand |

**9 situations.**

---

## Board O2: 8d 5c 2h Jh (Turn) — Turn Overcard Arrived, Facing Second Barrel

**Board:** 8d 5c 2h Jh
**Street:** Turn
**Hero position:** BB (OOP)
**Villain positions:** CO (opener, bettor), BTN (cold-caller)
**Pot:** 200 (90 preflop, CO bet 33 flop, BTN called, BB called. Turn pot ~200)
**To call:** 70 (CO bets 70 into 200)
**Facing bet:** Yes
**Action history:** CO opens, BTN calls, BB (hero) defends. Flop 8d 5c 2h:
CO bets 33, BTN calls, BB calls. Turn Jh: CO bets 70. BTN still behind.

J on turn changes overcard dynamics. Hands with J as an overcard now have
top pair. Hands with only A/K/Q overcards still have overcards but the J
is no longer available. Multi-street aggression (villain_aggression=2).

| # | Hero Hand | overcard_outs | Category | Equity Est. | Notes |
|---|-----------|--------------|----------|-------------|-------|
| 1 | Ah Kc | 6 | overcards (2) | ~0.25 | 2 overcards (A, K). Double barrel + 3-way = tight spot |
| 2 | Ah Qd | 6 | overcards (2) | ~0.23 | 2 overcards. AQ facing double barrel |
| 3 | Kc Qd | 6 | overcards (2) | ~0.20 | 2 overcards (K, Q). Weakest 2-overcard holding |
| 4 | Ah 7c | 3 | one_overcard (1) | ~0.18 | 1 overcard (A). A7 — one overcard facing aggression |
| 5 | Qd 9c | 3 | one_overcard (1) | ~0.20 | 1 overcard (Q) + middle pair on flop. J turn improves villain |
| 6 | Td 9d | 0 | high_card (0) | ~0.15 | 0 overcards (T < J). OESD (7-8-9-T-J) helps |
| 7 | 6c 4c | 0 | high_card (0) | ~0.10 | 0 overcards. Gutshot (3-4-5-6-7) |
| 8 | Jd Td | top_pair (6) | ~0.45 | 0 (has TP). Contrast: J gave hero top pair |
| 9 | 8c 7c | middle_pair (5) | ~0.22 | 0 overcards. Second pair + gutshot facing barrel |

**9 situations.**

---

## Board O3: 7c 4d 2s 9h Tc (River) — River Brick, Overcards Never Improved

**Board:** 7c 4d 2s 9h Tc
**Street:** River
**Hero position:** CO (IP, opener)
**Villain positions:** BTN (cold-caller), BB (defender, bettor)
**Pot:** 250 (90 preflop, all checked flop. Turn 9h: BB bet 40, CO called,
BTN folded = 170. River Tc: BB bets 80 into 170.)
**To call:** 80
**Facing bet:** Yes
**Action history:** CO (hero) opens, BTN calls, BB defends. Flop 7c 4d 2s:
all check. Turn 9h: BB bets 40, CO calls, BTN folds. River Tc: BB bets 80.

Overcards never improved. River T means only A, K, Q are now overcards.
Hero called turn with overcard equity — did it pay off? River facing bet
with missed overcards is a fold/call decision based on showdown value.

| # | Hero Hand | overcard_outs | Category | Equity Est. | Notes |
|---|-----------|--------------|----------|-------------|-------|
| 1 | Ah Kh | 6 | overcards (2) | ~0.20 | 2 overcards (A, K). Never improved. Fold or hero call? |
| 2 | Ah Qd | 6 | overcards (2) | ~0.18 | 2 overcards. AQ river — missed everything |
| 3 | Kd Qd | 6 | overcards (2) | ~0.15 | 2 overcards. KQ — weakest high cards, no pair |
| 4 | Ah 6c | 3 | one_overcard (1) | ~0.14 | 1 overcard (A). A6 with bottom-pair-ish equity |
| 5 | Kd 8c | 3 | one_overcard (1) | ~0.12 | 1 overcard (K). K8, one overcard remaining |
| 6 | Jd 8d | 0 | middle_pair (5) | ~0.10 | 0 overcards now (J < board cards). J not an overcard |
| 7 | 5c 3c | 0 | high_card (0) | ~0.05 | 0 overcards. Complete air, gutshot missed |
| 8 | Tc 8c | top_pair (6) | ~0.50 | 0 (has TP). Rivered top pair. Contrast: call easily |
| 9 | Qd Jd | 3 | one_overcard (1) | ~0.12 | 1 overcard (Q). QJ missed — J no longer an overcard |

**9 situations.**

---

## Board O4: 6s 3h 2c Ts (Turn) — Low Board, Not Facing Bet, Overcard Bet Decision

**Board:** 6s 3h 2c Ts
**Street:** Turn
**Hero position:** BTN (IP)
**Villain positions:** CO (opener), BB (defender)
**Pot:** 90 (90 preflop, all checked flop. Turn Ts: both check to hero.)
**To call:** 0 (not facing bet)
**Facing bet:** No
**Action history:** CO opens, BTN (hero) calls, BB defends. Flop 6s 3h 2c:
all check. Turn Ts: CO checks, BB checks. Hero closing action.

Both opponents showed weakness on flop and turn. Hero IP with closing
action — bet or check? Overcard outs affect whether hero should stab
at this pot or give up. T on turn means only A/K/Q/J are overcards.

| # | Hero Hand | overcard_outs | Category | Equity Est. | Notes |
|---|-----------|--------------|----------|-------------|-------|
| 1 | Ah Kh | 6 | overcards (2) | ~0.35 | 2 overcards. Opponents weak — bet thin? |
| 2 | Kd Qd | 6 | overcards (2) | ~0.30 | 2 overcards. KQ — bet or check behind? |
| 3 | Ah 5c | 3 | one_overcard (1) | ~0.25 | 1 overcard (A) + gutshot (2-3-4-5). Bet candidate |
| 4 | Qd 9c | 3 | one_overcard (1) | ~0.22 | 1 overcard (Q). Weak — check or stab? |
| 5 | Jc 9c | 0 | high_card (0) | ~0.18 | 0 overcards (J < T? No — J > T). Actually 1 overcard |
| 6 | 8h 7h | 0 | high_card (0) | ~0.15 | 0 overcards. Gutshot (4-5-6-7-8) |
| 7 | 4d 4c | underpair (4) | ~0.40 | 0 overcards. Pocket pair below board |
| 8 | Ah Jd | 6 | overcards (2) | ~0.33 | 2 overcards (A, J). AJ on low board — bet? |

**8 situations.**

---

## Summary

| Board | Street | Texture | Hero Pos | Facing Bet? | Hands | Key Axis |
|-------|--------|---------|----------|-------------|-------|----------|
| O1 | Flop | 9c 6h 3d (dry low) | BTN (IP) | Yes | 9 | Overcard call decision, dry board |
| O2 | Turn | 8d 5c 2h Jh (low + J turn) | BB (OOP) | Yes | 9 | Overcards facing double barrel |
| O3 | River | 7c 4d 2s 9h Tc (low, missed) | CO (IP) | Yes | 9 | Missed overcards, river fold/call |
| O4 | Turn | 6s 3h 2c Ts (low + T turn) | BTN (IP) | No | 8 | Overcard bet decision, opponents weak |

**Total: 35 situations across 4 boards.**
**Turn/River: 3 of 4 boards (75%).**

## Coverage checklist

- [x] overcard_outs = 6 (2 overcards): O1-H1/H2/H3, O2-H1/H2/H3, O3-H1/H2/H3, O4-H1/H2/H8
- [x] overcard_outs = 3 (1 overcard): O1-H4/H5/H6, O2-H4/H5, O3-H4/H5/H9, O4-H3/H4
- [x] overcard_outs = 0 (no overcards): O1-H7/H8, O2-H6/H7, O3-H6/H7, O4-H6/H7
- [x] Made hand contrast: O1-H9, O2-H8/H9, O3-H8
- [x] Facing bet and not facing bet
- [x] IP and OOP heroes
- [x] Flop, turn, and river

## What this does NOT include

- No expected labels. The GTO Expert labels every situation fresh.
- No boards above T-high for the flop — overcards must be overcards.
