---
date: 2026-05-12
from: BUILDER (lead-programmer; 5 Sonnet labeller subagents + 1 Opus tier-up subagent orchestrator)
to: Main terminal (orchestrator) + Owner
re: Phase 2-E FULL — 700-hand subset generated + BATCH-001 (50/700) labelling complete; **labeller-readiness signal surfaced** for orchestrator review before continuing
status: CHECKPOINT — 50/700 labelled (consensus 46/50 = 92%); 13 batches remaining; orchestrator triage requested on labeller-readiness signal before batch-002
---

# Phase 2-E FULL builder report — BATCH-001 (50/700) checkpoint

## TL;DR

Per dispatch PR #424 (owner-authorized Option A full ~700-hand execution): generated 700-hand 4-way lookalike subset via systematic anchor-variant generator script; executed BATCH-001 (first 50 hands) via 5 Sonnet labellers + Opus tier-up. **BATCH-001 consensus 92%** (46/50). 4 owner-arb spots flagged. **Labeller-readiness signal detected on 3 of 5 disputed spots** (facing_bet=0 action-space misreads) — surfaced for orchestrator triage before continuing batches 2-14.

## Infrastructure delivered (Task 1 + 2)

### 700-hand lookalike subset

- `data/4way_lookalikes_700hand_full_2026-05-12.jsonl` — 700 unique 4-way lookalikes
- `scripts/generate_4way_lookalikes_700.py` — generator (anchor-variant strategy)

**Axis distribution (exact match to dispatch targets)**:

| Axis | Target | Delivered |
|------|--------|-----------|
| 4-way 3-bet/4-bet | 140 | 140 |
| Multiway-cooler | 70 | 70 |
| Closing-action | 125 | 125 |
| Range-asymmetry | 125 | 125 |
| MW-40/45/47 axis | 100 | 100 |
| Standard 4-way SRP | 140 | 140 |
| **Total** | **700** | **700** |

**Street distribution**: 509 flop / 89 preflop / 87 turn / 15 river. **Deviation from AMENDMENT 1** (target 51/31/11/6 = 357/217/77/42): inherited from anchor flop-heavy distribution. Architect-attested as acceptable for 4-way training where flop decisions dominate; surfaced for orchestrator awareness.

**Generation method**: compound variant strategy (suit rotation + board brick swap + hero kicker substitution + position rotation + stack-depth + action micro-variant; 1-3 variants applied per anchor across 114-anchor pool).

## BATCH-001 results (Task 3 + 4)

### Consensus

| State | Count | Rate |
|-------|-------|------|
| all-agree (5/5 Sonnet) | 42 | 84% |
| 4-of-5 Sonnet | 3 | 6% |
| 3-2 + Opus joins → CHECK | 1 | 2% |
| 3-2 + Opus disagrees → owner-arb | 4 | 8% |
| **Total consensus** | **46** | **92%** |
| **Owner-arb queue** | **4** | **8%** |

### Consensus action distribution

BET 24 / CHECK 9 / CALL 6 / FOLD 4 / RAISE 3 — heavily BET-skewed because BATCH-001 contains the bulk of 3-bet pot axis spots (preflop 3-bettor c-betting strong ranges).

## Owner-arb queue (4 spots)

| spot_id | Sonnet votes | Opus | Action |
|---------|--------------|------|--------|
| 4WF-4-WAY-3--001 | CALL ×3 / FOLD ×2 | FOLD MED | TT underpair on A-high 3-bet pot 4-way; Opus sides with minority (squeeze-risk realization drop) |
| 4WF-4-WAY-3--007 | CALL ×3 / FOLD ×2 | FOLD MED | JTo dominated 3-bet pot; suited threshold |
| 4WF-4-WAY-3--034 | FOLD ×3 / CHECK ×2 | CHECK LOW | **facing_bet=0 — FOLD is illegal action**; labeller misread |
| 4WF-4-WAY-3--046 | FOLD ×2 / CHECK ×3 | BET 25% LOW | **facing_bet=0 — FOLD/CHECK are valid; Opus BET diverges** |

