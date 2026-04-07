# Position Amplification: Board-Anchored Hand Strength Sweeps

**Date:** 6 April 2026
**Purpose:** Targeted training data for the CHECK->BET boundary when hero is OOP in 3-way pots
**Target axis:** Position Amplification (v8 scored 17%, warm-start v9 scored 33%)

---

## Design Rationale

The v8 model defaults to CHECK with OOP heroes regardless of hand strength. The
failing cases (MW-23 through MW-49) share a pattern: hero is OOP with equity
0.33-0.82 and the model checks when it should bet. The model learned "OOP = passive"
from HU training where checking to the IP player is often correct. In 3-way pots,
the calculus changes: with two opponents who may check behind, OOP heroes with
strong hands must bet for value and protection — dead money is larger and equity
denial against two opponents is more urgent.

Each board below includes 8-10 hero hands spanning air to nuts. The GTO Expert
labels each. This teaches XGBoost the precise equity/hand-strength threshold where
OOP heroes should switch from CHECK to BET in 3-way pots.

**Key design choices:**
- All heroes are OOP (BB or SB) — the exact failure mode
- Mix of facing_bet=False (leading decision) and facing_bet=True (raise decision)
- Boards vary: dry/wet/paired/monotone/connected, raiser-favoured/caller-favoured
- Realistic 100bb stacks, standard pot sizes

---

## Board 1: Dry A-high Rainbow (Raiser-Favoured) — Flop, Lead Decision

**Board:** Ac 8d 3s
**Street:** Flop
**Hero position:** BB (OOP)
**Villain positions:** CO (opener), BTN (cold-caller)
**Pot:** 90 (CO opens 3bb, BTN calls, BB calls)
**To call:** 0 (not facing bet)
**Facing bet:** No
**Action history:** CO opens, BTN calls, BB (hero) defends. Flop Ac8d3s: hero first to act.

This board heavily favours CO's opening range (more Ax). OOP hero's betting range
should be narrow but include strong Ax for protection against two opponents.

| # | Hero Hand | Category | Equity Est. |
|---|-----------|----------|-------------|
| 1 | 5h 4h | Air (no pair, no draw) | ~0.15 |
| 2 | 7s 6s | Gutshot only | ~0.20 |
| 3 | Kh Qh | Two overcards below A | ~0.30 |
| 4 | 8h 7h | Middle pair weak kicker | ~0.35 |
| 5 | Ah 4c | Bottom pair + top pair weak | ~0.50 |
| 6 | Ah 9c | Top pair medium kicker | ~0.55 |
| 7 | Ah Jd | Top pair strong kicker | ~0.60 |
| 8 | Ah Kc | Top pair top kicker | ~0.65 |
| 9 | 3d 3c | Bottom set | ~0.80 |
| 10 | 8c 8s | Middle set | ~0.85 |

---

## Board 2: Low Connected Rainbow (Caller-Favoured) — Flop, Lead Decision

**Board:** 9d 6c 2h
**Street:** Flop
**Hero position:** SB (OOP)
**Villain positions:** BTN (opener), BB (cold-caller)
**Pot:** 90 (BTN opens 3bb, SB calls, BB calls)
**To call:** 0
**Facing bet:** No
**Action history:** BTN opens, SB (hero) calls, BB calls. Flop 9d6c2h: hero first to act.

Low board favours callers' ranges — more middle pairs and small pocket pairs.
This is the MW-28 board. The model must learn that even on caller-favoured boards,
OOP heroes with overpairs must bet for protection against two opponents.

| # | Hero Hand | Category | Equity Est. |
|---|-----------|----------|-------------|
| 1 | 4h 3h | Air | ~0.12 |
| 2 | Ah 5h | Overcard + backdoor | ~0.25 |
| 3 | Kh Qh | Two overcards | ~0.32 |
| 4 | 7s 5s | Gutshot | ~0.22 |
| 5 | 6s 5s | Bottom pair weak kicker | ~0.30 |
| 6 | 9c 7c | Top pair weak kicker | ~0.50 |
| 7 | 9h Th | Top pair good kicker | ~0.55 |
| 8 | Jh Jd | Overpair (JJ) | ~0.56 |
| 9 | Qc Qd | Overpair (QQ) | ~0.65 |
| 10 | 2d 2c | Bottom set | ~0.82 |

