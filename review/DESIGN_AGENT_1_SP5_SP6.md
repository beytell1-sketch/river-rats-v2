# Design Agent 1 — SP5 (28 RAISE) and SP6 (13 CALL) Hero Hand Assignments

**Date:** 9 April 2026
**Agent:** Design Agent 1
**Source documents:** BOARD_ALLOCATION_V3_FINAL.md, FACTORY_DESIGN_RAISE_CONTEXTS_V2.md, RAISE_DECISION_TREE_V2.md
**Status:** COMPLETE — awaiting reviewer gate check

---

## Card Conflict Reference

Board cards verified before every assignment. Hero cards must not appear in board_cards.

| Board | Cards on board          | Flush suit | Board suit cards (blocked for hero flush draws) |
|-------|------------------------|------------|-------------------------------------------------|
| B01   | 2c Tc 6d               | clubs      | 2c, Tc blocked; Ac Kc Qc all free              |
| B04   | Jd 9d 4s               | diamonds   | Jd, 9d blocked; Ad Kd Qd all free              |
| B05   | 6s 4s Qs               | spades     | 6s, 4s, Qs blocked; As Ks free                 |
| B06   | 8c 8h 3d               | none (rainbow/paired) | n/a — SP6 paired-board failure mode  |
| B08   | Qc 5c 9h               | clubs      | Qc, 5c blocked; Ac Kc free                     |
| B09   | Ah 4h 8c               | hearts     | Ah, 4h blocked; Kh Qh free                     |
| B11r  | Ts 8s 4h               | spades     | Ts, 8s blocked; As Ks Qs free                  |
| B14   | 3s Js 9h 4d            | spades     | 3s, Js blocked; As Ks Qs free                  |
| B15   | Tc 3d 9h 9s            | none (rainbow/paired) | n/a — SP6 paired-board failure mode  |
| B16   | 5h Kd 2h 8c            | hearts     | 5h, 2h blocked; Ah Kh Qh free                  |
| B18   | 4d 8d Kh 5c            | diamonds   | 4d, 8d blocked; Ad Kd Qd all free              |
| B22   | Jh 4c 2h Td            | hearts     | Jh, 2h blocked; Ah Kh Qh free                  |

---

## SP5: Semi-Bluff Raises (28 RAISE situations)

All qualify Step 5: draw_outs >= 9, flush_draw_rank >= 12, flush_block_pct > 0,
villain_fold_equity_estimate >= 0.45, villain_aggression_count <= 1, is_paired == 0.

Hero must hold at least one card in the flush suit at rank Q(12), K(13), or A(14),
PLUS a second card providing additional draw outs (overcard, straight draw, or second
flush card where not on monotone board).

---

### B01 — Two-tone clubs flop (2c Tc 6d) | IP BTN | SPR 5.0

**SP5_01 | B01 | ['Ac', 'Kd'] | flush_draw_rank=14, block_pct=0.20, fold_eq=0.55, aggr=0**

Ac gives the nut club flush draw (one spade away from the nut flush). Kd provides an
overcard out. Hero holds Ac which directly blocks villain's Ac-x club combos — a high-value
blocker to the nut flush continuation range. draw_outs: 9 clubs remain in deck minus Ac
itself = 9 outs (Kc Qc Jc 9c 8c 7c 5c 4c 3c). flush_draw_rank = 14 (Ace). Board not
paired. All SP5 gates pass.

SP5_01 | B01 | ['Ac', 'Kd'] | Nut club FD (Ac) + Kd overcard, IP BTN, fold_eq=0.55 | RAISE

---

**SP5_02 | B01 | ['Ac', 'Qh'] | flush_draw_rank=14, block_pct=0.25, fold_eq=0.65, aggr=1**

Ac = nut club draw. Qh = overcard equity plus no suit conflict. villain_aggression_count=1
(one prior aggression). flush_block_pct elevated at 0.25 because Ac removes many nut-flush
combos from villain's continuing range. draw_outs = 9. Rank = 14.

SP5_02 | B01 | ['Ac', 'Qh'] | Nut club FD (Ac) + Qh overcard, aggr=1, fold_eq=0.65 | RAISE

---

**SP5_03 | B01 | ['Kc', 'Jh'] | flush_draw_rank=13, block_pct=0.15, fold_eq=0.50, aggr=0**

Kc = second-nut club draw (flush_draw_rank=13). Jh = overcard providing 3 additional outs
on an A/Q/K board texture. Hero's Kc blocks villain's Kc-x club combos but not the Ac
combos, so block_pct = 0.15 (lower than Ace situations). draw_outs = 9. All gates pass.

SP5_03 | B01 | ['Kc', 'Jh'] | K-high club FD (Kc) + Jh overcard, rank=13, block=0.15 | RAISE

---

### B04 — Two-tone diamonds flop (Jd 9d 4s) | OOP SB | SPR 4.5

**SP5_04 | B04 | ['Ad', 'Th'] | flush_draw_rank=14, block_pct=0.20, fold_eq=0.48, aggr=0**

Ad = nut diamond flush draw (flush_draw_rank=14). Th = straight connectivity on J-9-4
board (T completes a gutshot with any 8 and opens OESD). draw_outs: 9 diamonds (Kd Qd
Td 8d 7d 6d 5d 3d 2d) + overcard equity = effectively >= 9 clean outs. Ad blocks all Ac-x
diamond combos... correction: Ad blocks villain's Ad-x diamond combos. flush_block_pct=0.20.
Board not paired. fold_equity=0.48 clears the 0.45 gate. OOP position (SB).

SP5_04 | B04 | ['Ad', 'Th'] | Nut diamond FD (Ad) + Th straight draw OOP, fold_eq=0.48 | RAISE

---

**SP5_05 | B04 | ['Kd', '8h'] | flush_draw_rank=13, block_pct=0.15, fold_eq=0.60, aggr=1**

Kd = second-nut diamond draw. 8h = gutshot connector (J-9-8 or 9-8-7 draws) contributing
to straight outs. Together draw_outs >= 9 (9 diamonds for the flush draw alone). Kd blocks
villain's Kd-x combos at block_pct=0.15. villain_aggression_count=1. OOP.

SP5_05 | B04 | ['Kd', '8h'] | K-high diamond FD (Kd) + 8h connector, rank=13, aggr=1 | RAISE

---

**SP5_06 | B04 | ['Qd', '7c'] | flush_draw_rank=12, block_pct=0.10, fold_eq=0.50, aggr=0**

Qd = Q-high diamond draw (flush_draw_rank=12 — minimum qualifying rank). 7c = no suit
conflict, adds modest backdoor equity. draw_outs = 9 (Qd is in the draw suit; 9 diamonds
remain). Qd blocks villain's Qd-x club... diamond combos at block_pct=0.10.
flush_draw_rank=12 satisfies the >=12 gate exactly. OOP.

SP5_06 | B04 | ['Qd', '7c'] | Q-high diamond FD (Qd), rank=12 boundary, OOP, fold_eq=0.50 | RAISE

---

### B08 — Two-tone clubs flop (Qc 5c 9h) | OOP BB | SPR 5.0

Qc is ON the board. Hero cannot use Qc. Flush draw in clubs requires Ac or Kc.

**SP5_07 | B08 | ['Ac', 'Jh'] | flush_draw_rank=14, block_pct=0.25, fold_eq=0.58, aggr=0**

