# Bluff Compression and Fold Equity in 3-Way Postflop Pots

**Research date:** 2026-04-06
**Scope:** Quantified, solver-backed findings on how bluffing strategy changes from heads-up (HU) to 3-way (MW) postflop pots.
**Method:** Web search of GTO Wizard blog, Upswing Poker, mypokercoaching, poker.pro, SplitSuit, and other strategy sources. All numbers attributed to sources below.

---

## 1. Fold Equity: The Multiplicative Problem

### The Core Math

In a HU pot, if Villain folds X% of the time, your fold equity is straightforward. In a 3-way pot, you need BOTH opponents to fold. The probabilities multiply:

- **HU:** P(fold equity) = P(A folds)
- **3-way:** P(fold equity) = P(A folds) x P(B folds)

**Example (pot-sized bet, alpha = 50%):**
- HU: Need opponent to fold 50% of the time.
- 3-way: If each folds 70%, total fold probability = 0.70 x 0.70 = 0.49 (49%). Barely meets the 50% breakeven threshold.
- If each folds only 60%, total = 0.60 x 0.60 = 0.36. Well below breakeven.

**Source:** mypokercoaching.com, "Playing Profitably in Multiway Pots -- Minimum Defense Frequency" (theoretical, derived from probability math). Also referenced in GTO Wizard "10 Tips for Multiway Pots."

### Key Quote

> "Multiway pots feature an absolutely terrible risk/reward ratio on pure bluffs. Your opponents can defend much tighter, even against very small bets, while still preventing you from profitably bluffing."
> -- GTO Wizard, "10 Tips for Multiway Pots in Poker" (https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/)

**Classification:** Solver-based (GTO Wizard references solver outputs throughout).

---

## 2. Minimum Defense Frequency (MDF) Per Player in 3-Way Pots

### HU Baseline

MDF = Pot / (Pot + Bet). For a pot-sized bet: MDF = 1/2 = 50%. Each defender must continue with at least 50% of their range HU.

Alpha (bluff breakeven) = Bet / (Pot + Bet). Alpha = 1 - MDF.

### 3-Way MDF: Shared Burden

In multiway pots, the defensive burden is shared among all remaining players. The math:

- **HU, pot-sized bet:** Single defender must continue 50% (fold no more than 50%).
- **3-way, pot-sized bet:** The two defenders collectively must ensure the bettor cannot profit from pure bluffs. Each player can fold ~70% and still meet the shared MDF: 0.70 x 0.70 = 0.49, which approximates the needed 50% total defense.

**Per-player defense frequency in 3-way (pot-sized bet): ~30% each** (compared to 50% HU).

