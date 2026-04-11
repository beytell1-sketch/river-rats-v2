---
date: 2026-04-09
from: Builder
re: flush_block_pct structural finding — SP6 failure mode 6 impossible
---

## Finding

flush_block_pct > 0 whenever hero holds ANY card in the flush suit.
flush_draw_rank >= 12 requires hero to hold a Q/K/A in the flush suit.

Therefore: flush_draw_rank >= 12 IMPLIES flush_block_pct > 0.

The AND gate in Step 5 (flush_draw_rank >= 12 AND flush_block_pct > 0)
is structurally redundant — the second condition is always satisfied
when the first is.

## Consequence for SP6

Failure mode 6 ("nut draw without blocker") cannot be constructed.
You cannot have flush_draw_rank >= 12 and flush_block_pct == 0
simultaneously — the feature extractor will always return positive
flush_block_pct when hero holds a card in the flush suit.

## Consequence for the decision tree

The AND gate still works correctly as a filter — it just does all
its filtering through flush_draw_rank alone. flush_block_pct > 0
adds no discriminative power when flush_draw_rank >= 12.

The poker concept the tree was trying to capture ("nut draw AND
blocker") is valid, but the feature implementation makes them
inseparable. A hero with Ac on a clubs board has BOTH a nut draw
AND a blocker — you can't have one without the other.

This does NOT require a tree change — the gate is correct, just
partially redundant. It should be noted in the tree for clarity.

## Fix for SP6

SP6_12 and SP6_13 (originally failure mode 6) reassigned:
- SP6_12 → additional fold_equity < 0.45 example (mode 1)
- SP6_13 → already works as mode 5 (flush_draw_rank = 0, no flush suit cards)

Mode 6 removed from SP6 requirements. Five failure modes remain,
all constructable. The brief's Item 9 ("nut-draw-without-blocker CALL")
is acknowledged as structurally impossible and documented.

## For owner awareness

This finding affects the tree's documentation, not its correctness.
The tree labels correctly — no situation will ever be mislabelled
because the AND gate is sound, just redundant on one condition.
