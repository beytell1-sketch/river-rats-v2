# Batch 1 Range Analysis: Retrofit Against Fixed Pipeline

**Date:** 2026-04-05
**Author:** GTO Expert
**Pipeline:** Post-Fix (Fix 1: opener-aware ranges, Fix 2: bettor-aware narrowing, Fix 3: SB calling)
**Commit:** dd40bac

---

## Methodology

Each hand is analysed with the **correct** opponent ranges:
- **Opener (CO):** `RFI['CO']` — the opening range (~53 hands, ~222 weighted combos)
- **BTN cold-caller:** `DEFEND['BTN']['vs_CO']` — defend range vs CO (~43 hands, ~181 combos)
- **SB cold-caller:** `DEFEND['SB']['vs_CO']` — defend range vs CO (~19 hands, ~74 combos)
- **When CO bets:** Only CO's range is narrowed to the betting range. BTN/SB retain full defend ranges.
- **When not facing a bet:** All opponents retain full preflop ranges.

Equity values are from the fixed pipeline (`extract_all_features` with `_opener_position` and `_bettor_position` set).

Pot odds for facing a 33 bet into 100: `33 / (100 + 33)` = **24.8%**

---

## Scenario: CO Opens, BTN Calls, SB Calls, BB Hero

All hands use this preflop action unless noted otherwise.

---

## MW-01a: K♠T♥ on K♣8♦5♠ — Top Pair, T Kicker Facing CO Bet

**Preflop action:** CO opens, BTN calls, SB calls, BB (hero) calls
**Flop:** K♣ 8♦ 5♠ (rainbow, dry)
**Action:** CO bets 33 into 100. Hero must decide.

### Opponent Ranges (corrected)

| Opponent | Range Type | Weighted Combos (board-adjusted) |
|----------|-----------|----------------------------------|
| CO (bettor) | RFI['CO'] → narrowed to betting range | ~4.4 (normalized) |
| BTN (caller) | DEFEND['BTN']['vs_CO'] full | ~156.2 |
| SB (caller) | DEFEND['SB']['vs_CO'] full | ~62.2 |

### Combo Analysis vs CO Betting Range (K♣8♦5♠)

CO bets into 3 opponents on a dry K-high board. CO's betting range is polarized:
- **Value:** KK(set), 88(set), 55(set), AA-99(overpairs), AK(TPTK) — all bet at 0.70-0.85
- **Medium:** KQ, KJ, KT(top pair) — bet at 0.45
- **Bluffs:** AQ, AJ, AT(overcards) — bet at 0.20-0.25

Hero KT: beats CO's bluffs and air, loses to overpairs/sets/better Kx. ~61% of CO's betting range is weaker.

### Pipeline Features

| Feature | Old Pipeline | Fixed Pipeline | Delta |
|---------|-------------|----------------|-------|
| raw_equity | 0.468 | 0.294 | **-0.174** |
| equity_margin | +0.219 | +0.046 | -0.173 |
| better_hand_pct | 0.120 | 0.207 | +0.087 |
| worse_hand_pct | 0.862 | 0.786 | -0.076 |

### GTO Action Assessment

**Old pipeline:** equity_margin +0.219 → comfortable CALL (well above pot odds)
**Fixed pipeline:** equity_margin +0.046 → **marginal CALL** (barely above pot odds of 0.248)

**GTO Action: CALL** — unchanged but now correctly identified as marginal.

Top pair T kicker on a dry board has enough equity against the field at these pot odds (24.8%), but this is no longer the easy call the old pipeline suggested. The -17.4pp equity drop is the largest single correction.

**Axis insight:** Against correct (tighter) defend ranges, the callers behind hold more premium hands. BTN defend vs CO is heavily weighted toward broadways and pairs — far more threatening than the full BTN RFI range.

---

## MW-01b: A♥Q♦ on K♣8♦5♠ — Overcards Facing CO Bet

### Pipeline Features

| Feature | Old Pipeline | Fixed Pipeline | Delta |
|---------|-------------|----------------|-------|
| raw_equity | 0.122 | 0.073 | -0.049 |
| equity_margin | -0.126 | -0.175 | -0.049 |
| better_hand_pct | 0.510 | 0.575 | +0.065 |

