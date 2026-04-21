---
date: 2026-04-21
from: Main terminal (orchestrator)
to: Builder (future v2.6+ work) · Teaching · Owner
re: v2.6+ queue — hero postflop range tracking; symmetric to villain action-history chain
status: QUEUED for v2.6+; explicit out-of-scope for v2.4 and v2.5
---

# v2.6+ Queued — Hero Postflop Range Tracking

Owner audit question (2026-04-21): given the villain action-history
chain represents villain's range narrowed by villain's actions,
can we represent **hero's** range narrowed by **hero's** action
history?

Honest answer: **no.** Hero is treated as a hand, not a range,
postflop. This is a representation gap, not a calibration gap.
Symmetric to the villain chain by design but not built.

## What exists today

`feature_extractor.py:1541-1579` — `compute_hero_range_percentile`:

```python
hero_range = _range_manager.get_postflop_range(hero_pos, is_pfr=is_pfr)
return _range_manager.get_hand_percentile(hand_notation, hero_range, board_cards)
```

Hero's range is constructed once at the preflop boundary using
`(hero_pos, is_pfr)` only. Two distinctions:
- Position (UTG / MP / CO / BTN / SB / BB)
- PFR vs caller (was hero the preflop raiser?)

That range is then **frozen** for all postflop streets. It feeds:
- `hero_range_percentile` (Feature 49)
- `board_adjusted_hrp` (Step 16) = `hero_range_percentile × equity_vs_range`
- Any teaching field that wants to express hero's relative position
  in their own range

## What's missing

No `narrow_by_action_history_for_hero` exists. There is no:
- Update to hero's range when hero check-calls (range caps)
- Update to hero's range when hero check-raises (range polarises)
- Update to hero's range when hero leads (range concentrates on
  the leading-range subset)
- Hero range object passed through the hand
- Hero range exposure to teaching layer

A BB defender who has check-called flop and turn carries the same
"BB-defending vs CO-RFI" range into a river decision as a BB
defender who check-raised the flop and barreled the turn. Both
read identically into `hero_range_percentile`.

## Why this matters

### Quantitative — feature accuracy

`hero_range_percentile` is currently mis-calibrated for any
non-trivial hero line. Concretely:

- **Capped lines:** hero check-calls flop and turn → real range is
  now stripped of nutty hands (those would check-raise) and
  polarised toward medium-made + draws. KK in this spot is now
  effectively the top of a capped range — but Feature 49 reports
  KK at its un-narrowed BB-defending percentile (~mid-90s). The
  feature understates KK's relative strength on capped lines and
  overstates it on uncapped lines.
- **Polarised lines:** hero leads turn after flop check-call → real
  range is two-pair-plus or pure bluff. Feature 49 reads the full
  defending range.
- **Board-adjusted HRP** (Step 16) inherits the same error as it's
  a multiplier of `hero_range_percentile`.

Magnitude is unmeasured. Likely material on multi-street lines;
probably small at flop decisions (chain has nothing to apply yet).

### Qualitative — teaching coverage

Range-based thinking is the central pillar of the teaching
philosophy. Today the system can say:

- "Villain's range here is ~60% medium-made, 30% draws, 10% air"
  ✅ shipped at l3_enriched_v3.0

The system **cannot** say:

- "Your range here is capped — your KK now plays as a bluff-catcher"
- "Your check-raise here represents two-pair-plus or pure bluff;
  villain knows this"
- "Your river donk range is polarised; balance your bluffs to your
  value"

These are the instructions that move a player from hand-thinking
to range-thinking. They are absent because the underlying object
isn't built.

## Scope sketch (v2.6+)

### Architecture

1. **Hero range as a first-class representable object.** Mirrors
   villain — a `Dict[hand_notation, frequency]` updated through
   the hand.
2. **`narrow_hero_by_action_history`** — symmetric to villain:
   walks hero's action sequence street-by-street, applies bet /
   check / call / raise narrowing, returns `(narrowed_range, meta)`.
