---
date: 2026-05-22
from: ARCHITECT (parallel 5-way reference workstream)
to: Main terminal (orchestrator) + Owner + Solver (verification)
re: DRAFT design — 10-hand 5-way reference set (MW-51 through MW-60); fills MASTER_PLAN §2 partition gap (0 → 5-10 hands); preparatory for v9-5way eval gate
status: DRAFT — DESIGN ONLY (no labels assigned; solver + owner verification follows)
scope: hand-crafted situation specs, NOT solver replay. Architect's GTO reasoning produces a SUGGESTED action/bucket per hand. Solver verifies. Owner arbitrates.
---

# DRAFT — 5-way reference set design memo (MW-51 through MW-60)

## 1. Context

### 1.1 Why this set is needed

`docs/MASTER_PLAN (1).md` §2 defines the multiway reference partition:

| Opponents | Hands | Status |
|-----------|-------|--------|
| 1 (HU) | 4 | OK |
| 2 (3-way) | 24 | OK |
| 3 (4-way) | 12 | Tight but OK (35 expanded since master plan) |
| **4+ (5-way)** | **0** | **Must add 5-10 before v9-5way ships** |

This memo proposes **10 expert-designed 5-way hands** (`num_opponents_at_decision = 4`) to fill that gap. The reference set is the **eval gate** for the trained 5-way specialist model. It is NOT training corpus. Each hand must be:

- Hand-crafted (not generated from a self-play runner)
- Stratified across street, position, action context, hand strength, board texture, structural feature
- Specifically chosen to STRESS v9-4way's blind spots when stepped up to 5-way
- Solvable on actual poker engines (legal card combos, legal action sequences)
- Labelled by **owner + solver verification**, not by architect's suggestion (which is anchor only)

### 1.2 Gated dependencies

This work is **preparatory** and runs in parallel with Phase 2-F1 corpus expansion. v9-5way training is gated on:

1. v9-4way ships and passes its eval gate
2. 5-10 5-way reference hands exist with **owner+solver-verified labels** (this memo + verification rubric)

This memo delivers (1) the design + (2) the unlabelled spec; verification rubric (separate deliverable) defines how labels are then attached.

### 1.3 Distinction: 5-way vs 4-way

In production routing (`oracle_router.py`), `num_opponents = 4` (5 players including hero) is the **catch-all** for all 4+ opponent pots (5-way through 9-way). For this reference set:

- All 10 hands have **`num_opponents_at_decision = 4`** (i.e., 5 players in the pot at the decision point)
- Hands assume 6-max table where 5 of 6 seats see the flop (only one fold, typically BB folds or UTG folds depending on action)
- For preflop spots, the action chain reaches hero with 4 villains already in (e.g., UTG opens, MP calls, CO calls, BTN calls, hero in blind closing)

### 1.4 What changes from 4-way → 5-way

The 5-way step introduces decision dynamics not stress-tested in the 4-way reference:

1. **Squeeze geometry intensifies**: 4 cold-callers + opener = squeeze frequency higher; hero in late position with 3+ flatters has very different range vs. 4-way
2. **Pot cascade is steeper**: bet → call → call → call → fold or call possibilities multiply; bet-and-call sequences narrow ranges harder
3. **Equity dilution worsens**: hero's raw equity drops further as more villains stay in
4. **Range chain narrowing depth**: 4 villains' independent ranges narrow across action — much narrower than 4-way analog
5. **Closing-action OOP from BB**: BB closing into 4 cold-callers is a fundamentally different range than BB closing 3
6. **Multi-villain action chains**: different villains can bet on different streets (e.g., CO bets flop, BTN bets turn) — a 5-way reference must include these chains

## 2. Stratification design

### 2.1 Eight-axis tag schema (per existing reference set patterns)

Each hand carries 8 stratification tags:

1. `street` — preflop / flop / turn / river
2. `position` — UTG / MP / HJ / CO / BTN / SB / BB
3. `action_context` — opener / facing-bet / facing-raise / facing-bet-and-call / closing-action / no-bet-OOP-first
4. `hand_strength` — monster / medium-made / weak-made / draw / air
5. `board_texture` — rainbow_dry / two_tone / paired / monotone / preflop
6. `villain_chain_type` — single-villain-action / multi-villain-action-chain / bet-and-call / 3-bet-pot
7. `hero_role` — opener / cold-caller / blind-closer / squeezer / bet-faced / bet-and-call-faced
8. `multiway_dimension` — squeeze-spot / equity-dilution / range-chain-narrowing / pot-cascade / closing-action / SPR-interaction / nut-potential

### 2.2 Target coverage (mandated by task)

| Dimension | Target | Plan |
|-----------|--------|------|
| Streets | 3 flop + 3 turn + 2 river + 2 preflop | MW-51, MW-52, MW-58 (flop); MW-54, MW-55, MW-57 (turn); MW-59, MW-60 (river); MW-53, MW-56 (preflop) |
| Hero positions | ≥1 of each EP/MP/CO/BTN/SB/BB | UTG (MW-55) / MP (MW-58) / HJ (MW-53) / CO (MW-52) / BTN (MW-51, MW-57) / SB (MW-54, MW-59) / BB (MW-56, MW-60) — wait: full check at §3 |
| Action contexts | ≥3 facing-raise | MW-52, MW-58, MW-60 facing-raise; MW-54 facing bet-and-call; MW-51, MW-55, MW-59 facing bet; MW-53, MW-56 closing preflop; MW-57 no-bet (checked OOP) |
| Hand strength | 2 monster, 3 medium-made, 2 weak-made, 2 draw, 1 air | per §3 table |
| Board texture | 2 rainbow_dry, 3 two-tone, 2 paired, 1 monotone, 2 preflop | per §3 table |
| Squeeze spot | ≥1 | MW-53 (squeeze spot: HJ opens, CO flats, BTN flats, hero(SB) squeezes vs 3 in) |
| Multi-villain action chains | ≥2 | MW-58 (CO bets flop, BTN raises flop, hero faces raise), MW-60 (CO bets flop, hero calls, MP bets turn, hero calls, BTN bets river facing hero) |

### 2.3 Cell coverage matrix (filled / TBD)

Each cell below is "filled" if at least one MW-51..60 hand covers it.

| Axis | Filled | TBD |
|------|--------|-----|
| street: preflop | MW-53, MW-56 | — |
| street: flop | MW-51, MW-52, MW-58 | — |
| street: turn | MW-54, MW-55, MW-57 | — |
| street: river | MW-59, MW-60 | — |
| hero pos: UTG | MW-55 | — |
| hero pos: MP | MW-58 | — |
| hero pos: HJ | — | not covered (acceptable: 6-max HJ + MP collapse to same range) |
| hero pos: CO | MW-52 | — |
| hero pos: BTN | MW-51, MW-57 | — |
| hero pos: SB | MW-53, MW-54, MW-59 | — |
| hero pos: BB | MW-56, MW-60 | — |
| context: opener | — | not covered (5-way decisions are mostly post-open) |
| context: closing-action | MW-53, MW-56 | — |
| context: facing-bet | MW-51, MW-55, MW-59 | — |
| context: facing-raise | MW-52, MW-58, MW-60 | — |
| context: facing-bet-and-call | MW-54 | — |
| context: no-bet (checked) | MW-57 | — |
| hand_strength: monster | MW-52 (KK 3-bet vs squeeze), MW-58 (set-of-eights) | — |
| hand_strength: medium-made | MW-51, MW-57, MW-60 | — |
| hand_strength: weak-made | MW-55 (TPmidkick), MW-59 (under-pair on draw-heavy river) | — |
| hand_strength: draw | MW-54 (nut FD), MW-56 (suited Ace closing) | — |
| hand_strength: air | MW-53 (squeeze with bluff-suited-broadway) | — |
| board: rainbow_dry | MW-51 (K72r), MW-55 (Q83r-turn) | — |
| board: two_tone | MW-52, MW-54, MW-58 | — |
| board: paired | MW-57 (88x), MW-60 (river-paired-board) | — |
| board: monotone | MW-59 (3-spade river) | — |
| board: preflop | MW-53, MW-56 | — |
| squeeze-spot | MW-53 | — |
| multi-villain chain | MW-58, MW-60 | — |
| 3-bet-pot | MW-52 (4-bet pot in 5-way is impractical; MW-52 is squeeze-pot facing 3-bet from BTN) | — |

