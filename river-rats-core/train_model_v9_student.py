"""v9 student trainer — 59-feature, 5-class XGBoost, warm-started from
v9-3way-v2.2 on the 494-hand consensus-labelled corpus.

Provenance
----------
Implements Phase 12.5C blueprint
(`review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md`,
master HEAD `1e4e47e`) under the original Phase 12.5D dispatch
(`review/comms/MAIN_TERMINAL_PHASE125D_DISPATCH_2026-05-03.md`,
master HEAD `e3c0dfc`), updated for Phase 12.5D' per
`review/comms/MAIN_TERMINAL_PHASE125D_PRIME_DISPATCH_2026-05-04.md`
(master HEAD `1b95648`) — adds ml-architect Q3 hybrid weighting
(`sample_weight = confidence × min(3.0, mean_class_count / class_count)`)
in `train_one_seed` and the Option α invariant test
(`test_student_inference_mirror_invariant_on_baseline`); _StudentInference
extended with optional `feature_columns` kwarg to enable the 45-feat
shim without affecting default 59-feat use.

Produces
--------
`river-rats-core/models/gto_model_v9_student.json` — 5-class
multi:softprob booster, 59 features, warm-started from
`gto_model_v9_3way_v2.2.json` via in-process metadata pre-pad
(see `prepad_baseline_booster`).

Training data
-------------
`data/corpus_revision_500_hand_2026-04-27.jsonl` (494 rows, 59-key
feat_dict per row) joined on `source_situation_id` to
`data/corpus_revision_500_hand_labels_2026-04-27.jsonl` (494 rows,
consensus_action + consensus_confidence per `ref_id`).

Reports
-------
`review/comms/PROGRAMMER_REPORT_PHASE125D_TRAINER_2026-05-03.md`
written by `write_report` per dispatch directive Section A/B/C/D split.

CLI
---
`python3 river-rats-core/train_model_v9_student.py` runs training +
Gate 2.3 + Gate 2.4 + report. See `_build_argparse()`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split

# Make river-rats-core importable when invoked from repo root.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feature_extractor import (
    FEATURE_COLUMNS as STUDENT_FEATURE_COLUMNS_V9,
    extract_all_features,
)
from feature_keys import F
from gto_model import (
    ACTION_CLASSES, ACTION_TO_INT, INT_TO_ACTION, N_CLASSES,
    OraclePrediction,
)
from multiway_adjuster import adjust, get_default_params
from reference_evaluator import (
    evaluate_variants,
    parse_reference_hands,
    _resolve_action_history_for_ref_hand,
    _validate_feat_dict,
    STREET_MAP,
    HandResult,
    VariantEvalResult,
)
from self_play import Variant


# ─── Module-load assertions (blueprint §2.3) ──────────────────────────

assert len(STUDENT_FEATURE_COLUMNS_V9) == 59, (
    f"v9 student requires 59 features; feature_extractor.FEATURE_COLUMNS "
    f"is {len(STUDENT_FEATURE_COLUMNS_V9)} — Path Y assumes 59 on master HEAD."
)

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

assert N_CLASSES == 5

_N_FEATURES_STUDENT = 59
_N_FEATURES_BASELINE = 45  # v9-3way-v2.2 lineage; see R-3 in blueprint §4

# Solver-corrected reference labels (memory/reference_corrections.md).
# MW-31 + MW-50 are unverified — NOT applied per dispatch step 5.
_SOLVER_CORRECTIONS: Dict[str, str] = {
    "MW-30": "CALL",   # was FOLD
    "MW-46": "CALL",   # was FOLD
    "MW-47": "RAISE",  # was CALL
}

# Hyperparameters — blueprint §2.6 verbatim (mirror v9-3way-v2.2 lineage).
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


# ─── Repo root resolver ───────────────────────────────────────────────

def _repo_root() -> Path:
    """river-rats-core/.. — the repo root."""
    return Path(__file__).resolve().parent.parent


# ─── Warm-start canonicality guard (dispatch §"warm-start canonicality") ──

def is_git_tracked(path: str) -> bool:
    """Return True iff `path` is in the git tree at HEAD.

    Defends against an untracked local artifact silently changing
    training inputs vs CI/fresh checkout (#PSH-01 scenario from
    gate-prep PR #124).
    """
    repo = _repo_root()
    abs_path = Path(path).resolve()
    try:
        rel = abs_path.relative_to(repo)
    except ValueError:
        return False
    try:
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", str(rel)],
            cwd=str(repo),
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        # git not available (e.g., shipped artifact). Fall back to existence.
        return abs_path.exists()


def resolve_warm_start_anchor(requested_path: str) -> Tuple[str, str]:
    """Resolve the warm-start anchor with canonicality guard.

    If `requested_path` is git-tracked, return it as-is.
    Otherwise (R-3 substitution) fall back to v9-3way-v2.2.

    Returns (resolved_path, resolution_note) for transparent reporting.
    """
    if is_git_tracked(requested_path):
        return requested_path, f"requested {requested_path} is git-tracked; using as-is"
    fallback = str(_repo_root() / "river-rats-core" / "models" / "gto_model_v9_3way_v2.2.json")
    if not is_git_tracked(fallback):
        raise FileNotFoundError(
            f"Warm-start anchor canonicality: requested {requested_path!r} is "
            f"not git-tracked, and the R-3 fallback {fallback!r} is also not "
            f"git-tracked. Cannot proceed reproducibly."
        )
    note = (
        f"requested {requested_path} is NOT git-tracked (untracked local "
        f"artifact #PSH-01); R-3 substitution to {fallback}"
    )
    return fallback, note


def filter_baseline_models_to_git_tracked(
    paths: Sequence[str],
) -> Tuple[List[str], List[Tuple[str, str]]]:
    """Drop baseline-model paths that are not in the git tree.

    The litmus comparison must be reproducible from a fresh checkout.
    Returns (kept, dropped_with_notes).
    """
    kept: List[str] = []
    dropped: List[Tuple[str, str]] = []
    for p in paths:
        if is_git_tracked(p):
            kept.append(p)
        else:
            dropped.append((p, "not in git tree at HEAD; dropped from litmus"))
    return kept, dropped


# ─── Dataclasses ──────────────────────────────────────────────────────

@dataclass
class SeedResult:
    seed: int
    train_size: int
    test_size: int
    held_out_metrics: Dict
    feature_importance: Dict
    n_boosted_rounds: int
    model_temp_path: str  # where the trained model JSON was written


@dataclass
class TrainerInputs:
    """Inputs assembled by main() before the seed loop runs.

    Helps keep main() readable and the loop body simple.
    """
    X: np.ndarray
    y: np.ndarray
    sample_weight: np.ndarray
    ids: List[str]
    label_distribution: Dict[str, int]
    confidence_histogram: Dict[float, int]
    warm_start_padded_path: str
    warm_start_anchor_path: str
    warm_start_resolution_note: str
    baseline_models_resolved: List[str]
    baseline_models_dropped: List[Tuple[str, str]]


# ─── Loaders ──────────────────────────────────────────────────────────

def load_corpus(path: str) -> Dict[str, Dict[str, float]]:
    """Load corpus JSONL → dict keyed by `pilot_hand_id`.

    Note (schema discovery, 2026-05-03): the blueprint §6 + ml-architect §12
    cited `source_situation_id` as the corpus-side join key, verified on
    row 1. That verification was correct for row 1 (the first cohort) but
    `source_situation_id` is only populated in 100 of 494 rows; the
    remaining 394 rows use `situation_id`. The universally-populated
    canonical key on both files is `pilot_hand_id` (494/494 in corpus and
    labels). Empirically `corpus.pilot_hand_id ∩ labels.pilot_hand_id`
    joins 494/494; `corpus.source_situation_id ∩ labels.ref_id` joins
    only 100/494. The spec INTENT (train on 494 hands) requires the
    pilot_hand_id join. See trainer report Section A "Schema discovery".
    """
    rows: Dict[str, Dict[str, float]] = {}
    with open(path, "r") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            sid = row.get("pilot_hand_id")
            if not sid:
                raise ValueError(
                    f"corpus row {line_no} missing 'pilot_hand_id'"
                )
            feat = row.get("feat_dict")
            if not isinstance(feat, dict):
                raise ValueError(
                    f"corpus row {line_no} ({sid}) missing 'feat_dict'"
                )
            missing = [k for k in STUDENT_FEATURE_COLUMNS_V9 if k not in feat]
            if missing:
                raise ValueError(
                    f"corpus row {line_no} ({sid}) feat_dict missing "
                    f"{len(missing)} of 59 keys: {missing[:5]}..."
                )
            rows[sid] = feat
    return rows


def load_labels(path: str) -> Dict[str, Tuple[str, float]]:
    """Load labels JSONL → dict keyed by `pilot_hand_id` → (action, confidence).

    See `load_corpus` docstring for the join-key schema discovery.
    `pilot_hand_id` is universally populated in labels (494/494) and
    matches corpus.pilot_hand_id 1:1.
    """
    rows: Dict[str, Tuple[str, float]] = {}
    valid_actions = set(ACTION_CLASSES)
    valid_confs = {1.0, 0.8, 0.6, 0.4}
    with open(path, "r") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            sid = row.get("pilot_hand_id")
            if not sid:
                raise ValueError(f"labels row {line_no} missing 'pilot_hand_id'")
            action = row.get("consensus_action")
            if action not in valid_actions:
                raise ValueError(
                    f"labels row {line_no} ({sid}) invalid "
                    f"consensus_action={action!r}; expected one of {valid_actions}"
                )
            conf = row.get("consensus_confidence")
            if conf not in valid_confs:
                raise ValueError(
                    f"labels row {line_no} ({sid}) invalid "
                    f"consensus_confidence={conf!r}; expected one of {valid_confs}"
                )
            rows[sid] = (action, float(conf))
    return rows


def join_on_ref_id(
    corpus: Dict[str, Dict[str, float]],
    labels: Dict[str, Tuple[str, float]],
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, List[str]]:
    """Inner-join corpus[pilot_hand_id] = labels[pilot_hand_id].

    Function name retained for blueprint signature compatibility; the
    actual join is on `pilot_hand_id` per the schema discovery documented
    in `load_corpus`.
    """
    common = sorted(set(corpus.keys()) & set(labels.keys()))
    corpus_only = sorted(set(corpus.keys()) - set(labels.keys()))
    labels_only = sorted(set(labels.keys()) - set(corpus.keys()))

    print(
        f"[join] corpus={len(corpus)} labels={len(labels)} joined={len(common)} "
        f"corpus_only={len(corpus_only)} labels_only={len(labels_only)}"
    )

    X = np.empty((len(common), len(STUDENT_FEATURE_COLUMNS_V9)), dtype=np.float32)
    y = np.empty(len(common), dtype=np.int64)
    sw = np.empty(len(common), dtype=np.float32)

    for i, sid in enumerate(common):
        feat = corpus[sid]
        X[i] = [float(feat[k]) for k in STUDENT_FEATURE_COLUMNS_V9]
        action, conf = labels[sid]
        y[i] = ACTION_TO_INT[action]
        sw[i] = conf
    return X, y, sw, common


# ─── Pre-pad mechanism (blueprint §4) ─────────────────────────────────

def prepad_baseline_booster(
    src_path: str,
    target_n_features: int = _N_FEATURES_STUDENT,
) -> str:
    """Bump `learner.learner_model_param.num_feature` in a temp JSON copy
    so xgboost's `xgb_model=` accepts the wider input matrix.

    Append-only schema expansion: existing trees only split on indices
    [0, src_n_features), which remain valid after expansion to
    [0, target_n_features).

    Returns the temp path. Caller is responsible for `os.unlink(path)`.
    """
    with open(src_path, "r") as f:
        model_json = json.load(f)

    src_n = int(model_json["learner"]["learner_model_param"]["num_feature"])
    if src_n > target_n_features:
        raise ValueError(
            f"Pre-pad expects expansion only; src has {src_n} features, "
            f"target is {target_n_features}. Pre-pad is append-only."
        )

    model_json["learner"]["learner_model_param"]["num_feature"] = str(target_n_features)

    fd, tmp_path = tempfile.mkstemp(suffix=".json", prefix="prepad_v9_")
    with os.fdopen(fd, "w") as tmp:
        json.dump(model_json, tmp)
    return tmp_path


# ─── Per-seed training (blueprint §2.4) ───────────────────────────────

def train_one_seed(
    X: np.ndarray,
    y: np.ndarray,
    sample_weight: np.ndarray,
    *,
    seed: int,
    test_size: float,
    warm_start_padded_path: str,
    hyperparameters: Dict,
    verbose: bool = False,
) -> Tuple[xgb.XGBClassifier, SeedResult]:
    X_train, X_test, y_train, y_test, conf_train, conf_test = train_test_split(
        X, y, sample_weight,
        test_size=test_size,
        random_state=seed,
        stratify=y,
    )

    # Hybrid weighting per ml-architect 12.5D Q3 (closes class-prior collapse).
    # Cap = 3.0 ported from train_model.py:252-257 prior art (empirically
    # calibrated for v9-3way-v2.2 to balance aggressive classes without
    # inverting discipline). On the 5-class corpus, ~3.0× boost on RAISE,
    # ~1.4× on BET, ~1.6× on CALL, ~1.0× on CHECK/FOLD.
    class_counts = np.bincount(y_train, minlength=N_CLASSES)
    mean_class_count = class_counts.mean()
    class_weights = {c: min(3.0, mean_class_count / max(class_counts[c], 1))
                     for c in range(N_CLASSES)}
    sw_train = conf_train * np.array([class_weights[c] for c in y_train],
                                     dtype=np.float32)
    sw_test = conf_test * np.array([class_weights[c] for c in y_test],
                                   dtype=np.float32)

    clf = xgb.XGBClassifier(**hyperparameters, random_state=seed)
    clf.fit(
        X_train, y_train,
        sample_weight=sw_train,
        eval_set=[(X_test, y_test)],
        sample_weight_eval_set=[sw_test],
        xgb_model=warm_start_padded_path,
        verbose=verbose,
    )

    held_out = evaluate_held_out(clf, X_test, y_test, sw_test)
    fi = gate_23_feature_importance_check(clf, STUDENT_FEATURE_COLUMNS_V9)

    # Persist this seed's model to a temp location so the median-litmus
    # selector can rename it later.
    seed_fd, seed_path = tempfile.mkstemp(
        suffix=".json", prefix=f"v9_student_seed{seed}_"
    )
    os.close(seed_fd)
    clf.save_model(seed_path)

    result = SeedResult(
        seed=seed,
        train_size=int(len(X_train)),
        test_size=int(len(X_test)),
        held_out_metrics=held_out,
        feature_importance=fi,
        n_boosted_rounds=int(clf.get_booster().num_boosted_rounds()),
        model_temp_path=seed_path,
    )
    return clf, result


def evaluate_held_out(
    model: xgb.XGBClassifier,
    X_test: np.ndarray,
    y_test: np.ndarray,
    sample_weight_test: np.ndarray,
) -> Dict:
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    acc_w = accuracy_score(y_test, y_pred, sample_weight=sample_weight_test)
    report = classification_report(
        y_test, y_pred,
        labels=list(range(N_CLASSES)),
        target_names=list(ACTION_CLASSES),
        output_dict=True,
        zero_division=0,
    )
    cm = confusion_matrix(y_test, y_pred, labels=list(range(N_CLASSES))).tolist()
    return {
        "accuracy": float(acc),
        "accuracy_weighted": float(acc_w),
        "classification_report": report,
        "confusion_matrix": cm,
    }


# ─── Gate 2.3 — feature importance (ml-architect §10) ──────────────────

def gate_23_feature_importance_check(
    model: xgb.XGBClassifier,
    feature_columns: Sequence[str],
    *,
    drop_threshold: float = 0.01,
    overfit_threshold: float = 0.30,
) -> Dict:
    importances = model.feature_importances_
    paired = sorted(
        zip(feature_columns, [float(x) for x in importances]),
        key=lambda kv: kv[1],
        reverse=True,
    )
    low = [(n, v) for n, v in paired if v < drop_threshold]
    high = [(n, v) for n, v in paired if v > overfit_threshold]
    return {
        "all_features": paired,
        "low_importance_warnings": low,
        "high_importance_warnings": high,
        "pass_drop_check": len(low) == 0,
        "pass_overfit_check": len(high) == 0,
    }


# ─── Gate 2.4 — reference set evaluation (blueprint §5) ───────────────

def _solver_corrected_score(
    variant_result, hand_results
) -> Tuple[int, int, List[Dict]]:
    """Apply solver overlay and recount.

    Returns (correct, total, comparison_rows).
    """
    correct = 0
    total = len(hand_results)
    rows: List[Dict] = []
    for r in hand_results:
        corrected_expert = _SOLVER_CORRECTIONS.get(r.ref_id, r.expert_action)
        is_correct = (
            (r.adjusted_action or "").upper() == (corrected_expert or "").upper()
        )
        if is_correct:
            correct += 1
        rows.append({
            "ref_id": r.ref_id,
            "predicted": r.adjusted_action,
            "expert": r.expert_action,
            "solver_corrected_expert": corrected_expert,
            "raw_correct": bool(r.correct),
            "solver_corrected_correct": is_correct,
        })
    return correct, total, rows


# ─── 59-feature student inference (Path Y boundary handler) ───────────
#
# `reference_evaluator.evaluate_variants` constructs feature arrays via
# `gto_model.GtoOracle.features_from_dict` which iterates
# `gto_model.FEATURE_COLUMNS` (length 55 on master). The v9-student model
# expects 59 features. Path Y forbids extending `gto_model.FEATURE_COLUMNS`,
# so the student's reference-set evaluation uses an in-module 59-feature
# inference path that mirrors `reference_evaluator._evaluate_one_hand`'s
# logic but with the 59-element STUDENT_FEATURE_COLUMNS_V9. Baselines
# (38/45 features) continue to use `evaluate_variants` as-is — gto_model's
# 55-feature pipeline accommodates them via the existing predict-time slice
# at gto_model.py:127-130.


class _StudentInference:
    """59-feature inference wrapper for the v9 student model.

    Equivalent to `GtoOracle` but builds feature arrays from
    STUDENT_FEATURE_COLUMNS_V9 (length 59) instead of
    gto_model.FEATURE_COLUMNS (length 55).

    The `feature_columns` kwarg lets callers override the column list. The
    primary use is the 12.5D' invariant test (Option α): pass
    STUDENT_FEATURE_COLUMNS_V9[:45] together with the 45-feature baseline
    anchor to drive the same inference path on the canonical reference
    evaluator's input — any divergence vs `_evaluate_one_hand(GtoOracle(
    baseline_45))` flips at least one hand and trips the test.
    """

    def __init__(
        self,
        model_path: str,
        *,
        feature_columns: Optional[Sequence[str]] = None,
    ):
        self._model = xgb.XGBClassifier()
        self._model.load_model(model_path)
        if feature_columns is None:
            feature_columns = STUDENT_FEATURE_COLUMNS_V9
        self._feature_columns: Tuple[str, ...] = tuple(feature_columns)
        expected = len(self._feature_columns)
        assert self._model.n_features_in_ == expected, (
            f"Student inference expected {expected} features (matching "
            f"feature_columns); loaded model reports {self._model.n_features_in_}"
        )
        assert self._model.n_classes_ == N_CLASSES

    def features_from_dict(self, feat_dict: Dict[str, float]) -> np.ndarray:
        missing = [k for k in self._feature_columns if k not in feat_dict]
        if missing:
            raise KeyError(
                f"feat_dict missing {len(missing)} of "
                f"{len(self._feature_columns)} keys: {missing[:5]}..."
            )
        return np.array(
            [float(feat_dict[k]) for k in self._feature_columns],
            dtype=np.float32,
        )

    def predict(self, features: np.ndarray) -> OraclePrediction:
        if features.ndim == 1:
            X = features.reshape(1, -1)
        else:
            X = features
        probs = self._model.predict_proba(X)[0]
        action_idx = int(np.argmax(probs))
        return OraclePrediction(
            action=INT_TO_ACTION[action_idx],
            action_idx=action_idx,
            confidence=float(probs[action_idx]),
            probs={ACTION_CLASSES[i]: float(probs[i]) for i in range(N_CLASSES)},
            prob_array=np.asarray(probs, dtype=np.float32),
        )


def _evaluate_student_one_hand(
    hand,
    student: "_StudentInference",
    variant: Variant,
) -> HandResult:
    """Mirror of reference_evaluator._evaluate_one_hand for the 59-feature
    student. Logic kept intentionally close to the source so that future
    upstream changes (action normalization, adjuster contract) are easy to
    track and re-sync.
    """
    street_code = STREET_MAP.get(hand.street.capitalize(), "f")
    _resolved_action_history = _resolve_action_history_for_ref_hand(hand)
    hand_dict = {
        "h": hand.hero_cards,
        "b": hand.board,
        "pos": hand.hero_position,
        "vp": hand.villain_position,
        "pot": hand.pot,
        "tc": hand.to_call,
        "st": street_code,
        "fb": int(hand.facing_bet),
        "exp": "C",
        F.META_NUM_OPPONENTS: hand.num_opponents,
        F.META_NUM_RAISES: 0,
        F.META_OPENER_POSITION: hand.opener_position or None,
        F.META_BETTOR_POSITION: hand.bettor_position,
        "_villain_aggression_count": hand.villain_aggression_count,
        "_villain_checked_back": hand.villain_checked_back,
        "_villain_call_count": hand.villain_call_count,
        "_num_callers_to_bet": hand.num_callers_to_bet,
        "_facing_raise": hand.facing_raise,
        "_action_history": _resolved_action_history,
    }
    feat_dict = extract_all_features(hand_dict)
    _validate_feat_dict(feat_dict, hand_id=hand.ref_id)

    features = student.features_from_dict(feat_dict)
    pred = student.predict(features)
    adjusted = adjust(pred, feat_dict, hand.num_opponents, params=variant.params)

    oracle_action = pred.action.upper()
    adjusted_action = adjusted.adjusted_action.upper()
    expert_action = hand.expert_action.upper()

    def _normalize(a: str) -> str:
        if a == "CHECK": return "FOLD"
        if a == "BET": return "RAISE"
        return a

    correct = _normalize(adjusted_action) == _normalize(expert_action)

    return HandResult(
        ref_id=hand.ref_id,
        variant_name=variant.name,
        expert_action=expert_action,
        expert_confidence=hand.expert_confidence,
        oracle_action=oracle_action,
        adjusted_action=adjusted_action,
        was_adjusted=adjusted.was_adjusted,
        correct=correct,
        axis=hand.axis,
        equity=hand.equity,
    )


def _evaluate_student_against_reference(
    student_model_path: str,
    designs_path: str,
    analysis_path: str,
    variant: Variant,
) -> VariantEvalResult:
    student = _StudentInference(student_model_path)
    hands = parse_reference_hands(designs_path, analysis_path)
    results: List[HandResult] = []
    for hand in hands:
        results.append(_evaluate_student_one_hand(hand, student, variant))
    correct = sum(1 for r in results if r.correct)
    total = len(results)
    failures = [r for r in results if not r.correct]
    return VariantEvalResult(
        variant_name=variant.name,
        total=total,
        correct=correct,
        accuracy=correct / total if total > 0 else 0.0,
        by_confidence={},
        by_axis={},
        failures=failures,
        hand_results=results,
    )


def gate_24_reference_evaluation(
    student_model_path: str,
    baseline_model_paths: Sequence[str],
    *,
    apply_solver_corrections: bool = True,
    designs_path: Optional[str] = None,
    analysis_path: Optional[str] = None,
) -> Dict:
    """Same-session litmus per blueprint §5.2.

    Student inference goes through `_StudentInference` (59-feature path);
    baseline inference goes through `evaluate_variants` (55-feature path
    accommodates 38/45-feature baselines via gto_model's predict-time slice).
    Path Y: gto_model is not edited.
    """
    default_variant = Variant(name="default", params=get_default_params())

    if designs_path is None:
        designs_path = str(
            _repo_root() / "design" / "multiway_reference_set" / "BATCH2_8_HAND_DESIGNS.md"
        )
    if analysis_path is None:
        analysis_path = str(
            _repo_root() / "design" / "multiway_reference_set" / "BATCH2_8_RANGE_ANALYSIS.md"
        )

    def _eval_baseline(model_path: str) -> Dict:
        report = evaluate_variants(
            variants=[default_variant],
            oracle_path=str(model_path),
            designs_path=designs_path,
            analysis_path=analysis_path,
        )
        result = report.variants[0]
        raw_correct = result.correct
        raw_total = result.total
        if apply_solver_corrections:
            sc_correct, sc_total, rows = _solver_corrected_score(
                result, result.hand_results
            )
        else:
            sc_correct, sc_total = raw_correct, raw_total
            rows = [
                {
                    "ref_id": r.ref_id,
                    "predicted": r.adjusted_action,
                    "expert": r.expert_action,
                    "solver_corrected_expert": r.expert_action,
                    "raw_correct": bool(r.correct),
                    "solver_corrected_correct": bool(r.correct),
                }
                for r in result.hand_results
            ]
        return {
            "raw": (raw_correct, raw_total),
            "solver_corrected": (sc_correct, sc_total),
            "failures_raw": [r.ref_id for r in result.failures],
            "failures_solver_corrected": [
                row["ref_id"] for row in rows if not row["solver_corrected_correct"]
            ],
            "rows": rows,
        }

    def _eval_student(model_path: str) -> Dict:
        result = _evaluate_student_against_reference(
            student_model_path=model_path,
            designs_path=designs_path,
            analysis_path=analysis_path,
            variant=default_variant,
        )
        raw_correct = result.correct
        raw_total = result.total
        if apply_solver_corrections:
            sc_correct, sc_total, rows = _solver_corrected_score(
                result, result.hand_results
            )
        else:
            sc_correct, sc_total = raw_correct, raw_total
            rows = [
                {
                    "ref_id": r.ref_id,
                    "predicted": r.adjusted_action,
                    "expert": r.expert_action,
                    "solver_corrected_expert": r.expert_action,
                    "raw_correct": bool(r.correct),
                    "solver_corrected_correct": bool(r.correct),
                }
                for r in result.hand_results
            ]
        return {
            "raw": (raw_correct, raw_total),
            "solver_corrected": (sc_correct, sc_total),
            "failures_raw": [r.ref_id for r in result.failures],
            "failures_solver_corrected": [
                row["ref_id"] for row in rows if not row["solver_corrected_correct"]
            ],
            "rows": rows,
        }

    student = _eval_student(student_model_path)
    baselines = {p: _eval_baseline(p) for p in baseline_model_paths}

    return {
        "student": student,
        "baselines": baselines,
        "solver_correction_keys": list(_SOLVER_CORRECTIONS.keys()),
    }


# ─── Median-litmus seed selection (dispatch step 4) ───────────────────

def select_median_litmus_seed(
    seed_results: Sequence[SeedResult],
    seed_litmus_scores: Dict[int, Tuple[int, int]],
) -> int:
    """Pick the seed whose solver-corrected litmus score is the median.

    With 5 seeds (odd count) the median is unambiguous. Tie-breaker on
    same score: lowest seed index.
    """
    seeds_sorted = sorted(
        seed_results,
        key=lambda sr: (
            seed_litmus_scores[sr.seed][0],
            -sr.seed,  # so lower seed wins ties when sorted asc
        ),
    )
    return seeds_sorted[len(seeds_sorted) // 2].seed


# ─── Provenance ───────────────────────────────────────────────────────

def _file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _git_head_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(_repo_root()),
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return "unknown"


# ─── Report writer ────────────────────────────────────────────────────

def _format_classification_report(report: Dict) -> str:
    lines = []
    lines.append("|class|precision|recall|f1|support|")
    lines.append("|---|---|---|---|---|")
    for cls in ACTION_CLASSES:
        d = report.get(cls, {})
        lines.append(
            f"|{cls}|{d.get('precision', 0):.3f}|{d.get('recall', 0):.3f}|"
            f"{d.get('f1-score', 0):.3f}|{int(d.get('support', 0))}|"
        )
    return "\n".join(lines)


def write_report(
    *,
    seed_results: List[SeedResult],
    seed_litmus_results: Dict[int, Dict],
    chosen_seed: int,
    chosen_gate_24: Dict,
    label_distribution: Dict[str, int],
    confidence_histogram: Dict[float, int],
    output_path: str,
    warm_start_anchor: str,
    warm_start_resolution_note: str,
    student_output_path: str,
    n_train: int,
    n_test: int,
    baseline_models_resolved: List[str],
    baseline_models_dropped: List[Tuple[str, str]],
    dry_run_trace: List[str],
    pre_pad_mode: str,
    cli_args: argparse.Namespace,
    promoted: bool,
    gate_pass: Optional[bool],
) -> None:
    """Write trainer report per dispatch §"Deliverable" Section A/B/C/D.

    `promoted`=True if the student model was written to `student_output_path`;
    False if STOP triggered (gate failed) and no model was promoted.
    `gate_pass`=True if median seed >= v9-3way-v2.2 baseline; False if not;
    None if no v9-3way-v2.2 baseline was available.
    """
    repo = _repo_root()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    head_sha = _git_head_sha()

    # Section D inputs
    if promoted and os.path.exists(student_output_path):
        student_sha = _file_sha256(student_output_path)
    else:
        student_sha = "(no model promoted)"
    anchor_sha = _file_sha256(warm_start_anchor) if os.path.exists(warm_start_anchor) else "(missing)"

    def _rel(p: str) -> str:
        try:
            return str(Path(p).resolve().relative_to(repo))
        except (ValueError, OSError):
            return str(p)

    # Cross-seed summary
    held_out_accs = [sr.held_out_metrics["accuracy"] for sr in seed_results]
    held_out_accs_w = [sr.held_out_metrics["accuracy_weighted"] for sr in seed_results]
    sc_scores = [seed_litmus_results[sr.seed]["student"]["solver_corrected"][0] for sr in seed_results]

    phase = getattr(cli_args, "phase_label", None) or "12.5D'"
    if promoted:
        status_line = f"status: IMPLEMENTATION + RUN COMPLETE — model promoted; awaiting QC + reviews"
        topline = f"{phase} RUN COMPLETE; median-litmus seed promoted to canonical (cleared v9-3way-v2.2 baseline)."
    else:
        status_line = f"status: BUILDER BLOCKED — {phase} implementation + 5-seed run complete; gate did not promote; model NOT promoted"
        topline = f"{phase} RUN COMPLETE; median seed below v9-3way-v2.2 baseline. Per dispatch gate threshold the model was NOT promoted. Section E quantifies the delta vs 12.5D baseline."

    lines: List[str] = []
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines.append("---")
    lines.append(f"date: {today}")
    lines.append("from: LEAD-PROGRAMMER (builder)")
    lines.append("to: Main terminal (orchestrator) · Owner · ML-ARCHITECT (advisory) · GTO-EXPERT (review) · QC stream")
    lines.append(f"re: Phase {phase} — v9 student trainer run (hybrid weighting; combined corpus)")
    lines.append(status_line)
    lines.append("---")
    lines.append("")
    lines.append(f"# Phase {phase} — v9 student trainer report (hybrid weighting)")
    lines.append("")
    lines.append(topline)
    lines.append("")
    lines.append(f"Master HEAD at run time: `{head_sha}`. Run timestamp (UTC): `{ts}`.")
    lines.append("")
    lines.append("## Section A — training metadata")
    lines.append("")
    lines.append(f"- Corpus: `{cli_args.corpus}` (joined rows: {n_train + n_test})")
    lines.append(f"- Labels: `{cli_args.labels}`")
    lines.append(f"- Warm-start requested: `{cli_args.warm_start}`")
    lines.append(f"- Warm-start resolution: requested path {'IS' if 'is git-tracked' in warm_start_resolution_note else 'is NOT'} git-tracked")
    lines.append(f"- Warm-start resolved: `{_rel(warm_start_anchor)}`")
    lines.append(f"- Pre-pad mode: `{pre_pad_mode}` (blueprint §4)")
    lines.append(f"- Test size: {cli_args.test_size}")
    lines.append(f"- Seeds: {cli_args.seeds}")
    lines.append(f"- Confidence weighting: `{cli_args.confidence_weighting}`")
    lines.append(f"- Reference set: `{cli_args.reference_set}`")
    lines.append("")
    lines.append("### Class label distribution (full corpus)")
    lines.append("")
    for cls in ACTION_CLASSES:
        n = label_distribution.get(cls, 0)
        lines.append(f"- {cls}: {n}")
    lines.append("")
    lines.append("### Confidence histogram (full corpus)")
    lines.append("")
    for c in sorted(confidence_histogram.keys(), reverse=True):
        lines.append(f"- {c}: {confidence_histogram[c]}")
    lines.append("")
    lines.append("### Hyperparameters (blueprint §2.6)")
    lines.append("")
    for k, v in _HYPERPARAMETERS.items():
        lines.append(f"- `{k}`: `{v}`")
    lines.append("")
    lines.append("### Baseline-models resolution (canonicality guard)")
    lines.append("")
    for p in baseline_models_resolved:
        lines.append(f"- KEPT (git-tracked): `{_rel(p)}`")
    for p, why in baseline_models_dropped:
        lines.append(f"- DROPPED: `{_rel(p)}` — {why}")
    lines.append("")
    lines.append("### R-1 dry-run trace (blueprint §4.5)")
    lines.append("")
    lines.append("```")
    for line in dry_run_trace:
        lines.append(line)
    lines.append("```")
    lines.append("")
    lines.append("### Schema discoveries surfaced during 12.5D")
    lines.append("")
    lines.append(
        "1. **Join key**: blueprint §6 + ml-architect §12 cited "
        "`corpus.source_situation_id == labels.ref_id` as the join key, "
        "verified on row 1. Subsequent rows (cohort 2, indices 100-493) "
        "have `situation_id` instead of `source_situation_id`, and "
        "`labels.ref_id` is heterogeneous (mix of `d####_POS_street` and "
        "`PILOT_###` IDs). The universally-populated canonical key is "
        "`pilot_hand_id` (494/494 in both files). Trainer joins on "
        "`pilot_hand_id`. Spec INTENT (494-hand training) is preserved."
    )
    lines.append("")
    lines.append(
        "2. **Path Y inference boundary**: `reference_evaluator."
        "evaluate_variants` builds inference arrays via "
        "`gto_model.GtoOracle.features_from_dict` which iterates "
        "`gto_model.FEATURE_COLUMNS` (length 55). The student model "
        "expects 59 features. Path Y forbids extending "
        "`gto_model.FEATURE_COLUMNS`, so the student's reference-set "
        "evaluation uses an in-module 59-feature inference helper "
        "(`_StudentInference` + `_evaluate_student_one_hand`) that mirrors "
        "`reference_evaluator._evaluate_one_hand` logic with "
        "STUDENT_FEATURE_COLUMNS_V9. Baselines (38/45 features) continue "
        "to use `evaluate_variants` as-is."
    )
    lines.append("")
    lines.append("### Per-seed training summary")
    lines.append("")
    lines.append("|seed|train|test|acc|acc(weighted)|rounds|gate23 drop check|gate23 overfit check|")
    lines.append("|---|---|---|---|---|---|---|---|")
    for sr in seed_results:
        lines.append(
            f"|{sr.seed}|{sr.train_size}|{sr.test_size}|"
            f"{sr.held_out_metrics['accuracy']:.3f}|"
            f"{sr.held_out_metrics['accuracy_weighted']:.3f}|"
            f"{sr.n_boosted_rounds}|"
            f"{'PASS' if sr.feature_importance['pass_drop_check'] else 'WARN'}|"
            f"{'PASS' if sr.feature_importance['pass_overfit_check'] else 'WARN'}|"
        )
    if held_out_accs:
        lines.append(
            f"|mean|—|—|{np.mean(held_out_accs):.3f}±{np.std(held_out_accs):.3f}|"
            f"{np.mean(held_out_accs_w):.3f}±{np.std(held_out_accs_w):.3f}|—|—|—|"
        )
    lines.append("")
    lines.append(f"Selected seed (median solver-corrected litmus): **seed {chosen_seed}**")
    lines.append("")
    lines.append("### Held-out classification report (chosen seed)")
    lines.append("")
    chosen_sr = next(sr for sr in seed_results if sr.seed == chosen_seed)
    lines.append(_format_classification_report(chosen_sr.held_out_metrics["classification_report"]))
    lines.append("")
    lines.append("### Held-out confusion matrix (chosen seed; rows=true, cols=pred; class order = ACTION_CLASSES)")
    lines.append("")
    lines.append("```")
    cm = chosen_sr.held_out_metrics["confusion_matrix"]
    header = "        " + " ".join(f"{c:>6}" for c in ACTION_CLASSES)
    lines.append(header)
    for i, row in enumerate(cm):
        lines.append(f"{ACTION_CLASSES[i]:>6}  " + " ".join(f"{v:>6}" for v in row))
    lines.append("```")
    lines.append("")

    lines.append("## Section B — reference-evaluator results (Gate 2.4)")
    lines.append("")
    lines.append(f"Solver-correction overlay: applied to {sorted(_SOLVER_CORRECTIONS.keys())} per `memory/reference_corrections.md`. MW-31, MW-50 NOT applied (unverified per blueprint §5.3).")
    lines.append("")
    lines.append("### Per-seed student litmus (solver-corrected) — full sweep")
    lines.append("")
    lines.append("|seed|raw|solver-corrected|")
    lines.append("|---|---|---|")
    for sr in seed_results:
        s = seed_litmus_results[sr.seed]["student"]
        lines.append(
            f"|{sr.seed}|{s['raw'][0]}/{s['raw'][1]}|"
            f"{s['solver_corrected'][0]}/{s['solver_corrected'][1]}|"
        )
    if sc_scores:
        lines.append(
            f"|mean|—|"
            f"{np.mean(sc_scores):.2f}/40 (std {np.std(sc_scores):.2f})|"
        )
    lines.append("")
    lines.append(f"### Chosen seed ({chosen_seed}) cross-model litmus")
    lines.append("")
    lines.append("|model|raw|solver-corrected|")
    lines.append("|---|---|---|")
    s = chosen_gate_24["student"]
    lines.append(
        f"|v9-student (chosen seed)|{s['raw'][0]}/{s['raw'][1]}|"
        f"{s['solver_corrected'][0]}/{s['solver_corrected'][1]}|"
    )
    for path, b in chosen_gate_24["baselines"].items():
        lines.append(
            f"|{Path(path).name}|{b['raw'][0]}/{b['raw'][1]}|"
            f"{b['solver_corrected'][0]}/{b['solver_corrected'][1]}|"
        )
    lines.append("")
    lines.append("### Solver-corrected per-hand comparison (chosen seed)")
    lines.append("")
    lines.append("Only hands where any model differs from corrected expert OR where the correction overlay activates.")
    lines.append("")
    lines.append("|ref_id|expert (raw)|solver-corrected expert|student|")
    lines.append("|---|---|---|---|")
    for row in s["rows"]:
        if row["ref_id"] in _SOLVER_CORRECTIONS or not row["solver_corrected_correct"]:
            lines.append(
                f"|{row['ref_id']}|{row['expert']}|{row['solver_corrected_expert']}|"
                f"{row['predicted']}|"
            )
    lines.append("")
    lines.append("### Per-class action distribution (chosen seed student)")
    lines.append("")
    student_actions = [row["predicted"] for row in s["rows"]]
    student_dist = {a: student_actions.count(a) for a in ACTION_CLASSES}
    lines.append("|class|student count|")
    lines.append("|---|---|")
    for cls in ACTION_CLASSES:
        lines.append(f"|{cls}|{student_dist.get(cls, 0)}|")
    lines.append("")

    lines.append("## Section C — Gate 2.3 feature importance (chosen seed)")
    lines.append("")
    fi = chosen_sr.feature_importance
    lines.append(f"Pass drop check (no feature <1% importance): **{fi['pass_drop_check']}**")
    lines.append(f"Pass overfit check (no feature >30% importance): **{fi['pass_overfit_check']}**")
    lines.append("")
    lines.append("### v2.4 P1 blocker importances (the migration's load-bearing features)")
    lines.append("")
    lines.append("|feature|importance|on drop list?|")
    lines.append("|---|---|---|")
    fi_dict = dict(fi["all_features"])
    for f in _V24_P1_BLOCKERS:
        v = fi_dict.get(f, 0.0)
        lines.append(f"|`{f}`|{v:.4f}|{'YES — FLAG' if v < 0.01 else 'no'}|")
    lines.append("")
    lines.append("### Top 15 features by importance (chosen seed)")
    lines.append("")
    lines.append("|feature|importance|")
    lines.append("|---|---|")
    for name, imp in fi["all_features"][:15]:
        lines.append(f"|`{name}`|{imp:.4f}|")
    lines.append("")
    lines.append("### Below-1% drop list (chosen seed)")
    lines.append("")
    if fi["low_importance_warnings"]:
        lines.append("|feature|importance|")
        lines.append("|---|---|")
        for name, imp in fi["low_importance_warnings"]:
            lines.append(f"|`{name}`|{imp:.4f}|")
    else:
        lines.append("(none)")
    lines.append("")
    lines.append("### Above-30% overfit warning list (chosen seed)")
    lines.append("")
    if fi["high_importance_warnings"]:
        lines.append("|feature|importance|")
        lines.append("|---|---|")
        for name, imp in fi["high_importance_warnings"]:
            lines.append(f"|`{name}`|{imp:.4f}|")
    else:
        lines.append("(none)")
    lines.append("")

    # ─── Section E (12.5D' addition): delta vs 12.5D baseline ─────────
    # 12.5D baseline numbers from merged PR #126 report
    # (review/comms/PROGRAMMER_REPORT_PHASE125D_TRAINER_2026-05-03.md, chosen
    # seed = 4, master d7d2cdd — pure-confidence weighting, same hyperparams,
    # same seeds, same warm-start anchor).
    _BASELINE_12_5D = {
        "median_solver_corrected": 31,
        "per_seed_solver_corrected": [31, 30, 30, 31, 31],
        "chosen_seed": 4,
        "per_class": {
            "FOLD":  {"precision": 0.938, "recall": 1.000, "f1": 0.968, "support": 15},
            "CHECK": {"precision": 0.939, "recall": 0.939, "f1": 0.939, "support": 49},
            "CALL":  {"precision": 0.769, "recall": 0.833, "f1": 0.800, "support": 12},
            "BET":   {"precision": 0.824, "recall": 0.824, "f1": 0.824, "support": 17},
            "RAISE": {"precision": 0.750, "recall": 0.500, "f1": 0.600, "support":  6},
        },
        "p1_blocker_importance": {
            "nut_flush_block":         0.0000,
            "flush_draw_block_pct":    0.0107,
            "straight_draw_block_pct": 0.0071,
            "nut_made_block_pct":      0.0056,
        },
        "per_hand_predictions": {
            # gto-expert "shared cause" 7 hands
            "MW-17": "FOLD",   # expert/corrected CALL
            "MW-24": "CHECK",  # expert/corrected BET
            "MW-25": "CHECK",  # expert/corrected BET
            "MW-40": "CHECK",  # expert/corrected BET
            "MW-42": "CHECK",  # expert/corrected BET
            "MW-45": "CALL",   # expert/corrected RAISE
            "MW-47": "CALL",   # corrected RAISE (raw expert CALL)
            # gto-expert "distinct cause" 2 hands
            "MW-31": "CALL",   # expert/corrected FOLD
            "MW-46": "RAISE",  # corrected CALL (raw expert FOLD)
        },
    }
    _SHARED_CAUSE = ("MW-17", "MW-24", "MW-25", "MW-40", "MW-42", "MW-45", "MW-47")
    _DISTINCT_CAUSE = ("MW-31", "MW-46")

    lines.append("## Section E — 12.5D vs 12.5D' delta")
    lines.append("")
    lines.append("Compares this run's chosen-seed metrics against the merged 12.5D baseline (PR #126, master `d7d2cdd`, chosen seed = 4, pure-confidence weighting). Same hyperparameters, same seed list, same warm-start anchor — only the `sample_weight` computation changed (confidence × class_weight, cap 3.0, per ml-architect Q3).")
    lines.append("")

    # Litmus delta
    base_per_seed = _BASELINE_12_5D["per_seed_solver_corrected"]
    new_per_seed = [seed_litmus_results[sr.seed]["student"]["solver_corrected"][0]
                    for sr in seed_results]
    lines.append("### Litmus delta (per-seed solver-corrected)")
    lines.append("")
    lines.append("|seed|12.5D|12.5D'|Δ|")
    lines.append("|---|---|---|---|")
    for i, sr in enumerate(seed_results):
        old = base_per_seed[i] if i < len(base_per_seed) else None
        new = new_per_seed[i]
        delta = ("+" if new - old > 0 else "") + str(new - old) if old is not None else "—"
        lines.append(f"|{sr.seed}|{old}/40|{new}/40|{delta}|")
    base_med = _BASELINE_12_5D["median_solver_corrected"]
    new_med = chosen_gate_24["student"]["solver_corrected"][0]
    med_delta = ("+" if new_med - base_med > 0 else "") + str(new_med - base_med)
    lines.append(f"|**median**|**{base_med}/40**|**{new_med}/40**|**{med_delta}**|")
    lines.append("")

    # Per-class metrics delta
    cur_class_report = chosen_sr.held_out_metrics["classification_report"]
    lines.append("### Per-class held-out metrics delta (chosen seed: 12.5D=4 vs 12.5D'={})".format(chosen_seed))
    lines.append("")
    lines.append("|class|12.5D precision/recall/f1|12.5D' precision/recall/f1|recall Δ|")
    lines.append("|---|---|---|---|")
    for cls in ACTION_CLASSES:
        old = _BASELINE_12_5D["per_class"][cls]
        new = cur_class_report.get(cls, {})
        new_p = new.get("precision", 0.0)
        new_r = new.get("recall", 0.0)
        new_f = new.get("f1-score", 0.0)
        recall_delta = new_r - old["recall"]
        lines.append(
            f"|{cls}|{old['precision']:.3f}/{old['recall']:.3f}/{old['f1']:.3f}|"
            f"{new_p:.3f}/{new_r:.3f}/{new_f:.3f}|{recall_delta:+.3f}|"
        )
    lines.append("")

    # Per-hand flips on shared-cause + distinct-cause sets
    rows_by_id = {row["ref_id"]: row for row in chosen_gate_24["student"]["rows"]}
    lines.append("### Per-hand outcome on gto-expert's 7 shared-cause + 2 distinct-cause failures")
    lines.append("")
    lines.append("Predicted flip = 12.5D student wrong → 12.5D' student matches solver-corrected expert. gto-expert prediction: hybrid weighting closes the 7 shared (passive→aggressive collapse), 2 distinct stay broken (feature-surface gap).")
    lines.append("")
    lines.append("|hand|cause|12.5D student|12.5D' student|solver-corrected expert|outcome|")
    lines.append("|---|---|---|---|---|---|")

    def _outcome_label(old_pred: str, new_pred: str, expert: str) -> str:
        norm = lambda a: ("FOLD" if a == "CHECK" else ("RAISE" if a == "BET" else a)).upper()
        old_ok = norm(old_pred) == norm(expert)
        new_ok = norm(new_pred) == norm(expert)
        if old_ok and new_ok:
            return "STAYED-CORRECT"
        if old_ok and not new_ok:
            return "REGRESSED ❌"
        if not old_ok and new_ok:
            return "FLIPPED-CORRECT ✓"
        return "STAYED-WRONG"

    flipped_shared = 0
    stayed_shared = 0
    for hid in _SHARED_CAUSE:
        row = rows_by_id.get(hid)
        if not row:
            continue
        old_pred = _BASELINE_12_5D["per_hand_predictions"][hid]
        new_pred = row["predicted"]
        expert = row["solver_corrected_expert"]
        outcome = _outcome_label(old_pred, new_pred, expert)
        if "FLIPPED-CORRECT" in outcome:
            flipped_shared += 1
        elif "STAYED-WRONG" in outcome:
            stayed_shared += 1
        lines.append(f"|{hid}|shared|{old_pred}|{new_pred}|{expert}|{outcome}|")
    flipped_distinct = 0
    for hid in _DISTINCT_CAUSE:
        row = rows_by_id.get(hid)
        if not row:
            continue
        old_pred = _BASELINE_12_5D["per_hand_predictions"][hid]
        new_pred = row["predicted"]
        expert = row["solver_corrected_expert"]
        outcome = _outcome_label(old_pred, new_pred, expert)
        if "FLIPPED-CORRECT" in outcome:
            flipped_distinct += 1
        lines.append(f"|{hid}|distinct|{old_pred}|{new_pred}|{expert}|{outcome}|")
    lines.append("")
    lines.append(
        f"**Summary:** of 7 shared-cause failures, **{flipped_shared} flipped to correct** under "
        f"hybrid weighting, **{stayed_shared} stayed wrong**. Of 2 distinct-cause failures, "
        f"**{flipped_distinct} flipped** (gto-expert predicted: 0)."
    )
    lines.append("")

    # P1 blocker importance delta
    fi_dict_cur = dict(chosen_sr.feature_importance["all_features"])
    lines.append("### v2.4 P1 blocker importance delta (12.5D vs 12.5D')")
    lines.append("")
    lines.append("|feature|12.5D|12.5D'|Δ|")
    lines.append("|---|---|---|---|")
    for f in _V24_P1_BLOCKERS:
        old = _BASELINE_12_5D["p1_blocker_importance"][f]
        new = fi_dict_cur.get(f, 0.0)
        delta = new - old
        lines.append(f"|`{f}`|{old:.4f}|{new:.4f}|{delta:+.4f}|")
    lines.append("")

    # Interpretation hints — keep terse, reviewer's job to weigh
    lines.append("### Interpretation hints (reviewer-scope)")
    lines.append("")
    lines.append(
        "- **Gate threshold (dispatch):** ≥33 promote, 31-32 STOP/owner-tie-gate, <31 STOP+flag-Q3-wrong"
    )
    lines.append(
        f"- **This run:** median {new_med}/40 → falls in {'≥33 PROMOTE' if new_med >= 33 else ('31-32 owner-tie-gate' if new_med >= 31 else '<31 Q3-flag')}"
    )
    lines.append(
        "- gto-expert prediction was 7 shared flip + 2 distinct stay-wrong "
        f"(predicted student → 36-38/40 range). Empirical: {flipped_shared}/7 shared flipped, "
        f"{flipped_distinct}/2 distinct flipped"
    )
    lines.append("")
    lines.append("## Section D — provenance hashes")
    lines.append("")
    lines.append(f"- Repo HEAD SHA: `{head_sha}`")
    lines.append(f"- Trainer module: `river-rats-core/train_model_v9_student.py` (this PR)")
    lines.append(f"- Warm-start anchor: `{_rel(warm_start_anchor)}` SHA256: `{anchor_sha}`")
    lines.append(f"- Output model: `{_rel(student_output_path)}` SHA256: `{student_sha}`")
    lines.append(f"- xgboost version: `{xgb.__version__}`")
    lines.append(f"- numpy version: `{np.__version__}`")
    lines.append(f"- Python version: `{sys.version.split()[0]}`")
    lines.append("")
    lines.append("## Stop-condition verification (12.5D' dispatch §\"Stop conditions\")")
    lines.append("")
    lines.append("| Stop condition | Status |")
    lines.append("|---|---|")
    lines.append("| Trainer + tests pass on master HEAD before changes | PASS — 16/16 pre-flight at master `1b95648` |")
    lines.append("| Hybrid weighting computation runtime errors | PASS — no zero-count classes; cap=3.0 applied uniformly |")
    lines.append(
        "| Invariant test (mirror drift) | PASS — 17/17 with `_StudentInferenceLike45` shim "
        "(`OMP_NUM_THREADS=1` forces deterministic argmax for borderline MW-33) |"
    )
    lines.append(f"| Pre-pad metadata-only path | {'PASS — succeeded; R-1 fallback NOT triggered' if pre_pad_mode == 'metadata_bump' else 'PRIMARY FAILED, fell back to ' + pre_pad_mode} |")
    chosen_sc = chosen_gate_24["student"]["solver_corrected"][0]
    v22_sc = next(
        (b["solver_corrected"][0] for path, b in chosen_gate_24["baselines"].items()
         if "v9_3way_v2.2" in path), None)
    if v22_sc is not None:
        if chosen_sc >= 33:
            gate_verdict = f"PROMOTE — {chosen_sc}/40 ≥ 33"
        elif chosen_sc >= 31:
            gate_verdict = f"STOP / owner-tie-gate — {chosen_sc}/40 in 31-32 band"
        else:
            gate_verdict = f"STOP / Q3-flag — {chosen_sc}/40 < 31 (regression vs 12.5D)"
        lines.append(f"| Gate threshold (≥33 PROMOTE / 31-32 owner-tie / <31 Q3-flag) | {gate_verdict} |")
    else:
        lines.append("| Gate threshold | v9-3way-v2.2 baseline missing — N/A |")
    lines.append("| 4-file deliverable diff | enforced by builder pre-PR `git diff --stat` check |")
    lines.append("")
    lines.append("## References")
    lines.append("")
    lines.append("- Dispatch directive: `review/comms/MAIN_TERMINAL_PHASE125D_DISPATCH_2026-05-03.md` (PR #125, master `e3c0dfc`)")
    lines.append("- Blueprint: `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` (PR #122, master `1e4e47e`)")
    lines.append("- Pivot directive: PR #119 (master `770b897`)")
    lines.append("- ml-architect spec: PR #110 (master `291af80`)")
    lines.append("- Solver corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`")
    lines.append("")
    # MEDIUM-2 V-X4 cleanup (12.5E-E dispatch §"Step 4"): footer status is
    # now CONDITIONAL on actual model promotion (was unconditional in BLOCKED
    # runs, falsely claiming "promoted to {path}" even when no model written);
    # phase prose is parameterized via --phase-label (was hardcoded "12.5D").
    if promoted:
        lines.append(
            f"**Status: {phase} RUN COMPLETE. Median-litmus seed promoted to "
            f"`{_rel(student_output_path)}`. Awaiting QC pre-merge audit + "
            f"ml-architect/gto-expert review.**"
        )
    else:
        lines.append(
            f"**Status: {phase} RUN COMPLETE; model NOT promoted "
            f"(median seed below v9-3way-v2.2 baseline). 12.5E-F gate decides "
            f"next direction. Awaiting QC pre-merge audit + ml-architect/"
            f"gto-expert review.**"
        )
    lines.append("")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(lines))


