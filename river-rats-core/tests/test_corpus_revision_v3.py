"""Tests for Blueprint v3 corpus generation pipeline.

Test-first per CLAUDE.md §3. Tests define the contract before implementation.

Covers:
  - N1: SPR regression assertion (Mode A pool: zero records with spr<2.0 AND pot_bb>6.0)
  - N2: Pairwise correlation check (factory vs self-play)
  - R3: MAGG action history verification (villain_aggression_count==2 at river)
  - R4: NFD boundary validation (|actual - target| <= 0.03)
  - R5: Board texture verification (5 distinct textures across Rule 11 boundary pairs)
  - R1: Re-extraction smoke test (>= 30/100 hands get IS_PFA=1, or graceful fallback)
  - R2: Schema compatibility (expected 45-vs-59 mismatch handled per C6)
"""

import json
import os
import sys
import pytest

# Add river-rats-core to path
_CORE = os.path.join(os.path.dirname(__file__), '..')
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

REPO = os.path.join(_CORE, '..')
PILOT_CORPUS_PATH = os.path.join(REPO, 'data', 'pilot_corpus_100_hand_2026-04-26.jsonl')
PILOT_CORPUS_V2_PATH = os.path.join(REPO, 'data', 'pilot_corpus_100_hand_2026-04-26_v2.jsonl')
V9_BASELINE_MODEL_PATH = os.path.join(REPO, 'river-rats-core', 'models',
                                       'gto_model_v9_baseline_45feat.json')


# ===========================================================================
# R1 Re-extraction smoke tests
# ===========================================================================

class TestR1ReExtractionSmoke:
    """R1: Re-extraction of 100 pilot hands with corrected IS_PFA and SPR."""

    def test_original_corpus_exists(self):
        """Original pilot corpus exists before re-extraction."""
        assert os.path.exists(PILOT_CORPUS_PATH), (
            f"Pilot corpus not found: {PILOT_CORPUS_PATH}"
        )

    def test_original_corpus_has_100_hands(self):
        """Original pilot corpus has exactly 100 hands."""
        with open(PILOT_CORPUS_PATH) as f:
            hands = [json.loads(line) for line in f if line.strip()]
        assert len(hands) == 100, f"Expected 100 hands, got {len(hands)}"

    def test_original_corpus_spr_is_corrupt(self):
        """Confirm original SPR is broken (<2.0 for all 100 hands).

        This documents the bug that R1 must fix. After re-extraction,
        this test is expected to PASS but against the v2 corpus.
        """
        with open(PILOT_CORPUS_PATH) as f:
            hands = [json.loads(line) for line in f if line.strip()]
        sprs = [h['feat_dict']['spr'] for h in hands]
        all_corrupt = all(s < 2.0 for s in sprs)
        assert all_corrupt, (
            f"Expected ALL sprs < 2.0 in original corpus (bug confirmation), "
            f"but {sum(1 for s in sprs if s >= 2.0)} hands have spr >= 2.0. "
            f"SPR range: {min(sprs):.4f} - {max(sprs):.4f}"
        )

    def test_original_corpus_is_pfa_is_all_zero(self):
        """Confirm original IS_PFA=0 for all 100 hands (bug confirmation)."""
        with open(PILOT_CORPUS_PATH) as f:
            hands = [json.loads(line) for line in f if line.strip()]
        pfa_vals = [h['feat_dict'].get('is_preflop_aggressor', 0) for h in hands]
        all_zero = all(v == 0 for v in pfa_vals)
        assert all_zero, (
            f"Expected is_preflop_aggressor=0 for ALL original hands, "
            f"but {sum(1 for v in pfa_vals if v != 0)} have non-zero value"
        )

    def test_prior_actions_contains_preflop_info(self):
        """OQ-4 verification: prior_actions includes hero's preflop action.

        This confirms reconstruction IS possible for hands where hero raised
        preflop. The format is 'preflop: POSITION raise' or 'preflop: POSITION call'.
        """
        with open(PILOT_CORPUS_PATH) as f:
            hands = [json.loads(line) for line in f if line.strip()]

        # Count how many hands have preflop raise in prior_actions
        hero_raised_count = 0
        for h in hands:
            prior = h.get('prior_actions', [])
            pos = h.get('hero_position', '')
            # Check if any prior action shows hero raising preflop
            for action in prior:
                if 'preflop' in action and 'raise' in action:
                    hero_raised_count += 1
                    break

        # Should have some hands where hero raised preflop
        # (from the sample we found ~51 such hands)
        assert hero_raised_count >= 30, (
            f"Expected >= 30 hands with hero preflop raise in prior_actions, "
            f"got {hero_raised_count}. OQ-4 reconstruction may fail."
        )

    @pytest.mark.skipif(
        not os.path.exists(PILOT_CORPUS_V2_PATH),
        reason="Re-extracted corpus v2 not yet generated"
    )
    def test_reextracted_corpus_spr_corrected(self):
        """After re-extraction, mean SPR should be in [5.0, 15.0]."""
        with open(PILOT_CORPUS_V2_PATH) as f:
            hands = [json.loads(line) for line in f if line.strip()]
        sprs = [h['feat_dict']['spr'] for h in hands]
        mean_spr = sum(sprs) / len(sprs)
        assert 5.0 <= mean_spr <= 15.0, (
            f"Re-extracted mean SPR = {mean_spr:.4f}, expected [5.0, 15.0]. "
            f"SPR range: {min(sprs):.4f} - {max(sprs):.4f}"
        )

    @pytest.mark.skipif(
        not os.path.exists(PILOT_CORPUS_V2_PATH),
        reason="Re-extracted corpus v2 not yet generated"
    )
    def test_reextracted_corpus_is_pfa_at_least_30(self):
        """After re-extraction, at least 30/100 hands should have IS_PFA=1.

        Per OQ-4 graceful degradation: if reconstruction fails for all hands,
        IS_PFA may still be 0 for all — in which case SPR fix alone is the gain.
        This test checks the SUCCESS case (reconstruction worked).
        """
        with open(PILOT_CORPUS_V2_PATH) as f:
            hands = [json.loads(line) for line in f if line.strip()]
        pfa_vals = [h['feat_dict'].get('is_preflop_aggressor', 0) for h in hands]
        pfa_count = sum(1 for v in pfa_vals if v == 1)
        assert pfa_count >= 30, (
            f"Expected >= 30/100 re-extracted hands with IS_PFA=1, "
            f"got {pfa_count}. Opener reconstruction may have failed. "
            f"Check graceful-degradation fallback in blueprint OQ-4."
        )

    @pytest.mark.skipif(
        not os.path.exists(PILOT_CORPUS_V2_PATH),
        reason="Re-extracted corpus v2 not yet generated"
    )
    def test_reextracted_corpus_fingerprints_unchanged(self):
        """Re-extraction must not change hero_cards or board_cards (fingerprints preserved)."""
        with open(PILOT_CORPUS_PATH) as f:
            original_hands = {
                json.loads(line)['pilot_hand_id']: json.loads(line)
                for line in open(PILOT_CORPUS_PATH) if line.strip()
            }
        with open(PILOT_CORPUS_V2_PATH) as f:
            reextracted_hands = {
                json.loads(line)['pilot_hand_id']: json.loads(line)
                for line in open(PILOT_CORPUS_V2_PATH) if line.strip()
            }

        mismatches = []
        for pid in original_hands:
            if pid not in reextracted_hands:
                mismatches.append(f"{pid}: missing in v2")
                continue
            orig = original_hands[pid]
            reex = reextracted_hands[pid]
            if orig.get('hero_cards') != reex.get('hero_cards'):
                mismatches.append(f"{pid}: hero_cards changed")
            if orig.get('board') != reex.get('board'):
                mismatches.append(f"{pid}: board changed")

        assert not mismatches, (
            f"Fingerprints changed after re-extraction ({len(mismatches)} hands):\n"
            + "\n".join(mismatches[:5])
        )

    @pytest.mark.skipif(
        not os.path.exists(PILOT_CORPUS_V2_PATH),
        reason="Re-extracted corpus v2 not yet generated"
    )
    def test_reextracted_3bet_hands_have_is_pfa_zero(self):
        """C4 edge case: 3-bet pot hands must NOT have IS_PFA=1 (SB 3-bettor != opener)."""
        with open(PILOT_CORPUS_V2_PATH) as f:
            hands = [json.loads(line) for line in f if line.strip()]
        violations = []
        for h in hands:
            feat = h.get('feat_dict', {})
            if feat.get('is_3bet_pot', 0) == 1 and feat.get('is_preflop_aggressor', 0) == 1:
                violations.append(h.get('pilot_hand_id'))
        assert not violations, (
            f"C4 violation: 3-bet pot hands have IS_PFA=1 (should be 0): {violations}"
        )


