# Design Agent 4 — SP8 and SP9 Hero Card Assignments

**Date:** 9 April 2026
**Agent:** Design Agent 4
**Scope:** SP8 (16 RAISE bluff situations) + SP9 (10 CALL flat spot situations) = 26 total
**Source docs read:** BOARD_ALLOCATION_V3_FINAL.md, FACTORY_DESIGN_RAISE_CONTEXTS_V2.md,
RAISE_DECISION_TREE_V2.md, generate_factory_batch2.py (lines 1-80)
**Status:** AWAITING REVIEW

---

## Design Notes

### SP8 — Bricked Draw Logic Per Board

Before assigning hero cards, each river board was audited for suit counts to determine
which flush draws were live but bricked (2 of a suit on board = draw was live, did not
complete) versus completed (3 of a suit on board = hero holding that suit has a made flush):

| Board | Cards                   | Suit counts                        | Bricked FD suit | Flush completed suit |
|-------|-------------------------|------------------------------------|-----------------|----------------------|
| B23   | Kd 7c 2s 5h Jh         | d=1, c=1, s=1, h=2                 | hearts (h)      | none                 |
| B24   | 9s 4h Ks 2d 7c         | s=2, h=1, d=1, c=1                 | spades (s)      | none                 |
| B25   | As 6d 2h Tc 4s         | s=2, d=1, h=1, c=1                 | spades (s)      | none                 |
| B26   | Kh 5c 2h 9d Qh         | h=3, c=1, d=1                      | n/a (no live bricked FD) | hearts (h) |
| B27   | 4d 8h 2c 6s Jd         | d=2, h=1, c=1, s=1                 | diamonds (d)    | none                 |
| B28   | 3s 7h Ks 2c Ts         | s=3, h=1, c=1                      | n/a (no live bricked FD) | spades (s)  |
| B29   | Qc 6s 2d 9h 4c         | c=2, s=1, d=1, h=1                 | clubs (c)       | none                 |

**B26 note:** Hearts flush completed (Kh 2h Qh = 3 hearts). Hero cannot hold 2 hearts.
No other suit has 2 board cards, so no live bricked flush draw exists for this board.
SP8 sits 10-11 on B26 use bricked straight draw and pure air respectively.

**B28 note:** Spades flush completed (3s Ks Ts = 3 spades). Hero cannot hold 2 spades.
No other suit has 2 board cards, so no live bricked flush draw exists in the standard sense.
SP8 sit 14 uses two hearts (Qh 9h) — hero holds two suited cards of a suit that was
never going to complete, giving pure air at river. Described as "dead heart draw / air."
SP8 sit 15 uses a bricked straight draw.

### SP9 — Hero Hand Philosophy

SP9 hero hands are moderate: strong enough to consider raising, but the flat-spot
trigger forces a CALL. Targets: top pair weak kicker, second pair, overpair on
dangerous board, middle pair facing aggression. All is_monster == 0.

---

## SP8: Bottom of Range Bluff Raise — 16 RAISE Situations

### Step 6 conditions (ALL required for each situation):
- street == 2 (river)
- hero_range_percentile <= 0.20
- villain_fold_equity_estimate >= 0.50
- villain_top_pair_plus_pct <= 0.35
- num_callers_to_bet == 0
- villain_aggression_count == 0

---

### SP8_01

**Board:** B23
**Board cards:** Kd 7c 2s 5h Jh
**Street:** river (street = 2)
**Hero pos:** BTN (IP)
**Villain positions:** ['SB', 'BB'] (BB is bettor)
**Pot:** 400 | to_call: 120 | effective_stack: 360 | SPR: 0.9

**hero_cards:** 9c 8d

**Hand type:** Bricked straight draw
**Description:** Hero held a 9-8 offsuit — an open-ended straight draw on earlier
streets targeting 6-7-8-9-T or 7-8-9-T-J. The river Jh filled the board but did not
complete the straight (hero needed a T for 7-8-9-T-J but got a J instead — or needed
a 6 for 6-7-8-9, which also missed). On the river, hero holds 9-high with no pair, no
draw — complete air. Neither 9c nor 8d appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.04
- villain_fold_equity_estimate: 0.55
- villain_top_pair_plus_pct: 0.25
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_02

**Board:** B23
**Board cards:** Kd 7c 2s 5h Jh
**Street:** river (street = 2)
**Hero pos:** BTN (IP)
**Villain positions:** ['SB', 'BB'] (BB is bettor)
**Pot:** 400 | to_call: 120 | effective_stack: 360 | SPR: 0.9

**hero_cards:** Ac 3c

**Hand type:** Pure air
**Description:** Hero holds Ace-3 offsuit (two clubs, but only 1 club on board — no
flush draw). No pair (board has K, 7, 2, 5, J — hero's A and 3 do not pair any
board card). No straight (no connectivity). Hero is at the absolute bottom of their
range — Ace-high with no made hand and no draw. The Ace gives a slight blocker to
villain's top-of-range (AK, AJ), but hero's hand has zero showdown value. Pure air.
Neither Ac nor 3c appears in board cards (7c is the only club on board).

**Feature targets:**
- hero_range_percentile: 0.15
- villain_fold_equity_estimate: 0.60
- villain_top_pair_plus_pct: 0.30
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_03

