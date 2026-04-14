---
date: 2026-04-14
from: Software Architect
to: Owner (Rupert) / Programmer
re: Blueprint — Feature Attention Training Experiments (all 4)
status: FOR OWNER REVIEW
prerequisite: PLAN_FEATURE_ATTENTION_TRAINING_2026-04-14.md (approved)
blocks: Programmer build (Step 5)
---

# Blueprint: Feature Attention Training Experiments

## Source files read before this blueprint was written

- `/home/rupertbeytell/river-rats-v2/review/comms/PLAN_FEATURE_ATTENTION_TRAINING_2026-04-14.md`
- `/home/rupertbeytell/river-rats-v2/review/comms/DIRECTIVE_FEATURE_ATTENTION_TRAINING_EXPERIMENT_2026-04-14.md`
- `/home/rupertbeytell/river-rats-v2/river-rats-core/train_model.py`
- `/home/rupertbeytell/river-rats-v2/river-rats-core/gto_model.py`
- `/home/rupertbeytell/river-rats-v2/river-rats-core/feature_keys.py`
- `/home/rupertbeytell/river-rats-v2/training-data/tag_vocabulary.json`
- `/tmp/pilot_situations.json` (20 hands, feat_dict per hand, confirmed structure)
- `/tmp/pilot_v2_consensus.json` (flat dict: situation_id -> action string)
- `/home/rupertbeytell/river-rats-v2/review/comms/PILOT_V2_UNTAGGED_FEATURES_2026-04-14.txt`
  (per-hand list of untagged feature names — the SOURCE for deriving binary attention flags)

---

## Critical data findings before reading this blueprint

### What data exists in files

| Data needed | File available | Format |
|---|---|---|
| Feature vectors (54 values per hand) | `/tmp/pilot_situations.json` | JSON list, `feat_dict` per record |
| Consensus labels | `/tmp/pilot_v2_consensus.json` | Flat dict: `{situation_id: action_string}` |
| Binary tagged/untagged per feature per hand | `PILOT_V2_UNTAGGED_FEATURES_2026-04-14.txt` | Text file listing UNTAGGED features per hand |
| Attention levels (PRIMARY/CONFIRMED/DISCOVERED) | NOT IN ANY FILE | Must be hardcoded |
| Intention tags per hand | NOT IN ANY FILE | Must be hardcoded |

### What must be hardcoded

The pilot v2 agent outputs (attention levels and intention tags) exist only in the
conversation context from the pilot run — they were not written to structured files.
The assembly script must hardcode two lookup tables:

1. `ATTENTION_LEVELS`: a dict mapping `situation_id -> {feature_name: level_string}`
   where level_string is one of "PRIMARY", "CONFIRMED", "DISCOVERED".
   Features absent from this dict are "Untagged" (weight 0.1).

2. `INTENTION_TAGS`: a dict mapping `situation_id -> list[str]` where each string
   is a tag from the vocabulary in `training-data/tag_vocabulary.json`.

The Programmer hardcodes these from the pilot report narrative and the tag vocabulary.
See Section 4 (Assembly Script) for the exact hardcoded data to embed.

### What the untagged file gives us

The PILOT_V2_UNTAGGED_FEATURES file lists untagged features per hand. Tagged features
= FEATURE_COLUMNS (54 total) minus the untagged set for that hand.
This is sufficient for computing binary attention flags (Exp 3) and binary tagged/untagged
arrays (Exp 1 masking).
It is NOT sufficient for attention levels (Exp 2) — the file doesn't record
PRIMARY/CONFIRMED/DISCOVERED per feature.

---

## Files to create

```
river-rats-core/
  assemble_pilot_data.py            NEW — assembly script
  run_attention_experiments.py      NEW — experiment runner (all 4 + baseline)
  tests/
    test_attention_experiments.py   NEW — tests written BEFORE implementation

training-data/
  pilot_20_enriched.jsonl           NEW — canonical one-row-per-hand JSONL (owner amendment 1)
  pilot_20_base.csv                 NEW — 20 x 55 cols (54 features + label)
  pilot_20_attention.csv            NEW — 20 x 109 cols (54 features + 54 attn flags + label)
  pilot_20_attention_levels.csv     NEW — 20 x 109 cols (54 features + 54 level cols + label)
  pilot_20_intentions.csv           NEW — 20 x (54 + N_tags) cols

results/                            EXISTING dir — new files added
  pilot_exp0_baseline.json          NEW
  pilot_exp1_masking.json           NEW
  pilot_exp2_weighting.json         NEW
  pilot_exp3_auxiliary.json         NEW
  pilot_exp4_intentions.json        NEW
  pilot_experiment_comparison.json  NEW
```

DO NOT MODIFY any existing file in `river-rats-core/`.

---

## Section 1: Imports and shared constants

