# Batch 2-8 Range Analysis: GTO Actions and Reasoning

**Date:** 2026-04-05
**Author:** GTO Expert
**Pipeline:** Post-Fix (opener-aware ranges, bettor-aware narrowing)

---

## GTO Action Table

| Ref ID | Axis | Equity | Pot Odds | GTO Action | Confidence |
|--------|------|--------|----------|------------|------------|
| MW-11 | bluff_compress | 0.085 | 0.000 | CHECK | HIGH |
| MW-12 | bluff_compress | 0.126 | 0.000 | CHECK | HIGH |
| MW-13 | bluff_compress | 0.124 | 0.000 | CHECK | HIGH |
| MW-14 | bluff_compress | 0.524 | 0.268 | CALL | HIGH |
| MW-15 | bluff_compress | 0.000 | 0.000 | CHECK | HIGH |
| MW-16 | bluff_compress | 0.089 | 0.000 | CHECK | HIGH |
| MW-17 | nut_potential | 0.251 | 0.268 | CALL | HIGH |
| MW-18 | nut_potential | 0.465 | 0.268 | CALL | MEDIUM |
| MW-19 | nut_potential | 0.803 | 0.000 | BET | HIGH |
| MW-20 | nut_potential | 0.589 | 0.267 | CALL | MEDIUM |
| MW-21 | nut_potential | 0.356 | 0.216 | CALL | HIGH |
| MW-22 | nut_potential | 0.121 | 0.000 | CHECK | MEDIUM |
| MW-23 | position_ampli | 0.458 | 0.000 | BET | HIGH |
| MW-24 | position_ampli | 0.604 | 0.000 | BET | MEDIUM |
| MW-25 | position_ampli | 0.337 | 0.000 | BET | HIGH |
| MW-26 | position_ampli | 0.368 | 0.000 | CHECK | HIGH |
| MW-27 | position_ampli | 0.476 | 0.000 | BET | HIGH |
| MW-28 | position_ampli | 0.561 | 0.000 | BET | MEDIUM |
| MW-29 | aggression_res | 0.254 | 0.226 | CALL | MEDIUM |
| MW-30 | aggression_res | 0.399 | 0.184 | CALL | HIGH |
| MW-31 | aggression_res | 0.653 | 0.222 | FOLD | HIGH |
| MW-32 | aggression_res | 0.538 | 0.333 | CALL | MEDIUM |
| MW-33 | aggression_res | 0.885 | 0.167 | RAISE | HIGH |
| MW-34 | aggression_res | 0.666 | 0.000 | BET | HIGH |
| MW-35 | spr_interactio | 0.474 | 0.250 | CALL | HIGH |
| MW-36 | spr_interactio | 0.454 | 0.268 | CALL | HIGH |
| MW-37 | spr_interactio | 0.472 | 0.250 | CALL | HIGH |
| MW-38 | spr_interactio | 0.422 | 0.333 | CALL | HIGH |
| MW-39 | spr_interactio | 0.439 | 0.268 | CALL | HIGH |
| MW-40 | spr_interactio | 0.206 | 0.000 | BET | MEDIUM |
| MW-41 | range_narrowin | 0.253 | 0.231 | CALL | MEDIUM |
| MW-42 | range_narrowin | 0.816 | 0.000 | BET | HIGH |
| MW-43 | range_narrowin | 0.087 | 0.400 | FOLD | HIGH |
| MW-44 | range_narrowin | 0.394 | 0.280 | CALL | MEDIUM |
| MW-45 | range_narrowin | 0.478 | 0.385 | RAISE | HIGH |
| MW-46 | range_narrowin | 0.908 | 0.286 | FOLD | HIGH |
| MW-47 | combined_nut_p | 0.445 | 0.167 | CALL | MEDIUM |
| MW-48 | combined_bluff | 0.220 | 0.000 | CHECK | HIGH |
| MW-49 | combined_posit | 0.540 | 0.000 | BET | HIGH |
| MW-50 | combined_aggre | 0.329 | 0.290 | FOLD | HIGH |

---

## Detailed GTO Analysis

## Axis 2 — Bluff Compression

### MW-11: 5h4h OOP air, checked to hero 4-way, Q72r flop

**Action history:** CO opens, BTN calls, SB calls, BB (hero) calls. Flop Q72r checks to hero.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.0845 |
| equity_margin | +0.0845 |
| better_hand_pct | 0.9967 |
| worse_hand_pct | 0.0000 |
| hand_category | high_card |
| num_opponents | 3 |

**GTO Action: CHECK** — Confidence: HIGH

**Reasoning:** Hero has 5h4h on Q72r in a 4-way pot with no pair, no draw, and no equity. With 3 opponents, any bluff requires folding all three players — fold equity is multiplicative and approaches zero in a 4-way pot. Checking and giving up is mandatory.

---

### MW-12: JsTs IP overcards, checked to BTN hero 3-way, 852r

**Action history:** CO opens, BTN (hero) calls, BB calls. Flop 852r checks around to hero.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.1255 |
| equity_margin | +0.1255 |
| better_hand_pct | 0.9264 |
| worse_hand_pct | 0.0569 |
| hand_category | overcards |
| num_opponents | 2 |

**GTO Action: CHECK** — Confidence: HIGH

**Reasoning:** JsTs on 852r with two overcards has backdoor equity but no immediate equity against two opponents. Bluffing 3-way requires folding two players; even IP, the multiplicative fold equity reduction makes a pure air bluff unprofitable. Checking is correct to preserve the option to realize equity on later streets.

---

### MW-13: KhJh OOP overcards, SB checks into 3-way, A93r

**Action history:** BTN opens, SB (hero) calls, BB calls. Flop A93r: hero first to act OOP.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.1242 |
| equity_margin | +0.1242 |
| better_hand_pct | 0.6442 |
| worse_hand_pct | 0.3282 |
| hand_category | high_card |
| num_opponents | 2 |

**GTO Action: CHECK** — Confidence: HIGH

**Reasoning:** KhJh on A93r OOP with 2 opponents has no pair and very low equity. The ace on board heavily connects with both an opener range (AK, AQ, AJ) and callers' ranges. Leading as a bluff OOP into two opponents on an ace-high board compounds both the OOP disadvantage and bluff compression — check is clear.

