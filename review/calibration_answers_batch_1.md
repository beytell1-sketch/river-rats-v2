# Calibration Batch 1 — GTO Labels

**Agent:** GTO Labelling Agent (gto_labeller_v1 + three_way_gto v1.2)
**Date:** 2026-04-09
**Batch:** calibration_batch_1.json (8 situations)

---

REF_ID: MW-12
ACTION: CHECK
CONFIDENCE: HIGH
REASONING: Hero holds JsTs on 8c5d2h with 13.55% equity and zero draw outs — pure air with no improvement path. Although hero is IP with closing action and villain_air_pct is high (0.56), a bet here is a pure bluff requiring both opponents to fold. 3-way pure bluffs are unprofitable (need ~49% combined fold equity, break-even for a pot-sized bet), and with only 13.55% equity there is no semi-bluff component to fall back on if called. The dry board and checked-around action tempt a bet, but with no made hand and no draw, the correct action is CHECK and concede equity realization.

---

REF_ID: MW-13
ACTION: CHECK
CONFIDENCE: HIGH
REASONING: Hero holds KhJh on Ac9d3s with 14.22% equity, no draw, and is OOP acting first. KJ completely missed this ace-high board — no pair, no flush draw, no straight draw. Betting OOP into two opponents with 14% equity is a pure bluff that fails both the fold equity threshold (need ~49% combined) and the semi-bluff conditions (no draw). With villain_aggression_count=1 showing prior street aggression and a board that favours the BTN opener's range (board_favour=0.19), CHECK is the only correct action. Hero should check and fold to any bet given the equity level.

---

REF_ID: MW-14
ACTION: CALL
CONFIDENCE: HIGH
REASONING: Hero holds Td9d on Jd8d3h — a massive combo draw with 17 outs (flush draw plus open-ended straight draw), generating 51.08% equity against 26.83% pot odds. The equity surplus of over 24 percentage points makes calling clearly profitable even OOP. This is a non-nut flush draw (queen-high, not ace-high), so Section 1.7 conditions for raising are not met — the correct action is CALL rather than RAISE. With num_callers_to_bet=0 there is no bet-and-call signal narrowing the field, and the single CO bet does not represent a condensed enough range to override the enormous equity advantage. CALL and realize 51% equity against 27% pot odds.

---

REF_ID: MW-15
ACTION: CHECK
CONFIDENCE: HIGH
REASONING: Hero holds 9s8s on QsJd5h2c6c on the river with 0.0% equity — a completely busted straight draw that cannot win at showdown. With better_hand_pct=0.957 and only 1.7% of hands losing to hero, betting would be a pure bluff requiring both opponents to fold. 3-way pure bluffs are unprofitable by the fold equity math, and on the river there are no future draw outs to justify a semi-bluff. Even though villain_checked_back=1 (BB showed weakness) and villain_air=0.35, the 0% showdown equity means a check-behind concedes a pot hero cannot win anyway. A bluff into two opponents with 0% equity is the clearest possible violation of the 3-way pure bluff rule.

---

REF_ID: MW-17
ACTION: CALL
CONFIDENCE: MEDIUM
REASONING: Hero holds AdKs on Jd8d4c with raw equity of 23.55% against pot odds of 26.83% — slightly below breakeven on reported features alone. However, this is the overcard hidden-equity pattern from Worked Example 7: draw_outs=0 because the pipeline does not count overcard outs, but AK has 6 overcard outs (3 aces + 3 kings worth approximately 24% improvement probability to top pair by the river) and the Ad provides backdoor flush equity on a two-diamond board. Accounting for these hidden outs pushes true equity close to or above pot odds, and implied odds when hero makes TPTK add further value. With num_callers_to_bet=0 (no bet-and-call signal) and a single CO c-bet, the action does not narrow ranges enough to override the improvement potential. CALL is correct per the AK-overcards precedent.

---

REF_ID: MW-18
ACTION: CALL
CONFIDENCE: HIGH
REASONING: Hero holds Qd3d on Jd8d4c with a non-nut flush draw generating 35.60% equity against 26.83% pot odds — a clear equity surplus of nearly 9 percentage points. Section 1.7 specifies that non-nut flush draws should call or fold, not raise; the conditions for raising (nut draw with blocker plus side equity) are not met here. With equity well above pot odds and no bet-and-call signal (num_callers_to_bet=0), folding would be a significant mistake — hero is giving up 35.6% equity for a 26.83% price. The hand is OOP and the flush draw is visible to opponents, but the equity surplus is too large to fold, making CALL the correct action.

---

REF_ID: MW-19
ACTION: BET
CONFIDENCE: HIGH
REASONING: Hero holds Tc9c on QhJs8d for the flopped nut straight (Q-J-T-9-8) with 82.93% equity, is_monster=1, and better_hand_pct=0.0. Both opponents checked to hero IP on a connected board (danger_score=0.30) that can produce flush draws and straight draws on later streets. Per Worked Example 4, monsters must bet multiway — with two opponents potentially holding draws, giving a free card risks being outdrawn at twice the rate versus heads-up. IP position plus near-100% of hands dominated makes this a mandatory value bet. Slow-playing is the only rejected alternative; with a connected board and two draw-capable opponents, betting for protection and value is unambiguously correct.

---

REF_ID: MW-23
ACTION: BET
CONFIDENCE: HIGH
REASONING: Hero holds QhJc for top pair second kicker on Qc8d3s (dry rainbow) with both opponents checked, IP with closing action. The feature constellation is strongly favourable: villain_air_pct=0.507 (over half of villain range is air), better_hand_pct=0.095 (only 9.5% of hands beat hero), villain_range_capped=1 (capped range, no premiums), and board danger_score=0.00 (static equity). This mirrors Worked Example 2 precisely — IP, both opponents showed weakness, high air, dry board. With 89% of villain hands losing to QJ and a static board where equity will not shift, a small bet (25-33% pot) extracts value from worse pairs and Jx hands while the capped range limits the risk of running into a dominating hand. The 49% equity reading understates the true advantage given the specific range composition.
