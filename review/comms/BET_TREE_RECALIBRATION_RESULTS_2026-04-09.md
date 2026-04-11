# BET Tree Recalibration — Run Results
**Author:** Lead Programmer
**Date:** 9 April 2026
**Status:** COMPLETE — findings require owner decision before next action

---

## What Was Done

All threshold changes from BET_TREE_RECALIBRATION_2026-04-09.md were applied
to both:

- `review/BET_DECISION_TREE_V1.md` — all threshold and Feature Reference updates
- `review/deterministic_labeller.py` — apply_bet_tree function updated to match

The deterministic labeller was then re-run on all 563 situations.

---

## Changes Applied (confirmed)

### BET_DECISION_TREE_V1.md

| Location | Old | New |
|----------|-----|-----|
| Step 3 primary condition | `board_favour >= 0.20` | `high_card_rank >= 12` |
| Step 3B OOP strict condition | `board_favour >= 0.35` | `high_card_rank >= 13` |
| Step 4 primary condition | `board_favour >= 0.20` | `high_card_rank >= 12` |
| Step 3A Gate 3A-1 | `connectivity_score <= 0.65` | `connectivity_score <= 6` |
| Step 3A Tier 1 | `connectivity_score <= 0.30` | `connectivity_score <= 3` |
| Step 3A Tier 2 | `connectivity_score <= 0.55` | `connectivity_score <= 5` |
| Step 3A Tier 3 | `connectivity_score <= 0.70` | `connectivity_score <= 7` |
| Step 6 | `connectivity_score <= 0.25` | `connectivity_score <= 3` |
| Feature Reference: connectivity_score | 0.0-1.0 | 0-10 integer (observed 2-8) |
| Feature Reference: board_favour | primary gate | [DEMOTED] |
| Feature Reference: high_card_rank | secondary | [PROMOTED] primary gate |

### deterministic_labeller.py

All equivalent code changes applied. Comments updated to remove stale
references to board_favour thresholds throughout apply_bet_tree.

---

## Run Results

```
=== ACTION DISTRIBUTION ===
  BET          9  (  1.6%)
  CALL       240  ( 42.6%)
  CHECK      137  ( 24.3%)
  FOLD       106  ( 18.8%)
  RAISE       71  ( 12.6%)

=== TREE USAGE ===
  bet_tree              146  ( 25.9%)
  fold_tree             346  ( 61.5%)
  raise_tree             71  ( 12.6%)

=== STEP FREQUENCY (bet tree steps only) ===
   60   Step 7 default CHECK
   46   S2 OOP suppressor (no override step fired)
   29   S3 multi-street aggressor suppressor
    9   Step 2 monster protection bet
    2   S1 wet board bluff suppressor
```

BET rate: 1.6% (unchanged from pre-recalibration).

Sanity checks: PASSED (all 563 valid actions, correct tree/action consistency).

---

## Why BET Rate Did Not Improve

The recalibration was applied correctly. The thresholds are now on the right
scale. The BET rate did not improve because the blocking conditions are NOT
the connectivity_score or board_favour thresholds — they are structural data
coverage problems that the recalibration cannot fix.

### Finding 1: Step 3A — No IP PFA situations exist

Step 3A requires `is_preflop_aggressor == 1` AND `is_ip == 1`.

The BET situation dataset (n=146) contains only 8 IP situations total.
Of those 8, zero are PFA. All 19 PFA + made hand + hcr>=12 situations are OOP.

Step 3A cannot fire until the factory generates IP PFA situations.

### Finding 2: Step 3B — villain_air_pct never reaches the 0.40 threshold

The 19 OOP PFA made-hand candidates (the Step 3B pool) have villain_air_pct
clustered at exactly two values: 0.162 and 0.297. Neither reaches 0.40.

Step 3B requires villain_air_pct >= 0.40. Every candidate fails this gate.
Secondary failures: most also fail hand_category >= 7 (many are middle pair
or worse) and hero_range_percentile >= 0.72.

Step 3B cannot fire with the current factory data.

### Finding 3: Step 4 — All PFA no-made-hand candidates are OOP and suppressed

