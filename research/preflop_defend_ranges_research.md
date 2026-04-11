# Preflop Defending Ranges Research: 6-Max Cash 100bb GTO

**Date:** 2026-04-06
**Purpose:** Establish correct GTO defending (calling + 3-betting) frequencies for the River Rats engine.
**Current engine problem:** BTN calls 4%, BB defends 5%. Both are catastrophically low.

---

## Executive Summary

Solver-based GTO solutions for 6-max 100bb cash games show defending frequencies dramatically higher than the current engine values:

| Matchup | Current Engine | GTO Approximate | Gap |
|---------|---------------|-----------------|-----|
| BTN call vs CO open | ~4% | ~13-16% | 3-4x too low |
| BB defend vs BTN open | ~5% | ~44-55% | 9-11x too low |
| BB defend vs CO open | ~5% | ~35-40% | 7-8x too low |
| BB defend vs HJ open | ~5% | ~30-35% | 6-7x too low |

---

## 1. Who Can Cold Call in GTO 6-Max?

A critical finding from solver solutions: **only the BTN and BB have significant cold-calling ranges** in standard 6-max GTO play. All other positions facing an open raise play a 3-bet-or-fold strategy.

### Position-by-Position Cold Call Policy

| Position | Facing Open From | Strategy |
|----------|-----------------|----------|
| **SB** | Any position | **3-bet or fold only** (no cold calls) |
| **BB** | Any position | Call + 3-bet (widest defending range in the game) |
| **BTN** | LJ/HJ/CO | Call + 3-bet (significant calling range) |
| **CO** | LJ/HJ | **3-bet or fold** (virtually no cold calls in raked games) |
| **HJ** | LJ | **3-bet or fold** (virtually no cold calls) |

**Source:** GTOBase 6-max cash library confirms that in main solver trees, only BB calls and BTN calls were kept as cold-call actions. CO/HJ/SB facing opens use 3-bet-or-fold. GTO Wizard preflop morphology articles confirm this structure.

---

## 2. Opening Range Baselines (for context)

Standard GTO opening (RFI) ranges at 100bb, 6-max:

| Position | Open % |
|----------|--------|
| LJ (UTG) | ~17-18% |
| HJ | ~21-22% |
| CO | ~27-28% |
| BTN | ~43-45% |
| SB | ~50-62% (wide range, includes limps in some solutions) |

---

## 3. BTN Defending vs Open Raises

### BTN vs CO Open (~27% open range, 2.5x sizing)

**Total continue: ~22-25%** (of all hands)
- **Call: ~13-16%**
- **3-bet: ~8-10%**

#### BTN Calling Range vs CO (Implementable)

**Pocket Pairs (call):** 55-99 (TT is mixed call/3-bet, JJ+ pure 3-bet)
**Suited Broadways (call):** AJs, ATs, KQs, KJs, KTs, QJs, QTs, JTs
**Suited Connectors:** T9s, 98s, 87s, 76s, 65s (some mixed)
**Suited Aces (call):** A5s, A4s, A3s, A2s (suited wheel aces -- mixed call/3-bet)
**Offsuit (call):** AQo, AJo (mixed), KQo (mixed)

**Key principle:** The BTN cold-call range is "condensed" -- it is missing the nutted ceiling (those hands 3-bet) and has very little trash from the floor. It consists primarily of medium-strength hands with good playability.

#### BTN 3-Bet Range vs CO (Implementable)

**Value:** QQ+, AKs, AKo, AQs (pure or high frequency)
**Mixed value/call:** TT-JJ, AJs, AQo
**Bluffs:** A5s-A4s (some frequency), K9s, Q9s, J9s, T8s, small suited connectors at low frequency

### BTN vs HJ Open (~21% open range)

**Total continue: ~18-22%**
- **Call: ~10-14%**
- **3-bet: ~7-9%**

The calling range tightens slightly vs HJ compared to CO. Drop bottom of suited connectors (65s, 76s become folds), tighten offsuit broadways.

### BTN vs LJ/UTG Open (~17% open range)

**Total continue: ~14-18%**
- **Call: ~8-12%** (GTO Wizard data: BTN plays ~16% of hands vs UTG when given call option)
- **3-bet: ~5-7%**

Important finding: "When given the option to call, BTN can play nearly 16% of hands against a UTG open. When forced to only 3-bet or fold, this drops to under 10%." This proves cold-calling adds significant strategic value.

---

## 4. BB Defending vs Open Raises

The BB is the most important defending position because:
1. You already have 1 BB invested (discount on calling)
2. You close the action preflop (no squeeze risk)
3. You face every opener's range

### BB vs BTN Open (~43% range, 2.5x sizing)

**Total continue: ~44-55%** (solver output: 44% continue is a commonly cited number)
- **Call: ~32-40%**
- **3-bet: ~10-14%**

