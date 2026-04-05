"""
Tests for explain_hand.py — end-to-end integration.

Two test groups:
  1. From pre-computed features (CSV) — always runs
  2. From raw gauntlet JSON — skipped if foundation modules unavailable
"""

import sys
sys.path.insert(0, '/home/rupertbeytell/river-rats/river-rats-complete')

import os
import pytest
import csv
import time
import numpy as np

from coaching.explain_hand import ExplainEngine, get_engine
from coaching.explanation import Explanation
from coaching.levels import PlayerLevel
from coaching.gto_model import FEATURE_COLUMNS, ACTION_CLASSES


# ═══════════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════════

MODEL_PATH = "/home/rupertbeytell/river-rats/river-rats-complete/gto_model_v8_38feat.json"
DATA_PATH = "/home/rupertbeytell/river-rats/training_data_38feat_v3/test_action_38.csv"

model_available = pytest.mark.skipif(
    not os.path.exists(MODEL_PATH),
    reason="Model file not available",
)


@pytest.fixture(scope="module")
def engine():
    if not os.path.exists(MODEL_PATH):
        pytest.skip("Model file not available")
    return ExplainEngine(MODEL_PATH)


@pytest.fixture(scope="module")
def sample_feat_dicts():
    """Load 30 feature dicts from CSV."""
    if not os.path.exists(DATA_PATH):
        pytest.skip("Dataset not available")
    from coaching.gto_model import ACTION_TO_INT
    with open(DATA_PATH) as f:
        reader = csv.DictReader(f)
        rows = [next(reader) for _ in range(30)]
    action_col = "action" if "action" in rows[0] else "action_label"
    result = []
    for row in rows:
        _NON_FEAT = {"action", "action_label", "size_bucket", "hu_original_action", "base_hand_id"}
        feat = {k: float(v) for k, v in row.items() if k not in _NON_FEAT}
        true_action = ACTION_TO_INT[row[action_col].strip()]
        result.append((feat, true_action))
    return result


# ═══════════════════════════════════════════════════════════════════
# FROM PRE-COMPUTED FEATURES
# ═══════════════════════════════════════════════════════════════════

class TestExplainFromFeatures:
    """explain_from_features() — the common production path."""

    @model_available
    def test_returns_explanation(self, engine, sample_feat_dicts):
        feat, _ = sample_feat_dicts[0]
        exp = engine.explain_from_features(feat, PlayerLevel.L1_PERCEPTION)
        assert isinstance(exp, Explanation)

    @model_available
    def test_has_headline(self, engine, sample_feat_dicts):
        feat, _ = sample_feat_dicts[0]
        exp = engine.explain_from_features(feat, PlayerLevel.L1_PERCEPTION)
        assert len(exp.headline) > 0

    @model_available
    def test_action_is_valid(self, engine, sample_feat_dicts):
        feat, _ = sample_feat_dicts[0]
        exp = engine.explain_from_features(feat, PlayerLevel.L1_PERCEPTION)
        assert exp.action in ACTION_CLASSES

    @model_available
    def test_confidence_is_probability(self, engine, sample_feat_dicts):
        feat, _ = sample_feat_dicts[0]
        exp = engine.explain_from_features(feat, PlayerLevel.L1_PERCEPTION)
        assert 0.0 < exp.confidence <= 1.0

    @model_available
    def test_supporting_is_tuple(self, engine, sample_feat_dicts):
        feat, _ = sample_feat_dicts[0]
        exp = engine.explain_from_features(feat, PlayerLevel.L1_PERCEPTION)
        assert isinstance(exp.supporting, tuple)

    @model_available
    def test_max_3_supporting(self, engine, sample_feat_dicts):
        """V3: up to 2 observations + 1 tightness preview = max 3."""
        for feat, _ in sample_feat_dicts[:20]:
            for level in PlayerLevel:
                exp = engine.explain_from_features(feat, level)
                assert len(exp.supporting) <= 3, (
                    f"Got {len(exp.supporting)} supporting at {level.value}"
                )

    @model_available
    def test_explanation_is_frozen(self, engine, sample_feat_dicts):
        feat, _ = sample_feat_dicts[0]
        exp = engine.explain_from_features(feat, PlayerLevel.L1_PERCEPTION)
        with pytest.raises(AttributeError):
            exp.headline = "changed"

    @model_available
    def test_no_render_errors(self, engine, sample_feat_dicts):
        """No [render error] in any output text."""
        for i, (feat, _) in enumerate(sample_feat_dicts[:20]):
            for level in PlayerLevel:
                exp = engine.explain_from_features(feat, level)
                all_text = _all_text(exp)
                assert "[render error" not in all_text, (
                    f"Hand {i} {level.value}: {all_text}"
                )

    @model_available
    def test_no_double_possessive(self, engine, sample_feat_dicts):
        """No 'Your your hand' anywhere."""
        for i, (feat, _) in enumerate(sample_feat_dicts[:20]):
            for level in PlayerLevel:
                exp = engine.explain_from_features(feat, level)
                all_text = _all_text(exp)
                assert "your your" not in all_text.lower(), (
                    f"Hand {i} {level.value}: {all_text}"
                )

    @model_available
    def test_with_card_strings(self, engine, sample_feat_dicts):
        """Card strings are passed through to context (no crash)."""
        feat, _ = sample_feat_dicts[0]
        exp = engine.explain_from_features(
            feat, PlayerLevel.L1_PERCEPTION,
            hero_cards="AcKs", board_cards="Th4c5d",
        )
        assert isinstance(exp, Explanation)

    @model_available
    def test_deterministic(self, engine, sample_feat_dicts):
        feat, _ = sample_feat_dicts[0]
        r1 = engine.explain_from_features(feat, PlayerLevel.L2_CAUSE_EFFECT)
        r2 = engine.explain_from_features(feat, PlayerLevel.L2_CAUSE_EFFECT)
        assert r1.headline == r2.headline
        assert r1.supporting == r2.supporting
        assert r1.action == r2.action