3. **Frequency tables for hero actions.** Not the villain tables
   verbatim — hero is a single seat with known prior actions, not
   an opponent inferred from observable choices. Likely needs
   solver-grounded derivation. Multi-day data task.
4. **Feature recomputation:** `hero_range_percentile` and
   `board_adjusted_hrp` re-derive against the chain-narrowed hero
   range. Backfill audit on training CSV; document magnitude of
   shift.
5. **Teaching surface:** new fields exposed in CONTENT_API for
   hero composition (mirror of villain_*_pct):
   - `hero_tp_pct`, `hero_medium_made_pct`, `hero_draw_pct`,
     `hero_air_pct`
   - `hero_range_capped`, `hero_range_polarised`
   - `hero_position_in_range_desc`

### Integration order (when greenlit)

1. Architecture spec — symmetric module to villain narrowing
2. Solver data commission for hero-action frequency tables
3. Implementation behind a feature flag; comparison run vs current
4. Backfill audit → magnitude report → owner decision on retrain
5. Stage gate: retrain + feature recomputation + teaching schema
   bump
6. Teaching layer adds hero-side composition fields
7. Game prototype renders hero composition (parallel to villain)

This is a multi-stage release of a sibling subsystem to villain
range tracking. Bigger lift than v2.5 sizing-conditional narrowing,
because it touches features + teaching + game in a coordinated
ship.

## Why v2.6+ not v2.4 or v2.5

- v2.4 Stage 3.5 closes the most visible bug today (villain action
  chaining). Ship that first.
- v2.5 candidates (bet-sizing-conditional, raise-aware-call) refine
  the existing villain chain. Same code paths.
- Hero range tracking is a **new subsystem** — it adds a sibling to
  the villain chain, plus new teaching fields, plus new game
  rendering. Coordinated cross-stream release.
- Pre-requirement: villain side stable through v2.4 and v2.5 first;
  hero side mirrors a known-good architecture.

## Out of scope for this ticket

- Modelling villain's range conditioned on hero's actions (raise-
  aware call, sizing-conditional) — those are v2.5 candidates
  about villain-side narrowing and remain in their own ticket.
- Hero range modelling for the **oracle** itself — the model
  receives hero's hand directly; it does not need to receive
  hero's range. This ticket is about feature accuracy + teaching
  representation.

## Symmetry table (where the gap lives)

| Subsystem | Villain | Hero |
|---|---|---|
| Preflop range construction | ✅ position + facing-action | ✅ position + PFR/caller |
| Postflop action-history chain | 🟡 v2.4 Stage 3.5 (5 MUSTs in flight) | ❌ NOT MODELLED |
| Composition features (TP+/medium/draw/air) | ✅ shipped | ❌ does not exist |
| Range-shape teaching fields | ✅ l3_enriched_v3.0 | ❌ no analogue |
| Game-side range rendering | ✅ V1 range bar | ❌ no analogue |

Every cell with ❌ in the hero column would be in scope for this
work.

## Action

- v2.4 Stage 3.5: **proceed unchanged.**
- v2.5 candidates: unchanged in priority.
- Add to manifest `pro_level_narrowing_gaps.deferred_architectural`
  and to `queued.v2_6_candidates` (new section).
- Owner decision point for v2.6+ later: prioritise hero range
  tracking against multiway cross-conditioning when v2.5 is
  stable. Both are architectural; both require data work; both
  unlock teaching coverage that doesn't exist today.

## Reference

- `feature_extractor.py:1541-1579` — current hero range construction
- `range_narrowing.py:695-843` — villain action-history chain (the
  pattern to mirror)
- `RELEASE_MANIFEST.yaml` `pro_level_narrowing_gaps` — sibling gaps
- `MAIN_TERMINAL_MULTIAGENT_RECONCILIATION_2026-04-20.md` — Stage
  3.5 MUSTs (villain side) blocking v2.4 ship
