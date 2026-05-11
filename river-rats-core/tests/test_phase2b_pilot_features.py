"""Unit tests for Phase 2-B RE-PILOT features (Step 18; 4 features).

Per dispatch PR #396 (owner-ratified Option A; supersedes PR #392):
  1. players_to_act_after_hero       — KEEP unchanged from PILOT v1
  2. tpmk_kicker_rank                — RE-ENGINEERED (numeric kicker)
  3. broadway_pressure_multiway_facing — RE-ENGINEERED (composite at boundary)
  4. nut_fd_blocker_multiway         — RE-ENGINEERED (no facing_bet gate)

Dropped from PILOT v1 (collinear with baseline):
  - multiway_equity_realization_factor (perfect collinearity with num_opponents)
  - closing_action (near-perfect collinearity with is_ip + players_to_act)
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


# ─── Feature 1: players_to_act_after_hero (KEEP from PILOT v1) ────────

class TestPlayersToActAfterHero:
    """0 if IP, num_opponents if OOP. PILOT v1: 3.58% importance, rank #10/65."""

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


# ─── Feature 2: tpmk_kicker_rank (RE-ENGINEERED MW-40) ────────────────

class TestTpmkKickerRank:
    """Numeric kicker rank when hero has top-pair, 0 otherwise.

    Re-engineered from v1 tpmk_position_with_kicker_strength (0.00%).
    """

    def test_zero_when_no_top_pair(self):
        # AhKs on 8c5d2h — no top pair (high_card=8; hero has no 8)
        f = extract_all_features(_hu_hand('AhKs', '8c5d2h'))
        assert _finite(f['tpmk_kicker_rank'])
        assert f['tpmk_kicker_rank'] == 0.0

    def test_returns_kicker_rank_for_top_pair_q_kicker(self):
        # KhQs on Kc7d2h — top pair K's with Q kicker. Expect 12.
        f = extract_all_features(_hu_hand('KhQs', 'Kc7d2h'))
        assert _finite(f['tpmk_kicker_rank'])
        assert f['tpmk_kicker_rank'] == 12.0

    def test_returns_kicker_rank_for_top_pair_low_kicker(self):
        # Kh3s on Kc7d2h — top pair K's with 3 kicker. Expect 3.
        f = extract_all_features(_hu_hand('Kh3s', 'Kc7d2h'))
        assert _finite(f['tpmk_kicker_rank'])
        assert f['tpmk_kicker_rank'] == 3.0


# ─── Feature 3: broadway_pressure_multiway_facing (RE-ENGINEERED MW-45) ─

class TestBroadwayPressureMultiwayFacing:
    """broadway_count_on_turn × multiway × facing_bet.

    Re-engineered from v1 broadway_density_completed_on_turn (0.00%).
    """

    def test_zero_in_hu_even_on_broadway_turn(self):
        # HU + Q-J-8-T turn; multiway=0 → 0
        f = extract_all_features(
            _hu_hand('AsKs', 'QcJh8dTh', st='t', tc=5.0, fb=1)
        )
        assert _finite(f['broadway_pressure_multiway_facing'])
        assert f['broadway_pressure_multiway_facing'] == 0.0

    def test_zero_without_facing_bet(self):
        # Multiway + broadway turn but not facing bet → 0
        f = extract_all_features(
            _multiway_hand('AsKs', 'QcJh8dTh', 'CO', 'BTN', 2, st='t', fb=0)
        )
        assert _finite(f['broadway_pressure_multiway_facing'])
        assert f['broadway_pressure_multiway_facing'] == 0.0

    def test_high_on_broadway_turn_multiway_facing(self):
        # Multiway + Q-J-8-T turn (broadway=3) + facing bet → 3.0
        f = extract_all_features(
            _multiway_hand('AsKs', 'QcJh8dTh', 'CO', 'BTN', 2,
                           st='t', tc=5.0, fb=1)
        )
        assert _finite(f['broadway_pressure_multiway_facing'])
        assert f['broadway_pressure_multiway_facing'] == 3.0

    def test_zero_on_flop_even_if_multiway_broadway_facing(self):
        f = extract_all_features(
            _multiway_hand('AsKs', 'QcJh8d', 'CO', 'BTN', 2,
                           st='f', tc=5.0, fb=1)
        )
        assert _finite(f['broadway_pressure_multiway_facing'])
        assert f['broadway_pressure_multiway_facing'] == 0.0


