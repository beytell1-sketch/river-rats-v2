"""Oracle Router — selects the correct specialist model by opponent count.

Progressive model chain: each opponent count gets a specialist XGBoost
model trained via warm-start from the previous level.

    v8 HU (38-feat)
      → v9-3way (45-feat)
      → v9-4way (45-feat)
      → v9-5way (45-feat)

The router loads all available models on init and dispatches predict()
to the correct one based on num_opponents. Falls back to the nearest
available model if a specialist doesn't exist yet.

Usage:
    from oracle_router import OracleRouter

    router = OracleRouter()  # auto-discovers models in models/ dir
    feat_dict = build_features_from_game_state(player, game, context)
    pred = router.predict(feat_dict, num_opponents=3)
"""
from __future__ import annotations
import os
from typing import Dict, Optional

from gto_model import GtoOracle, OraclePrediction, FEATURE_COLUMNS


# Default model directory
_MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')

# Model filename conventions
_MODEL_FILES = {
    1: 'gto_model_v8_hu.json',
    2: 'gto_model_v9_3way.json',
    3: 'gto_model_v9_4way.json',
    4: 'gto_model_v9_5way.json',  # 5-way handles 4+ opponents
}

# Legacy filename (before rename)
_LEGACY_HU = 'gto_model_v8_38feat.json'


class OracleRouter:
    """Routes predictions to the correct specialist model by opponent count.

    Auto-discovers available model files. Falls back to nearest available
    model when a specialist doesn't exist yet.
    """

    def __init__(self, models_dir: str = None):
        """Load all available specialist models.

        Args:
            models_dir: Directory containing model JSON files.
                        Defaults to river-rats-core/models/.
        """
        self._models_dir = models_dir or _MODELS_DIR
        self._oracles: Dict[int, GtoOracle] = {}
        self._fallback_order = [1, 2, 3, 4]  # try in order for fallback

        self._load_models()

    def _load_models(self):
        """Discover and load available model files.

        Skips model files that fail the 5-class assertion (e.g. legacy
        3-class artifacts on disk). Those slots fall back to the nearest
        available model at predict time.
        """
        for num_opp, filename in _MODEL_FILES.items():
            path = os.path.join(self._models_dir, filename)
            if os.path.exists(path):
                try:
                    self._oracles[num_opp] = GtoOracle(path)
                except AssertionError:
                    # File exists but is not a 5-class model — skip it.
                    # This handles legacy 3-class artifacts left on disk.
                    pass

        # Legacy fallback: if v8_hu doesn't exist but v8_38feat does
        if 1 not in self._oracles:
            legacy_path = os.path.join(self._models_dir, _LEGACY_HU)
            if os.path.exists(legacy_path):
                self._oracles[1] = GtoOracle(legacy_path)

        if not self._oracles:
            raise FileNotFoundError(
                f"No model files found in {self._models_dir}. "
                f"Expected: {list(_MODEL_FILES.values())}"
            )

    def _get_oracle(self, num_opponents: int) -> GtoOracle:
        """Get the best available oracle for this opponent count.

        Exact match first, then falls back to nearest lower count.
        5+ opponents use the 5-way model (key 4).
        """
        # Clamp: 5+ opponents → use 5-way slot
        key = min(num_opponents, 4)

        # Exact match
        if key in self._oracles:
            return self._oracles[key]

        # Fall back to nearest available (descending)
        for k in range(key - 1, 0, -1):
            if k in self._oracles:
                return self._oracles[k]

        # Last resort: any available model
        return next(iter(self._oracles.values()))

    def predict(self, feat_dict: dict, num_opponents: int) -> OraclePrediction:
        """Predict action using the correct specialist model.

        Args:
            feat_dict: Full feature dict from extract_all_features().
            num_opponents: Number of opponents at the decision point.

        Returns:
            OraclePrediction from the appropriate specialist.
        """
        oracle = self._get_oracle(num_opponents)
        features = GtoOracle.features_from_dict(feat_dict)
        return oracle.predict(features)

    @property
    def available_models(self) -> Dict[int, str]:
        """Return {num_opponents: model_info} for loaded models."""
        result = {}
        for num_opp, oracle in self._oracles.items():
            label = _MODEL_FILES.get(num_opp, 'unknown')
            n_feat = oracle._n_features
            result[num_opp] = f"{label} ({n_feat} features)"
        return result

    def has_specialist(self, num_opponents: int) -> bool:
        """Check if a specialist exists for this exact opponent count."""
        key = min(num_opponents, 4)
        return key in self._oracles
