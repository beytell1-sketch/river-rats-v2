# Independent Review: FOLD Decision Tree v1

**Date:** 9 April 2026
**Reviewer:** Independent Reviewer
**File reviewed:** review/FOLD_DECISION_TREE_V1.md
**Verdict:** PASS (with two minor notes — neither blocks approval)

---

## Checklist Results

### 1. Every branch outputs FOLD or CALL (never frequency)?

PASS. The tree is explicit in its header ("Output: FOLD or CALL — never a frequency").
Every step terminates in FOLD. The default terminates in CALL. No frequencies, no
percentages, no mixed strategies appear anywhere in the branch outputs. Correct.

---

### 2. All feature names real?

PASS. Every feature name used in the five steps and pre-checks was cross-checked
against `feature_keys.py` (class F). All 17 features used in the decision logic
are present in the file:

- `facing_bet`, `is_monster`, `raw_equity`, `pot_odds`, `draw_outs`,
  `overcard_outs`, `is_made_hand`, `has_showdown_value`, `equity_margin`,
  `villain_aggression_count`, `villain_top_pair_plus_pct`, `num_callers_to_bet`,
  `hero_range_percentile`, `board_favour`, `villain_range_capped` — all confirmed.

The Feature Reference Table at the bottom of the document lists 24 features and
every one of them resolves to a real key in feature_keys.py. No invented names,
no stale names from a prior feature set.

---

### 3. Default is CALL?

PASS. The Default section is unambiguous: "No step returned FOLD → CALL."
The preamble also states this: "If no FOLD step fires, the hand defaults to CALL."
Two locations confirm the default. Correct.

---

### 4. Pre-check exits for monsters?

PASS. Pre-check C: `is_monster == 1` exits the tree entirely with output CALL
before any step runs. The Monster Protection Rule block reinforces this with
explicit rationale. All five FOLD steps also include `is_monster == 0` as a
required condition, providing belt-and-suspenders protection: even if the pre-check
were somehow bypassed, no step would fold a monster hand. The Quick Reference
(Hands That CALL) confirms K7 trips on 775-9-J (MW-46) routes through pre-check C.

---

### 5. MW-50 pattern correctly captured?

PASS. Step 3 is built specifically for this pattern. The worked example at the
bottom of the document walks through MW-50 (JcTc on J845, flop raise + turn barrel,
equity_margin 0.04, villain_aggression_count 2, draw_outs 4, villain_top_pair_plus_pct
0.62) step by step and correctly fires Step 3 as FOLD.

The OR gate logic in Step 3 (`has_showdown_value == 0 OR villain_top_pair_plus_pct
>= 0.55`) correctly handles the MW-50 case: JcTc has showdown value (top pair), so
`has_showdown_value == 1`, but villain_top_pair_plus_pct = 0.62 >= 0.55 satisfies
the OR. The step fires. The rationale for nullifying showdown value when the villain
range is this top-pair-heavy is sound.

---

### 6. MW-30 pattern (22pp surplus) correctly passes through to CALL?

PASS. Step 4 requires `equity_margin < 0.10`. MW-30 (KT on KJ6, 40% equity vs 18%
pot odds) has equity_margin = 0.22. This is well above 0.10. Step 4 does not fire.
No other step fires either (Step 1 does not fire because raw_equity > pot_odds; Step 2
does not fire because is_made_hand == 1; Step 3 does not fire without multi-street
aggression at equity_margin 0.22). The hand correctly reaches the Default and outputs
CALL. The Quick Reference (Hands That CALL) explicitly names this pattern and confirms
the mechanism. Correct.

---

### 7. No overlap with RAISE tree logic?

PASS. The Relationship to Other Trees section documents the handoff cleanly. The FOLD
tree runs only after the RAISE tree has confirmed no RAISE. The RAISE tree's Step 1
flat-spot conditions (bet-and-call non-monster, board favouring villain, multi-street
aggressor non-monster) explicitly force CALL-not-RAISE. The FOLD tree then evaluates
those same hands and folds some of them — only when equity is also thin. This is not
overlap; it is a two-stage filter, and the boundary is well defined. BET tree is
entirely separate (applies when `to_call == 0`; FOLD tree requires `facing_bet == 1`).
No logic conflict found.

---

### 8. Three trees together cover all actions?

PASS. The five actions are: BET, CHECK, RAISE, CALL, FOLD.

- BET and CHECK: BET Decision Tree V1 (applies when `to_call == 0`)
- RAISE: RAISE Decision Tree V2 (applies when `facing_bet == 1`, fires RAISE or CALL)
- CALL and FOLD: FOLD Decision Tree V1 (applies when `facing_bet == 1` and RAISE tree
  did not fire RAISE)

