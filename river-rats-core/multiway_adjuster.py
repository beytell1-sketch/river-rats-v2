"""
MultiWay Adjuster -- post-oracle action adjustment for multiway pots.

Adjusts the heads-up oracle prediction based on number of opponents.
GTO principles: tighter value ranges, suppressed bluffs, reduced equity realization.

This is a pure function with no side effects. It never modifies the oracle model
or SHAP values -- it only adjusts the action recommendation.

Usage:
    from coaching.multiway_adjuster import adjust, AdjustedPrediction
    result = adjust(oracle_pred, feat_dict, num_opponents=3)
    if result.was_adjusted:
        # Use result.adjusted_action instead of oracle's action
        # result.adjustment_reason explains why
"""

import logging
import math
from contextlib import contextmanager
from dataclasses import dataclass

from feature_keys import F

_logger = logging.getLogger(__name__)


# Thresholds — calibrated via Optuna Round 3 (500 trials, 37k multiway hands)
# See design/calibration_results.json for optimization details
#
# Round 3 applied: cold_call_base (interior optimum found at 0.52),
# cold_call_per_raise, cold_call_per_opp, pot_odds_thresh.
#
# Round 4 (GTO Expert binding decisions):
# - raise_base: 0.50→0.45, raise_per_opp: 0.00→0.02
# - rule1_draw_bypass: 6→8, rule5_draw_bypass: 5→7
# - rule4_equity_exception: NEW — 65%+ realized equity skips OOP draw veto
# - Rule 3 equity floor: sub-bluff RAISE+facing_bet → FOLD (not CALL)
#
# Tier 3 calibration (260 boundary-zone expert-labelled hands):
# - bluff_eq_thresh: 0.19→0.30 (boundary data corrects pure-T1 suggestion)
# - cold_call_base: 0.52→0.48, per_raise: 0.16→0.20, per_opp: 0.04→0.07
#
# GTO Expert binding decision (cold_call_base):
# - 0.48 rejected: 20 false calls / 0 false folds in 60 expert-labelled hands (under-tightening)
# - 0.58 rejected: makes OOP cold-call impossible, IP needs 85%+ raw (too aggressive)
# - 0.54 rejected: 2-raise scenario impossible even IP; OOP 1-raise needs 95% (over-tightens)
# - 0.52 selected: matches Round 3 Optuna interior optimum; IP 1-raise/2-opp = 79% raw
#   (top pair top kicker+), OOP = 93% (sets+). Draw bypass (7 outs) handles implied odds.
#
BLUFF_EQUITY_THRESHOLD = 0.30       # Tier 3 calibrated (was 0.19 pure-T1, Tier 3 boundary data says 0.30)
VALUE_BASE_THRESHOLD = 0.40         # Confirmed across all rounds
VALUE_PER_OPPONENT = 0.00           # Confirmed across all rounds
RAISE_BASE_THRESHOLD = 0.45         # GTO Expert approved (Round 4)
RAISE_PER_OPPONENT = 0.02           # GTO Expert approved (Round 4)
MAX_OPPONENTS_CAP = 5               # Fixed
RULE1_DRAW_BYPASS = 8              # GTO Expert approved (Round 4)
DRAW_OUTS_IP_BASE = 8              # Not in calibration scope
DRAW_OUTS_IP_PER_OPPONENT = 1      # Not in calibration scope

# Cold-call tightening (Rule 5) — Tier 3 calibrated
COLD_CALL_BASE = 0.52              # GTO Expert binding decision: revert to Round 3 Optuna optimum (was 0.48 Tier 3, 0.58 optimizer suggestion — both rejected)
COLD_CALL_PER_RAISE = 0.20         # Tier 3 calibrated (was 0.16)
COLD_CALL_PER_OPP = 0.07           # Tier 3 calibrated (was 0.04)
RULE5_DRAW_BYPASS = 7              # GTO Expert approved (Round 4)

# Pot odds override threshold (Rule 6)
POT_ODDS_THRESHOLD = 0.11          # Round 3 calibrated

# Equity realization — expert-set from solver observations, not calibrated.
# The 0.85 OOP factor is derived from empirical equity realization studies.
# Calibrating this requires separate validation against position-specific solver output.
EQUITY_REALIZATION_IP = 1.00
EQUITY_REALIZATION_OOP = 0.85

