---
date: 2026-04-15
from: Builder (ML Architect + Programmer)
to: Main terminal / Owner
re: Track 3.5 — ANOMALY-A verification, street encoding corruption in v2.2 training
status: VERIFIED — root cause identified; training-impact verdict PARTIALLY BLOCKED (see §2)
severity: HIGH (mixed encoding confirmed on TWO columns, not one)
---

# ANOMALY-A Verification Report

## TL;DR

- **Root cause found and located in source.** The BP-series situation
  factory (`review/generate_factory_batch*.py`) writes `street='flop'`
  and `hero_pos='BTN'` as Python strings; the d-series pipeline emits
  the same fields as integers. The v2.2 assembly step merged both
  JSONL streams into `training-data/v2_2_training.csv` without
  normalising — producing the 200-numeric / 185-string split.
- **A SECOND column has the same defect: `hero_position`.** The audit
  only flagged `street`. `hero_position` in `v2_2_training.csv` has 185
  string rows (`BTN`/`SB`/`BB`/`CO`) and 200 numeric rows (`0.0`–`5.0`).
  `villain_position` is clean (all numeric). Scope of ANOMALY-A is
  therefore **~2× what the audit reported**.
- **Training-impact verdict is PARTIALLY BLOCKED.** The Python script
  that actually produced `river-rats-core/models/v2_2_model.json` is
  **not checked into the repo**. The only `train_model.py` in-tree
  consumes a different CSV (`train_3way_v3_combined.csv`, 54 raw features,
  label column `action`), not the v2.2 CSV (54 raw + 54 `attn_*` = 108
  features, label column `label`, situation_id present). See §2.
- **Test-first deliverable is in place** and fails on the current CSV.

## 1. Root cause — which pipeline stage produced mixed encoding

### BP-series (185 rows, string encoding)

The BP-series situations are defined as literal Python dicts in the
review-folder factory generators. Example from
`review/generate_factory_batch5.py:65-78` (situation FB5_01 → exported as
`BP1_01` in the training CSV):

```python
FB5_01 = dict(
    board_cards=['Ts', '6s', '3d'],
    hero_pos='BTN',                 # string
    villain_positions=['SB', 'BB'],
    pot=90.0,
    to_call=30.0,
    street='flop',                  # string
    ...
)
```

Every BP-series situation across `review/generate_factory_situations.py`,
`review/generate_factory_batch2.py`, `…batch3.py`, `…batch4.py`, and
`…batch5.py` uses `street='flop'|'turn'|'river'` and `hero_pos='BTN'|'SB'|
'BB'|'CO'|'HJ'|'UTG'`. The JSONL exporter (seen in
`training-data/factory_batch5_situations.jsonl`, record for `BP1_01`)
serialises these raw strings:

```json
{"street": "flop", ..., "hero_position": "BTN", "villain_position": 5, ...}
```

Note that `villain_position` was already numeric upstream, which is why
it is clean in the final CSV.

### d-series (200 rows, numeric encoding)

The d-series pipeline goes through `feature_extractor.py` / the
extractor chain, which coerces street and position to their ordinal
integer enum values before serialisation. Example from
`training-data/factory_situations.jsonl` first record:

```json
{"street": 0, ..., "hero_position": 5, "villain_position": 2, ..., "_street_raw": "f"}
```

The raw string representation is preserved under `_street_raw` but the
canonical `street` field is already numeric.

### Where the two streams merged

Phase 3.5H final assembly (commit `9dd1a68`) wrote
`training-data/v2_2_training.csv` from the union of the BP-series
factory JSONL and the d-series extractor output. **The assembly script
that performed this merge is not checked into the repo** — the commit
adds the CSV but no `.py`. No normalisation of `street` /
`hero_position` was applied.

## 2. Training impact — PARTIALLY BLOCKED

**I cannot give a code-cited answer for how v2.2 training handled the
mixed encoding, because the script that trained v2.2 is not in git.**

Evidence:
- `river-rats-core/train_model.py` (lines 28–55, 62–88) loads a CSV via
  `csv.DictReader` and runs `float(row[col]) for col in FEATURE_COLUMNS`
  (line 78). It uses a 54-column FEATURE_COLUMNS list and the label
  column is `action`. It targets `training-data/train_3way_v3_combined.csv`
  (line 394).
