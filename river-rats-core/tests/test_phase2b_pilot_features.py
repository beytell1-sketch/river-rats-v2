"""Unit tests for Phase 2-C cleanup features (Step 18; 2 winners).

Per dispatch PR #400 (owner-ratified Option B; supersedes PR #396 re-pilot):
  1. players_to_act_after_hero — KEEP (re-pilot 3.36% importance, rank #10/63)
  2. tpmk_kicker_rank          — KEEP (re-pilot 9.18% importance, rank #2/63)

Dropped from re-pilot (below ≥2% importance gate; baseline-absorbed):
  - broadway_pressure_multiway_facing (0.26%)
  - nut_fd_blocker_multiway (1.87%)
"""
from __future__ import annotations

import math
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feature_extractor import extract_all_features
from feature_keys import F


def _hu_hand(hero='AhKs', board='Ad8c3h', pos='BTN', vp='BB',
             pot=5.5, tc=0.0, st='f', fb=0):
    return {
        'h': hero, 'b': board, 'pos': pos, 'vp': vp,
        'pot': pot, 'tc': tc, 'st': st, 'fb': fb, 'exp': 'C',
        F.META_NUM_OPPONENTS: 1, F.META_NUM_RAISES: 0,
        F.META_OPENER_POSITION: pos, F.META_BETTOR_POSITION: vp if fb else None,
        '_villain_aggression_count': 1 if fb else 0,
        '_villain_checked_back': 0, '_villain_call_count': 0,
        '_num_callers_to_bet': 0, '_facing_raise': 0,
        '_action_history': [],
    }


def _multiway_hand(hero, board, pos, vp, num_opp, pot=15.0, tc=0.0,
                   st='f', fb=0):
    return {
        'h': hero, 'b': board, 'pos': pos, 'vp': vp,
        'pot': pot, 'tc': tc, 'st': st, 'fb': fb, 'exp': 'C',
        F.META_NUM_OPPONENTS: num_opp, F.META_NUM_RAISES: 0,
        F.META_OPENER_POSITION: pos, F.META_BETTOR_POSITION: vp if fb else None,
        '_villain_aggression_count': 1 if fb else 0,
        '_villain_checked_back': 0, '_villain_call_count': 0,
        '_num_callers_to_bet': 0, '_facing_raise': 0,
        '_action_history': [],
    }


def _finite(v):
    return isinstance(v, (int, float)) and not math.isnan(v) and not math.isinf(v)


# ─── Feature 1: players_to_act_after_hero ─────────────────────────────

class TestPlayersToActAfterHero:
    """0 if IP, num_opponents if OOP. Re-pilot 3.36% rank #10/63."""

    def test_zero_when_hero_is_ip_hu(self):
        f = extract_all_features(_hu_hand('AhKs', 'Ad8c3h', pos='BTN', vp='BB'))
        assert _finite(f['players_to_act_after_hero'])
        assert f['players_to_act_after_hero'] == 0.0

    def test_three_when_oop_in_4way(self):
        f = extract_all_features(
            _multiway_hand('JsTs', 'Jh9c4s', 'BB', 'BTN', 3)
        )
        assert _finite(f['players_to_act_after_hero'])
        assert f['players_to_act_after_hero'] == 3.0


# ─── Feature 2: tpmk_kicker_rank ──────────────────────────────────────

class TestTpmkKickerRank:
    """Numeric kicker rank when hero has top-pair, 0 otherwise.
    Re-pilot 9.18% rank #2/63 (MW-40 breakthrough)."""

    def test_zero_when_no_top_pair(self):
        f = extract_all_features(_hu_hand('AhKs', '8c5d2h'))
        assert _finite(f['tpmk_kicker_rank'])
        assert f['tpmk_kicker_rank'] == 0.0

    def test_returns_kicker_rank_for_top_pair_q_kicker(self):
        f = extract_all_features(_hu_hand('KhQs', 'Kc7d2h'))
        assert _finite(f['tpmk_kicker_rank'])
        assert f['tpmk_kicker_rank'] == 12.0

    def test_returns_kicker_rank_for_top_pair_low_kicker(self):
        f = extract_all_features(_hu_hand('Kh3s', 'Kc7d2h'))
        assert _finite(f['tpmk_kicker_rank'])
        assert f['tpmk_kicker_rank'] == 3.0


# ─── Aggregate: surface size + features populated ─────────────────────

class TestCleanupSurfaceSize61:
    """Phase 2-C cleanup: FEATURE_COLUMNS shrinks 63→61."""

    def test_feature_columns_count_is_61(self):
        from feature_extractor import FEATURE_COLUMNS
        assert len(FEATURE_COLUMNS) == 61

    def test_first_59_match_canonical(self):
        from feature_extractor import FEATURE_COLUMNS
        from inference_path_59 import FEATURE_COLUMNS_59, N_FEATURES_59
        assert tuple(FEATURE_COLUMNS[:N_FEATURES_59]) == FEATURE_COLUMNS_59

    def test_last_2_are_cleanup_features(self):
        from feature_extractor import FEATURE_COLUMNS
        assert tuple(FEATURE_COLUMNS[-2:]) == (
            'players_to_act_after_hero',
            'tpmk_kicker_rank',
        )

    def test_dropped_features_not_in_columns(self):
        """All non-winning pilot features must be absent from surface."""
        from feature_extractor import FEATURE_COLUMNS
        dropped = (
            # PILOT v1 dropped (Option A):
            'multiway_equity_realization_factor',
            'closing_action',
            # PILOT v1 renamed in re-pilot:
            'tpmk_position_with_kicker_strength',
            'broadway_density_completed_on_turn',
            'nut_fd_multiway_pressure_with_blocker',
            # Re-pilot dropped (Option B):
            'broadway_pressure_multiway_facing',
            'nut_fd_blocker_multiway',
        )
        for k in dropped:
            assert k not in FEATURE_COLUMNS, f'dropped feature {k} still in surface'

    def test_both_winners_populated_on_hu_hand(self):
        f = extract_all_features(_hu_hand())
        for k in ('players_to_act_after_hero', 'tpmk_kicker_rank'):
            assert k in f
            assert _finite(f[k]), f'{k}={f[k]} (NaN/Inf)'

    def test_both_winners_populated_on_4way_hand(self):
        f = extract_all_features(
            _multiway_hand('JsTs', 'Jh9c4s', 'BB', 'BTN', 3)
        )
        for k in ('players_to_act_after_hero', 'tpmk_kicker_rank'):
            assert k in f
            assert _finite(f[k]), f'{k}={f[k]} (NaN/Inf)'
