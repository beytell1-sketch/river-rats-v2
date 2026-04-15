---
date: 2026-04-15
from: Builder (Programmer)
to: Main terminal / Owner
re: Fix 1 — normalise BP-series generators at the JSONL serialisation boundary
status: APPLIED (source patched, BP JSONLs clean, schema gate wired)
---

# Fix 1 — BP Generators Normalisation

Implements §4 Fix 1 (option a) of
`review/comms/ANOMALY_A_VERIFICATION_2026-04-15.md`: normalise
`street` and `hero_position` to canonical numeric encoding at the
JSONL serialisation boundary in every BP-series generator, so future
runs cannot reintroduce the mixed-encoding defect that produced
ANOMALY-A in `training-data/v2_2_training.csv`.

## Files changed

Source:
- `river-rats-core/situation_factory.py` — added
  `normalise_situation()` helper plus `STREET_CODE` and
  `POSITION_CODE` constants.
- `river-rats-core/tests/test_situation_factory.py` — 6 new unit
  tests for `normalise_situation()` (street mapping, position
  mapping, idempotence, legacy `hero_pos` key handling, KeyError on
  unknown input, numeric passthrough).
- `river-rats-core/tests/test_training_data_encoding.py` — extended
  to parametrise over all 5 BP JSONLs × (`street`, `hero_position`)
  (10 new assertions) in addition to the pre-existing CSV checks.
- `river-rats-core/train_model.py` — added `_preflight_schema_check()`
  + `__main__` wiring as in-process schema gate.
- `review/generate_factory_situations.py`
- `review/generate_factory_batch2.py`
- `review/generate_factory_batch3.py`
- `review/generate_factory_batch4.py`
- `review/generate_factory_batch5.py`

  Each of the five generators: (a) replaced hard-coded
  `/home/rupertbeytell/...` paths with portable `__file__`-relative
  derivations, (b) imports and calls `normalise_situation(record)`
  immediately before `json.dumps` at the serialisation point.

Data (regenerated in-place via `normalise_situation`; row counts
identical to originals):
- `training-data/factory_situations.jsonl`
- `training-data/factory_batch2_situations.jsonl`
- `training-data/factory_batch3_situations.jsonl`
- `training-data/factory_batch5_situations.jsonl`

## Position → int mapping confirmed

Canonical mapping used for `hero_position`:
```
UTG/EP = 0
HJ/MP  = 1
CO     = 2
BTN    = 3
SB     = 4
BB     = 5
```
Source: `river-rats-core/feature_extractor.py:28-35`
(`POSITION_ORDINAL`), applied to hero at
`river-rats-core/feature_extractor.py:215`
(`'hero_position': POSITION_ORDINAL[hero_pos]`).

Cross-checked against d-series JSONL record
(`training-data/factory_situations.jsonl` row 1: `_hero_pos_raw='BB'`
→ `hero_position=5`) and BP batch2 row 1 (`_hero_pos_raw='SB'` →
`hero_position=4`). Both consistent with `POSITION_ORDINAL`.