- The actual v2.2 training CSV is 111 columns
  (`situation_id` + 54 raw + 54 `attn_*` + `label` + `label_source`) —
  see `training-data/v2_2_training.csv` header and
  `river-rats-core/models/v2_2_training_report.json`
  (`"n_features": 108, "features_raw": 54, "features_attn": 54`).
- Commit `5267a0b` ("Phase 4: v2.2 XGBoost training artefacts") added
  only the model JSON, training report, and evaluation report — **no
  training script**. `git log --diff-filter=A -- river-rats-core/*.py`
  around 2026-04-15 does not contain a v2.2 trainer.
- The v2.2 model file (`river-rats-core/models/v2_2_model.json`) was
  saved with `feature_names: []` and `feature_types: []` in the XGBoost
  learner block, so we cannot recover the feature ordering or the
  per-feature dtype from the model itself.

**Per CLAUDE.md Stop Conditions ("File doesn't exist where expected"
and "blueprint differs from source"), I am reporting this as
BLOCKED-ambiguity rather than improvising.** The three plausible code
paths in the missing v2.2 trainer are:

| Path | Outcome on 185 string rows | Would training have succeeded? |
|---|---|---|
| `float(row['street'])` (same as existing `train_model.py:78`) | `ValueError` on first 'flop' | No — training would crash, so this is ruled out |
| `pd.to_numeric(df['street'], errors='coerce')` | 185 rows → `NaN`; XGBoost treats NaN as missing (learns a directed default split) | Yes — model would train, street would be useful on 200 rows and "missing" on 185 |
| `df['street'].map({'flop':0,'turn':1,'river':2}).fillna(df['street'].astype(float))` or a unified mapping over both string and numeric inputs | 185 rows → correct integer encoding | Yes — clean |
| `pd.get_dummies(df['street'])` | `'flop'` and `0.0` become different columns | Training would succeed but with split signal |
| Silent `float` cast with error suppression → 0.0 | 185 rows → 0 (=flop) on every row regardless of actual street | Yes — this is the audit's worst-case hypothesis |

Given training *did* succeed (CV 93.0%, holdout 88.3%), path 1 is
eliminated. Distinguishing between paths 2, 3, 4, 5 requires the
missing script.

**What we can say with certainty:**
- The v2.2 training CSV is still committed and still corrupted. Any
  re-run of v2.2 or v2.3 training, using any loader that hits paths
  1/2/5 above, will either crash or corrupt 185 rows.
- The test-set metrics in `v2_2_evaluation_report.json` (FB-40 72.5%,
  MW 80%, MW normalised 44%) were computed with the same pipeline that
  did the training, so if corruption occurred at training time it is
  also present at eval time and the reported numbers are not
  "corrected" for it — they reflect whatever the loader produced.

## 3. Scope of damage

- **Mixed `street` encoding:** 185 / 385 rows (48.1%). All 185 are
  BP-series (situation_id prefix `BP*`).
- **Mixed `hero_position` encoding:** 185 / 385 rows (48.1%), same
  row set.
- **Worst-case (path 5 — silent-zero):** 185 rows would see `street=0`
  (=flop) regardless of their actual street, and `hero_position`
  coerced to either a default or an error-handled numeric. Of the 185
  BP rows, per-row street-source distribution is:
  - `flop`: 86 rows (0 correct, already encoded as 0 would be correct)
  - `turn`: 55 rows (incorrectly recoded as flop)
  - `river`: 44 rows (incorrectly recoded as flop)
  - → **99 rows (25.7% of total training data) would have had their
    turn/river examples presented to the model as flop examples.**
- **Best case (path 2 — NaN as missing):** XGBoost learns a directed
  split for missing. This is still degraded signal on 48% of data but
  is not "silently wrong"; the model may still perform reasonably. The
  93% CV does not disprove this.
- **MW miss connection:** The observed 80% MW accuracy with a
  bucket-first CHECK bias is consistent with, but not diagnostic of,
  street confusion. If path 5 was taken, the model saw 99 rows of
  turn/river action behaviour labelled as flop — this would bias it
  toward flop-like (less aggressive BET/RAISE) decisions on turn/river
  spots, matching the bucket-first CHECK signature.

## 4. Fix plan — upstream, at generation time

