---
date: 2026-04-19
from: Builder
to: Main terminal / Owner (+ GTO reviewer subagent for feature validation)
re: v2.4 P1 — new feature PLAN — `draw_block_pct` (continuous, 0-1)
status: PLAN — awaiting GTO-reviewer subagent validation before any code
related: directive-x (2026-04-19), TICKET_BLOCKER_DIRECTION_DEFENSIVE_2026-04-18.md
---

# P1 Plan — `draw_block_pct` (Feature 2 of 3)

## Sequence context

1. `nut_flush_block` — flush-specific boolean (plan 1, separate doc)
2. **`draw_block_pct`** ← this plan (broader bluff-removal signal, continuous)
3. `nut_made_block_pct` — replaces `flush_block_pct` (plan 3)

## Intent of `draw_block_pct`

Surface the **directional blocker effect on villain's semi-bluff combos**
that the owner's Apr 18 observation exposed:

> "We have mid pair, two spades on the board, and we hold one (a Jack).
> The blocker makes it more likely villain is betting with a made hand —
> we block flush draws, weakening our mid pair."

This is the **densification / unblocker effect** on villain's betting
range. The existing pipeline has no directional signal for it (per
`TICKET_BLOCKER_DIRECTION_DEFENSIVE_2026-04-18.md` empirical finding:
`flush_block_pct` tagged PRIMARY 0× in 470 expert labels).

`draw_block_pct` measures the **fraction of villain's pre-bet DRAW
combos that hero's specific holdings block**. Higher = hero's
defensive blocker is WORSE (villain's bet range densifies toward
value).

## Exact definition

```
draw_block_pct = (# villain draw combos blocked by hero's hole cards)
                 / (# villain draw combos in pre-bet range)

Where:
  - "Draw combos" = flush draws (4-card same-suit including board) +
                     OESD + gutshot (from range_decomposition.py
                     classification — the existing _DRAWS subcategory
                     set: combo_draw, nut_flush_draw, flush_draw, oesd,
                     gutshot)
  - "Blocked by hero" = villain combo contains at least one of hero's
    hole cards (which is impossible — hero holds those cards)
```

Range: `[0.0, 1.0]`. Default 0.0 when villain has no draw combos
(e.g., on paired/rainbow dry boards).

### Key distinction from `flush_block_pct`

- `flush_block_pct` = fraction of villain's FLUSH range (made flushes
  + flush draws combined) blocked
- `draw_block_pct` = fraction of villain's DRAW range (flush draws
  AND straight draws AND combo draws) blocked

**The directional interpretation differs:**

- `flush_block_pct` conflates:
  - Blocking villain's made flush (good for hero when defending —
    more bluff-catchability)
  - Blocking villain's flush draw (bad for hero when defending —
    fewer semi-bluffs means villain's bet is more value-heavy)
- `draw_block_pct` isolates the DRAW-side blocking — the one that
  makes villain's betting range densify to value when hero defends.

## Feature derivation

`feature_extractor.py`. Requires access to villain's range
decomposition (already computed for `villain_top_pair_plus_pct` etc.).

```python
def _draw_block_pct(hole_cards, range_breakdown):
    """Fraction of villain's draw combos blocked by hero's hole cards."""
    if range_breakdown is None or range_breakdown.total_combos == 0:
        return 0.0

    _DRAW_SUBCATS = {
        'combo_draw', 'nut_flush_draw', 'flush_draw', 'oesd', 'gutshot',
    }

    hole_set = set(c.lower() for c in hole_cards)

    draw_combos = 0
    blocked_combos = 0
    for bucket in range_breakdown.buckets:
        if bucket.subcategory not in _DRAW_SUBCATS:
            continue
        # Each bucket has a list of combos (pairs of cards).
        # Check each combo for hero-card overlap.
        for combo in bucket.combos:
            draw_combos += 1
            if any(c.lower() in hole_set for c in combo):
                blocked_combos += 1

    if draw_combos == 0:
        return 0.0
    return blocked_combos / draw_combos
```

Output: `draw_block_pct`, float [0.0, 1.0], feature #57 (after
`nut_flush_block` at #56).

## Why this lives alongside `flush_block_pct` (NOT replacing it)

Per directive-x: "Do NOT yet modify `flush_block_pct`; retirement
comes after `nut_made_block_pct` validates." This plan respects that.

`draw_block_pct` is the DEFENSIVE-BLOCKER signal. `flush_block_pct`
(to be evaluated for retirement in plan 3) is the AGGRESSOR-BLOCKER
signal (how much of villain's flush range your blocker removes when
you bluff-raise).

