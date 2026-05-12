---
date: 2026-05-12
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #429 — Phase 2-E.0.1 mini-pilot (facing_bet=0 brief patch + 10-hand 5-Sonnet + Opus tier-up; discipline-pass gate PROCEED; 0/50 illegal votes; 8/10 consensus; 2 substantive owner-arb) — fire audit now (pre-merge milestone)
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #429 (Phase 2-E.0.1 mini-pilot)

PR #429: `builder-phase2-e01-minipilot-2026-05-12`. Pushed 11:05 SAST (~30 min after dispatch PR #428 landed at master `0dae2dd`). Title: "Builder Phase 2-E.0.1 mini-pilot — brief patched; 0/50 illegal votes; PROCEED gate".

**Builder self-assessment: PROCEED** — discipline-pass gate cleared.

## Pilot results summary (from builder report)

- **Brief patched** (`data/4way_labeller_brief.md`; +33 lines for action-space discipline section + FL5 boilerplate; no other sections modified)
- **0/50 illegal action votes** (5 labellers × 10 facing_bet=0 spots = 50 votes; 31 BET + 19 CHECK + 0 FOLD + 0 CALL + 0 RAISE)
- **0 FL4-drift** instances
- **8/10 consensus** (5-of-5 all-agree) + **2/10 owner-arb** (3-2+Opus-disagrees; substantive GTO judgment calls)
- **Wall-clock ~30 min** (well under cap)
- **Solver-verify queue updates**: builder adds 2 spots (4WF-4-WAY-3--061 OOP donk vs check ambiguity; 4WF-MW-AXIS-466 NFD-blocker donk vs check); running total per orchestrator tracking: 48 (1.5-D) + 3 (pilot) + 4 (BATCH-001) + 2 (mini-pilot) = 57 spots HOLD per §6.4.

## Diff summary (per builder PR; QC verifies)

10 files expected:
- `data/4way_labeller_brief.md` (PATCHED; +33 lines)
- `data/4way_corpus/mini_pilot_2e01/mini_pilot_10hand_2026-05-12.jsonl` (NEW; 10-hand subset)
- `data/4way_corpus/mini_pilot_2e01/raw_labels_labeller_{1..5}.jsonl` (NEW; 5 × 10 = 50 labels)
- `data/4way_corpus/mini_pilot_2e01/raw_labels_opus_tierup.jsonl` (NEW; 2 Opus labels)
- `data/4way_corpus/mini_pilot_2e01/consensus.jsonl` (NEW; 8 consensus)
- `data/4way_corpus/mini_pilot_2e01/owner_arb_queue.jsonl` (NEW; 2 arb)
- `review/comms/BUILDER_REPORT_PHASE2E01_MINIPILOT_2026-05-12.md` (NEW; report)

No river-rats-core/ code edits expected.

## Audit scope (~20-30 min — pre-merge milestone; brief-patch + 10-hand subset audit)

### Part A — Diff scope (TC-23)

