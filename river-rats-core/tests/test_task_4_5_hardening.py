"""Task 4.5 — Logic hardening bundle test guards.

Phase 3 HIGH-1/2/3 + Phase 1 HIGH (audit-runner immutability) regression
tests. These are PERMANENT GUARDS — keep in canonical suite.

Per `MAIN_TERMINAL_QC_PHASE3_ACK_TASK4_5_DIRECTIVE_2026-04-26.md` and
`QC_FINDING_COMMIT14_ARCH_STRESS_2026-04-26.md`.

Coverage:
  HIGH-1 — STREET_NAME_MAP whitelist-or-raise via _normalise_street
  HIGH-2 — classify_hand raises ValueError on unrecognised notation
  HIGH-3 — _chain_cache key includes action_history hash (cache-poisoning
           regression test; this is the PILOT-DISPATCH GATE guard)
  Phase 1 — audit runner --out flag with timestamped default
"""
from __future__ import annotations

import datetime as _dt
import os
import sys
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import feature_extractor as fe  # noqa: E402
from range_narrowing import classify_hand  # noqa: E402


# ---------------------------------------------------------------------------
# HIGH-1: STREET_NAME_MAP whitelist-or-raise
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ('street_raw', 'expected'),
    [
        ('f', 'flop'),
        ('t', 'turn'),
        ('r', 'river'),
        ('F', 'flop'),
        ('T', 'turn'),
        ('R', 'river'),
        ('flop', 'flop'),
        ('turn', 'turn'),
        ('river', 'river'),
        ('FLOP', 'flop'),
        ('TURN', 'turn'),
        ('RIVER', 'river'),
        # whitespace tolerated via .strip().lower()
        (' flop ', 'flop'),
        ('Turn', 'turn'),
    ],
)
def test_high1_normalise_street_accepts_known_forms(street_raw, expected):
    """All single-char and full-word variants (case-insensitive) map
    correctly. Replaces silent-default `.get(street_raw, 'flop')`."""
    assert fe._normalise_street(street_raw) == expected


@pytest.mark.parametrize(
    'street_raw',
    ['preflop', 'PREFLOP', 'BOGUS', '', 'flopp', 'rivers', None, 0, 1, 2, 3],
)
def test_high1_normalise_street_raises_on_unknown(street_raw):
    """Anything outside the whitelist raises ValueError (vs silently
    coercing to 'flop'). 'preflop' specifically tested — was a reported
    failure mode."""
    with pytest.raises(ValueError, match='Unrecognised street'):
        fe._normalise_street(street_raw)


# ---------------------------------------------------------------------------
# HIGH-2: classify_hand raises on unrecognised notation
# ---------------------------------------------------------------------------

_BOARD = ['Ks', '7h', '2d']


@pytest.mark.parametrize(
    'notation',
    ['AKs', 'AKo', 'AK', 'JJ', '72o', '22', 'AhKs', '7h2d'],
)
def test_high2_classify_hand_accepts_valid_notation(notation):
    """Valid preflop notation forms ('AKs'/'AKo'/'AK'/'JJ') and 4-char
    specific-card forms still classify without raising."""
    classification = classify_hand(notation, _BOARD)
    assert classification is not None
    assert classification.category in {
        'nuts', 'strong_value', 'good_value', 'draw',
        'medium_made', 'weak_made', 'bluff', 'air',
    }


@pytest.mark.parametrize(
    'notation',
    ['BOGUS', '', 'A', 'AAA', 'XY', '1Ks', '?2', None, 123, 'JJo', 'JJs'],
)
def test_high2_classify_hand_raises_on_invalid_notation(notation):
    """Previously these silently classified to 'air'/'weak_made'/
    'strong_value'. Now they raise ValueError so corrupt range keys
    surface loudly. Includes 'JJo'/'JJs' (pairs cannot carry s/o
    modifier)."""
    with pytest.raises(ValueError, match='Unrecognised hand notation'):
        classify_hand(notation, _BOARD)


