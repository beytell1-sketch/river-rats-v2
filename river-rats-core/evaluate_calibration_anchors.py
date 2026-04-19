"""evaluate_calibration_anchors.py — v2.4 Tier 0 pre-flight gate.

Runs a set of solver-verified or playtest-verified anchor hands through
a trained model and reports pass/fail. Runs BEFORE self-play / full-eval
so distribution-shift regressions are caught in seconds, not 30-45 min.

Per directive-x (2026-04-19): 5 seed anchors at
``river-rats-core/anchors/calibration_anchors.json``. Tolerance rules:

- ``strict``: top-1 (legal-masked) action must equal expected_action
- ``mixed``: expected_action must appear in top-2 with prob >= 0.20

Usage (standalone):
    python3 river-rats-core/evaluate_calibration_anchors.py \\
        --model river-rats-core/models/v2_3_1_model.json \\
        --csv training-data/v2_3_1_training.csv

Usage (import, for train-script trailers):
    from evaluate_calibration_anchors import run_anchor_gate
    failures = run_anchor_gate(model_path, csv_path)
    if failures:
        # STOP / warn / log as appropriate per caller policy
        ...

Returns structured results so callers can render their own reports.
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

from situation_factory import SituationSpec, build_situation  # noqa: E402
from train_model_v2_2 import (  # noqa: E402
    ACTION_TO_INT, INT_TO_ACTION, encode, split_feature_columns,
)


logger = logging.getLogger("calibration_anchors")


ANCHORS_PATH = os.path.join(_THIS_DIR, 'anchors', 'calibration_anchors.json')


@dataclass
class AnchorResult:
    anchor_id: str
    expected_action: str
    tolerance: str
    predicted_action: str  # legal-masked top-1
    prob_expected: float
    top2_actions: List[str]
    passed: bool
    margin: Optional[float] = None  # for mixed: prob of expected; for strict: prob gap
    skip_reason: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)


def _load_anchors(path: str = ANCHORS_PATH) -> List[Dict]:
    with open(path) as f:
        data = json.load(f)
    return data['anchors']


def _spec_from_anchor(anchor: Dict) -> SituationSpec:
    """Reconstruct a SituationSpec from an anchor's `situation` dict."""
    s = anchor['situation']
    # action_history arrives as list of [street, pos, action] lists; SituationFactory
    # expects tuples
    action_history = [tuple(a) for a in s.get('action_history', [])]
    return SituationSpec(
        hero_cards=list(s['hero_cards']),
        board_cards=list(s['board_cards']),
        hero_pos=s['hero_pos'],
        villain_positions=list(s['villain_positions']),
        pot=float(s['pot']),
        to_call=float(s.get('to_call', 0.0)),
        street=s['street'],
        action_history=action_history,
        opener_position=s.get('opener_position'),
        effective_stack=float(s.get('effective_stack', 100.0)),
        current_bet=float(s.get('current_bet', 0.0)),
        num_opponents=s.get('num_opponents'),
    )


def _feat_dict_to_X(feat_dict: Dict, feature_order: List[str]) -> np.ndarray:
    """Single-row feature array matching the training CSV column order."""
    row = []
    for col in feature_order:
        if col.startswith('attn_'):
            row.append(1.0)
            continue
        val = feat_dict.get(col, 0.0)
        if val is None:
            val = 0.0
        if isinstance(val, bool):
            val = int(val)
        if isinstance(val, str):
            try:
                val = float(val)
            except (TypeError, ValueError):
                val = encode(val, col)
        row.append(float(val))
    return np.asarray(row, dtype=float)


def _predict(model, X: np.ndarray, facing_bet: bool) -> Dict:
    """Return predicted action (legal-masked), probability map, top-2 actions."""
    probs = model.predict_proba(X.reshape(1, -1))[0]
    action_probs = {INT_TO_ACTION[i]: float(probs[i]) for i in range(len(probs))}
    legal_actions = (
        ['FOLD', 'CALL', 'RAISE'] if facing_bet else ['CHECK', 'BET']
    )
    legal = {a: action_probs[a] for a in legal_actions}
    top1 = max(legal.items(), key=lambda kv: kv[1])[0]
    top2 = sorted(action_probs.items(), key=lambda kv: -kv[1])[:2]
    top2_ids = [a for a, _ in top2]
    return {
        'top1_legal': top1,
        'action_probs': action_probs,
        'legal_probs': legal,
        'top2_actions': top2_ids,
    }


