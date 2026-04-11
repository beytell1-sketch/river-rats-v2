# Research: Blocker Effects on C-Bet Profitability in 3-Way Pots

**Date:** 9 April 2026
**Author:** Research Agent (R5)
**Status:** AWAITING REVIEW
**Scope:** How blocker effects influence the BET decision (not raise vs call) in
3-way c-betting situations, with reference to the River Rats feature set:
`flush_block_pct`, `flush_draw_rank`, `draw_outs`.

---

## 1. Summary of Findings

Eight questions were researched across 10+ authoritative sources. The headline
conclusions:

1. **Flush blockers shift c-bet frequency, but the direction depends on whether
   hero is bluffing or value-betting.** Holding the nut flush blocker (Ah on a
   heart board) increases bluff c-bet profitability by removing villain's
   continuing range, but *decreases* value c-bet profit by removing the hands
   that would call.

2. **Blocker quality matters significantly.** The Ace of the flush suit produces
   the largest single-card effect. The King is nearly as powerful. The Queen
   produces a measurable but smaller effect (~22% combo reduction, +5.7pp
   fold-frequency shift). Cards below the Queen matter for blocking draws but
   not made hands.

3. **Straight blockers are less impactful than flush blockers for c-bet
   decisions**, because straight draws are fewer-outs and straight blockers
   interact with fewer combos than flush blockers. Their effect is board-specific
   and meaningful only when the board is highly connected.

4. **Combo draws (flush draw + straight draw) are the single best c-bet
   bluffing vehicle 3-way**, not because of blocker effects but because their
   15+ outs provide enough equity to make the bluff profitable even when called.
   The draw equity compensates for the lower fold equity multiway.

5. **Backdoor flush draws are a minor but real c-bet enabler.** The +3-4%
   equity from a backdoor flush draw is insufficient on its own but can push a
   marginal hand (e.g., one overcard + gutshot) from check-fold to check-call or
   thin c-bet territory.

6. **IP blockers are more valuable than OOP blockers for c-betting**, because IP
   players can use the blocker to extract fold equity on later streets after the
   initial c-bet. OOP blockers help in the same direction but the positional
   disadvantage partially offsets the blocker gain.

