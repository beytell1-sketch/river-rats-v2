# Review: v9-3way Gate Check

**Date:** 6 April 2026
**Status:** GATE FAILED — v9-3way underperforms v8

---

## Results

| Model | Correct | Total | Accuracy |
|-------|---------|-------|----------|
| v8 HU baseline | 23/40 | 40 | 57.5% |
| v9-3way specialist | 20/40 | 40 | **50.0%** |
| Gate threshold | 14/24 3-way | — | 54.2% |

v9-3way scored 50.0% overall, below v8's 57.5% and below the
54.2% gate threshold.

## Failure Analysis

### v8 failure pattern (17 errors)
- 8× expert BET, got CHECK — the known passive problem
- 4× expert FOLD, got CALL — doesn't respect opponent strength
- 2× expert RAISE, got CALL — misses value raises
- 2× expert CALL, got FOLD/RAISE
- 1× expert CALL, got RAISE

### v9-3way failure pattern (20 errors)
- **10× expert CALL, got FOLD** — over-folds massively
- 3× expert CALL, got RAISE — over-aggressive
- 2× expert BET, got FOLD — folds when should bet
- 2× expert FOLD, got RAISE — raises when should fold
- 1× expert RAISE, got CALL
- 1× expert CALL, got RAISE
- 1× expert BET, got FOLD (adjusted from RAISE)

### Root cause: CALL class starvation

v9-3way was trained on 11 CALL samples out of 199. The model
learned a binary FOLD-or-RAISE decision boundary and almost
never predicts CALL. Of the 20 failures, 13 involve incorrect
CALL handling (10 CALL→FOLD, 3 CALL→RAISE).

## What Improved

| Axis | v8 | v9-3way | Change |
|------|-----|---------|--------|
| position_amplification | 17% | 83% | +66pp |
| aggression_respect | 33% | 50% | +17pp |
| combined | 50% | 75% | +25pp |

## What Regressed

| Axis | v8 | v9-3way | Change |
|------|-----|---------|--------|
| spr_interaction | 83% | 0% | -83pp |
| nut_potential | 67% | 33% | -34pp |
| bluff_compression | 100% | 83% | -17pp |
| range_narrowing | 50% | 33% | -17pp |

## Diagnosis

The concept works — v9-3way fixed position_amplification from
17% to 83%, which was v8's worst axis. The feature importance
shows the model learned from equity-based features. But:

1. **CALL starvation (11 samples)** — the model can't learn
   CALL decision boundaries from 11 examples. It defaulted to
   FOLD-or-RAISE binary.

2. **Narrow training distribution** — 199 situations from
   self-play don't cover the reference set's decision space.
   SPR interaction hands (SPR <2) and nut potential hands
   (draw-heavy boards) are underrepresented.

3. **From-scratch training** — no warm-start from v9-baseline
   means no transfer from 25k PokerBench. The model only knows
   199 multiway situations.

## Next Steps

The gate failure confirms the ML expert's advice: **200 samples
from self-play is not enough.** The SituationFactory approach
(board-anchored hand strength sweeps) would produce:
- Many more CALL situations (targeted generation)
- Coverage of SPR/nut-potential/range-narrowing axes
- 1000+ independent situations instead of 199 correlated ones

The progressive chain concept is validated by the axis
improvements. The execution needs more and better training data.
