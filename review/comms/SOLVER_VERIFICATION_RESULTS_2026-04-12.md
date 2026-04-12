---
date: 2026-04-12
from: Main terminal (logging owner's GTO Wizard results)
to: Review
re: Solver verification results for facing-bet test set (in progress)
status: IN PROGRESS
---

## Results so far (FB-04 through FB-17)

| FB | Expert label | Solver result | Solver sizing used | Match? | Notes |
|---|---|---|---|---|---|
| FB-04 | RAISE HIGH | CALL 55% / RAISE 45% | 50%→66% flop | MIXED | Accept either CALL or RAISE |
| FB-07 | CALL HIGH | CALL | BB bet limited to 25% pot (couldn't choose 66%) | YES | Adjust test set bet size to 25% to match solver options |
| FB-08 | CALL MEDIUM | CALL 57% / RAISE 43% | Had to choose AcKc (closest), 25% pot BB bet | MIXED | Accept either |
| FB-09 | RAISE MEDIUM | CALL/RAISE coin flip at 33% | Had to use 25% pot BB bet | MIXED | Accept either |
| FB-11 | CALL MEDIUM | CALL | 25% BB bet | YES | Confirmed |
| FB-14 | RAISE HIGH | CALL 41% / RAISE 40% (at 66% sizing) / RAISE 19% (at 33%) | BB 25% pot bet | **OVERRIDE TO RAISE** | Owner decision: oracle should raise. We don't choose raise sizing — oracle just needs to raise. RAISE label correct. |
| FB-15 | CALL MEDIUM (relabelled from FOLD) | **FOLD** | — | **REVERT TO FOLD** | Solver confirms original FOLD. Our sandwich→closing relabel was wrong. Revert. |
| FB-17 | RAISE HIGH | Mixing spot, favours CALL | — | **CHANGE TO CALL** | Consistent with FB-37 (CALL). Both FB-17 and FB-37 should be CALL. |
| FB-18 | — | — | — | **NEEDS DISCUSSION** | — |

## Key decisions

### FB-14: RAISE label confirmed (owner override)
Solver shows CALL 41% / RAISE 40% — essentially a coin flip. Owner
preference: the oracle should RAISE here. Since we don't control
raise sizing (the oracle picks the action, the sizing oracle picks
the size), RAISE is the correct label. The solver's near-equal
split validates that RAISE is not wrong even though CALL is also
acceptable.

### FB-15: REVERT to FOLD
The sandwich→closing relabel (FOLD→CALL) was incorrect. Solver
confirms FOLD. The original GTO Expert label was right. The
positional correction (BB is closing, not sandwiched) does not
change the action — the nut flush draw with no side equity is a
FOLD even with full information. Revert to FOLD HIGH.

### FB-17: CHANGE to CALL
Solver shows mixing spot favouring CALL with the nut straight.
Combined with FB-37 (also CALL), both situations should be CALL.
The cross-reference note on FB-17/FB-37 should be updated: both
are now CALL (harmonized).

## Sizing observation from owner
BB bet options in GTO Wizard were limited to 25% pot on several
flop hands (FB-07, FB-08, FB-09, FB-11). The 66% option was not
available for BB donk bets. This suggests the test set's 50% pot
sizing for BB donk bets is not realistic — solvers typically offer
25% or 66%, not 50%. Consider revising the test set's BB donk-bet
sizings to 25% pot to match solver options.

## Results continued (FB-18 through FB-27)

| FB | Expert label | Solver result | Solver sizing used | Match? | Notes |
|---|---|---|---|---|---|
| FB-18 | CALL MEDIUM | CALL 45% / RAISE 80%pot 37% / RAISE 40%pot 20% | 75% turn (mapped from 67%) | **CALL** (raise noted) | BB folds on flop (redesigned). Heads-up on turn. CALL is primary but raise works too. |
| FB-20 | — | — | — | — | (not yet verified) |
| FB-24 | RAISE MEDIUM | RAISE (solver confirms) | Had to choose A3cc for hero | **RAISE confirmed** | Adjust test set hero to Ac3c to match solver input |
| FB-25 | CALL MEDIUM | CALL (solver confirms) | Had to choose J7dd for hero | **CALL confirmed** | 7♦8♦ also calls. Adjust hero to Jd7d to match solver input |
| FB-27 | RAISE MEDIUM | CALL 70% / RAISE 30% | 25% flop (mapped from 33%) | **INCONCLUSIVE** | Too close, sizing mismatch may swing it. Solver does not help here — both actions valid. Need more hands like this with CORRECT solver sizing. |

## FB-18 redesign applied
BB now folds on the flop (to CO's c-bet), making the turn heads-up
(CO vs BTN). This fixes the "BB folds when not facing bet" error.
BTN now correctly closes action heads-up on the turn.

## FB-24 hero card adjustment
Solver required Ac3c (couldn't use exact As9s). Test set hero
adjusted to Ac3c. Label RAISE confirmed by solver.

## FB-25 hero card adjustment
Solver required Jd7d (couldn't use exact Qh7h). Test set hero
adjusted to Jd7d. CALL confirmed. Note: 7d8d also calls — the
suited connector structure matters more than the specific high card.

## FB-27 sizing problem — LOGGED FOR FUTURE ACTION
The CALL 70% / RAISE 30% split at 25% pot may not hold at 33% pot
(our actual sizing). At a larger bet, CALL becomes even more
favoured (more to risk on the raise), which would push this further
toward CALL. But at 25% pot, RAISE at 30% is still meaningful.

**Decision:** Mark as "accept either CALL or RAISE" for now. BUT:
this is exactly the kind of hand that needs redesigning with sizing
that matches what the solver can model. Log as a systemic issue —
see "Sizing redesign recommendation" below.

## Sizing redesign recommendation (from owner)

Multiple hands required sizing adjustments to match GTO Wizard's
available options. This is a systemic mismatch: our test set uses
33%/50%/67% pot bets while the solver offers 25%/66% (flop) and
33%/75% (turn/river). The owner notes that hands like FB-27 where
the solver result is inconclusive because of sizing mismatch need to
be redesigned with correct solver-compatible sizing.

**Recommendation for the NEXT iteration of this test set:**
- Flop bets: use 25% or 66% pot ONLY (match solver)
- Turn/river bets: use 33% or 75% pot ONLY (match solver)
- This eliminates the sizing mismatch entirely and makes solver
  verification clean

This does NOT block the current verification round — hands where the
solver gives a clear answer (>60% one action) are reliable even with
the mismatch. Only inconclusive hands (FB-27 type) need redoing.

## Updated label tracker (all results so far)

| Change | FB | Old → New |
|---|---|---|
| Confirmed | FB-04 | RAISE → accept either (mixed) |
| Confirmed | FB-07 | CALL |
| Confirmed | FB-08 | CALL → accept either (mixed) |
| Confirmed | FB-09 | RAISE → accept either (mixed) |
| Confirmed | FB-11 | CALL |
| Confirmed | FB-14 | RAISE (owner override) |
| **Reverted** | FB-15 | CALL MEDIUM → **FOLD HIGH** (solver confirms) |
| **Changed** | FB-17 | RAISE HIGH → **CALL** (solver favours call) |
| Confirmed | FB-18 | CALL (raise noted as option) — redesigned BB folds flop |
| **Adjusted** | FB-24 | RAISE confirmed — hero changed to Ac3c |
| **Adjusted** | FB-25 | CALL confirmed — hero changed to Jd7d |
| **Inconclusive** | FB-27 | Accept either CALL or RAISE — sizing mismatch, needs redo with correct sizing |
| Confirmed | FB-29 | CALL — BB bet 25%, hero calls from CO |
