# Blueprint: Phase 0 — action_string as Mandatory Field

## Status: READY TO IMPLEMENT

All referenced files exist. All functions are at the line numbers stated below.
Verified by direct source reads dated 2026-04-13.

---

## 1. What We Are Adding

Every situation record in the pipeline needs a canonical `action_string` field
that:
- Is human-readable (e.g. `"BB check, CO bet 45, BTN call 45, BB ???"`)
- Encodes the current-street action sequence up to the hero's decision point
- Is validated by `validate_action_string()` before the record is written
- Appears in JSONL output from `generate_3way_situations.py`
- Is passed through `label_3way_situations.py` unchanged
- Is NOT a model feature and does NOT appear in training CSV columns

---

## 2. Data Schema

### 2a. action_string format

```
"<POS> <action>[ <amount>], <POS> <action>[ <amount>], ..., <HERO_POS> ???"
```

Rules:
- Positions are uppercase seat names: `BB`, `CO`, `BTN`, `SB`, `UTG`, `HJ`, `MP`
- Actions are lowercase: `check`, `bet`, `call`, `fold`, `raise`
- Amounts are included only for `bet`, `call`, `raise` — integers (chips), no
  decimal unless fractional chips are in the game (they are not here)
- The hero's pending decision is always the final token: `<HERO_POS> ???`
- If the hero acts first on the street with no prior actions, the string is
  just `<HERO_POS> ???`

Examples by situation type:

| Scenario | action_string |
|---|---|
| Hero first to act (BB, no prior action) | `"BB ???"` |
| BB checks, hero (CO) faces check | `"BB check, CO ???"` |
| BB checks, CO bets 45, hero (BTN) faces bet | `"BB check, CO bet 45, BTN ???"` |
| BB checks, CO bets 45, BTN calls 45, hero (BB) last | `"BB check, CO bet 45, BTN call 45, BB ???"` |

### 2b. JSONL record schema (additions in bold)

```json
{
  "situation_id":       "d0001_CO_flop",
  "deal_id":            1,
  "hero_cards":         "AhKd",
  "board":              "Jh8c2s",
  "street":             "flop",
  "hero_position":      "CO",
  "villain_positions":  ["BB", "BTN"],
  "pot":                30,
  "to_call":            0,
  "facing_bet":         false,
  "num_opponents":      2,
  "prior_actions":      ["preflop: CO raise", "preflop: BB call", "preflop: BTN call"],
  "action_string":      "BB check, CO ???",
  "feat_dict":          { ... },
  "oracle_action":      "BET",
  "adjusted_action":    "BET",
  "equity":             0.6123
}
```

`action_string` sits at the top level, alongside `prior_actions`. It is NOT
nested inside `feat_dict`.

---

## 3. Source of action_string Data

`action_string` is derived from the game's postflop action log for the current
street — the same data that already flows through `poker_game.py` into the
`HeroDecision` struct (via `context['street_actions']` in `game_state_bridge.py`).

### What data is available at decision time

In `self_play.py`, the callback that creates a `HeroDecision` record already
has access to:
- `dec.player_position` — hero seat
- `dec.street` — current street
- `context` dict passed to `build_features_from_game_state()` — contains
  `game.street_actions` which is `{street: [(name, pos, action), ...]}`

The `street_actions` dict does NOT carry amounts. Amounts are not currently
stored anywhere in the decision record. This is a gap (see Section 7).

### Short-term pragmatic approach (no bet amounts)

For Phase 0, build `action_string` from `game.street_actions[current_street]`
using position and action only. Bet amounts will be `0` in the string, which
causes `validate_action_string()` to parse correctly (amount defaults to 0.0
when the token is absent). The `???` terminator is appended for the hero.

Example output without amounts: `"BB check, CO bet 0, BTN ???"`

This is valid input to `validate_action_string()` — it will catch ordering
violations and illegal action types. Amount validation is not in scope for
Phase 0.

---

## 4. Insertion Points — situation_factory.py

File: `/home/rupertbeytell/river-rats-v2/river-rats-core/situation_factory.py`

### 4a. Add action_string field to SituationSpec (line 192)

The `SituationSpec` dataclass currently ends at line 192 (`current_bet: float = 0.0`).

Add one field after `current_bet`:

