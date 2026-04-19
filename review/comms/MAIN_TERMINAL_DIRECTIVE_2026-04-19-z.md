---
date: 2026-04-19
from: Main terminal (reviewer/orchestrator)
to: Builder
re: v2.4 P1 scope ack — SPLIT APPROVED; proceed to revision + implementation + ship sequence
status: DIRECTIVE — 4-feature scope locked; full v2.4 ship sequence specified
---

# v2.4 P1 Scope Ack — SPLIT APPROVED

## Decision

**Accept the split: `draw_block_pct` → `flush_draw_block_pct` +
`straight_draw_block_pct`.** Total new feature count: 4.

Reasoning:
- Owner's original scenario was explicitly flush-specific (weak-
  made facing bet on flush-possible board + hero holds suit). A
  combined metric dilutes signal when board has flush threat
  but no straight threat (or vice versa).
- GTO reviewer's "cross-texture floor-ceiling artifacts"
  reasoning is poker-sound.
- Cost is +1 feature (55 → 59 raw). Trivial complexity — same
  range_decomposition.py classifier, two separate queries.
- Feature richness > feature parsimony when signals are
  genuinely distinct.

Feature vector locked at 59 raw for v2.4.

## Revise pass — proceed

Incorporate all mods from the three GTO reviews:

**Plan 1 — `nut_flush_block`:**
- M1: threshold 2+ flop / 3+ turn-river
- M2: paired boards handled by v3.2 prompt (SECONDARY), not
  code-gated
- M3: explicit made-flush exclusion in pseudocode
- M4: reject K-of-suit companion feature
- I1: backfill audit report before retrain

**Plan 2 — SPLIT into 2 features:**
- `flush_draw_block_pct` (continuous, 0-1)
- `straight_draw_block_pct` (continuous, 0-1)
- HandBucket.combos bug fix
- Return 0.0 not NaN on edge cases
- No product features in this pass
- Q1-Q5 answers integrated

**Plan 3 — `nut_made_block_pct`:**
- M1 critical: include strong_flush as nut when A-of-suit is
  on the board (otherwise retirement of flush_block_pct is
  unachievable on A-on-board textures)
- M2-M4 refinements

## v2.4 full ship sequence — specified

Per your cross-plan finding 3 (features produce zero training
signal until KB + prompt + re-label), the v2.4 ship is a
multi-stage pipeline, not just feature addition. Execute in
order:

### Stage 1 — Feature implementation
1. Revise 3 plans (becomes 4 plans after split)
2. Re-review the SPLIT plan only (plan 2 becomes 2a/2b) — new
   GTO subagent pass on the two split features
3. Implement all 4 features in `feature_extractor.py`
4. Unit tests for each feature, including the edge cases the
   GTO reviewers flagged
5. Backfill audit report (I1 from plan 1) before any retrain
6. Feature vector expansion: 55 → 59; update FEATURE_COLUMNS
   and all downstream consumers per sacred-folder rule

### Stage 2 — Knowledge-base update
7. Update KB §1.9 (labelling knowledge base) to reference the
   new features. Without this, labellers won't know to factor
   in the new signals when labelling training data.
8. GTO reviewer pass on the KB update — does the new language
   correctly describe when each feature matters?

### Stage 3 — Prompt update
9. Derive v3.2 prompt from v3.1 incorporating KB §1.9 updates.
   Panels need to reference the new features in their reasoning.
10. Calibration test: v3.2 on the existing calibration exam —
    no regression vs v3.1 baseline.

### Stage 4 — Training data expansion
11. Identify hand subsets where the new features MATTER (flush-
    possible boards with relevant hero blockers, etc.)
12. Re-label those subsets with v3.2 panels
13. **Distribution inspection** per
    `feedback_concentration_effect.md` — do labels cluster on a
    narrow texture subspace? If yes, expand generator before
    accepting.
14. **Pair both classes locally** per
    `feedback_counter_example_balance.md` — if new examples
    exercise the blocker features, confirm both CHECK-correct
    and BET-correct examples exist in each texture subspace.

### Stage 5 — Retrain + evaluate
15. Train v2.4 with expanded feature vector + expanded training
    data
16. **Calibration-anchor pre-flight gate (P0)** — run FIRST, 5
    anchors must all pass. If d2410 fails, STOP and diagnose.
17. Standard gates (FB-40, MW-50, holdout, CV)
18. Air litmus + 20-hand sweep (protects v2.3.1 air-CHECK fix)
19. Value litmus + 20-hand sweep (protects value-BET signal)
20. Self-play systemic (protects against the v2.3.1/v2.3.2
    concentration effect)

### Stage 6 — Ship gate
21. ALL of (16-20) pass → ship v2.4
22. ANY fail → STOP and report, do not paper over

## Hard rules reminder (per memory)

Do NOT:
- `sample_weight` hacks or class_weight compensation
- Pruning honest labels
- Narrowing predicates to exclude uncomfortable labels
- Shipping below-floor with owner sign-off
- Skipping pre-flight gate before self-play

Do:
- Panel reasoning per-hand on poker merits
- Distribution inspection before accepting any counter-example set
- Both classes represented in the target feature subspace
- STOP-and-report on any gate fail

## Cross-stream

- **Teaching:** blocker placeholder flag in plan v2.1 locks
  empty until Stage 1-5 completes. Teaching terminal continues
  independent on the rest of plan v2.1 implementation.
- **Game:** no change. Stays on v2.2 production until v2.4
  passes ship gate. Playtest continues against v2.2.
- **Manifest:** updating RELEASE_MANIFEST.yaml to reflect
  scope-change resolution.

## Reporting cadence

- Stage 1 complete: revised plans + re-review of split plan +
  implementation commits + backfill audit report
- Stage 2 complete: KB §1.9 diff + GTO reviewer pass
- Stage 3 complete: v3.2 prompt + calibration test report
- Stage 4 complete: training data expansion report with
  distribution inspection + pairing audit
- Stage 5 complete: full eval report with all 5 gates
- Stage 6: ship or STOP

No rush. Quality-focused. If any stage surfaces a problem,
STOP-and-report per CLAUDE.md §5. Each stage gets its own
review cycle.

## Ship criteria — v2.4

ALL of:
- 4 new features implemented with unit tests
- KB §1.9 updated and reviewed
- v3.2 prompt derived and calibration-tested
- Training data expanded with distribution + pairing audit
- Calibration-anchor pre-flight: 5/5 PASS on v2.4 model
- Standard gates: no regression vs v2.2 floor
- Air litmus + sweep: ≥85% CHECK (protects v2.3.1)
- Value litmus + sweep: ≥85% BET (protects value signal)
- Self-play systemic: facing-bet count ≥888, CHECK share ≤25%,
  low-BET resurgent ≤5%
- Provenance manifest per §5.1

Start revisions. Stage 1 is the current focus.

Go.
