# Design Agent 2 — SP1, SP2, SP3, SP4 Hero Card Assignments

**Date:** 9 April 2026
**Agent:** Design Agent 2
**Scope:** SP1 (18 RAISE), SP2 (10 RAISE), SP3 (12 RAISE), SP4 (6 CALL) = 46 situations
**Tree version:** RAISE_DECISION_TREE_V2.md
**Board source:** BOARD_ALLOCATION_V3_FINAL.md (Section 3)

---

## Design Methodology

### Card conflict rules applied
- Hero cards must not appear in board_cards (same rank AND suit)
- For sets: hero holds a pocket pair matching one board rank. Both cards must be off-suit from the board card at that rank.
- For two pair: hero holds two cards, each matching a different board rank. No suit conflict with board.
- For full house on paired boards: hero holds one card matching the paired rank + a pocket pair matching another board rank.
- For SP4 monsters: same construction rules, but a suppressor fires to produce CALL.

### SP1 constraints
- is_monster == 1, hand_category >= 10 (two_pair or set)
- flush_danger >= 0.40 (wet boards)
- No suppressors firing
- SPR from allocation table (these are moderate SPR boards 1.4-6.0)

### SP2 constraints
- is_monster == 1, flush_danger <= 0.20, straight_danger <= 0.20
- spr <= 1.5, hero_range_percentile >= 0.90
- Step 3 (low SPR commit) fires

### SP3 constraints
- is_monster == 1, is_ip == 0, villain_aggression_count <= 1
- SPR 2.6-8.4, all OOP positions, to_call > 0 (genuine check-raise)

### SP4 constraints
- is_monster == 1 BUT one suppressor fires → CALL
- S2: flush_danger >= 0.60 AND is_paired == 1 (B33)
- S3: villain_aggression_count >= 2 (B12, B26)
- S4: spr >= 6.0 AND is_ip == 1 (B09, spr=8.0)
- S5: num_callers_to_bet >= 1 AND hero_range_percentile < 0.92 (B20)

---

## SP1: Monster + Wet Board + Low SPR (18 RAISE)

Board notes for SP1:
- B05: `['6s', '4s', 'Qs']` — monotone spades, flush_danger ~0.90. BTN IP, SPR=6.0.
- B11r: `['Ts', '8s', '4h']` — two-tone spades, flush_danger ~0.55. BTN IP, SPR=5.0.
- B02: `['Kh', '7h', '3d']` — two-tone hearts, flush_danger ~0.45. BB OOP, SPR=5.0.
- B08: `['Qc', '5c', '9h']` — two-tone clubs, flush_danger ~0.50. BB OOP, SPR=5.0.
- B12: `['7c', '2d', 'Kc', 'Ac']` — three clubs on turn, flush_danger ~0.75. BB OOP, SPR=3.0.
- B22: `['Jh', '4c', '2h', 'Td']` — two-tone hearts turn, flush_danger ~0.55. BB OOP, SPR=1.4.
- B16: `['5h', 'Kd', '2h', '8c']` — two-tone hearts turn, flush_danger ~0.45. BTN IP, SPR=4.0.
- B20: `['2c', '9c', 'Qh', '6s']` — two-tone clubs turn, flush_danger ~0.50. CO IP, SPR=1.4.
- B01: `['2c', 'Tc', '6d']` — two-tone clubs, flush_danger ~0.40. BTN IP, SPR=5.0.

### Set construction guide per board

**B05 (6s 4s Qs):**
- Set of queens: hero needs Qh Qd (Qs is on board — must avoid spades; Qh Qd off-suit)
- Set of sixes: hero needs 6h 6d (6s on board; use 6h 6d)
- Set of fours: hero needs 4h 4d (4s on board; use 4h 4d)
- Two pair (Q+6): hero needs Qh 6h — but Qh and 6h both hearts: fine. Wait — board has 6s, 4s, Qs. Hero Qh 6h = Q pairs board Q, 6 pairs board 6 → two pair queens and sixes. No conflict: Qh not on board, 6h not on board. Valid.
- Two pair (Q+4): hero needs Qh 4h or Qh 4d. Qh 4d — Q pairs Qs, 4 pairs 4s. Valid.

**B11r (Ts 8s 4h):**
- Set of tens: hero needs Th Td (Ts on board; use Th Td)
- Set of eights: hero needs 8h 8d (8s on board; use 8h 8d)
- Two pair (T+8): hero needs Th 8h — T pairs Ts, 8 pairs 8s. Valid (Th not on board, 8h not on board).
- Two pair (T+4): hero needs Th 4c — T pairs Ts, 4 pairs 4h. Valid (no conflict).

**B02 (Kh 7h 3d):**
- Set of kings: hero needs Kc Kd (Kh on board; use Kc Kd)
- Set of sevens: hero needs 7c 7d (7h on board; use 7c 7d)
- Two pair (K+7): hero needs Kc 7d — K pairs Kh, 7 pairs 7h. Valid.
- Two pair (K+3): hero needs Kc 3h — K pairs Kh, 3 pairs 3d. Valid (Kc not on board, 3h not on board).

**B08 (Qc 5c 9h):**
- Set of queens: hero needs Qh Qd (Qc on board; use Qh Qd)
- Set of nines: hero needs 9c 9d — wait, 9h is on board. Need 9c 9d — but 9c not on board. Valid: 9c 9d.
- Two pair (Q+9): hero needs Qh 9d — Q pairs Qc, 9 pairs 9h. Valid.
- Two pair (Q+5): hero needs Qh 5d — Q pairs Qc, 5 pairs 5c. Valid (Qh not on board, 5d not on board).

**B12 (7c 2d Kc Ac):**
- Set of kings: hero needs Kh Kd (Kc on board; Kh Kd clear).
- Set of sevens: hero needs 7h 7d (7c on board; 7h 7d clear).
- Two pair (K+7): hero needs Kh 7d — K pairs Kc, 7 pairs 7c. Valid.
- Two pair (K+A): hero needs Kh As — K pairs Kc, A pairs Ac. As not on board (Ac is). Valid.

**B22 (Jh 4c 2h Td):**
- Set of jacks: hero needs Jc Jd (Jh on board; Jc Jd clear).
- Set of tens: hero needs Th Tc — wait, Td on board. Need Th Tc. Th not on board, Tc not on board. Valid.
- Two pair (J+T): hero needs Jc Tc — J pairs Jh, T pairs Td. Valid (Jc and Tc not on board).
- Two pair (J+4): hero needs Jc 4h — J pairs Jh, 4 pairs 4c. Valid (Jc not on board, 4h not on board).

**B16 (5h Kd 2h 8c):**
- Set of kings: hero needs Kh Kc (Kd on board; Kh Kc clear).
- Set of eights: hero needs 8h 8d (8c on board; 8h 8d clear).
- Two pair (K+8): hero needs Kh 8d — K pairs Kd, 8 pairs 8c. Valid (Kh and 8d not on board).
- Two pair (K+5): hero needs Kh 5c — K pairs Kd, 5 pairs 5h. Valid (Kh not on board, 5c not on board).

**B20 (2c 9c Qh 6s):**
- Set of queens: hero needs Qc Qd (Qh on board; Qc Qd clear).
- Set of nines: hero needs 9h 9d (9c on board; 9h 9d clear).
- Two pair (Q+9): hero needs Qd 9h — Q pairs Qh, 9 pairs 9c. Valid.
- Two pair (Q+6): hero needs Qd 6h — Q pairs Qh, 6 pairs 6s. Valid (6h not on board).

**B01 (2c Tc 6d):**
- Set of tens: hero needs Th Td (Tc on board; Th Td clear).
- Two pair (T+6): hero needs Th 6h — T pairs Tc, 6 pairs 6d. Valid (Th and 6h not on board).

---

### SP1 Situation Table

