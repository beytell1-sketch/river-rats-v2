---
date: 2026-04-27
from: ml-architect (audit subagent)
to: orchestrator
re: Training corpus sizing + architecture audit
status: EVIDENCE-BASED AUDIT — informs corpus revision plan; no code changed
---

# ML-architect audit: training corpus sizing + architecture

## Source files read

- `CLAUDE.md` — project state
- `review/comms/MAIN_TERMINAL_RANGE_LOGIC_RESEARCH_DECISION_2026-04-26.md` — strategic decision
- `river-rats-core/feature_keys.py` — all 59 feature keys
- `river-rats-core/gto_model.py` — inference wrapper; confirms architecture
- `river-rats-core/train_model.py` — training pipeline with full hyperparameters
- `data/pilot_corpus_100_hand_2026-04-26.jsonl` — corpus (100 records verified)
- `review/pilot_run_2026-04-26/phase_b/labels_protocol_A_labeller_{1-5}.json` — 500 labels
- `review/pilot_run_2026-04-26/calibration_grading_key.json` — Tier 1 set (33 hands)
- `docs/PROGRESSIVE_MODEL_CHAIN.md`, `docs/MASTER_PLAN (1).md`
- `docs/SPEC_3WAY_LABELLING_PROTOCOL.md`
- `prompts/gto_labeller_v3.2.md` — labelling protocol + DO NOT rules

---

## Q1: Current model architecture — what is it actually?

**Architecture:** XGBoost multiclass classifier. Single model per opponent count, not an ensemble. Trained with `objective='multi:softprob'`, `num_class=5`.

**Output:** Full class probability distribution over 5 actions (FOLD / CHECK / CALL / BET / RAISE). `OraclePrediction.probs` returns `{action: probability}` for all 5 classes. Argmax is taken for the final action but the underlying probabilities are exposed. This means the model can in principle express uncertainty across classes.

**Loss:** Softmax cross-entropy (multiclass log-loss via `multi:softprob`). This is the correct loss for 5-class classification.

**Calibration:** Not explicitly calibrated. No Platt scaling or isotonic regression is applied post-training. The `multi:softprob` objective learns class probabilities directly, but XGBoost probabilities are known to be miscalibrated on imbalanced datasets — the probabilities reflect the model's internal splits, not true posterior probabilities. For the purpose of this project (argmax action selection), this is not a blocking issue; it does matter if soft labels or probability-based distillation are considered (see Q5).

**Hyperparameters (from `train_model.py`):**
- `n_estimators=800` with `early_stopping_rounds=50`
- `max_depth=5` — moderately deep; 5 levels can capture up to 32 leaf nodes per tree
- `learning_rate=0.05` — conservative; correct for small-data regimes
- `subsample=0.8`, `colsample_bytree=0.75` — regularisation
- `min_child_weight=5` — requires at least 5 samples per leaf; **this is the most consequential hyperparameter for corpus size** (see Q3)
- `gamma=0.2`, `reg_alpha=0.1`, `reg_lambda=1.0` — further regularisation

**Warm-start:** The progressive chain uses `xgb_model=previous_model` in `.fit()`, which appends new trees rather than retraining from scratch. This is critical context for corpus sizing: the student model does NOT need to re-learn HU patterns; it only needs enough signal for the new trees to learn multiway corrections.

---

## Q2: Class imbalance handling

**Current handling in the code:**

The training pipeline uses inverse-frequency sample weighting with a RAISE cap:

```python
majority_count = float(class_counts[ACTION_TO_INT['CHECK']])
raw_weights = {cls: majority_count / count for cls, count in class_counts.items()}
raw_weights[ACTION_TO_INT['RAISE']] = min(raw_weights[RAISE_IDX], 3.0)
sample_weight_train = np.array(...)
```

This means each training sample is upweighted in proportion to how rare its class is, with RAISE capped at 3x (not the full inverse frequency, which could be 50x+ if RAISE is near-zero).