# ─── Feature 4: nut_fd_blocker_multiway (RE-ENGINEERED MW-47) ─────────

class TestNutFdBlockerMultiway:
    """has_FD × nut_block × multiway (no facing_bet gate).

    Re-engineered from v1 nut_fd_multiway_pressure_with_blocker (1.53%).
    """

    def test_zero_in_hu(self):
        # AsKs on 8s5s2c HU = nut FD + nut blocker but HU (multiway=0) → 0
        f = extract_all_features(
            _hu_hand('AsKs', '8s5s2c', pot=15.0, tc=5.0, fb=1)
        )
        assert _finite(f['nut_fd_blocker_multiway'])
        assert f['nut_fd_blocker_multiway'] == 0.0

    def test_active_in_multiway_check_spot(self):
        # Multiway + nut FD (AsKs+8s5s = 4 spades) + nut blocker (As) +
        # NOT facing bet — v1 would have been 0 (facing_bet gate); v2 > 0.
        f = extract_all_features(
            _multiway_hand('AsKs', '8s5s2c', 'BB', 'BTN', 3, fb=0)
        )
        assert _finite(f['nut_fd_blocker_multiway'])
        assert f['nut_fd_blocker_multiway'] == 1.0


# ─── Aggregate: surface size + all 4 features populated ───────────────

class TestRepilotSurfaceSize63:
    """Phase 2-B RE-PILOT extends FEATURE_COLUMNS from 59 to 63."""

    def test_feature_columns_count_is_63(self):
        from feature_extractor import FEATURE_COLUMNS
        assert len(FEATURE_COLUMNS) == 63

    def test_first_59_match_canonical(self):
        from feature_extractor import FEATURE_COLUMNS
        from inference_path_59 import FEATURE_COLUMNS_59, N_FEATURES_59
        assert tuple(FEATURE_COLUMNS[:N_FEATURES_59]) == FEATURE_COLUMNS_59

    def test_last_4_are_repilot_features(self):
        from feature_extractor import FEATURE_COLUMNS
        expected_tail = (
            'players_to_act_after_hero',
            'tpmk_kicker_rank',
            'broadway_pressure_multiway_facing',
            'nut_fd_blocker_multiway',
        )
        assert tuple(FEATURE_COLUMNS[-4:]) == expected_tail

    def test_dropped_features_not_in_columns(self):
        from feature_extractor import FEATURE_COLUMNS
        dropped = (
            'multiway_equity_realization_factor',
            'closing_action',
            'tpmk_position_with_kicker_strength',
            'broadway_density_completed_on_turn',
            'nut_fd_multiway_pressure_with_blocker',
        )
        for k in dropped:
            assert k not in FEATURE_COLUMNS, f'dropped feature {k} still in surface'

    def test_all_4_populated_on_hu_hand(self):
        f = extract_all_features(_hu_hand())
        for k in (
            'players_to_act_after_hero',
            'tpmk_kicker_rank',
            'broadway_pressure_multiway_facing',
            'nut_fd_blocker_multiway',
        ):
            assert k in f
            assert _finite(f[k]), f'{k}={f[k]} (NaN/Inf)'

    def test_all_4_populated_on_4way_hand(self):
        f = extract_all_features(
            _multiway_hand('JsTs', 'Jh9c4s', 'BB', 'BTN', 3)
        )
        for k in (
            'players_to_act_after_hero',
            'tpmk_kicker_rank',
            'broadway_pressure_multiway_facing',
            'nut_fd_blocker_multiway',
        ):
            assert k in f
            assert _finite(f[k]), f'{k}={f[k]} (NaN/Inf)'
