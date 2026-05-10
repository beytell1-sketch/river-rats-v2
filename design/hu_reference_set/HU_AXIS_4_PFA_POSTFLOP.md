# HU Axis 4 — Preflop Aggressor Postflop Discipline (HU-4.1 to HU-4.5)

**Date:** 2026-05-10
**Status:** Design only — no labelling, no corpus changes
**Context:** Phase 1.5-D.1 HU reference set — 1 of 6 axis breakouts (per design memo §4.2)

## Axis intro

Axis HU-4 targets heads-up postflop spots where hero is the **preflop aggressor**
(BTN open or SB open; villain BB calls). The decision class under test is
**c-bet sizing + frequency discipline across dry vs wet board textures**: when
does PFA range-c-bet small (25%) for cheap equity denial, when does PFA bet
polarized (66%) to leverage range advantage on textures that allow it, and
when does PFA check the entire range (or the bottom of it) on textures that
shift range advantage to BB. The 5 hands span a TP+/draws/air composition
triple per `feedback_preflop_geometry_vs_postflop_composition.md` so the
sizing-frequency dimension is exercised across hand-strength categories rather
than within a single bucket. Across the 5 hands board texture varies dry rainbow
K-high / monotone broadway / two-tone TP-completing / two-tone wet draw-heavy /
dry low to checked-turn delayed-c-bet lines.

All 5 hands are heads-up (`num_opponents: 1`). Hero is the PFA in every spot
(BTN or SB opener; never BB). Bet sizes are solver-aligned per
`feedback_solver_aligned_sizing.md` (flop 25%/66%, turn 33%/75%, river
33%/75%/150%); deviations are documented inline. 3 hands are CLOSE
(model-uncertainty + poker-difficulty driven per `feedback_close_hand_selection.md`,
anchored on v9-3way-v22-on-59 predictive entropy across the 25% / 66% / check
action class trade-off); 2 hands are CANONICAL (uncontroversial small-range-c-bet
or check-back anchors).

Cross-axis hygiene: hero hands and flop boards do not collide with HU-1
(AhKs, 9d9c, KhQd, TsTd, AhJh; flops Ad8c3h, 9h7s2c, KcTc6d, 8h5c2d, Jc9c5d),
HU-2 (AhQh, Td9d, Js9s, 6c5c, Ad5d; flops Kd7h4h, 8s6c2d, Qs7s3d, 8c7d4h,
Jh8d3c), or HU-3 (7c6h, 4d3d, KsQs, Ts8h, Ac4c; flops AhKd4s, QcJh9s, 8h6h5c,
7d7c3h, Kh9d6s).

---

## Hand index

| ID | Marker | Street | Hero pos | Hand | Board | Decision class |
|----|--------|--------|----------|------|-------|----------------|
| HU-4.1 | CANONICAL | Flop | BTN | JsJh | Kd 7h 2c | Overpair on dry K-high, small range c-bet |
| HU-4.2 | CANONICAL | Flop | BTN | 4h4c | Kh Qh 9h | Small underpair on monotone broadway, check-back |
| HU-4.3 | CLOSE | Flop | SB | KsTs | Td 7d 5s | TP good kicker on two-tone wet, 25% vs 66% sizing dilemma |
| HU-4.4 | CLOSE | Flop | SB | QhJh | 9h 8h 2c | Combo draw on two-tone wet, polar 66% vs 25% vs check |
| HU-4.5 | CLOSE | Turn | BTN | AhJc | Tc 7c 3s 5d | Delayed c-bet sizing on dry-to-wet turn |

---

## HU-4.1: JsJh overpair on Kd7h2c dry rainbow, BTN small range c-bet vs BB

**Marker:** CANONICAL

**Target axis:** Axis HU-4 — Preflop aggressor postflop discipline
**Hero cards:** Js/Jh
**Board:** Kd 7h 2c
**Street:** Flop
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 5.5bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** TP+ (overpair to the 7-2 part of the board; second
pair to the king. JJ has showdown value vs all of BB's defend range below KQo
and beats every underpair / Ax-no-pair in BB's range, while losing to Kx and
sets only).

