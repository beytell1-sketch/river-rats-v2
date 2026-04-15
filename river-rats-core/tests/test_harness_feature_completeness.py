"""
Regression test: eval harness must hard-error on incomplete feat_dict.

Context: HRP_INVESTIGATION_2026-04-15.md
  MW test_set_50 feat_dict had 48 keys instead of 54. The old eval script
  called feat_dict.get(f, 0.0), silently defaulting 6 missing features to 0.
  This produced a bogus hero_range_percentile = 0.00 finding.

These tests verify:
  1. GtoOracle.features_from_dict() raises KeyError on an incomplete feat_dict.
  2. reference_evaluator._validate_feat_dict() raises ValueError listing all
     missing keys when any of the 54 FEATURE_COLUMNS are absent.
  3. A feat_dict produced by extract_all_features() always passes validation.
  4. The 6 specifically-missing MW schema keys are all caught.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gto_model import FEATURE_COLUMNS as GTO_FEATURE_COLUMNS
from feature_extractor import FEATURE_COLUMNS, extract_all_features


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _complete_feat_dict():
    """Return a minimal but complete feat_dict with all 54 FEATURE_COLUMNS."""
    hand = {
        'pos': 'BTN',
        'vp': 'BB',
        'fb': 0,
        'pot': 30.0,
        'tc': 0.0,
        'st': 'f',
        'h': 'AhKd',
        'b': 'Qs7h2c',
        'exp': 'B',
        '_is_3bet_pot': 0,
        '_villain_aggression_count': 0,
        '_villain_checked_back': 0,
        '_villain_call_count': 0,
        '_num_callers_to_bet': 0,
        '_facing_raise': 0,
    }
    return extract_all_features(hand)


def _mw_style_incomplete_feat_dict():
    """
    Simulate the MW test_set_50 feat_dict: 48 keys, missing the 6 Step-13/14/15
    features that were absent from the old pipeline schema.
    """
    feat = _complete_feat_dict()
    # Remove the exact 6 keys missing from MW test_set_50 per HRP investigation
    for key in (
        'flush_draw_rank',
        'has_showdown_value',
        'hero_range_percentile',
        'is_preflop_aggressor',
        'villain_fold_equity_estimate',
        'villain_medium_made_pct',
    ):
        feat.pop(key, None)
    return feat


# ---------------------------------------------------------------------------
# 1. GtoOracle.features_from_dict must hard-error on missing keys
# ---------------------------------------------------------------------------

class TestFeaturesFromDictHardError:

    def test_complete_dict_returns_array_of_54(self):
        """A complete feat_dict produces a length-54 numpy array without error."""
        import numpy as np
        from gto_model import GtoOracle
        feat = _complete_feat_dict()
        arr = GtoOracle.features_from_dict(feat)
        assert arr.shape == (54,), f"Expected shape (54,), got {arr.shape}"

    def test_mw_style_incomplete_raises(self):
        """
        An MW-style incomplete feat_dict (missing the 6 Step-13/14/15 keys)
        must raise KeyError — not silently default to 0.0.

        This is the regression test for the HRP_INVESTIGATION_2026-04-15.md bug.
        """
        from gto_model import GtoOracle
        incomplete = _mw_style_incomplete_feat_dict()
        # Verify the 6 keys are actually absent in the test fixture
        missing = [k for k in (
            'flush_draw_rank', 'has_showdown_value', 'hero_range_percentile',
            'is_preflop_aggressor', 'villain_fold_equity_estimate', 'villain_medium_made_pct',
        ) if k not in incomplete]
        assert len(missing) == 6, (
            f"Test setup error: expected 6 missing keys, found {len(missing)} missing: {missing}"
        )
        with pytest.raises(KeyError):
            GtoOracle.features_from_dict(incomplete)

    def test_single_missing_key_raises(self):
        """Even one missing key must raise KeyError."""
        from gto_model import GtoOracle
        feat = _complete_feat_dict()
        del feat['hero_range_percentile']
        with pytest.raises(KeyError):
            GtoOracle.features_from_dict(feat)

    def test_error_message_names_missing_key(self):
        """The KeyError message must identify which key is missing."""
        from gto_model import GtoOracle
        feat = _complete_feat_dict()
        del feat['villain_medium_made_pct']
        with pytest.raises(KeyError) as exc_info:
            GtoOracle.features_from_dict(feat)
        assert 'villain_medium_made_pct' in str(exc_info.value)

    def test_all_six_mw_missing_keys_are_caught(self):
        """Each of the 6 MW-missing keys individually triggers KeyError."""
        from gto_model import GtoOracle
        missing_keys = [
            'flush_draw_rank',
            'has_showdown_value',
            'hero_range_percentile',
            'is_preflop_aggressor',
            'villain_fold_equity_estimate',
            'villain_medium_made_pct',
        ]
        for key in missing_keys:
            feat = _complete_feat_dict()
            del feat[key]
            with pytest.raises(KeyError):
                GtoOracle.features_from_dict(feat)


# ---------------------------------------------------------------------------
# 2. reference_evaluator._validate_feat_dict hard-errors before scoring
# ---------------------------------------------------------------------------

class TestValidateFeatDict:

    def test_complete_dict_passes_validation(self):
        """A complete feat_dict passes _validate_feat_dict without error."""
        from reference_evaluator import _validate_feat_dict
        feat = _complete_feat_dict()
        # Must not raise
        _validate_feat_dict(feat, hand_id='test_hand')

    def test_mw_style_incomplete_raises_value_error(self):
        """
        An MW-style incomplete feat_dict must raise ValueError before scoring.

        This ensures the harness fails fast rather than scoring with zeros.
        """
        from reference_evaluator import _validate_feat_dict
        incomplete = _mw_style_incomplete_feat_dict()
        with pytest.raises(ValueError) as exc_info:
            _validate_feat_dict(incomplete, hand_id='MW-TEST')
        error_msg = str(exc_info.value)
        # Error message must mention the hand and at least one missing key
        assert 'MW-TEST' in error_msg
        assert 'hero_range_percentile' in error_msg

    def test_all_six_missing_keys_listed_in_error(self):
        """The ValueError for a 6-key-short dict must list all 6 missing keys."""
        from reference_evaluator import _validate_feat_dict
        incomplete = _mw_style_incomplete_feat_dict()
        with pytest.raises(ValueError) as exc_info:
            _validate_feat_dict(incomplete, hand_id='MW-TEST')
        error_msg = str(exc_info.value)
        for key in (
            'flush_draw_rank',
            'has_showdown_value',
            'hero_range_percentile',
            'is_preflop_aggressor',
            'villain_fold_equity_estimate',
            'villain_medium_made_pct',
        ):
            assert key in error_msg, (
                f"Expected '{key}' in error message, not found.\nMessage: {error_msg}"
            )

    def test_single_missing_key_raises(self):
        """Even a single missing key triggers ValueError."""
        from reference_evaluator import _validate_feat_dict
        feat = _complete_feat_dict()
        del feat['flush_draw_rank']
        with pytest.raises(ValueError):
            _validate_feat_dict(feat, hand_id='some_hand')


# ---------------------------------------------------------------------------
# 3. extract_all_features always produces a complete feat_dict
# ---------------------------------------------------------------------------

class TestExtractAllFeaturesCompleteness:

    def test_standard_flop_hand_has_all_54_columns(self):
        """extract_all_features on a normal flop hand returns all 54 FEATURE_COLUMNS."""
        feat = _complete_feat_dict()
        missing = [col for col in FEATURE_COLUMNS if col not in feat]
        assert not missing, f"extract_all_features missing columns: {missing}"

    def test_no_feature_column_is_none(self):
        """No FEATURE_COLUMNS entry should be None (only 0.0 or real value)."""
        feat = _complete_feat_dict()
        none_keys = [col for col in FEATURE_COLUMNS if feat.get(col) is None]
        assert not none_keys, f"Features with None value: {none_keys}"

    def test_feature_columns_match_gto_model(self):
        """FEATURE_COLUMNS in feature_extractor and gto_model must be identical."""
        assert list(FEATURE_COLUMNS) == list(GTO_FEATURE_COLUMNS), (
            "feature_extractor.FEATURE_COLUMNS and gto_model.FEATURE_COLUMNS are out of sync"
        )