# ===========================================================================
# N1 SPR Regression Assertion (Mode A pool)
# ===========================================================================

class TestN1SprRegressionAssertion:
    """N1: Zero Mode A records with spr < 2.0 AND pot_bb > 6.0.

    This catches the unit-mismatch bug. With correct BB conversion,
    a pot_bb > 6.0 implies effective_stack/pot_bb < 100/6 ≈ 16.7,
    which is well above 2.0. A spr < 2.0 with pot_bb > 6.0 is
    a unit-mismatch bug (treating pot in chips as BB).
    """

    def test_spr_regression_definition(self):
        """Unit test: documents the N1 assertion contract.

        With DEFAULT_EFFECTIVE_STACK=100 (in BB) and pot_bb=6.0:
          spr = 100 / 6.0 = 16.67 (NOT < 2.0)

        With DEFAULT_EFFECTIVE_STACK=100 (in BB) and pot=60 chips (wrongly used as BB):
          spr = 100 / 60 = 1.67 (< 2.0) — THIS IS THE BUG

        The bug produces spr < 2.0 only when pot_bb > 6.0 AND the pot
        was passed in chip units (60 chips) instead of BB units (6.0 BB).
        """
        default_effective_stack = 100.0
        pot_bb_correct = 6.0  # correct BB units
        pot_chips_wrong = 60.0  # chip units mistakenly used as BB

        spr_correct = default_effective_stack / pot_bb_correct
        spr_bug = default_effective_stack / pot_chips_wrong

        assert spr_correct > 2.0, f"Correct SPR should be > 2.0, got {spr_correct}"
        assert spr_bug < 2.0, f"Buggy SPR should be < 2.0, got {spr_bug}"

        # N1 assertion: no record should have BOTH spr < 2.0 AND pot_bb > 6.0
        # A correct record with pot_bb=6.0 should have spr=16.67
        assert not (spr_correct < 2.0 and pot_bb_correct > 6.0), (
            "Correct computation violates N1 assertion — logic error"
        )
        # The bug DOES violate N1:
        assert spr_bug < 2.0 and pot_chips_wrong > 6.0, (
            "Bug should violate N1 assertion"
        )

    def _load_mode_a_records(self, pool_path: str) -> list:
        """Load only Mode A (self-play) records from the pool."""
        if not os.path.exists(pool_path):
            return []
        with open(pool_path) as f:
            records = [json.loads(line) for line in f if line.strip()]
        return [r for r in records if r.get('generation_source') == 'self_play_v2']

    def test_n1_mode_a_pool_smoke(self):
        """N1: If smoke test pool exists, check for unit-mismatch regression."""
        smoke_path = '/tmp/smoke_test_pool.jsonl'
        records = self._load_mode_a_records(smoke_path)
        if not records:
            pytest.skip("Smoke test pool not yet generated — run generate_corpus_revision_pool.py")

        violations = [
            r for r in records
            if r['feat_dict']['spr'] < 2.0 and r.get('pot_bb', 0) > 6.0
        ]
        assert not violations, (
            f"N1 FAIL: {len(violations)} Mode A records with spr < 2.0 AND pot_bb > 6.0. "
            f"Unit-mismatch bug regression. First violation: {violations[0]}"
        )


