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

FEATURE_COLUMNS_59 = tuple(_FE_COLS)

# Module-load guard: if `feature_extractor.FEATURE_COLUMNS` ever extends
# beyond 59 (e.g., a future feature add), this assertion trips and forces
# the dispatch to be rewired explicitly rather than silently routing wrong-
# sized arrays to 59-trained models.
assert len(FEATURE_COLUMNS_59) == N_FEATURES_59, (
    f"inference_path_59 requires feature_extractor.FEATURE_COLUMNS to "
    f"contain exactly {N_FEATURES_59} entries; found {len(FEATURE_COLUMNS_59)}. "
    f"If feature surface has changed, update this module + oracle_router "
    f"surface-size dispatch logic explicitly."
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
