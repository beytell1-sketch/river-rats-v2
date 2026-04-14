---
date: 2026-04-14
from: Builder
to: Owner
re: Solver verification — top 10 most uncertain hands
---

# Solver Verification — Top 10 Most Uncertain Hands

These are the 10 hands where Pass 2 review most significantly departed from Pass 1 consensus (9 label flips) plus the only CHECK→BET over-aggression flagged by the Tier 5 challenger. Verify each in GTO Wizard at the flop/turn/river node described.

## Overview

| # | ID | Street | Hero pos | Hero cards | Board | Pot | Bet | SPR | Pass 1 actions | Pass 2 label |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `BP5_01` | flop | BB | 4♥2♦ | 8♠ 4♦ 2♥ | 90 | — | 1.11 | BET/BET/BET/CHECK | **BET** |
| 2 | `BP4_21` | flop | BTN | K♦Q♥ | J♥ 9♣ 6♦ | 90 | — | 1.11 | BET/CHECK/CHECK/BET | **CHECK** |
| 3 | `BP7_01` | turn | BTN | A♠J♠ | 9♠ 7♣ 4♠ K♦ | 180 | 59 | 0.56 | RAISE/CALL/CALL/RAISE | **CALL** |
| 4 | `d5222_BTN_flop` | flop | BTN | 7♦7♣ | 9♥ 5♥ 3♦ | 133 | 53 | 0.75 | CALL/CALL/FOLD/FOLD | **FOLD** |
| 5 | `d5620_CO_turn` | turn | CO | Q♦6♦ | J♠ K♠ K♦ Q♥ | 133 | 53 | 0.75 | CALL/FOLD/CALL/FOLD | **FOLD** |
| 6 | `d5749_HJ_turn` | turn | HJ | 9♦9♣ | J♣ 3♥ 5♣ 2♥ | 133 | 53 | 0.75 | CALL/FOLD/FOLD/CALL | **FOLD** |
| 7 | `d8002_BTN_flop` | flop | BTN | 7♠7♦ | 5♠ 3♣ T♥ | 133 | 53 | 0.75 | FOLD/CALL/CALL/FOLD | **CALL** |
| 8 | `d8886_BTN_flop` | flop | BTN | 9♣9♦ | 2♠ 5♦ J♦ | 80 | — | 1.25 | BET/CHECK/CHECK/BET | **CHECK** |
| 9 | `d8963_HJ_turn` | turn | HJ | J♥J♣ | K♠ 4♥ 9♣ 3♥ | 80 | — | 1.25 | BET/CHECK/BET/CHECK | **CHECK** |
| 10 | `d1983_BTN_turn` | turn | BTN | A♦4♦ | J♦ 7♦ K♥ 2♣ | 80 | — | 1.25 | BET/BET/BET/BET | **CHECK** |

---

# Per-hand details (players → preflop → flop → turn → river)

## 1. `BP5_01` — Tier 1 CONFIDENT_SPLIT

**Proposed (Pass 2) label: `BET`**

> D1-majority but action-split. Pass 2 2/3 panel: BET. T4 mis-classified bottom-2-pair as bottom set; actual is strong_made. Validate BB donk vs check-to-PFA on dry rainbow at SPR 1.11.

### Players
- **Hero**: BB — 4♥2♦
- **Villains**: CO (2 opponents remaining)

### Preflop
- 3-way single-raised pot; hero is BB, villains CO
- PFR is one of the villains (see action history for confirmation)

### Flop — 8♠ 4♦ 2♥
- Action to hero after checks (per: `BB check, BB ???`)
- **Decision (hero = BB): BET or CHECK**

### Key metrics
- **Pot**: 90 | **To call**: 0 | **SPR**: 1.11
- **Equity vs range**: 72.0% | **Equity margin over pot odds**: +72.0%
- **Villain range**: TP+ 20% / med 17% / draw 2% / air 61%
- **Hero range percentile**: 93.4% | **Fold-equity estimate**: 63%

### What to verify
- Pass 1 votes: **BET/BET/BET/CHECK**
- Pass 2 consensus: **BET**
- Key question: does GTO Wizard confirm `BET` as primary (or at least mixed), or should Pass 1 stand?

---

## 2. `BP4_21` — Tier 2 Pass 1 → Pass 2 flip

**Proposed (Pass 2) label: `CHECK`**

> Pass 1 BET (T1/T4), Pass 2 panel 3/3 CHECK. KQ overcards + gutshot on J9 6 rainbow at SPR 1.11 IP after BB/SB both check. Does KB 1.7 non-nut semi-bluff apply?

