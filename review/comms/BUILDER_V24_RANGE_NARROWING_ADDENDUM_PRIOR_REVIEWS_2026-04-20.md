---
date: 2026-04-20
from: Builder
to: Owner (+ GTO reviewer for Stage 3.5 context)
re: Stage 3.5 impact on prior-expert-reviewed hands
status: ADDENDUM to range-narrowing walkthrough — enumerates prior review hands
---

# Stage 3.5 impact on prior-expert-reviewed hands

Owner's question: did I pull in the plans from the other review
hands that were picked up previously? Short answer: I named d2410
and hand-waved at "other anchors"; I did not enumerate. This
addendum does.

For every hand that has already been through expert review, I
classify the Stage 3.5 impact:

- **HIGH** — prior-street action (bet or check) exists that
  Stage 3.5 would chain-narrow. Feature values WILL shift.
- **ZERO** — flop-only decision with no prior postflop action.
  Stage 3.5 does nothing; feature values unchanged.
- **MODERATE** — action history exists but the dominant narrowing
  direction is already applied by the current code (e.g., multi-
  street bet line). Minor shift.

## Category 1 — β panel re-label hands (v2.3.2 STOP investigation)

9 hands, 7 REGRESSIONS / 1 CORRECTION / 1 MIXED per the β panel
re-label (`review/label_batches_flipped/batch_01_result.txt`,
commit db222d3).

| Hand | Street | Prior postflop action | Stage 3.5 impact | β classification |
|---|---|---|---|---|
| **d2410_CO_turn** | turn | `flop: CO check` | **HIGH** — turn-decision after check-through; chain adds flop-check narrowing | REGRESSION (anchor) |
| **d0182_BTN_turn** | turn | `flop: BTN check` | **HIGH** — same shape | REGRESSION |
| **d8411_BB_turn** | turn | `flop: BB check` | **HIGH** — same shape | REGRESSION |
| **d2788_BTN_flop** | flop | none | **ZERO** | REGRESSION |
| **d4781_CO_flop** | flop | none | **ZERO** | REGRESSION |
| FB-04 (SW4d/Kc8c4d) | flop | N/A (FB test set) | **N/A** — FB hands have all-zero feature dict per β panel note; Stage 3.5 can't operate cleanly on synthetic zero-features rows. Separate issue. | MIXED |
| FB-24 (paired A-high river) | river | multi-street | **MODERATE** — re-extraction flows through Stage 3.5 | CORRECTION |
| FB-35 (nut FD + overcard turn) | turn | multi-street | **MODERATE** | REGRESSION |
| FB-40 (gutshot OOP flop) | flop | none | **ZERO** | REGRESSION |

**Critical read:** 3 of 7 β-panel REGRESSIONS (d2410, d0182,
d8411) are turn-decision-after-flop-check — the EXACT shape
Stage 3.5 changes. These were the 3 hands the β panel flagged as
"the class d2410 was designed to protect" and the "systematic
TPTK IP under-betting at compressed SPR."

**The line of reasoning this enables:** if Stage 3.5 causes
d2410/d0182/d8411 feature values to shift toward a more
action-conditioned range, does that shift push the model back
TOWARD the expert-label BET or does it leave things where v2.3.2
put them (wrong direction CHECK)? Either way we learn something:
- If model flips these to BET post-Stage 3.5 → **the feature was
  the missing signal all along. β panel right; Path C was a
  symptom, Stage 3.5 was the cause-level fix.**
- If model stays CHECK post-Stage 3.5 → **feature correctness
  alone insufficient; training-data class balance is also needed
  (Stage 4 re-label does this).** Both are plausible.

## Category 2 — v2.4 calibration anchors (seed 5)

