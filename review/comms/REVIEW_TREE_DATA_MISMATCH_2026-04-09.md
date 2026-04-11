# Review: BET Tree Threshold Mismatches

**Reviewer:** Process reviewer
**Date:** 9 April 2026
**File reviewed:** review/comms/TREE_DATA_MISMATCH_2026-04-09.md

**VERDICT: BLOCKER — must fix before labelling**

---

## Assessment

This is exactly the kind of finding the deterministic script was
built to catch. Two thresholds in the BET tree are calibrated
against assumed feature ranges that don't match reality. Steps 3-6
are structurally dead — they can never fire. The result: 1.6% BET
rate instead of the expected 9-14%.

The builder is right: LLM agents would have masked this by loosely
interpreting "board favours hero" without hitting the exact numeric
threshold. The deterministic approach exposed a real gap in the
tree design.

## Process observation

**[SHOULD_FIX] The GTO Expert designed thresholds without verifying
feature ranges.** This is a §7 common mistake ("Feature addition
without data consistency check") applied in reverse — the tree
used features without checking their encoding. The fix is correct:
recalibrate thresholds against actual data.

**The reviewer who checked the BET tree (independent review) also
missed this.** They verified feature NAMES exist in feature_keys.py
but did not verify feature VALUE RANGES match the tree's thresholds.
Future tree reviews should include a range check: for every
threshold in the tree, verify the feature's actual min/max/mean
in the training data.

## On the fix recommendations

**Mismatch 1 (connectivity_score):** Option A (rescale thresholds)
is correct. Don't change the pipeline — change the tree to match
the data. The proposed tiers (2-3, 4-5, 6-7, 8+) need GTO Expert
confirmation that they map to the intended poker concepts (dry,
moderate, connected, very connected).

**Mismatch 2 (board_favour):** Option A (>= 0.10) is reasonable.
14% of situations passing the gate aligns with PFA c-bet frequency
research. But this is a GTO Expert call — the threshold determines
how selective the BET gate is. The expert should confirm 0.10 is
the right cutoff given the feature's actual distribution.

## Recommendation

1. GTO Expert recalibrates both thresholds against actual feature
   distributions
2. Updated BET tree v1.1 produced
3. Independent reviewer verifies the new thresholds fire correctly
   (spot-check: do the right situations now produce BET?)
4. Deterministic script re-runs
5. Then proceed with the phased dual labelling

This should NOT be a quick fix-and-go. The expert needs to look at
the actual feature distributions and set thresholds intentionally,
not just pick the nearest round number.

**Add a new review checklist item for all future tree reviews:**
"For every threshold, verify the feature's actual min/max/mean in
the data. Confirm the threshold falls within the feature's range
and produces the intended selection rate."
