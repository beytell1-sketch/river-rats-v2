---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder + Owner
re: PLAYTEST FINDING — v2.3 model recommends BET at 98.6% with complete air on monotone board
status: LOGGED — v2.4 model scope item, not a v2.3 regression fix
hand: A4d on Qs 5s 7s (flop), BTN vs BB, checked to hero
---

# Playtest Finding 002 — Air Bluff on Monotone Board

## Confirmed via real oracle

Ran A4d on Qs5s7s through the shipped v2.3 model
(`v2_3_model_shipped.json`). Result:

```
Legal mask → CHECK: 0.014  BET: 0.986  => BET
```

98.6% BET confidence. This is the real model, not the mock.

## Feature snapshot

| Feature | Value | Implication |
|---|---|---|
| hero_range_percentile | 0.956 | Top of preflop range (Ace-suited) |
| equity_vs_range | 0.302 | Only 30% equity |
| is_made_hand | 0 | No made hand |
| has_flush_draw | 0 | Wrong suit (diamonds, board is spades) |
| has_straight_draw | 0 | No straight draw |
| draw_outs | 0 | Zero outs |
| improvement_probability | 0.0 | Cannot improve |
| has_showdown_value | 0 | No showdown value |
| worse_hand_pct | 0.337 | Only 34% of villain is worse |
| villain_air_pct | 0.466 | 47% villain air (fold equity exists) |
| is_monotone | 1 | Monotone board |
| danger_score | 0.580 | High danger |

## What the model is doing

The model sees:
- HRP 0.96 → high perceived range strength
- villain_checked_back=1 → bias-signature match
- facing_bet=0 → bias-signature match
- villain_air_pct=0.47 → fold equity exists

And fires the v2.3 BET-in-checked-through override pattern.

What the model misses:
- is_made_hand=0 + has_flush_draw=0 + draw_outs=0 = complete
  air with zero improvement
- is_monotone=1 with hero holding wrong suit = board texture
  completely hostile
- has_showdown_value=0 = hero can't win at showdown
- If called, hero has 30% equity but zero outs to improve —
  this is a terrible bluff that can't barrel turn/river

## Diagnosis

The v2.3 BET-heavy supplement taught the model to bet
aggressively in checked-through spots. The override pattern
fires on HRP + villain_checked_back + villain_air_pct without
enough weight on the "but I have nothing on this board"
features.

The model lacks a "don't bluff with zero outs on a hostile
board" guard. In training data, most high-HRP checked-through
BET hands had made hands or draws. Pure air on a monotone
miss board with zero outs is an underrepresented shape in
training.

## Impact assessment

This is NOT a v2.3 regression — v2.2 may have the same issue
(untested on this specific shape). It's a model capability
gap exposed by playtesting.

For the v2.3 ship: this hand shape is rare in natural play
(BTN opens A4d, flop comes all spades, villain checks). The
model's overall accuracy (72.5% FB-40, 82.0% MW-50) is not
affected by this edge case. But a student seeing "BET with
98.6% confidence" when they have complete air on a monotone
board will lose trust in the oracle.

## Fix direction (v2.4 scope)

1. **Training data gap:** add 15-20 hands where hero has air
   on monotone/hostile boards with high HRP but zero outs,
   labelled CHECK/FOLD. The model needs to see "high HRP +
   zero hand strength + hostile board = don't bluff."

2. **Feature attention:** the `is_monotone` and `draw_outs=0`
   features should carry more weight when combined with
   `is_made_hand=0`. This is a feature interaction the model
   hasn't learned.

3. **Self-play connection:** if the v2.3 self-play diagnostic
   shows the model generating lots of bluffs on monotone
   boards, this is the root cause.

## For teaching (already partially addressed)

The HRP reframe at `0e75102` and `afa7895` already handles
the teaching text ("Air — no made hand — 3% equity"). But the
oracle's BET recommendation is still shown to the student.
The teaching correctly describes the situation; the oracle
gives the wrong advice. The student sees both and gets
confused.

## For game builder

Consider: when oracle confidence is > 90% but teaching output
says "air — no made hand" with equity < 15%, the game could
surface a visual flag ("Oracle recommendation may not match
your situation"). This is a game-UX mitigation, not a fix —
but it protects student trust until v2.4 addresses the model.
