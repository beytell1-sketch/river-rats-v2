# HU Axis 1 — Made Hand vs Villain Range (HU-1.1 to HU-1.5)

**Date:** 2026-05-10
**Status:** Design only — no labelling, no corpus changes
**Context:** Phase 1.5-D.1 HU reference set — 1 of 6 axis breakouts (per design memo §4.2)

## Axis intro

Axis HU-1 targets heads-up postflop spots where hero holds top-pair-or-better
(TP+ composition exclusively) versus villain's full HU range. The decision class
under test is **value-betting and protection vs slowplay/pot-control discipline**:
when does a made hand bet for value/protection, when does it check to induce or
slow the pot, and at what sizing. Villain ranges vary from capped (BB defend)
to uncapped (BTN open / 3-bet) so the hand strength composition triple stays
TP+ while the range-asymmetry signal varies meaningfully across the 5 hands.

All 5 hands are heads-up (`num_opponents: 1`). Mix covers BTN/BB/SB hero
positions, flop/turn/river streets, and 60bb / 100bb / 150bb effective stack
depths. Bet sizes are solver-aligned per `feedback_solver_aligned_sizing.md`
(flop 25%/66%, turn 33%/75%, river 33%/75%/150%); deviations are documented.
3 hands are CLOSE (model-uncertainty + poker-difficulty driven per
`feedback_close_hand_selection.md`); 2 hands are CANONICAL (uncontroversial
ground-truth anchors).

---

## Hand index

| ID | Marker | Street | Hero pos | Hand | Board | Decision class |
|----|--------|--------|----------|------|-------|----------------|
| HU-1.1 | CANONICAL | Flop | BTN | AhKs | Ad 8c 3h | C-bet TPTK on dry A-high |
| HU-1.2 | CANONICAL | River | BTN | 9d9c | 9h 7s 2c 4d Jh | Thin value bet on safe runout (set) |
| HU-1.3 | CLOSE | Flop | BTN | KhQd | Kc Tc 6d | TP good kicker, wet board sizing dilemma |
| HU-1.4 | CLOSE | Turn | SB | TsTd | 8h 5c 2d Tc | Overpair-turned-set facing IP probe |
| HU-1.5 | CLOSE | River | BB | AhJh | Jc 9c 5d 2s Qd | TPGK bluff-catch on scary completed runout |

---

## HU-1.1: AhKs TPTK BTN c-bet on dry A83r vs BB

**Marker:** CANONICAL

**Target axis:** Axis HU-1 — Made hand vs villain range
**Hero cards:** Ah/Ks
**Board:** Ad 8c 3h
**Street:** Flop
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 5.5bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** TP+ (top pair top kicker on A-high dry board)

**Action history:** 100bb effective. BTN (hero) opens 2.5bb, SB folds, BB calls.
Flop Ad 8c 3h (rainbow, disconnected, A-high). BB checks. Hero acts.

---

## HU-1.2: 9d9c flopped set, river thin value on safe runout, BTN vs BB

**Marker:** CANONICAL

**Target axis:** Axis HU-1 — Made hand vs villain range
**Hero cards:** 9d/9c
**Board:** 9h 7s 2c 4d Jh
**Street:** River
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 30bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** TP+ (set of nines; rivered J overcard but no flush
or one-card straight completes — board pair would be needed; J is the only
overcard since 9 paired)

**Action history:** 100bb effective. BTN (hero) opens 2.5bb, BB calls. Flop
9h 7s 2c: BB checks, hero bets 25% pot, BB calls. Turn 4d: BB checks, hero bets
33% pot, BB calls. River Jh: BB checks. Hero acts on river facing a checked,
range-capped BB. (J is the only overcard relative to the turn; flushes impossible
since no three same-suit cards landed.)

---

## HU-1.3: KhQd TP good kicker on wet KTcc6 flop, BTN c-bet sizing dilemma

**Marker:** CLOSE

