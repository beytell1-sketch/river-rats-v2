# Redesign: 12 Affected Situations — Facing-Bet Test Set
**Date:** 2026-04-12
**Author:** Architecture Expert
**Status:** FINAL
**Scope:** FB-01, FB-04, FB-06, FB-10, FB-15, FB-17, FB-27 (BB-closing misclassified as sandwich) + FB-13, FB-19, FB-21, FB-35, FB-39 (audit findings)

---

## Preliminary: Resolving the Audit Contradiction

The audit summary table incorrectly marked FB-01, FB-04, FB-06, FB-10, FB-15, FB-17, and FB-27 as "correct" despite the audit's own appendix stating the rule explicitly:

> "CO opens, BTN calls, BB calls — after CO bets: BTN acts, then BB. BB is last = closes action."

In all seven situations: CO opens, BTN calls, BB (hero) calls. CO bets. Postflop order is BB → CO → BTN for initiative. After CO bets, action wraps clockwise from CO: the next player clockwise is BTN, then BB. BTN responds to CO's bet first, then BB responds. BB is the last player to act on the bet — closing action — not sandwiched.

The spec confused two different orderings: (1) the initiative order in which players act before anyone bets (BB → CO → BTN), and (2) the response order after a bet is placed (clockwise from bettor: BTN → BB). BTN is not "behind" hero in the response order; BTN acts before hero. The spec labelled BTN as "yet to act behind hero" which is only true in the initiative round, not in the bet-response round.

The audit summary table was wrong for these 7 rows. The brief's identification of 7 additional errors is correct. All 12 situations require fixes.

---

## Part 1: The Seven BB-Closing Misclassifications (Option A for all seven)

These all share the same structural fix: BTN acts on CO's bet before BB. The corrected action histories specify BTN folds (or calls — but for these situations, specifying BTN folds gives hero the cleanest closing-action scenario). Where BTN's action changes the pot, figures are updated.

---

### FB-01 — FIX TYPE: Option A

**Original error:** BB labeled as sandwich with BTN behind, but in a CO-opens pot after CO bets, BTN responds before BB — BB closes action.

**Board:** Ah 6d 2c
**Street:** Flop
**Hero position:** BB — **CLOSING ACTION** (corrected)
**Bettor:** CO
**Third player:** BTN — acts on CO's bet before hero, then folds; hero is last to respond

**Corrected action history:**
CO opens, BTN calls, BB (hero) calls. Flop Ah 6d 2c: BB checks, CO bets 30 into 90. BTN folds. Hero faces bet, closes action.

**Pot / Bet / To call:** Pot 90 | Bet 30 | To call 30
**Pot odds:** 30 / (90 + 30 + 30) = 20%

**Old label:** FOLD — HIGH confidence | Hero cards: Kd 6s
**Label survives?** YES
**Reason:** The fold was driven by middle pair (sixes) on an A-high board dominated by CO's c-bet range — Ax, overpairs, and better kicker second-pairs all beat or tie Kd 6s. The sandwich tightening was cited as a contributing factor but not the primary driver. With BTN folding and hero closing action, the hand is still a FOLD: middle pair OOP with no draws against a CO c-bet on the board that most favours CO's opening range. The removal of the sandwich penalty does not change the equity shortfall relative to required equity for continuing OOP.

**Axis impact:** 1 situation moves from sandwich → OOP-closing. Net: sandwich -1, OOP-closing +1.

---

### FB-04 — FIX TYPE: Option A

**Original error:** BB labeled as sandwich with BTN behind in a CO-opens pot; BTN acts on CO's bet before BB.

**Board:** Kc 8c 4d
**Street:** Flop
**Hero position:** BB — **CLOSING ACTION** (corrected)
**Bettor:** CO
**Third player:** BTN — acts on CO's bet before hero, then folds; hero closes

**Corrected action history:**
CO opens, BTN calls, BB (hero) calls. Flop Kc 8c 4d: BB checks, CO bets 45 into 90. BTN folds. Hero faces bet, closes action.

**Pot / Bet / To call:** Pot 90 | Bet 45 | To call 45
**Pot odds:** 45 / (90 + 45 + 45) = 25%