**Action history:** 100bb effective. BTN (hero) opens 2.5bb, SB folds, BB calls.
Flop Kd 7h 2c (rainbow, K-high, disconnected, BTN range-favoured top-of-board
texture). BB checks. Hero acts.

**Solver sizing notes:** The canonical solver action class on Kd7h2r vs BB
defend is a high-frequency 25% pot range-c-bet (solver-aligned flop small
size); JJ as a medium-strength made hand sits squarely in the range-bet block
because the texture's range-vs-range equity advantage sits with BTN (BTN's
range contains all the AK / KQ / KJ / KT / K-rag combos that crush BB's
defend range, plus all the overpairs JJ-AA, while BB's defend range tops
out at KQo / 77 / 22 sets). Small 25% gives BB a poor price to continue with
underpairs and Ax-no-pair, denies equity cheaply, and preserves hero's
turn-barrel flexibility. This is the canonical HU-4 dry-board small-range-c-bet
anchor: high-leverage, low-cost, range-bet inclusion of a medium overpair on
a BTN-favoured K-high dry board. Bet 25% — solver-aligned, no deviation.

---

## HU-4.2: 4h4c small underpair on monotone KhQh9h, BTN check-back vs BB

**Marker:** CANONICAL

**Target axis:** Axis HU-4 — Preflop aggressor postflop discipline
**Hero cards:** 4h/4c
**Board:** Kh Qh 9h
**Street:** Flop
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 5.5bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** Air (effectively) — small underpair to a monotone
broadway board where 44 is dominated by every Kx/Qx/9x BB continues with, by
every overpair 55-AA, and by any flush BB has flopped. The 4h gives a
worthless one-card backdoor flush blocker (essentially zero equity since BB's
flush combos are unaffected by hero's single 4h). No straight equity (4-4 has
no connectivity to K-Q-9). Set-mining equity is ~4% on the turn (one of two
fours) but BB's range crushes hero's set on most action. Classify as air with
showdown-loss-on-most-runouts; dominant feature is no realisable equity vs
BB's continuing range on this texture.

**Action history:** 100bb effective. BTN (hero) opens 2.5bb, SB folds, BB calls.
Flop Kh Qh 9h (monotone hearts, all-broadway, highly connected with one-card
straight draws via JT/JT-style and one-card flush draws via any heart). BB
checks. Hero acts.

