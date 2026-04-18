---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Decisions on HU labelling path + litmus/bridge semantics blocker
status: DIRECTIVE — both paths resolved; proceed
supersedes: REVIEW_BUILDER_AIR_CHECK_PLAN adjustment #1 (partial reversal)
---

# Decisions — Two Blockers Resolved

Both blockers surfaced pre-cycle-burn. Good STOP discipline.
Resolving both now.

## Blocker 1: HU labelling path → **Path B (with data prep)**

**Reverses my REVIEW adjustment #1 in part.** The calibration-
anchoring concern you raised changes the risk math. v3.1 was
calibrated against a 3-way exam; deriving v3.2 in ~30 min
without a parallel HU calibration pass produces unanchored
labels. That's label quality risk for a class of overgeneralization
we haven't observed in playtest.

Owner preference is quality over coverage. Applying it:

**Do this:**
- Generate BOTH HU and 3-way specs (data is cheap). Save to
  `training-data/v23_air_check_hu.jsonl` (unlabelled) and
  `training-data/v23_air_check_3way.jsonl` (for labelling).
- Label ONLY the 3-way set with v3.1 for v2.3.1.
- HU set sits ready for v2.4 when we do a proper v3.2
  derivation with HU calibration anchors.

**Why this works:**
- Playtest findings (A4d, T5) are both 3-way spots. We're
  fixing what we observed, not speculating about HU.
- HU data is preserved and ready — no rework when v2.4 picks
  up HU calibration.
- Labels come from an anchored prompt, not a rushed derivative.

**Yield target change:** 30–40 BP ALL 3-way for the labelled
set. HU set is opportunistic — whatever the generator produces
from the broader spec, fine. Don't force a target there.

## Blocker 2: Litmus vs bridge semantics → **Path B (turn-shift)**

Builder recommendation is correct. Accepting.

**Do this:**
- Shift both litmus seeds to turn decisions:
  - A4d on Qs5s7s + safe non-spade low turn (flop check-through)
  - T5h on JJ2 + safe low offsuit turn (flop check-through)
- Single consistent predicate (`villain_checked_back=1`) across
  all generated rows
- Hard-fail adjustment #2 remains intact

**Why Path B is right:**

The two layers divide labor cleanly:
- **Layer 1 (`board_adjusted_hrp`)** handles the flop playtest
  spots directly. A4d = 0.092 and T5h = 0.023 are both very
  low — the model should see these as weak via this signal.
- **Layer 2 (counter-examples)** teaches the broader
  `air + villain_checked_back=1 + checked-through → CHECK`
  pattern. This pattern manifests cleanly on turn+ because
  that's where vcb=1 can fire per bridge semantics.

Together they cover: (a) the flop spots via feature signal,
(b) the multi-street pattern via examples. Model generalizes
across `street` feature (that's literally what feature
decomposition in XGBoost does).

**Validation still tests flop spots.** The v2.3.1 litmus
criterion — "A4d/Qs5s7s and T5h/JJ2 must predict CHECK" —
is an **inference-time** test. The training set has turn
versions; inference tests the flop versions. If the retrained
model fails either litmus at inference, we know Layer 1 alone
wasn't enough and we revisit (likely adding flop memorization
spots per original Path A).

**Safe turn card guidance:**
- A4d on Qs5s7s: turn should be low non-spade (e.g., 2c, 3d,
  4h) — no flush draw, no board pair, no connection for hero
- T5h on JJ2: turn should be low offsuit that doesn't help T5h
  (e.g., 3c, 4d, 6c) — preserves "hero is air" state

Pick whatever the factory normalises cleanly. Flag if you hit
any weirdness.

## Updated proceed checklist

1. Update generator for:
   - Litmus seeds shifted to turn (Path B, Blocker 2)
   - Two output files: `v23_air_check_3way.jsonl` (labelled
     target) and `v23_air_check_hu.jsonl` (v2.4 prep)
2. 10-spec yield test on each stream
3. Full run; report:
   - 3-way yield (target 30–40 BP)
   - HU yield (opportunistic, report count)
   - Litmus pass/fail (hard-fail on 3-way litmus miss)
   - Predicate conformance, schema preflight errors
4. Commit both JSONLs + generator
5. Report yield stats; await labelling go-ahead for 3-way set only

## What stays unchanged

- Monotone board pool expansion (adjustment #3) ✓
- Hard-fail on litmus (adjustment #2, applies to 3-way set) ✓
- Batch6 reuse ✓
- No static overrides ✓
- Preflight schema gate ✓

## Scope summary

```
v2.3.1 ships with:
  Layer 1: board_adjusted_hrp (DONE, 80197cd)
  Layer 2: 3-way air-CHECK counter-examples (30-40 hands,
           labelled via v3.1)
  Layer 3: teaching value_extract air guard (teaching terminal)
  Validation: A4d/Qs5s7s AND T5h/JJ2 flop decisions must CHECK

v2.4 picks up:
  - HU counter-examples (data already generated)
  - v3.2 prompt with HU calibration anchors
  - Broader opponent-count coverage
```

Go.
