"""
Tests for preflop_engine.py
================================================================================
Covers all five scenarios, confidence clamping, pot odds formula, is_mixed flag,
detect_scenario routing, and implied odds override.

Run with: pytest test_preflop_engine.py -v
"""

import pytest
from range_manager import RangeManager
from preflop_engine import (
    PreflopDecision,
    detect_scenario,
    decide_preflop,
    _compute_pot_odds,
    _implied_odds_override,
    _derive_confidence,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope='module')
def rm():
    return RangeManager()


# ---------------------------------------------------------------------------
# Helper assertions
# ---------------------------------------------------------------------------

def assert_confidence_clamped(decision: PreflopDecision):
    """Confidence must always be in [0.30, 0.95]."""
    assert 0.30 <= decision.confidence <= 0.95, (
        f"Confidence {decision.confidence} outside [0.30, 0.95] "
        f"for hand={decision!r}"
    )


# ---------------------------------------------------------------------------
# 1. RFI scenario
# ---------------------------------------------------------------------------

class TestRFI:
    def test_aa_utg_raises_high_confidence(self, rm):
        """AA from UTG is always in the RFI range — RAISE with near-max confidence."""
        d = decide_preflop('AA', 'UTG', 'rfi', '', 1.5, 0.0, rm)
        assert d.action == 'RAISE'
        assert d.scenario == 'rfi'
        assert d.range_frequency == 1.0
        assert d.confidence == 0.95   # clamped from 1.0
        assert d.is_mixed is False    # 1.0 > 0.8 so not mixed
        assert d.opener_position == ''
        assert_confidence_clamped(d)

    def test_72o_utg_folds_high_confidence(self, rm):
        """72o is not in UTG RFI range — clear fold."""
        d = decide_preflop('72o', 'UTG', 'rfi', '', 1.5, 0.0, rm)
        assert d.action == 'FOLD'
        assert d.scenario == 'rfi'
        assert d.range_frequency == 0.0
        # FOLD confidence = 1.0 - 0.0 = 1.0, clamped to 0.95
        assert d.confidence == 0.95
        assert_confidence_clamped(d)

    def test_rfi_pot_odds_zero(self, rm):
        """RFI has no bet to call — pot_odds_pct and equity_needed must be 0."""
        d = decide_preflop('AKs', 'BTN', 'rfi', '', 1.5, 0.0, rm)
        assert d.pot_odds_pct == 0.0
        assert d.equity_needed == 0.0

    def test_66_utg_is_mixed(self, rm):
        """66 from UTG has freq=0.5 — exactly on the mixed boundary (0.1–0.8)."""
        d = decide_preflop('66', 'UTG', 'rfi', '', 1.5, 0.0, rm)
        # UTG RFI['66'] = 0.5 per range_manager.py
        assert d.range_frequency == 0.5
        assert d.is_mixed is True   # 0.5 is in [0.1, 0.8]
        assert d.action == 'RAISE'  # freq >= 0.5 → RAISE

    def test_55_utg_low_freq_raises_mixed(self, rm):
        """55 from UTG has freq=0.25 — mixed spot, action still RAISE."""
        d = decide_preflop('55', 'UTG', 'rfi', '', 1.5, 0.0, rm)
        assert d.range_frequency == 0.25
        assert d.is_mixed is True
        assert d.action == 'RAISE'   # freq > 0 → RAISE (mixed)

    def test_aks_btn_always_raises(self, rm):
        """AKs from BTN is always in the RFI range."""
        d = decide_preflop('AKs', 'BTN', 'rfi', '', 1.5, 0.0, rm)
        assert d.action == 'RAISE'
        assert d.range_frequency == 1.0
        assert_confidence_clamped(d)


# ---------------------------------------------------------------------------
# 2. DEFEND_CALL scenario
# ---------------------------------------------------------------------------