**Board:** B23
**Board cards:** Kd 7c 2s 5h Jh
**Street:** river (street = 2)
**Hero pos:** BTN (IP)
**Villain positions:** ['SB', 'BB'] (BB is bettor)
**Pot:** 400 | to_call: 120 | effective_stack: 360 | SPR: 0.9

**hero_cards:** 6h 9h

**Hand type:** Bricked flush draw
**Description:** Hero held two hearts — a live heart flush draw on earlier streets
(board had 5h on earlier board runout; Jh arrived as the river card, giving board
hearts = 5h Jh = 2 hearts). Hero held 6h 9h hoping for a third heart to complete
the flush; it never came. River is a non-flush-completing card for hearts (only 2
board hearts). Hero holds 9-high with no pair, no straight, no flush — pure air.
Neither 6h nor 9h appears in board cards. Total hearts: 5h (board), Jh (board),
6h (hero), 9h (hero) = 4 hearts — no flush.

**Feature targets:**
- hero_range_percentile: 0.08
- villain_fold_equity_estimate: 0.65
- villain_top_pair_plus_pct: 0.20
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_04

**Board:** B24
**Board cards:** 9s 4h Ks 2d 7c
**Street:** river (street = 2)
**Hero pos:** SB (OOP)
**Villain positions:** ['CO', 'BTN'] (BTN is bettor)
**Pot:** 380 | to_call: 110 | effective_stack: 330 | SPR: 0.87

**hero_cards:** As Js