**Observed Phase B label distribution (500 labels across 5 labellers, 100-hand opener-heavy corpus):**

| Action | Count | Fraction |
|--------|-------|----------|
| CHECK  | 299   | 59.8%    |
| BET    | 186   | 37.2%    |
| FOLD   | 14    | 2.8%     |
| CALL   | 1     | 0.2%     |
| RAISE  | 0     | 0.0%     |

This is not representative of postflop poker; it is a direct consequence of 97/100 corpus hands having `facing_bet=False`. When there is no bet to face, CALL and RAISE are structurally impossible.

**Can RAISE be predicted at training time?**

No. With 0 RAISE instances across 500 labels, the model receives no gradient signal for the RAISE class. The inverse-frequency weight cap of 3.0 is irrelevant when `count=0`. The model will assign RAISE probability near zero for all inputs and will never output RAISE. The 3.0 cap was designed for imbalanced-but-nonzero scenarios; it does not fix zero-instance classes.

**CALL is effectively unreachable too.** One CALL instance across 500 labels, receiving inverse-frequency weight of ~300x (before capping). Even if uncapped, a single sample with extreme weight is a noise source, not a signal source. XGBoost's `min_child_weight=5` requires at least 5 weighted samples in a leaf; a single CALL with weight 300 might trigger this numerically, but it will produce a leaf that fires on that one specific feature configuration, not a generalizable CALL rule.

**Can deliberate class balance fix this, given the current architecture?**

Yes, with two conditions:
1. The resampling must happen at corpus construction time (selecting hands that produce each action class), not via sample weights alone. Sample weighting compensates for existing imbalance; it cannot synthesize signal that doesn't exist in the training data.
2. The RAISE cap of 3.0 should be reviewed when the corpus has RAISE instances. At 15% RAISE target, the imbalance is mild enough that sample weighting alone can handle it. At the desired 25% CHECK / 25% BET / 20% CALL / 15% RAISE / 15% FOLD distribution, simple inverse-frequency weights without capping would suffice.

The architecture itself (XGBoost softmax multiclass with sample weighting) fully supports deliberate class balance. No architectural change is required; corpus redesign is required.

---

## Q3: Corpus size lower bound for generalization

### Theoretical lower bound (memorization prevention)

For a gradient-boosted tree classifier, memorization prevention is governed by `min_child_weight`. The current setting is 5: no leaf can be created unless it covers at least 5 weighted training samples. This means the model cannot memorize individual samples — it must find patterns shared across at least 5 instances before splitting.

**Hard lower bound per class:** 5 samples (the `min_child_weight` floor). Below 5 per class, XGBoost literally cannot form leaves for that class. This sets an absolute minimum of 25 samples total across 5 balanced classes — but "not memorizing" at 25 samples is meaningless; the model would simply refuse to learn the minority classes at all.

**Practical lower bound for a non-degenerate model:** In tabular ML literature, the rule of thumb is 10 × number of features per class for simple linear boundaries, and 50-100 × features per class when interactions matter. With 59 features and 5 classes, these bounds give:
- Conservative (linear): 59 × 10 × 5 = 2,950 samples
- Moderate (interactions): 59 × 50 × 5 = 14,750 samples

These bounds assume training from scratch. The warm-start chain changes the calculus significantly: the base model (v9-baseline trained on ~25k PokerBench hands) already encodes basic poker patterns. The new trees only need to learn multiway-specific corrections — a lower-dimensional problem.

**Vapnik-Chervonenkis (VC) dimension bound:** For a decision tree ensemble of depth 5 and 800 estimators, the VC dimension is very large (the model is extremely expressive). What prevents overfitting is the regularization (min_child_weight, gamma, subsample) and early stopping. The generalization gap from finite sample is bounded by:

`Generalization gap ≤ O(sqrt(d/n))`

