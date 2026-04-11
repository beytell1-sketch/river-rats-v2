# Gate Check — Batch 4 Board Allocation (BOARD_ALLOCATION_V4_BET.md)

**Reviewer:** Independent Reviewer
**Date:** 9 April 2026
**File reviewed:** river-rats-v2/review/BOARD_ALLOCATION_V4_BET.md (Revised v2)

---

## Verdict: FAIL

One action history error found in spot-check. All 5 prior-review fixes verified. All other checks pass.

---

## Check Results

### Prior-Review Fixes (Checks 1-5)

**Check 1 — B4_03 no longer assigned to BP1; marked OOP only?**
PASS. Board definition sets is_ip=0 with explicit note "R2-1 correction: removed from BP1 IP usage." Sub-patterns field reads "BP2 only." BP1 section header confirms removal. Section 7 final inventory confirms "BP2 only (R2-1: removed from BP1)." Summary table shows OOP and BP2 only.

**Check 2 — B4_25 added for BP6-G; B4_22 only serves BP5?**
PASS. B4_25 (6h 2c 4s) is fully defined as "BP6-G only." B4_22 sub-patterns field reads "BP5 only (R2-2 correction: BP6-G moved to dedicated B4_25...)." BP6 situation table sit 8 correctly uses B4_25. BP5 section explicitly lists B4_22 as BP5-only.

**Check 3 — Total updated to 104?**
PASS. Section 8 final summary table shows Total = 104. Revised counts table after Round 2 also shows 104. Header line confirms "104 Situations."

**Check 4 — BP2 reduced to 12?**
PASS. Corrections table records 15→12. Revised counts confirm "BP2: 12 (was 15)." BP2 section header reads "12 situations." Section 8 summary table shows BP2 = 12. BP2 situation table contains exactly 12 rows with note that sits 13-15 were removed.

**Check 5 — BP3 reduced to 20?**
PASS. Corrections table records 22→20. Revised counts confirm "BP3: 20 (was 22)." BP3 section header reads "20 situations — updated count." BP3 sub-count arithmetic: 8+6+3+3=20 confirmed. Section 8 summary table shows BP3 = 20.

---

### Additional Checks (Checks 6-10)

**Check 6 — All boards have to_call = 0?**
PASS. Section 1 header declares "All boards: to_call = 0." Every board definition verified individually including B4_20 (river, pot=270, to_call=0) and B4_17 (turn, with inline note confirming to_call=0 at decision point).

**Check 7 — No Section 8 (open items)?**
PASS. The original Section 8 (Open Items) has been removed per the corrections header: "Section 8 (Open Items) has been removed; all flags are cleared." What is now labeled Section 8 is the final Situation Count Summary table — a renamed section with no open items list.

**Check 8 — BP6 board isolation complete?**
PASS with note. BP6-A through BP6-G all use dedicated boards (B4_18, B4_19, B4_20, B4_21, B4_25) that are exclusive to BP6. BP6-H (a new sub-category added in Round 2) uses shared boards B4_13 and B4_16 — this is acknowledged explicitly in the document with structural justification (different hero_pos, different is_ip values, different failed conditions from the BP1/BP4 usage of those same boards). The document's own isolation status section marks this RESOLVED. Note for factory agent: BP6-H rows on B4_13 and B4_16 must carry distinct hero_pos and is_preflop_aggressor values from the BP1/BP4 rows on those boards.

**Check 9 — Card conflicts checked for B4_25?**
PASS. Section 5 conflict table includes a dedicated B4_25 row checking all three two-card combinations (6h+2c, 6h+4s, 2c+4s) against all prior boards and explicitly against B4_22. All clear. Section 6 summary confirms "Cards 6h 2c 4s verified CLEAR of all prior boards and all B4_01-B4_24 boards."

**Check 10 — Action history errors (spot-check: B4_03, B4_15, B4_17)?**
FAIL. Error found in B4_03.

- **B4_03 (FAIL):** Pot is CO raise / BTN call / BB call. Postflop order is BB first, CO second, BTN last (BTN is dealer-button and IP). The action_history records `(flop, BB, check), (flop, BTN, check)` — CO's flop action is absent and BTN appears to act before CO has been given the decision. In a three-way pot this order is wrong: BTN cannot check before CO acts. The correct history should read `(flop, BB, check)` only — CO is the hero and the decision point, so BTN's check should not appear in the history at all (BTN has not yet acted when hero CO is making the decision). As written, BTN's check entry implies BTN acted out of sequence before CO.

- **B4_15 (PASS):** CO raise / BTN call / BB call. Postflop order BB, CO, BTN. Action history records flop: BB check, CO check, BTN check; turn: BB check, CO check. Hero is BTN at turn decision. Order is correct throughout.

- **B4_17 (PASS):** CO raise / BTN call / SB call. Postflop order SB, CO, BTN. Action history records flop: SB check, CO check, BTN check; turn: SB check (hero decision). Order is correct throughout.

---

## Summary Table

| # | Check | Result |
|---|-------|--------|
| 1 | B4_03 removed from BP1, OOP only | PASS |
| 2 | B4_25 added for BP6-G; B4_22 BP5-only | PASS |
| 3 | Total = 104 | PASS |
| 4 | BP2 = 12 | PASS |
| 5 | BP3 = 20 | PASS |
| 6 | All boards to_call = 0 | PASS |
| 7 | No Section 8 open items | PASS |
| 8 | BP6 board isolation complete | PASS (with note on BP6-H shared boards) |
| 9 | B4_25 card conflicts checked | PASS |
| 10 | Action history errors (spot-check 3 boards) | FAIL — B4_03 flop history has BTN acting before CO |

---

## Required Fix

**B4_03 action_history correction.**

Current (incorrect):
```
(flop, BB, check), (flop, BTN, check)
```

Correct:
```
(flop, BB, check)
```

In the CO/BTN/BB postflop order (BB → CO → BTN), when hero is CO and both BB and CO have not yet resolved the flop, BTN cannot have a completed action in the history. The action_history should show only `(flop, BB, check)` — BB has acted, CO (hero) is next. BTN's action is pending and must not appear. This matches the pattern used by B4_15 and B4_17, where only villain actions prior to the hero's decision point are recorded.

This is a single-line correction in the board definition and in the BP2 section structural note.
