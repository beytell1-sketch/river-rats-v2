---
date: 2026-04-13
from: Owner + Main terminal
to: Builder team (Architecture Expert, ML Architect, GTO Expert)
re: Phase 3A enriched labelling output — three proposed additions, need expert input before plan
status: FOR EXPERT DISCUSSION — not a directive, not a plan yet
supersedes:
  - TEACHING_TO_BUILDER_FORWARD_THINKING_2026-04-13.md (concepts folded in here, that doc is now outdated)
---

# Phase 3A Enriched Output Briefing

## 0. Context

Phase 3A rewrites the labelling prompt to use bucket-first
reasoning. That's approved and unchanged. During the design
discussion, three additional ideas emerged about what the
labelling agents should OUTPUT alongside the action label. All
three are about collecting richer data now that enables better
teaching and potentially better models later.

**None of these change the v2.2 action model.** Model 1 still
trains on 5-class action labels from 48 features. These additions
are extra fields in the labelling JSON that get logged and stored.

We need your experts' assessment before any of this becomes a
plan. Specifically:

- **Architecture Expert:** Is the output schema reasonable? Does
  it overload the labelling agents? Integration concerns?
- **ML Architect:** Is the data actually useful for future models?
  What's noise vs signal? Feasibility of the v2.3 experiments?
- **GTO Expert:** Can labelling agents reliably produce these
  fields? Will they be consistent across agents? Are the
  vocabularies poker-correct?

---

## 1. Forward-Thinking (Street Plans)

### The gap

The current labelling prompt evaluates each street as an isolated
decision. The 5-factor framework asks "what is correct NOW?" but
never asks "what happens NEXT?" DO NOT Rule #7 says "consider the
full street tree" but gives no positive framework for how.

### What we propose

Labelling agents state a 1-2 sentence street plan for each
decision (flop and turn only — river has no future streets):

```json
"street_plan": "Bet flop for protection. If called, evaluate
  turn card — bet again on safe runouts, check-call on
  completing draws."
```

### Why it matters

- **Drawing hands:** Implied odds are the reason to call some
  draws — can't assess without thinking ahead
- **Medium hands:** Pot control only makes sense with a plan
  ("check flop, call one turn bet, fold river")
- **Protection bets:** Betting to deny equity is forward-looking
  by definition
- **Teaching:** "The plan is to bet flop and re-evaluate turn"
  is what a coach says. The current oracle can't produce this.

### Questions for experts

1. **GTO Expert:** Can agents reliably produce street plans
   in 1-2 sentences? Or will they write essays that slow
   labelling without adding signal?
2. **ML Architect:** Is the street plan text useful as future
   training data? Can it be classified into plan categories
   (value_barrel, pot_control, draw_and_evaluate, etc.) for
   a v2.3 model?
3. **Architecture Expert:** Any concern about requiring this
   field in the labelling pipeline? Impact on agent context?

---

## 2. Multi-Label Intentions

### The gap

The current `strategic_role` is a single string per hand. But
actions often have multiple simultaneous reasons. A top pair bet
on a wet flop is value AND protection at the same time. Forcing
one label loses information.

### What we propose

Replace `strategic_role` (single string) with `intentions` (list)
and `primary_intention` (string):

```json
"intentions": ["value_get_worse_to_call", "protection_fold_draws"],
"primary_intention": "protection_fold_draws"
```

### Proposed intention vocabulary (15 intentions)

**BET / RAISE:**

| Intention | What you want to happen |
|---|---|
| `value_get_worse_to_call` | Worse hands call, you profit |
| `thin_value_target_marginal_calls` | Targeting borderline calls from weaker holdings |
| `protection_fold_draws` | Fold out drawing hands that have equity against you |
| `equity_denial_prevent_free_cards` | Prevent future cards that shift equity |
| `semi_bluff_fold_equity_plus_draw` | Fold equity now + draw equity when called |
| `bluff_fold_out_better` | Pure bluff — fold out hands that beat you |
| `build_pot_for_future_streets` | Inflate pot to extract more later |