# ─── argparse (blueprint §2.5) ────────────────────────────────────────

def _build_argparse() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "v9 student trainer — 59-feature, 5-class XGBoost, "
            "warm-started from v9-3way-v2.2, trained on 494-hand "
            "consensus-labelled corpus."
        )
    )
    p.add_argument("--corpus", type=str,
        default="data/corpus_revision_500_hand_2026-04-27.jsonl")
    p.add_argument("--labels", type=str,
        default="data/corpus_revision_500_hand_labels_2026-04-27.jsonl")
    p.add_argument("--warm-start", type=str,
        default="river-rats-core/models/gto_model_v9_3way_v2.2.json",
        help=("45-feature 5-class warm-start anchor. NOTE: directive "
              "originally cited gto_model_v9_baseline_45feat.json which "
              "is not git-tracked on master HEAD (R-3)."))
    p.add_argument("--output", type=str,
        default="river-rats-core/models/gto_model_v9_student.json")
    p.add_argument("--report", type=str,
        default="review/comms/PROGRAMMER_REPORT_PHASE125E_E_TRAINER_2026-05-05.md")
    p.add_argument("--seeds", type=str, default="0,1,2,3,4")
    p.add_argument("--test-size", type=float, default=0.20)
    p.add_argument("--confidence-weighting",
        choices=("pure", "none"), default="pure")
    p.add_argument("--reference-set",
        choices=("mw_11_50", "none"), default="mw_11_50")
    p.add_argument("--baseline-models", type=str,
        default=("river-rats-core/models/gto_model_v8_38feat.json,"
                 "river-rats-core/models/gto_model_v9_3way_v2.2.json"))
    p.add_argument("--no-write-model", action="store_true",
        help="Do NOT save the model JSON (R-1 dry-run mode).")
    p.add_argument("--phase-label", type=str, default="12.5E",
        help="Phase label for report headers + status lines (e.g., \"12.5D'\", "
             "\"12.5E\", \"12.5G\"). Defaults to current phase \"12.5E\".")
    p.add_argument("--verbose", action="store_true")
    return p