The 6 PFA + no-made-hand + hcr>=12 candidates are all OOP. All have
s2_fires=True (S2 OOP suppressor active: hero_range_percentile < 0.72,
raw_equity < 0.60 in every case).

The only sub-condition that overrides S2 for OOP is 4A (combo draw, do>=12).
None of the 6 candidates have draw_outs >= 12 (max observed: 8).

Step 4 cannot fire without either IP PFA situations or OOP PFA hands with 12+
draw outs.

### Finding 4: Step 5 — Zero IP made-hand situations with hand_category >= 7

Of the 8 IP situations in the BET dataset, none are made hands with
hand_category >= 7. Step 5's partial match breaks at the very first gate.

Step 5 cannot fire without more IP made-hand situations in the factory.

### Finding 5: Step 6 — villain_aggression_count is always >= 1 for near-miss candidates

8 situations pass through all Step 6 gates up to and including hand_category >= 8
(the second-to-last condition). All 8 are blocked by villain_aggression_count == 1
(the step requires == 0).

villain_fold_equity_estimate is actually fine (0.266-0.745) for these candidates.
The single blocking feature is villain_aggression_count.

Step 6 cannot fire unless the factory produces OOP situations where villain has
not shown aggression.

---

## Steps That Never Fire — Flag for Review

| Step | Blocking Condition | Root Cause |
|------|-------------------|-----------|
| Step 3A | No IP PFA situations | Factory data: PFA hands are always OOP in current dataset |
| Step 3B | villain_air_pct <= 0.297 (never reaches 0.40) | Factory: villain range computation produces degenerate air_pct for PFA spots |
| Step 4A-D | All OOP + suppressed; no 12+ out draws | Factory: PFA no-made hands are OOP with weak draw equity |
| Step 5 | Zero IP made-hand situations with hcat>=7 | Factory: IP situations are rare and don't overlap with made hands |
| Step 6 | villain_aggression_count always >= 1 for eligible OOP candidates | Factory: villain always shows some street aggression in generated spots |

Step 2 (monster protection bet) fires correctly: 9 situations, 1.6%.

---

## What This Means

The recalibration from GTO Expert was correct. The thresholds are now on the
right scale. The problem is not the threshold values — it is that the factory
situations fed into the labeller do not contain the situational variety needed
to trigger BET outcomes.

Specifically:
1. 95% of BET situations (138/146) are OOP. The tree's best BET generators
   (Steps 3A, 4B-4D, 5) require IP positions.
2. villain_air_pct is degenerate for PFA spots (noted in the recalibration doc
   as a factory design issue — now confirmed to block Step 3B entirely).
3. villain_aggression_count >= 1 is effectively universal for the Step 6 pool.

This is a factory coverage gap, not a threshold gap.

---

## Decision Required

The owner needs to decide how to proceed:

**Option A: Accept the current BET rate and continue**
The 1.6% BET rate (9 labels) is too low to train a meaningful BET classifier.
The model will not learn IP PFA c-bet patterns.

**Option B: Regenerate factory situations with balanced position coverage**
The factory appears to generate predominantly OOP hero situations. Regenerating
with explicit IP coverage targets (e.g., 50% IP) would expose Steps 3A, 4B-D,
and 5 to matching situations.

**Option C: Audit villain_air_pct and villain_aggression_count computation**
Steps 3B and 6 are close to firing. Fixing the factory's villain range
computation (villain_air_pct too low for PFA spots; villain_aggression_count
always >= 1 for OOP near-misses) would unlock these steps without requiring
a full regeneration.

**Option D: Combine B and C**
Both position balance and villain feature accuracy need fixing. This is
the most complete solution.

---

## Files Modified

- `/home/rupertbeytell/river-rats-v2/review/BET_DECISION_TREE_V1.md`
- `/home/rupertbeytell/river-rats-v2/review/deterministic_labeller.py`
- `/home/rupertbeytell/river-rats-v2/review/deterministic_labels.json` (re-run output)

---

*Written to: review/comms/BET_TREE_RECALIBRATION_RESULTS_2026-04-09.md*
