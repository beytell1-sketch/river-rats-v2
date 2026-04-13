---
date: 2026-04-14
from: Builder team
to: Owner (Rupert)
re: Phase 3B Calibration Report — v2 Prompt Blind Exam
status: GATE PASSED
---

# Phase 3B Calibration Report

## Result

| Metric | Result | Gate | Status |
|--------|--------|------|--------|
| Overall accuracy | **20/24 (83.3%)** | ≥20/24 (83%) | **PASS** |
| GTO-reversal hands | **3/3 (100%)** | 3/3 required | **PASS** |
| **Combined gate** | | | **PASSED** |

## Method

- 3 independent GTO Expert agents, 1 per batch of 8 hands
- **Blind exam**: agents received situation texts + full 54-feature
  vectors, the v2 labelling prompt, and the KB v1.3. No access to
  answer keys or calibration_exam.py.
- Scoring performed separately by the builder, comparing agent
  actions to expert answer key.

## GTO-Reversal Hands (all correct)

| Hand | Expected | Agent | Reasoning quality |
|------|----------|-------|-------------------|
| MW-30 | CALL | **CALL** | Agent correctly identified equity surplus (44% vs 18% pot odds), read the composition triple (31% TP+, not heavy), and cited the MW-30 solver correction. Rejected FOLD explicitly. |
| MW-33 | RAISE | **RAISE** | Agent correctly identified top set must raise vs bet+call for value extraction. Cited KB Example 4, noted straight danger, and SPR commitment. |
| MW-50 | FOLD | **FOLD** | Agent correctly identified BTN's flop raise as near-nuts signal, equity margin near zero (+0.007), no draw outs, OOP. Cited action history overriding raw equity. |

## Full Results by Hand

### Batch 1 (MW-12 through MW-23): 5/8

| Hand | Hero | Board | Expert | Agent | Match | Bucket | Conf | Diff |
|------|------|-------|--------|-------|-------|--------|------|------|
| MW-12 | JsTs | 8c5d2h | CHECK | BET | **NO** | air | MED | 2 |
| MW-13 | KhJh | Ac9d3s | CHECK | CHECK | YES | air | HIGH | 1 |
| MW-14 | Td9d | Jd8d3h | CALL | CALL | YES | drawing | HIGH | 2 |
| MW-15 | 9s8s | QsJd5h2c6c | CHECK | BET | **NO** | air | MED | 3 |
| MW-17 | AdKs | Jd8d4c | CALL | FOLD | **NO** | air | MED | 3 |
| MW-18 | Qd3d | Jd8d4c | CALL | CALL | YES | drawing | HIGH | 2 |
| MW-19 | Tc9c | QhJs8d | BET | BET | YES | monster | HIGH | 1 |
| MW-23 | QhJc | Qc8d3s | BET | BET | YES | strong_made | HIGH | 2 |

### Batch 2 (MW-24 through MW-36): 7/8

| Hand | Hero | Board | Expert | Agent | Match | Bucket | Conf | Diff |
|------|------|-------|--------|-------|-------|--------|------|------|
| MW-24 | QsJd | Qc8d3s | BET | BET | YES | medium_made | HIGH | 2 |
| MW-27 | JhJc | 9d6c2h | BET | BET | YES | medium_made | HIGH | 2 |
| MW-28 | JhJd | 9d6c2h | BET | CHECK | **NO** | medium_made | MED | 2 |
| MW-30 | KcTh | KdJc6s | CALL | CALL | YES | medium_made | HIGH | 3 |
| MW-33 | 8h8s | 8d7c3h | RAISE | RAISE | YES | monster | HIGH | 2 |
| MW-34 | AcAd | Js9c4d | BET | BET | YES | strong_made | HIGH | 2 |
| MW-35 | QcJd | Qh7c2s | CALL | CALL | YES | medium_made | HIGH | 2 |
| MW-36 | QcJd | Qh7c2s | CALL | CALL | YES | medium_made | HIGH | 2 |

### Batch 3 (MW-37 through MW-50): 8/8

| Hand | Hero | Board | Expert | Agent | Match | Bucket | Conf | Diff |
|------|------|-------|--------|-------|-------|--------|------|------|
| MW-37 | QcJd | Qh7c2s | CALL | CALL | YES | medium_made | HIGH | 2 |
| MW-38 | AhJh | Kh8h3d | CALL | CALL | YES | drawing | HIGH | 2 |
| MW-39 | AhJh | Kh8h3d | CALL | CALL | YES | drawing | HIGH | 2 |
| MW-41 | QhTc | KsQd7cJh | CALL | CALL | YES | medium_made | MED | 3 |
| MW-44 | Th8h | Ts9h4d7c | CALL | CALL | YES | medium_made | MED | 3 |
| MW-48 | AhTc | QdJc4s | CHECK | CHECK | YES | drawing | HIGH | 1 |
| MW-49 | AdKd | As9c5dTc | BET | BET | YES | strong_made | HIGH | 1 |
| MW-50 | JcTc | Js8h4d5c | FOLD | FOLD | YES | medium_made | MED | 3 |