# Rule 4 monster draw exception — GTO Expert-set, not calibrated.
# 12+ outs with 40%+ realized equity (combo draw) can bet OOP multiway.
RULE4_MONSTER_DRAW_OUTS = 12     # 12+ outs = monster draw (combo draw)
RULE4_MONSTER_DRAW_EQUITY = 0.40 # 40%+ realized equity required
RULE4_EQUITY_EXCEPTION = 0.65   # Made hands with 65%+ equity bet OOP even with draws

# Sigmoid temperature — controls confidence score smoothness only.
# The binary action decision changes at the 0.5 crossing regardless of temperature.
# Only the AdjustedPrediction.adjustment_confidence value is affected.
SIGMOID_TEMPERATURE = 0.05


def _adjustment_probability(equity, threshold, temperature=0.05):
    """
    Sigmoid function: smooth transition around threshold.
    Returns probability of adjustment (0.0 to 1.0).

    At equity == threshold: returns 0.5
    Below threshold: approaches 1.0 (should adjust)
    Above threshold: approaches 0.0 (should NOT adjust)

    Temperature controls sharpness:
      0.01 = very sharp (nearly binary)
      0.05 = moderate smoothing
      0.10 = very smooth
    """
    z = (threshold - equity) / temperature
    # Clamp to avoid overflow
    z = max(-20, min(20, z))
    return 1.0 / (1.0 + math.exp(-z))


