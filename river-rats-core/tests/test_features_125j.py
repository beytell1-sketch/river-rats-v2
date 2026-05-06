"""Unit tests for 12.5J-B Direction-X-retro features (Step 18, positions 60-61).

Spec: review/comms/PLAN_PHASE125J_FEATURE_ENGINEERING_2026-05-06.md
Implementation: river-rats-core/feature_extractor.py:compute_nut_blocker_overcard_count
                river-rats-core/feature_extractor.py:compute_bet_call_multiway_oop_raise_pressure_index

Two new features added to bridge MW-17 (E-FEATURE primary; nut blocker +
overcards on zero-FD-outs hands) and MW-47 (v3.4 Fix 2.1.1 clause-e
equivalent at the model layer for bet+call multiway).

Both are pure composites of existing features; no new range/board/equity
work. Built on top of existing nut_flush_block + has_flush_draw +
overcard_outs / high_card_rank surface.
"""
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CORE = os.path.join(REPO_ROOT, "river-rats-core")
if CORE not in sys.path:
    sys.path.insert(0, CORE)

from feature_extractor import (
    compute_nut_blocker_overcard_count,
    compute_bet_call_multiway_oop_raise_pressure_index,
    extract_all_features,
    FEATURE_COLUMNS,
)
from feature_keys import F


# ─── Module-load shape assertions ─────────────────────────────────────


def test_feature_columns_extended_to_61():
    assert len(FEATURE_COLUMNS) == 61


def test_step18_features_at_tail():
    assert FEATURE_COLUMNS[-2] == "nut_blocker_overcard_count"
    assert FEATURE_COLUMNS[-1] == "bet_call_multiway_oop_raise_pressure_index"


# ─── nut_blocker_overcard_count (MW-17 axis) ──────────────────────────


def test_nbc_mw17_pattern_returns_2():
    # MW-17: AdKs on Jd8d4c. Ad nut blocker (diamond board); A+K both > J.
    # high_card_rank = 11 (J). nut_flush_block = 1.
    result = compute_nut_blocker_overcard_count(['Ad', 'Ks'], 11, 1)
    assert result == 2


def test_nbc_returns_0_when_no_nut_blocker():
    # Same overcards but no nut blocker → composite must be 0.
    result = compute_nut_blocker_overcard_count(['Ad', 'Ks'], 11, 0)
    assert result == 0


def test_nbc_mw47_pattern_returns_1():
    # MW-47: AsQs on KsJd5s. A is nut blocker (spade); A>K but Q<K.
    # high_card_rank = 13 (K). nut_flush_block = 1.
    # Only A is overcard (Q<K) → 1.
    result = compute_nut_blocker_overcard_count(['As', 'Qs'], 13, 1)
    assert result == 1


def test_nbc_no_overcards_returns_0():
    # Hero 7c2d on Ah-K-9: no overcards above board high A=14 → 0.
    result = compute_nut_blocker_overcard_count(['7c', '2d'], 14, 1)
    assert result == 0


def test_nbc_returns_2_for_AK_on_Q_high_with_blocker():
    # AdKd on Qh8d4c: A and K both > Q; nut_flush_block = 1 (Ad on diamond board).
    # Note: this is suited NFD pattern; nbc captures the overcard count.
    result = compute_nut_blocker_overcard_count(['Ad', 'Kd'], 12, 1)
    assert result == 2


# ─── bet_call_multiway_oop_raise_pressure_index (MW-47 axis) ──────────


def test_pri_mw47_pattern_returns_1_1():
    # MW-47: facing_bet=1, num_callers_to_bet=1, num_opponents=3, is_ip=0,
    # nut_flush_block=1, has_flush_draw=1, raw_equity=0.45.
    # Expected: 1.0 (NFD strength) + 0.3 (1 caller) - 0.2 (OOP) = 1.1.
    result = compute_bet_call_multiway_oop_raise_pressure_index(
        facing_bet=1, num_callers_to_bet=1, num_opponents=3, is_ip=0,
        nut_flush_block=1, has_flush_draw=1, raw_equity=0.45,
    )
    assert abs(result - 1.1) < 1e-6


def test_pri_returns_0_when_not_facing_bet():
    result = compute_bet_call_multiway_oop_raise_pressure_index(
        facing_bet=0, num_callers_to_bet=1, num_opponents=3, is_ip=0,
        nut_flush_block=1, has_flush_draw=1, raw_equity=0.45,
    )
    assert result == 0.0


def test_pri_returns_0_when_no_callers_to_bet_HU_line():
    # Single bet HU (no callers) — clause-e doesn't apply.
    result = compute_bet_call_multiway_oop_raise_pressure_index(
        facing_bet=1, num_callers_to_bet=0, num_opponents=2, is_ip=0,
        nut_flush_block=1, has_flush_draw=1, raw_equity=0.45,
    )
    assert result == 0.0


