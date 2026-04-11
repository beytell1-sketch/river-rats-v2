# Review: RAISE Decision Tree v1

**Reviewer:** Independent agent
**Date:** 9 April 2026
**Verdict:** ISSUES FOUND — 12 items, 1 critical

## Critical Issue

**Step 5 (semi-bluff) has no blocker or nut-draw quality condition.**
Any draw with 9+ outs and fold equity >= 0.45 gets RAISE — including
8s7s on a spade board (non-nut, no blocker), which KB Section 1.7
explicitly says should CALL. This is the documented root cause of MW-20.

Fix: Add `flush_draw_rank >= 12` (nut/near-nut) as a condition in
Step 5, OR add `flush_block_pct > 0` as a gate.

## Other Issues (see full review for details)

- S1 uses undefined "two-pair+" — replace with hand_category threshold
- S4 SPR >= 4.0 is too low for IP monster suppression — raise to 6.0
- Step 3 hero_range_percentile >= 0.80 too loose at low SPR 3-way — raise to 0.90
- Step 4 fold_equity >= 0.30 too permissive for OOP check-raise — raise to 0.40
- Step 6 fires on flop despite being designed for river — add street gate
- Sandwich detection needs explicit feature mapping
- Factory brief CALL count inconsistency (32 vs 43)
- SP6 missing "nut draw without blocker" CALL counterexample
- Mid-draw zone (percentile 0.70-0.80, draw_outs 6-8) needs CALL examples
