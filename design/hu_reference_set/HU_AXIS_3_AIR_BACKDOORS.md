# HU Axis 3 — Air with Backdoors (HU-3.1 to HU-3.5)

**Date:** 2026-05-10
**Status:** Design only — no labelling, no corpus changes
**Context:** Phase 1.5-D.1 HU reference set — 1 of 6 axis breakouts (per design memo §4.2)

## Axis intro

Axis HU-3 targets heads-up postflop spots where hero holds **air**: no made
pair, no direct strong draw (no flush draw, no open-ended straight draw, no
combo draw). The dominant composition feature is "no made hand, no strong
direct draw"; some hands carry secondary backdoor pair-equity, a single
overcard, or a 3-card backdoor straight draw, but those are subordinate
features that do not promote the spot out of the air bucket. The decision
class under test is **float vs check-fold vs c-bet bluff**: when does hero
turn pure-air-with-backdoors into an aggressive line (range-c-bet, delayed
c-bet, float-and-stab), when does the spot collapse to give-up / check-fold,
and how do board texture, position, and villain range cap mediate the choice.

Across the 5 hands the axis varies position (IP c-bet vs OOP float decisions),
street (flop range-c-bet, turn float continuation, river give-up bluff
threshold), board texture (dry A-high / paired / connected mid / broadway-heavy),
and villain range cap (capped BB defend vs uncapped BTN open). The composition
triple is **air** (with subcategory pure-air / one-overcard / backdoor-straight /
backdoor-flush) per `feedback_preflop_geometry_vs_postflop_composition.md`; no
spot in this axis relies on TP+ value or direct flush/straight-draw equity at
the moment of decision. Bet sizes are solver-aligned per
`feedback_solver_aligned_sizing.md` (flop 25%/66%, turn 33%/75%, river
33%/75%/150%); deviations are documented inline. 3 hands are CLOSE
(model-uncertainty + poker-difficulty driven per `feedback_close_hand_selection.md`);
2 hands are CANONICAL (uncontroversial high-leverage c-bet bluff or
clear check-fold anchors). All 5 hands are heads-up (`num_opponents: 1`).

Cross-axis hygiene: hero hands and flop boards do not collide with HU-1
(AhKs, 9d9c, KhQd, TsTd, AhJh; flops Ad8c3h, 9h7s2c, KcTc6d, 8h5c2d, Jc9c5d)
or HU-2 (AhQh, Td9d, Js9s, 6c5c, Ad5d; flops Kd7h4h, 8s6c2d, Qs7s3d, 8c7d4h,
Jh8d3c).

---

## Hand index

| ID | Marker | Street | Hero pos | Hand | Board | Decision class |
|----|--------|--------|----------|------|-------|----------------|
| HU-3.1 | CANONICAL | Flop | BTN | 7c6h | Ah Kd 4s | Range-c-bet bluff on dry A-high BTN-favoured board |
| HU-3.2 | CANONICAL | Flop | BB | 4d3d | Qc Jh 9s | Clear check-fold OOP on connected broadway flop |
| HU-3.3 | CLOSE | Turn | BTN | KsQs | 8h 6h 5c 2d | Two-overcard air, checked-to turn float vs stab |
| HU-3.4 | CLOSE | Flop | BB | Ts8h | 7d 7c 3h | Backdoor-straight + one overcard, OOP check-raise bluff vs check-call |
| HU-3.5 | CLOSE | River | BTN | Ac4c | Kh 9d 6s 5h 2c | Busted-air give-up vs polarised river bluff with A-blocker |

---

## HU-3.1: 7c6h pure air on AhKd4s, BTN range-c-bet bluff vs BB

**Marker:** CANONICAL