---

### MW-14: Td9d flush+gutshot OOP, facing CO bet 33 into 90 3-way, Jd8d3h

**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Jd8d3h: CO bets 33 into 90.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.5242 |
| equity_margin | +0.2560 |
| better_hand_pct | 0.9594 |
| worse_hand_pct | 0.0232 |
| hand_category | high_card |
| num_opponents | 2 |
| pot_odds | 0.2683 |
| pot_odds_needed | 0.2683 |

**GTO Action: CALL** — Confidence: HIGH

**Reasoning:** Td9d on Jd8d3h is a flush draw (9 outs) plus a gutshot (4 outs to a queen) — approximately 13 clean outs giving roughly 46% equity. Facing a 33-into-90 bet, pot odds require ~27% equity. Although raising would compress fold equity in a 3-way pot, calling is clearly correct given overwhelming equity versus the pot odds. The semi-bluff raise is suboptimal MW — just call and realize the draw.

---

### MW-15: 9s8s missed OESD on river, IP vs 2 opponents, QJ52r-6

**Action history:** CO opens, BTN (hero) calls, BB calls. Flop/turn check through. River 6c: BB checks, hero faces decision.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.0000 |
| equity_margin | +0.0000 |
| better_hand_pct | 0.9548 |
| worse_hand_pct | 0.0271 |
| hand_category | high_card |
| num_opponents | 2 |

**GTO Action: CHECK** — Confidence: HIGH

**Reasoning:** 9s8s missed the OESD completely (board QJ52-6 with no spades). Hero has nine-high with no pair and no remaining outs on the river. Bluffing IP on the river into 2 opponents who have called through two streets essentially requires two folds — multiplicative fold equity collapse. Check and fold if bet into.

---

### MW-16: JsTs IP overcards, BTN hero 4-way (vs MW-12 2-way), 852r

**Action history:** HJ opens, CO calls, BTN (hero) calls, BB calls. Flop 852r checks to hero. Compare to MW-12 (3-way same hand).

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.0895 |
| equity_margin | +0.0895 |
| better_hand_pct | 0.9678 |
| worse_hand_pct | 0.0129 |
| hand_category | overcards |
| num_opponents | 3 |

**GTO Action: CHECK** — Confidence: HIGH

**Reasoning:** Same hand and board as MW-12 (JsTs on 852r) but now 4-way with three opponents. Bluff fold equity goes from needing 2 folds (MW-12) to needing 3 folds. Even though hero is IP with some backdoor equity, the bluff is even more firmly unprofitable than the 3-way version. The contrast between MW-12 and MW-16 directly demonstrates bluff compression scaling.

---

## Axis 3 — Nut Potential

### MW-17: AdKs nut flush draw + overcards, facing CO bet 3-way, Jd8d4c

**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Jd8d4c: CO bets 33 into 90.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.2507 |
| equity_margin | -0.0175 |
| better_hand_pct | 0.5133 |
| worse_hand_pct | 0.4269 |
| hand_category | overcards |
| num_opponents | 2 |
| pot_odds | 0.2683 |
| pot_odds_needed | 0.2683 |

**GTO Action: CALL** — Confidence: HIGH

**Reasoning:** AdKs on Jd8d4c has the nut flush draw (9 outs) plus two overcards (6 outs to TPTK/TPGK) — approximately 15 outs giving roughly 54% equity. Pot odds require only 27% to call. The nut draw is especially valuable MW because if the flush hits, no opponent can beat it with a flush. Calling comfortably; raising as a semi-bluff is also viable.

---

### MW-18: 9d7d non-nut flush draw, same board Jd8d4c vs MW-17, 3-way

**Action history:** CO opens, BTN calls, BB (hero) calls. Flop Jd8d4c: CO bets 33 into 90. Compare to MW-17 (nut draw).

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.4645 |
| equity_margin | +0.1962 |
| better_hand_pct | 0.9801 |
| worse_hand_pct | 0.0199 |
| hand_category | high_card |
| num_opponents | 2 |
| pot_odds | 0.2683 |
| pot_odds_needed | 0.2683 |

**GTO Action: CALL** — Confidence: MEDIUM

**Reasoning:** 9d7d on Jd8d4c has a non-nut flush draw (9 outs) plus a weak gutshot (4 outs to T makes straight). Equity is sufficient to call the 33-into-90 bet. However, unlike the nut draw (MW-17), completing the flush may not win the pot if an opponent holds Adxx. MW, the non-nut draw's equity is discounted by the reverse implied odds of hitting and losing — call is correct but caution on raises warranted.

---

### MW-19: TcNc nut straight on QJ8, IP hero vs 2 opponents, checked to BTN

**Action history:** CO opens, BTN (hero) calls, BB calls. Flop QhJs8d: checks to hero.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.8035 |
| equity_margin | +0.8035 |
| better_hand_pct | 0.0000 |
| worse_hand_pct | 0.9815 |
| hand_category | straight |
| num_opponents | 2 |

**GTO Action: BET** — Confidence: HIGH

**Reasoning:** Tc9c on QhJs8d makes the nut straight (Q-J-T-9-8). Hero has the best possible hand on this board. In a 3-way pot with no better hand possible, hero should bet for value immediately — the nut hand multiway benefits from building the pot while no opponent can currently beat it. Slow-playing risks giving free cards to flush draws or pairs that might two-pair the board.

---

### MW-20: TsNs non-nut straight KQJ, IP hero facing BB lead 4-way

**Action history:** HJ opens, CO calls, BTN (hero) calls, BB calls. Flop KQJr: BB leads 40 into 110.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.5890 |
| equity_margin | +0.3223 |
| better_hand_pct | 0.0278 |
| worse_hand_pct | 0.9537 |
| hand_category | straight |
| num_opponents | 3 |
| pot_odds | 0.2667 |
| pot_odds_needed | 0.2667 |

**GTO Action: CALL** — Confidence: MEDIUM

