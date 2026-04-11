# 3-Way Postflop Worked Hand Examples Research

Research date: 2026-04-06

This document collects fully worked (or near-fully worked) hand examples from authoritative poker training sources where 3-way (or wider multiway) dynamics materially change the correct postflop decision compared to heads-up play. Each example is tagged with the principle it illustrates and whether it is solver-verified or expert opinion.

---

## Category A: Top Pair / Overpair Should CHECK (Not Bet) Multiway

### Example A1 -- AQ on Q-9-6 Flop, 3-Way (Fold to Check-Raise)

- **Source:** Card Player / Jonathan Little -- "Folding Top Pair, Top Kicker On The Flop"
  - https://www.cardplayer.com/poker-news/25013-poker-strategy-with-jonathan-little-folding-top-pair-top-kicker-on-the-flop
- **Event:** $5,000 buy-in live partypoker event, Montreal
- **Hero cards:** A-Q (top pair, top kicker)
- **Board:** Q-9-6 (flop)
- **Positions:** Hero in EP (first to act postflop after raise), tight-passive MP caller, excellent TAG in SB
- **Action:** Hero raises preflop to 4,500, MP calls, SB calls. Flop Q-9-6. SB checks, Hero bets 12,000 into 17,500. MP calls. SB tanks for ~3 minutes, then check-raises.
- **Correct play:** FOLD to the check-raise. The SB's 3-way check-raise range is almost exclusively sets (QQ/99/66), Q9, 96, or a premium draw. TPTK is crushed.
- **Verification:** Expert opinion (Jonathan Little), supported by range logic
- **Principle:** **Range narrowing in multiway pots.** A check-raise into two opponents in a 3-way pot is an extremely strong signal. The SB must beat not only Hero's betting range but also MP's calling range. HU, a check-raise could include semi-bluffs and lighter hands; 3-way, it is almost always the nuts or near-nuts.
- **HU vs 3-way difference:** HU, Hero would call (or even re-raise) the check-raise with TPTK. 3-way, it is a clear fold.

---

### Example A2 -- QJ on Q-3-4 Flop, 3-Way (Check Behind with Top Pair)

- **Source:** Card Player / Alex Fitzgerald -- "Five Multiway Pot Exploits"
  - https://www.cardplayer.com/poker-news/28642-poker-strategy-with-alex-fitzgerald-five-multiway-pot-exploits
- **Event:** WSOP event
- **Hero cards:** Q-clubs J-clubs
- **Board:** Q-spades 3-spades 4-diamonds (flop)
- **Positions:** EP min-raises to 200, Hero (HJ) flat calls, BTN 3-bets to 800, EP calls, Hero calls. 3-way to flop.
- **Action:** Flop Q-s 3-s 4-d. Hero checks (correct -- should check nearly entire range here).
- **Correct play:** CHECK. In a 3-bet pot 3-way, QJo with a marginal kicker is a showdown hand, not a value bet. If Hero bets, they mostly fold out worse and get continued against by better.
- **Verification:** Expert opinion (Alex Fitzgerald)
- **Principle:** **Equity dilution / hand demotion.** Top pair with a marginal kicker goes from a clear value hand HU to a bluff-catcher multiway. The BTN (3-bettor) has AA/KK/AQ/KQ in range; EP has broadways and pairs. QJ cannot bet for value against the combined field.
- **HU vs 3-way difference:** HU in position against the 3-bettor, QJs might c-bet or float. 3-way, it checks and plays for showdown value.

---

### Example A3 -- AA on K-spades T-spades 6-clubs, 4-Way (Reduced Value of Overpairs)

- **Source:** Phil Galfond -- "Mastering Multi-Way Pots"
  - https://www.philgalfond.com/articles/mastering-multi-way-pots
- **Event:** $2/$5 NL cash game (illustrative)
- **Hero cards:** A-clubs A-diamonds
- **Board:** K-spades T-spades 6-clubs (flop)
- **Positions:** Hero raises EP, 4 callers (blinds + 2 others)
- **Action:** Blinds check to Hero. Hero must decide whether to c-bet.
- **Correct play:** Bet small for protection/thin value, but recognize the dramatic equity shift. Against a single opponent, there is only a ~33% chance they have top pair or a strong draw. Against four opponents, there is an 83% chance at least one of them has top pair or better / strong draw. AA is no longer a confident value bet for large sizing.
- **Verification:** Solver-informed expert opinion (Phil Galfond, with solver data cited)
- **Principle:** **Equity dilution / combinatorial explosion.** As more players see the flop, the probability that someone has connected strongly rises multiplicatively. Overpairs lose their dominance.
- **HU vs 3-way difference:** HU, AA on KTs6c is a clear large c-bet for value. Multiway, it bets small for protection or checks on some board textures.