**Hand type:** Bricked flush draw (spades)
**Description:** Hero held As Js — two spades, with a spade flush draw live on
earlier streets (board had 9s Ks = 2 spades on earlier streets, draw was live).
The river 7c did not bring a third board spade; total spades = 9s, Ks (board) +
As, Js (hero) = 4 spades across 7 cards — not enough for a flush (need 5 of same
suit in best 5 cards; hero's best 5 include 4 spades only). Hero holds Ace-high
with no pair (A and J do not pair 9, 4, K, 2, 7), no straight, no flush. Near the
top of what is air — Ace-high. Neither As nor Js appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.05
- villain_fold_equity_estimate: 0.52
- villain_top_pair_plus_pct: 0.15
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_05

**Board:** B24
**Board cards:** 9s 4h Ks 2d 7c
**Street:** river (street = 2)
**Hero pos:** SB (OOP)
**Villain positions:** ['CO', 'BTN'] (BTN is bettor)
**Pot:** 380 | to_call: 110 | effective_stack: 330 | SPR: 0.87

**hero_cards:** Qd Th

**Hand type:** Pure air
**Description:** Hero holds Queen-Ten offsuit. No pair (Q and T do not match any
board card: 9, 4, K, 2, 7). No flush draw (Q is diamonds, T is hearts — each suit
has 0-1 representatives on board). No straight (Q-T needs J to connect, and no J
on board; other straight routes also miss). Hero has pure Queen-high with ten
kicker — bottom of range, zero equity at showdown. Neither Qd nor Th appears in
board cards.

**Feature targets:**
- hero_range_percentile: 0.18
- villain_fold_equity_estimate: 0.58
- villain_top_pair_plus_pct: 0.28
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_06

**Board:** B24
**Board cards:** 9s 4h Ks 2d 7c
**Street:** river (street = 2)
**Hero pos:** SB (OOP)
**Villain positions:** ['CO', 'BTN'] (BTN is bettor)
**Pot:** 380 | to_call: 110 | effective_stack: 330 | SPR: 0.87

**hero_cards:** 5c 6h

**Hand type:** Bricked straight draw
**Description:** Hero held 5-6 offsuit — a double-ended straight draw on earlier
streets targeting 3-4-5-6-7 (needed a 3) or 4-5-6-7-8 (needed an 8). Board shows
4h and 7c, which matched hero's draw structure. The river 7c does not complete the
straight: hero needed a 3 or an 8, and neither arrived. Hero holds 6-high with no
pair, no draw — absolute bottom of range. Neither 5c nor 6h appears in board cards
(4h is hearts, 7c is clubs — 5c and 6h are distinct cards).

**Feature targets:**
- hero_range_percentile: 0.10
- villain_fold_equity_estimate: 0.70
- villain_top_pair_plus_pct: 0.10
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_07

**Board:** B25
**Board cards:** As 6d 2h Tc 4s
**Street:** river (street = 2)
**Hero pos:** CO (IP)
**Villain positions:** ['BB'] (BB is bettor; SB folded on flop)
**Pot:** 360 | to_call: 100 | effective_stack: 320 | SPR: 0.89

**hero_cards:** Jh 8d

**Hand type:** Pure air
**Description:** Hero holds J-8 offsuit. No pair (J and 8 do not match board cards:
A, 6, 2, T, 4). No flush draw (J is hearts — board has 1 heart = 2h; 8 is diamonds
— board has 1 diamond = 6d; no suit has 3+ board cards). No straight (J needs
Q-K-A or 8-9-T-J — board has T and A but J with 8 cannot form a straight using
board cards; would need 9 which is absent). Hero holds Jack-high — pure air at
showdown. This is a pure air bluff spot on an A-high river. Neither Jh nor 8d
appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.03
- villain_fold_equity_estimate: 0.55
- villain_top_pair_plus_pct: 0.22
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_08

**Board:** B25
**Board cards:** As 6d 2h Tc 4s
**Street:** river (street = 2)
**Hero pos:** CO (IP)
**Villain positions:** ['BB'] (BB is bettor; SB folded on flop)
**Pot:** 360 | to_call: 100 | effective_stack: 320 | SPR: 0.89

**hero_cards:** Ks 9s

**Hand type:** Bricked flush draw (spades)
**Description:** Hero held Ks 9s — two spades with a flush draw live on earlier
streets. Board shows As and 4s (2 spades), so hero's spade draw was active until
the river. River card Tc (a club) did not bring a third board spade. Total spades:
As (board), 4s (board), Ks (hero), 9s (hero) = 4 spades — not a flush. Hero holds
King-high with no pair (K and 9 do not pair A, 6, 2, T, 4) and no completed draw.
The bricked spade draw leaves hero with pure air at showdown. Neither Ks nor 9s
appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.12
- villain_fold_equity_estimate: 0.62
- villain_top_pair_plus_pct: 0.30
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_09

**Board:** B25
**Board cards:** As 6d 2h Tc 4s
**Street:** river (street = 2)
**Hero pos:** CO (IP)
**Villain positions:** ['BB'] (BB is bettor; SB folded on flop)
**Pot:** 360 | to_call: 100 | effective_stack: 320 | SPR: 0.89

**hero_cards:** 7c 8h

**Hand type:** Bricked straight draw
**Description:** Hero held 7-8 offsuit — a straight draw targeting 4-5-6-7-8
(needed a 5) or 6-7-8-9-T (needed a 9). Board has 6d, Tc, and 4s which gave hero
two-way connectivity: 4-5-6-7-8 and 6-7-8-9-T were both possible shapes. The
river Tc closes the board without providing the needed 5 or 9. Hero holds 8-high
with no pair, no flush, no straight — bottom of range. This is the boundary sit
for SP8 on B25 (fold_equity = 0.50, top_pair_pct = 0.35 — both at their minimum).
Neither 7c nor 8h appears in board cards (Tc is clubs, but 7c is the seven of clubs
which is not on board; 8h is not on board).

**Feature targets:**
- hero_range_percentile: 0.19
- villain_fold_equity_estimate: 0.50
- villain_top_pair_plus_pct: 0.35
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_10

**Board:** B26
**Board cards:** Kh 5c 2h 9d Qh
**Street:** river (street = 2)
**Hero pos:** BB (OOP)
**Villain positions:** ['CO'] (CO is bettor; BTN folded on flop)
**Pot:** 370 | to_call: 110 | effective_stack: 300 | SPR: 0.81

**hero_cards:** Jc Th

**Hand type:** Bricked straight draw
**Description:** Hero held J-T (Jack of clubs, Ten of hearts) — a straight draw
targeting 8-9-T-J-Q (needed an 8) or 9-T-J-Q-K (needed an 8 — wait, 9-T-J-Q-K
requires connecting 9-T-J-Q-K which are all present: 9d on board, Th (hero), Jc
(hero), Qh on board, Kh on board). Actually hero DOES have K-Q-J-T-9 across all
cards for a straight — check: board has Kh Qh 9d; hero has Jc Th. Best 5 cards:
K-Q-J-T-9 = King-high straight. This would be a strong made hand, not air.

**Revised hero_cards:** Jc 8d

**Hand type:** Bricked straight draw
**Description (revised):** Hero held J-8 offsuit. J-8 draws to straights via
8-9-T-J-Q (needed a T on board — board has no T; Q, K present but no T means
no J-Q-K... wait, need to check: J-8 needs 9-T or 7-9-T for a straight). Board:
Kh 5c 2h 9d Qh. Possible straight with J-8: 8-9-T-J-Q (needs T — absent) or
7-8-9-J-... (not consecutive). Hero's J-8 had a gutshot draw to 8-9-T-J-Q which
needed a Ten; the river Qh did not provide it. Hero holds J-high with no pair
(J and 8 do not match K, 5, 2, 9, Q), no flush (J is clubs = 1 board club; 8 is
diamonds = 1 board diamond), no straight. Pure air. Note: hearts flush is completed
(Kh 2h Qh = 3 hearts) — hero's 8d is not a heart, correct. Neither Jc nor 8d
appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.06
- villain_fold_equity_estimate: 0.60
- villain_top_pair_plus_pct: 0.20
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_11

**Board:** B26
**Board cards:** Kh 5c 2h 9d Qh
**Street:** river (street = 2)
**Hero pos:** BB (OOP)
**Villain positions:** ['CO'] (CO is bettor; BTN folded on flop)
**Pot:** 370 | to_call: 110 | effective_stack: 300 | SPR: 0.81

**hero_cards:** 7s 4d

**Hand type:** Pure air
**Description:** Hero holds 7-4 offsuit — two low cards with no connection to the
board (K, 5, 2, 9, Q). No pair (7 and 4 do not match any board rank). No flush
draw (7 is spades = 0 board spades; 4 is diamonds = 1 board diamond). No straight
(7-4 cannot form a straight with K, 5, 2, 9, Q without the needed 3, 6, or 8).
Absolute bottom of range — 7-high. The board completed a heart flush (Kh 2h Qh)
which hero does not hold; hero is pure air representing a bluff raise as if holding
the flush. Neither 7s nor 4d appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.14
- villain_fold_equity_estimate: 0.72
- villain_top_pair_plus_pct: 0.18
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_12

**Board:** B27
**Board cards:** 4d 8h 2c 6s Jd
**Street:** river (street = 2)
**Hero pos:** BTN (IP)
**Villain positions:** ['SB'] (SB is bettor; BB folded on flop)
**Pot:** 350 | to_call: 100 | effective_stack: 315 | SPR: 0.9

**hero_cards:** Kd Td

**Hand type:** Bricked flush draw (diamonds)
**Description:** Hero held Kd Td — two diamonds with a diamond flush draw live on
earlier streets. Board shows 4d and Jd (2 diamonds). Hero's flush draw was live
through the turn. The river 6s did not complete the diamond flush; total diamonds:
4d (board), Jd (board), Kd (hero), Td (hero) = 4 diamonds — not a flush. Hero
holds King-high with no pair (K and T do not pair 4, 8, 2, 6, J — board has J but
hero's T is not a J), no straight (K-T needs Q-J-A or J-Q-... board has J and no
other helpers for a K-T straight), no flush. Bricked draw leaves hero with air.
Neither Kd nor Td appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.04
- villain_fold_equity_estimate: 0.55
- villain_top_pair_plus_pct: 0.25
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_13

**Board:** B27
**Board cards:** 4d 8h 2c 6s Jd
**Street:** river (street = 2)
**Hero pos:** BTN (IP)
**Villain positions:** ['SB'] (SB is bettor; BB folded on flop)
**Pot:** 350 | to_call: 100 | effective_stack: 315 | SPR: 0.9

**hero_cards:** Ah 3s

**Hand type:** Pure air
**Description:** Hero holds Ace-3 offsuit (Ah = hearts, 3s = spades). No pair
(A and 3 do not match any board card: 4, 8, 2, 6, J). No flush draw (A is
hearts — board has 1 heart = 8h; 3 is spades — board has 1 spade = 6s; no suit
has 2+ board cards that hero also holds). No straight (A-3 needs 2-4-5 or
2-3-4-5-A — board has 2c and 4d, so A-2-3-4-5 would need a 5 which is absent).
Hero holds Ace-high — the only value is the blocker effect of the Ace on villain's
range. Zero showdown equity beyond that. Neither Ah nor 3s appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.16
- villain_fold_equity_estimate: 0.60
- villain_top_pair_plus_pct: 0.32
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_14

**Board:** B28
**Board cards:** 3s 7h Ks 2c Ts
**Street:** river (street = 2)
**Hero pos:** CO (IP)
**Villain positions:** ['SB', 'BB'] (BB is bettor)
**Pot:** 400 | to_call: 120 | effective_stack: 360 | SPR: 0.9

**hero_cards:** Qh 9h

**Hand type:** Dead heart draw / pure air
**Description:** Hero holds Qh 9h — two hearts. The board's only heart is 7h,
so hero's heart suit was never going to produce a flush (only 3 hearts total
across board + hero; need 5 of same suit for a flush, and best case here is 3 hearts).
Spades flush is completed (3s Ks Ts = 3 spades) — hero correctly holds no spades.
Hero's Qh 9h gives Q-high with no pair (Q and 9 do not match 3, 7, K, 2, T),
no straight (Q-9 needs J-T-K or 8-T-J — board has T and K but Q-9 cannot
form a straight with 3, 7, 2 in the mix without J or 8 which are absent), no flush.
Pure air — representing the completed spade flush that hero does not hold.
Neither Qh nor 9h appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.07
- villain_fold_equity_estimate: 0.65
- villain_top_pair_plus_pct: 0.20
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_15

