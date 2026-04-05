"""
explain_hand â€" end-to-end integration: raw hand â†’ coaching explanation.

This is the API surface that the mobile app calls.

Two entry points:
    explain_hand(hand_json, level)
        Full pipeline from raw gauntlet JSON.
        Extracts features, predicts, explains, resolves.
        ~120ms per hand (dominated by feature extraction equity calc).

    explain_from_features(feat_dict, level, hero_cards, board_cards)
        From pre-computed features (skips extraction).
        ~12ms per hand (dominated by SHAP).

Both return an Explanation dataclass ready for the UI.

Usage:
    from coaching.explain_hand import ExplainEngine, explain_from_features

    # Option A: full pipeline (requires foundation modules in sys.path)
    engine = ExplainEngine("gto_model_v4_compact.json")
    result = engine.explain(hand_json, PlayerLevel.L2_CAUSE_EFFECT)

    # Option B: from pre-computed features (no foundation modules needed)
    engine = ExplainEngine("gto_model_v4_compact.json")
    result = engine.explain_from_features(
        feat_dict, PlayerLevel.L2_CAUSE_EFFECT,
        hero_cards="AcKs", board_cards="Th4c5d7s",
    )

    # Result (v3 — situation awareness):
    result.headline      # "GTO checks here."
    result.supporting    # ("You have top pair...", "The board is dry...")
    result.qualifier     # None or "The other action is also reasonable here."
    result.action        # "CHECK"
    result.confidence    # 0.72
    result.is_mixed      # False
"""

import dataclasses
import numpy as np
from typing import Dict, List, Optional

from coaching.gto_model import (
    GtoOracle, OraclePrediction, FEATURE_COLUMNS, N_FEATURES,
)
from coaching.shap_explainer import ShapExplainer, ShapResult
from coaching.hand_context import build_hand_context, HandContext
from coaching.levels import PlayerLevel, level_gte
from coaching.explanation import Explanation
from coaching.situation_describer import SituationDescriber
from coaching.narrative_builder import NarrativeBuilder
from coaching.decision_reporter import DecisionReporter


# ── Position ordinal → string (reverse of POSITION_ORDINAL) ──────

_POS_NAMES = {0: 'UTG', 1: 'HJ', 2: 'CO', 3: 'BTN', 4: 'SB', 5: 'BB'}


def _ordinal_to_pos(ordinal) -> str:
    """Convert a position ordinal (0-5) to a position name string."""
    return _POS_NAMES.get(int(ordinal), 'BTN')


def _split_cards(card_str: str) -> List[str]:
    """Split a concatenated card string like 'Jh9hKd' into ['Jh', '9h', 'Kd']."""
    return [card_str[i:i+2] for i in range(0, len(card_str), 2)] if card_str else []


# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
# ENGINE
# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â

