# SPEC: Feature Expansion 38 to 45 Columns

**Date:** 6 April 2026
**Status:** Draft — awaiting approval
**Depends on:** Bridge fix (completed this session)
**Blocks:** v9 training, 500-hand labelling

---

## Objective

Expand FEATURE_COLUMNS from 38 to 45 by promoting 5 existing metadata
features and adding 2 new current-street action features. This is
infrastructure only — no retraining. The v8 model continues to run on
38 columns until v9 is trained on the wider vector.

---

## The 7 New Columns

### Promotions (5) — computed today, gated behind `_` prefix

| # | Feature name | Source | What it measures |
|---|---|---|---|
| 39 | `villain_top_pair_plus_pct` | `extract_range_composition()` | Fraction of villain range that is top pair+ |
| 40 | `villain_draw_pct` | same | Fraction that is drawing |
| 41 | `villain_air_pct` | same | Fraction that is air/bluff |
| 42 | `villain_range_capped` | same | Binary: villain didn't 3-bet, range has ceiling |
| 43 | `board_favour` | same | Heuristic -1 to +1, positive = favours hero |

These are already computed every hand by `extract_range_composition()`
(feature_extractor.py:1085-1203) and stored with `_` prefix. Promotion
means: remove `_` prefix, add to FEATURE_COLUMNS, include in model
input vector.

### New features (2) — not yet computed

| # | Feature name | Source | What it measures |
|---|---|---|---|
| 44 | `num_callers_to_bet` | Bridge from game state | How many opponents cold-called the current-street bet before hero acts. 0 = no callers or no bet. MW-30 signal: bet-and-call = 1. |
| 45 | `facing_raise` | Bridge from game state | Binary: hero faces a raise (not just an initial bet). MW-31 signal: check-raise = 1. Distinct from `facing_bet` which is 1 for both bets and raises. |

---

## Files to Change

### 1. feature_keys.py

Add 7 new `F.XXX` constants (model features, no underscore):

```
VILLAIN_TOP_PAIR_PLUS_PCT = 'villain_top_pair_plus_pct'
VILLAIN_DRAW_PCT = 'villain_draw_pct'
VILLAIN_AIR_PCT = 'villain_air_pct'
VILLAIN_RANGE_CAPPED = 'villain_range_capped'
BOARD_FAVOUR = 'board_favour'
NUM_CALLERS_TO_BET = 'num_callers_to_bet'
FACING_RAISE = 'facing_raise'
```

Keep the existing `META_VILLAIN_*` and `META_VILLAIN_RANGE_CAPPED`
constants — they're used by the teaching pipeline (SituationDescriber).
The new constants are model-facing aliases.

### 2. gto_model.py (lines 33-49)

Expand FEATURE_COLUMNS tuple. Append 7 new names after `num_opponents`.
Update comment `# 38` to `# 45`. N_FEATURES auto-updates via `len()`.

**Compatibility:** The v8 model file (`gto_model_v8_38feat.json`) expects
38 features. After this change, `GtoOracle.features_from_dict()` produces
45-element arrays, which v8 will reject. Two options:

- **Option A (recommended):** `features_from_dict()` accepts an optional
  `columns` parameter. Default = FEATURE_COLUMNS (45). Pass v8's 38-column
  list when running the v8 model. The v8 model path carries `38feat` in the
  name — use that as the signal.
- **Option B:** Keep v8 on 38 columns by reading the model's expected
  feature count at load time and slicing. More magic, harder to debug.

### 3. sizing_oracle.py (lines 81-97)

Same expansion as gto_model.py. Same compatibility concern — the sizing
model is also v3/38feat. Apply the same `columns` parameter approach.

### 4. feature_extractor.py

**Promote 5 metadata features (around line 1244):**

Currently `extract_range_composition()` returns `_`-prefixed keys which
are stored in the feature dict as metadata. After promotion:

- The function still returns `_`-prefixed keys (teaching pipeline reads them)
- `extract_all_features()` copies them into unprefixed model keys:
  ```python
  features['villain_top_pair_plus_pct'] = features.get('_villain_top_pair_plus_pct', 0.0)
  features['villain_draw_pct'] = features.get('_villain_draw_pct', 0.0)
  features['villain_air_pct'] = features.get('_villain_air_pct', 0.0)
  features['villain_range_capped'] = features.get('_villain_range_capped', 0)
  features['board_favour'] = features.get('_board_favour', 0.0)
  ```

**Add 2 new features (after the promotion block):**

```python
features['num_callers_to_bet'] = hand.get('_num_callers_to_bet', 0)
features['facing_raise'] = hand.get('_facing_raise', 0)
```

