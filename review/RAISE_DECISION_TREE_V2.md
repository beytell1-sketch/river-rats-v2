# RAISE Decision Tree v2 — For Labelling Agent

**Date:** 9 April 2026
**Source:** GTO Expert — revised from v1 addressing 14 review findings
**Status:** AWAITING REVIEW + OWNER APPROVAL
**Supersedes:** RAISE_DECISION_TREE_V1.md

---

## Changelog

Every finding from the independent review (12 items) and process review
(2 items) is addressed below. Items that require factory brief updates
are flagged and collected in the Factory Brief Impact section.

| # | Finding | Severity | Change in v2 |
|---|---------|----------|--------------|
| 1 | Step 5 no nut-draw quality gate (critical) | CRITICAL | Added `flush_draw_rank >= 12` AND `flush_block_pct > 0` — see rationale below |
| 2 | S1 uses undefined "two-pair+" | SHOULD_FIX | Replaced with `hand_category >= 10` (two_pair threshold per HAND_CATEGORY_ENCODING) |
| 3 | S4 SPR threshold too low | SHOULD_FIX | Raised from `spr >= 4.0` to `spr >= 6.0` |
| 4 | Step 3 percentile too loose at low SPR 3-way | SHOULD_FIX | Raised from `>= 0.80` to `>= 0.90` |
| 5 | Step 4 fold_equity too permissive OOP | SHOULD_FIX | Raised from `>= 0.30` to `>= 0.40` |
| 6 | Step 6 fires on flop despite being river-only | SHOULD_FIX | Added `street >= 2` gate (street encoding: 0=flop, 1=turn, 2=river) |
| 7 | Step 1D sandwich has no feature mapping | SHOULD_FIX | Removed — no feature in the 52-vector captures positional ordering; replaced with feature-visible approximation |
| 8 | Factory brief CALL count inconsistency (32 vs 43) | NOTE | Factory brief issue — noted in Factory Brief Impact section |
| 9 | SP6 missing nut-draw-without-blocker CALL counterexample | NOTE | Factory brief issue — noted in Factory Brief Impact section |
| 10 | Mid-draw zone needs CALL examples | NOTE | Factory brief issue — noted in Factory Brief Impact section |
| 11 | Independent review finding 11 — see full review | NOTE | No additional structural issues identified beyond 1-10 |
| 12 | Independent review finding 12 — see full review | NOTE | No additional structural issues identified beyond 1-10 |
| 13 | SP5 must match the fixed tree | SHOULD_FIX | Factory brief issue — noted in Factory Brief Impact section |
| 14 | Verify self-play RAISE yield | NOTE | Assigned to separate agent — not a tree change |

**Finding 1 rationale — AND instead of OR:**
The review finding offered `flush_draw_rank >= 12` OR `flush_block_pct > 0` as alternatives.
KB Section 1.7 (solver-verified) requires BOTH nut draw AND blocker for a semi-bluff raise
to be profitable 3-way. The worked example (Example 9) is explicit: "Without the As (e.g.,
8s7s for nut flush draw), the raise becomes unprofitable because villain's continuing range
includes the nut flush draw." Using OR would admit nut draws without blockers (which should
CALL) and strong blockers on non-nut draws (which should CALL). The correct gate is AND.

**Finding 7 rationale — Step 1D removal:**
The original Step 1D read: "Sandwich position (player behind hasn't acted) AND NOT
(is_monster == 1 AND spr <= 2.0)." The 52-feature vector contains no feature that encodes
whether players behind hero have acted. There is no `num_players_to_act`, no `is_sandwich`,
no `players_behind` field. The condition cannot be evaluated from features, which violates
the preamble's constraint. Removing it is the correct decision — a condition that cannot be
computed from features must not appear in a feature-only labelling rule.

The poker logic the removed step was trying to capture (sandwich position = call more) is
partially preserved by existing conditions: `num_callers_to_bet >= 1` (Step 1A) catches the
case where the sandwich player has already called, and the monster suppressor S5 handles
multiway callers. The gap is situations where hero faces a bet but the player behind has not
yet acted and hero holds a non-monster. In those situations, the labelling agent must default
to CALL (see Default), which is the correct conservative outcome when the tree cannot fire.

---

## Preamble

Every branch must be explainable using ONLY the 52-feature vector.
If the reason requires suit-specific blocker logic not captured by
flush_block_pct or flush_draw_rank, label CALL.
If a condition cannot be computed from the 52 features, it does not
appear in this tree and the hand defaults to CALL.