def test_high2_extract_all_features_does_not_crash_on_clean_input():
    """`extract_all_features` should NOT crash on a normal HU hand;
    composition extraction now wraps classify_hand in try/except
    ValueError + log + skip rather than the prior bare except. Internal
    range builders only emit valid notation, so this end-to-end path
    is exercised without tripping the skip-on-corrupt-key branch."""
    hand = {
        'h': 'AhKd', 'b': 'Ks7h2d', 'pos': 'BTN', 'vp': 'BB',
        'pot': 10.0, 'tc': 5.0, 'st': 'f', 'fb': 1, 'exp': 'C',
    }
    features = fe.extract_all_features(hand)
    # Composition features are present and finite (or NaN, which is
    # also valid per MUST #10 NaN-flagging contract — but not a crash).
    for key in ('villain_top_pair_plus_pct', 'villain_air_pct'):
        assert key in features


# ---------------------------------------------------------------------------
# HIGH-3: cache key includes action_history hash (PILOT GATE)
# ---------------------------------------------------------------------------

def test_high3_action_history_cache_key_distinguishes_mutations():
    """Helper sanity check: different action histories MUST yield
    different cache-key tuples. Tuple form + dict form both supported."""
    ah_a = [('preflop', 'CO', 'RAISE'), ('preflop', 'BB', 'CALL')]
    ah_b = [('preflop', 'CO', 'RAISE'), ('preflop', 'BB', 'CALL'),
            ('flop', 'BB', 'CHECK')]
    ah_c = [('preflop', 'CO', 'RAISE'), ('preflop', 'BB', 'CALL'),
            ('flop', 'BB', 'BET')]
    k_a = fe._action_history_cache_key(ah_a)
    k_b = fe._action_history_cache_key(ah_b)
    k_c = fe._action_history_cache_key(ah_c)
    assert k_a != k_b
    assert k_b != k_c
    assert k_a != k_c
    # Empty / None
    assert fe._action_history_cache_key(None) == ()
    assert fe._action_history_cache_key([]) == ()
    # Dict form yields stable canonical keys
    ah_d = [{'street': 'preflop', 'position': 'CO', 'action': 'RAISE'}]
    k_d = fe._action_history_cache_key(ah_d)
    assert k_d != ()


def _turn_decision_hand(action_history):
    """Build a turn-decision hand dict with the given _action_history.

    Turn-decision is required so prior-street (flop) actions enter
    `narrow_by_action_history`'s chain (same-street actions are
    excluded by design per Stage 3.5 spec — they go through the
    current-street facing_bet gate, not the chain)."""
    return {
        'h': 'AhKd',
        'b': 'Ks7h2d6c',  # 4 cards = turn board
        'pos': 'BTN',
        'vp': 'BB',
        'pot': 10.0,
        'tc': 0.0,
        'st': 't',
        'fb': 0,
        'exp': 'C',
        '_hero_pos_raw': 'BTN',
        '_villain_pos_raw': 'BB',
        '_street_raw': 't',
        '_opener_position': 'BTN',
        '_action_history': list(action_history),
    }


def test_high3_cache_invalidation_on_mutated_action_history():
    """PERMANENT GUARD — Stage 4 pilot dispatch gate.

    Two consecutive `extract_all_features` calls on the SAME hand dict
    with mutated `_action_history` MUST return different `chain_steps`
    (and hence different composition / villain-folded sentinels). Prior
    to the HIGH-3 fix, the cache key omitted action_history → the
    second call returned the cached stale result from the first.

    Uses a TURN decision so prior-street (flop) actions enter the
    chain. This test FAILS on pre-fix code and PASSES on Task 4.5."""
    # First extraction: BB checked the flop (a real prior-street action
    # → enters the chain → produces 'BB:CHECK' chain step on a turn
    # decision).
    hand = _turn_decision_hand([
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
    ])
    feats_1 = fe.extract_all_features(hand)
    chain_steps_1 = list(feats_1.get('_villain_range_chain_steps', []))

    # Mutate action_history IN-PLACE on the same hand object — the
    # exact pattern a pilot agent would use across street decisions.
    # BB now BET the flop instead of checking → different chain.
    hand['_action_history'] = [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),
    ]
    feats_2 = fe.extract_all_features(hand)
    chain_steps_2 = list(feats_2.get('_villain_range_chain_steps', []))

    assert chain_steps_1, (
        'sanity: first extraction must produce non-empty chain_steps '
        '(prior-street BB:CHECK should enter the chain on a turn decision)'
    )
    assert chain_steps_1 != chain_steps_2, (
        'HIGH-3 cache poisoning regression: extract_all_features returned '
        'identical chain_steps despite mutated _action_history. '
        'Cache key must include action_history hash. '
        f'chain_steps_1={chain_steps_1!r} chain_steps_2={chain_steps_2!r}'
    )