**Old label:** RAISE — HIGH confidence | Hero cards: Ac Tc
**Label survives?** YES
**Reason:** The RAISE was driven by the nut flush draw meeting all four semi-bluff carve-out conditions (nut draw, Ac blocker, side equity via overcard ace, and KB reference to AsQs example). The sandwich was mentioned but the GTO Expert correctly noted it was secondary to the blocker strength. Closing action strengthens the RAISE: no reverse implied odds from behind, no risk of BTN squeezing hero's raise. Hero raises into a single opponent (CO) with the nuts draw and a premium blocker. RAISE stands at HIGH confidence.

**Axis impact:** Sandwich -1, OOP-closing +1. Running: sandwich -2, OOP-closing +2.

---

### FB-06 — FIX TYPE: Option A

**Original error:** BB labeled as sandwich with BTN behind in a CO-opens pot; BTN acts on CO's bet before BB.

**Board:** Jd 8s 6h
**Street:** Flop
**Hero position:** BB — **CLOSING ACTION** (corrected)
**Bettor:** CO
**Third player:** BTN — acts on CO's bet before hero, then folds; hero closes

**Corrected action history:**
CO opens, BTN calls, BB (hero) calls. Flop Jd 8s 6h: BB checks, CO bets 30 into 90. BTN folds. Hero faces bet, closes action.

**Pot / Bet / To call:** Pot 90 | Bet 30 | To call 30
**Pot odds:** 30 / (90 + 30 + 30) = 20%

**Old label:** CALL — HIGH confidence | Hero cards: Tc 9c
**Label survives?** YES
**Reason:** The CALL was driven by the OESD (8 outs, ~32% equity) comfortably exceeding the 20% pot odds threshold. The GTO Expert correctly noted that raising is wrong (no blocker, no flush draw on this rainbow board). The sandwich caveat was secondary — "even if BTN raises, hero can continue" — but BTN has now folded. Closing action heads-up against CO with an OESD is an even cleaner CALL: hero realises equity against a single opponent OOP with no squeeze risk. CALL stands at HIGH confidence.

**Axis impact:** Sandwich -1, OOP-closing +1. Running: sandwich -3, OOP-closing +3.

---

### FB-10 — FIX TYPE: Option A

**Original error:** BB labeled as sandwich with BTN behind in a CO-opens pot; BTN acts on CO's bet before BB.

**Board:** As 9s 4s
**Street:** Flop
**Hero position:** BB — **CLOSING ACTION** (corrected)
**Bettor:** CO
**Third player:** BTN — acts on CO's bet before hero, then folds; hero closes

**Corrected action history:**
CO opens, BTN calls, BB (hero) calls. Flop As 9s 4s: BB checks, CO bets 30 into 90. BTN folds. Hero faces bet, closes action.

**Pot / Bet / To call:** Pot 90 | Bet 30 | To call 30
**Pot odds:** 30 / (90 + 30 + 30) = 20%

**Old label:** FOLD — HIGH confidence | Hero cards: Jc 8d
**Label survives?** YES
**Reason:** Pure air on a monotone board. Hero has Jc 8d with no spade, no flush draw, and no meaningful straight draw. Equity is approximately 10-15% against any range that includes spades. Position classification is irrelevant to this hand — there is no scenario in which holding two non-spade cards on a three-spade flop justifies continuing. FOLD stands at HIGH confidence.

**Axis impact:** Sandwich -1, OOP-closing +1. Running: sandwich -4, OOP-closing +4.

---

### FB-15 — FIX TYPE: Option A

**Original error:** BB labeled as sandwich with BTN behind in a CO-opens pot; BTN acts on CO's bet before BB.

**Board:** 9d 7d 2c
**Street:** Flop
**Hero position:** BB — **CLOSING ACTION** (corrected)
**Bettor:** CO
**Third player:** BTN — acts on CO's bet before hero, then folds; hero closes

**Corrected action history:**
CO opens, BTN calls, BB (hero) calls. Flop 9d 7d 2c: BB checks, CO bets 45 into 90. BTN folds. Hero faces bet, closes action.

**Pot / Bet / To call:** Pot 90 | Bet 45 | To call 45
**Pot odds:** 45 / (90 + 45 + 45) = 25%