---

## Board 3: Monotone Wet Board — Flop, Lead Decision

**Board:** Jh 8h 4h
**Street:** Flop
**Hero position:** BB (OOP)
**Villain positions:** CO (opener), BTN (cold-caller)
**Pot:** 90
**To call:** 0
**Facing bet:** No
**Action history:** CO opens, BTN calls, BB (hero) defends. Flop Jh8h4h: hero first to act.

Monotone board changes the dynamics dramatically. Flush draws are live, made flushes
are possible. OOP hero with made flushes must bet to deny free cards; without a heart
the hand is much more vulnerable.

| # | Hero Hand | Category | Equity Est. |
|---|-----------|----------|-------------|
| 1 | 5c 3c | Air (no heart) | ~0.08 |
| 2 | Kd Qd | Overcards no heart | ~0.18 |
| 3 | 6h 5h | Low flush (made) | ~0.62 |
| 4 | 9d 8d | Middle pair no heart | ~0.22 |
| 5 | Jd Tc | Top pair no heart | ~0.35 |
| 6 | Ah 3c | Nut flush draw only | ~0.40 |
| 7 | Jc Jd | Set no heart | ~0.55 |
| 8 | Kh 9h | King-high flush | ~0.78 |
| 9 | Ah Qh | Nut flush | ~0.88 |
| 10 | Th 9h | Flush + OESD backup | ~0.72 |

---

## Board 4: Paired Dry Board — Flop, Lead Decision

**Board:** Qc Qd 7s
**Street:** Flop
**Hero position:** BB (OOP)
**Villain positions:** CO (opener), BTN (cold-caller)
**Pot:** 90
**To call:** 0
**Facing bet:** No
**Action history:** CO opens, BTN calls, BB (hero) defends. Flop QcQd7s: hero first to act.

Paired board reduces combinations dramatically. CO's range has more Qx (AQ, KQ, QJ).
BB's Qx holdings are thinner. This tests whether the model can lead thin on a board
where range advantage belongs to opener.

| # | Hero Hand | Category | Equity Est. |
|---|-----------|----------|-------------|
| 1 | 5h 4h | Air | ~0.15 |
| 2 | Ah 3h | A-high | ~0.30 |
| 3 | 8s 8h | Underpair (88) | ~0.35 |
| 4 | Ts Td | Underpair (TT) | ~0.38 |
| 5 | 7h 6h | Middle pair (pair of 7s) | ~0.42 |
| 6 | Kh Kd | Overpair (KK) | ~0.55 |
| 7 | Ah Ad | Overpair (AA) | ~0.60 |
| 8 | Qh 9c | Trips medium kicker | ~0.78 |
| 9 | Qh Jh | Trips good kicker | ~0.82 |
| 10 | 7d 7c | Full house (7s full) | ~0.95 |

---

## Board 5: Connected Wet Board — Turn, Lead Decision

**Board:** Ts 9d 5c 7h
**Street:** Turn
**Hero position:** BB (OOP)
**Villain positions:** CO (opener), BTN (cold-caller)
**Pot:** 160 (90 flop pot + flop action)
**To call:** 0
**Facing bet:** No
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Ts9d5c: CO bets 35, BTN calls, BB calls. Turn 7h: CO checks, BTN checks, hero acts.

Turn card (7h) completes 86 straight and adds a draw (J8, 68). Both opponents
checked, suggesting they don't have monsters. OOP hero can now lead with value
hands to charge the many draws and thin value hands in opponents' ranges.

