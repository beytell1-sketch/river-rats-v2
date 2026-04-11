---
date: 2026-04-09
from: Process reviewer (on behalf of owner)
re: Owner question — should we add is_preflop_aggressor as a feature?
---

## Owner's question

Should we label/track whether hero was the preflop aggressor (opened
the betting or raised a bet)? This affects postflop decisions — the
PFA has a range advantage on most boards.

## Current state (reviewer's findings)

The 52-feature vector has NO explicit is_preflop_aggressor feature.

What exists:
- `_pfr_advantage`: internal meta-feature (underscore prefix, not
  in training features). Used to compute board_favour.
- `opener_pos`: tracked internally for villain range construction
  but hero's own aggressor status isn't exposed to the model.
- `had_preflop_open`: was explicitly removed ("oracle always plays
  opened pots").

The model knows indirectly who opened (through board_favour and
villain range estimates) but doesn't know whether HERO specifically
was the opener vs a caller.

## What the builder needs to assess

This is a feature design question requiring GTO Expert + ML-architect
input per Process Guide §3.1 (research before design):

1. Does `is_preflop_aggressor` add signal beyond what `board_favour`
   already captures? (ML-architect)
2. Is it feature-visible for labelling — can the labeller see it
   in the situation data? (architect)
3. Does it interact with the RAISE decision tree? E.g., PFA on a
   dry board might change the bet/check threshold. (GTO Expert)
4. Is the data already there? The action_history in every situation
   records preflop actions — extracting hero's preflop action should
   be straightforward. (architect)

## Timing consideration

This came up during Step 7 (labelling). Adding a feature mid-pipeline
means:
- Feature 53 needs building + testing
- Factory situations need regenerating with 53 features
- The decision tree may need updating
- Calibration may need re-running

The builder should assess whether this blocks Step 7 or can be
deferred to v3.2 without wasting the current labelling work.

## Owner's intent

Brainstorming, not directing. Wants honest expert assessment of
whether this adds value.
