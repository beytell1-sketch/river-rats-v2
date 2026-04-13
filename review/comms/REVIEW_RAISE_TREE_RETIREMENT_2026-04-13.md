---
date: 2026-04-13
from: Owner (Rupert) + Main terminal
to: Builder team + Teaching team
re: RAISE decision tree retirement — switch to unified 5-factor labelling
status: APPROVED — proceed on this basis
---

# Review: Retire the RAISE Decision Tree

## 1. What this document is

Two audiences:

- **Builder team:** What to change in the v2.2 labelling pipeline
  before retraining. Specific instructions, specific files, specific
  data fixes.
- **Teaching team:** Why the change is happening, how it aligns with
  what you're already building in spot_classifier.py, and what it
  means for coaching explanations going forward.

Read the section relevant to your role. Section 6 (shared context)
is for everyone.

---

## 2. The problem we found

### 2.1 Two different reasoning models

The project currently has two contradictory approaches to poker
decision-making:

**Labelling (how training labels are produced):**
Sequential elimination via the RAISE Decision Tree v2
(`review/RAISE_DECISION_TREE_V2.md`). The tree asks "should I
RAISE?" and works backwards through 6 gates:

```
Step 1: Flat spot check (gates that suppress ALL raises)
Step 2: Monster value raise (is_monster == 1)
Step 3: Low SPR commit (spr <= 1.5 AND hero_range_percentile >= 0.90)
Step 4: Thin value OOP check-raise (8 conjunctive conditions)
Step 5: Semi-bluff raise (6 conjunctive conditions including
        flush_draw_rank >= 12 AND flush_block_pct > 0)
Step 6: Bluff raise (river only, 6 conjunctive conditions)
Default: No step fired → CALL
```

This starts from the action and checks if conditions permit it.

**Teaching (how coaching explanations are produced):**
Hand-bucket-first classification via `spot_classifier.py`. The
teaching system asks "what kind of hand do I have?" then maps
(hand_bucket + action + context) to a strategic role:

```
Step 1: Classify hand → bucket (monster, strong_made, medium_made,
        weak_made, drawing, air)
Step 2: Map (action + bucket + context) → strategic role
        (value_bet, semi_bluff, pot_control, protection, etc.)
```

This starts from the hand and reasons forward to the action.

**These are fundamentally different reasoning paths.** The labelling
tree can produce a RAISE label via Step 5 (6 conjunctive gates
firing) while the teaching system explains the same hand as
"semi_bluff because you have a drawing hand." The label and the
explanation are produced by completely different logic.

### 2.2 The RAISE tree suppresses non-monster raises

Empirical evidence from the current training data
(`training-data/train_3way_v2.2.csv`, 349 rows):

| Metric | Value |
|---|---|
| Total RAISE labels | 13 of 349 (3.7%) |
| RAISE where is_monster=1 | **13 of 13 (100%)** |
| Non-monster RAISE | **0** |
| flush_block_pct value in RAISE rows | NULL in all 13 |
| hero_range_percentile in RAISE rows | NULL in all 13 |
| flush_draw_rank in RAISE rows | NULL in all 13 |

Compare with the facing-bet test set
(`training-data/facing_bet_test_set_40.jsonl`, 40 hands):

| Metric | Value |
|---|---|
| Total RAISE | 9 of 40 (22.5%) |
| Monster RAISE | ~6 (sets, straights, flushes) |
| Non-monster RAISE | ~3 (FB-04: nut flush draw + blocker, FB-14: combo draw, FB-24: two pair) |

**The model has never seen a non-monster RAISE in training.** It
cannot learn to predict what it has never been shown. The 3.7% vs
22.5% RAISE rate (6x gap) is a direct consequence.

### 2.3 Why the tree fails on non-monster raises

Two separate causes:

