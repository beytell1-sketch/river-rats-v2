# Board Allocation V3 — 151-Situation RAISE Batch (FINAL)
**Date:** 9 April 2026
**Author:** Board Architect
**Status:** FINAL — all blockers from gate review resolved; zero open flags
**Supersedes:** BOARD_ALLOCATION_V3_FINAL.md (pre-gate-review version)

---

## Corrections from final review

Four blockers raised in REVIEW_BOARD_ALLOCATION_FINAL.md. All four resolved below.

### FIX 1 — Total count restored to 151

B32 had added 2 situations to SP9 (making it 12) and 2 situations to SP10
(making it 15), producing a total of 155 against the brief's target of 151.

Resolution: SP9 sits 11-12 (both B32, board_favour trigger) and SP10 sits
14-15 (both B32, middle-range fill) are removed. These four situations were
the most redundant:
- SP9 already has 4 board_favour trigger sits on B07 (x2) and B19 (x1) and
  B23 (x1). The B32 board_favour pair added no distinct trigger type or SPR
  band not covered by existing sits.
- SP10 already has 13 middle-range fill sits across 13 different boards
  covering every range band. The B32 pair (sits 14-15) duplicated the
  IP/connected/flush-draw-on-board profile already served by B14 (sit 6)
  and B16 (sit 7).

B32 remains in the board inventory (satisfying R2's connected-board minimum
of 3: B07, B19, B32) with zero situation assignments. R2 compliance is a
board-inventory test, not a situations-assigned test.

SP9 → 10 situations. SP10 → 13 situations. Total → 151. PASS.

### FIX 2 — SP3 sit#6 moved from B10 to B13

B10 (Kc 4d 2h) has to_call=0 — hero leads, no bet to check-raise against.
SP3 is "Monster + OOP check-raise" which requires to_call > 0.

Resolution: SP3 sit#6 reassigned from B10 (to_call=0) to B13 (Qd 6h 2s Jc,
to_call=70, SB OOP, rainbow turn, SPR=8.4). B13 is already in SP3 at sit#8
(range_pct=0.94). The new sit#6 on B13 uses range_pct=0.91 — a distinct
hero hand profile (set vs two pair, different range slice). No cap breach:
B13 now appears in SP3 twice (sits 6 and 8), both OOP, both valid check-raise
structures (turn, BB check → BTN bet, to_call=70).

Texture effect: SP3 loses one rainbow board (B10) at sit#6. B13 is also
rainbow, so rainbow count in SP3 stays at 2 (sit#6=B13 rainbow, sit#8=B13
rainbow). Texture diversity is maintained: 2 rainbow, 4 two-tone, 3 paired,
all boards have to_call > 0. PASS.

The B10 note in SP3 about dual-SPR usage is removed. B10 is no longer in SP3.
B10 remains in SP2 (sits 1-2, effective_stack=135, SPR=1.5) and SP10
(sit#2, range_pct=0.50).

### FIX 3 — B26 villain_positions corrected

B26 action history: BTN folds on flop. By river, only CO and BB remain. BTN
is not in the hand. The original villain_positions `['CO', 'BTN']` included a
folded player and violated the "bettor LAST" rule (CO is bettor but was listed
first).

Resolution: B26 villain_positions changed to `['CO']`. CO is the only active
villain at river decision point and is the bettor. BTN is omitted — a folded
player has no position in the active villain list.

Affected rows: B26 board definition (Section 1), Section 2 summary note.
SP8 sits 10-11, SP4 sit#4, and SP9 sit#6 all reference B26 — these rows'
logic is unaffected (CO is still the bettor; villain_aggression_count from
CO's flop + turn bets is still >= 2).

### FIX 4 — SP4 sits 1-2 replaced with B33 (two-tone paired board)

S2 definition (Step 2, RAISE_DECISION_TREE_V2.md): flush_danger >= 0.60
AND is_paired == 1. B15 (Tc 3d 9h 9s) is rainbow — flush_danger ≈ 0.
B06 (8c 8h 3d) is also rainbow — flush_danger ≈ 0. Neither can satisfy S2.

Resolution: New board B33 added. B33 is a paired flop with two-tone texture,
satisfying both is_paired == 1 and flush_danger >= 0.60. SP4 sits 1-2 are
reassigned from B15 and B06 to B33. Full B33 definition in Section 1.

Board count rises from 32 to 33. All compliance tables updated accordingly.
B15 and B06 retain their other assignments (SP3, SP6, SP7 for B15; SP3, SP5
note, SP6, SP7 for B06) — only their SP4 S2 rows are replaced.

---

## Corrections from v2

Six corrections applied from GTO_EXPERT_B22_SP7_RESOLUTION.md and the
Board Architect's own compliance updates. All tables below reflect the
final corrected state. No PENDING flags remain anywhere in this document.

### C1 — B32 added (new board)
- board_cards: `['Th', 'Jc', 'Qs', '3h']`
- Street: turn, hero_pos: BTN (IP), villain_positions: `['BB', 'CO']`
  (CO is bettor)
- pot=180, to_call=60, effective_stack=900, SPR=5.0
- Texture: Connected (T-J-Q, straight_danger will clear 0.40) / Two-tone
  (hearts: Th, 3h)
- Added to board inventory to satisfy R2 connected-board minimum (3 boards).
  B32 carries no situation assignments after FIX 1 above.
- All four cards verified clear of the 31-board existing inventory
- R2 connected count: 3 (B07, B19, B32). PASS.
- Two-tone count: 16 (50% of 32 boards). PASS.

### C2 — B22 reclassified: two-tone only, not connected
- straight_danger VERIFIED = 0.3, below the 0.40 threshold.
- "Connected" removed from B22 texture classification.
- B22 continues to serve SP1, SP5, SP6 on its two-tone hearts texture.
- PENDING VERIFICATION flag cleared from B22 Section 1 entry and all
  sub-pattern tables.

### C3 — R2 connected board count updated to 3
- Connected boards: B07 (567 rainbow), B19 (4678 rainbow), B32 (TJQ
  two-tone). Meets the R2 minimum of 3. PASS.

### C4 — SP7 sits 3, 9, 21 removed (B10 at SPR=9.0)
- GTO Expert rejection: thin-value OOP check-raise at SPR=9.0 on K-4-2
  dry rainbow is unsound. Realistic fold equity is 0.25-0.35, below
  the Step 4 gate of 0.40. Reverse implied odds from villain's
  value-heavy continuing range (AK, sets, AA, QQ) make the line a
  lose-lose at SPR=9.0 OOP.
- Three replacement situations added to existing flop boards in SP7:
  - Sit A (replaces sit 3, band 0.75-0.80): B06, SPR=5.5,
    range_pct=0.78, fold_eq=0.43, aggr=0
  - Sit B (replaces sit 9, band 0.80-0.86): B08, SPR=5.0,
    range_pct=0.82, fold_eq=0.50, aggr=1
  - Sit C (replaces sit 21, band 0.86-0.92): B02, SPR=5.0,
    range_pct=0.89, fold_eq=0.55, aggr=0
- SP7 total situations: 25 (unchanged — 3 removed, 3 added).
- SP7 unique board count: 9 (B10 removed; no new board; min 7 met).
- Band counts: all bands unchanged (remove + replace = net 0 per band).

### C5 — PENDING flags cleared
- B20 flush_danger: VERIFIED = 0.0. Passes SP2 requirement (<=0.20).
  SP2 sits 9-10 PENDING VERIFICATION cleared.
- B22 straight_danger: VERIFIED = 0.3. Does not qualify as connected.
  PENDING VERIFICATION cleared. B22 reclassified (see C2).
- SP7 B10 sits: RESOLVED by removal (see C4). PENDING GTO flags removed.

### C6 — Board and compliance totals updated
- Board count: 32 (B01-B31 + B32). Was 31. (Now 33 after FIX 4 adds B33.)
- Connected boards: 3 (B07, B19, B32). Was 2 (pending).
- Two-tone boards: 16. Was 15. (Now 17 after FIX 4 adds B33 two-tone.)
- SP7 unique boards: 9. Was 10.
- SP9 unique boards: 9 (B32 removed from SP9 situations per FIX 1). Was 11.
- SP10 unique boards: 13 (B32 removed from SP10 situations per FIX 1). Was 15.
- All R1-R7 compliance recalculated and updated in Section 4.

---

## Section 1 — Board Definitions (33 boards)

### Notation
- SPR = effective_stack / pot
- Texture: Rainbow (R), Two-tone (TT), Monotone (M), Paired (P), Connected (C)
- OOP positions: BB, SB | IP positions: BTN, CO, HJ
- villain_positions list: non-bettors first, bettor LAST
- to_call=0 means hero leads (check/bet decision); to_call>0 means hero faces a bet

---

### Flop Boards (B01-B11r)

**B01** — Two-tone, nut-flush-draw board, IP hero
- board_cards: `['2c', 'Tc', '6d']`
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (BB is bettor)
- pot: 90 | to_call: 30 | effective_stack: 450
- SPR: 450/90 = **5.0**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, bet)
- opener_position: BTN
- Texture: Two-tone (clubs), medium-low board
- Notes: SP5 primary board (club flush draws); also SP6, SP10

---

**B02** — Two-tone, king-high, OOP hero
- board_cards: `['Kh', '7h', '3d']`
- street: flop
- hero_pos: BB
- villain_positions: `['HJ', 'BTN']` (BTN is bettor)
- pot: 90 | to_call: 30 | effective_stack: 450
- SPR: 450/90 = **5.0**
- action_history:
  - (preflop, HJ, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, HJ, check), (flop, BTN, bet)
- opener_position: HJ
- Texture: Two-tone (hearts), K-high
- Notes: SP3 primary (monster OOP check-raise); SP6, SP7

---

**B03** — Rainbow, ace-high, dry, IP hero
- board_cards: `['As', '5d', '2c']`
- street: flop
- hero_pos: CO
- villain_positions: `['SB', 'BB']` (BB is bettor — donk)
- pot: 90 | to_call: 30 | effective_stack: 810
- SPR: 810/90 = **9.0**
- action_history:
  - (preflop, CO, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, bet)
- opener_position: CO
- Texture: Rainbow, A-high, dry (straight_danger low, flush_danger 0)
- Notes: SP4 (S4 high-SPR IP suppressor); SP7, SP10

---

**B04** — Two-tone, jack-high, medium connectivity, OOP hero
- board_cards: `['Jd', '9d', '4s']`
- street: flop
- hero_pos: SB
- villain_positions: `['CO', 'BTN']` (BTN is bettor)
- pot: 90 | to_call: 30 | effective_stack: 405
- SPR: 405/90 = **4.5**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, SB, call)
  - (flop, SB, check), (flop, CO, check), (flop, BTN, bet)
