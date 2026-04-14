"""
Tests for the feature attention training experiments.
Written BEFORE implementation per the blueprint Section 10 requirement.

Run with: python3 -m pytest river-rats-core/tests/test_attention_experiments.py -v
from the repo root.

Unit tests use synthetic data only. Integration tests are marked and skipped by default.
"""

import sys
import os
import json
import csv
import tempfile
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from gto_model import FEATURE_COLUMNS, ACTION_CLASSES

# Import functions under test (these will fail until implemented)
from assemble_pilot_data import (
    parse_untagged_features_file,
    validate_attention_levels,
    validate_intention_tags,
    build_enriched_record,
    LEVEL_WEIGHTS,
)
from run_attention_experiments import (
    load_feature_csv,
    run_loo_cv,
    apply_masking,
    get_named_importances,
)

# ═══════════════════════════════════════════════════════════════════
# CONSTANTS USED IN TESTS
# ═══════════════════════════════════════════════════════════════════

# Fast config for LOO CV tests — 5 trees instead of 50
PILOT_XGB_CONFIG_SUBSET = dict(
    n_estimators=5,
    max_depth=2,
    learning_rate=0.1,
    subsample=1.0,
    colsample_bytree=1.0,
    min_child_weight=1,
    gamma=0.0,
    reg_alpha=0.0,
    reg_lambda=1.0,
    objective='multi:softprob',
    num_class=5,
    random_state=42,
    n_jobs=1,
)


# ═══════════════════════════════════════════════════════════════════
# TESTS FOR assemble_pilot_data.py
# ═══════════════════════════════════════════════════════════════════

def test_feature_columns_count():
    """FEATURE_COLUMNS must have exactly 54 entries — the entire pipeline depends on this."""
    assert len(FEATURE_COLUMNS) == 54


def test_action_classes_order():
    """ACTION_CLASSES order is baked into result files — must not change."""
    assert ACTION_CLASSES == ('FOLD', 'CHECK', 'CALL', 'BET', 'RAISE')


def test_level_weights_values():
    """LEVEL_WEIGHTS must match the blueprint-specified values."""
    assert LEVEL_WEIGHTS['PRIMARY'] == 1.0
    assert LEVEL_WEIGHTS['CONFIRMED'] == 0.7
    assert LEVEL_WEIGHTS['DISCOVERED'] == 0.5
    assert LEVEL_WEIGHTS['Untagged'] == 0.1


def test_build_enriched_record_flags():
    """
    build_enriched_record must correctly compute attention_flags.
    First 2 features are untagged -> flag 0. Remaining 52 features -> flag 1.
    """
    situation = {
        'situation_id': 'test_hand',
        'feat_dict': {f: 1.0 for f in FEATURE_COLUMNS},
    }
    untagged_features = {FEATURE_COLUMNS[0], FEATURE_COLUMNS[1]}

    result = build_enriched_record(situation, 'CHECK', untagged_features)

    assert result['attention_flags'][FEATURE_COLUMNS[0]] == 0   # untagged
    assert result['attention_flags'][FEATURE_COLUMNS[1]] == 0   # untagged
    assert result['attention_flags'][FEATURE_COLUMNS[2]] == 1   # tagged
    assert result['n_tagged'] == 52
    assert result['label'] == 'CHECK'


def test_build_enriched_record_levels():
    """
    build_enriched_record must assign attention_levels from ATTENTION_LEVELS
    for the given situation_id, defaulting to 0.1 for untagged features.
    """
    import assemble_pilot_data as asmb

    # Temporarily inject a test entry into ATTENTION_LEVELS
    original = asmb.ATTENTION_LEVELS.get('test_hand')
    asmb.ATTENTION_LEVELS['test_hand'] = {
        FEATURE_COLUMNS[2]: 'PRIMARY',
        FEATURE_COLUMNS[3]: 'CONFIRMED',
        FEATURE_COLUMNS[4]: 'DISCOVERED',
    }

    situation = {
        'situation_id': 'test_hand',
        'feat_dict': {f: 1.0 for f in FEATURE_COLUMNS},
    }
    untagged_features = {FEATURE_COLUMNS[0], FEATURE_COLUMNS[1]}

    result = build_enriched_record(situation, 'CHECK', untagged_features)

    assert result['attention_levels'][FEATURE_COLUMNS[2]] == 1.0  # PRIMARY
    assert result['attention_levels'][FEATURE_COLUMNS[3]] == 0.7  # CONFIRMED
    assert result['attention_levels'][FEATURE_COLUMNS[4]] == 0.5  # DISCOVERED
    assert result['attention_levels'][FEATURE_COLUMNS[0]] == 0.1  # untagged

    # Cleanup
    if original is None:
        del asmb.ATTENTION_LEVELS['test_hand']
    else:
        asmb.ATTENTION_LEVELS['test_hand'] = original