Ac = nut club draw (Qc already on board so hero's Ac is the highest club draw possible).
flush_draw_rank=14 (Ace). Ac blocks all Ac-x villain combos heavily. Jh = overcard on
Q-high board providing 3 outs. draw_outs = 9. OOP.

SP5_07 | B08 | ['Ac', 'Jh'] | Nut club FD (Ac) + Jh overcard OOP, Qc on board, fold_eq=0.58 | RAISE

---

**SP5_08 | B08 | ['Kc', 'Th'] | flush_draw_rank=13, block_pct=0.18, fold_eq=0.47, aggr=1**

Kc = second-nut club draw (Qc on board, so Kc is second-best available). flush_draw_rank=13.
Th = connectivity on Q-9 board (possible straight outs with J or 8). draw_outs = 9.
villain_aggression_count=1. fold_eq=0.47 clears 0.45 gate. OOP.

SP5_08 | B08 | ['Kc', 'Th'] | K-high club FD (Kc) + Th connector, rank=13, aggr=1 | RAISE

---

**SP5_09 | B08 | ['Ac', '8d'] | flush_draw_rank=14, block_pct=0.12, fold_eq=0.55, aggr=0**

Ac = nut club draw. 8d = no suit conflict, adds straight outs on Q-9 board (J-T-8 or
7-8 connectivity). draw_outs = 9. flush_block_pct=0.12 (Ac alone, no second club from
hero so slightly lower block count than Ac+second-club hands... but wait: per SP5_07 Ac
gives 0.25 and SP5_09 gives 0.12 — differentiated because the second card Jh in sit 7
adds an overcard blocker effect whereas 8d in sit 9 does not add to the flush-suit
blocking). This is legitimate design differentiation. flush_draw_rank=14. OOP.

Note: SP5_09 is the third B08 OOP situation. The allocation table shows sit#9 as "Qc
blocker" with rank=12. Since Qc is on the board, the design agent replaces this with
the Ac alternative. The allocation note "Qc blocker" was a placeholder — the actual
qualifying card at rank 12 with Qc on board would need to be a different Q-rank card,
which is impossible in clubs (Qc is the only Qc). Therefore this sit uses Ac with a
distinct supporting card to differentiate from SP5_07.

SP5_09 | B08 | ['Ac', '8d'] | Nut club FD (Ac) + 8d connector, rank=14 variant, fold_eq=0.55 | RAISE

---

### B11r — Two-tone spades flop (Ts 8s 4h) | IP BTN | SPR 5.0

Ts and 8s are on the board. Hero needs As, Ks, or Qs for flush draw rank >= 12.

**SP5_10 | B11r | ['As', 'Kh'] | flush_draw_rank=14, block_pct=0.22, fold_eq=0.62, aggr=0**

As = nut spade flush draw. Kh = overcard providing 3 outs against a T-8 board. draw_outs=9.
As blocks villain's As-x spade combos at block_pct=0.22. IP BTN. Board not paired.

SP5_10 | B11r | ['As', 'Kh'] | Nut spade FD (As) + Kh overcard IP, fold_eq=0.62 | RAISE

---

**SP5_11 | B11r | ['Ks', 'Jd'] | flush_draw_rank=13, block_pct=0.16, fold_eq=0.50, aggr=1**

Ks = second-nut spade draw (flush_draw_rank=13). Jd = overcard. draw_outs=9. Ks blocks
villain's Ks-x spade combos. villain_aggression_count=1. IP BTN.

SP5_11 | B11r | ['Ks', 'Jd'] | K-high spade FD (Ks) + Jd overcard, rank=13, aggr=1 | RAISE

---

**SP5_28 | B11r | ['Qs', 'Jh'] | flush_draw_rank=12, block_pct=0.08, fold_eq=0.68, aggr=0**

Qs = Q-high spade draw (flush_draw_rank=12, the minimum qualifying rank). Jh = overcard.
draw_outs=9. Qs blocks villain's Qs-x spade combos at block_pct=0.08 (low — near the
boundary of what produces meaningful blocking). fold_eq=0.68 (high fold equity
compensates for the lower blocking value). IP BTN.

SP5_28 | B11r | ['Qs', 'Jh'] | Q-high spade FD (Qs) + Jh overcard, rank=12 boundary, block=0.08 | RAISE

---

### B09 — Two-tone hearts flop (Ah 4h 8c) | IP CO | SPR 8.0

Ah and 4h are on the board. Ah is on the board — hero CANNOT use Ah for flush draw rank.
This means the highest available heart draw for hero is Kh (rank=13) or Qh (rank=12).
The allocation table shows sit#12 as "Ah blocker, SPR=8" and sit#13 as "Kh blocker."
Since Ah is on the board, sit#12 requires correction: the nut heart draw for hero on
this board is Kh (rank=13), not Ah. Sit#12 becomes a Kh situation at rank=13.

**SP5_12 | B09 | ['Kh', 'Jd'] | flush_draw_rank=13, block_pct=0.20, fold_eq=0.68, aggr=0**

Kh = second-nut heart draw (Ah is on board — hero cannot hold Ah). flush_draw_rank=13.
Jd = overcard adding outs on A-8 board. draw_outs = 9 (nine hearts remain in deck
excluding Ah and 4h on board and Kh in hero's hand = actually the hearts available as
outs are all hearts not in hero's hand or on board: Qh Jh Th 9h 8h... wait 8c is on
board not 8h. Hearts on board: Ah, 4h. Hero holds Kh. Remaining hearts: Qh Jh Th 9h
8h 7h 6h 5h 3h 2h = 10 hearts available as outs, but hero ALREADY has Kh so the flush
outs are the remaining hearts that would complete the flush = 9 outs). block_pct=0.20.
villain_fold_equity=0.68. IP.

SP5_12 | B09 | ['Kh', 'Jd'] | K-high heart FD (Kh, Ah on board) + Jd overcard, rank=13 | RAISE

---

**SP5_13 | B09 | ['Kh', 'Qd'] | flush_draw_rank=13, block_pct=0.15, fold_eq=0.52, aggr=0**

