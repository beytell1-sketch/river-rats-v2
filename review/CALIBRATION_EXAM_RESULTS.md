# Calibration Exam Results — 3-Way Labelling Agent v1.0

**Date:** 6 April 2026
**Agent:** gto_labeller_v1.md + three_way_gto.md v1.0
**Model used for agents:** Sonnet (via subagent dispatch)

---

## Score

| Metric | Result | Gate | Status |
|--------|--------|------|--------|
| Overall accuracy | **20/24 (83.3%)** | >= 20/24 | **PASS** |
| GTO-reversal hands | **3/3 (100%)** | 3/3 | **PASS** |
| **GATE** | | | **PASSED** |

---

## Full Results

| Hand | Expert | Agent | Correct | Agent Confidence | Notes |
|------|--------|-------|---------|-----------------|-------|
| MW-12 | CHECK | CHECK | Y | HIGH | |
| MW-13 | CHECK | CHECK | Y | HIGH | |
| MW-14 | CALL | CALL | Y | HIGH | |
| MW-15 | CHECK | CHECK | Y | HIGH | |
| MW-17 | CALL | FOLD | **N** | HIGH | Agent folded AK with overcards — missed overcard equity |
| MW-18 | CALL | CALL | Y | HIGH | |
| MW-19 | BET | BET | Y | HIGH | |
| MW-23 | BET | BET | Y | MEDIUM | |
| MW-24 | BET | CHECK | **N** | HIGH | Agent defaulted to OOP pot control with TPSK |
| MW-27 | BET | BET | Y | HIGH | |
| MW-28 | BET | CHECK | **N** | HIGH | Agent defaulted to OOP pot control with overpair |
| MW-30 | FOLD | FOLD | Y | HIGH | **REVERSAL** — bet-and-call reasoning correct |
| MW-33 | RAISE | RAISE | Y | HIGH | **REVERSAL** — set must raise vs bet+call |
| MW-34 | BET | BET | Y | HIGH | |
| MW-35 | CALL | CALL | Y | HIGH | |
| MW-36 | CALL | CALL | Y | MEDIUM | |
| MW-37 | CALL | CALL | Y | HIGH | |
| MW-38 | CALL | CALL | Y | HIGH | |
| MW-39 | CALL | CALL | Y | MEDIUM | |
| MW-41 | CALL | FOLD | **N** | HIGH | Agent over-respected double barrel |
| MW-44 | CALL | CALL | Y | MEDIUM | |
| MW-48 | CHECK | CHECK | Y | HIGH | |
| MW-49 | BET | BET | Y | HIGH | |
| MW-50 | FOLD | FOLD | Y | HIGH | **REVERSAL** — action history override correct |

---

## Failure Analysis

### MW-17: Expert=CALL, Agent=FOLD (AKo on Jd8d4c, facing 33 into 90)

**Agent reasoning:** "Equity 24.85% below pot odds 26.83%, no made
hand, no draw."

**Why wrong:** AK has 6 overcard outs (3 aces + 3 kings) that the
`draw_outs` feature doesn't capture (it counts flush/straight draws,
not overcards). The expert labels CALL because AK's overcards to top
pair represent ~24% equity to improve, and when hero hits, the hand
is likely best. The pot odds are close enough that overcard equity
tips the decision.

**Knowledge base gap:** No guidance on overcard equity. The agent
treats "no draw" as "no improvement potential." Need a worked example
showing overcards as hidden equity.

### MW-24: Expert=BET, Agent=CHECK (QJ on Q83r, SB OOP)

**Agent reasoning:** "OOP with TPSK against uncapped opener. Betting
folds worse and gets called by better."

**Why wrong:** The expert says BET because despite OOP, QJ on Q83r
has 60% equity and 88% worse hands. The board is dry and static —
hero's hand is unlikely to be outdrawn. The villain's uncapped range
has QQ+/AK but the vast majority is worse. The OOP penalty doesn't
override the value from betting when so many worse hands call.

**Knowledge base gap:** The DO NOT rules and worked examples
over-emphasize OOP pot control. The agent learned "OOP = check" too
strongly. Need examples showing OOP value betting IS correct when
equity is high and worse_hand_pct is very large.

### MW-28: Expert=BET, Agent=CHECK (JJ on 962r, SB OOP)

