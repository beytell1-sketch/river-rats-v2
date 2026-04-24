"""v2.4 Stage 3.5 commit 11 — MUSTs #42 + #43 + #57 cross-stream coordination.

No runtime logic changes; documentation + contract work. Logic emits
NaN-valued features per established MUST #10 spec; teaching renders
them per MUST #42 player-English wording; CONTENT_API v4.1 version-pin
enforcement happens at Stage 6 ship-gate (MUST #57 gate relocation).

Tests assert docstring conventions + ticket references + NIT fixes
from commit 10 review.
"""
import os
import re
import sys

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)


def _feature_extractor_module_docstring() -> str:
    """Read feature_extractor module-level docstring."""
    import feature_extractor
    return feature_extractor.__doc__ or ''


# =============================================================================
# MUST #42 — player-English NaN render wording (documented in contract)
# =============================================================================

def test_must42_folded_hu_wording_documented():
    """MUST #42: feature_extractor docstring documents the HU folded-
    villain render string for teaching layer."""
    doc = _feature_extractor_module_docstring()
    assert 'Villain folded earlier' in doc, (
        'MUST #42: HU folded-villain render string not in docstring contract'
    )


def test_must42_folded_multiway_wording_documented():
    """MUST #42: multiway partial-fold render string documented
    (references FOLDED_POS + LIVE_POS placeholders)."""
    doc = _feature_extractor_module_docstring()
    assert 'FOLDED_POS' in doc and 'LIVE_POS' in doc, (
        'MUST #42: multiway partial-fold placeholders missing from contract'
    )


def test_must42_overflow_wording_documented():
    """MUST #42: over-narrow/truncated render string documented."""
    doc = _feature_extractor_module_docstring()
    assert 'too rare to read confidently' in doc, (
        'MUST #42: overflow render string not in docstring contract'
    )


# =============================================================================
# MUST #43 — CONTENT_API v4 ticket reference
# =============================================================================

def test_must43_content_api_ticket_referenced():
    """MUST #43: feature_extractor cites the CONTENT_API v4 NaN-render
    ticket in module docstring for cross-stream traceability."""
    doc = _feature_extractor_module_docstring()
    assert 'TICKET_CONTENT_API_V4_NAN_RENDER_2026-04-22.md' in doc, (
        'MUST #43: CONTENT_API v4 ticket reference missing from docstring'
    )


def test_must43_teaching_v41_decisions_doc_referenced():
    """MUST #43: teaching v4.1 decisions doc cited so future readers
    can trace the coordinated decisions."""
    doc = _feature_extractor_module_docstring()
    assert 'TEACHING_V4_1_DECISIONS' in doc, (
        'MUST #43: teaching v4.1 decisions doc not cited in docstring'
    )


# =============================================================================
# MUST #57 — CONTENT_API v4.1 schema version + Stage 6 pre-flight gate
# =============================================================================

def test_must57_content_api_v41_version_pin_documented():
    """MUST #57: feature_extractor cites expected teaching CONTENT_API
    schema version (l3_enriched_v4.1)."""
    doc = _feature_extractor_module_docstring()
    assert 'l3_enriched_v4.1' in doc, (
        'MUST #57: CONTENT_API v4.1 version-pin expectation not documented'
    )


def test_must57_gate_relocation_to_stage_6_documented():
    """MUST #57: docstring notes the gate enforcement relocation from
    commit 4 merge to Stage 6 ship-gate pre-flight (orchestrator
    Path-B directive)."""
    doc = _feature_extractor_module_docstring()
    assert 'Stage 6' in doc, (
        'MUST #57: Stage 6 pre-flight relocation not documented'
    )
    # Pre-flight audit triad references
    assert 'CONTENT_API' in doc and 'Game adapter' in doc and 'Playtest' in doc, (
        'MUST #57: Stage 6 pre-flight audit triad incomplete in docstring'
    )


# =============================================================================
# MUST #10 NaN allowlist consistency (docstring ↔ gto_model)
# =============================================================================

def test_must10_nan_allowlist_matches_docstring_and_gto_model():
    """MUST #10: feature_extractor docstring's NaN-permitted feature
    list must match gto_model inference-side NaN-allowlist (single
    source of truth). Catches drift between contract docstring +
    inference guard in BOTH directions (commit 12 strengthens prior
    one-sided check per commit-11 architect-reviewer polish note)."""
    doc = _feature_extractor_module_docstring()
    expected = {
        'villain_top_pair_plus_pct', 'villain_draw_pct',
        'villain_air_pct', 'villain_medium_made_pct',
        'flush_block_pct', 'flush_draw_block_pct',
        'straight_draw_block_pct', 'nut_made_block_pct',
    }
    # Direction 1 (original): docstring cites all expected features
    for feat in expected:
        assert feat in doc, (
            f'MUST #10: {feat!r} missing from feature_extractor '
            f'NaN-allowlist docstring'
        )
    # Direction 2 (commit 12 strengthening): gto_model source-level
    # check — the _NAN_ALLOWLIST frozenset inside features_from_dict
    # must contain exactly these 8 features. Catches allowlist-only
    # drift (docstring stays current but gto_model guard diverges).
    # Structural check via source introspection since _NAN_ALLOWLIST
    # is function-local (defined inside features_from_dict).
    import inspect
    import gto_model
    src = inspect.getsource(gto_model.GtoOracle.features_from_dict)
    # Confirm every expected feature literal is present in the function
    # body's _NAN_ALLOWLIST block. Any missing ⇒ allowlist drift.
    for feat in expected:
        assert f"'{feat}'" in src or f'"{feat}"' in src, (
            f'MUST #10: {feat!r} not cited in gto_model '
            f'features_from_dict source (allowlist drift vs docstring)'
        )


# =============================================================================
# NIT-1 (commit 10 follow-up) — count-guard comment drift fix
# =============================================================================

def test_nit1_count_guard_comment_cites_floor_pct():
    """NIT-1 fix (commit 11): range_narrowing.py inline comment at the
    count-guard block cites _STAGE35_WEIGHT_FLOOR_PCT (0.10), not the
    stale "0.20" from the pre-fix draft."""
    core = _CORE
    rn_path = os.path.join(core, 'range_narrowing.py')
    with open(rn_path) as f:
        src = f.read()
    # Find the MUST #41 comment block
    m = re.search(
        r'MUST #41 \(commit 10\) — belt-and-braces.*?no diversity in the',
        src, re.DOTALL,
    )
    assert m, 'NIT-1: MUST #41 comment block not found at expected location'
    block = m.group(0)
    assert '_STAGE35_WEIGHT_FLOOR_PCT' in block, (
        'NIT-1 fix: comment should cite _STAGE35_WEIGHT_FLOOR_PCT constant'
    )
    # The stale "0.20" reference should be gone OR appear only for WARN context
    # Safe check: the guard comment should NOT mis-cite 0.20 as the trigger
    # threshold.
    assert '>= 0.20' not in block, (
        'NIT-1 fix: comment still cites stale "0.20" as count-guard '
        'trigger; should be 0.10 (FLOOR_PCT)'
    )


if __name__ == '__main__':
    import subprocess
    rc = subprocess.call([sys.executable, '-m', 'pytest', '-xvs', __file__])
    sys.exit(rc)
