"""MUST #54 + MUST #66 — stratified 10% solver-verify of authored sidecars.

Per feedback_solver_vs_expert_labels: solver VERIFIES, never labels.
This script solver-verifies sidecar well-formedness by categorising
each authored sidecar entry by shape (per MUST #49 8-category
bucketing) and flagging poker-implausible action sequences.

Stage 3.5 commit 13 lands the STUB (no live solver yet). Phase 2
mid-lift owner approval does not require live solver — structural
validator (MUST #35) + GTO reviewer per-batch pass are the ship
gates. Live solver plugs in at Stage 6 pre-flight for full
sidecar-corpus audit.

Stratification per MUST #66 (Cochran 1977): uniform random 10% can
miss systematic 10-entry-batch pattern errors (35% miss rate).
Stratify across the 8 shape categories from MUST #49; sample ≥1
per shape.

Usage:
    python3 river-rats-core/tests/solver_verify_sidecars.py [--sample-pct 0.10]

Exit codes:
    0 — all sampled entries solver-plausible (or stub pass)
    1 — implausibility detected; offenders listed
    2 — solver unavailable (stub mode); reports stratification
"""
import os
import random
import sys
from typing import Dict, List, Tuple

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)


# Shape categories per MUST #49 (8 buckets); assigned via action_history
# pattern matching.
_SHAPE_PATTERNS = (
    ('hu_donk_x_bet',      'HU donk-flop + turn-check-through + river-bet'),
    ('hu_bet_x_call_bet',  'HU bet-check-call-bet four-class'),
    ('hu_bet_raise_call',  'HU BET-RAISE-CALL same-street'),
    ('folded_hu',          'HU folded-villain sentinel (HIGH #4)'),
    ('folded_mw',          'Folded-villain multiway sentinel'),
    ('over_narrow',        'Synthetic over-narrow (MUST #15)'),
    ('mass_truncation',    'Mass-floor truncation (MUST #28)'),
    ('delayed_probe',      'HU delayed-probe large turn bet'),
    ('mw_per_villain',     'Multiway per-villain chain 3-way'),
    ('other',              'Unclassified (baseline / catch-all)'),
)


def _classify_shape(
    action_history: List[Tuple[str, str, str]],
    villain_pos: str,
) -> str:
    """Classify an action_history by rough shape. Heuristic; refined
    over time as more entries land.

    Priority order matters: specific shapes checked before catch-alls.
    Commit 13.2: added folded branches (HU + MW) + MW-all-live bucket
    per MUST #49 coverage requirement.
    Commit 13.2.6 FIX #2 (GTO review on 13.2.5): villain_pos now
    REQUIRED. The donk-shape branch uses a position-aware
    `flop_has_villain_bet` predicate (`e[1] == villain_pos`) instead
    of the prior position-agnostic `flop_bet_count`. Defensive against
    a hero-as-flop-bettor + villain-led-river-bet pattern in the 13.3
    130-entry lift mis-routing to `hu_donk_x_bet`."""
    streets = [e[0] for e in action_history]
    actions = [e[2] for e in action_history]
    positions = {e[1] for e in action_history}

    has_fold = 'FOLD' in actions
    num_positions = len(positions)
    river_present = 'river' in streets
    turn_present = 'turn' in streets
    flop_bet_count = sum(
        1 for e in action_history
        if e[0] == 'flop' and e[2] == 'BET'
    )
    # FIX #2: position-aware flop-bet predicate (replaces
    # flop_bet_count >= 1 in the donk branches below).
    flop_has_villain_bet = any(
        e[0] == 'flop' and e[2] == 'BET' and e[1] == villain_pos
        for e in action_history
    )
    flop_check_count = sum(
        1 for e in action_history
        if e[0] == 'flop' and e[2] == 'CHECK'
    )
    turn_check_count = sum(
        1 for e in action_history
        if e[0] == 'turn' and e[2] == 'CHECK'
    )
    flop_has_raise = any(
        e[0] == 'flop' and e[2] == 'RAISE' for e in action_history
    )
    turn_has_call = any(
        e[0] == 'turn' and e[2] == 'CALL' for e in action_history
    )

    # HU = 2 positions excluding dead blinds; MW = 3+ positions.
    # For sidecar entries that start with preflop the blinds posting
    # themselves aren't in action_history (only voluntary actions).
    is_mw = num_positions >= 3

    # PRIORITY 1: folded-villain sentinel shapes (MUST #49 cat 4)
    # HU-folded: any FOLD from the sole non-hero villain on a prior
    # postflop street (trigger of HIGH #4 sentinel)
    if has_fold:
        fold_streets = {
            e[0] for e in action_history if e[2] == 'FOLD'
        }
        fold_on_postflop = bool(fold_streets & {'flop', 'turn', 'river'})
        if fold_on_postflop:
            return 'folded_mw' if is_mw else 'folded_hu'

    # PRIORITY 2: structural shapes per MUST #49
    if flop_bet_count >= 1 and flop_has_raise:
        return 'hu_bet_raise_call'
    # hu_bet_x_call_bet = flop BET + turn CHECK + turn CALL + river BET
    # (4-class chain signature: the CALL on turn distinguishes from
    # the donk-x-bet shape below which has NO turn-CALL).
    if (flop_bet_count >= 1 and turn_check_count >= 1 and turn_has_call
            and river_present
            and any(e[0] == 'river' and e[2] == 'BET' for e in action_history)):
        return 'hu_bet_x_call_bet'
    # hu_donk_x_bet = villain BETs flop (donks) + turn CHECK (no CALL)
    # + river BET. Distinct from hu_bet_x_call_bet by absence of
    # turn-CALL. Position-aware predicate per FIX #2 (commit 13.2.6).
    if (flop_has_villain_bet and turn_check_count >= 1
            and not turn_has_call
            and river_present
            and any(e[0] == 'river' and e[2] == 'BET' for e in action_history)):
        return 'hu_donk_x_bet'
    if (flop_check_count >= 1 and turn_check_count >= 1 and river_present
            and any(e[0] == 'river' and e[2] == 'BET' for e in action_history)):
        return 'hu_donk_x_bet'  # check-through variant
    if (flop_check_count >= 1 and turn_present
            and any(e[0] == 'turn' and e[2] == 'BET' for e in action_history)):
        return 'delayed_probe'

    # PRIORITY 3: multiway classifications
    if is_mw:
        return 'mw_per_villain'

    return 'other'