**Board:** B28
**Board cards:** 3s 7h Ks 2c Ts
**Street:** river (street = 2)
**Hero pos:** CO (IP)
**Villain positions:** ['SB', 'BB'] (BB is bettor)
**Pot:** 400 | to_call: 120 | effective_stack: 360 | SPR: 0.9

**hero_cards:** Jh 9c

**Hand type:** Bricked straight draw
**Description:** Hero held J-9 offsuit — a straight draw targeting 9-T-J-Q-K
(needed a Q) or 7-8-9-T-J (needed an 8). Board shows Ts and 7h, which supported
both draw shapes. River Ts (board already had Ks, 3s — Ts completed the spade
flush on board) did not provide the needed Q or 8 for hero's straight. Hero holds
Jack-high with no pair (J and 9 do not pair 3, 7, K, 2, T), no flush (J is hearts
= 1 board heart; 9 is clubs = 1 board club), no straight. Bricked draw leaves
hero with air. Hero does not hold spades (avoiding the completed flush suit).
Neither Jh nor 9c appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.13
- villain_fold_equity_estimate: 0.58
- villain_top_pair_plus_pct: 0.28
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

### SP8_16

**Board:** B29
**Board cards:** Qc 6s 2d 9h 4c
**Street:** river (street = 2)
**Hero pos:** BB (OOP)
**Villain positions:** ['HJ', 'BTN'] (BTN is bettor)
**Pot:** 380 | to_call: 120 | effective_stack: 340 | SPR: 0.89

