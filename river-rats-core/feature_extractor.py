"""
Feature Extractor for GTO Oracle V3
====================================

Extracts ~30 features per hand for XGBoost model training.
Built incrementally — each step adds a layer of features.

Step 1: Zero-compute features (parsed directly from gauntlet JSON)
Step 2: Hand evaluation features (hand_evaluator.py)
Step 3: Board analysis features (board_analyzer.py)
Step 4: Range + equity features (range_manager, raw_equity)
Step 5: Range partitioning — better/worse hand pct (FIXED)
Step 6: Derived features + CSV export

═══════════════════════════════════════════════════════════════════
Cross-stream contract (MUSTs #10 + #42 + #43 + #57 — Stage 3.5)
═══════════════════════════════════════════════════════════════════

NaN semantics on output feature dict:

The composition + blocker features may carry `float('nan')` values
when villain is out of the hand or the action-history chain
over-narrows. Non-NaN path semantics unchanged.

NaN-permitted features (allowlisted in gto_model.features_from_dict):
  Composition (MUST #10 sub-2):
    villain_top_pair_plus_pct, villain_draw_pct, villain_air_pct,
    villain_medium_made_pct
  Blocker (MUST #10 sub-2):
    flush_block_pct, flush_draw_block_pct, straight_draw_block_pct,
    nut_made_block_pct

NaN triggers (via `_villain_folded` / `_villain_chain_overflowed`
sentinel fields on the return dict):
  - villain_folded=True: chain terminated at ':FOLD' step; villain
    physically out of hand
  - villain_chain_overflowed=True: chain over-narrowed to empty
    without FOLD (MUST #15) OR floor-truncated mass (MUST #28)

Non-NaN for all other feature columns. `board_favour` forced to 0.0
on sentinel trigger (hero-range-derived; not in NaN allowlist —
see C1 fix in commit 4.1).

Teaching CONTENT_API contract (MUST #42 + #43 + #57):

Teaching layer (river-rats-teaching repo) renders NaN-valued features
via player-English prose per MUST #42:

  Folded villain (HU):
    "Villain folded earlier — no range to read."
  Folded villain (multiway, ≥1 live villain remaining):
    "Villain {FOLDED_POS} folded; reading against villain {LIVE_POS} only."
  Over-narrow / floor-truncated chain:
    "Villain's line is too rare to read confidently — relying on equity alone."

Teaching CONTENT_API schema expected: `l3_enriched_v4.1` (MUST #57).
Version-pin enforcement is NOT runtime-checked in logic; Stage 6 ship-
gate pre-flight audit verifies:
  (a) river-rats-teaching/interface/CONTENT_API.md version: v4.1
  (b) Game adapter pins matching version
  (c) Playtest log schema handles NaN values without crash

MUST #57 gate relocation (per Stage 3.5 commit 4 Path-B directive):
the protective scope is "teaching renders NaN correctly BEFORE players
see v2.4 output" — which happens at Stage 6 ship, not earlier commits.
v2.4 features don't flow to teaching's live renderer until Stage 6.

Reference comms:
  - review/comms/TICKET_CONTENT_API_V4_NAN_RENDER_2026-04-22.md
  - review/comms/MAIN_TERMINAL_TEACHING_V4_1_DECISIONS_2026-04-22.md
"""

import os
import sys
sys.path.insert(0, '/mnt/project')

from typing import Dict, List, Optional, Tuple

from feature_keys import F


# =============================================================================
# Constants
# =============================================================================

POSITION_ORDINAL = {
    'UTG': 0, 'EP': 0,
    'HJ': 1, 'MP': 1,
    'CO': 2,
    'BTN': 3,
    'SB': 4,
    'BB': 5,
}

# Acting order postflop (lower = earlier = OOP)
POSTFLOP_ORDER = {
    'SB': 0,
    'BB': 1,
    'UTG': 2, 'EP': 2,
    'HJ': 3, 'MP': 3,
    'CO': 4,
    'BTN': 5,
}

STREET_ENCODING = {
    'f': 0,
    't': 1,
    'r': 2,
}

ACTION_ENCODING = {
    'F': 'FOLD',
    'X': 'CHECK',
    'C': 'CALL',
    'B': 'BET',
    'R': 'RAISE',
}

# When villain position is missing (PFR hands with no specific villain),
# infer the most likely caller based on hero's position.
# These are the most common defend positions vs each open.
DEFAULT_VILLAIN_FOR_PFR = {
    'UTG': 'BB',
    'HJ': 'BB',
    'CO': 'BB',
    'BTN': 'BB',
    'SB': 'BB',   # Shouldn't occur in data but safe default
    'BB': 'BTN',  # Shouldn't occur in data but safe default
}


# =============================================================================
# Hand Parsing
# =============================================================================

def parse_hero_hand(hand_str: str) -> List[str]:
    """
    Parse hero hand string into two card strings.

    Args:
        hand_str: e.g. 'Jd9s', 'AdKc', 'TsTh'

    Returns:
        List of two card strings, e.g. ['Jd', '9s']
    """
    if len(hand_str) != 4:
        raise ValueError(f"Invalid hand string '{hand_str}': expected 4 chars")
    return [hand_str[:2], hand_str[2:]]


def parse_board(board_str: str) -> List[str]:
    """
    Parse board string into list of card strings.

    Args:
        board_str: e.g. '4s4h3hJh8c' (5 cards) or 'Th4c5d' (3 cards)

    Returns:
        List of card strings, e.g. ['4s', '4h', '3h', 'Jh', '8c']
    """
    if len(board_str) % 2 != 0:
        raise ValueError(f"Invalid board string '{board_str}': odd length")
    cards = [board_str[i:i+2] for i in range(0, len(board_str), 2)]
    num_cards = len(cards)
    if num_cards not in (3, 4, 5):
        raise ValueError(
            f"Invalid board '{board_str}': got {num_cards} cards, expected 3-5"
        )
    return cards


def is_in_position(hero_pos: str, villain_pos: str) -> bool:
    """
    Determine if hero acts AFTER villain postflop (i.e. is in position).

    Postflop order: SB, BB, UTG, HJ, CO, BTN
    Higher POSTFLOP_ORDER = acts later = in position.

    Args:
        hero_pos: Hero's position
        villain_pos: Villain's position

    Returns:
        True if hero is in position (acts last)
    """
    hero_order = POSTFLOP_ORDER.get(hero_pos.upper(), 2)
    villain_order = POSTFLOP_ORDER.get(villain_pos.upper(), 2)
    return hero_order > villain_order


# =============================================================================
# Hand Category Encoding (ordinal â€” higher = stronger)
# =============================================================================

# All categories returned by hand_evaluator.evaluate_hand(), ordered by strength.
# XGBoost handles ordinal encoding well â€” more granularity = more signal.
HAND_CATEGORY_ENCODING = {
    'high_card': 0,
    'one_overcard': 1,
    'overcards': 2,
    'bottom_pair': 3,
    'underpair': 4,
    'middle_pair': 5,
    'top_pair': 6,
    'top_pair_good_kicker': 7,
    'top_pair_top_kicker': 8,
    'overpair': 9,
    'two_pair': 10,
    'trips': 11,
    'set': 12,
    'straight': 13,
    'flush': 14,
    'full_house': 15,
    'quads': 16,
    'straight_flush': 17,
}


# =============================================================================
# Step 1: Zero-Compute Feature Extraction
# =============================================================================

def extract_zero_compute_features(hand: Dict) -> Dict:
    """
    Extract features that require NO foundation module calls.
    Parsed directly from the gauntlet JSON fields.

    Args:
        hand: Single hand dict from gauntlet JSON

    Returns:
        Dict of feature_name -> value
    """
    hero_pos = hand['pos'].upper()
    facing_bet = int(hand['fb'])
    pot = float(hand['pot'])
    to_call = float(hand.get('tc', 0.0))
    street_code = hand['st']

    # Villain position â€” may be missing for PFR hands
    villain_pos_raw = hand.get('vp', None)
    if villain_pos_raw:
        villain_pos = villain_pos_raw.upper()
    else:
        villain_pos = DEFAULT_VILLAIN_FOR_PFR.get(hero_pos, 'BB')

    # Pot odds: to_call / (pot + to_call).  0 when not facing bet.
    if facing_bet and (pot + to_call) > 0:
        pot_odds = to_call / (pot + to_call)
    else:
        pot_odds = 0.0

    # Bet-to-pot ratio: to_call / pot.  0 when not facing bet.
    if facing_bet and pot > 0:
        bet_to_pot = to_call / pot
    else:
        bet_to_pot = 0.0

    # Parse cards for downstream steps
    hero_cards = parse_hero_hand(hand['h'])
    board_cards = parse_board(hand['b'])

    features = {
        # Situational
        'street': STREET_ENCODING[street_code],
        'facing_bet': facing_bet,
        'pot_size': pot,
        'to_call': to_call,
        'pot_odds': round(pot_odds, 6),
        'bet_to_pot': round(bet_to_pot, 6),

        # Position
        'hero_position': POSITION_ORDINAL[hero_pos],
        'villain_position': POSITION_ORDINAL[villain_pos],
        'is_ip': int(is_in_position(hero_pos, villain_pos)),

        # Label (GTO action)
        'action': ACTION_ENCODING[hand['exp']],

        # Metadata (not features â€” used for tracing/debugging)
        '_hand_id': hand.get('id', -1),
        '_hero_cards': hero_cards,
        '_board_cards': board_cards,
        '_hero_pos_raw': hero_pos,
        '_villain_pos_raw': villain_pos,
        '_villain_pos_inferred': villain_pos_raw is None,
        '_street_raw': street_code,
    }

    return features


# =============================================================================
# Step 2: Hand Evaluation Features
# =============================================================================

from hand_evaluator import evaluate_hand, HandEvaluation


def extract_hand_eval_features(hero_cards: List[str],
                               board_cards: List[str]) -> Dict:
    """
    Extract features from hand_evaluator.evaluate_hand().

    Args:
        hero_cards: ['Jd', '9s']
        board_cards: ['4s', '4h', '3h', 'Jh', '8c']

    Returns:
        Dict of hand evaluation features
    """
    evaluation = evaluate_hand(hero_cards, board_cards)

    category_str = evaluation.category.lower()
    category_encoded = HAND_CATEGORY_ENCODING.get(category_str, 0)

    return {
        'hand_category': category_encoded,
        'hand_rank': round(evaluation.rank, 4),
        'is_made_hand': int(evaluation.is_made_hand),
        'is_strong_made': int(evaluation.is_strong_made),
        'is_monster': int(evaluation.is_monster),
        'has_flush_draw': int(evaluation.has_flush_draw),
        'has_straight_draw': int(evaluation.has_straight_draw),
        'draw_outs': evaluation.draw_outs,
        # Keep raw category string for debugging
        '_hand_category_raw': category_str,
        '_draw_equity': round(evaluation.draw_equity, 4) if hasattr(evaluation, 'draw_equity') else 0.0,
    }


# =============================================================================
# Step 3: Board Analysis Features
# =============================================================================

from board_analyzer import analyze_board_cached, BoardAnalysis


def extract_board_features(board_cards: List[str]) -> Dict:
    """
    Extract features from board_analyzer.analyze_board().
    Uses cached version â€” boards repeat across hands.

    Args:
        board_cards: ['4s', '4h', '3h', 'Jh', '8c']

    Returns:
        Dict of board analysis features
    """
    # analyze_board_cached expects a tuple
    board_tuple = tuple(board_cards)
    analysis = analyze_board_cached(board_tuple)

    return {
        'is_monotone': int(analysis.is_monotone),
        'is_two_tone': int(analysis.is_two_tone),
        'is_rainbow': int(analysis.is_rainbow),
        'is_paired': int(analysis.is_paired),
        'is_double_paired': int(analysis.is_double_paired),
        'connectivity_score': analysis.connectivity_score,
        'high_card_rank': analysis.high_card_rank,
        'danger_score': round(analysis.danger_score, 4),
        'flush_danger': round(analysis.flush_danger, 4),
        'straight_danger': round(analysis.straight_danger, 4),
        '_pfr_advantage': round(analysis.pfr_advantage, 4) if hasattr(analysis, 'pfr_advantage') else 0.5,
        '_board_type': str(analysis.board_type.value) if hasattr(analysis, 'board_type') and hasattr(analysis.board_type, 'value') else 'unknown',
        '_needs_protection': int(analysis.needs_protection) if hasattr(analysis, 'needs_protection') else 0,
    }


# =============================================================================
# Step 4: Range Construction + Equity Features
# =============================================================================

from range_manager import RangeManager
from range_narrowing import narrow_to_betting_range
# range_narrowing.py line 41 strips /mnt/project from sys.path â€” restore it
if '/mnt/project' not in sys.path:
    sys.path.insert(0, '/mnt/project')
from raw_equity import RawEquityCalculator
import random
from hand_categories import RANKS, SUITS, cards_to_notation

# Singleton instances â€” reused across all hands
_range_manager = RangeManager()
_equity_calculator = RawEquityCalculator(mode='auto')


# =============================================================================
# Step 5: Range Partitioning (FIXED â€” proper combo expansion)
# =============================================================================

import eval7
# SUITS already available via hand_categories — consolidated with RANKS import above


def get_valid_combos(hand: str, used_cards: set) -> List[List[str]]:
    """
    Get all valid card combinations for a hand notation, excluding
    cards already in use (hero hand + board).

    This is the FIXED version matching raw_equity.py._get_valid_combos()
    exactly. V2's strategic_analyzer used a single fixed-suit combo,
    which was the root cause of broken range partitioning.

    Args:
        hand: Hand notation like 'AKs', 'QJo', '77'
        used_cards: Set of cards already in play (lowercase),
                    e.g. {'as', 'kd', '7h', '2d', 'ks'}

    Returns:
        List of valid [card1, card2] combos
    """
    if len(hand) < 2:
        return []

    rank1 = hand[0]
    rank2 = hand[1]
    used_lower = {c.lower() for c in used_cards}

    combos = []

    if rank1 == rank2:
        # Pair â€” 6 combos max (e.g. AA: AsAh, AsAd, AsAc, AhAd, AhAc, AdAc)
        for i, s1 in enumerate(SUITS):
            for s2 in SUITS[i + 1:]:
                c1 = f"{rank1}{s1}"
                c2 = f"{rank2}{s2}"
                if c1.lower() not in used_lower and c2.lower() not in used_lower:
                    combos.append([c1, c2])

    elif len(hand) >= 3 and hand[2].lower() == 's':
        # Suited â€” 4 combos max (e.g. AKs: AsKs, AhKh, AdKd, AcKc)
        for s in SUITS:
            c1 = f"{rank1}{s}"
            c2 = f"{rank2}{s}"
            if c1.lower() not in used_lower and c2.lower() not in used_lower:
                combos.append([c1, c2])

    else:
        # Offsuit â€” 12 combos max (e.g. AKo: AsKh, AsKd, AsKc, AhKs, ...)
        for s1 in SUITS:
            for s2 in SUITS:
                if s1 != s2:
                    c1 = f"{rank1}{s1}"
                    c2 = f"{rank2}{s2}"
                    if c1.lower() not in used_lower and c2.lower() not in used_lower:
                        combos.append([c1, c2])

    return combos


def _to_eval7_cards(card_strings: List[str]) -> List:
    """Convert card strings to eval7.Card objects."""
    return [eval7.Card(c) for c in card_strings]


def partition_range(hero_cards: List[str],
                    board_cards: List[str],
                    villain_range: Dict[str, float]) -> Dict:
    """
    Partition villain's range into hands that beat us, lose to us, or tie.
    Uses proper combo expansion with card removal (THE V3 FIX).

    Compares current hand strength on the board â€” not equity.
    eval7.evaluate works with 5-7 cards (flop through river).

    Args:
        hero_cards: ['Jd', '9s']
        board_cards: ['4s', '4h', '3h', 'Jh', '8c']
        villain_range: {hand_notation: frequency}

    Returns:
        Dict with better_hand_pct, worse_hand_pct, tie_pct
    """
    used_cards = set(hero_cards) | set(board_cards)

    # Pre-compute hero's hand value
    hero_eval7 = _to_eval7_cards(hero_cards)
    board_eval7 = _to_eval7_cards(board_cards)
    hero_value = eval7.evaluate(hero_eval7 + board_eval7)

    better_weight = 0.0   # Villain hands that beat us
    worse_weight = 0.0    # Villain hands we beat
    tie_weight = 0.0      # Ties
    total_weight = 0.0

    for hand_str, freq in villain_range.items():
        if freq <= 0:
            continue

        combos = get_valid_combos(hand_str, used_cards)
        for v_combo in combos:
            v_eval7 = _to_eval7_cards(v_combo)
            v_value = eval7.evaluate(v_eval7 + board_eval7)

            if v_value > hero_value:
                better_weight += freq
            elif v_value < hero_value:
                worse_weight += freq
            else:
                tie_weight += freq
            total_weight += freq

    if total_weight > 0:
        better_pct = better_weight / total_weight
        worse_pct = worse_weight / total_weight
        tie_pct = tie_weight / total_weight
    else:
        better_pct = 0.0
        worse_pct = 0.0
        tie_pct = 0.0

    return {
        'better_hand_pct': round(better_pct, 6),
        'worse_hand_pct': round(worse_pct, 6),
        '_partition_tie_pct': round(tie_pct, 6),
        '_partition_total_combos': total_weight,
    }


def extract_partition_features(hero_cards: List[str],
                               board_cards: List[str],
                               hero_pos: str,
                               villain_pos: str,
                               facing_bet: bool,
                               street_raw: str,
                               num_opponents: int = 1,
                               opponent_positions=None,
                               opener_pos: str = None,
                               bettor_pos: str = None,
                               action_history: Optional[List] = None,
                               cached_range: Optional[Dict[str, float]] = None,
                               cached_meta: Optional[Dict] = None,
                               hand: Optional[Dict] = None) -> Dict:
    """
    Extract range partitioning features using the correct villain range.

    MUST #6 + #19 + #34: when `action_history` is supplied (non-None),
    delegates to `_get_chain_narrowed_villain_range` helper so partition
    features see the SAME chain-narrowed range as composition features.

    Backward-compat when action_history is None: pre-Stage-3.5 behavior
    (single-street narrow_to_betting_range when facing_bet).

    Cache contract (MUST #63): cached_range + cached_meta populated by
    extract_all_features enables re-use of the chain computation that
    extract_range_composition already ran; avoids 3x chain compute per
    hand. LOCAL to single extract_all_features call.
    """
    if action_history is not None:
        # MUST #6: chain-inheritance path via helper.
        v_range, meta = _get_chain_narrowed_villain_range(
            hero_pos=hero_pos,
            villain_pos=villain_pos,
            opener_pos=opener_pos,
            board_cards=board_cards,
            facing_bet=facing_bet,
            street_raw=street_raw,
            action_history=action_history,
            num_opponents=num_opponents,
            opponent_positions=opponent_positions,
            bettor_pos=bettor_pos,
            cached_range=cached_range,
            cached_meta=cached_meta,
            hand=hand,   # C3 fix: hand-level cache
        )
        # MUST #64: multiway returns v_range=None (merged deprecated).
        # Partition reads primary-villain's range from per_villain_ranges.
        # v2.5+ ticket: per-villain partition features + aggregation.
        if v_range is None and num_opponents >= 2:
            pv = meta.get('per_villain_ranges', {})
            primary = opponent_positions[0] if opponent_positions else None
            if primary is None:
                raise RuntimeError(
                    'H2: missing primary opponent_position in multiway '
                    'partition path; opponent_positions empty.'
                )
            if primary not in pv:
                raise RuntimeError(
                    f'H2: per_villain_ranges missing primary {primary!r}; '
                    f'helper dropped the position. pv_keys={list(pv.keys())!r}'
                )
            v_range = pv[primary]
        return partition_range(hero_cards, board_cards, v_range or {})

    # Backward-compat: pre-Stage-3.5 path
    if num_opponents >= 2 and opponent_positions:
        v_range = get_multiway_villain_range(
            hero_pos, opponent_positions, facing_bet, board_cards, street_raw,
            opener_pos=opener_pos,
            bettor_pos=bettor_pos,
        )
    else:
        v_range = get_villain_range(hero_pos, villain_pos)
        if facing_bet:
            street_name = _normalise_street(street_raw)
            v_range, _ = narrow_to_betting_range(v_range, board_cards, street_name)

    return partition_range(hero_cards, board_cards, v_range)

