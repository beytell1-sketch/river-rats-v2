"""
River Rats Poker — 6-player Texas Hold'em with GTO coaching.

Real cards, real poker logic, real coaching at hero's decision points.
Hero is seated at the table; 5 AI opponents use simple heuristic logic.

UX design:
  - Player decides BEFORE seeing coaching (coaching revealed after the action)
  - Single keypress input (1/2/3/Space/q) — no Enter needed
  - Context-appropriate action menus (preflop vs postflop, facing bet vs not)
  - Postflop sizing as % of pot (Small/Standard/Large)
  - Preflop range feedback — tells you after your action if hand was outside GTO range
  - Verdict display after each decision, then coaching on Space
"""

import sys
import os
import random
import tty
import termios
import logging

logger = logging.getLogger(__name__)

# Make sure project root is on the path so feature_extractor and coaching
# imports all resolve against the files in this directory.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from typing import List, Optional, Dict, Tuple

from feature_keys import F
from personality_profiles import (
    PersonalityProfile, TAG, LAG, NIT, CALLING_STATION, MANIAC, FISH,
)
from preflop_engine import decide_preflop, detect_scenario, PreflopDecision
from range_manager import RangeManager
from hand_categories import cards_to_notation

# Module-level RangeManager — initialised once, shared across all calls.
_RANGE_MANAGER = RangeManager()


# ═══════════════════════════════════════════════════════════════════════════
# SINGLE-KEYPRESS INPUT
# ═══════════════════════════════════════════════════════════════════════════

def getch() -> str:
    """Read a single character without waiting for Enter.
    Falls back gracefully when stdin is not a tty (e.g. piped input)."""
    fd = sys.stdin.fileno()
    if not sys.stdin.isatty():
        # Non-interactive mode: read one char normally (or return 'q' on EOF)
        try:
            ch = sys.stdin.read(1)
            return ch if ch else 'q'
        except Exception:
            return 'q'
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    except Exception:
        ch = 'q'
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    # Map Ctrl+C to quit
    if ch == '\x03':
        return 'q'
    return ch


def wait_for_space_or_q() -> str:
    """Block until Space or q is pressed. Returns 'q' if quit requested."""
    while True:
        ch = getch()
        if ch in (' ', 'q', '\r', '\n'):
            return ch


# ═══════════════════════════════════════════════════════════════════════════
# CARD / DECK
# ═══════════════════════════════════════════════════════════════════════════

RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUITS = ['h', 'd', 'c', 's']

RANK_VALUES = {r: i for i, r in enumerate(RANKS)}  # '2'=0 … 'A'=12

# ANSI color codes — red for hearts/diamonds, reset for clubs/spades
_ANSI_RED   = '\033[91m'
_ANSI_RESET = '\033[0m'

# Detect color support
_USE_COLOR = sys.stdout.isatty()


def _suit_display(suit: str) -> str:
    """Return a display string for the suit, with color if supported."""
    symbol = {'h': 'h', 'd': 'd', 'c': 'c', 's': 's'}[suit]
    if _USE_COLOR and suit in ('h', 'd'):
        return f"{_ANSI_RED}{symbol}{_ANSI_RESET}"
    return symbol


class Card:
    __slots__ = ('rank', 'suit')

    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

    # rank_val used by range checks
    @property
    def rank_val(self) -> int:
        return RANK_VALUES[self.rank]

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))


def make_deck() -> List[Card]:
    deck = [Card(r, s) for r in RANKS for s in SUITS]
    random.shuffle(deck)
    return deck


def fmt_card(card: Card) -> str:
    """Display a card like [Ah] with color for red suits."""
    return f"[{card.rank}{_suit_display(card.suit)}]"


def fmt_cards_inline(cards: List[Card]) -> str:
    """Space-separated bracketed cards: [Ah] [Ks]"""
    return ' '.join(fmt_card(c) for c in cards)


def card_str(card: Card) -> str:
    return str(card)


# ═══════════════════════════════════════════════════════════════════════════
# PLAYER
# ═══════════════════════════════════════════════════════════════════════════

POSITIONS = ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']


class Player:
    def __init__(self, name: str, position: str, stack: int, is_hero: bool = False):
        self.name = name
        self.position = position
        self.stack = stack
        self.hole_cards: List[Card] = []
        self.is_hero = is_hero
        self.is_folded = False
        self.is_all_in = False
        self.bet_this_street = 0
        self.total_invested = 0

    def reset_for_hand(self):
        self.hole_cards = []
        self.is_folded = False
        self.is_all_in = False
        self.bet_this_street = 0
        self.total_invested = 0

    def reset_for_street(self):
        self.bet_this_street = 0

    def put_in(self, amount: int) -> int:
        """Commit chips; returns amount actually put in (may be less if all-in)."""
        amount = min(amount, self.stack)
        self.stack -= amount
        self.bet_this_street += amount
        self.total_invested += amount
        if self.stack == 0:
            self.is_all_in = True
        return amount

    def is_active(self) -> bool:
        return not self.is_folded and not self.is_all_in

    def __repr__(self):
        return f"<Player {self.name} {self.position} stack={self.stack}>"


# ═══════════════════════════════════════════════════════════════════════════
# HAND STRENGTH (eval7-based, used by AI and coaching fallback)
# ═══════════════════════════════════════════════════════════════════════════

try:
    import eval7 as _eval7

    def eval7_rank(hole_cards: List[Card], board: List[Card]) -> int:
        """Lower eval7 value = BETTER hand (eval7 convention)."""
        cards = [_eval7.Card(str(c)) for c in hole_cards + board]
        return _eval7.evaluate(cards)

    def hand_strength_0_1(hole_cards: List[Card], board: List[Card]) -> float:
        """
        Normalised strength in [0,1] — higher = stronger hand.
        Monte Carlo equity estimate vs random opponent. Quick: 200 trials.
        """
        used = {str(c) for c in hole_cards + board}
        remaining = [Card(r, s) for r in RANKS for s in SUITS
                     if f"{r}{s}" not in used]
        wins = 0
        trials = 200
        cards_needed = 5 - len(board)
        h = [_eval7.Card(str(c)) for c in hole_cards]
        b = [_eval7.Card(str(c)) for c in board]
        for _ in range(trials):
            sample = random.sample(remaining, 2 + cards_needed)
            opp = sample[:2]
            run_out = sample[2:]
            board_cards = b + [_eval7.Card(str(c)) for c in run_out]
            hero_val = _eval7.evaluate(h + board_cards)
            opp_val = _eval7.evaluate([_eval7.Card(str(c)) for c in opp] + board_cards)
            if hero_val > opp_val:   # higher = better in eval7
                wins += 1
            elif hero_val == opp_val:
                wins += 0.5
        return wins / trials

    EVAL7_AVAILABLE = True

except ImportError:
    EVAL7_AVAILABLE = False

    def eval7_rank(hole_cards, board):
        return 1000

    def hand_strength_0_1(hole_cards, board):
        return 0.5


# ═══════════════════════════════════════════════════════════════════════════
# HAND DESCRIPTION
# ═══════════════════════════════════════════════════════════════════════════

def describe_hand(hole_cards: List[Card], board: List[Card]) -> str:
    if not board:
        r1, r2 = hole_cards[0].rank, hole_cards[1].rank
        s1, s2 = hole_cards[0].suit, hole_cards[1].suit
        if r1 == r2:
            return f"pocket {r1}s"
        suited = "suited" if s1 == s2 else "offsuit"
        return f"{r1}{r2} {suited}"
    try:
        from hand_evaluator import evaluate_hand
        eval_result = evaluate_hand(
            [str(c) for c in hole_cards],
            [str(c) for c in board]
        )
        return eval_result.description or eval_result.category
    except Exception:
        return ""


# ═══════════════════════════════════════════════════════════════════════════
# GTO PREFLOP RANGE
# ═══════════════════════════════════════════════════════════════════════════

