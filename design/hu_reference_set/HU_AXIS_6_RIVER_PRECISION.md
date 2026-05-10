# HU Axis 6 — River Decision Precision (HU-6.1 to HU-6.5)

**Date:** 2026-05-10
**Status:** Design only — no labelling, no corpus changes
**Context:** Phase 1.5-D.1 HU reference set — 1 of 6 axis breakouts (per design memo §4.2)

## Axis intro

Axis HU-6 targets heads-up postflop spots where every hand is on the
**river**, isolating the river-decision-precision class — value-bet
sizing across the solver-aligned 33% / 75% / 150% tier grid, bluff-catch
threshold spots facing villain's polarised river bet, and the river
overbet-response decision facing villain's 150%-pot overbet. All
draws have either completed or busted by the river, so hero's
composition triple at the decision node is restricted to TP+ (made
hands) versus busted-draws-now-air versus pure air (no live draw
equity remaining). Boards span dry-broadway-paired (canonical
nutted-overbet anchor), wet-completed-flush-and-straight (canonical
fold-to-overbet anchor), middling-paired-with-completed-front-door
(thin-value sizing entropy), broadway-with-busted-flush (bluff-catch
threshold), and connected-low-with-completed-straight (overbet-response
mid-strength bluff-catcher).

All 5 hands are heads-up (`num_opponents: 1`). Bet sizes are
solver-aligned per `feedback_solver_aligned_sizing.md` — river
sizes are restricted to 33% / 75% / 150% only, with no deviations;
prior-street sizes use the flop 25%/66% and turn 33%/75% solver
grid. 3 hands are CLOSE (model-uncertainty + poker-difficulty driven
per `feedback_close_hand_selection.md`, anchored on v9-3way-v22-on-59
predictive entropy across the relevant river-decision class — value-bet
sizing tier choice, bluff-catch fold/call threshold, or overbet-response
fold/call decision); 2 hands are CANONICAL (uncontroversial river
anchors — nutted hand 150% overbet for max value on dry-broadway-paired,
clear fold to 150% overbet with bottom of range on
wet-completed-flush-and-straight).

Cross-axis hygiene: hero hands and flop boards do not collide with HU-1
(AhKs, 9d9c, KhQd, TsTd, AhJh; flops Ad8c3h, 9h7s2c, KcTc6d, 8h5c2d,
Jc9c5d), HU-2 (AhQh, Td9d, Js9s, 6c5c, Ad5d; flops Kd7h4h, 8s6c2d,
Qs7s3d, 8c7d4h, Jh8d3c), HU-3 (7c6h, 4d3d, KsQs, Ts8h, Ac4c; flops
AhKd4s, QcJh9s, 8h6h5c, 7d7c3h, Kh9d6s), HU-4 (JsJh, 4h4c, KsTs, QhJh,
AhJc; flops Kd7h2c, KhQh9h, Td7d5s, 9h8h2c, Tc7c3s), or HU-5 (7d7s,
7h6h, QdTh, Th8h, KsJc; flops Th7c4h, 7c6s4d, Qh8s5c, 9h7c2h, 8h6d5h).

---

## Hand index

| ID | Marker | Street | Hero pos | Hand | Board | Decision class |
|----|--------|--------|----------|------|-------|----------------|
| HU-6.1 | CANONICAL | River | BTN | KhKs | Kc 7s 4h 2c Kd | Nutted quad kings on paired dry runout, river overbet 150% for max value |
| HU-6.2 | CANONICAL | River | BB | 8d8c | Jh 9h 6h Th Qd | Underpair on completed-flush-and-straight runout, fold to BTN 150% overbet |
| HU-6.3 | CLOSE | River | BTN | AsTs | Tc 7d 3c 5h 2s | Top pair top kicker on dry-disconnected runout, river value-bet sizing 33% vs 75% vs 150% |
| HU-6.4 | CLOSE | River | BB | AcQh | Qs 9c 4s 7c 2h | Top pair top kicker on busted-FD runout, bluff-catch fold/call threshold facing 75% bet |
| HU-6.5 | CLOSE | River | BTN | Qd9h | 7h 6c 5s 2d 8d | Nut straight without nut flush on completed-front-door-straight runout, overbet-response fold/call facing BB 150% lead |

---

## HU-6.1: KhKs flopped quad kings turning paired runout, BTN river 150% overbet for max value on Kc 7s 4h 2c Kd

**Marker:** CANONICAL