```python
# Line 193 — insert after current_bet
action_string: Optional[str] = None
```

This field is Optional because callers may construct a SituationSpec without
it and rely on `build_situation()` to generate it automatically.

### 4b. Add _build_action_string() helper (after line 235)

Insert a new private helper after `_count_raises_this_street()` which ends at
line 234:

```python
# Insert at approximately line 236

def _build_action_string(
    action_history: List[Tuple[str, str, str]],
    current_street: str,
    hero_pos: str,
) -> str:
    """
    Build a validated action string for the current street.

    Extracts only current-street actions from action_history, formats them
    as "POS action[ amount]" tokens, and appends "HERO_POS ???".

    Amount is omitted because action_history tuples carry no amount.
    validate_action_string() treats missing amounts as 0.0 — legal for
    Phase 0 validation (ordering and type checks only).

    Returns:
        Comma-separated string, e.g. "BB check, CO bet, BTN ???"
        If no prior actions on current street: "BTN ???"
    """
    current_acts = [
        (pos, act)
        for s, pos, act in action_history
        if s == current_street
    ]
    parts = [f"{pos.upper()} {act.lower()}" for pos, act in current_acts]
    parts.append(f"{hero_pos.upper()} ???")
    return ', '.join(parts)
```

### 4c. Call _build_action_string() inside build_situation() (line 299)

`build_situation()` currently returns `build_features_from_game_state(...)` on
line 299. Before that return, generate and validate `action_string`:

```python
# Insert before the return on line 299 (currently the last line of build_situation)

# Generate action_string if not pre-supplied on the spec
if spec.action_string is None:
    spec.action_string = _build_action_string(
        spec.action_history, spec.street, spec.hero_pos
    )

# Validate immediately — raise on invalid sequence
all_positions = [spec.hero_pos] + list(spec.villain_positions)
_as_errors = _hsv_validate_action_string(
    all_positions,
    spec.street,
    spec.action_string,
    spec.hero_pos,
)
if _as_errors:
    raise ValueError(
        f"Invalid action_string '{spec.action_string}': {_as_errors}"
    )

return build_features_from_game_state(hero, game, context)
```

Note: `_hsv_validate_action_string` is already imported at line 48 of
`situation_factory.py` as:
```python
from hand_sequence_validator import validate_action_string as _hsv_validate_action_string
```
No new import is needed.

---

## 5. Insertion Points — generate_3way_situations.py

File: `/home/rupertbeytell/river-rats-v2/river-rats-core/generate_3way_situations.py`

This is the primary JSONL writer. The situation dict is assembled in
`_extract_3way_decisions()` at lines 52-74.

### 5a. Reconstruct action_string from game record (lines 52-74)

`HeroDecision` does not carry a pre-built `action_string`. The current
`prior_actions` list (line 64) is per-player and cross-street — it is not
the current-street action string.

The `game.street_actions` dict is available in the `GameResult.hand_record`
(populated by `HandLogger`). Check the hand_record structure to confirm.

**BLOCKER RISK**: `hand_record` may not expose current-street actions in a
format usable here. Read `hand_logger.py` before implementing this step to
confirm the data path. If `hand_record` does not carry `street_actions`,
the action_string must be reconstructed from `dec.feat_dict` action-history
features (which are indirect) or the generation pipeline must be extended to
pass `game.street_actions` into the decision record.

**Safe fallback for Phase 0**: If `hand_record` does not provide
current-street action sequences, set `action_string` to `f"{pos} ???"`
(hero is first to act) for all records and let the validator pass them.
Flag them with `action_string_complete: false` for later enrichment.

### 5b. Add action_string to the situation dict (line 73)

Insert after line 72 (`'adjusted_action': dec.action.upper()`):

```python
'action_string': _build_situation_action_string(dec, game_street_actions),
```

Where `_build_situation_action_string` is a module-level helper that:
1. Takes `dec` (HeroDecision) and the current-street action list from
   `hand_record`
2. Returns a string in the canonical format
3. Calls `validate_action_string()` and raises if invalid (fail-fast during
   generation, not silently at training time)

### 5c. Add import

At the top of `generate_3way_situations.py`, add:

```python
from hand_sequence_validator import validate_action_string as _hsv_validate
```

---

