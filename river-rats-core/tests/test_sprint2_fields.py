"""
Sprint 2 Tests — New SpotObservation Fields
=============================================

Tests for the 6 new fields added in Sprint 2:
  WI-1: is_nut_draw
  WI-2: villain_aggression_streets
  WI-3: facing_bet_and_call
  WI-4: facing_check_raise
  WI-5: was_drawing_previous_street
  WI-6: players_behind_count
"""
import pytest
from coaching.observation_builders import (
    _is_nut_draw,
    _was_drawing_previous_street,
    _parse_cards,
)
from coaching.spot_observation import SpotObservation


# =====================================================================
# _parse_cards
# =====================================================================

class TestParseCards:
    def test_hero_cards(self):
        assert _parse_cards("AcKs") == ["Ac", "Ks"]

    def test_board_flop(self):
        assert _parse_cards("Th4c5d") == ["Th", "4c", "5d"]

    def test_board_river(self):
        assert _parse_cards("4s4h3hJh8c") == ["4s", "4h", "3h", "Jh", "8c"]

    def test_empty(self):
        assert _parse_cards("") == []

    def test_single_card(self):
        assert _parse_cards("As") == ["As"]


# =====================================================================
# WI-1: is_nut_draw
# =====================================================================

class TestIsNutDraw:
    def test_nut_flush_draw_ace_of_suit(self):
        # Hero has Ah, board has 2 hearts = nut flush draw
        assert _is_nut_draw("Ah5d", "9h7h4c", True, False) is True

    def test_non_nut_flush_draw_no_ace(self):
        # Hero has Jh, board has 2 hearts = NOT nut flush draw
        assert _is_nut_draw("JhTd", "9h7h4c", True, False) is False

    def test_no_flush_draw(self):
        assert _is_nut_draw("AcKs", "9h7h4c", False, False) is False

    def test_flush_draw_ace_wrong_suit(self):
        # Hero has Ac (clubs), but flush draw is in hearts
        assert _is_nut_draw("AcKs", "9h7h4c", True, False) is False

    def test_empty_cards(self):
        assert _is_nut_draw("", "9h7h4c", True, False) is False
        assert _is_nut_draw("AhKs", "", True, False) is False

    def test_straight_draw_only(self):
        # Straight draw, no flush draw — returns False (nut straight detection not implemented)
        assert _is_nut_draw("9c8c", "7h6d2s", False, True) is False

    def test_combo_draw_with_nut_flush(self):
        # Ah with flush + straight draw
        assert _is_nut_draw("Ah9h", "8h7h6c", True, True) is True

    def test_nut_flush_draw_two_hero_suited(self):
        # Hero has two hearts including Ace, board has 2 hearts (total 4 = flush draw)
        assert _is_nut_draw("AhKh", "9h7h4c", True, False) is True


# =====================================================================
# WI-5: was_drawing_previous_street
# =====================================================================

class TestWasDrawingPreviousStreet:
    def test_river_with_missed_flush_draw(self):
        # Hero: Ah5h, Board: 9h7h4c6s2d (had flush draw on flop/turn, missed on river)
        result = _was_drawing_previous_street("Ah5h", "9h7h4c6s2d", 2.0)
        assert result is True

    def test_river_no_prior_draw(self):
        # Hero: AcKd, Board: 9h7s4c6s2d (no draw on any street)
        result = _was_drawing_previous_street("AcKd", "9h7s4c6s2d", 2.0)
        assert result is False

    def test_not_river(self):
        # Should return False on flop/turn regardless
        assert _was_drawing_previous_street("Ah5h", "9h7h4c", 0.0) is False
        assert _was_drawing_previous_street("Ah5h", "9h7h4c6s", 1.0) is False

    def test_empty_cards(self):
        assert _was_drawing_previous_street("", "9h7h4c6s2d", 2.0) is False
        assert _was_drawing_previous_street("Ah5h", "", 2.0) is False

    def test_river_with_completed_flush(self):
        # Hero: Ah5h, Board: 9h7h4c6h2d (flush completed on turn, was drawing on flop)
        result = _was_drawing_previous_street("Ah5h", "9h7h4c6h2d", 2.0)
        # On the flop (9h7h4c), hero had a flush draw. Should return True.
        assert result is True

    def test_river_straight_draw_missed(self):
        # Hero: 9c8c, Board: 7h6d2sKs3d (had OESD on flop, missed)
        result = _was_drawing_previous_street("9c8c", "7h6d2sKs3d", 2.0)
        assert result is True


# =====================================================================
# SpotObservation defaults
# =====================================================================

class TestSpotObservationDefaults:
    """Verify new fields have safe defaults and don't break existing construction."""

    def test_defaults(self):
        # Minimal construction — all new fields should have safe defaults
        obs = SpotObservation(
            action="CHECK",
            strategic_role="pot_control",
            hand_bucket="medium_made",
            hand_description="top pair",
            hand_description_cap="Top pair",
            equity=0.55,
            worse_hand_pct=0.60,
            better_hand_pct=0.40,
            board_texture_label="dry",
            danger_score=0.2,
            has_draw=False,
            draw_outs=0,
            draw_description="",
            draw_equity=0.0,
            pot_odds_pct=0.0,
            equity_margin=55.0,
            facing_bet=False,
            is_ip=True,
            hero_position="BTN",
            villain_position="BB",
            opponent_phrase="your opponent",
            num_opponents=1,
            is_multiway=False,
        )
        # Sprint 2 fields should all be at defaults
        assert obs.is_nut_draw is False
        assert obs.villain_aggression_streets == 0
        assert obs.facing_bet_and_call is False
        assert obs.facing_check_raise is False
        assert obs.was_drawing_previous_street is False
        assert obs.players_behind_count == 0

    def test_explicit_sprint2_fields(self):
        obs = SpotObservation(
            action="FOLD",
            strategic_role="pot_control",
            hand_bucket="weak_made",
            hand_description="bottom pair",
            hand_description_cap="Bottom pair",
            equity=0.25,
            worse_hand_pct=0.30,
            better_hand_pct=0.70,
            board_texture_label="dangerous",
            danger_score=0.7,
            has_draw=True,
            draw_outs=9,
            draw_description="flush draw",
            draw_equity=0.35,
            pot_odds_pct=33.0,
            equity_margin=-8.0,
            facing_bet=True,
            is_ip=False,
            hero_position="BB",
            villain_position="BTN",
            opponent_phrase="your opponents",
            num_opponents=3,
            is_multiway=True,
            # Sprint 2 fields explicitly set
            is_nut_draw=True,
            villain_aggression_streets=2,
            facing_bet_and_call=True,
            facing_check_raise=False,
            was_drawing_previous_street=True,
            players_behind_count=3,
        )
        assert obs.is_nut_draw is True
        assert obs.villain_aggression_streets == 2
        assert obs.facing_bet_and_call is True
        assert obs.facing_check_raise is False
        assert obs.was_drawing_previous_street is True
        assert obs.players_behind_count == 3
