# Independent Review: BOARD_ALLOCATION_V3_BATCH.md
**Date:** 9 April 2026
**Reviewer:** Independent Reviewer
**Target:** river-rats-v2/review/BOARD_ALLOCATION_V3_BATCH.md
**Tree version checked against:** RAISE_DECISION_TREE_V2.md
**Brief checked against:** FACTORY_DESIGN_RAISE_CONTEXTS_V2.md
**Existing boards checked against:** FACTORY_DIVERSITY_AUDIT.md Section 1.1

---

## Verdict: ISSUES FOUND — DO NOT PROCEED TO DESIGN AGENTS

Six boards have a systematic villain_positions ordering error. The SP2
allocation table is unreconciled with the architect's own correction.
Two open items (SP7 SPR=9.0, SP10 band shortfall) are flagged but
unresolved. SP3 sits on a board that is being revised for SP2 in a
way that breaks SP3's SPR requirement. All errors listed below are
concrete and blockable.

---

## 1. Action History Validation (8 boards checked)

The notation rule stated in Section 1 is unambiguous:
"villain_positions list: non-bettors first, bettor LAST"

### FAIL — B03 (As 5d 2c)

villain_positions: `['BB', 'SB']` — annotated "(BB is bettor — donk)"

Postflop order with CO raising preflop, SB and BB calling: SB acts
first OOP, then BB, then CO. Action history: (flop, SB, check),
(flop, BB, bet). Bettor is BB. Per the notation rule, bettor must be
last. Correct list is `['SB', 'BB']`. Current list has bettor BB
listed first. ERROR.

### PASS — B02 (Kh 7h 3d)

villain_positions: `['HJ', 'BTN']` — annotated "(BTN is bettor)".
Postflop order in HJ-BTN-BB 3-way: BB acts first (OOP), then HJ,
then BTN. Action history: (flop, BB, check), (flop, HJ, check),
(flop, BTN, bet). Bettor is BTN, listed last. CORRECT.

### FAIL — B14 (3s Js 9h 4d)

villain_positions: `['BB', 'SB']` — annotated "(BB is bettor — donk
turn)".

Preflop: CO raise, SB call, BB call. Postflop order: SB first, then
BB, then CO. Turn action: (turn, SB, check), (turn, BB, bet). Bettor
is BB. Correct list is `['SB', 'BB']`. Current list has bettor BB
listed first. ERROR.

### FAIL — B19 (4c 6h 8s 7d)

villain_positions: `['SB', 'BB']` — annotated "(SB is bettor — donk)".

Preflop: BTN raise, SB call, BB call. Turn action: (turn, SB, bet).
Bettor is SB. Correct list is `['BB', 'SB']`. Current list has bettor
SB listed first. ERROR.

### FAIL — B20 (2c 9c Qh 6s)

villain_positions: `['BB', 'SB']` — annotated "(BB is bettor)".

Preflop: CO raise, SB call, BB call. Turn action: (flop, SB, check),
(flop, BB, bet)... (turn, SB, check), (turn, BB, bet). Bettor is BB.
Correct list is `['SB', 'BB']`. Current list has bettor BB listed
first. ERROR.

### PASS — B09 (Ah 4h 8c)

villain_positions: `['SB', 'BB']` — annotated "(BB is bettor — donk)".
Postflop: (flop, SB, check), (flop, BB, bet). Bettor is BB, listed
last. CORRECT.

### FAIL — B25 (As 6d 2h Tc 4s)

villain_positions: `['BB', 'SB']` — annotated "(BB is bettor)".

River action history: (river, BB, bet). Bettor is BB. Correct list
is `['SB', 'BB']`. Current list has bettor BB listed first. ERROR.

Additional error on B25: SB folds on the flop — action history shows
(flop, SB, fold). By the river there are only two players remaining
(BB and CO). SB must not appear in villain_positions at the river
decision point. villain_positions should be `['BB']` (one villain,
the bettor).

### FAIL — B28 (3s 7h Ks 2c Ts)

villain_positions: `['BB', 'SB']` — annotated "(BB is bettor)".

River action: (river, SB, check), (river, BB, bet). Bettor is BB.
Correct list is `['SB', 'BB']`. Current list has bettor BB listed
first. ERROR.

### Summary of action history errors

