"""
SHAP Explainer â€” wraps shap.TreeExplainer for the GTO Oracle.

Provides per-hand, per-class SHAP values that feed directly into
the Topic Resolver. This is the bridge between the oracle's
"what to do" and the teaching system's "why to do it."

Output shape from TreeExplainer for XGBoost multi:softprob:
    shap_values(X) â†’ ndarray of shape (n_samples, n_features, n_classes)

Values are in log-odds space (raw margin), NOT probability space.
This is fine for the teaching system â€” we only care about relative
magnitude and sign, not the absolute scale.

Usage:
    from coaching.gto_model import GtoOracle
    from coaching.shap_explainer import ShapExplainer

    oracle = GtoOracle("model.json")
    explainer = ShapExplainer(oracle)

    # For a single hand:
    result = explainer.explain(feature_array, predicted_action_idx)
    result.shap_dict          # {"equity_vs_range": 0.35, ...}
    result.shap_array         # ndarray (37,) for predicted class
    result.base_value         # base log-odds for predicted class
    result.top_features       # [("equity_vs_range", 0.35), ...]

    # Batch:
    results = explainer.explain_batch(X, pred_indices)

Performance:
    Explainer init: ~130ms (one-time, on first explain call)
    Per-hand:       ~0.6ms (batch), ~4ms (single)
    Memory:         Minimal â€” SHAP TreeExplainer stores tree paths, not data
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from coaching.gto_model import FEATURE_COLUMNS, N_FEATURES, N_CLASSES


# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
# SHAP RESULT
# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â

@dataclass(frozen=True)
class ShapResult:
    """SHAP explanation for one hand, one action class."""
    action_idx: int                     # which class these SHAP values explain
    shap_array: np.ndarray              # shape (37,) â€” raw SHAP for this class
    shap_dict: Dict[str, float]         # {feature_name: shap_value}
    base_value: float                   # base log-odds for this class
    all_class_shap: np.ndarray          # shape (37, 5) â€” SHAP for all classes

    @property
    def top_features(self) -> List[Tuple[str, float]]:
        """Features sorted by |SHAP| descending."""
        pairs = list(self.shap_dict.items())
        pairs.sort(key=lambda x: abs(x[1]), reverse=True)
        return pairs


# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
# EXPLAINER
# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â

class ShapExplainer:
    """
    SHAP TreeExplainer wrapper for the GTO Oracle.

    Lazily initializes the shap.TreeExplainer on first use to avoid
    the ~130ms cost if SHAP is never needed (e.g. replay mode).

    Thread-safety: TreeExplainer is read-only after init. Safe for
    concurrent explain() calls on different hands.
    """

    def __init__(self, oracle):
        """
        Args:
            oracle: GtoOracle instance (needs .model property).
        """
        self._oracle = oracle
        self._explainer = None      # lazy init
        self._base_values = None    # cached after init

    def _ensure_init(self):
        """Initialize TreeExplainer on first use."""
        if self._explainer is not None:
            return
        import shap
        self._explainer = shap.TreeExplainer(self._oracle.model)
        self._base_values = np.array(self._explainer.expected_value,
                                     dtype=np.float64)

    @property
    def base_values(self) -> np.ndarray:
        """Base log-odds values per class. Shape (5,)."""
        self._ensure_init()
        return self._base_values

    def explain(
        self,
        features: np.ndarray,
        action_idx: int,
    ) -> ShapResult:
        """
        Compute SHAP values for a single hand and action class.

        Args:
            features:   numpy array, shape (37,) or (1, 37)
            action_idx: which class to explain (0-4)

        Returns:
            ShapResult with SHAP values for the requested class.
        """
        self._ensure_init()

        X = features.reshape(1, -1) if features.ndim == 1 else features[:1]
        all_shap = self._explainer.shap_values(X)  # (1, 37, 5)
        sample_shap = all_shap[0]                    # (37, 5)
        class_shap = sample_shap[:, action_idx]      # (37,)

        return ShapResult(
            action_idx=action_idx,
            shap_array=class_shap,
            shap_dict={
                FEATURE_COLUMNS[i]: float(class_shap[i])
                for i in range(N_FEATURES)
            },
            base_value=float(self._base_values[action_idx]),
            all_class_shap=sample_shap,
        )

    def explain_predicted(
        self,
        features: np.ndarray,
    ) -> ShapResult:
        """
        Convenience: predict + explain in one call.

        Uses the oracle to predict, then explains the predicted class.
        """
        pred = self._oracle.predict(features)
        return self.explain(features, pred.action_idx)

    def explain_batch(
        self,
        features: np.ndarray,
        action_indices: np.ndarray,
    ) -> List[ShapResult]:
        """
        Compute SHAP for a batch of hands.

        Args:
            features:       shape (n_hands, 37)
            action_indices: shape (n_hands,) â€” which class per hand

        Returns:
            List of ShapResult, one per hand.
        """
        self._ensure_init()

        X = features if features.ndim == 2 else features.reshape(1, -1)
        n = X.shape[0]
        all_shap = self._explainer.shap_values(X)  # (n, 37, 5)

        results = []
        for i in range(n):
            aidx = int(action_indices[i])
            sample_shap = all_shap[i]              # (37, 5)
            class_shap = sample_shap[:, aidx]      # (37,)

            results.append(ShapResult(
                action_idx=aidx,
                shap_array=class_shap,
                shap_dict={
                    FEATURE_COLUMNS[j]: float(class_shap[j])
                    for j in range(N_FEATURES)
                },
                base_value=float(self._base_values[aidx]),
                all_class_shap=sample_shap,
            ))
        return results

    def raw_shap_values(self, features: np.ndarray) -> np.ndarray:
        """
        Raw SHAP for all classes. For advanced use / debugging.

        Args:
            features: shape (n, 37) or (37,)

        Returns:
            ndarray shape (n, 37, 5) or (1, 37, 5)
        """
        self._ensure_init()
        X = features.reshape(1, -1) if features.ndim == 1 else features
        return self._explainer.shap_values(X)
