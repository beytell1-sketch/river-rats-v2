---
date: 2026-05-22
from: ARCHITECT (parallel 5-way reference workstream)
to: Solver verifier + Owner arbitrator
re: Verification rubric for 10-hand 5-way reference set (MW-51..MW-60)
status: DRAFT — verification protocol; defines solver-run setup + expected ranges + owner-arbitration criteria per hand
companion: DRAFT_DESIGN_MEMO_5WAY_REFERENCE_SET_2026-05-22.md + DRAFT_5WAY_REFERENCE_PILOT_10HAND_2026-05-22.jsonl
---

# 5-way reference verification rubric

## Protocol overview

For each MW-51..MW-60:

1. **Solver run path**: set up the spot in PioSolver / GTO Wizard / equivalent with the specified ranges + sizing tree + stack depth.
2. **Solver query**: get the action-frequency distribution at hero's decision node.
3. **Expected output**: architect's prediction (dominant action + frequency mix).
4. **Arbitration criteria**: if solver disagrees with architect, owner decides.

## Global solver setup

- **Game**: 6-max NLHE, 100bb effective (all 10 hands; no deep-stack variants)
- **Preflop ranges**: solver-aligned RFI + cold-call + 3-bet ranges (e.g., GTO Wizard 6-max ranges)
- **Sizing tree per memory `feedback_solver_aligned_sizing.md`**:
  - Flop: 25% / 66% bets (b25, b66)
  - Turn: 33% / 75% bets
  - River: 33% / 75% / 150% bets
  - Raise sizes: 3x bet (default), 4x (overraise)
- **Rake**: per solver default (typically 5% cap 2bb) or rake-free if testing pure GTO
- **Per-hand**: cold-callers' calling ranges are solved jointly; opener's range is restricted to RFI

## Per-hand verification

### MW-51 — K9 IP BTN closing 5-way, K72r facing 25% c-bet

- **Solver tree**: UTG RFI → MP cold-call → CO cold-call → BTN cold-call → BB cold-call. Flop K72r. CO bets 25%. Solve for BTN at decision.
- **Architect's expected output**: CALL > 70%, RAISE 0-10%, FOLD 20-30%
- **Architect's lean**: CALL
- **Solver disagreement triggers**:
  - If solver FOLD > 50%: range-narrowing on CO's c-bet is stronger than estimated → owner re-evaluates K9 strength in 5-way
  - If solver RAISE > 20%: protection-value-mix more aggressive than estimated → owner verifies
- **Owner arbitration criteria**: if solver disagrees by >30pp on top action, owner re-reads the hand with solver output + chooses canonical label (the modal solver action is default; owner override permitted if owner identifies a pipeline-level reason for solver mismatch).

### MW-52 — KK facing BTN squeeze 5-way (multi-flat 3-bet pot)

- **Solver tree**: UTG RFI → MP flat → CO flat → BTN 3-bet to 13bb → SB folds → BB cold-flat 13 → UTG flat 13 → MP flat 13. Hero(CO) at decision.
- **Architect's expected output**: RAISE (4-bet) > 90%, CALL 5-10%, FOLD 0%
- **Architect's lean**: RAISE to ~36bb
- **Solver disagreement triggers**:
  - If solver CALL > 30%: stack-extraction line favored more than 4-bet → architect's sizing estimate revisited
  - If solver 4-bet sizing differs (e.g., shove vs 36bb): note solver size; sizing-only disagreement is NOT label-flip
- **Owner arbitration criteria**: action label (RAISE vs CALL) is the canonical label; sizing solver-aligned but owner accepts solver's exact sizing.

### MW-53 — A5s SB squeeze closing-action

- **Solver tree**: UTG/MP fold → HJ RFI → CO flat → BTN flat. Hero(SB) at decision.
- **Architect's expected output**: RAISE (squeeze) ~70-85%, CALL 10-25%, FOLD 5-10%
- **Architect's lean**: RAISE to ~14bb
- **Solver disagreement triggers**:
  - If solver CALL > 50%: A5s call-from-SB-OOP-in-5-way is favored over squeeze → architect's squeeze-EV assumption revisited
  - If solver FOLD > 25%: A5s is below squeeze threshold in solver → owner evaluates