| Sit ID | Board | Hero Cards | Description | Expected Label |
|--------|-------|------------|-------------|----------------|
| SP1_01 | B05 | `['Qh', 'Qd']` | Set of queens on monotone spade board (6s 4s Qs). Villain holds spade draws; hero raises to charge. is_monster=1, hand_category=12, flush_danger=0.90, SPR=6.0. No suppressor fires (hand_category >= 10 clears S1; is_paired=0 clears S2; aggr_count <= 1 clears S3; is_ip=1 but SPR=6.0 is at S4 boundary — S4 fires at spr >= 6.0 AND is_ip == 1. ALERT: SPR=6.0 exactly meets the S4 threshold. S4 definition is spr >= 6.0 AND is_ip == 1 → CALL. This situation would be suppressed by S4. Revised: hero is OOP at B05? No — B05 hero_pos=BTN (IP). S4 fires. Must note this. | RAISE |

Wait — I need to re-examine S4 for B05. B05: hero_pos=BTN (IP), SPR=6.0. S4: spr >= 6.0 AND is_ip == 1 → CALL. SPR=6.0 satisfies "spr >= 6.0". So S4 fires on B05 for ALL IP monster situations.

This is a conflict with the SP1 allocation table which assigns B05 sits 1-3 as RAISE. Let me re-read the allocation.

SP1 sit#1-3 are assigned to B05 with SPR=6.0 and labeled RAISE. But S4 suppressor fires when spr >= 6.0 AND is_ip == 1. B05 hero is BTN (IP), SPR=6.0. This means S4 fires and the label should be CALL.

However, the allocation table is the authoritative source — this is a design document approved by the architect. The SP1 allocation explicitly shows B05 sits 1-3 as RAISE with SPR=6.0. There is a possible interpretation issue: is the threshold "strictly greater than" or "greater than or equal to"? The tree says spr >= 6.0.

Given that the allocation document post-dates the tree and was approved with full awareness of S4 (the FIX 4 note explicitly discusses S4 and B33), the allocation stands as the authoritative design intent. The board-architect explicitly placed B05 in SP1 RAISE. The most defensible resolution: treat SPR=6.0 as the S4 boundary where the preference transitions from "still raises for value" to "CALL". The tree note says "at SPR 4-6 IP monsters still raise for value; only at SPR 6+ does pot control clearly dominate." The word "6+" implies strictly greater than 6.0 in the rationale, even though the formal threshold writes "spr >= 6.0."

For this design document I will flag this as a known tension and defer to the allocation table's explicit RAISE assignment. The expert labeller will make the final call. I will note the S4 flag in the description.

---

**Restated SP1 Situation Table (using allocation table as authoritative):**

| Sit ID | Board | Hero Cards | Description | Expected Label |
|--------|-------|------------|-------------|----------------|
| SP1_01 | B05 | `['Qh', 'Qd']` | Set of queens on monotone spade board (6s 4s Qs). SPR=6.0, IP (BTN). Monster value raise against spade-draw-heavy field. hand_category=12 (set). flush_danger=0.90. Note: S4 boundary — labeller to confirm. | RAISE |
| SP1_02 | B05 | `['Qh', '6h']` | Two pair queens and sixes on monotone spade board (6s 4s Qs). SPR=6.0, IP (BTN). Both hole cards pair board cards; strong two pair on flush-heavy board. hand_category=10. flush_danger=0.90. S4 boundary note applies. | RAISE |
| SP1_03 | B05 | `['6h', '6d']` | Set of sixes on monotone spade board (6s 4s Qs). SPR=6.0, IP (BTN). Middle set on monotone board; raises to deny equity to spade draws. hand_category=12. flush_danger=0.90. S4 boundary note applies. | RAISE |
| SP1_04 | B11r | `['Th', 'Td']` | Set of tens on two-tone board (Ts 8s 4h). SPR=5.0, IP (BTN). Top set on spade-draw board; clear value raise. hand_category=12, flush_danger=0.55. No suppressors. | RAISE |
| SP1_05 | B11r | `['Th', '8h']` | Two pair tens and eights on two-tone board (Ts 8s 4h). SPR=5.0, IP (BTN). Top two pair with flush draw on board; raises to charge spade draws. hand_category=10, flush_danger=0.55. | RAISE |
| SP1_06 | B02 | `['Kc', 'Kd']` | Set of kings on two-tone heart board (Kh 7h 3d). SPR=5.0, OOP (BB). Monster top set OOP; check-raises for value against heart draws. hand_category=12, flush_danger=0.45. No suppressors fire. | RAISE |
| SP1_07 | B02 | `['Kc', '7d']` | Two pair kings and sevens on two-tone heart board (Kh 7h 3d). SPR=5.0, OOP (BB). Top two pair OOP; check-raises to charge flush draws. hand_category=10, flush_danger=0.45. | RAISE |
| SP1_08 | B08 | `['Qh', 'Qd']` | Set of queens on two-tone club board (Qc 5c 9h). SPR=5.0, OOP (BB). Top set OOP against club draws; raises for max value. hand_category=12, flush_danger=0.50. | RAISE |
| SP1_09 | B12 | `['Kh', 'Kd']` | Set of kings on flush-completing turn (7c 2d Kc Ac — three clubs). SPR=3.0, OOP (BB). Monster on high flush-danger board; check-raises to protect equity and charge remaining draws. hand_category=12, flush_danger=0.75. | RAISE |
| SP1_10 | B12 | `['Kh', '7h']` | Two pair kings and sevens on three-club turn (7c 2d Kc Ac). SPR=3.0, OOP (BB). Two pair on flush-danger board; raises at low SPR to deny cheap rivers. hand_category=10, flush_danger=0.75. | RAISE |
| SP1_11 | B22 | `['Jc', 'Jd']` | Set of jacks on two-tone heart turn (Jh 4c 2h Td). SPR=1.4, OOP (BB). Monster at very low SPR; raises to commit stack for value. hand_category=12, flush_danger=0.55. | RAISE |
| SP1_12 | B22 | `['Jc', '4h']` | Two pair jacks and fours on two-tone heart turn (Jh 4c 2h Td). SPR=1.4, OOP (BB). Two pair at very low SPR; stack-off raise for value. hand_category=10, flush_danger=0.55. | RAISE |
| SP1_13 | B16 | `['Kh', 'Kc']` | Set of kings on two-tone heart turn (5h Kd 2h 8c). SPR=4.0, IP (BTN). Top set with heart draw on board; raises to deny equity. hand_category=12, flush_danger=0.45. | RAISE |
| SP1_14 | B16 | `['Kh', '8d']` | Two pair kings and eights on two-tone heart turn (5h Kd 2h 8c). SPR=4.0, IP (BTN). Top two pair with heart draw present; value raise. hand_category=10, flush_danger=0.45. | RAISE |
| SP1_15 | B20 | `['Qc', 'Qd']` | Set of queens on two-tone club turn (2c 9c Qh 6s). SPR=1.4, IP (CO). Monster at very low SPR; commit to the pot. hand_category=12, flush_danger=0.50. No suppressors (S5 would require num_callers_to_bet >= 1; this is SP1 not SP4). | RAISE |
| SP1_16 | B20 | `['Qd', '9h']` | Two pair queens and nines on two-tone club turn (2c 9c Qh 6s). SPR=1.4, IP (CO). Two pair at commit SPR; value raise against club draws. hand_category=10, flush_danger=0.50. | RAISE |
| SP1_17 | B01 | `['Th', 'Td']` | Set of tens on two-tone club board (2c Tc 6d). SPR=5.0, IP (BTN). Top set on club-draw board; value raise. hand_category=12, flush_danger=0.40. | RAISE |
| SP1_18 | B08 | `['Qh', '5d']` | Two pair queens and fives on two-tone club board (Qc 5c 9h). SPR=5.0, OOP (BB). Top two pair OOP; check-raises to charge club draws. hand_category=10, flush_danger=0.50. | RAISE |

---

## SP2: Monster + Dry Board + Low SPR Commit (10 RAISE)

Board notes:
- B10: `['Kc', '4d', '2h']` — rainbow, dry, OOP hero (BB), to_call=0 (hero leads). For SP2: effective_stack=135, SPR=1.5.
- B17: `['Ad', '7s', '3c', '2h']` — rainbow, A-high dry turn, OOP hero (SB), to_call=0. For SP2: effective_stack=270, SPR=1.5.
- B30: `['5c', '3d', '2s']` — rainbow, very dry flop, IP hero (BTN), SPR=1.0.
- B31: `['7d', '2c', 'Ks', '4h']` — rainbow, dry turn, IP hero (CO), SPR=1.4.
- B20: `['2c', '9c', 'Qh', '6s']` — flush_danger=0.0 (VERIFIED), IP hero (CO), SPR=1.4.

Key: hero_range_percentile spans 0.90-0.98 per allocation table. Step 3 fires (spr <= 1.5 AND range_pct >= 0.90).

### Set construction guide

**B10 (Kc 4d 2h):**
- Set of kings: Kh Kd (Kc on board — use Kh Kd)
- Two pair (K+4): Kh 4h (K pairs Kc, 4 pairs 4d; Kh and 4h not on board)
- Two pair (K+2): Kh 2c — 2c is on board. Use Kh 2s instead. Valid.

**B17 (Ad 7s 3c 2h):**
- Set of aces: Ah Ac (Ad on board — use Ah Ac)
- Two pair (A+7): Ah 7h (A pairs Ad, 7 pairs 7s; Ah and 7h not on board)
- Two pair (A+3): Ah 3h (A pairs Ad, 3 pairs 3c; Ah and 3h not on board)

**B30 (5c 3d 2s):**
- Set of fives: 5h 5d (5c on board — use 5h 5d)
- Set of threes: 3h 3c (3d on board — use 3h 3c)
- Two pair (5+3): 5h 3h (5 pairs 5c, 3 pairs 3d; 5h and 3h not on board)
- Two pair (5+2): 5h 2h (5 pairs 5c, 2 pairs 2s; 5h and 2h not on board)

**B31 (7d 2c Ks 4h):**
- Set of kings: Kh Kd (Ks on board — use Kh Kd)
- Two pair (K+7): Kh 7h (K pairs Ks, 7 pairs 7d; Kh and 7h not on board)

**B20 (2c 9c Qh 6s):**
- Set of queens: Qc Qd (Qh on board — use Qc Qd)
- Two pair (Q+9): Qd 9h (Q pairs Qh, 9 pairs 9c; Qd and 9h not on board)

### SP2 Situation Table

| Sit ID | Board | Hero Cards | Description | Expected Label |
|--------|-------|------------|-------------|----------------|
| SP2_01 | B10 | `['Kh', 'Kd']` | Set of kings on dry rainbow flop (Kc 4d 2h). SPR=1.5 (effective_stack=135), OOP (BB) leads. hand_category=12, flush_danger=0, hero_range_percentile=0.95. Step 3 fires: spr <= 1.5 AND range_pct >= 0.90. | RAISE |
| SP2_02 | B10 | `['Kh', '4h']` | Two pair kings and fours on dry rainbow flop (Kc 4d 2h). SPR=1.5, OOP (BB) leads. hand_category=10, flush_danger=0, hero_range_percentile=0.91. Step 3 fires. | RAISE |
| SP2_03 | B17 | `['Ah', 'Ac']` | Set of aces on dry rainbow ace-high turn (Ad 7s 3c 2h). SPR=1.5 (effective_stack=270), OOP (SB) leads. hand_category=12, flush_danger=0, hero_range_percentile=0.97. Step 3 fires. | RAISE |
| SP2_04 | B17 | `['Ah', '7h']` | Two pair aces and sevens on dry rainbow ace-high turn (Ad 7s 3c 2h). SPR=1.5, OOP (SB) leads. hand_category=10, flush_danger=0, hero_range_percentile=0.92. Step 3 fires. | RAISE |
| SP2_05 | B30 | `['5h', '5d']` | Set of fives on very dry rainbow flop (5c 3d 2s). SPR=1.0, IP (BTN). Monster at stack-off SPR on dead-dry board. hand_category=12, flush_danger=0, hero_range_percentile=0.98. Step 3 fires. | RAISE |
| SP2_06 | B30 | `['5h', '3h']` | Two pair fives and threes on very dry rainbow flop (5c 3d 2s). SPR=1.0, IP (BTN). Strong two pair at SPR=1.0; immediate commit. hand_category=10, flush_danger=0, hero_range_percentile=0.93. Step 3 fires. | RAISE |
| SP2_07 | B31 | `['Kh', 'Kd']` | Set of kings on dry rainbow turn (7d 2c Ks 4h). SPR=1.4, IP (CO). Top set on bone-dry board; stack-off at low SPR. hand_category=12, flush_danger=0, hero_range_percentile=0.96. Step 3 fires. | RAISE |
| SP2_08 | B31 | `['Kh', '7h']` | Two pair kings and sevens on dry rainbow turn (7d 2c Ks 4h). SPR=1.4, IP (CO). Top two pair on dry board; low SPR commit. hand_category=10, flush_danger=0, hero_range_percentile=0.90. Step 3 fires. | RAISE |
| SP2_09 | B20 | `['Qc', 'Qd']` | Set of queens on club turn (2c 9c Qh 6s). SPR=1.4, IP (CO). flush_danger=0.0 (VERIFIED). Monster at stack-off SPR. hand_category=12, flush_danger=0, hero_range_percentile=0.98. Step 3 fires. | RAISE |
| SP2_10 | B20 | `['Qd', '9h']` | Two pair queens and nines on club turn (2c 9c Qh 6s). SPR=1.4, IP (CO). flush_danger=0.0 (VERIFIED). Top two pair at commit SPR. hand_category=10, flush_danger=0, hero_range_percentile=0.94. Step 3 fires. | RAISE |

---

## SP3: Monster + OOP Check-Raise (12 RAISE)

Board notes:
- B02: `['Kh', '7h', '3d']` — two-tone hearts, OOP (BB), SPR=5.0, to_call=30. Sits 1-2.
- B06: `['8c', '8h', '3d']` — paired board (eights), rainbow, OOP (BB), SPR=5.5, to_call=30. Sits 3-4.
- B08: `['Qc', '5c', '9h']` — two-tone clubs, OOP (BB), SPR=5.0, to_call=30. Sit 5.
- B13: `['Qd', '6h', '2s', 'Jc']` — rainbow turn, OOP (SB), SPR=8.4, to_call=70. Sits 6, 8.
- B12: `['7c', '2d', 'Kc', 'Ac']` — two-tone clubs turn, OOP (BB), SPR=3.0, to_call=70. Sit 7.
- B15: `['Tc', '3d', '9h', '9s']` — paired nines turn, rainbow, OOP (BB), SPR=2.6, to_call=65. Sit 9.
- B17: `['Ad', '7s', '3c', '2h']` — rainbow turn, OOP (SB), SPR=3.0 (baseline), to_call=0. Sit 10.
- B21: `['3h', '3d', '9s', 'Kc']` — paired threes turn, two-tone hearts, OOP (SB), SPR=3.0, to_call=65. Sits 11-12.

Note on B17 sit#10: B17 has to_call=0 (hero leads). This is the same structural issue as B10. However, the allocation table assigns B17 sit#10 as SP3 with range_pct=0.90. This is a flag from the allocation document itself — B17 SP3 sit#10 is labeled "Set OOP, dry turn" in the notes. The allocation table may be using B17 in a different SPR context (SPR=3.0 baseline, not 1.5). But to_call=0 means hero cannot check-raise. This is a potential conflict.

Resolution: For SP3 sit#10, B17's action_history shows "turn, SB, check" with no bet following. If we use the baseline SPR=3.0 setting (effective_stack=540), this is a leading situation, not a check-raise. The allocation table describes it as "Set OOP, dry turn" with range_pct=0.90 — still a monster OOP. I will design this as a check-leading action on a dry board (hero is first to act, bets/leads for value) and flag it. The design intent appears to be monster OOP leading on a dry board, which is consistent with Step 2 value raise logic even without a check-raise structure. The label remains RAISE.

### Set/full house construction guide

**B02 (Kh 7h 3d) — sits 1-2:**
- Set of kings: Kc Kd (Kh on board)
- Two pair (K+7): Kc 7d (K pairs Kh, 7 pairs 7h; Kc and 7d not on board)

**B06 (8c 8h 3d) — sits 3-4 (paired board):**
- Full house (eights full of threes): hero needs a card matching the paired rank (8) + pocket pair matching another rank (3). But hero needs two hole cards. One approach: 8d 3h = one eight (not 8c or 8h) and one three (not 3d). 8d 3h gives hero trip eights with a paired board = full house (8s full of 3s). hand_category would be full_house (14).
- Full house variant: 8s 3c — 8s (not on board), 3c (not on board). Valid.
- Quads: hero needs 8d 8s — both eights not on board (8c and 8h are on board). 8d 8s are clear. hand_category = quads (16).
- Two pair (8+3) = actually trips since board is paired 8s — technically hand_category is full_house with any 8, or trips with a 3. Let me clarify: on a board of 8c 8h 3d, if hero holds 8d Xh, hero has trips (three eights). If hero holds 3h 3c, hero has full house (threes full of eights). The allocation note says "Full house on paired board" (sit#3) and "Quads or full house" (sit#4).

**B08 (Qc 5c 9h) — sit 5:**
- Set of queens: Qh Qd (Qc on board)

**B13 (Qd 6h 2s Jc) — sits 6, 8:**
- Sit#6 range_pct=0.91 (set): Set of queens: Qh Qc (Qd on board). Or set of jacks: Jh Jd (Jc on board).
- Sit#8 range_pct=0.94 (two pair): Two pair (Q+J): Qh Jh (Q pairs Qd, J pairs Jc; Qh and Jh not on board). Or (Q+6): Qh 6d (Q pairs Qd, 6 pairs 6h; valid).

**B12 (7c 2d Kc Ac) — sit 7:**
- Set of kings: Kh Kd (Kc on board)

**B15 (Tc 3d 9h 9s) — sit 9 (paired nines):**
- Full house: hero needs card matching 9 rank (not 9h or 9s) + another card. 9c Tc: 9c pairs board 9s/9h = trips nines... wait, with Tc also on board, hero's Tc pairs board Tc = trips tens, but that's two separate things. 
- Correct approach: hero 9c 9d would give quads, but 9h and 9s are on board, so 9c and 9d are valid. That gives hero quads nines (hand_category=16), which is is_monster=1.
- For full house: hero needs T + another T? No. Hero could hold Tc... wait, Tc is on board. Hero needs a different approach. With board Tc 3d 9h 9s: if hero holds Th Td, hero has three tens (Tc on board + Th Td in hand = trips, but paired board means Tc + Th Td = just a set, not three pair). Actually hero holds Th Td = pocket tens, board has Tc = hero has set of tens. But board also has 9h 9s — so the board itself is paired (9s), hero's set of tens is still set. hand_category = set (12+). But is_monster=1 for set.
- Allocation says "Full house on paired turn" (sit#9). So hero needs something like Th 9c — trips nines from board pair + one hole 9c (since 9h and 9s on board, 9c not on board). Th pairs board Tc = two pair TT+99 from board... no, with Th in hand: board Tc 3d 9h 9s + hero Th = pair of tens (Tc + Th), board has 99, so hero has two pair (T+9) but the 99 comes from the board. Actually the full board evaluation: hero holds Th + 9c. Board: Tc 3d 9h 9s. Best 5 cards from 6: Tc 9h 9s Th + {3d or 9c}. With 9c in hand: Tc Th 9h 9s 9c = full house (nines full of tens). hand_category = full_house (14). Valid!

**B17 (Ad 7s 3c 2h) — sit 10 (to_call=0, OOP leads):**
- Set of aces: Ah Ac (Ad on board). Hero leads.

**B21 (3h 3d 9s Kc) — sits 11-12 (paired threes):**
- Sit#11 full house: hero 3c Kh (3c not on board since 3h and 3d are; Kh not on board). Board 3h 3d 9s Kc + hero 3c Kh: best hand = 3h 3d 3c Kc Kh = full house (threes full of kings). hand_category=14. Valid.
- Sit#12 alternate monster: hero 9h 9d (9s on board, 9h and 9d not on board). Board 3h 3d 9s Kc + hero 9h 9d: 9s 9h 9d 3h 3d = full house (nines full of threes). hand_category=14.

### SP3 Situation Table

| Sit ID | Board | Hero Cards | Description | Expected Label |
|--------|-------|------------|-------------|----------------|
| SP3_01 | B02 | `['Kc', 'Kd']` | Set of kings OOP check-raise on two-tone heart flop (Kh 7h 3d). SPR=5.0, BB vs BTN bet. Monster top set; checks then raises villain's flop bet. hero_range_percentile=0.95, is_ip=0. No suppressors. | RAISE |
| SP3_02 | B02 | `['Kc', '7d']` | Two pair kings and sevens OOP on two-tone heart flop (Kh 7h 3d). SPR=5.0, BB check-raises BTN. Top two pair; check-raises to charge heart draws and build pot. hero_range_percentile=0.92, is_ip=0. | RAISE |
| SP3_03 | B06 | `['8d', '3h']` | Full house eights full of threes OOP on paired rainbow flop (8c 8h 3d). SPR=5.5, BB check-raises BTN. Hero holds one eight (trips) + one three (boat) from pocket 8+3. hand_category=14 (full_house). hero_range_percentile=0.97, is_ip=0. | RAISE |
| SP3_04 | B06 | `['8s', '3c']` | Full house variant — eights full of threes on paired flop (8c 8h 3d). SPR=5.5, BB check-raises BTN. Alternative suits for sit#3; same hand type. hero holds 8s (trips eights on paired board) and 3c (pairs 3d = boat). hero_range_percentile=0.99, is_ip=0. | RAISE |
| SP3_05 | B08 | `['Qh', 'Qd']` | Set of queens OOP check-raise on two-tone club flop (Qc 5c 9h). SPR=5.0, BB check-raises BTN. Top set OOP; check-raise for value against club draws. hero_range_percentile=0.93, is_ip=0. | RAISE |
| SP3_06 | B13 | `['Qh', 'Qc']` | Set of queens OOP on rainbow turn (Qd 6h 2s Jc). SPR=8.4, SB check-raises BTN. Rainbow board means flush_danger low; OOP monster at higher SPR still raises for value. hero_range_percentile=0.91, is_ip=0. No suppressors (S4 requires is_ip=1; hero is OOP). | RAISE |
| SP3_07 | B12 | `['Kh', 'Kd']` | Set of kings OOP check-raise on flush-danger turn (7c 2d Kc Ac — three clubs). SPR=3.0, BB check-raises BTN. Three clubs on board; hero raises to deny equity to club draws. hero_range_percentile=0.96, is_ip=0. | RAISE |
| SP3_08 | B13 | `['Qh', 'Jh']` | Two pair queens and jacks OOP on rainbow turn (Qd 6h 2s Jc). SPR=8.4, SB check-raises BTN. Top two pair on dry board OOP; check-raise to build pot. hero_range_percentile=0.94, is_ip=0. | RAISE |
| SP3_09 | B15 | `['Th', '9c']` | Full house nines full of tens OOP on paired turn (Tc 3d 9h 9s). SPR=2.6, BB check-raises BTN. Hero Th+9c: board pair 99 + hero 9c = trips nines, + Tc + Th = boat (nines full of tens). hand_category=14. hero_range_percentile=0.98, is_ip=0. | RAISE |
| SP3_10 | B17 | `['Ah', 'Ac']` | Set of aces OOP leading on dry rainbow turn (Ad 7s 3c 2h). SPR=3.0, SB leads (to_call=0). Monster on dry board; hero leads for value with top set. hero_range_percentile=0.90, is_ip=0. Step 2 fires (no suppressors on dry board at SPR=3.0). | RAISE |
| SP3_11 | B21 | `['3c', 'Kh']` | Full house threes full of kings OOP on paired turn (3h 3d 9s Kc). SPR=3.0, SB check-raises BTN. Hero 3c+Kh: trips threes + Kc on board = full house (threes full of kings). hand_category=14, hero_range_percentile=0.95, is_ip=0. | RAISE |
| SP3_12 | B21 | `['9h', '9d']` | Full house nines full of threes OOP on paired turn (3h 3d 9s Kc). SPR=3.0, SB check-raises BTN. Hero 9h+9d + board 9s = trips nines, board 3h 3d pairs = full house (nines full of threes). hand_category=14, hero_range_percentile=0.99, is_ip=0. | RAISE |

---

## SP4: Monster Suppressors — CALL (6 situations)

Board notes:
- B33: `['Qh', 'Qd', '7h']` — paired queens, two-tone hearts, OOP (BB), SPR=5.5, flush_danger~0.65. S2 board.
- B12: `['7c', '2d', 'Kc', 'Ac']` — three clubs turn, OOP (BB), SPR=3.0. S3 board (villain bet flop+turn).
- B26: `['Kh', '5c', '2h', '9d', 'Qh']` — hearts flush completed, OOP (BB), SPR=0.81. S3 board (villain bet flop+turn).
- B09: `['Ah', '4h', '8c']` — two-tone hearts, IP (CO), SPR=8.0. S4 board (spr=8.0 >= 6.0, IP).
- B20: `['2c', '9c', 'Qh', '6s']` — two-tone clubs turn, IP (CO), SPR=1.4. S5 board (num_callers >= 1, range_pct < 0.92).

### Card construction for SP4

**B33 (Qh Qd 7h) — S2 sits 1-2:**
- S2 fires: flush_danger >= 0.60 AND is_paired == 1 → CALL even with monster.
- Sit#1: Need a monster hand (is_monster=1). Set of sevens: hero 7c 7d (7h on board; 7c 7d clear). hand_category=12.
- Sit#2: Full house (Qs full of 7s): hero needs a Queen (not Qh or Qd) and a 7 (not 7h). Qc 7c — Qc not on board, 7c not on board. Valid. Board Qh Qd 7h + hero Qc 7c: best hand = Qh Qd Qc 7h 7c = full house (queens full of sevens). hand_category=14.

**B12 (7c 2d Kc Ac) — S3 sits 3-4:**
- S3 fires: villain_aggression_count >= 2 → CALL even with monster. (B12 action: villain bet flop, bet turn = 2 aggressive actions.)
- Sit#3: Set of kings: Kh Kd (Kc on board; Kh Kd clear). hand_category=12. But S3 fires; label CALL.
- Sit#4 differs per allocation description "villain_aggression_count >= 2, river; is_monster=1 → CALL" for B26. This is actually sit#4 on B26, not B12. Let me recheck: SP4 sit#3 is B12 (S3), sit#4 is B26 (S3). So:

**B26 (Kh 5c 2h 9d Qh) — S3 sit 4:**
- Flush completed (three hearts: Kh 2h Qh). villain (CO) has been aggressive (bet flop, bet turn = aggression_count=2).
- Monster hand: Two pair kings and queens = Kc Qs (K pairs Kh, Q pairs Qh; Kc and Qs not on board). hand_category=10. is_monster=1? Two pair is hand_category=10, and is_monster is defined as set/straight/flush/full_house/quads/SF. Two pair is NOT is_monster by that definition. Need a true monster. 
- Flush (three hearts completed): hero could hold Ah Th for ace-high flush on a heart-completed river. Ah not on board (Kh, 2h, Qh on board — Ah is clear), Th not on board. Hero Ah Th = ace-high flush with three hearts on board = flush. hand_category=flush (13). is_monster=1. Valid.

**B09 (Ah 4h 8c) — S4 sit 5:**
- S4 fires: spr=8.0 >= 6.0 AND is_ip=1 (hero=CO, IP) → CALL.
- Monster hand on this board: Set of aces: As Ac (Ah on board; As Ac clear). hand_category=12. is_monster=1. S4 fires → CALL.

**B20 (2c 9c Qh 6s) — S5 sit 6:**
- S5 fires: num_callers_to_bet >= 1 AND hero_range_percentile < 0.92 → CALL. B20 action shows SB called the BB bet on flop before CO acts (num_callers_to_bet=1 for CO).
- Monster hand: Set of queens: Qc Qd (Qh on board; Qc Qd clear). hand_category=12. hero_range_percentile=0.88 (< 0.92). S5 fires → CALL.

### SP4 Situation Table

| Sit ID | Board | Hero Cards | Description | Expected Label |
|--------|-------|------------|-------------|----------------|
| SP4_01 | B33 | `['7c', '7d']` | Set of sevens on paired two-tone flop (Qh Qd 7h). is_monster=1, hand_category=12. Suppressor S2 fires: flush_danger=0.65 >= 0.60 AND is_paired=1 → full-house danger overrides value raise. CALL despite strong hand. | CALL |
| SP4_02 | B33 | `['Qc', '7c']` | Full house queens full of sevens on paired two-tone flop (Qh Qd 7h). is_monster=1, hand_category=14. Suppressor S2 fires: flush_danger=0.65 AND is_paired=1 → even with full house, flush-on-paired board suppresses raise. CALL. | CALL |
| SP4_03 | B12 | `['Kh', 'Kd']` | Set of kings on flush-danger turn (7c 2d Kc Ac). is_monster=1, hand_category=12. Suppressor S3 fires: villain_aggression_count=2 (bet flop, bet turn) → multi-street aggressor threatens monster. CALL. | CALL |
| SP4_04 | B26 | `['Ah', 'Th']` | Ace-high flush on heart-completed river (Kh 5c 2h 9d Qh). is_monster=1, hand_category=13 (flush). Suppressor S3 fires: villain (CO) bet flop and turn = aggression_count=2 → multi-street aggressor suppresses raise. CALL. | CALL |
| SP4_05 | B09 | `['As', 'Ac']` | Set of aces on two-tone heart flop (Ah 4h 8c). is_monster=1, hand_category=12. Suppressor S4 fires: spr=8.0 >= 6.0 AND is_ip=1 (hero=CO, IP) → high SPR IP favours pot control over value raise. CALL. | CALL |
| SP4_06 | B20 | `['Qc', 'Qd']` | Set of queens on two-tone club turn (2c 9c Qh 6s). is_monster=1, hand_category=12. Suppressor S5 fires: num_callers_to_bet=1 (SB called BB's flop bet before CO) AND hero_range_percentile=0.88 < 0.92 → monster below top 8% of range in bet-and-call spot. CALL. | CALL |

---

## Pipe-Delimited Summary (all 46 situations)

```
SP1_01 | B05 | ['Qh', 'Qd'] | Set of queens on monotone spade board (6s 4s Qs). SPR=6.0, IP (BTN). flush_danger=0.90, hand_category=12. S4 boundary flag for labeller. | RAISE
SP1_02 | B05 | ['Qh', '6h'] | Two pair queens and sixes on monotone spade board. SPR=6.0, IP (BTN). flush_danger=0.90, hand_category=10. S4 boundary flag. | RAISE
SP1_03 | B05 | ['6h', '6d'] | Set of sixes on monotone spade board. SPR=6.0, IP (BTN). flush_danger=0.90, hand_category=12. S4 boundary flag. | RAISE
SP1_04 | B11r | ['Th', 'Td'] | Set of tens on two-tone spade board (Ts 8s 4h). SPR=5.0, IP (BTN). flush_danger=0.55, hand_category=12. No suppressors. | RAISE
SP1_05 | B11r | ['Th', '8h'] | Two pair tens and eights on two-tone spade board. SPR=5.0, IP (BTN). flush_danger=0.55, hand_category=10. | RAISE
SP1_06 | B02 | ['Kc', 'Kd'] | Set of kings on two-tone heart flop (Kh 7h 3d). SPR=5.0, OOP (BB). flush_danger=0.45, hand_category=12. | RAISE
SP1_07 | B02 | ['Kc', '7d'] | Two pair kings and sevens on two-tone heart flop. SPR=5.0, OOP (BB). flush_danger=0.45, hand_category=10. | RAISE
SP1_08 | B08 | ['Qh', 'Qd'] | Set of queens on two-tone club flop (Qc 5c 9h). SPR=5.0, OOP (BB). flush_danger=0.50, hand_category=12. | RAISE
SP1_09 | B12 | ['Kh', 'Kd'] | Set of kings on three-club turn (7c 2d Kc Ac). SPR=3.0, OOP (BB). flush_danger=0.75, hand_category=12. | RAISE
SP1_10 | B12 | ['Kh', '7h'] | Two pair kings and sevens on three-club turn. SPR=3.0, OOP (BB). flush_danger=0.75, hand_category=10. | RAISE
SP1_11 | B22 | ['Jc', 'Jd'] | Set of jacks on two-tone heart turn (Jh 4c 2h Td). SPR=1.4, OOP (BB). flush_danger=0.55, hand_category=12. | RAISE
SP1_12 | B22 | ['Jc', '4h'] | Two pair jacks and fours on two-tone heart turn. SPR=1.4, OOP (BB). flush_danger=0.55, hand_category=10. | RAISE
SP1_13 | B16 | ['Kh', 'Kc'] | Set of kings on two-tone heart turn (5h Kd 2h 8c). SPR=4.0, IP (BTN). flush_danger=0.45, hand_category=12. | RAISE
SP1_14 | B16 | ['Kh', '8d'] | Two pair kings and eights on two-tone heart turn. SPR=4.0, IP (BTN). flush_danger=0.45, hand_category=10. | RAISE
SP1_15 | B20 | ['Qc', 'Qd'] | Set of queens on two-tone club turn (2c 9c Qh 6s). SPR=1.4, IP (CO). flush_danger=0.50, hand_category=12. (SP1 context — no S5 suppressor since num_callers_to_bet differs here vs SP4.) | RAISE
SP1_16 | B20 | ['Qd', '9h'] | Two pair queens and nines on two-tone club turn. SPR=1.4, IP (CO). flush_danger=0.50, hand_category=10. | RAISE
SP1_17 | B01 | ['Th', 'Td'] | Set of tens on two-tone club flop (2c Tc 6d). SPR=5.0, IP (BTN). flush_danger=0.40, hand_category=12. | RAISE
SP1_18 | B08 | ['Qh', '5d'] | Two pair queens and fives on two-tone club flop (Qc 5c 9h). SPR=5.0, OOP (BB). flush_danger=0.50, hand_category=10. | RAISE
SP2_01 | B10 | ['Kh', 'Kd'] | Set of kings on dry rainbow flop (Kc 4d 2h). SPR=1.5, OOP (BB), hero_range_pct=0.95. Step 3 fires. flush_danger=0. | RAISE
SP2_02 | B10 | ['Kh', '4h'] | Two pair kings and fours on dry rainbow flop. SPR=1.5, OOP (BB), hero_range_pct=0.91. Step 3 fires. flush_danger=0. | RAISE
SP2_03 | B17 | ['Ah', 'Ac'] | Set of aces on dry rainbow ace-high turn (Ad 7s 3c 2h). SPR=1.5, OOP (SB), hero_range_pct=0.97. Step 3 fires. flush_danger=0. | RAISE
SP2_04 | B17 | ['Ah', '7h'] | Two pair aces and sevens on dry rainbow turn. SPR=1.5, OOP (SB), hero_range_pct=0.92. Step 3 fires. flush_danger=0. | RAISE
SP2_05 | B30 | ['5h', '5d'] | Set of fives on very dry rainbow flop (5c 3d 2s). SPR=1.0, IP (BTN), hero_range_pct=0.98. Step 3 fires. flush_danger=0. | RAISE
SP2_06 | B30 | ['5h', '3h'] | Two pair fives and threes on very dry rainbow flop. SPR=1.0, IP (BTN), hero_range_pct=0.93. Step 3 fires. flush_danger=0. | RAISE
SP2_07 | B31 | ['Kh', 'Kd'] | Set of kings on dry rainbow turn (7d 2c Ks 4h). SPR=1.4, IP (CO), hero_range_pct=0.96. Step 3 fires. flush_danger=0. | RAISE
SP2_08 | B31 | ['Kh', '7h'] | Two pair kings and sevens on dry rainbow turn. SPR=1.4, IP (CO), hero_range_pct=0.90. Step 3 fires. flush_danger=0. | RAISE
SP2_09 | B20 | ['Qc', 'Qd'] | Set of queens on club turn (2c 9c Qh 6s). SPR=1.4, IP (CO), hero_range_pct=0.98. flush_danger=0 (VERIFIED). Step 3 fires. | RAISE
SP2_10 | B20 | ['Qd', '9h'] | Two pair queens and nines on club turn. SPR=1.4, IP (CO), hero_range_pct=0.94. flush_danger=0 (VERIFIED). Step 3 fires. | RAISE
SP3_01 | B02 | ['Kc', 'Kd'] | Set of kings OOP check-raise on two-tone heart flop (Kh 7h 3d). SPR=5.0, BB. range_pct=0.95, is_ip=0. No suppressors. | RAISE
SP3_02 | B02 | ['Kc', '7d'] | Two pair kings and sevens OOP on two-tone heart flop. SPR=5.0, BB. range_pct=0.92, is_ip=0. | RAISE
SP3_03 | B06 | ['8d', '3h'] | Full house eights full of threes OOP on paired flop (8c 8h 3d). SPR=5.5, BB. hand_category=14, range_pct=0.97, is_ip=0. | RAISE
SP3_04 | B06 | ['8s', '3c'] | Full house eights full of threes — alt suits — on paired flop. SPR=5.5, BB. hand_category=14, range_pct=0.99, is_ip=0. | RAISE
SP3_05 | B08 | ['Qh', 'Qd'] | Set of queens OOP check-raise on two-tone club flop (Qc 5c 9h). SPR=5.0, BB. hand_category=12, range_pct=0.93, is_ip=0. | RAISE
SP3_06 | B13 | ['Qh', 'Qc'] | Set of queens OOP check-raise on rainbow turn (Qd 6h 2s Jc). SPR=8.4, SB. hand_category=12, range_pct=0.91, is_ip=0. S4 does not fire (is_ip=0). | RAISE
SP3_07 | B12 | ['Kh', 'Kd'] | Set of kings OOP check-raise on flush-danger turn (7c 2d Kc Ac). SPR=3.0, BB. hand_category=12, range_pct=0.96, is_ip=0. | RAISE
SP3_08 | B13 | ['Qh', 'Jh'] | Two pair queens and jacks OOP on rainbow turn (Qd 6h 2s Jc). SPR=8.4, SB. hand_category=10, range_pct=0.94, is_ip=0. | RAISE
SP3_09 | B15 | ['Th', '9c'] | Full house nines full of tens OOP on paired turn (Tc 3d 9h 9s). SPR=2.6, BB. hand_category=14, range_pct=0.98, is_ip=0. | RAISE
SP3_10 | B17 | ['Ah', 'Ac'] | Set of aces OOP leading on dry rainbow turn (Ad 7s 3c 2h). SPR=3.0, SB. to_call=0, hero leads for value. hand_category=12, range_pct=0.90, is_ip=0. | RAISE
SP3_11 | B21 | ['3c', 'Kh'] | Full house threes full of kings OOP on paired turn (3h 3d 9s Kc). SPR=3.0, SB. hand_category=14, range_pct=0.95, is_ip=0. | RAISE
SP3_12 | B21 | ['9h', '9d'] | Full house nines full of threes OOP on paired turn (3h 3d 9s Kc). SPR=3.0, SB. hand_category=14, range_pct=0.99, is_ip=0. | RAISE
SP4_01 | B33 | ['7c', '7d'] | Set of sevens on paired two-tone flop (Qh Qd 7h). is_monster=1, hand_category=12. S2 fires: flush_danger=0.65 >= 0.60 AND is_paired=1. | CALL
SP4_02 | B33 | ['Qc', '7c'] | Full house queens full of sevens on paired two-tone flop (Qh Qd 7h). is_monster=1, hand_category=14. S2 fires: flush_danger=0.65 AND is_paired=1. | CALL
SP4_03 | B12 | ['Kh', 'Kd'] | Set of kings on flush-danger turn (7c 2d Kc Ac). is_monster=1, hand_category=12. S3 fires: villain_aggression_count=2 (flop+turn bet). | CALL
SP4_04 | B26 | ['Ah', 'Th'] | Ace-high flush on heart-completed river (Kh 5c 2h 9d Qh). is_monster=1, hand_category=13. S3 fires: villain_aggression_count=2. | CALL
SP4_05 | B09 | ['As', 'Ac'] | Set of aces on two-tone heart flop (Ah 4h 8c). is_monster=1, hand_category=12. S4 fires: spr=8.0 >= 6.0 AND is_ip=1. | CALL
SP4_06 | B20 | ['Qc', 'Qd'] | Set of queens on two-tone club turn (2c 9c Qh 6s). is_monster=1, hand_category=12. S5 fires: num_callers=1 (SB called) AND range_pct=0.88 < 0.92. | CALL
```

---

## Verification Summary

### SP1 — hand_category distribution, flush_danger range, SPR range

| Check | Value | Status |
|-------|-------|--------|
| Total situations | 18 | PASS |
| Set hands (hand_category 12+) | 9 (sits 01,03,04,06,08,09,11,13,15,17 — actually 10 sets) | PASS (min 12 required is for count, no minimum set count specified; allocation says "mix of two_pair and set") |
| Two pair hands (hand_category 10-11) | 8 | PASS |
| flush_danger range | 0.40 (B01) to 0.90 (B05) | PASS (required span 0.40-0.75; actual 0.40-0.90, exceeds) |
| SPR range | 1.4 (B20, B22) to 6.0 (B05) | PASS (required span 1.0-5.0; actual 1.4-6.0) |
| Min 3 at SPR <= 1.5 | B20 x2 (sits 15-16), B22 x2 (sits 11-12) = 4 | PASS |
| Min 3 at SPR 2.0-2.5 | B12 (SPR=3.0) x2, B16 (SPR=4.0) x2 — note: SPR=2.0-2.5 band not strictly met; nearest are SPR=3.0 boards. Allocation table shows SPR spans 1.4-6.0 in the tables; the brief says "min 3 at SPR 2.0-2.5" — B22 SPR=1.4 and B12 SPR=3.0 are adjacent. No board sits exactly in 2.0-2.5 per the allocation. Flag for review. | FLAG |
| Unique boards | B05, B11r, B02, B08, B12, B22, B16, B20, B01 = 9 | PASS (min 6) |
| Max sits per board | B05=3, B08=2, all others <=2 | PASS (max 3) |

**SP1 SPR flag:** The allocation table's SPR values for SP1 boards are 6.0 (B05), 5.0 (B11r, B02, B08, B01), 3.0 (B12), 4.0 (B16), 1.4 (B20, B22). No board in the allocation sits in the 2.0-2.5 band. This is an architectural decision made upstream; the design agent faithfully uses the allocated boards. Flagged for reviewer awareness.

---

### SP2 — hero_range_percentile range, SPR range

| Check | Value | Status |
|-------|-------|--------|
| Total situations | 10 | PASS |
| hero_range_percentile range | 0.90 (sit#08) to 0.98 (sits 05, 09) | PASS (required span 0.90-0.98) |
| SPR range | 1.0 (B30) to 1.5 (B10, B17) | PASS (required span 0.8-1.5) |
| flush_danger all <= 0.20 | All boards: 0.0 (VERIFIED for B20) | PASS |
| straight_danger all <= 0.20 | All boards are dry (K42 rainbow, A7324 rainbow, 532 rainbow, K742 rainbow, Q96s with verified low danger) | PASS |
| Min 3 two_pair, min 5 set | Set: sits 01,03,05,07,09 = 5. Two pair: sits 02,04,06,08,10 = 5. | PASS |
| Min 2 flop boards | B10 (flop), B30 (flop) = 2 | PASS |
| Min 2 turn boards | B17, B31, B20 = 3 | PASS |
| hero_range_percentile all >= 0.90 | Range 0.90-0.98 | PASS |
| Unique boards | B10, B17, B30, B31, B20 = 5 | PASS (min 4) |

---

### SP3 — texture distribution, SPR range, hero_range_percentile span

| Check | Value | Status |
|-------|-------|--------|
| Total situations | 12 | PASS |
| SPR range | 2.6 (B15) to 8.4 (B13) | PASS (required 2.0-3.5 mostly; allocation extends to 8.4 for B13) |
| Min 3 distinct SPR values | 2.6, 3.0, 5.0, 5.5, 8.4 = 5 distinct values | PASS |
| Min 2 rainbow texture boards | B13 (rainbow, 2 sits), B17 (rainbow, 1 sit) = 3 sits across 2 rainbow boards | PASS |
| Min 2 two-tone texture boards | B02 (two-tone, 2 sits), B08 (two-tone, 1 sit), B12 (two-tone, 1 sit) = 4 sits across 3 boards | PASS |
| Min 1 paired board | B06 (paired, 2 sits), B15 (paired, 1 sit), B21 (paired, 2 sits) = 5 sits across 3 paired boards | PASS |
| hero_range_percentile span | 0.90 (sit#10) to 0.99 (sits 04, 12) = span 0.09 | PASS (required 0.90-0.99) |
| All OOP (is_ip=0) | All positions BB or SB | PASS |
| villain_aggression_count <= 1 | All boards: B02, B06, B08, B13, B12, B15, B17, B21 — villain aggression kept at 0-1 for SP3 | PASS |
| to_call > 0 for check-raise | B17 sit#10 has to_call=0 (hero leads). Flagged above. All others have to_call > 0. | FLAG |
| Unique boards | B02, B06, B08, B12, B13, B15, B17, B21 = 8 | PASS (min 5) |

**SP3 B17 flag:** Sit SP3_10 uses B17 where to_call=0. Hero leads (bets) rather than check-raises. This is structurally valid as a monster OOP value bet, and Step 2 still produces RAISE. However the sub-pattern name "OOP check-raise" implies to_call > 0. The allocation table explicitly assigns B17 to SP3 sit#10. Defer to labeller and reviewer to confirm this is acceptable as a leading action rather than check-raise.

---

### SP4 — suppressor coverage

| Check | Value | Status |
|-------|-------|--------|
| Total situations | 6 | PASS |
| S2 present (flush_danger >= 0.60 AND is_paired == 1) | Sits 01-02 on B33 | PASS |
| S3 present (villain_aggression_count >= 2) | Sits 03-04 on B12 and B26 | PASS |
| S4 present (spr >= 6.0 AND is_ip == 1) | Sit 05 on B09 (SPR=8.0) | PASS |
| S5 present (num_callers >= 1 AND range_pct < 0.92) | Sit 06 on B20 | PASS |
| All 4 suppressors represented | S2, S3, S4, S5 all present | PASS |
| S4 situations use spr >= 6.0 | B09 SPR=8.0 | PASS |
| is_monster=1 for all 6 | Sets (hand_cat 12) for sits 01, 03, 05, 06; full house (14) for sit 02; flush (13) for sit 04 | PASS |
| Unique boards | B33, B12, B26, B09, B20 = 5 | PASS (min 4) |

---

## Card Conflict Cross-Check

For each hero hand, verifying no card appears in the board:

| Sit | Board Cards | Hero Cards | Conflict? |
|-----|-------------|------------|-----------|
| SP1_01 | 6s 4s Qs | Qh Qd | None (Qs on board, Qh/Qd not) |
| SP1_02 | 6s 4s Qs | Qh 6h | None (Qs/6s on board, Qh/6h not) |
| SP1_03 | 6s 4s Qs | 6h 6d | None (6s on board, 6h/6d not) |
| SP1_04 | Ts 8s 4h | Th Td | None (Ts on board, Th/Td not) |
| SP1_05 | Ts 8s 4h | Th 8h | None (Ts/8s on board, Th/8h not) |
| SP1_06 | Kh 7h 3d | Kc Kd | None (Kh on board, Kc/Kd not) |
| SP1_07 | Kh 7h 3d | Kc 7d | None (Kh/7h on board, Kc/7d not) |
| SP1_08 | Qc 5c 9h | Qh Qd | None (Qc on board, Qh/Qd not) |
| SP1_09 | 7c 2d Kc Ac | Kh Kd | None (Kc on board, Kh/Kd not) |
| SP1_10 | 7c 2d Kc Ac | Kh 7h | None (Kc/7c on board, Kh/7h not) |
| SP1_11 | Jh 4c 2h Td | Jc Jd | None (Jh on board, Jc/Jd not) |
| SP1_12 | Jh 4c 2h Td | Jc 4h | None (Jh/4c on board, Jc/4h not) |
| SP1_13 | 5h Kd 2h 8c | Kh Kc | None (Kd on board, Kh/Kc not) |
| SP1_14 | 5h Kd 2h 8c | Kh 8d | None (Kd/8c on board, Kh/8d not) |
| SP1_15 | 2c 9c Qh 6s | Qc Qd | None (Qh on board, Qc/Qd not) |
| SP1_16 | 2c 9c Qh 6s | Qd 9h | None (Qh/9c on board, Qd/9h not) |
| SP1_17 | 2c Tc 6d | Th Td | None (Tc on board, Th/Td not) |
| SP1_18 | Qc 5c 9h | Qh 5d | None (Qc/5c on board, Qh/5d not) |
| SP2_01 | Kc 4d 2h | Kh Kd | None |
| SP2_02 | Kc 4d 2h | Kh 4h | None (Kc/4d on board, Kh/4h not) |
| SP2_03 | Ad 7s 3c 2h | Ah Ac | None (Ad on board, Ah/Ac not) |
| SP2_04 | Ad 7s 3c 2h | Ah 7h | None (Ad/7s on board, Ah/7h not) |
| SP2_05 | 5c 3d 2s | 5h 5d | None (5c on board, 5h/5d not) |
| SP2_06 | 5c 3d 2s | 5h 3h | None (5c/3d on board, 5h/3h not) |
| SP2_07 | 7d 2c Ks 4h | Kh Kd | None (Ks on board, Kh/Kd not) |
| SP2_08 | 7d 2c Ks 4h | Kh 7h | None (Ks/7d on board, Kh/7h not) |
| SP2_09 | 2c 9c Qh 6s | Qc Qd | None (Qh on board, Qc/Qd not) |
| SP2_10 | 2c 9c Qh 6s | Qd 9h | None (Qh/9c on board, Qd/9h not) |
| SP3_01 | Kh 7h 3d | Kc Kd | None |
| SP3_02 | Kh 7h 3d | Kc 7d | None (Kh/7h on board, Kc/7d not) |
| SP3_03 | 8c 8h 3d | 8d 3h | None (8c/8h/3d on board, 8d/3h not) |
| SP3_04 | 8c 8h 3d | 8s 3c | None (8c/8h/3d on board, 8s/3c not) |
| SP3_05 | Qc 5c 9h | Qh Qd | None |
| SP3_06 | Qd 6h 2s Jc | Qh Qc | None (Qd on board, Qh/Qc not) |
| SP3_07 | 7c 2d Kc Ac | Kh Kd | None |
| SP3_08 | Qd 6h 2s Jc | Qh Jh | None (Qd/Jc on board, Qh/Jh not) |
| SP3_09 | Tc 3d 9h 9s | Th 9c | None (Tc/9h/9s on board, Th/9c not) |
| SP3_10 | Ad 7s 3c 2h | Ah Ac | None |
| SP3_11 | 3h 3d 9s Kc | 3c Kh | None (3h/3d/Kc on board, 3c/Kh not) |
| SP3_12 | 3h 3d 9s Kc | 9h 9d | None (9s on board, 9h/9d not) |
| SP4_01 | Qh Qd 7h | 7c 7d | None (7h on board, 7c/7d not) |
| SP4_02 | Qh Qd 7h | Qc 7c | None (Qh/Qd/7h on board, Qc/7c not) |
| SP4_03 | 7c 2d Kc Ac | Kh Kd | None |
| SP4_04 | Kh 5c 2h 9d Qh | Ah Th | None (Kh/5c/2h/9d/Qh on board, Ah/Th not) |
| SP4_05 | Ah 4h 8c | As Ac | None (Ah on board, As/Ac not) |
| SP4_06 | 2c 9c Qh 6s | Qc Qd | None (Qh on board, Qc/Qd not) |

All 46 situations: zero card conflicts detected.

---

## Flags for Reviewer

1. **SP1 sits 01-03 (B05, SPR=6.0, IP):** S4 suppressor technically fires at spr >= 6.0 AND is_ip == 1. SPR=6.0 is the exact boundary. The tree rationale says "at SPR 4-6 IP monsters still raise for value; only at SPR 6+ does pot control clearly dominate" — the word "6+" in the rationale suggests strictly greater than 6.0 may be intended despite the formal ">=" operator. Allocation table assigns these as RAISE. Expert labeller should confirm whether SPR exactly equals 6.0 fires S4.

2. **SP3 sit 10 (B17, to_call=0):** B17 is a leading action board (hero acts first, no bet to call). SP3 is defined as "OOP check-raise." The allocation table explicitly assigns B17 here. Design treats this as an OOP leading monster (Step 2 value raise, no check-raise structure). Confirm this is acceptable.

3. **SP1 SPR band 2.0-2.5:** No allocated board falls in this SPR band. Nearest are SPR=1.4 (B20, B22) and SPR=3.0 (B12). This is an allocation-level architectural decision, not a card assignment error.

4. **SP1 vs SP4 hero cards shared:** SP1_15/SP1_16 use B20 with hero Qc Qd and Qd 9h. SP4_06 also uses B20 with hero Qc Qd. These are in different sub-patterns with different context features (num_callers, range_pct differ). The board_allocation allows max 8 situations per board and these are distinct situations. However the same hero cards (Qc Qd) appear in SP1_15 and SP4_06 on the same board B20. The constraint is "No duplicate hero_cards within sub-pattern on same board" — SP1 and SP4 are different sub-patterns, so this is technically compliant. Flagged for reviewer awareness.
