# Gate Review: BOARD_ALLOCATION_V3_FINAL.md

**Date:** 9 April 2026
**Reviewer:** Independent Reviewer
**Document reviewed:** BOARD_ALLOCATION_V3_FINAL.md
**Supporting docs:** GTO_EXPERT_B22_SP7_RESOLUTION.md, FACTORY_DESIGN_RAISE_CONTEXTS_V2.md

---

## Verdict: ISSUES FOUND — DO NOT PASS TO DESIGN AGENTS YET

Two blockers must be resolved. A third issue should be clarified before build.
Three known deviations are acceptable and do not block.

---

## Blockers (must fix before build)

### BLOCKER 1 — SP9 and SP10 situation counts exceed brief; total is 155, not 151

The brief (FACTORY_DESIGN_RAISE_CONTEXTS_V2.md) specifies:
- SP9 = 10 CALL situations
- SP10 = 13 CALL situations
- Total = 151

The allocation document adds 2 B32 situations to SP9 and 2 to SP10:
- SP9 header: "CALL only (12 situations)"
- SP10 header: "Middle range CALL fill (15 situations)"

Recount with updated sizes:
- RAISE: SP1(18) + SP2(10) + SP3(12) + SP5(28) + SP7(25) + SP8(16) = 109
- CALL: SP4(6) + SP6(13) + SP9(12) + SP10(15) = 46
- **Total: 155**

The document states "32 boards, 151 situations" in three places but the sub-pattern
rows sum to 155. The brief's totals table has not been updated to reflect the B32
additions. Either the brief's totals must be updated to 155, or four situations must
be removed from other sub-patterns to restore the 151 target.

This is an arithmetic inconsistency the design agents cannot resolve on their own.
A design agent following the totals table (151) will disagree with the sub-pattern
tables (155). The Board Architect must state the authoritative total and update
whichever document is wrong.

---

### BLOCKER 2 — SP3 sit#6 (B10) has no bet for hero to check-raise

SP3 is "Monster + OOP check-raise." Every SP3 situation requires hero (OOP) to be
facing a bet so they can check-raise.

B10 (Kc 4d 2h):
- to_call: 0
- action_history ends at: `(flop, BB, check)`
- villain_positions: `['CO', 'BTN']` (no bettor — hero leads, to_call=0)

There is no bet in the action history. A design agent following SP3 sit#6 would be
building a check-raise where no check-raise is available — the action sequence has
hero as the last actor with no bet facing them. The SituationSpec for this row cannot
produce a valid check-raise feature vector.

The Board Architect note on this row reads: "SP3 sit#6 uses B10 at SPR=9.0. SP2 also
uses B10 at SPR=1.5. This is not a conflict." The note addresses the SPR difference
but not the to_call=0 action structure problem.

Fix required: either assign SP3 sit#6 to a different board where hero faces a bet,
or add a villain bet to B10's action history (making to_call > 0) and update the
board definition accordingly for this usage. The latter would require B10 to split
into two board definitions (one with and one without a villain bet), which is the
cleanest solution given that B10 at to_call=0 is already used correctly in SP2 and
SP10.

---

## Clarification required (should fix, not strictly a hard blocker)

### ISSUE 3 — SP4 sit#1 (B15, suppressor S2): flush_danger condition cannot fire

SP4 S2 suppressor definition (from the brief): "paired board with flush danger
(flush_danger >= 0.60, is_paired == 1)."

B15 (Tc 3d 9h 9s) is rainbow. flush_danger = 0. The S2 condition requires
flush_danger >= 0.60. A rainbow board cannot satisfy this condition.

SP4 sit#1 is therefore not a valid S2 example — no design agent can construct a
feature vector from B15 that satisfies both is_paired=1 AND flush_danger >= 0.60.

The intent may be that S2 fires on is_paired alone (without the flush_danger
requirement), or that B15 should be replaced with a two-tone paired board (e.g.
B21, which is paired threes and two-tone). This needs an explicit ruling from the
Board Architect or GTO Expert before a design agent assigns hero cards to this row.

SP4 sit#2 (B06, S2) is correctly placed: B06 is the paired eights board and is
rainbow — same issue applies. B06's flush_danger is also 0 (rainbow board). If S2
requires flush_danger >= 0.60, neither SP4 sit#1 nor sit#2 has a valid board.

If the intent is that S2 fires on is_paired alone (paired board is sufficient,
flush_danger is a separate suppressor, S2 description is mislabelled in the brief),
this must be stated explicitly so design agents do not add artificial flush_danger
values to rainbow boards.

---

## Acceptable deviations (no action required)

### Turn at 45% (ceiling 43%)
Documented and justified. The 4 B32 situations are required for the connected-board
minimum. The overage is 2 percentage points on an approximate count. No trim needed.

### 8.0+ SPR tier at ~14% (minimum 15%)
Documented. ~21 situations remain in this tier across B03, B07, B09, B10 (SP3),
B13. The shortfall is 1-2 situations and the tier is qualitatively well-represented.
Acceptable.

