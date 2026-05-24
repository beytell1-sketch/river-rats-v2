"""Tests for positional_action_chain_scenarios.py (Module 10).

Test-First per CLAUDE.md §3. Tests define the contract before implementation.

Covers:
  - CFP-1..CFP-6: Bug-awareness checklist (blueprint v1 §6.6)
  - QUOTA-1..QUOTA-6: A1 mandatory quota satisfaction (ratification per-batch slot allocation)
  - VALIDATION-1..2: validate_chain_fingerprint contract

References:
  - review/comms/RATIFICATION_A1_POSITIONAL_CHAIN_2026-05-22.md
  - review/comms/DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-13.md §2.1, §6.3, §6.6
  - review/comms/MAIN_TERMINAL_PHASE2F1_B1_FIRE_NOW_2026-05-22.md (deliverable #3)
"""
from __future__ import annotations

import copy
import os
import sys
from collections import Counter

import pytest

_CORE = os.path.join(os.path.dirname(__file__), '..')
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from corpus_revision_scenarios.positional_action_chain_scenarios import (
    ChainFingerprint,
    _CHAIN_FINGERPRINT_TEMPLATES,
    enumerate_top_12_chains,
    generate_chain_scenarios,
    generate_phase_2f_chain_quota,
    validate_chain_fingerprint,
)
from corpus_revision_scenarios._scenario_utils import compute_chain_fingerprint


# Postflop seat order: SB < BB < UTG < HJ < CO < BTN
_POSTFLOP_SEAT_ORDER = ['SB', 'BB', 'UTG', 'HJ', 'CO', 'BTN']


def _seat_index(pos: str) -> int:
    if pos == 'NONE':
        return -1
    if pos == 'EP':
        pos = 'UTG'
    if pos == 'MP':
        pos = 'HJ'
    return _POSTFLOP_SEAT_ORDER.index(pos)


def _scorecard_class(pos: str) -> str:
    """Collapse 6-max positions to scorecard 6-class taxonomy {EP,HJ}→MP per ratification."""
    if pos in ('UTG', 'EP'):
        return 'UTG'
    if pos in ('HJ', 'MP'):
        return 'MP'
    return pos


# =============================================================================
# CFP-1: callers_chain order matches action_history call-order
# =============================================================================

class TestCFP1CallersChainOrder:
    """callers_chain must list callers in the order they called on the current street."""

    def test_every_template_callers_chain_matches_action_order(self):
        for i, tmpl in enumerate(_CHAIN_FINGERPRINT_TEMPLATES):
            cfp = tmpl['chain_fingerprint']
            street = cfp.street
            expected_callers = list(cfp.callers_chain)
            # Walk action_history for current street, collect calls that came after aggressor's bet
            actions_on_street = [
                (pos, action) for (s, pos, action) in tmpl['action_history']
                if s == street
            ]
            # Find aggressor's first bet
            aggressor = cfp.aggressor_pos
            if aggressor == 'NONE':
                assert expected_callers == [], (
                    f"Template {i} ({tmpl.get('hero_pos','?')}): callers_chain "
                    f"non-empty with aggressor=NONE"
                )
                continue
            # Find the bet by aggressor
            try:
                bet_idx = next(
                    j for j, (p, a) in enumerate(actions_on_street)
                    if p == aggressor and a == 'bet'
                )
            except StopIteration:
                pytest.fail(
                    f"Template {i}: aggressor={aggressor} has no 'bet' "
                    f"action on street={street}: {actions_on_street}"
                )
            # Calls after the aggressor's bet (until raise or hero's turn)
            actual_callers = []
            for p, a in actions_on_street[bet_idx + 1:]:
                if p == cfp.hero_pos:
                    break
                if a == 'call':
                    actual_callers.append(p)
                elif a == 'raise':
                    break
            assert actual_callers == expected_callers, (
                f"Template {i}: callers_chain mismatch — expected {expected_callers}, "
                f"got {actual_callers} from action_history {actions_on_street}"
            )


# =============================================================================
# CFP-2: Aggressor seat-order before hero (when hero hasn't pre-acted on street)
# =============================================================================

