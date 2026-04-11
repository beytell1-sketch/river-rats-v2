"""Observer flag tagger for self-play teaching signals.

The observer is a camera crew — it watches and tags but NEVER
influences decisions. Flags are computed from the same features
the oracle already sees, labelled in human language for the
teaching system to use later.

Three flag categories:
  - Situation flags: computed from features BEFORE the decision
  - Decision flags: computed AFTER the oracle chooses
  - Outcome flags: computed after the hand resolves

Usage:
    from observer import tag_situation, tag_decision, tag_outcome, ObserverFlags

    flags = ObserverFlags()
    tag_situation(flags, hero_decision, context_features)
    tag_decision(flags, hero_decision, hu_baseline_action)
    tag_outcome(flags, chips_won, went_to_showdown, hero_folded)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional

from self_play import HeroDecision


@dataclass
class ObserverFlags:
    """All flags for one decision point."""
    # Situation flags (before decision)
    hero_has_draw: bool = False
    hero_vulnerable: bool = False
    hero_dominating: bool = False
    villain_range_capped: bool = False
    multiway_pressure: bool = False
    positional_advantage: bool = False
    facing_aggression: bool = False
    pot_committed: bool = False

    # Decision flags (after oracle chooses)
    deviated_from_hu: bool = False
    tightened: bool = False
    loosened: bool = False
    protected: bool = False
    pot_controlled: bool = False

    # Outcome flags (after hand resolves)
    decision_profitable: bool = False
    showdown_winner: bool = False
    fold_equity_captured: bool = False
    drew_out: bool = False

    def to_dict(self) -> Dict[str, bool]:
        return {k: v for k, v in self.__dict__.items()}

    @property
    def situation_flags(self) -> Dict[str, bool]:
        return {
            'hero_has_draw': self.hero_has_draw,
            'hero_vulnerable': self.hero_vulnerable,
            'hero_dominating': self.hero_dominating,
            'villain_range_capped': self.villain_range_capped,
            'multiway_pressure': self.multiway_pressure,
            'positional_advantage': self.positional_advantage,
            'facing_aggression': self.facing_aggression,
            'pot_committed': self.pot_committed,
        }

    @property
    def decision_flags(self) -> Dict[str, bool]:
        return {
            'deviated_from_hu': self.deviated_from_hu,
            'tightened': self.tightened,
            'loosened': self.loosened,
            'protected': self.protected,
            'pot_controlled': self.pot_controlled,
        }

    @property
    def outcome_flags(self) -> Dict[str, bool]:
        return {
            'decision_profitable': self.decision_profitable,
            'showdown_winner': self.showdown_winner,
            'fold_equity_captured': self.fold_equity_captured,
            'drew_out': self.drew_out,
        }


# Thresholds for flag computation (from master plan Section 4.7)
_DRAW_OUTS_THRESHOLD = 0       # draw_outs > 0
_VULNERABLE_DANGER = 0.6       # danger_score > 0.6
_DOMINATING_EQUITY = 0.75      # equity > 0.75
_POT_COMMITTED_SPR = 3.0       # SPR < 3

# Action strength ordering for tightened/loosened detection
_ACTION_STRENGTH = {
    'fold': 0, 'check': 1, 'call': 2, 'bet': 3, 'raise': 4,
}


def tag_situation(flags: ObserverFlags, decision: HeroDecision,
                  feat_dict: Optional[Dict] = None) -> None:
    """Tag situation flags from features available before the decision.

    Args:
        flags: ObserverFlags to update in place.
        decision: The hero's decision (has equity, num_opponents, etc.)
        feat_dict: Optional full feature dict (if available) for richer tagging.
    """
    flags.hero_has_draw = (
        (feat_dict.get('draw_outs', 0) > _DRAW_OUTS_THRESHOLD)
        if feat_dict else False
    )

    flags.hero_vulnerable = (
        feat_dict.get('is_made_hand', 0) > 0
        and feat_dict.get('danger_score', 0) > _VULNERABLE_DANGER
    ) if feat_dict else False

    flags.hero_dominating = decision.equity > _DOMINATING_EQUITY

    flags.villain_range_capped = (
        feat_dict.get('villain_checked_back', 0) > 0
    ) if feat_dict else False

    flags.multiway_pressure = decision.num_opponents >= 3

    flags.positional_advantage = (
        feat_dict.get('is_ip', 0) > 0
    ) if feat_dict else False

    flags.facing_aggression = decision.to_call > 0

    flags.pot_committed = (
        feat_dict.get('spr', 999) < _POT_COMMITTED_SPR
    ) if feat_dict else False


def tag_decision(flags: ObserverFlags, decision: HeroDecision,
                 hu_baseline_action: Optional[str] = None) -> None:
    """Tag decision flags by comparing the oracle's choice to HU baseline.

    Args:
        flags: ObserverFlags to update in place.
        decision: The hero's decision (has action, oracle_action, was_adjusted).
        hu_baseline_action: What the HU oracle would have chosen (before adjuster).
            If None, uses decision.oracle_action as the HU baseline.
    """
    baseline = hu_baseline_action or decision.oracle_action
    actual = decision.action

    flags.deviated_from_hu = (actual != baseline)

    baseline_strength = _ACTION_STRENGTH.get(baseline, 0)
    actual_strength = _ACTION_STRENGTH.get(actual, 0)

    # Tightened: action is weaker than HU baseline
    # e.g., HU=BET→CHECK, HU=RAISE→CALL
    flags.tightened = (actual_strength < baseline_strength)

    # Loosened: action is stronger than HU baseline (rare in multiway)
    # e.g., HU=CHECK→BET
    flags.loosened = (actual_strength > baseline_strength)

    # Protected: bet/raise with a vulnerable made hand
    flags.protected = (
        actual in ('bet', 'raise')
        and flags.hero_vulnerable
    )

    # Pot controlled: checked with a strong-but-not-monster hand
    flags.pot_controlled = (
        actual in ('check', 'call')
        and not flags.hero_dominating
        and decision.equity > 0.4
    )


def tag_outcome(flags: ObserverFlags, chips_won: int,
                went_to_showdown: bool, hero_folded: bool,
                opponents_folded: bool = False) -> None:
    """Tag outcome flags after the hand resolves.

    Args:
        flags: ObserverFlags to update in place.
        chips_won: Hero's chip change for this hand.
        went_to_showdown: Whether hand went to showdown.
        hero_folded: Whether hero folded during the hand.
        opponents_folded: Whether all opponents folded to hero's bet.
    """
    flags.decision_profitable = chips_won > 0
    flags.showdown_winner = went_to_showdown and chips_won > 0
    flags.fold_equity_captured = opponents_folded and chips_won > 0
    # drew_out requires board history we don't have yet — default False
    flags.drew_out = False


def tag_game(game_result, feat_dicts: Optional[list] = None) -> list:
    """Tag all decisions in a GameResult. Returns list of ObserverFlags.

    Convenience function that runs all three tagging phases per decision.

    Args:
        game_result: GameResult with hero_decisions.
        feat_dicts: Optional list of feature dicts, one per decision.
            Features change per street (equity, danger_score, draw_outs
            differ flop vs turn vs river). If None, situation flags that
            require features will be False. If a single dict is passed
            (not a list), it's applied to all decisions (backward compat).
    """
    from self_play import GameResult
    flags_list = []

    # Normalize feat_dicts input
    if feat_dicts is not None and isinstance(feat_dicts, dict):
        # Single dict passed — apply to all (backward compat, but not ideal)
        feat_dicts = [feat_dicts] * len(game_result.hero_decisions)

    # Precompute hand-level outcome data
    hero_folded = any(d.action == 'fold' for d in game_result.hero_decisions)
    opponents_folded = (
        game_result.chips_won > 0
        and not game_result.hand_record.get('went_to_showdown', False)
        and not hero_folded
    )
    went_to_showdown = game_result.hand_record.get('went_to_showdown', False)

    for i, decision in enumerate(game_result.hero_decisions):
        flags = ObserverFlags()

        # Per-decision feature dict (if available)
        feat = feat_dicts[i] if feat_dicts and i < len(feat_dicts) else None
        tag_situation(flags, decision, feat)
        tag_decision(flags, decision)

        # Outcome is per-hand, not per-decision — apply to all decisions
        tag_outcome(flags, game_result.chips_won,
                    went_to_showdown, hero_folded, opponents_folded)

        flags_list.append(flags)

    return flags_list
