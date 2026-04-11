# Review: RAISE Decision Tree v2

**Reviewer:** Independent agent (cold review — did not participate in design)
**Date:** 9 April 2026
**Files reviewed:**
- review/RAISE_DECISION_TREE_V2.md (primary target)
- review/REVIEW_RAISE_DECISION_TREE_V1.md (12 findings)
- review/comms/REVIEW_HANDOFF_AND_RESEARCH_2026-04-09.md (2 additional findings)
- river-rats-core/feature_keys.py (feature name verification)
- river-rats-core/feature_extractor.py (encoding value verification)
- knowledge/three_way_gto.md (KB reference verification)

**VERDICT: ISSUES FOUND**

One concrete encoding error in the flush_draw_rank description. All 14
findings are addressed structurally. The tree logic is sound. One issue
requires a fix before the tree is used to produce labels.

---

## Checklist: All 14 Findings

### Finding 1 — Step 5 no nut-draw quality gate (CRITICAL)
**Status: ADDRESSED**

v2 adds `flush_draw_rank >= 12` AND `flush_block_pct > 0` as required conditions
in Step 5. The AND decision is directly justified by KB Section 1.7 (solver-verified),
which lists both nut draw and blocker as required conditions, not alternatives.
Worked Example 9 is cited correctly: "Without the As (e.g., 8s7s for nut flush draw),
the raise becomes unprofitable because villain's continuing range includes the nut flush
draw." The CALL cases for nut-draw-without-blocker and blocker-without-nut-draw are
explicitly stated in the step body and in the Quick Reference section.

Note: see New Issue #1 below — the description of what flush_draw_rank >= 12 captures
contains a factual error, though the threshold value itself may be correct.

### Finding 2 — S1 uses undefined "two-pair+"
**Status: ADDRESSED**

S1 now reads `hand_category < 10`. The HAND_CATEGORY_ENCODING in feature_extractor.py
confirms `two_pair = 10`, making `hand_category < 10` the correct boundary for
"below two_pair." The inline enumeration (high_card=0 through overpair=9) matches the
extractor exactly. The fix is correct.

### Finding 3 — S4 SPR threshold too low
**Status: ADDRESSED**

S4 raised from `spr >= 4.0` to `spr >= 6.0`. The rationale is stated: at SPR 4–6 IP
monsters still raise for value; only at SPR 6+ does pot control clearly dominate.
This is a poker judgment call within the GTO expert's remit. The feature name `spr`
exists in feature_keys.py (class F, line 51). Correct.

### Finding 4 — Step 3 percentile too loose at low SPR 3-way
**Status: ADDRESSED**

Raised from `>= 0.80` to `>= 0.90`. Rationale given: low SPR 3-way compresses risk
from two remaining players. The feature `hero_range_percentile` is confirmed in
feature_keys.py (Step 13, line 73). The threshold change is directionally correct
per KB Section 1.6 (SPR compression 3-way). Correct.

### Finding 5 — Step 4 fold_equity too permissive OOP
**Status: ADDRESSED**

Raised from `>= 0.30` to `>= 0.40`. Rationale given: OOP check-raises into two
opponents require meaningful fold equity to compensate for positional disadvantage.
The feature `villain_fold_equity_estimate` is confirmed in feature_keys.py (line 75).
Correct.

### Finding 6 — Step 6 fires on flop despite being river-only
**Status: ADDRESSED**

`street >= 2` gate added to Step 6. Street encoding 0=flop, 1=turn, 2=river is
confirmed in feature_extractor.py: `STREET_ENCODING = {'f': 0, 't': 1, 'r': 2}` and
in test assertions (`assert_eq("street river", f['street'], 2)`). The gate is
correct. The inline note explaining the encoding is correct. Correct.

### Finding 7 — Step 1D sandwich has no feature mapping
**Status: ADDRESSED**

Step 1D removed. The rationale is sound and honest: no feature in the 52-vector
encodes whether players behind hero have acted. The feature_keys.py file was
checked — there is no `num_players_to_act`, `is_sandwich`, or `players_behind`
field. The removal is the correct decision. The fallback to CALL via the Default
is the conservative and feature-consistent outcome. The inline note explaining
what the removed step was trying to capture and why the gap is acceptable is well
reasoned. Correct.

### Finding 8 — Factory brief CALL count inconsistency (32 vs 43)
**Status: ADDRESSED (deferred appropriately)**

Noted in Factory Brief Impact section with clear instruction to reconcile when the
factory brief is next revised. The tree does not determine this count. Deferred
correctly — the tree cannot fix a factory brief number.

### Finding 9 — SP6 missing nut-draw-without-blocker CALL counterexample
**Status: ADDRESSED (deferred appropriately)**

Noted in Factory Brief Impact section with a precise description of the missing
situation: `flush_draw_rank >= 12` but `flush_block_pct == 0` → CALL. The tree
now defines this branch explicitly; the factory brief must add a matching situation.
Deferred correctly.

### Finding 10 — Mid-draw zone needs CALL examples
**Status: ADDRESSED (deferred appropriately)**