**CALL:**

| Intention | What you want to happen |
|---|---|
| `drawing_call_implied_odds` | Hit draw, win big pot on later streets |
| `drawing_call_direct_odds` | Pot odds alone justify the call |
| `defend_range_mandatory` | Must call to avoid exploitable fold frequency |
| `pot_odds_priced_in` | Price too good to fold with any showdown value |

**CHECK:**

| Intention | What you want to happen |
|---|---|
| `pot_control_medium_hand` | Manage pot size — hand can't handle a big pot |
| `trap_induce_villain_bet` | Let villain bet, then raise or call |
| `no_value_target` | Nothing worse calls, nothing better folds |
| `free_card_draw` | See next card cheaply with a draw |

**FOLD:**

| Intention | What you want to happen |
|---|---|
| `range_fold_action_narrows_above` | Action puts you below villain's range |
| `equity_denial_accepted` | Can't profitably continue |

### Why multi-label matters

- **Teaching:** "You're betting for two reasons: to get value
  from weaker hands AND to fold out draws" is better coaching
  than "this is a protection bet"
- **Future model (v2.3):** A multi-label intention model learns
  to predict WHY from features. The oracle can explain itself.
- **Comparison report:** When old label and new label disagree,
  the intentions show whether the reasoning changed or just the
  conclusion

### Questions for experts

1. **GTO Expert:** Is the vocabulary complete? Any common poker
   intentions missing? Is multi-labelling realistic — can agents
   consistently identify 2-3 intentions? Or will they just tag
   everything with 2 intentions to satisfy the requirement?
2. **ML Architect:** With 385 rows and 15 intention categories,
   is there enough data for a v2.3 multi-label model? What's
   the minimum viable training size per intention?
3. **Architecture Expert:** Does the list → string relationship
   (`intentions` list + `primary_intention` scalar) create any
   schema complexity downstream? Should `primary_intention` just
   be derived as `intentions[0]` instead of a separate field?

---

## 3. Expert Feature Attention

### The concept

When a labelling agent decides "BET for protection," they looked
at specific features to reach that conclusion — `danger_score`
was high, `villain_draw_pct` was significant. Currently that
reasoning is buried in free text. What if they explicitly tag
which features from the 48-feature vector drove the decision?

```json
"feature_attention": {
  "danger_score": "PRIMARY",
  "villain_draw_pct": "PRIMARY",
  "equity_vs_range": "SUPPORTING",
  "is_ip": "SUPPORTING"
}
```

### Two attention levels (not three)

| Level | Meaning |
|---|---|
| `PRIMARY` | Main driver — without this feature, the decision might change |
| `SUPPORTING` | Reinforces the decision but didn't drive it alone |

**Why no "NOT_RELEVANT" level:** Experts can reliably say what
they DID look at. They cannot reliably say what doesn't matter.
XGBoost finds non-obvious feature interactions across hundreds
of hands that no expert sees from a single hand. If an expert
flags `is_paired_board` as irrelevant for a protection bet, but
the model discovers paired boards interact with protection across
385 hands, the expert's "not relevant" label becomes a blind spot
that propagates into teaching.

Absence from the attention map already means "not flagged by the
expert." The model and the teaching oracle decide for themselves
what matters among the unflagged features. We only record what
the expert positively identified as important — not what they
dismissed.

### Three uses

**Use 1 — Teaching oracle (v2.3):**

Train a model that learns which features to highlight for each
(action + intention) combination. The teaching system stops
relying on SHAP (which shows what the MODEL weighted) and
instead uses expert attention (which shows what an EXPERT would
highlight). These can diverge significantly:

| Situation | SHAP says | Expert says |
|---|---|---|
| Protection bet | `raw_equity` (top weight) | `danger_score` + `villain_draw_pct` |
| Drawing call | `pot_odds` | `draw_outs` + `improvement_probability` |
| Range fold | `facing_bet` | `villain_top_pair_plus_pct` + `num_callers_to_bet` |

A teaching oracle trained on expert attention produces
explanations grounded in expert reasoning, not model internals.