### GTO Action Assessment

**Old pipeline:** equity_margin -0.126 → clear FOLD
**Fixed pipeline:** equity_margin -0.175 → even clearer FOLD

**GTO Action: FOLD** — unchanged, confirmed more strongly.

AQ has no pair on K85r. 6 outs to TPTK (3 aces + 3 queens) but 3 opponents. Equity drops from 12.2% to 7.3% — well below the 24.8% pot odds needed. Zero implied odds for overcards in a multiway pot where someone has a K.

---

## MW-01c: 9♠9♥ on K♣8♦5♠ — Underpair Facing CO Bet

### Pipeline Features

| Feature | Old Pipeline | Fixed Pipeline | Delta |
|---------|-------------|----------------|-------|
| raw_equity | 0.210 | 0.119 | **-0.091** |
| equity_margin | -0.038 | -0.129 | -0.091 |
| better_hand_pct | 0.279 | 0.401 | +0.122 |

### GTO Action Assessment

**Old pipeline:** equity_margin -0.038 → close to breakeven, could argue CALL with set-mining implied odds
**Fixed pipeline:** equity_margin -0.129 → clear FOLD

**GTO Action: FOLD** — unchanged but now much more decisive.

99 is an underpair on a K-high board. Against correct defend ranges, 40.1% of the field beats us (up from 27.9%). The tighter defend ranges are more pair-heavy and broadway-heavy — exactly the hands that dominate 99 on K85r. With a 2-out set draw and -12.9% equity margin, this is a clear fold that the old pipeline made look close.

---

## MW-01d: K♦J♥ on K♣8♦5♠ — Top Pair J Kicker, Not Facing Bet

**Action:** CO checks. No bet yet. Hero decides.

### Pipeline Features

| Feature | Old Pipeline | Fixed Pipeline | Delta |
|---------|-------------|----------------|-------|
| raw_equity | 0.488 | 0.411 | -0.077 |
| better_hand_pct | 0.096 | 0.143 | +0.047 |
| worse_hand_pct | 0.886 | 0.826 | -0.060 |

### GTO Action Assessment

**Old pipeline:** equity 48.8% → marginal BET
**Fixed pipeline:** equity 41.1% → **CHECK or thin BET**

**GTO Action: CHECK** — changed from BET.

CO checked, which caps CO's range (strong hands would bet). But BTN and SB behind us have uncapped defend ranges that include sets, AK, overpairs. With 3 opponents and only 41.1% equity, betting KJ for value is thin — we're only getting called by better or draws. In a 4-way pot OOP, checking to control pot size and realize equity is the GTO play.

**Action changed: BET → CHECK.** The -7.7pp equity drop moves KJ from thin value to pot control territory. This is a significant coaching correction — the old pipeline would have told the student to bet.

---

## MW-02a: 9♠8♥ on Q♣9♦4♠ — Middle Pair Facing CO Bet (3-way)

**Note:** 3-way pot (SB folded). CO + BTN + BB.

### Pipeline Features

| Feature | Old Pipeline | Fixed Pipeline | Delta |
|---------|-------------|----------------|-------|
| raw_equity | 0.360 | 0.285 | -0.075 |
| equity_margin | +0.112 | +0.037 | -0.075 |

### GTO Action Assessment

**Old pipeline:** equity_margin +0.112 → comfortable CALL
**Fixed pipeline:** equity_margin +0.037 → **barely positive CALL**

**GTO Action: CALL** — unchanged but now correctly marginal.

Middle pair with a weak kicker on Q-high board. 3-way makes this easier than 4-way. Pot odds are 24.8% and we have 28.5% equity — just barely enough. The correct (tighter) BTN defend range removes the junk hands that inflated our equity before.

---

## MW-02b: Q♦T♠ on Q♣9♦4♠ — Top Pair T Kicker Facing CO Bet (3-way)

### Pipeline Features