---

### Example A4 -- AK on K-s 7-d 6-c, 3-Way (Top Pair Loses Value on Turn)

- **Source:** MyPokerCoaching / Fedor Holz -- "Playing Multiway Pots After the Flop"
  - https://www.mypokercoaching.com/fedor-holz-multiway-pots-postflop/
- **Hero cards:** A-K
- **Board:** K-spades 7-diamonds 6-clubs (flop), Q-diamonds (turn)
- **Positions:** Hero opens, 2 callers. 3-way single raised pot.
- **Action:** Hero c-bets flop, both opponents call. Turn Q-d. Hero should strongly consider checking.
- **Correct play:** CHECK the turn. Both opponents called the flop, narrowing their ranges to pairs, draws, and strong hands. The Q turn improves many of their continuing ranges (QK, QJ, QT) and the diamond adds flush draw possibilities. TPTK has gone from strong on the flop to mediocre on the turn when both opponents have shown interest.
- **Verification:** Expert opinion (Fedor Holz), solver-informed
- **Principle:** **Range narrowing after flop action.** When two opponents call a flop bet, their combined range is heavily weighted toward hands that have connected. The turn card further shifts equity. Betting again would be thin value at best and builds a pot Hero may lose.
- **HU vs 3-way difference:** HU, AK on this turn is still a standard value barrel. 3-way after both call flop, it becomes a check.

---

## Category B: Draws Should FOLD (Not Call/Raise) Multiway

### Example B1 -- K-clubs Q-clubs on 7-spades 5-spades 4-clubs, 3-Way (Overcards Must Check-Fold)

- **Source:** PokerNews / Jonathan Little -- "Playing a Draw Multiway Can Be a Really Tough Spot"
  - https://www.pokernews.com/strategy/playing-a-draw-multiway-can-be-a-really-tough-spot-37985.htm
- **Event:** Tournament, 20BB effective
- **Hero cards:** K-clubs Q-clubs
- **Board:** 7-spades 5-spades 4-clubs (flop)
- **Positions:** Hero UTG (raiser), BTN caller (40BB), BB caller (100BB). 3-way.
- **Action:** Flop 7s5s4c. Action checks to Hero.
- **Correct play:** CHECK-FOLD. The flop connects extremely well with the BB's defending range (67, 54, 76, 65, suited connectors, pairs). Hero has two overcards but zero board connection, no flush draw on the right suit, and terrible position. Continuation betting would fold out nothing and invite check-raises.
- **Verification:** Expert opinion (Jonathan Little)
- **Principle:** **Board texture vs. position and range interaction.** Low/connected boards hit blind-defending ranges hard. With multiple opponents, the chance that someone has connected is very high. Overcards are not semi-bluffs here -- they are pure bluffs against the field.
- **HU vs 3-way difference:** HU against one caller, Hero might c-bet as a semi-bluff (two overcards, backdoor straight potential). 3-way on this board, it is a check-fold.

---

### Example B2 -- T-diamonds 9-diamonds on 4-diamonds A-clubs 7-diamonds, 3-Way (Fold Flush Draw Facing Raise)

- **Source:** LearnWPT / PokerNews -- "How to Play a Flopped Flush Draw in a Multi-Way Hand"
  - https://www.pokernews.com/strategy/how-to-play-a-flopped-flush-draw-multi-way-hand-learnwpt-32903.htm
- **Event:** Live $1-2 cash game
- **Hero cards:** T-diamonds 9-diamonds
- **Board:** 4-diamonds A-clubs 7-diamonds (flop)
- **Positions:** MP2 raises, recreational HJ calls, Hero in BB with Td9d. 3-way.
- **Action:** Flop 4d Ac 7d. Everyone checks to MP2 who bets $10. HJ raises to $35. Action on Hero.
- **Correct play:** FOLD. Despite holding a flush draw (9 outs), the raise in a 3-way pot from a recreational player signals real strength (likely Ax with a diamond, two pair, or a set). Hero's flush draw is not to the nuts (only 9-high flush), and if Hero calls, MP2 may re-raise behind. The reverse implied odds are severe -- even making the flush, Hero could be drawing dead to a higher flush.
- **Verification:** Expert opinion (LearnWPT coaching staff)
- **Principle:** **Reverse implied odds + non-nut draws multiway.** When draws are not to the nuts, calling becomes much worse multiway because (a) someone is more likely to have a higher draw, and (b) the raise in front signals strength that further devalues your draw.
- **HU vs 3-way difference:** HU, a flush draw with two overcards (T9 on A-high board is not overcards, but the flush draw alone) would be a standard call or raise. 3-way facing a raise, it is a fold.