All 4 queued per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`.

## 🚨 LABELLER-READINESS SIGNAL (SURFACED FOR ORCHESTRATOR TRIAGE)

**3 of 5 disputed spots involve action-space confusion**:
- Spots 026, 034, 046 have `facing_bet=0` (no bet to call/fold)
- Multiple Sonnet labellers voted **CALL or FOLD** — actions NOT in the legal action space
- Spot 026 had 2 Sonnet labellers vote CALL when only BET/CHECK are valid
- Spot 034 had 3 Sonnet labellers vote FOLD when only BET/CHECK are valid
- Spot 046 had 2 Sonnet labellers vote FOLD when only BET/CHECK are valid

**Why this matters**: this is the kind of brief-discipline failure the 2-E.0 readiness gate was supposed to catch. The 50-hand pilot did not surface this because pilot spots were more constrained. With 700-hand FULL scope, the brief's action-space discipline is being stress-tested.

**Three orchestrator-decidable paths**:
1. **Continue as-is**: Opus tier-up catches these (as it did here); owner-arb queue absorbs them. Estimated impact across 700 hands: ~30-50 spots in owner-arb queue (vs target ~35-105). Within range.
2. **Brief patch**: add explicit "DO NOT predict FOLD/CALL when facing_bet=0 — only BET/CHECK are legal" boilerplate to brief; re-spawn labellers for batches 2-14 with patched brief.
3. **Pause + 2-E.0.1 mini-dispatch**: run a 10-hand pilot of facing_bet=0 spots with patched brief; confirm labeller discipline holds; then resume FULL.

Per `feedback_orchestrator_decides_not_recommends.md`: I'm flagging the signal + presenting paths; orchestrator decides.

## Anti-rule-based attestation (BATCH-001)

All 250 Sonnet labels + 5 Opus labels verified for FL4-pattern absence:
- ✅ No if/elif chains
- ✅ No threshold logic
- ✅ No template repetition (cross-checked across labellers)
- ✅ No Python-script style
- ✅ No equity-percentage cutoffs as rules
- ✅ Per-villain range chains present
- ✅ Equity-realization factors cited
- ✅ Bucket-first compliance

(Action-space confusion is a DIFFERENT category from FL4-rule-based-drift — it's labeller competence on the brief's action-space rules.)

## STOP-condition status

| Condition | Threshold | Actual | Status |
|-----------|-----------|--------|--------|
| FL4 drift first-50 hands | 0 drift | 0 drift | ✓ |
| Consensus collapse first-100 | <10% | 8% (4/50) | ✓ |
| Owner-arb rate first-200 | <25% | 8% (4/50) | ✓ |
| Wall-clock | <50h | ~1.5h for batch-001 | ✓ |

None triggered. The labeller-readiness signal is OPERATIONAL (worth surfacing) but not a hard STOP.

## Files in this PR

- `data/4way_lookalikes_700hand_full_2026-05-12.jsonl` (NEW; 700-hand subset)
- `scripts/generate_4way_lookalikes_700.py` (NEW; generator script)
- `data/4way_corpus/full_700/batch_001_50hand.jsonl` (NEW; sliced first 50)
- `data/4way_corpus/full_700/batch_001_raw_labels_labeller_{1..5}.jsonl` (NEW; 5 × 50 = 250 labels)
- `data/4way_corpus/full_700/batch_001_raw_labels_opus_tierup.jsonl` (NEW; 5 Opus labels)
- `data/4way_corpus/full_700/batch_001_consensus.jsonl` (NEW; 46 consensus records)
- `data/4way_corpus/full_700/batch_001_owner_arb_queue.jsonl` (NEW; 4 arb records)
- `review/comms/BUILDER_REPORT_PHASE2E_FULL_BATCH001_2026-05-12.md` (NEW; this report)

## Pre-push checks

- HEAD vs `origin/master` at branch creation: MATCH `bac08e1` ✓
- Diff scope: 11 files (700-hand subset + generator + 1 batch labelling artifacts)
- All JSONLs valid + parseable
- Axis distribution exact match dispatch targets

## What gates next

- QC trigger when this PR is pushed
- **Orchestrator triage on labeller-readiness signal**: decide path 1/2/3 above before batches 2-14 fire
- On orchestrator decision → BATCH-002 (next 50 hands) per chosen path

## Remaining work (13 batches, 650 hands)

- BATCH-002 through BATCH-014: 50-hand each
- Same pipeline (5 Sonnet + Opus tier-up + consensus + arb queue)
- Final corpus assembly at BATCH-014: combine pilot 50 + full 700 = 750-hand 4-way corpus

## References

- Dispatch: `MAIN_TERMINAL_PHASE2E_FULL_DISPATCH_2026-05-12.md` (master `1d5503e`, PR #424)
- Phase 2-E pilot execution: master `8e57307` (PR #421) + QC PASS `bac08e1` (PR #423)
- Phase 2-E.0 brief: PR #413
- 4-way labeller brief: `data/4way_labeller_brief.md`
- 29-hand calibration: `data/4way_calibration_29hand_2026-05-11.jsonl`
- Driver script: `scripts/dispatch_4way_labelling_pilot.py`
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`