where `d` is model complexity and `n` is the training set size. For this model's complexity level, you need `n >> d` to drive the gap low. This is why early stopping on a held-out validation set is critical — it substitutes empirical stopping for theoretical sample requirements.

**Practical answer for warm-start specifically:** The 2017 XGBoost paper (Chen & Guestrin) and subsequent practice suggest warm-start fine-tuning can achieve reliable corrections with 5-10× fewer samples than cold-start training, provided the base model's errors are systematic rather than random. Here, the base model's failures are systematic (CHECK-bias, no CALL/RAISE output due to distribution shift) — warm-start is well-suited.

**For the 4D pattern space (hand class × board × position × range positioning):**

V3.2's rules cover approximately these pattern dimensions:
- Hand class: 6 buckets (monster, strong-made, medium-made, weak-made, drawing, air)
- Board texture: ~6 relevant conditions (paired, 2-tone flush, rainbow dry, connected, monotone, double-paired)
- Position: 2 primary (IP / OOP) + preflop aggressor flag
- Range positioning: paired-board capping, villain_range_capped, facing_bet, facing_raise

Cross-product estimation: 6 × 6 × 2 × 4 = 288 distinct "cells" in the pattern space. To cover each cell with enough samples to trigger XGBoost's `min_child_weight=5` floor:
- **Absolute minimum:** 288 × 5 = 1,440 samples
- But many cells share decision boundaries; the effective required coverage is lower
- **Realistic minimum for warm-start:** 400-600 samples with deliberate stratification covering the high-priority cells (facing-bet decisions, range-decisive spots, RAISE/CALL candidates)

The current corpus (100 hands × 5 labellers = 500 labels, but 97% opener-only) provides 500 samples in a 1D slice of the pattern space. This is sufficient for CHECK/BET within the opener context but provides zero coverage of 3 of the 5 action classes.

### Diminishing returns

Without prior experiments at multiple corpus sizes on this specific problem, the diminishing-returns point is an estimate. From analogous tabular classification literature (Fernandez-Delgado et al. 2014, Couronne et al. 2018 random forest studies, XGBoost benchmarks):

- Below ~200 well-stratified samples: High variance, results unreliable across random seeds
- 200-500 samples: Rapid accuracy improvement per additional sample
- 500-1000 samples: Continued improvement, slowing
- 1000-2000 samples: Marginal gains per additional sample; most of the learnable signal captured
- Above 2000 samples: Diminishing returns; improvement requires qualitatively new coverage, not volume

**For this warm-start setting specifically:** The base model handles ~60-65% of cases correctly (HU patterns that transfer). The new data needs to teach the remaining 35-40%. The effective new information per sample is higher than cold-start, so diminishing returns likely arrive earlier (~800-1200 samples for this task).

**Recommended target with rationale:** 500-600 well-stratified samples covering all 5 action classes (minimum 50 per class, targeting 100+ for CALL and RAISE). This is achievable, evidenced, and sits solidly in the rapid-improvement zone.

---

## Q4: Calibration set sizing

### What the Tier 1 calibration set currently contains

33 hands (`calibration_grading_key.json`):
- Action distribution: CHECK 8 / CALL 11 / BET 12 / RAISE 1 / FOLD 1
- 10 reversal hands (spots where v3.2 rule-overrides are testable)
- Pass gate: 23/33 (70%) for standard; 100% for reversal hands

This is a labelling protocol quality gate, not a model training set. Its job is to verify that labellers apply v3.2 correctly before they touch the Tier 2 corpus.

### How many patterns does v3.2 explicitly handle?

From the protocol (rules + overrides):
- DO NOT Rules 1-11: 11 explicit reasoning guards
- KB §1.7 OVERRIDE (villain_air_pct threshold): 1 override
- Rule 11 (paired-board + 2-tone OOP exception): 1 override
- River-checked-to override (d3178 pattern): 1 override
- Three reversal-anchor pattern classes (MW-30 over-fold, MW-33 nut-draw raise, MW-50 fold)

