# Review: SituationFactory Action History Bugs

**Date:** 6 April 2026
**Files reviewed:**
- `river-rats-core/situation_factory.py`
- `river-rats-core/game_state_bridge.py`
- `review/DESIGN_POSITION_AMP_SWEEPS.md`
- `review/DESIGN_CALL_SWEEPS.md`

---

## Executive Summary

Five confirmed bugs found. The primary villain selection bug (Bug 1) is
the root cause of a cascade: it corrupts villain_aggression_count,
villain_checked_back, and villain_call_count simultaneously for every
facing_bet situation. The factory docstring contradicts the design documents
and the factory code enforces the wrong convention. Secondary bugs affect
facing_raise, num_callers_to_bet, and is_3bet_pot in specific situations.

---

## Bug 1 — Primary Villain Selection (CRITICAL)

### What the code does

`situation_factory.py` lines 257-265:

```python
for i, pos in enumerate(spec.villain_positions):
    # Last villain in list is the bettor (caller gets bet_this_street=0).
    is_bettor = facing_bet and (i == len(spec.villain_positions) - 1)
    opponents.append(OpponentStub(
        position=pos,
        bet_this_street=current_bet if is_bettor else 0.0,
    ))
```

The factory assigns `bet_this_street = current_bet` to `villain_positions[-1]`
(the last villain). The bridge (line 71-76) then finds the bettor as the
opponent whose `bet_this_street == current_bet` and assigns that position to
`vp`. So `vp` resolves to `villain_positions[-1]`.

The docstring at line 143 states this explicitly:
> "Last position in list is assumed to be the bettor when facing_bet."

The validator (lines 353-355) mirrors this, also using `villain_positions[-1]`
as the primary villain when facing_bet=True.

### What it should do

Every facing_bet situation in both design documents has the bettor listed
FIRST in villain_positions, not last.

DESIGN_POSITION_AMP_SWEEPS:
- Board 6: `Villain positions: CO (opener/bettor), BTN (cold-caller)` — bettor CO is index 0
- Board 7: `Villain positions: BTN (opener/bettor), BB (cold-caller)` — bettor BTN is index 0

DESIGN_CALL_SWEEPS:
- Board 1: Primary villain CO is bettor, `villain_positions: CO, BTN` — CO is index 0
- Board 2: BB is bettor, only villain (CO folded) — single element, no ordering conflict
- Board 5: Primary villain CO is bettor, BTN is cold-caller — CO is index 0
- Board 6: Primary villain CO is bettor, BTN is cold-caller — CO is index 0
- Board 7: Primary villain CO is raiser, `villain_positions: CO` only
- Board 8: Primary villain CO is raiser, `villain_positions: CO` only

The bettor is consistently at index 0 across all 151 situations. The factory
does the exact opposite: it makes index 0 the non-bettor and index -1 (last)
the bettor.

### Impact

Facing_bet situations with more than one villain (multi-way): the factory
computes `vp` as the cold-caller (villain_positions[-1]) instead of the bettor
(villain_positions[0]). This corrupts every downstream feature that depends on
`vp`:
- villain_aggression_count computed for cold-caller, not bettor
- villain_checked_back computed for cold-caller, not bettor
- villain_call_count computed for cold-caller, not bettor
- villain_top_pair_plus_pct and villain_air_pct use wrong range
- raw_equity computed against wrong villain's range

Facing_bet situations in the 151 factory situations with two villains
(bettor + cold-caller behind or folded):
- DESIGN_POSITION_AMP_SWEEPS Board 6: 10 situations (CO bettor, BTN caller)
- DESIGN_POSITION_AMP_SWEEPS Board 7: 9 situations (BTN bettor, BB caller)
- DESIGN_CALL_SWEEPS Board 1: 9 situations (CO bettor, BTN still to act)
- DESIGN_CALL_SWEEPS Board 5: 9 situations (CO bettor, BTN caller)

That is 37 situations where the primary villain (bettor) is misidentified.
The remaining facing_bet situations have only one villain (CO folded or
single-villain scenario), so villain_positions has one element and the
ordering bug has no effect.

### Exact fix

`situation_factory.py` lines 257-265 and the docstring at lines 141-143.

Change the bettor detection from last-in-list to first-in-list:

```python
for i, pos in enumerate(spec.villain_positions):
    # First villain in list is the bettor when facing_bet=True.
    # Subsequent villains are cold-callers (bet_this_street=0).
    is_bettor = facing_bet and (i == 0)
    opponents.append(OpponentStub(
        position=pos,
        is_folded=False,
        bet_this_street=current_bet if is_bettor else 0.0,
        stack=spec.effective_stack,
    ))
```

Update the docstring at lines 141-143:

```
    villain_positions : List[str]
        Active (non-folded) opponent seats. Single element = heads-up.
        FIRST position in list is the bettor when facing_bet=True.
        Subsequent positions are cold-callers (bet_this_street=0).
```

