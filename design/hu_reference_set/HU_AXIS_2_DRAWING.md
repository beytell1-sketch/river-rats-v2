# HU Axis 2 — Drawing Hand Profitability (HU-2.1 to HU-2.5)

**Date:** 2026-05-10
**Status:** Design only — no labelling, no corpus changes
**Context:** Phase 1.5-D.1 HU reference set — 1 of 6 axis breakouts (per design memo §4.2)

## Axis intro

Axis HU-2 targets heads-up postflop spots where hero holds a drawing hand
(flush draw, straight draw, or combo draw) with no made-pair value at the
moment of decision. The decision class under test is **semi-bluff aggression
versus check-call discipline**: when does a draw bet/raise to apply fold
equity + realize equity via fold, when does it check-call to realize equity
passively at the right price, and when does pot odds + implied odds make the
call (or fold) automatic. The composition triple is **draws** (with subcategory
flush draw / open-ended straight draw / combo draw / gutshot+backdoor) per
`feedback_preflop_geometry_vs_postflop_composition.md`; no spot in this axis
relies on TP+ value or pure-air bluff equity.

Across the 5 hands the axis varies pot odds (cheap call, marginal call,
borderline fold), SPR (shallow / standard / deep), position (IP semi-bluff
vs OOP check-call), and nut-potential (nut FD vs middling FD vs OESD that
makes the dummy end). Bet sizes are solver-aligned per
`feedback_solver_aligned_sizing.md` (flop 25%/66%, turn 33%/75%, river
33%/75%/150%); deviations are documented inline. 3 hands are CLOSE
(model-uncertainty + poker-difficulty driven per `feedback_close_hand_selection.md`);
2 hands are CANONICAL (uncontroversial semi-bluff or pot-odds-call anchors).
All 5 hands are heads-up (`num_opponents: 1`).

Cross-axis hygiene: hero hands and flop boards do not collide with HU-1
(AhKs, 9d9c, KhQd, TsTd, AhJh; flops Ad8c3h, 9h7s2c, KcTc6d, 8h5c2d,
Jc9c5d).

---

## Hand index

| ID | Marker | Street | Hero pos | Hand | Board | Decision class |
|----|--------|--------|----------|------|-------|----------------|
| HU-2.1 | CANONICAL | Flop | BTN | AhQh | Kd 7h 4h | Nut FD + overcards, IP semi-bluff bet |
| HU-2.2 | CANONICAL | Flop | BB | Td9d | 8s 6c 2d | OESD facing 66% c-bet, pot-odds call |
| HU-2.3 | CLOSE | Turn | BB | Js9s | Qs 7s 3d 2c | Bare nut FD OOP facing turn 75% barrel |
| HU-2.4 | CLOSE | Flop | BTN | 6c5c | 8c 7d 4h | Combo draw IP facing OOP check-raise |
| HU-2.5 | CLOSE | Turn | BTN | Ad5d | Jh 8d 3c 2d | Gutshot + backdoor-turned-FD, checked-to IP |

---

## HU-2.1: AhQh nut flush draw + two overcards on K74-two-tone, BTN c-bet semi-bluff vs BB

**Marker:** CANONICAL

**Target axis:** Axis HU-2 — Drawing hand profitability
**Hero cards:** Ah/Qh
**Board:** Kd 7h 4h
**Street:** Flop
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 5.5bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** Draws — nut flush draw (9 outs to the nut flush
via any heart) + two clean overcards (A and Q each give 3 outs that beat Kx);
~15 outs raw, ~25 clean equity vs Kx-heavy continuing range; no made-pair
component.

**Action history:** 100bb effective. BTN (hero) opens 2.5bb, SB folds, BB
calls. Flop Kd 7h 4h (two-tone hearts, K-high, disconnected). BB checks. Hero
acts.

---

## HU-2.2: Td9d open-ender on 862r BB defends, faces 66% c-bet — pot-odds call

**Marker:** CANONICAL