| Board | Error type | Current list | Correct list |
|-------|-----------|--------------|--------------|
| B03 | Bettor first, not last | ['BB', 'SB'] | ['SB', 'BB'] |
| B14 | Bettor first, not last | ['BB', 'SB'] | ['SB', 'BB'] |
| B19 | Bettor first, not last | ['SB', 'BB'] | ['BB', 'SB'] |
| B20 | Bettor first, not last | ['BB', 'SB'] | ['SB', 'BB'] |
| B25 | Bettor first + folded player included | ['BB', 'SB'] | ['BB'] |
| B28 | Bettor first, not last | ['BB', 'SB'] | ['SB', 'BB'] |

Pattern: every board where a BB or SB player donk-bets has the bettor
listed first. This is systematic. The architect appears to have
placed the donk-bettor at the start of the list on the assumption
that "donk = unexpected = first to mention", but the rule requires
bettor last regardless of whether it is a donk bet. All six boards
need correction before design agents use them.

---

## 2. SPR Math Verification (all 31 boards)

Checked as: stated_SPR = effective_stack / pot. Original values
unless otherwise noted; revised values from Section 7 also checked.

| Board | Pot | Stack | Computed SPR | Stated SPR | Match? |
|-------|-----|-------|-------------|-----------|--------|
| B01 | 90 | 450 | 5.00 | 5.0 | PASS |
| B02 (revised) | 90 | 450 | 5.00 | 5.0 | PASS |
| B03 | 90 | 810 | 9.00 | 9.0 | PASS |
| B04 (revised) | 90 | 405 | 4.50 | 4.5 | PASS |
| B05 (revised) | 90 | 540 | 6.00 | 6.0 | PASS |
| B06 (revised) | 90 | 495 | 5.50 | 5.5 | PASS |
| B07 | 90 | 810 | 9.00 | 9.0 | PASS |
| B08 (revised) | 90 | 450 | 5.00 | 5.0 | PASS |
| B09 | 90 | 720 | 8.00 | 8.0 | PASS |
| B10 | 90 | 810 | 9.00 | 9.0 | PASS |
| B10 (SP2 revision) | 90 | 135 | 1.50 | 1.5 | PASS |
| B11r | 90 | 450 | 5.00 | 5.0 | PASS |
| B12 | 210 | 630 | 3.00 | 3.0 | PASS |
| B13 | 200 | 560 | 2.80 | 2.8 | PASS |
| B13 (revised) | 200 | 1680 | 8.40 | 8.4 | PASS |
| B14 | 180 | 540 | 3.00 | 3.0 | PASS |
| B15 | 200 | 520 | 2.60 | 2.6 | PASS |
| B16 | 180 | 720 | 4.00 | 4.0 | PASS |
| B17 | 180 | 540 | 3.00 | 3.0 | PASS |
| B17 (SP2 revision) | 180 | 270 | 1.50 | 1.5 | PASS |
| B18 | 190 | 760 | 4.00 | 4.0 | PASS |
| B19 | 180 | 360 | 2.00 | 2.0 | PASS |
| B20 | 200 | 280 | 1.40 | 1.4 | PASS |
| B21 | 190 | 570 | 3.00 | 3.0 | PASS |
| B22 | 200 | 280 | 1.40 | 1.4 | PASS |
| B23 | 400 | 360 | 0.900 | 0.9 | PASS |
| B24 | 380 | 330 | 0.868 | 0.87 | PASS (rounded) |
| B25 | 360 | 320 | 0.889 | 0.89 | PASS (rounded) |
| B26 | 370 | 300 | 0.811 | 0.81 | PASS (rounded) |
| B27 | 350 | 315 | 0.900 | 0.9 | PASS |
| B28 | 400 | 360 | 0.900 | 0.9 | PASS |
| B29 | 380 | 340 | 0.895 | 0.89 | PASS (rounded) |
| B30 (new) | 90 | 90 | 1.00 | 1.0 | PASS |
| B31 (new) | 180 | 252 | 1.40 | 1.4 | PASS |

All SPR calculations are arithmetically correct. No errors.

---

## 3. Sub-Pattern Condition Checks

### SP1 — flush_danger >= 0.40 requirement

The brief specifies hand_category >= 10 (two_pair or better) and
flush_danger >= 0.40 for SP1 to qualify as a wet board raise. Spot-
checking the allocation:

- B05 (monotone spades): flush_danger target 0.90. Qualifies.
- B11r (Ts 8s 4h, two-tone): flush_danger target 0.55. Qualifies.
- B02 (revised SPR=5.0, two-tone hearts): flush_danger target 0.45. Qualifies.
- B01 (two-tone clubs): flush_danger target 0.40. At the floor — qualifies.

