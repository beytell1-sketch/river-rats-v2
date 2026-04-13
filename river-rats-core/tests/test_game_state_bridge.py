"""Tests for game_state_bridge — live game state to 38-feature dict.

Blocker 3: build_features_from_game_state() must produce a valid
feature dict from a running PokerGame instance. The bridge is
postflop-only — preflop uses the range-table engine.
"""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from poker_game import PokerGame
from game_state_bridge import build_features_from_game_state
from feature_keys import F
from gto_model import GtoOracle, FEATURE_COLUMNS


MODEL_FEATURES = set(FEATURE_COLUMNS)


def _make_postflop_callback(captured: dict):
    """Create a callback that captures features on first postflop decision.
    Uses preflop heuristic for preflop, captures + checks/folds postflop."""
    def callback(game, player, context):
        if context.get('street') == 'preflop':
            # Use default preflop heuristic
            from poker_game import ai_preflop_decision
            preflop_state = {
                'num_raises_this_street': context.get('num_raises_this_street', 0),
                'num_callers': context.get('num_callers', 0),
                'hero_has_raised': False,
                'hero_position': player.position,
                'to_call': context['to_call'],
                'opener_position': context.get('opener_position'),
            }
            return ai_preflop_decision(
                player, context['current_bet'], context['pot'], preflop_state
            )
        # Postflop: capture features
        if not captured:
            feat = build_features_from_game_state(player, game, context)
            captured['features'] = feat
            captured['context'] = context
            captured['player'] = player
        if context.get('to_call', 0) > 0:
            return ('fold', 0)
        return ('check', 0)
    return callback


class TestBridgeBasic:
    """build_features_from_game_state returns a valid feature dict on postflop."""

    def _run_and_capture(self):
        captured = {}
        cb = _make_postflop_callback(captured)
        game = PokerGame(headless=True)
        for p in game.players:
            p.decision_callback = cb
        for _ in range(50):
            game.play_hand()
            if captured:
                break
        assert captured, "Failed to reach postflop in 50 hands"
        return captured

    def test_returns_dict(self):
        result = self._run_and_capture()
        assert isinstance(result['features'], dict)

    def test_contains_all_38_model_features(self):
        result = self._run_and_capture()
        feat = result['features']
        missing = MODEL_FEATURES - set(feat.keys())
        assert missing == set(), f"Missing model features: {missing}"

    def test_features_are_numeric(self):
        result = self._run_and_capture()
        feat = result['features']
        for key in MODEL_FEATURES:
            val = feat[key]
            assert isinstance(val, (int, float)), \
                f"Feature {key} has non-numeric value: {val!r} ({type(val)})"

    def test_contains_num_opponents(self):
        result = self._run_and_capture()
        feat = result['features']
        assert F.NUM_OPPONENTS in feat

    def test_num_opponents_at_least_1(self):
        result = self._run_and_capture()
        feat = result['features']
        assert feat[F.NUM_OPPONENTS] >= 1


class TestBridgeWithOracle:
    """Feature dict is compatible with GtoOracle.features_from_dict()."""

    def test_features_from_dict_succeeds(self):
        captured = {}
        cb = _make_postflop_callback(captured)
        game = PokerGame(headless=True)
        for p in game.players:
            p.decision_callback = cb
        for _ in range(30):
            game.play_hand()
            if captured:
                break
        assert captured, "Failed to reach postflop"
        feat = captured['features']
        arr = GtoOracle.features_from_dict(feat)
        # gto_model.FEATURE_COLUMNS is 54: Phase 3A promoted features 49-54
        # (hero_range_percentile, has_showdown_value, villain_fold_equity_estimate,
        # flush_draw_rank, is_preflop_aggressor, villain_medium_made_pct).
        assert arr.shape == (54,)
        import numpy as np
        assert all(isinstance(v, (int, float, np.floating, np.integer)) for v in arr)


class TestBridgePreflop:
    """Bridge correctly rejects preflop calls."""

    def test_preflop_raises_error(self):
        captured = {'error': None}

        def spy_callback(game, player, context):
            if context.get('street') == 'preflop' and captured['error'] is None:
                try:
                    build_features_from_game_state(player, game, context)
                except ValueError as e:
                    captured['error'] = str(e)
            return ('fold', 0)

        game = PokerGame(headless=True)
        for p in game.players:
            p.decision_callback = spy_callback
        game.play_hand()
        assert captured['error'] is not None
        assert 'postflop-only' in captured['error']


class TestBridgePostflop:
    """Bridge handles postflop state correctly."""

    def test_postflop_has_board_features(self):
        captured = {}
        cb = _make_postflop_callback(captured)
        game = PokerGame(headless=True)
        for p in game.players:
            p.decision_callback = cb
        for _ in range(30):
            game.play_hand()
            if captured:
                break
        if captured:
            feat = captured['features']
            has_texture = (
                feat.get('is_monotone', 0) +
                feat.get('is_two_tone', 0) +
                feat.get('is_rainbow', 0)
            )
            assert has_texture > 0


class TestBridgeEndToEnd:
    """Full decision_callback using the bridge to make oracle-driven decisions."""

    def test_oracle_driven_hand_completes(self):
        oracle_path = os.path.join(
            os.path.dirname(__file__), '..', 'models', 'gto_model_v8_38feat.json'
        )
        if not os.path.exists(oracle_path):
            pytest.skip("Model file not available")

        from preflop_engine import decide_preflop, detect_scenario

        oracle = GtoOracle(oracle_path)
        decisions = []

        def oracle_callback(game, player, context):
            if context.get('street') == 'preflop':
                # Use preflop engine for preflop decisions
                preflop_state = {
                    'num_raises_this_street': context.get('num_raises_this_street', 0),
                    'num_callers': context.get('num_callers', 0),
                    'hero_has_raised': False,
                    'hero_position': player.position,
                    'to_call': context['to_call'],
                    'opener_position': context.get('opener_position'),
                }
                from poker_game import ai_preflop_decision
                action, amount = ai_preflop_decision(
                    player, context['current_bet'], context['pot'], preflop_state
                )
                decisions.append((player.position, 'preflop', action))
                return (action, amount)

            # Postflop: use oracle
            feat_dict = build_features_from_game_state(player, game, context)
            features = GtoOracle.features_from_dict(feat_dict)
            pred = oracle.predict(features)
            action = pred.action.lower()
            decisions.append((player.position, context['street'], action))

            if action in ('fold', 'check'):
                return (action, 0)
            elif action == 'call':
                return ('call', game.current_bet)
            else:
                amount = player.bet_this_street + max(int(context['pot'] * 0.67), 10)
                amount = min(amount, player.stack + player.bet_this_street)
                return (action, amount)

        game = PokerGame(headless=True)
        game.players[0].decision_callback = oracle_callback
        for _ in range(5):
            game.play_hand()
        assert game.hand_number == 5
        assert len(decisions) > 0
