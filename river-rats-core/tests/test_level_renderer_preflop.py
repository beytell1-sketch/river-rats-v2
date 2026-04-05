"""
test_level_renderer_preflop.py

Tests for the preflop rendering logic in LevelRenderer (Phase 4).

Coverage requirements:
- Each scenario × action combination at each level (Beginner, Intermediate, Advanced)
- At least 30 test cases
- Beginner output must not contain percentage signs
- Advanced output must contain numeric frequencies when preflop_range_frequency is set
- No crash on any valid scenario × action × tightness combination
"""
import re
import pytest
from coaching.spot_observation import SpotObservation
from coaching.level_renderer import render_beginner, render_intermediate, render_advanced, render


# ======================================================================
# FIXTURE HELPERS
# ======================================================================

def _base_kwargs(**overrides):
    """
    Return a minimal valid SpotObservation kwargs dict for preflop spots.
    Tests override what they need.
    """
    defaults = dict(
        action="FOLD",
        strategic_role="range_fold",
        hand_bucket="weak_made",
        hand_description="offsuit connector",
        hand_description_cap="Offsuit connector",
        equity=0.35,
        worse_hand_pct=0.30,
        better_hand_pct=0.70,
        board_texture_label="dry",
        danger_score=0.1,
        has_draw=False,
        draw_outs=0,
        draw_description="",
        draw_equity=0.0,
        pot_odds_pct=33.0,
        equity_margin=-0.05,
        facing_bet=True,
        is_ip=False,
        hero_position="BTN",
        villain_position="CO",
        opponent_phrase="your opponent",
        num_opponents=1,
        is_multiway=False,
        is_counterintuitive=False,
        counterintuitive_reason="",
        tightness="SILENCE",
        confidence=0.75,
        is_preflop=True,
        preflop_scenario="rfi",
        preflop_range_frequency=0.80,
        preflop_opener_position="CO",
        preflop_action_label="fold",
    )
    defaults.update(overrides)
    return defaults


def _obs(**overrides) -> SpotObservation:
    return SpotObservation(**_base_kwargs(**overrides))


# ======================================================================
# HELPERS
# ======================================================================

def has_percentage(text: str) -> bool:
    """Return True if the text contains a percentage character."""
    return "%" in text


def sentences_have_percentage(sentences) -> bool:
    return any(has_percentage(s) for s in sentences)


def sentences_have_number(sentences) -> bool:
    """Return True if any sentence contains a digit (for frequency checks)."""
    return any(re.search(r'\d', s) for s in sentences)


# ======================================================================
# SECTION 1: BEGINNER — no percentages in any scenario
# ======================================================================

class TestBeginnerRFI:
    def test_rfi_raise(self):
        obs = _obs(action="RAISE", preflop_scenario="rfi", hero_position="BTN")
        result = render_beginner(obs)
        assert isinstance(result, list)
        assert len(result) >= 1
        assert all(isinstance(s, str) for s in result)
        assert not sentences_have_percentage(result)
        assert "BTN" in result[0]

    def test_rfi_fold(self):
        obs = _obs(action="FOLD", preflop_scenario="rfi", hero_position="UTG")
        result = render_beginner(obs)
        assert len(result) >= 1
        assert not sentences_have_percentage(result)
        assert "too weak" in result[0].lower() or "weak" in result[0].lower()

    def test_rfi_raise_toss_up_appends_close_decision(self):
        obs = _obs(action="RAISE", preflop_scenario="rfi", tightness="TOSS_UP")
        result = render_beginner(obs)
        assert len(result) == 2
        assert "close" in result[1].lower()
        assert not sentences_have_percentage(result)


