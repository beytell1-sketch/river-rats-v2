# Review: Feature 53 + C-bet Research Plan

**Reviewer:** Process reviewer
**Date:** 9 April 2026
**Files reviewed:**
- review/comms/FEATURE53_COMPLETE_2026-04-09.md
- review/comms/CBET_RESEARCH_AND_FEATURE53_PLAN_2026-04-09.md
- review/HANDOFF_V3_1_STATE.md (updated)

**VERDICT: PASS**

---

## Feature 53

Feature added, all 3 batches regenerated, no existing features
changed. Clean implementation.

**[NOTE] Batch 1 has zero PFA=1 situations.** All Batch 1 boards
use BB/SB as hero (defenders). This is a known OOP bias from the
original factory design. The model will learn PFA=1 patterns only
from Batch 2 (60 PFA situations) and Batch 3 (58 PFA situations).
Combined: 118 PFA=1 out of 563 total (21%). This is adequate for
a binary feature but worth monitoring — if the BET tree has a PFA
branch, enough PFA situations must exist in the training data to
learn it.

**[NOTE] SP8_06 SUSPICIOUS resolved by regeneration.** Good — one
fewer edge case to track.

## C-bet Research Plan (Phases B-D)

The plan correctly identifies that BET labels need the same rigour
as RAISE labels. The Phase B-C-D sequence follows Process Guide:
- §3.1: research before design (Phase B)
- §3.2: minimum 8 sources (specified)
- §2.5: independent review before building (Phase C)
- §2.1: calibration before labelling (Phase D)

**[NOTE] The deterministic labelling approach (Phase E) now covers
both trees.** RAISE tree for facing-bet, BET tree for not-facing-bet.
CALL/FOLD when facing bet and no RAISE fires still needs a rule —
the builder should confirm whether this is also scriptable or needs
LLM judgment. (Same caveat I raised earlier.)

## Handoff

The handoff captures the full state including the PFA feature,
c-bet research plan, and updated pipeline. A new session can pick
this up cleanly.

## Recommendation

Proceed with Phase B (c-bet research) in the next session. The
builder has the right plan and the right sequence. I'll review the
research deliverables when they arrive in comms.
