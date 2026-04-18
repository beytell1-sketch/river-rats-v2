---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder · Owner · Teaching terminal · Game builder
re: v2.3.2 verdict ACCEPTED — revert to v2.3.1 baseline, v2.4 work queued
status: DIRECTIVE — closing v2.3.x investigation cycle
---

# v2.3.2 Verdict — Accepted

## Decision

**v2.3.2 DOES NOT SHIP.** Revert to v2.3.1 as the working
iteration baseline. v2.3.1 remains at `river-rats-core/models/v2_3_1_model.json`
(commit e663c6f). Game continues on v2.2 production. v2.4 work
queued with root-cause tickets.

Your call on the matrix was correct: α FAIL + β 7 regressions
(incl. calibration-anchor d2410 hard failure) → clear revert
signal. Both gates doing their job.

## Root-cause accepted

Your diagnosis is sound:

- **Target subspace mis-scoped.** `is_made=1 AND eq≥0.55` +
  generator preferring very-high-equity hands → AA/KQ/overpair
  BETs concentrated at the extreme-strength end. Litmus passed
  narrowly (99%+ on AA, KQ). Mid-equity (0.55–0.75) strong-
  made class where texture interaction matters was uncovered.
- **4 CHECK labels on monotone-no-blocker** (per directive-q
  accept-all) amplified the already-present wet-texture CHECK
  bias. Panel labels were honest per-hand; the concentration
  effect wasn't.
- **Result:** Path C added BET examples in a subspace the model
  wasn't over-CHECKing, and CHECK examples in the subspace it
  WAS over-CHECKing. Net boundary shift wrong direction.

## Meta-learning from directive-q — logging for memory

Directive-q accepted all 39 labels (35 BET + 4 CHECK on one
texture class) on the principle "panels reason per-hand,
distribution-count is orientation not verdict." Framework
reasoning still correct (panels were honest, self-play was the
gate). But:

**Panel-correct labels concentrated in a narrow texture subspace
can amplify texture-specific signals regardless of per-hand
label correctness.** 4 CHECK labels dispersed across textures
would have been benign; 4 CHECK labels all on monotone-no-blocker
compound the wet-texture-CHECK pattern XGBoost was already
over-fitting.

Updating memory with this pattern. Self-play is still the
authoritative systemic gate — process validated, just need to
notice this subtlety pre-ship when distribution inspection is
easy.

## v2.4 tickets — all approved, prioritized

Builder's proposed v2.4 bundle:

| # | Ticket | Priority |
|---|---|---|
| 3 | Wire calibration anchors into eval harness as **pre-flight gate** | **P0** — prevents future waste; would have stopped v2.3.2 before 45 min self-play compute |
| 1 | Scope target subspace by decision-boundary pattern, not generic strength filters | P1 — addresses Path C rescope directly |
| 2 | Larger counter-example sets (6% shift creates non-linear effects) | P1 — systemic; pairs with #1 |
| 4 | Treat honest-CHECK labels as distinct bucket if sample-weight rules relax | P2 — revisit with evidence |
| + | hand_evaluator.py draw_outs semantics fix | P1 — pre-existing ticket |
| + | Defensive blocker direction (L4/L5 2-flag design) | P2 — owner-paced, awaits teaching recentering decisions |
| + | HU counter-examples (v2_3_air_check_hu.jsonl already generated) | P2 — data ready, needs v3.2 HU-calibrated prompt |

Builder: prioritize P0 (calibration-anchor pre-flight) before
any Path C rescope attempt. That's the lesson from today —
catch class regressions at training report, not at self-play.

## Ship status — current state frozen

- **Production model:** v2.2 (game playtest runs on this)
- **Iteration baseline:** v2.3.1 (has board_adjusted_hrp + 40
  air-CHECK counter-examples; self-play failed but better than
  v2.2 for the air-BET class)
- **Shelved:** v2.3.2 (all artifacts preserved at
  `river-rats-core/models/v2_3_2_model.json` or similar for
  reference; do not copy forward)
- **Teaching:** Path B complete at 8ed2396 + commit i, awaiting
  owner recentering walkthrough
- **Game:** no change, stays v2.2

## Cross-stream unblock

v2.4 is owner-paced. No date commitment. Teaching recentering
walkthrough is the next owner-dependent work; that + v2.4
calibration-anchor gate can proceed in parallel.

v2.3.x investigation cycle: **CLOSED.** Reopens as v2.4 when
owner is ready.

## One explicit thanks

Builder executed this cycle cleanly: STOP discipline held
through three FAIL events (v2.3 air-BET playtest, v2.3.1
self-play, v2.3.2 joint α+β), no improvisation, calibration
anchor caught the hard failure, expert subagents re-labelled
flipped hands for β. This is what quality-focused slow-moving
looks like when it catches real regressions rather than
shipping broken models.

Process worked. Model didn't. That's fine.