1. All PR files match builder report. NO river-rats-core/ inference/router/model/trainer edits.
2. TC-23 EXISTENCE: all paths git-tracked post-commit.
3. NO production model file edits.
4. NO consensus rule / driver script changes (frozen from PR #417).
5. NO 29-hand calibration / 35-hand reference / 50-hand pilot subset / 700-hand subset modifications.
6. NO BATCH-001 label files modified (frozen at master b9e723f).

### Part B — Brief patch scope (CRITICAL — patch-scope-constraint)

7. **Brief patch ONLY adds action-space discipline section + FL5 boilerplate**. Verify:
   - Existing FL1-FL4 boilerplate untouched
   - Bucket-first section untouched
   - Worked examples untouched
   - Per-villain range chain requirement untouched
   - Anti-rule-based section untouched (only ADDS the new section after it)
   - No deletions; no reorderings; no rewording of existing content
8. Patch content includes:
   - **facing_bet == 0 rule**: BET / CHECK legal; FOLD / CALL / RAISE illegal
   - **facing_bet > 0 rule**: FOLD / CALL / RAISE legal; BET / CHECK illegal
   - **Sizing field rule**: BET/RAISE require predicted_sizing_pct; CHECK/CALL/FOLD null
   - **Hard-constraint emphasis** (not soft preference)
   - **FL5 failure-class** + FL4+FL5 compound-defect note
9. Terminology consistent with `feedback_terminology_raise_vs_bet.md` (raise vs bet vs open; no confusion).

### Part C — 10-hand subset validity

10. **10 hands in `mini_pilot_10hand_2026-05-12.jsonl`**; all valid JSONL.
11. **ALL 10 hands have `facing_bet == 0`** (verify field in subset; this is the entire point of the mini-pilot).
12. **No spot_id overlap** with BATCH-001's 50 hands (`batch_001_50hand.jsonl`).
13. Stratification: ≤2 hands per axis family (per dispatch §Task 2 cap); 6-axis-family coverage.

### Part D — Label JSONL validity

14. Each `raw_labels_labeller_<N>.jsonl` has 10 valid lines (5 × 10 = 50 Sonnet labels).
15. `raw_labels_opus_tierup.jsonl` covers exactly the 2 disputed (3-2) Sonnet spots (per builder report: 061 + 466).
16. Required fields per pilot pattern (spot_id, labeller_id, predicted_action, predicted_sizing_pct, confidence, bucket, reasoning, num_opponents_at_decision, primary_axis).

### Part E — Discipline-pass gate verification (CRITICAL — primary signal)

17. **0 illegal action votes across all 50 Sonnet votes** (5 labellers × 10 facing_bet=0 spots):
    - For each label: verify `predicted_action ∈ {BET, CHECK}` ONLY (FOLD/CALL/RAISE all illegal when facing_bet=0)
    - Per-labeller counts in builder report: FL1 [6 BET / 4 CHECK], FL2 [6 BET / 4 CHECK], FL3 [7 BET / 3 CHECK], FL4 [7 BET / 3 CHECK], FL5 [5 BET / 5 CHECK] → 31 BET + 19 CHECK = 50 legal votes
18. **No CALL/FOLD/RAISE anywhere** across the 50 Sonnet labels (spot-check via grep on predicted_action field).
19. Opus 2 labels also legal (BET or CHECK only; spot-check).

### Part F — Anti-rule-based attestation (FL4 prevention; still applies)

20. Spot-check 5-10 random Sonnet labels: NO if/elif chains, NO threshold cutoffs (`equity > X`), NO function-definition / return-statement patterns, NO template repetition.
21. Cross-check FL4 pattern: NONE of the 50 labels resemble FL4's Python-script-style.
22. **No FL5 violations** beyond the gate criterion (since 0 illegal votes confirmed in Part E).

### Part G — Consensus rule + owner-arb queue

23. Per design memo §4.3:
   - 8 all-agree (5-of-5) → consensus ✓
   - 2 (3-2 + Opus disagrees with majority) → owner-arb queue ✓
   - Total: 8+2 = 10 ✓
   - Sonnet consensus rate: 8/10 = 80% (below 85% target but above 70% FAIL gate; builder explains as substantive GTO ambiguity, not action-space confusion)
24. **Owner-arb queue VERIFY** (2 spots):
   - **4WF-4-WAY-3--061**: Sonnet BET ×3 / CHECK ×2; Opus CHECK; 4-way 3-bet pot MP AJo OOP on Q-9-3r
   - **4WF-MW-AXIS-466**: Sonnet BET ×3 / CHECK ×2; Opus CHECK; 4-way SRP SB AsKd (NFD blocker) on 8s5s2c
   - **Both spots have facing_bet=0** (verify in subset data); Sonnet/Opus disagreement is **about whether to BET or CHECK** (both legal), NOT illegal-action confusion. This is a GENUINE GTO judgment call; correctly classified as owner-arb (substantive) not action-space (procedural) failure.

### Part H — Process discipline

(Embedded above in Part B + Part C + Part G.)

## What this PR does NOT change

- ❌ river-rats-core/ (no code edits)
- ❌ Production code path
- ❌ Models, full corpus, training data (this is mini-pilot only; 13 batches still pending)
- ❌ BATCH-001 labels (frozen)
- ❌ Phase 1.5 ship state (vNext-HU-59 in production)
- ❌ Phase 2-F / 2-G / 2-H scope

## What gates next (post-QC-PASS orchestrator sequence)

1. Orchestrator merges PR #429 on QC PASS (PROCEED gate cleared).
2. Orchestrator dispatches **BATCH-002 with PATCHED brief** (50 hands; same 5-Sonnet + Opus pipeline; resumes FULL pipeline batches 2-14).
3. Solver-verify queue: +2 spots (running total per orchestrator tracking: 57 spots HOLD per §6.4).
4. Owner-arb queue from mini-pilot (2 spots): substantive GTO; HOLD per `feedback_solver_verification_queue.md`; not blocking.

## QC routing + Output

Standalone stream. ~20-30 min wall-clock (brief-patch scope + 10-hand-subset + 50-Sonnet-label illegal-vote verification + 2-spot arb queue substantiveness check). QC writes:
- `~/river-rats-qc/findings/2026-05-12-pr429-phase2e01-minipilot.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2E01_MINIPILOT_2026-05-12.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## SHOULD_FIX / BLOCKER classification guidance

- **BLOCKER**: ≥1 illegal action vote across 50 Sonnet votes (PRIMARY GATE FAILURE); brief patch leaks beyond action-space + FL5; consensus rule misapplied; production model/code edits; spot_id overlap with BATCH-001
- **SHOULD_FIX-substantive**: <10 labels per file; rationale word count consistently <150; missing required fields; FL4-drift detected
- **SHOULD_FIX-process**: minor wording/typo in brief patch; owner-arb classification ambiguity
- **PASS**: 0 illegal votes verified bit-exact + brief patch scope constrained + consensus + arb queue substantively-GTO-not-procedurally-broken

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `0dae2dd` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 2-E.0.1 dispatch (Path 3 quality-default): master `0dae2dd` (PR #428)
- Phase 2-E FULL BATCH-001 + QC PASS: master `b9e723f` (PR #425 + #427)
- Phase 2-E FULL dispatch (Option A authorized): master `1d5503e` (PR #424)
- Phase 2-E pilot execution + QC PASS: master `bac08e1` (PR #423)
- Phase 2-E.0 labeller readiness + QC PASS: PR #413 + #415
- 4-way labeller brief (PATCHED): `data/4way_labeller_brief.md`
- 29-hand calibration: `data/4way_calibration_29hand_2026-05-11.jsonl`
- 700-hand subset (mini-pilot source): `data/4way_lookalikes_700hand_full_2026-05-12.jsonl`
- BATCH-001 subset (non-overlap target): `data/4way_corpus/full_700/batch_001_50hand.jsonl`
- Driver script: `scripts/dispatch_4way_labelling_pilot.py`
- FL4 incident (anti-rule motivation): `review/comms/BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md`
- Builder report: `review/comms/BUILDER_REPORT_PHASE2E01_MINIPILOT_2026-05-12.md`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_solver_verification_queue.md`, `feedback_bucket_first_labelling.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`

**Status: QC stream — fire audit now on PR #429 Phase 2-E.0.1 mini-pilot. ~20-30 min wall-clock. 24-item audit covering brief-patch scope constraint (BLOCKER if leaks beyond action-space + FL5) + 10-hand subset validity (all facing_bet=0; no BATCH-001 overlap) + 50-Sonnet-vote illegal-action verification (PRIMARY GATE — BLOCKER if ≥1 illegal) + 2-Opus-tier-up integrity + consensus rule application + 2-spot owner-arb queue substantiveness (GTO judgment vs action-space failure) + FL4-drift verification. Builder self-assessed PROCEED gate clear. After QC PASS + merge → orchestrator dispatches BATCH-002 with PATCHED brief (resumes FULL pipeline batches 2-14).**
