"""
Spot Classifier -- classifies each hand into a teaching spot.

A 'spot' is the combination of action + hand strength + strategic context
that determines what to teach. By classifying the spot BEFORE selecting
observations, the teaching layer guarantees action-coherent narratives.
"""
from dataclasses import dataclass
from typing import Optional


# =====================================================================
# TIGHTNESS CONSTANTS (mirrored from situation_describer)
# =====================================================================

_TOSS_UP_GAP = 0.20   # gap < 0.20
_CLOSE_GAP   = 0.35   # gap < 0.35


@dataclass(frozen=True)
class SpotClassification:
    """What kind of teaching situation is this hand?"""
    action: str                    # CHECK, BET, CALL, FOLD, RAISE
    hand_bucket: str               # strong_made, medium_made, weak_made, drawing, air, monster
    strategic_role: str            # value_bet, semi_bluff, pure_bluff, pot_control,
                                   # showdown_value, protection, thin_value, trap,
                                   # mandatory_defend, priced_in, equity_denial,
                                   # range_fold, drawing_call
    is_preflop: bool
    preflop_scenario: Optional[str]  # open, defend, 3bet, squeeze, None
    facing_aggression: bool
    tightness: str                 # TOSS_UP, CLOSE, SILENCE


# =====================================================================
# HAND BUCKET CLASSIFICATION
# =====================================================================

def _classify_hand_bucket(equity, is_made_hand, draw_outs):
    """
    Classify the hand into one of 6 buckets.

    Priority order matters -- monster and drawing are checked before
    the made-hand strength tiers so a monster with draws stays 'monster'
    and a non-made hand with 4+ outs is 'drawing' rather than 'air'.
    """
    if equity > 0.80:
        return 'monster'

    if draw_outs >= 4 and not is_made_hand:
        return 'drawing'

    if is_made_hand:
        if equity > 0.55:
            return 'strong_made'
        if equity >= 0.35:
            return 'medium_made'
        # Made hand below 0.35 with meaningful draws -> drawing
        if draw_outs >= 4:
            return 'drawing'
        return 'weak_made'

    # Not made, fewer than 4 outs
    if draw_outs >= 4:
        return 'drawing'

    return 'air'


# =====================================================================
# STRATEGIC ROLE CLASSIFICATION
# =====================================================================

def _classify_strategic_role(action, hand_bucket, feat_dict, range_breakdown):
    """
    Map (action, hand_bucket, context) to a strategic role string.

    The mapping follows the design-doc table.  When multiple conditions
    could match for a single (action, bucket) pair, the FIRST match wins.
    """
    action = action.upper()

    # Context values (safe defaults)
    danger = feat_dict.get('danger_score', 0.0)
    value_target = 0.0
    if range_breakdown is not None:
        value_target = getattr(range_breakdown, 'value_target_pct', 0.0)

    price_ratio = feat_dict.get('pot_odds', 0.0)
    facing_bet = feat_dict.get('facing_bet', 0)
    draw_outs = feat_dict.get('draw_outs', 0)

    # ---- CHECK ----
    if action == 'CHECK':
        if hand_bucket == 'monster':
            return 'trap'
        if hand_bucket == 'strong_made':
            return 'pot_control'
        if hand_bucket == 'medium_made':
            return 'showdown_value'
        if hand_bucket == 'drawing':
            return 'pot_control'
        # weak_made or air
        return 'showdown_value'

    # ---- BET ----
    if action == 'BET':
        if hand_bucket == 'monster':
            return 'value_bet'
        if hand_bucket == 'strong_made':
            # Protection takes priority when danger is high
            if danger > 0.50:
                return 'protection'
            if value_target <= 0.20:
                return 'thin_value'
            return 'value_bet'
        if hand_bucket == 'medium_made':
            if danger > 0.50:
                return 'protection'
            return 'thin_value'
        if hand_bucket == 'drawing':
            return 'semi_bluff'
        # weak_made or air
        return 'pure_bluff'

    # ---- CALL ----
    if action == 'CALL':
        if hand_bucket == 'drawing':
            return 'drawing_call'
        if price_ratio < 0.15 and facing_bet:
            return 'priced_in'
        # medium_made or better with pot odds favorable
        if hand_bucket in ('monster', 'strong_made', 'medium_made'):
            return 'mandatory_defend'
        # weak/air calling (rare but possible)
        if price_ratio < 0.15:
            return 'priced_in'
        return 'mandatory_defend'

    # ---- FOLD ----
    if action == 'FOLD':
        if hand_bucket == 'medium_made':
            return 'range_fold'
        return 'equity_denial'

    # ---- RAISE ----
    if action == 'RAISE':
        if hand_bucket in ('monster', 'strong_made'):
            return 'value_bet'
        if hand_bucket == 'drawing' and draw_outs >= 8:
            return 'semi_bluff'
        if hand_bucket == 'drawing':
            return 'semi_bluff'
        # weak/air raise
        return 'pure_bluff'

    # Fallback (should not happen)
    return 'showdown_value'


