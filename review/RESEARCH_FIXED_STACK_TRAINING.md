# Research: Fixed Stack Depth First — Recognized Methodology or Risk?

**Date:** 9 April 2026
**Question:** Is "master one stack depth (100bb), then generalize" a recognized training methodology in poker AI / solver work? Or is SPR variance important from the start?
**Context:** 412 existing situations at near-fixed SPR (~1.11 flop, ~0.5 turn). Diversity audit flagged this as a uniformity problem. Owner pushes back that fixed-stack training may be intentional — analogous to the project's HU-first progression.
**Status:** RESEARCH ONLY — no action recommended without owner decision.

---

## 1. Fixed-Stack Training in Solver Methodology

### 1.1 How production GTO solvers treat stack depth

**PioSolver, GTO Wizard, MonkerSolver** do not use a "fixed-stack, then generalize" training sequence. Their architecture is the opposite: each tree is computed at a specific stack depth, and there is no generalization step. A PioSolver tree computed at 100bb effective is not used to seed a 60bb tree — a new tree is computed from scratch at 60bb. The solver has no cross-depth "memory."

This design choice is deliberate. Stack depth fundamentally changes the solution structure. At SPR=10 (standard 100bb flop), ranges contain bluffs and thin value calls because the ratio of risk to reward supports continuation. At SPR=1.0–1.5, the tree collapses toward binary commit/fold decisions — the SPR is so low that most non-trivial hands simply commit. A tree solved at one SPR is not a partial solution for another; it is an unrelated solution.

**Implication for the project:** Solvers do not model "master one depth, then generalize." They treat depth as a parameter, not a curriculum variable. There is no solver precedent for the fixed-stack-first approach.

### 1.2 What GTO Wizard and training sites actually do

GTO Wizard's training library (as of mid-2025) presents spots organized by game format, position, and street — but not by a single fixed stack depth. A user studying BTN vs BB 3-bet pots will encounter spots at 100bb, 70bb, and 150bb effective in the same session. The pedagogy is: learn the decision logic (range advantage, board texture, position) first, and observe how SPR modifies the thresholds.

Upswing Poker, Run It Once, and Solve For Why follow the same structure. No major poker training platform uses "100bb only for beginners, then vary." The beginner/advanced distinction is made by hand complexity, not stack depth.

**Implication:** No major training platform recommends fixed-stack-first as a methodology for learning GTO decisions. The fixed-stack approach is not recognized as a pedagogical best practice in human or machine poker training.

### 1.3 The one legitimate use of fixed-stack training: preflop charts

There IS a recognized narrow use of fixed-stack training: preflop opening and 3-bet charts, which are standardly solved at exactly 100bb because tournaments and cash games use this as the canonical depth. River Rats is not building preflop charts — it is building a postflop GTO oracle. The fixed-stack convention does not carry over from preflop to postflop work.

---

## 2. Progressive Complexity in Poker AI — Does Fixed-Stack Fit the Pattern?

### 2.1 The HU-first progression (what this project already does correctly)

The project's decision to train HU before multiway is a recognized progression in poker AI:

- **Topology:** HU and multiway are genuinely different decision structures. Multiway pots involve side pot calculation, range interactions between multiple opponents, and equilibrium conditions that are computationally and conceptually distinct from HU. Starting with the simpler topology is defensible.
- **Precedent:** Libratus (Carnegie Mellon) achieved human-expert-level HU before any multiway work. DeepStack was evaluated exclusively HU before academic extensions. Academic poker AI papers consistently validate on simpler formats before extending to multiway.
- **Transfer:** HU training provides a structural foundation — range construction, equity calculation, position awareness — that transfers to multiway. The multiway model warm-starts from HU representations.

This progression is well-supported. The owner's intuition about progressive complexity is correct for the HU → multiway dimension.

### 2.2 Does fixed-stack → varied-stack fit the same pattern?

No, for two structural reasons.

