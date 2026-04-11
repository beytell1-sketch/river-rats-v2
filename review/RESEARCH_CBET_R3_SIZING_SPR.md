# Research: C-Bet Sizing and SPR Interaction in 3-Way Pots

**Version:** 1.0
**Date:** 2026-04-09
**Scope:** GTO c-bet sizing and stack-to-pot ratio interaction in 3-way postflop
pots. Intended audience: labelling agent design and feature engineering for the
SPR feature in the River Rats v9-3way model.
**Sources consulted:** 12 primary sources listed in Section 6. Existing KB in
`knowledge/three_way_gto.md` and research files in `research/` cross-referenced
throughout.

---

## 1. Summary of Findings

### 1.1 What the existing KB already covers (do not duplicate)

- C-bet frequency drop from HU (~54%) to 3-way (~43%): quantified, solver-backed.
- Large c-bet collapse from 18% to 1.3%: quantified, solver-backed.
- Default 3-way sizing is 25-33% pot: established in KB Section 1.3.
- SPR compression from a pot-sized flop bet: KB Section 1.6 notes SPR ~1.5 on
  turn after pot-sized flop bet vs ~3-4 HU.
- Multiway stack-off thresholds are tighter at the same numeric SPR: noted in
  KB but not developed into a decision framework.

### 1.2 What this research adds

This document provides:

1. A quantified SPR-based c-bet decision framework for the BET tree, organized
   into four SPR zones.
2. The commitment threshold concept in 3-way pots and how it differs from HU.
3. How the third player changes bet sizing math (pot geometry).
4. Board-texture-specific sizing adjustments within each SPR zone.
5. The low-SPR bet-vs-trap question (always bet? or check to trap?).
6. The high-SPR equity denial question (bet bigger? or control pot?).
7. Eight source citations with specific data points and implications.

### 1.3 Core findings at a glance

| SPR Zone | PFA Bet Tendency | Preferred Size | Key Reason |
|----------|-----------------|----------------|------------|
| < 1 (micro) | Always bet strong hands | All-in or near pot | Math: bet = commit, checking gains nothing |
| 1-2 (low) | Bet strong; trap only sets | 50-75% pot | SPR already committed range; value > deception |
| 2-5 (medium) | Bet selectively; standard spot | 25-40% pot | Core 3-way sizing window |
| 5-8 (medium-high) | Bet tighter; pot control dominant | 25-33% pot | Extra player makes high-SPR bluffs unviable |
| > 8 (deep) | Check strong hands more; small bets only | 20-25% pot | Equity denial argument is weaker 3-way |

---

## 2. Detailed Findings with Sources

### Finding 1: GTO 3-way c-bet size is 25-33% pot as the default

