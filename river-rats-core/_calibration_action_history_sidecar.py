"""MUST #20 + MUST #35 — authored per-fixture action_history sidecar.

Stage 3.5 Path (c) Phase 1 (commit 5) lands this stub. Phase 2
(commit 13) populates ~140 authored entries after 5-entry dry-run
owner-approval gate.

Schema:
  _CALIBRATION_ACTION_HISTORY: Dict[ref_id, List[Tuple[street, position, action]]]
  where:
    - street ∈ {'preflop', 'flop', 'turn', 'river'}
    - position ∈ {'UTG', 'EP', 'HJ', 'MP', 'CO', 'BTN', 'SB', 'BB'}
    - action ∈ {'RAISE', 'CALL', 'FOLD', 'CHECK', 'BET'}
  Entries are prior-street sequences only (decision-street actions
  enter via the facing_bet gate, not the chain — see
  range_narrowing.narrow_by_action_history decision_street arg).

MUST #35 sentinel:
  _SIDECAR_MISSING = object()  # unique identity; never a dict value
  Callers check `entry is _SIDECAR_MISSING` (not `entry == ...`) so
  falsy values (empty list) are distinguished from missing-key state.

Backward compat path during migration:
  Canonical JSONL records may populate `action_history` field natively
  (Phase 4 cleanup); when that happens, sidecar becomes empty + can be
  deleted. Until Phase 4: ReferenceHand.action_history takes precedence
  over sidecar lookup; sidecar covers fixtures that predate the schema
  extension.

Phase 2 authoring (commit 13):
  Reconstruct per-fixture action_history from prose annotations in
  reference_evaluator._ACTION_HISTORY + BATCH*_HAND_DESIGNS.md source
  docs. 5-entry dry-run batch → owner approval gate → ~140-entry full
  authoring with stratified 10% solver-verify per MUST #54 + #66.
"""
from typing import Dict, List, Tuple


# MUST #35 — unique sentinel; identity comparison only.
_SIDECAR_MISSING = object()


