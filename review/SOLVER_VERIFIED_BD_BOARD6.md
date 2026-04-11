# Solver-Verified Hands: BD_Board6 (9c 7c 2d Kh)

**Date:** 7 April 2026
**Source:** GTO Wizard, exact line verified by owner
**Status:** VERIFIED — add to training data

---

## Setup (identical for all 5 hands)

**Players:** CO (hero, opener), BTN (cold-caller), BB (defender)

**Preflop:** CO opens. BTN calls. BB defends. Pot: 90.

**Flop: 9c 7c 2d**
CO bets 30. BTN calls. BB calls. Pot: 180.

**Turn: Kh**
CO bets 60. BB calls. BTN raises to 180.

**Hero's decision:** Faces 120 more. Pot ~420 if calling. Pot odds 28.6%. SPR 0.33.

All hands are **top two pair (K9)** — same hand category, same equity class. The ONLY variable is hero's suit holdings and what they block in villain's range.

---

## The teaching point

On a 9c 7c 2d board, the club flush draw is the dominant draw in villain's range. Hero's club holdings directly determine whether villain is likely to hold flush draw combos. This swings the raise/call decision from 0% raise to 100% raise — a bigger effect than any other feature.

This is Section 1.8 of the knowledge base in action: **blockers for action selection are still critical 3-way.** Suit holdings swing raise frequency by 80+ percentage points for the SAME hand on the SAME board in the SAME spot.

---

## Solver results (all K9 two pair, same board, same action)

| # | Hero Hand | Solver Action | Raise % | Call % | All-in % | Key Blocker Effect |
|---|-----------|--------------|---------|--------|----------|-------------------|
| 1 | Kh 9d | CALL | 9% | 80% | 11% | No club blocker. Villain's club flush draws fully live. Raising into a range with many flush combos is thin. Default CALL. |
| 2 | Kd 9h | RAISE (all-in) | 0% | 17% | 83% | 9h blocks heart draws (secondary). Kd blocks diamond backdoors. Neither blocks clubs but the combination removes enough equity from villain's continuing range. Near-pure all-in. |
| 3 | Ks 9h | MIXED | 47% | 53% | 0% | Ks doesn't block clubs. 9h blocks hearts. Roughly 50/50 — partial blocker effect from the 9h only. |
| 4 | Kc 9d | RAISE | 100% | 0% | 0% | Kc DIRECTLY blocks club flush draws. Villain's range loses its strongest continuing hands. Pure raise. This is the maximum blocker effect. |
| 5 | Kd 9c | RAISE | 71% | 29% | 0% | 9c blocks club flush draws (lower card, fewer combos removed than Kc). Strong but not pure raise. |

---

## Training labels (model can't express mixed — default to majority action)

| # | Hero Hand | Training Label | Reasoning |
|---|-----------|---------------|-----------|
| 1 | Kh 9d | **CALL** | 80% call in solver. No club blocker. |
| 2 | Kd 9h | **RAISE** | 83% all-in in solver. Strong combined blocker effect. |
| 3 | Ks 9h | **CALL** | 53% call in solver. Marginal — default to majority. |
| 4 | Kc 9d | **RAISE** | 100% raise in solver. Maximum club blocker. |
| 5 | Kd 9c | **RAISE** | 71% raise in solver. 9c blocks club draws. |

---

## Feature implications

The current `flush_block_pct` feature should capture this — hero holding clubs on a club-draw board increases flush_block_pct. But the solver data shows the effect is MUCH larger than the feature currently weights (0% importance at 349 samples). With these 5 hands plus the 45 flush-blocking design situations, the feature should activate.

**Critical teaching:** Same hand, same board, same action line. The ONLY difference is suits. The model must learn that suit composition (via flush_block_pct and related features) drives the raise/call boundary for non-set made hands.

---

## Action history for SituationFactory

All 5 hands share this spec:
```
board_cards: ['9c', '7c', '2d', 'Kh']
hero_pos: 'CO'
villain_positions: ['BB', 'BTN']  # BTN is raiser (last)
pot: 300.0
to_call: 120.0
street: 'turn'
action_history: [
    ('preflop', 'CO', 'raise'),
    ('preflop', 'BTN', 'call'),
    ('preflop', 'BB', 'call'),
    ('flop', 'CO', 'bet'),
    ('flop', 'BTN', 'call'),
    ('flop', 'BB', 'call'),
    ('turn', 'CO', 'bet'),
    ('turn', 'BB', 'call'),
    ('turn', 'BTN', 'raise'),
]
opener_position: 'CO'
effective_stack: 100.0
```

Hero cards for each:
1. ['Kh', '9d']
2. ['Kd', '9h']
3. ['Ks', '9h']
4. ['Kc', '9d']
5. ['Kd', '9c']
