# Design: Board-Anchored CALL Sweeps for v9-3way

**Date:** 6 April 2026
**Status:** DESIGN — awaiting owner review before generation

---

## Purpose

The v9-3way model has 11 CALL training samples out of 199 total. It
defaults to FOLD or RAISE in spots where CALL is correct. This design
produces 72 new situations across 8 boards, all targeting CALL decision
boundaries in 3-way pots.

## Three boundaries to teach

1. **FOLD to CALL** — equity is marginal but pot odds or implied odds
   justify continuing (draws, overcards with backdoors)
2. **CALL to RAISE** — hand is strong enough to continue but not strong
   enough to raise for value (bluff-catchers, medium pairs on wet boards)
3. **Anti-over-call** — high raw equity does NOT mean call when opponent
   action screams strength (check-raises, multi-barrel with callers)

## Encoding reference

Position: UTG=0, HJ=1, CO=2, BTN=3, SB=4, BB=5
Street: flop=0, turn=1, river=2
Hand category: high_card=0, one_overcard=1, overcards=2, bottom_pair=3,
  underpair=4, middle_pair=5, top_pair=6, top_pair_good_kicker=7,
  top_pair_top_kicker=8, overpair=9, two_pair=10, trips=11, set=12,
  straight=13, flush=14, full_house=15, quads=16, straight_flush=17

---

## Board 1: Jd 8d 4c (Flop) — Draw vs Made Hand Boundary

**Theme:** FOLD-to-CALL boundary. Draws need pot odds to continue.
Mirrors MW-17 (AKo overcards, expert=CALL) and MW-18 (flush draw, expert=CALL).

**Hero position:** BB (pos=5)
**Primary villain position:** CO (pos=2)
**is_ip:** 0 (OOP)
**Pot:** 90, To call: 33, Pot odds: 0.268, Bet-to-pot: 0.367
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Jd8d4c:
CO bets 33 into 90. BTN still to act behind.
**SPR:** ~1.1 (100bb stacks, ~90bb behind each)
**Board:** two-tone (diamonds), unpaired, connectivity=4, high_card=J(11),
danger_score ~0.25, flush_danger=0.49, straight_danger=0.0
**Villain context:** villain_aggression_count=1, villain_checked_back=0,
villain_call_count=0, num_callers_to_bet=0, facing_raise=0,
villain_top_pair_plus_pct ~0.47, villain_air_pct ~0.25, villain_range_capped=0

| # | Hero Hand | Category | Equity | Draw Outs | FD | SD |
|---|-----------|----------|--------|-----------|----|----|
| 1 | 6s 3c | high_card (0) | 0.04 | 0 | 0 | 0 |
| 2 | Ts 5s | one_overcard (1) | 0.09 | 0 | 0 | 0 |
| 3 | 9h 7h | high_card (0) | 0.22 | 8 | 0 | 1 |
| 4 | Qd 3d | one_overcard (1) | 0.36 | 9 | 1 | 0 |
| 5 | 7d 6d | high_card (0) | 0.38 | 12 | 1 | 1 |
| 6 | Ad Ks | overcards (2) | 0.25 | 0 | 0 | 0 |
| 7 | 8c 7c | middle_pair (5) | 0.31 | 4 | 0 | 0 |
| 8 | Jc 5h | top_pair (6) | 0.47 | 0 | 0 | 0 |
| 9 | Js Th | top_pair_good_kicker (7) | 0.52 | 0 | 0 | 0 |

**9 situations.**

---

## Board 2: Ks 9h 5d (Flop) — Bluff-Catcher Boundary IP

**Theme:** CALL-to-RAISE boundary. Hero IP with medium-strength hands.
When to flat vs when to raise for protection.

**Hero position:** BTN (pos=3)
**Primary villain position:** BB (pos=5)
**is_ip:** 1 (IP — BTN acts after BB/CO postflop)
**Pot:** 90, To call: 45, Pot odds: 0.333, Bet-to-pot: 0.500
**Action history:** CO opens, BTN (hero) calls, BB calls. Flop Ks9h5d:
BB leads 45 into 90. CO folds.
**SPR:** ~1.0
**Board:** rainbow, unpaired, connectivity=3, high_card=K(13),
danger_score ~0.0, flush_danger=0.0, straight_danger=0.0
**Villain context:** villain_aggression_count=0, villain_checked_back=0,
villain_call_count=1, num_callers_to_bet=0, facing_raise=0,
villain_top_pair_plus_pct ~0.27, villain_air_pct ~0.30, villain_range_capped=1

