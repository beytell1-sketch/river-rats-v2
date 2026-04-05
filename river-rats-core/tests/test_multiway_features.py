"""Tests for multiway feature extraction (38-feature contract)."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import pytest

from feature_extractor import (
    FEATURE_COLUMNS,
    extract_all_features,
    assign_opponent_positions,
    get_villain_range,
    get_multiway_villain_range,
)
from gto_model import FEATURE_COLUMNS as GTO_COLS, N_FEATURES as GTO_N
from sizing_oracle import FEATURE_COLUMNS as SZ_COLS, N_FEATURES as SZ_N
from train_model import FEATURE_COLUMNS as TM_COLS
from train_sizing_model import FEATURE_COLUMNS as TSM_COLS


def _make_hand(**overrides):
    """Build a valid test hand dict."""
    base = {
        'h': 'AhKd', 'b': 'Ks7h2d', 'pos': 'BTN', 'vp': 'BB',
        'pot': 10.0, 'tc': 5.0, 'st': 'f', 'fb': 1, 'exp': 'C',
    }
    base.update(overrides)
    return base


class TestFeatureContract:
    def test_feature_count_38(self):
        assert len(FEATURE_COLUMNS) == 38

    def test_last_feature_is_num_opponents(self):
        assert FEATURE_COLUMNS[-1] == 'num_opponents'

    def test_feature_columns_consistent_across_modules(self):
        assert list(FEATURE_COLUMNS) == list(GTO_COLS)
        assert list(FEATURE_COLUMNS) == list(SZ_COLS)
        assert list(FEATURE_COLUMNS) == list(TM_COLS)
        assert list(FEATURE_COLUMNS) == list(TSM_COLS)

    def test_n_features_consistent(self):
        assert GTO_N == 38
        assert SZ_N == 38


class TestNumOpponentsExtraction:
    def test_default_num_opponents_is_1(self):
        hand = _make_hand()
        features = extract_all_features(hand)
        assert features['num_opponents'] == 1

    def test_explicit_num_opponents(self):
        for n in [1, 2, 3, 4, 5]:
            hand = _make_hand(_num_opponents=n)
            features = extract_all_features(hand)
            assert features['num_opponents'] == n

    def test_num_opponents_in_feature_columns(self):
        hand = _make_hand(_num_opponents=2)
        features = extract_all_features(hand)
        for col in FEATURE_COLUMNS:
            assert col in features, f"Missing feature: {col}"


class TestAssignOpponentPositions:
    def test_correct_count(self):
        for n in range(1, 6):
            pos = assign_opponent_positions('BTN', n)
            assert len(pos) == n

    def test_excludes_hero(self):
        for hero in ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']:
            pos = assign_opponent_positions(hero, 3)
            assert hero not in pos

    def test_max_5_opponents(self):
        pos = assign_opponent_positions('BTN', 5)
        assert len(pos) == 5
        assert 'BTN' not in pos

    def test_priority_order(self):
        # BB should appear first (most likely in pot)
        pos = assign_opponent_positions('BTN', 3)
        assert pos[0] == 'BB'


class TestMultiwayVillainRange:
    def test_merged_range_is_superset(self):
        hero = 'BTN'
        board = ['Ks', '7h', '2d']
        r1 = get_villain_range(hero, 'UTG')
        r2 = get_villain_range(hero, 'BB')
        merged = get_multiway_villain_range(hero, ['UTG', 'BB'], False, board, 'f')
        for hand in set(list(r1.keys()) + list(r2.keys())):
            assert merged.get(hand, 0) >= max(r1.get(hand, 0), r2.get(hand, 0))

    def test_merged_range_nonempty(self):
        merged = get_multiway_villain_range('BTN', ['UTG', 'BB'], False, ['Ks', '7h', '2d'], 'f')
        assert len(merged) > 0

    def test_more_opponents_wider_range(self):
        board = ['Ks', '7h', '2d']
        r2 = get_multiway_villain_range('BTN', ['UTG', 'BB'], False, board, 'f')
        r3 = get_multiway_villain_range('BTN', ['UTG', 'BB', 'CO'], False, board, 'f')
        assert len(r3) >= len(r2)


class TestMultiwayEquity:
    def test_multiway_equity_differs_from_hu(self):
        hand_hu = _make_hand(_num_opponents=1)
        hand_mw = _make_hand(_num_opponents=3)
        f_hu = extract_all_features(hand_hu)
        f_mw = extract_all_features(hand_mw)
        # Equity against merged range should differ from single-opponent
        assert f_hu['raw_equity'] != f_mw['raw_equity']

    def test_partition_differs_multiway(self):
        hand_hu = _make_hand(_num_opponents=1)
        hand_mw = _make_hand(_num_opponents=3)
        f_hu = extract_all_features(hand_hu)
        f_mw = extract_all_features(hand_mw)
        # better_hand_pct should differ (wider range = more hands that beat you)
        assert f_hu['better_hand_pct'] != f_mw['better_hand_pct']

    def test_hu_behavior_unchanged(self):
        """With num_opponents=1, behavior should match no _num_opponents key."""
        hand_default = _make_hand()
        hand_explicit = _make_hand(_num_opponents=1)
        f_default = extract_all_features(hand_default)
        f_explicit = extract_all_features(hand_explicit)
        for col in FEATURE_COLUMNS:
            if isinstance(f_default[col], float):
                # Monte Carlo equity has random variance between runs
                assert abs(f_default[col] - f_explicit[col]) < 0.05, \
                    f"Mismatch on {col}: {f_default[col]} vs {f_explicit[col]}"
            else:
                assert f_default[col] == f_explicit[col], f"Mismatch on {col}"


class TestOpenerAwareRanges:
    def test_opener_gets_rfi_range(self):
        """CO is opener → RFI['CO']"""
        from range_manager import RangeManager
        rm = RangeManager()
        range_result = get_villain_range('BB', 'CO', opener_pos='CO')
        assert range_result == rm.get_rfi_range('CO')

    def test_cold_caller_gets_defend_range(self):
        """BTN cold-called CO → DEFEND['BTN']['vs_CO'], not RFI"""
        from range_manager import RangeManager
        rm = RangeManager()
        range_result = get_villain_range('BB', 'BTN', opener_pos='CO')
        assert range_result == rm.get_defend_range('BTN', 'CO')
        # Defend range must be tighter than RFI
        rfi = rm.get_rfi_range('BTN')
        assert len(range_result) < len(rfi)

    def test_hu_fallback_no_opener(self):
        """Legacy path — opener_pos=None identical to current behavior"""
        range_old = get_villain_range('BB', 'CO')
        range_new = get_villain_range('BB', 'CO', opener_pos=None)
        assert range_old == range_new

    def test_extraction_with_opener_pos(self):
        """Features extract successfully with _opener_position set"""
        hand = _make_hand(
            h='Ks7h', b='Kc9d4s', pos='BB', vp='CO',
            _num_opponents=3, _opener_position='CO',
            fb=1, pot=100.0, tc=33.0, st='f', exp='C'
        )
        features = extract_all_features(hand)
        for col in FEATURE_COLUMNS:
            assert col in features, f"Missing feature: {col}"

    def test_hu_with_opener_pos_unchanged(self):
        """HU path ignores opener_pos — zero regression"""
        hand_with = _make_hand(_num_opponents=1, _opener_position='CO')
        hand_without = _make_hand(_num_opponents=1)
        f_with = extract_all_features(hand_with)
        f_without = extract_all_features(hand_without)
        for col in FEATURE_COLUMNS:
            if isinstance(f_with[col], float):
                assert abs(f_with[col] - f_without[col]) < 0.05, \
                    f"Mismatch on {col}: {f_with[col]} vs {f_without[col]}"
            else:
                assert f_with[col] == f_without[col], \
                    f"Mismatch on {col}: {f_with[col]} vs {f_without[col]}"

    def test_sb_cold_caller_gets_defend_range(self):
        """SB cold-called CO → DEFEND['SB']['vs_CO']"""
        from range_manager import RangeManager
        rm = RangeManager()
        range_result = get_villain_range('BB', 'SB', opener_pos='CO')
        assert range_result == rm.get_defend_range('SB', 'CO')

    def test_multiway_merged_uses_opener_ranges(self):
        """Merged range with opener_pos should be tighter than without"""
        board = ['Kc', '9d', '4s']
        # Without opener_pos: all get RFI (wider)
        r_old = get_multiway_villain_range('BB', ['BTN', 'SB', 'CO'], False, board, 'f')
        # With opener_pos: BTN/SB get defend ranges (tighter)
        r_new = get_multiway_villain_range('BB', ['BTN', 'SB', 'CO'], False, board, 'f', opener_pos='CO')
        # New merged range should have fewer hands or lower total frequency
        old_total = sum(r_old.values())
        new_total = sum(r_new.values())
        assert new_total < old_total, f"Expected tighter range with opener_pos: {new_total} >= {old_total}"


class TestBettorAwareNarrowing:
    def test_bettor_range_narrowed(self):
        """When bettor_pos='CO', CO's range should be narrowed (via equity difference)"""
        # A hand facing a bet with bettor_pos should produce different equity
        # than the same hand not facing a bet (because bettor range is narrowed)
        hand_facing_bet = _make_hand(
            h='Ks7h', b='Kc9d4s', pos='BB', vp='CO',
            _num_opponents=3, _opener_position='CO', _bettor_position='CO',
            fb=1, pot=100.0, tc=33.0, st='f', exp='C'
        )
        hand_not_facing = _make_hand(
            h='Ks7h', b='Kc9d4s', pos='BB', vp='CO',
            _num_opponents=3, _opener_position='CO',
            fb=0, pot=100.0, tc=0.0, st='f', exp='C'
        )
        f_bet = extract_all_features(hand_facing_bet)
        f_no_bet = extract_all_features(hand_not_facing)
        # Equity should differ (narrowed range changes equity)
        assert f_bet['raw_equity'] != f_no_bet['raw_equity']

    def test_partition_narrows_only_bettor(self):
        """get_multiway_villain_range with bettor_pos narrows only that opponent"""
        board = ['Kc', '9d', '4s']
        # With bettor_pos='CO': only CO narrowed — BTN/SB keep full ranges
        r_bettor = get_multiway_villain_range(
            'BB', ['BTN', 'SB', 'CO'], True, board, 'f',
            opener_pos='CO', bettor_pos='CO'
        )
        # Without bettor_pos: narrow nobody (fallback)
        r_nobody = get_multiway_villain_range(
            'BB', ['BTN', 'SB', 'CO'], True, board, 'f',
            opener_pos='CO', bettor_pos=None
        )
        # With bettor narrowed, the merged range should differ from no-narrowing
        # (CO's betting range is tighter/different from full range)
        assert r_bettor != r_nobody

    def test_no_narrowing_when_not_facing_bet(self):
        """facing_bet=False means no narrowing even with bettor_pos set"""
        board = ['Kc', '9d', '4s']
        r_with_bettor = get_multiway_villain_range(
            'BB', ['BTN', 'SB', 'CO'], False, board, 'f',
            opener_pos='CO', bettor_pos='CO'
        )
        r_no_bettor = get_multiway_villain_range(
            'BB', ['BTN', 'SB', 'CO'], False, board, 'f',
            opener_pos='CO', bettor_pos=None
        )
        assert r_with_bettor == r_no_bettor

    def test_hu_ignores_bettor_pos(self):
        """HU path doesn't use bettor_pos"""
        hand_with = _make_hand(_num_opponents=1, _bettor_position='CO')
        hand_without = _make_hand(_num_opponents=1)
        f_with = extract_all_features(hand_with)
        f_without = extract_all_features(hand_without)
        for col in FEATURE_COLUMNS:
            if isinstance(f_with[col], float):
                assert abs(f_with[col] - f_without[col]) < 0.05, \
                    f"Mismatch on {col}"
            else:
                assert f_with[col] == f_without[col], f"Mismatch on {col}"

    def test_fallback_narrows_nobody(self):
        """When _bettor_position missing, no narrowing occurs"""
        board = ['Kc', '9d', '4s']
        # No bettor_pos, facing_bet=True: nobody should be narrowed
        r_fallback = get_multiway_villain_range(
            'BB', ['BTN', 'SB', 'CO'], True, board, 'f',
            opener_pos='CO', bettor_pos=None
        )
        # Not facing bet: also nobody narrowed
        r_no_bet = get_multiway_villain_range(
            'BB', ['BTN', 'SB', 'CO'], False, board, 'f',
            opener_pos='CO', bettor_pos=None
        )
        # Both should be identical (no narrowing in either case)
        assert r_fallback == r_no_bet

    def test_bettor_not_in_opponents_narrows_nobody(self):
        """Edge case: bettor position not in opponent list"""
        board = ['Kc', '9d', '4s']
        # bettor_pos='HJ' but opponents are BTN, SB, CO
        r = get_multiway_villain_range(
            'BB', ['BTN', 'SB', 'CO'], True, board, 'f',
            opener_pos='CO', bettor_pos='HJ'
        )
        # Should not crash, should be same as no-bet (nobody narrowed)
        r_no_bet = get_multiway_villain_range(
            'BB', ['BTN', 'SB', 'CO'], False, board, 'f',
            opener_pos='CO', bettor_pos=None
        )
        assert r == r_no_bet

    def test_full_extraction_with_bettor_pos(self):
        """Full extraction with bettor_pos produces valid features"""
        hand = _make_hand(
            h='Ks7h', b='Kc9d4s', pos='BB', vp='CO',
            _num_opponents=3, _opener_position='CO', _bettor_position='CO',
            fb=1, pot=100.0, tc=33.0, st='f', exp='C'
        )
        features = extract_all_features(hand)
        for col in FEATURE_COLUMNS:
            assert col in features, f"Missing feature: {col}"
        # Equity should be reasonable (0-1 range)
        assert 0.0 <= features['raw_equity'] <= 1.0
