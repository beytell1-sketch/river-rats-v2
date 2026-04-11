"""Variant evolver for the self-play loop.

Mechanical combination of winning traits between rounds.
No creative invention — just parameter merging.

Evolution rules (Master Plan §4.10):
  - Keep top 2 winners unchanged
  - Create 2 hybrids (merge overrides from top 3)
  - Pick 2 untested hypotheses from the hypothesis pool
  - No new parameters invented mid-loop

Usage:
    from variant_evolver import evolve_variants

    next_variants = evolve_variants(
        round_result=result,
        hypothesis_pool=all_hypotheses,
        used_names={"baseline", "tight", ...},
    )
"""
from __future__ import annotations
from typing import List, Set, Dict

from self_play import Variant, RoundResult, VariantScore
from multiway_adjuster import get_default_params


def evolve_variants(round_result: RoundResult,
                    hypothesis_pool: List[Variant],
                    used_names: Set[str],
                    num_variants: int = 6) -> List[Variant]:
    """Produce the next round's 6 variants from current results.

    Args:
        round_result: Results from the completed round.
        hypothesis_pool: All available hypotheses (including untested ones).
        used_names: Names of variants already tested in any round.
        num_variants: How many variants to produce (default 6).

    Returns:
        List of Variant objects for the next round.
    """
    # Rank variants by mbb/hand
    ranked = sorted(
        round_result.variant_results.values(),
        key=lambda vs: vs.mbb_per_hand,
        reverse=True,
    )

    # 1. Keep top 2 winners unchanged
    winners = []
    for vs in ranked[:2]:
        original = _find_variant(vs.name, hypothesis_pool, round_result)
        if original:
            winners.append(original)

    # 2. Create 2 hybrids from top 3
    top3 = []
    for vs in ranked[:3]:
        original = _find_variant(vs.name, hypothesis_pool, round_result)
        if original:
            top3.append(original)

    hybrids = _make_hybrids(top3, used_names)

    # 3. Pick untested hypotheses
    untested = [v for v in hypothesis_pool if v.name not in used_names]
    picks = untested[:max(0, num_variants - len(winners) - len(hybrids))]

    # Assemble: winners + hybrids + untested, cap at num_variants
    next_round = winners + hybrids + picks
    next_round = next_round[:num_variants]

    # If we still don't have enough (exhausted pool), pad with top performers
    while len(next_round) < num_variants and ranked:
        for vs in ranked:
            original = _find_variant(vs.name, hypothesis_pool, round_result)
            if original and original.name not in {v.name for v in next_round}:
                next_round.append(original)
                break
        else:
            break

    return next_round


def _find_variant(name: str, pool: List[Variant],
                  result: RoundResult) -> Variant | None:
    """Find a variant by name in the pool or reconstruct from result."""
    for v in pool:
        if v.name == name:
            return v
    # Not in pool — might be a hybrid from a previous round
    # Reconstruct from the result's game data if possible
    return None


def _make_hybrids(top_variants: List[Variant],
                  used_names: Set[str]) -> List[Variant]:
    """Create 2 hybrid variants by merging parameters from top performers.

    Hybrid A: average of top 1 and top 2 params
    Hybrid B: average of top 1 and top 3 params (or top 2 if only 2 available)
    """
    if len(top_variants) < 2:
        return []

    baseline = get_default_params()
    hybrids = []

    # Hybrid A: merge top 1 + top 2
    name_a = f"hybrid_{top_variants[0].name}_{top_variants[1].name}"
    if name_a not in used_names:
        params_a = _merge_params(top_variants[0].params, top_variants[1].params, baseline)
        hybrids.append(Variant(
            name=name_a,
            params=params_a,
            rationale=f"Hybrid of {top_variants[0].name} and {top_variants[1].name}",
        ))

    # Hybrid B: merge top 1 + top 3 (or top 2 again with different weighting)
    if len(top_variants) >= 3:
        partner = top_variants[2]
    else:
        partner = top_variants[1]

    name_b = f"hybrid_{top_variants[0].name}_{partner.name}_v2"
    if name_b not in used_names:
        # Weight toward the winner: 2/3 top1, 1/3 partner
        params_b = _merge_params(
            top_variants[0].params, partner.params, baseline, weight_a=0.67
        )
        hybrids.append(Variant(
            name=name_b,
            params=params_b,
            rationale=f"Weighted hybrid (67/33) of {top_variants[0].name} and {partner.name}",
        ))

    return hybrids[:2]


def _merge_params(params_a: dict, params_b: dict, baseline: dict,
                  weight_a: float = 0.5) -> dict:
    """Merge two parameter dicts by weighted average.

    Only averages numeric values. Non-numeric values take from params_a.
    """
    merged = dict(baseline)
    weight_b = 1.0 - weight_a

    for key in baseline:
        val_a = params_a.get(key, baseline[key])
        val_b = params_b.get(key, baseline[key])

        if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
            avg = val_a * weight_a + val_b * weight_b
            # Preserve int type for integer params
            if isinstance(baseline[key], int):
                merged[key] = round(avg)
            else:
                merged[key] = round(avg, 4)
        else:
            merged[key] = val_a

    return merged