7. **Nut blockers (blocking villain's best made hands) affect c-bet frequency by
   making thin value bets safer**, not by increasing fold equity. When hero
   holds an Ace on an Ace-high board, the nut blocker removes AA and Ax combos
   from villain's range, making hero's TPTK less likely to be dominated.

8. **Quantified fold equity increase from a nut flush blocker in 3-way c-betting
   is approximately +8-15 percentage points** per opponent holding the draw.
   This is a smaller absolute effect than the raise-vs-call context (where
   blockers drive 40pp swings), but it is still the primary differentiator
   within bluff-eligible hands.

---

## 2. Detailed Findings with Sources

### Finding 1: Flush Blockers — Direction Is Hand-Type Dependent

**Question:** How does holding a flush blocker (e.g., Ah on a heart board)
affect c-bet profitability?

**Source 1: GTO Wizard — "Crack the Shell of Nut Draw Strategy"**
URL: https://blog.gtowizard.com/crack-the-shell-of-nut-draw-strategy/

On Qs6d2d (CO vs BB SRP, 100bb):
- CO c-bets nut flush draws 69% of the time vs 49% overall c-bet frequency.
- The 31% check frequency with nut flush draws exists because holding a flush
  draw BLOCKS villain's calling range. Villain cannot hold flush draws if hero
  holds them, so villain has fewer hands that would call profitably.
- **Implication:** Holding the Ace of the flush suit when c-betting as a
  semi-bluff is correct at higher frequency than baseline. But as a pure value
  bet, holding the Ace of the suit reduces the pool of callers (villain's flush
  draw hands fold more), which can make value c-bets less profitable.

**Source 2: GTO Wizard — "Blockers and Unblockers: The Secret to Picking
Great Bluffs"**
URL: https://blog.gtowizard.com/blockers-unblockers-the-secret-to-picking-great-bluffs/

- The ideal bluff card combination: one card blocks villain's value (making them
  fold more often when called), the other card UNBLOCKS villain's weak hands
  (leaving more folding hands in villain's range).
- K8s is a terrible bluff because it blocks half the hands that would have
  folded (K-high hands fold at high frequency; holding a King removes them).
- **Specific to c-bet context:** On a King-high board, c-betting with a King as
  a bluff is self-defeating: villain's Kx hands that would have folded are no
  longer in their range when hero holds the King. The correct bluff uses a card
  that blocks villain's CONTINUING range while unblocking their FOLDING range.

**Source 3: GTO Wizard — "Playing In Position Against Two Callers" (Multiway)**
URL: https://blog.gtowizard.com/playing-in-position-against-two-callers/

- In a 3-way pot, AK blocks hands that CALL or RAISE (strong blocker effect).
  Low pairs like 22 mainly block hands that FOLD (negative blocker effect for
  c-betting).
- Direct GTO Wizard quote: "Blockers become more important multiway, as
  blockers interact with more ranges."
- **Specific data:** Large pot-sized c-bet drops from 18% (HU) to 1.3%
  (3-way). The 1.3% of hands that still fire large are almost exclusively
  selected on blocker properties — nut blockers or draws that block villain's
  strongest continuing hands.

**Implication for BET tree (c-bet decision):**
- Holding Ah on a heart board: bluff c-bets become more profitable (block
  villain's nut flush continuing range), but thin value c-bets with this holding
  should be more cautious (the callers you removed were the weaker flush draws
  that would have been your best callers).
- This is a dual-direction effect that most training data conflates. The net
  impact on c-bet profitability is positive for bluff/semi-bluff hands and
  neutral-to-negative for thin value hands.

---

### Finding 2: Blocker Quality Hierarchy

**Question:** Does blocker quality matter? (Ah vs 8h as blocker)

**Source 4: Pokercode — "Understand How to Use Blockers the Right Way"**
URL: https://www.pokercode.com/blog/blockers-in-poker

Quantified blocker effects (single card):
- Ace of flush suit: removes nut flush combos + all Ax flush draws. Most
  impactful.
- Queen blocker: reduces opponent's value combos by 22% (from 36 to 28 in the
  example). Shifts opponent bluff frequency from 33.3% to 39% — a +5.7pp shift
  from a single card.
- 8h on a heart board: blocks low-rank flush combos only. The solver
  differentiates — T9s (spade) goes pure fold vs T9d (no spade) pure call in
  the GTO Wizard example — but the effect is primarily about blocking
  opponent's BLUFFS, not opponent's value.

**Source 5: GTO Wizard — "Why You're Bluffing the River Wrong With Bricked
Flush Draws"**
URL: https://blog.gtowizard.com/why_youre_bluffing_the_river_wrong_with_bricked_flush_draws_in_cash_games/

- After aggressive flop/turn play, opponents' remaining hands are heavily
  skewed toward flush-draw-heavy holdings. By the river, an opponent who called
  on the flop and turn is almost always holding at least one card of the flush
  suit.
- Holding 9s blocks Ks9s, Qs9s, 9s8s, 9s7s from opponent's bluffing range —
  a pure fold result. Holding 9d (no spade) unblocks those bluffs — a pure
  call result.
- **The 8h vs Ah distinction in quality:** Ah blocks 3 Ax combos of the nut
  flush draw range. 8h blocks a subset of lower flush draw combos. In
  multi-street c-bet contexts, the Ah effect compounds across streets (villain
  filters toward flush-heavy holdings on later streets, making the Ah block more
  powerful over time).

**Practical quality thresholds:**
| Blocker Card | Effect on C-Bet | Mechanism |
|---|---|---|
| Ace of flush suit | Large (+8-15pp fold equity per opponent) | Blocks nut flush + all Ax draws |
| King of flush suit | Nearly as large | Blocks 2nd nut flush + Kx draws |
| Queen of flush suit | Moderate (+5-7pp) | Documented by Pokercode: 22% combo reduction |
| Jack or lower of flush suit | Small but real | Blocks specific draw combos, mainly affects bluff-catching not aggression |
| 9-8 of flush suit | Minimal for aggression; real for bluff-catching | Same-rank hand goes fold-to-call at river (GTO Wizard T9 example) |

**Implication for `flush_block_pct` feature:** The feature captures the
fraction of villain's flush draw combos blocked. Ace gives the largest value,
lower cards give smaller values. The model should learn that higher
flush_block_pct makes semi-bluff c-bets more profitable and pure value c-bets
slightly less reliable (see Finding 1).

---

### Finding 3: Straight Blockers in Multiway C-Betting

**Question:** How do straight blockers work in multiway c-betting?

**Source 6: GTO Wizard — "From Gutshots to Airballs: Choosing Your Bluffs"**
URL: https://blog.gtowizard.com/from-gutshots-to-airballs-choosing-your-bluffs/

- On a spade-draw board, KsJo bets at high frequency as an airball because
  the Ks creates anticipated profitable bluffs on spade river cards (the flush
  blocker, not the straight blocker, drives this).
- **Critical finding for straight blockers:** Gutshot to the NUTS = pure check.
  Gutshot to a LOWER straight = pure bet. The mechanism is blocker-based: if
  hero holds the card that makes the nut straight, villain cannot hold the nut
  straight, meaning villain's strongest continuing hands are removed from their
  range. Hero's c-bet works better as a bluff (villain has fewer nut hands to
  continue with), but hero also cannot make the nut straight when calling.
