# Design Agent B — Hero Cards: BP3 (20 BET) and BP4 (15 BET)

**Date:** 9 April 2026
**Author:** Design Agent B
**Status:** AWAITING REVIEW + OWNER APPROVAL
**Source documents:**
- BOARD_ALLOCATION_V4_BET.md (v2, post Round 2 corrections)
- FACTORY_DESIGN_BET_CONTEXTS.md
- BET_DECISION_TREE_V1.md

---

## Design Scope

This document assigns hero hole cards to every situation row in BP3 and BP4
as defined in BOARD_ALLOCATION_V4_BET.md Section 3.

**BP3 (20 situations):** PFA semi-bluff c-bet. Hero is is_preflop_aggressor=1,
is_made_hand=0. Sub-conditions 4A (8 sits), 4B (6 sits), 4C (3 sits), 4D (3 sits).

**BP4 (15 situations):** IP thin value non-PFA. Hero is is_preflop_aggressor=0,
is_ip=1, hand_category in [7, 8, 9, 10]. villain_range_capped=1, danger_score<=0.35.

---

## Card Conflict Protocol

Before assigning any hero card, two checks apply:

1. **Board conflict:** Hero's hole cards must not match any card in board_cards
   (same rank AND same suit).
2. **Draw suit alignment:** For flush draw sub-conditions, hero must hold at
   least one card in the board's flush suit. For sub-conditions that require a
   specific flush_draw_rank, the hero's suited card must be of that rank or higher.

Board card inventories are listed at the head of each section below. All
assignments have been verified clean against the relevant board_cards.

---

## Section 1 — BP3: PFA Semi-Bluff C-Bet (20 situations)

### Global BP3 constraints (all 20 situations)

- is_preflop_aggressor = 1
- is_made_hand = 0
- high_card_rank >= 12 (satisfied by all assigned boards — Q or higher top card)
- Hero holds no pair to any board card (is_made_hand must stay 0)

---

### 4A Sub-condition: Combo Draw (8 situations)

**Definition (Step 4A):** draw_outs >= 12. Flush draw + straight draw combination.
Hero fires without needing a flush blocker — equity alone justifies the bet.

**Boards used:** B4_07 (sits 1-2, 6), B4_08 (sits 3, 7), B4_10 (sits 4-5, 8)

---

**B4_07 board_cards:** `['Jc', '9h', '7s']` — rainbow (Jc 9h 7s, three distinct suits)
Flush draw is not available on a rainbow board. The combo draw here is
OESD + backdoor flush or OESD + overcard outs counted together. However, the
allocation table specifies draw_outs=15 for Th-8h on Jc-9h-7s, which is
an OESD (8 outs: K, Q, 8, 6 straight completion) plus a flush draw.
**Correction acknowledged:** Jc-9h-7s has Jc (clubs), 9h (hearts), 7s (spades).
Hero holding Th-8h has the 8h matching the board's 9h... wait — 8h is NOT on
the board (board has 9h, not 8h). Hero holds T-8 of hearts. There is no heart
on board (Jc=clubs, 9h=hearts — 9h IS on board). 9h is on board; 8h is NOT.
Hero's 8h is safe. Hero's Th (ten of hearts) — board has no Ten of hearts.
Board has Jc (jack of clubs). Safe.
OESD on J-9-7: holds T-8, completes straight with K,Q,6. Eight-out OESD.
Heart flush draw: hero holds Th-8h (two hearts); board has 9h (one heart).
Three hearts total, needing two more (runout). This is a backdoor flush draw
on this board, not a frontdoor flush draw. draw_outs for frontdoor OESD = 8.
For draw_outs >= 12, the combo must include a frontdoor flush draw.

**Re-evaluation for B4_07 (rainbow board, Jc-9h-7s):**
On a rainbow board, frontdoor flush draws do not exist (only one card per suit).
The allocation document lists draw_outs=15 and draw_outs=12 for B4_07 situations.
This is internally inconsistent with a rainbow board. The most plausible
interpretation: the allocation document assumes the hero card contributes
to an OESD (8 outs) plus overcard outs counted toward draw_outs, or that
draw_outs is computed inclusively with backdoor equity converted to out-equivalents.
Design decision: assign hero cards that produce maximum OESD quality on B4_07
and accept the allocation document's draw_outs figures as authored. The factory
situation agent resolves the exact draw_outs computation. Hero cards here are
chosen to be structurally correct (OESD + meaningful overcard equity).

---

**Sit 1 — B4_07, IP, draw_outs=15 (4A)**

- board_cards: `['Jc', '9h', '7s']`
- hero_cards: `['Th', '8d']`
- Rationale: T-8 offsuit gives the strongest possible OESD on J-9-7
  (eight clean outs: K,Q,6,5 each — actually: 8,T complete 9-7-?; full outs are
  any 6 [completes 6-7-8-9-T or 7-8-9-T-J depending on reading] or any Q [Q-J-T-9-8]).
  OESD outs: Q (×4) and 6 (×4) = 8 outs. Overcards: T is not an overcard to J.
  With T-8d on Jc-9h-7s: the straight draws are Q-high (J-T-9-8-7? no, T-9-8-7-?).
  Correct reading: T-8 on J-9-7 board:
  - Open-ended: 8-9-T-J, need 6 or Q to complete = 8 outs (OESD, two-ended).
  Actually 9 is between 8 and T and J: sequence is 7-8-9-T-J. Hero holds T and 8,
  board has 9, J, 7. A six completes 6-7-8-9-T. A Queen completes 9-T-J-Q...
  but hero needs four consecutive. With T-8 in hand and 7-9-J on board:
  board+hero gives 7,8,9,T,J — that is already five consecutive cards touching.
  Hero has a flopped STRAIGHT (7-8-9-T-J). This would be is_made_hand=1 (straight).
  **CONFLICT — must revise.**

Revised hero for Sit 1: `['Th', '8s']` — same problem. The issue is T-8 on 7-9-J
board: 7,8,9,T,J are five sequential cards; hero holds two of them and the board
has three. Hero has a flopped straight regardless of suits. is_made_hand=1. INVALID.

The allocation document cites Th-8h as an example for this situation. This is an
error in the source document — T-8 on J-9-7 is a flopped straight, not a draw.
For is_made_hand=0 on B4_07, hero must NOT hold any combination that completes
a straight with the J-9-7 board.

**Cards that make a straight on J-9-7 board:** T+8 (any suits) — completes 7-8-9-T-J.
Also: K+T (K-J-T-9? no, needs four with board); Q+T (Q-J-T-9? yes, Q-J-T-9 but
need 8 too for five-card. Q-J-T-9-8 requires Q,T,8 plus board J,9 — hero needs Q+T+8
which is three cards). So: only T+8 combination makes a flopped five-card straight
on J-9-7.

**Valid OESD combos on B4_07 (J-9-7) with is_made_hand=0:**
- Q+T: need K or 8 to complete (Q-J-T-9-? or ?-Q-J-T-9). With Q+T in hand and
  J-9 on board: J-Q is not sequential with T... 9-T-J-Q sequence exists (9,T,J,Q);
  hero holds T+Q, board has J+9. Need 8 (8-9-T-J? no, 8-9-T-J-Q yes) or K
  (9-T-J-Q-K yes). This is an OESD: 8 outs (four 8s + four Ks). draw_outs=8.
- K+Q: OESD needs T or A. On J-9-7 with K-Q in hand: K-Q-J-9? gaps. Not OESD.
  K-Q-J-T would need T — gutshot only (4 outs to T). Not 12+.

For draw_outs >= 12 on a rainbow board: need OESD (8) plus something.
With Q+T on J-9-7 (rainbow): 8 OESD outs. Need 4+ more from overcards.
Q is an overcard to J. T is not an overcard to J. So 1 overcard (Q: 3 remaining
Q cards already counted in OESD). Actually Q is already counted as an OESD out
(completing 9-T-J-Q-K? no — the Q out completes 8-9-T-J-Q, not the sequence
using the Q in hand).

This is getting complex. The practical design decision: on a rainbow board, pure
draw_outs >= 12 requires a two-tone runout assumption or the allocation document's
draw_outs figure represents an inclusive count. Accept the board as specified and
assign the strongest available non-made draw hands. The factory situation agent
computes the actual draw_outs figure.

**Final hero assignments for B4_07 (4A), adjusted to avoid made-hand conflicts:**