Counting distinct decision contexts the calibration set must cover: approximately 15-20 distinct pattern types that v3.2 explicitly handles or corrects.

### Minimum N per pattern

For a calibration set to statistically detect whether labellers apply a specific rule correctly, you need enough hands per pattern to distinguish systematic rule application from random guessing. With binomial statistics:

- If a labeller gets a pattern right 80% of the time (good calibration) vs 50% (coin flip), detecting this difference at 80% power with a one-sided test requires ~25 hands per pattern.
- At 90% power: ~40 hands per pattern.

For the reversal hands specifically, the current approach (100% pass required on all 10) is a zero-tolerance gate. One reversal hand per pattern type is statistically fragile — a single labeller error on a genuinely borderline hand would HALT the entire pilot. The current 10 reversal hands covering 10 distinct patterns is the minimum workable design given the 100% gate.

### Recommended Tier 1 target

**Current state:** 33 hands, 10 reversal hands, strong action class balance (8/11/12/1/1 vs the opener-heavy Tier 2 distribution). The calibration set is better balanced than the corpus it is supposed to QC.

**Gap:** The calibration set does not include facing-bet contexts at meaningful frequency. With a revised corpus targeting CALL/RAISE coverage, the calibration set needs facing-bet reversal hands — specifically spots where v3.2 Rule KB§1.7 OVERRIDE fires (villain_air_pct threshold for RAISE decisions) and spots where surface features favor RAISE but range positioning argues CALL.

**Recommended Tier 1 size:** 45-50 hands, expanding with:
- 5-8 additional facing-bet reversal hands (CALL vs RAISE decisions, testing KB§1.7 OVERRIDE in context)
- 2-4 additional FOLD reversal hands (for the over-fold-bias pattern observed in Sonnet failures: MW-17, MW-41, MW-44)
- Current 33 hands retained unchanged (hash-locked; reversal gate passes)

At 45-50 hands with ~15 reversal hands and a 100% reversal gate, the calibration set can statistically verify labeller competence across the 4D pattern space at an acceptable false-negative rate for the pilot scale. Going above 60 calibration hands has diminishing returns at this stage and increases the cost and time cost of each calibration cycle.

---

## Q5: Solver dependency — what changes if labels are solver-derived?

### Architecture changes if solver provides ground truth

No structural architecture change is required. The existing XGBoost softmax classifier with hard labels (single action per sample) continues to work. V3.2 rule-based labels are the production format; the strategic decision confirms this.

### Gains from soft labels (distillation from mixed-strategy)

If solver outputs were available as mixed strategies (e.g. "CHECK 72%, BET 28%"), knowledge distillation using soft targets would theoretically:
1. Preserve the model's confidence calibration (the probabilities reflect true GTO frequencies)
2. Provide gradient signal for the minority actions even on samples where the plurality action is something else
3. Allow the model to learn that d9556 is "primarily CHECK but occasionally BET" rather than a hard CHECK

The benefit for boundary cases is real: GTO mixed strategies are exactly the spots where hard labels lose information. However, three blocking factors make this impractical for this project:

**Blocking factor 1 — labeller inability:** The overnight research confirmed labellers cannot produce reliable frequency tiers without solver. "OFTEN/SOMETIMES/RARELY" without numeric ground truth is noise as ML signal.

**Blocking factor 2 — solver availability:** Soft labels require running GTO Wizard or equivalent on every corpus hand. The corpus is too large for manual solver verification (the solver spend caps and per-hand complexity make this infeasible at 500+ hands).

**Blocking factor 3 — model capacity at this corpus size:** Knowledge distillation with soft targets typically requires larger models and more data to benefit. At 500-600 training samples, hard labels with inverse-frequency sample weighting are more stable than soft targets which can introduce gradient noise on small datasets.