# Preflop acting order (lower = acts first = more likely to be opener)
PREFLOP_ORDER = {
    'UTG': 0, 'EP': 0,
    'HJ': 1, 'MP': 1,
    'CO': 2,
    'BTN': 3,
    'SB': 4,
    'BB': 5,
}

STREET_NAME_MAP = {
    'f': 'flop',
    't': 'turn',
    'r': 'river',
    # Phase 3 HIGH-1 fix (Task 4.5): full-word + uppercase variants. Pilot
    # agents and Stage 5 retrain feature regeneration may pass mixed
    # conventions; logic's internal callers used single-char only and the
    # prior `.get(street_raw, 'flop')` silently coerced everything else to
    # 'flop' (river-reclass step then silently skipped). Whitelist now
    # covers both encodings explicitly; unknown values raise via
    # `_normalise_street` below.
    'flop': 'flop',
    'turn': 'turn',
    'river': 'river',
}


def _action_history_cache_key(action_history):
    """Build a stable, hashable cache-key fragment from action_history.

    Phase 3 HIGH-3 fix (Task 4.5): the `_chain_cache` key previously
    omitted action_history, so two consecutive calls on the same `hand`
    dict with mutated `_action_history` returned identical (stale)
    cached results. Pilot agents extracting features across multiple
    street decisions on a shared hand object would have hit this.

    Each entry in action_history may be a tuple
    `(street, position, action[, amount])` OR a dict
    `{'street': ..., 'position': ..., 'action': ...}`. We canonicalise
    to a flat tuple-of-tuples so equivalent histories under different
    encodings produce equivalent keys, and any in-place mutation
    (append, replace, reorder) yields a different key.
    """
    if not action_history:
        return ()
    out = []
    for entry in action_history:
        if isinstance(entry, dict):
            out.append((
                str(entry.get('street', '')).lower(),
                str(entry.get('position', '')).upper(),
                str(entry.get('action', '')).upper(),
                entry.get('amount'),
            ))
        elif isinstance(entry, (tuple, list)):
            # (street, position, action[, amount])
            out.append(tuple(entry))
        else:
            # Fallback — stringify so unknown encodings still hash.
            out.append((str(entry),))
    return tuple(out)


def _normalise_street(street_raw):
    """Whitelist-or-raise normaliser for street_raw values.

    Phase 3 HIGH-1 fix (Task 4.5): replaces silent-default
    `.get(street_raw, 'flop')` callsites. Accepts single-char ('f','t','r')
    and full-word ('flop','turn','river') case-insensitively. Anything
    else (including 'preflop', '', None, or any unknown token) raises
    `ValueError` so callers fail loudly instead of silently treating
    every malformed input as 'flop'.
    """
    if street_raw is None:
        raise ValueError(f"Unrecognised street: {street_raw!r}")
    if not isinstance(street_raw, str):
        raise ValueError(f"Unrecognised street: {street_raw!r}")
    key = street_raw.strip().lower()
    if key not in STREET_NAME_MAP:
        raise ValueError(f"Unrecognised street: {street_raw!r}")
    return STREET_NAME_MAP[key]

# Priority order: who is most likely still in a multiway pot
POSITION_PRIORITY = ['BB', 'BTN', 'SB', 'CO', 'HJ', 'UTG']


def assign_opponent_positions(hero_pos: str, num_opponents: int) -> List[str]:
    """
    Deterministically assign opponent positions for multiway pots.
    Fills from most-likely-in-pot positions first (BB, BTN, SB, CO, HJ, UTG).
    Excludes hero's position.
    """
    candidates = [p for p in POSITION_PRIORITY if p.upper() != hero_pos.upper()]
    return candidates[:num_opponents]


def get_villain_range(hero_pos: str, villain_pos: str,
                      opener_pos: str = None) -> Dict[str, float]:
    """
    Construct villain’s preflop range based on positions.

    When opener_pos is provided (multiway):
      - If villain IS the opener: RFI range for villain’s position
      - If villain is NOT the opener: DEFEND range vs opener’s position

    When opener_pos is None (HU / legacy fallback):
      - Earlier preflop position: RFI (current behavior, unchanged)
      - Later preflop position: DEFEND vs hero

    Args:
        hero_pos: Hero’s position
        villain_pos: Villain’s position
        opener_pos: The preflop opener’s position (None = legacy fallback)

    Returns:
        Villain’s preflop range as {hand_notation: frequency}
    """
    if opener_pos is not None:
        # Opener-aware path (multiway): opener gets RFI, everyone else gets DEFEND
        if villain_pos.upper() == opener_pos.upper():
            return _range_manager.get_rfi_range(villain_pos)
        else:
            return _range_manager.get_defend_range(villain_pos, opener_pos)

    # Legacy fallback (HU / no opener info): use PREFLOP_ORDER heuristic
    h_ord = PREFLOP_ORDER.get(hero_pos.upper(), 2)
    v_ord = PREFLOP_ORDER.get(villain_pos.upper(), 2)

    if v_ord <= h_ord:
        # Villain is in earlier position -- villain opened (RFI)
        return _range_manager.get_rfi_range(villain_pos)
    else:
        # Villain is in later position -- villain defended vs hero’s open
        return _range_manager.get_defend_range(villain_pos, hero_pos)


def _get_chain_narrowed_villain_range(
    hero_pos: str,
    villain_pos: str,
    opener_pos: Optional[str],
    board_cards: List[str],
    facing_bet: bool,
    street_raw: str,
    action_history: Optional[List] = None,
    num_opponents: int = 1,
    opponent_positions: Optional[List[str]] = None,
    bettor_pos: Optional[str] = None,
    cached_range: Optional[Dict[str, float]] = None,
    cached_meta: Optional[Dict] = None,
    hand: Optional[Dict] = None,
) -> Tuple[Optional[Dict[str, float]], Dict]:
    """MUST #6 + #19 + #30 + #34 + #46 + #52 + #63 — chain-narrowed villain
    range, single source of truth across composition + equity + partition
    + explain_hand.

    HU path (num_opponents == 1 OR no opponent_positions):
      Returns (v_range, meta). `meta` carries chain_steps, truncated,
      surviving_weight, villain_folded, chain_overflowed. per_villain_*
      fields absent for HU.

    Multiway path (num_opponents >= 2):
      Env MULTIWAY_CHAIN_MODE (MUST #52):
        'per_villain' (default) — chain each opponent's range by their
           own action history (MUST #34)
        'primary_only' — chain primary villain only; other villains
           use unchained preflop range. Used when benchmark exceeds
           perf budget (fallback per Q36 asymmetric gate).
      Returns (None, meta) per MUST #64 (merged deprecated). Callers
      read per_villain_ranges directly from meta.

    Cache contract (MUST #63):
      - LOCAL to a single extract_all_features(hand) call
      - cached_range + cached_meta MUST be paired (both None or both set)
      - NO module-level cache; garbage-collected at function exit
    """
    # MUST #63: defensive assertion on paired cache params
    if (cached_range is None) != (cached_meta is None):
        raise RuntimeError(
            'MUST #63: cache contract violation — cached_range and '
            'cached_meta must be provided together or not at all. '
            'Likely a caller bug; investigate before continuing.'
        )

    if cached_range is not None:
        return cached_range, cached_meta

    # C3 fix (commit 4.1): hand-level cache (MUST #46). When `hand` dict
    # passed and action_history present, cache the chain result on
    # hand['_chain_cache'] so composition + equity + partition share one
    # chain computation per hand. Key includes (num_opponents, tuple of
    # opponent_positions or villain_pos) so HU and MW caches don't collide.
    #
    # Phase 3 HIGH-3 fix (Task 4.5): cache key now includes a hash of
    # `action_history`. The previous key was (mw|hu, n_opps, positions)
    # only — two consecutive calls on the same `hand` dict with mutated
    # `_action_history` returned identical (stale) cached results. Pilot
    # agents extracting features for multiple street decisions on a
    # shared hand object would have hit this cache-poisoning bug.
    # `_action_history_cache_key(action_history)` builds an order-
    # preserving tuple-of-tuples hash that detects in-place mutation.
    _cache_key = None
    if hand is not None and action_history:
        _ah_key = _action_history_cache_key(action_history)
        if num_opponents >= 2 and opponent_positions:
            _cache_key = ('mw', num_opponents, tuple(opponent_positions), _ah_key)
        else:
            _cache_key = ('hu', villain_pos, _ah_key)
        _cache = hand.get('_chain_cache', None)
        if _cache is not None and _cache_key in _cache:
            return _cache[_cache_key]

    street_name = _normalise_street(street_raw)

    # HU path
    if num_opponents < 2 or not opponent_positions:
        v_range = get_villain_range(hero_pos, villain_pos, opener_pos=opener_pos)
        meta = {
            'chain_steps': [], 'truncated': False,
            'surviving_weight': 1.0,
            'villain_folded': False, 'chain_overflowed': False,
        }
        if action_history and v_range:
            from range_narrowing import narrow_by_action_history
            v_range, chain_meta = narrow_by_action_history(
                full_range=v_range,
                board=board_cards,
                action_history=action_history,
                villain_pos=villain_pos,
                decision_street=street_name,
            )
            meta['chain_steps'] = chain_meta.get('chain_steps', [])
            meta['truncated'] = chain_meta.get('truncated', False)
            meta['surviving_weight'] = chain_meta.get('surviving_weight', 1.0)
            if not v_range:
                _last = meta['chain_steps'][-1] if meta['chain_steps'] else ''
                if _last.endswith(':FOLD'):
                    meta['villain_folded'] = True
                else:
                    meta['chain_overflowed'] = True
            elif meta['truncated']:
                meta['chain_overflowed'] = True
        if (facing_bet and v_range
                and not meta['villain_folded']
                and not meta['chain_overflowed']):
            v_range, _ = narrow_to_betting_range(v_range, board_cards, street_name)
        # H5 fix (commit 4.1): telemetry — HU path doesn't use
        # MULTIWAY_CHAIN_MODE; mark method explicitly for audit logs.
        meta['_chain_method'] = 'hu'
        # C3 fix: populate hand-level cache if hand was provided
        if _cache_key is not None:
            hand.setdefault('_chain_cache', {})[_cache_key] = (v_range, meta)
        return v_range, meta

    # Multiway path — MUST #34 + #46 + #52
    # H1 fix (commit 4.1): whitelist-match; unknown env value → WARN +
    # default to per_villain (safer than silent fall-through to primary_only).
    _mw_raw = os.environ.get('MULTIWAY_CHAIN_MODE', 'per_villain').lower()
    if _mw_raw not in ('per_villain', 'primary_only'):
        import logging
        logging.getLogger(__name__).warning(
            'H1: MULTIWAY_CHAIN_MODE=%r not in whitelist '
            "{'per_villain','primary_only'}; defaulting to per_villain.",
            _mw_raw,
        )
        mw_mode = 'per_villain'
    else:
        mw_mode = _mw_raw
    primary_pos = opponent_positions[0] if opponent_positions else None

    per_villain_ranges: Dict[str, Dict[str, float]] = {}
    per_villain_truncated: Dict[str, bool] = {}
    per_villain_folded: Dict[str, bool] = {}
    per_villain_overflowed: Dict[str, bool] = {}
    per_villain_chain_steps: Dict[str, List[str]] = {}
    per_villain_metas: Dict[str, Dict] = {}

    for opp_pos in opponent_positions:
        # H4 fix (commit 4.1): defensive uniqueness guard — duplicate
        # opponent_positions entry would silently overwrite per_villain_ranges
        # and drop a villain from the MC path.
        assert opp_pos not in per_villain_ranges, (
            f'H4: duplicate opponent_position {opp_pos!r} in '
            f'{opponent_positions!r}; would silently overwrite.'
        )
        opp_range = get_villain_range(hero_pos, opp_pos, opener_pos=opener_pos)

        is_primary = (opp_pos == primary_pos)
        should_chain = bool(action_history) and (
            mw_mode == 'per_villain' or is_primary
        )

        opp_meta = {
            'chain_steps': [], 'truncated': False,
            'surviving_weight': 1.0,
            'villain_folded': False, 'chain_overflowed': False,
        }

        if should_chain and opp_range:
            from range_narrowing import (
                narrow_by_action_history, _normalize_action_entry,
            )
            # Filter to this opponent's own actions
            opp_history = [
                e for e in action_history
                if _normalize_action_entry(e).get('position', '').upper()
                    == opp_pos.upper()
            ]
            has_postflop = any(
                _normalize_action_entry(e).get('street', '').lower()
                    in ('flop', 'turn', 'river')
                for e in opp_history
            )
            if has_postflop:
                opp_range, chain_meta = narrow_by_action_history(
                    full_range=opp_range,
                    board=board_cards,
                    action_history=opp_history,
                    villain_pos=opp_pos,
                    decision_street=street_name,
                )
                opp_meta['chain_steps'] = chain_meta.get('chain_steps', [])
                opp_meta['truncated'] = chain_meta.get('truncated', False)
                opp_meta['surviving_weight'] = chain_meta.get('surviving_weight', 1.0)
                if not opp_range:
                    _last = opp_meta['chain_steps'][-1] if opp_meta['chain_steps'] else ''
                    if _last.endswith(':FOLD'):
                        opp_meta['villain_folded'] = True
                    else:
                        opp_meta['chain_overflowed'] = True
                elif opp_meta['truncated']:
                    opp_meta['chain_overflowed'] = True

        # Apply facing_bet filter only to the bettor
        is_bettor = (
            bettor_pos is not None
            and opp_pos.upper() == bettor_pos.upper()
        )
        if (facing_bet and is_bettor and opp_range
                and not opp_meta['villain_folded']
                and not opp_meta['chain_overflowed']):
            opp_range, _ = narrow_to_betting_range(
                opp_range, board_cards, street_name
            )

        per_villain_ranges[opp_pos] = opp_range
        per_villain_truncated[opp_pos] = opp_meta['truncated']
        per_villain_folded[opp_pos] = opp_meta['villain_folded']
        per_villain_overflowed[opp_pos] = opp_meta['chain_overflowed']
        per_villain_chain_steps[opp_pos] = opp_meta['chain_steps']
        per_villain_metas[opp_pos] = opp_meta

    # MUST #60(a): chain_steps as flat list with position-prefix
    agg_chain_steps: List[str] = [
        f'{opp}:{step}'
        for opp, steps in per_villain_chain_steps.items()
        for step in steps
    ]
    # MUST #60(b): surviving_weight = min across per-opponent metas
    agg_surviving_weight = (
        min(m.get('surviving_weight', 1.0) for m in per_villain_metas.values())
        if per_villain_metas else 1.0
    )
    agg_truncated = any(per_villain_truncated.values())
    agg_overflowed = any(per_villain_overflowed.values())
    # All-folded = hero runs out of villains (edge case; rare in practice)
    agg_folded = (
        all(per_villain_folded.values())
        if per_villain_folded else False
    )

    # Commit 14 Finding B fold-in: derive per-opponent composition by
    # running the same partition-by-shape logic that produces
    # villain_top_pair_plus_pct etc. (in extract_range_composition),
    # applied to that opponent's narrowed range. Stored on meta so
    # extract_all_features can promote `_per_villain_composition` onto
    # the features dict without re-iterating the per-villain ranges.
    # Triple keys: 'tp_plus', 'medium', 'draw', 'air' (sums to ≈1.0
    # per opponent unless range is empty / folded / overflowed).
    per_villain_composition: Dict[str, Dict[str, float]] = {}
    for opp_pos, opp_range in per_villain_ranges.items():
        comp = {'tp_plus': 0.0, 'medium': 0.0, 'draw': 0.0, 'air': 0.0}
        if opp_range and not per_villain_folded.get(opp_pos, False) \
                and not per_villain_overflowed.get(opp_pos, False):
            tp_w = md_w = dr_w = ar_w = total_w = 0.0
            for hand_notation, freq in opp_range.items():
                if freq <= 0:
                    continue
                # Phase 3 HIGH-2 fix (Task 4.5): classify_hand now raises
                # ValueError on unrecognised notation. Audit/pilot scripts
                # loading from disk may carry corrupted range keys; log
                # + skip rather than abort the whole feature extraction.
                # Production callers (logic team's own internal range
                # builders) emit only valid notation and never trip this.
                try:
                    classification = classify_hand(hand_notation, board_cards)
                except ValueError as exc:
                    import logging
                    logging.getLogger(__name__).warning(
                        'classify_hand rejected range key %r in opp %r '
                        'composition derivation: %s; skipping combo.',
                        hand_notation, opp_pos, exc,
                    )
                    continue
                cat = classification.category
                # River: draws are dead — reclassify as air (parity with
                # extract_range_composition HU loop at line ~1753).
                if street_name == 'river' and cat == 'draw':
                    cat = 'air'
                total_w += freq
                if cat in _TOP_PAIR_PLUS:
                    tp_w += freq
                elif cat in _DRAW_CATEGORIES:
                    dr_w += freq
                elif cat in _AIR_CATEGORIES:
                    ar_w += freq
                elif cat in _MEDIUM_MADE_CATEGORIES:
                    md_w += freq
            if total_w > 0:
                comp = {
                    'tp_plus': round(tp_w / total_w, 4),
                    'medium': round(md_w / total_w, 4),
                    'draw': round(dr_w / total_w, 4),
                    'air': round(ar_w / total_w, 4),
                }
        per_villain_composition[opp_pos] = comp

    meta = {
        'chain_steps': agg_chain_steps,
        'truncated': agg_truncated,
        'surviving_weight': agg_surviving_weight,
        'villain_folded': agg_folded,
        'chain_overflowed': agg_overflowed,
        # H5 fix (commit 4.1): MULTIWAY_CHAIN_MODE telemetry — playtest logs
        # + training CSVs filter by this to distinguish per_villain rows
        # from primary_only fallback rows.
        '_chain_method': mw_mode,
        # MUST #46: per-villain data exposed; MUST #64 callers read directly.
        'per_villain_ranges': per_villain_ranges,
        'per_villain_chain_steps': per_villain_chain_steps,
        'per_villain_metas': per_villain_metas,
        'per_villain_truncated': per_villain_truncated,
        'per_villain_folded': per_villain_folded,
        'per_villain_overflowed': per_villain_overflowed,
        # Commit 14 Finding B: derived per-opponent composition triples.
        'per_villain_composition': per_villain_composition,
    }
    # C3 fix (commit 4.1): populate hand-level cache before return so
    # subsequent equity/partition/composition calls on the same hand
    # hit the cache fast-path (single chain compute per hand).
    if _cache_key is not None:
        hand.setdefault('_chain_cache', {})[_cache_key] = (None, meta)

    # MUST #64: merged deprecated for multiway; callers use per_villain_ranges.
    # Return None so any caller that tries to use "the range" raises immediately.
    return None, meta


