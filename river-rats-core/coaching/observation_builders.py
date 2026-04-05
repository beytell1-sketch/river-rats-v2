"""
ObservationBuilders -- construct SpotObservation from hand data.

One build function that populates the SpotObservation with all data
any level needs. The SpotObservation is a structured fact bag --
the renderer decides which fields to surface and how to word them.
"""
import logging
from typing import Optional, List

from coaching.spot_observation import SpotObservation
from coaching.spot_classifier import SpotClassification

_logger = logging.getLogger(__name__)


# =====================================================================
# BOARD TEXTURE LABELLING
# =====================================================================

def _board_texture_label(danger_score: float) -> str:
    """Classify danger_score into a human-readable board texture label."""
    if danger_score < 0.30:
        return "dry"
    if danger_score <= 0.60:
        return "moderate"
    return "dangerous"


# =====================================================================
# DRAW DESCRIPTION
# =====================================================================

def _draw_description(feat_dict: dict) -> str:
    """Build a draw description from feature dict flags."""
    is_river = feat_dict.get("street", -1) == 2.0
    if is_river:
        return ""

    has_fd = feat_dict.get("has_flush_draw", 0) > 0.5
    has_sd = feat_dict.get("has_straight_draw", 0) > 0.5

    if has_fd and has_sd:
        return "combo draw"
    if has_fd:
        return "flush draw"
    if has_sd:
        return "straight draw"
    return ""


# =====================================================================
# POT ODDS (correct formula)
# =====================================================================

def _correct_pot_odds_pct(pot_size: float, to_call: float) -> float:
    """
    Correct pot odds: to_call / (pot_size + 2 * to_call) * 100.

    In PokerBench data, pot_size is the pot BEFORE villain's bet,
    and to_call IS the bet amount. Total pot after hero calls =
    pot_size + bet + call = pot_size + 2 * to_call.
    """
    if to_call <= 0:
        return 0.0
    total = pot_size + 2 * to_call
    if total <= 0:
        return 0.0
    return (to_call / total) * 100


# =====================================================================
# TOP THREATS (from range breakdown buckets)
# =====================================================================

def _top_threats(range_breakdown) -> str:
    """
    Build a top-threats string from the top 2-3 buckets that beat hero.

    Example: "nut flush (3%), sets (2%)"
    """
    if range_breakdown is None:
        return ""

    threats = []
    for bucket in range_breakdown.buckets:
        if bucket.beats_hero > 0 and bucket.pct_of_range > 0.01:
            pct = round(bucket.pct_of_range * 100, 1)
            # Use subcategory for specificity, replacing underscores
            label = bucket.subcategory.replace("_", " ")
            threats.append(f"{label} ({pct}%)")
        if len(threats) >= 3:
            break

    return ", ".join(threats)


# =====================================================================
# BLOCKER DESCRIPTION
# =====================================================================

def _blocker_description(range_breakdown) -> str:
    """Build a blocker description from RangeBreakdown."""
    if range_breakdown is None:
        return ""

    bi = range_breakdown.blocker_info
    if bi.total_blocked == 0:
        return ""

    parts = []
    if bi.blocks_value:
        parts.append("Your cards block villain's value hands")
    if bi.blocks_bluffs:
        parts.append("Your cards block villain's bluff candidates")

    if not parts and bi.descriptions:
        return bi.descriptions[0]

    return ". ".join(parts)


# =====================================================================
# VILLAIN COMPOSITION (from range_decomposition buckets)
# =====================================================================

def _villain_composition(range_breakdown):
    """
    Compute tp_plus_pct, draw_pct, air_pct from range breakdown buckets.

    Uses the subcategory classification from range_decomposition.py.
    """
    if range_breakdown is None:
        return 0.0, 0.0, 0.0

    tp_plus_combos = 0
    draw_combos = 0
    air_combos = 0
    total = range_breakdown.total_combos

    if total == 0:
        return 0.0, 0.0, 0.0

    # Subcategories classified as TP+ (value hands)
    _TP_PLUS = {
        'straight_flush', 'quads', 'full_house',
        'nut_flush', 'strong_flush', 'weak_flush',
        'nut_straight', 'weak_straight',
        'top_set', 'lower_set',
        'top_two_pair', 'other_two_pair',
        'overpair', 'top_pair_strong_kicker', 'top_pair_weak_kicker',
    }

    # Subcategories classified as draws
    _DRAWS = {
        'combo_draw', 'nut_flush_draw', 'flush_draw', 'oesd', 'gutshot',
    }

    # Subcategories classified as air
    _AIR = {'overcards', 'air'}

    for bucket in range_breakdown.buckets:
        if bucket.subcategory in _TP_PLUS:
            tp_plus_combos += bucket.total_combos
        elif bucket.subcategory in _DRAWS:
            draw_combos += bucket.total_combos
        elif bucket.subcategory in _AIR:
            air_combos += bucket.total_combos

    return (
        tp_plus_combos / total,
        draw_combos / total,
        air_combos / total,
    )


