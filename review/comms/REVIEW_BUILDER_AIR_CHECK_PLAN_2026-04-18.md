---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Review of BUILDER_AIR_CHECK_PLAN_2026-04-18 — APPROVED with 3 adjustments
status: DIRECTIVE — proceed after incorporating adjustments
---

# Review — Air-CHECK Counter-Example Plan

## Verdict

**APPROVED** with three adjustments below. Predicate, yield
discipline, litmus seeding, reuse of batch6 idiom, and post-gen
checks are all correct. One scope drift from update-g flagged.

## Adjustments

### 1. Broaden `num_opponents` to {1, 2} — REQUIRED

Update-g specified `num_opponents >= 1`. Plan narrows to `= 2`
(3-way only). That leaves the HU (num_opponents=1) counter-example
class uncovered.

The model overgeneralizes "villain_checked_back=1 + high HRP →
BET" across opponent counts. If we only feed 3-way CHECK
counter-examples, the HU case stays broken — model will still
BET A4d on Qs5s7s in a HU checked-through spot.

**Do:** target split ~50/50 HU vs 3-way. Both playtest litmuses
(A4d/Qs5s7s, T5h/JJ2) stay 3-way per update-g framing. Add a
parallel HU spread on the same boards + archetypes.

Adjusted yield target:
- HU: 15–20 BP
- 3-way: 15–20 BP
- Combined: 30–40 BP (unchanged)

### 2. Litmus seed strictness — FAIL HARD

If A4d/Qs5s7s or T5h/JJ2 fail predicate or validator, the
generator has a bug. These are the exact playtest spots we're
trying to fix — if we can't produce them in the training set,
the fix won't land.

Flag-and-continue hides generator drift. Hard fail surfaces it
immediately. Change plan step to: litmus miss → raise, not warn.

### 3. Monotone coverage — EXPAND

Current pool: `DRY_BOARDS` + `TWO_TONE_BOARDS` + one seeded
monotone (Qs5s7s). That's one monotone out of ~30+ boards. The
A4d class is specifically about air on monotone/hostile-suit
boards — needs more than one example.

**Do:** add a `MONOTONE_BOARDS` constant (3–4 boards) and include
in the pool. Examples to consider:
- Qs5s7s (already seeded)
- Jh8h3h
- Kd9d4d
- Ac6c2c

Spread across flop and turn runouts. The goal is that the model
sees air on multiple monotone textures → CHECK, not one-off.

## Open questions — answered

| # | Question | Answer |
|---|---|---|
| 1 | File naming `v23_air_check.jsonl` | Approved — matches convention |
| 2 | Litmus seed strictness | **Fail hard** (see adjustment 2) |
| 3 | Monotone coverage | **Expand** (see adjustment 3) |

## Proceed checklist

1. Update plan doc with the 3 adjustments (or note them in the
   generator header)
2. Build `review/generate_air_check_v231.py`
3. 10-spec yield test first (per CLAUDE.md §2)
4. Full run; report HU count, 3-way count, predicate conformance,
   litmus pass/fail, schema preflight errors
5. Commit with message referencing update-g Layer 2 + this review
6. Push and report back — I'll review yield stats before labelling
   dispatch

## What remains unchanged from your plan

- Predicate conditions (6-feature gate) ✓
- Generator location (`review/generate_air_check_v231.py`) ✓
- Batch6 reuse pattern ✓
- No river hands ✓
- No label generation in this step (separate labelling pass) ✓
- No static overrides ✓
- Preflight schema gate (ANOMALY-A guard) ✓

Go.
