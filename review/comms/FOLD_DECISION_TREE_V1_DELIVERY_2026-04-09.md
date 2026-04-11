# FOLD Decision Tree V1 — Delivery Confirmation

**Date:** 9 April 2026
**From:** GTO Expert
**To:** Owner / Reviewer
**Re:** FOLD_DECISION_TREE_V1.md — delivery and notes

---

## Delivery

File written to: `/home/rupertbeytell/river-rats-v2/review/FOLD_DECISION_TREE_V1.md`

Status: AWAITING REVIEW + OWNER APPROVAL

---

## What Was Built

A FOLD vs CALL decision tree that runs after the RAISE tree returns no RAISE. Five
sequential steps encode the specific patterns from the KB and task brief that produce
FOLD. Default is CALL. No frequencies are output.

### The five FOLD steps

1. **Equity Below Pot Odds** — raw_equity < pot_odds with no draw and no overcard equity.
   The clearest possible fold. Gates prevent folding AK/AQ (hidden overcard equity).

2. **Pure Air** — no made hand, no draw, no showdown value, fewer than 4 overcard outs.
   Definitional air facing a bet has no path to winning.

3. **Thin Equity + Multi-Street Aggression** — equity_margin < 0.05 AND
   villain_aggression_count >= 2. The MW-50 pattern (JcTc on J845, 4pp surplus
   overwhelmed by range narrowing). Draw gate at draw_outs < 8 preserves calls for
   KB Example 8 hands (OESD survives aggression).

4. **Bet-and-Call Dominated Made Hand** — num_callers_to_bet >= 1 AND
   hero_range_percentile < 0.40 AND equity_margin < 0.10. Applies the MW-30 corrected
   teaching: the 22pp surplus of KT on KJ6 calls; only hands with < 10pp surplus and
   bottom-40% range percentile fold. Draw gate at draw_outs < 6.

5. **Board Heavily Favours Uncapped Villain** — board_favour <= -0.30 AND
   villain_range_capped == 0 AND equity_margin < 0.10 AND villain_aggression_count >= 1.
   The villain must have bet (not just check-backed on a board that favours them) for
   this step to fire.

---

## Key Design Decisions

**MW-30 correction fully applied.** The original MW-30 reasoning (bet-and-call = fold
despite equity) was over-applied. The KB correction is explicit: fold only when equity
is close to break-even AND the holding is dominated. Step 4 enforces equity_margin <
0.10 AND hero_range_percentile < 0.40. KT on KJ6 (22pp surplus) correctly bypasses
Step 4 and calls.

**Draw equity protection is consistent across steps.** Steps 3, 4, and 5 all have
draw_outs gates. The thresholds differ (8, 6, 6 respectively) reflecting the KB's
teaching: 8+ outs survive multi-street aggression (KB Example 8 sets this ceiling),
6+ outs survive bet-and-call and board-favour signals.

**Monster pre-check prevents any FOLD for monsters.** is_monster == 1 exits the
tree before any step. This matches the task brief requirement: "monsters always call
at minimum, RAISE tree handles the raise question."

**Tree is shorter than RAISE and BET trees.** Five steps vs six (RAISE) and seven (BET).
FOLD/CALL is a simpler decision — the task brief noted this explicitly and the design
reflects it.

---

## Concerns and Open Questions

**Q1: equity_margin encoding.** The tree assumes equity_margin = raw_equity - pot_odds
(signed float, positive = above pot odds). This must match feature_keys.py and the
actual extractor. If the encoding differs, Steps 3, 4, and 5 thresholds need adjustment.
Reviewer should verify feature_extractor.py computes equity_margin this way.

**Q2: Step 5 confidence is MEDIUM.** board_favour is a range-level metric that does
not know which specific hands villain holds. The step is directionally correct but the
threshold of -0.30 is based on the RAISE tree's Step 1B (which uses the same threshold
for a different purpose). If the reviewer has solver data suggesting a different
board_favour threshold is appropriate for FOLD decisions, it should be updated.

**Q3: Positional differentiation not encoded.** OOP hands under-realize equity relative
to IP (KB Section 1.5). The tree folds at the same equity_margin thresholds regardless
of position. This is a known approximation documented in the Limitations section. A
future revision could split Steps 3 and 4 by is_ip with tighter thresholds OOP.

**Q4: villain_aggression_count gate in Step 5.** Requiring >= 1 aggressive action
means a villain who is in a check-back-then-bet sequence on turn fires Step 5. A
villain who checks back on a board that favours their range may be trapping or holding
a specific subset — the board_favour signal alone without a bet is insufficient. The
gate is correct in principle but the count-based feature may catch some check-then-bet
sequences as intended.

---

## Files Produced

- `/home/rupertbeytell/river-rats-v2/review/FOLD_DECISION_TREE_V1.md` — main deliverable
- `/home/rupertbeytell/river-rats-v2/review/comms/FOLD_DECISION_TREE_V1_DELIVERY_2026-04-09.md` — this file
