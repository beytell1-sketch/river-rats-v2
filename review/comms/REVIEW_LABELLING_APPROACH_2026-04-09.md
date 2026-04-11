# Review: Labelling Approach Decision

**Reviewer:** Process reviewer
**Date:** 9 April 2026
**File reviewed:** review/comms/LABELLING_APPROACH_DECISION_2026-04-09.md

**VERDICT: PASS — with one important caveat**

---

## Assessment

The builder is right. The v2 decision tree IS a deterministic
flowchart. Every branch is a feature name, a comparison operator,
and a threshold. There are no judgment calls. Feeding this to 57
LLM agents introduces noise that the tree was specifically designed
to eliminate.

The reasoning about §1.1 is sound: the rule exists to prevent
context overload degrading expert judgment. A script has no context
and no judgment — the rule's purpose doesn't apply.

## The caveat

**The decision tree only covers RAISE vs CALL (when facing a bet).**

The tree's default is "No step returned RAISE → CALL (or BET/CHECK
if not facing bet)." The tree does NOT mechanically distinguish:
- BET vs CHECK (when not facing a bet)
- CALL vs FOLD (when facing a bet and no RAISE step fires)

Steps 1-6 determine whether a hand RAISEs. The remaining 90% of
decisions — the full BET/CHECK/CALL/FOLD spectrum — still require
the 5-factor framework and equity-vs-pot-odds reasoning from the
labelling prompt.

**The builder needs to clarify:** Does the deterministic script
handle ALL 5 labels, or only the RAISE/not-RAISE decision? If it
handles all 5, the script needs logic for BET vs CHECK and CALL vs
FOLD that goes beyond the decision tree. If it only handles RAISE,
the remaining labels still need LLM agents.

Check the plan (PLAN_V3_COMPLETE.md Phase 5 labelling rules):
- RAISE: is_monster only (now replaced by v2 tree — scriptable)
- BET/CHECK: 5-factor framework (feature-visible reasoning)
- CALL/FOLD: equity vs pot odds + action history + position

BET/CHECK and CALL/FOLD have thresholds too (equity vs pot odds is
a comparison), but the 5-factor framework for BET/CHECK involves
weighting multiple factors — that may or may not be scriptable.

## Recommendation

Ask the builder: is the FULL labelling pipeline scriptable, or just
the RAISE decision? If the BET/CHECK and CALL/FOLD rules are also
deterministic thresholds, script everything. If they involve judgment,
the hybrid approach is: script the RAISE decisions deterministically,
use LLM agents for BET/CHECK/CALL/FOLD on the non-RAISE situations.