# =====================================================================
# COUNTERINTUITIVE DETECTION
# =====================================================================

def _detect_counterintuitive(action: str, hand_bucket: str,
                              better_hand_pct: float,
                              num_opponents: int = 1):
    """
    Detect when the GTO action contradicts naive hand-strength logic.

    Returns (is_counterintuitive, reason).

    num_opponents: pass from build_observation(). Defaults to 1 (heads-up).
    """
    action = action.upper()

    # CHECK with a strong hand -- counterintuitive ONLY heads-up (S-1 / B3 fix).
    # Suppress strong_made multiway: checking strong hands is standard strategy
    # multiway, not counterintuitive.
    # Monsters retain the flag multiway: checking a flopped set is a genuine
    # teaching moment even in a 4-way pot.
    if action == "CHECK" and hand_bucket in ("monster", "strong_made"):
        if hand_bucket == "strong_made" and num_opponents > 1:
            # multiway: checking strong_made is standard -- not counterintuitive
            pass
        else:
            # heads-up strong_made, OR monster at any count
            return True, "strong_hand_checking"

    # BET with weak hands -- bluffing
    if action == "BET" and hand_bucket in ("weak_made", "air"):
        return True, "weak_hand_betting"

    # BET with a drawing hand -- semi-bluff
    if action == "BET" and hand_bucket == "drawing":
        return True, "semi_bluff"

    # FOLD a decent hand -- range discipline
    # Add multiway_fold_discipline reason when multiway (Architecture Brief §4)
    if action == "FOLD" and hand_bucket in ("medium_made", "strong_made"):
        if num_opponents > 1:
            return True, "multiway_fold_discipline"
        return True, "folding_decent_hand"

    # CALL when mostly behind -- priced in or mandatory defend
    if action == "CALL" and better_hand_pct > 0.60:
        return True, "calling_behind"

    return False, ""


# =====================================================================
# NUT DRAW DETECTION (WI-1)
# =====================================================================

def _parse_cards(card_str: str) -> List[str]:
    """Parse a card string like 'AcKs' or '9s7s4c' into ['Ac', 'Ks'] etc."""
    if not card_str:
        return []
    # Cards are 2-char tokens: rank + suit
    return [card_str[i:i+2] for i in range(0, len(card_str), 2)]


def _is_nut_draw(hero_cards_str: str, board_cards_str: str,
                 has_flush_draw: bool, has_straight_draw: bool) -> bool:
    """
    Determine if hero's draw is to the nuts.

    For flush draws: hero holds the Ace of the flush suit.
    For straight draws: not implemented (would need extensive card logic).
    Returns False if no draw or cards unavailable.
    """
    if not has_flush_draw and not has_straight_draw:
        return False

    if not hero_cards_str or not board_cards_str:
        return False

    if has_flush_draw:
        hero = _parse_cards(hero_cards_str)
        board = _parse_cards(board_cards_str)

        # has_flush_draw is already True from the feature extractor.
        # Find the flush draw suit: any suit where hero contributes at least
        # 1 card and total (hero + board) >= 4 cards of that suit.
        # On the flop: hero 2 + board 2 = 4, or hero 1 + board 3 = 4.
        # The feature extractor may also flag draws with hero 1 + board 2 = 3
        # (backdoor or specific draw detection). Accept any suit where hero
        # holds cards and check for the Ace.
        hero_suits = [c[1].lower() for c in hero if len(c) == 2]
        board_suits = [c[1].lower() for c in board if len(c) == 2]

        for suit in set(hero_suits):
            board_count = board_suits.count(suit)
            hero_count = hero_suits.count(suit)
            # Flush draw: hero has card(s) of this suit and board has 2+ of same suit
            if board_count >= 2 and hero_count >= 1:
                hero_ranks = [c[0].upper() for c in hero if len(c) == 2 and c[1].lower() == suit]
                if 'A' in hero_ranks:
                    return True
                return False

    # Straight draw nut detection is complex — skip for now
    return False