| # | Hero Hand | Category | Equity | Draw Outs | FD | SD |
|---|-----------|----------|--------|-----------|----|----|
| 1 | 7c 2h | high_card (0) | 0.05 | 0 | 0 | 0 |
| 2 | Qh Jh | overcards (2) | 0.18 | 0 | 0 | 0 |
| 3 | Th 8h | high_card (0) | 0.19 | 4 | 0 | 1 |
| 4 | 6d 4d | high_card (0) | 0.15 | 4 | 0 | 1 |
| 5 | 9c Tc | middle_pair (5) | 0.33 | 0 | 0 | 0 |
| 6 | 9s 8s | middle_pair (5) | 0.31 | 0 | 0 | 0 |
| 7 | Kc 4c | top_pair (6) | 0.52 | 0 | 0 | 0 |
| 8 | Kh Jd | top_pair_good_kicker (7) | 0.58 | 0 | 0 | 0 |
| 9 | As Ah | overpair (9) | 0.68 | 0 | 0 | 0 |

**9 situations.**

---

## Board 3: Qh 7c 2s 5d (Turn) — Turn Barrel Bluff-Catcher

**Theme:** CALL on turn facing double barrel. Teaches CALL-to-RAISE
boundary on later streets where ranges are narrower.

**Hero position:** BTN (pos=3)
**Primary villain position:** CO (pos=2)
**is_ip:** 1
**Pot:** 156, To call: 60, Pot odds: 0.278, Bet-to-pot: 0.385
**Action history:** CO opens, BTN (hero) calls, BB calls. Flop Q72r:
CO bets 33, hero calls, BB folds. Turn 5d: CO fires 60 into 156.
**SPR:** ~0.6
**Board:** rainbow, unpaired, connectivity=2, high_card=Q(12),
danger_score ~0.2, flush_danger=0.0, straight_danger=0.0
**Villain context:** villain_aggression_count=2, villain_checked_back=0,
villain_call_count=0, num_callers_to_bet=0, facing_raise=0,
villain_top_pair_plus_pct ~0.50, villain_air_pct ~0.18, villain_range_capped=0

| # | Hero Hand | Category | Equity | Draw Outs | FD | SD |
|---|-----------|----------|--------|-----------|----|----|
| 1 | Jh Th | high_card (0) | 0.08 | 4 | 0 | 1 |
| 2 | 9h 8h | high_card (0) | 0.10 | 4 | 0 | 1 |
| 3 | Ah 3h | one_overcard (1) | 0.14 | 3 | 0 | 0 |
| 4 | 5h 5c | set (12) | 0.91 | 0 | 0 | 0 |
| 5 | Qd Jd | top_pair_good_kicker (7) | 0.55 | 0 | 0 | 0 |
| 6 | Qs Ts | top_pair (6) | 0.45 | 0 | 0 | 0 |
| 7 | 7d 6d | middle_pair (5) | 0.22 | 0 | 0 | 0 |
| 8 | Qc Kh | top_pair_top_kicker (8) | 0.60 | 0 | 0 | 0 |
| 9 | Qs Jh | top_pair_good_kicker (7) | 0.48 | 0 | 0 | 0 |

**9 situations.**

---

## Board 4: Ah 9c 3s 6d Tc (River) — River Decision with Narrow Ranges

**Theme:** Anti-over-call. River decisions where range analysis matters
more than raw equity. Mirrors MW-46 (trips facing check-raise = FOLD).

**Hero position:** BB (pos=5)
**Primary villain position:** CO (pos=2)
**is_ip:** 0
**Pot:** 280, To call: 140, Pot odds: 0.333, Bet-to-pot: 0.500
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop A93r:
CO bets, BTN folds, hero calls. Turn 6: check-check. River T: CO bets
140 into 280.
**SPR:** 0.0 (effectively all-in decision)
**Board:** rainbow, unpaired, connectivity=3, high_card=A(14),
danger_score ~0.5, flush_danger=0.0, straight_danger=0.3
**Villain context:** villain_aggression_count=1, villain_checked_back=1,
villain_call_count=0, num_callers_to_bet=0, facing_raise=0,
villain_top_pair_plus_pct ~0.55, villain_air_pct ~0.15, villain_range_capped=0

