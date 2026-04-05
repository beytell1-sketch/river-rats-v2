"""
Tests for sizing_oracle.py
============================

Coverage targets:
  - SizingOracle.predict() for all 5 actions (FOLD/CHECK/CALL/BET/RAISE)
  - Raise model predictions (3-class: SMALL/STANDARD/LARGE)
  - Bet heuristic logic (street + SPR thresholds)
  - Bucket assignment utilities (boundary conditions)
  - predict_from_dict() convenience wrapper
  - SizingPrediction dataclass contract
  - Edge cases: array shapes, extreme values, boundary pot-ratios

Run:
    cd /home/claude && python3 -m pytest test_sizing_oracle.py -v
"""

import sys
import os
import numpy as np
import pytest

sys.path.insert(0, '/home/rupertbeytell/river-rats/river-rats-complete')

from sizing_oracle import (
    SizingOracle,
    SizingPrediction,
    assign_raise_bucket,
    assign_bet_bucket,
    RAISE_BUCKETS,
    RAISE_SMALL_UPPER,
    RAISE_STANDARD_UPPER,
    BET_SMALL_UPPER,
    RAISE_BUCKET_MIDPOINTS,
    BET_BUCKET_MIDPOINTS,
    FEATURE_COLUMNS,
    N_FEATURES,
    N_RAISE_CLASSES,
    SIZED_ACTIONS,
    INT_TO_RAISE_BUCKET,
)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# FIXTURES
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

MODEL_PATH = '/home/rupertbeytell/river-rats/river-rats-complete/raise_sizing_model_v3_38feat.json'


@pytest.fixture(scope="module")
def oracle():
    """Shared SizingOracle instance (model load is expensive)."""
    if not os.path.exists(MODEL_PATH):
        pytest.skip(f"Model not found: {MODEL_PATH}")
    return SizingOracle(MODEL_PATH)


def _make_features(**overrides) -> np.ndarray:
    """
    Build a 38-feature array with sensible defaults and optional overrides.

    Defaults represent a typical turn hand facing a bet from BB vs CO.
    """
    defaults = {
        'street': 1.0,            # turn
        'facing_bet': 1.0,
        'pot_size': 30.0,
        'to_call': 10.0,
        'pot_odds': 0.25,
        'bet_to_pot': 0.33,
        'hero_position': 4.0,     # CO
        'villain_position': 1.0,  # BB
        'is_ip': 1.0,
        'hand_category': 6.0,     # top pair
        'hand_rank': 0.65,
        'is_made_hand': 1.0,
        'is_strong_made': 0.0,
        'is_monster': 0.0,
        'has_flush_draw': 0.0,
        'has_straight_draw': 0.0,
        'draw_outs': 0.0,
        'is_monotone': 0.0,
        'is_two_tone': 1.0,
        'is_rainbow': 0.0,
        'is_paired': 0.0,
        'is_double_paired': 0.0,
        'connectivity_score': 0.3,
        'high_card_rank': 12.0,
        'danger_score': 0.4,
        'flush_danger': 0.3,
        'straight_danger': 0.2,
        'raw_equity': 0.55,
        'equity_vs_range': 0.55,
        'better_hand_pct': 0.3,
        'worse_hand_pct': 0.6,
        'equity_margin': 0.30,
        'spr': 3.33,
        'is_3bet_pot': 0.0,
        'villain_aggression_count': 0.0,
        'villain_checked_back': 0.0,
        'villain_call_count': 0.0,
        'num_opponents': 1.0,
    }
    defaults.update(overrides)
    return np.array(
        [defaults[col] for col in FEATURE_COLUMNS],
        dtype=np.float32,
    )


