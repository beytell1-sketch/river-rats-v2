# Independent Review: BOARD_ALLOCATION_V3_BATCH_V2.md
**Date:** 9 April 2026
**Reviewer:** Independent Reviewer
**Target:** river-rats-v2/review/BOARD_ALLOCATION_V3_BATCH_V2.md
**Reviewing against:** REVIEW_BOARD_ALLOCATION_V3.md (10 required actions)

---

## Verdict: PASS — with one narrow qualification on action 10

All 10 required actions from the v1 review have been applied. Two spot-check
items also pass. One qualification is noted on action 10: B20 is still
allocated to SP2 sits 9-10 (marked PENDING VERIFICATION), which is consistent
with the action requirement but leaves open a conditional exposure that the
reviewer flags below.

---

## Checklist: 10 Required Actions

### Action 1 — villain_positions fixed on B03, B14, B19, B20, B25, B28

PASS.

- B03 (As 5d 2c): corrected to `['SB', 'BB']` (BB is bettor — donk). Bettor
  last. CORRECT.
- B14 (3s Js 9h 4d): corrected to `['SB', 'BB']` (BB is bettor — donk turn).
  Bettor last. CORRECT.
- B19 (4c 6h 8s 7d): corrected to `['BB', 'SB']` (SB is bettor — donk).
  Bettor last. CORRECT.
- B20 (2c 9c Qh 6s): corrected to `['SB', 'BB']` (BB is bettor). Bettor
  last. CORRECT.
- B25 (As 6d 2h Tc 4s): corrected to `['BB']` only (BB is bettor; SB folded
  on flop). Single-element list, folded player removed. CORRECT.
- B28 (3s 7h Ks 2c Ts): corrected to `['SB', 'BB']` (BB is bettor). Bettor
  last. CORRECT.

All six boards corrected. B25 also correctly removes SB as required by the
secondary finding in the v1 review.

---

### Action 2 — SP2 table rewritten with corrected boards at SPR <= 1.5

PASS.

The SP2 allocation table in Section 3 has been fully rewritten. All ten
situations now use boards satisfying SPR <= 1.5:

- Sits 1-2: B10 at SPR=1.5 (effective_stack=135, set at SituationSpec level)
- Sits 3-4: B17 at SPR=1.5 (effective_stack=270, set at SituationSpec level)
- Sits 5-6: B30 at SPR=1.0
- Sits 7-8: B31 at SPR=1.4
- Sits 9-10: B20 at SPR=1.4 (flush_danger PENDING VERIFICATION — see action 10)

B03 and B13 have been removed from SP2. The table-level introductory note
explains the B10/B17 SituationSpec override mechanism explicitly, which is
correct. The v1 review's primary concern — design agents reading SPR=9.0
boards for SP2 — is fully resolved.

---

### Action 3 — Section 2 summary table updated with revised SPR/stack values

PASS.

The Section 2 summary table has been updated. The previously-stale values
are now corrected:

- B02: stack=450, SPR=5.0 (was 270/3.0 in v1)
- B04: stack=405, SPR=4.5 (was 450/5.0 in v1)
- B05: stack=540, SPR=6.0 (was 270/3.0 in v1)
- B06: stack=495, SPR=5.5 (was 270/3.0 in v1)
- B08: stack=450, SPR=5.0 (was 270/3.0 in v1)
- B13: stack=1680, SPR=8.4 (was 560/2.8 in v1)
- B30: stack=90, SPR=1.0 (new board)
- B31: stack=252, SPR=1.4 (new board)

All revised values from the v1 Section 7 revision log are now present in the
primary table. Section 7 itself has been removed (confirmed below). Design
agents reading Section 2 will receive correct values.

---

### Action 4 — SP1 table: sit#17 = B01, sit#18 = B08, B09 removed

PASS.