class TestDefendCall:
    def test_aks_bb_vs_btn_raises_3bet(self, rm):
        """
        AKs from BB facing BTN open — AKs is in the THREE_BET BB vs_BTN range.
        Expect RAISE (3-bet).
        """
        # pot: 2.5 (BTN) + 0.5 (SB) + 1 (BB already posted) = 4.0 before action
        d = decide_preflop('AKs', 'BB', 'defend_call', 'BTN', 4.0, 1.5, rm)
        assert d.action == 'RAISE'
        assert d.scenario == 'defend_call'
        assert d.opener_position == 'BTN'
        assert_confidence_clamped(d)

    def test_t9s_bb_vs_co_calls(self, rm):
        """
        T9s from BB facing CO open.
        T9s freq in CALL_VS_OPEN BB vs_CO = 1.0.
        THREE_BET BB vs_CO does not include T9s (freq 0.0).
        Expect CALL.
        """
        d = decide_preflop('T9s', 'BB', 'defend_call', 'CO', 4.0, 1.5, rm)
        assert d.action == 'CALL'
        assert d.scenario == 'defend_call'
        assert_confidence_clamped(d)

    def test_22_bb_vs_co_calls_implied_odds_or_range(self, rm):
        """
        22 from BB facing CO open.
        22 is in CALL_VS_OPEN BB vs_CO at low freq, or implied odds override fires
        (22 is a small pair, CO is not UTG/HJ).
        Expect CALL.
        """
        d = decide_preflop('22', 'BB', 'defend_call', 'CO', 4.0, 1.5, rm)
        assert d.action == 'CALL'
        assert_confidence_clamped(d)

    def test_tt_bb_vs_co_call_or_raise_mixed(self, rm):
        """
        TT from BB facing CO open.
        CALL_VS_OPEN BB vs_CO has TT at 0.50; THREE_BET BB vs_CO has TT at 0.25.
        THREE_BET fires first (priority) → RAISE mixed.
        If THREE_BET freq is 0, falls to CALL range.
        Either CALL or RAISE is acceptable — just ensure confidence is clamped.
        """
        d = decide_preflop('TT', 'BB', 'defend_call', 'CO', 4.0, 1.5, rm)
        assert d.action in ('CALL', 'RAISE')
        assert_confidence_clamped(d)

    def test_pot_odds_computed_correctly(self, rm):
        """
        pot=5.0, to_call=1.5 → pot_odds = 1.5 / (5.0 + 1.5) * 100 = 23.08%
        """
        d = decide_preflop('T9s', 'BB', 'defend_call', 'BTN', 5.0, 1.5, rm)
        expected = 1.5 / (5.0 + 1.5) * 100
        assert abs(d.pot_odds_pct - expected) < 0.01
        assert abs(d.equity_needed - expected) < 0.01

    def test_pot_odds_standard_formula_not_double_denominator(self, rm):
        """
        Explicitly verify the formula is to_call / (pot + to_call),
        NOT the postflop workaround to_call / (pot + 2 * to_call).
        """
        pot, to_call = 10.0, 4.0
        d = decide_preflop('T9s', 'BB', 'defend_call', 'BTN', pot, to_call, rm)
        correct = to_call / (pot + to_call) * 100          # ~28.57%
        wrong   = to_call / (pot + 2 * to_call) * 100      # ~22.22%
        assert abs(d.pot_odds_pct - correct) < 0.01, (
            f"pot_odds_pct={d.pot_odds_pct:.4f}, expected {correct:.4f} "
            f"(wrong formula would give {wrong:.4f})"
        )

    def test_72o_bb_vs_utg_folds(self, rm):
        """72o is not in any range; no implied odds; should FOLD."""
        d = decide_preflop('72o', 'BB', 'defend_call', 'UTG', 4.0, 1.5, rm)
        assert d.action == 'FOLD'
        assert_confidence_clamped(d)


# ---------------------------------------------------------------------------
# 3. DEFEND_3BET scenario
# ---------------------------------------------------------------------------

