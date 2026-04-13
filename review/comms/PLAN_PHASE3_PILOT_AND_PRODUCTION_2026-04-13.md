---
date: 2026-04-13
from: Builder team
to: Owner (Rupert)
re: Phase 3 — pilot plan + full production labelling plan
status: FOR OWNER REVIEW
incorporates:
  - Bucket-first labelling (approved)
  - Enriched output: intentions, street plans, feature attention (expert panel v2)
  - Emergent vocabulary with seed lists (GTO Expert)
  - Reason-first tag-second protocol (owner directive)
  - Multi-expert independent labelling (owner directive)
  - Untagged feature review (owner directive)
  - Tier 1 feature auto-tag pilot (three competing approaches)
  - Features 49-54 promoted (expert panel)
  - Slow deliberate pace — 10 hands per batch (owner directive)
---

# Phase 3: Pilot Plan + Production Labelling Plan

This document has two parts:
1. **Pilot plan** (20 hands) — tests the labelling protocol before
   committing to 385 hands
2. **Production plan** (~385 hands) — executes after pilot findings
   are incorporated

---

# PART 1: PILOT PLAN

## 1.1 Purpose

The pilot answers five questions before we commit to production:

1. **Which feature attention approach works best?** (A, B, or C)
2. **Can agents produce reliable enriched output?** (intentions,
   street plans, feature attention — all at once)
3. **Does multi-expert independent labelling surface real
   disagreements?** (Or do all agents agree on everything?)
4. **Does the emergent vocabulary process work?** (Do agents
   propose useful new tags, or noise?)
5. **Is 10 hands per agent the right batch size?** (Quality
   drift on hands 8-10?)

## 1.2 Pilot design

**20 hands** selected from the 385 training set. Not throwaway —
pilot labels become production labels if the protocol holds.

### Hand selection (stratified)

| Criterion | Count | Why |
|-----------|-------|-----|
| Facing bet — CALL expected | 4 | Weakest eval axis |
| Facing bet — FOLD expected | 3 | Boundary decisions |
| Facing bet — RAISE expected | 3 | New action, untested |
| Not facing — BET expected | 4 | Value + protection mix |
| Not facing — CHECK expected | 3 | Pot control + trap |
| Difficulty 3 (boundary) | 3 | Hardest spots, most disagreement expected |
| **Total** | **20** | |

Select from both reconstructed (10) and new factory (10) to test
both data sources.

### Three competing approaches for feature attention

Each approach is tested by a separate team on the same 20 hands.