| Feature | Old Pipeline | Fixed Pipeline | Delta |
|---------|-------------|----------------|-------|
| raw_equity | 0.544 | 0.420 | **-0.124** |
| equity_margin | +0.296 | +0.172 | -0.124 |
| better_hand_pct | 0.138 | 0.218 | +0.080 |

### GTO Action Assessment

**Old pipeline:** equity_margin +0.296 → strong CALL, borderline RAISE
**Fixed pipeline:** equity_margin +0.172 → comfortable CALL

**GTO Action: CALL** — unchanged but significantly recalibrated.

QT for top pair is still a clear call at these pot odds. But the old pipeline's +29.6% equity margin suggested this was close to raising territory. With correct ranges, +17.2% is a solid call — no more, no less. The student should be told to call confidently, not consider raising.

---

## MW-02c: J♥T♦ on Q♣9♦4♠ — OESD Facing CO Bet (3-way)

### Pipeline Features

| Feature | Old Pipeline | Fixed Pipeline | Delta |
|---------|-------------|----------------|-------|
| raw_equity | 0.337 | 0.304 | -0.033 |
| equity_margin | +0.089 | +0.056 | -0.033 |
| better_hand_pct | 0.878 | 0.935 | +0.057 |

### GTO Action Assessment

**Old pipeline:** equity_margin +0.089 → clear CALL (drawing hand with odds)
**Fixed pipeline:** equity_margin +0.056 → still CALL

**GTO Action: CALL** — unchanged.

8-out OESD (any K or 8 makes the straight). Even against tighter ranges, the draw equity plus pot odds justify a call. The -3.3pp equity drop is the smallest of all hands — draws are less affected by range corrections because their equity comes from unseen cards, not range composition.

**Axis insight:** Draw equity is more robust to range corrections than made-hand equity. This is expected — an OESD has ~31% raw draw equity regardless of what opponents hold.

---

## MW-03a: K♠7♥ on K♣9♦4♠ — Weak Top Pair Facing CO Bet

### Pipeline Features

| Feature | Old Pipeline | Fixed Pipeline | Delta |
|---------|-------------|----------------|-------|
| raw_equity | 0.420 | 0.314 | **-0.106** |
| equity_margin | +0.172 | +0.066 | -0.106 |

### GTO Action Assessment

**Old pipeline:** equity_margin +0.172 → comfortable CALL
**Fixed pipeline:** equity_margin +0.066 → **marginal CALL**

**GTO Action: CALL** — unchanged but now correctly shown as marginal.

Weak top pair (7 kicker) is the boundary hand in multiway pots. At 31.4% equity vs 24.8% pot odds, we have just enough to call. But this is the hand where one more opponent or a slightly bigger bet tips us to fold. The coaching system should communicate this thinness.

---

## MW-03b: T♦T♣ on K♣9♦4♠ — Pocket Tens Facing CO Bet

### Pipeline Features

| Feature | Old Pipeline | Fixed Pipeline | Delta |
|---------|-------------|----------------|-------|
| raw_equity | 0.241 | 0.123 | **-0.118** |
| equity_margin | -0.007 | -0.125 | -0.118 |
| better_hand_pct | 0.259 | 0.362 | +0.103 |

### GTO Action Assessment

**Old pipeline:** equity_margin -0.007 → extremely close, could go either way
**Fixed pipeline:** equity_margin -0.125 → clear FOLD

**GTO Action: FOLD** — unchanged but now decisively correct (was a coin flip before).

The old pipeline showed TT as almost breakeven (-0.7% margin), which would create a genuine teaching dilemma. The fixed pipeline reveals it's a clear fold (-12.5% margin). Against tighter defend ranges, 36.2% of the field beats TT (vs 25.9% before). The underpair has 2 outs to a set and nothing else on a K-high board with 3 opponents.

---

## MW-03c: A♠K♦ on K♣9♦4♠ — TPTK, Not Facing Bet

**Action:** CO checks. No bet yet.

### Pipeline Features

| Feature | Old Pipeline | Fixed Pipeline | Delta |
|---------|-------------|----------------|-------|
| raw_equity | 0.603 | 0.564 | -0.039 |
| better_hand_pct | 0.047 | 0.053 | +0.006 |
| worse_hand_pct | 0.934 | 0.915 | -0.019 |