| # | Hero Hand | Category | Equity | Draw Outs | FD | SD |
|---|-----------|----------|--------|-----------|----|----|
| 1 | Kd Qd | high_card (0) | 0.06 | 0 | 0 | 0 |
| 2 | 8s 7s | high_card (0) | 0.03 | 0 | 0 | 0 |
| 3 | Jd Jc | underpair (4) | 0.20 | 0 | 0 | 0 |
| 4 | 9d 8d | middle_pair (5) | 0.28 | 0 | 0 | 0 |
| 5 | As 5s | top_pair (6) | 0.42 | 0 | 0 | 0 |
| 6 | Ad Jd | top_pair_good_kicker (7) | 0.52 | 0 | 0 | 0 |
| 7 | Ac Kc | top_pair_top_kicker (8) | 0.60 | 0 | 0 | 0 |
| 8 | Tc 9c | two_pair (10) | 0.75 | 0 | 0 | 0 |
| 9 | 3h 3d | set (12) | 0.90 | 0 | 0 | 0 |

**9 situations.**

---

## Board 5: Kd Jc 6s (Flop) — Anti-Over-Call with Caller Behind

**Theme:** Anti-over-call. CO bets, BTN CALLS, hero in BB faces bet +
caller. The BTN cold-call dramatically strengthens the remaining range.
Mirrors MW-30 (KTo top pair, expert=FOLD despite 0.40 equity).

**Note:** This is technically 4-way preflop (CO opens, BTN calls, SB calls,
BB calls) becoming 3-way on the flop when SB folds. The feature extractor
should encode the flop as 3-way active (villain_positions: CO, BTN).
Preflop player count does not affect postflop feature encoding here.

**Hero position:** BB (pos=5)
**Primary villain position:** CO (pos=2)
**is_ip:** 0
**Pot:** 155, To call: 35, Pot odds: 0.184, Bet-to-pot: 0.226
**Action history:** CO opens, BTN calls, SB calls, BB (hero) calls.
Flop KJ6r: SB folds, CO bets 35, BTN CALLS. Hero faces bet + call.
**SPR:** ~0.65
**Board:** rainbow, unpaired, connectivity=3, high_card=K(13),
danger_score ~0.0, flush_danger=0.0, straight_danger=0.0
**Villain context:** villain_aggression_count=1, villain_checked_back=0,
villain_call_count=0, num_callers_to_bet=1, facing_raise=0,
villain_top_pair_plus_pct ~0.41, villain_air_pct ~0.15, villain_range_capped=0

| # | Hero Hand | Category | Equity | Draw Outs | FD | SD |
|---|-----------|----------|--------|-----------|----|----|
| 1 | 5h 4h | high_card (0) | 0.03 | 0 | 0 | 0 |
| 2 | Th 9h | high_card (0) | 0.12 | 4 | 0 | 1 |
| 3 | Qc Ts | high_card (0) | 0.14 | 4 | 0 | 1 |
| 4 | 6c 5c | bottom_pair (3) | 0.15 | 0 | 0 | 0 |
| 5 | Kc Th | top_pair (6) | 0.40 | 0 | 0 | 0 |
| 6 | Kh Qh | top_pair_good_kicker (7) | 0.48 | 0 | 0 | 0 |
| 7 | Ks Jd | two_pair (10) | 0.72 | 0 | 0 | 0 |
| 8 | Jh Ts | middle_pair (5) | 0.25 | 0 | 0 | 0 |
| 9 | Ac Qc | overcards (2) | 0.20 | 0 | 0 | 0 |

**9 situations.**

---

## Board 6: Ts 8h 3s (Flop) — Wet Board Draw Equity OOP

**Theme:** FOLD-to-CALL boundary on wet board. Flush draws and straight
draws have implied odds despite being OOP. Teaches that draws are
worth calling but pure air is not.

**Hero position:** BB (pos=5)
**Primary villain position:** CO (pos=2)
**is_ip:** 0
**Pot:** 90, To call: 25, Pot odds: 0.217, Bet-to-pot: 0.278
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Ts8h3s:
CO bets 25 into 90 (small sizing).
**SPR:** ~1.1
**Board:** two-tone (spades), unpaired, connectivity=5, high_card=T(10),
danger_score ~0.35, flush_danger=0.49, straight_danger=0.3
**Villain context:** villain_aggression_count=1, villain_checked_back=0,
villain_call_count=0, num_callers_to_bet=0, facing_raise=0,
villain_top_pair_plus_pct ~0.35, villain_air_pct ~0.30, villain_range_capped=0

