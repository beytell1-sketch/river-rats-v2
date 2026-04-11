# BET Decision Tree v1 — For Labelling Agent

**Date:** 9 April 2026
**Author:** GTO Expert — synthesised from 5 research papers + 3 cross-reviews
**Status:** AWAITING REVIEW + OWNER APPROVAL
**Applies to:** Situations where `to_call == 0` (hero is not facing a bet)
**Scope:** 3-way pots, 100bb effective, single-raised pots (SRP) unless noted
**Output:** BET or CHECK — never a frequency

---

## Changelog

| # | Description |
|---|-------------|
| 1 | New document — no prior version exists |
| 2 | Informed by RESEARCH_CBET_R1_FREQUENCY (position-split frequencies) |
| 3 | Informed by RESEARCH_CBET_R2_TEXTURE (4-tier board texture classification) |
| 4 | Informed by RESEARCH_CBET_R3_SIZING_SPR (SPR zone framework) |
| 5 | Informed by RESEARCH_CBET_R4_CHECKBACK (4 check types, protection vs trap) |
| 6 | Informed by RESEARCH_CBET_R5_BLOCKERS (blocker effects on c-bet direction) |
| 7 | Cross-reviews (REVIEW_CBET_R1_R2, REVIEW_CBET_R3_R4, REVIEW_CBET_R5_AND_CROSS) incorporated |
| 8 | Structured to match RAISE_DECISION_TREE_V2.md conventions |
| 9 | Feature names match feature_keys.py (class F), 53-feature vector |

**Key design decisions:**

- R2's 4-tier texture classification is the primary gate (board_favour is the
  main proxy; high_card_rank, flush_danger, straight_danger, connectivity_score,
  is_paired are the discriminating features).
- R1's position split (IP vs OOP) is the secondary gate. OOP PFA c-bets at
  approximately 22-30% on any texture — much lower than IP. OOP threshold is
  stricter on every step.
- R3 establishes that standard SRP flop SPR is high (8-12). "High SPR behaviour"
  — frequent checking, small sizing when betting — is the DEFAULT, not an
  exception. Low SPR (< 3) appears on turn in SRP or flop in 3-bet pots.
- R4's 4 check types (give up, pot control, trap, equity realization OOP) are
  encoded as the Default and suppressors, not as separate steps.
- R5 establishes that flush blockers aid bluff c-bets but do NOT aid thin value
  c-bets (opposite direction). Combo draws (12+ outs) can c-bet without a blocker.
- Cross-review Issue 4: R2's frequency tables were IP PFA figures. OOP figures are
  approximately 30-40% lower. This is enforced in every step below.
- Middle connected board disagreement (R1: 22-30%, R2: 30-40%): resolved by
  adopting R2's tiered system as the primary framework and treating R1's lower
  figure as applying to the high-connectivity end of that tier. Threshold reflects
  the more conservative boundary.

---

## Preamble

Every branch of this tree must be evaluable using ONLY the 53-feature vector.

Features available: `street`, `facing_bet`, `pot_size`, `to_call`, `pot_odds`,
`bet_to_pot`, `hero_position`, `villain_position`, `is_ip`, `hand_category`,
`hand_rank`, `is_made_hand`, `is_strong_made`, `is_monster`, `has_flush_draw`,
`has_straight_draw`, `draw_outs`, `is_monotone`, `is_two_tone`, `is_rainbow`,
`is_paired`, `is_double_paired`, `connectivity_score`, `high_card_rank`,
`danger_score`, `flush_danger`, `straight_danger`, `raw_equity`, `equity_vs_range`,
`better_hand_pct`, `worse_hand_pct`, `equity_margin`, `spr`, `is_3bet_pot`,
`villain_aggression_count`, `villain_checked_back`, `villain_call_count`,
`num_opponents`, `villain_top_pair_plus_pct`, `villain_draw_pct`, `villain_air_pct`,
`villain_range_capped`, `board_favour`, `num_callers_to_bet`, `facing_raise`,
`flush_block_pct`, `overcard_outs`, `improvement_probability`,
`hero_range_percentile`, `has_showdown_value`, `villain_fold_equity_estimate`,
`flush_draw_rank`, `is_preflop_aggressor`.

