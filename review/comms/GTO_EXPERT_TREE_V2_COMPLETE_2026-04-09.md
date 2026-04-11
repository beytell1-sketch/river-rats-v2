# GTO Expert: RAISE Decision Tree v2 — Delivery Confirmation

**Agent:** GTO Expert
**Date:** 9 April 2026
**Status:** DELIVERED — awaiting review + owner approval

---

## What was produced

File: `review/RAISE_DECISION_TREE_V2.md`

Fixed decision tree addressing all 14 findings from the independent
review (12 items) and process review (2 items).

---

## Summary of structural changes

**Step 1D removed.** Sandwich detection had no feature mapping —
no feature in the 52-vector encodes whether players behind hero have
acted. Removed with explanation. Sandwich hands default correctly to
CALL via the Default rule.

**S1 fixed.** "hand is not two-pair+" replaced with
`hand_category < 10`. Value 10 = two_pair in HAND_CATEGORY_ENCODING
(confirmed in feature_extractor.py line 150).

**S4 threshold raised.** `spr >= 4.0` → `spr >= 6.0` for IP monster
suppression.

**Step 3 threshold raised.** `hero_range_percentile >= 0.80` →
`>= 0.90` for low-SPR commit.

**Step 4 threshold raised.** `villain_fold_equity_estimate >= 0.30`
→ `>= 0.40` for OOP check-raise.

**Step 5 nut-draw gate added.** Added `flush_draw_rank >= 12` AND
`flush_block_pct > 0`. Used AND (not OR) because KB Section 1.7
(solver-verified) requires both nut draw and blocker. Rationale
documented in tree changelog and in the Step 5 body.

**Step 6 street gate added.** Added `street >= 2` (river only).
Street encoding confirmed in feature_extractor.py: f=0, t=1, r=2.

---

## Items NOT changed in tree (factory brief scope)

- Finding 8: CALL count inconsistency (32 vs 43) — factory brief
- Finding 9: SP6 missing counterexample — factory brief
- Finding 10: Mid-draw zone CALL examples — factory brief
- Finding 13: SP5 must match fixed tree — factory brief
- Finding 14: Self-play RAISE yield verification — separate agent

All four factory brief items are documented in the Factory Brief
Impact section at the bottom of the v2 tree.

---

## Verification steps taken

- Confirmed HAND_CATEGORY_ENCODING in feature_extractor.py line 139:
  two_pair = 10, confirming `hand_category < 10` as the correct
  threshold for S1.
- Confirmed STREET_ENCODING in feature_extractor.py line 47:
  f=0, t=1, r=2, confirming `street >= 2` as the river-only gate.
- Confirmed flush_draw_rank and flush_block_pct are live features
  in feature_keys.py (lines 76-77), added in Step 13.
- Confirmed no `sandwich`, `num_players_to_act`, or `players_behind`
  feature exists anywhere in feature_keys.py or feature_extractor.py.
- Cross-checked all threshold changes against review recommendations.
- KB Section 1.7 and Worked Example 9 re-read to confirm AND logic
  for Step 5 gate.

---

## Open questions for owner

1. **Step 5 AND vs OR:** The review finding offered OR as an option.
   The tree uses AND based on KB Section 1.7. If owner wants OR,
   the tree can be revised — but this would admit nut draws without
   blockers as RAISE, which contradicts the KB and the MW-47 finding.

2. **Step 1D gap:** Sandwich position situations where hero faces a
   bet and the player behind has not acted will default to CALL. This
   is conservative. If a proxy feature can be identified (e.g.,
   num_opponents combined with specific position encoding), a new
   step could be added in v3. No such proxy was identifiable in the
   current 52-feature vector.
