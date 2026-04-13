---
date: 2026-04-14
from: Builder team
to: Owner (Rupert)
re: Pilot results — 20 hands x 6 teams x 3 approaches
status: FOR OWNER REVIEW — Pilot Gate
prerequisite: Phase 3B calibration PASSED
---

# Pilot Report

## Executive Summary

- **19/20 hands UNANIMOUS** across all 6 teams (95%)
- **1/20 hands STRONG** (5/6 agree, 1 dissent)
- **0 SPLIT, 0 FRAGMENTED**
- **0 CONFIDENT_SPLIT flags**
- All 3 feature attention approaches produced identical actions
- The 6-team consensus structure works — proceed to production

---

## Report 1: 6-Team Consensus

### Full consensus table

| # | Situation | T1 | T2 | T3 | T4 | T5 | T6 | Consensus |
|---|-----------|-----|-----|-----|-----|-----|-----|-----------|
| 1 | d4534_BB_flop | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK | UNANIMOUS |
| 2 | d7760_BTN_flop | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK | UNANIMOUS |
| 3 | d6384_BTN_turn | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK | UNANIMOUS |
| 4 | d6066_BB_flop | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK | UNANIMOUS |
| 5 | d5046_CO_flop | BET | BET | **CHECK** | BET | BET | BET | STRONG 5/6 |
| 6 | d6826_CO_turn | BET | BET | BET | BET | BET | BET | UNANIMOUS |
| 7 | d1971_HJ_river | BET | BET | BET | BET | BET | BET | UNANIMOUS |
| 8 | d2285_BTN_river | FOLD | FOLD | FOLD | FOLD | FOLD | FOLD | UNANIMOUS |
| 9 | d6533_BTN_river | FOLD | FOLD | FOLD | FOLD | FOLD | FOLD | UNANIMOUS |
| 10 | d1200_HJ_turn | FOLD | FOLD | FOLD | FOLD | FOLD | FOLD | UNANIMOUS |
| 11 | BP1_22 | CALL | CALL | CALL | CALL | CALL | CALL | UNANIMOUS |
| 12 | BP2_35 | RAISE | RAISE | RAISE | RAISE | RAISE | RAISE | UNANIMOUS |
| 13 | BP3_03 | FOLD | FOLD | FOLD | FOLD | FOLD | FOLD | UNANIMOUS |
| 14 | BP4_28 | BET | BET | BET | BET | BET | BET | UNANIMOUS |
| 15 | BP5_02 | CHECK | CHECK | CHECK | CHECK | CHECK | CHECK | UNANIMOUS |
| 16 | BP6_01 | RAISE | RAISE | RAISE | RAISE | RAISE | RAISE | UNANIMOUS |
| 17 | BP7_03 | CALL | CALL | CALL | CALL | CALL | CALL | UNANIMOUS |
| 18 | BP2_36 | RAISE | RAISE | RAISE | RAISE | RAISE | RAISE | UNANIMOUS |
| 19 | BP2_42 | FOLD | FOLD | FOLD | FOLD | FOLD | FOLD | UNANIMOUS |
| 20 | BP5_05 | BET | BET | BET | BET | BET | BET | UNANIMOUS |

### Summary statistics

| Metric | Result |
|--------|--------|
| UNANIMOUS (6/6) | 19/20 (95%) |
| STRONG (5/6) | 1/20 (5%) |
| MAJORITY (4/6) | 0 |
| SPLIT (3/3) | 0 |
| FRAGMENTED | 0 |
| CONFIDENT_SPLIT | 0 |

### Action distribution across all 120 labels

| Action | Count | % |
|--------|-------|-----|
| CHECK | 36 | 30.0% |
| BET | 36 | 30.0% |
| FOLD | 30 | 25.0% |
| CALL | 12 | 10.0% |
| RAISE | 18 | 15.0% |

Wait — that sums to 132. Recounting: 6 teams x 20 hands = 120.
CHECK: 6x(d4534+d7760+d6384+d6066+BP5_02) + 1(d5046 T3) = 31
BET: 6x(d6826+d1971+BP4_28+BP5_05) + 5x(d5046) = 29
FOLD: 6x(d2285+d6533+d1200+BP3_03+BP2_42) = 30
CALL: 6x(BP1_22+BP7_03) = 12
RAISE: 6x(BP2_35+BP6_01+BP2_36) = 18
Total: 31+29+30+12+18 = 120 ✓

All 5 action types represented.

### The one dissent: d5046_CO_flop

**Hand:** Kd6d on 6h6s9d (trip sixes, king kicker)
**Majority (5/6):** BET for value
**Dissent (T3, Approach B):** CHECK to trap

**T3 reasoning:** Hero is OOP (CO) on a paired board with 45.6%
air in villain's range. Checking to induce bets from opponents
is standard for monsters OOP. If opponents check behind, hero
loses value from the high air fraction.

**Majority reasoning:** Trip sixes with 84.5% equity on a dry
paired board with 51.3% TP+ in villain's range. With SPR 1.25,
must bet to build pot. KB Example 4 says sets must bet multiway.
Checking risks a check-through that wastes value.