The routing is clean. `facing_bet == 1` routes to RAISE tree first, then FOLD tree.
`to_call == 0` routes to BET tree. Together the three trees cover all five actions
with no gaps and no ambiguous overlaps. The only theoretical gap (sandwich position
— no feature exists for it) is handled by RAISE tree's documented fallback to CALL,
and the FOLD tree would then evaluate whether to CALL or FOLD using available features.

---

### 9. equity_margin = raw_equity - pot_odds (confirmed)?

PASS. The Feature Reference Table in the FOLD tree states: `equity_margin | Signed
float (raw_equity − pot_odds)`. This matches the definition in feature_keys.py where
EQUITY_MARGIN = 'equity_margin' is a model feature (present in FEATURE_COLUMNS). The
BET tree also uses equity_margin in "Supporting context" without redefining it. The
RAISE tree's feature reference does not redefine it either. The definition is consistent
across all three trees and the feature file.

---

### 10. Thresholds reasonable for 3-way pots?

PASS on all five steps. Assessment per step:

**Step 1 (raw_equity < pot_odds, draw_outs < 6, overcard_outs < 4):** This is a
mathematically necessary fold — paying more than equity share with no improvement path.
The draw gates are conservative. draw_outs < 6 allows hands with a gutshot (4 outs) to
still trigger the step — that threshold is arguably tight, since a gutshot gives roughly
8% equity on one card (16% on two), which at typical pot odds of 20-30% does not
justify continuing. Acceptable; the overcard gate provides the main protection.

**Step 2 (pure air: is_made=0, draw_outs=0, has_showdown_value=0, overcard_outs < 4):**
Clear fold. No winner path. No issues.

**Step 3 (equity_margin < 0.05, villain_aggression_count >= 2):** 5pp surplus threshold
is appropriate for two-street aggression in a 3-way pot. The KB supports this (MW-50
pattern). The draw_outs < 8 gate (drawn from KB Example 8) is correctly calibrated.

**Step 4 (num_callers >= 1, hero_range_percentile < 0.40, equity_margin < 0.10,
draw_outs < 6):** 10pp surplus threshold is reasonable for bet-and-call with a dominated
hand. The hero_range_percentile < 0.40 proxy is explicitly flagged as imperfect in
Known Limitations. The equity_margin gate prevents the MW-30 trap. Acceptable.

**Step 5 (board_favour <= -0.30, villain uncapped, equity_margin < 0.10, villain_aggression_count >= 1):**
board_favour <= -0.30 is a meaningful threshold — this is a board that strongly
favours villain's range, not a marginal lean. The villain_aggression_count >= 1 gate
correctly requires the board read to be confirmed by action. MEDIUM confidence rating
is appropriate and honest.

---

## Minor Notes (non-blocking)

**Note 1: Step 1 fires on gutshots (draw_outs 4-5) when below pot odds.**

Step 1 requires draw_outs < 6. A gutshot (4 outs) satisfies this gate and will FOLD
when raw_equity < pot_odds. A gutshot provides roughly 8% one-card equity and 16%
two-card equity. If pot odds are, say, 0.25 (25%) and raw_equity is 0.22 (22%), and
the hand is a gutshot with 4 outs, Step 1 fires and folds it. The fold is likely
correct on the turn (one card to come, 8% equity vs 25% required) but may be
marginal on the flop (two cards, 16% vs 25% is a loss but not as decisive). The tree
does not split by street in Step 1. This is a known approximation. The tree's Known
Limitations section acknowledges the positional simplification; street-specific
calibration could be a future revision. Not a correctness error — flag for awareness.

**Note 2: Step 3 and Step 5 both fold hands with thin equity facing villain aggression
or board disadvantage, and can theoretically double-fire on the same hand.**

A hand with equity_margin 0.04, villain_aggression_count 2, draw_outs 4,
has_showdown_value 0 fires Step 3. The same hand would also satisfy Step 5 if
board_favour <= -0.30 and villain_range_capped == 0. In practice this does not matter
because the tree evaluates steps in order and Step 3 would fire first (outputting FOLD)
before Step 5 is reached. The tree is correctly structured for top-down evaluation.
Just noting that both conditions describe overlapping territory — the tree handles
it correctly through ordering, not branching.

---

## Summary

All ten review criteria pass. The tree is logically consistent, feature-complete
against the 53-feature vector, correctly handles all named reference hands (MW-50,
MW-30, MW-46, KB Example 7, KB Example 8), produces only FOLD or CALL, defaults
to CALL, and covers its segment of the action space without overlapping the RAISE
or BET trees.

The two minor notes are flagged for awareness and do not require changes before
approval.

**Verdict: PASS**