Both `assemble_pilot_data.py` and `run_attention_experiments.py` must import
FEATURE_COLUMNS and ACTION_CLASSES from `gto_model.py`, not redefine them.

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from gto_model import FEATURE_COLUMNS, ACTION_CLASSES
```

The FEATURE_COLUMNS tuple in gto_model.py has exactly 54 entries.
ACTION_CLASSES tuple is ("FOLD", "CHECK", "CALL", "BET", "RAISE") in that order.

---

## Section 2: Hardcoded pilot data

The assembly script contains two hardcoded module-level dicts.
The Programmer must embed these exactly.

### 2a. ATTENTION_LEVELS

Keys: situation_id strings (all 20)
Values: dict mapping feature_name -> level_string

Level strings: "PRIMARY", "CONFIRMED", "DISCOVERED"
Absent features (not in the inner dict): treated as "Untagged" at weight 0.1.

Source for these values: the pilot v2 run narrative and the PILOT_V2_REPORT.
Per the report, mandatory composition features on BET/RAISE/CALL/FOLD hands
(villain_top_pair_plus_pct, villain_medium_made_pct, villain_draw_pct, villain_air_pct)
were tagged PRIMARY by all 4 teams. Bucket-specific mandatory features
(e.g. draw_outs, improvement_probability for drawing hands) were tagged CONFIRMED.
Discovery team features (villain_fold_equity_estimate, spr, villain_checked_back, etc.)
were tagged DISCOVERED.

The Programmer derives the full table using this hierarchy:
- PRIMARY: features cited as primary decision drivers in the pilot report reasoning
- CONFIRMED: mandatory composition features + bucket-specific features
- DISCOVERED: discovery team finds from the report (top discoveries: villain_fold_equity_estimate,
  spr, villain_checked_back, connectivity_score, is_preflop_aggressor, overcard_outs,
  flush_draw_rank, board_favour, straight_danger, is_paired, flush_block_pct, flush_danger)

Any feature appearing in the PILOT_V2_UNTAGGED_FEATURES_2026-04-14.txt for a given hand
must NOT appear in that hand's ATTENTION_LEVELS entry.

For CHECK hands not facing a bet, composition features (villain_*_pct) are untagged
and must not be in PRIMARY or CONFIRMED for those hands.

The Programmer verifies: for every hand, the set of features in ATTENTION_LEVELS[hand_id]
must be DISJOINT from the untagged features list for that hand.

### 2b. INTENTION_TAGS

Keys: situation_id strings (all 20)
Values: list of 1-3 tag strings from tag_vocabulary.json

Tag vocabulary (from tag_vocabulary.json "intentions" section):
- "value_extract"
- "deny_equity"
- "bluff_fold_better"
- "continue_draw"
- "pot_control"
- "range_fold_priced_out"

The Programmer assigns intention tags per hand based on the pilot report
consensus reasoning. Reference mapping:

| Hand | Label | Bucket | Tags (from pilot report reasoning) |
|---|---|---|---|
| d4534_BB_flop | CHECK | strong_made | pot_control |
| d7760_BTN_flop | CHECK | air | pot_control |
| d6384_BTN_turn | CHECK | air | pot_control |
| d6066_BB_flop | CHECK | monster | pot_control |
| d5046_CO_flop | BET | monster | value_extract, deny_equity |
| d6826_CO_turn | BET | monster | value_extract |
| d1971_HJ_river | BET | strong_made | value_extract |
| d2285_BTN_river | FOLD | air | range_fold_priced_out |
| d6533_BTN_river | FOLD | weak_made | range_fold_priced_out |
| d1200_HJ_turn | FOLD | air | range_fold_priced_out |
| BP1_22 | CALL | drawing | continue_draw |
| BP2_35 | RAISE | monster | value_extract, deny_equity |
| BP3_03 | FOLD | air | range_fold_priced_out |
| BP4_28 | BET | strong_made | value_extract, deny_equity |
| BP5_02 | CHECK | monster | pot_control |
| BP6_01 | RAISE | drawing | bluff_fold_better, continue_draw |
| BP7_03 | CALL | drawing | continue_draw |
| BP2_36 | RAISE | monster | value_extract |
| BP2_42 | FOLD | air | range_fold_priced_out |
| BP5_05 | BET | monster | value_extract |

These are the blueprint-specified tags. The Programmer must verify each tag
string exactly matches a key in the tag_vocabulary.json "intentions" dict before
writing the hardcoded table. Any mismatch halts assembly with an error.

---

## Section 3: File 1 — assemble_pilot_data.py

**Path:** `/home/rupertbeytell/river-rats-v2/river-rats-core/assemble_pilot_data.py`

**Purpose:** Reads `/tmp/pilot_situations.json` and `/tmp/pilot_v2_consensus.json`,
merges with the hardcoded ATTENTION_LEVELS and INTENTION_TAGS tables,
writes `pilot_20_enriched.jsonl` (canonical JSONL) and four CSV files,
and prints a verification summary.

**Run from:** repo root. All paths relative to repo root.

### Module-level constants

```python
PILOT_SITUATIONS_PATH = '/tmp/pilot_situations.json'
PILOT_CONSENSUS_PATH  = '/tmp/pilot_v2_consensus.json'
TAG_VOCAB_PATH        = 'training-data/tag_vocabulary.json'
UNTAGGED_FEATURES_PATH = 'review/comms/PILOT_V2_UNTAGGED_FEATURES_2026-04-14.txt'
ENRICHED_JSONL_PATH   = 'training-data/pilot_20_enriched.jsonl'
BASE_CSV_PATH         = 'training-data/pilot_20_base.csv'
ATTENTION_CSV_PATH    = 'training-data/pilot_20_attention.csv'
LEVELS_CSV_PATH       = 'training-data/pilot_20_attention_levels.csv'
INTENTIONS_CSV_PATH   = 'training-data/pilot_20_intentions.csv'

