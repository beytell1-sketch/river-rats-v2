# Review: Sticky Opponent Yield Results

**Date:** 6 April 2026
**Status:** REVIEW — sticky callback built but ineffective, need new approach

---

## What Was Built

`_make_sticky_callback()` added to `self_play.py` (lines 206-270).
Equity-gated override: in 3+ way pots facing a bet, converts
opponent FOLD to CALL when raw equity >= 15%.

`generate_3way_situations.py` updated with `--no-sticky` and
`--equity-floor` CLI flags. Sticky mode enabled by default.

## Test Results

- 864 passed, 7 failed (all 7 pre-existing from range data change)
- Zero new failures from the sticky callback

## Yield Results

| Run | Deals | Games | 3-way decisions | Yield |
|-----|-------|-------|-----------------|-------|
| Sticky (equity_floor=15%) | 500 | 3,000 | 36 | 1.20% |
| Normal (no sticky) | 500 | 3,000 | 36 | 1.20% |

**Identical.** The sticky callback has zero effect.

## Root Cause: Wrong Layer

The sticky callback targets **opponent postflop folds in 3+ way
pots**. Debugging reveals these don't happen:

- **Zero** opponent fold attempts in 3+ way postflop pots across
  300 games. The oracle checks (doesn't fold) when not facing a
  bet in multiway spots.
- The collapse happens at the **preflop layer**, not postflop.

### The actual bottleneck

| Stage | % of games | Detail |
|-------|-----------|--------|
| Hero folds preflop | 92.8% | Correct GTO — fold most hands |
| Hero reaches postflop | 7.2% | ~43 of 600 games |
| Of those, multiway | 7.0% | 3 of 43 postflop games |
| **Net multiway rate** | **0.5%** | 3 of 600 games |

Hero is dealt random cards at each position. GTO correctly folds
most of them. The 7.2% postflop rate is normal. The problem is
that of the 7.2% that reach postflop, only 7% are multiway —
because the other oracle seats ALSO fold most hands preflop.

The sticky callback can't help because there's nothing to
override — opponents aren't folding postflop in multiway pots.
They're folding preflop (correct) or the pot never becomes
multiway in the first place.

## Options (revised)

**A. Brute-force volume: ~17,000 deals**
At 1.2% yield, 17,000 deals produces ~200 situations. Runtime
~35 minutes. Action distribution is 94% CHECK — but per your
earlier note, a CHECK-heavy first iteration is acceptable.
The v9-3way model will bet more, producing richer data next round.

**B. Log non-hero 3-way decisions too**
Currently only hero decisions are captured. If we also log
opponent decisions when they're in 3-way pots, we get ~5x more
situations (5 opponents per deal instead of 1 hero). But: these
decisions are made by the HU-trained oracle, so they represent
the broken model's play — not useful for training.

**C. Modify hero selection for generation only**
Instead of cycling hero through all 6 positions, only assign hero
to positions that reached the flop in a multiway pot. Run the
deal once to determine which positions survive preflop multiway,
then replay with hero at those positions. This doesn't increase
the number of multiway pots, but ensures hero is always in them.

**D. Accept yield, run large generation**
Same as A, but frame it as the intended approach. 1.2% yield is
low but stable. 17,000 deals is tractable. The CHECK-heavy
distribution is the expected first iteration.

## My Recommendation

**Option A/D.** The yield is low but workable. The action
distribution concern was already addressed in your review: a
CHECK-heavy first training set is acceptable because the v9-3way
model trained on it will bet more confidently in multiway spots,
which produces richer second-round data.

Trying to engineer higher yield risks over-engineering. The
pipeline works — it just needs more volume.

---

## Files Changed

| File | Change | Status |
|------|--------|--------|
| `self_play.py` | Added `_make_sticky_callback()`, `sticky_opponents` param | Built, tested, no effect |
| `generate_3way_situations.py` | Added `--no-sticky`, `--equity-floor` flags | Built, tested |

### Decision needed

The sticky callback code is clean and harmless (defaults to off
in production). Options:
1. **Keep it** — it's correct code that happens to not help here.
   May be useful if future oracle versions do fold postflop multiway.
2. **Remove it** — dead code violates CLAUDE.md "no dead code" rule.
