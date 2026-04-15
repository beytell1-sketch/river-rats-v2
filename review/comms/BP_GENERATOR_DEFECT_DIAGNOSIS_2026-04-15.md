---
date: 2026-04-15
from: Architecture Expert
to: Owner (Rupert)
re: Track B — BP generator defect diagnosis + fix blueprint
status: AWAITING OWNER REVIEW — do not implement until approved
---

# BP Generator Defect Diagnosis

## 1. One-sentence root cause

The Pass 1 batch preparation script that converted
`factory_batch5_situations.jsonl` into the `situation_text`
strings read the single-valued `_villain_pos_raw` field (e.g. `"BB"`)
from the flat feature dict instead of the top-level
`villain_positions` list (e.g. `["SB", "BB"]`), causing
176 of 185 BP labelling packets to show only one villain in the
"Villain positions:" header despite `num_opponents: 2`.

---

## 2. Evidence chain

### 2a. JSONL is correct — both seats present

`training-data/factory_batch5_situations.jsonl` contains 185 records,
all with `villain_positions` as a two-element list:

```
"villain_positions": ["SB", "BB"]   # e.g. BP1_01
```

Confirmed: `grep -c '"villain_positions"' factory_batch5_situations.jsonl`
returns 185. The generator (`generate_factory_batch5.py`) writes this
field correctly at line 1949:

```python
feat_dict['villain_positions'] = list(spec.villain_positions)
```

The JSONL was last modified 2026-04-13 23:52.

### 2b. Labelling batch shows only one seat

`/tmp/pass1_T1_batch37.json` (created 2026-04-14 14:35, AFTER the JSONL)
contains the `situation_text` field for BP1_01:

```
Villain positions: BB
Num opponents: 2
...
Action history: SB check, BB bet, BTN ???
```

`Villain positions` lists only `BB`. The action history reveals `SB` was
also active but the header dropped it. The same pattern appears for every
other multi-villain BP hand checked: only the bettor (the `_villain_pos_raw`
value) was written to the header.

The same record in the JSONL source has:

```json
"_villain_pos_raw": "BB",
"villain_positions": ["SB", "BB"]
```

The batch formatter used `_villain_pos_raw` (a single string) instead of
`villain_positions` (a list).

### 2c. Earlier batch generators did not write villain_positions at all

`generate_factory_batch2.py` and `generate_factory_batch3.py`
`generate_all()` loops (lines 1382–1386 and 1382–1386 respectively)
write only five metadata fields to `feat_dict`:

```python
feat_dict['situation_id'] = sit_id
feat_dict['sub_pattern'] = sub_pattern
feat_dict['hero_cards'] = hero_cards_str
feat_dict['board_cards'] = board_cards_str
feat_dict['description'] = description
```

`villain_positions`, `hero_position`, `action_string`, and `street`
are NOT written. The fix was added in `generate_factory_batch5.py`
(lines 1947–1950):

```python
feat_dict['action_string'] = spec.action_string
feat_dict['hero_position'] = spec.hero_pos
feat_dict['villain_positions'] = list(spec.villain_positions)
feat_dict['street'] = spec.street
```

`generate_factory_batch4.py` has the same omission as batches 2 and 3
(lines 1570–1574).

However, none of the batch4-and-earlier outputs are the BP-series — the
BP-series was generated exclusively by `generate_factory_batch5.py`. So
the missing-field bug in batches 2–4 is a separate concern (see section 7).

### 2d. The root defect is in the batch text formatter

The JSONL had both villain seats. The defect was in the ad-hoc batch
preparation script that converted the flat JSONL records into
`situation_text` strings for the Pass 1 labelling agents. That script
(not saved as a named file — run inline in conversation) built the
"Villain positions:" line using `_villain_pos_raw` (the single primary
villain resolved by `game_state_bridge.py`) rather than `villain_positions`
(the full list written by `generate_factory_batch5.py`).

The canonical formatter in `calibration_exam.py` (line 139) reads
`situation['villain_positions']` correctly:

```python
f"Villain positions: {', '.join(situation['villain_positions'])}",
```

But this formatter expects the d-series nested format
(`situation['feat_dict']` + top-level metadata). The BP-series JSONL is
flat — all features and metadata at the same level. The ad-hoc BP batch
formatter either:

- used `sit.get('_villain_pos_raw', 'BB')` directly, wrapping it as a
  single-element string, OR
- called `calibration_exam.format_situation_for_agent()` on the flat BP
  records, causing `situation['villain_positions']` to return `['BB']`
  because only the primary villain was present in an intermediate
  conversion step.

Either way, `_villain_pos_raw` from `game_state_bridge.py` (always one
seat) was substituted for the multi-seat `villain_positions` list from
the spec.

---

## 3. Why it passed existing tests

There are no tests that:
1. Run the BP batch text formatter and assert the count of positions in
   the "Villain positions:" header.
2. Verify `len(villain_positions) == num_opponents` at generation time.
3. Read the labelling batch text back and check it against the JSONL source.

The generator tests (`generate_factory_batch5.py` validation section) only
check situation counts per sub-pattern and run `validate_situation()`.
`validate_situation()` checks feature arithmetic but does NOT check that
`len(villain_positions) >= num_opponents`.

The `labelling_agent.py` preparation path reads
`sit.get('villain_positions', [])` (line 81) correctly, but the BP labelling
was not run through `labelling_agent.py` — it used a custom inline formatter.

---

## 4. Fix blueprint

### Fix 1: Add num_opponents validator in situation_factory.py
(v2.3 backlog item 5)

**File:** `river-rats-core/situation_factory.py`

**Location:** In `build_situation()`, after the opponents list is built
(after line 313, before the context dict).

**Before (no guard exists at this location):**

```python
    opponents: List[OpponentStub] = []
    for i, pos in enumerate(spec.villain_positions):
        is_bettor = facing_bet and (i == len(spec.villain_positions) - 1)
        opponents.append(OpponentStub(
            position=pos,
            is_folded=False,
            bet_this_street=current_bet if is_bettor else 0.0,
            stack=spec.effective_stack,
        ))

    # Context
    context: dict = {
```

**After (insert guard between opponents list and context dict):**

```python
    opponents: List[OpponentStub] = []
    for i, pos in enumerate(spec.villain_positions):
        is_bettor = facing_bet and (i == len(spec.villain_positions) - 1)
        opponents.append(OpponentStub(
            position=pos,
            is_folded=False,
            bet_this_street=current_bet if is_bettor else 0.0,
            stack=spec.effective_stack,
        ))

    # v2.3 backlog item 5: fail at generation if villain list is incomplete.
    # num_opponents must not exceed villain_positions length.
    num_opponents_declared = getattr(spec, 'num_opponents', len(spec.villain_positions))
    if len(spec.villain_positions) < num_opponents_declared:
        raise ValueError(
            f"villain_positions has {len(spec.villain_positions)} seats "
            f"but num_opponents={num_opponents_declared}. "
            f"Add the missing seat(s) to spec.villain_positions before calling "
            f"build_situation()."
        )

    # Context
    context: dict = {
```

Note: `SituationSpec` does not currently have a `num_opponents` field.
The fix should also add `num_opponents: Optional[int] = None` to the
`SituationSpec` dataclass (around line 193 in `situation_factory.py`),
defaulting to `None` (= infer from `len(villain_positions)`). See the
regression test spec below for the test case.

**SituationSpec change:**

```python
# Before (line ~193):
    action_string: Optional[str] = None

# After:
    num_opponents: Optional[int] = None
    action_string: Optional[str] = None
```

### Fix 2: Propagate villain_positions in generate_factory_batch4.py
(and batches 2, 3 — for completeness and to harden future regeneration)

**File:** `review/generate_factory_batch4.py`

**Location:** Lines 1570–1574 (the metadata attachment block in
`generate_all()`).

**Before:**

