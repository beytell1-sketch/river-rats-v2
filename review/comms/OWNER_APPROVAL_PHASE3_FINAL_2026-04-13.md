---
date: 2026-04-13
from: Owner (Rupert)
to: Builder team
re: Phase 3 Final Plan — APPROVED. Answers to your 5 questions. Start.
status: APPROVED — proceed immediately with Phase 3A
---

# Phase 3 Final Plan: APPROVED

The plan at PLAN_PHASE3_FINAL_2026-04-13.md is approved as
written, including the two builder additions (team
differentiation via random ordering, CONFIDENT_SPLIT flag).

## Answers to your 5 questions

**1. Is the pilot scope (20 hands, 3 approaches, 10 agents)
right?**

Yes. 20 hands is enough to compare the 3 feature attention
approaches. Pilot hands become production labels if protocol
holds. No changes.

**2. Is the production pace (10 hands/batch) acceptable given
the ~11-14 session timeline?**

Yes. Slow and careful is the directive. 10 hands per agent
is the right batch size. The 6-team parallel structure means
sessions are productive despite the smaller batches. Do not
rush.

**3. Should any difficulty-1 hands get reduced coverage (2
experts instead of 3)?**

No. All hands get 6 teams. Difficulty is classified
independently by each team — we don't know difficulty until
all 6 teams have labelled. The difficulty consensus across
6 teams IS the triage for Pass 2. Reducing first-pass
coverage defeats the purpose.

**4. Are the seed vocabularies correct starting points?**

Yes. The 6 intention seeds and 10 street plan seeds (5 action
+ 5 response) are the right starting point. Intentionally
small. Agents propose new tags when needed. One vocabulary
review after all labelling is complete. No mid-stream
vocabulary changes.

**5. Solver verification budget — ~30-50 hands through GTO
Wizard. Is this feasible?**

Yes. I have the time. If the actual count runs higher (up to
~80), I will triage by equity margin — marginal zone hands
(0.25-0.45 equity) first, clear cases last. If it exceeds 80,
we discuss before continuing.

## Execution order

1. **Phase 3A: Feature promotion + prompt update.** Start now.
2. **Gate 5: I review the updated prompt.** Nothing proceeds
   until I approve the prompt.
3. **Phase 3B: Calibration.** 20/24 + 3 reversals.
4. **Pilot: 20 hands × 3 approaches.**
5. **Pilot gate: I select the feature attention approach.**
6. **Pass 1: 6 teams × 385 hands.**
7. Continue per plan.

## One clarification

Feature 51 (`villain_fold_equity_estimate`): the plan flags
checking whether its formula is redundant (just `1 - tp_pct -
draw_pct`). If it IS redundant with existing features, drop it
and ship 53 features instead of 54. If it uses a nonlinear
formula (capped/product), keep it. Builder decides based on
the code — no need to come back for approval on this one.

---

**Start Phase 3A.**