**Target axis:** Axis HU-3 — Air with backdoors
**Hero cards:** 7c/6h
**Board:** Ah Kd 4s
**Street:** Flop
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 5.5bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** Air — no made pair, no flush draw, no straight
draw. Backdoor straight contribution is essentially zero on AhKd4s (7-6
needs running 5-3, 5-8, or 8-5 to make a straight; the A-K gap blocks any
useful 3-card BDSD that interacts with hero's 7-6); backdoor flush
contribution is zero (hero's two cards are different suits and neither
matches a board suit beyond a single coincidental match — clubs absent on
flop, hearts and diamonds and spades each one-on-board with hero holding
6h and the board hearts is Ah, so hero has at best a 2-card backdoor
hearts contribution that is dominated by villain Ax-of-hearts holdings).
Pure air with no meaningful equity.

**Action history:** 100bb effective. BTN (hero) opens 2.5bb, SB folds, BB
calls. Flop Ah Kd 4s (rainbow, two broadways, disconnected, BTN
range-favoured top-of-board texture). BB checks. Hero acts.

**Solver sizing notes:** The canonical solver action class on AhKd4r vs BB
defend is a high-frequency 25% pot range-c-bet (solver-aligned flop small
size); hero's air with no backdoor equity is a natural inclusion in the
range-bet block because the texture's range-vs-range equity advantage
sits with BTN and the small size denies equity to BB's underpair / weak
broadway holdings cheaply while preserving give-up flexibility on bad
turns. This is the canonical HU-3 c-bet-bluff anchor: high-leverage,
low-cost, range-bet inclusion of pure-air-with-no-backdoors on a
BTN-favoured A-high dry board. Bet 25% — solver-aligned, no deviation.

---

## HU-3.2: 4d3d air OOP on QJ9 connected broadway, BB faces 66% c-bet — clear check-fold

**Marker:** CANONICAL

**Target axis:** Axis HU-3 — Air with backdoors
**Hero cards:** 4d/3d
**Board:** Qc Jh 9s
**Street:** Flop
**Hero position:** BB
**Primary villain position:** BTN
**Num opponents:** 1
**Pot:** 5.5bb
**Facing bet:** Yes
**To call:** 3.6bb
**Pot odds required:** 28.6%
**Opener position:** BTN
**Bettor position:** BTN
**Hand strength composition:** Air — no made pair (4-3 against Q-J-9), no
direct draw, no overcards (both hero cards are below all three board cards),
no flush draw (board rainbow). Backdoor diamond flush contribution requires
running diamond-diamond on a board with one diamond (Qc Jh 9s — actually
zero diamonds on flop; hero's both diamonds need three more diamonds to
make a flush, which is a 3-card backdoor that is cosmetically negligible
and the board has zero diamonds so the BDFD requires runner-runner-runner
not runner-runner). Backdoor straight contribution requires running 5-6,
6-5, 2-5, 5-2, A-5, or 5-A — all blocked or negligible against the 9-J-Q
board's straight structure. Pure air, no realisable equity.

**Action history:** 100bb effective. BTN opens 2.5bb, SB folds, BB (hero)
defends call (4-3-suited is in BB's wide-defend range vs BTN open at
100bb effective by typical solver outputs; the defend is borderline but
included). Flop Qc Jh 9s (rainbow, all-broadway-and-9, highly connected,
range-favours BTN's open range with all the AT/KT/T8/T-stuff plus QJ/QT/JT
two-pair combos). BB checks. BTN bets 3.6bb (66% pot — solver-aligned
flop large c-bet on a connected broadway board where IP wants to deny
BB's defend-range equity decisively). Hero faces decision with 28.6%
pot odds required.

**Solver sizing notes:** This is the canonical HU-3 check-fold anchor:
hero has no equity (pure air, no backdoor equity worth speaking of),
hero faces a large c-bet that requires 28.6% equity to continue, hero is
OOP with no implied-odds story. The solver-aligned action is fold at
near-100% frequency; the spot serves as a ground-truth low-variance
anchor for inter-labeller agreement. Bet 66% — solver-aligned, no
deviation.

---

## HU-3.3: KsQs two-overcard air on 865-2 turn, BTN checked-to after flop check-back

**Marker:** CLOSE

**Target axis:** Axis HU-3 — Air with backdoors
**Hero cards:** Ks/Qs
**Board:** 8h 6h 5c 2d
**Street:** Turn
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 5.5bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** Air with two overcards — no made pair (K-Q
against 8-6-5-2), no flush draw (board has hearts on 8h 6h, hero holds
spades — hero blocks one heart only via Ks-of-spades irrelevantly),
no straight draw (K-Q has no connectivity to 8-6-5-2 — no gutshot, no
backdoor straight worth noting since the gap is 3 ranks). Backdoor
contribution: hero's two spades plus 0 spades on board provides no spade
backdoor flush. Two clean overcards (K and Q each give 3 outs that pair
hero ahead of the 8-high board's pair-equity range), but those outs are
not "draws" in the composition-triple sense; they are subordinate
overcard equity totalling ~12% direct equity vs villain's continuing
range. Classify as air with overcard-equity (subordinate); dominant
feature is no made hand, no direct draw.

**Action history:** 100bb effective. BTN (hero) opens 2.5bb, SB folds, BB
calls. Flop 8h 6h 5c (two-tone hearts, low, connected — straight-draw and
flush-draw heavy texture that range-favours BB's defend range
narrowly). BB checks, BTN checks back (range-balance check-back with
overcards-no-equity hands like K-high and Q-high that prefer to realise
equity passively rather than c-bet into BB's draw-heavy continuing range
on a BB-favoured low-connected texture). Turn 2d (brick, no flush
completes, no straight completes, no overcard pairs). BB checks. Hero
faces a checked-to turn with two streets remaining.

**CLOSE rationale:** Three-action genuine entropy. The decision splits
between (a) check-back-again to give up the pot and realise overcard
showdown equity for free, (b) bet 33% pot as a delayed c-bet / probe
that targets BB's medium-pair fold range (66/77 underpairs that
check-call flop and check-fold turn) plus the missed-draw frequency,
and (c) bet 75% pot as a polarised stab that leverages the K-Q
overcard-blockers against BB's second-pair value while folding out
8x weak-kicker holdings that would have gone to showdown. Predictive
entropy is high because the decision pivots on (i) modelled BB
check-check passive-line composition on this turn (heavy in
weak-pair / busted-FD or heavy in trapping two-pair), (ii) the
implied-odds value of free-river-card with two clean overcards vs
the immediate fold-equity value of a delayed stab, and (iii) the
overcard-blocker effect (K-Q blocks AK/AQ/KQ that BB might check-call
flop, but those combos are low-frequency in BB's defend range to start
with). v9-3way-on-59 model uncertainty is elevated here because the
spot sits at the boundary between "give up with showdown equity" and
"barrel as a delayed c-bet" with no clean dominant action.

**Solver sizing notes:** Turn check-back, 33%, and 75% all solver-aligned.
Hero's three-action candidate set covers the live solver mix on this
spot — no deviation.

---

## HU-3.4: Ts8h one-overcard backdoor-straight on 773 paired, BB check-raise bluff vs check-call vs check-fold

**Marker:** CLOSE

**Target axis:** Axis HU-3 — Air with backdoors
**Hero cards:** Ts/8h
**Board:** 7d 7c 3h
**Street:** Flop
**Hero position:** BB
**Primary villain position:** BTN
**Num opponents:** 1
**Pot:** 5.5bb
**Facing bet:** Yes
**To call:** 1.4bb
**Pot odds required:** 20.4%
**Opener position:** BTN
**Bettor position:** BTN
**Hand strength composition:** Air with one overcard + backdoor straight
draw — no made pair (T-8 against 7-7-3 paired board), no flush draw
(rainbow board, hero unsuited to anything relevant), no direct straight
draw on the flop (T-8 needs 9 plus 6 to make 10-9-8-7-6, or 9 plus J to
make J-T-9-8-7 — both are 2-card backdoor straight draws not direct
draws). One overcard (the T is over the unpaired 3 and over the 7s;
ranks above all unpaired board cards). Backdoor straight: any 9 plus
any 6 makes a straight, any 9 plus any J makes a straight (3-card BDSD
in two directions, ~6% additional equity over pure air). Classify as
air with one-overcard + backdoor-straight (subordinate); dominant
feature is no made pair, no direct draw.

**Action history:** 100bb effective. BTN opens 2.5bb, SB folds, BB (hero)
defends call. Flop 7d 7c 3h (paired low board, rainbow, range-favours
BTN's open range with all the overpairs and broadway air that range-bets
small here). BB checks. BTN bets 1.4bb (25% pot — solver-aligned flop
small range-c-bet; small size on paired boards is the canonical IP
range-bet sizing because BTN range advantage is wide and the paired
texture supports near-universal continuation). Hero faces decision with
20.4% pot odds required.

**CLOSE rationale:** Three-action genuine entropy. The decision splits
between (a) check-fold (no made pair, no direct draw, only 6% backdoor
equity), (b) check-call to float with the T-overcard + backdoor-straight
equity and look for a turn that improves equity or a turn check that
permits a stab, and (c) check-raise as a polarised bluff that leverages
the paired-board texture (BTN's 25% range-bet has a high
proportion of give-up overcards that fold to a check-raise) plus the
T-blocker on BTN's overpair-of-tens combos. Predictive entropy is
high because the decision pivots on (i) the implied-odds value of
backdoor straight + one-overcard equity vs a small price (20.4% pot
odds) — minimum-defence-frequency calculation says BB must defend
~80% of range vs a 25% c-bet, so even very weak holdings need to find
defends, (ii) the check-raise EV against BTN's range-c-bet that is
weighted toward overcards-with-no-equity which fold easily, vs the
check-raise's vulnerability to BTN's overpair-and-trips slowplays
that re-raise or call dominated, and (iii) the next-street plan if
calling — does hero check-call again on a brick turn or check-fold,
and how does that branch under a delayed-stab villain model. v9-3way-on-59
model uncertainty is elevated because the action mix is genuinely
three-way (fold / call / check-raise) with each carrying a meaningful
solver frequency on paired-low textures vs small range-bets.

**Solver sizing notes:** Flop bet 25% (solver-aligned small size). Hero's
candidate set (check-fold vs check-call vs check-raise) uses
solver-aligned check-raise sizing of ~3.5x the bet (~5bb total) if
raising — no deviation.

---

## HU-3.5: Ac4c busted-air, BTN faces BB river block-bet on K965-2, give-up bluff with A-blocker

**Marker:** CLOSE

**Target axis:** Axis HU-3 — Air with backdoors
**Hero cards:** Ac/4c
**Board:** Kh 9d 6s 5h 2c
**Street:** River
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 12bb
**Facing bet:** Yes
**To call:** 4bb
**Pot odds required:** 25.0%
**Opener position:** BTN
**Bettor position:** BB
**Hand strength composition:** Air — no made pair (A-4 against K-9-6-5-2,
hero's A is the only overcard and does not pair on river), no straight
(needs 3-4 or 7-8 to make any straight; hero has 4 but no second card
that completes), no flush (hero's clubs Ac/4c plus board clubs 2c only
= 2 clubs total, no flush). Backdoor flush completion did not happen
(turn 5h, river 2c — not a club runout). On the river, ace-high
no-pair no-draw is pure air with one A-blocker that interacts with
villain's value range (A-blocker reduces AK/AcKc/A-x-of-clubs combos in
BB's range modestly). Classify as air with A-high blocker (subordinate);
dominant feature is no made hand, no draw, no showdown equity beyond
ace-high.

**Action history:** 100bb effective. BTN (hero) opens 2.5bb, SB folds, BB
calls. Flop Kh 9d 6s (rainbow, K-high, disconnected). BB checks, BTN
bets 1.4bb (25% pot — solver-aligned flop small range-c-bet on a
BTN-favoured K-high dry texture), BB calls. Turn 5h (brings backdoor
hearts FD for villain holdings, brings 6-5 connected straight-draw
texture for villain's 87/78 holdings, but no draw completes for hero).
BB checks, BTN checks back (range-balance check-back with A-high air
that lacks equity to barrel and prefers showdown
realisation against BB's check-call-flop range that's now condensed to
weak-Kx + medium-pair holdings). River 2c (brick, no flush completes
since clubs total only 2c on board with hero holding two clubs, no
straight completes, no broadway pair). BB leads 4bb into 12bb (33% pot
— solver-aligned river small block-lead, characteristic of BB
medium-strength holdings that want to set their own price on the river
and avoid facing a polarised IP bet). Hero faces decision with 25.0%
pot odds required.

**CLOSE rationale:** Three-action genuine entropy. The decision splits
between (a) fold (give up the A-high air with no showdown value vs BB's
medium-strength block-lead range), (b) call as a thin bluff-catch (BB's
33% river block-lead range carries some bluff frequency from busted
backdoor draws and overcard-air give-ups, plus weak-Kx and medium-pair
value that hero's A-high can occasionally beat at showdown when BB's
range includes 99-blocker-heavy thin-value bets that hero loses to
deterministically), and (c) raise as a leverage bluff that exploits
the A-blocker effect on BB's two-pair-plus value range and the
small-bet-set-up that block-leads create vulnerability to. Predictive
entropy is high because the decision pivots on (i) modelled BB river
block-lead composition (heavy in medium-pair value vs heavy in
weak-Kx vs heavy in bluff-give-up) on K965-2 specifically given the
flop-bet-call-turn-check-check-river-lead line, (ii) the A-blocker's
combinatoric effect on BB's AK / AcKc / A-x-of-clubs holdings — the
A-blocker reduces both villain value (AK two-pair) and villain bluff
(A-high give-ups) in offsetting fashion, with the net pointing toward
slight call-EV improvement, and (iii) the raise-as-bluff option that
leverages BB's small block-lead's structural vulnerability to a
large raise but which requires hero's range to contain enough credible
value combos to balance. v9-3way-on-59 model uncertainty is elevated
because the spot sits at a three-way action boundary on a river with
a non-canonical lead-into-IP line that is rare in solver outputs and
therefore underweighted in training distributions.

**Solver sizing notes:** Flop 25%, river block-lead 33% — both
solver-aligned. Hero's candidate set (fold vs call vs raise) uses
solver-aligned river raise sizing if raising (~3x lead = 12bb total
raise, polarised raise sizing on a river block-lead) — no deviation.

---