The SP1 table (18 situations) now reads:
- Sit#17: B01, BTN (IP), SPR=5.0, flush_danger 0.40, set (12+)
- Sit#18: B08, BB (OOP), SPR=5.0, flush_danger 0.50, two_pair

B09 does not appear in the SP1 table at all. The conflict between the v1
table and the correction note is resolved — the table itself is now correct.
The unique board count note at the foot of the SP1 table reflects 9 unique
boards including B01, consistent with the correction.

---

### Action 5 — SP4 table: sit#6 = B20 with S5 suppressor

PASS.

SP4 sit#6 now reads: B20, S5, SPR=1.4, CO, "num_callers_to_bet >= 1 AND
range_pct < 0.92; is_monster=1 → CALL". The footer confirms all five
suppressors are present: S2 (sits 1-2), S3 (sits 3-4), S4 (sit 5), S5 (sit 6).

The v1 table had sit#6 as B03 with S4 suppressor. That entry is gone.
The table and the design intent are now consistent.

---

### Action 6 — SP3 + B10 collision resolved and documented

PASS.

The resolution is documented in two places:

1. The B10 board definition in Section 1 includes an explicit note:
   "For SP2 use, effective_stack is set to 135 in each SP2 SituationSpec
   (SPR=1.5). Each SituationSpec carries its own effective_stack field —
   B10 at SPR=9.0 (SP3/SP7) and B10 at SPR=1.5 (SP2) are separate rows,
   not a board-level conflict."

2. The SP3 section header includes the same explanation with reference to
   situation_factory.py line 190 as the authority.

The resolution is the correct one (per-situation effective_stack, not a
board-level fixed value). The documentation is explicit enough that design
agents will not misread it. The programmer should confirm that
situation_factory.py line 190 behaves as described — but that is outside
the scope of this allocation review.

---

### Action 7 — SP10 0.75-0.80 band has 3 situations

PASS.

The SP10 table correction note states: "sit#13 adjusted from pct=0.73 to
pct=0.76, placing it in the 0.75-0.80 band alongside sits 10 and 11. Band
now has 3 situations (sits 10, 11, 13), meeting the minimum of 3. Total
remains 13."

The band breakdown at the foot of the SP10 table confirms:
- Band 0.75-0.80: sits 10, 11, 13 = 3 (meets min 3)
- All other bands at min 3

Total situation count: 13. No overage. CORRECT.

---

### Action 8 — SP7 SPR=9.0 marked PENDING

PASS.

The SP7 table section header explicitly states: "SITS 3, 9, 21: PENDING
VERIFICATION — GTO Expert sign-off required before these situations are
built."

In the SP7 table itself, sits 3, 9, and 21 (all B10, SPR=9.0) carry
"PENDING GTO" in the Status column. The Pending Verification Summary at
the end of the document lists this as Item A with the specific action
required.

Three situations are marked, which matches the count in the v1 review
(sits 3, 9, 21 on B10).

---

### Action 9 — B22 straight_danger marked PENDING

PASS.

The B22 board definition in Section 1 states: "straight_danger: PENDING
VERIFICATION — programmer must confirm straight_danger >= 0.40 (J-T on
board). If confirmed, B22 counts as the third connected board. If not, a
replacement connected board must be added."

The R2 texture distribution table in Section 4 also carries an asterisk on
B22 with the same caveat. The Pending Verification Summary lists this as
Item B.

The marking is present in the right places. Design agents cannot miss it.

---

### Action 10 — B20 flush_danger marked PENDING

PASS WITH QUALIFICATION.

The B20 board definition in Section 1 notes: "flush_danger status: PENDING
VERIFICATION — programmer must confirm flush_danger <= 0.20 before any SP2
use of this board. B20 is not currently allocated to SP2."

However, the SP2 table (action 2) includes B20 at sits 9-10 with the cell
annotation "flush_danger: PENDING VERIFICATION". The Section 1 note says
"B20 is not currently allocated to SP2" — this is inconsistent with the SP2
table, which does allocate B20 to SP2 (sits 9-10) in a pending state.

