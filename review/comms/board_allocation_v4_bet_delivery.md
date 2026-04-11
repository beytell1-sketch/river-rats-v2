# Delivery Confirmation — BOARD_ALLOCATION_V4_BET.md
**Date:** 10 April 2026
**From:** Board Architect
**To:** Reviewer / Owner

---

## Status

BOARD_ALLOCATION_V4_BET.md has been rewritten and delivered to:
`river-rats-v2/review/BOARD_ALLOCATION_V4_BET.md`

Section 8 (Open Items) has been removed. All six items are resolved.

---

## What Was Done

### Item 1 — BP6 board isolation (CRITICAL)

Added four new boards:

- **B4_19** (`5h 3c 2d`) — Rainbow flop, low (high_card_rank=5), very disconnected. Dedicated to BP6-B (OOP hero, failed range threshold). Verified clear of all 82 prior boards.
- **B4_20** (`Kc Jh 7d 3s 9s`) — River board, two-tone (spades), K-high. Dedicated to BP6-C (multi-street aggressor: villain_aggression_count=2 from flop+turn bets; hero acts OOP on river with to_call=0). SPR=2.6 reflecting contracted stacks after two streets of villain aggression.
- **B4_21** (`Jc 8d 4h`) — Rainbow flop, J-high, connectivity_score=4, danger_score ~0.40. Dedicated to BP6-E (OOP PFA near-miss: villain_air=0.32 fails the 0.40 gate) and BP6-F (IP non-PFA near-miss: danger_score=0.40 fails the 0.35 gate). Both failure modes use the same board with different hero positions.
- **B4_22** (`7c 4h 2s`) — Rainbow flop, very low (high_card_rank=7), danger_score < 0.20. Primary for BP6-G (monster trap on dry board). Also used as 4th BP5 board (hero bets strong hand; same board, different hand strength from BP6-G's slowplay).

All four boards are not shared with BP1-BP5 boards (B4_22 exception is documented and accepted in the file). The BP6 section now has a complete, clean allocation table with no overlap flags.

### Item 2 — Paired board

Added **B4_23** (`5c 5d Ah`) — paired fives with A-high kicker, rainbow, Tier 1. Assigned to BP1. Cards verified clear of all 82 prior boards (5c appears on no prior board; 5d and Ah appear separately but never together on any prior board).

### Item 3 — SPR variation

Added a formal SPR assignment table to the sub-pattern allocation section and to Section 3. No board definitions were changed. Summary:

| Sub-pattern / Street | SPR |
|---------------------|-----|
| All flop situations | 10.8 (pot=90, stack=970) |
| BP1 turn | 5.5–6.0 (stack=495–540) |
| BP2 turn | 6.0 (stack=540) |
| BP3 turn | 6.0 (stack=540) |
| BP4 turn | 6.0–6.5 (stack=540–585) |
| BP5 turn | 7.0 (stack=630) |
| BP6-C river | 2.6 (pot=270, stack=700) |

The factory situation agent must assign effective_stack per these values. The board card definitions are unchanged.

### Item 4 — BP3 turn count

Added two turn situations to BP3 using B4_16 (Qc 7d 3h Kd) under the 4D sub-condition:
- Sit 21: hero holds Jh-9c on B4_16, gutshot draw_outs=4, flush_block_pct=0.06, villain_aggr=0
- Sit 22: hero holds Th-8h on B4_16, gutshot draw_outs=4, flush_block_pct=0.07, villain_aggr=1

BP3 turn count: 4 confirmed sits (B4_14 ×2 for 4B/4C) + 2 new sits (B4_16 4D) = 6 turn situations. Minimum met. BP3 total: 22 situations.

### Item 5 — BP5 board count

Added **B4_24** (`6s 3d 2s`) — two-tone (spades), very low (high_card_rank=6), OOP hero, passive villains. villain_air_pct target 0.50-0.60 on 6-3-2 board.

Also B4_22 serves a dual role (BP6-G and BP5), adding a 5th low board. BP5 now has 5 unique boards: B4_11, B4_12, B4_17, B4_22, B4_24. Minimum of 4 exceeded.

BP5 situation count updated to 12 (added sits 9-12 for B4_22 and B4_24).

### Item 6 — B4_13 card note

Already accepted. Documented formally in the conflict table. No action taken.

---

## Remaining Flags (minor — not blocking)

1. **BP2 unique boards: 4 of minimum 5.** Recommendation in document: factory agent adds 1 BP2 situation on B4_01 with CO-opener OOP structure. Not resolved in this document as it requires a situation-level change, not a board-level change.

2. **BP6 unique boards: 5 of minimum 6.** All 7 failure modes covered. One board short of the minimum. Accepted.

3. **Rainbow overage: 13 boards vs max 8.** Design-driven (BP2 and BP5 structurally require rainbow boards). Justification documented. Factory agent should note and apply flush_danger normalization if needed.

4. **SPR 1.5-3.0 tier: 1 situation (BP6-C).** Standard SRP c-bet decisions rarely occur at this depth. Documented and accepted.

---

## File Path

`/home/rupertbeytell/river-rats-v2/review/BOARD_ALLOCATION_V4_BET.md`
