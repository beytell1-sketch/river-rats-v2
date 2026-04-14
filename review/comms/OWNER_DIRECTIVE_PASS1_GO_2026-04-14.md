---
date: 2026-04-14
from: Owner (Rupert)
to: Builder team
re: Pass 1 GO — 385 hands, 4+2 teams, feature attention as auxiliary flags
status: DIRECTIVE — start immediately
prerequisites passed:
  - Phase 0 (Gate 1): pipeline hardened
  - Phase 1A (Gate 2): reconstruction tool
  - Phase 1C (Gate 3): feature diff — 200/200 clean
  - Phase 2A (Gate 4): allocation design
  - Phase 2B: 185 factory situations generated
  - Phase 3A (Gate 5): prompt v2 + features 49-54
  - Phase 3B: calibration 20/24 + 3/3 reversals
  - Pilot v1: 6-team structure validated (19/20 unanimous)
  - Pilot v2: CONFIRMED tier + mandatory composition validated
  - Feature attention experiment: Exp 3 (auxiliary flags) confirmed
---

# Pass 1: GO

## What to execute

385 hands. 4 labelling teams + 2 discovery teams. Feature
attention collected using the CONFIRMED tier and mandatory
composition protocol validated in Pilot v2.

## Team structure

### T1-T4: Labelling teams (Approach C amended)

Each team labels all 385 hands independently. No team sees
another team's output. Each team receives the 385 hands in a
different random order (4 seeds).

| Parameter | Value |
|---|---|
| Hands per agent | ≤10 |
| Agents per team | 39 (ceil(385/10)) |
| Teams | 4 |
| Total labelling agent-calls | 156 |

Each agent receives:
- `gto_labeller_v2.md` (bucket-first + enriched output)
- KB v1.3
- Tag vocabulary (tag_vocabulary.json)
- 10 situation specs with full 54-feature vectors + action strings
- Approach C feature attention instructions with CONFIRMED tier
- Mandatory composition for BET/RAISE/CALL/FOLD
- Bucket-specific mandatory features
- NO access to other teams' or agents' labels

Each agent produces per hand:
- hand_bucket, action, confidence, difficulty
- intentions_raw → intentions (1-3 tags, reason-first)
- street_plan_raw → street_plan_tags (flop/turn only)
- feature_attention (PRIMARY + CONFIRMED, mandatory features enforced)
- reasoning, alternatives_considered
- proposed_tags (if any)

### T5-T6: Discovery teams (bottom-up scan)

Run AFTER T1-T4 comparison report is built. They receive the
consensus labels from T1-T4. They do NOT produce new labels.

Each team scans all 385 hands for features that T1-T4 missed.
Bottom-up scan starting from feature 54, working upward.
Excluded features (already covered by T1-T4): equity_vs_range,
villain_top_pair_plus_pct, villain_medium_made_pct,
villain_draw_pct, villain_air_pct, is_ip, hero_range_percentile,
pot_odds.

| Parameter | Value |
|---|---|
| Hands per agent | ≤10 |
| Agents per team | 39 |
| Teams | 2 |
| Total discovery agent-calls | 78 |

Each agent produces per hand:
- discovered_features: {feature_name: "DISCOVERED — reason"}
- Typical output: 2-5 discovered features per hand

## Feature attention → training data

After all 6 teams complete, the union of all tagged features
becomes the binary attention flags:

```
For each hand, for each of the 54 features:
  attn_{feature} = 1 if ANY team tagged it (PRIMARY, CONFIRMED,
                     or DISCOVERED)
  attn_{feature} = 0 if NO team tagged it
```

This produces 54 binary columns added to the training CSV
alongside the 54 original features = 108 total training columns.

The v2.2 model trains on 108 features (Exp 3 mechanism).

## Intentions and street plans

Collected and stored in the labelling JSONL. NOT used for v2.2
model training. Used for:
- Teaching system (intention templates, street plan display)
- v2.3 Model 2 experiment (intention prediction)

## Comparison report (automated)