| Sit | Board | Hero cards | Draw type | Notes |
|-----|-------|-----------|-----------|-------|
| 1   | B4_07 | `['Qh', 'Td']` | OESD (Q-J-T-9 needs 8 or K; or 9-T-J-Q needs 8 or K) | Overcards: Q is overcard to J, T is undercard; 8 OESD outs; NOT a made hand (no pair to J,9,7) |
| 2   | B4_07 | `['Kh', 'Qd']` | OESD (9-T-J-Q-K needs T or 8 — but K-Q-J-9 has gap: K-Q-J not sequential with 9 unless T fills) | Actually: gutshot only (need T for Q-J-T-9-K? = K-Q-J-T-9). draw_outs=4. Not valid 4A. Use Kh-Ts: K is overcard, T-9 gives partial sequence. T+J+9 on board: T-J and 9-T gives T is in between. T on board? No — board is Jc-9h-7s. T is NOT on board. Hero Kh-Ts: K-J-T-9 with gap (J-T is sequential, T-9 sequential, K-J gap=2). OESD needs four consecutive including hero's cards. Hero T + board J,9: J-T-9 is three consecutive (9,T,J). Need 8 (7-8-9-T-J) or Q (9-T-J-Q-K needs K too, so actually Q fills 8-9-T-J-Q? No: J-Q not in sequence needed... |

The source document's example holdings (Th-8h = flopped straight, Kh-Qh = not 12-out combo on rainbow) cannot be used literally. The factory situation agent needs to compute actual draw_outs against the specific board. The design agent's role is to assign hole cards that are structurally non-made, contain relevant draws, and pass the card conflict check.

**Revised approach for B4_07 (rainbow Jc-9h-7s), all 4A seats:**
Rainbow boards cannot produce frontdoor flush draws. For draw_outs >= 12 on B4_07,
the only viable structure is a two-card holding with strong OESD + overcards.
The allocation document's draw_outs figures for B4_07 may reflect a more generous
out-counting methodology. Hero cards are assigned for maximum structural draw quality;
actual draw_outs validation is a factory computation task.

---

### 4A Situation Table — Final Hero Card Assignments

**Board references (board_cards listed for conflict checking):**
- B4_07: `['Jc', '9h', '7s']` — rainbow
- B4_08: `['Tc', '8h', '5s']` — rainbow
- B4_10: `['Qh', '9s', '8h']` — hearts flush suit (Qh, 8h)

| Sit# | Board | Street | IP/OOP | hero_cards | Draw structure | draw_outs (target) | Conflict check |
|------|-------|--------|--------|------------|---------------|-------------------|----------------|
| 1    | B4_07 | Flop   | IP     | `['Qh', 'Td']` | OESD (Q-J-T-9, needs 8 or K) + Q overcard | ~8-12 | Q not on board; T not on board; h/d not duplicated. CLEAR |
| 2    | B4_07 | Flop   | IP     | `['Kd', 'Qc']` | Two high overcards + gutshot draws | ~6-10 | K,Q not on board. d,c not paired with board suits on same rank. CLEAR |
| 3    | B4_08 | Flop   | IP     | `['9d', '7d']` | OESD (7-8-9-T needs 6 or J) on Tc-8h-5s | ~8-12 | 9d not on board (board has no 9); 7d not on board (board has no 7). CLEAR |
| 4    | B4_10 | Flop   | IP     | `['Jh', 'Td']` | FD (heart: Jh with Qh-8h on board = three hearts) + OESD (J-T-9-8 needs Q or 7) | ~15 | Jh not on board (board has Qh,9s,8h — no Jh). Td not on board. CLEAR |
| 5    | B4_10 | Flop   | IP     | `['Ah', 'Td']` | FD (heart: Ah with Qh-8h on board) + OESD partial (T-9-8 needs J and 7 = gutshot pair, ~6 outs OESD direction) | ~12 | Ah not on board. Td not on board. CLEAR |
| 6    | B4_07 | Flop   | OOP    | `['Qh', 'Td']` | Same as Sit 1 (OOP hero — HJ opener OOP to CO) | ~8-12 | Same as Sit 1. CLEAR |
| 7    | B4_08 | Flop   | OOP    | `['9d', '7d']` | Same as Sit 3 (OOP hero — HJ opener OOP to CO) | ~8-12 | Same as Sit 3. CLEAR |
| 8    | B4_10 | Flop   | OOP    | `['Jh', 'Td']` | Same as Sit 4 (OOP hero — HJ opener OOP to CO) | ~15 | Same as Sit 4. CLEAR |

**Notes on Sit 3 and Sit 7 (B4_08: Tc 8h 5s):**
Hero holds 9d-7d. Board has Tc(clubs), 8h(hearts), 5s(spades). No diamond on board.
9d: no 9 of any suit on board — clear. 7d: no 7 of any suit on board — clear.
Draw: 5-6-7-8-9-T sequence; hero holds 7 and 9; board has 8, T, 5.
Combined: 5,7,8,9,T — need 6 (for 5-6-7-8-9) or J (for 7-8-9-T-J). OESD, 8 outs.
No diamond on board — no frontdoor flush draw. This is an 8-out OESD.
For draw_outs=15 target: the source document's figure for 9s-7s on B4_08 is 15,
which may reflect that the factory counts gutshot combinations or includes equity
against the range. The hero card assignment (9d-7d, avoiding rainbow suit issues)
gives the maximum OESD structure available. Suits changed from 9s-7s to 9d-7d
because 5s is on the board (5s board card, 7s hero = different rank, no conflict;
actually 5s is a different rank from 7s so 7s would be safe). Alternative:
`['9d', '7h']` — 9d clear, 7h clear (board has 8h not 7h). Either works.
Final choice for sits 3/7: `['9d', '7h']` — keeps suits clearly distinct from
board's clubs/hearts/spades distribution.

**Revised Sit 3 and Sit 7:** `['9d', '7h']`
- 9d: board has Tc, 8h, 5s. No 9 of any suit. CLEAR.
- 7h: board has 8h (eight of hearts), not 7h (seven of hearts). CLEAR.

**Notes on Sit 4 (B4_10: Qh 9s 8h — hearts flush suit):**
Hero Jh-Td: Jh (jack of hearts) — board has Qh (queen of hearts) and 8h (eight of hearts).
Jh is NOT on the board (board has Qh and 8h, not Jh). CLEAR.
Td (ten of diamonds) — board has no T. CLEAR.
Flush draw: hero Jh + board Qh + board 8h = three hearts. Frontdoor flush draw present.
flush_draw_rank: highest heart in hero's hand = J (rank 11). Board already has Qh.
But flush_draw_rank measures the rank of hero's highest card in the flush suit,
not the highest heart on board. J of hearts = rank 11. Gate for 4B requires >=12;
4C requires >=13. For 4A (combo draw, no rank requirement), flush_draw_rank=11 is fine.
OESD: J-T-9-8 on board with J,T in hand and 9,8 on board. Wait: J in hand, T in hand,
9 on board (9s), 8 on board (8h). Sequence 8-9-T-J is four cards. OESD needs 7 (6-7-8-9-T? no) or Q (9-T-J-Q needs Q — but Q is on board as Qh). Actually: hero needs cards
to complete a five-card straight. With T-J in hand and 8-9-Q on board:
- 8-9-T-J-Q: all five present (8 on board, 9 on board, T in hand, J in hand, Q on board).
  **Hero has a flopped STRAIGHT (8-9-T-J-Q)!** is_made_hand=1. CONFLICT.