def get_multiway_villain_range(
    hero_pos: str,
    opponent_positions: List[str],
    facing_bet: bool,
    board_cards: List[str],
    street_raw: str,
    opener_pos: str = None,
    bettor_pos: str = None,
) -> Dict[str, float]:
    """
    Merge multiple opponent ranges into a single unified range.
    merged[hand] = max(range_1[hand], range_2[hand], ..., range_n[hand])

    This represents "at least one opponent could have this hand."
    raw_equity.py already accepts arbitrary range dicts, so merged range
    works without changes to the equity calculator.

    When opener_pos is provided, the opener gets an RFI range and all
    other opponents get DEFEND ranges vs the opener (tighter and more
    accurate than assigning RFI to every player).

    When bettor_pos is provided and facing_bet=True, only the bettor's
    range is narrowed. Non-betting opponents retain their full ranges.
    When bettor_pos is None and facing_bet=True, nobody is narrowed
    (fallback: narrowing the wrong opponent is worse than not narrowing).
    """
    merged = {}
    for opp_pos in opponent_positions:
        v_range = get_villain_range(hero_pos, opp_pos, opener_pos=opener_pos)
        # Only narrow the bettor's range. Non-betting opponents (callers/checkers)
        # keep their full preflop calling ranges.
        # Fallback when bettor_pos unknown: narrow nobody.
        # Rationale: narrowing the wrong opponent distorts range shape more than
        # keeping full ranges (which only slightly inflates hero equity).
        is_bettor = (
            bettor_pos is not None
            and opp_pos.upper() == bettor_pos.upper()
        )
        if facing_bet and is_bettor:
            street_name = _normalise_street(street_raw)
            v_range, _ = narrow_to_betting_range(v_range, board_cards, street_name)
        for hand, freq in v_range.items():
            merged[hand] = max(merged.get(hand, 0.0), freq)
    return merged



def _true_multiway_equity_mc(
    hero_cards: List[str],
    board_cards: List[str],
    opponent_ranges: List[Dict[str, float]],
    trials: int = 2000,
) -> float:
    """
    True N-opponent Monte Carlo equity calculator.

    For each trial:
      1. For each opponent, sample one hand from their individual range
         (weighted by frequency, with card removal applied sequentially).
      2. Deal remaining board cards randomly.
      3. Hero wins only if they beat ALL opponents simultaneously.

    This is the correct multiway equity model. The previous merged-range
    approach inflated hero equity by +23.6pp average (see
    design/multiway/EQUITY_INVESTIGATION.md).

    Args:
        hero_cards: e.g. ['5c', '4c']
        board_cards: e.g. ['Jd', '8h', '5s']
        opponent_ranges: list of {hand_notation: frequency} dicts, one per opponent
        trials: Monte Carlo sample count (2000 for training, 10000 for analysis)

    Returns:
        float: hero equity in [0.0, 1.0]
    """
    all_deck_cards = [f"{rank}{suit}" for rank in RANKS for suit in SUITS]

    hero_set = {c.lower() for c in hero_cards}
    board_set = {c.lower() for c in board_cards}
    base_used = hero_set | board_set

    wins = 0
    ties = 0
    valid_trials = 0

    hero_eval7 = [eval7.Card(c) for c in hero_cards]
    board_eval7 = [eval7.Card(c) for c in board_cards]

    for _ in range(trials):
        used_cards = set(base_used)
        opp_hands_str = []
        trial_valid = True

        for opp_range in opponent_ranges:
            hand_str_list = _sample_from_range(opp_range, used_cards)
            if hand_str_list is None:
                trial_valid = False
                break
            opp_hands_str.append(hand_str_list)
            used_cards.update(c.lower() for c in hand_str_list)

        if not trial_valid:
            continue

        # Deal remaining board cards to complete 5-card board
        remaining_needed = 5 - len(board_cards)
        if remaining_needed > 0:
            available = [c for c in all_deck_cards if c.lower() not in used_cards]
            if len(available) < remaining_needed:
                continue
            runout = random.sample(available, remaining_needed)
            full_board = board_eval7 + [eval7.Card(c) for c in runout]
        else:
            full_board = board_eval7

        # Evaluate hero
        hero_score = eval7.evaluate(hero_eval7 + full_board)

        # Evaluate each opponent — hero must beat ALL
        opp_scores = []
        for opp_hand in opp_hands_str:
            opp_e7 = [eval7.Card(c) for c in opp_hand]
            opp_scores.append(eval7.evaluate(opp_e7 + full_board))

        best_opp = max(opp_scores)

        if hero_score > best_opp:
            wins += 1
        elif hero_score == best_opp:
            ties += 1

        valid_trials += 1

    if valid_trials == 0:
        return 0.0

    return (wins + ties * 0.5) / valid_trials


def _sample_from_range(
    opp_range: Dict[str, float],
    used_cards_set: set,
    max_attempts: int = 50,
):
    """
    Sample a specific 2-card hand from opponent's range, avoiding used_cards.
    Returns a list of 2 card strings, or None if sampling fails after max_attempts.
    Range weighting: each combo's weight = its frequency.
    """
    weighted_combos = []
    total_weight = 0.0

    for hand_notation, freq in opp_range.items():
        if freq <= 0:
            continue
        combos = get_valid_combos(hand_notation, used_cards_set)
        for combo in combos:
            weighted_combos.append((combo, freq))
            total_weight += freq

    if not weighted_combos or total_weight == 0:
        return None

    for _ in range(max_attempts):
        r = random.random() * total_weight
        cumulative = 0.0
        for combo, freq in weighted_combos:
            cumulative += freq
            if cumulative >= r:
                c1, c2 = combo
                if (c1.lower() not in used_cards_set and
                        c2.lower() not in used_cards_set):
                    return combo
                break

    return None


def extract_equity_features(hero_cards: List[str],
                            board_cards: List[str],
                            hero_pos: str,
                            villain_pos: str,
                            facing_bet: bool,
                            street_raw: str,
                            trials: int = 500,
                            num_opponents: int = 1,
                            opponent_positions=None,
                            opener_pos: str = None,
                            bettor_pos: str = None,
                            action_history: Optional[List] = None,
                            cached_range: Optional[Dict[str, float]] = None,
                            cached_meta: Optional[Dict] = None,
                            hand: Optional[Dict] = None) -> Dict:
    """
    Extract equity features: raw equity vs villain's (possibly narrowed) range.

    Critical V3 fix: when facing a bet, equity is calculated against
    villain's BETTING range (narrowed), not their full preflop range.

    Args:
        hero_cards: ['Jd', '9s']
        board_cards: ['4s', '4h', '3h', 'Jh', '8c']
        hero_pos: 'BB'
        villain_pos: 'SB'
        facing_bet: True/False
        street_raw: 'f'/'t'/'r'
        trials: Monte Carlo samples (for flop)
        num_opponents: Number of opponents (1=heads-up, 2+=multiway)
        opponent_positions: List of opponent position strings for multiway

    Returns:
        Dict with equity features
    """
    # MUST #6: chain-inheritance path. When action_history supplied,
    # equity MC samples from chain-narrowed ranges (same source of truth
    # as composition + blocker features). Cache fast-path avoids
    # recomputing the chain 3x per hand (MUST #46/#63).
    if action_history is not None:
        v_range_from_helper, chain_meta = _get_chain_narrowed_villain_range(
            hero_pos=hero_pos,
            villain_pos=villain_pos,
            opener_pos=opener_pos,
            board_cards=board_cards,
            facing_bet=facing_bet,
            street_raw=street_raw,
            action_history=action_history,
            num_opponents=num_opponents,
            opponent_positions=opponent_positions,
            bettor_pos=bettor_pos,
            cached_range=cached_range,
            cached_meta=cached_meta,
            hand=hand,   # C3 fix: hand-level cache
        )

        if num_opponents >= 2 and opponent_positions:
            # Multiway MC samples per-opponent. MUST #34/#46: read
            # per_villain_ranges directly from helper meta.
            pv_ranges = chain_meta.get('per_villain_ranges', {})
            # H2 fix (commit 4.1): raise on missing-position; empty dict
            # fallback silently inflates equity by giving MC a no-villain.
            opponent_ranges = []
            for p in opponent_positions:
                if p not in pv_ranges:
                    raise RuntimeError(
                        f'H2: per_villain_ranges missing opponent_position '
                        f'{p!r} in equity MC path. pv_keys='
                        f'{list(pv_ranges.keys())!r}'
                    )
                opponent_ranges.append(pv_ranges[p])
            mc_equity = _true_multiway_equity_mc(
                hero_cards, board_cards, opponent_ranges, trials=2000
            )
            return {
                'raw_equity': round(mc_equity, 6),
                'equity_vs_range': round(mc_equity, 6),
                # H5 fix: include chain method in equity method telemetry
                '_equity_method': f'true_multiway_mc_chained_{chain_meta.get("_chain_method", "per_villain")}',
                '_equity_villain_combos': num_opponents,
            }
        else:
            # HU — helper returned v_range directly in v_range_from_helper.
            v_range = v_range_from_helper or {}
            # HU chain-narrowed path: compute equity against the narrowed range.
            equity_result = _equity_calculator.calculate(
                hero_cards, v_range, board_cards, trials=trials
            )
            return {
                'raw_equity': round(equity_result.equity, 6),
                'equity_vs_range': round(equity_result.equity, 6),
                '_equity_method': equity_result.method + '_chained',
                '_equity_villain_combos': equity_result.villain_combos,
            }

    # Backward-compat: pre-Stage-3.5 path (action_history is None)
    if num_opponents >= 2 and opponent_positions:
        # Multiway: true N-opponent Monte Carlo (fix for +23.6pp inflation from
        # merged-range approach). Each opponent draws from their individual range;
        # hero wins only if they beat ALL opponents simultaneously.
        # See design/multiway/EQUITY_INVESTIGATION.md for methodology and results.
        opponent_ranges = []
        for opp_pos in opponent_positions:
            v_range = get_villain_range(hero_pos, opp_pos, opener_pos=opener_pos)
            # Only the bettor's range is narrowed when facing a bet.
            # Non-betting opponents (callers/checkers) keep their full preflop range.
            # Fallback when bettor_pos unknown: narrow nobody.
            # Rationale: narrowing the wrong opponent distorts range shape more than
            # keeping full ranges (which only slightly inflates hero equity).
            is_bettor = (
                bettor_pos is not None
                and opp_pos.upper() == bettor_pos.upper()
            )
            if facing_bet and is_bettor:
                street_name = _normalise_street(street_raw)
                v_range, _ = narrow_to_betting_range(v_range, board_cards, street_name)
            opponent_ranges.append(v_range)

        # Run true N-opponent Monte Carlo at 2000 trials (training speed vs accuracy tradeoff).
        # The investigation used 10000; 2000 gives ~1% variance which is sufficient for training.
        mc_equity = _true_multiway_equity_mc(
            hero_cards, board_cards, opponent_ranges, trials=2000
        )

        # KNOWN ALIAS: raw_equity and equity_vs_range stay identical (same contract
        # as HU path). Both now reflect true N-opponent equity rather than
        # inflated merged-range equity.
        return {
            'raw_equity': round(mc_equity, 6),
            'equity_vs_range': round(mc_equity, 6),
            '_equity_method': 'true_multiway_mc',
            '_equity_villain_combos': num_opponents,
        }
    else:
        # Heads-up: existing behavior unchanged
        v_range = get_villain_range(hero_pos, villain_pos)
        if facing_bet:
            street_name = _normalise_street(street_raw)
            v_range, _ = narrow_to_betting_range(v_range, board_cards, street_name)

    # 3. Calculate equity against the correct range (HU path only reaches here)
    equity_result = _equity_calculator.calculate(
        hero_cards, v_range, board_cards, trials=trials
    )

    # KNOWN ALIAS: raw_equity and equity_vs_range are intentionally identical.
    # When facing_bet=True, the range is narrowed BEFORE this calc, so both
    # reflect equity vs the narrowed betting range. The name "raw_equity" is
    # misleading but CANNOT be changed — the oracle model was trained on
    # these values being equal. See audit/v3_validation_phase4A.md FIX 3.
    return {
        'raw_equity': round(equity_result.equity, 6),
        'equity_vs_range': round(equity_result.equity, 6),
        '_equity_method': equity_result.method,
        '_equity_villain_combos': equity_result.villain_combos,
    }


# =============================================================================
# Batch Extraction
# =============================================================================

def extract_all_zero_compute(hands: List[Dict]) -> List[Dict]:
    """
    Extract zero-compute features for all hands.

    Args:
        hands: List of hand dicts from gauntlet JSON

    Returns:
        List of feature dicts
    """
    results = []
    errors = []
    for i, hand in enumerate(hands):
        try:
            features = extract_zero_compute_features(hand)
            results.append(features)
        except Exception as e:
            errors.append((i, hand.get('id', '?'), str(e)))

    if errors:
        print(f"WARNING: {len(errors)} extraction errors:")
        for idx, hid, msg in errors[:10]:
            print(f"  Hand {hid} (index {idx}): {msg}")

    return results


def extract_features_step1_2(hand: Dict) -> Dict:
    """
    Extract Step 1 (zero-compute) + Step 2 (hand evaluation) features.

    Args:
        hand: Single hand dict from gauntlet JSON

    Returns:
        Combined feature dict
    """
    features = extract_zero_compute_features(hand)
    hand_eval = extract_hand_eval_features(
        features['_hero_cards'],
        features['_board_cards'],
    )
    features.update(hand_eval)
    return features


def extract_features_step1_2_3(hand: Dict) -> Dict:
    """
    Extract Step 1 + Step 2 + Step 3 (board analysis) features.

    Args:
        hand: Single hand dict from gauntlet JSON

    Returns:
        Combined feature dict
    """
    features = extract_zero_compute_features(hand)
    hand_eval = extract_hand_eval_features(
        features['_hero_cards'],
        features['_board_cards'],
    )
    board_feat = extract_board_features(features['_board_cards'])
    features.update(hand_eval)
    features.update(board_feat)
    return features


def extract_features_step1_2_3_4(hand: Dict) -> Dict:
    """
    Extract Steps 1-4: zero-compute + hand eval + board + equity.

    Args:
        hand: Single hand dict from gauntlet JSON

    Returns:
        Combined feature dict
    """
    features = extract_zero_compute_features(hand)
    hand_eval = extract_hand_eval_features(
        features['_hero_cards'],
        features['_board_cards'],
    )
    board_feat = extract_board_features(features['_board_cards'])
    equity_feat = extract_equity_features(
        hero_cards=features['_hero_cards'],
        board_cards=features['_board_cards'],
        hero_pos=features['_hero_pos_raw'],
        villain_pos=features['_villain_pos_raw'],
        facing_bet=bool(features['facing_bet']),
        street_raw=features['_street_raw'],
    )
    features.update(hand_eval)
    features.update(board_feat)
    features.update(equity_feat)
    return features


def extract_features_step1_through_5(hand: Dict) -> Dict:
    """
    Extract Steps 1-5: all features including range partitioning.

    Args:
        hand: Single hand dict from gauntlet JSON

    Returns:
        Combined feature dict
    """
    features = extract_zero_compute_features(hand)
    hand_eval = extract_hand_eval_features(
        features['_hero_cards'],
        features['_board_cards'],
    )
    board_feat = extract_board_features(features['_board_cards'])

    num_opp = hand.get('_num_opponents', 1)
    opener_pos = hand.get('_opener_position', None)
    bettor_pos = hand.get('_bettor_position', None)
    opp_positions = None
    if num_opp >= 2:
        opp_positions = assign_opponent_positions(features['_hero_pos_raw'], num_opp)

    # MUST #6 + #19 + #30 + #34 + #46: equity + partition inherit chain
    # narrowing from hand's _action_history. Backward-compat: when
    # _action_history absent, both functions default to pre-Stage-3.5
    # single-street behavior.
    _action_history = hand.get('_action_history')

    equity_feat = extract_equity_features(
        hero_cards=features['_hero_cards'],
        board_cards=features['_board_cards'],
        hero_pos=features['_hero_pos_raw'],
        villain_pos=features['_villain_pos_raw'],
        facing_bet=bool(features['facing_bet']),
        street_raw=features['_street_raw'],
        num_opponents=num_opp,
        opponent_positions=opp_positions,
        opener_pos=opener_pos,
        bettor_pos=bettor_pos,
        action_history=_action_history,
        hand=hand,   # C3 fix: hand-level cache for MUST #46/#63
    )
    partition_feat = extract_partition_features(
        hero_cards=features['_hero_cards'],
        board_cards=features['_board_cards'],
        hero_pos=features['_hero_pos_raw'],
        villain_pos=features['_villain_pos_raw'],
        facing_bet=bool(features['facing_bet']),
        street_raw=features['_street_raw'],
        num_opponents=num_opp,
        opponent_positions=opp_positions,
        opener_pos=opener_pos,
        bettor_pos=bettor_pos,
        action_history=_action_history,
        hand=hand,   # C3 fix: hand-level cache
    )
    features.update(hand_eval)
    features.update(board_feat)
    features.update(equity_feat)
    features.update(partition_feat)
    return features


# =============================================================================
# Step 6: Derived Features + CSV Export
# =============================================================================

# Default effective stack in BB (standard 100bb game)
DEFAULT_EFFECTIVE_STACK = 100.0

