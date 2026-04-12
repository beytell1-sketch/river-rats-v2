# GTO Expert Agent 2 — Facing-Bet Labels FB-11 through FB-20

**Date:** 2026-04-12
**Agent:** GTO Expert (Agent 2)
**Knowledge base:** knowledge/three_way_gto.md v1.3
**Spec source:** review/comms/ML_ARCHITECT_FACING_BET_TEST_SET_2026-04-12.md

---

### FB-11

**Board:** As 9s 4s (monotone flop)
**Street:** Flop
**Hero position:** BTN (IP — closes action)
**Hero cards:** Kh Qs
**Pot:** 90 | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25%

**GTO Action:** CALL — Confidence: MEDIUM

**Reasoning:** Hero holds the Qs, giving a second-nut flush draw on a monotone As-9s-4s board. BB's donk-bet range on a monotone flop is polarised: made flushes (small suited connectors that hit), strong Ax with a spade, and some semi-bluffs with a single spade. Hero's Qs flush draw has approximately 35% equity against this range (9 flush outs minus reverse implied odds when BB has a higher flush). The pot odds require 25% equity, so hero is well ahead of that threshold. However, RAISE is not correct here despite the draw strength: hero does not hold the nut flush draw (the As is on the board, so the Ks is the nut draw, and hero has only the Qs — the second nut draw). Per the KB Section 1.7, non-nut draws without a blocker to villain's continuing range should call rather than raise 3-way. The Kh provides no blocker value on this board. IP position means hero realises equity well (EQR 105-120%), making a call clearly profitable. FOLD is wrong given the equity surplus over pot odds.

**Solver verification needed:** YES — CALL with MEDIUM confidence on a flush draw facing donk bet on monotone; equity vs narrowed range needs verification.

---

### FB-12

**Board:** Th Td 7c (paired flop)
**Street:** Flop
**Hero position:** BB (OOP — closes action)
**Hero cards:** Jd Jc
**Pot:** 90 | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25%

**GTO Action:** CALL — Confidence: HIGH

**Reasoning:** Hero holds JJ, an overpair on a Th-Td-7c paired board. BTN's c-bet range on a paired flop includes Tx (trips), overpairs (QQ+), some 7x, and air/broadways that float. Hero's JJ has roughly 55-60% equity here: it beats all of BTN's air, 7x, and underpairs, while losing only to Tx trips, QQ+, and the rare full house. At 25% pot odds, JJ is a clear continue. RAISE is not correct because on a paired board, the hands that call a raise are almost exclusively Tx or better, which dominate JJ — hero would be turning a profitable call into a value-own. FOLD is clearly wrong with an overpair when pot odds are this generous. Hero closes action so there is no sandwich concern. OOP position reduces equity realisation somewhat, but the hand is strong enough that this is a straightforward call.

**Solver verification needed:** NO

---

### FB-13

**Board:** Th Td 7c (paired flop)
**Street:** Flop
**Hero position:** CO (sandwich — BB yet to act behind)
**Hero cards:** 9c 8c
**Pot:** 90 | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25%

**GTO Action:** FOLD — Confidence: HIGH

**Reasoning:** Hero holds 9c8c in the sandwich position on a Th-Td-7c paired board. This hand has a gutshot (6 makes a straight) and a backdoor flush draw, giving roughly 15-18% equity against BTN's c-bet range. The pot odds require 25%, so hero is below the threshold even before accounting for the sandwich penalty. The KB is clear that the sandwich player must tighten continuing range by 15-20% vs closing-action cutoffs (Section 2, Factor 2). BB is yet to act behind and could wake up with trips, an overpair, or a check-raise with a strong hand. Gutshot-only hands with backdoor equity are explicitly check/fold candidates 3-way per Section 1.7. The 9c8c has no blockers to villain's value range (no Tx) and no nut potential. CALL is wrong because equity is insufficient and position is the worst possible seat. RAISE is absurd without nut potential on a paired board.

**Solver verification needed:** NO

---

### FB-14

