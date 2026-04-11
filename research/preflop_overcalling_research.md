# Preflop Overcalling & Squeeze Dynamics: GTO Solver Research

**Date:** 2026-04-06  
**Sources:** GTO Wizard, Upswing Poker, PokerCoaching, Raise Your Edge, solver-derived data  
**Game type:** 6-max NL cash, 100bb effective, with rake

---

## Executive Summary

**The counterintuitive finding:** Despite better pot odds, BB defends TIGHTER (not wider) when there are callers in the pot. The equity realization penalty of multiway pots more than cancels out the improved pot odds. BB also shifts toward a more linear 3-bet (squeeze) strategy, removing many strong hands from the calling range.

---

## 1. Baseline: BB Defense vs a Single Raiser (Heads-Up to Flop)

### BB Defend Frequencies vs Single Opener (approx, 100bb cash, 2.5x open)

| Opener | BB Total Defend | BB Call | BB 3-Bet | BB Fold |
|--------|----------------|---------|----------|---------|
| HJ     | ~32-35%        | ~24-27% | ~8%      | ~65-68% |
| CO     | ~35-40%        | ~27-32% | ~8-9%    | ~60-65% |
| BTN    | ~45-52%        | ~35-42% | ~10-12%  | ~48-55% |
| SB     | ~55-65%        | ~42-50% | ~13-16%  | ~35-45% |

**Key principle:** BB defends wider against later position opens because those ranges are wider, giving BB more equity. The BTN opens ~43.5% of hands; the HJ opens ~21.4%.

### Pot Odds (Heads-Up)
- BB faces 2.5bb open: needs to call 1.5bb to win pot of ~4bb (SB 0.5 + BB 1.0 + open 2.5)
- Pot odds: 1.5 into 4.0 = 27% equity needed (before rake/EQR adjustments)
- After EQR adjustment (~70-80% OOP): effective equity needed ~34-38%

---

## 2. How the Pot Changes with a Caller

### CO Opens, BTN Calls -- BB to Act

**Pot odds improve significantly:**
- Pot before BB acts: SB 0.5 + BB 1.0 + CO open 2.5 + BTN call 2.5 = 6.5bb
- BB must call 1.5bb to win 6.5bb
- Pot odds: 1.5 into 6.5 = **18.8% equity needed** (raw)
- Compare to heads-up: 27% needed -- that is a 30% reduction in required equity

**But equity realization DROPS HARD multiway:**
- Heads-up OOP EQR: ~70-80%
- 3-way OOP EQR: ~55-65%
- Some weaker hands: EQR drops to ~50% or below

### The Critical Insight (from GTO Wizard)

> "A common mistake that many players make is they believe that the BB should defend a much wider preflop range after SB calls an IP open, but this is not usually the case. Yes, you're getting better pot odds, but your equity retention multiway is much worse."

> "At all stack depths, BB folds MORE and calls LESS as more people call in front of them."

**This is the key finding. BB does NOT defend wider with a caller. BB defends TIGHTER.**

---

## 3. Quantified Impact: BB Defend % With vs Without Caller

### Estimated BB Action Frequencies (CO open, 100bb cash)

| Scenario             | BB Fold | BB Call | BB 3-Bet/Squeeze | BB Total Defend |
|----------------------|---------|---------|-------------------|-----------------|
| CO opens (HU)        | ~60-65% | ~27-32% | ~8-9%             | ~35-40%         |
| CO opens, BTN calls  | ~63-70% | ~20-25% | ~9-12%            | ~30-37%         |
| CO opens, BTN+SB call| ~68-75% | ~16-20% | ~10-13%           | ~25-32%         |

### The Delta

- BB defend vs CO alone: ~35-40%
- BB defend vs CO + BTN call: ~30-37%
- **Delta: approximately -3% to -8% TIGHTER (not wider)**
- The more callers, the tighter BB's CALLING range becomes
- But BB's SQUEEZING frequency slightly increases (more dead money to pick up)

### Why the Tightening Happens

1. **Equity realization collapse:** OOP multiway, marginal hands like weak Ax, Kxo, disconnected hands cannot profitably see flops. Example from Raise Your Edge: a hand with 35% raw equity may only realize ~60% of it, dropping to ~21% effective equity -- below the 25% threshold needed.

2. **Showdown requirements increase:** In a heads-up pot, top pair is often good. In a 3-way pot, you need significantly stronger hands to win at showdown.

3. **Reverse implied odds:** Dominated hands (K7o, A3o, Q8o) are in much worse shape multiway. When you hit top pair, another player is more likely to have a better kicker or two pair.

4. **Reduced bluffing opportunities:** Postflop, BB cannot bluff as effectively into multiple opponents, reducing the value of speculative hands that rely partly on fold equity.

---

## 4. Which Hands Change Action?

### Hands That DROP from BB's Calling Range Multiway

These hands call HU but fold with a caller:
- **Weak offsuit broadways:** KTo, QTo, JTo, K9o, Q9o
- **Disconnected offsuit hands:** A8o-A2o, K8o-K2o
- **Weak suited hands:** K2s-K5s, Q2s-Q6s
- **Low pairs (sometimes):** 22-44 (reduced calling frequency)