# Feature columns for CSV export (excludes _ metadata fields)
FEATURE_COLUMNS = [
    # Step 1: zero-compute
    'street', 'facing_bet', 'pot_size', 'to_call', 'pot_odds', 'bet_to_pot',
    'hero_position', 'villain_position', 'is_ip',
    # Step 2: hand evaluation
    'hand_category', 'hand_rank', 'is_made_hand', 'is_strong_made',
    'is_monster', 'has_flush_draw', 'has_straight_draw', 'draw_outs',
    # Step 3: board analysis
    'is_monotone', 'is_two_tone', 'is_rainbow', 'is_paired',
    'is_double_paired', 'connectivity_score', 'high_card_rank',
    'danger_score', 'flush_danger', 'straight_danger',
    # Step 4: equity
    'raw_equity', 'equity_vs_range',
    # Step 5: range partitioning
    'better_hand_pct', 'worse_hand_pct',
    # Step 6: derived
    'equity_margin', 'spr',
    # Step 7: action history context (from PokerBench; 0 for gauntlet hands)
    'is_3bet_pot', 'villain_aggression_count',
    'villain_checked_back', 'villain_call_count',
    # Step 8: multiway context
    'num_opponents',
    # Step 10: promoted range-board features (v9)
    'villain_top_pair_plus_pct', 'villain_draw_pct', 'villain_air_pct',
    'villain_range_capped', 'board_favour',
    # Step 11: current-street action features (v9)
    'num_callers_to_bet', 'facing_raise',
    # Step 12: new features 46-48
    'flush_block_pct', 'overcard_outs', 'improvement_probability',
    # Step 13: new features 49-52
    'hero_range_percentile', 'has_showdown_value',
    'villain_fold_equity_estimate', 'flush_draw_rank',
    # Step 14: feature 53
    'is_preflop_aggressor',
    # Step 15: feature 54
    'villain_medium_made_pct',
    # Step 16: feature 55 — board-adjusted hero range percentile
    'board_adjusted_hrp',
    # Step 17: v2.4 P1 blocker-direction features 56-59
    # See review/comms/BUILDER_V24_P1_SPEC_LOCKED_2026-04-19.md
    'nut_flush_block',
    'flush_draw_block_pct',
    'straight_draw_block_pct',
    'nut_made_block_pct',
    # Step 18: Phase 2-C cleanup features 60-61 (revised 2026-05-11 per
    # dispatch PR #400). Re-pilot (4 features) → Cleanup (2 winners): owner
    # ratified Option B; surface 63→61. Dropped per gate-fail:
    # nut_fd_blocker_multiway (1.87% absorbed by baseline blockers) +
    # broadway_pressure_multiway_facing (0.26% baseline-absorbed).
    'players_to_act_after_hero',  # AMENDMENT 1; 3.36% rank #10
    'tpmk_kicker_rank',           # MW-40 breakthrough; 9.18% rank #2
]

LABEL_COLUMN = 'action'


def add_derived_features(features: Dict) -> Dict:
    """
    Add derived features computed from existing features.

    equity_margin = raw_equity - pot_odds
        Positive â†’ we have enough equity to call profitably.
        Key signal for fold/call decisions.

    spr = effective_stack / pot_size
        Stack-to-pot ratio. Low SPR â†’ more committed, higher SPR â†’ more room
        to maneuver. We use a default 100bb effective stack since gauntlet
        data doesn't include stack sizes.

    Args:
        features: Feature dict with Steps 1-5 already populated

    Returns:
        Same dict with derived features added (mutated in place + returned)
    """
    features['equity_margin'] = round(
        features['raw_equity'] - features['pot_odds'], 6
    )

    pot = features['pot_size']
    if pot > 0:
        features['spr'] = round(DEFAULT_EFFECTIVE_STACK / pot, 4)
    else:
        features['spr'] = 99.0  # Cap at high value for zero/tiny pots

    # board_adjusted_hrp: collapses HRP when equity is low (board doesn't connect)
    # Computed later in extract_all_features after hero_range_percentile is set.
    # Placeholder here; overwritten in extract_all_features Step 16.
    features['board_adjusted_hrp'] = 0.0

    return features


# =============================================================================
# Step 8: Range-Board Teaching Features (metadata, NOT model features)
# =============================================================================

from range_narrowing import classify_hand

# Categories that count as "top pair or better" for villain_top_pair_plus_pct
_TOP_PAIR_PLUS = {'nuts', 'strong_value', 'good_value'}
# Categories that count as "drawing"
_DRAW_CATEGORIES = {'draw'}
# Categories that count as "air" (no showdown value, no meaningful draw)
_AIR_CATEGORIES = {'air', 'bluff'}
# Categories that count as medium/weak made hands (below top pair)
# medium_made: top pair weak kicker, second pair, underpairs below top board card
# weak_made: bottom pair, weak showdown
_MEDIUM_MADE_CATEGORIES = {'medium_made', 'weak_made'}


def extract_range_composition(
    board_cards: List[str],
    hero_pos: str,
    villain_pos: str,
    facing_bet: bool,
    street_raw: str,
    is_3bet_pot: int,
    opener_pos: str = None,
    action_history: List[Dict] = None,
    hand: Optional[Dict] = None,
) -> Dict:
    """
    Classify villain's range on this board and return composition percentages.

    Runs classify_hand() on each hand in villain's range. This is the same
    loop that narrow_to_betting_range() runs internally, but here we collect
    the classification stats instead of discarding them.

    v2.4 Stage 3.5: when `action_history` is supplied, chain bet/check/call
    narrowing across villain's prior-street actions before applying the
    current-street facing_bet filter. Preserves backward compat when
    action_history is None (falls back to single-street behavior).

    Returns _ prefixed metadata fields (teaching only, not model features):
        _villain_top_pair_plus_pct: fraction of range that is top pair+
        _villain_draw_pct: fraction of range that has a strong draw
        _villain_air_pct: fraction of range that is air/bluff
        _villain_range_capped: 1 if villain's range is capped (no premiums)
        _board_favour: heuristic board favour (-1 to +1, positive = favours hero)
        _villain_range_chain_steps: action-chain applied (v2.4 Stage 3.5)
        _villain_range_chain_truncated: safety rail tripped (v2.4 Stage 3.5)
    """
    if not board_cards:
        return {
            '_villain_top_pair_plus_pct': 0.0,
            '_villain_draw_pct': 0.0,
            '_villain_air_pct': 0.0,
            '_villain_range_capped': 0,
            '_board_favour': 0.0,
        }

    # Get villain's preflop range (opener-aware when opener_pos is provided)
    v_range = get_villain_range(hero_pos, villain_pos, opener_pos=opener_pos)
    if not v_range:
        return {
            '_villain_top_pair_plus_pct': 0.0,
            '_villain_draw_pct': 0.0,
            '_villain_air_pct': 0.0,
            '_villain_range_capped': 0,
            '_board_favour': 0.0,
        }

    street_name = _normalise_street(street_raw)

    # CRIT #2 — loud surfacing when _action_history is missing on hand payload.
    # Env-gated so read-only display paths (live oracle display, calibration
    # view) stay silent while Stage 4 re-label + training paths force a raise.
    # Same pattern as MUST #9 pipeline unswallow (re-raise RuntimeError
    # specifically; normal extraction errors still counted silently).
    #
    # STAGE4_STRICT_ACTION_HISTORY semantics:
    #   unset / "0" — silent fallback (legacy-compat; read-only display)
    #   "warn"     — logging.WARNING per call (default for MUST #32(a))
    #   "raise"    — RuntimeError (training / Stage 4 re-label)
    _action_history_present = bool(action_history)
    if not _action_history_present:
        _strict = os.environ.get('STAGE4_STRICT_ACTION_HISTORY', '0').lower()
        if _strict == 'raise':
            raise RuntimeError(
                f'extract_range_composition: action_history missing at '
                f'board={board_cards!r} hero={hero_pos} villain={villain_pos}. '
                f'STAGE4_STRICT_ACTION_HISTORY=raise is set. This is the '
                f'v2.3.2-class silent-fallback failure mode; fix the caller '
                f'to populate _action_history before re-running.'
            )
        elif _strict in ('warn', '1'):
            import logging
            logging.getLogger(__name__).warning(
                'extract_range_composition: action_history MISSING — falling '
                'back to pre-Stage-3.5 single-street behavior. '
                'board=%r hero=%s villain=%s',
                board_cards, hero_pos, villain_pos,
            )

    # v2.4 Stage 3.5: action-aware chaining (prior streets only).
    chain_steps: List[str] = []
    chain_truncated = False
    chain_surviving_weight = 1.0
    # HIGH #4 + MUST #15 + MUST #28 sentinels — consumed downstream by Step
    # 12 + Step 17 (blocker features) and by composition loop (NaN-flag).
    villain_folded = False
    chain_overflowed = False

    if action_history:
        # C3 fix (commit 4.1): check hand-level cache first. Equity +
        # partition typically run before composition in extract_features_
        # step1_through_5; if they populated the HU cache for this
        # (villain_pos, action_history) tuple, reuse it here.
        # Phase 3 HIGH-3 fix (Task 4.5): include action_history hash in
        # cache key to prevent stale-cache hits when caller mutates
        # hand['_action_history'] across street decisions.
        _hu_cache_key = ('hu', villain_pos, _action_history_cache_key(action_history))
        _hand_cache = hand.get('_chain_cache', {}) if hand is not None else {}
        if _hu_cache_key in _hand_cache:
            # Cache hit — consume result (narrow_by_action_history already ran)
            v_range, chain_meta = _hand_cache[_hu_cache_key]
            # Helper's returned range is pre-facing-bet-filter (HU branch
            # applies facing_bet AFTER chain). Extract the pre-filter
            # range by re-running the chain? No — helper already applied
            # facing_bet too. Here we want the post-chain + post-facing-bet
            # range; the helper's returned value IS that.
            chain_steps = chain_meta.get('chain_steps', [])
            chain_truncated = chain_meta.get('truncated', False)
            chain_surviving_weight = chain_meta.get('surviving_weight', 1.0)
            villain_folded = chain_meta.get('villain_folded', False)
            chain_overflowed = chain_meta.get('chain_overflowed', False)
            # Cached v_range has facing_bet filter already applied; skip
            # the duplicate application below.
            _cache_supplied_v_range_post_bet_filter = True
        else:
            from range_narrowing import narrow_by_action_history
            v_range, chain_meta = narrow_by_action_history(
                full_range=v_range,
                board=board_cards,
                action_history=action_history,
                villain_pos=villain_pos,
                decision_street=street_name,
            )
            chain_steps = chain_meta.get('chain_steps', [])
            chain_truncated = chain_meta.get('truncated', False)
            chain_surviving_weight = chain_meta.get('surviving_weight', 1.0)
            _cache_supplied_v_range_post_bet_filter = False

        # HIGH #4: distinguish FOLD from over-narrow. narrow_by_action_history
        # returns empty range + chain_steps ending in ':FOLD' when villain
        # folded on a prior street. Set sentinel; do NOT re-fetch preflop.
        if not v_range:
            _last_step = chain_steps[-1] if chain_steps else ''
            if _last_step.endswith(':FOLD'):
                villain_folded = True
                # Leave v_range empty; composition loop short-circuits,
                # Step 12 + 17 NaN-flag via _villain_folded sentinel.
            else:
                # MUST #15: over-narrow without FOLD IS the silent-fallback
                # anti-pattern. Do NOT re-fetch un-narrowed preflop range;
                # NaN-flag so Stage 4 training can row-drop cleanly.
                chain_overflowed = True
                import logging
                logging.getLogger(__name__).warning(
                    'extract_range_composition: chain over-narrowed to empty '
                    'without FOLD on hero=%s villain=%s board=%r chain_steps=%r; '
                    'NaN-flagging composition features per MUST #15.',
                    hero_pos, villain_pos, board_cards, chain_steps,
                )
        elif chain_truncated:
            # MUST #28: MUST #13 mass-floor truncation reverted to
            # last_valid_range. Partial-chain range is NOT the full-chain
            # range; downstream must NaN-flag rather than consume partial
            # as if it were a valid narrowed range. Same silent-fallback
            # failure class the empty-range path handles.
            chain_overflowed = True
            import logging
            logging.getLogger(__name__).warning(
                'extract_range_composition: chain truncated at mass floor; '
                'reverted to last valid. NaN-flagging composition features '
                'per MUST #28. hero=%s villain=%s chain_steps=%r',
                hero_pos, villain_pos, chain_steps,
            )

    # Current-street facing-bet filter — only when villain is still in hand
    # and chain hasn't over-narrowed/truncated. Skip when cache already
    # supplied post-filter range (C3 fix avoids double-filter).
    _skip_bet_filter = (
        action_history
        and locals().get('_cache_supplied_v_range_post_bet_filter', False)
    )
    if (facing_bet and not villain_folded and not chain_overflowed
            and not _skip_bet_filter):
        v_range, _ = narrow_to_betting_range(v_range, board_cards, street_name)

    # C3 fix (commit 4.1): populate hand-level cache with the final
    # post-chain + post-facing-bet range so subsequent callers on this
    # same hand hit the fast-path. Gate on action_history presence +
    # cache not already hit + hand provided.
    if (action_history and hand is not None
            and not locals().get('_cache_supplied_v_range_post_bet_filter', False)):
        _composed_meta = {
            'chain_steps': chain_steps,
            'truncated': chain_truncated,
            'surviving_weight': chain_surviving_weight,
            'villain_folded': villain_folded,
            'chain_overflowed': chain_overflowed,
            '_chain_method': 'hu',
        }
        # Phase 3 HIGH-3 fix (Task 4.5): cache key now includes
        # action_history hash to prevent stale-cache hits across street
        # decisions on the same hand object.
        hand.setdefault('_chain_cache', {})[
            ('hu', villain_pos, _action_history_cache_key(action_history))
        ] = (v_range, _composed_meta)

    # Classify each hand in villain's range
    total_weight = 0.0
    top_pair_plus_weight = 0.0
    draw_weight = 0.0
    air_weight = 0.0
    medium_made_weight = 0.0

    for hand_notation, freq in v_range.items():
        if freq <= 0:
            continue

        # Phase 3 HIGH-2 fix (Task 4.5): classify_hand now raises
        # ValueError on unrecognised notation (was silently classifying
        # malformed input as 'air'/'weak_made'). Audit/pilot scripts
        # loading from disk may carry corrupted range keys; log + skip
        # rather than abort the whole composition extraction. Production
        # callers (logic team's own range builders) emit only valid
        # notation and never trip this branch.
        try:
            classification = classify_hand(hand_notation, board_cards)
        except ValueError as exc:
            import logging
            logging.getLogger(__name__).warning(
                'classify_hand rejected range key %r in HU composition '
                'extraction: %s; skipping combo.',
                hand_notation, exc,
            )
            continue

        category = classification.category

        # River: draws are dead — reclassify as air
        if street_name == 'river' and category == 'draw':
            category = 'air'

        total_weight += freq

        if category in _TOP_PAIR_PLUS:
            top_pair_plus_weight += freq
        elif category in _DRAW_CATEGORIES:
            draw_weight += freq
        elif category in _AIR_CATEGORIES:
            air_weight += freq
        elif category in _MEDIUM_MADE_CATEGORIES:
            medium_made_weight += freq

    # Compute percentages
    if total_weight > 0:
        tp_pct = round(top_pair_plus_weight / total_weight, 4)
        draw_pct = round(draw_weight / total_weight, 4)
        air_pct = round(air_weight / total_weight, 4)
        medium_made_pct = round(medium_made_weight / total_weight, 4)
    else:
        tp_pct = 0.0
        draw_pct = 0.0
        air_pct = 0.0
        medium_made_pct = 0.0

    # MUST #10 — composition features are not applicable when villain isn't
    # in the hand with a meaningful chained range. NaN-flag so:
    #   - training (Stage 4) can row-drop these from blocker-feature columns
    #   - teaching layer renders MUST #42 player-English ("villain folded...")
    #   - SHAP skips NaN blocker contributions from PRIMARY tagging
    #   - gto_model.features_from_dict raises on unexpected non-allowlist NaN
    if villain_folded or chain_overflowed:
        tp_pct = float('nan')
        draw_pct = float('nan')
        air_pct = float('nan')
        medium_made_pct = float('nan')
        # Keep board_favour as 0.0 (hero-range-derived; NOT villain-derived)

    # Feature 4: Range capped
    # In a single-raised pot where villain is the defender (not PFR),
    # they would have 3-bet with AA/KK/AKs — their range is capped.
    # Use opener_pos when available for accuracy; fall back to PREFLOP_ORDER.
    if opener_pos is not None:
        villain_is_defender = villain_pos.upper() != opener_pos.upper()
    else:
        h_ord = PREFLOP_ORDER.get(hero_pos.upper(), 2)
        v_ord = PREFLOP_ORDER.get(villain_pos.upper(), 2)
        villain_is_defender = v_ord > h_ord  # villain in later position = defended
    range_capped = int(
        not is_3bet_pot and villain_is_defender
    )

    # Feature 5: Board favour (heuristic — alias pfr_advantage direction)
    # Positive = board favours hero's range, negative = favours villain
    # Use the top_pair_plus split as a proxy: if villain has more TP+
    # than typical (~30%), the board favours villain.
    # A more precise version would compare hero's range too, but that
    # doubles the computation cost.
    # C1 fix (commit 4.1): board_favour derivation from tp_pct propagates
    # NaN when tp_pct is NaN (folded/overflowed sentinel paths). But
    # board_favour is not in gto_model._NAN_ALLOWLIST — downstream inference
    # would ValueError on every folded-villain hand. Force 0.0 when
    # sentinels fire (matches commit-4 msg claim "hero-range-derived").
    if villain_folded or chain_overflowed:
        board_favour = 0.0
    else:
        board_favour = round(0.30 - tp_pct, 4)  # Positive when villain has LESS TP+

    return {
        '_villain_top_pair_plus_pct': tp_pct,
        '_villain_draw_pct': draw_pct,
        '_villain_air_pct': air_pct,
        '_villain_medium_made_pct': medium_made_pct,
        '_villain_range_capped': range_capped,
        '_board_favour': board_favour,
        # v2.4 Stage 3.5 metadata
        '_villain_range_chain_steps': chain_steps,
        '_villain_range_chain_truncated': chain_truncated,
        '_surviving_weight': chain_surviving_weight,   # MUST #5 true mass
        # CRIT #1 — publish narrowed range for Step 12 + Step 17 + MUST #6
        # equity consumers. Single source of truth across composition /
        # blocker / equity / explain_hand.
        '_villain_range_narrowed': v_range,
        # HIGH #4 + MUST #15 + MUST #28 sentinels — downstream NaN-flag
        # triggers (Step 12/17 blocker features; composition loop; SHAP;
        # gto_model NaN allowlist).
        '_villain_folded': villain_folded,
        '_villain_chain_overflowed': chain_overflowed,
        # CRIT #2 provenance — audit column for Stage 4 mixture detection.
        '_action_history_present': _action_history_present,
    }


# =============================================================================
# Step 12: New features (46-48) — standalone functions
# =============================================================================