### Players
- **Hero**: BTN — K♦Q♥
- **Villains**: SB (2 opponents remaining)

### Preflop
- 3-way single-raised pot; hero is BTN, villains SB
- PFR is one of the villains (see action history for confirmation)

### Flop — J♥ 9♣ 6♦
- Action to hero after checks (per: `SB check, BB check, BTN ???`)
- **Decision (hero = BTN): BET or CHECK**

### Key metrics
- **Pot**: 90 | **To call**: 0 | **SPR**: 1.11
- **Equity vs range**: 26.6% | **Equity margin over pot odds**: +26.6%
- **Villain range**: TP+ 26% / med 22% / draw 0% / air 52%
- **Hero range percentile**: 51.2% | **Fold-equity estimate**: 55%
- **Draw outs**: 4 | **Improvement probability**: 8.5%

### What to verify
- Pass 1 votes: **BET/CHECK/CHECK/BET**
- Pass 2 consensus: **CHECK**
- Key question: does GTO Wizard confirm `CHECK` as primary (or at least mixed), or should Pass 1 stand?

---

## 3. `BP7_01` — Tier 2 Pass 1 → Pass 2 flip

**Proposed (Pass 2) label: `CALL`**

> Pass 1 RAISE (T1/T4), Pass 2 panel 2/3 CALL. Nut flush draw + A-blocker on K-high turn at SPR 0.56. Raise = near-jam with FE 38%. Reviewers: SPR commits, call preferred.

### Players
- **Hero**: BTN — A♠J♠
- **Villains**: BB (2 opponents remaining)

### Preflop
- 3-way single-raised pot; hero is BTN, villains BB
- PFR is one of the villains (see action history for confirmation)

### Flop — 9♠ 7♣ 4♠
- Flop checked through 3-way

### Turn — K♦ (board: 9♠ 7♣ 4♠ K♦)
- BB bets **59** into 121 (49% pot)
- **Decision (hero = BTN): CALL / RAISE / FOLD**

### Key metrics
- **Pot**: 180 | **To call**: 59 | **SPR**: 0.56
- **Equity vs range**: 28.8% | **Equity margin over pot odds**: +4.1%
- **Villain range**: TP+ 35% / med 34% / draw 6% / air 25%
- **Hero range percentile**: 43.4% | **Fold-equity estimate**: 38%
- **Draw outs**: 9 | **Improvement probability**: 19.6%

### What to verify
- Pass 1 votes: **RAISE/CALL/CALL/RAISE**
- Pass 2 consensus: **CALL**
- Key question: does GTO Wizard confirm `CALL` as primary (or at least mixed), or should Pass 1 stand?

---

## 4. `d5222_BTN_flop` — Tier 2 Pass 1 → Pass 2 flip

**Proposed (Pass 2) label: `FOLD`**

> Pass 1 CALL (T1/T2), Pass 2 panel 2/3 FOLD. 77 underpair on 9h5h3d. facing_raise=1 flag (MW-50 pattern: bet+raise 3-way = near-nuts).

### Players
- **Hero**: BTN — 7♦7♣
- **Villains**: CO, BB (2 opponents remaining)

### Preflop
- CO opens 2.5bb, BTN (BTN) calls, BB calls
- 3-way to flop

### Flop — 9♥ 5♥ 3♦
- Checked to CO; CO bets **53** into 80 (66% pot)
- Other villains fold / yet to act per action history: `['preflop: BTN call']`
- **Decision (hero = BTN): CALL / RAISE / FOLD**

### Key metrics
- **Pot**: 133 | **To call**: 53 | **SPR**: 0.75
- **Equity vs range**: 28.9% | **Equity margin over pot odds**: +0.4%
- **Villain range**: TP+ 27% / med 13% / draw 51% / air 8%
- **Hero range percentile**: 69.1% | **Fold-equity estimate**: 22%

### What to verify
- Pass 1 votes: **CALL/CALL/FOLD/FOLD**
- Pass 2 consensus: **FOLD**
- Key question: does GTO Wizard confirm `FOLD` as primary (or at least mixed), or should Pass 1 stand?

---

## 5. `d5620_CO_turn` — Tier 2 Pass 1 → Pass 2 flip

**Proposed (Pass 2) label: `FOLD`**

> Pass 1 CALL (T1/T3), Pass 2 panel 3/3 FOLD. Q6dd two pair on JsKs KdQh turn facing bet+raise on paired board. MW-50: raise = boats/sets.