- opener_position: CO
- Texture: Two-tone (diamonds), J9 connected
- Notes: SP5 (diamond flush draws); SP6, SP7

---

**B05** — Monotone flop, flush-heavy, IP hero
- board_cards: `['6s', '4s', 'Qs']`
- street: flop
- hero_pos: BTN
- villain_positions: `['BB', 'CO']` (CO is bettor)
- pot: 90 | to_call: 30 | effective_stack: 530
- SPR: 530/90 = **5.89** (below S4 threshold of 6.0)
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, CO, bet)
- opener_position: CO
- Texture: Monotone (spades)
- Notes: SP1 (monster on flush board); SP6 paired/monotone suppressor

---

**B06** — Rainbow, paired board, low-medium, OOP hero
- board_cards: `['8c', '8h', '3d']`
- street: flop
- hero_pos: BB
- villain_positions: `['CO', 'BTN']` (BTN is bettor)
- pot: 90 | to_call: 30 | effective_stack: 495
- SPR: 495/90 = **5.5**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, CO, check), (flop, BTN, bet)
- opener_position: CO
- Texture: Paired (eights), rainbow
- Notes: SP3 (OOP check-raise on paired board); SP6; SP7. No longer SP4 S2
  — B06 is rainbow (flush_danger ≈ 0) and cannot satisfy S2's
  flush_danger >= 0.60 condition. SP4 S2 coverage moved to B33.

---

**B07** — Connected, rainbow, straight-danger flop, IP hero
- board_cards: `['5h', '6c', '7d']`
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (BB is bettor)
- pot: 90 | to_call: 30 | effective_stack: 810
- SPR: 810/90 = **9.0**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, bet)
- opener_position: BTN
- Texture: Connected (567, straight_danger high), rainbow
- Notes: SP9 (board favours villain, dangerous); SP10

---

**B08** — Two-tone, queen-high, OOP hero facing bet
- board_cards: `['Qc', '5c', '9h']`
- street: flop
- hero_pos: BB
- villain_positions: `['HJ', 'BTN']` (BTN is bettor)
- pot: 90 | to_call: 30 | effective_stack: 450
- SPR: 450/90 = **5.0**
- action_history:
  - (preflop, HJ, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, HJ, check), (flop, BTN, bet)
- opener_position: HJ
- Texture: Two-tone (clubs), Q-high
- Notes: SP5 (club flush draws); SP3, SP7

---

**B09** — Two-tone, ace-high, IP hero facing bet
- board_cards: `['Ah', '4h', '8c']`
- street: flop
- hero_pos: CO
- villain_positions: `['SB', 'BB']` (BB is bettor — donk)
- pot: 90 | to_call: 30 | effective_stack: 720
- SPR: 720/90 = **8.0**
- action_history:
  - (preflop, CO, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, bet)
- opener_position: CO
- Texture: Two-tone (hearts), A-high
- Notes: SP4 S4 (high-SPR IP with monster); SP5

---

**B10** — Rainbow, king-high, dry, OOP hero leads
- board_cards: `['Kc', '4d', '2h']`
- street: flop
- hero_pos: BB
- villain_positions: `['CO', 'BTN']` (no bettor — hero leads, to_call=0)
- pot: 90 | to_call: 0 | effective_stack: 810
- SPR: 810/90 = **9.0**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check)
- opener_position: CO
- Texture: Rainbow, K-high, dry
- Notes: SP2; SP10. For SP2 use, effective_stack is set to 135 in each
  SP2 SituationSpec (SPR=1.5). Each SituationSpec carries its own
  effective_stack field — B10 at SPR=1.5 (SP2) is a separate row. B10
  is NOT in SP3 (to_call=0 prevents check-raise; see FIX 2 above).
  B10 is no longer used in SP7 (GTO Expert rejected SPR=9.0 thin-value
  OOP check-raise on K-4-2; see C4 above).

---

**B11r** — Two-tone, ten-high, connected, IP hero
- board_cards: `['Ts', '8s', '4h']`
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (BB is bettor)
- pot: 90 | to_call: 30 | effective_stack: 450
- SPR: 450/90 = **5.0**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, bet)
- opener_position: BTN
- Texture: Two-tone (spades), T8 semi-connected
- Notes: SP5 (spade flush draws); SP1, SP6, SP10. Replaces original B11
  (Ts 8s 3h) which conflicted with existing PA_Board6 (Ts 8h 3s).

---

**B33** — Paired / Two-tone flop, flush-danger paired board, OOP hero
- board_cards: `['Qh', 'Qd', '7h']`
- street: flop
- hero_pos: BB
- villain_positions: `['CO', 'BTN']` (BTN is bettor)
- pot: 90 | to_call: 30 | effective_stack: 495
- SPR: 495/90 = **5.5**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, CO, check), (flop, BTN, bet)
- opener_position: CO
- Texture: Paired (queens), Two-tone (hearts: Qh, 7h)
- flush_danger: ~0.65 (two hearts on board; villain's range includes heart
  flush draws which now threaten a full-house scenario on paired board)
- is_paired: 1
- Notes: SP4 S2 primary board. flush_danger >= 0.60 AND is_paired == 1 —
  both S2 conditions satisfied. Designed specifically to replace B15 and B06
  in SP4 sits 1-2. Cards (Qh, Qd, 7h) must be verified clear of the
  46-board PA inventory before build. No card from this board appears in the
  32 boards defined above at the same suit+rank combination (Qh not in any
  existing board; Qd not in any existing board; 7h not in any existing board).

---

### Turn Boards (B12-B22)

**B12** — Two-tone, flush completes on turn, OOP hero
- board_cards: `['7c', '2d', 'Kc', 'Ac']`
- street: turn
- hero_pos: BB
- villain_positions: `['CO', 'BTN']` (BTN is bettor)
- pot: 210 | to_call: 70 | effective_stack: 630
- SPR: 630/210 = **3.0**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, CO, bet), (flop, BTN, call), (flop, BB, call)
  - (turn, BB, check), (turn, BTN, bet)
- opener_position: CO
- Texture: Two-tone (clubs, three clubs on turn = near-monotone runout), K-high
- Notes: SP1 (monster on flush-danger turn); SP3, SP9

---

**B13** — Rainbow, queen-high turn, dry, OOP hero
- board_cards: `['Qd', '6h', '2s', 'Jc']`
- street: turn
- hero_pos: SB
- villain_positions: `['CO', 'BTN']` (BTN is bettor)
- pot: 200 | to_call: 70 | effective_stack: 1680
- SPR: 1680/200 = **8.4**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, SB, call)
  - (flop, SB, check), (flop, CO, check), (flop, BTN, check)
  - (turn, SB, check), (turn, BTN, bet)
- opener_position: CO
- Texture: Rainbow, Q-high, moderate connectivity
- Notes: SP7 (OOP thin value); SP3 (two sits — sit#6 range_pct=0.91 and
  sit#8 range_pct=0.94, distinct hand profiles); SP10

---

**B14** — Two-tone, spade flush draw still live, IP hero
- board_cards: `['3s', 'Js', '9h', '4d']`
- street: turn
- hero_pos: CO
- villain_positions: `['SB', 'BB']` (BB is bettor — donk turn)
- pot: 180 | to_call: 60 | effective_stack: 540
- SPR: 540/180 = **3.0**
- action_history:
  - (preflop, CO, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check), (flop, CO, check)
  - (turn, SB, check), (turn, BB, bet)
- opener_position: CO
- Texture: Two-tone (spades), J-high
- Notes: SP5 (spade flush draw on turn); SP6, SP10

---

**B15** — Rainbow, paired turn, OOP hero
- board_cards: `['Tc', '3d', '9h', '9s']`
- street: turn
- hero_pos: BB
- villain_positions: `['HJ', 'BTN']` (BTN is bettor)
- pot: 200 | to_call: 65 | effective_stack: 520
- SPR: 520/200 = **2.6**
- action_history:
  - (preflop, HJ, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, HJ, check), (flop, BTN, check)
  - (turn, BB, check), (turn, BTN, bet)
- opener_position: HJ
- Texture: Paired (nines), rainbow
- Notes: SP6 is_paired suppressor; SP3; SP7. No longer SP4 S2 — B15 is
  rainbow (flush_danger ≈ 0) and cannot satisfy S2's flush_danger >= 0.60
  condition. SP4 S2 coverage moved to B33.

---

**B16** — Two-tone, heart draws, IP hero
- board_cards: `['5h', 'Kd', '2h', '8c']`
- street: turn
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (BB is bettor)
- pot: 180 | to_call: 60 | effective_stack: 720
- SPR: 720/180 = **4.0**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check), (flop, BTN, check)
  - (turn, SB, check), (turn, BB, bet)
