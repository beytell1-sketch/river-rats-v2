# GTO Review: Sweep Design Documents

**Reviewer:** GTO QA Agent
**Date:** 6 April 2026
**Documents reviewed:**
1. `DESIGN_POSITION_AMP_SWEEPS.md` — 79 situations (8 boards)
2. `DESIGN_CALL_SWEEPS.md` — 72 situations (8 boards)

**Reference:** `agent_context.txt` (GTO knowledge base v1.1)

---

## 1. DESIGN_POSITION_AMP_SWEEPS.md

### Verdict: ISSUES FOUND

---

### 1.1 Card Conflicts

**PASS** -- No card conflicts found across all 8 boards. Every hero hand uses cards not present on the board.

Verified board-by-board:
- Board 1 (Ac 8d 3s): All hero hands clean.
- Board 2 (9d 6c 2h): All hero hands clean.
- Board 3 (Jh 8h 4h): All hero hands clean. Note: hands like 6h5h and Kh9h use hearts that are NOT on the board (board uses Jh, 8h, 4h specifically).
- Board 4 (Qc Qd 7s): All hero hands clean. Note: Qh9c and Qh Jh use Qh which is NOT on the board (board has Qc, Qd).
- Board 5 (Ts 9d 5c 7h): All hero hands clean.
- Board 6 (Ad 9d 4c): All hero hands clean. Note: Ad Kc (#8) uses Ad which IS on the board. **CARD CONFLICT FOUND.**
- Board 7 (Jc 8c 5d 2h): All hero hands clean.
- Board 8 (Qc 8d 3s 6h 2c): All hero hands clean.

**CRITICAL -- Board 6, Situation #8:** Hero hand is "Ad Kc" but the board is "Ad 9d 4c". The Ad appears in BOTH hero's hand and the board. This is physically impossible. Must fix -- change hero hand to e.g. "Ah Kc" or "As Kc".

Revised verdict for card conflicts: **FAIL (1 conflict)**

---

### 1.2 Label Accuracy

Reviewing each board against GTO knowledge base principles:

**Board 1 (Ac 8d 3s, dry A-high rainbow, OOP lead):**
- #1-4 CHECK: Correct. Air through middle pair on A-high board, can't bet for value OOP 3-way.
- #5 Ah4c BET: **QUESTIONABLE.** Top pair worst kicker on a raiser-favoured board. The knowledge base says "top pair weak kicker is a pot-control hand, not a value hand" (Section 1.2) and "TP weak kicker equity drops to ~38-42% 3-way" (dilution table). OOP on a board that heavily favours CO's range, Ah4c is near the bottom of Ax. CO has AK, AQ, AJ, AT all dominating. This is closer to CHECK than BET. The design rationale argues "protection" but with two opponents who both have better Ax hands frequently, a bet is thin. **Flag for GTO Expert review -- may be CHECK.**
- #6-8 (A9, AJ, AK) BET: Correct. These are strong enough Ax to bet for value and protection.
- #9-10 (sets) BET: Correct. Must bet sets 3-way.

**Board 2 (9d 6c 2h, low connected rainbow, OOP lead):**
- #1-5 CHECK: Correct.
- #6 9c7c BET: Correct. Top pair must protect 3-way.
- #7 9hTh BET: Correct.
- #8 JhJd BET: Correct. Overpair must charge on low board. This is the MW-28 target case.
- #9-10 BET: Correct.

**Board 3 (Jh 8h 4h, monotone, OOP lead):**
- #1-2 CHECK: Correct.
- #3 6h5h BET (low flush): Correct. Made flush must bet even if low.
- #4 9d8d CHECK (middle pair no heart): Correct.
- #5 JdTc CHECK (top pair no heart): Correct. Very vulnerable on monotone.
- #6 Ah3c BET (nut flush draw): **QUESTIONABLE.** The knowledge base explicitly states: "DO NOT barrel draws into 2 opponents" (DO NOT Rule #2) and "Semi-bluffs require nut draws... Check and realize equity, or check-raise only with the nut draw" (Section 1.1). Leading OOP with the nut flush draw as a semi-bluff into 2 opponents is debatable. The knowledge base says fold equity 3-way is ~36%, which is below breakeven for most bet sizes. However, the nut flush draw has 9 clean outs (~36% equity) plus the draw is to the nuts, giving strong implied odds. On balance, this is a borderline spot. The label BET is defensible as a small lead for protection/semi-bluff with the absolute nuts draw, but CHECK (to check-raise or check-call) is also GTO-viable. **Flag for Expert -- could go either way.**
- #7 JcJd BET (set no heart): Correct. Must protect against flush draws.
- #8-10 BET (flushes): Correct.

**Board 4 (Qc Qd 7s, paired dry, OOP lead):**
- #1-5 CHECK: Correct. Below the board pair or too thin.
- #5 7h6h CHECK: **Note** -- hand description says "Trips kicker (middle pair)" but 7h6h on QcQd7s is actually a pair of 7s, not trips. The category label is misleading. It's middle pair (sevens), not trips. The reasoning says "only 7s boat draw" which is correct but the category header is wrong.
- #6 KhKd BET (KK overpair): **QUESTIONABLE.** On a paired board (QQ7), OOP 3-way, KK is vulnerable. CO's opening range contains AQ, KQ, QJ, QTs -- all of which have trips. With two opponents, the chance at least one has a Q is significant. The knowledge base says "top pair is medium-strength 3-way" -- KK on this board is functionally similar to an overpair that loses to trips. Betting for value is thin when the board pairs at the top. However, there are fewer Q combos (only 2 queens left: Qh, Qs), so this is defensible. **Borderline -- lean BET but flag for Expert.**
- #7 AhAd BET: Similar reasoning but stronger. Correct.
- #8-9 (Trips) BET: Correct.
- #10 (Full house) BET: Correct.

**Board 5 (Ts 9d 5c 7h, connected turn, OOP lead after checks):**
- #1-5 CHECK: Correct.
- #6 Tc8c BET: Correct. Top pair + gutshot, must charge draws after both check.
- #7 TsJd BET: **CARD CONCERN.** Ts is on the board (Ts 9d 5c 7h). Hero holds "Ts Jd". **CARD CONFLICT FOUND.** The Ts is on the board AND in hero's hand. Must fix -- change to e.g. "Td Jd" or "Th Jd".
- #8 8h6h BET (made straight): Correct.
- #9 TdTc BET (top set): **CARD CONCERN.** Board has Ts. Hero holds TdTc. This is fine -- hero has two tens (Td, Tc) and the board has Ts. Three tens accounted for. No conflict.
- #10 9s9h BET: Board has 9d. Hero has 9s, 9h. Fine -- no conflict.

**Board 6 (Ad 9d 4c, A-high two-tone, facing bet):**
- #1-2 FOLD: Correct.
- #3-4 CALL (flush draws): Correct.
- #5 9c8c FOLD: Correct. Middle pair facing bet+call on A-high, dominated.
- #6-7 CALL (top pair hands): Correct.
- #8 AdKc RAISE: Already flagged as card conflict (Ad on board). Beyond the conflict, the label logic is sound -- TPTK should raise to thin the field.
- #9-10 RAISE (sets): Correct.

**Board 7 (Jc 8c 5d 2h, mid-connected turn, facing barrel):**
- All labels look correct. Note Board 7 has 9 situations (not 10).
- #6 8h7h FOLD (second pair facing turn barrel): Correct per knowledge base -- middle pair facing multi-street aggression.
- #8-9 RAISE (sets): Correct.

**Board 8 (Qc 8d 3s 6h 2c, river brick, OOP lead):**
- #1-2 CHECK: Correct.
- #3 KhJh BET (K-high as bluff): **QUESTIONABLE.** Bluffing with K-high OOP into 2 opponents on the river. The knowledge base says "Pure bluffs are unprofitable 3-way" (Section 1.1) and the bluff-to-value ratio 3-way is ~1:4. With two opponents, the fold equity needed is much higher. Even though opponents' ranges are capped by the turn check-through, K-high has some showdown value (beats other missed draws). Turning it into a bluff destroys that showdown value. **This should likely be CHECK.** K-high has too much SDV to bluff with, and not enough fold equity against 2 opponents.
- #4 CHECK: Correct.
- #5-8 BET (top pair variants): Correct. Opponents capped by turn check.
- #9-10 BET (sets): Correct.

**Label accuracy summary:** 2 card conflicts, 3-4 questionable labels. Most labels are sound.

---

### 1.3 Realistic Game States

**PASS with minor notes.**

- All pot sizes, bet sizes, and stack depths are plausible for 100bb 6-max.
- Board 7 note says "BB folded on flop" making it HU on the turn, which is correctly noted. The situation started 3-way, which is appropriate for 3-way training data (the preflop ranges were 3-way even though it's now HU).
- Board 8 pot of 200 after flop bet + call and turn check-through is realistic.
- All preflop action sequences are standard.

---

### 1.4 Summary Table Errors

The summary table (line 281) for Board 7 shows "2 RAISE, 2 CALL" in the BET/CALL/RAISE column, but the actual Board 7 hands show 2 FOLD, 3 CALL, 2 RAISE. That's 7 hands accounted for in the table, but Board 7 has 9 hands (2 FOLD + 3 CALL + 2 RAISE = 7). Counting the actual table: hands 1-2 FOLD, 3-5 CALL, 6 FOLD, 7 CALL, 8-9 RAISE = 3 FOLD, 4 CALL, 2 RAISE = 9 total. The summary says "2 FOLD, 3 CALL" but it should be "3 FOLD, 4 CALL." **Minor bookkeeping error in the summary table.**

Also the total label distribution claims: CHECK 27, BET 33, FOLD 4, CALL 9, RAISE 5 = 78, not 79. Recount needed. Board 7 has 3 FOLD (not 2), 4 CALL (not 3), and 2 RAISE, which changes the totals.

---

## 2. DESIGN_CALL_SWEEPS.md

### Verdict: ISSUES FOUND

---

### 2.1 Card Conflicts

Verified board-by-board:

- Board 1 (Jd 8d 4c): All clean. Td9d (#5) uses Td and 9d -- Jd and 8d are on board, Td and 9d are not. Clean.
- Board 2 (Ks 9h 5d): All clean.
- Board 3 (Qh 7c 2s 5d): **Situation #8: Qh Kh.** Board has Qh. Hero has Qh. **CARD CONFLICT.** The Qh is on the board AND in hero's hand. Must fix -- change to e.g. "Qd Kd" or "Qc Kc" (but 7c and 2s are taken). "Qs Kh" or "Qd Kh" would work.
- Board 4 (Ah 9c 3s 6d Tc): All clean. Checked each hand against all 5 board cards.
- Board 5 (Kd Jc 6s): Hero hand #6 KhQh -- clean. #7 KsJd -- Ks and Jd not on board (Kd and Jc are). Clean. Wait -- #8 "Jh Ts" -- Jh is not Jc, clean. All clean.
- Board 6 (Ts 8h 3s): All clean. Td7d (#8) -- Td is not Ts. Clean.
- Board 7 (As Qd 5h): **Situation #6: As Js.** Board has As. Hero has As. **CARD CONFLICT.** Must fix -- change to e.g. "Ah Jh" or "Ac Jc".
- Board 8 (7h 7d 5s 9c Js): Checking all hands against 5 board cards. #1 Ts8s -- 8s not on board. Wait, 5s is on board. Ts8s -- neither T nor 8 of spades on board. Clean. #2 Ks7c -- 7c not on board (7h, 7d are). Clean. #3 JdJc -- Jd not Js, Jc not on board. Clean. #4 9s9c -- 9c IS on board. **CARD CONFLICT.** Hero has 9c but board has 9c. Must fix. #5 AdKd -- clean. #6 As7s -- 7s not on board (7h, 7d), As not on board. Wait, 5s IS on board but hero doesn't have 5s. Clean. Actually wait -- #7 5c5s -- board has 5s. **CARD CONFLICT.** Hero has 5s, board has 5s. Must fix. #8 7s5c -- 7s not on board (7h, 7d are), 5c not on board (5s is). Clean. Actually wait -- the board is 7h 7d 5s 9c Js. Hero #8 is 7s5c. 7s is NOT on the board (7h and 7d are). 5c is NOT on the board (5s is). Clean.

Let me re-verify Board 8 conflicts:
- Board: 7h, 7d, 5s, 9c, Js
- #4: 9s, 9c -- **9c is on the board. CONFLICT.**
- #7: 5c, 5s -- **5s is on the board. CONFLICT.**

**Card conflicts found in CALL SWEEPS: 4 total (Board 3 #8, Board 7 #6, Board 8 #4, Board 8 #7)**

---

### 2.2 Label Accuracy

**Board 1 (Jd 8d 4c, flop, draw calls):**
- #1-2 FOLD: Correct.
- #3 9h7h CALL (OESD): Correct. 8 outs, ~32% equity, pot odds 27%.
- #4 Qd3d CALL (flush draw): Correct.
- #5 Td9d CALL (combo draw): Correct. Massive equity with combo draw.
- #6 AdKs CALL (overcards): **BORDERLINE.** Two overcards with no made hand and no direct draws. The knowledge base Example 7 (AK on Jd8d4c) explicitly covers this exact board and concludes CALL due to 6 hidden overcard outs. The label matches the knowledge base. Correct.
- #7-9 CALL: Correct. Middle/top pair hands calling a c-bet.

**Board 2 (Ks 9h 5d, flop, bluff-catchers IP):**
- #1-4 FOLD: Correct. No equity, no draws at this price.
- #3 Th8h FOLD (gutshot at 33% price): Correct. 4 outs = ~8% per street, not enough.
- #5-6 CALL (middle pairs): Correct.
- #7-8 CALL (top pair variants): Correct.
- #9 AsAh RAISE: Correct. Overpair vs BB donk bet.

**Board 3 (Qh 7c 2s 5d, turn barrel):**
- #1-3 FOLD: Correct.
- #4 5h5c RAISE (set): Correct. Set at SPR 0.6, get stacks in.
- #5 QdJd CALL: Correct. TPGK facing double barrel, just calling.
- #6 QsTs CALL: Correct.
- #7 7d6d FOLD: Correct. Middle pair vs double barrel.
- #8 QhKh CALL: **CARD CONFLICT already flagged.** Beyond the conflict, TPTK calling a double barrel at SPR 0.6 is correct.
- #9 2c2d RAISE: Correct. Bottom set raising.

**Board 4 (Ah 9c 3s 6d Tc, river):**
- #1-4 FOLD: Correct. Air and underpair/middle pair on river.
- #5-7 CALL (top pair variants): Correct. Villain capped by turn check.
- #8 Tc9c RAISE (two pair): **QUESTIONABLE.** River raise for value with two pair is reasonable against a capped range, but the pot is 280, villain bet 140, and raising means putting in a large amount. At effectively all-in (SPR 0.0), a raise is really a shove. Two pair on Ah9c3s6dTc is strong but loses to AT (better two pair), 33, TT, 99, and any set. Villain checked the turn and then bet the river -- this could be thin value with top pair or a delayed bluff. Raising risks only getting called by better. **Flag for Expert -- CALL may be safer.**
- #9 3h3d RAISE (set): Correct.

**Board 5 (Kd Jc 6s, flop, anti-over-call with caller behind):**
- #1-4 FOLD: Correct.
- #5 KcTh FOLD (top pair bad kicker facing bet + cold-call): Correct. This mirrors MW-30 exactly. The bet-and-call signal overrides raw equity.
- #6 KhQh CALL: Correct. TPGK just barely strong enough.
- #7 KsJd RAISE (two pair): Correct. Strong enough to raise for value.
- #8 JhTs FOLD (middle pair): Correct.
- #9 AcQc FOLD (overcards facing bet+call): Correct. No draws, two strong opponents.

**Board 6 (Ts 8h 3s, flop, wet board draws):**
- #1-2 FOLD: Correct.
- #3 7s6s CALL (flush draw + gutshot): Correct. 13 outs, massive draw.
- #4 AsKh CALL (nut flush draw): **NOTE.** As gives nut flush draw in spades (board has Ts, 3s). Kh is an overcard. This is correct -- nut flush draw at 22% price is a clear call. But the equity estimate of 0.30 seems reasonable with NFD + 2 overcards.
- #5-6 CALL: Correct.
- #7 3d3c RAISE: Correct. Bottom set on wet board must raise to deny equity.
- #8-9 CALL: Correct.

**Board 7 (As Qd 5h, flop, facing check-raise):**
- #1-4 FOLD: Correct. Air through second pair vs check-raise.
- #5 AhJh FOLD (top pair vs check-raise): Correct. Mirrors MW-31. Check-raise on AQ5 in 3-way = nuts.
- #6 AsJs FOLD (TPGK vs check-raise): **CARD CONFLICT flagged.** Label logic is correct -- even TPGK folds to 3-way check-raise.
- #7 AcKc CALL (TPTK): **DEBATABLE.** The knowledge base says "Even top pair top kicker folds to a 3-way check-raise" (Section 2, Factor 5). The design argues AK is just barely strong enough to call. But the action description says "CO raises to 90" after hero bet 30 and BB checked. This is CO raising hero's bet (not a check-raise from BB). CO's raise of hero's c-bet is strong but not as extreme as a check-raise. The action history description header says "Facing Check-Raise" but the actual action is: BB checks, hero bets, CO raises. That's a raise (not a check-raise by CO -- CO didn't check then raise; CO just raised). This is an important distinction. A raise from CO over hero's bet is strong but not necessarily nuts-only. TPTK calling this raise is more defensible than calling a true check-raise. **The board theme label "Facing Check-Raise" is misleading -- this is actually facing a raise from CO.** Label CALL for AK is acceptable in this context.
- #8 AdQd RAISE (top two): Correct.
- #9 5s5d RAISE (set): Correct.

**Board 8 (7h 7d 5s 9c Js, river, trips facing check-raise):**
- #1 Ts8s FOLD (straight facing c/r): Correct. Straight loses to all boats/quads on paired board.
- #2 Ks7c FOLD (trips facing c/r): Correct. Exact MW-46 mirror.
- #3 JdJc CALL (full house JJ over 77): Correct.
- #4 9s9c CALL: **CARD CONFLICT flagged.** Label logic is correct.
- #5 AdKd FOLD: Correct.
- #6 As7s FOLD (trips best kicker): Correct.
- #7 5c5s CALL: **CARD CONFLICT flagged.** Label logic is correct.
- #8 7s5c RAISE (full house): The reasoning note is confused ("77 over 55 AND 55 over 77... actually 775 gives hero quads potential is wrong"). Hero has 7s and 5c. Board is 7h 7d 5s 9c Js. Hero makes a full house: 777-55. That's three 7s and two 5s. This is actually very strong -- trips 7s full of 5s. But quads requires four 7s and hero only has one. The confused self-correction in the reasoning is sloppy but the label RAISE is correct -- this is the near-nuts on this board (only quad 7s beats it, which requires the other player to have the remaining 7). Actually with three 7s on board+hand (7h, 7d on board, 7s in hand) and 5s on board + 5c in hand, hero has 777-55 full house. The only hands that beat it: 77xx for quads (impossible, only 7c remains and no one has two 7s), or J-high full house JJ over 77 (JdJc -- which IS in the range as situation #3). Wait -- 777-55 vs JJJ-77: hero's 777-55 is three-of-a-kind 7s full, while JdJc makes JJ full of 77 (77-JJ). Actually: JdJc on 7h7d5s9cJs makes JJJ-77 (three jacks, pair of 7s) which is a weaker full house than 777-55 (three 7s, pair of 5s). Three 7s beats three jacks? No -- in standard poker rankings, three Jacks beats three 7s. So JJJ-77 > 777-55. So situation #3 (JdJc) actually beats situation #8 (7s5c). The label RAISE for 7s5c is still reasonable as a value raise since the hand is still very strong, but it's not "second nuts" as claimed. **The reasoning text is incorrect about hand rankings -- JJ full house beats 7-5 full house on this board. The label RAISE is still correct but the reasoning needs correction.**

---

### 2.3 Realistic Game States

**PASS with notes.**

- Board 5 has 4-way preflop action (CO opens, BTN calls, SB calls, BB calls) narrowing to 3-way on the flop. This is realistic.
- Board 7 action history: "BB checks, hero bets 30, CO raises to 90, BB folds." But the setup says CO is the primary villain and hero is BTN. The action sequence is: hero (BTN) bets the flop after BB checks, then CO raises. This is a CO raise over BTN's bet with BB still in the pot initially. Plausible.
- Board 8 action history involves HJ open, CO call, BTN call, BB call -- 4-way pot narrowing to 2-way. Started multiway which is appropriate.
- All pot sizes, bet sizes, and SPRs are realistic for 100bb 6-max.

**One concern: Board 5 pot math.** Preflop with CO open, BTN call, SB call, BB call -- if CO opens to 3bb, BTN calls 3bb, SB calls 3bb (completing from 0.5bb), BB calls 3bb (already has 1bb in). That's 3+3+3+3 = 12bb in calls, but SB posted 0.5bb and BB posted 1bb, so total pot = 12 + 0.5 (already posted by SB) + 1 (already posted by BB) = ... Actually standard: 4 players x 3bb = 12bb pot preflop (SB and BB posted blinds that are part of their call). Pot = 12bb. Then CO bets 35 on a 155 pot? Wait -- the pot is listed as 155 and the flop bet is 35. With 4 callers at 3bb each, preflop pot would be 12bb = 120 chips (if 1bb = 10 chips). Then 155 seems slightly off unless there's rake or the blinds are structured differently. Actually if BB = 10 and SB = 5, with CO opening to 30, BTN calls 30, SB calls 30, BB calls 30 (adds 20 more), pot = 30+30+30+20+5(SB already in)+10(BB already in) = actually just 30 x 4 = 120 + any dead money. The pot of 155 doesn't quite match. But this is close enough for training purposes -- the exact pot math doesn't need to be precise to the chip as long as it's in the right ballpark. **Minor.**

---

### 2.4 Board 3 Hero Position Note

Board 3 says hero is BTN (IP) but the action says "CO opens, BTN (hero) calls, BB calls. Flop Q72r: CO bets 33, hero calls, BB folds." After BB folds on flop, it's HU on the turn: CO vs BTN. Hero IS IP here. But the design purpose is 3-way CALL training. The flop call was 3-way (before BB folded). The turn call is HU. **This is fine for training -- the flop decision (call vs fold vs raise facing CO's bet with BB behind) was the 3-way moment, and the turn continues from that.**

---

## 3. Card Conflict Summary (CRITICAL)

| Design | Board | Situation | Conflict | Fix |
|--------|-------|-----------|----------|-----|
| Position Amp | 5 | #7 TsJd | Ts on board + in hand | Change to ThJd or TdJd |
| Position Amp | 6 | #8 AdKc | Ad on board + in hand | Change to AhKc or AsKc |
| Call Sweeps | 3 | #8 QhKh | Qh on board + in hand | Change to QsKh or QdKh |
| Call Sweeps | 7 | #6 AsJs | As on board + in hand | Change to AhJh or AcJc |
| Call Sweeps | 8 | #4 9s9c | 9c on board + in hand | Change to 9s9d or 9h9d |
| Call Sweeps | 8 | #7 5c5s | 5s on board + in hand | Change to 5c5h or 5d5h |

**6 total card conflicts across both designs. All must be fixed before generation.**

---

## 4. Redundancy Check

### Within Position Amp Sweeps

Moderate redundancy in anchor hands (air and nuts extremes), but this is by design -- each board needs anchors. The boundary hands (equity 0.35-0.55) are sufficiently different across boards due to texture variation. **No problematic duplicates.**

However:
- Board 1 #5 (Ah4c, top pair weak kicker on A-high) and Board 6 #6 (Ac5c, top pair weak kicker on A-high) are very similar situations -- both are weak-kicker Ax on A-high boards, OOP. Board 6 has facing_bet=True which differentiates the decision, so these are acceptable.

### Within Call Sweeps

- Board 5 #5 (KcTh FOLD, top pair bad kicker vs bet+call) and Board 7 #5 (AhJh FOLD, top pair vs check-raise) teach the same anti-over-call concept but in different action contexts (bet+call vs raise). **Acceptable -- different signals.**
- Board 1 #3 (9h7h OESD) and Board 6 #5 (9h7h OESD): Same hero hand, same draw type, similar boards. Board 1 is Jd8d4c and Board 6 is Ts8h3s. The draws are similar (open-enders on middle-connected boards). **Mild redundancy -- consider changing one hand to add diversity.**

### Between the Two Designs

- Position Amp Board 6 (Ad 9d 4c, facing bet) and Call Sweeps Board 1 (Jd 8d 4c, facing bet) are both two-tone flop boards with OOP hero facing a CO c-bet. The hero hands differ and the board textures differ (A-high vs J-high), so these are complementary, not redundant.
- No significant cross-design redundancy found.

---

## 5. Coverage Gap Analysis

### What the designs cover well:
- OOP leading decisions on varied board textures (Position Amp Boards 1-5, 8)
- OOP facing bets/raises (Position Amp Boards 6-7, Call Sweeps Boards 1, 5-7)
- IP facing bets (Call Sweeps Boards 2-4, 8)
- Anti-over-call (Call Sweeps Boards 5, 7, 8)
- Draw equity thresholds (Call Sweeps Boards 1, 6)
- River decisions (Position Amp Board 8, Call Sweeps Boards 4, 8)

### Missing or underrepresented:

1. **Turn barrel spots as OOP caller.** Call Sweeps Board 3 is a turn barrel spot but hero is IP. There is no situation where hero is OOP facing a turn barrel and must decide CALL vs FOLD. This is a common real-game scenario. Position Amp Board 7 has OOP hero facing a turn barrel but that design labels it as FOLD/CALL/RAISE for the Position Amp axis, not specifically CALL training.

2. **Multiway check-raise from OOP.** Position Amp covers OOP leading and OOP facing bets. Neither design covers the OOP check-raise decision (hero checks, villain bets, hero raises). This is an important OOP aggression spot. Board 3 situation #6 in Position Amp (Ah3c semi-bluff lead) touches on this but a dedicated check-raise sweep would add coverage.

3. **3-bet pot situations.** All 16 boards are single-raised pots. The Call Sweeps design itself flags this as Open Question #3. 3-bet pots have different SPRs, tighter ranges, and different GTO strategies. At least 1-2 boards in 3-bet pots would improve coverage.

4. **Monotone board CALL decisions.** Position Amp Board 3 covers monotone for BET/CHECK. Call Sweeps has no monotone board. When facing a bet on a monotone board without a flush, the CALL vs FOLD decision is important and distinct from other textures.

5. **Sandwich position (middle player).** The knowledge base emphasizes that sandwich position is the "worst seat" with unique strategic considerations. Neither design puts hero in the sandwich. All heroes are either first to act (OOP) or closing action (IP). A board with hero as the sandwich player (e.g., CO opens, BB [hero] faces bet from CO with BTN still behind) would cover this gap. Actually wait -- Board 1 of Call Sweeps does this: BB faces CO bet with BTN behind. That IS sandwich position. But it's only in one board.

---

## 6. Axis Coverage Assessment

### position_amplification (33% warm-start, need improvement)

**Well targeted.** The Position Amp design directly addresses the OOP CHECK-to-BET boundary with 60 lead-decision situations across 6 boards of varying texture. The diversity of board types (dry, wet, paired, monotone, connected) ensures the model sees OOP betting is context-dependent, not a blanket rule. The 19 facing-bet situations add FOLD/CALL/RAISE decisions for OOP heroes. **This should significantly improve the axis.**

### CALL decisions (11 samples, need volume)

**Well targeted.** The Call Sweeps design adds 27 CALL labels, bringing the total from 11 to 38. The Position Amp design adds another 9 CALL labels (Boards 6-7), potentially reaching 47 total. The CALL situations span draws, bluff-catchers, and anti-over-call contexts. **Sufficient volume increase.**

### spr_interaction (83% preserved, don't break)

**Low risk.** Both designs use standard pot sizes and SPRs (0.0 to 1.1). The Call Sweeps design explicitly varies SPR across boards. No extreme or unusual SPRs that would confuse the model. **Should preserve the axis.**

### nut_potential (67% preserved, don't break)

**Moderate risk.** Both designs include hands across the full strength spectrum (air to nuts). The Position Amp monotone board (Board 3) specifically tests flush-related nut potential. However, neither design explicitly tests situations where hero has nut potential but not the current nuts (e.g., holding a set on a board with flush draws -- hero has nut potential via board pairing). The nut_potential axis may not get additional positive signal. **Monitor but likely preserved.**

---

## 7. Specific Findings Summary

### CRITICAL (must fix before generation)

| ID | Issue | Location |
|----|-------|----------|
| C1 | Card conflict: Ts in hand and on board | Position Amp, Board 5, #7 |
| C2 | Card conflict: Ad in hand and on board | Position Amp, Board 6, #8 |
| C3 | Card conflict: Qh in hand and on board | Call Sweeps, Board 3, #8 |
| C4 | Card conflict: As in hand and on board | Call Sweeps, Board 7, #6 |
| C5 | Card conflict: 9c in hand and on board | Call Sweeps, Board 8, #4 |
| C6 | Card conflict: 5s in hand and on board | Call Sweeps, Board 8, #7 |

### HIGH (label accuracy concerns -- flag for GTO Expert)

| ID | Issue | Location |
|----|-------|----------|
| H1 | Ah4c BET may be CHECK -- TP worst kicker on raiser-favoured board OOP | Position Amp, Board 1, #5 |
| H2 | Ah3c BET semi-bluff OOP violates DO NOT Rule #2 (don't barrel draws into 2 opp) | Position Amp, Board 3, #6 |
| H3 | KhJh BET bluff OOP into 2 opponents violates "pure bluffs unprofitable 3-way" | Position Amp, Board 8, #3 |
| H4 | Tc9c RAISE on river -- two pair raising may only get called by better | Call Sweeps, Board 4, #8 |
| H5 | Board 7 theme says "Facing Check-Raise" but action is actually CO raising hero's bet | Call Sweeps, Board 7 header |

### MEDIUM (clarity/correctness issues)

| ID | Issue | Location |
|----|-------|----------|
| M1 | Board 4 #5 category says "Trips kicker" -- should be "Middle pair" (7h6h = pair of 7s, not trips) | Position Amp, Board 4 |
| M2 | Board 8 #8 reasoning confused about hand rankings (JJ full > 77 full) | Call Sweeps, Board 8 |
| M3 | Summary table miscount: Board 7 has 3 FOLD not 2, 4 CALL not 3 | Position Amp, summary |
| M4 | Total label count sums to 78 not 79 in summary | Position Amp, summary |

### LOW (nice-to-have improvements)

| ID | Issue | Location |
|----|-------|----------|
| L1 | 9h7h appears in both Call Sweeps Board 1 #3 and Board 6 #5 -- mild redundancy | Call Sweeps |
| L2 | No 3-bet pot boards in either design | Both |
| L3 | No monotone CALL decision board | Call Sweeps |

---

## 8. Recommended Actions

### Before generation (mandatory):
1. Fix all 6 card conflicts (C1-C6). Simple suit swaps.
2. Flag H1-H4 for GTO Expert independent evaluation. These are the boundary hands where a wrong label propagates the worst errors.
3. Fix M1-M2 text errors.
4. Recount and correct the Position Amp summary table (M3-M4).

### Before training (recommended):
5. Correct the Board 7 theme label in Call Sweeps (H5) -- it says "check-raise" but the action is a standard raise.
6. Consider changing Position Amp Board 8 #3 (KhJh) from BET to CHECK. Bluffing OOP into 2 opponents on the river with a hand that has showdown value contradicts the knowledge base.

### For future batches (optional):
7. Add 1-2 boards in 3-bet pot scenarios (L2).
8. Add a monotone board to the Call Sweeps design (L3).
9. Diversify one of the duplicate 9h7h hands (L1).

---

## 9. Overall Verdict and Risk Assessment

**Position Amp Sweeps: ISSUES FOUND -- fixable. Solid design with 2 card conflicts and 2-3 debatable labels.**

**Call Sweeps: ISSUES FOUND -- fixable. Strong design with 4 card conflicts and 1-2 debatable labels.**

**Combined risk assessment: LOW-MEDIUM after fixes.**

The 6 card conflicts are critical showstoppers but trivially fixable (suit swaps). The debatable labels (H1-H4) are genuinely close decisions where reasonable GTO players could disagree -- they should go to the GTO Expert for independent evaluation rather than being hard-coded either way.

The designs are well-targeted at the identified gaps. The Position Amp design directly attacks the v8 failure mode (OOP hero always checking). The Call Sweeps design addresses severe CALL starvation (11 to 38+ samples). Board texture diversity is good. Street coverage spans flop through river. The IP/OOP split is balanced in Call Sweeps and deliberately OOP-heavy in Position Amp (which is the point).

The biggest strategic risk is not in the designs themselves but in the absence of 3-bet pot boards. If the model encounters 3-bet pots in production and has never trained on one, the tighter ranges and lower SPRs may cause errors. This is a coverage gap for a future batch, not a blocker for this one.

**Recommendation: Fix the 6 card conflicts, flag the 4 debatable labels for Expert review, correct the text errors, and proceed to generation.**
