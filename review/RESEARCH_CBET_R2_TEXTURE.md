# C-Bet Frequency by Board Texture in 3-Way Pots
## Research Round 2: Board Texture Effects

**Date:** 2026-04-09
**Version:** 1.0
**Scope:** How specific board textures affect PFA c-bet frequency in 3-way pots (CO opens,
BTN + BB call). Cash game, 100bb, 6-max. Research extends existing KB coverage in
`knowledge/three_way_gto.md` and `research/3way_ranges_boards_research.md`.

---

## 1. Summary of Findings

### Core principle

C-bet frequency in 3-way pots is not a single number. It varies by a factor of 2-3x depending
on board texture. The existing KB gives an aggregate of ~43% (GTO Wizard: HU drops ~11pp to
~43% in 3-way). This research shows the range behind that average spans from roughly 20-25%
on the worst textures (low connected rainbow) to 65-70% on the best (A-high dry rainbow).

### Five headline findings

1. **A-high dry boards are the PFA's best c-bet texture.** Frequency approaches HU levels
   (~60-70%). The raiser's uncapped range (AK, AQ, AA) dominates both callers who lack
   these combos structurally.

2. **Low connected boards (5-4-2, 7-6-4) are the worst PFA c-bet textures.** Frequency
   drops to ~20-25%. Both callers' speculative ranges (BTN suited connectors, BB small pairs
   and connectors) interact heavily while the PFA's broadway-heavy range misses.

3. **Flush danger suppresses c-betting more than straight danger does.** Monotone boards
   reduce c-bet frequency by approximately 15-25 percentage points vs rainbow equivalents.
   Two-tone boards reduce frequency by ~5-10pp. Straight danger matters less because
   straight draws are less frequent in ranges and less visible on the board.

4. **Paired boards increase c-bet frequency.** The PFA's overpair combos dominate paired
   boards. Neither caller holds the pair (they would 3-bet AA/KK/QQ). Frequency on paired
   boards is higher than on the equivalent non-paired texture.

5. **Board texture interacts differently with each hand class.** Air (no pair, no draw)
   should almost never c-bet on any texture; the suppression is in value hands betting less
   often, not in bluffs. Made hands (top pair or better) adjust c-bet frequency based on
   whether the board connects with caller ranges. Draws follow the nut-potential filter.

---

## 2. Detailed Findings with Sources

### 2.1 A-High Dry / Rainbow Boards

**Examples:** A-7-2r, A-K-5r, A-J-3r

**C-bet frequency (3-way, PFA):** ~60-70% (highest tier)