GTO_OPEN_PCT = {
    'UTG': 0.13, 'HJ': 0.18, 'CO': 0.26,
    'BTN': 0.44, 'SB': 0.52, 'BB': 1.0,
}


def _rank_char(val: int) -> str:
    """Convert rank value (0-12) to rank character."""
    return RANKS[val]


def hand_in_opening_range(card1: Card, card2: Card, position: str) -> bool:
    """
    Check if hero's hand is in GTO opening range for this position.
    Uses RangeManager when available; falls back to tier-based approximation.
    """
    # Try the real range manager first
    try:
        from range_manager import RangeManager
        from hand_categories import cards_to_notation
        rm = RangeManager()
        notation = cards_to_notation(str(card1), str(card2))
        rfi = rm.get_rfi_range(position)
        freq = rfi.get(notation, 0.0)
        # Treat freq > 0.3 as "in range" — avoids asking about pure mixing spots
        return freq > 0.30
    except Exception:
        pass

    # Fallback: tier-based approximation
    r1, r2 = card1.rank_val, card2.rank_val
    suited = (card1.suit == card2.suit)

    if r1 == r2:
        notation = f"{_rank_char(r1)}{_rank_char(r2)}"
    elif r1 > r2:
        notation = f"{_rank_char(r1)}{_rank_char(r2)}{'s' if suited else 'o'}"
    else:
        notation = f"{_rank_char(r2)}{_rank_char(r1)}{'s' if suited else 'o'}"

    tier1 = {'AA', 'KK', 'QQ', 'JJ', 'AKs', 'AKo'}
    tier2 = tier1 | {'TT', '99', 'AQs', 'AQo', 'AJs', 'KQs'}
    tier3 = tier2 | {'88', '77', 'ATs', 'AJo', 'KJs', 'KQo', 'QJs'}
    tier4 = tier3 | {'66', '55', 'A9s', 'A8s', 'ATo', 'KTs', 'KJo', 'QTs', 'JTs', 'T9s'}
    tier5 = tier4 | {'44', '33', '22', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s', 'A9o',
                     'K9s', 'Q9s', 'J9s', 'T8s', '98s', '87s', '76s', '65s'}
    tier6 = tier5 | {'K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K3s', 'K2s', 'Q8s', 'J8s',
                     'T7s', '97s', '86s', '75s', '54s', 'A8o', 'A7o', 'A6o', 'A5o',
                     'KTo', 'QJo', 'QTo', 'JTo'}

    pct = GTO_OPEN_PCT.get(position, 0.20)
    if pct <= 0.05:  return notation in tier1
    if pct <= 0.13:  return notation in tier2
    if pct <= 0.18:  return notation in tier3
    if pct <= 0.26:  return notation in tier4
    if pct <= 0.44:  return notation in tier5
    return notation in tier6


# ═══════════════════════════════════════════════════════════════════════════
# AI PREFLOP DECISION (range-table based, position-aware)
# ═══════════════════════════════════════════════════════════════════════════

def _preflop_raise_size(to_call: int, pot: int, scenario: str) -> int:
    """
    Standard preflop raise sizes.

    Chip units: BB = 10, so 2.5bb = 25 chips.
    - RFI:          25 chips (2.5bb standard open)
    - 3-bet (defend_call / squeeze): 3x the current bet (e.g., 75 facing 25)
    - 4-bet (defend_3bet):           2x the current bet (~2.2x, rounds to 2x)
    """
    if scenario == 'rfi':
        return 25   # 2.5bb
    elif scenario in ('defend_call', 'squeeze') and to_call > 0:
        # 3-bet: 3× the open amount
        return to_call * 3
    elif scenario == 'defend_3bet' and to_call > 0:
        # 4-bet: 2× the 3-bet
        return to_call * 2
    return 25


def ai_preflop_decision(player: Player, current_bet: int, pot: int,
                        game_state: dict) -> Tuple[str, int]:
    """
    Position-aware preflop AI using the GTO range-table engine.

    Replaces the Monte Carlo hand_strength_0_1() path for preflop decisions.
    All five scenarios are handled: rfi, defend_call, defend_3bet, squeeze,
    bb_option.

    GTO mixing is applied: range_frequency is the probability of playing (so a
    hand that GTO opens 60% of the time folds the other 40%).

    game_state keys (same dict that detect_scenario() expects):
        'num_raises_this_street': int
        'num_callers': int
        'hero_has_raised': bool
        'hero_position': str
        'to_call': int / float
        'opener_position': str or None
    """
    hand = cards_to_notation(str(player.hole_cards[0]), str(player.hole_cards[1]))
    to_call = current_bet - player.bet_this_street

    # Normalize to_call for scenario detection: the initial big blind is NOT
    # a raise, so when no raises have happened yet we pass to_call=0 to
    # detect_scenario (which expects 0 when the player is first to act / RFI).
    raises = game_state.get('num_raises_this_street', 0)
    scenario_to_call = to_call if raises > 0 else 0
    scenario_state = dict(game_state)
    scenario_state['to_call'] = scenario_to_call

    scenario = detect_scenario(scenario_state)
    opener_pos = game_state.get('opener_position') or ''

    # For the decision itself, pass the actual to_call so pot odds are correct.
    decision = decide_preflop(
        hand_notation=hand,
        hero_position=player.position,
        scenario=scenario,
        opener_position=opener_pos,
        pot=float(pot),
        to_call=float(to_call) if raises > 0 else 0.0,
        rm=_RANGE_MANAGER,
    )

    # BB_OPTION: CHECK maps to ('check', 0) in game engine terms.
    if decision.action == 'CHECK':
        return ('check', 0)

    # GTO mixing: use range_frequency as probability to play the recommended action.
    # range_frequency == 0.0 means always fold (no table entry for this hand).
    r = random.random()
    if decision.action == 'FOLD':
        return ('fold', 0)
    elif decision.action == 'RAISE':
        if r < decision.range_frequency:
            raise_size = _preflop_raise_size(to_call, pot, scenario)
            # Amount is total chips committed this street (player.bet_this_street + raise_size)
            raise_total = player.bet_this_street + min(raise_size, player.stack)
            return ('raise', raise_total)
        else:
            # Mixed strategy: fold the non-raising fraction
            return ('fold', 0)
    elif decision.action == 'CALL':
        if r < decision.range_frequency:
            return ('call', current_bet)
        else:
            return ('fold', 0)

    return ('fold', 0)


# ═══════════════════════════════════════════════════════════════════════════
# AI DECISION
# ═══════════════════════════════════════════════════════════════════════════