def _make_feature_dict(**overrides) -> dict:
    """Build a feature dict with sensible defaults."""
    defaults = {
        'street': 1.0, 'facing_bet': 1.0, 'pot_size': 30.0,
        'to_call': 10.0, 'pot_odds': 0.25, 'bet_to_pot': 0.33,
        'hero_position': 4.0, 'villain_position': 1.0, 'is_ip': 1.0,
        'hand_category': 6.0, 'hand_rank': 0.65, 'is_made_hand': 1.0,
        'is_strong_made': 0.0, 'is_monster': 0.0,
        'has_flush_draw': 0.0, 'has_straight_draw': 0.0, 'draw_outs': 0.0,
        'is_monotone': 0.0, 'is_two_tone': 1.0, 'is_rainbow': 0.0,
        'is_paired': 0.0, 'is_double_paired': 0.0,
        'connectivity_score': 0.3, 'high_card_rank': 12.0,
        'danger_score': 0.4, 'flush_danger': 0.3, 'straight_danger': 0.2,
        'raw_equity': 0.55, 'equity_vs_range': 0.55,
        'better_hand_pct': 0.3, 'worse_hand_pct': 0.6,
        'equity_margin': 0.30, 'spr': 3.33,
        'is_3bet_pot': 0.0, 'villain_aggression_count': 0.0,
        'villain_checked_back': 0.0, 'villain_call_count': 0.0,
        'num_opponents': 1.0,
    }
    defaults.update(overrides)
    return defaults


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CONSTANTS TESTS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class TestConstants:
    """Verify sizing constants are self-consistent."""

    def test_raise_buckets_count(self):
        assert len(RAISE_BUCKETS) == 3

    def test_raise_buckets_names(self):
        assert RAISE_BUCKETS == ("SMALL", "STANDARD", "LARGE")

    def test_n_raise_classes(self):
        assert N_RAISE_CLASSES == 3

    def test_feature_count(self):
        assert N_FEATURES == 38

    def test_feature_columns_match_gto_model(self):
        """Feature columns must be identical to gto_model.py."""
        from coaching.gto_model import FEATURE_COLUMNS as GTO_FEATURES
        assert tuple(FEATURE_COLUMNS) == tuple(GTO_FEATURES)

    def test_raise_thresholds_ordered(self):
        assert 0 < RAISE_SMALL_UPPER < RAISE_STANDARD_UPPER

    def test_bet_threshold_positive(self):
        assert 0 < BET_SMALL_UPPER < 1.0

    def test_raise_midpoints_within_buckets(self):
        assert RAISE_BUCKET_MIDPOINTS["SMALL"] < RAISE_SMALL_UPPER
        assert RAISE_SMALL_UPPER <= RAISE_BUCKET_MIDPOINTS["STANDARD"] < RAISE_STANDARD_UPPER
        assert RAISE_BUCKET_MIDPOINTS["LARGE"] >= RAISE_STANDARD_UPPER

    def test_bet_midpoints_within_buckets(self):
        assert BET_BUCKET_MIDPOINTS["SMALL"] < BET_SMALL_UPPER
        assert BET_BUCKET_MIDPOINTS["STANDARD"] >= BET_SMALL_UPPER

    def test_sized_actions(self):
        assert SIZED_ACTIONS == {"BET", "RAISE"}

    def test_int_to_raise_bucket_complete(self):
        for i in range(N_RAISE_CLASSES):
            assert i in INT_TO_RAISE_BUCKET


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# BUCKET ASSIGNMENT TESTS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class TestAssignRaiseBucket:
    """Test raise bucket boundary conditions."""

    def test_small_well_below(self):
        assert assign_raise_bucket(0.50) == "SMALL"

    def test_small_just_below(self):
        assert assign_raise_bucket(0.99) == "SMALL"

    def test_standard_at_boundary(self):
        """pot_ratio == 1.00 is STANDARD (>= lower, < upper)."""
        assert assign_raise_bucket(1.00) == "STANDARD"

    def test_standard_mid(self):
        assert assign_raise_bucket(1.20) == "STANDARD"

    def test_standard_just_below_upper(self):
        assert assign_raise_bucket(1.39) == "STANDARD"

    def test_large_at_boundary(self):
        """pot_ratio == 1.40 is LARGE (>= threshold)."""
        assert assign_raise_bucket(1.40) == "LARGE"

    def test_large_above(self):
        assert assign_raise_bucket(2.00) == "LARGE"

    def test_large_extreme(self):
        assert assign_raise_bucket(5.00) == "LARGE"

    def test_small_zero(self):
        assert assign_raise_bucket(0.0) == "SMALL"

    def test_small_negative(self):
        """Negative ratios (shouldn't occur) still map to SMALL."""
        assert assign_raise_bucket(-0.5) == "SMALL"