**Reasoning:** Ts9s on KdQcJh makes the second-nut straight (K-Q-J-T-9). However, any AT makes the nut straight. In a 4-way pot with a BB lead of 40 into 110, pot odds require 26% equity. The second-nut straight has very strong equity but is vulnerable to AT which is common in preflop ranges. Calling is appropriate — raising risks stacking off against AT which is very likely in the BB's leading range.

---

### MW-21: Ah9h nut flush draw + gutshot, facing CO bet 4-way, JhTh2c

**Action history:** CO opens, BTN calls, SB calls, BB (hero) calls. Flop JhTh2c: CO bets 33 into 120.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.3558 |
| equity_margin | +0.1401 |
| better_hand_pct | 0.7135 |
| worse_hand_pct | 0.2671 |
| hand_category | one_overcard |
| num_opponents | 3 |
| pot_odds | 0.2157 |
| pot_odds_needed | 0.2157 |

**GTO Action: CALL** — Confidence: HIGH

**Reasoning:** Ah9h on JhTh2c is a nut flush draw (9 outs) plus a backdoor straight draw. With approximately 40-45% equity versus a 4-way pot, calling the 33-into-120 bet (pot odds ~22%) is mandatory. The nut flush draw in a 4-way pot has huge implied odds — if the flush hits, at least one opponent with a smaller flush draw or Jx hand will pay off significantly.

---

### MW-22: AdQs nut flush draw OOP, checked to hero 4-way, Kd9d4h

**Action history:** CO opens, BTN calls, SB calls, BB (hero) calls. Flop Kd9d4h: hero first to act OOP 4-way.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.1215 |
| equity_margin | +0.1215 |
| better_hand_pct | 0.5771 |
| worse_hand_pct | 0.3755 |
| hand_category | one_overcard |
| num_opponents | 3 |

**GTO Action: CHECK** — Confidence: MEDIUM

**Reasoning:** AdQs on Kd9d4h has the nut flush draw but no pair. OOP in a 4-way pot with no bet to respond to, donk-leading is generally a leak — the bettor's range advantage goes to the preflop opener (CO). Checking is preferred to allow the preflop aggressor to c-bet, then hero can check-raise the nut draw or call depending on the sizing. Checking also avoids turning a drawing hand into a naked bluff OOP.

---

## Axis 4 — Position Amplification

### MW-23: QhJc top pair IP BTN, 3-way checked to hero, Q83r

**Action history:** CO opens, BTN (hero) calls, BB calls. Flop Q83r: BB checks, CO checks, hero acts last.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.4575 |
| equity_margin | +0.4575 |
| better_hand_pct | 0.1799 |
| worse_hand_pct | 0.8083 |
| hand_category | top_pair |
| num_opponents | 2 |

**GTO Action: BET** — Confidence: HIGH

**Reasoning:** QhJc on Q83r gives top pair J kicker in position. Two opponents checked before hero, capping their ranges significantly. IP with top pair on a dry board, hero should bet for value and to deny equity to any draws or overcards. Position allows hero to set the price and control pot size — the canonical advantage of IP play in multiway pots.

---

### MW-24: QsJd top pair OOP SB, 3-way hero first to act, Q83r (mirror of MW-23)

**Action history:** BTN opens, SB (hero) calls, BB calls. Flop Q83r: hero first to act OOP.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.6042 |
| equity_margin | +0.6042 |
| better_hand_pct | 0.1004 |
| worse_hand_pct | 0.8824 |
| hand_category | top_pair |
| num_opponents | 2 |

**GTO Action: BET** — Confidence: MEDIUM

**Reasoning:** QsJd on Q83r gives top pair J kicker OOP in a 3-way pot. Unlike MW-23 (IP), hero must act without knowing what the two IP players will do. Betting is still correct — QJ is strong enough to bet for value even OOP — but the sizing should be smaller (~33% pot rather than 50%) to limit pot exposure before seeing how the IP players respond. OOP position reduces confidence level.

---

### MW-25: Ks7s flush draw IP BTN, 4-way checked to hero, As9s5d

**Action history:** HJ opens, CO calls, BTN (hero) calls, BB calls. Flop As9s5d: all check to hero.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.3372 |
| equity_margin | +0.3372 |
| better_hand_pct | 0.9125 |
| worse_hand_pct | 0.0875 |
| hand_category | high_card |
| num_opponents | 3 |

**GTO Action: BET** — Confidence: HIGH

**Reasoning:** Ks7s on As9s5d is a strong flush draw with three opponents who all checked. IP with a flush draw, hero can bet after seeing three checks — all opponents showed weakness. Betting serves double duty: deny free cards and potentially take the pot now. IP position allows hero to see all checks before committing chips — position amplified in 4-way pot.

---

### MW-26: Ks7s flush draw OOP SB, 4-way hero first to act, As9s5d (mirror of MW-25)

**Action history:** CO opens, BTN calls, SB (hero) calls, BB calls. Flop As9s5d: hero first to act OOP.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.3680 |
| equity_margin | +0.3680 |
| better_hand_pct | 0.8081 |
| worse_hand_pct | 0.1919 |
| hand_category | high_card |
| num_opponents | 3 |

**GTO Action: CHECK** — Confidence: HIGH

**Reasoning:** Ks7s on As9s5d OOP in a 4-way pot as first to act. Same hand as MW-25 but now OOP. Hero cannot see what opponents will do before acting. Donk-leading a flush draw OOP into three opponents is generally wrong — the preflop opener (CO) has range advantage on this ace-high board. Check and allow the IP players to act first; hero can check-call or check-raise if CO bets.

---

### MW-27: JhJc overpair IP BTN, 3-way checked to hero, 962r

**Action history:** CO opens, BTN (hero) calls, BB calls. Flop 962r: BB checks, CO checks, hero acts.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.4765 |
| equity_margin | +0.4765 |
| better_hand_pct | 0.1321 |
| worse_hand_pct | 0.8622 |
| hand_category | overpair |
| num_opponents | 2 |

**GTO Action: BET** — Confidence: HIGH

**Reasoning:** JhJc overpair on 962r in position. Two opponents checked before hero on a low, dry board. Overpair is dominant on this board — the only concerns are sets (99, 66, 22) which are very low frequency. IP with a strong made hand on a dry board after two checks, hero should bet for value. Position confirmation (seeing two checks) makes this a confident bet.

