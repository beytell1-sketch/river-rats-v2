"""Self-play loop runner for the oracle tournament.

Runs duplicate deals across multiple oracle variants. Each deal is
played on parallel tables where the ONLY variable is the hero's
oracle configuration. Opponents use the same heuristic AI.

Hero cycles through all 6 positions per deal, producing
N_deals × 6_positions × N_variants games per round.

Usage:
    from self_play import SelfPlayRunner, Variant

    variants = [
        Variant("baseline", get_default_params()),
        Variant("tight", {**get_default_params(), 'value_base': 0.50}),
    ]
    runner = SelfPlayRunner(variants, num_deals=100, seed=42)
    results = runner.run_round()
"""
from __future__ import annotations
import json
import os
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable

from deal_generator import DealGenerator, Deal
from poker_game import PokerGame, Card, ai_preflop_decision
from game_state_bridge import build_features_from_game_state
from gto_model import GtoOracle, FEATURE_COLUMNS
from oracle_router import OracleRouter
from multiway_adjuster import adjust, get_default_params, AdjustedPrediction
from hand_logger import HandLogger


POSITIONS = ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']


@dataclass
class Variant:
    """An oracle variant with specific adjuster parameters."""
    name: str
    params: dict  # keys match multiway_adjuster param names
    rationale: str = ""

    @staticmethod
    def from_hypothesis(hyp: dict) -> 'Variant':
        """Create from a hypothesis dict (name + rationale + overrides)."""
        base = get_default_params()
        base.update(hyp.get('overrides', {}))
        return Variant(
            name=hyp['name'],
            params=base,
            rationale=hyp.get('rationale', ''),
        )


@dataclass
class HeroDecision:
    """One decision made by the hero oracle during a game."""
    street: str
    action: str
    amount: int
    pot: int
    to_call: int
    num_opponents: int
    equity: float          # raw_equity from features (0 for preflop)
    was_adjusted: bool     # True if adjuster changed the oracle's action
    oracle_action: str     # what the oracle predicted before adjustment
    is_preflop: bool
    feat_dict: Optional[Dict] = None   # full 45-feature dict (for training export)
    hero_cards: str = ''               # e.g. "KsJh"
    board: str = ''                    # e.g. "Kd8c3s"
    villain_positions: List[str] = field(default_factory=list)
    facing_bet: bool = False
    player_position: str = ''             # seat of the deciding player


@dataclass
class GameResult:
    """Result of one game (one deal × one variant × one hero position)."""
    deal_id: int
    variant_name: str
    hero_position: str
    chips_won: int  # hero's stack_after - stack_before
    hand_record: dict  # from HandLogger
    hero_decisions: List[HeroDecision] = field(default_factory=list)
    opponent_decisions: Dict[str, List[HeroDecision]] = field(default_factory=dict)


@dataclass
class RoundResult:
    """Aggregate results from one round of the self-play loop."""
    round_id: int
    num_deals: int
    num_games: int  # deals × positions × variants
    seed: int
    variant_results: Dict[str, VariantScore]
    game_results: List[GameResult]


@dataclass
class VariantScore:
    """Aggregate score for one variant across all games in a round."""
    name: str
    total_chips: int = 0
    num_games: int = 0
    games_by_position: Dict[str, List[int]] = field(default_factory=dict)

    @property
    def mbb_per_hand(self) -> float:
        """Milli-big-blinds per hand (standard poker metric)."""
        if self.num_games == 0:
            return 0.0
        # Big blind = 10 chips in our game
        return (self.total_chips / self.num_games) / 10.0 * 1000.0