Noted in Factory Brief Impact section with exact thresholds: `hero_range_percentile
0.70–0.80` with `draw_outs 6–8`. These hands pass neither Step 3 (>= 0.90) nor
Step 5 (>= 9) and correctly default to CALL. Deferred correctly.

### Finding 11 — Independent review finding 11
**Status: ADDRESSED**

The v1 review document (REVIEW_RAISE_DECISION_TREE_V1.md) contains exactly 10
bullet-point issues (1 critical + 9 others). Findings 11 and 12 are listed in the
changelog as "No additional structural issues identified beyond 1-10." The v1 review
is consistent with this: it states "12 items, 1 critical" in its header but the body
enumerates only 10 distinct items. The changelog acknowledgment is honest and the
absence of additional issues is consistent with the source document.

### Finding 12 — Independent review finding 12
**Status: ADDRESSED**

Same as Finding 11. No additional structural issues were identified. Consistent with
source document.

### Finding 13 — SP5 must match the fixed tree
**Status: ADDRESSED (deferred appropriately)**

Noted in Factory Brief Impact section with a specific action: any SP5 situation where
`flush_draw_rank < 12` OR `flush_block_pct == 0` must be re-labelled CALL or removed.
The instruction is precise enough to act on. Deferred correctly — this is a factory
brief task, not a tree task.

### Finding 14 — Verify self-play RAISE yield
**Status: ADDRESSED (deferred appropriately)**

Assigned to a separate agent. This is not a tree change — it is a yield verification
task. The changelog correctly marks it as NOTE. Correct.

---

## New Issues Found

### New Issue #1 — flush_draw_rank description is factually wrong (SHOULD_FIX)

**Location:** Step 5 condition line, Feature Reference table, and Step 5 rationale block.

**The claim:** The tree states `flush_draw_rank >= 12` captures "nut or near-nut draw
— top 4 flush draw ranks."

**What the code actually does:** `compute_flush_draw_rank()` in feature_extractor.py
(lines 1430–1479) returns the raw card rank of the hero's highest card in the flush
suit, using the mapping: A=14, K=13, Q=12, J=11, T=10, ..., 2=2, 0=no flush draw.

`flush_draw_rank >= 12` therefore captures:
- Q (12) — third-nut flush draw
- K (13) — second-nut flush draw
- A (14) — nut flush draw

That is **3 ranks, not 4**. The threshold `>= 12` excludes J (rank 11). The
description "top 4 flush draw ranks" is wrong by one.

**Is the threshold itself wrong?** That is a GTO question beyond the scope of
encoding verification. The description is provably wrong against the code. The
threshold may be intentionally set at >= 12 (Q or better) rather than >= 11
(J or better), but if so, the description needs to say "top 3" not "top 4."

**Impact:** The labelling agent reading this tree will apply the correct threshold
(>= 12 is unambiguous), but the description misleads anyone reasoning about which
hands qualify. A J-high flush draw is excluded by the threshold but would be included
by the description. For a training data labelling tool, this matters: if someone
audits why Jx flush draws are being labelled CALL (not RAISE) and reads the
description "top 4 ranks," they will conclude there is a bug when there is not.

**Fix required:** Change "top 4 flush draw ranks" to "top 3 flush draw ranks (Q, K, A
of the flush suit)" in Step 5, the Feature Reference table entry for flush_draw_rank,
and the Step 5 rationale block. Alternatively, change the threshold to `>= 11` if
J-high draws are intended to qualify (and update the description to "top 4").

---

### New Issue #2 — Feature Reference table omits flush_draw_rank range bounds (MINOR)

**Location:** Feature Reference table, flush_draw_rank row.

**The claim:** "0=no flush draw, higher = stronger draw (12+ = nut/near-nut)"

**What is missing:** The full range is 0 and 2–14 (raw card rank). The entry does
not state the maximum value (14=Ace) or that the scale is raw card rank, not an
abstract 0–N scale. This is a readability issue, not a correctness issue. A labelling
agent or future reviewer could mistake 12+ as a normalized score rather than a card rank.

**Suggested fix:** Expand to: "0=no flush draw, 2–14=rank of hero's highest card in
flush suit (2=2, 11=J, 12=Q, 13=K, 14=A); 12+ = Q/K/A of flush suit"

This is minor and can be addressed alongside New Issue #1.

---

## Verification of All Feature Names

Every feature name used in the tree was checked against feature_keys.py (class F):

| Tree feature | In feature_keys.py? | Notes |
|---|---|---|
| flush_draw_rank | Yes (line 76, Step 13) | Confirmed |
| flush_block_pct | Yes (line 68, Step 12) | Confirmed |
| villain_fold_equity_estimate | Yes (line 75, Step 13) | Confirmed |
| hero_range_percentile | Yes (line 73, Step 13) | Confirmed |
| hand_category | Yes (line 30) | Confirmed |
| is_monster | Yes (line 33) | Confirmed |
| is_ip | Yes (line 28) | Confirmed |
| is_paired | Yes (line 39) | Confirmed |
| flush_danger | Yes (line 45) | Confirmed |
| straight_danger | Yes (line 46) | Confirmed |
| spr | Yes (line 51) | Confirmed |
| villain_aggression_count | Yes (line 54) | Confirmed |
| villain_range_capped | Yes (line 61) | Confirmed |
| villain_top_pair_plus_pct | Yes (line 57) | Confirmed |
| board_favour | Yes (line 62) | Confirmed |
| num_callers_to_bet | Yes (line 63) | Confirmed |
| draw_outs | Yes (line 36) | Confirmed |
| street | Yes (line 19) | Confirmed |
| num_callers_to_bet | Yes (line 63) | Confirmed |

