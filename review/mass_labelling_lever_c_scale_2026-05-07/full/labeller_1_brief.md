# Mass-labelling brief — labeller 1/5

You are a v3.4 GTO poker labeller. Read the protocol below in full BEFORE labelling. Then label each of the 150 hands in the corpus block. Apply the protocol verbatim — no improvisation.

## Output contract

Write your labels to:

    review/mass_labelling_lever_c_scale_2026-05-07/full/labels_v3_4_labeller_1.json

Schema (matches Phase B Protocol A on master 4bce49f):

```json
{
  "lane": "labeller_1",
  "model": "claude-sonnet-4-6",
  "protocol_version": "v3.4",
  "protocol": "prompts/gto_labeller_v3.4.md",
  "total_labels": 150,
  "labels": [
    {
      "ref_id": "<the HAND id from the corpus block>",
      "action": "BET|RAISE|CALL|CHECK|FOLD",
      "confidence": "HIGH|MEDIUM|LOW",
      "reasoning": "<one paragraph applying the v3.4 protocol>"
    },
    ...
  ]
}
```

Hard requirements:
- One label per hand, exactly. No duplicates, no skips.
- ``ref_id`` must match the HAND id from the corpus block verbatim.
- ``action`` must be one of {BET, RAISE, CALL, CHECK, FOLD}, uppercase.
- ``confidence`` must be one of {HIGH, MEDIUM, LOW}, uppercase.
- If you cannot determine an action with confidence, output
  ``"action": null`` and ``"confidence": "LOW"`` with the reasoning explaining the refusal. Refusals must NOT exceed 5%% of hands (<= 25 of 150).
- Output ONLY the JSON file at the path above. No markdown, no chat-style prose around it.

## v3.4 protocol (verbatim)

# 3-Way Postflop GTO Labelling Agent — v3.2

**Version:** v3.2
**Date:** 2026-04-26
**Replaces:** `prompts/gto_labeller_v3.1.md` (still on disk; do not delete — v3.1 remains a historical artifact)

## Changes from v3.1 (explicit)

**What's new in v3.2 (empirically motivated by A.4 Option C calibration HALT, master `b2de857`):**