def test_build_enriched_record_missing_feature():
    """build_enriched_record must raise ValueError when feat_dict is missing a key."""
    # feat_dict missing last feature
    feat_dict = {f: 1.0 for f in FEATURE_COLUMNS[:-1]}
    situation = {
        'situation_id': 'test_hand',
        'feat_dict': feat_dict,
    }
    with pytest.raises(ValueError):
        build_enriched_record(situation, 'CHECK', set())


def test_validate_intention_tags_bad_tag():
    """validate_intention_tags must raise ValueError for an unknown tag string."""
    import assemble_pilot_data as asmb

    vocab = {
        'value_extract': 'desc',
        'pot_control': 'desc',
    }
    # Temporarily inject a bad tag
    original = asmb.INTENTION_TAGS.get('test_hand')
    asmb.INTENTION_TAGS['test_hand'] = ['value_extract', 'NOT_A_REAL_TAG']

    with pytest.raises(ValueError):
        validate_intention_tags(vocab)

    # Cleanup
    if original is None:
        del asmb.INTENTION_TAGS['test_hand']
    else:
        asmb.INTENTION_TAGS['test_hand'] = original


def test_validate_attention_levels_conflict():
    """
    validate_attention_levels must raise ValueError if a feature is in both
    ATTENTION_LEVELS and the untagged_map for the same hand.
    """
    import assemble_pilot_data as asmb

    conflict_feature = FEATURE_COLUMNS[5]
    original = asmb.ATTENTION_LEVELS.get('conflict_hand')
    asmb.ATTENTION_LEVELS['conflict_hand'] = {conflict_feature: 'PRIMARY'}

    # Build an untagged_map covering all 20 real hands plus this conflict
    # We need to cover all keys in ATTENTION_LEVELS; patch just this one
    # Use the real untagged_map from parse (if possible) or build a minimal one
    # Build a complete untagged_map with the conflict hand present
    untagged_map = {h: set() for h in asmb.ATTENTION_LEVELS.keys()}
    untagged_map['conflict_hand'] = {conflict_feature}  # conflict!

    with pytest.raises(ValueError):
        validate_attention_levels(untagged_map)

    # Cleanup
    if original is None:
        del asmb.ATTENTION_LEVELS['conflict_hand']
    else:
        asmb.ATTENTION_LEVELS['conflict_hand'] = original


# ═══════════════════════════════════════════════════════════════════
# TESTS FOR run_attention_experiments.py
# ═══════════════════════════════════════════════════════════════════

def _write_temp_csv(tmp_path, n_rows, columns, label_col='label', labels=None):
    """Helper: write a temporary CSV with n_rows of data."""
    filepath = os.path.join(tmp_path, 'test.csv')
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns + ([label_col] if label_col else []))
        writer.writeheader()
        for i in range(n_rows):
            row = {col: float(i) for col in columns}
            if label_col:
                action_cycle = ['FOLD', 'CHECK', 'CALL', 'BET', 'RAISE']
                row[label_col] = labels[i] if labels else action_cycle[i % 5]
            writer.writerow(row)
    return filepath


def test_load_feature_csv_shape(tmp_path):
    """load_feature_csv must return X of (20, 54) and y of (20,) with dtype int32."""
    filepath = _write_temp_csv(str(tmp_path), 20, list(FEATURE_COLUMNS), 'label')
    X, y, col_names = load_feature_csv(filepath, list(FEATURE_COLUMNS), 'label')

    assert X.shape == (20, 54)
    assert y.shape == (20,)
    assert y.dtype == np.int32


def test_load_feature_csv_wrong_n_rows(tmp_path):
    """load_feature_csv must raise ValueError if n_rows != 20."""
    filepath = _write_temp_csv(str(tmp_path), 19, list(FEATURE_COLUMNS), 'label')
    with pytest.raises(ValueError):
        load_feature_csv(filepath, list(FEATURE_COLUMNS), 'label')