**Coverage gaps (acceptable per task):**
- No `opener` action context — in 5-way, hero-as-opener is preflop only and there's only 1 preflop opener (otherwise pot opens HU not 5-way). MW-53 (squeeze) is the closest analog and arguably covers this.
- No HJ hero position — collapses to MP/CO range in 6-max; covered indirectly by MW-58 (MP).

## 3. Situation specs

Each spec follows BATCH2_8_HAND_DESIGNS.md format. `num_opponents_at_decision = 4` for all 10.

---

### MW-51: Top pair, weak kicker; BTN IP facing CO single-barrel c-bet 5-way; K72r

**Target dimension:** Equity dilution × range-chain narrowing
**Hero cards:** Kh / 9h
**Board:** Ks 7d 2c
**Street:** Flop
**Hero position:** BTN
**Primary villain position:** CO (bettor)
**Other villains:** UTG (cold-caller), MP (cold-caller), BB (blind-closer)
**Num opponents at decision:** 4
**Pot bb:** 12.5 (each of 5 players put in 2.5bb)
**To call bb:** 3.0 (CO bets 25% pot)
**Stack:** 100bb effective
**Facing bet:** Yes
**Pot odds required:** 19.4%
**Opener position:** CO
**Bettor position:** CO

**Action history (preflop):** UTG opens 2.5bb, MP calls, CO calls, hero(BTN) calls, SB folds, BB calls. 5-way to flop.

**Action history (flop):** Pot 12.5bb. BB checks, UTG checks, MP checks, CO bets 3bb (25%). Hero (BTN) to act with BB / UTG / MP / behind (BB folded into earlier; CO is opener, so the chain is) — recheck: BB acts first on flop (out of position from BTN). Action order flop: BB, UTG, MP, CO, hero(BTN). BB checks, UTG checks, MP checks, CO bets 3 into 12.5. Hero acts with all 4 villains still in.

**Suggested correct action:** CALL (NO raise)
**Suggested size:** N/A (CALL)
**Suggested bucket label:** medium-made (TPweakkicker)