- **DO NOT Rule 11 added** (paired-board / 2-tone-flush-board OOP CHECK exception). Empirically motivated by A.4 Option C (`b2de857`): both Sonnet 4.6 AND Opus 4.7 on v3.1 incorrectly bet `d3688_BB_flop` (8cKc on KdTd4s; expert CHECK) and `d9556_BB_flop` (5h5d on 5s6d6h flopped fives full; expert CHECK). Both lanes invoked "monsters/strong-made must bet 3-way" reasoning. Rule 11 codifies the paired-board + 2-tone OOP exception (note: v3.1 numbering compacted v3's Rule 11 §3.B to Rule 10; this v3.2 Rule 11 is a fresh slot, not a revival). See empirical evidence: `review/pilot_run_2026-04-26/calibration_results_*.json` + `PILOT_PHASE_A_SUMMARY_HALT_2026-04-26.md`. Tag: `[v3.2 addition Fix 1]`.
- **KB §1.7 carve-out tightened** with `villain_air_pct >= 0.20` threshold. Empirically motivated by A.4 (`b2de857`): both Sonnet AND Opus on v3.1 incorrectly raised MW-39 (AhJh on Kh8h3d; expert CALL) by invoking KB §1.7 (nut FD + Ah blocker → RAISE) on a spot with `villain_air_pct = 0.05` (effectively zero fold equity). The 0.20 threshold matches `feedback_solver_findings.md` solver-corrected MW-30 CALL anchor. v3.2 adds an OVERRIDE section in Calibration Notes that supplements (does not edit) the standalone KB file `knowledge/three_way_gto.md` §1.7. Labellers reading v3.2 must apply the v3.2 threshold over the unmodified KB §1.7 carve-out. Tag: `[v3.2 addition Fix 2]`.

**What's preserved from v3.1:**
- All v3.1 features, KB references, DO NOT Rules 1-10 (the full v3.1 set), output schema, Calibration Notes for v2 + v2.3 anchors. v3.2 is purely additive — no content removed from v3.1; only DO NOT Rule 11 (Fix 1) and the KB §1.7 OVERRIDE section (Fix 2) added.

**Bundled cross-protocol fix (Protocol B only — applied at the protocol pilot artifact, not in this file):**
- F-S5 phantom feature patch: `prompts/protocol_b_composition_first_v1_0_pilot.md` L283-285 + `prompts/protocol_b_composition_first_v1_0.md` L264-266. Range-mass axis no longer references the phantom `hero_top_pair_plus_pct` feature; replaced with hand-class proxy derivation per `MAIN_TERMINAL_PHASE_A8_SYNTHESIS_FS5_PATCH_DIRECTIVE_2026-04-26.md` (master `947f176`) and bundled per `MAIN_TERMINAL_PATH_A_V32_PROTOCOL_REVISION_DIRECTIVE_2026-04-26.md` (master `24494eb`). This fix is Protocol-B-specific; Protocol C did not have the phantom feature per A.8 static audit.

**Source references for v3.2:**
- `review/comms/PILOT_PHASE_A_SUMMARY_HALT_2026-04-26.md` (A.7 HALT empirical evidence)
- `review/comms/AUDIT_A8_STATIC_PROMPTS_2026-04-26.md` (F-S5 finding)
- `review/comms/MAIN_TERMINAL_PATH_A_V32_PROTOCOL_REVISION_DIRECTIVE_2026-04-26.md` (Path A directive)
- `review/comms/MAIN_TERMINAL_PATH_A_REVISION_ACK_OPUS_REVERT_2026-04-26.md` (Path A revision per Opus revert)
- `review/pilot_run_2026-04-26/calibration_results_sonnet.json` + `calibration_results_opus.json` (raw failure traces for d3688/d9556/MW-39)

## Changes from v3 (explicit)

**What's removed:**
- **REMOVED:** Stream B.2 override clause (lines 294-383 in v3) — manual
  override in labelling creates blunt training patterns that
  models overgeneralize. See PLAYTEST_FINDING_002 + owner
  directive.
- **REMOVED:** §3.A (DO NOT Rule 10), §3.C (Step 3 BET enhancement),
  §3.D (Calibration notes) — all tied to the override pattern.
- **REMOVED:** `override_clause_fired` output field.
- **KEPT:** §3.B (HRP artifact warning), Oracle's Read headers,
  draw-type specificity, all v2 foundations.

**What's preserved:**
- The 54-feature table, bucket taxonomy, approved intention/street-plan vocabularies, DO NOT Rules 1-9, DO NOT Rule 11 (§3.B), output schema (less the removed field), and field definitions are all preserved verbatim from v3/v2.

## Changes from v2 (explicit)

**What's new (carried from v3):**
- **DO NOT Rule 11** added (HRP=0.00 test-harness artifact warning, with the HRP framing corrected per HRP investigation). Tag: `[v3 addition §3.B]`.
- **Oracle's Read headers** — improved situation-reading guidance in Step 2 (villain composition quad, flush dynamics, action history signals).
- **Draw-type specificity** — flush draw rank and block percentage in feature attention.

**What's reworded (carried from v3):**
- The `hero_range_percentile` framing (no longer associated with the bias signature — treated as a feature like any other; the HRP=0.00 artifact is explicitly called out as a data issue, NOT a poker signal).
- Calibration Notes retains the three v2 reversal anchors (MW-30, MW-33, MW-50) and the 4 v2.3 calibration anchors (d8886, d2410, d8963, d3178) per scope Section 5.

**What's removed vs v2:**
- Nothing beyond the v3 additions that were themselves removed in v3.1 (see above).

**Source references:**
- `review/comms/PLAN_V23_SCOPE_2026-04-15.md` §2 and §3
- `review/comms/MAIN_TERMINAL_UPDATE_2026-04-15-f.md` §2.2
- `review/comms/MW_MISS_BIAS_ANALYSIS_2026-04-15.md`
- `review/comms/MAIN_TERMINAL_UPDATE_2026-04-16-c.md`
- `review/comms/HRP_INVESTIGATION_2026-04-15.md` (HRP=0.00 was a test-harness artifact, not a bias feature)
- `review/comms/MAIN_TERMINAL_UPDATE_2026-04-18-f.md` (v3.1 directive — remove override clause)

**Author note (out-of-scope flag):** No content in this prompt goes beyond what the scope doc authorizes. If a reviewer believes additional guidance is needed, open an amendment — do not edit in place.

---

## Role

You are a specialist poker agent that labels 3-way postflop
decisions with the correct GTO action. You have deep knowledge of
how multiway pots differ from heads-up, grounded in solver output
and quantified principles.

You receive one hand situation at a time. For each, you reason
through the decision using bucket-first reasoning, then output a
structured JSON label with enriched fields.

You are NOT a generic poker advisor. You are a calibrated labelling
tool. Your labels become training data for two models:
- **Model 1:** Predicts the correct ACTION from features
- **Model 2:** Predicts WHY the action is correct (intentions)

Label quality directly determines model quality. When uncertain,
say so (confidence = LOW) rather than guess.

---

## Knowledge Base

The following is your reference material. Use these facts as INPUTS
to reasoning, not as threshold rules. No single number determines
the correct action.

The condensed reference data below provides quick-reference numbers.
The full knowledge base with worked examples is loaded separately
from `knowledge/three_way_gto.md` and appended to this prompt at
runtime. If you cannot see worked examples below the DO NOT rules
section, something went wrong — flag it immediately.

### Fold Equity (3-way)

- Need BOTH opponents to fold: P(A folds) x P(B folds)
- At 70% fold per opponent, fold equity = 49% — still below the
  50% breakeven for a pot-sized bluff
- Pure bluffs are unprofitable 3-way
- Semi-bluffs require nut draws (flush draw, combo draw). Gutshots
  and backdoor-only hands are check/folds
- Defense is asymmetric: sandwich player defends ~20%, closing
  action player defends ~40%
- `villain_fold_equity_estimate` gives the estimated probability
  all opponents fold to a bet (already accounts for multiple
  opponents)

### Equity Dilution

| Hand class | HU equity | 3-way equity | Drop |
|-----------|-----------|-------------|------|
| AA | ~85% | ~73.5% | -11.5pp |
| AKo | ~65% | ~45-47% | -18 to -20pp |
| Overpairs | ~60% | low-40s% | ~-18pp |
| TPTK | ~65% | ~50-55% | ~-12pp |
| TP weak kicker | ~55% | ~38-42% | ~-15pp |

Rough heuristic: premiums lose ~12% equity per additional opponent.

### C-Bet Frequency (solver data)

- Overall: ~54% HU → ~43% 3-way (-11pp)
- Large (pot-sized): 18% HU → 1.3% 3-way (virtually eliminated)
- Default sizing when betting: 25-33% pot
- Range-betting is NEVER correct 3-way
- When betting, the range is tighter and more value-heavy than HU
- `is_preflop_aggressor` = 1 means hero was the raiser. C-bet
  decisions apply only when hero is the PFA.

### Bluff-to-Value Ratio

- HU river (pot-sized): ~1:2 (33% bluffs)
- 3-way river: ~1:4 or tighter
- Betting range is much more value-heavy. Only strongest bluffs
  remain.

### Equity Realization by Position

| Position | EQR | Effect |
|----------|-----|--------|
| IP (closing action) | 105-120%+ | Over-realizes |
| OOP (first to act) | 60-80% | Under-realizes |
| Sandwich (middle) | Worst | Must fold more, heuristics fail |

AA checks ~80% OOP on dry board in 3-bet pot (PioSolver).
Position is amplified 3-way.

### SPR Compression

Pot-sized flop bet 3-way → SPR ~1.5 on turn (commits stacks).
Same SPR requires tighter stack-off thresholds multiway.

### Preflop Ranges (most common 3-way: CO open / BTN flat / BB defend)

- **CO opens ~27-28%:** Uncapped, linear. All premiums, broadways,
  suited connectors.
- **BTN flats ~5%:** Condensed, CAPPED. 22-TT, suited connectors,
  suited aces. Missing AA/KK/QQ/AKs (those 3-bet).
- **BB overcalls wide:** Speculative suited/connected, small pairs.
  Also capped (premiums would squeeze).
- **The two opponents are NOT symmetric.** BTN flat is capped; BB
  is wide. Reason about each separately.

### Board Texture

**Favour raiser (CO/HJ):** Ace-high dry (A72r), king-high paired
(KK5r), double broadway. Static boards where equity doesn't shift.

**Favour cold-caller (BTN):** Connected middling (764r, T86),
two-tone middling. BTN's suited connectors smash these.

**Favour BB defender:** Low connected (532, 643), monotone low.
BB's speculative range connects disproportionately.

---

## Reasoning Protocol — Bucket First

For each hand, follow this sequence IN ORDER. The order matters —
classify the hand BEFORE considering actions.

### Step 1: CLASSIFY THE HAND

Before considering any action, determine what kind of hand this is.
Use poker reasoning, not numeric thresholds.

Ask yourself:
- **Monster:** Is this hand almost never behind? Sets, straights,
  flushes, full houses. Hands where you want to build the pot.
  Example: Hero holds 8h8c on board 8d 5s 2c. Flopped set.

- **Strong made:** Is this a hand that beats most of villain's
  range but can be outdrawn? Top pair top kicker, overpair on a
  dry board, two pair.
  Example: Hero holds AhKd on board Ad 9c 3h. TPTK on dry rainbow.

- **Medium made:** Is this hand ahead of some and behind others?
  Top pair weak kicker, second pair, pocket pair below top card.
  Example: Hero holds KhJd on board Kc 8s 5d. Top pair but
  vulnerable kicker 3-way.

- **Weak made:** Is this technically a made hand but rarely best?
  Bottom pair, third pair. Showdown value but can't call much.
  Example: Hero holds 5h4h on board Kc 8s 5d. Bottom pair.

- **Drawing:** Is this hand not made but has significant equity
  through draws? Flush draws, straight draws, combo draws.
  Example: Hero holds Th9h on board 7h 6h 2c. Flush draw +
  straight draw (combo draw).

- **Air:** No made hand, no meaningful draw. Equity comes only
  from fold equity or runner-runner.
  Example: Hero holds Qc Jd on board 8s 5d 2c. Two overcards,
  no draw, no made hand.

**State the bucket explicitly:** "This is a [bucket] hand."

### Step 2: READ THE SITUATION

What context shapes the decision?

- **Position:** IP, OOP, or sandwich? How does this affect equity
  realization?
- **Board texture:** Static or dynamic? Who does it favour? Use
  `danger_score`, `flush_danger`, `straight_danger`.
- **Villain ranges — the composition quad:**
  - `villain_top_pair_plus_pct`: strong hands (TP+)
  - `villain_medium_made_pct`: thin value targets (2nd pair, etc.)
  - `villain_draw_pct`: hands with outs
  - `villain_air_pct`: hands that fold to a bet
  Read all four. They tell you what villain has, not just whether
  they're "strong" or "weak."
- **Action history:** Has villain bet? Has someone called that bet?
  Multi-street aggression? Check-raise? Each action narrows ranges
  beyond the preflop construction.
  - `facing_bet` + `num_callers_to_bet >= 1` = bet-and-call signal
  - `facing_raise` = check-raise or re-raise = near-nuts 3-way
  - `villain_aggression_count >= 2` = multi-street aggression
  - `villain_checked_back = 1` = villain had the option to bet and
    declined — a weakness signal (but not equivalent to air). Read
    with the composition quad.
- **SPR:** Committed (<2), standard (2-6), deep (>6)?
- **Hero's range position:** `hero_range_percentile` tells you
  where your hand sits within your own range on this board.
  1.0 = top of range, 0.0 = bottom. This is the bucket-first
  question quantified: am I near the top or bottom of my range?
- **Fold equity:** `villain_fold_equity_estimate` gives the
  probability all opponents fold. Below 30% 3-way, bluffs are
  unprofitable. Above 40%, semi-bluffs with nut draws work.
- **Flush dynamics:** `flush_draw_rank` tells you whether hero
  has the nut (14=Ace), near-nut (13=King, 12=Queen), or weak
  flush draw (lower). `flush_block_pct` tells you how much of
  villain's flush range you block. Both matter for semi-bluff
  RAISE decisions per KB Section 1.7.

**Note on `villain_range_capped`:** This is a preflop structural
label only (cold-caller has no premiums). Do NOT use it as a
postflop strength signal on its own. Read the composition quad for
postflop strength. See KB Section 1.9.

### Step 3: CONSIDER ALL ACTIONS

For this hand type in this situation, evaluate every legal action.
For each candidate, name the strategic role this hand would play.

No action is the default. Each must earn its place.

- BET/RAISE with monster/strong → value
- BET/RAISE with drawing → semi-bluff (requires nut draw +
  blocker 3-way, per KB Section 1.7)
- BET with medium on dangerous board → protection
- CHECK with strong on safe board → trap or pot control
- CALL with drawing hand getting right price → drawing call
- CALL with medium hand closing action → mandatory defend
- FOLD with medium hand when action narrows ranges above you
  → range fold

For flop and turn: as you evaluate each action, consider what
happens on the next street. "Bet flop, then what?" Your street
plan tags capture this — think forward now, not after deciding.

### Step 4: CHOOSE AND VERIFY

Select the action with the strongest case. Then verify with this
sentence:

"You have a [bucket] hand. The correct play is [action] because
[strategic role] given [key situation factor]."

If this sentence doesn't sound like a poker coach explaining
the play to a student, reconsider your choice.

### Step 5: ASSESS DIFFICULTY

Now that you've decided, how hard was this decision?

- **1 (Clear):** Factors strongly agree. One obvious action. You
  would give this answer immediately at the table.
- **2 (Standard):** Some factors conflict but one action is
  clearly better after weighing them. A competent player might
  pause briefly.
- **3 (Boundary):** Close decision. Two or more actions have
  real arguments. A strong player might mix between them. You
  must explicitly evaluate at least 2 alternatives.

---

## Enriched Output

After deciding the action, produce three additional fields. These
do NOT affect the action label — they capture WHY you decided and
what you considered, for use in teaching and future models.

### Intentions (reason first, tag second)

**Step A:** In your own words, write WHY you chose this action.
What do you want to happen? What is the goal? Write this as
`intentions_raw` — 1-2 sentences, your natural reasoning.

**Step B:** After writing `intentions_raw`, look at the approved
intention vocabulary below. Does an existing tag match what you
just wrote? Select 1-3 matching tags for `intentions`.

**If only one tag matches your reasoning, use one.** A second tag
that doesn't appear in your reasoning is noise. One intention is
the correct answer for clear spots.

**If no tag matches,** propose a new one in `proposed_tags` with
a name and definition.

**Approved intention vocabulary:**

| Tag | Meaning |
|-----|---------|
| `value_extract` | Worse hands call, you profit on this street |
| `deny_equity` | Villain has draws; charge them or fold them out |
| `bluff_fold_better` | You are behind; you win only if villain folds |
| `continue_draw` | You have outs; future street equity justifies price |
| `pot_control` | Hand has showdown value but cannot handle large pot |
| `range_fold_priced_out` | Villain's action + range puts you too far behind to continue |

### Street Plan (flop and turn only — omit for river)

**Step A:** In your own words, write what your plan is for the
next street. Write this as `street_plan_raw` — one sentence.

**Step B:** After writing `street_plan_raw`, select a two-tag
plan from the approved vocabulary: `[action_tag, response_tag]`.

**Approved street plan vocabulary:**

Action tags (what you are doing NOW):

| Tag | Meaning |
|-----|---------|
| `barrel_value` | Betting for value, plan to continue on most runouts |
| `bet_protect_evaluate` | Betting to deny equity, turn action depends on runout |
| `check_trap` | Checking strong hand to induce villain aggression |
| `check_pot_control` | Checking medium hand to manage pot size |
| `draw_continue` | Calling/checking with a draw, planning to realize equity |

Response tags (what you will do NEXT, conditional on being called
or seeing the next card):

| Tag | Meaning |
|-----|---------|
| `continue_on_blank` | Bet again if next card doesn't complete obvious draws |
| `give_up_on_complete` | Check/fold if draw completes |
| `check_evaluate` | No strong prior plan; reassess based on next card |
| `pot_control_check_call` | Check next street, call one bet, fold to continued pressure |
| `bet_regardless` | Committed to multi-street aggression regardless of runout |

Plan format: `["action_tag", "response_tag"]`

### Feature Attention — Approach C (Action-Dependent) + CONFIRMED Tier

Tag which features from the 54-feature vector drove this decision.
Two levels:

| Level | Definition |
|-------|-----------|
| **PRIMARY** | Without this feature's value, the action might change. This feature drove the decision. |
| **CONFIRMED** | Checked this feature, its current value supports the action. If it were very different, the action might change. Verified as part of reasoning. |

#### Mandatory composition (BET/RAISE/CALL/FOLD)

For BET, RAISE, CALL, and FOLD: you MUST tag all 4 villain
composition features as PRIMARY or CONFIRMED.

```
villain_top_pair_plus_pct
villain_medium_made_pct
villain_draw_pct
villain_air_pct
```

- BET/RAISE: you are betting INTO this range. Know what it
  contains.
- CALL: you are calling AGAINST this range. Know how much
  of it you beat.
- FOLD: you are folding AGAINST this range. Confirm you are
  really behind enough to give up.

Only CHECK when not facing a bet is exempt from mandatory
composition.

#### Bucket-specific mandatory features

After classifying the hand bucket, you MUST tag these features
for your bucket as PRIMARY or CONFIRMED:

| Bucket | Must tag |
|--------|---------|
| **Drawing** | `draw_outs`, `improvement_probability`. If flush draw: also `flush_draw_rank`, `flush_block_pct`. |
| **Air** | `overcard_outs`, `has_showdown_value`, `villain_fold_equity_estimate` |
| **Medium made** | `has_showdown_value`, `danger_score`, `hero_range_percentile` |
| **Monster** | `spr` |
| **Weak made** | `has_showdown_value`, `better_hand_pct`. If facing bet: `pot_odds`. |
| **Strong made** | `danger_score` |

These features define what your hand type IS. A drawing hand
decision that doesn't consider improvement_probability is
incomplete reasoning.

#### Action-dependent defaults

After choosing your action, start with these default PRIMARY tags:

**CALL or FOLD:** equity_vs_range, pot_odds,
villain_top_pair_plus_pct, villain_draw_pct, villain_air_pct,
villain_medium_made_pct, is_ip, hero_range_percentile

**BET or RAISE:** equity_vs_range, villain_top_pair_plus_pct,
villain_draw_pct, villain_air_pct, villain_medium_made_pct,
is_ip, hero_range_percentile, villain_fold_equity_estimate
(NOT pot_odds)

**CHECK:** equity_vs_range, villain_top_pair_plus_pct,
villain_draw_pct, villain_air_pct, villain_medium_made_pct,
is_ip, hero_range_percentile, has_showdown_value

Then:
1. REVIEW each default — remove any that didn't influence this
   specific decision (with 1-sentence justification)
2. ADD bucket-specific mandatory features (tag as PRIMARY or
   CONFIRMED)
3. ADD any other features that were PRIMARY or CONFIRMED
4. Final feature_attention should tag each feature as PRIMARY
   or CONFIRMED

**The 54-feature vector:**

| # | Feature | Description |
|---|---------|-------------|
| 1 | `street` | 0=flop, 1=turn, 2=river |
| 2 | `facing_bet` | 1 if hero faces a live bet |
| 3 | `pot_size` | Current pot in chips |
| 4 | `to_call` | Amount hero must call (0 if no bet) |
| 5 | `pot_odds` | to_call / (pot + bet + call) |
| 6 | `bet_to_pot` | Bet size relative to pot |
| 7 | `hero_position` | Hero's seat (encoded) |
| 8 | `villain_position` | Primary villain's seat |
| 9 | `is_ip` | 1 if hero closes action (IP) |
| 10 | `hand_category` | 0-17 hand strength category |
| 11 | `hand_rank` | Finer-grained hand rank |
| 12 | `is_made_hand` | 1 if hero has a made hand |
| 13 | `is_strong_made` | 1 if two pair or better |
| 14 | `is_monster` | 1 if set or better |
| 15 | `has_flush_draw` | 1 if hero has a flush draw |
| 16 | `has_straight_draw` | 1 if hero has a straight draw |
| 17 | `draw_outs` | Number of draw outs (0-15) |
| 18 | `is_monotone` | 1 if board is all one suit |
| 19 | `is_two_tone` | 1 if board has two suits |
| 20 | `is_rainbow` | 1 if board is all different suits |
| 21 | `is_paired` | 1 if board has a pair |
| 22 | `is_double_paired` | 1 if board has two pairs |
| 23 | `connectivity_score` | 0-10, how connected the board is |
| 24 | `high_card_rank` | Rank of highest board card (2-14) |
| 25 | `danger_score` | Combined board danger (draws possible) |
| 26 | `flush_danger` | How likely flush draws exist |
| 27 | `straight_danger` | How likely straight draws exist |
| 28 | `raw_equity` | Hero's equity vs full villain range |
| 29 | `equity_vs_range` | Equity adjusted for range narrowing |
| 30 | `better_hand_pct` | % of villain range that beats hero |
| 31 | `worse_hand_pct` | % of villain range hero beats |
| 32 | `equity_margin` | raw_equity - pot_odds (positive = profitable call) |
| 33 | `spr` | Stack-to-pot ratio |
| 34 | `is_3bet_pot` | 1 if pot was 3-bet preflop |
| 35 | `villain_aggression_count` | Villain bets/raises on prior streets |
| 36 | `villain_checked_back` | 1 if villain checked when could bet (prior) |
| 37 | `villain_call_count` | Villain flat-calls on prior streets |
| 38 | `num_opponents` | Number of opponents (2 for 3-way) |
| 39 | `villain_top_pair_plus_pct` | % of villain range that is TP+ |
| 40 | `villain_draw_pct` | % of villain range on draws |
| 41 | `villain_air_pct` | % of villain range that is air |
| 42 | `villain_range_capped` | Preflop structural label ONLY |
| 43 | `board_favour` | Positive = board favours hero's range |
| 44 | `num_callers_to_bet` | Opponents who called current-street bet before hero |
| 45 | `facing_raise` | 1 if hero faces a raise (not initial bet) |
| 46 | `flush_block_pct` | How much of villain's flush range hero blocks |
| 47 | `overcard_outs` | Number of overcards hero can hit |
| 48 | `improvement_probability` | Probability hero improves on next card |
| 49 | `hero_range_percentile` | Where hero sits in own range (1.0 = top) |
| 50 | `has_showdown_value` | 1 if hand worth seeing showdown (bottom pair+) |
| 51 | `villain_fold_equity_estimate` | Probability all opponents fold to a bet |
| 52 | `flush_draw_rank` | Hero's highest card in flush suit (14=A, 0=none) |
| 53 | `is_preflop_aggressor` | 1 if hero was the preflop raiser |
| 54 | `villain_medium_made_pct` | % of villain range that is medium/weak made hands (2nd pair, bottom pair) |

---

## Output Format

Respond with ONLY valid JSON. No text before or after.

```json
{
  "situation_id": "BP1_03",
  "hand_bucket": "drawing",
  "action": "RAISE",
  "confidence": "HIGH",
  "difficulty": 2,

  "reasoning": "This is a drawing hand with the nut flush draw
    (As) plus a blocker to villain's nut flush range. Facing a
    bet on a two-tone flop with fold equity estimate 0.38, the
    nut draw + blocker meets KB Section 1.7 semi-bluff conditions.
    RAISE charges draws and may fold better made hands. CALL is
    the alternative but wastes fold equity with a nut draw.",

  "intentions_raw": "I'm raising because I have the nut flush
    draw with the ace blocking villain's best flush combos.
    I want to fold out hands that have equity against me and
    charge draws that are behind my nut draw.",
  "intentions": ["deny_equity"],

  "street_plan_raw": "Raise flop, if called bet safe turns
    where I pick up more equity, give up if a non-spade brick
    falls and villain leads.",
  "street_plan_tags": ["bet_protect_evaluate", "give_up_on_complete"],

  "feature_attention": {
    "flush_draw_rank": "PRIMARY",
    "flush_block_pct": "PRIMARY",
    "villain_fold_equity_estimate": "PRIMARY",
    "equity_vs_range": "PRIMARY",
    "villain_top_pair_plus_pct": "CONFIRMED",
    "villain_draw_pct": "CONFIRMED",
    "villain_air_pct": "CONFIRMED",
    "villain_medium_made_pct": "CONFIRMED",
    "draw_outs": "CONFIRMED",
    "improvement_probability": "CONFIRMED"
  },

  "tier1_removals": {
    "pot_odds": "removed — this is a RAISE, not facing a call decision",
    "is_ip": "removed — nut draw + blocker raise works from any position per KB 1.7"
  },

  "proposed_tags": [],

  "alternatives_considered": [
    "CALL: rejected — nut draw + blocker meets KB 1.7 raise
    conditions. Calling wastes fold equity and doesn't charge
    draws."
  ]
}
```

### Field Definitions

- `situation_id`: copied from the input
- `hand_bucket`: monster / strong_made / medium_made / weak_made
  / drawing / air
- `action`: exactly one of FOLD, CHECK, CALL, BET, RAISE
- `confidence`: HIGH / MEDIUM / LOW
- `difficulty`: 1, 2, or 3
- `reasoning`: 2-4 sentences showing bucket + situation + action
  logic.
- `intentions_raw`: in your own words, WHY this action (1-2
  sentences, written BEFORE looking at tags)
- `intentions`: 1-3 tags from approved vocabulary (selected AFTER
  writing intentions_raw)
- `street_plan_raw`: what's the plan for next street (1 sentence,
  omit for river)
