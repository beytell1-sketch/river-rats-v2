# Reviewer Findings — Phase 1.5-D.1 HU Reference Set Design

**Date:** 2026-05-10
**From:** REVIEWER (independent design-stage)
**To:** BUILDER + orchestrator
**Re:** Phase 1.5-D.1 HU reference set — methodology compliance audit on the
6 per-axis spec files (HU-1..HU-6, 5 hands each = 30 hands total)

Files audited:
- design/hu_reference_set/HU_AXIS_1_MADE_HAND.md
- design/hu_reference_set/HU_AXIS_2_DRAWING.md
- design/hu_reference_set/HU_AXIS_3_AIR_BACKDOORS.md
- design/hu_reference_set/HU_AXIS_4_PFA_POSTFLOP.md
- design/hu_reference_set/HU_AXIS_5_OOP_DECISIONS.md
- design/hu_reference_set/HU_AXIS_6_RIVER_PRECISION.md

Binding spec read: PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md §4.2 +
MAIN_TERMINAL_PHASE15D1_HU_REFERENCE_SET_DESIGN_DISPATCH_2026-05-09.md.

---

## Checklist results

### 1. 30 hands total (6 axes × 5) — PASS

Each file contains exactly 5 hand entries (HU-x.1 through HU-x.5). Total
= 30 hands. Confirmed via the hand-index tables and per-hand sections in
all 6 files.

### 2. 3 CLOSE + 2 CANONICAL per axis (18 close + 12 canonical) — PASS

Every file follows the convention HU-x.1 = CANONICAL, HU-x.2 = CANONICAL,
HU-x.3..x.5 = CLOSE. Counts verified per hand-index table.

### 3. HU only (Num opponents: 1) — PASS

Spot-checked 3 hands per axis (18 total): HU-1.1, 1.3, 1.5; HU-2.1, 2.3,
2.5; HU-3.1, 3.3, 3.5; HU-4.1, 4.3, 4.5; HU-5.1, 5.3, 5.5; HU-6.1, 6.3,
6.5. All carry `Num opponents: 1`. Action histories all describe HU-only
preflop trees (BTN open + SB fold + BB call, or SB open + BB call).

### 4. Card collision check (cross-file hero hands) — FAIL