**Board:** 9d 7d 2c (low two-tone flop)
**Street:** Flop
**Hero position:** BTN (IP — closes action)
**Hero cards:** 7c 7h
**Pot:** 90 | **Bet:** 30 | **To call:** 30
**Pot odds:** 30 / (90 + 30 + 30) = 20%

**GTO Action:** RAISE — Confidence: HIGH

**Reasoning:** Hero holds 7c7h on 9d-7d-2c, giving middle set on a low two-tone board. BB's donk-bet range on this board is wide (this texture smashes BB's defending range: 9x, 7x, flush draws, 65s, small pairs) but mostly non-nut holdings. Hero's set of 7s is the second-best possible hand (behind 99 for top set, and ahead of 22 for bottom set). With approximately 75-80% equity against BB's donk-bet range, hero has a clear value raise. The small 33% pot sizing from BB invites a raise — hero can raise to approximately 3x (90) to charge the flush draws that are prevalent on this two-tone board. Per the KB Section 1.7, sets are explicitly labelled RAISE in training data. IP position is ideal for a raise: hero closes action, so there is no squeeze risk from a third player (CO already folded). The two-tone texture makes raising urgent — hero needs to charge the diamond flush draws for maximum value and to deny free equity. Calling risks allowing a cheap diamond turn that kills action or beats hero.

**Solver verification needed:** YES — RAISE label requires solver verification per rules.

---

### FB-15

**Board:** 9d 7d 2c (low two-tone flop)
**Street:** Flop
**Hero position:** BB (OOP — sandwich, BTN yet to act)
**Hero cards:** Ad 3h
**Pot:** 90 | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (90 + 45 + 45) = 25%

**GTO Action:** FOLD — Confidence: HIGH

**Reasoning:** Hero holds Ad3h on 9d-7d-2c in the sandwich position facing CO's c-bet with BTN still to act. The Ad gives a nut flush draw (9 outs to the nut flush), but the hand has no pair, no straight draw, and no other equity beyond the flush draw. Raw equity is approximately 28-32% against CO's c-bet range, which superficially exceeds the 25% pot odds. However, the sandwich position is critical: BTN is yet to act behind and could raise or call, creating a multiway scenario where hero's non-nut-made equity (when the flush doesn't come) is minimal. The KB Section 1.7 states that nut draw without a blocker to villain's continuing range should CALL rather than RAISE, but hero's Ad3h has virtually no side equity — no overcards that matter (3h is worthless), no straight potential. The Ad is a blocker but without side equity (overcards, gutshot), the hand is marginal. OOP position crushes equity realisation (EQR 60-80%). With the sandwich penalty (tighten 15-20%) applied to the already-marginal equity, and the risk of BTN raising behind, FOLD is correct. Quantified: even at 30% raw equity, OOP-sandwich EQR of ~60% yields ~18% realized equity, well below the 25% pot odds threshold. The equity realisation discount for OOP-sandwich makes the nominally above-threshold raw equity insufficient.

**Solver verification needed:** YES — FOLD where hero equity (~30%) appears to exceed pot odds (25%) by more than 5pp; needs solver check that OOP sandwich discount justifies the fold.

---

### FB-16

**Board:** 9d 7d 2c (low two-tone flop)
**Street:** Flop
**Hero position:** BB (OOP — faces bet-and-call)
**Hero cards:** 5d 5c
**Pot:** 135 (after BTN call) | **Bet:** 45 | **To call:** 45
**Pot odds:** 45 / (135 + 45) = 25%

**GTO Action:** FOLD — Confidence: HIGH

**Reasoning:** Hero holds 5d5c on 9d-7d-2c facing a bet-and-call from CO and BTN. The bet-and-call signal is the strongest range-narrowing signal in 3-way poker (KB Section 2, Factor 5). CO's bet into the flop represents overpairs, top pair, sets, and strong draws. BTN's cold-call of that bet further narrows to hands strong enough to continue against both the bettor and a remaining player — likely 9x, 7x, flush draws, and overpairs. Hero's 55 is a small underpair with no diamond for a flush draw. Equity against two narrowed ranges is approximately 15-18% (set outs only — two fives for roughly 8% equity on one card). The pot odds require 25%, and hero falls well short. Even if hero hits a set on the turn, the two-tone board means flush draws could still beat hero. The 5d provides a marginal backdoor flush component but this is explicitly identified as insufficient by the KB (backdoor-only = check/fold). With both opponents showing confirmed strength and hero holding an underpair with no draws, FOLD is clear.

