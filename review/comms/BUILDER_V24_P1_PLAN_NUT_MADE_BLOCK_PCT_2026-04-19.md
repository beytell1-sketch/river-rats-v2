---
date: 2026-04-19
from: Builder
to: Main terminal / Owner (+ GTO reviewer subagent for feature validation)
re: v2.4 P1 — new feature PLAN — `nut_made_block_pct` (continuous, 0-1; flush_block_pct retirement-gate)
status: PLAN — awaiting GTO-reviewer subagent validation before any code
related: directive-x (2026-04-19), TICKET_BLOCKER_DIRECTION_DEFENSIVE_2026-04-18.md
---

# P1 Plan — `nut_made_block_pct` (Feature 3 of 3)

## Sequence context

1. `nut_flush_block` — flush-specific boolean (plan 1)
2. `draw_block_pct` — bluff-removal continuous (plan 2)
3. **`nut_made_block_pct`** ← this plan (villain's MADE-nut blocking; retirement-gate for `flush_block_pct`)

Per directive-x: `flush_block_pct` is flagged for retirement AFTER
`nut_made_block_pct` validates as a replacement. This plan specifies
the replacement feature.

## Intent of `nut_made_block_pct`

Surface the **aggressor-favorable** blocker effect that KB §1.7 and
§1.8 already identify — how much of villain's nut-made range hero's
hole cards block. This is the signal hero uses when deciding RAISE
vs CALL with a strong hand or semi-bluff.

Existing `flush_block_pct` attempts this but is:

1. **Flush-only.** Doesn't count blocking villain's set/straight/
   full-house ranges.
2. **Nut/non-nut conflated.** A "50% flush block" could mean hero
   blocks half of villain's non-nut flush draws (weak signal) or
   half of villain's made nut flushes (strong signal).

`nut_made_block_pct` replaces both limitations:

```
nut_made_block_pct = (# villain NUT-MADE combos blocked by hero's holes)
                      / (# villain NUT-MADE combos in pre-action range)

Where NUT-MADE = top-category made hands on the current board texture:
  - Straight-flush / quads / full-house (always nut-class)
  - Nut flush (ace of flush suit in villain's range)
  - Nut straight (highest straight possible on board)
  - Top set (set of top-board-card)
```

Range: `[0.0, 1.0]`.

### Texture-dependent NUT definition

The "nut" bucket depends on board texture. On a 7h5d2c rainbow:
- Nut flush = impossible (needs 3+ same suit on board)
- Nut straight = 6x4x (hero needs 64 for open-ender to become nut on 3/8)
- Top set = 777 (if hero has 77)

On QsJsTs monotone spades:
- Nut flush = As-anything in spades
- Nut straight = AKxs (using hero AK)
- Top set = QQQ

The feature needs board-texture awareness. Implementation leverages
the existing `range_decomposition.py` subcategory taxonomy which
already classifies combos as `nut_flush`, `nut_straight`, `top_set`,
etc.

## Feature derivation

Pseudocode — builds on the existing range-decomposition infrastructure:

```python
def _nut_made_block_pct(hole_cards, range_breakdown):
    """Fraction of villain's NUT-MADE combos blocked by hero's holes."""
    if range_breakdown is None or range_breakdown.total_combos == 0:
        return 0.0

    _NUT_MADE_SUBCATS = {
        'straight_flush', 'quads', 'full_house',
        'nut_flush',        # Ace-of-suit flush
        'nut_straight',     # highest straight on current board
        'top_set',          # set of highest board card
    }

    hole_set = set(c.lower() for c in hole_cards)

    nut_combos = 0
    blocked_combos = 0
    for bucket in range_breakdown.buckets:
        if bucket.subcategory not in _NUT_MADE_SUBCATS:
            continue
        for combo in bucket.combos:
            nut_combos += 1
            if any(c.lower() in hole_set for c in combo):
                blocked_combos += 1

    if nut_combos == 0:
        return 0.0
    return blocked_combos / nut_combos
```

Output: `nut_made_block_pct`, float [0.0, 1.0], feature #58 (after
`nut_flush_block` at #56 and `draw_block_pct` at #57). Feature count
goes 55 → 58 raw; 110 → 116 total with attn mirror.

## Why this replaces `flush_block_pct` (post-validation)

`flush_block_pct` shortcomings addressed:

| Issue | `flush_block_pct` | `nut_made_block_pct` |
|---|---|---|
| Covers only flushes | Yes | No — covers full-house, quads, straight-flush, top set, nut straight, etc. |
| Conflates nut vs non-nut | Yes — single scalar | No — strictly nut-made class |
| Sensitive to hero's card rank | Partial (via `flush_draw_rank`) | Yes — the Ace-of-suit is counted into `nut_flush`; lower cards aren't |
| Aggressor-side signal (KB §1.7) | Present but diluted | Present and cleaner |

The existing `flush_block_pct` retires after this feature lands IF:

1. `nut_made_block_pct` subsumes its signal on worked examples
   (d2410, KB Example 9 "nut draw with blocker")
2. Model performance on calibration anchors + self-play does not
   regress when `flush_block_pct` is removed
3. GTO reviewer confirms the aggressor-side decision class is still
   covered

Retirement sequence (after this plan approves + feature lands):

1. Train v2.4 with `flush_block_pct` STILL PRESENT alongside all 3
   new features (116 raw cols)
2. Inspect XGBoost feature importance — if `flush_block_pct` is
   below some threshold (e.g., <1% of total gain) the feature is
   redundant
3. Train v2.4' with `flush_block_pct` REMOVED (115 raw cols, or 58 +
   57 attn = 115 total)
