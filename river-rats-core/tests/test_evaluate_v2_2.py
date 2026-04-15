"""Tests for evaluate_v2_2.py (the ported v2.2 evaluator).

Scope:
- Legal-action mask correctness (facing_bet vs no-bet).
- 108-feature shape (54 raw + 54 attn=1 padding).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from unittest.mock import MagicMock

import numpy as np
import pytest

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))

import evaluate_v2_2 as ev2  # noqa: E402


# -----------------------------------------------------------------------------
# Legal-action mask
# -----------------------------------------------------------------------------

# Class index order: FOLD=0, CHECK=1, CALL=2, BET=3, RAISE=4.

def test_legal_mask_no_bet_keeps_check_and_bet_only():
    m = ev2.legal_mask(facing_bet=False)
    assert m.tolist() == [0, 1, 0, 1, 0]


def test_legal_mask_facing_bet_keeps_fold_call_raise_only():
    m = ev2.legal_mask(facing_bet=True)
    assert m.tolist() == [1, 0, 1, 0, 1]


def test_predict_legal_masks_illegal_actions():
    """If the raw model's top prediction is CHECK but hero is facing
    a bet, masking must force the pick to FOLD/CALL/RAISE."""
    # Two hands. First NOT facing a bet, second facing a bet.
    probs = np.array([
        [0.05, 0.05, 0.60, 0.10, 0.20],  # raw argmax = CALL (idx 2)
        [0.05, 0.80, 0.05, 0.05, 0.05],  # raw argmax = CHECK (idx 1) — ILLEGAL
    ])
    model = MagicMock()
    model.predict_proba.return_value = probs

    preds = ev2.predict_legal(
        model, np.zeros((2, 3), dtype=np.float32),
        facing_bet=[False, True],
    )

    # Hand 0: not facing a bet → legal = {CHECK, BET}.
    # Of those two, BET has 0.10 vs CHECK 0.05 → BET (idx 3).
    assert preds[0] == 3
    # Hand 1: facing a bet → legal = {FOLD, CALL, RAISE}.
    # Of those, FOLD=0.05, CALL=0.05, RAISE=0.05 → argmax ties at FOLD (idx 0).
    assert preds[1] == 0


def test_predict_legal_preserves_legal_top_pick():
    """Legal top prediction survives masking unchanged."""
    probs = np.array([
        [0.05, 0.80, 0.05, 0.10, 0.00],  # CHECK top, not-facing: legal
    ])
    model = MagicMock()
    model.predict_proba.return_value = probs
    preds = ev2.predict_legal(
        model, np.zeros((1, 3), dtype=np.float32), facing_bet=[False],
    )
    assert preds[0] == 1  # CHECK


# -----------------------------------------------------------------------------
# 108-feature shape (54 raw + 54 attn=1 padding)
# -----------------------------------------------------------------------------

def test_feature_spec_loads_54_plus_54_from_real_csv():
    """The committed v2_2_training.csv header must split cleanly into
    54 raw + 54 attn."""
    csv_path = _ROOT.parent / "training-data" / "v2_2_training.csv"
    if not csv_path.exists():
        pytest.skip("v2_2 training CSV not available in this checkout")
    spec = ev2.load_feature_spec(str(csv_path))
    assert len(spec.raw) == 54, f"expected 54 raw, got {len(spec.raw)}"
    assert len(spec.attn) == 54, f"expected 54 attn, got {len(spec.attn)}"
    assert len(spec.all) == 108
    # Every attn_ column must be the raw name with the prefix.
    raw_set = set(spec.raw)
    for a in spec.attn:
        assert a.startswith("attn_")
        assert a[len("attn_"):] in raw_set


def test_attn_padding_always_one_on_fb40_row_assembly(tmp_path, monkeypatch):
    """_fb_row_from_hand must set every attn_* column to 1.0 and the
    resulting encoded vector must have the expected 108 width."""
    csv_path = _ROOT.parent / "training-data" / "v2_2_training.csv"
    if not csv_path.exists():
        pytest.skip("v2_2 training CSV not available in this checkout")
    spec = ev2.load_feature_spec(str(csv_path))

    # Stub extract_all_features to return all-zero numeric features
    # for every FEATURE_COLUMNS key (avoids requiring eval7 etc).
    from gto_model import FEATURE_COLUMNS
    fake_feats = {c: 0.0 for c in FEATURE_COLUMNS}
    # street/hero_position/villain_position are in FEATURE_COLUMNS as
    # numeric — give them sensible zeros.
    monkeypatch.setattr(ev2, "extract_all_features", lambda hd: dict(fake_feats))

    h = {
        "situation_id": "FB-TEST",
        "hero_cards": "AsKs", "board": "2h3h4c",
        "street": "flop", "hero_pos": "BTN",
        "villain_positions": ["BB"], "pot": 100, "to_call": 33,
        "facing_bet": 1, "expected_action": "CALL",
    }
    row, hid, fb, yt = ev2._fb_row_from_hand(h, spec)

    assert hid == "FB-TEST"
    assert fb is True
    # Every attn_* column was padded to 1.0:
    for c in spec.attn:
        assert row[c] == 1.0, f"{c} was not padded to 1.0"

    # Encoded shape via _build_matrix
    X = ev2._build_matrix([row], spec)
    assert X.shape == (1, 108), f"expected (1, 108), got {X.shape}"
    # The attn slice is all ones
    attn_slice = X[0, len(spec.raw):]
    assert np.allclose(attn_slice, 1.0)
