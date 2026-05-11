---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #413 — Phase 2-E.0 4-way labeller readiness (brief + 29-hand calibration + 5-hand pilot validation); 5/5 pilot gate self-assessed PASS — fire audit now (pre-merge milestone)
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #413 (Phase 2-E.0 labeller readiness)

PR #413: `builder-phase2-e0-labeller-readiness-2026-05-11`. Title: "Builder Phase 2-E.0 — 4-way labeller readiness; 5/5 pilot gate PASS". Pushed 11:49 (~30 min after dispatch).

Builder self-assessment: 5/5 pilot hands clear all gate criteria (anti-rule-based reasoning evident; multiway dimensions explicit; bucket-first compliance; solver-aligned sizing; terminology correct).

## Diff summary

5 files (per builder report):

- `data/4way_labeller_brief.md` (NEW; ~250 lines) — Production labeller brief
- `data/4way_calibration_29hand_2026-05-11.jsonl` (NEW; 29 lines) — Machine-readable calibration anchors
- `review/comms/PHASE2E0_4WAY_CALIBRATION_SET_2026-05-11.md` (NEW; ~20KB) — Human-readable calibration rationale
- `data/4way_pilot_validation_5hand_2026-05-11.jsonl` (NEW; 5 lines) — 5-hand pilot labels
- `review/comms/BUILDER_REPORT_PHASE2E0_LABELLER_PILOT_2026-05-11.md` (NEW; this report)

## Audit scope (~25-35 min — pre-merge milestone; 5-file design+judgment audit)