These are populated by the bridge (live play) or by hand dict (training/eval).
Default 0 for PokerBench rows (HU, no callers, no raises distinguished).

### 5. game_state_bridge.py

**`num_callers_to_bet`:** Count opponents who cold-called (not raised)
the current-street bet before hero acts. This must use the action
sequence from `game.street_actions`, not chip amounts — a player who
raised also has `bet_this_street == current_bet`, but a raise and a
cold-call are different signals. MW-30's "bet-and-call" is specifically
about a flat call confirming the bettor's range.

```python
if facing_bet and hasattr(game, 'street_actions'):
    current_street = context.get('street', 'flop')
    actions = game.street_actions.get(current_street, [])
    # Count call actions by opponents (not hero, not the bettor)
    num_callers_to_bet = sum(
        1 for name, pos, act in actions
        if act == 'call' and pos != player.position and pos != bettor_position
    )
else:
    num_callers_to_bet = 0
```

This correctly distinguishes cold-callers from raisers. A player who
raised appears as `('name', 'pos', 'raise')` in street_actions, not
as a caller.

**`facing_raise`:** True if `raises_this_street > 0` AND `facing_bet`.
A raise means someone bet, then someone else raised (or check-raised).

```python
facing_raise = int(facing_bet and num_raises > 0)
```

**Boundary case (documented, not a bug):** This captures "hero
currently faces a raise-level action" regardless of who initiated
aggression. If hero bet and villain raised, facing_raise = 1 (correct,
hero faces a raise). If hero raised preflop and faces a 3-bet,
facing_raise = 1 (also correct — hero faces a raise). The feature
does not distinguish "villain raised into me" from "I raised and got
re-raised." Both signal strength from the opponent. For MW-31
(check-raise) and MW-46 (river check-raise), the definition is exact.

**`is_3bet_pot` fix (feature 34, currently dead):** While touching the
bridge, also fix this one-liner. The bridge already has
`raises_this_street` from the context. For preflop context passed to
postflop decisions:

```python
# Preflop had 2+ raise actions = 3-bet pot
pf_actions = getattr(game, 'street_actions', {}).get('preflop', [])
is_3bet = int(sum(1 for _, _, a in pf_actions if a in ('bet', 'raise')) >= 2)
```

Add to hand dict: `'_is_3bet_pot': is_3bet`. This activates the last
dead feature — all 45 columns are now live.

Add all three to the hand dict:
```python
'_num_callers_to_bet': num_callers_to_bet,
'_facing_raise': facing_raise,
'_is_3bet_pot': is_3bet,
```

### 6. poker_game.py

**No changes needed.** The bridge computes `num_callers_to_bet` and
`facing_raise` from `game.street_actions` (added in the bridge fix)
and `context['num_raises_this_street']` (already tracked). The
`is_3bet_pot` fix also reads from `game.street_actions`. No new
tracking needed in PokerGame beyond what the bridge fix already added.

### 7. reference_evaluator.py

Add `_num_callers_to_bet` and `_facing_raise` to the hand dict in
`_evaluate_one_hand()`. These can be derived from the existing hand
design fields:

- `num_callers_to_bet`: Parse from action history prose (same approach
  as action-history annotations — lookup table per hand)
- `facing_raise`: 1 if the hand design describes a raise/check-raise
  scenario (MW-31, MW-46, MW-50)

Add `_NUM_CALLERS_TO_BET` and `_FACING_RAISE` to the `_ACTION_HISTORY`
lookup table.

### 8. train_model.py

Update to read 45-column CSV. The training pipeline reads
FEATURE_COLUMNS to select columns from the CSV — once FEATURE_COLUMNS
is 45-wide, training automatically expects 45 columns.

Update model output filename: `gto_model_v9_45feat.json`.

### 9. Tests to update

| File | What changes |
|---|---|
| `test_multiway_features.py:34` | `assert len(FEATURE_COLUMNS) == 45` |
| `test_multiway_features.py:46-47` | `assert GTO_N == 45; assert SZ_N == 45` |
| `test_sizing_oracle.py:152` | `assert N_FEATURES == 45` |
| `test_game_state_bridge.py:111` | `assert arr.shape == (45,)` (after v9 trained) |
| `test_oracle_shap.py:200` | `assert arr.shape == (N_FEATURES,)` (already uses N_FEATURES, OK) |

Tests that reference `gto_model_v8_38feat.json` by path: leave unchanged
until v9 model exists. Tests that use N_FEATURES dynamically: already
compatible.

### 10. coaching/ directory

`coaching/gto_model.py` and `coaching/sizing_oracle.py` are copies of
the core files. They must be updated in sync. `coaching/shap_explainer.py`
uses N_FEATURES dynamically — compatible.

