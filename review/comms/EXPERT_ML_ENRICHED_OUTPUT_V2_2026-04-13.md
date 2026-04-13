---
date: 2026-04-13
from: ML Architect
to: Owner (Rupert) + Builder team
re: REVISED ML assessment — Phase 3A enriched labelling (post-clarification)
status: EXPERT ASSESSMENT V2 — supersedes EXPERT_ML_ENRICHED_OUTPUT_2026-04-13.md
---

# ML Architect Revised Assessment: Enriched Output (Post-Clarification)

---

## 1. Emergent vocabulary — does it change ML feasibility?

Yes, materially for the better.

A pre-defined 15-category taxonomy risks label pollution: agents force-fit
decisions into ill-fitting categories, producing noisy positives. An emergent
vocabulary grown from 50 actual hands means every tag that exists has at least
one natural example. Tags that nobody uses simply don't appear. That removes
the low-frequency phantom problem from the schema side.

What it does NOT remove is the data volume problem. With a vocabulary that
stabilises at 10-20 tags and 385 total rows, the distribution still determines
what is learnable. Rough expectation at 385 rows:

- 3-4 tags covering frequent situations (e.g., value_thin, protect_equity,
  pot_control) will clear 50+ examples. These are trainable at v2.3.
- 4-6 tags covering moderate situations will land 20-50 examples. Trainable
  with class weighting; expect wider confidence intervals.
- Remaining tags (3-8) will be below 20 examples. Not trainable — data
  collection only.

The emergent process helps because the top tags will be genuinely frequent
(they earned their place by appearing repeatedly). A pre-defined list has no
such filter. Net effect: the trainable fraction of the vocabulary is larger
under emergent design. Still not a full-vocabulary model at v2.3, but better.

---

## 2. "Reason first, tag second" — better or worse training signal?

Better, with one risk.

Anchoring risk: agents who reason to a conclusion before selecting a tag are
less likely to pick the nearest-sounding label and more likely to pick the
correct one. The reasoning acts as a forced self-consistency check. This
produces higher-quality labels for the tags that ARE selected.

Consistency risk: different agents may reason to the same conclusion but
describe it with slightly different language, then map to different tags.
This is the real danger in the first 50-hand batch. Mitigate it during the
stabilisation review by looking for tag pairs that consistently appear
together or on semantically identical hands — those should be merged.

Overall verdict: reason-first produces better per-label quality than pick-
from-list, at the cost of needing a careful vocabulary consolidation pass
after the first batch. That pass is already planned. Run it.

---

## 3. Street plans as tags — does the "defer classifier" recommendation change?

Yes. The original recommendation to defer was specifically about text
classification (unreliable at 385 rows, requires 200-400 examples per
category). Tags eliminate that problem entirely.

If street_plan is a constrained tag set (`barrel_value`, `check_evaluate`,
`draw_implied`, etc.) emerging from the same process as intention tags, it is
already classified. No classifier needed. The tag IS the class label.

Revised recommendation: collect street_plan tags in v2.2 labelling. Treat
them exactly like intention tags — emergent vocabulary, stabilise after 50
hands, train the v2.3 model on tags that clear the 30-example threshold. The
previous "defer to v2.4" recommendation for plan classification is withdrawn.

The free-text plan field still has value as a teaching output (the oracle
surfaces the text to the player), but the ML target is the tag, not the text.

---

## 4. Tag frequency imbalance — how to handle it

Three tiers:

- Below 20 examples: do not train. Include in data collection, exclude from
  v2.3 model training. Flag for v2.4.
- 20-50 examples: train with class_weight="balanced" in sklearn, or
  scale_pos_weight in XGBoost. Set a minimum precision threshold of 0.60
  before deploying — below that, the classifier is worse than a frequency
  prior.
- Above 50 examples: train normally. These will be reliable.

Do not use a fixed frequency cutoff decided now. After labelling completes,
count actual tag frequencies, apply the tiers, and select which heads to
train. The vocabulary stabilisation review is the right moment to make this
decision with real numbers.

---

## 5. Should we train Model 2 on v2.2 data (385 rows) as an experiment?

Yes — but scoped correctly.

Train only the tags that clear 30 examples (expect 4-7 of them). Treat it
explicitly as a feasibility experiment, not a production model. The value
is not the model itself but the answers it produces:

- Which intention tags are actually separable from 48 features?
- Does SHAP alignment between Model 1 and Model 2 hold for the same hands?
- Are there features that predict intention but not action (or vice versa)?

These questions are worth answering at 385 rows even if the classifiers are
noisy, because the answers inform v2.3 design. A multi-label model trained on
4 reliable tags is a legitimate experiment. Label it as such in the model
registry. Do not deploy it as the teaching oracle — Model 1 + intention tags
as lookup text is the teaching oracle at this stage.

---

## Summary: what is learnable vs noise at 385 rows

| Target | Learnable at v2.3? | Condition |
|---|---|---|
| Action (5-class) | YES | Already proven in v8/v9 |
| Intention tags (top 4-7) | YES — experiment | Clear 30-example threshold |
| Intention tags (tail) | NO | Data collection only |
| Street plan tags (top 4-6) | YES — experiment | Same threshold applies |
| Street plan tags (tail) | NO | Data collection only |
| Feature attention (SHAP compare) | YES — analysis step | Free post-v2.2 train |

The constraint is not the emergent vocabulary design (good). The constraint
is 385 rows. That number limits the trainable frontier to the top half of the
tag vocabulary. Collect everything; train selectively.