| # | Hero Hand | Category | Equity | Draw Outs | FD | SD |
|---|-----------|----------|--------|-----------|----|----|
| 1 | Kd 2d | one_overcard (1) | 0.07 | 0 | 0 | 0 |
| 2 | Qd 4d | one_overcard (1) | 0.06 | 0 | 0 | 0 |
| 3 | 7s 6s | high_card (0) | 0.38 | 13 | 1 | 1 |
| 4 | As Kh | one_overcard (1) | 0.30 | 9 | 1 | 0 |
| 5 | 9h 7h | high_card (0) | 0.27 | 8 | 0 | 1 |
| 6 | Jc 9c | high_card (0) | 0.23 | 4 | 0 | 1 |
| 7 | 3d 3c | set (12) | 0.89 | 0 | 0 | 0 |
| 8 | Td 7d | top_pair (6) | 0.45 | 0 | 0 | 0 |
| 9 | 8d 7d | middle_pair (5) | 0.28 | 4 | 0 | 1 |

**9 situations.**

---

## Board 7: As Qd 5h (Flop) — Facing Check-Raise (Anti-Over-Call)

**Theme:** Anti-over-call facing extreme aggression. Mirrors MW-31
(AJ facing raise, expert=FOLD despite equity 0.653). Raises after
hero bets in 3-way pots are extremely polarized toward the nuts.