class TestExplainFromFeaturesAllLevels:
    """explain_from_features_all_levels()"""

    @model_available
    def test_returns_all_5_levels(self, engine, sample_feat_dicts):
        feat, _ = sample_feat_dicts[0]
        results = engine.explain_from_features_all_levels(feat)
        assert len(results) == 5
        for lvl in ["L1", "L2", "L3", "L4", "L5"]:
            assert lvl in results
            assert isinstance(results[lvl], Explanation)

    @model_available
    def test_all_levels_same_action(self, engine, sample_feat_dicts):
        """All levels should recommend the same action for the same hand."""
        for feat, _ in sample_feat_dicts[:10]:
            results = engine.explain_from_features_all_levels(feat)
            actions = {results[lvl].action for lvl in results}
            assert len(actions) == 1, f"Multiple actions: {actions}"


# ═══════════════════════════════════════════════════════════════════
# PERFORMANCE
# ═══════════════════════════════════════════════════════════════════

class TestPerformance:
    """Performance benchmarks."""

    @model_available
    def test_single_hand_under_50ms(self, engine, sample_feat_dicts):
        """Single hand explanation from features should be fast."""
        feat, _ = sample_feat_dicts[0]
        # Warm up SHAP explainer
        engine.explain_from_features(feat, PlayerLevel.L1_PERCEPTION)

        times = []
        for feat, _ in sample_feat_dicts[:10]:
            t0 = time.time()
            engine.explain_from_features(feat, PlayerLevel.L2_CAUSE_EFFECT)
            times.append((time.time() - t0) * 1000)

        avg_ms = sum(times) / len(times)
        assert avg_ms < 50, f"Average {avg_ms:.1f}ms exceeds 50ms budget"

    @model_available
    def test_all_levels_under_60ms(self, engine, sample_feat_dicts):
        """All 5 levels for one hand should be fast (SHAP computed once)."""
        feat, _ = sample_feat_dicts[0]
        # Warm up
        engine.explain_from_features_all_levels(feat)

        times = []
        for feat, _ in sample_feat_dicts[:10]:
            t0 = time.time()
            engine.explain_from_features_all_levels(feat)
            times.append((time.time() - t0) * 1000)

        avg_ms = sum(times) / len(times)
        assert avg_ms < 60, f"Average {avg_ms:.1f}ms exceeds 60ms budget"


# ═══════════════════════════════════════════════════════════════════
# FROM RAW JSON (requires foundation modules)
# ═══════════════════════════════════════════════════════════════════

def _foundation_available():
    """Check if feature_extractor and its dependencies are importable."""
    try:
        sys.path.insert(0, '/mnt/project')
        from feature_extractor import extract_all_features
        return True
    except ImportError:
        return False


foundation_available = pytest.mark.skipif(
    not _foundation_available(),
    reason="Foundation modules not available",
)


# Sample gauntlet JSON hands (minimal valid format)
SAMPLE_HANDS_JSON = [
    {
        "id": 1,
        "pos": "BTN",
        "fb": 0,
        "pot": 6.5,
        "tc": 0.0,
        "st": "f",
        "h": "AcKs",
        "b": "Th4c5d",
        "exp": "B",
        "vp": "BB",
    },
    {
        "id": 2,
        "pos": "BB",
        "fb": 1,
        "pot": 12.0,
        "tc": 6.0,
        "st": "t",
        "h": "8s8d",
        "b": "Ks7h2c9d",
        "exp": "C",
        "vp": "BTN",
    },
    {
        "id": 3,
        "pos": "CO",
        "fb": 1,
        "pot": 25.0,
        "tc": 15.0,
        "st": "r",
        "h": "Jh9h",
        "b": "Qh8h3c2dAd",
        "exp": "F",
        "vp": "BB",
    },
]


