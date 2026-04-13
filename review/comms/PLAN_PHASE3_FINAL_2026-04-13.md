---
date: 2026-04-13
from: Builder team
to: Owner (Rupert)
re: Phase 3 FINAL — pilot + 6-team parallel labelling + targeted deep review
status: FOR OWNER REVIEW
incorporates:
  - OWNER_DIRECTIVE_PHASE3_LABELLING_2026-04-13.md (6 teams, difficulty signal, simplified vocab)
  - PLAN_PHASE3_PILOT_AND_PRODUCTION_2026-04-13.md (pilot design, enriched output, seed vocabularies)
  - Expert panel v2 findings (emergent vocabulary, reason-first, all 3 fields adopted)
  - Expert panel features 49-54 (all 6 promoted)
supersedes:
  - PLAN_PHASE3_PILOT_AND_PRODUCTION_2026-04-13.md
---

# Phase 3 Final Plan

## Overview

```
Phase 3A: Prompt update + feature promotion (1 session)
Phase 3B: Calibration (0.5 session)
Pilot:    20 hands × 3 approaches (1 session) → Pilot gate
Pass 1:   6 independent teams × 385 hands (4-5 sessions)
          → Comparison report → Pass 1 gate
Pass 2:   Targeted deep review (2-3 sessions)
          → Solver verification → Pass 2 gate
Assembly: Final labels + vocabulary review (1 session)
          → Gate 6 (owner approves label set)
```

~275 agent-calls. ~11-14 sessions. 7 owner gates.

---

## Phase 3A: Prompt Update + Feature Promotion

### 3A.1 Promote features 49-54

**Code changes (Architecture Expert findings):**

| File | Change |
|------|--------|
| `train_model.py` line 28 | Add 6 feature names to FEATURE_COLUMNS |
| `gto_model.py` line 33 | Already has 49-53; add feature 54 |
| `sizing_oracle.py` line 92 | Add 6 feature names |
| `coaching/gto_model.py` line 33 | Add 6 feature names |
| `feature_extractor.py` ~line 1167 | Add `elif` branch for medium_made category (feature 54) |
| `feature_extractor.py` export list | Add feature 53 (silent bug: currently missing) |
| `feature_keys.py` | Add feature 54 constant |
| `tests/test_new_features.py` | Update count assertions (52→54) |

**Feature 51 check:** Verify `villain_fold_equity_estimate` formula
is nonlinear. If it equals `1 - tp_pct - draw_pct`, it's redundant
— drop it. If it uses a capped/product formula, keep it.

**After promotion:** Re-generate the 185 factory situations with
54 features. Re-extract the 200 reconstructed situations with 54
features. Verify zero NULLs across all 385 × 54.

### 3A.2 Update labelling prompt

Replace `prompts/gto_labeller_v1.md` reasoning protocol with
bucket-first + enriched output.

**Bucket-first reasoning (no thresholds):**

```
1. CLASSIFY THE HAND.
   Before considering any action, determine what kind of hand
   this is. Use poker reasoning, not numeric thresholds.

   - Monster: hands that are almost never behind (sets,
     straights, flushes, full houses)
   - Strong made: top pair top kicker, overpair on dry board
   - Medium made: top pair weak kicker, second pair
   - Weak made: bottom pair, third pair
   - Drawing: flush draws, straight draws, combo draws
   - Air: no made hand, no meaningful draw

   State the bucket: "This is a [bucket] hand."

2. READ THE SITUATION.
   - Position: IP, OOP, or sandwich?
   - Board: static or dynamic? Who does it favour?
   - Villain ranges: composition quad (TP+/medium made/draws/air)
   - Action history: bet-and-call, check-raise, multi-street?
   - SPR: committed (<2), standard (2-6), deep (>6)?

3. CONSIDER ALL ACTIONS.
   For this hand type in this situation, evaluate every legal
   action. Name the strategic role for each candidate.
   No action is the default. Each must earn its place.

4. CHOOSE AND VERIFY.
   "You have a [bucket] hand. The correct play is [action]
   because [strategic role] given [key situation factor]."
```

