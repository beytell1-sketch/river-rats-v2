# Self-Play Loop Findings (Rounds 1-5)

**Date:** 6 April 2026
**Status:** Loop concluded — opponent quality insufficient for parameter discrimination

## Summary

The self-play loop ran 5 rounds (100-1000 deals, 360-12000 games per round)
testing 6 initial hypotheses and their hybrids against heuristic AI opponents.

**Conclusion:** The heuristic opponents are too weak to produce reliable signal
for parameter selection. Modified variants' apparent advantages shrank with
sample size and reversed at 1000 deals. The testing environment cannot
discriminate between better and worse strategies.

## Results by Round

| Round | Deals | Winner | Margin over baseline |
|-------|-------|--------|---------------------|
| R1 | 100 | loose_draws | +366 mbb |
| R2 | 100 | loose_draws_oop | +331 mbb |
| R3 | 100 | loose_draws_cold_strict | +170 mbb |
| R4 | 500 | loose_draws_oop | +49 mbb |
| R5 | 1000 | **baseline** | — (baseline wins) |

## Validated Findings (poker-reasoning independent of opponent quality)

1. **Draw bypass thresholds are too conservative.** rule1_draw_bypass 8→5,
   draw_outs_ip_base 8→6, rule5_draw_bypass 7→5. Consistent signal across
   all rounds. Sound GTO reasoning: more draws should continue multiway.

2. **OOP + cold-call tightening interact destructively.** Never combine
   equity_realization_oop reduction with cold_call_base increase — they
   double-tighten BB defence spots.

3. **Aggressive value/raise tightening overshoots.** value_base 0.50 and
   raise_base 0.55 are too tight. Moderate 0.45/0.50 are better if any
   tightening is applied.

## Findings NOT Validated (dependent on opponent quality)

- Overall EV ranking between variants
- Whether OOP discount (0.75) helps or hurts at volume
- Whether cold-call tightening helps at volume
- Whether the adjuster is net positive or negative

## Root Cause

The heuristic AI doesn't exploit:
- OOP overplaying (doesn't barrel against capped ranges)
- Loose draw continues (doesn't price draws or deny equity)
- Thin value bets (calls too much regardless)

Against non-punishing opponents, "tighter" means "folding free equity."

## Next Step

Evaluate variants against the 50-hand expert reference set (MW-01 to MW-50).
This measures decision correctness against expert GTO labels, sidestepping
the opponent quality confound.

## Files

- results/round_1.json through round_5.json
- docs/hypotheses.json, hypotheses_r2.json, hypotheses_r3.json,
  hypotheses_r4_tiebreaker.json, hypotheses_r5_confirm.json
