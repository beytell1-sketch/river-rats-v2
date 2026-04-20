---
date: 2026-04-20
from: Builder
to: Owner (+ orchestrator for manifest update)
re: Stage 3.5 range-narrowing — GTO verdict APPROVED_WITH_MODS; spec now LOCKED for implementation
status: SPEC LOCKED — awaiting owner go-ahead on implementation
related: GTO_REVIEW_V24_STAGE35_RANGE_NARROWING_2026-04-20.md (just landed)
---

# Stage 3.5 Spec Locked — Implementation-Ready

GTO reviewer returned **APPROVED_WITH_MODIFICATIONS**. Mechanism is
poker-correct. Seven prioritized changes before code. All three
prior docs' open questions resolved.

## Two scope-question answers

### Q1 — CALL-narrow path → **Option A, REFINED**

Not the builder's "derive from 1-fold-raise using existing tables"
— that aliases the wrong tables. Instead use a **direct per-category
CALL-continue multiplier table**:

```python
FLOP_CALL_FREQUENCIES = {
    'nuts': 0.15, 'strong_value': 0.35, 'good_value': 0.75,
    'draw': 0.70, 'medium_made': 0.55, 'weak_made': 0.30,
    'bluff': 0.15, 'air': 0.05,
}
TURN_CALL_FREQUENCIES = {
    'nuts': 0.15, 'strong_value': 0.30, 'good_value': 0.70,
    'draw': 0.55, 'medium_made': 0.50, 'weak_made': 0.15,
    'bluff': 0.10, 'air': 0.03,
}
RIVER_CALL_FREQUENCIES = {
    'nuts': 0.20, 'strong_value': 0.40, 'good_value': 0.65,
    'draw': 0.00, 'medium_made': 0.55, 'weak_made': 0.20,
    'bluff': 0.05, 'air': 0.02,
}
```

Two poker properties the alias formula lacks:
1. `medium_made` stays elevated across streets — that's the
   canonical bluff-catch/showdown-value band.
2. `nuts` / `strong_value` get suppressed in CALL-continue because
   they raise, not just continue.

Documented as "heuristic, v2.4 MVP, not direct solver output."

**Anchor note:** d2410 / d0182 / d8411 all had villain CHECK (not
call) on the flop. CALL-narrow doesn't fire on those chains. The
heuristic table matters for playtest hands like H_8dfb6ef8, not
for our 3 load-bearing anchors.

### Q2 — Same-street pre-hero actions → **NO (exclude)**

Chain runs only STRICTLY prior-street actions. Four reviewer
reasons:

1. Flop check-to-IP signal already encoded via `facing_bet=0`;
   adding it would double-count
2. 3-way flop check-freq ~57% (§1.3) — check is weakly informative
3. "Historical" should mean "prior decision point," not "prior
   move on same street"