**Use 2 — Logic-teaching alignment check (v2.2, post-training):**

After v2.2 trains, compare model SHAP vs expert attention per
hand. Where they agree, the model learned the right reasoning.
Where they diverge, the model is using the wrong features —
fragile decisions that will break on edge cases. This check is
free (just analysis, no model change) and immediately valuable.

**Use 3 — Feature weighting experiment (v2.3+):**

Hands where model SHAP and expert attention agree get lower
training weight (model already learned this). Hands where they
disagree get higher weight (model needs correction). Retrain
with adjusted weights — the model is steered toward expert
reasoning, not just expert labels. Speculative but testable.

### Questions for experts

1. **GTO Expert:** Can labelling agents reliably tag 2-4 PRIMARY
   features per hand using exact feature names from the 48-feature
   vector? Or will they tag vague concepts ("equity was important")
   instead of specific features (`equity_vs_range`)? Do agents
   need the feature list in their prompt to tag correctly?
2. **ML Architect:** Is expert attention useful as training signal
   for a secondary model? How many labelled examples do you need
   for a "which features matter" model to be reliable? Is the
   SHAP-vs-attention comparison (Use 2) straightforward to
   implement post-training?
3. **Architecture Expert:** Does adding `feature_attention` to
   every labelled hand significantly increase context size for
   labelling agents? (They'd need the full feature list to tag
   correctly.) Is there a simpler schema that captures the same
   information — e.g., just a list of PRIMARY feature names
   instead of a full attention dict?

---

## 4. The combined output schema (if all three are adopted)

```json
{
  "situation_id": "d0244_CO_river",
  "hand_bucket": "strong_made",
  "action": "BET",
  "intentions": [
    "protection_fold_draws",
    "value_get_worse_to_call"
  ],
  "primary_intention": "protection_fold_draws",
  "feature_attention": {
    "danger_score": "PRIMARY",
    "villain_draw_pct": "PRIMARY",
    "equity_vs_range": "SUPPORTING",
    "is_ip": "SUPPORTING"
  },
  "street_plan": "Bet flop for protection. If called, evaluate
    turn — bet safe runouts, check-call completing draws.",
  "confidence": "HIGH",
  "reasoning": "Strong made hand on wet board. Danger score 0.72
    indicates significant draw equity in villain ranges. Betting
    denies free cards and extracts value from weaker made hands.
    IP position supports aggression.",
  "alternatives_considered": [
    "CHECK: rejected — dynamic board with 30% villain draws,
    free card too costly"
  ],
  "difficulty": 2
}
```

### Concern: agent overload

This is significantly richer output than the current prompt
produces. The question is whether labelling agents can produce
all of this reliably at ≤10 hands per agent without quality
degradation.

**Possible mitigations:**
- Make `feature_attention` optional for difficulty 1 hands
  (clear decisions where the features are obvious)
- Make `street_plan` omitted for river (already planned)
- Emphasise that `intentions` is 1-3 items, not an exhaustive
  list

**Or:** The experts may say some of these fields add noise, not
signal. That's a valid finding. We'd rather collect 2 high-
quality fields than 3 where one is unreliable.

---

## 5. What we're asking for

**Not a plan. Not a decision. A discussion.**

Each expert assesses:
1. Which of the three additions (street_plan, intentions,
   feature_attention) are worth doing in v2.2?
2. Which should be deferred to v2.3?
3. Which are noise?
4. What's the agent overload risk?
5. Any alternative approaches we haven't considered?

The experts can disagree — that's the point. We want the
tension surfaced before committing to a schema.

**After expert input:** Owner reviews findings, decides which
fields are in scope for Phase 3A. Then builder writes the plan
for the approved fields. Teaching team reviews the plan for
alignment with teaching needs.

---

**Builder: please have your Architecture Expert, ML Architect,
and GTO Expert respond to the questions in Sections 1-3. Each
expert writes a short assessment (1 page max) to review/comms/.
Findings presented together — no need for sequential handoff.**
