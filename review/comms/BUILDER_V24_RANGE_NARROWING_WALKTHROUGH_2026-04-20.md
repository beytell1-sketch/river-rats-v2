---
date: 2026-04-20
from: Builder
to: Owner
re: Range narrowing — per-street mechanics walkthrough + "can we do this automatically?" honest answer
status: EXPLAINER — owner-requested pre-GTO-dispatch clarity
---

# Range narrowing — how it works, what breaks, what we can fix automatically

Owner ask: "clarity on how range narrowing is done on each street, and what the plan is. range narrowing is the core of logic and teaching. we need honesty on if we can do it correctly and automatically based on actions."

This doc answers in plain mechanics — not code, not argument. Just the
picture per street + the honest capability map + what "automatic" means
concretely.

---

## Part 1 — The two moving pieces

Range narrowing has two parts:

1. **A baseline range** — villain's starting hand distribution.
   Set by position (e.g., "BB defending vs CO open"). Static. Comes
   from `get_villain_range()`.
2. **Narrowing filters** — frequency multipliers per hand category
   that adjust the baseline based on what villain did.

Three filters exist in the codebase:
- `narrow_to_betting_range` — frequencies for "would villain bet this?"
  per category per street. Solver-grounded tables (KB §1.3).
- `narrow_to_checking_range` — frequencies for "would villain check this?"
  per category per street. Solver-grounded.
- **(missing)** `narrow_to_continuing_range` — frequencies for "would
  villain call a bet with this?" per category per street. **Not
  solver-grounded in existing tables. Not implemented.**

Existing frequency tables (from `range_narrowing.py`, solver-sourced):

| Category | Flop bet | Turn bet | River bet | Flop check | Turn check | River check |
|---|---|---|---|---|---|---|
| nuts | 85% | 90% | 95% | 15% | 10% | 5% |
| strong value (set+) | 75% | 80% | 90% | 25% | 20% | 10% |
| good value (TPTK) | 70% | 60% | 55% | 30% | 40% | 45% |
| draw | 55% | 55% | 0% (miss=air) | 45% | 45% | 100% |
| **medium made** | 45% | **30%** | **8%** | 55% | 70% | **92%** |
| weak made | 35% | 20% | 5% | 65% | 80% | 95% |
| bluff | 25% | 25% | 35% | 75% | 75% | 65% |
| air | 20% | 15% | 20% | 80% | 85% | 80% |

**These tables are correct.** Solver-derived. What's broken isn't
the tables — it's how and when they're applied.

---

## Part 2 — What the code does on each street (IS)

`feature_extractor.py::classify_villain_range()` is the gate. What
it runs per hero decision:

```
1. v_range = get_villain_range(hero_pos, villain_pos, opener_pos)
   → raw preflop opener range, position-aware, NOT action-aware

2. IF hero is facing a bet (facing_bet = 1):
       v_range = narrow_to_betting_range(v_range, current_board, current_street)
   ELSE:
       # leave v_range at raw preflop

3. Classify v_range into TP+ / medium / draw / air buckets
   → these are what the model sees as villain composition
```

**That's the entire thing.** One narrowing call or zero. No
chaining. Never uses `narrow_to_checking_range`.

### Per-street breakdown — exactly what happens

#### Flop decision

| Hero context | What the code does | Villain range produced |
|---|---|---|
| Facing villain's bet | `narrow_to_betting_range(preflop, flop_board, 'flop')` | preflop ∩ flop-bet — **reasonable** |
| Checked to (villain checked first) | Nothing — uses raw preflop range | preflop only — **wrong**, should be preflop ∩ flop-check |
| Hero open-acting (no prior action) | Nothing | preflop only — **correct** (no action to condition on yet) |

#### Turn decision

| Hero context | What the code does | Villain range produced |
|---|---|---|
| Facing villain's turn bet (donk or continued) | `narrow_to_betting_range(preflop, turn_board, 'turn')` | preflop ∩ turn-bet — **misses flop action entirely** |
| Villain checked turn (owner's scenario) | Nothing | preflop only — **wrong**, misses both flop action AND turn check |
| Hero open-acting on turn (check-through flop) | Nothing | preflop only — **wrong**, misses flop check-through |

#### River decision

| Hero context | What the code does | Villain range produced |
|---|---|---|
| Facing villain's river bet, after check-through turn (owner's case) | `narrow_to_betting_range(preflop, river_board, 'river')` | preflop ∩ river-bet — **strips mediums to 8% from the PREFLOP range, ignoring that villain told us "not betting for value" on turn** |
| Facing villain's river bet after full BET-CALL-BET line | `narrow_to_betting_range(preflop, river_board, 'river')` | preflop ∩ river-bet — **ignores flop bet AND turn bet AND turn call; three streets of filtering discarded** |
| Checked to on river | Nothing | preflop only — wildly overestimates air |

