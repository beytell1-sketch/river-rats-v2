---
date: 2026-04-20
from: Builder
to: Main terminal / Owner (for scope decision + GTO-reviewer dispatch)
re: Range-narrowing — expert review prep. IS vs SHOULD vs PLAN vs CAN'T
status: CLARITY DOC — no code. Awaiting owner review + GTO-reviewer dispatch before plan.
related: TICKET_RANGE_NARROWING_ACTION_HISTORY_2026-04-20.md, owner-flagged 2026-04-20
---

# Range-Narrowing — IS / SHOULD / PLAN

Per owner request: exact clarity on current behavior, poker-correct
behavior, and what's buildable under current architecture — so GTO
reviewer can assess before any code lands.

## The owner's scenario (corrected)

Owner example: **turn was checked through** (hero checked, villain
checked behind). On the river, villain bet. Villain's river range
was narrowed to "almost no medium hands."

My earlier trace (`H_8dfb6ef8`) was a different shape — villain
BET-checked-CALLed, not check-through. **Only one hand across the
four playtest logs has a clean turn check-through**
(`H_d9edab5d`), and that session (2026-04-18T14-36) logged with an
empty features dict, so we can't see the villain composition
numbers directly. The diagnosis below is therefore based on
**reading the code** + solver theory, not on a full playtest trace.
If owner has a fresher example with populated features I'd like to
see it; otherwise the code-read is authoritative.

## Part 1 — IS (current behavior)

### Code path

`river-rats-core/feature_extractor.py::classify_villain_range()`:

```python
# Step 1: Get FULL preflop range (opener-aware)
v_range = get_villain_range(hero_pos, villain_pos, opener_pos=opener_pos)

# Step 2: If facing a live bet, narrow to betting range on CURRENT street
if facing_bet:
    v_range = narrow_to_betting_range(v_range, board_cards, street_name)

# Step 3: Classify (count TP+ / draw / air in this range)
for hand_notation, freq in v_range.items():
    ...
```

That's it. No other narrowing. No check narrowing. No chaining.

### What this produces per action class

| Hero context | Code behavior | Villain range used for composition |
|---|---|---|
| **Flop, facing bet** | narrow → flop betting range | preflop ∩ flop-bet (OK-ish) |
| **Flop, checked-to** | no narrow | preflop (wrong — should be preflop ∩ flop-check) |
| **Turn, facing bet** | narrow → turn betting range | preflop ∩ turn-bet (wrong — misses flop action) |
| **Turn, checked-through (facing_bet=0)** | no narrow | preflop (wrong — should compose flop+turn history) |
| **River, villain bet after turn check-through** | narrow → river betting range | preflop ∩ river-bet (wrong — misses turn check-through) |
| **River, villain bet after bet-call line** | narrow → river betting range | preflop ∩ river-bet (wrong — misses flop bet, turn bet) |

### The owner's scenario under this code

River, hero faces villain's bet after turn check-through:
- `v_range = get_villain_range(...)` — raw preflop opener range
- `facing_bet = 1` → `v_range = narrow_to_betting_range(v_range, river_board, 'river')`
- Composition computed on `preflop ∩ river-bet`