### Players
- **Hero**: CO — Q♦6♦
- **Villains**: BTN, BB (2 opponents remaining)

### Preflop
- CO opens 2.5bb
- Remaining positions fold/call to 3-way pot (hero=CO, villains=BTN, BB)

### Flop — J♠ K♠ K♦
- Flop: CO check (checked through 3-way based on next-street state)

### Turn — Q♥ (board: J♠ K♠ K♦ Q♥)
- BB bets **53** into 80 (66% pot)
- **Decision (hero = CO): CALL / RAISE / FOLD**

### Key metrics
- **Pot**: 133 | **To call**: 53 | **SPR**: 0.75
- **Equity vs range**: 38.7% | **Equity margin over pot odds**: +10.2%
- **Villain range**: TP+ 89% / med 0% / draw 8% / air 3%
- **Hero range percentile**: 63.3% | **Fold-equity estimate**: 1%

### What to verify
- Pass 1 votes: **CALL/FOLD/CALL/FOLD**
- Pass 2 consensus: **FOLD**
- Key question: does GTO Wizard confirm `FOLD` as primary (or at least mixed), or should Pass 1 stand?

---

## 6. `d5749_HJ_turn` — Tier 2 Pass 1 → Pass 2 flip

**Proposed (Pass 2) label: `FOLD`**

> Pass 1 CALL (T1/T4), Pass 2 panel 3/3 FOLD. 99 underpair on JcJ3h5c2h after checked flop; now facing bet+raise. KB DO-NOT #3: 3-way check-raise = near-nuts.

### Players
- **Hero**: HJ — 9♦9♣
- **Villains**: BTN, BB (2 opponents remaining)

### Preflop
- HJ opens 2.5bb
- Remaining positions fold/call to 3-way pot (hero=HJ, villains=BTN, BB)

### Flop — J♣ 3♥ 5♣
- Flop: HJ check (checked through 3-way based on next-street state)

### Turn — 2♥ (board: J♣ 3♥ 5♣ 2♥)
- BB bets **53** into 80 (66% pot)
- **Decision (hero = HJ): CALL / RAISE / FOLD**

### Key metrics
- **Pot**: 133 | **To call**: 53 | **SPR**: 0.75
- **Equity vs range**: 32.8% | **Equity margin over pot odds**: +4.3%
- **Villain range**: TP+ 43% / med 15% / draw 39% / air 3%
- **Hero range percentile**: 68.4% | **Fold-equity estimate**: 14%

### What to verify
- Pass 1 votes: **CALL/FOLD/FOLD/CALL**
- Pass 2 consensus: **FOLD**
- Key question: does GTO Wizard confirm `FOLD` as primary (or at least mixed), or should Pass 1 stand?

---

## 7. `d8002_BTN_flop` — Tier 2 Pass 1 → Pass 2 flip

**Proposed (Pass 2) label: `CALL`**

> Pass 1 FOLD (T1/T4), Pass 2 panel 2/3 CALL. 77 on 5s3cTh. facing_raise=1 flag appears mis-set (num_callers_to_bet=0, villain_aggression_count=1 = standard c-bet). Reviewers treated as normal BTN defend.

### Players
- **Hero**: BTN — 7♠7♦
- **Villains**: HJ, BB (2 opponents remaining)

### Preflop
- HJ opens 2.5bb, BTN (BTN) calls, BB calls
- 3-way to flop

### Flop — 5♠ 3♣ T♥
- Checked to HJ; HJ bets **53** into 80 (66% pot)
- Other villains fold / yet to act per action history: `['preflop: BTN call']`
- **Decision (hero = BTN): CALL / RAISE / FOLD**

### Key metrics
- **Pot**: 133 | **To call**: 53 | **SPR**: 0.75
- **Equity vs range**: 34.0% | **Equity margin over pot odds**: +5.5%
- **Villain range**: TP+ 47% / med 17% / draw 0% / air 36%
- **Hero range percentile**: 69.1% | **Fold-equity estimate**: 28%

### What to verify
- Pass 1 votes: **FOLD/CALL/CALL/FOLD**
- Pass 2 consensus: **CALL**
- Key question: does GTO Wizard confirm `CALL` as primary (or at least mixed), or should Pass 1 stand?

---

## 8. `d8886_BTN_flop` — Tier 2 Pass 1 → Pass 2 flip

**Proposed (Pass 2) label: `CHECK`**

> Pass 1 BET (T1/T4), Pass 2 panel 2/3 CHECK. 99 on 2s5dJd as non-PFA IP after BB/CO check-through. KB DO-NOT #4: non-PFA auto-bet forbidden.