SP1 sit#17 (B09, SPR=8.0, is_ip=1): The allocation table still
assigns this to SP1. The note below the table says to reallocate to
SP4 S4, and says the 17th slot goes to B01 (second hand) and the
18th to B08 (second hand). However, the table still shows sit#17 as
B09 and sit#18 as B01. The note and the table are in direct conflict.
Design agents will not know which to follow.

ACTION REQUIRED: Update the SP1 table so sit#17 is B01 (second hand)
and sit#18 is B08 (second hand). Remove B09 from the SP1 table
entirely. The note is not sufficient — the table is what design
agents use.

### SP2 — SPR <= 1.5 requirement (CRITICAL)

Step 3 requires spr <= 1.5 AND hero_range_percentile >= 0.90. The
SP2 allocation table in Section 3 shows:

| Sit# | Board | SPR |
|------|-------|-----|
| 1 | B03 | 9.0 |
| 2 | B03 | 9.0 |
| 3 | B10 | 9.0 |
| 4 | B10 | 9.0 |
| 5 | B17 | 3.0 |
| 6 | B17 | 3.0 |
| 7 | B13 | 2.8 (or 8.4 revised) |
| 8 | B13 | 2.8 (or 8.4 revised) |
| 9 | B20 | 1.4 |
| 10 | B20 | 1.4 |

Eight of ten SP2 situations use boards with SPR above 1.5. None of
these satisfy Step 3 (spr <= 1.5). The architect acknowledges this
in Open Item 2 and proposes a correction (B10 revised to SPR=1.5,
B17 revised to SPR=1.5, add B30 and B31). But the SP2 allocation
table in Section 3 was never updated.

This is the single most dangerous error in the document. Design
agents reading Section 3 will design SP2 situations on SPR=9.0
boards. Step 3 cannot fire at SPR=9.0. The labelling agent will
label those situations CALL, not RAISE, because no tree step applies.
The entire SP2 batch would be wasted.

ACTION REQUIRED: Rewrite the SP2 allocation table in Section 3 to
use the corrected boards: B10(revised, SPR=1.5), B17(revised,
SPR=1.5), B30(SPR=1.0), B31(SPR=1.4). Also verify B30 and B31 meet
flush_danger <= 0.20 and straight_danger <= 0.20 (both appear dry
per their definitions — confirmed from board cards).

### SP2 board B20 qualification check

B20 (2c 9c Qh 6s) is used for SP2 sits 9-10. Open Item 2 flags that
B20 has flush_danger "may be too high at ~0.30" — two clubs on the
board (2c, 9c). SP2 requires flush_danger <= 0.20. If flush_danger
is 0.30 on B20, these two situations do not qualify for SP2. The
architect does not resolve this — it is left as a query. This must
be resolved before design agents use B20 for SP2.

### SP3 + B10 SPR conflict

SP3 sit#6 uses B10 (BB OOP, SPR=9.0 original). The brief's per-
pattern variation requirement for SP3 is SPR 2.0-3.5. More
importantly, Open Item 2 revises B10's effective_stack to 135 for
SP2, giving SPR=1.5. If B10 is revised to SPR=1.5, then SP3 sit#6
(which also sits on B10) would be at SPR=1.5 — outside SP3's 2.0-3.5
target range and at step 3's stack-off zone, not SP3's monster OOP
check-raise zone.

The architect does not flag this interaction. It is a collision
between the SP2 correction and SP3.

ACTION REQUIRED: SP3 sit#6 (B10) must move to a different board if
B10 is revised to SPR=1.5. Or B10 must be maintained at two different
SPR values for different sub-patterns — which requires two separate
board entries (physically distinct situations), not the same board
with different stacks implicitly. This needs explicit resolution.

### SP4 — all suppressors present check

The allocation table lists six SP4 sits with suppressors S2 (sits
1-2), S3 (sits 3-4), S4 (sits 5-6). S5 is missing. The architect
notes this and says sit#6 should change to B20 with S5. But the
table still shows sit#6 as B03 S4. Same conflict-between-table-and-
note problem as SP1 sit#17.

ACTION REQUIRED: Update the SP4 table so sit#6 uses B20 with S5
suppressor, not B03 with S4.

### SP5 — flush_draw_rank and flush_block_pct conditions