class TestBeginnerDefendCall:
    def test_defend_call_call(self):
        obs = _obs(action="CALL", preflop_scenario="defend_call")
        result = render_beginner(obs)
        assert len(result) >= 1
        assert not sentences_have_percentage(result)
        assert "fair price" in result[0].lower() or "call" in result[0].lower()

    def test_defend_call_fold(self):
        obs = _obs(action="FOLD", preflop_scenario="defend_call")
        result = render_beginner(obs)
        assert len(result) >= 1
        assert not sentences_have_percentage(result)
        assert "not worth" in result[0].lower() or "lose" in result[0].lower()

    def test_defend_call_raise(self):
        obs = _obs(action="RAISE", preflop_scenario="defend_call")
        result = render_beginner(obs)
        assert len(result) >= 1
        assert not sentences_have_percentage(result)
        assert "re-raise" in result[0].lower() or "strong" in result[0].lower()


class TestBeginnerDefend3Bet:
    def test_defend_3bet_fold(self):
        obs = _obs(action="FOLD", preflop_scenario="defend_3bet")
        result = render_beginner(obs)
        assert len(result) >= 1
        assert not sentences_have_percentage(result)
        assert "re-raise" in result[0].lower() or "weak" in result[0].lower()

    def test_defend_3bet_raise(self):
        obs = _obs(action="RAISE", preflop_scenario="defend_3bet")
        result = render_beginner(obs)
        assert len(result) >= 1
        assert not sentences_have_percentage(result)
        assert "strong" in result[0].lower() or "re-raise" in result[0].lower()

    def test_defend_3bet_call(self):
        obs = _obs(action="CALL", preflop_scenario="defend_3bet")
        result = render_beginner(obs)
        assert len(result) >= 1
        assert not sentences_have_percentage(result)
        assert "worth" in result[0].lower() or "continuing" in result[0].lower()


class TestBeginnerBBOption:
    def test_bb_option_check(self):
        obs = _obs(action="CHECK", preflop_scenario="bb_option", hero_position="BB")
        result = render_beginner(obs)
        assert len(result) >= 1
        assert not sentences_have_percentage(result)
        assert "free" in result[0].lower() or "check" in result[0].lower()

    def test_bb_option_raise(self):
        obs = _obs(action="RAISE", preflop_scenario="bb_option", hero_position="BB")
        result = render_beginner(obs)
        assert len(result) >= 1
        assert not sentences_have_percentage(result)
        assert "strong" in result[0].lower() or "raise" in result[0].lower()


class TestBeginnerSqueeze:
    def test_squeeze_raise(self):
        obs = _obs(action="RAISE", preflop_scenario="squeeze")
        result = render_beginner(obs)
        assert len(result) >= 1
        assert not sentences_have_percentage(result)
        assert "squeeze" in result[0].lower() or "strong" in result[0].lower()

    def test_squeeze_fold(self):
        obs = _obs(action="FOLD", preflop_scenario="squeeze")
        result = render_beginner(obs)
        assert len(result) >= 1
        assert not sentences_have_percentage(result)
        assert "fold" in result[0].lower() or "not strong" in result[0].lower()

    def test_squeeze_toss_up_two_sentences(self):
        obs = _obs(action="RAISE", preflop_scenario="squeeze", tightness="TOSS_UP")
        result = render_beginner(obs)
        assert len(result) == 2
        assert not sentences_have_percentage(result)


# ======================================================================
# SECTION 2: INTERMEDIATE — contains position info and (for calling
# scenarios) pot odds percentages
# ======================================================================

class TestIntermediateRFI:
    def test_rfi_raise_includes_range_pct(self):
        obs = _obs(action="RAISE", preflop_scenario="rfi", hero_position="BTN")
        result = render_intermediate(obs)
        assert len(result) >= 1
        combined = " ".join(result)
        # Should mention the 44% BTN opening range
        assert "44" in combined
        assert "BTN" in combined

    def test_rfi_fold_mentions_outside_range(self):
        obs = _obs(action="FOLD", preflop_scenario="rfi", hero_position="UTG")
        result = render_intermediate(obs)
        combined = " ".join(result)
        assert "13" in combined  # UTG = 13%
        assert "outside" in combined.lower() or "range" in combined.lower()

    def test_rfi_toss_up_mentions_gto_mixes(self):
        obs = _obs(action="RAISE", preflop_scenario="rfi",
                   hero_position="CO", tightness="TOSS_UP")
        result = render_intermediate(obs)
        combined = " ".join(result).lower()
        assert "gto mixes" in combined or "borderline" in combined