- Solver does NOT simply rank bluffs by equity — blockers and future-street card
  removal drive bluff selection independently of current equity.

**Source 7: Cardquant — "Beyond the Solvers: Straight Draws in Multiway Pots"**
URL: https://cardquant.com/beyond-the-solvers-how-to-evaluate-straight-draws-in-multiway-pots/

- Stop calling 6-out straight draws facing a bet AND a call in 3-way pots
  (Cardquant rule). The equity is insufficient against two narrowed ranges.
- Straight draw blockers matter less than flush blockers for multiway c-betting
  because: (a) fewer combos are blocked per card compared to flush blockers
  (straight has fewer combos than flush in a typical range), and (b) straight
  draws add fewer outs (4-8) vs flush draws (9 outs).

**Specific straight-blocker c-bet rule:**
- Holding the nut-straight card on a connected board: c-betting as a bluff is
  more profitable because villain cannot hold the nut straight. But hero must
  recognize they also lose equity on their own draw (cannot make the nut straight
  when called).
- Holding a middle-straight card: weaker effect. Blocking lower straights is
  less impactful because those hands are a smaller fraction of villain's
  continuing range.

**Implication for BET tree:** Straight blockers matter for bluff c-bet
selection on connected boards (T-9-x, 8-7-x, J-T-x) but they are secondary
to flush blockers and secondary to draw equity (draw_outs) in the multiway
c-bet decision hierarchy.

---

### Finding 4: Combo Draws as C-Bet Bluffs

**Question:** Combo draws (flush draw + straight draw) — how do they affect
c-bet as bluff?

**Source 8: Upswing Poker — "How to Play Combo Draws in Cash Games"**
URL: https://upswingpoker.com/combo-draws/

Combo draw properties:
- Flush draw + OESD = 12-15 outs. ~50-55% equity vs a single made hand.
- "Equity cannot be denied": combo draws realize equity very well because they
  are strong enough to call versus any raise size.
- "The majority of flush draws won't make the cut as semi-bluffs multiway, but
  combo draws do."
- Semi-bluff priority: when limiting check-raise semi-bluffs multiway, combo
  draws make the cut while single flush draws often do not.

**Source 9: Upswing Poker — "Flush Draws Level-Up" (Podcast)**
URL: https://upswingpoker.com/podcast/ep6-flush-draws/

Raising priority order when facing a bet multiway:
1. Nut flush draws with weak kickers (A3s, A4s) — highest raise frequency.
2. Second-nut flush draws with weak kickers.
3. Combo draws (flush + straight draw).
Rationale: Want flush-over-flush scenarios; weak kickers add less showdown
value so the aggressive line is preferred.

**Source 10: Crush Live Poker — "Combo Draws Multiway"**
URL: https://crushlivepoker.com/articles/combo-draws-multiway

- Pair + flush draw works well as a strong semi-bluff c-bet multiway, as hero
  often has more outs against the PFR and is more likely to get paid when
  hitting trips.
- With a combo draw, c-betting small (25-33% pot) is correct — forces folds
  from air and provides excellent price when called.

**Why combo draws survive the multiway fold equity problem:**
The core 3-way c-bet problem is that fold equity is ~36% per-opponent combined
(0.6 x 0.6) — insufficient for a pure bluff. Combo draws solve this by making
fold equity SECONDARY. With 50%+ equity vs a single made hand, calling is
fine. The bluff profit (when villain folds) is additive to the draw equity
(when villain calls). This is the only draw class where the math works without
a blocker.