def _make_oracle_callback(oracle, params: dict,
                          decision_log: Optional[List[HeroDecision]] = None) -> Callable:
    """Build a decision_callback that uses the oracle + adjuster with given params.

    Args:
        oracle: GtoOracle (single model) or OracleRouter (specialist chain).
        params: Adjuster parameter dict for this variant.
        decision_log: Optional list to append HeroDecision records to.
                      Pass None for opponent seats that don't need logging.

    Decisions are appended to decision_log (if provided) for the comparator.
    """
    use_router = isinstance(oracle, OracleRouter)

    def callback(game, player, context):
        # Preflop: use range-table engine (oracle is postflop-only)
        if context.get('street') == 'preflop':
            preflop_state = {
                'num_raises_this_street': context.get('num_raises_this_street', 0),
                'num_callers': context.get('num_callers', 0),
                'hero_has_raised': False,
                'hero_position': player.position,
                'to_call': context['to_call'],
                'opener_position': context.get('opener_position'),
            }
            action, amount = ai_preflop_decision(
                player, context['current_bet'], context['pot'], preflop_state
            )
            num_opp = len([p for p in context.get('active_opponents', [])
                          if not p.is_folded])
            if decision_log is not None:
                decision_log.append(HeroDecision(
                    street='preflop', action=action, amount=amount,
                    pot=context['pot'], to_call=context['to_call'],
                    num_opponents=max(1, num_opp), equity=0.0,
                    was_adjusted=False, oracle_action=action, is_preflop=True,
                    player_position=player.position,
                ))
            return (action, amount)

        # Postflop: extract features → oracle predict → adjuster
        feat_dict = build_features_from_game_state(player, game, context)
        num_opponents = len([p for p in context.get('active_opponents', [])
                            if not p.is_folded])

        if use_router:
            pred = oracle.predict(feat_dict, max(1, num_opponents))
        else:
            features = GtoOracle.features_from_dict(feat_dict)
            pred = oracle.predict(features)

        # Apply multiway adjustment with this variant's params
        adjusted = adjust(pred, feat_dict, max(1, num_opponents), params=params)
        action = adjusted.adjusted_action.lower()

        # Log the decision with full context for training export
        if decision_log is not None:
            hero_cards_str = ''.join(str(c) for c in player.hole_cards)
            board_str = ''.join(str(c) for c in game.community_cards)
            villain_pos = [p.position for p in context.get('active_opponents', [])
                           if not p.is_folded]
            decision_log.append(HeroDecision(
                street=context.get('street', 'unknown'),
                action=action, amount=0,  # amount set below
                pot=context['pot'], to_call=context['to_call'],
                num_opponents=max(1, num_opponents),
                equity=float(feat_dict.get('raw_equity', 0)),
                was_adjusted=adjusted.was_adjusted,
                oracle_action=pred.action.lower(),
                is_preflop=False,
                feat_dict=dict(feat_dict),
                hero_cards=hero_cards_str,
                board=board_str,
                villain_positions=villain_pos,
                facing_bet=bool(context.get('facing_bet', False)),
                player_position=player.position,
            ))

        # Map action to amount
        if action in ('fold', 'check'):
            return (action, 0)
        elif action == 'call':
            return ('call', game.current_bet)
        else:
            # bet or raise: 2/3 pot sizing
            amount = player.bet_this_street + max(int(context['pot'] * 0.67), 10)
            amount = min(amount, player.stack + player.bet_this_street)
            return (action, amount)

    return callback