---

### MW-28: JhJd overpair OOP SB, 3-way hero first to act, 962r (mirror of MW-27)

**Action history:** BTN opens, SB (hero) calls, BB calls. Flop 962r: hero first to act OOP.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.5610 |
| equity_margin | +0.5610 |
| better_hand_pct | 0.0764 |
| worse_hand_pct | 0.9208 |
| hand_category | overpair |
| num_opponents | 2 |

**GTO Action: BET** — Confidence: MEDIUM

**Reasoning:** JhJd overpair on 962r OOP in a 3-way pot as first to act. Same hand as MW-27 but OOP. Overpair is still strong enough to bet OOP — the board is dry and hero's range advantage is clear. However, OOP position means hero cannot see IP responses before betting, and check-raise opportunities exist that are unavailable IP. Betting with a smaller sizing (~33% pot) is correct but confidence is reduced versus the IP version (MW-27).

---

## Axis 5 — Aggression Respect

### MW-29: KcTh top pair facing single CO bet 4-way, KJ6r

**Action history:** CO opens, BTN calls, SB calls, BB (hero) calls. Flop KJ6r: CO bets 35 into 120.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.2535 |
| equity_margin | +0.0277 |
| better_hand_pct | 0.2127 |
| worse_hand_pct | 0.7802 |
| hand_category | top_pair |
| num_opponents | 3 |
| pot_odds | 0.2258 |
| pot_odds_needed | 0.2258 |

**GTO Action: CALL** — Confidence: MEDIUM

**Reasoning:** KcTh on KJ6r gives top pair T kicker facing a single CO bet in a 4-way pot. Pot odds require ~22% equity (35 into 155). Top pair T kicker has adequate equity to call against CO's opening range narrowed to betting combos. However, 3 opponents means the field has many Kx combos that dominate KT — calling is correct but this is not a comfortable call.

---

### MW-30: KcTh top pair facing bet-and-call MW (same hand MW-29), KJ6r

**Action history:** CO opens, BTN calls, SB calls, BB (hero) calls. Flop KJ6r: CO bets 35, BTN calls, SB folds. Hero faces bet + call.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.3990 |
| equity_margin | +0.2148 |
| better_hand_pct | 0.2136 |
| worse_hand_pct | 0.7798 |
| hand_category | top_pair |
| num_opponents | 2 |
| pot_odds | 0.1842 |
| pot_odds_needed | 0.1842 |

**GTO Action: CALL** — Confidence: HIGH (solver-corrected 9 Apr 2026)

**Reasoning (corrected):** KcTh on KJ6r facing CO bet + BTN call. Equity 40% vs pot odds 18% = 22pp surplus. Solver (GTO Wizard) shows pure CALL for all KT combos. The original FOLD was based on "bet+call narrows ranges" but the 22pp equity surplus overwhelms the range-narrowing signal. Per KB v1.2 Example 3: fold only when equity is near/below pot odds AND hero's specific holding is dominated. Here, hero has top pair with 22pp surplus — CALL.

**Original reasoning (superseded):** Same KcTh on KJ6r, but now facing CO bet + BTN call. The call signal from BTN dramatically narrows the effective field range — BTN called a bet into a 4-way pot, meaning BTN has a Kx+ hand or a strong draw. KT is now almost certainly dominated by KJ, KQ, AK on one side and sets on the other. With both opponents representing strength, folding is correct despite the mathematically acceptable pot odds. Multiway bet-and-call is a condensed range signal.

---

### MW-31: AsJs TPJK facing check-raise from CO in 3-way, AQ5r

**Action history:** CO opens, BTN (hero) calls, BB calls. Flop AQ5r: BB checks, hero bets 30, CO raises to 90. BB folds.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.6533 |
| equity_margin | +0.4311 |
| better_hand_pct | 0.2301 |
| worse_hand_pct | 0.7298 |
| hand_category | top_pair |
| num_opponents | 1 |
| pot_odds | 0.2222 |
| pot_odds_needed | 0.2222 |

**GTO Action: FOLD** — Confidence: HIGH

**Reasoning:** AsJs on AQ5r facing a check-raise from CO after hero bet in a 3-way pot. Check-raises into a multiway pot represent the tightest possible range — CO checked (slightly capping range), hero bet, BB folded, CO raised. CO's check-raise range is essentially AQ two-pair, AK, AA, QQ sets, 55 sets. Top pair J kicker is dominated by almost this entire range. The pot odds (60 into 210, need 22%) are insufficient against CO's credible check-raise.

---

### MW-32: JsTs top pair facing double barrel turn, T843 (MW context: started 3-way)

**Action history:** CO opens, BTN (hero) calls, BB calls. Flop T84r: BB folds. Turn 3s: CO fires again, 45 into 90.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.5381 |
| equity_margin | +0.2048 |
| better_hand_pct | 0.4197 |
| worse_hand_pct | 0.5622 |
| hand_category | top_pair |
| num_opponents | 1 |
| pot_odds | 0.3333 |
| pot_odds_needed | 0.3333 |

**GTO Action: CALL** — Confidence: MEDIUM

**Reasoning:** JsTs on Tc8h4d3s is top pair J kicker facing a double barrel. The pot started 3-way but BB folded on flop, so this is now heads-up. CO double-barreling narrows range to strong Tx (QT, KT, AT), overpairs, sets, and two-pair. JT is near the top of the calling range — it beats two-pair combos but loses to sets and better Tx. Call is correct but marginal; the double barrel in a pot that started multiway is a credible range.

---

### MW-33: 8h8s set facing bet-and-call MW, hero should raise, 873r

**Action history:** CO opens, BTN calls, SB calls, BB (hero) calls. Flop 873r: CO bets 40, BTN calls, SB folds. Hero facing bet + call with set.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.8850 |
| equity_margin | +0.7183 |
| better_hand_pct | 0.0000 |
| worse_hand_pct | 1.0000 |
| hand_category | set |
| num_opponents | 2 |
| pot_odds | 0.1667 |
| pot_odds_needed | 0.1667 |

