# GTO Preflop Strategy: Small Blind (SB) in 6-Max Cash Games (100bb)

Research Date: 2026-04-06

## Executive Summary

The Small Blind is the most complex preflop position in poker. It is the only position
where the player has already invested chips (0.5bb), always acts first postflop, and
where GTO solvers sometimes recommend limping as part of an optimal strategy. The current
engine opens only 7% from SB, which is catastrophically tight. Solver-based GTO strategy
calls for the SB to play approximately 40-50% of hands when folded to (raise-or-fold at
most stakes), and to employ a 3-bet-or-fold strategy when facing opens from other positions.

---

## 1. SB RFI (Raise First In) -- Folded to SB

### Opening Percentage

Solver consensus across multiple sources:

| Source | SB RFI % | Strategy Type |
|--------|----------|---------------|
| MyPokerCoaching (100bb) | ~50% | Raise-or-fold |
| Upswing Poker | ~40-45% | Raise-or-fold |
| FreeBetRange (GTO Library) | ~47% | Raise-or-fold (simplified) |
| PokerCoaching.com | 81.6% | Raise + limp combined (MTT/high-stakes) |
| RangeConverter (exploitative) | ~62% | Raise + call combined |
| MonkerSolver (no-rake) | ~80-90% | Raise + limp mixed |
| Practical consensus (raked games) | 40-50% | Raise-or-fold only |

**Key finding: SB should open-raise approximately 40-50% of hands in raked cash games
at stakes below NL1000. The current engine's 7% is off by a factor of 6x.**

### Recommended Raise Size

- **3x BB** is the standard solver-recommended SB open size
- Rationale: BB has position and already has money committed, so larger sizing (3-4x)
  worsens their pot odds and compensates for SB's positional disadvantage
- Some solvers prefer 2.5x at higher stakes with lower rake

### Approximate SB RFI Range (Raise-or-Fold, ~45%)

**Always raise:**
- All pocket pairs: 22+
- All suited Aces: A2s-AKs
- Suited Kings: K2s-KQs
- Suited Queens: Q2s-QJs
- Suited Jacks: J5s-JTs
- Suited connectors/gappers: T7s+, 97s+, 86s+, 75s+, 64s+, 54s
- Offsuit broadways: ATo+, KTo+, QTo+, JTo
- Offsuit Aces: A2o-A9o (mixed, some pure raise some fold)
- Offsuit Kings: K9o+

**Fold:** Worst offsuit hands (72o-type trash), disconnected low cards

### The Limping Debate

**What solvers actually show:**
- In zero-rake or very low rake environments, solvers use a mixed strategy of
  raising ~40-50% and limping ~30-40%, totaling 70-90% of hands played
- The limp range typically includes small suited hands, weak suited connectors,
  and marginal offsuit hands that have some postflop playability but don't raise well
- Limping protects the SB's range by preventing BB from exploiting a pure raise-or-fold
  strategy (where a SB fold = free BB, and a SB raise = narrow predictable range)

**Why limping is NOT recommended in practice (below NL1000):**
1. **Rake** -- the rake in low/mid-stakes games destroys the EV of limped pots
2. **Complexity** -- implementing a correct mixed strategy requires knowing which
   hands to limp-raise, limp-call, limp-fold vs BB iso-raises
3. **Minimal gain** -- even at high stakes, the EV difference between a well-executed
   limp strategy and a simpler raise-or-fold strategy is tiny
4. **Exploit vulnerability** -- recreational players often limp too wide and fail
   to balance their limp-raise range

**Recommendation for the engine: Use raise-or-fold from SB. Do not implement limping.**

---

## 2. SB vs Opens from Other Positions (Facing a Raise)

### Core Principle: 3-Bet or Fold

GTO solvers overwhelmingly recommend a **3-bet-or-fold** strategy from the SB when
facing an open raise. Cold calling from SB is rarely correct because:

1. SB is always out of position postflop
2. Calling invites the BB to overcall or squeeze, creating a multiway pot where
   SB plays OOP with a capped range
3. The dead money in the pot (SB's 0.5bb + BB's 1bb) incentivizes aggression

### SB Cold Call Frequency (from Solver Data)

| Opener's Raise Size | SB Cold Call % |
|---------------------|----------------|
| BTN 3bb open | < 1% |
| BTN 2.5bb open | ~1-2% |
| BTN min-raise (2bb) | ~6% |
| CO 2.5bb open | < 1% |