## 6. Insertion Points — label_3way_situations.py

File: `/home/rupertbeytell/river-rats-v2/river-rats-core/label_3way_situations.py`

The labeller reads situations from JSONL and adds `expert_action`,
`expert_confidence`, `expert_reasoning` fields. It does NOT need to generate
`action_string` — that is done by the generator.

The labeller SHOULD add a guard to reject records that are missing
`action_string`, so bad data never gets labelled and silently flows downstream.

### 6a. Add validation guard in label_situation() (line 33)

`label_situation(sit: dict)` starts at line 33. At the top of the function,
before extracting `fd = sit.get('feat_dict', {})` (line 41), insert:

```python
# Guard: action_string must be present and non-empty
action_string = sit.get('action_string', '')
if not action_string:
    raise ValueError(
        f"situation {sit.get('situation_id', '?')} is missing action_string. "
        "Re-generate with updated generate_3way_situations.py."
    )
```

This ensures the labeller fails loudly on old-format JSONL rather than
silently producing labels for unvalidated sequences.

---

## 7. CSV Export — No Changes Required

The export pipeline (`export_3way_training.py`, `feature_extractor.export_to_csv`)
writes only `FEATURE_COLUMNS + LABEL_COLUMN`. `action_string` is metadata and
must NOT appear in training CSV.

`export_3way_training.py` reads from `entry.get('feat_dict', {})` (line 47).
`action_string` is at the top level of the JSONL record, not inside `feat_dict`,
so it will not leak into the CSV automatically. No change needed.

Confirm this after implementation by asserting `'action_string' not in FEATURE_COLUMNS`.

---

## 8. Validator Interface (confirmed)

```python
# hand_sequence_validator.py, line 285
def validate_action_string(
    positions: List[str],    # all active seat names (including hero)
    street_name: str,        # 'flop', 'turn', or 'river'
    action_string: str,      # e.g. "BB check, CO bet 45, BTN call 45, BB ???"
    hero_pos: str,           # hero's seat name
) -> List[str]:              # returns [] on valid, list of error strings on invalid
```

The `???` marker in the string signals the hero's pending decision point.
The validator does NOT require amounts — missing amounts default to 0.0.

---

## 9. Tests Required

Write these tests in a new file:
`/home/rupertbeytell/river-rats-v2/river-rats-core/tests/test_action_string_field.py`

### Test 1: _build_action_string() — no prior actions

```
Input:  action_history=[], street='flop', hero_pos='BTN'
Expect: "BTN ???"
```

### Test 2: _build_action_string() — hero acts after checks

```
Input:  action_history=[('flop','BB','check'),('flop','CO','check')],
        street='flop', hero_pos='BTN'
Expect: "BB check, CO check, BTN ???"
```

### Test 3: _build_action_string() — hero faces bet

```
Input:  action_history=[('flop','BB','check'),('flop','CO','bet')],
        street='flop', hero_pos='BTN'
Expect: "BB check, CO bet, BTN ???"
```

### Test 4: _build_action_string() — cross-street history filtered correctly

```
Input:  action_history=[
            ('preflop','CO','raise'),('preflop','BB','call'),
            ('flop','BB','check'),('flop','CO','bet')
        ],
        street='flop', hero_pos='BTN'
Expect: "BB check, CO bet, BTN ???"
```

### Test 5: SituationSpec — action_string auto-generated by build_situation()

Construct a valid SituationSpec with no `action_string` set.
Call `build_situation(spec)`.
Assert `spec.action_string` is not None after the call.
Assert it ends with `f"{spec.hero_pos.upper()} ???"`.

### Test 6: SituationSpec — pre-supplied action_string is preserved

Construct a valid SituationSpec with `action_string="BB check, BTN ???"` already
set.
Call `build_situation(spec)`.
Assert `spec.action_string == "BB check, BTN ???"` (not overwritten).

### Test 7: build_situation() raises on invalid pre-supplied action_string

Construct a spec where `action_string` has an illegal action type (e.g. a
player calls without a bet live).
Assert `build_situation(spec)` raises `ValueError` with the string containing
`"Invalid action_string"`.

### Test 8: JSONL roundtrip — action_string survives json.dumps/json.loads

Serialize a situation dict with `action_string` to JSON and back.
Assert the field is present and unchanged.