**Source 1:** GTO Wizard, "Playing In Position Against Two Callers"
(https://blog.gtowizard.com/playing-in-position-against-two-callers/)
> Data point: On ace-high dry rainbow boards, the PFA retains the strongest nut advantage
> of any texture. Neither the BTN flat (capped, no AA/AK) nor the BB overcaller (wide but
> no premiums via squeeze) can hold AA or AK at comparable frequency. The solver concentrates
> c-betting here.
> Implication: Ace-high dry rainbow = bet. Frequency ~60-70% justified even 3-way because
> nut advantage compensates for the multiway fold equity reduction.

**Source 2:** poker.pro, "CO vs BTN Flat in 6-Max Cash"
(https://www.poker.pro/strategy/how-to-play-one-of-the-most-annoying-spots-in-6-max-cash-games-co-vs-btn-flat/)
> Data point: On A-K-x rainbow boards, solver supports 50-66% c-bet sizing (larger than
> usual for multiway) when PFA holds AK, AA, or KK. The nut advantage justifies sizing up.
> Implication: A-high boards are the one multiway texture where large-ish sizing (not just
> 25-33%) is defensible.

**Source 3:** 888poker, "Flop C-Betting Textual Theory"
(https://www.888poker.com/magazine/flop-cbetting-textual-beginner-theory)
> Data point: High-card static boards are where "when hand values are static, sizing up
> turns your structural edge into chips." Ace-high and king-high boards with no flush or
> straight draw qualify as the clearest static textures.
> Implication: These boards also justify small-to-medium sized bets with the full value
> range (TPTK+, all overpairs) for protection and thin value.

**Source 4:** SplitSuit, "Continuation Betting In Multi-Way Pots"
(https://www.splitsuit.com/cb-in-multi-way-pots)
> Data point: "On a dry, rainbow board like A-7-2, the preflop raiser has a clear range
> advantage. Their Ace-x combos far outnumber the callers'. This is the best spot to
> continuation bet in multi-way pots."
> Implication: Even with weak Ace holdings (A5s type), a small c-bet on A-high dry boards
> is profitable because the folding range is wide enough.

**Why the nut advantage is so clean here:**
- CO opens: AA (6 combos), AKs (4), AKo (12), AQs (4), AQo (12), AJs (4) ... ~40+ strong Ax combos
- BTN flat: No AA/KK/QQ/AKs. A2s-A5s (suited) present but no AK/AQ off. ~8-10 Ax combos total
- BB overcall: Wide but capped. Suited Ax present but no AK/AQ type. ~10-12 Ax combos
- PFA's Ax combos outnumber each caller by 3-4x. This is the most pronounced range edge in poker.

---

### 2.2 King-High Dry / Rainbow Boards

**Examples:** K-8-3r, K-7-2r, K-T-4r

**C-bet frequency (3-way, PFA):** ~50-60%

**Source 1:** GTO Wizard, "Monkey in the Middle: 3-Way Pot Heuristics"
(https://blog.gtowizard.com/monkey-in-the-middle-3-way-pot-heuristics/)
> Data point: On K-7-2r, BB folds ~68% to a 1/4 pot c-bet. BTN is harder to move (condensed
> range hits Kx too), but the combined fold equity from both opponents is still profitable.
> Implication: K-high dry boards support a high c-bet frequency but less aggressively than
> A-high boards. BTN's KTs and KJs are in calling range.

**Source 2:** GTO Wizard, "Playing In Position Against Two Callers"
> Data point: On king-high boards, PFA has KK (the nuts on a non-paired board), AK (top
> pair top kicker), and QQ+ (overpairs). BTN flat has no KK, no AK. BB has no KK.
> Implication: PFA still has nut advantage but it is less one-sided than on ace-high boards.
> BTN's KTs/KJs are genuine Kx hands that interact with the board.

**Source 3:** poker.pro, "Multiway Muscle: Big-Bet Windows"
(https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/)
> Data point: K-high dry boards are listed as supporting ~50-70% value betting frequency.
> The raiser's premium pairs dominate vs neither caller holding KK.
> Implication: K-high boards are the second-best texture for PFA c-betting, but frequency
> should be ~10pp lower than A-high due to BTN's more competitive Kx holdings.

---

### 2.3 Paired Boards

**Examples:** K-K-5r, A-A-7r, Q-Q-4r, T-T-3r, 7-7-2r

**C-bet frequency (3-way, PFA):** ~55-65% (higher than non-paired equivalents)

**Source 1:** GTO Wizard, "Playing In Position Against Two Callers"
> Data point: The article notes that on K-K-7r, solver c-bet frequency is very high (~96%
> noted for HU; multiway "still high"). The raiser has all overpairs (AA, QQ, JJ, TT etc.)
> and the callers' pair-heavy ranges are dominated because their pairs lose to the board
> pairing -- middle pair on K-K-7 is now a very weak hand.
> Implication: Paired boards dramatically thin out callers' legitimate continuing hands.
> The PFA can bet wider because the callers' default "I have a pair" holdings are
> devalued. Neither BTN flat nor BB overcaller holds KK (they would have 3-bet/squeezed).

**Source 2:** poker.pro, "Multiway Muscle: Big-Bet Windows"
> Data point: "Board pairs on turn" is listed as a big-bet window in multiway pots. The
> principle extends to flops: when the board pairs, overpair holders (primarily the PFA)
> gain disproportionate value.
> Implication: On a paired board, the PFA can c-bet with their full overpair range plus
> some Ax hands (on AA-x boards). Sizing can be medium (~40-50% pot) rather than always
> 25-33%.

**Source 3:** Upswing Poker, "4 Ways to Improve Your Results in Multi-Way Pots"
(https://upswingpoker.com/multiway-pots-tips/)
> Data point: Paired boards significantly reduce callers' two-pair density. Two-pair
> requires two specific rank cards; paired boards pre-use one rank.
> Implication: Callers cannot make two-pair as easily, so the board is more static for
> made hands. PFA's overpairs are safer to bet for value.

**Source 4:** GTO Wizard, "10 Tips for Multiway Pots in Poker"
(https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/)
> Data point: "Betting frequencies in multiway pots strongly correlate with nut advantage."
> Paired boards give PFA a clear nut advantage: only PFA's range contains the hand that
> beats the board on a paired texture (overpairs are now effectively the best-possible
> non-set hand because neither caller holds the pair).
> Implication: Paired boards are among the best multiway c-bet textures.

---

### 2.4 Low Connected Boards (Rainbow)

**Examples:** 5-4-2r, 7-6-4r, 8-5-3r, 6-4-2r

**C-bet frequency (3-way, PFA):** ~20-30% (lowest tier, check-heavy)

**Source 1:** GTO Wizard, "Monkey in the Middle: 3-Way Pot Heuristics"
(https://blog.gtowizard.com/monkey-in-the-middle-3-way-pot-heuristics/)
> Data point: Low connected boards ("764r, T86") where BTN flat range is dense with suited
> connectors produce the strongest caller resistance. BTN "never folds a flush draw or an
> open-ended straight draw" and these boards give BTN both types regularly.
> Implication: PFA c-bet frequency drops sharply. Even with top pair (8-5-3, PFA has 98s),
> the callers' draws are too good to fold, making pot control correct.

**Source 2:** GTO Wizard, "Probing Out Of Position in 3-Way Pots"
(https://blog.gtowizard.com/probing-out-of-position-in-3-way-pots/)
> Data point: On low-connected boards (e.g., T-7-5), BB develops a nut advantage via
> their own suited connectors and small pairs making two-pair, sets, and straights. BB's
> range "depends on a texture-changing turn to develop a betting range" but on the flop
> itself is a check-call range.
> Implication: Even PFA's weakest opponents (BB) have significant equity on low connected
> boards. Combined with BTN's connected range, PFA is in the worst possible range
> interaction. C-bet frequency should be the lowest of any texture type.

**Source 3:** SplitSuit, "Continuation Betting In Multi-Way Pots"
> Data point: "On a connected board like 8-7-6, there's no range advantage for anyone.
> The preflop raiser has missed this board. Their broadway range has limited interaction.
> Check more than 70% of the time."
> Implication: Low/mid connected boards with no high card directly confirm a check-heavy
> strategy for PFA. Frequency ~20-30% only with genuine value hands that smash the board
> (AA, 87s for two-pair, 66 for middle set).

**Source 4:** Phil Galfond, "Mastering Multi-Way Pots"
(https://www.philgalfond.com/articles/mastering-multi-way-pots)
> Data point: "Your threshold for putting in big bets on the flop should go way up. Only
> bet with huge hands like sets and some nut flush draws."
> Implication: On low connected boards, even TPTK (PFA with 98s on 9-8-3 for example) is
> not a c-bet. Only two-pair, sets, and occasional nut-draw semi-bluffs justify betting.
> The board structure defeats range advantage.

**Source 5:** Cardquant, "How to Evaluate Straight Draws in Multiway Pots"
(https://cardquant.com/beyond-the-solvers-how-to-evaluate-straight-draws-in-multiway-pots/)
> Data point: On 6-4-2 and similar low-card coordinated boards, the combined caller range
> (BTN + BB) contains a disproportionate number of straight draws, pair+draw combos, and
> made two-pair hands. The PFA's broadway-heavy range "misses entirely."
> Implication: PFA should default to check-fold on these boards with most of their range.
> The one exception is when PFA holds a set (KK on K-4-2, 22 on 5-4-2).

---

### 2.5 Middle Connected Boards

**Examples:** T-8-6r, J-9-7r, 9-7-5r, T-9-6r

**C-bet frequency (3-way, PFA):** ~30-40%

**Source 1:** GTO Wizard, "Playing In Position Against Two Callers"
> Data point: On T-7-4tt (similar to middle connected two-tone), BTN folds significantly
> less (~55% stay in) than on K-7-2r (~32% stay in). The connected texture gives BTN
> too many continuing hands to fold to a small c-bet.
> Implication: Middle connected boards where BTN's suited connectors (T9s, 98s, 87s)
> interact directly suppress c-betting. PFA frequency ~30-40%, betting only with genuine
> two-pair+ or nut draw-type hands.

**Source 2:** poker.pro, "CO vs BTN Flat"
> Data point: BTN flat range is described as "dense with suited connectors, offsuit broadway
> combinations, and pocket pairs -- hands that interact heavily with" mid-connected textures.
> Implication: The PFA's range does contain some hands that connect (JJ for two-pair on
> J-9-7, ATs for nut flush draw on T-8-6ss), but the base rate is much lower than on
> high-card boards. Default is check-heavy.

---

### 2.6 Effect of Flush Danger (Flush_Danger Feature)

**How flush danger manifests:** Two suited cards on the flop (two-tone) vs three suited
cards (monotone).

#### Two-tone boards

**C-bet frequency reduction vs rainbow:** ~5-10 percentage points

**Source 1:** GTO Wizard, "Playing In Position Against Two Callers"
> Data point: On T-7-4tt (two-tone), BB folds ~45% vs ~68% on K-7-2r (rainbow). The
> flush draw kept in BB's range materially reduces fold equity.
> Implication: On two-tone boards, PFA must tighten c-bet range because BTN and BB both
> have flush draw equity that prevents folding. Small sizing still works but frequency
> is reduced.

**Source 2:** Upswing Poker, "Flush Draws as Preflop Caller"
(https://upswingpoker.com/flush-draws-preflop-caller/)
> Data point: "BTN never folds a flush draw or an open-ended straight draw" in 3-way pots.
> Two-tone boards give BTN flush draws more often from suited connectors.
> Implication: Two-tone boards featuring a suit that overlaps with BTN's calling range
> (hearts and spades are most common in BTN's suited connectors) are particularly bad
> c-bet textures because BTN becomes inelastic -- calling regardless of sizing.

**Source 3:** GTO Wizard, "Crack the Shell of Nut Draw Strategy"
(https://blog.gtowizard.com/crack-the-shell-of-nut-draw-strategy/)
> Data point: On Q-6-2 two-tone, CO c-bets nut flush draws 69% HU. The implication for
> multiway is that the PFA wants to c-bet when THEY hold the nut flush draw (to deny
> callers' backdoor equity), but c-betting into callers who HAVE flush draws is much less
> profitable.
> Implication: When PFA holds the nut flush draw, two-tone boards are still decent c-bet
> spots (semi-bluff with nut draw + nut blocker applies). When PFA does not hold the nut
> flush draw on a two-tone board, c-bet frequency is suppressed because callers will not
> fold their draws.

#### Monotone boards

**C-bet frequency reduction vs rainbow:** ~15-25 percentage points

**Source 1:** GTO Wizard, "10 Tips for Multiway Pots in Poker"
> Data point: Monotone boards are cited as the most extreme case of the "stop range-betting"
> principle. Every player holding a suited card has flush draw equity. PFA can only c-bet
> when they have the nut flush draw or a made hand that is already ahead of flush draws.
> Implication: Monotone boards suppress PFA c-betting to the lowest feasible frequency.
> Only sets, two-pair (as protection against draws), and nut flush draws justify betting.

**Source 2:** Phil Galfond, "Mastering Multi-Way Pots"
> Data point: "Only bet with huge hands like sets and some nut flush draws" applies most
> forcefully on monotone boards where everyone has flush equity.
> Implication: On a 9s-7s-4s board (monotone), PFA c-bets only with the nut flush
> (AsXs) or a set. Everything else checks. Frequency ~20-30% at most.

**Source 3:** GTO Wizard, "Probing Out Of Position in 3-Way Pots"
> Data point: Monotone boards dramatically increase BB's nut advantage on subsequent streets.
> Even weak suited hands (small flush draws) have significant equity on monotone boards.
> Implication: Against BB's wide calling range, a disproportionate fraction holds suited
> cards. On a monotone board, this fraction has connected to a flush draw. PFA c-bets into
> a range full of draws, dramatically reducing the profitability.

**Summary table for flush_danger:**

| Flush Danger Level | Board Type | C-Bet Frequency Delta vs Rainbow |
|-------------------|------------|----------------------------------|
| 0 (rainbow) | A-7-2r | Baseline (no reduction) |
| 1 (two-tone) | A-7-2ss | -5 to -10pp |
| 2 (monotone) | 9s-7s-4s | -15 to -25pp |

**Source:** Synthesized from GTO Wizard (multiple articles), Upswing, and Galfond above.

---

### 2.7 Effect of Straight Danger / Board Connectivity

**C-bet frequency reduction:** Graduated by connectivity level

**Source 1:** GTO Wizard, "Monkey in the Middle: 3-Way Pot Heuristics"
> Data point: On T-7-4tt (connectivity score: moderate) vs K-7-2r (disconnected): BTN
> stays in far more often on the connected board. The implication is that connectivity
> suppresses c-betting even on non-flush boards.
> Implication: Each "point" of board connectivity (i.e., whether the board allows straight
> draws for the callers' ranges) reduces c-bet frequency.

**Source 2:** Cardquant, "How to Evaluate Straight Draws in Multiway Pots"
> Data point: "When a board texture allows multiple straight draw combinations for the
> callers, the preflop raiser's c-betting range must contract." On J-T-8, T-8-6, 9-7-5,
> both BTN and BB have significant OESD and gutshot equity.
> Implication: High connectivity boards (straight_danger > 0.5 in pipeline terms) suppress
> PFA c-bet frequency significantly. Even with top pair on J-T-8, there are too many draws
> to bet without a strong hand.

**Source 3:** GTO Wizard, "Playing In Position Against Two Callers"
> Data point: On the highly connected board T-8-6 with two flush draws possible, the PFA
> should check 60-65% of their range. Only sets and nut hands justify betting.
> Implication: High connectivity + flush draw is the worst combination for PFA c-betting.
> The board hits BTN's entire suited connector range.

**Straight danger gradient:**

| Connectivity Level | Example | Approximate PFA C-Bet Frequency |
|-------------------|---------|----------------------------------|
| 0.0 (none) | A-7-2r | ~60-70% |
| 0.25 (low) | K-8-3r | ~50-60% |
| 0.5 (moderate) | T-8-4r | ~35-45% |
| 0.75 (high) | J-9-7r | ~25-35% |
| 1.0 (very high) | T-9-8r, 9-8-7 | ~20-30% |

These are estimates derived from the direction and magnitude of findings across sources.
No single source provides a clean table at these exact connectivity levels.

---

### 2.8 High Card vs Low Card Boards

**High card = at least one A, K, or Q on the flop.**
**Low card = highest card is 9 or lower.**

**C-bet frequency difference:** ~20-30 percentage points

**Source 1:** GTO Wizard, "Playing In Position Against Two Callers"
> Data point: The PFA's range is "dominated" on high-card boards (A/K-high) and
> "disadvantaged" on low-card boards (below 9-high). The article specifically notes the
> range morphology difference: PFA opens broadway-heavy, so high boards hit; callers flat
> connector-heavy, so low boards hit.
> Implication: A high-card board effectively reverses the structural disadvantage of c-
> betting into two callers. A low-card board amplifies it.

**Source 2:** Upswing Poker, "When Should You Bet the Flop in Multi-Way Pots?"
(https://upswingpoker.com/multiway-pots-flop-bet-strategy/)
> Data point: PFA should c-bet less on "coordinated low boards" and more on "high-card
> boards that interact with the PFA's opening range." The frequency difference is described
> as "dramatic."
> Implication: The high/low card distinction is the single biggest binary split for PFA
> c-bet frequency, even above flush/straight danger.

**Source 3:** MyPokerCoaching, "Multiway Pots Strategy Tips"
(https://www.mypokercoaching.com/multiway-pots-strategy-tips/)
> Data point: On low boards, PFA's "broadway range has limited interaction" while callers'
> suited connectors "interact heavily." On high boards, the reverse. C-bet frequencies on
> low boards: ~25-35%. High boards: ~50-65%.
> Implication: The highest-quality heuristic for PFA c-betting is board height (top card).
> Below 9: default check. At/above K: default bet (with adjustments for texture).

**Source 4:** SplitSuit, "Continuation Betting In Multi-Way Pots"
> Data point: "The higher the top card, the better for the preflop raiser." This is the
> most concise statement of the high/low card principle. Low boards (7-high, 8-high) give
> PFA almost nothing to work with.
> Implication: Low boards should trigger check-heavy defaults for the model's BET decision.

---

### 2.9 How Texture Interacts with Hero's Hand Class

This section synthesizes how PFA's specific holdings interact with each texture. The key
insight from GTO Wizard: "Betting frequencies in multiway pots strongly correlate with
nut advantage." The question for each hand class is: does this hand have nut advantage on
this texture?

#### Air (no pair, no draw — pure miss)

**C-bet frequency: ~0-5% on ALL textures**

**Source:** GTO Wizard, "10 Tips for Multiway Pots in Poker"; Phil Galfond, "Mastering
Multi-Way Pots"; Upswing, "7 Multiway Tactics"
> Consensus: Pure bluffs are "ineffective multiway." With the exception of the river, never
> bluff without solid drawing equity. Air hands should not c-bet on any texture.
> Implication: The texture suppression of air is absolute, not graded. A-high on 8-6-3 is
> a check; A-high on A-7-2 is TPTK, not air (it's now a value hand). Pure air means the
> board hit nothing in PFA's hand.

#### Draws (flush draw, straight draw)

**C-bet frequency by texture: Varies based on draw quality + texture combination**

**Source 1:** GTO Wizard, "Crack the Shell of Nut Draw Strategy"
> Data point: Nut flush draws c-bet at ~69% HU, lower multiway. The multiway reduction
> is board-texture dependent: on a board where the nut flush draw aligns with PFA's range
> advantage (e.g., AsXs on a spade board where A-high favors PFA), c-bet frequency stays
> relatively high (~50-60%). On a board where the texture favors callers, even nut draws
> should check.
> Implication: Nut draw + favorable board texture = c-bet (semi-bluff with backup). Nut
> draw + unfavorable texture = check-call or check (let others drive action).

**Source 2:** Upswing Poker, "How to Play Nut Flush Draws in Cash Games"
(https://upswingpoker.com/nut-flush-draws/)
> Data point: On A-Q-8 two-tone, K-7 suited (nut flush draw) is a strong bet/raise
> candidate. On low boards like 8-4-2 two-tone, even a nut flush draw should check-call
> more because the board structure doesn't help PFA's range.
> Implication: The texture determines whether the nut draw's semi-bluff value is realized.
> High board + nut draw = c-bet. Low board + nut draw = check-call (let the board tell
> you if the fold equity is there).

**Source 3:** Cardquant, "Straight Draws in Multiway Pots"
> Data point: Non-nut straight draws (OESDs that aren't the nut OESD) should check-call
> on most textures. Only the nut straight draw on a board where PFA has range advantage
> can semi-bluff.
> Implication: Straight draw c-bets are rarely correct for PFA in 3-way. The nut potential
> filter (from existing KB Section 1.7) applies here.

#### Top pair (TPTK, TPGK, top pair weak kicker)

**C-bet frequency by texture: Strong texture dependence (30-70% range)**

**Source 1:** GTO Wizard, "Playing In Position Against Two Callers"
> Data point: TPTK on A-high dry = c-bet at high frequency (~65-70%). TPTK on T-8-6 =
> check. The same hand (top pair top kicker in both cases) has dramatically different
> c-bet frequency depending on whether the texture favors PFA or the callers.
> Implication: Top pair's c-bet decision is almost entirely determined by board texture
> in 3-way. On good textures (A/K-high dry): bet. On bad textures (low/connected): check.

**Source 2:** Phil Galfond, "Mastering Multi-Way Pots"
> Data point: "Your threshold for putting in big bets on the flop should go way up. But
> you should use bigger bet sizes and only bet with huge hands like sets and some nut flush
> draws." TPTK does not meet this threshold on most textures except A/K-high dry.
> Implication: On dynamic, connected, or flush-dangerous textures, TPTK should check even
> though it would bet HU. The hand shifts from value hand to pot-control hand.

**Source 3:** GTO Wizard, "10 Tips for Multiway Pots"
> Data point: The article explicitly states "top pair is a medium-strength hand multiway."
> The correct action on a board that favors callers is check, not bet, with top pair.
> Implication: Top pair can only c-bet on the best textures (A-high dry, K-high dry,
> paired boards) where callers lack the connectivity to continue profitably.

#### Two-pair and sets (strong made hands)

**C-bet frequency: High (~70-85%) across most textures, with sizing adjustment**

**Source 1:** GTO Wizard, "10 Tips for Multiway Pots"
> Data point: "Must bet monster" principle (also in existing KB Example 4). Sets must bet
> multiway because two opponents drawing means free card risk doubles.
> Implication: Sets c-bet at very high frequency regardless of texture. The only question
> is sizing. On dynamic boards (more draws in callers' ranges), bet larger to deny equity.
> On static boards, smaller sizing is fine.

**Source 2:** Upswing Poker, "7 Multiway Tactics"
> Data point: Two-pair and sets are the hands that justify medium-to-large bet sizing
> multiway. These are the hands where protection (denying free cards to draws) outweighs
> deception value from slowplaying.
> Implication: On connected/flush-dangerous boards, sets should bet larger (50-66% pot)
> to make draws pay. On dry boards, smaller (33-40%) extracts value without over-charging.

---

## 3. Board Texture Classification for the BET Decision Tree

This section provides a structured classification of board textures for the model's
c-bet decision. It integrates findings above into a tiered system.

### Tier 1: HIGH C-Bet Frequency (60-70%)
C-bet with top pair or better as default. Air checks. Draws check or bet based on nut quality.

| Texture | Features | Why High |
|---------|----------|----------|
| A-high rainbow dry | High card + zero flush/straight danger | PFA dominant nut advantage; callers lack Ax |
| K-high rainbow dry | High card + zero flush/straight danger | PFA still has best Kx combos; callers capped |
| Paired board (A-A-x, K-K-x) | Paired + high card + low danger | Callers cannot hold the paired rank; PFA overpairs dominate |
| A-high two-tone (PFA has nut FD) | High card + flush danger but PFA holds it | PFA's nut advantage intact; semi-bluff valid |

### Tier 2: MODERATE C-Bet Frequency (40-55%)
C-bet with top pair+ when callers' continuing range is limited. Check marginal hands.

| Texture | Features | Why Moderate |
|---------|----------|--------------|
| Q-high or J-high rainbow dry | High-ish card, low connectivity | PFA has range edge but less extreme; BTN has JTs/QJs in range |
| K-high two-tone | High card, some flush danger | PFA has range advantage but flush draw reduces fold equity ~5-10pp |
| Paired board (T-T-x, 8-8-x) | Mid paired | PFA's overpairs dominate but texture is less cleanly static |
| A-high/K-high low connectivity | High card + connectivity score 0.25-0.5 | Straight draw equity for callers partially offsets high-card edge |

### Tier 3: LOW C-Bet Frequency (25-40%)
Check with most hands. Bet only with strong made hands (two-pair, sets) or nut draw.

| Texture | Features | Why Low |
|---------|----------|---------|
| Mid-high connected rainbow | Connectivity 0.5-0.75 + low flush danger | BTN suited connectors interact directly; fold equity collapses |
| K-high or Q-high two-tone + connected | High card + flush + straight danger | Both danger types active; callers have FDs + straight draws |
| Low-card rainbow moderately connected | Top card below J, connectivity 0.25-0.5 | PFA's range misses; callers' ranges connect |
| Any monotone board | Maximum flush danger | Every caller with suited cards has a FD; fold equity near zero |

### Tier 4: VERY LOW C-Bet Frequency (15-25%)
Default check. Only c-bet with sets, top two-pair, or nut flush draw with blocker.

| Texture | Features | Why Very Low |
|---------|----------|--------------|
| Low connected rainbow | Top card 9 or lower, connectivity 0.75+ | Worst texture for PFA; BTN + BB ranges hit directly |
| Low connected two-tone | Low card + flush danger | Double disadvantage; PFA's range misses everything |
| Any mid/low monotone | Monotone + middle/low board | Callers have FDs everywhere; PFA at structural disadvantage |
| 5-4-2, 6-4-2, 7-5-3 type | Very low, very connected | Both callers' ranges have two-pair, sets, straights, and draws |

### Decision Logic Summary

The primary split (ordered by importance):

1. **Top card height** — Highest impact. A/K = favor bet. 7/8/9 or lower = favor check.
2. **Flush danger** — Second highest. Rainbow = baseline. Two-tone = reduce. Monotone = strong reduction.
3. **Straight danger** — Third. Disconnected = baseline. Connected = reduce. Very connected = strong reduction.
4. **Board paired** — Shifts upward from non-paired baseline by ~10pp for PFA.
5. **PFA's specific hand** — Sets/two-pair: bet on all textures (adjust size). Top pair: only bet on Tier 1-2 textures. Draws: nut draw + Tier 1-2 texture = semi-bluff. Air: never bet.

---

## 4. Contradictions and Gaps

### 4.1 Contradictions

**Contradiction 1: "Always small multiway" vs "Large sizing on Tier 1 textures"**

The existing KB (Section 1.3) states "Default sizing when betting: Small (25-33% pot)."
The research in Section 2.1 and poker.pro's "Big-Bet Windows" shows that A-high dry boards
and A-K-x boards support 50-66% sizing for the PFA. These are not truly contradictory —
the existing KB notes "Range-betting is never correct 3-way" and the big-bet windows are
specific exceptions — but the framing can mislead. The KB should clarify: "25-33% is the
default when you have range advantage but limited nut advantage; larger sizing is correct
when nut advantage is clear (A-high dry, paired boards)."

**Contradiction 2: Frequency numbers are not in full agreement between sources**

GTO Wizard (via 3way_ranges_boards_research) reports BTN folds ~32% on K-7-2r to a 1/4
pot bet. SplitSuit describes checking >70% on connected boards. These are consistent with
each other directionally but the exact frequency numbers vary across sources because they
use different stake sizes, positions, and configurations. No two sources were measured on
identical setups.

**Contradiction 3: Semi-bluff with NFD OOP in 3-way**

The existing KB (Section 1.7, Example 9) says to RAISE with nut flush draw + blocker OOP.
This research (Section 2.9, draws section) says the texture must also be favorable. These
are reconcilable: the MW-47 pattern applies when the board is already favorable for PFA
(K-J-5 with spade two-tone is still a high-card board). But on a low connected two-tone
board, even a nut flush draw + blocker may not have sufficient fold equity to raise OOP.
The existing KB does not explicitly state this texture dependency. It's a gap worth noting.

### 4.2 Gaps

**Gap 1: Exact frequency numbers by texture from a single solver configuration**

No public source provides a clean table: "A-high dry: 68%, K-high dry: 57%, low connected:
24%" from a single solver run. All numbers in this research are synthesized from directional
findings, quoted frequency comparisons (e.g., "BB folds 68% vs 45%"), and qualitative
statements. The exact frequencies are robust directionally but the precise numbers should
be treated as estimates, not solver outputs.

**Gap 2: Queen-high boards are underrepresented**

Q-high boards appear rarely in the source material. They sit between K-high (well-covered)
and J-high (less covered) and have a different range interaction because QQ/KK/AA (PFA's
combos) all make overpairs but Q-J-x and Q-T-x are much more connected than K-8-x.
The model will need to handle Q-high boards by interpolating between K-high and J-high
estimates. No solver-specific data found for Q-high 3-way c-bet frequencies.

**Gap 3: Texture interaction with 3-bet pots**

All research is for single-raised pots (SRP). In 3-bet pots, the c-bet frequency profile
changes significantly because SPR is lower and ranges are narrower/stronger. The pipeline
features include pot size information, but no source in this research specifically addresses
board texture effects on c-bet frequency in 3-way 3-bet pots. This is a gap for the model
if it encounters 3-way 3-bet scenarios.

**Gap 4: Turn and river texture dynamics**

This research focuses on flop c-bet decisions. The texture of the turn and river (e.g., how
a completing flush turn or pairing turn changes c-bet frequency) is addressed only briefly in
the existing KB (big-bet windows section). A dedicated turn texture research pass would help.

**Gap 5: OOP PFA-specific frequency numbers**

When the PFA is OOP (e.g., HJ opens, CO and BTN call, or UTG opens multiway), the
c-bet frequency profile should be more conservative than when IP. The research is primarily
from IP PFA configurations. The directional finding (OOP reduces frequency) is clear but
specific OOP frequency numbers by texture are not available in public sources.

---

## 5. Source Index

| # | Source | URL | Type | Key Finding |
|---|--------|-----|------|-------------|
| 1 | GTO Wizard — Playing In Position Against Two Callers | https://blog.gtowizard.com/playing-in-position-against-two-callers/ | Solver-based | Board texture frequency data; K-7-2r vs T-7-4tt fold comparisons |
| 2 | GTO Wizard — Monkey in the Middle: 3-Way Heuristics | https://blog.gtowizard.com/monkey-in-the-middle-3-way-pot-heuristics/ | Solver-based | Low connected boards; BTN never folds FD/OESD; fold equity collapse |
| 3 | GTO Wizard — 10 Tips for Multiway Pots | https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/ | Solver-based | Nut advantage drives frequency; stop range-betting; 33% avg pot share |
| 4 | GTO Wizard — Crack the Shell of Nut Draw Strategy | https://blog.gtowizard.com/crack-the-shell-of-nut-draw-strategy/ | Solver-based | NFD c-bet frequency 69% HU on Q-6-2; multiway reduction |
| 5 | GTO Wizard — Probing Out Of Position in 3-Way Pots | https://blog.gtowizard.com/probing-out-of-position-in-3-way-pots/ | Solver-based | BB nut advantage on low boards; monotone board effects |
| 6 | GTO Wizard — Preflop Range Morphology | https://blog.gtowizard.com/preflop-range-morphology/ | Solver-based | Range shapes; linear/condensed/capped definitions |
| 7 | poker.pro — Multiway Muscle: Big-Bet Windows | https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/ | Solver-based | A/K-high and paired boards support larger sizing; 50-90% pot windows |
| 8 | poker.pro — CO vs BTN Flat in 6-Max Cash | https://www.poker.pro/strategy/how-to-play-one-of-the-most-annoying-spots-in-6-max-cash-games-co-vs-btn-flat/ | Solver-based | BTN condensed range hits mid-connected boards; frequency guidance |
| 9 | Phil Galfond — Mastering Multi-Way Pots | https://www.philgalfond.com/articles/mastering-multi-way-pots | Solver-based | "Only bet sets and nut flush draws" on most textures; small sizing default |
| 10 | SplitSuit — Continuation Betting In Multi-Way Pots | https://www.splitsuit.com/cb-in-multi-way-pots | Solver-informed | A-7-2 = best c-bet texture; 8-7-6 = check >70%; high card = higher frequency |
| 11 | Upswing Poker — When Should You Bet the Flop in Multi-Way Pots | https://upswingpoker.com/multiway-pots-flop-bet-strategy/ | Solver-informed | High-card boards vs coordinated low boards; "dramatic" frequency difference |
| 12 | Upswing Poker — Flush Draws as Preflop Caller | https://upswingpoker.com/flush-draws-preflop-caller/ | Solver-informed | BTN never folds FD; two-tone boards make BTN inelastic |
| 13 | Upswing Poker — How to Play Nut Flush Draws in Cash Games | https://upswingpoker.com/nut-flush-draws/ | Solver-informed | NFD on A-Q-8 = strong bet; on low boards = check-call |
| 14 | Upswing Poker — 4 Ways to Improve in Multi-Way Pots | https://upswingpoker.com/multiway-pots-tips/ | Solver-informed | Paired boards reduce callers' two-pair density; overpairs safer to bet |
| 15 | Upswing Poker — 7 Multiway Tactics | https://upswingpoker.com/multiway-pot-concepts/ | Solver-informed | "Enemy unit" concept; only sets and nut draws for large bets |
| 16 | Cardquant — Straight Draws in Multiway Pots | https://cardquant.com/beyond-the-solvers-how-to-evaluate-straight-draws-in-multiway-pots/ | Solver-informed | Connectivity level determines caller resistance; 6-out draws stop calling when bet+call |
| 17 | MyPokerCoaching — Multiway Pots Strategy Tips | https://www.mypokercoaching.com/multiway-pots-strategy-tips/ | Theoretical/solver-informed | High boards ~50-65% c-bet; low boards ~25-35% |
| 18 | 888poker — Flop C-Betting Textual Theory | https://www.888poker.com/magazine/flop-cbetting-textual-beginner-theory | Theoretical | Static vs dynamic board distinction; sizing up on static boards |