def test_pri_returns_0_when_IP():
    # IP hero — clause-e specifically applies to OOP raise pressure.
    result = compute_bet_call_multiway_oop_raise_pressure_index(
        facing_bet=1, num_callers_to_bet=1, num_opponents=3, is_ip=1,
        nut_flush_block=1, has_flush_draw=1, raw_equity=0.45,
    )
    assert result == 0.0


def test_pri_returns_0_when_no_nut_blocker():
    result = compute_bet_call_multiway_oop_raise_pressure_index(
        facing_bet=1, num_callers_to_bet=1, num_opponents=3, is_ip=0,
        nut_flush_block=0, has_flush_draw=1, raw_equity=0.45,
    )
    assert result == 0.0


def test_pri_returns_0_when_no_FD():
    result = compute_bet_call_multiway_oop_raise_pressure_index(
        facing_bet=1, num_callers_to_bet=1, num_opponents=3, is_ip=0,
        nut_flush_block=1, has_flush_draw=0, raw_equity=0.45,
    )
    assert result == 0.0


def test_pri_returns_0_when_equity_below_threshold():
    result = compute_bet_call_multiway_oop_raise_pressure_index(
        facing_bet=1, num_callers_to_bet=1, num_opponents=3, is_ip=0,
        nut_flush_block=1, has_flush_draw=1, raw_equity=0.30,
    )
    assert result == 0.0


def test_pri_increases_with_more_callers():
    # 2 callers should give higher pressure than 1.
    pri_1 = compute_bet_call_multiway_oop_raise_pressure_index(
        facing_bet=1, num_callers_to_bet=1, num_opponents=3, is_ip=0,
        nut_flush_block=1, has_flush_draw=1, raw_equity=0.45,
    )
    pri_2 = compute_bet_call_multiway_oop_raise_pressure_index(
        facing_bet=1, num_callers_to_bet=2, num_opponents=4, is_ip=0,
        nut_flush_block=1, has_flush_draw=1, raw_equity=0.45,
    )
    assert pri_2 > pri_1
    # 1.0 + 0.6 - 0.2 = 1.4
    assert abs(pri_2 - 1.4) < 1e-6


# ─── End-to-end via extract_all_features ──────────────────────────────


def test_extract_all_features_includes_step18_features_for_mw17():
    """Integration test: full pipeline produces both new features for MW-17."""
    hand_dict = {
        'h': 'AdKs', 'b': 'Jd8d4c', 'pos': 'BB', 'vp': 'CO',
        'pot': 13.0, 'tc': 5.0, 'st': 'f', 'fb': 1, 'exp': 'C',
        F.META_NUM_OPPONENTS: 2, F.META_NUM_RAISES: 0,
        F.META_OPENER_POSITION: 'CO', F.META_BETTOR_POSITION: 'CO',
        '_villain_aggression_count': 1, '_villain_checked_back': 0,
        '_villain_call_count': 0, '_num_callers_to_bet': 0,
        '_facing_raise': 0, '_action_history': [],
    }
    feat_dict = extract_all_features(hand_dict)
    # MW-17 has nut_flush_block=1 (Ad on diamond board) + 2 overcards (A, K above J)
    assert feat_dict['nut_blocker_overcard_count'] == 2
    # MW-17 is HU after BTN folds (num_callers_to_bet=0) → pressure_index=0
    assert feat_dict['bet_call_multiway_oop_raise_pressure_index'] == 0.0


def test_extract_all_features_includes_step18_features_for_mw47():
    """Integration test: full pipeline produces both new features for MW-47."""
    hand_dict = {
        'h': 'AsQs', 'b': 'KsJd5s', 'pos': 'SB', 'vp': 'CO',
        'pot': 240.0, 'tc': 40.0, 'st': 'f', 'fb': 1, 'exp': 'C',
        F.META_NUM_OPPONENTS: 3, F.META_NUM_RAISES: 0,
        F.META_OPENER_POSITION: 'CO', F.META_BETTOR_POSITION: 'CO',
        '_villain_aggression_count': 1, '_villain_checked_back': 0,
        '_villain_call_count': 1, '_num_callers_to_bet': 1,
        '_facing_raise': 0, '_action_history': [],
    }
    feat_dict = extract_all_features(hand_dict)
    # MW-47: A is overcard above K (Q is not); nut_flush_block=1 → nbc=1
    assert feat_dict['nut_blocker_overcard_count'] == 1
    # MW-47: facing_bet=1 + num_callers_to_bet=1 + OOP + NFD+blocker + eq>0.35 → 1.1
    assert abs(feat_dict['bet_call_multiway_oop_raise_pressure_index'] - 1.1) < 1e-6