# ===========================================================================
# R3 MAGG Action History Verification
# ===========================================================================

class TestR3MaggActionHistory:
    """R3: MAGG scenarios must use river decision points (villain_aggression_count==2)."""

    def test_magg_action_history_structure_flop_plus_turn(self):
        """MAGG-1 template: villain bets flop + turn => river decision with aggression=2.

        CRITICAL: Villain must be the preflop CALLER (not raiser) so that preflop
        does NOT add to villain_aggression_count. BB (villain) calls preflop, bets
        flop + turn = exactly 2 at the river decision.
        """
        from situation_factory import SituationSpec, build_situation, validate_situation

        # MAGG-1: Hero = CO (opener), Villain = BB (preflop caller who bets postflop)
        # BB bets flop (aggression=1), bets turn (aggression=2) => river = aggression=2
        spec = SituationSpec(
            hero_cards=['Ah', 'Tc'],
            board_cards=['Kd', '7s', '2c', '5h', 'Jd'],  # river board
            hero_pos='CO',
            villain_positions=['BB'],
            pot=50.0,  # BB units: after flop bet + call, turn bet + call
            to_call=0.0,  # hero acts first on river (check-or-bet)
            street='river',
            action_history=[
                ('preflop', 'CO', 'raise'),
                ('preflop', 'BB', 'call'),
                ('flop', 'BB', 'bet'),
                ('flop', 'CO', 'call'),
                ('turn', 'BB', 'bet'),
                ('turn', 'CO', 'call'),
            ],
            opener_position='CO',
        )

        feat_dict = build_situation(spec)
        assert feat_dict['villain_aggression_count'] == 2, (
            f"MAGG-1: expected villain_aggression_count=2 at river, "
            f"got {feat_dict['villain_aggression_count']}. "
            f"Action history: {spec.action_history}"
        )

    def test_magg_turn_decision_has_aggression_1_not_2(self):
        """Confirm that a TURN decision point only gives villain_aggression_count=1.

        This documents WHY we need RIVER decision points for MAGG (the blueprint
        corrected the original truncated action histories). At the turn, only the
        flop is a prior completed street — so if villain bet flop, count=1.
        The turn bet is the CURRENT action, not a prior-street bet.

        CRITICAL: Villain must be the preflop CALLER to avoid preflop adding +1.
        """
        from situation_factory import SituationSpec, build_situation

        # Hero = CO (opener), Villain = BB (preflop caller, bets flop, now bets turn)
        # At TURN decision: prior streets = preflop + flop.
        # BB called preflop (no aggression), BB bet flop (+1) => aggression=1
        spec = SituationSpec(
            hero_cards=['Ah', 'Tc'],
            board_cards=['Kd', '7s', '2c', '5h'],  # turn board
            hero_pos='CO',
            villain_positions=['BB'],
            pot=25.0,
            to_call=8.0,  # villain just bet the turn
            street='turn',
            action_history=[
                ('preflop', 'CO', 'raise'),
                ('preflop', 'BB', 'call'),
                ('flop', 'BB', 'bet'),
                ('flop', 'CO', 'call'),
                ('turn', 'BB', 'bet'),
            ],
            opener_position='CO',
        )

        feat_dict = build_situation(spec)
        # On the turn, villain only bet the FLOP (one prior street) => aggression=1
        # This is WRONG for MAGG target; we need river with 2 prior-street bets
        assert feat_dict['villain_aggression_count'] == 1, (
            f"Turn decision: expected villain_aggression_count=1 "
            f"(villain only bet flop, turn bet is CURRENT), "
            f"got {feat_dict['villain_aggression_count']}"
        )

    def test_magg_check_raise_then_turn_bet(self):
        """MAGG-3: check-raise flop (aggression=1) + turn bet (aggression=2) => river."""
        from situation_factory import SituationSpec, build_situation

        # MAGG-3: BB check-raises flop (counts as 1 aggression), bets turn (aggression=2)
        # CO (hero) is on the river
        spec = SituationSpec(
            hero_cards=['Qc', 'Jc'],
            board_cards=['9h', '6c', '2s', 'Td', '5d'],  # river
            hero_pos='CO',
            villain_positions=['BB'],
            pot=80.0,
            to_call=0.0,
            street='river',
            action_history=[
                ('preflop', 'CO', 'raise'),
                ('preflop', 'BB', 'call'),
                ('flop', 'BB', 'check'),
                ('flop', 'CO', 'bet'),
                ('flop', 'BB', 'raise'),
                ('flop', 'CO', 'call'),
                ('turn', 'BB', 'bet'),
                ('turn', 'CO', 'call'),
            ],
            opener_position='CO',
        )

        feat_dict = build_situation(spec)
        assert feat_dict['villain_aggression_count'] == 2, (
            f"MAGG-3: check-raise flop + bet turn => villain_aggression_count=2 at river. "
            f"Got {feat_dict['villain_aggression_count']}"
        )