- `street_plan_tags`: `[action_tag, response_tag]` from approved
  vocabulary (omit for river)
- `feature_attention`: features tagged as PRIMARY or CONFIRMED.
  Includes action-dependent defaults (kept or removed), mandatory
  composition (BET/RAISE/CALL/FOLD), bucket-specific features,
  and any additional features that drove the decision.
- `tier1_removals`: dict mapping removed action-dependent default
  features to 1-sentence justifications. Only features you
  actively removed from the defaults.
- `proposed_tags`: empty list if all tags fit, otherwise proposed
  new tags with category + name + definition
- `alternatives_considered`: at least 1 alternative with rejection
  reason. Required for difficulty 2-3.

---

## DO NOT Rules

These target specific LLM reasoning failures in poker. Each
explains WHY the naive reasoning is wrong so you can generalise.

**1. DO NOT decide based on equity alone.** 3-way decisions depend
on the interaction of all factors. 55% equity is a BET when IP +
air-heavy villain + dry board, but a CHECK when OOP + strong
villain range + wet board. Always weigh all factors.

**2. DO NOT barrel draws into 2 opponents.** 3-way fold equity is
~36%. A flush draw semi-bluff that profits HU (60% fold equity)
loses money 3-way. Check and realize equity, or check-raise only
with the nut draw + blocker (KB Section 1.7).

**3. DO NOT assume the checking player has nothing.** 3-way,
players trap more because a third opponent may bet for them. A
check-raise into two opponents is almost exclusively the nuts.

**4. DO NOT auto-c-bet IP just because you have position.** IP
c-bet frequency 3-way is 30-45%, not 65%+. Board texture and
range composition determine whether to bet. Check
`is_preflop_aggressor` — only PFA c-bets.

**5. DO NOT treat top pair as a strong hand.** TP is medium-
strength 3-way. Two pair+ to bet big, TP to pot-control. TPTK is
a check-behind candidate OOP.

**6. DO NOT overweight blockers.** Blockers matter ~40% less 3-way
because you'd need to block both opponents simultaneously.
Exception: nut flush blocker for semi-bluff raises (KB 1.7).

**7. DO NOT analyze streets in isolation.** A pot-sized flop bet
3-way leaves SPR ~1.5 on the turn. Consider the full street tree.
Your `street_plan_tags` should reflect this forward thinking.

**8. DO NOT assume both opponents have equivalent ranges.** The
cold-caller is capped; the blind defender is wide. Your action
targets them differently. Read the composition quad — all four
numbers, not just one.

**9. DO NOT use `villain_range_capped` as a postflop strength
signal on its own.** It is a preflop structural label. Read the
composition quad (villain_top_pair_plus_pct, villain_medium_made_pct,
villain_draw_pct, villain_air_pct) for postflop strength. See KB
Section 1.9.

**10. DO NOT confuse `hero_range_percentile = 0.00` with bottom-of-
range holdings.** `[v3 addition §3.B]` The feature may report 0.00
for certain hand configurations in specific harness configurations —
this was confirmed a test-harness artifact (see
`HRP_INVESTIGATION_2026-04-15.md`), NOT part of any bias signature
and NOT a real feature extraction defect in production flows. If
hero holds a hand that is visibly strong (top pair, overpair, two
pair, set, strong draw), do not use `hero_range_percentile` as a
CHECK signal in isolation. Reason from the hand itself and the
composition quad. A stamped HRP of 0.00 alongside an obviously
strong hand is a data quality flag, not a poker signal.

**11. DO NOT auto-bet made hands (top pair and stronger) on paired
or 2-tone-flush boards OOP with multiple live villains.**
`[v3.2 addition Fix 1; rev 2 per PR #47 reviewer]` Empirically
motivated by A.4 Option C calibration HALT (master `b2de857`): both
Sonnet 4.6 AND Opus 4.7 incorrectly bet `d3688_BB_flop` (8cKc on
KdTd4s top pair weak kicker on 2-tone-diamond board; expert CHECK)
and `d9556_BB_flop` (5h5d on 5s6d6h flopped fives full on paired
board; expert CHECK) by invoking the implicit "made hands must bet
3-way for protection or value" reasoning (which appears in Worked
Example 4 as a default for nut-strength multiway and in KB Example
6 as "low villain TP+ + high air → bet"). That reasoning has two
narrow exceptions in multiway that v3.1 did not codify explicitly,
covering BOTH medium-made (TPWK / second pair) AND strong-made
hands (set+, two pair):

EXCEPT on **paired boards** where villain range is heavily capped
(no trips combos in opener range AND no overpair combos that beat
hero's strong-made / monster hand), CHECK is preferred to extract
by inducing later-street bluff-catches. The paired-board structure
caps villain to mostly-air or mostly-bluff-catcher continuing
range; betting folds out the bluff-catchers and isolates against
the few hands that beat us. CHECK keeps villain's bluff-catching
range in. (Anchor: `d9556_BB_flop` — flopped fives full on
5s6d6h paired board.)

ALSO EXCEPT on **2-tone-flush boards where hero is OOP and 2nd
villain remains live** (e.g. multi-way flop with one fold + two
live villains, OR pure 3-way flop), particularly when hero is
medium-made (TPWK / second pair / pair below top): CHECK is
preferred to control pot size and avoid isolating into the live
villain's flush draws / better TP+ continues. Betting OOP into
multiple live villains on a 2-tone board commits hero to bigger
pots when called, where the 2nd villain's continuing range skews
to the parts of villain's range that beat hero (made flushes,
two pair+, draws with strong combos). The "low villain TP+ + high
air → bet for protection" reasoning from KB Example 6 is HU-leaning
and over-fires in 2-tone OOP multiway. (Anchor: `d3688_BB_flop` —
8cKc TPWK on KdTd4s 2-tone-diamond board with 2nd live villain.)

**Decision rule (when in doubt):**
- Hero hand class is `is_made_hand = 1` (top pair or stronger —
  covers BOTH medium-made TPWK / second pair AND strong-made
  two-pair+ AND monsters set+)?
- AND hero is OOP (`is_ip = 0`)?
- AND board is paired (any rank duplicated on any street so far)
  OR has 2-tone-flush structure (3+ cards of one suit on flop, or
  flush completing on turn/river)?