**5-way structural notes:**
- 5-way pot, CO's c-bet into 4 villains is **uncharacteristically thin** as a pure bluff — at this pot size and table density, the c-bet polarizes toward value (Kx good kicker, sets, AA-overpair). CO's value-heavy c-bet range narrows hero's relative strength.
- K9 is dominated by KQ, KJ, KT (CO's strong c-bet value range) and by sets (KK, 77, 22).
- However, hero closes the action — UTG, MP, BB all have ranges weighted toward middle-pair / ace-high air that will fold to a bet behind, so RAISE is dominated by inflating the pot vs a value-heavy CO.
- Call preserves position, controls pot, retains 2-out kicker outs.

**Architect's GTO reasoning:**
K9 in 5-way IP on K72r facing 25% c-bet from CO has ~30-35% equity vs CO's c-bet range (which in 5-way is value-tilted ~50% / bluff ~50% — much less polarized than 4-way because c-betting wide into 4 villains loses too much EV). Pot odds 19.4% needed → CALL is +EV. Raising commits stack vs villains who only continue with stronger Kx or sets. Position closure preserves equity-realization factor (~0.85).

**Confidence: MEDIUM** — close decision between CALL and FOLD; solver verification key. Architect leans CALL.

**Axis tags:**
- street: flop
- position: BTN
- action_context: facing-bet
- hand_strength: medium-made
- board_texture: rainbow_dry
- villain_chain_type: single-villain-action (CO only acted)
- hero_role: bet-faced (closing-action IP)
- multiway_dimension: equity-dilution

---

### MW-52: Pocket Kings; CO facing BTN 3-bet squeeze 5-way

**Target dimension:** Range-chain narrowing × squeeze pressure
**Hero cards:** Kc / Kd
**Board:** (preflop)
**Street:** Preflop
**Hero position:** CO
**Primary villain position:** BTN (3-bettor)
**Other villains:** UTG (opener), MP (cold-caller), SB (cold-caller), BB
**Num opponents at decision:** 4
**Pot bb:** 22 (UTG 2.5 + MP 2.5 + hero CO 2.5 + BTN 13 + SB 0.5 + BB 1 — wait, recount): UTG 2.5 + MP 2.5 + CO(hero) 2.5 + BTN 13 + SB 0.5 + BB 1 = 22bb
**To call bb:** 10.5 (hero already put in 2.5; BTN raised to 13)
**Stack:** 100bb effective (hero has 97.5 behind after call)
**Facing bet:** Yes (facing raise; this is `facing_raise = 1`)
**Pot odds required:** 32.3%
**Opener position:** UTG
**Bettor position:** BTN (3-bettor)

**Action history (preflop):** UTG opens 2.5bb, MP calls, hero(CO) calls, BTN raises to 13bb (squeeze), SB folds. Now action returns to UTG, then MP, then hero(CO). For this spec, hero acts BEFORE UTG/MP's response — actually action order requires UTG and MP to act first since they're earlier position. **Corrected**: After BTN's 3-bet, action goes UTG → MP → hero(CO). UTG calls, MP folds. Hero(CO) faces BTN's 3-bet to 13bb in a 4-way pot (UTG, hero, BTN, BB).

Wait — let me re-check the 5-way constraint. If MP folds, num_opps at decision = 3 (UTG, BTN, BB). To preserve 5-way: change to **UTG opens 2.5, MP calls, hero(CO) calls, BTN raises to 13, SB calls 13, BB calls 13**. Now action returns to UTG, MP, hero. For hero's decision to be 5-way, UTG and MP must still be in (or to-act). Simpler: **hero is FIRST to face the 3-bet**.

**Revised action history:** UTG opens 2.5bb, MP calls, hero(CO) calls, BTN raises to 13bb (squeeze), SB folds, BB calls 13bb. Action returns to UTG (calls 10.5), MP (calls 10.5). Now hero(CO) acts with UTG/MP/BTN/BB all in = 4 opponents.

**Pot at hero's decision:** UTG 13 + MP 13 + hero 2.5 (already in) + BTN 13 + BB 13 = 54.5bb. Hero to call 10.5bb. Pot odds: 10.5 / (54.5 + 10.5) = 16.2%.

**Suggested correct action:** RAISE (4-bet squeeze for value)
**Suggested size:** 36bb (3x the 3-bet size, solver-aligned 4-bet sizing in multi-cold-call pot)
**Suggested bucket label:** monster (premium pair)

**5-way structural notes:**
- KK in CO faced with BTN's squeeze on top of 2 cold-callers (UTG + hero) where UTG and MP have called the 3-bet: range-narrowing tells us BTN's 3-bet range is value-tilted (very wide squeeze frequency is suppressed because BTN must beat 4 villains, not 1).
- However, UTG/MP cold-calling the 3-bet means they have call-the-3-bet ranges (TT-JJ, AQ, AJs-types) — not 4-bet-fold-or-call ranges.
- KK is at the absolute top of CO's range; 4-betting for value is mandatory. AA would also 4-bet; QQ would 4-bet some.
- 4-bet sizing in 5-way 3-bet pot: BTN's 3-bet was 13bb; UTG + MP flatted = pot is 54.5bb (huge dead money). 4-bet to 36bb is ~2.75x the 3-bet, leaving stack-to-pot ratio for postflop play if called.

**Architect's GTO reasoning:**
KK is the second-strongest hand in poker. In a multi-flat squeeze pot, KK's relative equity is preserved (we still have a top-2 hand vs all calling ranges). 4-betting for value gets folds from AK/QQ/JJ rarely (those flat or fold) and value from AA (rare). The squeeze pot has so much dead money that 4-betting prints. CALL is acceptable mix to keep stack manageable but solver would 4-bet KK at near-100% frequency in this structure.

**Confidence: HIGH** — KK in 5-way squeeze pot is unambiguously 4-bet for value.

**Axis tags:**
- street: preflop
- position: CO
- action_context: facing-raise (3-bet)
- hand_strength: monster
- board_texture: preflop
- villain_chain_type: 3-bet-pot
- hero_role: bet-and-call-faced (3-bet on top of 2 flatters)
- multiway_dimension: range-chain-narrowing

---

### MW-53: Air squeeze; SB closing action 5-way, squeezing into HJ open + 3 flatters

**Target dimension:** Squeeze spot × closing-action × pre-flop geometry
**Hero cards:** As / 5s
**Board:** (preflop)
**Street:** Preflop
**Hero position:** SB
**Primary villain position:** HJ (opener)
**Other villains:** CO (cold-caller), BTN (cold-caller), BB (closing behind)
**Num opponents at decision:** 4
**Pot bb:** 8 (HJ 2.5 + CO 2.5 + BTN 2.5 + hero SB 0.5 already posted) — UTG folded, MP folded
**To call bb:** 2.0 (to call HJ's open)
**Stack:** 100bb effective
**Facing bet:** Yes (open + flats; hero closing-action vs open)
**Opener position:** HJ
**Bettor position:** HJ

**Action history (preflop):** UTG folds, MP folds, HJ opens 2.5bb, CO calls, BTN calls, hero(SB) to act with 0.5bb posted and BB behind. 5-way potential pot if hero + BB both call (4 villains).

Hero's decision: FOLD / CALL / RAISE (squeeze).

**Suggested correct action:** RAISE (squeeze) to 14bb
**Suggested size:** 14bb (mix of value-equity-from-A blocker + fold-equity from suited-Ace squeeze; 14 = ~6x open + bonus for cold-callers)
**Suggested bucket label:** air (squeeze with blocker, not a value hand)

**5-way structural notes:**
- A5s in SB with HJ opening + CO/BTN flatting: standard squeeze spot per modern GTO. Ace blocker reduces AA/AK combos in opponents' ranges; 5x gives wheel-equity backup if called.
- Hero is OOP for the rest of the hand if called → squeeze is the GTO preferred line over flat (flatting OOP in 5-way is dominated by reverse-implied-odds).
- Sizing: squeeze sizing in 6-max into 2 cold-callers + opener = ~5-6x open, NOT 3x (3x would be called too widely; needs to deny equity).
- 14bb squeeze size denies opponents' suited connectors / small pairs equity-realization; HJ folds 70%+ (only opens-with-call-range continues), CO/BTN fold ~80% (their flats fold to squeeze except QQ+/AK which 4-bet).
- BB closing behind: BB squeeze-cold-4-bet frequency from BB is real, ~10% over hero's squeeze. Acceptable risk.

**Architect's GTO reasoning:**
A5s in SB closing action with multi-flat squeeze opportunity is one of the **canonical pre-flop GTO squeeze spots**. Pure fold is too tight (gives up high-EV squeeze spot); pure call OOP in 5-way is dominated (no position, no closing on flop, ranges crush hero); squeeze captures pot equity from open + flats while preserving blocker effect. Sizing 5-6x open is solver-aligned. A5s is at the top of SB's pure-air-squeeze range (in equilibrium, SB squeezes ~3% with bluffs concentrated in A2s-A5s + suited connectors with blockers).

**Confidence: HIGH** — squeeze is well-established GTO line; A5s is canonical squeeze candidate.

**Axis tags:**
- street: preflop
- position: SB
- action_context: closing-action (vs open + 2 cold-calls; BB still behind)
- hand_strength: air
- board_texture: preflop
- villain_chain_type: 3-bet-pot (hero creates the 3-bet by squeezing)
- hero_role: squeezer
- multiway_dimension: squeeze-spot

---

### MW-54: Nut flush draw + gutshot; SB OOP facing CO bet + BTN flat, MP behind 5-way

**Target dimension:** Nut potential × bet-and-call range chain × OOP semi-bluff geometry
**Hero cards:** Ah / 9h
**Board:** Jh 7h 2c
**Street:** Flop
**Hero position:** SB
**Primary villain position:** CO (bettor)
**Other villains:** UTG (folded preflop; OOP not in pot — wait, must be 5-way; so 5 in pot)
**Re-pot 5 in pot:** UTG, MP, CO, BTN, hero(SB) — BB folded preflop
**Num opponents at decision:** 4 (UTG, MP, CO, BTN all still in)
**Pot bb:** 12.5
**To call bb:** 7.0 (CO bets 4bb; BTN flats 4bb; hero faces 4bb to call into 12.5+4+4 = 20.5)

Recompute: **Pot 12.5 (preflop) + CO bets 4 + BTN calls 4 = 20.5; hero to call 4; pot odds 4/(20.5+4) = 16.3%**

**Stack:** 100bb effective
**Facing bet:** Yes (bet-and-call)
**Pot odds required:** 16.3%
**Opener position:** UTG
**Bettor position:** CO

**Action history (preflop):** UTG opens 2.5bb, MP calls, CO calls, BTN calls, hero(SB) calls, BB folds. 5-way to flop.

**Action history (flop):** Pot 12.5. Hero(SB) checks, BB n/a (folded), UTG checks, MP checks, CO bets 4bb (32% pot), BTN calls. Action back to SB (hero) → UTG → MP. Hero (SB) acts first of the remaining un-acted villains. Hero faces 4bb bet + 1 caller into 20.5bb pot. UTG and MP still to act behind.

**Suggested correct action:** RAISE (check-raise semi-bluff to 16bb)
**Suggested size:** 16bb (4x bet, solver-aligned check-raise sizing in multiway)
**Suggested bucket label:** draw (nut flush draw + gutshot + 2 overcards = combo-draw monster)

**5-way structural notes:**
- 9 nut-flush outs + 4 gutshot outs (Tx for straight) + 6 overcard outs (Ax, but Ah is in hand → 3 As; same for K/Q overcards → 6 outs total). Adjusted outs ~14 (some overlap). Equity vs random hand ~50%; vs CO's bet-and-call range ~45-48%.
- **As blocker**: hero blocks Ax nut flush draws from CO/BTN — opponents holding flush draws are weaker (Kh, Qh, Th, etc.).
- CO + BTN bet-and-call sequence narrows their ranges to Jx-pair-or-better + sets + draws — c-bet-and-call into 4 villains is very value-heavy.
- Check-raise semi-bluff: pressures UTG/MP (who haven't acted yet — capped ranges, will fold near 100%) + CO/BTN forced to defend with Jx-or-better. Fold equity on UTG/MP/CO/BTN combined is real.
- Pure call: realizes draw equity at pot odds (need 16.3%, have 45%+) — clearly +EV call.

**Architect's GTO reasoning:**
Nut FD + gutshot + 2 overcards with As blocker, OOP in 5-way facing bet-and-call: solver mixes between CALL (realize equity passively) and RAISE (semi-bluff to capture dead money + fold equity). The architect's lean is RAISE (16bb check-raise) because:
1. UTG + MP behind have capped check-back ranges that fold to a CR
2. CO bet + BTN call commit to defending only with Jx-or-better; CR folds out their weakest defends
3. As blocker reduces villains' nut FD continuing combos
4. Hero builds the pot for nut flush hits
5. The combo-draw equity gives hero ~45% equity even if called by Jx — fold equity adds EV on top

However, the OOP position + 2 villains behind un-acted means CALL is acceptable mixed strategy (~30% frequency in solver). Architect's pure-play recommendation: RAISE (check-raise) ~70% / CALL ~30%.

**Confidence: MEDIUM** — solver may prefer pure CALL given OOP + 2 behind un-acted. Architect surfaces RAISE as primary; solver should verify the CALL vs RAISE mix.

**Axis tags:**
- street: flop
- position: SB
- action_context: facing-bet-and-call
- hand_strength: draw
- board_texture: two_tone
- villain_chain_type: bet-and-call (CO bet, BTN called; UTG/MP behind)
- hero_role: bet-and-call-faced (acting between CO/BTN action and UTG/MP behind)
- multiway_dimension: nut-potential / range-chain-narrowing

---

### MW-55: Top pair, medium kicker; UTG opener facing turn float-bet 5-way; Q83r-J

**Target dimension:** Multi-street range chain × hero-as-opener turn navigation
**Hero cards:** Qd / Jd
**Board:** Qc 8h 3s Jh
**Street:** Turn
**Hero position:** UTG
**Primary villain position:** BTN (turn bettor, leading after hero checks)
**Other villains:** MP, CO, BB (all in pot)
**Num opponents at decision:** 4
**Pot bb:** 12.5 (preflop) — flop checks through 5-way (hero(UTG) checked, MP checked, CO checked, BTN checked, BB checked). Turn pot 12.5bb.
**To call bb:** 8.0 (BTN bets 8bb on turn after hero checks)
**Stack:** 100bb effective
**Facing bet:** Yes (facing single bet on turn)
**Pot odds required:** 28%
**Opener position:** UTG
**Bettor position:** BTN

**Action history (preflop):** Hero(UTG) opens 2.5bb, MP calls, CO calls, BTN calls, SB folds, BB calls. 5-way to flop.

**Action history (flop):** Q83r. Hero(UTG) checks, MP checks, CO checks, BTN checks, BB checks. (All checked — flop checkdown caps all ranges.)

**Action history (turn):** J hits. Hero(UTG) checks, MP checks, CO checks, BTN bets 8 into 12.5 (65% pot — float-bet attempting to pick up the dead pot), BB folds.

Hero (UTG) acts with MP and CO still behind, facing BTN's 8bb bet into 12.5.

**Suggested correct action:** CALL
**Suggested size:** N/A (CALL)
**Suggested bucket label:** medium-made (TP-good-kicker that became TP-2-pair-blocker on J turn — actually Q-pair with J-kicker is still just TP-J-kicker; J turn does NOT pair hero's J because hero has QJ → wait: hero is QdJd, board Q-8-3-J → hero now has TWO PAIR (QQ + JJ) actually no: hero has Qd, board has Qc → one pair Q's; hero has Jd, board has Jh → one pair J's; **hero has TWO PAIR Q's + J's**)

**Re-classification:** Hero on turn has **two pair, top two (Q + J)** on Q83-J. This is a STRONG hand, not medium-made.

**Re-do suggested action:** RAISE (value-raise; solver-aligned ~3.5x bet = 28bb)
**Re-do suggested bucket label:** monster (top-two-pair on coordinated turn, hero-range-implies-strength)

**5-way structural notes (revised):**
- Top-two pair on Q83-J in 5-way is a near-monster hand. Only QQ, 88, 33, JJ (turn-set), Q8/Q3/QJ-other-suit beat hero.
- Flop checkdown 5-way caps everyone's range; BTN's turn-bet is a position-leveraged float that targets the dead-pot money — BTN's range is wide (Tx-Ax air + Jx mid-pair + occasional slowplay).
- Hero's check-raise sizing: 28bb (3.5x BTN's 8) builds pot, charges BTN's draws, denies equity from MP/CO behind. MP/CO will fold ~95% facing the raise (their checked-through flop ranges are very weak).
- Pure CALL is acceptable mix (~30% frequency) to keep MP/CO in for stack-extraction on river, but the architect's lean is RAISE because the turn is coordinated (J completes Q-T-X or some straights) and slow-playing risks bad river cards.

**Architect's GTO reasoning:**
Top-two pair on Q83-J with hero as preflop opener checked-through flop: hero's range is the strongest of the 5 ranges (UTG opener has the tightest preflop range, then checked flop). BTN's turn bet is read as range-bet-position-leveraged float, not a tight value bet. Hero's equity vs BTN's turn-bet range is ~70%. Value-raise dominates flat. Sizing 3.5x = 28bb in solver-aligned multiway turn raise.

**Confidence: MEDIUM-HIGH** — leaning HIGH. Solver verification on raise vs call mix would refine.

**Axis tags:**
- street: turn
- position: UTG
- action_context: facing-bet
- hand_strength: monster (revised from medium-made)
- board_texture: rainbow_dry → board now Qc8h3sJh = two-tone with backdoor flush from J (Jh + 8h = 2 hearts on board)
- villain_chain_type: single-villain-action (BTN turn only)
- hero_role: opener (hero opened pre)
- multiway_dimension: range-chain-narrowing (flop checkdown caps; turn lead from BTN narrows)

---

### MW-56: Suited ace closing-action preflop 5-way BB; QQ open + 3 flats

**Target dimension:** Closing-action OOP × range-asymmetry (BB closes 4 cold ranges)
**Hero cards:** As / 4s
**Board:** (preflop)
**Street:** Preflop
**Hero position:** BB
**Primary villain position:** CO (opener)
**Other villains:** UTG (cold-caller), MP (cold-caller), BTN (cold-caller); SB folded
**Num opponents at decision:** 4
**Pot bb:** 11.5 (UTG 2.5 + MP 2.5 + CO 2.5 + BTN 2.5 + SB 0.5 + BB 1)
**To call bb:** 1.5 (hero BB needs to call 1.5 to close)
**Stack:** 100bb effective
**Facing bet:** Yes (call to close)
**Pot odds required:** 11.5%
**Opener position:** CO
**Bettor position:** CO

**Action history (preflop):** UTG folds — wait, UTG must be in for 5-way. Let me re-spec.

**Revised:** UTG calls 2.5bb (cold? No, UTG can't "call" preflop — UTG is first to act). Let's instead say: **UTG opens 2.5bb, MP calls, CO calls, BTN calls, SB folds, hero(BB) closes.**

**Pot:** UTG 2.5 + MP 2.5 + CO 2.5 + BTN 2.5 + SB 0.5 + BB 1 = 11.5. To call 1.5.

**Suggested correct action:** CALL
**Suggested size:** N/A
**Suggested bucket label:** draw (suited Ace = implied-odds peeling hand, not a made hand yet)

**5-way structural notes:**
- A4s in BB closing 4 cold-callers + open: incredible pot odds (11.5%), implied odds for nut flush (5-out flush draws hit ~5% directly on flop but realize flush ~12% by river when 2 hearts come; nut flush blocker means villains can't have nut flush draw → hero's flush is nut), wheel-straight outs (any 5-3-2 board), top-pair outs.
- 5-way SRP IP-OOP factor: hero is OOP for the whole hand (BB), so equity realization factor is lower (~0.6-0.65). But pot odds 11.5% are so good that fold is impossible.
- Squeeze 3-bet alternative: 3-betting into 4 villains' combined cold-call range is dominated — villains have committed and call-3-bet ranges include AA-QQ + AK that hero loses to.
- Flat is the clear GTO play.

**Architect's GTO reasoning:**
A4s in BB closing 4 cold-callers + open: this is one of the canonical implied-odds peel spots. Suited Ace closes at 100% frequency in solvers at this pot-odds depth. Squeeze 3-bet is dominated. Fold is wrong (gives up 11.5% pot odds equity).

**Confidence: HIGH** — closing-action call is unambiguous.

**Axis tags:**
- street: preflop
- position: BB
- action_context: closing-action
- hand_strength: draw (preflop suited Ace = drawing hand)
- board_texture: preflop
- villain_chain_type: single-villain-action (only opener bet; flatters are passive)
- hero_role: blind-closer
- multiway_dimension: closing-action

---

### MW-57: Overpair on paired turn; BTN IP no-bet (checked-through) 5-way; 884-2

**Target dimension:** Pot-control × range-cap interpretation × overpair-on-paired-board
**Hero cards:** Th / Tc
**Board:** 8d 8s 4c 2h
**Street:** Turn
**Hero position:** BTN
**Primary villain position:** CO (preflop aggressor, checked flop)
**Other villains:** UTG, MP, BB
**Num opponents at decision:** 4
**Pot bb:** 12.5 (preflop) — flop and turn checked through 5-way
**To call bb:** 0 (no bet faced)
**Stack:** 100bb effective
**Facing bet:** No
**Opener position:** CO
**Bettor position:** None

**Action history (preflop):** UTG folds — must keep 5-way. Revised: UTG calls (cold-limp? No, UTG opens.) **Final**: UTG opens 2.5bb, MP calls, CO calls, hero(BTN) calls, SB folds, BB calls. 5-way.

**Action history (flop):** 884r (paired-low). All check (5-way pot, no one has Ax-8x-bluff-value). Pot 12.5.

**Action history (turn):** 2h. Hero now faces decision after UTG, MP, CO, BB all check.

Wait — hero(BTN) acts LAST. Action: BB checks, UTG checks, MP checks, CO checks, hero(BTN) to act. Hero can BET or CHECK.

**Suggested correct action:** CHECK
**Suggested size:** N/A
**Suggested bucket label:** medium-made (overpair on paired board with trip-blocker absence)

**5-way structural notes:**
- TT overpair on 8-8-4-2: hero loses to any 8x (4 + 4 = 8 combos of 8x in villains' ranges), 44 (set; 3 combos), 88 (quads; 1 combo), 22 (set; 3 combos), all overpairs JJ/QQ/KK/AA (rare; would've c-bet flop).
- 5-way flop checkdown caps all ranges to non-overpair, non-set, non-8x hands. Hero's TT is now AT THE TOP of the SDV range.
- Turn check-through caps further. Hero's TT is roughly 65-70% equity vs the remaining 5-way SDV pool.
- Why not BET turn for value: betting into 4 villains' capped ranges still loses to any 8x slowplay (which exists in checked-through 5-way) and gets called only by 22, 44, 9x (overpair-mid that wants showdown), Jx, Qx (lower SDV). Value vs bluff-catch tension: not enough value targets to justify betting OOP into 4 villains.
- CHECK preserves SPR for river decisions and avoids being check-raised by slowplay 8x.
- Donk-bet alternative: BET 4bb (~30% pot) gets value from BB's J/Q/K-high air SDV — but in 5-way the bet folds out the bluff-catch range too.

**Architect's GTO reasoning:**
TT overpair on 8-8-4-2 with 4 villains in pot and checked-through flop+turn: this is a textbook pot-control SDV spot. Hero's range is capped (would've c-bet TT flop in 3-way+ if value-confident, but in 5-way checked for pot control). Solver checks-back ~85% frequency, small thin-bet ~15% (vs BB-only ranges). Architect leans CHECK.

**Confidence: MEDIUM-HIGH** — CHECK is the dominant play but solver may surface a small thin-bet frequency.

**Axis tags:**
- street: turn
- position: BTN
- action_context: no-bet (checked-through)
- hand_strength: medium-made (overpair, top-of-SDV-range)
- board_texture: paired
- villain_chain_type: single-villain-action (no villain has acted aggressively)
- hero_role: bet-faced (no-bet IP closing)
- multiway_dimension: pot-cascade / SPR-interaction

---

### MW-58: Set facing flop raise (multi-villain action chain) 5-way; MP hero

**Target dimension:** Multi-villain action chain × set-strength on connected board
**Hero cards:** 8h / 8c
**Board:** Ts 9d 8s
**Street:** Flop
**Hero position:** MP
**Primary villain position:** BTN (raiser)
**Other villains:** CO (initial bettor), SB, BB
**Num opponents at decision:** 4
**Pot bb:** 12.5 preflop — flop CO bets 4, hero(MP) calls (wait, hero is in MP earlier than CO; hero acts before CO on flop)

Action order on flop (5-way): SB, BB, UTG (folded preflop? Let me re-spec) — need to ensure 5-way. **Revised**: UTG folds preflop; not 5-way. **Need 5 in**.

**Final preflop spec:** UTG opens 2.5bb, hero(MP) calls, CO calls, BTN calls, SB folds, BB calls. 5-way (UTG, MP, CO, BTN, BB) = 5 players. ✓

**Flop action order (OOP-first)**: BB acts first → UTG → hero(MP) → CO → BTN. So:
- BB checks, UTG checks, hero(MP) checks (hero slowplays set), CO bets 4bb (~32% pot), BTN raises to 14bb (~3.5x CO's bet).
- Action returns to BB (folds), UTG (folds), hero(MP). **Hero(MP) faces 14bb raise after slowplaying set; CO still behind.**

**Pot at hero's decision:** 12.5 (preflop) + CO 4 + BTN 14 = 30.5bb. To call 14bb.
**To call bb:** 14
**Stack:** 100bb effective
**Facing bet:** Yes (facing raise)
**Pot odds required:** 31.5%
**Opener position:** UTG (preflop)
**Bettor position:** CO (flop), BTN raised
**Num opponents at decision:** 4 (BB folded turn... wait, BB folded the raise, UTG folded the raise; CO still behind to act after hero. Let me recount opps still in: CO, BTN, BB, UTG — 4 villains)

Actually if BB and UTG fold to BTN's raise, then at hero's decision: BB out, UTG out, CO behind, BTN in. That's 2 opponents (CO + BTN), not 4.

**Revised to preserve 5-way decision:** Hero must act BEFORE BB and UTG, OR the raise must come from a player who acts AFTER hero.

**Re-spec from scratch — multi-villain action chain spot in 5-way (hero faces raise):**

UTG opens 2.5, hero(MP) calls, CO calls, BTN calls, SB folds, BB calls. 5-way preflop.

Flop Ts9d8s. Action order: BB → UTG → MP(hero) → CO → BTN.
- BB checks, UTG bets 4bb (donk-lead), hero(MP) raises to 14bb (semi-pressure raise w/ set), CO folds, BTN calls 14, BB folds, UTG calls 14.

Wait, this doesn't work — hero is the raiser, not the raise-faced.

**Alternative spec — hero faces raise with multi-villain chain BEFORE raise resolves:**

UTG opens 2.5, hero(MP) calls, CO calls, BTN calls, SB folds, BB calls. 5-way preflop.

Flop Ts9d8s. Action order: BB → UTG → MP(hero) → CO → BTN.
- BB checks, UTG checks, hero(MP) checks (slowplay set 8), CO bets 4bb, BTN raises to 14bb. Action returns to BB (will fold), UTG (will fold), hero(MP) decides — but UTG and BB still need to act after hero in this turn.

Actually re-checking order: once CO bets and BTN raises, action returns to the next-to-act player (BB), then UTG, then hero. So hero acts AFTER BB and UTG decide. If they fold, num_opps at hero = 2 (CO + BTN). Not 5-way.

**Resolution**: For a true 5-way decision facing raise, the raise must be from a player IN POSITION relative to hero such that the players still un-acted are still 4.

**Final final spec**: UTG opens, hero(MP) calls, CO calls, BTN calls, SB folds, BB calls. 5-way preflop.

Flop Ts9d8s. Action order BB → UTG → hero(MP) → CO → BTN.
- BB **bets** 4bb (donk-lead into 12.5), UTG **raises** to 14bb. Hero(MP) faces raise with set with CO and BTN still behind un-acted, plus BB still needs to defend or fold the raise after hero acts.

Pot at hero's decision: 12.5 + BB 4 + UTG 14 = 30.5. To call 14. **Opps still in (not yet folded)**: BB (acted, faces raise), CO (behind), BTN (behind), UTG (raised). That's 4 opponents — ✓ 5-way decision preserved.

**Action history (preflop):** UTG opens 2.5bb, hero(MP) calls, CO calls, BTN calls, SB folds, BB calls. 5-way to flop.

**Action history (flop):** Ts9d8s. BB donks 4bb (lead into 12.5), UTG raises to 14bb. Hero(MP) faces raise with set of 8's.

**Suggested correct action:** CALL (NOT 3-bet on flop)
**Suggested size:** N/A (CALL)
**Suggested bucket label:** monster (set on coordinated board — semi-monster due to straight texture)

**5-way structural notes:**
- 888 on T98 two-tone: hero has bottom set, but board has straights (QJ, J7, 67) and a flush draw (any-suit-with-2-spades).
- Multi-villain action chain — BB donks into pot, UTG raises = both showing strength. BB's donk + UTG's raise = at least one has T9 / two-pair / straight / set / combo-draw.
- 3-betting (squeeze the raise) commits hero to a huge pot OOP with 2 villains behind unacted (CO, BTN) — risk of running into higher set (99, TT) or straight is real.
- CALL retains position vs CO/BTN behind (they may call too, building hero's set-value) and preserves stack for board-friendly turns. Set on draw-heavy board needs to either commit big or pot-control; in 5-way the pot-control + see-turn line dominates.
- Sets need to go to value but in 5-way w/ raise-action-chain the raise range is value-tilted enough that 3-betting just gets sets-vs-sets / sets-vs-straight equity.

**Architect's GTO reasoning:**
Bottom set on coordinated 5-way board facing a multi-villain action chain (donk + raise) is a tougher CALL-vs-3-BET decision than it appears. Solver likely mixes: CALL 70% / RAISE 30%. Architect's pure play: CALL. The pot is already inflated, CO/BTN behind may call adding dead money to hero's set, and 3-betting commits hero stack against ranges that have hero crushed or even-money at best.

**Confidence: MEDIUM** — CALL vs RAISE mix is genuine; solver should verify. Architect's lean is CALL.

**Axis tags:**
- street: flop
- position: MP
- action_context: facing-raise
- hand_strength: monster (set)
- board_texture: two_tone (Ts9d8s = 2 spades — wait Ts and 8s = 2 spades; 9d = 1 diamond; two-tone confirmed)
- villain_chain_type: multi-villain-action-chain (BB donked, UTG raised, both showing strength)
- hero_role: bet-and-call-faced (faces donk + raise)
- multiway_dimension: range-chain-narrowing / pot-cascade

---

### MW-59: Under-pair on monotone river facing bet 5-way; SB hero on 3-spade river

**Target dimension:** Bluff-catch / monotone-board range narrowing × river decision
**Hero cards:** Tc / Td
**Board:** 7s 4s 2c 8h 5s
**Street:** River
**Hero position:** SB
**Primary villain position:** CO (bettor)
**Other villains:** UTG, MP, BTN, BB
**Num opponents at decision:** 4
**Pot bb:** 25 (flop-bet round adds; details below)
**To call bb:** 18 (CO bets 18 on monotone river)
**Stack:** 100bb effective
**Facing bet:** Yes
**Pot odds required:** 29.5%
**Opener position:** UTG
**Bettor position:** CO

**Action history (preflop):** UTG opens 2.5bb, MP calls, CO calls, BTN calls, hero(SB) calls, BB folds. 5-way to flop. Pot 12.5.

**Action history (flop):** 7s4s2c. SB(hero) checks, UTG checks, MP checks, CO bets 4 (~32%), BTN calls 4. SB(hero) calls 4. UTG folds, MP folds. Going to turn: 3-way (hero, CO, BTN). **WAIT — this loses 5-way at turn**.

**Re-spec to preserve 5-way through to river:** Need 5 still in at river decision. That requires very passive lines — most realistic 5-way river decisions have at most 2-3 villains by river. **Adjusted constraint**: 5-way decisions are dense pre-flop / flop / early-turn. River 5-way is rare but possible via flop checkdown + turn checkdown.

**Revised**: UTG opens 2.5, MP calls, CO calls, BTN calls, hero(SB) calls, BB folds. Flop 7s4s2c checked through 5-way (every player checks). Pot 12.5. Turn 8h checked through 5-way (every player checks). Pot 12.5. River 5s (3rd spade — monotone-river). hero(SB) acts first OOP — checks. UTG checks, MP checks, CO bets 18 (~140% pot — overbet polarized), BTN calls 18. Hero faces 18 to call with UTG and MP still behind.

**At hero's decision**: Pot 12.5 + CO 18 + BTN 18 = 48.5. To call 18. UTG and MP still un-acted (behind hero in the re-circuit). Num opps in: UTG, MP, CO, BTN = 4. ✓ 5-way preserved.

Actually no — after the river starts, hero(SB) is FIRST to act. Hero checked. Then UTG checked, MP checked, CO bet, BTN called. Now action returns to hero (SB), then UTG, then MP. So hero has 4 opps (all still in pot — UTG/MP have only checked, not folded), 3 unacted-after-hero. ✓ 5-way preserved.

**Suggested correct action:** FOLD
**Suggested size:** N/A
**Suggested bucket label:** weak-made (under-pair on monotone river vs polarized overbet)

**5-way structural notes:**
- River 5s = 3rd spade → monotone river. CO's polarized overbet (140% pot) range on monotone river after 5-way flop+turn checkdown is heavily flush-tilted (any spade higher than 7 = 8s/9s/Ts/Js/Qs/Ks/As-flush; or set/two-pair value).
- TT under-pair (no spade — Tc/Td are black) → hero has zero flush blocker and is below 8h (top-pair). Loses to: any flush, any two-pair (87, 75, 74, 72), any set (88, 77, 44, 22), any 8x with kicker, any higher pair.
- BTN cold-called the overbet — BTN's range here is flush-or-better OR a thin bluff-catch with set/two-pair. BTN's cold-call narrows further — almost certainly a flush.
- UTG / MP still behind: they may also call or raise; can be ignored for hero's decision since hero acts before them.
- Pot odds 29.5% — hero needs 30% equity vs CO+BTN combined range, which is realistically 5-10% (hero only beats stone bluffs which are nearly absent on monotone river overbet line).

**Architect's GTO reasoning:**
Under-pair (TT) on monotone river facing a polarized overbet + cold-call from CO+BTN in 5-way is the canonical "fold all bluff-catch SDV" spot. Solver folds ~95% frequency with TT here. Pure FOLD. The pot odds aren't enough to call a polarized range that is flush-or-better.

**Confidence: HIGH** — FOLD is unambiguous.

**Axis tags:**
- street: river
- position: SB
- action_context: facing-bet
- hand_strength: weak-made (under-pair on monotone river)
- board_texture: monotone (3 spades on river)
- villain_chain_type: bet-and-call (CO overbet + BTN cold-call)
- hero_role: bet-and-call-faced
- multiway_dimension: range-chain-narrowing / nut-potential (villain has nut potential, hero doesn't)

---

### MW-60: Two-pair on paired river, BB facing 3-street action chain ending in BTN bet; 5-way (or 4-way at decision; verify)

**Target dimension:** Multi-street range chain × paired-board reverse-equity × multi-villain action ladder
**Hero cards:** Ah / 5h
**Board:** Ad 5d 2c 8h 8c
**Street:** River
**Hero position:** BB
**Primary villain position:** BTN (river bettor)
**Other villains:** CO (flop bettor), MP (turn bettor), UTG (pre-aggressor, passive postflop)
**Num opponents at decision:** 4

**Action history (preflop):** UTG opens 2.5bb, MP calls, CO calls, BTN calls, SB folds, hero(BB) calls. 5-way to flop. Pot 12.5.

**Action history (flop):** Ad5d2c (two-tone diamond). Hero(BB) checks, UTG checks, MP checks, CO bets 4, BTN calls. Hero(BB) calls 4. UTG calls 4, MP folds. 4-way to turn.

Wait — for 5-way at river, need 5 still in. The flop call by hero, UTG, with CO/BTN: that's hero + UTG + CO + BTN = 4. MP folded. Not 5-way.

**Constraint reckoning**: 5-way at river is very rare because of folding cascade. Acceptable per task definition: "5-way pots = num_opponents = 4 at any decision point". This MW-60 spot can have num_opps = 4 at flop or turn but might drop to 3 by river. Let me re-spec to ensure num_opps = 4 at the actual decision point.

**Re-spec**: 5-way through turn; 4-way (num_opps=3) at river. **This violates the 5-way constraint**.

**Final re-spec to PRESERVE num_opps=4 at river**:

UTG opens 2.5, MP calls, CO calls, BTN calls, hero(BB) calls, SB folds. 5-way to flop.

Flop Ad5d2c. Hero(BB) **checks**. UTG checks. MP checks. CO checks. BTN checks. **Flop checks through 5-way**.

Turn 8h. Pot 12.5. Hero(BB) checks. UTG checks. MP checks. CO **bets 8bb** (turn float-bet attempting to scoop). BTN **calls 8bb**. Hero(BB) calls 8bb. UTG folds. MP folds. **Now 3 in at river (hero, CO, BTN)**. Not 5-way.

**Alternative**: To preserve 5-way at river, flop AND turn must check through 5-way. Then on river, hero(BB) is first to act and faces no action yet → that's not "facing a bet/raise" decision.

**Resolution — re-design MW-60**: Make it a TURN decision (not river) with multi-villain chain that preserves 5-way.

**MW-60 RE-DESIGN (TURN, MULTI-VILLAIN ACTION CHAIN):**

**Target dimension:** Multi-villain action chain (bet → raise → call → call) × turn decision × BB OOP
**Hero cards:** Ah / 5h
**Board:** Ad 5d 2c 8h
**Street:** Turn
**Hero position:** BB
**Primary villain position:** BTN (raiser on turn)
**Other villains:** UTG, MP, CO
**Num opponents at decision:** 4

**Action history (preflop):** UTG opens 2.5bb, MP calls, CO calls, BTN calls, SB folds, hero(BB) calls. 5-way preflop.

**Action history (flop):** Ad5d2c. Hero(BB) checks, UTG checks, MP checks, CO **checks**, BTN checks. Flop checks through 5-way (BTN's IP-check on a wet A-high board with 4 villains is unusual but realistic). Pot 12.5.

**Action history (turn):** 8h. Hero(BB) **checks**. UTG checks. MP **bets 4bb** (turn lead). CO calls 4. BTN **raises to 16bb**. Action returns to hero(BB) with UTG / MP / CO still in pot (UTG hasn't acted on the raise yet; MP has bet+now-faces-raise; CO has called now faces raise). 4 villains still in. ✓ 5-way decision preserved.

**Pot at hero's decision:** 12.5 + MP 4 + CO 4 + BTN 16 = 36.5bb. Hero needs 16 to call.
**To call bb:** 16
**Pot odds required:** 30.5%

**Suggested correct action:** FOLD
**Suggested size:** N/A
**Suggested bucket label:** weak-made (two-pair-top-and-bottom-on-paired-turn vs raise chain)

**5-way structural notes:**
- Hero has A5 of hearts = top-pair-Aces + bottom-pair-5's = TWO PAIR (A's and 5's) on a board where the 8 is now paired with… wait, board is Ad5d2c8h. Not paired. Two pair = Aces + Fives (hero's). A5 is bottom kicker for A-pair.

Actually: hero Ah5h on Ad5d2c8h. Hero pairs: A (with Ad) and 5 (with 5d). So hero has **two pair: Aces and Fives**. This is a strong hand on the flop, but on turn the action ladder (MP bets, CO calls, BTN raises) tells us:
- MP's turn lead = wakeup; likely set (88, 55, 22, AA — but AA had to slowplay flop) or two-pair-better (A8, 85)
- CO's call of MP's lead = strong: floats, sets, two-pair, top-pair-good-kicker
- BTN's raise from IP = monster: set, two-pair-better, slowplayed AA from flop, A8 turned-trips-equivalent (no, A8 = aces-with-8-kicker not trips)
- Hero's two-pair A5 loses to: AA (full house with the 5? AA has A's full of 5s if A5 in hero... no, AA+5 on board = 3 aces, no 5 in opp hand = top set. Actually A5 hero + Ad on board = 2 aces; AA in villain + Ad+5d on board = 3 aces (set) — set of aces. Hero loses), A8 (aces with 8 kicker = better two pair), 88 (set), 55 (set), 22 (set), 85s (two-pair 8+5).
- BTN's raise range is essentially the set + better two-pair combos; hero's A5 is a "first-to-fold" two-pair.

**Architect's GTO reasoning:**
Two-pair-bottom-kicker on a turn where 3 villains have shown aggression (bet + call + raise) in a 5-way pot: this is a textbook fold. Bet-call-raise sequence in multiway = the strongest possible range chain. Hero's A5 loses to virtually every combo in BTN's raise range. Even the 30.5% pot odds aren't met — hero has ~15-20% equity vs the raise range. FOLD is clear.

Hero may have an argument for CALL (hoping for boat-up on river if A or 5 hits, ~12% equity to improve), but the reverse-implied-odds (board pairing 8 = AA-better full house; board pairing 2 = 22-set-shoves; river-flush completes if 4th diamond) make CALL -EV.

**Confidence: HIGH** — FOLD is the GTO play vs the bet-call-raise chain.

**Axis tags:**
- street: turn
- position: BB
- action_context: facing-raise (bet + call + raise chain)
- hand_strength: weak-made (two-pair-bottom-kicker)
- board_texture: two_tone (Ad/5d on board + flush-completing potential)
- villain_chain_type: multi-villain-action-chain (bet + call + raise across 3 villains)
- hero_role: bet-and-call-faced (and now bet-and-call-and-raise-faced)
- multiway_dimension: range-chain-narrowing / pot-cascade

---

## 4. Architect's overall confidence

| Hand | Confidence | Reason |
|------|------------|--------|
| MW-51 | MEDIUM | Close CALL vs FOLD on TPweakkicker IP closing; solver to verify |
| MW-52 | HIGH | KK 4-bet vs squeeze is canonical |
| MW-53 | HIGH | A5s SB squeeze vs multi-flat is canonical solver line |
| MW-54 | MEDIUM | Check-raise vs call mix on combo-draw — solver verifies the mix |
| MW-55 | MEDIUM-HIGH | Top-two-pair value-raise; flat is acceptable mix; solver to verify |
| MW-56 | HIGH | BB closing with suited Ace at 11.5% pot odds is clear CALL |
| MW-57 | MEDIUM-HIGH | TT overpair on paired board checked-through; check is dominant |
| MW-58 | MEDIUM | Bottom set facing multi-villain raise chain — CALL vs 3-BET mix |
| MW-59 | HIGH | TT on monotone river vs polarized overbet → unambiguous FOLD |
| MW-60 | HIGH | Two-pair bottom kicker vs bet-call-raise turn chain → unambiguous FOLD |

**Summary**: 5 HIGH confidence (MW-52, MW-53, MW-56, MW-59, MW-60), 2 MEDIUM-HIGH (MW-55, MW-57), 3 MEDIUM (MW-51, MW-54, MW-58).

## 5. Hands flagged for owner-arbitration likelihood

The 3 MEDIUM hands (MW-51, MW-54, MW-58) are where architect's GTO reasoning is most likely to disagree with solver:

- **MW-51**: CALL vs FOLD on K9o IP closing facing 25% bet in 5-way. Solver may prefer FOLD if range-narrowing on CO's value-tilted c-bet is stronger than architect estimates.
- **MW-54**: Nut FD + gutshot + 2 overcards, SB OOP, bet-and-call faced. CALL vs CHECK-RAISE mix. Solver may prefer pure CALL given OOP + 2 villains un-acted.
- **MW-58**: Bottom set on coordinated 5-way board facing multi-villain raise chain. CALL vs 3-BET mix; architect leans CALL but raise frequency may be higher in solver.

For each, owner arbitration may be needed if solver result conflicts with architect's lean. Verification rubric (separate deliverable) defines the arbitration protocol.

## 6. Items needing orchestrator/owner attention

1. **Coverage gaps acknowledged**: No `opener` hero-role context (5-way decisions are mostly post-open); no HJ position (collapses to MP in 6-max). Accept or expand to 12 hands? Architect recommends **accept** — task asked for 10 hands and these gaps are structural, not omissions.

2. **River 5-way scarcity**: Only MW-59 is a pure river 5-way (MW-60 was redesigned to turn). 5-way pots rarely persist to river due to folding cascade. Acceptable for 10-hand pilot; full eval set may need 1-2 more river spots via passive lines.

3. **MW-60 redesign**: Originally intended as river spot; redesigned to turn to preserve `num_opps = 4`. Owner+solver should verify the turn decision is meaningful (architect confirms it is — bet-call-raise chain is canonical 5-way stress test).

4. **Squeeze pot complexity**: MW-52 has hero as **squeezer-faced** in 5-way (KK vs BTN squeeze with 2 cold-callers); MW-53 has hero as **squeezer** (A5s SB squeezing vs 3 in). Both are squeeze-pot family but different roles. This is intentional coverage of both sides of the squeeze geometry.

5. **5-way "labelling" path**: This memo does NOT assign labels. Verification rubric (separate deliverable) defines: (a) solver run setup per hand, (b) expected range, (c) arbitration if solver disagrees with architect. Owner+solver verification produces the FINAL labels that go into the production eval set JSONL.

## 7. Acceptance checklist (for owner + solver verification)

For each MW-51 through MW-60:

- [ ] Cards / board legal (no duplicate cards, valid suits)
- [ ] Action sequence legal (positions act in correct order; no impossible actions)
- [ ] `num_opponents_at_decision` correctly counted at the decision point
- [ ] Pot / stack / to_call arithmetic verified
- [ ] Sizing follows solver-aligned grid (flop 25/66, turn 33/75, river 33/75/150)
- [ ] Architect's suggested action runs through solver
- [ ] Solver outputs frequency for each action; verify architect's suggestion is the top or near-top frequency action
- [ ] If solver disagrees, owner arbitrates (per verification rubric)
- [ ] Final label committed to JSONL with full rationale

## 8. References

- `docs/MASTER_PLAN (1).md` §2 (partition definition + gate spec)
- `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` (existing format)
- `design/multiway_reference_set/BATCH1_RANGE_ANALYSIS.md` (range-narrowing analysis pattern)
- `data/4way_reference_35hand_2026-05-11.jsonl` (JSONL schema)
- `review/comms/4WAY_REFERENCE_PILOT_RATIONALE_2026-05-11.md` (per-hand rationale format)
- `review/comms/4WAY_REFERENCE_FULL_RATIONALE_2026-05-11.md` (full 35-hand rationale)
- Memory: `feedback_solver_vs_expert_labels.md`, `feedback_solver_aligned_sizing.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_findings.md`, `feedback_solver_verification_queue.md`

---

**STATUS**: DRAFT — DESIGN ONLY. No labels assigned. Solver + owner verification follows via separate rubric.
