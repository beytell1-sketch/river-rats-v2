---
date: 2026-04-13
from: Owner (Rupert)
to: Builder team
re: Phase 3 labelling — owner directive on agent allocation and difficulty classification
status: DIRECTIVE — incorporate into the Phase 3 plan
---

# Owner Directive: Phase 3 Labelling

## Principles

1. Tokens are not a constraint. Quality is.
2. Every hand is seen by multiple independent experts.
3. Difficulty classification is too important for one pass.
4. Disagreements are the signal — review them slowly and carefully.
5. Move deliberately. No rushing through batches.

## Structure: Two full independent passes + expert review

### Pass 1 — Full labelling (all 385 hands)

**6 independent GTO Expert teams.** Each team labels the same
385 hands. No team sees another team's output.

| Parameter | Value |
|---|---|
| Hands per agent | ≤10 |
| Agents per team | ~39 (385 ÷ 10) |
| Teams | 6 |
| Total agent-calls (Pass 1) | ~234 |

Each agent produces the full enriched output:
- hand_bucket, action, confidence, difficulty (1/2/3)
- intentions_raw → intentions
- street_plan_raw → street_plan_tags (flop/turn)
- feature_attention (PRIMARY only)
- reasoning, alternatives_considered

**Why 6 teams, not 3:** With 3 teams, a 2/1 split could be
noise (one agent had a bad take). With 6 teams, a 5/1 split
is a strong signal that the 1 is wrong. A 4/2 split is a
genuine disagreement worth investigating. A 3/3 split is a
truly hard hand. The resolution granularity is much finer.

### Pass 1 output — per-hand consensus report

For each of the 385 hands, automated comparison across 6 teams:

```
situation_id | T1_action | T2_action | T3_action | T4_action | T5_action | T6_action |
action_consensus | difficulty_consensus |
T1_bucket | T2_bucket | ... | bucket_consensus |
intention_jaccard | feature_jaccard |
disagreement_type | escalation_level
```

**Difficulty consensus:** Each team assigned difficulty 1/2/3.
Take the distribution:

| Difficulty votes | Classification | What it means |
|---|---|---|
| 6/6 say D1 | CLEAR | Unanimous easy. All experts agree this is obvious. |
| 5/6 say D1 | LIKELY CLEAR | One expert saw something others didn't. Worth a glance. |
| 4+ say D2 | STANDARD | Factor conflict but resolvable. |
| Any 3+ say D3 | HARD | Multiple experts think this is a boundary hand. |
| No majority | CONTESTED | Experts can't even agree on how hard it is. Treat as HARD. |

**Action consensus:**

| Agreement | Classification | Next step |
|---|---|---|
| 6/6 agree | UNANIMOUS | Confirmed. No second pass needed unless difficulty is CONTESTED. |
| 5/6 agree | STRONG | Examine the dissent. If reasoning is weak, majority wins. If reasoning has merit, escalate. |
| 4/6 agree | MAJORITY | Expert review of all 6 reasonings. Solver verification if equity is in marginal zone. |
| 3/3 split | SPLIT | Mandatory solver verification. Owner reviews all reasonings. |
| No majority | FRAGMENTED | Mandatory solver verification. Owner reviews. Possible prompt issue for this hand type. |

### Pass 2 — Difficulty-targeted deep review

**Only hands that need it.** Based on Pass 1 results:

| Category | Expected % | What happens |
|---|---|---|
| UNANIMOUS action + CLEAR difficulty | ~30-40% | Done. Label confirmed. |
| UNANIMOUS action + STANDARD difficulty | ~20-25% | 1 challenger agent reviews. Argues for unchosen action. If challenger finds nothing, confirmed. |
| STRONG (5/6) any difficulty | ~15-20% | Expert reviewer examines the dissent in detail. Reads all 6 reasonings. Writes finding. |
| MAJORITY (4/6) or worse | ~10-15% | Full expert panel: 1 GTO Expert reads all 6 reasonings + the hand context. Writes a detailed assessment. Solver verification triggered. |
| HARD or CONTESTED difficulty | ~15-20% | Full expert panel regardless of action consensus. These hands are where the model learns the most. |

**Pass 2 agent allocation (estimated):**

| Role | Hands | Agents |
|---|---|---|
| Challenger (unanimous + standard) | ~85-95 | ~9-10 |
| Expert reviewer (5/6 strong) | ~60-75 | ~6-8 |
| Full expert panel (4/6 or worse) | ~40-60 | ~4-6 |
| Full expert panel (hard/contested difficulty) | ~60-75 | ~6-8 |
| **Pass 2 total** | | **~25-32** |

