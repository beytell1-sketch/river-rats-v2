# HU Axis 5 — Out-of-Position Decisions (HU-5.1 to HU-5.5)

**Date:** 2026-05-10
**Status:** Design only — no labelling, no corpus changes
**Context:** Phase 1.5-D.1 HU reference set — 1 of 6 axis breakouts (per design memo §4.2)

## Axis intro

Axis HU-5 targets heads-up postflop spots where hero is **out-of-position**
versus an in-position villain (BTN/SB opener). The decision class under test
is the OOP-line triple — **check-raise frequency, donk-bet (lead-out)
usage, and lead-out-then-barrel lines** — across textures that vary in which
side owns the range advantage. Hero composition spans TP+ / draws / air per
`feedback_preflop_geometry_vs_postflop_composition.md` so the OOP-line
decision is exercised across hand-strength categories rather than within a
single bucket. Boards span BTN-favoured high-card (TP medium-kicker dilemmas),
BB-favoured low-connected (donk-lead canonicals), wet two-tone with combo
draws (semi-bluff check-raise vs lead vs check-call), and BB-favoured
two-tone-connected with overcard-air (donk vs check-fold vs check-call float).

All 5 hands are heads-up (`num_opponents: 1`). Hero is OOP (BB) in every
spot; villain is the IP preflop opener (BTN). Bet sizes are solver-aligned
per `feedback_solver_aligned_sizing.md` (flop 25%/66%, turn 33%/75%, river
33%/75%/150%); check-raise sizes are 3x the bet faced unless otherwise
documented. 3 hands are CLOSE (model-uncertainty + poker-difficulty driven
per `feedback_close_hand_selection.md`, anchored on v9-3way-v22-on-59
predictive entropy across the check-raise / check-call / donk / lead action
class trade-off); 2 hands are CANONICAL (uncontroversial OOP-line anchors —
flopped set check-raise on wet draw-heavy texture, two-pair donk-lead on
BB-favoured low-connected texture).

Cross-axis hygiene: hero hands and flop boards do not collide with HU-1
(AhKs, 9d9c, KhQd, TsTd, AhJh; flops Ad8c3h, 9h7s2c, KcTc6d, 8h5c2d,
Jc9c5d), HU-2 (AhQh, Td9d, Js9s, 6c5c, Ad5d; flops Kd7h4h, 8s6c2d, Qs7s3d,
8c7d4h, Jh8d3c), HU-3 (7c6h, 4d3d, KsQs, Ts8h, Ac4c; flops AhKd4s, QcJh9s,
8h6h5c, 7d7c3h, Kh9d6s), or HU-4 (JsJh, 4h4c, KsTs, QhJh, AhJc; flops
Kd7h2c, KhQh9h, Td7d5s, 9h8h2c, Tc7c3s).

---

## Hand index

| ID | Marker | Street | Hero pos | Hand | Board | Decision class |
|----|--------|--------|----------|------|-------|----------------|
| HU-5.1 | CANONICAL | Flop | BB | 7d7s | Th 7c 4h | Flopped set check-raise on wet two-tone vs BTN c-bet |
| HU-5.2 | CANONICAL | Flop | BB | 7h6h | 7c 6s 4d | Two-pair donk-lead on BB-favoured low-connected texture |
| HU-5.3 | CLOSE | Flop | BB | QdTh | Qh 8s 5c | TP medium kicker, check-call vs check-raise vs donk facing 25% c-bet |
| HU-5.4 | CLOSE | Flop | BB | Th8h | 9h 7c 2h | Combo draw OOP, donk-lead vs check-call vs check-raise after c-bet |
| HU-5.5 | CLOSE | Flop | BB | KsJc | 8h 6d 5h | Overcard air on BB-favoured two-tone-connected, donk vs check-fold vs check-call |

---

## HU-5.1: 7d7s flopped set on Th7c4h two-tone, BB check-raise vs BTN c-bet

**Marker:** CANONICAL

**Target axis:** Axis HU-5 — Out-of-position decisions
**Hero cards:** 7d/7s
**Board:** Th 7c 4h
**Street:** Flop
**Hero position:** BB
**Primary villain position:** BTN
**Num opponents:** 1
**Pot:** 7bb
**Facing bet:** Yes
**To call:** 4.6bb
**Pot odds required:** 24.5%
**Opener position:** BTN
**Bettor position:** BTN
**Hand strength composition:** TP+ (flopped middle set — second-nut made hand
on this texture, dominated only by TT top set. Beats every overpair JJ-AA,
every Tx top-pair, every two-pair Tx + 7x or Tx + 4x combo, every flush
draw, every straight draw, and every air holding in BTN's c-betting range.
Strongest possible value-and-protection holding given the wet two-tone
straight-and-flush-draw texture).