def test_high3_cache_invalidation_distinguishes_check_vs_bet():
    """Stronger variant of the regression guard: independent hand dicts
    sharing one `_chain_cache` (simulating a pilot agent that re-uses
    the cache across hands) with the SAME (villain_pos, num_opponents)
    but DIFFERENT action_history. Different histories MUST produce
    different chain output; pre-fix code would have collided on the
    (hu, BB) cache key and returned identical results."""
    hand_check = _turn_decision_hand([
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
    ])
    hand_bet = _turn_decision_hand([
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),
    ])
    # Shared cache dict simulates an adversarial cache-reuse pattern.
    shared_cache = {}
    hand_check['_chain_cache'] = shared_cache
    hand_bet['_chain_cache'] = shared_cache

    feats_check = fe.extract_all_features(hand_check)
    feats_bet = fe.extract_all_features(hand_bet)

    cs_check = list(feats_check.get('_villain_range_chain_steps', []))
    cs_bet = list(feats_bet.get('_villain_range_chain_steps', []))
    assert cs_check, 'sanity: CHECK extraction must produce chain_steps'
    assert cs_bet, 'sanity: BET extraction must produce chain_steps'
    assert cs_check != cs_bet, (
        'HIGH-3 regression: CHECK vs BET produced identical chain_steps '
        f'(cs_check={cs_check!r} cs_bet={cs_bet!r}). Cache key must '
        'distinguish action_history.'
    )


# ---------------------------------------------------------------------------
# Phase 1 HIGH: audit-runner --out flag with timestamped default
# ---------------------------------------------------------------------------

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_REVIEW_COMMS = os.path.join(_REPO_ROOT, 'review', 'comms')


def test_phase1_anchor_runner_default_path_is_timestamped():
    """The anchor recheck runner's default output path now contains a
    UTC timestamp and lives in review/comms/ (was a hard-coded
    2026-04-20 path that re-runs silently overwrote)."""
    full_path = os.path.join(_REPO_ROOT, 'review', 'run_v231_anchor_recheck_stage35.py')
    with open(full_path) as f:
        src = f.read()
    assert "--out" in src, 'anchor runner missing --out flag'
    assert "RERUN_run_v231_anchor_recheck_stage35_" in src, (
        'anchor runner default path missing timestamped RERUN_ prefix'
    )
    assert "strftime" in src, (
        'anchor runner default path missing strftime timestamp'
    )


def test_phase1_backfill_runner_default_path_is_timestamped():
    """Same guard for the backfill audit runner."""
    full_path = os.path.join(_REPO_ROOT, 'review', 'run_stage35_backfill_audit.py')
    with open(full_path) as f:
        src = f.read()
    assert "--out" in src, 'backfill runner missing --out flag'
    assert "RERUN_run_stage35_backfill_audit_" in src, (
        'backfill runner default path missing timestamped RERUN_ prefix'
    )
    assert "strftime" in src, (
        'backfill runner default path missing strftime timestamp'
    )


def test_phase1_anchor_runner_default_path_function_returns_unique_paths():
    """`_default_report_path` returns distinct timestamped paths on
    successive calls (full guard against accidental collision)."""
    import importlib.util
    full_path = os.path.join(_REPO_ROOT, 'review', 'run_v231_anchor_recheck_stage35.py')
    spec = importlib.util.spec_from_file_location('anchor_runner_under_test', full_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    p1 = mod._default_report_path()
    time.sleep(1.05)  # ensure timestamp ticks (resolution = seconds)
    p2 = mod._default_report_path()
    assert p1 != p2, f'default paths collided: {p1!r} vs {p2!r}'
    assert _REVIEW_COMMS in p1
    assert p1.endswith('.md')


def test_phase1_backfill_runner_default_path_function_returns_unique_paths():
    import importlib.util
    full_path = os.path.join(_REPO_ROOT, 'review', 'run_stage35_backfill_audit.py')
    spec = importlib.util.spec_from_file_location('backfill_runner_under_test', full_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    p1 = mod._default_report_path()
    time.sleep(1.05)
    p2 = mod._default_report_path()
    assert p1 != p2, f'default paths collided: {p1!r} vs {p2!r}'
    assert _REVIEW_COMMS in p1
    assert p1.endswith('.md')
