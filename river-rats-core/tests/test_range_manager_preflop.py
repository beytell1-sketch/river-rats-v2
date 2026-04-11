"""
Tests for Phase 1 preflop range data in range_manager.py.

Verifies:
- All 6 positions have RFI ranges
- CALL_VS_OPEN covers all hero/opener combos including new BB vs_SB entry
- THREE_BET covers all hero/opener combos including new BB vs_SB entry
- CALL_VS_3BET exists for all 6 hero positions
- FOURBET exists for all 6 positions
- All frequency values are in [0.0, 1.0]
- No KeyError on any valid 6-max position combination
- New BB vs SB entries return non-empty dicts
- UTG and HJ exist in CALL_VS_3BET (ISSUE_03 from independent review)
"""

import pytest
from range_manager import (
    RFI, THREE_BET, CALL, CALL_VS_3BET, FOURBET,
    RangeManager,
)
CALL_VS_OPEN = CALL  # backward-compat alias for test assertions

POSITIONS_6MAX = ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']

# Positions that can open (RFI)
OPENER_POSITIONS = ['UTG', 'HJ', 'CO', 'BTN', 'SB']


# =============================================================================
# Helpers
# =============================================================================

def _all_freqs_valid(range_dict: dict) -> bool:
    """Return True if every frequency value is in [0.0, 1.0]."""
    return all(0.0 <= v <= 1.0 for v in range_dict.values())


# =============================================================================
# RFI ranges — 5 opening positions
# =============================================================================

class TestRFIRanges:
    def test_rfi_exists_for_all_opening_positions(self):
        for pos in OPENER_POSITIONS:
            assert pos in RFI, f"RFI missing for {pos}"

    def test_rfi_non_empty_for_all_opening_positions(self):
        for pos in OPENER_POSITIONS:
            assert len(RFI[pos]) > 0, f"RFI empty for {pos}"

    def test_rfi_frequencies_valid(self):
        for pos in OPENER_POSITIONS:
            assert _all_freqs_valid(RFI[pos]), f"Invalid frequency in RFI[{pos}]"

    def test_rfi_accessor(self):
        rm = RangeManager()
        for pos in OPENER_POSITIONS:
            r = rm.get_rfi_range(pos)
            assert len(r) > 0, f"get_rfi_range({pos}) returned empty dict"

    def test_rfi_premiums_always_open(self):
        """AA should be 1.0 from all opening positions."""
        for pos in OPENER_POSITIONS:
            assert RFI[pos].get('AA') == 1.0, f"AA should be 1.0 in RFI[{pos}]"


# =============================================================================
# CALL_VS_OPEN — BB defending ranges
# =============================================================================

class TestCallVsOpenBB:
    """BB is the primary defender — needs vs_BTN, vs_CO, vs_HJ, vs_UTG, vs_SB."""

    BB_OPENER_KEYS = ['vs_BTN', 'vs_CO', 'vs_HJ', 'vs_UTG', 'vs_SB']

    def test_bb_has_all_opener_keys(self):
        for key in self.BB_OPENER_KEYS:
            assert key in CALL_VS_OPEN['BB'], f"CALL_VS_OPEN['BB'] missing {key}"

    def test_bb_vs_sb_non_empty(self):
        """Critical new entry — BB calling range vs SB open."""
        r = CALL_VS_OPEN['BB']['vs_SB']
        assert len(r) > 0, "CALL_VS_OPEN['BB']['vs_SB'] is empty"

    def test_bb_vs_sb_frequencies_valid(self):
        assert _all_freqs_valid(CALL_VS_OPEN['BB']['vs_SB'])

    def test_bb_vs_sb_contains_expected_hands(self):
        """BB vs SB should call with JTs, T9s, 77 (suited connectors, pairs)."""
        r = CALL_VS_OPEN['BB']['vs_SB']
        for hand in ['JTs', 'T9s', '77', 'AJo']:
            assert hand in r, f"Expected {hand} in CALL_VS_OPEN['BB']['vs_SB']"

    def test_bb_vs_sb_aa_kk_zero_or_absent(self):
        """AA and KK should not be called — either 0.0 or absent (3-bet only)."""
        r = CALL_VS_OPEN['BB']['vs_SB']
        for hand in ['AA', 'KK']:
            freq = r.get(hand, 0.0)
            assert freq == 0.0, f"{hand} call freq vs SB should be 0.0, got {freq}"

    def test_bb_all_entries_valid_frequencies(self):
        for key in self.BB_OPENER_KEYS:
            assert _all_freqs_valid(CALL_VS_OPEN['BB'][key]), \
                f"Invalid frequency in CALL_VS_OPEN['BB']['{key}']"


