# Review: BET Decision Tree v1

**Reviewer:** Process reviewer
**Date:** 9 April 2026
**Files reviewed:**
- review/BET_DECISION_TREE_V1.md
- review/comms/BET_TREE_FIXES_APPLIED_2026-04-09.md

**VERDICT: PASS — ready for owner approval**

---

## Structure Assessment

The tree is well-structured and mirrors the RAISE tree's conventions:
deterministic, feature-only, every branch references named features
with explicit thresholds. The frequency-to-threshold mapping table
(lines 449-465) is excellent — it traces every threshold back to a
specific research finding, which makes the tree auditable.

## Process Compliance

| Rule | Followed? | Evidence |
|------|-----------|----------|
| §3.1 Research before design | Yes | 5 research agents, 3 reviewers |
| §3.2 Min 8 sources | Yes | 28+ sources across 5 agents |
| §1.4 Expert recommends | Yes | GTO Expert produced tree, not options |
| §4.1 Present for review | Yes | In review/ folder + comms |
| Preamble constraint | Yes | All conditions reference 53-feature vector |

## Findings

**[NOTE] Output is BET or CHECK, never a frequency.** This directly
addresses the concern about frequency research. The tree correctly
converts frequencies into deterministic thresholds. Good.

**[NOTE] Feature 53 (is_preflop_aggressor) is load-bearing.** Steps
3, 4 gate on it. Step 5 gates on its absence. The PFA feature
enables the core c-bet logic — without it, Steps 3-4 couldn't
distinguish PFA from defender. This validates the decision to add
it before labelling.

**[NOTE] The 4-tier texture classification in Step 3A is concrete
and testable.** Tier determination uses feature thresholds
(high_card_rank, flush_danger, connectivity_score) evaluated in
order. Two agents applying this should produce the same tier.

**[NOTE] 6 known gaps documented honestly.** Backdoor draws,
made-hand blockers, 3-bet pots, OOP texture frequencies, MDF
framing, middle-connected disagreement. All flagged as "accept
limitation, don't hack around it." This is the right approach.

**[NOTE] Step 2 monster protection fires before the dry-board trap.**
This means monsters on dynamic boards BET, monsters on dry boards
CHECK (trap). The trap rule is implicit (default CHECK when Step 2
doesn't fire). The logic is correct and well-explained.

**[SHOULD_FIX] RAISE tree preamble still says 52 features.** The
builder noted this (item 5 in fixes doc) but didn't change it. This
should be updated to 53 in the next pass — not a blocker for the
BET tree, but the RAISE tree should be consistent.

**[NOTE] S2 override list now includes Steps 2, 3B, and 6.** Fix #2
from the review is correct — Step 3B is an OOP exception that must
bypass the OOP suppressor.

## The CALL/FOLD question (my earlier caveat)

This tree handles BET vs CHECK. The RAISE tree handles RAISE vs
CALL (when facing a bet). What's still missing: **CALL vs FOLD when
facing a bet and no RAISE step fires.** The deterministic labelling
script needs logic for this. The builder should confirm:

- Is CALL/FOLD also a deterministic threshold (equity vs pot_odds)?
- Or does it need LLM judgment?

If it's just `raw_equity >= pot_odds → CALL, else FOLD`, that's
trivially scriptable. But action history, position, and range
narrowing may matter (the MW-50 thin-margin case). This is the
last piece of the labelling puzzle.

## Recommendation

BET tree v1 is ready for your approval. The RAISE tree preamble
should be updated to 53 features. The builder needs to define the
CALL/FOLD rule to complete the deterministic labelling script.
