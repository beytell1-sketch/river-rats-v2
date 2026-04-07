"""
Preflop Decision Engine
================================================================================
Replaces the Monte Carlo + arbitrary-threshold preflop system with a clean
range-table lookup engine.

Design doc: design/preflop_system_design.md
Author: Lead Programmer (Phase 2)
Date: 2026-04-01

Core principle: range-table lookups drive every decision. No equity simulation.

Scenarios handled:
    rfi         — Raise First In (no prior action)
    defend_call — Facing one open, hero decides call / 3-bet / fold
    defend_3bet — Hero raised, now facing a re-raise; decides 4-bet / call / fold
    squeeze     — Open + caller(s) in front; hero can 3-bet over both
    bb_option   — Unraised pot, BB has the option to raise or check

Confidence contract:
    FOLD  → confidence = 1.0 - range_frequency  (how sure we are to fold)
    Else  → confidence = range_frequency         (how strongly GTO fires)
    Clamped to [0.30, 0.95] — we never show 0% or 100% certainty to students.

Pot odds formula: to_call / (pot + to_call) * 100
  This is the standard break-even equity formula. See design doc section 1.3.
  The to_call / (pot + 2*to_call) variant is a postflop pipeline workaround —
  it must NOT be used here.
"""

from dataclasses import dataclass
from typing import Optional

from range_manager import RangeManager


# ---------------------------------------------------------------------------
# Hand classification helpers (used for implied-odds override)
# ---------------------------------------------------------------------------

# Small pairs eligible for implied odds calls at 100bb
_SMALL_PAIRS = {'22', '33', '44', '55'}

# Suited connectors eligible for implied odds calls at 100bb (54s–98s)
_SUITED_CONNECTORS_IMPLIED = {'54s', '65s', '76s', '87s', '98s'}

# Positions where the opener's range is tight enough to kill implied odds
_TIGHT_OPENER_POSITIONS = {'UTG', 'HJ', 'EP', 'MP'}

# is_mixed fires when GTO genuinely mixes this hand
_MIXED_LOW = 0.1
_MIXED_HIGH = 0.8


# ---------------------------------------------------------------------------
# PreflopDecision dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PreflopDecision:
    """
    Immutable result of a preflop decision lookup.

    Fields
    ------
    action : str
        One of 'FOLD', 'CALL', 'RAISE'.
    confidence : float
        0.0–1.0. Derived from range_frequency, clamped to [0.30, 0.95].
        For FOLD: 1.0 - range_frequency. For everything else: range_frequency.
    scenario : str
        One of 'rfi', 'defend_call', 'defend_3bet', 'squeeze', 'bb_option'.
    is_mixed : bool
        True when GTO genuinely mixes — range_frequency is between 0.1 and 0.8.
    range_frequency : float
        Raw frequency from the GTO range table (0.0–1.0).
    pot_odds_pct : float
        Required break-even equity as a percentage.
        Formula: to_call / (pot + to_call) * 100.
        Zero for RFI and BB_OPTION (no bet to call).
    equity_needed : float
        Same value as pot_odds_pct. Separate field for display convenience.
    opener_position : str
        Position of the player who opened the pot. Empty string for RFI.
    """
    action: str
    confidence: float
    scenario: str
    is_mixed: bool
    range_frequency: float
    pot_odds_pct: float
    equity_needed: float
    opener_position: str


# ---------------------------------------------------------------------------
# detect_scenario
# ---------------------------------------------------------------------------

def detect_scenario(game_state: dict) -> str:
    """
    Determine the preflop scenario from a game state snapshot.

    Required keys
    -------------
    num_raises_this_street : int   — count of preflop raises (0 = no open yet)
    num_callers : int              — players who called the open (default 0)
    hero_has_raised : bool         — True if hero made the first raise
    hero_position : str            — 'UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB'
    to_call : int / float          — chips hero must call (0 = no bet to face)
    opener_position : str or None  — position of first raiser (None if no open)

    Returns
    -------
    One of: 'rfi', 'defend_call', 'defend_3bet', 'squeeze', 'bb_option'
    """
    raises = game_state['num_raises_this_street']
    callers = game_state.get('num_callers', 0)
    hero_raised = game_state.get('hero_has_raised', False)
    to_call = game_state['to_call']
    pos = game_state['hero_position']

    # No raise yet — hero is first to act or all others folded
    if raises == 0 and to_call == 0:
        if pos == 'BB':
            # BB gets a free play or can raise (isolation / squeeze vs limpers)
            return 'bb_option'
        return 'rfi'

    # One raise in front, hero has NOT raised — facing an open
    if raises == 1 and not hero_raised:
        if callers >= 1:
            # Open + at least one caller — hero can squeeze
            return 'squeeze'
        return 'defend_call'

    # Hero raised and is now facing a re-raise (3-bet against hero)
    if raises >= 2 and hero_raised:
        return 'defend_3bet'

    # Fallback: treat any multi-raise action facing hero as defend_3bet
    return 'defend_3bet'


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _compute_pot_odds(pot: float, to_call: float) -> float:
    """
    Standard pot-odds formula: to_call / (pot + to_call) * 100.

    Returns the minimum equity percentage needed to break even on a call.
    Returns 0.0 when to_call is zero (no bet to call).
    """
    if to_call <= 0:
        return 0.0
    return (to_call / (pot + to_call)) * 100.0