class TestDefend3Bet:
    def test_utg_kk_fourbets(self, rm):
        """
        UTG facing a 3-bet with KK — KK is in FOURBET['UTG'].
        Expect RAISE (4-bet).
        """
        d = decide_preflop('KK', 'UTG', 'defend_3bet', 'BTN', 12.0, 5.5, rm)
        assert d.action == 'RAISE'
        assert d.scenario == 'defend_3bet'
        assert_confidence_clamped(d)

    def test_utg_jj_calls_vs_3bet(self, rm):
        """
        UTG facing a 3-bet with JJ.
        JJ is NOT in UTG FOURBET (UTG only 4-bets AA, KK, AKs, AKo).
        JJ IS in CALL_VS_3BET UTG vs_BTN at 0.6 → CALL.
        """
        d = decide_preflop('JJ', 'UTG', 'defend_3bet', 'BTN', 12.0, 5.5, rm)
        assert d.action == 'CALL'
        assert d.scenario == 'defend_3bet'
        assert_confidence_clamped(d)

    def test_utg_72o_folds_vs_3bet(self, rm):
        """72o is not in any 4-bet or call range from UTG. Expect FOLD."""
        d = decide_preflop('72o', 'UTG', 'defend_3bet', 'BTN', 12.0, 5.5, rm)
        assert d.action == 'FOLD'
        assert_confidence_clamped(d)

    def test_defend_3bet_pot_odds(self, rm):
        """pot=12.0, to_call=5.5 → pot_odds = 5.5 / 17.5 * 100 ≈ 31.43%."""
        d = decide_preflop('72o', 'UTG', 'defend_3bet', 'BTN', 12.0, 5.5, rm)
        expected = 5.5 / (12.0 + 5.5) * 100
        assert abs(d.pot_odds_pct - expected) < 0.01

    def test_uses_call_vs_3bet_not_call_vs_open(self, rm):
        """
        Defend_3bet must use CALL_VS_3BET not CALL_VS_OPEN.
        AQs from UTG: in CALL_VS_3BET UTG vs_BTN (0.7) but also could be in other ranges.
        Key: action should be CALL or RAISE depending on which range fires first.
        """
        d = decide_preflop('AQs', 'UTG', 'defend_3bet', 'BTN', 12.0, 5.5, rm)
        # FOURBET UTG does NOT include AQs (UTG only: AA, KK, AKs, AKo)
        # CALL_VS_3BET UTG vs_BTN includes AQs at 0.7 → should CALL
        assert d.action == 'CALL'
        assert d.scenario == 'defend_3bet'


# ---------------------------------------------------------------------------
# 4. SQUEEZE scenario
# ---------------------------------------------------------------------------

class TestSqueeze:
    def test_aks_bb_squeezes(self, rm):
        """AKs from BB with a BTN open and caller — AKs is in THREE_BET BB vs_BTN."""
        d = decide_preflop('AKs', 'BB', 'squeeze', 'BTN', 8.0, 2.5, rm)
        assert d.action == 'RAISE'
        assert d.scenario == 'squeeze'
        assert_confidence_clamped(d)

    def test_72o_bb_folds_squeeze(self, rm):
        """72o from BB vs BTN open — not in any 3-bet range, expect FOLD."""
        d = decide_preflop('72o', 'BB', 'squeeze', 'BTN', 8.0, 2.5, rm)
        assert d.action == 'FOLD'
        assert_confidence_clamped(d)

    def test_aks_sb_squeezes_vs_co(self, rm):
        """AKs from SB vs CO open — in THREEB, should squeeze."""
        d = decide_preflop('AKs', 'SB', 'squeeze', 'CO', 75.0, 25.0, rm)
        assert d.action == 'RAISE'
        assert d.scenario == 'squeeze'

    def test_72o_sb_folds_squeeze(self, rm):
        """72o from SB — not in any range, folds."""
        d = decide_preflop('72o', 'SB', 'squeeze', 'CO', 75.0, 25.0, rm)
        assert d.action == 'FOLD'

    def test_98s_bb_calls_squeeze_vs_co(self, rm):
        """98s from BB vs CO open with caller — in CALL['BB']['vs_CO'], should CALL."""
        d = decide_preflop('98s', 'BB', 'squeeze', 'CO', 75.0, 25.0, rm)
        assert d.action == 'CALL'

    def test_small_pair_folds_vs_tight_opener(self, rm):
        """44 from SB vs UTG — UTG is tight, implied odds override blocked."""
        d = decide_preflop('44', 'SB', 'squeeze', 'UTG', 75.0, 25.0, rm)
        assert d.action == 'FOLD'


# ---------------------------------------------------------------------------
# 4b. SB 3-bet-or-fold policy
# ---------------------------------------------------------------------------