**Solver verification needed:** NO

---

### FB-17

**Board:** Ac Jh 5d Ks (turn)
**Street:** Turn
**Hero position:** BB (OOP — sandwich, BTN yet to act)
**Hero cards:** Qh Td
**Pot:** 90 | **Bet:** 60 | **To call:** 60
**Pot odds:** 60 / (90 + 60 + 60) = 29%

**GTO Action:** RAISE — Confidence: HIGH

**Reasoning:** Hero holds QhTd on Ac-Jh-5d-Ks. The board provides A, K, J and hero provides Q, T, completing the Broadway straight (A-K-Q-J-T) — the stone-cold nuts on this turn. CO's delayed c-bet (checked a dry A-J-5 flop, then bet 67% pot when the Ks arrived) represents Kx that improved, AK for top two pair, or KJ for two pair. These hands will pay off a raise. BTN behind may also hold Kx or AJ and want to call. With the nuts in a 3-way pot, RAISE is mandatory to build the pot and charge draws — any paired board card on the river could make a full house for set holders (55, JJ), so hero must extract maximum value now. The sandwich position is irrelevant when hero holds the nuts; hero actively wants BTN to come along for a bigger pot. Per the KB Section 1.7, sets and the pure nuts are explicitly labelled RAISE in training data.

**Solver verification needed:** YES — RAISE label requires solver verification per rules.

**Cross-reference note:** FB-37 (Agent 4) has the same nut straight on the same board but labels CALL from a closing-action position. The solver typically mixes RAISE/CALL with the nuts. Both labels are acceptable — model scoring should accept either CALL or RAISE on FB-17 and FB-37.

---

### FB-18

**Board:** Ac Jh 5d Ks (turn)
**Street:** Turn
**Hero position:** BTN (IP — closes action)
**Hero cards:** Kd Jd
**Pot:** 90 | **Bet:** 60 | **To call:** 60
**Pot odds:** 60 / (90 + 60 + 60) = 29%

**GTO Action:** CALL — Confidence: MEDIUM

**Reasoning:** Hero holds KdJd on Ac-Jh-5d-Ks, giving two pair (Kings and Jacks) on the turn. CO's delayed c-bet — checking an A-J-5 flop and then betting when the K arrives — is a strong signal. CO likely holds Kx (especially AK for top two pair, or KQ for a strong pair), and some hands that decided to trap the flop (sets of 5s, AA). Hero's KJ two pair is a strong hand but vulnerable: AK dominates it (also two pair but with the better kicker pair), and sets beat it. However, KJ two pair still beats a large portion of CO's range: single Kx hands (KQ, KT), Ax hands that didn't bet the flop (AT, A9s), and any air or draws that CO is semi-bluffing. Equity is approximately 55-65% against CO's range, well above the 29% pot odds. RAISE is tempting but risky: the hands that call or re-raise a raise on this board are almost exclusively AK or better, which dominate KJ. The KB default rule says non-set made hands at mixed SPR default to CALL (Section 1.7). IP position ensures excellent equity realisation on the river. CALL captures value from CO's worse hands while avoiding a value-own against AK.

**Solver verification needed:** YES — CALL with MEDIUM confidence; two pair facing delayed c-bet is a common solver mix spot.

---

### FB-19

**Board:** Kh 6h 3d Qc (turn)
**Street:** Turn
**Hero position:** BB (OOP)
**Hero cards:** 7h 5h
**Pot:** 150 | **Bet:** 90 | **To call:** 90
**Pot odds:** 90 / (150 + 90 + 90) = 27%

**GTO Action:** FOLD — Confidence: HIGH