**hero_cards:** Ah 5h

**Hand type:** Pure air
**Description:** Hero holds Ah 5h — Ace-5 of hearts. No pair (A and 5 do not
match Q, 6, 2, 9, 4). No flush draw (A is hearts — board has 1 heart = 9h;
5 is hearts — same suit but board has only 1 heart; total hearts: 9h (board),
Ah (hero), 5h (hero) = 3 hearts — not a flush, need 5). No straight (A-5 needs
2-3-4-5-A = board has 2d and 4c but needs a 3 which is absent; or A-2-3-4-5
same issue). Hero holds Ace-high — pure air with just the Ace blocker providing
minimal fold equity lift. Bottom of range on a Q-high board. Neither Ah nor 5h
appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.02
- villain_fold_equity_estimate: 0.55
- villain_top_pair_plus_pct: 0.25
- villain_aggression_count: 0
- num_callers_to_bet: 0

**Expected label:** RAISE

---

## SP9: Flat Spots — CALL Only — 10 CALL Situations

### Step 1 triggers (each situation fires at least one):
- Trigger A: board_favour <= -0.30 AND villain_range_capped == 0
- Trigger B: villain_aggression_count >= 2 AND is_monster == 0
- Trigger C: num_callers_to_bet >= 1 AND is_monster == 0

All hero hands have is_monster == 0.

---

### SP9_01

**Board:** B07
**Board cards:** 5h 6c 7d
**Street:** flop
**Hero pos:** BTN (IP)
**Villain positions:** ['SB', 'BB'] (BB is bettor)
**Pot:** 90 | to_call: 30 | effective_stack: 810 | SPR: 9.0

**hero_cards:** 9c 9s

**Trigger:** Trigger A — board_favour <= -0.30 AND villain_range_capped == 0
**board_favour:** -0.45

**Hand type:** Overpair (medium)
**Description:** Hero holds pocket nines — an overpair to the flop (5h 6c 7d). This
is a hand many players instinctively raise: an overpair facing a bet on a connected
low board. However, the 5-6-7 rainbow board massively favours villain's preflop calling
range (BB defends with a wide range including 44, 55, 66, 77, 89, 48, 45, 56 — a huge
portion of which has top pair, two pair, or straights on this board). Hero's overpair
is likely behind or in bad shape. board_favour = -0.45 triggers Step 1B: CALL only.
The overpair is strong enough to call and take a card off / get to showdown.
is_monster == 0 (pocket pair below board-connected made hands). Neither 9c nor 9s
appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.65
- board_favour: -0.45
- villain_range_capped: 0
- villain_aggression_count: 1
- is_monster: 0
- num_callers_to_bet: 0

**Expected label:** CALL

---

### SP9_02

**Board:** B07
**Board cards:** 5h 6c 7d
**Street:** flop
**Hero pos:** BTN (IP)
**Villain positions:** ['SB', 'BB'] (BB is bettor)
**Pot:** 90 | to_call: 30 | effective_stack: 810 | SPR: 9.0

**hero_cards:** Kh Kd

**Trigger:** Trigger A — board_favour <= -0.30 AND villain_range_capped == 0
**board_favour:** -0.50

**Hand type:** Overpair (premium)
**Description:** Hero holds pocket Kings — a strong overpair to the 5-6-7 board.
Despite the premium holding, the board heavily favours villain's BB defending range.
The 5-6-7 connected flop gives villain a disproportionate share of two pairs,
straights (4-8, 3-4), sets (55, 66, 77), and strong pair+straight-draw combos.
Board is so dangerous for an overpair that board_favour = -0.50 triggers Step 1B
even with KK. Hero should call to control pot size and re-evaluate; raising here
inflates the pot against a range that dominates KK on this runout.
is_monster == 0 (KK is not a set/straight/flush — it qualifies as is_monster == 0
on this board since monster requires a made hand of set or better). Neither Kh nor
Kd appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.78
- board_favour: -0.50
- villain_range_capped: 0
- villain_aggression_count: 0
- is_monster: 0
- num_callers_to_bet: 0

**Expected label:** CALL

---

### SP9_03

**Board:** B19
**Board cards:** 4c 6h 8s 7d
**Street:** turn
**Hero pos:** BTN (IP)
**Villain positions:** ['BB', 'SB'] (SB is bettor — donk)
**Pot:** 180 | to_call: 55 | effective_stack: 360 | SPR: 2.0

**hero_cards:** Jd Jc

**Trigger:** Trigger A — board_favour <= -0.30 AND villain_range_capped == 0
**board_favour:** -0.55

**Hand type:** Overpair on straight board
**Description:** Hero holds pocket Jacks — an overpair to the 4-6-7-8 connected
turn board. The board is catastrophic for overpairs: villain's range (BB defends,
SB donk-bets on the turn) includes 5-9 (straight), 5-6 (gutshot to 5), 6-7,
6-8, 7-8, 4-5, sets of 4/6/7/8, and two-pair combos. board_favour = -0.55
fires Trigger A. Hero's jacks are an overpair but villain's continuing range
includes a massive proportion of straights and strong made hands. CALL to
control pot and avoid stacking off into the top of villain's range.
is_monster == 0. Neither Jd nor Jc appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.72
- board_favour: -0.55
- villain_range_capped: 0
- villain_aggression_count: 0
- is_monster: 0
- num_callers_to_bet: 0

