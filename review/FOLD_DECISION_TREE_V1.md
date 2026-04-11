# FOLD Decision Tree v1 — For Labelling Agent

**Date:** 9 April 2026
**Author:** GTO Expert — synthesised from three_way_gto.md KB + RAISE_DECISION_TREE_V2.md
**Status:** AWAITING REVIEW + OWNER APPROVAL
**Applies to:** Situations where `facing_bet == 1` AND the RAISE tree returned no RAISE
**Scope:** 3-way pots, 100bb effective, single-raised pots (SRP) unless noted
**Output:** FOLD or CALL — never a frequency

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

**When this tree runs:**
1. `facing_bet == 1` — hero is facing a bet (to_call > 0).
2. The RAISE tree was checked first. No RAISE step fired.
3. This tree now decides: FOLD or CALL.

If no FOLD step fires, the hand defaults to CALL. CALL is correct for the
majority of situations where the RAISE tree did not fire — these are hands
that have equity, showdown value, or pot odds sufficient to continue.

Do not duplicate the RAISE tree's logic. This tree complements it. The RAISE
tree's Step 1 flat-spot checks (bet-and-call non-monster, board heavily
favours villain, multi-street aggressor) force CALL-not-RAISE. Some of those
same hands — once position, equity margin, and hand quality are examined here —
should actually FOLD. The RAISE tree correctly identified they should not raise.
This tree identifies which of those should fold rather than call.

If any condition in a step cannot be computed from the above features,
that condition is removed and the step is skipped.

---

## Global Pre-Check: Is This Tree Applicable?

Before running any step, verify:

A. `facing_bet == 1` — hero is facing a bet. If not, this tree does not apply.
B. RAISE tree returned CALL (no RAISE step fired) — if RAISE tree fired, output is RAISE.
C. `is_monster == 1` — monsters always call at minimum (RAISE tree handles whether to
   raise). If `is_monster == 1`, skip this tree entirely and output CALL.

If any pre-check fails, this tree does not apply.

**Monster protection rule:** `is_monster == 1` is an unconditional CALL gate. Monsters
never fold facing a single bet — they have enough equity to call in all configurations
the feature vector can represent. If a monster should raise, the RAISE tree handles it.
If not, it calls. It does not fold.

---

## Step 1 — Equity Below Pot Odds (Pure Math Fold)

**Condition — ALL required:**
- `raw_equity < pot_odds`
- `draw_outs < 6` (fewer than 6 outs — not enough improvement equity to justify continuing)
- `overcard_outs < 4` (fewer than 4 overcard outs — no meaningful hidden equity)
- `is_monster == 0`

→ **FOLD**. Confidence: HIGH.

**Rationale:** When raw equity is below the pot odds required to call, hero is paying
more than their equity share. The draw_outs and overcard_outs gates prevent folding
hands with hidden equity paths not captured in raw_equity. KB Example 7 establishes
that AK on a missed board has 6 overcard outs (~24% hidden equity) and should call
even when raw_equity looks close to pot odds. Step 1 only fires when there is no
credible improvement path — true air with no draws and no overcards.

**Teaching point:** This is the clearest fold in poker. If you're not getting the odds
and you cannot improve, fold. This should not fire often — the RAISE tree's pre-check
already blocked hands with clear equity, and most hands that survive to this tree have
some equity. Step 1 catches the edge case where hero holds a weak hand type (bottom
pair, underpair) that happened to avoid the RAISE tree's other suppressors.

---

## Step 2 — Pure Air: No Made Hand, No Draw, No Showdown Value

**Condition — ALL required:**
- `is_made_hand == 0`
- `draw_outs == 0`
- `has_showdown_value == 0`
- `overcard_outs < 4` (fewer than 4 overcard outs — KB Example 7 gap protection)
- `is_monster == 0`

→ **FOLD**. Confidence: HIGH.

**Rationale:** A hand with no pair, no draw, and no showdown value has no way to win
at showdown and no improvement path. Against a bet from villain, calling pays to see
a card that almost certainly will not help. This is the definitional "pure air"
holding. KB Section 1.7 and DO NOT Rule #2 establish that pure bluffs are not
profitable 3-way (fold equity ~36% combined). The reverse logic applies to the caller:
pure air cannot win the pot at showdown, and the bet-behind has not created a fold
situation for the bettor. Fold.