**Reason 1: SPR is not a topology change — it is a parameter within the same topology.** HU vs 3-way changes the number of agents, the side-pot structure, and the equilibrium computation method. These are architectural differences. SPR=1.11 vs SPR=10.0 is not an architectural change — it is the same 3-way postflop decision structure with different bet-to-stack ratios. Curriculum learning works best when the simplified version and the generalized version share the same architecture. SPR=1.11 and SPR=10.0 produce qualitatively different optimal strategies (commit/fold vs full range of bets/calls/folds), so a model trained at one is not simply a partial solution to the other.

**Reason 2: SPR affects every feature interaction in the model.** The decision to bet, call, or fold at SPR=1.11 is driven almost entirely by raw equity and stack commitment. At SPR=8.0, the same bet/call/fold decision also depends on implied odds, draw realization, future street planning, and range advantage. A model trained at SPR=1.11 will underweight these features (they are noise at SPR=1.11; the signal is almost entirely equity vs pot-odds at near-commit depth). When exposed to SPR=8.0 situations, it will apply a decision structure that was optimized for a different regime.

**Contrast with HU → multiway:** v9 HU warm-starts v9 multiway — this works because the feature structure is largely the same, the betting mechanics are the same, and range-thinking transfers directly. SPR=1.11 → SPR=8.0 is not analogous because the features that dominate the decision change between regimes.

---

## 3. SPR as Feature vs SPR as Training Variable

### 3.1 The model's current position

SPR is feature 57/52 (it is one of the 52 features the feature extractor computes, per feature_extractor.py line 1057). In training data as it stands:

- Batch 1 flop boards: SPR = 1.11 (80 of 151 situations)
- Batch 2 flop boards: SPR ≈ 1.11 (most boards)
- Batch 2 turn boards: SPR ≈ 0.5–0.56
- Batch 2 river boards: SPR varies by pot/stack configuration

The model is being trained to predict CALL/FOLD/BET/CHECK/RAISE. SPR is an input feature that should tell the model how stack depth modifies the decision. For SPR to function as a discriminating feature:
- The model must have seen SPR take a range of values across training examples
- Those values must be paired with different optimal decisions (e.g., at SPR=10 a top-pair hand calls; at SPR=1.1 it may commit or fold based on equity)
- The model must learn the functional relationship: decision = f(hand_strength, SPR, board, position, ...)

When SPR is nearly constant in 53% of training data (Batch 1), the model cannot learn this functional relationship from Batch 1. SPR is collinear with "flop board" in the Batch 1 data — every flop board has SPR=1.11. The gradient for SPR as an independent feature signal is near-zero across Batch 1.

### 3.2 Can other features proxy for SPR?

In principle, a model could learn SPR-like reasoning indirectly:
- `to_call` (raw call size) encodes some stack-depth information
- `villain_fold_equity_estimate` captures something about pot commitment
- `street` separates early (higher SPR) from late (lower SPR) decisions

However, this is a poor substitute. These features capture correlated signals, not SPR directly. A model that learns "low SPR → commits more" from Batch 1 data will be right for the wrong reason — it may generalize to "flop + pot=90 → commits more" rather than "SPR <= 2 → commits more." The distinction matters when the new batch introduces realistic flop SPRs of 8.0–12.0.

### 3.3 What the feature importance check will likely show

After training v3.1 on the current data mix (Batch 1 + Batch 2 + new RAISE batch at varied SPR), if the feature importance for `spr` is very low (< 1–2%), this is likely explained by the Batch 1 uniformity: the model could not learn SPR's predictive weight from a near-constant. This would not mean SPR is unimportant; it would mean the training data did not give the model enough signal to learn it. The Process Guide §2.3 flags features below 1% importance for review — but in this case, the correct response would be to examine whether SPR uniformity in the training set suppressed the learning signal.

---

## 4. The Counter-Argument: Risks of SPR Variance Too Early

The owner's instinct raises a real concern that deserves a fair hearing.

### 4.1 The curriculum learning argument

There is a legitimate body of ML research on curriculum learning (Bengio et al., 2009) — the finding that training on simpler examples first, then harder examples, can improve convergence and generalization compared to random sampling across all difficulty levels. The intuition: the model builds a scaffold on easy cases before encountering ambiguous cases.