### Players
- **Hero**: BTN — 9♣9♦
- **Villains**: CO, BB (2 opponents remaining)

### Preflop
- CO opens 2.5bb, BTN (BTN) calls, BB calls
- 3-way to flop

### Flop — 2♠ 5♦ J♦
- **Decision (hero = BTN): BET or CHECK**

### Key metrics
- **Pot**: 80 | **To call**: 0 | **SPR**: 1.25
- **Equity vs range**: 39.4% | **Equity margin over pot odds**: +39.4%
- **Villain range**: TP+ 18% / med 23% / draw 0% / air 59%
- **Hero range percentile**: 72.8% | **Fold-equity estimate**: 67%

### What to verify
- Pass 1 votes: **BET/CHECK/CHECK/BET**
- Pass 2 consensus: **CHECK**
- Key question: does GTO Wizard confirm `CHECK` as primary (or at least mixed), or should Pass 1 stand?

---

## 9. `d8963_HJ_turn` — Tier 2 Pass 1 → Pass 2 flip

**Proposed (Pass 2) label: `CHECK`**

> Pass 1 BET (T1/T3), Pass 2 panel 3/3 CHECK. JJ underpair on Ks4h9c3h turn after HJ (PFA) checked the flop. Pot-control vs. thin value bet.

### Players
- **Hero**: HJ — J♥J♣
- **Villains**: BTN, BB (2 opponents remaining)

### Preflop
- HJ opens 2.5bb
- Remaining positions fold/call to 3-way pot (hero=HJ, villains=BTN, BB)

### Flop — K♠ 4♥ 9♣
- Flop: HJ check (checked through 3-way based on next-street state)

### Turn — 3♥ (board: K♠ 4♥ 9♣ 3♥)
- Checked to hero
- **Decision (hero = HJ): BET or CHECK**

### Key metrics
- **Pot**: 80 | **To call**: 0 | **SPR**: 1.25
- **Equity vs range**: 38.5% | **Equity margin over pot odds**: +38.5%
- **Villain range**: TP+ 28% / med 40% / draw 31% / air 1%
- **Hero range percentile**: 61.1% | **Fold-equity estimate**: 32%

### What to verify
- Pass 1 votes: **BET/CHECK/BET/CHECK**
- Pass 2 consensus: **CHECK**
- Key question: does GTO Wizard confirm `CHECK` as primary (or at least mixed), or should Pass 1 stand?

---

## 10. `d1983_BTN_turn` — Tier 5 over-aggression flag

**Proposed (Pass 2) label: `CHECK`**

> All 4 Pass 1 teams BET. Pass 2 challenger CHECK. Ad4d nut flush draw on Jd7dKh2c turn, 28.8% equity, 19.6% improvement, SPR 1.25. Challenger: KB 1.7 semi-bluff fails at low SPR with poor equity-when-called.

### Players
- **Hero**: BTN — A♦4♦
- **Villains**: HJ, BB (2 opponents remaining)

### Preflop
- HJ opens 2.5bb, BTN (BTN) calls, BB calls
- 3-way to flop

### Flop — J♦ 7♦ K♥
- Flop: BTN check (checked through 3-way based on next-street state)

### Turn — 2♣ (board: J♦ 7♦ K♥ 2♣)
- Checked to hero
- **Decision (hero = BTN): BET or CHECK**

### Key metrics
- **Pot**: 80 | **To call**: 0 | **SPR**: 1.25
- **Equity vs range**: 28.8% | **Equity margin over pot odds**: +28.8%
- **Villain range**: TP+ 23% / med 45% / draw 8% / air 23%
- **Hero range percentile**: 45.0% | **Fold-equity estimate**: 53%
- **Draw outs**: 9 | **Improvement probability**: 19.6%

### What to verify
- Pass 1 votes: **BET/BET/BET/BET**
- Pass 2 consensus: **CHECK**
- Key question: does GTO Wizard confirm `CHECK` as primary (or at least mixed), or should Pass 1 stand?

---

## Solver pre-flight reminders

- Flop bet sizes to use: **25% or 66% pot** (GTO Wizard options; not 33% or 50%)
- Turn sizes: **33% or 75% pot**
- River sizes: **33% / 75% / 150% pot**
- If a specific hand combo isn't available in GTO Wizard, pick the closest combo of the same suit pattern and note the substitution

## How to log results

For each hand, record in a reply:

| # | ID | Pass 2 label | Solver result | Match? | Notes |
|---|---|---|---|---|---|
| 1 | BP5_01 | BET | — | — | — |