# =====================================================================
# PREFLOP SCENARIO
# =====================================================================

def _classify_preflop_scenario(feat_dict):
    """
    Determine preflop scenario from feature context.

    Returns None for postflop hands.
    """
    street = feat_dict.get('street', 0)
    if street != -1.0:
        # Postflop (street 0=flop, 1=turn, 2=river) -- preflop isn't
        # represented in the current pipeline, but guard anyway.
        pass

    facing_bet = feat_dict.get('facing_bet', 0)
    num_raises = feat_dict.get('_num_raises_this_street', 0)

    if num_raises >= 2:
        return 'squeeze'
    if num_raises == 1:
        return '3bet'
    if facing_bet:
        return 'defend'
    return 'open'


# =====================================================================
# TIGHTNESS
# =====================================================================

def _classify_tightness(pred):
    """
    Classify tightness from top-two probability gap.

    Uses the same thresholds as situation_describer's _tightness_preview.
    """
    sorted_probs = sorted(pred.probs.values(), reverse=True)
    if len(sorted_probs) < 2:
        gap = 1.0
    else:
        gap = sorted_probs[0] - sorted_probs[1]

    if gap < _TOSS_UP_GAP:
        return 'TOSS_UP'
    if gap < _CLOSE_GAP:
        return 'CLOSE'
    return 'SILENCE'


# =====================================================================
# MAIN ENTRY POINT
# =====================================================================

def classify_spot(action, ctx, feat_dict, pred, range_breakdown=None):
    """
    Classify a hand into a teaching spot.

    Args:
        action: The GTO-recommended action (post-adjustment)
        ctx: HandContext
        feat_dict: Feature dictionary
        pred: OraclePrediction
        range_breakdown: Optional RangeBreakdown (L4+ only)

    Returns:
        SpotClassification
    """
    action_upper = action.upper() if action else 'CHECK'

    # Equity: prefer equity_vs_range, fall back to raw_equity
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    is_made_hand = feat_dict.get('is_made_hand', 0) > 0.5
    draw_outs = feat_dict.get('draw_outs', 0)

    # Hand bucket
    hand_bucket = _classify_hand_bucket(equity, is_made_hand, draw_outs)

    # Strategic role
    strategic_role = _classify_strategic_role(
        action_upper, hand_bucket, feat_dict, range_breakdown,
    )

    # Preflop detection
    is_preflop = feat_dict.get('is_preflop', False)
    preflop_scenario = None
    if is_preflop:
        preflop_scenario = _classify_preflop_scenario(feat_dict)
        strategic_role = f"preflop_{preflop_scenario}"

    # Facing aggression
    facing_aggression = feat_dict.get('facing_bet', 0) > 0.5

    # Tightness
    tightness = _classify_tightness(pred)

    return SpotClassification(
        action=action_upper,
        hand_bucket=hand_bucket,
        strategic_role=strategic_role,
        is_preflop=is_preflop,
        preflop_scenario=preflop_scenario,
        facing_aggression=facing_aggression,
        tightness=tightness,
    )
