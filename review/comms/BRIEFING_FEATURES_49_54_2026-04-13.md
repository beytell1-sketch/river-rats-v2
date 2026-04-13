---
date: 2026-04-13
from: Owner + Main terminal
to: Builder team (Architecture Expert, ML Architect, GTO Expert)
re: Promote features 49-53 + add feature 54 — include in v2.2?
status: FOR EXPERT INPUT — not a directive yet
---

# Feature Promotion Briefing: 48 → 54 for v2.2

## 0. Context

Features 49-53 are already coded in `feature_extractor.py` and
`feature_keys.py`. They were deferred from v2.2 training to limit
scope. Feature 54 is new but trivial to implement (~5 lines).

The v2.2 rebuild re-extracts all 200 reconstructed situations and
generates ~185 new ones through the factory. The model trains from
scratch. There is no warm-start compatibility concern.

The question: should we promote all 6 to training features now,
or keep them deferred?

## 1. The features

### Already coded, currently deferred

| # | Feature | Type | What it does |
|---|---|---|---|
| 49 | `hero_range_percentile` | Float 0.0-1.0 | Where hero's hand sits within their own range on this board. 1.0 = top of range. |
| 50 | `has_showdown_value` | Binary | Is this hand worth seeing a showdown? (bottom pair or better, derived from `is_made_hand` and `hand_category >= 3`) |
| 51 | `villain_fold_equity_estimate` | Float 0.0-1.0 | Estimated probability all opponents fold to a bet. Computed from `villain_top_pair_plus_pct` and `villain_draw_pct`. |
| 52 | `flush_draw_rank` | Int 0-14 | Rank of hero's highest card in the board's flush suit. 0 = no card in flush suit. 14 = ace of flush suit (nut flush draw). |
| 53 | `is_preflop_aggressor` | Binary | Was hero the preflop raiser? `int(hero_position == opener_position)` |

### New — not yet coded

| # | Feature | Type | What it does |
|---|---|---|---|
| 54 | `villain_medium_made_pct` | Float 0.0-1.0 | % of villain's range that is made hands below top pair (second pair, bottom pair, weak top pair). Currently this category is silently dropped at line 1173 of `feature_extractor.py` — the composition triple doesn't add to 100%. |

## 2. Why this matters now

### The composition gap (feature 54)

The current villain range composition is:

```
villain_top_pair_plus_pct + villain_draw_pct + villain_air_pct ≠ 100%
```

Medium and weak made hands fall through all three buckets. If
villain's range is 20% TP+, 15% draws, 30% air, and 35% medium
made — the model sees 20/15/30 and the missing 35% is invisible.

This matters most for:
- **Thin value decisions:** Is there a population of worse made
  hands that will call? The model can't answer this without
  knowing `villain_medium_made_pct`.
- **Bucket-first labelling:** Agents classify hero's hand into
  buckets (monster/strong/medium/weak/drawing/air). The villain
  range should be described in compatible terms. Currently it
  has a hole where medium/weak made should be.

### Features that directly support v2.2 goals

| Feature | Supports |
|---|---|
| 52 (`flush_draw_rank`) | BP7 RAISE situations — nut flush draw vs weak draw is the difference between RAISE and CALL. Without this feature the model can't distinguish them. |
| 51 (`villain_fold_equity_estimate`) | Semi-bluff raise decisions — the model needs fold equity to evaluate RAISE for drawing hands. |
| 49 (`hero_range_percentile`) | Thin value vs check — "am I near the top or bottom of my range?" is the bucket-first question for medium made hands. |
| 53 (`is_preflop_aggressor`) | C-bet vs defender play — fundamentally different strategies. Teaching team already flagged this gap (TEACHING_TEAM_PFA_CROSS_REFERENCE). |
| 50 (`has_showdown_value`) | Check decisions — separates "check to see showdown" from "check because we have nothing." |
| 54 (`villain_medium_made_pct`) | Completes villain composition. Enables accurate value target assessment. |

