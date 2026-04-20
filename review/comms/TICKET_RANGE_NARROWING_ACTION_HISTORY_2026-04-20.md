---
date: 2026-04-20
from: Builder
to: Main terminal / Owner
re: TICKET — villain range narrowing ignores cross-street action history
status: FILED — scope recommendation: insert as Stage 3.5 before v2.4 Stage 4 re-labelling
related: owner-flagged from playtest-logs inspection (2026-04-20)
---

# TICKET — Range narrowing is single-street; action history is lost

## Summary

`river-rats-core/range_narrowing.py` exposes `narrow_to_betting_range()`
and `narrow_to_checking_range()`, and `feature_extractor.py` calls
`narrow_to_betting_range()` **only when `facing_bet == 1`**, and only
against the **current street**. No chaining across streets — the
villain range on every decision starts from `get_villain_range()`
(raw preflop opener range) and applies at most one street's filter.

Result: on multi-street hands, villain's actual betting history
(flop bet → turn check → river bet, say) is never composed into the
range computation. Every feature derived from villain range
composition reads an action-oblivious distribution.

## Owner repro (from playtest-logs)

Playtest session `river-rats-session-log-77221d98-2026-04-18T15-12-37Z.json`,
hand `H_8dfb6ef8`, board `5d 3s 5h`:

| Street | Action history | `facing_bet` | `vcb` | TP+ | Med | Draw | Air |
|---|---|---|---|---|---|---|---|
| Flop  | BB BET, hero CALL | 1 | 0 | 0.60 | **0.00** | 0.02 | 0.39 |
| Turn  | BB CHECK, hero BET, BB CALL | 0 | 0 | 0.31 | **0.01** | 0.01 | 0.67 |
| River | BB BET (into hero) | 1 | 1 | 0.72 | **0.001** | 0.00 | 0.28 |

Owner's read: "Villain range on turn had medium hands, then he
checked, river range was narrowed to almost no medium hands." The
observation is correct — and it exposes the single-street narrowing
behavior rather than a narrowing-direction mis-call.

- On the **turn**, villain had already bet the flop and was about to
  check. The turn range (raw preflop, 67% air) is NOT the post-flop-bet
  continuing range (which would be substantially tighter and less air-
  heavy). Medium-made is 1% because the raw preflop range is sparsely
  medium on a paired low board.
- On the **river**, villain bet. Narrowing runs `narrow_to_betting_range`
  against `RIVER_BETTING_FREQUENCIES`, starting again from the raw
  preflop range (not from the turn-check-continuing range). Medium-made
  drops to 0.1% because medium hands don't value-bet the river per the
  betting-frequency table. **Correct for a bettor's river range, wrong
  relative to the path-conditioned range that actually brought villain
  here.**

The TP+ 0.72 at the river reflects the same single-street artifact
— it's "what river-betting hands look like from the preflop range,"
not "what river-betting hands look like conditional on this player
having bet-flop, check-turn, bet-river."

## Code location

`river-rats-core/feature_extractor.py` lines ~1141-1157 inside
`classify_villain_range()`:

```python
v_range = get_villain_range(hero_pos, villain_pos, opener_pos=opener_pos)
# ...
street_name = STREET_NAME_MAP.get(street_raw, 'flop')
if facing_bet:
    v_range = narrow_to_betting_range(v_range, board_cards, street_name)
```

No `narrow_to_checking_range` call on prior streets. No chaining.
`street_name` is the CURRENT street; action_history from prior
streets isn't consulted.

Same pattern inside `compute_flush_block_pct()` (Step 12) and — by
extension — inside `blocker_features.compute_block_percentages()`
(the v2.4 Step 17 wiring I just landed), which receive the same
single-street-narrowed range.

## Blast radius

All features derived from villain range composition:
- `villain_top_pair_plus_pct`
- `villain_medium_made_pct`
- `villain_draw_pct`
- `villain_air_pct`
- `villain_range_capped`
- `board_favour`
- `villain_fold_equity_estimate` (derived from TP+/draw/air)
- `flush_block_pct`
- **[v2.4 NEW]** `flush_draw_block_pct`
- **[v2.4 NEW]** `straight_draw_block_pct`
- **[v2.4 NEW]** `nut_made_block_pct`

Every training row across v2.2 / v2.3.1 / v2.3.2 carries this bug
in the villain-composition columns. Fix + re-extract would shift
those feature values across the entire dataset.

## Proposed fix — action-aware narrowing

Replace the single-street narrowing call with a chained narrowing
that walks the action history street-by-street:

```python
def narrow_by_action_history(
    full_range, board_cards, current_street, action_history, villain_pos
):
    """Chain narrow_to_betting/checking_range across the action history
    so villain's CURRENT range is properly conditioned on every prior
    decision they took.

    For each street ordered preflop→flop→turn→river (up to current):
      1. Collect villain's action on that street (bet/raise/call/check/fold)
      2. If bet/raise: apply narrow_to_betting_range for THAT street's
         board slice
      3. If check: apply narrow_to_checking_range for THAT street's
         board slice
      4. If call/fold: call narrowing is trickier (calls typically don't
         narrow as sharply as bets; folds are terminal) — start with
         treating call the same as "continuing range" heuristic

    Each narrowing step uses the board as it existed on THAT street
    (3 cards flop, 4 turn, 5 river), NOT the current-decision board.
    """
```

The narrowing should use the street-local board, not the current
board, so a flop-bet narrowing examines only the flop cards.

Implementation notes:
- `range_narrowing.py` already has both betting and checking frequency
  tables keyed by street — they're there, just not chained.
- Need a new helper `narrow_to_continuing_range()` for the
  call-or-raise-but-not-fold case (approx = narrow_to_betting_range
  minus folds, plus some calls that wouldn't bet).
- Must handle facing_bet on prior streets — villain's "call" after
  hero's bet is a distinct continuation pattern.

## Scope recommendation — where this fits v2.4

Per current directive-x 6-stage ship sequence:

1. ✅ Stage 1 — features + backfill audit (complete)
2. ✅ Stage 2 — KB §1.10-§1.12 (complete)
3. 🔜 Stage 3 — v3.2 prompt derivation (next, no feature dependency)
4. Stage 4 — training data expansion + re-label with v3.2
5. Stage 5 — retrain + full eval
6. Stage 6 — ship gate

**Proposal: insert as new Stage 3.5 — "action-aware range narrowing"**
between Stage 3 and Stage 4.

Why this placement:
- **Must land BEFORE Stage 4 re-labelling.** Stage 4 computes new
  training feature values for re-labelled hands. If villain ranges
  are still single-street, the 4 new blocker features and the
  existing composition quad all get computed wrong for the new
  labels. Baked into v2.4 training data.
- **Cannot land in Stage 3.** Stage 3 is prompt derivation —
  prose, no feature changes. Mixing unrelated concerns breaks
  Stage 3's tight scope.
- **Cannot wait until Stage 5.** By Stage 5 the retrain is running;
  fixing features mid-retrain requires redoing all preceding stages.

Stage 3.5 content:
1. Specify `narrow_by_action_history()` + `narrow_to_continuing_range()`
   (helper for call case)
2. GTO reviewer pass on the narrowing semantics BEFORE code (same
   discipline as v2.4 P1 plans)
3. Implement in `range_narrowing.py` + wire `classify_villain_range`
   and `compute_flush_block_pct` + `blocker_features` to use it
4. Unit tests on synthetic multi-street action histories
5. Retroactive audit: re-extract v2.3.1 training CSV, compare
   villain composition columns pre-fix vs post-fix — document the
   distribution shift
6. Calibration-anchor regression check — do anchors still pass?

Budget estimate: ~3-5 hours implementation + review. Less than a
full stage; insertion between stages is proportionate.

## Interaction with other v2.4 tickets

- **TICKET_HAND_EVALUATOR_DRAW_SEMANTICS** — independent; fix
  alongside as bundled feature-correctness work for v2.4
- **TICKET_BLOCKER_DIRECTION_DEFENSIVE** — this ticket's fix
  materially improves the defensive-blocker reasoning (villain's
  post-action range is what densification operates on)
- **v2.4 P1 blocker features** — bar raises from "probably wrong"
  to "actually correct" since `compute_block_percentages` iterates
  whatever range it's given

## Not blocking v2.2 production

Game stays on v2.2. No urgency on prod. This is a v2.4 correctness
gate, not a v2.3.1 blocker.

## Risks / unknowns

- Action-aware narrowing may shift villain composition values
  materially across the training set. v2.3.1 model's anchor gate
  could fail after re-extraction because anchors' villain
  compositions will differ. Need to run anchor-gate audit before
  declaring the fix safe.
- Computational cost: chaining narrowing across 3 streets triples
  the range-filtering work. Likely tolerable (<50ms per decision)
  but worth measuring.
- `narrow_to_continuing_range` (call case) is not solver-verified.
  Needs GTO review — possibly punt to "treat call = light
  narrowing towards medium/draw strength" for MVP.

## Action requested

Confirm the proposed scope placement (Stage 3.5). If approved, I'll
draft the plan doc (same format as P1 plans) and dispatch a GTO
reviewer subagent on the narrowing semantics before writing code.

Stage 3 (v3.2 prompt derivation) can proceed in parallel on owner go.