| Anchor | Street | Prior postflop action | Stage 3.5 impact |
|---|---|---|---|
| d2410_CO_turn | turn | flop check | **HIGH** — see above |
| LITMUS_A4d_Qs5s7s_flop | flop | checked-to (villains pre-acted) | **ZERO at its street** (flop decisions ignore prior-street action chain because there is no prior street) |
| LITMUS_T5h_JJ2_flop | flop | checked-to | ZERO |
| LITMUS_AA_7h5d2c_flop | flop | checked-to | ZERO |
| LITMUS_KQ_KsTs3h_flop | flop | checked-to | ZERO |

**Only 1 of 5 anchors shifts with Stage 3.5.** The other 4 are
flop-only; they serve as CONTROL anchors that should NOT
regress. If d2410 flips and the other 4 stay passing, Stage 3.5
is isolated correctly. If any flop anchor flips, we've
accidentally broken something unrelated — STOP.

## Category 3 — v2.4 generalization sweep (20 flop cases)

All 20 are flop decisions across HU + 3-way, varied hero/texture/
position. 18 passed CHECK (94.7%), 1 FAIL (SW02), 1 predicate-
dropped (SW04).

**Stage 3.5 impact on all 20: ZERO.** Flop decisions with no
prior postflop action in the spec. These serve as a secondary
control set — sweep pass-rate should NOT regress from 94.7%
after Stage 3.5.

## Category 4 — Playtest findings (v2.3 → v2.3.1)

| Finding | Street | Prior postflop action | Stage 3.5 impact |
|---|---|---|---|
| PLAYTEST_FINDING_002 (A4d/Qs5s7s flop, checked-to BTN IP) | flop | villains pre-acted (same-street check) | Current code: facing_bet=0 → no narrow. Stage 3.5: villains pre-acted on SAME street, not prior street. `narrow_by_action_history` as spec'd only chains per street's ACTIONS — same-street pre-hero checks are not yet "historical." | **LOW** — not chained unless we extend to same-street pre-hero actions |
| T5h/JJ2 flop, checked-to | flop | same | **LOW** |

**Spec caveat.** My Stage 3.5 plan walks action_history street-by-
street. On a FLOP decision, the loop finds the flop street and
can include villain's SAME-street check if villain acted before
hero. That's a spec detail worth the GTO reviewer's input — is
"villain's same-street pre-hero check" part of the chain or
separate?

If yes: Stage 3.5 narrows the flop range by flop-check for
checked-to IP decisions. ALL 5 flop anchors gain some narrowing.
Could cause anchor shift. Need to audit.

If no: same-street pre-hero actions are excluded from the chain,
and the 4 flop anchors stay ZERO-impact.

**Flagging for GTO review decision.** Consistency argument says
yes (villain's check IS a historical action the moment it
happened); pragmatic argument says no (preserves the 4 anchor
passes as controls).

## Category 5 — Playtest logs (live data)

| Hand | Session | Street | Action history | Stage 3.5 impact |
|---|---|---|---|---|
| H_a423db11 (re-confirmed earlier) | 4388e6e3 | flop → turn → river | flop BB BET, turn BB BET, river BB BET | **HIGH on turn + river decisions** — chained narrowing runs the bet-chain |
| H_8dfb6ef8 | 77221d98 | flop → turn → river | flop BB BET, turn BB CHECK, turn BTN BET, turn BB CALL, river BB BET | **HIGH on river** — chain must handle BET-CHECK-CALL-BET sequence; this is exactly the CALL-narrow case |
| H_d9edab5d | 4dc31ce7 | river | flop ?, turn all-check, river BB check + CO bet | **HIGH** on river but **features are empty** in that session's log (logging bug). Cannot empirically validate. |

**H_8dfb6ef8 is the clearest test case.** Post-Stage 3.5, it
chains:
1. Flop: BB bet → apply `narrow_to_betting_range` for flop
2. Turn: BB checked → apply `narrow_to_checking_range` for turn
3. Turn: BB called → apply `narrow_to_continuing_range` for turn
   (the CALL-narrow question)
4. River: BB bet → apply `narrow_to_betting_range` for river