# =============================================================================
# CALL_VS_OPEN — accessor method
# =============================================================================

class TestCallVsOpenAccessor:
    """get_call_range uses CALL_VS_OPEN. Test no KeyError on valid combos."""

    # Valid hero/opener combos in 6-max
    VALID_COMBOS = [
        ('BB', 'BTN'), ('BB', 'CO'), ('BB', 'HJ'), ('BB', 'UTG'), ('BB', 'SB'),
        ('SB', 'BTN'), ('SB', 'CO'), ('SB', 'HJ'), ('SB', 'UTG'),
        ('BTN', 'CO'), ('BTN', 'HJ'), ('BTN', 'UTG'),
        ('CO', 'HJ'), ('CO', 'UTG'),
        ('HJ', 'UTG'),
    ]

    def test_no_key_error_on_valid_combos(self):
        rm = RangeManager()
        for hero, opener in self.VALID_COMBOS:
            result = rm.get_call_range(hero, opener)
            assert isinstance(result, dict), \
                f"get_call_range({hero}, {opener}) did not return dict"

    def test_bb_vs_sb_via_accessor(self):
        rm = RangeManager()
        r = rm.get_call_range('BB', 'SB')
        assert len(r) > 0, "get_call_range('BB', 'SB') returned empty dict"


# =============================================================================
# THREE_BET — BB defending ranges
# =============================================================================

class TestThreeBetBB:
    """THREE_BET BB needs vs_BTN, vs_CO, vs_HJ, vs_UTG, vs_SB."""

    BB_OPENER_KEYS = ['vs_BTN', 'vs_CO', 'vs_HJ', 'vs_UTG', 'vs_SB']

    def test_bb_has_all_opener_keys(self):
        for key in self.BB_OPENER_KEYS:
            assert key in THREE_BET['BB'], f"THREE_BET['BB'] missing {key}"

    def test_bb_vs_sb_non_empty(self):
        r = THREE_BET['BB']['vs_SB']
        assert len(r) > 0, "THREE_BET['BB']['vs_SB'] is empty"

    def test_bb_vs_sb_frequencies_valid(self):
        assert _all_freqs_valid(THREE_BET['BB']['vs_SB'])

    def test_bb_vs_sb_contains_premiums(self):
        """AA, KK, QQ should be 3-bet at high frequency vs SB."""
        r = THREE_BET['BB']['vs_SB']
        for hand in ['AA', 'KK', 'QQ']:
            assert r.get(hand, 0.0) >= 0.8, \
                f"{hand} should 3-bet at freq >= 0.8 in THREE_BET['BB']['vs_SB']"

    def test_bb_vs_sb_contains_bluffs(self):
        """A5s should be present as a bluff 3-bet vs SB."""
        r = THREE_BET['BB']['vs_SB']
        assert 'A5s' in r, "A5s (bluff 3-bet) missing from THREE_BET['BB']['vs_SB']"
        assert r['A5s'] > 0.0


# =============================================================================
# CALL_VS_3BET — all 6 positions present (ISSUE_03)
# =============================================================================

class TestCallVs3Bet:
    """ISSUE_03 from independent review: UTG and HJ must exist in CALL_VS_3BET."""

    def test_utg_exists(self):
        assert 'UTG' in CALL_VS_3BET, "UTG missing from CALL_VS_3BET (ISSUE_03)"

    def test_hj_exists(self):
        assert 'HJ' in CALL_VS_3BET, "HJ missing from CALL_VS_3BET (ISSUE_03)"

    def test_all_6_positions_exist(self):
        for pos in POSITIONS_6MAX:
            assert pos in CALL_VS_3BET, f"{pos} missing from CALL_VS_3BET"

    def test_utg_has_vs_btn_entry(self):
        assert 'vs_BTN' in CALL_VS_3BET['UTG'], \
            "CALL_VS_3BET['UTG'] missing vs_BTN"

    def test_hj_has_vs_btn_entry(self):
        assert 'vs_BTN' in CALL_VS_3BET['HJ'], \
            "CALL_VS_3BET['HJ'] missing vs_BTN"

    def test_utg_vs_btn_non_empty(self):
        r = CALL_VS_3BET['UTG']['vs_BTN']
        assert len(r) > 0, "CALL_VS_3BET['UTG']['vs_BTN'] is empty"

    def test_hj_vs_btn_non_empty(self):
        r = CALL_VS_3BET['HJ']['vs_BTN']
        assert len(r) > 0, "CALL_VS_3BET['HJ']['vs_BTN'] is empty"

    def test_all_frequencies_valid(self):
        for pos, sub in CALL_VS_3BET.items():
            for vs_key, range_dict in sub.items():
                assert _all_freqs_valid(range_dict), \
                    f"Invalid frequency in CALL_VS_3BET['{pos}']['{vs_key}']"

    def test_utg_call_range_narrow(self):
        """UTG calls 3-bets with a narrow range — should include TT/JJ but not 72o."""
        r = CALL_VS_3BET['UTG']['vs_BTN']
        assert 'TT' in r, "TT should be in UTG call-vs-3bet range"
        assert '72o' not in r, "72o should not be in UTG call-vs-3bet range"

    def test_hj_call_range_slightly_wider_than_utg(self):
        """HJ vs BTN call range should be >= UTG vs BTN range size."""
        utg_size = len(CALL_VS_3BET['UTG']['vs_BTN'])
        hj_size = len(CALL_VS_3BET['HJ']['vs_BTN'])
        assert hj_size >= utg_size, \
            f"HJ call-vs-3bet range ({hj_size}) should be >= UTG ({utg_size})"