**Target axis:** Axis HU-1 — Made hand vs villain range
**Hero cards:** Kh/Qd
**Board:** Kc Tc 6d
**Street:** Flop
**Hero position:** BTN
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 5.5bb
**Facing bet:** No
**Opener position:** BTN
**Bettor position:** None
**Hand strength composition:** TP+ (top pair good kicker, but board has flush
draw + straight-draw equity for villain caller; backdoor straight equity for
hero with QJ/J9-type runouts)

**Action history:** 100bb effective. BTN (hero) opens 2.5bb, SB folds, BB calls.
Flop Kc Tc 6d (two-tone, one-card straight draw via QJ/J9, gutshots via AQ/AJ).
BB checks. Hero acts.

**CLOSE rationale:** Three-action genuine entropy across the sizing-and-frequency
dimension. The decision splits between (a) bet 25% pot as a small range c-bet
that protects hero's range structure, denies BB's draw-heavy capped range
equity at a poor price, and supports a high c-bet frequency, (b) bet 66% pot
as a polarized sizing that extracts more value from worse Kx and second-pair
calls but folds out hero's natural bluff candidates and exposes hero to
check-raises by combo draws and sets, and (c) check-back to control vs
check-raise risk on the draw-heavy texture for the weakest TP+ combos in
hero's range. v9-3way-on-59 model uncertainty is elevated because (i) the
composition triple (TP+ with backdoor straight) sits at the sizing boundary
in solver outputs where small deviations in modelled villain check-raise
frequency tip the optimum between 25% and 66%; (ii) Kc Tc 6d two-tone
mid-connected boards are a known mixing-zone where the optimal solver size
splits across small/large/check at non-trivial frequencies for medium-strength
TP+ holdings with backdoor equity; (iii) the kicker-dominance asymmetry
(KQ ahead of K-rag worse-kicker top-pair, behind AK and KQ-set) interacts
with the draw-heavy continuing range in ways the v9-3way-on-59 model has
not seen at high training-distribution density. Predictive entropy across
the bet-25% / bet-66% / check-back action triple is high because no single
action dominates across plausible BB defend range models.

---

## HU-1.4: TsTd overpair-turned-set facing BB probe on Tc turn, hero SB

**Marker:** CLOSE

**Target axis:** Axis HU-1 — Made hand vs villain range
**Hero cards:** Ts/Td
**Board:** 8h 5c 2d Tc
**Street:** Turn
**Hero position:** SB
**Primary villain position:** BB
**Num opponents:** 1
**Pot:** 6bb
**Facing bet:** Yes
**To call:** 2bb
**Pot odds required:** 25.0%
**Opener position:** SB
**Bettor position:** BB
**Hand strength composition:** TP+ (turned set of tens — strongest possible TP+
holding given the 8-5-2 flop texture and the runout)

**Action history:** 60bb effective (short-stack HU dynamic). SB (hero) opens 3bb,
BB calls. Flop 8h 5c 2d (rainbow, dry, low). Hero checks as part of a
check-first range that includes overpairs and air; BB checks back. Turn Tc
(rainbow holds, 6bb pot): BB bets 2bb into 6bb (33% pot probe — solver-aligned
turn small size, characteristic of BB taking the betting lead after a flop
check-check on a turn that interacts with both ranges). Hero faces BB's bet
with the turned set.

**CLOSE rationale:** Two-action genuine entropy on this turn. The decision
splits between (a) flat-call (slowplay to keep BB's bluffs and weak-Tx
range live for a river barrel against a check-call line that conceals the
set) and (b) raise-of-the-existing-bet (immediate value and protection vs
the 9x / J-T-style equity that BB's betting range contains, building the
pot at a favourable SPR for a river jam). With 60bb effective and a turn
raise committing significant SPR, the choice between calling to induce a
third-street barrel and raising to set up a river jam against the strongest
portion of BB's bet range is genuinely contested. v9-3way-on-59 model
uncertainty is elevated because (i) BB's bet range on a T-completing turn
versus an SB who checked the flop carries a wide strength distribution
(turned trips, two-pair, 8x value, plus pure air bluffs from missed
overcards), (ii) the slowplay-vs-raise EV gap is sensitive to BB's
modelled triple-barrel frequency on river bricks vs scare-cards, which the
v9-3way-on-59 model has limited training signal for at 60bb-effective
short-stack HU dynamics, (iii) the SPR-management dimension at 60bb
effective creates a commit-now-vs-commit-later choice where each branch
opens distinct river decision trees with non-trivial EV variance.

