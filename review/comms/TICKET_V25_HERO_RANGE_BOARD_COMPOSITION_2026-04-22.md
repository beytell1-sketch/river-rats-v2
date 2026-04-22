---
date: 2026-04-22
from: Main terminal (orchestrator)
to: Builder (future v2.5 work) · Teaching · Owner
re: v2.5 queue — hero range-board composition features (subset of v2.6+ hero-range-tracking)
status: QUEUED for v2.5; minimal subset of TICKET_V26_HERO_RANGE_TRACKING
triggered_by: Owner playtest finding 2026-04-22
---

# v2.5 Queued — Hero Range-Board Composition Features

## Trigger

Owner playtest finding 2026-04-22: the current teaching wording "where
our hand sits among all hands we'd play this way" — backed by
`hero_range_percentile` (Feature 49) — is not accurate or useful.

What owner wants to see instead:
1. Hero's **range** and how it connects to the board (range composition)
2. Hero's **hand** and how it connects to the board (hand classification)
3. Where the hand sits **within the range's composition** (position in
   distribution, not 1D rank)

## What exists today

`feature_extractor.py:1541-1579` — `compute_hero_range_percentile`:
- Single 0.0-1.0 scalar via `_range_manager.get_hand_percentile(hand, hero_range, board)`
- 1D rank of hero's hand within hero's preflop-conditional range on board
- Does NOT decompose the range by category (TP+/medium/draws/air)
- Does NOT report where hand sits category-wise within range

Hero-side fields present:
- `hero_range_percentile` — 1D rank
- `board_adjusted_hrp` — held-back; `hero_range_percentile × equity_vs_range`
- `hand_category`, `is_made_hand`, `is_strong_made`, `has_flush_draw`,
  `has_straight_draw`, etc. — hand-vs-board fields (not range-vs-board)

## What's missing (this ticket)

Symmetric to villain-side composition features. Hero needs equivalents of:
- `villain_tp_pct` → `hero_tp_pct`
- `villain_medium_made_pct` → `hero_medium_made_pct`
- `villain_draw_pct` → `hero_draw_pct`
- `villain_air_pct` → `hero_air_pct`

Plus optionally:
- `hero_board_favour` (parallel to `board_favour` for villain, if useful)
- `hero_range_capped` (parallel to `villain_range_capped`)
- `hero_hand_category_in_range_pct` — where hero's hand's category
  ranks within the range's distribution (e.g., "hero's TP is in the
  top 40% of hero's TP+ slice")

## v2.5 scope — MINIMAL (subset of v2.6+)

This ticket is a **subset** of
`TICKET_V26_HERO_RANGE_TRACKING_2026-04-21.md`. Key scoping choice:

**v2.5 (this ticket):** Hero range-board composition from
**preflop-conditional range only**. No postflop-action chain
narrowing. Hero's range is whatever `get_postflop_range(hero_pos,
is_pfr=is_pfr)` returns today; we classify each hand in it against
the board and return composition percentages.

**v2.6+ (TICKET_V26):** Full hero postflop range tracking with
`narrow_hero_by_action_history` symmetric to villain chain. Hero's
range updates as hero acts (check-call caps range, check-raise
polarises, etc.).

The v2.5 subset is cheaper (no chain work needed) and unblocks
teaching's structured range-composition rendering. v2.6+ refines
it later with action-aware narrowing.

## Feature extraction sketch

```python
# New helper in feature_extractor.py alongside compute_hero_range_percentile
def compute_hero_range_composition(
    hero_pos: str,
    opener_pos: Optional[str],
    board_cards: List[str],
) -> Dict[str, float]:
    """v2.5 — decompose hero's preflop-conditional range on current board.

    Symmetric to extract_range_composition's villain-side work; no
    action-history chain (that's v2.6+).

    Returns:
      {
        'hero_tp_pct': float,
        'hero_medium_made_pct': float,
        'hero_draw_pct': float,
        'hero_air_pct': float,
      }
    """
    is_pfr = (opener_pos is None or opener_pos.upper() == hero_pos.upper())
    hero_range = _range_manager.get_postflop_range(hero_pos, is_pfr=is_pfr)
    if not hero_range:
        return {...zeros...}

    # Same loop as extract_range_composition villain-side:
    total = 0.0
    tp = medium = draw = air = 0.0
    for hand, freq in hero_range.items():
        if freq <= 0:
            continue
        cls = classify_hand(hand, board_cards)
        total += freq
        if cls.category in _TOP_PAIR_PLUS:
            tp += freq
        elif cls.category in _MEDIUM_MADE:
            medium += freq
        elif cls.category == 'draw':
            draw += freq
        elif cls.category in ('air', 'bluff'):
            air += freq
    if total > 0:
        tp /= total; medium /= total; draw /= total; air /= total
    return {
        'hero_tp_pct': round(tp, 4),
        'hero_medium_made_pct': round(medium, 4),
        'hero_draw_pct': round(draw, 4),
        'hero_air_pct': round(air, 4),
    }