class TestIntermediateDefendCall:
    def test_defend_call_call_shows_pot_odds(self):
        obs = _obs(action="CALL", preflop_scenario="defend_call",
                   pot_odds_pct=33.0, preflop_opener_position="CO")
        result = render_intermediate(obs)
        combined = " ".join(result)
        assert "33" in combined  # pot odds shown at Intermediate
        assert "CO" in combined

    def test_defend_call_fold_shows_pot_odds(self):
        obs = _obs(action="FOLD", preflop_scenario="defend_call",
                   pot_odds_pct=41.0, preflop_opener_position="UTG")
        result = render_intermediate(obs)
        combined = " ".join(result)
        assert "41" in combined

    def test_defend_call_raise_mentions_3bet(self):
        obs = _obs(action="RAISE", preflop_scenario="defend_call",
                   hero_position="BTN")
        result = render_intermediate(obs)
        combined = " ".join(result).lower()
        assert "3-bet" in combined or "re-raise" in combined


class TestIntermediateDefend3Bet:
    def test_defend_3bet_fold_mentions_equity(self):
        obs = _obs(action="FOLD", preflop_scenario="defend_3bet", pot_odds_pct=31.0)
        result = render_intermediate(obs)
        combined = " ".join(result)
        assert "31" in combined

    def test_defend_3bet_raise(self):
        obs = _obs(action="RAISE", preflop_scenario="defend_3bet",
                   hero_position="BTN")
        result = render_intermediate(obs)
        combined = " ".join(result).lower()
        assert "4-bet" in combined or "pressure" in combined

    def test_defend_3bet_call_shows_pot_odds(self):
        obs = _obs(action="CALL", preflop_scenario="defend_3bet", pot_odds_pct=31.0)
        result = render_intermediate(obs)
        combined = " ".join(result)
        assert "31" in combined


class TestIntermediateBBOption:
    def test_bb_option_check(self):
        obs = _obs(action="CHECK", preflop_scenario="bb_option", hero_position="BB")
        result = render_intermediate(obs)
        combined = " ".join(result).lower()
        assert "free" in combined or "big blind" in combined or "check" in combined

    def test_bb_option_raise_mentions_isolate(self):
        obs = _obs(action="RAISE", preflop_scenario="bb_option")
        result = render_intermediate(obs)
        combined = " ".join(result).lower()
        assert "isolate" in combined or "heads-up" in combined


class TestIntermediateSqueeze:
    def test_squeeze_raise_mentions_fold_equity(self):
        obs = _obs(action="RAISE", preflop_scenario="squeeze",
                   preflop_opener_position="UTG")
        result = render_intermediate(obs)
        combined = " ".join(result).lower()
        assert "fold equity" in combined or "squeeze" in combined

    def test_squeeze_fold(self):
        obs = _obs(action="FOLD", preflop_scenario="squeeze")
        result = render_intermediate(obs)
        assert len(result) >= 1


# ======================================================================
# SECTION 3: ADVANCED — must contain numeric frequencies
# ======================================================================

class TestAdvancedRFI:
    def test_rfi_raise_contains_frequency(self):
        obs = _obs(action="RAISE", preflop_scenario="rfi",
                   hero_position="BTN", preflop_range_frequency=0.85)
        result = render_advanced(obs)
        combined = " ".join(result)
        # 0.85 * 100 = 85 → should appear as "85"
        assert "85" in combined

    def test_rfi_fold_contains_frequency(self):
        obs = _obs(action="FOLD", preflop_scenario="rfi",
                   hero_position="CO", preflop_range_frequency=0.10)
        result = render_advanced(obs)
        combined = " ".join(result)
        assert "10" in combined  # 10% shown

    def test_rfi_raise_contains_range_pct(self):
        obs = _obs(action="RAISE", preflop_scenario="rfi",
                   hero_position="UTG", preflop_range_frequency=1.0)
        result = render_advanced(obs)
        combined = " ".join(result)
        assert "13" in combined  # UTG opens 13%