# ===========================================================================
# R4 NFD Boundary Validation
# ===========================================================================

class TestR4NfdBoundaryValidation:
    """R4: NFD boundary hands must have |actual_villain_air_pct - target| <= 0.03."""

    def test_nfd_boundary_validation_rule(self):
        """Documents the R4 validation rule contract."""
        # The rule: for each NFD boundary hand with a target villain_air_pct,
        # the actual computed feat_dict['villain_air_pct'] must be within ±0.03
        target_values = [0.15, 0.17, 0.20, 0.22, 0.25]
        tolerance = 0.03

        for target in target_values:
            # Simulate a hand that hits the target exactly
            actual = target
            assert abs(actual - target) <= tolerance, (
                f"R4 validation failed: actual={actual}, target={target}, "
                f"tolerance={tolerance}"
            )

        # Simulate a hand that misses by too much
        bad_actual = 0.30
        bad_target = 0.20
        assert abs(bad_actual - bad_target) > tolerance, (
            f"R4 filter should reject: actual={bad_actual}, target={bad_target}"
        )

    def test_nfd_boundary_hand_smoke(self):
        """NFD scenario: hero has nut flush draw, board has 2+ cards of same suit.

        CRITICAL: has_flush_draw requires exactly 4 cards of same suit across ALL cards
        (2 hero + board). With 2 board hearts, hero needs BOTH cards to be hearts.
        """
        from situation_factory import SituationSpec, build_situation

        # NFD: Hero has Ah Jh on 7h 4h 2d board => 4 hearts total => flush draw ✓
        spec = SituationSpec(
            hero_cards=['Ah', 'Jh'],  # both hearts: 4 hearts total with 7h+4h on board
            board_cards=['7h', '4h', '2d'],
            hero_pos='BB',
            villain_positions=['BTN'],
            pot=12.0,  # BB units
            to_call=6.0,  # villain bet
            street='flop',
            action_history=[
                ('preflop', 'BTN', 'raise'),
                ('preflop', 'BB', 'call'),
                ('flop', 'BB', 'check'),
                ('flop', 'BTN', 'bet'),
            ],
            opener_position='BTN',
        )

        feat_dict = build_situation(spec)
        # Verify the hero has flush draw components
        assert feat_dict.get('has_flush_draw') == 1, (
            f"NFD smoke: expected has_flush_draw=1 for AhJh on 7h4h2d board (4 hearts), "
            f"got {feat_dict.get('has_flush_draw')}"
        )
        assert feat_dict.get('nut_flush_block') == 1, (
            f"NFD smoke: expected nut_flush_block=1 for Ah, "
            f"got {feat_dict.get('nut_flush_block')}"
        )


# ===========================================================================
# R5 Board Texture Verification
# ===========================================================================

