"""Unit tests for sizing_schema_normalizer.

Covers the 12 mandatory cases enumerated in
`review/comms/DRAFT_BLUEPRINT_A0_SCHEMA_FIX_v1_2026-05-17.md` §3.5.

Run from repo root:

    python -m pytest river-rats-core/tests/test_sizing_schema_normalizer.py -v
"""

from __future__ import annotations

import os
import sys
import unittest

# Make `river-rats-core/` importable when invoked from repo root (the
# directory name has a hyphen so we can't use `import` directly).
_HERE = os.path.dirname(os.path.abspath(__file__))
_RR_CORE = os.path.dirname(_HERE)
if _RR_CORE not in sys.path:
    sys.path.insert(0, _RR_CORE)

import sizing_schema_normalizer as ssn  # noqa: E402


def ctx(
    pot_bb: float,
    to_call_bb: float,
    stack_size_bb: float = 100.0,
    facing_bet: int = 1,
    street: str = "flop",
) -> ssn.SpotContext:
    """Helper: build a SpotContext with sensible defaults."""
    return ssn.SpotContext(
        pot_bb=pot_bb,
        to_call_bb=to_call_bb,
        facing_bet=facing_bet,
        stack_size_bb=stack_size_bb,
        street=street,
    )


class TestSizingSchemaNormalizer(unittest.TestCase):
    # ────────────────────────────────────────────────────────────────────
    # 1. FOLD/CHECK/CALL with non-null legacy → warned + nulled
    # ────────────────────────────────────────────────────────────────────
    def test_check_call_fold_legacy_value_warned(self) -> None:
        """FOLD/CHECK/CALL with non-null legacy sizing → null/null + WARN."""
        spot = ctx(pot_bb=12.5, to_call_bb=2.5, facing_bet=0)
        for action in ("FOLD", "CHECK", "CALL"):
            result = ssn.normalize_sizing(action, legacy_sizing_pct=75, ctx=spot)
            self.assertIsNone(result.predicted_bet_pct, msg=action)
            self.assertIsNone(result.predicted_raise_to_bb, msg=action)
            self.assertEqual(result.status, "clean", msg=action)
            self.assertIn("WARN", result.rationale, msg=action)

        # Also: null legacy on non-aggressive action is clean (no WARN).
        ok = ssn.normalize_sizing("CHECK", legacy_sizing_pct=None, ctx=spot)
        self.assertEqual(ok.status, "clean")
        self.assertNotIn("WARN", ok.rationale)

    # ────────────────────────────────────────────────────────────────────
    # 2. BET v=66 → clean
    # ────────────────────────────────────────────────────────────────────
    def test_bet_clean_value(self) -> None:
        """BET v=66 → bet_pct=66, raise_to_bb=None, clean."""
        spot = ctx(pot_bb=12.5, to_call_bb=0.0, facing_bet=0)
        result = ssn.normalize_sizing("BET", legacy_sizing_pct=66, ctx=spot)
        self.assertEqual(result.predicted_bet_pct, 66)
        self.assertIsNone(result.predicted_raise_to_bb)
        self.assertEqual(result.status, "clean")

    # ────────────────────────────────────────────────────────────────────
    # 3. BET v=40 → off-solver, malformed
    # ────────────────────────────────────────────────────────────────────
    def test_bet_off_solver_value(self) -> None:
        """BET v=40 ∉ {25,33,50,66,75,100,150} → malformed_rejected."""
        spot = ctx(pot_bb=12.5, to_call_bb=0.0, facing_bet=0)
        result = ssn.normalize_sizing("BET", legacy_sizing_pct=40, ctx=spot)
        self.assertIsNone(result.predicted_bet_pct)
        self.assertIsNone(result.predicted_raise_to_bb)
        self.assertEqual(result.status, "malformed_rejected")

    # ────────────────────────────────────────────────────────────────────
    # 4. Example A — v=9, pot=12.5, to_call=2.5 → bb interpretation, clean
    # ────────────────────────────────────────────────────────────────────
    def test_raise_clean_bb_canonical(self) -> None:
        """Example A: v=9, pot=12.5, to_call=2.5, stack=97.5 → raise_to=9, clean."""
        spot = ctx(pot_bb=12.5, to_call_bb=2.5, stack_size_bb=97.5)
        result = ssn.normalize_sizing("RAISE", legacy_sizing_pct=9, ctx=spot)
        self.assertIsNone(result.predicted_bet_pct)
        self.assertEqual(result.predicted_raise_to_bb, 9)
        self.assertEqual(result.status, "clean")

    # ────────────────────────────────────────────────────────────────────
    # 5. Example B — v=75, pot=36.5, to_call=9 → pct interpretation
    # ────────────────────────────────────────────────────────────────────
    def test_raise_pct_canonical(self) -> None:
        """Example B: v=75, pot=36.5, to_call=9, stack=91 → raise_to=36, ambiguous."""
        spot = ctx(pot_bb=36.5, to_call_bb=9.0, stack_size_bb=91.0)
        result = ssn.normalize_sizing("RAISE", legacy_sizing_pct=75, ctx=spot)
        self.assertIsNone(result.predicted_bet_pct)
        # pct_to = round(9 + 0.75 * 36.5) = round(36.375) = 36
        self.assertEqual(result.predicted_raise_to_bb, 36)
        self.assertEqual(result.status, "ambiguous_resolved")

    # ────────────────────────────────────────────────────────────────────
    # 6. Tie-break path — v=22 at pot=45 (both bb and pct legal) → bb=22
    # ────────────────────────────────────────────────────────────────────
    def test_raise_tiebreak_both_legal_prefers_bb(self) -> None:
        """v=22 with pot=45, to_call=9 → both bb=22 and pct_to=19 legal; bb wins.

        Per blueprint §3.2: v=22 ∈ CANONICAL_BB and ∉ CANONICAL_PCT, so the
        pure-bb branch fires (not the explicit tie-break branch) — but the
        outcome is the same: raise_to=22 (bb interpretation chosen).
        """
        spot = ctx(pot_bb=45.0, to_call_bb=9.0, stack_size_bb=91.0)
        result = ssn.normalize_sizing("RAISE", legacy_sizing_pct=22, ctx=spot)
        self.assertEqual(result.predicted_raise_to_bb, 22)
        # bb interpretation chosen → status is "clean" (pure-bb branch).
        # If algorithm changes to route via the explicit tie-break branch
        # status would become "ambiguous_resolved"; both indicate bb pick.
        self.assertIn(result.status, ("clean", "ambiguous_resolved"))
        self.assertIsNone(result.predicted_bet_pct)

    # ────────────────────────────────────────────────────────────────────
    # 7. Multiplier interpretation — v=720, to_call=2.5 → raise_to=18
    # ────────────────────────────────────────────────────────────────────
    def test_raise_multiplier_720(self) -> None:
        """Preflop squeeze: v=720, to_call=2.5 → mult interp → raise_to=18."""
        # Preflop facing 2.5bb open in a 4-way limped+open pot; stack=100.
        spot = ctx(pot_bb=12.5, to_call_bb=2.5, stack_size_bb=100.0, street="preflop")
        result = ssn.normalize_sizing("RAISE", legacy_sizing_pct=720, ctx=spot)
        # mult candidate = round(7.20 * 2.5) = 18
        self.assertEqual(result.predicted_raise_to_bb, 18)
        self.assertEqual(result.status, "ambiguous_resolved")
        self.assertIsNone(result.predicted_bet_pct)

    # ────────────────────────────────────────────────────────────────────
    # 8. Multiplier 4-bet — v=300, to_call=9 → raise_to=27
    # ────────────────────────────────────────────────────────────────────
    def test_raise_multiplier_300_4bet(self) -> None:
        """4-bet: v=300, to_call=9 → mult interp → raise_to=27."""
        # 3-bet pot, hero faces 9bb 3-bet; pot=23 (open+3bet+blinds), stack=100.
        spot = ctx(pot_bb=23.0, to_call_bb=9.0, stack_size_bb=100.0, street="preflop")
        result = ssn.normalize_sizing("RAISE", legacy_sizing_pct=300, ctx=spot)
        # mult candidate = round(3.00 * 9) = 27
        self.assertEqual(result.predicted_raise_to_bb, 27)
        self.assertEqual(result.status, "ambiguous_resolved")

    # ────────────────────────────────────────────────────────────────────
    # 9. Neither legal — v=2 facing 9bb → malformed_rejected
    # ────────────────────────────────────────────────────────────────────
    def test_raise_neither_legal_malformed(self) -> None:
        """v=2 facing 9bb bet (min_raise=18) → both candidates illegal → reject."""
        spot = ctx(pot_bb=23.0, to_call_bb=9.0, stack_size_bb=100.0)
        result = ssn.normalize_sizing("RAISE", legacy_sizing_pct=2, ctx=spot)
        # candidate_bb=2 < min_raise=18 → illegal
        # candidate_pct_to = round(9 + 0.02*23) = round(9.46) = 9 < 18 → illegal
        # candidate_mult_to = round(0.02*9) = 0 → illegal
        self.assertIsNone(result.predicted_raise_to_bb)
        self.assertIsNone(result.predicted_bet_pct)
        self.assertEqual(result.status, "malformed_rejected")

    # ────────────────────────────────────────────────────────────────────
    # 10. Above-stack — v=200 with stack=100 → malformed_rejected
    # ────────────────────────────────────────────────────────────────────
    def test_raise_above_stack_malformed(self) -> None:
        """v=200 with stack=100 → bb illegal (>stack), pct illegal → reject."""
        # Context where pct interpretation is ALSO illegal so we cleanly
        # exercise the "above-stack malformed" path:
        #   pot=50, to_call=20, stack=100 → min_raise=40
        #     candidate_bb=200 > 100 → illegal
        #     candidate_pct_to=round(20+2.0*50)=120 > 100 → illegal
        #     candidate_mult_to=round(2.0*20)=40 → legal, but v=200 ∉ CANONICAL_MULT.
        spot = ctx(pot_bb=50.0, to_call_bb=20.0, stack_size_bb=100.0)
        result = ssn.normalize_sizing("RAISE", legacy_sizing_pct=200, ctx=spot)
        self.assertIsNone(result.predicted_raise_to_bb)
        self.assertIsNone(result.predicted_bet_pct)
        self.assertEqual(result.status, "malformed_rejected")

    # ────────────────────────────────────────────────────────────────────
    # 11. Round-trip idempotence — v2 input → v2 output (no-op)
    # ────────────────────────────────────────────────────────────────────
    def test_round_trip_idempotence(self) -> None:
        """A label already in v2 split form passes through with status=no_op."""
        v2_label = {
            "spot_id": "4WF-IDEM-001",
            "labeller_id": 1,
            "predicted_action": "RAISE",
            "predicted_bet_pct": None,
            "predicted_raise_to_bb": 9,
            "confidence": "HIGH",
            "bucket": "test",
            "reasoning": "...",
        }
        context = {
            "pot_bb": 12.5,
            "to_call_bb": 2.5,
            "facing_bet": 1,
            "stack_size_bb": 97.5,
            "street": "flop",
        }
        out = ssn.normalize_label(v2_label, context)
        self.assertEqual(out.status, "no_op")
        self.assertEqual(out.predicted_raise_to_bb, 9)
        self.assertIsNone(out.predicted_bet_pct)
        self.assertEqual(out.predicted_action, "RAISE")
        # Extras preserved.
        self.assertEqual(out.extras.get("confidence"), "HIGH")
        self.assertEqual(out.extras.get("bucket"), "test")

        # And running it a second time stays no-op.
        out_dict = ssn._label_to_v2_dict(out)  # private but exercised intentionally
        self.assertNotIn("predicted_sizing_pct", out_dict)
        second = ssn.normalize_label(out_dict, context)
        self.assertEqual(second.status, "no_op")
        self.assertEqual(second.predicted_raise_to_bb, 9)

    # ────────────────────────────────────────────────────────────────────
    # 12. Consensus alignment — 5 labellers, divergent legacy → same v2
    # ────────────────────────────────────────────────────────────────────
    def test_consensus_alignment(self) -> None:
        """5 RAISE labellers on one spot; 3 distinct legacy encodings → same raise_to_bb.

        Spot context: pot=21, to_call=2.5, stack=100. Three different
        interpretations all converge on raise_to_bb=18:

          - L1, L4: v=18  (bb interpretation, canonical)
          - L2:    v=720 (multiplier interp:   round(7.2 * 2.5) = 18)
          - L3, L5: v=75 (pct interp:          round(2.5 + 0.75 * 21) = 18)

        This is the regression test cited by blueprint §3.5: divergent
        per-labeller encoding does NOT cause v2-consensus drift.
        """
        spot = ctx(pot_bb=21.0, to_call_bb=2.5, stack_size_bb=100.0)
        legacy_values = [18, 720, 75, 18, 75]  # 3 distinct encodings × 5 labellers
        results = [
            ssn.normalize_sizing("RAISE", v, spot) for v in legacy_values
        ]
        for v, r in zip(legacy_values, results):
            self.assertEqual(
                r.predicted_raise_to_bb,
                18,
                msg=(
                    f"v={v} did not normalize to 18 (got "
                    f"{r.predicted_raise_to_bb!r}; rationale={r.rationale!r})"
                ),
            )
            self.assertIsNone(r.predicted_bet_pct, msg=f"v={v}")
            self.assertIn(r.status, ("clean", "ambiguous_resolved"), msg=f"v={v}")


if __name__ == "__main__":
    unittest.main()