**Target axis:** Axis HU-2 — Drawing hand profitability
**Hero cards:** Td/9d
**Board:** 8s 6c 2d
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
**Hand strength composition:** Draws — open-ended straight draw (8 outs: any
5 or any 7 makes the straight) + backdoor diamond runner-runner flush
contribution (~3% additional equity) + two overcards that play dirty
against any 8x continuing range (T and 9 are not clean outs vs Tx/9x in
BTN's range). Net ~8 clean OESD outs on the turn; ~31-34% raw equity vs
88+/8x/77/22 continuing range plus overpairs.

**Action history:** 100bb effective. BTN opens 2.5bb, SB folds, BB (hero)
defends call. Flop 8s 6c 2d (rainbow, low, disconnected aside from 8-6 gap
that the OESD spans). BB checks. BTN bets 3.6bb (66% pot — solver-aligned
flop large c-bet on a low rainbow board where IP wants high equity-realisation
denial against BB's wide defend range). Hero faces decision with 28.6% pot
odds required.

---

## HU-2.3: Js9s bare nut spade flush draw OOP, facing BTN turn 75% barrel on Q73-2

**Marker:** CLOSE

**Target axis:** Axis HU-2 — Drawing hand profitability
**Hero cards:** Js/9s
**Board:** Qs 7s 3d 2c
**Street:** Turn
**Hero position:** BB
**Primary villain position:** BTN
**Num opponents:** 1
**Pot:** 11bb
**Facing bet:** Yes
**To call:** 8.25bb
**Pot odds required:** 30.0%
**Opener position:** BTN
**Bettor position:** BTN
**Hand strength composition:** Draws — bare flush draw to the nut spade
flush (9 outs to any spade gives nut or near-nut flush since hero holds Js
as the second-highest spade behind any Ax-of-spades villain holding) + 1
gutshot to the wheel via any T (4 outs, 3 clean of the spades already
counted) — total ~12 outs raw, ~22% direct equity vs polarised barrel
range, with implied odds modest given OOP position and one card to come.
No made pair, no overcard outs that beat villain's value range.

**Action history:** 100bb effective. BTN opens 2.5bb, SB folds, BB (hero)
defends call. Flop Qs 7s 3d (two-tone spades, Q-high, disconnected). BB
checks, BTN bets 1.4bb (25% pot — solver-aligned flop small c-bet,
range-bet sizing on a board that favours BTN's range), BB calls. Turn 2c
(brick, no flush completes, no straight completes). BB checks. BTN bets
8.25bb (75% pot — solver-aligned turn large barrel, polarised between
Qx-for-value and FD-blockers / overpair-fold-equity bluffs). Hero faces
decision with 30.0% pot odds required.

**CLOSE rationale:** Three-action genuine entropy at the canonical
FD-vs-large-barrel threshold. The decision splits between (a) fold —
direct pot odds (30%) exceed direct equity (~22% on a one-card draw with
one card to come), so without implied odds the call is -EV; (b) call to
realise the FD equity if implied odds on the river clear the gap (hero
hits the spade flush and extracts on river, plus the rare wheel-T
straight from the gutshot); and (c) check-raise as a leverage / fold-equity
semi-bluff with the nut-FD blocker against BTN's polarised barrel range.
v9-3way-on-59 model uncertainty is elevated because (i) modelled BTN
bluff frequency on Q73-2 turn-brick varies meaningfully between
value-heavy (sets, two-pair Q7, overpair JJ+) and bluff-heavy (KJ/KT/AJ-
no-spade air with overcard equity) range models, and the call/fold
threshold pivots on small shifts in this frequency; (ii) implied-odds
estimation is OOP-degraded (hero acts first on the river, can be
checked back when hero misses and bet again when hero hits a scare card),
and the discount factor for OOP draws against a polarised range is not
cleanly captured in the v9-3way-on-59 training distribution; (iii) the
check-raise option leverages the nut-FD blocker effect in a way that the
v9-3way-on-59 model has limited training signal for at this exact
turn-barrel-facing-OOP-draw spot, leaving a third low-probability action
class live in solver outputs. Predictive entropy across the fold / call /
check-raise action triple is high because no single action dominates
across plausible BTN turn-barrel range models.

**Solver sizing notes:** Flop 25%, turn 75% — both solver-aligned. Hero's
candidate response set (call vs fold vs check-raise) uses standard
solver-aligned raise sizing if raising — no deviation.

---

## HU-2.4: 6c5c combo draw IP, BTN c-bets, BB check-raises — call vs jam vs fold

**Marker:** CLOSE

**Target axis:** Axis HU-2 — Drawing hand profitability
**Hero cards:** 6c/5c
**Board:** 8c 7d 4h
**Street:** Flop
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 14.85bb
**Facing bet:** Yes
**To call:** 9.9bb
**Pot odds required:** 28.6%
**Opener position:** BTN
**Bettor position:** BB
**Hand strength composition:** Draws — combo draw: open-ended straight draw
(8 outs — any 9 makes 9-8-7-6-5; any 4 makes 8-7-6-5-4, but a 4 pairs the
board, so the 4 outs are 4-pair-board straights with reverse-implied-odds
risk vs full houses; the 4 nines are clean) + backdoor club flush draw
(needs club-club runout, ~4% additional equity) + a pair-of-fives or
pair-of-sixes pickup on the turn that adds showdown equity but does not
beat villain's check-raise range. Net ~8 OESD outs (4 clean nines + 4
board-pairing fours) on the turn; ~32-36% raw equity vs typical BB
check-raise range
(two-pair 87/84/74, sets 88/77/44, overpairs 99-AA, plus combo-draw
semi-bluffs 65/96/T9/etc). No made-pair component at decision time.

**Action history:** 60bb effective (short-stack HU dynamic to keep SPR
relevant for the jam-or-call decision). BTN (hero) opens 2.5bb, SB folds,
BB calls. Flop 8c 7d 4h (rainbow, mid, OESD-heavy, multi-way-style
texture). BB checks. BTN bets 3.63bb (66% pot — solver-aligned flop large
c-bet on a connected mid board where BTN range advantage is limited and
the larger size targets BB's weak Bx range plus draws). BB check-raises
to 9.9bb (~3x raise of the 3.63bb bet, solver-aligned check-raise
sizing). Hero faces 9.9bb to call into a 14.85bb pot. Pot odds 28.6%.

**CLOSE rationale:** Three-action genuine entropy across fold / call / jam.
The decision splits between (a) fold — forfeits ~32-36% raw equity above
the 28.6% pot odds, but BB's check-raise range is condensed to value-heavy
(two-pair+, sets, occasional overpair) where hero's straight outs can
still leave hero second-best on made-straight runouts; (b) call — realises
equity but commits hero on most turns at 60bb effective with SPR ~1.3
after the call; (c) jam as a semi-bluff — leverages hero's combo-draw
equity + fold equity against BB's bluff check-raises and overpair
give-ups, and dodges reverse-implied-odds scenarios. v9-3way-on-59 model
uncertainty is elevated because (i) modelled BB check-raise bluff
frequency at 60bb varies meaningfully across range models — looser
check-raise models support call/jam EV and tighter check-raise models
support fold EV, and the optimum sits at a knife-edge; (ii) the
straight-vs-better-straight reverse-implied-odds penalty on 8c7d4h
specifically (87 makes a higher straight on a 6 if BB has 87; 44/77/88
fill on the same cards that complete hero's draw on some runouts) is a
texture-specific blocker effect that the v9-3way-on-59 model has not seen
densely; (iii) the SPR-driven jam-now-or-jam-later choice that the short
stack forces creates a commit-EV trade-off where solver mixes between
flat-call and jam at varying frequencies based on the exact BB range model.
Predictive entropy across the fold / call / jam action triple is high
because no single action dominates across plausible BB check-raise range
models.

**Solver sizing notes:** Flop bet 66% (solver-aligned large size). BB's
check-raise to ~3x is solver-aligned. Hero's response set (call vs jam
vs fold) uses jam sizing constrained by remaining stack at 60bb effective
— deviation justified: with SPR ~1.3 after call, raise-to-non-jam is
not a meaningful option, so the response simplifies to call/jam/fold.

---

## HU-2.5: Ad5d gutshot + turned diamond FD IP, checked-to on J83-2 vs OOP villain

**Marker:** CLOSE

**Target axis:** Axis HU-2 — Drawing hand profitability
**Hero cards:** Ad/5d
**Board:** Jh 8d 3c 2d
**Street:** Turn
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 5.5bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** Draws — turned nut-diamond flush draw (9
outs to the nut flush via any diamond) + gutshot to the wheel via any 4
(4 outs, 3 clean of the diamonds already counted) + ace-overcard equity
of marginal value against BB's range (3 outs that pair the ace, but
top-pair-no-kicker on a J83-2 board is not a clean win); ~12 clean draw
outs on the river plus ~3 noisy A-pair outs. No made pair at decision
time; classify as draws with backdoor pair-equity (subordinate).

**Action history:** 100bb effective. BTN (hero) opens 2.5bb, SB folds, BB
calls. Flop Jh 8d 3c (rainbow, J-high, disconnected). BB checks, BTN
checks back (range-balance check-back for backdoor draws + showdown
hands). Turn 2d (completes hero's turned diamond FD; brings backdoor
diamond runout but no flush yet; brings a wheel gutshot to hero via any
4). BB checks. Hero acts on a checked-to turn with two streets remaining.

**CLOSE rationale:** Three-action genuine entropy across check-back /
33% bet / 75% overbet on a checked-to turn after a flop check-back.
Hero's range is uncapped after the flop check-back (hero may have pocket
pairs, weak Jx checked back for showdown, and the exact draws hero now
holds), and BB's range is uncapped on the check-check flop response
(BB may have weak Jx or Tx pair-equity that declined to lead). The
decision splits between (a) check-back to realise equity for free with
the option to bet a river hit, (b) bet 33% pot as a semi-bluff to deny
equity to BB's two-overcard hands and underpairs while retaining fold
equity from the draw outs and the A-blocker, and (c) overbet 75% pot
to leverage the A-blocker as polarised semi-bluff. v9-3way-on-59 model
uncertainty is elevated because (i) modelled BB check-check-check
willingness with weak Jx versus check-call with a Tx underpair varies
meaningfully across range models, and the optimal hero action depends
on which model BB carries; (ii) the implied-odds value of checking-back
to make a disguised river FD-hit trades against the immediate fold-equity
value of betting now to fold out weaker overcard hands that would float
a small bet, and the EV difference is small in either direction; (iii)
the A-blocker effect on BB's check-call-bet-river-fold range against an
A-high turn shove is a non-trivial polarising signal that the v9-3way-on-59
model has limited training-distribution density to capture cleanly,
leaving a third action class (75% overbet) live in solver outputs.
Predictive entropy across the check-back / 33% bet / 75% overbet action
triple is high because no single action dominates across plausible BB
check-check-flop range models.

**Solver sizing notes:** Turn 33% (solver-aligned small size if betting).
Hero's candidate set (check-back vs 33% bet vs 75% bet) all
solver-aligned — no deviation.

---
