# GTO Expert Relabel — FB-15 and FB-35

**Date:** 2026-04-12
**Agent:** GTO Expert (Relabel — positional reclassification)
**Knowledge base:** knowledge/three_way_gto.md v1.3
**Trigger:** REDESIGN_12_AFFECTED_SITUATIONS_2026-04-12.md flagged FB-15 and FB-35 as NEEDS RE-EVALUATION after sandwich-to-closing-action reclassification.

---

## FB-15 — RELABELLED: FOLD to CALL

**Board:** 9d 7d 2c (low two-tone flop)
**Street:** Flop
**Hero position:** BB — **CLOSING ACTION** (corrected from sandwich)
**Hero cards:** Ad 3h
**Bettor:** CO (c-bet 45 into 90)
**Third player:** BTN folded after CO's bet; hero closes action heads-up vs CO
**Pot:** 90 | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25%

**Corrected action history:** CO opens, BTN calls, BB (hero) calls. Flop 9d 7d 2c: BB checks, CO bets 45 into 90. BTN folds. Hero faces bet, closes action.

**Old label:** FOLD — HIGH confidence
**Old reasoning:** "OOP-sandwich EQR of ~60% yields ~18% realized equity, below 25% pot odds."

**New label:** CALL — Confidence: MEDIUM

**Reasoning:** Hero holds the nut flush draw (Ad on a two-diamond board) with approximately 30% raw equity against CO's c-bet range, computed from 9 flush outs to the nuts plus the Ad as an overcard that can make top pair on ace-high turn cards. The original fold was driven entirely by the sandwich EQR penalty: 30% raw equity discounted by a 60% OOP-sandwich EQR yielded ~18% realized equity, well below 25% pot odds. That sandwich penalty no longer applies. With BTN folding, hero is heads-up against CO in closing action — the positional configuration is OOP-closing, not OOP-sandwich. The relevant EQR for OOP-closing is 70-80% (KB Section 1.5), and for what is now effectively a heads-up pot on the flop, realization climbs higher still because there is only one opponent's range to navigate.

The nut flush draw is the single best-realizing draw type in poker. When it hits, hero has the stone-cold nuts with no reverse implied odds from a dominated flush. When it misses, hero can check-fold the turn cleanly — the binary outcome profile (nuts or nothing) maximizes equity realization compared to non-nut draws or marginal made hands that face difficult turn and river decisions. At 30% raw equity with an OOP-closing EQR of ~80% (justified by the nut-or-nothing realization profile and the heads-up pot), realized equity is ~24% — borderline against 25% pot odds but within the margin where the Ad blocker effect tips the balance. The Ad blocks a significant portion of CO's diamond flush draw combos, meaning CO's continuing range is disproportionately made hands (overpairs, top pair) rather than competing flush draws, which improves hero's implied odds when the flush arrives.

The flop context further supports the call: hero has two cards to come, and the call price is a single 50% pot bet. If the turn is a diamond (~19% probability), hero has the nuts and can check-raise or call profitably. If the turn blanks, hero can check-fold to a second barrel — the total investment is one flop call, not a multi-street commitment. This "call one, evaluate on turn" line is the standard GTO approach with nut flush draws on the flop, even OOP, when pot odds are in the 20-25% range. The removal of the sandwich penalty — the only factor that previously pushed this below the calling threshold — restores the hand to its natural action: CALL.

**Solver verification needed:** YES — CALL with MEDIUM confidence. The margin between realized equity and pot odds is narrow (~24% vs 25%). Solver should confirm that the nut flush draw with no side equity beyond the overcard is a call (not a fold) OOP heads-up on this board texture facing a 50% pot c-bet. If the solver shows this as a pure fold even without the sandwich penalty, the label should revert to FOLD.

---

## FB-35 — RELABELLED: FOLD to CALL

**Board:** Kh 6h 3d Qc (turn)
**Street:** Turn
**Hero position:** CO — **CLOSING ACTION** (corrected from sandwich)
**Hero cards:** Kd 9d
**Bettor:** BTN (second barrel 90 into 150)
**Third player:** BB folded after BTN's turn bet; hero closes action heads-up vs BTN
**Pot:** 150 | **Bet:** 90 | **To call:** 90
**Pot odds:** 90 / (150 + 90 + 90) = 27.3%

