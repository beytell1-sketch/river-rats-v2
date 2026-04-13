---
date: 2026-04-13
from: Builder team (programmer)
to: Owner (Rupert)
re: Phase 1C feature diff report — reconstruction vs stored features
status: FOR OWNER REVIEW (Gate 3)
---

# Phase 1C: Feature Diff Report

## Summary

| Metric | Value |
|---|---|
| Total situations checked | 200 |
| PASS (features match) | 200 |
| SUSPECT (features differ) | 0 |
| CERTAIN | 173 |
| AMBIGUOUS | 27 |

## What was checked

For each of the 200 reconstructed situations, the following
sequence-derived features were compared between the stored
feature values and what the reconstructed action string implies:

1. **facing_bet** — does the action string show a bet/raise before hero's ????
2. **num_callers_to_bet** — how many calls appear between bettor and hero?
3. **facing_raise** — does the action string show a raise before hero?

These are the features most directly derivable from the current-street
action sequence. Other sequence-derived features (villain_aggression_count,
villain_checked_back, villain_call_count) are cross-street counters that
can't be verified from the current-street sequence alone.

## SUSPECT Situations

**None.** All 200 situations pass feature verification.

## NULL Features (expected — will be populated in full re-extraction)

These features are NULL/zero across all stored situations.
They were added after the training data was generated and have
never been populated. Full re-extraction with card data will
populate them.

- `flush_draw_rank`: NULL in 200/200 situations
- `hero_range_percentile`: NULL in 200/200 situations
- `has_showdown_value`: NULL in 200/200 situations
- `villain_fold_equity_estimate`: NULL in 200/200 situations
- `is_preflop_aggressor`: NULL in 200/200 situations
- `flush_block_pct`: NULL in 175/200 situations
- `overcard_outs`: NULL in 112/200 situations
- `improvement_probability`: NULL in 93/200 situations

## Classification Breakdown

| Classification | Count | Enters training? |
|---|---|---|
| CERTAIN + PASS | 173 | Yes |
| AMBIGUOUS + PASS | 27 | Yes (flagged) |
| CORRUPT | 0 | N/A |
| SUSPECT | 0 | No |
| Factory 2-way (discarded) | 151 | No |

## Interpretation

**All 200 self-play situations pass feature verification.**

The stored feature values are consistent with the reconstructed
action sequences. This means:

1. The self-play pipeline produced valid sequences (confirmed by
   reconstruction: 0 CORRUPT)
2. The feature extraction was consistent with those sequences
   (confirmed by this diff: 0 SUSPECT)
3. The only data quality issues are:
   - 8 NULL features that were never populated (expected)
   - Labels produced by sequential reasoning (addressed in Phase 3)
   - 151 factory 2-way situations already discarded

**The 200 self-play situations are clean.** Sequence corruption
was not a factor in this dataset. The problems we're fixing are:
(a) missing features (NULL), (b) labelling methodology (sequential
→ bucket-first), and (c) 2-way contamination (discarded).

## What this means for Phase 2 allocation

- **200 situations survive** from reconstruction (all PASS)
- **151 factory 2-way discarded** (heads-up, harmful for 3-way)
- **New situations needed:** ~200-270 to reach target of ~400-470
- **Focus areas for new situations:** BP7 non-monster RAISE (mandatory),
  BET/CHECK factory to fill gaps, CALL/FOLD facing-bet diversity
- **Allocation should be designed based on action/street/position
  distribution of the surviving 200**