class TestAssignBetBucket:
    """Test bet bucket boundary conditions."""

    def test_small_well_below(self):
        assert assign_bet_bucket(0.30) == "SMALL"

    def test_small_just_below(self):
        assert assign_bet_bucket(0.59) == "SMALL"

    def test_standard_at_boundary(self):
        """pot_ratio == 0.60 is STANDARD."""
        assert assign_bet_bucket(0.60) == "STANDARD"

    def test_standard_typical(self):
        assert assign_bet_bucket(0.75) == "STANDARD"

    def test_standard_overbet(self):
        assert assign_bet_bucket(1.50) == "STANDARD"

    def test_small_zero(self):
        assert assign_bet_bucket(0.0) == "SMALL"


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# PREDICTION RESULT CONTRACT TESTS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class TestSizingPrediction:
    """Verify the SizingPrediction dataclass contract."""

    def test_is_frozen(self):
        pred = SizingPrediction(
            bucket="LARGE", pot_ratio=1.50,
            confidence=0.95, method="model",
        )
        with pytest.raises(AttributeError):
            pred.bucket = "SMALL"

    def test_fields_present(self):
        pred = SizingPrediction(
            bucket="SMALL", pot_ratio=0.80,
            confidence=0.88, method="model",
        )
        assert pred.bucket == "SMALL"
        assert pred.pot_ratio == 0.80
        assert pred.confidence == 0.88
        assert pred.method == "model"

    def test_heuristic_method(self):
        pred = SizingPrediction(
            bucket="STANDARD", pot_ratio=0.75,
            confidence=1.0, method="heuristic",
        )
        assert pred.method == "heuristic"
        assert pred.confidence == 1.0


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# ORACLE PREDICTION TESTS â€” NON-SIZED ACTIONS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class TestNonSizedActions:
    """predict() returns None for FOLD/CHECK/CALL."""

    def test_fold_returns_none(self, oracle):
        result = oracle.predict(_make_features(), "FOLD")
        assert result is None

    def test_check_returns_none(self, oracle):
        result = oracle.predict(_make_features(), "CHECK")
        assert result is None

    def test_call_returns_none(self, oracle):
        result = oracle.predict(_make_features(), "CALL")
        assert result is None

    def test_fold_lowercase(self, oracle):
        result = oracle.predict(_make_features(), "fold")
        assert result is None

    def test_call_mixed_case(self, oracle):
        result = oracle.predict(_make_features(), "Call")
        assert result is None


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# ORACLE PREDICTION TESTS â€” RAISE (MODEL)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class TestRaisePrediction:
    """Raise sizing predictions via XGBoost model."""

    def test_returns_sizing_prediction(self, oracle):
        result = oracle.predict(_make_features(), "RAISE")
        assert isinstance(result, SizingPrediction)

    def test_bucket_is_valid(self, oracle):
        result = oracle.predict(_make_features(), "RAISE")
        assert result.bucket in RAISE_BUCKETS

    def test_method_is_model(self, oracle):
        result = oracle.predict(_make_features(), "RAISE")
        assert result.method == "model"

    def test_confidence_in_range(self, oracle):
        result = oracle.predict(_make_features(), "RAISE")
        assert 0.0 < result.confidence <= 1.0

    def test_pot_ratio_matches_bucket(self, oracle):
        result = oracle.predict(_make_features(), "RAISE")
        assert result.pot_ratio == RAISE_BUCKET_MIDPOINTS[result.bucket]

    def test_lowercase_action(self, oracle):
        result = oracle.predict(_make_features(), "raise")
        assert isinstance(result, SizingPrediction)
        assert result.method == "model"

    def test_1d_array_shape(self, oracle):
        """Accepts (38,) shape."""
        features = _make_features()
        assert features.shape == (38,)
        result = oracle.predict(features, "RAISE")
        assert result is not None

    def test_2d_array_shape(self, oracle):
        """Accepts (1, 38) shape."""
        features = _make_features().reshape(1, -1)
        assert features.shape == (1, 38)
        result = oracle.predict(features, "RAISE")
        assert result is not None

    def test_different_scenarios_can_differ(self, oracle):
        """Different feature inputs can produce different buckets."""
        # Small pot, deep stacks â†’ might differ from large pot, shallow
        f1 = _make_features(pot_size=6.0, spr=16.67, facing_bet=0.0,
                            to_call=0.0, pot_odds=0.0, bet_to_pot=0.0)
        f2 = _make_features(pot_size=150.0, spr=0.67, facing_bet=1.0,
                            to_call=50.0, pot_odds=0.25, bet_to_pot=0.33)
        r1 = oracle.predict(f1, "RAISE")
        r2 = oracle.predict(f2, "RAISE")
        # We can't guarantee they differ, but both must be valid
        assert r1.bucket in RAISE_BUCKETS
        assert r2.bucket in RAISE_BUCKETS


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# ORACLE PREDICTION TESTS â€” BET (HEURISTIC)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class TestBetPrediction:
    """Bet sizing predictions via heuristic rule."""

    def test_returns_sizing_prediction(self, oracle):
        result = oracle.predict(_make_features(), "BET")
        assert isinstance(result, SizingPrediction)

    def test_method_is_heuristic(self, oracle):
        result = oracle.predict(_make_features(), "BET")
        assert result.method == "heuristic"

    def test_confidence_is_one(self, oracle):
        """Heuristic has no probability â€” always 1.0."""
        result = oracle.predict(_make_features(), "BET")
        assert result.confidence == 1.0

    def test_bucket_is_valid(self, oracle):
        result = oracle.predict(_make_features(), "BET")
        assert result.bucket in ("SMALL", "STANDARD")

    def test_pot_ratio_matches_bucket(self, oracle):
        result = oracle.predict(_make_features(), "BET")
        assert result.pot_ratio == BET_BUCKET_MIDPOINTS[result.bucket]

    def test_flop_deep_is_small(self, oracle):
        """Flop (street=0) + deep stacks (SPR > 5) â†’ SMALL bet."""
        features = _make_features(street=0.0, spr=10.0)
        result = oracle.predict(features, "BET")
        assert result.bucket == "SMALL"

    def test_flop_shallow_is_standard(self, oracle):
        """Flop but shallow (SPR â‰¤ 5) â†’ STANDARD."""
        features = _make_features(street=0.0, spr=3.0)
        result = oracle.predict(features, "BET")
        assert result.bucket == "STANDARD"

    def test_flop_spr_exactly_5_is_standard(self, oracle):
        """SPR == 5.0 is NOT > 5.0, so â†’ STANDARD."""
        features = _make_features(street=0.0, spr=5.0)
        result = oracle.predict(features, "BET")
        assert result.bucket == "STANDARD"

    def test_turn_deep_is_standard(self, oracle):
        """Turn (street=1) â†’ STANDARD regardless of SPR."""
        features = _make_features(street=1.0, spr=15.0)
        result = oracle.predict(features, "BET")
        assert result.bucket == "STANDARD"

    def test_river_deep_is_standard(self, oracle):
        """River (street=2) â†’ STANDARD."""
        features = _make_features(street=2.0, spr=20.0)
        result = oracle.predict(features, "BET")
        assert result.bucket == "STANDARD"

    def test_lowercase_action(self, oracle):
        result = oracle.predict(_make_features(), "bet")
        assert isinstance(result, SizingPrediction)
        assert result.method == "heuristic"


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CONVENIENCE WRAPPER TESTS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class TestPredictFromDict:
    """Test predict_from_dict() convenience method."""

    def test_raise_from_dict(self, oracle):
        feat_dict = _make_feature_dict()
        result = oracle.predict_from_dict(feat_dict, "RAISE")
        assert isinstance(result, SizingPrediction)
        assert result.method == "model"

    def test_bet_from_dict(self, oracle):
        feat_dict = _make_feature_dict(street=0.0, spr=12.0)
        result = oracle.predict_from_dict(feat_dict, "BET")
        assert result.bucket == "SMALL"

    def test_fold_from_dict(self, oracle):
        result = oracle.predict_from_dict(_make_feature_dict(), "FOLD")
        assert result is None

    def test_missing_features_default_zero(self, oracle):
        """Missing keys default to 0.0 via features_from_dict."""
        sparse_dict = {'pot_size': 30.0, 'spr': 3.0}
        result = oracle.predict_from_dict(sparse_dict, "RAISE")
        assert isinstance(result, SizingPrediction)