LEVEL_WEIGHTS = {
    'PRIMARY': 1.0,
    'CONFIRMED': 0.7,
    'DISCOVERED': 0.5,
    'Untagged': 0.1,
}
```

Hardcoded ATTENTION_LEVELS and INTENTION_TAGS are also at module level (see Section 2).

### Function: load_pilot_sources()

```python
def load_pilot_sources() -> tuple[list[dict], dict[str, str]]:
```

Reads `/tmp/pilot_situations.json` and `/tmp/pilot_v2_consensus.json`.
Returns a 2-tuple: (situations_list, consensus_dict).
`situations_list`: the raw list of 20 dicts from the JSON file.
`consensus_dict`: the flat dict mapping situation_id to action string.

Raises `FileNotFoundError` if either source file is missing.
Raises `ValueError` if the situations list does not contain exactly 20 items.
Raises `ValueError` if any situation_id in situations_list is not present in consensus_dict.
Raises `ValueError` if any consensus action is not in ACTION_CLASSES.

### Function: parse_untagged_features_file()

```python
def parse_untagged_features_file(path: str) -> dict[str, set[str]]:
```

Parses `PILOT_V2_UNTAGGED_FEATURES_2026-04-14.txt`.
Returns a dict mapping situation_id -> set of untagged feature names.

The file format is: lines beginning with "--- HAND_ID |" start a new block.
Within each block, lines matching the pattern `  FEATURE_NAME  =  VALUE` are feature lines.
Extract FEATURE_NAME (the part before the first whitespace group following the leading spaces).

Raises `ValueError` if the parsed dict does not contain exactly 20 keys.
Raises `ValueError` if any parsed feature name is not in FEATURE_COLUMNS.
Note: the file uses human-readable position names for hero_position and villain_position
(e.g., "BTN", "CO") in some hands; these are display values in the file, not feature names.
The feature names being parsed are the dict keys (left column), which do match FEATURE_COLUMNS.

### Function: validate_attention_levels()

```python
def validate_attention_levels(untagged_map: dict[str, set[str]]) -> None:
```

Cross-validates the hardcoded ATTENTION_LEVELS table against the parsed untagged map.
For each situation_id and each feature in ATTENTION_LEVELS[situation_id]:
- Asserts that feature is in FEATURE_COLUMNS.
- Asserts that feature is NOT in untagged_map[situation_id] (a tagged feature cannot
  also appear as untagged).
- Asserts that the level string is one of ("PRIMARY", "CONFIRMED", "DISCOVERED").

Raises `ValueError` with a descriptive message on the first violation found.
Prints "ATTENTION_LEVELS: OK — N feature-level assignments validated" on success.

### Function: validate_intention_tags()

```python
def validate_intention_tags(vocab: dict) -> None:
```

Validates the hardcoded INTENTION_TAGS table.
`vocab` is the parsed content of tag_vocabulary.json (the "intentions" sub-dict).
For each situation_id and each tag in INTENTION_TAGS[situation_id]:
- Asserts that tag is a key in vocab.
- Asserts that the tag list has 1-3 entries.

Raises `ValueError` if any tag string does not match the vocabulary.
Raises `ValueError` if INTENTION_TAGS does not have exactly 20 keys.
Prints "INTENTION_TAGS: OK — N tag assignments validated" on success.

### Function: build_enriched_record()

```python
def build_enriched_record(
    situation: dict,
    label: str,
    untagged_features: set[str],
) -> dict:
```

Builds one enriched record for the canonical JSONL.
`situation`: one item from pilot_situations.json (has `situation_id`, `feat_dict`).
`label`: consensus action string for this hand.
`untagged_features`: set of feature names that are untagged for this hand.

Returns a dict with these keys:
- `situation_id`: str
- `label`: str (the consensus action)
- `feat_dict`: dict mapping each of the 54 FEATURE_COLUMNS to its float value
  (taken directly from situation['feat_dict'], verified against FEATURE_COLUMNS)
- `attention_flags`: dict mapping each of the 54 FEATURE_COLUMNS to int (0 or 1)
  (1 if feature is tagged — i.e., NOT in untagged_features — else 0)
- `attention_levels`: dict mapping each of the 54 FEATURE_COLUMNS to float
  (the LEVEL_WEIGHT for this feature: 1.0 if PRIMARY, 0.7 if CONFIRMED,
  0.5 if DISCOVERED, 0.1 if untagged. Source: ATTENTION_LEVELS[situation_id])
- `intention_tags`: list[str] from INTENTION_TAGS[situation_id]
- `n_tagged`: int — count of features with attention_flag == 1

Raises `ValueError` if situation['feat_dict'] is missing any key in FEATURE_COLUMNS.

### Function: write_enriched_jsonl()

```python
def write_enriched_jsonl(records: list[dict], path: str) -> None:
```

Writes one JSON-serialized record per line to `path`.
Each line is a complete JSON object (no newlines within the object).
Raises `IOError` if the file cannot be written.
Prints "Wrote N records to PATH" on success.

### Function: write_base_csv()

```python
def write_base_csv(records: list[dict], path: str) -> None:
```

Writes `pilot_20_base.csv`.
Columns: the 54 FEATURE_COLUMNS (in FEATURE_COLUMNS order) then `label`.
Values from `record['feat_dict']` and `record['label']`.
20 rows, header row included.
Raises `ValueError` if records list is not length 20.

### Function: write_attention_csv()

```python
def write_attention_csv(records: list[dict], path: str) -> None:
```

Writes `pilot_20_attention.csv`.
Columns: 54 FEATURE_COLUMNS + 54 `attn_{feature_name}` columns (one per feature,
in FEATURE_COLUMNS order) + `label`.
Total: 109 columns.
`attn_*` values are 0 or 1 from `record['attention_flags']`.
Values from `record['feat_dict']`, `record['attention_flags']`, `record['label']`.

### Function: write_levels_csv()

```python
def write_levels_csv(records: list[dict], path: str) -> None:
```

Writes `pilot_20_attention_levels.csv`.
Columns: 54 FEATURE_COLUMNS + 54 `level_{feature_name}` columns (one per feature,
in FEATURE_COLUMNS order) + `label`.
Total: 109 columns.
`level_*` values are floats from `record['attention_levels']`
(1.0, 0.7, 0.5, or 0.1 per the LEVEL_WEIGHTS mapping).

### Function: write_intentions_csv()

```python
def write_intentions_csv(records: list[dict], path: str) -> None:
```

Writes `pilot_20_intentions.csv`.
Columns: 54 FEATURE_COLUMNS + one `intent_{tag}` column per unique intention tag
observed across all 20 records (sorted alphabetically). No `label` column.
Each `intent_*` cell is 1 if the tag appears in `record['intention_tags']`, else 0.
Total columns: 54 + N_unique_tags.

Before writing, prints the intention tag distribution:
"  intent_{tag}: {count}/20 hands" for each unique tag, sorted by count descending.

### Function: print_verification_summary()

```python
def print_verification_summary(records: list[dict]) -> None:
```

Prints to stdout:
- Total records: 20
- Feature column count: 54
- Label distribution: {FOLD: N, CHECK: N, CALL: N, BET: N, RAISE: N}
- Attention coverage: avg tagged per hand, min tagged, max tagged
- Intention tag distribution: count per unique tag (owner amendment 2 — tag discovery)
- A finding line: "Top N tags cover M% of hands" where N and M are computed
  (find the smallest N such that the top-N tags by frequency cover >= 90% of hands)
- Files written: list of all 5 output file paths

### Function: main()

```python
def main() -> None:
```

Orchestrates assembly in this exact order:
1. Load tag vocabulary from TAG_VOCAB_PATH
2. Call `load_pilot_sources()` — get situations list and consensus dict
3. Call `parse_untagged_features_file(UNTAGGED_FEATURES_PATH)` — get untagged map
4. Call `validate_attention_levels(untagged_map)` — halt on failure
5. Call `validate_intention_tags(vocab['intentions'])` — halt on failure
6. Build enriched records: `[build_enriched_record(s, consensus[s['situation_id']], untagged_map[s['situation_id']]) for s in situations]`
7. Call `write_enriched_jsonl(records, ENRICHED_JSONL_PATH)`
8. Call `write_base_csv(records, BASE_CSV_PATH)`
9. Call `write_attention_csv(records, ATTENTION_CSV_PATH)`
10. Call `write_levels_csv(records, LEVELS_CSV_PATH)`
11. Call `write_intentions_csv(records, INTENTIONS_CSV_PATH)`
12. Call `print_verification_summary(records)`
13. Print "ASSEMBLY COMPLETE — proceed to experiments"

If any step raises an exception, print "ASSEMBLY FAILED: {error}" and exit(1).
The Programmer must NOT proceed to any experiment if assembly exits with code 1.

---

## Section 4: File 2 — run_attention_experiments.py

**Path:** `/home/rupertbeytell/river-rats-v2/river-rats-core/run_attention_experiments.py`

**Purpose:** Loads the 4 CSV files from training-data/, runs Baseline + Experiments 1-4,
writes 6 JSON results files to results/, and prints a summary.

**Run from:** repo root. All paths relative to repo root.

### Module-level constants

```python
BASE_CSV         = 'training-data/pilot_20_base.csv'
ATTENTION_CSV    = 'training-data/pilot_20_attention.csv'
LEVELS_CSV       = 'training-data/pilot_20_attention_levels.csv'
INTENTIONS_CSV   = 'training-data/pilot_20_intentions.csv'
RESULTS_DIR      = 'results'

PILOT_XGB_CONFIG = dict(
    n_estimators=50,
    max_depth=2,
    learning_rate=0.1,
    subsample=1.0,
    colsample_bytree=1.0,
    min_child_weight=1,
    gamma=0.0,
    reg_alpha=0.0,
    reg_lambda=1.0,
    objective='multi:softprob',
    num_class=5,
    random_state=42,
    n_jobs=1,
)