```python
        feat_dict['situation_id'] = sit_id
        feat_dict['sub_pattern'] = sub_pattern
        feat_dict['hero_cards'] = hero_cards_str
        feat_dict['board_cards'] = board_cards_str
        feat_dict['description'] = description
```

**After:**

```python
        feat_dict['situation_id'] = sit_id
        feat_dict['sub_pattern'] = sub_pattern
        feat_dict['hero_cards'] = hero_cards_str
        feat_dict['board_cards'] = board_cards_str
        feat_dict['description'] = description
        feat_dict['action_string'] = spec.action_string
        feat_dict['hero_position'] = spec.hero_pos
        feat_dict['villain_positions'] = list(spec.villain_positions)
        feat_dict['street'] = spec.street
```

Apply the same change to:
- `review/generate_factory_batch2.py` lines 1382–1386 (same block)
- `review/generate_factory_batch3.py` lines 1382–1386 (same block)

### Fix 3: Enforce the validator in generate_factory_batch5.py
(and all future BP generators)

`generate_factory_batch5.py` already calls `build_situation(spec)`, so
once Fix 1 is applied to `situation_factory.py`, the validator fires
automatically during generation. No code change needed in batch5 — the
validator in `build_situation()` covers it.

### Fix 4: Standardise the batch text formatter

The ad-hoc inline formatter is gone. Going forward, all batch text
generation (BP-series or d-series) must use the canonical path through
`labelling_agent.prepare_batches()` or `calibration_exam.format_situation_for_agent()`.

`calibration_exam.format_situation_for_agent()` (line 139) correctly reads
`situation['villain_positions']`. For BP-series flat records (no nested
`feat_dict`), a thin adapter is needed. The Programmer should add a
normalisation step in `labelling_agent.prepare_batches()` that handles
both formats:

```python
# In prepare_batches(), before calling format_situation_for_agent():
# Normalise flat BP records to nested format if feat_dict is absent.
if 'feat_dict' not in sit:
    # Flat factory_batch5 record: split into metadata + feat_dict.
    sit = _normalise_flat_situation(sit)
```

The `_normalise_flat_situation()` helper extracts known metadata keys
(`situation_id`, `hero_cards`, `board_cards`, `hero_position`,
`villain_positions`, `street`, `pot`, `to_call`, `facing_bet`,
`num_opponents`, `action_string`, `description`) into the top-level
dict and puts all remaining keys into a `feat_dict` sub-dict. This
ensures all batch text generation uses a single, tested formatter.

This fix is medium-priority: the existing BP labels have been corrected
by the Phase 3.5 relabel. Fix 4 prevents recurrence for v2.3 supplement
generation.

---

## 5. Regression test specification

**File:** `river-rats-core/tests/test_situation_factory.py`
(new test, or add to existing test file if one exists)

**Test name:** `test_build_situation_raises_when_villain_count_mismatch`

**Input that reproduces the bug:**

```python
from situation_factory import SituationSpec, build_situation

spec = SituationSpec(
    hero_cards=['As', '9s'],
    board_cards=['Ts', '6s', '3d'],
    hero_pos='BTN',
    villain_positions=['BB'],  # Only 1 seat declared
    num_opponents=2,            # But spec says 2 opponents
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'),
        ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'),
        ('flop', 'BB', 'bet'),
    ],
    opener_position='BTN',
)
```

**Expected behaviour after fix:**

```python
import pytest
with pytest.raises(ValueError, match="villain_positions has 1 seats but num_opponents=2"):
    build_situation(spec)
```

**Correct (passing) case — should not raise:**

```python
spec_correct = SituationSpec(
    hero_cards=['As', '9s'],
    board_cards=['Ts', '6s', '3d'],
    hero_pos='BTN',
    villain_positions=['SB', 'BB'],  # Both seats present
    num_opponents=2,
    pot=90.0,
    to_call=30.0,
    street='flop',
    action_history=[
        ('preflop', 'BTN', 'raise'),
        ('preflop', 'BB', 'call'),
        ('flop', 'SB', 'check'),
        ('flop', 'BB', 'bet'),
    ],
    opener_position='BTN',
)
feat_dict = build_situation(spec_correct)
assert feat_dict['num_opponents'] == 2
```