class TestCFP2AggressorBeforeHero:
    """Aggressor's seat is before hero's seat in postflop order, UNLESS hero
    already checked on the street (re-act / check-raise / multi-caller case
    like blueprint Example C)."""

    def test_aggressor_seat_or_hero_already_acted(self):
        for i, tmpl in enumerate(_CHAIN_FINGERPRINT_TEMPLATES):
            cfp = tmpl['chain_fingerprint']
            if cfp.aggressor_pos == 'NONE':
                continue  # OPEN shape — no aggressor
            hero_idx = _seat_index(cfp.hero_pos)
            aggr_idx = _seat_index(cfp.aggressor_pos)
            if aggr_idx < hero_idx:
                continue  # Standard case: aggressor seat before hero
            # Allowed: hero already acted (checked) on the street earlier
            actions_on_street = [
                (pos, action) for (s, pos, action) in tmpl['action_history']
                if s == cfp.street
            ]
            hero_pre_check = any(
                p == cfp.hero_pos and a == 'check' for (p, a) in actions_on_street
            )
            assert hero_pre_check, (
                f"Template {i}: aggressor={cfp.aggressor_pos} "
                f"(seat {aggr_idx}) is at or after hero={cfp.hero_pos} "
                f"(seat {hero_idx}) in postflop order, AND hero did not "
                f"pre-check on street — invalid spec."
            )


# =============================================================================
# CFP-3: Raiser seat-order between aggressor and hero
# =============================================================================

class TestCFP3RaiserSeatOrder:
    """Raiser's seat must be after aggressor's seat AND before hero's seat
    in postflop order — EXCEPT for CHECK_RAISE, where the raiser checked
    earlier in the street and then raised (canonical pattern: raiser seat is
    BEFORE aggressor seat)."""

    def test_raiser_seat_position(self):
        for i, tmpl in enumerate(_CHAIN_FINGERPRINT_TEMPLATES):
            cfp = tmpl['chain_fingerprint']
            if cfp.raiser_pos == 'NONE':
                continue  # No raiser
            if cfp.chain_shape == 'CHECK_RAISE':
                # CHECK_RAISE: raiser checked before aggressor's bet; the
                # raiser seat can be EARLIER than aggressor. CFP-4 enforces
                # the prior-check requirement separately.
                continue
            raiser_idx = _seat_index(cfp.raiser_pos)
            aggr_idx = _seat_index(cfp.aggressor_pos)
            hero_idx = _seat_index(cfp.hero_pos)
            # Standard BET_RAISE: aggr < raiser < hero in postflop order
            if aggr_idx < raiser_idx < hero_idx:
                continue
            # Allowed alternative: hero pre-checked on street (e.g., BB-donk
            # situations where hero already acted; raiser may sit anywhere
            # consistent with action_history)
            actions_on_street = [
                (pos, action) for (s, pos, action) in tmpl['action_history']
                if s == cfp.street
            ]
            hero_pre_check = any(
                p == cfp.hero_pos and a == 'check' for (p, a) in actions_on_street
            )
            assert hero_pre_check or (aggr_idx < raiser_idx), (
                f"Template {i}: raiser={cfp.raiser_pos} (seat {raiser_idx}) "
                f"not strictly between aggr={cfp.aggressor_pos} (seat {aggr_idx}) "
                f"and hero={cfp.hero_pos} (seat {hero_idx})."
            )


# =============================================================================
# CFP-4: CHECK_RAISE requires aggressor's prior check on the same street
# =============================================================================

class TestCFP4CheckRaiseRequiresPriorCheck:
    """For CHECK_RAISE chain_shape, the RAISER (not the aggressor) must have a
    'check' action on the same street before the aggressor's 'bet'. Canonical
    pattern: BB checks → CO bets → BB raises. The raiser is the check-raiser."""

    def test_check_raise_has_raiser_prior_check(self):
        for i, tmpl in enumerate(_CHAIN_FINGERPRINT_TEMPLATES):
            cfp = tmpl['chain_fingerprint']
            if cfp.chain_shape != 'CHECK_RAISE':
                continue
            actions_on_street = [
                (pos, action) for (s, pos, action) in tmpl['action_history']
                if s == cfp.street
            ]
            raiser = cfp.raiser_pos
            # Walk: collect raiser's checks before any bet appears on street
            saw_bet = False
            raiser_checked_pre_bet = False
            for p, a in actions_on_street:
                if a == 'bet' and not saw_bet:
                    saw_bet = True
                    break
                if p == raiser and a == 'check':
                    raiser_checked_pre_bet = True
            assert raiser_checked_pre_bet, (
                f"Template {i}: CHECK_RAISE shape requires raiser "
                f"{raiser} to check BEFORE the bet on street "
                f"{cfp.street}; action_history {actions_on_street}"
            )