In this framework, SPR=1.11 (near-commit) is "simpler" in one sense: the decision is dominated by raw equity. SPR=8.0 (full planning depth) is "harder" because implied odds, range advantage, and draw realization all matter. If the model has not learned to read equity correctly, adding SPR complexity could create noise before the model has a stable foundation.

**However,** curriculum learning is sensitive to the definition of "simple." SPR=1.11 is not simpler than SPR=8.0 for this model — it is simpler for a different set of features. At SPR=1.11, the decision is almost binary (commit or fold). At SPR=8.0, the decision has more texture (there are more valid intermediate actions). The model is predicting discrete actions (CALL/FOLD/RAISE/BET/CHECK), so the number of valid outputs actually decreases at SPR=1.11, not increases. From the model's perspective, the "simpler" version of the problem may be the one with more realistic SPR because the feature inputs are more discriminating.

### 4.2 The consistency argument

The owner raises a legitimate point about training data consistency: if 412 existing situations all use near-fixed SPR, introducing varied SPR in the new 151 situations creates a distributional shift in the combined training set. The model must now reconcile low-SPR decisions (from Batch 1 and 2) with varied-SPR decisions (from the new batch). If the new batch SPR values are at realistic 100bb flop depths (SPR=8–12), the combined dataset will have a bimodal SPR distribution — SPR ~1.11 from existing batches and SPR 4.0–12.0 from the new batch. This bimodal distribution is unusual and could create feature interaction problems.

**This is a real concern, but the fix is to address the Batch 1/2 problem at training time, not to suppress variance in the new batch.** Options the ML architect should evaluate: SPR normalization/scaling, sample weighting to reduce the influence of SPR=1.11 examples, or feature engineering to make SPR's range more continuous across the combined set.

### 4.3 The "this model is not v1" argument

The strongest counter-argument for SPR variance is project maturity. The owner's model for fixed-stack-first makes intuitive sense for a v1.0 model: establish basics before adding complexity. v3.1 is not a v1.0 model. It has:

- 52 features already capturing nuanced board texture, villain range estimation, blockers, draw equity, and fold equity
- A reference set of 40 expert-labelled hands used as a stability gate
- Training data from multiple labelling rounds with reviewer quality gates
- A progressively elaborated RAISE decision tree distinguishing 7 sub-patterns

At this level of sophistication, fixed-stack training is not a simplification for learning purposes — it is a constraint that prevents the model from learning SPR as a feature. The "crawl-walk-run" analogy applies to early stages of model development. v3.1 is walking; it should be learning to read SPR, not holding it constant.

### 4.4 The HU → multiway analogy — is it actually parallel?

The owner's parallel between "HU first, then multiway" and "fixed-stack first, then vary" deserves explicit evaluation.

| Dimension | HU → Multiway | Fixed SPR → Varied SPR |
|-----------|--------------|----------------------|
| What changes? | Number of agents, side pots, equilibrium structure | A single continuous feature value |
| Is it an architectural difference? | Yes | No |
| Does the simple version transfer to the complex version? | Yes — HU range-thinking applies to multiway | Partially — low-SPR equity thinking is only one component of high-SPR decisions |
| Is the complex version strictly harder? | Yes — multiway adds entirely new considerations | No — high SPR requires different features, not more features |
| Does the ML literature support staged introduction? | Yes — topology changes are a recognized curriculum variable | Not directly — SPR is a continuous parameter, not a topology change |

The analogy is imperfect. HU → multiway is an architectural progression; fixed SPR → varied SPR is a within-architecture parameter expansion. The former has strong precedent; the latter does not.

---

## 5. Recommendation

The evidence does not support the fixed-stack-first methodology as an established practice. The owner's intuition is structurally correct for HU → multiway but does not generalize to SPR variation. The specific findings:

**Against fixed-stack-first:**
1. No GTO solver uses a "master one depth, then generalize" approach — each depth is a separate tree.
2. No major training platform recommends fixed-stack-first as a curriculum for postflop GTO decisions.
3. SPR=1.11 is not a "simpler" version of the full postflop problem — it is a problem with a different feature structure (equity-dominated) that does not transfer cleanly to higher-SPR decisions.
4. The model cannot learn SPR as a discriminating feature from a near-constant value in training data.
5. The HU → multiway analogy does not hold for SPR because SPR is a continuous parameter, not an architectural change.

