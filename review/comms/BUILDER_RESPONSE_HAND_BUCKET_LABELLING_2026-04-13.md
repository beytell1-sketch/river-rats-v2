---
date: 2026-04-13
from: Builder team
to: Teaching team + Owner
re: Hand-bucket-first labelling — yes, it works. Here's what changes.
status: FOR OWNER REVIEW
---

# Builder Response: Hand-Bucket-First Labelling

## 1. Answer to teaching's question

**Yes, hand-bucket-first reasoning works for labelling. It is
structurally better than what we have. Here's why and what it
changes.**

## 2. The problem we now understand

The current labelling prompt (`prompts/gto_labeller_v1.md`) tells
agents to "reason through all 5 factors before deciding." The
5-factor framework is sound. But the prompt does not tell agents
HOW to organise their reasoning. It lists 5 factors in order
(equity, position, range composition, board texture, action history)
and says "resolve conflicts."

In practice, agents reason sequentially through the factor list.
The retired decision trees made this explicit — RAISE tree first,
then FOLD tree, then default CALL. But even without the trees, the
prompt's structure encourages sequential processing: evaluate
Factor 1, then Factor 2, etc., then resolve.

The cognitive science research confirms this creates three biases:

**Bias 1: Anchoring from evaluation order.** Whichever action the
agent considers first (typically the one suggested by Factor 1 —
equity) anchors all subsequent reasoning. If equity says CALL, the
agent needs strong evidence from other factors to override it.

**Bias 2: Default-option inflation.** When no factor strongly
dominates, the agent defaults to the "safe" action — CHECK when
not facing a bet, CALL when facing one. This is status quo bias.
The 63% passive bias in the oracle is this bias baked into
training labels.

**Bias 3: No hand identity.** The prompt never asks "what kind of
hand is this?" The agent reasons about features (equity numbers,
position flags, danger scores) without first establishing whether
this is a monster, a draw, a marginal made hand, or air. Without
hand identity, the agent can't reason about strategic role — it
can only compare numbers against thresholds.

## 3. What hand-bucket-first changes

The labelling prompt needs a structural change. Not a new framework
— a restructuring of HOW the 5-factor framework runs.

### Current flow (implicit sequential):
```
Factor 1 (equity) → impression of action
Factor 2 (position) → modify impression
Factor 3 (ranges) → modify further
Factor 4 (board) → modify further
Factor 5 (action history) → modify further
→ Resolve conflicts → Action
```

### Proposed flow (hand-bucket-first):
```
Step 1: CLASSIFY THE HAND
  What kind of hand is this?
  Use equity + is_made_hand + draw_outs to determine:
  → monster / strong_made / medium_made / weak_made / drawing / air

Step 2: READ THE SITUATION
  What context shapes the decision?
  → Position (IP/OOP/sandwich)
  → Board texture (static/dynamic, who it favours)
  → Villain ranges (composition triple: TP+/draws/air)
  → Action history (bet-and-call, check-raise, multi-street)
  → SPR and stack commitment

Step 3: MAP (HAND + SITUATION) → ACTION
  Given this hand type in this situation, what is correct?
  Consider all legal actions simultaneously.
  For each candidate action, state what strategic role this
  hand would play (value_bet, semi_bluff, pot_control,
  drawing_call, range_fold, etc.)

Step 4: VERIFY
  Does the chosen action match how a coach would explain it?
  "You have a [bucket] hand. In this situation, the correct
  play is [action] because [strategic role]."
  If this sentence doesn't make poker sense, reconsider.
```

### What this concretely fixes

**Monster-only RAISE:** Under the current flow, RAISE only happens
when specific gates fire. Under bucket-first, a drawing hand with
a nut flush draw and blocker is classified as "drawing" in Step 1.
In Step 3, the agent considers RAISE as a candidate and reasons:
"drawing hand + nut draw + blocker + fold equity = semi-bluff
raise." RAISE is on the table from the start, not gated behind
6 conjunctive conditions.

**Passive bias:** Under the current flow, ambiguous spots default
to CHECK/CALL. Under bucket-first, the agent classifies the hand
first. A medium_made hand facing a bet doesn't default to CALL —
the agent asks "what does a medium made hand do in this situation?"
and considers CALL, FOLD, and RAISE based on the situation context.
No action is the default.

**Teachability:** Under the current flow, the agent's reasoning is
"equity vs pot odds, position modifies, action history overrides."
Under bucket-first, the reasoning is "this is a drawing hand, in
this situation a semi-bluff raise is correct because..." — which
matches how the teaching system explains the decision. Label
production and teaching explanation follow the same chain.

## 4. Impact on existing 348 training labels

This is the hard part. The existing 348 labels were produced by
agents (and in some cases self-play evaluations) using the current
sequential-implicit flow. The labels carry the three biases above.

**Quantified evidence of bias in existing labels:**
- 13/13 RAISE labels are is_monster=1 (zero non-monster raises)
- 132/233 not-facing-bet labels are CHECK (57% — plausible but
  possibly passive-biased)
- 58/116 facing-bet labels are CALL (50% — the default action)

**What we cannot determine without relabelling:** Whether specific
CALL labels should be FOLD (over-calling from passive bias) or
RAISE (under-raising from gate failure). The bias is structural —
it shifts the distribution, but we can't point to individual wrong
labels without re-evaluating each hand.

**Options:**

**Option A: Relabel all 348 with bucket-first prompt.**
- Most thorough. Eliminates all sequential bias.
- Cost: ~35 GTO Expert agents + ~18 reviewers = ~53 agents.
- Risk: new labels may disagree with old on borderline hands,
  creating noise if the new labels have their own biases.

