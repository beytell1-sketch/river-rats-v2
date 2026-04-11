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
    Convert live game state into a full 38-feature dict.

    Args:
        player: The Player object making the decision.
        game: The PokerGame instance.
        context: The context dict passed to decision_callback (see Blocker 2).

    Returns:
        Feature dict with all 38 model features plus metadata keys.
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
    }

    # Run the full feature extraction pipeline
    features = extract_all_features(hand)

    return features
