---
date: 2026-04-14
from: Builder team (revised per owner directive)
to: Owner (Rupert)
re: Pilot execution plan — 6-team structure + feature attention test on 20 hands
status: FOR OWNER REVIEW
prerequisite: Phase 3B calibration PASSED (20/24, 3/3 reversals)
incorporates: OWNER_DIRECTIVE_PILOT_6TEAM_2026-04-14.md
---

# Pilot Execution Plan (Amended)

## Purpose

Test the full production pipeline on 20 hands before committing
to 385. Six questions to answer:

1. Which feature attention approach (A, B, or C)?
2. Can agents produce reliable enriched output?
3. Does the 6-team consensus structure surface real disagreements?
4. Does the comparison report format work for owner decisions?
5. Does Pass 2 escalation add value?
6. Is 10 hands per agent the right batch size?

## 20 Pilot Hands

10 reconstructed + 10 factory. Pilot labels become production
labels if protocol holds.

### Selection principles

- All 5 action types represented (CHECK, BET, CALL, FOLD, RAISE)
- All 3 streets represented (flop, turn, river)
- Mix of facing-bet and not-facing-bet
- At least 3 difficulty-3 boundary spots
- At least 2-3 hands matching calibration failure patterns
  (MW-12/15 river air over-bet, MW-17 AK overcard equity,
  MW-28 OOP under-bet)
- Both data sources (reconstructed + factory)

### Reconstructed (10)

| # | ID | Street | FB | Expected | Pattern |
|---|-----|--------|-----|----------|---------|
| R1 | d4534_BB_flop | flop | No | CHECK | Monster check (trap?) |
| R2 | d7760_BTN_flop | flop | No | CHECK | Air check — MW-12/15 type |
| R3 | d6384_BTN_turn | turn | No | CHECK | Air turn — MW-12/15 type |
| R4 | d6066_BB_flop | flop | No | BET | Monster value bet |
| R5 | d5046_CO_flop | flop | No | BET | Monster IP bet |
| R6 | d6826_CO_turn | turn | No | BET | Near-nut turn bet |
| R7 | d1971_HJ_river | river | No | BET | Strong river value — MW-28 type (OOP bet) |
| R8 | d2285_BTN_river | river | Yes | FOLD | Air facing river bet |
| R9 | d6533_BTN_river | river | Yes | FOLD | Air facing river bet |
| R10 | d1200_HJ_turn | turn | Yes | FOLD | Weak facing turn bet |

### Factory (10)

| # | ID | Street | FB | Expected | Pattern |
|---|-----|--------|-----|----------|---------|
| F1 | BP1_22 | flop | Yes | CALL | Flush draw facing bet — drawing call |
| F2 | BP2_35 | flop | Yes | RAISE | Set facing bet — value raise |
| F3 | BP3_03 | flop | Yes | FOLD | Air/weak facing bet — range fold |
| F4 | BP4_28 | turn | No | BET | Two pair not facing — value bet |
| F5 | BP5_02 | flop | No | BET | Set not facing — value bet |
| F6 | BP6_01 | flop | Yes | CALL | Monotone FD — drawing call with blocker |
| F7 | BP7_03 | turn | Yes | CALL | Turn draw — MW-17 type (hidden equity) |
| F8 | BP2_36 | turn | Yes | RAISE | Set facing turn bet — value raise |
| F9 | BP2_42 | river | Yes | FOLD | Air facing river — clear fold |
| F10 | BP5_05 | flop | No | BET | Set not facing — value/protection |

### Stratification summary

| Category | Count | Hands |
|----------|-------|-------|
| Not facing — CHECK expected | 3 | R1, R2, R3 |
| Not facing — BET expected | 5 | R4, R5, R6, R7, F4, F5, F10 |
| Facing — CALL expected | 3 | F1, F6, F7 |
| Facing — FOLD expected | 4 | R8, R9, R10, F3, F9 |
| Facing — RAISE expected | 2 | F2, F8 |
| Calibration failure patterns | 4 | R2/R3 (air over-bet), R7 (OOP bet), F7 (hidden equity) |
| Expected difficulty 3 | 3+ | F1, F6, F7 (drawing/marginal spots) |

Note: Some hands appear in multiple categories. F4/F5/F10 are
not-facing BET that could also be CHECK depending on reasoning.

---

## 6-Team Structure

### Team assignment

