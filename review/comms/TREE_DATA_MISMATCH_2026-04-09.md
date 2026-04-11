---
date: 2026-04-09
from: Builder
re: BET tree threshold mismatches — deterministic script findings
---

## Two mismatches make BET tree Steps 3-6 structurally dead

### Mismatch 1: connectivity_score encoding

**Tree assumes:** 0.0-1.0 float (thresholds: 0.30, 0.55, 0.70)
**Actual feature:** 0-10 integer (min=2, max=9, mean=3.3)

The tree's tier gates (Tier 1: <= 0.30, Tier 2: <= 0.55, Tier 3: <= 0.70)
can never fire because the minimum value in the data is 2.0.

**Fix options:**
A. Rescale thresholds to match 0-10 encoding: Tier 1 <= 3, Tier 2 <= 5, Tier 3 <= 7
B. Normalize feature to 0.0-1.0 in the extractor (connectivity_score / 10)
C. Replace connectivity_score with straight_danger in the tree (already 0.0-1.0)

**Recommendation:** Option A is simplest and doesn't change the pipeline.
Tier 1 (very dry) ≈ connectivity 2-3, Tier 2 (moderate) ≈ 4-5,
Tier 3 (connected) ≈ 6-7, Tier 4 (very connected) ≈ 8+.

### Mismatch 2: board_favour range

**Tree assumes:** board_favour can reach 0.20+
**Actual feature:** max = 0.171 (computed as 0.30 - villain_top_pair_plus_pct)

The tree's >= 0.20 gate on Steps 3, 4, 5, 6 can never fire.

**Fix options:**
A. Lower threshold to >= 0.10 (captures boards where hero's range
   is mildly favoured — board_favour > 0 means hero range has more
   TP+ than villain, which is already a PFA signal)
B. Lower to >= 0.05 (very permissive — lets almost any non-villain-
   favoured board through)
C. Remove board_favour gate entirely from Steps 3-4 (rely on
   is_preflop_aggressor + texture tier instead)

**Recommendation:** Option A (>= 0.10). The board_favour distribution:
- Negative (villain-favoured): 68% of situations
- 0.00 to 0.10: 18% of situations
- 0.10 to 0.17: 14% of situations
- >= 0.10 captures the top ~14% most hero-favoured boards, which is
  reasonable for PFA c-betting range (PFA bets ~30-45% overall, but
  only on favourable boards)

### Impact on labels

With both fixes, BET tree Steps 3-6 would start firing. The current
action distribution (BET: 9/563 = 1.6%) would increase significantly
— probably to 50-80 BETs (9-14%), which aligns with the research
(PFA c-bets ~30-45% of facing-no-bet situations, not 1.6%).

### For owner awareness

These are tree calibration errors, not poker logic errors. The GTO
Expert designed the tree with conceptually correct thresholds but
didn't verify them against actual feature encodings and ranges. This
is why the deterministic script was valuable — LLM agents would
have loosely interpreted "board favours hero" without hitting the
exact threshold, masking the mismatch.