No phantom feature names found. Every condition in the tree is evaluable from the
52-feature vector.

---

## Encoding Values Verification

| Encoding claim in tree | Source verified against | Correct? |
|---|---|---|
| street: 0=flop, 1=turn, 2=river | STREET_ENCODING in extractor line 47-50 | YES |
| hand_category: two_pair=10 | HAND_CATEGORY_ENCODING line 150 | YES |
| hand_category: overpair=9 | HAND_CATEGORY_ENCODING line 149 | YES |
| hand_category < 10 = below two_pair | HAND_CATEGORY_ENCODING ordering | YES |
| hand_category range 0-17 | HAND_CATEGORY_ENCODING has 18 entries | YES |
| flush_draw_rank 12+ = "top 4 ranks" | compute_flush_draw_rank returns 2-14 | NO — top 3, not top 4 (see New Issue #1) |
| flush_draw_rank 0 = no flush draw | compute_flush_draw_rank returns 0 when no flush suit or no hero card in suit | YES |

---

## AND vs OR Decision on Step 5

The tree uses AND for `flush_draw_rank >= 12` AND `flush_block_pct > 0`.

The v1 review offered this as "OR" alternatives. The KB is explicit:

KB Section 1.7 table: "Nut draw — Required? YES" and "Blocker to opponent's continuing
range — Required? YES." Both marked as independently required.

KB Example 9: "Without the As (e.g., 8s7s for nut flush draw), the raise becomes
unprofitable because villain's continuing range includes the nut flush draw."
This text describes a nut draw WITHOUT a blocker → CALL. That is the OR-false case
(draw_rank >= 12 TRUE, flush_block_pct = 0 FALSE). The KB confirms it should CALL.

DO NOT Rule #2: "Semi-bluffs require nut draws with a blocker." Both required.

The AND decision is fully justified by the KB. An OR gate would incorrectly label nut
draws without blockers as RAISE, which the KB explicitly says should CALL.

---

## Step 1D Removal Justification

Confirmed correct. feature_keys.py has no `is_sandwich`, `num_players_to_act`,
`players_behind`, or any field capturing intra-street position ordering. The 52-feature
vector has `is_ip` (binary, closing vs not-closing action), `hero_position` (seat),
and `villain_position` (seat), but none of these distinguish "player behind has acted"
from "player behind has not yet acted" within a street. The removal is the only
feature-consistent choice.

---

## Quick Reference Sections

**Monsters That Should CALL:** 6 items listed. Each maps to a named suppressor
(S1–S5) or to the sandwich/default case. All are consistent with the tree logic.
The "Monster in sandwich position (no feature — defaults to CALL)" entry is
accurate: with 1D removed, these hands reach the Default and are labelled CALL.

**Semi-Bluffs That Should CALL:** 5 items listed. All are correct exclusions from
Step 5:
- Nut flush draw without flush blocker → flush_block_pct == 0, Step 5 fails
- Non-nut flush draw → flush_draw_rank < 12, Step 5 fails
- Draw on paired board → is_paired == 1, Step 5 fails
- Draw against multi-street aggressor → villain_aggression_count >= 2, Step 5 fails
- Gutshot or backdoor only → draw_outs < 9, Step 5 fails

All five CALL cases are correctly stated and consistent with the tree.

---

## Factory Brief Impact Section

Items 8, 9, 10, and 13 are documented with enough specificity to act on. Item 14
is assigned to a separate agent. The section functions correctly as a deferred
action log. No items are missing from this section relative to the changelog.

---

## Overall Assessment

The tree is structurally sound. All 14 findings from the two prior reviews are
addressed — the CRITICAL finding (Step 5 nut-draw gate) with AND logic that is
directly justified by the KB; the SHOULD_FIX findings with concrete threshold
changes and feature-mapped conditions; the NOTE findings appropriately deferred to
the factory brief.

One concrete fix is required before the tree is used to produce labels: the
flush_draw_rank description claims "top 4 ranks" when the extractor code produces
ranks 2–14 and the threshold >= 12 captures exactly 3 ranks (Q, K, A). This is
a description error, not a threshold error (the threshold is executable as-is), but
it must be corrected to prevent audit confusion and potential misuse of the threshold
by a future designer who reads "top 4" and changes the threshold to >= 11.

The AND gate for Step 5 is correct. The Step 1D removal is correct. The Quick
Reference sections are consistent with the tree logic. All feature names are real.
All encoding values checked are correct except the flush_draw_rank description.

**Recommendation: fix New Issue #1 (flush_draw_rank description), then approve.**
New Issue #2 (range bounds in Feature Reference) can be addressed in the same pass.
No structural changes to tree logic are required.