def ai_decision(player: Player, current_bet: int, pot: int,
                board: List[Card],
                personality: Optional[PersonalityProfile] = None) -> Tuple[str, int]:
    """
    Heuristic AI with optional personality profile.

    Returns (action, amount) where action is one of:
        'fold', 'check', 'call', 'bet', 'raise'
    and amount is the total chips to put in this street.

    When personality is provided, thresholds and frequencies come from
    the profile; otherwise the original hardcoded defaults are used.
    """
    to_call = current_bet - player.bet_this_street
    can_check = to_call == 0
    strength = hand_strength_0_1(player.hole_cards, board)
    r = random.random()

    # Pull thresholds and frequencies from personality or use defaults
    if personality is not None:
        strong_th = personality.strong_threshold
        medium_th = personality.medium_threshold
        strong_bet_f = personality.strong_bet_freq
        strong_raise_f = personality.strong_raise_freq
        medium_check_f = personality.medium_check_freq
        medium_bet_f = personality.medium_bet_freq
        medium_fold_f = personality.medium_fold_to_bet
        weak_bluff_f = personality.weak_bluff_freq
        weak_fold_f = personality.weak_fold_to_bet
        weak_call_f = personality.weak_call_freq
        size_min = personality.bet_size_min
        size_max = personality.bet_size_max
    else:
        strong_th = 0.65
        medium_th = 0.45
        strong_bet_f = 0.70
        strong_raise_f = 0.30
        medium_check_f = 0.80
        medium_bet_f = 0.20
        medium_fold_f = 0.20
        weak_bluff_f = 0.10
        weak_fold_f = 0.65
        weak_call_f = 0.15
        size_min = 0.50
        size_max = 0.75

    # Random sizing within the personality's range
    size_frac = random.uniform(size_min, size_max)

    if strength > strong_th:
        # Strong hand
        if can_check:
            if r < strong_bet_f:
                bet_size = max(int(pot * size_frac), 10)
                bet_size = min(bet_size, player.stack)
                return ('bet', player.bet_this_street + bet_size)
            else:
                return ('check', 0)
        else:
            if r < strong_raise_f:
                raise_to = max(current_bet * 3, current_bet + pot // 2)
                raise_to = min(raise_to, player.stack + player.bet_this_street)
                return ('raise', raise_to)
            else:
                return ('call', current_bet)
    elif strength > medium_th:
        # Medium hand
        if can_check:
            if r < medium_check_f:
                return ('check', 0)
            else:
                bet_size = max(int(pot * size_frac), 10)
                bet_size = min(bet_size, player.stack)
                return ('bet', player.bet_this_street + bet_size)
        else:
            if r < medium_fold_f:
                return ('fold', 0)
            else:
                return ('call', current_bet)
    else:
        # Weak hand
        if can_check:
            if r < weak_bluff_f:
                bet_size = max(int(pot * size_frac), 10)
                bet_size = min(bet_size, player.stack)
                return ('bet', player.bet_this_street + bet_size)
            else:
                return ('check', 0)
        else:
            if r < weak_fold_f:
                return ('fold', 0)
            elif r < weak_fold_f + weak_call_f:
                return ('call', current_bet)
            else:
                return ('fold', 0)


# ═══════════════════════════════════════════════════════════════════════════
# COACHING PIPELINE
# ═══════════════════════════════════════════════════════════════════════════

LEVEL_NAMES = {
    1: 'Beginner',
    2: 'Intermediate',
    3: 'Advanced',
}

_PLAYER_LEVEL_MAP = None


def _get_player_level(level_int: int):
    global _PLAYER_LEVEL_MAP
    if _PLAYER_LEVEL_MAP is None:
        from coaching.levels import PlayerLevel
        _PLAYER_LEVEL_MAP = {
            1: PlayerLevel.L1_PERCEPTION,
            2: PlayerLevel.L2_CAUSE_EFFECT,
            3: PlayerLevel.L3_ARCHITECTURE,
            4: PlayerLevel.L4_MEASUREMENT,
            5: PlayerLevel.L5_SYSTEMS,
        }
    return _PLAYER_LEVEL_MAP[level_int]


_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        from coaching.explain_hand import ExplainEngine
        model_path = os.path.join(_HERE, 'gto_model_v8_38feat.json')
        sizing_path = os.path.join(_HERE, 'raise_sizing_model_v3_38feat.json')
        if not os.path.exists(sizing_path):
            sizing_path = None
        _engine = ExplainEngine(model_path, sizing_path)
    return _engine


STREET_CODE = {'flop': 'f', 'turn': 't', 'river': 'r'}


def run_coaching(hero: Player, board: List[Card],
                 pot: int, to_call: int,
                 street: str, facing_bet: bool,
                 active_opponents: List[Player],
                 level: int,
                 betting_villain_position: str = '',
                 num_raises_this_street: int = 0,
                 opener_position: str = '',
                 ) -> Optional[object]:
    """
    Run the full coaching pipeline and return an Explanation.
    Returns None if coaching is unavailable.

    betting_villain_position: position of the player who made the current bet/raise.
        When provided and facing_bet=True, this is used as the villain position (vp)
        for range analysis instead of defaulting to the highest-stack villain.
    opener_position: position of the preflop raiser (PFR). Used by feature_extractor
        to assign correct ranges (RFI for opener, DEFEND for callers).
    """
    try:
        engine = _get_engine()
        player_level = _get_player_level(level)

        villains = [p for p in active_opponents if not p.is_folded and not p.is_hero]
        if not villains:
            return None

        # Use the actual betting villain for range analysis when available;
        # otherwise fall back to the highest-stack villain.
        if facing_bet and betting_villain_position:
            vp = betting_villain_position
        else:
            villain = max(villains, key=lambda p: p.stack)
            vp = villain.position

        hero_card_str = ''.join(str(c) for c in hero.hole_cards)
        board_str = ''.join(str(c) for c in board)

        num_opponents = len([p for p in active_opponents
                             if not p.is_folded and not p.is_hero])

        hand_json = {
            'h': hero_card_str,
            'b': board_str,
            'pos': hero.position,
            'vp': vp,
            'pot': float(pot),
            'tc': float(to_call),
            'st': STREET_CODE.get(street, 'f'),
            'fb': int(facing_bet),
            'exp': 'C',
            F.META_NUM_OPPONENTS: max(1, num_opponents),
            F.META_NUM_RAISES: num_raises_this_street,
            F.META_OPENER_POSITION: opener_position or None,
            F.META_BETTOR_POSITION: betting_villain_position or None,
        }

        return engine.explain(hand_json, player_level,
                              num_opponents=max(1, num_opponents))

    except Exception as e:
        logger.warning("run_coaching failed: %s", e, exc_info=True)
        return None


def run_coaching_all_levels(hero: Player, board: List[Card],
                             pot: int, to_call: int,
                             street: str, facing_bet: bool,
                             active_opponents: List[Player],
                             betting_villain_position: str = '',
                             num_raises_this_street: int = 0,
                             opener_position: str = '',
                             ) -> List[object]:
    """Run coaching for all 3 levels and return list of Explanations."""
    results = []
    for lvl in range(1, 4):
        exp = run_coaching(hero, board, pot, to_call, street, facing_bet,
                           active_opponents, lvl,
                           betting_villain_position=betting_villain_position,
                           num_raises_this_street=num_raises_this_street,
                           opener_position=opener_position)
        results.append(exp)
    return results


# ═══════════════════════════════════════════════════════════════════════════
# DISPLAY HELPERS
# ═══════════════════════════════════════════════════════════════════════════

W = 42  # display width (inner content width)
SEP = '━' * (W + 2)  # horizontal rule for verdict box
DOUBLE = '═' * (W + 2)


def ruler(char: str = '━') -> str:
    return char * (W + 2)


def center(text: str, width: int = W + 2) -> str:
    return text.center(width)


def pad_line(text: str, width: int = W) -> str:
    """Left-padded line with 2-space indent."""
    return f"  {text}"


def _strip_ansi(s: str) -> int:
    """Return visible length of string, ignoring ANSI escape codes."""
    import re
    return len(re.sub(r'\x1b\[[0-9;]*m', '', s))


def fmt_board_display(board: List[Card], street: str) -> str:
    """Display board with blanks for undealt streets."""
    slots = [fmt_card(c) for c in board]
    if street == 'flop':
        slots += ['__', '__']
    elif street == 'turn':
        slots += ['__']
    return ' '.join(slots)


def print_situation(street: str, hand_number: int, pot: int,
                    board: List[Card], hero: Player, players: List[Player],
                    current_bet: int, villain_bet: int = 0,
                    villain_position: str = ''):
    """
    Print the situation display (cards, board, pot, position).
    NO coaching, NO equity, NO GTO recommendation.

    villain_position: position label (e.g. 'BB', 'CO') of the player who
        made the current bet/raise. Shown as "BB bets 25 into 45 (56% pot)".
        If empty and there is a villain bet, falls back to "Villain bets".
    """
    print()
    print(ruler('═'))

    street_label = street.upper() if street != 'preflop' else 'PREFLOP'
    header = f"  {street_label}  |  Hand #{hand_number}  |  Pot: {pot}"
    print(header)
    print(ruler('═'))
    print()

    # Board
    if board:
        board_str = fmt_board_display(board, street)
        print(f"  Board:  {board_str}")
    else:
        print(f"  Board:  (preflop — no community cards)")

    print()

    # Hero's cards
    hero_cards_str = fmt_cards_inline(hero.hole_cards)
    print(f"  Your cards: {hero_cards_str}")

    # Position
    if hero.position in ('BTN', 'CO', 'HJ'):
        ip_tag = "(in position)"
    elif hero.position in ('SB', 'BB', 'UTG'):
        ip_tag = "(out of position)"
    else:
        ip_tag = ""
    print(f"  Position: {hero.position} {ip_tag}".rstrip())

    # Show active opponents with position and stack
    active_villains = [p for p in players if not p.is_folded and not p.is_hero]
    if active_villains:
        villain_info = ', '.join(f"{p.position} ({p.stack})" for p in active_villains)
        print(f"  Stack: {hero.stack}  |  Opponents: {villain_info}")
    else:
        print(f"  Stack: {hero.stack}")

    print()

    # Show villain's bet if facing one, with position label
    if villain_bet > 0 and pot > 0:
        pct = int(100 * villain_bet / pot) if pot > 0 else 0
        actor = villain_position if villain_position else 'Villain'
        print(f"  {actor} bets {villain_bet} into {pot} ({pct}% pot)")
        print()

    print(ruler('═'))


def print_action_menu(options: List[Tuple[str, str]]):
    """Print the action menu line: [1] FOLD  [2] CALL 25  [3] RAISE"""
    parts = '  '.join(f"[{key}] {label}" for key, label in options)
    print(f"  {parts}")
    print(ruler('═'))


def print_verdict(gto_action: str, gto_conf: float,
                  hero_action: str, correct: bool,
                  note: str = ''):
    """
    Print the verdict block after hero acts.

    correct: True if action was correct, False if missed.
    note: extra context line (e.g. "SIZE OFF")
    """
    gto_pct = int(gto_conf * 100)
    print()
    print(ruler('━'))

    gto_line  = f"  GTO says: {gto_action} ({gto_pct}%)  |  You chose: {hero_action}"
    print(gto_line)

    if correct:
        print(f"  CORRECT")
    elif note:
        print(f"  {note}")
    else:
        print(f"  MISSED — {gto_action.split()[0]} probability: {gto_pct}%")

    print(ruler('━'))
    print(f"  [Space for coaching  |  q to quit]")


def print_coaching_box(explanation, level: int):
    """Print the coaching box with headline and supporting lines."""
    print()
    level_name = LEVEL_NAMES.get(level, f'L{level}')
    box_w = W  # inner content width
    top    = f"\u250c\u2500 COACH ({level_name}) " + "\u2500" * max(0, box_w - 10 - len(level_name)) + "\u2510"
    bottom = f"\u2514" + "\u2500" * (len(top) - 2) + "\u2518"

    def box_row(text: str) -> str:
        # wrap if needed
        visible = _strip_ansi(text)
        pad = max(0, len(top) - 4 - visible)
        return f"\u2502 {text}{' ' * pad} \u2502"

    print(top)

    if explanation is not None:
        headline = str(explanation.headline)
        # Word-wrap headline at 36 chars
        _wrap_and_print_box(headline, box_row, max_w=36)

        supporting = explanation.supporting or []
        if supporting:
            print(box_row(''))
            for line in supporting[:3]:
                _wrap_and_print_box(str(line), box_row, max_w=36)

        if hasattr(explanation, 'sizing') and explanation.sizing is not None:
            size_label = getattr(explanation.sizing, 'size_label', '') or ''
            if size_label:
                print(box_row(''))
                print(box_row(f"[Sizing: {size_label}]"))
    else:
        print(box_row("(coaching unavailable for this hand)"))

    print(bottom)
    print(f"  [Space to continue  |  q to quit]")


def _wrap_and_print_box(text: str, box_row_fn, max_w: int = 36):
    """Word-wrap text and print each chunk through box_row_fn."""
    words = text.split()
    line = ''
    for word in words:
        candidate = f"{line} {word}".strip()
        if len(candidate) <= max_w:
            line = candidate
        else:
            if line:
                print(box_row_fn(f'"{line}"' if not line.startswith('"') else line))
            line = word
    if line:
        chunk = f'"{line}"' if not line.startswith('"') else line
        print(box_row_fn(chunk))


def print_all_levels_coaching(explanations: List[object]):
    """Print coaching for all 5 levels (triggered by 'a' key)."""
    print()
    print(ruler('═'))
    print("  ALL COACHING LEVELS")
    print(ruler('═'))
    for i, exp in enumerate(explanations, 1):
        level_name = LEVEL_NAMES.get(i, f'L{i}')
        print(f"\n  -- {level_name} --")
        if exp is not None:
            print(f"  {exp.headline}")
            for line in (exp.supporting or [])[:2]:
                print(f"  {line}")
        else:
            print("  (unavailable)")
    print()
    print(ruler('═'))
    print("  [Space to continue  |  q to quit]")


# ═══════════════════════════════════════════════════════════════════════════
# SESSION STATISTICS
# ═══════════════════════════════════════════════════════════════════════════

class SessionStats:
    """Track hero decisions across the session for the summary screen."""

    def __init__(self):
        self.hands = 0
        self.decisions: List[Dict] = []   # list of decision records

    def record(self, street: str, gto_action: str, hero_action: str,
               gto_conf: float, correct: bool):
        self.decisions.append({
            'street':     street,
            'gto':        gto_action.lower(),
            'hero':       hero_action.lower(),
            'conf':       gto_conf,
            'correct':    correct,
        })

    def preflop_decisions(self):
        return [d for d in self.decisions if d['street'] == 'preflop']

    def postflop_decisions(self):
        return [d for d in self.decisions if d['street'] != 'preflop']

    def _leak_counts(self, subset: List[Dict]) -> Dict[str, int]:
        leaks: Dict[str, int] = {}
        for d in subset:
            if not d['correct']:
                key = f"You {d['hero'].upper()} (GTO: {d['gto'].upper()})"
                leaks[key] = leaks.get(key, 0) + 1
        return leaks

    def print_summary(self):
        total = len(self.decisions)
        correct = sum(1 for d in self.decisions if d['correct'])
        pf = self.preflop_decisions()
        pf_correct = sum(1 for d in pf if d['correct'])
        po = self.postflop_decisions()
        po_correct = sum(1 for d in po if d['correct'])

        print()
        print(ruler('═'))
        print(center("SESSION SUMMARY"))
        print(ruler('═'))
        print()

        pct = int(100 * correct / total) if total else 0
        print(f"  Hands: {self.hands}  |  Decisions: {total}")
        print(f"  Correct: {correct}/{total} ({pct}%)")
        print()

        if pf:
            pf_pct = int(100 * pf_correct / len(pf))
            print(f"  Preflop:  {pf_correct}/{len(pf)} ({pf_pct}%)")
        if po:
            po_pct = int(100 * po_correct / len(po))
            print(f"  Postflop: {po_correct}/{len(po)} ({po_pct}%)")

        # Top leaks
        leaks = self._leak_counts(self.decisions)
        if leaks:
            print()
            print("  Common leaks:")
            for desc, count in sorted(leaks.items(), key=lambda x: -x[1])[:3]:
                print(f"    {desc}: {count}x")

        # Encouragement
        print()
        if total == 0:
            print("  No decisions recorded yet.")
        elif pct >= 80:
            print("  Strong session — keep it up!")
        elif pct >= 60:
            print("  Good work. Review the leaks above.")
        else:
            print("  Keep working on decision-making consistency.")

        print()
        print(ruler('═'))


# ═══════════════════════════════════════════════════════════════════════════
# GAME STATE
# ═══════════════════════════════════════════════════════════════════════════

class PokerGame:
    SMALL_BLIND = 5
    BIG_BLIND = 10

    def __init__(self, coaching_level: int = 2, starting_stack: int = 1000,
                 hero_callback=None, ai_callback=None):
        self.coaching_level = coaching_level
        self.starting_stack = starting_stack
        self.hero_callback = hero_callback
        self.ai_callback = ai_callback
        self.stats = SessionStats()

        # Build 6 players; hero is BTN
        names = ['Alex', 'Blake', 'Casey', 'Hero', 'Dana', 'Ellis']
        self.players: List[Player] = []
        for i, pos in enumerate(POSITIONS):
            name = names[i]
            is_hero = (pos == 'BTN')
            p = Player(name, pos, starting_stack, is_hero)
            p.personality = None
            self.players.append(p)

        self.hero: Player = next(p for p in self.players if p.is_hero)

        self.deck: List[Card] = []
        self.community_cards: List[Card] = []
        self.pot = 0
        self.current_bet = 0
        self.street = 'preflop'
        self.hand_number = 0
        self.last_winners = []
        self.last_pot = 0
        # Preflop action tracking — reset each hand in deal_hand()
        self.opener_position: str = ''          # Position of the first raiser
        self.callers_this_street: int = 0       # Number of callers to the open
        self.hero_has_raised_preflop: bool = False  # True once hero raises

    def _player_at(self, position: str) -> Player:
        for p in self.players:
            if p.position == position:
                return p
        raise ValueError(f"No player at {position}")

    def active_players(self) -> List[Player]:
        return [p for p in self.players if not p.is_folded and p.stack > 0 or
                (not p.is_folded and p.is_all_in)]

    def players_to_act(self) -> List[Player]:
        return [p for p in self.players if not p.is_folded and not p.is_all_in]

    def rotate_positions(self):
        pos_cycle = POSITIONS[:]
        current = [p.position for p in self.players]
        new_positions = [pos_cycle[(pos_cycle.index(pos) + 1) % 6]
                         for pos in current]
        for p, pos in zip(self.players, new_positions):
            p.position = pos
        self.hero = next(p for p in self.players if p.is_hero)

    # ─── Setup ──────────────────────────────────────────────────────────

    def deal_hand(self):
        self.hand_number += 1
        self.stats.hands += 1
        self.deck = make_deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.street = 'preflop'
        self.opener_position = ''
        self.callers_this_street = 0
        self.hero_has_raised_preflop = False
        self.raises_this_street = 0

        for p in self.players:
            p.reset_for_hand()
            if p.stack <= 0:
                p.stack = self.starting_stack

        sb = self._player_at('SB')
        bb = self._player_at('BB')
        sb_posted = sb.put_in(min(self.SMALL_BLIND, sb.stack))
        bb_posted = bb.put_in(min(self.BIG_BLIND, bb.stack))
        self.pot += sb_posted + bb_posted
        self.current_bet = self.BIG_BLIND

        deal_order = ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']
        for _ in range(2):
            for pos in deal_order:
                p = self._player_at(pos)
                p.hole_cards.append(self.deck.pop())

    # ─── Betting round ───────────────────────────────────────────────────

    def run_betting_round(self) -> bool:
        """
        Run a complete betting round. Returns True if hand should continue.
        Returns False if only one player remains.
        """
        # Reset raise counter for this street
        self.raises_this_street = 0
        # Reset preflop tracking on each new street (postflop streets clear it too,
        # but it only matters preflop — no harm clearing it here).
        if self.street != 'preflop':
            self.opener_position = ''
            self.callers_this_street = 0

        if self.street == 'preflop':
            order = ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']
        else:
            order = ['SB', 'BB', 'UTG', 'HJ', 'CO', 'BTN']

        players_in_order = [self._player_at(pos) for pos in order]

        n = len(players_in_order)
        acted_this_round: set = set()
        idx = 0
        passes = 0

        while passes < n * 3:
            passes += 1
            p = players_in_order[idx % n]

            if p.is_folded or p.is_all_in:
                idx += 1
                continue

            to_call = self.current_bet - p.bet_this_street

            if p.name in acted_this_round and to_call == 0:
                idx += 1
                can_act = [q for q in players_in_order
                           if not q.is_folded and not q.is_all_in]
                if all(q.name in acted_this_round and
                       q.bet_this_street == self.current_bet
                       for q in can_act):
                    break
                continue

            bet_before = self.current_bet

            if p.is_hero:
                self._hero_turn(p)
            else:
                self._ai_turn(p)

            if not p.is_folded:
                acted_this_round.add(p.name)

            if self.current_bet > bet_before:
                acted_this_round = {p.name}

            survivors = [q for q in self.players if not q.is_folded]
            if len(survivors) < 2:
                break

            idx += 1

            can_act = [q for q in players_in_order
                       if not q.is_folded and not q.is_all_in]
            if can_act and all(q.name in acted_this_round and
                               q.bet_this_street == self.current_bet
                               for q in can_act):
                break

        survivors = [p for p in self.players if not p.is_folded]
        return len(survivors) >= 2

    def _apply_action(self, player: Player, action: str, amount: int):
        """Apply a resolved action. Also updates preflop opener/caller tracking."""
        if action == 'fold':
            player.is_folded = True
        elif action == 'check':
            pass
        elif action == 'call':
            to_call = min(self.current_bet - player.bet_this_street, player.stack)
            added = player.put_in(to_call)
            self.pot += added
            # Count callers to the open for squeeze detection (preflop only)
            if self.street == 'preflop' and self.opener_position and added > 0:
                self.callers_this_street += 1
        elif action == 'bet':
            # If current_bet > 0, a 'bet' over it functions as a raise
            if self.current_bet > 0:
                self.raises_this_street = getattr(self, 'raises_this_street', 0) + 1
            chips_to_add = amount - player.bet_this_street
            chips_to_add = min(chips_to_add, player.stack)
            if chips_to_add > 0:
                added = player.put_in(chips_to_add)
                self.pot += added
                self.current_bet = player.bet_this_street
            # Track first preflop raiser as opener
            if self.street == 'preflop' and not self.opener_position:
                self.opener_position = player.position
            if self.street == 'preflop' and player.is_hero:
                self.hero_has_raised_preflop = True
        elif action == 'raise':
            self.raises_this_street = getattr(self, 'raises_this_street', 0) + 1
            chips_to_add = amount - player.bet_this_street
            chips_to_add = min(chips_to_add, player.stack)
            if chips_to_add > 0:
                added = player.put_in(chips_to_add)
                self.pot += added
                self.current_bet = player.bet_this_street
            # Track first preflop raiser as opener
            if self.street == 'preflop' and not self.opener_position:
                self.opener_position = player.position
            if self.street == 'preflop' and player.is_hero:
                self.hero_has_raised_preflop = True

    def _ai_turn(self, player: Player):
        if self.street == 'preflop':
            # Position-aware range-table decision preflop
            preflop_state = {
                'num_raises_this_street': getattr(self, 'raises_this_street', 0),
                'num_callers': self.callers_this_street,
                'hero_has_raised': False,  # This is an AI player, not hero
                'hero_position': player.position,
                'to_call': self.current_bet - player.bet_this_street,
                'opener_position': self.opener_position or None,
            }
            action, amount = ai_preflop_decision(
                player, self.current_bet, self.pot, preflop_state
            )
        else:
            action, amount = ai_decision(player, self.current_bet,
                                         self.pot, self.community_cards,
                                         getattr(player, 'personality', None))
        self._apply_action(player, action, amount)
        if self.ai_callback is not None:
            self.ai_callback(self, player, action, amount)

    # ─── Hero's turn ─────────────────────────────────────────────────────

    def _hero_turn(self, hero: Player):
        """New UX flow: show situation → menu → player acts → verdict → coaching."""
        to_call = self.current_bet - hero.bet_this_street
        facing_bet = to_call > 0

        # Figure out who last put chips in (for villain bet display)
        villain_bet = to_call if facing_bet else 0

        # Find the position of the last aggressor (the player whose
        # bet_this_street equals current_bet and is not the hero).
        villain_position = ''
        if facing_bet and self.current_bet > 0:
            aggressors = [
                p for p in self.players
                if not p.is_folded and not p.is_hero
                and p.bet_this_street == self.current_bet
            ]
            if aggressors:
                villain_position = aggressors[0].position

        # If a hero_callback is set, delegate the decision to it instead of
        # using the interactive getch()-based flow.
        if self.hero_callback is not None:
            context = {
                'to_call': to_call,
                'facing_bet': facing_bet,
                'pot': self.pot,
                'street': self.street,
                'board': list(self.community_cards),
                'current_bet': self.current_bet,
                'active_opponents': [p for p in self.players if not p.is_folded and not p.is_hero],
                'hero': hero,
                'is_preflop': self.street == 'preflop',
                'villain_position': villain_position,
                'villain_bet': villain_bet,
                'hand_number': self.hand_number,
                'num_raises_this_street': getattr(self, 'raises_this_street', 0),
                # Preflop scenario context (used by preflop_engine)
                'opener_position': self.opener_position or None,
                'num_callers': self.callers_this_street,
                'hero_has_raised': self.hero_has_raised_preflop,
            }
            action, amount = self.hero_callback(self, hero, context)
            self._apply_action(hero, action, amount)
            return

        if self.street == 'preflop':
            self._hero_preflop(hero, to_call, facing_bet, villain_bet,
                               villain_position)
        else:
            self._hero_postflop(hero, to_call, facing_bet, villain_bet,
                                villain_position)

    # ─── Preflop hero decision ────────────────────────────────────────────

    def _hero_preflop(self, hero: Player, to_call: int, facing_bet: bool,
                      villain_bet: int, villain_position: str = ''):
        """Preflop decision with range gate."""
        # Determine scenario
        in_range = hand_in_opening_range(hero.hole_cards[0], hero.hole_cards[1],
                                         hero.position)

        # Show situation
        print_situation(
            self.street, self.hand_number, self.pot,
            self.community_cards, hero, self.players,
            self.current_bet, villain_bet,
            villain_position=villain_position,
        )

        # Build menu — always show all options, feedback comes after
        if facing_bet:
            options = [('1', 'FOLD'), ('2', f'CALL {to_call}'), ('3', '3-BET')]
            valid_keys = {'1': 'fold', '2': 'call', '3': 'raise'}
        elif hero.position == 'BB' and to_call == 0:
            options = [('1', 'CHECK'), ('2', 'RAISE')]
            valid_keys = {'1': 'check', '2': 'raise'}
        else:
            options = [('1', 'OPEN (2.5x)'), ('2', 'FOLD')]
            valid_keys = {'1': 'bet', '2': 'fold'}

        print_action_menu(options)

        # Get hero keypress
        action_key, action, amount = self._get_preflop_action(
            hero, valid_keys, to_call, facing_bet
        )

        # Run coaching now (after decision)
        active = [p for p in self.players if not p.is_folded]
        explanation = None
        # Preflop coaching is limited — only attempt if we have a board situation
        # For preflop, use simplified verdict logic
        gto_action = None
        gto_conf = 0.0

        # Simplified preflop GTO verdict
        if facing_bet:
            # Very rough: calling or 3-betting premium hands
            gto_action, gto_conf = self._preflop_gto_estimate(
                hero, to_call, facing_bet, in_range)
        elif hero.position == 'BB' and to_call == 0:
            gto_action = 'CHECK'
            gto_conf = 0.75
        else:
            if in_range:
                gto_action = 'OPEN'
                gto_conf = 0.90
            else:
                gto_action = 'FOLD'
                gto_conf = 0.92

        hero_label = self._action_to_label(action, to_call)
        gto_label  = gto_action or hero_label

        # Determine correctness (preflop: action vs gto_action mapping)
        correct = self._preflop_correct(action, gto_action or '', in_range,
                                        facing_bet)

        # Record stat
        self.stats.record(self.street, gto_label, hero_label, gto_conf, correct)

        # Show verdict
        print_verdict(gto_label, gto_conf, hero_label, correct)

        # Wait for Space/q
        ch = wait_for_space_or_q()
        if ch == 'q':
            self._quit()

        # Show coaching (preflop is range-based, not ML pipeline)
        self._show_preflop_coaching(hero, action, in_range, facing_bet)

        # Wait for Space to continue
        ch = wait_for_space_or_q()
        if ch == 'q':
            self._quit()

        self._apply_action(hero, action, amount)

    def _preflop_gto_estimate(self, hero: Player, to_call: int,
                               facing_bet: bool, in_range: bool
                               ) -> Tuple[str, float]:
        """Simple preflop GTO estimate when facing a raise."""
        # Use hand strength as proxy
        strength = hand_strength_0_1(hero.hole_cards, [])
        if strength > 0.75:
            return ('3-BET', 0.80)
        elif strength > 0.55:
            return ('CALL', 0.72)
        else:
            return ('FOLD', 0.68)

    def _preflop_correct(self, action: str, gto_action: str,
                          in_range: bool, facing_bet: bool) -> bool:
        """Check if preflop action matches GTO recommendation."""
        a = action.lower()
        g = gto_action.lower()
        # Map to canonical actions
        action_map = {
            'open': 'bet', 'bet': 'bet',
            '3-bet': 'raise', 'raise': 'raise',
            'call': 'call', 'fold': 'fold', 'check': 'check',
        }
        a_norm = action_map.get(a, a)
        g_norm = action_map.get(g, g)
        # Allow bet≈raise and check≈call as near-correct
        close = {('bet', 'raise'), ('raise', 'bet'), ('check', 'call'), ('call', 'check')}
        return a_norm == g_norm or (a_norm, g_norm) in close

    def _show_preflop_coaching(self, hero: Player, action: str,
                                in_range: bool, facing_bet: bool):
        """Show a preflop coaching box (range-based, no ML pipeline)."""
        print()
        box_w = W
        top    = f"\u250c\u2500 PREFLOP COACH " + "\u2500" * max(0, box_w - 13) + "\u2510"
        bottom = f"\u2514" + "\u2500" * (len(top) - 2) + "\u2518"

        def row(text: str) -> str:
            pad = max(0, len(top) - 4 - len(text))
            return f"\u2502 {text}{' ' * pad} \u2502"

        print(top)

        if facing_bet:
            print(row('Facing a raise -- consider your hand'))
            print(row('strength and position.'))
        elif not in_range:
            print(row('This hand is outside your opening'))
            print(row('range from this position.'))
            print(row(''))
            print(row(f'From {hero.position}, focus on hands'))
            print(row('in the GTO opening range.'))
        else:
            print(row('Opening from this position builds the'))
            print(row('pot with a range advantage.'))

        print(bottom)
        print(f"  [Space to continue  |  q to quit]")

    def _get_preflop_action(self, hero: Player, valid_keys: Dict[str, str],
                             to_call: int, facing_bet: bool
                             ) -> Tuple[str, str, int]:
        """Get a single keypress action for preflop. Returns (key, action, amount)."""
        while True:
            ch = getch()
            if ch == 'q':
                self._quit()
            if ch == 'L':
                self._change_level_silent()
                return (ch, list(valid_keys.values())[0], 0)  # re-use first option

            if ch in valid_keys:
                action = valid_keys[ch]
                amount = self._resolve_preflop_amount(action, hero, to_call, facing_bet)
                return (ch, action, amount)

    def _resolve_preflop_amount(self, action: str, hero: Player,
                                 to_call: int, facing_bet: bool) -> int:
        """Calculate the chip amount for a preflop action."""
        if action == 'fold':
            return 0
        elif action == 'check':
            return 0
        elif action == 'call':
            return self.current_bet
        elif action == 'bet':
            # Open: 2.5x big blind
            open_size = int(self.BIG_BLIND * 2.5)
            return hero.bet_this_street + min(open_size, hero.stack)
        elif action == 'raise':
            if facing_bet:
                # 3-bet: 3x the current bet
                three_bet = self.current_bet * 3
                return min(three_bet, hero.stack + hero.bet_this_street)
            else:
                # BB raise: 3x big blind
                return min(self.BIG_BLIND * 3, hero.stack + hero.bet_this_street)
        return 0

    # ─── Postflop hero decision ───────────────────────────────────────────

    def _hero_postflop(self, hero: Player, to_call: int, facing_bet: bool,
                        villain_bet: int, villain_position: str = ''):
        """Postflop decision with full coaching pipeline."""
        can_check = to_call == 0
        active = [p for p in self.players if not p.is_folded]

        # Run coaching pipeline BEFORE showing the menu (but hidden until after action)
        explanation = run_coaching(
            hero=hero,
            board=self.community_cards,
            pot=self.pot,
            to_call=to_call,
            street=self.street,
            facing_bet=facing_bet,
            active_opponents=active,
            level=self.coaching_level,
            betting_villain_position=villain_position,
            num_raises_this_street=getattr(self, 'raises_this_street', 0),
            opener_position=self.opener_position,
        )

        # Show situation (no coaching visible here)
        print_situation(
            self.street, self.hand_number, self.pot,
            self.community_cards, hero, self.players,
            self.current_bet, villain_bet,
            villain_position=villain_position,
        )

        # Build menu
        if can_check:
            options = [('1', 'CHECK'), ('2', 'BET')]
            valid_keys = {'1': 'check', '2': 'bet'}
        else:
            options = [('1', 'FOLD'), ('2', f'CALL {to_call}'), ('3', 'RAISE')]
            valid_keys = {'1': 'fold', '2': 'call', '3': 'raise'}

        print_action_menu(options)

        # Get action (single keypress, with sizing submenu if BET/RAISE)
        action, amount, size_label = self._get_postflop_action(
            hero, valid_keys, to_call, can_check
        )

        # Determine verdict
        gto_action  = ''
        gto_conf    = 0.0
        gto_sizing  = ''
        correct     = False
        size_note   = ''

        if explanation is not None:
            gto_action = str(explanation.action).upper()
            gto_conf   = float(explanation.confidence)

            # Sizing from oracle
            if hasattr(explanation, 'sizing') and explanation.sizing is not None:
                gto_sizing = getattr(explanation.sizing, 'size_label', '') or ''

            # Compare action
            correct = self._postflop_correct(action, gto_action)

            # Compare sizing if action was BET or RAISE
            if correct and action in ('bet', 'raise') and gto_sizing and size_label:
                if size_label.lower() != gto_sizing.lower():
                    size_note = f"ACTION CORRECT, SIZE OFF — GTO prefers {gto_sizing}"
                    # Still counts as correct action
        else:
            gto_action = 'N/A'
            gto_conf   = 0.0
            correct    = True  # no coaching → don't penalise

        hero_label = self._action_to_label(action, to_call, size_label)
        gto_label  = gto_action
        if gto_sizing and gto_action in ('BET', 'RAISE'):
            gto_label = f"{gto_action} {gto_sizing}"

        # Record
        self.stats.record(self.street, gto_label, hero_label, gto_conf, correct)

        # Verdict display
        print_verdict(gto_label, gto_conf, hero_label, correct, size_note)

        # Wait for Space (coaching) or 'a' (all levels)
        ch = self._wait_for_coaching_key()
        if ch == 'q':
            self._quit()
        elif ch == 'a':
            # Show all 5 levels
            all_exp = run_coaching_all_levels(
                hero, self.community_cards, self.pot, to_call,
                self.street, facing_bet, active,
                betting_villain_position=villain_position,
                opener_position=self.opener_position,
            )
            print_all_levels_coaching(all_exp)
            ch2 = wait_for_space_or_q()
            if ch2 == 'q':
                self._quit()
        else:
            # Show coaching at current level
            print_coaching_box(explanation, self.coaching_level)
            ch2 = wait_for_space_or_q()
            if ch2 == 'q':
                self._quit()

        self._apply_action(hero, action, amount)

    def _postflop_correct(self, action: str, gto_action: str) -> bool:
        """Check if postflop action matches GTO recommendation."""
        a = action.lower()
        g = gto_action.lower()
        close = {('bet', 'raise'), ('raise', 'bet'), ('check', 'call'), ('call', 'check')}
        return a == g or (a, g) in close

    def _get_postflop_action(self, hero: Player, valid_keys: Dict[str, str],
                              to_call: int, can_check: bool
                              ) -> Tuple[str, int, str]:
        """
        Get postflop action via single keypress.
        Returns (action, amount, size_label).
        """
        while True:
            ch = getch()
            if ch == 'q':
                self._quit()
            if ch == 'L':
                self._change_level_silent()
                continue

            if ch not in valid_keys:
                continue

            action = valid_keys[ch]

            if action == 'fold':
                return ('fold', 0, '')

            elif action == 'check':
                return ('check', 0, '')

            elif action == 'call':
                return ('call', self.current_bet, '')

            elif action == 'bet':
                # Show sizing submenu
                size, label = self._sizing_submenu_bet(hero)
                amount = hero.bet_this_street + min(size, hero.stack)
                return ('bet', amount, label)

            elif action == 'raise':
                # Show sizing submenu
                size, label = self._sizing_submenu_raise(hero, to_call)
                # size is the raise-to amount
                return ('raise', min(size, hero.stack + hero.bet_this_street), label)

        return ('check', 0, '')  # unreachable

    def _sizing_submenu_bet(self, hero: Player) -> Tuple[int, str]:
        """
        Show bet sizing submenu and return (amount_to_add, label).
        amount_to_add is the chips to add on top of current bet.
        """
        pot = self.pot
        print()
        print(f"  Size your bet:  [1] Small (33%)  [2] Standard (66%)  [3] Large (100%)")

        sizes = {
            '1': (max(int(pot * 0.33), self.BIG_BLIND), 'SMALL (33%)'),
            '2': (max(int(pot * 0.66), self.BIG_BLIND), 'STANDARD (66%)'),
            '3': (max(pot,             self.BIG_BLIND), 'LARGE (100%)'),
        }

        while True:
            ch = getch()
            if ch == 'q':
                self._quit()
            if ch in sizes:
                return sizes[ch]

    def _sizing_submenu_raise(self, hero: Player, to_call: int) -> Tuple[int, str]:
        """
        Show raise sizing submenu and return (raise_to_total, label).
        """
        base = self.current_bet
        print()
        print(f"  Size your raise:  [1] Small (2.2x)  [2] Standard (2.5x)  [3] Large (3x+)")

        raise_to = {
            '1': (max(int(base * 2.2), base + self.BIG_BLIND), 'SMALL (2.2x)'),
            '2': (max(int(base * 2.5), base + self.BIG_BLIND), 'STANDARD (2.5x)'),
            '3': (max(base * 3,        base + self.BIG_BLIND), 'LARGE (3x+)'),
        }

        while True:
            ch = getch()
            if ch == 'q':
                self._quit()
            if ch in raise_to:
                return raise_to[ch]

    def _action_to_label(self, action: str, to_call: int, size_label: str = '') -> str:
        """Convert internal action to a display label."""
        labels = {
            'fold':  'FOLD',
            'check': 'CHECK',
            'call':  f'CALL {to_call}' if to_call else 'CALL',
            'bet':   f'BET {size_label}' if size_label else 'BET',
            'raise': f'RAISE {size_label}' if size_label else 'RAISE',
        }
        return labels.get(action, action.upper())

    def _wait_for_coaching_key(self) -> str:
        """Wait for Space, 'a', or 'q'."""
        while True:
            ch = getch()
            if ch in (' ', 'q', 'a', '\r', '\n'):
                return ch

    def _change_level_silent(self):
        """Change coaching level with a small inline prompt."""
        print()
        print("  Change level (1-3): ", end='', flush=True)
        ch = getch()
        if ch in ('1', '2', '3'):
            self.coaching_level = int(ch)
            print(ch)
            print(f"  Level set to: {LEVEL_NAMES[self.coaching_level]}")
        else:
            print()

    def _quit(self):
        self.stats.print_summary()
        print("\n  Thanks for playing River Rats Poker!")
        sys.exit(0)

    # ─── Streets ─────────────────────────────────────────────────────────

    def deal_flop(self):
        self.deck.pop()
        for _ in range(3):
            self.community_cards.append(self.deck.pop())
        self.street = 'flop'
        self._reset_street()
        if self.hero_callback is None:
            flop_str = fmt_cards_inline(self.community_cards)
            print(f"\n  --- FLOP: {flop_str} ---")

    def deal_turn(self):
        self.deck.pop()
        self.community_cards.append(self.deck.pop())
        self.street = 'turn'
        self._reset_street()
        if self.hero_callback is None:
            board_str = fmt_cards_inline(self.community_cards)
            print(f"\n  --- TURN: {board_str} ---")

    def deal_river(self):
        self.deck.pop()
        self.community_cards.append(self.deck.pop())
        self.street = 'river'
        self._reset_street()
        if self.hero_callback is None:
            board_str = fmt_cards_inline(self.community_cards)
            print(f"\n  --- RIVER: {board_str} ---")

    def _reset_street(self):
        self.current_bet = 0
        for p in self.players:
            p.reset_for_street()

    # ─── Showdown ────────────────────────────────────────────────────────

    def showdown(self):
        contenders = [p for p in self.players if not p.is_folded]
        _print = print if self.hero_callback is None else (lambda *a, **k: None)

        if len(contenders) == 1:
            winner = contenders[0]
            self.last_winners = [{'name': winner.name, 'amount': self.pot, 'reason': 'everyone else folded'}]
            self.last_pot = self.pot
            winner.stack += self.pot
            you_tag = " (you!)" if winner.is_hero else ""
            _print(f"\n  {winner.name} wins {self.pot} chips{you_tag} "
                   f"(everyone else folded)")
            self.pot = 0
            return

        if not EVAL7_AVAILABLE:
            share = self.pot // len(contenders)
            self.last_winners = [{'name': p.name, 'amount': share, 'reason': 'split (no eval)'} for p in contenders]
            self.last_pot = self.pot
            for p in contenders:
                p.stack += share
            _print(f"\n  Pot split equally (eval7 not available).")
            self.pot = 0
            return

        board_e7 = [_eval7.Card(str(c)) for c in self.community_cards]
        scores = {}
        for p in contenders:
            hole_e7 = [_eval7.Card(str(c)) for c in p.hole_cards]
            score = _eval7.evaluate(hole_e7 + board_e7)
            scores[p.name] = score

        best_score = max(scores.values())  # higher eval7 score = better hand
        winners = [p for p in contenders if scores[p.name] == best_score]

        share = self.pot // len(winners)
        remainder = self.pot - share * len(winners)

        _print(f"\n  --- SHOWDOWN ---")
        for p in contenders:
            you_tag = " (you)" if p.is_hero else ""
            desc = describe_hand(p.hole_cards, self.community_cards)
            _print(f"  {p.position} {p.name}: {fmt_cards_inline(p.hole_cards)}"
                   f"  {desc}{you_tag}")

        self.last_winners = []
        self.last_pot = self.pot
        for w in winners:
            award = share + (remainder if w == winners[0] else 0)
            w.stack += award
            you_tag = " (you!)" if w.is_hero else ""
            desc = describe_hand(w.hole_cards, self.community_cards)
            self.last_winners.append({'name': w.name, 'amount': award, 'reason': desc})
            _print(f"\n  {w.name} wins {award} chips{you_tag}  ({desc})")

        self.pot = 0

    # ─── Play one hand ───────────────────────────────────────────────────

    def play_hand(self) -> bool:
        self.deal_hand()

        hero = self.hero
        if self.hero_callback is None:
            print(f"\n  Hand #{self.hand_number}  |  "
                  f"Your cards: {fmt_cards_inline(hero.hole_cards)}  "
                  f"  Stack: {hero.stack}")
            print(f"  Your position: {hero.position}  "
                  f"|  Pot after blinds: {self.pot}")

        # Preflop
        if not self.run_betting_round():
            self.showdown()
            return True

        survivors = [p for p in self.players if not p.is_folded]
        if len(survivors) < 2:
            self.showdown()
            return True

        # If hero folded, skip remaining streets but still award the pot
        if hero.is_folded:
            self.showdown()
            return True

        # Flop
        self.deal_flop()
        if not self.run_betting_round():
            self.showdown()
            return True

        survivors = [p for p in self.players if not p.is_folded]
        if len(survivors) < 2 or hero.is_folded:
            self.showdown()
            return True

        # Turn
        self.deal_turn()
        if not self.run_betting_round():
            self.showdown()
            return True

        survivors = [p for p in self.players if not p.is_folded]
        if len(survivors) < 2 or hero.is_folded:
            self.showdown()
            return True

        # River
        self.deal_river()
        if not self.run_betting_round():
            self.showdown()
            return True

        self.showdown()
        return True


# ═══════════════════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════

def print_welcome():
    print()
    print(ruler('═'))
    print(center("RIVER RATS POKER"))
    print(center("6-player Texas Hold'em  |  GTO Coaching"))
    print(ruler('═'))
    print()


def choose_level_keypress() -> int:
    """Show level menu and get a single keypress choice."""
    print("  Coaching levels:")
    for k, v in LEVEL_NAMES.items():
        print(f"    [{k}] {v}")
    print()
    print("  Press 1–3 to choose (default: 2): ", end='', flush=True)

    ch = getch()
    print(ch)
    try:
        lvl = int(ch)
        if 1 <= lvl <= 3:
            return lvl
    except ValueError:
        pass
    return 2


def main():
    print_welcome()

    try:
        level = choose_level_keypress()
    except (EOFError, Exception):
        level = 2

    print(f"\n  Level: {LEVEL_NAMES[level]}")
    print(f"  Stack: 1000 chips each  |  Blinds: {PokerGame.SMALL_BLIND}/{PokerGame.BIG_BLIND}")
    print(f"  You are seated at BTN")
    print()
    print(f"  Controls:")
    print(f"    1/2/3  — select action (single key, no Enter)")
    print(f"    Space  — advance (see coaching / next decision)")
    print(f"    a      — after verdict, show all 3 coaching levels")
    print(f"    L      — change coaching level (between hands)")
    print(f"    q      — quit to session summary")
    print()
    print(f"  [Press any key to deal first hand]")

    getch()

    game = PokerGame(coaching_level=level)

    while True:
        try:
            game.play_hand()
        except SystemExit:
            raise
        except KeyboardInterrupt:
            game.stats.print_summary()
            print("\n  Goodbye!")
            break
        except Exception as e:
            print(f"\n  [Error during hand: {e}]")
            import traceback
            traceback.print_exc()

        # Rebuy busted players silently
        for p in game.players:
            if p.stack <= 0:
                p.stack = game.starting_stack

        print()
        print(ruler('─'))
        print(f"  Hand #{game.hand_number} complete  |  Your stack: {game.hero.stack}")
        print(ruler('─'))
        print()
        print(f"  [Space = next hand  |  L = change level  |  q = quit]")

        while True:
            ch = getch()
            if ch == 'q':
                game.stats.print_summary()
                print("  Thanks for playing River Rats Poker!")
                return
            elif ch == 'L':
                game._change_level_silent()
                print(f"  [Space = next hand  |  q = quit]")
            elif ch in (' ', '\r', '\n', '1', '2', '3'):
                break

        game.rotate_positions()


if __name__ == '__main__':
    main()