**Solver sizing notes:** BB's bet size is 33% pot (solver-aligned turn small
size). Hero's response set (call vs raise) uses standard solver-aligned raise
sizing if raising — no deviation.

---

## HU-1.5: AhJh TPGK on J95-2-Q runout, BB faces BTN 75% river bet

**Marker:** CLOSE

**Target axis:** Axis HU-1 — Made hand vs villain range
**Hero cards:** Ah/Jh
**Board:** Jc 9c 5d 2s Qd
**Street:** River
**Hero position:** BB
**Primary villain position:** BTN
**Num opponents:** 1
**Pot:** 50bb
**Facing bet:** Yes
**To call:** 37.5bb
**Pot odds required:** 30.0%
**Opener position:** BTN
**Bettor position:** BTN
**Hand strength composition:** TP+ (top pair good kicker; A-high blocker into
villain's KT/AK straights; no flush possible since the c-suited turn brick was
the 2s and the river Qd does not complete a flush — only Jc/9c/Qd suit count
verified: clubs Jc + 9c only = 2 clubs, no flush)

**Action history:** 150bb effective (deep-stack HU dynamic). BTN opens 2.5bb,
BB (hero) defends call. Flop Jc 9c 5d (two-tone,
straight-draw heavy). BB checks, BTN bets 25% pot (solver-aligned flop small),
BB calls. Turn 2s (brick, removes one flush card option but still two clubs):
BB checks, BTN bets 33% pot, BB calls. River Qd (Q completes KT straight and
T8 straight; brings second diamond but no flush completes — only one diamond
on flop/turn). BTN bets 75% pot (37.5bb into 50bb). Hero faces a polarized
river bet with TPGK and an A-blocker.

**CLOSE rationale:** Two-action genuine entropy at the canonical bluff-catch
threshold. The decision splits between (a) call — hero's TPGK with A-high
blocker beats BTN's bluff frequency (busted backdoor flush attempts, A-high
give-ups, busted gutshots) and clears pot odds against the realistic
value-vs-bluff ratio if BTN's polarised triple-barrel range contains
~30-33% bluffs as solver outputs typically suggest, and (b) fold — hero
loses to the natural value range (KT/T8 straights, two-pair J9/Q9 if BTN's
range contains them, sets that triple-barrel for value), and if BTN's actual
bluff frequency falls below the 30% pot-odds threshold the call is -EV.
v9-3way-on-59 model uncertainty is elevated because (i) BTN's polarized
75% river bet on a Q-completing turn carries a value-to-bluff ratio that
sits near 30-33% bluffs in solver outputs, bracketing the pot-odds
threshold with high enough variance that the optimal action is mixed;
(ii) the Ah blocker reduces villain's AK/AcKc combos modestly (nudging
toward a call), but the Jh blocker on hero's own hand reduces villain's
J-bluffs and J-value in offsetting fashion, leaving the net blocker
effect ambiguous; (iii) Q-completing river runouts on J9-prefix flops
are a low-frequency line in the v9-3way-on-59 training distribution,
leaving the model uncertain across the call/fold threshold for
medium-strength bluff-catchers in this specific texture-and-action
combination. Predictive entropy across the call / fold action pair is
high because no single action dominates across plausible BTN
triple-barrel range models.

**Solver sizing notes:** Flop 25%, turn 33%, river 75% — all solver-aligned.

---