---

### Example B3 -- 8-hearts 9-hearts on Q-diamonds 6-hearts T-clubs, 5-Way (Call Only -- Do Not Raise Draw Multiway)

- **Source:** LearnWPT / PokerNews -- "Flopped a Double-Gutshot in a Multi-Way Pot"
  - https://www.pokernews.com/strategy/playing-drawing-hands-multi-way-pot-learnwpt-28962.htm
- **Event:** Tournament
- **Hero cards:** 8-hearts 9-hearts
- **Board:** Q-diamonds 6-hearts T-clubs (flop)
- **Positions:** UTG min-raises, MP1 calls, HJ calls, Hero calls. SB calls. 5-way (wider multiway but principle applies to 3-way).
- **Action:** SB and UTG check, MP1 bets, HJ calls. Action on Hero.
- **Correct play:** CALL (not raise). Hero has a double gutshot (7 or J makes a straight) plus backdoor flush draw -- roughly 9 outs. Getting ~4:1 pot odds, calling is profitable. But raising is wrong because: (a) Hero cannot fold out all opponents in a multiway pot, (b) the draw is hidden so implied odds are better by calling, and (c) a raise bloats the pot with a hand that will miss ~80% of the time on the next card.
- **Verification:** Expert opinion (LearnWPT)
- **Principle:** **Reduced fold equity multiway kills semi-bluff raises.** The more opponents, the less likely a raise will fold everyone out, converting the semi-bluff raise into a pure equity gamble at bad odds. Just call and realize equity cheaply.
- **HU vs 3-way difference:** HU, raising with a double gutshot + backdoor flush as a semi-bluff is standard. Multiway, just call.

---

## Category C: Thin Value Betting IS Correct Multiway (Factor Combination)

### Example C1 -- JJ on T-5-2 Flop, 3-Way (Small Value Bet with Vulnerable Overpair)

- **Source:** Card Player / Jonathan Little -- "Getting Value With An Overpair In A Multi-Way Pot"
  - https://www.cardplayer.com/poker-news/27159-poker-strategy-with-jonathan-little-getting-value-with-an-overpair-in-a-multi-way-pot
- **Event:** $3,000 buy-in WSOP event
- **Hero cards:** J-J (pocket jacks)
- **Board:** T-5-2 rainbow (flop)
- **Positions:** Hero raises EP (20,000 stack), TAG calls MP, loose-splashy player calls from BB. 3-way.
- **Action:** BB checks. Hero bets.
- **Correct play:** BET SMALL. Hero bets 1,100 into a 3,075 pot (roughly 1/3 pot). The key insight: JJ is almost certainly best on this board (overpair on a dry texture), but it is vulnerable to being outdrawn. A small bet extracts value from tens, pocket pairs below TT, and random hands the loose BB might have, while not over-committing. A large bet (e.g., 2,300) would fold out the hands Hero crushes and only get action from hands that beat Hero.
- **Verification:** Expert opinion (Jonathan Little), with stack-depth reasoning
- **Principle:** **Thin value with vulnerable hands requires small sizing multiway.** The bet must be small enough that worse hands call (tens, nines, eights) but protect equity against draws. The 3-way dynamic matters because the loose player in the BB provides extra calling stations to extract from.
- **HU vs 3-way difference:** HU, Hero might bet larger (50-75% pot) for protection and value. 3-way with a loose player, smaller sizing gets more calls from a wider field of worse hands.

---

### Example C2 -- 9-hearts T-spades on J-diamonds T-diamonds 9-clubs, 3-Way 3-Bet Pot (Thin Value with Bottom Two Pair)

- **Source:** CrushLivePoker -- "Thin Value in 3-Bet Pots"
  - https://crushlivepoker.com/articles/thin-value-in-3-bet-pots