**Target axis:** Axis HU-6 — River decision precision
**Hero cards:** Kh/Ks
**Board:** Kc 7s 4h 2c Kd
**Street:** River
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 13.7bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** TP+ (quad kings — the absolute nuts on
this runout. Hero's KhKs combined with the Kc on the flop and the Kd
on the river makes four-of-a-kind kings, which beats every possible
villain holding without exception: every full house combination is
impossible because the only candidate full houses would be KK-full-of-
something (impossible, hero blocks both remaining kings) or
something-full-of-kings (777-KK / 444-KK / 222-KK — none of which can
exist because the board is K-7-4-2-K and a full house requires
three-of-a-kind plus a pair, which would need the under-card to be
paired in villain's hand — i.e., 77 / 44 / 22 sets — but those are
sets-not-boats because hero holds the only two remaining kings and the
only paired card on the board is the K, which means villain's 77 / 44 /
22 is a set with the K-K full-house-blocker = 77-KK / 44-KK / 22-KK
under-fulls that lose to hero's quads). Quads is the absolute nuts on
a board where hero holds both case-cards of the paired rank. Beats
every Kx trips combo (AK / KQ / KJ / KT — hero blocks both kings so
these combos cannot exist for villain; they reduce to AK / KQ / KJ /
KT being impossible holdings), every overpair AA / QQ / JJ / TT
bluff-catcher, every two-pair 7-4 / 7-2 / 4-2, every one-pair Ax-Kx
top-pair, every air bluff. No equity-tie possible.).

**Action history:** 100bb effective. BTN (hero) opens 2.5bb, BB calls.
Flop Kc 7s 4h (paired-with-the-turn structure not yet visible —
single-king flop with rainbow low cards; from villain's perspective,
this is a K-high disconnected texture where BB's range contains modest
Kx defends + medium pairs + air): BB checks, BTN (hero) bets 1.4bb
into 5.5bb (25% pot — solver-aligned flop small range-c-bet on a
K-high disconnected texture; hero has top set Kx-Kx and continues at
the range-c-bet size to keep BB's underpair / Ax / floats in the pot
without polarising hero's range). BB calls 1.4bb. Turn 2h (8.3bb pot;
brick low card, no draw completion, adds a backdoor heart-FD for BB's
two-heart combos): BB checks, BTN bets 2.7bb into 8.3bb (33% pot —
solver-aligned turn small; thin-pot-building size that keeps BB's
medium-pair + Ax floating range engaged at a price that does not fold
them out before the river extraction). BB calls 2.7bb. River Kd
(13.7bb pot; second king pairs the board for the second time and
turns hero's top set into quad kings — final runout is K-7-4-2-K,
two-tone hearts (4h / 2h) but with the Kd not adding a flush, so no
flush is possible on this exact runout): BB checks. Hero (BTN) faces
a checked-into river with the absolute nuts (quad kings) on a runout
where BB's range is condensed to medium pairs / weak top-pair Ax-K /
busted floats that may pay off a polarised overbet at meaningful
frequency.

**Solver sizing notes:** The canonical solver action class for the
absolute nuts on a paired-dry river runout where villain's range is
condensed to bluff-catcher pairs and busted floats is the **150% pot
overbet** (river large size — solver-aligned per
`feedback_solver_aligned_sizing.md` river 33/75/150 grid). The
overbet-for-max-value rationale is (i) BB's range on this runout
contains essentially zero combos that beat hero (no Kx full houses
because hero blocks both remaining kings; no straight or flush
completions possible on K-7-4-2-K with two hearts on board but no
third-heart river card), so hero's value bet has zero risk of being
raised by a better hand and the entire sizing decision reduces to
maximising the call frequency × bet size product, (ii) BB's
bluff-catcher range (77 / 88 / 99 / TT / JJ / QQ overpairs that turned
into underpairs on the K-river-pairing board, plus Ax-high and weak
Kx that called the small flop and turn bets) has a non-trivial
calling frequency against the 150% overbet because BB's pot odds at
150% are still 23.1% — and BB's medium-pair / weak-Kx holdings have
~50%+ equity vs the bluff-frequency component of hero's overbetting
range (which on this paired-river runout includes plausibly some
busted-float air combos that take the same line to balance), so BB's
call frequency is driven by inferred bluff frequency rather than by
absolute hand strength, (iii) the smaller 75% and 33% sizes leave
significant value on the table because they fail to extract from BB's
medium-pair range any more frequency than the 150% size would —
medium-pair calls or folds based on the ratio not the absolute size,
and the 150% size captures the additional value from the calls without
losing meaningful frequency, (iv) the paired-dry runout is the textbook
texture where overbets carry the maximum frequency in the solver
output for the strongest value combos because the lack of credible
straight / flush completions on the board means villain's range
contains no combos that can credibly raise the overbet (no nut-hand
threats), so the overbet sizing risks no raise-jam from a better
hand. This is the canonical HU-6 nutted-overbet-for-max-value anchor:
absolute nuts on the textbook paired-dry runout where the 150% river
overbet is the single highest-EV sizing in the solver-aligned grid.
Bet 20.6bb into 13.7bb (150% pot — solver-aligned river overbet, no
deviation).

---

## HU-6.2: 8d8c underpair on Jh 9h 6h Th Qd completed-flush-and-straight runout, BB fold to BTN 150% overbet

**Marker:** CANONICAL

**Target axis:** Axis HU-6 — River decision precision
**Hero cards:** 8d/8c
**Board:** Jh 9h 6h Th Qd
**Street:** River
**Hero position:** BB
**Primary villain position:** BTN
**Num opponents:** 1
**Pot:** 13.7bb
**Facing bet:** Yes
**To call:** 20.6bb
**Pot odds required:** 37.5%
**Opener position:** BTN
**Bettor position:** BTN
**Hand strength composition:** Air (busted underpair → effectively no
showdown value on this runout. Hero held 88 — a pocket pair that was an
underpair on the J-9-6 flop, remained an underpair on the J-9-6-T turn
where hero's pair lost to any T+ overpair and was now further dominated
by every made T-or-better top pair, and on the Q river hero's 88 is
beaten by every overpair JJ-AA, every Tx top-pair, every Jx /Qx /
9x / Tx / Jx top-pair, every two-pair combination on this five-card
board that contains four broadway connectors, every flopped + turned
+ rivered straight (K8-or-87 makes the wheel-irrelevant, but T8 / 87 /
J7 etc. give villain T-J-Q straights, K-Q-J-T-9 broadway via any K, and
Q-J-T-9-8 wraparound with hero's 8 contributing only a blocker), and
every completed flush from the three hearts on board (any villain Xh +
Xh = made flush). Re-spec — on J-9-6-T-Q with three hearts on board, 88
is no-showdown-value air at the river: hero loses to virtually every
combo in BTN's value range and ties or loses to any holding with a
single broadway card. Backdoor / overcard / flush-blocker contribution:
zero — hero holds Sd / 8c, no hearts in hand for flush blocker, no
broadway cards for straight-blocker. Classify as air — busted underpair
with no showdown value and no blocker effect against villain's value
range.).

**Action history:** 100bb effective. BTN (hero villain) opens 2.5bb,
BB (hero) calls. Flop Jh 9h 6h (monotone hearts, J-high,
straight-and-flush-draw-saturated): BB checks, BTN bets 1.4bb into 5.5bb
(25% pot — solver-aligned flop small range-c-bet on a monotone texture
where BTN's range-vs-range advantage is modest but the small size
keeps the pot manageable for OOP play). Hero calls 1.4bb with the
underpair-and-backdoor-equity 88 (vague backdoor: any 7 or T gives a
gutshot on later streets; no flush draw because hero holds zero hearts).
Turn Th (8.3bb pot; T of hearts — completes flush draws and brings
straight equity for hands containing K / 8 / 7): BB checks, BTN bets
2.7bb into 8.3bb (33% pot — solver-aligned turn small; range-balanced
size on a runout where BTN's range now contains made flushes / straights
and bluffs that benefit from the small pot-build for river polarisation).
Hero calls 2.7bb (peeling cheaply with the now-three-card-straight-draw
via 87 wheel — *correction*: the wheel needs A-2-3-4-5, hero's 88 has
no straight draw; hero is calling purely to peel a turn card hoping for
an 8 to make a set, ~2 outs, ~4% equity, an over-call relative to pot
odds but justified by the small turn size + implied odds on an 8 turn).
River Qd (13.7bb pot; Q completes K-J-T or J-T-9-8-Q straights, brings
a fourth broadway card on a board with three hearts, board is now
J-9-6-T-Q with three hearts and four broadway connectors): BTN bets
20.6bb into 13.7bb (150% pot — solver-aligned river overbet from BTN
representing made flush / made straight / set-of-T-or-Q value on a
runout where BTN's polarised overbetting range is tightly bounded to
made-hand value plus a low frequency of well-chosen bluffs). Hero
faces BTN's 150% overbet OOP with no-showdown-value air.

**Solver sizing notes:** The canonical solver action class for
no-showdown-value air facing a 150% river overbet on a runout where
villain's overbetting range is dominated by made flushes and straights
is the **fold** (river overbet-response — solver-aligned per the
`feedback_solver_aligned_sizing.md` river 33/75/150 size grid; the
hero's response to villain's 150% is fold/call, not raise/re-raise).
The fold rationale is (i) hero's 88 has effectively zero showdown
equity on this runout — beating only a thin slice of busted-bluff
combos that BTN may polarise into the overbet bucket as balance, and
losing to the entire flush + straight + set + two-pair + top-pair
mass of BTN's value range, (ii) hero requires 37.5% equity to call
the 150% overbet given the pot odds, and the bluff-frequency required
for hero's call to be break-even is ~37.5% / (1 + bluff-frequency)
which on a monotone-completed-flush + straight-completed runout is
significantly above any plausible BTN overbet bluff-frequency
(realistic BTN overbet bluff frequency on this texture is ~15-25%
of the overbetting range — well below the call-required threshold),
(iii) hero holds zero blockers to BTN's value range (no hearts to
block flushes, no broadway cards to block straights), so hero's
fold-equity-via-blocker argument is null, (iv) hero's underpair has
no improvement equity going forward because the action ends at the
river — it is a pure showdown-value calculation and the showdown value
is zero against the dominant value range, (v) the overbet sizing
itself signals BTN's confidence in being ahead — the 150% size on
the most flush-and-straight-saturated possible runout is the textbook
solver tell that BTN's range is condensed to nut + near-nut combos
plus a thin bluff-frequency tail. This is the canonical HU-6
overbet-fold-with-bottom-of-range anchor: no-showdown-value air on
the textbook flush-and-straight-completed runout where the fold to
the 150% overbet is the single highest-EV response in the
solver-aligned grid. Fold — solver-aligned, no deviation.

---

## HU-6.3: AsTs top pair top kicker on Tc 7d 3c 5h 2s dry-disconnected runout, BTN river value-bet sizing 33% vs 75% vs 150%

**Marker:** CLOSE

**Target axis:** Axis HU-6 — River decision precision
**Hero cards:** As/Ts
**Board:** Tc 7d 3c 5h 2s
**Street:** River
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 13.7bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** TP+ (top pair top kicker — A-T-of-spades
on a T-7-3-5-2 rainbow runout; ahead of every Tx top-pair with a kicker
worse than ace (TJ / T9 / T8 / T6 / T5 / T4 / T3 / T2 — many of these
unlikely combos in BB's defending-and-passive-line range, but K-T / Q-T
/ J-T are all live and dominated by hero's A-kicker), behind only Ax-set
combos (TT / 77 / 33 / 55 / 22 — which on this runout would have
two-pair-or-better and could plausibly bet the river themselves for
value) and a thin slice of straight combos (4-6 / 6-4 / 6-8 / 4-6
straight completions on the 7-3-5-2 portion of the board: the relevant
wheel-and-mid-straight combos are A-2-3-4-5 needing both an A and a 4
in villain's hand, 3-4-5-6-7 needing a 4 and 6, and 4-5-6-7-8 needing
a 4 and 6 or 8 and a 4 — the relevant straight completions reduce to
"villain holds a 4-6 or 4-x" which is a narrow band of suited-connector
defends from BB). Net: hero has top pair top kicker on a textbook
medium-disconnected dry runout where the dominant beat-vs-lose
distribution is one-pair-better (hero ahead of all medium-and-low
one-pair combos) and a small straight + set tail that beats hero. The
classification is solidly TP+ with a clear thin-value extraction
problem on the river.).

**Action history:** 100bb effective. BTN (hero) opens 2.5bb, BB calls.
Flop Tc 7d 3c (rainbow with one club-club setup, T-high, mid-low
disconnected): BB checks, BTN bets 1.4bb into 5.5bb (25% pot —
solver-aligned flop small range-c-bet on a T-high disconnected texture
where BTN's range advantage is meaningful and the small size keeps
BB's wide defend range engaged at favourable equity for hero's TPTK).
BB calls 1.4bb. Turn 5h (8.3bb pot; brick low card, no draw completion,
adds a heart for backdoor flush possibility on BB's range): BB checks,
BTN bets 2.7bb into 8.3bb (33% pot — solver-aligned turn small;
thin-pot-building size on a runout that has not changed BB's calling
range significantly). BB calls 2.7bb. River 2s (13.7bb pot; second brick
low card, no draw completion, runout is now T-7-3-5-2 rainbow with one
heart on turn — no flush possible, only the 4-6 straight completions
beat hero among the straight-relevant combos): BB checks. Hero (BTN)
faces a checked-into river with TPTK on a runout where BB's range is
condensed to medium-pair bluff-catchers (88 / 99 / JJ / QQ / KK
overpairs that called twice without raising), thin Tx top-pair
holdings (KT / QT / JT — dominated by hero's kicker), Ax-with-pair
floats, and a small busted-draw bluff-frequency tail (gutshot 6-8 / 4-6
combos that missed).

**CLOSE rationale:** Three-action genuine entropy across the river
value-bet-sizing tier dimension (33% / 75% / 150% of pot per the
solver-aligned grid). The decision splits between (a) value-bet 4.5bb
into 13.7bb (33% — solver-aligned river small thin-value sizing that
maximises call-frequency by keeping BB's medium-pair underpair range
calling at ~80%+ frequency and extracting modest value from Tx-worse
combos at ~70% frequency, conceding the upside that 75% and 150% would
extract from the strongest-call combos), (b) value-bet 10.3bb into
13.7bb (75% — solver-aligned river large thin-to-medium value sizing
that targets the Tx-worse + medium-overpair-bluff-catcher mid-range of
BB's calling distribution, accepting reduced call-frequency from the
weakest underpairs in exchange for higher absolute value from the
calls hero does get), and (c) value-bet 20.6bb into 13.7bb (150% —
solver-aligned river overbet thick-value sizing that polarises hero's
range to nut + near-nut + thin-bluff and extracts maximum value from
BB's overpair-bluff-catcher range that calls based on inferred bluff
frequency, accepting the risk that BB's medium-pair range folds at
elevated frequency to the polarising size). v9-3way-on-59 model
uncertainty is elevated because (i) T-7-3-5-2 rainbow is a textbook
mixing-zone river runout for the value-bet-sizing-tier decision class,
where the optimal solver size for TPTK splits across 33% / 75% / 150%
at non-trivial frequencies depending on the exact turn-bet-and-call
range distribution BB carries to the river — and the v9-3way-on-59
model has not been trained on a river-sizing-tier label distribution
that distinguishes the three sizes cleanly because the 988-on-59
training corpus mixes the three sizes within the bet-large action
class; (ii) the kicker-dominance asymmetry (hero's A blocks BB's
A-high overpair AA reducing BB's value-raise frequency to near-zero,
but hero's T blocks BB's KT / QT / JT dominated-Tx range reducing
hero's thin-value extraction frequency on the 150% size) creates a
non-monotone EV profile across the three sizes — the small size
captures the most low-frequency calls, the medium size captures the
most medium-frequency calls, and the large size captures the most
inferred-bluff-frequency-driven calls; (iii) the medium-disconnected
dry runout is one of the few HU board classes where the solver actually
mixes meaningfully across all three river value sizes for top-pair
value combos, making it a rare clean test of the river-sizing-tier
decision class without the texture defaulting to a single size.
Predictive entropy across the bet-33% / bet-75% / bet-150% action
triple is high because no single size dominates across plausible BB
turn-call range models.

**Solver sizing notes:** All three candidate river bet sizes (33% =
4.5bb, 75% = 10.3bb, 150% = 20.6bb into 13.7bb pot) are solver-aligned
per `feedback_solver_aligned_sizing.md` river 33/75/150 grid. Hero's
three-action candidate set covers the live solver mix on this spot
exactly — no deviation from the solver-aligned grid. (Check-back is
not in the solver action class for TPTK on a checked-into river with
BB capped at bluff-catchers; the entropy is exclusively across the
three value-sizing tiers.)

---

## HU-6.4: AcQh top pair top kicker on Qs 9c 4s 7c 2h busted-FD runout, BB bluff-catch fold/call threshold facing 75% bet

**Marker:** CLOSE

**Target axis:** Axis HU-6 — River decision precision
**Hero cards:** Ac/Qh
**Board:** Qs 9c 4s 7c 2h
**Street:** River
**Hero position:** BB
**Primary villain position:** BTN
**Num opponents:** 1
**Pot:** 20.7bb
**Facing bet:** Yes
**To call:** 15.5bb
**Pot odds required:** 30.0%
**Opener position:** BTN
**Bettor position:** BTN
**Hand strength composition:** TP+ (top pair Q with A-kicker on a
Q-9-4-7-2 runout; ahead of every Qx with a kicker worse than A (KQ /
QJ / QT / Q9 / Q8 / Q7 / Q5 / Q4 / Q3 / Q2 — most are non-credible BTN
opens but KQ / QJ / QT are credible defends and dominated by hero's
A-kicker, and Q9-suited / Q7-suited / Q4-suited make two-pair and
beat hero), behind every overpair AA (partially blocked by hero's A) /
KK, every set QQ / 99 / 77 / 44 / 22, every two-pair combination 97 /
94 / 92 / 74 / 72 / 42 (most of these unlikely defends, but Q9-suited
from a BTN open is plausible in an open-and-c-bet line), and the
now-busted spade flush draws that remained as bluffs. Spade flush draw
on the board (Qs / 4s on flop + turn) busted because the river 2h is
not a spade — no flush possible, so any spade-flush-draw combos in
BTN's barrel range are busted and arrive at the river as bluffs.
Backdoor club-flush from the 9c / 7c turn pair busted on the 2h river
(hero's Ac contributes a single club but no flush completes). Hero's
A-kicker provides credible top-pair-top-kicker showdown value with the
dominant uncertainty being whether BTN's polarised river-bet range is
weighted toward value (sets / two-pair / overpairs that beat TPTK) or
toward busted-FD bluffs.).

**Action history:** 100bb effective. BTN (hero villain) opens 2.5bb,
BB (hero) calls. Flop Qs 9c 4s (two-tone spades, Q-high, mid-low
disconnected): BB checks, BTN bets 1.4bb into 5.5bb (25% pot —
solver-aligned flop small range-c-bet on a Q-high two-tone texture;
BTN's range-bet structure on this texture is the small-c-bet because
his range advantage from the open-raise is meaningful but the spade-FD
texture rewards high-frequency continuation at small size). BB calls
1.4bb with TPTK. Turn 7c (8.3bb pot; brick mid card adding a backdoor
club-FD that hero touches via the Ac single-club but does not turn
into a flush draw, while BTN's range contains some Cc-Cc combos that
pick up a turned FD): BB checks, BTN bets 6.2bb into 8.3bb (75% pot —
solver-aligned turn large polarised double-barrel; BTN polarises on
the turn with value + spade-FDs + some pure bluffs balancing as the
spade-FD texture supports a polarising large size on the turn brick).
BB calls 6.2bb. River 2h (20.7bb pot; brick low card that completes no
draws — the spade-FD from the flop busted on the brick turn and brick
river, the turned club-FD busted on the heart river, no
straight-completing card; runout is Q-9-4-7-2 rainbow at the river
with the spade-FD fully dead): BTN bets 15.5bb into 20.7bb (75% pot —
solver-aligned river large polarised triple-barrel; BTN's polarised
range at this node is value (sets / two-pair / overpairs that beat
TPTK) plus the busted-spade-FD bluffs (any two-spade combo that bet
flop / turn and arrived at the river without showdown value)). Hero
faces BTN's 75% river polarised triple-barrel OOP with TPTK on a
runout where every relevant draw busted.

**CLOSE rationale:** Two-action genuine entropy across the bluff-catch
fold/call threshold dimension. The decision splits between (a) call
15.5bb to win 20.7bb (requires 30.0% equity vs BTN's polarised
river-bet range) — the calling rationale is that BTN's triple-barrel
range on a busted-FD runout contains a non-trivial bluff frequency
from the spade-FDs and combo-draws that took the bet-bet-bet line
and arrived without showdown value, hero's TPTK beats the entire
bluff-frequency component (busted FDs / busted combo-draws / pure
air that took the polarising line), the A-kicker dominates BTN's
entire Qx value range (KQ / QJ / QT credible) and only loses to the
narrow set / two-pair / overpair value mass; and (b)
fold — the folding rationale is that BTN's triple-barrel on a
75% / 75% / 75% line represents a polarising sequence weighted heavily
toward the strongest value combos (sets / two-pair / overpairs) and the
required-equity-to-call of 30% is not cleared by hero's actual equity
against the realistic value-vs-bluff distribution: if BTN's
river-bet bluff frequency is below ~30% of the betting range (a
plausible upper bound for triple-barrel polarised lines on busted-FD
runouts, where the FD combos that bet flop + turn often check-give-up
the river instead of triple-barrelling), then hero's call is -EV.
v9-3way-on-59 model uncertainty is elevated because (i) the bluff-catch
fold/call threshold for TPTK facing a 75% triple-barrel on a busted-FD
runout sits at the equity-vs-bluff-frequency boundary —
BTN's actual bluff frequency in solver outputs is typically 25-35%
of the betting range on this texture, bracketing the 30% pot-odds
threshold with high enough variance that the optimal action is
mixed; (ii) Q-high two-tone spade textures with brick turn and brick
no-flush river are a known mixing-zone for the OOP TPTK bluff-catch
decision because the spade-FD bluff frequency component of BTN's
range varies meaningfully with the exact turn-call range model
(tighter turn-call models reduce river bluff frequency, looser turn-call
models elevate it); (iii) hero's A-kicker provides modest blocker
benefit against AA and AQ in BTN's value range, marginally improving
the call EV but not by enough to break the threshold cleanly; (iv) the
v9-3way-on-59 model has not been trained on a label distribution
that distinguishes triple-barrel-polarised-lines cleanly from
double-barrel-then-give-up lines because the 988-on-59 corpus does
not over-weight river-decision spots, leaving the model uncertain
across the fold/call threshold for medium-strength bluff-catchers.
Predictive entropy across the call / fold action pair is high because
no single action dominates across plausible BTN triple-barrel range
models.

**Solver sizing notes:** Facing 75% river bet (15.5bb into 20.7bb,
30.0% pot odds) is solver-aligned per
`feedback_solver_aligned_sizing.md` river 33/75/150 grid. Hero's
two-action candidate set (call / fold) covers the live solver mix
on this spot — raise is not in the solver action class for TPTK
facing a polarised 75% triple-barrel on a busted-FD runout (no
credible value-raise from below sets, no credible bluff-raise from a
hand with showdown value). No deviation from the solver-aligned
grid.

---

## HU-6.5: Qd9h nut straight without nut flush on 7h 6c 5s 2d 8d completed-front-door-straight runout, BTN overbet-response fold/call facing BB 150% lead

**Marker:** CLOSE

**Target axis:** Axis HU-6 — River decision precision
**Hero cards:** Qd/9h
**Board:** 7h 6c 5s 2d 8d
**Street:** River
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 13.7bb
**Facing bet:** Yes
**To call:** 20.6bb
**Pot odds required:** 37.5%
**Opener position:** BTN
**Bettor position:** BB
**Hand strength composition:** TP+ (nut-straight 9-high — hero holds Qd/9h
on a 7-6-5-2-8 runout that completes the straight 5-6-7-8-9 with hero's
9h making the high end of the straight; the Qd is an overcard with no
made-pair contribution. Hero held two-overcards-with-backdoor-straight on
the 7-6-5 flop (Q overcard + 9 backdoor inside-straight piece), retained
the same shape on the 7-6-5-2 turn (the 2d added a backdoor diamond-FD
for hero only via the Qd, not a direct draw), and the 8 river card
converts the holding into the nut straight 5-6-7-8-9 — hero's 9 makes
the high end of the straight which is the nut straight on this runout
(no T+ overcard on board, so 6-7-8-9-T is impossible; the only better
hand on the made-straight axis would be a higher straight 6-7-8-9-T
which requires a T which is not on the board, so 9-high straight = the
absolute nuts on the made-straight axis). Hero loses only to a higher
straight (impossible — no T on board), a flush (board has two diamonds
2d/8d, BB needs two diamonds for a flush — hero's Qd blocks one diamond
combo modestly), a full house (impossible — board is unpaired), or
quads (impossible — board is unpaired). On the made-straight axis,
hero = the nuts on this exact runout. Re-classify: hero is at the
absolute top of the straight ranking but loses to flushes if BB held a
flush draw. Net: hero's Q9 makes the nut straight but is dominated by
a flush completion from any two-diamond hand in BB's range — and BB
just led 150% pot into the river, which is a textbook overbet sizing
for the nut flush.).

**Action history:** 100bb effective. BTN (hero) opens 2.5bb, BB calls.
Flop 7h 6c 5s (rainbow, mid-low connected with maximal straight-and-OESD
texture, no FD on flop — purely a straight-draw-saturated texture for
both ranges): BB checks, BTN (hero) bets 1.4bb into 5.5bb (25% pot —
solver-aligned flop small range-c-bet on a connected mid-low texture
where BTN's range advantage is modest but the small size keeps BB's
wide pair-and-draw defend range engaged). BB calls 1.4bb. Turn 2d
(8.3bb pot; brick low card, adds a backdoor diamond-FD for any
two-diamond combos in BB's range — including 9d-Td combo-straight-draws,
4d-3d wheel-completing-with-FD, etc.): BB checks, BTN bets 2.7bb into
8.3bb (33% pot — solver-aligned turn small; BTN continues with the
two-overcard + backdoor-straight equity holding plus range-bet
thin-value on a brick turn that did not change the range structure
significantly). BB calls 2.7bb. River 8d (13.7bb pot; 8 of diamonds —
completes the front-door straight 5-6-7-8-9 for hero and any BB combo
with a 9 or 4, completes the back-door diamond-FD for any two-diamond
combo in BB's range that turned a draw on the 2d): BB leads (donks)
20.6bb into 13.7bb (150% pot — solver-aligned river overbet from BB
representing the polarised range of nut-straight combos (9x) +
nut-flush completions (high-diamond-pairs that turned the BDFD on the
2d and rivered the diamond on the 8d) + a thin slice of well-chosen
polarising bluffs). Hero faces BB's 150% river overbet IP with the
nut-straight-but-not-the-nut-flush Q9.

**CLOSE rationale:** Two-action genuine entropy across the
overbet-response fold/call threshold dimension for a mid-strength
bluff-catcher (specifically: nut-straight-on-flush-completing-runout,
the textbook two-tier bluff-catcher problem where hero is ahead of
all non-flush combos in villain's range and behind all flush-completion
combos). The decision splits between (a) call 20.6bb to win 13.7bb
(requires 37.5% equity vs BB's 150% overbet range) — the calling
rationale is that BB's overbet range on this runout contains a
non-trivial frequency of straight-and-set-and-overpair value combos
that hero beats with the nut straight (any 9x makes the same straight
and chops, but credible BB defending combos with a 9 are 9-T / 9-J /
9-Q / 9-K offsuit which are not standard BB defends — the realistic
9x mass in BB's range is small; sets 77 / 66 / 55 — hero's straight
beats any set on this unpaired board; two-pair 76 / 75 / 65 — hero's
straight beats all of these; overpair 88 / 99 / TT / JJ / QQ / KK / AA
— hero's straight beats all overpairs except a higher straight which is
impossible without a T on board; and the bluff-frequency component
which hero beats trivially), and the fold-equity-against-bluffs argument:
BB's 150% overbet bluff frequency on a flush-completing runout is
typically the highest frequency hero can hope for from polarised
overbet ranges (~25-30% of the betting range), making the call EV
positive against the realistic value-vs-bluff distribution; and (b)
fold — the folding rationale is that BB's 150% lead-overbet on a
flush-completing runout polarises BB's range so strongly toward
nut-flush-and-near-nut value that the bluff frequency drops below
the 37.5% pot-odds threshold required to break even: if BB's
overbet-bluff frequency is below 37.5% of the betting range, hero's
call is -EV against the value-weighted range. The BB lead-instead-of-
check-call-line on the river is itself a tell of polarisation (BB
chose the strongest available action sequence — donk-overbet-150% on
a flush-completing river — which solver outputs reserve for the
strongest value combos plus a thin bluff-frequency tail). v9-3way-on-59
model uncertainty is elevated because (i) the overbet-response
fold/call threshold for nut-straight-without-the-nut-flush facing a
150% lead-overbet on a flush-completing runout sits at the
equity-vs-bluff-frequency knife-edge — the model has limited training
signal on the donk-lead-overbet-150% line because this is a low-
frequency action class in the 988-on-59 corpus, leaving model
uncertainty elevated across the fold/call threshold; (ii) the
two-tier bluff-catcher problem (hero ahead of all non-flush, behind
all flush) creates a sharp EV cliff at the bluff-frequency threshold
that the model uncertainty signal captures clearly — small changes
in inferred BB bluff frequency flip the optimal action; (iii) the
nut-straight-on-flush-completing-runout texture is a known mixing-zone
for the overbet-response decision class because hero's diamond
blocker is weak — the Qd blocks a single diamond combo modestly but
is not a high-diamond blocker (no Ad / Kd in hand) against BB's
nut-flush combos, so hero's blocker argument is weak and the decision
reduces near pure equity-vs-frequency math; (iv) the donk-lead overbet
line from BB is rare enough in the 988-on-59 training distribution
that the model has not converged on a tight optimal-frequency signal
for this exact action sequence, elevating predictive entropy across
the call / fold pair. Predictive entropy across the call / fold
action pair is high because no single action dominates across plausible
BB lead-overbet range models.

**Solver sizing notes:** Facing 150% river overbet (20.6bb into 13.7bb,
37.5% pot odds) is solver-aligned per
`feedback_solver_aligned_sizing.md` river 33/75/150 grid. Hero's
two-action candidate set (call / fold) covers the live solver mix
on this spot — raise is not in the solver action class for
nut-straight-without-the-nut-flush facing a polarised 150% lead-overbet
on a flush-completing runout (no credible value-raise from a hand
that loses to the top of villain's range, no credible bluff-raise
from a hand with showdown value at the second tier). No deviation
from the solver-aligned grid.

---
