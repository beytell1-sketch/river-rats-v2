"""Unit tests for Phase 2-B PILOT features (Step 18; 6 features).

Per dispatch PR #392 + design memo PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md:
  - 3 D5 candidates (MW-40/45/47 stay-wrong axes):
      tpmk_position_with_kicker_strength
      broadway_density_completed_on_turn
      nut_fd_multiway_pressure_with_blocker
  - 2 4-way candidates (AMENDMENT 1 + §3.2.2):
      players_to_act_after_hero
      multiway_equity_realization_factor
  - 1 re-raise × players-left candidate (AMENDMENT 2 §3.Y.3 #11):
      closing_action

Tests verify (per dispatch §STOP): non-NaN/Inf numeric scalars + correct
semantic behavior across HU, 3-way, 4-way, and street variants.
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
    """Minimal HU hand_dict."""
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
    """Minimal multiway hand_dict (num_opp=2 → 3-way; =3 → 4-way; etc)."""
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


# ─── Feature 1: tpmk_position_with_kicker_strength (MW-40) ────────────

class TestTpmkPositionWithKickerStrength:
    """Composite: TPMK on J-high board × kicker percentile.

    Per blueprint §3.1: discriminates TPMK with T+ kicker (thin value)
    from TPMK with low kicker (CHECK). 0 elsewhere.
    """

    def test_zero_for_top_set_on_a_high(self):
        # AhKs on Ad8c3h = top pair top kicker (TPTK; hc=8 not in {6,7})
        # → tpmk score should be 0
        f = extract_all_features(_hu_hand('AhKs', 'Ad8c3h'))
        assert _finite(f['tpmk_position_with_kicker_strength'])
        assert f['tpmk_position_with_kicker_strength'] == 0.0

    def test_positive_for_tpmk_on_j_high(self):
        # JsTs on Jh9c4s = top pair with T kicker (TPGK; hc=7) on J-high
        # → tpmk score > 0
        f = extract_all_features(_multiway_hand('JsTs', 'Jh9c4s', 'BB', 'BTN', 3))
        assert _finite(f['tpmk_position_with_kicker_strength'])
        assert f['tpmk_position_with_kicker_strength'] > 0.0

    def test_zero_for_non_j_high_board(self):
        # JsTs on Qh9c4s = no pair (Q-high board, J/T no pair)
        # → tpmk score = 0 (not J-high; also not TPMK)
        f = extract_all_features(_hu_hand('JsTs', 'Qh9c4s'))
        assert _finite(f['tpmk_position_with_kicker_strength'])
        assert f['tpmk_position_with_kicker_strength'] == 0.0


# ─── Feature 2: broadway_density_completed_on_turn (MW-45) ────────────

class TestBroadwayDensityCompletedOnTurn:
    """Count of broadway cards (T/J/Q/K/A) on board AT THE TURN.

    Per blueprint §3.2: discriminates Q+J+T turn (high broadway density;
    multiway pressure) from non-completing turns. Always 0 on flop/river.
    """

    def test_zero_on_flop_even_if_broadway_heavy(self):
        # Flop QJ8 has 2 broadway but street != turn → 0
        f = extract_all_features(_multiway_hand('AsKs', 'QcJh8d', 'CO', 'BTN', 2))
        assert _finite(f['broadway_density_completed_on_turn'])
        assert f['broadway_density_completed_on_turn'] == 0.0

    def test_high_on_qjt_turn(self):
        # Turn Q-J-8-T = 3 broadway on turn → 3.0
        f = extract_all_features(
            _multiway_hand('AsKs', 'QcJh8dTh', 'CO', 'BTN', 2, st='t')
        )
        assert _finite(f['broadway_density_completed_on_turn'])
        assert f['broadway_density_completed_on_turn'] == 3.0

    def test_zero_on_river_even_if_broadway_heavy(self):
        # River QJ8TK = 4 broadway but street == river (not turn) → 0
        f = extract_all_features(
            _multiway_hand('AsKs', 'QcJh8dThKc', 'CO', 'BTN', 2, st='r')
        )
        assert _finite(f['broadway_density_completed_on_turn'])
        assert f['broadway_density_completed_on_turn'] == 0.0


# ─── Feature 3: nut_fd_multiway_pressure_with_blocker (MW-47) ─────────

class TestNutFdMultiwayPressureWithBlocker:
    """Composite: nut FD × nut blocker × multiway × facing bet.

    Per blueprint §3.3: nut FD with blocker on bet-call line should RAISE
    but model predicts CALL. Active only when ALL 4 conditions met.
    """

    def test_zero_in_hu(self):
        # Nut FD on multiway features doesn't activate in HU (multiway=0)
        f = extract_all_features(
            _hu_hand('AsKd', '8s5s2c', pot=15.0, tc=5.0, fb=1)
        )
        assert _finite(f['nut_fd_multiway_pressure_with_blocker'])
        assert f['nut_fd_multiway_pressure_with_blocker'] == 0.0

    def test_zero_without_facing_bet(self):
        # Multiway + nut FD but not facing bet → factor 0
        f = extract_all_features(
            _multiway_hand('AsKd', '8s5s2c', 'BB', 'BTN', 3, fb=0)
        )
        assert _finite(f['nut_fd_multiway_pressure_with_blocker'])
        assert f['nut_fd_multiway_pressure_with_blocker'] == 0.0


# ─── Feature 4: players_to_act_after_hero (AMENDMENT 1) ───────────────

class TestPlayersToActAfterHero:
    """Approximation: 0 if IP, num_opponents if OOP.

    Discriminates EP > MP > LP pressure asymmetry in multiway.
    """

    def test_zero_when_hero_is_ip_hu(self):
        f = extract_all_features(_hu_hand('AhKs', 'Ad8c3h', pos='BTN', vp='BB'))
        assert _finite(f['players_to_act_after_hero'])
        assert f['players_to_act_after_hero'] == 0.0

    def test_three_when_oop_in_4way(self):
        # OOP (BB) in 4-way → 3 villains behind
        f = extract_all_features(
            _multiway_hand('JsTs', 'Jh9c4s', 'BB', 'BTN', 3)
        )
        assert _finite(f['players_to_act_after_hero'])
        assert f['players_to_act_after_hero'] == 3.0


# ─── Feature 5: multiway_equity_realization_factor (§3.2.2) ───────────

class TestMultiwayEquityRealizationFactor:
    """Lookup: HU≈1.0; 3-way≈0.85; 4-way≈0.75; 5+way≈0.70."""

    def test_hu_is_one(self):
        f = extract_all_features(_hu_hand())
        assert _finite(f['multiway_equity_realization_factor'])
        assert f['multiway_equity_realization_factor'] == 1.0

    def test_3way_is_085(self):
        f = extract_all_features(
            _multiway_hand('AsKs', '8c5h2d', 'CO', 'BTN', 2)
        )
        assert _finite(f['multiway_equity_realization_factor'])
        assert f['multiway_equity_realization_factor'] == 0.85

    def test_4way_is_075(self):
        f = extract_all_features(
            _multiway_hand('AsKs', '8c5h2d', 'BB', 'BTN', 3)
        )
        assert _finite(f['multiway_equity_realization_factor'])
        assert f['multiway_equity_realization_factor'] == 0.75

    def test_5way_falls_to_070(self):
        f = extract_all_features(
            _multiway_hand('AsKs', '8c5h2d', 'BB', 'BTN', 4)
        )
        assert _finite(f['multiway_equity_realization_factor'])
        assert f['multiway_equity_realization_factor'] == 0.70


# ─── Feature 6: closing_action (AMENDMENT 2 §3.Y.3 #11) ───────────────

class TestClosingAction:
    """Binary: hero is last to act this street (IP + no players behind)."""

    def test_one_when_hu_ip(self):
        f = extract_all_features(_hu_hand(pos='BTN', vp='BB'))
        assert _finite(f['closing_action'])
        assert f['closing_action'] == 1.0

    def test_zero_when_hu_oop(self):
        f = extract_all_features(_hu_hand(pos='BB', vp='BTN'))
        assert _finite(f['closing_action'])
        assert f['closing_action'] == 0.0

    def test_zero_when_multiway_oop(self):
        # OOP in 4-way → 3 players behind → not closing
        f = extract_all_features(
            _multiway_hand('JsTs', 'Jh9c4s', 'BB', 'BTN', 3)
        )
        assert _finite(f['closing_action'])
        assert f['closing_action'] == 0.0


# ─── Aggregate: surface size + all 6 features populated ───────────────

class TestPilotSurfaceSize65:
    """Phase 2-B PILOT extends FEATURE_COLUMNS from 59 to 65."""

    def test_feature_columns_count_is_65(self):
        from feature_extractor import FEATURE_COLUMNS
        assert len(FEATURE_COLUMNS) == 65

    def test_last_6_are_pilot_features(self):
        from feature_extractor import FEATURE_COLUMNS
        expected_tail = (
            'tpmk_position_with_kicker_strength',
            'broadway_density_completed_on_turn',
            'nut_fd_multiway_pressure_with_blocker',
            'players_to_act_after_hero',
            'multiway_equity_realization_factor',
            'closing_action',
        )
        assert tuple(FEATURE_COLUMNS[-6:]) == expected_tail

    def test_all_6_populated_on_hu_hand(self):
        # Every pilot feature must produce a finite numeric scalar.
        f = extract_all_features(_hu_hand())
        for k in (
            'tpmk_position_with_kicker_strength',
            'broadway_density_completed_on_turn',
            'nut_fd_multiway_pressure_with_blocker',
            'players_to_act_after_hero',
            'multiway_equity_realization_factor',
            'closing_action',
        ):
            assert k in f, f'missing feature {k}'
            assert _finite(f[k]), f'{k}={f[k]} (NaN/Inf)'

    def test_all_6_populated_on_4way_hand(self):
        f = extract_all_features(
            _multiway_hand('JsTs', 'Jh9c4s', 'BB', 'BTN', 3)
        )
        for k in (
            'tpmk_position_with_kicker_strength',
            'broadway_density_completed_on_turn',
            'nut_fd_multiway_pressure_with_blocker',
            'players_to_act_after_hero',
            'multiway_equity_realization_factor',
            'closing_action',
        ):
            assert k in f, f'missing feature {k}'
            assert _finite(f[k]), f'{k}={f[k]} (NaN/Inf)'
