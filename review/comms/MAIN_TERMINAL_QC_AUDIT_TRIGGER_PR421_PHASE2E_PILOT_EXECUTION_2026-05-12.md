---
date: 2026-05-12
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #421 — Phase 2-E PILOT execution (5-labeller + Opus tier-up production pipeline; 50/50 PROCEED gate verdict; 0 owner-arb; 0 FL4-drift; 3 solver-verify queue items) — fire audit now (pre-merge milestone)
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #421 (Phase 2-E PILOT execution)

PR #421: `builder-phase2-e-pilot-execution-2026-05-12`. Pushed 01:35 SAST (12h after owner-authorized dispatch PR #420). Title: "Builder Phase 2-E PILOT execution — 50/50 PROCEED gate verdict; 5-labeller+Opus production pipeline".

**Builder self-assessment: 50/50 PROCEED** — best-possible outcome per dispatch §gate.

## Pilot results summary (from builder report)

- **251 labels delivered** (50 hands × 5 Sonnet labellers + 1 Opus tier-up)
- **Sonnet consensus rate**: 43/50 = 86% (≥85% target ✓)
- **Owner-arb rate**: 0/50 = 0% (5-20% target; under range because Opus closed all disputes)
- **FL4-drift detection**: 0 actual instances (1 regex false-positive on `facing_bet=0` text; verified benign)
- **Consensus collapse rate**: 0%
- **Decision class diversity**: 5-of-5 (BET 15 / CALL 12 / CHECK 9 / RAISE 8 / FOLD 6)
- **Wall-clock**: ~30 min agent dispatch + ~30 min consensus/report
- **Solver-verify queue**: 3 spots (post-consensus quality items, NOT owner-arb): 4WL-SRP-09 (Opus LOW), 4WL-SRP-04 (Opus MEDIUM), 4WL-SRP-10 (sizing divergence only)

## Diff summary (per builder PR; QC verifies)

Likely 8-12 files:
- `data/4way_corpus/pilot_50/raw_labels_labeller_1.jsonl` through `_5.jsonl` (5 Sonnet outputs)
- `data/4way_corpus/pilot_50/raw_labels_opus_tierup.jsonl` (Opus output)
- `data/4way_corpus/pilot_50/consensus.jsonl` (consensus state per spot)
- `data/4way_corpus/pilot_50/owner_arb_queue.jsonl` (empty per builder; 0 spots)
- `data/4way_corpus/pilot_50/solver_verify_queue.jsonl` (3 spots flagged)
- `data/4way_corpus/pilot_50/drift_alerts.log` (1 regex false-positive)
- `review/comms/BUILDER_REPORT_PHASE2E_PILOT_EXECUTION_2026-05-12.md` (this report)

No river-rats-core/ code edits expected (pure data generation via subagents).

## Audit scope (~30-45 min — pre-merge milestone; data-generation audit at production scale)