# =====================================================================
# PREVIOUS-STREET DRAW DETECTION (WI-5)
# =====================================================================

def _was_drawing_previous_street(hero_cards_str: str, board_cards_str: str,
                                  street: float) -> bool:
    """
    On river hands, reconstruct prior-street boards and check if hero had a draw.

    Only fires on river (street == 2). Returns False otherwise.
    Requires board_cards ordered as [flop1, flop2, flop3, turn, river].
    """
    if street != 2.0:
        return False

    if not hero_cards_str or not board_cards_str:
        return False

    hero = _parse_cards(hero_cards_str)
    board = _parse_cards(board_cards_str)

    if len(board) < 5 or len(hero) < 2:
        return False

    try:
        from hand_evaluator import evaluate_hand

        # Check turn board (4 cards)
        turn_board = board[:4]
        turn_eval = evaluate_hand(hero, turn_board)
        if turn_eval.has_flush_draw or turn_eval.has_straight_draw:
            return True

        # Check flop board (3 cards)
        flop_board = board[:3]
        flop_eval = evaluate_hand(hero, flop_board)
        if flop_eval.has_flush_draw or flop_eval.has_straight_draw:
            return True

    except Exception as e:
        _logger.debug("Previous-street draw detection failed: %s", e)

    return False


# =====================================================================
# TIGHTNESS FROM PREDICTION
# =====================================================================

def _tightness_from_spot(spot: SpotClassification):
    """Extract tightness and confidence from SpotClassification."""
    return spot.tightness


# =====================================================================
# MAIN BUILDER
# =====================================================================