This tree applies when `to_call == 0`. If `to_call > 0`, use the RAISE tree.

If any condition in a step cannot be computed from the above features,
that condition is removed and the step is skipped. If no step fires BET,
the hand defaults to CHECK.

---

## Global Pre-Check: Is This Tree Applicable?

Before running any step, verify:

A. `to_call == 0` — hero is not facing a bet. If `to_call > 0`, stop. Use RAISE tree.
B. `num_callers_to_bet == 0` — no opponent has already called a bet into this pot
   on this street in a way that would redirect to the RAISE tree.
C. `num_opponents >= 1` — pot is contested.

If any pre-check fails, this tree does not apply.

---

## Step 1 — Global Suppressors (force CHECK regardless of later steps)

If ANY of the following is true, output CHECK and do not proceed further.

**S1. Wet board bluff suppressor:**
`flush_danger >= 0.60 OR straight_danger >= 0.50`
AND `is_made_hand == 0`
AND `draw_outs < 12`
→ CHECK. Wet board with no made hand and no combo draw — bluff c-bet is
unprofitable (two opponents on flush/straight draws do not fold).

**S2. OOP suppressor (non-monster, non-exception):**
`is_ip == 0`
AND `is_monster == 0`
AND `hero_range_percentile < 0.72`
AND `raw_equity < 0.60`
→ CHECK. OOP PFA c-bets only 22-30% on any texture. Below top 28% of range
and below 60% raw equity, OOP default is pot control or give-up.
(Steps 2, 3B, and 6 provide the OOP exceptions that override this suppressor.)

**S3. Multi-street villain aggressor suppressor:**
`villain_aggression_count >= 2`
AND `hero_range_percentile < 0.85`
→ CHECK. Villain has shown strength across multiple streets. Thin value bets
and bluffs are punished. Only near-top-of-range hands proceed past this.

**Note:** S1 and S3 apply to ALL subsequent steps. S2 applies to Steps 3, 4,
and 5 only — Steps 2 and 6 have explicit OOP carve-outs built into their
conditions.

---

## Step 2 — Monster Protection Bet (Dynamic Board)

**Purpose:** Strong hands must bet for protection when draw danger is high.
Slowplaying costs too much when two opponents hold draws. R4 Finding 10.

**Condition — ALL required:**
- `is_monster == 1`
- `danger_score >= 0.45` OR `flush_danger >= 0.45` OR `straight_danger >= 0.40`
- `is_preflop_aggressor == 1` OR `raw_equity >= 0.70`

**Logic:** Monster on a dynamic board — two opponents can outdraw. Bet regardless
of position. Protection outweighs deception.

**IP threshold:** danger_score >= 0.45 (bet)
**OOP threshold:** danger_score >= 0.45 (same — protection requirement does not
loosen for OOP; if anything OOP needs to bet more urgently because they cannot
control future streets).

→ **BET**. Confidence: HIGH.

**Why this fires before the dry-board trap check:** On dynamic boards, checking
a monster hands two opponents a free card with combined draw equity that can exceed
40%. The free card cost overwhelms any deception value. R4 "The trap rule: Slowplay
monsters on dry, disconnected boards. Bet monsters on dynamic boards."

**Dry/moderate board monster (does NOT fire this step):** `is_monster == 1` AND
`danger_score < 0.45` — proceed to Default CHECK (trap on static boards).

---

## Step 3 — PFA Value C-Bet (Made Hand, Favorable Board)

**Purpose:** PFA bets for value when board favors their range and they hold a
made hand. The core PFA c-bet scenario. R1 Finding 6, R2 Tier 1-2 classification.

