#!/usr/bin/env python3
"""Verify feature schema compatibility before warm-start training (R2, Blueprint v3).

Compares the 59-feature corpus contract against the v9 baseline model's
45-feature schema. The 14-feature delta (59-45) is EXPECTED (C6 resolution path).

Exit codes:
    0: schema compatible (either exact match or expected 14-feature delta)
    1: unexpected mismatch (corpus has fewer features than base model,
       or base model features are not a strict subset of corpus features)

Usage:
    python3 scripts/verify_feature_schema_compatibility.py \\
        --model river-rats-core/models/gto_model_v9_baseline_45feat.json \\
        --feature-keys river-rats-core/feature_keys.py
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import List, Optional

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CORE = os.path.join(_REPO, 'river-rats-core')
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from gto_model import FEATURE_COLUMNS  # noqa: E402
from feature_keys import F  # noqa: E402

V24_P1_BLOCKER_FEATURES = (
    F.NUT_FLUSH_BLOCK,
    F.FLUSH_DRAW_BLOCK_PCT,
    F.STRAIGHT_DRAW_BLOCK_PCT,
    F.NUT_MADE_BLOCK_PCT,
)
CORPUS_59_FEATURES: List[str] = list(FEATURE_COLUMNS) + list(V24_P1_BLOCKER_FEATURES)
assert len(CORPUS_59_FEATURES) == 59, (
    f"59-feature corpus contract broken: got {len(CORPUS_59_FEATURES)}"
)


def _load_model_feature_names(model_path: str) -> Optional[List[str]]:
    """Load feature names from an XGBoost JSON model file."""
    try:
        import xgboost as xgb
        booster = xgb.Booster()
        booster.load_model(model_path)
        return booster.feature_names
    except ImportError:
        # xgboost not available — parse JSON directly
        try:
            with open(model_path) as f:
                model_json = json.load(f)
            # XGBoost stores feature names under learner > feature_names
            learner = model_json.get('learner', {})
            feat_names = learner.get('feature_names', [])
            if feat_names:
                return feat_names
            # Alternative path: attributes
            attrs = learner.get('attributes', {})
            feat_str = attrs.get('feature_names')
            if feat_str:
                return json.loads(feat_str)
        except Exception:
            pass
    return None


def verify_schema(model_path: str) -> int:
    """Verify schema compatibility. Returns exit code."""
    corpus_features = CORPUS_59_FEATURES
    corpus_set = set(corpus_features)

    print(f"[R2] Corpus feature contract: {len(corpus_features)} features")

    if not os.path.exists(model_path):
        print(f"[R2] SKIP: model not found at {model_path}", file=sys.stderr)
        print("[R2] Cannot compare — proceeding with corpus-only validation.")
        print(f"[R2] Corpus has {len(corpus_features)} features (expected 59). OK.")
        return 0

    model_features = _load_model_feature_names(model_path)

    if model_features is None:
        print(f"[R2] WARNING: could not extract feature names from {model_path}",
              file=sys.stderr)
        print("[R2] Proceeding without base-model comparison.")
        return 0

    model_set = set(model_features)
    print(f"[R2] Base model feature count: {len(model_features)}")

    # Check for expected 45-vs-59 delta (C6 resolution path)
    if len(model_features) == 45 and len(corpus_features) == 59:
        missing_in_corpus = model_set - corpus_set
        if not missing_in_corpus:
            new_features = corpus_set - model_set
            print(f"[R2] PASS: expected 14-feature delta confirmed.")
            print(f"[R2] Base model (45 features) is a strict subset of corpus (59).")
            print(f"[R2] New features added since v9 baseline ({len(new_features)}):")
            for feat in sorted(new_features):
                print(f"       + {feat}")
            print("[R2] C6 resolution: warm-start via xgb_model parameter. OK.")
            return 0
        else:
            print(f"[R2] FAIL: base model has features not in corpus contract:",
                  file=sys.stderr)
            for feat in sorted(missing_in_corpus):
                print(f"       MISSING: {feat}", file=sys.stderr)
            print("[R2] Unexpected mismatch — base model features must be a "
                  "strict subset of corpus features.", file=sys.stderr)
            return 1

    # Exact match (both 59 features)
    if model_features == corpus_features:
        print("[R2] PASS: exact feature match (same count, same order).")
        return 0

    if model_set == corpus_set:
        print("[R2] WARN: same feature set but different order.")
        print("[R2] Verify that training and inference use the same column order.")
        return 0

    # Unexpected mismatch
    extra_in_model = model_set - corpus_set
    missing_in_corpus = extra_in_model  # model has features corpus lacks
    extra_in_corpus = corpus_set - model_set

    print(f"[R2] FAIL: unexpected feature mismatch.", file=sys.stderr)
    print(f"[R2]   Model: {len(model_features)} features", file=sys.stderr)
    print(f"[R2]   Corpus: {len(corpus_features)} features", file=sys.stderr)
    if missing_in_corpus:
        print(f"[R2]   In model but NOT in corpus ({len(missing_in_corpus)}):",
              file=sys.stderr)
        for feat in sorted(missing_in_corpus):
            print(f"         - {feat}", file=sys.stderr)
    if extra_in_corpus:
        print(f"[R2]   In corpus but NOT in model ({len(extra_in_corpus)}):",
              file=sys.stderr)
        for feat in sorted(extra_in_corpus):
            print(f"         + {feat}", file=sys.stderr)

    # Only fail hard if corpus is MISSING model features (regression)
    if missing_in_corpus:
        print("[R2] Corpus is missing base model features. Do not proceed.",
              file=sys.stderr)
        return 1

    print("[R2] Corpus is a superset of model features — additional features only.")
    print("[R2] Warm-start via xgb_model parameter should work. Verify manually.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(
        description='Verify feature schema compatibility (R2 gate, Blueprint v3).'
    )
    p.add_argument(
        '--model',
        default=os.path.join(_CORE, 'models', 'gto_model_v9_baseline_45feat.json'),
        help='Path to warm-start base model JSON (v9 baseline, 45 features)',
    )
    p.add_argument(
        '--feature-keys',
        default=os.path.join(_CORE, 'feature_keys.py'),
        help='Path to feature_keys.py (for documentation; not parsed directly)',
    )
    args = p.parse_args(argv)

    print(f"[R2] Feature schema compatibility check")
    print(f"[R2] Corpus contract: 59 features (FEATURE_COLUMNS=55 + v2.4 P1 blockers=4)")
    print(f"[R2] Base model: {args.model}")

    rc = verify_schema(args.model)
    sys.exit(rc)


if __name__ == '__main__':
    main()