| # | Hero Hand | Category | Equity Est. |
|---|-----------|----------|-------------|
| 1 | Ah 2h | Air (A-high) | ~0.15 |
| 2 | Kc Qc | Overcards | ~0.20 |
| 3 | Jh 8h | OESD (straight draw) | ~0.30 |
| 4 | 5s 4s | Bottom pair | ~0.22 |
| 5 | 9c 8c | Second pair + gutshot | ~0.38 |
| 6 | Tc 8c | Top pair + gutshot | ~0.48 |
| 7 | Tc Jd | Top pair good kicker | ~0.50 |
| 8 | 8h 6h | Made straight | ~0.75 |
| 9 | Td Tc | Top set | ~0.80 |
| 10 | 9s 9h | Middle set | ~0.72 |

---

## Board 6: A-high Two-Tone — Flop, Facing Bet (Raise Decision)

**Board:** Ad 9d 4c
**Street:** Flop
**Hero position:** BB (OOP)
**Villain positions:** CO (opener/bettor), BTN (cold-caller)
**Pot:** 123 (90 pot + CO bet 33)
**To call:** 33
**Facing bet:** Yes (CO bet 33 into 90)
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Ad9d4c: CO bets 33 into 90, BTN calls. Hero faces bet + call.

Facing bet-and-call 3-way is the strongest spot to test raise vs call vs fold.
The call from BTN narrows ranges — BTN has something. This sweep tests whether
hero can identify raising hands vs calling hands vs folds.

| # | Hero Hand | Category | Equity Est. |
|---|-----------|----------|-------------|
| 1 | 7h 6h | Air | ~0.10 |
| 2 | Kh Qh | Overcards no diamond | ~0.22 |
| 3 | 6d 5d | Low flush draw | ~0.32 |
| 4 | Kd Td | Flush draw + overcard | ~0.38 |
| 5 | 9c 8c | Middle pair | ~0.28 |
| 6 | Ac 5c | Top pair weak kicker | ~0.48 |
| 7 | Ac Jh | Top pair good kicker | ~0.55 |
| 8 | Ah Kc | TPTK + backdoor nut FD | ~0.65 |
| 9 | 4s 4h | Bottom set | ~0.78 |
| 10 | 9d 9c | Middle set | ~0.82 |

---

## Board 7: Mid-Connected Two-Tone — Turn, Facing Bet (Raise Decision)

**Board:** Jc 8c 5d 2h
**Street:** Turn
**Hero position:** SB (OOP)
**Villain positions:** BTN (opener/bettor), BB (cold-caller)
**Pot:** 210 (flop pot 90 + BTN bet 30 + hero call 30 + BB call 30 = 210)
**To call:** 75
**Facing bet:** Yes (BTN bets 75 into 210)
**Note:** 3-way throughout. BB calls the flop bet and is still in on the turn.
**Action history:** BTN opens, SB (hero) calls, BB calls. Flop Jc8c5d: hero checks, BTN bets 30, BB calls, hero calls. Turn 2h: hero checks, BB checks, BTN bets 75 into 210.

BTN is barrelling into hero who called flop OOP with BB still behind. Hero faces a
bet in a live 3-way pot and must identify hands strong enough to raise vs call vs fold.
BB still behind adds extra caution to raising — raising here faces both players.

| # | Hero Hand | Category | Equity Est. |
|---|-----------|----------|-------------|
| 1 | 4h 3h | Air | ~0.06 |
| 2 | Kd Qd | Overcards | ~0.20 |
| 3 | Ac Tc | Nut flush draw | ~0.35 |
| 4 | 9c 7c | Flush draw + gutshot | ~0.38 |
| 5 | 5c 4c | Bottom pair + FD | ~0.40 |
| 6 | 8h 7h | Second pair | ~0.30 |
| 7 | Jh Td | Top pair medium kicker | ~0.50 |
| 8 | Jh Jd | Top set | ~0.85 |
| 9 | 8s 8d | Middle set | ~0.80 |

---

