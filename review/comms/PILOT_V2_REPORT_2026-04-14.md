---
date: 2026-04-14
from: Builder team
to: Owner (Rupert)
re: Pilot v2 rerun results — 4 labelling teams + 2 discovery teams
status: FOR OWNER REVIEW — proceed to Pass 1?
prerequisite: PILOT_GATE_APPROVAL_V2_2026-04-14.md
---

# Pilot v2 Rerun Report

## Executive Summary

- **18/20 hands UNANIMOUS** across 4 labelling teams (90%)
- **2/20 hands STRONG** (3/4 agree, 1 dissent)
- **20/20 labels match pilot v1 consensus** — zero regressions
- Mandatory composition and CONFIRMED tier working as designed
- Discovery teams found 2-6 features per hand beyond standard tags
- Average: 17.6 features tagged per hand (union of all 6 teams)
- Average: 36.4 features UNTAGGED per hand (for owner scan)

---

## Report 1: T1-T4 Action Consensus

| Hand | T1 | T2 | T3 | T4 | Consensus |
|------|-----|-----|-----|-----|-----------|
| d4534_BB_flop | CHECK | CHECK | CHECK | CHECK | UNANIMOUS |
| d7760_BTN_flop | CHECK | CHECK | CHECK | CHECK | UNANIMOUS |
| d6384_BTN_turn | CHECK | CHECK | CHECK | CHECK | UNANIMOUS |
| d6066_BB_flop | CHECK | CHECK | CHECK | CHECK | UNANIMOUS |
| d5046_CO_flop | **CHECK** | BET | BET | BET | STRONG 3/4 |
| d6826_CO_turn | BET | BET | BET | BET | UNANIMOUS |
| d1971_HJ_river | BET | BET | BET | BET | UNANIMOUS |
| d2285_BTN_river | FOLD | FOLD | FOLD | FOLD | UNANIMOUS |
| d6533_BTN_river | FOLD | FOLD | FOLD | FOLD | UNANIMOUS |
| d1200_HJ_turn | FOLD | FOLD | FOLD | FOLD | UNANIMOUS |
| BP1_22 | CALL | CALL | CALL | CALL | UNANIMOUS |
| BP2_35 | RAISE | RAISE | RAISE | RAISE | UNANIMOUS |
| BP3_03 | FOLD | FOLD | FOLD | FOLD | UNANIMOUS |
| BP4_28 | BET | BET | BET | BET | UNANIMOUS |
| BP5_02 | CHECK | CHECK | CHECK | CHECK | UNANIMOUS |
| BP6_01 | **CALL** | RAISE | RAISE | RAISE | STRONG 3/4 |
| BP7_03 | CALL | CALL | CALL | CALL | UNANIMOUS |
| BP2_36 | RAISE | RAISE | RAISE | RAISE | UNANIMOUS |
| BP2_42 | FOLD | FOLD | FOLD | FOLD | UNANIMOUS |
| BP5_05 | BET | BET | BET | BET | UNANIMOUS |

**Both dissents are from T1.** Same team, same pattern as pilot v1
— T1 tends toward the more conservative action on borderline
monster/drawing spots.

### Dissent analysis

**BP6_01** (As4d on Ks8s3s monotone, RAISE vs T1 CALL):
T1 argued that on a monotone board villain's betting range
already contains made flushes, reducing fold equity. The majority
(and KB Section 1.7) says nut flush draw + As blocker = RAISE
regardless of board texture. **Majority confirmed: RAISE.**

**d5046_CO_flop** (Kd6d on 6h6s9d, BET vs T1 CHECK):
T1 argued check-trap on paired board OOP. Same as pilot v1 (T3
dissent). Majority says trips with 51% TP+ in villain range =
bet for value. **Majority confirmed: BET.**

---

## Report 2: Feature Attention Coverage

### Mandatory composition compliance

All 4 teams tagged all 4 villain composition features
(villain_top_pair_plus_pct, villain_medium_made_pct,
villain_draw_pct, villain_air_pct) on every BET/RAISE/CALL/FOLD
hand. **100% compliance.**

Only CHECK hands (not facing bet) were exempt.

### Bucket-specific compliance

| Bucket | Required features | Compliance |
|--------|------------------|------------|
| Drawing | draw_outs, improvement_probability | 100% |
| Drawing (flush) | + flush_draw_rank, flush_block_pct | 100% |
| Air | overcard_outs, has_showdown_value, villain_fold_equity_est | 100% |
| Monster | spr | 100% |
| Strong made | danger_score | 100% |
| Weak made | has_showdown_value, better_hand_pct | 100% |

### CONFIRMED tier usage

Average per hand: ~5 CONFIRMED tags (in addition to ~4 PRIMARY).
CONFIRMED was used meaningfully — agents tagged composition
features and bucket-specific features as CONFIRMED when they
checked the value but it didn't drive the decision. This
produces richer feature attention data without inflating PRIMARY.

