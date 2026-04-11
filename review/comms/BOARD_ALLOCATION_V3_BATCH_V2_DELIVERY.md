# Delivery: BOARD_ALLOCATION_V3_BATCH_V2.md
**Date:** 9 April 2026
**From:** Board Architect
**To:** Owner / Design Agents
**Re:** Clean v2 of board allocation — all 10 review corrections applied

---

## Delivery confirmed

File written to:
`river-rats-v2/review/BOARD_ALLOCATION_V3_BATCH_V2.md`

This is the clean production version. All tables reflect final state.
No correction notes below tables. Section 7 (SPR Revision Log) and
Section 8 (Open Items) removed.

---

## What changed from v1

### Critical fixes applied to tables

1. **villain_positions corrected on 6 boards.** Bettor is now last in
   every list. Boards corrected: B03 ['SB','BB'], B14 ['SB','BB'],
   B19 ['BB','SB'], B20 ['SB','BB'], B28 ['SB','BB']. B25 now shows
   ['BB'] only — SB folded on the flop and must not appear at the
   river decision point.

2. **SP2 table rewritten.** Old table had 8 of 10 situations on boards
   with SPR=9.0 or SPR=3.0 — none satisfying Step 3 (spr <= 1.5).
   New table uses B10 (SPR=1.5), B17 (SPR=1.5), B30 (SPR=1.0), B31
   (SPR=1.4). B03 and B13 removed from SP2 entirely.

3. **Section 2 summary table updated.** All revised stack values now
   shown: B02 (450/5.0), B04 (405/4.5), B05 (540/6.0), B06 (495/5.5),
   B08 (450/5.0), B13 (1680/8.4), B30 and B31 added as new rows.

### Required fixes applied to tables

4. **SP1 table corrected.** sit#17 = B01 (second hand, SPR=5.0),
   sit#18 = B08 (second hand, SPR=5.0). B09 removed from SP1 — it
   belongs in SP4 S4 only.

5. **SP4 table corrected.** sit#6 = B20 with S5 suppressor
   (num_callers_to_bet >= 1, is_monster=1, range_pct < 0.92 → CALL).
   All 5 suppressors now represented.

6. **SP3 + B10 collision resolved and documented.** SituationSpec
   (situation_factory.py line 190) carries effective_stack as a per-
   instance field. B10 at SPR=9.0 (SP3/SP7 rows) and B10 at SPR=1.5
   (SP2 rows) are separate JSONL rows with different feature vectors.
   No board-level conflict. Explanation written into Section 1 B10
   notes and Section 3 SP3 header.

7. **SP10 band 0.75-0.80 fixed.** sit#13 (B15) adjusted from pct=0.73
   to pct=0.76. Band now has 3 situations (sits 10, 11, 13). Total
   stays at 13.

### Pending verification items (marked in tables, not separate notes)

8. **SP7 sits 3, 9, 21** marked PENDING GTO in the SP7 table. GTO
   Expert must sign off on thin-value OOP check-raises at SPR=9.0
   before these situations are built.

9. **B22 straight_danger** marked PENDING VERIFICATION in Section 1.
   Programmer must confirm straight_danger >= 0.40 before B22 counts
   as connected board.

10. **B20 flush_danger for SP2** marked PENDING VERIFICATION in SP2
    table. Programmer must confirm flush_danger <= 0.20. Note: B20 is
    not currently in SP2 — sits 9-10 are allocated to B20 but flagged
    as conditional on this verification.

---

## Design agent readiness

The document is ready for design agents to use for all sub-patterns
except the three pending items above. Agents should skip SP7 sits 3,
9, 21 until GTO Expert confirms; treat B22's connected status as
provisional; treat SP2 sits 9-10 as provisional pending flush_danger
check.

All other 148 situations have clean, self-consistent board definitions
with correct villain_positions, correct SPR values, and correct
allocation tables.