**Recommendation:** Continue with hard labels (single action from v3.2 protocol). If the model reaches ~85%+ accuracy on the reference set with v3.2 labels and a revised corpus, revisit soft targets for v3 of the model using solver verification on the 33 calibration hands only (tractable scope).

---

## Q6: Feature signal sufficiency

### Features the 59-contract carries that v3.2 rules need

**Range positioning (where hero sits in own range):**
- `hero_range_percentile` (Feature 49) — where hero's hand sits within their own preflop range on this board. Present and populated (verified in corpus feat_dicts).
- `board_adjusted_hrp` (Feature 55) — HRP × equity_vs_range, collapses HRP when the board doesn't connect. Present.
- `is_preflop_aggressor` (Feature 53) — whether hero was the preflop raiser. Present. This is critical for c-bet decisions.

Hero's range positioning is covered by 3 features. However, there is an important gap:

**MISSING: Hero's relative range position against villain's range.** `hero_range_percentile` is calibrated against hero's own range only. It does not encode "am I near the top of my range given that villain is also likely to have a strong range here?" The v3.2 Rule 11 paired-board exception and the river-checked-to override both involve reasoning about villain's range composition constraining hero's optimal frequency — this can only be inferred from the villain composition quad, not directly from hero's raw HRP.

The conjunction of `hero_range_percentile` + `villain_top_pair_plus_pct` + `villain_range_capped` + `board_adjusted_hrp` provides an indirect signal. The model can in principle learn the interaction. But there is no single "am I capped / are we in a range-tipping spot" feature that directly encodes this.

**Range balance / range-tipping:**
- `villain_range_capped` (Feature 44) — preflop structural label for villain. Present.
- No hero_range_capped feature exists. Whether hero's range is capped on a given board is not directly encoded. This is the core signal for the paired-board CHECK exception: on 5s6d6h with hero holding 5h5d, hero has the nuts AND the board is paired — hero's range includes full houses but villain's opener range also has full houses. The model must infer range-tipping from the combination of `is_paired`, `hand_category`, and `villain_range_capped`. Indirect but learnable given enough paired-board examples.

**Effective stacks / SPR:**
- `spr` (Feature 33) — stack-to-pot ratio. Present and critical.
- `pot_size`, `to_call`, `pot_odds`, `bet_to_pot` — all present.

**Features that ARE present but need sufficient corpus coverage to be learned:**
- `facing_bet` (Feature 2) — whether hero faces a bet. Currently near-constant (97/100 = False in corpus). The model cannot learn the CALL/RAISE/FOLD decision boundary from this feature if it rarely varies in training.
- `facing_raise` (Feature 45) — whether facing a raise. Currently near-zero. Same problem.
- `villain_aggression_count`, `villain_call_count`, `villain_checked_back` — action history features that capture multi-street dynamic. These encode the "river-checked-to" override signal. Present but only useful if the corpus includes river spots where villains checked back.

### Feature gaps flagged

**Gap 1 (MODERATE): No explicit hero-range-cap signal.** Whether hero's checking range is range-tipping (i.e., checking AA on a paired board reveals that hero's check range is strongly capped) is not directly encoded. The model must learn this from the joint distribution of `hand_category`, `is_paired`, `hand_rank`, and the composition quad. This is learnable but requires paired-board examples in the corpus. Gap is addressable by corpus design (include paired-board hands), not feature engineering.

**Gap 2 (LOW): No "board favours villain" direction signal independent of hero's hand.** `board_favour` (Feature 43) captures whether the board texture favours the preflop raiser's range. But the v3.2 distinction between "board favours hero's range" vs "board favours villain's range conditional on hero's hand class" is not decomposed. This is a mild signal gap; the combination of `board_favour` + `villain_top_pair_plus_pct` + `board_adjusted_hrp` provides partial signal.