---

## Report 3: Discovery Team Findings

### Coverage

| Metric | T5 | T6 | Combined |
|--------|-----|-----|----------|
| Avg discoveries per hand | 4.8 | 5.0 | 5-6 unique per hand |
| Total discoveries | 48 | 50 | ~55 unique |

### Most frequently discovered features

| Feature | Times discovered | Key insight |
|---------|-----------------|-------------|
| villain_fold_equity_estimate | 14 | Inverted meaning: high = don't bet monsters; low = do bet |
| spr | 10 | Drives stack commitment decisions |
| villain_checked_back | 9 | Delayed aggression signal, range capping |
| connectivity_score | 7 | Straight draw density on connected boards |
| is_preflop_aggressor | 7 | C-bet authority, deception for traps |
| overcard_outs | 7 | Hidden equity for AK/AJ type hands |
| flush_draw_rank | 6 | Nut vs non-nut draw discrimination |
| board_favour | 6 | Range advantage/disadvantage |
| straight_danger | 6 | Protection urgency for made hands |
| is_paired | 5 | Trips/full house board texture |
| flush_block_pct | 4 | Semi-bluff raise qualification |
| flush_danger | 4 | Board wetness for protection decisions |

### Key discovery patterns

1. **villain_fold_equity_estimate inverts by hand strength:**
   Monsters should CHECK when fold equity is high (60-70%)
   because betting folds too many worse hands. Monsters should
   BET when fold equity is low (10-15%) because villain calls
   with most of their range.

2. **overcard_outs gap:** The pipeline reports
   improvement_probability=0 for unpaired overcards (AK/AJ),
   but these hands have 6 hidden overcard outs. Discovery teams
   flagged this in 3 hands. Known gap per KB Example 7.

3. **facing_raise is underweighted:** On later streets, a raise
   into multiple opponents is nearly always the nuts. Discovery
   teams flagged this as a critical signal in 3 river/turn folds.

---

## Report 4: Untagged Feature List

Full untagged feature list per hand is at:
`review/comms/PILOT_V2_UNTAGGED_FEATURES_2026-04-14.txt`

### Summary

- Average untagged: 36.4/54 features per hand
- Average tagged (union of all 6 teams): 17.6/54
- Many untagged features are structural (street, num_opponents,
  pot_size, to_call, hero_position, villain_position) that
  don't directly drive decisions
- **Flagged untagged features** (potentially missed):

| Hand | Feature | Value | Why it might matter |
|------|---------|-------|---------------------|
| BP1_22 | is_preflop_aggressor | 1 | PFA status affects c-bet credibility |
| BP2_35 | is_preflop_aggressor | 1 | PFA with top set — adds deception |
| BP3_03 | flush_draw_rank | 12 | Queen-high flush draw on same board — near-nut |
| BP5_02 | spr | 1.11 | Low SPR drives stack commitment |
| d1971_HJ_river | spr | 0.75 | Committed SPR on river |
| d6384_BTN_turn | connectivity_score | 7 | High connectivity supports fold on air |

Most flagged features were covered by discovery teams. The
remaining untagged features are genuinely non-decision-driving
for their specific hands (structural features, zero-value
features like is_3bet_pot=0, num_callers_to_bet=0, etc.).

---

## Comparison: Pilot v1 vs v2

| Metric | Pilot v1 (6 teams) | Pilot v2 (4+2 teams) |
|--------|-------------------|---------------------|
| Action consensus | 19/20 unanimous | 18/20 unanimous |
| Action match rate | — | 20/20 vs v1 |
| Composition coverage | ~60% | 100% (mandatory) |
| CONFIRMED tier | N/A | Active, ~5/hand |
| Discovery features | 0 | ~5/hand |
| Avg features tagged | ~4.2 | 17.6 (union) |
| Untagged scan | N/A | Full 54-feature list |

The v2 structure produces much richer feature attention data
while maintaining identical action consensus.

---

## Recommendation

**Proceed to Pass 1 production** with this structure:
- 4 labelling teams (Approach C amended)
- 2 discovery teams (bottom-up scan after consensus)
- Mandatory composition on BET/RAISE/CALL/FOLD
- Bucket-specific mandatory features
- CONFIRMED tier
- Full untagged feature list per hand for owner spot-checks

The 20 pilot v2 labels become production labels for these hands.

**Agent count for Pass 1 (385 hands):**

| Role | Calculation | Agents |
|------|-------------|--------|
| T1-T4 labelling | 4 teams x 39 batches of 10 | 156 |
| T5-T6 discovery | 2 teams x 39 batches of 10 | 78 |
| Comparison reports | 39 | 39 |
| **Total** | | **~273** |