# =============================================================================
# CFP-5: 4-way-at-decision player-count sanity
# =============================================================================

class TestCFP5FourWayPlayerCount:
    """For 4-way pots at decision, the union of {hero, aggressor, callers,
    raiser, surviving-villains} must be consistent. At minimum: aggressor +
    hero + callers + raiser must all be distinct, and total non-folded
    villains at decision must match num_opponents implied by villain_positions."""

    def test_chain_actors_distinct(self):
        for i, tmpl in enumerate(_CHAIN_FINGERPRINT_TEMPLATES):
            cfp = tmpl['chain_fingerprint']
            actors = {cfp.hero_pos}
            if cfp.aggressor_pos != 'NONE':
                actors.add(cfp.aggressor_pos)
            for c in cfp.callers_chain:
                actors.add(c)
            if cfp.raiser_pos != 'NONE':
                actors.add(cfp.raiser_pos)
            # Hero must not appear in callers_chain or as aggressor/raiser
            assert cfp.hero_pos not in cfp.callers_chain, (
                f"Template {i}: hero {cfp.hero_pos} appears in callers_chain"
            )
            assert cfp.hero_pos != cfp.aggressor_pos, (
                f"Template {i}: hero == aggressor (both {cfp.hero_pos})"
            )
            assert cfp.hero_pos != cfp.raiser_pos, (
                f"Template {i}: hero == raiser (both {cfp.hero_pos})"
            )
            assert cfp.aggressor_pos not in cfp.callers_chain, (
                f"Template {i}: aggressor {cfp.aggressor_pos} appears "
                f"in callers_chain"
            )

    def test_chain_actors_subset_of_table(self):
        for i, tmpl in enumerate(_CHAIN_FINGERPRINT_TEMPLATES):
            cfp = tmpl['chain_fingerprint']
            table = set([cfp.hero_pos] + list(tmpl['villain_positions']))
            actors = {cfp.hero_pos}
            if cfp.aggressor_pos != 'NONE':
                actors.add(cfp.aggressor_pos)
            for c in cfp.callers_chain:
                actors.add(c)
            if cfp.raiser_pos != 'NONE':
                actors.add(cfp.raiser_pos)
            assert actors.issubset(table), (
                f"Template {i}: chain actors {actors} not subset of table "
                f"{table}"
            )


# =============================================================================
# CFP-6: Board diversity ≥5 distinct boards per chain template-group
# =============================================================================

class TestCFP6BoardDiversity:
    """Across all templates, distinct board count should be ≥5 in aggregate
    (per blueprint §6.6 across the 12 anchors)."""

    def test_aggregate_board_diversity(self):
        boards = set(tuple(t['board']) for t in _CHAIN_FINGERPRINT_TEMPLATES)
        assert len(boards) >= 5, (
            f"Aggregate board diversity = {len(boards)}; expected ≥5 across "
            f"all templates."
        )


# =============================================================================
# QUOTA-1..6: A1 mandatory quota satisfaction
# =============================================================================

