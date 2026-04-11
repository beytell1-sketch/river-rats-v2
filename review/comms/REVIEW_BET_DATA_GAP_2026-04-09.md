# Review: BET Tree Data Gap

**Reviewer:** Process reviewer
**Date:** 9 April 2026
**File reviewed:** review/comms/BET_DATA_GAP_2026-04-09.md

**VERDICT: ISSUES FOUND — builder's recommendation is sound**

---

## Assessment

The builder correctly identified that the factory was designed
entirely for RAISE contexts (facing a bet). The BET tree has no
matching data. 95% of not-facing-bet situations are OOP defenders,
and zero are IP PFA — which is the core c-bet scenario the entire
research round was built around.

This is a gap in the original PLAN_V3_COMPLETE.md — it planned
factory batches for RAISE but never planned BET-context situations.
The c-bet research and BET tree came later (owner-initiated), so
the factory design predates the BET tree. Nobody failed to follow
process — the scope expanded after the factory was designed.

## On the three options

**Option A (new factory batch):** The builder is right that this
completes the investment. You funded 5 research agents, 3 reviewers,
feature 53, and a full BET decision tree. Training without BET
coverage wastes all of that work. Option A is the no-deadlines,
do-it-right approach.

**Option B (defer to v3.2):** This is the "ship now, fix later"
framing you've explicitly rejected. The no-deadlines memory applies.

**Option C (LLM agents for BET only):** Hybrid. Avoids the factory
work but reintroduces LLM bias for the hardest decisions (c-bet
bluffing). The whole point of the deterministic approach was to
avoid LLM bias on threshold decisions.

## Process note

**[SHOULD_FIX] The builder presented three options.** Option A has
a clear expert recommendation with reasoning. Options B and C are
included for completeness but Option B contradicts the no-deadlines
principle. The builder should have recommended A outright and noted
B and C only as rejected alternatives with reasons.

This is the options-menu pattern from §1.4 appearing again — though
milder than earlier instances, since the builder did mark Option A
as recommended.

## Recommendation

Option A. Design ~80-100 BET-context factory situations. The
infrastructure exists (board allocation process, diversity
requirements, hero hand design pipeline). The BET tree is ready.
This is factory design work, not research — it should be faster
than the RAISE batch.

The builder should present the BET factory brief (similar to
FACTORY_DESIGN_RAISE_CONTEXTS_V2.md) with sub-patterns matching
each BET tree step, diversity requirements, and a reviewer
checklist. Same process as the RAISE batch.