class TestAdvancedDefendCall:
    def test_defend_call_call_shows_pot_odds_and_freq(self):
        obs = _obs(action="CALL", preflop_scenario="defend_call",
                   pot_odds_pct=33.0, preflop_range_frequency=0.75,
                   preflop_opener_position="BTN")
        result = render_advanced(obs)
        combined = " ".join(result)
        assert "33" in combined   # pot odds
        assert "75" in combined   # 75% call frequency

    def test_defend_call_fold_shows_pot_odds(self):
        obs = _obs(action="FOLD", preflop_scenario="defend_call",
                   pot_odds_pct=41.0, preflop_range_frequency=0.0,
                   preflop_opener_position="UTG")
        result = render_advanced(obs)
        combined = " ".join(result)
        assert "41" in combined

    def test_defend_call_raise_shows_3bet_freq(self):
        obs = _obs(action="RAISE", preflop_scenario="defend_call",
                   preflop_range_frequency=0.60, preflop_opener_position="CO")
        result = render_advanced(obs)
        combined = " ".join(result)
        assert "60" in combined  # 3-bet frequency


class TestAdvancedDefend3Bet:
    def test_defend_3bet_fold_shows_pot_odds(self):
        obs = _obs(action="FOLD", preflop_scenario="defend_3bet",
                   pot_odds_pct=31.0, preflop_range_frequency=0.0)
        result = render_advanced(obs)
        combined = " ".join(result)
        assert "31" in combined

    def test_defend_3bet_raise_shows_4bet_freq(self):
        obs = _obs(action="RAISE", preflop_scenario="defend_3bet",
                   preflop_range_frequency=0.90, pot_odds_pct=31.0)
        result = render_advanced(obs)
        combined = " ".join(result)
        assert "90" in combined

    def test_defend_3bet_call_shows_both(self):
        obs = _obs(action="CALL", preflop_scenario="defend_3bet",
                   pot_odds_pct=31.0, preflop_range_frequency=0.70)
        result = render_advanced(obs)
        combined = " ".join(result)
        assert "31" in combined
        assert "70" in combined


class TestAdvancedBBOption:
    def test_bb_option_check_shows_freq(self):
        obs = _obs(action="CHECK", preflop_scenario="bb_option",
                   hero_position="BB", preflop_range_frequency=0.20)
        result = render_advanced(obs)
        combined = " ".join(result)
        assert "20" in combined

    def test_bb_option_raise_shows_freq(self):
        obs = _obs(action="RAISE", preflop_scenario="bb_option",
                   hero_position="BB", preflop_range_frequency=0.55)
        result = render_advanced(obs)
        combined = " ".join(result)
        assert "55" in combined


class TestAdvancedSqueeze:
    def test_squeeze_raise_shows_freq(self):
        obs = _obs(action="RAISE", preflop_scenario="squeeze",
                   preflop_range_frequency=0.65, preflop_opener_position="BTN")
        result = render_advanced(obs)
        combined = " ".join(result)
        assert "65" in combined

    def test_squeeze_fold_shows_pot_odds(self):
        obs = _obs(action="FOLD", preflop_scenario="squeeze",
                   pot_odds_pct=28.0, preflop_range_frequency=0.0)
        result = render_advanced(obs)
        combined = " ".join(result)
        assert "28" in combined


# ======================================================================
# SECTION 4: Mixed-spot rendering across levels
# ======================================================================