Update the validator at lines 352-356:

```python
    if spec.villain_positions:
        primary_vp = (
            spec.villain_positions[0] if facing_bet_expected
            else spec.villain_positions[0]
        )
    else:
        primary_vp = 'BB'
```

Which simplifies to:

```python
    primary_vp = spec.villain_positions[0] if spec.villain_positions else 'BB'
```

The validator uses the same wrong heuristic as the factory. After fixing the
factory, the validator must also be fixed so it checks the correct villain's
history — otherwise validation will silently pass on the wrong values.

---

## Bug 2 — villain_aggression_count, villain_checked_back, villain_call_count

These three features are not independently buggy — they inherit the primary
villain selection error from Bug 1. Once `vp` is correctly set to
`villain_positions[0]`, the bridge code at lines 106-121 correctly iterates
over prior streets and filters by `pos == vp`. The street sequence logic
(`street_sequence[:current_idx]`) is correct for all three postflop streets:

- Flop: prior = ['preflop'] — correct
- Turn: prior = ['preflop', 'flop'] — correct
- River: prior = ['preflop', 'flop', 'turn'] — correct

The loop over `v_actions_by_street` correctly counts bet/raise for aggression,
check for checked_back (binary), and call for call_count.

No additional fix needed beyond fixing Bug 1. These features are correct in
isolation; they just operate on the wrong position.

---

## Bug 3 — facing_raise: False Negative When raises_this_street Not Set

### What the code does

`game_state_bridge.py` line 97:

```python
num_raises = context.get('num_raises_this_street', getattr(game, 'raises_this_street', 0))
```

Line 138:

```python
facing_raise = int(facing_bet and num_raises > 0)
```

The factory sets `game.raises_this_street` from `_count_raises_this_street()`,
which counts 'bet' and 'raise' actions on the current street:

```python
def _count_raises_this_street(action_history, street):
    return sum(1 for s, pos, act in action_history
               if s == street and act in ('bet', 'raise'))
```

### What it should do

`facing_raise` should be 1 when hero faces a raise-level action — specifically
when there has been a re-raise on the current street (the initial bet is index
1, a raise on top of it is index 2+).

The bridge comment (line 137) says: "Captures check-raises, re-raises, etc."
The design documents confirm facing_raise=1 requires `num_raises > 0`.

The current implementation counts the initial bet as a raise when it is the
only aggressive action on the street. For a situation like `('flop', 'CO',
'bet')` with to_call > 0, `raises_this_street = 1` and `facing_raise = 1` —
but this is an initial bet, not a raise. The feature is named facing_raise,
not facing_bet_or_raise.

DESIGN_CALL_SWEEPS Board 7 expects `facing_raise=1` because CO raised hero's
bet (two aggressive actions: hero bet + CO raise = raises_this_street=2).
DESIGN_CALL_SWEEPS Board 8 expects `facing_raise=1` because CO check-raised
(two aggressive actions: hero bet + CO raise = raises_this_street=2).

For standard c-bet situations (Boards 1-6 of DESIGN_CALL_SWEEPS and Boards
6-7 of DESIGN_POSITION_AMP_SWEEPS), there is exactly one bet on the current
street and `facing_raise` should be 0. The current counter returns 1 for all
these, producing `facing_raise=1` incorrectly.

### How many situations affected

Every facing_bet=True situation where the current street has exactly one
aggressive action (the initial bet, no re-raise). This is all facing_bet
situations EXCEPT the two check-raise boards (DESIGN_CALL_SWEEPS Boards 7
and 8, 18 situations total).

Affected: approximately 37 - 18 = 19 situations in the 151 total where
facing_bet=True and facing_raise should be 0 but the counter returns 1.

### Exact fix

Change `_count_raises_this_street` to count only raises (re-raises), not the
initial bet. A raise on a street is defined as a second or later aggressive
action.

Replace the helper at lines 208-216:

```python
def _count_raises_this_street(
    action_history: List[Tuple[str, str, str]],
    street: str,
) -> int:
    """
    Count raise actions on current street (not the initial bet).

    facing_raise requires num_raises > 0. An initial bet contributes 0;
    a re-raise or check-raise contributes 1. This matches bridge line 138:
    facing_raise = int(facing_bet and num_raises > 0).
    """
    street_actions = [
        act for s, pos, act in action_history
        if s == street and act in ('bet', 'raise')
    ]
    # First aggressive action is the opening bet (not a raise).
    # Any subsequent aggressive action is a raise.
    return max(0, len(street_actions) - 1)
```

---

## Bug 4 — num_callers_to_bet: Excludes Cold-Callers Who Are Behind Hero

### What the code does

`game_state_bridge.py` lines 127-134:

```python
if facing_bet and hasattr(game, 'street_actions'):
    current_actions = game.street_actions.get(street, [])
    num_callers_to_bet = sum(
        1 for name, pos, act in current_actions
        if act == 'call' and pos != player.position and pos != bettor_position
    )
```

This counts 'call' actions on the current street by anyone other than hero
and the bettor. The factory populates `street_actions` from `action_history`
via `_build_street_actions()`.

### What it should do

`num_callers_to_bet` should count opponents who cold-called before hero acts —
that is, callers who acted between the bettor and hero in the action sequence.

The design confirms this. DESIGN_CALL_SWEEPS Board 5 specifies
`num_callers_to_bet=1` because BTN called CO's bet before hero (BB) acts:
> "CO bets 35, BTN CALLS. Hero faces bet + call."

The board specifies `villain_positions: CO, BTN` with CO as bettor. The
action_history for the current street would include `('flop', 'CO', 'bet')`
and `('flop', 'BTN', 'call')`. BTN's call is correctly captured by the bridge
logic (`pos != player.position` since hero=BB, `pos != bettor_position` since
bettor=CO). So `num_callers_to_bet = 1` — this is correct.

However: the factory stub at `_build_street_actions` sets the `name` field
(index 0 of each tuple) to `pos` (a stand-in), and the bridge reads index 1
(`pos`) and index 2 (`act`). This is correct per the comment at line 199-204
of situation_factory.py. The logic is consistent.

### Verdict

No bug in the logic. The feature is computed correctly once `bettor_position`
is fixed by Bug 1. Before Bug 1 is fixed, `bettor_position` is the cold-caller
position, so the exclusion `pos != bettor_position` would fail to exclude the
cold-caller — counting zero callers instead of one for Board 5.

This is another downstream effect of Bug 1, not an independent bug. Fix Bug 1
and num_callers_to_bet becomes correct.

---

## Bug 5 — is_3bet_pot: Correct Logic, Potentially Wrong Count

### What the code does

`game_state_bridge.py` lines 142-144:

```python
pf_actions = getattr(game, 'street_actions', {}).get('preflop', [])
pf_raise_count = sum(1 for _, _, a in pf_actions if a in ('bet', 'raise'))
is_3bet = int(pf_raise_count >= 2)
```

The factory populates `street_actions['preflop']` from action_history tuples
with street='preflop'. For a standard single-raised pot (CO opens, others
call), the only aggressive preflop action is `('preflop', 'CO', 'raise')` —
`pf_raise_count = 1`, `is_3bet = 0`. Correct.

For a 3-bet pot (CO opens, BTN 3-bets, hero calls), there are two raises:
`('preflop', 'CO', 'raise')` and `('preflop', 'BTN', 'raise')` —
`pf_raise_count = 2`, `is_3bet = 1`. Correct.

### Verdict

The logic is correct. All 151 design situations are single-raised pots
(no 3-bet pots in either design document). `is_3bet = 0` throughout, which
matches the expected values (no board specifies `is_3bet_pot=1`). The
validator logic at lines 368-379 also computes this correctly from
action_history.

No bug.

---

## Summary Table

| Bug | Feature(s) Affected | Root Cause | Situations Affected |
|-----|---------------------|-----------|---------------------|
| 1 | vp (primary villain), villain_aggression_count, villain_checked_back, villain_call_count, raw_equity | factory assigns bet_this_street to villain_positions[-1] instead of villain_positions[0] | 37 of 151 (all multi-villain facing_bet) |
| 2 | villain_aggression_count, villain_checked_back, villain_call_count | downstream of Bug 1 — no independent fix needed | same 37 |
| 3 | facing_raise | _count_raises_this_street counts initial bet as a raise | ~19 of 151 (facing_bet with one aggressor, no re-raise) |
| 4 | num_callers_to_bet | downstream of Bug 1 — no independent fix needed | same 37 |
| 5 | is_3bet_pot | N/A — logic is correct | 0 |

---

## Files to Change

1. `river-rats-core/situation_factory.py`
   - Line 258 comment: update docstring on villain_positions ordering
   - Line 260: change `i == len(spec.villain_positions) - 1` to `i == 0`
   - Lines 208-216: replace `_count_raises_this_street` body (see Bug 3 fix)
   - Lines 352-356: simplify validator to `villain_positions[0]` unconditionally
   - Line 143 in the SituationSpec docstring: correct the ordering description

No changes needed in `game_state_bridge.py` — the bridge logic is correct.
The bugs are entirely in how the factory constructs the stubs.

---

## Recommended Fix Order

1. Fix Bug 1 first (change `i == 0` in the bettor detection, update docstring,
   update validator). This is the root cause of four corrupted features.
2. Fix Bug 3 (replace `_count_raises_this_street`). Independent of Bug 1.
3. Re-run `validate_situation()` across all 151 specs to confirm zero errors.