class TestSBIs3BetOrFold:
    def test_jts_sb_folds_vs_co_open(self, rm):
        """
        JTs from SB facing CO open — SB has no CALL range.
        JTs is not in THREE_BET['SB']['vs_CO'] at any meaningful freq.
        Expect FOLD.
        """
        d = decide_preflop('JTs', 'SB', 'squeeze', 'CO', 75.0, 25.0, rm)
        assert d.action == 'FOLD'
        assert d.scenario == 'squeeze'

    def test_kts_sb_folds_vs_co_open(self, rm):
        """
        KTs from SB facing CO open — not in SB 3-bet range, should FOLD.
        """
        d = decide_preflop('KTs', 'SB', 'squeeze', 'CO', 75.0, 25.0, rm)
        assert d.action == 'FOLD'

    def test_small_pair_btn_calls_via_implied_odds_vs_utg(self, rm):
        """
        44 from BTN vs UTG open — BTN has a CALL range.
        44 is in CALL['BTN']['vs_UTG'] at 1.0.
        Implied odds path in engine also fires for BTN (non-SB, non-tight opener check differs).
        Expect CALL.
        (Replaces test_small_pair_calls_via_implied_odds which wrongly used SB hero.)
        """
        d = decide_preflop('44', 'BTN', 'defend_call', 'UTG', 4.0, 1.5, rm)
        assert d.action == 'CALL'
        assert d.scenario == 'defend_call'


# ---------------------------------------------------------------------------
# 5. BB_OPTION scenario
# ---------------------------------------------------------------------------

class TestBBOption:
    def test_weak_hand_checks(self, rm):
        """
        72o is not in BTN RFI range → freq=0.0 < 0.5 → CHECK.
        """
        d = decide_preflop('72o', 'BB', 'bb_option', '', 1.5, 0.0, rm)
        assert d.action == 'CHECK'
        assert d.scenario == 'bb_option'
        assert d.pot_odds_pct == 0.0
        assert d.equity_needed == 0.0
        assert_confidence_clamped(d)

    def test_aa_bb_option_raises(self, rm):
        """
        AA is in BTN RFI at 1.0 → freq >= 0.5 → RAISE (isolation).
        """
        d = decide_preflop('AA', 'BB', 'bb_option', '', 1.5, 0.0, rm)
        assert d.action == 'RAISE'
        assert d.scenario == 'bb_option'
        assert_confidence_clamped(d)

    def test_bb_option_no_pot_odds(self, rm):
        """BB option on unraised pot — no call required, so pot odds = 0."""
        d = decide_preflop('T9s', 'BB', 'bb_option', '', 1.5, 0.0, rm)
        assert d.pot_odds_pct == 0.0
        assert d.equity_needed == 0.0


# ---------------------------------------------------------------------------
# 6. detect_scenario
# ---------------------------------------------------------------------------

class TestDetectScenario:
    def test_no_raise_non_bb_is_rfi(self):
        gs = {
            'num_raises_this_street': 0, 'num_callers': 0,
            'hero_has_raised': False, 'hero_position': 'BTN',
            'to_call': 0, 'opener_position': None,
        }
        assert detect_scenario(gs) == 'rfi'

    def test_no_raise_bb_is_bb_option(self):
        gs = {
            'num_raises_this_street': 0, 'num_callers': 0,
            'hero_has_raised': False, 'hero_position': 'BB',
            'to_call': 0, 'opener_position': None,
        }
        assert detect_scenario(gs) == 'bb_option'

    def test_one_raise_no_callers_is_defend_call(self):
        gs = {
            'num_raises_this_street': 1, 'num_callers': 0,
            'hero_has_raised': False, 'hero_position': 'BB',
            'to_call': 2, 'opener_position': 'BTN',
        }
        assert detect_scenario(gs) == 'defend_call'

    def test_one_raise_with_callers_is_squeeze(self):
        gs = {
            'num_raises_this_street': 1, 'num_callers': 1,
            'hero_has_raised': False, 'hero_position': 'BB',
            'to_call': 2, 'opener_position': 'CO',
        }
        assert detect_scenario(gs) == 'squeeze'

    def test_hero_raised_facing_reraise_is_defend_3bet(self):
        gs = {
            'num_raises_this_street': 2, 'num_callers': 0,
            'hero_has_raised': True, 'hero_position': 'BTN',
            'to_call': 6, 'opener_position': 'BB',
        }
        assert detect_scenario(gs) == 'defend_3bet'

    def test_multiple_callers_still_squeeze(self):
        gs = {
            'num_raises_this_street': 1, 'num_callers': 2,
            'hero_has_raised': False, 'hero_position': 'SB',
            'to_call': 2, 'opener_position': 'CO',
        }
        assert detect_scenario(gs) == 'squeeze'


# ---------------------------------------------------------------------------
# 7. Confidence clamping
# ---------------------------------------------------------------------------

