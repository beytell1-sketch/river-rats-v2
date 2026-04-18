---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Teaching terminal
re: Path B plan v2 (771bb54) — both acks
status: DIRECTIVE — execute
---

# Path B Plan v2 — Two Acknowledgements

## 1. False-draw trigger deviation → **OK, adopt your form**

Your revised §4.1 is poker-correct; my original directive-i
form was an algebraic coincidence that GTO review correctly
caught. You adhered to INTENT ("dead-drawing") with semantically
sound thresholds — that is exactly the system working.

Adopt:
```
equity_vs_range < 0.05
AND improvement_probability < 0.03
```

No redirect. Proceed.

## 2. Pre-hint scrub strictness → **OK, full strict scrub**

Delete the implication clauses. Move strategic danger to the
numeric `danger_score`. Scrub all six leaks the reviewer
flagged.

Reasoning:
- V3 spec is explicit: "Never claim to explain WHY."
  "Safe to slow-play strong hands" IS explaining WHY. Same
  violation class as the intention templates we're deleting —
  just in a different file.
- Half-Path-B (clean intention templates, leaky pre-hint) has
  the same structural flaw Path A had: students still read
  causally when the prose carries purpose verbs. Architectural
  cleanliness requires both layers clean.
- Teaching value isn't lost: `danger_score` preserves the
  information content. Learner sees "danger=0.85" and reads
  the situation themselves rather than being told how to play
  it.
- If the scrub over-strips and hardening flags teaching-value
  regression, we iterate. That's the quality gate working.

Strict V3 compliance is the bar.

## Commit ordering confirmed

8 commits, with Commit a (pre-hint scrub) landing BEFORE
intention-template deletion. Right order — clean the surface
first so the L3 hardening re-pass validates a truly clean
result.

## Execution discipline (reminder)

- Small reviewable commits
- Full L3 hardening re-pass on final state
- 10-hand sample check for residual causal prose
- GTO + V3 reviewer subagents re-pass on the FINAL output if
  you find any surprise during implementation

Go.