This hand exercises all 4 action-types in a single chain. GTO
reviewer should use this as a primary mental test case.

## Category 6 — Owner's conceptual blocker scenario

> "Villain bets, we have mid pair, two spades on the board and we hold one
> (a Jack)" — from 2026-04-18 session

- Street: not specified (flop or turn implied)
- Prior action: villain's current-street BET is the only action
  mentioned; no prior-street chain in scope
- Stage 3.5 impact: **MODERATE** — if this is a turn decision,
  prior-street narrowing enters the chain; if flop, little
  changes

The ticket for this scenario
(`TICKET_BLOCKER_DIRECTION_DEFENSIVE_2026-04-18`) is separate
scope and handled by the 4 new v2.4 P1 features. Stage 3.5
improves the VILLAIN RANGE those block-pct features iterate
over, so both tickets benefit from Stage 3.5 independently.

## Category 7 — Other v2.4 feature plans (P1 GTO reviews)

From the 3 GTO reviewer outputs:

- `nut_flush_block` review — no range-narrowing concern; boolean
  derived from board + hero only.
- `flush_draw_block_pct` review — reviewer noted "features
  produce ZERO training signal until KB §1.9 + v3.2 prompt +
  re-label." This is a SEPARATE dependency chain (prompt →
  panel attention → label), not range-narrowing. Stage 3.5 is
  orthogonal but necessary: the block-pct feature iterates
  villain range, and under Stage 3.5 that range becomes
  action-correct. So the feature's OUTPUT quality depends on
  Stage 3.5 even if its WIRING doesn't.
- `nut_made_block_pct` review — same.

## Summary — where Stage 3.5 changes outcomes

**HIGH impact class (shifts expected):**
- d2410, d0182, d8411 (β panel TPTK turn-after-flop-check)
- H_a423db11, H_8dfb6ef8 (multi-street playtest traces)
- All turn/river decisions in the ~550 remaining training rows
  with multi-street action history

**ZERO impact class (controls):**
- 4 of 5 calibration anchors (all flop seeds)
- 20 generalization sweep cases (all flop)
- β panel REGRESSIONS d2788, d4781, FB-40 (flop-only)

**Decision gate for Stage 3.5 ship:**
- d2410 re-run: if BET is restored at HIGH confidence →
  Stage 3.5 has done work cleanly; ship.
- 4 flop anchors must stay passing (no regression from the
  fix).
- Sweep pass-rate must stay ≥85% (matches the broader sweep
  discipline).

## Plans I did NOT carry forward into Stage 3.5 spec

Flagging explicitly so they don't slip:

1. **TICKET_HAND_EVALUATOR_DRAW_SEMANTICS** — `_check_straight_draw`
   board-only bug. Independent scope; not bundled into Stage 3.5.
   Can land in parallel or after.
2. **TICKET_BLOCKER_DIRECTION_DEFENSIVE** — closed by v2.4 P1
   Stage 1-2 (features + KB). No additional work needed.
3. **Teaching recentering walkthrough** — owner-paced; separate
   from Stage 3.5.
4. **Flush_block_pct retirement A/B** — deferred per directive.
   Stage 3.5 changes the range-narrowing; retirement decision
   comes after Stage 5 retrain on new range.

## Action for owner

Confirm addendum is complete (no hand you wanted enumerated that I
missed), and I'll dispatch the GTO reviewer on the full set:

- `BUILDER_V24_RANGE_NARROWING_EXPERT_REVIEW_2026-04-20.md`
  (IS/SHOULD/PLAN/CAN'T doc)
- `BUILDER_V24_RANGE_NARROWING_WALKTHROUGH_2026-04-20.md`
  (per-street mechanics + automation honesty)
- THIS doc (prior-review hands impact map)

Reviewer gets the A/B/C CALL-narrow question + the same-street
pre-hero-action question + the full expert-reviewed-hand catalog
to reason against.
