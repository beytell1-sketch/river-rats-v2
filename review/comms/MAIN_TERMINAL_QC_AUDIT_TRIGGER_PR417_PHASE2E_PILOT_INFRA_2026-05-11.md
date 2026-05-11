---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #417 — Phase 2-E PILOT INFRASTRUCTURE (50-hand lookalike subset + driver script + analysis; production 5-labeller execution surfaced as separate STOP per dispatch §STOP wall-clock budget) — fire audit now (pre-merge milestone)
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #417 (Phase 2-E PILOT infrastructure)

PR #417: `builder-phase2-e-pilot-2026-05-11`. Pushed 12:40. Title: "Builder Phase 2-E PILOT — 50-hand lookalikes + driver; STOP-surface for production execution".

Builder hit STOP-condition per dispatch §STOP wall-clock budget. Production 5-labeller × 50-hand × Opus tier-up execution (~3-5h + token spend) is separately allocated per HU 1.5-D out-of-band pattern. This PR is INFRASTRUCTURE-ONLY:
1. 50-hand lookalike subset (axis-balanced per dispatch)
2. Driver script (`scripts/dispatch_4way_labelling_pilot.py`) — `prepare` + `collect` modes + consensus rule + FL4-drift detection
3. Pre-execution analysis + STOP-surface for orchestrator/owner-direction

Builder explicitly STOP'd per CLAUDE.md §5 (did NOT improvise production execution).

## Diff summary

3-4 files (builder report §"Files in this PR" — to be verified):
- `data/4way_lookalikes_50hand_pilot_2026-05-11.jsonl` (NEW; 50 hands)
- `scripts/dispatch_4way_labelling_pilot.py` (NEW; driver)
- `review/comms/BUILDER_REPORT_PHASE2E_PILOT_2026-05-11.md` (NEW; STOP-surface report)
- (possibly other support files; QC verifies)

## Audit scope (~20-30 min — pre-merge infrastructure audit)

### Part A — Diff scope (TC-23)