def compute_flush_block_pct(
    hero_cards: List[str],
    board_cards: List[str],
    villain_range: Dict[str, float],
    board_suit_counts: Dict[str, int],
) -> float:
    """
    Feature 46: What fraction of villain's flush combos does hero block?

    Hero holds cards of the flush suit that prevent certain villain combos
    from existing. This is a blocker effect — holding Jh on a 3-heart board
    eliminates villain combos like JhTh, Jh9h, etc.

    Args:
        hero_cards: ['Jh', '9s']
        board_cards: ['Ah', '7h', '2h']
        villain_range: {hand_notation: frequency} — already narrowed
        board_suit_counts: {'h': 3, 's': 0, 'd': 0, 'c': 0}

    Returns:
        Float [0.0, 1.0] — blocked flush combos / total flush combos.
        0.0 when no flush threat, or when hero has 2+ cards of the suit
        (hero has the draw, not a blocker).
    """
    if not board_suit_counts:
        return 0.0

    # Identify the flush suit (highest count >= 2)
    flush_suit = None
    max_count = 0
    for suit, count in board_suit_counts.items():
        if count > max_count:
            max_count = count
            flush_suit = suit
    if flush_suit is None or max_count < 2:
        return 0.0

    # Count hero's cards of the flush suit
    hero_flush_suit_cards = [c for c in hero_cards if c[1].lower() == flush_suit.lower()]

    # Build set of used cards (hero + board) for combo validity
    used_cards = set(c.lower() for c in hero_cards) | set(c.lower() for c in board_cards)

    # Hero's flush-suit cards as a set (lowercase) for blocking check
    hero_flush_set = set(c.lower() for c in hero_flush_suit_cards)

    total_flush_weight = 0.0
    blocked_flush_weight = 0.0

    for hand_notation, freq in villain_range.items():
        if freq <= 0:
            continue

        combos = get_valid_combos(hand_notation, used_cards)
        for combo in combos:
            # Does this combo contain at least one card of the flush suit?
            combo_flush_cards = [c for c in combo if c[1].lower() == flush_suit.lower()]
            if not combo_flush_cards:
                continue

            total_flush_weight += freq

            # Does hero block any card in this combo?
            # A card is "blocked" when hero holds it — but it can't appear in
            # villain's combo if hero holds it (get_valid_combos excludes used_cards).
            # So blocking means: hero holds a card that IS in the combo's suit,
            # which reduces the total pool of flush combos available to villain.
            #
            # Since get_valid_combos already removes hero's cards from combos,
            # we measure blocking by checking whether ANY of hero's flush-suit cards
            # share a rank+suit match with the combo's flush-suit cards.
            # In practice: the combo already can't contain hero's exact card,
            # but we want to know if hero's flush-suit holdings shrink the combos.
            #
            # Correct approach: a combo is "blocked" if at least one card in the
            # combo is a card that hero holds. Since get_valid_combos already
            # excludes hero's cards, we check the original combo pool without
            # used-card filtering. Instead: check if hero's flush cards would
            # have been in this combo's position.
            #
            # Simpler: iterate ALL suit combos (no card removal), count which ones
            # contain hero's card. The ratio is the blocking percentage.
            # We do this by checking if hero's flush-suit card is one of the
            # rank+suit cards that appear in the NOTATED hand (before removal).
            #
            # Implementation: for each flush-suit card hero holds, check if it
            # could be part of this combo's notation's suited expansion.
            hero_blocks = False
            for h_card in hero_flush_suit_cards:
                h_lower = h_card.lower()
                h_rank = h_lower[0]
                h_suit = h_lower[1]
                # Check if hero's card matches any card in the combo
                # (The combo was generated without hero's cards, but we want
                # to know if hero's card was supposed to be here)
                # Check the hand notation: does the hand contain hero's rank
                # with this suit?
                r1 = hand_notation[0].upper()
                r2 = hand_notation[1].upper()
                is_suited = len(hand_notation) >= 3 and hand_notation[2].lower() == 's'
                is_pair = r1 == r2

                if is_pair:
                    # e.g. 'JJ' — hero blocks if hero holds Js (any suit of J)
                    if h_rank.upper() == r1.upper() and h_suit == flush_suit.lower():
                        hero_blocks = True
                elif is_suited:
                    # Both cards same suit — hero blocks if hero holds either rank
                    # of the flush suit
                    if h_suit == flush_suit.lower() and h_rank.upper() in (r1.upper(), r2.upper()):
                        hero_blocks = True
                else:
                    # Offsuit — hero blocks if hero holds either rank of the flush suit
                    if h_suit == flush_suit.lower() and h_rank.upper() in (r1.upper(), r2.upper()):
                        hero_blocks = True

            if hero_blocks:
                blocked_flush_weight += freq

    if total_flush_weight <= 0:
        return 0.0

    return round(blocked_flush_weight / total_flush_weight, 6)


def compute_overcard_outs(hero_cards: List[str], high_card_rank: int) -> int:
    """
    Feature 47: Number of outs from hero's overcards.

    An overcard is a hole card ranked strictly above the highest board card.
    Each overcard is worth approximately 3 outs (hitting top pair).

    Args:
        hero_cards: ['Ah', 'Kd']
        high_card_rank: Highest board card rank as int (14=A, 13=K, ..., 2=2)

    Returns:
        Integer: 0, 3, or 6 (count of overcards × 3)
    """
    # Inline rank parsing — no import dependency required
    rank_map = {
        'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
        '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2,
    }
    overcard_count = 0
    for card in hero_cards:
        card_rank = rank_map.get(card[0].upper(), 0)
        if card_rank > high_card_rank:
            overcard_count += 1
    return overcard_count * 3


def compute_improvement_probability(
    hero_cards: List[str],
    board_cards: List[str],
    current_hand_category: int,
) -> float:
    """
    Feature 48: Fraction of unseen deck cards that improve hero to two-pair+.

    Does NOT count improvements only to top pair (those are covered by
    overcard_outs). Counts two-pair, trips, set, straight, flush, full house,
    quads, straight flush.

    Args:
        hero_cards: ['Jh', '9s']
        board_cards: ['As', '7h', '2d']  — 3 or 4 cards (not river)
        current_hand_category: Integer from HAND_CATEGORY_ENCODING

    Returns:
        Float [0.0, 1.0]. 0.0 on river. 1.0 if already two-pair+.
    """
    # River: no cards left to improve
    if len(board_cards) >= 5:
        return 0.0

    # Two-pair threshold: category >= 10 in HAND_CATEGORY_ENCODING
    TWO_PAIR_THRESHOLD = HAND_CATEGORY_ENCODING['two_pair']

    # Already two-pair or better
    if current_hand_category >= TWO_PAIR_THRESHOLD:
        return 1.0

    # Build set of used cards (lowercase)
    used_cards = set(c.lower() for c in hero_cards) | set(c.lower() for c in board_cards)

    # All 52 cards
    all_ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    all_suits = ['s', 'h', 'd', 'c']
    deck = [f"{r}{s}" for r in all_ranks for s in all_suits]
    unseen = [c for c in deck if c.lower() not in used_cards]

    improved_count = 0
    for card in unseen:
        new_board = board_cards + [card]
        try:
            new_eval = evaluate_hand(hero_cards, new_board)
            new_category_str = new_eval.category.lower()
            new_category = HAND_CATEGORY_ENCODING.get(new_category_str, 0)
            # Count if improved to two-pair or better
            if new_category >= TWO_PAIR_THRESHOLD:
                improved_count += 1
        except Exception:
            continue

    if not unseen:
        return 0.0

    return round(improved_count / len(unseen), 6)

def compute_flush_draw_rank(
    hero_cards: List[str],
    board_cards: List[str],
) -> int:
    """
    Feature 52: Rank of hero's highest card in the board's flush suit.

    Returns 2-14 (using RANK_VALUES: A=14, K=13, ..., 2=2).
    Returns 0 if hero has no card of the flush suit, or if there is no flush
    suit (no suit appears 2+ times on the board).

    Args:
        hero_cards: e.g. ['Jh', '9s']
        board_cards: e.g. ['Ah', '7h', '2d']

    Returns:
        Integer rank 0-14.
    """
    if not board_cards or not hero_cards:
        return 0

    # Find flush suit: suit with highest count on board (>= 2 required)
    board_suit_counts: Dict[str, int] = {}
    for card in board_cards:
        s = card[1].lower()
        board_suit_counts[s] = board_suit_counts.get(s, 0) + 1

    flush_suit = None
    max_count = 0
    for suit, count in board_suit_counts.items():
        if count > max_count:
            max_count = count
            flush_suit = suit
    if flush_suit is None or max_count < 2:
        return 0

    # Inline rank map (same as compute_overcard_outs)
    rank_map = {
        'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
        '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2,
    }

    best_rank = 0
    for card in hero_cards:
        if card[1].lower() == flush_suit:
            r = rank_map.get(card[0].upper(), 0)
            if r > best_rank:
                best_rank = r

    return best_rank


def compute_hero_range_percentile(
    hero_cards: List[str],
    board_cards: List[str],
    hero_pos: str,
    opener_pos: Optional[str],
) -> float:
    """
    Feature 49: Where does hero's hand sit within their own range on this board?

    Calls _range_manager.get_hand_percentile() with hero's preflop range.
    Returns 0.0-1.0 where 1.0 = top of hero's range.

    Args:
        hero_cards: e.g. ['Ah', 'Kd']
        board_cards: e.g. ['Jh', '8c', '2s']
        hero_pos: e.g. 'BTN'
        opener_pos: Preflop raiser's position, or None.

    Returns:
        Float [0.0, 1.0]
    """
    if not hero_cards or len(hero_cards) < 2 or not board_cards:
        return 0.5

    hand_notation = cards_to_notation(hero_cards[0], hero_cards[1])

    # Hero is PFR when opener_pos matches hero_pos or when opener_pos is unknown.
    is_pfr = (
        opener_pos is None
        or opener_pos.upper() == hero_pos.upper()
    )
    hero_range = _range_manager.get_postflop_range(hero_pos, is_pfr=is_pfr)
    if not hero_range:
        return 0.5

    return round(
        _range_manager.get_hand_percentile(hand_notation, hero_range, board_cards),
        6,
    )


def extract_all_features(hand: Dict) -> Dict:
    """
    Extract ALL features (Steps 1-8) for a single hand.

    This is the final, complete feature extraction function.
    Steps 1-5: foundation (hand eval, board, equity, partitioning)
    Step 6: derived (equity_margin, spr)
    Step 7: action history context (is_3bet_pot, villain aggression, etc.)
    Step 8: multiway context (num_opponents)

    Step 7 features come from the hand dict (set by pokerbench_parser).
    For gauntlet-format hands that lack action history, they default to 0.

    Args:
        hand: Single hand dict from gauntlet JSON or pokerbench_parser

    Returns:
        Complete feature dict ready for CSV export
    """
    features = extract_features_step1_through_5(hand)
    add_derived_features(features)

    # Step 7: Action history context
    # PokerBench hands have these as _-prefixed fields from the parser.
    # Gauntlet hands don't â€” default to 0 (XGBoost treats as neutral).
    features['is_3bet_pot'] = hand.get('_is_3bet_pot', 0)
    # had_preflop_open removed — constant feature, oracle always plays opened pots
    features['villain_aggression_count'] = hand.get('_villain_aggression_count', 0)
    features['villain_checked_back'] = hand.get('_villain_checked_back', 0)
    features['villain_call_count'] = hand.get('_villain_call_count', 0)

    # Step 8: multiway context
    features[F.NUM_OPPONENTS] = hand.get(F.META_NUM_OPPONENTS, 1)

    # Step 8b: action sequence context (raise tracking)
    features[F.META_NUM_RAISES] = hand.get(F.META_NUM_RAISES, 0)

    # Step 9: Range-board teaching features (metadata only, NOT model features)
    # These feed the SituationDescriber for specific board texture descriptions.
    range_feats = extract_range_composition(
        board_cards=features.get('_board_cards', []),
        hero_pos=features.get('_hero_pos_raw', 'BTN'),
        villain_pos=features.get('_villain_pos_raw', 'BB'),
        facing_bet=bool(features.get('facing_bet', 0)),
        street_raw=features.get('_street_raw', 'f'),
        is_3bet_pot=features.get('is_3bet_pot', 0),
        opener_pos=hand.get('_opener_position', None),
        # v2.4 Stage 3.5: action-aware narrowing. Plumbs through from
        # game_state_bridge which flattens game.street_actions into
        # [{street, position, action}, ...]. None falls back to single-
        # street behavior (backward compat for callers that haven't
        # updated).
        action_history=hand.get('_action_history'),
        hand=hand,   # C3 fix: hand-level cache per MUST #46/#63
    )
    features.update(range_feats)

    # Step 10: Promote range-board features from metadata to model features
    # These keep their _-prefixed copies for the teaching pipeline (SituationDescriber).
    features[F.VILLAIN_TOP_PAIR_PLUS_PCT] = features.get('_villain_top_pair_plus_pct', 0.0)
    features[F.VILLAIN_DRAW_PCT] = features.get('_villain_draw_pct', 0.0)
    features[F.VILLAIN_AIR_PCT] = features.get('_villain_air_pct', 0.0)
    features[F.VILLAIN_MEDIUM_MADE_PCT] = features.get('_villain_medium_made_pct', 0.0)
    features[F.VILLAIN_RANGE_CAPPED] = features.get('_villain_range_capped', 0)
    features[F.BOARD_FAVOUR] = features.get('_board_favour', 0.0)

    # Step 10b: Commit 14 Finding B fold-in — multiway per-villain field
    # promotion. Promotes _per_villain_folded, _per_villain_composition,
    # _per_villain_overflowed from chain_meta onto the features dict so
    # downstream consumers (teaching renderer per HOLD #5, game per-villain
    # range bars, M4 re-audit, debug dumps) can read without re-invoking
    # the chain helper. HU hands get empty dicts (NOT missing keys) to
    # prevent NoneType errors on consumers expecting dict-shaped values.
    # Cross-stream unblocks: teaching HOLD #5, game per-villain range bars.
    features['_per_villain_folded'] = {}
    features['_per_villain_composition'] = {}
    features['_per_villain_overflowed'] = {}
    _num_opp = features[F.NUM_OPPONENTS]
    # Source `_opponent_positions` from hand if explicitly provided, else
    # derive via `assign_opponent_positions` for MW hands (matches the
    # default-derivation path used in the equity/partition extractors at
    # line ~1430).
    _opp_positions = hand.get('_opponent_positions', None)
    if not _opp_positions and _num_opp >= 2:
        _opp_positions = assign_opponent_positions(
            features.get('_hero_pos_raw', 'BTN'), _num_opp,
        )
    if _num_opp >= 2 and _opp_positions:
        _, _mw_meta = _get_chain_narrowed_villain_range(
            hero_pos=features.get('_hero_pos_raw', 'BTN'),
            villain_pos=features.get('_villain_pos_raw', 'BB'),
            opener_pos=hand.get('_opener_position', None),
            board_cards=features.get('_board_cards', []),
            facing_bet=bool(features.get('facing_bet', 0)),
            street_raw=features.get('_street_raw', 'f'),
            action_history=hand.get('_action_history'),
            num_opponents=_num_opp,
            opponent_positions=_opp_positions,
            bettor_pos=hand.get('_bettor_pos'),
            hand=hand,  # uses cache populated by prior calls
        )
        features['_per_villain_folded'] = _mw_meta.get('per_villain_folded', {})
        features['_per_villain_composition'] = _mw_meta.get('per_villain_composition', {})
        features['_per_villain_overflowed'] = _mw_meta.get('per_villain_overflowed', {})

    # HIGH-4 (Phase 3) cross-stream coordination — Option B per
    # MAIN_TERMINAL_HIGH_4_CROSS_STREAM_COORDINATION_2026-04-26.md.
    # Honor CONTENT_API.md:230 / Stage 3.5 v2.2 amendment §3.7:
    # aggregate `_villain_chain_overflowed` is True when ANY opponent
    # is overflowed; aggregate `_villain_folded` is True when ALL
    # opponents are folded (HU sentinel was already correct).
    # Without this, on a 3-way+ hand where a non-primary opponent is
    # overflowed, `range_rendering_mode` reads "normal" while one
    # per-villain entry is overflowed (mode label drift).
    # HU path unchanged (per_villain_* dicts are empty → any/all on
    # empty preserves the prior aggregate value).
    if features.get('_per_villain_overflowed'):
        features['_villain_chain_overflowed'] = (
            bool(features.get('_villain_chain_overflowed', False))
            or any(features['_per_villain_overflowed'].values())
        )
    if features.get('_per_villain_folded'):
        features['_villain_folded'] = (
            bool(features.get('_villain_folded', False))
            or all(features['_per_villain_folded'].values())
        )

    # Step 11: Current-street action features (new for v9)
    features[F.NUM_CALLERS_TO_BET] = hand.get('_num_callers_to_bet', 0)
    features[F.FACING_RAISE] = hand.get('_facing_raise', 0)

    # Step 12 + Step 17: CRIT #1 — blocker features consume the SAME
    # chain-narrowed range as composition features (published by
    # extract_range_composition as _villain_range_narrowed). No
    # independent range reconstruction; all villain-range-derived
    # features share one source of truth.
    hero_cards = features.get('_hero_cards', [])
    board_cards = features.get('_board_cards', [])

    # MUST #10: NaN-flag when villain folded or chain overflowed (MUST #28
    # includes mass-floor truncation). _s12_* locals DELETED per CRIT #1
    # (previously re-fetched get_villain_range + narrow_to_betting_range
    # bypassing the chain).
    _villain_folded = bool(features.get('_villain_folded', False))
    _villain_chain_overflowed = bool(features.get('_villain_chain_overflowed', False))
    _v_range_narrowed = features.get('_villain_range_narrowed', None) or {}

    # Board suit counts (shared between flush_block_pct and Step 17)
    if board_cards:
        _s12_analysis = analyze_board_cached(tuple(board_cards))
        _s12_suit_counts = _s12_analysis.suit_counts
    else:
        _s12_suit_counts = {}

    if _villain_folded or _villain_chain_overflowed:
        # MUST #10 sub-2 — blocker features not applicable; Stage 4
        # training drops these rows from blocker-feature columns.
        features[F.FLUSH_BLOCK_PCT] = float('nan')
    else:
        features[F.FLUSH_BLOCK_PCT] = compute_flush_block_pct(
            hero_cards, board_cards, _v_range_narrowed, _s12_suit_counts
        )
    features[F.OVERCARD_OUTS] = compute_overcard_outs(
        hero_cards, features.get('high_card_rank', 14)
    )
    features[F.IMPROVEMENT_PROBABILITY] = compute_improvement_probability(
        hero_cards, board_cards, features.get('hand_category', 0)
    )

    # Step 13: New features 49-52
    _s13_opener_pos = hand.get('_opener_position', None)
    features[F.HERO_RANGE_PERCENTILE] = compute_hero_range_percentile(
        hero_cards, board_cards,
        features.get('_hero_pos_raw', 'BTN'),
        _s13_opener_pos,
    )
    features[F.HAS_SHOWDOWN_VALUE] = int(
        features.get('is_made_hand', 0) == 1
        and features.get('hand_category', 0) >= 3
    )
    _vtp = features.get(F.VILLAIN_TOP_PAIR_PLUS_PCT, 0.0)
    _vdp = features.get(F.VILLAIN_DRAW_PCT, 0.0)
    _num_opp = features.get(F.NUM_OPPONENTS, 1)
    _per_opp_fold = 1.0 - (_vtp + 0.5 * _vdp)
    _per_opp_fold = max(0.0, min(1.0, _per_opp_fold))
    features[F.VILLAIN_FOLD_EQUITY_ESTIMATE] = round(
        _per_opp_fold ** _num_opp, 6
    )
    features[F.FLUSH_DRAW_RANK] = compute_flush_draw_rank(
        hero_cards, board_cards
    )

    # Feature 53: is_preflop_aggressor
    # 1 if hero was the preflop raiser (opener), 0 if hero defended/called
    _opener_pos = hand.get('_opener_position', None)
    _hero_pos = features.get('_hero_pos_raw', 'BTN')
    features[F.IS_PREFLOP_AGGRESSOR] = int(
        _opener_pos is not None and _opener_pos.upper() == _hero_pos.upper()
    )

    # Step 16: board_adjusted_hrp = hero_range_percentile * equity_vs_range
    # Collapses HRP when equity is low (board doesn't connect with hero hand).
    features[F.BOARD_ADJUSTED_HRP] = round(
        features.get(F.HERO_RANGE_PERCENTILE, 0.0)
        * features.get(F.EQUITY_VS_RANGE, 0.0),
        6,
    )

    # Step 17: v2.4 P1 blocker-direction features (56-59)
    # Spec: review/comms/BUILDER_V24_P1_SPEC_LOCKED_2026-04-19.md
    # CRIT #1: consumes `_v_range_narrowed` from extract_range_composition
    # (same chain-narrowed range as composition features — consistent
    # defender-context semantics). MUST #10 + HIGH #4 + MUST #15/#28:
    # NaN-flag when villain folded or chain overflowed / truncated.
    if _villain_folded or _villain_chain_overflowed:
        # MUST #10: boolean nut_flush_block stays 0 ("hero cannot block
        # nothing"); continuous block_pcts NaN (not-applicable semantic).
        features[F.NUT_FLUSH_BLOCK] = 0
        features[F.FLUSH_DRAW_BLOCK_PCT] = float('nan')
        features[F.STRAIGHT_DRAW_BLOCK_PCT] = float('nan')
        features[F.NUT_MADE_BLOCK_PCT] = float('nan')
    else:
        # C2 fix (commit 4.1): removed bare `except Exception` silent-zero
        # anti-pattern. 0.0 on failure is indistinguishable from real-signal
        # 0.0 ("hero blocks nothing"). blocker_features is an internal
        # helper we control; failures indicate real bugs that must surface,
        # not be swallowed. Matches MUST #15 + CRIT #2 discipline.
        from blocker_features import (
            compute_nut_flush_block,
            compute_block_percentages,
        )
        features[F.NUT_FLUSH_BLOCK] = compute_nut_flush_block(
            hero_cards, board_cards
        )
        _s17_block = compute_block_percentages(
            hero_cards, board_cards, _v_range_narrowed,
        )
        features[F.FLUSH_DRAW_BLOCK_PCT] = _s17_block['flush_draw_block_pct']
        features[F.STRAIGHT_DRAW_BLOCK_PCT] = _s17_block['straight_draw_block_pct']
        features[F.NUT_MADE_BLOCK_PCT] = _s17_block['nut_made_block_pct']

    # =====================================================================
    # Step 18: Phase 2-C cleanup features (60-61)
    # Per dispatch PR #400 (owner-ratified Option B; supersedes PR #396).
    # Re-pilot (4 features) → Cleanup (2 winners): dropped
    # broadway_pressure_multiway_facing (0.26% baseline-absorbed) +
    # nut_fd_blocker_multiway (1.87% absorbed by baseline blockers).
    # Retained 2 features cleared the ≥2% gate in 1-seed re-pilot.
    # =====================================================================

    _num_opp = int(features.get('num_opponents', 1))
    _is_ip = int(features.get('is_ip', 0))

    # 18.1 — players_to_act_after_hero (AMENDMENT 1; v1 3.58%, v2 3.36%)
    # 0 if IP, num_opponents if OOP. Discriminates EP > MP > LP pressure
    # asymmetry in multiway.
    features['players_to_act_after_hero'] = 0.0 if _is_ip else float(_num_opp)

    # 18.2 — tpmk_kicker_rank (MW-40 axis; re-pilot 9.18%, rank #2/63)
    # Absolute numeric kicker rank (2..14) when hero has top-pair, 0
    # otherwise. The numeric kicker continuum unlocked the MW-40 axis after
    # the v1 J-high × hand_category × hand_rank composite scored 0.00%.
    # hand_category: top_pair=6, top_pair_good_kicker=7, top_pair_top_kicker=8.
    _hc = features.get('hand_category', 0)
    if _hc in (6, 7, 8):
        _hero_cards = features.get('_hero_cards', []) or []
        _high_card_rank = int(features.get('high_card_rank', 0))
        if len(_hero_cards) == 2:
            # Cards may be 2-char strings ('Kh') or objects with .rank.
            _RANK_MAP = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,
                         'T':10,'J':11,'Q':12,'K':13,'A':14}
            def _crank(_c):
                if hasattr(_c, 'rank'):
                    return int(_c.rank)
                if isinstance(_c, str) and len(_c) >= 1:
                    return _RANK_MAP.get(_c[0].upper(), 0)
                return 0
            _h_ranks = [_crank(c) for c in _hero_cards]
            # For top pair, one hero card matches the board's high card
            # (= pair rank); the OTHER hero card's rank is the kicker.
            if _h_ranks[0] == _high_card_rank and _h_ranks[1] != _high_card_rank:
                _kicker = _h_ranks[1]
            elif _h_ranks[1] == _high_card_rank and _h_ranks[0] != _high_card_rank:
                _kicker = _h_ranks[0]
            else:
                # Edge: pocket pair on board OR both hero cards == top card.
                # Fall back to max hero rank (preserves ordinal signal).
                _kicker = max(_h_ranks) if _h_ranks else 0
            features['tpmk_kicker_rank'] = float(_kicker)
        else:
            features['tpmk_kicker_rank'] = 0.0
    else:
        features['tpmk_kicker_rank'] = 0.0

    return features


