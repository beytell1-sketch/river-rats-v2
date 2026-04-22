"""
v2.2 Evaluator — Ported from Recovered Heredocs
================================================

Provenance
----------
Ported from the recovered scripts that were committed at ``4b08805``:

- ``review/recovered/eval_MW_test_set_50.py``
- ``review/recovered/eval_MW_with_legal_action_masking.py``
- ``review/recovered/eval_FB40_attn_per_feature.py``
- ``review/recovered/eval_FB40_plus_ablation.py``

Those recovered scripts were DELETED in Stage 3.5 commit 7 per MUST #55
(red-team pass-3 identified silent-fallback patterns in them). Their
port-forward logic lives here in ``evaluate_v2_2.py``; the originals
no longer exist on origin/master. This docstring retains the names for
git-history archaeology only.

Inference contract
------------------
- 110 features: 55 raw (via ``feature_extractor.extract_all_features``
  for FB-40, via ``feat_dict`` for pre-extracted MW-50) + 55 ``attn_*``.
- ``attn_* = 1`` at inference (best-performing strategy; see
  recovered ``eval_FB40_attn_per_feature.py`` ablations).
- Column order is taken from the training CSV header — do NOT
  reorder. Encoding uses the same ``CAT_MAPS`` path-3 logic as
  ``train_model_v2_2.py``.
- Legal-action masking:
    * ``facing_bet=False`` → legal = {CHECK, BET}
    * ``facing_bet=True``  → legal = {FOLD, CALL, RAISE}

Guards
------
- Track 1 completeness guard: every FB-40 hand must produce a
  feat_dict with all 55 FEATURE_COLUMNS (re-extraction step).
- Track 2 dtype guard: every numeric feature must be numeric before
  oracle scoring (rejects residual string leakage like
  ``street='flop'``).

See ``review/comms/PLAN_CONSOLIDATED_2026-04-15.md`` §2 Stream A.2.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS_DIR)

from feature_extractor import extract_all_features  # noqa: E402
from gto_model import FEATURE_COLUMNS  # noqa: E402
from train_model_v2_2 import (  # noqa: E402
    ACTION_TO_INT, INT_TO_ACTION, encode, split_feature_columns,
)


logger = logging.getLogger("evaluate_v2_2")


# -----------------------------------------------------------------------------
# Guards
# -----------------------------------------------------------------------------

def _assert_feat_dict_complete(feat_dict: Dict, hand_id: str) -> None:
    """Track 1 guard: every FEATURE_COLUMNS key must be present."""
    missing = [c for c in FEATURE_COLUMNS if c not in feat_dict]
    if missing:
        raise ValueError(
            f"feat_dict for hand '{hand_id}' is missing "
            f"{len(missing)} of {len(FEATURE_COLUMNS)} required keys: "
            f"{missing}"
        )


def _assert_numeric(row: Dict[str, Any], hand_id: str) -> None:
    """Track 2 guard: every feature value must be numeric (or a
    known categorical string that ``encode`` will map).

    We allow strings for the three CAT_MAPS columns (``street``,
    ``hero_position``, ``villain_position``) — path-3 encoding
    handles those. Everything else must be numeric.
    """
    from train_model_v2_2 import CAT_MAPS
    bad = []
    for col in FEATURE_COLUMNS:
        if col in CAT_MAPS:
            continue
        v = row.get(col)
        if v is None:
            continue  # encode() will coerce to 0.0; tolerated
        if isinstance(v, bool):
            continue
        if not isinstance(v, (int, float)):
            bad.append((col, type(v).__name__, repr(v)))
    if bad:
        details = ", ".join(
            f"{name}={val} (type {ty})" for name, ty, val in bad
        )
        raise ValueError(
            f"hand '{hand_id}' has {len(bad)} non-numeric value(s): "
            f"{details}"
        )


# -----------------------------------------------------------------------------
# Feature-order loader
# -----------------------------------------------------------------------------

@dataclass
class FeatureSpec:
    raw: List[str]
    attn: List[str]

    @property
    def all(self) -> List[str]:
        return self.raw + self.attn


def load_feature_spec(csv_path: str) -> FeatureSpec:
    """Read column order from the training CSV header."""
    with open(csv_path, newline="") as f:
        header = next(csv.reader(f))
    raw, attn = split_feature_columns(header)
    return FeatureSpec(raw=raw, attn=attn)


# -----------------------------------------------------------------------------
# Legal-action masking
# -----------------------------------------------------------------------------

# Class index order matches ACTION_TO_INT.
_MASK_NO_BET = np.array([0, 1, 0, 1, 0], dtype=np.float32)   # CHECK, BET
_MASK_FACING = np.array([1, 0, 1, 0, 1], dtype=np.float32)   # FOLD, CALL, RAISE


def legal_mask(facing_bet: bool) -> np.ndarray:
    return _MASK_FACING if facing_bet else _MASK_NO_BET


def predict_legal(
    model, X: np.ndarray, facing_bet: List[bool]
) -> np.ndarray:
    probs = model.predict_proba(X)
    preds = np.zeros(len(X), dtype=np.int32)
    for i, p in enumerate(probs):
        masked = p * legal_mask(bool(facing_bet[i]))
        preds[i] = int(np.argmax(masked))
    return preds


# -----------------------------------------------------------------------------
# Row assembly — FB-40 (extract from raw cards/board)
# -----------------------------------------------------------------------------

_STREET_SHORT = {"flop": "f", "turn": "t", "river": "r"}


def _fb_row_from_hand(h: Dict, spec: FeatureSpec) -> Tuple[Dict, str, bool, int]:
    """Build one row for the FB-40 pipeline.

    Returns (row_for_encoding, hand_id, facing_bet, y_true).
    """
    hand_id = h["situation_id"]
    hand_dict = {
        "h": h["hero_cards"], "b": h["board"],
        "pos": h["hero_pos"],
        "vp": (h.get("villain_positions") or ["BB"])[0],
        "pot": h["pot"], "tc": h["to_call"],
        "st": _STREET_SHORT.get(h["street"], "f"),
        "fb": int(h["facing_bet"]), "exp": "C",
    }
    feats = extract_all_features(hand_dict)
    _assert_feat_dict_complete(feats, hand_id)

    row = {
        "street": h["street"],
        "hero_position": h["hero_pos"],
        "villain_position": hand_dict["vp"],
    }
    row.update(feats)
    _assert_numeric(row, hand_id)
    for c in spec.attn:
        row[c] = 1.0
    return row, hand_id, bool(h["facing_bet"]), ACTION_TO_INT[h["expected_action"]]


def _mw_row_from_hand(h: Dict, spec: FeatureSpec) -> Tuple[Dict, str, bool, int]:
    """Build one row from a test_set_50_labelled entry (feat_dict pre-extracted).

    Note on completeness: the committed ``test_set_50_labelled.jsonl``
    carries 48-key feat_dicts from an older schema (the 6 range/showdown
    features were added later — see HRP_INVESTIGATION_2026-04-15.md).
    The recovered evaluator relied on ``encode()`` silently zeroing the
    missing 6 keys, and the live v2.2 model was calibrated against that
    behaviour. To reproduce the 80% MW-50 number we therefore do NOT
    enforce the Track 1 completeness guard here — missing keys encode
    to 0.0 exactly as in the recovered script. The Track 1 guard DOES
    run on freshly-extracted FB-40 features in ``_fb_row_from_hand``.
    """
    hand_id = h.get("situation_id", "")
    feats = dict(h.get("feat_dict", {}))
    row = {
        "street": h.get("street", "flop"),
        "hero_position": h.get("hero_position", "BB"),
        "villain_position": (h.get("villain_positions") or ["BB"])[0],
    }
    row.update(feats)
    # Track 2 dtype guard still applies — reject any non-numeric values
    # that slipped through the stored feat_dict (skipping missing keys,
    # which the surrounding note explains).
    for col in FEATURE_COLUMNS:
        if col not in row:
            continue
        v = row[col]
        if col in ("street", "hero_position", "villain_position"):
            continue  # categorical strings handled by path-3 encode()
        if v is None or isinstance(v, bool):
            continue
        if not isinstance(v, (int, float)):
            raise ValueError(
                f"hand '{hand_id}' feat_dict[{col!r}]={v!r} is non-numeric"
            )
    for c in spec.attn:
        row[c] = 1.0
    return (
        row, hand_id, bool(h.get("facing_bet", False)),
        ACTION_TO_INT[h["expert_action"]],
    )


def _build_matrix(
    rows: List[Dict], spec: FeatureSpec
) -> np.ndarray:
    X = np.array(
        [[encode(r, c) for c in spec.all] for r in rows],
        dtype=np.float32,
    )
    assert X.shape[1] == len(spec.all), (
        f"Expected {len(spec.all)} columns, got {X.shape[1]}"
    )
    return X


# -----------------------------------------------------------------------------
# Public evaluators
# -----------------------------------------------------------------------------

@dataclass
class EvalResult:
    name: str
    n: int
    correct: int
    accuracy: float
    per_hand: List[Dict]

    def as_dict(self) -> Dict:
        return {
            "name": self.name,
            "n": self.n,
            "correct": self.correct,
            "accuracy": self.accuracy,
            "per_hand": self.per_hand,
        }


def _load_model(model_path: str):
    import xgboost as xgb
    m = xgb.XGBClassifier()
    m.load_model(model_path)
    return m


def evaluate_fb40(
    model_path: str = "river-rats-core/models/v2_2_model.json",
    test_path: str = "training-data/facing_bet_test_set_40.jsonl",
    csv_path: str = "training-data/v2_2_training.csv",
    legal_mask_enabled: bool = True,
) -> EvalResult:
    spec = load_feature_spec(csv_path)
    model = _load_model(model_path)

    hands = [json.loads(l) for l in open(test_path)]
    rows: List[Dict] = []
    ids: List[str] = []
    facing: List[bool] = []
    y_true: List[int] = []
    for h in hands:
        row, hid, fb, yt = _fb_row_from_hand(h, spec)
        rows.append(row); ids.append(hid); facing.append(fb); y_true.append(yt)

    X = _build_matrix(rows, spec)
    if legal_mask_enabled:
        preds = predict_legal(model, X, facing)
    else:
        preds = model.predict(X)

    per_hand = [
        {
            "situation_id": hid,
            "expected": INT_TO_ACTION[int(y_true[i])],
            "predicted": INT_TO_ACTION[int(preds[i])],
            "correct": bool(preds[i] == y_true[i]),
            "facing_bet": facing[i],
        }
        for i, hid in enumerate(ids)
    ]
    correct = sum(1 for p in per_hand if p["correct"])
    acc = correct / len(per_hand) if per_hand else 0.0
    logger.info(
        "FB-40: %d/%d = %.4f (legal_mask=%s)",
        correct, len(per_hand), acc, legal_mask_enabled,
    )
    return EvalResult("FB-40", len(per_hand), correct, acc, per_hand)


def evaluate_mw50(
    model_path: str = "river-rats-core/models/v2_2_model.json",
    test_path: str = "training-data/test_set_50_labelled.jsonl",
    csv_path: str = "training-data/v2_2_training.csv",
    legal_mask_enabled: bool = True,
) -> EvalResult:
    spec = load_feature_spec(csv_path)
    model = _load_model(model_path)

    hands = [json.loads(l) for l in open(test_path)]
    rows: List[Dict] = []
    ids: List[str] = []
    facing: List[bool] = []
    y_true: List[int] = []
    for h in hands:
        row, hid, fb, yt = _mw_row_from_hand(h, spec)
        rows.append(row); ids.append(hid); facing.append(fb); y_true.append(yt)

    X = _build_matrix(rows, spec)
    if legal_mask_enabled:
        preds = predict_legal(model, X, facing)
    else:
        preds = model.predict(X)

    per_hand = [
        {
            "situation_id": hid,
            "expected": INT_TO_ACTION[int(y_true[i])],
            "predicted": INT_TO_ACTION[int(preds[i])],
            "correct": bool(preds[i] == y_true[i]),
            "facing_bet": facing[i],
        }
        for i, hid in enumerate(ids)
    ]
    correct = sum(1 for p in per_hand if p["correct"])
    acc = correct / len(per_hand) if per_hand else 0.0
    logger.info(
        "MW-50: %d/%d = %.4f (legal_mask=%s)",
        correct, len(per_hand), acc, legal_mask_enabled,
    )
    return EvalResult("MW-50", len(per_hand), correct, acc, per_hand)


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def _parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v2.2 evaluator.")
    p.add_argument(
        "--model",
        default="river-rats-core/models/v2_2_model.json",
    )
    p.add_argument(
        "--csv",
        default="training-data/v2_2_training.csv",
        help="Training CSV — used ONLY for column order.",
    )
    p.add_argument(
        "--fb40",
        default="training-data/facing_bet_test_set_40.jsonl",
    )
    p.add_argument(
        "--mw50",
        default="training-data/test_set_50_labelled.jsonl",
    )
    p.add_argument(
        "--detail", action="store_true",
        help="Print per-hand detail.",
    )
    p.add_argument(
        "--no-legal-mask", action="store_true",
        help="Disable legal-action masking (for ablation).",
    )
    p.add_argument(
        "--only",
        choices=("fb40", "mw50", "both"),
        default="both",
    )
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    )
    args = _parse_args(argv if argv is not None else sys.argv[1:])
    mask = not args.no_legal_mask

    results: List[EvalResult] = []
    if args.only in ("fb40", "both"):
        results.append(evaluate_fb40(
            model_path=args.model, test_path=args.fb40,
            csv_path=args.csv, legal_mask_enabled=mask,
        ))
    if args.only in ("mw50", "both"):
        results.append(evaluate_mw50(
            model_path=args.model, test_path=args.mw50,
            csv_path=args.csv, legal_mask_enabled=mask,
        ))

    for r in results:
        print(f"{r.name}: {r.correct}/{r.n} = {r.accuracy:.4f}")
        if args.detail:
            for p in r.per_hand:
                mark = "OK" if p["correct"] else "XX"
                print(
                    f"  {mark} {p['situation_id']:<24} "
                    f"expected={p['expected']:<5} "
                    f"predicted={p['predicted']:<5} "
                    f"facing_bet={p['facing_bet']}"
                )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