**Option B: Relabel the facing-bet subset (116 rows) only.**
- The facing-bet subset has the strongest evidence of bias
  (CALL default, monster-only RAISE, FOLD tree thresholds).
- The BET/CHECK subset (233 rows) has a 43% BET rate which
  is reasonable — less evidence of systematic bias.
- Cost: ~12 GTO Expert agents + ~6 reviewers = ~18 agents.
- Risk: BET/CHECK labels may also carry bias we haven't
  quantified.

**Option C: Spot-check sample, relabel if bias confirmed.**
- Take a stratified sample of ~40 hands (20 facing-bet,
  20 not-facing-bet). Relabel with bucket-first prompt.
  Compare old vs new labels.
- If disagreement rate > 15%, relabel the full subset.
- If disagreement rate ≤ 15%, existing labels are good
  enough — add batch 4 with bucket-first and retrain.
- Cost: ~4 GTO Expert agents + ~2 reviewers = ~6 agents
  for the sample. Full relabel only if triggered.

**Builder recommendation: Option C.**

Why: We don't know the actual magnitude of the bias in
finished labels. The 63% passive bias is measured in the
MODEL, not in the labels — the model may amplify label bias
through class weighting and feature interactions. A spot-check
tells us whether the labels themselves are contaminated or
whether the bias is primarily a model training issue (class
weights, feature coverage, NULL features).

If the spot-check shows ≤15% disagreement, the existing labels
are defensible and we can focus resources on:
1. Populating NULL features (flush_block_pct, flush_draw_rank,
   hero_range_percentile) across all 348 rows
2. Adding BP7 non-monster RAISE situations (15-20 new rows)
3. Adding batch 4 BET/CHECK situations (~104 new rows)
4. All new labels produced with bucket-first prompt

If the spot-check shows >15% disagreement, we relabel the
affected subset before retraining.

## 5. Labelling prompt changes (concrete)

The updated `prompts/gto_labeller_v1.md` needs these changes:

**A. Replace the Reasoning Protocol (lines 166-186) with:**

```
## Reasoning Protocol

For each hand, follow this sequence:

1. **CLASSIFY THE HAND.**
   Before considering any action, determine what kind of hand
   this is:
   - monster: equity > 80%, or set/straight/flush/full house
   - strong_made: made hand with equity > 55%
   - medium_made: made hand with equity 35-55%
   - weak_made: made hand with equity < 35%, few outs
   - drawing: not made but 4+ draw outs
   - air: not made, fewer than 4 outs

   State the bucket explicitly: "This is a [bucket] hand."

2. **READ THE SITUATION.**
   From the features provided, establish:
   - Position: IP, OOP, or sandwich?
   - Board: static or dynamic? Who does it favour?
   - Villain ranges: composition triple (TP+/draws/air)
   - Action history: any bet-and-call, check-raise, or
     multi-street aggression signals?
   - SPR: committed (< 2), standard (2-6), deep (> 6)?

3. **CONSIDER ALL ACTIONS.**
   For this hand bucket in this situation, evaluate every
   legal action. For each, state what strategic role the
   hand would play:
   - BET/RAISE with monster/strong → value_bet
   - BET/RAISE with drawing → semi_bluff (requires nut
     draw + blocker 3-way, per KB Section 1.7)
   - CHECK with strong → pot_control or trap
   - CALL with drawing → drawing_call (check pot odds)
   - FOLD with medium → range_fold (when action narrows
     ranges beyond equity)

   No action is the default. Each must earn its place.

4. **CHOOSE AND VERIFY.**
   Select the action with the strongest case. Then verify:
   "You have a [bucket] hand. The correct play is [action]
   because [strategic role] given [key situation factor]."
   If this sentence doesn't sound like a poker coach
   explaining the play, reconsider.
```

**B. Update Calibration Notes (lines 268-275):**

Replace MW-30 FOLD with MW-30 CALL per solver correction
(already flagged in retirement doc Section 4.1.B).

**C. Update Factor 3 (line 128):**

Demote villain_range_capped per KB v1.3 Section 1.9
(already flagged in retirement doc Section 4.1.B).

## 6. What this does NOT change

- **The XGBoost model architecture.** Still 5-class softmax,
  still 48 features for v2.2.
- **The feature pipeline.** No new features needed for
  bucket-first labelling. The bucket is determined by the
  agent's reasoning, not by a feature column.
- **The test sets.** Reference set and facing-bet test set
  are evaluation tools, not training data. Their labels were
  produced by the 5-factor framework + solver verification.
- **The teaching system.** spot_classifier.py already does
  bucket-first. No changes needed.
- **The v2.2 success criteria.** Same gates: reference ≥82.5%,
  facing-bet ≥70%, CALL accuracy ≥55%.

## 7. Immediate next steps (pending owner approval)

1. **Update gto_labeller_v1.md** with the bucket-first
   reasoning protocol (Section 5 above)
2. **Run spot-check** (Option C): 40 hands from existing 348,
   stratified by action and facing_bet, relabelled with
   bucket-first prompt, compared against existing labels
3. **Based on spot-check results:**
   - ≤15% disagreement → proceed with v2.2 as planned
     (existing labels + bucket-first batch 4 + BP7)
   - >15% disagreement → relabel affected subset before
     retraining
4. **Populate NULL features** across all existing rows
   (blocking prerequisite regardless of spot-check outcome)

---

**For owner: Does Option C (spot-check first) make sense, or
do you want full relabelling (Option A) regardless?**