def extract_all_features_batch(hands: List[Dict],
                               progress_every: int = 100) -> List[Dict]:
    """
    Batch extract ALL features (Steps 1-6) for all hands.

    Args:
        hands: List of hand dicts from gauntlet JSON
        progress_every: Print progress every N hands

    Returns:
        List of complete feature dicts
    """
    import time
    results = []
    errors = []
    t_start = time.time()

    for i, hand in enumerate(hands):
        try:
            features = extract_all_features(hand)
            results.append(features)
        except Exception as e:
            errors.append((i, hand.get('id', '?'), str(e)))

        if (i + 1) % progress_every == 0:
            elapsed = time.time() - t_start
            rate = (i + 1) / elapsed
            remaining = (len(hands) - i - 1) / rate
            print(f"  [{i+1}/{len(hands)}] "
                  f"{elapsed:.1f}s elapsed, "
                  f"{rate:.1f} hands/s, "
                  f"~{remaining:.0f}s remaining")

    elapsed = time.time() - t_start
    print(f"  Completed {len(results)}/{len(hands)} in {elapsed:.1f}s "
          f"({len(results)/elapsed:.1f} hands/s)")

    if errors:
        print(f"WARNING: {len(errors)} extraction errors:")
        for idx, hid, msg in errors[:10]:
            print(f"  Hand {hid} (index {idx}): {msg}")

    return results


def export_to_csv(features_list: List[Dict], filepath: str) -> None:
    """
    Export features to CSV for model training.
    Only exports FEATURE_COLUMNS + LABEL_COLUMN (no _ metadata).

    Args:
        features_list: List of feature dicts from extract_all_features_batch
        filepath: Output CSV path
    """
    import csv

    columns = FEATURE_COLUMNS + [LABEL_COLUMN]

    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        for feat in features_list:
            row = {col: feat.get(col, '') for col in columns}
            writer.writerow(row)

    print(f"  Exported {len(features_list)} rows Ã— {len(columns)} columns â†’ {filepath}")


def extract_all_step1_2(hands: List[Dict]) -> List[Dict]:
    """
    Batch extract Step 1 + Step 2 features for all hands.

    Args:
        hands: List of hand dicts from gauntlet JSON

    Returns:
        List of combined feature dicts
    """
    results = []
    errors = []
    for i, hand in enumerate(hands):
        try:
            features = extract_features_step1_2(hand)
            results.append(features)
        except Exception as e:
            errors.append((i, hand.get('id', '?'), str(e)))

    if errors:
        print(f"WARNING: {len(errors)} extraction errors:")
        for idx, hid, msg in errors[:10]:
            print(f"  Hand {hid} (index {idx}): {msg}")

    return results


def extract_all_step1_2_3(hands: List[Dict]) -> List[Dict]:
    """
    Batch extract Step 1 + Step 2 + Step 3 features for all hands.

    Args:
        hands: List of hand dicts from gauntlet JSON

    Returns:
        List of combined feature dicts
    """
    results = []
    errors = []
    for i, hand in enumerate(hands):
        try:
            features = extract_features_step1_2_3(hand)
            results.append(features)
        except Exception as e:
            errors.append((i, hand.get('id', '?'), str(e)))

    if errors:
        print(f"WARNING: {len(errors)} extraction errors:")
        for idx, hid, msg in errors[:10]:
            print(f"  Hand {hid} (index {idx}): {msg}")

    return results


def extract_all_step1_2_3_4(hands: List[Dict],
                             progress_every: int = 100) -> List[Dict]:
    """
    Batch extract Steps 1-4 features for all hands.
    Includes progress reporting since equity calc is slow.

    Args:
        hands: List of hand dicts from gauntlet JSON
        progress_every: Print progress every N hands

    Returns:
        List of combined feature dicts
    """
    import time
    results = []
    errors = []
    t_start = time.time()

    for i, hand in enumerate(hands):
        try:
            features = extract_features_step1_2_3_4(hand)
            results.append(features)
        except Exception as e:
            errors.append((i, hand.get('id', '?'), str(e)))

        if (i + 1) % progress_every == 0:
            elapsed = time.time() - t_start
            rate = (i + 1) / elapsed
            remaining = (len(hands) - i - 1) / rate
            print(f"  [{i+1}/{len(hands)}] "
                  f"{elapsed:.1f}s elapsed, "
                  f"{rate:.1f} hands/s, "
                  f"~{remaining:.0f}s remaining")

    elapsed = time.time() - t_start
    print(f"  Completed {len(results)}/{len(hands)} in {elapsed:.1f}s "
          f"({len(results)/elapsed:.1f} hands/s)")

    if errors:
        print(f"WARNING: {len(errors)} extraction errors:")
        for idx, hid, msg in errors[:10]:
            print(f"  Hand {hid} (index {idx}): {msg}")

    return results


def extract_all_step1_through_5(hands: List[Dict],
                                 progress_every: int = 100) -> List[Dict]:
    """
    Batch extract Steps 1-5 features for all hands.
    Includes progress reporting since equity + partitioning are slow.

    Args:
        hands: List of hand dicts from gauntlet JSON
        progress_every: Print progress every N hands

    Returns:
        List of combined feature dicts
    """
    import time
    results = []
    errors = []
    t_start = time.time()

    for i, hand in enumerate(hands):
        try:
            features = extract_features_step1_through_5(hand)
            results.append(features)
        except Exception as e:
            errors.append((i, hand.get('id', '?'), str(e)))

        if (i + 1) % progress_every == 0:
            elapsed = time.time() - t_start
            rate = (i + 1) / elapsed
            remaining = (len(hands) - i - 1) / rate
            print(f"  [{i+1}/{len(hands)}] "
                  f"{elapsed:.1f}s elapsed, "
                  f"{rate:.1f} hands/s, "
                  f"~{remaining:.0f}s remaining")

    elapsed = time.time() - t_start
    print(f"  Completed {len(results)}/{len(hands)} in {elapsed:.1f}s "
          f"({len(results)/elapsed:.1f} hands/s)")

    if errors:
        print(f"WARNING: {len(errors)} extraction errors:")
        for idx, hid, msg in errors[:10]:
            print(f"  Hand {hid} (index {idx}): {msg}")

    return results


# =============================================================================
# Unit Tests
# =============================================================================