Per dispatch (PR #412) §"QC stream — what you audit":

### Part A — Diff scope (TC-23)

1. All 5 PR files match builder report list.
2. TC-23 EXISTENCE: `git ls-files` returns all 5 paths.
3. NO river-rats-core/ edits.
4. NO oracle_router edits.
5. NO model file edits.
6. NO lookalike corpus generation (that's 2-E scope).

### Part B — Labeller brief content (Task 1)

7. Brief at `data/4way_labeller_brief.md` covers all dispatch-required dimensions:
   - Multiway range-chain reasoning (with worked examples)
   - Players-left-to-act + squeeze-pressure (AMENDMENT 1)
   - Closing-action vs early-action variants (AMENDMENT 2)
   - **Mandatory anti-rule-based boilerplate** — explicit prohibition on if/elif chains, threshold-based, template repetition, Python-script-style reasoning
   - Bucket-first compliance preserved
   - Per-hand structure (250-400 word target) — verify mentioned even if pilot rationales come in under range
   - Solver-aligned bet sizing guidance (25/66/33/75/150)
   - Terminology compliance (open/bet/raise)
   - HU-vs-4-way delta documentation
8. Brief is operational (could be used by a fresh labeller without further explanation).

### Part C — 29-hand calibration set (Task 2)

9. **Exactly 29 hands** in `data/4way_calibration_29hand_2026-05-11.jsonl`.
10. **Axis coverage**: 4-way 3-bet/4-bet (6) + multiway-cooler (3) + closing-action (5) + range-asymmetry (5) + MW-40/45/47 (4) + standard 4-way SRP (6) = 29. Verify counts match.
11. **Non-overlap with 35-hand reference set**: spot-check no calibration hands duplicate reference set hands (different boards/hole cards/action sequences).
12. **Per-hand rationale**: 150-220 words/hand per builder claim (under dispatch's 250-400). Builder cites QC PR #411 prior precedent for relaxed range. QC categorize: SHOULD_FIX-process (same pattern as 2-D-FULL).
13. **Reasoning chain complete**: range composition / equity / blocker / pot geometry / position dynamics all present despite shorter prose.

### Part D — 5-hand pilot validation (Task 3)

14. 5 NEW lookalike spots (distinct from reference set + calibration set).
15. Per-pilot-hand fields complete:
    - P1: 4-way SRP flop OOP AA on 8-5-3 → BET 66%
    - P2: 4-way 3-bet pot OOP KK on Q-9-4 → BET 60%
    - P3: closing-action preflop BTN QJs vs 3 callers → CALL
    - P4: range-asymmetry MP AK on 9-4-2 → CALL
    - P5: multiway-cooler top set FD 77 on 7-4-3 → BET 66%
16. **Pilot gate criteria (5/5)**:
    - Anti-rule-based: 5/5 (NO if/elif/threshold patterns)
    - Multiway dimensions explicit: 5/5 (range chains, equity realization by num-opp, position dynamics)
    - Bucket-first: 5/5 (bucket field assigned, action derived)
    - Per-hand uniqueness: 5/5 (no template repetition)
    - Solver-aligned sizing: 3/3 applicable
    - Terminology: 5/5
    - Adjacent alternatives addressed: 5/5
    - True 4-way at decision: 5/5

### Part E — Sample reasoning chain quality (spot check)

17. Spot-check 2-3 pilot rationales for gto-expert reasoning depth:
    - P1 (AA 4-way SRP OOP): range chains for UTG/CO/BTN/SB; equity realization "~0.75 OOP in 4-way"; pot-cascade dynamics; position
    - Verify NO rule-based shortcuts ("if hand_rank > X, then ...") — labeller derives from poker theory throughout
18. Cross-check vs FL4-incident pattern: builder's labels look NOTHING like FL4's Python-script style.

### Part F — Process discipline

19. **TC-X-DISPATCH-COMPLIANCE**: builder honored all 4 dispatch tasks.
20. **STOP-condition compliance**: builder explicitly states no STOP triggered.
21. **TC-X-OWNER-SCOPE-DISCIPLINE**: no river-rats-core/ / model / 2-E corpus generation work; pure brief+calibration+pilot.

## What this PR does NOT change

- ❌ river-rats-core/ (no code edits)
- ❌ Production code path
- ❌ Models, full corpus, training data
- ❌ Phase 1.5 ship state
- ❌ Solver-verification queue (48 spots HOLD per owner-ratified §6.4)
- ❌ Phase 2-E / 2-F / 2-G / 2-H scope

## What gates next (post-QC-PASS orchestrator sequence)

1. Orchestrator merges PR #413 on QC PASS
2. Orchestrator dispatches **2-E (full ~750-hand labelling pipeline)** using the validated brief + calibration anchors

## QC routing + Output

Standalone stream. ~25-35 min wall-clock. QC writes:
- `~/river-rats-qc/findings/2026-05-11-pr413-phase2e0.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2E0_LABELLER_READINESS_2026-05-11.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## SHOULD_FIX / BLOCKER classification guidance

- **BLOCKER**: pilot labels show rule-based/template shortcuts (mirrors FL4); brief lacks anti-rule-based boilerplate; calibration count ≠ 29; pilot hands overlap reference set; pilot gate criteria failed
- **SHOULD_FIX-substantive**: brief missing any of the 10 required sections; calibration axis coverage skewed; pilot rationale reasoning incomplete
- **SHOULD_FIX-process**: rationale word count under 250 (builder's 150-220; per PR #411 precedent acceptable); minor wording / typo issues
- **PASS**: builder self-assessment 5/5 + QC independent verification confirms

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `849d8aa` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 2-E.0 dispatch: master `849d8aa` (PR #412)
- Phase 2-D-FULL builder: master `b669541` (PR #409) + QC PASS `a44780f` (PR #411)
- AMENDMENT 3 (labeller readiness): master `3763d8a` (PR #389)
- FL4 incident (anti-rule-based motivation): `review/comms/BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md`
- Builder report: `review/comms/BUILDER_REPORT_PHASE2E0_LABELLER_PILOT_2026-05-11.md`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_bucket_first_labelling.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`

**Status: QC stream — fire audit now on PR #413 Phase 2-E.0 labeller readiness. ~25-35 min wall-clock. 21-item audit covering diff scope + brief content (10 required sections) + calibration set (29 hands × 6 axes; non-overlap with reference set) + 5-hand pilot validation (8-criterion gate) + sample reasoning chain quality + dispatch compliance. Builder self-assessed 5/5 PASS. After QC PASS + merge → orchestrator dispatches 2-E (full ~750-hand labelling pipeline).**