**Action history:** 100bb effective. BTN (hero villain) opens 2.5bb, BB
(hero) calls. Flop Th 7c 4h (two-tone hearts, T-high, mid-low connected
with OESD via 8-9 / 9-J one-card straights and FD via any heart). BB
checks. BTN bets 4.6bb into 7bb (66% pot — solver-aligned flop large size,
the polarized sizing BTN takes with value + nut-FDs + air on this dynamic
texture). Hero faces BTN's c-bet OOP with the flopped set.

**Solver sizing notes:** The canonical solver action class for OOP set on
a wet two-tone draw-heavy texture facing a polarized 66% c-bet is the
check-raise — high frequency because (i) BB needs to charge BTN's wide
draw-heavy continuing range a fair price before the turn brings a
straight or flush card that kills hero's action, (ii) BB needs to deny
the realisation of equity for BTN's two-overcard / gutshot floats,
(iii) BB's range protection benefits from including the strongest value
combos in the check-raise range alongside the semi-bluff combos
(NFD + OESD) to prevent BTN from over-bluffing the turn against a
condensed BB check-call range, and (iv) the SPR after a check-raise sets
up a clean 2-street value extraction on safe runouts plus a credible
turn jam on flush- or straight-completing scare cards. Hero's check-raise
size is 3x the c-bet (4.6bb → ~14bb total raise into a pot that becomes
~25.6bb, ~55% of the post-raise pot — a standard 3x check-raise sizing
that builds the pot decisively while leaving stacks-behind room for a
turn jam). This is the canonical HU-5 strong-hand-OOP check-raise anchor:
flopped set on the wettest mainstream HU board class, where the
check-raise is the textbook solver line at the highest-frequency rung.
Check-raise to ~14bb (3x the bet) — solver-aligned action class; the 3x
check-raise sizing is a documented standard for OOP value-and-protection
raises into 66% c-bets on draw-heavy textures (no deviation from the
solver-aligned grid).

---

## HU-5.2: 7h6h flopped two-pair on 7c6s4d BB-favoured low-connected, BB donk-lead vs BTN

**Marker:** CANONICAL

**Target axis:** Axis HU-5 — Out-of-position decisions
**Hero cards:** 7h/6h
**Board:** 7c 6s 4d
**Street:** Flop
**Hero position:** BB
**Primary villain position:** BTN
**Num opponents:** 1
**Pot:** 5.5bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** TP+ (flopped top + second pair = top two-pair,
sevens-and-sixes. Beats every overpair 88-AA on this texture (vs sets only;
hero blocks 76 / 77 / 66 reduces overpair-set combos), beats every one-pair
Ax / Kx / Qx / Jx / Tx / 9x / 8x holding, beats every gutshot backdoor
combo, loses only to the three flopped sets 777 / 666 / 444 and to the
flopped straight 85 / 53 / 35 wheel-straight-completing holdings — which
are heavily blocked by hero's 7 and 6. Backdoor heart-flush contribution
from 7h-6h adds modest equity vs 4x / overpair turns. Strongest realistic
made-hand class on this BB-favoured low-connected texture).

**Action history:** 100bb effective. BTN (hero villain) opens 2.5bb, BB
(hero) calls. Flop 7c 6s 4d (rainbow, low, maximally connected — every
3, 5, 8 brings a one-card straight; BB's defend range contains the
overwhelming majority of straight + two-pair + set combos on this
texture, while BTN's open-only-no-3bet range is dominated by overcard-air
that misses entirely). BB acts first OOP. Hero faces a checked-into
flop with two-pair on the most BB-favoured low-card texture in the
HU spectrum.