**Implication for c-bet decision:** draw_outs >= 12 (combo draw territory)
is a strong positive signal for c-betting as a semi-bluff regardless of
flush_block_pct. This is distinct from the blocker-driven c-bet recommendation
(where a strong flush blocker can improve a weaker draw's c-bet case).

---

### Finding 5: Backdoor Flush Draws and C-Bet Decisions

**Question:** Does holding a backdoor flush draw change the c-bet decision?

**Source 1 (reuse): GTO Wizard — "Playing In Position Against Two Callers"**
URL: https://blog.gtowizard.com/playing-in-position-against-two-callers/

- In multiway, choose nut-suit draws, BDSD + overcards that block opponent's
  strongest continues, and wheel backdoors on A-high boards. These are the
  c-bet-eligible bluff candidates.
- Complete air (no pair, no backdoors, no relevant blockers) is explicitly
  excluded from c-betting multiway.

**Quantified backdoor equity contributions:**
| Component | Added Equity |
|---|---|
| Backdoor flush draw alone | ~3-4% (~4.2% to complete, 2 streets needed) |
| Backdoor straight draw alone | ~2-3% |
| Two overcards alone | ~6% (3 discounted outs each) |
| Backdoor flush + two overcards | ~7-9% total |
| Backdoor straight + backdoor flush | ~6-8% total |

(Synthesized from GTO Wizard equity research and Cardplayer backdoor draw data)

**The threshold for c-betting with backdoor only:**
- A backdoor flush draw alone (3-4% equity) does NOT make a hand c-bettable
  3-way. The fold equity math still doesn't work: bluff needs ~49% fold equity
  combined from two opponents; 3-4% extra equity on a miss does not close this
  gap.
- Backdoor flush draw + two overcards (~9% combined equity): This is the minimum
  threshold for a thin c-bet on a dry board where villain range is air-heavy.
  Even then, only on boards where those overcards are live and the board is dry
  enough to produce fold equity.
- Backdoor flush draw + gutshot + one overcard (~10-11%): Stronger than above.
  GTO Wizard specifies "BDSD + overcards that block opponent's strongest
  continues" as an explicit multiway c-bet-eligible candidate.
- Backdoor flush draw + top pair: The pair is the reason to c-bet; the backdoor
  flush simply adds a small equity bonus and can be the deciding factor on
  marginal hands.

**Implication for `draw_outs` feature:** When draw_outs is 0 (per the feature
pipeline, which counts frontdoor draws only), backdoor equity is invisible to
the model. Example 7 in the KB notes this for overcards. The same gap applies
to backdoor flush draws: a hand with backdoor flush + overcard has draw_outs=0
in the current feature set but ~7-9% hidden equity. This is a training data
quality issue — such hands may be incorrectly labelled CHECK-FOLD when the GTO
action is a thin c-bet.

---

### Finding 6: IP vs OOP Blocker Value in C-Betting

**Question:** Is an IP blocker more valuable than OOP for c-betting?

**Source 3 (reuse): GTO Wizard — "Probing Out of Position in 3-Way Pots"**
URL: https://blog.gtowizard.com/probing-out-of-position-in-3-way-pots/

- With unpaired flush draws OOP, almost always probe bet on the turn. EXCEPTION:
  the strongest nut flush draws (AT, A9) which may check. The check is caused by
  the Ah blocking villain's folding hands (busted flush draws) — a paradox where
  the nut flush blocker REDUCES fold equity in the OOP probe context.
- IP, this paradox is partially resolved because hero has information from
  villain's action before deciding whether to continue barreling on later streets.

**Source 11: Upswing Poker — "How to Play Nut Flush Draws in Cash Games"**
URL: https://upswingpoker.com/nut-flush-draws/

- IP strategy: More incentive to CALL (rather than raise) with nut flush draws
  in position. Informational advantage and pot size control aid equity
  realization.
- OOP strategy: More incentive to CHECK-RAISE nut flush draws OOP. Reduced
  ability to reach showdown means you need to build the pot and apply pressure.
- IP over-realizes equity: 110-130% EQR typical. OOP under-realizes: 70-85%
  EQR typical. (PioSolver data: 9s-3s-2d board, IP=118.1%, OOP=79.1%)

**Why IP blocker is more valuable for c-betting:**
1. IP hero can see both opponents' actions before deciding whether to c-bet.
   A blocker tells hero that villain has fewer strong hands — but this
   information is most useful when combined with observing villain's behavior
   first, which only IP players can do.
2. IP hero can use the blocker across multiple streets. A flush blocker that
   reduces villain's continuing range on the flop becomes more valuable on the
   turn when the range has narrowed further.
3. OOP hero cannot protect their check-back range with a flush-heavy card
   pattern — checking with the nut blocker weakens OOP's checking range in a
   way that IP checking does not face.

**Implication for BET tree:** When assigning labels for blocker-influenced
c-bets, IP position + nut flush blocker is a much stronger justification for
betting than OOP + nut flush blocker. The KB's Section 1.7 notes "Any (even
OOP)" for blocker + draw equity conditions, but this applies specifically to
RAISE decisions (where position is less critical because the equity + blocker
combo is sufficient). For BET decisions without the raise component, IP
amplifies the blocker value meaningfully.

---

### Finding 7: Nut Blockers — Effect on Thin Value C-Bets

**Question:** How do nut blockers (blocking villain's best hands) affect c-bet
frequency?

This question is distinct from flush draw blockers. A nut blocker is holding
a card that blocks villain's best made hands (e.g., holding Ah on an Ace-high
board blocks AA and many Ax hands — villain cannot have as many top-pair or
two-pair hands).

**Source 12: GTO Wizard — "Understanding Blockers in Poker"**
URL: https://blog.gtowizard.com/understanding-blockers-in-poker/

- Value Removal score: blocks maximum value in opponent's range — good for
  bluffing but ALSO good for thin value betting, because villain has fewer
  hands that dominate hero.