### Hands That STAY in BB's Calling Range

These hands still call (or call more) with a caller:
- **Suited connectors:** 54s-T9s (make nutted hands multiway)
- **Suited aces:** A2s-A9s (nut flush potential)
- **Medium-high pairs:** 55-99 (set mining with better implied odds)
- **Suited gappers:** 75s, 86s, 97s (nutted straight/flush potential)

### The Pattern

BB's calling range SHIFTS from "wide and exploitative" to "narrow and nutted." Hands that make one pair are cut. Hands that make flushes, straights, and sets are retained because:
- They can win big pots multiway
- Their nutted potential justifies the reduced EQR on other boards
- Set mining and flush draws have better implied odds multiway (more money in the pot)

---

## 5. The Squeeze Dynamic

### When Should BB 3-Bet (Squeeze) vs Overcall?

When there is a caller in the pot, BB's 3-betting becomes a "squeeze" -- and it becomes MORE attractive, not less.

#### Why Squeezing Increases with Callers

1. **More dead money:** Pot is 6.5bb+ instead of 4bb. A squeeze to ~10-11bb risks 10bb to win 6.5bb. Opponents only need to fold ~60% of the time for auto-profit.

2. **Caller's range is capped:** The BTN flat-caller has already defined their range as "not strong enough to 3-bet." They hold medium pairs, suited broadways, suited connectors -- not AA/KK/AKs. They fold frequently to a squeeze.

3. **Positional leverage:** BB is squeezing from OOP, but the squeeze itself takes away the positional disadvantage by often winning the pot preflop.

### Squeeze Frequencies (solver-derived)

| Scenario                 | BB Squeeze % | Typical Sizing |
|--------------------------|-------------|----------------|
| CO open, BTN call        | ~9-12%      | 10-11bb        |
| HJ open, CO call         | ~8-10%      | 10-11bb        |
| HJ open, CO call, BTN call | ~10-13%  | 11-13bb        |
| MTT (40bb eff)           | ~12-13%     | 10bb or shove   |

**More callers = slightly higher squeeze frequency** because there is more dead money and the callers' ranges are weaker (capped).

### What Hands Squeeze vs Overcall?

**Pure squeeze (always 3-bet):**
- AA, KK, QQ, JJ (value)
- AKs, AKo (value)
- AQs (mostly value)
- A5s, A4s (blocker-based bluff squeezes)

**Mixed squeeze (sometimes 3-bet, sometimes call):**
- TT, 99 (squeeze or set-mine)
- AJs, ATs (squeeze or call)
- KQs (squeeze or call depending on exact spot)
- Suited Ax with blockers (A3s, A2s)

**Pure overcall (always call, never squeeze):**
- Small-medium suited connectors: 54s-87s
- Medium pairs: 66-88
- Suited gappers: 75s, 86s, 97s