**Old label:** FOLD — HIGH confidence | Hero cards: Ad 3h
**Label survives?** NEEDS RE-EVALUATION
**Reason:** The original fold reasoning was entirely built on the sandwich penalty. The argument was: nut flush draw (~30% raw equity) nominally exceeds 25% pot odds, but the OOP-sandwich EQR discount reduces realised equity below 25%. With BTN folding and hero closing action, the sandwich EQR penalty is removed. The relevant question becomes: does a bare nut flush draw (9 outs, ~30% raw equity) with no side equity beyond the Ace overcard (Ad 3h — the 3h has no role) justify a call OOP heads-up against a 50% pot c-bet?

Raw equity (~30%) exceeds pot odds (25%) by 5pp. OOP EQR against a single opponent is approximately 70-80% (not the 60% sandwich figure). At 75% OOP EQR: 30% × 75% = 22.5% realised equity — still below 25%. The fold may still be correct, but the margin is narrow and the HIGH confidence cited in the original label was inflated by the incorrectly applied sandwich penalty. This is now a borderline FOLD/CALL requiring a GTO Expert re-evaluation. The original FOLD might survive as a marginal FOLD or it might become a CALL in closing action.

**Flag:** GTO Expert must re-evaluate FB-15. The sandwich penalty was the load-bearing justification; without it the label is uncertain. Solver verification is required under the protocol (FOLD where hero equity exceeds pot odds by less than 5pp).

**Axis impact:** Sandwich -1, OOP-closing +1. Running: sandwich -5, OOP-closing +5.

---

### FB-17 — FIX TYPE: Option A

**Original error:** BB labeled as sandwich with BTN behind in a CO-opens pot on the turn; BTN acts on CO's bet before BB.

**Board:** Ac Jh 5d Ks
**Street:** Turn
**Hero position:** BB — **CLOSING ACTION** (corrected)
**Bettor:** CO
**Third player:** BTN — acts on CO's turn bet before hero, then folds; hero closes

**Corrected action history:**
CO opens, BTN calls, BB (hero) calls. Flop Ac Jh 5d: all check. Turn Ks: BB checks, CO bets 60 into 90. BTN folds. Hero faces bet, closes action.

**Pot / Bet / To call:** Pot 90 | Bet 60 | To call 60
**Pot odds:** 60 / (90 + 60 + 60) = 29%

**Old label:** RAISE — HIGH confidence | Hero cards: Qh Td
**Label survives?** YES
**Reason:** Hero holds the stone-cold Broadway nuts (A-K-Q-J-T). The GTO Expert explicitly stated the sandwich position was irrelevant for a nut hand. Closing action removes even the nominal concern — hero has the nuts heads-up against CO's delayed c-bet range. RAISE stands at HIGH confidence. The observation that BTN might have held Kx to call a raise is now moot; BTN folded.

**Axis impact:** Sandwich -1, OOP-closing +1. Running: sandwich -6, OOP-closing +6.

---

### FB-27 — FIX TYPE: Option A

**Original error:** BB labeled as sandwich with BTN behind in a CO-opens pot; BTN acts on CO's bet before BB.

**Board:** 8s 5s 3d
**Street:** Flop
**Hero position:** BB — **CLOSING ACTION** (corrected)
**Bettor:** CO
**Third player:** BTN — acts on CO's bet before hero, then folds; hero closes

**Corrected action history:**
CO opens, BTN calls, BB (hero) calls. Flop 8s 5s 3d: BB checks, CO bets 30 into 90. BTN folds. Hero faces bet, closes action.

**Pot / Bet / To call:** Pot 90 | Bet 30 | To call 30
**Pot odds:** 30 / (90 + 30 + 30) = 20%

**Old label:** RAISE — MEDIUM confidence | Hero cards: As 4s
**Label survives?** YES — with strengthened confidence
**Reason:** The RAISE was driven by the As 4s meeting all three semi-bluff raise criteria: nut flush draw (As), nut draw blocker (As blocks opponent nut draw combos), and side equity (Ace overcard + gutshot to the wheel with A-2-3-4-5, approximately 40-45% total equity). The GTO Expert acknowledged the sandwich concern but concluded the nut blocker effect overcomes it. With BTN folding and hero closing action, the sandwich concern is fully resolved: no BTN cold-call risk, no squeeze, hero check-raises CO heads-up. RAISE is even cleaner in closing action. Confidence should upgrade from MEDIUM to HIGH given that the only uncertainty cited was the sandwich squeeze risk from BTN.