**Enriched output fields:**

```
Required for every hand:
  hand_bucket          — monster/strong_made/medium_made/weak_made/drawing/air
  action               — FOLD/CHECK/CALL/BET/RAISE
  confidence           — HIGH/MEDIUM/LOW
  difficulty           — 1 (clear) / 2 (standard) / 3 (boundary)
  reasoning            — free text, full factor analysis
  alternatives_considered — at least 1 alternative with rejection reason

Intention tagging (reason first, tag second):
  intentions_raw       — in your own words, WHY did you choose this action?
  intentions           — after writing intentions_raw, find matching tags
                         from the approved vocabulary. 1-3 tags. If no tag
                         fits, propose a new one in proposed_tags.
                         One intention is valid for clear spots. A second
                         tag that doesn't appear in your reasoning is noise.

Street plan tagging (flop/turn only, omit for river):
  street_plan_raw      — in your own words, what is the plan for the next street?
  street_plan_tags     — two-tag structure: [action_tag, response_tag]
                         After writing street_plan_raw, find matching tags.

Feature attention:
  feature_attention    — which features from the 54-feature vector drove
                         this decision? Tag 2-6 features as PRIMARY.
                         Definition: "without this feature value, the
                         label might change."
                         [Protocol determined by pilot — A, B, or C]

Tag proposals:
  proposed_tags        — empty list if all tags fit. Otherwise:
                         [{"category": "intentions"|"street_plans",
                           "proposed_name": "...",
                           "definition": "..."}]
```

**Calibration notes update:**
- MW-30: CALL (solver-corrected)
- MW-33: RAISE (set must raise vs bet+call)
- MW-50: FOLD (BTN raised flop, range narrowed)

**Factor 3 update:**
- `villain_range_capped`: demoted to preflop structural label
  per KB v1.3 Section 1.9

**54-feature vector in prompt:**
- All 54 features listed with descriptions
- `hero_range_percentile` explicitly framed: "1.0 = top of your
  range on this board"
- `villain_medium_made_pct` explained: "% of villain's range that
  is made hands below top pair"

**Gate 5: Owner reviews updated prompt.**

### 3A.3 Create tag vocabulary seed file

`training-data/tag_vocabulary.json`:

```json
{
  "intentions": {
    "value_extract": "Worse hands call, you profit on this street",
    "deny_equity": "Villain has draws; charge them or fold them out",
    "bluff_fold_better": "You are behind; you win only if villain folds",
    "continue_draw": "You have outs; future street equity justifies price",
    "pot_control": "Hand has showdown value but cannot handle large pot",
    "range_fold_priced_out": "Villain's action + range puts you too far behind"
  },
  "street_plan_actions": {
    "barrel_value": "Betting for value, plan to continue on most runouts",
    "bet_protect_evaluate": "Betting to deny equity, turn action depends on runout",
    "check_trap": "Checking strong hand to induce villain aggression",
    "check_pot_control": "Checking medium hand to manage pot size",
    "draw_continue": "Calling/checking with a draw, planning to realize equity"
  },
  "street_plan_responses": {
    "continue_on_blank": "Bet again if turn does not complete obvious draws",
    "give_up_on_complete": "Check/fold if draw completes",
    "check_evaluate": "No strong prior plan; reassess on turn card",
    "pot_control_check_call": "Check turn, call one bet, fold river to pressure",
    "bet_regardless": "Committed to multi-street aggression regardless of runout"
  }
}
```

---

## Phase 3B: Calibration

1 GTO Expert takes the 24-question blind exam with the updated
prompt + KB v1.3. Gate: 20/24 + all 3 GTO-reversal hands correct
(MW-30 CALL, MW-33 RAISE, MW-50 FOLD).

If calibration fails: diagnose, adjust prompt, re-run. Do not
proceed to pilot with a failing prompt.

---

