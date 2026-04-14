---
date: 2026-04-14
from: Owner (Rupert)
to: Builder team
re: Pilot Gate v2 — amended structure, CONFIRMED tier, mandatory composition, discovery teams, rerun
status: DIRECTIVE — supersedes PILOT_GATE_APPROVAL_2026-04-14.md
---

# Pilot Gate v2: Final Structure + Rerun

## Decisions

1. **Feature attention: Approach C (amended) + discovery teams**
2. **6-team structure: CONFIRMED** — 4 labelling + 2 discovery
3. **10-hand batch size: CONFIRMED**
4. **Mandatory composition: expanded** — BET, RAISE, CALL, and
   FOLD (any action facing or placing chips)
5. **CONFIRMED tier: added**
6. **Rerun pilot before production**

---

## The Structure: Two Roles, One Union

### Role 1: Labelling Teams (T1-T4) — Approach C amended

4 independent teams. Each labels all 385 hands (production) or
all 20 hands (pilot rerun). No team sees another's output.

These teams produce:
- The label (bucket, action, intentions, street plan, reasoning)
- Feature attention with CONFIRMED tier
- Mandatory features per action type and hand bucket

### Role 2: Discovery Teams (T5-T6) — Bottom-up outlier scan

2 independent teams. They run AFTER the T1-T4 comparison report
is built. They receive the consensus label per hand. They do NOT
produce a new label.

Their job: find features that T1-T4 missed.

**Discovery agent prompt:**

```
You are a FEATURE DISCOVERY agent. Your job is different from
the standard labelling agents.

You receive:
- The hand data (cards, board, 54-feature vector, action string)
- The consensus label (action, bucket, intentions) from 4
  independent labelling teams

Your job is NOT to relabel. The action is decided. Your job is
to find features that matter for THIS specific hand that the
standard labelling teams may have missed.

SCAN PROTOCOL:
1. Start from feature 54 and work UPWARD to feature 1.
2. For each feature, look at its SPECIFIC VALUE for this hand.
3. Ask: "Given that the action is [consensus action] with
   bucket [consensus bucket], does this feature's value matter
   in a way that the obvious features (equity, position,
   composition) don't capture?"
4. If yes: tag as DISCOVERED with a one-sentence explanation
   of why this feature matters for THIS hand specifically.
5. If no: skip.

DO NOT tag these features (already covered by labelling teams):
- equity_vs_range
- villain_top_pair_plus_pct, villain_medium_made_pct,
  villain_draw_pct, villain_air_pct
- is_ip
- hero_range_percentile
- pot_odds

YOU ARE LOOKING FOR:
- Board texture features that interact with this specific hand
  (connectivity_score when hero has a straight draw,
  flush_danger when hero has the nut flush draw)
- Action history that changes the range story
  (villain_checked_back on a player who is usually aggressive,
  villain_aggression_count = 2 meaning multi-street pressure)
- Hand-specific features the standard view misses
  (overcard_outs on unpaired AK, improvement_probability on
  a turn draw, flush_draw_rank distinguishing nut vs weak
  flush draw, flush_block_pct on a semi-bluff raise hand)
- SPR when it creates commitment or stack-off thresholds
- is_preflop_aggressor affecting c-bet logic
- has_showdown_value on check/fold boundary hands
- is_3bet_pot changing range assumptions

Typical output: 2-5 discovered features per hand. Some hands
will have 0 (the obvious features told the whole story). Some
will have 5+ (complex, multi-factor hand).
```

**Discovery output per hand:**

```json
{
  "situation_id": "BP7_03",
  "consensus_action": "CALL",
  "consensus_bucket": "drawing",
  "discovered_features": {
    "improvement_probability": "DISCOVERED — 0.32 means hero
      improves ~1 in 3 rivers. Combined with pot odds this
      justifies the call even without implied odds.",
    "flush_draw_rank": "DISCOVERED — rank 14 (ace) means hero
      has the NUT flush draw, not just any flush draw. Changes
      implied odds significantly.",
    "villain_checked_back": "DISCOVERED — villain checked flop,
      suggesting a capped range. Turn bet is more likely a
      delayed c-bet than a strong hand."
  }
}
```

