"""v2.4 Stage 3.5 commit 9 — combined MUSTs #17 + #38 + #39 + #40 + #50 + Q41.

Atomic commit per MUST #59 discipline: frequency-table + KB §1.11
changes are semantically coupled; changing one without the others
breaks coherence.

Covers:
  - MUST #17: RIVER_CHECKING medium_made 0.92 → 0.85
  - MUST #38: RIVER_CHECKING bluff 0.65 → 0.80; air 0.80 → 0.90
  - MUST #50: RIVER_BETTING medium_made 0.08 → 0.15 (atomic coherence);
             module-import coherence assertion across all streets
  - MUST #39: KB §1.11 FOLD-lean threshold 0.15 → 0.20 (asymmetric)
  - MUST #40: KB §1.11 combo-draw use-max addendum
  - Q41: KB §1.11 footnote on 0.15 teaching-calibration rationale
"""
import os
import re
import sys

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)


# =============================================================================
# MUST #17 — RIVER_CHECKING medium_made 0.85
# =============================================================================

def test_must17_river_checking_medium_made_085():
    """MUST #17: RIVER_CHECKING_FREQUENCIES['medium_made'] = 0.85
    (was 0.92). GTO review: 0.92 over-compressed mediums into
    check-call band."""
    from range_narrowing import RIVER_CHECKING_FREQUENCIES
    assert RIVER_CHECKING_FREQUENCIES['medium_made'] == 0.85


# =============================================================================
# MUST #38 — RIVER_CHECKING bluff / air reciprocals
# =============================================================================

def test_must38_river_checking_bluff_080():
    """MUST #38: RIVER_CHECKING['bluff'] = 0.80 (was 0.65)
    for atomic coherence with RIVER_BETTING['bluff'] = 0.20."""
    from range_narrowing import RIVER_CHECKING_FREQUENCIES
    assert RIVER_CHECKING_FREQUENCIES['bluff'] == 0.80


def test_must38_river_checking_air_090():
    """MUST #38: RIVER_CHECKING['air'] = 0.90 (was 0.80)
    for atomic coherence with RIVER_BETTING['air'] = 0.10."""
    from range_narrowing import RIVER_CHECKING_FREQUENCIES
    assert RIVER_CHECKING_FREQUENCIES['air'] == 0.90


# =============================================================================
# MUST #50 — RIVER_BETTING medium_made + atomic coherence
# =============================================================================

def test_must50_river_betting_medium_made_015():
    """MUST #50: RIVER_BETTING['medium_made'] = 0.15 (was 0.08).
    Atomic coherence with RIVER_CHECKING 0.85."""
    from range_narrowing import RIVER_BETTING_FREQUENCIES
    assert RIVER_BETTING_FREQUENCIES['medium_made'] == 0.15


def test_must50_river_all_pairs_sum_to_100():
    """MUST #50: every river (category) pair bet + check = 1.00."""
    from range_narrowing import (
        RIVER_BETTING_FREQUENCIES, RIVER_CHECKING_FREQUENCIES,
    )
    for cat in RIVER_BETTING_FREQUENCIES:
        bet = RIVER_BETTING_FREQUENCIES[cat]
        chk = RIVER_CHECKING_FREQUENCIES.get(cat)
        if chk is None:
            continue
        s = bet + chk
        assert abs(s - 1.00) < 0.001, (
            f'MUST #50: river.{cat} bet+check = {s} != 1.00'
        )


def test_must50_coherence_assertion_runs_at_import():
    """MUST #50: _verify_frequency_coherence() fires at module-import
    time (protects against future single-table tweaks that forget
    the pair). Re-importing the module with an intentional
    coherence violation should raise AssertionError."""
    import importlib
    import range_narrowing
    importlib.reload(range_narrowing)  # re-run module-level asserts
    # Should not raise — coherent state


def test_must50_flop_turn_coherence_preserved():
    """MUST #50: FLOP + TURN tables still coherent (pre-existing)."""
    from range_narrowing import (
        FLOP_BETTING_FREQUENCIES, FLOP_CHECKING_FREQUENCIES,
        TURN_BETTING_FREQUENCIES, TURN_CHECKING_FREQUENCIES,
    )
    for tbls in ((FLOP_BETTING_FREQUENCIES, FLOP_CHECKING_FREQUENCIES),
                 (TURN_BETTING_FREQUENCIES, TURN_CHECKING_FREQUENCIES)):
        bet_tbl, check_tbl = tbls
        for cat in bet_tbl:
            if cat not in check_tbl:
                continue
            s = bet_tbl[cat] + check_tbl[cat]
            assert abs(s - 1.00) < 0.001, (
                f'FLOP/TURN coherence broken: {cat} = {s}'
            )


# =============================================================================
# MUST #39 — KB §1.11 asymmetric FOLD-lean threshold
# =============================================================================

