# How to Play Draws in Multiway Pots: Research Summary

## Sources

1. **GTO Wizard -- 10 Tips for Multiway Pots**: https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/
2. **GTO Wizard -- Crack the Shell of Nut Draw Strategy**: https://blog.gtowizard.com/crack-the-shell-of-nut-draw-strategy/
3. **GTO Wizard -- The Trouble With Implied Odds**: https://blog.gtowizard.com/the-trouble-with-implied-odds/
4. **GTO Wizard -- Visualizing Implied Odds**: https://blog.gtowizard.com/visualizing-implied-odds/
5. **GTO Wizard -- Equity Realization**: https://blog.gtowizard.com/equity-realization/
6. **GTO Wizard -- Betting Draws in Position: The Real Rules**: https://blog.gtowizard.com/betting-draws-in-position-the-real-rules/
7. **GTO Wizard -- Protect Equity and Prosper**: https://blog.gtowizard.com/protect-equity-and-prosper/
8. **GTO Wizard -- Playing In Position Against Two Callers**: https://blog.gtowizard.com/playing-in-position-against-two-callers/
9. **GTO Wizard -- Probing Out of Position in 3-Way Pots**: https://blog.gtowizard.com/probing-out-of-position-in-3-way-pots/
10. **Upswing Poker -- Flush Draws as Preflop Caller**: https://upswingpoker.com/flush-draws-preflop-caller/
11. **Upswing Poker -- How to Play Nut Flush Draws in Cash Games**: https://upswingpoker.com/nut-flush-draws/
12. **Upswing Poker -- Equity Realization Explained**: https://upswingpoker.com/equity-realization-explained/
13. **Upswing Poker -- How to Play Combo Draws in Cash Games**: https://upswingpoker.com/combo-draws/
14. **Upswing Poker -- Gutshot Straight Draws 101**: https://upswingpoker.com/gutshot-straight-draws-tips/
15. **Cardquant -- Straight Draws in Multiway Pots**: https://cardquant.com/beyond-the-solvers-how-to-evaluate-straight-draws-in-multiway-pots/
16. **Crush Live Poker -- Combo Draws Multiway**: https://crushlivepoker.com/articles/combo-draws-multiway
17. **Phil Galfond -- Mastering Multi-Way Pots**: https://www.philgalfond.com/articles/mastering-multi-way-pots
18. **Red Chip Poker -- Equity Realization**: https://redchippoker.com/equity-realization/

---

## 1. Fundamental Principle: Multiway Pots Demand Stronger Draws

### The Core Shift from Heads-Up to Multiway

**Source: GTO Wizard -- 10 Tips [1], Phil Galfond [17]**

- You do NOT need to defend nearly as wide in multiway as in heads-up. Defense burden is shared across multiple players.
- Your betting range must become much stronger -- stronger value bets AND stronger bluffs.
- Pure bluffs (no pair, no backdoors, no blockers) are ineffective multiway. With the exception of the river, almost never bluff without solid drawing equity.
- The more players acting behind you, the less profitable calling becomes, pushing strategy toward merged raises or folds -- not passive calls with weak draws.

**Key heuristic (Galfond [17]):** A single opponent flops worse than top pair without a strong draw 67% of the time. With four opponents, the chance that at least one has a strong hand rises dramatically.

---

## 2. Solver Frequencies for Flush Draws in 3-Way Pots

### Nut Flush Draws (NFD) -- Heads-Up Baseline

**Source: GTO Wizard -- Crack the Shell of Nut Draw Strategy [2]**

On Q-6-2 two-tone (100bb CO vs BB SRP):
- CO c-bets nut flush draws **69% of the time** (vs 49% overall c-bet frequency)
- CO checks nut flush draws **31% of the time**
- None of the NFD combos are pure bets -- all mix across multiple bet sizes
- Specific combo: A-8 suited performs ~6bb/100 better as a pure bet; A-3 suited has identical EV as bet or check (pure mix)

### Multiway Adjustments to Flush Draw Betting

**Source: Upswing Poker -- Flush Draws [10], GTO Wizard -- 10 Tips [1]**

In multiway pots, c-bet frequency drops significantly from the heads-up baseline:
- **8-high flush draws (e.g., 8s4s):** Bet far LESS frequently -- these are dominated flush draws with poor nut potential
- **King-high and Ace-high flush draws:** Bet far MORE frequently -- these have nut potential
- On A-Q-8 two-tone: K-7 suited (nut flush draw) is a strong bet/raise candidate; 6-4 suited (weak flush) is a check/fold candidate