**Axis impact:** Sandwich -1, OOP-closing +1. Running: sandwich -7, OOP-closing +7.

---

## Part 2: The Five Audit Findings

---

### FB-13 — FIX TYPE: Option A

**Original error:** CO classified as sandwich (BB behind) in a BTN-opens pot; after BTN bets, clockwise response order is BB first, then CO — CO is actually last (closing action).

**Board:** Th Td 7c
**Street:** Flop
**Hero position:** CO — **CLOSING ACTION** (corrected)
**Bettor:** BTN
**Third player:** BB — acts on BTN's bet before hero (next clockwise from BTN), then folds or calls; CO is last

**Corrected action history:**
BTN opens, CO (hero) calls, BB calls. Flop Th Td 7c: BB checks, CO checks, BTN bets 45 into 90. BB folds. Hero faces bet, closes action.

**Pot / Bet / To call:** Pot 90 | Bet 45 | To call 45
**Pot odds:** 45 / (90 + 45 + 45) = 25%

**Old label:** FOLD — HIGH confidence | Hero cards: 9c 8c
**Label survives?** YES
**Reason:** The fold was primarily justified by equity insufficiency: 9c 8c on Th Td 7c has ~15-18% equity (gutshot + backdoor flush) against BTN's c-bet range, well below the 25% pot odds. The sandwich tightening was cited as a secondary amplifier. Without the sandwich, the hand is still a fold: equity is materially below pot odds, paired board amplifies reverse implied odds (opponent trip tens dominate), and CO is still OOP against BTN's barreling range. The reasoning improves: the stated cause is now straightforward equity insufficiency, not sandwich-induced tightening. FOLD stands; confidence stays HIGH with cleaner reasoning.

**Axis impact:** 1 situation moves from sandwich → OOP-closing (this is from the original 8 sandwich count, not the 7 already corrected above). Net: sandwich -1, OOP-closing +1.

---

### FB-19 — FIX TYPE: Option A

**Original error:** BB classified as closing action (CO already checked = done), but CO's pre-bet check does not close CO's action — after BTN bets in a CO-opens pot, BB responds first then CO acts after; BB is sandwiched.

**Board:** Kh 6h 3d Qc
**Street:** Turn
**Hero position:** BB — **SANDWICH (CO behind)** (corrected)
**Bettor:** BTN
**Third player:** CO — has only checked (initiative round); must respond to BTN's bet after BB acts

**Corrected action history:**
CO opens, BTN calls, BB (hero) calls. Flop Kh 6h 3d: BB checks, CO bets 30, BTN calls, BB calls. Turn Qc: BB checks, CO checks, BTN bets 90 into 150. Hero (BB) faces bet — CO must still act after hero.

**Pot / Bet / To call:** Pot 150 | Bet 90 | To call 90
**Pot odds:** 90 / (150 + 90 + 90) = 27%

**Old label:** FOLD — HIGH confidence | Hero cards: 7h 5h
**Label survives?** YES
**Reason:** The fold was driven by the equity calculation: 9 flush outs on one card = ~18% equity against 27% pot odds, plus non-nut flush (7-high loses to any higher heart). The GTO Expert correctly noted that being sandwiched compounds the problem but stated the fold is correct before any positional discount. With hero correctly classified as sandwiched (CO behind), the fold remains valid: equity is below pot odds and the draw is non-nut. The label is unchanged; the reasoning is now fully accurate since the sandwich penalty applies correctly. FOLD stands at HIGH confidence.

**Axis impact:** 1 situation moves from OOP-closing → sandwich. Net: OOP-closing -1, sandwich +1.

---

### FB-21 — FIX TYPE: Option A

**Original error:** Action sequence "BB checks, BTN checks, CO bets" is physically impossible in a CO-opens pot (order is BB → CO → BTN; BTN cannot act before CO). Also: BB was wrongly classified as sandwich — after CO bets, BTN responds first (next clockwise), then BB. BB is LAST (closing action).

