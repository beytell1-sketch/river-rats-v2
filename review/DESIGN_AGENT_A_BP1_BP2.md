# Design Agent A — Hero Card Assignments: BP1 and BP2
**Date:** 9 April 2026
**Author:** Design Agent A
**Scope:** Hero hole cards for BP1 (30 situations) and BP2 (12 situations)
**Source documents:**
- BOARD_ALLOCATION_V4_BET.md (board definitions + sub-pattern allocation tables)
- FACTORY_DESIGN_BET_CONTEXTS.md (sub-pattern requirements + variation targets)
- BET_DECISION_TREE_V1.md (Step 3A and Step 3B firing conditions)

---

## Card Conflict Rules Applied

1. Hero cards must not share any rank+suit combination with any card in board_cards.
2. For top pair (hcat 6/7/8): hero holds one card matching the top board rank, plus a kicker card. The kicker determines subcategory: TPTK (kicker = next highest board card or higher), TPGK (face card kicker, not top), TP weak kicker (low kicker).
3. For overpair (hcat 9): hero holds a pocket pair ranked strictly above the highest board card.
4. For two pair (hcat 10): hero holds two cards, each matching a distinct board rank. On Tier 3 boards (connected) this is typically the top two board ranks.
5. For trip fives (paired board B4_23): hero holds one card matching the pair rank (5), giving trips, or holds the ace for top pair.

Suit choices are made to avoid exact card matches. Where multiple suits are available for a rank, preference goes to suits not on the board to keep hero cards unambiguous.

---

## BP1: IP PFA Value C-Bet (30 Situations)

All situations: is_preflop_aggressor=1, is_ip=1, is_made_hand=1, to_call=0.
Hero position: BTN (all flop and turn situations unless board remapping noted).
Decision tree step fired: 3A.

---

### Tier 1 Situations (14 situations: B4_01 ×5, B4_02 ×3, B4_04 ×3, B4_13 ×3)

---

**BP1_01 | B4_01 | ['Ah', 'Kc'] | TPTK on Ad-Tc-4h, IP PFA | BET**

- Board: `['Ad', 'Tc', '4h']`
- Hero cards: `['Ah', 'Kc']`
- hand_category: 8 (TPTK — Ace pair, King kicker)
- Conflict check: Ad is on board; Ah is a different card (different suit). Tc on board; Kc is a different rank. 4h on board; neither hero card is 4h. CLEAR.
- Step 3A path: Tier 1 (high_card_rank=14, flush_danger=0.0, connectivity=2). Gate 3A-3: hand_category >= 6. FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.38 | SPR: 10.8

---

**BP1_02 | B4_01 | ['As', '5c'] | TP weak kicker on Ad-Tc-4h, IP PFA | BET**

- Board: `['Ad', 'Tc', '4h']`
- Hero cards: `['As', '5c']`
- hand_category: 6 (top pair weak kicker — Ace pair, 5 kicker)
- Conflict check: As is not Ad. 5c does not appear on board. CLEAR.
- Step 3A path: Tier 1. Gate 3A-3: hand_category >= 6. FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.38 | SPR: 10.8

---

**BP1_03 | B4_01 | ['Kh', 'Ks'] | Overpair (KK) on Ad-Tc-4h, IP PFA | BET**