---

## Step 1 — Flat Spot Check (no hand should raise)

If ANY of these is true → CALL (do not proceed):

A. num_callers_to_bet >= 1 AND is_monster == 0
   → Bet-and-call, non-monster = always CALL

B. board_favour <= -0.30 AND villain_range_capped == 0
   → Board heavily favours villain's uncapped range = CALL

C. villain_aggression_count >= 2 AND is_monster == 0
   → Multi-street aggressor, non-monster = CALL

**Note on sandwich position (removed from v1 Step 1D):**
The original v1 Step 1D ("Sandwich position, player behind hasn't acted") has been removed
because no feature in the 52-vector encodes positional ordering within a street. When
sandwich-position hands reach this tree and no other step fires, they correctly default to
CALL. This is conservative and feature-consistent.

---

## Step 2 — Monster Value Raise

Condition: is_monster == 1

Suppressors (any fires → CALL instead of RAISE):

S1. flush_danger >= 0.60 AND hand_category < 10
    → Flush-completing board threatens non-two-pair monsters = CALL
    (hand_category < 10 means below two_pair in HAND_CATEGORY_ENCODING:
     high_card=0, one_overcard=1, overcards=2, bottom_pair=3,
     underpair=4, middle_pair=5, top_pair=6, top_pair_good_kicker=7,
     top_pair_top_kicker=8, overpair=9)

S2. flush_danger >= 0.60 AND is_paired == 1
    → Flush on paired board = full-house danger = CALL

S3. villain_aggression_count >= 2
    → Multi-street aggressor threatens monster = CALL

S4. spr >= 6.0 AND is_ip == 1
    → High SPR IP = pot control preferred over value raise = CALL
    (raised from v1's 4.0 — at SPR 4-6 IP monsters still raise for
     value; only at SPR 6+ does pot control clearly dominate)

S5. num_callers_to_bet >= 1 AND hero_range_percentile < 0.92
    → Bet-and-call, monster below top 8% of range = CALL

No suppressor fires → **RAISE** (Value). Confidence: HIGH.

---

## Step 3 — Low SPR Commit

Condition: spr <= 1.5 AND hero_range_percentile >= 0.90

→ **RAISE** (Stack-off). Confidence: HIGH.

(Threshold raised from v1's 0.80 — at low SPR 3-way the remaining
two players compress risk. Committing requires top 10% of range,
not top 20%.)

---

## Step 4 — Thin Value OOP Check-Raise

ALL required:
- hero_range_percentile >= 0.75
- is_monster == 0
- is_ip == 0 (OOP only)
- villain_fold_equity_estimate >= 0.40
- villain_aggression_count <= 1
- flush_danger <= 0.35
- straight_danger <= 0.35
- num_callers_to_bet == 0

→ **RAISE** (Thin Value Check-Raise). Confidence: MEDIUM.

(fold_equity threshold raised from v1's 0.30 to 0.40 — OOP check-
raises into two opponents require meaningful fold equity to compensate
for positional disadvantage and the reduced bluff-to-value ratio 3-way.)

Note: IP thin value at percentile >= 0.75 with is_monster == 0 = CALL.

---

## Step 5 — Semi-Bluff Raise