Defend ~50% as a starting point against 2.5x from BTN. Solver says 44% minimum continue.

#### BB Calling Range vs BTN (Implementable -- WIDE)

**Pocket Pairs:** 22-TT (JJ+ typically 3-bet)
**Suited Aces:** A2s-ATs (AJs+ typically 3-bet)
**Suited Kings:** K2s-KTs (KJs+ mixed 3-bet)
**Suited Queens:** Q8s-QTs (QJs mixed)
**Suited Jacks:** J8s-JTs
**Suited Connectors:** T7s+, 96s+, 85s+, 74s+, 63s+, 53s+, 43s
**Offsuit Broadways:** ATo-AQo, KJo-KQo, QJo, JTo (AKo 3-bets)
**Offsuit Connected:** K9o-KTo, Q9o+, J9o+, T9o, 98o, 87o, 76o, 65o

This is a very wide range -- roughly 35-40% of all hands call, with another 10-14% 3-betting.

#### BB 3-Bet Range vs BTN (Implementable)

**Value:** AA-JJ, AKs, AKo, AQs, AQo (some frequency), AJs (some)
**Bluffs/Semi-bluffs:** A8o, A5s-A2s (blockers), KTo, K9o, K7s, J8s, T7s, small suited connectors at low frequency

### BB vs CO Open (~27% range, 2.5x sizing)

**Total continue: ~35-42%**
- **Call: ~25-32%**
- **3-bet: ~8-12%**

#### BB Calling Range vs CO (Implementable)

**Pocket Pairs:** 22-TT
**Suited Aces:** A2s-ATs
**Suited Kings:** K8s-KQs
**Suited Queens:** Q9s-QJs
**Suited Jacks:** J9s-JTs
**Suited Connectors:** T9s, 98s, 87s, 76s, 65s, 54s (some)
**Offsuit:** ATo-AQo, KJo-KQo, QJo, JTo

Tighter than vs BTN -- drop the weakest suited trash, some offsuit connectors, weakest suited Kings.

### BB vs HJ Open (~21% range)

**Total continue: ~28-35%**
- **Call: ~20-26%**
- **3-bet: ~7-10%**

Tighten further. Drop small pocket pairs below 44, drop weak suited connectors, tighten offsuit range.

### BB vs LJ/UTG Open (~17% range)

**Total continue: ~22-28%**
- **Call: ~16-20%**
- **3-bet: ~5-8%**

Tightest defend. Core is: 22-TT, A2s-ATs, KTs+, QTs+, JTs, T9s, 98s, 87s, ATo+, KQo.

### BB Defend % Scaling Rule

The later the opener's position, the wider the BB defends:
- vs LJ: ~22-28% total
- vs HJ: ~28-35% total
- vs CO: ~35-42% total
- vs BTN: ~44-55% total
- vs SB: ~50-60% total (widest, because SB opens widest)

---

## 5. SB Facing Open Raises

**The SB plays a 3-bet-or-fold strategy in GTO.** No cold calling.

### SB 3-Bet Ranges (vs different openers)

| Facing | 3-Bet % | Fold % |
|--------|---------|--------|
| vs LJ open | ~5-7% | ~93-95% |
| vs HJ open | ~7-9% | ~91-93% |
| vs CO open | ~9-12% | ~88-91% |
| vs BTN open | ~12-16% | ~84-88% |

The SB 3-bet range is polarized: premiums for value + suited blockers (A5s, A4s type hands) as bluffs.

---

## 6. CO Facing HJ/LJ Opens

The CO uses a **3-bet-or-fold strategy** in most solver solutions at 100bb with rake.

### CO vs HJ Open

- **3-bet: ~8-11%**
- **Call: ~0-2%** (negligible; solvers essentially remove cold calls here due to rake + being OOP vs BTN squeeze risk)
- **Fold: ~87-92%**

### CO vs LJ Open

- **3-bet: ~6-8%**
- **Fold: ~92-94%**

---

## 7. Key Structural Rules for the Engine

### Rule 1: Only BTN and BB Have Cold-Call Ranges
All other positions facing an open: 3-bet or fold.

### Rule 2: BB Defends Widest
BB always has the widest continue range because of the pot-odds discount and closing the action.

### Rule 3: Position Scaling
BB defend % increases as the opener is in later position (wider open = wider defend).

### Rule 4: BTN Always Has a Call Range vs Any Opener
BTN calls range from ~8% (vs UTG) to ~16% (vs CO), plus 3-bets on top.

### Rule 5: Calling Ranges Are Condensed
Cold-call ranges lack the top (those hands 3-bet) and the bottom (those fold). They are medium-strength hands with good playability: medium pairs, suited broadways, suited connectors, suited aces.

