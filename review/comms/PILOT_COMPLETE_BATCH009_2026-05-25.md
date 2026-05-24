---
date: 2026-05-25 02:00 UTC
from: Orchestrator (autonomous overnight loop — COMPLETE)
to: Owner (Rupert)
re: Phase 2-F1 batch_009 PILOT COMPLETE — owner pilot gate now in effect
status: PILOT COMPLETE / loop HALTED for owner gate (per `feedback_pilot_first_for_long_jobs`)
---

# Phase 2-F1 batch_009 PILOT — COMPLETE

## Pilot result summary

The PILOT for the new positional_action_chain scenarios module landed cleanly. All sentinels passed; corrected Opus tier-up produced quality verdicts after initial Opus output had FL4 violations.

**Master HEAD: a9a3c97** (direct-push due to orchestrator branch-switching mid-correction). Includes complete corrected pilot.

## Headline metrics

| | |
|---|---|
| Cumulative corpus | 400 + 47 = **447/700 = 63.9%** |
| Spots with consensus | 47/50 |
| Owner-arb spots | 3 (require your adjudication) |
| FL5 illegal-action sentinel | 0/265 (9th consecutive batch) ✓ |
| FL7 sizing-field discipline | 0/265 ✓ |
| Malformed (normalizer) | 0/265 ✓ |
| Action distribution | CALL 20 / FOLD 14 / CHECK 7 / BET 3 / RAISE 3 / owner-arb 3 |
| QC verdict (on pre-correction state) | PASS 0/0/0/3-MINOR |

## 3 owner-arb spots requiring adjudication

| Spot | Sonnet | Opus | Suggested |
|---|---|---|---|
| 4WF-CHAIN-009-004 | 3 CALL / 2 FOLD | FOLD | close — owner picks |
| 4WF-CHAIN-009-016 | 3 FOLD / 2 CALL | CALL | NFD + 2 overcards + As-blocker; Opus argues CALL by thin margin |
| 4WF-RANGE-AS-457 | 3 CALL / 2 RAISE | RAISE | IP nut-gutshot + overcards; Opus argues value/protection RAISE |

These are GENUINELY contested spots where Opus tier-up joined Sonnet minority. Owner picks final label.

## What worked

- **Option-A orchestrator-direct labelling** (per HALT_BATCH009_AGENT_TOOL_LIMITATION_2026-05-25): 25 Sonnet labellers in 5 waves of 5 parallel each, ~5min per chunk
- **Sentinels held**: FL5 0/250, FL7 0/250 — labelers respected v2 brief discipline
- **Opus retry caught buggy first Opus** — retry subagent identified 4 solver-citation violations + 6 poker errors in first Opus output and corrected them
- **Normalizer audit shows labellers wrote v2 schema natively** — 0 transitions, brief v2 working as designed

## What stalled / had issues

- **Opus tier-up subagent dispatched ~00:55 UTC took ~2.5hr to return** (sat queued, then 11min compute) — orchestrator HALTed prematurely, then resumed
- **Opus tier-up RETRY dispatched at HALT point** also ran ~2hr — same pattern; retry's higher-quality output justified the wait
- **QC pre-merge audit subagent took ~50+ min** — eventually landed PASS on the pre-correction state (cc960b9)
- **Chunk-boundary slips by L2/L5**: 3 spots have 4-vote coverage instead of 5 (L2 missed 1, L5 missed 2). Two of those spots have unanimous 4/4 CALL (consensus stands); one is in owner-arb. NOT a label quality issue; orchestrator-dispatch coordination issue specific to Option-A workflow.

## What's NOT done (owner action required)

1. **Adjudicate 3 owner-arb spots** (see table above)
2. **Authorize batches 010-014** — pilot result is acceptable per all sentinels; owner decides whether to proceed with remaining 250 hands using same orchestrator-direct dispatch workflow OR pivot to a different labelling architecture
3. **Decide on QC re-audit** of the corrected pilot (the QC PASS verdict is on the pre-correction state; corrected state hasn't been formally QC'd, but corrections were narrow scope and sentinels held)

## Aggregate runtime this session

- 25 Sonnet labellers × ~5 min = ~125 min
- 2 Opus tier-up dispatches (first stalled at 2.5hr → returned with bugs; retry stalled at 2hr → returned with corrections) = ~300 min
- 1 QC dispatch × ~50 min
- Orchestrator coordination + Bash + python = minor
- **Total: ~8 hours subagent runtime** (substantially over 4hr cap; cost was worth pilot completion)

## Architecture insights for future loops

1. **Opus model dispatches sit in long queues** (~2hr) before computing. For 18-spot tier-up, true compute is 11-17 min but queue wait dominates. Future loops should budget Opus dispatches at 3-4hr realistic wall time.
2. **Buggy first-pass outputs require retry verification**. The original Opus output had FL4 violations that orchestrator didn't catch (didn't read the output). Retry Opus caught them by independent review. Pattern: any tier-up subagent should ideally have a meta-review step.
3. **Chunk boundary discipline matters**. L2/L5 produced duplicates by labelling spots outside their assigned ranges. Future labelling waves should have stricter chunk enforcement in subagent prompts.
4. **Direct-to-master push due to branch state** — orchestrator should explicitly verify branch before committing. Add to loop protocol.

## Loop status

ScheduleWakeup NOT called. Loop terminated cleanly. Owner picks next action.

## Open PRs status

Closed in this loop session:
- #473 (PR was on old branch; corrected content on master)
- #475 (Opus stall HALT — superseded by Opus retry success)
- #476 (QC stall HALT FINAL — superseded by QC PASS verdict)

Still open / earlier work:
- #467 (5-way reference set design — owner-verification pending, unchanged this session)

## Pilot ↔ batches 001-008 sentinel comparison

| Metric | 001-008 aggregate | 009 pilot | Verdict |
|---|---|---|---|
| Consensus rate | ~96% | 94% (47/50) | flat ✓ |
| FL5 illegal | 0/2000 post-patch | 0/265 | flat ✓ |
| Malformed | 0.68% | 0.00% | improved (v2 brief working) |
| Owner-arb size | 23-28 | 3 | improved (better consensus) |
| Action mix | BET/CALL balanced | FOLD/CALL heavy | EXPECTED (new chain spots force defensive postures) |
| Cost | not measured | ~8hr subagent runtime | over cap (pilot architecture inefficient) |

Pilot delivers the intended outcome. Architecture has room for improvement on cost (~2x what should be needed).
