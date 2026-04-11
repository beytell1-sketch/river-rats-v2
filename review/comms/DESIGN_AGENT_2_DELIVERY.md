# Design Agent 2 — Delivery Confirmation

**Date:** 9 April 2026
**From:** Design Agent 2
**To:** Reviewer / Owner
**Re:** SP1-SP4 hero card assignments

---

## Delivery status: COMPLETE

Design document written to:
`river-rats-v2/review/DESIGN_AGENT_2_SP1_SP2_SP3_SP4.md`

46 situations assigned across SP1 (18 RAISE), SP2 (10 RAISE),
SP3 (12 RAISE), SP4 (6 CALL).

All 46 hero card pairs verified clear of board cards.

---

## Summary counts

| Sub-pattern | Count | Label | Boards used |
|-------------|-------|-------|-------------|
| SP1 | 18 | RAISE | B05, B11r, B02, B08, B12, B22, B16, B20, B01 (9 boards) |
| SP2 | 10 | RAISE | B10, B17, B30, B31, B20 (5 boards) |
| SP3 | 12 | RAISE | B02, B06, B08, B12, B13, B15, B17, B21 (8 boards) |
| SP4 | 6  | CALL  | B33, B12, B26, B09, B20 (5 boards) |

---

## Verification gate results

SP1: flush_danger span 0.40-0.90 (exceeds required 0.40-0.75). SPR span
1.4-6.0. hand_category: 10 sets, 8 two_pair. 9 unique boards. PASS with
one flag: no board sits in the 2.0-2.5 SPR band (allocation-level decision,
not a card assignment error).

SP2: hero_range_percentile span 0.90-0.98. SPR span 1.0-1.5. flush_danger=0
on all boards. 5 unique boards, 2 flop, 3 turn. PASS.

SP3: SPR span 2.6-8.4. hero_range_percentile span 0.90-0.99. Texture: 2
rainbow boards (3 sits), 3 two-tone boards (4 sits), 3 paired boards (5
sits). All OOP. 8 unique boards. PASS with one flag: SP3_10 uses B17
where to_call=0 (hero leads, not check-raises) — allocation-level decision.

SP4: All 4 suppressors present — S2 (sits 01-02, B33), S3 (sits 03-04,
B12/B26), S4 (sit 05, B09 SPR=8.0), S5 (sit 06, B20). 5 unique boards.
S4 situation uses SPR=8.0 (>= 6.0 requirement met). PASS.

---

## Flags requiring reviewer decision

1. SP1 sits 01-03: S4 boundary at exactly SPR=6.0 on B05 (IP). Tree
   rationale suggests strictly greater than 6.0; formal threshold writes
   ">=". Expert labeller should confirm.

2. SP3 sit 10: B17 has to_call=0. Hero leads rather than check-raises.
   Allocation assigns B17 here explicitly. Design interprets as OOP
   monster lead (Step 2 still fires). Confirm acceptable.

3. SP1 and SP4 share hero cards Qc Qd on board B20 (SP1_15 and SP4_06).
   These are different sub-patterns — no intra-sub-pattern duplicate rule
   violated. Flagged for awareness.