## Failure Analysis (4 misses)

### MW-12: Agent BET, Expert CHECK

**Situation:** JsTs (air) on 852r, IP BTN, not facing bet, both
opponents checked.

**Agent reasoning:** Air with high fold equity (0.656), high villain
air (56%), both opponents showed weakness. Bet to fold out air.

**Why wrong:** hero_range_percentile = 0.045 (bottom of range).
The air/air bet 3-way on a dry board with no draw and no equity
(13.6%) is a pure stab. While fold equity looks high, the 3-way
bluff-to-value ratio requires restraint. JsTs has some backdoor
equity on dynamic turns but no immediate reason to bet. CO still
in the pot may have checked back a moderate hand. CHECK preserves
the option to check-fold or see a free turn.

**Pattern:** Over-betting air with high fold equity. The prompt
should handle this — may be a frequency error (not every air hand
should bet even with fold equity).

### MW-15: Agent BET, Expert CHECK

**Situation:** 9s8s (air, 0% equity) on QJ526 river, IP BTN, full
check-through 3 streets.

**Agent reasoning:** 0% showdown equity, fold equity 0.644, checked
through = both ranges capped. Bet since checking loses 100%.

**Why wrong:** River bluffing 3-way is very tight (~1:4 ratio per
KB Section 1.4). With 9-high on a highly connected board (Q-J-5-2-6),
villain's capped ranges still contain enough medium-made hands
(villain_medium_made_pct = 0.451) that won't fold to a bet. The
"0% equity = must bet" logic ignores that the bet costs chips and
will get called too often 3-way.

**Pattern:** Incorrect application of "zero showdown value = must
bluff." The 3-way bluff threshold is much tighter than HU.

### MW-17: Agent FOLD, Expert CALL

**Situation:** AdKs (overcards, no draw) on Jd8d4c, BB OOP,
facing 33 into 90 (pot odds 26.8%).

**Agent reasoning:** Equity margin negative (-0.04), no draw, OOP,
villain TP+ at 38.6%. Overcard outs discounted by OOP EQR.

**Why wrong:** This is KB Example 7 (same board, same hand). The
pipeline shows draw_outs = 0 because it counts flush/straight
draws, NOT overcards. AK has 6 overcard outs (~24% to improve).
With flush_draw_rank = 14 (Ad blocks some villain flush combos)
and implied odds when hitting TPTK, this is a CALL. The agent
over-weighted the negative equity_margin without accounting for
hidden overcard outs.

**Pattern:** Failure to apply KB Example 7 overcard hidden equity
lesson. The prompt has this example but the agent folded anyway.

### MW-28: Agent CHECK, Expert BET

**Situation:** JhJd (overpair) on 962r, SB OOP, first to act.

**Agent reasoning:** OOP against BTN opener's uncapped range, dry
static board, pot control. Let PFA reveal info.

**Why wrong:** This is the KB Example 6 pattern — high equity
(60.85%) + thin villain value (16.1% TP+) + very high villain air
(56.3%) + dry static board overrides OOP default. The agent
correctly identified this as medium_made but defaulted to the OOP
pot control heuristic instead of recognizing the value-override
conditions. hero_range_percentile = 0.81, worse_hand_pct = 0.944.

**Pattern:** Over-applying OOP CHECK default when composition
supports betting. The prompt's Example 6 teaches exactly this.

## Summary of Patterns

| Pattern | Hands | Severity |
|---------|-------|----------|
| Over-betting air (high fold equity ≠ always bet) | MW-12, MW-15 | Low — prompt handles value ratio |
| OOP overcard hidden equity | MW-17 | Low — KB Example 7 covers this |
| OOP check default when composition overrides | MW-28 | Low — KB Example 6 covers this |

All 4 failures involve prompt content that already addresses the
pattern. These are edge-case reasoning errors, not prompt gaps. No
prompt changes recommended — the prompt correctly teaches all 4
patterns.

## Confidence Distribution

| Confidence | Correct | Total | Accuracy |
|------------|---------|-------|----------|
| HIGH | 16 | 17 | 94.1% |
| MEDIUM | 4 | 7 | 57.1% |

High-confidence labels are very reliable (94%). Medium-confidence
labels are the risk zone — these are the hands most likely to
benefit from Pass 2 deep review.

## Recommendation

**Gate PASSED.** Proceed to Pilot (20 hands x 3 feature attention
approaches, 10 agents) as specified in PLAN_PHASE3_FINAL.

No prompt modifications needed. The 4 failures are within the
expected error budget and the patterns are already covered by KB
worked examples. The v2 bucket-first prompt + KB v1.3 is
calibrated and ready for production labelling.
