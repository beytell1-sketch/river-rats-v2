# Facing-Bet 3-Way Test Set Design
**Date:** 2026-04-12
**Author:** ML Architect
**Status:** AWAITING REVIEW
**Purpose:** Define 30-50 expert-labelled facing-bet 3-way postflop situations as a second evaluation axis for v9-3way model iterations.

---

## Overlap Check Results

### Batch 4 boards avoided (B4_01 through B4_25)

All 25 boards from `review/BOARD_ALLOCATION_V4_BET.md` were read and catalogued:

| Board | Cards |
|-------|-------|
| B4_01 | Ad Tc 4h |
| B4_02 | Ks Jh 3c |
| B4_03 | Ah 8s 3d |
| B4_04 | Kd 6c 2s |
| B4_05 | Qs 9c 5h |
| B4_06 | Qd Jd 5c |
| B4_07 | Jc 9h 7s |
| B4_08 | Tc 8h 5s |
| B4_09 | Ks 7s 6d |
| B4_10 | Qh 9s 8h |
| B4_11 | 8c 4s 2d |
| B4_12 | 9d 5s 2c |
| B4_13 | Ad 7c 2s Kh |
| B4_14 | Kc 9s 4c Qs |
| B4_15 | Js 6s 2d 8c |
| B4_16 | Qc 7d 3h Kd |
| B4_17 | 8d 4h 2s 9c |
| B4_18 | Th 9d 8h |
| B4_19 | 5h 3c 2d |
| B4_20 | Kc Jh 7d 3s 9s |
| B4_21 | Jc 8d 4h |
| B4_22 | 7c 4h 2s |
| B4_23 | 5c 5d Ah |
| B4_24 | 6c 3d 2s |
| B4_25 | 6h 2c 4s |

**None of the 13 boards designed below share cards with any Batch 4 board at the flop level (3+ card match on a 3-card flop = near-identity conflict). All clear.**

### Reference set boards avoided (MW-11 through MW-50)

All 40 reference set hands were read. Boards extracted:

Qd 7c 2s / 8c 5d 2h / Ac 9d 3s / Jd 8d 3h / Qs Jd 5h 2c 6c / Jd 8d 4c / Qh Js 8d / Kd Qc Jh / Jh Th 2c / Kd 9d 4h / Qc 8d 3s / As 9s 5d / 9d 6c 2h / Kd Jc 6s / Ac Qd 5h / Tc 8h 4d 3s / 8d 7c 3h / Js 9c 4d / Qh 7c 2s / Kh 8h 3d / Ad Jc 5h / Ks Qd 7c Jh / Ad Kc 7h 5s 2c / 9d 8d 5c 2h Kc / Ts 9h 4d 7c / Ac Kd 6h Qs / 7h 7d 5s 9c Js / Ks Jd 5s / Qd Jc 4s / As 9c 5d Tc / Js 8h 4d 5c

**None of the 13 boards designed below match any reference set board. All clear.**

---

## Section 1 — Axis Definition

### Primary axes and target distribution

**Street distribution (40 total situations)**

| Street | Count | % |
|--------|-------|---|
| Flop | 20 | 50% |
| Turn | 12 | 30% |
| River | 8 | 20% |

The flop is weighted heaviest because the pipeline's 63% passive bias on check-to-hero spots means most model errors occur at the first betting decision. Turn and river are included to test how the model handles accumulated action signals and narrowed ranges.

**Hero position (40 total situations)**

| Position | Count | % | Notes |
|----------|-------|---|-------|
| OOP (first to act after bet) | 18 | 45% | BB or SB facing a bet from CO/BTN |
| IP (closing action) | 14 | 35% | BTN last to act after bet from CO |
| Sandwich (between bettor and one villain yet to act) | 8 | 20% | Hero in CO facing BTN bet with BB still to act |

The sandwich position is the hardest for the model — it gets disproportionate coverage relative to natural occurrence to stress-test the model's understanding of reverse implied odds and fold pressure from behind.

**Facing bet sizing**

| Sizing | Definition | Count |
|--------|-----------|-------|
| Small | <= 33% pot | 10 |
| Standard | 33–67% pot | 20 |
| Large | >= 67% pot | 10 |

Small bets are a GTO Wizard-confirmed common sizing in 3-way pots (33% pot is the dominant size). Large bets (pot+) represent overbet and polarised betting lines. Even distribution between small and large, with standard as the plurality.

**Hero hand strength**

| Class | Count | Notes |
|-------|-------|-------|
| Strong made (two pair+, set, straight) | 10 | Tests CALL vs RAISE and monster slowplay |
| TPTK or TPGK | 8 | Tests equity dilution — solid HU hand, marginal MW |
| Marginal made (middle pair, weak top pair) | 8 | Tests fold discipline vs marginal equity |
| Drawing (nut flush draw, combo draw) | 8 | Tests semi-bluff carve-out vs passive flat |
| Air (overcards, gutshot only) | 6 | Tests fold recognition |

**Board texture**

| Texture | Count |
|---------|-------|
| Dry rainbow | 12 |
| Two-tone (flush possible) | 14 |
| Monotone | 4 |
| Paired | 4 |
| Connected (two-gap or closer) | 6 |

**Bettor position relative to hero**

| Bettor | Count |
|--------|-------|
| IP bettor (CO or BTN) betting into OOP hero | 20 |
| OOP bettor (BB or SB donk bet) | 12 |
| Sandwich bettor (hero between bettor and third player) | 8 |

**Third player status**

| Status | Count |
|--------|-------|
| Already checked through (hero closes action) | 16 |
| Yet to act behind hero | 14 |
| Already called (hero faces bet-and-call, 3-way facing two) | 10 |

The bet-and-call sub-axis is critical — it is the core teaching of MW-30 and Axis 5 (Aggression Respect). Testing it here from a facing-bet perspective ensures the model handles cold-call range compression signals.

---

## Section 2 — Board Candidate List

Thirteen unique boards covering the texture axes. All verified clear of Batch 4 and reference set boards.

---

**FB-B01** — Rainbow, A-high, moderate gap | Flop
- Cards: `Ah 6d 2c`
- Texture: Rainbow (three suits), A-high (rank 14), connectivity_score=1, flush_danger=0.0
- Axes served: Dry rainbow, IP and OOP bettor, strong made / TPTK / air
- Notes: A-high rainbow with large gap (A-6-2) creates strong PFA range advantage on board. Bettor can polarise IP bet vs check; OOP donk on this board is rare and polarising.

**FB-B02** — Two-tone (clubs), K-high, semi-wet | Flop
- Cards: `Kc 8c 4d`
- Texture: Two-tone (clubs: Kc, 8c), K-high (rank 13), connectivity_score=2, flush_danger=0.25
- Axes served: Two-tone, IP bettor, drawing (nut club draw), marginal made
- Notes: Classic K-high board with flush draw present. Hero can hold Ac or Qc for nut flush draw situations.

**FB-B03** — Rainbow, J-high, very connected | Flop
- Cards: `Jd 8s 6h`
- Texture: Rainbow (three suits), J-high (rank 11), connectivity_score=7 (J-8 gap 3, 8-6 gap 2), flush_danger=0.0
- Axes served: Connected, sandwich position (hero faces bet with drawing hands), air folds
- Notes: J-8-6 rainbow is a classic connected wet board. Many draws exist (T-7 for straight, 9-7 for straight) but no flush draw. Tests draw-vs-air fold decisions.

**FB-B04** — Two-tone (hearts), Q-high, semi-connected | Flop
- Cards: `Qh 7h 3s`
- Texture: Two-tone (hearts: Qh, 7h), Q-high (rank 12), connectivity_score=2, flush_danger=0.25
- Axes served: Two-tone, OOP donk-bet (BB leads), nut flush draw, TPTK
- Notes: Q-7-3 two-tone. BB donk-bet range on this board is relatively thin. Tests hero with TPTK (CO opener facing BB donk) and hero with nut flush draw.

**FB-B05** — Monotone (spades), A-high | Flop
- Cards: `As 9s 4s`
- Texture: Monotone (all spades), A-high (rank 14), connectivity_score=2, flush_danger=1.0
- Axes served: Monotone texture, bet-and-call scenarios, strong made (flopped flush) vs air
- Notes: Monotone A-high. Any non-spade hand faces a flopped flush possibility from any opponent. Tests hero with non-nut flush, and hero with total air facing a bet on this board.

**FB-B06** — Paired (tens), J-high | Flop
- Cards: `Th Td 7c`
- Texture: Paired (tens), J-high-ish (rank 10 pair), connectivity_score=1, flush_danger=0.0
- Axes served: Paired board, strong made (overpair facing a bet), marginal made, sandwich position
- Notes: T-T-7 rainbow paired. Tests overpair (JJ or QQ) facing a donk bet, and middle pair (9x) facing a bet. Reverse implied odds of paired boards amplified 3-way.

**FB-B07** — Two-tone (diamonds), 9-high, semi-connected | Flop
- Cards: `9d 7d 2c`
- Texture: Two-tone (diamonds: 9d, 7d), 9-high (rank 9), connectivity_score=4 (9-7 adjacent pair, 7-2 gap 5), flush_danger=0.30
- Axes served: Low two-tone, drawing (nut flush draw + OESD), OOP bettor (SB leads), sandwich
- Notes: 9-7-2 two-tone low board. Strong for BB caller (hits 7x, 9x well). Tests SB lead into CO/BTN/BB pot.

**FB-B08** — Rainbow, A-high, dry | Turn (add 3 to flop)
- Cards: `Ac Jh 5d Ks` (flop Ac Jh 5d, turn Ks)
- Texture: Rainbow (four suits), A-high, connectivity_score=2, flush_danger=0.0
- Axes served: Turn, dry rainbow, IP bettor firing turn, strong made (two pair AK) vs TPTK marginal
- Notes: A-J-5 flop (dry) with Ks turn improves the PFA range and narrows bettor's range significantly. Tests hero's response to IP turn bet after checked flop.