### Rule 6: Raise Size Matters
Against 2x: defend wider (better odds)
Against 2.5x: standard ranges above
Against 3x: tighten by ~5-10%

---

## 8. Recommended Engine Target Values

Based on the research, here are the target percentages for the engine:

### BTN Facing Opens (Call + 3-Bet = Total Continue)

| Opener | BTN Call % | BTN 3-Bet % | BTN Total % |
|--------|-----------|-------------|-------------|
| LJ | 10% | 6% | 16% |
| HJ | 12% | 8% | 20% |
| CO | 15% | 9% | 24% |

### BB Facing Opens

| Opener | BB Call % | BB 3-Bet % | BB Total % |
|--------|----------|-----------|-----------|
| LJ | 18% | 7% | 25% |
| HJ | 23% | 9% | 32% |
| CO | 28% | 10% | 38% |
| BTN | 35% | 12% | 47% |
| SB | 40% | 15% | 55% |

### SB Facing Opens (3-bet or fold)

| Opener | SB 3-Bet % |
|--------|-----------|
| LJ | 6% |
| HJ | 8% |
| CO | 10% |
| BTN | 14% |

### Other Positions (3-bet or fold)

| Matchup | 3-Bet % |
|---------|---------|
| CO vs LJ | 7% |
| CO vs HJ | 9% |
| HJ vs LJ | 6% |

---

## 9. Comparison: Current Engine vs GTO Targets

| Scenario | Current | Target | Multiplier Needed |
|----------|---------|--------|-------------------|
| BTN call vs CO | 4% | 15% | 3.75x |
| BTN total vs CO | ~7% | 24% | 3.4x |
| BB defend vs BTN | 5% | 47% | 9.4x |
| BB defend vs CO | 5% | 38% | 7.6x |
| BB call vs BTN | ~3% | 35% | 11.7x |

The current engine is folding far too much from both the BTN and BB, which means:
1. Opponents can profitably open any two cards against these positions
2. The engine hemorrhages equity by surrendering blinds
3. Postflop play is irrelevant because the engine never gets there with enough hands

---

## 10. Sources

- [GTO Wizard: Preflop Range Morphology](https://blog.gtowizard.com/preflop-range-morphology/)
- [GTO Wizard: Playing Calls From the Button in Cash Games](https://blog.gtowizard.com/playing-calls-from-the-button-in-cash-games/)
- [GTO Wizard: MDF & Alpha](https://blog.gtowizard.com/mdf-alpha/)
- [GTOBase: Overview of 6-Max Cash Library](https://blog.gtobase.com/theory/overview-of-the-new-gto-poker-solutions-in-the-6-max-cash-library/)
- [Upswing Poker: 6-Handed Poker Strategy](https://upswingpoker.com/6-handed-max-poker-strategy/)
- [Upswing Poker: 3-Bet Strategy](https://upswingpoker.com/3-bet-strategy-aggressive-preflop/)
- [PokerCoaching: GTO Charts (PDF)](https://poker-coaching.s3.amazonaws.com/tools/preflop-charts/online-6max-gto-charts.pdf)
- [FreeBetRange: Smart Preflop Ranges for 6-Max](https://blog.freebetrange.com/article/smart-preflop-ranges-for-6-max-no-limit-holdem)
- [Poker Trainer: Preflop Calling Ranges](https://pokertrainer.se/preflop-calling-ranges/)
- [Poker Trainer: Preflop 3-Betting Ranges](https://pokertrainer.se/preflop-3-betting-ranges/)
- [BetAndBeat: Preflop Calling Ranges](https://betandbeat.com/poker/strategy/preflop/calling-ranges/)
- [VIP-Grinders: Defend BB vs BTN in Zoom](https://www.vip-grinders.com/defend-the-big-blind-vs-button/)
- [GetCoach: How to Defend from the BB](https://www.getcoach.poker/articles/how-to-defend-from-the-big-blind/)
- [PokerVIP Forum: BTN Calling Range vs CO Open](https://www.pokervip.com/forum/general-discussion/btn-calling-range-vs-co-open)
- [MicroGrinder: Defending Your Big Blind](https://microgrinder.com/poker-strategy-articles/defending-your-big-blind/)
- [Run It Once: BB Defense Frequencies](https://www.runitonce.com/nlhe/question-on-bb-defense-frequencies-preflop/)
- [Simple GTO: 6-Max 100bb Preflop Solutions](https://simplegto.com/product/6-max-100bb-500z-cash-game-preflop-solution/)
- [RangeConverter: 6-Max 100bb Poker Charts](https://rangeconverter.com/articles/poker-charts-6-max-100bb-no-limit-texas-holdem)
- [HHDealer: How to Defend Blinds](https://hhdealer.com/blog/how-to-defend-blinds-in-poker-strategy-and-key-statistics/)