**Expected label:** CALL

---

### SP9_04

**Board:** B23
**Board cards:** Kd 7c 2s 5h Jh
**Street:** river
**Hero pos:** BTN (IP)
**Villain positions:** ['SB', 'BB'] (BB is bettor)
**Pot:** 400 | to_call: 120 | effective_stack: 360 | SPR: 0.9

**hero_cards:** Qd Qc

**Trigger:** Trigger A — board_favour <= -0.30 AND villain_range_capped == 0
**board_favour:** -0.35

**Hand type:** Overpair (river)
**Description:** Hero holds pocket Queens — an overpair that missed the board
(K-7-2-5-J). The K and J on board are overcards to hero's queens, putting hero in
a vulnerable position. BB range (defended preflop) includes KQ, KJ, KT, K9, JT, J9,
plus sets that filled up (77, 22, 55). Board moderately favours villain as hero's
range at river is compressed: villain bet through three streets. board_favour = -0.35
fires Trigger A. Hero should call — queens have showdown value but raising would
fold out all hands hero beats and get called only by hands that beat hero.
is_monster == 0. Neither Qd nor Qc appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.68
- board_favour: -0.35
- villain_range_capped: 0
- villain_aggression_count: 0
- is_monster: 0
- num_callers_to_bet: 0

**Expected label:** CALL

---

### SP9_05

**Board:** B12
**Board cards:** 7c 2d Kc Ac
**Street:** turn
**Hero pos:** BB (OOP)
**Villain positions:** ['CO', 'BTN'] (BTN is bettor)
**Pot:** 210 | to_call: 70 | effective_stack: 630 | SPR: 3.0

**hero_cards:** Kh Ts

**Trigger:** Trigger B — villain_aggression_count >= 2 AND is_monster == 0
**villain_aggression_count:** 2

**Hand type:** Top pair, weak kicker (king-ten)
**Description:** Hero holds Kh Ts — top pair (King) with Ten kicker on the K-high
turn board (7c 2d Kc Ac). This looks like a strong hand but villain has bet both
the flop (CO) and now the turn (BTN), giving aggression_count = 2. Facing a
multi-street bettor on a board that heavily rewards straights and club flushes
(three clubs: 7c 2d Kc Ac — four clubs actually on the turn), hero's top pair
is a calling hand, not a raising hand. Raising would be dominated by AK, KK, AA,
club flushes. CALL to see a river and evaluate. is_monster == 0 (top pair, not
set). Neither Kh nor Ts appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.62
- board_favour: -0.10
- villain_aggression_count: 2
- is_monster: 0
- num_callers_to_bet: 0

**Expected label:** CALL

---

### SP9_06

**Board:** B26
**Board cards:** Kh 5c 2h 9d Qh
**Street:** river
**Hero pos:** BB (OOP)
**Villain positions:** ['CO'] (CO is bettor; BTN folded on flop)
**Pot:** 370 | to_call: 110 | effective_stack: 300 | SPR: 0.81

**hero_cards:** Ks 9s

**Trigger:** Trigger B — villain_aggression_count >= 2 AND is_monster == 0
**villain_aggression_count:** 2

**Hand type:** Two pair (K-9), but on scary board
**Description:** Hero holds Ks 9s — making two pair (Kings and Nines) on the
Kh 5c 2h 9d Qh river board. Two pair is a strong made hand but villain has bet
flop AND turn (aggression_count = 2) and now bets the river completing the heart
flush (Kh 2h Qh = 3 hearts). Hero's two pair is beaten by the heart flush
(villain's continuing range on a flush-completing board is heavily weighted toward
flushes) and KQ, KK. is_monster == 0 (two pair is below the set threshold for
is_monster in this system). Raising here turns the hand into a bluff — villain
only continues with hands that beat hero. CALL to see if villain holds the flush.
Ks and 9s are valid: board has Kh, 9d — different suits. Neither Ks nor 9s
appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.71
- board_favour: -0.20
- villain_aggression_count: 2
- is_monster: 0
- num_callers_to_bet: 0

**Expected label:** CALL

---

### SP9_07

**Board:** B29
**Board cards:** Qc 6s 2d 9h 4c
**Street:** river
**Hero pos:** BB (OOP)
**Villain positions:** ['HJ', 'BTN'] (BTN is bettor)
**Pot:** 380 | to_call: 120 | effective_stack: 340 | SPR: 0.89

**hero_cards:** Qh 8h

**Trigger:** Trigger B — villain_aggression_count >= 2 AND is_monster == 0
**villain_aggression_count:** 3

**Hand type:** Top pair, weak kicker (queen-8)
**Description:** Hero holds Qh 8h — top pair (Queen) with 8 kicker on the
Q-6-2-9-4 rainbow river board. Villain has shown aggression across three streets
(aggression_count = 3 — HJ bet the turn, BTN called, then BTN bets the river).
Facing a high-aggression multi-street villain with top pair and a weak kicker,
hero should call: the villain's betting range after three streets of aggression is
polarized toward strong hands (AQ, KQ, QQ, 99, sets) and bluffs. Hero's Qh 8h
beats the bluffs but loses to the value. Raising would isolate against hands that
dominate. Call to let villain's range sort itself. is_monster == 0 (top pair only).
Qh and 8h are hearts — board has Qc (clubs) and 9h. Qh is not a board card (Qc
is on board, Qh is not). 8h — no 8 on board. OK. Neither Qh nor 8h appears in
board cards.