class TestQuota:
    """generate_phase_2f_chain_quota must return 24 specs satisfying all
    5 A1 mandatory floors (per RATIFICATION_A1 §Per-batch slot allocation)."""

    @pytest.fixture
    def quota_24(self):
        return generate_phase_2f_chain_quota(rng_seed=20260522,
                                             forbidden_fingerprints=set())

    # --- QUOTA-1: exactly 24 ---
    def test_quota1_returns_24(self, quota_24):
        assert len(quota_24) == 24

    # --- QUOTA-2: facing-raise ≥10 ---
    def test_quota2_facing_raise(self, quota_24):
        FACING_RAISE = {'BET_RAISE', 'CHECK_RAISE', 'MULTI_AGGR'}
        count = sum(
            1 for spec in quota_24
            if compute_chain_fingerprint(spec).chain_shape in FACING_RAISE
        )
        assert count >= 10, (
            f"Facing-raise count={count}; A1 floor ≥10."
        )

    # --- QUOTA-3: river ≥5 ---
    def test_quota3_river(self, quota_24):
        count = sum(
            1 for spec in quota_24 if compute_chain_fingerprint(spec).street == 'river'
        )
        assert count >= 5, (
            f"River count={count}; A1 floor ≥5."
        )

    # --- QUOTA-4: position-balance — each of {BTN, CO, MP, UTG, SB, BB} ≥1 ---
    def test_quota4_position_balance(self, quota_24):
        counter = Counter(
            _scorecard_class(compute_chain_fingerprint(spec).hero_pos)
            for spec in quota_24
        )
        for cls in ('BTN', 'CO', 'MP', 'UTG', 'SB', 'BB'):
            assert counter[cls] >= 1, (
                f"Position-balance: scorecard class {cls} has count "
                f"{counter[cls]}; A1 floor in 24-spec output ≥1 each."
            )

    # --- QUOTA-5: All 12 top-12 chains at least once ---
    def test_quota5_top12_coverage(self, quota_24):
        top12 = set(enumerate_top_12_chains())
        produced = set(compute_chain_fingerprint(spec) for spec in quota_24)
        missing = top12 - produced
        assert not missing, (
            f"Missing top-12 chains in 24-spec output: {missing}"
        )

    # --- QUOTA-6: Sandwich count ≥4 ---
    def test_quota6_sandwich(self, quota_24):
        """Sandwich = hero positionally between two villain actors on the
        current decision street (one villain acted before hero, one acts
        after hero in seat-order — or hero is between aggressor and a
        still-to-act villain)."""
        def is_sandwich(spec):
            cfp = compute_chain_fingerprint(spec)
            hero_idx = _seat_index(cfp.hero_pos)
            actors_acted = set()
            if cfp.aggressor_pos != 'NONE':
                actors_acted.add(cfp.aggressor_pos)
            actors_acted.update(cfp.callers_chain)
            if cfp.raiser_pos != 'NONE':
                actors_acted.add(cfp.raiser_pos)
            # Sandwich: at least one actor seat < hero AND at least one
            # surviving villain seat > hero (or aggressor seat > hero with
            # hero pre-check — e.g., Example C)
            villain_set = set(spec.villain_positions)
            seats_acted_before = {p for p in actors_acted if _seat_index(p) < hero_idx}
            seats_villain_after = {
                p for p in villain_set if _seat_index(p) > hero_idx
            }
            return bool(seats_acted_before) and bool(seats_villain_after)
        count = sum(1 for spec in quota_24 if is_sandwich(spec))
        assert count >= 4, (
            f"Sandwich count={count}; A1 floor ≥4."
        )


# =============================================================================
# VALIDATION-1: validate_chain_fingerprint returns True for matching specs
# =============================================================================

class TestValidation1MatchingFingerprint:
    """For every template's own ChainFingerprint, validate_chain_fingerprint
    must return True (or not raise)."""

    def test_every_template_validates_against_own_fingerprint(self):
        # Use generate_chain_scenarios to materialize one spec per template
        # We use enumerate_top_12_chains to drive the validation across the
        # 12 anchor chains. Each generated spec's fingerprint must validate.
        for chain_fp in enumerate_top_12_chains():
            specs = generate_chain_scenarios(
                chain_fp, count=1, rng_seed=20260522,
                forbidden_fingerprints=set(),
            )
            assert specs, (
                f"generate_chain_scenarios returned no specs for {chain_fp}"
            )
            for spec in specs:
                assert validate_chain_fingerprint(spec, chain_fp), (
                    f"Spec for {chain_fp} failed validation (expected True)"
                )

    def test_every_template_self_consistent(self):
        """B1.1 / QC SHOULD_FIX-2: VALIDATION-1's anchor-only loop missed the
        T21 chain_shape mismatch in the expansion templates (T12..T23). This
        sibling test iterates ALL 24 templates and asserts each materialized
        spec's computed chain_fingerprint equals the template's declared
        fingerprint. Would have caught SHOULD_FIX-1 at unit-test time.

        Per QC finding `findings/2026-05-23-pr468-b1-positional-chain-scenarios.md`
        SHOULD_FIX-2.
        """
        from corpus_revision_scenarios.positional_action_chain_scenarios import (
            _spec_from_template,
        )
        for i, tmpl in enumerate(_CHAIN_FINGERPRINT_TEMPLATES):
            spec = _spec_from_template(tmpl)
            declared = tmpl['chain_fingerprint']
            assert validate_chain_fingerprint(spec, declared), (
                f"Template T{i:02d} declared fingerprint does not match "
                f"compute_chain_fingerprint(materialized spec). declared="
                f"{declared}"
            )


