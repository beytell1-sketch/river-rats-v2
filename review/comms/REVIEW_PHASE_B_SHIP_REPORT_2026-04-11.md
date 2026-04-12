---
date: 2026-04-11
from: Reviewer terminal
to: Main terminal (orchestrator) / Owner (Rupert)
re: Review of PHASE_B_SHIP_REPORT_2026-04-11.md — direction on Q1-Q4
verdict: SHIP APPROVED, 2 PRE-STEPS REQUIRED BEFORE TASK #4/#6
---

## Scope

Reviewed `review/comms/PHASE_B_SHIP_REPORT_2026-04-11.md` (404 lines)
covering Phase B Preflop Range Fix ship state, yield diagnostic, and
4 open questions for direction. Reviewed against:

- `feedback_solver_findings.md` (residual failure patterns)
- `project_river_rats_v2.md` (ceiling-iterate-first directive)
- `feedback_no_deadlines.md` (quality over momentum)
- `feedback_verify_source_not_plan.md` (verify diagnostic from source)
- Process Guide Section 1.1 (agent allocation, ≤10 hands per GTO agent)

## Verdict on the ship itself

**APPROVED.** Phase B is a cleaner win than projected:

- 960 pass / 0 fail, 62 tests flipped green
- 6.95% yield vs 3-5% target (with seed caveat, see below)
- Latent `get_3bet_range()` duplicate-method bug was a genuinely
  dangerous silent failure — that catch alone justifies the cycle
- 3 clean atomic commits, proper task decomposition (7 specialist
  agents across 3 rounds), full paperwork trail

The ship itself does not require rework. The concerns below are
about **what comes next**, not about what landed.

## Observations before Q1-Q4

### O1 — Seed variance is real and must be acknowledged

seed=42 gave 3.20%, seed=77 gave 6.95%. Both clear the 3-5% target,
but that is a 2x swing from seed choice alone. The honest number is
"3-7%, seed-dependent," not "6.95%."

**Required before task #6:** run 3-5 additional seeds to establish
the yield band. If the lower bound holds above 3%, no further
action. If any seed falls below 2%, we have a reproducibility
concern that needs investigation before declaring Phase B a
stable win.

### O2 — ml-architect static projection was wrong by 7x

Not a criticism of the agent — but the static projection missed the
all-seats-logging multiplier that is documented in
`generate_3way_situations.py`'s own docstring. Lesson: when
projecting pipeline metrics, read the runner code, don't just model
the probability tree.

**Recommended:** save a brief feedback memo
(`feedback_pipeline_projections.md`) encoding "static yield math
must read the runner, not just the probability tree." This is a
durable anti-pattern worth capturing.

### O3 — The "9 FOLD with 0 facing_bet" line is a diagnostic bug

The ship report flags this as a "definitional quirk" but it is not
— you cannot fold when no bet is live. Either the classifier is
miscategorizing actions, or the logger is conflating
hero-perspective with other-seat perspective (one of the
all-seats-logging side effects).

**This matters because it means we do not actually know what the
139 situations are.** Q2's "investigate the passive oracle" cannot
run cleanly until the diagnostic itself is trusted. Any
investigation into the "0 BETs in 139 decisions" finding is
unreliable until the classifier is fixed.

**Required before Q2:** 15-minute read of `generate_3way_situations.py`
logging code to resolve the FOLD-without-facing-bet contradiction,
then re-run the diagnostic.

## Direction on Q1-Q4

### Q1 — Task #4 first (facing-bet test set). Strongly.

Option A. The yield diagnostic produced empirical evidence that the
existing pipeline generates zero facing-bet multiway situations,
which means every reference-set evaluation to date has been blind
on the facing-bet half of the decision space. Retraining v2.2 now
would produce a model whose facing-bet behavior is literally
uninterpretable — we would have no test set to measure it against.

The v2.1 residual failures (MW-17 under-calling, MW-25/40 passive,
MW-45 under-raising, MW-47 shared blind spot) are not going
anywhere; they will still be failing next week. The facing-bet gap
compounds with every training cycle run without it. Do task #4
first.

This is also consistent with the owner's earlier stated preference
(Q1 in `AUDIT_PROJECT_STATE_2026-04-11.md`): "retraining blind on a
single 40-hand reference axis has bitten us before. A second axis
de-risks v2.2 evaluation and is cheap relative to a retrain cycle."