def _implied_odds_override(hand: str, opener_pos: str) -> bool:
    """
    Returns True when implied odds justify a call that the raw range tables
    might under-represent.

    Eligible hands at 100bb:
        - Small pairs: 22, 33, 44, 55 (set-mining equity)
        - Suited connectors: 54s, 65s, 76s, 87s, 98s (nut-potential)

    Condition: opener is NOT UTG or HJ (tighter ranges reduce implied odds
    because we hit less often against a strong range and get paid less).

    Stack depth is always 100bb in this engine — no additional check needed.
    """
    hand_eligible = hand in _SMALL_PAIRS or hand in _SUITED_CONNECTORS_IMPLIED
    opener_not_tight = opener_pos.upper() not in _TIGHT_OPENER_POSITIONS
    return hand_eligible and opener_not_tight


def _derive_confidence(action: str, range_frequency: float, scenario: str) -> float:
    """
    Compute confidence from the range frequency and the recommended action.

    For range-based preflop decisions the range frequency is the confidence
    signal for the recommended action:
        RAISE with freq=1.0  → confidence=1.0 (always raise)
        CALL  with freq=0.9  → confidence=0.9 (almost always call)
        FOLD  when freq=0.0  → confidence=1.0 (clear fold, no playable freq)

    For FOLD: confidence = 1.0 - range_frequency
        (the lower the play frequency, the more confident the fold)

    Clamped to [0.30, 0.95] — never display 0% or 100% to students.
    """
    if action == 'FOLD':
        conf = 1.0 - range_frequency
    else:
        conf = range_frequency
    return max(0.30, min(0.95, conf))


# ---------------------------------------------------------------------------
# Scenario decision functions
# ---------------------------------------------------------------------------

def _decide_rfi(hand: str, hero_pos: str, pot: float, to_call: float,
                rm: RangeManager) -> PreflopDecision:
    """
    RFI: no prior action. Hero decides whether to open or fold.

    Range table: RFI[hero_pos]
    Logic:
        freq >= 0.5  → RAISE (clear open or mixed-but-lean-raise)
        0 < freq < 0.5 → RAISE with mixed flag (GTO mixes but leans fold at low freqs;
                          the standard threshold is 0.5 per design doc section 1.2)
        freq == 0.0  → FOLD
    """
    rfi_range = rm.get_rfi_range(hero_pos)
    freq = rfi_range.get(hand, 0.0)

    if freq >= 0.5:
        action = 'RAISE'
    elif freq > 0.0:
        # GTO mixes — still fire RAISE but flag as mixed
        action = 'RAISE'
    else:
        action = 'FOLD'

    is_mixed = _MIXED_LOW <= freq <= _MIXED_HIGH
    pot_odds = _compute_pot_odds(pot, to_call)  # Will be 0 for RFI
    conf = _derive_confidence(action, freq, 'rfi')

    return PreflopDecision(
        action=action,
        confidence=conf,
        scenario='rfi',
        is_mixed=is_mixed,
        range_frequency=freq,
        pot_odds_pct=pot_odds,
        equity_needed=pot_odds,
        opener_position='',
    )


