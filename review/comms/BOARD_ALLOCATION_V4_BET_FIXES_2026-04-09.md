# Board Allocation V4 BET — Round 2 Fixes Confirmed

**Date:** 9 April 2026
**From:** Board Architect
**To:** Owner / Reviewer
**Re:** BOARD_ALLOCATION_V4_BET.md — all 5 reviewer issues resolved

---

## Status

All 5 issues from REVIEW_BOARD_ALLOCATION_V4.md have been applied to
`review/BOARD_ALLOCATION_V4_BET.md`. File is overwritten in place.
The document is now REVISED v2.

---

## What Changed

### Issue 1 — CRITICAL: B4_03 removed from BP1

CO in a CO/BTN/BB pot acts second postflop (between BB and BTN), not last.
CO is OOP relative to BTN. The IP claim was wrong.

- B4_03 removed from BP1 entirely.
- Its 2 BP1 situations (former sits 7-8) reassigned to B4_01 (BTN opener — genuinely IP last to act).
- B4_01 now carries 5 BP1 situations instead of 3.
- BP1 total unchanged at 30.
- B4_03 retained in BP2 only (OOP PFA — correct usage confirmed).
- B4_03 board definition corrected: is_ip=0, sub-patterns note updated.

### Issue 2 — MODERATE: B4_22 now BP5-only; B4_25 added for BP6-G

B4_22 appeared in both BP5 and BP6-G, violating the brief's R1 board isolation requirement.

- New board B4_25 (`6h 2c 4s`) added as dedicated BP6-G board.
- Cards verified CLEAR of all 82 prior boards and all B4_01–B4_24 boards.
- B4_22 sub-patterns updated to BP5 only.
- BP6-G sit 8 updated to use B4_25.
- B4_25 added to Section 1 board definitions, Section 2 summary table, Section 5 conflict table, Section 6 conflict resolution summary, and Section 7 final inventory.
- Board total: 24 → 25.

### Issue 3 — MODERATE: Total documented as 104

The 104 total is retained (brief said 100; 4 extra fill structural gaps).
Header updated from "100 Situations" to "104 Situations".
Section 8 (new) added with explicit situation count table showing 104 total.
Round 2 corrections block at top documents the per-sub-pattern counts.

### Issue 4 — MODERATE: BP2 sits 13-15 moved to BP6-H

BP2 sits 13-15 used B4_13 turn with villain_air_pct=0.38, failing the Step 3B gate of 0.40.
The old self-declared PASS was incorrect.

- Sits 13-15 removed from BP2 table.
- BP2: 15 → 12. BP2 now uses B4_02, B4_03, B4_04 only (all flop, all villain_air_pct >= 0.40).
- The 3 sits added to BP6 as BP6-H near-miss CHECK counterexamples (sits 11-13 in updated BP6 table).
- BP6-H mode description added: villain_air near-miss — hand strength and position pass but air fraction fails the gate.
- B4_13 updated in Section 7: sub-patterns now include BP6-H.

### Issue 5 — MODERATE: BP3 4D sits 21-22 moved to BP6-H

BP3 4D sits 21-22 used B4_16 turn with villain_air_pct=0.29, failing the Step 4D gate of 0.40.

- Sits 21-22 removed from BP3 4D table.
- BP3 4D: 5 situations → 3 situations (flop-only).
- BP3 total: 22 → 20.
- The 2 sits added to BP6 as BP6-H near-miss CHECK counterexamples (sits 14-15 in updated BP6 table).
- BP3 footer updated with flag: turn count now 4 (was 6). Factory agent may add 2 BP3 turn sits on B4_14 to recover the 6-turn minimum, or accept 4 with documentation.
- B4_16 updated in Section 7: sub-patterns now include BP6-H.

---

## Final Counts

| Sub-pattern | Before | After |
|-------------|--------|-------|
| BP1 | 30 | 30 |
| BP2 | 15 | 12 |
| BP3 | 22 | 20 |
| BP4 | 15 | 15 |
| BP5 | 12 | 12 |
| BP6 | 10 | 15 |
| **Total** | **104** | **104** |

Boards: 24 → 25 (B4_25 added).

---

## Open Item Flagged for Owner Attention

BP3 turn count is now 4 (down from 6 after removes). The brief minimum is 6 turns for BP3.
Options:
1. Factory agent adds 2 more BP3 turn situations on B4_14 (4B or 4C sub-conditions, villain_air >= 0.40).
2. Accept 4 BP3 turn situations with documented exception.

No decision required before file is ready for factory generation — the flag is documented in the BP3 section footer.

---

## No Open Items Remain from Reviewer

All 5 reviewer issues are resolved. File is ready for owner review and factory situation generation.
