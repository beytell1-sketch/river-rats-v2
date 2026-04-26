---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed)
re: PR #12 (Task 2 Protocol C v1.0) — APPROVE-WITH-NITS verdict; fix-forward to v1.0.1 required per quality-default discipline (raise-sizing taxonomy aligns to solver memory)
status: DIRECTIVE — 1 MEDIUM-severity finding (raise-sizing); same pattern as Task 1.1 (PR #10 → PR #11); fix-forward branch stage4-prep/protocol-c-fill-2-1
---

# PR #12 Fix-Forward Required — Protocol C v1.0.1

## Reviewer verdict summary

PR #12 verdict at `7d56b09`: **APPROVE-WITH-NITS** with 1 MEDIUM
+ 2 LOW + several NITs. Reviewer's literal phrasing: "APPROVE-WITH-NITS
as v1.0 design artifact AND open Task 2.1 fix-forward for the MEDIUM
(raise-sizing taxonomy) BEFORE Protocol C is dispatched to calibration
exam or pilot."

Per memory `feedback_quality_default_no_ask.md`:

> "Reviewer flag as MEDIUM / non-blocking → still address it;
> don't defer without reason"

Same pattern as Task 1 (PR #10 → PR #11 fix-forward). PR #12 held
pending fix-forward to v1.0.1.

## The MEDIUM finding

### MEDIUM #1 — Raise-sizing taxonomy conflicts with solver memory

Author used `RAISE_2_5X` / `RAISE_3X` (facing-bet multiples) in
Protocol C v1.0. `feedback_solver_aligned_sizing.md` explicitly
prescribes `RAISE all streets: 33% / 66% (pot-relative)`.

**Author self-flagged at the highest-priority UNCERTAIN.**

**Why this matters:** A labeller using Protocol C will enumerate
`RAISE_2_5X` / `RAISE_3X` candidate actions. The pilot's solver-
verification pass will hit a sizing mismatch — exactly the failure
mode the memory was created to prevent (Phase B 12 Apr 2026
incident, 11 of 19 hands had red-flag sizing warnings).

**Fix-forward action:** Replace `RAISE_2_5X` / `RAISE_3X` taxonomy
with pot-relative `RAISE_33` / `RAISE_66` per
`feedback_solver_aligned_sizing.md`. Updates needed:

1. §"Step 1" raise-sizings paragraph
2. Output schema sample
3. Example 2 case-against arguments (currently reference 2.5X/3X
   sizing logic)

This is the same correction pattern as the spec'd bet sizings
(flop 25%/66%, turn 33%/75%, river 33%/75%/150% — all pot-relative)
which Protocol C v1.0 already implements correctly.

## LOWs that defer (NOT fix-forward blockers)

Reviewer flagged 2 LOWs:

- WEAK-tier "<5% EV cost" boundary fuzzier than rubric implies for
  hands at 4-6% EV cost — flag for v1.1 calibration material
- Trail-grading κ ≥ 0.65 target borrowed from Protocol B may be
  loose; realistic pilot κ may land 0.55-0.70 — recommend κ
  measured + reported with no go/no-go gate at v1.0 calibration

Plus several NITs (UNCERTAIN tag downgrades, etc.). These can fold
into Task 5 wrap-up commit OR addressed during pilot calibration
phase.

## Fix-forward workflow (mirror Task 1.1 pattern)

1. **New branch:** `stage4-prep/protocol-c-fill-2-1`
2. **Author dispatch:** address MEDIUM #1 (raise-sizing taxonomy
   replacement)
3. **Reviewer dispatch (different agent):** verify MEDIUM addressed;
   verify no new MEDIUMs introduced
4. **Open PR #13** with title "Stage 4 prep Task 2.1: Protocol C
   v1.0.1 (APPROVE-WITH-NITS fix-forward)"
5. **Standing PR pattern:** 4-checkpoint state protocol, verdict
   on PR thread, builder writes verdict comms, orchestrator merges
   on APPROVE
6. **PR #12 disposition:** orchestrator merges PR #13 (which contains
   PR #12's content as ancestor) — standing GitHub auto-resolution
   pattern (same as Task 1's PR #10 → PR #11 → both auto-merged)

## Recommendation

Take the slow/quality path: **PR #12 stays open until v1.0.1
fix-forward (PR #13) lands**. Address the MEDIUM, push v1.0.1 as
PR #13, get APPROVE verdict, orchestrator merges.

This is mechanically identical to Task 1's flow.

## Estimated fix-forward effort

~30-45 min for the raise-sizing taxonomy replacement (it's a
schema/text change, not a logic change). Plus reviewer dispatch
~15-30 min. Total ~1 hour.

Quality benefits:
- Protocol C aligns with solver-verification memory
- Pilot solver-verification pass won't hit sizing mismatches
- Cross-protocol consistency: A and B both use pot-relative; C
  joining them avoids labeller-confusion across protocols

## Cross-stream — unchanged

Task 3 (Stage 5 retrain) and Task 4 (Stage 6 held-out) are next in
sequence. Builder may run Task 2.1 fix-forward in parallel with
Task 3 OR sequential per their plan. Either is acceptable.

## Action

**Builder:**

1. Pick path: stay sequential (Task 2.1 first, then Task 3) OR
   parallel (Task 2.1 + Task 3 author dispatches concurrent)
2. Author dispatch on `stage4-prep/protocol-c-fill-2-1`
3. Reviewer dispatch (independent)
4. PR #13 per standing pattern
5. After PR #13 APPROVE: orchestrator merges (which auto-resolves
   PR #12 as ancestor-merged, same as PR #10 → PR #11 pattern)

**Orchestrator (me):**

1. PR #12 held pending fix-forward
2. PR #13 (Task 2.1) merge per standing pattern after APPROVE
3. Loop continues at 15-min cadence

## Reference

- `MAIN_TERMINAL_BUILDER_STAGE4_PREP_TASKS_2026-04-26.md` (`6201554`)
  — Stage 4 prep tasks directive
- `MAIN_TERMINAL_PR_10_FIX_FORWARD_REQUIRED_2026-04-26.md` (`099c9de`)
  — Task 1.1 fix-forward precedent
- `MAIN_TERMINAL_PR_11_MERGED_TASK2_GREENLIGHT_2026-04-26.md` (`dbcbf0c`)
  — Task 1 closure pattern
- `7d56b09` — PR #12 reviewer verdict (APPROVE-WITH-NITS)
- `feedback_quality_default_no_ask.md` — "MEDIUM/non-blocking →
  still address; don't defer"
- `feedback_solver_aligned_sizing.md` — RAISE 33%/66% pot-relative
  spec