def _decide_defend_call(hand: str, hero_pos: str, opener_pos: str,
                        pot: float, to_call: float, rm: RangeManager) -> PreflopDecision:
    """
    DEFEND_CALL: facing exactly one open, hero has not yet acted.

    Priority order per design doc section 1.3:
        1. Check THREE_BET range — if hand is in it, recommend RAISE (3-bet)
        2. Check CALL_VS_OPEN range — if in it, recommend CALL
        3. Check implied odds override — small pairs / suited connectors vs non-tight opener
        4. FOLD

    The 'call_freq' threshold for CALL is 0.3 per design doc. For 3-bet the
    threshold is 0.5 for a clear 3-bet (any > 0.0 is a mixed 3-bet spot).
    """
    threeb_range = rm.get_3bet_range(hero_pos, opener_pos)
    call_range = rm.get_call_range(hero_pos, opener_pos)

    threeb_freq = threeb_range.get(hand, 0.0)
    call_freq = call_range.get(hand, 0.0)

    pot_odds = _compute_pot_odds(pot, to_call)

    # Step 1: 3-bet range takes priority
    if threeb_freq >= 0.5:
        action = 'RAISE'
        raw_freq = threeb_freq
    elif threeb_freq > 0.0:
        # Mixed 3-bet spot — lean toward 3-bet per design doc
        action = 'RAISE'
        raw_freq = threeb_freq
    # Step 2: flat-call range
    elif call_freq >= 0.3:
        action = 'CALL'
        raw_freq = call_freq
    elif call_freq > 0.0:
        # Mixed call spot
        action = 'CALL'
        raw_freq = call_freq
    # Step 3: implied odds safety net (SB is 3-bet-or-fold, no cold-calls)
    elif hero_pos.upper() != 'SB' and _implied_odds_override(hand, opener_pos):
        action = 'CALL'
        raw_freq = 0.45  # Fixed implied-odds confidence per design doc
    # Step 4: fold
    else:
        action = 'FOLD'
        raw_freq = max(threeb_freq, call_freq)  # Best playable frequency

    is_mixed = _MIXED_LOW <= raw_freq <= _MIXED_HIGH
    conf = _derive_confidence(action, raw_freq, 'defend_call')

    return PreflopDecision(
        action=action,
        confidence=conf,
        scenario='defend_call',
        is_mixed=is_mixed,
        range_frequency=raw_freq,
        pot_odds_pct=pot_odds,
        equity_needed=pot_odds,
        opener_position=opener_pos,
    )


def _decide_defend_3bet(hand: str, hero_pos: str, opener_pos: str,
                        pot: float, to_call: float, rm: RangeManager) -> PreflopDecision:
    """
    DEFEND_3BET: hero raised, villain 3-bet, hero decides to 4-bet / call / fold.

    Priority per design doc section 1.5:
        1. FOURBET range → RAISE (4-bet)
        2. CALL_VS_3BET range → CALL
        3. FOLD
    """
    fourbet_range = rm.get_fourbet_range(hero_pos)
    call_3bet_range = rm.get_call_vs_3bet_range(hero_pos, opener_pos)

    fourbet_freq = fourbet_range.get(hand, 0.0)
    call_freq = call_3bet_range.get(hand, 0.0)

    pot_odds = _compute_pot_odds(pot, to_call)

    if fourbet_freq > 0.0:
        action = 'RAISE'
        raw_freq = fourbet_freq
    elif call_freq > 0.0:
        action = 'CALL'
        raw_freq = call_freq
    else:
        action = 'FOLD'
        raw_freq = max(fourbet_freq, call_freq)

    is_mixed = _MIXED_LOW <= raw_freq <= _MIXED_HIGH
    conf = _derive_confidence(action, raw_freq, 'defend_3bet')

    return PreflopDecision(
        action=action,
        confidence=conf,
        scenario='defend_3bet',
        is_mixed=is_mixed,
        range_frequency=raw_freq,
        pot_odds_pct=pot_odds,
        equity_needed=pot_odds,
        opener_position=opener_pos,
    )


def _decide_squeeze(hand: str, hero_pos: str, opener_pos: str,
                    pot: float, to_call: float, rm: RangeManager) -> PreflopDecision:
    """
    SQUEEZE: open + caller(s) in front, hero can 3-bet, call, or fold.

    Priority:
        1. THREEB range → RAISE (squeeze)
        2. CALL range → CALL (flat with implied odds)
        3. Implied odds override → CALL (small pairs, suited connectors)
        4. FOLD

    The extra caller(s) add dead money, which slightly improves pot odds for
    a flat call. The CALL range here is the same as in defend_call — the
    positional disadvantage (OOP vs BB) is offset by the added dead money.
    This mirrors _decide_defend_call() with the same priority chain.
    """
    threeb_range = rm.get_3bet_range(hero_pos, opener_pos)
    call_range = rm.get_call_range(hero_pos, opener_pos)

    threeb_freq = threeb_range.get(hand, 0.0)
    call_freq = call_range.get(hand, 0.0)

    pot_odds = _compute_pot_odds(pot, to_call)

    # Step 1: Squeeze (3-bet) range
    if threeb_freq > 0.0:
        action = 'RAISE'
        raw_freq = threeb_freq
    # Step 2: Flat-call range
    elif call_freq > 0.0:
        action = 'CALL'
        raw_freq = call_freq
    # Step 3: Implied odds safety net (SB is 3-bet-or-fold, no cold-calls)
    elif hero_pos.upper() != 'SB' and _implied_odds_override(hand, opener_pos):
        action = 'CALL'
        raw_freq = 0.45  # Fixed implied-odds confidence
    # Step 4: Fold
    else:
        action = 'FOLD'
        raw_freq = max(threeb_freq, call_freq)

    is_mixed = _MIXED_LOW <= raw_freq <= _MIXED_HIGH
    conf = _derive_confidence(action, raw_freq, 'squeeze')

    return PreflopDecision(
        action=action,
        confidence=conf,
        scenario='squeeze',
        is_mixed=is_mixed,
        range_frequency=raw_freq,
        pot_odds_pct=pot_odds,
        equity_needed=pot_odds,
        opener_position=opener_pos,
    )


