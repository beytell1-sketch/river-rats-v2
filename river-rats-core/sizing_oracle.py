"""
Sizing Oracle — raise sizing and bet sizing predictions.

Separate from the action oracle (gto_model.py). Predicts the appropriate
sizing bucket for BET and RAISE actions using the same feature set.

Sizes are aligned to GTO Wizard solver options so that training data,
test sets, and solver verification all use the same sizing language.

Bet sizing:   Street-dependent heuristic → SMALL / LARGE
  Flop:  SMALL = 25% pot,  LARGE = 66% pot
  Turn:  SMALL = 33% pot,  LARGE = 75% pot
  River: SMALL = 33% pot,  LARGE = 75% pot

Raise sizing: 2-class (SMALL / LARGE), uniform across streets
  SMALL = 33% pot,  LARGE = 66% pot

Usage:
    oracle = SizingOracle("/path/to/raise_sizing_model.json")
    result = oracle.predict(feature_array, action="RAISE")
    result.bucket       # "LARGE"
    result.pot_ratio    # 0.66
    result.confidence   # 0.94

    result = oracle.predict(feature_array, action="BET")
    result.bucket       # "SMALL"
    result.pot_ratio    # 0.25  (flop) or 0.33 (turn/river)

    result = oracle.predict(feature_array, action="FOLD")
    # → None

Contract with teaching layer:
    size_bucket: Optional[str]   # None for FOLD/CHECK/CALL
                                  # "SMALL" / "LARGE" for RAISE
                                  # "SMALL" / "LARGE" for BET

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

# Raise bucket definitions (2-class, solver-aligned)
RAISE_BUCKETS = ("SMALL", "LARGE")
RAISE_BUCKET_TO_INT = {b: i for i, b in enumerate(RAISE_BUCKETS)}
INT_TO_RAISE_BUCKET = {i: b for i, b in enumerate(RAISE_BUCKETS)}
N_RAISE_CLASSES = len(RAISE_BUCKETS)

# Raise bucket boundary (pot-ratio threshold)
#   SMALL: pot_ratio < 0.50  (33% pot raise)
#   LARGE: pot_ratio >= 0.50 (66% pot raise)
RAISE_SMALL_UPPER = 0.50

# Bet bucket definitions (2-class, solver-aligned)
BET_BUCKETS = ("SMALL", "LARGE")

# Bet bucket boundary (pot-ratio threshold)
#   SMALL: pot_ratio < 0.45  (25% flop / 33% turn+river)
#   LARGE: pot_ratio >= 0.45 (66% flop / 75% turn+river)
BET_SMALL_UPPER = 0.45

# Raise midpoints — uniform across all streets (solver: 33% and 66%)
RAISE_BUCKET_MIDPOINTS = {
    "SMALL": 0.33,
    "LARGE": 0.66,
}

# Bet midpoints — street-dependent (solver options differ by street)
# Flop: 25% / 66%  |  Turn: 33% / 75%  |  River: 33% / 75%
BET_BUCKET_MIDPOINTS_BY_STREET = {
    0: {"SMALL": 0.25, "LARGE": 0.66},   # flop
    1: {"SMALL": 0.33, "LARGE": 0.75},   # turn
    2: {"SMALL": 0.33, "LARGE": 0.75},   # river
}

# Fallback for callers that don't pass street (uses turn/river values)
BET_BUCKET_MIDPOINTS = {"SMALL": 0.33, "LARGE": 0.75}

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
    # v9 features (45->48): blocker + outs + improvement
    "flush_block_pct", "overcard_outs", "improvement_probability",
)

N_FEATURES = len(FEATURE_COLUMNS)  # 48

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

    - RAISE: XGBoost 2-class model (SMALL / LARGE) or legacy 3-class
    - BET:   Heuristic rule (SMALL / LARGE), street-dependent midpoints
    - FOLD/CHECK/CALL: Returns None

    Completely separate from GtoOracle — no shared state, no coupling.
    Thread-safe for read-only prediction after initialization.
    """

    def __init__(self, raise_model_path: str):
        """
        Load the raise sizing model from disk.

        Args:
            raise_model_path: Path to the exported XGBoost model JSON file.

        Raises:
            FileNotFoundError: If model file doesn't exist.
        """
        import xgboost as xgb
        self._raise_model = xgb.XGBClassifier()
        self._raise_model.load_model(raise_model_path)

        self._n_features = getattr(
            self._raise_model, 'n_features_in_', len(FEATURE_COLUMNS)
        )

        # Support both legacy 3-class and new 2-class models
        self._legacy_3class = (self._raise_model.n_classes_ == 3)

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

        if self._legacy_3class:
            # Legacy 3-class model: map SMALL→SMALL, STANDARD→LARGE, LARGE→LARGE
            legacy_map = {0: "SMALL", 1: "LARGE", 2: "LARGE"}
            bucket = legacy_map[bucket_idx]
            confidence = float(probs[bucket_idx])
        else:
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

        Rule: Flop bets with deep stacks (SPR > 5) → SMALL, else LARGE.
        Street-dependent midpoints aligned to GTO Wizard solver options:
          Flop:  SMALL = 25% pot,  LARGE = 66% pot
          Turn:  SMALL = 33% pot,  LARGE = 75% pot
          River: SMALL = 33% pot,  LARGE = 75% pot
        """
        flat = features.ravel()
        street = int(float(flat[_STREET_IDX]))
        spr = float(flat[_SPR_IDX])

        if street == 0 and spr > 5.0:
            bucket = "SMALL"
        else:
            bucket = "LARGE"

        midpoints = BET_BUCKET_MIDPOINTS_BY_STREET.get(
            street, BET_BUCKET_MIDPOINTS
        )

        return SizingPrediction(
            bucket=bucket,
            pot_ratio=midpoints[bucket],
            confidence=1.0,
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
        "SMALL" or "LARGE"
    """
    if pot_ratio < RAISE_SMALL_UPPER:
        return "SMALL"
    else:
        return "LARGE"


def assign_bet_bucket(pot_ratio: float) -> str:
    """
    Classify a bet pot-ratio into a sizing bucket.

    Args:
        pot_ratio: bet_size / pot_size

    Returns:
        "SMALL" or "LARGE"
    """
    if pot_ratio < BET_SMALL_UPPER:
        return "SMALL"
    else:
        return "LARGE"
