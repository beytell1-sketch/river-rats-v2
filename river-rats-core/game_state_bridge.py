"""Bridge between live game state and the 38-feature extraction pipeline.

This module provides build_features_from_game_state() which converts
a live PokerGame + Player + context dict into the feature dict that
GtoOracle.predict() consumes.

Usage in a decision_callback:

    from game_state_bridge import build_features_from_game_state
    from gto_model import GtoOracle

    oracle = GtoOracle("models/gto_model_v8_38feat.json")

    def oracle_callback(game, player, context):
        feat_dict = build_features_from_game_state(player, game, context)
        features = GtoOracle.features_from_dict(feat_dict)
        pred = oracle.predict(features)
        action = pred.action.lower()
        ...
        return (action, amount)
"""
from __future__ import annotations
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    pass  # No runtime imports from poker_game to avoid circular deps

from feature_keys import F
from feature_extractor import extract_all_features


STREET_MAP = {'preflop': 'p', 'flop': 'f', 'turn': 't', 'river': 'r'}


def build_features_from_game_state(player, game, context: dict) -> Dict:
    """
    Convert live game state into a full 45-feature dict.

    Args:
        player: The Player object making the decision.
        game: The PokerGame instance.
        context: The context dict passed to decision_callback (see Blocker 2).

    Returns:
        Feature dict with all 45 model features plus metadata keys.
        Ready for GtoOracle.features_from_dict() → GtoOracle.predict().
    """
    # Preflop guard: the XGBoost model is postflop-only.
    # Preflop decisions use the range-table engine (decide_preflop), not the oracle.
    street = context.get('street', 'flop')
    if street == 'preflop':
        raise ValueError(
            "build_features_from_game_state() is postflop-only. "
            "Use preflop_engine.decide_preflop() for preflop decisions."
        )

    # Hero cards and board as strings
    hero_card_str = ''.join(str(c) for c in player.hole_cards)
    board_str = ''.join(str(c) for c in game.community_cards)

    # Resolve villain position
    # Priority: bettor_position from context > largest-stack active opponent > 'BB'
    active_opps = context.get('active_opponents', [])
    num_opponents = max(1, len([p for p in active_opps if not p.is_folded]))

    facing_bet = context.get('facing_bet', False)
    bettor_position = None

    if facing_bet:
        # Try to find who made the bet: the opponent with highest bet_this_street
        betting_villains = [
            p for p in active_opps
            if not p.is_folded and p.bet_this_street == context.get('current_bet', 0)
        ]
        if betting_villains:
            bettor_position = betting_villains[0].position

    # Villain position for range analysis
    if bettor_position:
        vp = bettor_position
    elif active_opps:
        non_folded = [p for p in active_opps if not p.is_folded]
        if non_folded:
            vp = max(non_folded, key=lambda p: p.stack).position
        else:
            vp = 'BB'
    else:
        vp = 'BB'

    # Street code
    street_code = STREET_MAP.get(street, 'f')

    # Opener position
    opener_position = context.get('opener_position') or getattr(game, 'opener_position', '') or None

    # Number of raises
    num_raises = context.get('num_raises_this_street', getattr(game, 'raises_this_street', 0))

    # Compute action-history features from prior streets
    # Matches PokerBench semantics: count prior streets (not current) where
    # the primary villain bet/raised, checked, or flat-called.
    street_sequence = ['preflop', 'flop', 'turn', 'river']
    current_idx = street_sequence.index(street) if street in street_sequence else 1

    # Filter to primary villain's actions on prior streets (match by position)
    v_actions_by_street: dict = {}
    for s in street_sequence[:current_idx]:
        for name, pos, act in getattr(game, 'street_actions', {}).get(s, []):
            if pos == vp:
                v_actions_by_street.setdefault(s, []).append(act)

    villain_aggression_count = 0
    villain_checked_back = 0
    villain_call_count = 0
    for s, acts in v_actions_by_street.items():
        if any(a in ('bet', 'raise') for a in acts):
            villain_aggression_count += 1
        if 'check' in acts:
            villain_checked_back = 1  # binary: any prior street
        if any(a == 'call' for a in acts):
            villain_call_count += 1

    # Current-street action features (v9)
    # num_callers_to_bet: count actual 'call' actions on this street from opponents
    # (not the bettor, not hero). Uses street_actions, not chip amounts, to
    # distinguish cold-callers from raisers.
    if facing_bet and hasattr(game, 'street_actions'):
        current_actions = game.street_actions.get(street, [])
        num_callers_to_bet = sum(
            1 for name, pos, act in current_actions
            if act == 'call' and pos != player.position and pos != bettor_position
        )
    else:
        num_callers_to_bet = 0

    # facing_raise: hero faces a raise-level action (not just an initial bet).
    # Captures check-raises (MW-31), re-raises, etc.
    facing_raise = int(facing_bet and num_raises > 0)

    # is_3bet_pot: 2+ bet/raise actions preflop = 3-bet pot
    # had_preflop_raise: any bet/raise preflop (single raise or more)
    pf_actions = getattr(game, 'street_actions', {}).get('preflop', [])
    pf_raise_count = sum(1 for _, _, a in pf_actions if a in ('bet', 'raise'))
    is_3bet = int(pf_raise_count >= 2)
    # had_preflop_open removed — oracle always plays opened pots

    # Build the hand dict in the format extract_all_features() expects
    hand = {
        'h': hero_card_str,
        'b': board_str,
        'pos': player.position,
        'vp': vp,
        'pot': float(context.get('pot', 0)),
        'tc': float(context.get('to_call', 0)),
        'st': street_code,
        'fb': int(bool(facing_bet)),
        'exp': 'C',  # placeholder label, not used by model
        F.META_NUM_OPPONENTS: num_opponents,
        F.META_NUM_RAISES: num_raises,
        F.META_OPENER_POSITION: opener_position,
        F.META_BETTOR_POSITION: bettor_position,
        '_villain_aggression_count': villain_aggression_count,
        '_villain_checked_back': villain_checked_back,
        '_villain_call_count': villain_call_count,
        '_num_callers_to_bet': num_callers_to_bet,
        '_facing_raise': facing_raise,
        '_is_3bet_pot': is_3bet,
    }

    # Run the full feature extraction pipeline
    features = extract_all_features(hand)

    return features