**Frequency pattern multiway:**
- Nut flush draws: Bet/raise at moderate-to-high frequency (~50-70% depending on board)
- Second/third nut flush draws: Mix of check-call and occasional check-raise (~30-50% continue)
- Low flush draws (8-high or worse): Predominantly check-fold, occasionally check-call with additional equity (pair, backdoor straight)

### Check-Raise Frequencies with Flush Draws OOP

**Source: Upswing Poker -- Nut Flush Draws [11], Flush Draws as Caller [10]**

- Check-calling should be the MOST frequent play with a flush draw against a c-bet
- Check-raising is mixed in to balance the value range
- Solver check-raises about **33% less often** when facing larger bet sizes (more polarized ranges)
- Counter-intuitive: **Jack-high flush draws check-raise MORE often** than Ace-high flush draws
- Reason: Low-kicker NFDs (e.g., As3s on 9s7s2d) are better check-raise candidates than high-kicker NFDs (e.g., AsJs), because Js blocks opponent's lower flush draw calling range

---

## 3. Combo Draws vs Single Draws

### What Makes Combo Draws Special

**Source: Upswing Poker -- Combo Draws [13], Crush Live Poker [16]**

A combo draw has 12+ outs (flush draw + straight draw combined). Key properties:

- **Equity cannot be denied:** Combo draws realize equity very well because they are strong enough to call versus any raise size. There is no downside to playing them aggressively.
- **Semi-bluff priority:** When you must limit check-raise semi-bluffs multiway, combo draws make the cut while single flush draws often do not. "The majority of flush draws won't make the cut, but combo draws do." [10]
- **Pair + flush draw:** Middle or bottom pair + flush draw works well as a strong semi-bluff multiway, as you often have more outs against the PFR and are more likely to get paid when you hit trips.

### Hierarchy of Draw Aggression (Multiway)

**Source: GTO Wizard [1, 2], Upswing [10, 13]**

From most aggressive to most passive in multiway:

1. **Combo draws (flush + OESD): 12-15 outs** -- Bet/raise at high frequency. ~55-65% equity vs a single made hand. Can profitably call any raise size.
2. **Nut flush draw + gutshot: 12 outs** -- Strong semi-bluff candidate. Raise or bet at moderate frequency.
3. **Nut flush draw alone: 9 outs** -- Mix of bet, check-call, check-raise. IP: lean toward calling. OOP: lean toward check-raising with low kickers.
4. **Non-nut flush draw + overcards: 9+3 "discounted" outs** -- Check-call if nut potential exists; fold if dominated flush possible.
5. **Open-ended straight draw (OESD): 8 outs** -- Weaker multiway than heads-up. ~32% equity flop-to-river but only ~50% equity when hit 3-handed. Primarily check-call.
6. **Non-nut flush draw alone: 9 outs but dominated** -- Dangerous multiway. Check-fold most of the time.
7. **Gutshot alone: 4 outs** -- "Naked gutshots should quickly find their way to the muck in multiway pots." [14] Only continue with additional backdoor equity.

---

## 4. Equity Realization: IP vs OOP, Heads-Up vs Multiway

### Position Impact on EQR

**Source: Upswing Poker -- Equity Realization [12], GTO Wizard -- EQR [5]**

EQR = pot-share / raw equity. An EQR of 100% means you win exactly your fair share.

Concrete solver example (9s-3s-2d board, BB vs CO):
- **BB (OOP) realized only 79.1% of preflop equity**
- **CO (IP) realized 118.1% of preflop equity**
- This ~39 percentage point gap is the positional tax on equity realization

General patterns:
- **IP players regularly realize 110-130% of raw equity** by combining value betting, bluffing, and board coverage
- **OOP players typically realize 70-85% of raw equity** depending on board texture and range composition
- The higher the SPR, the more the IP player over-realizes and the more the OOP player under-realizes

### Draw-Specific EQR

**Source: GTO Wizard [5], Upswing [12], Red Chip [18]**

- **Flush draws IP:** Can over-realize equity (>100% EQR) because they benefit from "visibility" -- the ability to value bet or bluff on later streets depending on runout
- **Flush draws OOP:** Under-realize equity significantly; raw 35% equity may only realize ~25-28% pot share in practice
- **Suited connectors (e.g., 98s):** High degree of "robustness" -- realize much of their equity, often more than their fair share, because they frequently pick up weak draws that enable aggressive play
- **76s hits the flop 62.4% of the time** (some equity: pair, draw, or backdoor); 76o hits only 55.9% -- the suited component adds ~6.5% more flop connectivity

### Multiway Equity Realization Penalties

**Source: GTO Wizard [1, 5], Phil Galfond [17]**

