# Design Agent 3 — Delivery Confirmation

**Date:** 9 April 2026
**From:** Design Agent 3
**To:** Reviewer / Owner
**Re:** SP7 (25 RAISE) and SP10 (13 CALL) hero card assignments

---

## Delivery Confirmed

File written: `/home/rupertbeytell/river-rats-v2/review/DESIGN_AGENT_3_SP7_SP10.md`

38 situations fully specified: SP7_01 through SP7_25 and SP10_01 through SP10_13.

---

## What Was Produced

For each of the 38 situations:
- Situation ID
- Board ID (matching BOARD_ALLOCATION_V3_FINAL.md allocation table)
- hero_cards: exactly 2 cards, no conflict with board_cards
- hand_category with reasoning
- is_monster check with explicit confirmation it is 0
- Description of the hand and why the RAISE/CALL label applies
- All feature values from the allocation table (range_pct, fold_eq, aggr, flush_d, etc.)

---

## SP7 Verification Results

**Band distribution (min 6 per band required):**
- 0.75-0.80: 8 situations (sits 01, 02, 03, 04, 05, 06, 22, 23) — PASS
- 0.80-0.86: 8 situations (sits 07, 08, 09, 10, 11, 12, 13, 24) — PASS
- 0.86-0.92: 9 situations (sits 14, 15, 16, 17, 18, 19, 20, 21, 25) — PASS

**fold_equity range:** 0.40 (SP7_12) to 0.65 (SP7_14, 18, 25). Span = 0.25 (meets min 0.20).

**is_monster check:** All 25 SP7 situations use hand_category 7, 8, or 9 (top_pair_good_kicker, top_pair_top_kicker, overpair). None are sets, straights, flushes, full houses, or quads. All is_monster == 0. PASS.

**Card conflicts:** All 25 hero hands verified against their board's card list. No rank+suit duplicates. PASS.

---

## SP10 Verification Results

**Band distribution (min 3 per band required):**
- 0.40-0.55: 4 situations (sits 01, 02, 03, 06) — PASS
- 0.55-0.65: 3 situations (sits 04, 05, 08) — PASS
- 0.65-0.75: 3 situations (sits 07, 09, 12) — PASS
- 0.75-0.80: 3 situations (sits 10, 11, 13) — PASS

**IP thin value CALL count (is_ip==1 AND range_pct >= 0.75):**
- SP10_10: B03, CO IP, range_pct=0.75 — QUALIFIES
- SP10_11: B11r, BTN IP, range_pct=0.78 — QUALIFIES
- SP10_09: B28, CO IP, range_pct=0.72 — DOES NOT QUALIFY (0.03 below threshold)

Count confirmed at 2. Brief requires minimum 3. FLAG RAISED — see below.

**draw_outs range:** 0 (river hands, no outs) to 7. All within 0-8 specification.

**Card conflicts:** All 13 hero hands verified against their board's card list. No rank+suit duplicates. PASS.

---

## Open Flags (referred to reviewer)

**FLAG 1 (structural — requires board architect decision):**
The allocation table sets SP10 sit#9 (B28, CO IP) at range_pct=0.72, below the 0.75 threshold for the IP thin value CALL contrast requirement. Only 2 of the required 3 IP contrast situations are confirmed. Options: raise sit#9 to 0.76 (disrupts 0.65-0.75 band minimum), or add a dedicated 14th SP10 situation for IP contrast. This conflict originated in the board allocation, not in hero card design. Flagging for owner/reviewer decision before build.

**FLAG 2 (transparency):** SP7_22 uses B12 with flush_danger=0.35, exactly at the Step 4 ceiling. Feature extractor floating-point output should be verified to not produce 0.351+ on this board before building this situation.

---

## Hand Design Approach

SP7: All hands are hand_category 7 (top_pair_good_kicker), 8 (top_pair_top_kicker), or 9 (overpair). Two pair was deliberately avoided even though it is not technically is_monster per the tree definition. This keeps the training signal clean: the model should associate this sub-pattern with one-pair hands near the top of range, not two-pair hands which border on monster territory and carry different strategic implications.

SP10: Hands span bottom_pair (3) through top_pair_good_kicker (7), with draw_outs 0-7. The three highest-percentile SP10 hands (sits 10, 11, 13) are positioned to directly contrast with SP7: similar percentile range (0.75-0.78) but IP position (sits 10, 11) or draw_outs below threshold (sit 13 OOP but fails Step 5 at draw_outs=6 < 9).

---

Design Agent 3 task complete. Awaiting reviewer gate check.