class SelfPlayRunner:
    """Orchestrates one round of the self-play tournament."""

    def __init__(self, variants: List[Variant], num_deals: int = 100,
                 seed: int = 0, oracle_path: str = None,
                 oracle: object = None,
                 starting_stack: int = 1000,
                 log_all_multiway: bool = False):
        self.variants = variants
        self.num_deals = num_deals
        self.seed = seed
        self.starting_stack = starting_stack
        self.log_all_multiway = log_all_multiway

        # Load oracle: explicit oracle/router > oracle_path > default
        if oracle is not None:
            self.oracle = oracle
        elif oracle_path is not None:
            self.oracle = GtoOracle(oracle_path)
        else:
            # Try router first (auto-discovers specialist models)
            try:
                self.oracle = OracleRouter()
            except FileNotFoundError:
                # Fallback to legacy single model
                legacy = os.path.join(
                    os.path.dirname(__file__), 'models', 'gto_model_v8_38feat.json'
                )
                self.oracle = GtoOracle(legacy)

    def run_round(self, round_id: int = 1) -> RoundResult:
        """Run one complete round: all deals × all positions × all variants."""
        deal_gen = DealGenerator(seed=self.seed)
        deals = deal_gen.generate(self.num_deals)

        # Initialize scoring
        scores = {v.name: VariantScore(name=v.name) for v in self.variants}
        all_results = []

        for deal in deals:
            for hero_pos in POSITIONS:
                for variant in self.variants:
                    result = self._play_one_game(deal, hero_pos, variant)
                    all_results.append(result)

                    # Accumulate score
                    vs = scores[variant.name]
                    vs.total_chips += result.chips_won
                    vs.num_games += 1
                    if hero_pos not in vs.games_by_position:
                        vs.games_by_position[hero_pos] = []
                    vs.games_by_position[hero_pos].append(result.chips_won)

        return RoundResult(
            round_id=round_id,
            num_deals=self.num_deals,
            num_games=len(all_results),
            seed=self.seed,
            variant_results=scores,
            game_results=all_results,
        )

    def _play_one_game(self, deal: Deal, hero_pos: str,
                       variant: Variant) -> GameResult:
        """Play a single game with a specific deal, hero position, and variant."""
        # Seed global RNG for opponent AI reproducibility.
        # Unique per (deal, position, variant) so each game is deterministic.
        game_seed = hash((deal.deal_id, hero_pos, variant.name)) & 0xFFFFFFFF
        random.seed(game_seed)

        logger = HandLogger()
        game = PokerGame(headless=True, ai_callback=logger.on_action)

        # Reset all stacks to starting_stack (Gen 2: 100bb, independent deals)
        for p in game.players:
            p.stack = self.starting_stack

        # Wire ALL seats with oracle callbacks.
        # Hero: variant params + decision logging.
        # Opponents: baseline params. When log_all_multiway is True,
        # each opponent gets its own decision log (keyed by position)
        # so their multiway postflop decisions can be captured for
        # training data generation without cross-contaminating priors.
        baseline_params = get_default_params()
        hero_decisions: List[HeroDecision] = []
        opp_decisions: Dict[str, List[HeroDecision]] = {}
        for p in game.players:
            if p.position == hero_pos:
                p.decision_callback = _make_oracle_callback(
                    self.oracle, variant.params, hero_decisions)
            else:
                if self.log_all_multiway:
                    opp_decisions[p.position] = []
                    p.decision_callback = _make_oracle_callback(
                        self.oracle, baseline_params, opp_decisions[p.position])
                else:
                    p.decision_callback = _make_oracle_callback(
                        self.oracle, baseline_params)

        hero_player = game._player_at(hero_pos)

        # Snapshot stacks before
        logger.start_hand(game)

        # Play the hand with the predetermined deck.
        # deal_hand(deck_override=...) uses our stacked deck instead of
        # shuffling a random one. The deck is arranged so pop() yields
        # the correct hole cards and board cards in dealing order.
        game.play_hand(deck_override=deal.make_card_deck())

        # Record outcome
        hand_record = logger.end_hand(game)

        # Calculate hero's chip change
        hero_after = hero_player.stack
        # Hero started with starting_stack, minus any blind posted
        chips_won = hero_after - self.starting_stack

        return GameResult(
            deal_id=deal.deal_id,
            variant_name=variant.name,
            hero_position=hero_pos,
            chips_won=chips_won,
            hand_record=vars(hand_record) if hasattr(hand_record, '__dict__') else {},
            hero_decisions=hero_decisions,
            opponent_decisions=opp_decisions,
        )

    def save_results(self, result: RoundResult, output_dir: str) -> None:
        """Save round results to JSON files."""
        os.makedirs(output_dir, exist_ok=True)

        # Summary
        summary = {
            'round_id': result.round_id,
            'num_deals': result.num_deals,
            'num_games': result.num_games,
            'seed': result.seed,
            'variants': {},
        }
        for name, vs in result.variant_results.items():
            summary['variants'][name] = {
                'total_chips': vs.total_chips,
                'num_games': vs.num_games,
                'mbb_per_hand': round(vs.mbb_per_hand, 2),
                'by_position': {
                    pos: round(sum(chips) / len(chips) / 10.0 * 1000.0, 2)
                    for pos, chips in vs.games_by_position.items()
                    if chips
                },
            }

        summary_path = os.path.join(output_dir, f'round_{result.round_id}.json')
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