BINARY_XGB_CONFIG = dict(
    n_estimators=50,
    max_depth=2,
    learning_rate=0.1,
    subsample=1.0,
    colsample_bytree=1.0,
    min_child_weight=1,
    gamma=0.0,
    reg_alpha=0.0,
    reg_lambda=1.0,
    objective='binary:logistic',
    random_state=42,
    n_jobs=1,
)
```

### Function: load_feature_csv()

```python
def load_feature_csv(
    path: str,
    feature_cols: list[str],
    label_col: str | None = 'label',
) -> tuple[np.ndarray, np.ndarray | None, list[str]]:
```

Reads a CSV file. Returns a 3-tuple: (X, y, column_names).
`feature_cols`: list of column names to use as features (in order).
`label_col`: name of the label column. If None, y is returned as None.
`X`: numpy float32 array of shape (n_rows, len(feature_cols)).
`y`: numpy int32 array of shape (n_rows,) with integer-encoded labels
     using ACTION_TO_INT = {a: i for i, a in enumerate(ACTION_CLASSES)}.
     None if label_col is None.
`column_names`: the list of feature column names (same as feature_cols).

Raises `ValueError` if any feature_col is not in the CSV header.
Raises `ValueError` if label_col is specified but not in the CSV header.
Raises `ValueError` if n_rows != 20.

### Function: run_loo_cv()

```python
def run_loo_cv(
    X: np.ndarray,
    y: np.ndarray,
    model_config: dict,
    exp_name: str,
) -> tuple[list[str], list[str], int]:
```

Runs leave-one-out cross-validation with XGBClassifier using `model_config`.
Returns a 3-tuple: (true_labels, loo_predictions, n_fold_failures).

`true_labels`: list of 20 action strings (from INT_TO_ACTION), in sample order.
`loo_predictions`: list of 20 predicted action strings, in sample order.
  For folds that failed (see below), the prediction is the string "FOLD_ERROR".
`n_fold_failures`: count of folds where XGBoost raised an exception.

Implementation: use `sklearn.model_selection.LeaveOneOut`.
For each (train_index, test_index) pair:
  - Fit `xgb.XGBClassifier(**model_config)` on X[train_index], y[train_index].
  - Predict on X[test_index], append INT_TO_ACTION[pred] to loo_predictions.
  - If XGBoost raises any exception during fit or predict:
    - Increment n_fold_failures.
    - Append "FOLD_ERROR" to loo_predictions.
    - Print "  [WARN] {exp_name} fold {i} failed: {error_type}"
    - Continue to next fold.

Do NOT use `cross_val_predict` from sklearn — it does not support per-fold
error handling. Use the explicit loop.

### Function: fit_full_model()

```python
def fit_full_model(
    X: np.ndarray,
    y: np.ndarray,
    model_config: dict,
) -> tuple[object, dict[str, float]]:
```

Fits a single XGBClassifier on all 20 samples (no CV).
Returns a 2-tuple: (fitted_model, feature_importance_dict).
`fitted_model`: the fitted xgb.XGBClassifier instance.
`feature_importance_dict`: dict mapping feature index (as string "feat_0", "feat_1", ...)
  to importance float. This is the raw form — callers convert to named form.

Note: callers are responsible for mapping indices to named features.

### Function: get_named_importances()

```python
def get_named_importances(
    model: object,
    column_names: list[str],
) -> list[tuple[str, float]]:
```

Extracts `model.feature_importances_` and pairs with column_names.
Returns a list of (feature_name, importance_float) tuples sorted by importance descending.
`column_names` must have the same length as `model.feature_importances_`.
Raises `ValueError` if lengths differ.

### Function: run_baseline()

```python
def run_baseline(output_path: str) -> dict:
```

Runs Experiment 0 (Baseline).
1. Calls `load_feature_csv(BASE_CSV, list(FEATURE_COLUMNS), 'label')` to get X (20x54), y.
2. Calls `run_loo_cv(X, y, PILOT_XGB_CONFIG, 'exp0_baseline')` for LOO predictions.
3. Calls `fit_full_model(X, y, PILOT_XGB_CONFIG)` for feature importance.
4. Calls `get_named_importances(model, list(FEATURE_COLUMNS))` for named importance list.
5. Assembles result dict (see Output Format below).
6. Writes result dict as JSON to `output_path`.
7. Returns the result dict (other experiments use baseline predictions for comparison).

Output format (pilot_exp0_baseline.json):
```json
{
  "experiment": "baseline",
  "n_samples": 20,
  "n_features": 54,
  "xgb_config": { ... },
  "action_distribution": {"FOLD": N, "CHECK": N, ...},
  "loo_true_labels": ["FOLD", "CHECK", ...],
  "loo_predictions": ["FOLD", "CHECK", ...],
  "n_fold_failures": 0,
  "feature_importance": [
    {"feature": "equity_vs_range", "importance": 0.1234},
    ...
  ],
  "top20_features": ["equity_vs_range", ...]
}
```
`feature_importance` is the full sorted list of all 54 features.
`top20_features` is the ordered list of the top 20 feature names by importance.

### Function: apply_masking()

```python
def apply_masking(
    X: np.ndarray,
    column_names: list[str],
    untagged_per_hand: list[set[str]],
) -> tuple[np.ndarray, dict]:
```

Applies per-sample feature masking (Experiment 1).
`X`: shape (20, 54).
`column_names`: list of 54 feature names in column order.
`untagged_per_hand`: list of 20 sets, each containing the untagged feature names for that row.
  Must be in the same order as X rows. The Programmer loads this from the enriched JSONL.

Creates a copy of X. For each row i:
  For each feature j where column_names[j] is in untagged_per_hand[i]:
    Set X_masked[i, j] = 0.0

Returns (X_masked, stats_dict) where stats_dict has:
  "avg_features_zeroed": float (mean number of features zeroed per row)
  "min_features_zeroed": int
  "max_features_zeroed": int

### Function: run_exp1_masking()

```python
def run_exp1_masking(baseline_result: dict, output_path: str) -> dict:
```

Runs Experiment 1 (per-sample feature masking).
1. Loads base CSV: `load_feature_csv(BASE_CSV, list(FEATURE_COLUMNS), 'label')` for X, y.
2. Loads enriched JSONL to get `untagged_per_hand`: for each record in order matching
   pilot_situations.json order, extract the set `{f for f in FEATURE_COLUMNS if record['attention_flags'][f] == 0}`.
   Note: the enriched JSONL rows must be in the same order as BASE_CSV rows.
3. Calls `apply_masking(X, list(FEATURE_COLUMNS), untagged_per_hand)` to get X_masked and stats.
4. Calls `run_loo_cv(X_masked, y, PILOT_XGB_CONFIG, 'exp1_masking')`.
5. Calls `fit_full_model(X_masked, y, PILOT_XGB_CONFIG)` for importance.
6. Calls `get_named_importances(model, list(FEATURE_COLUMNS))`.
7. Computes comparison_to_baseline: count of positions where loo_predictions differs from
   baseline_result['loo_predictions']. Only counts positions without "FOLD_ERROR".
8. Assembles and writes result dict (see format below).
9. Returns the result dict.

Output format (pilot_exp1_masking.json):
```json
{
  "experiment": "exp1_masking",
  "n_samples": 20,
  "n_features": 54,
  "masking_stats": {
    "avg_features_zeroed": 36.4,
    "min_features_zeroed": 34,
    "max_features_zeroed": 39
  },
  "loo_true_labels": [...],
  "loo_predictions": [...],
  "n_fold_failures": 0,
  "feature_importance": [...],
  "top20_features": [...],
  "comparison_to_baseline": {
    "n_predictions_differ": N,
    "hands_that_differ": ["situation_id_1", ...]
  },
  "notes": ["Zero conflation: 0 values may be structural (facing_bet=0) not masked"]
}
```
`hands_that_differ` must list the situation_ids (not indices) of diverging predictions.
The Programmer loads the situation_id order from `pilot_20_enriched.jsonl` to map index to id.

### Function: run_exp2_weighting()

```python
def run_exp2_weighting(baseline_result: dict, output_path: str) -> dict:
```

Runs Experiment 2 (attention-weighted features).
1. Loads `pilot_20_attention_levels.csv`:
   `load_feature_csv(LEVELS_CSV, level_col_names + list(FEATURE_COLUMNS), None)`
   where `level_col_names = ['level_' + f for f in FEATURE_COLUMNS]`.
   Actually, loads the 54 original features and 54 level columns separately.
   Call: `load_feature_csv(LEVELS_CSV, list(FEATURE_COLUMNS), 'label')` for X and y.
   Then separately load the level columns: `load_feature_csv(LEVELS_CSV, ['level_' + f for f in FEATURE_COLUMNS], None)` for W (shape 20x54).
2. Compute X_weighted: `X_weighted = X * W` (element-wise multiplication).
   X_weighted has the same shape as X (20, 54).
3. Calls `run_loo_cv(X_weighted, y, PILOT_XGB_CONFIG, 'exp2_weighting')`.
4. Calls `fit_full_model(X_weighted, y, PILOT_XGB_CONFIG)`.
5. Calls `get_named_importances(model, list(FEATURE_COLUMNS))`.
6. Computes comparison_to_baseline.
7. Computes the "top10 attention alignment" check: extracts the top-10 features by
   importance in exp2, computes their average attention level weight. Also computes
   the average attention level weight for baseline's top-10. Reports both.
   A feature's average attention level weight = mean of its W column across 20 rows.
8. Assembles and writes result dict.

Output format (pilot_exp2_weighting.json):
```json
{
  "experiment": "exp2_weighting",
  "n_samples": 20,
  "n_features": 54,
  "loo_true_labels": [...],
  "loo_predictions": [...],
  "n_fold_failures": 0,
  "feature_importance": [...],
  "top20_features": [...],
  "comparison_to_baseline": { "n_predictions_differ": N, "hands_that_differ": [...] },
  "attention_alignment": {
    "exp2_top10_avg_weight": 0.72,
    "baseline_top10_avg_weight": 0.65,
    "top10_in_attention_union": ["feat1", "feat2", ...],
    "note": "Are exp2 top10 features higher-weighted than baseline top10?"
  },
  "notes": [
    "XGBoost rank-ordering invariance: multiplying continuous features by 0.1 may not change tree splits",
    "Binary feature distortion: is_made_hand*0.1 = 0.1 vs is_made_hand*1.0 = 1.0"
  ]
}
```

### Function: run_exp3_auxiliary()

```python
def run_exp3_auxiliary(baseline_result: dict, output_path: str) -> dict:
```

Runs Experiment 3 (auxiliary attention flags).
1. Loads `pilot_20_attention.csv`. The column set is:
   54 original feature columns (FEATURE_COLUMNS) + 54 `attn_*` columns + `label`.
   Full feature list for XGBoost: `list(FEATURE_COLUMNS) + ['attn_' + f for f in FEATURE_COLUMNS]`.
   Call: `load_feature_csv(ATTENTION_CSV, list(FEATURE_COLUMNS) + ['attn_' + f for f in FEATURE_COLUMNS], 'label')`
   This gives X of shape (20, 108).
2. Column names list (length 108): `list(FEATURE_COLUMNS) + ['attn_' + f for f in FEATURE_COLUMNS]`.
3. Uses `PILOT_XGB_CONFIG` with `colsample_bytree=1.0` (all columns eligible — verify config has this).
4. Calls `run_loo_cv(X, y, PILOT_XGB_CONFIG, 'exp3_auxiliary')`.
5. Calls `fit_full_model(X, y, PILOT_XGB_CONFIG)`.
6. Calls `get_named_importances(model, column_names_108)`.
7. Splits importance into original_54 and attn_54 subsets.
8. Computes: how many `attn_*` columns have non-zero importance?
9. Computes: are any `attn_*` columns in the top-20 by importance?

Owner amendment 3: For each `attn_*` flag with non-zero importance, records:
- The flag's feature name (e.g. "attn_equity_vs_range")
- Its importance score
- The corresponding original feature name (e.g. "equity_vs_range")
- The original feature's importance score
This directly answers "does XGBoost learn to use expert attention signals?"

10. Computes comparison_to_baseline (comparing against 54-feature baseline predictions).
11. Assembles and writes result dict.

Output format (pilot_exp3_auxiliary.json):
```json
{
  "experiment": "exp3_auxiliary",
  "n_samples": 20,
  "n_features": 108,
  "loo_true_labels": [...],
  "loo_predictions": [...],
  "n_fold_failures": 0,
  "feature_importance_all108": [...],
  "top20_features": [...],
  "original_54_importance": [...],
  "attn_54_importance": [...],
  "nonzero_attn_flags": [
    {
      "attn_feature": "attn_equity_vs_range",
      "attn_importance": 0.045,
      "original_feature": "equity_vs_range",
      "original_importance": 0.112
    }
  ],
  "n_attn_flags_nonzero": N,
  "any_attn_in_top20": true,
  "comparison_to_baseline": { "n_predictions_differ": N, "hands_that_differ": [...] },
  "notes": [
    "With 20 samples and 108 features, model is massively underdetermined",
    "Near-constant attn flags (tagged 17+/20 hands) will have low discriminative importance"
  ]
}
```

### Function: run_exp4_intentions()

```python
def run_exp4_intentions(output_path: str) -> dict:
```

Runs Experiment 4 (intention prediction, Model 2).
1. Loads `pilot_20_intentions.csv`.
   Feature columns: `list(FEATURE_COLUMNS)` (54 columns).
   Target columns: all `intent_*` columns in the CSV (discovered at load time).
   Load features: `load_feature_csv(INTENTIONS_CSV, list(FEATURE_COLUMNS), None)` for X (20x54).
   Load targets separately: read the CSV header, identify all columns starting with `intent_`,
   load them as a numpy int32 matrix Y of shape (20, N_tags).
2. Tag list: the `intent_*` column names in sorted order.
3. For each tag i, compute: positive_count = sum of Y[:, i].
4. Logs tag frequency for each tag (owner amendment 2 discovery reporting).
5. Trains MultiOutputClassifier(XGBClassifier(**BINARY_XGB_CONFIG)) on full data (all 20).
   This fits one binary XGBClassifier per tag.
6. Runs LOO CV for multi-label:
   - Use `sklearn.model_selection.LeaveOneOut`.
   - For each fold: fit `MultiOutputClassifier(XGBClassifier(**BINARY_XGB_CONFIG))` on
     X[train], Y[train]. Predict on X[test]. Append prediction row to loo_matrix.
   - loo_matrix shape: (20, N_tags) after all folds.
7. Per-tag evaluation:
   - is_nontrivial[tag]: True if loo_matrix[:, i] has any 1s (not all-zero).
8. Per-tag feature importance (from full-data model):
   For each estimator in MultiOutputClassifier.estimators_:
     extract feature_importances_, pair with FEATURE_COLUMNS.
9. Compares per-tag top features against baseline top features:
   For each tag: do the top-3 features differ from baseline top-3?
10. Assembles and writes result dict.

Output format (pilot_exp4_intentions.json):
```json
{
  "experiment": "exp4_intentions",
  "n_samples": 20,
  "n_features": 54,
  "tag_list": ["intent_bluff_fold_better", "intent_continue_draw", ...],
  "tag_frequencies": {
    "intent_bluff_fold_better": {"positive_count": 2, "pct": 10.0},
    "intent_continue_draw": {"positive_count": 4, "pct": 20.0},
    ...
  },
  "loo_predictions_per_tag": {
    "intent_continue_draw": [0, 0, 1, ...],
    ...
  },
  "per_tag_results": {
    "intent_continue_draw": {
      "positive_count": 4,
      "loo_predicted_positive": 2,
      "is_nontrivial": true,
      "feature_importance": [
        {"feature": "draw_outs", "importance": 0.21},
        ...
      ],
      "top3_features": ["draw_outs", "improvement_probability", "has_flush_draw"],
      "differs_from_baseline_top3": true
    }
  },
  "n_nontrivial_tags": N,
  "mechanical_success": true,
  "notes": [
    "Tags with <=2 positive examples will collapse to all-zero (majority class)",
    "Multi-output LOO: 20 folds x N_tags binary models x 50 trees each"
  ]
}
```

### Function: build_comparison_report()

```python
def build_comparison_report(
    baseline: dict,
    exp1: dict,
    exp2: dict,
    exp3: dict,
    exp4: dict,
    output_path: str,
) -> dict:
```

Builds `pilot_experiment_comparison.json`.

1. Per-hand comparison table: for each of the 20 hands (by situation_id), records:
   - true_label
   - baseline prediction
   - exp1 prediction
   - exp2 prediction
   - exp3 prediction

2. Per-experiment summary:
   - n_predictions_differ (vs baseline)
   - spearman_rho_importance: Spearman correlation between baseline feature importances
     and the experiment's feature importances (for the 54 original features only).
     Use `scipy.stats.spearmanr` on the two importance vectors.
   - mechanical_success: true/false (derived from presence of "FOLD_ERROR" count
     and whether experiment-specific success criteria were met)

3. Exp3 attention signal section (owner amendment 3):
   - Lists each attn_* flag with non-zero importance from exp3['nonzero_attn_flags']
   - States whether any appeared in top-20
   - Direct answer to "does XGBoost learn to use expert attention signals?"

4. Ranking of experiments by prediction divergence from baseline (most divergent first).

Output format (pilot_experiment_comparison.json):
```json
{
  "n_hands": 20,
  "per_hand_predictions": [
    {
      "situation_id": "d4534_BB_flop",
      "true_label": "CHECK",
      "baseline": "CHECK",
      "exp1_masking": "CHECK",
      "exp2_weighting": "CHECK",
      "exp3_auxiliary": "CHECK"
    },
    ...
  ],
  "experiment_summary": {
    "exp1_masking": {
      "n_predictions_differ": 3,
      "spearman_rho_importance": 0.82,
      "mechanical_success": true
    },
    "exp2_weighting": { ... },
    "exp3_auxiliary": { ... }
  },
  "attention_signal_finding": {
    "nonzero_attn_flags": [
      {
        "attn_feature": "attn_equity_vs_range",
        "attn_importance": 0.045,
        "original_feature": "equity_vs_range",
        "original_importance": 0.112
      }
    ],
    "n_nonzero": N,
    "any_in_top20": true,
    "conclusion": "XGBoost [did/did not] learn to use expert attention signals at 20 samples"
  },
  "ranking_by_divergence": ["exp1_masking", "exp3_auxiliary", "exp2_weighting"],
  "most_divergent_experiment": "exp1_masking"
}
```

### Function: main()

```python
def main() -> None:
```

Orchestrates in this exact order:
1. Verify all 4 CSV source files exist. If any are missing, print
   "ERROR: Run assemble_pilot_data.py first" and exit(1).
2. `os.makedirs(RESULTS_DIR, exist_ok=True)`
3. Print "Running Baseline (Exp 0)..."
4. `baseline = run_baseline(f'{RESULTS_DIR}/pilot_exp0_baseline.json')`
5. Print "Running Experiment 1: Feature Masking..."
6. `exp1 = run_exp1_masking(baseline, f'{RESULTS_DIR}/pilot_exp1_masking.json')`
7. Print "Running Experiment 2: Attention Weighting..."
8. `exp2 = run_exp2_weighting(baseline, f'{RESULTS_DIR}/pilot_exp2_weighting.json')`
9. Print "Running Experiment 3: Auxiliary Flags..."
10. `exp3 = run_exp3_auxiliary(baseline, f'{RESULTS_DIR}/pilot_exp3_auxiliary.json')`
11. Print "Running Experiment 4: Intention Prediction..."
12. `exp4 = run_exp4_intentions(f'{RESULTS_DIR}/pilot_exp4_intentions.json')`
13. Print "Building comparison report..."
14. `build_comparison_report(baseline, exp1, exp2, exp3, exp4, f'{RESULTS_DIR}/pilot_experiment_comparison.json')`
15. Print summary table:
    ```
    Experiment   | N predictions differ | Spearman rho | Success
    Baseline     | —                    | —            | YES
    Exp1 Masking | N                    | 0.xx         | YES/NO
    Exp2 Weight  | N                    | 0.xx         | YES/NO
    Exp3 Aux     | N                    | 0.xx         | YES/NO
    Exp4 Intent  | N/A                  | N/A          | YES/NO
    ```
16. Print "ALL EXPERIMENTS COMPLETE"

---

## Section 5: File 3 — tests/test_attention_experiments.py

**Path:** `/home/rupertbeytell/river-rats-v2/river-rats-core/tests/test_attention_experiments.py`

**Purpose:** Tests written BEFORE implementation. Each test defines a contract that
the implementation must satisfy. Run with `python3 -m pytest tests/test_attention_experiments.py`
from the `river-rats-core/` directory.

All tests are unit tests using synthetic data. Tests must NOT depend on
`/tmp/pilot_situations.json`, the CSV files in training-data/, or the results/ directory.
Tests that depend on those files are integration tests (flagged as such with
`pytest.mark.integration` and skipped by default).

### Test file structure

```python
import sys
import os
import json
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from gto_model import FEATURE_COLUMNS, ACTION_CLASSES