1. PR files match builder report list. NO river-rats-core/ inference/router/model edits.
2. TC-23 EXISTENCE: all paths `git ls-files`-visible post-commit.
3. NO 5-labeller raw outputs in this PR (those come in production-execution PR).
4. NO consensus outputs (those come post-execution).
5. Brief + calibration set NOT modified (frozen from 2-E.0 PR #413).

### Part B — 50-hand lookalike subset

6. **Exactly 50 hands** in `data/4way_lookalikes_50hand_pilot_2026-05-11.jsonl`.
7. **Axis distribution** per dispatch Task 1:
   - 4-way 3-bet/4-bet pots: ~10
   - Multiway-cooler: ~5
   - Closing-action: ~9
   - Range-asymmetry: ~9
   - MW-40/45/47: ~7
   - Standard 4-way SRP: ~10
   - Total: 50 (builder claims exact match)
8. **Each hand UNLABELLED** (no `expected_action` field; labellers will produce via consensus).
9. **Non-overlap with reference set (35-hand) + calibration set (29-hand)**: spot-check distinct boards/hole cards/action sequences.
10. **True 4-way attestation**: builder claims 37/50 are 4+way at decision; 13 have ≥2 opponents (3+way) due to cascade dynamics. QC verifies this is REALISTIC pot-cascade behavior (per design memo §3.X.3 flexibility) AND brief explicitly addresses this.

### Part C — Driver script verification

11. `scripts/dispatch_4way_labelling_pilot.py` exists; pattern matches HU 1.5-D analog (`river-rats-core/labelling_agent.py`).
12. **`prepare` mode**: splits 50 hands → 5 labeller-input batches; writes manifest JSON.
13. **`collect` mode**: parses 5-labeller outputs + Opus tier-up; applies consensus rule per design memo §4.3 (≥4-of-5 / 3-2+Opus / 3-2+Opus-disagree / 2-2-1+).
14. **FL4-drift detection heuristics**:
    - if/elif Python-script patterns
    - Threshold cutoffs (e.g., `equity > 0.55` literals)
    - Function-definition / return-statement patterns
    - Template-opening repetition
15. **STOP-trip condition**: ANY labeller fails drift check in first 10 hands → script halts (saves $80+ wasted spend).

### Part D — Driver script syntax/runnable verification

16. Independently run `python3 scripts/dispatch_4way_labelling_pilot.py --help` (or analog) — verify no syntax errors / import errors.
17. Run `prepare` mode in dry-run; verify output structure matches expected manifest.
18. (Do NOT run `collect` since no labeller outputs exist yet.)

### Part E — Process discipline

19. **TC-X-DISPATCH-COMPLIANCE per PR #416**:
    - ✅ Task 1 (50-hand subset) ✓
    - ✅ Task 2 (sourcing infrastructure) ✓
    - ✅ Task 3 (driver script) — partial: script ready; production execution STOP'd
    - ⏭ Task 4 (consensus + arb queue) — driver supports; production execution STOP'd
    - ⏭ Task 5 (pilot evidence report) — builder report is interim STOP-surface; final gate evidence after production execution
20. **STOP-condition compliance**: builder explicitly STOP'd per dispatch §STOP; did NOT improvise production execution; properly surfaces for orchestrator/owner-direction. ✓
21. **TC-X-OWNER-SCOPE-DISCIPLINE**: no scope leak; pure infrastructure + STOP-surface.

## What this PR does NOT change

- ❌ Production code path (no inference/router/trainer/model edits)
- ❌ 5-labeller raw outputs (not yet generated)
- ❌ Consensus + arb queue results (require production execution)
- ❌ Pilot gate verdict (requires production execution evidence)
- ❌ Solver-verification queue (48 spots HOLD per owner-ratified §6.4)

## What gates next (post-QC-PASS orchestrator sequence)

1. Orchestrator merges PR #417 on QC PASS (infrastructure scope; cleared STOP-surface)
2. Orchestrator surfaces to owner via AskUserQuestion: production-execution allocation decision
   - 5-labeller × 50-hand × Opus tier-up requires fresh-agent dispatch (~3-5h wall-clock + LLM token usage; estimate $150-350 if billed as raw API)
   - Quality default + HU 1.5-D analog precedent: owner has authorized similar
   - Alternative paths: smaller pilot (e.g., 3 labellers × 10 hands first) / defer 2-E
3. On owner-authorize → orchestrator dispatches builder agents for production execution

## QC routing + Output

Standalone stream. ~20-30 min wall-clock. QC writes:
- `~/river-rats-qc/findings/2026-05-11-pr417-phase2e-pilot-infra.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2E_PILOT_INFRA_2026-05-11.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## SHOULD_FIX / BLOCKER classification guidance

- **BLOCKER**: 50-hand subset not exactly 50; hand overlap with reference/calibration sets; driver script syntax errors / unrunnable; FL4-drift detection heuristics missing or broken
- **SHOULD_FIX-substantive**: axis distribution skewed (e.g., 0 multiway-cooler); driver consensus rule application incorrect per §4.3
- **SHOULD_FIX-process**: minor wording / typo; STOP-surface documentation gaps
- **PASS**: infrastructure sound + driver runnable + STOP-condition properly surfaced

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `9043497` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 2-E pilot dispatch: master `9043497` (PR #416)
- Phase 2-E.0 builder + QC PASS: PR #413 + #415
- HU 1.5-D analog (production labelling pattern): `river-rats-core/labelling_agent.py`
- FL4 incident: `review/comms/BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md`
- Builder report: `review/comms/BUILDER_REPORT_PHASE2E_PILOT_2026-05-11.md`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`

**Status: QC stream — fire audit now on PR #417 Phase 2-E pilot INFRASTRUCTURE. ~20-30 min wall-clock. 21-item audit covering 50-hand subset + driver script + STOP-surface. Builder explicitly STOP'd per dispatch §STOP wall-clock budget (proper compliance). After QC PASS + merge → orchestrator surfaces production-execution allocation decision to owner.**
