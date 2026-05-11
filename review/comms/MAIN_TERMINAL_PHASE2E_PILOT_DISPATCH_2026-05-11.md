---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous)
to: LEAD-PROGRAMMER (architect-hat + ml-architect-hat + gto-expert-hat)
re: Phase 2-E PILOT — 50-hand 5-labeller 4-way labelling pilot (analog to 1.5-D.2); pilot-first split before ~700-hand full pipeline; uses 2-E.0 brief + 29-hand calibration set
status: DISPATCH — fire now (Phase 2-E.0 merged at master a2834c6; PR #413 + #415 PASS; labeller brief + calibration validated)
---

# Phase 2-E PILOT dispatch — 50-hand 5-labeller 4-way labelling pilot

## Context

Phase 2-E.0 (PR #413) merged + QC PASS (PR #415, 0/0/1 process). 4-way labeller brief + 29-hand calibration set + single-labeller 5-hand brief validation all cleared.

Phase 2-E target per design memo §5 row 2-E: ~750 lookalike hands labelled by 5-labeller consensus to build 4-way corpus for 2-G retrain. Wall-clock estimate ~25-40h.

Per `feedback_pilot_first_for_long_jobs.md` STANDING RULE: long batches MUST split pilot+full with explicit gate. 750 hands × 5 labellers = ~3750 labels is LONG; pilot first.

Per Phase 1.5-D HU labelling lessons:
- D.2 was 50-hand pilot (surfaced FL4 rule-based methodology violation)
- D.3 was 696-hand full (recovery via explicit-anti-rule prompt)
- Phase 2-E.0 already validated brief; this pilot validates multi-labeller dynamics

## What 2-E pilot scope tests (that 2-E.0 didn't)

2-E.0 validated:
- Brief content (10 dispatch-required sections)
- Single-labeller 5-hand pilot validation (anti-rule-based discipline holds)
- Calibration set anchors

2-E pilot validates (NEW):
- **5-labeller consensus dynamics** per design memo §4.3 (≥4-of-5 → consensus; 3-2 + Opus agree → consensus; 3-2 + Opus disagree OR 2-2-1+ → owner-arb)
- **Multi-labeller drift detection** across 50 hands (would FL4-style drift have been caught by 5-labeller consensus alone?)
- **Owner-arb adjudication pattern for 4-way** (per HU 1.5-D pattern; ~10-15% owner-arb rate expected)
- **Production labeller infrastructure** end-to-end (driver + 5 instances + consensus + arb pipeline)

## What Phase 2-E pilot builds

### Task 1 — 50-hand lookalike subset

- Source: ~750-hand candidate set filtered from existing PokerBench-multiway data OR generated per 2-E lookalike generator (architect picks; see Task 2)
- Pilot subset: 50 hands sampled to cover axis space from 2-E.0 calibration set:
  - 4-way 3-bet/4-bet pots: ~10 hands
  - Multiway-cooler: ~5 hands
  - Closing-action variants: ~9 hands
  - Range-asymmetry: ~9 hands
  - MW-40/45/47: ~7 hands
  - Standard 4-way SRP: ~10 hands
- Each pilot hand has same spec format as 2-D reference set (pre-flop history, board, hero cards, opponent count, etc.)
- NOT labelled per architect's spec (architect provides only setup; labellers label)

### Task 2 — Lookalike sourcing infrastructure (if not already exists)

Architect picks source:
- Option A: PokerBench-multiway data filtered to 4-way at decision moment (preferred if sufficient volume)
- Option B: Generate via existing self-play infrastructure or analog

50-hand pilot set persisted as `data/4way_lookalikes_50hand_pilot_2026-05-11.jsonl`.

### Task 3 — 5-labeller labelling pipeline (driver + 5 instances)

Per design memo §4.3 + Phase 1.5-D pattern:
- 5 Sonnet labellers (FL1-FL5) per the brief + calibration anchors
- 1 Opus tier-up (per `feedback_pilot_first_for_long_jobs.md` sub-rule: training-data outputs require tier-up verification)
- Driver script: `river-rats-core/label_4way_pilot.py` (architect names; may live in `river-rats-core/coaching/` per CLAUDE.md)
- Each labeller produces full per-hand label per brief structure
- Consensus rule applied per spot

### Task 4 — Consensus rule + owner-arb queue

Per design memo §4.3:
- ≥4-of-5 → consensus (use majority action)
- 3-2 + Opus agree → consensus
- 3-2 + Opus disagree OR 2-2-1+ → owner-arb queue
- Owner-arb queue: surfaced via comm OR via solver-queue per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`

### Task 5 — Pilot evidence report

`review/comms/BUILDER_REPORT_PHASE2E_PILOT_2026-05-11.md` covering:
- 50 hands labelled + per-hand consensus state
- Multi-labeller drift detection (any labeller showing FL4-style rule-based pattern? — early-stop if yes)
- Owner-arb rate: expected 10-15% per HU analog; report actual
- Per-axis quality check (per design memo §5 "per-axis QC")
- Pilot gate verdict:

| Outcome | Action |
|---------|--------|
| 50/50 hands clear (no FL4-style drift; consensus pattern healthy; owner-arb rate in 5-20% range) | PROCEED to 2-E full ~700 hands |
| Mixed signal (1-2 labellers showing drift; OR owner-arb rate >25%; OR consensus collapse on >5% of hands) | REPORT to orchestrator; orchestrator triages (re-prompt vs continue with revised brief) |
| Broad fail (rule-based drift; owner-arb >40%; FL4-style methodology violation) | HALT 2-E; STOP-condition report; brief design re-iteration needed |

## What Phase 2-E pilot does NOT do

Per design memo §5 + `feedback_pilot_first_for_long_jobs.md`:

- ❌ Does NOT label the full ~700 hands (that's 2-E full scope; gates on pilot clear)
- ❌ Does NOT touch `feature_extractor.py` (surface 61 frozen)
- ❌ Does NOT touch `oracle_router.py` (2-H scope)
- ❌ Does NOT retrain (2-F / 2-G)
- ❌ Does NOT touch model artifacts
- ❌ Does NOT drain solver-verification queue (HOLD per owner-ratified §6.4); owner-arb queue from this pilot may overlap with solver queue

## STOP conditions (per CLAUDE.md §5)

- Lookalike sourcing fails (e.g., insufficient 4-way at decision moment in PokerBench-multiway data; need different source) → STOP / REPORT
- ANY labeller produces FL4-style rule-based/template/Python-script labels in first 10 hands → STOP IMMEDIATELY (saves ~$80 LLM cost on bad labels); REPORT for brief revision
- Consensus collapse rate >10% on first 20 hands → STOP / REPORT; brief or labeller config issue
- Owner-arb rate exceeds 30% on first 30 hands → STOP / REPORT (HU was 10-15%; severe deviation = drift signal)
- Wall-clock blows past ~10h (pilot estimate 3-5h × 2x buffer) → REPORT
- TC-23 EXISTENCE: 50-hand lookalike JSONL + 5-labeller output + opus output + driver + report all git-tracked

## Solver queue interaction note

Per owner-ratified §6.4 + `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`:
- Owner-arb spots from 2-E pilot may be QUEUED for solver verification later (when solver online)
- Orchestrator does NOT unilaterally adjudicate owner-arb spots; surfaces to owner per HU 1.5-D pattern
- This 2-E pilot's owner-arb count + solver-queue impact: surface in builder report; orchestrator triages adjudication strategy (could be owner-arb-by-batch OR solver-queue-defer)

## QC stream — what you audit (pre-merge milestone)

Per `feedback_qc_required_before_approval.md`:

1. **Diff scope**: 50-hand lookalike JSONL + 5-labeller outputs (5 JSONL × 50 = ~250 records OR combined) + Opus outputs + driver script + builder report; NO oracle_router / model / inference path edits; NO production-corpus modification (this is pilot subset only)
2. **Lookalike subset**: 50 hands; axis coverage per pilot Task 1 breakdown
3. **5-labeller outputs**: each labeller produces 50 labels; per-label structure complete (bucket-first; reasoning chain; multiway dimensions explicit)
4. **Anti-rule-based attestation**: independently spot-check 5-10 random labels across labellers; verify NO FL4-style patterns (if/elif/threshold/template/Python-script-style)
5. **Consensus rule application**: per-spot consensus state correctly classified per §4.3 rule (4-of-5 / 3-2+Opus / 3-2-Opus-disagree / 2-2-1+)
6. **Owner-arb queue**: spots needing arb are clearly identified; not silently auto-adjudicated by builder
7. **Per-axis QC**: each axis has reasonable label distribution (not 50 hands of all-CALL; not all axis hands clustered to single decision class)
8. **TC-X-DISPATCH-COMPLIANCE**: all 5 tasks complete; no scope leak; pilot gate evidence honest
9. **STOP-condition compliance**: builder reports any STOPs hit; did NOT improvise

QC routing: standalone. Output:
- `~/river-rats-qc/findings/2026-05-11-pr<N>-phase2e-pilot.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2E_PILOT_2026-05-11.md`
- Heartbeat update

## What gates

- Builder Phase 2-E pilot PR → QC trigger when pushed
- On QC PASS + 50/50 gate clear → orchestrator merges + handles owner-arb queue (may surface to owner OR defer to solver-queue) → dispatches 2-E full ~700 hands
- On QC PASS + mixed signal → orchestrator triages
- On QC PASS + broad fail → HALT 2-E full; brief revision
- On QC SHOULD_FIX → amend + re-fire
- On QC BLOCKER → hold
- STOP condition → REPORT

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `a2834c6` ✓
- Diff vs master: 1 file (this dispatch)
- Log vs master: 1 commit

## References

- Phase 2-E.0 builder: master `1a6f6cb` (PR #413) + QC PASS `a2834c6` (PR #415)
- Phase 2-D-FULL builder: master `b669541` (PR #409) + QC PASS `a44780f` (PR #411)
- Phase 2-A design memo: master `0e5f91f` (PR #388) + QC PASS `a221a9b` (PR #391)
- AMENDMENT 3 (labeller readiness): master `3763d8a` (PR #389)
- HU 1.5-D analog: Phase 1.5-D pilot (FL4 incident lessons) + full (recovery)
- 4-way labeller brief (production runtime): `data/4way_labeller_brief.md`
- 29-hand calibration set (anchor): `data/4way_calibration_29hand_2026-05-11.jsonl`
- 35-hand 4-way reference set (eval anchor): `data/4way_reference_35hand_2026-05-11.jsonl`
- FL4 incident: `review/comms/BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md`
- Design memo §4.3 consensus rule: `review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md`
- Design memo §5 row 2-E: lines 553
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_bucket_first_labelling.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_qc_required_before_approval.md`, `feedback_solver_verification_queue.md`, `feedback_attention_flags_when_features_change.md`

**Status: Phase 2-E PILOT dispatch — 50-hand 5-labeller 4-way labelling pilot per pilot-first standing rule. Tests multi-labeller consensus dynamics + drift detection + owner-arb pattern that 2-E.0 single-labeller validation didn't cover. Pilot gates: 50/50 PROCEED → 2-E full ~700 hands; mixed → triage; broad fail → HALT brief revision. Architect estimate ~3-5h. After 2-E pilot PASS → 2-E full → 2-F (3-way retrain) → 2-G (4-way retrain) → 2-H (production swap).**