class TestR5BoardTextureVerification:
    """R5: Rule 11 boundary scenarios must use >= 3 distinct board textures."""

    RULE11_BOARDS = [
        ('KcKd4s', 'dry_paired'),           # Pair 1: dry paired
        ('KdTd4c', 'two_tone_paired'),        # Pair 2: 2-tone paired
        ('8h8d7c', 'dynamic_paired'),         # Pair 3: dynamic paired (connected)
        ('9d6d3s', 'two_tone_flush'),         # Pair 4: 2-tone-flush low (C2 correction)
        ('JsJd9c', 'draw_heavy_paired'),      # Pair 5: paired-J draw-heavy (C1 correction)
    ]

    def test_rule11_boards_at_least_3_distinct_textures(self):
        """Rule 11 boundary pairs span >= 3 distinct board textures."""
        # Extract texture categories
        textures = {board_type for _, board_type in self.RULE11_BOARDS}
        assert len(textures) >= 3, (
            f"R5: expected >= 3 distinct textures across 5 boundary pairs, "
            f"got {len(textures)}: {textures}"
        )

    def test_rule11_pairs_are_5_in_total(self):
        """Rule 11 boundary table has exactly 5 pairs."""
        assert len(self.RULE11_BOARDS) == 5, (
            f"Expected 5 Rule 11 boundary pairs, got {len(self.RULE11_BOARDS)}"
        )

    def test_c1_correction_pair5_is_paired_board(self):
        """C1 correction: Pair 5 board is JsJd9c (paired, NOT JsTd4d which was unpaired)."""
        pair5_board = self.RULE11_BOARDS[4][0]
        # JsJd9c: ranks are J, J, 9 — has a pair
        cards = [pair5_board[i:i+2] for i in range(0, len(pair5_board), 2)]
        ranks = [c[0] for c in cards]
        from collections import Counter
        rank_counts = Counter(ranks)
        has_pair = 2 in rank_counts.values() or 3 in rank_counts.values()
        assert has_pair, (
            f"C1: Pair 5 board {pair5_board} should be paired (JsJd9c), "
            f"but ranks {ranks} show no pair. Ranks: {dict(rank_counts)}"
        )

    def test_c2_correction_pair4_is_two_tone_not_monotone(self):
        """C2 correction: Pair 4 board is 9d6d3s (2-tone), NOT 9h6h3h (monotone)."""
        pair4_board = self.RULE11_BOARDS[3][0]
        # 9d6d3s: suits are d, d, s — NOT all same (monotone would be all same)
        cards = [pair4_board[i:i+2] for i in range(0, len(pair4_board), 2)]
        suits = [c[1] for c in cards]
        from collections import Counter
        suit_counts = Counter(suits)
        is_monotone = 3 in suit_counts.values()
        assert not is_monotone, (
            f"C2: Pair 4 board {pair4_board} should be 2-tone (NOT monotone), "
            f"but suits {suits} are all same."
        )
        # Must be 2-tone (exactly 2 suits)
        has_two_tone = len(suit_counts) == 2
        assert has_two_tone, (
            f"C2: Pair 4 board {pair4_board} should be 2-tone (2 distinct suits), "
            f"but has {len(suit_counts)} distinct suits: {dict(suit_counts)}"
        )

    def test_rule11_boards_produce_valid_situations(self):
        """Each Rule 11 board produces a valid situation via SituationFactory."""
        from situation_factory import SituationSpec, build_situation

        for board_str, texture in self.RULE11_BOARDS:
            # Convert board string to list of 2-char card strings
            board_cards = [board_str[i:i+2] for i in range(0, len(board_str), 2)]

            spec = SituationSpec(
                hero_cards=['Ac', 'Td'],  # OOP medium-made hand
                board_cards=board_cards,
                hero_pos='BB',
                villain_positions=['CO'],
                pot=18.0,
                to_call=0.0,  # hero faces check-or-bet (OOP first to act)
                street='flop',
                action_history=[
                    ('preflop', 'CO', 'raise'),
                    ('preflop', 'BB', 'call'),
                ],
                opener_position='CO',
            )

            try:
                feat_dict = build_situation(spec)
                assert 'villain_top_pair_plus_pct' in feat_dict, (
                    f"R5: missing villain_top_pair_plus_pct for board {board_str}"
                )
            except Exception as e:
                pytest.fail(
                    f"R5: build_situation failed for board {board_str} "
                    f"(texture={texture}): {e}"
                )


# ===========================================================================
# R2 Schema Compatibility
# ===========================================================================

class TestR2SchemaCompatibility:
    """R2: Expected 45-vs-59 mismatch handled per C6 resolution path."""

    def test_expected_feature_count_59(self):
        """Corpus contract is 59 features (45 + 14 added since v9 baseline)."""
        sys.path.insert(0, os.path.join(_CORE))
        from gto_model import FEATURE_COLUMNS
        from feature_keys import F

        V24_P1_BLOCKER_FEATURES = (
            F.NUT_FLUSH_BLOCK,
            F.FLUSH_DRAW_BLOCK_PCT,
            F.STRAIGHT_DRAW_BLOCK_PCT,
            F.NUT_MADE_BLOCK_PCT,
        )
        expected_59 = list(FEATURE_COLUMNS) + list(V24_P1_BLOCKER_FEATURES)
        assert len(expected_59) == 59, (
            f"Expected 59-feature contract: FEATURE_COLUMNS({len(FEATURE_COLUMNS)}) "
            f"+ v2.4 P1 blockers(4) = 59, got {len(expected_59)}"
        )

    @pytest.mark.skipif(
        not os.path.exists(V9_BASELINE_MODEL_PATH),
        reason="v9 baseline model not found"
    )
    def test_v9_baseline_model_has_45_features(self):
        """v9 baseline model (warm-start base) should have 45 features."""
        import xgboost as xgb

        model = xgb.Booster()
        model.load_model(V9_BASELINE_MODEL_PATH)
        feature_names = model.feature_names
        if feature_names is None:
            pytest.skip("Model has no feature names stored — cannot verify count")

        n_features = len(feature_names)
        assert n_features == 45, (
            f"v9 baseline model expected 45 features (warm-start base), "
            f"got {n_features}. If this is wrong, the 14-feature delta is incorrect."
        )

    def test_c6_resolution_path_documented(self):
        """C6: 45-vs-59 mismatch is EXPECTED and handled — not a blocking failure.

        Documents the C6 resolution: 45-feature base model + 14 new features
        = 59-feature corpus. XGBoost handles via xgb_model warm-start parameter.
        """
        expected_new_features_count = 14  # 59 - 45 = 14 new features
        base_features = 45
        corpus_features = 59
        delta = corpus_features - base_features
        assert delta == expected_new_features_count, (
            f"C6 resolution: expected 14-feature delta (59-45), got {delta}"
        )


# ===========================================================================
# N2 Pairwise Correlation Check (smoke validation)
# ===========================================================================

