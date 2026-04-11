# Feature Proposal: Bluff Signal Features

**Date:** 8 April 2026
**Status:** AWAITING OWNER REVIEW
**Sources:** Architecture Expert, Research A (poker strategy, 12+ sources),
Research B (poker AI/ML, 10+ sources), GTO Expert

---

## The Problem

The model identifies value raises (is_monster=1) but cannot identify
bluff raises. All non-monster hands facing a bet are CALL or FOLD.
The missing signal: where hero's hand sits within hero's OWN range.

## Key Research Findings

1. **Bluffing is a range-relative decision.** Solvers bluff with the
   bottom of hero's range — hands with no showdown value that gain
   nothing from calling. (All sources agree.)

2. **The strongest draws are NOT the best bluffs.** Strong combo draws
   (nut flush + overcards) play well without fold equity — they should
   CALL to realize equity. Weaker draws that "need" fold equity are
   better bluff candidates. (GTO Wizard "Picking the Right Semi-Bluffs")

3. **Showdown value is continuous, not binary.** PioSolver sometimes
   bluffs with weak pairs. The spectrum runs from "fat value" through
   "thin value" to "showdown value" to "no showdown value." (GTO
   Wizard equity buckets framework)

4. **`get_hand_percentile` already exists** in range_manager.py line
   1718 but is never wired to the feature extractor. (Architecture Expert)

5. **The dual blocker principle:** Good bluffs block villain's
   CONTINUING range while NOT blocking villain's FOLDING range. Our
   current `flush_block_pct` captures neither dimension for hero's own
   draws (returns 0 when hero has 2 flush-suit cards). (GTO Wizard
   "Blockers & Unblockers")

6. **Multiway bluffing is rare and requires all conditions met.**
   3-way fold equity threshold is ~49%. Only nut draws with blockers
   cross this threshold. (KB Section 1.1, confirmed by all sources)

---

## Proposed Features

### Feature #49: `hero_range_percentile` (PRIMARY)

**What:** Where hero's hand ranks in hero's own preflop range on this
board. 0.0 = bottom of range (bluff candidate), 1.0 = top of range
(value).

**Computation:** Mirror of existing `partition_range` but over hero's
range instead of villain's range. The function `get_hand_percentile`
already exists in range_manager.py — needs wiring to feature_extractor.

**Cost:** ~300-500 eval7 calls per situation. Negligible (same order
as existing range features).

**What it teaches the model:**
- Bottom of range (0.0-0.15) + facing bet = bluff raise candidate
- Middle of range (0.15-0.70) + facing bet = call
- Top of range (0.70-1.0) + facing bet = value raise

**Would it have prevented MW-20?** Yes. Ts9s (pair + draw) on MW-20's
board sits in the MIDDLE of hero's range (~0.40-0.50 percentile). The
model would see "middle of range = CALL" instead of overgeneralizing
to RAISE.

### Feature #50: `has_showdown_value` (SIMPLE DERIVED)

**What:** Binary — does hero's hand win at showdown without improvement?

**Computation:** `int(is_made_hand == 1 and hand_category >= 3)`
Zero computation cost — derived from existing features.

**What it teaches:**
- has_showdown_value=0 + draws = bluff candidate (nothing to lose)
- has_showdown_value=1 + draws = call (protect showdown value)
- has_showdown_value=0 + no draws = fold (no equity, no bluff equity)

### Feature #51: `villain_fold_equity_estimate` (DERIVED)

**What:** Estimated probability both opponents fold to a raise.

**Computation:** Derived from existing features:
```
per_opp_fold = 1 - (villain_top_pair_plus_pct + 0.5 * villain_draw_pct)
fold_equity = per_opp_fold * per_opp_fold  # squared for 2 opponents
```

**What it teaches:** When fold_equity < 0.35, raising is burning money
regardless of draw strength. When fold_equity > 0.49, the bluff
threshold is met.

---

## Features Considered but Deferred

| Feature | Why defer |
|---------|----------|
| `nut_draw_bluff_eligible` | Requires card-level blocker check. Valid but complex — defer until flush_block_pct is fixed for hero's draws |
| `bluff_raise_composite_score` | Depends on above. Defer. |
| `flush_draw_rank` | Identified in solver analysis. Separate from bluff signal. Add in same batch but independent rationale. |
| `board_polarization_index` | Research B suggests this. Useful but lower priority than range percentile. |

---

## Integration Plan

| Feature | Files changed | Breaks models? | Effort |
|---------|--------------|----------------|--------|
| hero_range_percentile | feature_extractor.py, feature_keys.py | No (adds column, old models ignore) | Medium — wire existing function |
| has_showdown_value | feature_extractor.py (add_derived_features) | No | Trivial — 1 line |
| villain_fold_equity_estimate | feature_extractor.py (add_derived_features) | No | Trivial — 3 lines |

All 3 features are additive — existing models continue to work.
New models trained on 51 features will use them. Old training data
needs the 3 columns appended (hero_range_percentile requires
recomputation; the other 2 are derivable from existing columns).

---

## Recommendation

Add all 3 features BEFORE the factory rebuild. This means:
1. Implement features #49-51 in feature_extractor.py
2. Regenerate factory data with 51-feature vectors
3. Relabel with updated feature context
4. Train v3.1 on 51 features

The `hero_range_percentile` is the highest-impact addition. If only
one feature can be added, add that one.

---

## Research finding to LOG (not implement now)

"The strongest draws are NOT the best bluffs" (GTO Wizard). This
CONTRADICTS KB Section 1.7 which frames nut draws as the primary
raise candidates. The solver raises nut draws for equity + fold
equity combined. But the research shows that pure bluff selection
prefers WEAKER draws that need fold equity. This is a KB v1.3
discussion item — the Section 1.7 framing may need to distinguish
"semi-bluff raise" (strong draw, equity-driven) from "pure bluff
raise" (weak hand, fold-equity-driven).