---

## Compatibility Strategy

The v8 model (38 features) must continue to work during development.
The v9 model (45 features) won't exist until training completes.

**Approach:** `GtoOracle.__init__()` reads `n_features_in_` from the
loaded XGBoost model to detect the expected feature count. If the model
expects 38, `features_from_dict()` uses the first 38 columns of
FEATURE_COLUMNS. If it expects 45, it uses all 45. This makes the code
forward-compatible without needing two column lists.

```python
def __init__(self, model_path: str):
    import xgboost as xgb
    self._model = xgb.XGBClassifier()
    self._model.load_model(model_path)
    # Auto-detect feature width for backwards compatibility
    self._n_features = getattr(self._model, 'n_features_in_', len(FEATURE_COLUMNS))

@staticmethod
def features_from_dict(feat_dict: dict, n_features: int = None) -> np.ndarray:
    cols = FEATURE_COLUMNS[:n_features] if n_features else FEATURE_COLUMNS
    return np.array([feat_dict.get(f, 0.0) for f in cols], dtype=np.float32)
```

The oracle's `predict()` method passes `self._n_features` to
`features_from_dict()`.

---

## What This Does NOT Do

- No retraining. The v8 model runs on 38 features throughout.
- No new training data. The PokerBench backfill and 500-hand labelling
  are separate specs.
- No changes to adjuster logic. The adjuster reads features by name
  (`.get()`), not by index — new columns don't affect it.
- No changes to preflop engine. Preflop uses range tables, not the oracle.
- No dead features after this ships. Features 34-37 (formerly dead)
  are all activated: `is_3bet_pot` via preflop action count,
  features 35-37 via the bridge fix from earlier this session.

---

## Verification

After implementation, verify:

1. `python3 -m pytest tests/` — all existing tests pass (v8 model still works)
2. Reference evaluator produces identical 21/40 results (no regression)
3. `features_from_dict()` with a 45-feature dict produces a 38-element
   array when v8 model is loaded (backwards compat)
4. The 5 promoted features have nonzero values in the reference hand
   feature dicts (spot-check MW-30, MW-42)
5. `num_callers_to_bet` = 1 for MW-30 (BTN called CO's bet)
6. `facing_raise` = 1 for MW-31 (CO check-raised)
7. `facing_raise` = 1 for MW-46 (CO check-raised river)
8. `is_3bet_pot` correctly computed from preflop action sequence
   (0 for single-raised pots, 1 for 3-bet pots)

---

## Risk

**Sizing oracle drift.** The sizing oracle has its own FEATURE_COLUMNS
and its own model. If we expand its columns but don't retrain the
sizing model, the same compatibility layer must apply. The sizing model
is less critical than the action model — it only affects bet sizing,
not action selection. But it must not break.

**Range computation cost.** The 5 promoted features run
`extract_range_composition()` which iterates villain's range and
classifies each hand. This already runs every hand (for teaching
metadata). Promoting to model features doesn't add computation — the
values are already there. No performance regression.

**PokerBench backfill accuracy.** When generating 45-column PokerBench
CSV, the range features will be computed in HU context (num_opponents=1).
The values will be "correct for HU" but different from what they'd be
in multiway. This is expected — the 500 MW-labelled rows provide the
multiway signal. XGBoost handles mixed-context training data well as
long as `num_opponents` separates the distributions.

---

## Expected Outcome: v9-on-PokerBench Will NOT Improve MW Accuracy

This must be stated explicitly so nobody misreads the results.

The 5 promoted range features have **different semantics depending on
num_opponents.** In PokerBench (HU) rows, `villain_top_pair_plus_pct`
reflects a single opponent's full preflop range on the board. In MW
rows, the same feature reflects a narrower range in a contested
multiway pot — a fundamentally different distribution.

When v9 trains on 25k PokerBench rows (HU context) + the range
features, the model will learn HU-specific splits on those features.
It **cannot** learn MW-specific patterns (like "high TP+% plus
aggression = fold") from data that has no MW examples with correct
MW labels. The 500 MW rows (2% of training data) are what teach
the MW interactions.

**Therefore:**
- A v9 retrain on PokerBench-only with 45 columns should produce
  ~identical accuracy on the 40-hand MW reference set. This is the
  expected outcome, not a failure.
- The accuracy improvement comes in Step 4 (retrain on PokerBench +
  500 MW expert labels), not Step 3 (retrain on PokerBench alone).
- Do not skip the PokerBench-only retrain — it establishes the v9
  baseline and validates the pipeline. Just don't expect MW gains.
