---
date: 2026-04-19
from: Main terminal (reviewer/orchestrator)
to: Builder (logic team)
re: Logic team instructions — start v2.4 P0 (calibration-anchor pre-flight), scope P1 features in parallel
status: DIRECTIVE — P0 work begins now; P1 scoping in parallel; no model training yet
---

# Logic Team — Current Instructions

## Context

v2.3.x investigation cycle closed. Baseline: v2.3.1 (iteration
anchor; not production). Game stays on v2.2 production. Teaching
is recentering in parallel. Game is building range-bar UI.

Your work now: **build the pre-flight validation infrastructure
and scope the blocker features, without starting model training.**
The v2.3.x lessons taught us that the eval harness was weaker
than it needed to be. Fix that before the next training cycle,
not during.

## Do now — P0: calibration-anchor pre-flight gate

Per directive-t: wire calibration anchors into the eval harness
as a **pre-flight gate** that runs BEFORE self-play.

### Requirements

- Accept a list of known-correct anchor hands (hero cards +
  board + street + action_history + solver-verified correct
  action)
- For each anchor, run the model under test and compare
  predicted action against the solver label
- Gate semantics: ANY anchor miss → FAIL, report which anchor(s)
  and the model's prediction + confidence
- Run BEFORE self-play and holdout evaluation — cheap (seconds)
  so it catches distribution-shift regressions before burning
  30-45 min of self-play compute
- Report format matches existing eval tier reports

### Anchor set — start minimal, grow over time

Seed anchors from what we've already got:

- **d2410_CO_turn** (v2.3.2 hard failure — solver-verified BET)
- **A4d/Qs5s7s flop** (directive-g litmus — CHECK)
- **T5h/JJ2 flop** (directive-g litmus — CHECK)
- **AA/7h5d2c flop** (directive-o litmus — BET)
- **KQ/KsTs3h flop** (directive-o litmus — BET)

Five anchors is enough for v1. Grow as playtest surfaces more
solver-verified spots.

### Storage + discipline

- Anchors live as structured JSON at
  `river-rats-core/anchors/calibration_anchors.json` (or
  similar path matching existing conventions)
- Each anchor includes: hero cards, board, street, history,
  position context, correct action, solver source reference,
  date added
- Adding an anchor requires solver verification — no
  "probably correct" entries. If unclear, flag and solve.
- Pre-flight gate is DETERMINISTIC. Same model + anchors →
  identical pass/fail.

### Integration

Wire into the existing eval harness as tier 0 (before tier 1
standard gates). Fail-fast: don't continue to tier 1+ if
pre-flight fails. STOP-and-report discipline per CLAUDE.md §5.

## Do in parallel — scope v2.4 P1 blocker features

Per directive-u: three new blocker features queued for v2.4.
Scope each one as an **implementation plan doc** before writing
code. Same discipline as Path B planning: plan → expert review
→ small commits.

### For each of the three features:

**`nut_flush_block` (P0 among blocker features — simplest):**
- Plan doc: exact signature, exact location in
  `feature_extractor.py` (near existing flush_block_pct at line
  1240-1362), exact compute logic
- Integration: add to feature vector (expand from 55 to 56
  features — confirm no downstream breakage)
- Tests: unit tests covering Ace-of-suit vs non-Ace-of-suit
  hero cards, monotone vs two-tone vs rainbow board

**`draw_block_pct` (P1):**
- Plan doc: signature, location, compute logic using
  `range_decomposition.py` subcategory output
- Range-weighted math — confirm which range (preflop or
  current-street narrowed) is used; match convention of
  existing `flush_block_pct`
- Tests: unit tests covering hero blocks villain flush draws,
  hero blocks villain straight draws, hero blocks both, hero
  blocks neither

**`nut_made_block_pct` (P1):**
- Plan doc: signature, location, compute logic spanning all
  nut-category made hands (set, two-pair, straight, flush,
  full house)
- Reuses `hand_categories.py:488-530 count_combos_with_blockers`
  utility
- Eventually replaces `flush_block_pct`; plan includes the
  retirement path (parallel feature for one training cycle
  while both validate, then retire flush_block_pct)
- Tests as above, plus comparison test: on a flush-possible
  board, `nut_made_block_pct` should include what
  `flush_block_pct` measures

### Scope docs location

`review/comms/` with names like:
- `BUILDER_NUT_FLUSH_BLOCK_PLAN_2026-04-19.md`
- `BUILDER_DRAW_BLOCK_PCT_PLAN_2026-04-19.md`
- `BUILDER_NUT_MADE_BLOCK_PCT_PLAN_2026-04-19.md`

One doc per feature. Each gets expert review (GTO reviewer
subagent for poker correctness) before any code ships.

## Do NOT do yet

- Do NOT start model training. v2.4 model work waits for owner
  signal after the pre-flight gate + feature plans are
  reviewed.
- Do NOT touch teaching layer — teaching recentering owns that,
  and the PlayerLevel enum / coaching module imports are their
  territory.
- Do NOT modify `flush_block_pct` yet. It stays in place until
  `nut_made_block_pct` is validated.
- Do NOT paper over v2.3.1 self-play fail — v2.3.1 is the
  iteration baseline, not the production model. Production
  stays v2.2.

## Cross-stream awareness

- **Game:** building range-bar + action-order UI on v2.2 — your
  pre-flight work is orthogonal
- **Teaching:** executing plan v2 for V4.0 schema — your
  feature expansion feeds into future teaching flags (blocker
  placeholder in their locked directive awaits your features)
- **Playtest:** owner's hand-log system is now complete with
  SHAP + commit SHAs + schema version (game's 817b646). When
  playtest runs, findings route to logic/teaching feedback
  boxes; logic team consumes the logic-tagged entries.

## Ship order when v2.4 training starts (eventual)

1. Pre-flight gate wired + anchors loaded (this directive)
2. `nut_flush_block` feature plan reviewed + implemented
3. `draw_block_pct` feature plan reviewed + implemented
4. `nut_made_block_pct` feature plan reviewed + implemented
5. New training data assembled with expanded feature vector
6. v2.4 training run with pre-flight gate enforced pre-self-play
7. Full 4-tier eval including self-play
8. Ship if clean; STOP-and-report if not

No pressure on timeline. Quality-focused, slow, no rush. Get
pre-flight and feature plans right before training starts.

## Reporting cadence

- Pre-flight gate: report when wired + first anchor set runs
  (pass/fail against v2.3.1 baseline — expect d2410 to fail on
  v2.3.1 since that's the known regression)
- Feature plans: each plan gets its own push + review cycle
- Any blocker: STOP-and-report per CLAUDE.md §5

Go.
