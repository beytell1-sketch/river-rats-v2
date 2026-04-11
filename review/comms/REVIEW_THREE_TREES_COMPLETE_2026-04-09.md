# Review: Three Trees Complete — Full Decision Flow

**Reviewer:** Process reviewer
**Date:** 9 April 2026
**Files reviewed:**
- review/comms/THREE_TREES_COMPLETE_2026-04-09.md
- review/comms/FOLD_DECISION_TREE_V1_DELIVERY_2026-04-09.md
- review/comms/REVIEW_FOLD_DECISION_TREE_V1.md
- review/BET_DECISION_TREE_V1.md (reviewed earlier)

**VERDICT: PASS — all three trees ready for deterministic labelling**

---

## Decision Flow Verification

The routing is clean and gap-free:

```
to_call == 0? → BET tree → BET or CHECK
to_call > 0?  → RAISE tree → RAISE?
                  YES → RAISE
                  NO  → FOLD tree → FOLD or CALL
```

All 5 actions covered. No ambiguous handoffs between trees. The
independent reviewer verified this explicitly (checklist item 8).

## FOLD Tree Assessment

**[NOTE] MW-30 and MW-50 correctly handled.** MW-50 (4pp surplus,
multi-street aggression) correctly folds via Step 3. MW-30 (22pp
surplus) correctly passes through to CALL (equity_margin 0.22 >
0.10 threshold in Step 4). This was the hardest boundary to get
right and the tree handles it cleanly.

**[NOTE] Monster pre-check is belt-and-suspenders.** Pre-check C
exits for monsters, AND every step requires is_monster == 0. Good
defensive design.

**[NOTE] Default is CALL.** Correct — when in doubt, call. The
conservative default prevents over-folding, which was the
documented labelling agent bias.

**[NOTE] The GTO Expert raised 4 open questions honestly.** 
equity_margin encoding (confirmed by reviewer), Step 5 confidence
(MEDIUM, appropriately cautious), positional differentiation (known
limitation), villain_aggression_count gate logic. All flagged, none
blocking. Good transparency.

## Process Compliance (Full Session)

| Rule | Followed? | Evidence |
|------|-----------|----------|
| §3.1 Research before design | Yes | 5 research agents for BET tree |
| §3.2 Min 8 sources | Yes | 28+ sources |
| §1.1 One topic per agent | Yes | 5 agents, 5 topics |
| §1.2 Independent reviewers | Yes | 3 reviewers for research, 1 for each tree |
| §1.4 Expert recommends | Yes | All 3 trees are concrete, no options menus |
| §2.5 Review before building | Yes | All trees reviewed before labelling |
| §0 Phase decomposition | Yes | Research → tree → review → approval sequence |

## Outstanding Items

1. **RAISE tree preamble: 52 → 53 features.** Noted in BET tree
   review. Should be fixed before the labelling script references it.

2. **Calibration re-run needed.** Feature 53 was added and factory
   batches regenerated. The earlier calibration (24/24) was on
   52-feature situations. Per §2.1, KB checksum change requires
   re-calibration. The BET and FOLD trees are new labelling rules.
   Calibration should verify the agent can apply all three trees.

   However — if labelling is now deterministic (script, not LLM
   agents), calibration of LLM agents is no longer the gate. The
   gate becomes: does the script correctly implement all three trees?
   That's verified by the LLM reviewer sample, not calibration.

   The builder should clarify: is calibration still needed given the
   deterministic approach?

## Recommendation

Approve both the BET tree and FOLD tree. The three trees together
form a complete, deterministic, feature-only labelling specification.
The builder can proceed with writing the labelling script.

Resolve the calibration question before labelling runs.