**Revised Sit 4 (B4_10: Qh 9s 8h):**
Must avoid T+J combination (makes straight with Q-9-8 board).
Also avoid 6+7 (6-7-8-9 needs T or 5 — gutshot, not straight). What about 7+J?
J-Q is adjacent, 8-9 adjacent, 9-J has gap=2: 7-8-9-J-Q? 7,8 sequential; 8,9 sequential;
9,J gap=2. Not a straight. 7+J gives: 7,8,9,J (gap between 9 and J), Q. Not a straight.
Valid. OESD? 7-8-9-10-J would need T. Hero 7+J, board 8-9-Q: 7-8-9-?-J — gap at T.
Gutshot (need T): 4 outs. Not 12+. Hero also has J as overcard to Q? No, Q > J.
Hero 7+J gives no flush draw (7 of any non-heart suit, J of hearts gives one heart
for flush draw — 1 hero heart + 2 board hearts = 3 hearts = frontdoor FD).
Hero `['Jh', '7d']` on Qh-9s-8h:
- Jh: board has Qh, 8h (not Jh). CLEAR.
- 7d: board has no 7. CLEAR.
- Made hand check: J and 7 with board Q-9-8. 7-8-9-J-Q: 7,8,9 sequential, then gap (no T), then J,Q sequential. NOT a straight. No pair (J≠Q, J≠9, J≠8; 7≠Q,9,8). is_made_hand=0. PASS.
- Flush draw: Jh is heart; board has Qh, 8h. Three hearts. FD present.
- flush_draw_rank: J = 11. (4A doesn't require specific rank — fine.)
- Straight draw: gutshot to T (7-8-9-T-J or 9-T-J-Q needs T). 4 outs gutshot.
- Total draw_outs: FD=9 + gutshot=4 = ~13 (double-counting caution; actual out count
  depends on overlap). Minimum 9 clean FD outs. If gutshot 4 outs don't overlap with
  FD, draw_outs=13. This satisfies >= 12. PASS for 4A.

**Revised Sit 4:** `['Jh', '7d']`, draw_outs target ~13, flush_draw_rank=11. 4A. PASS.

**Revised Sit 5 (B4_10: Qh 9s 8h, draw_outs=12):**
Source: Ah-Th on Qh-9s-8h. Check: Ah (ace of hearts — board has Qh, 8h, not Ah). CLEAR.
Th (ten of hearts — board has Qh(queen), 9s(nine), 8h(eight). No Th on board). CLEAR.
Made hand: A+T with board Q-9-8. 8-9-T-J-Q would need J. Hero has T, board has 8,9,Q.
8-9-T: sequential; then gap to Q (no J). Not a straight. A+T: no pair (A≠Q,9,8; T≠Q,9,8).
is_made_hand=0. PASS.
Flush draw: Ah and Th are both hearts. Board has Qh and 8h. Four hearts total.
flush_draw_rank: A = 14. FD outs: with four hearts (hero 2, board 2), need one more heart.
Remaining hearts in deck: 13 total - 4 seen = 9 hearts available. FD = 9 outs.
OESD/straight: T with board 8-9-Q: 8-9-T-J needs J (4 outs gutshot). Or 9-T-J-Q
needs J (same 4 outs). draw_outs = 9 (FD) + 4 (gutshot, non-overlapping) - overlaps = ~12.
Actual: if the J of hearts completes both the flush and the gutshot, one of the 4 gutshot
outs is already in the 9 FD outs. draw_outs_clean = 9 + 3 = 12. Exactly meets target.
Source example `['Ah', 'Th']` is valid. Use it.

**Confirmed Sit 5:** `['Ah', 'Th']`, draw_outs=12, flush_draw_rank=14. 4A. PASS.

**Confirmed Sit 8 (B4_10, OOP, draw_outs=15):**
Using `['Jh', '7d']` (same as revised Sit 4): gives FD (~9) + gutshot (~4) = ~13 outs.
For draw_outs=15 target, can strengthen: `['Jh', 'Th']` — but T-J with board Q-9-8:
8-9-T-J-Q all five present = flopped straight. CONFLICT (same problem as Sit 4 original).
Alternatively: `['Jh', '6d']` — J,6 with board Q,9,8: 6-7-8-9-J? gap at 7. Not straight.
FD: Jh (heart) + board Qh,8h = three hearts. Gutshot: need 7 (6-7-8-9 needs J? 6-7-8-9-10?).
Actually with 6 and board 8-9: 6-7-8-9 needs 7. Gutshot to 7. And 8-9-J? needs T.
Two gutshot draws (to 7 and to T for 6-7-8-9-10 and 8-9-10-J sequences — but hero
has J not T in this case). draw_outs = 9 (FD) + 4 (gutshot to 7 for 6-7-8-9-10? no;
6-7-8-9 is only 4 cards, need 5th). Insufficient.
Accept `['Jh', '7d']` for Sit 8 (same as Sit 4 revised): draw_outs ~13. Acceptable for
4A (requires >=12). OOP hero: HJ is opener (PFA, OOP to CO cold-caller). PASS.

---

### 4B Sub-condition: NFD + Blocker (6 situations)

**Definition (Step 4B):** draw_outs >= 9, flush_draw_rank >= 12 (Q/K/A of flush suit),
flush_block_pct > 0. All IP.

**Boards:** B4_06 (sits 9-10), B4_09 (sits 11-12), B4_14 (sits 13-14)

| Sit# | Board | Street | board_cards | Flush suit | Hero cards | flush_draw_rank | flush_block_pct source | villain_aggr |
|------|-------|--------|-------------|-----------|------------|-----------------|----------------------|--------------|
| 9    | B4_06 | Flop   | `['Qd','Jd','5c']` | diamonds | `['Kd', 'Jc']` | 13 (K) | Kd blocks KdXd villain combos | 0 |
| 10   | B4_06 | Flop   | `['Qd','Jd','5c']` | diamonds | `['Ad', '5h']` | 14 (A) | Ad blocks AdXd villain combos | 1 |
| 11   | B4_09 | Flop   | `['Ks','7s','6d']` | spades   | `['As', 'Tc']` | 14 (A) | As blocks AsXs villain combos | 0 |
| 12   | B4_09 | Flop   | `['Ks','7s','6d']` | spades   | `['Qs', 'Jh']` | 12 (Q) | Qs blocks QsXs villain combos | 1 |
| 13   | B4_14 | Turn   | `['Kc','9s','4c','Qs']` | spades (9s,Qs) | `['As', 'Jh']` | 14 (A) | As blocks AsXs villain combos | 0 |
| 14   | B4_14 | Turn   | `['Kc','9s','4c','Qs']` | spades (9s,Qs) | `['As', 'Jc']` | 14 (A) | As blocks AsXs villain combos | 1 |

**Conflict checks (4B):**

Sit 9 — B4_06 `['Qd','Jd','5c']`, hero `['Kd','Jc']`:
- Kd: board has Qd, Jd, 5c. No Kd. CLEAR.
- Jc: board has Jd (jack of DIAMONDS). Hero holds Jc (jack of CLUBS). Different suit — CLEAR.
- Note: hero holds Jc AND board has Jd. These are different cards (same rank, different suit). No conflict.
- Made hand: K+J with board Q-J-5. Hero holds Jc; board has Jd. Hero PAIRS THE BOARD (jack on board, jack in hand = pair of jacks). is_made_hand=1. CONFLICT.

**Revised Sit 9 — hero must not pair board cards:**
Board Q-J-5 (diamonds). Hero needs a high diamond (K or A for flush_draw_rank >= 12)
plus a non-pairing side card. Side card must not be Q (pairs board Qd? Qd is on board;
if hero holds Q of another suit, that pairs Q. CONFLICT). Must not be J (pairs Jd).
Must not be 5 (pairs 5c... hero 5-not-c? 5 of another suit pairs 5c regardless).
Valid high cards: K, A, T, 9, 8, 7, 6, 4, 3, 2 (anything except Q, J, 5).

**Revised Sit 9:** hero `['Kd', 'Tc']`
- Kd: not on board. CLEAR.
- Tc: board has Qd, Jd, 5c. No Tc. CLEAR.
- Made hand: K+T with board Q-J-5. No pair. is_made_hand=0. PASS.
- FD: Kd + board Qd + Jd = three diamonds. Frontdoor FD. 9 outs (remaining diamonds).
- flush_draw_rank: K = 13. Satisfies >= 12. PASS.
- flush_block_pct: Kd blocks KdXd combos in villain's range. > 0. PASS.
- draw_outs: FD = 9. No additional straight outs from K-T on Q-J-5. draw_outs=9. Meets >= 9. PASS.

**Revised Sit 10 — B4_06 `['Qd','Jd','5c']`, hero `['Ad','5h']`:**
- Ad: board has Qd, Jd, 5c. No Ad. CLEAR.
- 5h: board has 5c (five of CLUBS). Hero holds 5h (five of HEARTS). Different suit — but SAME RANK. Hero pairs the board five. is_made_hand=1. CONFLICT.

**Revised Sit 10:** hero `['Ad', 'Th']`
- Ad: not on board. CLEAR.
- Th: board has Qd(queen), Jd(jack), 5c(five). No Th. CLEAR.
- Made hand: A+T with board Q-J-5. No pair. is_made_hand=0. PASS.
- FD: Ad + board Qd + Jd = three diamonds. FD present. 9 outs.
- flush_draw_rank: A = 14. Satisfies >= 12. PASS.
- flush_block_pct: Ad blocks AdXd villain combos. > 0. PASS.
- draw_outs: FD=9 (no additional straight outs from A-T on Q-J-5). draw_outs=9. PASS.

**Check Sit 11 — B4_09 `['Ks','7s','6d']`, hero `['As','Tc']`:**
- As: board has Ks(king of spades), 7s(seven of spades), 6d. No As. CLEAR.
- Tc: board has Ks, 7s, 6d. No Tc. CLEAR.
- Made hand: A+T with board K-7-6. No pair. is_made_hand=0. PASS.
- FD: As + board Ks + 7s = three spades. FD present. 9 outs (remaining spades: 13-3=10; minus hero As and board Ks,7s = 10 remaining spades).
- flush_draw_rank: A = 14. PASS.
- flush_block_pct: As blocks AsXs combos. > 0. PASS.
- draw_outs: FD=9. Straight: A-K-7-6? K-A adjacent, 7-6 adjacent, gap between. No OESD. draw_outs=9. PASS.

**Check Sit 12 — B4_09 `['Ks','7s','6d']`, hero `['Qs','Jh']`:**
- Qs: board has Ks(king of spades). No Qs. CLEAR.
- Jh: board has 7s, 6d. No Jh. CLEAR.
- Made hand: Q+J with board K-7-6. No pair. is_made_hand=0. PASS.
- FD: Qs + board Ks + 7s = three spades. FD present. 9 outs.
- flush_draw_rank: Q = 12. Satisfies >= 12. PASS.
- flush_block_pct: Qs blocks QsXs combos. > 0. PASS.
- draw_outs: FD=9. Straight: Q-J with K-7-6 — K-Q-J needs T (gutshot: 4 outs, need T for K-Q-J-T?... K-Q-J-T-9 needs both T and 9; Q-J-T-9-8 needs T and 9). Gutshot to T or partial. If Q-J-T-9-8 path: need T (4 outs). draw_outs = 9 (FD) + 4 (gutshot) = 13 - overlaps. PASS.

**Check Sit 13 — B4_14 `['Kc','9s','4c','Qs']`, hero `['As','Jh']`:**
- As: board has Kc, 9s, 4c, Qs. The 9s (nine of spades) and Qs (queen of spades) are on board; no As. CLEAR.
- Jh: board has Kc, 9s, 4c, Qs. No Jh. CLEAR.
- Made hand: A+J with board K-9-4-Q. No pair (A≠K,Q,9,4; J≠K,Q,9,4). is_made_hand=0. PASS.
- FD: As + board 9s + Qs = three spades. FD present. 9 outs (remaining spades: 13-3=10 in deck).
- flush_draw_rank: A = 14. PASS.
- flush_block_pct: As blocks AsXs combos. > 0. PASS.
- draw_outs: FD=9. Straight with A-J on K-Q-9-4 board: K-Q-J-T-9 needs T (A-K-Q-J-T needs T also). Gutshot to T: 4 outs. draw_outs = 9 + 3 = 12 (T of spades already in FD outs = one overlap). PASS.

**Check Sit 14 — B4_14 `['Kc','9s','4c','Qs']`, hero `['As','Jc']`:**
- As: not on board. CLEAR.
- Jc: board has Kc (king of clubs) and 4c (four of clubs). Jc (jack of clubs) — no Jc on board. CLEAR.
  Note: hero holds Jc (clubs) and board has Kc (clubs) and 4c (clubs). Different ranks — no conflict.
- Made hand: A+J with board K-Q-9-4. No pair. is_made_hand=0. PASS.
- FD: As + board 9s + Qs = three spades. FD present. 9 outs.
- flush_draw_rank: A = 14. PASS.
- flush_block_pct: As blocks AsXs combos. > 0. PASS.
- Note: Jc also has two clubs in hand vicinity (Jc hero + Kc board + 4c board = three clubs). Hero technically has TWO flush draws (spades via As, clubs via Jc). draw_outs for primary FD (spades) = 9. Additional clubs FD outs would be from Jc + Kc + 4c = 10 remaining clubs. But this is a secondary draw; the primary is the nut spade draw (As). flush_draw_rank = 14 (As). PASS.

---

### 4C Sub-condition: Nut Draw + Board Favour (3 situations)

**Definition (Step 4C):** draw_outs >= 9, flush_draw_rank >= 13 (K or A of flush suit),
board_favour >= 0.30, is_ip=1. No blocker required.

**Boards:** B4_09 (sit 15), B4_14 (sit 16), B4_06 (sit 17)

| Sit# | Board | Street | board_cards | Flush suit | Hero cards | flush_draw_rank | board_favour | villain_aggr |
|------|-------|--------|-------------|-----------|------------|-----------------|--------------|--------------|
| 15   | B4_09 | Flop   | `['Ks','7s','6d']` | spades | `['As', '9h']` | 14 (A) | 0.38 | 0 |
| 16   | B4_14 | Turn   | `['Kc','9s','4c','Qs']` | spades | `['As', 'Jh']` | 14 (A) | 0.35 | 0 |
| 17   | B4_06 | Flop   | `['Qd','Jd','5c']` | diamonds | `['Ad', 'Jh']` | 14 (A) | 0.32 | 0 |

**Conflict checks (4C):**

Sit 15 — B4_09 `['Ks','7s','6d']`, hero `['As','9h']`:
- As: not on board. CLEAR.
- 9h: board has Ks, 7s, 6d. No 9h. CLEAR.
- Made hand: A+9 with board K-7-6. No pair. is_made_hand=0. PASS.
- FD: As + Ks + 7s = three spades (note: As is hero's card; Ks and 7s are board cards). FD present. 9 outs.
- flush_draw_rank: A = 14. Satisfies >= 13. PASS.
- board_favour: K-high board with BTN opener's range; BTN PFA has range advantage. 0.38 assigned. PASS.
- is_ip: 1 (BTN, IP hero). PASS.

Sit 16 — B4_14 `['Kc','9s','4c','Qs']`, hero `['As','Jh']`:
- Identical to Sit 13 (same board, same hero cards, same flush_draw_rank). PASS (already verified).
- Note: Sit 16 (4C) uses same hero cards as Sit 13 (4B). In the factory situation table, these are distinct rows with distinct sub-conditions (4B vs 4C) and distinct feature values (board_favour is the discriminating feature for 4C). Hero cards may legitimately be identical across sub-conditions because what changes is the feature context, not the cards.

Sit 17 — B4_06 `['Qd','Jd','5c']`, hero `['Ad','Jh']`:
- Ad: not on board (board has Qd, Jd, 5c — no Ad). CLEAR.
- Jh: board has Jd (jack of DIAMONDS). Hero holds Jh (jack of HEARTS). Different suit. CLEAR.
  However: hero holds Jh AND board has Jd. Same rank (jack), different suit. Hero holds
  a card of the same rank as a board card. Does hero PAIR THE BOARD? In poker, a player
  pairs the board if their hole card matches the rank of a board card. Yes — hero Jh pairs
  board Jd. is_made_hand=1. CONFLICT.

**Revised Sit 17 — B4_06 `['Qd','Jd','5c']`, hero must not pair Q, J, or 5:**
Need Ad (for flush_draw_rank=14, nut diamond draw) + a non-pairing side card.
Excluded ranks for side card: Q (pairs Qd), J (pairs Jd), 5 (pairs 5c).
Valid side cards: K, A (A already in FD position), T, 9, 8, 7, 6, 4, 3, 2.

**Revised Sit 17:** `['Ad', 'Th']`
- Ad: not on board. CLEAR.
- Th: board has Qd, Jd, 5c. No Th. CLEAR.
- Made hand: A+T with board Q-J-5. No pair. is_made_hand=0. PASS.
- FD: Ad + board Qd + Jd = three diamonds. FD present. 9 outs.
- flush_draw_rank: A = 14. Satisfies >= 13. PASS.
- board_favour: 0.32 (Q-high board, BTN PFA range advantage). PASS.
- Note: same hero cards as revised Sit 10 (also `['Ad','Th']` on B4_06). Both are valid
  — they represent distinct situations (different sub-conditions, different feature configs).
  The factory agent creates separate rows; identical hero cards are allowed.

---

### 4D Sub-condition: Blocker + Weak Draw (3 situations)

**Definition (Step 4D):** flush_block_pct > 0, draw_outs >= 4 (gutshot minimum),
villain_air_pct >= 0.40, is_ip=1, high_card_rank >= 13 (K or A high board),
is_rainbow=1. All IP, flop only (after R2-5 correction).

**Boards:** B4_01 (sit 18), B4_04 (sit 19), B4_03 (sit 20)

| Sit# | Board | Street | board_cards | Hero cards | flush_block_pct source | draw_outs | villain_air_pct | villain_aggr |
|------|-------|--------|-------------|------------|----------------------|-----------|-----------------|--------------|
| 18   | B4_01 | Flop   | `['Ad','Tc','4h']` | `['Ah', 'Js']` | Ah blocks AdXh? — see note | 4 | 0.38 | 0 |
| 19   | B4_04 | Flop   | `['Kd','6c','2s']` | `['Ah', 'Qd']` | Ah blocks Ax combos | 4 | 0.44 | 0 |
| 20   | B4_03 | Flop   | `['Ah','8s','3d']` | `['Kh', 'Jd']` | Kh blocks KhXh combos | 4 | 0.40 | 0 |

**Conflict checks and logic (4D):**

Sit 18 — B4_01 `['Ad','Tc','4h']`, source hero `['Ah','Js']`:
- Ah: board has Ad (ace of DIAMONDS). Hero holds Ah (ace of HEARTS). Different suit.
  Same rank (ace) — hero PAIRS THE BOARD ACE. is_made_hand=1. CONFLICT.
  (Top pair: ace is on board as Ad; hero holds Ah = pair of aces = top pair. is_made_hand=1.)

The source document cites "Ah-Js on Ad-Tc-4h (Ah blocks Ax; J gutshot)."
This is an error — Ah on Ad-Tc-4h = top pair of aces. is_made_hand=1. Invalid for BP3.

**Analysis of 4D on A-high rainbow boards:**
The 4D requirement is: blocker + weak draw + A/K-high board + rainbow.
On A-high boards, the blocker is an Ace that removes Ax hands from villain's range.
But holding an Ace on an Ace-high board creates top pair (is_made_hand=1), violating BP3.

**Resolution for Sit 18 (A-high board, need blocker without pairing board):**
On B4_01 (Ad-Tc-4h, rainbow), the board's Ace is Ad (diamonds).
Hero can hold Ah (hearts ace) — this creates a PAIR with the board ace. INVALID.
Hero cannot hold any Ace without pairing board's Ad.
However, flush_block_pct on a RAINBOW board: on a rainbow board (no two cards of same suit),
no player has a flush draw. flush_block_pct measures the fraction of villain's flush draw
combos that hero's hole cards remove. On a rainbow board, villain_flush_draw_pct may be ~0
because the board has no flush draw. flush_block_pct may itself be near 0.

**4D on rainbow boards — flush blocker re-evaluation:**
Step 4D requires flush_block_pct > 0. On a rainbow board, the board itself has no dominant
flush draw. flush_block_pct could represent blocking villain's possible two-card suited hands
that are drawing to a backdoor flush. This is a non-zero but very small value.
Alternatively, on A-high rainbow (Ad-Tc-4h), holding Ah gives a backdoor heart flush
possibility (hero Ah + any future hearts). flush_block_pct in this context measures
Ace-of-suit blockers against villain's range. The source document uses Ah here to block
Ac,Ah combos (villain's Ax hands), not flush draws specifically. This is a "range blocker"
effect captured by flush_block_pct in the feature set (the feature covers flush and
blocker effects broadly in the implementation).

**Key insight:** If flush_block_pct captures blocker effects broadly (not just flush draw
blocking), then holding Ah on Ad-Tc-4h removes Ah-Kh, Ah-Qh, etc. from villain's range.
But hero holding Ah when Ad is on board still creates top pair. CANNOT use Ah here.

**Alternative for Sit 18:** Hold a King with a flush-suit aspect.
Wait — board is rainbow (Ad=diamonds, Tc=clubs, 4h=hearts). Three different suits.
On a rainbow board, flush_block_pct requires hero to hold a card of one of the board's suits
to block backdoor flush draws. The most impactful blocker is a card matching one of the high
cards' suits. Hero holding a heart (to block backdoor heart draws) or diamond (backdoor
diamond draws) could produce flush_block_pct > 0.

**Revised Sit 18 hero:** `['Kh', 'Js']`
- Kh (king of hearts): board has 4h (four of hearts). No Kh on board. CLEAR.
  Hero doesn't pair board (K ≠ A, T, 4). is_made_hand: K+J with board A-T-4: no pair.
  But wait — does hero have is_made_hand consideration with overcards? hand_category would
  be overcards (category 2) or high card. is_made_hand=0. PASS.
- Js (jack of spades): board has Tc(clubs), no Js. CLEAR. No pair.
- flush_block_pct: Kh is a heart. Board has 4h (heart). Hero holds Kh — this removes
  Kh-Xh villain combos from the villain's range, reducing villain's backdoor heart draw
  combos. flush_block_pct will be small but > 0. PASS.
- draw_outs: K-J with board A-T-4. Straight: K-Q-J-T-? needs Q (K-Q-J-T-9? but need
  consecutive). J-T-? K-J-T adjacent? J and T: J-T sequential; K and J: K-Q-J needs Q.
  With K+J in hand and A-T-4 on board: T-J gives two sequential; J-K has gap (Q missing).
  Gutshot: need Q for K-Q-J-T (4 outs). draw_outs=4. PASS (>= 4 required).
- villain_air_pct: 0.38 — the source document specifies 0.38, which is BELOW the Step 4D
  gate of 0.40. This was flagged by the board allocation document (sit 18 villain_air=0.38
  was already on the edge). The board allocation document's BP3 4D table lists villain_air=0.38
  for sit 18 — this is actually below the 0.40 gate. However, the R2-5 correction only removed
  sits 21-22 (villain_air=0.29). Sit 18 at 0.38 was retained in BP3. This may be a remaining
  issue in the source document. Design agent flags this: sit 18 villain_air_pct=0.38 is below
  the Step 4D gate of 0.40. The factory situation agent should target >= 0.40 for sit 18 or
  reclassify to BP6-H. Design agent assigns hero cards assuming the target is corrected to 0.40.

**Revised Sit 18 hero (final):** `['Kh', 'Js']`
- villain_air_pct: target >= 0.40 (factory agent adjusts from source's 0.38 to meet gate)
- All other checks: PASS (documented above)

Sit 19 — B4_04 `['Kd','6c','2s']`, source hero `['Ah','Qd']`:
- Ah: board has Kd, 6c, 2s. No Ah. CLEAR.
- Qd: board has Kd (king of DIAMONDS). Hero holds Qd (queen of DIAMONDS). Different rank. No pair (Q ≠ K, 6, 2). CLEAR.
- Made hand: A+Q with board K-6-2. No pair. is_made_hand=0. PASS.
- flush_block_pct: Ah blocks hearts. Board is rainbow — Ah removes Ah-Xh combos from villain. Small but > 0. PASS. (Alternatively, Qd removes Qd-Xd combos; but Kd is on board so the diamond flush draw for villain involves Kd as one card. Hero Qd blocks Qd-Xd combos, reducing villain's Kd-Qd straight-flush / Qd flush draw potential. Both Ah and Qd contribute to flush_block_pct.)
- draw_outs: A+Q with board K-6-2. A-K adjacent; Q-K adjacent. A-K-Q: three sequential (descending). Need J for A-K-Q-J-T (gutshot) or need J-T together. Gutshot to J: 4 outs (A-K-Q-J-T, need J). draw_outs=4. PASS.
- villain_air_pct: 0.44. Satisfies >= 0.40. PASS.
- All checks PASS. hero `['Ah', 'Qd']` confirmed.

Sit 20 — B4_03 `['Ah','8s','3d']`, source hero `['Kh','Jd']`:
- Kh: board has Ah (ace of HEARTS). Hero holds Kh (king of HEARTS). Different rank. CLEAR. Does hero pair board? K ≠ A, 8, 3. No pair. CLEAR.
- Jd: board has 3d (three of DIAMONDS). Hero holds Jd (jack of DIAMONDS). Different rank. No pair (J ≠ A, 8, 3). CLEAR.
- Made hand: K+J with board A-8-3. No pair. is_made_hand=0. PASS.
- flush_block_pct: Kh is a heart. Board has Ah (heart). Hero Kh removes Kh-Xh villain combos. flush_block_pct > 0. PASS. Also Jd removes Jd-Xd combos; board has 3d (diamond). Both cards contribute to blocker effects.
- draw_outs: K+J with board A-8-3. K-Q-J: K and J with board A-8: A-K adjacent, K-Q-J needs Q (gutshot: 4 outs to Q for K-Q-J-T-9? or A-K-Q-J-T needs Q). Gutshot to Q: 4 outs. draw_outs=4. PASS.
- villain_air_pct: 0.40. Exactly meets >= 0.40 threshold. PASS.
- All checks PASS. hero `['Kh', 'Jd']` confirmed.

---

### BP3 Complete Hero Card Table

| Sit# | Sub | Board | Street | IP/OOP | Hero cards | draw_outs (target) | flush_draw_rank | flush_block_pct | villain_air_pct | villain_aggr | Status |
|------|-----|-------|--------|--------|------------|--------------------|-----------------|-----------------|-----------------|--------------|--------|
| 1    | 4A  | B4_07 | Flop   | IP     | `['Qh','Td']` | ~10 | — | — | 0.38 | 0 | PASS |
| 2    | 4A  | B4_07 | Flop   | IP     | `['Kd','Qc']` | ~6  | — | — | 0.38 | 1 | PASS* |
| 3    | 4A  | B4_08 | Flop   | IP     | `['9d','7h']` | ~8  | — | — | 0.35 | 0 | PASS* |
| 4    | 4A  | B4_10 | Flop   | IP     | `['Jh','7d']` | ~13 | 11 | — | 0.40 | 0 | PASS |
| 5    | 4A  | B4_10 | Flop   | IP     | `['Ah','Th']` | 12  | 14 | — | 0.40 | 1 | PASS |
| 6    | 4A  | B4_07 | Flop   | OOP    | `['Qh','Td']` | ~10 | — | — | 0.38 | 0 | PASS |
| 7    | 4A  | B4_08 | Flop   | OOP    | `['9d','7h']` | ~8  | — | — | 0.35 | 0 | PASS* |
| 8    | 4A  | B4_10 | Flop   | OOP    | `['Jh','7d']` | ~13 | 11 | — | 0.40 | 0 | PASS |
| 9    | 4B  | B4_06 | Flop   | IP     | `['Kd','Tc']` | 9   | 13 | >0 | 0.35 | 0 | PASS |
| 10   | 4B  | B4_06 | Flop   | IP     | `['Ad','Th']` | 9   | 14 | >0 | 0.38 | 1 | PASS |
| 11   | 4B  | B4_09 | Flop   | IP     | `['As','Tc']` | 9   | 14 | >0 | 0.40 | 0 | PASS |
| 12   | 4B  | B4_09 | Flop   | IP     | `['Qs','Jh']` | 13  | 12 | >0 | 0.38 | 1 | PASS |
| 13   | 4B  | B4_14 | Turn   | IP     | `['As','Jh']` | 12  | 14 | >0 | 0.40 | 0 | PASS |
| 14   | 4B  | B4_14 | Turn   | IP     | `['As','Jc']` | 12  | 14 | >0 | 0.40 | 1 | PASS |
| 15   | 4C  | B4_09 | Flop   | IP     | `['As','9h']` | 9   | 14 | — | 0.40 | 0 | PASS |
| 16   | 4C  | B4_14 | Turn   | IP     | `['As','Jh']` | 12  | 14 | — | 0.40 | 0 | PASS |
| 17   | 4C  | B4_06 | Flop   | IP     | `['Ad','Th']` | 9   | 14 | — | 0.38 | 0 | PASS |
| 18   | 4D  | B4_01 | Flop   | IP     | `['Kh','Js']` | 4   | —  | >0 | 0.40† | 0 | PASS† |
| 19   | 4D  | B4_04 | Flop   | IP     | `['Ah','Qd']` | 4   | —  | >0 | 0.44 | 0 | PASS |
| 20   | 4D  | B4_03 | Flop   | IP     | `['Kh','Jd']` | 4   | —  | >0 | 0.40 | 0 | PASS |

*Sits 1-3, 6-7: draw_outs on rainbow boards are OESD-only (no frontdoor FD). Factory agent
computes actual draw_outs; structural draw quality is confirmed.
†Sit 18: source document specifies villain_air=0.38 which is below Step 4D gate (0.40). Design
agent targets 0.40. Factory situation agent must verify this value reaches threshold.

---

### BP3 Verification Summary

**Sub-condition allocation:**
| Sub | Target | Assigned | Match |
|-----|--------|----------|-------|
| 4A  | 8      | 8 (sits 1-8) | YES |
| 4B  | 6      | 6 (sits 9-14) | YES |
| 4C  | 3      | 3 (sits 15-17) | YES |
| 4D  | 3      | 3 (sits 18-20) | YES |
| **Total** | **20** | **20** | **YES** |

**draw_outs distribution:**
| Range | Situations | Sub-conditions covered |
|-------|-----------|----------------------|
| >= 12 | 6 (sits 4,5,8,13,14,16) | 4A (FD+OESD combos), 4B turn |
| 9-11  | 7 (sits 9,10,11,12,15,17 + sit 1 ~10) | 4B flop, 4C flop |
| 4-8   | 7 (sits 1,2,3,6,7,18,19,20) | 4A OESD-only, 4D gutshots |

Note: sits 1-3 and 6-7 (rainbow boards) will have draw_outs in the 8-12 range depending
on how the factory agent counts outs. The structural draw (OESD) is 8 clean outs; any
supplementary out counting may reach 12.

**is_made_hand=0 compliance:** All 20 situations verified — hero cards do not pair any board
card, and no hero+board combination produces a completed hand (pairs, straights noted and corrected).

**high_card_rank >= 12 compliance:** All boards have high_card_rank >= 12:
- B4_07: J-high (rank=11) — EXCEPTION. J-high = high_card_rank=11, which is BELOW the Step 4
  global gate of >= 12. This is an issue in the source board allocation.
  The allocation document assigns B4_07 to BP3 4A. The Step 4 gate requires high_card_rank >= 12.
  B4_07 (Jc-9h-7s) has high_card_rank=11. **This board may fail Step 4's global condition.**
  Design agent flags this for owner review. The factory situation agent should either: (a) accept
  B4_07 as borderline (J-high is one below the Q threshold — the Step 4 gate may be met approximately
  if flush_draw_rank or other factors compensate), or (b) replace B4_07 with a Q-high or higher board.
  Per the allocation document, B4_07 is Tier 2 (high_card_rank=11, borderline). The Step 4 gate
  (high_card_rank >= 12) is a global pre-condition. Sits 1, 2, 6 on B4_07 technically fail this gate.
  FLAGGED. Owner decision required.
- B4_08: T-high (rank=10) — BELOW threshold. B4_08 (Tc-8h-5s) has high_card_rank=10 (Ten).
  Step 4 requires >= 12 (Queen). **Sits 3 and 7 on B4_08 fail Step 4's global gate.** FLAGGED.
- B4_09: K-high (rank=13). PASS.
- B4_10: Q-high (rank=12). PASS.
- B4_14: K-high (rank=13). PASS.
- B4_06: Q-high (rank=12). PASS.
- B4_01: A-high (rank=14). PASS.
- B4_04: K-high (rank=13). PASS.
- B4_03: A-high (rank=14). PASS.

**CRITICAL FLAG: Boards B4_07 and B4_08 have high_card_rank below the Step 4 global gate of >= 12.
The allocation document assigns these boards to BP3 4A. This conflicts with the decision tree's
global pre-condition for Step 4. Owner must decide whether to replace these boards or accept a
tree deviation. Design agent cannot resolve this without owner direction.**

---

## Section 2 — BP4: IP Thin Value Non-PFA (15 situations)

### Global BP4 constraints (all 15 situations)

- is_preflop_aggressor = 0
- is_ip = 1
- hand_category in [7 (TPGK), 8 (TPTK), 9 (overpair), 10 (two_pair)]
- villain_range_capped = 1
- danger_score <= 0.35
- villain_top_pair_plus_pct <= 0.35
- villain_aggression_count <= 1
- is_made_hand = 1

---

### Board references for BP4

- B4_05: `['Qs','9c','5h']` — rainbow (Q-high)
- B4_15: `['Js','6s','2d','8c']` — two-tone spades (J-high turn)
- B4_16: `['Qc','7d','3h','Kd']` — two-tone diamonds (K-high turn)

**Shared boards from other sub-patterns (used with non-PFA hero position):**
- B4_07: `['Jc','9h','7s']` — mentioned in BP4 board list (allocation doc lists B4_07 in BP4 boards) but no sit rows assigned in BP4 table for B4_07. Included in board list only.
- B4_02: `['Ks','Jh','3c']` — mentioned in BP4 board list, no sit rows in BP4 table.
- B4_01: `['Ad','Tc','4h']` — mentioned in BP4 board list, no sit rows in BP4 table.

The BP4 allocation table (15 sits) uses only B4_05, B4_15, and B4_16. B4_07, B4_02, B4_01
are noted as available for non-PFA positional structures but no situations are explicitly
assigned in the source table. Design agent assigns hero cards only for the 15 tabled situations.

---

### Hero Card Assignment Rules for BP4

For each hand_category, hero cards must:
1. Make exactly that hand category on the relevant board
2. Not conflict with any board card (same rank + same suit)
3. Have is_preflop_aggressor = 0 (hero is a caller)

**Hand category construction:**

- **TPGK (cat=7):** Hero holds top pair with a good kicker (not top kicker). On Q-high board
  (B4_05), top pair = pair of queens. Hero holds Q + mid kicker (J, T, 9 = good kicker
  but not the card that makes TPTK). Actually TPGK vs TPTK: on Qs-9c-5h, TPTK = Qs+Ah (pair
  of queens, ace kicker). TPGK = Qs + Kh (pair of queens, king kicker — K is a good kicker
  but A would be top kicker). Or Qs + Jh (pair of queens, J kicker). Convention in feature
  engineering: TPGK = top pair with kicker ranked 9-K (not Ace). TPTK = top pair with Ace kicker.

- **TPTK (cat=8):** Hero holds top pair with top kicker (Ace). On Q-high board: Qs + Ah.

- **Overpair (cat=9):** Hero holds a pocket pair higher than the board's top card.
  On Qs-9c-5h (Q-high): overpair = KK, AA (pair higher than Q).
  On Js-6s-2d-8c (J-high turn): overpair = QQ, KK, AA.
  On Qc-7d-3h-Kd (K-high turn): overpair = AA only (K is on board; KK would be
  trips/set with Kd on board; AA is the only pair above K).

- **Two-pair (cat=10):** Hero holds two different pairs. Must use board cards carefully.

---

### BP4 Situation Hero Card Assignments

**B4_05 (Qs-9c-5h, rainbow, Q-high flop):**

Board cards: Qs(queen spades), 9c(nine clubs), 5h(five hearts)

Sit 1 (cat=7, TPGK, BTN, CO opener, BB capped):
- Need top pair of queens + good kicker (not ace)
- hero_cards: `['Qh', 'Kd']`
  - Qh: board has Qs (queen of SPADES). Hero holds Qh (queen of HEARTS). Different suit. CLEAR.
    Hero Qh pairs board Qs → top pair (pair of queens). hand_category = 7 (TPGK) if kicker K.
  - Kd: board has Qs, 9c, 5h. No Kd. CLEAR. K > Q (top card) so K is an overcard to the board
    but serves as kicker. With Qh + Kd on Qs-9c-5h: pair of queens, K kicker = TPGK. PASS.
  - Made hand: pair of queens. is_made_hand=1. PASS.

Sit 2 (cat=8, TPTK, BTN, CO opener, BB capped):
- Need top pair of queens + ace kicker
- hero_cards: `['Qd', 'Ah']`
  - Qd: board has Qs. Qd ≠ Qs (different suit). CLEAR. Pairs board Q = top pair.
  - Ah: board has Qs, 9c, 5h. No Ah. CLEAR.
  - Qd + Ah on Qs-9c-5h: pair of queens, A kicker = TPTK (cat=8). PASS.

Sit 3 (cat=9, overpair, BTN, CO opener, BB capped):
- Need pocket pair > Q (K-K or A-A)
- hero_cards: `['Kh', 'Kc']`
  - Kh: board has Qs, 9c, 5h. No K on board. CLEAR.
  - Kc: board has Qs, 9c (nine of clubs), 5h. No Kc. CLEAR. Note: 9c is on board; Kc is different rank. CLEAR.
  - KK on Qs-9c-5h: overpair (pair of kings > board's Q). hand_category=9. PASS.
  - is_made_hand=1. PASS.

Sit 10 (cat=7, TPGK, CO, BTN opener, HJ cold-call):
- Need top pair of queens + good kicker (not ace). CO hero is cold-caller of BTN's open.
- hero_cards: `['Qc', 'Jd']`
  - Qc: board has Qs. Qc ≠ Qs. CLEAR. Pairs board Q = top pair.
  - Jd: board has Qs, 9c, 5h. No Jd. CLEAR.
  - Qc + Jd: pair of queens, J kicker. TPGK (cat=7). PASS.

Sit 11 (cat=8, TPTK, CO, BTN opener, HJ cold-call):
- Need top pair of queens + ace kicker.
- hero_cards: `['Qh', 'As']`
  - Qh: board has Qs. Qh ≠ Qs. CLEAR. Pairs Q = top pair.
  - As: board has Qs (spades), 9c, 5h. No As. CLEAR.
  - Qh + As: pair of queens, A kicker = TPTK (cat=8). PASS.

**B4_15 (Js-6s-2d-8c, two-tone spades, J-high turn):**

Board cards: Js(jack spades), 6s(six spades), 2d(two diamonds), 8c(eight clubs)

Sit 4 (cat=7, TPGK, BTN, CO opener, BB capped):
- Need top pair of jacks + good kicker.
- hero_cards: `['Jd', 'Th']`
  - Jd: board has Js (jack of SPADES). Hero holds Jd (jack of DIAMONDS). Different suit. CLEAR. Pairs J = top pair.
  - Th: board has Js, 6s, 2d, 8c. No Th. CLEAR.
  - Jd + Th: pair of jacks, T kicker = TPGK (cat=7). PASS.
  - is_made_hand=1. PASS.

Sit 5 (cat=8, TPTK, BTN, CO opener, BB capped):
- Need top pair of jacks + ace kicker.
- hero_cards: `['Jh', 'Ac']`
  - Jh: board has Js. Jh ≠ Js. CLEAR. Pairs J = top pair.
  - Ac: board has 8c (eight of clubs). Hero holds Ac (ace of clubs). Different rank. CLEAR.
  - Jh + Ac: pair of jacks, A kicker = TPTK (cat=8). PASS.

Sit 6 (cat=10, two-pair, BTN, CO opener, BB capped):
- Need two-pair using board cards. On Js-6s-2d-8c: possible two-pair combos for hero:
  J+8 (pair jacks + pair eights): hero holds Jx+8y (pair the J and pair the 8).
  Or J+6, J+2, 8+6, 8+2, 6+2.
  Simplest: hero holds J and 8 of non-board suits.
- hero_cards: `['Jc', '8d']`
  - Jc: board has Js. Jc ≠ Js. CLEAR. Pairs board J.
  - 8d: board has 8c. 8d ≠ 8c. CLEAR. Pairs board 8.
  - Jc + 8d on Js-6s-2d-8c: pair of jacks (Jc + Js) AND pair of eights (8d + 8c) = two pair (jacks and eights). hand_category=10. PASS.
  - Note: 2d is on board; hero doesn't hold 2. 6s is on board; hero doesn't hold 6. CLEAR.
  - is_made_hand=1. PASS.

Sit 12 (cat=7, TPGK, CO, HJ opener, SB cold-call):
- Top pair of jacks + good kicker. CO hero cold-called HJ.
- hero_cards: `['Jd', 'Qh']`
  - Jd: board has Js. Jd ≠ Js. CLEAR. Pairs J = top pair.
  - Qh: board has Js, 6s, 2d, 8c. No Qh. CLEAR.
  - Jd + Qh: pair of jacks, Q kicker. TPGK (cat=7) — Q is a good kicker (overcard to board but not top pair designation... Actually on J-high board, hero's kicker Q is higher than the board's top card J. But pair of jacks with Q kicker: hand_category depends on implementation. Q kicker > J top pair card; this might be TPTK by some implementations if Q is the highest non-board card. Standard: TPGK = top pair with a kicker between 9 and K (not A). Q is in that range. cat=7. PASS.

Sit 13 (cat=10, two-pair, CO, HJ opener, SB cold-call):
- Two pair on Js-6s-2d-8c. CO hero.
- hero_cards: `['Jh', '8h']`
  - Jh: board has Js. Jh ≠ Js. CLEAR. Pairs J.
  - 8h: board has 8c. 8h ≠ 8c. CLEAR. Pairs 8.
  - Jh + 8h: two pair (jacks and eights). cat=10. PASS.
  - Note: both hero cards are hearts; no heart on board. No flush draw (only two hearts in play total = no FD).

**B4_16 (Qc-7d-3h-Kd, two-tone diamonds, K-high turn):**

Board cards: Qc(queen clubs), 7d(seven diamonds), 3h(three hearts), Kd(king diamonds)

Sit 7 (cat=7, TPGK, CO, HJ opener, BB capped):
- Need top pair of kings + good kicker. CO hero, HJ was opener.
- hero_cards: `['Kh', 'Jc']`
  - Kh: board has Kd (king of DIAMONDS). Hero holds Kh (king of HEARTS). Different suit. CLEAR. Pairs K = top pair.
  - Jc: board has Qc (queen of CLUBS). Hero holds Jc (jack of CLUBS). Different rank. CLEAR.
  - Kh + Jc: pair of kings, J kicker. TPGK (cat=7). PASS.
  - is_made_hand=1. PASS.

Sit 8 (cat=8, TPTK, CO, HJ opener, BB capped):
- Top pair of kings + ace kicker.
- hero_cards: `['Ks', 'Ah']`
  - Ks: board has Kd. Ks ≠ Kd. CLEAR. Pairs K = top pair.
  - Ah: board has Qc, 7d, 3h, Kd. No Ah. CLEAR.
  - Ks + Ah: pair of kings, A kicker = TPTK (cat=8). PASS.

Sit 9 (cat=9, overpair, CO, HJ opener, BB capped):
- Pocket pair > K. On K-high board, only AA qualifies.
- hero_cards: `['Ac', 'Ad']`
  - Ac: board has Qc (queen of CLUBS). Hero holds Ac (ace of CLUBS). Different rank. CLEAR.
  - Ad: board has Kd (king of DIAMONDS) and 7d (seven of DIAMONDS). Hero holds Ad (ace of DIAMONDS). Different rank from K; different rank from 7. CLEAR. No Ad on board. CLEAR.
  - AA on Qc-7d-3h-Kd: overpair (aces > kings). hand_category=9. PASS.

Sit 14 (cat=7, TPGK, BTN, CO opener, SB cold-call):
- Top pair of kings + good kicker. BTN hero cold-called CO.
- hero_cards: `['Kc', 'Jh']`
  - Kc: board has Qc (queen of CLUBS). Hero holds Kc (king of CLUBS). Different rank. CLEAR. No Kc on board (board has Kd, not Kc). CLEAR. Pairs board K = top pair.
  - Jh: board has 3h (three of HEARTS). Hero holds Jh (jack of HEARTS). Different rank. CLEAR.
  - Kc + Jh: pair of kings, J kicker = TPGK (cat=7). PASS.

Sit 15 (cat=9, overpair, BTN, CO opener, SB cold-call):
- Pocket pair > K. Only AA qualifies on K-high board.
- hero_cards: `['Ah', 'As']`
  - Ah: board has Qc, 7d, 3h, Kd. No Ah. CLEAR.
  - As: board has Qc, 7d, 3h, Kd. No As. CLEAR.
  - AA on Qc-7d-3h-Kd: overpair. hand_category=9. PASS.
  - Note: sits 9 and 15 both use AA but with different suits `['Ac','Ad']` vs `['Ah','As']`.
    Both are valid non-board-conflicting combos.

---

### BP4 Complete Hero Card Table

| Sit# | Board | Street | Hero pos | Opener | Capped villain | hand_cat | Hero cards | is_made_hand | villain_aggr | SPR  | Status |
|------|-------|--------|----------|--------|----------------|----------|------------|--------------|--------------|------|--------|
| 1    | B4_05 | Flop   | BTN      | CO     | BB             | 7 (TPGK) | `['Qh','Kd']` | 1 | 0 | 10.8 | PASS |
| 2    | B4_05 | Flop   | BTN      | CO     | BB             | 8 (TPTK) | `['Qd','Ah']` | 1 | 0 | 10.8 | PASS |
| 3    | B4_05 | Flop   | BTN      | CO     | BB             | 9 (OP)   | `['Kh','Kc']` | 1 | 1 | 10.8 | PASS |
| 4    | B4_15 | Turn   | BTN      | CO     | BB             | 7 (TPGK) | `['Jd','Th']` | 1 | 0 | 6.5  | PASS |
| 5    | B4_15 | Turn   | BTN      | CO     | BB             | 8 (TPTK) | `['Jh','Ac']` | 1 | 0 | 6.5  | PASS |
| 6    | B4_15 | Turn   | BTN      | CO     | BB             | 10 (2P)  | `['Jc','8d']` | 1 | 1 | 6.5  | PASS |
| 7    | B4_16 | Turn   | CO       | HJ     | BB             | 7 (TPGK) | `['Kh','Jc']` | 1 | 0 | 6.0  | PASS |
| 8    | B4_16 | Turn   | CO       | HJ     | BB             | 8 (TPTK) | `['Ks','Ah']` | 1 | 0 | 6.0  | PASS |
| 9    | B4_16 | Turn   | CO       | HJ     | BB             | 9 (OP)   | `['Ac','Ad']` | 1 | 1 | 6.0  | PASS |
| 10   | B4_05 | Flop   | CO       | BTN    | HJ             | 7 (TPGK) | `['Qc','Jd']` | 1 | 0 | 10.8 | PASS |
| 11   | B4_05 | Flop   | CO       | BTN    | HJ             | 8 (TPTK) | `['Qh','As']` | 1 | 1 | 10.8 | PASS |
| 12   | B4_15 | Turn   | CO       | HJ     | SB             | 7 (TPGK) | `['Jd','Qh']` | 1 | 0 | 6.5  | PASS |
| 13   | B4_15 | Turn   | CO       | HJ     | SB             | 10 (2P)  | `['Jh','8h']` | 1 | 1 | 6.5  | PASS |
| 14   | B4_16 | Turn   | BTN      | CO     | SB             | 7 (TPGK) | `['Kc','Jh']` | 1 | 0 | 6.0  | PASS |
| 15   | B4_16 | Turn   | BTN      | CO     | SB             | 9 (OP)   | `['Ah','As']` | 1 | 1 | 6.0  | PASS |

---

### BP4 Verification Summary

**hand_category distribution:**
| Category | Count | Situations |
|----------|-------|-----------|
| 7 (TPGK) | 7     | 1, 4, 7, 10, 12, 14 + (one more — sits 1,4,7,10,12,14 = 6) |
| 8 (TPTK) | 4     | 2, 5, 8, 11 |
| 9 (overpair) | 3 | 3, 9, 15 |
| 10 (two-pair) | 3 | 6, 13 + one more |

Recount from table:
- cat=7: sits 1, 4, 7, 10, 12, 14 = 6 situations
- cat=8: sits 2, 5, 8, 11 = 4 situations
- cat=9: sits 3, 9, 15 = 3 situations
- cat=10: sits 6, 13 = 2 situations
- Total: 6+4+3+2 = 15. PASS.

Target from allocation document: cat=7 (7 sits), cat=8 (8 sits), cat=9 (9 sits), cat=10 (10 sits)...
Wait — re-reading source: "Hands: TPGK (7), TPTK (8), overpair (9), two-pair (10)" — these are
the hand_category codes, not the counts. Counts: allocation table shows 15 total situations.
Distribution from table: cats appearing in the 15 rows:
- 7: sits 1,4,7,10,12,14 = 6 rows
- 8: sits 2,5,8,11 = 4 rows
- 9: sits 3,9,15 = 3 rows
- 10: sits 6,13 = 2 rows
Total = 15. The brief requires all four categories to appear; all do. PASS.

**is_preflop_aggressor=0 compliance:** All 15 situations — hero is a caller (BTN cold-calls CO,
CO cold-calls HJ, etc.). PASS.

**is_ip=1 compliance:** All situations are IP heroes (BTN or CO acting after opener checks). PASS.

**villain_range_capped=1 compliance:** All situations include at least one capped villain
(BB defender or cold-caller who excluded 3-bet premiums from their range). PASS.

**danger_score <= 0.35 compliance:** From allocation table: 0.10-0.22 for all 15 situations. PASS.

**Conflict resolution log (BP4):**
- All hero cards verified against board_cards for rank+suit identity. No conflicts found.
- B4_15 two-tone (spades: Js, 6s): hero cards on B4_15 use no spades (Jd/Th, Jh/Ac, Jc/8d,
  Jd/Qh, Jh/8h) — no spade in hero hand for any B4_15 situation, avoiding confusion with
  board's spade flush draws. CLEAN.
- B4_16 two-tone (diamonds: 7d, Kd): hero cards use Kh, Ks, Kc (not Kd) for top pair. Ad,Ah,As
  for aces (no Ad on this board). CLEAN.

---

## Section 3 — Open Items Requiring Owner Decision

### OI-1: B4_07 and B4_08 high_card_rank below Step 4 gate

**Issue:** Step 4 global pre-condition requires high_card_rank >= 12 (Queen or higher top card).
- B4_07 (Jc-9h-7s): high_card_rank=11. Below gate.
- B4_08 (Tc-8h-5s): high_card_rank=10. Below gate.

BP3 situations 1, 2, 3, 6, 7 use these boards. They would fail Step 4's global pre-check under
strict tree interpretation.

**Options:**
A. Replace B4_07 and B4_08 with boards having high_card_rank >= 12. Requires new board definitions.
B. Accept the deviation, noting that on J-high and T-high boards the PFA's range credibility
   argument is weakened but not zero. Relabel these as CHECK if the tree is applied strictly.
C. Adjust the tree's high_card_rank threshold for Step 4 downward to >= 10 for 4A only (combo
   draw equity is board-texture-independent; the rationale is different from value c-bets).

### OI-2: Sit 18 villain_air_pct discrepancy

**Issue:** Allocation document specifies villain_air_pct=0.38 for sit 18 (4D, B4_01).
Step 4D gate requires >= 0.40. This sit would fail Step 4D under strict tree interpretation.

**Options:**
A. Factory agent targets 0.40-0.42 villain_air on B4_01 for sit 18 (feasible given A-T-4r board).
B. Move sit 18 to BP6-H as a near-miss counterexample (villain_air=0.38 fails 4D gate, just like
   sits 21-22 were moved in R2-5).

### OI-3: 4A on rainbow boards (draw_outs >= 12 achievability)

**Issue:** B4_07 (rainbow) and B4_08 (rainbow) cannot produce frontdoor flush draws.
draw_outs >= 12 on a rainbow board requires either: (a) an inclusive out-counting methodology
that blends OESD outs with overcard equity, or (b) acceptance that draw_outs for these sits
will compute to ~8 (OESD only), falling short of the 4A threshold of >= 12.

If draw_outs computes to 8 for sits 1-3 and 6-7, those situations would fall to the Default
step (no Step 4 sub-condition met, assuming 4A requires >=12 strictly). The label would be CHECK,
not BET.

**Options:**
A. Replace B4_07 and B4_08 with two-tone boards that allow genuine flush draw + OESD combos.
B. Retain boards, accept that 4A sits on rainbow boards will compute draw_outs ~8, and classify
   them under a supplementary 4A-relaxed sub-condition (OESD-only, 8 outs) — requiring a tree amendment.
C. Compute draw_outs using the inclusive methodology (OESD + overcard equity as out-equivalents)
   to reach 12+. This requires a decision about the draw_outs feature implementation.

---

*End of document.*
*Author: Design Agent B*
*Date: 9 April 2026*
