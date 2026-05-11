"""59-feature production inference path — Phase 1.5-E PR-A.

Provides a public 59-feature feature-extraction helper for inference at
production runtime. Used by `oracle_router.py` for models with
`n_features_in_ > 55` (currently: vNext-HU-59 + v9-3way-on-59 / v9-3way-v2.2).

Provenance
----------
Built per Phase 1.5-E AMENDMENT (Option C; PR #378) at master `7c6e845`,
in response to builder STOP (PR #377) where `oracle_router.predict()`
crashed on vNext-HU-59 with `ValueError: Feature shape mismatch, expected:
59, got 55`.

Background
----------
The legacy `gto_model.FEATURE_COLUMNS` tuple has 55 entries (production
runtime ceiling). Modern HU + 3-way models trained against
`feature_extractor.FEATURE_COLUMNS` (59 entries) cannot consume features
built from the legacy 55-tuple. Per `train_model_v9_student.py` Path Y:
extending `gto_model.FEATURE_COLUMNS` is forbidden because it is shared
across multiple inference paths and would risk regressing legacy
consumers.

This module provides a parallel public 59-feature path. `oracle_router`
selects between the legacy 55-feature path (`GtoOracle.features_from_dict`)
and this 59-feature path based on the model's expected feature count
(`oracle._n_features`).

Design choices
--------------
- Imports `feature_extractor.FEATURE_COLUMNS` directly (same source of
  truth as the trainers); guards with module-load assertion that it
  remains 59 entries (so future extension to 60+ trips this module).
- Pure function (`features_from_dict_59`); no class wrapper; matches the
  style of `gto_model.GtoOracle.features_from_dict`.
- Stateless — caller supplies feat_dict and gets numpy array. No model
  loading; oracle continues to be loaded by `GtoOracle`.

Usage (from oracle_router):
    from inference_path_59 import FEATURE_COLUMNS_59, features_from_dict_59
    if oracle._n_features >= 59:
        features = features_from_dict_59(feat_dict)
    else:
        features = GtoOracle.features_from_dict(feat_dict)
    pred = oracle.predict(features)
"""
from __future__ import annotations

import os
import sys
from typing import Dict

import numpy as np

# Make river-rats-core importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feature_extractor import FEATURE_COLUMNS as _FE_COLS


# Public surface size constant — current 59-feature production surface
N_FEATURES_59 = 59

# Canonical 59-feature production surface — captured at Phase 1.5-B prune
# (PR #356) and Phase 1.5-E PR-A (PR #379). This frozen tuple is the
# load-time invariant: production HU + 3-way inference always builds an
# array in exactly this order. If feature_extractor.FEATURE_COLUMNS later
# appends new features (e.g., Phase 2-B PILOT), the FIRST 59 entries MUST
# remain identical to this list or the dispatch silently routes wrong-
# sized / mis-ordered arrays to 59-trained production models.
_CANONICAL_FEATURE_COLUMNS_59 = (
    'street', 'facing_bet', 'pot_size', 'to_call', 'pot_odds', 'bet_to_pot',
    'hero_position', 'villain_position', 'is_ip', 'hand_category', 'hand_rank',
    'is_made_hand', 'is_strong_made', 'is_monster', 'has_flush_draw',
    'has_straight_draw', 'draw_outs', 'is_monotone', 'is_two_tone', 'is_rainbow',
    'is_paired', 'is_double_paired', 'connectivity_score', 'high_card_rank',
    'danger_score', 'flush_danger', 'straight_danger', 'raw_equity',
    'equity_vs_range', 'better_hand_pct', 'worse_hand_pct', 'equity_margin',
    'spr', 'is_3bet_pot', 'villain_aggression_count', 'villain_checked_back',
    'villain_call_count', 'num_opponents', 'villain_top_pair_plus_pct',
    'villain_draw_pct', 'villain_air_pct', 'villain_range_capped',
    'board_favour', 'num_callers_to_bet', 'facing_raise', 'flush_block_pct',
    'overcard_outs', 'improvement_probability', 'hero_range_percentile',
    'has_showdown_value', 'villain_fold_equity_estimate', 'flush_draw_rank',
    'is_preflop_aggressor', 'villain_medium_made_pct', 'board_adjusted_hrp',
    'nut_flush_block', 'flush_draw_block_pct', 'straight_draw_block_pct',
    'nut_made_block_pct',
)

FEATURE_COLUMNS_59 = _CANONICAL_FEATURE_COLUMNS_59

# Module-load guard: production-surface integrity. The 59-feature production
# inference array MUST match the canonical column order — even after
# feature_extractor extends with new columns (Phase 2-B PILOT and beyond).
# This guard trips if the FIRST 59 entries of feature_extractor.FEATURE_COLUMNS
# diverge from canonical (e.g., column reorder, rename, or removal), which
# would silently break vNext-HU-59 + v9-3way-on-59 inference.
_fe_first_59 = tuple(_FE_COLS[:N_FEATURES_59])
assert len(_FE_COLS) >= N_FEATURES_59, (
    f"feature_extractor.FEATURE_COLUMNS has only {len(_FE_COLS)} entries; "
    f"need ≥{N_FEATURES_59} for production 59-feature path."
)
assert _fe_first_59 == _CANONICAL_FEATURE_COLUMNS_59, (
    f"feature_extractor.FEATURE_COLUMNS first {N_FEATURES_59} entries diverged "
    f"from canonical production surface. Diff: "
    f"{[(i, _fe_first_59[i], _CANONICAL_FEATURE_COLUMNS_59[i]) for i in range(N_FEATURES_59) if _fe_first_59[i] != _CANONICAL_FEATURE_COLUMNS_59[i]][:5]}. "
    f"Production 59-trained models will silently produce wrong predictions. "
    f"Surface re-extension requires explicit dispatch rewire in oracle_router."
)


def features_from_dict_59(feat_dict: Dict[str, float]) -> np.ndarray:
    """Build a 59-feature numpy array from a feat_dict for inference.

    Parallel to `gto_model.GtoOracle.features_from_dict` but uses the
    59-entry feature_extractor surface instead of the 55-entry gto_model
    surface.

    Args:
        feat_dict: Full feature dict from `feature_extractor.extract_all_features`.

    Returns:
        numpy.ndarray of shape (59,) dtype float32.

    Raises:
        KeyError: if any of the 59 FEATURE_COLUMNS_59 keys are absent
            from feat_dict (callers must populate via
            `feature_extractor.extract_all_features`).
    """
    missing = [k for k in FEATURE_COLUMNS_59 if k not in feat_dict]
    if missing:
        raise KeyError(
            f"feat_dict missing {len(missing)} of {N_FEATURES_59} keys: "
            f"{missing[:5]}... Run feature_extractor.extract_all_features() "
            f"before calling features_from_dict_59()."
        )
    return np.array(
        [float(feat_dict[k]) for k in FEATURE_COLUMNS_59],
        dtype=np.float32,
    )