def test_load_feature_csv_missing_column(tmp_path):
    """load_feature_csv must raise ValueError if a requested feature column is absent."""
    # Write CSV with only 53 columns (missing last feature)
    cols = list(FEATURE_COLUMNS[:-1])
    filepath = _write_temp_csv(str(tmp_path), 20, cols, 'label')
    with pytest.raises(ValueError):
        # Request all 54 but CSV only has 53
        load_feature_csv(filepath, list(FEATURE_COLUMNS), 'label')


def test_apply_masking_zeros_correct_features():
    """apply_masking must zero the correct cells per row without touching others."""
    X = np.ones((3, 4), dtype=np.float32)
    column_names = ['a', 'b', 'c', 'd']
    untagged_per_hand = [{'b', 'c'}, {'a'}, {'d'}]

    X_masked, stats = apply_masking(X.copy(), column_names, untagged_per_hand)

    assert X_masked[0, 0] == 1.0   # 'a', not untagged for row 0
    assert X_masked[0, 1] == 0.0   # 'b', untagged for row 0
    assert X_masked[0, 2] == 0.0   # 'c', untagged for row 0
    assert X_masked[0, 3] == 1.0   # 'd', not untagged for row 0
    assert X_masked[1, 0] == 0.0   # 'a', untagged for row 1
    assert X_masked[2, 3] == 0.0   # 'd', untagged for row 2

    # avg = (2+1+1)/3 = 4/3 ≈ 1.333... — wait, that's 4/3, not 2.0
    # Actually: row 0 has 2 zeroed, row 1 has 1 zeroed, row 2 has 1 zeroed
    # avg = (2+1+1)/3 = 4/3
    assert abs(stats['avg_features_zeroed'] - (4.0 / 3.0)) < 1e-6


def test_apply_masking_does_not_mutate_input():
    """apply_masking must not mutate its input array."""
    X = np.ones((3, 4), dtype=np.float32)
    X_copy = np.copy(X)
    column_names = ['a', 'b', 'c', 'd']
    untagged_per_hand = [{'b'}, {'c'}, {'d'}]

    apply_masking(X, column_names, untagged_per_hand)

    assert np.array_equal(X, X_copy), "apply_masking must not mutate the input array"


def test_get_named_importances_length():
    """get_named_importances must return a list of length equal to column_names."""

    class MockModel:
        feature_importances_ = np.array([0.1, 0.5, 0.2, 0.05, 0.15])

    result = get_named_importances(MockModel(), ['a', 'b', 'c', 'd', 'e'])
    assert len(result) == 5
    # Must be sorted descending by importance
    importances = [imp for _, imp in result]
    assert importances == sorted(importances, reverse=True)


def test_get_named_importances_mismatch():
    """get_named_importances must raise ValueError if column_names length doesn't match."""

    class MockModel:
        feature_importances_ = np.array([0.1, 0.5, 0.2, 0.05, 0.15])

    with pytest.raises(ValueError):
        get_named_importances(MockModel(), ['a', 'b', 'c'])  # 3 names for 5 importances


def test_run_loo_cv_n_predictions():
    """run_loo_cv must return exactly 20 predictions and 20 true_labels."""
    rng = np.random.default_rng(42)
    X = rng.random((20, 4), dtype=np.float32)
    y = np.array(list(range(5)) * 4, dtype=np.int32)  # 0-4 cycling, 20 items

    true_labels, loo_predictions, n_fold_failures = run_loo_cv(
        X, y, PILOT_XGB_CONFIG_SUBSET, 'test'
    )

    assert len(loo_predictions) == 20
    assert len(true_labels) == 20

    valid_outputs = set(ACTION_CLASSES) | {'FOLD_ERROR'}
    for pred in loo_predictions:
        assert pred in valid_outputs


def test_run_loo_cv_returns_strings():
    """run_loo_cv predictions must be strings (action names), not integers."""
    rng = np.random.default_rng(99)
    X = rng.random((20, 4), dtype=np.float32)
    y = np.array(list(range(5)) * 4, dtype=np.int32)

    _, loo_predictions, _ = run_loo_cv(X, y, PILOT_XGB_CONFIG_SUBSET, 'test_str')

    for pred in loo_predictions:
        assert isinstance(pred, str), f"Expected str, got {type(pred)}: {pred}"


