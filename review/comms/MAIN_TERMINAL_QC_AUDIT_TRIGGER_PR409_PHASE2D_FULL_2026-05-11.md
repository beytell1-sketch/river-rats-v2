---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #409 — Phase 2-D-FULL (30 additional 4-way reference hands; 35-hand set complete) — fire audit now (pre-merge milestone)
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #409 (Phase 2-D-FULL)

PR #409: `builder-phase2-d-full-2026-05-11`. Head per push `origin/builder-phase2-d-full-2026-05-11` (10:35). Title: "Builder Phase 2-D-FULL — 30 additional 4-way reference hands; full set 35-hand complete".

Builder self-assessment: 30 hands delivered (H6-H35); street distribution **exact** match to AMENDMENT 1 (18/11/4/2); 5-of-5 decision class diversity; NO owner-arb items pending; per-hand rationale ~200-300 words. Wall-clock ~4-5h (well under dispatch's 6-8h estimate).

## Diff summary (per builder report §"Files in this PR")

3 files / no code touched:

- `data/4way_reference_35hand_2026-05-11.jsonl` (NEW; 35 lines — consolidates pilot 5 + new 30)
- `review/comms/4WAY_REFERENCE_FULL_RATIONALE_2026-05-11.md` (NEW; ~7400 words; H6-H35 rationale)
- `review/comms/BUILDER_REPORT_PHASE2D_FULL_4WAY_REFERENCE_2026-05-11.md` (NEW; this PR's report)

**Note: NO separate FULL spec design doc.** Builder reused pilot's spec framework (PR #405's `PHASE2D_4WAY_REFERENCE_SPEC_DESIGN_2026-05-11.md`); rationale doc + JSONL + pilot spec framework jointly satisfy Task 1. Architect-attested as sufficient; QC verifies acceptable.

## Audit scope (~25-35 min — pre-merge milestone; 3-file design+judgment audit at scale)

Per dispatch (PR #408) §"QC stream — what you audit":

### Part A — Diff scope (TC-23)

1. **All 3 PR files match builder report list.** No additional files.
2. **TC-23 EXISTENCE**: `git ls-files` returns all 3 paths post-commit.
3. **NO river-rats-core/ edits** (no code touched).
4. **NO oracle_router edits**.
5. **NO model file edits**.
6. **NO corpus / labelling work** (this is reference set DESIGN, not labelling).

### Part B — JSONL artifact verification

7. **JSONL has 35 valid lines** (5 pilot + 30 new).
8. **Each parseable as JSON**; each contains required fields (pre-flop action history, board, hero hole cards, opponent count, expected action, axis, rationale-summary).
9. **5 pilot hands (H1-H5) preserved unchanged** from pilot JSONL (regression check vs `data/4way_reference_pilot_5hand_2026-05-11.jsonl`).
10. **30 new hands (H6-H35) all present** with full field coverage.

### Part C — Street distribution (35-total)

11. **18 flop / 11 preflop / 4 turn / 2 river** = exact match to AMENDMENT 1 51/31/11/6 at 35-hand scale.
12. Within dispatch ±2 tolerance (here: exact, 0 deviation).

### Part D — Decision class diversity

13. **5-of-5 classes present**: BET (4) + FOLD (4) + CHECK (8) + CALL (14) + RAISE (5).
14. **CALL over-target (14 vs 7-9)**: builder argues "GTO-realistic distribution favors CALL in 4-way SRP IP/closing + multi-way SDV bluff-catchers". QC validates: force-converting CALL→RAISE corrupts GTO; force-converting CALL→FOLD over-tightens. QC categorization: builder reasoning acceptable; "approximate" range guidance in dispatch absorbs this. Cosmetic-only concern.
15. **FOLD slight over-target (4 vs 2-3)**: builder argues 4 distinct fold axes (range-discipline + sub-defend + cbet-no-equity + river-jam). QC validates each fold serves distinct reference axis. Cosmetic-only concern.

### Part E — Axis coverage

16. **4-way 3-bet pots**: H12, H15 ✓
17. **4-way 4-bet pots**: H12 (BTN 4-bet vs 3-bet+cold-call) ✓ (1 hand acceptable per dispatch "~1-2 hands; architect's call")
18. **Multiway-cooler spots**: H17, H19, H25 ✓
19. **River decisions**: H31 (FOLD), H32 (BET thin value) ✓ (both river decision classes)
20. **BET decisions**: H17, H19, H28, H32 ✓ (4 hands; within 3-4 target)
21. **FOLD decisions**: H10, H14, H21, H31 ✓ (4 hands; over 2-3 target but distinct axes)
22. **Range-asymmetry continuations**: H4 (pilot), H7, H13, H35 ✓

### Part F — True 4-way at decision moment (§3.X.3)

23. **33/35 hands are 4+way at decision moment** (`num_opponents_at_decision >= 3`).
24. **2 exceptions (H31 + H32 river hands)**: 4-way SRPs that collapsed to 2-way by river due to natural fold attrition. Builder claims design memo §3.X.3 allows flexibility for terminal-street references.
    - **QC verifies**: read design memo §3.X.3; check if terminal-street flexibility is actually allowed OR if this is a SHOULD_FIX/BLOCKER for the 2 river hands.
    - **Note**: even if NOT explicitly allowed, the 2 hands serve river decision class coverage which IS required per AMENDMENT 1; trade-off between strict "4-way at decision" and "river decision class coverage" — QC categorize per evidence.

### Part G — Per-hand rationale quality

25. **Total rationale doc ~7400 words** (≈ 247 words/hand on 30 hands).
26. **Builder claims 200-300 words per hand** (slightly under dispatch's 250-400 target for efficiency).
    - QC may flag: SHOULD_FIX-process if word count consistently below 200; SHOULD_FIX-substantive if reasoning chain incomplete due to brevity.
    - Spot-check 3-5 random hand rationales; verify gto-expert reasoning chain complete (range composition, equity, blocker effects, pot geometry).
27. **Anti-rule-based attestation**: every rationale derives from poker theory; NOT rule-based / threshold-based / template repetition.
28. **Terminology compliance**: open = preflop opener; bet = first postflop; raise = raise-of-existing-bet. Cross-check no postflop "raise" misuse.
29. **Bet sizing solver-aligned**: flop 25%/66%, turn 33%/75%, raise 3-4x bet per `feedback_solver_aligned_sizing.md`.

### Part H — Spec framework reuse

30. Builder reused pilot's spec framework (merged in PR #405) rather than creating a new FULL spec design doc. Per dispatch Task 1 "architect picks (cleaner: single combined doc)" — this is the cleaner path.
    - QC verifies: pilot spec framework still covers the FULL-set axis allocation + street allocation methodology (no scope creep beyond what pilot framework established).

### Part I — Process discipline

31. **TC-X-DISPATCH-COMPLIANCE**: builder honored all dispatch requirements per §"Compliance with dispatch" checklist.
32. **STOP-condition compliance**: builder explicitly states "None triggered" + lists each. No owner-arb items pending.
33. **TC-X-OWNER-SCOPE-DISCIPLINE**: no scope leak; no river-rats-core/ / model / corpus / labelling work; pure design+judgment.

## What this PR does NOT change

- ❌ river-rats-core/ (no code edits)
- ❌ Production code path (no inference/router/trainer changes)
- ❌ Models, corpus, training data
- ❌ Phase 1.5 ship state (vNext-HU-59 still in production)
- ❌ Solver-verification queue (48 spots HOLD per owner-ratified §6.4)
- ❌ Phase 2-E.0 / 2-E / 2-F / 2-G / 2-H scope

## What gates next (post-QC-PASS orchestrator sequence)

1. Orchestrator merges PR #409 on QC PASS (no owner-arb pending)
2. Orchestrator dispatches **2-E.0 (4-way labeller readiness)** per AMENDMENT 3 owner-ratified §6.8:
   - 4-way labeller brief design + 29-hand calibration set + 5-hand pilot validation
   - Anti-rule-based boilerplate (mandatory per FL4 lessons + `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`)
3. After 2-E.0 clears: 2-E (4-way corpus ~750 lookalikes) → 2-F (3-way retrain on 61-feat) → 2-G (4-way retrain) → 2-H (production swap)

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~25-35 min wall-clock (35-hand design+judgment audit at scale). QC writes:
- `~/river-rats-qc/findings/2026-05-11-pr409-phase2d-full.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2D_FULL_2026-05-11.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## SHOULD_FIX / BLOCKER classification guidance

- **BLOCKER**: JSONL malformed; pilot hands H1-H5 changed; rationale uses rule-based shortcuts; FOLD/CALL distribution outside GTO defense (extreme deviation); terminology violations; ≥5/35 hands not-actually-4-way without documentation
- **SHOULD_FIX-substantive**: missing axis coverage (e.g., 0 river hands); rationale below 150 words consistently with broken reasoning chain; spec framework reuse breaks axis allocation logic
- **SHOULD_FIX-process**: rationale word count under 250 throughout (builder's 200-300 below dispatch's 250-400); 2 river hands not-strictly-4-way (acceptable per design memo §3.X.3 flexibility OR flagged for owner attention); minor wording / typo issues
- **PASS**: builder self-assessment 5/5 + QC independent verification confirms

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `80d935f` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 2-D-FULL dispatch: master `80d935f` (PR #408)
- Phase 2-D pilot builder: master `3509679` (PR #405) + QC PASS `e518028` (PR #407)
- Phase 2-A design memo: master `0e5f91f` (PR #388) + QC PASS `a221a9b` (PR #391)
- AMENDMENTS 1+2+3: masters `cee0705` / `596bb89` / `3763d8a`
- Builder report: `review/comms/BUILDER_REPORT_PHASE2D_FULL_4WAY_REFERENCE_2026-05-11.md`
- Full rationale: `review/comms/4WAY_REFERENCE_FULL_RATIONALE_2026-05-11.md`
- Pilot rationale: `review/comms/4WAY_REFERENCE_PILOT_RATIONALE_2026-05-11.md`
- Pilot spec framework: `review/comms/PHASE2D_4WAY_REFERENCE_SPEC_DESIGN_2026-05-11.md`
- Full JSONL artifact: `data/4way_reference_35hand_2026-05-11.jsonl`
- Pilot JSONL artifact: `data/4way_reference_pilot_5hand_2026-05-11.jsonl`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_bucket_first_labelling.md`, `feedback_orchestrator_branch_base_verification.md`

**Status: QC stream — fire audit now on PR #409 Phase 2-D-FULL (35-hand 4-way reference set complete). ~25-35 min wall-clock. 33-item audit covering diff scope + JSONL (35 valid lines; pilot 5 preserved) + street distribution 18/11/4/2 exact + 5-of-5 decision class + axis coverage + 33/35 true-4-way + 2 river-by-collapse documented + rationale quality + terminology + bet sizing + spec framework reuse + dispatch compliance. Builder self-assessed PASS; no owner-arb items. After QC PASS + merge → orchestrator dispatches 2-E.0 (4-way labeller readiness per AMENDMENT 3).**
