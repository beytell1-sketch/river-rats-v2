"""Tests for deal_generator — reproducible duplicate deals."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from deal_generator import DealGenerator, Deal
from poker_game import PokerGame, Card


class TestDealGeneration:
    """DealGenerator produces valid, reproducible deals."""

    def test_generates_n_deals(self):
        gen = DealGenerator(seed=42)
        deals = gen.generate(100)
        assert len(deals) == 100

    def test_each_deal_has_6_positions(self):
        gen = DealGenerator(seed=42)
        deal = gen.generate(1)[0]
        assert set(deal.hole_cards.keys()) == {'UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB'}

    def test_each_position_has_2_cards(self):
        gen = DealGenerator(seed=42)
        deal = gen.generate(1)[0]
        for pos, cards in deal.hole_cards.items():
            assert len(cards) == 2, f"{pos} has {len(cards)} cards"

    def test_board_has_5_cards(self):
        gen = DealGenerator(seed=42)
        deal = gen.generate(1)[0]
        assert len(deal.board) == 5

    def test_no_duplicate_cards_in_deal(self):
        gen = DealGenerator(seed=42)
        deal = gen.generate(1)[0]
        all_cards = []
        for cards in deal.hole_cards.values():
            all_cards.extend(cards)
        all_cards.extend(deal.board)
        assert len(all_cards) == len(set(all_cards)), "Duplicate cards found"

    def test_reproducible_with_same_seed(self):
        gen1 = DealGenerator(seed=99)
        gen2 = DealGenerator(seed=99)
        deals1 = gen1.generate(10)
        deals2 = gen2.generate(10)
        for d1, d2 in zip(deals1, deals2):
            assert d1.hole_cards == d2.hole_cards
            assert d1.board == d2.board

    def test_different_seeds_different_deals(self):
        gen1 = DealGenerator(seed=1)
        gen2 = DealGenerator(seed=2)
        d1 = gen1.generate(1)[0]
        d2 = gen2.generate(1)[0]
        # Extremely unlikely to be identical
        assert d1.hole_cards != d2.hole_cards or d1.board != d2.board

    def test_reset_reproduces(self):
        gen = DealGenerator(seed=42)
        deals1 = gen.generate(5)
        gen.reset()
        deals2 = gen.generate(5)
        for d1, d2 in zip(deals1, deals2):
            assert d1.hole_cards == d2.hole_cards


class TestStackedDeck:
    """Deal.make_stacked_deck() produces a deck that yields the right cards."""

    def test_stacked_deck_has_52_cards(self):
        gen = DealGenerator(seed=42)
        deal = gen.generate(1)[0]
        deck = deal.make_stacked_deck()
        assert len(deck) == 52

    def test_stacked_deck_no_duplicates(self):
        gen = DealGenerator(seed=42)
        deal = gen.generate(1)[0]
        deck = deal.make_stacked_deck()
        assert len(deck) == len(set(deck))

    def test_stacked_deck_yields_correct_hole_cards(self):
        """Popping from stacked deck gives the right hole cards."""
        gen = DealGenerator(seed=42)
        deal = gen.generate(1)[0]
        deck = list(deal.make_stacked_deck())  # copy

        # Simulate poker_game.py dealing: 2 rounds of UTG→BB
        positions = ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']
        dealt = {pos: [] for pos in positions}
        for _ in range(2):
            for pos in positions:
                dealt[pos].append(deck.pop())

        for pos in positions:
            assert dealt[pos] == deal.hole_cards[pos], \
                f"{pos}: got {dealt[pos]}, expected {deal.hole_cards[pos]}"

    def test_stacked_deck_yields_correct_board(self):
        """After dealing hole cards, burn+flop+burn+turn+burn+river match."""
        gen = DealGenerator(seed=42)
        deal = gen.generate(1)[0]
        deck = list(deal.make_stacked_deck())

        # Pop 12 hole cards
        for _ in range(12):
            deck.pop()

        # Flop: burn 1, deal 3
        deck.pop()  # burn
        flop = [deck.pop() for _ in range(3)]

        # Turn: burn 1, deal 1
        deck.pop()  # burn
        turn = deck.pop()

        # River: burn 1, deal 1
        deck.pop()  # burn
        river = deck.pop()

        assert flop == deal.board[:3]
        assert turn == deal.board[3]
        assert river == deal.board[4]


class TestDealInjection:
    """Stacked deck integrates with PokerGame via deck_override."""

    def test_game_uses_deck_override(self):
        """PokerGame.deal_hand(deck_override=...) deals predetermined cards."""
        gen = DealGenerator(seed=42)
        deal = gen.generate(1)[0]

        game = PokerGame(headless=True)
        game.deal_hand(deck_override=deal.make_card_deck())

        for pos in ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']:
            p = game._player_at(pos)
            actual = [str(c) for c in p.hole_cards]
            expected = deal.hole_cards[pos]
            assert actual == expected, f"{pos}: got {actual}, expected {expected}"

    def test_play_hand_with_deck_override(self):
        """A full hand plays correctly with deck_override."""
        gen = DealGenerator(seed=42)
        deal = gen.generate(1)[0]

        game = PokerGame(headless=True)
        game.play_hand(deck_override=deal.make_card_deck())
        assert game.hand_number == 1

    def test_two_games_same_deal_same_cards(self):
        """Two separate games with the same deal get identical cards."""
        gen = DealGenerator(seed=42)
        deal = gen.generate(1)[0]

        cards = {}
        for table_id in range(2):
            game = PokerGame(headless=True)
            game.deal_hand(deck_override=deal.make_card_deck())
            cards[table_id] = {
                pos: [str(c) for c in game._player_at(pos).hole_cards]
                for pos in ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']
            }

        assert cards[0] == cards[1]

    def test_no_double_blind_posting(self):
        """deck_override doesn't cause double blind posting."""
        gen = DealGenerator(seed=42)
        deal = gen.generate(1)[0]

        game = PokerGame(headless=True)
        game.deal_hand(deck_override=deal.make_card_deck())

        # SB should have posted exactly 5, BB exactly 10
        sb = game._player_at('SB')
        bb = game._player_at('BB')
        assert sb.stack == 995, f"SB stack {sb.stack}, expected 995"
        assert bb.stack == 990, f"BB stack {bb.stack}, expected 990"
        assert game.pot == 15