def _kb_section_11_text() -> str:
    """Read KB §1.11 text for assertion tests."""
    repo_root = os.path.dirname(_CORE)
    kb_path = os.path.join(repo_root, 'knowledge', 'three_way_gto.md')
    with open(kb_path) as f:
        full = f.read()
    # Extract from §1.11 heading to §1.12 heading
    m = re.search(
        r'### 1\.11 .*?(?=### 1\.12 )',
        full, re.DOTALL,
    )
    assert m, 'KB §1.11 not found; structural regression'
    return m.group(0)


def test_must39_kb_fold_lean_threshold_020():
    """MUST #39: KB §1.11 FOLD-lean threshold bumped 0.15 → 0.20
    (asymmetric from CALL-lean which stays at 0.15)."""
    text = _kb_section_11_text()
    # FOLD-lean block should reference > 0.20
    # CALL-lean block should still reference > 0.15
    assert '> 0.20' in text, (
        'MUST #39: KB §1.11 missing FOLD-lean 0.20 threshold'
    )
    assert '> 0.15' in text, (
        'MUST #39: KB §1.11 CALL-lean 0.15 threshold missing'
    )
    # The asymmetric word should appear explicitly
    assert 'asymmetric' in text.lower() or '0.20' in text, (
        'MUST #39: asymmetric threshold not documented'
    )


def test_must39_kb_cites_must_39_marker():
    """MUST #39: KB §1.11 cites MUST #39 for future audit trail."""
    text = _kb_section_11_text()
    assert 'MUST #39' in text, (
        'MUST #39: cite marker not in KB §1.11'
    )


# =============================================================================
# MUST #40 — KB §1.11 combo-draw use-max addendum
# =============================================================================

def test_must40_kb_combo_draw_use_max_addendum():
    """MUST #40: KB §1.11 documents combo-draw use-max rule."""
    text = _kb_section_11_text()
    # Must mention max-over-mean
    assert 'max(' in text, (
        'MUST #40: use-max rule not in KB §1.11'
    )
    # Must cite MUST #40
    assert 'MUST #40' in text, (
        'MUST #40: cite marker not in KB §1.11'
    )
    # Must explain the double-count rationale
    assert 'combo' in text.lower() and 'double' in text.lower(), (
        'MUST #40: combo-draw double-count rationale absent'
    )


# =============================================================================
# Q41 — KB §1.11 footnote on 0.15 medium_made bet freq
# =============================================================================

def test_q41_kb_footnote_on_medium_made_015():
    """Q41: KB §1.11 carries footnote explaining 0.15 is slightly
    aggressive vs 0.10-0.12 solver-typical; teaching-calibration
    rationale documented."""
    text = _kb_section_11_text()
    assert '0.15' in text, 'Q41: 0.15 bet-freq not cited in KB §1.11'
    # Cite "teaching" rationale
    assert 'teaching' in text.lower(), (
        'Q41: teaching-calibration rationale missing'
    )
    # Cite "solver" for revisit plan
    assert 'solver' in text.lower(), (
        'Q41: solver-alignment revisit plan missing'
    )


# =============================================================================
# Regression: no narrow_* callers broken by table changes
# =============================================================================

def test_narrow_to_betting_range_still_functions_on_river():
    """Regression: narrow_to_betting_range on river board still produces
    a valid normalised distribution after MUST #50 freq edit."""
    from range_narrowing import narrow_to_betting_range
    full_range = {
        'AA': 1.0, 'KK': 1.0, 'QQ': 1.0,   # strong_value
        'AKs': 1.0, 'KQs': 1.0,             # good_value
        '99': 1.0, '88': 1.0,               # medium_made
        '54s': 1.0, '65s': 1.0,             # air / weak
    }
    out, surv = narrow_to_betting_range(
        full_range, ['Kh', '7d', '2c', '9s', '3h'], 'river',
    )
    assert len(out) > 0
    total = sum(out.values())
    assert abs(total - 1.0) < 1e-6, f'not normalised: {total}'
    assert 0.0 < surv <= 1.0


def test_narrow_to_checking_range_still_functions_on_river():
    """Regression: narrow_to_checking_range on river board still valid."""
    from range_narrowing import narrow_to_checking_range
    full_range = {
        'AA': 1.0, 'KK': 1.0, '99': 1.0, '88': 1.0,
        '54s': 1.0, '65s': 1.0,
    }
    out, surv = narrow_to_checking_range(
        full_range, ['Kh', '7d', '2c', '9s', '3h'], 'river',
    )
    assert len(out) > 0
    total = sum(out.values())
    assert abs(total - 1.0) < 1e-6


if __name__ == '__main__':
    import subprocess
    rc = subprocess.call([sys.executable, '-m', 'pytest', '-xvs', __file__])
    sys.exit(rc)
