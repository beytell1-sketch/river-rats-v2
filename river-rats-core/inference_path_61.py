"""61-feature production inference path — Phase 2-C cleanup.

Provides a public 61-feature feature-extraction helper for inference at
production runtime. Used by `oracle_router.py` for models trained on the
Phase 2-C surface (post-cleanup: 59 baseline + 2 confirmed pilot winners).

Provenance
----------
Built per Phase 2-C dispatch (PR #400) at master `bbda9d9` after Phase
2-B re-pilot delivered 2/4 gate-pass and owner ratified Option B
(partial-proceed with the 2 confirmed winners).

Surface composition (61 features = 59 + 2):
  Indices 0..58: canonical 59-feature production surface (matches
                 `inference_path_59.FEATURE_COLUMNS_59`).
  Index 59:      players_to_act_after_hero (AMENDMENT 1; re-pilot 3.36%)
  Index 60:      tpmk_kicker_rank (MW-40 axis; re-pilot 9.18% rank #2)

Design choices
--------------
- Modeled on `inference_path_59.py`: same pattern (frozen canonical tuple
  + module-load assertion + pure function).
- The canonical 61-tuple is `FEATURE_COLUMNS_59 + (players_to_act, tpmk)`.
- Module-load assertion validates that `feature_extractor.FEATURE_COLUMNS`'s
  first-59 entries match `FEATURE_COLUMNS_59` AND last-2 entries match the
  2 canonical pilot winners.

Usage (from oracle_router; wiring deferred to Phase 2-H):
    from inference_path_61 import FEATURE_COLUMNS_61, features_from_dict_61
    if oracle._n_features == N_FEATURES_61:
        features = features_from_dict_61(feat_dict)
    elif oracle._n_features >= N_FEATURES_59:
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
from inference_path_59 import (
    FEATURE_COLUMNS_59 as _CANONICAL_59,
    N_FEATURES_59,
)


# Public surface size constant — Phase 2-C cleanup 61-feature surface
N_FEATURES_61 = 61

# Canonical 2 pilot features added at indices 59-60 (Phase 2-C cleanup).
# Order matches feature_extractor.FEATURE_COLUMNS tail; re-pilot winners
# per `BUILDER_REPORT_PHASE2B_REPILOT_2026-05-11.md` gate-pass evidence.
_CANONICAL_PILOT_2 = (
    'players_to_act_after_hero',
    'tpmk_kicker_rank',
)

FEATURE_COLUMNS_61 = _CANONICAL_59 + _CANONICAL_PILOT_2

# Module-load guard: production-surface integrity for the 61-feature path.
# The 61-feature production inference array MUST be in canonical column
# order. This guard trips if either:
#   (a) the FIRST 59 entries of feature_extractor.FEATURE_COLUMNS diverge
#       from canonical 59 (would silently break vNext-HU-59 + v9-3way-on-59
#       inference for the 59-feat models still in production), OR
#   (b) the LAST 2 entries diverge from the 2 confirmed pilot winners
#       (would silently break the 61-feat models trained on this surface).
_fe_first_59 = tuple(_FE_COLS[:N_FEATURES_59])
_fe_last_2 = tuple(_FE_COLS[N_FEATURES_59:N_FEATURES_61])
assert len(_FE_COLS) >= N_FEATURES_61, (
    f"feature_extractor.FEATURE_COLUMNS has only {len(_FE_COLS)} entries; "
    f"need ≥{N_FEATURES_61} for production 61-feature path."
)
assert _fe_first_59 == _CANONICAL_59, (
    f"feature_extractor.FEATURE_COLUMNS first {N_FEATURES_59} entries "
    f"diverged from canonical 59 production surface. Diff: "
    f"{[(i, _fe_first_59[i], _CANONICAL_59[i]) for i in range(N_FEATURES_59) if _fe_first_59[i] != _CANONICAL_59[i]][:5]}."
)
assert _fe_last_2 == _CANONICAL_PILOT_2, (
    f"feature_extractor.FEATURE_COLUMNS indices {N_FEATURES_59}..{N_FEATURES_61-1} "
    f"diverged from canonical 61-feature pilot winners. Found: {_fe_last_2}. "
    f"Expected: {_CANONICAL_PILOT_2}."
)


def features_from_dict_61(feat_dict: Dict[str, float]) -> np.ndarray:
    """Build a 61-feature numpy array from a feat_dict for inference.

    Parallel to `inference_path_59.features_from_dict_59` but uses the
    61-entry Phase 2-C cleanup surface.

    Args:
        feat_dict: Full feature dict from `feature_extractor.extract_all_features`.

    Returns:
        numpy.ndarray of shape (61,) dtype float32.

    Raises:
        KeyError: if any of the 61 FEATURE_COLUMNS_61 keys are absent
            from feat_dict.
    """
    missing = [k for k in FEATURE_COLUMNS_61 if k not in feat_dict]
    if missing:
        raise KeyError(
            f"feat_dict missing {len(missing)} of {N_FEATURES_61} keys: "
            f"{missing[:5]}... Run feature_extractor.extract_all_features() "
            f"before calling features_from_dict_61()."
        )
    return np.array(
        [float(feat_dict[k]) for k in FEATURE_COLUMNS_61],
        dtype=np.float32,
    )