### GTO Action Assessment

**Old pipeline:** equity 60.3% → clear BET for value
**Fixed pipeline:** equity 56.4% → still BET for value

**GTO Action: BET** — unchanged.

TPTK is the strongest non-set/non-two-pair hand possible on K94r. Against 3 opponents, 56.4% equity is very strong — only sets (KK, 99, 44) and K9 two-pair beat us, and those are few combos. CO checking caps their range. BTN and SB defend ranges are premium-heavy but most of their premiums are overpairs (AA, QQ, JJ, TT) which we beat with top pair + ace kicker.

The small equity drop (-3.9pp) shows that TPTK is robust — premium hands are less sensitive to range corrections because they dominate most of the field regardless.

---

## Summary

### Equity Impact

| Hand | Old Equity | Fixed Equity | Delta | Direction |
|------|-----------|-------------|-------|-----------|
| MW-01a (KT, K85r, facing bet) | 0.468 | 0.294 | **-0.174** | Largest drop |
| MW-01b (AQ, K85r, facing bet) | 0.122 | 0.073 | -0.049 | |
| MW-01c (99, K85r, facing bet) | 0.210 | 0.119 | -0.091 | |
| MW-01d (KJ, K85r, no bet) | 0.488 | 0.411 | -0.077 | |
| MW-02a (98, Q94r, facing bet) | 0.360 | 0.285 | -0.075 | |
| MW-02b (QT, Q94r, facing bet) | 0.544 | 0.420 | -0.124 | |
| MW-02c (JT, Q94r, OESD) | 0.337 | 0.304 | -0.033 | Smallest drop |
| MW-03a (K7, K94r, facing bet) | 0.420 | 0.314 | -0.106 | |
| MW-03b (TT, K94r, facing bet) | 0.241 | 0.123 | -0.118 | |
| MW-03c (AK, K94r, no bet) | 0.603 | 0.564 | -0.039 | |

**Average equity drop: -8.9 percentage points**
**Median equity drop: -8.4 percentage points**
**Range: -3.3pp (draws) to -17.4pp (medium made hands facing bet)**

### Actions Changed

| Hand | Old Action | New Action | Reason |
|------|-----------|------------|--------|
| MW-01d (KJ, K85r) | BET | **CHECK** | Equity dropped from 48.8% to 41.1%. Against correct defend ranges with 3 opponents, KJ is pot control territory OOP, not thin value. |

**1 of 10 actions changed (10%).**

### Systematic Patterns

1. **Medium made hands facing a bet see the largest equity drops** (MW-01a: -17.4pp, MW-02b: -12.4pp, MW-03b: -11.8pp). These hands relied most on beating the junk in wide RFI ranges. When opponents have tighter defend ranges, the junk is gone and medium hands face a tougher field.

2. **Draws are least affected** (MW-02c: -3.3pp). Draw equity comes from unseen cards (outs to straights/flushes), not from outranking opponents' current holdings. Range corrections barely change draw equity.

3. **Premium hands are moderately affected** (MW-03c: -3.9pp). TPTK dominates most hands regardless of range width. The correction is directionally correct but small.

4. **Hands not facing a bet see smaller drops** than hands facing a bet (MW-01d: -7.7pp, MW-03c: -3.9pp vs facing-bet average of -9.6pp). This is because non-bet hands compare against full preflop ranges (no narrowing), while facing-bet hands compare against the bettor's narrowed range plus callers' full ranges — a more polarized field.

5. **All equity drops are negative.** The old pipeline systematically inflated hero equity by assigning opponents wider-than-reality ranges. The fixed pipeline corrects this inflation by ~9pp on average.

6. **Equity margin shifts affect coaching recommendations.** Several hands moved from "comfortable call" to "marginal call" territory. While only one action changed outright (MW-01d), the coaching language should change for MW-01a, MW-02a, MW-03a — all now correctly identified as marginal rather than comfortable.

---

[BATCH1 RANGE ANALYSIS] COMPLETE
