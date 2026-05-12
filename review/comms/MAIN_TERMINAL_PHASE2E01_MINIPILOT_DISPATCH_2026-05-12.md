---
date: 2026-05-12
from: Main terminal (orchestrator; standing-directive autonomous; quality default)
to: LEAD-PROGRAMMER (spawns 5 Sonnet labeller subagents + 1 Opus tier-up subagent at 10-hand mini-pilot scale)
re: Phase 2-E.0.1 mini-pilot — facing_bet=0 action-space discipline patch + 10-hand re-pilot before resuming BATCH-002..014 per orchestrator-decided Path 3 quality-default
status: DISPATCH — fire now (Path 3 chosen per quality-default standing rule; PR #425 QC PASS at master b9e723f)
---

# Phase 2-E.0.1 mini-pilot dispatch — facing_bet=0 action-space discipline patch + 10-hand re-pilot

## Orchestrator triage record (2026-05-12)

PR #425 (Phase 2-E FULL BATCH-001) cleared QC at PASS (0/0/0; master b9e723f). Builder surfaced labeller-readiness signal: **3 of 5 disputed BATCH-001 spots (026/034/046) had Sonnet labellers voting illegal actions** (FOLD/CALL when facing_bet=0; only BET/CHECK are legal). 4 owner-arb spots; 2 of them (034/046) trace directly to action-space illegal-vote pattern; spot 026 also facing_bet=0 with Opus joining a 2-2-1 fragment.

QC findings (`2026-05-12-pr425-phase2e-full-batch001.md`) verified the signal bit-exact + classified it as **brief-completeness gap** (distinct from FL4 rule-based drift; action-space failure is upstream of poker-reasoning quality).

**Builder presented Paths 1/2/3** per `feedback_orchestrator_decides_not_recommends.md`. Orchestrator decision per quality-default standing rule (`feedback_quality_default_no_ask.md` + `feedback_pilot_first_for_long_jobs.md`):

**PATH 3 — pause + 2-E.0.1 mini-pilot**

Rationale:
- Action-space confusion is a labelling instrument defect; patching brief is the root-cause fix
- A brief patch is a non-trivial change to the labelling instrument; standing rule requires pilot-first verification
- Mini-pilot cost is ~$5-10 + 30min; saves ~$X across 13 remaining batches if patch reveals additional brief issues
- Alternative (Path 1 continue) leaves Opus tier-up burden carrying brief-completeness debt across 650 more hands; alternative (Path 2 patch-and-scale) skips verification of the patch itself

Owner authorization for FULL ~700-hand scope (master 1d5503e, PR #424) extends to corrective scaffolding within scope. No re-authorization needed for orchestrator-decided HOW per `feedback_orchestrator_decides_not_recommends.md`.

## Scope of 2-E.0.1 mini-pilot

### Task 1 — Brief patch: action-space discipline section

Edit `data/4way_labeller_brief.md`:
- Add new section (likely after the bucket-first / action-space section, or as a new top-level rule block) titled "Action-space discipline: when each action is LEGAL"
- Content must include explicit rules:
  - **When `facing_bet == 0`** (no bet to call): legal actions are **BET / CHECK only**. FOLD and CALL are ILLEGAL.
  - **When `facing_bet > 0`** (facing a bet): legal actions are **FOLD / CALL / RAISE only**. BET and CHECK are ILLEGAL (CHECK only legal if there's no bet to face).
  - **When `predicted_action` is BET or RAISE**: must specify `predicted_sizing_pct`. If CHECK/CALL/FOLD, omit sizing.
  - Action-space is a HARD constraint, NOT a soft preference. If you find yourself reaching for an illegal action, your reasoning has departed from the actual decision moment.
- Reuse existing terminology per `feedback_terminology_raise_vs_bet.md` (raise = raise of existing bet; bet = first postflop bet)
- Add to the brief's existing "Common labeller mistakes" or analog section: "FL5: voting an illegal action (e.g., FOLD when facing_bet=0). If your label cites threshold-style reasoning to reach an illegal action, your label is wrong twice over (FL4 drift + FL5 action-space)."
- No other brief edits; preserve all existing FL1-FL4 boilerplate + bucket-first + worked examples + per-villain range chain requirements

### Task 2 — Select 10-hand facing_bet=0 mini-pilot subset

From `data/4way_lookalikes_700hand_full_2026-05-12.jsonl`:
- Filter to `facing_bet == 0` hands
- Exclude hands already in `data/4way_corpus/full_700/batch_001_50hand.jsonl` (batch-001 already labelled with un-patched brief)
- Sample 10 hands stratified across the 6 axis families (cap any single family at 3 of 10)
- Persist as `data/4way_corpus/mini_pilot_2e01/mini_pilot_10hand_2026-05-12.jsonl`

### Task 3 — 5 fresh Sonnet labeller subagents + Opus tier-up

Same pattern as PR #421 + PR #425:
- Each labeller reads PATCHED `data/4way_labeller_brief.md` + `data/4way_calibration_29hand_2026-05-11.jsonl` + the 10-hand JSONL
- Each produces 10 labels with full reasoning chains
- Output: `data/4way_corpus/mini_pilot_2e01/raw_labels_labeller_<N>.jsonl` for N ∈ {1,2,3,4,5}
- Opus tier-up on 3-2 disputes: `data/4way_corpus/mini_pilot_2e01/raw_labels_opus_tierup.jsonl`
- Consensus per design memo §4.3: `data/4way_corpus/mini_pilot_2e01/consensus.jsonl` + `owner_arb_queue.jsonl`

### Task 4 — Discipline-pass gate evaluation

**PROCEED gate (mini-pilot PASS)**:
- **0 illegal action votes across all 5 Sonnet labellers** (10 hands × 5 labellers = 50 votes; all must be BET or CHECK since all are facing_bet=0)
- Consensus rate ≥85% on 10-hand subset
- 0 FL4-drift instances
- 0 FL5-action-space violations (the new failure class added by patch)

**FAIL gate (any of)**:
- ≥1 illegal action vote
- Consensus rate <70%
- FL4-drift detected

On PROCEED → orchestrator dispatches BATCH-002 with PATCHED brief + resumes FULL pipeline batches 2-14.

On FAIL → STOP-surface for orchestrator triage; do NOT improvise additional brief edits; report builder observation comm with failure diagnostics.

### Task 5 — Final mini-pilot evidence report

`review/comms/BUILDER_REPORT_PHASE2E01_MINIPILOT_2026-05-12.md`:
- 10/10 labels per labeller delivered (50 Sonnet + Opus tier-up)
- Discipline-pass gate verdict (PROCEED / FAIL with per-violation rationale)
- Per-labeller illegal-action vote counts (target: 0 across all 5)
- Consensus rate
- FL4 + FL5 drift check
- Brief diff (so orchestrator/QC can audit patch scope)

## STOP-IMMEDIATELY conditions

- ANY labeller produces FL4-style rule-based labels → STOP IMMEDIATELY; REPORT
- ANY labeller produces ≥1 illegal action vote on facing_bet=0 spots (gate FAIL) → STOP and report (NOT a methodology violation; this is the gate working as designed)
- Brief patch scope leaks beyond action-space discipline section + FL5 boilerplate → STOP / REPORT
- TC-23 EXISTENCE: all output JSONL files + patched brief + builder report git-tracked

## What 2-E.0.1 does NOT do

- ❌ Does NOT touch river-rats-core/ code
- ❌ Does NOT touch oracle_router / model files / inference path / FEATURE_COLUMNS
- ❌ Does NOT retrain models
- ❌ Does NOT modify 29-hand calibration set, 35-hand reference set, 50-hand pilot subset, BATCH-001 labels
- ❌ Does NOT re-label BATCH-001 spots (already labelled at master 8e57307 + b9e723f; downstream Opus tier-up closure on 026 was acceptable; 4 arb spots queued for solver-verify per §6.4; not re-opening)
- ❌ Does NOT drain solver-verification queue (55 spots HOLD per §6.4)
- ❌ Does NOT generate new lookalike subset (uses existing 700-hand JSONL)
- ❌ Does NOT modify driver script `scripts/dispatch_4way_labelling_pilot.py` (frozen from PR #417; reuse as-is)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `b9e723f` ✓
- Diff vs master: 1 file (this dispatch)
- Log vs master: 1 commit

## References

- Phase 2-E FULL BATCH-001 + QC PASS: master `b9e723f` (PR #425 + #427)
- Phase 2-E FULL dispatch (Option A authorized): master `1d5503e` (PR #424)
- Phase 2-E pilot execution + QC PASS: master `bac08e1` (PR #423)
- Phase 2-E.0 labeller readiness + QC PASS: PR #413 + #415
- 4-way labeller brief (target of patch): `data/4way_labeller_brief.md`
- 29-hand calibration (frozen): `data/4way_calibration_29hand_2026-05-11.jsonl`
- 700-hand subset (frozen; mini-pilot source): `data/4way_lookalikes_700hand_full_2026-05-12.jsonl`
- BATCH-001 evidence (where labeller-readiness signal originated): `review/comms/BUILDER_REPORT_PHASE2E_FULL_BATCH001_2026-05-12.md`
- QC findings on signal verification: `review/comms/REVIEW_QC_PHASE2E_FULL_BATCH001_2026-05-12.md` (cross-post) + `~/river-rats-qc/findings/2026-05-12-pr425-phase2e-full-batch001.md`
- Driver script (reuse): `scripts/dispatch_4way_labelling_pilot.py`
- FL4 incident (anti-rule-based motivation): `review/comms/BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_aligned_sizing.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`

**Status: Phase 2-E.0.1 mini-pilot dispatch — orchestrator-decided Path 3 quality-default per labeller-readiness signal on facing_bet=0 action-space confusion. Builder patches brief (add action-space discipline section + FL5 boilerplate), selects 10 facing_bet=0 hands NOT in BATCH-001, spawns 5 Sonnet labellers + Opus tier-up with PATCHED brief, evaluates discipline-pass gate (0 illegal action votes required for PROCEED). On PROCEED → orchestrator resumes BATCH-002..014 with PATCHED brief. On FAIL → STOP and surface for triage. Owner-authorization for FULL scope extends to this corrective scaffolding per orchestrator-decides-HOW principle.**