**GTO Action: RAISE** — Confidence: HIGH

**Reasoning:** 8h8s on 873r gives hero a set of eights — the best possible hand on this board. Facing a CO bet + BTN call in a 4-way pot, hero should raise to build the pot and protect against straight draws (6x, 5x hands need only two outs). With a set facing bet-and-call MW, raising is correct despite the narrowed range of opponents — hero is crushing them regardless and must extract maximum value while denying straight draws.

---

### MW-34: AcAd overpair CO hero c-bets into 3-way checked board, J94r

**Action history:** CO (hero) opens, BTN calls, BB calls. Flop J94r: BB checks, BTN checks. Hero acts.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.6657 |
| equity_margin | +0.6657 |
| better_hand_pct | 0.0545 |
| worse_hand_pct | 0.9388 |
| hand_category | overpair |
| num_opponents | 2 |

**GTO Action: BET** — Confidence: HIGH

**Reasoning:** AcAd on J94r — hero opened preflop and is now the aggressor with an overpair on a middling board. Two opponents checked to hero. CO c-betting an overpair after two checks is standard — the checking range of two opponents is capped relative to an opening range. However, 3-way, hero should bet at a reduced frequency (~50-60%) and smaller sizing to account for the wider combined defense range. Betting is still correct with an overpair.

---

## Axis 6 — SPR Interaction

### MW-35: QcJd top pair, SPR ~3 committed, facing CO bet 3-way, Q72r

**Action history:** CO opens 2.5, BTN (hero) calls, BB calls. Flop Q72r (SPR ~3): BB checks, CO bets 9 into 27.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.4740 |
| equity_margin | +0.2240 |
| better_hand_pct | 0.1802 |
| worse_hand_pct | 0.8139 |
| hand_category | top_pair |
| num_opponents | 2 |
| pot_odds | 0.2500 |
| pot_odds_needed | 0.2500 |

**GTO Action: CALL** — Confidence: HIGH

**Reasoning:** QcJd on Q72r at SPR ~3 facing a bet of 9 into 27 (pot odds 25%). At SPR ~3, top pair J kicker is committed — there is not enough money behind to fold to further action without being pot-committed anyway. Calling now and getting it in on the turn is the plan. The low SPR simplifies the decision: top pair at SPR 3 in a 3-way pot = call, stack off.

---

### MW-36: QcJd top pair, SPR ~8 standard, facing CO bet 3-way, Q72r (same as MW-35)

**Action history:** CO opens, BTN (hero) calls, BB calls. Flop Q72r (SPR ~8): BB checks, CO bets 33 into 90.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.4542 |
| equity_margin | +0.1860 |
| better_hand_pct | 0.1802 |
| worse_hand_pct | 0.8139 |
| hand_category | top_pair |
| num_opponents | 2 |
| pot_odds | 0.2683 |
| pot_odds_needed | 0.2683 |

**GTO Action: CALL** — Confidence: HIGH

**Reasoning:** QcJd on Q72r at SPR ~8 facing 33 into 90 (pot odds 27%). At standard SPR, top pair J kicker is a comfortable call against a single CO bet in a 3-way pot. There is enough money behind to see turn and river development. Pot odds are met and equity margin is positive. Raising is not standard here — we're in between committed and deep.

---

### MW-37: QcJd top pair, SPR ~15 deep, facing CO bet 3-way, Q72r (same as MW-35/36)

**Action history:** CO opens deep stack 200bb, BTN (hero) calls, BB calls. Flop Q72r (SPR ~15): BB checks, CO bets 15 into 45.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.4723 |
| equity_margin | +0.2223 |
| better_hand_pct | 0.1802 |
| worse_hand_pct | 0.8139 |
| hand_category | top_pair |
| num_opponents | 2 |
| pot_odds | 0.2500 |
| pot_odds_needed | 0.2500 |

**GTO Action: CALL** — Confidence: HIGH

**Reasoning:** QcJd on Q72r at SPR ~15 facing 15 into 45 (pot odds 25%). At deep SPR, top pair J kicker is a call but hero should be more cautious about inflating the pot. The deep stacks mean implied odds work both ways — hero has more to lose if the turn brings a check-raise. Call is correct, but hero should reassess carefully on each street rather than auto-stacking off as at low SPR. The coaching difference from MW-35/36 is the caution level, not the action.

---

### MW-38: AhJh nut flush draw, low SPR ~3 facing BB lead 3-way, Kh8h3d

**Action history:** CO opens, BTN (hero) calls, BB calls. Flop Kh8h3d (SPR ~3): BB leads 15 into 30.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.4225 |
| equity_margin | +0.0892 |
| better_hand_pct | 0.7993 |
| worse_hand_pct | 0.1506 |
| hand_category | one_overcard |
| num_opponents | 2 |
| pot_odds | 0.3333 |
| pot_odds_needed | 0.3333 |

**GTO Action: CALL** — Confidence: HIGH

**Reasoning:** AhJh on Kh8h3d has the nut flush draw at low SPR ~3, facing a 15-into-30 lead from BB in a 3-way pot. Pot odds require 33% equity; the nut flush draw has approximately 35% equity to improve. At low SPR, calling here is essentially getting committed — hero will be in for most of the stack. Calling (or even raising all-in) with a nut draw at SPR 3 is correct. The low SPR amplifies the draw's power by removing implied-odds uncertainty.

---

### MW-39: AhJh nut flush draw, high SPR ~15 facing CO bet 3-way, Kh8h3d (vs MW-38)

**Action history:** CO opens, BTN (hero) calls, BB calls deep. Flop Kh8h3d (SPR ~15): CO bets 33 into 90.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.4392 |
| equity_margin | +0.1710 |
| better_hand_pct | 0.6226 |
| worse_hand_pct | 0.3208 |
| hand_category | one_overcard |
| num_opponents | 2 |
| pot_odds | 0.2683 |
| pot_odds_needed | 0.2683 |

**GTO Action: CALL** — Confidence: HIGH