```

Plus optional hand-in-range placement:

```python
def compute_hero_hand_in_range_category_rank(
    hero_cards: List[str], board_cards: List[str],
    hero_pos: str, opener_pos: Optional[str],
) -> float:
    """Where hero's hand sits *within its own category* on this board.

    e.g., if hero's TP is 'top pair good kicker' and the TP+ slice of
    hero's range includes sets + two-pair + TPTK/TPGK/TP-weak, return
    the rank of hero's specific hand within that slice (0.0-1.0).
    """
    # Classify hero's hand; filter range to same category; rank within.
    ...
```

## Teaching integration

Once v2.5 ships, teaching renders structured composition instead of
1D rank:

**Before (today's wording owner flagged):**
> "Where your hand sits among all hands we'd play this way."

**After (v2.5-enabled wording):**
> "Your range here is ~30% top-pair-plus, ~20% medium-made, ~30% draws,
> ~20% air. Your hand (top pair, Kx on K84r) sits in the top-pair-plus
> slice."

CONTENT_API bump accompanies the logic ship. Suggested v4.2 (after
v4.1 NaN-render currently in flight).

## Immediate non-blocking fix for teaching

Regardless of this ticket's timing, teaching should replace the
current "where your hand sits among all hands we'd play this way"
wording. The current scalar is `hero_range_percentile` — a rank within
range on board. More honest wording until v2.5 ships:

> "Relative rank of your hand within your opening range on this board
> (0-100%)."

Or drop the field from display until v2.5 fills in the structured
composition. Teaching owns the decision; add to v4.1 plan if capacity.

## Scope vs v2.6+

| Concern | v2.5 (this ticket) | v2.6+ (TICKET_V26) |
|---|---|---|
| Hero range source | Preflop-conditional (static) | Postflop-action-narrowed (chain) |
| Composition features | ✅ 4 pct fields | ✅ same 4 + chain-updated |
| Hand-in-range rank | ✅ category-aware | ✅ chain-aware |
| Teaching rendering | Structured range composition | Same + "your range is capped/polarised" |
| Game rendering | Optional hero range bar | Hero range bar tracks through hand |
| Cost | Moderate — mirror villain composition loop | High — new chain subsystem + solver-grounded freqs |

## Action

- Add to manifest `queued.v2_5_candidates` as `hero_range_board_composition`
- Reference this ticket + TICKET_V26 in the v2.5 entry
- Teaching includes the wording cleanup in their v4.1 plan (immediate)
- Logic picks up the feature work when v2.4 ships (after Stage 6)

## Reference

- `feature_extractor.py:1541-1579` — current `compute_hero_range_percentile`
- `feature_extractor.py:extract_range_composition` villain-side pattern
  to mirror
- `TICKET_V26_HERO_RANGE_TRACKING_2026-04-21.md` — superset ticket
- Owner playtest finding 2026-04-22 — trigger
