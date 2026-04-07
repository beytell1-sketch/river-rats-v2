# 3-Way Postflop GTO Knowledge Base

**Version:** 1.0
**Date:** 6 April 2026
**Purpose:** Reference document for the 3-way labelling agent.
Contains quantified facts (as reasoning inputs), a decision
framework, preflop range construction, board texture interactions,
and worked examples. NOT a set of threshold rules.
**Sources:** 80+ references across GTO Wizard (solver), Upswing,
Phil Galfond, Peter Clarke, MonkerSolver, PioSolver. Full source
index in research/ directory.

---

## 1. Reference Data

Quantified facts the agent uses as INPUTS to reasoning. These are
not decision rules. No single number determines the correct action.

### 1.1 Fold Equity

| Context | Fold equity to break even (pot-sized bet) | Source |
|---------|------------------------------------------|--------|
| HU | 50% (one opponent folds) | Math |
| 3-way | ~49% (need BOTH to fold: 0.70 x 0.70) | Math + GTO Wizard |

Each opponent only needs to defend ~30% (vs 50% HU). The defense
burden is shared. But it's asymmetric:
- Sandwich player (action behind): defends ~20%, folds ~80%
- Closing action player: defends ~40%, folds ~60%
- Combined: 0.80 x 0.60 = 0.48, meeting the ~50% MDF

**Implication for reasoning:** At 70% fold per opponent, fold equity
is 49% — still below the 50% breakeven for a pot-sized bluff. Pure
bluffs are unprofitable 3-way. Semi-bluffs require strong draws (nut flush draw,
combo draws). Gutshots and backdoor-only hands are check/folds.

### 1.2 Equity Dilution by Hand Class

| Hand class | Equity HU | Equity 3-way | Drop |
|-----------|-----------|-------------|------|
| AA | ~85% | ~73.5% | -11.5pp |
| AKo | ~65% | ~45-47% | -18 to -20pp |
| Overpairs (general) | ~60% | low-40s% | ~-18pp |
| TPTK | ~65% | ~50-55% | ~-12pp |
| Top pair weak kicker | ~55% | ~38-42% | ~-15pp |

Rough heuristic: premiums lose ~12% equity per additional opponent.

**Implication for reasoning:** Hands that are clear value bets HU
become marginal or even check-behind candidates 3-way. Top pair
weak kicker is a pot-control hand, not a value hand.

### 1.3 C-Bet Frequency (Solver)

| Metric | HU | 3-way | Change |
|--------|-----|-------|--------|
| Overall c-bet frequency | ~54% | ~43% | -11pp |
| Large (pot-sized) c-bet | ~18% | ~1.3% | virtually eliminated |
| Check frequency | ~46% | ~57% | +11pp |
| Default sizing when betting | Mixed (33-100%) | Small (25-33% pot) | Size down |

Range-betting is never correct 3-way. When betting, the range is
tighter and stronger than HU. Big bets (50%+ pot) are rare
exceptions on specific textures.

### 1.4 Bluff-to-Value Ratio

| Context | Ratio (pot-sized bet, river) | Source |
|---------|----------------------------|--------|
| HU | ~1:2 (33% bluffs) | GTO math |
| 3-way | ~1:4 or tighter (estimated) | Derived from solver principles |

The betting range is much more value-heavy 3-way. Pure bluffs are
nearly eliminated; only the strongest bluffs (nut blockers, strong
draws that missed) remain.

### 1.5 Equity Realization by Position

| Position | EQR range | Notes |
|----------|-----------|-------|
| IP (BTN/CO, closing action) | 105-120%+ | Over-realizes |
| OOP (BB, first to act) | 60-80% | Under-realizes |
| Sandwich (middle) | Worst seat | Must fold more, heuristics fail |

On 9s-3s-2d: IP realized 118.1% of equity, BB realized 79.1%
(PioSolver). Position is amplified 3-way because there's more
information to exploit and more opponents to act behind.