@contextmanager
def override_thresholds(params: dict):
    """Temporarily override adjuster thresholds for calibration.

    Keys match the module-level constant names (lowercase):
        bluff_eq_thresh, value_base, value_per_opp, raise_base, raise_per_opp,
        cold_call_base, cold_call_per_raise, cold_call_per_opp,
        rule5_draw_bypass, pot_odds_thresh, rule1_draw_bypass,
        draw_outs_ip_base, equity_realization_ip, equity_realization_oop,
        sigmoid_temperature, rule4_monster_draw_outs, rule4_monster_draw_equity,
        rule4_equity_exception
    """
    global BLUFF_EQUITY_THRESHOLD, VALUE_BASE_THRESHOLD, VALUE_PER_OPPONENT
    global RAISE_BASE_THRESHOLD, RAISE_PER_OPPONENT
    global COLD_CALL_BASE, COLD_CALL_PER_RAISE, COLD_CALL_PER_OPP
    global RULE5_DRAW_BYPASS, POT_ODDS_THRESHOLD
    global RULE1_DRAW_BYPASS, DRAW_OUTS_IP_BASE
    global EQUITY_REALIZATION_IP, EQUITY_REALIZATION_OOP, SIGMOID_TEMPERATURE
    global RULE4_MONSTER_DRAW_OUTS, RULE4_MONSTER_DRAW_EQUITY, RULE4_EQUITY_EXCEPTION

    old = {
        'BLUFF_EQUITY_THRESHOLD': BLUFF_EQUITY_THRESHOLD,
        'VALUE_BASE_THRESHOLD': VALUE_BASE_THRESHOLD,
        'VALUE_PER_OPPONENT': VALUE_PER_OPPONENT,
        'RAISE_BASE_THRESHOLD': RAISE_BASE_THRESHOLD,
        'RAISE_PER_OPPONENT': RAISE_PER_OPPONENT,
        'COLD_CALL_BASE': COLD_CALL_BASE,
        'COLD_CALL_PER_RAISE': COLD_CALL_PER_RAISE,
        'COLD_CALL_PER_OPP': COLD_CALL_PER_OPP,
        'RULE5_DRAW_BYPASS': RULE5_DRAW_BYPASS,
        'POT_ODDS_THRESHOLD': POT_ODDS_THRESHOLD,
        'RULE1_DRAW_BYPASS': RULE1_DRAW_BYPASS,
        'DRAW_OUTS_IP_BASE': DRAW_OUTS_IP_BASE,
        'EQUITY_REALIZATION_IP': EQUITY_REALIZATION_IP,
        'EQUITY_REALIZATION_OOP': EQUITY_REALIZATION_OOP,
        'SIGMOID_TEMPERATURE': SIGMOID_TEMPERATURE,
        'RULE4_MONSTER_DRAW_OUTS': RULE4_MONSTER_DRAW_OUTS,
        'RULE4_MONSTER_DRAW_EQUITY': RULE4_MONSTER_DRAW_EQUITY,
        'RULE4_EQUITY_EXCEPTION': RULE4_EQUITY_EXCEPTION,
    }

    BLUFF_EQUITY_THRESHOLD = params.get('bluff_eq_thresh', old['BLUFF_EQUITY_THRESHOLD'])
    VALUE_BASE_THRESHOLD = params.get('value_base', old['VALUE_BASE_THRESHOLD'])
    VALUE_PER_OPPONENT = params.get('value_per_opp', old['VALUE_PER_OPPONENT'])
    RAISE_BASE_THRESHOLD = params.get('raise_base', old['RAISE_BASE_THRESHOLD'])
    RAISE_PER_OPPONENT = params.get('raise_per_opp', old['RAISE_PER_OPPONENT'])
    COLD_CALL_BASE = params.get('cold_call_base', old['COLD_CALL_BASE'])
    COLD_CALL_PER_RAISE = params.get('cold_call_per_raise', old['COLD_CALL_PER_RAISE'])
    COLD_CALL_PER_OPP = params.get('cold_call_per_opp', old['COLD_CALL_PER_OPP'])
    RULE5_DRAW_BYPASS = params.get('rule5_draw_bypass', old['RULE5_DRAW_BYPASS'])
    POT_ODDS_THRESHOLD = params.get('pot_odds_thresh', old['POT_ODDS_THRESHOLD'])
    RULE1_DRAW_BYPASS = params.get('rule1_draw_bypass', old['RULE1_DRAW_BYPASS'])
    DRAW_OUTS_IP_BASE = params.get('draw_outs_ip_base', old['DRAW_OUTS_IP_BASE'])
    EQUITY_REALIZATION_IP = params.get('equity_realization_ip', old['EQUITY_REALIZATION_IP'])
    EQUITY_REALIZATION_OOP = params.get('equity_realization_oop', old['EQUITY_REALIZATION_OOP'])
    SIGMOID_TEMPERATURE = params.get('sigmoid_temperature', old['SIGMOID_TEMPERATURE'])
    RULE4_MONSTER_DRAW_OUTS = params.get('rule4_monster_draw_outs', old['RULE4_MONSTER_DRAW_OUTS'])
    RULE4_MONSTER_DRAW_EQUITY = params.get('rule4_monster_draw_equity', old['RULE4_MONSTER_DRAW_EQUITY'])
    RULE4_EQUITY_EXCEPTION = params.get('rule4_equity_exception', old['RULE4_EQUITY_EXCEPTION'])

    try:
        yield
    finally:
        BLUFF_EQUITY_THRESHOLD = old['BLUFF_EQUITY_THRESHOLD']
        VALUE_BASE_THRESHOLD = old['VALUE_BASE_THRESHOLD']
        VALUE_PER_OPPONENT = old['VALUE_PER_OPPONENT']
        RAISE_BASE_THRESHOLD = old['RAISE_BASE_THRESHOLD']
        RAISE_PER_OPPONENT = old['RAISE_PER_OPPONENT']
        COLD_CALL_BASE = old['COLD_CALL_BASE']
        COLD_CALL_PER_RAISE = old['COLD_CALL_PER_RAISE']
        COLD_CALL_PER_OPP = old['COLD_CALL_PER_OPP']
        RULE5_DRAW_BYPASS = old['RULE5_DRAW_BYPASS']
        POT_ODDS_THRESHOLD = old['POT_ODDS_THRESHOLD']
        RULE1_DRAW_BYPASS = old['RULE1_DRAW_BYPASS']
        DRAW_OUTS_IP_BASE = old['DRAW_OUTS_IP_BASE']
        EQUITY_REALIZATION_IP = old['EQUITY_REALIZATION_IP']
        EQUITY_REALIZATION_OOP = old['EQUITY_REALIZATION_OOP']
        SIGMOID_TEMPERATURE = old['SIGMOID_TEMPERATURE']
        RULE4_MONSTER_DRAW_OUTS = old['RULE4_MONSTER_DRAW_OUTS']
        RULE4_MONSTER_DRAW_EQUITY = old['RULE4_MONSTER_DRAW_EQUITY']
        RULE4_EQUITY_EXCEPTION = old['RULE4_EQUITY_EXCEPTION']