# MUST #20 Phase 2 authored table. Empty until commit 13's authoring
# phase (owner-approval-gated).
#
# 5-entry dry-run batch lands first. After owner go/no-go, remaining
# ~135 entries follow. See BUILDER_V24_STAGE35_BLUEPRINT_V2_2_AMENDED_
# 2026-04-22.md §3.2 + §5 for sidecar-authoring pattern.
_CALIBRATION_ACTION_HISTORY: Dict[str, List[Tuple[str, str, str]]] = {
    # ─────────────────────────────────────────────────────────────────
    # COMMIT 13 Phase 2 — 5-ENTRY DRY-RUN BATCH (owner-approval gated)
    # ─────────────────────────────────────────────────────────────────
    # Calibration exam draws from MW-* fixtures. 3 of the 5 dry-run
    # entries are MW-* and belong here; 2 are FB-* and only live in
    # _reference_action_history_sidecar (reference_evaluator path).
    #
    # Mirrors _reference_action_history_sidecar values — single
    # source of truth would be cleaner but intentionally separate per
    # MUST #35 (each pipeline owns its sidecar; miss-sentinel fires
    # at each pipeline's resolver independently).

    # MW-11: "Flop. CO opens, checks to hero (BB). No bet to call."
    'MW-11': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'SB', 'CHECK'),
    ],

    # MW-15: "River. BB called pf, checked flop+turn. Checks to hero (BTN)."
    'MW-15': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'CHECK'),
        ('river', 'BB', 'CHECK'),
    ],

    # MW-30: "Flop. CO bets, BTN CALLS, hero faces bet+call. Key hand."
    'MW-30': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
    ],

    # ─────────────────────────────────────────────────────────────────
    # COMMIT 13.3.3 — MW-12..29 calibration mirrors (first MW batch in
    # the full lift). MW-* entries live in BOTH sidecars per existing
    # convention (MW-11/15/30 pattern). Values are byte-identical to
    # `_REFERENCE_ACTION_HISTORY` for the same ref_id; the cross-sidecar
    # consistency test (test_mw_entries_match_across_sidecars) gates
    # any drift.
    # ─────────────────────────────────────────────────────────────────

    'MW-12': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
    ],
    'MW-13': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
    ],
    'MW-14': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],
    'MW-16': [
        ('preflop', 'HJ', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'HJ', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
    ],
    'MW-17': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],
    'MW-18': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],
    'MW-19': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
    ],
    'MW-20': [
        ('preflop', 'HJ', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),
        ('flop', 'HJ', 'FOLD'),
        ('flop', 'CO', 'FOLD'),
    ],
    'MW-21': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'SB', 'CHECK'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],
    'MW-22': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'SB', 'CHECK'),
    ],
    'MW-23': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
    ],
    'MW-24': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
    ],
    'MW-25': [
        ('preflop', 'HJ', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'HJ', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
    ],
    'MW-26': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
    ],
    'MW-27': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
    ],
    'MW-28': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
    ],
    'MW-29': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'SB', 'CHECK'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],

    # ─────────────────────────────────────────────────────────────────
    # COMMIT 13.3.4 — MW-31..50 calibration mirrors. Byte-identical to
    # _REFERENCE_ACTION_HISTORY entries; gated by
    # test_mw_entries_match_across_sidecars.
    # ─────────────────────────────────────────────────────────────────

    'MW-31': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'BET'),
        ('flop', 'BB', 'FOLD'),
        ('flop', 'CO', 'RAISE'),
    ],
    'MW-32': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
        ('flop', 'BB', 'FOLD'),
        ('turn', 'CO', 'BET'),
    ],
    'MW-33': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'SB', 'CHECK'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
        ('flop', 'SB', 'FOLD'),
    ],
    'MW-34': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
    ],
    'MW-35': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
    ],
    'MW-36': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
    ],
    'MW-37': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
    ],
    'MW-38': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),
        ('flop', 'CO', 'FOLD'),
    ],
    'MW-39': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
    ],
    'MW-40': [
        ('preflop', 'HJ', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'HJ', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
    ],
    'MW-41': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
        ('flop', 'BB', 'CALL'),
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'BET'),
    ],
    'MW-42': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
        ('flop', 'BB', 'FOLD'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'BET'),
        ('turn', 'CO', 'CALL'),
        ('river', 'CO', 'CHECK'),
    ],
    'MW-43': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'SB', 'CHECK'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        ('turn', 'SB', 'CHECK'),
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'CHECK'),
        ('river', 'SB', 'CHECK'),
        ('river', 'BB', 'CHECK'),
        ('river', 'CO', 'BET'),
        ('river', 'BTN', 'FOLD'),
        ('river', 'SB', 'FOLD'),
    ],
    'MW-44': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),
        ('flop', 'CO', 'CALL'),
        ('flop', 'BTN', 'CALL'),
        ('turn', 'BB', 'BET'),
        ('turn', 'CO', 'FOLD'),
    ],
    'MW-45': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'SB', 'CHECK'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        ('turn', 'SB', 'CHECK'),
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'BET'),
        ('turn', 'BTN', 'FOLD'),
        ('turn', 'SB', 'FOLD'),
    ],
    'MW-46': [
        ('preflop', 'HJ', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'HJ', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
        ('flop', 'BB', 'FOLD'),
        ('flop', 'HJ', 'FOLD'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'BET'),
        ('turn', 'CO', 'CALL'),
        ('river', 'CO', 'CHECK'),
        ('river', 'BTN', 'BET'),
        ('river', 'CO', 'RAISE'),
    ],
    'MW-47': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'SB', 'CHECK'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
    ],
    'MW-48': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'SB', 'CHECK'),
    ],
    'MW-49': [
        ('preflop', 'HJ', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'HJ', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'BET'),
        ('flop', 'BB', 'CALL'),
        ('flop', 'HJ', 'FOLD'),
        ('flop', 'CO', 'CALL'),
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
    ],
    'MW-50': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'SB', 'CHECK'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'RAISE'),
        ('flop', 'SB', 'FOLD'),
        ('flop', 'BB', 'CALL'),
        ('flop', 'CO', 'CALL'),
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'BET'),
    ],
}


def lookup(ref_id: str):
    """MUST #20 sidecar lookup with MUST #35 sentinel semantics.

    Returns:
      - List[Tuple[str, str, str]]: authored action_history for this
        fixture (non-empty list)
      - _SIDECAR_MISSING sentinel: no entry for ref_id (caller applies
        STAGE4_STRICT_ACTION_HISTORY gate)

    Does NOT return an empty list for missing — that would be ambiguous
    with legitimate "no prior-street actions" (e.g., flop-decision
    fixtures where hero is first to act postflop). The sentinel is the
    only way to distinguish "no sidecar entry" from "entry exists with
    empty list."
    """
    return _CALIBRATION_ACTION_HISTORY.get(ref_id, _SIDECAR_MISSING)
