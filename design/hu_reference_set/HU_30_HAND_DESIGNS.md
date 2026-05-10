# HU Reference Set — 30 Hand Designs (Phase 1.5-D.1)

**Date:** 2026-05-10
**Status:** Complete — 30 hands across 6 axes (HU-1 through HU-6)
**Context:** Phase 1.5-D.1 HU reference set design per architect's
design memo §4.2 + dispatch
`MAIN_TERMINAL_PHASE15D1_HU_REFERENCE_SET_DESIGN_DISPATCH_2026-05-09.md`
**Close-hand-anchor:** `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json`
(α/β resolution = β per standing directive)

---

## Coverage

| Axis | Decision class | Hands | IDs |
|------|----------------|-------|-----|
| HU-1 | Made hand vs villain range | 5 | HU-1.1 .. HU-1.5 |
| HU-2 | Drawing hand profitability | 5 | HU-2.1 .. HU-2.5 |
| HU-3 | Air with backdoors | 5 | HU-3.1 .. HU-3.5 |
| HU-4 | PFA postflop discipline | 5 | HU-4.1 .. HU-4.5 |
| HU-5 | OOP decisions | 5 | HU-5.1 .. HU-5.5 |
| HU-6 | River decision precision | 5 | HU-6.1 .. HU-6.5 |

Per-axis: 3 CLOSE + 2 CANONICAL = 18 close + 12 canonical total.

## Per-axis breakouts (full hand specs)

- `HU_AXIS_1_MADE_HAND.md` — Axis HU-1 (5 hands, all TP+)
- `HU_AXIS_2_DRAWING.md` — Axis HU-2 (5 hands, all draws)
- `HU_AXIS_3_AIR_BACKDOORS.md` — Axis HU-3 (5 hands, all air)
- `HU_AXIS_4_PFA_POSTFLOP.md` — Axis HU-4 (5 hands, mixed composition)
- `HU_AXIS_5_OOP_DECISIONS.md` — Axis HU-5 (5 hands, mixed composition)
- `HU_AXIS_6_RIVER_PRECISION.md` — Axis HU-6 (5 hands, mostly TP+ + busted)

## Methodology compliance (binding)

- **Close-hand selection** per `feedback_close_hand_selection.md`: model
  uncertainty on v9-3way-on-59 + poker difficulty (NOT feature-stat
  extremes). Each CLOSE hand carries an explicit rationale citing
  v9-3way-on-59 model uncertainty with numbered (i)/(ii)/(iii) breakdown.
- **Canonical hands**: uncontroversial value-bet or fold spots; serve
  as ground-truth anchors for inter-labeller agreement.
- **Hand strength composition** per
  `feedback_preflop_geometry_vs_postflop_composition.md`: TP+/draws/air
  triple per hand. Axes HU-1/2/3 are pure (TP+/draws/air respectively);
  HU-4/5/6 mix.
- **Solver-aligned bet sizes** per `feedback_solver_aligned_sizing.md`:
  flop 25%/66%, turn 33%/75%, river 33%/75%/150%. Documented deviations
  only.
- **Terminology** per `feedback_terminology_raise_vs_bet.md`: "raise"
  = raise of existing bet; "bet" = first postflop bet; "open" = preflop
  opener; "donk-lead" / "lead" = OOP first-in postflop.
- **HU only**: every hand has `Num opponents: 1`. HU is the
  `num_opponents=1` value of the existing `num_opponents` feature in
  the 59-surface (per architect's β-anchor reasoning in §4.2).

## Cross-axis hygiene

- **Hand-class collisions**: zero (all 30 hand classes distinct across
  the 6 files; no suit-rotation duplicates). Verified post-fixer.
- **Flop board collisions** (suit-aware exact match): zero.
- **Hand-on-board collisions** (hero card appearing on its own board):
  zero.

Final 30 hand classes (canonical): AKo, 99, KQo, TT, AJs (HU-1) ·
AQs, T9s, J9s, 65s, A5s (HU-2) · 76o, 43s, KQs, T8o, A4s (HU-3) ·
JJ, 44, KTs, QJs, AJo (HU-4) · 77, 76s, QTo, T8s, KJo (HU-5) ·
KK, 88, ATs, AQo, Q9o (HU-6).

## Design dispatch evidence

- 6 design agents (one per axis) dispatched in parallel per
  `docs/PROCESS_GUIDE.md` §1.1, §1.2, §1.3
- 1 reviewer agent (independent design-stage) dispatched after design
  agents completed; findings file:
  `review/comms/REVIEWER_FINDINGS_PHASE15D1_HU_REFERENCE_SET_DESIGN_2026-05-10.md`
- Reviewer verdict: APPROVE_WITH_FINDINGS (2 MUST-FIX + 2 SHOULD-FIX,
  all resolved by fixer agent before PR open)

## Negative scope (per dispatch)

- ❌ Does NOT execute 1.5-D.2 labelling (separate sub-sub-phase)
- ❌ Does NOT execute 1.5-D.3 corpus assembly (separate)
- ❌ Does NOT execute 1.5-D.4 retrain (separate)
- ❌ Does NOT modify any source / data / prompt / model files (DESIGN ONLY)
- ❌ Does NOT touch v8-HU-38 artifacts (Path β chosen)

## Next sub-sub-phase

After this PR + QC verdict merge: orchestrator dispatches Phase 1.5-D.2
(HU labelling pipeline; pilot 5 hands → Sonnet→Opus tier-up gate →
full 25 hands) per design memo §4.3.