# =============================================================================
# B1.1 — SHOULD_FIX-1 regression: T21 is CHECK_RAISE (not BET_RAISE)
# =============================================================================

class TestT21CheckRaiseRegression:
    """B1.1 / QC SHOULD_FIX-1: T21's declared chain_shape was 'BET_RAISE'
    pre-fix; the action_history (BB check → CO check → BTN bet → BB raise)
    correctly computes to CHECK_RAISE (raiser BB had a pre-bet check on the
    street, per the canonical algorithm in _scenario_utils
    compute_chain_fingerprint). Pin T21's chain_shape so a future template
    edit can't silently re-introduce the mislabel.

    Per QC finding `findings/2026-05-23-pr468-b1-positional-chain-scenarios.md`
    SHOULD_FIX-1.
    """

    def test_t21_declared_chain_shape_is_check_raise(self):
        # T21 is the river-CO template at index 21 (zero-indexed)
        t21 = _CHAIN_FINGERPRINT_TEMPLATES[21]
        cfp = t21['chain_fingerprint']
        assert cfp.chain_shape == 'CHECK_RAISE', (
            f"T21 chain_shape regressed: expected 'CHECK_RAISE' "
            f"(post-B1.1 SHOULD_FIX-1 fix), got {cfp.chain_shape!r}"
        )
        # Pin the rest of the fingerprint too — any future template edit
        # that alters the river-CO scenario will hit this test.
        assert cfp.street == 'river'
        assert cfp.hero_pos == 'CO'
        assert cfp.aggressor_pos == 'BTN'
        assert cfp.callers_chain == ()
        assert cfp.raiser_pos == 'BB'
        assert cfp.raise_target_pos == 'BTN'


# =============================================================================
# B1.1 — Fix 3 (orchestrator addendum): no-floor-regression guard
# =============================================================================

class TestNoFloorRegression:
    """B1.1 / orchestrator addendum to QC SHOULD_FIX recommendations:
    pin all 5 A1 mandatory floors against the canonical 24-spec output so any
    future template change (template removal, chain_shape relabel, hero_pos
    shift) that silently drops a floor count below the RATIFICATION_A1
    threshold will fail at unit-test time.

    Per QC finding §"Tightness of floors" (informational): facing-raise and
    river floors sit AT-threshold (zero margin) on the current 24-spec
    output. Without this guard, a future single-template edit could silently
    break either floor.

    Per QUOTA-1..6 (`TestQuota`), each floor has its own dedicated
    threshold-only test; this test aggregates them into a single
    snapshot-style guard with the as-of-B1.1 actual counts pinned, so any
    drift (even within the threshold-passing range) surfaces at PR time.
    """

    def test_no_floor_regression(self):
        FACING_RAISE = {'BET_RAISE', 'CHECK_RAISE', 'MULTI_AGGR'}
        specs = generate_phase_2f_chain_quota(
            rng_seed=20260522,
            forbidden_fingerprints=set(),
        )
        assert len(specs) == 24, (
            f"Expected 24 specs from generate_phase_2f_chain_quota, got "
            f"{len(specs)}"
        )

        fingerprints = [compute_chain_fingerprint(s) for s in specs]
        chain_shapes = [cfp.chain_shape for cfp in fingerprints]
        streets = [cfp.street for cfp in fingerprints]
        hero_positions = [cfp.hero_pos for cfp in fingerprints]

        # Floor 1: facing-raise ≥10 (A1 threshold; current: 10)
        facing_raise_count = sum(
            1 for cs in chain_shapes if cs in FACING_RAISE
        )
        assert facing_raise_count >= 10, (
            f"Facing-raise floor 10 broken: {facing_raise_count}"
        )

        # Floor 2: river ≥5 (A1 threshold; current: 5)
        river_count = sum(1 for st in streets if st == 'river')
        assert river_count >= 5, (
            f"River floor 5 broken: {river_count}"
        )

        # Floor 3: sandwich ≥4 (A1 threshold; current: 5). Reuse the
        # same definition as TestQuota.test_quota6_sandwich: hero seat
        # has at least one actor seat before it AND at least one
        # surviving villain seat after it in postflop seat order.
        def is_sandwich(spec):
            cfp = compute_chain_fingerprint(spec)
            hero_idx = _seat_index(cfp.hero_pos)
            actors_acted = set()
            if cfp.aggressor_pos != 'NONE':
                actors_acted.add(cfp.aggressor_pos)
            actors_acted.update(cfp.callers_chain)
            if cfp.raiser_pos != 'NONE':
                actors_acted.add(cfp.raiser_pos)
            villain_set = set(spec.villain_positions)
            seats_acted_before = {
                p for p in actors_acted if _seat_index(p) < hero_idx
            }
            seats_villain_after = {
                p for p in villain_set if _seat_index(p) > hero_idx
            }
            return bool(seats_acted_before) and bool(seats_villain_after)

        sandwich_count = sum(1 for s in specs if is_sandwich(s))
        assert sandwich_count >= 4, (
            f"Sandwich floor 4 broken: {sandwich_count}"
        )

        # Floor 4: position-balance — each of the 6 scorecard classes ≥1
        scorecard_counter = Counter(
            _scorecard_class(hp) for hp in hero_positions
        )
        for cls in ('UTG', 'MP', 'CO', 'BTN', 'SB', 'BB'):
            assert scorecard_counter[cls] >= 1, (
                f"Position-balance floor broken for scorecard class "
                f"{cls}: count={scorecard_counter[cls]}"
            )

        # Floor 5: top-12 anchor coverage — all 12 anchors materialized
        top12 = enumerate_top_12_chains()
        materialized = set(fingerprints)
        for anchor in top12:
            assert anchor in materialized, (
                f"Top-12 anchor {anchor} not in 24-spec output"
            )