| Team | Feature attention approach | Random seed |
|------|--------------------------|-------------|
| T1 | A (auto-tag Tier 1, agent removes) | seed 1 |
| T2 | A | seed 2 |
| T3 | B (blank slate + automated check) | seed 3 |
| T4 | B | seed 4 |
| T5 | C (action-dependent auto-tags) | seed 5 |
| T6 | C | seed 6 |

Each team receives the 20 hands in a different random order.
No team sees another team's output.

### Agent allocation

Process Guide §1.1: ≤10 hands per agent.

| Team | Agent 1 | Agent 2 | Total |
|------|---------|---------|-------|
| T1 | 10 hands (batch A) | 10 hands (batch B) | 2 agents |
| T2 | 10 hands (batch A) | 10 hands (batch B) | 2 agents |
| T3 | 10 hands (batch A) | 10 hands (batch B) | 2 agents |
| T4 | 10 hands (batch A) | 10 hands (batch B) | 2 agents |
| T5 | 10 hands (batch A) | 10 hands (batch B) | 2 agents |
| T6 | 10 hands (batch A) | 10 hands (batch B) | 2 agents |

**12 labelling agent-calls** (6 teams × 2 batches).

Each team's batch A and batch B are assigned by the team's
random seed — different teams split the 20 hands differently.

### Approach-specific instructions

**Approach A (Teams T1, T2):** Auto-tag Tier 1, agent removes.

All 8 Tier 1 features start pre-tagged as PRIMARY. Agent reviews
each, can REMOVE with 1-sentence justification. Agent adds
Tier 2 features from scratch.

**Approach B (Teams T3, T4):** Blank slate + automated check.

Agent tags all features from scratch. After tagging, automated
check notes which Tier 1 features the agent did NOT tag. These
are recorded as "misses" — agent is NOT asked to add them (that
would bias the data).

**Approach C (Teams T5, T6):** Action-dependent auto-tags.

Tier 1 defaults vary by chosen action:
- CALL/FOLD: equity_vs_range, pot_odds, villain_top_pair_plus_pct,
  villain_draw_pct, villain_air_pct, villain_medium_made_pct,
  is_ip, hero_range_percentile
- BET/RAISE: equity_vs_range, villain_top_pair_plus_pct,
  villain_draw_pct, villain_air_pct, villain_medium_made_pct,
  is_ip, hero_range_percentile, villain_fold_equity_estimate
  (NOT pot_odds)
- CHECK: equity_vs_range, villain_top_pair_plus_pct,
  villain_draw_pct, villain_air_pct, villain_medium_made_pct,
  is_ip, hero_range_percentile, has_showdown_value

Agent reviews defaults, removes/adds with justification.

### Tier 1 candidate features (all approaches)

| Feature | Rationale |
|---------|-----------|
| `equity_vs_range` | Where hero stands |
| `villain_top_pair_plus_pct` | Range composition — strength |
| `villain_draw_pct` | Range composition — draws |
| `villain_air_pct` | Range composition — weakness |
| `villain_medium_made_pct` | Range composition — thin value |
| `pot_odds` | Price of continuing |
| `is_ip` | Position |
| `hero_range_percentile` | Where hero sits in own range |

---

## Execution Sequence

### Step 1: Prepare situations

Extract full 54-feature situation text for all 20 hands.
Write to `/tmp/pilot_situations.json`.

### Step 2: Launch 6 teams (parallel)

12 labelling agent-calls. Each agent receives:
- v2 labelling prompt (gto_labeller_v2.md)
- KB v1.3
- Approach-specific feature attention instructions (A, B, or C)
- Tag vocabulary seed (tag_vocabulary.json)
- 10 situation texts with full 54-feature vectors
- Randomised hand order per team seed
- NO access to other teams' or agents' labels

### Step 3: Collect all 6 × 20 = 120 label records

Store per-team JSONL. Each record has the full enriched output:
hand_bucket, action, confidence, difficulty, reasoning,
intentions_raw, intentions, street_plan_raw, street_plan_tags,
feature_attention, proposed_tags, alternatives_considered.

### Step 4: Build comparison reports

**Report 1 — 6-team consensus (per hand):**

For each of the 20 hands, compare across all 6 teams:

```
situation_id |
T1_action T2_action T3_action T4_action T5_action T6_action |
action_consensus (UNANIMOUS/STRONG/MAJORITY/SPLIT/FRAGMENTED) |
T1_diff T2_diff T3_diff T4_diff T5_diff T6_diff |
difficulty_consensus (CLEAR/LIKELY_CLEAR/STANDARD/HARD/CONTESTED) |
bucket_agreement |
intention_jaccard (pairwise avg across 6 teams) |
feature_jaccard (pairwise avg across 6 teams) |
CONFIDENT_SPLIT flag (D1 majority + action split)
```

Summary statistics:
- % UNANIMOUS, STRONG, MAJORITY, SPLIT, FRAGMENTED
- % CLEAR, STANDARD, HARD, CONTESTED difficulty
- Number of CONFIDENT_SPLIT hands
- Average intention Jaccard across all hands
- Average feature Jaccard across all hands

**Report 2 — Feature attention comparison (per approach):**

| Metric | A (T1+T2) | B (T3+T4) | C (T5+T6) |
|--------|-----------|-----------|-----------|
| Within-approach action agreement (%) | | | |
| Avg Tier 1 coverage (% of 8 tagged) | | | |
| False positive rate | | | |
| False negative rate (Tier 1 misses) | | | |
| Within-approach feature Jaccard | | | |
| Within-approach intention Jaccard | | | |
| Removal burden (count, A only) | | | |
| Automated miss count (B only) | | | |
| Proposed new tags (count) | | | |
| Quality drift (hands 8-10 vs 1-3) | | | |

**Report 3 — Calibration cross-check:**

For hands R2, R3, R7, F7 (matching calibration failure patterns):
- Did the 6-team consensus get the correct action?
- How many teams matched the calibration failure (BET on air,
  CHECK when should BET, FOLD when should CALL)?
- Did the consensus process catch and correct the error?

### Step 5: Pass 2 dry run (if applicable)

For any hand that is NOT UNANIMOUS on action:

| Consensus | Treatment |
|-----------|-----------|
| STRONG (5/6) | 1 expert reviewer reads all 6 reasonings, assesses dissent |
| MAJORITY (4/6) or worse | 1 full panel agent reads all 6, writes detailed assessment |
| CONFIDENT_SPLIT | Panel agent + flag for solver |

For any hand with HARD or CONTESTED difficulty (regardless of
action consensus):
- 1 panel agent investigates the difficulty disagreement

Agent count for Pass 2 dry run: estimated 2-4 agents depending
on how many hands are non-unanimous.

### Step 6: Write pilot report

Consolidate Reports 1-3 + Pass 2 dry run results into
`review/comms/PILOT_REPORT_2026-04-14.md`.

Present for owner review at Pilot Gate.

---

## Agent Count

| Role | Agent-calls |
|------|-------------|
| 6 teams × 2 batches of 10 | 12 |
| Comparison programmer | 1 |
| Pass 2 dry run (estimated) | 2-4 |
| **Total** | **15-17** |

Note: no separate challenger agents. The 6-team structure
replaces the per-approach challenger — 6 independent opinions
are more powerful than 2 opinions + 1 challenger. If any hand
splits, Pass 2 provides the deep review.

---

## Success Criteria

### 6-team structure works if:

- At least 2-3 hands are non-unanimous (surface real disagreements)
- CONFIDENT_SPLIT flag fires at least once OR all hands are
  genuinely clear (either outcome is informative)
- Comparison report is readable and actionable by owner
- Pass 2 escalation produces useful resolutions on split hands
- Difficulty consensus is meaningful (not all hands rated D1)

### Feature attention approach wins if:

- Within-approach feature Jaccard > 0.5
- False positive rate < 20%
- False negative rate on Tier 1 < 30%
- Clear separation from other approaches on at least 2 metrics

### Protocol works if:

- Overall action agreement across 6 teams > 75% (15/20 hands)
- Enriched output is complete (no missing fields)
- Vocabulary proposals are sparse (< 5 new tags across all teams)
- No quality drift on later hands within batches

### Failure triggers:

- Action agreement < 60% across teams → prompt issue, stop
- Feature Jaccard < 0.3 on all approaches → feature attention
  too subjective, consider simplifying
- All 20 hands UNANIMOUS → 6 teams may be overkill, consider 4
- > 30% proposed new tags → vocabulary incomplete, review seeds
- Calibration failure patterns repeated by 4+ teams → systemic
  prompt gap, fix before production

---

**Awaiting owner review. On "go" the builder executes Steps 1-6.**