### Test 9: label_3way_situations — raises on missing action_string

Call `label_situation({})` (no action_string key).
Assert `ValueError` is raised.

### Test 10: export_3way_training — action_string does not appear in CSV

Run `export_training_csv()` on a minimal JSONL with `action_string` present.
Read the output CSV header.
Assert `'action_string'` is not in the header.

---

## 10. Concerns and Blockers

### BLOCKER: Bet amounts not in action_history tuples

`action_history` in `SituationSpec` and `game.street_actions` in `GameStub`
both carry `(street, pos, action)` triples with no amount. Phase 0 strings
will read `"CO bet, BTN ???"` not `"CO bet 45, BTN ???"`.

This is acceptable for Phase 0 (ordering validation works without amounts).
For Phase 1, bet amounts must be plumbed from `poker_game.py` through to the
decision record. Coordinate with the Lead Programmer before Phase 1.

### BLOCKER RISK: generate_3way_situations.py has no access to current-street action list

`HeroDecision` does not carry `street_actions`. The generation path must be
confirmed:
1. Read `hand_logger.py` to check whether `hand_record` exposes street-level
   action sequences.
2. If not: the `SelfPlayRunner` oracle callback at `self_play.py` line ~189
   must be extended to capture current-street actions at decision time and
   attach them to `HeroDecision`.

This is a concrete gap. Do not implement `generate_3way_situations.py` changes
until this is resolved. Implement `situation_factory.py` first — that path is
fully self-contained and unblocked.

### WARNING: validate_situation() already calls _hsv_validate_action_string

`situation_factory.py` lines 543-565 already call `_hsv_validate_action_string`
inside `validate_situation()`. The proposed change in Section 4c adds a second
call inside `build_situation()`, which runs unconditionally (fail-fast). This
means `validate_situation()` will double-validate the same sequence.

This is acceptable — the two calls serve different purposes (build-time hard
fail vs. post-build consistency check). There is no correctness risk. If
performance becomes a concern, deduplicate later.

### MINOR: action_string mutates the spec object

Section 4c mutates `spec.action_string` in place inside `build_situation()`.
If a caller passes a frozen or shared spec, this will cause unexpected
side-effects. Phase 0 callers (factory batch scripts) construct specs fresh
each call, so this is not an issue now. Flag for review if specs become shared.

---

## 11. Implementation Order

1. Write tests in `test_action_string_field.py` (all failing — test-first)
2. Add `_build_action_string()` helper to `situation_factory.py`
3. Add `action_string` field to `SituationSpec`
4. Add generation + validation block inside `build_situation()`
5. Run tests — all Tests 1-8 should now pass (Tests 9, 10 still fail)
6. Add guard in `label_3way_situations.py` — Test 9 passes
7. Verify Test 10 passes (should be no-op — just confirming isolation)
8. Read `hand_logger.py` and `self_play.py` oracle callback to resolve the
   BLOCKER above before touching `generate_3way_situations.py`
9. Implement `generate_3way_situations.py` changes once blocker is resolved

---

## 12. Files Changed (Summary)

| File | Change | Lines Affected |
|---|---|---|
| `river-rats-core/situation_factory.py` | Add `action_string` field to `SituationSpec` | ~193 |
| `river-rats-core/situation_factory.py` | Add `_build_action_string()` helper | after line 234 |
| `river-rats-core/situation_factory.py` | Call helper + validate inside `build_situation()` | ~296-299 |
| `river-rats-core/label_3way_situations.py` | Add missing-field guard in `label_situation()` | ~40-41 |
| `river-rats-core/generate_3way_situations.py` | Add `action_string` to situation dict | ~73 (BLOCKED pending hand_logger investigation) |
| `river-rats-core/tests/test_action_string_field.py` | New test file | new file |

Files NOT changed:
- `feature_extractor.py` — `action_string` is metadata, not a feature
- `export_3way_training.py` — reads only `feat_dict`; isolation confirmed
- `hand_sequence_validator.py` — interface unchanged
- `gto_model.py` — `FEATURE_COLUMNS` unchanged

---

*Blueprint produced by Architecture Expert, 2026-04-13.*
*Programmer implements from this document only. Do not deviate without updated blueprint.*
