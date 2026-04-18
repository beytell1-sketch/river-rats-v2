---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder + Teaching terminal
re: v2.3.1 scope expanded — board_adjusted_hrp + air-CHECK counter-examples + teaching guard
status: DIRECTIVE — amends update-f
---

# v2.3.1 — Three-Layer Fix

Two playtest findings (A4d on Qs5s7s, T5 on JJ2) expose
related but distinct problems. All three layers need fixing.

## Finding comparison

| | A4d on Qs5s7s | T5 on JJ2 |
|---|---|---|
| HRP | 0.96 (misleading — good preflop, missed board) | 0.15 (correct — bad preflop) |
| board_adjusted_hrp | 0.29 | 0.044 |
| equity | 0.30 | 0.29 |
| worse_hand_pct | 0.34 | 0.20 |
| villain_air_pct | 0.47 | 0.70 |
| is_made_hand | 0 | 0 |
| has_showdown_value | 0 | 0 |
| Oracle BET confidence | 98.6% | 72% |
| **Primary driver** | High HRP misleads | High villain_air + checked_back misleads |

A4d: model thinks hero is strong because HRP is high.
T5: model thinks hero should bet because villain is weak.
Both wrong because hero has nothing.

## The three layers

### Layer 1 — Feature: board_adjusted_hrp (DONE, commit 80197cd)

Helps on both hands (0.29 and 0.044 respectively). Addresses
the A4d-class problem (misleading HRP). Partially addresses
the T5 class (provides another "hero has nothing" signal).

Already built. No further work.

### Layer 2 — Training data: air-in-checked-through CHECK counter-examples (NEW)

The model has seen:
- Hundreds of (villain_weak + checked_back → BET) examples
  with MADE HANDS
- Nearly zero (villain_weak + checked_back + hero_has_air
  → CHECK) examples

It extrapolated "villain weak → bet" without learning "but
only if you have something." The 0 SUSPECT labels from the
audit confirm this — the BET labels were honest (made hands).
The gap is the MISSING counter-examples, not wrong labels.

**Task:** Factory-generate ~30-40 hands matching:
- facing_bet=0
- villain_checked_back=1
- num_opponents >= 1
- is_made_hand=0
- draw_outs <= 2 (air or very weak draw)
- equity_vs_range < 0.35
- Spread across streets (flop/turn) and positions

These are "villain checked, villain range is weak/capped,
but hero also has nothing" spots. The correct action is
CHECK (no value to extract, poor bluff candidates on most
board textures).

Label with v3.1 prompt (no override). Panels should
produce CHECK on poker merits — these are genuinely
CHECK-correct spots.

Add to the training CSV alongside all existing data.

### Layer 3 — Teaching: value_extract guard on air (NEW)

**Teaching terminal:** add a coherence guard for the
`value_extract` intention when hero has air.

When `primary_intention = value_extract` AND
`is_made_hand = 0` AND `has_showdown_value = 0`:

The template must NOT say "extracts value from hands
worse than hero" — nothing is worse than air. Instead:

- If action is BET/RAISE: reframe as "leveraging fold
  equity against villain's air — this is a bluff, not a
  value bet"
- If action is CHECK: reframe as "no value to extract
  with this hand — checking preserves the option to
  improve or fold"

This is the same coherence-guard pattern as D2/D3 from
Phase 2 — detect the incoherent (intention, hand_state)
pair and reframe. Not a static override; a coherence
guard that says "don't say value extract when you have
nothing to extract."

Also: the sentence "betting extracts value from the 30%
who call with worse than air" is logically wrong — the
30% made hands BEAT hero. The template confused villain's
made-hand portion with "hands worse than hero." Guard
must prevent this inversion.

## Execution order

### Builder (logic):

1. ~~board_adjusted_hrp~~ (done)
2. Override audit ~~→ label cleanup~~ (done — 0 SUSPECT,
   no cleanup needed)
3. Factory-generate ~30-40 air-CHECK counter-examples
4. Label with v3.1 prompt
5. Re-extract ALL training data with new feature (110 cols)
6. Assemble: v2.2 base + Section 1 + CALL supplement +
   air-CHECK counter-examples
7. Retrain → `v2_3_1_model.json`
8. Evaluate: standard gates + BOTH litmus tests
   (A4d/Qs5s7s and T5/JJ2 must predict CHECK)

### Teaching terminal:

9. Add value_extract air guard to coherence registry
10. Verify on T5/JJ2: output should say "bluff / fold
    equity" not "value extract from worse"

### Steps 3-4 and 9-10 run in parallel.
### Steps 5-8 sequential after 3-4 complete.

## Litmus tests for v2.3.1

Both MUST predict CHECK:

| Hand | Key features | Why CHECK |
|---|---|---|
| A4d on Qs5s7s | Air, wrong suit, monotone, 0 outs | No hand, no draw, hostile board |
| T5 on JJ2 | 10-high, paired board, 0 outs | 80% of villain beats hero |

If either still predicts BET after the fix, the model needs
more counter-examples or the feature isn't carrying enough
weight. Iterate.

## What this is NOT

This is NOT a static override ("when hero has air, force
CHECK"). This is:
- A feature that honestly represents hero's board-adjusted
  strength
- Training examples that show the model what to do when
  hero has nothing in a villain-weak spot
- A teaching guard that doesn't say "value extract" when
  there's nothing to extract

All three work with honest data. No rules imposed.
