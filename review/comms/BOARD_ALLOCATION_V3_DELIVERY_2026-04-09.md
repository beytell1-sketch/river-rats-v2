# Board Allocation V3 — Delivery Note
**Date:** 9 April 2026
**From:** Board Architect
**To:** Reviewer / Owner
**File delivered:** river-rats-v2/review/BOARD_ALLOCATION_V3_BATCH.md

---

## What was produced

31 unique boards (B01-B29 + B30, B31) allocated across all 10 sub-patterns for the 151-situation RAISE batch. The document contains:

1. Full board definitions with all required fields (board_cards, street, hero_pos, villain_positions, pot, to_call, effective_stack, SPR, action_history, opener_position, texture classification)
2. Per-sub-pattern situation allocation tables with feature targets for design agents
3. R1-R5 compliance verification with counts and distribution tables
4. SPR revision log documenting all effective_stack changes made to hit tier targets
5. Open items section flagging issues design agents must resolve

---

## Key findings and corrections made during design

**B11 conflict:** Original B11 (Ts 8s 3h) matched existing PA_Board6 (Ts 8h 3s) at rank level. Replaced with B11r (Ts 8s 4h).

**SP2 SPR problem:** Initial allocation placed SP2 situations on boards with SPR 3.0-9.0, violating the SPR <= 1.5 requirement for Step 3 (stack-off). Corrected by revising B10 and B17 effective_stacks and adding two dedicated dry-board boards (B30, B31). SP2 now uses four boards all at SPR 1.0-1.5.

**SPR tier gap:** Initial design was short on 4.0-8.0 tier (16% vs 25% minimum). Fixed by raising effective_stack on B02, B05, B06, B08 from 270 to 450-540, and by raising B04 stack to 405. Also short on 8.0+ tier — fixed by raising B13 stack to 1680 (200bb game context).

**SP7 SPR flag:** Three SP7 situations use B10 (SPR=9.0). The brief targets SPR 2.0-3.5 for SP7 but does not hard-gate it in the decision tree. Flagged for GTO Expert confirmation.

---

## R1-R5 status summary

| Requirement | Status | Notes |
|-------------|--------|-------|
| R1: 25+ unique boards, no reuse | PASS | 31 boards, all cleared vs existing 46 |
| R2: Texture distribution | PASS | Rainbow 31%, Two-tone 52%, Monotone 3%, Paired 10%, Connected 10% |
| R3: SPR distribution | PASS | After revisions: 22%/32%/32%/15% across four tiers |
| R4: Street distribution | PASS | Flop 32%, Turn 42%, River 26% |
| R5: Position distribution | PASS | OOP ~45% (68 sits), IP ~55% (83 sits) |
| R6: Boards per sub-pattern | PASS | All sub-patterns meet minimum unique boards and max sits/board |

---

## What the design agents need to do next

- Assign actual hero_cards to each situation slot using the feature targets in each sub-pattern table
- Verify no hero card conflicts with board_cards
- Resolve SP7 SPR question with GTO Expert before finalising sits 3, 9, 21
- Confirm B02 action sequence validates correctly (postflop order for BB vs HJ+BTN 3-way)
- Use revised SPR values from the revision log (not the original values in board definitions)

---

Delivery confirmed.