@dataclass(frozen=True)
class AdjustedPrediction:
    """Result of multiway adjustment."""
    original_action: str      # Oracle's HU action ("BET", "RAISE", etc.)
    adjusted_action: str      # After multiway adjustment
    was_adjusted: bool        # True if action changed
    adjustment_reason: str    # "bluff_suppression", "value_tightening", etc.
    num_opponents: int        # Number of opponents (1 = HU)
    adjustment_confidence: float = 1.0  # 0.0-1.0, sigmoid confidence of adjustment


def adjust(pred, feat_dict: dict, num_opponents: int) -> AdjustedPrediction:
    """
    Adjust oracle prediction for multiway pots.

    Args:
        pred: OraclePrediction with .action attribute
        feat_dict: {feature_name: value} dict with the 37 model features
        num_opponents: Number of opponents (1=HU, 2-5=multiway)

    Returns:
        AdjustedPrediction with original and potentially adjusted action
    """
    action = pred.action

    # Passthrough for heads-up or invalid
    if num_opponents <= 1:
        return AdjustedPrediction(
            original_action=action,
            adjusted_action=action,
            was_adjusted=False,
            adjustment_reason="",
            num_opponents=num_opponents,
        )

    # Cap opponents for threshold calculation
    n = min(num_opponents, MAX_OPPONENTS_CAP)

    # CHECK is never adjusted
    if action == "CHECK":
        return _passthrough(action, num_opponents)

    # --- Rules 5 & 6: Action-sequence rules (CALL/FOLD before BET/RAISE rules) ---

    # Rule 5: Cold-call tightening (facing raise over bet)
    num_raises = feat_dict.get(F.META_NUM_RAISES, 0)
    if num_raises >= 1 and action == 'CALL':
        equity = max(
            feat_dict.get(F.RAW_EQUITY, 0),
            feat_dict.get(F.EQUITY_VS_RANGE, 0.5),
        )

        # Equity realization: OOP equity is worth less than IP equity
        is_ip_flag = feat_dict.get(F.IS_IP, 0)
        realization_factor = EQUITY_REALIZATION_IP if is_ip_flag else EQUITY_REALIZATION_OOP
        realized_equity = equity * realization_factor

        # Threshold scales with number of raises
        cold_call_threshold = COLD_CALL_BASE + num_raises * COLD_CALL_PER_RAISE
        # Also scale with opponents
        cold_call_threshold += (n - 1) * COLD_CALL_PER_OPP

        adjustment_confidence = _adjustment_probability(
            realized_equity, cold_call_threshold, temperature=SIGMOID_TEMPERATURE)

        if adjustment_confidence > 0.5:
            # Check if hero has a draw worth continuing with
            draw_outs = feat_dict.get(F.DRAW_OUTS, 0)
            if draw_outs < RULE5_DRAW_BYPASS:  # No strong draw
                return _adjusted(action, 'FOLD', 'cold_call_tightening',
                                 num_opponents, adjustment_confidence)

    # Rule 6: Pot odds override (great price to see a flop/card)
    to_call = feat_dict.get(F.TO_CALL, 0)
    pot_size = feat_dict.get(F.POT_SIZE, 0)
    if pot_size > 0 and to_call > 0:
        price_ratio = to_call / pot_size
        if price_ratio < POT_ODDS_THRESHOLD:  # Getting better than ~7:1
            draw_outs = feat_dict.get(F.DRAW_OUTS, 0)
            has_flush_draw = feat_dict.get(F.HAS_FLUSH_DRAW, 0)
            has_straight_draw = feat_dict.get(F.HAS_STRAIGHT_DRAW, 0)
            hand_category = feat_dict.get(F.HAND_CATEGORY, 0)

            # If oracle says FOLD but we're getting great odds with a playable hand
            if action == 'FOLD' and (draw_outs >= 4 or has_flush_draw
                                     or has_straight_draw or hand_category >= 1):
                return _adjusted(action, 'CALL', 'pot_odds_override', num_opponents)

    # FOLD, CALL passthrough (after action-sequence rules)
    if action in ("FOLD", "CALL"):
        return _passthrough(action, num_opponents)

    # Get key features
    equity = max(
        feat_dict.get(F.EQUITY_VS_RANGE, 0),
        feat_dict.get(F.RAW_EQUITY, 0),
    )

    # Equity realization: OOP equity is worth less than IP equity
    is_ip = feat_dict.get(F.IS_IP, 0) > 0.5
    realization_factor = EQUITY_REALIZATION_IP if is_ip else EQUITY_REALIZATION_OOP
    realized_equity = equity * realization_factor

    draw_outs = feat_dict.get(F.DRAW_OUTS, 0)
    facing_bet = feat_dict.get(F.FACING_BET, 0) > 0.5

    # Rule 1: Bluff suppression (highest priority for non-draw hands)
    adjustment_confidence = _adjustment_probability(
        realized_equity, BLUFF_EQUITY_THRESHOLD, temperature=SIGMOID_TEMPERATURE)
    if adjustment_confidence > 0.5:
        # Draw bypass: hands with 6+ outs are not pure bluffs
        # They should fall through to Rule 4 (draw check) for proper evaluation
        if draw_outs >= RULE1_DRAW_BYPASS:
            pass  # Skip bluff suppression, let Rule 4 handle
        elif action == "BET":
            return _adjusted(action, "CHECK", "bluff_suppression",
                             num_opponents, adjustment_confidence)
        elif action == "RAISE":
            return _adjusted(action, "FOLD", "bluff_suppression",
                             num_opponents, adjustment_confidence)

    # Rule 2: Value tightening (BET only)
    if action == "BET":
        value_threshold = VALUE_BASE_THRESHOLD + (n - 1) * VALUE_PER_OPPONENT
        adjustment_confidence = _adjustment_probability(
            realized_equity, value_threshold, temperature=SIGMOID_TEMPERATURE)
        if adjustment_confidence > 0.5:
            return _adjusted(action, "CHECK", "value_tightening",
                             num_opponents, adjustment_confidence)

    # Rule 3: Raise demotion (RAISE only)
    if action == "RAISE":
        raise_threshold = RAISE_BASE_THRESHOLD + (n - 1) * RAISE_PER_OPPONENT
        adjustment_confidence = _adjustment_probability(
            realized_equity, raise_threshold, temperature=SIGMOID_TEMPERATURE)
        if adjustment_confidence > 0.5:
            if facing_bet:
                if realized_equity < BLUFF_EQUITY_THRESHOLD:
                    # Sub-bluff equity: fold, don't call (consistent with Rule 1)
                    return _adjusted(action, "FOLD", "raise_demotion_to_fold",
                                     num_opponents, adjustment_confidence)
                else:
                    return _adjusted(action, "CALL", "raise_demotion",
                                     num_opponents, adjustment_confidence)
            else:
                return _adjusted(action, "CHECK", "raise_demotion",
                                 num_opponents, adjustment_confidence)

    # Rule 4: Draw check (OOP semi-bluff suppression)
    if action == "BET" and draw_outs > 0:
        if not is_ip:
            # Monster draw exception: 12+ outs with 40%+ realized equity
            if draw_outs >= RULE4_MONSTER_DRAW_OUTS and realized_equity >= RULE4_MONSTER_DRAW_EQUITY:
                pass  # Skip OOP veto
            # Equity exception: strong made hands (65%+) with incidental draws bet for value
            elif realized_equity >= RULE4_EQUITY_EXCEPTION:
                pass  # Skip OOP veto — hand is primarily a value bet
            else:
                return _adjusted(action, "CHECK", "draw_check", num_opponents)
        else:
            # IP with draws: need enough outs
            ip_threshold = DRAW_OUTS_IP_BASE + (n - 1) * DRAW_OUTS_IP_PER_OPPONENT
            if draw_outs < ip_threshold:
                return _adjusted(action, "CHECK", "draw_check", num_opponents)

    # No adjustment needed
    return _passthrough(action, num_opponents)


def _passthrough(action: str, num_opponents: int) -> AdjustedPrediction:
    return AdjustedPrediction(
        original_action=action,
        adjusted_action=action,
        was_adjusted=False,
        adjustment_reason="",
        num_opponents=num_opponents,
    )


def _adjusted(original: str, adjusted: str, reason: str, num_opponents: int,
              adjustment_confidence: float = 1.0) -> AdjustedPrediction:
    _logger.info("Multiway override: %s → %s (reason=%s, n_opp=%d, conf=%.2f)",
                 original, adjusted, reason, num_opponents, adjustment_confidence)
    return AdjustedPrediction(
        original_action=original,
        adjusted_action=adjusted,
        was_adjusted=True,
        adjustment_reason=reason,
        num_opponents=num_opponents,
        adjustment_confidence=adjustment_confidence,
    )