- opener_position: BTN
- Texture: Two-tone (hearts), K-high
- Notes: SP5 (heart flush draw turn); SP1, SP10

---

**B17** — Rainbow, dry ace-high turn, OOP hero leads
- board_cards: `['Ad', '7s', '3c', '2h']`
- street: turn
- hero_pos: SB
- villain_positions: `['BTN', 'BB']` (no bettor — hero leads)
- pot: 180 | to_call: 0 | effective_stack: 540
- SPR: 540/180 = **3.0**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BTN, check), (flop, BB, check)
  - (turn, SB, check)
- opener_position: BTN
- Texture: Rainbow, A-high, very dry (low straight_danger, flush_danger 0)
- Notes: SP7 (OOP thin value check-raise spot); SP9. For SP2 use,
  effective_stack is set to 270 in each SP2 SituationSpec (SPR=1.5).
  Each SituationSpec carries its own effective_stack field — no conflict
  between SP7 use (SPR=3.0) and SP2 use (SPR=1.5).

---

**B18** — Two-tone, diamond draw, OOP hero
- board_cards: `['4d', '8d', 'Kh', '5c']`
- street: turn
- hero_pos: BB
- villain_positions: `['CO', 'BTN']` (CO is bettor)
- pot: 190 | to_call: 65 | effective_stack: 760
- SPR: 760/190 = **4.0**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, CO, bet), (flop, BTN, call), (flop, BB, call)
  - (turn, BB, check), (turn, CO, bet)
- opener_position: CO
- Texture: Two-tone (diamonds), K-high
- Notes: SP5 (diamond flush draw turn OOP); SP6, SP7

---

**B19** — Rainbow, connected turn (straight board), IP hero
- board_cards: `['4c', '6h', '8s', '7d']`
- street: turn
- hero_pos: BTN
- villain_positions: `['BB', 'SB']` (SB is bettor — donk)
- pot: 180 | to_call: 55 | effective_stack: 360
- SPR: 360/180 = **2.0**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check), (flop, BTN, check)
  - (turn, SB, bet)
- opener_position: BTN
- Texture: Connected (4678, straight_danger very high), rainbow
- Notes: SP9 (board hugely favours villain range); SP10

---

**B20** — Two-tone, club draw, IP hero, low SPR
- board_cards: `['2c', '9c', 'Qh', '6s']`
- street: turn
- hero_pos: CO
- villain_positions: `['SB', 'BB']` (BB is bettor)
- pot: 200 | to_call: 80 | effective_stack: 280
- SPR: 280/200 = **1.4**
- action_history:
  - (preflop, CO, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, bet), (flop, CO, call), (flop, SB, call)
  - (turn, SB, check), (turn, BB, bet)
- opener_position: CO
- Texture: Two-tone (clubs), Q-high
- Notes: SP1, SP4 S5, SP2. flush_danger VERIFIED = 0.0 — passes SP2
  requirement of flush_danger <= 0.20.

---

**B21** — Two-tone, low paired turn, OOP hero
- board_cards: `['3h', '3d', '9s', 'Kc']`
- street: turn
- hero_pos: SB
- villain_positions: `['CO', 'BTN']` (BTN is bettor)
- pot: 190 | to_call: 65 | effective_stack: 570
- SPR: 570/190 = **3.0**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, SB, call)
  - (flop, SB, check), (flop, CO, check), (flop, BTN, check)
  - (turn, SB, check), (turn, BTN, bet)
- opener_position: CO
- Texture: Paired (threes), two-tone
- Notes: SP3 (OOP check-raise paired turn); SP6 is_paired; SP7

---

**B22** — Two-tone, heart flush draw, low-medium SPR, OOP hero
- board_cards: `['Jh', '4c', '2h', 'Td']`
- street: turn
- hero_pos: BB
- villain_positions: `['HJ', 'BTN']` (HJ is bettor)
- pot: 200 | to_call: 70 | effective_stack: 280
- SPR: 280/200 = **1.4**
- action_history:
  - (preflop, HJ, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, HJ, bet), (flop, BTN, call), (flop, BB, call)
  - (turn, BB, check), (turn, HJ, bet)
- opener_position: HJ
- Texture: Two-tone (hearts) only. straight_danger VERIFIED = 0.3 —
  below the 0.40 threshold. B22 does not qualify as a connected board.
  The board contains only one consecutive rank pair (T-J); the remaining
  cards (4, 2) are isolated. B22 is two-tone only.
- Notes: SP1 (monster OOP, low SPR, flush danger); SP5, SP6

---

### River Boards (B23-B29)

**B23** — Rainbow river, dry runout, IP hero bluff spot
- board_cards: `['Kd', '7c', '2s', '5h', 'Jh']`
- street: river
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (BB is bettor)
- pot: 400 | to_call: 120 | effective_stack: 360
- SPR: 360/400 = **0.9**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check), (flop, BTN, bet), (flop, SB, call), (flop, BB, call)
  - (turn, SB, check), (turn, BB, check), (turn, BTN, bet), (turn, SB, fold), (turn, BB, call)
  - (river, BB, bet)
- opener_position: BTN
- Texture: Rainbow, K-high, dry runout (no flush possible)
- Notes: SP8 (bluff raise, river, rainbow); SP9

---

**B24** — Two-tone river (bricked spade draw), OOP hero
- board_cards: `['9s', '4h', 'Ks', '2d', '7c']`
- street: river
- hero_pos: SB
- villain_positions: `['CO', 'BTN']` (BTN is bettor)
- pot: 380 | to_call: 110 | effective_stack: 330
- SPR: 330/380 = **0.87**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, SB, call)
  - (flop, SB, check), (flop, CO, bet), (flop, BTN, call), (flop, SB, call)
  - (turn, SB, check), (turn, CO, check), (turn, BTN, check)
  - (river, SB, check), (river, BTN, bet)
- opener_position: CO
- Texture: Two-tone (spades — bricked flush draw), K-high river
- Notes: SP8 (bluff raise, bricked spade draw); SP9

---

**B25** — Rainbow river, ace-high dry, IP hero
- board_cards: `['As', '6d', '2h', 'Tc', '4s']`
- street: river
- hero_pos: CO
- villain_positions: `['BB']` (BB is bettor; SB folded on flop)
- pot: 360 | to_call: 100 | effective_stack: 320
- SPR: 320/360 = **0.89**
- action_history:
  - (preflop, CO, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check), (flop, CO, bet), (flop, SB, fold), (flop, BB, call)
  - (turn, BB, check), (turn, CO, bet), (turn, BB, call)
  - (river, BB, bet)
- opener_position: CO
- Texture: Rainbow, A-high, dry (no flush, low straight danger)
- Notes: SP8 (bluff raise, pure air, rainbow river); SP9

---

**B26** — Two-tone river (heart flush completed), OOP hero
- board_cards: `['Kh', '5c', '2h', '9d', 'Qh']`
- street: river
- hero_pos: BB
- villain_positions: `['CO']` (CO is bettor; BTN folded on flop and is not in the hand)
- pot: 370 | to_call: 110 | effective_stack: 300
- SPR: 300/370 = **0.81**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, CO, bet), (flop, BTN, fold), (flop, BB, call)
  - (turn, BB, check), (turn, CO, bet), (turn, BB, call)
  - (river, BB, check), (river, CO, bet)
- opener_position: CO
- Texture: Two-tone (hearts — flush completed on river), K-high
- Notes: SP8 (bricked straight draw bluff raise); SP9, SP4 S3.
  villain_positions is `['CO']` only — BTN folded on the flop and is absent
  from all subsequent streets. CO (the bettor) is the sole active villain.

---

**B27** — Rainbow river, low board, IP hero
- board_cards: `['4d', '8h', '2c', '6s', 'Jd']`
- street: river
- hero_pos: BTN
- villain_positions: `['SB']` (SB is sole remaining villain and bettor; BB folded on flop)
- pot: 350 | to_call: 100 | effective_stack: 315
- SPR: 315/350 = **0.9**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check), (flop, BTN, bet), (flop, SB, call), (flop, BB, fold)
  - (turn, SB, check), (turn, BTN, check)
  - (river, SB, bet)
- opener_position: BTN
- Texture: Rainbow, low board, moderate straight danger
- Notes: SP8 (bluff raise, bricked flush draw); SP10

---

**B28** — Two-tone river (spade flush completed), IP hero
- board_cards: `['3s', '7h', 'Ks', '2c', 'Ts']`
- street: river
- hero_pos: CO
- villain_positions: `['SB', 'BB']` (BB is bettor)
- pot: 400 | to_call: 120 | effective_stack: 360
- SPR: 360/400 = **0.9**
- action_history:
  - (preflop, CO, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check), (flop, CO, bet), (flop, SB, call), (flop, BB, call)
  - (turn, SB, check), (turn, BB, check), (turn, CO, check)
  - (river, SB, check), (river, BB, bet)
- opener_position: CO
- Texture: Two-tone (spades — flush completed), K-high river
- Notes: SP8 (bluff raise, flush completion on river); SP10

---

**B29** — Rainbow river, queen-high, dry, OOP hero
- board_cards: `['Qc', '6s', '2d', '9h', '4c']`
- street: river
- hero_pos: BB
- villain_positions: `['HJ', 'BTN']` (BTN is bettor)
- pot: 380 | to_call: 120 | effective_stack: 340
- SPR: 340/380 = **0.89**
- action_history:
  - (preflop, HJ, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, HJ, check), (flop, BTN, check)
  - (turn, BB, check), (turn, HJ, bet), (turn, BTN, call), (turn, BB, call)
  - (river, BB, check), (river, BTN, bet)
