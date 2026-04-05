"""
NarrativeBuilder -- produces action-coherent observations.

Pipeline:
  1. Classify the spot (SpotClassification)
  2. Build SpotObservation (structured fact bag)
  3. Try LevelRenderer (new 3-level architecture)
  4. If LevelRenderer produces output -> use it
  5. Fallback to SpotCatalog -> SituationDescriber
"""
from typing import List, Optional
import logging

from coaching.spot_classifier import classify_spot, SpotClassification
from coaching.spot_narratives import SPOT_CATALOG
from coaching.observation_builders import build_observation
from coaching.level_renderer import render
from coaching.situation_describer import SituationDescriber
from coaching.levels import PlayerLevel, level_index

_logger = logging.getLogger(__name__)
_fallback_count = 0


class NarrativeBuilder:
    def __init__(self):
        self._describer = SituationDescriber()

    def build(self, ctx, feat_dict, shap_dict, pred, level,
              action=None, range_breakdown=None):
        """
        Produce 2-3 action-coherent observation sentences.

        Pipeline:
          1. Classify the spot (SpotClassification)
          2. Build SpotObservation (structured fact bag)
          3. Try LevelRenderer (3-level architecture: Beginner/Intermediate/Advanced)
          4. If LevelRenderer miss -> try SpotCatalog
          5. Fallback to SituationDescriber
        """
        global _fallback_count

        effective_action = action or pred.action

        # 1. Classify the spot
        spot = classify_spot(effective_action, ctx, feat_dict, pred, range_breakdown)

        # 2. Build SpotObservation (intermediate representation)
        spot_obs = None
        try:
            spot_obs = build_observation(spot, ctx, feat_dict, range_breakdown)
            _logger.debug(
                "SpotObservation built: action=%s role=%s bucket=%s "
                "equity=%.2f ci=%s(%s) range_state=%s",
                spot_obs.action, spot_obs.strategic_role, spot_obs.hand_bucket,
                spot_obs.equity, spot_obs.is_counterintuitive,
                spot_obs.counterintuitive_reason,
                spot_obs.villain_range_state,
            )
        except Exception as e:
            _logger.warning("SpotObservation build failed: %s", e)

        # 3. Try LevelRenderer (new 3-level architecture)
        #    Map 5 levels to 3: L1->Beginner(0), L2->Intermediate(1), L3+->Advanced(2+)
        if spot_obs is not None:
            try:
                lidx = level_index(level)  # L1=0, L2=1, L3=2, L4=3, L5=4
                # Map: 0->0(Beginner), 1->1(Intermediate), 2+=2(Advanced)
                teaching_level = min(lidx, 2)
                result = render(spot_obs, teaching_level)
                if result:
                    self._last_spot_observation = spot_obs
                    return result
            except Exception as e:
                _logger.debug("LevelRenderer failed, falling back: %s", e)

        # 4. Try SpotCatalog
        key = (spot.action, spot.strategic_role, level.value)
        narrative = SPOT_CATALOG.get(key)

        if narrative is not None:
            # Build observations from catalog
            observations = []
            for fn in narrative.observations:
                try:
                    obs = fn(ctx, feat_dict, range_breakdown)
                    if obs:
                        observations.append(obs)
                except Exception:
                    pass

            if observations:
                self._last_spot_observation = spot_obs
                return observations

        # 5. Fallback to SituationDescriber
        _fallback_count += 1
        if _fallback_count <= 10 or _fallback_count % 100 == 0:
            _logger.debug(
                "NarrativeBuilder fallback #%d: spot=(%s, %s, %s)",
                _fallback_count, spot.action, spot.strategic_role, level.value,
            )

        self._last_spot_observation = spot_obs

        return self._describer.describe(ctx, feat_dict, shap_dict, pred, level)

    @property
    def last_spot_observation(self):
        """The most recently built SpotObservation (for future LevelRenderer)."""
        return getattr(self, '_last_spot_observation', None)

    @staticmethod
    def fallback_count():
        return _fallback_count
