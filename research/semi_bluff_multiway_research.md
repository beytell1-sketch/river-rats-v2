# Semi-Bluffing in Multiway Pots: Research Compilation

## Research Date: 2026-04-06
## Sources: 15+ distinct sources with solver data, frequencies, and concrete examples

---

## TABLE OF CONTENTS
1. [Core Principle: Why Semi-Bluffing Changes Multiway](#1-core-principle)
2. [Solver C-Bet Frequencies: HU vs 3-Way](#2-solver-c-bet-frequencies)
3. [Nut Flush Draw Betting Frequencies](#3-nut-flush-draw-frequencies)
4. [Blocker Effects: Ace of Flush Suit 3-Way](#4-blocker-effects)
5. [Bet Sizing for 3-Way Semi-Bluffs](#5-bet-sizing)
6. [Board Texture Effects on 3-Way Semi-Bluff EV](#6-board-texture)
7. [IP vs OOP Semi-Bluff Strategy 3-Way](#7-ip-vs-oop)
8. [Hand Classes That Should NEVER Semi-Bluff 3-Way](#8-never-semi-bluff)
9. [When Semi-Bluffing IS Correct 3-Way](#9-when-correct)
10. [Defense Frequency Math: Shared Burden Multiway](#10-defense-math)
11. [Academic/Theoretical Findings](#11-academic)

---

## 1. CORE PRINCIPLE: WHY SEMI-BLUFFING CHANGES MULTIWAY

### Source: GTO Wizard - "10 Tips for Multiway Pots in Poker"
- **URL:** https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/
- **Key finding:** Players can defend much tighter multiway without becoming exploitable. The burden of defense is shared between opponents.
- **Data point:** For a pot-sized bluff to be profitable, you need folds at least 50% of the time HU. Multiway, each opponent only needs to defend enough such that BETWEEN them they don't fold more than half the time.
- **Implication:** Pure bluffs are ineffective multiway. You need stronger value bets AND stronger bluffs.
- **Rule:** "With the exception of the river, you'd do well to almost never bluff a hand without solid drawing equity."

### Source: Upswing Poker - "7 Multiway Tactics You Should Know"
- **URL:** https://upswingpoker.com/multiway-pot-concepts/
- **Key finding:** Multiple opponents act as a "singular, much stronger opponent" -- the "enemy unit" concept.
- **Rule:** Tighten your value range AND your bluff range. You need more than one overcard + backdoor flush draw to justify bluffing multiway.

### Source: Upswing Poker - "When Should You Bet the Flop in Multi-Way Pots?"
- **URL:** https://upswingpoker.com/multiway-pots-flop-bet-strategy/
- **Key finding:** Since we have fewer value bets in multiway situations, we must also reduce our number of bluffs to remain balanced.
- **Data point:** Small bet sizing is preferred for bluffs multiway -- forces only slightly fewer folds than standard sizing while giving significantly better price on bluffs.

---

## 2. SOLVER C-BET FREQUENCIES: HU vs 3-WAY

### Source: GTO Wizard - "Playing In Position Against Two Callers"
- **URL:** https://blog.gtowizard.com/playing-in-position-against-two-callers/
- **Critical data:**
  - LJ checking frequency increases by **+11%** when facing both SB+BB vs just BB alone
  - Large pot-sized c-bet used **18%** of the time HU drops to only **1.3%** multiway (virtually eliminated)
  - Many hands that were considered valuable HU are no longer worth betting 3-way
- **Draw-specific finding:** Choose nut-suit draws, BDSD + overcards that block opponent's strongest continues, and wheel backdoors on A-high boards. Avoid complete air (no pair, no backdoors, no relevant blockers).
- **Reason:** Multiway calls gravitate to exactly the hands you need to block.

### Source: GTO Wizard - "Betting Draws in Position: The Real Rules"
- **URL:** https://blog.gtowizard.com/betting-draws-in-position-the-real-rules/
- **Critical data:**
  - Overall range betting frequency: ~58%
  - Draw checking frequency: ~56% (draws are checked MORE than the overall range)
  - This is counterintuitive -- draws are bet LESS frequently than the average hand
- **Rule:** Draws that don't want to face a check-jam should be checked back, not bet.

### Source: GTO Wizard - "GTO Wizard AI 3-way Benchmarks"
- **URL:** https://blog.gtowizard.com/gto_wizard_ai_3_way_benchmarks/
- **Key finding:** GTO Wizard AI now supports full 3-way postflop solving with customizable ranges, bet sizes, and rake structures.

---

## 3. NUT FLUSH DRAW BETTING FREQUENCIES

### Source: GTO Wizard - "Crack the Shell of Nut Draw Strategy"
- **URL:** https://blog.gtowizard.com/crack-the-shell-of-nut-draw-strategy/
- **Critical data (100bb CO vs BB SRP, Q-s-6d-2d flop):**
  - CO overall c-bet frequency: **49%**
  - CO c-bets nut flush draws: **69%** (higher than average, but NOT a pure bet)
  - With only single bet size permitted: CO c-bets **70%** of range but **76%** of nut flush draws
  - **A-d-8d:** performs **6bb/100 better** as a pure bet
  - **A-d-3d:** same EV whether bet or checked
  - **A-d-9d:** mixes in a decent chunk of checking at equilibrium
- **Key principle:** Solvers scatter nut draws across ALL actions to prepare for flush-completing turn cards. If solver mixes a hand across multiple actions, that hand has the SAME equilibrium EV for all those actions.
- **Warning:** If you bet ALL your nut flush draws, your opponent can exploit you (your checking range becomes too weak when flush completes).

### Source: GTO Wizard - "Picking the Right Semi-Bluffs"
- **URL:** https://blog.gtowizard.com/picking-the-right-semi-bluffs/
- **Critical data:**
  - Non-flush draws average **28.43% equity** or less -- bet more often (prefer folds)
  - Flush draw variants (combo draws with flush) are bet the LEAST among strong drawing hands
  - Heart combo draws have almost **2x the equity** of non-flush counterparts
  - Every heart combo draw has >**50% equity**
  - **A-heart-K-heart has 67.4% equity** on the example board
- **Core rule:** "For a hand to be considered a bluff, it needs to be weak enough so that taking down the pot uncontested is one of the best possible outcomes."
- **Implication for nut flush draws:** They are often TOO STRONG to bluff with -- you'd hate to bet AhKh and get a fold when you have 67% equity.

### Source: Upswing Poker - "How to Play Nut Flush Draws in Cash Games"
- **URL:** https://upswingpoker.com/nut-flush-draws/
- **Critical data:**
  - Solver checks back flush draws **31%** of the time on 8d-6c-4c type boards
  - **30-40%** of flush draws should be checked using simplified rules
  - Jack-high flush draws have HIGHER raising frequency than Ace-high flush draws
  - Against 66-80% pot double barrel: need nut or 2nd-nut flush draw to justify calling
  - Against overbet: only nut flush draws are strong enough to check-call

### Source: Upswing Poker - "Flush Draws as Preflop Aggressor"
- **URL:** https://upswingpoker.com/flush-draws-preflop-aggressor/
- **Data point:** In multiway, bet WAY LESS of 8-high flush draws, bet WAY MORE of king-high and ace-high flush draws.
- **Solver data:** On good turn cards, checking frequency reduces to **43%**; solver splits roughly evenly between checking and betting non-paired flush draws.

---

## 4. BLOCKER EFFECTS: ACE OF FLUSH SUIT 3-WAY

### Source: GTO Wizard - "Understanding Blockers in Poker" / "Blockers & Unblockers"
- **URL:** https://blog.gtowizard.com/understanding-blockers-in-poker/
- **URL:** https://blog.gtowizard.com/blockers-unblockers-the-secret-to-picking-great-bluffs/
- **Critical findings for multiway:**
  - Blockers become MORE important multiway -- card removal effects interact with more ranges
  - Blocking the nuts counts for a LOT more multiway
  - Blocking folds is MORE problematic for bluffs multiway
  - Blocking continues makes it substantially harder to get paid with value hands
- **Specific Ace-of-suit effect:**
  - Having a flush draw REDUCES likelihood opponents will fold (you block their folding hands -- they can't have busted flush draws if you hold the Ace of that suit)
  - A missed straight draw interferes LESS with folding range, making folds relatively more likely
  - **King-high flush draws prefer to jam certain rivers; Ace-high flush draws prefer checking** -- due to the Ace blocking opponent's strongest flush draws and unblocking their value range

### Source: PokerStrategy.com - "Why Do We Not Check/Raise with the Nut Flush Draw?"
- **URL:** https://www.pokerstrategy.com/news/content/Self-Study:-Why-do-we-not-check-raise-with-the-nut-flush-draw-_129523/
- **Critical solver data (BB vs BTN, K-s-6s-5h board):**
  - GTO Wizard NEVER check-raises with any combination of nut flush draw in this spot
  - Preferred check-raise bluffs: weaker hands like Q-s-7s and 7-s-3s (with blocker/straight potential)
  - **A-s-9s** has a lot of equity but UNBLOCKS Button's value hands -- when you check-raise with it, you're much more likely to face value
  - The hand plays better as a bluff-catcher because it keeps in all villain's bluffs

### Source: Upswing Poker - "Flush Draws Level-Up Podcast"
- **URL:** https://upswingpoker.com/podcast/ep6-flush-draws/
- **Key finding:** When raising draws after an opponent bets, prioritize nut flush draws and second-nut flush draws with WEAKER kickers (A3s, A4s raise more than T9s).
- **Reason:** You want flush-over-flush or flush-draw-over-flush-draw scenarios when raising.

---

## 5. BET SIZING FOR 3-WAY SEMI-BLUFFS

### Source: GTO Wizard - "10 Tips for Multiway Pots"
- **URL:** https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/
- **Data:** Use smaller bet sizes due to decreased equity retention. Large pot-sized bets that were 18% of HU strategy drop to 1.3% multiway.

### Source: Poker.pro - "Multiway Muscle: Big-Bet Windows Revealed by GTO Wizard"
- **URL:** https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/
- **Key finding:** "Always small" is a helpful starting point multiway, BUT leave money on the table when nut edge + last action + low SPR converge on high/paired or front-door textures.
- **Data on paired board (Q-Q-5r) in 3-bet pot:**
  - With AA/KK/AQ: bet **65-75%** pot
  - Third-pot bet invites sticky calls from underpairs and ace-highs
  - Large bet captures value now and sets up comfortable turn shove on bricks
- **Rule:** Big bets work when nut edge, last position, and low SPR all converge. Otherwise default to small sizing.

### Source: Phil Galfond / philgalfond.com - "Mastering Multi-Way Pots"
- **URL:** https://www.philgalfond.com/articles/mastering-multi-way-pots
- **Key finding:** Small betting creates incentives to clear up equity for "pretty good" hands.
- **Strategy:** Bet small with hands that "like" small bets (flush draws, equity denial hands). Check hands that want to put big money in (let opponents make bad big bets against your strong holdings).

### Source: Upswing Poker - "Multiway Pots Flop Bet Strategy"
- **URL:** https://upswingpoker.com/multiway-pots-flop-bet-strategy/
- **Finding:** Small bet size for bluffs multiway -- forces only slightly fewer folds than standard sizing while giving significantly better price.

---

## 6. BOARD TEXTURE EFFECTS ON 3-WAY SEMI-BLUFF EV

### Source: GTO Wizard - "Flop Heuristics: IP C-Betting in Cash Games"
- **URL:** https://blog.gtowizard.com/flop-heuristics-ip-c-betting-in-cash-games/
- **Simplified heuristic:** Bet small on dry boards, bet big on wet boards, bet small on VERY wet boards.
- **Paired flops:** Bet significantly more often but only for small sizing (preflop equity advantage but reduced nut advantage from trips being in both ranges).
- **Very wet boards:** Many nutted hands in both ranges prevents overextending with big bets. Most draws call anyway; only complete misses fold (low fold equity value).

### Source: GTO Wizard - "Playing In Position Against Two Callers"
- **URL:** https://blog.gtowizard.com/playing-in-position-against-two-callers/
- **Board-specific data:**
  - A/K-high boards: Button retains dense concentration of TPTK and overpairs; blinds are capped. **50-66% pot** bet outperforms small automatic c-bet.
  - Coordinated boards: Less c-betting, more checking, as opponents hit more of these textures.

### Source: Ed Miller / Card Player - "Bluffing in Multiway Pots"
- **URL:** https://www.cardplayer.com/poker-news/16520-poker-strategy-with-ed-miller-bluffing-in-multiway-pots
- **Practical example:** $490 pot, $240 all-in bluff. Getting slightly better than 2:1 odds -- needs to work only 1/3 of the time.
- **Board texture rule:** "Don't touch coordinated boards in multiway unless you have legitimate hand strength." On dry boards like J-9-5, bluff success rate increases.
- **Live-game insight:** "Because the pot is multiway, I get that extra measure of credit. 'He wouldn't be crazy enough to bluff like that into four other players. Must be aces.'"

---

## 7. IP vs OOP SEMI-BLUFF STRATEGY 3-WAY

### Source: Upswing Poker - "How to Play Nut Flush Draws in Cash Games"
- **URL:** https://upswingpoker.com/nut-flush-draws/
- **IP strategy:** More incentive to CALL (rather than raise) with nut flush draws in position. You have informational advantage and control over pot size, aiding equity realization.
- **OOP strategy:** More incentive to CHECK-RAISE nut flush draws OOP. Reduced ability to reach showdown means you need to build the pot and apply pressure.

### Source: GTO Wizard - "Monkey in the Middle: 3-Way Pot Heuristics"
- **URL:** https://blog.gtowizard.com/monkey-in-the-middle-3-way-pot-heuristics/
- **Key finding:** Playing "monkey in the middle" (player behind AND in front of you) is the weakest position in 3-way pots. Most hands lose value going multiway; equity retention is much worse.
- **Warning:** HU heuristics are especially likely to steer you wrong when facing a small c-bet with a third player still to act behind you.

### Source: GTO Wizard - "Probing Out Of Position in 3-Way Pots"
- **URL:** https://blog.gtowizard.com/probing-out-of-position-in-3-way-pots/
- **Key finding:** When a 3-way flop checks through, you CANNOT conclude ranges are capped as confidently as in HU pots. OOP probe betting requires more caution.
- **Draw-specific:** With unpaired flush draws OOP, almost always probe bet on the turn. EXCEPTION: the strongest nut flush draws (AT, A9) which may check.

### Source: Fedor Holz / MyPokerCoaching - "Playing Multiway Pots After the Flop"
- **URL:** https://www.mypokercoaching.com/fedor-holz-multiway-pots-postflop/
- **Key rules:**
  - Fewer value hands + fewer bluffs = much lower overall betting frequency
  - "Completely fine to take free cards with your draws and try to realize your equity"
  - Pick hands with clean outs and nut potential; avoid hands that can easily be dominated

---

## 8. HAND CLASSES THAT SHOULD NEVER SEMI-BLUFF 3-WAY

### Source: GTO Wizard - "Picking the Right Semi-Bluffs"
- **URL:** https://blog.gtowizard.com/picking-the-right-semi-bluffs/
- **NEVER semi-bluff with:**
  - Nut flush draws that have >50% equity (too strong to want folds -- AhKh at 67.4% equity is a CHECK, not a bluff)
  - Hands where getting a fold is NOT one of the best outcomes

### Source: GTO Wizard - "From Gutshots to Airballs: Choosing Your Bluffs"
- **URL:** https://blog.gtowizard.com/from-gutshots-to-airballs-choosing-your-bluffs/
- **NEVER semi-bluff with:**
  - Draws that won't be strong enough to keep betting if they hit (dominated draws)
  - Flush draws used as bluffs reduce likelihood opponents fold (you block their missed draws = their folding range)

### Source: Upswing Poker - "7 Multiway Tactics"
- **URL:** https://upswingpoker.com/multiway-pot-concepts/
- **NEVER semi-bluff with:**
  - Complete air (no pair, no backdoors, no relevant blockers)
  - One overcard + single backdoor flush draw (not enough multiway)
  - Inside straight draws alone (not strong enough as sole equity source multiway)

### Source: MyPokerCoaching.com - "Multiway Pots Strategy Tips"
- **URL:** https://www.mypokercoaching.com/multiway-pots-strategy-tips/
- **NEVER semi-bluff with:**
  - Even inside straight draws are "not the best candidates to bet against multiple opponents"
  - Small-Ace hands without flush potential (e.g., As8d) -- often dominated when opponent has better Ace
  - Hands that can easily be dominated -- go for clean outs and nut potential instead

### Source: GTO Wizard - "Playing In Position Against Two Callers"
- **URL:** https://blog.gtowizard.com/playing-in-position-against-two-callers/
- **NEVER semi-bluff with:**
  - Complete air: no pair, no backdoors, no relevant blockers
  - Reason: multiway calls gravitate to exactly the hands you need to block

---

## 9. WHEN SEMI-BLUFFING IS CORRECT 3-WAY

### Source: GTO Wizard - "Playing In Position Against Two Callers"
- **URL:** https://blog.gtowizard.com/playing-in-position-against-two-callers/
- **CORRECT to semi-bluff with:**
  - Nut-suit draws (drawing to best possible flush)
  - BDSD (backdoor straight draw) + overcards that block opponent's strongest continues
  - Wheel backdoors on A-high boards that pressure non-ace one-pair

### Source: Upswing Poker - "Semi-Bluff Poker Strategy"
- **URL:** https://upswingpoker.com/semi-bluff-poker-strategy/
- **CORRECT to semi-bluff with:**
  - Flush draws and open-ended straight draws (the best candidates multiway)
  - Draws that have some potential of turning the best hand but have NO showdown value
  - When you can fold out better hands AND still make a hand worth value betting

### Source: Upswing Poker - "Flush Draws Level-Up"
- **URL:** https://upswingpoker.com/podcast/ep6-flush-draws/
- **Raising priority order when facing a bet multiway:**
  1. Nut flush draws with weak kickers (A3s, A4s) -- highest raise frequency
  2. Second-nut flush draws with weak kickers
  3. Combo draws (flush + straight draw)
  - Rationale: Want flush-over-flush scenarios; weak kickers add less showdown value so prefer aggressive line

### Source: Jonathan Little / PokerCoaching - "Multiway Play"
- **URL:** https://jonathanlittlepoker.com/wph-451-how-to-play-multiway-perfectly-with-rampage-poker/
- **Key insight:** Many poker players OVERFOLD in multiway pots, allowing higher-frequency betting than strict GTO. However, for fundamentals: check a lot with marginal made hands, mix in some value hands to check-raise.
- **Semi-bluff candidates for check-raise:** Hands with backdoor flush draws + top pair, or hands that can improve significantly.

---

## 10. DEFENSE FREQUENCY MATH: SHARED BURDEN MULTIWAY

### Source: GTO Wizard - "MDF & Alpha"
- **URL:** https://blog.gtowizard.com/mdf-alpha/
- **Formula:** Alpha (a) = Bet / (Bet + Pot) = minimum fold frequency needed for profitable bluff
- **HU example:** Pot-sized bet requires folds 50% of the time
- **Multiway math:** Defense burden is SHARED. Each player defends enough that combined they prevent profitable bluffing.
- **Extreme example:** If 8 players face a 10% pot bet:
  - HU defense requirement: 91%
  - 8-way defense requirement per player: only ~26%

### Source: hhDealer.com - "Bluff Frequencies: A Data-Driven Scientific Analysis"
- **URL:** https://hhdealer.com/blog/bluff-frequencies-a-data-driven-scientific-analysis-of-deception-in-poker/
- **Data:**
  - Breakeven fold % = Bet Size / (Bet Size + Pot Size)
  - Optimal bluff ratio: ~30% bluff ratio with bet of 7.5 into pot of 10 creates equilibrium
  - AI research (DQN/CFR): long-term bluff success rates between **33-37%** depending on variables
  - CFR bluffs more than DQN because equilibrium-driven strategy must sometimes bluff to remain unpredictable

### Source: MyPokerCoaching.com - "Playing Profitably in Multiway Pots -- MDF"
- **URL:** https://www.mypokercoaching.com/playing-profitably-in-mutliway-pots-mdf/
- **Key finding:** Folding frequencies are multiplicative multiway. Each player only needs to defend enough that between them all they don't collectively overfold.

---

## 11. ACADEMIC/THEORETICAL FINDINGS

### Source: arXiv - "A Survey on Game Theory Optimal Poker"
- **URL:** https://arxiv.org/html/2401.06168v1
- **Key finding:** Poker bots use default GTO strategies for betting/bluffing that slowly adjust as opponent models are built.

### Source: arXiv - "Beyond Game Theory Optimal: Profit-Maximizing Poker Agents for No-Limit Hold'em"
- **URL:** https://arxiv.org/pdf/2509.23747
- **Critical finding:** CFR-style methods LACK proven convergence to Nash equilibrium when there are 3+ players. Multiway games are evaluated using regret-style and expected-value diagnostics rather than exact exploitability.
- **Implication:** All "GTO" multiway solutions are approximations. True equilibrium in 3+ player games is not provably achieved by current solvers.

### Source: arXiv - "Analysis of Bluffing by DQN and CFR in Leduc Hold'em Poker"
- **URL:** https://arxiv.org/pdf/2509.04125
- **Finding:** CFR attempts to bluff more than DQN because equilibrium-driven strategy must sometimes bluff to remain unpredictable. DQN only bluffs when estimated Q-value says it's profitable.

---

## SUMMARY: KEY NUMERICAL TAKEAWAYS

| Metric | HU Value | 3-Way Value | Source |
|--------|----------|-------------|--------|
| C-bet frequency (LJ) | Baseline | +11% more checking | GTO Wizard |
| Large (pot-sized) c-bet usage | 18% | 1.3% | GTO Wizard |
| NFD c-bet frequency (CO vs BB, Qs6d2d) | 69% | Lower (unspecified) | GTO Wizard |
| Overall c-bet frequency (same spot) | 49% | Lower (unspecified) | GTO Wizard |
| NFD with single size allowed | 76% bet | N/A | GTO Wizard |
| Draw checking frequency | ~56% | Higher | GTO Wizard |
| AhKh equity on example board | 67.4% | Similar | GTO Wizard |
| Non-flush draw equity | <=28.43% | Similar | GTO Wizard |
| Solver flush draw check-back rate | 31% | Higher | Upswing |
| Bluff success rate needed (pot-size) | 50% | Shared across players | GTO Wizard |
| AI optimal bluff success rate | 33-37% | N/A | hhDealer/arXiv |
| Paired board value bet sizing (3bp) | N/A | 65-75% pot | Poker.pro |

---

## PRACTICAL RULES FOR RIVER RATS CURRICULUM

1. **Default to NOT semi-bluffing 3-way.** The burden of proof is on the semi-bluff to justify itself, not the other way around.

2. **Nut flush draws with high equity (>50%) are often CHECKS, not bets.** You don't want folds when you have 67% equity. This is the single most counterintuitive finding.

3. **If you semi-bluff, use small sizing.** Large bets virtually disappear from solver output multiway (18% to 1.3%).

4. **Prioritize nut potential over raw equity.** A3s is a better raising candidate than T9s despite lower raw equity, because flush-over-flush pays off and weak kickers add less showdown value (prefer aggressive line).

5. **The Ace blocker paradox:** Holding the Ace of the flush suit BLOCKS opponent's folding hands (busted flush draws). This makes Ace-high flush draws worse as bluffs on rivers where the flush misses. King-high flush draws are often better river bluff candidates.

6. **Board texture screen:** Never semi-bluff on coordinated/wet boards multiway unless you hold genuine nutted draws. Dry boards offer more fold equity.

7. **Position amplifies everything:** IP, prefer calling with draws over raising (information advantage aids equity realization). OOP, prefer check-raising to compensate for reduced showdown ability.

8. **The scatter principle:** Solvers distribute nut draws across all actions to prevent exploitation on flush-completing turns. Always keep some nut draws in your checking range.

9. **CFR solvers don't provably converge in 3+ player games.** All multiway solver outputs are approximations. Use them as heuristics, not gospel.

10. **Minimum viable semi-bluff 3-way:** Nut flush draw OR combo draw (flush + straight) with no showdown value. Anything less is a check.