class TestMixedSpots:
    def test_beginner_toss_up_two_sentences(self):
        obs = _obs(action="CALL", preflop_scenario="defend_call", tightness="TOSS_UP")
        result = render_beginner(obs)
        assert len(result) == 2
        assert "close" in result[1].lower()
        assert not sentences_have_percentage(result)

    def test_intermediate_toss_up_mentions_gto_mix(self):
        obs = _obs(action="FOLD", preflop_scenario="rfi",
                   hero_position="BTN", tightness="TOSS_UP")
        result = render_intermediate(obs)
        combined = " ".join(result).lower()
        assert "gto mixes" in combined or "borderline" in combined

    def test_intermediate_close_mentions_also_reasonable(self):
        obs = _obs(action="RAISE", preflop_scenario="rfi",
                   hero_position="CO", tightness="CLOSE")
        result = render_intermediate(obs)
        combined = " ".join(result).lower()
        assert "reasonable" in combined

    def test_advanced_toss_up_mentions_mixed_strategy(self):
        obs = _obs(action="CALL", preflop_scenario="defend_call",
                   tightness="TOSS_UP", preflop_range_frequency=0.40)
        result = render_advanced(obs)
        combined = " ".join(result).lower()
        assert "mixed" in combined

    def test_advanced_close_mentions_close_decision(self):
        obs = _obs(action="RAISE", preflop_scenario="rfi",
                   hero_position="BTN", tightness="CLOSE",
                   preflop_range_frequency=0.70)
        result = render_advanced(obs)
        combined = " ".join(result).lower()
        assert "close" in combined


# ======================================================================
# SECTION 5: render() dispatcher routes correctly
# ======================================================================

class TestDispatcher:
    def test_level_0_routes_to_beginner(self):
        obs = _obs(action="RAISE", preflop_scenario="rfi", hero_position="BTN")
        result = render(obs, 0)
        # Beginner output: no percentages
        assert not sentences_have_percentage(result)

    def test_level_1_routes_to_intermediate(self):
        obs = _obs(action="RAISE", preflop_scenario="rfi",
                   hero_position="BTN", preflop_range_frequency=0.9)
        result = render(obs, 1)
        # Intermediate includes position range pct
        combined = " ".join(result)
        assert "44" in combined  # BTN 44%

    def test_level_2_routes_to_advanced(self):
        obs = _obs(action="RAISE", preflop_scenario="rfi",
                   hero_position="BTN", preflop_range_frequency=0.90)
        result = render(obs, 2)
        # Advanced includes hand frequency "90"
        combined = " ".join(result)
        assert "90" in combined

    def test_level_3_also_routes_to_advanced(self):
        obs = _obs(action="FOLD", preflop_scenario="rfi",
                   hero_position="UTG", preflop_range_frequency=0.05)
        result = render(obs, 3)
        assert isinstance(result, list)
        assert len(result) >= 1


# ======================================================================
# SECTION 6: No crash on all valid combinations
# ======================================================================

_SCENARIOS = ["rfi", "defend_call", "defend_3bet", "bb_option", "squeeze"]
_ACTIONS = ["FOLD", "CALL", "RAISE", "CHECK"]
_TIGHTNESS = ["SILENCE", "CLOSE", "TOSS_UP"]
_LEVELS = [0, 1, 2]


@pytest.mark.parametrize("scenario", _SCENARIOS)
@pytest.mark.parametrize("action", _ACTIONS)
@pytest.mark.parametrize("tightness", _TIGHTNESS)
@pytest.mark.parametrize("level", _LEVELS)
def test_no_crash_all_combinations(scenario, action, tightness, level):
    """No scenario × action × tightness × level combination should raise an exception."""
    obs = _obs(
        action=action,
        preflop_scenario=scenario,
        tightness=tightness,
        hero_position="BTN",
        preflop_range_frequency=0.50,
        pot_odds_pct=33.0,
        preflop_opener_position="CO",
    )
    result = render(obs, level)
    assert isinstance(result, list)
    assert len(result) >= 1
    assert all(isinstance(s, str) and len(s) > 0 for s in result)
