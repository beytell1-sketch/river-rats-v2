"""v2.4 Stage 3.5 commit 7 — MUST #23 + MUST #55.

MUST #23 — train_sizing_model.py bypass-with-audit per Q20:
  - Sizing trains on PokerBench hands that lack per-street action_history;
    bypass-permanent is the accepted trade-off (sizing is less
    chain-sensitive than composition/equity).
  - CSV schema adds _sizing_chain_bypass audit column (True uniformly).
  - MUST #9 consistency: except RuntimeError: raise precedes
    except Exception: errors += 1.

MUST #55 — review/recovered/eval_*.py deletion:
  - 4 recovered scripts deleted per red-team pass-3 silent-fallback
    findings.
  - No runtime importers (verified via grep).
  - evaluate_v2_2.py docstring updated to note deletion.
"""
import csv
import io
import os
import sys

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)


# =============================================================================
# MUST #23 — sizing CSV schema + bypass audit column
# =============================================================================

def test_sizing_csv_header_includes_bypass_audit_column(tmp_path):
    """MUST #23: save_features_csv writes _sizing_chain_bypass column at
    end of header. Schema: FEATURE_COLUMNS + size_bucket + bypass flag."""
    import numpy as np
    from train_sizing_model import (
        save_features_csv, FEATURE_COLUMNS, RAISE_BUCKET_TO_INT,
    )

    # Minimal 2-row synthetic training data
    X = np.zeros((2, len(FEATURE_COLUMNS)), dtype=np.float32)
    y = np.array([RAISE_BUCKET_TO_INT['STANDARD'],
                  RAISE_BUCKET_TO_INT['SMALL']], dtype=np.int32)
    out_path = tmp_path / 'sizing_test.csv'
    save_features_csv(X, y, str(out_path))

    with open(out_path) as f:
        header_line = f.readline().strip()
    header_cols = header_line.split(',')
    assert '_sizing_chain_bypass' in header_cols, (
        f'MUST #23 audit column absent from CSV header: {header_cols}'
    )
    # Positioned at the END of header
    assert header_cols[-1] == '_sizing_chain_bypass', (
        f'_sizing_chain_bypass not at end: {header_cols}'
    )


def test_sizing_csv_row_writes_true_bypass_value(tmp_path):
    """MUST #23: each row carries True in _sizing_chain_bypass column.
    Uniform marker — sizing CSV is wholly bypass."""
    import numpy as np
    from train_sizing_model import (
        save_features_csv, FEATURE_COLUMNS, RAISE_BUCKET_TO_INT,
    )

    X = np.zeros((3, len(FEATURE_COLUMNS)), dtype=np.float32)
    y = np.array([0, 1, 2], dtype=np.int32)
    out_path = tmp_path / 'sizing_test.csv'
    save_features_csv(X, y, str(out_path))

    with open(out_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 3
    for row in rows:
        assert row['_sizing_chain_bypass'] == 'True', (
            f'MUST #23: expected True marker, got {row["_sizing_chain_bypass"]!r}'
        )


def test_sizing_load_from_csv_tolerates_bypass_column(tmp_path):
    """MUST #23: load_from_csv reads CSVs with or without bypass column.
    Only FEATURE_COLUMNS + size_bucket used; audit column ignored."""
    import numpy as np
    from train_sizing_model import (
        save_features_csv, load_from_csv, FEATURE_COLUMNS,
    )

    X = np.zeros((2, len(FEATURE_COLUMNS)), dtype=np.float32)
    y = np.array([0, 1], dtype=np.int32)
    out_path = tmp_path / 'sizing_test.csv'
    save_features_csv(X, y, str(out_path))

    X_loaded, y_loaded = load_from_csv(str(out_path))
    assert X_loaded.shape == (2, len(FEATURE_COLUMNS))
    assert list(y_loaded) == [0, 1]


def test_sizing_extraction_propagates_runtime_error():
    """MUST #9 consistency in sizing: CRIT #2 RuntimeError must propagate
    out of extract_from_pokerbench's per-hand loop. Silent swallow would
    defeat STAGE4_STRICT_ACTION_HISTORY=raise."""
    import pytest
    import train_sizing_model as tsm

    # Monkey-patch extract_all_features to raise RuntimeError
    _orig = tsm.extract_all_features if hasattr(tsm, 'extract_all_features') else None

    def _raising(hand):
        raise RuntimeError('STAGE4 strict-raise (simulated)')

    # extract_from_pokerbench imports extract_all_features inside the
    # function body; patch at feature_extractor module level
    import feature_extractor
    orig_fe = feature_extractor.extract_all_features
    feature_extractor.extract_all_features = _raising

    # Patch load_raise_hands to return a single synthetic hand
    import pokerbench_parser
    orig_load = pokerbench_parser.load_raise_hands
    pokerbench_parser.load_raise_hands = lambda *a, **kw: [{'_pot_ratio': 0.5}]

    try:
        with pytest.raises(RuntimeError, match='STAGE4 strict-raise'):
            tsm.extract_from_pokerbench(['dummy_chunk'])
    finally:
        feature_extractor.extract_all_features = orig_fe
        pokerbench_parser.load_raise_hands = orig_load


# =============================================================================
# MUST #55 — recovered scripts deleted; no runtime importers
# =============================================================================

def test_must55_recovered_eval_scripts_deleted():
    """MUST #55 path (a): 4 recovered eval_*.py scripts deleted from
    review/recovered/. Red-team pass-3 silent-fallback patterns removed
    at source; their port-forward logic lives in evaluate_v2_2.py."""
    repo_root = os.path.dirname(os.path.dirname(_CORE))
    recovered_dir = os.path.join(repo_root, 'review', 'recovered')
    deleted_files = [
        'eval_FB40_attn_per_feature.py',
        'eval_FB40_plus_ablation.py',
        'eval_MW_test_set_50.py',
        'eval_MW_with_legal_action_masking.py',
    ]
    for fname in deleted_files:
        path = os.path.join(recovered_dir, fname)
        assert not os.path.exists(path), (
            f'MUST #55: {path!r} still exists; commit 7 path (a) '
            f'required deletion. Red-team pass-3 silent-fallback '
            f'findings must not return.'
        )


def test_must55_no_importers_of_deleted_modules():
    """MUST #55 regression guard: no Python source in repo imports from
    the deleted eval_*.py names (they would ModuleNotFoundError at
    runtime). Docstrings / comms docs may still reference the names for
    archaeology; code imports must not."""
    import subprocess
    repo_root = os.path.dirname(os.path.dirname(_CORE))
    patterns = [
        r'from\s+review\.recovered\.eval_FB40',
        r'from\s+review\.recovered\.eval_MW',
        r'import\s+review\.recovered\.eval_FB40',
        r'import\s+review\.recovered\.eval_MW',
    ]
    combined = '|'.join(patterns)
    result = subprocess.run(
        ['grep', '-rn', '--include=*.py', '-E', combined, repo_root],
        capture_output=True, text=True,
    )
    # grep returncode 1 = no matches (pass); 0 = matches found (fail)
    offenders = [
        line for line in result.stdout.splitlines()
        if line.strip() and '/tests/' not in line
    ]
    assert not offenders, (
        f'MUST #55 regression: {len(offenders)} import(s) of deleted '
        f'recovered modules:\n' + '\n'.join(offenders)
    )


if __name__ == '__main__':
    import subprocess
    rc = subprocess.call([sys.executable, '-m', 'pytest', '-xvs', __file__])
    sys.exit(rc)
