"""Decision-point comparator for self-play analysis.

Groups games by (deal_id, hero_position) and finds where variants
made different decisions at the same decision point. Each divergence
is a data point for understanding which strategy choices work better.

Usage:
    from decision_comparator import compare_decisions, Divergence

    result = runner.run_round()
    divergences = compare_decisions(result.game_results)

    for d in divergences:
        print(f"Deal {d.deal_id} {d.hero_position} {d.street}: "
              f"{d.decisions_by_variant}")
"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

from self_play import GameResult, HeroDecision


@dataclass
class VariantDecision:
    """What one variant did at a specific decision point."""
    variant_name: str
    action: str
    oracle_action: str    # pre-adjustment action
    was_adjusted: bool
    equity: float
    chips_won: int        # outcome for the whole hand


@dataclass
class Divergence:
    """A decision point where variants chose differently."""
    deal_id: int
    hero_position: str
    street: str
    decision_index: int       # which decision in the hand (0=first)
    pot: int
    to_call: int
    num_opponents: int
    decisions: List[VariantDecision]

    @property
    def actions(self) -> Dict[str, str]:
        """Map of variant_name → action."""
        return {d.variant_name: d.action for d in self.decisions}

    @property
    def unique_actions(self) -> set:
        return set(d.action for d in self.decisions)

    @property
    def best_variant(self) -> str:
        """Variant with highest chips_won at this deal+position."""
        return max(self.decisions, key=lambda d: d.chips_won).variant_name

    @property
    def worst_variant(self) -> str:
        return min(self.decisions, key=lambda d: d.chips_won).variant_name

    @property
    def chip_spread(self) -> int:
        """Difference between best and worst outcome."""
        chips = [d.chips_won for d in self.decisions]
        return max(chips) - min(chips)


@dataclass
class ComparisonSummary:
    """Aggregate statistics from comparing all decision points."""
    total_decision_points: int      # across all deals × positions
    divergent_points: int           # where at least 2 variants differ
    divergence_rate: float          # divergent / total
    divergences: List[Divergence]
    action_pair_counts: Dict[Tuple[str, str], int]  # (action_a, action_b) → count
    variant_win_rate: Dict[str, float]  # how often each variant was "best" at divergences
    avg_chip_spread: float


def compare_decisions(game_results: List[GameResult]) -> ComparisonSummary:
    """Compare hero decisions across variants for all deal+position pairs.

    Groups games by (deal_id, hero_position), then aligns decisions
    street-by-street. A divergence is any point where at least two
    variants chose different actions.
    """
    # Group by (deal_id, hero_position)
    groups: Dict[Tuple[int, str], List[GameResult]] = defaultdict(list)
    for gr in game_results:
        groups[(gr.deal_id, gr.hero_position)].append(gr)

    divergences = []
    total_points = 0
    action_pairs: Dict[Tuple[str, str], int] = defaultdict(int)
    variant_wins: Dict[str, int] = defaultdict(int)

    for (deal_id, hero_pos), games in groups.items():
        if len(games) < 2:
            continue

        # Compare decisions only up to (and including) the first divergence.
        # After a divergent hero action, opponents react differently on each
        # table, so later decisions are at different game states and comparing
        # them is meaningless. (Master Plan §4.4: "same prior action history")
        min_decisions = min(len(g.hero_decisions) for g in games)

        for dec_idx in range(min_decisions):
            total_points += 1

            # Collect each variant's decision at this index
            variant_decs = []
            for g in games:
                hd = g.hero_decisions[dec_idx]
                variant_decs.append(VariantDecision(
                    variant_name=g.variant_name,
                    action=hd.action,
                    oracle_action=hd.oracle_action,
                    was_adjusted=hd.was_adjusted,
                    equity=hd.equity,
                    chips_won=g.chips_won,
                ))

            # Check if there's a divergence
            actions = set(vd.action for vd in variant_decs)
            if len(actions) > 1:
                ref_hd = games[0].hero_decisions[dec_idx]
                div = Divergence(
                    deal_id=deal_id,
                    hero_position=hero_pos,
                    street=ref_hd.street,
                    decision_index=dec_idx,
                    pot=ref_hd.pot,
                    to_call=ref_hd.to_call,
                    num_opponents=ref_hd.num_opponents,
                    decisions=variant_decs,
                )
                divergences.append(div)

                # Count action pairs
                sorted_actions = sorted(actions)
                for i in range(len(sorted_actions)):
                    for j in range(i + 1, len(sorted_actions)):
                        action_pairs[(sorted_actions[i], sorted_actions[j])] += 1

                # Track which variant won at this divergence
                variant_wins[div.best_variant] += 1

                # Stop comparing this deal+position — game states diverge
                # from here. Only the first divergence is valid.
                break

    # Compute summary stats
    divergent_count = len(divergences)
    total_variants = set()
    for gr in game_results:
        total_variants.add(gr.variant_name)

    variant_win_rate = {}
    if divergent_count > 0:
        for v in total_variants:
            variant_win_rate[v] = variant_wins.get(v, 0) / divergent_count
        avg_spread = sum(d.chip_spread for d in divergences) / divergent_count
    else:
        for v in total_variants:
            variant_win_rate[v] = 0.0
        avg_spread = 0.0

    return ComparisonSummary(
        total_decision_points=total_points,
        divergent_points=divergent_count,
        divergence_rate=divergent_count / max(1, total_points),
        divergences=divergences,
        action_pair_counts=dict(action_pairs),
        variant_win_rate=variant_win_rate,
        avg_chip_spread=avg_spread,
    )


def format_divergence_report(summary: ComparisonSummary) -> str:
    """Format a human-readable report of divergences."""
    lines = [
        f"Decision-Point Comparison Report",
        f"================================",
        f"Total decision points:  {summary.total_decision_points}",
        f"Divergent points:       {summary.divergent_points}",
        f"Divergence rate:        {summary.divergence_rate:.1%}",
        f"Avg chip spread:        {summary.avg_chip_spread:.1f}",
        f"",
        f"Action pair frequencies:",
    ]
    for (a1, a2), count in sorted(summary.action_pair_counts.items(),
                                   key=lambda x: -x[1]):
        lines.append(f"  {a1} vs {a2}: {count}")

    lines.append("")
    lines.append("Variant win rates at divergences:")
    for v, rate in sorted(summary.variant_win_rate.items(), key=lambda x: -x[1]):
        lines.append(f"  {v}: {rate:.1%}")

    if summary.divergences:
        lines.append("")
        lines.append(f"Top 10 highest-impact divergences:")
        top = sorted(summary.divergences, key=lambda d: -d.chip_spread)[:10]
        for d in top:
            actions_str = ", ".join(f"{vd.variant_name}={vd.action}"
                                   for vd in d.decisions)
            lines.append(
                f"  Deal {d.deal_id} {d.hero_position} {d.street} "
                f"(spread={d.chip_spread}): {actions_str}"
            )

    return "\n".join(lines)