- **Owner arbitration criteria**: A5s is canonically a squeeze candidate in solvers; if solver favors CALL, owner reviews equity-realization assumptions.

### MW-54 — Nut FD + gutshot SB OOP, bet-and-call faced 5-way

- **Solver tree**: UTG RFI → MP flat → CO flat → BTN flat → SB flat → BB fold. Flop Jh7h2c. SB check, UTG check, MP check, CO bets 32%, BTN calls. SB at decision.
- **Architect's expected output**: RAISE (check-raise) 50-70%, CALL 30-50%, FOLD 0%
- **Architect's lean**: RAISE (check-raise to ~16bb), MIX with CALL acceptable
- **Solver disagreement triggers**:
  - If solver pure CALL (>80%): OOP + 2 villains un-acted dominates fold-equity calculus → CALL is canonical label
  - If solver pure RAISE (>80%): semi-bluff dominance stronger than mix estimate
- **Owner arbitration criteria**: if solver MIX (40-60% RAISE / 40-60% CALL), owner picks the modal action; both are defensible labels. Architect leans RAISE but accepts CALL as canonical if solver favors it.

### MW-55 — Top-two-pair UTG facing BTN turn float-bet, Q83r-J

- **Solver tree**: UTG RFI → MP flat → CO flat → BTN flat → SB fold → BB flat. Flop Q83r checks-through 5-way. Turn J. UTG/MP/CO check; BTN bets 65%. UTG at decision.
- **Architect's expected output**: RAISE (check-raise) 60-80%, CALL 20-40%, FOLD 0%
- **Architect's lean**: RAISE to ~28bb (3.5x BTN's bet)
- **Solver disagreement triggers**:
  - If solver pure CALL (>80%): keeping MP/CO in for river extraction is favored over raise-now
  - If solver RAISE sizing differs (smaller, e.g., 2.5x): solver-aligned sizing override
- **Owner arbitration criteria**: top-two-pair on coordinated turn is the strongest hand class in this spot; the choice is RAISE vs CALL trap. Owner picks modal solver action.

### MW-56 — A4s BB closing 4 cold-callers + open

- **Solver tree**: UTG RFI → MP flat → CO flat → BTN flat → SB fold → BB at decision.
- **Architect's expected output**: CALL > 95%, RAISE 0-5%, FOLD 0%
- **Architect's lean**: CALL
- **Solver disagreement triggers**:
  - If solver RAISE > 20%: BB squeeze frequency vs 4 cold-callers more aggressive than estimated → architect reconsiders implied-odds vs squeeze EV
  - If solver FOLD > 5%: pot odds calculation error or unusual range constraint
- **Owner arbitration criteria**: A4s closing at 11.5% pot odds is canonically CALL. If solver disagrees, sanity-check the solver setup.

### MW-57 — TT IP BTN turn no-bet on 884-2

- **Solver tree**: UTG RFI → MP flat → CO flat → BTN flat → SB fold → BB flat. Flop 884r checked through. Turn 2h checked to BTN. BTN at decision (no bet faced; CHECK or BET choices).
- **Architect's expected output**: CHECK 70-90%, BET 10-30% (small thin-bet)
- **Architect's lean**: CHECK
- **Solver disagreement triggers**:
  - If solver BET > 50%: thin-value vs capped ranges more lucrative than estimated; sizing matters (25% likely)
  - If solver CHECK ~100%: pure pot-control; architect's mix overestimated
- **Owner arbitration criteria**: CHECK is canonical for TT on paired-board checked-through; thin-bet mix is reasonable solver detail but not label-flipping.

### MW-58 — Bottom set MP facing flop bet-raise chain on T98ss

- **Solver tree**: UTG RFI → MP flat → CO flat → BTN flat → SB fold → BB flat. Flop Ts9d8s. BB donk-leads 4bb, UTG raises to 14bb. Hero(MP) at decision; CO/BTN behind.
- **Architect's expected output**: CALL 50-75%, RAISE (3-bet) 20-40%, FOLD 0-10%
- **Architect's lean**: CALL
- **Solver disagreement triggers**:
  - If solver RAISE > 60%: 3-betting bottom set in 5-way more aggressive than estimated; protection vs straights drives RAISE
  - If solver FOLD > 25%: bottom set facing donk-raise chain is too dominated; owner re-evaluates set strength on T98ss