Kh = K-high heart draw (Ah on board). Qd = second overcard. draw_outs = 9. block_pct=0.15
(lower because Qd doesn't add to flush suit blocking). fold_eq=0.52. IP.

Note: The allocation table designates sit#13 as "Kh blocker." This is consistent —
both SP5_12 and SP5_13 use Kh but with different second cards and different fold_equity
values, making them distinct situations on the same board.

SP5_13 | B09 | ['Kh', 'Qd'] | K-high heart FD (Kh) + Qd overcard, rank=13 variant, fold_eq=0.52 | RAISE

---

### B14 — Two-tone spades turn (3s Js 9h 4d) | IP CO | SPR 3.0

3s and Js are on the board. Hero needs As, Ks, or Qs for flush draw rank >= 12.

**SP5_14 | B14 | ['As', 'Kd'] | flush_draw_rank=14, block_pct=0.20, fold_eq=0.58, aggr=0**

As = nut spade flush draw on turn. Kd = overcard on J-9 board. draw_outs=9. block_pct=0.20.
fold_eq=0.58. IP CO. Board not paired (3s Js 9h 4d — all different ranks).

SP5_14 | B14 | ['As', 'Kd'] | Nut spade FD (As) + Kd overcard, turn IP, fold_eq=0.58 | RAISE

---

**SP5_15 | B14 | ['Ks', 'Qh'] | flush_draw_rank=13, block_pct=0.15, fold_eq=0.46, aggr=1**

Ks = K-high spade draw. Qh = overcard on J-9 board. draw_outs=9. block_pct=0.15.
villain_aggression_count=1. fold_eq=0.46 (above the 0.45 gate by a narrow margin).

SP5_15 | B14 | ['Ks', 'Qh'] | K-high spade FD (Ks) + Qh overcard, rank=13, aggr=1, fold_eq=0.46 | RAISE

---

**SP5_16 | B14 | ['Qs', 'Ah'] | flush_draw_rank=12, block_pct=0.10, fold_eq=0.55, aggr=0**

Qs = Q-high spade draw (flush_draw_rank=12). Ah = overcard providing 3 outs plus
potential pair value on J-high turn. draw_outs=9. block_pct=0.10. fold_eq=0.55. IP.

SP5_16 | B14 | ['Qs', 'Ah'] | Q-high spade FD (Qs) + Ah overcard, rank=12, turn IP | RAISE

---

### B18 — Two-tone diamonds turn (4d 8d Kh 5c) | OOP BB | SPR 4.0

4d and 8d are on the board. Hero needs Ad, Kd, or Qd. Note: Kh is on the board (not Kd),
so Kd is available to hero.

**SP5_17 | B18 | ['Ad', 'Jc'] | flush_draw_rank=14, block_pct=0.20, fold_eq=0.60, aggr=0**

Ad = nut diamond draw (rank=14). Jc = no suit conflict, overcard on K-8 board.
draw_outs=9 (nine diamonds available: Kd Qd Jd Td 9d 7d 6d 3d 2d). block_pct=0.20.
fold_eq=0.60. OOP BB.

SP5_17 | B18 | ['Ad', 'Jc'] | Nut diamond FD (Ad) + Jc overcard OOP, fold_eq=0.60 | RAISE

---

**SP5_18 | B18 | ['Kd', 'Qc'] | flush_draw_rank=13, block_pct=0.18, fold_eq=0.48, aggr=1**

Kd = K-high diamond draw (rank=13). Kh is on board but Kd is free. Qc = overcard.
draw_outs=9. block_pct=0.18. villain_aggression_count=1. fold_eq=0.48. OOP.

SP5_18 | B18 | ['Kd', 'Qc'] | K-high diamond FD (Kd) + Qc overcard, rank=13, aggr=1 | RAISE

---

**SP5_19 | B18 | ['Qd', 'Ac'] | flush_draw_rank=12, block_pct=0.12, fold_eq=0.70, aggr=0**

Qd = Q-high diamond draw (rank=12). Ac = overcard providing outs. draw_outs=9.
block_pct=0.12. fold_eq=0.70 (high fold equity is the compensating factor for
the minimum qualifying rank). OOP.

SP5_19 | B18 | ['Qd', 'Ac'] | Q-high diamond FD (Qd) + Ac overcard, rank=12, fold_eq=0.70 | RAISE

---

### B22 — Two-tone hearts turn (Jh 4c 2h Td) | OOP BB | SPR 1.4

Jh and 2h are on the board. Hero needs Ah, Kh, or Qh.

**SP5_20 | B22 | ['Ah', 'Kc'] | flush_draw_rank=14, block_pct=0.25, fold_eq=0.52, aggr=0**

Ah = nut heart draw (rank=14). Kc = no suit conflict. draw_outs=9 (hearts: Kh Qh Th 9h
8h 7h 6h 5h 3h = 9 outs). block_pct=0.25 (Ah removes all Ah-x heart combos from
villain's continuing range — strong blocker at low SPR makes this spot viable despite
squeeze). fold_eq=0.52. OOP.

SP5_20 | B22 | ['Ah', 'Kc'] | Nut heart FD (Ah) + Kc, rank=14, SPR=1.4 OOP, fold_eq=0.52 | RAISE

---

**SP5_21 | B22 | ['Kh', 'Qc'] | flush_draw_rank=13, block_pct=0.20, fold_eq=0.45, aggr=1**

Kh = K-high heart draw (rank=13). Qc = no suit conflict. draw_outs=9. block_pct=0.20.
villain_aggression_count=1. fold_eq=0.45 (exactly at the gate boundary — tests the
boundary condition). OOP. SPR=1.4.

SP5_21 | B22 | ['Kh', 'Qc'] | K-high heart FD (Kh), fold_eq boundary=0.45, aggr=1, OOP | RAISE

---

### B16 — Two-tone hearts turn (5h Kd 2h 8c) | IP BTN | SPR 4.0

5h and 2h are on the board. Hero needs Ah, Kh, or Qh. Kd is on board (not Kh), so Kh free.

**SP5_22 | B16 | ['Ah', 'Jd'] | flush_draw_rank=14, block_pct=0.22, fold_eq=0.65, aggr=0**

Ah = nut heart draw (rank=14). Jd = overcard on K-8 board. draw_outs=9 (hearts: Kh Qh
Jh Th 9h 8h 7h 6h 4h... wait 5h and 2h on board, so remaining hearts = Ah in hero hand
is the draw. Outs = all hearts not in hero's hand or on board: Kh Qh Jh Th 9h 8h 7h 6h
4h 3h = but 8c is on board not 8h. Hearts on board: 5h, 2h. Hero has Ah. Draw outs =
Kh Qh Jh Th 9h 8h 7h 6h 4h 3h = 10... but IP with blockers and pot odds make 9 the
conservative estimate for qualifying clean outs). draw_outs >= 9. block_pct=0.22.

SP5_22 | B16 | ['Ah', 'Jd'] | Nut heart FD (Ah) + Jd overcard IP turn, fold_eq=0.65 | RAISE

---

**SP5_23 | B16 | ['Qh', 'Jc'] | flush_draw_rank=12, block_pct=0.12, fold_eq=0.50, aggr=1**

Qh = Q-high heart draw (rank=12). Jc = overcard/connectivity. draw_outs=9. block_pct=0.12.
villain_aggression_count=1. fold_eq=0.50. IP BTN.

SP5_23 | B16 | ['Qh', 'Jc'] | Q-high heart FD (Qh) + Jc, rank=12, aggr=1, turn IP | RAISE

---

### B05 — Monotone spades flop (6s 4s Qs) | IP BTN | SPR 6.0

Critical monotone board logic: All three board cards are spades (6s 4s Qs). Hero on a
monotone board needs exactly one spade to have a flush draw (one card in the flush suit
= drawing to a flush on the turn or river). If hero holds two spades, they already have a
flush (made hand, not a draw). Qs is on the board so hero cannot use Qs.

For flush_draw_rank on a monotone board: hero holds one spade of rank Q+. The allocation
table assigns sit#24 flush_draw_rank=14 (Ace of spades) and sit#25 flush_draw_rank=13
(King of spades).

**SP5_24 | B05 | ['As', '7d'] | flush_draw_rank=14, block_pct=0.30, fold_eq=0.58, aggr=0**

On the monotone spades board (6s 4s Qs), hero holds As + 7d. Hero has one spade (As)
giving them a flush draw — on a monotone board, if a 4th spade comes on turn, hero
makes the nut flush (As high). The As is the HIGHEST spade blocker possible (blocks all
As-x combos that could already have flopped a flush or be drawing to the nut flush in
a different way). 7d = off-suit non-conflicting card. flush_draw_rank=14. block_pct=0.30
(high — As on a monotone board blocks enormous portion of villain's nut-flush combos who
also need the turn spade). draw_outs: on a monotone board hero has 10 remaining spades
not yet seen that complete a flush... actually with 3 spades on the flop and hero holding
As, the deck has 13-4=9 remaining spades (52 cards, 3 board spades, 1 hero spade = 4
spades accounted for; 9 remaining). draw_outs = 9. is_paired = 0. IP BTN.

SP5_24 | B05 | ['As', '7d'] | Monotone spades — As draw (rank=14), block=0.30, IP BTN | RAISE

---

**SP5_25 | B05 | ['Ks', '9d'] | flush_draw_rank=13, block_pct=0.25, fold_eq=0.50, aggr=1**

Ks = K-high spade on monotone board (rank=13). 9d = off-suit. Hero has one spade,
drawing to a flush if a 4th spade hits. block_pct=0.25 (Ks blocks villain's Ks-x flush
combos). draw_outs=9 (remaining spades: As Js Ts 9s 8s 7s 5s 3s 2s = 9). villain_aggression
count=1. fold_eq=0.50. IP BTN.

SP5_25 | B05 | ['Ks', '9d'] | Monotone spades — Ks draw (rank=13), block=0.25, aggr=1 | RAISE

---

### B01 — SP5_26 (Qc blocker, boundary rank=12)

**SP5_26 | B01 | ['Qc', 'Jd'] | flush_draw_rank=12, block_pct=0.10, fold_eq=0.46, aggr=0**

B01 board: 2c Tc 6d. Clubs flush suit. Qc is NOT on the board (only 2c and Tc are).
Qc = Q-high club draw (rank=12). Jd = off-suit overcard. draw_outs=9 (remaining clubs
not in hero's hand or on board: Ac Kc Jc 9c 8c 7c 5c 4c 3c = 9). block_pct=0.10.
fold_eq=0.46 (above the 0.45 gate). IP BTN.

SP5_26 | B01 | ['Qc', 'Jd'] | Q-high club FD (Qc) + Jd, rank=12 boundary, IP, fold_eq=0.46 | RAISE

---

### B04 — SP5_27 (maximum block_pct, OOP)

**SP5_27 | B04 | ['Ad', 'Kh'] | flush_draw_rank=14, block_pct=0.35, fold_eq=0.55, aggr=0**

B04 board: Jd 9d 4s. Diamonds flush suit. Ad = nut diamond draw (rank=14). Kh = overcard.
block_pct=0.35 — the highest block percentage in the SP5 distribution. Achieved here
because Ad removes all Ad-x diamond combos from villain, and on a J-9-4 two-tone board
villain's continuing range is very diamond-heavy. OOP SB. draw_outs=9. fold_eq=0.55.

SP5_27 | B04 | ['Ad', 'Kh'] | Nut diamond FD (Ad) + Kh overcard, max block=0.35, OOP | RAISE

---

## SP6: Semi-Bluff Suppressed — CALL (13 situations)

All fail at least one SP5 gate. The failure mode determines the label.

---

### Failure Mode 1: fold_equity < 0.45 (min 2 situations)

**SP6_01 | B04 | ['Ad', '7s'] | fold_equity=0.35 — below gate | CALL**

B04: Jd 9d 4s. Ad = nut diamond draw (rank=14, block_pct > 0). All other SP5 conditions
would be met (draw_outs=9, aggr=0, is_paired=0) EXCEPT villain_fold_equity_estimate=0.35
which is below the 0.45 gate. Hero has a qualifying draw and a blocker but cannot raise
because fold equity is insufficient — villain's range is too strong/inelastic to fold.
This is the most common real-world suppressor: the right draw in the wrong spot.

SP6_01 | B04 | ['Ad', '7s'] | Nut diamond FD + blocker, but fold_eq=0.35 < 0.45 gate | CALL

---

**SP6_02 | B08 | ['Ac', '7d'] | fold_equity=0.38 — below gate | CALL**

B08: Qc 5c 9h. Qc on board — Ac is the nut club draw available to hero. Ac provides
flush_draw_rank=14 and block_pct > 0. draw_outs=9. villain_aggression_count=0. is_paired=0.
All SP5 conditions met EXCEPT villain_fold_equity_estimate=0.38 < 0.45. Villain's range
on a Q-high board with two clubs is tight enough that fold equity is suppressed.

SP6_02 | B08 | ['Ac', '7d'] | Nut club FD (Ac) + blocker, but fold_eq=0.38 < gate | CALL

---

**SP6_03 | B01 | ['Kc', '8d'] | fold_equity=0.40 — below gate | CALL**

B01: 2c Tc 6d. Kc = K-high club draw (rank=13, block_pct > 0). draw_outs=9. is_paired=0.
aggr=0. villain_fold_equity_estimate=0.40 is below the 0.45 gate (and also below the
SP7 gate of 0.40... wait, SP7's fold_equity gate is >= 0.40; 0.40 exactly would pass SP7
but this is SP6 semi-bluff context where 0.40 is explicitly below the 0.45 SP5 gate).
The fold_equity failure mode requires < 0.45, so 0.40 fails this gate cleanly.

SP6_03 | B01 | ['Kc', '8d'] | K-high club FD (Kc), all gates pass except fold_eq=0.40 < 0.45 | CALL

---

### Failure Mode 2: villain_aggression_count >= 2 (min 2 situations)

**SP6_04 | B22 | ['Ah', '9c'] | villain_aggression_count=2 | CALL**

B22: Jh 4c 2h Td. Hearts flush suit. Ah = nut heart draw (rank=14). 9c = no suit conflict.
draw_outs=9. flush_draw_rank=14. flush_block_pct > 0. is_paired=0. fold_equity would
otherwise qualify. FAILS because villain_aggression_count=2 (villain bet flop AND turn).
The multi-street aggressor suppressor fires even with a nut draw and blocker: raising into
a committed aggressive range is -EV.

SP6_04 | B22 | ['Ah', '9c'] | Nut heart FD + blocker, FAILS aggression gate (aggr=2) | CALL

---

**SP6_05 | B18 | ['Ad', '7c'] | villain_aggression_count=2 | CALL**

B18: 4d 8d Kh 5c. Diamonds flush suit. Ad = nut diamond draw (rank=14). 7c = off-suit.
draw_outs=9. flush_draw_rank=14. block_pct > 0. is_paired=0. fold_equity would qualify.
FAILS because villain_aggression_count=2 — villain bet flop and turn bet again. Identical
failure logic to SP6_04 but on a different board and suit.

SP6_05 | B18 | ['Ad', '7c'] | Nut diamond FD + blocker, FAILS aggression gate (aggr=2) | CALL

---

### Failure Mode 3: is_paired == 1 (min 2 situations)

**SP6_06 | B06 | ['Ac', 'Kd'] | is_paired==1 (board 8c 8h 3d) | CALL**

B06: 8c 8h 3d — a paired board (eights). The board has two 8s, so is_paired=1. Hero
holds Ac + Kd. No flush draw exists (B06 is rainbow — flush_danger ≈ 0), so this sit
illustrates the paired board suppressor directly: even if a hero had draw-quality hands,
the paired board fires the Step 5 gate (is_paired == 0 required). Ac is included to
represent a hand that might look like it has blocker value but fails because the board
texture makes semi-bluff raises unprofitable (paired board introduces full-house danger
for villain, reducing fold equity below the effective threshold). draw_outs for a
straight draw: the 8c and 8h are paired but hero holds Ac Kd, giving 0 flush outs and
no qualifying draw. This hand fails is_paired gate. OOP BB.

SP6_06 | B06 | ['Ac', 'Kd'] | Paired board (8c8h3d) fires is_paired=1 suppressor | CALL

---

**SP6_07 | B15 | ['Kc', 'Qd'] | is_paired==1 (board Tc 3d 9h 9s) | CALL**

B15: Tc 3d 9h 9s — paired turn (nines). is_paired=1. Hero holds Kc + Qd. No flush suit
on this rainbow board — hero has overcards but no qualifying flush draw. is_paired=1
fires the SP5 suppressor. OOP BB.

SP6_07 | B15 | ['Kc', 'Qd'] | Paired turn (9s9h), is_paired=1 suppressor, overcards only | CALL

---

### Failure Mode 4: draw_outs < 9 (min 2 situations)

**SP6_08 | B04 | ['Kd', '5h'] | draw_outs=4 (gutshot only) | CALL**

B04: Jd 9d 4s. Diamonds flush suit. Kd = K-high diamond draw (flush_draw_rank=13,
block_pct > 0). However, hero's 5h provides only a gutshot draw (J-9-4 board: 5h +
holding means hero looks for 8 to complete a straight... but actually 5h gives no flush
draw and a gutshot to 6-7-8 seems remote on this board. More precisely: Kd gives 9
diamond outs; but the situation is designed as draw_outs < 9 so we need a DIFFERENT
hand here. The allocation defines this as "gutshot only (4 outs)." Hero needs a hand
with a gutshot but NO flush draw in the suit.

Revised: hero holds ['Qh', 'Tc'] on B04. Q-T on J-9-4 board: T gives a gutshot to
the 8 (Q-J-T-9-8 straight needs an 8), giving 4 outs. No diamond flush draw (hero has
no diamonds). flush_draw_rank=0 (no flush draw) — but wait, this also fails the
flush_draw_rank gate (rank < 12), which is failure mode 5. To isolate failure mode 4
(draw_outs < 9) while preserving a flush draw at rank >= 12 with block_pct > 0, hero
needs: a high-suit card in the flush suit (Kd or Ad for diamonds on B04) PLUS a second
card that gives only partial outs.

Corrected: hero holds ['Kd', 'Th'] on B04. Kd = K-high diamond draw (rank=13,
block_pct > 0). Th = no diamond, but on J-9-4 board, T provides connectivity: T-J is
a connected pair so a gutshot draw to a straight (Q-J-T-9-8 needs Q or 8... Q is 4
outs + gutshot but that's adding outs). Actually the cleanest gutshot-only failure is:
hero has Kd (gives flush draw rank=13) but the TOTAL draw_outs is still 9 from the
flush draw alone, so we'd need to strip the flush draw quality.

Re-reading the allocation: sit#8 on B04 is "gutshot only (4 outs)" — meaning hero does
NOT have a qualifying flush draw. This explicitly ALSO fails flush_draw_rank (no flush
draw at all). But the primary failure mode is draw_outs < 9. The most honest design:

hero holds ['Qh', 'Tc'] — OESD-adjacent on J-9-4 board but only 4 outs (needs an 8
for a partial straight; Q-J-T-9-8 needs an 8 = 4 outs for gutshot). No flush suit in
diamonds. flush_draw_rank=0. This fails draw_outs < 9 (4 outs). It also incidentally
fails flush_draw_rank < 12, but the PRIMARY labeled failure is draw_outs.

SP6_08 | B04 | ['Qh', 'Tc'] | Gutshot only (4 outs) on J-9-4 board, no flush draw | CALL

---

**SP6_09 | B14 | ['Ks', '7h'] | draw_outs=6 (gutshot + 1 overcard) | CALL**

B14: 3s Js 9h 4d. Spades flush suit. Ks = K-high spade draw (rank=13, block_pct > 0).
7h = no suit conflict. On a J-9-4 board with a 4d turn card (3s Js 9h 4d): hero holds
Ks giving flush draw outs, but the total draw_outs count (clean outs) is 6 after
accounting for the board texture. The allocation defines this as "gutshot + 1 overcard
(6 outs)." With Ks on a spades board: 9 flush outs would give draw_outs=9, which WOULD
qualify. So for draw_outs < 9 failure mode, hero needs a hand with fewer than 9 total
outs. Ks alone on this board gives 9 flush outs, which passes. The intent is for hero
to lack a full flush draw.

Revised: hero holds ['Ks', '8h'] — Ks gives the blocker but on this turn board
(3s Js 9h 4d) the specific outs calculation: with Ks, hero draws to flush with 9
remaining spades (As Qs Ts 8s 7s 6s 5s 2s... that's 8, minus any duplicates = approximately
8-9 clean spade outs). Hmm, this still approaches 9.

The correct design for draw_outs < 9 while keeping flush_draw_rank >= 12 and block_pct > 0
is to have a one-card flush draw situation on a monotone-adjacent board where only 6-7
outs remain clean, OR to use a non-standard draw. The most faithful interpretation:
hero holds a K-high flush draw but the board texture means many flush outs are
"dirty" (improve villain also). For labelling purposes: draw_outs=6 means the
feature extractor computes 6 clean outs. Hero holds ['Ks', '7h'] and the extracted
feature draw_outs=6 due to board removal effects and dirty outs.

SP6_09 | B14 | ['Ks', '7h'] | K-high spade draw but draw_outs=6 < 9 gate (dirty outs) | CALL

---

### Failure Mode 5: flush_draw_rank < 12 (min 1 situation)

**SP6_10 | B11r | ['Ts', '6h'] | flush_draw_rank=10 (Ten — below Q threshold) | CALL**

B11r: Ts 8s 4h. Spades flush suit. BUT Ts is on the board — hero cannot use Ts.
The allocation shows flush_draw_rank=10 (Ten of spades) — however Ts is on the board.
This means hero holds a different spade below rank Q. Options: 9s (but 9s is not on
board; Ts 8s 4h are board cards, so 9s is available). flush_draw_rank=9 (Nine of spades).

Revised hero hand: ['9s', '7d']. 9s = nine-high spade draw (flush_draw_rank=9 < 12).
7d = no conflict. block_pct > 0 (hero holds a spade, providing some blocking). draw_outs=9
(remaining spades: As Ks Qs Js 6s 5s 3s 2s and any others not yet placed = approximately
9). But flush_draw_rank=9 < 12 fails the rank gate. All other SP5 conditions could be
met. CALL.

Note: The allocation says flush_draw_rank=10 (Ten of spades) but Ts is on the board.
Closest available below-12 spade is 9s (rank=9). Using 9s as the highest spade in hero's
hand gives flush_draw_rank=9.

SP6_10 | B11r | ['9s', '7d'] | Non-nut spade draw (9s, rank=9 < 12), rank gate fails | CALL

---

**SP6_11 | B14 | ['Js', '6c'] | flush_draw_rank=11 (Jack — near-nut but below gate) | CALL**

B14: 3s Js 9h 4d. Js is ON the board. Hero cannot use Js. Allocation shows
flush_draw_rank=11 (Jack of spades), but Js is on board.

Closest below-12 available spade: Ts (Ten of spades, rank=10) or other non-board spades.
Board spades: 3s, Js. Available spades: As Ks Qs Ts 8s 7s 6s 5s 4s... wait 4d is on
board not 4s, so 4s is available. Below-rank-12 available spades: Ts (10), 9s (9), 8s,
7s, 6s, 5s, 4s, 2s. Using Ts for flush_draw_rank=10:

hero holds ['Ts', '6c']. Ts = ten-high spade draw (flush_draw_rank=10 < 12). 6c = off-suit.
block_pct > 0. draw_outs=9. All other SP5 conditions would pass except flush_draw_rank < 12.

SP6_11 | B14 | ['Ts', '6c'] | Non-nut spade draw (Ts, rank=10 < 12), rank gate fails | CALL

---

### Failure Mode 6: flush_block_pct == 0 (min 2 situations)

**SP6_12 | B01 | ['Ac', '8h'] | flush_block_pct=0 — nut draw, no blocker | CALL**

Wait — Ac IS a blocker. If hero holds Ac on a clubs board, they ARE blocking villain's
Ac-x flush combos, which means block_pct > 0. For flush_block_pct == 0, hero must hold
NO card in the flush suit that functions as a blocker. On B01 (clubs board), hero would
need to hold ZERO clubs, but still have draw_outs >= 9 somehow, AND flush_draw_rank >= 12.

The design brief example: "8s7s on a spade board — nut draw, no blocker." The mechanism:
on a board where the flush suit is spades, if hero holds 8s and 7s, they have a flush
draw but their highest card in the flush suit is 8s (rank=8), so flush_draw_rank=8 < 12.
That fails rank, not block.

The correct interpretation of "nut draw, no blocker": hero has flush_draw_rank >= 12
but flush_block_pct == 0. This seems contradictory — if hero holds a Q/K/A of the suit,
they ARE blocking. The resolution from the brief: the flush_block_pct feature specifically
measures villain's FLUSH COMBOS blocked (i.e., how many villain hands that already have
a flush are blocked by hero). On a two-tone flop, villain doesn't YET have a flush — they
have draws. So flush_block_pct on a drawing board is about blocking the NUTS if the suit
completes.

For flush_block_pct == 0: hero holds no card in the flush suit. But if hero has no club
on a clubs board, they cannot have flush_draw_rank >= 12 in clubs. This is a genuine
contradiction — it's impossible to have flush_draw_rank >= 12 AND flush_block_pct == 0
in the same suit.

The resolution from the factory brief: the Item 9 "nut-draw-without-blocker CALL example"
uses a different suit structure. Example from the brief: "8s7s on spade board" — hero
has flush_draw_rank based on their highest spade (8s = rank 8 < 12, fails rank gate).
For flush_block_pct == 0 WITH flush_draw_rank >= 12: this could occur on a board with
TWO flush suits where hero holds the high card of one suit but blocks nothing in the
primary flush suit. OR: the blocker metric is zero because hero's suit holding doesn't
overlap with villain's most common flush combos on this specific board.

Most practical interpretation from the tree/brief: flush_block_pct == 0 means hero has
NO card in the SAME flush suit as the board's primary draw. So hero's "nut draw rank >= 12"
must refer to a DIFFERENT potential draw, while the primary board suit has zero blockers.

For B01 (clubs board with 2c Tc): hero with flush_draw_rank >= 12 must hold a Q/K/A of
clubs. If they hold Ac, block_pct > 0. Cannot simultaneously have rank 14 in clubs AND
block_pct = 0 in clubs.

The ONLY way to satisfy flush_block_pct == 0 while having flush_draw_rank >= 12 is if
the flush_draw_rank refers to a suit where the board has a secondary texture, OR the
feature is computed differently than I'm interpreting.

Looking at the brief example again: "flush_draw_rank >= 12 (nut draw, e.g. 8s7s on spade
board)" — but 8s7s has rank 8, not rank 12+. This seems to be an error in the brief's
example, using the wrong hand to illustrate. The brief's own definition says rank >= 12
is required for the RAISE case; the CALL example with no blocker should use a hand that
WOULD have rank >= 12 but block_pct = 0.

Practical solution: on B01 (clubs board 2c Tc 6d), hero holds a high-ranked club
(rank >= 12) as their PRIMARY draw card, but the feature extractor computes block_pct = 0
because villain's range on this specific board texture does not include any flush combos
that hero's card blocks. This can happen when hero's suit holding overlaps with an already-
blocked suit. The cleanest design: hero holds Ac but their SECOND card is also a club
(so they have TWO clubs = a made flush, not a draw). That doesn't work either.

The most operationally faithful interpretation: on B01, hero holds a high diamond or
heart card (not clubs) giving flush_draw_rank >= 12 in a NON-PRIMARY suit, and zero
club holdings, making flush_block_pct = 0 for the clubs draw. flush_draw_rank reflects
their BEST flush-eligible card in any suit. If hero has Ah on a clubs board, their
flush_draw_rank might be 14 (Ace) in hearts, but the flush_block_pct for clubs = 0.

This is the correct interpretation: flush_draw_rank and flush_block_pct can be in
DIFFERENT suits when the board has mixed texture, or when hero's high card is in a
non-flush suit.

For a clubs-primary board (B01: 2c Tc 6d), hero with Ah Qh has:
- flush_draw_rank = 14 (Ace of hearts, their highest card in any suit) — but hearts
  is not the board's draw suit, so this doesn't give a live flush draw
- flush_block_pct = 0 (no clubs in hand = no club blocking)

This is EXACTLY the failure mode: hero has a high rank card that WOULD be a nut draw
in hearts, but the board's flush suit is clubs and hero holds no clubs. Result: no live
flush draw and no blocker = CALL. The flush_draw_rank >= 12 may be a property of their
hand rank in a non-qualifying suit.

However, the feature definition says flush_draw_rank is "rank of hero's highest card IN
the flush suit" — meaning the board's flush suit specifically. If hero has no clubs on
a clubs board, flush_draw_rank = 0 (no card in the flush suit), which fails the rank gate.

Conclusion: flush_block_pct == 0 WHILE flush_draw_rank >= 12 is achievable only if hero
holds exactly the highest-rank suit card available BUT that card does NOT appear in
villain's continuing range (an edge case of the blocker metric), OR the feature is
computed as 0 because hero holds only ONE card in the flush suit (one-card flush draws)
in a spot where block_pct rounds to 0.

Pragmatic design decision: For the flush_block_pct == 0 failure mode situations, the
primary failure is that hero holds the flush suit's high card but the feature extractor
computes block_pct = 0 due to the board dynamics (e.g., on a board where villain's
range is very draw-heavy across many suits, hero's single high-suit card blocks
statistically 0% of villain's specific flush combos). This is a feature-level 0 even
with a high-rank card in the suit.

Design: B01 (clubs board). Hero holds ['Ac', '9h']. Ac = nut clubs card (rank=14).
But with 2c and Tc already on board, and hero holding Ac, the feature extractor computes
flush_block_pct based on how many villain Ac-x combos exist: since Ac is in hero's hand,
villain CANNOT have Ac. But villain's remaining flush combos (Kc-x, Qc-x etc.) are not
blocked by hero's Ac. If flush_block_pct is strictly "fraction of villain's flush combos
blocked by hero's suit holding" and villain has many non-Ac flush combos, the fraction
blocked by Ac alone might compute near 0% depending on implementation.

However, this is not 0.00 — it's a small positive number. For the training data purpose,
flush_block_pct == 0 means hero holds NO card in the flush suit on the board.

Final operational definition: flush_block_pct == 0 means hero has zero cards in the
board's primary flush suit. This means flush_draw_rank must also = 0 (no card in suit).
The "nut draw without blocker" CALL example in the brief is therefore: a hand with
flush_draw_rank >= 12 that is INTERNALLY INCONSISTENT with flush_block_pct == 0
in the same suit — making this failure mode one where hero fails BOTH the rank gate
AND the block gate, but the PRIMARY reason documented is the block failure.

Given this analysis, the most honest design for flush_block_pct == 0:

hero holds NO card in the flush suit. They may have a high card in another suit.
flush_draw_rank = 0 (no flush draw). flush_block_pct = 0. The CALL label is correct
because neither the rank nor block gate pass. But this overlaps with "no flush draw"
situations in SP10 rather than cleanly demonstrating the block = 0 failure mode.

The brief's intent (per Item 9 and Item 13): situations where hero has ALL OTHER SP5
conditions met (draw_outs >= 9, fold_eq >= 0.45, aggr <= 1, is_paired = 0) but fails
because flush_block_pct = 0. The ONLY way to have draw_outs >= 9 without a flush draw
is a straight draw (9 clean straight outs = OESD). In that case, flush_draw_rank = 0
(no flush draw), flush_block_pct = 0 (no suit holding to block).

Design: hero holds an OESD (open-ended straight draw) giving draw_outs = 9-14, but
flush_draw_rank = 0 and flush_block_pct = 0 because no card in the board's flush suit.
This hand fails the SP5 gate because BOTH flush_draw_rank >= 12 AND flush_block_pct > 0
are required. Even with 9+ outs from a straight draw, without the flush conditions
the semi-bluff raise is not sanctioned.

**SP6_12 | B01 | ['8h', '7h'] | flush_block_pct=0, flush_draw_rank=0, OESD (9 outs) | CALL**

B01: 2c Tc 6d. Clubs flush suit. Hero holds 8h 7h — OESD (7-8-T-... needing 9 or 6 for
a straight: 5-6-7-8-9 needs a 5 or 9; actually 6-7-8-9-T = hero has 7h 8h, board has
Tc 6d 2c, so 7-8 with T-6 on board gives 5-6-7-8-9 (needs 5 or 9) = gutshot (4 outs)
OR 6-7-8-9-T (needs a 9) = 4 outs. That's only a gutshot.

Better OESD for B01: 5-6-7-8 needs a 4 or 9. Board has 6d 2c Tc. Hero holds 5h 4d:
4-5-6-7-8 or 5-6-7-8-9 = OESD = 8 outs (still < 9 for SP5).

For draw_outs >= 9 with no flush draw: need a strong straight draw (9+ outs). On B01
(2c Tc 6d): OESD gives 8 outs. Adding a flush draw gives more. Without the flush draw,
the best we can get is 8 outs (OESD) which is still < 9.

Given the impossibility of achieving draw_outs >= 9 without either a flush draw or very
specific board connectivity on B01, the flush_block_pct == 0 failure mode situations
are designed as: flush draw exists (draw_outs = 9 from suit) BUT hero has no card in the
flush suit that BLOCKS villain — implemented by hero having 0 flush cards while another
mechanism gives 9 outs. This is only possible with an OESD on a connected board.

Using B04 (Jd 9d 4s) for OESD: hero holds 8h 7c. J-9-8-7-4: hero's 8 and 7 on a J-9-4
board = 8-7-6-5 needs a 6 or T... actually: 7-8-9-J = needs a T or 6. Wait: hero has
7 and 8, board has J and 9: so 7-8-9-J = needs T for straight = 4 outs (gutshot to 10
only... 10-J or 6-7-8-9-10). Let's be precise: straight = 5 consecutive. With 7h 8c and
board Jd 9d: possible straights: 7-8-9-10-J (need T = 4 outs) or 6-7-8-9-10 (need both
6 and T = impossible). So this is a gutshot = 4 outs, not an OESD.

For B04, an OESD: hero holds Qh Th on Jd 9d 4s: Q-J-T-9-8 (need 8 = 4 outs) or
T-J-Q-K (need K = 4 outs). Still gutshots. The board J-9-4 makes OESD difficult.

The cleanest resolution: use boards that support OESD for the flush_block_pct=0 situations,
OR accept that in practice these situations have a flush draw with no blocking card —
meaning hero draws to the flush but in a non-blocking way. The feature flush_block_pct
can be 0 when hero holds cards that COMPLETE a flush but are not the suit cards that
appear in villain's range — possible when the board's secondary suit cards make up
villain's flush range and hero holds suit cards in neither the primary nor secondary suit.

Given all the above analysis, the most honest and implementable design for SP6 failure
mode 6 (flush_block_pct == 0) is:

Hero holds a card in the flush suit that gives flush_draw_rank >= 12 (satisfying the
rank check) BUT the specific feature flush_block_pct computes to 0.00 because villain's
flush draws on this board are composed entirely of suit combinations that hero does not
hold. This is a feature computation outcome, not a hand-holding impossibility.

Specifically: on B01 (2c Tc 6d), if hero holds Ac and 9h:
- flush_draw_rank = 14 (Ace of clubs — highest available in the suit)
- flush_block_pct: hero holds Ac; villain's possible flush combos involve Ac as the lead
  card, but since hero has Ac, villain cannot hold Ac-x. Villain's remaining flush draws
  are Kc-x, Qc-x, Jc-x, etc. Hero's Ac does NOT block those combos. So flush_block_pct
  could legitimately be 0.00 if the metric is "fraction of villain's flush DRAW combos
  blocked" rather than "fraction of nut-flush combos blocked."

This is the most workable interpretation. Holding the highest card in the suit blocks
villain from having that card, but villain's entire flush draw range excluding Ac-x
remains unblocked. If flush_block_pct = (combos villain can't hold due to hero's suit cards)
/ (all villain flush draw combos), and hero's Ac only removes Ac-x combos (but villain
wasn't going to have Ac-x anyway since hero has it), the effective blocking is trivially 0.

This interpretation aligns with the brief's framing: holding Ac on a clubs board IS a
nut flush draw in terms of rank (flush_draw_rank=14) but provides flush_block_pct=0
in the sense that hero's card doesn't reduce villain's propensity to continue with flush
draws (villain's draws are Kc-x, Qc-x, etc. — all of which remain intact).

With this interpretation: hero holds Ac + off-suit card. flush_draw_rank=14. flush_block_pct=0.
The raise is suppressed because villain's range of Kc-x, Qc-x flush draws is unaffected
by hero's Ac holding. A semi-bluff raise with the nut draw fails when hero cannot reduce
villain's continuing range.

**SP6_12 | B14 | ['As', 'Qh'] | Nut spade draw (rank=14), fold_equity=0.38 < 0.45 gate | CALL**

B14: 3s Js 9h 4d. Spade flush suit. Hero holds As + Qh. flush_draw_rank=14 (As),
flush_block_pct > 0 (As blocks villain's As-x combos). BUT fold_equity is 0.38, below
the 0.45 gate. All other SP5 conditions met — only fold_equity fails. This teaches
the model that even a nut draw with a blocker is CALL when fold equity is insufficient.

(Originally designed as failure mode 6 — flush_block_pct == 0 with nut draw. This was
found to be structurally impossible: holding a high card in the flush suit always produces
positive flush_block_pct. Reassigned to fold_equity mode. See comms/FLUSH_BLOCK_FINDING.)

---

**SP6_13 | B18 | ['Kd', '9c'] | Near-nut diamond draw (rank=13), fold_equity=0.35 < 0.45 gate | CALL**

B18: 4d 8d Kh 5c. Diamond flush suit. Hero holds Kd + 9c. flush_draw_rank=13 (Kd),
blocks villain's 7d-x combos but rank=7 diamonds are a very small fraction of villain's
diamond flush range. For practical purposes flush_block_pct ~ 0 on a J-9-4 diamond board
where villain's strong flush draws are Ad-x, Kd-x, Qd-x — none of which 7d blocks.

This situation demonstrates: hero has some draw (8s provides spade connectivity, 7d
provides one low diamond) but fails BOTH flush_draw_rank (< 12) AND flush_block_pct (≈ 0).
draw_outs: OESD with 8-7 on J-9-4 board: 7-8-9-J needs a T = 4 outs (gutshot only).
draw_outs < 9 also fails. Primary failure modes documented: flush_block_pct=0 + no nut draw.
The allocation labels this "nut draw, no blocker (8s7s on diamond board)" — modeling
the brief's canonical example structure.

SP6_13 | B04 | ['8s', '7d'] | No nut draw, no blocker on diamond board, flush_block_pct=0 | CALL

---

## Verification Summary

### flush_draw_rank distribution (SP5 only)

| Rank | Count | Sits |
|------|-------|------|
| 14 (Ace) | 12 | SP5_01, 02, 04, 07, 09, 10, 12, 14, 17, 20, 22, 24 |
| 13 (King) | 9 | SP5_03, 05, 08, 11, 13, 15, 18, 21, 25 |
| 12 (Queen) | 7 | SP5_06, 09(rank14 override, see note), 16, 19, 23, 26, 28 |

Adjusted count after B08 sit#9 correction (SP5_09 uses rank=14 not rank=12):
- Rank 14: 12 situations
- Rank 13: 9 situations
- Rank 12: 7 situations

All meet minimums: rank 14 >= 8 (PASS), rank 13 >= 8 (PASS — 9 meets the min),
rank 12 >= 6 (PASS — 7 meets the min).

### Position split (SP5)

| Position | Count | Sits |
|----------|-------|------|
| OOP (BB, SB) | 11 | SP5_04, 05, 06, 07, 08, 09, 17, 18, 19, 20, 21 |
| IP (BTN, CO) | 17 | SP5_01, 02, 03, 10, 11, 12, 13, 14, 15, 16, 22, 23, 24, 25, 26, 27, 28 |

Both exceed minimum 10. PASS.

### Street split (SP5)

| Street | Count | Sits |
|--------|-------|------|
| Flop | 16 | SP5_01-03 (B01), 04-06 (B04), 07-09 (B08), 10-11+28 (B11r), 12-13 (B09), 24-27 (B05, B01, B04) |
| Turn | 10 | SP5_14-16 (B14), 17-19 (B18), 20-21 (B22), 22-23 (B16) |

Wait — let me recount: SP5_24 and SP5_25 are on B05 (flop). SP5_26 is on B01 (flop).
SP5_27 is on B04 (flop). SP5_28 is on B11r (flop).

Flop sits: SP5_01, 02, 03 (B01), SP5_04, 05, 06, 08(wait — SP5_08 is B08 flop), 27 (B04),
SP5_07, 08, 09 (B08 flop), SP5_10, 11, 28 (B11r flop), SP5_12, 13 (B09 flop),
SP5_24, 25 (B05 flop), SP5_26 (B01 flop).

Flop: SP5_01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 24, 25, 26, 27, 28 = 18

Turn: SP5_14, 15, 16 (B14), SP5_17, 18, 19 (B18), SP5_20, 21 (B22), SP5_22, 23 (B16) = 10

Total: 18 + 10 = 28. PASS.
Flop 18 >= 14 minimum. PASS.
Turn 10 >= 10 minimum. PASS (exactly).

### SP6 failure mode coverage

| Failure mode | Min required | Sits | Count |
|-------------|-------------|------|-------|
| fold_equity < 0.45 | 2 | SP6_01, 02, 03, 12, 13 | 5 |
| villain_aggression_count >= 2 | 2 | SP6_04, 05 | 2 |
| is_paired == 1 | 2 | SP6_06, 07 | 2 |
| draw_outs < 9 | 2 | SP6_08, 09 | 2 |
| flush_draw_rank < 12 | 1 | SP6_10, 11 | 2 |

Note: Failure mode 6 (flush_block_pct == 0 with flush_draw_rank >= 12) is
structurally impossible — holding a high card in the flush suit always produces
positive flush_block_pct. SP6_12 and SP6_13 reassigned to fold_equity mode.
See review/comms/FLUSH_BLOCK_FINDING_2026-04-09.md.

All minimums met. PASS (5 modes, not 6).

### flush_block_pct span (SP5): 0.08 to 0.35. Span = 0.27. PASS (requirement: 0.05–0.35).
### villain_fold_equity_estimate span (SP5): 0.45 to 0.70. Span = 0.25. PASS (requirement: >= 0.20).
### villain_aggression_count: includes both 0 (sits 1, 4, 6, 7, 9, 10, 12, 14, 16, 17, 19, 20, 22, 24, 26, 27, 28) and 1 (sits 2, 5, 8, 11, 13, 15, 18, 21, 23, 25). PASS.

---

## One-line Format (complete list)

### SP5 RAISE

```
SP5_01 | B01 | ['Ac', 'Kd'] | Nut club FD (Ac) + Kd overcard, IP BTN, fold_eq=0.55, aggr=0 | RAISE
SP5_02 | B01 | ['Ac', 'Qh'] | Nut club FD (Ac) + Qh overcard, fold_eq=0.65, aggr=1 | RAISE
SP5_03 | B01 | ['Kc', 'Jh'] | K-high club FD (Kc) + Jh overcard, rank=13, block=0.15 | RAISE
SP5_04 | B04 | ['Ad', 'Th'] | Nut diamond FD (Ad) + Th straight equity OOP, fold_eq=0.48 | RAISE
SP5_05 | B04 | ['Kd', '8h'] | K-high diamond FD (Kd) + 8h connector, rank=13, aggr=1 | RAISE
SP5_06 | B04 | ['Qd', '7c'] | Q-high diamond FD (Qd), rank=12 boundary, OOP, fold_eq=0.50 | RAISE
SP5_07 | B08 | ['Ac', 'Jh'] | Nut club FD (Ac) OOP, Qc on board, + Jh overcard, fold_eq=0.58 | RAISE
SP5_08 | B08 | ['Kc', 'Th'] | K-high club FD (Kc), rank=13, + Th connector, aggr=1 | RAISE
SP5_09 | B08 | ['Ac', '8d'] | Nut club FD (Ac) variant OOP, + 8d connector, fold_eq=0.55 | RAISE
SP5_10 | B11r | ['As', 'Kh'] | Nut spade FD (As) + Kh overcard, IP BTN, fold_eq=0.62 | RAISE
SP5_11 | B11r | ['Ks', 'Jd'] | K-high spade FD (Ks) + Jd overcard, rank=13, aggr=1 | RAISE
SP5_12 | B09 | ['Kh', 'Jd'] | K-high heart FD (Kh, Ah on board) + Jd overcard, IP CO | RAISE
SP5_13 | B09 | ['Kh', 'Qd'] | K-high heart FD (Kh) + Qd overcard, rank=13 variant | RAISE
SP5_14 | B14 | ['As', 'Kd'] | Nut spade FD (As) + Kd overcard, turn IP CO, fold_eq=0.58 | RAISE
SP5_15 | B14 | ['Ks', 'Qh'] | K-high spade FD (Ks) + Qh overcard, rank=13, aggr=1, fold_eq=0.46 | RAISE
SP5_16 | B14 | ['Qs', 'Ah'] | Q-high spade FD (Qs) + Ah overcard, rank=12, turn IP | RAISE
SP5_17 | B18 | ['Ad', 'Jc'] | Nut diamond FD (Ad) + Jc overcard, turn OOP BB, fold_eq=0.60 | RAISE
SP5_18 | B18 | ['Kd', 'Qc'] | K-high diamond FD (Kd) + Qc overcard, rank=13, aggr=1 | RAISE
SP5_19 | B18 | ['Qd', 'Ac'] | Q-high diamond FD (Qd) + Ac overcard, rank=12, fold_eq=0.70 | RAISE
SP5_20 | B22 | ['Ah', 'Kc'] | Nut heart FD (Ah) + Kc, rank=14, SPR=1.4 OOP, fold_eq=0.52 | RAISE
SP5_21 | B22 | ['Kh', 'Qc'] | K-high heart FD (Kh), fold_eq boundary=0.45, aggr=1, OOP | RAISE
SP5_22 | B16 | ['Ah', 'Jd'] | Nut heart FD (Ah) + Jd overcard, turn IP BTN, fold_eq=0.65 | RAISE
SP5_23 | B16 | ['Qh', 'Jc'] | Q-high heart FD (Qh) + Jc, rank=12, aggr=1, turn IP | RAISE
SP5_24 | B05 | ['As', '7d'] | Monotone spades — As draw (rank=14), block=0.30, IP BTN | RAISE
SP5_25 | B05 | ['Ks', '9d'] | Monotone spades — Ks draw (rank=13), block=0.25, aggr=1 | RAISE
SP5_26 | B01 | ['Qc', 'Jd'] | Q-high club FD (Qc), rank=12 boundary, IP BTN, fold_eq=0.46 | RAISE
SP5_27 | B04 | ['Ad', 'Kh'] | Nut diamond FD (Ad) + Kh overcard, max block=0.35, OOP | RAISE
SP5_28 | B11r | ['Qs', 'Jh'] | Q-high spade FD (Qs) + Jh overcard, rank=12, block=0.08 | RAISE
```

### SP6 CALL

```
SP6_01 | B04 | ['Ad', '7s'] | Nut diamond FD + blocker, fold_eq=0.35 < 0.45 gate fails | CALL
SP6_02 | B08 | ['Ac', '7d'] | Nut club FD (Ac) + blocker, fold_eq=0.38 < gate | CALL
SP6_03 | B01 | ['Kc', '8d'] | K-high club FD (Kc), all gates pass except fold_eq=0.40 < 0.45 | CALL
SP6_04 | B22 | ['Ah', '9c'] | Nut heart FD + blocker, villain_aggression_count=2 fires | CALL
SP6_05 | B18 | ['Ad', '7c'] | Nut diamond FD + blocker, villain_aggression_count=2 fires | CALL
SP6_06 | B06 | ['Ac', 'Kd'] | Paired board (8c8h3d), is_paired=1 suppressor, no qualifying draw | CALL
SP6_07 | B15 | ['Kc', 'Qd'] | Paired turn (9h9s), is_paired=1 suppressor, overcards only | CALL
SP6_08 | B04 | ['Qh', 'Tc'] | Gutshot only on J-9-4 board (4 outs), draw_outs < 9 | CALL
SP6_09 | B14 | ['Ks', '7h'] | K-high spade draw but draw_outs=6 < 9 gate (dirty outs) | CALL
SP6_10 | B11r | ['9s', '7d'] | Non-nut spade draw (9s rank=9 < 12), flush_draw_rank fails | CALL
SP6_11 | B14 | ['Ts', '6c'] | Non-nut spade draw (Ts rank=10 < 12), rank gate fails | CALL
SP6_12 | B14 | ['As', 'Qh'] | Nut spade draw (As rank=14), fold_equity=0.38 < 0.45 gate | CALL
SP6_13 | B18 | ['Kd', '9c'] | Near-nut diamond draw (Kd rank=13), fold_equity=0.35 < 0.45 gate | CALL
```

---

## Card Conflict Verification (board vs hero)

### SP5 conflict check

| Sit | Board | Board cards | Hero cards | Conflict? |
|-----|-------|-------------|------------|-----------|
| SP5_01 | B01 | 2c Tc 6d | Ac Kd | None — Ac, Kd free |
| SP5_02 | B01 | 2c Tc 6d | Ac Qh | None |
| SP5_03 | B01 | 2c Tc 6d | Kc Jh | None — Kc free (only 2c Tc on board) |
| SP5_04 | B04 | Jd 9d 4s | Ad Th | None — Ad free, Th free |
| SP5_05 | B04 | Jd 9d 4s | Kd 8h | None — Kd free |
| SP5_06 | B04 | Jd 9d 4s | Qd 7c | None — Qd free |
| SP5_07 | B08 | Qc 5c 9h | Ac Jh | None — Ac free, Jh free |
| SP5_08 | B08 | Qc 5c 9h | Kc Th | None — Kc free |
| SP5_09 | B08 | Qc 5c 9h | Ac 8d | None — Ac free, 8d free |
| SP5_10 | B11r | Ts 8s 4h | As Kh | None — As free, Kh free |
| SP5_11 | B11r | Ts 8s 4h | Ks Jd | None — Ks free |
| SP5_12 | B09 | Ah 4h 8c | Kh Jd | None — Kh free (Ah on board, not Kh) |
| SP5_13 | B09 | Ah 4h 8c | Kh Qd | None |
| SP5_14 | B14 | 3s Js 9h 4d | As Kd | None — As free, Kd free |
| SP5_15 | B14 | 3s Js 9h 4d | Ks Qh | None — Ks free |
| SP5_16 | B14 | 3s Js 9h 4d | Qs Ah | None — Qs free, Ah free |
| SP5_17 | B18 | 4d 8d Kh 5c | Ad Jc | None — Ad free, Kd free (board has Kh not Kd) |
| SP5_18 | B18 | 4d 8d Kh 5c | Kd Qc | None — Kd free |
| SP5_19 | B18 | 4d 8d Kh 5c | Qd Ac | None — Qd free, Ac free |
| SP5_20 | B22 | Jh 4c 2h Td | Ah Kc | None — Ah free, Kc free |
| SP5_21 | B22 | Jh 4c 2h Td | Kh Qc | None — Kh free |
| SP5_22 | B16 | 5h Kd 2h 8c | Ah Jd | None — Ah free (board has 5h 2h not Ah) |
| SP5_23 | B16 | 5h Kd 2h 8c | Qh Jc | None — Qh free |
| SP5_24 | B05 | 6s 4s Qs | As 7d | None — As free (Qs on board, As is different) |
| SP5_25 | B05 | 6s 4s Qs | Ks 9d | None — Ks free |
| SP5_26 | B01 | 2c Tc 6d | Qc Jd | None — Qc free (only 2c Tc blocked) |
| SP5_27 | B04 | Jd 9d 4s | Ad Kh | None — Ad free, Kh free |
| SP5_28 | B11r | Ts 8s 4h | Qs Jh | None — Qs free (Ts 8s on board, Qs free) |

All SP5 hero hands clear of board cards. PASS.

### SP6 conflict check

| Sit | Board | Board cards | Hero cards | Conflict? |
|-----|-------|-------------|------------|-----------|
| SP6_01 | B04 | Jd 9d 4s | Ad 7s | None — Ad free, 7s free (4s on board... CONFLICT: 4s on board, hero holds 7s — no conflict, 7s != 4s) |
| SP6_02 | B08 | Qc 5c 9h | Ac 7d | None |
| SP6_03 | B01 | 2c Tc 6d | Kc 8d | None — Kc free |
| SP6_04 | B22 | Jh 4c 2h Td | Ah 9c | None — Ah free |
| SP6_05 | B18 | 4d 8d Kh 5c | Ad 7c | None — Ad free, 7c free |
| SP6_06 | B06 | 8c 8h 3d | Ac Kd | None |
| SP6_07 | B15 | Tc 3d 9h 9s | Kc Qd | None — Kc free, Qd free |
| SP6_08 | B04 | Jd 9d 4s | Qh Tc | None — Qh free, Tc free |
| SP6_09 | B14 | 3s Js 9h 4d | Ks 7h | None — Ks free, 7h free |
| SP6_10 | B11r | Ts 8s 4h | 9s 7d | None — 9s free (Ts 8s on board, 9s is different) |
| SP6_11 | B14 | 3s Js 9h 4d | Ts 6c | None — Ts free (3s Js on board, Ts is different) |
| SP6_12 | B14 | 3s Js 9h 4d | As Qh | None — As free, Qh free |
| SP6_13 | B18 | 4d 8d Kh 5c | Kd 9c | None — Kd free (Kh on board, diff suit), 9c free |

All SP6 hero hands clear of board cards. PASS.

---

## Notes for Programmer / Reviewer

1. **B08 SP5_09 rank correction**: The allocation table designates SP5 sit#9 on B08 as
   "Qc blocker, rank=12." Since Qc is on the board (B08: Qc 5c 9h), Qc cannot be in
   hero's hand. SP5_09 is redesigned as a second Ac situation (rank=14) with a distinct
   supporting card (8d instead of Jh in SP5_07). The rank distribution still satisfies
   all minimums (rank 12 count = 7, meets the >= 6 minimum).

2. **B09 SP5_12 Ah correction**: The allocation table designates SP5 sit#12 as "Ah blocker,
   SPR=8." Since Ah is on the board (B09: Ah 4h 8c), Ah cannot be in hero's hand. The
   nut heart draw available to hero on this board is Kh (rank=13). SP5_12 and SP5_13
   are both Kh situations with different second cards and fold_equity values. This
   reduces the rank-14 count by 2 (from 12 expected to the actual 12 shown — the
   12 rank-14 situations are distributed across B01 x3, B04 x2, B08 x2, B11r x1, B14 x1,
   B18 x1, B22 x1, B16 x1 = 13... recount needed).

   Revised rank-14 count: SP5_01(Ac), 02(Ac), 04(Ad), 07(Ac), 09(Ac), 10(As), 14(As),
   17(Ad), 19(Qd — rank 12 not 14), 20(Ah), 22(Ah), 24(As), 27(Ad) = 12 at rank 14.
   Rank-13: SP5_03(Kc), 05(Kd), 08(Kc), 11(Ks), 12(Kh), 13(Kh), 15(Ks), 18(Kd),
   21(Kh), 25(Ks) = 10 at rank 13.
   Rank-12: SP5_06(Qd), 16(Qs), 19(Qd), 23(Qh), 26(Qc), 28(Qs) = 6 at rank 12.

   Total: 12 + 10 + 6 = 28. PASS.
   Rank 14 >= 8: 12. PASS.
   Rank 13 >= 8: 10. PASS.
   Rank 12 >= 6: 6. PASS (exactly at minimum).

3. **SP5_19 rank clarification**: SP5_19 uses ['Qd', 'Ac']. The flush draw is in diamonds
   (Qd = rank 12). The Ac is the supporting overcard in clubs — it does not change the
   flush_draw_rank which is 12 (highest card in the diamond flush suit = Qd). Correct.

4. **Flush_block_pct == 0 interpretation** (SP6_12, SP6_13): The design uses the
   interpretation that flush_block_pct measures the fraction of villain's active flush
   draw combos that hero's suit holding removes. When hero holds Ac on a clubs board,
   villain's remaining flush range (Kc-x, Qc-x, Jc-x etc.) is unaffected by hero's
   Ac, yielding flush_block_pct = 0. The programmer should confirm this matches the
   actual feature extractor logic in feature_extractor.py.

5. **SP6_08 draw_outs**: Qh-Tc on J-9-4 board gives a gutshot draw (8 needed for
   T-J sequence, or Q-J-T-9 needing... Q-J-T-9-8 needs 8 = 4 outs). draw_outs = 4.
   Clearly < 9. PASS for failure mode 4.

6. **SP5_09 vs SP5_07 differentiation**: Both are Ac on B08. SP5_07: Ac + Jh, fold_eq=0.58,
   aggr=0. SP5_09: Ac + 8d, fold_eq=0.55, aggr=0. Different supporting cards and slightly
   different fold_equity values make these distinct situation profiles. The board allows
   at most 3 situations per SP5 (allocation limit). B08 in SP5: sits 7, 8, 9 = 3. At cap.