**Cause 1 — Key features are NULL in training data.**
Step 5 (semi-bluff raise) requires `flush_block_pct > 0` AND
`flush_draw_rank >= 12`. But `flush_block_pct`, `flush_draw_rank`,
and `hero_range_percentile` are NULL (not zero — NULL) in 100% of
the v2.2 training CSV. These features exist in `feature_keys.py`
and `feature_extractor.py` but were not populated when the training
data was generated. Step 5 literally cannot fire.

**Cause 2 — No path for non-monster value raises.**
The tree has no step for "strong two pair facing a bet → RAISE."
Two pair (hand_category=10) is NOT is_monster, so Step 2 doesn't
fire. Step 3 requires spr <= 1.5 AND hero_range_percentile >= 0.90
(both of which may not apply). Step 4 is OOP-only. There is no IP
value raise path for strong-but-not-monster hands. FB-24 (AhKc
making two pair on AdKd river) is a test set RAISE that has no
viable path through the tree.

### 2.4 How experts actually reason (and why it matters for teaching)

Every major coaching source teaches hand-bucket-first reasoning:

- **Upswing Poker:** "Categorize your hand (nuts, strong, medium,
  draw, trash), then decide your action based on the category and
  situation."
- **Peter Clarke (Grinder's Manual, From The Ground Up):** Range
  buckets → action. "What is my hand relative to the ranges in
  play? Then: what does that imply about my action?"
- **Pokercoaching.com:** Hand strength tiers → strategic role →
  action.
- **GTO Wizard articles:** Solver outputs are presented as "hands
  in this bucket take this action at this frequency."

No major coaching source teaches sequential action elimination
("first check if you should raise, then check if you should fold,
then default to call"). This is not how humans learn to think about
poker, and it is not how solvers compute.

**Your teaching system already mirrors the coaching approach.**
`spot_classifier.py` lines 39-67 classify the hand into a bucket,
then lines 74-158 map (action + bucket + context) → strategic role.
This is the same hand-bucket-first reasoning that coaches use. The
RAISE tree is the only part of the system that doesn't follow this
pattern.

---

## 3. The decision

**Retire the RAISE Decision Tree v2.** Do not use it for v2.2
labelling or any future labelling.

**Use the 5-factor framework for ALL actions including RAISE.** The
GTO Expert labelling agents already use the 5-factor framework
(gto_labeller_v1.md) for BET/CHECK/CALL/FOLD decisions. RAISE
should be handled the same way — the agent weighs all 5 factors,
reasons from the hand's strength and context, and chooses the
correct action. The KB (knowledge/three_way_gto.md v1.3) already
contains everything needed:

- Section 1.7: Semi-bluff conditions (solver-verified)
- Section 1.8: Blocker effects on action selection
- Worked Example 9: Nut draw raise with blocker
- DO NOT Rule #2: Semi-bluff carve-out for nut draws

The agents don't need a separate decision tree. They need the
same hand-bucket-first reasoning the coaching system uses.

**Why this is not risky:**

1. The 5-factor framework already handles 95%+ of labelling
   decisions (all non-RAISE actions). It is proven.
2. The RAISE tree produced only monster RAISEs — the framework
   cannot do worse.
3. The KB v1.3 has detailed RAISE guidance with solver-verified
   conditions and worked examples.
4. The calibration exam (20/24 gate) catches systematic errors
   before any labels are produced.

---

## 4. Builder team — what to change

### 4.1 Labelling pipeline changes

**A. Remove the RAISE tree from the labelling flow.**

The RAISE Decision Tree v2 (`review/RAISE_DECISION_TREE_V2.md`) is
no longer used for labelling. The labelling prompt
(`prompts/gto_labeller_v1.md`) already instructs agents to reason
through all 5 factors for every hand. No code change is needed in
the prompt itself — the agents already consider RAISE as a possible
action. What changes is that we no longer override the agents'
RAISE judgment with a deterministic tree.

If there is any code or scripting that applies the tree's Step 1-6
logic to override agent labels, remove it. The agents' 5-factor
reasoning is now authoritative for all actions.

**B. Update the labelling prompt's calibration notes.**

In `prompts/gto_labeller_v1.md`, lines 269-276, the calibration
notes section still lists MW-30 as FOLD. Per the solver correction
(KB v1.3 Example 3), MW-30 is CALL. Update:

```
Before:
- **MW-30:** FOLD despite 0.399 equity (bet-and-call signal)

After:
- **MW-30:** CALL despite bet-and-call signal (solver-verified:
  40% equity vs 18% pot odds, composition triple shows <40% TP+
  — equity surplus overrides action-implied narrowing)
```

Also in `prompts/gto_labeller_v1.md`, line 128:
`villain_range_capped` is listed as a Factor 3 signal. The KB v1.3
demoted this to a preflop structural label only (Section 1.9, DO
NOT Rule #8). Update the prompt to match the KB:

```
Before:
- `villain_range_capped`: 1 = no premiums (cold-caller pattern)

After:
- `villain_range_capped`: preflop structural label only — do NOT
  use as a postflop strength signal. Read the composition triple
  (villain_top_pair_plus_pct, villain_draw_pct, villain_air_pct)
  for postflop strength. See KB Section 1.9.
```

**C. Populate missing features in training data.**

The following features are NULL in the v2.2 training CSV but are
required for the model to learn non-monster RAISE patterns:

| Feature | Source | Status |
|---|---|---|
| flush_block_pct | feature_extractor.py (Step 12) | NULL in CSV — must populate |
| flush_draw_rank | feature_extractor.py (Step 13) | NULL in CSV — must populate |
| hero_range_percentile | feature_extractor.py (Step 13) | NULL in CSV — must populate |
| overcard_outs | feature_extractor.py | Present but verify |
| has_showdown_value | feature_extractor.py | Present but verify |

**Action required:** Before generating batch 4 factory data or
retraining, verify that the CSV export pipeline populates ALL 48
features (features 1-48, with 49-53 deferred to v2.3). Run the
feature extractor on a sample of existing training situations and
confirm no features are NULL. If the older training data (v2.1
existing 348 rows) has NULL features, re-extract features for those
rows from the source JSONL files.

**This is a prerequisite for v2.2 retraining.** Training on data
with NULL features wastes the training run.

**D. Add RAISE factory situations to batch 4.**

The v2.2 plan (PLAN_V2.2_RETRAIN_2026-04-13.md) specifies ~104
batch 4 situations across BP1-BP6, all targeting BET/CHECK. Add a
new batch pattern:

**BP7 — Non-Monster RAISE Situations (~15-20 situations):**

| Sub-pattern | Count | Description | Expected label |
|---|---|---|---|
| BP7a: Nut flush draw + blocker | 5 | Hero holds As/Ks with flush draw, facing bet, blocker to villain's flush range | RAISE (semi-bluff) |
| BP7b: Combo draw | 5 | Hero holds flush draw + straight draw (8+ outs), facing bet, non-paired board | RAISE (semi-bluff) |
| BP7c: Strong two pair | 3-4 | Hero holds two pair (not set), facing bet, low-medium SPR | RAISE (value) |
| BP7d: RAISE counterexamples | 4-5 | Nut draw WITHOUT blocker, non-nut draw, draw on paired board → expected CALL | CALL |

BP7d is critical — the model needs to see the boundary between
RAISE and CALL for draws. The KB (Section 1.7) defines this boundary
precisely: nut draw + blocker + side equity = RAISE; anything less
= CALL. The factory situations must include both sides.

Design these situations using solver-aligned sizing (25%/66% flop,
33%/75% turn, 33%/75%/150% river) per the mandatory pre-flight
protocol.

**E. Update the v2.2 plan.**

The retrain plan (PLAN_V2.2_RETRAIN_2026-04-13.md) needs these
amendments:

1. Total training data: ~467-472 rows (348 existing + ~104 BET/CHECK
   + ~15-20 RAISE)
2. Batch 4 breakdown: add BP7 (non-monster RAISE situations)
3. Labelling: all actions via 5-factor framework (no RAISE tree)
4. Success criteria: add RAISE accuracy target for facing-bet set:
   maintain ≥ 56% (current baseline), target 67%+ (6/9)
5. Prerequisite: NULL feature audit passes before any training run

### 4.2 What NOT to change

- **The KB (knowledge/three_way_gto.md v1.3):** No changes. The KB
  already contains the correct RAISE guidance. The 5-factor
  framework, the semi-bluff conditions, the blocker logic, the
  worked examples — all correct and solver-verified.
- **The calibration exam:** Keep the 20/24 gate. The exam tests
  whether agents can reason correctly, which is exactly what we
  need now that agents handle RAISE reasoning directly.
- **The XGBoost model architecture:** No changes. The model learns
  from features → action. How labels are produced (tree vs
  framework) is invisible to the model.
- **The facing-bet test set:** Already shipped (commit 22b02e9).
  No changes.
- **The reference set:** Already corrected (MW-31/MW-34, commit
  6379761). No changes.

---

## 5. Teaching team — what this means for you

### 5.1 Your approach is correct

The hand-bucket-first reasoning in `spot_classifier.py` is the
right approach. It mirrors how every major coaching source teaches
poker decision-making:

```python
# spot_classifier.py — this is the expert coaching model
def _classify_hand_bucket(equity, is_made_hand, draw_outs):
    if equity > 0.80: return 'monster'
    if draw_outs >= 4 and not is_made_hand: return 'drawing'
    if is_made_hand:
        if equity > 0.55: return 'strong_made'
        if equity >= 0.35: return 'medium_made'
        ...
    return 'air'

# Then: (action + bucket + context) → strategic role
# RAISE + drawing + draw_outs >= 8 → 'semi_bluff'
# RAISE + monster/strong_made → 'value_bet'
```

The labelling system is now being aligned to this same reasoning
model. When a GTO Expert agent labels a hand as RAISE, it will be
reasoning "this is a drawing hand with a nut flush draw and a
blocker — the strategic role is semi-bluff raise" — the same logic
your spot_classifier uses. Labels and teaching explanations will
flow from the same reasoning chain.

### 5.2 What changes for teaching

**Before:** The oracle might predict RAISE for a combo draw, but
the label was produced by a sequential tree (Step 5 fired because
6 feature thresholds were met). The teaching system would explain
it as "semi-bluff because you have a drawing hand" — a different
reasoning path than the one that produced the label.

**After:** The oracle predicts RAISE for a combo draw because the
training label was produced by an agent reasoning "this is a
drawing hand with a nut flush draw, a blocker to villain's flush
range, and side equity — the strategic role is semi-bluff raise."
The teaching system explains it the same way. Label production and
teaching explanation now follow the same reasoning chain.

### 5.3 New RAISE spots the model will learn

The model will now see training examples for these RAISE patterns
that it currently cannot predict:

| Pattern | Hand bucket | Strategic role | Teaching angle |
|---|---|---|---|
| Nut flush draw + blocker facing bet | drawing | semi_bluff | "You have a strong draw with a key blocker — raising folds out hands that might outdraw you and builds the pot for when you hit" |
| Combo draw (flush + straight) facing bet | drawing | semi_bluff | "Your combined outs give you ~44% equity even if called, plus fold equity against both opponents" |
| Strong two pair facing bet | strong_made | value_bet | "Two pair is strong enough to raise for value — you beat top pair and most of villain's continuing range" |

The teaching team should be prepared to handle these spots in
coaching explanations. The `spot_classifier.py` mapping at lines
147-155 already handles them correctly:

```python
if action == 'RAISE':
    if hand_bucket in ('monster', 'strong_made'):
        return 'value_bet'
    if hand_bucket == 'drawing' and draw_outs >= 8:
        return 'semi_bluff'
```

No code changes needed in the teaching system.

### 5.4 The teaching alignment principle

Going forward, the labelling system and the teaching system share
one reasoning model:

```
Hand → Bucket → (Bucket + Situation) → Action → Strategic Role
```

This is the same chain a coach walks a student through:

1. "What do you have?" (hand bucket)
2. "What's the situation?" (position, board, villain ranges, action
   history)
3. "What should you do?" (action)
4. "Why?" (strategic role)

The oracle's prediction, the training label, and the coaching
explanation all follow this chain. When they diverge, something
is wrong — and we can trace the divergence to a specific step.

---

## 6. Shared context — why this matters

### 6.1 The core insight

River Rats is a teaching tool. The oracle's job is not just to be
accurate — it's to make decisions that can be explained in a way
that helps players learn. An oracle that is accurate but reasons
in a way that cannot be taught is less valuable than an oracle that
reasons the way coaches teach.

The sequential RAISE tree was accurate for monsters (100% of its
output was is_monster=1). But it produced labels via a reasoning
chain that no coach would use and no student would follow. Dropping
it and using the same hand-bucket-first reasoning that coaches
teach means:

- Labels are more likely to be correct (agents reason through the
  full 5-factor framework, not a narrow gate sequence)
- Labels produce richer training signal (the model sees non-monster
  RAISE patterns it has never seen before)
- Teaching explanations are grounded in the same reasoning that
  produced the label

### 6.2 What this is NOT

- **Not a solver-copying exercise.** We are not trying to replicate
  solver output. We are trying to replicate how expert coaches
  reason about poker decisions — which is what makes the teaching
  system useful.
- **Not an architecture redesign.** The XGBoost model, the feature
  pipeline, the coaching system, the test sets — all unchanged. We
  are fixing how labels are produced, not how the system works.
- **Not a v2.2 scope expansion.** The v2.2 retrain plan is amended
  (add BP7 RAISE situations, remove RAISE tree dependency, add
  RAISE accuracy target), not replaced.

### 6.3 Risk assessment

| Risk | Likelihood | Mitigation |
|---|---|---|
| Agents over-label RAISE without tree gates | Medium | Calibration exam (20/24) catches bias. KB v1.3 has explicit "DO NOT semi-bluff 3-way" defaults with narrow carve-outs. Reviewer agents check KB consistency. |
| Non-monster RAISE labels are wrong | Low | Solver verification protocol covers BET with equity < 0.50 and any RAISE that isn't a monster. Owner runs in GTO Wizard with solver-aligned sizing. |
| RAISE accuracy doesn't improve | Medium | 15-20 new RAISE training examples is a small number. If accuracy stays flat, batch 5 adds more RAISE situations with solver verification. |
| Teaching explanations become inconsistent | Low | spot_classifier.py already handles RAISE correctly. No code change needed. |

---

## 7. Immediate next steps

### For the builder:

1. Audit the CSV export pipeline — confirm ALL 48 features are
   populated (no NULLs). Fix any that are missing. This is the
   blocker.
2. Re-extract features for existing 348 training rows if any
   features are NULL.
3. Design BP7 RAISE factory situations (15-20 hands) per Section
   4.1.D.
4. Update gto_labeller_v1.md per Section 4.1.B (MW-30 correction,
   villain_range_capped demotion).
5. Amend v2.2 plan per Section 4.1.E.
6. Proceed with calibration (as originally planned).

### For the teaching team:

1. No code changes required in spot_classifier.py or the coaching
   pipeline.
2. Be aware that v2.2 will produce RAISE predictions for non-monster
   hands (combo draws, nut flush draws with blockers, strong two
   pair). Verify that coaching explanations for these spots read
   naturally.
3. The alignment principle in Section 5.4 is the design standard
   going forward. If you find a spot where the oracle's action
   and the teaching explanation don't follow the same reasoning
   chain, flag it — that's a bug.

---

**This review is approved. Builder may proceed.**