## Expected model behavior

The model should learn:

- **Defending (facing_bet = 1) with marginal made hand + high
  `draw_block_pct`** → hero's bluff-catcher equity is overstated by
  `equity_vs_range` alone; model should lean CHECK/FOLD/CALL-less.
  This is the owner-flagged scenario.
- **Bluffing/semi-bluffing aggressor with high `draw_block_pct`** →
  effect is ambiguous. In hero's bluff line, blocking villain's
  draws doesn't help hero's fold equity much (villain folds draws
  to a bet with or without hero's card blocker). Model likely learns
  this is near-neutral.
- **Value betting with high `draw_block_pct`** → hero blocks the
  semi-bluff portion of villain's calling range → villain calls
  with value more often → hero's thin value is thinner. Mild
  negative on thin value bets. Conversely, hero's value bets get
  called fairly.

The multi-direction interpretation is why we expose this as a
feature rather than hardcoding the signal: the model's tree splits
interact with `facing_bet`, `is_made_hand`, `expert_action` to learn
context-appropriate weightings.

## Feature attention guidance (for v3.2 prompt)

In the v3.2 labelling prompt (not written yet — this is v2.4 scope
later), `draw_block_pct` should be:

- PRIMARY for **Medium-made / Weak-made + facing_bet = 1** (the
  owner's scenario): "Is hero's blocker reducing villain's
  bluff-to-value ratio below the bluff-catch threshold?"
- CONFIRMED for **Drawing / Air + bluffing aggressor**: checked but
  rarely decision-critical.
- Default for **Strong-made / Monster + facing_bet = 0**: most
  decisions are value-bet driven; blocker effect minor.

Prompt-side changes come AFTER v2.4 feature is live. This plan only
specifies feature semantics.

## Validation plan (post-approval)

1. Unit tests: on synthetic situations with known draw combos,
   verify block fractions match hand-calculation.
2. Backfill existing training CSV. Since `range_breakdown` is
   computed at feature-extraction time from `hero_cards` +
   `board_cards` + preflop action, all existing rows can be
   re-extracted for this feature only.
3. Distribution audit:
   - Mean `draw_block_pct` across training data — sanity-check
     that the median isn't ~0 or ~1 (would imply feature is
     degenerate)
   - Hero's spot-class vs `draw_block_pct` correlation: hands
     with 1+ suited connector should have higher block% on wet
     boards
4. **No model training** yet — gated on all 3 plans approved.

## Open questions for GTO reviewer

1. **Is "draw combos" the right granularity?** Alternative: split
   into `flush_draw_block_pct` and `straight_draw_block_pct`. The
   owner's scenario specifically invoked flush-draw blocking; if
   that's the primary class, a flush-specific version might carry
   the signal better than a combined metric.

2. **Should draw combos with more than one outs-class (e.g., combo
   draws) be weighted differently?** Blocking a combo-draw combo
   (9 outs + OESD) removes more fold-equity probability than
   blocking a 4-out gutshot. The current definition treats all
   "draw" combos equally. Weight-by-outs variant could be:
   `sum(blocked_combos * outs) / sum(all_draw_combos * outs)`.

3. **Unblocker effect on straight draws specifically.** On
   connected boards (e.g., 9h8s5c), hero's Th blocks TOH-one-combo
   of villain's OESD JT. But villain might also have 76-OESD that
   hero doesn't block. Is `draw_block_pct` sensitive enough to
   capture this asymmetry, or does it need to be suit/rank
   aware?

4. **Interaction with `villain_draw_pct`.** `villain_draw_pct` is
   the SIZE of villain's draw portion (% of range that's drawing).
   `draw_block_pct` is the FRACTION of that draw portion hero
   blocks. Both are needed for the "densification" reasoning
   (low villain_draw_pct means blocking a lot of it is less
   impactful on overall range). Are these two features enough,
   or do we need a derived `effective_draw_block` = product?

5. **Numerical stability.** When villain has very few draw combos
   (e.g., dry rainbow board), `draw_block_pct` can be 0.0 or
   undefined. Current plan returns 0.0. Is that the right null
   semantics, or should we return a NaN sentinel the model
   doesn't try to interpret?

## What this plan does NOT cover

- Plan for `nut_flush_block` (separate doc, approved independently)
- Plan for `nut_made_block_pct` (separate doc)
- `flush_block_pct` retirement (deferred per directive-x)
- v3.2 prompt update with feature_attention guidance (later scope)
- Model training (not yet)

Ready for GTO reviewer subagent to validate.
