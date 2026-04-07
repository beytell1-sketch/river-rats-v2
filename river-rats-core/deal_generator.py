"""Duplicate deal generator for self-play.

Produces reproducible deals from a seed. Each deal specifies hole cards
for all 6 seats and a 5-card board runout. The same deal is played on
all tables — only the hero oracle variant differs.

Usage:
    from deal_generator import DealGenerator, Deal

    gen = DealGenerator(seed=42)
    deals = gen.generate(n=1000)

    # Each deal has:
    #   deal.hole_cards  — {position: [card1, card2]}
    #   deal.board       — [flop1, flop2, flop3, turn, river]
    #   deal.deck        — pre-stacked deck for PokerGame injection
"""
from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

# Card constants — must match poker_game.py
RANKS = '23456789TJQKA'
SUITS = 'shdc'
POSITIONS = ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']

# Deal order matches poker_game.py deal_hand(): 2 rounds of UTG→BB
DEAL_ORDER = POSITIONS * 2  # 12 pops for hole cards


@dataclass
class Deal:
    """A single predetermined deal for all 6 seats."""
    deal_id: int
    hole_cards: Dict[str, List[str]]  # {position: [card_str, card_str]}
    board: List[str]                   # [flop1, flop2, flop3, turn, river]
    _remaining: List[str] = field(repr=False, default_factory=list)

    def make_stacked_deck(self) -> List[str]:
        """Build a deck where pop() yields the predetermined cards.

        The deck is a list where the LAST element is popped first.
        poker_game.py dealing order:
          - 12 pops: hole cards (2 rounds of UTG→BB)
          - 1 burn + 3 pops: flop
          - 1 burn + 1 pop: turn
          - 1 burn + 1 pop: river
          - remaining cards fill the rest (never dealt)

        Total from top: 12 + 1 + 3 + 1 + 1 + 1 + 1 = 20 cards.
        """
        # Build the top of deck in deal order (first popped = last in list)
        top_cards = []

        # Hole cards: 2 rounds of UTG→BB
        # Round 1: one card per position, Round 2: second card per position
        for round_idx in range(2):
            for pos in POSITIONS:
                top_cards.append(self.hole_cards[pos][round_idx])

        # Burn + flop (3 cards)
        top_cards.append('__burn1__')  # placeholder, replaced below
        top_cards.extend(self.board[:3])

        # Burn + turn
        top_cards.append('__burn2__')
        top_cards.append(self.board[3])

        # Burn + river
        top_cards.append('__burn3__')
        top_cards.append(self.board[4])

        # Replace burn placeholders with unused cards
        used = set(top_cards) - {'__burn1__', '__burn2__', '__burn3__'}
        unused = [c for c in self._remaining if c not in used]
        burn_idx = 0
        for i, c in enumerate(top_cards):
            if c.startswith('__burn'):
                top_cards[i] = unused[burn_idx]
                burn_idx += 1

        # Remaining unused cards go at the bottom (never dealt)
        remaining_unused = unused[burn_idx:]

        # Deck is reversed because pop() takes from the end
        deck_list = remaining_unused + list(reversed(top_cards))
        return deck_list

    def make_card_deck(self) -> list:
        """Build a stacked deck of Card objects for PokerGame injection."""
        return [_str_to_card(s) for s in self.make_stacked_deck()]


def _str_to_card(card_str: str):
    """Convert a card string like 'Ah' to a poker_game.Card object."""
    from poker_game import Card
    return Card(card_str[0], card_str[1])


class DealGenerator:
    """Generates reproducible deals from a seed."""

    def __init__(self, seed: int = 0):
        self.seed = seed
        self._rng = random.Random(seed)

    def generate(self, n: int) -> List[Deal]:
        """Generate n deals."""
        return [self._one_deal(i) for i in range(n)]

    def _one_deal(self, deal_id: int) -> Deal:
        """Generate a single deal."""
        # Full deck as strings
        all_cards = [f'{r}{s}' for r in RANKS for s in SUITS]
        self._rng.shuffle(all_cards)

        # Deal hole cards: 2 cards per position
        idx = 0
        hole_cards = {}
        for pos in POSITIONS:
            hole_cards[pos] = [all_cards[idx], all_cards[idx + 1]]
            idx += 2

        # Board: 5 cards
        board = all_cards[idx:idx + 5]
        idx += 5

        # Remaining cards (for burns and padding)
        remaining = all_cards[idx:]

        deal = Deal(
            deal_id=deal_id,
            hole_cards=hole_cards,
            board=board,
            _remaining=remaining,
        )
        return deal

    def reset(self, seed: int = None) -> None:
        """Reset the generator with a new or same seed."""
        if seed is not None:
            self.seed = seed
        self._rng = random.Random(self.seed)
