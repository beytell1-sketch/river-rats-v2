---
date: 2026-04-14
from: Owner (Rupert) + Main terminal
to: Future session
re: v2.3 research backlog — action distributions instead of class labels
status: BACKLOG — revisit after v2.2 ships
trigger: After v2.2 ships and Pass 1 labelling is complete
---

# v2.3 Backlog: Action Distributions (Gauge Labels)

## The idea (owner-originated)

Instead of labellers picking a single action (BET, CHECK, CALL,
FOLD, RAISE), they produce a distribution or "gauge" showing
the percentage lean across actions:

```json
{"action_distribution": {"BET": 0.72, "CHECK": 0.28, "CALL": 0, "FOLD": 0, "RAISE": 0}}
```

This matches how solvers actually work. GTO Wizard doesn't say
"BET" — it says "BET 72%, CHECK 28%" for mixed strategy spots.
Single-class labels throw away this information.

## Why this matters

- **Mixed strategies are real GTO.** Many spots have no single
  correct answer — the solver output is a frequency mix. Single-
  class labels force a binary choice where reality is probabilistic.
- **Close decisions handled naturally.** A 52/48 BET/CHECK spot
  should be labelled as a 52/48, not forced into difficulty-3 BET.
- **Richer training signal per hand.** A distribution contains
  more information than a class label.
- **Teaching matches poker reality.** "Mix your bet and check
  roughly 50/50 here" is a real coaching sentence. Current oracle
  can't produce it.
- **Lossless solver alignment.** When solver-verifying hands, we
  get exact frequencies. Storing the frequency is lossless.

## Technical approaches (three options)

### 1. Soft labels with cross-entropy loss
XGBoost's `multi:softprob` already outputs probabilities. Train
it on soft probability targets instead of hard class targets
using custom objective functions.

### 2. Separate regression per action
Train 5 separate XGBoost regressors — one for P(BET), one for
P(CHECK), etc. Each predicts action frequency from features. At
inference, normalize outputs to sum to 1.

### 3. Ordinal encoding for mixed strategies
Dedicated architecture predicting primary action + mixing ratio.
Less general, simpler.

## The calibration problem

LLMs are bad at calibrated probability estimates. Asking agents
to produce "72% BET, 28% CHECK" means they're making up numbers.

**Realistic path: coarse 3-level gauge.**

Add an optional field to the labelling output:

```json
{
  "action": "BET",
  "confidence": "HIGH",
  "action_lean": {
    "primary": "BET",
    "primary_strength": "strong"  // strong / moderate / marginal
  }
}
```

Where `primary_strength`:
- **strong** (≥90% BET) — pure strategy
- **moderate** (65-85% BET) — weighted toward BET
- **marginal** (50-65% BET) — close decision, mixed strategy

Much easier for LLMs to estimate than raw percentages. Gives a
3-level gauge without calibration problems. When later training
on distributions, map strong→0.95, moderate→0.75, marginal→0.55.
Calibrate to solver-verified hands.

## Architecture: Model chain

v2.2 has:
- Model 1: features → action (5-class)
- v2.3 Model 2 (planned): features → intentions (multi-label)

This backlog adds:
- v3.0 Model 3: features → action distribution

Eventually Model 1 gets deprecated — the distribution contains
more information, and Model 1's class is just argmax of Model 3.

## Teaching implications

L3 renderer can produce:
> "This is a close spot — mix your BET and CHECK roughly 60/40.
> The stronger line is BET for value against villain's 40% medium
> made hands, but CHECK trap is nearly as good on this safe board."

Instead of:
> "BET"

The teaching oracle gets another dimension to explain.

## Challenges to solve before building

1. **Team consensus becomes harder.** With class labels: "5/6 teams
   chose BET" is easy. With distributions: how do you combine 6
   probability estimates? Average? Weight by confidence? The
   comparison report becomes more complex.

2. **Agent cognitive load.** Asking for action frequencies is harder
   than picking one action. Labelling slows down.

3. **Solver budget explodes.** To validate distributions you need
   solver output on most hands, not just escalations. The solver
   effectively becomes the labeller.

4. **Mandatory composition rules need rethinking.** Current
   mandatory tagging for BET/RAISE/CALL/FOLD assumes a single
   action per hand. With distributions, every hand has some
   probability mass on multiple actions.

## When to revisit

After v2.2 ships and stabilises. Specifically:
- v2.2 must be deployed and showing accuracy improvements
- Pass 1 labelling must be complete (to have baseline class labels
  to compare against)
- Solver verification pipeline must be mature (since distributions
  require heavy solver use)
- Teaching system must be consuming Phase 3 enriched output
  (intentions, street plans) — so distributions are the natural
  next enrichment

## Easy first step (if low-risk data collection desired)

Add the coarse 3-level `action_lean` field to the labelling prompt
as an OPTIONAL output. Agents estimate primary_strength
(strong/moderate/marginal). Collect it in Pass 2 or a later batch.
Zero risk — it's optional data that doesn't affect v2.2 training.
The data is there when ready to experiment with distribution
training in v2.3 or v3.0.

## Related concepts to remember

- **Action confidence as soft proxy.** The current `confidence`
  field (HIGH/MEDIUM/LOW) is a primitive version of this. LOW
  confidence ≈ marginal lean. MEDIUM ≈ moderate. HIGH ≈ strong.
  We could extract this signal from existing data without new
  fields.
- **Difficulty as soft proxy.** Difficulty 3 (boundary) hands are
  by definition closer to mixed strategy. Difficulty 1 (clear)
  hands are near-pure strategy.
- **Intention multi-label as partial distribution.** When a hand
  has 2 intentions (value + protection), it's partially capturing
  the mixed nature of the decision.

Existing data already has proxies for the distribution concept.
Making them explicit is the v2.3+ upgrade.

---

**Revisit trigger:** After v2.2 ships and Phase 4 training
confirms the current pipeline works. Revisit before planning
v2.3 scope.
