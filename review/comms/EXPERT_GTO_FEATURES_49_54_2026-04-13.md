---
date: 2026-04-13
from: GTO Expert
to: Builder team
re: Feature promotion 49-54 — GTO assessment
---

# GTO Expert: Features 49–54 Assessment

## Q1. Are these the right 6 features? Any bigger gap?

Yes, these are the right 6. The most painful gap in the current 48 is the villain
composition hole (feature 54). The second most painful is the PFA gap (53) — c-bet
vs. in-position-call-versus-3bet are structurally different strategies and the model
currently conflates them.

One gap that is NOT addressed: position relative to the betting player in multiway
pots. The existing `position_vs_dealer` feature captures absolute seat but not
whether hero is sandwiched (action behind) vs. closing. The three_way_gto.md section
1.5 shows sandwich EQR is the worst seat and heuristics fail there. This is the next
feature worth adding after v2.2 — it is not in the current 48 and is not trivial to
derive. Flag for v2.3 only.

## Q2. Feature 54: single or split (medium + weak)?

Single `villain_medium_made_pct`. Do not split.

At 385 training rows, splitting costs a feature slot for marginal gain. The key
question the model needs to answer for thin value is "is there a population of worse
made hands that will call?" — second pair and bottom pair both answer YES to that
question. The granularity that matters is TP+ (will re-raise or call strong) vs.
medium made (will call a bet) vs. air/draws (folds or has equity). The TP+/medium/
draw/air four-bucket composition is the right resolution. Second pair vs. bottom pair
distinction is not load-bearing at v2.2 scale.

## Q3. Does has_showdown_value (50) add anything over is_made_hand + hand_category?

Marginal. It is a convenience binary derived entirely from `is_made_hand` and
`hand_category >= 3`. XGBoost will learn this interaction from the existing features.
The only case where it adds signal is if hand_category is noisy or missing, which
it should not be. The real value is for the labelling agent, not the model: the
explicit binary makes "this hand is worth seeing a showdown" immediately readable
in the feature vector when an agent is reasoning about CHECK vs. BET decisions.

Verdict: include it. The agent attention data is worth the one feature slot, and
the redundancy cost is near zero at this scale.

## Q4. Will agents actually use hero_range_percentile (49)?

Yes — but only if the prompt makes it explicit. Left to their own devices, agents
reason from hand_category (a readable category) and will anchor on that. The float
0.0–1.0 is only useful if the agent prompt names the feature and explains what it
means: "1.0 = top of your range on this board, 0.0 = bottom." Without that framing
agents will deprioritise an unlabelled float.

The feature is correct and important for thin value decisions (am I at the top or
bottom of my medium-made range?). It must be named and explained in the v2.2
labelling agent prompt, otherwise it will appear in feature_attention logs at near
zero frequency.

## Q5. Most important features for bucket-first RAISE and thin value

**For RAISE decisions:**
1. `flush_draw_rank` (52) — nut flush draw vs. weak flush draw is the single biggest
   binary in semi-bluff raise logic 3-way. Without it the model cannot distinguish
   BP7-eligible raises from check/folds.
2. `villain_fold_equity_estimate` (51) — RAISE for a drawing hand only makes sense
   with fold equity. The existing composition features give the model the raw
   ingredients; the derived estimate makes the conclusion explicit.
3. `is_preflop_aggressor` (53) — determines whether hero has a credible raising range
   at all on this texture.

**For thin value decisions:**
1. `villain_medium_made_pct` (54) — the direct answer to "who calls a thin bet?" If
   this is zero, thin value is unambiguous bluff territory. If it is 30%+, a
   small bet has value targets.
2. `hero_range_percentile` (49) — "am I top or bottom of my medium-made range?"
   Combined with villain_medium_made_pct, this is the complete thin value question.
3. `has_showdown_value` (50) — separates "check to realize equity" from "bet thin."

**Promote all 6.** The cost of deferring and retraining outweighs any scope concern.