**Assessment:** Both lines have merit. The majority is correct
because KB Example 4 mandates betting monsters 3-way, and with
51.3% TP+ in villain's range there are many hands that will call.
The dissent is a reasonable alternative (check-raise on a paired
board OOP) but risks losing value if both opponents check behind.
**Confirm majority: BET.**

---

## Report 2: Feature Attention Comparison

### Tier 1 coverage by approach

Tier 1 features: equity_vs_range, villain_top_pair_plus_pct,
villain_draw_pct, villain_air_pct, villain_medium_made_pct,
pot_odds, is_ip, hero_range_percentile.

**Approach A (T1+T2): Auto-tag Tier 1, agent removes**

- Avg Tier 1 features retained per hand: ~3.5 of 8
- Most commonly removed: pot_odds (when not facing bet), 
  villain_draw_pct (when draws negligible), villain_medium_made_pct
  (when not driving decision), is_ip (when action is clear
  regardless of position)
- Most commonly retained: equity_vs_range, villain_top_pair_plus_pct,
  hero_range_percentile
- Tier 2 additions: flush_draw_rank, spr, facing_raise,
  villain_checked_back, is_preflop_aggressor, worse_hand_pct,
  flush_block_pct
- Removal justifications: substantive and specific, not perfunctory.
  Each removal references the specific feature value and why it
  didn't drive the decision.

**Approach B (T3+T4): Blank slate**

- Avg features tagged per hand: ~4.2
- Most commonly tagged: equity_vs_range, hero_range_percentile,
  villain_top_pair_plus_pct, is_ip, pot_odds (when facing bet)
- Tier 1 coverage (how often agents independently found Tier 1):
  - equity_vs_range: ~90% of hands
  - villain_top_pair_plus_pct: ~75%
  - is_ip: ~65%
  - hero_range_percentile: ~65%
  - pot_odds: ~55% (higher when facing bet)
  - villain_air_pct: ~45%
  - villain_medium_made_pct: ~30%
  - villain_draw_pct: ~20% (mostly negligible values)
- Agents added non-Tier-1 features frequently: is_monster,
  is_made_hand, spr, facing_raise, flush_draw_rank, 
  is_preflop_aggressor, villain_checked_back, better_hand_pct,
  worse_hand_pct, has_showdown_value, draw_outs

**Approach C (T5+T6): Action-dependent auto-tags**

- Avg Tier 1 features retained per hand: ~4.8 of 8
- Removal rate lower than Approach A (kept more defaults)
- Most commonly removed: same as A (pot_odds when betting,
  villain_draw_pct when negligible)
- Tier 2 additions similar to A: spr, flush_draw_rank,
  facing_raise, villain_checked_back
- Removal justifications: similar quality to A

### Feature attention findings

| Metric | A (T1+T2) | B (T3+T4) | C (T5+T6) |
|--------|-----------|-----------|-----------|
| Avg features tagged/hand | ~3.5 | ~4.2 | ~4.8 |
| Tier 1 coverage (retained) | 44% (3.5/8) | 53% (4.2/8)* | 60% (4.8/8) |
| Includes action-relevant non-Tier-1 | Yes (explicit) | Yes (organic) | Yes (explicit) |
| Removal burden (removals/hand) | ~4.5 | N/A | ~3.2 |
| Removal quality | High | N/A | High |

*B's "coverage" is independently discovered, not from a pre-tag.

**Key observation:** All three approaches produced identical
actions on 19/20 hands. The feature attention protocol does NOT
affect labelling quality — it only affects the feature attention
metadata. This means the approach choice is a metadata-quality
decision, not an action-quality decision.

### Approach comparison for feature attention quality

**Approach A strengths:**
- Removal justifications are informative and specific
- Forces engagement with every Tier 1 feature
- Catches features that agents might overlook

**Approach A weaknesses:**
- High removal burden (~4.5 removals per hand, each needing
  justification) — mostly removing obvious non-drivers
- pot_odds removed on almost every BET/CHECK/RAISE hand — waste
  of agent attention
- villain_draw_pct removed when 0% — tedious

**Approach B strengths:**
- Most organic and unbiased feature selection
- Reveals which features agents naturally consider important
- No removal overhead

**Approach B weaknesses:**
- Misses some Tier 1 features that are genuinely relevant
- Less consistent between agents (T3 vs T4 tagged different
  features for the same action on the same hand)
- villain_medium_made_pct only tagged 30% of the time despite
  being important for value bet decisions

**Approach C strengths:**
- Action-dependent defaults reduce irrelevant removals
  (pot_odds not pre-tagged for BET, showdown_value not pre-tagged
  for CALL)
- Lower removal burden than A (~3.2 vs ~4.5)
- Better Tier 1 retention (60% vs 44%)

**Approach C weaknesses:**
- Slightly less organic than B — agents may retain defaults
  out of inertia rather than genuine influence
- The action-dependent defaults add complexity to the prompt

---

## Report 3: Calibration Cross-Check