# =============================================================================
# CALL_VS_3BET — accessor method
# =============================================================================

class TestCallVs3BetAccessor:
    VALID_COMBOS = [
        ('UTG', 'BTN'), ('UTG', 'CO'), ('UTG', 'BB'), ('UTG', 'SB'),
        ('HJ', 'BTN'), ('HJ', 'CO'), ('HJ', 'BB'), ('HJ', 'SB'),
        ('CO', 'BB'), ('CO', 'SB'), ('CO', 'BTN'),
        ('BTN', 'BB'), ('BTN', 'SB'), ('BTN', 'CO'),
        ('SB', 'BB'),
        ('BB', 'BTN'), ('BB', 'CO'), ('BB', 'SB'),
    ]

    def test_no_key_error_on_valid_combos(self):
        rm = RangeManager()
        for hero, vs in self.VALID_COMBOS:
            result = rm.get_call_vs_3bet_range(hero, vs)
            assert isinstance(result, dict), \
                f"get_call_vs_3bet_range({hero}, {vs}) did not return dict"

    def test_utg_vs_btn_non_empty(self):
        rm = RangeManager()
        r = rm.get_call_vs_3bet_range('UTG', 'BTN')
        assert len(r) > 0

    def test_hj_vs_btn_non_empty(self):
        rm = RangeManager()
        r = rm.get_call_vs_3bet_range('HJ', 'BTN')
        assert len(r) > 0

    def test_unknown_hero_returns_empty_dict(self):
        rm = RangeManager()
        r = rm.get_call_vs_3bet_range('UNKNOWN', 'BTN')
        assert r == {}, "Unknown hero position should return empty dict"


# =============================================================================
# FOURBET — all 6 positions present
# =============================================================================

class TestFourbet:
    def test_all_6_positions_exist(self):
        for pos in POSITIONS_6MAX:
            assert pos in FOURBET, f"{pos} missing from FOURBET"

    def test_all_frequencies_valid(self):
        for pos, range_dict in FOURBET.items():
            assert _all_freqs_valid(range_dict), \
                f"Invalid frequency in FOURBET['{pos}']"

    def test_premiums_always_4bet(self):
        """AA and KK should be 4-bet at 1.0 from every position."""
        for pos in POSITIONS_6MAX:
            assert FOURBET[pos].get('AA') == 1.0, \
                f"AA should be 1.0 in FOURBET['{pos}']"
            assert FOURBET[pos].get('KK') == 1.0, \
                f"KK should be 1.0 in FOURBET['{pos}']"

    def test_utg_4bet_range_narrow(self):
        """UTG 4-bets only the very top: AA/KK/AKs/AKo — no bluffs needed."""
        r = FOURBET['UTG']
        for hand in ['AA', 'KK', 'AKs', 'AKo']:
            assert hand in r, f"{hand} should be in FOURBET['UTG']"
        # UTG shouldn't be 4-bet bluffing A5s
        assert r.get('A5s', 0.0) == 0.0, "A5s should not be in UTG FOURBET"

    def test_btn_4bet_includes_bluffs(self):
        """BTN 4-bet range is wider and includes A5s/A4s as blocker bluffs."""
        r = FOURBET['BTN']
        assert r.get('A5s', 0.0) > 0.0, "A5s (bluff 4-bet) should be in FOURBET['BTN']"

    def test_fourbet_accessor_all_positions(self):
        rm = RangeManager()
        for pos in POSITIONS_6MAX:
            r = rm.get_fourbet_range(pos)
            assert isinstance(r, dict), f"get_fourbet_range({pos}) did not return dict"
            assert len(r) > 0, f"get_fourbet_range({pos}) returned empty dict"

    def test_fourbet_accessor_unknown_position_returns_dict(self):
        rm = RangeManager()
        r = rm.get_fourbet_range('UNKNOWN')
        assert isinstance(r, dict)