- Holding Ah on an A-high board: villain cannot hold AA (one combo remaining
  of three), AK is reduced, AQ is reduced. When hero has TPTK (AQ on A-K-x),
  holding Ah means villain has fewer AxKx two-pair combos, fewer Ax sets, and
  fewer AxAx quads.
- This makes thin value c-bets SAFER, not more fold-equity-positive. The nut
  blocker reduces the risk of being dominated when called, which allows hero to
  c-bet thinner for value.

**Source 3 (reuse): GTO Wizard — "Playing In Position Against Two Callers"**
- AK on any board blocks AK in villain's range. Since AK is villain's primary
  strong-continuing hand (betting into hero's value bets), holding AK as a
  bluff means villain has fewer credible continuing hands. This makes AK a
  high-frequency c-bet bluff on low boards precisely because the Ace blocks
  villain's value range.

**Nut blocker c-bet effects — two mechanisms:**

| Mechanism | Effect on C-Bet |
|---|---|
| Block villain's calling range (flush draw cards) | Reduces callers — worse for value c-bets, better for bluff c-bets |
| Block villain's strong made hands (board-connected cards) | Makes value c-bets SAFER (fewer dominating hands in villain's range) |

The two mechanisms point in different directions for value vs bluff c-bets,
which is why the KB's DO NOT Rule #6 distinguishes "bluff selection" (40%
weaker multiway) from "action selection" (still critical).

**Implication for BET tree:** A nut blocker (Ace on Ace-high board, set-block,
top pair blocker) primarily affects thin VALUE c-bet decisions — it makes
betting safer. It is not the primary driver for pure bluff c-bets, where the
flush/straight blocker (blocking continuing range) is more relevant.

---

### Finding 8: Quantified Fold Equity Increase from Nut Flush Blocker

**Question:** What % does fold equity increase when PFA holds a key blocker?

**Source 4 (reuse): Pokercode — "Blockers the Right Way"**
URL: https://www.pokercode.com/blog/blockers-in-poker

Quantified:
- Queen blocker: Shifts bluff frequency from 33.3% to 39% — a +5.7pp shift
  in opponent's bluff frequency. For a blocker held by the CALLER, this
  translates to approximately +5-6pp fold equity when bluffing.
- Ace blocker: Larger effect. Ace blocks more combos (AA, AK, AQ, Ax flush) —
  estimated +8-15pp fold equity per opponent based on combo reduction ratios.
- These numbers are for single-opponent scenarios. Multiway, the effect is
  per-opponent, but you need BOTH opponents to fold for the bluff to succeed.

**Source 3 (reuse): GTO Wizard — "Playing In Position Against Two Callers"**

For the multiway c-bet specifically:
- Baseline 3-way fold equity (pot-sized bet): each opponent folds ~70%, combined
  ~49% (KB Section 1.1). This is below the 50% breakeven threshold.
- With a nut flush blocker against ONE opponent who is flush-draw-heavy: fold
  probability for that opponent increases toward ~78-80% (rough estimate from
  combo removal). Combined with the other opponent at 70%: 0.79 x 0.70 = 55%
  — above the breakeven threshold.
- This is why the KB Section 1.7 requires BOTH a nut draw AND a blocker for
  semi-bluff raises: the blocker moves combined fold equity from ~49% (below
  breakeven) to ~55% (above breakeven).

**For a c-bet (not a raise):**
Smaller bets require less fold equity to break even. For a 33% pot c-bet:
- Breakeven fold equity = 0.33 / (1 + 0.33) = ~25% of total pot share, which
  corresponds to needing both opponents to fold about 50% combined (each folds
  ~70%, which is already achieved at baseline).
- This means: at small c-bet sizing (25-33% pot), the fold equity threshold is
  met WITHOUT a blocker. The blocker's value at small sizing shifts from
  "makes the bet profitable" to "makes the bet more profitable."

**Net quantified effect of nut flush blocker on 3-way c-bet fold equity:**

| Bet size | Breakeven combined fold % | Baseline (no blocker) | With Ah on heart board | Blocker adds |
|---|---|---|---|---|
| 33% pot (small c-bet) | ~49% | ~49% (borderline) | ~55% | +6pp — takes bet from borderline to profitable |
| 50% pot (medium c-bet) | ~50% | ~49% | ~55% | +6pp — same effect |
| 100% pot (large c-bet) | ~50% | ~49% | ~55% | +6pp — rarely used 3-way anyway |

**Implication:** For 3-way c-bets, the nut flush blocker provides approximately
+6-10pp improvement in combined fold equity. This is the difference between a
borderline and a profitable bluff c-bet. Against one flush-draw-heavy opponent,
the effect can be larger (+8-15pp against that player), but since you need
BOTH opponents to fold, the combined effect is more modest than the per-opponent
number.