Note: overlap between categories (a hand can be both 4/6 and
HARD). Deduplicate — a hand gets the highest treatment it
qualifies for, not multiple reviews.

### Difficulty disagreement — special handling

When the 6 teams disagree on difficulty itself, that's a
separate finding worth investigating:

| Difficulty pattern | What it means | Action |
|---|---|---|
| 3 say D1, 3 say D3 | Half the experts think it's obvious, half think it's a coin flip. The hand is teaching something about what makes spots hard. | Expert panel writes up: WHY did 3 agents think this was easy? What did the other 3 see that made it hard? |
| Most say D1, action split | Experts think it's easy but disagree on the answer. This is the most dangerous pattern — confident and wrong. | Mandatory solver verification. These hands expose prompt bias. |
| Most say D3, action unanimous | Hard hand but everyone agrees. These are the best training examples — the model needs to learn nuance here. | Confirm with challenger. These hands get extra weight in teaching. |

### Expert review protocol (Pass 2)

Expert reviewers and panel members are NOT additional labellers.
They don't produce a new label. They produce an ASSESSMENT:

```
For this hand, I have read all 6 expert reasonings.

Action consensus: [X/6 agree on ACTION]
My assessment: [CONFIRM majority / CONFIRM minority / INCONCLUSIVE]

Key reasoning differences:
- Teams 1,2,3,5,6 chose CALL because [summary]
- Team 4 chose FOLD because [summary]

The disagreement is about: [what specifically]
My judgment: [which reasoning is stronger and why]

Recommendation: [confirm CALL / escalate to solver / flag for owner]
```

Slow. Careful. Reading all the evidence before judging.

## Total agent allocation

| Phase | Agent-calls |
|---|---|
| Pass 1: 6 teams × ~39 agents | ~234 |
| Pass 2: challengers + reviewers + panels | ~25-32 |
| Pilot (unchanged from builder plan) | 10 |
| Calibration | 2 |
| Prompt architect | 1 |
| Comparison report automation | 1 |
| Vocabulary review (after all labelling) | 1 |
| **Total** | **~275-280** |

## Timeline

| Phase | Sessions |
|---|---|
| Phase 3A: prompt + feature promotion | 1 |
| Phase 3B: calibration | 0.5 |
| Pilot (20 hands × 3 approaches) | 1 |
| Pilot gate | — |
| Pass 1: 6 teams labelling in parallel | 4-5 |
| Pass 1 comparison report | 0.5 |
| Pass 1 gate: owner reviews consensus | — |
| Pass 2: targeted deep review | 2-3 |
| Pass 2 gate: owner reviews findings | — |
| Solver verification | 1-2 |
| Final label set assembly | 0.5 |
| Vocabulary review (one-time, after all labels) | 0.5 |
| **Total Phase 3** | **~11-14 sessions** |

## What this changes from the builder's plan

| Builder plan | This directive |
|---|---|
| 3 experts per batch, all hands equal | 6 teams full pass, then targeted deep review |
| Challenger on every batch | Challenger only where needed (unanimous + standard) |
| Vocabulary review every 3 batches | One vocabulary review after all labelling |
| 202 agent-calls, 18-20 sessions | ~275 agent-calls, 11-14 sessions |
| Sequential batches | Pass 1 teams run in parallel |

More agents, fewer sessions. The parallelism of 6 independent
teams is faster than sequential batches of 10 hands each.

## What this does NOT change

- Pilot plan (unchanged — still 20 hands, 3 approaches, 10 agents)
- Features 49-54 promotion (unchanged)
- Enriched output schema (unchanged)
- Seed vocabularies (unchanged)
- Solver verification triggers (unchanged)
- Phase 4 training plan (unchanged)

## Vocabulary management — simplified

No tag registry. No vocab versions. No migration scripts.

1. Pilot produces initial tags.
2. Owner reviews pilot tags. Approves a list.
3. Pass 1 agents use the approved list + propose new tags.
4. After ALL of Pass 1, one vocabulary review:
   - How many unique tags emerged?
   - Which are genuinely distinct vs synonyms?
   - Merge synonyms, reject noise, accept useful additions.
   - Produce the final approved vocabulary.
5. If Model 2 is built in v2.3, the final vocabulary is the
   training target.

No mid-labelling vocabulary changes. No version numbers. No
migration scripts. Simple.

---

**Builder: incorporate this directive into the Phase 3 plan.
Keep the pilot unchanged. Restructure production labelling
as two passes (6-team full pass + targeted deep review).
Simplify vocabulary management. Send back for review.**