### Why NOW, not v2.3

- All situations are re-extracted anyway (Phase 1C done, Phase
  2B pending). Zero incremental extraction cost.
- Model trains from scratch. No compatibility concern.
- Labelling agents see a richer feature vector — better informed
  decisions, especially for the new RAISE and thin value spots.
- Features 49-52 are already coded. Feature 53 is already coded.
  Feature 54 is ~5 lines.
- **If we defer and v2.2 accuracy is limited by missing features,
  we retrain for v2.3 anyway.** Adding them now avoids a wasted
  training cycle.

### Additional benefit: expert feature attention

The enriched labelling output includes `feature_attention` —
labelling agents tag which features drove their decision. If
features 49-54 are available, agents can tag them as PRIMARY
when relevant (e.g., `flush_draw_rank: PRIMARY` for a semi-bluff
raise decision). This gives us attention data on the new features
from day one.

If we defer the features, agents can't tag what they can't see.
We lose a full batch of attention data on features that matter
most for the new decision types (RAISE, thin value, c-bet).

## 3. Questions for experts

### Architecture Expert

1. Features 49-52 are in `feature_keys.py` but NOT in the
   training `FEATURE_COLUMNS` list in `train_model.py` (line 28).
   Is promoting them just adding 4 strings to that list, or are
   there other touchpoints (gto_model.py, coaching pipeline,
   sizing oracle)?
2. Feature 54 requires changing the range classification at
   line 1167-1173 of `feature_extractor.py` to capture the
   medium/weak category instead of dropping it. Any downstream
   impact?
3. `gto_model.py` line 60 says `N_FEATURES = 53`. Does it
   auto-detect from `FEATURE_COLUMNS` or is this hardcoded?

### ML Architect

1. Going from 48 to 54 features on ~385 training rows — any
   concern about feature-to-sample ratio? Standard guidance is
   10-20 samples per feature minimum. At 385 rows / 54 features
   = 7.1 ratio. Is this tight?
2. Feature 51 (`villain_fold_equity_estimate`) is derived from
   features that are already in the vector (`villain_top_pair_plus_pct`,
   `villain_draw_pct`, `num_opponents`). XGBoost can learn this
   interaction. Does the explicit derived feature add value, or
   is it redundant?
3. Should any of these go through an ablation study first, or
   is the from-scratch training + 5-fold CV sufficient to judge
   their contribution?
4. Feature 54 changes the interpretation of the existing
   composition features — `villain_air_pct` was absorbing some
   medium made hands (because they fell through). After fixing,
   `villain_air_pct` drops and `villain_medium_made_pct` appears.
   Does this create a distribution shift the model needs to
   handle?

### GTO Expert

1. Are these the right 6 features to add? Any other gap in the
   48-feature vector that matters more for bucket-first labelling?
2. For feature 54 — should it be a single `villain_medium_made_pct`
   that covers everything between TP+ and air/draws? Or split
   into `villain_medium_made_pct` (second pair, marginal TP) and
   `villain_weak_made_pct` (bottom pair, third pair)?
3. Does `has_showdown_value` (feature 50) add anything that
   `is_made_hand` + `hand_category` don't already provide?
4. Will labelling agents actually use `hero_range_percentile`
   (feature 49) in their reasoning, or will they ignore a
   0.0-1.0 float and reason from hand_category instead?

## 4. What we're NOT asking

- We're not asking to change the v2.2 plan structure (phases,
  gates, agent counts).
- We're not asking to add features that don't already exist in
  code (except feature 54, which is ~5 lines).
- We're not asking for a separate feature engineering sprint.
  This is: should we flip the switch on features already built?

---

**Builder: please have all three experts respond. Short
assessments (half page each) to review/comms/. This feeds
directly into the Phase 2B generation and Phase 3A prompt
update — we need the answer before those steps execute.**