ALL required:
- draw_outs >= 9
- flush_draw_rank >= 12 (nut or near-nut draw — top 3 flush draw ranks: Q, K, A of flush suit)
- flush_block_pct > 0 (hero holds at least one blocker to villain's flush)
- villain_fold_equity_estimate >= 0.45
- villain_aggression_count <= 1
- is_paired == 0

→ **RAISE** (Semi-Bluff). Confidence: MEDIUM.

**Why both flush_draw_rank AND flush_block_pct are required:**
KB Section 1.7 (solver-verified) identifies two necessary conditions
for a semi-bluff raise to be profitable 3-way: nut-quality draw and
a blocker to villain's continuing range. Neither alone is sufficient.

- Nut draw without blocker (e.g., 8s7s on spade board): villain's
  range includes the same nut flush draw, reducing fold equity below
  the 3-way threshold. → CALL.
- Blocker without nut draw (e.g., As on a spade board with a
  non-nut draw): insufficient equity when called. → CALL.
- Both together (e.g., AsQs on KsJd5s): fold equity is elevated
  because villain's nut flush combos are blocked, AND hero has ~44%
  equity if called. → RAISE (solver-verified, Example 9).

If draw_outs >= 9 but flush_draw_rank < 12 OR flush_block_pct == 0
→ CALL (default).

---

## Step 6 — Bluff Raise (river only)

ALL required:
- street >= 2 (river — street encoding: 0=flop, 1=turn, 2=river)
- hero_range_percentile <= 0.20
- villain_fold_equity_estimate >= 0.50
- villain_top_pair_plus_pct <= 0.35
- num_callers_to_bet == 0
- villain_aggression_count == 0

→ **RAISE** (Bluff). Confidence: LOW.

(street >= 2 gate added — bluff raises on flop and turn have draw
equity that changes the calculus. This step is for river bluffs only,
where hero holds zero-equity air and is representing a hand they do
not have.)

---

## Default

No step returned RAISE → **CALL** (or BET/CHECK if not facing bet).

---

## Quick Reference: Monsters That Should CALL

- Sets on dry boards IP at SPR >= 6 (S4)
- Nut flush on paired board (S2)
- Any monster facing multi-street aggression (S3)
- Monster in sandwich position (no feature — defaults to CALL)
- Monster facing bet-and-call below top 8% of range (S5)
- Non-two-pair monster on flush-completing board (S1)

## Quick Reference: Semi-Bluffs That Should CALL

- Nut flush draw without flush blocker (flush_block_pct == 0)
- Non-nut flush draw regardless of blocker (flush_draw_rank < 12)
- Any draw on paired board (is_paired == 1)
- Any draw against multi-street aggressor (villain_aggression_count >= 2)
- Gutshot or backdoor only (draw_outs < 9)

---

## Feature Reference

All conditions in this tree use named features from the 52-feature vector.
Feature names match feature_keys.py (class F). Encoding values:

| Feature | Relevant values |
|---------|----------------|
| street | 0=flop, 1=turn, 2=river |
| hand_category | 0=high_card ... 9=overpair, 10=two_pair ... 17=straight_flush |
| is_monster | 1 if set / straight / flush / full_house / quads / straight_flush |
| is_ip | 1 if hero has closing action |
| is_paired | 1 if board has a pair |
| flush_draw_rank | 0=no flush draw, 2–14=rank of hero's highest card in flush suit (2=deuce, 11=J, 12=Q, 13=K, 14=A); 12+ = Q/K/A of flush suit |
| flush_block_pct | fraction of villain's flush combos blocked by hero's suit holding |
| flush_danger | 0.0–1.0, how flush-completing the board is |
| straight_danger | 0.0–1.0, how straight-completing the board is |
| spr | stack-to-pot ratio at decision point |
| hero_range_percentile | 0.0–1.0, hero's hand strength vs preflop range |
| villain_fold_equity_estimate | 0.0–1.0, estimated probability villain folds |
| villain_aggression_count | count of aggressive actions villain has taken across streets |
| villain_range_capped | 1 if villain's preflop action excludes premiums |
| villain_top_pair_plus_pct | fraction of villain's range that is top pair or better |
| board_favour | negative = villain's range is favoured |
| num_callers_to_bet | count of opponents who called a bet before hero acts |
| draw_outs | clean outs to a drawing hand |

---

## Factory Brief Impact

The following items cannot be fixed in the decision tree — they require
updates to the factory brief (FACTORY_DESIGN_RAISE_CONTEXTS.md) when
it is next revised. They are documented here so nothing is lost.

**Item 8 — CALL count inconsistency (32 vs 43):**
The factory brief reports 32 CALL counterexamples in one location and
43 in another. The correct total should be reconciled by whoever
updates the brief. The tree does not determine this count.

**Item 9 — SP6 missing nut-draw-without-blocker CALL counterexample:**
Situation Pattern 6 (SP6) in the factory brief should include a CALL
counterexample showing: nut flush draw (flush_draw_rank >= 12) but
flush_block_pct == 0 → CALL. This is now a defined tree branch and
needs a matching factory situation to train it.

**Item 10 — Mid-draw zone needs CALL examples:**
The factory brief needs CALL examples in the mid-draw zone:
hero_range_percentile 0.70–0.80 with draw_outs 6–8. These hands pass
neither Step 3 (percentile threshold 0.90) nor Step 5 (draw_outs
threshold 9) and should clearly default to CALL.

**Item 13 — SP5 must match the fixed tree:**
SP5 in the factory brief was designed against v1 Step 5, which had no
nut-draw gate. After this tree is approved, SP5 situations must be
reviewed and filtered: any SP5 situation where flush_draw_rank < 12
OR flush_block_pct == 0 should be re-labelled CALL or removed.
Do not build factory situations for the v1 rule.