4. Run calibration anchors + self-play on v2.4 vs v2.4'
5. If v2.4' matches or beats v2.4 on gates, retire
   `flush_block_pct` from future feature vectors

All of this is gated on this plan approving, which this doc is
requesting.

## What this plan does NOT cover

- Retirement mechanics for `flush_block_pct` — requires its own
  ticket after `nut_made_block_pct` training validates
- Model training — gated on all 3 plans approved + v2.4 P1b Path C
  rescope
- Interaction effects between the 3 new features (to be evaluated
  empirically post-training)

## Interaction with plans 1 and 2 (for reviewer)

The three new blocker features form a **covering triple**:

| Feature | Class | Direction for hero |
|---|---|---|
| `nut_flush_block` | Flush-specific, boolean | Positive when aggressing (KB §1.7); slight positive when bluff-catching |
| `draw_block_pct` | Bluff-draw continuous | **Negative when defending** (densifies villain to value) |
| `nut_made_block_pct` | Made-nut continuous | **Positive when defending** (villain's value combos reduced → more bluff-catch equity) |

Together they give the model two independent signals on blocker
direction — what hero blocks from VILLAIN'S BLUFF RANGE
(`draw_block_pct`) vs what hero blocks from VILLAIN'S VALUE RANGE
(`nut_made_block_pct`). The model can learn:

- Defending decisions: lean toward CALL/CHECK when `nut_made_block_pct`
  is high (villain value blocked, bluffs relatively more common) and
  lean toward FOLD when `draw_block_pct` is high (villain bluffs
  blocked, value relatively more common).
- Aggressor decisions: `nut_flush_block` is the canonical raise-trigger
  for semi-bluffs; `nut_made_block_pct` adds broader value-range
  blocking for thin-value decisions.

## Validation plan (post-approval)

Same shape as plans 1 and 2:

1. Unit tests on synthetic situations with known nut-made combos
2. Backfill existing training CSV
3. Distribution audit — what's the mean? Highly skewed?
4. **No model training** yet

## Open questions for GTO reviewer

1. **What counts as "nut made"?** My definition includes:
   - straight_flush, quads, full_house (always)
   - nut_flush (A-of-suit)
   - nut_straight (highest possible straight on the board)
   - top_set (set of top board card)
   
   Should it also include:
   - Second nut flush (K-of-suit when A-of-suit not on board)?
   - Two-pair top-two (e.g., top + second pair)?
   
   Broader = more signal but more diluted. My instinct is "keep
   strictly nut-class only" so the feature is decision-critical,
   but want GTO opinion.

2. **Top-set on paired board.** On 8h8c3d, top-set is 888 (hero has
   88 for quads, actually — on paired board, "top set" isn't
   canonical). Edge case: what's `top_set` on paired boards?
   Proposal: `top_set` undefined on paired boards, only counts
   `quads`/`full_house` there.

3. **Nut-straight ambiguity on connected boards.** On JhTh9s,
   multiple straights are possible (KQ for broadway, Q8 for 8-Q).
   Is "nut straight" strictly the highest (KQ nut)? Or does "any
   high-made straight" count? Current plan: strictly highest = nut.

4. **Multiway nut dilution.** In 3-way pots, villain ranges are
   narrower and nut-combos rarer. Should `nut_made_block_pct` be
   weighted differently 3-way vs HU? Current plan: raw fraction,
   model learns the weighting via `num_opponents` interaction.
   Reasonable?

5. **Retirement criteria for `flush_block_pct`.** Section above
   proposes comparing v2.4 (with both features) vs v2.4' (without
   `flush_block_pct`). Is this the right test, or should retirement
   be gated on feature-importance thresholds alone (e.g., if
   `flush_block_pct` has <1% of total gain, drop it without running
   a second training pass)?

## What happens after GTO review approves all 3 plans

Order of operations (not yet — plans only at this stage):

1. All 3 features added to `feature_extractor.py` + `feature_keys.py`
2. Unit tests
3. Backfill existing training CSV (feature_count 55 → 58 raw)
4. Distribution audit + GTO review of training data's new columns
5. P0 calibration-anchor gate re-runs on v2.3.1 with new features
   present (sanity check: does adding 3 features without retraining
   regress the model? Should be zero effect since XGBoost
   inference uses only known features — new feature columns not
   read until retrain)
6. **Then** and only then: v2.4 retrain (alongside P1b Path C
   rescope + hand_evaluator draw_outs fix)
7. Calibration-anchor gate auto-runs at end of training (trailer
   wired once retrain proceeds)

## Not in scope

- Flush_block_pct retirement mechanics (post-feature-validation)
- v3.2 prompt update with blocker-feature guidance
- Model training

Ready for GTO reviewer subagent to validate this plan (last of 3).
