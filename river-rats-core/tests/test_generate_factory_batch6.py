"""
Tests for review/generate_factory_batch6.py (v2.3 supplement generator).

These tests pin the contract per
review/comms/V23_HAND_GENERATION_PLAN_2026-04-16.md §1.2 + §1.3:

1. Every factory spec sets num_opponents=2 (3-way context).
2. Every output record has villain_positions (list of 2),
   hero_position, action_string, street in feat_dict.
3. After json serialisation pass through normalise_situation(),
   street is numeric (0/1/2) and hero_position is numeric (0-5).
4. For the MM_IP_TURN sub-pattern, the flop actions include a
   check-through pattern (primary villain checked flop) so the
   turn decision is genuinely "checked-to" context.

Run from repo root:
    cd river-rats-core && python -m pytest tests/test_generate_factory_batch6.py -v
"""

import os
import sys
import json
import importlib.util
import pytest


_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REPO = os.path.abspath(os.path.join(_CORE, '..'))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

BATCH6_PATH = os.path.join(_REPO, 'review', 'generate_factory_batch6.py')


def _load_batch6():
    """Load the generator module by absolute path (it lives outside package)."""
    if not os.path.exists(BATCH6_PATH):
        pytest.skip(f"generate_factory_batch6.py not yet created at {BATCH6_PATH}")
    # Ensure core is importable during module load
    cwd = os.getcwd()
    os.chdir(_CORE)
    try:
        spec = importlib.util.spec_from_file_location(
            'generate_factory_batch6', BATCH6_PATH
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    finally:
        os.chdir(cwd)


# -----------------------------------------------------------------------------
# Test 1: every factory spec sets num_opponents=2
# -----------------------------------------------------------------------------

def test_num_opponents_set_on_every_spec():
    """
    Every sub-pattern generator must yield SituationSpecs with
    num_opponents=2 (3-way context per plan §1.3).
    """
    mod = _load_batch6()

    # Each sub-pattern exposes a build_<bucket>_specs() callable returning
    # a list of (SituationSpec, hero_cards, description) or similar.
    bucket_builders = mod.BUCKET_BUILDERS
    assert len(bucket_builders) == 10, (
        f"Expected 10 sub-pattern builders, got {len(bucket_builders)}: "
        f"{list(bucket_builders.keys())}"
    )

    for bucket, build_fn in bucket_builders.items():
        specs = build_fn()
        assert len(specs) >= 1, f"{bucket}: builder returned no specs"
        for spec, *_ in specs:
            assert spec.num_opponents == 2, (
                f"{bucket}: spec.num_opponents = {spec.num_opponents}, "
                f"expected 2"
            )


# -----------------------------------------------------------------------------
# Test 2: feat_dict records carry required metadata fields
# -----------------------------------------------------------------------------

def test_feat_dict_has_required_metadata():
    """
    Every generated record (pre-normalisation) must carry
    villain_positions (list of 2), hero_position, action_string, street.
    """
    mod = _load_batch6()

    # generate_one_bucket() runs build_situation + feat_dict assembly
    # and returns the list of raw (pre-normalisation) feat_dicts for the bucket.
    # It does NOT write JSONL.
    sample_bucket = next(iter(mod.BUCKET_BUILDERS))
    records = mod.generate_one_bucket(sample_bucket)
    assert len(records) >= 1, f"{sample_bucket}: no records generated"

    for r in records:
        assert 'villain_positions' in r, (
            f"{sample_bucket}: record missing villain_positions: {list(r.keys())[:20]}"
        )
        assert isinstance(r['villain_positions'], list), (
            f"{sample_bucket}: villain_positions not a list: {r['villain_positions']}"
        )
        assert len(r['villain_positions']) == 2, (
            f"{sample_bucket}: villain_positions length "
            f"{len(r['villain_positions'])} != 2"
        )
        assert 'hero_position' in r, f"{sample_bucket}: missing hero_position"
        assert 'action_string' in r, f"{sample_bucket}: missing action_string"
        assert 'street' in r, f"{sample_bucket}: missing street"


# -----------------------------------------------------------------------------
# Test 3: records serialise with numeric street / hero_position
# -----------------------------------------------------------------------------

def test_records_are_normalised():
    """
    After piping through normalise_situation() and json.dumps +
    json.loads, street is an int and hero_position is an int.
    Mirrors the preflight check the trainer performs on the JSONL.
    """
    mod = _load_batch6()
    from situation_factory import normalise_situation

    sample_bucket = next(iter(mod.BUCKET_BUILDERS))
    records = mod.generate_one_bucket(sample_bucket)
    assert len(records) >= 1

    for r in records:
        normalised = normalise_situation(r)
        line = json.dumps(normalised)
        round_trip = json.loads(line)
        assert isinstance(round_trip['street'], int), (
            f"street not numeric: {round_trip['street']!r}"
        )
        assert round_trip['street'] in (0, 1, 2), (
            f"street out of range: {round_trip['street']}"
        )
        assert isinstance(round_trip['hero_position'], int), (
            f"hero_position not numeric: {round_trip['hero_position']!r}"
        )
        assert round_trip['hero_position'] in range(0, 6), (
            f"hero_position out of range: {round_trip['hero_position']}"
        )


# -----------------------------------------------------------------------------
# Test 4: MM_IP_TURN has checked-to flop context
# -----------------------------------------------------------------------------

def test_mm_ip_turn_action_history_is_checked_to():
    """
    MM_IP_TURN = Medium made, IP, checked-to (Section 1 row 1).
    The flop must have at least one check from the primary villain so that
    the bridge emits villain_checked_back=1, preserving the
    "checked-to" context required by the Section 2 predicate.

    Turn = first action of street is hero facing a check-to (i.e. the
    villain who will be primary on this street already checked the flop).
    """
    mod = _load_batch6()

    specs = mod.BUCKET_BUILDERS['MM_IP_TURN']()
    assert len(specs) >= 1

    for spec_tuple in specs:
        spec = spec_tuple[0]
        flop_actions = [
            (pos, act) for s, pos, act in spec.action_history if s == 'flop'
        ]
        # At least one villain must have checked the flop
        villain_checks = [
            pos for pos, act in flop_actions
            if act == 'check' and pos in spec.villain_positions
        ]
        assert villain_checks, (
            f"MM_IP_TURN: no villain check on flop in action_history. "
            f"flop_actions={flop_actions}"
        )

        # No bet/raise on the flop — this is a check-through context
        aggressive = [
            (pos, act) for pos, act in flop_actions
            if act in ('bet', 'raise')
        ]
        assert not aggressive, (
            f"MM_IP_TURN: flop had aggressive action {aggressive}; "
            f"expected check-through."
        )

        # Hero is in position, i.e. hero_pos postflop order > all villain
        # positions' postflop order.
        from situation_factory import _POSTFLOP_ORDER
        hero_ord = _POSTFLOP_ORDER[spec.hero_pos]
        for vp in spec.villain_positions:
            assert hero_ord > _POSTFLOP_ORDER[vp], (
                f"MM_IP_TURN: hero {spec.hero_pos} (ord={hero_ord}) is "
                f"not IP vs villain {vp} (ord={_POSTFLOP_ORDER[vp]})."
            )