Note: the verification report's §4 sketch used `POSITION_CODE = {'SB':
0, 'BB': 1, ...}` — that's the acting-order mapping (`POSTFLOP_ORDER`)
used for IP/OOP computation, **not** the field serialisation mapping.
I used `POSITION_ORDINAL` to match what downstream consumers actually
see. This was explicitly verified against the existing numeric
d-series JSONLs before applying.

Street mapping (matches `feature_extractor.STREET_ENCODING` via
`'f'→0, 't'→1, 'r'→2`, mapped from long-form):
```
flop = 0, turn = 1, river = 2
```

## Regenerated JSONLs — row counts

| File | Before | After | Rows with string-encoded street | Rows with string-encoded hero_position |
|------|--------|-------|---------------------------------|-----------------------------------------|
| `factory_situations.jsonl` | 151 | 151 | 0 → 0 (already clean) | 0 → 0 |
| `factory_batch2_situations.jsonl` | 261 | 261 | 0 → 0 (already clean) | 0 → 0 |
| `factory_batch3_situations.jsonl` | 151 | 151 | 0 → 0 (already clean) | 0 → 0 |
| `factory_batch4_situations.jsonl` | absent | absent | n/a | n/a |
| `factory_batch5_situations.jsonl` | 185 | 185 | **185 → 0** | **185 → 0** |

Only `factory_batch5_situations.jsonl` carried the live defect on
disk; the bug was in generators 3/4/5 (lines that overwrote
`feat_dict['street']` / `['hero_position']` with the raw
`spec.street` / `spec.hero_pos` strings after `build_situation()`
had emitted numeric values). Generators 1/2 happened to serialise
`build_situation()` output directly, so their existing files were
already numeric. Normalisation is applied defensively at all five
serialisation points to harden against regression.

`factory_batch4_situations.jsonl` was never committed (its
`generate_all()` aborts on a pre-existing situation-count mismatch
unrelated to ANOMALY-A). Source is patched; the file will emit
correctly when `generate_factory_batch4.py` is next run to
completion.

### Regeneration method — note

Attempted full `python3 generate_factory_*.py` runs after patching
hard-coded `/home/rupertbeytell/...` paths to portable `__file__`
derivations. Multiple generators (batch1, batch2, batch4) hit
pre-existing validation errors in `hand_sequence_validator.py`
(e.g. "HJ should respond first (clockwise from BTN)") that rejected
rows present in the committed JSONLs and produced row-count
regressions. Per the task's explicit stop condition ("If
regeneration produces row counts different from the originals —
STOP, do not commit, investigate") I reverted the failed runs and
instead piped each committed JSONL through
`situation_factory.normalise_situation()` in-place — guaranteeing
byte-level row-count parity while delivering the same data
transformation the patched generators now apply. The source change
is the authoritative fix; the in-place transform is the immediate
data remediation.

## Schema-test result on regenerated data

```
pytest river-rats-core/tests/test_training_data_encoding.py \
       river-rats-core/tests/test_situation_factory.py

12 passed, 2 skipped, 3 failed in 1.03s
```

- **PASS (12):** 6 `normalise_situation()` unit tests + 1 villain
  position CSV check + 3 BP JSONL numeric checks (factory_situations,
  factory_batch2, factory_batch3 each × 2 columns minus duplicates /
  skip, plus factory_batch5).
- **SKIP (2):** `factory_batch4_situations.jsonl` (not on disk;
  test correctly skips rather than failing).
- **FAIL (3):** the three pre-existing assertions on
  `training-data/v2_2_training.csv` still fail by design — the task
  explicitly constrains "Do NOT regenerate `v2_2_training.csv`". The
  CSV remains in its audited-corrupted state; the pre-flight gate
  (below) blocks any v2.3 training run on this file until it is
  regenerated from the clean BP JSONLs in a separate task.

## Pre-flight gate wiring

Added to `river-rats-core/train_model.py`:
1. Module docstring now documents the gate and points to
   `FIX1_BP_GENERATORS_2026-04-15.md`.
2. `_preflight_schema_check()` function scans
   `training-data/v2_2_training.csv` and all five BP JSONLs;
   raises `RuntimeError` listing offending files if any row has a
   non-numeric `street` or `hero_position`.
3. Invoked from a new `if __name__ == '__main__':` block at module
   top (line 109), before any training work starts. The existing
   training `__main__` block (line 485) is unchanged, so the gate
   runs first and the training body second.
4. CI-style alternative: `pytest
   river-rats-core/tests/test_training_data_encoding.py` encodes the
   same invariant as a hookable gate.

Sanity check:
```
$ python3 -c 'import sys; sys.path.insert(0,"river-rats-core"); \
             import train_model; train_model._preflight_schema_check()'
RuntimeError: ANOMALY-A pre-flight schema check failed:
  training-data/v2_2_training.csv:street has 185 non-numeric rows
  training-data/v2_2_training.csv:hero_position has 185 non-numeric rows
```
(Correctly flags the known-corrupt CSV; BP JSONLs are not listed,
confirming they are clean.)

## Blockers / caveats

- **v2_2_training.csv is still corrupted** (per task constraints).
  The pre-flight gate will block any `python3 train_model.py` run
  until this CSV is regenerated from the now-clean BP JSONLs +
  d-series JSONLs. Not in scope for Fix 1.
- **Full `generate_all()` regeneration not feasible today** due to
  pre-existing `hand_sequence_validator` strictness and one
  situation-count-mismatch abort in `generate_factory_batch4.py`.
  These are separate defects (not introduced by Fix 1 and not in
  its scope). Source-level fix is in place; in-place normalisation
  of existing JSONLs provides the equivalent data outcome with
  row-count parity.
- **`factory_batch4_situations.jsonl` is not on disk.** Source is
  patched; the file will emit correctly the next time
  `generate_factory_batch4.py` is run to completion (requires
  resolving the "BP1: expected 30, got 32" count mismatch — out of
  scope for Fix 1).