**Condition — ALL required:**
- `is_preflop_aggressor == 1`
- `is_made_hand == 1`
- `high_card_rank >= 12` (board favors PFA's range — Q or higher top card)

**Then split by position and hand strength:**

### Step 3A: IP PFA Value Bet

Additional requirements:
- `is_ip == 1`
- `hand_category >= 7` (top_pair_good_kicker or better)
  AND board texture gates below pass

**Board texture gates (IP PFA, all must pass):**

Gate 3A-1: Dry or moderately connected board.
`connectivity_score <= 6` OR `high_card_rank >= 12`
(Queen or higher top card forgives moderate connectivity)

Gate 3A-2: Flush danger is not severe.
`flush_danger <= 0.50` OR (`flush_danger > 0.50` AND `flush_draw_rank >= 12`)
(High flush danger is acceptable only if hero holds the nut flush draw)

Gate 3A-3: Hand is strong enough for the texture.
- Tier 1 texture (A/K-high dry): `hand_category >= 6` (top_pair+)
- Tier 2 texture (Q/J-high, mild danger): `hand_category >= 7` (TPGK+)
- Tier 3 texture (moderate danger): `hand_category >= 10` (two_pair+)
- Tier 4 texture (low connected / monotone): Step 3A does NOT fire; skip to Step 7

Texture tier determination from features (evaluate in order — first match applies):
- Tier 1: `high_card_rank >= 13` (K or A) AND `flush_danger <= 0.20` AND `connectivity_score <= 3`
- Tier 2: (`high_card_rank >= 11` (J+)) AND `flush_danger <= 0.35` AND `connectivity_score <= 5`
- Tier 3: `flush_danger <= 0.50` AND `connectivity_score <= 7`
- Tier 4: everything else (default to CHECK via Step 7)

→ **BET** (IP PFA Value). Confidence: HIGH on Tier 1, MEDIUM on Tier 2,
MEDIUM-LOW on Tier 3.

**Frequency calibration note (do not use as threshold — informs permissiveness):**
- Tier 1 IP PFA: 60-70% bet frequency → loose gate (hand_category >= 6)
- Tier 2 IP PFA: 40-55% bet frequency → moderate gate (hand_category >= 7)
- Tier 3 IP PFA: 25-40% bet frequency → strict gate (hand_category >= 10)

### Step 3B: OOP PFA Value Bet (Exception)

The OOP suppressor (S2) blocks most OOP bets. Step 3B is the narrow carve-out.

Additional requirements:
- `is_ip == 0`
- `hand_category >= 7` (TPGK minimum — no thin value OOP)
- `high_card_rank >= 13` (K or A high board required OOP — stricter range advantage gate)
- `villain_air_pct >= 0.40` (both opponents holding mostly air)
- `is_rainbow == 1` OR `flush_danger <= 0.20` (dry board — reduces callers' draws)
- `villain_aggression_count == 0` (passive opponents — OOP bet into aggressive
  opponents invites check-raises from hands that dominate)
- `hero_range_percentile >= 0.72` (top 28% of range minimum OOP)

→ **BET** (OOP PFA Value Exception). Confidence: MEDIUM.

**Source:** R4 Finding 5 + KB Example 6 (OOP value exception pattern).
OOP PFA c-bets approximately 22-30% even on best textures. These requirements
produce a bet frequency in that range.

---

## Step 4 — PFA Bluff C-Bet (Semi-Bluff with Equity)

**Purpose:** PFA missed but holds enough equity (draw or blocker) to make a
semi-bluff c-bet credible. Pure air NEVER bets. R4 Finding 2, R5 Findings 4-5.

**Condition — ALL required:**
- `is_preflop_aggressor == 1`
- `is_made_hand == 0`
- `high_card_rank >= 12` (range credibility — Q or higher top card means PFA's range has
  high-card advantage on this board even if this specific hand missed; threat is in the range)

**Then one of these equity sub-conditions must also be true:**

**Sub-condition 4A: Combo draw (primary semi-bluff vehicle):**
`draw_outs >= 12`
(Combo draws — flush draw + straight draw — have 50%+ equity when called.
Fold equity becomes secondary. This fires regardless of flush_block_pct.
R5 Finding 4: "The only draw class where the math works without a blocker.")

**Sub-condition 4B: Near-nut flush draw with blocker:**
`draw_outs >= 9`
AND `flush_draw_rank >= 12` (Q, K, or A of flush suit)
AND `flush_block_pct > 0`
(Nut/near-nut flush draw + blocker to villain's continuing range. Fold equity
is elevated because villain's nut flush combos are removed. R5 Findings 1-2.)

**Sub-condition 4C: Nut draw + favorable board (no blocker required):**
`draw_outs >= 9`
AND `flush_draw_rank >= 13` (K or A of flush suit — extra strength)
AND `board_favour >= 0.30` (stronger board advantage required without blocker)
AND `is_ip == 1` (IP only — OOP semi-bluffs without blocker not viable 3-way)

**Sub-condition 4D: Blocker + weak draw (edge case, restricted):**
`flush_block_pct > 0`
AND `draw_outs >= 4` (gutshot minimum — pure backdoor is NOT sufficient)
AND `villain_air_pct >= 0.40` (villain range is air-heavy; fold equity exists)
AND `is_ip == 1` (IP only)
AND `high_card_rank >= 13` (K or A high board — dry enough for blocker to matter)
AND `is_rainbow == 1` (rainbow board — flush blocker is most impactful when board
has no existing flush draws for villains; on two-tone board, one villain has flush
draw regardless of blocker)

**Position gate for Step 4:**
- IP: sub-conditions 4A, 4B, 4C, 4D all apply
- OOP: sub-condition 4A only (combo draw 12+ outs, OOP can semi-bluff with combo
  draw equity). OOP with sub-conditions 4B, 4C, 4D → CHECK.

**Wet board suppressor (Step 4 specific):**
If `flush_danger >= 0.60` AND sub-condition 4B or 4D (not 4A) → CHECK.
Wet boards mean villain holds draws, making the blocker less effective.
(Sub-condition 4A survives wet boards because 12+ outs provide own equity.)

→ **BET** (PFA Bluff C-Bet). Confidence: MEDIUM (4A), MEDIUM (4B),
MEDIUM-LOW (4C, 4D).

**Backdoor-only hands (draw_outs == 0, overcard_outs only):**
Backdoor flush draw alone adds only 3-4% equity — insufficient for a bluff
c-bet 3-way. These hands CHECK. The lone exception is if hand_category >= 6
(top pair qualifies as a made hand, not a bluff — handled in Step 3).
R5 Finding 5: "A backdoor flush draw alone does NOT make a hand c-bettable 3-way."

---

## Step 5 — Thin Value Bet (IP, Capped Opponent)

**Purpose:** IP hero with a decent made hand bets into capped opponents for thin
value. Distinct from Step 3 because hero may not be the PFA. R1 Finding 5.

**Condition — ALL required:**
- `is_ip == 1`
- `is_made_hand == 1`
- `hand_category >= 7` (TPGK minimum for thin value)
- `villain_range_capped == 1` (at least one opponent's preflop action caps their range)
- `villain_top_pair_plus_pct <= 0.35` (villain is unlikely to hold strong made hands;
  thin value bets need callers that are behind, not callers with top pair+)
- `danger_score <= 0.35` (dry board — thin value bets into draws lose value)
- `villain_aggression_count <= 1` (not against a multi-street aggressor)
- `is_preflop_aggressor == 0` (if PFA, Step 3 already handled this)

**Rationale:** The cold-caller (capped range) holds no premiums but has medium pairs,
top pair weak kicker, suited connectors that missed. IP hero with TPGK bets small
into this range for thin value on dry boards. R1 Finding 5.

→ **BET** (Thin Value IP). Confidence: MEDIUM-LOW.

**Validator check:** If `villain_aggression_count >= 2`, do NOT fire this step.
A capped range that has shown multi-street aggression is not actually "capped" in
the way this step requires — they are representing strength. Default to CHECK.

---

## Step 6 — OOP Value Bet Exception (KB Example 6 Pattern)

**Purpose:** Non-PFA OOP hero with strong equity and air-heavy opponents bets for
value. Rare but explicitly documented in the KB. R4 Step 3 decision framework.

**Condition — ALL required:**
- `is_ip == 0`
- `raw_equity >= 0.65` (strong equity edge — OOP value bet requires more than IP)
- `villain_air_pct >= 0.45` (majority of opponent ranges are air)
- `is_rainbow == 1` (dry board — no flush draw for opponents to continue with)
- `connectivity_score <= 3` (disconnected — no straight draw either)
- `hand_category >= 8` (TPTK minimum — OOP value requires strong made hand)
- `villain_aggression_count == 0` (passive opponents — OOP bet into aggression invites
  check-raises)
- `villain_fold_equity_estimate >= 0.35` (some fold equity required OOP)

→ **BET** (OOP Value Exception). Confidence: MEDIUM-LOW.

**Note:** This step overrides OOP Suppressor S2 because it has stronger requirements
than S2's thresholds. The step fires only when all conditions are simultaneously
satisfied, which occurs rarely and matches the documented pattern.

---

## Step 7 — Default

No step 2-6 returned BET.

→ **CHECK**.

This is the correct outcome for the majority of 3-way flop decisions. The PFA checks
approximately 57% of the time 3-way (R4 Finding 1). This default encodes:
- Check to give up (air, complete miss)
- Check for pot control (top pair on dangerous board, overpair on connected board)
- Check to trap (monster on dry board — Step 2 did not fire because danger_score < 0.45)
- Check to realize equity OOP (draws and marginal hands OOP)

---

## Quick Reference: Hands That BET

| Scenario | Key Features | Step |
|----------|-------------|------|
| Monster on wet/dynamic board | is_monster=1, danger_score >= 0.45 | 2 |
| PFA, top pair+, A/K-high dry, IP | is_preflop_aggressor=1, hand_cat >= 6, Tier 1, is_ip=1 | 3A |
| PFA, TPGK+, Q/J-high dry, IP | is_preflop_aggressor=1, hand_cat >= 7, Tier 2, is_ip=1 | 3A |
| PFA, two pair+, connected board, IP | is_preflop_aggressor=1, hand_cat >= 10, Tier 3, is_ip=1 | 3A |
| PFA, TPGK+, dry board, passive villain, OOP | is_preflop_aggressor=1, villain_air >= 0.40, rainbow | 3B |
| PFA missed, combo draw 12+ outs | is_preflop_aggressor=1, is_made=0, draw_outs >= 12 | 4 (4A) |
| PFA missed, nut FD + blocker | is_preflop_aggressor=1, FD rank >= 12, flush_block > 0 | 4 (4B) |
| PFA missed, nut FD (K/A), IP, board favour | is_preflop_aggressor=1, FD rank >= 13, is_ip=1 | 4 (4C) |
| IP non-PFA, TPGK, capped villain, dry | is_ip=1, villain_capped=1, danger <= 0.35 | 5 |
| OOP non-PFA, strong equity, air villain, dry | is_ip=0, raw_eq >= 0.65, air >= 0.45 | 6 |

---

## Quick Reference: Hands That CHECK

| Scenario | Reason | Suppressor/Default |
|----------|--------|-------------------|
| Monster on dry board (slowplay) | Trap: opponents drawing nearly dead | Default 7 (Step 2 did not fire) |
| Air, no draw, any board | Give up: pure bluffs lose 3-way | S1 or Default 7 |
| Backdoor-only draw | Equity too low (3-4%) for c-bet | Default 7 |
| Top pair on low connected board | Way ahead/way behind or dominated | Default 7 |
| Top pair, OOP, passive board | Pot control: reach showdown cheap | S2 or Default 7 |
| Overpair, connected board, IP | WAWB: worse hands fold, better hands call | Default 7 |
| Any hand vs multi-street aggressor | Villain strength suppresses thin value/bluff | S3 or Default 7 |
| OOP hand below top 28% range | OOP c-bet frequency too low | S2 (overridden only by Steps 2, 6) |
| NFD without blocker OOP | Fold equity insufficient OOP without blocker | Step 4 position gate |
| Monotone board, not monster | Villain flush draws everywhere; fold equity near zero | Tier 4 in Step 3A; S1 if is_made=0 |

---

## Suppressor Summary

| Suppressor | Condition | Effect |
|------------|-----------|--------|
| S1 (wet bluff) | flush_danger >= 0.60 OR straight_danger >= 0.50, no made hand, draw_outs < 12 | Force CHECK |
| S2 (OOP default) | is_ip == 0, not monster, hero_range_percentile < 0.72, raw_equity < 0.60 | Force CHECK (Steps 3A, 4, 5). Overridden by Steps 2, 3B, and 6. |
| S3 (aggressor) | villain_aggression_count >= 2, hero_range_percentile < 0.85 | Force CHECK |

---

## Feature Reference Table

All features used in this tree. Names match `feature_keys.py` (class F).

| Feature | Encoding / Range | How Used |
|---------|-----------------|----------|
| `to_call` | Integer >= 0 | Pre-check: must be 0 for this tree |
| `is_preflop_aggressor` | 0 or 1 | Identifies PFA; gates Steps 3, 4 |
| `is_ip` | 0 or 1 | Position gate on all steps |
| `is_monster` | 0 or 1 | Gates Step 2 |
| `is_made_hand` | 0 or 1 | Gates Steps 3 (made) vs 4 (bluff) |
| `is_strong_made` | 0 or 1 | Supporting context; hand_category is primary |
| `hand_category` | 0=high_card, 1=one_overcard, 2=overcards, 3=bottom_pair, 4=underpair, 5=middle_pair, 6=top_pair, 7=top_pair_good_kicker, 8=top_pair_top_kicker, 9=overpair, 10=two_pair, 11=trips, 12=straight, 13=flush, 14=full_house, 15=quads, 16=straight_flush | Primary hand strength gate |
| `hero_range_percentile` | 0.0–1.0 | OOP threshold (S2: < 0.72); aggressor threshold (S3: < 0.85) |
| `raw_equity` | 0.0–1.0 | OOP bet gate (Step 3B >= 0.60, Step 6 >= 0.65) |
| `board_favour` | Negative = villain range favoured; positive = PFA favoured | [DEMOTED] No longer used as primary gate. Retained in preamble for context. Steps 3 and 4 use high_card_rank >= 12 as range-advantage proxy. |
| `high_card_rank` | 2–14 (card rank of highest board card) | [PROMOTED] Primary range-advantage gate in Steps 3 and 4. Tier determination in Step 3A (existing). OOP threshold >= 13. |
| `flush_danger` | 0.0–1.0 | Tier gate; suppressor S1 (>= 0.60) |
| `straight_danger` | 0.0–1.0 | Tier gate; suppressor S1 (>= 0.50) |
| `connectivity_score` | 0–10 integer (observed range: 2–8 in BET situations) | Tier determination in Step 3A; Step 6 gate |
| `danger_score` | 0.0–1.0 | Protection bet gate in Step 2 (>= 0.45) |
| `is_monotone` | 0 or 1 | Tier 4 indicator; cross-check |
| `is_two_tone` | 0 or 1 | Flush danger context |
| `is_rainbow` | 0 or 1 | OOP exception gates (Steps 3B, 6) |
| `is_paired` | 0 or 1 | Paired board modifier (raises tier) |
| `draw_outs` | 0–17 (clean outs to best draw) | Semi-bluff gates in Step 4 |
| `flush_draw_rank` | 0=no flush draw, 2–14=rank of highest card in flush suit | Step 4B/4C nut draw quality gate (>= 12 = Q/K/A) |
| `flush_block_pct` | 0.0–1.0 | Blocker gate in Steps 4B, 4D |
| `has_flush_draw` | 0 or 1 | Context; draw_outs is primary |
| `has_straight_draw` | 0 or 1 | Context; draw_outs is primary |
| `villain_range_capped` | 0 or 1 | Step 5 thin value gate |
| `villain_aggression_count` | Integer count | Suppressor S3 (>= 2); Step 5 gate (<= 1); Step 3B/6 gate (== 0) |
| `villain_air_pct` | 0.0–1.0 | Steps 3B, 4D, 6 (air-heavy opponent required for OOP/thin bets) |
| `villain_top_pair_plus_pct` | 0.0–1.0 | Step 5 gate (<= 0.35) |
| `villain_fold_equity_estimate` | 0.0–1.0 | Step 6 gate (>= 0.35) |
| `villain_checked_back` | 0 or 1 | Context for delayed c-bet situations |
| `num_callers_to_bet` | Integer | Pre-check (must be 0) |
| `num_opponents` | Integer | Pre-check (must be >= 1) |
| `spr` | Stack-to-pot ratio | High SPR (>= 8) = high-SPR default behaviour |
| `is_3bet_pot` | 0 or 1 | Context: 3-bet pots have different SPR profiles |
| `overcard_outs` | Integer | Context for backdoor situations |
| `improvement_probability` | 0.0–1.0 | Supporting context for draw quality |
| `equity_margin` | Signed float | Supporting context |
| `better_hand_pct` | 0.0–1.0 | Supporting context |
| `worse_hand_pct` | 0.0–1.0 | Supporting context |

---

## Frequency-to-Threshold Mapping

This table documents how each research frequency finding was converted into a
deterministic feature threshold. Required by the task specification.

| Research Frequency | Context | Threshold Derived | Step | Permissiveness |
|-------------------|---------|------------------|------|----------------|
| IP PFA, A-high dry: 60-70% | R1 Finding 6, R2 Tier 1 | hand_category >= 6 (top_pair) | 3A Tier 1 | Wide — most made hands bet |
| IP PFA, K-high dry: 50-60% | R1 Finding 6, R2 Tier 1 | hand_category >= 6 (top_pair) | 3A Tier 1 | Wide (included with A-high) |
| IP PFA, Q-high dry: 40-48% | R1 Finding 6, R2 Tier 2 | hand_category >= 7 (TPGK) | 3A Tier 2 | Moderate |
| IP PFA, connected mid (T86): 22-30% | R1 Finding 6 (lower end) | hand_category >= 10 (two_pair) | 3A Tier 3 | Narrow — only strong hands |
| IP PFA, monotone: 20-30% | R1 Finding 6, R2 Tier 4 | Step 3A does not fire (Tier 4 excluded) | — | No bet (Step 2 or Default) |
| OOP PFA, any: 22-30% | R1 Finding 3 | hero_range_percentile >= 0.72 (top 28%) | S2, Steps 3B, 4 | Tight |
| OOP PFA, A-high dry: 35-45% | R1 Finding 3, R2 Tier 1 | villain_air >= 0.40 + is_rainbow required | 3B | Tighter than IP Tier 1 |
| Defender donk: 5-12% | R1 Finding 4 | Not a c-bet step — tree is for PFA/IP | — | Handled by Steps 5, 6 (rare) |
| Cold-caller probe: 20-35% | R1 Finding 5 | is_preflop_aggressor=0, villain_capped=1, danger <= 0.35 | 5 | Narrow for non-PFA |
| Monster on dynamic board: ~80%+ | R4 Finding 4 (wet board), KB Example 4 | danger_score >= 0.45 | 2 | Wide — all monsters on wet boards |
| Monster on dry board: ~35-50% IP trap | R4 Finding 4 | Step 2 does not fire (danger_score < 0.45) → Check | Default 7 | Trap = CHECK |
| Combo draw: viable semi-bluff | R5 Finding 4 | draw_outs >= 12 | 4A | Single threshold |
| NFD + blocker: semi-bluff viable | R5 Findings 1-2, KB 1.7 | flush_draw_rank >= 12 AND flush_block_pct > 0 | 4B | Both conditions required |
| OOP value exception: rare | R4 Step 3, KB Example 6 | raw_equity >= 0.65 + villain_air >= 0.45 + rainbow | 6 | Very strict |
| Pure air bluff 3-way: ~0-5% | R2 Section 2.9, R4 Finding 2 | No bluff step fires for draw_outs < 4 | — | Suppressed to zero |

---

## SPR Notes for Labelling Agent

Standard 3-way SRP flop SPR at 100bb is approximately 8-12 (high SPR zone).
This is the DEFAULT environment. Behaviour:
- Default c-bet frequency: ~43% (GTO Wizard aggregate)
- Default sizing: 25-33% pot
- Large bets (> 50% pot): near zero (1.3% of situations)

Low SPR (< 3) appears on:
- Turn in SRP after a flop c-bet
- Flop in 3-bet pots (is_3bet_pot == 1)

At low SPR: strong hands should bet more urgently (two pair+ BET). The commitment
threshold shifts: at SPR < 2, two pair or better commits regardless of other factors.
This tree's Step 2 (monster protection) and Step 3A (PFA value) both produce BET
for these hands and remain correct at low SPR. SPR does not need to be an explicit
gate in this tree because the hand strength and protection conditions already produce
the right outputs; SPR modulates sizing (not covered by this tree, which outputs
BET or CHECK only).

---

## Known Limitations and Gaps

These are inherited from the research documents and flagged by the reviewers.
They do not block using this tree but should inform future revisions.

**Gap 1: OOP texture-specific frequencies not quantified.**
R2's texture tables are IP PFA figures (REVIEW_CBET_R5_AND_CROSS Issue 4).
OOP equivalents reduce by approximately 30-40% from IP. This tree enforces
tighter OOP thresholds throughout but exact OOP-by-texture solver data is not
available.

**Gap 2: Backdoor flush draw equity not in draw_outs.**
draw_outs counts frontdoor draws only. A hand with backdoor flush + overcard
has approximately 7-9% hidden equity but draw_outs == 0 in the feature set.
Such hands may be labelled CHECK when the GTO action is a thin c-bet. Accept
this limitation — do not add a backdoor exception to the tree without a feature
that captures it. (R5 Finding 5, REVIEW_CBET_R5_AND_CROSS Gap A.)

**Gap 3: Made-hand nut blocker effect not in flush_block_pct.**
flush_block_pct measures villain's flush draw combos blocked, not the value-safety
effect of holding an Ace on an Ace-high board (blocking AA, AK). Thin value c-bets
on Ace-high boards where hero holds Ah may be slightly under-labelled. Accept.
(REVIEW_CBET_R5_AND_CROSS Gap B.)

**Gap 4: Middle connected board frequency disagreement.**
R1 says 22-30%, R2 Tier 3 says 25-40% for similar textures. This tree resolves
by using hand_category >= 10 (two_pair) as the Tier 3 gate — conservative enough
to satisfy R1's lower bound while being met by hands that would also bet under R2.

**Gap 5: Three-bet pots have different profiles.**
is_3bet_pot == 1 puts the situation in medium SPR territory on the flop (SPR ~2-4).
This tree was designed for SRP. At 3-bet pot SPR, bet thresholds should tighten
(two opponents at medium SPR with narrower, stronger ranges). The tree's conditions
remain directionally correct but may over-produce BET labels on 3-bet pot flops.
Flag these for separate review if 3-bet pot situations are in the labelling dataset.

**Gap 6: MDF math framing (R3 vs R4).**
R3 computes required per-opponent fold rate (86.7% for break-even on 33% pot pure
bluff). R4 computes combined achieved fold rate (0.75 x 0.75 = 56%) against the
alpha (24.8%). These frame the same math differently. Both support the same conclusion:
pure air bluffs do not work 3-way; semi-bluffs with equity can. This tree reflects
that conclusion in Step 4 (equity required for all bluff sub-conditions).

---

*File: `/home/rupertbeytell/river-rats-v2/review/BET_DECISION_TREE_V1.md`*
*Status: Ready for owner review. Not yet approved or integrated.*
