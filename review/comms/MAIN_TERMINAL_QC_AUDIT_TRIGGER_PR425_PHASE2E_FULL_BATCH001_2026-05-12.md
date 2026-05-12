---
date: 2026-05-12
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #425 — Phase 2-E FULL BATCH-001 (700-hand subset infrastructure + 50/700 labelling; 92% consensus; 4 owner-arb; labeller-readiness signal surfaced on facing_bet=0 action-space confusion) — fire audit now (pre-merge milestone)
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #425 (Phase 2-E FULL BATCH-001 checkpoint)

PR #425: `builder-phase2-e-full-batch1-2026-05-12`. Pushed 09:48 SAST (~1h after owner-authorized Option A full ~700-hand dispatch landed at master `1d5503e` via PR #424). Title: "Builder Phase 2-E FULL BATCH-001 — 700-hand subset + 50/700 labelled (92% consensus); labeller-readiness signal".

**Builder self-assessment: CHECKPOINT** — first batch of 14 complete; 700-hand subset infrastructure delivered; surfaces labeller-readiness signal to orchestrator before batches 2-14 fire.

## Builder report summary

- **700-hand 4-way lookalike subset generated**: `data/4way_lookalikes_700hand_full_2026-05-12.jsonl` + `scripts/generate_4way_lookalikes_700.py`. Axis distribution exact match dispatch targets (140 / 70 / 125 / 125 / 100 / 140 = 700).
- **Street distribution deviation**: 509 flop / 89 preflop / 87 turn / 15 river vs AMENDMENT 1 target 357/217/77/42 (51/31/11/6). Builder attests acceptable for 4-way training where flop dominates; flagged for orchestrator awareness.
- **BATCH-001 (50 hands) labelling complete**:
  - 250 Sonnet labels (5 × 50) + 5 Opus tier-up = 255 total
  - Consensus: 42 all-agree + 3 4-of-5 + 1 (3-2+Opus-joins) = **46/50 = 92%** (up from pilot 86%)
  - Owner-arb queue: **4 spots** (8%; within 5-20% target)
  - Decision class diversity: BET 24 / CHECK 9 / CALL 6 / FOLD 4 / RAISE 3 = 46 consensus + 4 arb
  - Wall-clock: ~1.5h for batch-001
- **STOP-conditions**: NONE triggered (FL4-drift 0; consensus-collapse 8% <10%; owner-arb 8% <25%; wall-clock <50h).
- **Labeller-readiness signal SURFACED** (not a hard STOP): 3 of 5 disputed spots involve `facing_bet=0` action-space confusion (Sonnet labellers voting FOLD/CALL when only BET/CHECK are legal); builder presents Path 1/2/3 for orchestrator triage.

## Diff summary (per builder PR; QC verifies)

11 files expected:
- `data/4way_lookalikes_700hand_full_2026-05-12.jsonl` (NEW; 700-hand subset)
- `scripts/generate_4way_lookalikes_700.py` (NEW; anchor-variant generator)
- `data/4way_corpus/full_700/batch_001_50hand.jsonl` (NEW; sliced first 50)
- `data/4way_corpus/full_700/batch_001_raw_labels_labeller_{1..5}.jsonl` (NEW; 5 × 50 = 250 labels)
- `data/4way_corpus/full_700/batch_001_raw_labels_opus_tierup.jsonl` (NEW; 5 Opus labels)
- `data/4way_corpus/full_700/batch_001_consensus.jsonl` (NEW; 46 consensus records)
- `data/4way_corpus/full_700/batch_001_owner_arb_queue.jsonl` (NEW; 4 arb records)
- `review/comms/BUILDER_REPORT_PHASE2E_FULL_BATCH001_2026-05-12.md` (NEW; report)

No river-rats-core/ code edits expected (pure data generation + generator script).

## Audit scope (~30-45 min — pre-merge milestone; 700-hand subset infra + 50-hand batch data audit)

### Part A — Diff scope (TC-23)

