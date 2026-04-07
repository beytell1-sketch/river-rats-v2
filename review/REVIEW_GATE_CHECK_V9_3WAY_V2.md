# Review: v9-3way-v2 Gate Check

**Date:** 7 April 2026
**Status:** REVIEW — improvement confirmed, regressions identified

---

## Results

| Model | Correct | Accuracy | Training |
|-------|---------|----------|----------|
| v8 HU baseline | 21/40 | 52.5% | 25k PokerBench |
| v9-3way-v1 (199) | 21/40 | 52.5% | warm-start + 199 self-play |
| **v9-3way-v2 (349)** | **24/40** | **60.0%** | warm-start + 349 (199 + 151 factory) |

## Axis Breakdown

| Axis | v8 | v1 | v2 | Delta v8→v2 |
|------|----|----|-----|-------------|
| position_amplification | 17% | 17% | **67%** | **+50pp** |
| combined | 50% | 50% | **75%** | **+25pp** |
| range_narrowing | 50% | 50% | **67%** | **+17pp** |
| nut_potential | 50% | 50% | **67%** | **+17pp** |
| bluff_compression | 83% | 83% | 83% | 0 |
| spr_interaction | 83% | 83% | **50%** | **-33pp** |
| aggression_respect | 33% | 33% | **17%** | **-16pp** |

## What Improved (targeted axes)

**Position amplification: 17% → 67% (+50pp)**
The factory's 79 OOP betting situations directly addressed this.
v8 checked with strong hands OOP; v2 now bets correctly 4/6 times.

**Range narrowing: 50% → 67% (+17pp)**
Factory CALL situations with bet-and-call signals improved this.

**Combined + nut_potential: both improved.**

## What Regressed

**SPR interaction: 83% → 50% (-33pp)**
The factory didn't include SPR-focused situations. The additional
training data may have diluted v9-baseline's SPR knowledge.
Next iteration target.

**Aggression respect: 33% → 17% (-16pp)**
The model now over-raises in some facing-bet spots (4 cases of
expert=CALL, got=RAISE). The polarized-raise instruction may not
have been strong enough, or the factory's RAISE training examples
shifted the CALL→RAISE boundary too aggressively.
Next iteration target.

## Failure Analysis (v2, 16 failures)

- 4x expert=CALL, got=RAISE — over-raising (aggression)
- 3x expert=FOLD, got=CALL — over-calling
- 2x expert=CALL, got=FOLD — under-calling
- 2x expert=BET, got=CHECK — residual passive
- 2x expert=BET, got=RAISE — over-aggressive
- 1x expert=CHECK, got=FOLD — mis-fold
- 1x expert=RAISE, got=CALL — under-raising
- 1x expert=CALL, got=RAISE (adj) — adjuster issue

## Feature Importance Concern

`facing_bet` dominates at 62.2% importance. The model may be
over-splitting on this binary feature. The factory data has a
strong facing_bet/action correlation (all CALLs/RAISEs face a
bet, all CHECKs/BETs don't). Next iteration should include
more variety in action-per-facing_bet combinations.

## Next Iteration Targets

1. **SPR interaction** — construct low-SPR situations (SPR < 2)
   where decisions change based on stack commitment
2. **Aggression respect** — more bet-and-call situations where
   CALL is correct (not RAISE), to pull the CALL→RAISE boundary
   back
3. **facing_bet feature dominance** — include situations where
   facing_bet=True but action is not always CALL/FOLD/RAISE
   (some CHECK-raise setups?)

## Summary

v9-3way-v2 is the best multiway model so far (60% vs 52.5%).
The progressive chain concept works — targeted factory data
moved the target axes significantly. But each iteration creates
new regressions that need addressing. The iteration cycle
continues: diagnose → target → generate → label → train → gate.