**Key insight for the owner's scenario:** medium hands disappearing
from the river range is not arithmetic error — it's the river BET
filter correctly stripping mediums (solver-right) from the wrong
starting set (preflop full range, not the post-check-turn range
that would have RETAINED mediums at ~70%).

---

## Part 3 — What it SHOULD do (solver-correct)

Villain's range at any decision = preflop baseline narrowed by
**every prior action villain took**, in order, using that street's
board.

For the owner's scenario (BB called preflop, BB+hero check turn,
villain bets river):

```
preflop_range = get_villain_range(BB-defend-vs-CO-open)
after_flop    = ?? (depends on flop action — presumably BB called hero's bet,
                    needs CALL-narrow, OR checked through which needs CHECK-narrow)
after_turn    = narrow_to_checking_range(after_flop, turn_board, 'turn')
                 → medium hands retained at 70% of after_flop weight
after_river   = narrow_to_betting_range(after_turn, river_board, 'river')
                 → medium hands dropped to 8% of after_turn weight

Net medium-made at river:
  preflop_medium × [flop_continue] × 0.70 × 0.08
  ≈ preflop_medium × [flop_continue] × 0.056
```

Against the BUGGY current path:

```
preflop_medium × 0.08  (starts from full preflop, jumps straight to river-bet filter)
```

So when preflop_medium is ~15% and the full chain gives you ~0.84%
medium-made, the current code gives ~1.2% — looks similar only
because medium gets crushed to ~1% either way. **The error is
bigger on TP+ and draw classes where the turn-check filter
retains more of the range.** That's the feature-importance leak.

---

## Part 4 — Can we do this automatically? (honest answer)

The owner's core question: can we get correctness from the action
sequence alone, no manual inputs per hand?

### What IS automatic from action history

| Action | Narrow function | Solver-grounded? | Automatic from `action_history`? |
|---|---|---|---|
| BET | `narrow_to_betting_range` | ✅ tables exist | ✅ yes |
| RAISE | same as BET (subtype) | ✅ | ✅ |
| CHECK | `narrow_to_checking_range` | ✅ tables exist | ✅ yes — function exists, just not invoked |
| FOLD | range removal (terminal) | N/A (trivial) | ✅ |

**For a decision in the wake of bet/check/fold/raise actions:
YES, we can automate it. The tables are there, the action_history
data is passed to feature extraction, the narrowing functions exist.
The only thing missing is the chaining logic.**

### Where automation hits a wall

**CALL is the gap.** When villain called hero's bet on a prior
street, villain's range should be narrowed to "hands that called,
not raised, not folded." That's a separate category from `bet` or
`check`.

Solver theory doesn't give a clean "call-frequency table" per
category the way it gives bet/check tables. Why: "would you call
this bet?" depends on the specific bet sizing, who bet, position,
stack, etc. It's not a single scalar per hand category.

Three paths for CALL:

- **A. Approximate (heuristic).** Treat call-continue ≈ (1 - fold_freq -
  raise_freq) per category, using the bet and check tables as
  anchors (hands that would bet are more likely to raise; hands that
  would check are more likely to call). Document the approximation.
  **Fully automatic, not solver-clean.**
- **B. Defer.** Skip CALL-narrowing — leave the range un-narrowed on
  CALL actions. Then the chain reduces to "bet/check narrowing only"
  with CALL acting as a pass-through. **Fully automatic, directionally
  biased on hands that saw CALL actions (over-estimates air and
  edge hands).**
- **C. Solver-derive.** Commission solver runs specifically for
  call-continuing-frequency tables across positions, sizings, and
  textures. **Fully automatic once data exists, but data does not
  exist today.** Multi-day (at minimum) data task.

**None of these require per-hand manual intervention.** The
choice is about quality, not automation.

### Other limits — also automatic, with caveats

- **Multiway (3-way pots).** Villain A's range ideally conditions
  on villain B's action too. Our code tracks a "primary villain"
  seat. We CAN narrow primary villain's action history automatically;
  we CAN'T cleanly track the cross-conditioning without a
  data-structure change to track all villains. Compromise: automate
  primary-villain narrowing in v2.4; defer multiway cross-conditioning.
- **Baseline position ranges are static.** `get_villain_range(pos)`
  returns the same distribution regardless of opponent stack, skill,
  game flow. Pre-existing limit, not in scope. Automation doesn't
  change here.
- **Raise-aware call narrow.** A call-of-a-raise is tighter than a
  call-of-a-bet. Automatable from `action_history` (look at the
  preceding action) but adds complexity. Defer to v2.5 unless
  playtest proves it matters.

---

## Part 5 — The plan, concretely

### What Stage 3.5 will build

Single new function in `range_narrowing.py`:

```
narrow_by_action_history(preflop_range, full_board, action_history, primary_villain):

    For each street in [flop, turn, river]:
        If the street hasn't happened yet: stop.

        street_board = board cards up through this street
        villain_actions_on_street = [a for a in action_history if a.street == street and a.pos == primary_villain]

        For each action villain took on this street (in order):
            If BET or RAISE:
                range = narrow_to_betting_range(range, street_board, street)
            Elif CHECK:
                range = narrow_to_checking_range(range, street_board, street)
            Elif CALL:
                range = narrow_to_continuing_range(range, street_board, street)
                  # body per CALL decision A/B/C
            Elif FOLD:
                return empty range (villain out of hand)

    Return range
```