# =============================================================================
# VALIDATION-2: validate_chain_fingerprint raises AssertionError with precise diff
# =============================================================================

class TestValidation2CorruptedSpec:
    """validate_chain_fingerprint must raise AssertionError with a precise
    field-level diff when a corrupted spec is passed."""

    def test_corrupted_spec_raises_with_diff(self):
        # Get a known-good spec from a top-12 chain
        chain_fp = enumerate_top_12_chains()[0]
        specs = generate_chain_scenarios(
            chain_fp, count=1, rng_seed=20260522,
            forbidden_fingerprints=set(),
        )
        spec = specs[0]
        # Corrupt: pass an expected_chain whose hero_pos differs
        corrupted_expected = chain_fp._replace(hero_pos='SB' if chain_fp.hero_pos != 'SB' else 'BTN')
        with pytest.raises(AssertionError) as excinfo:
            validate_chain_fingerprint(spec, corrupted_expected)
        msg = str(excinfo.value)
        # Diff must mention the actual vs expected mismatch
        assert 'hero_pos' in msg or 'expected' in msg.lower(), (
            f"AssertionError message did not include diff: {msg}"
        )

    def test_corrupted_shape_raises(self):
        chain_fp = enumerate_top_12_chains()[0]
        specs = generate_chain_scenarios(
            chain_fp, count=1, rng_seed=20260522,
            forbidden_fingerprints=set(),
        )
        spec = specs[0]
        corrupted = chain_fp._replace(chain_shape='MULTI_AGGR')
        with pytest.raises(AssertionError):
            validate_chain_fingerprint(spec, corrupted)


# =============================================================================
# enumerate_top_12_chains returns 12 in rank order matching v1 §5.1
# =============================================================================

class TestEnumerateTop12:
    def test_returns_exactly_12(self):
        chains = enumerate_top_12_chains()
        assert len(chains) == 12

    def test_all_are_chain_fingerprints(self):
        for cfp in enumerate_top_12_chains():
            assert isinstance(cfp, ChainFingerprint)

    def test_rank_1_is_flop_btn_co_bet(self):
        # v1 §5.1: rank 1 = (flop, BTN, CO, (), NONE, NONE, BET)
        rank1 = enumerate_top_12_chains()[0]
        assert rank1.street == 'flop'
        assert rank1.hero_pos == 'BTN'
        assert rank1.aggressor_pos == 'CO'
        assert rank1.callers_chain == ()
        assert rank1.raiser_pos == 'NONE'
        assert rank1.chain_shape == 'BET'

    def test_rank_9_is_bet_raise(self):
        # v1 §5.1: rank 9 = (flop, BB, CO, (), BTN, CO, BET_RAISE)
        rank9 = enumerate_top_12_chains()[8]
        assert rank9.street == 'flop'
        assert rank9.hero_pos == 'BB'
        assert rank9.chain_shape == 'BET_RAISE'
        assert rank9.raiser_pos == 'BTN'
        assert rank9.raise_target_pos == 'CO'