### Connected boards at 9% (target 12-16%)
Three connected boards meet the hard minimum of 3. The percentage shortfall is
structural — adding a fourth connected board would require either displacing an
existing board or growing the set. Documented and accepted.

---

## Spot-checks: action history validity

**B01 (SP5 sit#1):** Preflop BTN raise → SB call → BB call. Flop: SB check → BB
bet. Hero (BTN) faces BB's bet. to_call=30 matches. IP check-raise semi-bluff
structure valid.

**B19 (SP9 sit#3):** Preflop BTN raise → SB call → BB call. Flop: SB/BB/BTN all
check. Turn: SB bets (donk). villain_positions: ['BB', 'SB'] — SB is last (bettor).
Hero BTN faces the bet. to_call=55. board_favour trigger valid. Action sequence
valid.

**B26 (SP8 sit#10):** Preflop CO raise → BTN call → BB call. Flop: BB check → CO
bet → BTN fold → BB call. Turn: BB check → CO bet → BB call. River: BB check → CO
bet. hero_pos=BB (OOP), faces CO's river bet. villain_positions: ['CO', 'BTN'] — CO
is listed first, BTN folded on flop. Wait: BTN folded flop but is still in
villain_positions list. This is notation only — the bettor (CO) must be LAST per the
rule, but CO is listed first here with BTN second. This violates the "bettor LAST"
rule.

Checking B26 definition: villain_positions: `['CO', 'BTN']` (CO is bettor). CO is
first, not last. If the rule is "bettor LAST," this entry is wrong. BTN folded on the
flop but is listed after CO, which would imply BTN is the bettor. A design agent
reading this row would assign the bettor role to BTN (the last listed villain) — but
BTN is not in the hand on the river.

This is a notation error in B26's villain_positions. It should be
`['BTN', 'CO']` with CO last to indicate CO is the bettor, or the folded player
should be omitted entirely. This affects SP8 sits 10-11, SP4 sit#4, and SP9
sit#6 which all reference B26.

**Adding to blockers:** B26 villain_positions has bettor listed first, not last.
This is a fourth issue that needs correction before build.

---

## PENDING flags

All three v2 pending items (A, B, C) are confirmed resolved. No PENDING text
remains in the document. GTO Expert sign-offs are correctly recorded in the
corrections section.

---

## SP2 compliance check (SPR <= 1.5 throughout)

All 10 SP2 rows use SPR <= 1.5:
- B10 rows: SPR=1.5 (effective_stack=135, pot=90)
- B17 rows: SPR=1.5 (effective_stack=270, pot=180)
- B30 rows: SPR=1.0
- B31 rows: SPR=1.4
- B20 rows: SPR=1.4

The dual-SPR mechanism (B10 at SPR=9.0 for SP3 vs SPR=1.5 for SP2) is clearly
explained. Design agents are explicitly told to set effective_stack at the
SituationSpec level. PASS.

---

## SP7 replacement sits placement

GTO Expert specified:
- Sit A (band 0.75-0.80): B06, SPR=5.5, range_pct=0.78, fold_eq=0.43, aggr=0
- Sit B (band 0.80-0.86): B08, SPR=5.0, range_pct=0.82, fold_eq=0.50, aggr=1
- Sit C (band 0.86-0.92): B02, SPR=5.0, range_pct=0.89, fold_eq=0.55, aggr=0

In the allocation SP7 table:
- Sit 3 (band 0.75-0.80): B06, SPR=5.5, range_pct=0.78, fold_eq=0.43, aggr=0 — matches Sit A. PASS.
- Sit 9 (band 0.80-0.86): B08, SPR=5.0, range_pct=0.82, fold_eq=0.50, aggr=1 — matches Sit B. PASS.
- Sit 21 (band 0.86-0.92): B02, SPR=5.0, range_pct=0.89, fold_eq=0.55, aggr=0 — matches Sit C. PASS.

All three replacements correctly placed and values match the GTO Expert resolution.

---

## Summary of actions required before passing to design agents

| # | Issue | Severity | Action |
|---|-------|----------|--------|
| 1 | Total count 155 vs claimed 151 — brief and allocation disagree | BLOCKER | Board Architect to state authoritative total; update brief or allocation |
| 2 | SP3 sit#6 (B10): no bet in action history, to_call=0, check-raise impossible | BLOCKER | Replace board for SP3 sit#6, or split B10 into two variants |
| 3 | SP4 sits 1-2 (B15, B06): S2 requires flush_danger >= 0.60 but both boards are rainbow (flush_danger = 0) | CLARIFY | Ruling needed: does S2 fire on is_paired alone, or must flush_danger also be >= 0.60? Correct sit or brief accordingly |
| 4 | B26 villain_positions: CO (bettor) listed first, not last | BLOCKER | Fix to `['BTN', 'CO']` or omit folded BTN; affects SP8 sits 10-11, SP4 sit#4, SP9 sit#6 |

Blockers 1, 2, and 4 must be resolved. Issue 3 requires a ruling.
The document is not safe for design agents in its current state.