# Import functions under test (these will fail until implemented)
from assemble_pilot_data import (
    parse_untagged_features_file,
    validate_attention_levels,
    validate_intention_tags,
    build_enriched_record,
    LEVEL_WEIGHTS,
)
from run_attention_experiments import (
    load_feature_csv,
    run_loo_cv,
    apply_masking,
    get_named_importances,
)
```

### Tests for assemble_pilot_data.py

#### test_feature_columns_count

Asserts that `len(FEATURE_COLUMNS) == 54`.
This is the contract the entire pipeline depends on.

#### test_action_classes_order

Asserts that `ACTION_CLASSES == ('FOLD', 'CHECK', 'CALL', 'BET', 'RAISE')`.
The integer encoding is baked into results files — order must not change.

#### test_level_weights_values

Asserts that:
- `LEVEL_WEIGHTS['PRIMARY'] == 1.0`
- `LEVEL_WEIGHTS['CONFIRMED'] == 0.7`
- `LEVEL_WEIGHTS['DISCOVERED'] == 0.5`
- `LEVEL_WEIGHTS['Untagged'] == 0.1`

#### test_build_enriched_record_flags

Creates a synthetic situation dict with `situation_id = 'test_hand'` and a feat_dict
containing all 54 FEATURE_COLUMNS with value 1.0.
Creates untagged_features = {FEATURE_COLUMNS[0], FEATURE_COLUMNS[1]} (first 2 features).

Calls `build_enriched_record(situation, 'CHECK', untagged_features)`.

Asserts:
- result['attention_flags'][FEATURE_COLUMNS[0]] == 0  (untagged)
- result['attention_flags'][FEATURE_COLUMNS[1]] == 0  (untagged)
- result['attention_flags'][FEATURE_COLUMNS[2]] == 1  (tagged)
- result['n_tagged'] == 52
- result['label'] == 'CHECK'

#### test_build_enriched_record_levels

Same setup as above, but also sets a module-level ATTENTION_LEVELS for the test_hand:
`{FEATURE_COLUMNS[2]: 'PRIMARY', FEATURE_COLUMNS[3]: 'CONFIRMED', FEATURE_COLUMNS[4]: 'DISCOVERED'}`.

Asserts:
- result['attention_levels'][FEATURE_COLUMNS[2]] == 1.0  (PRIMARY)
- result['attention_levels'][FEATURE_COLUMNS[3]] == 0.7  (CONFIRMED)
- result['attention_levels'][FEATURE_COLUMNS[4]] == 0.5  (DISCOVERED)
- result['attention_levels'][FEATURE_COLUMNS[0]] == 0.1  (untagged)

#### test_build_enriched_record_missing_feature

Creates a feat_dict with one FEATURE_COLUMNS key missing.
Asserts that `build_enriched_record` raises `ValueError`.

#### test_validate_intention_tags_bad_tag

Creates a mock vocab dict with known valid tags.
Calls `validate_intention_tags` with INTENTION_TAGS containing one invalid tag string.
Asserts that `ValueError` is raised.

#### test_validate_attention_levels_conflict

Creates a minimal ATTENTION_LEVELS with one feature.
Creates an untagged_map where that same feature is listed as untagged for that hand.
Calls `validate_attention_levels(untagged_map)`.
Asserts that `ValueError` is raised (a feature cannot be both tagged and untagged).

### Tests for run_attention_experiments.py

#### test_load_feature_csv_shape

Writes a temporary CSV file with 20 rows and columns matching FEATURE_COLUMNS + 'label'.
Calls `load_feature_csv(tmp_path, list(FEATURE_COLUMNS), 'label')`.
Asserts X.shape == (20, 54).
Asserts y.shape == (20,).
Asserts y.dtype == np.int32.

#### test_load_feature_csv_wrong_n_rows

Writes a temporary CSV with 19 rows.
Asserts that `load_feature_csv` raises `ValueError` (n_rows != 20).

#### test_load_feature_csv_missing_column

Writes a CSV missing one feature column.
Asserts that `load_feature_csv` raises `ValueError`.

#### test_apply_masking_zeros_correct_features

Creates synthetic X of shape (3, 4) where all values are 1.0.
Creates column_names = ['a', 'b', 'c', 'd'].
Creates untagged_per_hand = [{'b', 'c'}, {'a'}, {'d'}].

Calls `apply_masking(X_copy, column_names, untagged_per_hand)`.

Asserts:
- X_masked[0, 0] == 1.0  (feature 'a', not untagged for row 0)
- X_masked[0, 1] == 0.0  (feature 'b', untagged for row 0)
- X_masked[0, 2] == 0.0  (feature 'c', untagged for row 0)
- X_masked[0, 3] == 1.0  (feature 'd', not untagged for row 0)
- X_masked[1, 0] == 0.0  (feature 'a', untagged for row 1)
- X_masked[2, 3] == 0.0  (feature 'd', untagged for row 2)

Asserts stats_dict['avg_features_zeroed'] == 2.0 (2+1+1 / 3).
Asserts original X is NOT modified (masking must work on a copy).

#### test_apply_masking_does_not_mutate_input

Creates X and X_copy (np.copy).
Calls apply_masking with X.
Asserts `np.array_equal(X, X_copy)` — input not mutated.

#### test_get_named_importances_length

Creates a mock model with a `feature_importances_` attribute of length 5.
Calls `get_named_importances(model, ['a', 'b', 'c', 'd', 'e'])`.
Asserts len(result) == 5.
Asserts result is sorted descending by importance.

#### test_get_named_importances_mismatch

Creates mock model with feature_importances_ of length 5.
Calls `get_named_importances(model, ['a', 'b', 'c'])` (3 names for 5 importances).
Asserts `ValueError` is raised.

#### test_run_loo_cv_n_predictions

Creates synthetic X (20x4) and y (20,) with values 0-4 cycling.
Calls `run_loo_cv(X, y, PILOT_XGB_CONFIG_SUBSET, 'test')` where the config uses
`num_class=5` and a fast config (n_estimators=5).
Asserts `len(loo_predictions) == 20`.
Asserts `len(true_labels) == 20`.
Asserts all values in loo_predictions are either in ACTION_CLASSES or == "FOLD_ERROR".

#### test_run_loo_cv_returns_strings

Same as above. Asserts that loo_predictions contains strings, not integers.

#### test_run_loo_cv_fold_failure_handling

Creates X (20x4) and y where one class has only 1 sample (guarantees a degenerate fold).
Calls `run_loo_cv(X, y, config, 'test')`.
Asserts that the function does NOT raise an exception even if some folds fail.
Asserts n_fold_failures >= 0 (function returns a count, not None).

### Integration test (skipped by default)

#### test_assemble_produces_correct_files

```python
@pytest.mark.integration
def test_assemble_produces_correct_files():
```

Calls `main()` from assemble_pilot_data (with monkeypatched paths).
Asserts that all 5 output files are created.
Asserts pilot_20_base.csv has 20 data rows and 55 columns.
Asserts pilot_20_attention.csv has 109 columns.
Asserts pilot_20_attention_levels.csv has 109 columns.
Asserts pilot_20_intentions.csv has 54 + N_tags columns.
Asserts pilot_20_enriched.jsonl has 20 lines, each valid JSON.

---

## Section 6: Data row ordering contract

The ordering of rows in all 4 CSVs and in pilot_20_enriched.jsonl must be identical.
The canonical order is the order of `situation_id` as they appear in
`/tmp/pilot_situations.json` (the input file order, not alphabetical).

This order is:
```
0:  d4534_BB_flop
1:  d7760_BTN_flop
2:  d6384_BTN_turn
3:  d6066_BB_flop
4:  d5046_CO_flop
5:  d6826_CO_turn
6:  d1971_HJ_river
7:  d2285_BTN_river
8:  d6533_BTN_river
9:  d1200_HJ_turn
10: BP1_22
11: BP2_35
12: BP3_03
13: BP4_28
14: BP5_02
15: BP6_01
16: BP7_03
17: BP2_36
18: BP2_42
19: BP5_05
```

The experiment runner uses index-based access to the enriched JSONL for per-hand
comparison. This order must not change between assembly and experiments.

---

## Section 7: Dependency graph

```
tests/test_attention_experiments.py
  -> assemble_pilot_data.py (imports)
  -> run_attention_experiments.py (imports)
  -> gto_model.py (imports FEATURE_COLUMNS, ACTION_CLASSES)