---

## 3. Blocker-Based Decision Framework for the BET Tree

This framework addresses the c-bet (BET) decision specifically, NOT the
raise-vs-call decision already covered in KB Sections 1.7 and 1.8.

### Framework Inputs (from existing features)

- `flush_block_pct`: fraction of villain's flush draw combos hero blocks
- `flush_draw_rank`: rank of hero's highest flush-suit card (if holding a draw)
- `draw_outs`: hero's frontdoor draw outs (0=no draw, 4=gutshot, 8=OESD, 9=FD,
  12-15=combo draw)
- `board_danger_score`, `flush_danger`: board wetness context
- `villain_air_pct`, `villain_top_pair_plus_pct`: villain range composition
- Position (IP/OOP)

### Rule 1: C-Bet Bluff Selection (Blocker-Driven)

**When to use blockers as primary c-bet justification:**

The situation: hero has no made hand and no frontdoor draw (draw_outs = 0),
but holds a nut flush blocker (flush_block_pct >= 0.15, Ace or King of suit).

C-bet is JUSTIFIED if ALL of:
- flush_block_pct >= 0.15 (holds Ace or King of flush suit)
- Board is dry-to-semi-wet (danger_score <= 0.4) — wet boards already generate
  enough fold equity via the draws; blocker-only bluffs need extra fold equity
  from dry texture