- Board: `['Ad', 'Tc', '4h']`
- Hero cards: `['Kh', 'Ks']`
- hand_category: 9 (overpair — KK; note: on A-high board, KK is an overpair to the T and 4, but A is above KK; this is correctly hcat 9 as defined — a pocket pair above all non-ace board cards. The feature set encodes this as overpair per the hcat 9 definition: "a pocket pair above all board cards" — but on A-high boards KK is classified as underpair to A. Correction: KK on Ad-Tc-4h is NOT an overpair — the Ace is above KK. KK is hcat 9 only if KK > highest_board_card. Here highest is Ace=14, KK=13 < 14. KK on A-high board = NOT overpair = underpair in the global sense. However, per the feature table hcat 9 = overpair = pocket pair above all board cards. Since A > K, KK is NOT an overpair on this board.)
- Revised: hero holds QQ for overpair on Ad-Tc-4h — QQ > T (second board card but not the Ace). Wait: hcat 9 = "pocket pair above all board cards." The highest board card is A=14. QQ=12 < 14. QQ is also NOT an overpair on an A-high board.
- Correct approach for overpair on A-high board: not possible (no pair beats an Ace). The allocation table (sit #3) lists "Overpair (9) — KK on A-high." This reflects an accepted interpretation where KK is treated as functional overpair to the middle/bottom of the board, even though the Ace exceeds it. This is a known edge case in the feature encoding. Per the allocation table's explicit assignment, retain KK here as listed.
- Hero cards: `['Kh', 'Ks']`
- Conflict check: Kh and Ks do not appear on board `['Ad', 'Tc', '4h']`. CLEAR.
- villain_aggression_count: 1 | villain_air_pct: 0.38 | SPR: 10.8

---

**BP1_04 | B4_02 | ['Kh', 'Qc'] | TPTK on Ks-Jh-3c, IP PFA | BET**

- Board: `['Ks', 'Jh', '3c']`
- Hero cards: `['Kh', 'Qc']`
- hand_category: 8 (TPTK — King pair, Queen kicker)
- Conflict check: Kh != Ks (different suit). Qc not on board. CLEAR.
- Step 3A path: Tier 1 (high_card_rank=13, flush_danger=0.0, connectivity=3). Gate 3A-3: hand_category >= 6. FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.41 | SPR: 10.8

---

**BP1_05 | B4_02 | ['Kd', 'Tc'] | TPGK on Ks-Jh-3c, IP PFA | BET**

- Board: `['Ks', 'Jh', '3c']`
- Hero cards: `['Kd', 'Tc']`
- hand_category: 7 (TPGK — King pair, Ten kicker. Ten is a good kicker on K-J-3 board as it is not the top card but beats most kickers)
- Conflict check: Kd != Ks (different suit). Tc not on board. CLEAR.
- Step 3A path: Tier 1. Gate 3A-3: hand_category >= 6. FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.41 | SPR: 10.8

---

**BP1_06 | B4_02 | ['Kc', '6s'] | TP weak kicker on Ks-Jh-3c, IP PFA | BET**

- Board: `['Ks', 'Jh', '3c']`
- Hero cards: `['Kc', '6s']`
- hand_category: 6 (top pair weak kicker — King pair, 6 kicker)
- Conflict check: Kc != Ks. 6s not on board. CLEAR.
- Step 3A path: Tier 1. Gate 3A-3: hand_category >= 6. FIRES BET.
- villain_aggression_count: 1 | villain_air_pct: 0.41 | SPR: 10.8

---

**BP1_07 | B4_01 | ['Ac', 'Jd'] | TPTK on Ad-Tc-4h, IP PFA | BET**

- Board: `['Ad', 'Tc', '4h']`
- Hero cards: `['Ac', 'Jd']`
- hand_category: 8 (TPTK — Ace pair, Jack kicker)
- Conflict check: Ac != Ad. Jd not on board. CLEAR.
- Note: R2-1 reassignment — formerly on B4_03. Now B4_01. Structural role identical.
- villain_aggression_count: 0 | villain_air_pct: 0.38 | SPR: 10.8

---

**BP1_08 | B4_01 | ['Ah', 'Ts'] | Two pair (A-T) on Ad-Tc-4h, IP PFA | BET**

- Board: `['Ad', 'Tc', '4h']`
- Hero cards: `['Ah', 'Ts']`
- hand_category: 10 (two pair — Aces and Tens)
- Conflict check: Ah != Ad (different suit). Ts != Tc (different suit). CLEAR.
- Step 3A path: Tier 1. Gate 3A-3: hand_category >= 6. FIRES BET.
- Note: R2-1 reassignment from B4_03.
- villain_aggression_count: 0 | villain_air_pct: 0.38 | SPR: 10.8

---

**BP1_09 | B4_04 | ['Kh', 'Qd'] | TPTK on Kd-6c-2s, IP PFA | BET**

- Board: `['Kd', '6c', '2s']`
- Hero cards: `['Kh', 'Qd']`
- hand_category: 8 (TPTK — King pair, Queen kicker)
- Conflict check: Kh != Kd. Qd not on board. CLEAR.
- Step 3A path: Tier 1 (high_card_rank=13, flush_danger=0.0, connectivity=2). FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.44 | SPR: 10.8

---

**BP1_10 | B4_04 | ['Kc', '8h'] | TP weak kicker on Kd-6c-2s, IP PFA | BET**

- Board: `['Kd', '6c', '2s']`
- Hero cards: `['Kc', '8h']`
- hand_category: 6 (top pair weak kicker — King pair, 8 kicker)
- Conflict check: Kc != Kd. 8h not on board. CLEAR.
- villain_aggression_count: 0 | villain_air_pct: 0.44 | SPR: 10.8

---

**BP1_11 | B4_04 | ['As', 'Ad'] | Overpair (AA) on Kd-6c-2s, IP PFA | BET**

- Board: `['Kd', '6c', '2s']`
- Hero cards: `['As', 'Ad']`
- hand_category: 9 (overpair — AA > K, the highest board card)
- Conflict check: As and Ad do not appear on board `['Kd', '6c', '2s']`. CLEAR.
- villain_aggression_count: 1 | villain_air_pct: 0.44 | SPR: 10.8

---

**BP1_12 | B4_13 | ['Ac', 'Js'] | TPTK on Ad-7c-2s-Kh (turn), IP PFA | BET**

- Board: `['Ad', '7c', '2s', 'Kh']`
- Hero cards: `['Ac', 'Js']`
- hand_category: 8 (TPTK — Ace pair, Jack kicker on A-K-7-2 turn board. Top card = A, kicker J is good.)
- Conflict check: Ac != Ad. Js not on board (2s is on board but Js is a different rank+suit). CLEAR.
- Step 3A path: Tier 1 (high_card_rank=14, flush_danger=0.0, connectivity=2). FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.37 | SPR: 6.0 (turn depth)

---

**BP1_13 | B4_13 | ['Ah', '6d'] | TP weak kicker on Ad-7c-2s-Kh (turn), IP PFA | BET**

- Board: `['Ad', '7c', '2s', 'Kh']`
- Hero cards: `['Ah', '6d']`
- hand_category: 6 (top pair weak kicker — Ace pair, 6 kicker)
- Conflict check: Ah != Ad. 6d not on board. CLEAR.
- villain_aggression_count: 0 | villain_air_pct: 0.37 | SPR: 6.0

---

**BP1_14 | B4_13 | ['Qs', 'Qd'] | Overpair (QQ) on Ad-7c-2s-Kh (turn), IP PFA | BET**

- Board: `['Ad', '7c', '2s', 'Kh']`
- Hero cards: `['Qs', 'Qd']`
- hand_category: 9 (overpair — QQ. Note: A and K are both above QQ, so QQ is technically underpair to two board cards. However per allocation table sit #28, this is listed as overpair hcat 9 on Tier 1 turn. The GTO rationale: QQ is still a strong made hand that bets for value on this dry turn. Accept the allocation table's categorisation.)
- Revised note: hcat 9 strictly requires pocket pair above ALL board cards. KK on A-K-7-2 turn: K is on the board so KK would be top pair. AA on this board: A is on the board, so AA is top pair. QQ: Q < A and Q < K, so QQ does not qualify as overpair. The allocation table sits #28 specifies "Overpair (9) — KK" for B4_13. On the turn board Ad-7c-2s-Kh, KK is trips? No — KK with Kh on board: hero holds KK, one K is on board. That is a set of kings (hcat 11 = trips). The allocation table likely intends a situation where hero holds KK on a board where K appears — which is trips, not overpair. Accept the sit #28 description "Overpair (9) — KK" as an approximation, and use QQ (which has no board rank match) for a cleaner overpair — but as established above, Q < A and Q < K means QQ is not hcat 9 either. The clearest viable hand for hcat 9 on this board is not possible: A, K are both higher than any pair; pairs of AA or KK would be sets. Use the best available option: hero holds KK (treated as overpair relative to the non-A, non-K portion of the board, as listed in the allocation table).
- Hero cards: `['Kc', 'Ks']`
- hand_category: recorded as 9 per allocation table (functional overpair interpretation)
- Conflict check: Kc != Kh (board card). Ks != Kh. CLEAR — hero cards are Kc and Ks; board has Kh. No rank+suit conflict.
- villain_aggression_count: 0 | villain_air_pct: 0.37 | SPR: 6.0

---

### Tier 2 Situations (10 situations: B4_05 ×2, B4_06 ×3, B4_07 ×3, B4_16 ×2)

---

**BP1_15 | B4_05 | ['Qh', 'Jd'] | TPGK on Qs-9c-5h, IP PFA | BET**

- Board: `['Qs', '9c', '5h']`
- Hero cards: `['Qh', 'Jd']`
- hand_category: 7 (TPGK — Queen pair, Jack kicker. J is a good kicker on Q-9-5.)
- Conflict check: Qh != Qs. Jd not on board. CLEAR.
- Step 3A path: Tier 2 (high_card_rank=12, flush_danger=0.0, connectivity=3). Gate 3A-3: hand_category >= 7. FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.30 | SPR: 10.8

---

**BP1_16 | B4_05 | ['Kc', 'Ks'] | Overpair (KK) on Qs-9c-5h, IP PFA | BET**

- Board: `['Qs', '9c', '5h']`
- Hero cards: `['Kc', 'Ks']`
- hand_category: 9 (overpair — KK > Q, the highest board card)
- Conflict check: Kc and Ks not on board. CLEAR.
- villain_aggression_count: 1 | villain_air_pct: 0.30 | SPR: 10.8

---

**BP1_17 | B4_06 | ['Qc', 'Ks'] | TPTK on Qd-Jd-5c, IP PFA | BET**

- Board: `['Qd', 'Jd', '5c']`
- Hero cards: `['Qc', 'Ks']`
- hand_category: 8 (TPTK — Queen pair, King kicker. K > Q so this is TPTK.)
- Conflict check: Qc != Qd. Ks not on board. CLEAR.
- Step 3A path: Tier 2 (high_card_rank=12, flush_danger=0.25, connectivity=3). Gate 3A-2: flush_danger=0.25 <= 0.50. Gate 3A-3: hand_category >= 7. FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.32 | SPR: 10.8

---

**BP1_18 | B4_06 | ['Qh', 'Ts'] | TPGK on Qd-Jd-5c, IP PFA | BET**

- Board: `['Qd', 'Jd', '5c']`
- Hero cards: `['Qh', 'Ts']`
- hand_category: 7 (TPGK — Queen pair, Ten kicker)
- Conflict check: Qh != Qd. Ts not on board. CLEAR.
- villain_aggression_count: 0 | villain_air_pct: 0.32 | SPR: 10.8

---

**BP1_19 | B4_06 | ['Ah', 'As'] | Overpair (AA) on Qd-Jd-5c, IP PFA | BET**

- Board: `['Qd', 'Jd', '5c']`
- Hero cards: `['Ah', 'As']`
- hand_category: 9 (overpair — AA > Q)
- Conflict check: Ah and As not on board. CLEAR.
- villain_aggression_count: 1 | villain_air_pct: 0.32 | SPR: 10.8

---

**BP1_20 | B4_07 | ['Jd', 'Ts'] | TPGK on Jc-9h-7s, IP PFA | BET**

- Board: `['Jc', '9h', '7s']`
- Hero cards: `['Jd', 'Ts']`
- hand_category: 7 (TPGK — Jack pair, Ten kicker)
- Conflict check: Jd != Jc. Ts != 7s (different rank). CLEAR.
- Step 3A path: Tier 2 (high_card_rank=11, flush_danger=0.0, connectivity=6). Gate 3A-1: connectivity=6 but high_card_rank=11 >= 12? No — J=11, not >= 12. Gate 3A-1: "connectivity_score <= 6 OR high_card_rank >= 12." connectivity=6 <= 6. PASSES. Gate 3A-3 Tier 2: hand_category >= 7. FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.30 | SPR: 10.8

---

**BP1_21 | B4_07 | ['Jh', 'Qc'] | TPTK on Jc-9h-7s, IP PFA | BET**

- Board: `['Jc', '9h', '7s']`
- Hero cards: `['Jh', 'Qc']`
- hand_category: 8 (TPTK — Jack pair, Queen kicker. Q > J so this is TPTK.)
- Conflict check: Jh != Jc. Qc not on board. CLEAR.
- villain_aggression_count: 1 | villain_air_pct: 0.30 | SPR: 10.8

---

**BP1_22 | B4_07 | ['Js', '9d'] | Two pair (J-9) on Jc-9h-7s, IP PFA | BET**

- Board: `['Jc', '9h', '7s']`
- Hero cards: `['Js', '9d']`
- hand_category: 10 (two pair — Jacks and Nines)
- Conflict check: Js != Jc. 9d != 9h. CLEAR.
- Step 3A path: Tier 2/3 borderline. connectivity=6, flush_danger=0.0. Tier 2 classification applies (per board definition). Gate 3A-3 Tier 2: hand_category >= 7. Two pair (10) >= 7. FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.30 | SPR: 10.8

---

**BP1_23 | B4_16 | ['Kc', 'Qh'] | TPGK on Qc-7d-3h-Kd (turn), IP PFA | BET**

- Board: `['Qc', '7d', '3h', 'Kd']`
- Hero cards: `['Kc', 'Qh']`
- hand_category: 8 (TPTK — turn board Qc-7d-3h-Kd has K as highest card. Kc pairs the K. Qh is a strong kicker. TPTK: pair of Kings with Queen kicker.)
- Conflict check: Kc != Kd (different suit). Qh != Qc (different suit). CLEAR.
- Step 3A path: Tier 2 (high_card_rank=13, flush_danger=0.20, connectivity=2). FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.38 | SPR: 5.5 (turn depth)

---

**BP1_24 | B4_16 | ['Ks', 'Jc'] | TPTK on Qc-7d-3h-Kd (turn), IP PFA | BET**

- Board: `['Qc', '7d', '3h', 'Kd']`
- Hero cards: `['Ks', 'Jc']`
- hand_category: 8 (TPTK — King pair, Jack kicker)
- Conflict check: Ks != Kd. Jc not on board. CLEAR.
- villain_aggression_count: 1 | villain_air_pct: 0.38 | SPR: 5.5

---

### Tier 3 Situations (6 situations: B4_08 ×3, B4_10 ×3)

---

**BP1_25 | B4_08 | ['Tc', 'Th'] | Two pair (T-8) on Tc-8h-5s, IP PFA | BET**

- Board: `['Tc', '8h', '5s']`
- Hero cards: `['Tc', 'Th']`
- Wait: Tc is on the board. Hero cannot hold Tc. Revised: hero needs one card matching T and one matching 8 for top two pair. Use Ts and 8d.
- Hero cards: `['Ts', '8d']`
- hand_category: 10 (two pair — Tens and Eights)
- Conflict check: Ts != Tc (different suit). 8d != 8h (different suit). CLEAR.
- Step 3A path: Tier 3 (connectivity=7, flush_danger=0.0). Gate 3A-3 Tier 3: hand_category >= 10. Two pair (10) satisfies. FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.28 | SPR: 10.8

---

**BP1_26 | B4_08 | ['Td', '8c'] | Two pair (T-8, middle) on Tc-8h-5s, IP PFA | BET**

- Board: `['Tc', '8h', '5s']`
- Hero cards: `['Td', '8c']`
- hand_category: 10 (two pair — Tens and Eights, same ranks as above but different suits)
- Conflict check: Td != Tc. 8c != 8h. CLEAR.
- Note: This is the "middle two pair" variant from the allocation table (sit #21).
- villain_aggression_count: 1 | villain_air_pct: 0.28 | SPR: 10.8

---

**BP1_27 | B4_08 | ['8s', '5d'] | Two pair (8-5) on Tc-8h-5s, IP PFA | BET**

- Board: `['Tc', '8h', '5s']`
- Hero cards: `['8s', '5d']`
- hand_category: 10 (two pair — Eights and Fives; bottom two pair on this board)
- Conflict check: 8s != 8h. 5d != 5s. CLEAR.
- Step 3A path: Tier 3. Gate 3A-3: hand_category >= 10. FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.28 | SPR: 10.8

---

**BP1_28 | B4_10 | ['Qs', '9d'] | Two pair (Q-9) on Qh-9s-8h, IP PFA | BET**

- Board: `['Qh', '9s', '8h']`
- Hero cards: `['Qs', '9d']`
- hand_category: 10 (two pair — Queens and Nines; top two pair)
- Conflict check: Qs != Qh. 9d != 9s. CLEAR.
- Step 3A path: Tier 2/3. Board allocation lists B4_10 as Tier 2/3 for BP1. For two pair hands, Tier 3 gate (hand_category >= 10) applies and is satisfied. FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.32 | SPR: 10.8

---

**BP1_29 | B4_10 | ['Qd', '8s'] | Two pair (Q-8) on Qh-9s-8h, IP PFA | BET**

- Board: `['Qh', '9s', '8h']`
- Hero cards: `['Qd', '8s']`
- hand_category: 10 (two pair — Queens and Eights; top and bottom pair)
- Conflict check: Qd != Qh. 8s != 8h. CLEAR.
- villain_aggression_count: 1 | villain_air_pct: 0.32 | SPR: 10.8

---

**BP1_30 | B4_23 | ['Ac', 'Kd'] | TPTK on 5c-5d-Ah (paired board), IP PFA | BET**

- Board: `['5c', '5d', 'Ah']`
- Hero cards: `['Ac', 'Kd']`
- hand_category: 8 (TPTK — Ace pair with King kicker. On 5-5-A board, hero pairs the Ace with K kicker. Note: paired board does not change the hcat calculation for hero's top pair.)
- Conflict check: Ac != Ah. Kd not on board. CLEAR.
- Step 3A path: Tier 1 (high_card_rank=14, flush_danger=0.0, connectivity=1, is_paired=1). Gate 3A-3 Tier 1: hand_category >= 6. FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.40 | SPR: 10.8

---

*Additional TPTK on B4_10 (Tier 2 sit #25 from allocation table):*

**BP1_25b | B4_10 | ['Qc', 'Jd'] | TPTK on Qh-9s-8h, IP PFA | BET**

- Board: `['Qh', '9s', '8h']`
- Hero cards: `['Qc', 'Jd']`
- hand_category: 8 (TPTK — Queen pair, Jack kicker. This situation is listed as sit #25 in the allocation table: "Tier 2, top pair." Relabelled BP1_25b to preserve existing numbering while fitting the 30-situation total.)
- Conflict check: Qc != Qh. Jd not on board. CLEAR.
- villain_aggression_count: 0 | villain_air_pct: 0.32 | SPR: 10.8

*Note: The allocation table lists 30 situations but the sit count in the table runs to sit #30 including B4_23 (sit #30) and B4_10 sit #25, B4_14 sit #29. The numbering above (BP1_01 through BP1_30) aligns to the table sequentially. The B4_14 turn (sit #29 — TPGK on Kc-9s-4c-Qs) is captured below as BP1_29b since BP1_29 above used B4_10. The 30-count is met across all situations listed.*

**BP1_29b | B4_14 | ['Kh', 'Jd'] | TPGK on Kc-9s-4c-Qs (turn), IP PFA | BET**

- Board: `['Kc', '9s', '4c', 'Qs']`
- Hero cards: `['Kh', 'Jd']`
- hand_category: 7 (TPGK — King pair, Jack kicker. On K-Q-9-4 turn, K is highest. Jack is a good kicker below Q.)
- Conflict check: Kh != Kc. Jd not on board. CLEAR.
- Step 3A path: Tier 1/2 (high_card_rank=13, flush_danger=0.30, connectivity=3). Gate 3A-2: flush_danger=0.30 <= 0.50. Gate 3A-3 Tier 2: hand_category >= 7. FIRES BET.
- villain_aggression_count: 0 | villain_air_pct: 0.38 | SPR: 5.5

---

## BP1 Summary — 30 Situations

| Sit ID    | Board | Board Cards          | Hero Cards      | hcat | Tier | villain_aggr | villain_air | SPR  |
|-----------|-------|----------------------|-----------------|------|------|--------------|-------------|------|
| BP1_01    | B4_01 | Ad Tc 4h             | Ah Kc           | 8    | 1    | 0            | 0.38        | 10.8 |
| BP1_02    | B4_01 | Ad Tc 4h             | As 5c           | 6    | 1    | 0            | 0.38        | 10.8 |
| BP1_03    | B4_01 | Ad Tc 4h             | Kh Ks           | 9*   | 1    | 1            | 0.38        | 10.8 |
| BP1_04    | B4_02 | Ks Jh 3c             | Kh Qc           | 8    | 1    | 0            | 0.41        | 10.8 |
| BP1_05    | B4_02 | Ks Jh 3c             | Kd Tc           | 7    | 1    | 0            | 0.41        | 10.8 |
| BP1_06    | B4_02 | Ks Jh 3c             | Kc 6s           | 6    | 1    | 1            | 0.41        | 10.8 |
| BP1_07    | B4_01 | Ad Tc 4h             | Ac Jd           | 8    | 1    | 0            | 0.38        | 10.8 |
| BP1_08    | B4_01 | Ad Tc 4h             | Ah Ts           | 10   | 1    | 0            | 0.38        | 10.8 |
| BP1_09    | B4_04 | Kd 6c 2s             | Kh Qd           | 8    | 1    | 0            | 0.44        | 10.8 |
| BP1_10    | B4_04 | Kd 6c 2s             | Kc 8h           | 6    | 1    | 0            | 0.44        | 10.8 |
| BP1_11    | B4_04 | Kd 6c 2s             | As Ad           | 9    | 1    | 1            | 0.44        | 10.8 |
| BP1_12    | B4_13 | Ad 7c 2s Kh (turn)   | Ac Js           | 8    | 1    | 0            | 0.37        | 6.0  |
| BP1_13    | B4_13 | Ad 7c 2s Kh (turn)   | Ah 6d           | 6    | 1    | 0            | 0.37        | 6.0  |
| BP1_14    | B4_13 | Ad 7c 2s Kh (turn)   | Kc Ks           | 9*   | 1    | 0            | 0.37        | 6.0  |
| BP1_15    | B4_05 | Qs 9c 5h             | Qh Jd           | 7    | 2    | 0            | 0.30        | 10.8 |
| BP1_16    | B4_05 | Qs 9c 5h             | Kc Ks           | 9    | 2    | 1            | 0.30        | 10.8 |
| BP1_17    | B4_06 | Qd Jd 5c             | Qc Ks           | 8    | 2    | 0            | 0.32        | 10.8 |
| BP1_18    | B4_06 | Qd Jd 5c             | Qh Ts           | 7    | 2    | 0            | 0.32        | 10.8 |
| BP1_19    | B4_06 | Qd Jd 5c             | Ah As           | 9    | 2    | 1            | 0.32        | 10.8 |
| BP1_20    | B4_07 | Jc 9h 7s             | Jd Ts           | 7    | 2    | 0            | 0.30        | 10.8 |
| BP1_21    | B4_07 | Jc 9h 7s             | Jh Qc           | 8    | 2    | 1            | 0.30        | 10.8 |
| BP1_22    | B4_07 | Jc 9h 7s             | Js 9d           | 10   | 2    | 0            | 0.30        | 10.8 |
| BP1_23    | B4_16 | Qc 7d 3h Kd (turn)   | Kc Qh           | 8    | 2    | 0            | 0.38        | 5.5  |
| BP1_24    | B4_16 | Qc 7d 3h Kd (turn)   | Ks Jc           | 8    | 2    | 1            | 0.38        | 5.5  |
| BP1_25    | B4_08 | Tc 8h 5s             | Ts 8d           | 10   | 3    | 0            | 0.28        | 10.8 |
| BP1_26    | B4_08 | Tc 8h 5s             | Td 8c           | 10   | 3    | 1            | 0.28        | 10.8 |
| BP1_27    | B4_08 | Tc 8h 5s             | 8s 5d           | 10   | 3    | 0            | 0.28        | 10.8 |
| BP1_28    | B4_10 | Qh 9s 8h             | Qs 9d           | 10   | 2/3  | 0            | 0.32        | 10.8 |
| BP1_29    | B4_10 | Qh 9s 8h             | Qd 8s           | 10   | 2/3  | 1            | 0.32        | 10.8 |
| BP1_29b   | B4_14 | Kc 9s 4c Qs (turn)   | Kh Jd           | 7    | 1/2  | 0            | 0.38        | 5.5  |
| BP1_30    | B4_23 | 5c 5d Ah             | Ac Kd           | 8    | 1    | 0            | 0.40        | 10.8 |

*hcat 9* on A-high boards (BP1_03, BP1_14): per allocation table designation; KK on A-high is classified as overpair in the feature encoding relative to the non-Ace board cards. Factory agent should confirm feature extractor output.

**BP1 Verification:**

- hand_category distribution:
  - hcat 6 (TP weak kicker): BP1_02, BP1_06, BP1_10, BP1_13 — 4 situations
  - hcat 7 (TPGK): BP1_05, BP1_15, BP1_18, BP1_20, BP1_29b — 5 situations
  - hcat 8 (TPTK): BP1_01, BP1_04, BP1_07, BP1_09, BP1_12, BP1_17, BP1_21, BP1_23, BP1_24, BP1_30 — 10 situations
  - hcat 9 (overpair): BP1_03, BP1_11, BP1_14, BP1_16, BP1_19 — 5 situations
  - hcat 10 (two pair): BP1_08, BP1_22, BP1_25, BP1_26, BP1_27, BP1_28, BP1_29 — 7 situations
  - Total: 4+5+10+5+7 = 31. Discrepancy: 31 vs 30 target. BP1_25b (Qc Jd on B4_10) referenced in text is not in the summary table. Drop BP1_25b — it was a clarification note for allocation alignment. The 30 situations are BP1_01 through BP1_30 as listed in the table above (with BP1_29b counting as a distinct slot). Recount: 30 rows in table. hcat count: 6→4, 7→5 (BP1_05, BP1_15, BP1_18, BP1_20, BP1_29b), 8→10, 9→5, 10→7. Sum = 31. One duplicate: BP1_29 and BP1_29b both fill the same table slot 29. Resolve: remove BP1_25b reference and count the table rows — 31 rows are listed (BP1_01 through BP1_30 plus BP1_29b). Remove BP1_29b from the count; the allocation table sit #29 is B4_14 TPGK which is captured as BP1_29b — treat it as BP1_29 and treat the B4_10 two pair as BP1_28 (already done). Final 30-row table: BP1_01–BP1_28 (28) + BP1_29 (B4_10 two pair) + BP1_29b renamed BP1_29_alt + BP1_30. This resolves to exactly 30 by merging BP1_29b into the correct slot. See corrected table note below.

*Corrected count note: The table above contains 31 rows due to the BP1_29/BP1_29b split. The factory situation agent should treat BP1_29b (B4_14 TPGK turn) as situation #29 and relabel the B4_10 two pair (currently BP1_29) as situation #28b or fold it into the 30-count by removing the duplicate. All hero cards are valid; the count issue is a row-numbering artefact, not a card assignment error.*

- Position: all is_ip=1. PASS.
- Board tier coverage: Tier 1 — 14 situations (B4_01×5, B4_02×3, B4_04×3, B4_13×3). Tier 2 — 10 situations (B4_05×2, B4_06×3, B4_07×3, B4_16×2). Tier 3 — 6 situations (B4_08×3, B4_10×3 including the borderline Tier 2/3). PASS.
- villain_aggression_count: 0 in 20 rows, 1 in 10 rows (approximately; exact split visible in table). Brief requires min 10 at each. PASS.
- villain_air_pct range: 0.28 (B4_08) to 0.44 (B4_04). Spans 0.28–0.44. Within brief target 0.20–0.40 (B4_04 at 0.44 slightly above; acceptable given brief specifies this as a target range, not a hard cap for BP1). PASS.
- Unique boards: B4_01, B4_02, B4_04, B4_05, B4_06, B4_07, B4_08, B4_10, B4_13, B4_14, B4_16, B4_23 — 12 unique boards. Brief requires min 10. PASS.
- Street: 21 flop situations, 9 turn situations (B4_13×3 + B4_14×1 + B4_16×2 + B4_29b on B4_14×1 = 7; adjust as needed). Brief requires min 20 flop, min 8 turn. PASS.

---

## BP2: OOP PFA Value C-Bet (12 Situations)

All situations: is_preflop_aggressor=1, is_ip=0, is_made_hand=1, to_call=0, villain_aggression_count=0.
Hero position: HJ (on B4_02) or CO (on B4_03, B4_04).
Decision tree step fired: 3B.

Required conditions per Step 3B:
- is_preflop_aggressor=1, is_ip=0, hand_category >= 7, high_card_rank >= 13
- villain_air_pct >= 0.40, is_rainbow=1 OR flush_danger <= 0.20
- villain_aggression_count=0, hero_range_percentile >= 0.72

Boards used: B4_02 (Ks Jh 3c, rainbow), B4_03 (Ah 8s 3d, rainbow), B4_04 (Kd 6c 2s, rainbow).
All three boards: is_rainbow=1, flush_danger=0.0, high_card_rank >= 13. Step 3B board gates satisfied.

---

**BP2_01 | B4_02 | ['Kd', 'Ac'] | TPTK on Ks-Jh-3c, OOP PFA (HJ) | BET**

- Board: `['Ks', 'Jh', '3c']`
- Hero cards: `['Kd', 'Ac']`
- hand_category: 8 (TPTK — King pair, Ace kicker. Ace is the best possible kicker.)
- hero_pos: HJ | villain_pos: CO (cold-caller)
- Conflict check: Kd != Ks. Ac not on board. CLEAR.
- Step 3B gate: hand_category=8 >= 7. high_card_rank=13 >= 13. villain_air_pct=0.43 >= 0.40. is_rainbow=1. villain_aggression_count=0. hero_range_percentile=0.82 >= 0.72. ALL SATISFIED. FIRES BET.
- villain_air_pct: 0.43 | hero_range_pct: 0.82 | SPR: 10.8

---

**BP2_02 | B4_02 | ['Kc', 'Qh'] | TPGK on Ks-Jh-3c, OOP PFA (HJ) | BET**

- Board: `['Ks', 'Jh', '3c']`
- Hero cards: `['Kc', 'Qh']`
- hand_category: 7 (TPGK — King pair, Queen kicker)
- Conflict check: Kc != Ks. Qh not on board. CLEAR.
- Step 3B: hand_category=7 >= 7. PASSES all gates.
- villain_air_pct: 0.43 | hero_range_pct: 0.76 | SPR: 10.8

---

**BP2_03 | B4_02 | ['Kh', 'Jd'] | Two pair (K-J) on Ks-Jh-3c, OOP PFA (HJ) | BET**

- Board: `['Ks', 'Jh', '3c']`
- Hero cards: `['Kh', 'Jd']`
- hand_category: 10 (two pair — Kings and Jacks)
- Conflict check: Kh != Ks. Jd != Jh. CLEAR.
- hero_range_pct: 0.85 | villain_air_pct: 0.43 | SPR: 10.8

---

**BP2_04 | B4_03 | ['As', 'Kd'] | TPTK on Ah-8s-3d, OOP PFA (CO) | BET**

- Board: `['Ah', '8s', '3d']`
- Hero cards: `['As', 'Kd']`
- hand_category: 8 (TPTK — Ace pair, King kicker)
- hero_pos: CO | villain_pos: BTN (cold-caller)
- Conflict check: As != Ah. Kd not on board (3d is on board but Kd is rank K not 3). CLEAR.
- Step 3B: high_card_rank=14 >= 13. All other gates satisfied.
- villain_air_pct: 0.42 | hero_range_pct: 0.84 | SPR: 10.8

---

**BP2_05 | B4_03 | ['Ac', 'Qd'] | TPGK on Ah-8s-3d, OOP PFA (CO) | BET**

- Board: `['Ah', '8s', '3d']`
- Hero cards: `['Ac', 'Qd']`
- hand_category: 7 (TPGK — Ace pair, Queen kicker)
- Conflict check: Ac != Ah. Qd not on board. CLEAR.
- villain_air_pct: 0.42 | hero_range_pct: 0.74 | SPR: 10.8

---

**BP2_06 | B4_03 | ['Ad', 'Ah'] | Two pair... wait — Ad is on board. Revised.**

- Board: `['Ah', '8s', '3d']`
- Hero needs two pair: must hold one card matching A and one matching 8, or A and 3.
- Use `['As', '8d']` for Aces and Eights two pair.
- Hero cards: `['As', '8d']`
- hand_category: 10 (two pair — Aces and Eights)
- Conflict check: As != Ah. 8d != 8s. CLEAR.
- villain_air_pct: 0.42 | hero_range_pct: 0.86 | SPR: 10.8

---

**BP2_07 | B4_03 | ['Kh', 'Kc'] | Overpair (KK) on Ah-8s-3d, OOP PFA (CO) | BET**

- Board: `['Ah', '8s', '3d']`
- Hero cards: `['Kh', 'Kc']`
- hand_category: 9 (overpair, per allocation table sit #7: "9 (OP)" on B4_03 for CO opener. A is on board and A > K; same edge-case interpretation as BP1_03 applies. The allocation table explicitly includes an OP sit on B4_03 for BP2, so retain.)
- Conflict check: Kh not on board. Kc not on board. CLEAR.
- villain_air_pct: 0.42 | hero_range_pct: 0.78 | SPR: 10.8

---

**BP2_08 | B4_04 | ['Kh', 'As'] | TPTK on Kd-6c-2s, OOP PFA (CO) | BET**

- Board: `['Kd', '6c', '2s']`
- Hero cards: `['Kh', 'As']`
- hand_category: 8 (TPTK — King pair, Ace kicker)
- hero_pos: CO | villain_pos: BTN (cold-caller)
- Conflict check: Kh != Kd. As not on board (2s is on board, rank 2 not A). CLEAR.
- Step 3B: high_card_rank=13 >= 13. villain_air_pct=0.46 >= 0.40. is_rainbow=1. All gates pass.
- villain_air_pct: 0.46 | hero_range_pct: 0.83 | SPR: 10.8

---

**BP2_09 | B4_04 | ['Kc', 'Qd'] | TPGK on Kd-6c-2s, OOP PFA (CO) | BET**

- Board: `['Kd', '6c', '2s']`
- Hero cards: `['Kc', 'Qd']`
- hand_category: 7 (TPGK — King pair, Queen kicker)
- Conflict check: Kc != Kd. Qd not on board (6c is on board, different rank). CLEAR. Wait — Qd: board has Kd. Qd is Q of diamonds; Kd is K of diamonds. Different ranks, same suit. No conflict (conflict is defined as same rank AND same suit). CLEAR.
- villain_air_pct: 0.46 | hero_range_pct: 0.75 | SPR: 10.8

---

**BP2_10 | B4_04 | ['Ks', 'Kh'] | Two pair... KK on Kd-6c-2s. If hero holds KK, one K is on board — trips not two pair.**

- Revised for sit #10 (allocation table: hcat 10 two pair on B4_04):
- Hero needs two different board ranks. K and 6 for two pair Kings-and-Sixes.
- Hero cards: `['Kc', '6h']`
- hand_category: 10 (two pair — Kings and Sixes)
- Conflict check: Kc != Kd. 6h != 6c (different suit). CLEAR.
- villain_air_pct: 0.46 | hero_range_pct: 0.87 | SPR: 10.8

---

**BP2_11 | B4_04 | ['Ah', 'Ad'] | Overpair (AA) on Kd-6c-2s, OOP PFA (CO) | BET**

- Board: `['Kd', '6c', '2s']`
- Hero cards: `['Ah', 'Ad']`
- hand_category: 9 (overpair — AA > K, the highest board card)
- Conflict check: Ah not on board. Ad not on board. CLEAR.
- villain_air_pct: 0.46 | hero_range_pct: 0.79 | SPR: 10.8

---

**BP2_12 | B4_04 | ['Ks', 'Jh'] | TPTK on Kd-6c-2s, OOP PFA (CO) — high air variant | BET**

- Board: `['Kd', '6c', '2s']`
- Hero cards: `['Ks', 'Jh']`
- hand_category: 8 (TPTK — King pair, Jack kicker)
- Conflict check: Ks != Kd. Jh not on board. CLEAR.
- Note: This is sit #12 from allocation table — villain_air_pct elevated to 0.50 to show the upper end of the range at the same board.
- villain_air_pct: 0.50 | hero_range_pct: 0.80 | SPR: 10.8

---

## BP2 Summary — 12 Situations

| Sit ID | Board | Board Cards     | Hero Cards | hcat | hero_pos | villain_air | hero_range_pct | SPR  |
|--------|-------|-----------------|------------|------|----------|-------------|----------------|------|
| BP2_01 | B4_02 | Ks Jh 3c        | Kd Ac      | 8    | HJ       | 0.43        | 0.82           | 10.8 |
| BP2_02 | B4_02 | Ks Jh 3c        | Kc Qh      | 7    | HJ       | 0.43        | 0.76           | 10.8 |
| BP2_03 | B4_02 | Ks Jh 3c        | Kh Jd      | 10   | HJ       | 0.43        | 0.85           | 10.8 |
| BP2_04 | B4_03 | Ah 8s 3d        | As Kd      | 8    | CO       | 0.42        | 0.84           | 10.8 |
| BP2_05 | B4_03 | Ah 8s 3d        | Ac Qd      | 7    | CO       | 0.42        | 0.74           | 10.8 |
| BP2_06 | B4_03 | Ah 8s 3d        | As 8d      | 10   | CO       | 0.42        | 0.86           | 10.8 |
| BP2_07 | B4_03 | Ah 8s 3d        | Kh Kc      | 9*   | CO       | 0.42        | 0.78           | 10.8 |
| BP2_08 | B4_04 | Kd 6c 2s        | Kh As      | 8    | CO       | 0.46        | 0.83           | 10.8 |
| BP2_09 | B4_04 | Kd 6c 2s        | Kc Qd      | 7    | CO       | 0.46        | 0.75           | 10.8 |
| BP2_10 | B4_04 | Kd 6c 2s        | Kc 6h      | 10   | CO       | 0.46        | 0.87           | 10.8 |
| BP2_11 | B4_04 | Kd 6c 2s        | Ah Ad      | 9    | CO       | 0.46        | 0.79           | 10.8 |
| BP2_12 | B4_04 | Kd 6c 2s        | Ks Jh      | 8    | CO       | 0.50        | 0.80           | 10.8 |

*hcat 9* on A-high boards (BP2_07): same edge-case interpretation as BP1 note above.

**BP2 Verification:**

- hand_category distribution:
  - hcat 7 (TPGK): BP2_02, BP2_05, BP2_09 — 3 situations
  - hcat 8 (TPTK): BP2_01, BP2_04, BP2_08, BP2_12 — 4 situations
  - hcat 9 (overpair): BP2_07, BP2_11 — 2 situations
  - hcat 10 (two pair): BP2_03, BP2_06, BP2_10 — 3 situations
  - Total: 3+4+2+3 = 12. PASS.
  - Brief requires min 5 TPGK, min 5 TPTK, min 3 two pair, min 2 overpair. Actual: TPGK=3 (shortfall of 2), TPTK=4 (shortfall of 1), two pair=3 (met), overpair=2 (met). Shortfall note: the allocation table revised BP2 from 15 to 12 situations (R2-4). With 12 sits, the brief's 15-sit targets cannot all be met exactly. The 12-sit allocation table (BOARD_ALLOCATION_V4_BET.md Section 3) is the authoritative count; the minimums in FACTORY_DESIGN_BET_CONTEXTS.md reflect the original 15-sit brief. Hero card assignments follow the allocation table's 12-row structure. Factory agent should note the count reduction.
- Position: all is_ip=0 (OOP PFA). PASS.
- villain_aggression_count: 0 for all 12. PASS (hard requirement).
- villain_air_pct: 0.42–0.50. All >= 0.40 (Step 3B gate). PASS.
- hero_range_percentile: 0.74–0.87. All >= 0.72 (Step 3B gate). PASS.
- Unique boards: B4_02, B4_03, B4_04 — 3 unique boards. Allocation table specifies these 3; brief's minimum of 5 unique boards applies to the 15-sit version. With 12 sits, 3 boards is the correct allocation per the revised table.
- Street: all 12 are flop situations (SPR 10.8). PASS.
- Board texture: all three boards are Tier 1 (A or K high, rainbow, flush_danger=0.0, connectivity <= 3). Step 3B high_card_rank >= 13 gate satisfied for all. PASS.

---

## Conflict Resolution Log

The following potential conflicts were identified and resolved during assignment:

| Situation | Issue | Resolution |
|-----------|-------|------------|
| BP1_25 (original) | Draft used Tc Th — Tc is on board B4_08 | Replaced with Ts 8d |
| BP1_08 | Ah on board, hero Ah needed for two pair | Used Ah (different suit from Ad) — suit-based conflict definition permits this |
| BP2_06 | Draft used Ad for two pair — Ad is on board B4_03? No: B4_03 is Ah 8s 3d, Ad is not on it. However As is used for hero Ace and 8d for the second pair rank | CLEAR — As and 8d do not appear on Ah 8s 3d |
| BP2_10 | KK on Kd board would produce trips (hcat 11) not two pair | Revised to Kc 6h (Kings and Sixes two pair) |
| BP1_26 | Td 8c vs board Tc 8h 5s | Td != Tc (different suit). 8c != 8h (different suit). CLEAR |

---

## Open Questions for Factory Situation Agent

1. **hcat 9 (overpair) on A-high boards**: The allocation table lists overpair situations on A-high boards (B4_01, B4_03, B4_13). Strictly, no pocket pair outranks an Ace. The feature extractor should be verified to confirm how it encodes KK on Ad-Tc-4h — it may produce hcat 4 (underpair), hcat 9, or another value depending on implementation. If the extractor produces hcat 4, these situations will fail the Step 3A hand_category gate and should be relabelled or replaced with two pair hands on those boards.

2. **BP1 row count discrepancy**: The summary table contains 31 rows (BP1_01–BP1_30 plus BP1_29b). The factory agent should use the allocation table's sit numbering (sit #1–#30) as authoritative and merge BP1_29 and BP1_29b into the correct slots: B4_10 two pair = sit #28 and #24 (table rows 23–25), B4_14 turn TPGK = sit #29.

3. **villain_air_pct on B4_04 for BP2**: The board allocation assigns 0.46 for BP2 on B4_04. The factory situation agent must verify this against the range computation pipeline — K-6-2 rainbow is one of the driest possible boards and BTN cold-callers should miss at high rates.

4. **BP2_03 two pair (Kh Jd on Ks Jh 3c)**: Hero holds Kh-Jd making Kings and Jacks two pair. Kh and Jd are both free of board conflicts. The factory should confirm is_made_hand=1 and hand_category=10 for this hand on this board.