**Solver sizing notes:** The canonical solver action class on
7-6-4-rainbow texture from BB into BTN's c-betting range is a
high-frequency donk-lead at small size (25% pot — solver-aligned flop
small) because (i) BB has a meaningful range advantage on this texture
(BB defends 76s / 87s / 65s / 54s / 75s / 64s / 33-77 small pairs at
high frequency, while BTN's open range contains far fewer of the
straight-and-set combos that interact with 7-6-4 and many more
overcard-air combos that have given up by the flop), (ii) the
donk-lead protects BB's range against BTN's checked-back equity-realising
overcard hands that would see a free turn under the standard
check-and-c-bet line, (iii) the 25% size charges BTN's continuing range
(overcard-pair + backdoor-FD) a poor immediate price while keeping the
pot small for OOP play on later streets, and (iv) two-pair specifically
sits in the donk-lead-for-value bucket because it benefits from immediate
pot-building against the wide range of one-pair + overcard hands BTN
will float at small size while remaining ahead of all but a small set
of straight + set combos on the turn. This is the canonical HU-5
donk-lead anchor: top-two-pair on the most BB-favoured mainstream HU
board class, where the donk-lead at 25% pot is the textbook solver line
at the highest-frequency rung. Donk-bet 1.4bb into 5.5bb (25% pot) —
solver-aligned, no deviation.

---

## HU-5.3: QdTh top pair medium kicker on Qh8s5c, BB facing BTN 25% c-bet — check-call vs check-raise vs donk-leading

**Marker:** CLOSE

**Target axis:** Axis HU-5 — Out-of-position decisions
**Hero cards:** Qd/Th
**Board:** Qh 8s 5c
**Street:** Flop
**Hero position:** BB
**Primary villain position:** BTN
**Num opponents:** 1
**Pot:** 6.5bb
**Facing bet:** Yes
**To call:** 1.6bb
**Pot odds required:** 19.7%
**Opener position:** BTN
**Bettor position:** BTN
**Hand strength composition:** TP+ (top pair Q with a T kicker on a Q-high
two-tone-mismatched + low-connected texture; ahead of every non-Q one-pair
in BTN's c-betting range and ahead of every air / backdoor float, behind
QJ / AQ / KQ value combos and the small set / two-pair frequency. Medium
kicker creates the dominated-vs-Qx asymmetry that defines the close
decision: hero beats Qx with 9-or-worse kicker but loses to QJ / KQ / AQ
that BTN c-bets at high frequency. Backdoor heart-FD contribution from
the Th gives a thin equity bump on heart turns).