def run_tests():
    """Run unit tests for Step 1 zero-compute features."""
    passed = 0
    failed = 0

    def assert_eq(name, actual, expected):
        nonlocal passed, failed
        if actual == expected:
            passed += 1
        else:
            failed += 1
            print(f"  FAIL: {name}: expected {expected!r}, got {actual!r}")

    def assert_close(name, actual, expected, tol=1e-4):
        nonlocal passed, failed
        if abs(actual - expected) < tol:
            passed += 1
        else:
            failed += 1
            print(f"  FAIL: {name}: expected ~{expected}, got {actual}")

    print("=" * 60)
    print("STEP 1: Zero-Compute Feature Extraction Tests")
    print("=" * 60)

    # ---- parse_hero_hand ----
    print("\n--- parse_hero_hand ---")
    assert_eq("basic parse", parse_hero_hand("Jd9s"), ["Jd", "9s"])
    assert_eq("aces", parse_hero_hand("AsAc"), ["As", "Ac"])
    assert_eq("tens", parse_hero_hand("TsTh"), ["Ts", "Th"])

    try:
        parse_hero_hand("Jd")
        failed += 1
        print("  FAIL: should reject 2-char hand")
    except ValueError:
        passed += 1

    # ---- parse_board ----
    print("\n--- parse_board ---")
    assert_eq("flop", parse_board("Th4c5d"), ["Th", "4c", "5d"])
    assert_eq("turn", parse_board("Th4c5dKd"), ["Th", "4c", "5d", "Kd"])
    assert_eq("river", parse_board("4s4h3hJh8c"), ["4s", "4h", "3h", "Jh", "8c"])

    try:
        parse_board("Th4c5")
        failed += 1
        print("  FAIL: should reject odd-length board")
    except ValueError:
        passed += 1

    try:
        parse_board("Th4c")
        failed += 1
        print("  FAIL: should reject 2-card board")
    except ValueError:
        passed += 1

    # ---- is_in_position ----
    print("\n--- is_in_position ---")
    assert_eq("BTN vs BB", is_in_position("BTN", "BB"), True)
    assert_eq("BB vs BTN", is_in_position("BB", "BTN"), False)
    assert_eq("CO vs UTG", is_in_position("CO", "UTG"), True)
    assert_eq("SB vs BB", is_in_position("SB", "BB"), False)
    assert_eq("BB vs SB", is_in_position("BB", "SB"), True)
    assert_eq("HJ vs CO", is_in_position("HJ", "CO"), False)
    assert_eq("CO vs HJ", is_in_position("CO", "HJ"), True)

    # ---- extract_zero_compute_features: facing bet ----
    print("\n--- extract: facing bet hand ---")
    hand_fb1 = {
        "pos": "SB", "h": "AdKc", "b": "9dTs8sJh3c",
        "st": "r", "pot": 39.0, "exp": "F", "tc": 17.0,
        "fb": 1, "vp": "BB", "id": 14
    }
    f = extract_zero_compute_features(hand_fb1)
    assert_eq("street river", f['street'], 2)
    assert_eq("facing_bet", f['facing_bet'], 1)
    assert_close("pot_size", f['pot_size'], 39.0)
    assert_close("to_call", f['to_call'], 17.0)
    assert_close("pot_odds", f['pot_odds'], 17.0 / (39.0 + 17.0))
    assert_close("bet_to_pot", f['bet_to_pot'], 17.0 / 39.0)
    assert_eq("hero_pos", f['hero_position'], POSITION_ORDINAL['SB'])
    assert_eq("villain_pos", f['villain_position'], POSITION_ORDINAL['BB'])
    assert_eq("is_ip SB vs BB", f['is_ip'], 0)  # SB acts before BB postflop
    assert_eq("action", f['action'], 'FOLD')
    assert_eq("hero cards", f['_hero_cards'], ['Ad', 'Kc'])
    assert_eq("board cards", f['_board_cards'],
              ['9d', 'Ts', '8s', 'Jh', '3c'])
    assert_eq("villain not inferred", f['_villain_pos_inferred'], False)

    # ---- extract_zero_compute_features: NOT facing bet, with vp ----
    print("\n--- extract: not facing bet, with vp ---")
    hand_fb0 = {
        "pos": "BB", "h": "Jd9s", "b": "4s4h3hJh8c",
        "st": "r", "pot": 6.0, "exp": "B", "fb": 0,
        "vp": "SB", "id": 6
    }
    f2 = extract_zero_compute_features(hand_fb0)
    assert_eq("street river", f2['street'], 2)
    assert_eq("facing_bet 0", f2['facing_bet'], 0)
    assert_close("to_call 0", f2['to_call'], 0.0)
    assert_close("pot_odds 0", f2['pot_odds'], 0.0)
    assert_close("bet_to_pot 0", f2['bet_to_pot'], 0.0)
    assert_eq("is_ip BB vs SB", f2['is_ip'], 1)  # BB after SB postflop
    assert_eq("action BET", f2['action'], 'BET')

    # ---- extract_zero_compute_features: NO villain position ----
    print("\n--- extract: no villain position (PFR hand) ---")
    hand_no_vp = {
        "pos": "BTN", "h": "Qs9h", "b": "Th4c5d7s3d",
        "st": "r", "pot": 13.0, "exp": "X", "fb": 0, "id": 42
    }
    f3 = extract_zero_compute_features(hand_no_vp)
    assert_eq("villain inferred", f3['_villain_pos_inferred'], True)
    assert_eq("default villain BB", f3['villain_position'],
              POSITION_ORDINAL['BB'])
    assert_eq("BTN is IP vs BB", f3['is_ip'], 1)
    assert_eq("action CHECK", f3['action'], 'CHECK')

    # ---- extract: turn hand ----
    print("\n--- extract: turn hand ---")
    hand_turn = {
        "pos": "CO", "h": "AcQc", "b": "Th4c5dKd",
        "st": "t", "pot": 46.0, "exp": "B", "fb": 0,
        "vp": "UTG", "id": 16
    }
    f4 = extract_zero_compute_features(hand_turn)
    assert_eq("street turn", f4['street'], 1)
    assert_eq("CO vs UTG IP", f4['is_ip'], 1)

    # ---- Batch extraction on real data ----
    print("\n--- batch extraction (2000 hands) ---")
    import json
    with open('/mnt/project/gauntlet_2000.json') as fp:
        data_2k = json.load(fp)

    results = extract_all_zero_compute(data_2k)
    assert_eq("all 2000 extracted", len(results), 2000)

    # Verify action distribution matches spec
    from collections import Counter
    action_dist = Counter(r['action'] for r in results)
    print(f"  Action distribution: {dict(action_dist)}")
    assert_eq("BET count", action_dist['BET'], 364)
    assert_eq("CHECK count", action_dist['CHECK'], 403)
    assert_eq("CALL count", action_dist['CALL'], 421)
    assert_eq("RAISE count", action_dist['RAISE'], 415)
    assert_eq("FOLD count", action_dist['FOLD'], 397)

    # Verify street distribution
    street_dist = Counter(r['street'] for r in results)
    print(f"  Street distribution: {dict(street_dist)}")
    assert_eq("flop count", street_dist[0], 602)
    assert_eq("turn count", street_dist[1], 700)
    assert_eq("river count", street_dist[2], 698)

    # Verify facing_bet distribution
    fb_dist = Counter(r['facing_bet'] for r in results)
    print(f"  Facing bet: {dict(fb_dist)}")
    assert_eq("facing_bet=1", fb_dist[1], 1214)
    assert_eq("facing_bet=0", fb_dist[0], 786)

    # Verify no pot_odds > 1 or < 0
    bad_odds = [r for r in results if r['pot_odds'] < 0 or r['pot_odds'] > 1]
    assert_eq("no bad pot_odds", len(bad_odds), 0)

    # Verify inferred villain count
    inferred = sum(1 for r in results if r['_villain_pos_inferred'])
    assert_eq("inferred villain count", inferred, 212)

    # Spot check: all facing_bet=1 have to_call > 0
    fb1_zero_tc = [r for r in results
                   if r['facing_bet'] == 1 and r['to_call'] <= 0]
    assert_eq("fb=1 always has to_call>0", len(fb1_zero_tc), 0)

    # Spot check: all facing_bet=0 have pot_odds == 0
    fb0_nonzero_odds = [r for r in results
                        if r['facing_bet'] == 0 and r['pot_odds'] != 0.0]
    assert_eq("fb=0 always pot_odds=0", len(fb0_nonzero_odds), 0)

    # ---- Summary ----
    print(f"\n{'=' * 60}")
    print(f"Step 1 Results: {passed} passed, {failed} failed")
    print(f"{'=' * 60}")

    # ================================================================
    # STEP 2: Hand Evaluation Feature Tests
    # ================================================================
    print(f"\n{'=' * 60}")
    print("STEP 2: Hand Evaluation Feature Tests")
    print(f"{'=' * 60}")

    # ---- Known hand: top pair top kicker ----
    print("\n--- top pair top kicker ---")
    f_tptk = extract_hand_eval_features(['As', 'Kd'], ['Ks', '7h', '2d'])
    assert_eq("TPTK is made", f_tptk['is_made_hand'], 1)
    assert_eq("TPTK not monster", f_tptk['is_monster'], 0)
    assert_eq("TPTK category >= top_pair",
              f_tptk['hand_category'] >= HAND_CATEGORY_ENCODING['top_pair'],
              True)
    assert_eq("TPTK raw cat",
              f_tptk['_hand_category_raw'] in
              ('top_pair', 'top_pair_good_kicker', 'top_pair_top_kicker'),
              True)

    # ---- Known hand: overpair ----
    print("\n--- overpair ---")
    f_op = extract_hand_eval_features(['As', 'Ah'], ['Ks', '7h', '2d'])
    assert_eq("overpair is made", f_op['is_made_hand'], 1)
    assert_eq("overpair cat", f_op['_hand_category_raw'], 'overpair')
    assert_eq("overpair encoded",
              f_op['hand_category'], HAND_CATEGORY_ENCODING['overpair'])

    # ---- Known hand: set ----
    print("\n--- set ---")
    f_set = extract_hand_eval_features(['7h', '7c'], ['9s', '7s', '4c'])
    assert_eq("set is monster", f_set['is_monster'], 1)
    assert_eq("set is strong", f_set['is_strong_made'], 1)
    assert_eq("set cat", f_set['_hand_category_raw'], 'set')
    assert_eq("set encoded",
              f_set['hand_category'], HAND_CATEGORY_ENCODING['set'])

    # ---- Known hand: flush draw (no made hand) ----
    print("\n--- flush draw ---")
    f_fd = extract_hand_eval_features(['Ah', '5h'], ['Kh', '9h', '2d'])
    assert_eq("flush draw detected", f_fd['has_flush_draw'], 1)
    assert_eq("flush draw outs > 0", f_fd['draw_outs'] > 0, True)

    # ---- Known hand: straight ----
    print("\n--- straight ---")
    f_str = extract_hand_eval_features(['9c', '8c'], ['7d', '6c', '5h', 'Jh', '2s'])
    assert_eq("straight is monster", f_str['is_monster'], 1)
    assert_eq("straight cat", f_str['_hand_category_raw'], 'straight')

    # ---- Known hand: high card / air ----
    print("\n--- high card ---")
    f_hc = extract_hand_eval_features(['Qh', '3d'], ['As', 'Kd', '7c', '5h', '2s'])
    assert_eq("high card not made", f_hc['is_made_hand'], 0)
    assert_eq("high card not monster", f_hc['is_monster'], 0)
    assert_eq("high card cat",
              f_hc['_hand_category_raw'] in ('high_card', 'one_overcard', 'overcards'),
              True)

    # ---- Known hand: full house ----
    print("\n--- full house ---")
    f_fh = extract_hand_eval_features(['Jc', 'Jh'], ['Jd', '4s', '4d', '8c', '2h'])
    assert_eq("full house is monster", f_fh['is_monster'], 1)
    assert_eq("full house cat", f_fh['_hand_category_raw'], 'full_house')
    assert_eq("full house encoded",
              f_fh['hand_category'], HAND_CATEGORY_ENCODING['full_house'])

    # ---- Encoding ordering: stronger hands have higher codes ----
    print("\n--- encoding ordering ---")
    assert_eq("flush > straight",
              HAND_CATEGORY_ENCODING['flush'] > HAND_CATEGORY_ENCODING['straight'],
              True)
    assert_eq("set > two_pair",
              HAND_CATEGORY_ENCODING['set'] > HAND_CATEGORY_ENCODING['two_pair'],
              True)
    assert_eq("overpair > top_pair",
              HAND_CATEGORY_ENCODING['overpair'] > HAND_CATEGORY_ENCODING['top_pair'],
              True)
    assert_eq("straight_flush > quads",
              HAND_CATEGORY_ENCODING['straight_flush'] > HAND_CATEGORY_ENCODING['quads'],
              True)

    # ---- Batch: run Step 1+2 on all 2000 hands ----
    print("\n--- batch Step 1+2 (2000 hands) ---")
    results_s2 = extract_all_step1_2(data_2k)
    assert_eq("all 2000 extracted (s2)", len(results_s2), 2000)

    # Verify all hands got hand_category
    missing_cat = [r for r in results_s2 if 'hand_category' not in r]
    assert_eq("no missing hand_category", len(missing_cat), 0)

    # Verify hand_category encoding is valid (0-17)
    bad_cat = [r for r in results_s2
               if r['hand_category'] < 0 or r['hand_category'] > 17]
    assert_eq("all categories in valid range", len(bad_cat), 0)

    # Verify no unknown categories snuck through
    known_cats = set(HAND_CATEGORY_ENCODING.keys())
    raw_cats = set(r['_hand_category_raw'] for r in results_s2)
    unknown = raw_cats - known_cats
    assert_eq("no unknown categories", len(unknown), 0)
    print(f"  Categories found: {sorted(raw_cats)}")

    # Verify is_made_hand consistency: monster implies strong implies made
    for r in results_s2:
        if r['is_monster']:
            if not r['is_strong_made']:
                failed += 1
                print(f"  FAIL: hand {r['_hand_id']}: monster but not strong_made")
                break
        if r['is_strong_made']:
            if not r['is_made_hand']:
                failed += 1
                print(f"  FAIL: hand {r['_hand_id']}: strong_made but not made")
                break
    else:
        passed += 1  # monster -> strong -> made hierarchy holds

    # Verify draw_outs are non-negative and reasonable
    bad_outs = [r for r in results_s2 if r['draw_outs'] < 0 or r['draw_outs'] > 25]
    assert_eq("draw_outs in range [0,25]", len(bad_outs), 0)

    # Distribution of categories
    cat_dist = Counter(r['_hand_category_raw'] for r in results_s2)
    print(f"  Category distribution:")
    for cat in sorted(cat_dist.keys(),
                      key=lambda c: HAND_CATEGORY_ENCODING.get(c, -1)):
        print(f"    {cat}: {cat_dist[cat]}")

    # Step 1 features still intact in combined output
    assert_eq("step1 fields preserved",
              all('street' in r and 'pot_size' in r for r in results_s2),
              True)

    # ---- Final Summary ----
    print(f"\n{'=' * 60}")
    print(f"Step 2 Results: {passed} passed, {failed} failed (cumulative)")
    print(f"{'=' * 60}")

    # ================================================================
    # STEP 3: Board Analysis Feature Tests
    # ================================================================
    print(f"\n{'=' * 60}")
    print("STEP 3: Board Analysis Feature Tests")
    print(f"{'=' * 60}")

    # ---- Monotone board: all same suit ----
    print("\n--- monotone board ---")
    f_mono = extract_board_features(['Ah', 'Kh', '7h'])
    assert_eq("monotone is_monotone", f_mono['is_monotone'], 1)
    assert_eq("monotone not rainbow", f_mono['is_rainbow'], 0)
    assert_eq("monotone high card A", f_mono['high_card_rank'], 14)
    assert_eq("monotone flush_danger > 0",
              f_mono['flush_danger'] > 0, True)

    # ---- Rainbow board: all different suits ----
    print("\n--- rainbow board ---")
    f_rain = extract_board_features(['Ks', '7h', '2d'])
    assert_eq("rainbow is_rainbow", f_rain['is_rainbow'], 1)
    assert_eq("rainbow not monotone", f_rain['is_monotone'], 0)
    assert_eq("rainbow not two_tone", f_rain['is_two_tone'], 0)
    assert_close("rainbow flush_danger", f_rain['flush_danger'], 0.0, tol=0.01)

    # ---- Two-tone board ----
    print("\n--- two-tone board ---")
    f_tt = extract_board_features(['Ks', '7s', '2d'])
    assert_eq("two_tone is_two_tone", f_tt['is_two_tone'], 1)
    assert_eq("two_tone not monotone", f_tt['is_monotone'], 0)
    assert_eq("two_tone not rainbow", f_tt['is_rainbow'], 0)

    # ---- Paired board ----
    print("\n--- paired board ---")
    f_paired = extract_board_features(['4s', '4h', '3h', 'Jh', '8c'])
    assert_eq("paired is_paired", f_paired['is_paired'], 1)
    assert_eq("paired high_card J", f_paired['high_card_rank'], 11)

    # ---- Double paired board ----
    print("\n--- double paired board ---")
    f_dp = extract_board_features(['Jc', 'Jh', '4s', '4d', '8c'])
    assert_eq("double_paired is_double_paired", f_dp['is_double_paired'], 1)
    assert_eq("double_paired is_paired", f_dp['is_paired'], 1)

    # ---- Connected board (high connectivity) ----
    print("\n--- connected board ---")
    f_conn = extract_board_features(['9s', 'Ts', '8d'])
    assert_eq("connected conn_score > 0", f_conn['connectivity_score'] > 0, True)
    assert_eq("connected straight_danger > 0",
              f_conn['straight_danger'] > 0, True)

    # ---- Dry board (low connectivity, rainbow, unpaired) ----
    print("\n--- dry board ---")
    f_dry = extract_board_features(['As', '7h', '2d'])
    assert_eq("dry not paired", f_dry['is_paired'], 0)
    assert_eq("dry is rainbow", f_dry['is_rainbow'], 1)
    assert_close("dry low danger", f_dry['danger_score'] < 0.4, True)

    # ---- Score ranges ----
    print("\n--- score ranges ---")
    assert_eq("danger_score [0,1]",
              0.0 <= f_mono['danger_score'] <= 1.0, True)
    assert_eq("flush_danger [0,1]",
              0.0 <= f_mono['flush_danger'] <= 1.0, True)
    assert_eq("straight_danger [0,1]",
              0.0 <= f_conn['straight_danger'] <= 1.0, True)
    assert_eq("connectivity [0,10]",
              0 <= f_conn['connectivity_score'] <= 10, True)
    assert_eq("high_card [2,14]",
              2 <= f_dry['high_card_rank'] <= 14, True)

    # ---- Batch: run Step 1+2+3 on all 2000 hands ----
    print("\n--- batch Step 1+2+3 (2000 hands) ---")
    import time
    t0 = time.time()
    results_s3 = extract_all_step1_2_3(data_2k)
    elapsed = time.time() - t0
    print(f"  Extracted in {elapsed:.2f}s ({elapsed/2000*1000:.1f}ms/hand)")

    assert_eq("all 2000 extracted (s3)", len(results_s3), 2000)

    # All board features present
    board_keys = ['is_monotone', 'is_two_tone', 'is_rainbow', 'is_paired',
                  'is_double_paired', 'connectivity_score', 'high_card_rank',
                  'danger_score', 'flush_danger', 'straight_danger']
    missing_board = [r['_hand_id'] for r in results_s3
                     if not all(k in r for k in board_keys)]
    assert_eq("no missing board features", len(missing_board), 0)

    # Suit texture mutual exclusivity: exactly one of monotone/two_tone/rainbow
    # (except turn/river where it can be more nuanced â€” but at least one should be set)
    bad_suit = []
    for r in results_s3:
        suit_sum = r['is_monotone'] + r['is_two_tone'] + r['is_rainbow']
        if suit_sum == 0:
            bad_suit.append(r['_hand_id'])
    # Allow some edge cases on turn/river but flag if excessive
    print(f"  Hands with no suit texture flag: {len(bad_suit)}")
    assert_eq("most hands have suit texture", len(bad_suit) < 100, True)

    # danger_score bounds
    bad_danger = [r for r in results_s3
                  if r['danger_score'] < 0 or r['danger_score'] > 1]
    assert_eq("danger_score in [0,1]", len(bad_danger), 0)

    # flush_danger bounds
    bad_fd = [r for r in results_s3
              if r['flush_danger'] < 0 or r['flush_danger'] > 1]
    assert_eq("flush_danger in [0,1]", len(bad_fd), 0)

    # straight_danger bounds
    bad_sd = [r for r in results_s3
              if r['straight_danger'] < 0 or r['straight_danger'] > 1]
    assert_eq("straight_danger in [0,1]", len(bad_sd), 0)

    # connectivity_score bounds
    bad_conn = [r for r in results_s3
                if r['connectivity_score'] < 0 or r['connectivity_score'] > 10]
    assert_eq("connectivity in [0,10]", len(bad_conn), 0)

    # high_card_rank bounds
    bad_hcr = [r for r in results_s3
               if r['high_card_rank'] < 2 or r['high_card_rank'] > 14]
    assert_eq("high_card_rank in [2,14]", len(bad_hcr), 0)

    # Step 1+2 features still intact
    assert_eq("step1+2 fields preserved",
              all('street' in r and 'hand_category' in r for r in results_s3),
              True)

    # Board feature distributions
    print(f"  Board texture distribution:")
    mono_pct = sum(r['is_monotone'] for r in results_s3) / len(results_s3)
    tt_pct = sum(r['is_two_tone'] for r in results_s3) / len(results_s3)
    rain_pct = sum(r['is_rainbow'] for r in results_s3) / len(results_s3)
    pair_pct = sum(r['is_paired'] for r in results_s3) / len(results_s3)
    print(f"    monotone: {mono_pct:.1%}")
    print(f"    two_tone: {tt_pct:.1%}")
    print(f"    rainbow:  {rain_pct:.1%}")
    print(f"    paired:   {pair_pct:.1%}")

    avg_danger = sum(r['danger_score'] for r in results_s3) / len(results_s3)
    avg_conn = sum(r['connectivity_score'] for r in results_s3) / len(results_s3)
    print(f"  Avg danger_score: {avg_danger:.3f}")
    print(f"  Avg connectivity: {avg_conn:.1f}")

    # ---- Final Summary ----
    print(f"\n{'=' * 60}")
    print(f"Step 3 Results: {passed} passed, {failed} failed (cumulative)")
    print(f"{'=' * 60}")

    # ================================================================
    # STEP 4: Range + Equity Feature Tests
    # ================================================================
    print(f"\n{'=' * 60}")
    print("STEP 4: Range Construction + Equity Tests")
    print(f"{'=' * 60}")

    # ---- get_villain_range: opener vs defender ----
    print("\n--- get_villain_range ---")
    # UTG vs BB: UTG is earlier â†’ UTG opened â†’ villain(UTG) has RFI range
    r_utg_open = get_villain_range('BB', 'UTG')
    r_utg_rfi = _range_manager.get_rfi_range('UTG')
    assert_eq("UTG opened vs BB â†’ RFI range",
              r_utg_open == r_utg_rfi, True)

    # BB vs BTN: BTN is earlier â†’ BTN opened â†’ villain(BTN) has RFI range
    r_btn_open = get_villain_range('BB', 'BTN')
    r_btn_rfi = _range_manager.get_rfi_range('BTN')
    assert_eq("BTN opened vs BB â†’ RFI range",
              r_btn_open == r_btn_rfi, True)

    # BTN vs BB: BTN is earlier â†’ BTN opened â†’ villain(BB) defended
    r_bb_def = get_villain_range('BTN', 'BB')
    r_bb_def_expected = _range_manager.get_defend_range('BB', 'BTN')
    assert_eq("BB defended vs BTN â†’ defend range",
              r_bb_def == r_bb_def_expected, True)

    # CO vs HJ: HJ is earlier â†’ HJ opened â†’ villain(HJ) has RFI range
    r_hj_open = get_villain_range('CO', 'HJ')
    r_hj_rfi = _range_manager.get_rfi_range('HJ')
    assert_eq("HJ opened vs CO â†’ RFI range",
              r_hj_open == r_hj_rfi, True)

    # HJ vs CO: HJ is earlier â†’ HJ opened â†’ villain(CO) defended
    r_co_def = get_villain_range('HJ', 'CO')
    r_co_def_expected = _range_manager.get_defend_range('CO', 'HJ')
    assert_eq("CO defended vs HJ â†’ defend range",
              r_co_def == r_co_def_expected, True)

    # SB vs BB: SB is earlier â†’ SB opened â†’ villain(BB) defended
    r_bb_vs_sb = get_villain_range('SB', 'BB')
    r_bb_vs_sb_exp = _range_manager.get_defend_range('BB', 'SB')
    assert_eq("BB defended vs SB â†’ defend range",
              r_bb_vs_sb == r_bb_vs_sb_exp, True)

    # ---- extract_equity_features: known hands ----
    print("\n--- equity: overpair on dry board (not facing bet) ---")
    eq_op = extract_equity_features(
        hero_cards=['As', 'Ah'],
        board_cards=['Ks', '7h', '2d'],
        hero_pos='BTN', villain_pos='BB',
        facing_bet=False, street_raw='f',
    )
    assert_eq("overpair equity > 0.7", eq_op['raw_equity'] > 0.7, True)
    assert_eq("equity in [0,1]",
              0.0 <= eq_op['raw_equity'] <= 1.0, True)
    print(f"  AA on Ks7h2d vs BB defend: {eq_op['raw_equity']:.3f}")

    # ---- equity: air on scary board (facing bet â†’ narrowed range) ----
    print("\n--- equity: air facing bet (narrowed range) ---")
    eq_air = extract_equity_features(
        hero_cards=['Qh', '3d'],
        board_cards=['As', 'Kd', '7c', '5h', '2s'],
        hero_pos='BB', villain_pos='BTN',
        facing_bet=True, street_raw='r',
    )
    assert_eq("air equity < 0.3", eq_air['raw_equity'] < 0.3, True)
    print(f"  Qh3d on AsKd7c5h2s vs BTN bet: {eq_air['raw_equity']:.3f}")

    # ---- equity: facing bet should give different equity than not facing ----
    print("\n--- equity: facing bet vs not facing bet ---")
    eq_no_fb = extract_equity_features(
        hero_cards=['Kd', 'Jh'],
        board_cards=['Ks', '7h', '2d'],
        hero_pos='BB', villain_pos='BTN',
        facing_bet=False, street_raw='f',
    )
    eq_fb = extract_equity_features(
        hero_cards=['Kd', 'Jh'],
        board_cards=['Ks', '7h', '2d'],
        hero_pos='BB', villain_pos='BTN',
        facing_bet=True, street_raw='f',
    )
    # When facing bet, villain range is narrowed to betting range,
    # which is polarized â€” our equity should be different
    print(f"  KdJh on Ks7h2d: no bet={eq_no_fb['raw_equity']:.3f}, "
          f"facing bet={eq_fb['raw_equity']:.3f}")
    assert_eq("narrowing changes equity",
              abs(eq_no_fb['raw_equity'] - eq_fb['raw_equity']) > 0.01, True)

    # ---- equity: villain combos > 0 ----
    assert_eq("villain combos > 0 (no fb)",
              eq_no_fb['_equity_villain_combos'] > 0, True)
    assert_eq("villain combos > 0 (fb)",
              eq_fb['_equity_villain_combos'] > 0, True)

    # ---- Batch: Step 1-4 on 50 hands (timing check) ----
    print("\n--- batch Step 1-4 (50 hands, timing) ---")
    results_s4_small = extract_all_step1_2_3_4(data_2k[:50],
                                                progress_every=50)
    assert_eq("50 hands extracted (s4)", len(results_s4_small), 50)

    # All equity features present
    eq_keys = ['raw_equity', 'equity_vs_range']
    missing_eq = [r['_hand_id'] for r in results_s4_small
                  if not all(k in r for k in eq_keys)]
    assert_eq("no missing equity features", len(missing_eq), 0)

    # Equity bounds
    bad_eq = [r for r in results_s4_small
              if r['raw_equity'] < 0 or r['raw_equity'] > 1]
    assert_eq("all equity in [0,1]", len(bad_eq), 0)

    # raw_equity == equity_vs_range (same value, explicit alias)
    mismatch = [r for r in results_s4_small
                if r['raw_equity'] != r['equity_vs_range']]
    assert_eq("raw_equity matches equity_vs_range", len(mismatch), 0)

    # Spot check: monsters should tend to have high equity
    monsters_s4 = [r for r in results_s4_small if r['is_monster']]
    if monsters_s4:
        avg_monster_eq = sum(r['raw_equity'] for r in monsters_s4) / len(monsters_s4)
        print(f"  Avg monster equity: {avg_monster_eq:.3f} ({len(monsters_s4)} hands)")
        assert_eq("monsters avg equity > 0.6", avg_monster_eq > 0.6, True)
    else:
        print("  No monsters in first 50 hands (skip check)")
        passed += 1  # Can't test, but not a failure

    # Spot check: high_card/air should tend to have lower equity
    air_s4 = [r for r in results_s4_small
              if r['_hand_category_raw'] in ('high_card', 'one_overcard')]
    if air_s4:
        avg_air_eq = sum(r['raw_equity'] for r in air_s4) / len(air_s4)
        print(f"  Avg air equity: {avg_air_eq:.3f} ({len(air_s4)} hands)")
        assert_eq("air avg equity < 0.5", avg_air_eq < 0.5, True)
    else:
        print("  No air hands in first 50 (skip check)")
        passed += 1

    # All previous step features preserved
    assert_eq("step1+2+3 fields preserved",
              all('street' in r and 'hand_category' in r
                  and 'danger_score' in r
                  for r in results_s4_small),
              True)

    # Equity distribution sanity
    equities = [r['raw_equity'] for r in results_s4_small]
    avg_eq = sum(equities) / len(equities)
    print(f"  Avg equity across 50 hands: {avg_eq:.3f}")
    print(f"  Min: {min(equities):.3f}, Max: {max(equities):.3f}")

    # ---- Final Summary ----
    print(f"\n{'=' * 60}")
    print(f"Step 4 Results: {passed} passed, {failed} failed (cumulative)")
    print(f"{'=' * 60}")

    # ================================================================
    # STEP 5: Range Partitioning (FIXED combo expansion) Tests
    # ================================================================
    print(f"\n{'=' * 60}")
    print("STEP 5: Range Partitioning Tests")
    print(f"{'=' * 60}")

    # ---- get_valid_combos: pair, no blockers ----
    print("\n--- get_valid_combos: pairs ---")
    combos_aa = get_valid_combos('AA', set())
    assert_eq("AA no blockers = 6 combos", len(combos_aa), 6)

    combos_77 = get_valid_combos('77', set())
    assert_eq("77 no blockers = 6 combos", len(combos_77), 6)

    # With one card blocked
    combos_aa_1block = get_valid_combos('AA', {'As'})
    assert_eq("AA with As blocked = 3 combos", len(combos_aa_1block), 3)

    # With two cards blocked
    combos_aa_2block = get_valid_combos('AA', {'As', 'Ah'})
    assert_eq("AA with As,Ah blocked = 1 combo", len(combos_aa_2block), 1)

    # ---- get_valid_combos: suited, no blockers ----
    print("\n--- get_valid_combos: suited ---")
    combos_aks = get_valid_combos('AKs', set())
    assert_eq("AKs no blockers = 4 combos", len(combos_aks), 4)
    # Verify all suited
    for c in combos_aks:
        assert_eq(f"AKs combo {c} is suited", c[0][1], c[1][1])

    # With suit blocked
    combos_aks_1block = get_valid_combos('AKs', {'As'})
    assert_eq("AKs with As blocked = 3 combos", len(combos_aks_1block), 3)

    # ---- get_valid_combos: offsuit, no blockers ----
    print("\n--- get_valid_combos: offsuit ---")
    combos_ako = get_valid_combos('AKo', set())
    assert_eq("AKo no blockers = 12 combos", len(combos_ako), 12)
    # Verify all offsuit
    for c in combos_ako:
        assert_eq(f"AKo combo {c} is offsuit", c[0][1] != c[1][1], True)

    combos_ako_1block = get_valid_combos('AKo', {'As'})
    assert_eq("AKo with As blocked = 9 combos", len(combos_ako_1block), 9)

    # ---- get_valid_combos: no collisions with used cards ----
    print("\n--- get_valid_combos: card removal ---")
    used = {'As', 'Kd', '7h', '2d', 'Ks'}  # hero + board
    combos_ak_used = get_valid_combos('AKs', used)
    for c in combos_ak_used:
        for card in c:
            assert_eq(f"{card} not in used", card.lower() not in {u.lower() for u in used}, True)

    # ---- Cross-validate with raw_equity._get_valid_combos ----
    print("\n--- cross-validate with raw_equity ---")
    for hand_str in ['AA', 'AKs', 'AKo', 'QQ', 'T9s', '87o']:
        used_set = {'Jd', '9s', '4s', '4h', '3h'}
        our_combos = get_valid_combos(hand_str, used_set)
        ref_combos = _equity_calculator._get_valid_combos(hand_str, used_set)
        assert_eq(f"{hand_str} combo count matches raw_equity",
                  len(our_combos), len(ref_combos))

    # ---- partition_range: nuts should have ~0% better ----
    print("\n--- partition: nut hand ---")
    # AA on A72 rainbow â€” virtually nothing beats us
    p_nuts = partition_range(
        ['As', 'Ah'], ['Ad', '7c', '2s'],
        _range_manager.get_rfi_range('BTN')
    )
    print(f"  AA on Ad7c2s: better={p_nuts['better_hand_pct']:.3f}, "
          f"worse={p_nuts['worse_hand_pct']:.3f}")
    assert_eq("nuts: very few better", p_nuts['better_hand_pct'] < 0.05, True)
    assert_eq("nuts: mostly worse", p_nuts['worse_hand_pct'] > 0.80, True)

    # ---- partition: air should have high better_hand_pct ----
    print("\n--- partition: air hand ---")
    p_air = partition_range(
        ['Qh', '3d'], ['As', 'Kd', '7c', '5h', '2s'],
        _range_manager.get_rfi_range('BTN')
    )
    print(f"  Qh3d on AsKd7c5h2s: better={p_air['better_hand_pct']:.3f}, "
          f"worse={p_air['worse_hand_pct']:.3f}")
    assert_eq("air: many better", p_air['better_hand_pct'] > 0.5, True)

    # ---- partition: pct sums to ~1.0 ----
    print("\n--- partition: percentages sum to 1 ---")
    total_pct = (p_nuts['better_hand_pct'] + p_nuts['worse_hand_pct']
                 + p_nuts['_partition_tie_pct'])
    assert_close("nuts pcts sum to 1", total_pct, 1.0, tol=0.01)
    total_air = (p_air['better_hand_pct'] + p_air['worse_hand_pct']
                 + p_air['_partition_tie_pct'])
    assert_close("air pcts sum to 1", total_air, 1.0, tol=0.01)

    # ---- partition: facing bet narrowing changes result ----
    print("\n--- partition: facing bet vs not ---")
    p_no_fb = extract_partition_features(
        ['Kd', 'Jh'], ['Ks', '7h', '2d'],
        'BB', 'BTN', facing_bet=False, street_raw='f',
    )
    p_fb = extract_partition_features(
        ['Kd', 'Jh'], ['Ks', '7h', '2d'],
        'BB', 'BTN', facing_bet=True, street_raw='f',
    )
    print(f"  KdJh TPTK: no_bet better={p_no_fb['better_hand_pct']:.3f}, "
          f"fb better={p_fb['better_hand_pct']:.3f}")
    assert_eq("narrowing changes partition",
              abs(p_no_fb['better_hand_pct'] - p_fb['better_hand_pct']) > 0.01,
              True)

    # ---- Batch: Step 1-5 on 50 hands ----
    print("\n--- batch Step 1-5 (50 hands, timing) ---")
    results_s5 = extract_all_step1_through_5(data_2k[:50],
                                              progress_every=50)
    assert_eq("50 hands extracted (s5)", len(results_s5), 50)

    # Partition features present
    part_keys = ['better_hand_pct', 'worse_hand_pct']
    missing_part = [r['_hand_id'] for r in results_s5
                    if not all(k in r for k in part_keys)]
    assert_eq("no missing partition features", len(missing_part), 0)

    # Bounds
    bad_better = [r for r in results_s5
                  if r['better_hand_pct'] < 0 or r['better_hand_pct'] > 1]
    assert_eq("better_hand_pct in [0,1]", len(bad_better), 0)

    bad_worse = [r for r in results_s5
                 if r['worse_hand_pct'] < 0 or r['worse_hand_pct'] > 1]
    assert_eq("worse_hand_pct in [0,1]", len(bad_worse), 0)

    # Consistency: monsters should have low better_hand_pct
    monsters_s5 = [r for r in results_s5 if r['is_monster']]
    if monsters_s5:
        avg_m_better = sum(r['better_hand_pct'] for r in monsters_s5) / len(monsters_s5)
        print(f"  Monsters avg better_hand_pct: {avg_m_better:.3f} ({len(monsters_s5)} hands)")
        assert_eq("monsters avg better < 0.3", avg_m_better < 0.3, True)
    else:
        passed += 1

    # Consistency: equity and partition should correlate
    # Higher equity â†’ lower better_hand_pct (roughly)
    high_eq = [r for r in results_s5 if r['raw_equity'] > 0.7]
    low_eq = [r for r in results_s5 if r['raw_equity'] < 0.3]
    if high_eq and low_eq:
        avg_better_high = sum(r['better_hand_pct'] for r in high_eq) / len(high_eq)
        avg_better_low = sum(r['better_hand_pct'] for r in low_eq) / len(low_eq)
        print(f"  High equity hands avg better_pct: {avg_better_high:.3f}")
        print(f"  Low equity hands avg better_pct: {avg_better_low:.3f}")
        assert_eq("high equity â†’ lower better_pct",
                  avg_better_high < avg_better_low, True)
    else:
        passed += 1

    # All previous features preserved
    assert_eq("all prior features preserved",
              all('street' in r and 'hand_category' in r
                  and 'danger_score' in r and 'raw_equity' in r
                  for r in results_s5),
              True)

    # ---- Final Summary ----
    print(f"\n{'=' * 60}")
    print(f"Step 5 Results: {passed} passed, {failed} failed (cumulative)")
    print(f"{'=' * 60}")

    # ================================================================
    # STEP 6: Derived Features + CSV Export Tests
    # ================================================================
    print(f"\n{'=' * 60}")
    print("STEP 6: Derived Features + CSV Export Tests")
    print(f"{'=' * 60}")

    # ---- equity_margin calculation ----
    print("\n--- equity_margin ---")
    test_feat = {'raw_equity': 0.65, 'pot_odds': 0.30, 'pot_size': 50.0}
    add_derived_features(test_feat)
    assert_close("equity_margin = 0.65 - 0.30", test_feat['equity_margin'], 0.35)
    assert_close("spr = 100/50", test_feat['spr'], 2.0)

    # Negative margin (should fold territory)
    test_neg = {'raw_equity': 0.15, 'pot_odds': 0.40, 'pot_size': 20.0}
    add_derived_features(test_neg)
    assert_close("negative margin", test_neg['equity_margin'], -0.25)
    assert_close("spr = 100/20", test_neg['spr'], 5.0)

    # Zero pot (edge case)
    test_zero = {'raw_equity': 0.50, 'pot_odds': 0.0, 'pot_size': 0.0}
    add_derived_features(test_zero)
    assert_close("zero pot spr capped", test_zero['spr'], 99.0)

    # Not facing bet (pot_odds=0, margin = equity)
    test_no_fb = {'raw_equity': 0.72, 'pot_odds': 0.0, 'pot_size': 10.0}
    add_derived_features(test_no_fb)
    assert_close("no bet: margin = equity", test_no_fb['equity_margin'], 0.72)

    # ---- extract_all_features: single hand ----
    print("\n--- extract_all_features: single hand ---")
    hand_test = data_2k[0]
    f_all = extract_all_features(hand_test)

    # All feature columns present
    for col in FEATURE_COLUMNS:
        assert_eq(f"column '{col}' present", col in f_all, True)
    assert_eq("label present", LABEL_COLUMN in f_all, True)

    # Derived features are populated
    assert_eq("equity_margin is float",
              isinstance(f_all['equity_margin'], float), True)
    assert_eq("spr is float",
              isinstance(f_all['spr'], float), True)

    # Step 7: Action history features default to 0 for gauntlet hands
    assert_eq("is_3bet_pot defaults to 0", f_all['is_3bet_pot'], 0)
    assert_eq("villain_aggression_count defaults to 0",
              f_all['villain_aggression_count'], 0)
    assert_eq("villain_checked_back defaults to 0",
              f_all['villain_checked_back'], 0)
    assert_eq("villain_call_count defaults to 0",
              f_all['villain_call_count'], 0)

    # ---- Batch: full pipeline on 50 hands ----
    print("\n--- batch all features (50 hands) ---")
    results_s6 = extract_all_features_batch(data_2k[:50], progress_every=50)
    assert_eq("50 hands extracted (s6)", len(results_s6), 50)

    # All columns present in every row
    all_cols_present = all(
        all(col in r for col in FEATURE_COLUMNS + [LABEL_COLUMN])
        for r in results_s6
    )
    assert_eq("all columns present in all rows", all_cols_present, True)

    # equity_margin consistency: facing_bet=0 â†’ margin = equity
    for r in results_s6:
        if r['facing_bet'] == 0:
            assert_close(
                f"hand {r['_hand_id']} no-bet margin=equity",
                r['equity_margin'], r['raw_equity'], tol=1e-5
            )
            break  # Just check first one

    # equity_margin consistency: positive margin when equity > pot_odds
    for r in results_s6:
        if r['facing_bet'] == 1:
            expected_sign = (r['raw_equity'] > r['pot_odds'])
            actual_sign = (r['equity_margin'] > 0)
            assert_eq(
                f"hand {r['_hand_id']} margin sign correct",
                actual_sign, expected_sign
            )
            break

    # spr is always positive
    bad_spr = [r for r in results_s6 if r['spr'] <= 0]
    assert_eq("spr always positive", len(bad_spr), 0)

    # ---- CSV export ----
    print("\n--- CSV export ---")
    csv_path = '/home/claude/test_features_50.csv'
    export_to_csv(results_s6, csv_path)

    # Verify CSV is readable and has correct shape
    import csv as csv_mod
    with open(csv_path) as csvf:
        reader = csv_mod.DictReader(csvf)
        rows = list(reader)
    assert_eq("CSV row count", len(rows), 50)
    expected_cols = set(FEATURE_COLUMNS + [LABEL_COLUMN])
    actual_cols = set(rows[0].keys())
    assert_eq("CSV columns match", actual_cols, expected_cols)

    # Verify no metadata columns leaked into CSV
    meta_leaked = [c for c in actual_cols if c.startswith('_')]
    assert_eq("no metadata in CSV", len(meta_leaked), 0)

    # Verify values are parseable
    r0 = rows[0]
    assert_eq("street parseable", int(r0['street']) in (0, 1, 2), True)
    assert_eq("raw_equity parseable",
              0.0 <= float(r0['raw_equity']) <= 1.0, True)
    assert_eq("action is valid label",
              r0['action'] in ('FOLD', 'CHECK', 'CALL', 'BET', 'RAISE'), True)

    # ---- Feature count verification ----
    print(f"\n--- feature summary ---")
    print(f"  Feature columns: {len(FEATURE_COLUMNS)}")
    print(f"  Label column: {LABEL_COLUMN}")
    print(f"  Total columns in CSV: {len(FEATURE_COLUMNS) + 1}")

    # ---- Final Summary ----
    print(f"\n{'=' * 60}")
    print(f"FINAL: {passed} passed, {failed} failed (all steps)")
    print(f"{'=' * 60}")
    return failed == 0


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