def _decide_bb_option(hand: str, pot: float, rm: RangeManager) -> PreflopDecision:
    """
    BB_OPTION: unraised pot, BB has the option.

    Per design doc section 1.4:
        - Use BTN RFI as proxy for BB isolation / raise range (top ~45% of hands)
        - If hand qualifies (freq >= 0.5 in BTN RFI): RAISE
        - Otherwise: CHECK (represented as action='CALL' with 0 to_call, or a
          dedicated CHECK action)

    We use 'CALL' as the CHECK action label because the game engine calls it that
    and because the student sees "CHECK" from context. The design explicitly maps
    no-raise → CHECK.
    """
    # BTN RFI as proxy for BB isolation range per design doc
    btn_rfi = rm.get_rfi_range('BTN')
    freq = btn_rfi.get(hand, 0.0)

    pot_odds = _compute_pot_odds(pot, 0.0)  # No bet to call in unraised pot

    if freq >= 0.5:
        action = 'RAISE'
    else:
        # Recommend check — stored as FOLD with action 'CALL' would be confusing;
        # we use a literal 'CHECK' string here per design doc section 1.4
        action = 'CHECK'

    is_mixed = _MIXED_LOW <= freq <= _MIXED_HIGH
    conf = _derive_confidence('FOLD' if action == 'CHECK' else action, freq, 'bb_option')

    return PreflopDecision(
        action=action,
        confidence=conf,
        scenario='bb_option',
        is_mixed=is_mixed,
        range_frequency=freq,
        pot_odds_pct=pot_odds,
        equity_needed=pot_odds,
        opener_position='',
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def decide_preflop(
    hand_notation: str,
    hero_position: str,
    scenario: str,
    opener_position: str,
    pot: float,
    to_call: float,
    rm: RangeManager,
) -> PreflopDecision:
    """
    Main entry point. Returns a PreflopDecision for the given game state.

    Parameters
    ----------
    hand_notation : str
        Hand in standard notation: 'AKs', 'TT', 'J9o', etc.
    hero_position : str
        Hero's seat: 'UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB'.
    scenario : str
        One of: 'rfi', 'defend_call', 'defend_3bet', 'squeeze', 'bb_option'.
        Use detect_scenario() to derive this from a game_state dict.
    opener_position : str
        Position of the player who opened. Empty string or any value for RFI /
        BB_OPTION (it's ignored in those scenarios).
    pot : float
        Total chips in the pot before hero acts.
    to_call : float
        Chips hero must put in to call. Zero for RFI and BB_OPTION.
    rm : RangeManager
        An initialised RangeManager instance.

    Returns
    -------
    PreflopDecision
    """
    s = scenario.lower()

    if s == 'rfi':
        return _decide_rfi(hand_notation, hero_position, pot, to_call, rm)
    elif s == 'defend_call':
        return _decide_defend_call(hand_notation, hero_position, opener_position,
                                   pot, to_call, rm)
    elif s == 'defend_3bet':
        return _decide_defend_3bet(hand_notation, hero_position, opener_position,
                                   pot, to_call, rm)
    elif s == 'squeeze':
        return _decide_squeeze(hand_notation, hero_position, opener_position,
                               pot, to_call, rm)
    elif s == 'bb_option':
        return _decide_bb_option(hand_notation, pot, rm)
    else:
        raise ValueError(
            f"Unknown scenario '{scenario}'. "
            "Expected one of: rfi, defend_call, defend_3bet, squeeze, bb_option"
        )