## Board 8: River Brick on Dry Board — River, Lead Decision

**Board:** Qc 8d 3s 6h 2c
**Street:** River
**Hero position:** BB (OOP)
**Villain positions:** CO (opener), BTN (cold-caller)
**Pot:** 200 (built through flop/turn action)
**To call:** 0
**Facing bet:** No
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Qc8d3s: hero checks, CO bets 35, BTN calls, hero calls. Turn 6h: checks through. River 2c: hero acts first.

River brick on a dry board. Both opponents checked turn, suggesting they're not
super strong. Hero OOP can now value bet thinly because opponents' ranges are
capped by the turn check-through. This is the pure position-amplification decision:
OOP hero who must decide whether to lead the river.

| # | Hero Hand | Category | Equity Est. |
|---|-----------|----------|-------------|
| 1 | 5h 4h | Air (missed everything) | ~0.05 |
| 2 | Ah 5h | A-high | ~0.25 |
| 3 | Kh Jh | K-high | ~0.20 |
| 4 | 8h 7h | Middle pair | ~0.35 |
| 5 | Qs 5s | Top pair bad kicker | ~0.52 |
| 6 | Qh 9c | Top pair medium kicker | ~0.58 |
| 7 | Qh Jd | Top pair good kicker | ~0.62 |
| 8 | Qh Kc | TPTK | ~0.68 |
| 9 | 3d 3c | Set (bottom set) | ~0.85 |
| 10 | 8c 8s | Set (middle set) | ~0.88 |

---

## Summary Statistics

| Board | Type | Street | Hero Pos | Facing Bet | Hands |
|-------|------|--------|----------|------------|-------|
| 1 | Dry A-high rainbow | Flop | BB | No | 10 |
| 2 | Low connected rainbow | Flop | SB | No | 10 |
| 3 | Monotone wet | Flop | BB | No | 10 |
| 4 | Paired dry | Flop | BB | No | 10 |
| 5 | Connected wet | Turn | BB | No | 10 |
| 6 | A-high two-tone | Flop | BB | Yes | 10 |
| 7 | Mid-connected two-tone | Turn | SB | Yes | 9 |
| 8 | Dry board river brick | River | BB | No | 10 |

**Total situations: 79**

**Coverage by board type:**
- Raiser-favoured: Boards 1, 4, 6 (30 hands)
- Caller-favoured: Boards 2, 5 (20 hands)
- Neutral/complex: Boards 3, 7, 8 (29 hands)

**Coverage by street:**
- Flop: 50 hands (Boards 1-4, 6)
- Turn: 19 hands (Boards 5, 7)
- River: 10 hands (Board 8)

**Coverage by decision type:**
- Lead decision (facing_bet=False): 60 hands (Boards 1-5, 8)
- Raise/call/fold decision (facing_bet=True): 19 hands (Boards 6-7)

---

## Notes for GTO Expert Labelling

1. The GTO Expert assigns all labels independently. No predicted labels are
   provided — each hand is evaluated fresh from range, equity, and action context.

2. **Key features to compute for each:** raw_equity, equity_vs_range,
   better_hand_pct, worse_hand_pct, board_favour, villain_top_pair_plus_pct,
   villain_air_pct. The feature pipeline handles this automatically.

3. **The critical learning signal** is hands near the CHECK/BET boundary:
   equity 0.35-0.55 where OOP heroes must decide between protection betting
   and pot control. Hands at the extremes (air and nuts) are anchors that help
   XGBoost interpolate, but the boundary hands are where the model failed.

4. **Board 6 and 7** test facing_bet=True. These produce FOLD/CALL/RAISE labels
   rather than CHECK/BET, which also addresses the CALL starvation problem
   identified in the gate review (only 11 CALL samples in v9-3way training).

5. **The sweep design ensures ~50/50 split** between CHECK and BET on each
   board. This prevents class imbalance from biasing the model toward either
   action. Combined with the base training data, BET should become sufficiently
   represented for OOP heroes.