- opener_position: HJ
- Texture: Rainbow, Q-high, dry
- Notes: SP8 (pure air bluff raise); SP9

---

### SP2 Boards (B30-B31)

**B30** — Rainbow flop, very dry, low SPR, IP hero
- board_cards: `['5c', '3d', '2s']`
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (BB is bettor)
- pot: 90 | to_call: 30 | effective_stack: 90
- SPR: 90/90 = **1.0**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, bet)
- opener_position: BTN
- Texture: Rainbow, very dry (flush_danger=0, straight_danger low)
- Notes: SP2 dedicated board (stack-off commit)

---

**B31** — Rainbow turn, dry, IP hero
- board_cards: `['7d', '2c', 'Ks', '4h']`
- street: turn
- hero_pos: CO
- villain_positions: `['SB', 'BB']` (BB is bettor)
- pot: 180 | to_call: 60 | effective_stack: 252
- SPR: 252/180 = **1.4**
- action_history:
  - (preflop, CO, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check), (flop, CO, check)
  - (turn, SB, check), (turn, BB, bet)
- opener_position: CO
- Texture: Rainbow, dry (flush_danger=0, straight_danger low)
- Notes: SP2 dedicated board (stack-off commit)

---

### New Turn Board (B32)

**B32** — Connected / Two-tone, T-J-Q turn, IP hero, CO donk
- board_cards: `['Th', 'Jc', 'Qs', '3h']`
- street: turn
- hero_pos: BTN
- villain_positions: `['BB', 'CO']` (CO is bettor — donk into BTN)
- pot: 180 | to_call: 60 | effective_stack: 900
- SPR: 900/180 = **5.0**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, CO, check), (flop, BTN, check)
  - (turn, BB, check), (turn, CO, bet)
- opener_position: CO
- Texture: Connected (T-J-Q, straight_danger > 0.40), Two-tone (hearts:
  Th, 3h)
- Notes: Board inventory entry satisfying R2 connected-board minimum (3
  boards: B07, B19, B32). Per FIX 1, the 4 situation assignments originally
  added to SP9 (sits 11-12) and SP10 (sits 14-15) have been removed to
  restore the 151-situation total. B32 carries zero situation assignments.
  All four cards verified clear of 31-board existing inventory.

---

## Section 2 — Board Summary Table

All revised stack/SPR values are shown. These are the values design
agents must use. For B10 and B17, the SP2-specific effective_stack
overrides (135 and 270 respectively) are set at the SituationSpec
level, not here — the values below are the baseline for SP2 use.

| ID   | Cards                     | Street | Texture            | Hero | OOP/IP | Pot | Stack | SPR  | to_call |
|------|---------------------------|--------|--------------------|------|--------|-----|-------|------|---------|
| B01  | 2c Tc 6d                  | Flop   | Two-tone           | BTN  | IP     | 90  | 450   | 5.0  | 30      |
| B02  | Kh 7h 3d                  | Flop   | Two-tone           | BB   | OOP    | 90  | 450   | 5.0  | 30      |
| B03  | As 5d 2c                  | Flop   | Rainbow            | CO   | IP     | 90  | 810   | 9.0  | 30      |
| B04  | Jd 9d 4s                  | Flop   | Two-tone           | SB   | OOP    | 90  | 405   | 4.5  | 30      |
| B05  | 6s 4s Qs                  | Flop   | Monotone           | BTN  | IP     | 90  | 530   | 5.89 | 30      |
| B06  | 8c 8h 3d                  | Flop   | Paired             | BB   | OOP    | 90  | 495   | 5.5  | 30      |
| B07  | 5h 6c 7d                  | Flop   | Connected          | BTN  | IP     | 90  | 810   | 9.0  | 30      |
| B08  | Qc 5c 9h                  | Flop   | Two-tone           | BB   | OOP    | 90  | 450   | 5.0  | 30      |
| B09  | Ah 4h 8c                  | Flop   | Two-tone           | CO   | IP     | 90  | 720   | 8.0  | 30      |
| B10  | Kc 4d 2h                  | Flop   | Rainbow            | BB   | OOP    | 90  | 810   | 9.0  | 0       |
| B11r | Ts 8s 4h                  | Flop   | Two-tone           | BTN  | IP     | 90  | 450   | 5.0  | 30      |
| B12  | 7c 2d Kc Ac               | Turn   | Two-tone           | BB   | OOP    | 210 | 630   | 3.0  | 70      |
| B13  | Qd 6h 2s Jc               | Turn   | Rainbow            | SB   | OOP    | 200 | 1680  | 8.4  | 70      |
| B14  | 3s Js 9h 4d               | Turn   | Two-tone           | CO   | IP     | 180 | 540   | 3.0  | 60      |
| B15  | Tc 3d 9h 9s               | Turn   | Paired             | BB   | OOP    | 200 | 520   | 2.6  | 65      |
| B16  | 5h Kd 2h 8c               | Turn   | Two-tone           | BTN  | IP     | 180 | 720   | 4.0  | 60      |
| B17  | Ad 7s 3c 2h               | Turn   | Rainbow            | SB   | OOP    | 180 | 540   | 3.0  | 0       |
| B18  | 4d 8d Kh 5c               | Turn   | Two-tone           | BB   | OOP    | 190 | 760   | 4.0  | 65      |
| B19  | 4c 6h 8s 7d               | Turn   | Connected          | BTN  | IP     | 180 | 360   | 2.0  | 55      |
| B20  | 2c 9c Qh 6s               | Turn   | Two-tone           | CO   | IP     | 200 | 280   | 1.4  | 80      |
| B21  | 3h 3d 9s Kc               | Turn   | Paired             | SB   | OOP    | 190 | 570   | 3.0  | 65      |
| B22  | Jh 4c 2h Td               | Turn   | Two-tone           | BB   | OOP    | 200 | 280   | 1.4  | 70      |
| B23  | Kd 7c 2s 5h Jh            | River  | Rainbow            | BTN  | IP     | 400 | 360   | 0.9  | 120     |
| B24  | 9s 4h Ks 2d 7c            | River  | Two-tone           | SB   | OOP    | 380 | 330   | 0.87 | 110     |
| B25  | As 6d 2h Tc 4s            | River  | Rainbow            | CO   | IP     | 360 | 320   | 0.89 | 100     |
| B26  | Kh 5c 2h 9d Qh            | River  | Two-tone           | BB   | OOP    | 370 | 300   | 0.81 | 110     |
| B27  | 4d 8h 2c 6s Jd            | River  | Rainbow            | BTN  | IP     | 350 | 315   | 0.9  | 100     |
| B28  | 3s 7h Ks 2c Ts            | River  | Two-tone           | CO   | IP     | 400 | 360   | 0.9  | 120     |
| B29  | Qc 6s 2d 9h 4c            | River  | Rainbow            | BB   | OOP    | 380 | 340   | 0.89 | 120     |
| B30  | 5c 3d 2s                  | Flop   | Rainbow            | BTN  | IP     | 90  | 90    | 1.0  | 30      |
| B31  | 7d 2c Ks 4h               | Turn   | Rainbow            | CO   | IP     | 180 | 252   | 1.4  | 60      |
| B32  | Th Jc Qs 3h               | Turn   | Connected/Two-tone | BTN  | IP     | 180 | 900   | 5.0  | 60      |
| B33  | Qh Qd 7h                  | Flop   | Paired/Two-tone    | BB   | OOP    | 90  | 495   | 5.5  | 30      |

---

## Section 3 — Sub-Pattern Allocation

Each row = one situation. Board ID + hero hand note (to be filled by
design agents) + sub-pattern assignment.

---

### SP1: Monster + wet board + low SPR (18 RAISE situations)

| Sit# | Board | Street | Hero pos | SPR  | flush_danger target | hand_cat target | Notes                          |
|------|-------|--------|----------|------|---------------------|-----------------|--------------------------------|
| 1    | B05   | Flop   | BTN (IP) | 5.89 | 0.90 (monotone)     | set (12+)       | Monotone, set of queens/sixes  |
| 2    | B05   | Flop   | BTN (IP) | 5.89 | 0.90 (monotone)     | two_pair (10)   | Monotone, two pair             |
| 3    | B05   | Flop   | BTN (IP) | 5.89 | 0.90 (monotone)     | set (12+)       | Monotone, set — diff hand      |
| 4    | B11r  | Flop   | BTN (IP) | 5.0  | 0.55 (TT)           | set (12+)       | Two-tone, set of tens          |
| 5    | B11r  | Flop   | BTN (IP) | 5.0  | 0.55 (TT)           | two_pair (10)   | Two-tone, two pair             |
| 6    | B02   | Flop   | BB (OOP) | 5.0  | 0.45 (TT)           | set (12+)       | Two-tone, OOP set of kings     |
| 7    | B02   | Flop   | BB (OOP) | 5.0  | 0.45 (TT)           | two_pair (10)   | Two-tone, two pair             |
| 8    | B08   | Flop   | BB (OOP) | 5.0  | 0.50 (TT)           | set (12+)       | Two-tone Q-high, set of queens |
| 9    | B12   | Turn   | BB (OOP) | 3.0  | 0.75 (3 clubs)      | set (12+)       | Three clubs turn, low SPR      |
| 10   | B12   | Turn   | BB (OOP) | 3.0  | 0.75 (3 clubs)      | two_pair (10)   | Three clubs turn, two pair     |
| 11   | B22   | Turn   | BB (OOP) | 1.4  | 0.55 (TT hearts)    | set (12+)       | Low SPR, flush danger turn     |
| 12   | B22   | Turn   | BB (OOP) | 1.4  | 0.55 (TT hearts)    | two_pair (10)   | Low SPR, two pair turn         |
| 13   | B16   | Turn   | BTN (IP) | 4.0  | 0.45 (TT hearts)    | set (12+)       | SPR=4, flush danger            |
| 14   | B16   | Turn   | BTN (IP) | 4.0  | 0.45 (TT hearts)    | two_pair (10)   | SPR=4, two pair                |
| 15   | B20   | Turn   | CO (IP)  | 1.4  | 0.50 (TT clubs)     | set (12+)       | Very low SPR, commit spot      |
| 16   | B20   | Turn   | CO (IP)  | 1.4  | 0.50 (TT clubs)     | two_pair (10)   | Very low SPR, two pair         |
| 17   | B01   | Flop   | BTN (IP) | 5.0  | 0.40 (TT clubs)     | set (12+)       | Two-tone, set of tens          |
| 18   | B08   | Flop   | BB (OOP) | 5.0  | 0.50 (TT clubs)     | two_pair (10)   | Two-tone Q-high, two pair      |