assemble_pilot_data.py
  -> gto_model.py (FEATURE_COLUMNS, ACTION_CLASSES)
  -> /tmp/pilot_situations.json (read)
  -> /tmp/pilot_v2_consensus.json (read)
  -> review/comms/PILOT_V2_UNTAGGED_FEATURES_2026-04-14.txt (read)
  -> training-data/tag_vocabulary.json (read)
  -> ATTENTION_LEVELS (hardcoded in this file)
  -> INTENTION_TAGS (hardcoded in this file)
  Writes:
  -> training-data/pilot_20_enriched.jsonl
  -> training-data/pilot_20_base.csv
  -> training-data/pilot_20_attention.csv
  -> training-data/pilot_20_attention_levels.csv
  -> training-data/pilot_20_intentions.csv

run_attention_experiments.py
  -> gto_model.py (FEATURE_COLUMNS, ACTION_CLASSES)
  -> training-data/pilot_20_base.csv (Exp 0, 1)
  -> training-data/pilot_20_attention_levels.csv (Exp 2)
  -> training-data/pilot_20_attention.csv (Exp 3)
  -> training-data/pilot_20_intentions.csv (Exp 4)
  -> training-data/pilot_20_enriched.jsonl (Exp 1, for untagged_per_hand and situation_id order)
  Writes:
  -> results/pilot_exp0_baseline.json
  -> results/pilot_exp1_masking.json
  -> results/pilot_exp2_weighting.json
  -> results/pilot_exp3_auxiliary.json
  -> results/pilot_exp4_intentions.json
  -> results/pilot_experiment_comparison.json