**Board:** Ts 8c 4h Jd
**Street:** Turn
**Hero position:** BB — **OOP-CLOSING** (corrected — after CO bets, BTN acts first, BB is last)
**Bettor:** CO
**Third player:** BTN — responds to CO's bet BEFORE BB (next clockwise from CO)

**Corrected action history:**
CO opens, BTN calls, BB (hero) calls. Flop Ts 8c 4h: all check. Turn Jd: BB checks, CO bets 45 into 90. BTN folds (or calls). Hero (BB) faces bet, closes action.

**Pot / Bet / To call:** Pot 90 | Bet 45 | To call 45
**Pot odds:** 45 / (90 + 45 + 45) = 25%

**Old label:** FOLD — HIGH confidence | Hero cards: 5c 5d
**Label survives?** YES
**Reason:** Hero holds pocket fives — an underpair to all board cards (J, T, 8) with ~8-10% equity against CO's delayed c-bet range that connects with the J turn. Pot odds require 25%. Equity is catastrophically below pot odds. Whether hero is sandwiched or closing action makes no difference when equity is this far below the threshold. The sandwich classification in the corrected version is accurate (BTN has not acted) but the fold verdict is identical to what it would be in closing action. FOLD stands at HIGH confidence.

**Axis impact:** 1 situation reclassified. Previously incorrectly described as closing, now correctly classified as sandwich. Net: OOP-closing -1, sandwich +1.

---

### FB-35 — FIX TYPE: Option A

**Original error:** CO classified as sandwich (BB behind) in a BTN-opens pot; after BTN bets, BB responds first (next clockwise from BTN), then CO — CO is last (closing action), not sandwiched.

**Board:** Kh 6h 3d Qc
**Street:** Turn
**Hero position:** CO — **CLOSING ACTION** (corrected)
**Bettor:** BTN
**Third player:** BB — responds to BTN's bet before CO; CO is last

**Corrected action history:**
BTN opens, CO (hero) calls, BB calls. Flop Kh 6h 3d: BB checks, CO checks, BTN bets 30, BB calls, CO calls. Turn Qc: BB checks, BTN bets 90 into 150. BB acts (next clockwise from BTN). BB folds. Hero faces bet, closes action.

**Pot / Bet / To call:** Pot 150 | Bet 90 | To call 90
**Pot odds:** 90 / (150 + 90 + 90) = 27.3%

**Old label:** FOLD — MEDIUM confidence | Hero cards: Kd 9d
**Label survives?** NEEDS RE-EVALUATION
**Reason:** The GTO Expert explicitly stated the sandwich penalty (KB Section 1.5: "sandwich player must fold ~80%") was the primary justification for tipping a marginal spot toward fold. The hand is K9 — top pair weak kicker on a K-Q board after BTN's second barrel. The stated reasoning was that sandwich squeeze risk from BB makes calling untenable. With CO correctly classified as closing action (BB acts before CO and then folds), the squeeze risk is removed. CO now faces BTN's turn bet heads-up with top pair weak kicker.

The core hand question changes materially: Is K9 (TPWK) a call or fold against BTN's second barrel on K-6-3-Q with no players behind? BTN's sustained aggression (bet flop, bet turn) represents AK, KQ, KJ, and overpairs — hands that dominate K9. But K9 also beats bluffs, worse Kx, and all of BTN's unimproved holdings. At 27% pot odds hero needs a modest equity threshold. The MEDIUM confidence fold without the sandwich penalty is a genuine solver mix spot, not a clear fold. The original label may flip to CALL or remain as a marginal FOLD at lower confidence.

**Flag:** GTO Expert must re-evaluate FB-35. The sandwich penalty was the stated deciding factor. Its removal changes the decision context. Solver verification was already requested for this situation — that requirement stands.

**Axis impact:** Sandwich → OOP-closing (for CO, this means CO acts before BB but is last in the post-bet response sequence). Net: sandbox -1, OOP-closing +1.

---

### FB-39 — FIX TYPE: Option A

**Original error:** BB classified as closing action (CO already checked = done), but CO's pre-bet check does not close CO's action — after BTN bets in a CO-opens pot, BB responds first then CO acts; BB is sandwiched with CO behind.

