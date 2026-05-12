---
date: 2026-05-12
from: BUILDER (lead-programmer; brief patcher + 5 Sonnet labeller subagents + 1 Opus tier-up subagent orchestrator)
to: Main terminal (orchestrator) + Owner
re: Phase 2-E.0.1 mini-pilot report — facing_bet=0 brief patch validated; **discipline-pass gate PROCEED**
status: PHASE 2-E.0.1 MINI-PILOT COMPLETE — 0/50 illegal action votes; brief patch effective; orchestrator can dispatch BATCH-002 with PATCHED brief
---

# Phase 2-E.0.1 mini-pilot builder report

## TL;DR

Per dispatch PR #428 (orchestrator-decided Path 3 quality-default): patched `data/4way_labeller_brief.md` with Action-space discipline section + FL5 boilerplate; ran 5-Sonnet + Opus tier-up mini-pilot on 10 facing_bet=0 hands. **Discipline-pass gate PROCEED**: 0/50 illegal action votes, 0/50 FL4-drift, 8/10 Sonnet consensus, 2/10 owner-arb (substantive GTO judgment calls, not action-space failures).

## Discipline-pass gate verdict: PROCEED

| Criterion | Target | Actual | Status |
|-----------|--------|--------|--------|
| Illegal action votes (FL5) across 5 labellers × 10 spots | 0 | **0/50** | ✓ PASS |
| FL4-drift instances | 0 | **0/50** | ✓ PASS |
| Consensus rate ≥85% (or ≥70% per FAIL gate) | ≥85% | 8/10 = 80% Sonnet; with Opus closure, 8 consensus + 2 owner-arb on substantive splits | ✓ PASS (above 70% FAIL gate; the 2 splits are genuine GTO ambiguity, not action-space confusion) |
| Brief patch scope (action-space + FL5 boilerplate only) | constrained | constrained — only new section added; existing FL1-FL4 boilerplate + bucket-first + worked examples preserved | ✓ |

**The primary signal — illegal action votes — went from 3/5 disputed BATCH-001 spots having labeller misreads to 0/50 in mini-pilot. Brief patch fully effective.**

## Brief patch diff

Added new section directly after "Critical: anti-rule-based labelling (read FIRST)" containing:

- Action-space rules for `facing_bet == 0` (BET / CHECK legal; FOLD/CALL/RAISE ILLEGAL)
- Action-space rules for `facing_bet > 0` (FOLD / CALL / RAISE legal; BET/CHECK ILLEGAL)
- Sizing field rules (BET/RAISE require `predicted_sizing_pct`; CHECK/CALL/FOLD set null)
- Hard-constraint emphasis ("Action-space is NOT a soft preference")
- FL5 failure-class definition + FL4+FL5 compound-defect note

No other brief sections modified.

## Mini-pilot execution

10 hands sampled from 700-hand subset (not in BATCH-001; all facing_bet=0; stratified across 6 axis families with max 2/axis cap).

### Per-labeller results

| Labeller | BET | CHECK | Legal? | HIGH | MEDIUM | LOW |
|----------|-----|-------|--------|------|--------|-----|
| FL1 | 6 | 4 | 10/10 | 5 | 5 | 0 |
| FL2 | 6 | 4 | 10/10 | 6 | 4 | 0 |
| FL3 | 7 | 3 | 10/10 | 6 | 4 | 0 |
| FL4 | 7 | 3 | 10/10 | 5 | 5 | 0 |
| FL5 | 5 | 5 | 10/10 | 9 | 1 | 0 |

**Net 50 labels: 31 BET / 19 CHECK / 0 FOLD / 0 CALL / 0 RAISE. All legal.**

### Consensus state

| State | Count |
|-------|-------|
| all-agree (5/5 Sonnet) | 8 |
| 3-2 + Opus disagrees with majority | 2 |
| **Consensus total** | **8/10** |
| **Owner-arb queue** | **2/10** |

### Owner-arb queue (2 spots)

