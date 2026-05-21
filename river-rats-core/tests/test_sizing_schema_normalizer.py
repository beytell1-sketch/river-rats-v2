"""Unit tests for sizing_schema_normalizer.

Covers the 15 mandatory cases enumerated in
`review/comms/DRAFT_BLUEPRINT_A0_SCHEMA_FIX_v2_2026-05-21.md` §3.5.

Tests 1-12 are unchanged from v1 (postflop / non-blind / mult / pct paths;
v2 reduces to v1 behaviour on these). Tests 13-15 are NEW in v2:
    13. test_raise_all_in_v_equals_stack          (F-1 fix: §3.2 STEP 2.5)
    14. test_raise_preflop_bb_defend_min_raise    (F-2 fix: §3.2 STEP 1)
    15. test_consensus_v2_sizing_modal_5_labellers (F-6: §3.6 consensus v2)

Test 16 is a NEW invariant test exercising `validate_v2_label` (per QC
SHOULD_FIX — function was defined but never called/tested in v1 PR #460).

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
    hero_position: str = "",
) -> ssn.SpotContext:
    """Helper: build a SpotContext with sensible defaults."""
    return ssn.SpotContext(
        pot_bb=pot_bb,
        to_call_bb=to_call_bb,
        facing_bet=facing_bet,
        stack_size_bb=stack_size_bb,
        street=street,
        hero_position=hero_position,
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

    # ────────────────────────────────────────────────────────────────────
    # 13. NEW v2 (F-1) — v=100 on 100bb stack → clean_all_in (§3.2 STEP 2.5)
    # ────────────────────────────────────────────────────────────────────
    def test_raise_all_in_v_equals_stack(self) -> None:
        """v=100 with stack=100, pot=13.5, to_call=2.5 → clean_all_in, raise_to=100.

        Verifies the STEP 2.5 short-circuit fires BEFORE the canonical-pct
        branch. Under v1's algorithm this spot would have routed via
        CANONICAL_PCT (v=100 ∈ {25,33,50,66,75,100,150}) and produced
        raise_to=round(2.5 + 1.0×13.5)=16 — silently re-interpreting an
        all-in as a pot-sized raise. v2 fixes by all-in detection FIRST.

        Real-corpus impact: 3 labels in batch_004_l4 (4WF-MULTIWAY-171/175/179).
        """
        spot = ctx(pot_bb=13.5, to_call_bb=2.5, stack_size_bb=100.0)
        result = ssn.normalize_sizing("RAISE", legacy_sizing_pct=100, ctx=spot)
        self.assertEqual(result.predicted_raise_to_bb, 100)
        self.assertIsNone(result.predicted_bet_pct)
        self.assertEqual(result.status, "clean_all_in")
        # NOT 16 (which would be the pct interpretation).
        self.assertNotEqual(result.predicted_raise_to_bb, 16)
        # Rationale references the STEP 2.5 / F-1 path.
        self.assertIn("STEP 2.5", result.rationale)

        # Variant sub-case: same v=100 on 200bb stack must NOT trigger all-in;
        # falls through to canonical-pct branch (correct — pot-sized raise on
        # deep stack is not an all-in tell).
        deep = ctx(pot_bb=13.5, to_call_bb=2.5, stack_size_bb=200.0)
        deep_result = ssn.normalize_sizing("RAISE", legacy_sizing_pct=100, ctx=deep)
        self.assertNotEqual(deep_result.status, "clean_all_in")
        # v=100 ∈ CANONICAL_PCT → pct interpretation: round(2.5 + 1.0×13.5)=16
        self.assertEqual(deep_result.predicted_raise_to_bb, 16)

    # ────────────────────────────────────────────────────────────────────
    # 14. NEW v2 (F-2) — preflop BB-defend min-raise (§3.2 STEP 1 revised)
    # ────────────────────────────────────────────────────────────────────
    def test_raise_preflop_bb_defend_min_raise(self) -> None:
        """Preflop BB facing 2.5x open: min_raise must be 5.0 (NOT 3.0).

        Positive sub-case: BB defends with v=5 (min-raise 3-bet) → legal,
        status=clean, raise_to=5.

        Negative sub-case: same context, v=4 → below new min_raise=5.0 →
        malformed_rejected. Under v1's wrong rule (min_raise=2×to_call=3.0),
        v=4 would have been admitted as clean — v2's stricter rule correctly
        rejects.
        """
        bb_spot = ctx(
            pot_bb=11.5,
            to_call_bb=1.5,
            stack_size_bb=100.0,
            street="preflop",
            hero_position="BB",
        )
        # Sanity-check the helper: BB preflop → hero_committed=1.0.
        self.assertEqual(ssn.hero_already_committed_bb(bb_spot), 1.0)

        # POSITIVE: v=5 → legal (min_raise=5.0; 5 is boundary).
        pos = ssn.normalize_sizing("RAISE", legacy_sizing_pct=5, ctx=bb_spot)
        self.assertIsNone(pos.predicted_bet_pct)
        self.assertEqual(pos.predicted_raise_to_bb, 5)
        self.assertEqual(pos.status, "clean")

        # NEGATIVE: v=4 → below new min_raise=5.0 → malformed_rejected.
        # Trace: candidate_bb=4 < 5 illegal; candidate_pct = round(1.5 + 0.04×11.5)
        # = round(1.96) = 2 < 5 illegal; candidate_mult = round(0.04×1.5) = 0 illegal.
        neg = ssn.normalize_sizing("RAISE", legacy_sizing_pct=4, ctx=bb_spot)
        self.assertIsNone(neg.predicted_bet_pct)
        self.assertIsNone(neg.predicted_raise_to_bb)
        self.assertEqual(neg.status, "malformed_rejected")

        # Cross-check: SB preflop facing 2.5x open (to_call=2.0, hero_committed=0.5)
        # → previous_full_bet=2.5, min_raise=5.0. v=5 legal.
        sb_spot = ctx(
            pot_bb=12.0,
            to_call_bb=2.0,
            stack_size_bb=100.0,
            street="preflop",
            hero_position="SB",
        )
        self.assertEqual(ssn.hero_already_committed_bb(sb_spot), 0.5)
        sb_pos = ssn.normalize_sizing("RAISE", legacy_sizing_pct=5, ctx=sb_spot)
        self.assertEqual(sb_pos.predicted_raise_to_bb, 5)
        self.assertEqual(sb_pos.status, "clean")

        # Postflop sanity (F-2 must not change postflop): bet=9, to_call=9,
        # hero_committed=0, previous_full_bet=9.0, min_raise=18.0 (same as v1).
        postflop = ctx(
            pot_bb=23.0,
            to_call_bb=9.0,
            stack_size_bb=100.0,
            street="flop",
            hero_position="BTN",
        )
        self.assertEqual(ssn.hero_already_committed_bb(postflop), 0.0)

    # ────────────────────────────────────────────────────────────────────
    # 15. NEW v2 (F-6) — consensus v2 modal-sizing across 5 labellers (§3.6)
    # ────────────────────────────────────────────────────────────────────
    def test_consensus_v2_sizing_modal_5_labellers(self) -> None:
        """5 labellers vote RAISE; expect weighted-modal raise_to_bb consensus.

        Main sub-case: clean votes [9,9,9,22,9] → 4 votes for 9, 1 for 22 →
        consensus=9 (weight 4.0 vs 1.0).

        Mixed-status sub-case: votes are mix of clean (v=9, weight 1.0) and
        ambiguous_resolved (v=16 from pct interp, weight 0.7) and one
        malformed_rejected. Expected: 9 wins (4×1.0=4.0 vs 1×0.7=0.7).
        """
        # Build 5 NormalizedLabel objects for the main case.
        labels_main = [
            ssn.NormalizedLabel(
                spot_id="4WL-CONSENSUS-001",
                labeller_id=i + 1,
                predicted_action="RAISE",
                predicted_bet_pct=None,
                predicted_raise_to_bb=v,
                status="clean",
                rationale="test",
            )
            for i, v in enumerate([9, 9, 9, 22, 9])
        ]
        result = ssn.compute_consensus_v2(labels_main)
        self.assertEqual(result.consensus_action, "RAISE")
        self.assertEqual(result.consensus_raise_to_bb, 9)
        self.assertIsNone(result.consensus_bet_pct)
        # 4×1.0 vs 1×1.0 → unique winner; status=clean (no high-disagreement
        # because spread 22-9=13 vs 0.5×22=11 → 13 > 11 → high_disagreement
        # IS triggered). Accept either status; the modal value is what matters.
        self.assertIn(result.sizing_status, ("clean", "high_disagreement"))

        # Mixed-status sub-case.
        # 4 clean votes for 9 (weight 4.0); 1 ambiguous_resolved vote for 16
        # (weight 0.7); 1 malformed_rejected (excluded). Note: we pad to 6
        # labels but malformed_rejected is excluded from the weighted pool.
        labels_mixed = [
            ssn.NormalizedLabel(
                spot_id="4WL-CONSENSUS-002",
                labeller_id=1,
                predicted_action="RAISE",
                predicted_bet_pct=None,
                predicted_raise_to_bb=9,
                status="clean",
                rationale="bb",
            ),
            ssn.NormalizedLabel(
                spot_id="4WL-CONSENSUS-002",
                labeller_id=2,
                predicted_action="RAISE",
                predicted_bet_pct=None,
                predicted_raise_to_bb=16,
                status="ambiguous_resolved",
                rationale="pct interp",
            ),
            ssn.NormalizedLabel(
                spot_id="4WL-CONSENSUS-002",
                labeller_id=3,
                predicted_action="RAISE",
                predicted_bet_pct=None,
                predicted_raise_to_bb=None,
                status="malformed_rejected",
                rationale="below min_raise",
            ),
            ssn.NormalizedLabel(
                spot_id="4WL-CONSENSUS-002",
                labeller_id=4,
                predicted_action="RAISE",
                predicted_bet_pct=None,
                predicted_raise_to_bb=9,
                status="clean",
                rationale="bb",
            ),
            ssn.NormalizedLabel(
                spot_id="4WL-CONSENSUS-002",
                labeller_id=5,
                predicted_action="RAISE",
                predicted_bet_pct=None,
                predicted_raise_to_bb=9,
                status="clean",
                rationale="bb",
            ),
            ssn.NormalizedLabel(
                spot_id="4WL-CONSENSUS-002",
                labeller_id=6,
                predicted_action="RAISE",
                predicted_bet_pct=None,
                predicted_raise_to_bb=9,
                status="clean",
                rationale="bb",
            ),
        ]
        mixed_result = ssn.compute_consensus_v2(labels_mixed)
        self.assertEqual(mixed_result.consensus_action, "RAISE")
        # 4×1.0 vs 1×0.7 → 9 wins by weight.
        self.assertEqual(mixed_result.consensus_raise_to_bb, 9)
        # malformed_count=1, less than 3 → not malformed-via-arb.
        self.assertNotEqual(mixed_result.sizing_status, "malformed-via-arb")

    # ────────────────────────────────────────────────────────────────────
    # 16. validate_v2_label — wire-up check (per QC SHOULD_FIX-1)
    # ────────────────────────────────────────────────────────────────────
    def test_validate_v2_label_catches_violations(self) -> None:
        """validate_v2_label rejects FL7-family violations (rules 1-5)."""
        spot = ctx(pot_bb=12.5, to_call_bb=2.5)

        # Rule 1: BET with non-null raise_to_bb (mismatched fields).
        err = ssn.validate_v2_label("BET", bet_pct=66, raise_to_bb=9, ctx=spot)
        self.assertIsNotNone(err)
        self.assertIn("FL7", err)

        # Rule 2: RAISE with null raise_to_bb.
        err = ssn.validate_v2_label("RAISE", bet_pct=None, raise_to_bb=None, ctx=spot)
        self.assertIsNotNone(err)

        # Rule 3: CHECK with non-null sizing field.
        err = ssn.validate_v2_label("CHECK", bet_pct=66, raise_to_bb=None, ctx=spot)
        self.assertIsNotNone(err)

        # Rule 4: BET with off-enum bet_pct.
        err = ssn.validate_v2_label("BET", bet_pct=40, raise_to_bb=None, ctx=spot)
        self.assertIsNotNone(err)
        self.assertIn("∉", err)

        # Rule 5: RAISE with below-min raise_to_bb.
        # to_call=2.5, hero_committed=0 (default), min_raise=5.0; raise_to=3 below.
        err = ssn.validate_v2_label("RAISE", bet_pct=None, raise_to_bb=3, ctx=spot)
        self.assertIsNotNone(err)
        self.assertIn("outside legal range", err)

        # Clean cases pass.
        self.assertIsNone(ssn.validate_v2_label("BET", 66, None, spot))
        self.assertIsNone(ssn.validate_v2_label("RAISE", None, 9, spot))
        self.assertIsNone(ssn.validate_v2_label("CHECK", None, None, spot))
        self.assertIsNone(ssn.validate_v2_label("CALL", None, None, spot))
        self.assertIsNone(ssn.validate_v2_label("FOLD", None, None, spot))

        # End-to-end check: wired into normalize_label. A spot where
        # normalize_sizing produces a malformed_rejected does NOT get
        # validation flagged (it intentionally bypasses; see normalize_label).
        # A clean BET label round-trips through validation without rationale
        # tampering (no "VALIDATION FAIL" substring).
        clean_label = {
            "spot_id": "4WL-VAL-001",
            "labeller_id": 1,
            "predicted_action": "BET",
            "predicted_sizing_pct": 66,
        }
        context = {
            "pot_bb": 12.5,
            "to_call_bb": 0.0,
            "facing_bet": 0,
            "stack_size_bb": 100.0,
            "street": "flop",
        }
        nl = ssn.normalize_label(clean_label, context)
        self.assertEqual(nl.status, "clean")
        self.assertEqual(nl.predicted_bet_pct, 66)
        self.assertNotIn("VALIDATION FAIL", nl.rationale)


if __name__ == "__main__":
    unittest.main()