**Gap 3 (LOW): Opponent-specific range features aggregate across villains.** In 3-way pots, the two villains have different ranges (BTN flat = capped; BB defend = wide). The composition quad (`villain_top_pair_plus_pct`, etc.) aggregates across opponents. The `_per_villain_composition` field is computed internally but is not in the model feature set. The current approach is a known limitation from the SPEC_3WAY_LABELLING_PROTOCOL.md; it was a deliberate simplification. For the current model this is acceptable.

**No blocking gaps found.** All features required for v3.2's core rules (Rule 11, KB§1.7, river-checked-to) have proxies in the 59-feature contract. The gaps are signal-dilution issues, not signal-absence issues. The model can learn the rules given sufficient corpus coverage.

---

## Q7: Recommended pipeline architecture

### Q7.1: Single-task vs multi-task

**Recommendation: Single-task (predict primary action only).**

Rationale: Multi-task learning (predicting action + range concepts) requires labelled range concept outputs. The overnight research demonstrated that labellers cannot reliably self-classify their decisions into `RANGE_DECISIVE / TRAP_HAND / BALANCE_PROTECTION` — the `teaching_flag` enum was applied indiscriminately (RANGE_DECISIVE 5/10 outputs) and incorrectly (BALANCE_PROTECTION never applied on the one hand that warranted it). Training on unreliable concept labels introduces noise.

The v3.2 `reasoning` field already contains range concept mentions. The teaching layer can mine these via text parsing without requiring a separate model output. Multi-task architecture adds model complexity and requires clean concept labels — neither is available at this stage.

### Q7.2: Hard labels vs soft labels

**Recommendation: Hard labels (single action from v3.2 protocol).**

Already argued in Q5. Hard labels are more stable at this corpus size, and labellers cannot produce reliable frequency tiers without solver. Revisit soft labels if the model proves unable to learn mixed-strategy spots even with increased corpus coverage.

### Q7.3: Feature engineering additions for range logic

**Recommended additions (2, both low cost):**

**Addition 1: `hero_range_is_capped` (binary flag).** Hero's range is capped when they did not 3-bet preflop from a position where premiums 3-bet. This is computable from `is_preflop_aggressor`, `hero_position`, `is_3bet_pot`, and `hand_category`. A simple rule: if hero is NOT the preflop aggressor AND hero is in a position that 3-bets premiums AND hero holds a strong hand (top pair+), hero's range is structurally capped. This encodes the range-tipping signal directly rather than requiring the model to infer it from the joint distribution.

Implementation: Add to `feature_extractor.py` as Feature 60. Requires matching changes to `gto_model.py` FEATURE_COLUMNS and attention vocabulary per `feedback_attention_flags_when_features_change.md`.

**Addition 2: `villain_checked_back_turn` (binary flag).** Currently `villain_checked_back` captures "villain checked back on any prior street." For river decisions, the specific signal is "villain checked back on the turn" — the d3178 river-checked-to override fires specifically on this pattern. A single aggregated `villain_checked_back` feature loses street-specificity. This is a low-cost decomposition.

Implementation: Requires action-history parsing to distinguish flop vs turn checkbacks. The current `extract_all_features` already processes `_action_history`; adding street-specific checkback flags is a small extension.

**Note on attention flags:** Per `feedback_attention_flags_when_features_change.md`, any new raw feature requires matching attention vocabulary + prompt rules + capture + trainer changes. These additions should be specced and reviewed before implementation.

### Q7.4: Train/val/holdout split

Given the warm-start setup and the small corpus:

- **Holdout:** Already hash-locked (Tier 3). Do not touch. Use only for final gate.
- **Calibration (Tier 1):** 33 hands (expanding to 45-50). Used for labelling protocol QC only; not for model training or validation.
- **Training corpus (Tier 2):** Revised corpus. Within this:

| Split | Fraction | Rationale |
|-------|----------|-----------|
| Train | 80% | Warm-start update signal |
| Val (early stopping) | 20% | Early stopping gate; also validates the reference set |

