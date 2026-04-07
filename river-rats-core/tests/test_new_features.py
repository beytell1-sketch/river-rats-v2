"""
Unit tests for features 46-48:
  - compute_flush_block_pct   (feature 46)
  - compute_overcard_outs     (feature 47)
  - compute_improvement_probability (feature 48)

Each function is tested independently before integration.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from feature_extractor import (
    compute_flush_block_pct,
    compute_overcard_outs,
    compute_improvement_probability,
    get_villain_range,
    HAND_CATEGORY_ENCODING,
)


# =============================================================================
# Helpers
# =============================================================================

def _parse_board(s: str):
    """'As7c2d' -> ['As', '7c', '2d']"""
    return [s[i:i+2] for i in range(0, len(s), 2)]


def _suit_counts(board_cards):
    """Count suits present in board_cards."""
    counts = {}
    for card in board_cards:
        suit = card[1].lower()
        counts[suit] = counts.get(suit, 0) + 1
    return counts


def _range_for(hero_pos='BTN', villain_pos='BB'):
    """Get a basic villain range for testing."""
    return get_villain_range(hero_pos, villain_pos)


# =============================================================================
# Feature 46: compute_flush_block_pct
# =============================================================================

class TestFlushBlockPct:

    def test_rainbow_board_returns_zero(self):
        """No flush threat on a rainbow board -> 0.0."""
        board = _parse_board('As7c2d')
        suit_counts = _suit_counts(board)
        v_range = _range_for()
        result = compute_flush_block_pct(['Kh', 'Qh'], board, v_range, suit_counts)
        assert result == 0.0, f"Expected 0.0 on rainbow board, got {result}"

    def test_two_tone_hero_one_card_returns_positive(self):
        """Two-tone board, hero has 1 card of flush suit -> positive blocking pct."""
        board = _parse_board('Ah7h2d')   # two hearts on board
        suit_counts = _suit_counts(board)
        # Hero holds Jh (one heart) — blocks heart combos
        v_range = _range_for()
        result = compute_flush_block_pct(['Jh', '9s'], board, v_range, suit_counts)
        assert result > 0.0, f"Expected positive flush_block_pct, got {result}"
        assert result <= 1.0, f"Value must be <= 1.0, got {result}"

    def test_two_tone_hero_two_cards_returns_zero(self):
        """Hero has 2 cards of flush suit -> hero has the draw, not a blocker -> 0.0."""
        board = _parse_board('Ah7h2d')
        suit_counts = _suit_counts(board)
        # Hero holds Jh and Th (two hearts) -> hero is the draw holder
        v_range = _range_for()
        result = compute_flush_block_pct(['Jh', 'Th'], board, v_range, suit_counts)
        assert result == 0.0, (
            f"Hero with 2 flush-suit cards should return 0.0, got {result}"
        )

    def test_monotone_board_hero_one_card_returns_positive(self):
        """Monotone board (3 hearts), hero holds 1 heart -> positive."""
        board = _parse_board('AhKh7h')   # 3 hearts
        suit_counts = _suit_counts(board)
        v_range = _range_for()
        # Hero has Jh — 1 heart, blocking some flush combos
        result = compute_flush_block_pct(['Jh', '9s'], board, v_range, suit_counts)
        assert result > 0.0, f"Expected positive on monotone board, got {result}"
        assert result <= 1.0, f"Value must be <= 1.0, got {result}"

    def test_empty_board_returns_zero(self):
        """Empty board -> no flush threat -> 0.0."""
        result = compute_flush_block_pct(['Ah', 'Kh'], [], {}, {})
        assert result == 0.0

    def test_no_villain_range_returns_zero(self):
        """Empty villain range -> 0.0."""
        board = _parse_board('Ah7h2d')
        suit_counts = _suit_counts(board)
        result = compute_flush_block_pct(['Jh', '9s'], board, {}, suit_counts)
        assert result == 0.0

    def test_result_is_float(self):
        """Return type is always float."""
        board = _parse_board('Ah7h2d')
        suit_counts = _suit_counts(board)
        v_range = _range_for()
        result = compute_flush_block_pct(['Jh', '9s'], board, v_range, suit_counts)
        assert isinstance(result, float), f"Expected float, got {type(result)}"

    def test_result_between_0_and_1(self):
        """Result is always in [0.0, 1.0]."""
        board = _parse_board('Ah7h2h')  # monotone
        suit_counts = _suit_counts(board)
        v_range = _range_for()
        result = compute_flush_block_pct(['Jh', '9s'], board, v_range, suit_counts)
        assert 0.0 <= result <= 1.0, f"Out of bounds: {result}"


# =============================================================================
# Feature 47: compute_overcard_outs
# =============================================================================

class TestOvercardOuts:

    def test_ak_on_742_board(self):
        """AK vs 742 board: both A and K are overcards -> 2 overcards -> 6 outs."""
        # high_card_rank = 7 (the highest board card)
        result = compute_overcard_outs(['Ah', 'Kd'], 7)
        assert result == 6, f"Expected 6, got {result}"

    def test_aq_on_k72_board(self):
        """AQ vs K72 board: only A overcards K (Q does not) -> 3 outs."""
        # high_card_rank = 13 (K)
        result = compute_overcard_outs(['Ah', 'Qd'], 13)
        assert result == 3, f"Expected 3, got {result}"

    def test_55_on_a72_board(self):
        """55 vs A72 board: neither 5 overcards A -> 0 outs."""
        # high_card_rank = 14 (A)
        result = compute_overcard_outs(['5h', '5d'], 14)
        assert result == 0, f"Expected 0, got {result}"

    def test_ace_high_board_always_zero(self):
        """Ace is always the highest rank — nothing overcards it."""
        result = compute_overcard_outs(['Kh', 'Qd'], 14)
        assert result == 0, f"Expected 0, got {result}"

    def test_two_overcards_return_six(self):
        """Two overcards give 6 outs."""
        result = compute_overcard_outs(['Ah', 'Kd'], 9)
        assert result == 6

    def test_one_overcard_returns_three(self):
        """One overcard gives 3 outs."""
        result = compute_overcard_outs(['Ah', '8d'], 9)
        assert result == 3

    def test_no_overcards_returns_zero(self):
        """No overcards gives 0."""
        result = compute_overcard_outs(['7h', '6d'], 9)
        assert result == 0

    def test_exact_rank_not_overcard(self):
        """A card exactly matching high_card_rank does NOT count as an overcard."""
        # high_card_rank = 10 (T board), hero has T — ties, not overcards
        result = compute_overcard_outs(['Th', 'Jd'], 10)
        # J > T, T == T (not strictly above)
        assert result == 3, f"Expected 3 (only J overcards), got {result}"

    def test_return_type_is_int(self):
        result = compute_overcard_outs(['Ah', 'Kd'], 7)
        assert isinstance(result, int), f"Expected int, got {type(result)}"


# =============================================================================
# Feature 48: compute_improvement_probability
# =============================================================================

class TestImprovementProbability:

    def test_river_returns_zero(self):
        """River (5 board cards) -> no unseen cards -> 0.0."""
        board = _parse_board('As7h2dKcJc')
        # hand_category doesn't matter — river check comes first
        result = compute_improvement_probability(['Qh', '9d'], board, 0)
        assert result == 0.0, f"Expected 0.0 on river, got {result}"

    def test_already_two_pair_returns_one(self):
        """Hero already has two-pair -> 1.0."""
        board = _parse_board('As7h2d')
        two_pair_category = HAND_CATEGORY_ENCODING['two_pair']
        result = compute_improvement_probability(['Ah', '7d'], board, two_pair_category)
        assert result == 1.0, f"Expected 1.0 for two-pair, got {result}"

    def test_already_set_returns_one(self):
        """Hero already has a set -> 1.0."""
        board = _parse_board('As7h2d')
        set_category = HAND_CATEGORY_ENCODING['set']
        result = compute_improvement_probability(['Ah', 'Ad'], board, set_category)
        assert result == 1.0, f"Expected 1.0 for set, got {result}"

    def test_flush_draw_on_flop_returns_positive(self):
        """Hero has flush draw on flop -> 9 flush cards improve to flush (flush >= two_pair).
        Should return a positive value (9/47 ~ 0.19)."""
        board = _parse_board('Ah7h2d')   # flop, 2 hearts
        # Hero has two hearts (flush draw)
        # hand_category = overcards or high_card or something below two_pair
        top_pair_category = HAND_CATEGORY_ENCODING['top_pair']
        result = compute_improvement_probability(['Jh', 'Kh'], board, top_pair_category)
        # Should be positive (flush cards improve to flush which is >= two_pair)
        assert result > 0.0, f"Expected positive for flush draw, got {result}"
        assert result <= 1.0, f"Out of bounds: {result}"

    def test_no_draws_no_overcards_low_value(self):
        """Hero has no draws and no connection to board -> low improvement probability."""
        board = _parse_board('As7h2d')   # rainbow dry board
        # Hero has 6-5 offsuit — no straight draw possible, no flush draw,
        # hits nothing on A-7-2
        high_card_category = HAND_CATEGORY_ENCODING['high_card']
        result = compute_improvement_probability(['6h', '5c'], board, high_card_category)
        # Some improvement possible (pair, two-pair), but should be low
        assert 0.0 <= result <= 1.0, f"Out of bounds: {result}"
        # Realistically hero can pair either card (~6 outs / 47 ≈ 0.13),
        # but two-pair would need two specific cards — so overall quite low
        assert result < 0.5, f"Expected low probability for 65o on A72, got {result}"

    def test_result_between_0_and_1(self):
        """Result always in [0.0, 1.0]."""
        board = _parse_board('KsQh2d')
        result = compute_improvement_probability(['Jh', '9c'], board, 0)
        assert 0.0 <= result <= 1.0, f"Out of bounds: {result}"

    def test_return_type_is_float(self):
        board = _parse_board('KsQh2d')
        result = compute_improvement_probability(['Jh', '9c'], board, 0)
        assert isinstance(result, float), f"Expected float, got {type(result)}"

    def test_turn_board_works(self):
        """Turn (4 board cards) -> 0 < result < 1 when there are outs."""
        board = _parse_board('As7h2dKc')   # turn
        top_pair_category = HAND_CATEGORY_ENCODING['top_pair']
        # Hero has AQ — top pair, one overcard Q does nothing to improve to 2-pair+
        # unless a Q hits giving top two pair
        result = compute_improvement_probability(['Ah', 'Qd'], board, top_pair_category)
        # Q hitting gives AQ two-pair
        assert result > 0.0, f"Expected positive on turn with live outs, got {result}"
        assert result <= 1.0, f"Out of bounds: {result}"


# =============================================================================
# Integration smoke test — extract_all_features includes all 3 new features
# =============================================================================

class TestIntegration:

    def _make_hand(self):
        """Minimal hand dict for a flop situation."""
        return {
            'id': 'test_001',
            'pos': 'BTN',
            'vp': 'BB',
            'fb': 0,
            'pot': 10.0,
            'tc': 0.0,
            'st': 'f',
            'h': 'AhKd',
            'b': 'Qs7h2c',
            'exp': 'B',
            '_is_3bet_pot': 0,
            '_villain_aggression_count': 0,
            '_villain_checked_back': 0,
            '_villain_call_count': 0,
        }

    def test_all_three_features_present_in_extract_all(self):
        from feature_extractor import extract_all_features
        hand = self._make_hand()
        features = extract_all_features(hand)
        assert 'flush_block_pct' in features, "flush_block_pct missing"
        assert 'overcard_outs' in features, "overcard_outs missing"
        assert 'improvement_probability' in features, "improvement_probability missing"

    def test_existing_features_unchanged(self):
        """Existing 45 features must be present and correct type."""
        from feature_extractor import extract_all_features, FEATURE_COLUMNS
        hand = self._make_hand()
        features = extract_all_features(hand)
        # All 48 feature columns should be present
        for col in FEATURE_COLUMNS:
            assert col in features, f"Feature '{col}' missing from extract_all_features"

    def test_feature_columns_count(self):
        """FEATURE_COLUMNS should now have 48 entries."""
        from feature_extractor import FEATURE_COLUMNS
        assert len(FEATURE_COLUMNS) == 48, (
            f"Expected 48 feature columns, got {len(FEATURE_COLUMNS)}"
        )

    def test_gto_model_feature_columns_count(self):
        """gto_model.FEATURE_COLUMNS should have 48 entries."""
        from gto_model import FEATURE_COLUMNS as GTO_COLS
        assert len(GTO_COLS) == 48, (
            f"Expected 48 in gto_model.FEATURE_COLUMNS, got {len(GTO_COLS)}"
        )

    def test_new_feature_types(self):
        """flush_block_pct and improvement_probability are float; overcard_outs is int."""
        from feature_extractor import extract_all_features
        hand = self._make_hand()
        features = extract_all_features(hand)
        assert isinstance(features['flush_block_pct'], float)
        assert isinstance(features['overcard_outs'], int)
        assert isinstance(features['improvement_probability'], float)

    def test_new_features_in_range(self):
        """All new features are in their valid ranges."""
        from feature_extractor import extract_all_features
        hand = self._make_hand()
        features = extract_all_features(hand)
        assert 0.0 <= features['flush_block_pct'] <= 1.0
        assert features['overcard_outs'] in (0, 3, 6)
        assert 0.0 <= features['improvement_probability'] <= 1.0