**Reasoning:** Hero holds 7h5h on Kh-6h-3d-Qc facing BTN's turn bet of 90 into 150 after BTN called the flop bet and now fires the turn when CO checks. Hero had a flush draw on the flop (two hearts) but the turn Qc is a blank — the flush draw remains but hero has only one card to come. With 9 flush outs, hero has approximately 18% equity (9/46) on one card. The pot odds require 27%, so hero is well below the required equity. The 7h5h has no pair, no straight draw that matters (hero needs runner-runner), and the flush draw alone is insufficient. BTN's turn bet after calling the flop and seeing CO check is a strong signal: BTN likely has Kx, Qx that improved, or a strong made hand. Even if hero hits the flush, it's the 7-high flush — any opponent with Ah or higher heart has a better flush draw. OOP position further diminishes equity realisation. With equity below pot odds, no implied odds from a non-nut flush, and OOP position, FOLD is clear.

**Solver verification needed:** NO

---

### FB-20

**Board:** Kh 6h 3d Qc (turn)
**Street:** Turn
**Hero position:** CO (OOP — closes action, BB out)
**Hero cards:** Ah Jh
**Pot:** 120 | **Bet:** 90 | **To call:** 90
**Pot odds:** 90 / (120 + 90 + 90) = 30%

**GTO Action:** CALL — Confidence: MEDIUM

**Reasoning:** Hero holds AhJh on Kh-6h-3d-Qc facing BTN's second barrel of 90 into 120 (75% pot). Hero has the nut flush draw (Ah is the nut heart) plus a gutshot straight draw (any T makes A-K-Q-J-T Broadway). That gives approximately 9 flush outs + 3 clean straight outs (Ts, Td, Tc — the Th is already counted in flush outs) = 12 outs, roughly 26% equity on one card. The pot odds require 30%, so raw equity on the turn alone is slightly below pot odds. However, implied odds are significant: if hero hits the nut flush or Broadway straight on the river, BTN's strong range (Kx, Qx, two pair) will pay off a river bet. The Ah also serves as a blocker to BTN's nut flush draw combos, making it slightly less likely BTN has a flush draw and more likely BTN's range is made-hand heavy (which pays off hero's draws). RAISE is considered: hero has the nut flush draw with a blocker and side equity (gutshot + Ace overcard), which meets the Section 1.7 criteria for a semi-bluff raise. However, this is now heads-up on the turn (not 3-way), and BTN's 75% pot sizing suggests a strong range. Raising OOP risks getting jammed on when hero misses. The default for draws with implied odds that approach break-even is CALL, reserving raise for situations with higher fold equity. CALL is the conservative correct action.

**Solver verification needed:** YES — CALL with MEDIUM confidence; nut flush draw + gutshot facing large turn barrel is a classic raise/call mix spot.

---

## Summary Table

| Situation | Hero cards | Action | Confidence | Solver needed |
|-----------|-----------|--------|------------|---------------|
| FB-11 | Kh Qs | CALL | MEDIUM | YES |
| FB-12 | Jd Jc | CALL | HIGH | NO |
| FB-13 | 9c 8c | FOLD | HIGH | NO |
| FB-14 | 7c 7h | RAISE | HIGH | YES |
| FB-15 | Ad 3h | FOLD | HIGH | YES |
| FB-16 | 5d 5c | FOLD | HIGH | NO |
| FB-17 | Qh Td | RAISE | HIGH | YES |
| FB-18 | Kd Jd | CALL | MEDIUM | YES |
| FB-19 | 7h 5h | FOLD | HIGH | NO |
| FB-20 | Ah Jh | CALL | MEDIUM | YES |

**Distribution:** 4 CALL, 4 FOLD, 2 RAISE

**Note on distribution:** The spec target was 3-4 CALL, 3-4 FOLD, 2-3 RAISE. Final distribution is 4/4/2, within target range. Both RAISE labels are nut or near-nut holdings (middle set, Broadway straight) consistent with the KB rule that only sets and the pure nuts are labelled RAISE in training data.
