"""
Sprint 4 Tests
===============

D2: Missed-draw river teaching (was_drawing_previous_street)
WI-17: Protect checking range (pending GTO review)
"""
import pytest
from coaching.spot_observation import SpotObservation
from coaching.level_renderer import (
    render_beginner,
    render_intermediate,
    render_advanced,
)


def _build_obs(**overrides) -> SpotObservation:
    defaults = dict(
        action="CHECK",
        strategic_role="pot_control",
        hand_bucket="medium_made",
        hand_description="top pair",
        hand_description_cap="Top pair",
        equity=0.45,
        worse_hand_pct=0.50,
        better_hand_pct=0.50,
        board_texture_label="moderate",
        danger_score=0.4,
        has_draw=False,
        draw_outs=0,
        draw_description="",
        draw_equity=0.0,
        pot_odds_pct=0.0,
        equity_margin=0.0,
        facing_bet=False,
        is_ip=True,
        hero_position="BTN",
        villain_position="BB",
        opponent_phrase="your opponents",
        num_opponents=2,
        is_multiway=True,
    )
    defaults.update(overrides)
    return SpotObservation(**defaults)


# =====================================================================
# D2: Missed-Draw River Teaching
# =====================================================================

class TestD2MissedDrawRiver:
    """
    Trigger: river (street implicit via was_drawing_previous_street)
    AND was_drawing_previous_street == True
    AND action == CHECK
    AND is_multiway
    """

    def _d2_obs(self, **extras) -> SpotObservation:
        kw = dict(
            action="CHECK",
            strategic_role="pot_control",
            hand_bucket="weak_made",
            hand_description="high card",
            hand_description_cap="High card",
            equity=0.12,
            worse_hand_pct=0.15,
            better_hand_pct=0.85,
            facing_bet=False,
            is_ip=False,
            is_multiway=True,
            num_opponents=2,
            was_drawing_previous_street=True,
        )
        kw.update(extras)
        return _build_obs(**kw)

    def test_beginner_mentions_draw_missed(self):
        result = render_beginner(self._d2_obs())
        text = " ".join(result).lower()
        assert "draw" in text and "missed" in text, (
            f"D2 Beginner should mention missed draw: {result}"
        )

    def test_beginner_says_check(self):
        result = render_beginner(self._d2_obs())
        text = " ".join(result).lower()
        assert "check" in text, (
            f"D2 Beginner should recommend checking: {result}"
        )

    def test_intermediate_mentions_bluff_difficulty(self):
        result = render_intermediate(self._d2_obs())
        text = " ".join(result).lower()
        assert "missed" in text or "draw" in text, (
            f"D2 Intermediate should reference missed draw: {result}"
        )
        assert "fold" in text or "all" in text or "bluff" in text, (
            f"D2 Intermediate should mention difficulty of bluffing multiway: {result}"
        )

    def test_advanced_includes_fold_probability(self):
        result = render_advanced(self._d2_obs())
        text = " ".join(result).lower()
        assert "%" in text, (
            f"D2 Advanced should include fold probability math: {result}"
        )

    def test_does_not_fire_when_not_drawing(self):
        """was_drawing_previous_street=False should not trigger D2 language."""
        obs = self._d2_obs(was_drawing_previous_street=False)
        result = render_intermediate(obs)
        text = " ".join(result).lower()
        assert "missed draw" not in text

    def test_does_not_fire_when_not_multiway(self):
        obs = self._d2_obs(is_multiway=False, num_opponents=1,
                           opponent_phrase="your opponent")
        result = render_intermediate(obs)
        text = " ".join(result).lower()
        assert "all opponents" not in text

    def test_does_not_fire_when_action_is_bet(self):
        """D2 only fires on CHECK, not BET."""
        obs = self._d2_obs(action="BET")
        result = render_intermediate(obs)
        text = " ".join(result).lower()
        assert "missed draw" not in text


# =====================================================================
# WI-17: Protect Checking Range (tests added after GTO review)
# =====================================================================

class TestWI17ProtectCheckingRange:
    """
    Trigger: is_multiway AND NOT is_ip AND hand_bucket in (strong_made, monster)
    AND tightness in (CLOSE, TOSS_UP) AND action == BET
    """

    def _wi17_obs(self, **extras) -> SpotObservation:
        kw = dict(
            action="BET",
            strategic_role="value_bet",
            hand_bucket="strong_made",
            hand_description="overpair",
            hand_description_cap="Overpair",
            equity=0.65,
            worse_hand_pct=0.60,
            better_hand_pct=0.40,
            facing_bet=False,
            is_ip=False,
            is_multiway=True,
            num_opponents=2,
            tightness="CLOSE",
            confidence=0.60,
        )
        kw.update(extras)
        return _build_obs(**kw)

    def test_intermediate_mentions_close_spot_and_checking(self):
        result = render_intermediate(self._wi17_obs())
        text = " ".join(result).lower()
        assert "close" in text and "check" in text, (
            f"WI-17 Intermediate should mention close spot and checking: {result}"
        )
        assert "bet" in text and "correct" in text, (
            f"WI-17 Intermediate should frame BET as correct: {result}"
        )

    def test_advanced_mentions_checking_range_and_capped(self):
        result = render_advanced(self._wi17_obs())
        text = " ".join(result).lower()
        assert "check" in text and ("range" in text or "capped" in text), (
            f"WI-17 Advanced should reference checking range or capped range: {result}"
        )

    def test_beginner_does_not_mention_range(self):
        result = render_beginner(self._wi17_obs())
        text = " ".join(result).lower()
        assert "range" not in text
        assert "checking range" not in text

    def test_does_not_fire_when_ip(self):
        obs = self._wi17_obs(is_ip=True)
        result = render_intermediate(obs)
        text = " ".join(result).lower()
        assert "checking range" not in text

    def test_does_not_fire_when_not_close(self):
        obs = self._wi17_obs(tightness="SILENCE", confidence=0.90)
        result = render_intermediate(obs)
        text = " ".join(result).lower()
        assert "checking range" not in text

    def test_does_not_fire_when_weak_hand(self):
        obs = self._wi17_obs(hand_bucket="weak_made")
        result = render_intermediate(obs)
        text = " ".join(result).lower()
        assert "checking range" not in text