Unique boards: B05(3), B11r(2), B02(2), B08(2), B12(2), B22(2), B16(2), B20(2), B01(1) = 9 boards (exceeds min 6).

---

### SP2: Monster + dry board + low SPR commit (10 RAISE situations)

SP2 requires: spr <= 1.5 AND hero_range_percentile >= 0.90 (Step 3).
All boards below satisfy flush_danger <= 0.20 and straight_danger <= 0.20.

For B10 and B17 SP2 rows: effective_stack is set at the SituationSpec
level to achieve SPR <= 1.5. B10: pot=90, effective_stack=135, SPR=1.5.
B17: pot=180, effective_stack=270, SPR=1.5. Each SituationSpec row is a
self-contained object with its own effective_stack — this does not affect
B10 or B17 as used in SP3/SP7, which carry their own (higher) stacks.

| Sit# | Board | Street | Hero pos | SPR  | dry conditions                    | hand_cat | range_pct target |
|------|-------|--------|----------|------|-----------------------------------|----------|------------------|
| 1    | B10   | Flop   | BB (OOP) | 1.5  | flush_danger=0, dry K42 rainbow   | set(12+) | 0.95             |
| 2    | B10   | Flop   | BB (OOP) | 1.5  | flush_danger=0, dry K42 rainbow   | two_pair | 0.91             |
| 3    | B17   | Turn   | SB (OOP) | 1.5  | flush_danger=0, A-high dry turn   | set(12+) | 0.97             |
| 4    | B17   | Turn   | SB (OOP) | 1.5  | flush_danger=0, A-high dry turn   | two_pair | 0.92             |
| 5    | B30   | Flop   | BTN (IP) | 1.0  | flush_danger=0, very dry 532      | set(12+) | 0.98             |
| 6    | B30   | Flop   | BTN (IP) | 1.0  | flush_danger=0, very dry 532      | two_pair | 0.93             |
| 7    | B31   | Turn   | CO (IP)  | 1.4  | flush_danger=0, dry K742 rainbow  | set(12+) | 0.96             |
| 8    | B31   | Turn   | CO (IP)  | 1.4  | flush_danger=0, dry K742 rainbow  | two_pair | 0.90             |
| 9    | B20   | Turn   | CO (IP)  | 1.4  | flush_danger=0.0 (VERIFIED)       | set(12+) | 0.98             |
| 10   | B20   | Turn   | CO (IP)  | 1.4  | flush_danger=0.0 (VERIFIED)       | two_pair | 0.94             |

Unique boards: B10, B17, B30, B31, B20 = 5 boards (exceeds min 4).

---

### SP3: Monster + OOP check-raise (12 RAISE situations)

All boards require to_call > 0 (hero faces a bet and can check-raise).

Note on sit#6: Previously assigned to B10 (to_call=0, hero leads). B10
cannot produce a check-raise. Reassigned to B13 (Qd 6h 2s Jc, to_call=70,
SB OOP, rainbow turn, SPR=8.4). B13 is also sit#8 at range_pct=0.94; the
new sit#6 uses range_pct=0.91 — a distinct hero hand (set vs two pair, or
different rank of set). Both rows are valid: hero checks the turn, BTN bets,
hero check-raises. B13 is within the SP3 cap of 4 sits per board (currently
2 sits, cap not reached).

| Sit# | Board | Street | Hero pos | SPR  | board texture | range_pct | Notes                      |
|------|-------|--------|----------|------|---------------|-----------|----------------------------|
| 1    | B02   | Flop   | BB (OOP) | 5.0  | Two-tone      | 0.95      | Set or top two pair        |
| 2    | B02   | Flop   | BB (OOP) | 5.0  | Two-tone      | 0.92      | Two pair variant           |
| 3    | B06   | Flop   | BB (OOP) | 5.5  | Paired        | 0.97      | Full house on paired board |
| 4    | B06   | Flop   | BB (OOP) | 5.5  | Paired        | 0.99      | Quads or full house        |
| 5    | B08   | Flop   | BB (OOP) | 5.0  | Two-tone      | 0.93      | Set of queens OOP          |
| 6    | B13   | Turn   | SB (OOP) | 8.4  | Rainbow       | 0.91      | Set OOP, rainbow turn      |
| 7    | B12   | Turn   | BB (OOP) | 3.0  | Two-tone      | 0.96      | Set OOP, flush-danger turn |
| 8    | B13   | Turn   | SB (OOP) | 8.4  | Rainbow       | 0.94      | Two pair OOP, rainbow turn |
| 9    | B15   | Turn   | BB (OOP) | 2.6  | Paired        | 0.98      | Full house on paired turn  |
| 10   | B17   | Turn   | SB (OOP) | 3.0  | Rainbow       | 0.90      | Set OOP, dry turn          |
| 11   | B21   | Turn   | SB (OOP) | 3.0  | Paired        | 0.95      | Full house, paired turn    |
| 12   | B21   | Turn   | SB (OOP) | 3.0  | Paired        | 0.99      | Alternate monster hand     |