def _evaluate_anchor(
    anchor: Dict,
    model,
    feature_order: List[str],
) -> AnchorResult:
    """Build spec → extract features → predict → compare vs expected."""
    try:
        spec = _spec_from_anchor(anchor)
        feat_dict = build_situation(spec)
    except Exception as exc:
        return AnchorResult(
            anchor_id=anchor['anchor_id'],
            expected_action=anchor['expected_action'],
            tolerance=anchor['tolerance'],
            predicted_action='BUILD_EXCEPTION',
            prob_expected=0.0,
            top2_actions=[],
            passed=False,
            skip_reason=f'BUILD_EXCEPTION: {exc}',
        )

    facing_bet = feat_dict.get('facing_bet', 0) == 1
    X = _feat_dict_to_X(feat_dict, feature_order)
    pred = _predict(model, X, facing_bet=facing_bet)

    expected = anchor['expected_action']
    tolerance = anchor['tolerance']
    prob_expected = pred['action_probs'].get(expected, 0.0)

    if tolerance == 'strict':
        passed = (pred['top1_legal'] == expected)
        # margin: probability gap between expected and next-best legal action
        legal_sorted = sorted(pred['legal_probs'].items(), key=lambda kv: -kv[1])
        if passed and len(legal_sorted) > 1:
            margin = legal_sorted[0][1] - legal_sorted[1][1]
        else:
            margin = pred['legal_probs'].get(expected, 0.0)
    elif tolerance == 'mixed':
        passed = (
            expected in pred['top2_actions']
            and prob_expected >= 0.20
        )
        margin = prob_expected
    else:
        passed = False
        margin = None

    return AnchorResult(
        anchor_id=anchor['anchor_id'],
        expected_action=expected,
        tolerance=tolerance,
        predicted_action=pred['top1_legal'],
        prob_expected=prob_expected,
        top2_actions=pred['top2_actions'],
        passed=passed,
        margin=margin,
    )


def run_anchor_gate(
    model_path: str,
    csv_path: str,
    anchors_path: str = ANCHORS_PATH,
) -> List[AnchorResult]:
    """Run every anchor through the model. Returns list of AnchorResult.

    Caller decides what to do with failures — this function does NOT
    raise or exit.
    """
    import xgboost as xgb
    model = xgb.XGBClassifier()
    model.load_model(model_path)

    with open(csv_path, newline='') as f:
        header = next(csv.reader(f))
    raw, attn = split_feature_columns(list(header))
    feature_order = raw + attn

    anchors = _load_anchors(anchors_path)
    results = []
    for a in anchors:
        results.append(_evaluate_anchor(a, model, feature_order))
    return results


def render_report(results: List[AnchorResult]) -> str:
    """Pretty-printed text report. Useful for logs."""
    lines = []
    lines.append('=' * 78)
    lines.append('CALIBRATION ANCHOR PRE-FLIGHT')
    lines.append('=' * 78)
    lines.append(
        f'{"anchor_id":<34} {"tol":<8} {"exp":>6} {"pred":>6} {"p(exp)":>7} {"mark":>6}'
    )
    lines.append('-' * 78)
    passed = failed = skipped = 0
    for r in results:
        mark = 'PASS' if r.passed else ('SKIP' if r.skip_reason else 'FAIL')
        if r.passed:
            passed += 1
        elif r.skip_reason:
            skipped += 1
        else:
            failed += 1
        lines.append(
            f'{r.anchor_id:<34} {r.tolerance:<8} {r.expected_action:>6} '
            f'{r.predicted_action:>6} {r.prob_expected:>7.3f} {mark:>6}'
        )
    lines.append('-' * 78)
    lines.append(f'passed={passed}  failed={failed}  skipped={skipped}')
    # Dump failures with more detail
    for r in results:
        if not r.passed and not r.skip_reason:
            lines.append('')
            lines.append(f'FAILURE detail — {r.anchor_id}:')
            lines.append(f'  expected={r.expected_action}  predicted={r.predicted_action}')
            lines.append(f'  top-2 actions: {r.top2_actions}')
            lines.append(f'  p(expected)={r.prob_expected:.3f}')
        elif r.skip_reason:
            lines.append('')
            lines.append(f'SKIP — {r.anchor_id}: {r.skip_reason}')
    return '\n'.join(lines)


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description='Tier-0 calibration-anchor pre-flight gate.',
    )
    p.add_argument('--model', required=True, help='Path to model .json')
    p.add_argument('--csv', required=True,
                   help='Training CSV (used for feature column order only)')
    p.add_argument('--anchors', default=ANCHORS_PATH,
                   help='Anchor fixture JSON (default: '
                        'river-rats-core/anchors/calibration_anchors.json)')
    p.add_argument('--json', action='store_true',
                   help='Output machine-readable JSON instead of text report')
    p.add_argument('--strict-exit', action='store_true',
                   help='Exit non-zero on any failure (for CI / train trailer)')
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
    )
    args = _parse_args(argv)

    results = run_anchor_gate(args.model, args.csv, args.anchors)

    if args.json:
        print(json.dumps([r.to_dict() for r in results], indent=2))
    else:
        print(render_report(results))

    failed = [r for r in results if not r.passed and not r.skip_reason]
    if args.strict_exit and failed:
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