- Equity retention plummets multiway because collective defense against large bets produces extremely strong continuing ranges
- Use smaller bet sizes multiway to preserve equity retention
- Draws with nut potential partially escape the multiway EQR penalty because they win the largest pots when they connect
- Non-nut draws suffer the worst EQR multiway: they under-realize on both the "miss" path (fold equity denied) and the "hit" path (lose to better made hands)

---

## 5. Implied Odds and Draws Multiway

### How Implied Odds Change Multiway

**Source: GTO Wizard -- Trouble With Implied Odds [3], Visualizing Implied Odds [4]**

Classic example: Holding 7c6c on As-Kh-8c-5d. Facing a $10 bet into $10 pot with 8 outs:
- Need 5.25:1 odds based on raw equity
- With $50 behind, effective odds become $70:$10 = 7:1 -- a profitable call

**Multiway dynamics:**
- Multiway pots increase BOTH implied odds AND reverse implied odds
- This effect is similar to deep-stacked pots -- more money can be won, but more can be lost
- To replicate solver EV gradients in multiway equity calculations, implied odds can be artificially increased by expanding the number of players considered
- Hands with better "visibility" and more paths to the nuts perform well -- nut potential is the key variable

### The Trouble

**Source: GTO Wizard [3]**

- Players began thinking in terms of "implied odds hands" as early as preflop -- calling with speculative hands expecting to get paid when they hit
- The trouble: implied odds are not free. You pay reverse implied odds when you hit a non-nut hand (e.g., make a flush but opponent has a higher flush)
- Multiway amplifies this problem: the more opponents, the higher the chance someone has a better draw or a set that fills up

---

## 6. Overcard Equity and Hidden Outs

### How Overcards Factor Into Draw Equity

**Source: GTO Wizard [1], Upswing [14], Misc search data**

- Random overcards have approximately a **25% chance to improve** (pair up) by the river
- In multiway, even AK on a low board can be behind the collective calling ranges
- Overcards add "discounted" outs to draws: typically count at 3 outs each (not full 6) due to the risk of being outkicked or facing two pair

### Backdoor Draw Equity Contributions

**Source: Cardplayer/backdoor research, GTO Wizard [1]**

| Draw Component | Added Equity |
|---|---|
| Backdoor flush draw alone | ~3-4% (~4.2% to complete) |
| Backdoor straight draw alone | ~2-3% |
| Two overcards alone | ~6% (3 discounted outs each) |
| Backdoor flush + two overcards | ~7-9% total |
| Backdoor straight + backdoor flush | ~6-8% total |

### When Overcards + Backdoors Save a Hand

**Source: GTO Wizard [1], Upswing [14]**

- In multiway, choose bluffs/semi-bluffs that have: nut-suit draws, backdoor straight draw + overcards that block opponent's strongest continues, or wheel backdoors on A-high boards
- A naked gutshot (4 outs) is a fold multiway. But gutshot + backdoor flush + overcard (~9-10 "partial" outs) can be a check-call
- The key threshold: a hand needs at minimum backdoor equity (flush or straight) plus some primary equity (pair, overcard, or frontdoor draw) to justify continuing multiway

---

## 7. Out Thresholds: From Check-Fold to Check-Call to Semi-Bluff

### Decision Matrix by Out Count (Multiway, Flop)

**Source: Synthesized from GTO Wizard [1, 2, 6], Upswing [10, 13, 14], Cardquant [15]**

| Outs | Draw Type Example | Multiway Action | Notes |
|---|---|---|---|
| 0-3 | No draw, pure air | CHECK-FOLD | Never bluff without drawing equity multiway |
| 4 | Naked gutshot | CHECK-FOLD | "Should quickly find way to the muck" [14]. Only exception: gutshot to the nuts with backdoor flush |
| 4+BD | Gutshot + backdoor flush/straight | CHECK-CALL (marginal) | Need the backdoor component to justify continuing. ~10% combined equity |
| 6 | Non-nut OESD or pair+gutshot | CHECK-CALL | Cardquant [15]: stop calling 6-out straight draws facing a bet AND a call |
| 8 | OESD (nut) | CHECK-CALL | ~32% equity flop-to-river but only ~50% when hit 3-handed. Lean toward calling, not raising |
| 9 | Non-nut flush draw | CHECK-FOLD to CHECK-CALL | Depends entirely on nut potential. Low flush draws (8-high) mostly fold multiway |
| 9 | Nut flush draw | CHECK-CALL or CHECK-RAISE | IP: lean toward calling. OOP: mix of call and raise. ~35% raw equity |
| 9+3 | NFD + overcard | CHECK-CALL to BET/RAISE | ~41% equity. Strong enough to semi-bluff with position |
| 12 | NFD + gutshot | BET or RAISE | Strong semi-bluff. ~45% equity. Combo draw territory |
| 12-15 | Flush draw + OESD | BET or RAISE (high frequency) | ~50-55% equity vs a single made hand. "No downside to playing aggressively" [13] |