After T1-T4 complete, build the comparison report per the
Phase 3 Final Plan:

Per hand (385 rows):
- T1 through T4 actions
- Action consensus (UNANIMOUS / STRONG / MAJORITY / SPLIT)
- T1 through T4 difficulty ratings
- Difficulty consensus (CLEAR / LIKELY_CLEAR / STANDARD / HARD / CONTESTED)
- CONFIDENT_SPLIT flag (D1 majority + action split)
- Intention Jaccard (pairwise avg across 4 teams)
- Feature Jaccard (pairwise avg across 4 teams)
- Bucket agreement

Summary statistics:
- % per consensus category
- % per difficulty category
- N CONFIDENT_SPLIT hands
- Average Jaccard scores

## For the 200 reconstructed hands — comparison with old labels

The comparison report also includes, for the 200 reconstructed
situations only:

```
situation_id | old_label | new_consensus_label | agree? |
difficulty_consensus | feature_changes_from_reconstruction
```

Disagreement escalation:
- CALL→RAISE or RAISE→CALL: solver mandatory
- CALL→FOLD with equity >0.30: solver mandatory
- >25% total disagreement: review prompt for over-correction
- ≤15%: high confidence in bucket-first

## Pass 1 gate

After the comparison report is built, present to owner for
review. Owner decides which hands need Pass 2 treatment based
on consensus categories.

## Pass 2 (after Pass 1 gate)

Per the Phase 3 Final Plan:

| Category | Treatment |
|---|---|
| UNANIMOUS + CLEAR | Done |
| UNANIMOUS + STANDARD | 1 challenger |
| STRONG (3/4) | 1 expert reviewer reads all 4 reasonings |
| MAJORITY (3/4 split to 2/4) or worse | Full panel + solver |
| HARD or CONTESTED difficulty | Full panel regardless of action |
| CONFIDENT_SPLIT | Panel + solver mandatory |

Estimated Pass 2: 25-32 agent-calls.

## Vocabulary management

One review after all labelling is complete. No mid-stream
vocabulary changes. After Pass 1 + Pass 2:
- Collect all proposed_tags across all teams
- Merge synonyms, reject noise, accept useful additions
- Apply merges to all labels (simple string replacement)
- Produce final approved vocabulary

## Solver verification

Owner runs flagged hands in GTO Wizard after Pass 2.
Estimated 30-50 hands. Pre-flight: sequences validated,
sizing matches solver options exactly.

## Total agent count

| Role | Agent-calls |
|---|---|
| T1-T4 labelling | 156 |
| T5-T6 discovery | 78 |
| Comparison report | 1 |
| Pass 2 (estimated) | 25-32 |
| Vocabulary review | 1 |
| **Total** | **~261-268** |

## Timeline

| Step | Sessions |
|---|---|
| Pass 1: T1-T4 parallel | 4-5 |
| Pass 1 comparison report | 0.5 |
| Pass 1 gate (owner review) | — |
| Pass 1: T5-T6 discovery | 2 |
| Pass 2: targeted review | 2-3 |
| Solver verification | 1-2 |
| Final assembly + vocab review | 1 |
| **Total** | **~11-13 sessions** |

## Gates remaining

| Gate | When | Decision |
|---|---|---|
| Pass 1 gate | After comparison report | Which hands need Pass 2 |
| Pass 2 gate | After deep review + solver | Approve final labels |
| Gate 6 | After assembly | Approve label set for training |
| Gate 7 | After Phase 4 training | Ship or iterate |

## Pilot v2 labels

The 20 pilot v2 labels are confirmed as production labels.
They are included in the 385 total. T1-T4 relabel them
alongside the other 365 hands — if the production labels
match pilot consensus (expected), the pilot labels stand.
If they differ, flag for review.

## One reminder

Agents see the prompt, the KB, and the hand data. They do
NOT see this plan, the team structure, the comparison framework,
or any other team's output. Independence is the design.

---

**Builder: start T1-T4 immediately. All 4 teams in parallel.
Report when comparison report is ready for Pass 1 gate.**