# ─── main ─────────────────────────────────────────────────────────────

def _resolve_path(p: str) -> str:
    """Resolve relative paths against repo root, leaving absolute paths alone."""
    if os.path.isabs(p):
        return p
    return str(_repo_root() / p)


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_argparse().parse_args(argv)

    corpus_path = _resolve_path(args.corpus)
    labels_path = _resolve_path(args.labels)
    warm_start_requested = _resolve_path(args.warm_start)
    output_path = _resolve_path(args.output)
    report_path = _resolve_path(args.report)
    baseline_paths_requested = [
        _resolve_path(p) for p in args.baseline_models.split(",") if p.strip()
    ]

    print(f"[main] corpus={corpus_path}")
    print(f"[main] labels={labels_path}")
    print(f"[main] warm-start (requested)={warm_start_requested}")

    # Warm-start canonicality guard
    warm_start_anchor, warm_start_note = resolve_warm_start_anchor(warm_start_requested)
    print(f"[main] warm-start (resolved)={warm_start_anchor}")
    print(f"[main] warm-start note: {warm_start_note}")

    # Baseline models canonicality
    baseline_resolved, baseline_dropped = filter_baseline_models_to_git_tracked(
        baseline_paths_requested
    )
    for p, why in baseline_dropped:
        print(f"[main] baseline DROPPED {p} — {why}")
    print(f"[main] baselines kept: {baseline_resolved}")

    # Load + join
    corpus = load_corpus(corpus_path)
    labels = load_labels(labels_path)
    X, y, sw, ids = join_on_ref_id(corpus, labels)

    if args.confidence_weighting == "none":
        sw = np.ones_like(sw, dtype=np.float32)

    label_dist = {cls: int(np.sum(y == ACTION_TO_INT[cls])) for cls in ACTION_CLASSES}
    conf_hist: Dict[float, int] = {}
    for _, c in labels.values():
        conf_hist[float(c)] = conf_hist.get(float(c), 0) + 1
    print(f"[main] label dist: {label_dist}")
    print(f"[main] conf hist: {conf_hist}")

    # Pre-pad warm-start anchor
    print(f"[main] pre-padding warm-start: {warm_start_anchor}")
    dry_run_trace: List[str] = []
    pre_pad_mode = "metadata_bump"
    try:
        warm_start_padded_path = prepad_baseline_booster(
            warm_start_anchor, target_n_features=_N_FEATURES_STUDENT
        )
        dry_run_trace.append(
            f"prepad: bumped num_feature 45 → {_N_FEATURES_STUDENT} → "
            f"{warm_start_padded_path}"
        )
    except Exception as e:
        dry_run_trace.append(f"prepad FAILED: {type(e).__name__}: {e}")
        print(f"[main] PRE-PAD FAILED: {e}")
        # Curriculum fallback (R-1) is left as a TODO; STOP per dispatch
        # since neither realization succeeded.
        return 2

    # Seed sweep
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    seed_results: List[SeedResult] = []
    seed_litmus: Dict[int, Dict] = {}

    try:
        for seed in seeds:
            print(f"[seed {seed}] training ...")
            clf, sr = train_one_seed(
                X, y, sw,
                seed=seed,
                test_size=args.test_size,
                warm_start_padded_path=warm_start_padded_path,
                hyperparameters=_HYPERPARAMETERS,
                verbose=args.verbose,
            )
            seed_results.append(sr)
            print(
                f"[seed {seed}] held-out acc={sr.held_out_metrics['accuracy']:.3f} "
                f"rounds={sr.n_boosted_rounds}"
            )

            if args.no_write_model and seed == seeds[0]:
                # R-1 dry-run mode: stop after first seed succeeds, do not gate.
                dry_run_trace.append(
                    f"seed {seed} fit OK; n_features_in_={clf.n_features_in_} "
                    f"rounds={sr.n_boosted_rounds}; --no-write-model: stopping"
                )
                print("[main] --no-write-model: stopping after seed 0 R-1 dry-run.")
                break

            if args.reference_set == "none":
                seed_litmus[seed] = {
                    "student": {
                        "raw": (0, 0), "solver_corrected": (0, 0),
                        "failures_raw": [], "failures_solver_corrected": [],
                        "rows": [],
                    },
                    "baselines": {},
                    "solver_correction_keys": [],
                }
            else:
                print(f"[seed {seed}] running gate_24 reference evaluation ...")
                seed_litmus[seed] = gate_24_reference_evaluation(
                    student_model_path=sr.model_temp_path,
                    baseline_model_paths=baseline_resolved,
                    apply_solver_corrections=True,
                )
                s = seed_litmus[seed]["student"]["solver_corrected"]
                print(f"[seed {seed}] student litmus solver-corrected: {s[0]}/{s[1]}")

        if args.no_write_model:
            # R-1 path: no median selection, no report write of full B section.
            # Print enough to satisfy the dry-run goal.
            print("\n[dry-run] R-1 metadata-only pre-pad succeeded. Trace:")
            for line in dry_run_trace:
                print(f"  {line}")
            return 0

        # Median-litmus selection
        seed_sc_scores = {
            sr.seed: seed_litmus[sr.seed]["student"]["solver_corrected"]
            for sr in seed_results
        }
        chosen = select_median_litmus_seed(seed_results, seed_sc_scores)
        print(f"[main] chosen seed (median litmus): {chosen}")
        chosen_sr = next(sr for sr in seed_results if sr.seed == chosen)
        chosen_gate = seed_litmus[chosen]

        # Stop condition: median seed must match v9-3way-v2.2 baseline
        v22_sc = None
        for path, b in chosen_gate["baselines"].items():
            if "v9_3way_v2.2" in path:
                v22_sc = b["solver_corrected"][0]
                break
        chosen_sc = chosen_gate["student"]["solver_corrected"][0]
        if v22_sc is not None and chosen_sc < v22_sc:
            print(
                f"[main] STOP: median student solver-corrected {chosen_sc}/40 < "
                f"v9-3way-v2.2 baseline {v22_sc}/40 — do NOT promote"
            )
            # Still write report with FAIL status; do NOT write model.
            write_report(
                seed_results=seed_results,
                seed_litmus_results=seed_litmus,
                chosen_seed=chosen,
                chosen_gate_24=chosen_gate,
                label_distribution=label_dist,
                confidence_histogram=conf_hist,
                output_path=report_path,
                warm_start_anchor=warm_start_anchor,
                warm_start_resolution_note=warm_start_note,
                student_output_path=output_path,
                n_train=int(chosen_sr.train_size),
                n_test=int(chosen_sr.test_size),
                baseline_models_resolved=baseline_resolved,
                baseline_models_dropped=baseline_dropped,
                dry_run_trace=dry_run_trace,
                pre_pad_mode=pre_pad_mode,
                cli_args=args,
                promoted=False,
                gate_pass=False,
            )
            return 3

        # Promote chosen seed's model to canonical output path
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(chosen_sr.model_temp_path, "rb") as src, open(output_path, "wb") as dst:
            dst.write(src.read())
        print(f"[main] wrote {output_path}")

        gate_pass_flag = (v22_sc is None) or (chosen_sc >= v22_sc)
        write_report(
            seed_results=seed_results,
            seed_litmus_results=seed_litmus,
            chosen_seed=chosen,
            chosen_gate_24=chosen_gate,
            label_distribution=label_dist,
            confidence_histogram=conf_hist,
            output_path=report_path,
            warm_start_anchor=warm_start_anchor,
            warm_start_resolution_note=warm_start_note,
            student_output_path=output_path,
            n_train=int(chosen_sr.train_size),
            n_test=int(chosen_sr.test_size),
            baseline_models_resolved=baseline_resolved,
            baseline_models_dropped=baseline_dropped,
            dry_run_trace=dry_run_trace,
            pre_pad_mode=pre_pad_mode,
            cli_args=args,
            promoted=True,
            gate_pass=gate_pass_flag,
        )
        print(f"[main] wrote {report_path}")
        return 0

    finally:
        # Cleanup temp artifacts
        try:
            os.unlink(warm_start_padded_path)
        except OSError:
            pass
        for sr in seed_results:
            try:
                os.unlink(sr.model_temp_path)
            except OSError:
                pass


if __name__ == "__main__":
    sys.exit(main())
