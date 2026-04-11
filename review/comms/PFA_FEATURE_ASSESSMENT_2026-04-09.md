---
date: 2026-04-09
from: Builder (GTO Expert + ML-architect + architect assessment)
re: is_preflop_aggressor feature — assessment
---

## Assessment: Defer to v3.2. Does not block Step 7.

---

## Question 1: Does it add signal beyond board_favour?

**Yes, but not much in the current architecture.**

`board_favour` is computed from villain's top_pair_plus_pct split — it
measures whether the board texture favours hero's range or villain's.
It indirectly captures PFA advantage because the PFA's wider range
hits more boards, but it doesn't distinguish WHY hero's range is
favoured.

`is_preflop_aggressor` would add one bit of information: did hero open
or defend? This matters because:
- PFA has uncapped range (can have AA, KK, AKs) → c-bet more
- Defender has capped range (3-bet with premiums) → check more
- The same top pair on the same board plays differently depending on
  which side hero is on

However: the current feature extractor ALREADY uses opener_pos
internally to construct hero's range for hero_range_percentile
(line 1508-1512). The model sees the EFFECT of being PFA through
percentile, fold_equity, and board_favour — it just doesn't see the
raw fact.

**ML-architect view:** Adding a binary feature that's already captured
through 3+ derived features risks multicollinearity without adding
discriminative power. The gradient will be near-zero if the derived
features already explain the variance. Test needed: train with and
without, compare feature importance. But this is a v3.2 experiment,
not a v3.1 blocker.

## Question 2: Feature-visible for labelling?

**Yes, trivially.** The action_history in every SituationSpec records
preflop actions. hero_pos + action_history → is_hero_PFA is a
one-line extraction. The data is already there.

## Question 3: Does it interact with the RAISE decision tree?

**Not directly.** The v2 tree's conditions are:
- is_monster, hand_category, hero_range_percentile, spr, flush_danger,
  villain_fold_equity_estimate, etc.

None of these reference PFA status. The tree would need a new branch
like "Step 2.5: PFA on dry board → lower threshold for value bet"
to use it. That's a tree redesign, not a tree fix.

The tree was designed to be feature-complete with 52 features. Adding
feature 53 without a corresponding tree branch means the labelling
process can't use it. It would only help the ML model's internal
discrimination.

## Question 4: Is the data already there?

**Yes.** `opener_position` is stored in every SituationSpec and passed
through the pipeline. Extracting `is_preflop_aggressor = int(hero_pos
== opener_position)` is trivial. The factory situations already have
opener_position.

## Timing assessment

Adding this feature NOW would require:
1. Add feature 53 to feature_extractor.py + feature_keys.py
2. Update gto_model.py FEATURE_COLUMNS (52 → 53)
3. Regenerate ALL factory situations (batch 1, 2, 3) — ~3 hours
4. Potentially update the decision tree
5. Re-run calibration (KB checksum changed)
6. Re-run all downstream steps

**This is a v3.2 task, not a v3.1 task.** The current 52-feature
pipeline is tested, validated, and ready to label. Adding a feature
mid-pipeline is the exact pattern the Process Guide warns against
(§7: "Feature addition without data consistency check").

## Recommendation

**Defer to v3.2.** After v3.1 ships and we have a baseline score,
test is_preflop_aggressor as feature 53 in a controlled experiment:
train with and without, compare CV log-loss and feature importance.
If it adds >1% importance, keep it. If not, drop it.

The owner's instinct is correct — PFA status matters in poker. The
question is whether the model needs it as a raw feature when it
already has 3 derived features that capture the same information.
That's an empirical question best answered with a trained model,
not with theory.