- **Event:** $5/$10 NL cash game, Bicycle Casino
- **Hero cards:** 9-hearts T-spades
- **Board:** J-diamonds T-diamonds 9-clubs (flop), 6-diamonds (turn), 3-hearts (river)
- **Positions:** Hero opens BTN to $30, villain 3-bets from blinds to $100, Hero calls. (Heads-up after preflop, but the thin-value principle applies identically in 3-way 3-bet pots.)
- **Action:** Flop JdTd9c. Villain checks, Hero bets $130. Turn 6d. Hero bets $290. River 3h. Hero bets $605 into ~$1,000 pot.
- **Correct play:** VALUE BET ALL THREE STREETS. Bottom two pair on a coordinated board is often scared money. But the combination of factors -- position, opponent's check (indicating medium-strength), and the river bricking out -- makes thin value correct. Opponent's range includes overpairs with a diamond (like QQ with Qd), AK with a diamond, and other one-pair hands that will pay off.
- **Verification:** Expert opinion (CrushLivePoker coaching staff)
- **Principle:** **Factor combination for thin value.** Position + opponent's passive line + favorable runout = thin value is correct. The principle amplifies in 3-way pots when you have the betting lead and opponents have shown weakness (checking to you).
- **HU vs 3-way difference:** This specific hand was HU, but the coaching article explicitly states the principle applies to 3-bet pots with multiple players -- you must be willing to value bet thinly even in inflated pots.

---

### Example C3 -- JJ on J-spades 8-hearts 5-diamonds, 5-Way (Bet Top Set for Value + Protection)

- **Source:** PokerNews / Jonathan Little -- "Flopping Top Set in a Multi-Way Pot"
  - https://www.pokernews.com/strategy/flopping-top-set-in-a-multi-way-pot-how-to-extract-value-34057.htm
- **Event:** $5,000 WSOP event
- **Hero cards:** J-clubs J-diamonds
- **Board:** J-spades 8-hearts 5-diamonds (flop)
- **Positions:** Hero raises EP, 4 callers. 5-way pot.
- **Action:** Action checks to Hero on the flop.
- **Correct play:** BET. With top set multiway on a board with straight draw potential (9-7, 6-7, T-9), Hero must bet for both value and protection. Checking risks giving free cards to multiple drawing hands. The multiway field guarantees at least one caller with a pair or draw.
- **Verification:** Expert opinion (Jonathan Little)
- **Principle:** **Protection betting multiway with nutted hands.** Unlike HU where slow-playing a set might be profitable (one opponent, fewer draws live), multiway you must bet because the cumulative probability of someone drawing out increases with each opponent. Sets go from "trap" hands HU to "bet for protection" hands multiway.
- **HU vs 3-way difference:** HU, slow-playing top set on a dry-ish board is a viable option. Multiway, bet every time -- you need to charge the field.

---

## Category D: Range Narrowing and Information Signals

### Example D1 -- K-clubs 9-clubs Facing Big Bet on K-diamonds T-hearts 9-diamonds, 4-Way (Bet-and-Call Signal)

- **Source:** Upswing Poker / Nick Petrangelo -- "Multiway Hand Analysis"
  - https://upswingpoker.com/multiway-double-straddle-hand/
- **Event:** High-stakes cash game with straddles
- **Hero cards (Ginge):** K-clubs 9-clubs (two pair)
- **Board:** K-diamonds T-hearts 9-diamonds (flop), 4-clubs (turn)
- **Positions:** JD opens UTG (AJ), Doug calls BB (QdTd), Ginge calls straddle (Kc9c), Nick calls double straddle (9h8s). 4-way.
- **Action:** Flop KdTh9d. Checked to Doug who bets 70% pot into 3 opponents. Ginge (K9 = top two) just calls.
- **Correct play for Ginge:** CALL (not raise). Doug's 70% pot bet into 3 opponents represents a narrow, strong range. When someone bets big into multiple opponents, they need to beat not one but several ranges. Ginge's two pair is strong but raising isolates against only better hands (straights, sets) and folds out the hands Ginge beats. Calling keeps weaker hands in and disguises strength.
- **River:** Board finishes Kd Th 9d 4c 8d. Doug bets small. Ginge folds (correctly or questionably -- the article notes K9 is a GTO call but Ginge may have read under-bluffing).
- **Verification:** Solver-referenced expert analysis (Nick Petrangelo, with solver comparison)
- **Principle:** **Bet-and-call as a range-narrowing signal.** A big bet into multiple opponents narrows the bettor's range dramatically. The call from a player behind narrows their range too (strong but not nutted). Each action in a 3-way pot provides more information than the same action HU.
- **HU vs 3-way difference:** HU, two pair would likely raise for value. 3-way+, calling to keep the field in and avoid isolating against better is often correct.

