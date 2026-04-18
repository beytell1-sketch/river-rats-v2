---
date: 2026-04-18
from: Builder
to: Main terminal / Owner
re: v2.3.1 Layer 2 — BLOCKER: litmus seeds cannot satisfy villain_checked_back predicate
status: BLOCKED — awaiting decision between two clean paths
---

# Blocker — Litmus vs `villain_checked_back` Bridge Semantics

Ran 10-spec yield test (per CLAUDE.md §2, assumption validation).
Both litmus seeds build cleanly and produce the feature values
we'd expect (A4d eq=0.096, T5h eq=0.155, board_adjusted_hrp 0.092
/ 0.023 respectively). BUT both fail the predicate on
`villain_checked_back=0 (expected 1)`.

## Root cause

Both `game_state_bridge.py` (factory path) and
`pokerbench_parser.py` (PokerBench ingest) compute
`_villain_checked_back` using **prior streets only**, not the
current street:

```python
# game_state_bridge.py line 107
for s in street_sequence[:current_idx]:   # PRIOR streets
    for name, pos, act in game.street_actions.get(s, []):
```

```python
# pokerbench_parser.py line 239-241
# Don't commit current street — that's the decision point street
```

So a flop decision with villains having checked before hero acts
on the flop gets `villain_checked_back=0`. To get
`villain_checked_back=1`, we need villain action on a PRIOR
street — i.e., the decision must be on the turn (with flop
check-through) or later.

## Consequence for update-g Layer 2

Update-g §Layer 2 lists two requirements that conflict at the
factory layer:

- `villain_checked_back=1` (requires non-flop decisions)
- "Spread across streets (flop/turn)" (allows flop)

The TWO playtest litmus hands (A4d/Qs5s7s and T5h/JJ2) are both
flop decisions. They cannot pass `villain_checked_back=1` through
the factory.

## Re-reading update-g

Update-g's Finding-comparison table for A4d/T5 lists HRP,
board_adjusted_hrp, equity, worse_hand_pct, villain_air_pct,
is_made_hand, has_showdown_value — but NOT
`villain_checked_back`. The narrative says "High villain_air +
checked_back misleads" for T5. That may be the *pattern* the
model learned from turn/river training data and is now
over-firing on flop spots where villain_checked_back actually
equals 0 but related features (villain_air_pct, facing_bet=0)
are shaped similarly.

If so, Layer 2's job is to teach the model "AIR + villain_air_pct
high + villain_checked_back=1 → CHECK" using turn/river spots
(the only places the predicate can fire), and Layer 1
(board_adjusted_hrp) handles the flop playtest spots directly via
the board-adjusted signal (A4d: 0.096, T5h: 0.155 — both very
low).

## Two paths

### Path A — Keep litmus as FLOP seeds; drop `villain_checked_back=1` for them

Rationale: the litmus hands ARE the playtest spots — keep them
as training samples even if they don't pass the generator's
universal predicate. Predicate applies to the other 28–38
counter-examples (turn/river only). Litmus seeds tagged
`bucket=LITMUS_FLOP_AIR_CHECK` distinct from the main
`AIR_CHECK_3WAY` / `AIR_CHECK_HU` buckets.

Pros:
- Training data literally includes the exact playtest spots
- Model memorizes them → guaranteed CHECK at inference

Cons:
- Mixed predicate (one bucket has vcb=0, others have vcb=1)
- "Hard-fail on litmus" adjustment #2 needs relaxation (fail on
  validator/build error only, not predicate mismatch for LITMUS
  bucket)

### Path B — Move litmus seeds to TURN (with flop check-through)

Seeds become: A4d on [Qs,5s,7s, + safe turn card] with flop
check-through history; T5h on [Jc,Jd,2h, + safe turn card] with
flop check-through. Same hero + flop + villain weakness context,
just shifted one street.

Pros:
- Single consistent predicate across all generated rows
- Matches bridge semantics cleanly
- Hard-fail adjustment #2 remains intact
- Arguably more general teaching signal (air+vcb=1+checked-through
  across all streets)

Cons:
- Training data doesn't literally contain the playtest spots
  (flop vs turn — different street encoding in feature 1)
- Relies on the model generalizing across `street` feature
  (which it's supposed to do, but it's an assumption)

### Builder recommendation

**Path B.** Layer 1's `board_adjusted_hrp` already addresses the
flop playtest spots directly (values 0.092 / 0.023 are very low
— model should now see these as weak). Layer 2's job is to teach
the broader pattern (AIR + checked-back + air-heavy villain →
CHECK), which only manifests cleanly on turn+. Path B produces
consistent, predicate-clean training data; the model's
street-invariant generalization handles the playtest spots.

If reviewer wants the literal playtest spots in training, Path A
is clean too — just needs adjustment #2 relaxed for the LITMUS
bucket.

## What I've done / not done

- Generator script written: `review/generate_air_check_v231.py`
- 10-spec yield test surfaces this blocker
- No JSONL output written yet — holding for direction

Decision needed on A vs B. I'll switch to either in ~5 minutes
of code change and re-run.