def test_run_loo_cv_fold_failure_handling():
    """run_loo_cv must not raise even when some folds are degenerate."""
    # Create a dataset where one class has only 1 sample
    X = np.ones((20, 4), dtype=np.float32)
    X[:, 0] = np.arange(20)
    # 19 samples of class 0, 1 sample of class 4
    y = np.zeros(20, dtype=np.int32)
    y[0] = 4

    # This will likely produce fold failures (class 4 only appears once)
    try:
        _, _, n_fold_failures = run_loo_cv(X, y, PILOT_XGB_CONFIG_SUBSET, 'test_fail')
        assert n_fold_failures >= 0  # must return a count
    except Exception as e:
        pytest.fail(f"run_loo_cv raised an exception when it should not: {e}")


# ═══════════════════════════════════════════════════════════════════
# INTEGRATION TESTS (skipped by default)
# ═══════════════════════════════════════════════════════════════════

@pytest.mark.integration
def test_assemble_produces_correct_files(tmp_path, monkeypatch):
    """
    Integration test: assembly produces all 5 output files with correct dimensions.
    Skipped unless --integration flag is passed.
    """
    import assemble_pilot_data as asmb

    # Monkeypatch paths to tmp_path
    monkeypatch.setattr(asmb, 'ENRICHED_JSONL_PATH', str(tmp_path / 'pilot_20_enriched.jsonl'))
    monkeypatch.setattr(asmb, 'BASE_CSV_PATH', str(tmp_path / 'pilot_20_base.csv'))
    monkeypatch.setattr(asmb, 'ATTENTION_CSV_PATH', str(tmp_path / 'pilot_20_attention.csv'))
    monkeypatch.setattr(asmb, 'LEVELS_CSV_PATH', str(tmp_path / 'pilot_20_attention_levels.csv'))
    monkeypatch.setattr(asmb, 'INTENTIONS_CSV_PATH', str(tmp_path / 'pilot_20_intentions.csv'))

    asmb.main()

    # Verify all 5 files exist
    for fname in [
        'pilot_20_enriched.jsonl',
        'pilot_20_base.csv',
        'pilot_20_attention.csv',
        'pilot_20_attention_levels.csv',
        'pilot_20_intentions.csv',
    ]:
        fpath = tmp_path / fname
        assert fpath.exists(), f"Missing output file: {fname}"

    # Check pilot_20_base.csv: 20 data rows, 55 columns
    with open(tmp_path / 'pilot_20_base.csv') as f:
        reader = csv.reader(f)
        rows = list(reader)
    assert len(rows) == 21, f"base.csv should have 1 header + 20 data rows, got {len(rows)}"
    assert len(rows[0]) == 55, f"base.csv should have 55 columns, got {len(rows[0])}"

    # Check pilot_20_attention.csv: 109 columns
    with open(tmp_path / 'pilot_20_attention.csv') as f:
        reader = csv.reader(f)
        header = next(reader)
    assert len(header) == 109, f"attention.csv should have 109 columns, got {len(header)}"

    # Check pilot_20_attention_levels.csv: 109 columns
    with open(tmp_path / 'pilot_20_attention_levels.csv') as f:
        reader = csv.reader(f)
        header = next(reader)
    assert len(header) == 109, f"levels.csv should have 109 columns, got {len(header)}"

    # Check pilot_20_intentions.csv: 54 + N_tags columns
    with open(tmp_path / 'pilot_20_intentions.csv') as f:
        reader = csv.reader(f)
        header = next(reader)
    n_tags = sum(1 for col in header if col.startswith('intent_'))
    assert len(header) == 54 + n_tags, f"intentions.csv columns mismatch"

    # Check pilot_20_enriched.jsonl: 20 valid JSON lines
    with open(tmp_path / 'pilot_20_enriched.jsonl') as f:
        lines = f.readlines()
    assert len(lines) == 20, f"enriched.jsonl should have 20 lines, got {len(lines)}"
    for i, line in enumerate(lines):
        try:
            json.loads(line)
        except json.JSONDecodeError as e:
            pytest.fail(f"enriched.jsonl line {i} is not valid JSON: {e}")