## Pilot: 20 Hands × 3 Approaches

**Unchanged from the builder's pilot plan.** Summary:

- 20 hands selected from the 385 (10 reconstructed + 10 new,
  stratified by action/street/difficulty)
- 3 competing feature attention approaches tested:
  - A: Auto-tag Tier 1, agent removes with justification
  - B: Blank slate + automated Tier 1 check
  - C: Action-dependent auto-tags
- 2 independent labellers per approach × 3 approaches = 6 labellers
- 3 challengers (1 per approach)
- 10 agent-calls total

**Tier 1 candidate features (pilot validates):**

| Feature | Rationale |
|---------|-----------|
| `equity_vs_range` | Where hero stands against villain |
| `villain_top_pair_plus_pct` | Range composition — strength |
| `villain_draw_pct` | Range composition — draws |
| `villain_air_pct` | Range composition — weakness |
| `villain_medium_made_pct` | Range composition — thin value targets |
| `pot_odds` | Price of continuing |
| `is_ip` | Position |
| `hero_range_percentile` | Where hero sits in own range |

**Pilot evaluation:** inter-rater agreement on actions, features,
intentions. False positive/negative rates on feature tags. Which
approach produces the most consistent and accurate attention data.

**Pilot gate: Owner reviews results, selects approach for
production. Adjusts Tier 1 list if needed.**

---

## Pass 1: 6-Team Parallel Labelling (all 385 hands)

### Team structure

6 independent teams. Each team labels all 385 hands. No team
sees another team's output.

| Parameter | Value |
|-----------|-------|
| Hands per agent | ≤10 |
| Agents per team | 39 (385 ÷ 10, rounded up) |
| Teams | 6 |
| Total Pass 1 agent-calls | 234 |

### Team differentiation

To prevent correlated errors from identical sequencing:
- Each team receives the 385 situations in a **different random
  order** (6 random seeds)
- Each team's agents are assigned hands by shuffled index, not by
  situation_id order
- The prompt and vocabulary are identical — only the hand order
  differs

### Per-agent output

Each agent produces per hand:

```json
{
  "situation_id": "BP1_03",
  "team": "T1",
  "hand_bucket": "drawing",
  "action": "RAISE",
  "confidence": "HIGH",
  "difficulty": 2,
  "reasoning": "...",
  "intentions_raw": "I'm raising because...",
  "intentions": ["deny_equity", "bluff_fold_better"],
  "street_plan_raw": "Raise flop, if called...",
  "street_plan_tags": ["bet_protect_evaluate", "give_up_on_complete"],
  "feature_attention": {
    "flush_draw_rank": "PRIMARY",
    "villain_fold_equity_estimate": "PRIMARY",
    "equity_vs_range": "PRIMARY"
  },
  "proposed_tags": [],
  "alternatives_considered": ["CALL: rejected because..."]
}
```

### Pass 1 comparison report

Automated. For each of the 385 hands:

```
situation_id |
T1_action T2_action T3_action T4_action T5_action T6_action |
action_agreement (6/6, 5/6, 4/6, 3/3, fragmented) |
T1_diff T2_diff T3_diff T4_diff T5_diff T6_diff |
difficulty_agreement (CLEAR/LIKELY_CLEAR/STANDARD/HARD/CONTESTED) |
T1_bucket ... T6_bucket | bucket_agreement |
intention_jaccard (average pairwise across 6 teams) |
feature_jaccard (average pairwise across 6 teams) |
danger_flag (D1 majority + action split = "CONFIDENT_SPLIT") |
escalation_level
```

**Action consensus classification:**

| Agreement | Classification | Pass 2 action |
|-----------|---------------|---------------|
| 6/6 | UNANIMOUS | Done (unless difficulty CONTESTED) |
| 5/6 | STRONG | Examine dissent |
| 4/6 | MAJORITY | Expert panel reads all 6 |
| 3/3 | SPLIT | Solver verification mandatory |
| No majority | FRAGMENTED | Solver + owner review |