**Agent reasoning:** "OOP against uncapped opener with QQ+/AK in
range. AA checks 80% OOP on dry boards."

**Why wrong:** Same pattern as MW-24. JJ on 962r has 56% equity,
92% worse hands. The board is below the top of the opener's range
(no overcards above J), so hero's overpair is less likely to be
dominated than the agent assumed. The AA-checks-80% reference
data was over-applied — AA on 842 in a 3-bet pot is a different
spot than JJ on 962 in a single-raised pot.

**Knowledge base gap:** The agent over-indexed on the "AA checks
80% OOP" data point without distinguishing the context (3-bet pot
with deep SPR vs single-raised pot). Need a worked example showing
when OOP betting IS correct: high equity + very high worse_hand_pct
+ dry board + the hand is near the top of hero's range.

### MW-41: Expert=CALL, Agent=FOLD (QT on KQJ7, facing 60 into 200)

**Agent reasoning:** "Double barrel into two opponents, 63% TP+,
only 4% air. Multi-street aggression = strong range. Equity barely
exceeds pot odds against full range, much worse against narrowed
range."

**Why wrong:** The agent correctly identified the aggression signal
but over-applied the "action history overrides equity" rule. QT
here has second pair + an 8-out straight draw (any T or A makes a
straight). The 8 draw outs are significant — combined with the
26.7% raw equity exceeding 23.1% pot odds, this is a profitable
call even against a somewhat narrowed range. The agent treated this
like MW-30 (dominated with no outs) when it's actually a call with
draw equity.

**Knowledge base gap:** The agent can't distinguish "dominated with
no outs" (MW-30, correct fold) from "behind but with significant
draw equity" (MW-41, correct call). Need a worked example showing
that multi-street aggression narrows ranges but doesn't eliminate
the call when hero has substantial draw outs.

---

## By Confidence

| Confidence | Correct | Total | Accuracy |
|-----------|---------|-------|----------|
| HIGH | 17/20 | 20 | 85.0% |
| MEDIUM | 3/4 | 4 | 75.0% |
| LOW | 0/0 | 0 | N/A |

All 4 failures were labelled HIGH confidence — the agent was
confidently wrong. This is the calibration problem: overconfidence
on spots where the knowledge base created blind spots.

---

## Reversal Hands

| Hand | Expert | Agent | Pattern | Correct |
|------|--------|-------|---------|---------|
| MW-30 | FOLD | FOLD | bet-and-call | **YES** |
| MW-33 | RAISE | RAISE | set must raise vs bet+call | **YES** |
| MW-50 | FOLD | FOLD | flop raiser bets turn | **YES** |

All 3 reversal hands correct with strong reasoning. The agent
successfully applied action-history-overrides-equity in all three
cases. This is the core 3-way skill and the agent has it.

---

## Knowledge Base v1.1 Changes Needed

To fix the 4 failures, add these worked examples:

1. **Overcard equity example:** AK on a missed board where overcards
   represent hidden outs not captured by draw_outs. Show that "no
   draw" doesn't mean "no improvement potential."

2. **OOP value betting example:** Strong hand (60%+ equity, 85%+
   worse_hand_pct) on a dry board OOP where betting IS correct
   despite position. Show that the OOP pot-control default has
   exceptions when equity and worse_hand_pct are both very high.

3. **Multi-street aggression WITH draw equity example:** Second pair
   + straight draw facing a double barrel. Show that the action-
   history-overrides-equity rule applies to dominated hands without
   outs (MW-30), but NOT to hands with significant draw equity.

These are additive — principles stay stable, examples accumulate.
v1.0 → v1.1 following the iteration model.

---

## Summary

The agent passed the calibration gate: 20/24 (83.3%) with all 3
reversal hands correct. The 4 failures are diagnosable and fixable
through worked example additions. The factor-weighting framework
worked — the agent correctly reasoned through factor interactions
on 20 hands. The failures are where the knowledge base created
blind spots (overcard equity, OOP betting exceptions, draw equity
vs aggression).

**Recommendation:** Proceed to labelling training data with v1.0.
The 4 failure patterns affect ~15-20% of spots but the agent's
overall reasoning quality is strong. Update to v1.1 after the first
training gate for improved accuracy on the relabel pass.
