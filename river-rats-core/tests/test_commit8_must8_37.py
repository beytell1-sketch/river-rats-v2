"""v2.4 Stage 3.5 commit 8 — MUST #8 partial delete + MUST #37 sys.path audit.

MUST #8 partial delete (narrowed scope per v2.2 amendment):
  - coaching/feature_extractor.py DELETED (stale duplicate; zero importers)
  - coaching/range_narrowing.py DELETED (same)
  - Rest of coaching/ survives (load-bearing facade implementations)
  - Full coaching/ collapse queued as v2.5+ candidate

MUST #37 sys.path side-effect audit:
  - Pre-deletion audit: both deleted files mutate sys.path on import
    (`/mnt/project` insert + `/home/claude` prepend). Verified no
    surviving coaching/* module depends on those mutations (23/23
    import in isolation without them).
  - Surviving coaching/raw_equity.py has its OWN `/mnt/project` insert
    at line 38 — independent of deleted modules.

Tests:
  - Regression guard: both deleted modules raise ModuleNotFoundError
    on import attempt
  - Sanity: all 23 surviving coaching/* modules still import cleanly
  - Import-regression grep: no runtime import of the deleted names
    anywhere in repo source (docstrings ignored via /tests/ self-ref
    exclusion + per-line shape check)
"""
import importlib
import os
import sys

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)


# =============================================================================
# MUST #8 — deleted modules raise ModuleNotFoundError
# =============================================================================

def test_must8_coaching_feature_extractor_deleted():
    """MUST #8: coaching.feature_extractor not importable post-delete."""
    import pytest
    # Clear any cache
    sys.modules.pop('coaching.feature_extractor', None)
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module('coaching.feature_extractor')


def test_must8_coaching_range_narrowing_deleted():
    """MUST #8: coaching.range_narrowing not importable post-delete."""
    import pytest
    sys.modules.pop('coaching.range_narrowing', None)
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module('coaching.range_narrowing')


def test_must8_deleted_files_absent_on_disk():
    """MUST #8: verify the 2 files are gone from the filesystem
    (regression guard — readers should point at root
    feature_extractor.py + range_narrowing.py)."""
    core = _CORE
    deleted = [
        'coaching/feature_extractor.py',
        'coaching/range_narrowing.py',
    ]
    for rel in deleted:
        path = os.path.join(core, rel)
        assert not os.path.exists(path), (
            f'MUST #8: {rel!r} still present on disk post-delete.'
        )


# =============================================================================
# MUST #37 — surviving coaching/* imports cleanly in isolation
# =============================================================================

_SURVIVING_COACHING_MODULES = (
    'coaching.board_analyzer',
    'coaching.decision_reporter',
    'coaching.equity_types',
    'coaching.explain_hand',
    'coaching.explanation',
    'coaching.feature_keys',
    'coaching.gto_model',
    'coaching.hand_categories',
    'coaching.hand_context',
    'coaching.hand_evaluator',
    'coaching.level_renderer',
    'coaching.levels',
    'coaching.multiway_adjuster',
    'coaching.narrative_builder',
    'coaching.observation_builders',
    'coaching.range_manager',
    'coaching.raw_equity',
    'coaching.shap_explainer',
    'coaching.situation_describer',
    'coaching.sizing_oracle',
    'coaching.spot_classifier',
    'coaching.spot_narratives',
    'coaching.spot_observation',
)


def test_must37_all_surviving_coaching_modules_importable():
    """MUST #37 post-deletion audit: each of the 23 surviving coaching/*
    modules imports cleanly. Deleted modules' sys.path side-effects
    (/mnt/project + /home/claude prepends) are NOT required by any
    survivor — verified by this import-in-isolation test."""
    failed = []
    for name in _SURVIVING_COACHING_MODULES:
        try:
            # Force re-import: pop from cache if present
            sys.modules.pop(name, None)
            importlib.import_module(name)
        except Exception as e:
            failed.append((name, type(e).__name__, str(e)[:200]))
    assert not failed, (
        f'MUST #37: {len(failed)} surviving coaching/* module(s) failed '
        f'to import:\n' + '\n'.join(
            f'  {n}: {t}: {m}' for n, t, m in failed
        )
    )


def test_must37_raw_equity_independent_sys_path_mutation():
    """MUST #37: coaching/raw_equity.py has its OWN /mnt/project insert
    (line 38). Not a dependency on the deleted modules' mutations;
    confirms independence."""
    core = _CORE
    path = os.path.join(core, 'coaching', 'raw_equity.py')
    with open(path) as f:
        src = f.read()
    assert "sys.path.insert(0, '/mnt/project')" in src, (
        'MUST #37: coaching/raw_equity.py no longer has own '
        '/mnt/project insert — scope drift; verify independence.'
    )


# =============================================================================
# Import-regression grep — no runtime import of deleted names
# =============================================================================

def test_no_runtime_imports_of_deleted_coaching_modules():
    """Repo-wide: no Python source file (outside /tests/) has a live
    import of coaching.feature_extractor or coaching.range_narrowing.
    Docstring references + comments are permitted; `from` / `import`
    statement lines are not."""
    import subprocess
    repo_root = os.path.dirname(_CORE)
    patterns = [
        r'^\s*from\s+coaching\.(feature_extractor|range_narrowing)',
        r'^\s*import\s+coaching\.(feature_extractor|range_narrowing)',
    ]
    combined = '|'.join(patterns)
    result = subprocess.run(
        ['grep', '-rn', '--include=*.py', '-E', combined, repo_root],
        capture_output=True, text=True,
    )
    offenders = [
        line for line in result.stdout.splitlines()
        if line.strip() and '/tests/' not in line
    ]
    assert not offenders, (
        f'MUST #8 regression: live import(s) of deleted coaching/* '
        f'modules:\n' + '\n'.join(offenders)
    )


if __name__ == '__main__':
    import subprocess
    rc = subprocess.call([sys.executable, '-m', 'pytest', '-xvs', __file__])
    sys.exit(rc)
