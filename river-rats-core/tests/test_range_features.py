"""
Tests for Step 8: Range-Board Teaching Features.

These features are _ prefixed metadata for the teaching layer.
They do NOT affect model predictions.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from feature_extractor import extract_range_composition, extract_all_features


# ═══════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════

def _extract(board, hero_pos='BTN', villain_pos='BB', facing_bet=False,
             street='f', is_3bet=0):
    return extract_range_composition(
        board_cards=list(board) if isinstance(board, str) else board,
        hero_pos=hero_pos,
        villain_pos=villain_pos,
        facing_bet=facing_bet,
        street_raw=street,
        is_3bet_pot=is_3bet,
    )


def _parse_board(s):
    """Parse 'As7c2d' into ['As', '7c', '2d']."""
    return [s[i:i+2] for i in range(0, len(s), 2)]


# ═══════════════════════════════════════════════════════════════════
# Feature presence and type
# ═══════════════════════════════════════════════════════════════════

class TestFeaturePresence:

    def test_all_five_features_returned(self):
        r = _extract(_parse_board('As7c2d'))
        assert '_villain_top_pair_plus_pct' in r
        assert '_villain_draw_pct' in r
        assert '_villain_air_pct' in r
        assert '_villain_range_capped' in r
        assert '_board_favour' in r

    def test_features_are_numeric(self):
        r = _extract(_parse_board('As7c2d'))
        assert isinstance(r['_villain_top_pair_plus_pct'], float)
        assert isinstance(r['_villain_draw_pct'], float)
        assert isinstance(r['_villain_air_pct'], float)
        assert isinstance(r['_villain_range_capped'], int)
        assert isinstance(r['_board_favour'], float)

    def test_percentages_between_0_and_1(self):
        r = _extract(_parse_board('As7c2d'))
        for key in ['_villain_top_pair_plus_pct', '_villain_draw_pct', '_villain_air_pct']:
            assert 0.0 <= r[key] <= 1.0, f"{key} = {r[key]}"

    def test_empty_board_returns_defaults(self):
        r = extract_range_composition([], 'BTN', 'BB', False, 'f', 0)
        assert r['_villain_top_pair_plus_pct'] == 0.0
        assert r['_villain_draw_pct'] == 0.0
        assert r['_villain_air_pct'] == 0.0


# ═══════════════════════════════════════════════════════════════════
# Board texture makes poker sense
# ═══════════════════════════════════════════════════════════════════

class TestPokerSense:

    def test_dry_board_has_zero_draws(self):
        """A72 rainbow — no flush draws, no straight draws."""
        r = _extract(_parse_board('As7c2d'))
        assert r['_villain_draw_pct'] == 0.0 or r['_villain_draw_pct'] < 0.05

    def test_dry_board_has_high_air(self):
        """A72 rainbow — most hands miss this board."""
        r = _extract(_parse_board('As7c2d'))
        assert r['_villain_air_pct'] > 0.25

    def test_wet_board_has_draws(self):
        """Ts9s8h — flush draws and straight draws. classify_hand counts
        only 8+ out draws as 'draw' category, so threshold is moderate."""
        r = _extract(_parse_board('Ts9s8h'))
        assert r['_villain_draw_pct'] > 0.08

    def test_broadway_board_has_high_tp_plus(self):
        """KQJ board — many hands in villain's range hit this.

        Threshold is relative to the villain's cold-call range, which is
        intentionally wider post-Phase-B (solver-backed mixed frequencies
        replaced the old tight flat ranges). Wider ranges include more
        weaker made hands and small pairs, which dilutes the top-pair-plus
        percentage slightly even on broadway boards. 0.12 is the floor
        that still captures the directional "broadway boards favour
        villain TP+" claim without being tuned to the old data."""
        r = _extract(_parse_board('KsQdJc'))
        assert r['_villain_top_pair_plus_pct'] > 0.12

    def test_low_board_has_lower_tp_plus(self):
        """742 rainbow — fewer hands in BB's range connect."""
        r = _extract(_parse_board('7s4d2c'))
        assert r['_villain_top_pair_plus_pct'] < r['_villain_air_pct']

    def test_river_draws_become_air(self):
        """On river, draw category reclassifies as air."""
        flop = _extract(_parse_board('Ts9s8h'), street='f')
        river = _extract(_parse_board('Ts9s8h'), street='r')
        # River should have more air (draws reclassified) and zero draws
        assert river['_villain_draw_pct'] == 0.0
        assert river['_villain_air_pct'] > flop['_villain_air_pct']