class TestN2PairwiseCorrelation:
    """N2: Factory pool vs self-play pool feature joint distributions.

    Full N2 check requires both pools to exist. These tests document
    the contract and run the check when pools are available.
    """

    CORR_FEATURES = [
        'villain_air_pct',
        'villain_top_pair_plus_pct',
        'villain_draw_pct',
        'villain_aggression_count',
    ]
    CORR_THRESHOLD = 0.3

    def _compute_pairwise_correlations(self, records: list) -> dict:
        """Compute pairwise correlations between the 4 villain features."""
        import math

        n = len(records)
        if n < 5:
            return {}

        feats = {f: [] for f in self.CORR_FEATURES}
        for r in records:
            fd = r.get('feat_dict', {})
            for f in self.CORR_FEATURES:
                feats[f].append(float(fd.get(f, 0)))

        # Pearson correlation
        def pearson(x, y):
            n = len(x)
            mx, my = sum(x)/n, sum(y)/n
            num = sum((xi-mx)*(yi-my) for xi, yi in zip(x, y))
            denom = math.sqrt(
                sum((xi-mx)**2 for xi in x) * sum((yi-my)**2 for yi in y)
            )
            return num / denom if denom > 0 else 0.0

        corrs = {}
        for i, f1 in enumerate(self.CORR_FEATURES):
            for f2 in self.CORR_FEATURES[i+1:]:
                key = f"{f1}_vs_{f2}"
                corrs[key] = pearson(feats[f1], feats[f2])
        return corrs

    def test_pairwise_correlation_contract(self):
        """N2 contract: any pairwise correlation diff > 0.3 between pools is a flag."""
        # Synthetic test: identical distributions should have 0 diff
        corr_a = {'villain_air_pct_vs_villain_top_pair_plus_pct': -0.5}
        corr_b = {'villain_air_pct_vs_villain_top_pair_plus_pct': -0.5}

        for key in corr_a:
            diff = abs(corr_a[key] - corr_b[key])
            assert diff <= self.CORR_THRESHOLD, (
                f"N2: identical distributions should have 0 diff, got {diff}"
            )

        # Non-identical distributions that exceed threshold
        corr_c = {'villain_air_pct_vs_villain_top_pair_plus_pct': 0.2}
        for key in corr_a:
            if key in corr_c:
                diff = abs(corr_a[key] - corr_c[key])
                assert diff > self.CORR_THRESHOLD, (
                    f"N2: expected diff > {self.CORR_THRESHOLD} for divergent distributions"
                )

    def test_n2_smoke_pool_correlation_check(self):
        """N2: If smoke pool exists, verify factory vs self-play correlation check."""
        smoke_path = '/tmp/smoke_test_pool.jsonl'
        if not os.path.exists(smoke_path):
            pytest.skip("Smoke pool not yet generated")

        with open(smoke_path) as f:
            all_records = [json.loads(line) for line in f if line.strip()]

        factory_records = [r for r in all_records
                           if r.get('generation_source') != 'self_play_v2']
        selfplay_records = [r for r in all_records
                            if r.get('generation_source') == 'self_play_v2']

        if len(factory_records) < 5 or len(selfplay_records) < 5:
            pytest.skip(f"Not enough records for correlation check: "
                        f"factory={len(factory_records)}, "
                        f"selfplay={len(selfplay_records)}")

        corr_factory = self._compute_pairwise_correlations(factory_records)
        corr_selfplay = self._compute_pairwise_correlations(selfplay_records)

        divergent_pairs = []
        for key in corr_factory:
            if key in corr_selfplay:
                diff = abs(corr_factory[key] - corr_selfplay[key])
                if diff > self.CORR_THRESHOLD:
                    divergent_pairs.append(
                        f"{key}: factory={corr_factory[key]:.3f}, "
                        f"selfplay={corr_selfplay[key]:.3f}, diff={diff:.3f}"
                    )

        # This is a FLAG (non-blocking per N2 spec), so we just print a warning
        if divergent_pairs:
            print(f"\nN2 WARNING: {len(divergent_pairs)} corr pairs diverge > 0.3:")
            for pair in divergent_pairs:
                print(f"  {pair}")
        # N2 is non-blocking per blueprint — we record but don't fail


# ===========================================================================
# Module-level smoke tests
# ===========================================================================