---

## 6. Spot-check: does this affect d-series?

**No.** The d-series uses `generate_3way_situations.py`, which writes
`villain_positions` from `dec.villain_positions` (line 59). This field
comes from the live game state (`self_play.py`), which always has the
full list of active opponents. There is no intermediate text formatter
involved — the d-series goes through `labelling_agent.prepare_batches()`
which reads `sit['villain_positions']` directly from the top-level dict.

The d-series labelling batch files (`/tmp/pass1_T1_batch15.json` etc.)
show correctly-populated villain lists (e.g. `Villain positions: HJ, BTN`).
Confirmed by direct inspection.

**The bug is BP-series-only** because:
1. Only the BP-series used the ad-hoc inline formatter.
2. Only the BP-series used a flat JSONL record format (features at
   top level, no nested `feat_dict`).
3. Only the BP-series had the opportunity to confuse `_villain_pos_raw`
   (single string) with `villain_positions` (list).

The d-series JSONL has the nested `feat_dict` structure matching the
`calibration_exam.format_situation_for_agent()` contract. As long as
the d-series continues to go through the canonical formatter, it is not
at risk.

---

## 7. Scope of fix to older batch generators (batches 2, 3, 4)

`generate_factory_batch2.py`, `generate_factory_batch3.py`, and
`generate_factory_batch4.py` all omit `villain_positions` from the
`feat_dict` output. These generate the PA-series and earlier factory
situations (not BP-series). Their output JSONLs do not have a
`villain_positions` key:

```
grep -c '"villain_positions"' factory_batch2_situations.jsonl  → 0
grep -c '"villain_positions"' factory_batch3_situations.jsonl  → 0
```

These situations were labelled before the batch text formatter defect
was introduced (their labelling used the earlier calibration_exam
formatter, which handled the PA-series differently). The omission does
not affect the v2.2 labels for these series. Fix 2 above adds the field
for completeness and forward-compatibility only.

The `factory_situations_formatted.jsonl` (151 records, PA-series) DOES
have `villain_positions` at the top level — it was built by a different
path. That file is not affected.

---

## 8. Files involved in the fix

| File | Change | Priority |
|------|--------|----------|
| `river-rats-core/situation_factory.py` | Add `num_opponents` field to `SituationSpec`; add validator in `build_situation()` | HIGH — required for v2.3 backlog item 5 |
| `river-rats-core/labelling_agent.py` | Add `_normalise_flat_situation()` helper; call it in `prepare_batches()` | HIGH — prevents recurrence |
| `river-rats-core/tests/test_situation_factory.py` | Add regression test (see section 5) | HIGH — test-first per protocol |
| `review/generate_factory_batch4.py` | Add 4 missing metadata fields to `feat_dict` | MEDIUM — completeness |
| `review/generate_factory_batch2.py` | Same | LOW — labelling complete, regeneration unlikely |
| `review/generate_factory_batch3.py` | Same | LOW — labelling complete, regeneration unlikely |

---

## 9. What the Programmer must NOT do

- Do NOT re-run labelling on any BP hands. The v2.2 labels are locked
  (Phase 3.5 relabel is complete). Fix is for v2.3 supplement generation
  only.
- Do NOT change `factory_batch5_situations.jsonl`. It is correct as-is.
- Do NOT touch `generate_factory_batch5.py` — it already has the fix.
- Do NOT add a `num_opponents` field to the spec unless it is Optional
  with `None` default. Existing callers must not break.

---

## 10. Verification after fix

After implementation, the Programmer should run:

```bash
cd /home/rupertbeytell/river-rats-v2/river-rats-core
python3 -m pytest tests/test_situation_factory.py -v
```

The new regression test must fail on the old code and pass after the fix.
Full test suite must also pass.

No regeneration of existing situations is needed for verification.
The fix is validated by the test alone.