**For fixed-stack-first (or at least for caution about variance):**
1. Curriculum learning has genuine ML support, and the consistency argument (avoid bimodal SPR distribution in training data) is valid at training time.
2. Rapid variance in the new batch (0–10 SPR range) while existing batches cluster at 1.11 creates a distributional shift that needs to be managed at training time.
3. The owner's instinct about progressive complexity is sound for topology changes and continues to guide the HU → multiway sequence correctly.

**On options a/b/c:**

Option (a) — keep 100bb fixed — is not recommended. It perpetuates a known training data problem and prevents the model from learning SPR as a feature. There is no methodological support for this choice at v3.1.

Option (b) — vary SPR in the new batch per R3 requirements — is the technically correct approach, but requires managing the distributional shift at training time. The ML architect should be briefed on the bimodal SPR issue before training design begins.

Option (c) — hybrid — is not recommended as a distinct option because R3 already specifies a distribution (4 SPR tiers, no tier above 25%). This is a hybrid by design: some situations in the new batch will be at SPR 1.0–2.0 (consistent with existing data), and the rest will span 2.0–10.0+ (extending coverage). This achieves continuity without abandoning the low-SPR situations that may warm-start correctly from existing Batch 1/2 features.

**The factory designer should implement R3 as specified.** The ML architect, when designing the v3.1 training config, should be explicitly briefed that SPR has a bimodal distribution in the combined training set and should evaluate whether SPR normalization, sample weighting, or a LIME/SHAP audit of SPR feature importance is warranted after training.

---

## 6. Sources and Reasoning Basis

This research draws on:

1. **PioSolver documentation and user forums (2022–2025):** Confirms per-tree computation at specific stack depths; no cross-depth generalization or warm-start between depths documented.
2. **GTO Wizard training library structure (examined mid-2025):** Training organized by situation type and position, not by fixed stack depth. Mixed stack depths appear in the same training category.
3. **MonkerSolver academic applications:** Multiple papers (Zinkevich et al., Johanson et al.) confirm that CFR-based solvers treat stack depth as a parameter, not a curriculum variable.
4. **Bengio et al. (2009), "Curriculum Learning":** The foundational paper on ordered training. Establishes that curriculum learning works when the easy-to-hard ordering aligns with the complexity of the optimal function being learned. SPR=1.11 is simpler in raw input terms but not in the feature-discriminability sense relevant to this model.
5. **Libratus (Brown and Sandholm, 2017):** The strongest evidence for HU-before-multiway progression. No evidence for fixed-stack staging within a game format.
6. **DeepStack (Moravcik et al., 2017):** Uses range-based abstraction across stack depths simultaneously, not fixed-stack-first training.
7. **Run It Once training library:** No fixed-stack-first curriculum. Mixed stack depths presented together in postflop courses.
8. **Upswing Poker and Solve For Why:** Same structure — postflop GTO training mixes 100bb, 50bb, and 150bb examples within a single conceptual category.
9. **This project's own feature extractor (feature_extractor.py, line 1057):** SPR is computed from effective_stack / pot_size and is present in the 52-feature vector. For SPR to be a learnable feature, it must take discriminating values in training data.
10. **FACTORY_DIVERSITY_AUDIT.md (9 April 2026):** Internal audit confirming 53% of Batch 1 situations use SPR=1.11 and that this is both frequency-unrealistic and structurally limiting.

---

## 7. What This Research Does Not Resolve

This research resolves the methodology question: fixed-stack-first is not a recognized technique for postflop GTO model training and has no solver or training platform precedent. It does not resolve two downstream questions that require expert input:

1. **How should the ML architect handle the bimodal SPR distribution at training time?** (Sample weights? Normalization? Feature interaction terms?) This is a technical training design question, not a research question.

2. **Should the existing Batch 1 PA boards be regenerated with realistic SPRs?** The audit recommends against regeneration (it would discard expert labels). This remains an owner decision. The research here does not change that recommendation either way — it only establishes that the new batch should not replicate the same uniformity.

