"""
Regression test: training-data CSVs must use consistent numeric encoding
for categorical-but-ordinal columns BEFORE they are passed to XGBoost.

Context: TRAINING_DATA_AUDIT_2026-04-15.md (ANOMALY-A) +
         ANOMALY_A_VERIFICATION_2026-04-15.md

The v2.2 training CSV (training-data/v2_2_training.csv) was found to encode
`street` two different ways:
  - 200 rows (d-series):  numeric 0.0/1.0/2.0
  - 185 rows (BP-series): string 'flop'/'turn'/'river'

A further audit during ANOMALY-A verification uncovered the same defect on
`hero_position`:
  - 200 rows (d-series):  numeric 0.0..5.0
  - 185 rows (BP-series): string 'BTN'/'SB'/'BB'/'CO'/'HJ'/'UTG'

Any downstream consumer that naively calls float() / pd.to_numeric() will
either crash (float('flop') -> ValueError) or silently produce NaN/0 on
half the training set. Neither outcome is acceptable.

These tests enforce: every training CSV whose rows will be fed to XGBoost
must have numeric-only values for `street` and `hero_position`.

Tests are expected to FAIL on the current (committed, suspect) CSV at
training-data/v2_2_training.csv and PASS once the upstream generator
normalises encoding at serialisation time.
"""

import os
import sys
import csv
import json

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Columns that must be numeric in any CSV destined for XGBoost.
# (Ordinal-categorical values; no string labels allowed at the training boundary.)
NUMERIC_REQUIRED_COLUMNS = ('street', 'hero_position', 'villain_position')

# CSVs that are consumed by the v2.2 / v2.3 training pipeline.
# Add new training CSVs here as they are produced.
TRAINING_CSVS = (
    'training-data/v2_2_training.csv',
)


def _is_numeric_string(s: str) -> bool:
    """True iff s parses as a float (int/float literal, scientific notation)."""
    if s is None:
        return False
    s = s.strip()
    if s == '':
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False


def _non_numeric_rows(csv_path: str, column: str):
    """Return list of (row_index, value) for rows whose `column` is non-numeric."""
    offenders = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        if column not in reader.fieldnames:
            return None  # column absent — caller handles
        for i, row in enumerate(reader, start=1):
            val = row.get(column, '')
            if not _is_numeric_string(val):
                offenders.append((i, val))
    return offenders


@pytest.mark.parametrize('csv_rel', TRAINING_CSVS)
@pytest.mark.parametrize('column', NUMERIC_REQUIRED_COLUMNS)
def test_training_csv_column_is_numeric(csv_rel: str, column: str):
    """
    Every row in every training CSV must encode `column` as a numeric literal.

    Fails loudly (with counts and a sample of offending values) when the
    upstream generator has produced mixed string/numeric encoding.
    """
    csv_path = os.path.join(REPO_ROOT, csv_rel)
    if not os.path.exists(csv_path):
        pytest.skip(f'{csv_rel} not present on disk')

    offenders = _non_numeric_rows(csv_path, column)
    if offenders is None:
        pytest.skip(f'{csv_rel} does not contain column {column!r}')

    if offenders:
        # Summarise: total count + distinct non-numeric values + a few examples
        distinct = sorted({v for _, v in offenders})
        sample = offenders[:5]
        pytest.fail(
            f'{csv_rel}: column {column!r} has {len(offenders)} non-numeric rows.\n'
            f'  Distinct non-numeric values: {distinct}\n'
            f'  First offenders (row_index, value): {sample}\n'
            f'  XGBoost will either crash on float() or silently NaN/0-coerce\n'
            f'  these rows. Fix upstream at the generator (BP-series exporter),\n'
            f'  not by patching the CSV in place.'
        )


def test_training_csv_street_has_no_string_literals():
    """
    Focused assertion: v2_2_training.csv must not contain literal 'flop',
    'turn', or 'river' in the `street` column. This is the exact ANOMALY-A
    signature.
    """
    csv_path = os.path.join(REPO_ROOT, 'training-data/v2_2_training.csv')
    if not os.path.exists(csv_path):
        pytest.skip('v2_2_training.csv not present')

    forbidden = {'flop', 'turn', 'river'}
    hits = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            if row.get('street', '').strip().lower() in forbidden:
                hits.append((i, row['street']))
    assert not hits, (
        f'ANOMALY-A still present: {len(hits)} rows have string street '
        f'values. First offenders: {hits[:5]}'
    )


# =============================================================================
# Fix-1 follow-up: BP-series JSONLs must also carry numeric encoding.
#
# These are the upstream sources that feed the training CSV. Once the
# BP-series generators normalise at serialisation time, every row in
# every BP JSONL must have numeric street / hero_position.
# =============================================================================

BP_JSONLS = (
    'training-data/factory_situations.jsonl',
    'training-data/factory_batch2_situations.jsonl',
    'training-data/factory_batch3_situations.jsonl',
    'training-data/factory_batch4_situations.jsonl',
    'training-data/factory_batch5_situations.jsonl',
)

JSONL_NUMERIC_COLUMNS = ('street', 'hero_position')


@pytest.mark.parametrize('jsonl_rel', BP_JSONLS)
@pytest.mark.parametrize('column', JSONL_NUMERIC_COLUMNS)
def test_bp_jsonl_column_is_numeric(jsonl_rel: str, column: str):
    """
    Every row in every BP-series JSONL must encode `column` as a number
    (int or float), not a Python string. Enforced at the generator's
    serialisation boundary via situation_factory.normalise_situation().
    """
    jsonl_path = os.path.join(REPO_ROOT, jsonl_rel)
    if not os.path.exists(jsonl_path):
        pytest.skip(f'{jsonl_rel} not present on disk')

    offenders = []
    with open(jsonl_path) as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            val = rec.get(column)
            if val is None:
                continue  # absent — not this test's job
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                offenders.append((i, val))

    if offenders:
        distinct = sorted({repr(v) for _, v in offenders})
        sample = offenders[:5]
        pytest.fail(
            f'{jsonl_rel}: column {column!r} has {len(offenders)} non-numeric '
            f'rows.\n  Distinct non-numeric values: {distinct}\n'
            f'  First offenders (line_no, value): {sample}\n'
            f'  Fix at situation_factory.normalise_situation(); ensure the '
            f'generator pipes every record through it before json.dumps().'
        )