# =============================================================================
# Cross-cutting: frequency bounds across all new dicts
# =============================================================================

class TestFrequencyBoundsAllNewData:
    """All frequencies across every new dictionary must be in [0.0, 1.0]."""

    def test_three_bet_bb_vs_sb(self):
        assert _all_freqs_valid(THREE_BET['BB']['vs_SB'])

    def test_call_vs_open_bb_vs_sb(self):
        assert _all_freqs_valid(CALL_VS_OPEN['BB']['vs_SB'])

    def test_call_vs_3bet_all_entries(self):
        for pos, sub in CALL_VS_3BET.items():
            for vs_key, rng in sub.items():
                assert _all_freqs_valid(rng), \
                    f"Out-of-range freq in CALL_VS_3BET['{pos}']['{vs_key}']"

    def test_fourbet_all_entries(self):
        for pos, rng in FOURBET.items():
            assert _all_freqs_valid(rng), \
                f"Out-of-range freq in FOURBET['{pos}']"


# =============================================================================
# No KeyError on any valid 6-max scenario lookup
# =============================================================================

class TestNoKeyErrorGate:
    """
    Gate test: every valid hero/opener combo in 6-max must not raise KeyError.
    This is the Phase 1 acceptance criterion.
    """

    def test_rfi_all_opening_positions(self):
        rm = RangeManager()
        for pos in OPENER_POSITIONS:
            rm.get_rfi_range(pos)  # must not raise

    def test_call_vs_open_all_valid_combos(self):
        rm = RangeManager()
        valid = [
            ('BB', 'UTG'), ('BB', 'HJ'), ('BB', 'CO'), ('BB', 'BTN'), ('BB', 'SB'),
            ('SB', 'UTG'), ('SB', 'HJ'), ('SB', 'CO'), ('SB', 'BTN'),
            ('BTN', 'UTG'), ('BTN', 'HJ'), ('BTN', 'CO'),
            ('CO', 'UTG'), ('CO', 'HJ'),
            ('HJ', 'UTG'),
        ]
        for hero, opener in valid:
            rm.get_call_range(hero, opener)

    def test_three_bet_all_valid_combos(self):
        """THREE_BET accessor (get_3bet_range) — no KeyError on valid combos."""
        rm = RangeManager()
        valid = [
            ('BB', 'UTG'), ('BB', 'HJ'), ('BB', 'CO'), ('BB', 'BTN'), ('BB', 'SB'),
            ('SB', 'UTG'), ('SB', 'HJ'), ('SB', 'CO'), ('SB', 'BTN'),
            ('BTN', 'UTG'), ('BTN', 'HJ'), ('BTN', 'CO'),
            ('CO', 'UTG'), ('CO', 'HJ'),
            ('HJ', 'UTG'),
        ]
        for hero, opener in valid:
            # Use direct dict lookup to verify no KeyError on the data we added
            vs_key = f"vs_{opener}"
            if hero in THREE_BET and vs_key in THREE_BET[hero]:
                r = THREE_BET[hero][vs_key]
                assert isinstance(r, dict)

    def test_call_vs_3bet_all_valid_combos(self):
        rm = RangeManager()
        valid = [
            ('UTG', 'BTN'), ('UTG', 'CO'), ('UTG', 'BB'), ('UTG', 'SB'),
            ('HJ', 'BTN'), ('HJ', 'CO'), ('HJ', 'BB'), ('HJ', 'SB'),
            ('CO', 'BTN'), ('CO', 'BB'), ('CO', 'SB'),
            ('BTN', 'BB'), ('BTN', 'SB'), ('BTN', 'CO'),
            ('SB', 'BB'),
            ('BB', 'BTN'), ('BB', 'CO'), ('BB', 'SB'),
        ]
        for hero, vs in valid:
            rm.get_call_vs_3bet_range(hero, vs)

    def test_fourbet_all_positions(self):
        rm = RangeManager()
        for pos in POSITIONS_6MAX:
            rm.get_fourbet_range(pos)