**Approach A — Auto-tag Tier 1, agent removes:**
- All Tier 1 features start pre-tagged
- Agent reviews each, removes any that didn't influence decision
- Must write one sentence per removal ("pot_odds removed because
  this is a BET decision")
- Tier 2 features: agent adds from scratch

**Approach B — Blank slate + automated check:**
- Agent tags all features from scratch (reason first, tag second)
- After tagging, automated check flags missing Tier 1 features
- Agent responds: add tag or explain why not relevant

**Approach C — Action-dependent auto-tags:**
- Different Tier 1 defaults per action:
  - CALL/FOLD: equity, pot_odds, range composition, position
  - BET/RAISE: equity, range composition, position, fold equity
    (NOT pot_odds)
  - CHECK: equity, range composition, position, showdown value
- Agent reviews and adjusts
- Tier 2: agent adds from scratch

### Tier 1 features (candidate list — pilot validates)

These are features that GTO reasoning should almost always
consider. The pilot determines which are truly universal vs
action-dependent.

| Feature | Why Tier 1 candidate |
|---------|---------------------|
| `equity_vs_range` | Where you stand against villain |
| `villain_top_pair_plus_pct` | Range composition — strength |
| `villain_draw_pct` | Range composition — draws |
| `villain_air_pct` | Range composition — weakness |
| `villain_medium_made_pct` | Range composition — thin value targets |
| `pot_odds` | Price of continuing (CALL/FOLD) |
| `is_ip` | Position shapes everything |
| `hero_range_percentile` | Where hero sits in own range |

### Agent allocation per approach

| Role | Per approach | Total (3 approaches) |
|------|-------------|---------------------|
| GTO Expert labellers | 2 agents × 10 hands | 6 agents |
| Challenger (untagged review) | 1 agent | 3 agents |
| **Total per group** | 3 | 9 agents |

Each approach team labels the same 20 hands. Two independent
labellers per approach — their agreement/disagreement is measured.

**Total pilot agent count: 9 agents + 1 comparison programmer = 10**

### Pilot output per hand

Each agent produces:

```json
{
  "situation_id": "BP1_03",
  "vocab_version": 1,

  "hand_bucket": "drawing",
  "action": "RAISE",
  "confidence": "HIGH",
  "difficulty": 2,

  "reasoning": "Free-form reasoning about the hand...",

  "intentions_raw": "I'm raising because I have the nut flush
    draw with the ace of spades blocking villain's nut flush
    combos, and two opponents may fold.",
  "intentions": ["deny_equity", "bluff_fold_better"],
  "proposed_tags": [],

  "street_plan_raw": "Raise flop, if called bet safe turns,
    give up if flush completes and I miss.",
  "street_plan_tags": ["bet_protect_evaluate", "give_up_on_complete"],

  "feature_attention": {
    "flush_draw_rank": "PRIMARY",
    "villain_fold_equity_estimate": "PRIMARY",
    "equity_vs_range": "PRIMARY",
    "villain_draw_pct": "PRIMARY"
  },

  "alternatives_considered": [
    "CALL: rejected — nut draw + blocker meets KB 1.7 raise
    conditions, calling wastes fold equity"
  ]
}
```

### Pilot evaluation criteria

After all 3 approach teams finish, compare:

| Metric | How measured |
|--------|-------------|
| **Inter-rater action agreement** | % of hands where both agents within a team chose the same action |
| **Inter-rater feature agreement** | Jaccard similarity of tagged feature sets between agents on same hand |
| **Cross-approach feature quality** | Which approach tags features the reviewer agrees are relevant? |
| **False positive rate** | Tagged features that a reviewer says didn't matter |
| **False negative rate** | Untagged features that a reviewer says should have been tagged |
| **Removal burden (A only)** | How many Tier 1 removals per hand? Is the justification meaningful or perfunctory? |
| **Flag response quality (B only)** | When flagged on missing Tier 1, do agents add meaningfully or just comply? |
| **Intention consistency** | Same action, same intentions across agents? Or same action, different reasons? |
| **Vocabulary proposals** | How many new tags proposed? How many are genuinely useful vs noise? |
| **Time per hand** | Rough proxy via agent output length — are later hands getting shorter (drift)? |

### Pilot gate

**Owner reviews pilot results before production labelling starts.**

Decisions from pilot:
1. Which feature attention approach (A, B, or C) for production
2. Whether Tier 1 list needs adjustment
3. Whether enriched output is working or needs simplification
4. Whether 10 hands per agent is right or should be 8
5. Whether multi-expert is needed for all hands or only difficulty 2-3
6. Vocabulary: accept/merge/reject proposed tags from pilot

---

# PART 2: PRODUCTION LABELLING PLAN

## 2.1 Prerequisites (must be done before production starts)

| # | Item | Status |
|---|------|--------|
| 1 | Features 49-54 promoted in code | Pending |
| 2 | All 385 situations re-extracted with 54 features | Pending |
| 3 | Labelling prompt updated (bucket-first, enriched output) | Pending |
| 4 | Calibration exam passed (20/24 + GTO reversals) | Pending |
| 5 | Pilot complete, approach selected | Pending |
| 6 | Seed vocabulary finalized (intentions + street plans) | Pending |
| 7 | Tag vocabulary registry created | Pending |

## 2.2 Production structure

### Batch design

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Batch size | 10 hands | Slow, deliberate, researched |
| Independent labellers per hand | 3 | Multi-expert for reliability |
| Challenger per batch | 1 | Reviews untagged features + argues for unchosen action |
| Batches needed | ~37 (385 ÷ 10, rounded) | |
| Batches per session | 2-3 | Each batch: label → compare → resolve |

### Per-batch workflow

```
Step 1: SELECT 10 hands for this batch
  Stratified by: action expectation, street, position,
  difficulty, data source (reconstructed vs new)

Step 2: LABEL — 3 independent GTO Expert agents
  Each agent receives:
  - 10 situation specs (cards, board, action_string, 54 features)
  - KB v1.3
  - Updated labelling prompt (bucket-first + enriched output)
  - Current approved tag vocabulary
  - NO access to other agents' labels

  Each agent produces per hand:
  - hand_bucket, action, confidence, difficulty
  - intentions_raw → intentions (from vocabulary, or propose new)
  - street_plan_raw → street_plan_tags (flop/turn only)
  - feature_attention (PRIMARY tags, Tier 1 check per selected approach)
  - reasoning, alternatives_considered

Step 3: COMPARE — automated report
  Per hand:
  - Action agreement (3/3, 2/3, or 3-way split)
  - Intention agreement (Jaccard on tag sets)
  - Feature attention agreement (Jaccard on tagged features)
  - Flag any 2/3 or 3-way splits

Step 4: CHALLENGE — 1 challenger agent
  Reviews hands where all 3 agents agreed.
  For each: argues the case for the action nobody picked.
  Also reviews untagged Tier 2 features across all 10 hands.

  Reviews hands where 2/3 agreed:
  Reads the dissenting agent's reasoning. Does the dissent
  have merit? Should this go to solver?

Step 5: RESOLVE
  - 3/3 agree + challenger finds no issue → label confirmed
  - 3/3 agree + challenger raises valid point → escalate to
    owner or solver verification
  - 2/3 agree + dissent is weak → majority label confirmed,
    dissent logged
  - 2/3 agree + dissent has merit → solver verification
  - 3-way split → mandatory solver verification + owner review

Step 6: VOCABULARY REVIEW (every 3 batches)
  Review all proposed_tags from last 3 batches.
  Accept, merge, or reject. Update tag_vocabulary.json.
  Increment vocab_version.

Step 7: COMMIT batch results
  - Labels written to batch JSONL
  - Comparison report saved
  - Challenger findings saved
  - All committed to git
```

### Escalation thresholds

| Situation | Action |
|-----------|--------|
| 3/3 agree, challenger quiet | Confirmed. Move on. |
| 3/3 agree, challenger raises valid alternative | Flag for owner. Solver verify if equity is in marginal zone (0.25-0.50). |
| 2/3 agree, dissent is reasoning error | Majority wins. Log dissent for training data. |
| 2/3 agree, dissent is valid alternative | Solver verification. Owner decides. |
| 3-way split | STOP. Solver verification mandatory. Owner reviews all 3 reasonings. |
| >20% of batch is 2/3 or split | Possible prompt issue. Review prompt before next batch. |
| >30% of any batch has proposed new tags | Vocabulary may be incomplete. Review seed list. |

### Solver verification triggers

| Trigger | When |
|---------|------|
| Any 3-way action split | Always |
| 2/3 split where dissent cites range composition | Always |
| CALL↔FOLD disagreement with equity 0.25-0.45 | Always |
| CALL↔RAISE disagreement | Always |
| BET with equity < 0.40 on non-monster | Always |
| Challenger makes strong case for unchosen action | Owner discretion |

### Comparison report format (per hand)

```
situation_id | A1_action | A2_action | A3_action | agree? |
A1_bucket | A2_bucket | A3_bucket | bucket_agree? |
A1_intentions | A2_intentions | A3_intentions |
A1_features | A2_features | A3_features | feature_jaccard |
challenger_finding | escalation | final_label
```

### Vocabulary management

| Event | Action |
|-------|--------|
| Every 3 batches (~30 hands) | Review proposed tags. Accept/merge/reject. |
| After batch 10 (~100 hands) | Major vocabulary review. Prune unused seeds. |
| Zero new tags in 3 consecutive batches | Vocabulary stabilized. Lock for Model 2 training. |
| Tag merged | Migration script updates all prior labels. |
| Tag rejected | Label keeps intentions_raw. No data loss. |

### Seed vocabulary (starting point)

**Intention seeds (6):**

| Tag | Action class | Meaning |
|-----|-------------|---------|
| `value_extract` | BET/RAISE | Worse hands call, you profit |
| `deny_equity` | BET/RAISE | Fold out draws or charge them |
| `bluff_fold_better` | BET/RAISE | You're behind, win only if villain folds |
| `continue_draw` | CALL | Future street equity justifies price |
| `pot_control` | CHECK/CALL | Showdown value, can't handle big pot |
| `range_fold_priced_out` | FOLD | Villain's range puts you too far behind |

Intentionally excluded from seeds (expected to emerge):
`semi_bluff`, `trap`, `thin_value`, `mandatory_defend`,
`build_pot`, `information_bet`

**Street plan seeds (5 action + 5 response):**

Action tags:
- `barrel_value` — betting for value, continue on most runouts
- `bet_protect_evaluate` — deny equity, turn depends on card
- `check_trap` — check strong hand to induce
- `check_pot_control` — check medium hand, manage size
- `draw_continue` — realize equity, reassess next street

Response tags:
- `continue_on_blank` — bet again on safe runouts
- `give_up_on_complete` — check/fold if draws complete
- `check_evaluate` — reassess based on turn card
- `pot_control_check_call` — check, call one bet
- `bet_regardless` — committed to multi-street aggression

Plan format: `["action_tag", "response_tag"]` (flop/turn only)

## 2.3 The labelling prompt

The prompt update (Phase 3A proper) incorporates:

1. **Bucket-first reasoning** — classify hand before considering
   actions. No equity thresholds. Poker reasoning with examples.

2. **Enriched output schema** — intentions, street plans, feature
   attention as structured fields.

3. **Reason-first protocol** — for intentions and street plans:
   write your reason in your own words FIRST, then look at the
   tag vocabulary to find a match. If no match, propose a new tag.

4. **Feature attention protocol** — whichever approach wins the
   pilot (A, B, or C). Tier 1 features enforced. Tier 2 tagged
   from fresh reasoning.

5. **Anti-padding instruction** — "If only one intention tag
   matches your reasoning, use one. A second tag that doesn't
   appear in your reasoning is noise."

6. **54-feature vector** — all features listed with descriptions.
   `hero_range_percentile` explicitly framed as "1.0 = top of
   your range on this board."

7. **Calibration notes** — MW-30 CALL (solver-corrected),
   MW-33 RAISE, MW-50 FOLD.

8. **villain_range_capped** — demoted to preflop structural label
   per KB v1.3 Section 1.9.

## 2.4 Timeline

| Phase | What | Sessions | Hands |
|-------|------|----------|-------|
| 3A | Prompt update + feature promotion | 1 | — |
| 3B | Calibration | 0.5 | — |
| **Pilot** | **20 hands × 3 approaches** | **1** | **20** |
| Pilot gate | Owner reviews, selects approach | — | — |
| Production batches 1-10 | 100 hands (10 × 10) | 4 | 100 |
| Vocab review 1 | After batch 3 | — | — |
| Vocab review 2 | After batch 6 | — | — |
| Vocab review 3 | After batch 10 (major) | — | — |
| Production batches 11-20 | 100 hands | 4 | 100 |
| Production batches 21-37 | 165 hands | 6 | 165 |
| Vocab review 4 | After batch 20 | — | — |
| Final vocab review | After batch 37 | — | — |
| Comparison report (200 reconstructed) | 1 | — |
| Solver verification | Owner in GTO Wizard | 1-2 | ~30-50 hands |
| **Total** | | **~18-20 sessions** | **385** |

## 2.5 Agent count

| Role | Per batch | Batches | Total calls |
|------|-----------|---------|-------------|
| GTO Expert labeller | 3 | 37 | 111 |
| Challenger | 1 | 37 | 37 |
| Comparison (automated) | 1 | 37 | 37 |
| Pilot (3 approaches) | 9 | 1 | 9 |
| Calibration | 2 | 1 | 2 |
| Prompt architect | 1 | 1 | 1 |
| Vocab reviewer | 1 | 5 | 5 |
| **Total** | | | **~202 agent-calls** |

This is more than the original plan (~67 agents) but each call
is smaller (10 hands not 40) and the quality is incomparably
higher. The multi-expert redundancy catches errors that a single
agent + reviewer cannot.

## 2.6 Owner gates

| Gate | When | What |
|------|------|------|
| Gate 5 | After prompt update | Review labelling prompt |
| Pilot gate | After pilot | Select approach, review results |
| Gate 6a | After batch 10 | Review first 100 labels + vocab |
| Gate 6b | After batch 20 | Mid-point review |
| Gate 6c | After batch 37 | Final labels + comparison report |
| Gate 6d | After solver | Solver results integrated |
| Gate 7 | After training | Ship or iterate |

## 2.7 Risk register

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Agents agree on wrong action (groupthink) | Low | Challenger argues for unchosen action on every agreed hand |
| Feature attention is noisy across approaches | Medium | Pilot tests 3 approaches before committing |
| Vocabulary explodes (too many proposed tags) | Low | Review every 3 batches. Merge aggressively. |
| 202 agent-calls is expensive | — | Quality over speed. Each call is 10 hands. Alternative: wrong labels, wrong model, retrain. |
| 18-20 sessions is too slow | — | Owner directive: move slowly, carefully, deliberately. Each batch is self-contained and committed. |
| Pilot approach is inconclusive (no clear winner) | Medium | Default to Approach B (blank slate + check). It has the least bias risk. |
| Late-batch vocabulary drift | Medium | Agents use only approved tags + own proposals. Not other agents' unreviewed proposals. |

## 2.8 What this plan does NOT cover

- Phase 4 (training) — unchanged from PLAN_V2.2_FINAL_COMBINED
- Model 2 (intention prediction) — v2.3, after vocabulary stabilizes
- Sandwich position feature — v2.3
- Teaching system updates — after v2.2 ships

---

**For owner review. Key decisions needed:**

1. Is the pilot scope (20 hands, 3 approaches, 10 agents) right?
2. Is the production pace (10 hands/batch, 3 experts + 1
   challenger) acceptable given the ~18-20 session timeline?
3. Should any difficulty-1 hands get reduced coverage (2 experts
   instead of 3)?
4. Are the seed vocabularies correct starting points?
5. Solver verification budget — ~30-50 hands through GTO Wizard
   over the full production run. Is this feasible?

**On "go" the builder starts Phase 3A (prompt update + feature
promotion), then runs the pilot.**