**Hero position:** BTN (pos=3)
**Primary villain position:** CO (pos=2)
**is_ip:** 1
**Pot:** 210, To call: 60, Pot odds: 0.222, Bet-to-pot: 0.286
**Action history:** CO opens, BTN (hero) calls, BB calls. Flop AQ5r:
BB checks, hero bets 30, CO raises to 90. BB folds. Hero faces standard raise
(CO raised hero's bet — CO did not check first, so this is a raise, not a check-raise).
**SPR:** ~0.5
**Board:** rainbow, unpaired, connectivity=1, high_card=A(14),
danger_score ~0.0, flush_danger=0.0, straight_danger=0.0
**Villain context:** villain_aggression_count=1, villain_checked_back=0,
villain_call_count=0, num_callers_to_bet=0, facing_raise=1,
villain_top_pair_plus_pct ~0.80, villain_air_pct ~0.05, villain_range_capped=0

| # | Hero Hand | Category | Equity | Draw Outs | FD | SD |
|---|-----------|----------|--------|-----------|----|----|
| 1 | Kh Jh | high_card (0) | 0.12 | 0 | 0 | 0 |
| 2 | Th 9h | high_card (0) | 0.06 | 4 | 0 | 0 |
| 3 | 5c 4c | bottom_pair (3) | 0.10 | 0 | 0 | 0 |
| 4 | Qc Jc | middle_pair (5) | 0.25 | 0 | 0 | 0 |
| 5 | Ah Jh | top_pair (6) | 0.42 | 0 | 0 | 0 |
| 6 | Ac Js | top_pair_good_kicker (7) | 0.48 | 0 | 0 | 0 |
| 7 | Ac Kc | top_pair_top_kicker (8) | 0.55 | 0 | 0 | 0 |
| 8 | Ad Qd | two_pair (10) | 0.82 | 0 | 0 | 0 |
| 9 | 5s 5d | set (12) | 0.93 | 0 | 0 | 0 |

**9 situations.**

---

## Board 8: 7h 7d 5s 9c Js (River) — Trips Facing Check-Raise

**Theme:** Anti-over-call at its most extreme. Mirrors MW-46 exactly
(Ks7c trips facing river c/r, expert=FOLD despite equity 0.908).
Even monster-looking hands must fold to the most credible strength lines.

**Hero position:** BTN (pos=3)
**Primary villain position:** CO (pos=2)
**is_ip:** 1
**Pot:** 500, To call: 200, Pot odds: 0.286, Bet-to-pot: 0.400
**Action history:** HJ opens, CO calls, BTN (hero) calls, BB calls.
Flop 775: CO bets, BTN calls, others fold. Turn 9: CO checks, hero bets,
CO calls. River J: CO check-raises hero.
**SPR:** 0.0 (all-in decision)
**Board:** paired, two-tone, connectivity=5, high_card=J(11),
danger_score ~0.7, flush_danger=0.0, straight_danger=0.5
**Villain context:** villain_aggression_count=1, villain_checked_back=1,
villain_call_count=2, num_callers_to_bet=0, facing_raise=1,
villain_top_pair_plus_pct ~0.90, villain_air_pct ~0.02, villain_range_capped=0

| # | Hero Hand | Category | Equity | Draw Outs | FD | SD |
|---|-----------|----------|--------|-----------|----|----|
| 1 | Ts 8s | straight (13) | 0.55 | 0 | 0 | 0 |
| 2 | Ks 7c | trips (11) | 0.30 | 0 | 0 | 0 |
| 3 | Jd Jc | full_house (15) | 0.85 | 0 | 0 | 0 |
| 4 | 9s 9h | full_house (15) | 0.78 | 0 | 0 | 0 |
| 5 | Ad Kd | high_card (0) | 0.02 | 0 | 0 | 0 |
| 6 | As 7s | trips (11) | 0.35 | 0 | 0 | 0 |
| 7 | 5c 5h | full_house (15) | 0.72 | 0 | 0 | 0 |
| 8 | 7s 5c | full_house (15) | 0.95 | 0 | 0 | 0 |
| 9 | Ac Jh | top_pair (6) | 0.12 | 0 | 0 | 0 |

**9 situations.**

---

## Summary

| Board | Street | Hero Pos | IP? | Theme | Total |
|-------|--------|----------|-----|-------|-------|
| 1: Jd8d4c | Flop | BB | OOP | Draw calls | 9 |
| 2: Ks9h5d | Flop | BTN | IP | Bluff-catchers | 9 |
| 3: Qh7c2s5d | Turn | BTN | IP | Turn barrel | 9 |
| 4: Ah9c3s6dTc | River | BB | OOP | River narrow ranges | 9 |
| 5: KdJc6s | Flop | BB | OOP | Anti-over-call (caller) | 9 |
| 6: Ts8h3s | Flop | BB | OOP | Wet board draws | 9 |
| 7: AsQd5h | Flop | BTN | IP | Anti-over-call (c/r) | 9 |
| 8: 775-9-J | River | BTN | IP | Extreme anti-over-call | 9 |
| **Total** | | | | | **72** |

### Design coverage

| Boundary | Boards covering it | Situations |
|----------|--------------------|------------|
| FOLD to CALL (draws, pot odds) | 1, 2, 6 | ~18 |
| CALL to RAISE (bluff-catchers) | 2, 3, 4 | ~15 |
| Anti-over-call (fold despite equity) | 5, 7, 8 | ~18 |
| River narrow ranges | 4, 8 | ~18 |

### Feature diversity

| Feature | Range covered |
|---------|--------------|
| Pot odds | 0.18 to 0.33 |
| Streets | Flop (5), Turn (1), River (2) |
| IP/OOP | IP (4 boards), OOP (4 boards) |
| facing_raise | 0 (6 boards), 1 (2 boards) |
| num_callers_to_bet | 0 (7 boards), 1 (1 board) |
| SPR | 0.0 to 1.1 |
| Board texture | Rainbow (4), two-tone (3), paired (1) |

### Pot odds variation

| Board | Pot odds | Sizing description |
|-------|----------|--------------------|
| 5 | 0.184 | Small bet + cold-caller |
| 6 | 0.217 | Small bet (~28% pot) |
| 7 | 0.222 | Check-raise (~29% pot) |
| 1 | 0.268 | Standard 1/3 pot c-bet |
| 3 | 0.278 | Standard turn barrel |
| 4, 8 | 0.286-0.333 | Half-pot river / half-pot flop |

---

## Open Questions for Owner

1. **Volume:** 72 situations across 8 boards. Should we add 1-2 more
   boards to reach 80+, or is 72 sufficient?

2. **Board 8 complexity:** The MW-46 mirror (paired board, trips folding
   to c/r) is the hardest concept. Should we simplify or keep as-is?

3. **3-bet pot boards:** All boards above are single-raised pots. Should
   one board be a 3-bet pot (is_3bet_pot=1, smaller SPR, tighter ranges)?

4. **RAISE labels:** 12 RAISE situations are included for contrast. Too
   many, too few?

5. **Generation method:** After approval, should these be generated as
   a hand-coded JSONL (precise control) or run through the feature
   extractor pipeline (ensures feature consistency)?
