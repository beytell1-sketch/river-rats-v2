---
date: 2026-04-13
from: ML Architect
to: Owner + Builder team
re: ML assessment — features 49-54 for v2.2 training
---

# ML Assessment: Features 49-54

## Q1. Feature-to-sample ratio at 385/54 = 7.1

Tight but acceptable for XGBoost specifically. The 10-20 rule applies to
parametric models (logistic regression, linear SVM). XGBoost is a
tree ensemble — it learns from splits, not parameters per feature.
With default depth-3 trees and 100-300 estimators, the effective
parameter count is far lower than 54. The practical floor for XGBoost
on a 5-class classification is roughly 5-7 samples per feature; 7.1
clears this. The real risk is not underfitting — it is class imbalance
within folds. If any class has fewer than ~30 rows total, 5-fold CV
will produce folds with 0-2 examples of that class, and per-class
metrics will be noisy. Check class counts before training and apply
stratified CV. If any class is below 30 rows, weight it via
`scale_pos_weight` or merge into the nearest class for the v2.2 run.

**Verdict: ratio is not a blocker. Stratified CV is mandatory.**

## Q2. Is feature 51 (villain_fold_equity_estimate) redundant?

Partially. XGBoost can learn `f(villain_top_pair_plus_pct,
villain_draw_pct)` on its own if the interaction appears frequently
enough in the training data. At 385 rows it may not see the interaction
sufficient times to reliably split on it. The explicit derived feature
pre-computes that interaction and makes it available at every node
without requiring a depth-2 split to recover it. On small datasets,
explicit interaction features consistently outperform relying on the
tree to discover them.

However: if `villain_fold_equity_estimate` is a simple linear
combination of its parents (e.g., `1 - top_pair_plus - draw`), it
adds zero information beyond `villain_air_pct`. Confirm the formula.
If it is a nonlinear composite (e.g., product or capped estimate), it
earns its place. If it is linear, drop it and rely on the components —
the added column will have exactly zero gain in the importance plot and
will only confuse the attention tagging.

**Verdict: include if formula is nonlinear. Drop if it equals
`1 - villain_top_pair_plus_pct - villain_draw_pct`.**

## Q3. Ablation study vs 5-fold CV

Ablation is not needed before v2.2 training. It is appropriate after.
All 6 features have a clear GTO motivation (per the briefing). Given
from-scratch training and the full re-extraction, run with all 6 and
read feature importance and permutation importance post-training. Any
feature with near-zero gain and near-zero permutation importance should
be flagged for removal in v2.3. Full ablation (retrain 6 times, one
feature dropped each) costs 6x training time and is disproportionate
at this dataset size — importance plots give the same signal at 1x
cost.

**Verdict: 5-fold stratified CV now. Importance-based ablation after
v2.2 trains.**

## Q4. Distribution shift from fixing feature 54

Yes, this is a real shift and it is the right kind. `villain_air_pct`
was artificially inflated (absorbed ~35% medium made hands). After the
fix it drops to its true value and `villain_medium_made_pct` carries
that mass. Because the model trains from scratch on the corrected
values, there is no backward-compatibility problem. The model will
learn the correct joint distribution of all four composition features.

The only risk is labelling consistency: if any training rows were
labelled under the old (broken) composition and the new rows are
labelled under the corrected composition, the feature values will be
inconsistent within the training set. Since all 385 rows are being
re-extracted from scratch (Phase 1C done, Phase 2B pending), this is
not an issue — all rows see the corrected extractor. There is no
mixed-vintage problem.

**Verdict: no concern given full re-extraction. Do not mix old-extract
rows with new-extract rows in the v2.2 training set.**

## Q5. Net recommendation

Include all 6. Conditions:

- Confirm feature 51 formula is nonlinear before training. If linear,
  drop it.
- Verify stratified class distribution before training. Flag any class
  below 30 rows.
- Re-extract all training rows with the corrected extractor (no
  mixed-vintage rows).
- Read feature importance after training. Any feature at zero gain for
  two consecutive models is a v2.3 cut candidate.

The argument for deferral — "wait for more data" — does not apply here
because the data is being re-generated anyway and the model trains from
scratch. Deferral only makes sense when adding features would require
re-extracting a stable corpus. That condition does not hold.