Six suit-rotation collisions detected (per dispatch §"suit-rotation
matches DO count as a collision flag"):

| Hand class | First hand | Second hand |
|------------|------------|-------------|
| AKo | HU-1.1 (AhKs) | HU-4.5 (AsKd) |
| KQo | HU-1.3 (KhQd) | HU-6.4 (KdQc) |
| 99 | HU-1.2 (9d9c) | HU-6.5 (9s9d) |
| J9s | HU-2.3 (Js9s) | HU-5.4 (Jd9d) |
| 65s | HU-2.4 (6c5c) | HU-5.2 (6h5h) |
| ATs | HU-4.3 (AcTc) | HU-6.3 (AsTs) |

Each pair is the same hand class with a different suit assignment, which
the dispatch explicitly flags as a collision (example given: AhKs vs
AsKh). 6 of 30 hands (20%) are duplicated at the hand-class level. This
breaks the cross-axis-hygiene invariants asserted in the axis intros of
HU-2 through HU-6 ("hero hands ... do not collide with HU-1 ...").

### 5. Board overlap check (cross-file flops) — PASS

Listed all 30 flops (first 3 board cards). No two hands share an exact
3-card flop. Several pairs share rank structure with different suits
(e.g., HU-2.4 8c7d4h vs HU-1.4 8h5c2d are different boards), but per
dispatch criterion that boards differing only in suit are NOT collisions,
no flag is raised here.

### 6. Hand-on-board collision (per hand) — PASS

Spot-checked all river-runout hands (HU-1.2, 1.5, 3.5, 6.1, 6.2, 6.3,
6.4, 6.5) and selected flop/turn hands. No hero card appears on any
hand's board. Notably HU-6.1 (KhKs hero / Kc 7s 4h 2c Kd board) uses
the two non-hero kings on the board, which is internally consistent and
required for the quad-kings setup.

### 7. Solver-aligned bet sizes — PASS_WITH_MINOR_WARN

All bet sizes scanned across the 30 hands sit on the solver-aligned
grid (flop 25%/66%, turn 33%/75%, river 33%/75%/150%). Every deviation
from the simple grid is documented:
- HU-2.4 jam-sizing (constrained by SPR ~1.3 at 60bb effective) is
  documented as deviation justified.
- HU-5.1 check-raise sizing 3x the bet is described as standard
  solver-aligned check-raise sizing.

WARN (HU-1.4 internal arithmetic): The HU-1.4 turn pot is stated as
"12bb" with BB leading "4bb into 12bb (33% pot)". With SB open 3bb +
BB call + flop check-check, the flop and turn pot should be 6bb, not
12bb. The 33% sizing math (4/12) is internally consistent within the
stated pot but the pot value contradicts the documented action history.
This is an arithmetic/bookkeeping inconsistency, not a sizing-grid
violation. Recommend the builder reconcile pot to 6bb (turn lead would
then be ~2bb to keep 33%) or adjust action history to produce a 12bb
turn pot.

### 8. Terminology compliance (raise / bet / open / lead) — WARN

One terminology misuse detected:

- HU-1.4 uses "BB leads 4bb" on the turn after a flop check-check, but
  in HU postflop BB is the IP player (SB acts first as OOP). After SB
  checks, BB betting is a regular IP bet, not a "lead" / "donk-lead."
  Per `feedback_terminology_raise_vs_bet.md`, "lead" / "donk-lead" is
  appropriate for OOP first-in only. Should read "BB bets 4bb."

All other usage scanned is compliant:
- "open" used only for preflop opener (BTN open, SB open) — compliant
  across all files.
- "bet" used for first postflop bet (e.g., "BTN bets 3.6bb (66% pot)")
  — compliant.
- "raise" used for raise-of-existing-bet (HU-2.4 BB check-raises;
  HU-5.1 BB check-raises; HU-1.4 hero "raise-of-the-existing-bet") —
  compliant.
- "donk-lead" / "lead" used correctly in HU-3.5 (BB river lead-into-IP),
  HU-5.2 (BB flop donk-lead OOP first-in), HU-5.4 (BB flop donk-lead
  OOP first-in), HU-5.5 (BB flop donk-lead OOP first-in), HU-6.5 (BB
  river lead-overbet OOP first-in).

### 9. Composition triple per axis — PASS

- HU-1: All 5 hands TP+ (TPTK / set / TPGK / set / TPGK). Compliant.
- HU-2: All 5 hands draws (NFD+overcards / OESD / FD+gutshot / combo /
  FD+gutshot+A-overcard). Compliant.
- HU-3: All 5 hands air (pure air / pure air / two-overcard air /
  one-overcard+BDSD air / busted air with A-blocker). Compliant.
- HU-4: Mixed across TP+ (4.1 JJ overpair, 4.3 ATs TPTK), air (4.2 44
  underpair, 4.5 AKo two-overcard backdoor air), and draws (4.4 QJs
  combo). Per dispatch, mixed is allowed for HU-4/5/6.
- HU-5: Mixed across TP+ (5.1 set, 5.2 two-pair, 5.3 TP-medium-kicker),
  draws (5.4 combo), air (5.5 KJo two-overcard). Compliant.
- HU-6: Mostly TP+ (6.1 quads, 6.3 TPTK, 6.4 TPGK, 6.5 nut straight)
  with one air (6.2 8d8c busted underpair). Per dispatch, mixed allowed.

Each hand explicitly states its composition class in the
`Hand strength composition:` field, with detailed reasoning. Compliant
with `feedback_preflop_geometry_vs_postflop_composition.md`.

### 10. CLOSE rationale present — PASS_WITH_MINOR_WARN

All 18 CLOSE hands have a `CLOSE rationale:` block of 1-3+ sentences
citing both model uncertainty and poker difficulty.

WARN (HU-1.3, 1.4, 1.5, 2.3, 2.4, 2.5 = 6 of 18): These cite "predictive
entropy" / "model uncertainty" with strong poker-difficulty reasoning,
but do not explicitly name the v9-3way-on-59 model. The remaining 12
CLOSE hands (HU-3.3..3.5, HU-4.3..4.5, HU-5.3..5.5, HU-6.3..6.5) all
explicitly cite "v9-3way-on-59 model uncertainty is elevated because
..." with a numbered (i)/(ii)/(iii) breakdown of the contributing
factors. Recommend the builder upgrade HU-1 and HU-2 CLOSE rationales
to the explicit v9-3way-on-59 model-uncertainty citation pattern used
in HU-3 through HU-6 for stylistic and methodological consistency.

---

## Final verdict: APPROVE_WITH_FINDINGS

The 30-hand HU reference set is methodologically sound on counts,
composition triples, board separation, hand-on-board hygiene, bet-size
solver-alignment, and (largely) terminology. Two material findings
(item 4 hand-class collisions; item 7 HU-1.4 pot arithmetic) and one
stylistic-consistency warning (item 8 + item 10) require fixes before
the set proceeds to labelling.

## Itemised fixes

**MUST-FIX (blocking before labelling):**

1. **Resolve 6 hand-class collisions** (item 4). Re-roll the second
   occurrence of each duplicated hand class to a non-duplicated combo:
   - HU-4.5 AsKd → re-roll to a non-AKo two-overcard backdoor-air combo
     (e.g., AcQs, KdJh) that preserves the axis HU-4 delayed-c-bet
     decision class
   - HU-6.4 KdQc → re-roll to a non-KQo TPGK on Q-high busted-FD river
     combo (e.g., KsQh on a different-suit Q-high board, or AhQs)
   - HU-6.5 9s9d → re-roll to a non-99 nut-straight-on-flush-completing
     combo (e.g., TsTd on an 8h-7c-6s-2d-9d runout, or another 9x
     non-pair holding that makes the same straight)
   - HU-5.4 Jd9d → re-roll to a non-J9s combo-draw OOP combo
     (e.g., Th8h on a Jd-7c-2s board with FD+OESD)
   - HU-5.2 6h5h → re-roll to a non-65s flopped-two-pair combo
     (e.g., 7h6h on a 7c-6s-4d board, or 8s7s on a 8c-7d-3h board)
   - HU-4.3 AcTc → re-roll to a non-ATs TPTK two-tone-wet SB-open
     combo (e.g., AdJd on Jc-7s-5d, or KsTs on Td-7d-5s)

   After re-rolls, also update the cross-axis-hygiene assertions in the
   axis intros of HU-2 through HU-6 to reflect the new card sets.

2. **HU-1.4 pot arithmetic** (item 7). With 60bb effective, SB open
   3bb, BB call, flop check-check, the turn pot is 6bb not 12bb. Either
   (a) reduce the turn-pot field to 6bb and reduce BB's lead from 4bb
   to 2bb to preserve 33% sizing, or (b) re-author the action history
   to produce a 12bb turn pot (e.g., flop bet-call exchange that adds
   to the pot before the turn). Also reconcile the `To call: 4bb` and
   `Pot odds required: 25.0%` fields downstream.

**SHOULD-FIX (non-blocking but recommended):**

3. **HU-1.4 terminology** (item 8). Replace "BB leads 4bb into 12bb"
   with "BB bets 4bb into 12bb" (or the corrected pot per fix #2). BB
   is IP postflop in HU; the action after SB checks is a bet, not a
   lead. Also reconsider "Hero checks back as part of a check-back
   range that includes overpairs and air" in the same hand — SB
   checking first-in is "checks", not "checks back" (only IP can
   check back).

4. **HU-1 + HU-2 CLOSE rationales** (item 10). Upgrade the 6 CLOSE
   rationales in HU-1.3, 1.4, 1.5, 2.3, 2.4, 2.5 to the explicit
   v9-3way-on-59-model-uncertainty citation pattern used uniformly
   in HU-3 through HU-6. Stylistic-consistency only — the substantive
   poker reasoning is already present.

---

End of findings.