- **Owner arbitration criteria**: CALL vs RAISE mix; owner picks modal action. FOLD would be surprising and require re-analysis.

### MW-59 — TT under-pair SB on monotone-spade river facing overbet + cold-call

- **Solver tree**: UTG RFI → MP flat → CO flat → BTN flat → SB flat → BB fold. Flop 7s4s2c checked through. Turn 8h checked through. River 5s. SB checks, UTG checks, MP checks, CO bets 140% pot, BTN calls. SB at decision.
- **Architect's expected output**: FOLD > 95%, CALL < 5%, RAISE 0%
- **Architect's lean**: FOLD
- **Solver disagreement triggers**:
  - If solver CALL > 20%: bluff-catch frequency vs polarized overbet underestimated; rare in monotone-river structure
- **Owner arbitration criteria**: FOLD is canonical for under-pair vs polarized overbet + cold-call on monotone river.

### MW-60 — Two-pair A's+5's BB on Ad5d2c-8h facing bet-call-raise chain

- **Solver tree**: UTG RFI → MP flat → CO flat → BTN flat → SB fold → BB flat. Flop Ad5d2c checked through. Turn 8h. BB checks, UTG checks, MP bets 33%, CO calls, BTN raises 3x. BB at decision; UTG/MP/CO still in pot.
- **Architect's expected output**: FOLD > 90%, CALL < 10%, RAISE 0%
- **Architect's lean**: FOLD
- **Solver disagreement triggers**:
  - If solver CALL > 25%: reverse-implied-odds underestimated; A's+5's has more equity vs bet-call-raise chain than expected
  - Note: A5 has improvement outs (boats up on A/5) but board-pair-8/2 + 4th-diamond brick equity
- **Owner arbitration criteria**: FOLD is canonical for two-pair-bottom-kicker vs multi-villain action chain. CALL surprise → owner re-evaluates BTN's raise range composition.

## Overall arbitration framework

For each disagreement between architect and solver:

1. **Solver run defines the action distribution** (frequency mix at decision node)
2. **Modal action becomes the default label** (top-frequency action in solver output)
3. **Owner override permitted** if owner identifies:
   - Pipeline-level reason for solver mismatch (e.g., range setup error, sizing tree mismatch)
   - GTO-reversal-style spot (per MW-30, MW-46 precedent — solver-equity vs realistic-deployment-equity divergence)
   - Action that solver tags as <5% mix but is canonical "stress test" answer for v9-5way training

4. **Final label written to production JSONL** with:
   - `expected_action` = canonical label
   - `expected_size_bb` = solver-aligned size (if bet/raise)
   - `rationale_summary` = combined architect reasoning + solver verification result
   - `verification_path` = "solver: <tool> + owner: <arbitration_note>"

## Verification queue order

Recommended verification sequence:

1. **HIGH-confidence hands first** (MW-52, MW-53, MW-56, MW-59, MW-60): quick sanity checks; expected to PASS
2. **MEDIUM-HIGH next** (MW-55, MW-57): action class likely confirmed; verify sizing
3. **MEDIUM last** (MW-51, MW-54, MW-58): potential owner-arbitration spots; review more carefully

If 9+/10 confirm architect's lean: ship the reference set with confidence.
If 5-8/10 confirm: owner reviews the disagreements + decides keep / re-design.
If <5/10 confirm: architect's GTO reasoning is systematically off; flag the workstream + revise.

## References

- Design memo: `review/comms/DRAFT_DESIGN_MEMO_5WAY_REFERENCE_SET_2026-05-22.md`
- JSONL spec: `review/comms/DRAFT_5WAY_REFERENCE_PILOT_10HAND_2026-05-22.jsonl`
- Memory: `feedback_solver_vs_expert_labels.md`, `feedback_solver_aligned_sizing.md`, `feedback_solver_verification_queue.md`, `feedback_solver_findings.md`, `reference_corrections.md`
- Existing reference set precedents: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` (MW-30, MW-46 GTO-override examples)

---

**STATUS**: DRAFT — verification protocol ready for solver + owner verification cycle. All 10 hands have defined solver setup + expected output + arbitration criteria.
