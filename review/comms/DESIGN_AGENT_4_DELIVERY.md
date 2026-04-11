# Design Agent 4 — Delivery Confirmation

**Date:** 9 April 2026
**From:** Design Agent 4
**To:** Reviewer / Owner
**Re:** SP8 and SP9 hero card assignments — 26 situations

---

## Delivery

File written to:
`river-rats-v2/review/DESIGN_AGENT_4_SP8_SP9.md`

---

## Scope Delivered

- SP8: 16 RAISE situations (river bluff raises, Step 6)
- SP9: 10 CALL situations (flat spots, Step 1)
- Total: 26 situations across 7 SP8 boards and 9 SP9 boards

---

## SP8 Summary

All 16 situations satisfy Step 6 requirements:
- street == 2 (river): all 16 PASS
- hero_range_percentile <= 0.20: range 0.02-0.19, PASS
- villain_fold_equity_estimate >= 0.50: range 0.50-0.72, PASS
- villain_top_pair_plus_pct <= 0.35: range 0.10-0.35, PASS
- num_callers_to_bet == 0: all 16, PASS
- villain_aggression_count == 0: all 16, PASS

Hand type counts (minimums all met):
- Bricked flush draw: 5 situations (min 4)
- Bricked straight draw: 5 situations (min 4)
- Pure air: 6 situations (min 4)

Unique boards: 7 (B23, B24, B25, B26, B27, B28, B29 — all river boards, min 5)

One correction during design: SP8_10 initial hero_cards (Jc Th on B26 board
Kh 5c 2h 9d Qh) were rejected because J-T makes a King-high straight with the
board (K-Q-J-T-9). Revised to Jc 8d — a gutshot draw to 8-9-T-J-Q that missed.

B26 and B28 cannot support bricked flush draws in the traditional sense (B26 has
3 hearts completing a flush; B28 has 3 spades completing a flush; no other suit
has 2 board cards). B26 uses bricked straight draw (SP8_10) and pure air (SP8_11).
B28 uses dead heart draw/air (SP8_14) and bricked straight draw (SP8_15). This is
documented in the design file.

---

## SP9 Summary

All 3 triggers present with minimum counts met:
- Trigger A (board_favour <= -0.30): 5 situations (SP9_01, 02, 03, 04, 10)
- Trigger B (aggr_count >= 2): 3 situations (SP9_05, 06, 07)
- Trigger C (num_callers >= 1): 2 situations (SP9_08, 09)

board_favour range: -0.32 to -0.55 (spans target of -0.30 to -0.60)
villain_aggression_count variation: 2 and 3 both used
All 10 situations: is_monster == 0

Unique boards: 9 (B07, B19, B23, B26, B29, B12, B24, B25, B17)

---

## Card Conflict Verification

All hero cards were verified individually against their board card list:
- Rank AND suit checked for each hero card against each board card
- SP8: flush suits carefully audited per board (2-suit boards = bricked draws OK;
  3-suit boards = completing suit excluded from hero holdings)
- SP9: standard conflict check (no suit-specific constraints apply)

No conflicts found.

---

## Ready for review
