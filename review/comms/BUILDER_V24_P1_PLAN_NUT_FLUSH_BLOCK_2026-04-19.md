---
date: 2026-04-19
from: Builder
to: Main terminal / Owner (+ GTO reviewer subagent for feature validation)
re: v2.4 P1 — new feature PLAN — `nut_flush_block` (Boolean)
status: PLAN — awaiting GTO-reviewer subagent validation before any code
related: directive-x (2026-04-19), TICKET_BLOCKER_DIRECTION_DEFENSIVE_2026-04-18.md
---

# P1 Plan — `nut_flush_block` (Feature 1 of 3)

## Sequence context

Per directive-x, three new blocker features to be designed in order:

1. **`nut_flush_block`** ← this plan (flush-specific, boolean, simplest)
2. `draw_block_pct` (broader bluff-draw blocking, continuous)
3. `nut_made_block_pct` (retirement-gate for `flush_block_pct`)

Each plan is expert-reviewed by a GTO reviewer subagent BEFORE any code
is written. No training fires until all three plans are approved.

## Intent of `nut_flush_block`

Surface the **single most actionable blocker signal in poker**:
does hero hold the specific card that blocks villain's nut-flush
combos on a flush-possible board?

Two reasons this is worth a dedicated boolean feature vs relying on
`flush_block_pct`:

1. **Asymmetric decision weight.** Holding the nut-flush blocker is
   qualitatively different from holding any flush blocker. It's the
   one feature the v3.1 KB explicitly validates for action selection
   (KB §1.7: "The As blocker is critical. It removes AsXs combos from
   villain's nut flush range" — Worked Example 9). The decision
   between raise, call, and fold often hinges on this single bit.
2. **Categorical vs continuous.** `flush_block_pct` is continuous
   (0-1) and conflates nut vs non-nut block into one scalar. The
   model has to re-derive "was it the ace?" from other features.
   Exposing it as a boolean lets tree splits find the pattern with
   minimal depth.

## Exact definition

```
nut_flush_block == 1 IF AND ONLY IF:
  (a) Board has a flush-possible suit (3+ cards of one suit on turn/river,
      2+ cards of one suit on flop + at least one card that could still
      complete by river — i.e., "nut-flush matters this street")
  (b) Hero holds the Ace of the flush-possible suit in hole cards
  (c) The flush is not already a made hand on board (no 4-flush on
      turn/river where the ace card would only decide tie-breaks)

Otherwise nut_flush_block == 0.
```

### Edge cases

- **Paired flush boards** (e.g., AhKh on hero + board 7h7h3d): trips
  on board, flush is possible only on one remaining street. Still
  counts — hero's hypothetical Ah would be the nut-flush blocker.
  Note: above is a malformed example (can't have two Ah) — correct
  case would be hero with two cards, one being the Ah on any board
  with 2+ same-suit and at least one street remaining.
- **Monotone flop + hero no-suit** (e.g., hero Kc2d on QsJs6s): hero
  does NOT hold the Ace of spades → `nut_flush_block = 0`. The
  feature is only about hero holding the nut specifically.
- **Made flush** (e.g., hero has As3s on Qs7s2s): hero HAS the nut
  flush already; this isn't "blocking" — it's making. Feature
  returns 0; the `is_made_hand` signal carries the strength here.
- **Two remaining cards** (flop with 2 of a suit): the nut flush
  matters only if board completes to 3+ same suit on turn/river.
  Conservative implementation: count `nut_flush_block = 1` at flop
  if board has 2+ of a suit and hero holds A-of-that-suit. The
  model learns the runner-runner dilution via other features.

### What this feature does NOT do

- Does not distinguish hero's action context (aggressor vs defender) —
  that's the model's job to interact with `facing_bet`, `is_ip`, etc.
- Does not try to capture non-nut blockers (K-flush blocker, Q-flush
  blocker). Those are weaker and less decision-critical; `draw_block_pct`
  (feature 2) captures the broader draw-blocking signal.
- Does not encode "which street" — stays a simple boolean, the model
  reads `street` separately.

## Feature derivation

`feature_extractor.py` in both repos. Logic:

```python
def _nut_flush_block(hole_cards, board):
    """Return 1 if hero holds A of a flush-possible suit on board."""
    if not board or len(hole_cards) != 2:
        return 0

    # Count suit frequencies on board
    board_suits = [c[1].lower() for c in board]
    from collections import Counter
    suit_counts = Counter(board_suits)

    # Flush-possible suit: board has 2+ of it (3+ makes flush currently
    # possible on the street; 2+ can become 3+ on future streets)
    flush_suits = {s for s, n in suit_counts.items() if n >= 2}

    if not flush_suits:
        return 0

    hero_suits = {c[1].lower() for c in hole_cards}
    hero_ranks_by_suit = {
        c[1].lower(): c[0].upper() for c in hole_cards
    }

    for fs in flush_suits:
        if fs in hero_ranks_by_suit and hero_ranks_by_suit[fs] == 'A':
            return 1
    return 0
```

Output: `nut_flush_block` column, int 0/1, added to FEATURE_COLUMNS
as feature #56 (v2.4 raw count 56, total count 112 with attn mirror).

## Why this doesn't duplicate existing features

- `flush_block_pct`: continuous, conflates nut/non-nut. Scalar signal.
  Future retirement per directive-x — not removed until
  `nut_made_block_pct` validates as a replacement.
- `flush_draw_rank`: hero's highest card in a hero-held flush suit
  (14=A, 0=none). Activates only when hero has a flush draw. Doesn't
  cover the "hero blocks but has no draw" case.
- `has_flush_draw`: boolean about hero's own draw. Different axis.

New feature is orthogonal — it's about the blocker effect when hero
might NOT have any flush involvement otherwise.

## Expected model behavior

The tree model should be able to learn:
- When `nut_flush_block = 1` AND hero is aggressing (BET/RAISE) on a
  flush-possible board → boost value of aggression (KB §1.7)
- When `nut_flush_block = 1` AND hero is defending (facing_bet, CALL/
  FOLD decision) → slight positive (villain's nut-flush combos
  removed from their betting range means hero's bluff-catchers have
  more fold equity in play; "nut blocker = villain is bluffier when
  betting")

The current feature set cannot represent the second case cleanly —
that's the gap the defensive-blocker ticket was tracking.

## Validation plan (post-approval)

1. Unit test: assert `_nut_flush_block` returns 1 on clear cases
   (hero As + 2-spade+ board), 0 on negatives (no ace of suit, no
   2+ board suit, hero already has flush).
2. Backfill existing training CSV (compute `nut_flush_block` from
   `hero_cards` + `board_cards` without re-running
   `build_features_from_game_state`).
3. Distribution audit: how many training rows have
   `nut_flush_block = 1`? If < 5% of total, the feature is rare and
   may have limited training signal — decide whether to proceed or
   augment.
4. **No model training** — plan only. Training is gated on all 3
   plans approved + P1b rescope.

## Open questions for GTO reviewer

1. **Is the "2+ on flop, becomes 3+ later" framing the right
   coverage?** Or should the feature ONLY activate when the flush is
   currently possible (3+ same suit on current board)? Argument for
   conservative (3+ only): the feature's poker meaning is strongest
   when the flush is on-the-board-now. Argument for broader (2+):
   some playtest-level decisions (bet sizing on flop two-tone with
   ace of the suit) would benefit from the signal.

2. **Should there be a companion `near_nut_flush_block` for K-of-suit?**
   Holding the Kc on a three-club board where Ac is live is ALMOST as
   strong a blocker. Current plan treats it as "covered by
   `draw_block_pct`." Is that acceptable, or does K-blocker deserve
   its own bit?

3. **What's the right handling of hero's own flush?** If hero has the
   nut flush already (e.g., As5s on 2s7sQs), is feature = 0 correct?
   Or should it signal "hero has the nut + blocks all competing flush
   draws"? KB §1.7's "blocker + nut draw raise" case is subtly
   different from "hero has made flush."

4. **Paired-board edge case.** On 7h7d5h, hero Ah4c: `nut_flush_block`
   would be 1 per my definition (board 2+ hearts). But villain's
   range on a paired board is less flush-heavy (more trips-focused).
   Is the signal still meaningful, or should the feature be gated on
   `is_paired == 0`?

## What happens after GTO review approves

1. Add `_nut_flush_block` to `feature_extractor.py` (+ mirror
   `feature_keys.py`)
2. Unit tests
3. Backfill existing CSV + verify distribution
4. WAIT for plans 2 and 3 to also approve before model training
5. Eventually: retrain with all 3 new features + P1b Path C rescope;
   calibration-anchor gate runs automatically

## What this plan does NOT cover

- Plan doc for `draw_block_pct` — separate plan, separate GTO review
- Plan doc for `nut_made_block_pct` — separate plan
- Retirement of `flush_block_pct` — deferred until
  `nut_made_block_pct` validates
- Any model training

Ready for GTO reviewer subagent to validate.
