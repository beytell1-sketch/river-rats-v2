"""Convergence checker for the self-play loop.

Measures decision stability between rounds. The loop converges when
the winning variant's decisions match the previous round's winner
on >95% of an evaluation set.

Master Plan §4.8:
  - Primary: decision stability >95% on evaluation set
  - Hard cap: 10 rounds maximum
  - If 6 parameter sets converge to similar EV: rule structure is the
    ceiling, signal for structural change between generations

Usage:
    from convergence_checker import check_convergence, ConvergenceResult

    result = check_convergence(
        current_round=round_result,
        previous_round=prev_result,
        stability_threshold=0.95,
        max_rounds=10,
    )
    if result.converged:
        print("Loop complete!")
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple

from self_play import RoundResult, GameResult, HeroDecision


@dataclass
class ConvergenceResult:
    """Result of convergence check between two rounds."""
    converged: bool
    round_number: int
    decision_stability: float    # 0.0–1.0, fraction of matching decisions
    hit_max_rounds: bool
    ev_spread: float             # mbb/hand spread between best and worst variant
    plateau_detected: bool       # True if all variants within narrow EV band
    winner_name: str
    previous_winner_name: str
    matching_decisions: int
    total_decisions: int
    reason: str                  # human-readable convergence reason


# EV spread below this (mbb/hand) signals a plateau — all variants
# performing similarly means thresholds aren't the lever.
PLATEAU_THRESHOLD_MBB = 5.0


def check_convergence(current_round: RoundResult,
                      previous_round: Optional[RoundResult] = None,
                      stability_threshold: float = 0.95,
                      max_rounds: int = 10) -> ConvergenceResult:
    """Check whether the self-play loop should stop.

    Args:
        current_round: Results from the round just completed.
        previous_round: Results from the previous round (None for round 1).
        stability_threshold: Required fraction of matching decisions (default 0.95).
        max_rounds: Hard cap on total rounds (default 10).

    Returns:
        ConvergenceResult with convergence status and diagnostics.
    """
    round_num = current_round.round_id

    # Find current winner
    current_scores = sorted(
        current_round.variant_results.values(),
        key=lambda vs: vs.mbb_per_hand,
        reverse=True,
    )
    current_winner = current_scores[0].name if current_scores else ""

    # EV spread
    if len(current_scores) >= 2:
        ev_spread = current_scores[0].mbb_per_hand - current_scores[-1].mbb_per_hand
    else:
        ev_spread = 0.0

    plateau = ev_spread < PLATEAU_THRESHOLD_MBB and len(current_scores) >= 3

    # Hard cap
    if round_num >= max_rounds:
        return ConvergenceResult(
            converged=True,
            round_number=round_num,
            decision_stability=0.0,
            hit_max_rounds=True,
            ev_spread=ev_spread,
            plateau_detected=plateau,
            winner_name=current_winner,
            previous_winner_name="",
            matching_decisions=0,
            total_decisions=0,
            reason=f"Hard cap reached ({max_rounds} rounds)",
        )

    # Round 1: no previous round to compare against
    if previous_round is None:
        return ConvergenceResult(
            converged=False,
            round_number=round_num,
            decision_stability=0.0,
            hit_max_rounds=False,
            ev_spread=ev_spread,
            plateau_detected=plateau,
            winner_name=current_winner,
            previous_winner_name="",
            matching_decisions=0,
            total_decisions=0,
            reason="First round — no baseline for stability comparison",
        )

    # Find previous winner
    prev_scores = sorted(
        previous_round.variant_results.values(),
        key=lambda vs: vs.mbb_per_hand,
        reverse=True,
    )
    prev_winner = prev_scores[0].name if prev_scores else ""

    # Compare decisions between current winner and previous winner
    # on all shared (deal_id, hero_position) pairs
    stability, matching, total = _compare_winner_decisions(
        current_round, current_winner,
        previous_round, prev_winner,
    )

    converged = stability >= stability_threshold and total > 0

    if converged:
        reason = (f"Decision stability {stability:.1%} >= {stability_threshold:.0%} "
                  f"({matching}/{total} decisions match)")
    elif plateau:
        reason = (f"EV spread {ev_spread:.1f} mbb/hand — all variants similar. "
                  f"Rule structure may be the ceiling.")
    else:
        reason = (f"Decision stability {stability:.1%} < {stability_threshold:.0%} "
                  f"({matching}/{total} decisions match)")

    return ConvergenceResult(
        converged=converged,
        round_number=round_num,
        decision_stability=stability,
        hit_max_rounds=False,
        ev_spread=ev_spread,
        plateau_detected=plateau,
        winner_name=current_winner,
        previous_winner_name=prev_winner,
        matching_decisions=matching,
        total_decisions=total,
        reason=reason,
    )


def _compare_winner_decisions(
    current: RoundResult, current_winner: str,
    previous: RoundResult, prev_winner: str,
) -> Tuple[float, int, int]:
    """Compare first decisions of two winners on shared deal+position pairs.

    Only compares the FIRST decision per deal+position (before any
    game-state divergence). Returns (stability_ratio, matching, total).
    """
    # Index current winner's first decisions by (deal_id, hero_position)
    current_first = _extract_first_decisions(current.game_results, current_winner)
    prev_first = _extract_first_decisions(previous.game_results, prev_winner)

    # Find shared keys (same deal_id + hero_position in both rounds)
    # Note: if seeds differ between rounds, there are no shared keys.
    # The typical pattern is same seed → same deals → direct comparison.
    shared = set(current_first.keys()) & set(prev_first.keys())

    if not shared:
        return (0.0, 0, 0)

    matching = 0
    for key in shared:
        if current_first[key] == prev_first[key]:
            matching += 1

    total = len(shared)
    stability = matching / total if total > 0 else 0.0
    return (stability, matching, total)


def _extract_first_decisions(
    game_results: List[GameResult], variant_name: str
) -> Dict[Tuple[int, str], str]:
    """Extract the first hero action per (deal_id, hero_position) for a variant."""
    first_actions = {}
    for gr in game_results:
        if gr.variant_name == variant_name and gr.hero_decisions:
            key = (gr.deal_id, gr.hero_position)
            first_actions[key] = gr.hero_decisions[0].action
    return first_actions


def format_convergence_report(result: ConvergenceResult) -> str:
    """Format a human-readable convergence report."""
    lines = [
        f"Convergence Check — Round {result.round_number}",
        f"{'=' * 45}",
        f"Converged:          {'YES' if result.converged else 'NO'}",
        f"Reason:             {result.reason}",
        f"Current winner:     {result.winner_name}",
        f"Previous winner:    {result.previous_winner_name or 'N/A'}",
        f"Decision stability: {result.decision_stability:.1%}",
        f"  ({result.matching_decisions}/{result.total_decisions} match)",
        f"EV spread:          {result.ev_spread:.1f} mbb/hand",
        f"Plateau detected:   {'YES' if result.plateau_detected else 'NO'}",
        f"Hit max rounds:     {'YES' if result.hit_max_rounds else 'NO'}",
    ]
    return "\n".join(lines)