Single new function `narrow_to_continuing_range` if we pick
Option A (otherwise it's a pass-through).

`classify_villain_range()` in `feature_extractor.py` swaps its
single-street conditional for `narrow_by_action_history(...)` plus
a fallback for hands that don't carry action history (test fixtures
etc.).

All 10 villain-derived features pick up the corrected range
automatically because they consume the range from
`classify_villain_range`.

### Outcome per feature (automatic, downstream)

| Feature | Before Stage 3.5 | After Stage 3.5 |
|---|---|---|
| `villain_top_pair_plus_pct` | single-street + preflop | action-chain through streets |
| `villain_medium_made_pct` | same | same |
| `villain_draw_pct` | same | same |
| `villain_air_pct` | same | same |
| `villain_range_capped` | same | same |
| `board_favour` | same | same |
| `villain_fold_equity_estimate` | same | same |
| `flush_block_pct` (v9) | single-street range | action-chained range |
| `flush_draw_block_pct` (v2.4) | single-street range | action-chained range |
| `straight_draw_block_pct` (v2.4) | single-street range | action-chained range |
| `nut_made_block_pct` (v2.4) | single-street range | action-chained range |

**No per-feature code changes.** All 10 features flow through the
same range input. Fix the range, fix them all.

### What this means for teaching

Owner called out teaching specifically. Teaching reads these same
features (`villain_medium_made_pct`, etc.) to build the "Oracle's
Read" on villain's range composition. **Teaching inherits the fix
automatically.** No separate teaching work needed.

Today teaching says things like "villain range is 70% TP+" when
villain bet the river. After Stage 3.5, the number that comes out
will be action-chain-correct. If the old number was "72% TP+" from
the buggy chain and the new number is "58% TP+" from the correct
chain, teaching text updates automatically.

### What automation can NOT do

The hard limits, restated for owner visibility:

1. **CALL narrowing accuracy.** We can automate the narrowing;
   we can't automatically guarantee the CALL-continue table is
   solver-correct. This is the A/B/C question for the GTO reviewer.
2. **Multiway cross-conditioning.** Primary-villain chain is
   automatic; cross-villain conditioning isn't — that's a v2.5
   data-structure change.
3. **Opponent-specific baseline.** Static position-ranges are the
   ceiling unless we add opponent priors.

These are limits of the solution, not limits of automation. The
solution we ship runs end-to-end on action_history with zero
per-hand intervention, but the CALL branch uses a documented
heuristic (if we pick A) or a pass-through (if we pick B).

---

## Part 6 — What honesty compels me to flag

1. **This fix changes every training row.** Stage 3.5 re-extracts
   villain composition columns on all ~700 v2.3.1 training rows.
   Some TP+/medium/draw/air values will shift. The v2.3.1 model
   was TRAINED on the buggy values. Until we retrain (Stage 5),
   the model's coefficients don't match the corrected features.
   The calibration-anchor gate is how we check — if anchors still
   pass, the current model still works for inference; if not,
   we surface it.

2. **d2410 specifically is a turn decision with a turn-check.**
   Stage 3.5 directly touches this exact decision shape. Whether
   d2410 still predicts BET is the single most load-bearing test
   of the fix. If d2410 flips to CHECK **and** that flip is
   solver-correct, we ship and log it as a calibration anchor
   update. If it flips **wrong direction**, we STOP.

3. **The v2.3.1 playtest-observable medium-disappearing behavior
   partially reflects correct poker** (medium hands don't value-bet
   rivers). But it's reported from the wrong range, so it's
   accidentally right-looking on one axis and wrong on three others
   (TP+, air, draw percentages that feed downstream features).

4. **Teaching may get noisier before it gets better.** The fix makes
   villain composition numbers action-conditioned. On boards where
   the chain changes the range substantially (e.g., turn check-through),
   teaching will say noticeably different things. This is correct
   change, but it looks like a regression until the new numbers are
   understood as reflecting the actual poker.

---

## What I need from owner

Three quick confirms before GTO dispatch:

1. **Explainer clarity.** This doc answers your "how does narrowing
   work per street + can we do it automatically" question. Confirm
   understanding + any questions before I put this in front of the
   GTO reviewer.
2. **Proceed with GTO dispatch** on the prior doc
   (`BUILDER_V24_RANGE_NARROWING_EXPERT_REVIEW_2026-04-20.md`) +
   this walkthrough as supplementary material.
3. **Stage 3.5 scope** — already accepted in your last directive,
   flagging no change. Just confirming the explainer doesn't change
   the scope decision.

Once confirmed I'll dispatch the GTO reviewer with both docs. Their
A/B/C CALL verdict is the next decision gate.
