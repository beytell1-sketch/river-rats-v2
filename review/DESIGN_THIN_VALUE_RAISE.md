# Design: Thin Value & Raise Boundary Situations for v9-3way

**Date:** 7 April 2026
**Status:** DESIGN — awaiting review before labelling
**Purpose:** Teach thin value betting against capped/weak ranges and raising
with combined equity + fold equity
**Budget:** 35 situations across 4 boards

---

## Design Principles

1. **Thin value boards:** Villain ranges are capped or weak (checked,
   cold-called). Hero holds marginal made hands where betting thin
   is correct against the weak range but checking is standard HU thinking.
2. **Raise boundary boards:** Hero has equity + fold equity (strong draw
   or strong made hand facing a bet). The decision is call vs raise — not
   fold.
3. No specific hand references from the reference set. These boards teach
   general principles, not patch fixes.
4. Mix of positions, streets, and action contexts.
5. 75% turn/river weighting.

---

## Board TV1: Qc 8d 4s 2h (Turn) — Capped Villain, Thin Value Bet OOP

**Board:** Qc 8d 4s 2h
**Street:** Turn
**Hero position:** BB (OOP)
**Villain positions:** CO (opener), BTN (cold-caller)
**Pot:** 180 (90 preflop, CO bet 30 flop, BTN called, BB called. Turn 2h:
CO checks, BTN checks. Hero closing action after both check.)
**To call:** 0 (not facing bet — both opponents checked)
**Facing bet:** No
**Action history:** CO opens, BTN calls, BB (hero) defends. Flop Qc 8d 4s:
CO bets 30, BTN calls, BB calls. Turn 2h: CO checks, BTN checks.

Both opponents checked turn after CO c-bet flop. This caps their ranges —
CO gave up continuation, BTN showed weakness. Hero is OOP but has last
action on this round. The question: bet thin with marginal made hands
against two capped ranges, or check for pot control?

| # | Hero Hand | Category | Equity Est. | Notes |
|---|-----------|----------|-------------|-------|
| 1 | Qd 7d | top_pair (6) | ~0.58 | TPWK. Both opponents weak — bet thin for value? |
| 2 | Qh 5h | top_pair (6) | ~0.55 | TP worst kicker. Even weaker — still thin value? |
| 3 | 8c 7c | middle_pair (5) | ~0.35 | Second pair. Too thin to bet? Or value vs air? |
| 4 | 4h 3h | bottom_pair (3) | ~0.22 | Bottom pair. Check for showdown value? |
| 5 | Ah Kh | overcards (2) | ~0.30 | Two overcards, no pair. Bet as bluff or check? |
| 6 | Jd Td | high_card (0) | ~0.18 | Overcards + gutshot (7-8-9-T-J). Semi-bluff? |
| 7 | Qc Jc | top_pair (6) | ~0.62 | TPGK. Clear value — how does sizing change? |
| 8 | Kd Qd | top_pair (6) | ~0.65 | TPSK. Strongest TP — bet for value OOP |
| 9 | 9c 9d | overpair (9) | ~0.52 | Underpair to Q but overpair to board. Thin value? |

**9 situations.**

---

## Board TV2: Jd 7c 3s Ah (Turn) — Scare Card, Thin Value Against Scared Ranges

