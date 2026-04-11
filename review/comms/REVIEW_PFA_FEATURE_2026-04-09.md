# Review: PFA Feature Decision

**Reviewer:** Process reviewer
**Date:** 9 April 2026
**Files reviewed:**
- review/comms/PFA_FEATURE_ASSESSMENT_2026-04-09.md (initial: defer)
- review/comms/GTO_EXPERT_PFA_BLUFF_ASSESSMENT_2026-04-09.md (rebuttal: add now)

**VERDICT: Both assessments are well-reasoned. Owner decision needed.**

---

## The tension

The ML-architect says: the signal is already captured through 3
derived features (board_favour, hero_range_percentile, 
villain_fold_equity_estimate). Adding a raw binary risks
multicollinearity. Defer and test empirically in v3.2.

The GTO Expert says: the derived features capture the RESULT of PFA
advantage but not the CAUSE. A defender-hero can produce identical
feature values on the right board, and the correct action diverges.
The model can't separate the two without knowing who raised. This
is structural, not marginal.

## Process observations

**[NOTE] The builder reversed their own recommendation based on new
expert input.** The initial assessment said defer. The GTO Expert's
structural argument changed the recommendation to add now. This is
good process — the builder didn't anchor to their first position.

**[NOTE] The GTO Expert's analysis is specific and testable.** They
constructed a concrete scenario (defender BB on Kh 4d 2c with
positive board_favour) where the feature vectors are
indistinguishable from PFA bluff but the correct action differs.
This is the right way to identify a feature gap.

**[NOTE] The ML-architect's multicollinearity concern is valid in
general but may not apply here.** Multicollinearity is a problem
when features are linearly correlated. is_preflop_aggressor
interacts with board_favour — the interaction term (PFA × 
board_favour) is what matters, not the main effect. XGBoost handles
interaction terms natively through tree splits. The risk is not
multicollinearity but redundancy — and the GTO Expert showed it's
not redundant.

## The timing question

The builder says adding now costs ~1 hour of pipeline work and
avoids relabelling everything in v3.2. The ML-architect says adding
mid-pipeline violates §7 (feature addition without consistency 
check). Both are right — but the labelling hasn't started yet. The
pipeline is at the exact point where adding a feature is cheapest.
After labelling 563 situations, adding it means relabelling.

## What I can't decide

This is a genuine trade-off between two expert positions:
- Ship v3.1 with 52 features, test PFA empirically in v3.2
- Add feature 53 now, regenerate, update tree, label once

Both are defensible. The GTO Expert's structural argument is
stronger than the ML-architect's statistical argument, but "stronger
argument" doesn't mean "certain." The model might learn the
distinction from derived features alone — that's an empirical claim
neither expert can prove without training.

## Recommendation

This is an owner decision, not a technical one. The experts
disagree. The trade-off is:
- Add now: more work upfront, guaranteed the model has the signal
- Defer: less disruption, risk of discovering the gap in v3.2

Both positions were presented with reasoning, not as menus. The
builder's updated recommendation (add now) has the stronger poker
argument. The ML-architect's concern (test empirically) is prudent
but risks wasting the labelling effort if the gap proves real.

Your call.
