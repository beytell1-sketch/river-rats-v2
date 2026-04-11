# Board Architect — Blocker Fixes Delivery

**Date:** 9 April 2026
**From:** Board Architect
**To:** Owner / Independent Reviewer
**Re:** BOARD_ALLOCATION_V3_FINAL.md — all 4 gate-review blockers resolved

---

## Status

BOARD_ALLOCATION_V3_FINAL.md has been overwritten with the corrected version.
All four blockers from REVIEW_BOARD_ALLOCATION_FINAL.md are resolved.
Total situation count verified at 151. Document is ready for design agents.

---

## What was fixed

### BLOCKER 1 — Total count (was 155, now 151)

Removed SP9 sits 11-12 (both B32, board_favour trigger) and SP10 sits 14-15
(both B32, middle-range fill). These were the four situations added by B32 in
the previous iteration. They were the most redundant:

- SP9 board_favour trigger was already covered by 4 sits on B07 (x2), B19,
  and B23. The B32 pair added no new trigger type or texture variant.
- SP10 middle-range fill was already served by 13 sits across 13 distinct
  boards. The B32 pair duplicated the IP/connected/draw profile of B14/B16.

B32 is retained in the board inventory (satisfying R2's connected-board
minimum of 3: B07, B19, B32) with zero situation assignments. R2 is a
board-inventory test. SP9 is now 10 sits; SP10 is now 13 sits. Total = 151.

### BLOCKER 2 — SP3 sit#6: no bet to check-raise

B10 (to_call=0, hero leads) cannot produce a check-raise. SP3 sit#6
reassigned to B13 (Qd 6h 2s Jc, turn, SB OOP, to_call=70, SPR=8.4,
rainbow). B13 already appears in SP3 at sit#8 (range_pct=0.94); sit#6 uses
range_pct=0.91 — a distinct hand profile. Both rows are structurally valid
check-raise situations. Rainbow count in SP3 is preserved at 2 (B13 x2,
B17 x1). B10 is removed from SP3 entirely; it remains in SP2 and SP10. The
SP3 "Note on B10 SPR" explaining the dual-SPR mechanism has been removed as
it no longer applies to SP3.

### BLOCKER 3 — B26 villain_positions

BTN folded on the flop. By river, only BB (hero) and CO remain. The original
`['CO', 'BTN']` violated the "bettor LAST" rule and included a folded player.

Fixed to `['CO']`. CO is the sole active villain and is the bettor. This is
the cleanest notation — a folded player has no presence at the river decision
point. The fix is in the B26 board definition only. All SP8, SP9, and SP4
rows referencing B26 remain logically correct (CO is still the bettor;
villain_aggression_count from CO's flop + turn bets is still >= 2).

### BLOCKER 4 — SP4 sits 1-2: S2 requires flush_danger >= 0.60 AND is_paired == 1

B15 (rainbow, flush_danger = 0) and B06 (rainbow, flush_danger = 0) cannot
satisfy S2. New board B33 added to the inventory.

B33: `['Qh', 'Qd', '7h']` — flop, BB OOP, SPR=5.5, to_call=30.
- Paired (queens): is_paired = 1
- Two hearts (Qh, 7h): flush_danger ~0.65, satisfying flush_danger >= 0.60
- Both S2 conditions satisfied simultaneously

SP4 sits 1-2 reassigned from B15/B06 to B33 (x2 sits, different monster
hand profiles). B33 must be verified against the 46-board PA inventory
before build — flagged in the B33 board definition note. B06 and B15 retain
all other assignments (SP3, SP6, SP7).

Board count rises to 33. SP4 unique board count is now 5 (B33, B09, B12,
B20, B26). All minimums met.

---

## Verification counts

| Sub-pattern | Situations |
|-------------|------------|
| SP1         | 18         |
| SP2         | 10         |
| SP3         | 12         |
| SP4         | 6          |
| SP5         | 28         |
| SP6         | 13         |
| SP7         | 25         |
| SP8         | 16         |
| SP9         | 10         |
| SP10        | 13         |
| **Total**   | **151**    |

RAISE total: 18+10+12+28+25+16 = 109
CALL total: 6+13+10+13 = 42
Grand total: 109 + 42 = **151**

---

## File written

`river-rats-v2/review/BOARD_ALLOCATION_V3_FINAL.md` — overwritten.

The "Corrections from final review" section appears at the top of the
document, listing all four fixes before the v2 corrections section.

---

*Board Architect delivery confirmed. Document is safe for design agents.*