### 1.6 SPR Compression

A pot-sized flop bet 3-way leaves SPR ~1.5 on the turn (vs ~3-4
HU), which effectively commits stacks. The flop bet decision must
account for the full remaining tree at compressed SPR. Same numeric
SPR requires tighter stack-off thresholds multiway (more opponents
who could have you beat).

---

## 2. Decision Framework

Every 3-way postflop decision depends on the interaction of 5
factors. No single factor is decisive. The correct action emerges
from weighing all five.

### Factor 1: Equity Position

Raw equity relative to pot odds. Reference data (Section 1.2)
provides the baseline, but equity alone does not determine the
action. A hand with 45% equity may be a BET (if other factors
align) or a CHECK (if they don't).

### Factor 2: Position

- **IP (closing action):** Can bet thinner for value, can bluff
  more effectively (one fewer player to act behind), realizes
  more equity. But 3-way IP c-bet frequency is still only 30-45%,
  not 65%+.
- **OOP (first to act):** Under-realizes equity. Must play tighter
  ranges. Pot control is more important. Checking strong hands is
  common (even AA checks ~80% OOP on dry boards in 3-bet pots).
- **Sandwich:** Worst position. Must worry about players on both
  sides. Tighten continuing range 15-20% vs HU cutoffs.

### Factor 3: Range Composition

The 45-feature pipeline provides:
- `villain_top_pair_plus_pct`: high = villain range is strong
- `villain_air_pct`: high = villain range is weak
- `villain_range_capped`: 1 = no premiums in villain range
- `board_favour`: positive = board favours hero's range

These features encode the preflop construction → postflop range
interaction. When villain_air_pct is high, thin value bets become
profitable. When villain_tp_plus_pct is high, pot control is
correct even with strong hands.

**Critical: the two opponents are NOT symmetric.** The cold-caller
(BTN flat) is capped — no AA/KK/QQ/AKs. The blind defender (BB)
is wide but uncapped via squeeze. Reasoning must distinguish them.

### Factor 4: Board Texture

From the pipeline: `danger_score`, `flush_danger`,
`straight_danger`, `connectivity_score`, `is_monotone`, etc.

**Boards that favour the preflop raiser (CO/HJ):**
- Ace-high dry/rainbow (A72r, AK5r): raiser has more Ax, AK
- King-high paired (KK5r): raiser has all premium pairs
- Static, disconnected: equity doesn't shift across streets

**Boards that favour the cold-caller (BTN):**
- Connected middling (764r, T86): BTN flat range is dense with
  suited connectors that smash these
- Two-tone middling: BTN has flush draws + pair+draw combos

**Boards that favour the BB defender:**
- Low, connected (532, 643): BB's speculative overcalling range
  hits hard — small pairs for sets, suited connectors for straights
- Monotone low: BB's suited hands connect disproportionately

### Factor 5: Action History

- `facing_bet`: someone has bet this street
- `facing_raise`: someone raised (not just bet) — strong signal
- `num_callers_to_bet`: bet-and-call = confirming signal from
  second opponent. Two ranges are condensed.
- `villain_aggression_count`: multi-street betting = strong range
- `villain_checked_back`: villain showed weakness on a prior street

**The bet-and-call signal (MW-30 pattern):** When one opponent bets
and another calls in a 3-way pot, both ranges have narrowed. The
bettor is representing strength. The caller is confirming with a
hand strong enough to continue against the bet AND the remaining
player. Facing bet-and-call, only strong hands continue.

**The check-raise signal (MW-31 pattern):** A check-raise into
two opponents in a 3-way pot is almost exclusively the nuts or
near-nuts. The raiser must beat not only the bettor's range but
also the third player's calling range. Even top pair top kicker
folds to a 3-way check-raise.

---

## 3. Preflop Construction → Postflop Ranges

### CO open / BTN flat / BB defend (most common 3-way)

- **CO opens ~27-28%:** Linear, uncapped. All premiums, strong
  broadways, suited connectors, suited aces, medium pairs.
- **BTN flats ~5%:** Condensed, capped. 22-TT, suited connectors
  (76s-JTs), suited aces (A2s-A5s), some KTs/QJs. Missing AA/KK/
  QQ/AKs (those 3-bet). Hits most boards with pairs and draws but
  can't make the nuts as often as CO.
- **BB overcalls wide:** Speculative suited/connected hands, small
  pairs. Needs ~19% equity. Capped (premiums would squeeze). OOP
  reduces EQR, so BB is selective despite good odds.

### HJ open / CO flat / BB defend

- **HJ opens tighter (~22-24%):** Stronger range than CO. More
  overpairs, more AK/AQ.
- **CO flats ~4-6%:** Even more capped than BTN vs CO. Very
  condensed.
- **BB:** Similar to above but facing a stronger open.

### Key insight for labelling

The opener's range width determines villain_air_pct. A CO opener
has more air than an HJ opener. The cold-caller is always capped.
The BB is always wide. When the features show high villain_air_pct,
it reflects a wider opening range, which supports thinner value.

---

## 4. Worked Examples

Each example shows the full reasoning chain: factors identified →
weighed → conflicts resolved → action chosen.

### Example 1: Strong hand OOP — check for pot control

**Setup:** Hero holds KcQc on Kh 8d 3s. BB (OOP), 2 opponents
(CO opened, BTN called). Pot 90, checked to hero (first to act).

**Factors:**
1. Equity: ~52% (marginal 3-way for top pair second kicker)
2. Position: OOP — hero acts first, worst position
3. Range composition: villain_air_pct ~0.25 (moderate), BTN is
   capped but CO is uncapped with AK/KK in range
4. Board: dry, rainbow, low danger — favours raiser (CO)
5. Action: no prior aggression this street

**Factor interaction:** Equity suggests possible thin value. But
OOP + board favouring CO + CO's uncapped range (has AK, KK that
dominate KQ) = too much risk. Betting folds out worse (BTN's
middle pairs) and gets called/raised by better (CO's AK, KK).

**Action:** CHECK
**Confidence:** HIGH
**Alternative:** BET small (33%) — rejected because OOP, and the
hands that call are mostly better. Showdown value is high enough
to check-call if CO bets.

### Example 2: Thin value bet IP with air-heavy villain range

**Setup:** Hero holds Jh9h on Jc 7d 2s. BTN (IP), 2 opponents
(CO opened, BB defended). Pot 100, both check to hero.

**Factors:**
1. Equity: ~54% (top pair decent kicker, marginal 3-way)
2. Position: IP with closing action — strong positive
3. Range composition: villain_air_pct ~0.32 (high air — CO checked
   back on a board that favours their range, BB checked)
4. Board: dry, rainbow — low danger
5. Action: both opponents checked — showing weakness

**Factor interaction:** Equity is marginal by reference data. But
IP + high villain air (0.32) + dry board + both opponents showed
weakness = strong factor combination for thin value. Hero's bet
folds out villain's air (which has some equity) and gets called
by worse pairs (77, 88, Jx worse kicker).

**Action:** BET (small, ~33% pot)
**Confidence:** MEDIUM
**Alternative:** CHECK — reasonable for pot control, but leaving
value against two wide, weak ranges.

### Example 3: Fold to bet-and-call despite decent equity

**Setup:** Hero holds Kd Th on Ks Jc 6h. BB, 2 opponents. Pot 155.
CO bet 35, BTN called. Hero faces 35 to call (pot odds ~18.4%).

**Factors:**
1. Equity: ~39.9% (well above pot odds of 18.4%)
2. Position: last to act this street
3. Range composition: CO's bet into 3-way = strong. BTN's cold-call
   of CO's bet = credibly Kx+ or better. Combined range is strong.
4. Board: dry — but irrelevant when both opponents show strength
5. Action: bet-and-call — the strongest signal in multiway poker

**Factor interaction:** Raw equity (39.9%) massively exceeds pot odds
(18.4%), which naively suggests CALL. But the bet-and-call sequence
narrows both opponents' ranges to hands that crush KT. BTN's call
specifically represents KJ, KQ, AK, or better — all dominating
hero's kicker. The raw equity is computed against full preflop ranges,
not the narrowed post-action ranges. This is where action history
overrides equity.

**Action:** FOLD
**Confidence:** HIGH
**Alternative:** CALL — rejected. Equity against the ACTION-IMPLIED
ranges (not the preflop ranges) is much lower than 39.9%. Hero is
dominated by better Kx and crushed by sets/two-pair.

### Example 4: Must bet monster — don't slowplay 3-way

**Setup:** Hero holds 8c 8h on Jd 8s 5c. BTN (IP), 2 opponents.
Pot 120. Both check to hero.

**Factors:**
1. Equity: ~82% (middle set, near-nut hand)
2. Position: IP — ideal for building pot
3. Range composition: both opponents checked on a board with
   straight draws and flush draws possible on future streets
4. Board: semi-connected, two-tone possible on turn — danger of
   free cards
5. Action: both checked — giving free cards is dangerous with draws

**Factor interaction:** Monster equity + IP + two opponents who
could have draws = must bet. 3-way, the probability of being
outdrawn on free cards is dramatically higher than HU (two opponents
drawing). Sets MUST bet multiway — slowplaying risks letting
draws get there for free.

**Action:** BET (50-66% pot)
**Confidence:** HIGH
**Alternative:** CHECK (slowplay) — rejected. Multiple opponents =
too many draws in the combined range. Protection is critical.

### Example 5: Draw OOP — check, don't semi-bluff

**Setup:** Hero holds Td 9d on Qd 7h 3d. BB (OOP), 2 opponents.
Pot 90. First to act.

**Factors:**
1. Equity: ~36% (flush draw + gutshot = 12 outs)
2. Position: OOP — worst position for semi-bluffing
3. Range composition: CO opened (uncapped), BTN called (capped
   but connected range hits middle boards)
4. Board: two-tone — flush draw is visible to opponents
5. Action: hero is first to act

**Factor interaction:** Decent draw equity, but OOP + two opponents
= fold equity is ~36% (0.6 x 0.6). Semi-bluff needs fold equity to
be profitable. With two opponents who see the flush draw on board,
even fewer will fold. Check and realize equity cheaply — if someone
bets, calling has correct odds with 12 outs.

**Action:** CHECK
**Confidence:** HIGH
**Alternative:** BET (semi-bluff) — rejected. OOP semi-bluffs into
two opponents have ~36% fold equity at best. With a visible flush
draw on board, actual fold equity is even lower. Check-call is the
line.

### Example 6: OOP value bet — high equity overrides position default

**Setup:** Hero holds Qs Jd on Qc 8d 3s. SB (OOP, first to act),
2 opponents (BTN opened, BB called). Pot 90, not facing bet.

**Factors:**
1. Equity: ~60% (top pair second kicker — strong for 3-way)
2. Position: OOP — normally argues for pot control
3. Range composition: villain_air_pct ~0.49 (very high), villain
   range capped (BTN flat missing premiums), worse_hand_pct 88%
4. Board: dry, rainbow, danger 0.00 — static, equity stable
5. Action: hero is first to act, no aggression to respect

**Factor interaction:** OOP position normally defaults to CHECK for
pot control. But this hand has 60% equity with 88% worse hands on
a dry board — far above the typical OOP pot-control threshold.
The key distinction: "AA checks 80% OOP on dry board" applies to
3-bet pots with deep SPR where the opponent's range is strong and
uncapped. Here, in a single-raised pot, villain ranges are weaker
(high air, capped) and hero's TPSK is near the top of hero's own
range. When equity is 60%+, worse_hand_pct is 85%+, and the board
is dry/static, the OOP penalty is insufficient to override the
value from betting. A small bet (25-33% pot) gets called by worse
pairs, Jx, pocket pairs, and some draws.

**Action:** BET
**Confidence:** HIGH
**Alternative:** CHECK — defensible as pure pot control, but leaves
significant value against two wide, weak ranges. With 88% worse
hands and a dry board, hero's equity is stable enough that OOP
risk is minimal.

**When does OOP default to CHECK instead?** When equity is marginal
(< 50%), villain range is strong/uncapped, or the board is dynamic.
The AA-checks-80% reference data applies to 3-bet pots where the
opponent has AA/KK/AK — not to single-raised pots against capped
ranges with high air.

### Example 7: Overcard equity — AK on a missed board

**Setup:** Hero holds Ad Ks on Jd 8d 4c. BB (OOP), 2 opponents.
Pot 90. CO bets 33 (pot odds 26.8%). draw_outs = 0 in the feature
vector.

**Factors:**
1. Equity: ~25% (no pair, no flush/straight draw per pipeline)
2. Position: OOP — unfavourable
3. Range composition: CO uncapped, villain_tp_plus ~0.47 (strong)
4. Board: semi-wet (two diamonds), danger 0.25
5. Action: facing a standard c-bet from CO

**Factor interaction:** The pipeline reports draw_outs = 0 because
it counts flush draws and straight draws, NOT overcards. But AK
has 6 overcard outs (3 aces + 3 kings) worth ~24% to improve to
top pair by the river. These are "hidden outs" not captured in the
feature vector. When hero hits an ace or king, the hand is likely
best (TPTK). Additionally, AK has backdoor flush draw potential
with Ad. The true equity (~25%) is close to pot odds (26.8%), but
accounting for overcard improvement and implied odds when hero hits,
this becomes a profitable call.

**Action:** CALL
**Confidence:** MEDIUM
**Alternative:** FOLD — defensible if equity is exactly at pot odds
with no improvement path. But AK's overcards provide hidden equity
the feature vector understates. The hand has showdown potential if
checked through on turn, and significant value when it improves.

**Key lesson:** When draw_outs = 0 but hero holds unpaired high
cards (AK, AQ) on a low/medium board, consider overcard outs as
hidden equity not captured in the features. 6 overcards ≈ 24%
improvement probability.

### Example 8: Draw equity survives multi-street aggression

**Setup:** Hero holds Qh Tc on Ks Qd 7c Jh. BTN (IP), 2 opponents.
Turn. Pot 200. CO fires 60 (second barrel). villain_aggression=2.

**Factors:**
1. Equity: ~27% (second pair + open-ended straight draw, 8 outs)
2. Position: IP — favourable for equity realization
3. Range composition: villain_tp_plus 63%, villain_air 4% — very
   strong, value-heavy betting range
4. Board: danger 0.88 (very high), many straights possible
5. Action: CO double-barrel into two opponents — strong signal

**Factor interaction:** Multi-street aggression (villain_aggression=2)
signals a strong, narrow range. The knowledge base teaches that
action history overrides equity for dominated hands without outs
(the MW-30 pattern). But this hand is NOT dominated without outs —
hero has second pair (showdown value) PLUS 8 straight outs (any T
or A makes a straight). The distinction is critical:

- MW-30 pattern (FOLD): top pair weak kicker, no draws, facing
  bet-and-call. Hero is dominated with zero improvement path.
- THIS pattern (CALL): second pair with 8 draw outs, IP, pot odds
  nearly met. Hero has a significant improvement path.

The aggression signal narrows villain's range, reducing hero's
made-hand equity. But the 8 draw outs survive range narrowing —
when hero makes the straight, it beats villain's entire range.
Combined with IP position and nearly correct pot odds, the draw
equity tips the decision from FOLD to CALL.

**Action:** CALL
**Confidence:** MEDIUM
**Alternative:** FOLD — defensible given the multi-street aggression
and 63% TP+ in villain's range. But hero's 8 clean outs to a
straight (~16% per street, ~32% by river) combined with IP position
and current pot odds make calling marginally profitable even against
the narrowed range.

**Key lesson:** "Action history overrides equity" applies to
dominated hands with no outs. When hero has significant draw equity
(8+ outs to a strong hand), the draw equity survives range
narrowing. Don't conflate "villain is strong" with "always fold."

---

## 5. DO NOT Rules

Each rule explains WHY the naive reasoning fails so the agent can
generalise, not memorise.

**1. DO NOT decide based on equity alone.** 3-way decisions depend
on the interaction of all 5 factors. 55% equity is a BET when IP +
air-heavy villain + dry board, but a CHECK when OOP + strong villain
range + wet board. Equity is an input, not a threshold.

**2. DO NOT barrel draws into 2 opponents hoping for folds.** 3-way
fold equity is ~36% (0.6 x 0.6). A flush draw semi-bluff that
prints money HU (60% fold equity) loses money 3-way. Check and
realize equity, or check-raise only with the nut draw.

**3. DO NOT assume the checking player has nothing.** 3-way, players
trap more because a third opponent may bet for them. A check-raise
into two opponents is almost exclusively the nuts.

**4. DO NOT auto-c-bet IP just because you have position.** IP
c-bet frequency 3-way is 30-45%, not 65%+. Two opponents = two
chances to run into strength. Board texture and range composition
determine whether to bet.

**5. DO NOT treat top pair as a strong hand.** Top pair is medium-
strength 3-way. The threshold for "strong enough to build a pot"
shifts up by roughly one hand class: two pair+ to bet big, vs TP+
in HU. Top pair good kicker is a pot-control hand.

**6. DO NOT overweight blockers.** Blockers matter ~40% less 3-way
because you'd need to block both opponents' ranges simultaneously.

**7. DO NOT analyze streets in isolation.** A pot-sized flop bet
3-way leaves SPR ~1.5 on the turn. The flop decision must account
for the full remaining tree at compressed SPR.

**8. DO NOT assume both opponents have equivalent ranges.** The
cold-caller (BTN flat) is capped — no premiums. The blind defender
(BB) is wide but uncapped via squeeze. Reasoning must distinguish
between them: the capped player folds strong draws less, the wide
player folds air more.

---

## 6. Sources

**Solver-based (highest authority):**
- GTO Wizard blog (10+ articles on multiway strategy)
- PioSolver equity realization studies
- MonkerSolver multiway benchmarks

**Expert with solver support:**
- Phil Galfond (philgalfond.com) — multiway pot framework
- Peter Clarke — multiway postflop principles
- PokerCoaching.com — multiway modules
- Run It Once — multiway strategy content

**Theoretical:**
- MDF/Alpha math (universally accepted)
- Equity dilution calculations

**Full source index:** See `research/` directory for 80+ cited URLs
with per-source classification.

## 7. Ignore List

- Pre-2018 poker forum advice (outdated, pre-solver era)
- HU-focused content applied to multiway without adjustment
- Exploitative "read-based" frameworks (not GTO)
- Any source that uses HU c-bet frequencies in multiway spots
- Doug Polk / Upswing HU-specific content repurposed for multiway

---

## Version History

- **v1.1 (6 Apr 2026):** Added 3 worked examples from calibration
  exam failures. Fixes: OOP value betting exception (Example 6),
  overcard hidden equity (Example 7), draw equity surviving
  aggression (Example 8). Now 8 examples total. Calibration:
  v1.0 scored 20/24, v1.1 targets fixing MW-17/24/28/41.
- **v1.0 (6 Apr 2026):** Initial knowledge base. 5 worked examples,
  8 DO NOT rules, quantified reference data from 80+ sources.
  Research files in `research/` directory.

After each training gate, failures are analyzed and new worked
examples are added. Principles stay stable. Examples accumulate.
