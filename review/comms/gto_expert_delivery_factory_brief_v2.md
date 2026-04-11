# Delivery Note — Factory Design Brief v2

**From:** GTO Expert
**Date:** 9 April 2026
**Re:** FACTORY_DESIGN_RAISE_CONTEXTS_V2.md

## Delivered

File: river-rats-v2/review/FACTORY_DESIGN_RAISE_CONTEXTS_V2.md

## What was changed

All four items from the Factory Brief Impact section of
RAISE_DECISION_TREE_V2.md have been addressed, plus the SP7 threshold
correction.

**Item 13 (SP5 gate):** SP5 now requires flush_draw_rank >= 12 AND
flush_block_pct > 0. RAISE count reduced from 20 to 16. Four displaced
situations moved to SP6 as CALL counterexamples.

**Item 9 (SP6 nut-draw-no-blocker CALL):** One explicit CALL example
added to SP6: nut draw (flush_draw_rank >= 12) with flush_block_pct == 0,
all other SP5 conditions met.

**Item 10 (mid-draw zone CALL):** Five CALL examples added to SP10 for
hero_range_percentile 0.70–0.80 with draw_outs 6–8. These fail both
Step 3 and Step 5 and are unambiguous CALL.

**Item 8 (CALL count reconciliation):** Correct total is 42 CALL
counterexamples (SP4: 6, SP6: 13, SP9: 10, SP10: 13). The v1 summary
line of 43 and totals table of 32 are both superseded. 42 is the
derived count.

**SP7 fold_equity threshold:** Updated from >= 0.30 to >= 0.40 per v2
Step 4. Description warns explicitly against using the old threshold.

**Additional alignment notes added:** SP2 percentile threshold (now
0.90), SP4 spr threshold (now 6.0), SP8 street gate (river only),
hand_category encoding note (>= 10 for two_pair+). None of these
changed situation counts but all affect what situations are valid.

## Totals after changes

- RAISE: 79 (down 4 from v1's 83 due to SP5 tightening)
- CALL: 42 (up 10 from v1's 32 due to Items 9, 10, 13)
- Total new: 121

## No structural changes

The 10 sub-pattern structure is preserved. SP10 absorbs the mid-draw
CALL additions without becoming a new pattern.

## Ready for owner review