**Reasoning:** Same AhJh nut flush draw on Kh8h3d at high SPR ~15, facing CO bet of 33 into 90 (pot odds 27%). At deep SPR, the flush draw's implied odds are enormous — if the flush hits, hero can extract large bets on turn and river from opponents with weaker flushes, sets, or top pair. Calling is correct and the high SPR actually increases the value of the draw versus MW-38 because the remaining-stack reward is larger when the flush completes.

---

### MW-40: AhTs top pair T kicker, high SPR 4-way IP, checked to hero, AJ5r

**Action history:** HJ opens, CO calls, BTN (hero) calls, BB calls 200bb deep. Flop AJ5r: all check to hero.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.2062 |
| equity_margin | +0.2062 |
| better_hand_pct | 0.3120 |
| worse_hand_pct | 0.6764 |
| hand_category | top_pair |
| num_opponents | 3 |

**GTO Action: BET** — Confidence: MEDIUM

**Reasoning:** AhTs on AJ5r gives top pair T kicker in position after 4-way check-through at high SPR. Despite the deep stacks, top pair is strong enough to bet after three checks — the checks cap opponents' ranges. However, at high SPR 4-way, hero should bet small (25-30% pot) rather than a standard 50% sizing to avoid over-inflating the pot with a vulnerable hand. Medium confidence because the bet is thin but correct after complete check-through.

---

## Axis 7 — Range Narrowing

### MW-41: QhTc middle pair+gutshot facing CO turn barrel 3-way, KQ7-J

**Action history:** CO opens, BTN (hero) calls, BB calls. Flop KQ7r: CO bets, hero calls, BB calls. Turn J: CO fires 60 into 200.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.2530 |
| equity_margin | +0.0222 |
| better_hand_pct | 0.4414 |
| worse_hand_pct | 0.5518 |
| hand_category | middle_pair |
| num_opponents | 2 |
| pot_odds | 0.2308 |
| pot_odds_needed | 0.2308 |

**GTO Action: CALL** — Confidence: MEDIUM

**Reasoning:** QhTc on KQ7-J gives middle pair plus a gutshot to the broadway straight. CO's double-barrel narrows his range considerably from the initial opening range — turn barrels in 3-way pots represent strong made hands or strong draws (KJ, KT, AK, QQ). However, hero's gutshot to the broadway straight (any A makes the nuts) combined with middle pair provides enough equity to call. Range narrowing makes this call thinner than it looks.

---

### MW-42: AsJs TPTK on river, CO checks after 2-street action, AK752

**Action history:** CO opens, BTN (hero) calls, BB calls. Flop AK7: CO bets, hero calls, BB folds. Turn 5: CO checks, hero bets, CO calls. River 2: CO checks.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.8157 |
| equity_margin | +0.8157 |
| better_hand_pct | 0.1659 |
| worse_hand_pct | 0.7972 |
| hand_category | top_pair |
| num_opponents | 1 |

**GTO Action: BET** — Confidence: HIGH

**Reasoning:** AsJs on AK752 (rainbow) gives TPTK on a clean river. CO checked to hero after two streets of action. CO's check after a call-call line significantly caps CO's range — monsters would bet the river. TPTK is very strong on AK752 (only AK, A5, K7 two-pairs beat us, and full houses). Hero should bet the river for thin value, targeting CO's Ax/Kx hands that check-call. Range narrowing through streets allows confident river value bet.

---

### MW-43: 9s7s middle pair vs CO river bet after check-check line 4-way, 9852K

**Action history:** CO opens, BTN calls, SB calls, BB (hero) calls. Flop 985d: all check. Turn 2: all check. River K: CO bets 80 into 120 (late street bet after passive line).

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.0875 |
| equity_margin | -0.3125 |
| better_hand_pct | 0.4789 |
| worse_hand_pct | 0.5211 |
| hand_category | middle_pair |
| num_opponents | 3 |
| pot_odds | 0.4000 |
| pot_odds_needed | 0.4000 |

**GTO Action: FOLD** — Confidence: HIGH

**Reasoning:** 9s7s on 9852K with middle pair faces a CO river bet of 80 into 120 after a check-check-check passive line. The check-check-bet line from CO after passive play is an extremely credible range in multiway pots — CO either slowplayed a monster (set, two pair) or picked up a strong hand on the river (K-high two pair, etc). Middle pair on a paired board cannot call a large river bet after this line MW. Fold is mandatory.

---

### MW-44: Th8h top pair+OESD facing BB double-lead turn 3-way, T947

**Action history:** CO opens, BTN (hero) calls, BB calls. Flop T94r: BB donks 30, CO calls, hero calls. Turn 7: BB leads again 70 into 180.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.3937 |
| equity_margin | +0.1138 |
| better_hand_pct | 0.3968 |
| worse_hand_pct | 0.6028 |
| hand_category | top_pair |
| num_opponents | 2 |
| pot_odds | 0.2800 |
| pot_odds_needed | 0.2800 |

**GTO Action: CALL** — Confidence: MEDIUM

**Reasoning:** Th8h on T947 gives top pair with an OESD (6, J completes the straight). BB's double-lead narrows BB's range to strong Tx, sets (TT, 99), or straights (68, 56). Hero's equity from top pair + 8-out OESD is approximately 40-45% against this narrowed range. Pot odds for calling 70 into 250 require ~22% equity — call is correct. The 8-outer specifically targets BB's non-made-hand portion of the narrowed range.

---

### MW-45: 6d6c set (flopped), facing CO turn bet after checked flop, AK6-Q 4-way

**Action history:** CO opens, BTN calls, SB calls, BB (hero) calls. Flop AK6r: all check (hero slowplays set). Turn Q: CO fires 75 into 120.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.4785 |
| equity_margin | +0.0939 |
| better_hand_pct | 0.0896 |
| worse_hand_pct | 0.9104 |
| hand_category | set |
| num_opponents | 3 |
| pot_odds | 0.3846 |
| pot_odds_needed | 0.3846 |

**GTO Action: RAISE** — Confidence: HIGH

**Reasoning:** 6d6c flopped a set on AK6r and slowplayed through the flop. Now facing CO's turn bet on AKQ. Despite the scary turn card (Q fills AQ two-pair for CO), hero has a full house draw (6 makes a boat) and trips with bottom set. CO's range after passive flop is wide — some AK, some AQ, some sets. Hero's set of sixes is still very strong and should raise the turn to protect and extract value. The range-narrowing axis: CO's turn bet after passive flop suggests made hand value, but hero dominates.