**Corrected action history:** BTN opens, CO (hero) calls, BB calls. Flop Kh 6h 3d: BB checks, CO checks, BTN bets 30, BB calls, CO calls. Turn Qc: BB checks, BTN bets 90 into 150. BB folds. Hero faces bet, closes action.

**Old label:** FOLD — MEDIUM confidence
**Old reasoning:** "Sandwich squeeze risk from BB means hero's effective equity is lower... sandwich position under-realization pushes this to a fold."

**New label:** CALL — Confidence: MEDIUM

**Reasoning:** Hero holds top pair weak kicker (Kd 9d) on Kh-6h-3d-Qc facing BTN's second barrel. The original fold was explicitly justified by the sandwich penalty — the GTO Expert stated "sandwich position is the deciding factor" and cited KB Section 1.5's ~80% fold frequency for sandwich players. With BB now confirmed as having folded, hero is heads-up against BTN in closing action with no squeeze risk. The entire load-bearing justification for the fold has been removed.

BTN's double-barrel range on K-6-3-Q is polarized between value and bluffs. BTN's value range includes AK, KQ (now two pair), KJ, KT, AA, and QQ (turned set). BTN's bluff and semi-bluff range includes heart flush draws (AhXh, QhJh, JhTh, Th9h that continue barreling), floated broadways that picked up equity on the Q turn (AJ, AT), and some pure bluffs. At a 60% pot turn sizing, GTO principles dictate roughly 2:1 value-to-bluff ratio in the bettor's range, meaning approximately one-third of BTN's double-barrel range is bluffs or semi-bluffs. Hero's K9 beats all bluffs, all semi-bluffs, and ties or beats weaker Kx combos. Against BTN's full double-barrel range, hero's raw equity is approximately 35-40%.

The positional reconfiguration is decisive. In what is now effectively a heads-up pot, OOP EQR is significantly higher than the 3-way sandwich figure — approximately 80-90% for a heads-up OOP spot on the turn with a made hand that has clear showdown value. At 35% raw equity and 80% EQR, realized equity is ~28%, which exceeds the 27.3% pot odds. Even at the conservative end (35% raw, 75% EQR = 26.25%), the shortfall is under 1.1 percentage points — well within the margin where top pair's showdown value and the information advantage of closing action justify a call. Hero knows BB folded, which removes the weakest range from the pot and gives hero complete information about the competitive landscape.

The Qc turn card is unfavorable (completes KQ two pair, brings QQ as a set) but it also adds equity to BTN's bluff range — hands like AhJh or JhTh that picked up a gutshot or overcard now have more reason to barrel. This means BTN's bluffing frequency on the turn is higher than it would be on a brick, which supports hero's call with a bluff-catching hand. K9 with top pair is squarely in hero's bluff-catching range: it beats the bluffs and loses to the value, which is exactly the hand type that should be calling at these pot odds.

**Solver verification needed:** YES — CALL with MEDIUM confidence. Top pair weak kicker facing a second barrel on a board that improved several value hands in villain's range is a classic solver mix spot. The solver should confirm that K9 is in CO's calling range (rather than folding range) when closing action heads-up vs BTN's 60% pot turn bet. If the solver shows K9 as a fold even without the sandwich penalty, the label should revert to FOLD.

---

## Summary Table

| Situation | Old label | New label | Confidence | Change reason | Solver needed |
|-----------|-----------|-----------|------------|---------------|---------------|
| FB-15 | FOLD HIGH | CALL MEDIUM | Sandwich penalty removed; nut flush draw realizes well OOP-closing | YES |
| FB-35 | FOLD MEDIUM | CALL MEDIUM | Sandwich penalty removed; TPWK bluff-catches profitably heads-up | YES |

**Impact on test set label distribution:** 2 labels move from FOLD to CALL. The facing-bet test set previously had 17 CALL, 15 FOLD, 8 RAISE. After this relabel: 19 CALL, 13 FOLD, 8 RAISE. The CALL count increases by 2 at the expense of FOLD. This is directionally expected — removing sandwich penalties makes continuing more attractive in marginal spots.

**Both labels carry MEDIUM confidence and require solver verification.** If solver verification contradicts either label, the label should revert to FOLD with updated reasoning citing the solver result.