---

### Example D2 -- KQ on A-K-3 Board, 3-Way (Check-Raise Signal is Extremely Strong)

- **Source:** Card Player -- "Playing Top Pair In A Multi-Way Pot" (Jonathan Little commentary)
  - https://www.cardplayer.com/cardplayer-poker-magazines/66354-the-bicycle-hotel-casino-30-9/articles/23045-playing-top-pair-in-a-multi-way-pot
- **Hero cards:** Not specified (observer analysis)
- **Board:** A-K-3 (flop)
- **Positions:** 3-way pot, SRP. Original raiser + 2 callers.
- **Action:** Check, original raiser bets, one player calls, third player check-raises.
- **Correct play (for caller):** FOLD most of the time. In a 3-way pot, a bet followed by a call followed by a check-raise is the strongest possible sequence of actions. The check-raiser must beat both the bettor's range AND the caller's range. This almost always represents two pair or better. Even AK (top two pair) should proceed cautiously; AQ/AJ/KQ are likely drawing very thin.
- **Verification:** Expert opinion (Jonathan Little)
- **Principle:** **Cascading range narrowing.** Each successive action in a multiway pot creates a more filtered, stronger range requirement. Bet -> call -> raise means the raiser's range is the narrowest of all three. HU, a check-raise could be a semi-bluff; facing two opponents, it is almost always value.

---

## Category E: C-Betting Strategy Changes Multiway

### Example E1 -- BTN vs SB+BB on A-K-x Rainbow, 3-Way (Larger C-Bet, Not Small)

- **Source:** GTO Wizard -- "Playing In Position Against Two Callers"
  - https://blog.gtowizard.com/playing-in-position-against-two-callers/
  - Also: poker.pro -- "Multiway Muscle: Big-Bet Windows Revealed by GTO Wizard"
  - https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/
- **Setup:** BTN opens, SB calls, BB calls. 3-way SRP.
- **Board:** A-K-x rainbow (e.g., A-K-4r)
- **Action:** SB checks, BB checks, action on BTN.
- **Correct play:** C-BET at 55-75% pot (larger than "default small" multiway). On A-K-x rainbow boards, BTN has a massive nut advantage: AK, AA, KK are heavily in BTN's range. The blinds' flat-calling ranges are capped (they would have 3-bet AK/AA/KK). The larger sizing extracts value from dominated Ax hands and denies equity to underpairs.
- **Verification:** Solver-verified (GTO Wizard 3-way solver)
- **Principle:** **Nut advantage allows larger sizing even multiway.** The conventional wisdom is "always bet small multiway." The solver disagrees on specific board textures where one player has a dominant nut advantage. A-K-x rainbow is the classic example because the blinds are capped.
- **HU vs 3-way difference:** HU, BTN would range-bet small on this texture. 3-way, the solver shifts to larger sizing with a tighter value range because the blinds' combined defense creates more dead money and the nut advantage is even more pronounced.

---

### Example E2 -- BTN vs SB+BB on Two-Tone Board, 3-Way (Big Bet on Specific Textures)

- **Source:** GTO Wizard / poker.pro -- "Multiway Muscle: Big-Bet Windows"
  - https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/