---

### MW-46: Ks7c trips facing river check-raise after 2-street action, 775-9-J

**Action history:** HJ opens, CO calls, BTN (hero) calls, BB calls. Flop 775: CO bets, BTN calls, others fold. Turn 9: CO checks, hero bets, CO calls. River J: CO check-raises hero.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.9079 |
| equity_margin | +0.6222 |
| better_hand_pct | 0.0921 |
| worse_hand_pct | 0.9079 |
| hand_category | trips |
| num_opponents | 1 |
| pot_odds | 0.2857 |
| pot_odds_needed | 0.2857 |

**GTO Action: FOLD** — Confidence: HIGH

**Reasoning:** Ks7c on 775-9-J gives trips (three sevens) but faces a check-raise from CO on the river. CO's line: bet flop, call turn bet, check-raise river — this is one of the most credible lines in poker. After calling a turn bet and then check-raising the river in a multiway pot origin, CO's range is essentially quads (77 — but unlikely) or full houses (99, JJ, 55 made full, 97s, J7s). Trip sevens lose to all these hands. River check-raise after multi-street action = fold trips.

---

## Axis 8 — Combined (3+4+5)

### MW-47: AsQs nut FD+gutshot OOP SB, facing bet+call 4-way, KJ5ss (axes 3+4+5)

**Action history:** CO opens, BTN calls, SB (hero) calls, BB calls. Flop KJ5ss: BB checks, CO bets 40, BTN calls. Hero (SB) faces bet+call OOP.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.4450 |
| equity_margin | +0.2783 |
| better_hand_pct | 0.6179 |
| worse_hand_pct | 0.3240 |
| hand_category | one_overcard |
| num_opponents | 3 |
| pot_odds | 0.1667 |
| pot_odds_needed | 0.1667 |

**GTO Action: CALL** — Confidence: MEDIUM

**Reasoning:** AsQs on KJ5ss gives the nut flush draw plus a gutshot to the broadway straight — approximately 15 outs and very high equity (50-55%). Facing a CO bet of 40 + BTN call into a 4-way pot OOP: the nut draw power (axis 3) partially offsets the OOP disadvantage (axis 4) and the condensed field range signaled by bet+call (axis 5). Call is correct — equity is strong enough despite position. Raising as a semi-bluff OOP into bet+call is too aggressive; just call and realize equity.

---

## Axis 8 — Combined (2+6)

### MW-48: AhTc gutshot+overcards, low SPR ~2, OOP BB 3-way, QJ4r (axes 2+6)

**Action history:** BTN opens, SB calls, BB (hero) calls. Flop QJ4r (SPR ~2): hero first to act OOP. Bluffing compresses at low SPR.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.2195 |
| equity_margin | +0.2195 |
| better_hand_pct | 0.5329 |
| worse_hand_pct | 0.4395 |
| hand_category | one_overcard |
| num_opponents | 2 |

**GTO Action: CHECK** — Confidence: HIGH

**Reasoning:** AhTc on QJ4r at low SPR ~2 OOP in a 3-way pot. Hero has a gutshot (K makes broadway) and two overcards — approximately 10 outs but no made hand. At low SPR (axis 6), committing chips as a bluff is dangerous because pot odds become compressed — opponents are pot-committed to call any bet. Bluff compression (axis 2) is also severe: folding two opponents at low SPR almost never works. Check and fold to a bet, or check-call if the price is right for the gutshot.

---

## Axis 8 — Combined (4+7)

### MW-49: AdKd TPTK IP BTN betting turn after flop bet-call-call 3-way, A95-T (axes 4+7)

**Action history:** HJ opens, CO calls, BTN (hero) calls, BB calls. Flop A95r: hero bets 35, CO calls, BB calls, HJ folds. Turn T: CO/BB check, hero acts.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.5397 |
| equity_margin | +0.5397 |
| better_hand_pct | 0.1447 |
| worse_hand_pct | 0.7799 |
| hand_category | top_pair_good_kicker |
| num_opponents | 2 |

**GTO Action: BET** — Confidence: HIGH

**Reasoning:** AdKd on A95-T gives TPTK in position after hero bet the flop and two opponents called. The flop call-call from two opponents narrowed their ranges (axis 7): they both have Ax, draws, or strong pairs. The turn T is a card that helps some draws (OESD on 9-T-x) but not sets. IP on the turn (axis 4) after two checks, hero should bet for value — the narrowed field still contains many Ax hands that will call a turn bet. TPTK at the top of hero's range merits a 50-60% pot bet to build value and charge draws.

---

## Axis 8 — Combined (4+5+7)

### MW-50: JcTc top pair OOP facing BTN turn bet after flop raise, J845 (axes 4+5+7)

**Action history:** CO opens, BTN calls, SB calls, BB (hero) calls. Flop J84r: CO bets, BTN raises, SB folds, BB calls. Turn 5: CO calls. BTN bets 90 into 220.

**Pipeline features:**

| Feature | Value |
|---------|-------|
| raw_equity | 0.3292 |
| equity_margin | +0.0389 |
| better_hand_pct | 0.3365 |
| worse_hand_pct | 0.6494 |
| hand_category | top_pair |
| num_opponents | 2 |
| pot_odds | 0.2903 |
| pot_odds_needed | 0.2903 |

**GTO Action: FOLD** — Confidence: HIGH

**Reasoning:** JcTc on J845 gives top pair T kicker OOP facing BTN's turn bet of 90 into 220. BTN raised the flop and now fires the turn — two streets of aggression from a flop raiser represents a maximally condensed range: sets, two-pair, strong straights. Axis 7 (range narrowing): BTN's double-aggression line eliminates almost all bluffs. Axis 5 (aggression respect): MW context makes the flop raise even more credible. Axis 4 (position): hero is OOP with a capped range. JT top pair folds to two-street aggression from BTN.

---

## Axis Summaries

### Axis 5 — Aggression Respect