**Source:** mypokercoaching.com, "Playing Profitably in Multiway Pots -- Minimum Defense Frequency" (https://www.mypokercoaching.com/playing-profitably-in-mutliway-pots-mdf/)

### Asymmetric Defense (Position Matters)

The MDF is NOT split equally. The player in the middle (sandwiched) must fold more because they face action behind:

> "The player stuck in the middle will have to fold more often, as they have another player left to act to worry about. Facing a bet from Player A (the bettor), Player B might fold 80%, and Player C might fold around 60%, which brings us to about 48% -- very close to the required MDF."
> -- mypokercoaching.com

So the per-player breakdown is approximately:
- **Sandwich player (IP behind them):** folds ~80% (defends ~20%)
- **Closing action player:** folds ~60% (defends ~40%)
- **Combined total fold frequency:** 0.80 x 0.60 = 0.48 (meeting the ~50% defense requirement)

**Classification:** Theoretical (derived from game theory principles, not direct solver output, but consistent with solver findings).

### MDF Table by Number of Defenders (Pot-Sized Bet)

| Defenders | Combined MDF | Per-Player Fold % (symmetric) | Per-Player Continue % |
|-----------|-------------|-------------------------------|----------------------|
| 1 (HU)    | 50%         | 50%                           | 50%                  |
| 2 (3-way) | 50%         | ~70%                          | ~30%                 |
| 3 (4-way) | 50%         | ~79%                          | ~21%                 |

**Note:** Symmetric assumption. Real solver outputs show asymmetric defense as described above.

**Source:** Derived from shared MDF principle described in mypokercoaching.com and GTO Wizard "MDF & Alpha" (https://blog.gtowizard.com/mdf-alpha/).

---

## 3. C-Bet Frequency: HU vs 3-Way

### HU C-Bet Baseline (Solver)

From GTO Wizard "Flop Heuristics: IP C-Betting in Cash Games" (https://blog.gtowizard.com/flop-heuristics-ip-c-betting-in-cash-games/):

In a 100bb deep NL500 6-max cash game (BTN vs BB, single-raised pot):
- **Pot-sized bet:** 17.5% of the time
- **Smaller downbet (~33% pot):** 36.9% of the time
- **Check back:** 45.7% of the time
- **Total betting frequency:** ~54.3%

**Classification:** Solver-based (GTO Wizard aggregate report).

### 3-Way C-Bet (Solver)

From GTO Wizard "Playing In Position Against Two Callers" (https://blog.gtowizard.com/playing-in-position-against-two-callers/):

When comparing HU to 3-way (LJ opens, two callers):
- **Checking frequency increased by +11% in the MW scenario** compared to HU against BB alone.
- **The large (pot-sized) c-bet dropped from 18% (HU) to 1.3% (3-way).**

> "The LJ has reduced their c-betting frequency and sizings in the MW solution. The large (pot-sized) c-bet that was used 18% of the time heads up is now all but gone, being used only 1.3% of the time."
> -- GTO Wizard, "Playing In Position Against Two Callers"

**Key takeaway:** Overall c-bet frequency drops ~11 percentage points. Large sizing nearly disappears (18% to 1.3%). Small sizing becomes the dominant bet when betting occurs.

**Classification:** Solver-based (GTO Wizard 3-way solver output).

### Why Sizing Shrinks

> "You should typically size down in multiway pots as your equity retention just plummets off a cliff as the collective defense facing large bets results in extremely strong ranges."
> -- GTO Wizard, "10 Tips for Multiway Pots in Poker"

> "Part of this reduced betting frequency is due to the reduced overall EV across flops when playing against two ranges, but part is also due to the lower polarity of the aggressor's range when facing two opponents."
> -- GTO Wizard, "Playing In Position Against Two Callers"

**Classification:** Solver-based interpretation.

---

## 4. Bluff-to-Value Ratio Compression

### HU Baseline (River, Pot-Sized Bet)

From GTO theory (SplitSuit, GTO Wizard "MDF & Alpha"):
- Pot-sized bet gives defender 2:1 odds, so defender gets 33% pot odds.
- Aggressor should bluff 33% of betting range (1 bluff for every 2 value bets).
- **HU bluff-to-value ratio: 1:2** (pot-sized bet on river).

For a 2/3-pot bet:
- Defender gets ~29% pot odds.
- Aggressor bluffs ~29% of betting range.
- **HU bluff-to-value ratio: roughly 1:2.5.**

**Source:** SplitSuit "Perfect GTO Bluffing" (https://www.splitsuit.com/perfect-gto-bluffing), GTO Wizard "MDF & Alpha" (https://blog.gtowizard.com/mdf-alpha/).

**Classification:** Theoretical (math-derived, universally accepted).

### 3-Way Bluff-to-Value Ratio (Derived)

No single source provides a clean "the 3-way bluff-to-value ratio is X:Y" number from a solver. However, the logic chain is clear:

1. In 3-way, each defender only needs to continue ~30% vs pot-sized bet (vs 50% HU).
2. Both defenders independently tighten, meaning only very strong hands continue.
3. If you bluff, you need both to fold. With each folding ~70%, you succeed only ~49% of the time.
4. Since you barely break even on pure bluffs (and often don't), the solver drastically reduces bluffs.

**Estimated 3-way bluff-to-value ratio: approximately 1:4 or lower** (compared to 1:2 HU for pot-sized bet).

This is consistent with the qualitative findings:

> "Multiway pots feature an absolutely terrible risk/reward ratio on pure bluffs."
> -- GTO Wizard

> "Your betting range should become much stronger. Pure bluffs are ineffective multiway -- you need stronger value bets, and stronger bluffs."
> -- GTO Wizard, "10 Tips for Multiway Pots in Poker"

**Classification:** Theoretical estimate derived from solver-consistent principles. No direct solver number found for exact 3-way B:V ratio on river.

---

## 5. Semibluff Profitability in 3-Way Pots

### HU Semibluff EV

Standard formula:
EV = (P_fold x Pot) + (P_call x [(P_improve x New_Pot) - Bet])

In HU, fold equity is the primary driver. A flush draw with ~35% equity and ~50% fold equity is typically a profitable semibluff.

### 3-Way Semibluff Changes

Two compounding effects hurt semibluff profitability in 3-way:

1. **Fold equity collapses:** You need BOTH opponents to fold. If each folds 50%, you only win the pot uncontested 25% of the time (vs 50% HU).
2. **Equity dilution:** Your draw equity is lower against two ranges. A flush draw has ~35% equity HU but only ~25-30% equity vs two opponents with random holdings.

> "In a 3-way pot when you only have 35-40% pot share, it is hard to justify betting often. We are bloating a pot that we will more often than not lose."
> -- GTO Wizard, "10 Tips for Multiway Pots in Poker"

> "When considering a semibluff in a multiway pot, give more consideration to your outs."
> -- GTO Wizard

**Key finding:** The solver response is to restrict semibluffs to hands with the best equity (nut flush draws, combo draws) and largely eliminate weak semibluffs (gutshots, backdoor draws only) that are standard HU.

**Classification:** Solver-informed (qualitative from GTO Wizard solver analysis, no exact frequency numbers found for semibluff-specific hands in 3-way).

---

## 6. Sizing Preferences in 3-Way Pots

### Small Bet Dominance

From multiple sources, the solver strongly prefers small bet sizing in MW pots:

> "Essentially no big betting is used on the flop when playing GTO [in multiway], and in theory, there should be a lot of small betting in multi-way pots."
> -- Phil Galfond (https://www.philgalfond.com/articles/mastering-multi-way-pots)

**Classification:** Solver-based (Galfond references solver outputs).

### Exception: Big-Bet Windows

From poker.pro "Multiway Muscle: Big-Bet Windows Revealed by GTO Wizard" (https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/):

Big bets re-emerge in specific MW spots:
- Front door flush completes on the turn
- Board pairs
- High-card static boards where the PFR holds a linear range edge (e.g., A-K-x rainbow)
- Low SPR situations

> "While 'always small' is a helpful starting point in multiway pots, it leaves money on the felt when nut edge, last action, and low SPR converge on high/paired or front-door textures -- in those windows, big bets are the most efficient way to extract value and deny realisation across two ranges at once."
> -- poker.pro

**Classification:** Solver-based (references GTO Wizard 3-way solver outputs).

---

## 7. Pot Share and Equity Distribution

From GTO Wizard "10 Tips for Multiway Pots in Poker":

> "When 3 players enter the pot, they each have an average of 33% equity."

This 33% average pot share (vs 50% HU) is the fundamental reason everything compresses:
- Less equity to protect means less reason to bet.
- Less reason to bet means fewer bluffs are viable.
- Fewer bluffs means the betting range is more value-heavy.

From Upswing Poker "4 Ways to Improve Your Results in Multi-Way Pots":

> "Ace-King's equity suffers nearly a 26 percentage point decrease against three opponents holding random hands."

This means even premium holdings lose significant equity MW, further compressing profitable betting ranges.

**Classification:** Theoretical (equity math).

---

## 8. Summary Table: HU vs 3-Way Key Metrics

| Metric | Heads-Up | 3-Way | Source Type |
|--------|----------|-------|-------------|
| Average pot share | 50% | 33% | Theoretical |
| MDF per defender (pot-sized bet) | 50% | ~30% (symmetric) | Theoretical |
| C-bet frequency (IP, aggregate) | ~54% | ~43% (est. -11pp) | Solver (GTO Wizard) |
| Large c-bet frequency (pot-sized) | ~18% | ~1.3% | Solver (GTO Wizard) |
| Bluff-to-value ratio (pot-sized, river) | 1:2 | ~1:4 (estimated) | Theoretical + solver-informed |
| Pure bluff profitability | Breakeven at 50% fold | Breakeven at ~70% fold per player | Theoretical |
| Preferred flop sizing | Mixed (33%-100% pot) | Small (25-33% pot), rarely large | Solver (multiple sources) |

---

## 9. Source Index

| # | URL | Key Finding | Type |
|---|-----|-------------|------|
| 1 | https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/ | MW pots have "terrible risk/reward on pure bluffs"; defense burden is shared; 33% avg pot share | Solver-based |
| 2 | https://blog.gtowizard.com/playing-in-position-against-two-callers/ | Pot-sized c-bet drops from 18% (HU) to 1.3% (3-way); checking frequency up +11% MW | Solver-based |
| 3 | https://blog.gtowizard.com/monkey-in-the-middle-3-way-pot-heuristics/ | Sandwich player must fold more; HU heuristics fail in MW | Solver-based |
| 4 | https://blog.gtowizard.com/mdf-alpha/ | MDF = Pot/(Pot+Bet); Alpha = 1 - MDF | Theoretical |
| 5 | https://www.mypokercoaching.com/playing-profitably-in-mutliway-pots-mdf/ | 3-way MDF: each player folds ~70% (0.7x0.7=0.49); asymmetric: sandwich folds 80%, closer folds 60% | Theoretical |
| 6 | https://blog.gtowizard.com/flop-heuristics-ip-c-betting-in-cash-games/ | HU aggregate: pot-sized 17.5%, downbet 36.9%, check 45.7% | Solver-based |
| 7 | https://www.splitsuit.com/perfect-gto-bluffing | Bluff frequency = pot odds offered to defender; pot-sized = 33% bluffs | Theoretical |
| 8 | https://www.philgalfond.com/articles/mastering-multi-way-pots | "Essentially no big betting on the flop" in MW; small bets dominate | Solver-based |
| 9 | https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/ | Big-bet exceptions: front-door completions, paired boards, high-card textures with nut edge | Solver-based |
| 10 | https://upswingpoker.com/multiway-pots-flop-bet-strategy/ | Tighten value range MW; shrink bluffing range; lower aggression frequency | Solver-informed |
| 11 | https://blog.gtowizard.com/probing-out-of-position-in-3-way-pots/ | OOP probing changes in 3-way (article exists, specific numbers behind paywall) | Solver-based |
| 12 | https://blog.gtowizard.com/gto_wizard_ai_3_way_benchmarks/ | GTO Wizard AI 3-way solver benchmarks available | Solver-based |
| 13 | https://pokerenergy.net/edu/item/3way-review | Simple 3-Way: Nash calculator for multiway pots | Tool reference |

---

## 10. Gaps and Contradictions

### Gaps (data not found in public sources)
- **Exact 3-way river bluff-to-value ratio from a solver.** The 1:4 estimate is derived from theory, not a directly quoted solver output. GTO Wizard likely has this data but it sits behind their tool, not in public blog posts.
- **Hand-class-level betting frequencies in 3-way** (e.g., "top pair bets X%, middle pair bets Y%"). These exist in GTO Wizard's study mode but are not published in aggregate form.
- **MonkerSolver-specific 3-way data.** MonkerSolver can run 3-way sims but they are computationally expensive. No public MonkerSolver 3-way frequency tables were found.
- **Exact semibluff EV comparison** (same hand, HU vs 3-way, with numbers). No source provides a side-by-side EV calculation.

### Contradictions
- **No material contradictions found between sources.** All sources agree on the direction: fewer bluffs, smaller sizing, tighter value ranges, shared MDF burden. The only variation is in the exact per-player MDF split (symmetric vs asymmetric), which is not a contradiction but a modeling choice.
- **Phil Galfond's "essentially no big betting"** might appear to conflict with the poker.pro "big-bet windows" article, but the latter explicitly frames big bets as rare exceptions to the small-bet default, so these are complementary rather than contradictory.

---

## 11. Key Takeaways for River Rats Curriculum

The quantified compression from HU to 3-way:

1. **Fold equity halves** (roughly). Need ~70% fold per player instead of ~50% from one player.
2. **C-bet frequency drops ~11 percentage points** (solver). Large sizing nearly vanishes (18% to 1.3%).
3. **Bluff-to-value ratio compresses from ~1:2 to ~1:4** (estimated). Far fewer bluffs are viable.
4. **MDF per player drops from 50% to ~30%** (pot-sized bet). Each defender can be much tighter.
5. **Small sizing dominates** with rare big-bet exceptions on specific textures.
6. **Semibluffs require stronger draws** -- gutshots and weak backdoors drop out; nut draws remain.
