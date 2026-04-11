"""Tests for hand_logger — per-hand outcome logging.

Blocker 5: Record board, hole cards, actions, chip movement per hand.
"""
import sys, os, json, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from poker_game import PokerGame
from hand_logger import HandLogger, HandRecord, ActionRecord


class TestHandLoggerBasic:
    """HandLogger records actions and hand outcomes."""

    def _run_logged_hands(self, n=5):
        logger = HandLogger()
        game = PokerGame(headless=True, ai_callback=logger.on_action)
        for _ in range(n):
            logger.start_hand(game)
            game.play_hand()
            logger.end_hand(game)
        return logger, game

    def test_records_hands(self):
        logger, _ = self._run_logged_hands(5)
        assert len(logger.hands) == 5

    def test_records_actions(self):
        logger, _ = self._run_logged_hands(5)
        assert len(logger.actions) > 0

    def test_hand_record_structure(self):
        logger, _ = self._run_logged_hands(1)
        hand = logger.hands[0]
        assert isinstance(hand, HandRecord)
        assert hand.hand_id == 1
        assert isinstance(hand.board, list)
        assert isinstance(hand.players, list)
        assert len(hand.players) == 6
        assert isinstance(hand.winners, list)
        assert len(hand.winners) > 0

    def test_action_record_structure(self):
        logger, _ = self._run_logged_hands(1)
        action = logger.actions[0]
        assert isinstance(action, ActionRecord)
        assert action.hand_id == 1
        assert action.street in ('preflop', 'flop', 'turn', 'river')
        assert action.action in ('fold', 'check', 'call', 'bet', 'raise')

    def test_player_has_hole_cards(self):
        logger, _ = self._run_logged_hands(1)
        hand = logger.hands[0]
        for p in hand.players:
            assert 'hole_cards' in p
            assert isinstance(p['hole_cards'], list)
            assert len(p['hole_cards']) == 2

    def test_stack_tracking(self):
        logger, _ = self._run_logged_hands(1)
        hand = logger.hands[0]
        for p in hand.players:
            assert 'stack_before' in p
            assert 'stack_after' in p
            assert isinstance(p['stack_before'], int)
            assert isinstance(p['stack_after'], int)

    def test_chips_conserved(self):
        logger, _ = self._run_logged_hands(1)
        hand = logger.hands[0]
        total_before = sum(p['stack_before'] for p in hand.players)
        total_after = sum(p['stack_after'] for p in hand.players)
        assert total_before == total_after


class TestHandLoggerWithCallbacks:
    """Logger works alongside decision_callbacks."""

    def test_logs_callback_driven_actions(self):
        logger = HandLogger()

        def always_fold(game, player, context):
            return ('fold', 0)

        game = PokerGame(headless=True, ai_callback=logger.on_action)
        game.players[0].decision_callback = always_fold

        logger.start_hand(game)
        game.play_hand()
        logger.end_hand(game)

        # The callback player's folds should be logged
        p0_actions = [a for a in logger.actions if a.player_name == game.players[0].name]
        assert len(p0_actions) > 0
        assert all(a.action == 'fold' for a in p0_actions)


class TestHandLoggerJSONL:
    """Logger writes valid JSONL files."""

    def test_hands_jsonl(self):
        logger, _ = TestHandLoggerBasic()._run_logged_hands(3)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            path = f.name
        logger.to_jsonl(path)

        with open(path) as f:
            lines = f.readlines()
        assert len(lines) == 3

        for line in lines:
            record = json.loads(line)
            assert 'hand_id' in record
            assert 'board' in record
            assert 'players' in record
            assert 'winners' in record

        os.unlink(path)

    def test_actions_jsonl(self):
        logger, _ = TestHandLoggerBasic()._run_logged_hands(2)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            path = f.name
        logger.actions_to_jsonl(path)

        with open(path) as f:
            lines = f.readlines()
        assert len(lines) == len(logger.actions)

        for line in lines:
            record = json.loads(line)
            assert 'hand_id' in record
            assert 'action' in record
            assert 'player_name' in record

        os.unlink(path)


class TestHandLoggerClear:
    """Logger can be cleared and reused."""

    def test_clear(self):
        logger, _ = TestHandLoggerBasic()._run_logged_hands(3)
        assert len(logger.hands) == 3
        logger.clear()
        assert len(logger.hands) == 0
        assert len(logger.actions) == 0