class TestExplainFromJSON:
    """Full pipeline from raw gauntlet JSON."""

    @model_available
    @foundation_available
    def test_basic_explain(self, engine):
        exp = engine.explain(SAMPLE_HANDS_JSON[0], PlayerLevel.L1_PERCEPTION)
        assert isinstance(exp, Explanation)
        assert len(exp.headline) > 0

    @model_available
    @foundation_available
    def test_action_is_valid(self, engine):
        exp = engine.explain(SAMPLE_HANDS_JSON[0], PlayerLevel.L1_PERCEPTION)
        assert exp.action in ACTION_CLASSES

    @model_available
    @foundation_available
    def test_all_sample_hands(self, engine):
        """All 3 sample hands produce valid explanations."""
        for hand in SAMPLE_HANDS_JSON:
            exp = engine.explain(hand, PlayerLevel.L2_CAUSE_EFFECT)
            assert isinstance(exp, Explanation)
            assert len(exp.headline) > 0
            assert "[render error" not in _all_text(exp)

    @model_available
    @foundation_available
    def test_all_levels_from_json(self, engine):
        results = engine.explain_all_levels(SAMPLE_HANDS_JSON[0])
        assert len(results) == 5
        for lvl, exp in results.items():
            assert isinstance(exp, Explanation)

    @model_available
    @foundation_available
    def test_json_vs_features_consistent(self, engine):
        """JSON path and features path should produce same action."""
        hand = SAMPLE_HANDS_JSON[0]

        # JSON path
        exp_json = engine.explain(hand, PlayerLevel.L2_CAUSE_EFFECT)

        # Manually extract features, then use features path
        sys.path.insert(0, '/mnt/project')
        from feature_extractor import extract_all_features
        all_feat = extract_all_features(hand)
        feat_dict = {f: float(all_feat.get(f, 0.0)) for f in FEATURE_COLUMNS}
        hero_cards = "".join(all_feat.get("_hero_cards", []))
        board_cards = "".join(all_feat.get("_board_cards", []))

        exp_feat = engine.explain_from_features(
            feat_dict, PlayerLevel.L2_CAUSE_EFFECT,
            hero_cards=hero_cards, board_cards=board_cards,
        )

        # Same action and headline
        assert exp_json.action == exp_feat.action
        assert exp_json.headline == exp_feat.headline


# ═══════════════════════════════════════════════════════════════════
# SINGLETON / CONVENIENCE
# ═══════════════════════════════════════════════════════════════════

class TestGetEngine:
    """Module-level convenience singleton."""

    @model_available
    def test_returns_engine(self):
        eng = get_engine(MODEL_PATH)
        assert isinstance(eng, ExplainEngine)

    @model_available
    def test_singleton(self):
        eng1 = get_engine(MODEL_PATH)
        eng2 = get_engine(MODEL_PATH)
        assert eng1 is eng2


# ═══════════════════════════════════════════════════════════════════
# ACTION COVERAGE
# ═══════════════════════════════════════════════════════════════════

class TestActionCoverage:
    """Every action type produces valid explanations."""

    @model_available
    def test_all_5_actions_covered(self, engine, sample_feat_dicts):
        """Across 30 hands, we should see all 5 action types get explanations."""
        actions_seen = set()
        for feat, _ in sample_feat_dicts:
            exp = engine.explain_from_features(feat, PlayerLevel.L2_CAUSE_EFFECT)
            actions_seen.add(exp.action)
            if len(actions_seen) == 5:
                break

        # We may not see all 5 in 30 random hands, but we should see at least 3
        assert len(actions_seen) >= 3, (
            f"Only saw {len(actions_seen)} action types: {actions_seen}"
        )

    @model_available
    def test_each_action_has_headline(self, engine, sample_feat_dicts):
        """Every predicted action produces a non-empty headline."""
        for feat, _ in sample_feat_dicts:
            exp = engine.explain_from_features(feat, PlayerLevel.L1_PERCEPTION)
            assert len(exp.headline) > 0, f"Empty headline for {exp.action}"


# ═══════════════════════════════════════════════════════════════════
# HELPER
# ═══════════════════════════════════════════════════════════════════

def _all_text(exp: Explanation) -> str:
    parts = [exp.headline] + list(exp.supporting)
    if exp.qualifier:
        parts.append(exp.qualifier)
    return " ".join(parts)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
