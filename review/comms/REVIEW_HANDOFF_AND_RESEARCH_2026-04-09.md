# Review: Handoff + Research Deliverables

**Reviewer:** Independent process reviewer
**Date:** 9 April 2026
**Files reviewed:**
- review/HANDOFF_V3_1_STATE.md
- review/RAISE_DECISION_TREE_V1.md
- review/REVIEW_RAISE_DECISION_TREE_V1.md
- review/FACTORY_DESIGN_RAISE_CONTEXTS.md

**VERDICT: ISSUES FOUND**

---

## Handoff Document

Well structured. A new terminal could pick this up. No issues.

---

## Decision Tree v1

**[SHOULD_FIX] Step 5 semi-bluff has no nut-draw quality gate.**
The independent reviewer already caught this. A non-nut flush draw
with 9 outs qualifies for RAISE, contradicting KB Section 1.7 and
the MW-20 finding. Add `flush_draw_rank >= 12` or `flush_block_pct > 0`.

**[SHOULD_FIX] S1 references "two-pair+" which isn't a feature.**
Needs mapping to `hand_category` threshold. The tree claims to use
only the 52-feature vector but this branch can't be evaluated from
features as written. Violates the preamble's own constraint.

**[SHOULD_FIX] Step 1D "sandwich position" has no feature mapping.**
"Player behind hasn't acted" — which feature captures this? If none,
this step is feature-invisible logic and can't be in the labelling
rule.

**[NOTE] The 12 independent review findings are reasonable and
should all be addressed.**

**[NOTE] Tree structure is sound — sequencing makes poker sense.**

---

## Factory Design Brief

**[SHOULD_FIX] SP5 must match the fixed tree.** After adding the
nut-draw gate to Step 5, SP5 factory situations need the same gate.
Don't design situations for a rule that's about to change.

**[SHOULD_FIX] Verify self-play RAISE yield.** The 200 self-play
rows — how many are RAISE? If <10, factory needs more than 115
situations to hit the 150 target.

**[NOTE] 115 situations is reasonable volume. CALL counterexample
count (32) adds up correctly from sub-patterns.**

---

## Process Compliance

| Rule | Followed? | Evidence |
|------|-----------|----------|
| §3.1 Research before design | Yes | 28 sources |
| §3.2 Min 8 sources | Yes | 28 sources cited |
| §3.3 Research reviewed | Yes | 12-item independent review |
| §1.1 One topic per agent | Yes | A = strategy, B = features |
| §1.4 Expert recommends | Yes | Concrete tree, not options |
| §4.1 Present for review | Yes | All docs in review/ |

---

## Recommendations (for builder)

1. Fix the decision tree — address all 12 review findings,
   especially Step 5 nut-draw gate, S1 feature mapping, Step 1D
   sandwich feature, Step 6 street gate. Present as v2.
2. Update factory brief to match the fixed tree.
3. Verify self-play RAISE yield before finalizing situation count.
4. Get owner approval on fixed tree + updated brief before building.

Research was done properly. Tree needs fixes the reviewer already
identified. This is the process working as intended.