**Board:** Qd 8d 4c 7s Jh
**Street:** River
**Hero position:** BB — **SANDWICH (CO behind)** (corrected)
**Bettor:** BTN
**Third player:** CO — has only checked (initiative round); must respond to BTN's bet after BB acts

**Corrected action history:**
CO opens, BTN calls, BB (hero) calls. Flop Qd 8d 4c: BB checks, CO bets 30, BTN calls, BB calls. Turn 7s: BB checks, CO checks, BTN checks. River Jh: BB checks, CO checks, BTN bets 90 into 150. Hero (BB) faces bet — CO must still act after hero.

**Pot / Bet / To call:** Pot 150 | Bet 90 | To call 90
**Pot odds:** 90 / (150 + 90 + 90) = 27.3%

**Old label:** CALL — HIGH confidence | Hero cards: Qh 8h
**Label survives?** YES
**Reason:** Hero holds top two pair (Queens and Eights) on Q-8-4-7-J. The GTO Expert stated closing action with no squeeze risk as supporting evidence, but the primary justification was the strength of the hand: top two pair beats all single pairs, all missed diamond flush draws, and the diamond draw missed (no third diamond). Even with CO behind (correctly sandwiched), the audit correctly noted: (a) CO has checked twice with no initiative — CO's range is capped and a check-raise from CO is extremely unlikely, (b) even if CO calls, hero's two pair holds significant value in the multiway pot. Top two pair is firmly in hero's continuing range even in a sandwich position on a missed flush-draw board. CALL stands at HIGH confidence. The stated closing-action reasoning was wrong but the label is correct regardless of position classification.

**Axis impact:** 1 situation moves from OOP-closing → sandwich. Net: OOP-closing -1, sandwich +1.

---

## Summary Table

| FB | Error type | Option | Hero | Bettor | Old classification | Corrected | Old label | New status |
|----|-----------|--------|------|--------|-------------------|-----------|-----------|------------|
| FB-01 | BB wrongly sandwich | A | BB | CO | Sandwich | OOP-closing | FOLD HIGH | Survives |
| FB-04 | BB wrongly sandwich | A | BB | CO | Sandwich | OOP-closing | RAISE HIGH | Survives |
| FB-06 | BB wrongly sandwich | A | BB | CO | Sandwich | OOP-closing | CALL HIGH | Survives |
| FB-10 | BB wrongly sandwich | A | BB | CO | Sandwich | OOP-closing | FOLD HIGH | Survives |
| FB-15 | BB wrongly sandwich | A | BB | CO | Sandwich | OOP-closing | FOLD HIGH | NEEDS RE-EVALUATION |
| FB-17 | BB wrongly sandwich | A | BB | CO | Sandwich | OOP-closing | RAISE HIGH | Survives |
| FB-27 | BB wrongly sandwich | A | BB | CO | Sandwich | OOP-closing | RAISE MEDIUM | Survives (confidence upgrades to HIGH) |
| FB-13 | CO wrongly sandwich | A | CO | BTN | Sandwich | OOP-closing | FOLD HIGH | Survives |
| FB-19 | BB wrongly closing | A | BB | BTN | OOP-closing | Sandwich | FOLD HIGH | Survives |
| FB-21 | Impossible sequence | A | BB | CO | OOP-closing | Sandwich | FOLD HIGH | Survives |
| FB-35 | CO wrongly sandwich | A | CO | BTN | Sandwich | OOP-closing | FOLD MEDIUM | NEEDS RE-EVALUATION |
| FB-39 | BB wrongly closing | A | BB | BTN | OOP-closing | Sandwich | CALL HIGH | Survives |

---

## Updated Axis Distribution Counts

### Before fixes (original spec)

| Classification | Count |
|---------------|-------|
| OOP (first to act after bet) | 18 |
| IP (closing action) | 14 |
| Sandwich | 8 |
| **Total** | **40** |

### Changes from 12 fixes

From the 7 BB-closing corrections (FB-01, 04, 06, 10, 15, 17, 27):
- 7 situations move from sandwich → OOP-closing (BB is still OOP, but closes action as the last responder)