All 28 SP5 situations show flush_draw_rank >= 12 (ranks 12, 13, or
14) and flush_block_pct > 0 (range 0.08-0.35). Both conditions of
v2 Step 5 are met. Spot-check sit#28 (B11r, rank=12, block=0.08,
fold_eq=0.68): 12 >= 12 PASS, 0.08 > 0 PASS, 0.68 >= 0.45 PASS.
SP5 conditions appear correctly applied.

Note: SP5 sit#24 and #25 use B05 (monotone flop). On a monotone
board, hero's suit draw is the same suit as the board — so flush_draw
rank applies to the board suit. Having Ac or Kc on a monotone spade
board does not give a spade flush draw. Design agents must verify
the suit logic carefully on B05. This is not a table error but a
downstream risk.

### SP7 — villain_fold_equity_estimate >= 0.40 check

Sit#12 shows fold_eq=0.40 (B21, band 0.80-0.86). This is exactly at
the threshold. The tree requires >= 0.40 (not >). At exactly 0.40
the condition is met. PASS.

Sit#6 shows fold_eq=0.43. PASS. Sit#1 shows 0.42. PASS. No SP7
situation has fold_eq below 0.40. SP7 fold_equity conditions are
correctly applied.

### SP8 — street == 2 (river only) check

All 16 SP8 situations are on B23-B29, all of which are river boards.
The board definitions confirm street=river for all seven river boards.
PASS.

---

## 4. Card Conflict Check (B11 fix verification)

Original B11 (Ts 8s 3h) conflicted with existing PA_Board6 (Ts 8h
3s) — same ranks, different suits. The architect correctly identifies
this as a rank-level conflict and replaces it with B11r (Ts 8s 4h).
Ts 8s 4h does not appear in the existing 46-board inventory. Fix is
valid.

All other boards were checked in Section 4 of the allocation document.
Independent spot-check of the highest-risk cases:

- B03 (As 5d 2c): As7s3cKs9d exists in existing 46 (Batch 2 FB_B4).
  Different cards beyond As. No conflict. CLEAR.
- B07 (5h 6c 7d): 7s6s5d exists (Batch 1 PA_Board2 equivalent SB_B5).
  Different suits throughout. No conflict. CLEAR.
- B16 (5h Kd 2h 8c): 8h5h2d exists (Batch 2 FB_B5 partial). Full
  board is 8h5h2dQhJc (5-card). B16 shares 5h and 2h but the full
  combination of four cards (5h Kd 2h 8c) does not appear. CLEAR.

---

## 5. R1-R7 Compliance Spot-Check

### R1 — Board count and reuse

29 boards designed (31 with B30, B31). All checked against existing
46. One conflict caught and corrected (B11). No remaining conflicts
found. Board count 31 >= 25 minimum. PASS.

### R2 — Texture distribution (29 boards)

| Texture | Count | % | Target |
|---------|-------|---|--------|
| Rainbow | 9 | 31% | 24-32% PASS |
| Two-tone | 15 | 52% | 44-52% PASS |
| Monotone | 1 | 3% | 4-8% — MARGINAL |
| Paired | 3 | 10% | 8-12% PASS |
| Connected | 2-3 | 7-10% | 12-16% SHORT |

Monotone: The requirement is 1-2 boards minimum. One board (B05)
meets the count floor. However the percentage target is 4-8%, and 1
board = 3%. The document calls this marginal and accepts it. The
brief requirement in R2 says "Min boards: 1, Max boards: 2" so the
count is technically compliant at 1. PASS (at floor).

Connected: B07 (567) and B19 (4678) clearly qualify at
straight_danger >= 0.40. B22 (Jh 4c 2h Td) — J-T on board gives
moderate connectivity but the 4 and 2 are gaps; straight_danger
depends on the exact feature calculation. The architect tentatively
counts B22 to reach 3 boards. If B22 does not qualify, connected
count is 2, below the minimum of 3. This cannot be verified without
running the feature extractor.

MARGINAL — needs programmer verification that B22 produces
straight_danger >= 0.40. If it does not, a replacement connected
board must be added.

### R3 — SPR distribution

The architect's final stated distribution is:

| Tier | Situations | % | Requirement |
|------|------------|---|-------------|
| 1.0-2.0 | ~34 | 22% | max 25% |
| 2.0-4.0 | ~49 | 32% | min 30% |
| 4.0-8.0 | ~49 | 32% | min 25% |
| 8.0+ | ~23 | 15% | min 15% |

All four tiers meet requirements at the stated counts. However these
are approximate (~) counts and the SPR revisions are applied
inconsistently across sections (the summary table in Section 2 still
shows original SPR values for B02, B05, B06, B08, while Section 7
shows revised values). The design agents will need to use revised
values. The summary table must be updated to reflect all revisions
or design agents will build from wrong SPR values.