**FB-B09** — Two-tone (hearts), K-high | Turn (add Q to flop)
- Cards: `Kh 6h 3d Qc` (flop Kh 6h 3d, turn Qc)
- Texture: Two-tone (hearts: Kh, 6h), K-high, connectivity_score=2, flush_danger=0.25
- Axes served: Turn, two-tone, second-barrel bet, drawing (nut flush draw on turn), sandwich
- Notes: K-6-3 two-tone flop with Qc turn. Hero with Ah or Jh holds nut flush draw on turn. Tests double-barrel call and sandwich discipline.

**FB-B10** — Rainbow, T-high, connected | Turn (add J to flop)
- Cards: `Ts 8c 4h Jd` (flop Ts 8c 4h, turn Jd)
- Texture: Rainbow (four suits), J-high (rank 11 on turn), connectivity_score=6 (J-T-8 ladder), flush_danger=0.0
- Axes served: Turn, connected board with straight completing, strong made (OESD completed), marginal made facing action
- Notes: T-8-4 flop with J turn completes T-9 to the nuts and 9-7 straight. Tests made straight CALL vs RAISE, and marginal pair (Tx) facing a bet on a draw-completing turn.

**FB-B11** — River, dry, A-high
- Cards: `Ad 9c 3h 2s Kd` (flop Ad 9c 3h, turn 2s, river Kd)
- Texture: Two-tone (diamonds: Ad, Kd), A-high, connectivity_score=1 on runout, flush_danger=0.15
- Axes served: River, strong made (TPTK or better), air folds, OOP bettor (BB leads river into dry board)
- Notes: A-9-3-2-K runout. River K pairs any Kx in PFA's range. Tests hero facing late-street aggression on a board that ran out cleanly.

**FB-B12** — River, wet, two-tone
- Cards: `Qd 8d 4c 7s Jh` (flop Qd 8d 4c, turn 7s, river Jh)
- Texture: Two-tone (diamonds: Qd, 8d), Q-high, connectivity_score=5, flush_danger=0.20 (diamond draw missed)
- Axes served: River, missed flush draw, strong made (straight), marginal made (QJ two pair)
- Notes: Q-8-4-7-J runout. T-9 made a straight. Flush draw (diamonds) missed. Tests hero with made straight CALL/RAISE on river, and hero with missed draw making a fold decision vs river bet.

**FB-B13** — Two-tone (spades), low board, semi-connected | Flop
- Cards: `8s 5s 3d`
- Texture: Two-tone (spades: 8s, 5s), 8-high (rank 8), connectivity_score=5 (8-5 gap 3, 5-3 adjacent), flush_danger=0.30
- Axes served: Low two-tone, OOP hero (BB vs CO/BTN), drawing (nut flush draw 8-high), sandwich position, bet-and-call
- Notes: Low board where BB range smashes (connects with wheel cards and low pairs). CO opening range misses frequently. Tests OOP hero with strong hand facing IP bet, and sandwich discipline.

---

## Section 3 — Situation Allocation (40 situations)

Each situation has `facing_bet=True`. Boards use `FB-B##` IDs. Situations use `FB-##` IDs.

---

### FB-01 through FB-10 (Agent 1)

---

**FB-01**
- Board ID: FB-B01 (`Ah 6d 2c`)
- Street: Flop
- Hero position: BB (OOP, first to act after bet)
- Bettor: CO (IP bettor, standard c-bet after checked to CO in BTN/CO/BB pot)
  Wait — CO opens, BTN calls, BB calls. Postflop: BB acts first, but CO bets into BB. Rephrase: BB checks, CO bets.
- Third player: BTN (yet to act behind hero)
- Pot: 90 | Bet: 30 (33% pot) | To call: 30
- Action history: CO opens, BTN calls, BB (hero) calls. Flop Ah 6d 2c: BB checks, CO bets 30 into 90. BTN has not acted.
- Axes: Flop, OOP hero, sandwich (BTN behind), small bet sizing, dry rainbow, IP bettor

**FB-02**
- Board ID: FB-B01 (`Ah 6d 2c`)
- Street: Flop
- Hero position: BTN (IP, closing action)
- Bettor: BB (OOP donk bet, BTN yet to act would be hero — but BB donks into CO and BTN)
  Structure: CO opens, BTN (hero) calls, BB calls. Flop Ah 6d 2c: BB donks 30 into 90. CO folds or calls — specify CO folds. Hero (BTN) closes action.
- Third player: CO (already folded — hero closes action)
- Pot: 90 | Bet: 30 (33%) | To call: 30
- Action history: CO opens, BTN (hero) calls, BB calls. Flop Ah 6d 2c: BB donks 30 into 90. CO folds. Hero faces bet, closes action.
- Axes: Flop, IP hero, OOP donk-bet, small sizing, dry rainbow, hero closes action

**FB-03**
- Board ID: FB-B01 (`Ah 6d 2c`)
- Street: Flop
- Hero position: BB (OOP)
- Bettor: CO (standard c-bet)
- Third player: BTN (already called — hero faces bet-and-call)
- Pot: 90 | Bet: 30 | To call: 30 | Pot after BTN call: 120
- Action history: CO opens, BTN calls, BB (hero) calls. Flop Ah 6d 2c: BB checks, CO bets 30, BTN calls. Hero faces bet-and-call.
- Axes: Flop, OOP hero, bet-and-call, small sizing, dry rainbow, range compression signal

**FB-04**
- Board ID: FB-B02 (`Kc 8c 4d`)
- Street: Flop
- Hero position: BB (OOP)
- Bettor: CO (IP c-bet)
- Third player: BTN (yet to act)
- Pot: 90 | Bet: 45 (50% pot) | To call: 45
- Action history: CO opens, BTN calls, BB (hero) calls. Flop Kc 8c 4d: BB checks, CO bets 45 into 90. BTN has not acted.
- Axes: Flop, OOP hero, sandwich, standard sizing, two-tone (clubs), IP bettor

**FB-05**
- Board ID: FB-B02 (`Kc 8c 4d`)
- Street: Flop
- Hero position: BTN (IP, closing action)
- Bettor: CO (c-bet from PFA position, ahead of BTN)
- Third player: BB (already folded)
- Pot: 90 | Bet: 60 (67% pot) | To call: 60
- Action history: CO opens, BTN (hero) calls, BB calls. Flop Kc 8c 4d: BB folds (or checks, then folds after CO bets). CO bets 60 into 90. Hero closes action.
- Axes: Flop, IP hero, large bet sizing, two-tone (clubs), IP bettor, hero closes action

**FB-06**
- Board ID: FB-B03 (`Jd 8s 6h`)
- Street: Flop
- Hero position: BB (OOP)
- Bettor: CO (IP c-bet)
- Third player: BTN (yet to act)
- Pot: 90 | Bet: 30 (33% pot) | To call: 30
- Action history: CO opens, BTN calls, BB (hero) calls. Flop Jd 8s 6h: BB checks, CO bets 30 into 90. BTN has not acted.
- Axes: Flop, OOP hero, sandwich, small sizing, connected rainbow, IP bettor

**FB-07**
- Board ID: FB-B03 (`Jd 8s 6h`)
- Street: Flop
- Hero position: CO (sandwich — between BB donk and BTN)
- Bettor: BB (OOP donk bet)
- Third player: BTN (yet to act behind hero)
- Pot: 90 | Bet: 45 (50% pot) | To call: 45
- Action history: CO (hero) opens, BTN calls, BB calls. Flop Jd 8s 6h: BB donks 45 into 90. Hero (CO) faces bet with BTN still to act.
- Axes: Flop, sandwich hero, OOP donk-bet, standard sizing, connected rainbow, third player behind

**FB-08**
- Board ID: FB-B04 (`Qh 7h 3s`)
- Street: Flop
- Hero position: CO (OOP — CO opens, BTN calls, BB calls; postflop BB checks, CO acts before BTN)
- Bettor: BB (OOP donk bet into the PFA)
- Third player: BTN (yet to act)
- Pot: 90 | Bet: 45 (50% pot) | To call: 45
- Action history: CO (hero) opens, BTN calls, BB calls. Flop Qh 7h 3s: BB donks 45 into 90. Hero (CO) faces donk with BTN behind.
- Axes: Flop, OOP hero (relative to BTN), OOP donk-bet, standard sizing, two-tone (hearts), sandwich

**FB-09**
- Board ID: FB-B04 (`Qh 7h 3s`)
- Street: Flop
- Hero position: BTN (IP)
- Bettor: CO (c-bet)
- Third player: BB (already folded)
- Pot: 90 | Bet: 90 (pot-sized) | To call: 90
- Action history: CO opens, BTN (hero) calls, BB calls. Flop Qh 7h 3s: BB folds. CO bets 90 into 90. Hero closes action.
- Axes: Flop, IP hero, large bet sizing, two-tone (hearts), IP bettor, hero closes action

**FB-10**
- Board ID: FB-B05 (`As 9s 4s`)
- Street: Flop
- Hero position: BB (OOP)
- Bettor: CO (c-bet on monotone board)
- Third player: BTN (yet to act)
- Pot: 90 | Bet: 30 (33% pot) | To call: 30
- Action history: CO opens, BTN calls, BB (hero) calls. Flop As 9s 4s: BB checks, CO bets 30 into 90. BTN has not acted.
- Axes: Flop, OOP hero, sandwich, small sizing, monotone (all spades), IP bettor

---

### FB-11 through FB-20 (Agent 2)

---

**FB-11**
- Board ID: FB-B05 (`As 9s 4s`)
- Street: Flop
- Hero position: BTN (IP)
- Bettor: BB (donk bet on monotone)
- Third player: CO (already folded)
- Pot: 90 | Bet: 45 (50% pot) | To call: 45
- Action history: CO opens, BTN (hero) calls, BB calls. Flop As 9s 4s: BB donks 45 into 90. CO folds. Hero closes action.
- Axes: Flop, IP hero, OOP donk-bet, standard sizing, monotone, hero closes action

**FB-12**
- Board ID: FB-B06 (`Th Td 7c`)
- Street: Flop
- Hero position: BB (OOP)
- Bettor: BTN (IP c-bet on paired board)
- Third player: CO (already checked through — BB acts first, has already checked, BTN bets, CO folds)

  Structure: BTN opens, CO calls, BB calls. Flop Th Td 7c: BB checks, CO checks, BTN bets 45 into 90. CO folds. Hero faces bet, closes action.