**Important caveat:** Many solver runs show 0% cold calling from SB because the modeler
excluded the option from the game tree. When cold calling IS included, it appears at
very low frequencies. The hands that cold call (when it occurs) are typically medium
pocket pairs (77-99) and strong suited broadways (KQs, QJs) that play well multiway
but don't want to bloat the pot OOP.

**Recommendation for the engine: SB should almost never cold call. Use 3-bet-or-fold.**

### SB 3-Bet Ranges vs Different Openers

**SB vs UTG Open (~15% RFI):**
- SB 3-bet frequency: ~5-7% of all hands
- Range: QQ+, AKs, AKo (value), plus a few suited bluffs (A5s, A4s type)
- Mostly fold -- UTG's range is very strong

**SB vs MP/HJ Open (~18-22% RFI):**
- SB 3-bet frequency: ~7-9% of all hands
- Range: TT+, AQs+, AKo (value), plus suited Ax bluffs, some suited connectors

**SB vs CO Open (~25-28% RFI):**
- SB 3-bet frequency: ~10-13% of all hands
- Range: 88+, AJs+, AQo+ (value), plus wider bluff range including suited connectors,
  suited Ax, some suited Kings

**SB vs BTN Open (~40-48% RFI):**
- SB 3-bet frequency: ~15-20% of all hands
- Range: 77+, ATs+, AJo+, KQs (value), plus extensive bluff range including
  suited connectors (76s-T9s), suited Ax (A2s-A5s), suited Kx, some suited Qx
- This is the widest 3-bet range because BTN opens very wide

### 3-Bet Sizing from SB

- Standard: **3x the open raise** (e.g., vs 2.5bb open, 3-bet to 7.5-8bb)
- Out of position sizing should be larger (3x-4x) than in-position 3-bets (2.5x-3x)
- Purpose: Deny BB favorable odds, punish BTN's wide opens, build pot with strong hands

---

## 3. SB in Multiway Pots (Squeeze Situations)

### When CO Opens and BTN Calls (or Similar)

This is a **squeeze** spot. The SB should squeeze (3-bet) with a tighter, more
linear range than a standard 3-bet because:

1. There are two opponents to get through
2. The dead money is larger (open + call + blinds)
3. The callers have capped ranges (they didn't 3-bet)

### SB Squeeze Range (Approximate)

**vs CO open + BTN call:**
- Squeeze frequency: ~8-12% of hands
- Value: TT+, AQs+, AKo
- Bluffs: A5s-A2s, some suited connectors (prefer hands that block calling ranges)
- Suited Broadways: KQs, KJs sometimes squeeze (they perform well if called multiway)

**vs BTN open + BB has not acted:**
- This is a standard 3-bet spot, not a true squeeze
- See "SB vs BTN Open" above

### SB Overcall (Call after Open + Call)

- Very rare in GTO -- typically < 3-5% frequency
- When it occurs, hands are: medium pocket pairs (55-88), suited connectors with
  good implied odds, suited Aces
- Generally discouraged because SB plays OOP in a multiway pot

**Recommendation for the engine: Implement squeeze at ~8-12% in multiway spots.
Avoid overcalling.**

---

## 4. SB Defense Frequency Summary (All Scenarios)

| Scenario | Total Defend % | 3-Bet % | Cold Call % | Fold % |
|----------|---------------|---------|-------------|--------|
| Folded to SB (RFI) | 40-50% raise | N/A | N/A | 50-60% |
| vs UTG open | ~5-7% | ~5-7% | ~0% | ~93-95% |
| vs MP/HJ open | ~7-9% | ~7-9% | ~0% | ~91-93% |
| vs CO open | ~10-13% | ~10-13% | ~0-1% | ~87-90% |
| vs BTN open | ~15-20% | ~15-19% | ~0-1% | ~80-85% |
| vs CO open + BTN call | ~8-12% | ~8-12% | ~0-3% | ~88-92% |

---

## 5. Common Misconceptions Addressed

### "SB should never limp"
**Partially false.** Solvers DO limp from SB in zero/low-rake environments. However,
at typical online stakes (NL25-NL500), the rake makes limping -EV. A raise-or-fold
strategy is correct for practical purposes. At NL1000+ with low rake, a mixed
raise/limp strategy can extract marginal additional EV.

### "SB should only open tight because they're out of position"
**False.** SB is heads-up against one random hand (BB). The positional disadvantage
is offset by the favorable pot odds (only need to beat one player) and the dead money
already in the pot. SB should open WIDER than CO or HJ -- approximately 40-50% of hands.

### "SB should cold call with medium pairs vs late position opens"
**Mostly false.** Cold calling from SB is almost never correct in GTO. Medium pairs
should either 3-bet (as part of a polarized range) or fold. The risk of BB squeezing
and the positional disadvantage make flat calling very unattractive.

### "SB should play the same range regardless of who opened"
**False.** SB defense frequency varies dramatically by opener position:
- vs UTG: defend ~5-7%
- vs BTN: defend ~15-20%
This 3x difference reflects the much wider range of late-position openers.

---

## 6. Implementation Recommendations for Engine

### Priority Fixes

1. **SB RFI is critically broken at 7%.** Must increase to ~40-50%.
   - Raise to 3x BB
   - Include all pairs, all suited Aces, most suited broadways, many suited connectors,
     and most offsuit broadways

2. **SB vs opens should be 3-bet-or-fold**, not call-or-fold.
   - vs BTN: 3-bet ~15-20%, fold rest
   - vs CO: 3-bet ~10-13%, fold rest
   - vs EP: 3-bet ~5-7%, fold rest

3. **Add squeeze logic** for multiway pots.
   - When facing open + call(s), SB squeezes ~8-12%
   - Tighter, more linear range than heads-up 3-bet

4. **Do not implement limping** -- raise-or-fold is sufficient and correct for
   the engine's target use case.

5. **Cold calling should be near-zero** from SB in all spots.

### Sizing Guidelines

| Action | Size |
|--------|------|
| SB open raise | 3x BB (3bb) |
| SB 3-bet vs 2.5x open | ~8bb (3.2x open) |
| SB 3-bet vs 3x open | ~9-10bb (3-3.3x open) |
| SB squeeze vs open + call | ~10-12bb |

---

## Sources

- [FreeBetRange: 6-max Open Raise Charts](https://blog.freebetrange.com/article/preflop-charts-open-raise-in-6-max-poker-cash-games)
- [Upswing Poker: Small Blind Strategy](https://upswingpoker.com/small-blind-poker-strategy-tips/)
- [Upswing Poker: 6-Handed Poker Guide](https://upswingpoker.com/6-handed-max-poker-strategy/)
- [888poker: Debunking Small Blind Cold-Call Myths](https://www.888poker.com/magazine/debunking-small-blind-sb-myths)
- [GTO Wizard: Exploiting SB Preflop Mistakes](https://blog.gtowizard.com/heads-up-exploiting-sbs-preflop-mistakes/)
- [GTO Wizard: How to Construct a Squeezing Range](https://blog.gtowizard.com/how-to-construct-a-squeezing-range/)
- [GTO Wizard: Preflop Range Morphology](https://blog.gtowizard.com/preflop-range-morphology/)
- [MyPokerCoaching: Optimal Cash Game Opening Ranges 100bb](https://www.mypokercoaching.com/optimal-cash-game-opening-ranges-100bb/)
- [MyPokerCoaching: 3-Betting from the Blinds](https://www.mypokercoaching.com/optimal-strategy-for-3-betting-from-the-blinds-early-late-position/)
- [PokerCoaching: GTO Preflop Charts](https://pokercoaching.com/preflop-charts)
- [RangeConverter: 6-max 100bb Charts](https://rangeconverter.com/articles/poker-charts-6-max-100bb-no-limit-texas-holdem)
- [SplitSuit: Understanding 3-Bet Ranges](https://www.splitsuit.com/understanding-3-bet-ranges)
- [Upswing Poker: 3-Bet Strategy](https://upswingpoker.com/3-bet-strategy-aggressive-preflop/)
- [Upswing Poker: Multiway Pots and Squeezing](https://upswingpoker.com/multiway-pot-preflop-squeezing-leaks/)
- [GTOBase: 6-max Cash Library Overview](https://blog.gtobase.com/theory/overview-of-the-new-gto-poker-solutions-in-the-6-max-cash-library/)
- [Beasts of Poker: 6-Max Strategy](https://beastsofpoker.com/6-max-poker-strategy/)
- [Upswing Poker: SB Preflop Podcast](https://upswingpoker.com/podcast/ep16-small-blind-preflop/)
- [Total Online Poker: Limping in the Small Blind](https://www.totalonlinepoker.com/single-post/limping-in-the-small-blind)