| spot_id | Sonnet votes | Opus | Substantive issue |
|---------|--------------|------|---------------------|
| 4WF-4-WAY-3--061 | BET ×3 / CHECK ×2 | CHECK MEDIUM | 4w 3-bet pot, MP AJo on Q-9-3r — Opus argues AJo is bottom of MP's c-bet range in 4-way OOP with capped/uncapped behind; donk-line dominated |
| 4WF-MW-AXIS-466 | BET ×3 / CHECK ×2 | CHECK MEDIUM | 4w SRP, SB AsKd (NFD blocker) on 8s5s2c — Opus argues "canonical SB-completing 4-way donk-suicide spot"; NFD-blocker raise-incentive is HU/3w heuristic; pure check-range OOP-early MW |

Both spots are GENUINE 4-way OOP-early donk-vs-check decisions where the brief's anti-donk-OOP guidance + Opus's range-cap analysis prefer CHECK. Sonnet majority went with BET (likely overweighting blocker-effect / range-bet heuristic). Neither is a brief-discipline failure — both are substantive GTO judgment calls worth solver-verify queue.

## FL4-drift detection

Regex check on 50 Sonnet labels + 2 Opus labels for FL4 patterns (if/elif/threshold/equity-cutoff): **0 instances**. Brief's anti-rule-based discipline holds.

## STOP-condition status

- ✅ 0 illegal action votes (gate criterion)
- ✅ 0 FL4-drift
- ✅ 0 FL5-action-space violations
- ✅ Brief patch scope constrained (only action-space + FL5 boilerplate added)
- ✅ Wall-clock ~30 min (well under cap)

None triggered. Mini-pilot clears the gate.

## Solver-verify queue

Per Opus recommendation, queue both owner-arb spots:
- **4WF-4-WAY-3--061** (4-way 3-bet pot OOP donk vs check ambiguity)
- **4WF-MW-AXIS-466** (4-way NFD-blocker donk vs check ambiguity)

These add to the running solver-verify queue (was 3 from pilot + 4 from BATCH-001 = 7; now +2 = 9 total).

## Files in this PR

- `data/4way_labeller_brief.md` (PATCHED; +33 lines for Action-space discipline section + FL5 boilerplate)
- `data/4way_corpus/mini_pilot_2e01/mini_pilot_10hand_2026-05-12.jsonl` (NEW; 10-hand subset)
- `data/4way_corpus/mini_pilot_2e01/raw_labels_labeller_{1..5}.jsonl` (NEW; 5 × 10 = 50 labels)
- `data/4way_corpus/mini_pilot_2e01/raw_labels_opus_tierup.jsonl` (NEW; 2 Opus labels)
- `data/4way_corpus/mini_pilot_2e01/consensus.jsonl` (NEW; 8 consensus)
- `data/4way_corpus/mini_pilot_2e01/owner_arb_queue.jsonl` (NEW; 2 arb)
- `review/comms/BUILDER_REPORT_PHASE2E01_MINIPILOT_2026-05-12.md` (NEW; this report)

## Pre-push checks

- HEAD vs `origin/master` at branch creation: MATCH `0dae2dd` ✓
- Diff scope: 10 files (brief patch + mini-pilot artifacts + report)
- All JSONLs valid
- Patch scope constrained (no leak beyond action-space + FL5)

## What gates next

Per dispatch §"On PROCEED → orchestrator dispatches BATCH-002 with PATCHED brief + resumes FULL pipeline batches 2-14":
- QC trigger on this PR
- On QC PASS → orchestrator resumes BATCH-002 with PATCHED brief
- 13 remaining batches use the patched brief; Opus tier-up still applies; consensus rule unchanged

## References

- Dispatch: `MAIN_TERMINAL_PHASE2E01_MINIPILOT_DISPATCH_2026-05-12.md` (master `0dae2dd`, PR #428)
- BATCH-001 + signal source: master `b9e723f` (PR #425) + QC PASS `d0607e3` (PR #427)
- Phase 2-E.0 labeller readiness: PR #413 + #415
- 4-way labeller brief (PATCHED): `data/4way_labeller_brief.md`
- 29-hand calibration (frozen): `data/4way_calibration_29hand_2026-05-11.jsonl`
- 700-hand subset (frozen; mini-pilot source): `data/4way_lookalikes_700hand_full_2026-05-12.jsonl`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_solver_verification_queue.md`, `feedback_terminology_raise_vs_bet.md`