```

---

## Section 8: External library requirements

The Programmer must verify these are importable before writing any code:
- `xgboost` (for XGBClassifier)
- `sklearn.model_selection` (LeaveOneOut, MultiOutputClassifier via sklearn.multioutput)
- `sklearn.multioutput.MultiOutputClassifier`
- `scipy.stats.spearmanr`
- `numpy`
- `json`, `csv`, `os`, `sys` (stdlib)

No additional libraries are permitted. If `shap` is needed for owner amendment 3,
the Programmer must check it is available first. The blueprint specifies that
the attention signal finding in Exp 3 uses feature_importances_ (not SHAP) to answer
owner amendment 3. This avoids the SHAP dependency.

---

## Section 9: Stop conditions for the Programmer

Stop and report BLOCKED if any of the following occur:

1. `/tmp/pilot_situations.json` contains anything other than exactly 20 records
   or any record is missing a `feat_dict` key.
2. `/tmp/pilot_v2_consensus.json` contains anything other than exactly 20 entries
   or any action string is not in ACTION_CLASSES.
3. The untagged features file cannot be parsed to yield exactly 20 hand blocks
   with valid feature names.
4. `validate_attention_levels()` or `validate_intention_tags()` fails — do not
   manually patch the hardcoded tables to pass validation. Report the conflict.
5. Any test fails for a reason that indicates the blueprint spec is wrong
   (e.g., FEATURE_COLUMNS has a different length than 54).
6. XGBoost raises an error on the 108-column input in Exp 3 that is not a
   per-fold LOO error — this would indicate a version incompatibility.
7. `scipy.stats.spearmanr` is not available.

---

## Section 10: Implementation order

The Programmer must implement in this exact order:

1. Write `tests/test_attention_experiments.py` — all tests must FAIL initially (imports fail).
2. Implement `assemble_pilot_data.py` with hardcoded ATTENTION_LEVELS and INTENTION_TAGS.
3. Run assembly: `python3 river-rats-core/assemble_pilot_data.py` from repo root.
4. Verify all 5 output files exist and have correct dimensions. Print the verification summary.
5. Implement `run_attention_experiments.py`.
6. Run experiments: `python3 river-rats-core/run_attention_experiments.py` from repo root.
7. Run tests: `python3 -m pytest river-rats-core/tests/test_attention_experiments.py -v`
8. Write all 6 results files to `results/`.
9. Write a brief results report to `review/comms/RESULTS_FEATURE_ATTENTION_TRAINING_2026-04-14.md`.

The Programmer must NOT run experiments before assembly completes successfully.
The Programmer must NOT modify gto_model.py, train_model.py, or any other existing file.