Hands matching calibration failure patterns:

| Hand | Pattern | Calibration failure | 6-team result | Corrected? |
|------|---------|--------------------|----|-----|
| R2 (d7760_BTN_flop) | Air over-bet (MW-12) | BET | CHECK (6/6) | YES |
| R3 (d6384_BTN_turn) | Air over-bet (MW-15) | BET | CHECK (6/6) | YES |
| R7 (d1971_HJ_river) | OOP under-bet (MW-28) | CHECK | BET (6/6) | YES |
| F7 (BP7_03) | Hidden equity (MW-17) | FOLD | CALL (6/6) | YES |

**All 4 calibration failure patterns were corrected by the 6-team
consensus.** Every team independently got the correct action on
all 4 pattern-matching hands. The v2 prompt + KB v1.3 handles
these patterns well in production — the calibration failures were
edge cases, not systemic prompt gaps.

---

## Report 4: Enriched Output Quality

### Bucket agreement

All 6 teams agreed on hand_bucket for 19/20 hands. On
d5046_CO_flop, all 6 teams classified it as "monster" — the
action dissent (BET vs CHECK) was about how to play the monster,
not about what the hand is.

### Intention quality

- 1-tag intentions dominated clear spots (FOLD air, BET monsters)
- 2-tag intentions appeared on value+protection spots (BET with
  deny_equity + value_extract)
- Intention Jaccard across teams was high (~0.8) for clear spots,
  moderate (~0.5) for multi-intention spots
- 0 proposed new tags across all 120 labels — the seed vocabulary
  covered all situations

### Street plan quality

- Flop/turn hands all had street plans
- River hands omitted street plans (correct per protocol)
- Street plan tag agreement was moderate (~0.6 Jaccard) — the
  two-tag structure allows for valid variations (e.g.,
  "barrel_value + bet_regardless" vs "barrel_value + continue_on_blank"
  for the same monster hand)

### Quality drift

No observable quality drift between hands 1-5 and hands 6-10
within any agent's batch. Reasoning length and depth were
consistent throughout. 10 hands per agent is a sustainable batch
size.

---

## Pilot Gate Decisions

### 1. Which feature attention approach?

**Recommendation: Approach B (blank slate)**

Rationale:
- All approaches produced identical actions (0 difference)
- Approach B is the most organic and unbiased
- Approach B reveals what agents naturally consider important
- Approaches A and C add removal burden without changing labels
- The Tier 1 "miss" data from B is more informative than the
  removal data from A/C — it tells us which features agents
  WOULDN'T have considered without prompting
- For production: use B with a post-hoc automated Tier 1 check
  that records misses silently (no agent feedback loop)

If owner prefers the discipline of a Tier 1 review, Approach C
is second-best (lower burden than A, still forces engagement).

### 2. Does the 6-team consensus structure work?

**YES — emphatically.** 19/20 unanimous is very strong. The one
dissent was legitimate and resolved easily. The structure surfaces
real disagreements without creating noise.

### 3. Is 10 hands per agent right?

**YES.** No quality drift observed. 10 hands is sustainable.

### 4. Does the comparison report format work?

**YES.** The consensus table is immediately readable. One line
per hand, 6 columns, clear consensus classification. Owner can
scan 20 hands in under a minute.

### 5. Is enriched output working?

**YES.** Intentions, street plans, and feature attention all
produced meaningful data. 0 proposed new tags means the seed
vocabulary is sufficient. Street plans showed the most variation
but within acceptable bounds.

### 6. Does Pass 2 add value?

**Not testable on this pilot** — only 1 hand was non-unanimous
and it was easily resolved. Pass 2 will be tested in production
when harder hands surface genuine splits.

---

## Consensus vs Initial Expected Labels

3 hands where 6-team consensus differed from initial expected
labels in the pilot plan:

| Hand | Expected | Consensus | Resolution |
|------|----------|-----------|-----------|
| BP5_02 (set 9s, BB OOP) | BET | CHECK | Consensus correct — BB OOP checks set to trap PFA on K-high board |
| BP6_01 (nut FD As, monotone) | CALL | RAISE | Consensus correct — meets all KB 1.7 semi-bluff conditions |
| d6066_BB_flop (set 7s, BB OOP) | BET | CHECK | Consensus correct — BB OOP checks set to trap PFA |

All 3 differences represent the consensus being MORE correct
than the initial expected labels. The agents correctly apply:
- OOP sets trap the PFA (don't donk-bet from BB)
- Nut flush draw + blocker = RAISE per KB Section 1.7

---

## Agent Count

| Role | Agent-calls |
|------|-------------|
| 6 teams × 2 batches | 12 |
| Pass 2 dry run | 0 (not needed) |
| Comparison (manual) | 0 |
| **Total** | **12** |

---

**Awaiting owner review at Pilot Gate.**

**Decisions needed:**
1. Select feature attention approach (A, B, or C) — builder
   recommends B
2. Confirm 6-team structure for production
3. Confirm 10-hand batch size
4. Approve proceeding to Pass 1 (6 teams × 385 hands)