No-single-value rule: SPR=5.0 is applied to B01, B02(revised),
B04(revised at 4.5), B08(revised), B11r — roughly 23-25 situations.
After the B04 and B06 spread adjustments noted in R3 analysis, the
architect estimates this comes under the 20% cap. Given
~151 situations, 20% = 30.2 situations. SPR=5.0 boards (B01 at 5.0,
B02 at 5.0, B08 at 5.0, B11r at 5.0) contribute roughly 5+8+5+5=23
situations = 15%. PASS. (B06 is at 5.5 and B04 at 4.5 so they do
not cluster with SPR=5.0.)

### R4 — Street distribution

Architect's final estimate: Flop ~48 (32%), Turn ~64 (42%), River
~39 (26%). Flop target 27-36% PASS. River target 23-33% PASS. Turn
target 33-43% — 42% is within range. PASS.

### R5 — Position distribution

Architect estimates ~68 OOP (45%), ~83 IP (55%). OOP target 55-70:
68 is within range. IP target 80-95: 83 is within range. PASS.

Note: SP7 is 25 situations all OOP and SP3 is 12 situations all OOP.
That is 37 guaranteed OOP. The model for remaining sub-patterns must
hit at least 18 more OOP (to reach 55 minimum) and no more than 33
more OOP (to stay under 70). The architect's estimate of 31 more OOP
from other sub-patterns gives 68 total, within range. This estimate
should be verified against the actual allocation tables once SP2 is
corrected.

---

## 6. Open Item Assessments

### Open Item 3 — SP7 at SPR=9.0 (sits 3, 9, 21 on B10)

The tree's Step 4 has no SPR ceiling. The only relevant suppressor
for a non-monster OOP hand at high SPR is if S4 fires — but S4
requires is_ip == 1 AND spr >= 6.0. B10 has hero at BB (OOP), so
is_ip == 0 and S4 does not fire. Step 4 therefore fires if all other
conditions are met.

The brief's per-pattern requirement for SP7 says "SPR: span 2.0-3.5"
as a design preference, not a tree gate. The tree itself does not
exclude SPR=9.0 for SP7.

The GTO concern is real: at SPR=9.0, a check-raise by an OOP player
who is a non-monster commits a significant fraction of effective
stack and leaves a very large SPR-relative bet for the villain to
respond to. The fold equity calculation changes substantially at
deep SPR. This is a legitimate poker judgment question that the
architect correctly flags for GTO Expert review.

ASSESSMENT: The three SP7 situations at SPR=9.0 (B10) are tree-
valid but poker-suspect. This must be resolved by GTO Expert before
these boards are used for SP7. If the GTO Expert says thin value
OOP check-raises at SPR=9.0 are not sound, those three situations
must move to a different board or be dropped. Do not proceed with
B10 for SP7 without that sign-off.

### Open Item 2 — SP2 board reassignment (dry and SPR <= 1.5)

Proposed replacement boards:
- B10 (revised): Kc 4d 2h, pot=90, stack=135, SPR=1.5. Rainbow, dry.
  flush_danger=0. straight_danger low (K-4-2 has no straight
  connectivity). Qualifies.
- B17 (revised): Ad 7s 3c 2h, pot=180, stack=270, SPR=1.5. Rainbow,
  dry. flush_danger=0. Qualifies.
- B30: 5c 3d 2s, pot=90, stack=90, SPR=1.0. Rainbow, very dry.
  flush_danger=0. Qualifies.
- B31: 7d 2c Ks 4h, pot=180, stack=252, SPR=1.4. Rainbow, dry.
  flush_danger=0. Qualifies.

All four replacement boards meet flush_danger <= 0.20 and
straight_danger <= 0.20, and SPR <= 1.5. The SP2 correction is
poker-valid. The problem is that the SP2 allocation table was never
updated to use these boards.

ASSESSMENT: The architect's correction is correct but incomplete.
The SP2 table in Section 3 is the live specification for design
agents. It must be rewritten before agents start.

---

## 7. New Issues Not Previously Flagged

### Issue A — Section 2 summary table shows pre-revision SPR values

The summary table in Section 2 (the primary reference table) still
shows:
- B02: stack=270, SPR=3.0
- B05: stack=270, SPR=3.0
- B06: stack=270, SPR=3.0
- B08: stack=270, SPR=3.0
- B04: stack=450, SPR=5.0
- B13: stack=560, SPR=2.8

