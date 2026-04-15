"""Tests for train_model_v2_2.py (the ported v2.2 trainer).

Scope:
- Preflight gate blocks a mixed-encoding CSV by default.
- ``--allow-mixed-encoding`` flag bypasses the gate.
- Encoding (CAT_MAPS path 3) handles both numeric and string values
  for the three categorical columns.
"""

from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))

import train_model_v2_2 as tv2  # noqa: E402


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------

def _write_mixed_csv(path: Path) -> None:
    """Write a tiny 108-column CSV with MIXED street/hero_position encoding —
    some rows numeric, some string. This mirrors the v2.2 defect."""
    raw_cols = [
        "situation_id", "street", "facing_bet", "pot_size", "to_call",
        "pot_odds", "bet_to_pot", "hero_position", "villain_position",
    ]
    attn_cols = [f"attn_{c}" for c in raw_cols[1:]]  # skip situation_id
    meta_cols = ["label", "label_source"]
    header = raw_cols + attn_cols + meta_cols

    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        # d-series row: numeric encoding
        w.writerow([
            "d0001", "0", "0", "80.0", "0.0", "0.0", "0.0", "5", "2",
            *["1"] * len(attn_cols),
            "CHECK", "d-series",
        ])
        # BP-series row: STRING encoding (the defect)
        w.writerow([
            "BP0001", "flop", "1", "100.0", "33.0", "0.25", "0.33",
            "BTN", "BB",
            *["1"] * len(attn_cols),
            "CALL", "BP-series",
        ])


@pytest.fixture()
def mixed_csv(tmp_path):
    p = tmp_path / "mixed.csv"
    _write_mixed_csv(p)
    return p


# -----------------------------------------------------------------------------
# Encoding tests (CAT_MAPS path 3)
# -----------------------------------------------------------------------------

def test_encode_numeric_street_returns_float():
    row = {"street": "0"}
    assert tv2.encode(row, "street") == 0.0


def test_encode_string_street_maps_via_cat_maps():
    # path 3: float() fails, fall back to CAT_MAPS
    row = {"street": "flop"}
    assert tv2.encode(row, "street") == 0.0
    assert tv2.encode({"street": "turn"}, "street") == 1.0
    assert tv2.encode({"street": "river"}, "street") == 2.0


def test_encode_string_hero_position_maps_via_cat_maps():
    assert tv2.encode({"hero_position": "BTN"}, "hero_position") == 3.0
    assert tv2.encode({"hero_position": "BB"}, "hero_position") == 5.0
    # Unknown string falls through to 0
    assert tv2.encode({"hero_position": "???"}, "hero_position") == 0.0


def test_encode_non_categorical_numeric_passthrough():
    assert tv2.encode({"pot_size": "100.5"}, "pot_size") == 100.5
    assert tv2.encode({"pot_size": ""}, "pot_size") == 0.0


# -----------------------------------------------------------------------------
# Preflight gate integration
# -----------------------------------------------------------------------------

def test_preflight_blocks_mixed_csv_by_default(monkeypatch, mixed_csv, tmp_path):
    """Calling train() without --allow-mixed-encoding must raise
    RuntimeError on a mixed-encoding CSV.

    We monkey-patch the canonical preflight to inspect our temp CSV
    instead of the repo CSV.
    """
    import train_model as tm

    def _fake_preflight():
        errors = []
        with open(mixed_csv, newline="") as f:
            reader = csv.DictReader(f)
            for col in ("street", "hero_position"):
                f.seek(0)
                r2 = csv.DictReader(f)
                bad = 0
                for row in r2:
                    v = (row.get(col) or "").strip()
                    if v == "":
                        continue
                    try:
                        float(v)
                    except ValueError:
                        bad += 1
                if bad:
                    errors.append(f"mixed.csv:{col} has {bad} non-numeric rows")
        if errors:
            raise RuntimeError(
                "ANOMALY-A pre-flight schema check failed:\n  "
                + "\n  ".join(errors)
            )

    monkeypatch.setattr(tv2, "_preflight_schema_check", _fake_preflight)

    with pytest.raises(RuntimeError, match="pre-flight schema check failed"):
        tv2.train(
            csv_path=str(mixed_csv),
            out_model_path=str(tmp_path / "out.json"),
            report_path=str(tmp_path / "report.json"),
            allow_mixed_encoding=False,
        )


def test_allow_mixed_encoding_skips_preflight(monkeypatch, mixed_csv, tmp_path):
    """With --allow-mixed-encoding, preflight must be skipped.

    We stub preflight to raise unconditionally; if it's called, the
    test fails. We also stub out xgboost/sklearn inside train() by
    raising a distinctive sentinel AFTER preflight, so the test
    doesn't need those packages to assert the flag's behaviour.
    """
    def _should_not_be_called():
        raise AssertionError(
            "preflight was called despite --allow-mixed-encoding"
        )

    monkeypatch.setattr(tv2, "_preflight_schema_check", _should_not_be_called)

    # Make the very next import/use after preflight raise a sentinel.
    # We do this by replacing ``build_matrix`` (first call post-preflight
    # in train()) with a marker.
    class _Sentinel(Exception):
        pass

    def _raise_sentinel(*a, **kw):
        raise _Sentinel("reached post-preflight code")

    monkeypatch.setattr(tv2, "build_matrix", _raise_sentinel)

    with pytest.raises(_Sentinel):
        tv2.train(
            csv_path=str(mixed_csv),
            out_model_path=str(tmp_path / "out.json"),
            report_path=str(tmp_path / "report.json"),
            allow_mixed_encoding=True,
        )


# -----------------------------------------------------------------------------
# CLI safety: refuse to overwrite canonical v2_2_model.json
# -----------------------------------------------------------------------------

def test_cli_refuses_to_overwrite_canonical_model(tmp_path):
    with pytest.raises(SystemExit, match="Refusing to overwrite"):
        tv2.main([
            "--csv", str(tmp_path / "does_not_exist.csv"),
            "--out", "river-rats-core/models/v2_2_model.json",
        ])