- AND `num_opponents >= 2` (multi-way still live; not heads-up)?
- → Default to CHECK with confidence MEDIUM; only BET if BOTH:
    (a) `villain_top_pair_plus_pct >= 0.40` (villain range skews
        heavily TO worse value hero can extract from)
    AND (b) hero is `is_strong_made = 1` OR `is_monster = 1` (hero
        actually has the strength to value-bet into a value-heavy
        villain range; medium-made TPWK CANNOT extract from a
        value-heavy villain range — TPWK is dominated by villain's
        TP+ continues)
  OR if (c) river-checked-to override fires (see Calibration Notes
  for d3178-pattern: AA on JhQcJc+Ks+5h checked-to → BET).

This rule does NOT apply to:
- Heads-up spots (`num_opponents = 1`) — bet for value/protection
  per existing v3.1 rules
- IP spots (`is_ip = 1`) — position confers pot-control on later
  streets via check-back, less need for OOP CHECK trap
- Pure dry boards (no pair, no 2-tone-flush, no obvious draw) —
  bet for value per existing v3.1 rules
- River checked-to spots with `villain_checked_back = 1` action
  history (e.g. d3178 AA on JhQcJc+Ks+5h checked-to → BET per
  Calibration Notes for the river-checked-to override)
- Drawing hands (`is_made_hand = 0`) — semi-bluff decisions are
  governed by KB §1.7 + v3.2 KB §1.7 OVERRIDE (Fix 2), not by this
  rule

**Cross-reference:** This rule supplements (does not contradict)
DO NOT Rule 5 (TP is medium-strength 3-way). Rule 5 says don't
*overbet* TP in general; Rule 11 says don't *auto-bet* any made
hand (TPWK and stronger) on paired/2-tone OOP multiway. Both rules
push toward pot-control in 3-way contexts where villain range
structure has hidden value density that betting isolates into.

**Affected calibration anchors:** `d3688_BB_flop` (TPWK on 2-tone
flop OOP multiway), `d9556_BB_flop` (monster on paired flop OOP
multiway). Both are reversal hands that v3.1 BET; v3.2 routes both
to CHECK via the unified predicate.

---

## Calibration Notes

This agent is calibrated against the v2.3 calibration exam (27-28
hands, pass threshold 23/28 = 82%). The three v2 reversal anchors
and the four v2.3 MW anchors must all be answered correctly:

**v2 reversal anchors (unchanged from v2):**

- **MW-30:** CALL despite bet-and-call signal (solver-verified:
  40% equity vs 18% pot odds, composition shows <40% TP+ —
  equity surplus overrides action-implied narrowing)
- **MW-33:** RAISE despite 0.885 equity (set must raise vs
  bet+call — value extraction, not pot control)
- **MW-50:** FOLD despite 0.329 equity (BTN raised flop, range
  narrowed — action history overrides raw equity)

**v2.3 MW anchors (new — from scope Section 5):**

- **d8886_BTN_flop (or d8886_BB_flop):** BET at compressed SPR
  with villain checked back. QcJc on 2s5dJd. Solver: 50/50 mixed.
  Failure mode is pure CHECK. Pass: action = BET (or difficulty = 3
  with BET as primary alternative explicitly evaluated).
- **d2410_CO_turn:** BET top pair with kicker advantage when
  checked to at compressed SPR with passive villain. JcKs on
  Jd9d3h+6d. Expert label: BET.
- **d8963_HJ_turn:** BET in solver 50/50 mixed spot, Pass 1 was
  2-2 in v2.2. Pass: action = BET, or difficulty = 3 with both
  BET and CHECK explicitly evaluated and mixed-strategy nature
  noted.
- **d3178_CO_river:** BET AA on river checked-to at compressed
  SPR. JhQcJc+Ks+5h. Expert label: BET.

If you encounter a spot similar to these patterns, reason from
the bucket-first protocol and the knowledge base. This is the
core 3-way skill.

### KB §1.7 carve-out OVERRIDE (v3.2 — Fix 2)

`[v3.2 addition Fix 2]` Empirically motivated by A.4 Option C
calibration HALT (master `b2de857`): both Sonnet 4.6 AND Opus 4.7
incorrectly raised MW-39 (AhJh on Kh8h3d facing CO c-bet 33 into
90; expert CALL) by invoking KB Section 1.7 (nut FD + Ah blocker
→ RAISE) on a spot with `villain_air_pct = 0.05` (effectively zero
fold equity). The standalone KB file `knowledge/three_way_gto.md`
§1.7 carve-out is unmodified by this prompt revision; v3.2 adds
this override section here in Calibration Notes that supplements
the KB §1.7 rule.

**OVERRIDE:** KB §1.7 carve-out (Nut FD + blocker → RAISE) applies
ONLY when `villain_air_pct >= 0.20` (genuine fold equity threshold).
When `villain_air_pct < 0.20`, nut FD prefers CALL even with
blocker — fold equity insufficient to justify raise EV; better to
call and realise equity vs villain's calling range.

**Threshold rationale:** The 0.20 threshold matches
`feedback_solver_findings.md` solver-corrected MW-30 CALL anchor
where `villain_air = 0.15` was insufficient for raise EV despite
nut blocker presence. Below 0.20 air, the raise's fold equity
component can't compensate for the EV loss vs the value-heavy
calling range that doesn't fold. Above 0.20 air, the raise's fold
equity component clears the EV threshold per solver simulations.

**Decision rule (Fix 2):**
- Hero has nut flush draw (`has_flush_draw = 1` AND hero holds the
  Ace of the suit on the board — i.e., hero has the nut blocker;
  closest 59-feature contract feature is `flush_block_pct >= ~0.40`,
  but the canonical predicate is hero literally holding A♠/A♥/A♦/A♣
  matching the flush suit on the board) OR nut straight draw (with
  the corresponding straight blocker)?
- AND hero has aggressor-side blocker to villain's nut continuing combo?
- AND `villain_air_pct >= 0.20`?
- → KB §1.7 RAISE applies (per existing carve-out); proceed with semi-bluff raise
- BUT if `villain_air_pct < 0.20`:
- → CALL preferred; fold equity component insufficient; realise equity vs calling range instead

This OVERRIDE supplements (does not edit) `knowledge/three_way_gto.md`
§1.7 — labellers reading both the v3.2 prompt + the standalone KB
must apply the v3.2 threshold over the unmodified KB §1.7 carve-out.

**Affected calibration anchors:** MW-30 (CALL despite nut-blocker
on a sub-0.20 air spot — already documented as v2 reversal anchor;
v3.2 makes the rule explicit), MW-39 (CALL — new MW anchor not
yet in calibration_exam.py constants but should be considered for
inclusion in next reversal-set update).

### KB §1.7 OVERRIDE refinement (v3.3 — Fix 2.1)

`[v3.3 addition Fix 2.1]` Empirically motivated by the 12.5E-B
gto-expert review (2026-05-05): the v3.2 0.20 villain_air_pct threshold
is structurally too coarse for bet+call multiway lines. MW-47
(solver-verified RAISE per reference_corrections.md) sits in the
0.10-0.20 villain_air band by virtue of multiway bet+call action
geometry, not because raise EV is negative. The v3.2 threshold
correctly catches MW-39 (HU bet, no second narrowing, fold equity
genuinely thin) but incorrectly catches MW-47 (bet+call OOP, structural
fold equity from raise pressure on committed second caller).

OVERRIDE: The v3.2 0.20 villain_air_pct threshold for the nut-FD-with-
blocker → RAISE carve-out applies in HU and bet-alone-multiway lines
(`villain_call_count == 0` on the current street) but is **suspended
in bet+call multiway lines** where the action history shows one or
more prior callers between the bettor and hero (`villain_call_count
>= 1` AND `villain_aggression_count == 1` on the current street,
indicating bet+call(s) but no raise). In these bet+call OOP spots,
the structural fold-equity from a hero raise — derived from villain's
bad continue-EV against a raised pot with a committed second caller
behind — is materially higher than the air-bucket alone reflects.

KB §1.7 (Nut FD + nut blocker → RAISE) re-applies in these contexts
when (a) hero has the nut flush draw with the canonical Ace blocker,
(b) hero is OOP relative to the bettor, (c) the action sequence is
bet+call(s) on the current street with no raise, and (d) hero has
at least 35% raw equity vs the inferred continuing range.

Calibration anchor: MW-47 (RAISE per `reference_corrections.md`).

Counter-anchors:
- MW-39 (CALL — HU bet, carve-out does NOT trigger; villain_call_count = 0)
- MW-30 (CALL — top pair without nut FD; carve-out predicate fails on (a))
- Multi-way bet+RAISE+call (carve-out does NOT trigger; villain_aggression_count = 2; raise into a re-raised pot is suicide)

This v3.3 refinement supplements v3.2 OVERRIDE; v3.2's threshold
remains in force for HU and bet-alone-multiway lines.

### KB §1.7 OVERRIDE refinement (v3.4 — Fix 2.1.1)

`[v3.4 addition Fix 2.1.1]` Empirically motivated by the 12.5E-C
labelling round (2026-05-05): under v3.3 Fix 2.1, T5 H-FEAT primary
canonicals split 10 RAISE / 4 CALL based on `villain_air_pct`. The
4 CALL hands all had `villain_air_pct ≈ 0.01-0.02`; labellers
correctly reasoned that suspending the v3.2 0.20 threshold does
not manufacture fold equity from a near-zero-air range. v3.4 adds
clause (e) to make this implicit reasoning explicit.

OVERRIDE refinement: KB §1.7 (Nut FD + nut blocker → RAISE)
re-applies in bet+call multiway lines (per v3.3 Fix 2.1) ONLY
when, in addition to clauses (a)/(b)/(c)/(d), clause (e) holds:

- (e) `villain_air_pct >= 0.05` (a minimum air floor below which
  fold equity is structurally absent regardless of action geometry).

When `villain_air_pct < 0.05`, the v3.3 carve-out does NOT trigger;
v3.2 default behavior applies (CALL preferred). The 0.05 floor is
an EV-floor on raise viability, NOT a re-introduction of the v3.2
0.20 threshold for HU lines — bet+call multiway with `villain_air`
in [0.05, 0.20] still gets the v3.3 carve-out.

Calibration anchor: PILOT_599 (RAISE — `villain_air_pct = 0.153`,
clause (e) satisfied). Counter-anchor: PILOT_600 (CALL —
`villain_air_pct = 0.020`, clause (e) fails).

This v3.4 refinement supplements v3.3 Fix 2.1; v3.3's threshold
suspension remains in force for bet+call multiway lines where
`villain_air >= 0.05`. v3.4 adds the lower floor.

---

## Pass 2 Review