**Not used anywhere:**
- flop checking (flop was bet-and-called — wait, in this specific scenario flop is unknown; let's assume whatever happened)
- turn check-through — the single most important signal about villain's range given they declined to bet

Medium hands disappear because `RIVER_BETTING_FREQUENCIES['medium_made'] = 0.08` (solver-correct for a value-bettor's river range). The filter is correct; the **baseline range it's applied to is wrong**.

## Part 2 — SHOULD (poker-correct per solver)

### General principle

Villain's range at any decision is the **intersection of every
street's continuing range**:

```
current_range = preflop_opener_range
  ∩ flop_action_continue_range(board_flop, villain_flop_action)
  ∩ turn_action_continue_range(board_turn, villain_turn_action)
  ∩ river_action_continue_range(board_river, villain_river_action)
```

"Continue" means: filter to hands that would have taken the action
villain actually took, per solver frequencies. Each street's
continue-range is a narrowing, not a full resampling.

### Per action class (solver-grounded, from KB §1.3 + tables in range_narrowing.py)

| Villain action | Narrow by | Availability in code today |
|---|---|---|
| **BET / RAISE** | `narrow_to_betting_range(range, street_board)` | ✅ Function exists |
| **CHECK** | `narrow_to_checking_range(range, street_board)` | ✅ Function exists but NEVER called from feature extraction |
| **CALL** | "continuing range" ≈ calls-a-bet filter (hands that call but don't raise) | ❌ No function |
| **FOLD** | Terminal — no continuing range; hand excluded from further sampling | N/A |

### Owner's scenario SHOULD-behavior

River, hero faces villain's bet after turn check-through:

1. Preflop: BB defend → `get_villain_range(BB-defend-vs-opener)`. Baseline.
2. Flop action: whatever happened — if villain faced hero's bet and called, narrow by `call-continue`; if villain bet, narrow by `bet`; etc.
3. Turn: villain checked (check-through) → apply `narrow_to_checking_range(turn_board, 'turn')`. Medium-made retained at 70%.
4. River: villain bet → apply `narrow_to_betting_range(river_board, 'river')`. Medium-made falls to 8%.

Net effect on medium-made (assuming it was 15% of the preflop range): `15% × [flop-continue-freq] × 70% × 8%`. Depending on flop action, medium stays at 1-2% of the current range — much lower than turn check-through alone would suggest, but **correctly reflecting that villain went from "check turn (keeps mediums)" to "bet river (drops mediums)".**

The user's observation "medium hands disappear" is actually **correct** at the river: medium hands don't value-bet the river. The **surprise** is that the intermediate turn-check-through state didn't produce higher medium counts — because the turn-check-through state was **never computed**. The river betting filter sees it fresh off the preflop range.

### KB §1.3 grounding

v3.1 KB §1.3 (C-Bet Frequency) gives the solver-sourced betting
frequencies. §1.4 (Bluff-to-Value) gives river-specific filters.
The existing `RIVER_BETTING_FREQUENCIES` and `RIVER_CHECKING_FREQUENCIES`
tables in `range_narrowing.py` encode these values correctly. The
tables aren't the bug — the **application** of the tables is.

## Part 3 — CAN (clean implementation)

### 3.1 Chain the betting + checking narrowing (ACHIEVABLE)

Add `narrow_by_action_history(range, board_cards, action_history, villain_pos)`:

```python
def narrow_by_action_history(full_range, board_cards, action_history, villain_pos):
    """Walk villain's action history street-by-street, applying bet or check
    narrowing at each step using THAT street's board slice."""
    STREETS = ['flop', 'turn', 'river']
    BOARDS_BY_STREET = {'flop': board_cards[:3], 'turn': board_cards[:4], 'river': board_cards[:5]}

    current_range = dict(full_range)

    for street in STREETS:
        # Villain's action on this street (first aggressive or check action)
        v_actions = [a for a in action_history
                     if a['street'] == street and a['position'] == villain_pos]
        if not v_actions:
            continue  # villain didn't act this street

        # Use the FIRST action villain took this street (pre-hero-response)
        first = v_actions[0]['action']
        street_board = BOARDS_BY_STREET[street]

        if first in ('BET', 'RAISE'):
            current_range = narrow_to_betting_range(current_range, street_board, street)
        elif first == 'CHECK':
            current_range = narrow_to_checking_range(current_range, street_board, street)
        elif first == 'CALL':
            current_range = narrow_to_continuing_range(current_range, street_board, street)
        elif first == 'FOLD':
            return {}  # terminal — villain out of hand
        # If villain acted twice (e.g. check-raise), second action is a
        # raise; that narrows further. Handle as a subsequent narrow_to_
        # betting_range call.

        # Second action (response to hero's action on same street)
        if len(v_actions) > 1:
            second = v_actions[1]['action']
            if second in ('BET', 'RAISE'):
                current_range = narrow_to_betting_range(current_range, street_board, street)
            elif second == 'CALL':
                current_range = narrow_to_continuing_range(current_range, street_board, street)
            elif second == 'FOLD':
                return {}

    return current_range
```

Clean refactor. Preserves backward compat (existing callers go through
a shim). Unit-testable on synthetic action histories. ~50 LOC
implementation + tests.

### 3.2 Hook into feature extraction (ACHIEVABLE)

Replace the `if facing_bet: narrow_to_betting_range(...)` block
with:

```python
action_history = hand.get('_action_history', [])  # full action list
if action_history:
    v_range = narrow_by_action_history(v_range, board_cards, action_history, villain_pos)
elif facing_bet:
    # fallback: old behavior for hands without action history
    v_range = narrow_to_betting_range(v_range, board_cards, street_name)
```

Preserves backward compat with hands that don't carry action history
(some test harnesses). For hands that DO carry history, the chained
narrowing applies.

### 3.3 Compute cost (ACHIEVABLE, low risk)

Chaining 3 narrow calls across flop/turn/river instead of 1 ≈ 3x
cost per range computation. Current cost is <20ms per decomposition
(per range_decomposition.py header). Expect <60ms after the fix.
Not a production constraint.

## Part 4 — CAN'T (architectural limits)

### 4.1 Call-continue frequencies are NOT solver-verified

For BET and CHECK actions we have solver-grounded frequency tables
in `range_narrowing.py`. For **CALL** we don't. A "call-continuing
range" has to be approximated heuristically:

- Hands that call a bet: not the nuts (would raise), not the worst
  air (would fold), but include mediums, draws, weak made hands.
- Possible approximations:
  - `narrow_to_continuing_range(range) ≈ range minus hands that would fold
    AND minus hands that would raise`
  - i.e., a band of equity in the "call" zone

But the thresholds for "would fold" vs "would call" vs "would
raise" depend heavily on bet size, position, and villain identity —
solver data on CALL classes is less standardized than bet/check.

**Risk if we ship a naive call-narrow:** the approximation biases
villain composition on every multi-street bet-called decision. Not
fatal, but not solver-clean either.

**Option A:** implement a crude call-narrow (treat call as
"non-fold and non-raise" — strips air + strips the top of value),
ship it, document the heuristic, verify against playtest traces.

**Option B:** defer call-narrow — leave the range un-narrowed on
CALL actions. This is what the code does today implicitly for some
cases, but it's directionally wrong (too-wide range → overstates
air and draws).

**Option C:** solver-derive call tables — multi-day effort with
GTO Wizard or similar. Not in scope for a single stage.

GTO reviewer's opinion on A vs B vs C is the key scope question.

### 4.2 Raise reopens action (CAN but messy)

If villain CALLED hero's raise, vs. CALLED hero's initial bet,
those are different ranges (raise-call is much tighter). The
generic `narrow_to_continuing_range` loses this distinction unless
we expose `facing_raise`-aware variants. Can be handled via a
second check on `action_history` entries' preceding-action, but
adds complexity.

Recommendation: start without raise-aware call narrowing, observe
playtest impact, add only if it materially changes outputs.

### 4.3 Multiway complications

In 3-way, villain A's range depends on what villain B did too. If
villain A called after villain B bet, A's range is tighter than if
A faced hero's bet alone. `narrow_by_action_history` for "primary
villain" can only track that one seat's actions — multiway
interactions are approximations.

Not a blocker for v2.4 since all existing features are
per-primary-villain anyway. Just noting the limitation.

### 4.4 Baseline ranges are position-coarse

`get_villain_range` returns a position-level preflop range (e.g.,
"BB defend vs CO open"). Actual hand-level ranges vary by opponent
stack size, game flow, and player type. Our model doesn't have
opponent-specific priors. Not new; not in scope for this ticket.

## Part 5 — PROPOSED PLAN (what goes to GTO reviewer)

### Inside this ticket's scope

1. **Implement `narrow_by_action_history`** per §3.1
2. **Ship naive CALL narrow (Option A from §4.1)**: `narrow_to_continuing_range = range minus folds minus raises`, using `FOLD_FREQUENCIES` ≈ (1 - CALL_FREQ - RAISE_FREQ). Solver frequencies we already have cover bet/check, not call directly — approximation to be documented in code + KB.
3. **Hook into feature_extractor** per §3.2
4. **Update `compute_flush_block_pct` + `blocker_features.compute_block_percentages`** to use the newly narrowed range (they import villain range via caller, so likely no changes at their level — the chain flows from `classify_villain_range` upstream).
5. **Unit tests** on synthetic action histories: flop-bet-call-turn-check-river-bet, flop-check-through-turn-bet-call-river-check, etc.
6. **Retroactive audit** on v2.3.1 training CSV: re-extract villain composition columns, compare to stored values. Document the distribution shift.
7. **Calibration-anchor regression check** on v2.3.1 model: do the 5 anchors still pass with the new range? Expected: YES on the shape anchors (A4d, T5h, AA, KQ flop), UNSURE on d2410 (turn decision with checked-back history — the chained narrowing will change its feature values).

### Explicitly punted to later

- **Solver-derive CALL tables** (Option C §4.1) → v2.5 or separate research ticket.
- **Raise-aware call narrow** (§4.2) → if playtest reveals bias, add.
- **Multiway range cross-conditioning** (§4.3) → not in v2.4 scope.

### Scope placement

Per earlier ticket: **Stage 3.5** — between v2.4 Stage 3 (v3.2
prompt derivation, no feature dependency) and Stage 4 (re-label).

Must land before Stage 4 re-labelling — Stage 4 computes new
feature values against villain ranges, and those ranges need to
be action-aware before new labels enter v2.4 training.

## What GTO reviewer needs to answer

1. **Is the SHOULD column (Part 2) poker-correct?** Especially:
   - Turn-check-through keeps medium hands at 70% per
     TURN_CHECKING_FREQUENCIES — does that match solver behavior?
   - River-bet filter is correct at 8% medium per
     RIVER_BETTING_FREQUENCIES — confirmed solver-grounded?
   - Is the "chained narrowing = intersection of per-street
     continues" the right mental model, or does solver theory
     call for something else (e.g., fresh conditional computation
     per street)?

2. **Option A call-narrow (naive "non-fold non-raise")** — is
   this acceptable as a v2.4 MVP, or is it materially wrong
   enough that we should defer and leave CALL un-narrowed?

3. **Raise-aware call narrowing** — needed for v2.4 or deferrable?

4. **Multiway** — do we need a different range per primary villain,
   or is current "villain = opener or bettor" good enough?

5. **Calibration-anchor risk** — any of the 5 anchors likely to
   flip action after this fix? If d2410 flips (TPGK on turn,
   checked by villain-then-hero flop, now-facing-bet on turn)
   we need to re-anchor or accept the fix changes the decision.

## What I'd like owner to confirm before GTO dispatch

- **Stage 3.5 placement**: accepted or revise?
- **Scope of this ticket**: §5 proposed plan acceptable?
- **Parallel Stage 3** — proceed with v3.2 prompt derivation while
  this plan is reviewed?

Once owner confirms, I'll:
1. Dispatch GTO reviewer on this doc
2. Incorporate reviewer verdict into the spec
3. Implement + audit per §5
4. Report Stage 3.5 complete; Stage 4 gate then re-opens

Standing by.