### Raw Equity Math Reminders

- Rule of 4: Multiply outs by 4 for flop-to-river probability (approximate)
- Rule of 2: Multiply outs by 2 for single-street probability
- Flush draw (9 outs): ~36% flop-to-river, ~19% on single street
- OESD (8 outs): ~32% flop-to-river, ~17% on single street
- Gutshot (4 outs): ~17% flop-to-river, ~8.5% on single street

### Required Equity to Call by Pot Odds (Multiway)

Facing a 50% pot bet into a 3-way pot with one caller already:
- Pot = P, bet = 0.5P, call before you = 0.5P
- You need: 0.5P / (P + 0.5P + 0.5P + 0.5P) = 0.5 / 2.5 = **20% equity to call**

Facing a 75% pot bet into a 3-way pot:
- You need: 0.75P / (P + 0.75P + 0.75P + 0.75P) = 0.75 / 3.25 = **23% equity to call**

These are BEFORE implied odds adjustments. Nut draws get implied odds bonuses; non-nut draws get reverse implied odds penalties.

---

## 8. Specific Multiway Adjustments Summary

### Bet Sizing

**Source: GTO Wizard [1, 7], Phil Galfond [17]**

- Use SMALLER bet sizes multiway (25-40% pot rather than 66-75%)
- Reason: equity retention drops off a cliff as collective defense produces extremely strong continuing ranges
- Exception: With very strong hands (sets, nut draws with pair) in low-SPR pots, can use larger sizes

### Blocker Effects

**Source: GTO Wizard [1], Upswing [11]**

- Blockers become MORE important multiway because they interact with more ranges
- Card removal effects are more powerful with 3+ opponents
- When check-raising with NFD OOP: favor low kickers (As3s better than AsJs on 9s7s2d) because the high card blocks opponent's flush draw calling range

### Position Hierarchy for Draws

**Source: GTO Wizard [8, 9], Upswing [11, 12]**

- **IP with nut draw:** Best spot. Can call and realize equity, or raise for fold equity + value. Over-realize equity (110-130% EQR).
- **IP with non-nut draw:** Decent. Call and evaluate turn. Under-realize vs heads-up but better than OOP.
- **OOP with nut draw (one behind):** Mix of check-call and check-raise. Check-raise with low kickers.
- **OOP with nut draw (two behind):** More inclined to check-raise. Calling is less profitable with players behind.
- **OOP with non-nut draw:** Worst spot. Under-realize heavily (~70-80% EQR). Often a fold unless very cheap.

### The "Nut Potential" Filter

**Source: GTO Wizard [1, 2], Phil Galfond [17]**

The single most important concept for draws multiway: **does this draw have nut potential?**

- Betting frequencies multiway correlate strongly with nut advantage
- A player with range advantage but lacking nut hands should play passively
- In multiway, non-nut draws are traps: "With multiple players often holding suited cards, the second-nut flush frequently loses"
- Galfond: "Your threshold for putting in big bets on the flop should go way up, but you should use bigger bet sizes and only bet with huge hands like sets and some nut flush draws"

---

## 9. Key Takeaways for Curriculum Design

1. **Nut potential is the #1 filter.** Before deciding how to play any draw multiway, ask: "Can this draw make the nuts or near-nuts?" If no, lean heavily toward check-fold.

2. **Combo draws are the exception to multiway passivity.** With 12+ outs, equity cannot be denied and aggressive play is warranted regardless of number of opponents.

3. **Position amplifies draw value by ~40% EQR.** The gap between IP (118%) and OOP (79%) equity realization means the same 9-out flush draw is a clear continue IP but a marginal one OOP.

4. **Naked gutshots are multiway poison.** 4 outs is never enough to continue without supplementary equity (backdoor flush, overcards, pair).

5. **Non-nut flush draws are the biggest multiway trap.** Players overvalue the "9 outs" of a low flush draw. Multiway, these hands have massive reverse implied odds.

6. **Backdoor equity is the tiebreaker.** The 3-4% from a backdoor flush or 2-3% from a backdoor straight is what separates "check-fold" from "check-call" for marginal hands.

7. **Bet smaller multiway with draws.** 25-40% pot preserves equity retention and costs less when you miss. Save large bets for nut hands.

8. **The more players behind, the less profitable calling becomes.** With two players behind, lean toward raise-or-fold rather than passive calling with draws.