**Overcard_outs < 4 gate:** KB Example 7 (AK on J84) shows that two unpaired high
cards (AK, AQ) have 6 overcard outs — approximately 24% hidden equity to improve to
top pair. The feature pipeline's draw_outs does not count overcards. Setting the gate
at overcard_outs < 4 ensures that AK (6 outs) and AQ (6 outs) do not fire this step.
Only hands with zero to three overcard outs fire Step 2.

---

## Step 3 — Thin Equity Plus Multi-Street Aggression (MW-50 Pattern)

**Condition — ALL required:**
- `equity_margin < 0.05` (equity is within 5pp of pot odds — thin surplus)
- `villain_aggression_count >= 2` (villain has shown strength across two or more streets)
- `is_monster == 0`
- `draw_outs < 8` (fewer than 8 outs — no significant draw equity surviving range narrowing)
- `has_showdown_value == 0` OR `villain_top_pair_plus_pct >= 0.55`

→ **FOLD**. Confidence: HIGH.

**Rationale — the MW-50 pattern:** JcTc on J845 facing flop raise plus turn barrel.
Raw equity is 33%, pot odds are 29% — a 4pp surplus that naively says "call." But
villain's two-street aggression (flop raise, turn barrel) into two opponents is a
very strong signal. The RAISE tree's Step 1C blocked a raise (`villain_aggression_count
>= 2 AND is_monster == 0`). Now this tree evaluates whether the 4pp surplus is
enough to call against a now-narrowed villain range.

It is not. When villain fires two streets of aggression into a 3-way pot, their
range condenses to strong made hands and premium draws. Against that condensed range,
hero's raw equity drops materially from the original preflop-range-based calculation.
A 4pp surplus built on the full preflop range does not survive that range narrowing.
The fold is correct.

**The draw_outs < 8 gate:** KB Example 8 (QT on KQ7J, second pair + OESD, 8 outs)
establishes that draw equity survives range narrowing when hero has 8+ outs to a hand
that beats villain's entire range. The KB is explicit: "Don't conflate 'villain is
strong' with 'always fold.'" Step 3 does not fire when hero holds a significant draw
because the 8 clean outs remain clean regardless of range narrowing — when hero makes
the straight, it beats everything. Only thin equity without a draw fires Step 3.

**The has_showdown_value gate:** If hero has showdown value (has_showdown_value == 1)
AND villain's range is not heavily weighted towards top pair+ (villain_top_pair_plus_pct
< 0.55), the showdown value is meaningful — hero can win at showdown against parts of
villain's range. Step 3 does not fire in that case. When villain_top_pair_plus_pct
>= 0.55, villain's range is so top-pair-heavy that hero's showdown value (e.g., bottom
pair, weak middle pair) is largely nullified — the made hand rarely wins at showdown.
Combined with thin equity margin and multi-street aggression, this is a fold.

---

## Step 4 — Bet-and-Call Signal with Dominated Non-Premium

**Condition — ALL required:**
- `num_callers_to_bet >= 1` (one opponent bet, another called — both ranges narrowed)
- `hero_range_percentile < 0.40` (hero is in the bottom 40% of their range)
- `equity_margin < 0.10` (equity surplus is less than 10pp above pot odds)
- `is_monster == 0`
- `is_made_hand == 1` (this step applies to dominated made hands, not draws — draws
  handled by the draw equity exception below)
- `draw_outs < 6` (no significant draw to compensate for range domination)

→ **FOLD**. Confidence: MEDIUM-HIGH.

**Rationale — applying the MW-30 correction carefully:** KB Section 2 (Factor 5) and
the corrected Example 3 are the foundation for this step. The bet-and-call signal
narrows both opponents' ranges. The KB correction is critical: "The fold applies ONLY
when BOTH conditions are met: (1) Hero's equity against the narrowed ranges is close
to break-even (within ~5pp of pot odds), AND (2) Hero's specific holding is dominated
by the calling range."

The correction to Example 3 showed that KT on KJ6 is a CALL despite bet-and-call —
40% equity vs 18% pot odds, a 22pp surplus too large to fold. This step enforces
equity_margin < 0.10 (10pp surplus) as the threshold. At 10pp+, folding is wrong
(the MW-30 trap). At under 10pp, with a hand in the bottom 40% of range facing both
opponents showing strength, the equity against the now-narrowed ranges is insufficient.

**hero_range_percentile < 0.40:** This is the "dominated" proxy. A hand in the bottom
40% of range facing bet-and-call is not a premium. The callers are representing hands
in the top 30-40% of their ranges. Hero's bottom-40% holding is likely behind or
marginally ahead of small parts of the caller's range — not enough to justify continuing
at thin pot odds.

**Draw equity exception:** If draw_outs >= 6, this step does not fire. KB Example 8
establishes that draw equity survives range narrowing when outs are sufficient. A hand
with 6+ outs to a strong hand (e.g., flush draw, OESD) has equity that is independent
of how narrow villain's range is — making the straight beats everything. Step 4 only
targets dominated made hands with no draw.

**Note on why this is MEDIUM-HIGH, not HIGH:** The equity_margin and hero_range_percentile
thresholds are approximate proxies for "dominated." A hand at percentile 0.39 with
equity_margin 0.09 is correctly folded by this step. A hand at 0.41 with equity_margin
0.11 is called. The line is real but the proxies are imperfect. Flag any bet-and-call
FOLD that is close to these thresholds for expert review.

---

## Step 5 — Board Heavily Favours Villain, Uncapped Range, Thin Equity

**Condition — ALL required:**
- `board_favour <= -0.30` (board strongly favours villain's range)
- `villain_range_capped == 0` (villain's preflop action allows premiums — they are uncapped)
- `equity_margin < 0.10` (thin equity surplus — less than 10pp above pot odds)
- `is_monster == 0`
- `draw_outs < 6` (no significant draw providing independent equity)
- `villain_aggression_count >= 1` (villain has bet at least once — passive check-backs
  on boards that favour villain are usually weaker hands, not the strong range that
  warrants folding)

→ **FOLD**. Confidence: MEDIUM.

**Rationale:** When the board strongly favours villain's range (board_favour <= -0.30)
and villain is uncapped (can hold premiums), a bet from villain connects heavily with
their range. A typical example: hero holds middle pair on an ace-high dry board, villain
opened from early position (uncapped, lots of Ax in range), and board_favour is deeply
negative. Villain's bet on the board that smashes their range is a credible, range-wide
threat.

Hero's thin equity margin (< 10pp above pot odds) combined with a board that genuinely
favours villain means the equity calculation is working against a strong range — even
if the preflop-range-based raw_equity shows a nominal surplus, the board-texture
interaction means villain's betting range within that preflop range is significantly
stronger than average.

**villain_aggression_count >= 1 gate:** A villain who checks back on a board that
favours their range is often trapping or holding a specific hand subset. The betting
line is the signal that matters. Without at least one bet, the board_favour signal
alone is insufficient to fold.

**Why MEDIUM confidence:** board_favour is a range-level metric, not a hand-specific
one. The board may favour villain's range without the specific hands villain holds
dominating hero. The equity_margin gate partially corrects for this, but the step
may occasionally fire on hands that have a stronger equity position than the board
metric suggests.

---

## Default

No step returned FOLD.

→ **CALL**.

This is the correct outcome for the majority of situations where the RAISE tree did
not fire a RAISE. Most hands that reach this tree have sufficient equity, draw equity,
or pot odds to continue. The 5 FOLD steps target specific, well-defined patterns from
the KB. Everything else calls.

**What this default encodes:**
- Clear equity surplus (equity_margin >= 0.10+) against any aggression
- Draw hands with 8+ outs (independent equity survives range narrowing)
- Made hands with showdown value facing thin villain ranges
- Small bets with any made hand (pot_odds <= 0.20 makes folding almost always wrong)
- Monster hands (pre-check blocked these from the tree entirely)
- AK/AQ with overcard outs on missed boards (KB Example 7 pattern)

---

## Quick Reference: Hands That FOLD

| Scenario | Key Features | Step |
|----------|-------------|------|
| Pure air: no pair, no draw, no showdown value, no overcards | is_made=0, draw_outs=0, sdv=0, overcard_outs < 4 | 2 |
| Below pot odds, no draws, no overcards | raw_equity < pot_odds, draw_outs < 6, overcard_outs < 4 | 1 |
| Thin equity + two-street villain aggression, no significant draw | equity_margin < 0.05, villain_agg >= 2, draw_outs < 8 | 3 |
| Dominated made hand facing bet-and-call, thin odds | num_callers >= 1, hero_range_pct < 0.40, equity_margin < 0.10, draw_outs < 6 | 4 |
| Thin equity, uncapped villain, board heavily favours villain | board_favour <= -0.30, villain_capped=0, equity_margin < 0.10, draw_outs < 6 | 5 |

---

## Quick Reference: Hands That CALL (despite potential fold signals)

| Scenario | Why It Calls | Override |
|----------|-------------|---------|
| Monster (any configuration) | Pre-check: is_monster == 1 exits tree → CALL | Pre-check C |
| Large equity surplus (equity_margin >= 0.15+) | Steps 1, 3, 4, 5 all require equity_margin < 0.10; clear surplus bypasses them | No step fires |
| Draw with 8+ outs facing multi-street aggressor | Draw equity survives range narrowing (KB Example 8, OESD on KQJ) | Step 3 draw gate (draw_outs >= 8) |
| Draw with 6+ outs facing bet-and-call | Draw equity is hand-specific, not range-dependent | Step 4 draw gate (draw_outs >= 6) |
| AK/AQ on missed board (overcard_outs >= 4) | Hidden equity not in raw_equity (KB Example 7) | Steps 1, 2 overcard gates |
| KT top pair on KJ6 facing bet-and-call (MW-30 corrected) | 40% equity vs 18% pot odds = 22pp surplus, too large to fold | Step 4 equity_margin gate (0.22 > 0.10) |
| K7 trips on 775-9-J facing check-raise (MW-46) | Trips always call; is_monster check exits tree | Pre-check C |
| Small bet, any made hand (pot_odds <= 0.20) | Pot odds too good — even weak made hands call small bets | No step fires (equity_margin likely >= 0.10) |
| Second pair + OESD facing double barrel (KB Example 8) | 8 draw outs + IP + pot odds nearly met → draw equity tips call | Step 3 draw gate (draw_outs >= 8) |

---

## MW-50 Worked Example (Calibration Reference)

**Setup:** Hero holds JcTc on J845 (flop raise, turn barrel from villain). Raw equity
33%, pot odds 29%, equity_margin = 0.04. villain_aggression_count = 2. draw_outs = 4
(gutshot only). has_showdown_value = 1 (top pair). villain_top_pair_plus_pct = 0.62.

**Tree evaluation:**

- Pre-check C: is_monster == 0 — continue.
- Step 1: raw_equity (0.33) > pot_odds (0.29) — Step 1 does NOT fire.
- Step 2: is_made_hand == 1 (top pair) — Step 2 does NOT fire.
- Step 3: equity_margin = 0.04 < 0.05 ✓. villain_aggression_count = 2 >= 2 ✓.
  is_monster == 0 ✓. draw_outs = 4 < 8 ✓. has_showdown_value == 1 — check the OR gate:
  villain_top_pair_plus_pct = 0.62 >= 0.55 ✓. ALL conditions met.

→ **FOLD** (Step 3). Confidence: HIGH.

**Why this is correct:** The 4pp surplus (33% vs 29%) is overwhelmed by two streets
of aggression narrowing villain's range. Against that narrowed range, hero's JT on
J845 is mostly behind — villain's range is dense with sets, two pair (J8, J4, J5, 84,
85, 45), and premium draws that have hero dominated. The nominal equity surplus was
computed against the full preflop range; the realized equity against the aggression-
narrowed range is below pot odds. Step 3 catches this.

---

## Relationship to Other Trees

**RAISE tree (RAISE_DECISION_TREE_V2.md):**
- Runs first. If RAISE fires, output is RAISE — this tree does not run.
- RAISE Step 1 flat-spot checks block raising for: bet-and-call non-monster (1A),
  board heavily favours villain (1B), multi-street aggressor non-monster (1C).
- Those same hands reach this tree. Some FOLD here (Step 4 for bet-and-call, Step 5
  for board-favour, Step 3 for aggressor) — but only when equity is also thin.
  Hands with clear equity surplus still call despite not raising.

**BET tree (BET_DECISION_TREE_V1.md):**
- Applies when facing_bet == 0 (hero is not facing a bet). Completely separate path.
- No overlap with this tree.

---

## Feature Reference Table

All features used in this tree. Names match `feature_keys.py` (class F).
Street encoding: 0=flop, 1=turn, 2=river.
hand_category encoding: 0=high_card, 1=one_overcard, 2=overcards, 3=bottom_pair,
4=underpair, 5=middle_pair, 6=top_pair, 7=top_pair_good_kicker,
8=top_pair_top_kicker, 9=overpair, 10=two_pair, 11=trips, 12=straight,
13=flush, 14=full_house, 15=quads, 16=straight_flush.

| Feature | Encoding / Range | How Used in FOLD Tree |
|---------|-----------------|----------------------|
| `facing_bet` | 0 or 1 | Pre-check A: must be 1 for this tree |
| `is_monster` | 0 or 1 | Pre-check C: monsters always CALL, skip tree |
| `raw_equity` | 0.0–1.0 | Step 1: must be < pot_odds to fire |
| `pot_odds` | 0.0–1.0 | Step 1: equity benchmark; Step 4/5: implied by equity_margin |
| `equity_margin` | Signed float (raw_equity − pot_odds) | Steps 3, 4, 5: thin equity gate |
| `draw_outs` | 0–17 (clean outs to best draw) | Steps 1, 2, 3, 4, 5: draw equity gate prevents fold |
| `overcard_outs` | Integer | Steps 1, 2: prevents folding AK/AQ (KB Example 7) |
| `is_made_hand` | 0 or 1 | Step 2: pure air check; Step 4: dominated made hand |
| `has_showdown_value` | 0 or 1 | Step 3: showdown value check in OR gate |
| `villain_aggression_count` | Integer count | Step 3: two-street aggression signal; Step 5: at least one bet |
| `villain_top_pair_plus_pct` | 0.0–1.0 | Step 3: OR gate — high TP+ nullifies showdown value |
| `num_callers_to_bet` | Integer | Step 4: bet-and-call signal |
| `hero_range_percentile` | 0.0–1.0 | Step 4: dominated hand proxy (< 0.40) |
| `board_favour` | Negative = villain range favoured; positive = PFA favoured | Step 5: board texture gate |
| `villain_range_capped` | 0 or 1 | Step 5: uncapped villain has premiums |
| `hand_category` | 0–16 | Supporting context; is_made_hand is primary gate |
| `num_opponents` | Integer | Context: confirms 3-way configuration |
| `street` | 0=flop, 1=turn, 2=river | Context: multi-street aggression is street-dependent |
| `spr` | Stack-to-pot ratio | Context: low SPR raises commitment threshold |
| `is_ip` | 0 or 1 | Context: position affects equity realization but not FOLD steps directly |
| `villain_air_pct` | 0.0–1.0 | Context: high air weakens aggression signal |
| `better_hand_pct` | 0.0–1.0 | Supporting context for range domination |
| `worse_hand_pct` | 0.0–1.0 | Supporting context; does not gate any step |
| `improvement_probability` | 0.0–1.0 | Supporting context for draw quality |

---

## Known Limitations

**Limitation 1: raw_equity is preflop-range-based.**
The raw_equity feature is computed against villain's preflop range, not the
aggression-narrowed range. Steps 3, 4, and 5 all use equity_margin as a proxy for
"thin equity against a narrowed range." This is an approximation — the actual equity
against the narrowed range is lower. The approximation is conservative (it folds only
when the preflop-range equity is already thin), which is the correct direction.

**Limitation 2: hero_range_percentile as a domination proxy.**
Step 4 uses hero_range_percentile < 0.40 as a proxy for "dominated hand facing
bet-and-call." This is imperfect — a 38th-percentile hand on one board might be
strong on another. The equity_margin gate partially compensates. Hands close to the
0.40 threshold should be reviewed with caution.

**Limitation 3: No positional differentiation in FOLD steps.**
The FOLD steps do not split by is_ip. OOP hands under-realize equity (KB Section 1.5:
60-80% EQR OOP vs 105-120% IP), which makes OOP folds more correct than IP folds at
the same equity level. This tree treats both positions identically for simplicity. If
equity_margin is 0.04 OOP, folding is even more correct than the tree signals; if
0.04 IP with a made hand, it may be a closer decision. Accept this approximation.

**Limitation 4: villain_aggression_count is cumulative, not street-specific.**
Step 3 uses villain_aggression_count >= 2 to detect multi-street aggression. The
feature counts all aggressive actions across all streets — it cannot distinguish
"two bets on consecutive streets" from "one raise and one bet separated by a call."
Both read as >= 2. In practice, any two aggressive actions into a 3-way pot signal
a strong range. The distinction is noted but does not change the folding logic.

---

*File: `/home/rupertbeytell/river-rats-v2/review/FOLD_DECISION_TREE_V1.md`*
*Status: Ready for owner review. Not yet approved or integrated.*