4. Turn-check-through (owner's scenario) is fixed by prior-street-
   only logic; no need to extend

**Bonus upside:** preserves the 4 flop calibration anchors as
ZERO-impact controls, with real diagnostic value (if they shift
after Stage 3.5, the isolation is broken).

## Additional non-negotiable changes before code

### M1 — Update `RIVER_BETTING_FREQUENCIES` for 3-way (FLAG A)

Two entries are HU-correct but over-state 3-way bluff density
when applied post-chain:

```python
RIVER_BETTING_FREQUENCIES['bluff'] = 0.20  # was 0.35 — per §1.4
RIVER_BETTING_FREQUENCIES['air']   = 0.10  # was 0.20 — per §1.4, §1.7
```

Rationale: §1.4 explicitly says 3-way river bluff:value ratio is
"~1:4 or tighter" → ~20% bluffs. The current 0.35 reflects HU
theory. Post-chain, this bias compounds — the river-bet filter
runs on an already-narrowed range, so an inflated bluff fraction
directly pulls TP+ down.

Flop and turn entries are fine; no change.

### M2 — Three safety rails in the chain (FLAG B)

1. **Empty-chain fallback.** If a narrowing step produces
   `total_weight == 0`, do NOT return `{}` to
   `classify_villain_range` (would silently zero out composition
   features). Return the previous valid step's range + log a
   warning.
2. **Weight-floor threshold.** Track cumulative surviving weight.
   If chain drops below 5% of original total range weight,
   short-circuit with warning or reset to last valid intermediate.
3. **Surviving-weight metadata.** Expose
   `_villain_range_surviving_weight` as a metadata field so
   downstream consumers can distinguish "fraction of surviving
   range that is air" from "fraction of original range that is
   air." Current consumers likely OK with normalized fractions
   but confirm before calling done.

### M3 — Extended unit-test plan

Original plan's test list expanded:
- `H_8dfb6ef8` chain (bet-check-call-bet) as canonical
- Turn-check-through → river-bet (owner's scenario)
- Flop-check → turn-decision (d2410 shape)
- Deep chain (4+ actions) for empty-range guard
- Schema-mismatch guard (wrong key in action entry)

### M4 — Retroactive audit before Stage 4

Before any retrain, produce distribution-shift report on the 10
villain-composition features across ~700 training rows:
- Multi-street hands: any direction change is expected
- Flop-only hands: near-zero shift (isolation check)

### M5 — Pre-retrain diagnostic on v2.3.1 model

Run the v2.3.1 model inference on d2410 / d0182 / d8411 using
NEW (action-chained) feature values.

- **If BET restored on d2410** → feature correctness alone fixes
  the regression. Stage 4 re-label becomes additive insurance.
- **If still CHECK** → diagnosis is Stage 4 re-label (class
  imbalance), not Stage 3.5.

Either outcome informs the Stage 4 scope. Cheap diagnostic (runs
in seconds).

### M6 — d2410 expected direction

Reviewer predicts **BET confidence UP** after Stage 3.5.
Mechanism:
- Flop-CHECK filter drops premium pockets (AA/KK/QQ) that would
  have bet flop
- Post-check range is **condensed, capped** (§1.3)
- Turn-bet filter applied to a capped range raises medium_made /
  bluff density, lowers TP+ density
- Hero's TPGK is ahead of a larger fraction of villain's actual
  turn-bet range
- Value-bet EV up → model restores BET

If the model does NOT flip, diagnosis is Stage 4, not Stage 3.5.

### M7 — Keep scope narrow

Reviewer concurs with builder §4.2: one CALL-continue table per
street, applied uniformly regardless of facing-bet-vs-facing-raise.
Raise-aware variants deferred to v2.5+ unless playtest shows bias.

## The verified chain composition

Reviewer walked the H_8dfb6ef8 bet-check-call-bet chain manually:
- Flop: BB bet → `narrow_to_betting_range` flop (`good_value` 0.70)
- Turn: BB check → `narrow_to_checking_range` turn (× 0.40 → 0.28 of preflop)
- Turn: BB call → `narrow_to_continuing_range` turn (× 0.70 → 0.196)
- River: BB bet → `narrow_to_betting_range` river (× 0.55 → 0.108)

Compound: 10.8% of `good_value` survives to river-bet; 1.3% of
`medium_made` survives. Solver-intuitive: "BB who bet-checked-
called-bet is value-heavy, bluff-light, medium almost extinct."

Chain composes correctly. No double-counting. **PASS.**

## Risk unknowns (will test for)

1. Range collapsing to empty on 4+-action chains
2. NaN weights if normalizer divides by zero (current guard OK;
   chain must not bypass)
3. Compute cost: ~3x (60ms per decision estimated). 700-row
   regen ~minutes not hours; consider cached per-board-per-hand
   classification
4. Action-history schema drift: assert first entry's keys at
   chain entry

## Implementation plan (locked)

File changes:
1. `river-rats-core/range_narrowing.py` — add:
   - `FLOP_CALL_FREQUENCIES`, `TURN_CALL_FREQUENCIES`, `RIVER_CALL_FREQUENCIES` (M1)
   - `narrow_to_continuing_range` function
   - `narrow_by_action_history` function with 3 safety rails (M2)
   - Update `RIVER_BETTING_FREQUENCIES['bluff']` and `['air']` (M1)

2. `river-rats-core/feature_extractor.py::classify_villain_range` —
   swap single-street gate for `narrow_by_action_history` call;
   fallback to old path when action_history is unavailable.

3. `river-rats-core/tests/test_range_narrowing.py` — unit tests
   per M3.

4. Standalone backfill/audit script —
   `review/run_stage35_backfill_audit.py` generating distribution-
   shift report per M4.

5. Standalone diagnostic script —
   `review/run_v231_anchor_recheck_stage35.py` for M5.

No other changes this stage. Does not touch `gto_model.py`
FEATURE_COLUMNS (those stay at 55 for v2.3.x inference compat).
Does not touch the 4 new v2.4 P1 blocker features (they
inherit the corrected range automatically).

## Verification before Stage 3.5 complete

| Check | Expected | Action if fail |
|---|---|---|
| All M3 unit tests pass | 100% | Fix before commit |
| `d2410` re-inference on v2.3.1 model | BET at HIGH | Surface to reviewer; don't auto-fix |
| 4 flop calibration anchors still pass | 5/5 on v2.3.1 model w/ new features | Bug in isolation — same-street actually leaking |
| Distribution-shift report on 700 rows | Flop-only ≈ 0 shift; multi-street non-zero | If flop-only > threshold, same-street leak |
| Compute cost per decision | < 100ms | Cache classifications |
| `villain_range_surviving_weight` metadata populated | Non-NaN, in (0, 1] | Safety rail broken |

## NOT in Stage 3.5 scope (explicit)

Reviewer explicitly concurred with builder scope boundaries:

- Raise-aware call narrowing — v2.5+
- Multiway cross-conditioning beyond primary villain — v2.5+
- Opponent-specific baseline ranges — pre-existing, separate
- `hand_evaluator.py` straight-draw bug — independent ticket
- `flush_block_pct` retirement — post-Stage 5 A/B decision
- Teaching recentering — owner-paced separate stream

## What would make GTO reviewer reject

- Stage 3.5 ships with alias-formula CALL-continue (rejected)
- Stage 3.5 includes same-street pre-hero actions in the chain
  (rejected)
- Stage 3.5 defers the RIVER_BETTING_FREQUENCIES updates
  (discouraged; reviewer OK'd deferral only if retro-audit shows
  shift within ±3pp on bluff density)

## Asks for owner before implementation

1. **Confirm spec lock** — builder implements per M1-M7 above. No
   further spec discussion needed unless owner wants changes.
2. **Confirm sequencing** — Stage 3.5 implementation proceeds in
   parallel with Stage 3 (v3.2 prompt)? Or does owner want Stage
   3 complete first?
3. **Confirm scope of retroactive audit (M4)** — distribution-
   shift report on all ~700 training rows OK, or owner wants a
   smaller sample for first look?

Once confirmed I start implementation. Budget estimate ~4-6
hours (table updates + 2 new functions + wiring + 5 unit tests +
backfill audit + diagnostic run + report).

Standing by.