1. All PR files match builder report. NO river-rats-core/ inference/router/model/trainer edits.
2. TC-23 EXISTENCE: all paths git-tracked post-commit.
3. NO production model file edits.
4. NO consensus rule / driver script changes (frozen from PR #417).
5. NO brief / calibration / 35-hand reference / 50-hand pilot subset modifications.

### Part B — 700-hand subset validity (NEW scope vs pilot QC)

6. `data/4way_lookalikes_700hand_full_2026-05-12.jsonl` parses; exactly 700 unique 4-way records.
7. **Axis distribution exact match dispatch targets**: 4-way 3-bet/4-bet=140; multiway-cooler=70; closing-action=125; range-asymmetry=125; MW-40/45/47=100; standard 4-way SRP=140. Spot-check via grep on `primary_axis` field.
8. **No overlap** with: pilot 50-hand subset, 35-hand reference set, 29-hand calibration set. Spot-check spot_id pool independence.
9. `scripts/generate_4way_lookalikes_700.py` produces the JSONL deterministically (or with RNG-seed if non-deterministic; verify generator's seed/anchor logic).
10. Street distribution flop-heavy (509/89/87/15 vs AMENDMENT 1 51/31/11/6) — QC's job: NOTE the deviation as an architect-attested operational choice. Builder claim: 4-way decisions are flop-dominated. Acceptable.

### Part C — BATCH-001 label JSONL validity

11. Each `batch_001_raw_labels_labeller_<N>.jsonl` (N=1..5) has exactly 50 valid lines.
12. `batch_001_raw_labels_opus_tierup.jsonl` covers exactly the disputed (3-2) Sonnet spots (5 spots per builder).
13. Required fields present per pilot: spot_id, labeller_id, predicted_action, predicted_sizing_pct, confidence, bucket, reasoning, num_opponents_at_decision, primary_axis.

### Part D — Consensus rule application

14. Per design memo §4.3 rule applied correctly per spot:
    - 42 all-agree (5-of-5 Sonnet) → consensus
    - 3 4-of-5 Sonnet → consensus
    - 1 (3-2 + Opus joins majority) → consensus (CHECK)
    - 4 (3-2 + Opus disagrees) → owner-arb queue
    - 0 (2-2-1+) fragments (verify)
    - Total: 42+3+1+4 = 50 ✓
15. Sonnet consensus rate: (42+3)/50 = 90% Sonnet-only; with Opus closure = 46/50 = 92% (≥85% target ✓).
16. Spot-check 5-10 consensus.jsonl entries: state classification matches actual votes.

### Part E — Anti-rule-based attestation (CRITICAL — FL4 prevention)

17. Spot-check 5-10 random Sonnet labels across all 5 labellers: NO if/elif chains, NO threshold cutoffs (`equity > X`), NO function-definition / return-statement patterns, NO template repetition.
18. Cross-check FL4-incident pattern: NONE of the 250 labels resemble FL4's Python-script-style.
19. **Action-space confusion is a DIFFERENT category from FL4 rule-based drift** — QC should NOT classify the facing_bet=0 issue as FL4-drift (it's labeller competence on action-space rules, not threshold logic).

### Part F — Owner-arb queue integrity (4 spots)

20. 4 spots queued correctly per consensus rule (3-2 + Opus-disagrees):
    - 4WF-4-WAY-3--001: CALL ×3 / FOLD ×2 / Opus FOLD (Opus sides with minority)
    - 4WF-4-WAY-3--007: CALL ×3 / FOLD ×2 / Opus FOLD (Opus sides with minority)
    - 4WF-4-WAY-3--034: FOLD ×3 / CHECK ×2 / Opus CHECK (Opus sides with minority; **FOLD illegal when facing_bet=0**)
    - 4WF-4-WAY-3--046: FOLD ×2 / CHECK ×3 / Opus BET 25% (Opus diverges from both Sonnet camps; **facing_bet=0 spot**)
21. Verify NONE of the 4 are silently auto-adjudicated by orchestrator/builder (per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`); confirm builder surfaced them for orchestrator-pick + solver-verify queue, NOT decided.
22. **Verify labeller-readiness signal claim**: builder claims 3 of 5 disputed spots involve facing_bet=0 action-space misreads. QC reads spots 026, 034, 046 raw_labels — confirms facing_bet=0 in spot data + Sonnet labellers voted FOLD or CALL (actions illegal when no bet to face).

### Part G — Process discipline

23. **TC-X-DISPATCH-COMPLIANCE per PR #424**: builder honored Task 1 (700-hand subset) + Task 2 (5 Sonnet labellers, batch-001 only as legitimate checkpoint per dispatch §"Builder STOP-surface pattern") + Task 3 (Opus tier-up) + Task 4 (consensus) + Task 5 (arb queue handling — surfaced not adjudicated) + builder report.
24. **STOP-condition compliance**: builder honored STOP discipline (4 STOP-conditions all clean); builder did NOT improvise unilateral owner-arb adjudication; builder correctly classified labeller-readiness signal as SURFACE-FOR-TRIAGE (not STOP-IMMEDIATELY) since it's <25% owner-arb rate within tolerance.

## What this PR does NOT change

- ❌ river-rats-core/ (no code edits)
- ❌ Production code path
- ❌ Models, full corpus, training data (this is BATCH-001 only; 13 batches remain)
- ❌ Phase 1.5 ship state (vNext-HU-59 still in production)
- ❌ Solver-verification queue from §6.4 (48 spots from 1.5-D + 3 from PR #421 = 51 spots HOLD; this PR adds 0 new solver-verify items but adds 4 to owner-arb queue)
- ❌ Phase 2-F / 2-G / 2-H scope

## What gates next (post-QC-PASS orchestrator sequence)

1. Orchestrator merges PR #425 on QC PASS.
2. **Orchestrator triage on labeller-readiness signal** (orchestrator-decidable HOW per `feedback_orchestrator_decides_not_recommends.md`):
   - Path 1: continue as-is (Opus tier-up catches; owner-arb queue absorbs)
   - Path 2: brief patch (add facing_bet=0 action-space discipline boilerplate; re-spawn labellers)
   - Path 3 [QUALITY DEFAULT]: pause + 2-E.0.1 mini-pilot (10 facing_bet=0 hands with patched brief; verify discipline holds; then resume FULL batches 2-14)
3. Owner-arb queue: 4 spots → solver-verify queue (HOLD-with-accepted-risk per §6.4); 4 + 51 = 55-spot solver queue running total.
4. Orchestrator dispatches BATCH-002 per chosen path (likely Path 3 mini-pilot per quality default).

## QC routing + Output

Standalone stream. ~30-45 min wall-clock (700-hand subset axis verification + 250-Sonnet-label spot-checks + 4-arb-queue verification + labeller-readiness signal validation). QC writes:
- `~/river-rats-qc/findings/2026-05-12-pr425-phase2e-full-batch001.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2E_FULL_BATCH001_2026-05-12.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## SHOULD_FIX / BLOCKER classification guidance

- **BLOCKER**: 700-hand subset axis distribution drift from dispatch targets; labels show actual FL4-style rule-based pattern; consensus rule misapplied per §4.3; builder silently adjudicated owner-arb spots; production model edits; brief/calibration/pilot-subset tampered with; spot_id overlap with pilot/reference/calibration sets
- **SHOULD_FIX-substantive**: labellers produced <50 labels per file; rationale word count consistently <150; axis monoculture; missing required fields
- **SHOULD_FIX-process**: solver-verify queue lacks per-spot rationale; minor wording/typo; generator script missing seed for reproducibility
- **PASS**: BATCH-001 92% consensus + 700-hand subset infra independently verified bit-exact + labeller-readiness signal correctly classified (surface-for-triage, not silent-adjudication)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `bac08e1` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 2-E FULL dispatch (owner-authorized Option A): master `1d5503e` (PR #424)
- Phase 2-E pilot execution + QC PASS: master `bac08e1` (PR #423)
- Phase 2-E pilot infrastructure + QC PASS: PR #417 + #419
- Phase 2-E.0 labeller readiness + QC PASS: PR #413 + #415
- Phase 2-A design memo §4.3 consensus rule + §6.3 corpus origin: `review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md`
- 4-way labeller brief (operational): `data/4way_labeller_brief.md`
- 29-hand calibration: `data/4way_calibration_29hand_2026-05-11.jsonl`
- 50-hand pilot subset: `data/4way_lookalikes_50hand_pilot_2026-05-11.jsonl`
- Driver script: `scripts/dispatch_4way_labelling_pilot.py`
- FL4 incident (anti-rule-based motivation): `review/comms/BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md`
- Builder report: `review/comms/BUILDER_REPORT_PHASE2E_FULL_BATCH001_2026-05-12.md`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_solver_verification_queue.md`, `feedback_bucket_first_labelling.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`

**Status: QC stream — fire audit now on PR #425 Phase 2-E FULL BATCH-001 checkpoint. ~30-45 min wall-clock. 24-item audit covering 700-hand subset axis distribution + BATCH-001 data integrity (255 labels) + consensus rule application + Opus tier-up integrity + FL4-drift verification + 4-spot owner-arb queue + labeller-readiness signal validation (verify facing_bet=0 action-space misreads claim) + dispatch compliance. Builder self-assessed CHECKPOINT (92% consensus; 4 arb; no STOP-trip). After QC PASS + merge → orchestrator dispatches BATCH-002 per quality-default Path 3 (pause + 2-E.0.1 mini-pilot with patched brief on facing_bet=0 discipline before scaling to batches 2-14).**
