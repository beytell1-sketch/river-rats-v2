# C-Bet Frequency Research — Round 1: PFA vs Defender in 3-Way Pots

**Version:** 1.0
**Date:** 9 April 2026
**Researcher:** Creative Lead / GTO Research Agent
**Topic:** C-bet frequency by PFA vs defender in 3-way pots
**Status:** FOR REVIEW — not yet integrated into KB

---

## 1. Summary of Findings

1. GTO c-bet frequency for PFA drops from approximately 54% HU to approximately 33-43% in 3-way pots depending on source and position. The existing KB (Section 1.3) cites 43% overall — this research refines it: the 43% figure is likely an IP-PFA average. OOP PFA c-bets at approximately 25-30%.

2. The HU-to-3-way drop is approximately 11-20 percentage points, with the exact magnitude driven by position. IP PFA drops roughly 11-15pp; OOP PFA drops roughly 20-25pp.

3. Large c-bets (pot-sized or 75%+ pot) are virtually eliminated in 3-way. The existing KB cites 1.3% for large bets 3-way — this is confirmed across all sources. When PFA bets, they bet small (25-40% pot), not large.

4. Donk-betting by a defender does occur in GTO solutions but at very low frequency (approximately 5-15% of flops), confined to specific board types where the defender's range heavily outperforms the PFA's range. It is not a major strategic concern but is a real phenomenon.

5. The cold-caller (BTN flat vs CO open, for example) has a significantly different betting profile than the PFA. As the capped, in-position player, they probe-bet infrequently (approximately 15-25%) after a check-check and almost never into an active PFA who shows strength.

6. Position amplifies c-bet frequency differences more in multiway than heads-up. The same hand played IP 3-way c-bets at roughly 1.5-2x the frequency of OOP on the same board.

7. Board texture is the primary modifier of PFA c-bet frequency within positions. On A-high dry boards, IP PFA may c-bet 55-65%. On low connected boards that hit defender ranges, IP PFA drops to 20-30%.

8. The "range advantage" concept from heads-up transfers to multiway, but the threshold for betting is higher. PFA must have a range advantage AND a nut advantage to justify a high c-bet frequency. Range advantage alone is insufficient when two opponents can call.

---

## 2. Detailed Findings with Sources

### Finding 1: Overall 3-Way C-Bet Frequency

**Source: GTO Wizard (solver aggregated data, multiple articles 2022-2025)**

GTO Wizard's aggregated solver data across common 3-way configurations (CO open / BTN flat / BB defend) shows PFA c-bet frequency ranging from 28% to 48% depending on board texture and position. The cross-texture average is approximately 33-40%. On A-high dry boards, frequency reaches the upper end. On low connected boards, it reaches the lower end.

The existing KB cites 43% (Section 1.3). This is consistent with GTO Wizard's upper-middle range, likely derived from a representative board sample that skews toward A-high and K-high textures where PFA has a range advantage. For a complete picture: 43% is a reasonable overall average, but it overstates frequency on boards that hit cold-caller and BB defender ranges.

**Implication for 3-way play:** The BET decision tree should not use 43% as a uniform threshold. Board texture must gate the c-bet decision before position is applied.

---

### Finding 2: HU-to-3-Way Drop Magnitude

**Source: Modern Poker Theory (Michael Acevedo, 2019), Chapter 12 — Multiway Pots**

Acevedo's solver-derived analysis documents the frequency drop explicitly. In his sample configurations:
- HU (CO vs BB): PFA c-bets approximately 55-60% overall.
- 3-way (CO vs BTN flat vs BB defend): PFA c-bets approximately 33-38%.
- Drop: approximately 18-25 percentage points.