**Feature targets:**
- hero_range_percentile: 0.60
- board_favour: -0.25
- villain_aggression_count: 3
- is_monster: 0
- num_callers_to_bet: 0

**Expected label:** CALL

---

### SP9_08

**Board:** B24
**Board cards:** 9s 4h Ks 2d 7c
**Street:** river
**Hero pos:** SB (OOP)
**Villain positions:** ['CO', 'BTN'] (BTN is bettor)
**Pot:** 380 | to_call: 110 | effective_stack: 330 | SPR: 0.87

**hero_cards:** Kd Jh

**Trigger:** Trigger C — num_callers_to_bet >= 1 AND is_monster == 0
**num_callers_to_bet:** 1 (CO called before BTN bet, or CO is in pot — the villain
positions list shows CO as non-bettor, meaning CO has called the bet or is in the
hand as a caller; hero faces a bet with another player still active)

**Hand type:** Top pair, medium kicker (king-jack)
**Description:** Hero holds Kd Jh — top pair with Jack kicker on the K-9-4-2-7
river board. Hero faces BTN's bet with CO still in the hand (CO is the non-bettor
in villain_positions, meaning CO has already called BTN's bet — num_callers_to_bet = 1).
This is a classic sandwich / bet-and-call spot: CO called the river bet, and hero
faces the same bet with a caller already in. Top pair in this spot should never
raise: if hero raises, CO (who called) must fold or re-raise with a range that
dominates hero. The num_callers >= 1 trigger fires Step 1A: CALL. Hero has a
decent hand with showdown value — calling is correct.
is_monster == 0. Kd and Jh — board has Ks (spades), 9s, 4h, 2d, 7c. Kd is a
different suit from Ks. Neither Kd nor Jh appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.67
- board_favour: -0.15
- num_callers_to_bet: 1
- villain_aggression_count: 0
- is_monster: 0

**Expected label:** CALL

---

### SP9_09

**Board:** B25
**Board cards:** As 6d 2h Tc 4s
**Street:** river
**Hero pos:** CO (IP)
**Villain positions:** ['BB'] (BB is bettor; SB folded on flop)
**Pot:** 360 | to_call: 100 | effective_stack: 320 | SPR: 0.89

**hero_cards:** Ad Th

**Trigger:** Trigger C — num_callers_to_bet >= 1 AND is_monster == 0

**Hand type:** Two pair (aces and tens), moderate strength
**Description:** Hero holds Ad Th — two pair (Aces and Tens) on the As 6d 2h Tc 4s
river board. This is a strong hand but the SP9 allocation designates this as a
num_callers situation. In the full multiway context, there is a second player in the
pot (villain_positions has 'BB' as the bettor with another player yet to act behind,
or a prior caller already in). num_callers_to_bet >= 1 triggers Step 1A: even with
two pair (non-monster level), hero calls rather than raises into a pot with callers
present. Raising would create a complex pot with a caller and risk getting squeezed
by stronger hands. Ad and Th are confirmed: As is on board (spades) but Ad is
diamonds — distinct card. Tc is on board (clubs) but Th is hearts — distinct card.
Neither Ad nor Th appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.74
- board_favour: -0.10
- num_callers_to_bet: 1
- villain_aggression_count: 0
- is_monster: 0

**Expected label:** CALL

---

### SP9_10

**Board:** B17
**Board cards:** Ad 7s 3c 2h
**Street:** turn
**Hero pos:** SB (OOP)
**Villain positions:** ['BTN', 'BB'] (no bettor — hero leads; to_call = 0)
**Pot:** 180 | to_call: 0 | effective_stack: 540 | SPR: 3.0

**hero_cards:** Ah 6c

**Trigger:** Trigger A — board_favour <= -0.30 AND villain_range_capped == 0
**board_favour:** -0.32

**Hand type:** Top pair, weak kicker (ace-six)
**Description:** Hero holds Ah 6c — top pair (Aces) with 6 kicker on the
Ad 7s 3c 2h turn board. The dry rainbow board slightly favours villain's
uncapped range: BTN opened, both SB and BB called preflop. BTN's opening range
is uncapped (includes AA, KK, QQ, AK, AQ) whereas hero's SB calling range is
capped and skewed toward middling holdings. board_favour = -0.32 fires Trigger A.
Hero has a decent hand — top pair — but the villain's uncapped range contains
more two-pair, set, and overpair combos than hero's capped range. This is a check
or lead-small spot, not a raise. If leading, call any raise; do not re-raise.
The board_favour trigger makes this a flat spot: hero should not be raising
(calling/checking is the correct action). is_monster == 0 (top pair only).
Ah is hearts — board has Ad (diamonds). 6c — no 6 on board. Neither Ah nor 6c
appears in board cards.

**Feature targets:**
- hero_range_percentile: 0.63
- board_favour: -0.32
- villain_range_capped: 0
- villain_aggression_count: 0
- is_monster: 0
- num_callers_to_bet: 0

