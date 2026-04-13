---
date: 2026-04-13
from: Teaching team (via owner)
to: Builder team
re: Hand-bucket-first reasoning — can logic use the same concept?
status: FOR DISCUSSION — teaching discovery, not a directive
---

# Teaching Discovery: Hand-Bucket-First Reasoning

## 1. What teaching built

The teaching system's `spot_classifier.py` classifies every hand
through a two-step chain:

```
Step 1: Hand → Bucket
  equity > 0.80           → monster
  draw_outs >= 4, !made   → drawing
  made + equity > 0.55    → strong_made
  made + equity >= 0.35   → medium_made
  made + equity < 0.35    → weak_made
  else                    → air

Step 2: (Action + Bucket + Context) → Strategic Role
  RAISE + monster/strong_made           → value_bet
  RAISE + drawing (any outs)            → semi_bluff
  BET + monster                         → value_bet
  BET + strong_made + danger > 0.50     → protection
  BET + drawing                         → semi_bluff
  CALL + drawing                        → drawing_call
  FOLD + medium_made                    → range_fold
  CHECK + monster                       → trap
  ... (full mapping in spot_classifier.py lines 74-158)
```

This was designed for teaching — to produce coaching explanations
that match how human coaches reason about poker. But during the
RAISE tree retirement review, we noticed something: **this reasoning
model is structurally better than the decision trees for labelling
too.**

## 2. The contrast

**Current labelling (decision trees):**
Sequential action elimination. Start from a candidate action, check
if feature gates permit it. The RAISE tree asks "should I RAISE?"
through 6 steps. The BET tree asks "should I BET?" through similar
gates. The FOLD tree asks "should I FOLD?"

Each tree reasons from action → conditions → yes/no. The trees are
independent — the RAISE tree doesn't know what the BET tree would
say about the same hand.

**Teaching's approach (hand-bucket-first):**
Start from the hand. Classify it once. Then map the (bucket +
situation) to the action and strategic role. All actions are
considered in parallel — the bucket determines what's possible,
the context determines which action wins.

## 3. Why this matters for labelling

### 3.1 The trees can't see across actions

The RAISE tree fires on is_monster and 5 narrow gate sequences.
The BET tree fires on equity thresholds and board texture. The
FOLD tree fires on equity-vs-pot-odds. But none of them asks the
fundamental question: **what kind of hand is this?**

A nut flush draw with a blocker could be:
- A RAISE (semi-bluff) via the RAISE tree Step 5
- A CALL (drawing hand with odds) via the FOLD tree's default
- A BET (semi-bluff) if checked to us

The trees handle this by having each tree independently evaluate
the hand against its own gates. If Step 5 fires, it's a RAISE.
If Step 5 doesn't fire (because flush_block_pct was NULL), it
falls through to CALL. The hand's identity is invisible — only
the gates matter.

Hand-bucket-first says: "This is a drawing hand with a nut flush
draw and a blocker. Given that, in this situation, the correct
action is RAISE because the draw has enough equity, the blocker
reduces villain's strong range, and fold equity is meaningful
3-way." The reasoning starts from what the hand IS, not from
which gate fires.

### 3.2 The trees produced the monster-only RAISE problem

The retirement review documented this: 13/13 training RAISEs were
is_monster=1. Zero non-monster RAISEs. The tree's Step 5 (semi-bluff
raise) required features that were NULL. But the deeper problem is
structural — if you start from "should I RAISE?" and work through
narrow gates, any missing gate kills the entire path. If you start
from "this is a drawing hand with a nut flush draw," the RAISE
option is on the table from the beginning — you evaluate it
alongside CALL, not as a separate gate sequence.

### 3.3 The coaching literature agrees

Every major coaching source teaches hand-bucket-first:
- Upswing: categorize your hand, then decide
- Peter Clarke: range buckets → action
- GTO Wizard: solver outputs presented by hand bucket
- No source teaches sequential action elimination

The teaching system mirrors what coaches do. If the labelling
system used the same reasoning chain, labels and explanations
would follow the same logic.

## 4. What we're suggesting (not demanding)

The 5-factor framework already used by the GTO Expert labelling
agents is compatible with hand-bucket-first reasoning. The
agents already classify hands implicitly when they reason through
the KB. What we're suggesting is making it explicit:

**Could the labelling prompt ask agents to classify the hand
bucket FIRST, then reason from (bucket + situation) to action?**

Something like:

```
For each hand:
1. Classify: What kind of hand is this?
   (monster / strong_made / medium_made / weak_made / drawing / air)
2. Situation: What's the context?
   (facing bet? position? board texture? SPR? villain ranges?)
3. Action: Given this hand type in this situation, what's correct?
4. Why: What's the strategic role of this action with this hand?
```

This doesn't replace the 5-factor framework — it structures HOW
the agent walks through the 5 factors. Factor 1 (equity) and
Factor 2 (position in range) determine the bucket. Factors 3-5
(villain ranges, board, bet sizing) determine the situation.
The action falls out of (bucket + situation).

## 5. What teaching gets if this works

If labelling and teaching share the same reasoning chain:

| Today | After alignment |
|-------|----------------|
| Label produced by tree gates, explanation produced by bucket reasoning | Both produced by bucket reasoning |
| RAISE label from Step 5 firing, teaching says "semi-bluff because drawing hand" | Both say "drawing hand → semi-bluff raise" |
| Teaching can't explain WHY a gate fired — only that it did | Teaching explains the same logic that produced the label |
| Divergences are invisible (different reasoning, same or different answer) | Divergences are traceable (same chain, different step) |

## 6. What we DON'T need

- We're not asking you to import spot_classifier.py into the
  labelling pipeline. The classifier uses the model's output
  (action + features) — the labelling agent needs to produce
  the action, not consume it.
- We're not asking you to change the XGBoost model or features.
- We're not asking you to delay v2.2. This is a framing change
  in the labelling prompt, not a pipeline rebuild.
- We're not asking you to copy teaching's equity thresholds
  (0.80 for monster, 0.55 for strong_made, etc.) into the
  labelling prompt. The GTO Expert should use poker reasoning
  to classify the hand, not rigid thresholds.

## 7. The one thing to check

The retirement review already approved retiring the RAISE tree
and using the 5-factor framework for all actions. This suggestion
is about structuring HOW the 5-factor reasoning runs — bucket
first, then situation, then action. If the builder team sees a
reason this wouldn't work for the labelling agents, we'd like to
understand why, because it would mean teaching and labelling are
reasoning differently and we'd need to account for that gap.

---

**This is a suggestion, not a directive. Builder team: does this
concept work for labelling logic? If so, how would you integrate
it? If not, what's the structural reason?**