The substantive protection is in place: sits 9-10 carry the pending flag and
the SP2 table footer explicitly states those sits must be replaced if
flush_danger > 0.20. Design agents reading the SP2 table will see the
pending status before building those situations.

The Section 1 note is technically inaccurate ("not currently allocated to SP2"
when it is allocated but flagged). This is a wording error, not a structural
failure. The risk of an agent misreading this in a dangerous direction (missing
the pending flag) is low because the SP2 table itself is explicit. It should
be corrected in any future edit but does not block design agents.

The Pending Verification Summary lists this as Item C.

---

## Spot-Check Items

### Correction notes below tables

PASS. No correction notes appear below any allocation table. All corrections
have been applied directly to the tables. The document's preamble states
"No correction notes appear below tables" and this holds throughout.

### Section 7 (SPR Revision Log) removed

PASS. The document ends at Section 6 (Distribution Summary Tables) followed
by a Pending Verification Summary. No Section 7 exists. The only references
to Section 7 are in the corrections preamble at line 55 confirming its
removal. Confirmed by search — no "Section 7" heading present in the body.

### Section 8 (Open Items) removed

PASS. No Section 8 exists in the document. The corrections preamble at line
58 confirms its removal. Pending items are now tracked in the Pending
Verification Summary table, which is appropriate — it replaces the open
items section with a structured tracking table rather than an unresolved
discrepancy list.

---

## Additional Observations (not blocking)

**Rainbow texture ceiling:** The Section 4 R2 table shows Rainbow at 35%,
above the 24-32% target ceiling. The document acknowledges this and accepts
it as a marginal overage due to the two new SP2 boards (B30, B31 are both
rainbow). This was not raised in the v1 review because B30/B31 are new.
The overage is 3 percentage points and is self-documented. Not a blocker but
should be noted for the architect if the batch is expanded further.

**Section 1 note inconsistency on B20 SP2 allocation:** Described under
action 10 above. Wording error only — does not affect design agent safety.

**Connected texture still SHORT at 10%:** The R2 table notes connected
boards at 10%, below the 12-16% target, dependent on B22 verification.
This was flagged in the v1 review as marginal. The v2 document correctly
preserves this as a pending item rather than resolving it prematurely.

---

## Summary

| Action | Description | Status |
|--------|-------------|--------|
| 1 | villain_positions fixed on B03, B14, B19, B20, B25, B28 | PASS |
| 2 | SP2 table rewritten with corrected boards at SPR <= 1.5 | PASS |
| 3 | Section 2 summary table updated with revised SPR/stack values | PASS |
| 4 | SP1: sit#17=B01, sit#18=B08, B09 removed | PASS |
| 5 | SP4: sit#6 = B20 with S5 suppressor | PASS |
| 6 | SP3 + B10 collision resolved and documented | PASS |
| 7 | SP10 0.75-0.80 band has 3 situations | PASS |
| 8 | SP7 SPR=9.0 sits marked PENDING GTO | PASS |
| 9 | B22 straight_danger marked PENDING VERIFICATION | PASS |
| 10 | B20 flush_danger marked PENDING VERIFICATION | PASS (wording error in Section 1 note) |
| Spot | No correction notes below tables | PASS |
| Spot | Section 7 revision log removed | PASS |
| Spot | Section 8 open items removed | PASS |

**Verdict: PASS.** All 10 required actions have been applied. The document
is structurally clean. Three items remain in a correctly-marked PENDING
VERIFICATION state — GTO Expert sign-off (SP7 sits 3/9/21), programmer
confirmation of B22 straight_danger, and programmer confirmation of B20
flush_danger for SP2 sits 9-10. These are blocking gates for the affected
situations only, not for the batch overall.

Design agents may proceed using this document. They must not build SP7
sits 3, 9, 21 or SP2 sits 9-10 until the relevant verifications are
complete.