**Action history:** 100bb effective. BTN (hero villain) opens 2.5bb, BB
(hero) calls. Flop Qh 8s 5c (rainbow with one-tone setup via the Qh /
hero's Th = backdoor heart possibility; Q-high disconnected from 8-5).
BB checks. BTN bets 1.6bb into 6.5bb (25% pot — solver-aligned flop
small, the range-c-bet sizing BTN uses on Q-high dry-ish boards). Hero
faces BTN's small c-bet OOP with TP medium kicker.

**CLOSE rationale:** Three-action genuine entropy across the OOP-line
dimension after the small c-bet. The decision splits between (a) check-call
to keep BTN's air / underpair / backdoor-float range in the pot at a
favourable price, conceding the kicker-dominated frequency of being
behind QJ / KQ / AQ but realising equity vs the much wider one-pair-worse
+ overcard-air mass, (b) check-raise to ~5bb (3x the small c-bet) as a
pot-building line that charges BTN's draw-heavy continuing range,
denies equity to two-overcard floats, and protects against the turn-card
that improves BTN's two-overcard hands to top pair good kicker —
trading off the risk of being check-raise-jammed by sets / two-pair /
QJ that have hero crushed, and (c) donk-leading on the turn after a
flop check-call — i.e., committing to a check-call-then-lead-turn line
that develops the protection-and-thin-value plan over two streets rather
than one. v9-3way-on-59 model uncertainty is elevated because (i) Q-high
two-tone-mismatched + low-connected boards are a known mixing zone
where BB's optimal response to a 25% c-bet splits across check-call /
check-raise at non-trivial frequencies for medium-kicker top-pair
holdings; (ii) the kicker-dominated frequency band (QT vs QJ / KQ /
AQ) is precisely the equity range where check-raise EV is closest to
check-call EV — strong enough to want protection, weak enough that
many turn cards (J, K, A, any heart that pairs hero's backdoor) shift
the dominated-versus-dominating balance materially; (iii) the OOP
position complicates the check-call line because the turn brings a
binary scare-card vs brick split that the IP villain's range exploits
asymmetrically — BTN can barrel scare-cards thin while hero's check-call
range is condensed. Predictive entropy across the check-call /
check-raise / check-call-then-donk-turn action triple is high because
no single action dominates across plausible BTN c-bet range models.

**Solver sizing notes:** Flop bet sizes 25% (BTN c-bet) and the 3x
check-raise (~5bb total raise into the ~8bb pre-raise pot) are
solver-aligned. The donk-lead-turn branch uses the turn 33% size on
the next street. Hero's three-action candidate set covers the live
solver mix on this spot — no deviation from the solver-aligned grid.

---

## HU-5.4: Th8h combo draw on 9h7c2h two-tone, BB OOP — donk-lead vs check-call vs check-raise after BTN c-bet

**Marker:** CLOSE

**Target axis:** Axis HU-5 — Out-of-position decisions
**Hero cards:** Th/8h
**Board:** 9h 7c 2h
**Street:** Flop
**Hero position:** BB
**Primary villain position:** BTN
**Num opponents:** 1
**Pot:** 5.5bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** Draws (combo) — open-ended straight draw via
any 6 or J (8 outs to a straight: 6-7-8-9-T or 7-8-9-T-J) plus second-nut
flush draw (9 outs to a heart flush; A-of-hearts blocks the nut-FD on
hero's specific holding but hero's Th-8h still makes second-nut if the
runner is anything other than a pair-the-board heart). Net ~16 outs
raw, with substantial overlap-cleaned ~14-15 outs ≈ ~34-36% direct
turn-and-river equity vs typical BTN c-betting range. No made pair, but
two clean overcards (T and 8 are both above the 7-2 portion of the board;
T is also an overcard to the 9, 8 is below 9) that contribute thin
top-pair-improvement equity on T or 8 turns. Classify as draws (combo)
with subordinate overcard / pair-improvement backup; dominant feature
is the combined OESD + FD draw structure with a credible turn-barrel
plan on either draw completing.

**Action history:** 100bb effective. BTN (hero villain) opens 2.5bb, BB
(hero) calls. Flop 9h 7c 2h (two-tone hearts, 9-high, mid-low
disconnected on the bottom card but with OESD + FD interaction with
hero's specific Th8h holding). BB acts first OOP on a checked-into flop
with the combo draw.

**CLOSE rationale:** Three-action genuine entropy across the OOP-line
dimension before any c-bet has been made. The decision splits between
(a) donk-lead 1.4bb into 5.5bb (25% pot — solver-aligned flop small) as
a small-size lead that builds the pot at a favourable price for hero's
combined draw + overcard equity profile, denies BTN the option of
checking back air for a free turn realisation, and sets up a credible
turn-barrel on either draw completing or any overcard pairing the T/8,
(b) check-call BTN's expected c-bet — using hero's high realised-equity
draw to see the turn at a fair price while concealing range strength
and preserving BTN's bluff frequency on later streets, and (c)
check-raise to a multiple of BTN's c-bet as a pure semi-bluff that
leverages hero's combined fold equity (BTN's two-overcard / weak-pair
range folds to the check-raise) plus hero's substantial direct equity
when called (the OESD + FD combination retains ~34-36% equity even vs
BTN's check-raise-call value range of overpairs and 9x top-pair).
v9-3way-on-59 model uncertainty is elevated because (i) 9h7c2h two-tone
is a textbook mixing-zone texture for OOP draw lines where solver
outputs split donk-lead / check-call / check-raise across the combo-draw
bucket at non-trivial frequencies; (ii) the flush-draw blocker / second-nut
distinction (hero holds Th not Ah) shifts the optimal line marginally
because hero's range-vs-range fold-equity profile differs from a hero
with the nut-FD; (iii) the 100bb SPR creates a 3-street planning problem
where each of the three first-street lines opens distinct turn-and-river
trees — donk-lead-then-barrel, check-call-then-lead-turn, and
check-raise-then-jam-turn each have meaningfully different EV
distributions across the 8 turn-card classes (heart / 6 / J / T / 8 /
brick-overcard / brick-undercard / pair-the-board), and the relative
EV ranking across these lines is sensitive to the BTN range model.
Predictive entropy across the donk-lead / check-call / check-raise
action triple is high because no single action dominates across plausible
BTN c-bet range models.

**Solver sizing notes:** Donk-lead 25% (1.4bb into 5.5bb) is solver-aligned.
The check-call branch implies BTN's standard c-bet sizing of 25% or
66% (both solver-aligned). The check-raise branch uses 3x BTN's c-bet
as the standard OOP semi-bluff check-raise size. Hero's three-action
candidate set covers the live solver mix on this spot — no deviation
from the solver-aligned grid.

---

## HU-5.5: KsJc overcard air on 8h6d5h BB-favoured two-tone-connected, BB OOP — donk-lead vs check-fold vs check-call

**Marker:** CLOSE

**Target axis:** Axis HU-5 — Out-of-position decisions
**Hero cards:** Ks/Jc
**Board:** 8h 6d 5h
**Street:** Flop
**Hero position:** BB
**Primary villain position:** BTN
**Num opponents:** 1
**Pot:** 5.5bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** Air with two overcards + backdoors — no made
pair (K-J against 8-6-5, all three board cards below both hero cards), no
flush draw (board has hearts 8h/5h, hero holds Ks/Jc — zero hearts in
hand), no direct straight draw (K-J needs running 9-T or T-Q for any
straight; the 6-5 board structure gives no inside straight cards K-J can
reach in one). Two clean overcards (K and J each give 3 outs that pair
hero ahead of the 8-6-5 portion of the board on a one-card improvement,
~6 noisy overcard outs by the river) plus a backdoor straight via running
7-9 / T-9 / Q-T for broadway-to-mid completion (~3 backdoor combos, ~2-3%
backdoor equity). No flush blocker effect (hero holds zero hearts).
Classify as air with two-overcard + backdoor (subordinate); dominant
feature is no made hand, no direct draw on a board where BB's range is
strong but hero's specific KJ-offsuit combo is at the bottom of BB's
defend range on this texture.

**Action history:** 100bb effective. BTN (hero villain) opens 2.5bb, BB
(hero) calls. Flop 8h 6d 5h (two-tone hearts, 8-high, low-connected with
straight + flush draw equity for both ranges; BB's defend range contains
all the 87s / 76s / 65s / 54s / 64s / 53s / 33-88 combos that flop
made hands and draws at high frequency relative to BTN's open range,
which contains comparatively more high-card-air that misses entirely on
this texture). BB acts first OOP. Hero faces a checked-into flop with
overcard-air on the most-BB-favoured two-tone-connected board class.

**CLOSE rationale:** Three-action genuine entropy across the OOP-line
dimension before any c-bet has been made, with the unusual feature that
hero's specific hand is at the bottom of BB's defend range on a texture
where BB's overall range is strong. The decision splits between (a)
donk-lead 1.4bb into 5.5bb (25% pot — solver-aligned flop small) as a
range-balanced small lead that piggybacks on BB's range advantage on
this texture, applies fold equity against BTN's high-card-air that has
no continuing equity, and gives hero a credible turn-barrel plan on
overcard runouts (K, J turns) or straight-completing runouts that scare
BTN, (b) check-fold to BTN's expected c-bet — conceding the pot with a
no-equity holding rather than continuing on a board where hero's
specific combo can neither call profitably nor semi-bluff-raise with
fold equity that recovers the cost, and (c) check-call BTN's expected
c-bet — floating with the two-overcard + backdoor-straight equity to
realise improvement on K / J / 7 / 9 / T turn cards while concealing
BB's range strength and preserving BTN's bluff frequency on later
streets. v9-3way-on-59 model uncertainty is elevated because (i)
8-6-5-two-tone is a known BB-favoured texture where BB's optimal donk
frequency is meaningfully non-zero across a wide composition range
including weak draws and air-with-backdoors, and the marginal hand for
the donk bucket vs the check bucket is precisely two-overcard-air with
~6 noisy outs; (ii) the float-vs-fold decision after BTN's expected
c-bet sits at the equity threshold where any combination of overcard
outs + backdoor-straight outs + implied odds may or may not justify
the immediate price, and the solver's optimal frequency split for
KJo-no-FD specifically is sensitive to the exact c-bet sizing BTN
selects (25% vs 66%); (iii) the OOP position penalises the float line
because hero gives up positional information and faces a turn-barrel
decision tree with low realisation on most brick turns; (iv) the
donk-lead line trades the immediate fold equity against BTN's
range-c-bet-give-up frequency and is the rare case where OOP air
profitably leads on a texture the OOP player range-favours. Predictive
entropy across the donk-lead / check-fold / check-call action triple
is high because no single action dominates across plausible BTN c-bet
range models.

**Solver sizing notes:** Donk-lead 25% (1.4bb into 5.5bb) is solver-aligned.
The check-fold and check-call branches imply BTN's standard c-bet
sizings of 25% and 66% (both solver-aligned) on the next decision node.
Hero's three-action candidate set covers the live solver mix on this
spot — no deviation from the solver-aligned grid.

---