**Decision: option A (task #4 first).**

### Q2 — Investigate, but fix the diagnostic FIRST

Before running the option (b) targeted oracle probe, resolve the
diagnostic classifier bug from O3 above. Until the FOLD/facing_bet
contradiction is explained, we do not know whether "0 BETs in 139
decisions" is:

- a real oracle passive bias (which would be alarming and require
  multiway_adjuster review)
- a classifier miscategorization (which would mean the oracle is
  actually betting and we cannot see it)
- a legitimate consequence of the 139 situations being a skewed
  slice (e.g., all flop-OOP-first-to-act, where check IS correct)

**Do NOT run option (c) widening the multiway_adjuster thresholds.**
Adjusting thresholds to fix a diagnostic bug would bake in a
phantom correction that corrupts v2.2 and every downstream model.
This would be a classic "patch symptom, not root cause" anti-pattern
per CLAUDE.md anti-patterns list.

**Decision: fix diagnostic, re-run, then option (b) if 0-BET finding
survives.**

### Q3 — (a) + (b) combined, with decomposition constraint

Agree with the ship report's recommendation: SituationFactory for
board candidates + GTO Expert agents for per-hand hero/action
design. This matches the batch 2-4 pattern.

**Process Guide constraint:** ≤10 hands per GTO Expert agent. For
30-50 situations that is 3-5 GTO Expert agents in parallel, plus
an independent reviewer agent as the quality gate. **Not one
agent designing all 50** — that is the "stingy agent allocation"
anti-pattern from `process_guide_pointer.md`.

Sequencing:
1. ml-architect agent designs the facing-bet axis specs (what board
   textures × hero positions × facing-bet sizings to cover)
2. SituationFactory generates board candidates against those specs
3. 3-5 GTO Expert agents (parallel) design hero hands and label
   actions, ≤10 hands each
4. Independent reviewer agent audits the full 30-50 before
   they become the test set
5. Solver verification on any RAISE/CALL or high-equity FOLD
   (mandatory per memory)

**Decision: (a) + (b) combined, 3-5 GTO Expert agents, reviewer
gate mandatory.**

### Q4 — Yes, add the paranoia test

One-line introspection assertion on `RangeManager.__dict__` verifying
no method name is bound twice. Trivial scope, prevents a class of
silent bugs that just cost us real range data correctness.

**Bundle with task #4's first commit** so it lands as part of the
next test-set infrastructure work. Do not make it its own commit —
too small to justify commit overhead.

**Decision: yes, bundled with task #4.**

## Proposed sequence

| # | Step | Owner | Estimate |
|---|------|-------|----------|
| 1 | Fix diagnostic classifier (O3) — resolve FOLD/facing_bet contradiction | 1 programmer agent | 15 min |
| 2 | Multi-seed yield verification (O1) — 3-5 seeds, confirm 3-7% band | 1 programmer agent | 10 min |
| 3 | If O3 fix shows 0-BET persists: targeted oracle probe (Q2 option b) | 1 programmer agent | 15 min |
| 4 | Save `feedback_pipeline_projections.md` (O2) | main terminal | 5 min |
| 5 | Task #4 decomposition: ml-architect brief for facing-bet axis | architecture-expert | ~30 min |
| 6 | Task #4 execution: SituationFactory + 3-5 GTO Expert agents + reviewer | team | multiple hours |
| 7 | Task #6 retrain decomposition | gated on task #4 completion | — |

Steps 1-4 are prep and can run in parallel. Steps 5-6 are the
actual task #4 work. Step 7 gates on step 6.

**Task #4 does not start until steps 1-4 are complete.** Otherwise
we risk designing the facing-bet test set on top of an unverified
diagnostic, which would be a second-order version of the same
Phase B projection error.

## What I did NOT review

- The actual Phase B code commits (1f9f739, aed81a6, c4f2f39) — the
  ship report's test delta (960 pass / 0 fail) and architect +
  programmer + lead-programmer chain provide sufficient evidence
  that the code itself is sound. A line-by-line audit of
  `range_manager.py` +734/-803 is out of scope for a direction
  review.
- The ml-architect design doc and architect blueprint — these were
  consumed during execution and are paperwork, not open work.
- The B-2 task file — downgraded to future iteration, not reviewed.

## Open questions for owner

**OQ1 — Accept the 4-step prep sequence (steps 1-4 above) before
task #4 starts, or compress into task #4's prep phase?**

My recommendation: run them as explicit steps, not folded into
task #4 prep. They are shared-infrastructure concerns that the
facing-bet test set should not carry on its back. Explicit
sequencing also makes the "we fixed the diagnostic before building
on it" decision auditable.

**OQ2 — Multi-seed yield verification (step 2): what is the
go/no-go threshold?**

Proposed: if all 5 seeds clear 2.5% yield, task #4 proceeds. If any
seed falls below 2%, pause task #4 and investigate seed sensitivity
before building test infrastructure on an unstable yield foundation.

**OQ3 — Should `feedback_pipeline_projections.md` be written now
or after task #4 ships?**

My recommendation: now. The lesson is fresh, and task #4 will
involve more pipeline projections — better to have the feedback
memo in place before that work starts so it guides the new design.

---

**End of review. Awaiting owner direction on Q1-Q4 positions above
and OQ1-OQ3.**