class TestConfidenceClamping:
    def test_fold_confidence_clamped_below(self, rm):
        """
        72o vs UTG open: both range freqs are 0.0.
        FOLD confidence = 1.0 - 0.0 = 1.0, clamped to 0.95.
        """
        d = decide_preflop('72o', 'BB', 'defend_call', 'UTG', 4.0, 1.5, rm)
        assert d.confidence == 0.95

    def test_raise_confidence_clamped_above(self, rm):
        """
        AA vs BTN open from BB: 3-bet freq = 1.0 → confidence = min(1.0, 0.95) = 0.95.
        """
        d = decide_preflop('AA', 'BB', 'defend_call', 'BTN', 4.0, 1.5, rm)
        assert d.confidence == 0.95

    def test_all_scenarios_confidence_clamped(self, rm):
        """Smoke test: every scenario produces clamped confidence."""
        cases = [
            ('AA', 'UTG', 'rfi', '', 1.5, 0.0),
            ('T9s', 'BB', 'defend_call', 'CO', 4.0, 1.5),
            ('KK', 'UTG', 'defend_3bet', 'BTN', 12.0, 5.5),
            ('AKs', 'BB', 'squeeze', 'BTN', 8.0, 2.5),
            ('AA', 'BB', 'bb_option', '', 1.5, 0.0),
        ]
        for hand, pos, scenario, opener, pot, to_call in cases:
            d = decide_preflop(hand, pos, scenario, opener, pot, to_call, rm)
            assert_confidence_clamped(d), f"Clamping failed for {hand} {pos} {scenario}"


# ---------------------------------------------------------------------------
# 8. _derive_confidence unit tests
# ---------------------------------------------------------------------------

class TestDeriveConfidence:
    def test_fold_inverts_frequency(self):
        assert _derive_confidence('FOLD', 0.0, 'rfi') == 0.95   # 1.0 - 0.0 = 1.0 → 0.95
        assert _derive_confidence('FOLD', 0.5, 'rfi') == 0.50   # 1.0 - 0.5 = 0.5

    def test_raise_uses_frequency(self):
        assert _derive_confidence('RAISE', 1.0, 'rfi') == 0.95  # clamped
        assert _derive_confidence('RAISE', 0.4, 'rfi') == 0.40

    def test_call_uses_frequency(self):
        assert _derive_confidence('CALL', 0.7, 'defend_call') == 0.70

    def test_low_frequency_clamped_up(self):
        # RAISE with freq=0.05 → 0.05 clamped to 0.30
        assert _derive_confidence('RAISE', 0.05, 'rfi') == 0.30

    def test_high_fold_confidence_clamped(self):
        # FOLD with freq=0.0 → 1.0 clamped to 0.95
        assert _derive_confidence('FOLD', 0.0, 'rfi') == 0.95


# ---------------------------------------------------------------------------
# 9. _compute_pot_odds unit tests
# ---------------------------------------------------------------------------

class TestComputePotOdds:
    def test_standard_formula(self):
        """to_call / (pot + to_call) * 100"""
        result = _compute_pot_odds(5.0, 2.0)
        expected = 2.0 / (5.0 + 2.0) * 100
        assert abs(result - expected) < 0.001

    def test_zero_to_call_returns_zero(self):
        assert _compute_pot_odds(10.0, 0.0) == 0.0

    def test_bb_vs_sb_open_pot_odds(self):
        """
        Classic spot: BB vs 2.5bb SB open.
        pot_before = 2.5 (SB open) + 1.0 (BB posted) = 3.5
        But SB already put in their 0.5, so pot = 2.5 + 0.5 + 1.0 = 4.0
        to_call = 1.5 (BB already posted 1, must add 1.5 to call 2.5)
        pot_odds = 1.5 / (4.0 + 1.5) * 100 = 27.27%
        """
        result = _compute_pot_odds(4.0, 1.5)
        expected = 1.5 / 5.5 * 100
        assert abs(result - expected) < 0.01

    def test_not_double_denominator(self):
        """Explicitly: formula is NOT to_call / (pot + 2*to_call)."""
        pot, tc = 10.0, 3.0
        correct = _compute_pot_odds(pot, tc)
        wrong = tc / (pot + 2 * tc) * 100
        assert abs(correct - wrong) > 0.5  # The two formulas must differ


# ---------------------------------------------------------------------------
# 10. _implied_odds_override unit tests
# ---------------------------------------------------------------------------

