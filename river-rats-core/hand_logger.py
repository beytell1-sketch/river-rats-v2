"""Per-hand outcome logging for self-play.

Records every action and hand outcome in a structured format.
Foundation for the observer flag system in the self-play loop.

Usage:
    from hand_logger import HandLogger

    logger = HandLogger()
    game = PokerGame(headless=True, ai_callback=logger.on_action)
    game.play_hand()
    logger.end_hand(game)   # call after each play_hand()

    # Access records
    logger.hands      # list of hand records
    logger.actions    # list of action records
    logger.to_jsonl("output.jsonl")   # write JSONL
"""
from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional


@dataclass
class ActionRecord:
    """One player action within a hand."""
    hand_id: int
    street: str
    player_name: str
    player_position: str
    action: str
    amount: int
    pot_before: int
    current_bet: int
    num_active: int


@dataclass
class HandRecord:
    """Summary of one complete hand."""
    hand_id: int
    board: List[str]
    players: List[Dict]       # [{name, position, hole_cards, stack_before, stack_after}]
    winners: List[Dict]       # [{name, amount, reason}]
    pot_total: int
    went_to_showdown: bool
    num_players_saw_flop: int


class HandLogger:
    """Accumulates per-action and per-hand records across a session."""

    def __init__(self):
        self.hands: List[HandRecord] = []
        self.actions: List[ActionRecord] = []
        self._current_hand_actions: List[ActionRecord] = []
        self._stacks_at_start: Dict[str, int] = {}
        self._hand_started = False

    def start_hand(self, game) -> None:
        """Call before play_hand() to snapshot starting state."""
        self._stacks_at_start = {p.name: p.stack for p in game.players}
        self._current_hand_actions = []
        self._hand_started = True

    def on_action(self, game, player, action: str, amount: int) -> None:
        """ai_callback hook — called after every AI decision."""
        active = [p for p in game.players if not p.is_folded]
        record = ActionRecord(
            hand_id=game.hand_number,
            street=game.street,
            player_name=player.name,
            player_position=player.position,
            action=action,
            amount=amount,
            pot_before=game.pot,
            current_bet=game.current_bet,
            num_active=len(active),
        )
        self._current_hand_actions.append(record)
        self.actions.append(record)

    def end_hand(self, game) -> HandRecord:
        """Call after play_hand() to record the hand outcome."""
        # Build player records
        players = []
        for p in game.players:
            players.append({
                'name': p.name,
                'position': p.position,
                'hole_cards': [str(c) for c in p.hole_cards],
                'stack_before': self._stacks_at_start.get(p.name, 0),
                'stack_after': p.stack,
                'folded': p.is_folded,
            })

        # Count players who saw flop (had actions on flop or later)
        flop_players = set()
        for a in self._current_hand_actions:
            if a.street != 'preflop':
                flop_players.add(a.player_name)

        # Went to showdown if multiple players not folded
        not_folded = [p for p in game.players if not p.is_folded]
        went_to_showdown = len(not_folded) > 1 and len(game.community_cards) == 5

        record = HandRecord(
            hand_id=game.hand_number,
            board=[str(c) for c in game.community_cards],
            players=players,
            winners=list(game.last_winners),
            pot_total=game.last_pot,
            went_to_showdown=went_to_showdown,
            num_players_saw_flop=len(flop_players),
        )
        self.hands.append(record)
        self._hand_started = False
        return record

    def to_jsonl(self, path: str) -> None:
        """Write all hand records as JSONL."""
        with open(path, 'w') as f:
            for hand in self.hands:
                f.write(json.dumps(asdict(hand)) + '\n')

    def actions_to_jsonl(self, path: str) -> None:
        """Write all action records as JSONL."""
        with open(path, 'w') as f:
            for action in self.actions:
                f.write(json.dumps(asdict(action)) + '\n')

    def clear(self) -> None:
        """Reset all records."""
        self.hands.clear()
        self.actions.clear()
        self._current_hand_actions.clear()
        self._stacks_at_start.clear()
