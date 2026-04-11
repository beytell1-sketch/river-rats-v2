# Solver-Verified Hands: FB_Board4 (As 7s 3c Ks 9d) — River

**Date:** 7 April 2026
**Source:** GTO Wizard, exact line verified by owner
**Status:** VERIFIED — select useful hands for training later

---

## Setup (identical for all hands)

**Players:** CO (hero, opener, IP), BTN (cold-caller, folded turn), BB (defender, bettor)

**Preflop:** CO opens. BTN calls. BB defends. Pot: 90.

**Flop: As 7s 3c**
CO bets 30. BTN calls. BB calls. Pot: 180.

**Turn: Ks**
CO bets 60. BB calls. BTN folds. Pot: 300.

**River: 9d**
BB bets 100 into 300.

**Hero's decision:** Faces 100. Pot ~500 if calling. Pot odds 25%. SPR 0.33. IP.

---

## Solver results

### Group 1: Made flushes — all RAISE

| # | Hero Hand | Solver Action | Notes |
|---|-----------|--------------|-------|
| 1 | Ts 9s | **RAISE** | Strong flush. River 9d gives hero pair + flush. |
| 2 | Ts 8s | **RAISE** | T-high flush. Original hand. |
| 3 | 8s 6s | **RAISE** | 8-high flush. Low flush still raises. |
| 4 | 6s 5s | **RAISE** | 6-high flush. Even bottom flushes raise. |
| 5 | 5s 4s | **RAISE** | 5-high flush. Lowest possible flush still raises. |

**Teaching point:** ALL made flushes raise on this river, even the smallest. On a 4-spade board (As Ks on board), any flush is strong enough to raise for value because villain's betting range includes many non-flush hands (Ax, Kx, two pair) that will call.

### Group 2: Blocker hands (Ace + spade or club) — RAISE

| # | Hero Hand | Solver Action | Notes |
|---|-----------|--------------|-------|
| 6 | Ac 8s | **RAISE** | No flush (only 1 spade) but Ac blocks nut flush combos + 8s partial spade block. Bluff-raise with blocker. |
| 7 | Ad 8c | **RAISE** | No spade at all. Ad blocks villain's Ax value hands. Pure bluff-raise with range blocker. |

**Teaching point:** These are BLUFF raises, not value raises. Hero doesn't have a flush but blocks villain's value range (Ax) and/or flush combos. River raise is polarized: nuts or bluffs. These are the bluff portion.

### Group 3: Top pair with specific suits — CALL

| # | Hero Hand | Solver Action | Notes |
|---|-----------|--------------|-------|
| 8 | Ad 9c | **CALL** | Top pair A (Ad) + rivered pair 9. No spade. Showdown value too strong to bluff, too weak to raise for value. |
| 9 | Ac 9s | **CALL** | Top pair A (Ac) + 9s (one spade). Same — has showdown value, not raising. |

**Teaching point:** A9 has too much showdown value to turn into a bluff-raise, but isn't strong enough for a value raise. This is the classic "middle of range = call" on the river.

### Group 4: Made hand without flush — CALL

| # | Hero Hand | Solver Action | Notes |
|---|-----------|--------------|-------|
| 10 | All K7 variants | **CALL** | Two pair (K7) on As7s3cKs9d. Strong but not a flush. Calls — can't raise for value (only flushes call a raise), can't bluff (has showdown value). |

**Teaching point:** Two pair on a 4-flush board = pure call. Raising folds out everything hero beats and gets called only by flushes that beat hero.

---

## Training label for original hand

FB_Board4_h2 (Ts 8s): **RAISE** confirmed. Labeller was correct, reviewer was wrong.

---

## Key patterns for training selection (discuss later)

- All flushes raise (value) — teaches river value raising with made flushes on 4-flush boards
- Ace-blocker hands raise (bluff) — teaches river bluff-raising with blockers
- A9 calls (showdown value) — teaches that middle-strength hands with showdown value don't raise
- K7 calls (two pair) — teaches that non-flush made hands call on flush boards
- The flush/non-flush boundary is the raise/call boundary on this board