**Difficulty consensus classification:**

| Pattern | Classification | Pass 2 action |
|---------|---------------|---------------|
| 6/6 D1 | CLEAR | No extra review |
| 5/6 D1 | LIKELY CLEAR | Glance at dissent |
| 4+ D2 | STANDARD | Normal review |
| Any 3+ D3 | HARD | Full panel regardless of action consensus |
| No majority | CONTESTED | Full panel — difficulty disagreement is the finding |

**Special danger flag — CONFIDENT_SPLIT:**

When difficulty majority is D1 (most say easy) BUT action is
split (not unanimous). This is the most dangerous pattern —
confident and wrong. Mandatory solver verification. These hands
expose prompt bias.

**Pass 1 gate: Owner reviews the comparison report. Decides
which hands need Pass 2 treatment.**

---

## Pass 2: Targeted Deep Review

Only hands that need it. Based on Pass 1 results:

### Category A: UNANIMOUS + CLEAR (estimated ~30-40%)

Done. Label confirmed. No Pass 2 work.

### Category B: UNANIMOUS + STANDARD (estimated ~20-25%)

1 challenger agent per batch of ~10 hands.

The challenger:
- Argues the case for the action nobody picked
- Reviews untagged Tier 2 features
- Does NOT produce a new label — produces an assessment

If challenger finds nothing: confirmed.
If challenger raises a valid point: escalate.

Agent-calls: ~9-10

### Category C: STRONG 5/6 (estimated ~15-20%)

1 expert reviewer per batch of ~10 hands.

The reviewer:
- Reads all 6 team reasonings for each hand
- Examines the dissenting team's logic specifically
- Writes assessment: confirm majority, confirm minority, or
  inconclusive
- Recommends: confirm / escalate to solver / flag for owner

Agent-calls: ~6-8

### Category D: MAJORITY 4/6 or worse (estimated ~10-15%)

1 full expert panel agent per batch of ~10 hands.

The panel agent:
- Reads all 6 team reasonings slowly and carefully
- Identifies the specific point of disagreement
- Makes a poker judgment on which reasoning is stronger
- Writes detailed assessment with recommendation
- Solver verification triggered automatically

Agent-calls: ~4-6

### Category E: HARD or CONTESTED difficulty (estimated ~15-20%)

1 full expert panel agent per batch of ~10 hands.

Same treatment as Category D. These hands get full review
regardless of action consensus because the difficulty
disagreement itself is a finding worth investigating.

For difficulty disagreements specifically, the panel also
answers: "WHY did some experts think this was easy while
others thought it was hard? What did the hard-raters see?"

Agent-calls: ~6-8

### Category overlap

A hand can qualify for multiple categories (e.g., both 4/6
action AND CONTESTED difficulty). It gets the highest treatment
only — no duplicate reviews.

### Pass 2 escalation to solver

| Trigger | When |
|---------|------|
| Any 3/3 or FRAGMENTED action | Always |
| 4/6 action where dissent cites range composition | Always |
| CALL↔FOLD disagreement with equity 0.25-0.45 | Always |
| CALL↔RAISE disagreement | Always |
| BET with equity <0.40 on non-monster | Always |
| CONFIDENT_SPLIT (D1 majority + action split) | Always |
| Panel agent recommends solver | Always |
| Challenger makes strong case for unchosen action | Owner discretion |

### Pass 2 output

Per hand that went through Pass 2:

```
situation_id | pass2_category | reviewer_type |
assessment_summary | recommendation |
solver_needed | solver_result (if run) |
final_label | final_confidence
```

**Pass 2 gate: Owner reviews all Pass 2 findings + solver
results. Approves final label set.**

---

## Solver Verification

Owner runs flagged hands in GTO Wizard.

**Pre-flight mandatory:**
- Action sequences validated by hand_sequence_validator
- Bet sizes matching solver options EXACTLY (25%/66% flop,
  33%/75% turn/river)

**Estimated hands:** ~30-50 (from splits, CONFIDENT_SPLIT,
escalated disagreements).