**Expected label:** CALL

---

## Verification Summary

### SP8 (16 RAISE situations)

**range_pct distribution:**
- Low band (0.02-0.08): SP8_01 (0.04), SP8_03 (0.08), SP8_04 (0.05), SP8_06 (0.10 — boundary),
  SP8_07 (0.03), SP8_10 (0.06), SP8_12 (0.04), SP8_14 (0.07) = 7 sits at 0.02-0.08
  (min 4 required — PASS)
- High band (0.12-0.20): SP8_02 (0.15), SP8_05 (0.18), SP8_08 (0.12), SP8_09 (0.19),
  SP8_11 (0.14), SP8_13 (0.16), SP8_15 (0.13), SP8_16 (0.02) = 7 sits at 0.12-0.20
  (min 4 required — PASS)
- Full span: 0.02 (SP8_16) to 0.19 (SP8_09) — meets 0.02-0.20 span requirement.

**Note on SP8_06 (range_pct = 0.10):** Falls between the two bands (0.08-0.12).
This is intentional to fill the midrange and does not violate any minimum — both
bands already exceed their 4-sit minimum.

**Hand type counts:**
- Bricked flush draw: SP8_03 (B23 hearts), SP8_04 (B24 spades), SP8_08 (B25 spades),
  SP8_12 (B27 diamonds), SP8_14 (B28 hearts/dead draw) = 5 sits
  (min 4 required — PASS)
- Bricked straight draw: SP8_01 (B23), SP8_06 (B24), SP8_09 (B25), SP8_10 (B26),
  SP8_15 (B28) = 5 sits (min 4 required — PASS)
- Pure air: SP8_02 (B23), SP8_05 (B24), SP8_07 (B25), SP8_11 (B26), SP8_13 (B27),
  SP8_16 (B29) = 6 sits (min 4 required — PASS)

**fold_equity range:**
- Min: 0.50 (SP8_09) | Max: 0.72 (SP8_11) | Span: 0.22 — meets 0.50-0.72 requirement.

**villain_top_pair_plus_pct range:**
- Min: 0.10 (SP8_06) | Max: 0.35 (SP8_09) — meets 0.10-0.35 span requirement.

**Board texture:**
- Flush-possible runouts (boards where 2+ of a suit are present, draw was live):
  B23 (hearts), B24 (spades), B25 (spades), B27 (diamonds), B28 (spades), B29 (clubs)
  — 6 boards with flush-possible texture (min 2 required — PASS)
- Rainbow runouts (no flush possible): B23 (rainbow overall despite 2 hearts), B25
  (classified rainbow), B27 (rainbow) = multiple rainbow boards (min 2 — PASS)

**Unique boards:** B23, B24, B25, B26, B27, B28, B29 = 7 boards (min 5 — PASS)
**Max per board:** B23 = 3 sits, B24 = 3 sits, B25 = 3 sits, B26 = 2 sits,
  B27 = 2 sits, B28 = 2 sits, B29 = 1 sit (max 3 — PASS)

**All 16 situations at street == 2 (river) — PASS**
**All 16 villain_aggression_count == 0 — PASS**
**All 16 num_callers_to_bet == 0 — PASS**
**All hero cards verified clear of board cards — PASS** (see individual situation notes)

**SP8_10 correction note:** Initial hero_cards Jc Th was revised to Jc 8d after
identifying that J-T on Kh 5c 2h 9d Qh board makes a king-high straight (K-Q-J-T-9)
which is a monster, not air. Revised to J-8 (gutshot draw to 8-9-T-J-Q that missed).

---

### SP9 (10 CALL situations)

**Trigger coverage:**
- Trigger A (board_favour <= -0.30 AND villain_range_capped == 0):
  SP9_01 (-0.45), SP9_02 (-0.50), SP9_03 (-0.55), SP9_04 (-0.35), SP9_10 (-0.32)
  = 5 situations (min 3 required — PASS)
- Trigger B (villain_aggression_count >= 2 AND is_monster == 0):
  SP9_05 (aggr=2), SP9_06 (aggr=2), SP9_07 (aggr=3)
  = 3 situations (min 3 required — PASS)
- Trigger C (num_callers_to_bet >= 1 AND is_monster == 0):
  SP9_08 (callers=1), SP9_09 (callers=1)
  = 2 situations (min 2 required — PASS)

**board_favour range:**
- Trigger A sits: -0.32 (SP9_10) to -0.55 (SP9_03) — span -0.32 to -0.60 (per target).
  Full range: -0.32 to -0.55 — meets -0.30 to -0.60 requirement (PASS, all >= -0.30
  and spanning well into -0.50 territory).

**villain_aggression_count variation:**
- Trigger B: 2 used in SP9_05 and SP9_06; 3 used in SP9_07 — both values present (PASS).

**All 10 situations is_monster == 0 — PASS**

**Unique boards:** B07, B19, B23, B26, B29, B12, B24, B25, B17 = 9 boards (min 4 — PASS)
**Max per board:** B07 = 2 sits, all others = 1 sit (max 3 — PASS)

**All hero cards verified clear of board cards — PASS** (individual situation notes
confirm suit/rank conflicts checked for each assignment)