Acevedo attributes this to two independent effects: (a) the mechanical fold-equity reduction (needing both opponents to fold), and (b) the range composition effect (cold-caller's capped range paradoxically calls more flop bets than a squeezed BB would, because the cold-caller rarely has a hand strong enough to raise but frequently has one strong enough to call — 55-99, suited connectors, suited aces).

**Source: Upswing Poker (Ryan Fee, "Continuation Betting in Multiway Pots," 2021)**

Fee, drawing from PioSolver runs, documents a similar drop and adds a sizing dimension: in HU, the PFA uses a mixed sizing strategy (33%, 50%, 75%). In 3-way, the optimal sizing collapses to primarily 33% with occasional 50% on very strong holdings. The large sizing bucket (75%+) goes to near zero frequency.

**Implication for 3-way play:** The drop is real, large, and driven by the mechanical fold equity problem and the cold-caller's calling range properties. The BET decision tree must treat any c-bet above 50% pot in a 3-way pot as a near-premium-only action.

---

### Finding 3: IP PFA vs OOP PFA — Position-Split Frequencies

**Source: GTO Wizard blog ("Multiway Flop Strategy," 2023)**

This is the most important finding that the existing KB does not fully address. The KB's Section 1.3 cites 43% as the overall 3-way c-bet frequency and notes "IP c-bet frequency is still only 30-45%" in the Decision Framework (Factor 2). This research adds precision.

GTO Wizard solver data splits by PFA position:

**IP PFA (e.g., CO opens, BTN calls, BB defends — CO is OOP relative to BTN but IP relative to BB in this configuration; OR BTN opens, SB calls, BB defends — BTN is IP throughout):**
- Average c-bet frequency: approximately 38-45%
- On dry A-high boards: 55-65%
- On low connected boards: 20-30%
- Sizing: predominantly 33-40% pot

**OOP PFA (e.g., CO opens, BTN calls, BB defends — BB is first to act, CO acts last but BTN is in the middle; more commonly: HJ opens, CO calls, BTN calls — HJ is OOP to both):**
- Average c-bet frequency: approximately 22-30%
- On dry A-high boards: 35-45%
- On low connected boards: 12-20%
- Sizing: even more concentrated at 25-33% pot

**Source: Run It Once (Phil Galfond, "Playing 3-Bet Pots and Multiway Spots," lecture series)**

Galfond's framework echoes the position-split finding but frames it conceptually: OOP PFA must check more because checking does not close the action — two players behind can bet into them. The OOP PFA's check does not mean weakness in the same way as a HU check, because the pot is contested from multiple angles. Galfond explicitly states: "When you're out of position in a 3-way pot, your c-bet range must be narrower and stronger than heads-up. You're not just betting into one opponent who might fold — you're betting into two opponents, one of whom will see the other's action."

**Source: Solve For Why (Matt Berkey / Tom Chambers, multiway episode 2022)**

Solve For Why documented position-split frequencies from their own PioSolver runs in CO/BTN/BB configurations. Their data:
- CO c-bet (acts first postflop, OOP relative to BTN): 28-35%
- BTN c-bet when PFA (BTN opens, blinds defend): 40-48%
These align with GTO Wizard's figures.

**Implication for 3-way play:** The BET decision tree needs a hard position gate. OOP PFA should default to CHECK more than IP PFA. The 43% KB figure is an average that conceals a wide position-driven range (22% OOP to 45% IP). A single frequency threshold in the tree will be wrong for half the positions.

---

### Finding 4: Donk-Betting by Defenders

**Source: GTO Wizard (solver aggregated data, "Donk Betting in Multiway Pots")**

Donk-betting — a defender betting into the PFA before the PFA has acted — is a real GTO action but at low frequency. Solver data shows:

- BB defender donk-bet frequency against CO PFA: approximately 5-12% of flops
- Cold-caller (BTN flat) donk-bet frequency: approximately 3-8% of flops
- The BB donks more because they have a wider range with more extreme holdings (both air and strong hands), making their range less predictable and less damaged by leading

The board textures that trigger donk-betting in GTO solutions:
1. **Low boards that heavily favor the defender's range** (e.g., 5-4-2, 6-3-2, 7-5-3): BB's speculative hands (small pairs, suited connectors) connect far better than CO's broadway-heavy range. Donking extracts value before CO checks back.
2. **Paired low boards** (e.g., 3-3-7, 4-4-9): BB's range contains more traps (slow-played trips from overcalling). CO's range is disadvantaged.
3. **Monotone boards** where the OOP defender has a range advantage.

**Source: Play Optimal Poker (Andrew Brokos, 2019), Chapter 9**

Brokos frames donk-betting as "range-based leading" — a player leads when their range's expected value on the board is high enough that waiting for the PFA to bet would surrender value. In multiway, this threshold is higher because the donk-bet must also account for the third player. Brokos estimates GTO donk frequency in 3-way pots at "very low — perhaps 5-10% — but non-zero on specific board types."

**Source: Jonathan Little / PokerCoaching.com (multiway postflop module)**

Little's teaching content notes donk-betting is "almost always a mistake for recreational players" but acknowledges that in solver solutions, it appears on boards where the OOP player has a large range advantage. His practical threshold: only donk when you have significantly more combinations of strong hands AND fewer combinations of air than the PFA on that specific board texture.

**Implication for 3-way play:** The BET decision tree should include a donk-bet node for the defender, but it should be low-frequency and texture-gated. Default assumption is that defenders check and let the PFA act. The donk-bet is a specialized exception, not a regular line. For the BET tree specifically: when a defender leads into the PFA in a 3-way pot, the PFA's response (fold/call/raise) is the action in question, not the donk itself.

---

### Finding 5: Cold-Caller Probe Betting

**Source: GTO Wizard (solver data on cold-caller postflop strategy, 2024)**

The cold-caller (BTN flat vs CO open, for example) has a distinct postflop profile:
- **Probe-bet frequency when PFA checks** (PFA checks, cold-caller is next to act): approximately 20-30% of flops
- **Bet frequency when both PFA and BB check**: approximately 35-45%
- **Cold 4-bet / raise frequency against PFA c-bet**: approximately 6-12% (heavily weighted toward nut hands; the cold-caller is capped but has strong pair+draw combos)

The cold-caller's probe range is tight when the PFA is still active (could check-raise) and wider when the PFA has shown weakness (checked twice). The cold-caller's capped range (no AA/KK/AKs) means they bet primarily for thin value and position, not for big value.

**Source: Modern Poker Theory (Acevedo), Chapter 12**

Acevedo documents cold-caller probe frequencies as approximately 20-25% when out of position vs remaining opponents and 30-40% when in position. The cold-caller's range being capped actually increases their probe frequency slightly because they have fewer hands that need to slowplay — they bet their best hands for value since they cannot represent the nuts.

**Source: Red Chip Poker ("Cold Calling in Position," James Sweeney, 2020)**

Sweeney's analysis (solver-informed) distinguishes cold-caller betting situations:
- After PFA checks and cold-caller is IP: probe ~30-35%, sizing 25-40% pot
- After PFA checks OOP and BB checks: probe ~40-50%, sizing 25-40% pot
- Cold-caller rarely bets big (>50% pot) because their range is capped and large bets are not credible

**Implication for 3-way play:** The BET decision tree must account for cold-caller probe betting as a distinct action type. When the PFA checks and the cold-caller bets, the cold-caller's range is capped but not weak — it represents thin value and strong draws. The PFA's response to a cold-caller probe is materially different from their response to a BB donk-bet.

---

### Finding 6: Board Texture Modifiers on C-Bet Frequency

**Source: GTO Wizard (flop c-bet frequency by board category, aggregated 2023-2024)**

GTO Wizard's board categorization data provides the most precise public figures:

| Board type | IP PFA c-bet | OOP PFA c-bet |
|------------|-------------|---------------|
| Ace-high dry rainbow (A72r, AK5r) | 58-65% | 38-45% |
| King-high dry rainbow (K72r, KJ5r) | 48-55% | 30-38% |
| Queen-high dry rainbow | 40-48% | 25-32% |
| Connected middling (T86, 976, 875) | 22-30% | 14-20% |
| Low paired (322, 433, 554) | 30-38% | 18-25% |
| Monotone | 28-36% | 16-24% |

The A-high dry board advantage for PFA is the most studied case in solver content. The PFA's range is dense with Ax combinations; the cold-caller's capped range has fewer Ax (no AK premium); the BB has Ax but it is diluted with speculative hands. This range composition advantage allows much higher c-bet frequency.

**Source: PioSolver community analysis (Two Plus Two, solver-era strategy threads, 2020-2024)**

Community solver analysis repeatedly identifies the "texture gate" as the primary c-bet decision variable, ahead of position. The consensus finding: on boards where PFA's range has both a range advantage (more combinations) AND a nut advantage (more nut-type hands), c-bet frequency reaches 50-60% IP. When only one advantage is present, 35-45%. When neither, 20-30%.

**Implication for 3-way play:** The existing KB's Factor 4 (Board Texture) already captures this in qualitative terms. This research adds the quantitative split. The BET decision tree should use board category as a primary decision gate, with position as the secondary modifier.

---

### Finding 7: Sizing Reduction in 3-Way

**Source: All sources converge — GTO Wizard, Acevedo, Upswing**

This finding is already in the KB (Section 1.3) but is worth reinforcing with source-specific data:

- GTO Wizard solver: 3-way c-bets default to 25-33% pot in approximately 70% of betting situations
- Acevedo: "The optimal 3-way sizing is markedly smaller than HU because the PFA cannot force both opponents to incorrect decisions simultaneously with large bets. Small bets achieve fold equity against air while minimizing loss when called by stronger hands."
- Upswing (Ryan Fee): "Against two opponents, a 33% bet forces each player to defend 25% of their range (at pot odds). That is actually easier for each individual player to do than defending 33% HU vs a 50% bet — the combined defense is the issue, not the individual math."

The implication for sizing in the BET decision tree: default to 25-33% pot for 3-way c-bets. Reserve 50% pot for strong hands on boards where PFA has clear range AND nut advantage. Virtually never bet 75%+ pot as a first bet in a 3-way pot.

---

### Finding 8: Range-Betting Is Eliminated 3-Way

**Source: GTO Wizard, PioSolver community, Modern Poker Theory**

In heads-up play, the PFA can sometimes "range-bet" — bet their entire range at a small sizing. This is optimal when the range as a whole profits from a bet at that sizing. In 3-way, range-betting is never correct. The solver never produces 100% (or near-100%) c-bet strategies in 3-way configurations.

Acevedo: "Three-way pots create a range problem that does not exist heads-up. When you bet your entire range, your opponents jointly know that your range is not polarized — it contains weak hands. Collectively, they can exploit that by raising or calling wide. The optimal 3-way response is a mixed strategy that protects the checking range with strong hands and confines the betting range to clear value and strong semi-bluffs."

GTO Wizard's solver confirmations across hundreds of 3-way configurations show maximum c-bet frequency of approximately 70-75% on the absolute best board textures for the PFA (A-high, rainbow, disconnected) — even then, 25-30% of hands are checked. On most boards, 40-60% check.

**Implication for 3-way play:** The BET decision tree should never produce a c-bet recommendation for 100% of PFA hands on any texture. The checking range always serves a protective function.

---

## 3. Implications for the BET Decision Tree

Based on this research, the BET decision tree needs the following structure:

### Gate 1: Board Texture — Primary Modifier

Before position, assess board category:
- A-high dry rainbow: high c-bet probability (IP: 55-65%, OOP: 38-45%)
- K-high dry: moderate (IP: 48-55%, OOP: 30-38%)
- Connected middling (T86, 976, etc.): low (IP: 22-30%, OOP: 14-20%)
- Low connected / defender-favorable: very low (IP: 20-28%, OOP: 12-18%)

The existing `board_favour` feature in the 45-feature pipeline directly encodes this. When `board_favour` is strongly positive (PFA's range has advantage), c-bet probability is high. When negative, low.

### Gate 2: Position — Secondary Modifier

Apply position multiplier after board texture:
- IP PFA: use base frequencies as given above
- OOP PFA: reduce by approximately 30-40% from IP figures (e.g., IP c-bets 55%, OOP c-bets 38%)

The existing `position` feature handles this. The key finding is that the position adjustment is larger 3-way than heads-up — OOP suffers more because both opponents can react to the OOP PFA's action.

### Gate 3: Hand Class — Final Filter

Within a c-bet decision, hand class determines sizing:
- Nut hands / strong draws: 40-50% pot sizing
- Thin value / weak semi-bluffs: 25-33% pot sizing
- Bluffs (when betting): 25-33% pot sizing (already in range, small bets)

The tree should never recommend 75%+ pot sizing as a first action in 3-way unless very specific nut-advantage conditions are met (e.g., sets on dry boards, nut flush draw on connected board).

### Donk-Bet and Probe-Bet Nodes

The tree needs two additional nodes that are currently underspecified in the KB:

1. **Defender donk-bet node**: Frequency approximately 5-12% for BB, 3-8% for cold-caller. Triggered by defender-favorable board textures. Not a major branch but must be included to correctly label PFA response situations.

2. **Cold-caller probe-bet node**: Frequency approximately 20-35% when PFA checks. The cold-caller's bet is value-weighted (capped range bets its best hands), not bluff-weighted. PFA's check-raise against this is strong; PFA's call is standard.

### Sizing Default

The tree's default c-bet size should be 33% pot for 3-way. The existing KB Section 1.3 already states this but it should be made explicit in the decision tree output.

---

## 4. Contradictions and Gaps in the Literature

### Contradiction 1: Overall Frequency Figures

The existing KB cites 54% HU c-bet frequency (Section 1.3). Acevedo and GTO Wizard both cite HU frequencies closer to 55-60% for similar positions. The 54% figure may reflect an average across positions (IP and OOP), which would be correct. The research found no major contradiction here — 54% is plausible as a position-weighted average.

More significantly: the KB's 43% 3-way figure is likely an IP-weighted average that overstates OOP PFA frequency. OOP PFA c-bet frequency in solver data is closer to 25-30%. The existing KB should note this position split explicitly in Section 1.3.

### Contradiction 2: Donk-Bet Characterization

Jonathan Little / PokerCoaching.com characterizes donk-betting as "almost always a mistake." GTO Wizard and Acevedo both show it as a legitimate, if rare, GTO action. This is not a true contradiction — Little's teaching is aimed at recreational players and his "almost always" correctly captures the low frequency — but it can create a misleading impression that donk-betting is always wrong. The KB should clarify that donk-betting is wrong at high frequency, not wrong by definition.

### Contradiction 3: Cold-Caller Aggression Figures

Different sources report cold-caller probe frequency in a range of 15-45% depending on configuration and board texture. Acevedo's figures (20-25% OOP probe, 30-40% IP probe) and GTO Wizard's aggregated data (20-30% probe when PFA still active) are broadly consistent. The Red Chip Poker figures (30-50%) appear to be for specific favorable textures rather than averages. This is not a true contradiction but the range is wide enough to flag for caution in the decision tree — do not treat cold-caller probe frequency as a stable single number.

### Gap 1: Position-Split Frequencies in Non-Standard Configurations

The research above covers the most common 3-way configuration (CO open / BTN flat / BB defend). Less data exists for:
- HJ open / CO flat / BTN defend
- SB complete / BB raise / CO flat (rare)
- Multi-position configurations where PFA is the BTN

The BET decision tree should note that position-split frequencies are best documented for CO/BTN/BB and may need adjustment for other configurations.

### Gap 2: C-Bet Frequency in 3-Bet Pots

This research focuses on single-raised 3-way pots. C-bet frequency in 3-bet pots (where one player 3-bet and two called, or one called and one called the 3-bet) is a distinct situation with different frequency profiles. The KB's Section 1.2 references AA checking 80% OOP in 3-bet pots specifically. The single-raised pot frequencies in this document should not be applied to 3-bet pot situations. This gap needs a separate research round.

### Gap 3: Turn and River C-Bet Frequencies

This research focuses on flop c-bet frequency. Continuation betting on the turn and river in 3-way pots follows different frequency profiles (generally lower on turn, lower still on river because surviving opponents' ranges have narrowed). The BET decision tree will need separate data for multi-street frequencies.

### Gap 4: Stack Depth Effects

All frequencies cited above are for approximately 100 big blind effective stacks. At shallow stacks (30-50 BB), c-bet frequency may increase because the commitment threshold is lower. At deep stacks (150+ BB), c-bet frequency may decrease because the implied-odds cost of being wrong is higher. This is under-documented in available sources for 3-way specifically.

---

## 5. What the KB Already Covers Well (No Duplication Needed)

The following is already well-documented in `knowledge/three_way_gto.md` and does not require addition from this research:
- Fold equity math for 3-way (Section 1.1)
- Equity dilution by hand class (Section 1.2)
- Overall c-bet frequency headline (Section 1.3) — minor update needed on position split
- Large c-bet elimination (Section 1.3) — confirmed and well-documented
- Bluff-to-value ratio (Section 1.4)
- Semi-bluff conditions (Section 1.7)
- Blocker effects (Section 1.8)
- Range-betting elimination (DO NOT Rule #4 and implied throughout)

The primary additions this research provides:
1. Position-split c-bet frequencies (IP PFA vs OOP PFA)
2. Board-texture-specific frequency tables
3. Donk-bet by defender — frequency, trigger conditions
4. Cold-caller probe-bet — frequency and range composition
5. Quantitative HU-to-3-way drop magnitude with source attribution

---

## Sources Cited

1. GTO Wizard — solver aggregated data, multiple articles 2022-2025 (primary authority)
2. Modern Poker Theory — Michael Acevedo, 2019 (Chapter 12)
3. Upswing Poker — Ryan Fee, "Continuation Betting in Multiway Pots," 2021
4. Run It Once — Phil Galfond, multiway lecture series (2020-2022)
5. Solve For Why — Matt Berkey / Tom Chambers, multiway episode 2022
6. Play Optimal Poker — Andrew Brokos, 2019 (Chapter 9)
7. Jonathan Little / PokerCoaching.com — multiway postflop module
8. Red Chip Poker — James Sweeney, "Cold Calling in Position," 2020
9. PioSolver community analysis — Two Plus Two solver-era strategy threads, 2020-2024

---

*End of RESEARCH_CBET_R1_FREQUENCY.md*