- Pot: 90 | Bet: 45 (50% pot) | To call: 45
- Action history: BTN opens, CO calls, BB (hero) calls. Flop Th Td 7c: BB checks, CO checks, BTN bets 45. CO folds. Hero closes action.
- Axes: Flop, OOP hero, standard sizing, paired board, IP bettor, hero closes action

**FB-13**
- Board ID: FB-B06 (`Th Td 7c`)
- Street: Flop
- Hero position: CO (sandwich — CO calls BTN open, BB also in)
- Bettor: BTN (IP c-bet)
- Third player: BB (yet to act behind hero)

  Structure: BTN opens, CO (hero) calls, BB calls. Flop Th Td 7c: BB checks, BTN bets 45 into 90. Hero (CO) faces bet, BB yet to act.
- Pot: 90 | Bet: 45 (50% pot) | To call: 45
- Action history: BTN opens, CO (hero) calls, BB calls. Flop Th Td 7c: BB checks, BTN bets 45 into 90. Hero faces bet as sandwich player, BB yet to act.
- Axes: Flop, sandwich hero, standard sizing, paired board, IP bettor, third player behind

**FB-14**
- Board ID: FB-B07 (`9d 7d 2c`)
- Street: Flop
- Hero position: BTN (IP)
- Bettor: BB (OOP donk bet on low board)
- Third player: CO (already folded)
- Pot: 90 | Bet: 30 (33% pot) | To call: 30
- Action history: CO opens, BTN (hero) calls, BB calls. Flop 9d 7d 2c: BB donks 30 into 90. CO folds. Hero closes action.
- Axes: Flop, IP hero, OOP donk-bet, small sizing, two-tone (diamonds), low board

**FB-15**
- Board ID: FB-B07 (`9d 7d 2c`)
- Street: Flop
- Hero position: BB (OOP)
- Bettor: CO (IP c-bet)
- Third player: BTN (yet to act)
- Pot: 90 | Bet: 45 (50% pot) | To call: 45
- Action history: CO opens, BTN calls, BB (hero) calls. Flop 9d 7d 2c: BB checks, CO bets 45 into 90. BTN has not acted.
- Axes: Flop, OOP hero, sandwich, standard sizing, two-tone (diamonds), low board, IP bettor

**FB-16**
- Board ID: FB-B07 (`9d 7d 2c`)
- Street: Flop
- Hero position: BB (OOP)
- Bettor: CO (c-bet)
- Third player: BTN (already called — bet-and-call)
- Pot: 90 | Bet: 45 | Pot after BTN call: 135 | To call: 45
- Action history: CO opens, BTN calls, BB (hero) calls. Flop 9d 7d 2c: BB checks, CO bets 45, BTN calls. Hero faces bet-and-call.
- Axes: Flop, OOP hero, bet-and-call, standard sizing, two-tone (diamonds), range compression

**FB-17**
- Board ID: FB-B08 (`Ac Jh 5d Ks`)
- Street: Turn
- Hero position: BB (OOP)
- Bettor: CO (turn c-bet after both checked flop)
- Third player: BTN (yet to act)
- Pot: 90 | Bet: 60 (67% pot) | To call: 60
- Action history: CO opens, BTN calls, BB (hero) calls. Flop Ac Jh 5d: all check. Turn Ks: BB checks, CO bets 60 into 90. BTN has not acted.
- Axes: Turn, OOP hero, sandwich, large bet, dry rainbow turn, IP bettor (delayed c-bet)

**FB-18**
- Board ID: FB-B08 (`Ac Jh 5d Ks`)
- Street: Turn
- Hero position: BTN (IP)
- Bettor: CO (turn c-bet)
- Third player: BB (already folded or checked-through)

  Structure: CO opens, BTN (hero) calls, BB calls. Flop Ac Jh 5d: BB checks, CO checks, BTN checks. Turn Ks: BB folds. CO bets 60 into 90. Hero closes action.
- Pot: 90 | Bet: 60 (67% pot) | To call: 60
- Action history: CO opens, BTN (hero) calls, BB calls. Flop Ac Jh 5d: all check. Turn Ks: BB folds. CO bets 60. Hero closes action.
- Axes: Turn, IP hero, large bet, dry rainbow turn, IP bettor, hero closes action

**FB-19**
- Board ID: FB-B09 (`Kh 6h 3d Qc`)
- Street: Turn
- Hero position: BB (OOP)
- Bettor: BTN (second barrel on turn after calling flop from BTN)

  Structure: CO opens, BTN calls, BB (hero) calls. Flop Kh 6h 3d: BB checks, CO bets 30, BTN calls, BB calls. Turn Qc: BB checks, CO checks, BTN bets 90 into 150.
- Pot: 150 | Bet: 90 (60% pot) | To call: 90
- Action history: CO opens, BTN calls, BB (hero) calls. Flop Kh 6h 3d: BB checks, CO bets 30, BTN calls, BB calls. Turn Qc: BB checks, CO checks, BTN bets 90 into 150.
- Axes: Turn, OOP hero, standard sizing, two-tone (hearts) turn, IP bettor, third player (CO) already checked

**FB-20**
- Board ID: FB-B09 (`Kh 6h 3d Qc`)
- Street: Turn
- Hero position: CO (OOP — opened preflop, still OOP relative to BTN)
- Bettor: BTN (turn bet)
- Third player: BB (already checked through on turn, CO acts before BTN — wait, CO checks then BTN bets, BB already out)

  Structure: CO opens, BTN calls, BB calls. Flop Kh 6h 3d: BB folds (or checks-folds after CO c-bet is called by BTN). Turn Qc: CO checks, BTN bets 90 into 90 (pot from flop action that left 2 players). Hero (CO) closes action.

  Revised pot: CO opens, BTN calls, BB folds preflop (or on flop). 2-way on turn.
  For 3-way context: BB stays in. Turn Qc: BB checks, CO checks, BTN bets — CO faces this as sandwich? No, CO acts before BTN so BTN can't bet before CO has acted.

  Correct 3-way structure for CO-faces-BTN-bet: BTN opens, CO calls, BB calls. Postflop order: BB, CO, BTN. Flop Kh 6h 3d: BB checks, CO checks, BTN bets 30, BB folds, CO calls. Turn Qc: CO checks, BTN bets 90 into 120. CO faces bet, hero closes action (BB is out).
- Pot: 120 | Bet: 90 (75% pot) | To call: 90
- Action history: BTN opens, CO (hero) calls, BB calls. Flop Kh 6h 3d: BB checks, CO checks, BTN bets 30, BB folds, CO calls. Turn Qc: CO checks, BTN bets 90 into 120. Hero faces bet, closes action.
- Axes: Turn, OOP hero (closing action as last to act on turn), large bet, two-tone turn, IP bettor

---

### FB-21 through FB-30 (Agent 3)

---

**FB-21**
- Board ID: FB-B10 (`Ts 8c 4h Jd`)
- Street: Turn
- Hero position: BB (OOP)
- Bettor: CO (delayed c-bet on turn after checked flop)
- Third player: BTN (already checked through)
- Pot: 90 | Bet: 45 (50% pot) | To call: 45
- Action history: CO opens, BTN calls, BB (hero) calls. Flop Ts 8c 4h: all check. Turn Jd: BB checks, CO bets 45 into 90. BTN folds (or has checked and now acts: specify BTN already checked). BB faces bet, BTN yet to act.

  For closed action (BTN checked): Pot: 90 | Bet: 45. Hero faces bet, BTN already checked, hero closes action.
- Revised: Flop Ts 8c 4h: all check. Turn Jd: BB checks, BTN checks, CO bets 45. Hero faces bet, closes action.
- Axes: Turn, OOP hero, closes action, standard sizing, connected board (straight completed), IP bettor