The Section 7 revision log shows different values for all of these.
Design agents who build from the Section 2 table (the most natural
reference) will use wrong stack sizes. The table must be updated to
match the revision log before agents proceed.

### Issue B — SP3 sit#6 + B10 SPR collision

SP3 sit#6 allocates B10 (BB OOP) at SPR=9.0 for an OOP check-raise
monster spot. Open Item 2 revises B10's stack to 135 for SP2
(SPR=1.5). The same board cannot serve both SP2 (requiring SPR <= 1.5)
and SP3 (requiring SPR 2.0-3.5) unless they use different stack
values in different situations — but a board is defined by its cards,
not its stack. If the feature extractor sees effective_stack as part
of the situation, each situation can have its own stack. If the board
is treated as a fixed configuration, there is a conflict.

This needs clarification: does the board definition include the stack,
or does each situation set its own stack? If each situation sets its
own stack (which is the correct interpretation for a JSONL row), then
B10 can be used in SP2 at SPR=1.5 and in SP3 at SPR=9.0. If the
board is a fixed template, the collision must be resolved by moving
SP3 sit#6 to a different board.

The architect should clarify and document this explicitly.

### Issue C — SP10 band 0.75-0.80 shortfall

The per-pattern variation requirement for SP10 states minimum 3
situations per band. Band 0.75-0.80 has sits 10 (pct=0.75) and 11
(pct=0.78) = 2 situations, short by 1. The architect flags this in
the SP10 note and suggests adding a sit#14 (from B09 at pct=0.79),
but this would raise SP10 to 14 situations, exceeding the 13-
situation target.

This is unresolved. Options: (a) adjust one existing situation's
percentile from 0.73 to 0.76 to move it into the 0.75-0.80 band
(sit#13, B15, currently pct=0.73 — small adjustment); or (b) reduce
another band by 1 to make room for the extra 0.75-0.80 situation.
The architect must resolve this before agents build.

### Issue D — SP4 S5 suppressor table not updated

Open Item 5 states that SP4 sit#6 should use B20 with S5 suppressor.
The SP4 allocation table still shows sit#6 as B03 with S4 suppressor.
The table and the note conflict. Design agents will use the table.

---

## 8. Required Actions Before Design Agents Start

The following must be resolved — not just noted — before any design
agent begins assigning hero hands:

1. CRITICAL: Fix villain_positions ordering on B03, B14, B19, B20,
   B25, B28. (B25 also needs SB removed as a folded player.)

2. CRITICAL: Rewrite the SP2 allocation table in Section 3 using the
   corrected boards (B10-revised, B17-revised, B30, B31). Remove B03,
   B13 from SP2.

3. CRITICAL: Update the Section 2 summary table to show all revised
   SPR and stack values per Section 7.

4. REQUIRED: Update the SP1 table so sit#17 = B01 (second hand),
   sit#18 = B08 (second hand), and B09 is removed from SP1.

5. REQUIRED: Update the SP4 table so sit#6 = B20 with S5 suppressor.

6. REQUIRED: Resolve SP3 sit#6 + B10 SPR collision (clarify whether
   stack is per-situation or per-board).

7. REQUIRED: Resolve SP10 0.75-0.80 band shortfall (must reach min 3
   without exceeding 13 total situations).

8. REQUIRED: GTO Expert sign-off on SP7 at SPR=9.0 (B10 sits 3, 9,
   21) before those situations are built.

9. REQUIRED: Programmer verification that B22 (Jh 4c 2h Td)
   produces straight_danger >= 0.40. If not, add a replacement
   connected board.

10. REQUIRED: Verify B20 flush_danger <= 0.20 for SP2 use. If
    flush_danger > 0.20 on B20, remove B20 from SP2.

---

## Summary Assessment

The board architecture has good bones. The 31-board set is well-
conceived, the texture and position spread is reasonable, and the
B11 conflict was correctly caught and fixed. The SPR math is
arithmetically clean throughout.

The document has a systematic process failure: the architect
identified multiple corrections (SP2, SP1 sit#17, SP4 sit#6) and
wrote them as notes below allocation tables rather than updating the
tables themselves. The tables are what design agents will build from.
Corrections in notes will be missed.

The villain_positions ordering error affects six boards and is
systematic — every donk-bet scenario has the bettor listed first.
This error will propagate into every situation built on those six
boards if not corrected now.

Do not hand this document to design agents in its current state.