Per dispatch (PR #420) §"Final pilot gate evidence report":

### Part A — Diff scope (TC-23)

1. All PR files match builder report. NO river-rats-core/ inference/router/model/trainer edits.
2. TC-23 EXISTENCE: all paths git-tracked post-commit.
3. NO production model file edits.
4. NO consensus rule changes (driver script frozen from PR #417).
5. NO brief / calibration / lookalike subset modifications (all frozen from prior PRs).

### Part B — Label JSONL validity

6. Each labeller JSONL has 50 valid lines (5 × 50 = 250 Sonnet labels).
7. Opus tier-up JSONL covers the 7 disputed spots (3-2 or 3-1-1 Sonnet patterns).
8. Each label has required fields: bucket, action, action_size (where applicable), confidence, rationale (~200-400 words), reasoning_chain (range composition / equity / blocker / pot geometry / position dynamics where relevant).

### Part C — Consensus rule application

9. Per design memo §4.3 rule applied correctly per spot:
   - ≥4-of-5 Sonnet agree → consensus (34 all-agree + 9 4-of-5 = 43 ✓)
   - 3-2 + Opus agrees → consensus (7 spots resolved this way ✓)
   - 3-2 + Opus disagrees → owner-arb (0 instances; verify Opus always agreed with Sonnet majority on 3-2 splits)
   - 2-2-1+ → owner-arb (0 fragments; verify no missing fragments)
10. Spot-check 5-10 consensus.jsonl entries: state classification matches actual votes.

### Part D — Anti-rule-based attestation (CRITICAL — FL4 prevention)

11. Spot-check 5-10 random Sonnet labels across all 5 labellers: NO if/elif chains, NO threshold cutoffs (`equity > X`), NO function-definition / return-statement patterns, NO template repetition.
12. **Verify the 1 regex false-positive (FL1, 4WL-SRP-10, `if facing_bet=0`)**: builder claims benign (explaining spec field, NOT rule-based decision). QC reads the FL1 rationale on 4WL-SRP-10 + confirms decision derives from poker theory (not threshold).
13. Cross-check FL4-incident pattern: NONE of the 250 labels resemble FL4's Python-script-style.

### Part E — Decision class diversity + axis distribution

14. **Decision class**: 5-of-5 present (BET 15 / CALL 12 / CHECK 9 / RAISE 8 / FOLD 6). Reasonable balance.
15. **Axis distribution**: no axis monoculture (each of 6 axis families has ≥3 labels covered).
16. Per-labeller action distributions within ±3 per class (strong agreement across labellers).

### Part F — Opus tier-up integrity

17. 7 disputed spots covered by Opus: 4WL-3BET-02, 4WL-3BET-10, 4WL-CLOSE-09, 4WL-MW45-02, 4WL-SRP-04, 4WL-SRP-09, 4WL-SRP-10.
18. Opus rationale ~250-400 words per spot; reasoning chain complete.
19. Opus action in 7/7 spots matched Sonnet majority direction (consensus closed without owner-arb).

### Part G — Solver-verify queue

20. 3 spots flagged for solver-verify per `feedback_solver_verification_queue.md`:
    - 4WL-SRP-09 (Opus LOW confidence; genuinely close)
    - 4WL-SRP-04 (Opus MEDIUM; close mix)
    - 4WL-SRP-10 (Opus action-agrees but sizing diverges; verify size on nuts in 4-way wet)
21. These spots reached CONSENSUS on action; flag is post-consensus quality QA only. QC verifies these are NOT silently auto-adjudicated owner-arbs (which would be a methodology violation).

### Part H — Process discipline

22. **TC-X-DISPATCH-COMPLIANCE per PR #420**: builder honored all 5 tasks (5 Sonnet labellers, Opus tier-up, consensus, arb queue handling, report).
23. **STOP-condition compliance**: builder honored FL4-drift STOP-trip (would have halted if drift detected); did NOT improvise unilateral owner-arb adjudication.
24. **TC-X-OWNER-SCOPE-DISCIPLINE**: no scope leak; no river-rats-core/ / model / 2-E-full / 2-F-G-H work.

## What this PR does NOT change

- ❌ river-rats-core/ (no code edits)
- ❌ Production code path
- ❌ Models, full corpus, training data (this is pilot subset only)
- ❌ Phase 1.5 ship state (vNext-HU-59 still in production)
- ❌ Solver-verification queue from §6.4 (48 spots HOLD; this PR adds 3 new spots to solver-verify-later queue but does NOT drain existing)
- ❌ Phase 2-E full / 2-F / 2-G / 2-H scope

## What gates next (post-QC-PASS orchestrator sequence)

1. Orchestrator merges PR #421 on QC PASS (50/50 PROCEED gate cleared)
2. Owner-arb queue: 0 spots — no owner direction needed for adjudication
3. Solver-verify queue: 3 new spots added to existing 48-spot queue (per `feedback_solver_verification_queue.md`; HOLD-with-accepted-risk per owner-ratified §6.4); orchestrator does NOT block 2-E full on solver-verify; queue drains when solver online
4. Orchestrator dispatches **2-E full ~700 hands** (full labelling pipeline; same brief + calibration + labeller infrastructure)

## QC routing + Output

Standalone stream. ~30-45 min wall-clock (data-generation audit at 251-label scale; sample-checking required). QC writes:
- `~/river-rats-qc/findings/2026-05-12-pr421-phase2e-pilot-execution.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2E_PILOT_EXECUTION_2026-05-12.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## SHOULD_FIX / BLOCKER classification guidance

- **BLOCKER**: ANY label shows actual FL4-style rule-based pattern; consensus rule misapplied per §4.3; Opus didn't close 3-2 disputes; owner-arb queue silently auto-adjudicated; production model edits; brief/calibration tampered with
- **SHOULD_FIX-substantive**: missing labels (e.g., labeller produced <50); rationale word count consistently <150 across labellers; axis monoculture
- **SHOULD_FIX-process**: minor wording / typo; solver-verify queue lacks per-spot rationale
- **PASS**: 50/50 PROCEED verdict verified independently + all data integrity checks pass

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `7a45640` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 2-E pilot production execution dispatch (owner-authorized): master `7a45640` (PR #420)
- Phase 2-E pilot infrastructure + QC PASS: PR #417 + #419
- Phase 2-E.0 labeller readiness + QC PASS: PR #413 + #415
- Phase 2-A design memo §4.3 consensus rule: `review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md`
- 4-way labeller brief (operational): `data/4way_labeller_brief.md`
- 29-hand calibration set: `data/4way_calibration_29hand_2026-05-11.jsonl`
- 50-hand lookalike subset: `data/4way_lookalikes_50hand_pilot_2026-05-11.jsonl`
- Driver script: `scripts/dispatch_4way_labelling_pilot.py`
- FL4 incident (anti-rule-based motivation): `review/comms/BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md`
- Builder report: `review/comms/BUILDER_REPORT_PHASE2E_PILOT_EXECUTION_2026-05-12.md`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_solver_verification_queue.md`, `feedback_bucket_first_labelling.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`

**Status: QC stream — fire audit now on PR #421 Phase 2-E pilot production execution. ~30-45 min wall-clock. 24-item audit covering 251-label data integrity + consensus rule application + Opus tier-up integrity + FL4-drift verification (with 1 regex false-positive case to validate as benign) + solver-verify queue + dispatch compliance. Builder self-assessed 50/50 PROCEED. After QC PASS + merge → orchestrator dispatches 2-E full ~700 hands (3 solver-verify items added to existing 48-spot queue; HOLD-with-accepted-risk per §6.4).**