**Hands:** MW-29, MW-30, MW-31, MW-32, MW-33, MW-34
**Actions:** CALL, CALL, FOLD, CALL, RAISE, BET
**Average equity:** 0.5658

**Axis insight:** MW-31 identifies FOLD with a decent hand — check-raise in multiway pots is a condensed range signal. MW-30 (solver-corrected to CALL) shows the limit: when equity surplus is 22pp, the range signal is insufficient to override. MW-33 shows the other end: when hero has the nuts (set), facing aggression MW means RAISE. Aggression respect is about what opponents have, not reflexive folding.

### Axis 2 — Bluff Compression

**Hands:** MW-11, MW-12, MW-13, MW-14, MW-15, MW-16
**Actions:** CHECK, CHECK, CHECK, CALL, CHECK, CHECK
**Average equity:** 0.1580

**Axis insight:** All 6 bluff-compression hands correctly identify CHECK/FOLD as the action. The contrast between MW-12 (3-way) and MW-16 (4-way) with the same hand shows how fold equity degrades as opponents increase. MW-14 (semi-bluff with draw) correctly identifies CALL over RAISE — drawing hands call MW, they don't raise as semi-bluffs.

### Axis 8 — Combined (4+5+7)

**Hands:** MW-50
**Actions:** FOLD
**Average equity:** 0.3292

**Axis insight:** MW-50 shows how three axes combine to make a FOLD decisive: OOP position, narrowed range from flop raise, and two streets of aggression from BTN = top pair is crushed despite looking like a decent hand in isolation.

### Axis 8 — Combined (2+6)

**Hands:** MW-48
**Actions:** CHECK
**Average equity:** 0.2195

**Axis insight:** MW-48 shows how low SPR completely eliminates bluffing: even with some equity, bluff compression at low SPR makes any bet a commitment, not a bluff.

### Axis 8 — Combined (3+4+5)

**Hands:** MW-47
**Actions:** CALL
**Average equity:** 0.4450

**Axis insight:** MW-47 shows how nut draw equity overrides OOP disadvantage and condensed range signals — CALL is correct despite facing bet+call OOP.

### Axis 8 — Combined (4+7)

**Hands:** MW-49
**Actions:** BET
**Average equity:** 0.5397

**Axis insight:** MW-49 shows how IP range advantage compounds over streets: hero's betting authority on the turn is amplified by position AND range narrowing from the flop bet.

### Axis 3 — Nut Potential

**Hands:** MW-17, MW-18, MW-19, MW-20, MW-21, MW-22
**Actions:** CALL, CALL, BET, CALL, CALL, CHECK
**Average equity:** 0.4308

**Axis insight:** Nut draws (MW-17, MW-21) and nut made hands (MW-19) receive clear BET/CALL signals. Non-nut draws (MW-18, MW-20) receive more cautious CALL signals with MEDIUM confidence. MW-22 (nut draw checked to OOP) correctly identifies CHECK — donk-leading a draw OOP into a 4-way pot is a leak regardless of the draw's strength.

### Axis 4 — Position Amplification

**Hands:** MW-23, MW-24, MW-25, MW-26, MW-27, MW-28
**Actions:** BET, BET, BET, CHECK, BET, BET
**Average equity:** 0.4674

**Axis insight:** IP hands (MW-23, MW-25, MW-27) all receive HIGH confidence BET recommendations. OOP mirrors (MW-24, MW-26, MW-28) receive MEDIUM confidence: MW-24 and MW-28 still BET but with reduced sizing rationale; MW-26 flips to CHECK. The flush draw IP/OOP split (MW-25 vs MW-26) shows the starkest position effect — same draw, opposite action.

### Axis 7 — Range Narrowing

**Hands:** MW-41, MW-42, MW-43, MW-44, MW-45, MW-46
**Actions:** CALL, BET, FOLD, CALL, RAISE, FOLD
**Average equity:** 0.4894

**Axis insight:** MW-43 and MW-46 show FOLD with decent holdings because opponent range credibility is established through consistent action patterns. MW-45 (slowplayed set) and MW-42 (TPTK) show BET/RAISE because hero's range is strong relative to the now-narrowed opponent range. The key insight: range narrowing through streets changes the meaning of opponent actions, requiring re-evaluation at each decision point.

### Axis 6 — SPR Interaction

**Hands:** MW-35, MW-36, MW-37, MW-38, MW-39, MW-40
**Actions:** CALL, CALL, CALL, CALL, CALL, BET
**Average equity:** 0.4114

**Axis insight:** SPR trio (MW-35/36/37) uses identical hand/board with three different SPR levels. All three correctly CALL but with different strategic nuance: MW-35 (SPR 3) = committed/stack-off plan; MW-36 (SPR 8) = standard call; MW-37 (SPR 15) = call with caution, street-by-street reassessment required. The flush draw SPR pair (MW-38/39) shows how deep SPR increases draw value via implied odds.

---

## Coverage Summary

### Hands per Axis

| Axis | Count |
|------|-------|
| Axis 5 — Aggression Respect | 6 |
| Axis 2 — Bluff Compression | 6 |
| Axis 8 — Combined (4+5+7) | 1 |
| Axis 8 — Combined (2+6) | 1 |
| Axis 8 — Combined (3+4+5) | 1 |
| Axis 8 — Combined (4+7) | 1 |
| Axis 3 — Nut Potential | 6 |
| Axis 4 — Position Amplification | 6 |
| Axis 7 — Range Narrowing | 6 |
| Axis 6 — SPR Interaction | 6 |

### Hands per Opponent Count

| Opponents | Count |
|-----------|-------|
| 1 | 4 |
| 2 | 24 |
| 3 | 12 |

### Hands per Street

| Street | Count |
|--------|-------|
| Flop | 30 |
| Turn | 6 |
| River | 4 |

### IP vs OOP Balance

| Position | Count |
|----------|-------|
| IP (hero acts later) | 22 |
| OOP (hero acts earlier) | 18 |

### GTO Action Distribution

| Action | Count |
|--------|-------|
| FOLD | 5 |
| CHECK | 8 |
| CALL | 15 |
| BET | 10 |
| RAISE | 2 |
