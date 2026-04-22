"""
GTO Oracle — inference wrapper for the XGBoost poker model.

Loads the exported model and provides a clean predict() interface.
Returns action name, confidence, and full probability distribution.

Usage:
    oracle = GtoOracle("/path/to/gto_model_v4_compact.json")
    result = oracle.predict(feature_array)   # numpy (37,)
    result.action      # "CHECK"
    result.confidence  # 0.72
    result.probs       # {"FOLD": 0.01, "CHECK": 0.72, ...}

Performance:
    Model load: ~50ms (one-time)
    Prediction: <1ms per hand
    Memory: ~2MB for model
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Optional


# ═══════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════

ACTION_CLASSES = ("FOLD", "CHECK", "CALL", "BET", "RAISE")
ACTION_TO_INT = {a: i for i, a in enumerate(ACTION_CLASSES)}
INT_TO_ACTION = {i: a for i, a in enumerate(ACTION_CLASSES)}

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
    # v9 features (45→48): blocker + outs + improvement
    "flush_block_pct", "overcard_outs", "improvement_probability",
    # v9 features (48→52): range percentile, showdown value, fold equity, flush draw rank
    "hero_range_percentile", "has_showdown_value",
    "villain_fold_equity_estimate", "flush_draw_rank",
    # v9 feature 53: preflop aggressor flag
    "is_preflop_aggressor",
    # feature 54: medium/weak made hand pct in villain range
    "villain_medium_made_pct",
    # feature 55: board-adjusted hero range percentile
    "board_adjusted_hrp",
)

N_FEATURES = len(FEATURE_COLUMNS)  # 55
N_CLASSES = len(ACTION_CLASSES)     # 5


# ═══════════════════════════════════════════════════════════════════
# PREDICTION RESULT
# ═══════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class OraclePrediction:
    """Result of a single oracle prediction."""
    action: str                    # "FOLD", "CHECK", "CALL", "BET", "RAISE"
    action_idx: int                # 0-4
    confidence: float              # probability of chosen action
    probs: Dict[str, float]        # {action_name: probability}
    prob_array: np.ndarray         # shape (5,) raw probabilities


# ═══════════════════════════════════════════════════════════════════
# ORACLE
# ═══════════════════════════════════════════════════════════════════

class GtoOracle:
    """
    GTO poker oracle backed by XGBoost multiclass classifier.

    Thread-safe for read-only prediction after initialization.
    """

    def __init__(self, model_path: str):
        """
        Load the XGBoost model from disk.

        Args:
            model_path: Path to the exported model JSON file.
        """
        import xgboost as xgb
        self._model = xgb.XGBClassifier()
        self._model.load_model(model_path)

        # Auto-detect feature width for backwards compatibility (v8=38, v9=45)
        self._n_features = getattr(
            self._model, 'n_features_in_', len(FEATURE_COLUMNS)
        )

        # All models are 5-class warm-start. 3-class code path is dead.
        assert self._model.n_classes_ == N_CLASSES, (
            f"Model has {self._model.n_classes_} classes, expected {N_CLASSES}"
        )
        self._action_map = INT_TO_ACTION
        self._action_names = ACTION_CLASSES

    def predict(self, features: np.ndarray) -> OraclePrediction:
        """
        Predict action for a single hand.

        Args:
            features: numpy array of shape (N,) or (1, N) where N matches model width.

        Returns:
            OraclePrediction with action, confidence, and probabilities.
        """
        # Slice to model's expected width (v8=38, v9=45)
        if features.ndim == 1:
            features = features[:self._n_features]
        else:
            features = features[:, :self._n_features]
        X = self._ensure_2d(features)
        probs = self._model.predict_proba(X)[0]
        action_idx = int(np.argmax(probs))
        action = self._action_map[action_idx]
        confidence = float(probs[action_idx])

        return OraclePrediction(
            action=action,
            action_idx=action_idx,
            confidence=confidence,
            probs={a: float(probs[i]) for i, a in enumerate(self._action_names)},
            prob_array=probs,
        )

    def predict_batch(self, features: np.ndarray):
        """
        Predict actions for multiple hands.

        Args:
            features: numpy array of shape (n_hands, N) where N >= model width.

        Returns:
            List of OraclePrediction.
        """
        X = features if features.ndim == 2 else features.reshape(1, -1)
        X = X[:, :self._n_features]
        all_probs = self._model.predict_proba(X)
        results = []
        for i in range(X.shape[0]):
            probs = all_probs[i]
            action_idx = int(np.argmax(probs))
            results.append(OraclePrediction(
                action=self._action_map[action_idx],
                action_idx=action_idx,
                confidence=float(probs[action_idx]),
                probs={a: float(probs[j]) for j, a in enumerate(self._action_names)},
                prob_array=probs,
            ))
        return results

    @property
    def model(self):
        """Expose the underlying XGBClassifier (read-only, for SHAP explainer)."""
        return self._model

    @staticmethod
    def features_from_dict(feat_dict: Dict[str, float]) -> np.ndarray:
        """Convert a feature dict to a numpy array in correct column order.

        Raises KeyError if any of the 54 FEATURE_COLUMNS are absent from
        feat_dict.  Never silently defaults to 0.0 — a missing key means
        the upstream pipeline is broken and must be fixed before scoring.

        Context: HRP_INVESTIGATION_2026-04-15.md — the old feat_dict.get(f, 0.0)
        silently zeroed 6 missing MW test-set features, producing bogus
        hero_range_percentile = 0.00 across all MW misses.
        """
        missing = [f for f in FEATURE_COLUMNS if f not in feat_dict]
        if missing:
            raise KeyError(
                f"feat_dict is missing {len(missing)} required feature(s): {missing}. "
                f"Run extract_all_features() to populate all {len(FEATURE_COLUMNS)} "
                f"FEATURE_COLUMNS before calling features_from_dict()."
            )
        # Dtype guard: catch string/None/other-non-numeric values before
        # np.array() either raises a cryptic cast error or silently coerces.
        # Context: MAIN_TERMINAL_UPDATE_2026-04-15-c.md §1. BP generators were
        # emitting `street='flop'` instead of a numeric code; the guard
        # ensures these are caught at the harness boundary.
        bad = []
        for f in FEATURE_COLUMNS:
            v = feat_dict[f]
            # bool is a subclass of int — explicitly allowed.
            if isinstance(v, bool):
                continue
            if not isinstance(v, (int, float)):
                bad.append((f, type(v).__name__, repr(v)))
        if bad:
            details = ', '.join(f"{name}={val!s} (type {ty})" for name, ty, val in bad)
            raise TypeError(
                f"feat_dict has {len(bad)} non-numeric value(s): {details}. "
                f"All FEATURE_COLUMNS must be numeric (int/float/bool). "
                f"Re-extract via extract_all_features() — do not pass raw "
                f"serialisation dicts with string codes like street='flop'."
            )

        # MUST #10 sub-4 — NaN allowlist. Villain-range-derived features
        # may be NaN when villain folded OR chain over-narrowed/truncated
        # (HIGH #4 + MUST #15 + MUST #28 sentinels). These feed XGBoost's
        # default-direction branch at inference. All OTHER columns must
        # be finite — unexpected NaN in raw_equity / pot_odds / etc.
        # indicates upstream pipeline breakage; raise.
        import math
        _NAN_ALLOWLIST = {
            # Composition features (villain-range-derived)
            'villain_top_pair_plus_pct', 'villain_draw_pct',
            'villain_air_pct', 'villain_medium_made_pct',
            # Blocker features (villain-range-derived; continuous only)
            'flush_block_pct', 'flush_draw_block_pct',
            'straight_draw_block_pct', 'nut_made_block_pct',
        }
        unexpected_nan = [
            f for f in FEATURE_COLUMNS
            if f not in _NAN_ALLOWLIST
            and isinstance(feat_dict[f], float)
            and math.isnan(feat_dict[f])
        ]
        if unexpected_nan:
            raise ValueError(
                f"MUST #10: unexpected NaN in non-allowlist feature(s): "
                f"{unexpected_nan}. NaN is only permitted on villain-range-"
                f"derived composition + blocker features (when villain "
                f"folded or chain over-narrowed). NaN elsewhere indicates "
                f"upstream pipeline breakage — investigate."
            )

        return np.array(
            [feat_dict[f] for f in FEATURE_COLUMNS],
            dtype=np.float32,
        )

    @staticmethod
    def _ensure_2d(features: np.ndarray) -> np.ndarray:
        if features.ndim == 1:
            return features.reshape(1, -1)
        return features