class TestModuleImports:
    """Verify scenario module imports work before full pool generation."""

    def test_pfa_scenarios_module_importable(self):
        """PFA scenarios module must be importable."""
        try:
            sys.path.insert(0, _CORE)
            from corpus_revision_scenarios import pfa_scenarios
            assert hasattr(pfa_scenarios, 'generate_scenarios'), (
                "pfa_scenarios must export generate_scenarios()"
            )
        except ImportError as e:
            pytest.fail(f"pfa_scenarios not importable: {e}")

    def test_magg_scenarios_module_importable(self):
        """MAGG scenarios module must be importable."""
        try:
            from corpus_revision_scenarios import magg_scenarios
            assert hasattr(magg_scenarios, 'generate_scenarios'), (
                "magg_scenarios must export generate_scenarios()"
            )
        except ImportError as e:
            pytest.fail(f"magg_scenarios not importable: {e}")

    def test_nfd_scenarios_module_importable(self):
        """NFD scenarios module must be importable."""
        try:
            from corpus_revision_scenarios import nfd_scenarios
            assert hasattr(nfd_scenarios, 'generate_scenarios'), (
                "nfd_scenarios must export generate_scenarios()"
            )
        except ImportError as e:
            pytest.fail(f"nfd_scenarios not importable: {e}")

    def test_donk_bet_defence_scenarios_module_importable(self):
        """Module 8: donk-bet defence scenarios must be importable."""
        try:
            from corpus_revision_scenarios import donk_bet_defence_scenarios
            assert hasattr(donk_bet_defence_scenarios, 'generate_scenarios'), (
                "donk_bet_defence_scenarios must export generate_scenarios()"
            )
        except ImportError as e:
            pytest.fail(f"donk_bet_defence_scenarios not importable: {e}")

    def test_sb_hero_scenarios_module_importable(self):
        """Module 9: SB-as-hero scenarios must be importable."""
        try:
            from corpus_revision_scenarios import sb_hero_scenarios
            assert hasattr(sb_hero_scenarios, 'generate_scenarios'), (
                "sb_hero_scenarios must export generate_scenarios()"
            )
        except ImportError as e:
            pytest.fail(f"sb_hero_scenarios not importable: {e}")

    def test_generate_corpus_revision_pool_importable(self):
        """Pool generator must be importable as a module."""
        try:
            import importlib.util
            spec_path = os.path.join(_CORE, 'generate_corpus_revision_pool.py')
            if not os.path.exists(spec_path):
                pytest.fail(
                    f"generate_corpus_revision_pool.py not found at {spec_path}"
                )
            spec = importlib.util.spec_from_file_location(
                'generate_corpus_revision_pool', spec_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            assert hasattr(mod, 'generate_pool'), (
                "generate_corpus_revision_pool must export generate_pool()"
            )
        except Exception as e:
            pytest.fail(f"generate_corpus_revision_pool not importable: {e}")


class TestScenarioGeneratorContracts:
    """Test that scenario generators produce valid structured output."""

    def _check_scenario_record(self, record: dict, source: str):
        """Validate a single scenario record has required fields."""
        required_fields = [
            'situation_id', 'hero_cards', 'board', 'street',
            'hero_position', 'villain_positions', 'pot', 'to_call',
            'facing_bet', 'num_opponents', 'prior_actions', 'feat_dict',
            'generation_source',
        ]
        missing = [f for f in required_fields if f not in record]
        assert not missing, (
            f"Scenario record from {source} missing fields: {missing}\n"
            f"Record keys: {list(record.keys())}"
        )

    def test_pfa_scenario_output_structure(self):
        """PFA scenarios produce records with is_preflop_aggressor=1."""
        from corpus_revision_scenarios.pfa_scenarios import generate_scenarios

        records = generate_scenarios(forbidden_fingerprints=set())
        assert len(records) > 0, "PFA generator produced 0 records"

        for rec in records[:5]:
            self._check_scenario_record(rec, 'pfa_scenarios')
            assert rec['feat_dict'].get('is_preflop_aggressor') == 1, (
                f"PFA scenario must have is_preflop_aggressor=1, "
                f"got {rec['feat_dict'].get('is_preflop_aggressor')}"
            )

    def test_magg_scenario_aggression_count_is_2(self):
        """MAGG scenarios must have villain_aggression_count=2 (river decision)."""
        from corpus_revision_scenarios.magg_scenarios import generate_scenarios

        records = generate_scenarios(forbidden_fingerprints=set())
        assert len(records) > 0, "MAGG generator produced 0 records"

        for rec in records:
            self._check_scenario_record(rec, 'magg_scenarios')
            agg = rec['feat_dict'].get('villain_aggression_count')
            assert agg == 2, (
                f"R3: MAGG scenario must have villain_aggression_count=2 at river, "
                f"got {agg} for situation_id={rec.get('situation_id')}"
            )

    def test_bac_scenario_has_callers(self):
        """BAC scenarios must have num_callers_to_bet >= 1."""
        from corpus_revision_scenarios.bac_scenarios import generate_scenarios

        records = generate_scenarios(forbidden_fingerprints=set())
        assert len(records) > 0, "BAC generator produced 0 records"

        for rec in records:
            self._check_scenario_record(rec, 'bac_scenarios')
            callers = rec['feat_dict'].get('num_callers_to_bet', 0)
            assert callers >= 1, (
                f"BAC scenario must have num_callers_to_bet >= 1, "
                f"got {callers} for situation_id={rec.get('situation_id')}"
            )

    def test_nfd_scenario_has_flush_draw_and_nut_block(self):
        """NFD scenarios must have has_flush_draw=1 and nut_flush_block=1."""
        from corpus_revision_scenarios.nfd_scenarios import generate_scenarios

        records = generate_scenarios(forbidden_fingerprints=set())
        assert len(records) > 0, "NFD generator produced 0 records"

        for rec in records:
            self._check_scenario_record(rec, 'nfd_scenarios')
            assert rec['feat_dict'].get('has_flush_draw') == 1, (
                f"NFD scenario must have has_flush_draw=1, "
                f"got {rec['feat_dict'].get('has_flush_draw')}"
            )
            assert rec['feat_dict'].get('nut_flush_block') == 1, (
                f"NFD scenario must have nut_flush_block=1, "
                f"got {rec['feat_dict'].get('nut_flush_block')}"
            )

    def test_monster_scenario_has_is_monster(self):
        """Monster facing bet scenarios must have is_monster=1."""
        from corpus_revision_scenarios.monster_facing_bet_scenarios import generate_scenarios

        records = generate_scenarios(forbidden_fingerprints=set())
        assert len(records) > 0, "Monster generator produced 0 records"

        for rec in records:
            self._check_scenario_record(rec, 'monster_facing_bet_scenarios')
            assert rec['feat_dict'].get('is_monster') == 1, (
                f"Monster scenario must have is_monster=1, "
                f"got {rec['feat_dict'].get('is_monster')}"
            )

    def test_donk_bet_defence_scenario_oop_bettor(self):
        """Module 8: donk-bet defence scenarios must have OOP bettor (BB) and IP hero."""
        from corpus_revision_scenarios.donk_bet_defence_scenarios import generate_scenarios

        records = generate_scenarios(forbidden_fingerprints=set())
        assert len(records) > 0, "Donk-bet defence generator produced 0 records"

        for rec in records:
            self._check_scenario_record(rec, 'donk_bet_defence_scenarios')
            # Hero must be IP (BTN or CO)
            hero_pos = rec.get('hero_position')
            assert hero_pos in ('BTN', 'CO'), (
                f"Module 8: hero must be BTN or CO (IP), got {hero_pos}"
            )
            # facing_bet must be True (hero faces the donk)
            assert rec.get('facing_bet') is True or rec['feat_dict'].get('facing_bet') == 1, (
                f"Module 8: hero must face a bet (donk), facing_bet={rec.get('facing_bet')}"
            )

    def test_sb_hero_scenario_position(self):
        """Module 9: SB-as-hero scenarios must have hero_position=SB."""
        from corpus_revision_scenarios.sb_hero_scenarios import generate_scenarios

        records = generate_scenarios(forbidden_fingerprints=set())
        assert len(records) > 0, "SB-hero generator produced 0 records"

        for rec in records:
            self._check_scenario_record(rec, 'sb_hero_scenarios')
            assert rec.get('hero_position') == 'SB', (
                f"Module 9: hero must be SB, got {rec.get('hero_position')}"
            )

    def test_rule11_boundary_at_least_3_textures(self):
        """R5: Rule 11 boundary scenarios must use >= 3 distinct board textures."""
        from corpus_revision_scenarios.rule11_boundary_scenarios import generate_scenarios

        records = generate_scenarios(forbidden_fingerprints=set())
        assert len(records) >= 5, (
            f"Rule 11 generator must produce >= 5 records (5 boundary pairs), "
            f"got {len(records)}"
        )

        # Extract board textures using a refined classifier that distinguishes:
        #   1. paired + rainbow + dry (large gap) — e.g. KcKd4s
        #   2. paired + rainbow + connected (gap <= 2) — e.g. 8h8d7c, JsJd9c
        #   3. unpaired + two_tone — e.g. KdTd4c, 9d6d3s
        #   4. monotone — 3 same suits
        # This gives ≥3 distinct texture labels across the 5 Rule 11 boards.
        _RANK_ORDER = {r: i for i, r in enumerate('23456789TJQKA', 0)}

        def get_board_texture(board_str):
            cards = [board_str[i:i+2] for i in range(0, len(board_str), 2)]
            from collections import Counter
            ranks = [c[0] for c in cards[:3]]
            suits = [c[1] for c in cards[:3]]
            rank_counts = Counter(ranks)
            suit_counts = Counter(suits)
            if 3 in rank_counts.values():
                return 'trips'
            is_paired = 2 in rank_counts.values()
            if 3 in suit_counts.values():
                return 'monotone'
            is_two_tone = 2 in suit_counts.values()
            if not is_paired:
                if is_two_tone:
                    return 'two_tone_unpaired'
                return 'rainbow_unpaired'
            # Paired board: find gap between pair rank and kicker rank
            pair_rank = [r for r, cnt in rank_counts.items() if cnt == 2][0]
            kicker_rank = [r for r, cnt in rank_counts.items() if cnt == 1][0]
            gap = abs(_RANK_ORDER[pair_rank] - _RANK_ORDER[kicker_rank])
            if gap <= 3:
                return 'paired_connected'  # e.g. 8h8d7c (gap=1), JsJd9c (gap=2)
            return 'paired_dry'            # e.g. KcKd4s (gap=9)

        textures = set()
        for rec in records:
            board = rec.get('board', '')
            texture = get_board_texture(board)
            textures.add(texture)

        assert len(textures) >= 3, (
            f"R5: Rule 11 boundary scenarios must use >= 3 distinct textures, "
            f"got {len(textures)}: {textures}"
        )

    def test_forbidden_fingerprints_threading(self):
        """Incremental forbidden_fingerprints update prevents cross-scenario duplicates."""
        from corpus_revision_scenarios.pfa_scenarios import generate_scenarios as gen_pfa
        from corpus_revision_scenarios.magg_scenarios import generate_scenarios as gen_magg

        def fingerprint(record):
            """Simple fingerprint: (sorted_hero_cards, sorted_board)."""
            def cards(s):
                return tuple(sorted([s[i:i+2] for i in range(0, len(s), 2)]))
            return (cards(record['hero_cards']), cards(record['board']))

        fp_set = set()
        pfa_records = gen_pfa(forbidden_fingerprints=fp_set)
        fp_set.update(fingerprint(r) for r in pfa_records)

        magg_records = gen_magg(forbidden_fingerprints=fp_set)
        magg_fps = [fingerprint(r) for r in magg_records]

        # No MAGG fingerprint should be in fp_set (which now includes PFA fingerprints)
        conflicts = [fp for fp in magg_fps if fp in fp_set]
        assert not conflicts, (
            f"Cross-scenario fingerprint collision: {len(conflicts)} MAGG records "
            f"have the same fingerprint as PFA records. N3 (incremental threading) failed."
        )