class TestImpliedOddsOverride:
    def test_small_pair_vs_co_triggers(self):
        """22 vs CO open — CO is not UTG/HJ, small pair → True."""
        assert _implied_odds_override('22', 'CO') is True

    def test_small_pair_vs_utg_no_trigger(self):
        """22 vs UTG open — UTG is a tight opener → False."""
        assert _implied_odds_override('22', 'UTG') is False

    def test_small_pair_vs_hj_no_trigger(self):
        """55 vs HJ open — HJ is tight → False."""
        assert _implied_odds_override('55', 'HJ') is False

    def test_suited_connector_vs_btn_triggers(self):
        """87s vs BTN open → True (BTN is loose, 87s is a suited connector)."""
        assert _implied_odds_override('87s', 'BTN') is True

    def test_suited_connector_outside_range_no_trigger(self):
        """T9s is NOT in the eligible suited connector set (54s-98s)."""
        assert _implied_odds_override('T9s', 'BTN') is False

    def test_broadways_not_eligible(self):
        """AKo is not a small pair or suited connector → False."""
        assert _implied_odds_override('AKo', 'BTN') is False


# ---------------------------------------------------------------------------
# 11. PreflopDecision frozen dataclass
# ---------------------------------------------------------------------------

class TestPreflopDecisionDataclass:
    def test_frozen(self):
        """PreflopDecision must be immutable."""
        d = PreflopDecision(
            action='RAISE', confidence=0.9, scenario='rfi', is_mixed=False,
            range_frequency=0.9, pot_odds_pct=0.0, equity_needed=0.0, opener_position=''
        )
        with pytest.raises((AttributeError, TypeError)):
            d.action = 'FOLD'  # type: ignore

    def test_fields_present(self, rm):
        """All required fields exist on a real decision."""
        d = decide_preflop('AKs', 'BTN', 'rfi', '', 0.0, 0.0, rm)
        assert hasattr(d, 'action')
        assert hasattr(d, 'confidence')
        assert hasattr(d, 'scenario')
        assert hasattr(d, 'is_mixed')
        assert hasattr(d, 'range_frequency')
        assert hasattr(d, 'pot_odds_pct')
        assert hasattr(d, 'equity_needed')
        assert hasattr(d, 'opener_position')


# ---------------------------------------------------------------------------
# 12. Invalid scenario raises ValueError
# ---------------------------------------------------------------------------

class TestInvalidScenario:
    def test_unknown_scenario_raises(self, rm):
        with pytest.raises(ValueError, match="Unknown scenario"):
            decide_preflop('AKs', 'BTN', 'unknown_scenario', '', 0.0, 0.0, rm)


# ---------------------------------------------------------------------------
# 13. is_mixed flag
# ---------------------------------------------------------------------------

class TestIsMixed:
    def test_freq_1_not_mixed(self, rm):
        """AA from UTG: freq=1.0 → is_mixed=False (0.1–0.8 range)."""
        d = decide_preflop('AA', 'UTG', 'rfi', '', 1.5, 0.0, rm)
        assert d.is_mixed is False

    def test_freq_0_not_mixed(self, rm):
        """72o from UTG: freq=0.0 → is_mixed=False."""
        d = decide_preflop('72o', 'UTG', 'rfi', '', 1.5, 0.0, rm)
        assert d.is_mixed is False

    def test_mixed_freq_range(self, rm):
        """66 from UTG: freq=0.5 → is_mixed=True."""
        d = decide_preflop('66', 'UTG', 'rfi', '', 1.5, 0.0, rm)
        assert d.is_mixed is True


# ---------------------------------------------------------------------------
# 14. equity_needed == pot_odds_pct invariant
# ---------------------------------------------------------------------------

class TestEquityNeededInvariant:
    def test_equity_needed_equals_pot_odds(self, rm):
        """equity_needed and pot_odds_pct must always be equal."""
        cases = [
            ('T9s', 'BB', 'defend_call', 'CO', 4.0, 1.5),
            ('KK', 'UTG', 'defend_3bet', 'BTN', 12.0, 5.5),
            ('AKs', 'BB', 'squeeze', 'BTN', 8.0, 2.5),
        ]
        for hand, pos, scenario, opener, pot, to_call in cases:
            d = decide_preflop(hand, pos, scenario, opener, pot, to_call, rm)
            assert d.pot_odds_pct == d.equity_needed