- **Setup:** BTN opens, SB calls, BB calls. 3-way SRP.
- **Board:** A-clubs 9-clubs 4-diamonds (flop), K-clubs (turn -- front door flush completes)
- **Action:** Flop checks through or small bet. Turn Kc completes the club draw.
- **Correct play:** If holding the nut flush or made flush, BET 70-90% POT on the turn. Multiway ranges are full of pair+draw combos that hit or missed. The completed flush texture puts immense pressure on two opponents simultaneously. Each must fear the other has the flush.
- **Bluff selection:** If bluffing, use A-clubs Q-spades type hands (nut club blocker + overcards that block opponents' strongest continues).
- **Verification:** Solver-verified (GTO Wizard 3-way solver)
- **Principle:** **Big-bet windows exist multiway when nut edge, last position, and scare cards converge.** The default "always small multiway" fails on these turns because the completed draw creates a polarization opportunity.

---

### Example E3 -- LJ vs SB+BB, 3-Way (Drastically Reduced C-Bet Frequency)

- **Source:** GTO Wizard -- "10 Tips for Multiway Pots"
  - https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/
- **Setup:** LJ opens, SB calls, BB calls. 3-way SRP.
- **Board:** Various (aggregate strategy)
- **Action:** Flop checks to LJ. LJ must decide c-bet frequency.
- **Correct play:** LJ c-bets MUCH less frequently compared to HU. The solver shows a dramatic drop in c-betting frequency when facing two opponents vs. one. The reason: LJ does not have position (BTN would), the nut advantage is less pronounced from early position, and each additional opponent doubles the chance someone has connected with the board.
- **Verification:** Solver-verified (GTO Wizard aggregate data)
- **Principle:** **Bluff compression.** Multiway pots have a terrible risk/reward ratio on pure bluffs. If you bet and need both opponents to fold, the combined probability of getting through is much lower (e.g., if each folds 60% HU, the probability both fold is only 36%). The solver compensates by drastically cutting bluffing frequency.

---

## Category F: Turn and River Specific Multiway Examples

### Example F1 -- Turn Probing OOP in 3-Way Pot (BB Probes After Flop Checks Through)

- **Source:** GTO Wizard -- "Probing Out Of Position in 3-Way Pots"
  - https://blog.gtowizard.com/probing-out-of-position-in-3-way-pots/
- **Setup:** BTN opens, SB calls, BB calls. Flop checks through. Turn action on BB.
- **Board example:** A-hearts 8-hearts 7-diamonds (flop), 3-diamonds (turn)
- **Action:** Flop checks through (BTN checks back). Turn 3d. BB probes.
- **Correct play:** BB PROBES with a polarized range. Because the flop checked through, BTN has capped their range (no sets, no top pair with strong kicker, or they would have bet). BB can now probe the turn with strong made hands (slow-played two pair, sets) and bluffs (draws that picked up equity). The probe sizing is typically large (75%+ pot) because BB leverages a nut advantage on boards where their range includes the strongest hands the BTN's checked-back range lacks.
- **When turn is 3-hearts (third heart):** BB's betting pattern shifts to smaller sizing because the flush completing is less polarizing and BB has more medium-strength flush holdings.
- **Verification:** Solver-verified (GTO Wizard 3-way solver)
- **Principle:** **Checked-back ranges are capped multiway.** When the in-position player checks back in a 3-way pot, they have voluntarily given up an extremely profitable betting opportunity. This caps their range harder than HU (because they passed on betting against TWO opponents who showed weakness). The OOP player can exploit this with polarized probes.

---

### Example F2 -- River Decision on K-d T-h 9-d 4-c 8-d, 4-Way (Thin Call vs. Exploitative Fold)

- **Source:** Upswing Poker / Nick Petrangelo -- "Multiway Hand Analysis"
  - https://upswingpoker.com/multiway-double-straddle-hand/
- **Hero (Ginge):** K-clubs 9-clubs (two pair)
- **Board:** K-diamonds T-hearts 9-diamonds 4-clubs 8-diamonds
- **Action:** River 8d completes the diamond flush and makes a straight for QJ. Doug bets small ($5,500 into $19,100). Ginge folds.
- **GTO play:** K9 is theoretically a call (getting great odds, Doug should have enough bluffs in a balanced range). But Ginge's exploitative fold reflects the reality that most live players under-bluff rivers, especially in multiway pots where the betting line has been: bet into 3 players on flop -> called -> bet again on turn -> called -> bet river.
- **Verification:** Solver reference (Nick Petrangelo notes GTO says call, but endorses the exploitative fold)
- **Principle:** **Exploitative adjustment to under-bluffing on multiway rivers.** In theory, defend. In practice, multiway river bets (especially after a multi-street line) are almost always value. The presence of multiple opponents throughout the hand makes bluffing extremely risky, so most players under-bluff.

---

### Example F3 -- Set on 7-spades 7-diamonds on A-diamonds J-clubs 7-hearts Flop (Do NOT Slow-Play Multiway)

- **Source:** PokerNews -- "Multi-Way vs. Heads-Up Pots: Five Key Strategic Differences"
  - https://www.pokernews.com/strategy/multi-way-vs-heads-up-pots-five-key-strategic-differences-23528.htm
- **Hero cards:** 7-spades 7-diamonds (set of sevens)
- **Board:** A-diamonds J-clubs 7-hearts (flop)
- **Positions:** Multiple opponents (3+ way)
- **Action:** Hero flops middle set. Must decide: slow-play or bet?
- **Correct play:** BET. Do not slow-play. Against a single opponent, checking with a set on AJ7 to trap can be profitable. Against multiple opponents, the risk of giving free cards to multiple draws (flush draws, straight draws like QT/KQ/KT, or even just overcards that pair up) makes slow-playing negative EV. The probability that at least one of multiple opponents improves to beat you is much higher.
- **Verification:** Expert opinion (PokerNews strategy article)
- **Principle:** **Slow-playing is much more dangerous multiway.** With one opponent, the chance they outdraw you on the turn is manageable. With 2-3 opponents, the combined probability of being outdrawn skyrockets. Always lean toward betting/raising sets and strong hands multiway.

---

## Category G: Bluff Compression and Pure Bluffs Failing Multiway

### Example G1 -- Pure Bluffs Are Nearly Worthless Multiway (Aggregate)

- **Source:** GTO Wizard -- "10 Tips for Multiway Pots in Poker"
  - https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/
- **Setup:** Any multiway pot (3+ players)
- **Concept:** If you need one opponent to fold for a bluff to work, and they fold 50% of the time, your bluff succeeds 50% of the time. If you need TWO opponents to fold and each folds 50%, your bluff succeeds only 25% of the time. If each folds 60%, your bluff works 36% of the time. The risk/reward ratio for pure bluffs collapses multiway.
- **Correct play:** With the exception of river spots, NEVER bluff without drawing equity multiway. Semi-bluffs with nut draws are acceptable; pure air bluffs are not.
- **Verification:** Solver-verified (GTO Wizard aggregate data across boards)
- **Principle:** **Bluff compression.** The mathematical reality of needing multiple opponents to fold simultaneously compresses the bluffing range to near-zero. This is the most fundamental difference between HU and multiway play.

---

### Example G2 -- Bluff Selection Multiway: Use Nut Blockers, Not Air

- **Source:** GTO Wizard / poker.pro -- "Multiway Muscle"
  - https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/
- **Board:** A-clubs 9-clubs 4-diamonds (flop)
- **Bluff candidate:** A-clubs Q-spades (nut club blocker, overcard, blocks AQ/AK continues)
- **Why this hand bluffs:** It blocks the nut flush draw (has the A-clubs), blocks strong Ax hands that would call, and has backdoor equity. Against two opponents, blocking their strongest continues is essential because the bluff needs to get through twice.
- **Avoid bluffing with:** Complete air (no pair, no backdoors, no relevant blockers). These hands have zero equity when called and no blocking effect to increase fold probability.
- **Verification:** Solver-verified (GTO Wizard)
- **Principle:** **Blocker importance amplifies multiway.** Blockers interact with more ranges (2+ opponents instead of 1), making card removal effects more powerful. The solver's bluffing range multiway is almost exclusively hands with nut blockers and backup equity.

---

## Category H: Defense and Calling Adjustments

### Example H1 -- Defense Burden Splits Across Players

- **Source:** GTO Wizard -- "GTO Wizard AI 3-Way Benchmarks"
  - https://blog.gtowizard.com/gto_wizard_ai_3_way_benchmarks/
- **Setup:** BTN opens, SB calls, BB calls. BTN overbets.
- **Concept:** Facing an overbet HU, the defender needs to defend ~44% of their range (based on MDF). Facing the same overbet in a 3-way pot, the average burden of defense drops to ~25% per player. Each player can fold more because the other player's calling absorbs part of the defense requirement.
- **Correct play:** Tighten calling ranges significantly. Hands that are mandatory defenses HU (like middle pair, weak top pair) become folds multiway because someone else will absorb the bluffing EV.
- **Verification:** Solver-verified (GTO Wizard 3-way solver)
- **Principle:** **Shared defense burden.** The minimum defense frequency per player drops in multiway pots. This means each individual player should fold MORE, not less, compared to HU. Counterintuitively, this makes overbetting potentially more effective multiway on the right textures because each player is folding a higher percentage.

---

## Summary Table

| # | Category | Hero Hand | Board | Street | Correct 3-Way Action | HU Would Be | Principle |
|---|----------|-----------|-------|--------|----------------------|-------------|-----------|
| A1 | TP check/fold | AQ | Q96 | Flop | Fold to check-raise | Call/raise | Range narrowing |
| A2 | TP check | QcJc | Qs3s4d | Flop | Check behind | C-bet or float | Equity dilution |
| A3 | Overpair caution | AA | KsTs6c | Flop | Bet small only | Bet large for value | Equity dilution |
| A4 | TP check turn | AK | Ks7d6c Qd | Turn | Check (after 2 callers) | Barrel turn | Range narrowing |
| B1 | Draw check-fold | KcQc | 7s5s4c | Flop | Check-fold | C-bet semi-bluff | Board texture vs range |
| B2 | Draw fold | Td9d | 4dAc7d | Flop | Fold facing raise | Call or raise | Reverse implied odds |
| B3 | Draw call only | 8h9h | Qd6hTc | Flop | Call (not raise) | Raise as semi-bluff | Reduced fold equity |
| C1 | Thin value bet | JJ | T52r | Flop | Bet 1/3 pot | Bet 50-75% pot | Vulnerable overpair sizing |
| C2 | Thin value 3 streets | 9hTs | JdTd9c | All | Value bet all streets | Same | Factor combination |
| C3 | Bet for protection | JcJd | Js8h5d | Flop | Bet (don't slow-play) | Can slow-play | Protection betting |
| D1 | Call don't raise | Kc9c | KdTh9d 4c | Turn | Call (not raise) | Raise for value | Bet-and-call signal |
| D2 | Cascading narrows | Any TP | AK3 | Flop | Fold to bet-call-raise | Call or raise | Cascading signals |
| E1 | Larger c-bet | Strong Ax | AK4r | Flop | C-bet 55-75% | Range-bet small | Nut advantage |
| E2 | Big turn bet | Nut flush | Ac9c4d Kc | Turn | Bet 70-90% | Bet 60-75% | Big-bet windows |
| E3 | Reduced c-bet | Various | Various | Flop | C-bet much less | Range c-bet | Bluff compression |
| F1 | Turn probe OOP | Polar range | Ah8h7d 3d | Turn | Probe big, polarized | Probe smaller | Capped ranges |
| F2 | River fold exploit | Kc9c | KdTh9d4c8d | River | Exploitative fold | GTO call | Under-bluffing rivers |
| F3 | Don't slow-play | 7s7d | AdJc7h | Flop | Bet (never trap) | Can slow-play | Slow-play danger |
| G1 | No pure bluffs | Air | Any | Any | Never bluff without equity | Can bluff | Bluff compression |
| G2 | Blocker bluffs only | AcQs | Ac9c4d | Flop | Bluff with blockers | Bluff wider | Blocker importance |
| H1 | Fold more vs bets | Medium pairs | Any | Any | Fold more often | Defend wider | Shared defense burden |

---

## Key Sources

- GTO Wizard Blog (solver-verified): https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/
- GTO Wizard -- Playing IP vs Two Callers: https://blog.gtowizard.com/playing-in-position-against-two-callers/
- GTO Wizard -- Probing OOP 3-Way: https://blog.gtowizard.com/probing-out-of-position-in-3-way-pots/
- GTO Wizard -- 3-Way Benchmarks: https://blog.gtowizard.com/gto_wizard_ai_3_way_benchmarks/
- GTO Wizard -- Custom Multiway Solving: https://blog.gtowizard.com/gto-wizard-ai-custom-multiway-solving/
- Poker.pro -- Multiway Muscle / Big-Bet Windows: https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/
- Upswing Poker -- Nick Petrangelo Multiway Analysis: https://upswingpoker.com/multiway-double-straddle-hand/
- Phil Galfond -- Mastering Multi-Way Pots: https://www.philgalfond.com/articles/mastering-multi-way-pots
- Card Player / Jonathan Little -- multiple articles (linked above)
- LearnWPT / PokerNews -- multiple hand examples (linked above)
- CrushLivePoker -- Thin Value in 3-Bet Pots: https://crushlivepoker.com/articles/thin-value-in-3-bet-pots
- MyPokerCoaching / Fedor Holz -- Multiway Postflop: https://www.mypokercoaching.com/fedor-holz-multiway-pots-postflop/
- Card Player / Alex Fitzgerald -- Five Multiway Exploits: https://www.cardplayer.com/poker-news/28642-poker-strategy-with-alex-fitzgerald-five-multiway-pot-exploits