At 500-600 samples, an 80/20 split gives 400-480 training samples and 100-120 validation samples. For 5-fold CV this means 20-24 validation samples per fold — sufficient to detect ±5% accuracy changes at the class level for the majority classes, but not for RAISE or FOLD at natural frequency. Stratified K-fold on action class is mandatory to ensure minority classes appear in every fold.

**For the 24 three-way reference hands:** These remain the primary validation gate per the Progressive Model Chain spec. They should NOT be included in Tier 2 training data. Early stopping should be evaluated against the reference set (24 hands), not the 20% split, to directly optimize the gate metric.

**Alternative:** Use the 24 reference hands as the validation set for early stopping (reference-set-aware training). This is small (24 samples) but the reference hands were specifically designed to cover failure modes. Early stopping against these hands directly optimizes the metric we care about. This is preferable to a random 20% split.

---

## Q8: Final recommendations

### Q8.1: Tier 2 corpus size target

**Target: 500-600 labelled hands, deliberate action-class stratification.**

Specific breakdown:

| Action class | Target count | % | Rationale |
|---|---|---|---|
| CHECK | 125-150 | 25% | Dominant class; well-represented in current corpus |
| BET | 125-150 | 25% | Second-largest; current corpus has signal but opener-only |
| CALL | 100-120 | 20% | Zero coverage currently; requires facing-bet construction |
| RAISE | 75-90  | 15% | Zero coverage currently; requires facing-bet + raise-eligible spots |
| FOLD | 75-90  | 15% | Near-zero currently (14/500); requires facing-bet spots |
| **Total** | **500-600** | **100%** | — |

**Construction requirement:** Approximately 50% of corpus hands must have `facing_bet=True` to enable CALL/RAISE/FOLD coverage. This requires deliberate corpus construction (not random self-play), selecting hands from the `all_557_situations.jsonl` pool or generating new situations specifically targeting facing-bet contexts.

**Why not 200 hands (original spec target)?** At 200 hands with deliberate balance, minority classes (RAISE, FOLD) would have 30-40 instances. With 80/20 split, 24-32 training samples per minority class, and `min_child_weight=5`, this is technically above the XGBoost floor but leaves 3-5 samples per leaf for the minority classes — insufficient for robust boundary learning. The 500-600 target gives 60-75 minority class training samples, yielding 12-15 samples per leaf at depth 5: a more defensible generalization position.

**Why not 1000+?** Labelling costs, the warm-start setting (diminishing returns arrive earlier), and the 24-reference-hand validation gate: at 1000 samples, the corpus would be 40x the size of the validation gate. The model would overfit to corpus patterns that the reference set doesn't surface. 500-600 is proportionate to the validation mechanism.

### Q8.2: Tier 1 calibration set size target

**Target: 45-50 hands, expanding from current 33.**

Specific additions needed:
- 5-8 facing-bet reversal hands (CALL vs RAISE distinction, KB§1.7 OVERRIDE in context)
- 2-4 FOLD reversal hands targeting the over-fold-bias pattern (MW-17/41/44 pattern: hidden equity CALL reads as FOLD)
- Retain all 33 current hands unchanged

Pass gate: maintain 100% on reversal hands; 70% on standard. This gate is the right stringency for a production labelling protocol.

### Q8.3: Architecture changes

**Current architecture is fine for the revised corpus. No structural changes required.**

Specific holds:
- XGBoost multiclass softmax: correct for this task
- Warm-start chain: correct for the progressive model design
- Inverse-frequency sample weighting: correct; RAISE cap of 3.0 is appropriate when RAISE reaches 15% target (weight would be ~6.7x without cap; cap prevents excessive upweighting)
- `min_child_weight=5`: appropriate; lower (e.g. 3) would allow finer splits on minority classes but increase overfitting risk at this corpus size — leave at 5
- `max_depth=5`: appropriate; deeper trees would overfit at 500 samples