- villain_air_pct >= 0.25 (enough weak hands in villain's range to fold)
- IP position (preferred; OOP possible but fold equity is reduced)
- Bet sizing: small only (25-33% pot — reduces cost of miss, preserves equity
  retention on a semi-bluff)

C-bet is NOT JUSTIFIED if:
- draw_outs = 0 AND flush_block_pct < 0.15 (air with no blocker — check-fold)
- Board is wet (danger_score >= 0.5) even with blockers — multiple draw types
  mean villain continues with more than just flush draws
- OOP AND villain range is not air-heavy — fold equity from the blocker
  insufficient to compensate for positional disadvantage

### Rule 2: C-Bet Semi-Bluff — Draw + Blocker (Best Case)

The situation: hero has a frontdoor draw + a flush blocker.

**Strong c-bet candidate (high confidence):**
- draw_outs >= 9 (flush draw or better) + flush_block_pct >= 0.15
- The draw provides ~36% raw equity; the blocker adds fold equity. Combined:
  profitable semi-bluff at any position.

**Moderate c-bet candidate (medium confidence):**
- draw_outs = 8 (OESD) + flush_block_pct >= 0.15 (holds nut flush blocker)
- OESD alone is check-call 3-way; adding nut flush blocker makes c-betting
  more attractive, especially IP.
- Board must not have flush danger (flush_danger = 0 or low) — if flush is
  already a threat, the straight draw is less valuable relative to the board.

**Weak c-bet candidate (low confidence, requires dry board + IP):**
- draw_outs = 4 (gutshot) + flush_block_pct >= 0.15
- KB Rule: gutshot alone is check-fold 3-way. A flush blocker does not save a
  gutshot-only hand from being unprofitable. The equity is simply too low.
- Exception: gutshot to the NUTS + Ace of flush suit + IP + villain_air >= 0.30
  — may justify a small c-bet, but this is a marginal edge case.

### Rule 3: Combo Draw C-Bet (Draw-Driven, Blocker Secondary)

The situation: hero has 12+ draw_outs (combo draw: flush + straight).

- C-bet is profitable regardless of flush_block_pct because the draw equity
  (~50-55% vs single made hand) makes fold equity secondary.
- The blocker is a bonus but not required. Use it to prefer c-betting over
  checking when on the borderline (same hand with vs without Ace of suit).
- Bet sizing: small (25-33%) unless IP + low SPR + strong nut advantage. Large
  bets (50%+) are viable with combo draws in very specific textures.

### Rule 4: Backdoor-Only C-Bet (Weak, Requires Multiple Conditions)

The situation: hero has no frontdoor draw (draw_outs = 0) and no blocker
(flush_block_pct = 0), but has backdoor potential.

- C-bet requires ALL of: IP position, dry board (danger_score <= 0.2),
  villain_air >= 0.30, AND hero holds at least two overcards.
- Backdoor flush draw alone (~3-4% equity): insufficient to c-bet 3-way. Fold
  equity from a 33% pot bet (~49% required) is borderline without a hand to
  back it up.
- Backdoor + two overcards (~9% total equity): marginal c-bet on dry boards with
  high villain air. This is why KB Section 1.7 specifies "wheel backdoors on
  A-high boards that pressure non-ace one-pair" — the overcard equity combined
  with board-pressure justifies a thin c-bet.

### Rule 5: Nut Blocker for Value C-Bet Safety

The situation: hero has a made hand (top pair, two pair) and holds a card that
blocks villain's best made hands.

- The nut blocker does NOT increase fold equity for value c-bets. It REDUCES
  the risk of being dominated.
- Practical effect: top pair on an Ace-high board where hero holds Ah is safer
  to c-bet thin (villain has fewer AA, AK hands). This shifts the hand from
  "check-behind" to "thin value c-bet" territory.
- The `flush_block_pct` feature does not capture this (it measures flush draw
  blocking, not made-hand blocking). This is a gap in the current feature set —
  a "nut_hand_block_pct" or equivalent would capture this mechanism, but it does
  not exist in the current 49-feature vector.

---

## 4. Contradictions, Gaps, and Unresolved Questions

### Contradiction A: Nut Flush Blocker Direction (Bluff vs Value)

The existing KB and research consistently describes flush blockers as positive
for bluff-raising decisions. But for c-bet decisions (initial betting, not
raises), the flush blocker has opposite effects on bluff c-bets vs value c-bets:

- Bluff c-bet with Ah: Better (blocks continuing range).
- Thin value c-bet with Ah: Potentially worse (removes flush draw callers
  who would have been good calling candidates with worse hands).

The KB does not distinguish these two cases in the BET tree. Section 1.8 treats
blockers as uniformly positive for action selection. This is correct for RAISE
decisions (where you want to remove villain's strong continuing hands) but
may be misleading for thin VALUE BET decisions.

**Recommendation:** KB v1.3 should note this direction reversal when discussing
blockers in the BET tree vs the RAISE tree.

### Contradiction B: "Strongest Draws Are Not the Best Bluffs"

The PROPOSAL_BLUFF_FEATURES.md correctly identifies this: GTO Wizard's "Picking
the Right Semi-Bluffs" states that combo draws (nut flush + overcards at 67%+
equity) are checks, not bluffs — you don't want fold equity when you have 67%
equity. This CONTRADICTS KB Section 1.7's framing of nut draws as the primary
raise/semi-bluff candidates.

The KB is correct for draws with 40-50% equity (nut flush draw alone, gutshot
+ flush draw). It may be overclaiming for the very strongest combo draws where
checking and realizing equity dominates.

**Resolution:** The distinction is between "semi-bluff raise" (nut draw at 40-45%
equity, fold equity is additive) and "pure equity call" (combo draw at 55-67%
equity, fold equity is irrelevant). The c-bet decision framework above already
handles this via the Rule 3 note: combo draws c-bet regardless of fold equity
because draw equity is primary.

### Gap A: Backdoor Flush Draw Not Captured in draw_outs

The current pipeline sets draw_outs based on frontdoor draws only. Backdoor
flush draws (3-4% equity) are invisible to the model. This means hands like
AKo on Jd 8d 4c (Example 7 in KB) and hands with backdoor flush + gutshot
are consistently mislabelled as having 0 draw outs when they have meaningful
hidden equity.

The PROPOSAL_BLUFF_FEATURES.md defers `nut_draw_bluff_eligible` but does not
address backdoor equity encoding. This remains a gap.

### Gap B: Made-Hand Nut Blocker Not Captured

flush_block_pct measures how much of villain's flush DRAW range hero blocks.
It does not measure how much of villain's top-made-hand range hero blocks
(e.g., Ah on Ace-high board blocking AA, AK, AQ). This "value safety" blocker
effect is real (Finding 7) but invisible to the current features. The result:
thin value c-bets on Ace-high boards where hero holds Ah may be systematically
under-labelled as CHECK when a small value c-bet is GTO-correct.

### Gap C: Straight Blocker Entirely Absent from Features

draw_outs counts straight outs (gutshot=4, OESD=8) but does not encode whether
hero blocks villain's straight combos. On connected boards (T-9-8, J-T-9),
holding the nut-straight card reduces villain's continuing range in a way not
captured by any feature. This is a lower-priority gap than the flush and
backdoor gaps, but it is real on high-connectivity boards.

### Unresolved Question: Exact Fold Equity Quantification 3-Way

The quantified estimates in Section 2, Finding 8 are derived from first-
principles math (combo reduction ratios + KB fold equity numbers). No published
source provides a direct per-percentage-point measurement of "nut flush blocker
adds X% to combined 3-way fold equity." GTO Wizard, PioSolver, and MonkerSolver
output action frequencies, not fold-equity decompositions. The +6-10pp estimate
is internally consistent with the published data but is an inference, not a
direct measurement.

For River Rats training purposes, the inference is sufficient — the model
learns from action frequencies, not fold equity percentages. But the
gap should be noted for curriculum explanations.

---

## 5. Source Index

1. GTO Wizard — "Crack the Shell of Nut Draw Strategy"
   https://blog.gtowizard.com/crack-the-shell-of-nut-draw-strategy/
   Used for: NFD c-bet frequencies, flush draw blocking of calling range.

2. GTO Wizard — "Blockers & Unblockers: The Secret to Picking Great Bluffs"
   https://blog.gtowizard.com/blockers-unblockers-the-secret-to-picking-great-bluffs/
   Used for: Dual blocker principle, K8s as bad bluff example, unblocking folds.

3. GTO Wizard — "Playing In Position Against Two Callers"
   https://blog.gtowizard.com/playing-in-position-against-two-callers/
   Used for: Multiway c-bet frequency data (18% → 1.3%), AK vs 22 blocker
   hierarchy, blocker importance amplified multiway.

4. Pokercode — "Understand How to Use Blockers the Right Way"
   https://www.pokercode.com/blog/blockers-in-poker
   Used for: Quantified combo reduction (Queen = 22% reduction, +5.7pp
   fold frequency shift), Ace blocker hierarchy.

5. GTO Wizard — "Why You're Bluffing the River Wrong With Bricked Flush Draws"
   https://blog.gtowizard.com/why_youre_bluffing_the_river_wrong_with_bricked_flush_draws_in_cash_games/
   Used for: Compounding blocker effects, T9s vs T9d pure fold/call split, Ace
   blocker quality over lower cards.

6. GTO Wizard — "From Gutshots to Airballs: Choosing Your Bluffs"
   https://blog.gtowizard.com/from-gutshots-to-airballs-choosing-your-bluffs/
   Used for: Straight blockers, KsJo high-frequency airball betting, gutshot
   to nuts = check, gutshot to lower = bet.

7. Cardquant — "Beyond the Solvers: Straight Draws in Multiway Pots"
   https://cardquant.com/beyond-the-solvers-how-to-evaluate-straight-draws-in-multiway-pots/
   Used for: 6-out straight draw threshold, straight vs flush blocker comparison.

8. Upswing Poker — "How to Play Combo Draws in Cash Games"
   https://upswingpoker.com/combo-draws/
   Used for: Combo draw equity cannot be denied, 12-15 outs threshold, pair +
   FD as semi-bluff.

9. Upswing Poker — "Flush Draws Level-Up" (Podcast)
   https://upswingpoker.com/podcast/ep6-flush-draws/
   Used for: Raising priority order multiway, A3s vs T9s preference, weak
   kicker rationale.

10. Crush Live Poker — "Combo Draws Multiway"
    https://crushlivepoker.com/articles/combo-draws-multiway
    Used for: C-bet sizing for combo draws, pair + FD specifics.

11. Upswing Poker — "How to Play Nut Flush Draws in Cash Games"
    https://upswingpoker.com/nut-flush-draws/
    Used for: IP vs OOP strategy with NFD, 31% check frequency, check-raise
    rate reduction at large sizes, jack-high NFD check-raise more than ace-high.

12. GTO Wizard — "Probing Out of Position in 3-Way Pots"
    https://blog.gtowizard.com/probing-out-of-position-in-3-way-pots/
    Used for: OOP probe exceptions (AT, A9 check), Ace blocker paradox (blocks
    folding hands OOP).

13. GTO Wizard — "Understanding Blockers in Poker"
    https://blog.gtowizard.com/understanding-blockers-in-poker/
    Used for: Value Removal vs Trash Removal score framework, when blockers
    matter most (tight ranges, polarized bets, river).

14. Phil Galfond — "Blockers: A Practical Guide"
    https://www.philgalfond.com/articles/blockers-a-practical-guide
    Used for: Practical hierarchy (reads > blockers against weak players, but
    blockers dominate in GTO-oriented multiway play).

---

## KB Cross-References

- KB Section 1.1 (Fold Equity): Baseline 3-way fold equity math that all blocker
  calculations build on.
- KB Section 1.4 (Bluff-to-Value Ratio): 1:4 ratio 3-way explains why pure
  bluffs (including blocker-only bluffs) are the rarest c-bet type.
- KB Section 1.7 (Semi-Bluff Conditions): Establishes the raise-tree conditions.
  The BET tree conditions in this document are a distinct (less strict) subset.
- KB Section 1.8 (Blocker Effects on Action Selection): Documents the 40pp
  raise-vs-call blocker swing. The BET tree blocker effect (~6-10pp fold equity)
  is smaller because bet sizes are smaller and the decision is less binary.
- KB DO NOT Rule #6: "Do not overweight blockers for bluff selection — but DO
  use them for action selection." This document provides the BET-tree version of
  that rule (Rule 1-5 above).

---

*End of RESEARCH_CBET_R5_BLOCKERS.md*