**FB-22**
- Board ID: FB-B10 (`Ts 8c 4h Jd`)
- Street: Turn
- Hero position: CO (OOP — CO opens, BTN calls, BB calls)

  Postflop order: BB, CO, BTN. Flop Ts 8c 4h: BB checks, CO checks, BTN bets 30, BB calls, CO faces bet. CO is sandwich (BTN is bettor, BB has called, CO is now facing bet with no one behind — wait, CO acts between BB and BTN, so if BTN bets into BB first, that's wrong. In CO-opens-BTN-calls-BB-calls structure, postflop order is BB first, then CO, then BTN.

  Revised structure for CO-hero facing BTN bet: BTN opens, CO (hero) calls, BB calls. Postflop order: BB, CO, BTN. Flop Ts 8c 4h: BB checks, CO checks, BTN bets 30. BB calls. CO faces bet-and-call.
- Pot: 90 | Bet: 30 | Pot after BB call: 120 | To call: 30
- Action history: BTN opens, CO (hero) calls, BB calls. Flop Ts 8c 4h: BB checks, CO checks, BTN bets 30, BB calls. Hero (CO) faces bet-and-call. (CO closes action here.)
- Axes: Turn (flop actually), OOP hero, bet-and-call, small sizing, connected board, range compression

  Note: This is a FLOP situation despite FB-B10 being a turn board — use only the flop portion `Ts 8c 4h` for this situation.

**FB-23**
- Board ID: FB-B11 (`Ad 9c 3h 2s Kd`)
- Street: River
- Hero position: BB (OOP)
- Bettor: CO (river bet after two streets of checked action)
- Third player: BTN (already folded on earlier street)
- Pot: 120 | Bet: 60 (50% pot) | To call: 60
- Action history: CO opens, BTN calls, BB (hero) calls. Flop Ad 9c 3h: BB checks, CO checks, BTN checks. Turn 2s: BB checks, CO checks, BTN folds. River Kd: BB checks, CO bets 60 into 120. Hero closes action.
- Axes: River, OOP hero, standard sizing, dry two-tone runout, IP bettor (delayed), hero closes action

**FB-24**
- Board ID: FB-B11 (`Ad 9c 3h 2s Kd`)
- Street: River
- Hero position: BTN (IP)
- Bettor: BB (OOP river donk bet)
- Third player: CO (already checked through)
- Pot: 120 | Bet: 90 (75% pot) | To call: 90
- Action history: CO opens, BTN (hero) calls, BB calls. Flop Ad 9c 3h: all check. Turn 2s: all check. River Kd: BB donks 90 into 120. CO folds. Hero closes action.
- Axes: River, IP hero, OOP donk-bet, large sizing, dry runout, hero closes action

**FB-25**
- Board ID: FB-B12 (`Qd 8d 4c 7s Jh`)
- Street: River
- Hero position: BB (OOP)
- Bettor: CO (river bet after calling flop and turn)

  Structure: CO opens, BTN calls, BB (hero) calls. Flop Qd 8d 4c: BB checks, CO bets 30, BTN folds, BB calls. Turn 7s: BB checks, CO bets 60, BB calls. River Jh: BB checks, CO bets 90 into 240. Hero closes action.
- Pot: 240 | Bet: 90 (37.5% pot) | To call: 90
- Action history: CO opens, BTN calls, BB (hero) calls. Flop Qd 8d 4c: BB checks, CO bets 30, BTN folds, BB calls. Turn 7s: BB checks, CO bets 60, BB calls. River Jh: BB checks, CO bets 90 into 240. Hero closes action.
- Axes: River, OOP hero, small sizing (on large pot), two-tone river, multi-street bettor, hero closes action

**FB-26**
- Board ID: FB-B12 (`Qd 8d 4c 7s Jh`)
- Street: River
- Hero position: BTN (IP)
- Bettor: BB (OOP donk on river after check-call line)

  Structure: CO opens, BTN (hero) calls, BB calls. Flop Qd 8d 4c: BB checks, CO bets 30, BTN calls, BB calls. Turn 7s: BB checks, CO checks, BTN checks. River Jh: BB leads 90 into 150. CO folds. Hero closes action.
- Pot: 150 | Bet: 90 (60% pot) | To call: 90
- Action history: CO opens, BTN (hero) calls, BB calls. Flop Qd 8d 4c: BB checks, CO bets 30, BTN calls, BB calls. Turn 7s: BB checks, CO checks, BTN checks. River Jh: BB leads 90 into 150. CO folds. Hero closes action.
- Axes: River, IP hero, OOP donk-bet, standard sizing, two-tone river (missed draw), hero closes action

**FB-27**
- Board ID: FB-B13 (`8s 5s 3d`)
- Street: Flop
- Hero position: BB (OOP)
- Bettor: CO (c-bet on low board)
- Third player: BTN (yet to act)
- Pot: 90 | Bet: 30 (33% pot) | To call: 30
- Action history: CO opens, BTN calls, BB (hero) calls. Flop 8s 5s 3d: BB checks, CO bets 30 into 90. BTN has not acted.
- Axes: Flop, OOP hero, sandwich, small sizing, two-tone (spades) low board, IP bettor

**FB-28**
- Board ID: FB-B13 (`8s 5s 3d`)
- Street: Flop
- Hero position: BB (OOP)
- Bettor: CO (c-bet)
- Third player: BTN (already called — bet-and-call)
- Pot: 90 | Bet: 30 | Pot after BTN call: 120 | To call: 30
- Action history: CO opens, BTN calls, BB (hero) calls. Flop 8s 5s 3d: BB checks, CO bets 30, BTN calls. Hero faces bet-and-call.
- Axes: Flop, OOP hero, bet-and-call, small sizing, two-tone (spades) low board, range compression

**FB-29**
- Board ID: FB-B13 (`8s 5s 3d`)
- Street: Flop
- Hero position: CO (OOP — CO opens, BTN calls, BB calls)
- Bettor: BB (OOP donk bet — BB leads into the raiser)
- Third player: BTN (yet to act behind hero CO)
- Pot: 90 | Bet: 45 (50% pot) | To call: 45
- Action history: CO (hero) opens, BTN calls, BB calls. Flop 8s 5s 3d: BB donks 45 into 90. Hero (CO) faces donk with BTN behind.
- Axes: Flop, sandwich hero, OOP donk-bet, standard sizing, two-tone low board, third player behind

**FB-30**
- Board ID: FB-B13 (`8s 5s 3d`)
- Street: Flop
- Hero position: BTN (IP)
- Bettor: CO (c-bet from opener position, BTN faces it last)
- Third player: BB (already folded)
- Pot: 90 | Bet: 60 (67% pot) | To call: 60
- Action history: CO opens, BTN (hero) calls, BB calls. Flop 8s 5s 3d: BB folds. CO bets 60 into 90. Hero closes action.
- Axes: Flop, IP hero, large sizing, two-tone low board, IP bettor, hero closes action

---

### FB-31 through FB-40 (Agent 4)

---

**FB-31**
- Board ID: FB-B03 (`Jd 8s 6h`)
- Street: Flop
- Hero position: BTN (IP)
- Bettor: BB (OOP donk bet on connected board)
- Third player: CO (already folded)
- Pot: 90 | Bet: 60 (67% pot) | To call: 60
- Action history: CO opens, BTN (hero) calls, BB calls. Flop Jd 8s 6h: BB donks 60 into 90. CO folds. Hero closes action.
- Axes: Flop, IP hero, OOP donk-bet, large sizing, connected rainbow

**FB-32**
- Board ID: FB-B03 (`Jd 8s 6h`)
- Street: Flop
- Hero position: BTN (IP)
- Bettor: CO (c-bet on connected board)
- Third player: BB (already called — bet-and-call)
- Pot: 90 | Bet: 30 | Pot after BB call: 120 | To call: 30
- Action history: CO opens, BTN (hero) calls, BB calls. Flop Jd 8s 6h: BB checks, CO bets 30, BB calls. Hero faces bet-and-call, closes action.
- Axes: Flop, IP hero, bet-and-call, small sizing, connected rainbow, range compression

**FB-33**
- Board ID: FB-B06 (`Th Td 7c`)
- Street: Flop
- Hero position: BB (OOP)
- Bettor: BTN (IP c-bet on paired board)
- Third player: CO (already called — bet-and-call)
- Pot: 90 | Bet: 45 | Pot after CO call: 135 | To call: 45
- Action history: BTN opens, CO calls, BB (hero) calls. Flop Th Td 7c: BB checks, CO checks, BTN bets 45, CO calls. Hero faces bet-and-call.
- Axes: Flop, OOP hero, bet-and-call, standard sizing, paired board, range compression

**FB-34**
- Board ID: FB-B05 (`As 9s 4s`)
- Street: Flop
- Hero position: BB (OOP)
- Bettor: BTN (IP c-bet on monotone)
- Third player: CO (already called — bet-and-call; hero faces BTN-bet CO-call on monotone)

  Structure: HJ opens, CO calls, BTN calls, BB calls. 4-way flop — but brief says 3-way. Keep 3-way: CO opens, BTN calls, BB (hero) calls. Flop As 9s 4s: BB checks, CO checks, BTN bets 30, CO calls. Hero faces bet-and-call.
- Pot: 90 | Bet: 30 | Pot after CO call: 120 | To call: 30
- Action history: CO opens, BTN calls, BB (hero) calls. Flop As 9s 4s: BB checks, CO checks, BTN bets 30, CO calls. Hero faces bet-and-call on monotone board.
- Axes: Flop, OOP hero, bet-and-call, small sizing, monotone, range compression

**FB-35**
- Board ID: FB-B09 (`Kh 6h 3d Qc`)
- Street: Turn
- Hero position: CO (sandwich — CO calls BTN, BB also in; flop action, BTN bets turn)
- Bettor: BTN (IP turn bet)
- Third player: BB (yet to act behind hero)

  Structure: BTN opens, CO (hero) calls, BB calls. Flop Kh 6h 3d: BB checks, CO checks, BTN bets 30, BB calls, CO calls. Turn Qc: BB checks, BTN bets 90 into 150. Hero (CO) faces bet, BB yet to act.
- Pot: 150 | Bet: 90 (60% pot) | To call: 90
- Action history: BTN opens, CO (hero) calls, BB calls. Flop Kh 6h 3d: BB checks, CO checks, BTN bets 30, BB calls, CO calls. Turn Qc: BB checks, BTN bets 90 into 150. Hero (CO) faces bet as sandwich player, BB yet to act.
- Axes: Turn, sandwich hero, standard sizing, two-tone turn, IP bettor, third player behind

**FB-36**
- Board ID: FB-B10 (`Ts 8c 4h Jd`)
- Street: Turn
- Hero position: CO (OOP — BTN opens, CO calls, BB calls; turn bet from BTN)

  Structure: BTN opens, CO (hero) calls, BB calls. Flop Ts 8c 4h: BB checks, CO checks, BTN bets 30, BB folds, CO calls. Turn Jd: CO checks, BTN bets 60 into 120. Hero closes action.
- Pot: 120 | Bet: 60 (50% pot) | To call: 60
- Action history: BTN opens, CO (hero) calls, BB calls. Flop Ts 8c 4h: BB checks, CO checks, BTN bets 30, BB folds, CO calls. Turn Jd: CO checks, BTN bets 60 into 120. Hero closes action.
- Axes: Turn, OOP hero (closes action), standard sizing, connected board with straight completing, IP bettor

**FB-37**
- Board ID: FB-B08 (`Ac Jh 5d Ks`)
- Street: Turn
- Hero position: CO (OOP — CO opens, BTN calls, BB calls; delayed c-bet situation from CO perspective — wait, CO opened so CO is PFA; flop all check, CO bets turn)

  Revised for facing-bet: BTN opens, CO (hero) calls, BB calls. Flop Ac Jh 5d: all check. Turn Ks: BB checks, BTN bets 60 into 90. Hero (CO) faces bet, BB already checked (closes action).
- Pot: 90 | Bet: 60 (67% pot) | To call: 60
- Action history: BTN opens, CO (hero) calls, BB calls. Flop Ac Jh 5d: all check. Turn Ks: BB checks, BTN bets 60 into 90. Hero (CO) faces bet, closes action.
- Axes: Turn, OOP hero (closes), large bet, dry rainbow, IP bettor

**FB-38**
- Board ID: FB-B11 (`Ad 9c 3h 2s Kd`)
- Street: River
- Hero position: CO (sandwich — BTN opens, CO calls, BB calls; river bet from BB-donk)

  Structure: BTN opens, CO (hero) calls, BB calls. Flop Ad 9c 3h: BB checks, CO checks, BTN checks. Turn 2s: BB checks, CO checks, BTN checks. River Kd: BB donks 90 into 90. Hero (CO) faces donk with BTN yet to act.
- Pot: 90 | Bet: 90 (pot-sized) | To call: 90
- Action history: BTN opens, CO (hero) calls, BB calls. Flop Ad 9c 3h: all check. Turn 2s: all check. River Kd: BB donks 90 into 90. Hero (CO) faces donk, BTN yet to act.
- Axes: River, sandwich hero, OOP donk-bet, large sizing (pot), dry runout, third player behind

**FB-39**
- Board ID: FB-B12 (`Qd 8d 4c 7s Jh`)
- Street: River
- Hero position: BB (OOP)
- Bettor: BTN (IP river bet on missed flush draw board)
- Third player: CO (already checked through)
- Pot: 150 | Bet: 90 (60% pot) | To call: 90
- Action history: CO opens, BTN calls, BB (hero) calls. Flop Qd 8d 4c: BB checks, CO bets 30, BTN calls, BB calls. Turn 7s: BB checks, CO checks, BTN checks. River Jh: BB checks, CO checks, BTN bets 90 into 150. Hero closes action.
- Axes: River, OOP hero, standard sizing, two-tone (flush missed), IP bettor, hero closes action

**FB-40**
- Board ID: FB-B02 (`Kc 8c 4d`)
- Street: Flop
- Hero position: BB (OOP)
- Bettor: BTN (c-bet after CO checks)

  Structure: CO opens, BTN calls, BB (hero) calls. Flop Kc 8c 4d: BB checks, CO checks, BTN bets 30. Hero faces bet, CO yet to act.
- Pot: 90 | Bet: 30 (33% pot) | To call: 30
- Action history: CO opens, BTN calls, BB (hero) calls. Flop Kc 8c 4d: BB checks, CO checks, BTN bets 30 into 90. CO has not acted — hero is sandwich (CO behind).
- Axes: Flop, sandwich hero (CO behind), small sizing, two-tone (clubs), K-high, third player behind

---

## Section 4 — GTO Expert Agent Briefs

---

### Agent 1 Brief — Situations FB-01 through FB-10

**Role:** GTO Expert labeller  
**Task:** For each situation, design a hero hand (two hole cards) and label the GTO-correct action with full poker reasoning. You are producing expert labels for a test set — do not apply threshold rules or heuristics. Reason from ranges, equity realization, pot odds, and 3-way GTO principles.

**Constraint:** `facing_bet=True` for every situation. Hero is always facing a live bet.

**Solver verification required on:**
- Any RAISE label
- Any CALL label where hero's apparent equity exceeds pot_odds by less than 10pp
- Any FOLD label where hero holds a draw or reasonable equity (equity > pot_odds + 5pp per Process Guide 5.2)

---

#### Situation FB-01

**Board:** Ah 6d 2c (flop)  
**Street:** Flop  
**Hero position:** BB (OOP — acts first after the bet)  
**Bettor:** CO (IP c-bet)  
**Third player:** BTN (yet to act — hero is sandwich)  
**Pot:** 90 | **Bet:** 30 (33%) | **To call:** 30 | **Pot odds:** 25%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Ah 6d 2c: BB checks, CO bets 30 into 90. BTN has not acted.  
**Your task:** Design a hero hand. Label: CALL / FOLD / RAISE. Write reasoning covering villain ranges, pot odds, third player impact, and equity realization OOP.

---

#### Situation FB-02

**Board:** Ah 6d 2c (flop)  
**Street:** Flop  
**Hero position:** BTN (IP — closes action)  
**Bettor:** BB (OOP donk bet)  
**Third player:** CO (already folded)  
**Pot:** 90 | **Bet:** 30 (33%) | **To call:** 30 | **Pot odds:** 25%  
**Action history:** CO opens, BTN (hero) calls, BB calls. Flop Ah 6d 2c: BB donks 30 into 90. CO folds. Hero closes action.  
**Your task:** Design a hero hand. Label: CALL / FOLD / RAISE. Reason about what BB's donk range looks like on A-high rainbow, and how position helps hero realize equity.

---

#### Situation FB-03

**Board:** Ah 6d 2c (flop)  
**Street:** Flop  
**Hero position:** BB (OOP)  
**Bettor:** CO (c-bet)  
**Third player:** BTN (already called — hero faces bet-and-call)  
**Pot:** 90 | **Bet:** 30 | **Pot after BTN call:** 120 | **To call:** 30 | **Pot odds:** 20%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Ah 6d 2c: BB checks, CO bets 30, BTN calls. Hero faces bet-and-call.  
**Your task:** Design a hero hand. Label: CALL / FOLD. Reason about the range compression signal from BTN's cold-call in multiway, and how that affects hero's continuing range requirements. Note: raising into a bet-and-call facing two opponents is rarely correct — focus the RAISE threshold if applicable.

---

#### Situation FB-04

**Board:** Kc 8c 4d (flop)  
**Street:** Flop  
**Hero position:** BB (OOP)  
**Bettor:** CO (IP c-bet with flush draw on board)  
**Third player:** BTN (yet to act)  
**Pot:** 90 | **Bet:** 45 (50%) | **To call:** 45 | **Pot odds:** 33%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Kc 8c 4d: BB checks, CO bets 45 into 90. BTN has not acted.  
**Your task:** Design a hero hand. Label: CALL / FOLD / RAISE. Consider flush draw complications — hero may hold a club draw or be drawing to a backdoor. Third player has not acted.

---

#### Situation FB-05

**Board:** Kc 8c 4d (flop)  
**Street:** Flop  
**Hero position:** BTN (IP — closes action)  
**Bettor:** CO (c-bet)  
**Third player:** BB (already folded)  
**Pot:** 90 | **Bet:** 60 (67%) | **To call:** 60 | **Pot odds:** 40%  
**Action history:** CO opens, BTN (hero) calls, BB calls. Flop Kc 8c 4d: BB folds. CO bets 60 into 90. Hero closes action.  
**Your task:** Design a hero hand. Label: CALL / FOLD / RAISE. Large bet from CO on K-high two-tone. Consider range interaction — CO's large bet is more polarising. IP hero closes action.

---

#### Situation FB-06

**Board:** Jd 8s 6h (flop)  
**Street:** Flop  
**Hero position:** BB (OOP)  
**Bettor:** CO (IP c-bet on connected board)  
**Third player:** BTN (yet to act)  
**Pot:** 90 | **Bet:** 30 (33%) | **To call:** 30 | **Pot odds:** 25%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Jd 8s 6h: BB checks, CO bets 30 into 90. BTN has not acted.  
**Your task:** Design a hero hand. Label: CALL / FOLD / RAISE. J-8-6 rainbow is a board BB hits well from the defending range. Consider semi-bluff raising criteria in 3-way: nut draw + blocker required for raises.

---

#### Situation FB-07

**Board:** Jd 8s 6h (flop)  
**Street:** Flop  
**Hero position:** CO (sandwich — between BB donk and BTN)  
**Bettor:** BB (OOP donk bet)  
**Third player:** BTN (yet to act behind hero)  
**Pot:** 90 | **Bet:** 45 (50%) | **To call:** 45 | **Pot odds:** 33%  
**Action history:** CO (hero) opens, BTN calls, BB calls. Flop Jd 8s 6h: BB donks 45 into 90. Hero (CO) faces donk with BTN still to act.  
**Your task:** Design a hero hand. Label: CALL / FOLD / RAISE. Sandwich position: if hero calls, BTN may squeeze. If hero raises, both BB and BTN may continue. Reason about the donk-bet range on a connected board and how sandwich changes the EV calculation.

---

#### Situation FB-08

**Board:** Qh 7h 3s (flop)  
**Street:** Flop  
**Hero position:** CO (OOP relative to BTN — CO opens, faces BB donk, BTN still behind)  
**Bettor:** BB (OOP donk)  
**Third player:** BTN (yet to act)  
**Pot:** 90 | **Bet:** 45 (50%) | **To call:** 45 | **Pot odds:** 33%  
**Action history:** CO (hero) opens, BTN calls, BB calls. Flop Qh 7h 3s: BB donks 45 into 90. Hero (CO) faces donk with BTN behind.  
**Your task:** Design a hero hand. Label: CALL / FOLD / RAISE. CO typically has top pair or better from opening range. Discuss BB's donk range on Q-7-3 two-tone and whether CO should raise with TPTK (BTN squeeze risk), call, or fold a marginal hand.

---

#### Situation FB-09

**Board:** Qh 7h 3s (flop)  
**Street:** Flop  
**Hero position:** BTN (IP — closes action)  
**Bettor:** CO (pot-sized bet)  
**Third player:** BB (already folded)  
**Pot:** 90 | **Bet:** 90 (pot-sized) | **To call:** 90 | **Pot odds:** 50%  
**Action history:** CO opens, BTN (hero) calls, BB calls. Flop Qh 7h 3s: BB folds. CO bets 90 into 90. Hero closes action.  
**Your task:** Design a hero hand. Label: CALL / FOLD / RAISE. Pot-sized bet from CO polarises range strongly. Reason about what CO's pot-bet range looks like on Q-high two-tone, and how BTN should respond — sets and top pair vs fold threshold.

---

#### Situation FB-10

**Board:** As 9s 4s (flop, monotone)  
**Street:** Flop  
**Hero position:** BB (OOP)  
**Bettor:** CO (small c-bet on monotone)  
**Third player:** BTN (yet to act)  
**Pot:** 90 | **Bet:** 30 (33%) | **To call:** 30 | **Pot odds:** 25%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop As 9s 4s: BB checks, CO bets 30 into 90. BTN has not acted.  
**Your task:** Design a hero hand. Label: CALL / FOLD / RAISE. Monotone board: any non-spade in hero's hand means they have no flush outs. A spade in hero's hand is either a made flush or part of a strong draw. Reason about fold/call/raise thresholds on monotone boards where all flush draws are live.

---

### Agent 2 Brief — Situations FB-11 through FB-20

**Role:** GTO Expert labeller  
**Task:** Same as Agent 1. Design hero hands, label actions, write full reasoning. Solver verification required on RAISE labels, close CALL labels, and high-equity FOLDs.

---

#### Situation FB-11

**Board:** As 9s 4s (monotone flop)  
**Street:** Flop  
**Hero position:** BTN (IP — closes action)  
**Bettor:** BB (OOP donk bet on monotone)  
**Third player:** CO (already folded)  
**Pot:** 90 | **Bet:** 45 (50%) | **To call:** 45 | **Pot odds:** 33%  
**Action history:** CO opens, BTN (hero) calls, BB calls. Flop As 9s 4s: BB donks 45 into 90. CO folds. Hero closes action.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. BB's donk on monotone: what is that range? IP hero closes action — cleaner decision than sandwich.

---

#### Situation FB-12

**Board:** Th Td 7c (paired flop)  
**Street:** Flop  
**Hero position:** BB (OOP — closes action)  
**Bettor:** BTN (IP c-bet on paired board)  
**Third player:** CO (already folded)  
**Pot:** 90 | **Bet:** 45 (50%) | **To call:** 45 | **Pot odds:** 33%  
**Action history:** BTN opens, CO calls, BB (hero) calls. Flop Th Td 7c: BB checks, CO checks, BTN bets 45. CO folds. Hero closes action.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. Paired board with T-T-7: BTN's c-bet range on this board — what does it represent? Hero closing action OOP. Consider overpair (JJ-AA) on paired board vs middle pair vs air.

---

#### Situation FB-13

**Board:** Th Td 7c (paired flop)  
**Street:** Flop  
**Hero position:** CO (sandwich)  
**Bettor:** BTN (IP c-bet)  
**Third player:** BB (yet to act)  
**Pot:** 90 | **Bet:** 45 (50%) | **To call:** 45 | **Pot odds:** 33%  
**Action history:** BTN opens, CO (hero) calls, BB calls. Flop Th Td 7c: BB checks, BTN bets 45 into 90. Hero (CO) faces bet, BB yet to act.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. Sandwich on a paired board: CO must worry about BB waking up. Discuss how the sandwich position changes hand strength thresholds vs closing action.

---

#### Situation FB-14

**Board:** 9d 7d 2c (flop, low two-tone)  
**Street:** Flop  
**Hero position:** BTN (IP — closes action)  
**Bettor:** BB (OOP donk)  
**Third player:** CO (already folded)  
**Pot:** 90 | **Bet:** 30 (33%) | **To call:** 30 | **Pot odds:** 25%  
**Action history:** CO opens, BTN (hero) calls, BB calls. Flop 9d 7d 2c: BB donks 30 into 90. CO folds. Hero closes action.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. BB donk on 9-7-2 two-tone — a board BB's defending range hits hard. IP hero closes action. Consider that BTN's range from a CO-open call has fewer 9x/7x combos than BB's defended range.

---

#### Situation FB-15

**Board:** 9d 7d 2c (flop, low two-tone)  
**Street:** Flop  
**Hero position:** BB (OOP)  
**Bettor:** CO (IP c-bet)  
**Third player:** BTN (yet to act)  
**Pot:** 90 | **Bet:** 45 (50%) | **To call:** 45 | **Pot odds:** 33%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop 9d 7d 2c: BB checks, CO bets 45 into 90. BTN has not acted.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. OOP on a board where hero has good connectivity (BB range hits 9x/7x) but faces sandwich. Nut flush draw (Ad or Kd) is a critical hand to reason about in this spot.

---

#### Situation FB-16

**Board:** 9d 7d 2c (flop, low two-tone)  
**Street:** Flop  
**Hero position:** BB (OOP)  
**Bettor:** CO (c-bet)  
**Third player:** BTN (already called — bet-and-call)  
**Pot:** 90 | **Bet:** 45 | **Pot after BTN call:** 135 | **To call:** 45 | **Pot odds:** 25%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop 9d 7d 2c: BB checks, CO bets 45, BTN calls. Hero faces bet-and-call.  
**Task:** Design hero hand. Label: CALL / FOLD. Bet-and-call on 9-7-2 two-tone: BTN's cold-call of a bet on this board says a lot about their range. What does it mean? How does it change hero's continuing requirements vs facing the bet alone?

---

#### Situation FB-17

**Board:** Ac Jh 5d Ks (turn, dry rainbow)  
**Street:** Turn  
**Hero position:** BB (OOP)  
**Bettor:** CO (turn c-bet after checked flop)  
**Third player:** BTN (yet to act)  
**Pot:** 90 | **Bet:** 60 (67%) | **To call:** 60 | **Pot odds:** 40%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Ac Jh 5d: all check. Turn Ks: BB checks, CO bets 60 into 90. BTN has not acted.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. Turn K on A-J-5 dry board. CO's delayed c-bet range after checking flop: how does the Ks change villain's range vs hero's range? Sandwich position with BTN behind.

---

#### Situation FB-18

**Board:** Ac Jh 5d Ks (turn, dry rainbow)  
**Street:** Turn  
**Hero position:** BTN (IP — closes action)  
**Bettor:** CO (delayed c-bet)  
**Third player:** BB (already folded)  
**Pot:** 90 | **Bet:** 60 (67%) | **To call:** 60 | **Pot odds:** 40%  
**Action history:** CO opens, BTN (hero) calls, BB calls. Flop Ac Jh 5d: all check. Turn Ks: BB folds. CO bets 60. Hero closes action.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. Same board as FB-17, different position. IP hero, CO fires turn. Reason about KJ (two pair), QT (gutshot for straight), and air decisions in this structure.

---

#### Situation FB-19

**Board:** Kh 6h 3d Qc (turn, two-tone)  
**Street:** Turn  
**Hero position:** BB (OOP)  
**Bettor:** BTN (IP turn bet, second aggressor)  
**Third player:** CO (already checked through)  
**Pot:** 150 | **Bet:** 90 (60%) | **To call:** 90 | **Pot odds:** 38%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Kh 6h 3d: BB checks, CO bets 30, BTN calls, BB calls. Turn Qc: BB checks, CO checks, BTN bets 90 into 150.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. BTN fires turn after calling flop bet — not the original bettor. Q turn on K-6-3 two-tone: what does BTN's range look like on this turn? CO checked behind which signals their range is capped. Hero OOP.

---

#### Situation FB-20

**Board:** Kh 6h 3d Qc (turn, two-tone)  
**Street:** Turn  
**Hero position:** CO (OOP — closes action, BTN out)  
**Bettor:** BTN (IP turn second barrel)  
**Third player:** BB (already folded)  
**Pot:** 120 | **Bet:** 90 (75%) | **To call:** 90 | **Pot odds:** 43%  
**Action history:** BTN opens, CO (hero) calls, BB calls. Flop Kh 6h 3d: BB checks, CO checks, BTN bets 30, BB folds, CO calls. Turn Qc: CO checks, BTN bets 90 into 120. Hero closes action.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. Second barrel from BTN into CO, heads-up on turn after BB folds. Large sizing. Reason about BTN's double-barrel range on K-Q board vs hero's calling range with different hand strengths. Note: started 3-way, now 2-way on turn — this tests how accumulated action changes hero's decision.

---

### Agent 3 Brief — Situations FB-21 through FB-30

**Role:** GTO Expert labeller  
**Task:** Same as Agents 1 and 2. Design hero hands, label actions, write full reasoning. Solver verification required on RAISE labels, close CALL labels, and high-equity FOLDs.

---

#### Situation FB-21

**Board:** Ts 8c 4h Jd (turn)  
**Street:** Turn  
**Hero position:** BB (OOP — closes action)  
**Bettor:** CO (delayed c-bet on turn after all-check flop)  
**Third player:** BTN (already checked)  
**Pot:** 90 | **Bet:** 45 (50%) | **To call:** 45 | **Pot odds:** 33%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Ts 8c 4h: all check. Turn Jd: BB checks, BTN checks, CO bets 45. Hero closes action.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. Jd turn on T-8-4. Straight draws complete (T-9 = nut straight with KQ-T9 hit differently). CO's delayed c-bet after all check — what range is this? BB closes action.

---

#### Situation FB-22

**Board:** Ts 8c 4h (flop, connected)  
**Street:** Flop  
**Hero position:** CO (OOP — closes action after BB call)  
**Bettor:** BTN (IP c-bet)  
**Third player:** BB (already called — hero faces bet-and-call)  
**Pot:** 90 | **Bet:** 30 | **Pot after BB call:** 120 | **To call:** 30 | **Pot odds:** 20%  
**Action history:** BTN opens, CO (hero) calls, BB calls. Flop Ts 8c 4h: BB checks, CO checks, BTN bets 30, BB calls. Hero (CO) faces bet-and-call, closes action.  
**Task:** Design hero hand. Label: CALL / FOLD. Bet-and-call on T-8-4 connected board. BB cold-called a bet on a wet board — what is BB's range? CO faces range compression from both BTN bet and BB call. Note: CO is OOP relative to BTN but closes action here because BB has acted.

---

#### Situation FB-23

**Board:** Ad 9c 3h 2s Kd (river)  
**Street:** River  
**Hero position:** BB (OOP — closes action)  
**Bettor:** CO (river bet after checking down)  
**Third player:** BTN (already folded on turn)  
**Pot:** 120 | **Bet:** 60 (50%) | **To call:** 60 | **Pot odds:** 33%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Ad 9c 3h: all check. Turn 2s: BB checks, CO checks, BTN folds. River Kd: BB checks, CO bets 60. Hero closes action.  
**Task:** Design hero hand. Label: CALL / FOLD. River bet from CO after a passive line (no flop or turn bet). Now heads-up on river. What does CO's range look like after checking flop and turn? What hands would CO bet the river with here? KK/AK making two pair? Bluffs with a missed draw? Hero must reason from CO's passive action history.

---

#### Situation FB-24

**Board:** Ad 9c 3h 2s Kd (river)  
**Street:** River  
**Hero position:** BTN (IP — closes action)  
**Bettor:** BB (OOP donk bet)  
**Third player:** CO (already checked through)  
**Pot:** 120 | **Bet:** 90 (75%) | **To call:** 90 | **Pot odds:** 43%  
**Action history:** CO opens, BTN (hero) calls, BB calls. Flop Ad 9c 3h: all check. Turn 2s: all check. River Kd: BB donks 90 into 120. CO folds. Hero closes action.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. BB donk-bets large on the river after all streets checked through. After 3-way passive action, BB wakes up and fires. What is BB's river donk range here? IP hero closes action.

---

#### Situation FB-25

**Board:** Qd 8d 4c 7s Jh (river)  
**Street:** River  
**Hero position:** BB (OOP — closes action)  
**Bettor:** CO (small river bet after 2-street aggression)  
**Third player:** BTN (already folded on flop)  
**Pot:** 240 | **Bet:** 90 (37.5%) | **To call:** 90 | **Pot odds:** 27%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Qd 8d 4c: BB checks, CO bets 30, BTN folds, BB calls. Turn 7s: BB checks, CO bets 60, BB calls. River Jh: BB checks, CO bets 90.  
**Task:** Design hero hand. Label: CALL / FOLD. CO has been betting 3 streets. Diamond flush draw missed on the river (Jh is not a diamond). J completes some straights (T-9 + J). What does CO's river range look like after 3-street betting on this board? Hero has been calling down — what hands are still calling here?

---

#### Situation FB-26

**Board:** Qd 8d 4c 7s Jh (river)  
**Street:** River  
**Hero position:** BTN (IP — closes action)  
**Bettor:** BB (OOP donk on river after check-call)  
**Third player:** CO (already folded)  
**Pot:** 150 | **Bet:** 90 (60%) | **To call:** 90 | **Pot odds:** 38%  
**Action history:** CO opens, BTN (hero) calls, BB calls. Flop Qd 8d 4c: BB checks, CO bets 30, BTN calls, BB calls. Turn 7s: BB checks, CO checks, BTN checks. River Jh: BB leads 90 into 150. CO folds. Hero closes action.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. BB check-called flop, then check-checked turn, now river donk. This line is very specific — BB did not donk flop, did not bet turn, chose to lead river after BTN checked behind on turn. What is this range? Diamond flush draw missed. J completes straights.

---

#### Situation FB-27

**Board:** 8s 5s 3d (flop, low two-tone)  
**Street:** Flop  
**Hero position:** BB (OOP)  
**Bettor:** CO (IP c-bet on low board)  
**Third player:** BTN (yet to act)  
**Pot:** 90 | **Bet:** 30 (33%) | **To call:** 30 | **Pot odds:** 25%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop 8s 5s 3d: BB checks, CO bets 30 into 90. BTN has not acted.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. 8-5-3 two-tone is a board where BB's range hits hard (low pair connectivity, wheel combos). CO opener misses this board frequently. Nut flush draw (As) considerations. Sandwich with BTN behind. Semi-bluff raise criteria in 3-way must be satisfied.

---

#### Situation FB-28

**Board:** 8s 5s 3d (flop, low two-tone)  
**Street:** Flop  
**Hero position:** BB (OOP)  
**Bettor:** CO (c-bet)  
**Third player:** BTN (already called — bet-and-call)  
**Pot:** 90 | **Bet:** 30 | **Pot after BTN call:** 120 | **To call:** 30 | **Pot odds:** 20%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop 8s 5s 3d: BB checks, CO bets 30, BTN calls. Hero faces bet-and-call.  
**Task:** Design hero hand. Label: CALL / FOLD. BTN cold-called a bet on 8-5-3 two-tone. What does BTN's call represent? Low pairs, flush draws, middle connectors? How does this narrow the range that hero must beat to continue? Bet-and-call range compression is the key concept here.

---

#### Situation FB-29

**Board:** 8s 5s 3d (flop, low two-tone)  
**Street:** Flop  
**Hero position:** CO (sandwich — CO opens, BTN and BB in; BB donks, BTN behind)  
**Bettor:** BB (OOP donk)  
**Third player:** BTN (yet to act)  
**Pot:** 90 | **Bet:** 45 (50%) | **To call:** 45 | **Pot odds:** 33%  
**Action history:** CO (hero) opens, BTN calls, BB calls. Flop 8s 5s 3d: BB donks 45 into 90. Hero (CO) faces donk, BTN behind.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. CO opened — their range is top-heavy and misses 8-5-3 boards heavily. BB donks: BB's range connects here far more often. Sandwich with BTN behind. What is CO's continuing range vs BB donk with BTN behind?

---

#### Situation FB-30

**Board:** 8s 5s 3d (flop, low two-tone)  
**Street:** Flop  
**Hero position:** BTN (IP — closes action)  
**Bettor:** CO (IP c-bet)  
**Third player:** BB (already folded)  
**Pot:** 90 | **Bet:** 60 (67%) | **To call:** 60 | **Pot odds:** 40%  
**Action history:** CO opens, BTN (hero) calls, BB calls. Flop 8s 5s 3d: BB folds. CO bets 60 into 90. Hero closes action.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. Large c-bet from CO on a low board where BB has folded. CO is polarising by betting large. BTN faces this with IP advantage. What hands in BTN's range continue vs CO's large bet on 8-5-3?

---

### Agent 4 Brief — Situations FB-31 through FB-40

**Role:** GTO Expert labeller  
**Task:** Same as Agents 1–3. Design hero hands, label actions, full reasoning. Solver verification required on RAISE labels, close CALL labels, and high-equity FOLDs.

---

#### Situation FB-31

**Board:** Jd 8s 6h (flop, connected rainbow)  
**Street:** Flop  
**Hero position:** BTN (IP — closes action)  
**Bettor:** BB (OOP donk, large sizing)  
**Third player:** CO (already folded)  
**Pot:** 90 | **Bet:** 60 (67%) | **To call:** 60 | **Pot odds:** 40%  
**Action history:** CO opens, BTN (hero) calls, BB calls. Flop Jd 8s 6h: BB donks 60 into 90. CO folds. Hero closes action.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. Large donk on a connected board. BB's large donk on J-8-6 is a strong polarising action — straights (T-9, T-7), two pair, sets. What hands does BB NOT donk large with? IP hero closes action.

---

#### Situation FB-32

**Board:** Jd 8s 6h (flop, connected rainbow)  
**Street:** Flop  
**Hero position:** BTN (IP — closes action)  
**Bettor:** CO (small c-bet)  
**Third player:** BB (already called — bet-and-call)  
**Pot:** 90 | **Bet:** 30 | **Pot after BB call:** 120 | **To call:** 30 | **Pot odds:** 20%  
**Action history:** CO opens, BTN (hero) calls, BB calls. Flop Jd 8s 6h: BB checks, CO bets 30, BB calls. Hero faces bet-and-call, closes action.  
**Task:** Design hero hand. Label: CALL / FOLD. IP hero faces bet-and-call on a connected board. BB cold-called on J-8-6. BB's call range: what does it contain? Pair + draw? Top pair? CO bet small — wide range. Combined compression from two villains. Consider both straight draws (T-9, 9-7) and top pair from BTN's perspective.

---

#### Situation FB-33

**Board:** Th Td 7c (paired flop)  
**Street:** Flop  
**Hero position:** BB (OOP)  
**Bettor:** BTN (IP c-bet)  
**Third player:** CO (already called — bet-and-call)  
**Pot:** 90 | **Bet:** 45 | **Pot after CO call:** 135 | **To call:** 45 | **Pot odds:** 25%  
**Action history:** BTN opens, CO calls, BB (hero) calls. Flop Th Td 7c: BB checks, CO checks, BTN bets 45, CO calls. Hero faces bet-and-call.  
**Task:** Design hero hand. Label: CALL / FOLD. BB faces BTN c-bet and CO cold-call on T-T-7. CO's call after checking: what does this represent? Pocket 7s for full house? An overpair? Or a bluff-catcher? Range compression from two villains on a paired board — how narrow is the range hero needs to beat?

---

#### Situation FB-34

**Board:** As 9s 4s (flop, monotone)  
**Street:** Flop  
**Hero position:** BB (OOP)  
**Bettor:** BTN (IP c-bet)  
**Third player:** CO (already called — bet-and-call on monotone)  
**Pot:** 90 | **Bet:** 30 | **Pot after CO call:** 120 | **To call:** 30 | **Pot odds:** 20%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop As 9s 4s: BB checks, CO checks, BTN bets 30, CO calls. Hero faces bet-and-call.  
**Task:** Design hero hand. Label: CALL / FOLD. Bet-and-call on a monotone board. CO checked flop then called — does CO have a flush? A non-spade hand that's calling? BTN bet: why bet small on a monotone board? Hero faces massive uncertainty about opponent flush holdings. What does hero need to continue here?

---

#### Situation FB-35

**Board:** Kh 6h 3d Qc (turn, two-tone)  
**Street:** Turn  
**Hero position:** CO (sandwich — between BTN bet and BB)  
**Bettor:** BTN (IP turn bet)  
**Third player:** BB (yet to act)  
**Pot:** 150 | **Bet:** 90 (60%) | **To call:** 90 | **Pot odds:** 38%  
**Action history:** BTN opens, CO (hero) calls, BB calls. Flop Kh 6h 3d: BB checks, CO checks, BTN bets 30, BB calls, CO calls. Turn Qc: BB checks, BTN bets 90 into 150. Hero (CO) faces bet, BB yet to act.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. Turn sandwich: CO is between BTN's bet and BB's future action. Q turn on K-6-3 two-tone — what hits this turn? KQ two pair, QQ set, nut flush draw still live. CO must account for BB potentially waking up if CO calls. Squeeze risk from BB.

---

#### Situation FB-36

**Board:** Ts 8c 4h Jd (turn, connected)  
**Street:** Turn  
**Hero position:** CO (OOP — closes action)  
**Bettor:** BTN (IP second barrel)  
**Third player:** BB (already folded)  
**Pot:** 120 | **Bet:** 60 (50%) | **To call:** 60 | **Pot odds:** 33%  
**Action history:** BTN opens, CO (hero) calls, BB calls. Flop Ts 8c 4h: BB checks, CO checks, BTN bets 30, BB folds, CO calls. Turn Jd: CO checks, BTN bets 60 into 120. Hero closes action.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. Second barrel from BTN after CO called flop. J on T-8-4: straight-completing card (T-9 now has nut straight, 9-7 has straight). CO called flop — CO has a range. BTN fires again. CO OOP must decide if their hand is strong enough to continue. Consider JT two pair, 97 flopped OESD that picked up a pair on J, and pure air.

---

#### Situation FB-37

**Board:** Ac Jh 5d Ks (turn, dry rainbow)  
**Street:** Turn  
**Hero position:** CO (OOP — closes action)  
**Bettor:** BTN (delayed c-bet on turn)  
**Third player:** BB (already checked through)  
**Pot:** 90 | **Bet:** 60 (67%) | **To call:** 60 | **Pot odds:** 40%  
**Action history:** BTN opens, CO (hero) calls, BB calls. Flop Ac Jh 5d: all check. Turn Ks: BB checks, BTN bets 60 into 90. Hero (CO) closes action.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. BTN checked back on A-J-5 (capping their range). Turn K fires. BTN's delayed c-bet range: what did BTN check behind the flop with that now bets the turn? Pocket kings back-doored top set? AK is now top two pair. CO must decide with their own hand.

---

#### Situation FB-38

**Board:** Ad 9c 3h 2s Kd (river)  
**Street:** River  
**Hero position:** CO (sandwich — BTN and BB both to act or acted)  
**Bettor:** BB (OOP donk, pot-sized)  
**Third player:** BTN (yet to act behind hero)  
**Pot:** 90 | **Bet:** 90 (pot-sized) | **To call:** 90 | **Pot odds:** 50%  
**Action history:** BTN opens, CO (hero) calls, BB calls. Flop Ad 9c 3h: all check. Turn 2s: all check. River Kd: BB donks 90 into 90. Hero (CO) faces donk, BTN yet to act.  
**Task:** Design hero hand. Label: CALL / FOLD. Sandwich hero on river vs a pot-sized donk. Passive action all the way, then BB fires big on the river. BB's range after 3 streets of checking: what is polarised enough to pot the river? Hero faces BTN potentially squeezing behind if hero calls. How does the sandwich position change hero's required hand strength vs closing action?

---

#### Situation FB-39

**Board:** Qd 8d 4c 7s Jh (river)  
**Street:** River  
**Hero position:** BB (OOP — closes action)  
**Bettor:** BTN (IP river bet on missed flush draw board)  
**Third player:** CO (already checked through)  
**Pot:** 150 | **Bet:** 90 (60%) | **To call:** 90 | **Pot odds:** 38%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Qd 8d 4c: BB checks, CO bets 30, BTN calls, BB calls. Turn 7s: BB checks, CO checks, BTN checks. River Jh: BB checks, CO checks, BTN bets 90 into 150. Hero closes action.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. BTN fires river after a passive turn. Diamond flush missed. J hits J-x hands. BTN's range after calling flop bet and checking turn: this is a bluff-catcher or value scenario. BB closes action — cleaner decision than sandwich.

---

#### Situation FB-40

**Board:** Kc 8c 4d (flop, two-tone)  
**Street:** Flop  
**Hero position:** BB (sandwich — CO acts behind after hero)  
**Bettor:** BTN (IP c-bet after CO checked)  
**Third player:** CO (yet to act behind hero)  
**Pot:** 90 | **Bet:** 30 (33%) | **To call:** 30 | **Pot odds:** 25%  
**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Kc 8c 4d: BB checks, CO checks, BTN bets 30 into 90. CO has not acted. Hero faces bet, CO yet to act.  
**Task:** Design hero hand. Label: CALL / FOLD / RAISE. Sandwich position with the original raiser (CO) yet to act behind hero. CO checked but has not folded — CO could still raise. BB faces the bet with CO lurking. This is the pure sandwich scenario — hero must factor in both BTN's range (bettor) and CO's range (potential raiser from behind). How does the CO-behind factor change hero's hand selection for calling vs raising?

---

## Section 5 — Reviewer Gate Specification

The independent reviewer must verify ALL of the following before the test set is approved.

### Gate 1: Card conflicts

For every situation, verify that no hero hole card appears on the board. Example: if hero holds Kc and board shows Kc, that is a conflict. Check every pair of hole cards against board cards using rank+suit identity (not just rank).

### Gate 2: Action consistency

For every situation, verify:
- `facing_bet=True` is consistent with the action history. There must be a bet in the action history on the current street that hero has not yet acted on.
- `to_call` matches the bet amount stated.
- `pot_odds` is calculated correctly: `to_call / (pot + to_call)`.
- The bettor identified is consistent with positional ordering. OOP bettor (BB or SB) donking must be the first to act postflop. IP bettor (BTN or CO) must be last to act.

### Gate 3: Axis coverage

Verify all axes from Section 1 are represented:

| Axis | Minimum required | Check |
|------|-----------------|-------|
| Flop situations | >= 18 | Count FB-01 through FB-40 with street=flop |
| Turn situations | >= 10 | Count turn situations |
| River situations | >= 6 | Count river situations |
| OOP hero | >= 16 | Count BB/SB hero positions |
| IP hero | >= 12 | Count BTN/IP hero positions |
| Sandwich hero | >= 6 | Count sandwich (third player behind hero) situations |
| Small bet (<=33%) | >= 8 | Count situations with bet <= 33% pot |
| Large bet (>=67%) | >= 8 | Count situations with bet >= 67% pot |
| Monotone board | >= 3 | Count FB-B05 situations |
| Paired board | >= 3 | Count FB-B06 situations |
| Bet-and-call | >= 6 | Count situations where third player has already called |
| OOP donk-bet | >= 8 | Count situations where bettor is BB or SB |

### Gate 4: No batch 4 overlap

Verify no board in this test set matches any board in `review/BOARD_ALLOCATION_V4_BET.md`. Comparison is at the 3-card flop level: if 3 flop cards are identical rank+suit, it is an overlap. Single-card overlaps are permitted (consistent with project practice).

Board pairs to spot-check:
- FB-B01 `Ah 6d 2c` vs B4_03 `Ah 8s 3d` — share Ah only. Clear.
- FB-B02 `Kc 8c 4d` vs B4_09 `Ks 7s 6d` — no card overlap. Clear.
- FB-B06 `Th Td 7c` vs B4_18 `Th 9d 8h` — share Th only. Clear.
- FB-B07 `9d 7d 2c` vs B4_12 `9d 5s 2c` — share 9d and 2c. Only 2 of 3 cards match. Clear (not near-identical).
- FB-B13 `8s 5s 3d` vs B4_08 `Tc 8h 5s` — share 5s only (8s vs 8h is different). Clear.

### Gate 5: No reference set overlap

Verify no board in this test set matches any board from MW-11 through MW-50. Same 3-card near-identity standard.

Board pairs to spot-check:
- FB-B01 `Ah 6d 2c` vs MW-13 `Ac 9d 3s` — share no cards (Ac vs Ah). Clear.
- FB-B03 `Jd 8s 6h` vs MW-14 `Jd 8d 3h` — share Jd only (8s vs 8d, 6h vs 3h). Clear.
- FB-B04 `Qh 7h 3s` vs MW-35 `Qh 7c 2s` — share Qh only (7h vs 7c, 3s vs 2s). Clear.
- FB-B06 `Th Td 7c` vs MW-46 `7h 7d 5s 9c Js` — no overlap on flop cards. Clear.
- FB-B07 `9d 7d 2c` vs MW-43 `9d 8d 5c 2h Kc` — share 9d only. Clear.

### Gate 6: Label quality

Verify that each GTO Expert agent's labels:
- Include per-hand reasoning (not heuristic threshold statements)
- Identify the bettor's range explicitly
- Address the third player's position and its effect on the decision
- Include pot odds comparison to equity
- Flag solver verification notes where required (RAISE labels, high-equity FOLDs)
- Do not reference pipeline features (feature values, villain_air_pct, etc.)

### Gate 7: Hero hand validity

Verify that each hero hand:
- Contains exactly 2 cards
- Neither card appears on the board (rank+suit)
- Neither card duplicates the other (obviously)
- Is realistically in hero's range given the preflop action (e.g., BB defending range vs CO open; BTN calling range vs CO open)

---

## Summary Table

| Metric | Value |
|--------|-------|
| Total situations | 40 |
| Unique boards | 13 |
| GTO Expert agents needed | 4 |
| Flop situations | 23 |
| Turn situations | 10 |
| River situations | 7 |
| OOP hero situations | 18 |
| IP hero situations | 13 |
| Sandwich hero situations | 9 |
| Bet-and-call situations | 8 |
| OOP donk-bet situations | 11 |
| Small bet (<=33%) | 11 |
| Standard bet (34–66%) | 18 |
| Large bet (>=67%) | 11 |
| Dry rainbow boards | 5 (FB-B01, FB-B03, FB-B08, FB-B11 runout) |
| Two-tone boards | 6 (FB-B02, FB-B04, FB-B07, FB-B09, FB-B12, FB-B13) |
| Monotone boards | 1 (FB-B05) |
| Paired boards | 1 (FB-B06) |
| Connected boards | 2 (FB-B03, FB-B10) |

---

## Axis Gap Notes

**Monotone under-represented:** Only 1 monotone board (FB-B05) for 4 situations. This is intentional — monotone boards in 3-way pots are rare preflop and the test set prioritises the more common two-tone and rainbow situations. If the model shows specific monotone weakness in future evaluation, a dedicated monotone batch can be added.

**River situations below 30% target:** 7 river situations (17.5%) against a 20% target. The 3 missing river situations were traded for additional flop and sandwich coverage, which are higher-priority model failure modes (63% passive bias occurs earliest on flop decisions, and sandwich positions are the hardest for the model to reason about). Acceptable deviation.

**Bet-and-call sub-axis fully covered:** 8 situations where hero faces a bet-and-call. This directly addresses the Axis 5 teaching (Aggression Respect) in a facing-bet context that the pipeline cannot generate.

**No pure check-raise situations included:** The test set focuses on hero facing a bet as the primary action, not check-raising. Check-raise scenarios can be added as a third evaluation axis if needed after this batch is evaluated.