class TestFeaturesFromDict:
    """Test the static features_from_dict conversion."""

    def test_output_shape(self):
        feat_dict = _make_feature_dict()
        arr = SizingOracle.features_from_dict(feat_dict)
        assert arr.shape == (38,)

    def test_output_dtype(self):
        feat_dict = _make_feature_dict()
        arr = SizingOracle.features_from_dict(feat_dict)
        assert arr.dtype == np.float32

    def test_column_order(self):
        """Values must be in FEATURE_COLUMNS order."""
        feat_dict = _make_feature_dict(street=0.0, pot_size=42.0)
        arr = SizingOracle.features_from_dict(feat_dict)
        assert arr[0] == 0.0     # street is first column
        assert arr[2] == 42.0    # pot_size is third column


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# MODEL LOADING / VALIDATION TESTS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class TestModelLoading:
    """Test model loading and validation."""

    def test_model_loads(self, oracle):
        assert oracle.raise_model is not None

    def test_model_has_correct_classes(self, oracle):
        assert oracle.raise_model.n_classes_ == N_RAISE_CLASSES

    def test_invalid_path_raises(self):
        with pytest.raises(Exception):
            SizingOracle("/nonexistent/model.json")


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# EDGE CASE TESTS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class TestEdgeCases:
    """Edge cases and boundary conditions."""

    def test_zero_features(self, oracle):
        """All-zero features don't crash."""
        features = np.zeros(38, dtype=np.float32)
        result = oracle.predict(features, "RAISE")
        assert isinstance(result, SizingPrediction)

    def test_extreme_pot_size(self, oracle):
        """Very large pot doesn't crash."""
        features = _make_features(pot_size=10000.0, spr=0.01)
        result = oracle.predict(features, "RAISE")
        assert result.bucket in RAISE_BUCKETS

    def test_extreme_spr(self, oracle):
        """Very high SPR doesn't crash."""
        features = _make_features(pot_size=2.0, spr=50.0)
        result = oracle.predict(features, "RAISE")
        assert result.bucket in RAISE_BUCKETS

    def test_unknown_action_returns_none(self, oracle):
        """Non-standard action string returns None."""
        result = oracle.predict(_make_features(), "ALLIN")
        assert result is None

    def test_empty_string_action_returns_none(self, oracle):
        result = oracle.predict(_make_features(), "")
        assert result is None


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TEACHING LAYER CONTRACT TESTS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class TestTeachingContract:
    """
    Verify the contract the teaching layer depends on.

    The teaching layer expects:
      - size_bucket: Optional[str] â€” None for non-sized, string for sized
      - Raise bucket strings are exactly "SMALL", "STANDARD", or "LARGE"
      - Bet bucket strings are exactly "SMALL" or "STANDARD"
      - pot_ratio is always a float > 0
      - method is "model" or "heuristic"
    """

    def test_none_for_fold(self, oracle):
        assert oracle.predict(_make_features(), "FOLD") is None

    def test_none_for_check(self, oracle):
        assert oracle.predict(_make_features(), "CHECK") is None

    def test_none_for_call(self, oracle):
        assert oracle.predict(_make_features(), "CALL") is None

    def test_raise_bucket_is_string(self, oracle):
        result = oracle.predict(_make_features(), "RAISE")
        assert isinstance(result.bucket, str)

    def test_raise_bucket_in_expected_set(self, oracle):
        result = oracle.predict(_make_features(), "RAISE")
        assert result.bucket in {"SMALL", "STANDARD", "LARGE"}

    def test_bet_bucket_in_expected_set(self, oracle):
        result = oracle.predict(_make_features(), "BET")
        assert result.bucket in {"SMALL", "STANDARD"}

    def test_pot_ratio_is_positive_float(self, oracle):
        for action in ("BET", "RAISE"):
            result = oracle.predict(_make_features(), action)
            assert isinstance(result.pot_ratio, float)
            assert result.pot_ratio > 0

    def test_confidence_is_float(self, oracle):
        for action in ("BET", "RAISE"):
            result = oracle.predict(_make_features(), action)
            assert isinstance(result.confidence, float)

    def test_method_is_valid_string(self, oracle):
        bet = oracle.predict(_make_features(), "BET")
        rse = oracle.predict(_make_features(), "RAISE")
        assert bet.method in ("model", "heuristic")
        assert rse.method in ("model", "heuristic")

    def test_bet_always_heuristic(self, oracle):
        result = oracle.predict(_make_features(), "BET")
        assert result.method == "heuristic"

    def test_raise_always_model(self, oracle):
        result = oracle.predict(_make_features(), "RAISE")
        assert result.method == "model"