### The Union

Final feature attention per hand = union of:
- T1 tags (PRIMARY + CONFIRMED)
- T2 tags (PRIMARY + CONFIRMED)
- T3 tags (PRIMARY + CONFIRMED)
- T4 tags (PRIMARY + CONFIRMED)
- T5 discovered features
- T6 discovered features

Any feature tagged by ANY team at ANY level enters the final
set. The level is preserved (PRIMARY > CONFIRMED > DISCOVERED).
If T1 tags `equity_vs_range` as PRIMARY and T3 tags it as
CONFIRMED, the final level is PRIMARY.

---

## Mandatory Feature Requirements

### By action type (any action involving chips)

For BET, RAISE, CALL, and FOLD: agent MUST tag all 4 villain
composition features as PRIMARY or CONFIRMED.

```
villain_top_pair_plus_pct
villain_medium_made_pct
villain_draw_pct
villain_air_pct
```

**Prompt language:**

```
For BET, RAISE, CALL, and FOLD: you MUST tag all 4 villain
composition features as PRIMARY or CONFIRMED.

- BET/RAISE: you are betting INTO this range. Know what it
  contains.
- CALL: you are calling AGAINST this range. Know how much
  of it you beat.
- FOLD: you are folding AGAINST this range. Confirm you are
  really behind enough to give up.

Only CHECK when not facing a bet is exempt from mandatory
composition.
```

### By hand bucket

After classifying the hand in Step 1, the agent MUST tag these
bucket-specific features as PRIMARY or CONFIRMED:

| Bucket | Must tag | Why |
|---|---|---|
| **Drawing** | `draw_outs`, `improvement_probability`. If flush draw: also `flush_draw_rank`, `flush_block_pct`. | These define what the draw IS. A draw decision without considering outs and improvement is incomplete. |
| **Air** | `overcard_outs`, `has_showdown_value`, `villain_fold_equity_estimate` | Air lives on fold equity and overcard improvement. These determine bluff, check, or fold. |
| **Medium made** | `has_showdown_value`, `danger_score`, `hero_range_percentile` | Medium hands are about showdown viability and range position. |
| **Monster** | `spr` | Stack-to-pot determines pot-building vs trapping. |
| **Weak made** | `has_showdown_value`, `better_hand_pct`. If facing bet: `pot_odds`. | Weak hands are about "worth showing down?" and "priced in?" |
| **Strong made** | `danger_score` | Strong hands care about board safety — static vs dynamic. |

**Prompt language:**

```
After classifying the hand bucket, you MUST tag these features
for your bucket as PRIMARY or CONFIRMED:

Drawing: draw_outs, improvement_probability
  + if flush draw: flush_draw_rank, flush_block_pct
Air: overcard_outs, has_showdown_value, villain_fold_equity_estimate
Medium made: has_showdown_value, danger_score, hero_range_percentile
Monster: spr
Weak made: has_showdown_value, better_hand_pct
  + if facing bet: pot_odds
Strong made: danger_score

These features define what your hand type IS. A drawing hand
decision that doesn't consider improvement_probability is
incomplete reasoning.
```

---

## CONFIRMED Tier Definition

| Level | Definition | Use |
|---|---|---|
| **PRIMARY** | Without this feature's value, the action might change. | The feature drove the decision. |
| **CONFIRMED** | Checked this feature, its current value supports the action. If it were very different, the action might change. | Verified as part of reasoning. Value aligns with action. |
| **DISCOVERED** | Found by discovery team. Not tagged by labelling teams but relevant to this specific hand. | Bottom-up scan caught something the top-down view missed. |

---

## Pilot Rerun Design

### Step 1: T1-T4 label 20 hands (parallel)