**Output:** Solver result per hand — action, frequency, notes.
Label confirmed, flipped, or marked as mixed.

---

## Final Assembly

### Label selection per hand

| Situation | Final label source |
|-----------|-------------------|
| UNANIMOUS + no escalation | Any team's label (all agree) |
| STRONG 5/6 + dissent dismissed | Majority label |
| STRONG 5/6 + dissent confirmed | Minority label (with reasoning) |
| 4/6 + panel confirmed majority | Majority label |
| 4/6 + panel confirmed minority | Minority label |
| Split + solver resolved | Solver-informed label |
| Split + solver inconclusive | Owner decides |

### Vocabulary review (one-time, after all labelling)

After all labels are assembled:

1. Collect all proposed_tags across 6 teams × 385 hands
2. How many unique tags emerged?
3. Which are genuinely distinct vs synonyms?
4. Merge synonyms, reject noise, accept useful additions
5. Produce the final approved vocabulary
6. Apply merges to all labels (simple string replacement)

No mid-labelling vocabulary changes. No version numbers. No
migration scripts. One review, one cleanup.

### Comparison report (200 reconstructed situations)

For the 200 situations that have both old labels (sequential)
and new labels (bucket-first consensus):

```
situation_id | old_label | new_label | agree? |
classification | difficulty_consensus |
old_reasoning_available | new_intentions |
action_consensus (from 6 teams) | feature_jaccard
```

**Disagreement escalation (old vs new):**

| Disagreement | Action |
|--------------|--------|
| CALL→RAISE or RAISE→CALL | Solver verification mandatory |
| CALL→FOLD with equity >0.30 | Solver verification |
| >25% total disagreement | Review prompt for over-correction |
| ≤15% disagreement | High confidence in bucket-first |

**Gate 6: Owner reviews final label set, comparison report,
solver results, vocabulary. Approves for training.**

---

## Resource Summary

| Phase | Agent-calls | Sessions |
|-------|-------------|----------|
| 3A: Prompt + features | 1 (architect) | 1 |
| 3B: Calibration | 2 | 0.5 |
| Pilot | 10 | 1 |
| Pass 1: 6 teams × 39 | 234 | 4-5 |
| Pass 1 comparison | 1 (programmer) | 0.5 |
| Pass 2: targeted review | 25-32 | 2-3 |
| Solver verification | Owner | 1-2 |
| Assembly + vocab review | 2 | 1 |
| **Total Phase 3** | **~275-280** | **~11-14** |

## Owner Gates

| Gate | When | Decision |
|------|------|----------|
| Gate 5 | After 3A | Approve prompt + features |
| Pilot gate | After pilot | Select feature attention approach |
| Pass 1 gate | After comparison report | Which hands need Pass 2 |
| Pass 2 gate | After deep review + solver | Approve final labels |
| Gate 6 | After assembly | Approve label set for training |

## Risk Register

| Risk | Mitigation |
|------|------------|
| 6 teams all wrong on same hand (shared blind spot) | Challenger argues unchosen action. CONFIDENT_SPLIT flag catches confident-and-wrong. |
| Feature attention noisy across approaches | Pilot tests 3 approaches before committing. |
| Too many splits overwhelm solver budget | Estimated 30-50 hands. If >80, triage by equity margin — marginal zone first. |
| 275 agent-calls expensive | Quality over speed. Wrong labels → wrong model → retrain. The cost of labelling right is less than the cost of retraining. |
| Vocabulary explodes | One post-labelling review. No mid-stream changes. |
| CONFIDENT_SPLIT pattern is common (>15%) | Indicates prompt bias. Stop, diagnose prompt, potentially re-run affected hands. |
| Difficulty disagreement is noise, not signal | Pilot will show: if difficulty agreement is high on pilot hands, it's a reliable signal. If not, downweight it. |

---

**Awaiting owner review. On "go" the builder starts Phase 3A
(feature promotion + prompt update).**
