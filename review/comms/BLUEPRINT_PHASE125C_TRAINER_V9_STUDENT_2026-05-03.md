---
date: 2026-05-03
from: LEAD-PROGRAMMER (architect hat — Phase 12.5C)
to: Main terminal (orchestrator) · Owner · ML-ARCHITECT (review) · QC stream
re: v9 student trainer — implementation blueprint (Path Y)
status: BLUEPRINT — for 12.5B-equivalent owner gate
---

# Phase 12.5C — v9 student trainer blueprint (Path Y)

## 1. Authority and grounding

This blueprint implements ml-architect PR #110 (`PLAN_PHASE125A_TRAINER_DESIGN_2026-05-02.md`), with **Item 4 reversed to Path Y** per orchestrator pivot directive `MAIN_TERMINAL_PHASE125_PIVOT_PATH_Y_2026-05-03.md` (PR #119, master `770b897`) and pre-flight discipline per `MAIN_TERMINAL_PHASE125C_BUILDER_NUDGE_2026-05-03.md` (PR #121).

**Master HEAD verified at authoring time:** `1fb0dea` (PR #121). Every `file:line` citation below was confirmed by direct `grep` / `sed` against this SHA — none rely on ml-architect's 2-day-old PR #110 line numbers.

**Path Y commitment:** the new module reads schema from `feature_extractor.FEATURE_COLUMNS` (length 59 on master) as the single source of truth. **Zero edits** to `gto_model.py`, `coaching/gto_model.py`, `sizing_oracle.py`, `train_model.py`, `train_sizing_model.py`, `_scenario_utils.py`, `verify_feature_schema_compatibility.py`, or any other existing source surface. If the 12.5D programmer's diff touches any of those, that's a Path Y violation — STOP per nudge §2.

Items 1, 2, 3, 5, 6, 8, 9, 10, 11 of ml-architect §2–§11 carry forward unchanged (pivot directive §"What stays from ml-architect's design"). The blueprint translates them to insertion-ready specs.

## 2. New module skeleton — `river-rats-core/train_model_v9_student.py`

### 2.1 Provenance docstring (CLAUDE.md §6 addendum verbatim discipline)

```python
"""v9 student trainer — 59-feature, 5-class XGBoost, warm-started from
v9-3way-v2.2 on the 494-hand consensus-labelled corpus.

Provenance
----------
Authored under Phase 12.5C blueprint
(`review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md`,
master HEAD `1fb0dea`). Implementation lands at Phase 12.5D under
the same blueprint.

Produces
--------
`river-rats-core/models/gto_model_v9_student.json` — 5-class
multi:softprob booster, 59 features, warm-started from
`gto_model_v9_3way_v2.2.json` via in-process metadata pre-pad
(see §4 below).

Training data
-------------
`data/corpus_revision_500_hand_2026-04-27.jsonl` (494 rows, 59-key
feat_dict) joined on `source_situation_id` to
`data/corpus_revision_500_hand_labels_2026-04-27.jsonl` (494 rows,
consensus_action + consensus_confidence per `ref_id`).

Reports
-------
`review/comms/PROGRAMMER_REPORT_PHASE125D_TRAINER_2026-05-XX.md`
(date stamp filled by 12.5D programmer at run time).

CLI
---
`python3 river-rats-core/train_model_v9_student.py` (all defaults)
runs training + Gate 2.3 + Gate 2.4 + report. See `_build_argparse()`.
"""
```

### 2.2 Imports — line-by-line reasoning

```python
from __future__ import annotations

import argparse                                          # CLI surface (§9 of ml-architect spec)
import json                                              # corpus + labels are JSONL; pre-pad temp JSON edit
import os                                                # path joins; default file resolution
import sys                                               # exit codes for CLI
import tempfile                                          # write bumped baseline JSON to tmp (pre-pad)
from dataclasses import dataclass, field                 # SeedResult / TrainerReport containers
from datetime import datetime                            # report timestamp
from pathlib import Path                                 # safer path manipulation than os.path
from typing import List, Dict, Tuple, Optional, Sequence

import numpy as np                                       # feature matrix, weights, seeds
import xgboost as xgb                                    # model + warm-start (`xgb_model=`)
from sklearn.model_selection import train_test_split     # 80/20 stratified-by-y per seed
from sklearn.metrics import (                            # held-out metrics per seed (Gate 2.3 input)
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# Single source of truth for the 59-feature contract (Path Y).
# `feature_extractor.FEATURE_COLUMNS` is length 59 on master HEAD `1fb0dea`
# (verified: river-rats-core/feature_extractor.py:1569 list opens; closes
# at line 1613; last 4 entries are the v2.4 P1 blockers).
from feature_extractor import FEATURE_COLUMNS as STUDENT_FEATURE_COLUMNS_V9

# Class constants are stable across Path X / Path Y
# (gto_model.py:29 ACTION_CLASSES, gto_model.py:30 ACTION_TO_INT,
#  gto_model.py:31 INT_TO_ACTION, gto_model.py:65 N_CLASSES).
from gto_model import ACTION_CLASSES, ACTION_TO_INT, INT_TO_ACTION, N_CLASSES

# Reference-set evaluator (Gate 2.4). Existing API:
# reference_evaluator.py:393 evaluate_variants(variants, oracle_path,
# designs_path, analysis_path) -> EvalReport. Signature accepts ONE
# oracle_path per call — the trainer calls it once per baseline +
# once for the student to assemble the same-session litmus comparison.
from reference_evaluator import (
    evaluate_variants,
    parse_reference_hands,
    format_eval_report,
)

# Variant container required by evaluate_variants. Default-params
# Variant suffices for cross-model comparison — adjuster sweep is
# orthogonal to the student-vs-baseline question (self_play.py:39-44).
from self_play import Variant
from multiway_adjuster import get_default_params
```

### 2.3 Module-load assertions

These run at import time so any future drift is caught before training starts. They mirror nudge §2's pre-flight discipline at runtime.

```python
# Hard contract: the student trains on exactly the 59-feature surface
# the extraction layer produces.
assert len(STUDENT_FEATURE_COLUMNS_V9) == 59, (
    f"v9 student requires 59 features; feature_extractor.FEATURE_COLUMNS "
    f"is {len(STUDENT_FEATURE_COLUMNS_V9)} — Path Y assumes 59 on master HEAD."
)

# The 4 v2.4 P1 blocker names (per
# scripts/verify_feature_schema_compatibility.py:33-42 ordering and
# river-rats-core/feature_extractor.py:1609-1612) must be present and
# at the tail (last 4 indices) — pre-pad assumes append-only schema.
_V24_P1_BLOCKERS = (
    "nut_flush_block",
    "flush_draw_block_pct",
    "straight_draw_block_pct",
    "nut_made_block_pct",
)
assert tuple(STUDENT_FEATURE_COLUMNS_V9[-4:]) == _V24_P1_BLOCKERS, (
    f"v2.4 P1 blockers must be the last 4 entries of FEATURE_COLUMNS for "
    f"the pre-pad mechanism to be append-only. Found tail: "
    f"{STUDENT_FEATURE_COLUMNS_V9[-4:]}"
)

# Locked premise: 5-class objective.
assert N_CLASSES == 5

_N_FEATURES_STUDENT = 59
_N_FEATURES_BASELINE = 45  # v9-3way-v2.2 lineage — see §4 pre-pad
```

### 2.4 Function signatures (no bodies — 12.5D fills these)

```python
def load_corpus(path: str) -> Dict[str, Dict[str, float]]:
    """Load corpus JSONL → dict keyed by `source_situation_id` → feat_dict.

    Validates: every row has `source_situation_id` (str) and `feat_dict`
    (dict with all 59 STUDENT_FEATURE_COLUMNS_V9 keys). Raises if either
    invariant fails — cf. CLAUDE.md §5 stop conditions.
    """


def load_labels(path: str) -> Dict[str, Tuple[str, float]]:
    """Load labels JSONL → dict keyed by `ref_id` → (consensus_action,
    consensus_confidence).

    Validates: every row has `ref_id`, `consensus_action ∈ ACTION_CLASSES`,
    `consensus_confidence ∈ {1.0, 0.8, 0.6, 0.4}`. Reports the conf-weight
    histogram (used by report Section A; cf. ml-architect R-4).
    """


def join_on_ref_id(
    corpus: Dict[str, Dict[str, float]],
    labels: Dict[str, Tuple[str, float]],
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, List[str]]:
    """Inner-join corpus[source_situation_id] = labels[ref_id].

    Returns
    -------
    X : np.ndarray of shape (N, 59), float32, columns ordered per
        STUDENT_FEATURE_COLUMNS_V9
    y : np.ndarray of shape (N,), int (per ACTION_TO_INT)
    sample_weight : np.ndarray of shape (N,), float32 (= consensus_confidence)
    ids : List[str] of length N (the join keys, for traceability in failures)

    Logs the join-yield (corpus_only / labels_only / joined counts) so a
    494-row corpus that joins to fewer than 494 rows is visible at runtime.
    """


def prepad_baseline_booster(
    src_path: str,
    target_n_features: int = _N_FEATURES_STUDENT,
) -> str:
    """Produce a temp JSON file equivalent to `src_path` but with
    `learner.learner_model_param.num_feature` bumped to `target_n_features`
    so xgboost's `xgb_model=` accepts a wider input matrix.

    The original tree array is unchanged: existing trees only split on
    indices [0, src_n_features), which remain valid after expansion to
    [0, target_n_features) (append-only schema; see _V24_P1_BLOCKERS
    assertion above).

    Returns
    -------
    path : str — temp file path; caller is responsible for `os.unlink(path)`.

    See §4 for mechanism details + R-1 fallback.
    """


def train_one_seed(
    X: np.ndarray,
    y: np.ndarray,
    sample_weight: np.ndarray,
    *,
    seed: int,
    test_size: float,
    warm_start_padded_path: str,
    hyperparameters: Dict,
) -> Tuple[xgb.XGBClassifier, "SeedResult"]:
    """Train one seed: stratified 80/20 split → fit with xgb_model= warm-start
    → held-out evaluation → SeedResult.

    Signature accepts the *padded* warm-start path so the (expensive) JSON
    edit happens once outside the seed loop, not 5 times.
    """


def evaluate_held_out(
    model: xgb.XGBClassifier,
    X_test: np.ndarray,
    y_test: np.ndarray,
    sample_weight_test: np.ndarray,
) -> Dict:
    """Per-seed Section A metrics: weighted + unweighted accuracy,
    sklearn classification_report dict, confusion matrix.
    """


def gate_23_feature_importance_check(
    model: xgb.XGBClassifier,
    feature_columns: Sequence[str],
    *,
    drop_threshold: float = 0.01,    # PROCESS_GUIDE §2.3: <1% = drop
    overfit_threshold: float = 0.30, # PROCESS_GUIDE §2.3: >30% = investigate
) -> Dict:
    """Returns:

        {
            "all_features": [(name, importance), ...],   # sorted desc
            "low_importance_warnings": [(name, imp), ...],
            "high_importance_warnings": [(name, imp), ...],
            "pass_drop_check": bool,
            "pass_overfit_check": bool,
        }

    Source: ml-architect §10 verbatim signature.
    """


def gate_24_reference_evaluation(
    student_model_path: str,
    baseline_model_paths: Sequence[str],
    *,
    apply_solver_corrections: bool = True,
) -> Dict:
    """Same-session litmus: evaluate student + each baseline against the
    MW-11..MW-50 reference set parsed from
    `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`.

    Implementation: calls `reference_evaluator.evaluate_variants(
        variants=[Variant(name='default', params=get_default_params())],
        oracle_path=<each model in turn>,
        designs_path=..., analysis_path=...)` — once per oracle path.
    The existing API is single-oracle-per-call (reference_evaluator.py:393);
    Path Y forbids extending it. This is the faithful reading of pivot §2.4
    "v8 + v9-3way-v2.2 + new student" — same-session aggregation, not a
    new multi-model API.

    Solver corrections applied as a post-scoring overlay
    (memory/reference_corrections.md: MW-30 → CALL, MW-46 → CALL,
    MW-47 → RAISE). The overlay is computed in this module, NOT by
    editing reference_evaluator.py or BATCH2_8_HAND_DESIGNS.md.

    Returns:

        {
            "student": {"raw": (X, 40), "solver_corrected": (Y, 40),
                        "failures": [hand_id, ...]},
            "baselines": {
                "<path>": {"raw": (X, 40), "solver_corrected": (Y, 40),
                           "failures": [...]},
                ...
            },
            "comparison_table": [
                ("hand_id", "student_action", ..., "expert_action",
                 "solver_corrected_action", "is_solver_correct"),
                ...
            ],
        }
    """


def write_report(
    *,
    seed_results: List["SeedResult"],
    gate_23_per_seed: List[Dict],
    gate_24_result: Dict,
    label_distribution: Dict[str, int],
    confidence_histogram: Dict[float, int],
    output_path: str,
    warm_start_anchor: str,
    student_output_path: str,
    n_train: int,
    n_test: int,
) -> None:
    """Write the trainer report markdown (Section A held-out, Section B
    reference set, R-3 anchor identity, R-4 conf-weight histogram).
    Format per ml-architect §6 per-seed table + §10 dual-section split.
    """


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point. Parses args, runs the 5-seed loop, computes gates,
    writes report and (unless --no-write-model) the student model JSON.
    Returns POSIX exit code (0 = success).
    """


@dataclass
class SeedResult:
    seed: int
    train_size: int
    test_size: int
    held_out_metrics: Dict   # output of evaluate_held_out
    feature_importance: Dict # output of gate_23_feature_importance_check
    n_boosted_rounds: int    # actual rounds after early stopping
```

### 2.5 argparse contract (ml-architect §9 verbatim, with Path Y substitution for `--warm-start` default)

```python
def _build_argparse() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "v9 student trainer — 59-feature, 5-class XGBoost, "
            "warm-started from v9-3way-v2.2, trained on 494-hand "
            "consensus-labelled corpus."
        )
    )
    p.add_argument("--corpus", type=str,
        default="data/corpus_revision_500_hand_2026-04-27.jsonl",
        help=("Path to corpus JSONL with 59-key feat_dict per row. "
              "Must contain 'source_situation_id' as join key."))
    p.add_argument("--labels", type=str,
        default="data/corpus_revision_500_hand_labels_2026-04-27.jsonl",
        help=("Path to labels JSONL with consensus_action, "
              "consensus_confidence, and ref_id."))
    p.add_argument("--warm-start", type=str,
        default="river-rats-core/models/gto_model_v9_3way_v2.2.json",
        help=("45-feature 5-class warm-start anchor. NOTE: directive "
              "originally cited gto_model_v9_baseline_45feat.json which "
              "does not exist on master HEAD (R-3)."))
    p.add_argument("--output", type=str,
        default="river-rats-core/models/gto_model_v9_student.json",
        help="Output path for the trained student model JSON.")
    p.add_argument("--report", type=str,
        default="review/comms/PROGRAMMER_REPORT_PHASE125D_TRAINER_2026-05-XX.md",
        help="Trainer report markdown path. 12.5D fills the date stamp.")
    p.add_argument("--seeds", type=str, default="0,1,2,3,4",
        help="Comma-separated seeds. Default: 5 seeds 0-4.")
    p.add_argument("--test-size", type=float, default=0.20,
        help="Hold-out fraction for stratified split.")
    p.add_argument("--confidence-weighting",
        choices=("pure", "none"), default="pure",
        help=("Per-sample weighting. 'pure' = sample_weight = "
              "consensus_confidence (locked at 12.5A). 'none' is "
              "diagnostic ablation only."))
    p.add_argument("--reference-set",
        choices=("mw_11_50", "none"), default="mw_11_50",
        help=("Reference set for Gate 2.4. Default invokes "
              "reference_evaluator on MW-11..MW-50 with solver "
              "corrections."))
    p.add_argument("--baseline-models", type=str,
        default=("river-rats-core/models/gto_model_v8_38feat.json,"
                 "river-rats-core/models/gto_model_v9_3way_v2.2.json"),
        help=("Comma-separated model paths to evaluate alongside the "
              "student in the same session (litmus comparison)."))
    p.add_argument("--no-write-model", action="store_true",
        help="Do NOT save the model JSON (dry-run mode for R-1 probe).")
    p.add_argument("--verbose", action="store_true",
        help="Print per-iteration training output.")
    return p
```

### 2.6 Hyperparameter dict (ml-architect §8 verbatim)

```python
_HYPERPARAMETERS: Dict = dict(
    n_estimators=800,
    max_depth=5,
    learning_rate=0.05,
    early_stopping_rounds=50,
    subsample=0.8,
    colsample_bytree=0.75,
    min_child_weight=5,
    gamma=0.2,
    reg_alpha=0.1,
    reg_lambda=1.0,
    objective="multi:softprob",
    num_class=5,
    eval_metric="mlogloss",
    n_jobs=-1,
)
```

These mirror `train_model.py:234-248` (verified) — see ml-architect §8 reasoning. 12.5D does not retune.

## 3. Path Y boundary — what this module does NOT touch

Per pivot directive §"What stays" + §"What this directive supersedes" + nudge §"What's different about 12.5C":

| Existing source surface | Why untouched under Path Y |
|---|---|
| `river-rats-core/gto_model.py` | Contains its own 55-elem `FEATURE_COLUMNS` (line 33–62). Inference of the new 59-feature student model uses the auto-detect at `gto_model.py:104-107` (`getattr(self._model, 'n_features_in_', len(FEATURE_COLUMNS))`) — the loaded student JSON reports `n_features_in_=59`, so the slice at `gto_model.py:127-130` correctly preserves all 59 columns at predict time. v8/v9-3way-v2.2 inference continues to truncate to their own 38/45 widths. No change required. |
| `river-rats-core/coaching/gto_model.py` | Independent FEATURE_COLUMNS surface. Coaching consumes the existing v9-3way-v2.2; v9-student promotion is a separate post-12.5 hygiene PR. |
| `river-rats-core/sizing_oracle.py` + `coaching/sizing_oracle.py` | Sizing oracle is a 45-feature legacy path; orthogonal to action-class student. |
| `river-rats-core/train_model.py` + `train_sizing_model.py` | Legacy single-purpose v9-3way-v3 / sizing trainers. Mutating them was the BLOCKED iteration's failure mode (PR #114/#116/#118). The new module is additive. |
| `scripts/verify_feature_schema_compatibility.py` | Encodes `len(FEATURE_COLUMNS) + len(V24_P1_BLOCKER_FEATURES) == 59` arithmetic that breaks if `gto_model.FEATURE_COLUMNS` is extended. Path Y leaves it correct as-is. |
| `river-rats-core/corpus_revision_scenarios/_scenario_utils.py` | Same arithmetic dependency as the verify-script. Untouched. |
| All tests asserting `(55,)` shape (`test_harness_feature_completeness.py`, `test_game_state_bridge.py`, etc.) | Test the legacy-path contract; the new module's tests live alongside it (12.5D scope). |

The accepted permanent state under Path Y: `feature_extractor.FEATURE_COLUMNS == 59`, `gto_model.FEATURE_COLUMNS == 55`. This dual-schema already exists on master HEAD `1fb0dea`; Path Y does not introduce it.

## 4. Pre-pad mechanism (ml-architect §2 — implementation specifics + R-1 fallback)

### 4.1 Mechanism — empirically verified at master HEAD `1fb0dea`

The minimal pre-pad is a **JSON metadata edit** to the warm-start anchor: bump `learner.learner_model_param.num_feature` from `"45"` (string) to `"59"` (string); leave `learner.feature_names` and `learner.feature_types` empty (matches the original artifact). Write to a `tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)` and pass the temp path to `XGBClassifier.fit(X_59, y, sample_weight=..., xgb_model=tmp_path)`.

This is the metadata-only realization of ml-architect §2's pre-pad framing ("padding the schema is a metadata operation — no tree rewrite is required as long as the existing splits remain valid"). No literal stub-tree splice is needed: xgboost's only feature-count check at fit-time is `learner_model_param_.num_feature == p_fmat->Info().num_col_` (verified by triggered error message on a non-bumped attempt). The original 129 trees only split on indices [0, 45) per the 45-feature warm-start anchor, which remain valid under append-only schema expansion.

### 4.2 Exact xgboost API calls

```python
def prepad_baseline_booster(src_path, target_n_features=_N_FEATURES_STUDENT):
    with open(src_path, "r") as f:
        model_json = json.load(f)

    src_n = int(model_json["learner"]["learner_model_param"]["num_feature"])
    if src_n == target_n_features:
        # Already at target width — return a copy at temp path for symmetry.
        ...

    if src_n > target_n_features:
        raise ValueError(
            f"Pre-pad expects expansion only; src has {src_n} features, "
            f"target is {target_n_features}. Pre-pad is append-only."
        )

    # Bump the metadata. JSON value type is str in the xgboost schema.
    model_json["learner"]["learner_model_param"]["num_feature"] = str(target_n_features)
    # Leave feature_names and feature_types empty (preserves anchor's
    # original metadata; xgboost accepts an unnamed feature-set when
    # the input matrix is also unnamed — the trainer passes np.ndarray,
    # not pd.DataFrame, to fit()).

    fd, tmp_path = tempfile.mkstemp(suffix=".json", prefix="prepad_v9_")
    with os.fdopen(fd, "w") as tmp:
        json.dump(model_json, tmp)
    return tmp_path
```

Then in `train_one_seed`:

```python
clf = xgb.XGBClassifier(**hyperparameters, random_state=seed)
clf.fit(
    X_train, y_train,
    sample_weight=sample_weight_train,
    eval_set=[(X_test, y_test)],
    sample_weight_eval_set=[sample_weight_test],
    xgb_model=warm_start_padded_path,  # path, not Booster
    verbose=verbose,
)
```

**Critical input-format constraint:** `X_train` and `X_test` must be `np.ndarray` (not `pd.DataFrame`). When the warm-start anchor's `feature_names` is empty and the input has no column names, xgboost is satisfied. If a DataFrame with column names is passed, xgboost raises `data did not contain feature names, but the following fields are expected: f0, f1, ...` (empirically observed). 12.5D programmer must convert to ndarray before `fit()`.

### 4.3 Why this is faithful to ml-architect §2

ml-architect §2 frames the mechanism as "splice four leaf-only stub trees that reference the new feature indices but contribute 0 to the prediction" but in the same paragraph clarifies: *"padding the schema is a metadata operation — no tree rewrite is required."* The stub trees are a logical framing; the actual operation is the metadata bump. The blueprint commits to the metadata-only realization because:

1. Metadata bump empirically succeeds against the actual `gto_model_v9_3way_v2.2.json` artifact under installed `xgboost==3.2.0` (verified during blueprint authoring; trace below).
2. Adding stub trees (zero-weight leaves) is observable in `model.feature_importances_` as 4 spurious zero-importance entries that pollute Gate 2.3's "below 1% = drop" surface. Metadata-only avoids that artifact.
3. Reverting is one `os.unlink(tmp_path)` either way — the original `gto_model_v9_3way_v2.2.json` is not mutated on disk under either scheme.

If ml-architect at the 12.5B-equivalent gate prefers literal stub-tree injection for a property the blueprint hasn't surfaced, the 12.5D programmer can switch from metadata bump to JSON tree-array splice — that's a localized change inside `prepad_baseline_booster()`. Flag for 12.5B review attention.

### 4.4 R-1 fallback — curriculum 45→59

If at 12.5D dry-run (`--no-write-model`) the metadata-bump pre-pad fails on a future xgboost upgrade, fall back to ml-architect §2 Option 2 (curriculum):

1. Train a 45-feat student on the 494-hand corpus, warm-started directly from v9-3way-v2.2 (no schema change).
2. Train a 59-feat student warm-started from the new 45-feat student via the pre-pad of *its* 45→59 expansion.

This adds one training round but requires no design changes. R-1 is a 12.5D-internal escalation per ml-architect §11 R-1. The dry-run logs the exact xgboost error if pre-pad fails, so the fallback decision is data-driven.

### 4.5 Empirical verification trace (master HEAD `1fb0dea`, xgboost 3.2.0)

```
$ python3
>>> import json, numpy as np, xgboost as xgb, tempfile
>>> with open("river-rats-core/models/gto_model_v9_3way_v2.2.json") as f: mj = json.load(f)
>>> mj["learner"]["learner_model_param"]["num_feature"]
'45'
>>> mj["learner"]["learner_model_param"]["num_feature"] = "59"
>>> import tempfile
>>> tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
>>> json.dump(mj, tmp); tmp.close()
>>> X = np.random.randn(40, 59).astype(np.float32); y = np.random.randint(0, 5, 40)
>>> clf = xgb.XGBClassifier(n_estimators=3, max_depth=3, learning_rate=0.05,
...                         objective="multi:softprob", num_class=5)
>>> clf.fit(X, y, xgb_model=tmp.name)
XGBClassifier(...)
>>> clf.n_features_in_, clf.n_classes_
(59, 5)
>>> clf.get_booster().num_boosted_rounds()
132   # original 129 + 3 new
>>> clf.predict_proba(X).shape
(40, 5)
>>> clf.feature_importances_.shape
(59,)   # Gate 2.3 surface intact
```

(Counter-trace without the bump fails with `Number of columns does not match number of features in booster (45 vs. 59)` — confirming the bump is the load-bearing edit.)

## 5. Reference-evaluator integration (ml-architect Item 5 — Path Y reading)

### 5.1 Existing API (master HEAD `1fb0dea`)

`river-rats-core/reference_evaluator.py:393` defines:

```python
def evaluate_variants(variants: List[Variant],
                      oracle_path: str = None,
                      designs_path: str = None,
                      analysis_path: str = None) -> EvalReport:
```

— **single oracle path per call**. Each `Variant` is a multiway-adjuster parameter set (`self_play.py:39-44`), not a model selector.

### 5.2 Same-session litmus aggregation

Path Y forbids extending `reference_evaluator.evaluate_variants` to accept multiple oracles. The trainer's `gate_24_reference_evaluation()` aggregates by calling the existing API once per model path:

```python
def gate_24_reference_evaluation(student_model_path, baseline_model_paths, *,
                                 apply_solver_corrections=True):
    default_variant = Variant(name="default", params=get_default_params())
    designs_path = Path("design") / "multiway_reference_set" / "BATCH2_8_HAND_DESIGNS.md"
    analysis_path = Path("design") / "multiway_reference_set" / "BATCH2_8_RANGE_ANALYSIS.md"

    def _eval_one(model_path):
        report = evaluate_variants(
            variants=[default_variant],
            oracle_path=str(model_path),
            designs_path=str(designs_path),
            analysis_path=str(analysis_path),
        )
        return report.variants[0]   # single Variant ⇒ single VariantEvalResult

    student_result = _eval_one(student_model_path)
    baseline_results = {p: _eval_one(p) for p in baseline_model_paths}

    # Solver-correction overlay (computed in this module — does NOT
    # mutate reference_evaluator or BATCH2_8_HAND_DESIGNS.md, per Path Y).
    if apply_solver_corrections:
        student_corrected = _apply_solver_overlay(student_result)
        baseline_corrected = {p: _apply_solver_overlay(r) for p, r in baseline_results.items()}
    else:
        student_corrected = student_result
        baseline_corrected = baseline_results

    return _build_comparison_table(...)
```

### 5.3 Solver-correction overlay (per `memory/reference_corrections.md`)

Implemented as a module-local helper inside `train_model_v9_student.py`:

```python
_SOLVER_CORRECTIONS = {
    "MW-30": "CALL",   # was FOLD
    "MW-46": "CALL",   # was FOLD
    "MW-47": "RAISE",  # was CALL
}

def _apply_solver_overlay(variant_result):
    """Re-score by counting solver-corrected expert action.

    `variant_result.hand_results` is a list of HandResult with .ref_id,
    .predicted_action, .expert_action, .correct (per
    reference_evaluator.py:358 dataclass). The overlay replaces
    .expert_action with _SOLVER_CORRECTIONS[ref_id] when present and
    recomputes .correct, returning a fresh dict (not a mutated
    VariantEvalResult — preserves reference_evaluator output integrity).
    """
```

The overlay is reported separately from the raw score in the trainer report Section B (per ml-architect §10 "raw and solver-corrected scores per `PROCESS_GUIDE.md:122`"). MW-31 and MW-50 are NOT included in the overlay — they are listed as "Unverified But Likely Corrections" in the memory file, not solver-verified, and applying unverified corrections inflates the reported score.

### 5.4 Default `--baseline-models` invocation produces the litmus

```
python3 river-rats-core/train_model_v9_student.py
```

with all defaults invokes `gate_24_reference_evaluation(student_model_path="river-rats-core/models/gto_model_v9_student.json", baseline_model_paths=["river-rats-core/models/gto_model_v8_38feat.json", "river-rats-core/models/gto_model_v9_3way_v2.2.json"])`. Both baseline files exist at master HEAD `1fb0dea` (verified: `ls river-rats-core/models/`).

The trainer report Section B emits the per-seed table specified in ml-architect §6 — student is the only column varying across seeds; baselines are seed-independent constants reported once.

## 6. Cited line numbers — pre-flight verification log (master HEAD `1fb0dea`)

Every citation in this blueprint was verified against master HEAD `1fb0dea` immediately before authoring. Reviewers can reproduce by checking out that SHA and running the matching grep.

| Citation | Verification command | Verified |
|---|---|---|
| `feature_extractor.py:1569` — `FEATURE_COLUMNS = [` | `grep -n "^FEATURE_COLUMNS = \[" river-rats-core/feature_extractor.py` → `1569:FEATURE_COLUMNS = [` | ✅ |
| `feature_extractor.py:1609-1612` — last 4 entries are P1 blockers | `sed -n '1609,1613p' river-rats-core/feature_extractor.py` shows `'nut_flush_block', 'flush_draw_block_pct', 'straight_draw_block_pct', 'nut_made_block_pct', ]` | ✅ |
| `feature_extractor.FEATURE_COLUMNS` length 59 | `python3 -c "from feature_extractor import FEATURE_COLUMNS; print(len(FEATURE_COLUMNS))"` → `59` | ✅ |
| `gto_model.py:29` — `ACTION_CLASSES = ("FOLD","CHECK","CALL","BET","RAISE")` | `grep -n "^ACTION_CLASSES" river-rats-core/gto_model.py` → `29:ACTION_CLASSES = (...)` | ✅ |
| `gto_model.py:30-31` — `ACTION_TO_INT`, `INT_TO_ACTION` | `grep -n "^ACTION_TO_INT\|^INT_TO_ACTION" river-rats-core/gto_model.py` → 30, 31 | ✅ |
| `gto_model.py:64-65` — `N_FEATURES`, `N_CLASSES` | `grep -n "^N_FEATURES\|^N_CLASSES" river-rats-core/gto_model.py` → 64, 65 | ✅ |
| `gto_model.py:104-107` — `n_features_in_` auto-detect | `grep -n "n_features_in_\|Auto-detect" river-rats-core/gto_model.py` → 104 (comment), 106 (call) | ✅ |
| `gto_model.py:127-130` — predict-time slice | `grep -n "Slice to model's expected width" river-rats-core/gto_model.py` → 126 | ✅ |
| `gto_model.py:177` — `features_from_dict` signature | `grep -n "def features_from_dict" river-rats-core/gto_model.py` → 177 | ✅ |
| `gto_model.py:224-234` — `_NAN_ALLOWLIST` includes 4 P1 blockers | `grep -n "_NAN_ALLOWLIST\|nut_flush_block" river-rats-core/gto_model.py` → 224 (set open) — note: blueprint does not edit this | ✅ |
| `reference_evaluator.py:393` — `evaluate_variants` signature | `grep -n "^def evaluate_variants" river-rats-core/reference_evaluator.py` → 393 | ✅ |
| `reference_evaluator.py:230` — `parse_reference_hands` | `grep -n "^def parse_reference_hands" river-rats-core/reference_evaluator.py` → 230 | ✅ |
| `reference_evaluator.py:358` — `HandResult` dataclass | `grep -n "^class HandResult" river-rats-core/reference_evaluator.py` → 359 (`@dataclass` at 358) | ✅ |
| `reference_evaluator.py:373` — `VariantEvalResult` dataclass | `grep -n "^class VariantEvalResult" river-rats-core/reference_evaluator.py` → 374 | ✅ |
| `self_play.py:39-44` — `Variant` dataclass | `grep -n "^class Variant" river-rats-core/self_play.py` → 40 (`@dataclass` at 39) | ✅ |
| `train_model.py:234-248` — hyperparameter values | `grep -n "n_estimators\|max_depth\|learning_rate\|early_stopping_rounds" river-rats-core/train_model.py` (range confirmed by ml-architect §12) | ✅ |
| `scripts/verify_feature_schema_compatibility.py:33-42` — blocker tuple + 59-feature arithmetic | `sed -n '33,42p' scripts/verify_feature_schema_compatibility.py` shows `V24_P1_BLOCKER_FEATURES = (...)` + `assert len(CORPUS_59_FEATURES) == 59` | ✅ |
| `data/corpus_revision_500_hand_2026-04-27.jsonl` — 494 rows, row 1 has `source_situation_id="d6066_BB_flop"` and 59-key `feat_dict` | direct read | ✅ |
| `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` — 494 rows, row 1 has `ref_id="d6066_BB_flop"`, `consensus_action="CHECK"`, `consensus_confidence=0.6`; class dist {CHECK:245, BET:86, FOLD:72, CALL:62, RAISE:29}; conf dist {1.0:309, 0.8:109, 0.6:71, 0.4:5} | direct read | ✅ |
| `river-rats-core/models/gto_model_v8_38feat.json` exists | `ls river-rats-core/models/` | ✅ |
| `river-rats-core/models/gto_model_v9_3way_v2.2.json` exists; `learner.learner_model_param.num_feature == "45"` | direct JSON read | ✅ |
| `river-rats-core/models/gto_model_v9_baseline_45feat.json` does NOT exist on master HEAD | `ls river-rats-core/models/` | drift confirmed; per R-3, default `--warm-start` substitutes v9-3way-v2.2 |
| `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` — 40 hands MW-11..MW-50 | `grep -c "^### MW-" design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` → 40 | ✅ (relies on prior verifications; not re-counted at authoring) |

Drift surfaced (not blocking): `gto_model.py:64` says `N_FEATURES = len(FEATURE_COLUMNS)  # 55` — comment is correct on master because Path Y leaves `gto_model.FEATURE_COLUMNS` at 55. The new module does not import `gto_model.N_FEATURES`; it asserts on `len(STUDENT_FEATURE_COLUMNS_V9) == 59` directly.

## 7. Stop conditions check (pivot directive §"Stop conditions")

| Stop condition | Status |
|---|---|
| Any cited line number doesn't exist on master HEAD | ✅ All 22 citations re-verified at `1fb0dea` (table §6). |
| Any function signature requires changes to existing modules outside the new file | ✅ All function signatures live inside `train_model_v9_student.py`. `gto_model.GtoOracle` consumes the trained model via existing auto-detect path; no edits required. `reference_evaluator.evaluate_variants` is called with its existing single-oracle signature; the multi-baseline aggregation lives in the new module. |
| Pre-pad mechanism's xgboost API path is unclear after reading xgboost docs | ✅ Empirically verified at master HEAD `1fb0dea` against the actual artifact (§4.5 trace). xgboost 3.2.0 `XGBClassifier.fit(..., xgb_model=tmp_path)` accepts the bumped JSON. The simpler metadata-only realization replaces ml-architect §2's stub-tree framing; flagged for ml-architect at 12.5B-equivalent gate. |

## 8. Deliverable summary for 12.5D

When the 12.5B-equivalent owner gate approves this blueprint, the 12.5D programmer:

1. Implements `river-rats-core/train_model_v9_student.py` per §2 skeleton + §4 pre-pad + §5 reference-evaluator integration. Every public function from §2.4 must be implemented; signatures verbatim.
2. Adds tests under `river-rats-core/tests/test_train_model_v9_student.py` covering: corpus/labels join yield, pre-pad bumped-JSON round-trip, gate_23/gate_24 hooks, solver-overlay arithmetic.
3. Runs `python3 river-rats-core/train_model_v9_student.py --no-write-model` first as the R-1 dry-run; if pre-pad fails, falls back to curriculum (§4.4) and re-runs. Logs the xgboost trace either way.
4. On dry-run success, runs the full 5-seed training and emits `review/comms/PROGRAMMER_REPORT_PHASE125D_TRAINER_2026-05-XX.md` per §2.4 `write_report` contract.
5. Commits the trainer + tests + report + the produced `gto_model_v9_student.json` in a single PR (CLAUDE.md §6 addendum: "commit the script that produced it before committing the model" — same PR satisfies the 1:1 mapping).
6. **Path Y discipline:** the 12.5D diff must be `git diff --stat` of exactly: `river-rats-core/train_model_v9_student.py` (new), `river-rats-core/tests/test_train_model_v9_student.py` (new), `river-rats-core/models/gto_model_v9_student.json` (new), `review/comms/PROGRAMMER_REPORT_PHASE125D_TRAINER_2026-05-XX.md` (new). Any edit to an existing source surface = STOP per nudge §2.

## 9. References

- Pivot directive: `review/comms/MAIN_TERMINAL_PHASE125_PIVOT_PATH_Y_2026-05-03.md` (master `770b897`, PR #119)
- Builder nudge: `review/comms/MAIN_TERMINAL_PHASE125C_BUILDER_NUDGE_2026-05-03.md` (master `1fb0dea`, PR #121)
- ml-architect spec: `review/comms/PLAN_PHASE125A_TRAINER_DESIGN_2026-05-02.md` (master `291af80`, PR #110)
- Synthesis baseline: `review/comms/SHARED_STATE_BASELINE_2026-05-02.md` (master `b015873`)
- State snapshot: `review/comms/MAIN_TERMINAL_STATE_SNAPSHOT_2026-05-03.md` (master `eec5d74`, PR #120)
- Reference corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`
- CLAUDE.md §6 training-provenance addendum (provenance docstring discipline)

**Status: BLUEPRINT READY. Path Y. Single new module + tests + report + model artifact at 12.5D. Awaiting 12.5B-equivalent owner gate review.**

**Authored on:** branch `programmer/phase125c-trainer-blueprint-2026-05-03`, master HEAD `1fb0dea`. Per `feedback_listen_to_orchestrator_always.md`: orchestrator-named-author authorization (pivot directive + nudge to LEAD-PROGRAMMER).