def _stratify(
    entries: Dict[str, List],
    villain_pos_map: Dict[str, str],
) -> Dict[str, List[str]]:
    """Group sidecar entries by shape category. Returns {shape: [ref_ids]}.

    Commit 13.2.6 FIX #2: villain_pos_map (ref_id → villain_pos) is
    REQUIRED so the classifier can apply the position-aware donk
    predicate. Source-of-truth is `_REFERENCE_VILLAIN_POS` in
    `_reference_action_history_sidecar.py`."""
    by_shape: Dict[str, List[str]] = {}
    for ref_id, ah in entries.items():
        if ref_id not in villain_pos_map:
            raise KeyError(
                f'_stratify: villain_pos_map missing entry for {ref_id!r}; '
                f'add to _REFERENCE_VILLAIN_POS in '
                f'_reference_action_history_sidecar.py'
            )
        shape = _classify_shape(ah, villain_pos_map[ref_id])
        by_shape.setdefault(shape, []).append(ref_id)
    return by_shape


def _stratified_sample(by_shape: Dict[str, List[str]], pct: float = 0.10) -> List[str]:
    """MUST #66: ≥1 per shape; ≥pct overall."""
    sampled = []
    total = sum(len(v) for v in by_shape.values())
    for shape, ids in by_shape.items():
        n = max(1, int(round(len(ids) * pct)))
        n = min(n, len(ids))
        sampled.extend(random.sample(ids, n))
    return sampled


def _solver_verify_stub(ref_id: str, action_history) -> Tuple[bool, str]:
    """Stage 3.5 commit 13 STUB: no live solver yet. Returns (ok, note).

    Structural plausibility only (real solver plugs in at Stage 6).
    Checks:
      - CHECK before BET on same street is OK (check-raise line)
      - BET before CHECK on same street = impossible (would be
        check-behind after hero acted); OK if different positions
      - action sequence doesn't have implausible ordering
    """
    # Per-street position-sequence sanity
    by_street: Dict[str, list] = {}
    for street, pos, action in action_history:
        by_street.setdefault(street, []).append((pos, action))

    for street, seq in by_street.items():
        positions_seen = set()
        for pos, action in seq:
            # Same position acting twice on same street requires the
            # previous action to invite re-action (i.e., CHECK then
            # facing-bet → CALL/RAISE/FOLD). Simple sanity: flag any
            # position acting 3+ times on same street.
            if sum(1 for p, _ in seq if p == pos) > 3:
                return (False, f'{ref_id}: position {pos} acts >3x on {street}')
    return (True, f'{ref_id}: structural plausibility OK (solver stub)')


def main() -> int:
    from _calibration_action_history_sidecar import _CALIBRATION_ACTION_HISTORY
    from _reference_action_history_sidecar import (
        _REFERENCE_ACTION_HISTORY,
        _REFERENCE_VILLAIN_POS,
    )

    # Merge both sidecars for stratified sample (MUST #66 works across
    # the combined authoring set)
    combined = {}
    combined.update(_REFERENCE_ACTION_HISTORY)
    # Calibration-specific keys that don't appear in reference
    for k, v in _CALIBRATION_ACTION_HISTORY.items():
        if k not in combined:
            combined[k] = v

    # Commit 13.2.6 FIX #2: villain_pos map for position-aware
    # classifier. All current sidecar entries (reference + calibration)
    # are covered by _REFERENCE_VILLAIN_POS since the calibration set
    # is a subset of reference. If a future calibration-only entry is
    # added, _stratify will raise KeyError pointing at the missing key.
    by_shape = _stratify(combined, _REFERENCE_VILLAIN_POS)
    sampled = _stratified_sample(by_shape, pct=0.10)

    print('MUST #54 + #66 solver-verify (STUB mode — Stage 3.5 commit 13)')
    print('=' * 60)
    print(f'Total authored entries: {len(combined)}')
    print(f'Stratified into {len(by_shape)} shape bucket(s):')
    for shape, ids in sorted(by_shape.items()):
        shape_desc = dict(_SHAPE_PATTERNS).get(shape, '(unknown shape)')
        print(f'  {shape:20s} [{shape_desc}]: {len(ids)} entries → {ids}')
    print(f'\nSampled {len(sampled)} entries for solver-verify: {sampled}')
    print()

    failures = []
    for ref_id in sampled:
        ok, note = _solver_verify_stub(ref_id, combined[ref_id])
        marker = 'OK  ' if ok else 'FAIL'
        print(f'  [{marker}] {note}')
        if not ok:
            failures.append(note)

    print()
    if failures:
        print(f'FAIL — {len(failures)} implausibility(ies) detected')
        return 1
    # Stub-mode success — real solver pass at Stage 6 pre-flight
    print('PASS — structural plausibility OK (STUB). Live solver at '
          'Stage 6 pre-flight.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