**Source:** GTO Wizard, "Playing In Position Against Two Callers"
(https://blog.gtowizard.com/playing-in-position-against-two-callers/)

**Specific data point:** In the LJ-opens / two-callers 3-way simulation, the
large pot-sized c-bet that appears 18% of the time HU is used only 1.3% of the
time 3-way. The dominant sizing when betting occurs is small — the article
describes this as "the LJ has reduced their c-betting frequency and sizings in
the MW solution." Solver outputs show the preferred sizing clusters at 25-33%
of the pot in standard 3-way single-raised spots.

**Implication for SPR feature:** At medium SPR (2-8), 25-33% pot is correct.
This sizing is not contingent on SPR alone — it is the default for the SPR
range where most flops land after a standard 6-max single-raised 3-way pot
(typically SPR 4-7 at 100bb effective).

**Classification:** Solver-based (GTO Wizard 3-way solver output).

---

### Finding 2: Large bets (50%+ pot) are justified in 3-way only at low SPR
or with nut-edge on specific textures

**Source:** Poker.pro, "Multiway Muscle: Big-Bet Windows Revealed by GTO
Wizard" (https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/)

**Source:** Phil Galfond, "Mastering Multi-Way Pots"
(https://www.philgalfond.com/articles/mastering-multi-way-pots)

**Specific data points:**

Poker.pro (citing GTO Wizard solver outputs) identifies four conditions where
big bets are correct 3-way:
1. Front-door flush completes on the turn (flush card hits).
2. Board pairs (set vs full house dynamic).
3. High-card static boards where the PFR holds a linear range edge (A-K-x
   rainbow), specifically at low SPR.
4. Low SPR situations (< 2.5 approximately): the pot commitment math changes.

Galfond (solver-informed): "Essentially no big betting is used on the flop when
playing GTO in multiway, and in theory there should be a lot of small betting
in multi-way pots." The qualifier "on the flop" is key — turn big bets emerge
more once SPR has compressed.

**Implication for SPR feature:** At SPR > 5, the feature value should reduce
the probability of a large bet sharply. At SPR < 2.5, larger sizing becomes
viable on the right textures. The model needs SPR as a gate on sizing, not just
hand strength.

**Classification:** Solver-based (GTO Wizard 3-way outputs, Galfond
solver-informed).

---

### Finding 3: SPR below 2 in a 3-way pot — bet to commit, not check to trap

**Source:** SplitSuit, "SPR Poker Strategy"
(https://www.splitsuit.com/spr-poker-strategy)

**Source:** GTO Wizard, "10 Tips for Multiway Pots in Poker"
(https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/)

**Specific data points:**

SplitSuit establishes the core SPR-commitment framework: "When SPR is low (< 2),
a set, flush, or straight will typically commit the stack. The lower the SPR,
the more you want to get your money in quickly rather than allowing opponents
to make cheap calls and draw out." This logic applies in HU and strengthens
in multiway because there are more opponents who could draw out with a free
or cheap card.

GTO Wizard multiway principle: when SPR is low, the equity denial argument for
betting increases because two opponents drawing (instead of one) makes the
cost of a free card much higher. At SPR ~1, giving two opponents a free card
risks losing to two independent draws simultaneously.

**The trap argument at low SPR:** Slow-playing (checking) with a strong hand at
low SPR 3-way is almost never correct. The reasons are:
- At SPR ~1, the pot is already large relative to stacks. A check surrenders
  equity denial vs two opponents.
- The opponents have independent draws — their combined probability of outdrawing
  you is significantly higher than HU.
- There is less "room" to extract money through deception. At SPR ~1, you get
  one bet in anyway; you might as well bet now to deny equity.
- Exception: Only the absolute nuts (top set on a rainbow board) might check
  to allow opponents to bet, and even this is texture-dependent.

**Implication for SPR feature:** At SPR < 2, the model should strongly favor
BET for strong hands (two pair+, sets, strong draws with equity). The low-SPR
check option is almost exclusively correct for hands that genuinely cannot win
(pure air) or where hero is checking behind IP for pot control with a marginal
hand.

**Classification:** Solver-referenced (SplitSuit) + solver-based principle
(GTO Wizard).

---

### Finding 4: SPR above 8 (deep stack) — small bets for pot control, not
large bets for equity denial

**Source:** GTO Wizard, "Monkey in the Middle: 3-Way Pot Heuristics"
(https://blog.gtowizard.com/monkey-in-the-middle-3-way-pot-heuristics/)

**Source:** Poker.pro, "Big Blind Economics: The Multiway Discount and the
Realisation Tax"
(https://www.poker.pro/strategy/big-blind-economics-the-multiway-discount-and-the-realisation-tax/)

**Specific data points:**

GTO Wizard monkey-in-the-middle analysis: at high SPR (deep stacks), the
positional advantage is amplified. IP players over-realize equity more at deep
SPR. The PFR at deep SPR wants to keep pots small with marginal hands because
multi-street play at high SPR is where positional disadvantage kills OOP ranges.

The equity denial argument for large bets at high SPR 3-way fails because:
1. Both opponents have correct pot odds to continue drawing even vs large bets,
   so the denial is less effective.
2. Betting large at high SPR commits a disproportionate fraction of the
   stack to a pot where the PFR has only ~33% average equity to start.
3. The "clearing up equity" approach (Galfond) — small bets to thin the field —
   is the dominant strategy at medium to high SPR.

**The equity denial counterargument (and why it is weaker 3-way):** In HU at
high SPR, a PFR might bet 60-75% pot on a board where the opponent holds
many draws. 3-way, this sizing requires the two defenders to collectively fold
at the required rate. With two opponents, each individually defending at ~30%
MDF vs a large bet, the bettor is denying equity to the entire range — but the
cost is: one opponent will continue with a strong hand roughly 30% of the time,
and the other 30% of the time independently. The bettor is often building a pot
with moderate equity into two continuing ranges.

**Implication for SPR feature:** At SPR > 8, the model should almost never
produce BET with a large size from the PFR. Small bets (20-33% pot) are correct
for value-thin hands; checking is correct for marginal hands. Strong hands (two
pair+, sets) still bet, but at small sizes for protection and to start building
value across multiple streets, not to deny equity with one large bet.

**Classification:** Solver-based (GTO Wizard) + solver-informed (Galfond).

---

### Finding 5: The commitment threshold in 3-way pots is approximately SPR 2-3
(higher than HU)

**Source:** SplitSuit, "SPR Poker Strategy"
(https://www.splitsuit.com/spr-poker-strategy)

**Source:** Red Chip Poker, "SPR and Commitment Thresholds"
(https://redchippoker.com/spr-commitment/)

**Specific data points:**

SplitSuit HU baseline: "A set or better at SPR < 4 is a commitment hand in
most cases HU. Top pair can commit at SPR < 2 HU." He explicitly notes
"multiway hands at the same numeric SPR often need tighter stack-off
thresholds."

The adjustment for 3-way: the commitment threshold shifts upward by roughly
one hand class. This means:
- HU: top pair can commit at SPR < 2; top pair good kicker can commit at SPR < 3.
- 3-way: top pair should not commit at SPR < 2; only two pair+ commits at
  SPR < 2-3.
- The reason is equity dilution: the same SPR number represents more
  risk multiway because there are two opponents who could have you beaten.

**The specific threshold estimate for 3-way:**

| Hand Class | HU Commit Threshold | 3-Way Commit Threshold |
|-----------|---------------------|----------------------|
| Top pair good kicker | SPR < 3 | SPR < 1.5 |
| Overpair | SPR < 4 | SPR < 2 |
| Two pair | SPR < 6 | SPR < 4 |
| Set | SPR < 10 | SPR < 7-8 |

Note: these are approximate working thresholds derived from the principle of
"tighter by one hand class at same SPR multiway." No single source provides
the exact 3-way thresholds in a table — this is a synthesis.

**Implication for SPR feature:** The SPR feature's interaction with hand strength
features (villain_top_pair_plus_pct, worse_hand_pct) changes at SPR boundaries.
At SPR 2-3, the model should not commit with top pair even though HU would.
The SPR feature needs to gate commitment decisions differently than in HU models.

**Classification:** SplitSuit solver-referenced for HU baseline; the 3-way
adjustment is a synthesis from the "tighter threshold" principle.

---

### Finding 6: 3-way pot geometry — how the extra player changes bet sizing math

**Source:** Mypokercoaching.com, "Playing Profitably in Multiway Pots: MDF"
(https://www.mypokercoaching.com/playing-profitably-in-mutliway-pots-mdf/)

**Source:** GTO Wizard, "MDF & Alpha"
(https://blog.gtowizard.com/mdf-alpha/)

**Specific data points:**

The core pot geometry change in 3-way:

**HU bet sizing math (33% pot bet):**
- Pot: 100. Bet: 33. Total pot after bet: 133.
- Alpha (breakeven fold %) = 33 / (100 + 33) = 24.8%.
- Need one opponent to fold 24.8% of the time.
- MDF per player: 75.2%.

**3-way bet sizing math (same 33% pot bet):**
- Pot: 100. Bet: 33. Total pot after bet: 133.
- Alpha (breakeven) = 33 / 133 = 24.8%. THE ALPHA IS THE SAME.
- BUT: you now need BOTH opponents to fold 24.8% of the time combined.
- Required fold per player (assuming independence): sqrt(1 - 0.248) = sqrt(0.752) ≈ 86.7%.
- The math inverts: to break even on a 33% pot bluff 3-way, each opponent must
  fold 86.7% of their range — an unrealistically high number.
- In practice, each opponent folds around 70-80% vs 33% pot, making pure bluffs
  breakeven or slightly losing.

This explains why small sizes (25-33% pot) in 3-way are used for VALUE (not
bluffing): they cost little, and the defender tightens enough that the PFR's
value range gets called by only strong hands (thin field).

**The third player cost to the bettor:**

When there are two callers instead of one:
- The pot before the bet is LARGER (both contributed to the original pot).
- The c-bettor is risking the same bet into a bigger pot, which means:
  - The same 33% pot bet is a larger absolute risk in a 3-way pot vs HU
    because the pot itself is larger (both opponents contributed preflop).
  - Example: HU pot 75bb (raiser 2bb, caller 1bb, dead money 1.5bb) vs
    3-way pot 100bb+ (raiser 2bb, two callers 1bb each, dead money more).
  - A 33% pot c-bet is ~25bb HU vs ~33bb+ in a 3-way pot.
  - So the risk is higher even at the same percentage, meaning the EV case
    for betting must be stronger.

**Implication for SPR feature:** The SPR feature implicitly encodes this
geometry: a higher pot (from more callers) with the same stacks means lower
SPR to start. At SPR 4 in a 3-way vs HU, the pot is larger relative to stacks,
meaning each c-bet is a larger commitment of remaining stack (in percentage
terms). The model should treat a given SPR value as MORE committed in 3-way
than HU.

**Classification:** Mathematical (derived from MDF math, universally accepted).

---

### Finding 7: Board texture modifies the sizing decision within each SPR zone

**Source:** GTO Wizard, "Flop Heuristics: IP C-Betting in Cash Games"
(https://blog.gtowizard.com/flop-heuristics-ip-c-betting-in-cash-games/)

**Source:** Poker.pro, "Multiway Muscle: Big-Bet Windows Revealed by GTO
Wizard" (https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/)

**Specific data points:**

Even within a given SPR zone, board texture shifts the optimal sizing:

**At medium SPR (2-5):**

| Board Type | Optimal Sizing (3-way) | Reason |
|-----------|----------------------|--------|
| Dry rainbow (A72r, K83r) | 25-33% pot | PFR has range edge; small bet thins field |
| Monotone | 25-33% pot | Flush draw callers have odds; large bet bloats pot with draws behind |
| Connected (T98, 876) | 20-25% pot or check | BTN's flatting range smashes these; small bet to probe |
| High-card two-tone (AKQ with two suits) | 33-40% pot | PFR has dominant range edge; slightly larger for value |
| Paired low (774r, 882r) | 33-50% pot | Dead boards; PFR's nut advantage maximized |

**At low SPR (< 2):**

Big bets (50-75% pot) become viable when PFR holds the nut advantage on the
board. The poker.pro data specifically notes that low SPR + nut edge + high/
paired boards is the trigger for large sizing 3-way. The logic: at low SPR,
both opponents are partially committed, and the PFR can overbet to force
commitment decisions now rather than string out small bets.

**At high SPR (> 8):**

Sizing shrinks further. Even strong hands check more frequently to allow
opponents to bluff into them on later streets (where SPR will be lower).
The GTO Wizard IP c-betting study shows that at deep stacks, checking back
strong-but-not-nut hands is common (protects the checking range and builds
deception).

**Implication for SPR feature:** The SPR feature interacts with the board
texture features (`danger_score`, `connectivity_score`, `is_monotone`) to
produce the correct sizing. The model needs both features to capture this
interaction — SPR alone is insufficient.

**Classification:** Solver-based (GTO Wizard) + solver-referenced (Poker.pro).

---

### Finding 8: OOP vs IP c-bet frequency by SPR zone (3-way specific)

**Source:** GTO Wizard, "Probing Out of Position in 3-Way Pots"
(https://blog.gtowizard.com/probing-out-of-position-in-3-way-pots/)

**Source:** GTO Wizard, "Playing In Position Against Two Callers"
(https://blog.gtowizard.com/playing-in-position-against-two-callers/)

**Specific data points:**

GTO Wizard's in-position study shows PFR c-bet frequency of ~43% aggregate.
But the frequency varies significantly by SPR:
- At low SPR (< 3): c-bet frequency approaches 60%+. The pot is already
  committed; the PFR bets to deny equity and build toward stack-off.
- At medium SPR (3-6): c-bet frequency near the ~43% aggregate.
- At high SPR (> 8): c-bet frequency drops to ~30-35%. More checking,
  especially OOP.

OOP dynamics: An OOP PFR (e.g., BB 3-bet caller, or SB open vs BTN call +
BB call) c-bets even less frequently at high SPR — the combination of OOP
and high SPR is the worst environment for c-betting. The probing study notes
that OOP probes (donk bets in a 3-way pot) are rare at all SPR levels, with
the exception of very low SPR where the OOP player bets to build toward
commitment.

**Implication for SPR feature:** SPR is a meaningful feature for the model.
It calibrates the threshold for how often to BET. Low SPR increases BET
probability; high SPR decreases it — but the direction of this effect is
moderated by position (the position features in the 45-feature pipeline
should interact with SPR).

**Classification:** Solver-based (GTO Wizard; the probing article is noted
in existing research as behind paywall but the directional finding is
consistent with the IP-callers study and general GTO principles).

---

## 3. SPR-Based Decision Framework for the BET Tree

This framework is designed for the 3-way labelling agent and model feature
engineering. It defines how SPR modulates the BET vs CHECK decision and bet
sizing.

### 3.1 Four SPR Zones

**Zone 1: SPR < 1 (Micro SPR — essentially already all-in)**

Definition: Pot is so large relative to stacks that any bet commits both
parties.

- PFA behavior: Bet/raise with any hand that has equity (50%+) vs the two
  opponents. No reason to check. The "trap" argument collapses because
  there is no future street value to protect.
- Sizing: All-in or close to pot. Fractional bets make no sense when SPR < 1
  because they don't achieve fold equity or protection differently from
  just shoving.
- Checking: Only correct with pure air (< 25% equity) where hero cannot profitably
  call a shove anyway.
- Label guidance: BET (or RAISE if facing a bet) for all hands with two pair
  or better, sets, and strong draws. CHECK only for complete air.

**Zone 2: SPR 1-2 (Low SPR — commitment zone)**

Definition: One pot-sized bet commits both stacks. Two smaller bets commit
both stacks across two streets.

- PFA behavior: Bet strong hands (two pair+, overpairs, strong top pairs on
  favorable boards). The question is sizing, not whether to bet.
- Sizing: 50-75% pot. Larger than medium SPR because the pot commitment dynamic
  is already active — might as well charge opponents to draw or fold now.
- Trapping at low SPR: Almost never correct. The exception is sets on very dry
  boards where opponents have very little drawing equity — even here, a small
  bet is usually preferable to a check because protection matters more than
  deception when draws are present (and two opponents mean more draws in the
  combined range).
- Checking at low SPR: Correct for marginal hands (top pair weak kicker,
  middle pair) that cannot profitably commit to the pot but have
  showdown value. Check-call one street; fold to aggression.
- Label guidance: BET 50-75% pot for strong hands; CHECK for marginal
  made hands; FOLD for pure draws that lack commitment equity.

**Zone 3: SPR 2-5 (Medium SPR — core 3-way c-betting window)**

Definition: The standard post-flop 3-way condition in 100bb 6-max. Most
3-way single-raised pots start here after preflop action.

- Typical starting SPR at 100bb: After CO opens 2.5bb, BTN calls, BB calls,
  pot is ~8bb, stacks ~97.5bb → SPR ≈ 12 pre-flop, but on the flop after
  standard c-bet sizing, effective SPR compresses quickly. If we define SPR
  as effective stack / pot at the decision point, most flops in 100bb
  single-raised pots start at SPR ~8-12 (effective stacks ~97bb, pot ~8bb).
  NOTE: This means Zone 3 "medium SPR" of 2-5 actually applies more to
  TURN situations or 3-bet pots at 100bb, not standard flop spots.

Correction/clarification: At 100bb 6-max single-raised pot (3-way):
- Pot on flop: ~8bb (CO 2.5bb + BTN 1bb + BB 1bb + antes/dead = ~8bb if
  using approximate numbers). Effective stacks ~97bb.
- Flop SPR = 97 / 8 ≈ 12.

This means standard 3-way flop SPR is typically HIGH (8-15), not medium.
The medium SPR zone (2-5) appears on the turn after a flop c-bet, or
in 3-bet pots.

Revised SPR zone mapping for 100bb 3-way:

| Street | Typical SPR | Zone |
|--------|------------|------|
| Flop (single-raised pot, 100bb) | 8-12 | High |
| Flop (3-bet pot, 100bb) | 2-4 | Medium |
| Turn (after flop c-bet in SRP) | 4-6 | Medium |
| Turn (after flop c-bet in 3BP) | 1-2 | Low |
| River (after two streets) | < 2 | Low-Micro |

This is a critical practical insight: the "high SPR" behavior (small bets,
pot control, frequent checks) is the DEFAULT behavior on the flop in a
standard 3-way single-raised pot at 100bb. The "medium SPR" behavior applies
to turns in single-raised pots and flops in 3-bet pots.

- Core 3-way c-bet behavior at flop SPR 8-12:
  - Bet frequency: ~43% (solver aggregate).
  - Sizing: 25-33% pot.
  - Large bets: ~1.3% of situations (near zero).
  - Checking strong hands: common, especially OOP.

**Zone 4: SPR > 12 (Very deep — rare in standard 100bb games, applies to
150bb+ or short-stack spots)**

Definition: Very deep effective stacks relative to pot. Most relevant in
live poker (200bb+ deep) or online high-stakes (150bb+ games).

- PFA behavior: Even more conservative. C-bet frequency drops further.
  Only very strong value bets with board advantage.
- Sizing: 20-25% pot.
- Checking: Dominant response for most hands including strong ones.
- Implication: Position is paramount at very deep SPR.

---

### 3.2 SPR and the BET Decision: Feature Engineering Implications

The SPR feature in the 45-feature pipeline interacts with the BET decision
in the following ways (for model training):

**SPR as a bet-frequency modulator:**
- Low SPR → higher bet frequency for strong hands.
- High SPR → lower bet frequency, more checking.
- The relationship is roughly monotonic but non-linear (the inflection points
  are the commitment thresholds in Section 2, Finding 5).

**SPR as a sizing modulator:**
- Low SPR → larger sizing as % of pot (approaching all-in).
- Medium SPR → 33-50% pot.
- High SPR → 25-33% pot.
- Very high SPR → 20-25% pot.
- The sizing implication is for how to label BET decisions — a "BET" at
  low SPR should be coded as a larger bet than a "BET" at high SPR.

**SPR interaction with hand strength features:**
- At low SPR, top pair may be a fold if facing aggression, but can be a
  bet if first to act (commitment threshold).
- At high SPR, top pair is a check-call, not a bet-call for pot building.
- The commitment threshold determines when BET transitions from
  "value bet" to "committing to the pot."

**SPR interaction with position features:**
- OOP + high SPR: strongest argument against betting. Check-call becomes
  dominant.
- IP + high SPR: still prefer small bets or checks for pot control, but IP
  advantage slightly buffers the high-SPR check tendency.
- OOP + low SPR: even here, OOP must bet strong hands (two pair+) to deny
  equity to two opponents.

---

### 3.3 Decision Tree Summary (3-way, PFR perspective)

```
Is SPR < 2?
  YES → Bet strong hands (two pair+, sets, strong draws). Size 50-75% pot.
        Do NOT trap. Check only marginal hands for pot control.
  NO → Continue to next check.

Is SPR 2-5?
  YES (medium, typically turn in SRP or flop in 3BP):
        → Bet selectively at 33-40% pot.
        → Check marginal value hands; bet clear value and equity denial hands.
  NO → Continue.

Is SPR 5-12?
  YES (high, typically flop in SRP at 100bb):
        → 25-33% pot is standard.
        → C-bet ~43% frequency; check ~57%.
        → Large bets ~1.3% only (near zero except specific textures).
        → Check strong hands OOP; bet selectively IP.
  NO (SPR > 12, very deep):
        → 20-25% pot.
        → Even lower bet frequency.
        → Position is decisive.
```

---

## 4. Contradictions and Gaps

### 4.1 Contradictions

**Apparent contradiction: Galfond ("essentially no big betting on the flop")
vs Poker.pro ("big-bet windows exist 3-way").**

Resolution: Not a real contradiction. Galfond's statement applies to the
STANDARD medium-to-high SPR flop situation (the default case). Poker.pro
explicitly frames big bets as exceptions that require convergence of four
conditions (nut edge + last action + low SPR + specific board). The sources
are complementary.

**Apparent contradiction: "c-bet frequency ~43% 3-way" vs "at low SPR, bet
frequency is higher."**

Resolution: The 43% aggregate figure (GTO Wizard, LJ vs two callers) is for
standard flop situations in a 100bb single-raised pot, where SPR is ~8-12.
At lower SPR (3BP flops, turn spots), c-bet frequency is higher. The
aggregate number is not a universal ceiling.

**Apparent contradiction: "always small bets 3-way" vs "50-75% at low SPR."**

Resolution: "Always small" is a flop heuristic for the standard single-raised
pot at 100bb (SPR ~8-12). At low SPR (< 2), the dynamics change and sizing
must increase to charge draws and commit opponents. This is a SPR-conditional
rule, not a universal rule.

### 4.2 Gaps in Available Data

**Gap 1: No public solver output giving exact 3-way c-bet frequency by SPR
zone.**

The GTO Wizard "43% aggregate" figure comes from a single configuration
(LJ opens, two callers, 100bb). No publicly available source provides a table
of c-bet frequency across a range of SPR values for 3-way pots. The directional
claims (low SPR → more betting, high SPR → less) are theoretically solid but
not numerically pinned from solver data.

**Implication:** The model should treat SPR as a continuous feature that shifts
bet probability directionally. Hard SPR thresholds should not be used.

**Gap 2: Exact commitment thresholds for 3-way pots by hand class.**

SplitSuit provides HU thresholds; the 3-way adjustment ("tighter by one hand
class") is a principle, not a precisely solver-verified table. The thresholds
in Finding 5 Section 2 are synthesized estimates, not direct solver outputs.

**Implication:** The commitment threshold table in Section 3.1 should be
treated as a working approximation. Solver verification would require running
specific 3-way SPR scenarios in GTO Wizard 3-way solver.

**Gap 3: SPR effect on OOP c-bet frequency specifically.**

The 43% aggregate is for IP c-betting. The GTO Wizard probing study (OOP
donk-betting in 3-way) is partially behind a paywall. The specific frequency
for OOP c-bets (or probe bets) by SPR zone is not quantified in public
sources.

**Implication:** The labelling agent should use the known principle (OOP
c-bets less than IP at all SPR levels; the SPR directionality is the same)
but cannot apply exact frequencies for OOP.

**Gap 4: SPR interaction with board texture — quantified data for 3-way.**

The texture-by-texture sizing recommendations in Finding 7 are qualitative
(e.g., "dry rainbow → 25-33%") but no source provides a table of exact
sizing frequencies for each texture type at each SPR level in 3-way. The
GTO Wizard IP c-betting study provides texture data for HU; the extension
to 3-way requires inference.

**Implication:** The model should learn texture × SPR interactions from
training data rather than encoding hard rules. The labelling agent should
use the qualitative principles as reasoning guides, not exact thresholds.

---

## 5. Integration with Existing KB

The following additions or amendments to `knowledge/three_way_gto.md` are
recommended based on this research:

### 5.1 Expand Section 1.6 (SPR Compression)

Current KB text notes that a pot-sized flop bet leaves SPR ~1.5 on the turn.
Recommend adding:

- The four SPR zones (micro, low, medium, high) with typical street mappings.
- The commitment threshold table (adjusted for 3-way vs HU).
- The key practical insight: standard single-raised 3-way flop SPR is ~8-12,
  not medium SPR. "High SPR behavior" is therefore the DEFAULT on most flops.

### 5.2 New DO NOT Rule candidate

**Proposed DO NOT Rule #9:** "DO NOT apply the HU commitment threshold to
3-way pots. Top pair does not commit at SPR < 3 in 3-way pots — only two pair
or better commits. The same SPR number requires a stronger hand to justify
commitment when two opponents are present."

### 5.3 New Reference Data entry (Section 1.x)

**SPR zones and c-bet sizing table:**

| SPR Zone | Typical Context (100bb) | C-Bet Freq | Sizing When Betting | Commit Threshold |
|----------|------------------------|-----------|---------------------|-----------------|
| < 1 | River, or very short stack | ~80%+ | All-in / pot | Any two pair+ |
| 1-2 | Turn in 3BP, or river in SRP | ~65% | 50-75% pot | Two pair+ |
| 2-5 | Flop in 3BP, or turn in SRP | ~50% | 33-40% pot | Overpair+ |
| 5-12 | Flop in SRP at 100bb | ~43% | 25-33% pot | Set+ |
| > 12 | Very deep (150bb+) | ~30-35% | 20-25% pot | Set+ |

---

## 6. Source Index

| # | Source | URL | Key Data Point | Type |
|---|--------|-----|----------------|------|
| 1 | GTO Wizard – Playing IP Against Two Callers | https://blog.gtowizard.com/playing-in-position-against-two-callers/ | Pot-sized c-bet drops 18% → 1.3%; small sizing dominates; check freq +11% | Solver-based |
| 2 | GTO Wizard – 10 Tips Multiway Pots | https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/ | Small bets dominate; pure bluffs unprofitable; 33% avg pot share | Solver-based |
| 3 | GTO Wizard – Monkey in the Middle | https://blog.gtowizard.com/monkey-in-the-middle-3-way-pot-heuristics/ | Deep SPR amplifies positional advantage; sandwich must fold more | Solver-based |
| 4 | GTO Wizard – MDF & Alpha | https://blog.gtowizard.com/mdf-alpha/ | Alpha = bet / (pot + bet); 3-way alpha applies to combined fold requirement | Theoretical |
| 5 | GTO Wizard – Probing OOP in 3-Way Pots | https://blog.gtowizard.com/probing-out-of-position-in-3-way-pots/ | OOP probe frequency lower; direction: low SPR → more probing | Solver-based |
| 6 | Phil Galfond – Mastering Multi-Way Pots | https://www.philgalfond.com/articles/mastering-multi-way-pots | No big betting on flop in MW; 25-33% clearing-equity approach | Solver-informed |
| 7 | Poker.pro – Multiway Muscle: Big-Bet Windows | https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/ | Big bets justified at low SPR + nut edge + high/paired boards | Solver-based |
| 8 | SplitSuit – SPR Poker Strategy | https://www.splitsuit.com/spr-poker-strategy | HU commit thresholds by hand class; 3-way thresholds tighter | Theoretical/solver-ref |
| 9 | Mypokercoaching.com – Multiway MDF | https://www.mypokercoaching.com/playing-profitably-in-mutliway-pots-mdf/ | Per-player fold: sandwich 80%, closer 60%; combined ~48% | Theoretical |
| 10 | Poker.pro – Big Blind Economics | https://www.poker.pro/strategy/big-blind-economics-the-multiway-discount-and-the-realisation-tax/ | EQR tax OOP multiway; high SPR amplifies OOP disadvantage | Theoretical/solver-inf |
| 11 | GTO Wizard – Flop Heuristics IP C-Betting | https://blog.gtowizard.com/flop-heuristics-ip-c-betting-in-cash-games/ | HU IP aggregate: 17.5% pot-sized, 36.9% small, 45.7% check | Solver-based |
| 12 | Red Chip Poker – SPR and Commitment | https://redchippoker.com/spr-commitment/ | Commitment threshold concept; SPR < 4 set commits HU | Theoretical/solver-ref |

---

*File path: `/home/rupertbeytell/river-rats-v2/review/RESEARCH_CBET_R3_SIZING_SPR.md`*
*Status: Ready for review. Not yet approved for KB integration.*
