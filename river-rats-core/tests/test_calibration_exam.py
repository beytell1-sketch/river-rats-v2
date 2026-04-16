"""Tests for calibration_exam.py v2.3 updates.

Covers Phase 3 prerequisite (per review/comms/V23_HAND_GENERATION_PLAN_2026-04-16.md §3.1):
- 23/28 pass threshold (up from 20/24)
- 4 new hard anchors (d8886, d2410, d8963, d3178)
- Group-D reversal ingestion + 100% reversal enforcement
- Canonical sourcing of anchor data (not hardcoded from memory)

These tests intentionally FAIL on the pre-v2.3 (24-hand, 20/24) version
and PASS after the update lands.
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import calibration_exam as ce


_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TEST_SET = os.path.join(_CORE, '..', 'training-data', 'test_set_50_labelled.jsonl')
_3WAY_COMBINED = os.path.join(_CORE, '..', 'training-data', '3way_combined_350.jsonl')


def _load_canonical_record(sid: str) -> dict:
    """Find the canonical labelled record for a situation_id across v2.3 sources."""
    for path in (_TEST_SET, _3WAY_COMBINED):
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for line in f:
                r = json.loads(line)
                if r.get('situation_id') == sid:
                    return r
    return None


class TestExamHandCount(unittest.TestCase):
    """C.4 test 1: exam contains 28 hands after v2.3 update."""

    def test_exam_has_28_hands(self):
        hands = ce.load_all_calibration_hands()
        self.assertEqual(
            len(hands), 28,
            f"v2.3 calibration exam must contain 28 hands, got {len(hands)}. "
            "24 MW reference hands + 4 new hard anchors (d8886/d2410/d8963/d3178)."
        )


class TestThreshold(unittest.TestCase):
    """C.4 test 2: pass threshold is 23/28."""

    def test_threshold_is_23_of_28(self):
        self.assertEqual(
            ce.STANDARD_PASS_THRESHOLD, 23,
            "v2.3 standard pass threshold must be 23 (see Scope §5 and "
            "V23_HAND_GENERATION_PLAN §3.1)."
        )
        self.assertEqual(
            ce.STANDARD_EXAM_SIZE, 28,
            "v2.3 base exam size must be 28 (24 MW + 4 new anchors)."
        )


class TestReversalHands(unittest.TestCase):
    """C.4 test 3: new predicate-matching anchors are in the reversal set."""

    def test_reversal_hands_include_predicate_anchors(self):
        self.assertIn('d2410_CO_turn', ce.GTO_REVERSAL_HANDS,
                      "d2410_CO_turn is a predicate-matching reversal anchor "
                      "(villain_checked_back=1, capped villain, MW CHECK->BET).")
        self.assertIn('d3178_CO_river', ce.GTO_REVERSAL_HANDS,
                      "d3178_CO_river is a predicate-matching reversal anchor "
                      "(villain_checked_back=1, trap-lean AA).")

    def test_original_reversal_anchors_preserved(self):
        for ref_id in ('MW-30', 'MW-33', 'MW-50'):
            self.assertIn(ref_id, ce.GTO_REVERSAL_HANDS,
                          f"Original reversal anchor {ref_id} must remain.")

    def test_standard_anchors_not_in_reversal_set(self):
        self.assertNotIn('d8886_BB_flop', ce.GTO_REVERSAL_HANDS,
                         "d8886_BB_flop is a standard (mixed-zone) anchor, "
                         "not a Group-D reversal.")
        self.assertNotIn('d8963_HJ_turn', ce.GTO_REVERSAL_HANDS,
                         "d8963_HJ_turn is a standard (mixed-zone) anchor, "
                         "not a Group-D reversal.")

    def test_group_d_registry_exists(self):
        self.assertTrue(hasattr(ce, 'GROUP_D_REVERSAL_HANDS'),
                        "A GROUP_D_REVERSAL_HANDS registry must exist so Group D "
                        "diagnostic hands can be registered without code changes.")
        # The diagnostic test set confirms d3688 as a Group D reversal.
        self.assertIn('d3688_BB_flop', ce.GROUP_D_REVERSAL_HANDS,
                      "d3688_BB_flop is named in PLAN_V23_DIAGNOSTIC_TEST_SET "
                      "as a confirmed Group D reversal.")
        # Group D hands must also be enforced as 100%-must-pass.
        self.assertIn('d3688_BB_flop', ce.GTO_REVERSAL_HANDS,
                      "Group D hands must be ingested into GTO_REVERSAL_HANDS so "
                      "the 100% reversal enforcement applies to them.")


class TestReversalEnforcement(unittest.TestCase):
    """C.4 tests 4 & 5: any reversal failure fails; all reversals + 23/28 passes."""

    def test_any_single_reversal_failure_fails_exam(self):
        reversal_ids = sorted(ce.GTO_REVERSAL_HANDS)
        # Build a run where 28 base hands all pass EXCEPT one reversal hand.
        # Include all reversals in the 28 (placed in the first slots), then
        # standard-filler after.
        results = []
        # Inject reversals (all correct except the second one)
        for i, ref_id in enumerate(reversal_ids):
            results.append({
                'ref_id': ref_id,
                'expert_action': 'BET',
                'agent_action': 'BET' if i != 1 else 'CHECK',  # FAIL slot 1
                'agent_confidence': 'HIGH',
                'agent_reasoning': '',
                'correct': i != 1,
                'equity': 0.5,
            })
        # Fill to 28 total with standard-passing hands
        filler = 28 - len(reversal_ids)
        for i in range(filler):
            results.append({
                'ref_id': f'STD-{i:02d}',
                'expert_action': 'BET',
                'agent_action': 'BET',
                'agent_confidence': 'HIGH',
                'agent_reasoning': '',
                'correct': True,
                'equity': 0.5,
            })
        correct = sum(1 for r in results if r['correct'])
        # Overall count should still satisfy 23/28
        self.assertGreaterEqual(
            correct, ce.STANDARD_PASS_THRESHOLD,
            f"Test setup error: overall count {correct} < 23")
        scores = ce.score_results(results)
        self.assertFalse(
            scores['gate_passed'],
            "Exam must FAIL when any reversal hand is incorrect, even if "
            "overall standard-hand score passes. "
            f"Actual: overall={scores['gate_overall']}, reversals={scores['gate_reversals']}"
        )

    def test_23_of_28_plus_100pct_reversals_passes_exam(self):
        reversal_ids = sorted(ce.GTO_REVERSAL_HANDS)
        # Build 28-hand exam: all reversals in it (pass), plus fill remaining
        # with standard slots. Exactly 23 of the 28 correct.
        results = []
        # First place all reversals as correct
        for ref_id in reversal_ids:
            results.append({
                'ref_id': ref_id, 'expert_action': 'BET', 'agent_action': 'BET',
                'agent_confidence': 'HIGH', 'agent_reasoning': '',
                'correct': True, 'equity': 0.5,
            })
        # Fill remaining slots up to 28, with correctness until we hit 23 total
        remaining = 28 - len(reversal_ids)
        correct_budget = 23 - len(reversal_ids)  # reversals already counted
        for i in range(remaining):
            is_correct = i < correct_budget
            results.append({
                'ref_id': f'STD-{i:02d}',
                'expert_action': 'BET',
                'agent_action': 'BET' if is_correct else 'CHECK',
                'agent_confidence': 'HIGH',
                'agent_reasoning': '',
                'correct': is_correct,
                'equity': 0.5,
            })
        self.assertEqual(len(results), 28)
        correct = sum(1 for r in results if r['correct'])
        self.assertEqual(correct, 23, f"Test setup should have 23 correct; got {correct}")
        scores = ce.score_results(results)
        self.assertTrue(
            scores['gate_passed'],
            f"Exam must PASS with 23/28 standard correct + 100% reversals. "
            f"Got: {scores['gate_overall']} / {scores['gate_reversals']}"
        )


class TestAnchorSourcing(unittest.TestCase):
    """C.4 test 6: new anchor data comes from canonical labelled JSONL."""

    def test_new_anchors_are_fetched_from_canonical_labelled_set(self):
        new_anchor_ids = ['d8886_BB_flop', 'd2410_CO_turn',
                          'd8963_HJ_turn', 'd3178_CO_river']
        hands = ce.load_new_hard_anchors()
        self.assertEqual(
            {h.ref_id for h in hands}, set(new_anchor_ids),
            "load_new_hard_anchors() must return all 4 new anchors by ref_id."
        )

        # For each anchor, verify expected_action and hero_cards match the
        # canonical labelled record (i.e. sourced, not hardcoded from memory).
        for h in hands:
            canonical = _load_canonical_record(h.ref_id)
            self.assertIsNotNone(
                canonical,
                f"{h.ref_id} must be present in test_set_50_labelled.jsonl "
                "or 3way_combined_350.jsonl (canonical labelled sources)."
            )
            self.assertEqual(
                h.expert_action, canonical['expert_action'],
                f"{h.ref_id} expert_action must match canonical labelled record."
            )
            self.assertEqual(
                h.hero_cards, canonical['hero_cards'],
                f"{h.ref_id} hero_cards must match canonical labelled record."
            )
            self.assertEqual(
                h.board, canonical['board'],
                f"{h.ref_id} board must match canonical labelled record."
            )

    def test_all_new_anchors_have_bet_expected_action(self):
        """Sanity: each of the 4 new anchors has expert_action=BET
        (this is why they test the passive-lean bias)."""
        hands = ce.load_new_hard_anchors()
        for h in hands:
            self.assertEqual(
                h.expert_action, 'BET',
                f"{h.ref_id}: all 4 new anchors are BET-expected "
                "(per MW_MISS_BIAS_ANALYSIS + solver log for d8963)."
            )


if __name__ == '__main__':
    unittest.main()