def build_observation(
    spot: SpotClassification,
    ctx,           # HandContext
    feat_dict: dict,
    range_breakdown=None,  # Optional RangeBreakdown
) -> SpotObservation:
    """
    Build a SpotObservation from a classified spot and hand context.

    This is the single factory function that populates ALL fields
    any level could need. The renderer reads whichever fields it wants.

    Args:
        spot: SpotClassification from classify_spot()
        ctx: HandContext from build_hand_context()
        feat_dict: Raw feature dictionary
        range_breakdown: Optional RangeBreakdown from decompose_range()

    Returns:
        Frozen SpotObservation ready for any renderer.
    """
    # -- Hand strength --
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_hand_pct = ctx.worse_hand_pct
    better_hand_pct = ctx.better_hand_pct

    # -- Board texture --
    danger_score = ctx.danger_score
    board_label = _board_texture_label(danger_score)

    # -- Draw info --
    draw_desc = _draw_description(feat_dict)
    has_draw = bool(draw_desc)
    draw_outs = int(feat_dict.get("draw_outs", 0))
    draw_equity = ctx.draw_equity

    # -- Pot odds --
    pot_size = ctx.pot_size
    to_call = ctx.to_call_amount
    facing_bet = feat_dict.get("facing_bet", 0) > 0.5
    pot_odds_pct = _correct_pot_odds_pct(pot_size, to_call)
    equity_pct = equity * 100
    equity_margin = equity_pct - pot_odds_pct

    # -- Position --
    is_ip = ctx.is_ip
    hero_position = ctx.hero_position_name
    villain_position = ctx.villain_position_name
    opponent_phrase = ctx.opponent_phrase

    # -- Multiway --
    num_opponents = ctx.num_opponents
    is_multiway = num_opponents > 1

    # -- Range decomposition --
    value_target_pct = 0.0
    top_threats_str = ""
    hero_label = ""
    blocker_desc = ""
    villain_tp_plus_pct = 0.0
    villain_draw_pct_val = 0.0
    villain_air_pct_val = 0.0

    if range_breakdown is not None:
        value_target_pct = getattr(range_breakdown, 'value_target_pct', 0.0)
        hero_label = getattr(range_breakdown, 'hero_label', '')
        top_threats_str = _top_threats(range_breakdown)
        blocker_desc = _blocker_description(range_breakdown)
        villain_tp_plus_pct, villain_draw_pct_val, villain_air_pct_val = \
            _villain_composition(range_breakdown)

    # -- Villain range state (Decision A) --
    villain_range_state = None
    villain_range_confidence = 0.0
    try:
        from testing.range_state import classify_range_state
        state, confidence = classify_range_state(feat_dict)
        villain_range_state = state.value  # store as string
        villain_range_confidence = confidence
    except Exception as e:
        _logger.debug("Range state classification failed: %s", e)

    # -- Counterintuitive detection --
    is_ci, ci_reason = _detect_counterintuitive(
        spot.action, spot.hand_bucket, better_hand_pct, num_opponents,
    )

    # -- Tightness --
    tightness = spot.tightness

    # -- Strategic context --
    spr = ctx.spr
    is_3bet_pot = ctx.is_3bet_pot

    # -- Sprint 2: new multiway data fields --
    # WI-2: villain aggression streets (direct promotion from HandContext)
    villain_aggression_streets = int(getattr(ctx, 'villain_aggression_count', 0))

    # WI-6: players behind count (positional approximation)
    players_behind_count = 0 if is_ip else num_opponents

    # WI-1: nut draw detection
    has_fd = feat_dict.get("has_flush_draw", 0) > 0.5
    has_sd = feat_dict.get("has_straight_draw", 0) > 0.5
    is_nut_draw = _is_nut_draw(
        ctx.hero_cards, ctx.board_cards, has_fd, has_sd
    )

    # WI-3: facing bet and call (heuristic)
    facing_bet_and_call = (
        facing_bet
        and getattr(ctx, 'villain_call_count', 0) > 0
        and num_opponents >= 2
    )

    # WI-4: facing check-raise (heuristic)
    facing_check_raise = (
        facing_bet
        and feat_dict.get('_num_raises_this_street', 0) >= 1
    )

    # WI-5: was drawing previous street (inferential, river only)
    street = feat_dict.get("street", -1)
    was_drawing = _was_drawing_previous_street(
        ctx.hero_cards, ctx.board_cards, street
    )

    return SpotObservation(
        # Identity
        action=spot.action,
        strategic_role=spot.strategic_role,
        hand_bucket=spot.hand_bucket,

        # Hand strength
        hand_description=ctx.hand_description,
        hand_description_cap=ctx.hand_description_cap,
        equity=equity,
        worse_hand_pct=worse_hand_pct,
        better_hand_pct=better_hand_pct,

        # Board
        board_texture_label=board_label,
        danger_score=danger_score,

        # Draws
        has_draw=has_draw,
        draw_outs=draw_outs,
        draw_description=draw_desc,
        draw_equity=draw_equity,

        # Pot odds
        pot_odds_pct=pot_odds_pct,
        equity_margin=equity_margin,
        facing_bet=facing_bet,

        # Position
        is_ip=is_ip,
        hero_position=hero_position,
        villain_position=villain_position,
        opponent_phrase=opponent_phrase,

        # Multiway
        num_opponents=num_opponents,
        is_multiway=is_multiway,

        # Range decomposition (Advanced)
        value_target_pct=value_target_pct,
        top_threats=top_threats_str,
        hero_label=hero_label,
        blocker_description=blocker_desc,

        # Villain range state
        villain_range_state=villain_range_state,
        villain_range_confidence=villain_range_confidence,

        # Villain composition
        villain_tp_plus_pct=villain_tp_plus_pct,
        villain_draw_pct=villain_draw_pct_val,
        villain_air_pct=villain_air_pct_val,

        # Strategic context
        spr=spr,
        is_3bet_pot=is_3bet_pot,

        # Sprint 2: multiway data fields
        is_nut_draw=is_nut_draw,
        villain_aggression_streets=villain_aggression_streets,
        facing_bet_and_call=facing_bet_and_call,
        facing_check_raise=facing_check_raise,
        was_drawing_previous_street=was_drawing,
        players_behind_count=players_behind_count,

        # Counterintuitive
        is_counterintuitive=is_ci,
        counterintuitive_reason=ci_reason,

        # Tightness
        tightness=tightness,
        confidence=0.0,  # Set by caller if oracle prediction available

        # Preflop
        is_preflop=spot.is_preflop,
        preflop_scenario=spot.preflop_scenario,
    )