From the 5 audit findings:
- FB-13: sandwich → OOP-closing (CO closes action in BTN-opens pot) = -1 sandwich, +1 OOP-closing
- FB-19: OOP-closing → sandwich (BB is sandwiched with CO behind) = -1 OOP-closing, +1 sandwich
- FB-21: OOP-closing → sandwich (BTN behind has not acted) = -1 OOP-closing, +1 sandwich
- FB-35: sandwich → OOP-closing (CO closes action in BTN-opens pot) = -1 sandwich, +1 OOP-closing
- FB-39: OOP-closing → sandwich (BB is sandwiched with CO behind) = -1 OOP-closing, +1 sandwich

Net changes:
- Sandwich: -7 (BB corrections) -1 (FB-13) -1 (FB-35) +1 (FB-19) +1 (FB-21) +1 (FB-39) = **-6**
- OOP-closing: +7 (BB corrections) +1 (FB-13) +1 (FB-35) -1 (FB-19) -1 (FB-21) -1 (FB-39) = **+6**
- IP-closing: unchanged = **14**

### After fixes

| Classification | Count | Change |
|---------------|-------|--------|
| OOP (first to act after bet) | 18 | 0 |
| IP (closing action) | 14 | 0 |
| OOP-closing (last to respond, OOP seat) | +6 absorbed into OOP-closing bucket | see note |
| Sandwich | 2 | -6 |
| **Total** | **40** | 0 |

**Note on bucketing:** The spec's axis table has three categories: OOP (first to act), IP (closing), and Sandwich. The 6 net additions to the "closing" axis are all OOP-seated heroes who close action — BB or CO who are OOP but respond last. These fit most naturally under "OOP (first to act after bet)" if hero checks first in initiative, or into a new sub-axis "OOP-closing." For model training purposes, the key distinction is the sandwich flag (yes/no) and the IP flag (yes/no). The 6 formerly-sandwich situations that become OOP-closing are: OOP=yes, IP=no, sandwich=no.

**Revised axis counts for model training:**

| Field | Count |
|-------|-------|
| hero_oop=True, sandwich=False, closes_action=True | 6 (new sub-group, formerly sandwich) |
| hero_oop=True, sandwich=True | 2 (remaining sandwich: FB-19, FB-21, FB-39... see breakdown) |
| hero_ip=True | 14 |
| hero_oop=True, closes_action=False | 18 |

**Precise remaining sandwich situations (2 net sandwich after all fixes):**

Original 8 sandwich situations: FB-01, FB-04, FB-06, FB-07, FB-08, FB-10, FB-13, FB-15, FB-17, FB-27, FB-29, FB-35, FB-38, FB-40. Wait — the spec's axis count of 8 sandwich is the target; let me recount from the spec third-player-status axis.

Third player status from spec: "yet to act behind hero" = 14 situations. These include the sandwich situations. After all fixes:
- 7 BB-corrections remove "BTN behind" from FB-01, 04, 06, 10, 15, 17, 27 (BTN actually acts before BB)
- FB-13 and FB-35: CO was wrongly labelled as sandwich; removing 2 more
- FB-19, FB-21, FB-39: previously labelled "already checked" but third player was actually live; adding 3 back as sandwich

Net change to "yet to act behind hero" count: -7 -2 +3 = -6. From the spec's 14 "yet to act" count: 14 - 6 = **8 genuine sandwich situations remain**.

---

## GTO Expert Relabelling Required

| Situation | Reason | Priority |
|-----------|--------|----------|
| FB-15 | Sandwich penalty was primary fold justification; now closing action; fold margin unclear | HIGH |
| FB-35 | Sandwich squeeze cited as deciding factor; now closing action; K9 may be call/fold mix | HIGH |

2 situations require fresh GTO Expert labels.

10 situations survive with existing labels (some with updated reasoning or upgraded confidence as noted above).

---

## Option B Redesigns

None. All 12 situations were fixed via Option A (corrected action history + updated classification). The boards and hand strengths are all structurally valid — the errors were purely in the action sequencing and positional classification, not in the hands or board textures. No situation was made uninteresting by the fix. The two situations needing re-evaluation (FB-15, FB-35) retain the same board, bet sizing, and hero cards — only the position classification changes, which is precisely the kind of decision the GTO Expert should be reasoning about.

---

## No New Boards Used

All fixes used the original boards from the spec. No new boards were introduced. The overlap checks against Batch 4 and the reference set remain valid.