# ═══════════════════════════════════════════════════════════════════
# Range capped
# ═══════════════════════════════════════════════════════════════════

class TestRangeCapped:

    def test_defender_in_single_raised_pot_is_capped(self):
        """BB defending vs BTN open — no 3-bet premiums."""
        r = _extract(_parse_board('As7c2d'),
                     hero_pos='BTN', villain_pos='BB', is_3bet=0)
        assert r['_villain_range_capped'] == 1

    def test_3bet_pot_not_capped(self):
        """In a 3-bet pot, defender has premiums."""
        r = _extract(_parse_board('As7c2d'),
                     hero_pos='BTN', villain_pos='BB', is_3bet=1)
        assert r['_villain_range_capped'] == 0

    def test_villain_is_pfr_not_capped(self):
        """Villain opened (PFR) — has full range including premiums."""
        r = _extract(_parse_board('As7c2d'),
                     hero_pos='BB', villain_pos='BTN', is_3bet=0)
        assert r['_villain_range_capped'] == 0


# ═══════════════════════════════════════════════════════════════════
# Board favour
# ═══════════════════════════════════════════════════════════════════

class TestBoardFavour:

    def test_board_favour_is_bounded(self):
        r = _extract(_parse_board('As7c2d'))
        assert -1.0 <= r['_board_favour'] <= 1.0

    def test_dry_ace_high_favours_hero_range(self):
        """A-high dry board favours PFR (BTN) range — more Ax combos."""
        r = _extract(_parse_board('As7c2d'),
                     hero_pos='BTN', villain_pos='BB')
        assert r['_board_favour'] > 0  # Positive = favours hero


# ═══════════════════════════════════════════════════════════════════
# Integration: features flow through extract_all_features
# ═══════════════════════════════════════════════════════════════════

class TestIntegration:

    def test_features_in_extract_all(self):
        """Range features appear in full extraction output."""
        hand = {
            'pos': 'BTN', 'h': 'AhKd', 'b': 'As7c2d',
            'st': 'f', 'pot': 30.0, 'fb': 0, 'exp': 'B', 'vp': 'BB',
        }
        feats = extract_all_features(hand)
        assert '_villain_top_pair_plus_pct' in feats
        assert '_villain_draw_pct' in feats
        assert '_villain_air_pct' in feats
        assert '_villain_range_capped' in feats
        assert '_board_favour' in feats

    def test_model_features_unchanged(self):
        """Range features are _ prefixed and do NOT appear in FEATURE_COLUMNS."""
        from gto_model import FEATURE_COLUMNS
        for col in FEATURE_COLUMNS:
            assert not col.startswith('_villain'), f"{col} should not be a model feature"
            assert col != '_board_favour'


# ═══════════════════════════════════════════════════════════════════
# Performance
# ═══════════════════════════════════════════════════════════════════

class TestPerformance:

    def test_under_100ms(self):
        """Range composition should complete in under 100ms per hand."""
        import time
        board = _parse_board('Ts9s8h')
        start = time.time()
        for _ in range(5):
            _extract(board)
        elapsed = (time.time() - start) / 5
        assert elapsed < 0.100, f"Took {elapsed*1000:.0f}ms per hand (budget: 100ms)"
