"""Tests for headless (all-AI, no hero) game operation.

Blocker 1: The game engine must support self.hero = None so that
6 AI players can compete without a human player.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from poker_game import PokerGame, Player


class TestHeadlessConstruction:
    """PokerGame can be created with no hero player."""

    def test_no_hero_construction(self):
        game = PokerGame(headless=True)
        assert game.hero is None
        assert len(game.players) == 6
        assert all(not p.is_hero for p in game.players)

    def test_hero_construction_still_works(self):
        game = PokerGame(headless=False)
        assert game.hero is not None
        assert game.hero.is_hero is True

    def test_default_is_not_headless(self):
        game = PokerGame()
        assert game.hero is not None


class TestHeadlessRotation:
    """Position rotation works without a hero."""

    def test_rotate_no_hero(self):
        game = PokerGame(headless=True)
        positions_before = [p.position for p in game.players]
        game.rotate_positions()
        positions_after = [p.position for p in game.players]
        assert positions_before != positions_after
        assert game.hero is None


class TestHeadlessPlayHand:
    """A full hand completes with all AI players."""

    def test_play_one_hand_headless(self):
        game = PokerGame(headless=True)
        result = game.play_hand()
        assert result is True
        assert game.hand_number == 1

    def test_play_multiple_hands_headless(self):
        game = PokerGame(headless=True)
        for _ in range(10):
            game.play_hand()
        assert game.hand_number == 10

    def test_play_hand_with_rotation(self):
        game = PokerGame(headless=True)
        game.play_hand()
        game.rotate_positions()
        game.play_hand()
        assert game.hand_number == 2

    def test_no_output_in_headless(self, capsys):
        game = PokerGame(headless=True)
        game.play_hand()
        captured = capsys.readouterr()
        # Headless mode should produce no interactive output
        # (AI decision prints may still occur, but no hero prompts)
        assert "Your cards:" not in captured.out
        assert "Your position:" not in captured.out
        assert "Your stack:" not in captured.out


class TestHeadlessShowdown:
    """Showdown resolves correctly without a hero."""

    def test_showdown_has_winners(self):
        game = PokerGame(headless=True)
        game.play_hand()
        assert len(game.last_winners) > 0

    def test_chips_conserved(self):
        game = PokerGame(headless=True)
        total_before = sum(p.stack for p in game.players)
        game.play_hand()
        total_after = sum(p.stack for p in game.players)
        assert total_before == total_after


class TestHeroCallbackStillWorks:
    """Existing hero_callback path is unaffected."""

    def test_hero_callback_mode(self):
        actions_seen = []

        def callback(game, hero, context):
            actions_seen.append(context.get('street', 'unknown'))
            return ('fold', 0)

        game = PokerGame(hero_callback=callback)
        assert game.hero is not None
        game.play_hand()
        assert len(actions_seen) > 0


class TestPerPlayerDecisionCallback:
    """Blocker 2: Per-player decision_callback overrides ai_decision()."""

    def test_decision_callback_invoked(self):
        calls = []

        def always_fold(game, player, context):
            calls.append(player.name)
            return ('fold', 0)

        game = PokerGame(headless=True)
        target = game.players[0]  # UTG
        target.decision_callback = always_fold
        game.play_hand()
        assert len(calls) > 0
        assert all(name == target.name for name in calls)

    def test_callback_receives_context_keys(self):
        context_seen = {}

        def spy_callback(game, player, context):
            context_seen.update(context)
            return ('fold', 0)

        game = PokerGame(headless=True)
        game.players[0].decision_callback = spy_callback
        game.play_hand()
        expected_keys = {
            'current_bet', 'to_call', 'pot', 'board', 'street',
            'is_preflop', 'facing_bet', 'personality',
            'num_raises_this_street', 'opener_position', 'num_callers',
            'active_opponents', 'hand_number',
        }
        assert expected_keys.issubset(context_seen.keys())

    def test_multiple_players_different_callbacks(self):
        p0_calls = []
        p3_calls = []

        def cb0(game, player, context):
            p0_calls.append(1)
            return ('fold', 0)

        def cb3(game, player, context):
            p3_calls.append(1)
            return ('fold', 0)

        game = PokerGame(headless=True)
        game.players[0].decision_callback = cb0
        game.players[3].decision_callback = cb3
        game.play_hand()
        # Both callbacks should have been invoked (unless one was
        # already folded by position/blind action before their turn)
        assert len(p0_calls) > 0 or len(p3_calls) > 0

    def test_callback_none_falls_back_to_heuristic(self):
        """Players without decision_callback use the default AI."""
        game = PokerGame(headless=True)
        assert all(p.decision_callback is None for p in game.players)
        # Should complete without errors — all players use heuristic
        game.play_hand()
        assert game.hand_number == 1

    def test_ai_callback_still_fires_with_decision_callback(self):
        ai_notifications = []

        def oracle_cb(game, player, context):
            return ('fold', 0)

        def ai_hook(game, player, action, amount):
            ai_notifications.append((player.name, action))

        game = PokerGame(headless=True, ai_callback=ai_hook)
        game.players[0].decision_callback = oracle_cb
        game.play_hand()
        # ai_callback should fire for ALL players including the one with decision_callback
        names_notified = [n for n, _ in ai_notifications]
        assert game.players[0].name in names_notified

    def test_full_hand_completes_with_all_callbacks(self):
        """All 6 players with callbacks — simulates self-play table."""
        def always_fold(game, player, context):
            return ('fold', 0)

        game = PokerGame(headless=True)
        for p in game.players:
            p.decision_callback = always_fold
        game.play_hand()
        assert game.hand_number == 1
        assert len(game.last_winners) > 0