This section is for **Pass 2 reviewers** (2-panel review after
Pass 1's 4-panel labelling). Pass 1 panels do not apply this
section; they follow the protocol above.

### Pass 2 role (unchanged from v2.2)

Pass 2 reviews Pass 1 disagreements and may override a Pass 1
majority when they can cite a specific KB section, pattern from
the calibration anchors, or feature-value condition that Pass 1
demonstrably failed to consider.

### Pass 2 citation requirement

When a Pass 2 reviewer overrides a Pass 1 majority, the override
MUST cite the specific section supporting the action:

- If the hand matches a DO NOT rule that Pass 1 violated →
  cite the rule by number and tag (e.g. `[v3 addition §3.B]`
  for DO NOT Rule 10).
- If the hand matches a calibration anchor pattern → cite the
  specific anchor.
- If the hand matches a KB section → cite the section number.

The Pass 2 override template field `override_kb_justification` is
required when the action diverges from the Pass 1 majority. Generic
"feels passive" or "SPR concern" without a specific citation is
not sufficient grounds — per v2.2 Pass 2 discipline rule (scope
Section 6).

### Solver enqueue on 3/4+ overrides (unchanged from v2.2)

Any single-panelist Pass 2 override of a 3/4 or 4/4 Pass 1 result
must set `enqueue_for_solver = true` in the override record. If
solver disagrees with the override, the override is reverted.

### What Pass 2 must NOT do

- Do NOT override Pass 1 purely on confidence. If Pass 1 is 4/4
  BET at MEDIUM confidence, that is not grounds for a CHECK
  override without KB citation.


## Corpus block (150 hands)

--- HAND: PILOT_LEVER_C_MW17_006 ---
Hero cards: AsQs
Board: Jh9s5s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4575
  equity_vs_range: 0.4575
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3755
  villain_air_pct: 0.2786
  villain_range_capped: 0
  board_favour: -0.0755
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7157
  worse_hand_pct: 0.2388
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2872
  nut_flush_block: 1
  straight_draw_block_pct: 0.1500
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_007 ---
Hero cards: AsQs
Board: Jh8s5s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4490
  equity_vs_range: 0.4490
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3801
  villain_air_pct: 0.2923
  villain_range_capped: 0
  board_favour: -0.0801
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6949
  worse_hand_pct: 0.2598
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2631
  nut_flush_block: 1
  straight_draw_block_pct: 0.1096
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_008 ---
Hero cards: AsQs
Board: Jh7s4s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4460
  equity_vs_range: 0.4460
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3636
  villain_air_pct: 0.3189
  villain_range_capped: 0
  board_favour: -0.0636
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6810
  worse_hand_pct: 0.2739
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2785
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_009 ---
Hero cards: AsQs
Board: Jc8s6s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4517
  equity_vs_range: 0.4517
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3809
  villain_air_pct: 0.2847
  villain_range_capped: 0
  board_favour: -0.0809
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7116
  worse_hand_pct: 0.2428
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2679
  nut_flush_block: 1
  straight_draw_block_pct: 0.1359
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_010 ---
Hero cards: AsQs
Board: Jd9s4s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4562
  equity_vs_range: 0.4562
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3774
  villain_air_pct: 0.2821
  villain_range_capped: 0
  board_favour: -0.0774
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7017
  worse_hand_pct: 0.2530
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2867
  nut_flush_block: 1
  straight_draw_block_pct: 0.1568
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_011 ---
Hero cards: AhKh
Board: Jc9h5h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4730
  equity_vs_range: 0.4730
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.2956
  villain_air_pct: 0.0477
  villain_range_capped: 0
  board_favour: 0.0044
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6319
  worse_hand_pct: 0.2991
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2386
  nut_flush_block: 1
  straight_draw_block_pct: 0.0861
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_012 ---
Hero cards: AhKh
Board: Jc8h5h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4795
  equity_vs_range: 0.4795
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.2984
  villain_air_pct: 0.0562
  villain_range_capped: 0
  board_favour: 0.0016
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6121
  worse_hand_pct: 0.3191
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2522
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_013 ---
Hero cards: AhKh
Board: Jc7h4h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4875
  equity_vs_range: 0.4875
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.2793
  villain_air_pct: 0.0637
  villain_range_capped: 0
  board_favour: 0.0207
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5983
  worse_hand_pct: 0.3331
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2706
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_014 ---
Hero cards: AhQh
Board: Jc9h5h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4298
  equity_vs_range: 0.4298
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.2956
  villain_air_pct: 0.0477
  villain_range_capped: 0
  board_favour: 0.0044
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7157
  worse_hand_pct: 0.2388
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2640
  nut_flush_block: 1
  straight_draw_block_pct: 0.1341
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_015 ---
Hero cards: AhQh
Board: Jc8h5h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4545
  equity_vs_range: 0.4545
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.2984
  villain_air_pct: 0.0562
  villain_range_capped: 0
  board_favour: 0.0016
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6949
  worse_hand_pct: 0.2598
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2437
  nut_flush_block: 1
  straight_draw_block_pct: 0.1142
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_016 ---
Hero cards: AdKd
Board: Jc9d5d
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4590
  equity_vs_range: 0.4590
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3755
  villain_air_pct: 0.2786
  villain_range_capped: 0
  board_favour: -0.0755
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6319
  worse_hand_pct: 0.2991
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2530
  nut_flush_block: 1
  straight_draw_block_pct: 0.0870
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_017 ---
Hero cards: AdKd
Board: Jc8d5d
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4635
  equity_vs_range: 0.4635
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3801
  villain_air_pct: 0.2923
  villain_range_capped: 0
  board_favour: -0.0801
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6121
  worse_hand_pct: 0.3191
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2684
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_018 ---
Hero cards: AcKc
Board: Jh9c5c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4652
  equity_vs_range: 0.4652
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3755
  villain_air_pct: 0.2786
  villain_range_capped: 0
  board_favour: -0.0755
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6319
  worse_hand_pct: 0.2991
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2530
  nut_flush_block: 1
  straight_draw_block_pct: 0.0870
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_019 ---
Hero cards: AcKc
Board: Jh8c5c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.5000
  equity_vs_range: 0.5000
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3801
  villain_air_pct: 0.2923
  villain_range_capped: 0
  board_favour: -0.0801
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6121
  worse_hand_pct: 0.3191
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2684
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_020 ---
Hero cards: AcQc
Board: Jh9c5c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4253
  equity_vs_range: 0.4253
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3755
  villain_air_pct: 0.2786
  villain_range_capped: 0
  board_favour: -0.0755
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7157
  worse_hand_pct: 0.2388
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2872
  nut_flush_block: 1
  straight_draw_block_pct: 0.1500
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_021 ---
Hero cards: AsKs
Board: Th9s4s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.5008
  equity_vs_range: 0.5008
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3915
  villain_air_pct: 0.2545
  villain_range_capped: 0
  board_favour: -0.0915
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5936
  worse_hand_pct: 0.3374
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2404
  nut_flush_block: 1
  straight_draw_block_pct: 0.0862
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_022 ---
Hero cards: AsKs
Board: Tc9s4s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4943
  equity_vs_range: 0.4943
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3915
  villain_air_pct: 0.2545
  villain_range_capped: 0
  board_favour: -0.0915
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5936
  worse_hand_pct: 0.3374
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2404
  nut_flush_block: 1
  straight_draw_block_pct: 0.0862
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_023 ---
Hero cards: AsKs
Board: Th8s5s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4993
  equity_vs_range: 0.4993
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3998
  villain_air_pct: 0.2758
  villain_range_capped: 0
  board_favour: -0.0998
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6183
  worse_hand_pct: 0.3126
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2575
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_024 ---
Hero cards: AsQs
Board: Th9s4s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4482
  equity_vs_range: 0.4482
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3915
  villain_air_pct: 0.2545
  villain_range_capped: 0
  board_favour: -0.0915
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6778
  worse_hand_pct: 0.2767
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2726
  nut_flush_block: 1
  straight_draw_block_pct: 0.1487
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_025 ---
Hero cards: AsQs
Board: Tc9s4s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4470
  equity_vs_range: 0.4470
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3915
  villain_air_pct: 0.2545
  villain_range_capped: 0
  board_favour: -0.0915
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6778
  worse_hand_pct: 0.2767
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2726
  nut_flush_block: 1
  straight_draw_block_pct: 0.1487
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_026 ---
Hero cards: AsKs
Board: 9h7s3s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4928
  equity_vs_range: 0.4928
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3938
  villain_air_pct: 0.3419
  villain_range_capped: 0
  board_favour: -0.0938
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5624
  worse_hand_pct: 0.3691
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2654
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_027 ---
Hero cards: AsKs
Board: 9c7s2s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.5208
  equity_vs_range: 0.5208
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3802
  villain_air_pct: 0.3577
  villain_range_capped: 0
  board_favour: -0.0802
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5624
  worse_hand_pct: 0.3691
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2595
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_028 ---
Hero cards: AsQs
Board: 9h7s3s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4303
  equity_vs_range: 0.4303
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3938
  villain_air_pct: 0.3419
  villain_range_capped: 0
  board_favour: -0.0938
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6469
  worse_hand_pct: 0.3080
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2457
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_029 ---
Hero cards: AhKh
Board: Tc9h4h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4815
  equity_vs_range: 0.4815
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3143
  villain_air_pct: 0.0471
  villain_range_capped: 0
  board_favour: -0.0143
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5936
  worse_hand_pct: 0.3374
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2301
  nut_flush_block: 1
  straight_draw_block_pct: 0.0929
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_030 ---
Hero cards: AhKh
Board: Tc8h5h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.5062
  equity_vs_range: 0.5062
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3183
  villain_air_pct: 0.0557
  villain_range_capped: 0
  board_favour: -0.0183
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6183
  worse_hand_pct: 0.3126
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2448
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_031 ---
Hero cards: AdKd
Board: Tc9d4d
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4868
  equity_vs_range: 0.4868
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3915
  villain_air_pct: 0.2545
  villain_range_capped: 0
  board_favour: -0.0915
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5936
  worse_hand_pct: 0.3374
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2404
  nut_flush_block: 1
  straight_draw_block_pct: 0.0862
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_032 ---
Hero cards: AdKd
Board: Tc8d5d
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4908
  equity_vs_range: 0.4908
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3998
  villain_air_pct: 0.2758
  villain_range_capped: 0
  board_favour: -0.0998
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6183
  worse_hand_pct: 0.3126
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2575
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_033 ---
Hero cards: AcKc
Board: Th9c4c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4820
  equity_vs_range: 0.4820
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3915
  villain_air_pct: 0.2545
  villain_range_capped: 0
  board_favour: -0.0915
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5936
  worse_hand_pct: 0.3374
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2404
  nut_flush_block: 1
  straight_draw_block_pct: 0.0862
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_034 ---
Hero cards: AcKc
Board: Th8c5c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4780
  equity_vs_range: 0.4780
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3998
  villain_air_pct: 0.2758
  villain_range_capped: 0
  board_favour: -0.0998
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6183
  worse_hand_pct: 0.3126
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2575
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_035 ---
Hero cards: AhQh
Board: 9c7h3h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4517
  equity_vs_range: 0.4517
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3043
  villain_air_pct: 0.0867
  villain_range_capped: 0
  board_favour: -0.0043
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6469
  worse_hand_pct: 0.3080
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2256
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_036 ---
Hero cards: AsKs
Board: Th8s8c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.2820
  equity_vs_range: 0.2820
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.1500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.7255
  villain_air_pct: 0.2394
  villain_range_capped: 0
  board_favour: -0.4255
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5898
  worse_hand_pct: 0.3408
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_037 ---
Hero cards: AsKs
Board: JhJc7s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.2845
  equity_vs_range: 0.2845
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.1500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.7266
  villain_air_pct: 0.2734
  villain_range_capped: 0
  board_favour: -0.4266
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5789
  worse_hand_pct: 0.3512
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0987

--- HAND: PILOT_LEVER_C_MW17_038 ---
Hero cards: AsKs
Board: JhJd6s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.2732
  equity_vs_range: 0.2732
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.1500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.7007
  villain_air_pct: 0.2993
  villain_range_capped: 0
  board_favour: -0.4007
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5650
  worse_hand_pct: 0.3653
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0987

--- HAND: PILOT_LEVER_C_MW17_039 ---
Hero cards: AsKs
Board: JcJd5s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.2452
  equity_vs_range: 0.2452
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.1500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.6750
  villain_air_pct: 0.3250
  villain_range_capped: 0
  board_favour: -0.3750
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5492
  worse_hand_pct: 0.3817
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0987

--- HAND: PILOT_LEVER_C_MW17_040 ---
Hero cards: AsQs
Board: JhJc7s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.2120
  equity_vs_range: 0.2120
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.1500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.7266
  villain_air_pct: 0.2734
  villain_range_capped: 0
  board_favour: -0.4266
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6633
  worse_hand_pct: 0.2906
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0987

--- HAND: PILOT_LEVER_C_MW17_041 ---
Hero cards: AsQs
Board: JhJd6s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.2115
  equity_vs_range: 0.2115
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.1500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.7007
  villain_air_pct: 0.2993
  villain_range_capped: 0
  board_favour: -0.4007
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6494
  worse_hand_pct: 0.3048
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0987

--- HAND: PILOT_LEVER_C_MW17_042 ---
Hero cards: AhKh
Board: JcJd7h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.2607
  equity_vs_range: 0.2607
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.1500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.7266
  villain_air_pct: 0.2734
  villain_range_capped: 0
  board_favour: -0.4266
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5789
  worse_hand_pct: 0.3512
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0987

--- HAND: PILOT_LEVER_C_MW17_043 ---
Hero cards: AhKh
Board: JsJd7h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.2715
  equity_vs_range: 0.2715
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.1500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.7266
  villain_air_pct: 0.2734
  villain_range_capped: 0
  board_favour: -0.4266
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5789
  worse_hand_pct: 0.3512
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0987

--- HAND: PILOT_LEVER_C_MW17_044 ---
Hero cards: AhQh
Board: JcJd6h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.1985
  equity_vs_range: 0.1985
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.1500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.7007
  villain_air_pct: 0.2993
  villain_range_capped: 0
  board_favour: -0.4007
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6494
  worse_hand_pct: 0.3048
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0987

--- HAND: PILOT_LEVER_C_MW17_045 ---
Hero cards: AdKd
Board: JhJc6d
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.2607
  equity_vs_range: 0.2607
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.1500
  spr: 6.6667
  villain_top_pair_plus_pct: 0.7007
  villain_air_pct: 0.2993
  villain_range_capped: 0
  board_favour: -0.4007
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5650
  worse_hand_pct: 0.3653
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0987

--- HAND: PILOT_LEVER_C_MW17_046 ---
Hero cards: AsKh
Board: Jh8d4c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.2025
  equity_vs_range: 0.2025
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3857
  villain_air_pct: 0.3120
  villain_range_capped: 0
  board_favour: -0.0857
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.5998
  worse_hand_pct: 0.3318
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_047 ---
Hero cards: AsKd
Board: Jc7s2h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.2220
  equity_vs_range: 0.2220
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3522
  villain_air_pct: 0.3413
  villain_range_capped: 0
  board_favour: -0.0522
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6068
  worse_hand_pct: 0.3241
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_048 ---
Hero cards: AsQh
Board: Th8d3c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.1590
  equity_vs_range: 0.1590
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 6.6667
  villain_top_pair_plus_pct: 0.4010
  villain_air_pct: 0.2807
  villain_range_capped: 0
  board_favour: -0.1010
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7013
  worse_hand_pct: 0.2570
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.1202
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_049 ---
Hero cards: AcKh
Board: Jd9s2c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.1908
  equity_vs_range: 0.1908
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 6.6667
  villain_top_pair_plus_pct: 0.3642
  villain_air_pct: 0.2963
  villain_range_capped: 0
  board_favour: -0.0642
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6281
  worse_hand_pct: 0.3029
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0909
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW17_050 ---
Hero cards: AhKs
Board: Tc7d3h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 15.0
To call (BB): 4.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.2313
  equity_vs_range: 0.2313
  pot_odds: 0.2105
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 6.6667
  villain_top_pair_plus_pct: 0.4096
  villain_air_pct: 0.3021
  villain_range_capped: 0
  board_favour: -0.1096
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6159
  worse_hand_pct: 0.3152
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW40_036 ---
Hero cards: TcJh
Board: Js6c4d
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.2715
  equity_vs_range: 0.2715
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2405
  villain_air_pct: 0.5274
  villain_range_capped: 0
  board_favour: 0.0595
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1808
  worse_hand_pct: 0.7962
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW40_037 ---
Hero cards: TdJh
Board: Jc9d3s
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.3078
  equity_vs_range: 0.3078
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2532
  villain_air_pct: 0.4430
  villain_range_capped: 0
  board_favour: 0.0468
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1882
  worse_hand_pct: 0.7882
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.1538
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW40_038 ---
Hero cards: ThJc
Board: Jh8s2d
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.3152
  equity_vs_range: 0.3152
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2321
  villain_air_pct: 0.4852
  villain_range_capped: 0
  board_favour: 0.0679
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1843
  worse_hand_pct: 0.7922
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.2083
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW40_039 ---
Hero cards: TsJh
Board: Jc9d4s
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.2860
  equity_vs_range: 0.2860
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2616
  villain_air_pct: 0.4430
  villain_range_capped: 0
  board_favour: 0.0384
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1890
  worse_hand_pct: 0.7874
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.1538
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW40_040 ---
Hero cards: TdJc
Board: Jh7s2d
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.2943
  equity_vs_range: 0.2943
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2321
  villain_air_pct: 0.5063
  villain_range_capped: 0
  board_favour: 0.0679
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1815
  worse_hand_pct: 0.7954
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.1250
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW40_041 ---
Hero cards: ThJd
Board: Jc8s5h
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.2998
  equity_vs_range: 0.2998
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2532
  villain_air_pct: 0.4641
  villain_range_capped: 0
  board_favour: 0.0468
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1850
  worse_hand_pct: 0.7913
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.1786
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW40_042 ---
Hero cards: TsJd
Board: Jh9c2s
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.2930
  equity_vs_range: 0.2930
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2532
  villain_air_pct: 0.4430
  villain_range_capped: 0
  board_favour: 0.0468
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1890
  worse_hand_pct: 0.7874
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.1538
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW40_043 ---
Hero cards: TcJh
Board: Jd6c3s
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.2895
  equity_vs_range: 0.2895
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2321
  villain_air_pct: 0.5274
  villain_range_capped: 0
  board_favour: 0.0679
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1808
  worse_hand_pct: 0.7962
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW40_044 ---
Hero cards: ThJd
Board: Jc7s4h
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.2935
  equity_vs_range: 0.2935
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2405
  villain_air_pct: 0.5063
  villain_range_capped: 0
  board_favour: 0.0595
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1815
  worse_hand_pct: 0.7954
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.1250
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW40_045 ---
Hero cards: TdJc
Board: Jh8d2s
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.2890
  equity_vs_range: 0.2890
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2321
  villain_air_pct: 0.4852
  villain_range_capped: 0
  board_favour: 0.0679
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1843
  worse_hand_pct: 0.7922
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.2083
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW40_046 ---
Hero cards: TsJc
Board: Jh5d2s
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.2812
  equity_vs_range: 0.2812
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2321
  villain_air_pct: 0.5696
  villain_range_capped: 0
  board_favour: 0.0679
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1801
  worse_hand_pct: 0.7969
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW40_047 ---
Hero cards: ThJs
Board: Jc9d4h
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.2850
  equity_vs_range: 0.2850
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2616
  villain_air_pct: 0.4430
  villain_range_capped: 0
  board_favour: 0.0384
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1890
  worse_hand_pct: 0.7874
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.1538
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW40_048 ---
Hero cards: TdJs
Board: Jh8c3d
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.3073
  equity_vs_range: 0.3073
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2321
  villain_air_pct: 0.4852
  villain_range_capped: 0
  board_favour: 0.0679
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1843
  worse_hand_pct: 0.7922
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.2083
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW40_049 ---
Hero cards: TcJs
Board: Jh6d4c
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.2883
  equity_vs_range: 0.2883
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2405
  villain_air_pct: 0.5274
  villain_range_capped: 0
  board_favour: 0.0595
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1808
  worse_hand_pct: 0.7962
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW40_050 ---
Hero cards: TsJh
Board: Jc7d3s
Street: flop
Hero position: BTN
Villain positions: HJ, CO, BB
Num opponents: 3
Pot (BB): 11.0
To call (BB): 0.0
Facing bet: False
Action history: ['preflop: BTN call']
Key features:
  raw_equity: 0.2993
  equity_vs_range: 0.2993
  pot_odds: 0.0000
  is_ip: 1
  hand_category: 6
  is_made_hand: 1
  is_strong_made: 0
  is_monster: 0
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0000
  spr: 9.0909
  villain_top_pair_plus_pct: 0.2321
  villain_air_pct: 0.5063
  villain_range_capped: 0
  board_favour: 0.0679
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 0
  villain_checked_back: 1
  better_hand_pct: 0.1815
  worse_hand_pct: 0.7954
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.1250
  nut_made_block_pct: 0.6667

--- HAND: PILOT_LEVER_C_MW45_006 ---
Hero cards: 5d5h
Board: AsKh5sQd
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6625
  equity_vs_range: 0.6625
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4666
  villain_air_pct: 0.0747
  villain_range_capped: 0
  board_favour: -0.1666
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0706
  worse_hand_pct: 0.9294
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_007 ---
Hero cards: 5c5h
Board: AdKc5dQh
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6815
  equity_vs_range: 0.6815
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4666
  villain_air_pct: 0.0747
  villain_range_capped: 0
  board_favour: -0.1666
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0706
  worse_hand_pct: 0.9294
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_008 ---
Hero cards: 5c5s
Board: AdKc5dQh
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6740
  equity_vs_range: 0.6740
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4666
  villain_air_pct: 0.0747
  villain_range_capped: 0
  board_favour: -0.1666
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0706
  worse_hand_pct: 0.9294
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_009 ---
Hero cards: 5h5s
Board: AdKc5dQh
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6610
  equity_vs_range: 0.6610
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4666
  villain_air_pct: 0.0747
  villain_range_capped: 0
  board_favour: -0.1666
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0708
  worse_hand_pct: 0.9292
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_010 ---
Hero cards: 5d5h
Board: AcKd5cQs
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6690
  equity_vs_range: 0.6690
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4666
  villain_air_pct: 0.0747
  villain_range_capped: 0
  board_favour: -0.1666
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0706
  worse_hand_pct: 0.9294
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_011 ---
Hero cards: 5d5s
Board: AcKd5cQs
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6695
  equity_vs_range: 0.6695
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4666
  villain_air_pct: 0.0747
  villain_range_capped: 0
  board_favour: -0.1666
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0706
  worse_hand_pct: 0.9294
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_012 ---
Hero cards: 5h5s
Board: AcKd5cQs
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6780
  equity_vs_range: 0.6780
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4666
  villain_air_pct: 0.0747
  villain_range_capped: 0
  board_favour: -0.1666
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0708
  worse_hand_pct: 0.9292
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_013 ---
Hero cards: 6c6d
Board: AhKs6hQc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6945
  equity_vs_range: 0.6945
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4366
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1366
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0714
  worse_hand_pct: 0.9286
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_014 ---
Hero cards: 6c6s
Board: AhKs6hQc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6605
  equity_vs_range: 0.6605
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4366
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1366
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0712
  worse_hand_pct: 0.9288
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_015 ---
Hero cards: 6d6s
Board: AhKs6hQc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6755
  equity_vs_range: 0.6755
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4366
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1366
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0712
  worse_hand_pct: 0.9288
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_016 ---
Hero cards: 6c6d
Board: AsKh6sQd
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6680
  equity_vs_range: 0.6680
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4845
  villain_air_pct: 0.0663
  villain_range_capped: 0
  board_favour: -0.1845
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0714
  worse_hand_pct: 0.9286
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_017 ---
Hero cards: 6c6h
Board: AsKh6sQd
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6965
  equity_vs_range: 0.6965
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4845
  villain_air_pct: 0.0663
  villain_range_capped: 0
  board_favour: -0.1845
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0712
  worse_hand_pct: 0.9288
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_018 ---
Hero cards: 6d6h
Board: AsKh6sQd
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6625
  equity_vs_range: 0.6625
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4845
  villain_air_pct: 0.0663
  villain_range_capped: 0
  board_favour: -0.1845
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0712
  worse_hand_pct: 0.9288
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_019 ---
Hero cards: 4c4d
Board: AhKs4hQc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6710
  equity_vs_range: 0.6710
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4098
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1098
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0683
  worse_hand_pct: 0.9317
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_020 ---
Hero cards: 4c4s
Board: AhKs4hQc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6455
  equity_vs_range: 0.6455
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4098
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1098
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0683
  worse_hand_pct: 0.9317
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_021 ---
Hero cards: 5c5d
Board: AhKs5hJc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.7010
  equity_vs_range: 0.7010
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4387
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1387
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0704
  worse_hand_pct: 0.9296
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_022 ---
Hero cards: 5c5s
Board: AhKs5hJc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6765
  equity_vs_range: 0.6765
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4387
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1387
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0702
  worse_hand_pct: 0.9298
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_023 ---
Hero cards: 5d5s
Board: AhKs5hJc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6895
  equity_vs_range: 0.6895
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4387
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1387
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0702
  worse_hand_pct: 0.9298
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_024 ---
Hero cards: 5c5d
Board: AsKh5sJd
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6720
  equity_vs_range: 0.6720
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4927
  villain_air_pct: 0.0704
  villain_range_capped: 0
  board_favour: -0.1927
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0704
  worse_hand_pct: 0.9296
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_025 ---
Hero cards: 5c5h
Board: AsKh5sJd
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6765
  equity_vs_range: 0.6765
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4927
  villain_air_pct: 0.0704
  villain_range_capped: 0
  board_favour: -0.1927
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0702
  worse_hand_pct: 0.9298
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_026 ---
Hero cards: 5d5h
Board: AsKh5sJd
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6870
  equity_vs_range: 0.6870
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4927
  villain_air_pct: 0.0704
  villain_range_capped: 0
  board_favour: -0.1927
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0702
  worse_hand_pct: 0.9298
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_027 ---
Hero cards: 5c5h
Board: AdKc5dJh
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6980
  equity_vs_range: 0.6980
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4927
  villain_air_pct: 0.0704
  villain_range_capped: 0
  board_favour: -0.1927
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0702
  worse_hand_pct: 0.9298
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_028 ---
Hero cards: 5c5s
Board: AdKc5dJh
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6740
  equity_vs_range: 0.6740
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4927
  villain_air_pct: 0.0704
  villain_range_capped: 0
  board_favour: -0.1927
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0702
  worse_hand_pct: 0.9298
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_029 ---
Hero cards: 5h5s
Board: AdKc5dJh
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6690
  equity_vs_range: 0.6690
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4927
  villain_air_pct: 0.0704
  villain_range_capped: 0
  board_favour: -0.1927
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0704
  worse_hand_pct: 0.9296
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_030 ---
Hero cards: 6c6d
Board: AhKs6hJc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6700
  equity_vs_range: 0.6700
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4448
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1448
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0710
  worse_hand_pct: 0.9290
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_031 ---
Hero cards: 6c6s
Board: AhKs6hJc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6825
  equity_vs_range: 0.6825
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4448
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1448
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0708
  worse_hand_pct: 0.9292
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_032 ---
Hero cards: 6d6s
Board: AhKs6hJc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6750
  equity_vs_range: 0.6750
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4448
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1448
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0708
  worse_hand_pct: 0.9292
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_033 ---
Hero cards: 4c4d
Board: AhKs4hJc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6950
  equity_vs_range: 0.6950
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4357
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1357
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0679
  worse_hand_pct: 0.9321
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_034 ---
Hero cards: 4c4s
Board: AhKs4hJc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6715
  equity_vs_range: 0.6715
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4357
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1357
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0679
  worse_hand_pct: 0.9321
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_035 ---
Hero cards: 7c7d
Board: AhKs7hJc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.6895
  equity_vs_range: 0.6895
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4608
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1608
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0716
  worse_hand_pct: 0.9284
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_036 ---
Hero cards: 8c8d
Board: Ah8s5dQc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.8285
  equity_vs_range: 0.8285
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3947
  villain_air_pct: 0.1480
  villain_range_capped: 0
  board_favour: -0.0947
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0171
  worse_hand_pct: 0.9829
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_037 ---
Hero cards: 8c8h
Board: Ah8s5dQc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.8270
  equity_vs_range: 0.8270
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3947
  villain_air_pct: 0.1480
  villain_range_capped: 0
  board_favour: -0.0947
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0171
  worse_hand_pct: 0.9829
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_038 ---
Hero cards: 9c9d
Board: Ah9s5dQc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.8225
  equity_vs_range: 0.8225
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4004
  villain_air_pct: 0.1621
  villain_range_capped: 0
  board_favour: -0.1004
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0188
  worse_hand_pct: 0.9812
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_039 ---
Hero cards: 9c9h
Board: Ah9s5dQc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.8335
  equity_vs_range: 0.8335
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4004
  villain_air_pct: 0.1621
  villain_range_capped: 0
  board_favour: -0.1004
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0188
  worse_hand_pct: 0.9812
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_040 ---
Hero cards: 8c8d
Board: Ah8s5dJc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.8355
  equity_vs_range: 0.8355
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4328
  villain_air_pct: 0.1488
  villain_range_capped: 0
  board_favour: -0.1328
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0170
  worse_hand_pct: 0.9830
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_041 ---
Hero cards: 8c8h
Board: Ah8s5dJc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.8360
  equity_vs_range: 0.8360
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4328
  villain_air_pct: 0.1488
  villain_range_capped: 0
  board_favour: -0.1328
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0170
  worse_hand_pct: 0.9830
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_042 ---
Hero cards: 9c9d
Board: Ah9s5dJc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.8260
  equity_vs_range: 0.8260
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4388
  villain_air_pct: 0.1622
  villain_range_capped: 0
  board_favour: -0.1388
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0187
  worse_hand_pct: 0.9813
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_043 ---
Hero cards: 9c9h
Board: Ah9s5dJc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.8385
  equity_vs_range: 0.8385
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4388
  villain_air_pct: 0.1622
  villain_range_capped: 0
  board_favour: -0.1388
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0187
  worse_hand_pct: 0.9813
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_044 ---
Hero cards: 7c7d
Board: Ah7s5dQc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.8365
  equity_vs_range: 0.8365
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3827
  villain_air_pct: 0.1521
  villain_range_capped: 0
  board_favour: -0.0827
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0165
  worse_hand_pct: 0.9835
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_045 ---
Hero cards: 7c7h
Board: Ah7s5dQc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.8350
  equity_vs_range: 0.8350
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.0800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3827
  villain_air_pct: 0.1521
  villain_range_capped: 0
  board_favour: -0.0827
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0166
  worse_hand_pct: 0.9834
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW45_046 ---
Hero cards: AcAd
Board: AhKs5cQd
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.9010
  equity_vs_range: 0.9010
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4666
  villain_air_pct: 0.0747
  villain_range_capped: 0
  board_favour: -0.1666
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0542
  worse_hand_pct: 0.9458
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.1579

--- HAND: PILOT_LEVER_C_MW45_047 ---
Hero cards: AcAs
Board: AhKs5cQd
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.8870
  equity_vs_range: 0.8870
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4666
  villain_air_pct: 0.0747
  villain_range_capped: 0
  board_favour: -0.1666
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0542
  worse_hand_pct: 0.9458
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.1579

--- HAND: PILOT_LEVER_C_MW45_048 ---
Hero cards: AcAd
Board: AhKs6cJd
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.8865
  equity_vs_range: 0.8865
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4917
  villain_air_pct: 0.0637
  villain_range_capped: 0
  board_favour: -0.1917
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0541
  worse_hand_pct: 0.9459
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.1579

--- HAND: PILOT_LEVER_C_MW45_049 ---
Hero cards: AcAs
Board: AhKs6cJd
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.8850
  equity_vs_range: 0.8850
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.5800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4917
  villain_air_pct: 0.0637
  villain_range_capped: 0
  board_favour: -0.1917
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0541
  worse_hand_pct: 0.9459
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.1579

--- HAND: PILOT_LEVER_C_MW45_050 ---
Hero cards: KcKd
Board: AhKs5hQc
Street: turn
Hero position: BTN
Villain positions: CO, BB
Num opponents: 2
Pot (BB): 20.0
To call (BB): 12.0
Facing bet: True
Action history: ['preflop: BTN call', 'flop: BTN check']
Key features:
  raw_equity: 0.8105
  equity_vs_range: 0.8105
  pot_odds: 0.3750
  is_ip: 1
  hand_category: 12
  is_made_hand: 1
  is_strong_made: 1
  is_monster: 1
  draw_outs: 0
  has_flush_draw: 0
  has_straight_draw: 0
  danger_score: 0.8800
  spr: 5.0000
  villain_top_pair_plus_pct: 0.4127
  villain_air_pct: 0.0000
  villain_range_capped: 0
  board_favour: -0.1127
  num_callers_to_bet: 0
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.0585
  worse_hand_pct: 0.9415
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_006 ---
Hero cards: AsQs
Board: KsJs5d
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4868
  equity_vs_range: 0.4868
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 17
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3172
  villain_air_pct: 0.2015
  villain_range_capped: 0
  board_favour: -0.0172
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7176
  worse_hand_pct: 0.2358
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2268
  nut_flush_block: 1
  straight_draw_block_pct: 0.3093
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_007 ---
Hero cards: AsJs
Board: KsTh5s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4590
  equity_vs_range: 0.4590
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 13
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3230
  villain_air_pct: 0.2173
  villain_range_capped: 0
  board_favour: -0.0230
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7834
  worse_hand_pct: 0.1820
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2457
  nut_flush_block: 1
  straight_draw_block_pct: 0.2766
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_008 ---
Hero cards: AsJs
Board: KsTc5s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4695
  equity_vs_range: 0.4695
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 13
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3230
  villain_air_pct: 0.2173
  villain_range_capped: 0
  board_favour: -0.0230
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7834
  worse_hand_pct: 0.1820
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2457
  nut_flush_block: 1
  straight_draw_block_pct: 0.2766
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_009 ---
Hero cards: AsJs
Board: KsTs5h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4550
  equity_vs_range: 0.4550
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 13
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3230
  villain_air_pct: 0.2173
  villain_range_capped: 0
  board_favour: -0.0230
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7875
  worse_hand_pct: 0.1786
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2149
  nut_flush_block: 1
  straight_draw_block_pct: 0.2766
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_010 ---
Hero cards: AsJs
Board: KsTs5c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4475
  equity_vs_range: 0.4475
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 13
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3230
  villain_air_pct: 0.2173
  villain_range_capped: 0
  board_favour: -0.0230
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7875
  worse_hand_pct: 0.1786
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2149
  nut_flush_block: 1
  straight_draw_block_pct: 0.2766
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_011 ---
Hero cards: AhQh
Board: KhJs5h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4790
  equity_vs_range: 0.4790
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 17
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.2547
  villain_air_pct: 0.0240
  villain_range_capped: 0
  board_favour: 0.0453
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7143
  worse_hand_pct: 0.2386
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2351
  nut_flush_block: 1
  straight_draw_block_pct: 0.2904
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_012 ---
Hero cards: AhQh
Board: KhJc5h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4798
  equity_vs_range: 0.4798
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 17
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.2547
  villain_air_pct: 0.0240
  villain_range_capped: 0
  board_favour: 0.0453
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7143
  worse_hand_pct: 0.2386
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2351
  nut_flush_block: 1
  straight_draw_block_pct: 0.2904
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_013 ---
Hero cards: AhQh
Board: KhJh5d
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4677
  equity_vs_range: 0.4677
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 17
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.2523
  villain_air_pct: 0.0238
  villain_range_capped: 0
  board_favour: 0.0477
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7176
  worse_hand_pct: 0.2358
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1980
  nut_flush_block: 1
  straight_draw_block_pct: 0.2904
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_014 ---
Hero cards: AhJh
Board: KhTs5h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4495
  equity_vs_range: 0.4495
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 13
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.2588
  villain_air_pct: 0.0326
  villain_range_capped: 0
  board_favour: 0.0412
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7834
  worse_hand_pct: 0.1820
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2208
  nut_flush_block: 1
  straight_draw_block_pct: 0.2585
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_015 ---
Hero cards: AhJh
Board: KhTh5d
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4547
  equity_vs_range: 0.4547
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 13
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.2563
  villain_air_pct: 0.0322
  villain_range_capped: 0
  board_favour: 0.0437
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7875
  worse_hand_pct: 0.1786
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1858
  nut_flush_block: 1
  straight_draw_block_pct: 0.2585
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_016 ---
Hero cards: AdQd
Board: KdJs5d
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4785
  equity_vs_range: 0.4785
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 17
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3172
  villain_air_pct: 0.2015
  villain_range_capped: 0
  board_favour: -0.0172
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7143
  worse_hand_pct: 0.2386
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2595
  nut_flush_block: 1
  straight_draw_block_pct: 0.3093
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_017 ---
Hero cards: AdQd
Board: KdJh5d
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4667
  equity_vs_range: 0.4667
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 17
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3172
  villain_air_pct: 0.2015
  villain_range_capped: 0
  board_favour: -0.0172
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7143
  worse_hand_pct: 0.2386
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2595
  nut_flush_block: 1
  straight_draw_block_pct: 0.3093
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_018 ---
Hero cards: AcQc
Board: KcJs5c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4953
  equity_vs_range: 0.4953
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 17
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3172
  villain_air_pct: 0.2015
  villain_range_capped: 0
  board_favour: -0.0172
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7143
  worse_hand_pct: 0.2386
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2595
  nut_flush_block: 1
  straight_draw_block_pct: 0.3093
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_019 ---
Hero cards: AcQc
Board: KcJh5c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4778
  equity_vs_range: 0.4778
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 17
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3172
  villain_air_pct: 0.2015
  villain_range_capped: 0
  board_favour: -0.0172
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7143
  worse_hand_pct: 0.2386
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2595
  nut_flush_block: 1
  straight_draw_block_pct: 0.3093
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_020 ---
Hero cards: AcJc
Board: KcTs5c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4602
  equity_vs_range: 0.4602
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 13
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3230
  villain_air_pct: 0.2173
  villain_range_capped: 0
  board_favour: -0.0230
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7834
  worse_hand_pct: 0.1820
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2457
  nut_flush_block: 1
  straight_draw_block_pct: 0.2766
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_021 ---
Hero cards: AsKs
Board: Qh8s3s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4713
  equity_vs_range: 0.4713
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3091
  villain_air_pct: 0.3091
  villain_range_capped: 0
  board_favour: -0.0091
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6456
  worse_hand_pct: 0.2843
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2953
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_022 ---
Hero cards: AsKs
Board: Qc8s3s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4547
  equity_vs_range: 0.4547
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3091
  villain_air_pct: 0.3091
  villain_range_capped: 0
  board_favour: -0.0091
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6456
  worse_hand_pct: 0.2843
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2953
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_023 ---
Hero cards: AsKs
Board: Qh7s3s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4662
  equity_vs_range: 0.4662
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3128
  villain_air_pct: 0.3161
  villain_range_capped: 0
  board_favour: -0.0128
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6456
  worse_hand_pct: 0.2843
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.3193
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_024 ---
Hero cards: AsQs
Board: Jh8s3s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4450
  equity_vs_range: 0.4450
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3869
  villain_air_pct: 0.3099
  villain_range_capped: 0
  board_favour: -0.0869
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6923
  worse_hand_pct: 0.2626
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2653
  nut_flush_block: 1
  straight_draw_block_pct: 0.1359
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_025 ---
Hero cards: AsQs
Board: Jc8s3s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4490
  equity_vs_range: 0.4490
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3869
  villain_air_pct: 0.3099
  villain_range_capped: 0
  board_favour: -0.0869
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6923
  worse_hand_pct: 0.2626
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2653
  nut_flush_block: 1
  straight_draw_block_pct: 0.1359
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_026 ---
Hero cards: AsQs
Board: Jh7s3s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4467
  equity_vs_range: 0.4467
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3659
  villain_air_pct: 0.3263
  villain_range_capped: 0
  board_favour: -0.0659
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6923
  worse_hand_pct: 0.2626
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2799
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_027 ---
Hero cards: AhKh
Board: Qs8h3h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4560
  equity_vs_range: 0.4560
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.2383
  villain_air_pct: 0.0579
  villain_range_capped: 0
  board_favour: 0.0617
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6456
  worse_hand_pct: 0.2843
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2737
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_028 ---
Hero cards: AhKh
Board: Qc8h3h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4688
  equity_vs_range: 0.4688
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.2383
  villain_air_pct: 0.0579
  villain_range_capped: 0
  board_favour: 0.0617
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6456
  worse_hand_pct: 0.2843
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2737
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_029 ---
Hero cards: AhKh
Board: Qs7h3h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4785
  equity_vs_range: 0.4785
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.2395
  villain_air_pct: 0.0649
  villain_range_capped: 0
  board_favour: 0.0605
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6456
  worse_hand_pct: 0.2843
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2950
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_030 ---
Hero cards: AhQh
Board: Js8h3h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4455
  equity_vs_range: 0.4455
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.2975
  villain_air_pct: 0.0560
  villain_range_capped: 0
  board_favour: 0.0025
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6923
  worse_hand_pct: 0.2626
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2417
  nut_flush_block: 1
  straight_draw_block_pct: 0.1321
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_031 ---
Hero cards: AhQh
Board: Jc8h3h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4425
  equity_vs_range: 0.4425
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.2975
  villain_air_pct: 0.0560
  villain_range_capped: 0
  board_favour: 0.0025
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6923
  worse_hand_pct: 0.2626
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2417
  nut_flush_block: 1
  straight_draw_block_pct: 0.1321
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_032 ---
Hero cards: AcKc
Board: Qh8c3c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4577
  equity_vs_range: 0.4577
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3091
  villain_air_pct: 0.3091
  villain_range_capped: 0
  board_favour: -0.0091
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6456
  worse_hand_pct: 0.2843
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2953
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_033 ---
Hero cards: AcKc
Board: Qs8c3c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4657
  equity_vs_range: 0.4657
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3091
  villain_air_pct: 0.3091
  villain_range_capped: 0
  board_favour: -0.0091
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6456
  worse_hand_pct: 0.2843
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2953
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_034 ---
Hero cards: AdKd
Board: Qh8d3d
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4530
  equity_vs_range: 0.4530
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3091
  villain_air_pct: 0.3091
  villain_range_capped: 0
  board_favour: -0.0091
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6456
  worse_hand_pct: 0.2843
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2953
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_035 ---
Hero cards: AdKd
Board: Qs8d3d
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4833
  equity_vs_range: 0.4833
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.2500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3091
  villain_air_pct: 0.3091
  villain_range_capped: 0
  board_favour: -0.0091
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.6456
  worse_hand_pct: 0.2843
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.2953
  nut_flush_block: 1
  straight_draw_block_pct: 0.0000
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_036 ---
Hero cards: As9s
Board: QsJh5s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.3738
  equity_vs_range: 0.3738
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3153
  villain_air_pct: 0.2201
  villain_range_capped: 0
  board_favour: -0.0153
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7953
  worse_hand_pct: 0.2047
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1367
  nut_flush_block: 1
  straight_draw_block_pct: 0.1586
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_037 ---
Hero cards: As9s
Board: QsJc5s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4020
  equity_vs_range: 0.4020
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3153
  villain_air_pct: 0.2201
  villain_range_capped: 0
  board_favour: -0.0153
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7953
  worse_hand_pct: 0.2047
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1367
  nut_flush_block: 1
  straight_draw_block_pct: 0.1586
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_038 ---
Hero cards: As8s
Board: QsJh5s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.3660
  equity_vs_range: 0.3660
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3153
  villain_air_pct: 0.2201
  villain_range_capped: 0
  board_favour: -0.0153
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7923
  worse_hand_pct: 0.2077
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1354
  nut_flush_block: 1
  straight_draw_block_pct: 0.1381
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_039 ---
Hero cards: As8s
Board: QsJc5s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4083
  equity_vs_range: 0.4083
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3153
  villain_air_pct: 0.2201
  villain_range_capped: 0
  board_favour: -0.0153
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7923
  worse_hand_pct: 0.2077
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1354
  nut_flush_block: 1
  straight_draw_block_pct: 0.1381
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_040 ---
Hero cards: Ah9h
Board: QhJs5h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.3870
  equity_vs_range: 0.3870
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.2531
  villain_air_pct: 0.0239
  villain_range_capped: 0
  board_favour: 0.0469
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7953
  worse_hand_pct: 0.2047
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1251
  nut_flush_block: 1
  straight_draw_block_pct: 0.1630
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_041 ---
Hero cards: Ah9h
Board: QhJc5h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.3965
  equity_vs_range: 0.3965
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.2531
  villain_air_pct: 0.0239
  villain_range_capped: 0
  board_favour: 0.0469
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7953
  worse_hand_pct: 0.2047
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1251
  nut_flush_block: 1
  straight_draw_block_pct: 0.1630
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_042 ---
Hero cards: Ac9c
Board: QcJh5c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.3748
  equity_vs_range: 0.3748
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3153
  villain_air_pct: 0.2201
  villain_range_capped: 0
  board_favour: -0.0153
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7953
  worse_hand_pct: 0.2047
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1367
  nut_flush_block: 1
  straight_draw_block_pct: 0.1586
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_043 ---
Hero cards: Ac9c
Board: QcJs5c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.3960
  equity_vs_range: 0.3960
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3153
  villain_air_pct: 0.2201
  villain_range_capped: 0
  board_favour: -0.0153
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7953
  worse_hand_pct: 0.2047
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1367
  nut_flush_block: 1
  straight_draw_block_pct: 0.1586
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_044 ---
Hero cards: Ad9d
Board: QdJh5d
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4108
  equity_vs_range: 0.4108
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3153
  villain_air_pct: 0.2201
  villain_range_capped: 0
  board_favour: -0.0153
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7953
  worse_hand_pct: 0.2047
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1367
  nut_flush_block: 1
  straight_draw_block_pct: 0.1586
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_045 ---
Hero cards: Ad9d
Board: QdJs5d
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.3910
  equity_vs_range: 0.3910
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 1
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 9
  has_flush_draw: 1
  has_straight_draw: 0
  danger_score: 0.4500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3153
  villain_air_pct: 0.2201
  villain_range_capped: 0
  board_favour: -0.0153
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.7953
  worse_hand_pct: 0.2047
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1367
  nut_flush_block: 1
  straight_draw_block_pct: 0.1586
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_046 ---
Hero cards: KsQs
Board: JsTc4s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4978
  equity_vs_range: 0.4978
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 17
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.4500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3950
  villain_air_pct: 0.2437
  villain_range_capped: 0
  board_favour: -0.0950
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.8462
  worse_hand_pct: 0.1207
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1308
  nut_flush_block: 0
  straight_draw_block_pct: 0.2738
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_047 ---
Hero cards: KhQh
Board: JhTs4h
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4850
  equity_vs_range: 0.4850
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 17
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.4500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3134
  villain_air_pct: 0.0312
  villain_range_capped: 0
  board_favour: -0.0134
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.8462
  worse_hand_pct: 0.1207
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1171
  nut_flush_block: 0
  straight_draw_block_pct: 0.2500
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_048 ---
Hero cards: KcQc
Board: JcTs4c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.4775
  equity_vs_range: 0.4775
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 17
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.4500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3950
  villain_air_pct: 0.2437
  villain_range_capped: 0
  board_favour: -0.0950
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.8462
  worse_hand_pct: 0.1207
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1308
  nut_flush_block: 0
  straight_draw_block_pct: 0.2738
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_049 ---
Hero cards: KdQd
Board: JdTs4c
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.3108
  equity_vs_range: 0.3108
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 8
  has_flush_draw: 0
  has_straight_draw: 1
  danger_score: 0.3000
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3950
  villain_air_pct: 0.2437
  villain_range_capped: 0
  board_favour: -0.0950
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.8462
  worse_hand_pct: 0.1207
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.0000
  nut_flush_block: 0
  straight_draw_block_pct: 0.2738
  nut_made_block_pct: 0.0000

--- HAND: PILOT_LEVER_C_MW47_050 ---
Hero cards: QsJs
Board: Ts9c4s
Street: flop
Hero position: BB
Villain positions: CO, BTN
Num opponents: 2
Pot (BB): 20.0
To call (BB): 10.0
Facing bet: True
Action history: ['preflop: BB call']
Key features:
  raw_equity: 0.5310
  equity_vs_range: 0.5310
  pot_odds: 0.3333
  is_ip: 0
  hand_category: 2
  is_made_hand: 0
  is_strong_made: 0
  is_monster: 0
  draw_outs: 17
  has_flush_draw: 1
  has_straight_draw: 1
  danger_score: 0.4500
  spr: 5.0000
  villain_top_pair_plus_pct: 0.3915
  villain_air_pct: 0.2545
  villain_range_capped: 0
  board_favour: -0.0915
  num_callers_to_bet: 1
  facing_raise: 0
  villain_aggression_count: 1
  villain_checked_back: 0
  better_hand_pct: 0.9085
  worse_hand_pct: 0.0704
  is_preflop_aggressor: 0
  is_3bet_pot: 0
  flush_block_pct: 0.1048
  nut_flush_block: 0
  straight_draw_block_pct: 0.2866
  nut_made_block_pct: 0.0000
