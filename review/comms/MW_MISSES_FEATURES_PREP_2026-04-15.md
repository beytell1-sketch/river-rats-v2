---
date: 2026-04-15
from: Programmer (Architecture Expert mixed role)
to: Track 4 analyst (when unblocked)
re: MW-miss feature extraction prep — data staged, no analysis performed
---

# MW Misses — Feature Extraction Prep (Track 4 data only)

## Scope

Per `MAIN_TERMINAL_UPDATE_2_2026-04-15.md` §Track 4 exception. Track 4 analysis
itself remains HELD. This deliverable is the staged feature data only.

## What's in `MW_MISSES_FEATURES_PREP_2026-04-15.jsonl`

10 records, one per MW reference miss (hands where v2.2 model predicts CHECK
but MW expert label is BET). Hand IDs match the solver verification set in
`SOLVER_VERIFICATION_MW_MISSES_2026-04-15.html`:

```
d1454_CO_turn, d1562_HJ_turn, d1983_HJ_turn, d2410_CO_turn, d2920_BB_turn,
d3178_CO_river, d3229_BTN_river, d3688_BB_flop, d8411_BB_turn, d8886_BB_flop
```

Per `HRP_INVESTIGATION_2026-04-15.md`, this list reflects the 1-hand swap
(d2920 now in, d4534 now out) relative to earlier reports.

Each JSONL record contains:

| Field | Meaning |
|---|---|
| `situation_id` | e.g. `d1454_CO_turn` |
| `hand_id` | alias of situation_id |
| `deal_id` | integer deal id |
| `hero_cards`, `board`, `street` | card-level context |
| `hero_position`, `villain_positions`, `num_opponents` | seat context |
| `facing_bet`, `pot`, `to_call` | pot context |
| `prior_actions`, `action_string` | action history (prior-street summary) |
| `ground_truth_label` / `expert_action` | MW expert-labelled GTO action |
| `oracle_action`, `adjusted_action`, `model_prediction` | stored v2.2 model outputs |
| `features` | dict of all **54 FEATURE\_COLUMNS** (see `feature_keys.py::F`) |
| `feature_columns_count` | 54 (the v9 contract width) |
| `features_extracted_count` | 54 for every record (no missing keys) |

All 10 records pass the `_validate_feat_dict()` completeness guard:
54/54 features present.

## How it was generated

1. Source situations: `training-data/test_set_50_labelled.jsonl`
   (filtered by the 10 `situation_id`s above).
2. Situation records were re-shaped into the gauntlet-format hand dict expected
   by `extract_all_features()`:
   - `h`, `b`, `pos`, `vp`, `fb`, `pot`, `tc`, `st`, `exp` mapped from
     the labelled record.
   - Primary villain position taken as the first entry in `villain_positions`
     (positional-order convention).
   - `_is_3bet_pot` derived by counting `raise` tokens in the preflop
     prior-action string (≥2 ⇒ 3bet pot).
   - `_opener_position` = first `<POS> raise` token on the preflop street.
   - `_villain_checked_back` = 1 if hero checked on any prior postflop street
     (since `facing_bet=0` on the decision street, villain also checked).
   - `_villain_aggression_count`, `_villain_call_count`,
     `_num_raises_this_street`, `_num_callers_to_bet`, `_facing_raise`
     default to 0 (consistent with the observed "all checks" action history
     on every miss).
   - `_num_opponents` from the record's `num_opponents` field.
3. `extract_all_features()` was called per hand (Steps 1–13, 54-feature
   output). No feature values were edited post-extraction.
4. The `features` dict in each record strips `_`-prefixed internal metadata
   and list-valued keys; the 54 canonical FEATURE\_COLUMNS are all retained
   as scalars.

Script: `/tmp/mw_extract.py` (ephemeral; this manifest is the record of intent).

## Hands that couldn't be processed

**None.** All 10 targeted `situation_id`s were located in
`test_set_50_labelled.jsonl` and extracted without exception.
`features_extracted_count == 54` for every record.

## Caveats for the Track 4 analyst

- The `oracle_action` / `adjusted_action` fields in the source JSONL are the
  **stored** v2.2 predictions from the original labelling run, not a fresh
  re-evaluation. If Track 4 wants current model predictions, re-run the
  v2.2 model on the `features` dict at analysis time.
- `d3688_BB_flop` has `expert_action = CHECK` in the stored record, but the
  MW-miss verification list treats it as a miss. This reflects pre/post
  re-extraction labelling discrepancy — flagging for the analyst, not
  resolving here.
- Metadata fields (`_villain_aggression_count`, etc.) were inferred from
  prior_actions text parsing. These are used by the extractor for a small
  subset of features; the inference is conservative (all zeros except
  `_villain_checked_back` and `_is_3bet_pot` where the preflop action string
  supports it).
- No analysis, bias signature computation, or model scoring was performed.
  That belongs to Track 4.