4 labelling teams, Approach C amended. Each team: 2 agents ×
10 hands = 8 agent-calls. Different random order per team.

Full enriched output including:
- Mandatory composition (BET/RAISE/CALL/FOLD)
- Bucket-specific mandatory features
- CONFIRMED tier
- All other enriched fields (intentions, street plan, etc.)

### Step 2: Build T1-T4 comparison report

Per hand: 4-team action consensus, difficulty consensus, feature
Jaccard, intention Jaccard.

### Step 3: T5-T6 discovery scan (parallel)

2 discovery teams receive: 20 hands + T1-T4 consensus labels.
Each team: 2 agents × 10 hands = 4 agent-calls.

Bottom-up feature scan per the discovery prompt above.

### Step 4: Build union + final report

Per hand, the report includes:

```
situation_id | consensus_action | consensus_bucket |
difficulty_consensus |

T1_tags: {feature: level, ...}
T2_tags: {feature: level, ...}
T3_tags: {feature: level, ...}
T4_tags: {feature: level, ...}
T5_discovered: {feature: reason, ...}
T6_discovered: {feature: reason, ...}

UNION (final): {feature: highest_level, ...}

UNTAGGED features (not tagged by any team):
  feature_name: value — [NOT TAGGED BY ANY TEAM]
  feature_name: value — [NOT TAGGED BY ANY TEAM]
  ...
```

**The UNTAGGED list is critical.** For every hand, show ALL
54 features that were not tagged by ANY of the 6 teams. Include
the feature's actual value for this hand. This lets the owner
scan for: "wait, `connectivity_score` is 8 on a hand with a
straight draw and nobody tagged it?"

### Agent count for rerun

| Role | Agent-calls |
|---|---|
| T1-T4: 4 teams × 2 batches of 10 | 8 |
| T5-T6: 2 teams × 2 batches of 10 | 4 |
| Comparison + union builder | 1 |
| **Total** | **13** |

### Rerun evaluation

| Metric | Target |
|---|---|
| Action agreement (T1-T4) | ≥ 95% (match pilot 1) |
| Composition coverage on BET/RAISE/CALL/FOLD | 100% (all 4 tagged) |
| Bucket-specific coverage | 100% (required features tagged) |
| CONFIRMED tags per hand | 2-5 average |
| Discovery features per hand | 1-4 average |
| Untagged features per hand | Reviewed by owner — any misses? |
| Feature Jaccard (T1-T4) | Higher than pilot 1 |
| No action regressions from pilot 1 | Labels match pilot 1 consensus |

### If rerun confirms

Proceed directly to Pass 1 production. The rerun labels become
the production labels for these 20 hands. No additional gate.

### If rerun shows problems

- CONFIRMED is noisy → simplify to PRIMARY-only, keep mandatory
  requirements
- Discovery teams find nothing useful → drop to 4 teams, accept
  some feature blind spots
- Mandatory requirements change labels → investigate, this means
  forced range-thinking revealed something
- Untagged list reveals systematic gaps → add to mandatory
  requirements or discovery prompt

---

## Changes from Pilot Gate v1

| v1 | v2 |
|---|---|
| All 6 teams use Approach C | 4 labelling (C) + 2 discovery (bottom-up) |
| Mandatory composition: BET/RAISE only | Mandatory composition: BET/RAISE/CALL/FOLD |
| No bucket-specific requirements | Bucket-specific mandatory features |
| No discovery scan | Bottom-up discovery after consensus |
| No untagged feature list | Full untagged list per hand for owner review |
| 6 teams parallel | T1-T4 parallel, then T5-T6 after consensus |

---

**Builder: update the v2 prompt with mandatory composition
(expanded to CALL/FOLD), bucket-specific requirements, and
CONFIRMED tier. Build the discovery agent prompt. Rerun the
pilot on the same 20 hands. Include the full untagged feature
list per hand in the report. Fresh agents only.**