**Board:** Jd 7c 3s Ah
**Street:** Turn
**Hero position:** CO (IP, opener)
**Villain positions:** BTN (cold-caller), BB (defender)
**Pot:** 180 (90 preflop, CO bet 30 flop, BTN called, BB called. Turn Ah:
hero's action.)
**To call:** 0 (hero is the potential bettor, not facing a bet)
**Facing bet:** No
**Action history:** CO (hero) opens, BTN calls, BB defends. Flop Jd 7c 3s:
CO bets 30, BTN calls, BB calls. Turn Ah: hero to act.

Ace on turn is a scare card that favours CO's opening range. BTN and BB
are scared of Ax. Hero can bet thin knowing opponents will fold a lot,
or check with marginal hands to control pot. Tests bet/check boundary
when board favours hero's range.

| # | Hero Hand | Category | Equity Est. | Notes |
|---|-----------|----------|-------------|-------|
| 1 | Ac 9c | top_pair (6) | ~0.60 | Turned TP with A. Value bet the scare card? |
| 2 | Ah 5h | top_pair (6) | ~0.55 | Turned TP weak kicker. Thin value on scary turn? |
| 3 | Jh Th | middle_pair (5) | ~0.30 | Was TP on flop, now 2nd pair. Check or barrel? |
| 4 | Jc 9c | middle_pair (5) | ~0.28 | Was TPWK, now 2nd pair weaker. Turn check? |
| 5 | Kc Kd | overpair (9) | ~0.45 | KK — A on turn is nightmare card. Still value? |
| 6 | 7h 6h | middle_pair (5) | ~0.20 | Second pair (7s). Check for showdown? |
| 7 | Qd Qc | overpair (9) | ~0.42 | QQ — same dilemma as KK. Ace scares hero too |
| 8 | Ac Kc | top_pair (6) | ~0.70 | TPTK. Clear value but how big? |
| 9 | 5d 4d | high_card (0) | ~0.10 | Air. Bluff the scare card? Or give up? |

**9 situations.**

---

## Board TV3: Kd 9s 5h 2c Qh (River) — River Raise Boundary, Value Raise vs Call

**Board:** Kd 9s 5h 2c Qh
**Street:** River
**Hero position:** BTN (IP)
**Villain positions:** CO (opener, bettor), BB (defender)
**Pot:** 350 (90 preflop, CO bet 30 flop, BTN called, BB called = 180.
Turn: CO bet 60, BB folded, BTN called = 300. River Qh: CO bets 50.)
**To call:** 50
**Facing bet:** Yes
**Action history:** CO opens, BTN (hero) calls, BB defends. Flop Kd 9s 5h:
CO bets 30, BTN calls, BB calls. Turn 2c: CO bets 60, BB folds, BTN calls.
River Qh: CO bets 50 (small, ~14% pot).

CO made a small river bet — often a blocking bet or thin value. Hero IP
with range advantage from having called two streets. The raise boundary:
which hands should call vs raise for value? River raises are polarized
(nuts or bluff). Thin value CALLS, it doesn't raise.

| # | Hero Hand | Category | Equity Est. | Notes |
|---|-----------|----------|-------------|-------|
| 1 | Kc Qc | two_pair (10) | ~0.75 | Rivered top two. Raise for value or call (trap)? |
| 2 | Kh Jh | top_pair (6) | ~0.55 | TPGK. Call the small bet — too thin to raise |
| 3 | Kd 8d | top_pair (6) | ~0.45 | TPWK. Marginal call vs small bet |
| 4 | 9c 8c | middle_pair (5) | ~0.30 | Second pair. Call or fold small river bet? |
| 5 | Qd Jd | middle_pair (5) | ~0.40 | Rivered pair of Q. Was drawing — now marginal made |
| 6 | Ah Ad | overpair (9) | ~0.60 | AA — call. Too thin to raise river (only better calls) |
| 7 | 5c 5d | set (12) | ~0.85 | Set of 5s. Raise for value — sets are the raise threshold |
| 8 | 7h 6h | high_card (0) | ~0.08 | Air. Bluff-raise the small bet? |
| 9 | Kc 9c | two_pair (10) | ~0.70 | K9 two pair. Raise or call? |

**9 situations.**

---

## Board TV4: Tc 7d 4c 8s (Turn) — Raise Boundary, Equity + Fold Equity

**Board:** Tc 7d 4c 8s
**Street:** Turn
**Hero position:** SB (OOP)
**Villain positions:** CO (opener, bettor), BTN (cold-caller)
**Pot:** 200 (90 preflop, CO bet 33 flop, BTN called, SB called. Turn 8s pot ~200)
**To call:** 70 (CO bets 70 into 200)
**Facing bet:** Yes
**Action history:** CO opens, BTN calls, SB (hero) calls. Flop Tc 7d 4c:
CO bets 33, BTN calls, SB calls. Turn 8s: CO bets 70. BTN still behind.

Connected board with straight and flush draws. CO double-barrelling shows
strength. The raise boundary for hero: which combinations of equity + fold
equity justify a raise vs a call? Strong draws + position or blockers may
tip to raise. Pure made hands call.

| # | Hero Hand | Category | Equity Est. | Notes |
|---|-----------|----------|-------------|-------|
| 1 | Ac 9c | high_card (0) | ~0.38 | NFD + OESD (6-7-8-9-T) + Ac blocker. Raise candidate? |
| 2 | 9c 6c | high_card (0) | ~0.35 | NFD + OESD. No Ac blocker — call instead? |
| 3 | Jh 9h | high_card (0) | ~0.30 | OESD only (7-8-9-T-J). No flush. Call with odds? |
| 4 | 9d 6d | high_card (0) | ~0.25 | OESD (6-7-8-9). No flush. Weaker straight draw |
| 5 | Th 9h | top_pair (6) | ~0.50 | TP + OESD. Strong combo — raise or call? |
| 6 | Tc Jc | top_pair (6) | ~0.55 | TP + NFD redraw + OESD. Monster combo — raise? |
| 7 | 8d 7c | two_pair (10) | ~0.60 | Turned two pair. Raise for protection or call? |
| 8 | 4d 4h | set (12) | ~0.80 | Set of 4s. Clear raise territory |
| 9 | Kd Qd | overcards (2) | ~0.15 | Two overcards, no draws. Fold facing barrel |

**8 situations (H9 is a clear fold, included as contrast).**

---

## Summary

| Board | Street | Texture | Hero Pos | Facing Bet? | Hands | Key Axis |
|-------|--------|---------|----------|-------------|-------|----------|
| TV1 | Turn | Qc 8d 4s 2h (dry) | BB (OOP) | No | 9 | Thin value bet against capped ranges |
| TV2 | Turn | Jd 7c 3s Ah (scare card) | CO (IP) | No | 9 | Bet/check when board favours hero's range |
| TV3 | River | Kd 9s 5h 2c Qh (dry) | BTN (IP) | Yes | 9 | River raise boundary: call vs raise for value |
| TV4 | Turn | Tc 7d 4c 8s (connected) | SB (OOP) | Yes | 9 | Raise boundary: equity + fold equity combinations |

**Total: 36 situations across 4 boards.**
**Turn/River: 4 of 4 boards (100%).**

## Coverage checklist

- [x] Thin value with TPWK/TPGK against weak ranges (TV1, TV2)
- [x] Thin value with second pair (TV1-H3, TV2-H3/H4/H6)
- [x] Overpair on scary board (TV2-H5/H7)
- [x] River raise/call boundary with two pair, sets, overpairs (TV3)
- [x] Turn raise with equity + fold equity: combo draw, pair+draw (TV4)
- [x] Turn raise with blocker vs without (TV4-H1 vs H2)
- [x] Bluff and air contrast hands (TV1-H5/H6, TV2-H9, TV3-H8)
- [x] IP and OOP heroes
- [x] Facing bet and not facing bet

## What this does NOT include

- No expected labels. The GTO Expert labels every situation fresh.
- No reference to specific model failures. These teach general principles.