Do **not** patch `v2_2_training.csv` in place. Fix the two upstream
sources so any future re-serialisation emits canonical numeric codes.

### Fix 1: BP-series factory generators (primary root cause)

Files: `review/generate_factory_situations.py`,
`review/generate_factory_batch2.py`, `…batch3.py`, `…batch4.py`,
`…batch5.py`.

Two options, in order of preference:

**(a) Normalise in the generator** — add helpers and apply before
writing JSONL:

```python
STREET_CODE = {'flop': 0, 'turn': 1, 'river': 2}
POSITION_CODE = {'SB': 0, 'BB': 1, 'UTG': 2, 'HJ': 3, 'CO': 4, 'BTN': 5}

def normalise_situation(sit: dict) -> dict:
    sit = dict(sit)
    if isinstance(sit.get('street'), str):
        sit['street'] = STREET_CODE[sit['street']]
    if isinstance(sit.get('hero_pos'), str):
        sit['hero_pos'] = POSITION_CODE[sit['hero_pos']]
    return sit
```

Apply at the serialisation boundary (where situations are written to
`factory_batch*_situations.jsonl`).

**(b) Normalise at the assembly step** — retrieve the missing v2.2
assembly script (or rewrite it), and apply the same mapping before
writing `v2_2_training.csv`. This also protects any future sources we
haven't audited. Recommended as a defence-in-depth layer **in
addition** to (a), not instead of.

### Fix 2: Pre-training schema gate

The test in §5 below must run as part of the v2.3 training pipeline so
any future encoding regression fails fast rather than corrupting a
model. Minimum integration: call pytest on this test file before
invoking the XGBoost training script.

### Fix 3: Recover / rewrite the v2.2 training script

Independent of encoding: the v2.2 training script itself should be
checked into `river-rats-core/` with a version suffix
(e.g. `train_model_v2_2.py`) so that future audits can cite its line
numbers. This is a process fix, not a code fix.

## 5. Test result

**New test file:** `river-rats-core/tests/test_training_data_encoding.py`

Three tests, parametrised over (`street`, `hero_position`,
`villain_position`) × (`v2_2_training.csv`) plus one focused assertion
that `street` contains no `'flop'`/`'turn'`/`'river'` literals.

### Current behaviour (ANOMALY-A present)

```
pytest river-rats-core/tests/test_training_data_encoding.py -v
…
FAILED test_training_csv_column_is_numeric[street-training-data/v2_2_training.csv]
  — 185 non-numeric rows; distinct values ['flop', 'river', 'turn']
FAILED test_training_csv_column_is_numeric[hero_position-training-data/v2_2_training.csv]
  — 185 non-numeric rows; distinct values ['BB', 'BTN', 'CO', 'SB']
FAILED test_training_csv_street_has_no_string_literals
  — 185 rows have string street values
PASSED test_training_csv_column_is_numeric[villain_position-training-data/v2_2_training.csv]

3 failed, 1 passed in 0.04s
```

### Expected behaviour after Fix 1 applied + CSV regenerated

All 4 tests pass. The village check on `villain_position` continues to
pass (it was always clean); the two regressions on `street` and
`hero_position` flip to green once the BP-series generator emits
numeric codes.

## 6. Do-not-do (per task constraints)

- v2.2 was **not** retrained. No changes made to
  `river-rats-core/models/`.
- `training-data/v2_2_training.csv` was **not** modified. Fix is
  queued for the upstream generators.
- No improvisation on the missing v2.2 trainer: §2 documents the
  ambiguity rather than guessing.

## 7. Recommended next actions

1. **Owner decision:** accept BLOCKED-ambiguity on the training-impact
   verdict (path 2 vs path 5), or authorise recovering the v2.2
   trainer from whatever environment produced `v2_2_model.json` so the
   audit can cite exact behaviour.
2. **Before any v2.3 supplement is appended:** apply Fix 1 to the
   BP-series generators, regenerate affected JSONLs, re-run the new
   pytest — it must pass.
3. **Before v2.3 training runs:** integrate
   `test_training_data_encoding.py` into the training entry point as
   a pre-flight schema check.
4. **Gate 7 input:** this anomaly is a reason to hold v2.2 ship — the
   model may have been trained with partially-missing street signal
   on 48% of rows, and the MW miss bias is consistent with this.
   Owner call.