**The principle:** Squeeze hands have BLOCKER value (Ax blocks AA/AKs in opener's range, Kx blocks KK) and play well in 3-bet pots if called. Overcall hands have NUTTED MULTIWAY potential and benefit from seeing a cheap flop with multiple opponents.

### Range Morphology Shift

When BB squeezes with strong suited broadways (AKs, AQs, KQs, AJs), these hands are REMOVED from the calling range. This means:

> "BB switches to an almost purely linear 3-bet strategy [with a caller]. Suited Broadways become a pure 3-bet, as well as TT-JJ, while many lower-EV hands move from a mixed to a pure strategy (i.e., call)."

This creates an important downstream effect: BB's CALLING range in a multiway pot is capped and nutted-hand-oriented, lacking strong top-pair hands.

---

## 6. BTN/CO Cold Calling with Callers Behind

### BTN vs HJ Open (Standard, No Callers)

- BTN defends ~30-35% (call ~20-25%, 3-bet ~10-12%)
- Wide cold-calling range because of guaranteed position and no squeeze risk from only the blinds

### BTN vs HJ Open When CO Has Already Called

- BTN cold-call range NARROWS because:
  1. Pot is going multiway (reduced EQR)
  2. Blinds behind can still squeeze
  3. Must beat 3 opponents instead of 2

### CO vs HJ Open (Standard)

- CO defends ~20-25% (call ~12-16%, 3-bet ~8-10%)
- Narrower than BTN because BTN and blinds are still behind

### Solver Principle for Non-Blind Cold Callers

> "Solvers recommend using 3-bet-or-fold strategies from every position except the Big Blind in non-ante, deep-stack games."

This means: from CO, BTN (non-blind positions), the solver often prefers 3-bet or fold. Cold calling is permitted but minimized because:
- Calling creates squeeze vulnerability
- Calling caps your range
- A weaker calling range can be attacked by squeezes

When there ARE callers ahead, the non-blind player behind should further tighten their cold-call range and increase 3-bet frequency (or fold more).

---

## 7. Multiple Callers: The Extreme Case

### HJ Opens, CO Calls, BTN Calls -- BB to Act

**Pot odds:**
- Pot: 0.5 + 1.0 + 2.5 + 2.5 + 2.5 = 9.0bb
- BB calls 1.5bb to win 9.0bb
- Pot odds: 1.5/10.5 = **14.3% equity needed** (raw)

**But 4-way EQR is brutal:**
- OOP 4-way EQR: ~45-55% for most hands
- Many hands that have 25% raw equity (which looks like enough given 14.3% needed) will only realize ~12-14% effective equity
- The math roughly cancels: great odds but terrible realization

**Result:** BB defends roughly the same or slightly tighter than vs a single caller, NOT significantly wider.

### BB Strategy with Multiple Callers

1. **Squeeze more aggressively:** With 9bb of dead money, squeezing becomes very profitable. All three callers have capped ranges. A squeeze to 12-13bb risks 12 to win 9, needing only ~57% fold frequency.

2. **Call with a narrow, nutted range:** Only suited connectors, suited aces, and medium pairs for set mining. Cut ALL weak offsuit hands.

3. **Fold everything marginal:** K9o, Q8o, J7o -- all folds despite the great pot odds.

---

## 8. Summary Table: How BB Strategy Shifts

| Factor | HU vs Opener | With 1 Caller | With 2+ Callers |
|--------|-------------|---------------|-----------------|
| Pot odds (raw equity needed) | ~27% | ~19% | ~14% |
| EQR multiplier (OOP) | ~0.75 | ~0.60 | ~0.50 |
| Effective equity needed | ~36% | ~32% | ~28% |
| BB total defend % | ~35-40% | ~30-37% | ~25-32% |
| BB calling % | ~27-32% | ~20-25% | ~16-20% |
| BB squeeze/3-bet % | ~8-9% | ~9-12% | ~10-13% |
| Range composition | Wide, mixed | Narrow, suited | Very narrow, nutted |
| Key hands added | Weak Kx, Qx, broadways | -- | -- |
| Key hands removed | -- | KTo, QTo, A8o-A2o, weak Kxs | Low pairs, weak suited |

---

## 9. Practical Implications for River Rats

### What This Means for Simplified Ranges

1. **Do NOT widen your BB calling range when someone has already called.** This is the most common population leak. The extra caller makes your marginal hands WORSE, not better.

2. **Do squeeze more often with strong hands and Ax blockers.** Dead money in the pot rewards aggression. With a caller, shift strong broadways (AQs, KQs, AJs) from call to 3-bet.

3. **Keep suited connectors and pairs in your calling range.** These are the hands that benefit from multiway action through implied odds and nutted potential.

4. **Fold all weak offsuit hands.** K9o, Q8o, J7o, A5o -- these are clear folds multiway despite pot odds that look tempting.

5. **From non-blind positions, prefer 3-bet or fold over cold calling when someone has already called.** Cold calling creates squeeze vulnerability and a capped range.

### The Simplified Heuristic

- **Heads-up vs open:** Defend wide, mix calls and 3-bets
- **With 1 caller:** Tighten calling range by ~5-8%, increase squeeze frequency by ~2-3%, shift to nutted/suited hands only for calls
- **With 2+ callers:** Tighten calling range by ~10-15%, increase squeeze frequency by ~3-5%, only call with hands that make the nuts

---

## 10. Key Sources

- [Overcalling From the BB - GTO Wizard](https://blog.gtowizard.com/overcalling-from-the-bb/)
- [How To Construct a Squeezing Range - GTO Wizard](https://blog.gtowizard.com/how-to-construct-a-squeezing-range/)
- [Responding to BB Squeezes - GTO Wizard](https://blog.gtowizard.com/responding-to-bb-squeezes/)
- [Introducing Multiway Preflop Solving - GTO Wizard](https://blog.gtowizard.com/introducing-multiway-preflop-solving/)
- [The Ultimate Guide to Preflop Multiway Pots (And Squeezing) - Upswing Poker](https://upswingpoker.com/multiway-pot-preflop-squeezing-leaks/)
- [Defending The Big Blind In Multi-Way Pots - PokerCoaching](https://pokercoaching.com/blog/defending-the-big-blind-multiway/)
- [The Secret to Playing Multiway Preflop - Raise Your Edge](https://www.raiseyouredge.com/multiway-preflop)
- [Preflop Range Morphology - GTO Wizard](https://blog.gtowizard.com/preflop-range-morphology/)
- [Equity Realization - GTO Wizard](https://blog.gtowizard.com/equity-realization/)
- [10 Tips for Multiway Pots in Poker - GTO Wizard](https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/)
- [Big Blind Strategy 101 - Upswing Poker](https://upswingpoker.com/big-blind-defend-strategy-mtt-vs-cash/)

---

## Confidence Notes

- The **directional findings** are high confidence -- sourced directly from GTO Wizard solver outputs and confirmed across multiple strategy sites.
- The **exact percentages** are moderate confidence -- solver outputs vary by rake structure, stack depth, and exact open sizing. The numbers presented are best estimates from aggregating multiple sources for 100bb, 6-max, standard rake.
- The **hand-specific recommendations** are high confidence for the general pattern (suited connectors stay, offsuit broadways go) but individual hands will have mixed frequencies in solvers rather than pure actions.
