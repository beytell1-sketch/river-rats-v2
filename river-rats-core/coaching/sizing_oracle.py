"""
Sizing Oracle â€" raise sizing and bet sizing predictions.

Separate from the action oracle (gto_model.py). Predicts the appropriate
sizing bucket for BET and RAISE actions using the same 37 features.

Raise sizing: XGBoost 3-class classifier â†' SMALL / STANDARD / LARGE
Bet sizing:   Heuristic rule â†' SMALL / STANDARD (89% of bets are STANDARD)

Usage:
    oracle = SizingOracle("/path/to/raise_sizing_model.json")
    result = oracle.predict(feature_array, action="RAISE")
    result.bucket       # "LARGE"
    result.pot_ratio    # 1.50
    result.confidence   # 0.94

    result = oracle.predict(feature_array, action="BET")
    result.bucket       # "STANDARD"
    result.pot_ratio    # 0.75

    result = oracle.predict(feature_array, action="FOLD")
    # â†' None

Contract with teaching layer:
    size_bucket: Optional[str]   # None for FOLD/CHECK/CALL
                                  # "SMALL" / "STANDARD" / "LARGE" for RAISE
                                  # "SMALL" / "STANDARD" for BET

Performance:
    Model load: ~50ms (one-time)
    Prediction: <1ms per hand
    Memory: ~2MB for model
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Optional


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CONSTANTS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

# Raise bucket definitions
RAISE_BUCKETS = ("SMALL", "STANDARD", "LARGE")
RAISE_BUCKET_TO_INT = {b: i for i, b in enumerate(RAISE_BUCKETS)}
INT_TO_RAISE_BUCKET = {i: b for i, b in enumerate(RAISE_BUCKETS)}
N_RAISE_CLASSES = len(RAISE_BUCKETS)

# Raise bucket boundaries (pot-ratio thresholds)
#   SMALL:    pot_ratio < 1.00   (~2x-2.2x raise, ~31% of GTO raises)
#   STANDARD: 1.00 â‰¤ ratio < 1.40 (~2.5x raise, ~47% of GTO raises)
#   LARGE:    ratio â‰¥ 1.40       (3x+ raise, pot-sized or bigger)
RAISE_SMALL_UPPER = 1.00
RAISE_STANDARD_UPPER = 1.40

# Bet bucket definitions
BET_BUCKETS = ("SMALL", "STANDARD")

# Bet bucket boundaries (pot-ratio thresholds)
#   SMALL:    pot_ratio < 0.60  (~11% of GTO bets â€" flop probes, small pots)
#   STANDARD: ratio â‰¥ 0.60     (~89% â€" the default, ~75% pot)
BET_SMALL_UPPER = 0.60

# Pot-ratio midpoints per bucket (for teaching layer display)
RAISE_BUCKET_MIDPOINTS = {
    "SMALL":    0.80,   # ~2.2x raise
    "STANDARD": 1.20,   # ~2.5x raise
    "LARGE":    1.50,   # ~3x raise
}

BET_BUCKET_MIDPOINTS = {
    "SMALL":    0.40,   # ~40% pot
    "STANDARD": 0.75,   # ~75% pot
}

# Actions that have sizing
SIZED_ACTIONS = frozenset({"BET", "RAISE"})

# Feature columns (identical to gto_model.py â€" same 45 features)
FEATURE_COLUMNS = (
    "street", "facing_bet", "pot_size", "to_call", "pot_odds", "bet_to_pot",
    "hero_position", "villain_position", "is_ip",
    "hand_category", "hand_rank", "is_made_hand", "is_strong_made",
    "is_monster", "has_flush_draw", "has_straight_draw", "draw_outs",
    "is_monotone", "is_two_tone", "is_rainbow", "is_paired",
    "is_double_paired", "connectivity_score", "high_card_rank",
    "danger_score", "flush_danger", "straight_danger",
    "raw_equity", "equity_vs_range",
    "better_hand_pct", "worse_hand_pct",
    "equity_margin", "spr",
    "is_3bet_pot", "villain_aggression_count",
    "villain_checked_back", "villain_call_count",
    "num_opponents",
    # v9 features (38→45): range composition + current-street action
    "villain_top_pair_plus_pct", "villain_draw_pct", "villain_air_pct",
    "villain_range_capped", "board_favour",
    "num_callers_to_bet", "facing_raise",
)

N_FEATURES = len(FEATURE_COLUMNS)  # 45

# Feature indices (for heuristic access without dict lookup)
_STREET_IDX = 0
_SPR_IDX = 32


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# PREDICTION RESULT
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

@dataclass(frozen=True)
class SizingPrediction:
    """
    Result of a sizing prediction.

    Attributes:
        bucket:     "SMALL", "STANDARD", or "LARGE" (raise) / "SMALL" or "STANDARD" (bet)
        pot_ratio:  Midpoint of bucket as pot fraction (e.g. 0.75 for STANDARD bet)
        confidence: Model probability for chosen bucket (1.0 for heuristic bets)
        method:     "model" for raise sizing, "heuristic" for bet sizing
    """
    bucket: str
    pot_ratio: float
    confidence: float
    method: str


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SIZING ORACLE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class SizingOracle:
    """
    Sizing prediction for BET and RAISE actions.

    - RAISE: XGBoost 3-class model (SMALL / STANDARD / LARGE)
    - BET:   Heuristic rule (SMALL / STANDARD)
    - FOLD/CHECK/CALL: Returns None

    Completely separate from GtoOracle â€" no shared state, no coupling.
    Thread-safe for read-only prediction after initialization.
    """

    def __init__(self, raise_model_path: str):
        """
        Load the raise sizing model from disk.

        Args:
            raise_model_path: Path to the exported XGBoost model JSON file.

        Raises:
            FileNotFoundError: If model file doesn't exist.
            ValueError: If model has wrong number of classes.
        """
        import xgboost as xgb
        self._raise_model = xgb.XGBClassifier()
        self._raise_model.load_model(raise_model_path)

        # Auto-detect feature width for backwards compatibility (v8=38, v9=45)
        self._n_features = getattr(
            self._raise_model, 'n_features_in_', len(FEATURE_COLUMNS)
        )

        if self._raise_model.n_classes_ != N_RAISE_CLASSES:
            raise ValueError(
                f"Raise model has {self._raise_model.n_classes_} classes, "
                f"expected {N_RAISE_CLASSES}"
            )

    def predict(
        self,
        features: np.ndarray,
        action: str,
    ) -> Optional[SizingPrediction]:
        """
        Predict sizing bucket for a given action.

        Args:
            features: numpy array of shape (37,) or (1, 37).
                      Same features as GtoOracle.predict().
            action:   Action string: "FOLD", "CHECK", "CALL", "BET", "RAISE"

        Returns:
            SizingPrediction for BET/RAISE actions.
            None for FOLD/CHECK/CALL.
        """
        action_upper = action.upper()

        if action_upper not in SIZED_ACTIONS:
            return None

        if action_upper == "RAISE":
            return self._predict_raise(features)
        else:
            return self._predict_bet(features)

    def predict_from_dict(
        self,
        feat_dict: Dict[str, float],
        action: str,
    ) -> Optional[SizingPrediction]:
        """
        Predict sizing from a feature dict (convenience wrapper).

        Args:
            feat_dict: {feature_name: value} dict with all 37 features.
            action:    Action string.

        Returns:
            SizingPrediction or None.
        """
        features = self.features_from_dict(feat_dict)
        return self.predict(features, action)

    def _predict_raise(self, features: np.ndarray) -> SizingPrediction:
        """XGBoost model prediction for raise sizing."""
        if features.ndim == 1:
            features = features[:self._n_features]
        else:
            features = features[:, :self._n_features]
        X = self._ensure_2d(features)
        probs = self._raise_model.predict_proba(X)[0]
        bucket_idx = int(np.argmax(probs))
        bucket = INT_TO_RAISE_BUCKET[bucket_idx]
        confidence = float(probs[bucket_idx])

        return SizingPrediction(
            bucket=bucket,
            pot_ratio=RAISE_BUCKET_MIDPOINTS[bucket],
            confidence=confidence,
            method="model",
        )

    def _predict_bet(self, features: np.ndarray) -> SizingPrediction:
        """
        Heuristic prediction for bet sizing.

        Rule: Flop bets with deep stacks (SPR > 5) â†' SMALL, else STANDARD.
        Based on data analysis: 89% of GTO bets are 50-90% pot (STANDARD),
        the remaining 11% are flop probes at lower sizing.
        """
        flat = features.ravel()
        street = float(flat[_STREET_IDX])
        spr = float(flat[_SPR_IDX])

        # street == 0.0 means flop in our encoding
        if street == 0.0 and spr > 5.0:
            bucket = "SMALL"
        else:
            bucket = "STANDARD"

        return SizingPrediction(
            bucket=bucket,
            pot_ratio=BET_BUCKET_MIDPOINTS[bucket],
            confidence=1.0,  # Heuristic â€" no probability distribution
            method="heuristic",
        )

    @property
    def raise_model(self):
        """Expose underlying XGBClassifier (read-only, for inspection/testing)."""
        return self._raise_model

    @staticmethod
    def features_from_dict(feat_dict: Dict[str, float]) -> np.ndarray:
        """Convert a feature dict to a numpy array in correct column order."""
        return np.array(
            [feat_dict.get(f, 0.0) for f in FEATURE_COLUMNS],
            dtype=np.float32,
        )

    @staticmethod
    def _ensure_2d(features: np.ndarray) -> np.ndarray:
        if features.ndim == 1:
            return features.reshape(1, -1)
        return features


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# BUCKET UTILITIES (used by training pipeline and tests)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def assign_raise_bucket(pot_ratio: float) -> str:
    """
    Classify a raise pot-ratio into a sizing bucket.

    Args:
        pot_ratio: raise_size / pot_size

    Returns:
        "SMALL", "STANDARD", or "LARGE"
    """
    if pot_ratio < RAISE_SMALL_UPPER:
        return "SMALL"
    elif pot_ratio < RAISE_STANDARD_UPPER:
        return "STANDARD"
    else:
        return "LARGE"


def assign_bet_bucket(pot_ratio: float) -> str:
    """
    Classify a bet pot-ratio into a sizing bucket.

    Args:
        pot_ratio: bet_size / pot_size

    Returns:
        "SMALL" or "STANDARD"
    """
    if pot_ratio < BET_SMALL_UPPER:
        return "SMALL"
    else:
        return "STANDARD"