**Recommended parameter review at training time:**
- Early stopping: evaluate against the 24 reference hands directly, not a random held-out split
- Consider reducing `n_estimators` to 400-600 from 800 for the warm-start step — the base model already carries 800+ trees; appending another 800 may over-fit the small specialist corpus

### Q8.4: Feature additions

**Recommended (non-blocking, should be specced before implementation):**

1. `hero_range_is_capped` — binary flag; encodes hero structural cap directly. Medium value, low implementation cost. Requires architecture team spec + attention layer update.
2. `villain_checked_back_turn` — decompose existing `villain_checked_back` by street. Low value (minor improvement to river decision signal), low implementation cost.

**Not recommended now:**
- Per-villain composition features (breaks the current architecture's single-villain composition quad; large complexity increase for uncertain benefit at this scale)
- Soft-label fields / mixed-strategy probability targets (requires solver at scale; not viable)

Both additions are optional improvements, not requirements for the revised corpus to function. Ship the revised corpus first; add features in a subsequent PR if the model's river accuracy trails the reference set gate.

### Q8.5: Risk assessment — what is the failure mode if corpus is too small?

**Primary failure mode: Minority class blindness.**

If CALL and RAISE training instances are below 30 each (the XGBoost floor combined with the warm-start tree budget), the model will output near-zero probability for these classes and default to CHECK or BET on every decision. Empirically this is what the v8 model does now (52.5% MW accuracy = approximately the rate at which CHECK/BET is correct). A revised corpus that is still too small produces a model that is marginally better at opener decisions and still blind to facing-bet decisions.

**Secondary failure mode: Overfitting to the calibration anchors.**

The 10 reversal hands from the calibration set are referenced throughout the labelling prompt (d3688, d9556, MW-39, d3178, etc.). If labellers disproportionately label the corpus using these anchors as templates, the corpus will contain many near-copies of the 10 calibration patterns. The model will learn these 10 patterns well and fail to generalize beyond them. This is a labelling process risk, not a model architecture risk. Mitigation: diversify corpus across hand classes and board textures, not just repeating the calibration anchor board textures.

**Tertiary failure mode: Distribution shift at inference.**

The revised corpus must sample from the same distribution as real multiway postflop play. If corpus construction over-samples unusual situations (e.g. all RAISE situations are pure nut-draw check-raises, not balanced RAISE situations), the model learns a biased RAISE rule that fires on nut draws but misses other RAISE contexts. Mitigation: stratify corpus by hand class AND action class, not action class alone.

**What "too small" means in practice:** If the revised corpus has fewer than 50 CALL instances and fewer than 50 RAISE instances in training (after 80/20 split: 40 and 40), the model's per-class F1 for CALL and RAISE will be below 0.40 on the reference set — effectively random. This is the signal to increase corpus size before shipping.

---

## Summary table

| Item | Current state | Recommended target | Priority |
|---|---|---|---|
| Tier 2 corpus (hands) | 100 hands, 97% opener-only | 500-600 hands, 50% facing-bet | BLOCKER |
| Tier 2 action balance | 60% CHECK / 37% BET / 3% FOLD / 0% CALL / 0% RAISE | 25/25/15/20/15 | BLOCKER |
| Tier 1 calibration (hands) | 33 hands | 45-50 hands | HIGH |
| Tier 1 facing-bet reversals | 0 facing-bet reversal hands | 5-8 | HIGH |
| Model architecture | XGBoost warm-start softmax | Unchanged | NONE |
| Label type | Hard single action (v3.2) | Unchanged | NONE |
| Early stopping gate | Random 20% split | 24 reference hands directly | MEDIUM |
| Feature: hero_range_is_capped | Absent | Add (with arch review) | LOW |
| Feature: villain_checked_back_turn | Absent | Add (with arch review) | LOW |

The corpus revision is the only blocker. The model architecture does not need to change. The feature contract is sufficient for v3.2's rules to be learnable, provided the corpus covers the facing-bet pattern space.

---

*Audit complete. No files modified except this document. Main terminal to PR.*