**Solver sizing notes:** The canonical solver action class on KhQh9h
monotone vs BB defend is a high-frequency check-back from PFA, with the
remaining frequency split between a small 25% probe and a polarized 66%
that's reserved for nut-flush + nut-straight value combos. The board is
BB-favoured on monotone broadway (BB's defend range contains all the
QJ/JT/T9/A-of-hearts combos that flop made hands and nut flush draws at
high frequency relative to BTN's range), and 44 has no realisable equity
to support continuation. This is the canonical HU-4 wet-board check-back
anchor: a small underpair on a monotone broadway texture where range
advantage shifts to BB and PFA's bottom-range correctly checks at near-100%
frequency. Check — solver-aligned action class (no bet sizing required for
the check action), no deviation.

---

## HU-4.3: KsTs TPGK on Td7d5s two-tone wet, SB c-bet sizing dilemma vs BB

**Marker:** CLOSE

**Target axis:** Axis HU-4 — Preflop aggressor postflop discipline
**Hero cards:** Ks/Ts
**Board:** Td 7d 5s
**Street:** Flop
**Hero position:** SB
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 6bb
**Facing bet:** No
**Opener position:** SB
**Bettor position:** None
**Hand strength composition:** TP+ (top pair good kicker — top pair of tens
with K-kicker on a T-high two-tone diamond board; hero's Ks/Ts are spades,
contributing a backdoor spade-flush draw via the 5s on board (3 spades
total, needs runner-runner spades for flush) and zero diamonds, so BB's
nut-FD combos are unblocked by hero. Vulnerable TP+ — board has direct
straight equity for BB (8x/9x OESD via any 6 or 9 / one-card straights via
86/96 holdings) and direct flush draw equity for BB's diamond holdings;
hero's K-kicker dominates Tx-worse top pair (TJ / T9 / T8) but loses to
AT / KK+ overpairs / sets / two-pair).

**Action history:** 100bb effective. SB (hero) opens 3bb (SB open size larger
than BTN open per standard solver outputs), BB calls. Flop Td 7d 5s (two-tone
diamonds, T-high, mid-low connected with OESD and flush-draw equity for BB).
BB checks. Hero acts.

**CLOSE rationale:** Three-action genuine entropy across the sizing-frequency
dimension. The decision splits between (a) bet 25% pot as a small range
c-bet that protects hero's range structure and gives BB a poor immediate
price on draws while keeping the pot small for OOP play on later streets,
(b) bet 66% pot as a polarized sizing that charges BB's draw-heavy continuing
range a fair price + extracts thin value from worse Tx and 7x/5x pairs +
denies free turn equity to BB's two-overcard hands, and (c) check-back to
control pot size OOP and pocket showdown equity vs BB's draw-heavy range
that would semi-bluff-raise a small c-bet. v9-3way-on-59 model uncertainty
is elevated because (i) SB-open vs BB-defend on T-high two-tone is a
range-vs-range texture where SB's range advantage is real but smaller than
BTN's, narrowing the optimal sizing band; (ii) the OESD + FD double-draw
texture penalises small sizings (BB realises equity cheaply) and penalises
large sizings (hero gets check-raised by combo draws + sets and folds out
the worst Tx); (iii) the OOP position adds a SPR-management dimension —
betting commits hero to barrel decisions on bricked turns and check-raise
defence with TPGK, while checking concedes initiative on a board where BB
will probe-bet the turn aggressively. Predictive entropy across the
25% / 66% / check action triple is high because no single action dominates
the others across plausible BB range models.

**Solver sizing notes:** Flop bet sizes 25% and 66% are solver-aligned.
Hero's three-action candidate set covers the live solver mix on this spot
— no deviation.

---

## HU-4.4: QhJh combo draw on 9h8h2c two-tone wet, SB polar 66% vs 25% vs check vs BB

**Marker:** CLOSE

**Target axis:** Axis HU-4 — Preflop aggressor postflop discipline
**Hero cards:** Qh/Jh
**Board:** 9h 8h 2c
**Street:** Flop
**Hero position:** SB
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 6bb
**Facing bet:** No
**Opener position:** SB
**Bettor position:** None
**Hand strength composition:** Draws — combo draw of two overcards (Q and J,
each give 3 outs that pair hero ahead of the 9-high board's pair-equity
range, ~6 noisy overcard outs) + nut-heart flush draw (9 outs to the
second-nut or near-nut flush — A-of-hearts dominates hero, but hero's QhJh
blocks BB's KhQh / KhJh / QhTh / JhTh nut-flush-draw combos modestly) +
gutshot to the ten-high straight via any T (4 outs, 3 clean of the hearts
already counted). Net ~16 outs on the turn raw, ~46% direct equity vs
typical BB defend continuing range; classify as draws (combo) with no
made-pair component at decision time.

**Action history:** 100bb effective. SB (hero) opens 3bb, BB calls. Flop
9h 8h 2c (two-tone hearts, 9-high, low-end connected with OESD and FD
texture). BB checks. Hero acts.

**CLOSE rationale:** Three-action genuine entropy across the sizing-frequency
dimension. The decision splits between (a) bet 25% pot as a small range
c-bet that protects hero's wide SB-open range, prices BB poorly on
underpair / weak-draw continues, and keeps the pot small OOP, (b) bet 66%
pot as a polarized semi-bluff that leverages hero's ~46% equity to charge
BB's continuing range a fair price + applies maximum fold equity against
BB's two-overcard / weak-pair holdings + sets up a credible turn barrel
on heart / straight-completing runouts, and (c) check-back to disguise
hero's combo-draw and induce BB to bluff or thinly value-bet the turn
into hero's check-call range with a draw plus showdown equity. v9-3way-on-59
model uncertainty is elevated because (i) the 9h8h2c texture is one of the
classic wet-board sizing-mix spots where solvers split the PFA c-bet across
small / large / check at non-trivial frequencies for many holdings;
(ii) hero's combo-draw composition is at the top of the draw bucket, where
the marginal EV of bet vs check is small in either direction (high equity
permits both check-and-realise and bet-and-leverage); (iii) the OOP
position complicates the check-back line because BB will probe-bet the
turn, forcing hero to play a check-call-or-check-raise decision with a
draw that may have completed (heart turn) or missed (brick turn), and the
EV of that branch trades off against the immediate-value branch of betting
the flop. Predictive entropy across the 25% / 66% / check action triple is
high because the optimal solver action mixes across all three at meaningful
frequencies depending on the precise BB range model.

**Solver sizing notes:** Flop bet sizes 25% and 66% are solver-aligned.
Hero's three-action candidate set covers the live solver mix on this spot
— no deviation.

---

## HU-4.5: AhJc two-overcard backdoor air, BTN delayed c-bet sizing on Tc7c3s-5d turn vs BB

**Marker:** CLOSE

**Target axis:** Axis HU-4 — Preflop aggressor postflop discipline
**Hero cards:** Ah/Jc
**Board:** Tc 7c 3s 5d
**Street:** Turn
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 5.5bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** Air with two overcards + backdoor equity — no
made pair (A-J against T-7-3-5, all four board cards below both hero cards),
no flush draw (hero's Ah is the only heart in hero's hand and zero hearts
on board, so hero has zero hearts-FD; hero's Jc gives a backdoor club draw
with the Tc/7c on board for 3 clubs total — needs runner-runner clubs for
flush, ~4% backdoor-FD equity), no direct straight draw (A-J needs running
KQ for broadway; J-7-5 gap leaves no direct gutshot for the J either).
Two clean overcards (A and J each give 3 outs that pair hero ahead of the
T-high board's continuing-range pair-equity, ~6 noisy overcard outs on the
river) + the ace-blocker effect on BB's Ax holdings (A-T two-pair, A-T-pair
floats) + the J-blocker on BB's JT / J-x pair-equity holdings. Classify as
air with two-overcard + backdoor (subordinate); dominant feature is no made
hand, no direct draw on the turn.

**Action history:** 100bb effective. BTN (hero) opens 2.5bb, SB folds, BB
calls. Flop Tc 7c 3s (two-tone clubs, T-high, mid-low disconnected). BB
checks, BTN checks back (range-balance check-back with two-overcard air
that prefers to realise overcard showdown equity rather than c-bet into
BB's two-tone-club continuing range that contains all the FD + Tx
floats). Turn 5d (brick — does not complete any flush, does not complete
any direct straight, brings a third suit but no flush draw for hero,
brings a 6-4 / 6-7 / 4-3 backdoor-straight discount for BB's
small-connector range that check-called the flop). BB checks. Hero acts
on a checked-to turn with one street remaining.

**CLOSE rationale:** Three-action genuine entropy across the sizing-frequency
dimension on a delayed-c-bet line. The decision splits between (a) check
back again to preserve overcard showdown equity vs BB's check-check-down
range and avoid being check-raised off the hand, (b) bet 33% pot as a
small delayed c-bet / probe that targets BB's medium-pair fold range
(small pocket pairs that check-called flop and check-fold turn, busted
backdoor draws) plus the missed-FD frequency, and (c) bet 75% pot as a
polarized stab that leverages the A and J overcard-blockers against BB's
two-pair-Tx value range while folding out 7x weak-kicker holdings that
would have gone to showdown. v9-3way-on-59 model uncertainty is elevated
because (i) the delayed-c-bet line on Tc7c3s checked-flop into a 5d brick
turn is a low-frequency spot in solver outputs and therefore underweighted
in training distributions, (ii) the A-J overcard-blocker effect cuts both
directions on BB's range — A blocks AT two-pair value while J blocks JT
top-pair-good-kicker float-call, leaving the net blocker effect ambiguous,
and (iii) the implied-odds value of free-river-card with two clean
overcards trades off against the immediate-fold-equity value of a delayed
stab on a turn where BB's range is condensed to weak-pair / busted-FD /
trap-Tx after the flop check-check. Predictive entropy across the
check-back / 33% / 75% action triple is high because no single action
dominates across plausible BB check-flop-and-check-turn range models.

**Solver sizing notes:** Turn check-back, 33%, and 75% are all solver-aligned.
Hero's three-action candidate set covers the live solver mix on this spot
— no deviation.

---
