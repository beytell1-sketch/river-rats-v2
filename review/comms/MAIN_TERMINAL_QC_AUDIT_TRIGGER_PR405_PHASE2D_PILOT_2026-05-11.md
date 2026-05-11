---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #405 — Phase 2-D pilot (5-hand 4-way reference set + 35-hand spec framework) — fire audit now (pre-merge milestone)
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #405 (Phase 2-D pilot)

PR #405: `builder-phase2-d-pilot-2026-05-11`. Head per push `origin/builder-phase2-d-pilot-2026-05-11` (09:22). Title: "Builder Phase 2-D pilot — 5-hand 4-way reference + 35-hand spec framework".

Builder Phase 2-D pilot per dispatch (PR #404). **Builder self-assessment: 5/5 pilot gate PASS** (all axes covered, gto-expert reasoning evident, street distribution within ±10% of 51/31/11/6 at 5-hand scale, no rule-based shortcuts).

This is the design+judgment phase deliverable; no river-rats-core/ code touched. Per pilot-first standing rule, pilot gate clearance gates the 2-D-FULL 30-hand dispatch.

## Diff summary (per builder report §"Deliverables")

4 files / no code touched:

- `review/comms/PHASE2D_4WAY_REFERENCE_SPEC_DESIGN_2026-05-11.md` (NEW; 7KB) — 35-hand spec framework
- `data/4way_reference_pilot_5hand_2026-05-11.jsonl` (NEW) — Machine-readable 5-hand pilot artifact
- `review/comms/4WAY_REFERENCE_PILOT_RATIONALE_2026-05-11.md` (NEW; 14KB) — Per-hand gto-expert rationale
- `review/comms/BUILDER_REPORT_PHASE2D_PILOT_4WAY_REFERENCE_2026-05-11.md` (NEW; 6KB) — pilot report

## Audit scope (~20-30 min — pre-merge milestone; 4-file PR; design+judgment audit)

Per dispatch (PR #404) §"QC stream — what you audit":

### Part A — Diff scope (TC-23)

1. **All 4 PR files match builder report list.** No additional files.
2. **TC-23 EXISTENCE**: `git ls-files` returns all 4 paths post-commit (including the JSONL artifact in `data/`).
3. **NO river-rats-core/ edits** (no code touched).
4. **NO oracle_router edits**.
5. **NO model file edits**.
6. **NO corpus / labelling work** (this is reference set DESIGN, not labelling).

### Part B — 5-hand pilot artifact verification

7. **JSONL is valid**: 5 lines; each parseable as JSON; each contains required fields (pre-flop action history, board, hero hole cards, opponent count, expected action, axis, rationale-summary).
8. **5 hands match builder report Table** (PILOT-1 through PILOT-5):
   - PILOT-1: preflop, BTN 8h7h, CALL, closing-action
   - PILOT-2: flop, BTN KsJd, Kh7d2c, CALL, MW-40 (TPGK)
   - PILOT-3: flop, SB AsKd, 8s5s2c, CHECK, MW-47 (nut FD blocker)
   - PILOT-4: flop, MP AhJd, QcJh9c, RAISE 9bb, range-asymmetry MP
   - PILOT-5: turn, SB ThTc, 8d5h2sJc, CHECK, MW-45 (broadway turn)

### Part C — Per-hand rationale quality

9. **`4WAY_REFERENCE_PILOT_RATIONALE_2026-05-11.md` length**: ~14KB ≈ ~1700 words; 5 hands × 250-400 words ≈ 1250-2000 word budget — within range.
10. **gto-expert-hat reasoning chain evident** in each rationale section (NOT rule-based / threshold-based / template):
    - Range composition reasoning (which villain holdings get to this node)
    - Equity realization considerations (position, SPR, multiway equity collapse)
    - Blocker effects (where relevant — PILOT-3 nut FD blocker; PILOT-2 K-blocker)
    - Pot geometry (raise sizing rationale; SPR-aware folding lines)
    - NO if/elif rule chains; NO "score = X * Y * Z therefore action" formulations
11. **Terminology compliance** (per `feedback_terminology_raise_vs_bet.md`): no first-postflop "raise"; first postflop action is "bet"; raise = raise of existing bet.
12. **Bet sizing solver-aligned** (per `feedback_solver_aligned_sizing.md`): flop 25%/66% or analog; raise sizing 3x bet (= 9bb for solver-scaled value/protection).

### Part D — Axis coverage

13. **5 distinct axes covered**:
    - PILOT-1: closing-action (AMENDMENT 2 §3.Y.3)
    - PILOT-2: MW-40 (TPGK on multiway)
    - PILOT-3: MW-47 (nut FD with blocker MW)
    - PILOT-4: range-asymmetry MP (design memo §3.3 axis)
    - PILOT-5: MW-45 (broadway-completion turns)
14. No axis monoculture — verify each hand's primary axis is distinct from the others.

### Part E — Street distribution

15. **3 flop / 1 preflop / 1 turn / 0 river** matches AMENDMENT 1 ratios at 5-hand scale:
    - 51% flop = 2.55 → 3 flop hands ✓
    - 31% preflop = 1.55 → 1 preflop ✓
    - 11% turn = 0.55 → 1 turn ✓
    - 6% river = 0.30 → 0 river ✓ (deferred to full 30-hand)
16. Within dispatch ±10% tolerance at small-sample scale.

### Part F — True 4-way attestation

17. Each hand verified 4-way at decision moment (`num_opponents_at_decision == 3` per pilot JSONL).
18. NOT 4-way-preflop-pot-that's-2-way-by-river. The decision moment is the bound.

### Part G — Decision class diversity

19. Pilot decision distribution: CALL × 2 + CHECK × 2 + RAISE × 1 (per builder report).
20. **Acceptable**: BET + FOLD deferred to full 30-hand set per builder's "decision-class diversity within 5-hand constraint" reasoning.
21. **NOT acceptable** would be 5/5 same decision (e.g., all CHECK). Pilot has 3 distinct decision classes — verify diverse.

### Part H — Spec framework (`PHASE2D_4WAY_REFERENCE_SPEC_DESIGN_2026-05-11.md`)

22. 35-hand spec framework covers:
    - Axis allocation (which axes get how many hands across 35)
    - Street allocation (51/31/11/6 mapping to 35 hands)
    - Per-hand format (fields each entry must have)
23. Spec framework includes the 5 axes pilot covered + identifies 4-way 3-bet / 4-way 4-bet / multiway-cooler / river / BET / FOLD axes for full 30-hand expansion.

### Part I — Process discipline

24. **TC-X-DISPATCH-COMPLIANCE per PR #404**: builder honored all task list:
    - ✓ Task 1 spec design
    - ✓ Task 2 5-hand pilot execution
    - ✓ Task 3 gate evidence
    - ⏭ Task 4 deferred to 2-D-FULL (correctly NOT in this PR; separate dispatch)

25. **STOP-condition compliance**: builder explicitly states "None triggered" + lists each STOP condition. ✓

26. **TC-X-OWNER-SCOPE-DISCIPLINE**: no scope leak; no river-rats-core/ / model / corpus / labelling work; pure design+judgment.

## What this PR does NOT change

- ❌ river-rats-core/ (no code edits)
- ❌ Production code path (no inference/router/trainer changes)
- ❌ Models, corpus, training data
- ❌ Phase 1.5 ship state (vNext-HU-59 still in production)
- ❌ Solver-verification queue (48 spots HOLD per owner-ratified §6.4)
- ❌ Phase 2-D-FULL / 2-E / 2-F / 2-G / 2-H scope

## What gates next (post-QC-PASS orchestrator sequence)

1. Orchestrator merges PR #405 on QC PASS
2. Orchestrator dispatches 2-D-FULL (30-hand design; ~3-5h estimate)
3. After 2-D-FULL clears: 2-E.0 (4-way labeller readiness per AMENDMENT 3) → 2-E (corpus) → 2-F (3-way retrain on 61-feat) → 2-G (4-way retrain) → 2-H (production swap)

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~20-30 min wall-clock (4-file design+judgment audit). QC writes:
- `~/river-rats-qc/findings/2026-05-11-pr405-phase2d-pilot.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2D_PILOT_2026-05-11.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## SHOULD_FIX / BLOCKER classification guidance

- **BLOCKER**: JSONL parse errors; rationale uses rule-based shortcuts (e.g., if/elif chains; threshold-based decisions); not-actually-4-way spots; terminology violations (raise/bet); axis monoculture
- **SHOULD_FIX-substantive**: street distribution wildly off 51/31/11/6 (>±10%); axis coverage < 4 distinct; missing spec framework sections
- **SHOULD_FIX-process**: missing references; minor wording / typo issues; bet sizing not solver-aligned (architect should use 25%/66% flop sizing convention)
- **PASS**: builder self-assessment 5/5 + QC independent verification confirms

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `e2efc93` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 2-D dispatch: master `e2efc93` (PR #404)
- Phase 2-C cleanup: master `ff64928` (PR #401) + QC PASS `dafa8f9` (PR #403)
- Phase 2-A design memo: master `0e5f91f` (PR #388) + QC PASS `a221a9b` (PR #391)
- AMENDMENTS 1+2+3: masters `cee0705` / `596bb89` / `3763d8a`
- Builder report: `review/comms/BUILDER_REPORT_PHASE2D_PILOT_4WAY_REFERENCE_2026-05-11.md`
- Pilot rationale: `review/comms/4WAY_REFERENCE_PILOT_RATIONALE_2026-05-11.md`
- Spec framework: `review/comms/PHASE2D_4WAY_REFERENCE_SPEC_DESIGN_2026-05-11.md`
- Pilot artifact: `data/4way_reference_pilot_5hand_2026-05-11.jsonl`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_bucket_first_labelling.md`, `feedback_orchestrator_branch_base_verification.md`

**Status: QC stream — fire audit now on PR #405 Phase 2-D pilot. ~20-30 min wall-clock. 26-item audit covering diff scope + JSONL artifact + per-hand rationale quality + axis coverage + street distribution + true-4-way attestation + decision class diversity + spec framework + dispatch compliance. Builder self-assessed 5/5 PASS. After QC PASS + merge → orchestrator dispatches 2-D-FULL (30-hand design).**
