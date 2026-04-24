"""MUST #22 + MUST #35 — authored per-fixture action_history sidecar
for reference_evaluator's FB-40 + MW-50 baseline eval paths.

Stage 3.5 Path (c) Phase 1 (commit 6) lands this stub. Phase 2
(commit 13) populates ~90 entries (FB-40 + MW-50) after the same
owner-approval-gated dry-run batch that authors
_calibration_action_history_sidecar.

MUST #35 sentinel is reused from the calibration sidecar module —
single source of truth for identity comparison. Import pattern:

    from _calibration_action_history_sidecar import _SIDECAR_MISSING

Schema (identical to calibration sidecar):
  _REFERENCE_ACTION_HISTORY: Dict[ref_id, List[Tuple[street, position, action]]]

Fixture coverage:
  - FB-01 through FB-40 (facing-bet test set; used by
    reference_evaluator.evaluate_facing_bet_test_set at line ~797)
  - MW-11 through MW-50 (multiway reference set; used by
    reference_evaluator._evaluate_one_hand at line ~473)

Source annotations for authoring:
  - _FB_ACTION_HISTORY prose comments at reference_evaluator.py:630-672
    document each FB fixture's action line in English. Phase 2
    reconstructs structured tuples from those.
  - _ACTION_HISTORY prose comments at reference_evaluator.py:123+
    document each MW fixture. Same reconstruction pattern.
  - BATCH*_HAND_DESIGNS.md source docs provide additional context for
    edge cases not fully captured by the 5-tuple count encoding.

Phase 2 (commit 13) gates:
  - 5-entry dry-run owner-approval batch
  - 10% stratified solver-verify per MUST #54 + #66
  - GTO reviewer pass per batch of 10

Phase 4 cleanup: once canonical JSONL records populate `action_history`
natively (Stage 4 data prep), this sidecar becomes empty + deletable.
"""
from typing import Dict, List, Tuple

# Reuse sentinel from calibration sidecar (single source of truth —
# identity equality only works when importing the same object).
from _calibration_action_history_sidecar import _SIDECAR_MISSING


# MUST #22 Phase 2 authored table. Empty until commit 13's authoring
# phase (owner-approval-gated).
#
# Covers both FB-40 (FB-01..FB-40) and MW-50 (MW-11..MW-50+) fixtures.
# See BUILDER_V24_STAGE35_BLUEPRINT_V2_2_AMENDED_2026-04-22.md §3.2 +
# §5 for sidecar-authoring pattern.
_REFERENCE_ACTION_HISTORY: Dict[str, List[Tuple[str, str, str]]] = {
    # ─────────────────────────────────────────────────────────────────
    # COMMIT 13 Phase 2 — 5-ENTRY DRY-RUN BATCH (owner-approval gated)
    # ─────────────────────────────────────────────────────────────────
    # 5 representative shapes per MUST #49 enumeration. Authored from
    # `_ACTION_HISTORY` prose comments (reference_evaluator.py:123+)
    # + `_FB_ACTION_HISTORY` prose (reference_evaluator.py:630+).
    # Sequence convention: ALL prior-street + same-street actions up to
    # hero's decision. narrow_by_action_history filters to prior
    # postflop streets internally; same-street pre-hero actions
    # excluded per Stage 3.5 spec (calibration-anchor stability).
    #
    # Owner reviews these 5 before remaining ~135 authored (per v2.2
    # amendment §5 mid-lift approval gate).
    #
    # Batch composition (5 diverse shapes):
    #   MW-11 : flop-decision baseline (no prior chain; 3-way)
    #   MW-30 : flop-facing-bet-and-call (facing_bet gate; 3-way key hand)
    #   FB-17 : turn-delayed-cbet (chain fires flop:CHECK)
    #   FB-23 : river-after-check-through (chain fires 2×)
    #   MW-15 : river-check-through (chain fires 2× different villain pos)

    # MW-11: "Flop. CO opens, checks to hero (BB). No bet to call."
    #   action_string: "SB check, BB ???"
    'MW-11': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision street for BB; SB check is same-street-pre-hero.
        ('flop', 'SB', 'CHECK'),
    ],

    # MW-30: "Flop. CO bets, BTN CALLS, hero faces bet+call. Key hand."
    #   action_string: "BB check, CO bet 35, BTN call 35, BB ???"
    'MW-30': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for BB; same-street sequence up to hero action.
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
    ],

    # FB-17: "Turn. CO checked flop, delayed c-bet turn; BTN folded."
    #   action_string (FB): "BB check, CO check, BTN check" (flop) then
    #   turn: BB check, CO bet, BTN fold, BB ???
    'FB-17': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: check-through (primary villain CO checks → chain fires)
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        # Turn decision for BB; same-street sequence up to hero action.
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'BET'),
        ('turn', 'BTN', 'FOLD'),
    ],

    # FB-23: "River. All checked flop+turn; CO first bet on river; BTN folded."
    'FB-23': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: check-through (primary villain CO checks)
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        # Turn: check-through again (primary villain CO checks — chain
        # fires flop:CHECK + turn:CHECK narrowings)
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'CHECK'),
        # River decision for BB
        ('river', 'BB', 'CHECK'),
        ('river', 'CO', 'BET'),
        ('river', 'BTN', 'FOLD'),
    ],

    # MW-15: "River. BB called pf, checked flop+turn. Checks to hero (BTN)."
    #   action_string: "BB check, BTN ???"
    #   Primary villain: BB (hero is BTN).
    'MW-15': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: check-through (primary villain BB checks)
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        # Turn: check-through again (primary villain BB checks — chain
        # fires flop:CHECK + turn:CHECK for villain BB)
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'CHECK'),
        # River decision for BTN; same-street BB check precedes.
        ('river', 'BB', 'CHECK'),
    ],
}


def lookup(ref_id: str):
    """MUST #22 sidecar lookup with MUST #35 sentinel semantics.

    Returns:
      - List[Tuple[str, str, str]]: authored action_history for this
        fixture
      - _SIDECAR_MISSING sentinel: no entry for ref_id (caller applies
        STAGE4_STRICT_ACTION_HISTORY gate)

    Identity comparison (`is _SIDECAR_MISSING`) distinguishes "no
    sidecar entry" from "entry exists with empty list".
    """
    return _REFERENCE_ACTION_HISTORY.get(ref_id, _SIDECAR_MISSING)