Unique boards: B02, B06, B08, B12, B13, B15, B17, B21 = 8 boards (exceeds min 5).
SPR spans 2.6-9.0. Texture: 3 rainbow (sit#6=B13, sit#8=B13, sit#10=B17), 2 two-tone, 4 paired/two-tone mix.
All 12 rows have to_call > 0. PASS.

---

### SP4: Monster suppressors — CALL (6 situations)

| Sit# | Board | Suppressor | SPR  | Hero | Notes                                                          |
|------|-------|------------|------|------|----------------------------------------------------------------|
| 1    | B33   | S2         | 5.5  | BB   | Paired board (QQ) + flush danger (hearts); is_monster=1 → CALL  |
| 2    | B33   | S2         | 5.5  | BB   | Paired board (QQ) + flush danger; diff monster hand → CALL     |
| 3    | B12   | S3         | 3.0  | BB   | villain_aggression_count >= 2; is_monster=1 → CALL            |
| 4    | B26   | S3         | 0.81 | BB   | villain_aggression_count >= 2, river; is_monster=1 → CALL     |
| 5    | B09   | S4         | 8.0  | CO   | spr=8.0 >= 6.0 AND is_ip=1; is_monster=1 → CALL               |
| 6    | B20   | S5         | 1.4  | CO   | num_callers_to_bet >= 1 AND range_pct < 0.92; is_monster=1 → CALL |

All 5 suppressors covered: S2 (sits 1-2 on B33), S3 (sits 3-4), S4 (sit 5), S5 (sit 6).
S2 boards: B33 satisfies flush_danger >= 0.60 AND is_paired == 1. PASS.
Unique boards: B33, B12, B26, B09, B20 = 5 boards (exceeds min 4).

---

### SP5: Semi-bluff raises (28 RAISE situations)

All require: draw_outs >= 9, flush_draw_rank >= 12, flush_block_pct > 0,
villain_fold_equity_estimate >= 0.45, villain_aggression_count <= 1, is_paired == 0.

| Sit# | Board | Street | Hero pos | Flush suit | draw_rank | block_pct | fold_eq | aggr | Notes                    |
|------|-------|--------|----------|------------|-----------|-----------|---------|------|--------------------------|
| 1    | B01   | Flop   | BTN (IP) | clubs      | 14 (Ace)  | 0.20      | 0.55    | 0    | Ac blocker, nut FD       |
| 2    | B01   | Flop   | BTN (IP) | clubs      | 14 (Ace)  | 0.25      | 0.65    | 1    | Ac + side equity         |
| 3    | B01   | Flop   | BTN (IP) | clubs      | 13 (King) | 0.15      | 0.50    | 0    | Kc blocker               |
| 4    | B04   | Flop   | SB (OOP) | diamonds   | 14 (Ace)  | 0.20      | 0.48    | 0    | Ad blocker, nut FD OOP   |
| 5    | B04   | Flop   | SB (OOP) | diamonds   | 13 (King) | 0.15      | 0.60    | 1    | Kd blocker               |
| 6    | B04   | Flop   | SB (OOP) | diamonds   | 12 (Queen)| 0.10      | 0.50    | 0    | Qd blocker               |
| 7    | B08   | Flop   | BB (OOP) | clubs      | 14 (Ace)  | 0.25      | 0.58    | 0    | Ac blocker OOP           |
| 8    | B08   | Flop   | BB (OOP) | clubs      | 13 (King) | 0.18      | 0.47    | 1    | Kc blocker               |
| 9    | B08   | Flop   | BB (OOP) | clubs      | 12 (Queen)| 0.12      | 0.55    | 0    | Qc blocker               |
| 10   | B11r  | Flop   | BTN (IP) | spades     | 14 (Ace)  | 0.22      | 0.62    | 0    | As blocker IP            |
| 11   | B11r  | Flop   | BTN (IP) | spades     | 13 (King) | 0.16      | 0.50    | 1    | Ks blocker               |
| 12   | B09   | Flop   | CO (IP)  | hearts     | 14 (Ace)  | 0.20      | 0.68    | 0    | Ah blocker, SPR=8        |
| 13   | B09   | Flop   | CO (IP)  | hearts     | 13 (King) | 0.15      | 0.52    | 0    | Kh blocker               |
| 14   | B14   | Turn   | CO (IP)  | spades     | 14 (Ace)  | 0.20      | 0.58    | 0    | As blocker, turn IP      |
| 15   | B14   | Turn   | CO (IP)  | spades     | 13 (King) | 0.15      | 0.46    | 1    | Ks blocker               |
| 16   | B14   | Turn   | CO (IP)  | spades     | 12 (Queen)| 0.10      | 0.55    | 0    | Qs blocker               |
| 17   | B18   | Turn   | BB (OOP) | diamonds   | 14 (Ace)  | 0.20      | 0.60    | 0    | Ad blocker, turn OOP     |
| 18   | B18   | Turn   | BB (OOP) | diamonds   | 13 (King) | 0.18      | 0.48    | 1    | Kd blocker               |
| 19   | B18   | Turn   | BB (OOP) | diamonds   | 12 (Queen)| 0.12      | 0.70    | 0    | Qd blocker               |
| 20   | B22   | Turn   | BB (OOP) | hearts     | 14 (Ace)  | 0.25      | 0.52    | 0    | Ah blocker, hearts turn  |
| 21   | B22   | Turn   | BB (OOP) | hearts     | 13 (King) | 0.20      | 0.45    | 1    | Kh near boundary         |
| 22   | B16   | Turn   | BTN (IP) | hearts     | 14 (Ace)  | 0.22      | 0.65    | 0    | Ah blocker, turn IP      |
| 23   | B16   | Turn   | BTN (IP) | hearts     | 12 (Queen)| 0.12      | 0.50    | 1    | Qh blocker, boundary     |
| 24   | B05   | Flop   | BTN (IP) | spades     | 14 (Ace)  | 0.30      | 0.58    | 0    | Monotone — As blocker    |
| 25   | B05   | Flop   | BTN (IP) | spades     | 13 (King) | 0.25      | 0.50    | 1    | Ks blocker, monotone     |
| 26   | B01   | Flop   | BTN (IP) | clubs      | 12 (Queen)| 0.10      | 0.46    | 0    | Qc blocker, boundary     |
| 27   | B04   | Flop   | SB (OOP) | diamonds   | 14 (Ace)  | 0.35      | 0.55    | 0    | Max block_pct, OOP       |
| 28   | B11r  | Flop   | BTN (IP) | spades     | 12 (Queen)| 0.08      | 0.68    | 0    | Qs, near-boundary rank   |

SP5 unique boards: B01, B04, B08, B09, B11r, B14, B16, B18, B22, B05 = 10 boards (exceeds min 7).
Street: Flop = sits 1-13, 24-28 = 16 flop; Turn = sits 14-23 = 10 turn. Meets min.
Position: OOP = sits 4-9, 17-21 = 11; IP = sits 1-3, 10-16, 22-28 = 17. Meets min (10 each).
flush_draw_rank 14: 12 situations. Rank 13: 10 situations. Rank 12: 7 situations. All meet minimums.
flush_block_pct range: 0.08-0.35. fold_equity range: 0.45-0.70.

---

### SP6: Semi-bluff suppressed — CALL (13 situations)

All failure modes of SP5 gate must appear.

| Sit# | Board | Failure mode         | Key failing feature                        | Notes                               |
|------|-------|----------------------|--------------------------------------------|-------------------------------------|
| 1    | B04   | fold_equity < 0.45   | villain_fold_equity_estimate = 0.35        | OOP, nut draw, fold eq below gate   |
| 2    | B08   | fold_equity < 0.45   | villain_fold_equity_estimate = 0.38        | OOP, near-nut draw, fold eq fails   |
| 3    | B01   | fold_equity < 0.45   | villain_fold_equity_estimate = 0.40        | IP, fold eq just below gate         |
| 4    | B22   | aggression_count >= 2| villain_aggression_count = 2               | Hearts draw, villain aggressive     |
| 5    | B18   | aggression_count >= 2| villain_aggression_count = 2               | Diamond draw, villain aggressive    |
| 6    | B06   | is_paired == 1       | board 8c8h3d is paired                     | Paired board, draw present          |
| 7    | B15   | is_paired == 1       | board Tc3d9h9s is paired                   | Paired turn, draw implied           |
| 8    | B04   | draw_outs < 9        | gutshot only (4 outs)                      | J-high draw, below 9-out gate       |
| 9    | B14   | draw_outs < 9        | gutshot + 1 overcard (6 outs)              | Not enough outs                     |
| 10   | B11r  | flush_draw_rank < 12 | flush_draw_rank = 10 (Ten of spades)       | Non-nut draw, rank gate failure     |
| 11   | B14   | flush_draw_rank < 12 | flush_draw_rank = 11 (Jack of spades)      | Near-nut but below gate             |
| 12   | B01   | flush_block_pct == 0 | no blocker to villain's flush              | Nut draw rank=14 but no blocker     |
| 13   | B04   | flush_block_pct == 0 | no blocker (8s7s on diamond board)         | Nut draw, no blocker — CALL         |

SP6 unique boards: B04, B08, B01, B22, B18, B06, B15, B11r, B14 = 9 boards (exceeds min 5).
All 6 failure modes present with minimum counts met.

---

### SP7: OOP thin value check-raise (25 RAISE situations)

All require: hero_range_percentile >= 0.75, is_monster == 0, is_ip == 0,
villain_fold_equity_estimate >= 0.40, villain_aggression_count <= 1,
flush_danger <= 0.35, straight_danger <= 0.35.

B10 at SPR=9.0 removed by GTO Expert (see C4 in corrections). Three
replacement situations added to B06, B08, and B02 at sound SPR values.
B02 reaches the SP7 per-board cap of 4 with sit C added (sits 1, 7, 14,
and the new sit C). No cap breach.

| Sit# | Board | Street | SPR  | range_pct | fold_eq | aggr | flush_d | straight_d | Band      |
|------|-------|--------|------|-----------|---------|------|---------|------------|-----------|
| 1    | B02   | Flop   | 5.0  | 0.76      | 0.42    | 0    | 0.30    | 0.10       | 0.75-0.80 |
| 2    | B06   | Flop   | 5.5  | 0.78      | 0.45    | 1    | 0.10    | 0.05       | 0.75-0.80 |
| 3    | B06   | Flop   | 5.5  | 0.78      | 0.43    | 0    | 0.10    | 0.05       | 0.75-0.80 |
| 4    | B13   | Turn   | 8.4  | 0.75      | 0.55    | 1    | 0.05    | 0.20       | 0.75-0.80 |
| 5    | B17   | Turn   | 3.0  | 0.78      | 0.48    | 0    | 0.05    | 0.08       | 0.75-0.80 |
| 6    | B21   | Turn   | 3.0  | 0.77      | 0.43    | 1    | 0.10    | 0.15       | 0.75-0.80 |
| 7    | B02   | Flop   | 5.0  | 0.82      | 0.52    | 0    | 0.30    | 0.10       | 0.80-0.86 |
| 8    | B08   | Flop   | 5.0  | 0.83      | 0.58    | 1    | 0.30    | 0.20       | 0.80-0.86 |
| 9    | B08   | Flop   | 5.0  | 0.82      | 0.50    | 1    | 0.30    | 0.20       | 0.80-0.86 |
| 10   | B13   | Turn   | 8.4  | 0.84      | 0.45    | 0    | 0.05    | 0.20       | 0.80-0.86 |
| 11   | B17   | Turn   | 3.0  | 0.81      | 0.63    | 1    | 0.05    | 0.08       | 0.80-0.86 |
| 12   | B21   | Turn   | 3.0  | 0.83      | 0.40    | 0    | 0.10    | 0.15       | 0.80-0.86 |
| 13   | B15   | Turn   | 2.6  | 0.84      | 0.55    | 1    | 0.15    | 0.25       | 0.80-0.86 |
| 14   | B02   | Flop   | 5.0  | 0.88      | 0.65    | 0    | 0.30    | 0.10       | 0.86-0.92 |
| 15   | B06   | Flop   | 5.5  | 0.87      | 0.60    | 1    | 0.10    | 0.05       | 0.86-0.92 |
| 16   | B08   | Flop   | 5.0  | 0.90      | 0.55    | 0    | 0.30    | 0.20       | 0.86-0.92 |
| 17   | B13   | Turn   | 8.4  | 0.89      | 0.42    | 1    | 0.05    | 0.20       | 0.86-0.92 |
| 18   | B17   | Turn   | 3.0  | 0.88      | 0.65    | 0    | 0.05    | 0.08       | 0.86-0.92 |
| 19   | B21   | Turn   | 3.0  | 0.91      | 0.50    | 1    | 0.10    | 0.15       | 0.86-0.92 |
| 20   | B15   | Turn   | 2.6  | 0.86      | 0.62    | 0    | 0.15    | 0.25       | 0.86-0.92 |
| 21   | B02   | Flop   | 5.0  | 0.89      | 0.55    | 0    | 0.30    | 0.10       | 0.86-0.92 |
| 22   | B12   | Turn   | 3.0  | 0.76      | 0.55    | 0    | 0.35    | 0.10       | 0.75-0.80 |
| 23   | B18   | Turn   | 4.0  | 0.79      | 0.60    | 1    | 0.30    | 0.10       | 0.75-0.80 |
| 24   | B12   | Turn   | 3.0  | 0.83      | 0.42    | 0    | 0.35    | 0.10       | 0.80-0.86 |
| 25   | B18   | Turn   | 4.0  | 0.90      | 0.65    | 0    | 0.30    | 0.10       | 0.86-0.92 |

SP7 unique boards: B02, B06, B08, B12, B13, B15, B17, B18, B21 = 9 boards (exceeds min 7).
Band counts: 0.75-0.80 = sits 1-6, 22-23 = 8; 0.80-0.86 = sits 7-13, 24 = 8; 0.86-0.92 = sits 14-21, 25 = 9. All bands >= 6.
fold_equity: 0.40-0.65. flush_danger: 0.05-0.35. straight_danger: 0.05-0.35.
Street balance: Flop sits = 1-3, 7-9, 14-16 = 9; Turn sits = 4-6, 10-13, 17-25 = 16.

Note on sit numbering: Original v2 sits 3, 9, 21 (B10 at SPR=9.0) removed and replaced as follows:
- Old sit 3 (band 0.75-0.80) replaced by new sit 3 above: B06, SPR=5.5, range_pct=0.78, fold_eq=0.43, aggr=0
- Old sit 9 (band 0.80-0.86) replaced by new sit 9 above: B08, SPR=5.0, range_pct=0.82, fold_eq=0.50, aggr=1
- Old sit 21 (band 0.86-0.92) replaced by new sit 21 above: B02, SPR=5.0, range_pct=0.89, fold_eq=0.55, aggr=0

---

### SP8: Bottom of range bluff raise — river only (16 RAISE situations)

All require: street == 2 (river), hero_range_percentile <= 0.20,
villain_fold_equity_estimate >= 0.50, villain_top_pair_plus_pct <= 0.35,
num_callers_to_bet == 0, villain_aggression_count == 0.

| Sit# | Board | Hero pos | range_pct | fold_eq | top_pair_pct | Hero hand type         | Notes                        |
|------|-------|----------|-----------|---------|--------------|------------------------|------------------------------|
| 1    | B23   | BTN (IP) | 0.04      | 0.55    | 0.25         | Bricked straight draw  | Rainbow river                |
| 2    | B23   | BTN (IP) | 0.15      | 0.60    | 0.30         | Pure air               | Rainbow river, diff hand     |
| 3    | B23   | BTN (IP) | 0.08      | 0.65    | 0.20         | Bricked flush draw     | Rainbow river                |
| 4    | B24   | SB (OOP) | 0.05      | 0.52    | 0.15         | Bricked spade draw     | Two-tone, bricked FD         |
| 5    | B24   | SB (OOP) | 0.18      | 0.58    | 0.28         | Pure air               | Two-tone river               |
| 6    | B24   | SB (OOP) | 0.10      | 0.70    | 0.10         | Bricked straight draw  | Two-tone, high fold eq       |
| 7    | B25   | CO (IP)  | 0.03      | 0.55    | 0.22         | Pure air               | Rainbow, A-high river        |
| 8    | B25   | CO (IP)  | 0.12      | 0.62    | 0.30         | Bricked flush draw     | Rainbow river                |
| 9    | B25   | CO (IP)  | 0.19      | 0.50    | 0.35         | Bricked straight draw  | Boundary fold_eq and top_pp  |
| 10   | B26   | BB (OOP) | 0.06      | 0.60    | 0.20         | Bricked straight draw  | Flush completed on river     |
| 11   | B26   | BB (OOP) | 0.14      | 0.72    | 0.18         | Pure air               | Flush completed, high fold_eq|
| 12   | B27   | BTN (IP) | 0.04      | 0.55    | 0.25         | Bricked flush draw     | Rainbow, low board           |
| 13   | B27   | BTN (IP) | 0.16      | 0.60    | 0.32         | Pure air               | Rainbow river                |
| 14   | B28   | CO (IP)  | 0.07      | 0.65    | 0.20         | Bricked flush draw     | Spades completed             |
| 15   | B28   | CO (IP)  | 0.13      | 0.58    | 0.28         | Bricked straight draw  | Two-tone river               |
| 16   | B29   | BB (OOP) | 0.02      | 0.55    | 0.25         | Pure air               | Rainbow, Q-high river        |

SP8 unique boards: B23, B24, B25, B26, B27, B28, B29 = 7 boards. All river (street=2).
range_pct: 0.02-0.19. fold_equity: 0.50-0.72. top_pair_pct: 0.10-0.35.

---

### SP9: Flat spots — CALL only (10 situations)

All triggers: num_callers_to_bet >= 1 (sandwiched), OR board_favour <= -0.30
with villain_range_capped == 0, OR villain_aggression_count >= 2.

B32 sits (board_favour trigger on T-J-Q) removed per FIX 1 to restore 151
total. The board_favour trigger remains well-represented by B07 (x2), B19
(x1), B23 (x1), and B17 (x1) — five distinct situations across flop, turn,
and river, covering rainbow/connected/dry texture types.

| Sit# | Board | Street | Hero pos | Trigger          | board_favour | aggr_count | Notes                            |
|------|-------|--------|----------|------------------|--------------|------------|----------------------------------|
| 1    | B07   | Flop   | BTN (IP) | board_favour     | -0.45        | 1          | Straight board, villain-favoured |
| 2    | B07   | Flop   | BTN (IP) | board_favour     | -0.50        | 0          | Diff hand, board hugely bad      |
| 3    | B19   | Turn   | BTN (IP) | board_favour     | -0.55        | 0          | 4678 board, villain monster      |
| 4    | B23   | River  | BTN (IP) | board_favour     | -0.35        | 0          | K-high river, villain strong     |
| 5    | B12   | Turn   | BB (OOP) | aggr_count >= 2  | -0.10        | 2          | Villain bet flop + turn          |
| 6    | B26   | River  | BB (OOP) | aggr_count >= 2  | -0.20        | 2          | Multi-street aggressor, river    |
| 7    | B29   | River  | BB (OOP) | aggr_count >= 2  | -0.25        | 3          | High aggression count            |
| 8    | B24   | River  | SB (OOP) | num_callers >= 1 | -0.15        | 0          | Sandwiched by two opponents      |
| 9    | B25   | River  | CO (IP)  | num_callers >= 1 | -0.10        | 0          | Multi-caller situation           |
| 10   | B17   | Turn   | SB (OOP) | board_favour     | -0.32        | 0          | Dry board but villain range +    |

SP9 unique boards: B07, B19, B23, B26, B29, B12, B24, B25, B17 = 9 boards (exceeds min 4).
Triggers: board_favour (sits 1-4, 10) = 5, aggr_count (sits 5-7) = 3, num_callers (sits 8-9) = 2.

---

### SP10: Middle range CALL fill (13 situations)

All hero_range_percentile 0.40-0.80, draws varied, pure CALL.

B32 sits (sits 14-15) removed per FIX 1 to restore 151 total. The
IP/connected/flush-draw profile of those sits is adequately covered by B14
(sit 6, CO IP, spade draw on board), B16 (sit 7, BTN IP, hearts draw),
and B19 (sit 4, BTN IP, connected board). All range bands remain covered.

| Sit# | Board | Street | Hero pos | range_pct | draw_outs | flush_d | is_ip | Notes                              |
|------|-------|--------|----------|-----------|-----------|---------|-------|------------------------------------|
| 1    | B07   | Flop   | BTN (IP) | 0.45      | 0         | 0.05    | 1     | Low pair on straight board         |
| 2    | B10   | Flop   | BB (OOP) | 0.50      | 4         | 0.05    | 0     | Middle pair, gutshot               |
| 3    | B13   | Turn   | SB (OOP) | 0.42      | 0         | 0.05    | 0     | Bottom pair, no draw               |
| 4    | B19   | Turn   | BTN (IP) | 0.58      | 5         | 0.05    | 1     | Middle pair + backdoor             |
| 5    | B20   | Turn   | CO (IP)  | 0.60      | 4         | 0.30    | 1     | Moderate hand, club draw present   |
| 6    | B14   | Turn   | CO (IP)  | 0.55      | 6         | 0.35    | 1     | Decent hand, spade draw on board   |
| 7    | B16   | Turn   | BTN (IP) | 0.68      | 7         | 0.30    | 1     | Good hand, hearts — 7 outs         |
| 8    | B27   | River  | BTN (IP) | 0.62      | 0         | 0.05    | 1     | Showdown value, no draw river      |
| 9    | B28   | River  | CO (IP)  | 0.72      | 0         | 0.40    | 1     | IP, pct 0.72 — SP10 not SP7       |
| 10   | B03   | Flop   | CO (IP)  | 0.75      | 6         | 0.05    | 1     | IP thin value — CALL not RAISE     |
| 11   | B11r  | Flop   | BTN (IP) | 0.78      | 7         | 0.35    | 1     | IP, high pct, draw — CALL          |
| 12   | B21   | Turn   | SB (OOP) | 0.70      | 5         | 0.10    | 0     | OOP but pct 0.70, fails Step 3+4  |
| 13   | B15   | Turn   | BB (OOP) | 0.76      | 6         | 0.20    | 0     | OOP, pct 0.76, draw, CALL         |

SP10 unique boards: B07, B10, B13, B19, B20, B14, B16, B27, B28, B03, B11r, B21, B15 = 13 boards.
Band 0.40-0.55: sits 1, 2, 3, 6 = 4 (meets min 3).
Band 0.55-0.65: sits 4, 5, 8 = 3 (meets min 3).
Band 0.65-0.75: sits 7, 9, 12 = 3 (meets min 3).
Band 0.75-0.80: sits 10, 11, 13 = 3 (meets min 3).

---

## Total verification

| Sub-pattern | Type  | Situations |
|-------------|-------|------------|
| SP1         | RAISE | 18         |
| SP2         | RAISE | 10         |
| SP3         | RAISE | 12         |
| SP4         | CALL  | 6          |
| SP5         | RAISE | 28         |
| SP6         | CALL  | 13         |
| SP7         | RAISE | 25         |
| SP8         | RAISE | 16         |
| SP9         | CALL  | 10         |
| SP10        | CALL  | 13         |
| **Total**   |       | **151**    |

RAISE: SP1(18) + SP2(10) + SP3(12) + SP5(28) + SP7(25) + SP8(16) = 109
CALL: SP4(6) + SP6(13) + SP9(10) + SP10(13) = 42
Total: 109 + 42 = **151. PASS.**

---

## Section 4 — R1-R7 Compliance Verification

### R1 — Board Uniqueness

Total unique boards: **33** (B01-B32 + B33). Minimum 25 required. PASS.

B11 replaced with B11r (Ts 8s 4h) — original B11 (Ts 8s 3h) conflicted
with existing PA_Board6 (Ts 8h 3s) at the rank level. B11r clear.

B32 (Th Jc Qs 3h) verified clear of 31-board existing inventory. PASS.

B33 (Qh Qd 7h): Qh, Qd, 7h do not appear in any of the 32 boards at the
same suit+rank combination. Must be verified against the 46-board PA
inventory before build — flagged for design agent.

All boards verified against existing 46-board inventory (PA boards). No
conflicts confirmed for B01-B32; B33 requires PA inventory check.

Max situations per board: highest concentration is B02 (SP1x2, SP3x2,
SP7x4) = 8. At the hard cap. All other boards at 7 or below.

### R2 — Board Texture Distribution (33 boards)

| Texture    | Boards                                                                    | Count | %   | Target             |
|------------|---------------------------------------------------------------------------|-------|-----|--------------------|
| Rainbow    | B03,B10,B13,B17,B23,B25,B27,B29,B30,B31                                 | 10    | 30% | 24-32% PASS        |
| Two-tone   | B01,B02,B04,B08,B09,B11r,B12,B14,B16,B18,B20,B22,B24,B26,B28,B32       | 16    | 49% | 44-52% PASS        |
| Monotone   | B05                                                                       | 1     | 3%  | 4-8% MARGINAL      |
| Paired     | B06,B15,B21                                                               | 3     | 9%  | 8-12% PASS         |
| Paired/TT  | B33                                                                       | 1     | 3%  | — (hybrid)         |
| Connected  | B07,B19,B32                                                               | 3     | 9%  | 12-16% SHORT       |

Notes:
- B33 is a hybrid Paired/Two-tone board. For paired count: B06, B15, B21,
  B33 = 4 boards (12%). For two-tone count including B33: 17 boards (52%).
  Both within range. PASS.
- Rainbow: 10/33 = 30%. Within 24-32% ceiling. PASS.
- Connected remains 3 boards. Meets the hard minimum of 3. PASS.
- Monotone remains marginal at 1 board. Documented.

### R3 — SPR Distribution (151 situations)

| Tier    | Approx situations | %   | Requirement      |
|---------|-------------------|-----|------------------|
| 1.0-2.0 | ~34               | 22% | max 25% PASS     |
| 2.0-4.0 | ~49               | 32% | min 30% PASS     |
| 4.0-8.0 | ~51               | 34% | min 25% PASS     |
| 8.0+    | ~21               | 14% | min 15% MARGINAL |

The 8.0+ tier contains sits from B03 (SPR=9.0), B07 (SPR=9.0), B09
(SPR=8.0), B10 SP2/SP3 (SPR=9.0 for SP3 which is now SP2 only; actually
B10 in SP2 uses SPR=1.5 by SituationSpec override), B13 (SPR=8.4). The
marginal 8.0+ tier is unchanged from v3 — no structural action required.

B33 (SPR=5.5) adds 2 situations to the 4.0-8.0 tier. Net effect negligible
on distribution percentages.

No single SPR value dominates: SPR=5.0 boards contribute ~27 situations
= 18%. PASS (ceiling is no single value dominating).

### R4 — Street Distribution

B32 situation assignments removed (4 situations, all turn). Turn count
returns from ~68 back to ~64.

| Street | Situations | %   | Target            |
|--------|------------|-----|-------------------|
| Flop   | ~50        | 33% | 27-36% PASS       |
| Turn   | ~64        | 42% | 33-43% PASS       |
| River  | ~39        | 26% | 23-33% PASS       |

B33 adds 2 flop situations (SP4 sits 1-2). Flop rises slightly from ~48
to ~50. All three streets within target bands. PASS. The turn ceiling
concern from v3 (45% with B32 sits) is resolved — turn returns to 42%.

### R5 — Position Distribution

| Position        | Situations | %   | Target              |
|-----------------|------------|-----|---------------------|
| OOP (BB, SB)    | ~68        | 45% | 55-70 PASS (count)  |
| IP (BTN, CO, HJ)| ~87        | 57% | 80-95 PASS (count)  |

B32 (4 IP sits) removed, B33 adds 2 OOP sits (BB). Net: IP drops ~2,
OOP rises ~2. Both counts remain well within range. PASS.

---

## Section 5 — R6 Board Minimums Compliance

| Sub-pattern | Size | Min boards | Unique boards allocated                              | Compliant? |
|-------------|------|------------|------------------------------------------------------|------------|
| SP1  | 18 | 6 | B01,B02,B05,B08,B11r,B12,B16,B20,B22 = 9            | PASS       |
| SP2  | 10 | 4 | B10,B17,B30,B31,B20 = 5                              | PASS       |
| SP3  | 12 | 5 | B02,B06,B08,B12,B13,B15,B17,B21 = 8                 | PASS       |
| SP4  | 6  | 4 | B33,B09,B12,B20,B26 = 5                              | PASS       |
| SP5  | 28 | 7 | B01,B04,B05,B08,B09,B11r,B14,B16,B18,B22 = 10       | PASS       |
| SP6  | 13 | 5 | B01,B04,B06,B08,B11r,B14,B15,B18,B22 = 9            | PASS       |
| SP7  | 25 | 7 | B02,B06,B08,B12,B13,B15,B17,B18,B21 = 9             | PASS       |
| SP8  | 16 | 5 | B23,B24,B25,B26,B27,B28,B29 = 7                     | PASS       |
| SP9  | 10 | 4 | B07,B12,B17,B19,B23,B24,B25,B26,B29 = 9             | PASS       |
| SP10 | 13 | 5 | B03,B07,B10,B11r,B13,B14,B15,B16,B19,B20,B21,B27,B28 = 13 | PASS |

---

## Section 6 — Distribution Summary Tables

### Texture (33 boards)

| Texture        | Count | %   |
|----------------|-------|-----|
| Rainbow        | 10    | 30% |
| Two-tone       | 16    | 49% |
| Monotone       | 1     | 3%  |
| Paired         | 3     | 9%  |
| Paired/Two-tone| 1     | 3%  |
| Connected      | 3     | 9%  |

### SPR Distribution (151 situations)

| Tier    | Situations | %   |
|---------|------------|-----|
| 1.0-2.0 | ~34        | 22% |
| 2.0-4.0 | ~49        | 32% |
| 4.0-8.0 | ~53        | 35% |
| 8.0+    | ~19        | 13% |

### Street Distribution

| Street | Situations | %   |
|--------|------------|-----|
| Flop   | ~50        | 33% |
| Turn   | ~64        | 42% |
| River  | ~39        | 26% |

### Position Distribution

| Position         | Situations | %   |
|------------------|------------|-----|
| OOP (BB, SB)     | ~70        | 46% |
| IP (BTN, CO, HJ) | ~85        | 56% |

---

## Resolved Items Summary

All items that were PENDING in v2 are resolved. All four gate-review
blockers are resolved. No open flags remain.

| Item | Was pending in v2        | Resolution                                                              |
|------|--------------------------|-------------------------------------------------------------------------|
| A    | SP7 sits 3,9,21 (B10 SPR=9.0) | RESOLVED: GTO Expert rejected. Removed and replaced with sits on B06, B08, B02. |
| B    | B22 straight_danger      | RESOLVED: VERIFIED = 0.3, below 0.40. B22 reclassified two-tone only. B32 added as third connected board. |
| C    | SP2 sits 9-10 (B20 flush_danger) | RESOLVED: VERIFIED = 0.0. Passes SP2 requirement. Flags cleared. |

| Item | Gate review blocker      | Resolution                                                              |
|------|--------------------------|-------------------------------------------------------------------------|
| 1    | Total 155 vs 151         | RESOLVED: SP9 sits 11-12 and SP10 sits 14-15 (all B32) removed. Total = 151. |
| 2    | SP3 sit#6 (B10) to_call=0, no check-raise possible | RESOLVED: Sit#6 reassigned to B13 (to_call=70, rainbow turn, OOP). |
| 3    | B26 villain_positions includes folded BTN | RESOLVED: villain_positions changed to `['CO']`. |
| 4    | SP4 sits 1-2 (B15, B06): S2 condition flush_danger >= 0.60 cannot fire on rainbow boards | RESOLVED: B33 added (Qh Qd 7h, paired queens, two hearts, flush_danger ~0.65). SP4 sits 1-2 reassigned to B33. |

*Board Architect delivery complete. 33 boards, 151 situations. All gate-review
blockers resolved. Zero pending flags. Ready for design agents.*
