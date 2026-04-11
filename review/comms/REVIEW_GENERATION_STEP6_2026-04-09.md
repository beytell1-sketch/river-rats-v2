# Review: Step 6 — Factory Batch 3 Generation

**Reviewer:** Process reviewer
**Date:** 9 April 2026
**Files reviewed:**
- review/comms/SESSION_2_GENERATION_COMPLETE_2026-04-09.md
- training-data/factory_batch3_situations.jsonl (verified)

**VERDICT: PASS**

---

## Verification

- Row count: 151 (confirmed)
- Sub-pattern counts: all 10 match design targets exactly
- SP8_06 SUSPICIOUS warning: noted, not a blocker

## Process Compliance

Builder correctly identifies Step 7 as a phase transition requiring:
- §2.1 calibration before labelling
- §1.1 agent allocation (≤10 per GTO agent)
- §1.2 reviewer count (≥ labeller count ÷ 2)
- §0 team decomposition

## Note for next session

The 557-situation relabelling (Step 7) is the largest labelling round
in the project so far. At ≤10 per agent, that's ≥56 labelling agents
plus ≥28 reviewers. The builder should plan for this scale in the
team decomposition.

The calibration exam answer key must be addressed before labelling —
the stale MW-30/MW-50 issue from the earlier review is still open.
The calibration agent needs to be tested against a corrected key.

## Recommendation

Proceed to Step 7 in a fresh session. Read the handoff first.
