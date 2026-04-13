---
date: 2026-04-13
from: ML Architect
to: Owner (Rupert) + Builder team
re: ML assessment — Phase 3A enriched labelling output (three proposed additions)
status: EXPERT ASSESSMENT — input to owner decision, not a directive
---

# ML Architect Assessment: Enriched Output Additions

## Headline

Two of the three additions have genuine ML value. One is documentation only.
Adopt intentions + feature_attention. Defer street_plan text classification.

---

## 1. Multi-Label Intentions — ADOPT (with constraints)

**Is 385 rows with 15 categories feasible for v2.3?**

No — not as a 15-class multi-label model trained directly. The math is bad.

With 385 rows and a realistic class imbalance, many intention categories will
have fewer than 20 positive examples. The accepted minimum for a reliable
binary classifier head (which is how multi-label works — one binary head per
class) is 30-50 positive examples. At 385 total rows, you can expect the
frequent categories (value_get_worse_to_call, pot_control_medium_hand,
range_fold_action_narrows_above) to hit 50+ examples. The tail categories
(thin_value_target_marginal_calls, trap_induce_villain_bet,
free_card_draw) will likely land below 20. Those tail classifiers will be
noise.

**Minimum per-category count recommendation: 30 positive examples.**

At 385 rows, you can probably train 5-7 reliable intention classifiers — the
ones that cover frequent, well-separated situations. The other 8-10 are data
collection for v2.4+.

**What to do with the data now:** Collect all 15 intention labels in v2.2
labelling regardless. They cost nothing extra to collect and solve a real
teaching problem immediately (see below). Run the v2.3 multi-label model only
on categories that clear the 30-example threshold after labelling completes.

**Immediate value without waiting for v2.3:** The intentions + primary_intention
fields make the teaching oracle substantively better now. "You bet for value
AND protection" is a better coaching output than "strategic_role: protection".
This value is available the moment the labels exist — no new model required.

**The primary_intention scalar field should stay separate from intentions[0].**
Agents will not always list their primary intention first. A separate field
enforces that they explicitly declare it, which is the data you actually need
for teaching. Deriving it as intentions[0] trades away agent clarity for
schema simplicity — wrong trade.

---

## 2. Street Plan Text — COLLECT NOW, CLASSIFY LATER

**Is street_plan text classifiable into plan categories?**

Yes, but not with 385 rows. Text classification of 1-2 sentence plans requires
200-400 examples per category minimum for a fine-tuned classifier to be useful.
At 385 total rows you cannot train a reliable plan classifier.

**How many categories would be learnable?**

With 385 rows the answer is 2-3 if you collapse aggressively (e.g.,
aggressive_barrel vs pot_control vs draw_and_evaluate). A 6-8 category
taxonomy will have most cells empty.

**What to do:** Collect street_plan as free text in v2.2. It has immediate
teaching value — the oracle can surface the plan text directly without any
classifier. Run text classification in v2.4 when training data reaches 800+
rows. Do NOT build a v2.3 plan classifier on 385 rows.

**Risk to flag for GTO Expert:** Street plans will drift toward stock phrases
("bet for protection, re-evaluate turn") if agents are not forced to be
specific about board texture and villain composition. Generic plans are noise.
The GTO Expert should assess whether agents can write situation-specific plans
reliably or will produce boilerplate.

---

## 3. Expert Feature Attention — ADOPT (highest ML value of the three)

**Is expert attention useful as training signal?**

Yes — and it is the most underrated of the three additions. Here is why:

The current model is trained only on labels (what to do). Feature attention
gives you a second training signal: which features the correct reasoning
depends on. For a 53-feature XGBoost model, this is valuable for three reasons:

First, it identifies fragile decisions. If the model weights raw_equity
highly for a protection bet decision but the expert attention says
danger_score + villain_draw_pct are the drivers, the model is using a
proxy feature that will break when raw_equity is high but the board is
safe. Feature attention surfaces this without needing edge cases.

Second, it provides a regularisation signal. Hands where model SHAP and
expert attention agree are well-learned. Hands where they diverge are
candidates for higher training weight in v2.3 (Use 3 from the briefing).
This is a principled approach — better than uniform sample weighting.

Third, it is the correct foundation for the teaching oracle. SHAP values
explain the model. Expert attention explains the reasoning. For coaching,
you want the second.

**How many labelled examples do you need for a "which features matter"
model to be reliable?**

The question is slightly mis-framed. You do not need a separate "which
features matter" model — you need enough attention-labelled hands per
(action + intention) combination to build a lookup-style teaching oracle.
For a teaching oracle (not a classifier), 15-20 examples per bucket is
sufficient to identify which features are consistently flagged. At 385
rows you will have enough for the frequent (action + intention) pairs.

**Is the SHAP-vs-attention comparison (Use 2) straightforward post-training?**

Yes. It is a straightforward analysis step, not a new model. After v2.2 trains:
1. Run SHAP on all training hands (TreeExplainer, already supported by the
   XGBoost model interface exposed in gto_model.py via the .model property).
2. For each hand that has feature_attention labels, rank SHAP values and
   compare top-3 SHAP features against PRIMARY attention features.
3. Compute overlap score per hand, flag divergences.

This is a pandas + shap operation, maybe 50 lines. The only complexity is
normalising feature names consistently (SHAP returns feature indices; the
FEATURE_COLUMNS tuple in gto_model.py maps these to names). This is already
in place.

**Schema note for Architecture Expert:** A simple list of PRIMARY feature
names is cleaner than a full attention dict with PRIMARY/SUPPORTING levels
for storage, but the dict is better for the SHAP comparison because
SUPPORTING features can be used to validate that lower-ranked SHAP values
are at least in the expected neighbourhood. Keep the dict.

---

## Summary Table

| Addition | Collect in v2.2? | ML value | When to model |
|---|---|---|---|
| intentions (multi-label) | YES | HIGH — teaching oracle immediately; v2.3 model for 5-7 frequent categories | v2.3 (threshold: 30 examples/category) |
| primary_intention | YES | HIGH — required field, not derivable | Teaching oracle v2.2 |
| feature_attention | YES | HIGHEST — SHAP comparison free post-v2.2 train; teaching oracle grounded in expert reasoning | Use 2 post-v2.2; Use 1 in v2.3 |
| street_plan (text) | YES | MEDIUM now (teaching text), LOW for ML | Text classifier not before 800 rows |

**What is noise:** Trying to train a 15-class intention model on 385 rows.
Trying to build a plan classifier before 800 rows. Both should be explicitly
deferred rather than attempted and discarded.

**What is signal:** Collecting all three fields now. The teaching value of
intentions and street_plan is immediate without any new model. The
feature_attention SHAP comparison is free after v2.2 trains and directly
answers whether the model learned the right reasoning or a proxy.