class ExplainEngine:
    """
    End-to-end coaching engine.

    Holds the oracle and SHAP explainer. Stateless per-hand â€"
    no memory between calls. Thread-safe after __init__.

    Lifecycle:
        1. Create once at app startup
        2. Call explain() or explain_from_features() per hand
        3. No cleanup needed
    """

    def __init__(self, model_path: str, sizing_model_path: str = None):
        """
        Args:
            model_path: Path to the XGBoost action model JSON file.
            sizing_model_path: Optional path to the raise sizing model JSON.
                If provided, explanations for BET/RAISE include sizing advice.
        """
        self._oracle = GtoOracle(model_path)
        self._explainer = ShapExplainer(self._oracle)
        self._describer = SituationDescriber()
        self._narrator = NarrativeBuilder()
        self._reporter = DecisionReporter()
        self._sizing_oracle = None
        if sizing_model_path:
            from coaching.sizing_oracle import SizingOracle
            self._sizing_oracle = SizingOracle(sizing_model_path)

    @property
    def oracle(self) -> GtoOracle:
        return self._oracle

    @property
    def explainer(self) -> ShapExplainer:
        return self._explainer

    # â"€â"€ Full pipeline: raw JSON â†’ Explanation â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

    def explain(
        self,
        hand_json: dict,
        level: PlayerLevel,
        num_opponents: int = 1,
    ) -> Explanation:
        """
        Full pipeline from raw gauntlet JSON.

        Requires feature_extractor.py and its foundation modules
        (hand_evaluator, board_analyzer, range_manager, raw_equity)
        to be importable.

        Args:
            hand_json: Raw hand dict from gauntlet JSON format.
                Required keys: pos, fb, pot, h, b, st, exp
                Optional: tc, vp
            level: Player level for the explanation.
            num_opponents: Number of opponents (1 = HU, 2+ = multiway).

        Returns:
            Explanation with headline + supporting + qualifier.
        """
        feat_dict, hero_cards, board_cards = self._extract_features(hand_json)
        return self._explain_core(feat_dict, level, hero_cards, board_cards,
                                  num_opponents)

    def explain_all_levels(
        self,
        hand_json: dict,
        num_opponents: int = 1,
    ) -> Dict[str, Explanation]:
        """
        Full pipeline, all 5 levels at once.

        Args:
            hand_json: Raw hand dict from gauntlet JSON format.
            num_opponents: Number of opponents (1 = HU, 2+ = multiway).

        Returns:
            {level_str: Explanation} e.g. {"L1": ..., "L2": ..., ...}
        """
        feat_dict, hero_cards, board_cards = self._extract_features(hand_json)
        return self._explain_all_core(feat_dict, hero_cards, board_cards,
                                      num_opponents)

    # â"€â"€ From pre-computed features â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

    def explain_from_features(
        self,
        feat_dict: Dict[str, float],
        level: PlayerLevel,
        hero_cards: str = "",
        board_cards: str = "",
        num_opponents: int = 1,
    ) -> Explanation:
        """
        From pre-computed features (skips extraction).

        Args:
            feat_dict: {feature_name: value} for the 37 model features.
            level: Player level for the explanation.
            hero_cards: Optional card string (e.g. "AcKs") for display.
            board_cards: Optional board string (e.g. "Th4c5d") for display.
            num_opponents: Number of opponents (1 = HU, 2+ = multiway).

        Returns:
            Explanation with headline + supporting + qualifier.
        """
        return self._explain_core(feat_dict, level, hero_cards, board_cards,
                                  num_opponents)

    def explain_from_features_all_levels(
        self,
        feat_dict: Dict[str, float],
        hero_cards: str = "",
        board_cards: str = "",
        num_opponents: int = 1,
    ) -> Dict[str, Explanation]:
        """
        From pre-computed features, all 5 levels at once.

        Args:
            feat_dict: {feature_name: value} for the 37 model features.
            hero_cards: Optional card string (e.g. "AcKs") for display.
            board_cards: Optional board string (e.g. "Th4c5d") for display.
            num_opponents: Number of opponents (1 = HU, 2+ = multiway).
        """
        return self._explain_all_core(feat_dict, hero_cards, board_cards,
                                      num_opponents)

    # â"€â"€ Core implementation â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

    def _explain_core(
        self,
        feat_dict: Dict[str, float],
        level: PlayerLevel,
        hero_cards: str = "",
        board_cards: str = "",
        num_opponents: int = 1,
    ) -> Explanation:
        """Shared core: features -> oracle -> SHAP -> describe + report."""
        # Oracle prediction
        X = GtoOracle.features_from_dict(feat_dict)
        pred = self._oracle.predict(X)

        # SHAP explanation
        shap_res = self._explainer.explain(X, pred.action_idx)

        # Multiway adjustment (post-oracle, pre-teaching)
        adjustment = None
        effective_action = pred.action
        if num_opponents >= 2:
            from coaching.multiway_adjuster import adjust
            adjustment = adjust(pred, feat_dict, num_opponents)
            effective_action = adjustment.adjusted_action

        # Post-prediction guard: RAISE is impossible without a bet to face.
        # If the model outputs RAISE on a street where no bet is present, demote to BET.
        if effective_action == 'RAISE' and not feat_dict.get('facing_bet', 0):
            effective_action = 'BET'

        # Sizing prediction (additive — None for non-BET/RAISE or no sizing oracle)
        sizing = None
        if self._sizing_oracle is not None and effective_action in ("BET", "RAISE"):
            sizing = self._sizing_oracle.predict(X, effective_action)

        # Hand context
        ctx = build_hand_context(feat_dict, hero_cards, board_cards,
                                 num_opponents)

        # Range decomposition at L4+ (lazy, ~7ms)
        if level_gte(level, PlayerLevel.L4_MEASUREMENT) and hero_cards and board_cards:
            try:
                from range_decomposition import decompose_range
                from feature_extractor import get_villain_range

                hero_pos_raw = feat_dict.get('_hero_pos_raw', '') or _ordinal_to_pos(feat_dict.get('hero_position', 3))
                villain_pos_raw = feat_dict.get('_villain_pos_raw', '') or _ordinal_to_pos(feat_dict.get('villain_position', 5))

                hero_cards_list = _split_cards(hero_cards)
                board_cards_list = _split_cards(board_cards)

                v_range = get_villain_range(hero_pos_raw, villain_pos_raw)
                if feat_dict.get('facing_bet', 0):
                    from range_narrowing import narrow_to_betting_range
                    street_map = {0: 'flop', 1: 'turn', 2: 'river'}
                    street_name = street_map.get(int(feat_dict.get('street', 0)), 'flop')
                    v_range = narrow_to_betting_range(v_range, board_cards_list, street_name)

                breakdown = decompose_range(
                    hero_cards_list, board_cards_list, v_range,
                    spr=feat_dict.get('spr', 10.0),
                    bet_to_pot=feat_dict.get('bet_to_pot', 0.0),
                )
                ctx = dataclasses.replace(ctx, range_breakdown=breakdown)
            except Exception:
                pass  # Graceful fallback — coaching works without decomposition

        # V3: Situation description + Decision report
        return self._assemble(pred, shap_res, feat_dict, ctx, level,
                              effective_action, sizing, adjustment)

    def _explain_all_core(
        self,
        feat_dict: Dict[str, float],
        hero_cards: str = "",
        board_cards: str = "",
        num_opponents: int = 1,
    ) -> Dict[str, Explanation]:
        """Shared core: features -> oracle -> SHAP -> all 5 levels."""
        X = GtoOracle.features_from_dict(feat_dict)
        pred = self._oracle.predict(X)
        shap_res = self._explainer.explain(X, pred.action_idx)

        # Multiway adjustment
        adjustment = None
        effective_action = pred.action
        if num_opponents >= 2:
            from coaching.multiway_adjuster import adjust
            adjustment = adjust(pred, feat_dict, num_opponents)
            effective_action = adjustment.adjusted_action

        # Post-prediction guard: RAISE is impossible without a bet to face.
        if effective_action == 'RAISE' and not feat_dict.get('facing_bet', 0):
            effective_action = 'BET'

        # Sizing prediction (only for BET/RAISE after adjustment)
        sizing = None
        if self._sizing_oracle is not None and effective_action in ("BET", "RAISE"):
            sizing = self._sizing_oracle.predict(X, effective_action)

        ctx = build_hand_context(feat_dict, hero_cards, board_cards,
                                 num_opponents)

        # Range decomposition (computed once, used for L4+ levels)
        ctx_with_breakdown = ctx
        if hero_cards and board_cards:
            try:
                from range_decomposition import decompose_range
                from feature_extractor import get_villain_range

                hero_pos_raw = feat_dict.get('_hero_pos_raw', '') or _ordinal_to_pos(feat_dict.get('hero_position', 3))
                villain_pos_raw = feat_dict.get('_villain_pos_raw', '') or _ordinal_to_pos(feat_dict.get('villain_position', 5))

                hero_cards_list = _split_cards(hero_cards)
                board_cards_list = _split_cards(board_cards)

                v_range = get_villain_range(hero_pos_raw, villain_pos_raw)
                if feat_dict.get('facing_bet', 0):
                    from range_narrowing import narrow_to_betting_range
                    street_map = {0: 'flop', 1: 'turn', 2: 'river'}
                    street_name = street_map.get(int(feat_dict.get('street', 0)), 'flop')
                    v_range = narrow_to_betting_range(v_range, board_cards_list, street_name)

                breakdown = decompose_range(
                    hero_cards_list, board_cards_list, v_range,
                    spr=feat_dict.get('spr', 10.0),
                    bet_to_pot=feat_dict.get('bet_to_pot', 0.0),
                )
                ctx_with_breakdown = dataclasses.replace(ctx, range_breakdown=breakdown)
            except Exception:
                pass  # Graceful fallback

        # V3: Generate all levels from shared oracle + SHAP computation
        results = {}
        for level in PlayerLevel:
            level_ctx = ctx_with_breakdown if level_gte(level, PlayerLevel.L4_MEASUREMENT) else ctx
            results[level.value] = self._assemble(
                pred, shap_res, feat_dict, level_ctx, level,
                effective_action, sizing, adjustment,
            )
        return results

    # -- Assembly: combine SituationDescriber + DecisionReporter ------

    def _assemble(
        self,
        pred: OraclePrediction,
        shap_res: ShapResult,
        feat_dict: Dict[str, float],
        ctx: HandContext,
        level: PlayerLevel,
        effective_action: str,
        sizing,
        adjustment,
    ) -> Explanation:
        """Assemble v3 Explanation from situation + decision modules."""
        # Situation observations (pre-decision)
        observations = self._narrator.build(
            ctx, feat_dict, shap_res.shap_dict, pred, level,
            action=effective_action,
            range_breakdown=getattr(ctx, 'range_breakdown', None),
        )

        # Decision report (post-decision) — pass effective_action so the headline
        # reflects the final adjusted action, not the raw oracle prediction.
        report = self._reporter.report(pred, feat_dict, ctx, level,
                                       effective_action=effective_action)

        # Build qualifier from tightness + causal bridge
        qualifier_parts = []
        if report.tightness_sentence:
            qualifier_parts.append(report.tightness_sentence)
        if report.causal_bridge:
            qualifier_parts.append(report.causal_bridge)
        qualifier = " ".join(qualifier_parts) if qualifier_parts else None

        # Sizing info
        sizing_bucket = None
        sizing_pot_ratio = None
        if sizing is not None:
            sizing_bucket = sizing.bucket if hasattr(sizing, 'bucket') else None
            sizing_pot_ratio = sizing.pot_ratio if hasattr(sizing, 'pot_ratio') else None

        # Multiway flag
        multiway_adjusted = (adjustment is not None
                             and hasattr(adjustment, 'was_adjusted')
                             and adjustment.was_adjusted)

        return Explanation(
            headline=report.action_statement,
            supporting=tuple(observations),
            qualifier=qualifier,
            is_mixed=report.is_mixed,
            action=effective_action,
            confidence=pred.confidence,
            sizing_bucket=sizing_bucket,
            sizing_pot_ratio=sizing_pot_ratio,
            multiway_adjusted=multiway_adjusted,
            level=level,
        )

    # -- Feature extraction (lazy import) ------------------------------

    @staticmethod
    def _extract_features(hand_json: dict):
        """
        Extract features from raw gauntlet JSON.

        Lazy-imports feature_extractor to avoid pulling in
        foundation modules unless actually needed.

        Returns:
            (feat_dict, hero_cards_str, board_cards_str)
        """
        from feature_extractor import extract_all_features

        all_features = extract_all_features(hand_json)

        # Build numeric-only feature dict for the model
        # Use .get() for new features to support both 33- and 37-feature extractors
        feat_dict = {
            f: float(all_features.get(f, 0.0))
            for f in FEATURE_COLUMNS
        }

        # Pass through metadata fields (underscore-prefixed) for HandContext
        for key, val in all_features.items():
            if key.startswith("_") and key not in ("_hero_cards", "_board_cards"):
                feat_dict[key] = val

        # Extract card strings for HandContext display
        hero_cards_list = all_features.get("_hero_cards", [])
        board_cards_list = all_features.get("_board_cards", [])
        hero_cards = "".join(hero_cards_list)
        board_cards = "".join(board_cards_list)

        return feat_dict, hero_cards, board_cards


# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
# MODULE-LEVEL CONVENIENCE (stateless â€" creates engine each call)
# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
#
# For production use, create an ExplainEngine once and reuse it.
# These are provided only for quick scripting / REPL use.

_default_engine = None


def get_engine(
    model_path: str = "/mnt/project/gto_model_v4_compact.json",
    sizing_model_path: str = None,
) -> ExplainEngine:
    """Get or create the default engine singleton."""
    global _default_engine
    if _default_engine is None:
        _default_engine = ExplainEngine(model_path, sizing_model_path)
    return _default_engine
