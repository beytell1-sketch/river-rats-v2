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

═══════════════════════════════════════════════════════════════════
AUTHORING SPEC — COMMIT 13.2.5 FIX #4 BOARD-FORMAT CLARIFICATION
═══════════════════════════════════════════════════════════════════

**Sidecar stores action_history ONLY — not boards.**

The board for each fixture lives in:
  - Real fixture (MW-*/FB-*): the canonical JSONL record's `board`
    field (reference_evaluator.py reads it into ReferenceHand.board
    as a concatenated string like 'Kh7d2c')
  - Synthetic fixture (SYN-*): per-test `fixture_meta` dict in the
    test harness (e.g., `tests/test_commit13_sidecar_dryrun.py`
    fixture_meta block), stored as LIST-OF-STRINGS format:
    `['Kh', '7d', '2c']` — NOT concatenated `'Kh7d2c'`.

**Format enforcement:**
  - MUST #35 structural validator checks sidecar action_history shape
  - Separate fixture_meta board-format check added in commit 13.2.5
    (see validate_fixture_meta_boards in validate_sidecar_completeness.py)
  - Per-batch GTO reviewer catches format drift as final gate

**Canonical types:**
  action_history entry : Tuple[str, str, str]
    e.g. ('flop', 'BB', 'CHECK')
  fixture_meta entry  : Tuple[board_list, villain_pos, decision_street, expects_chain_fire]
    board_list : List[str]
    e.g. (['Kh', '7d', '2c'], 'CO', 'flop', False)
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

    # ─────────────────────────────────────────────────────────────────
    # COMMIT 13.2 — 2ND DRY-RUN BATCH (synthetic deferred shapes)
    # ─────────────────────────────────────────────────────────────────
    # 5 synthetic entries covering shapes not reachable via real FB-*/
    # MW-* ref-IDs in commit-13 batch. Keys prefixed SYN- so sentinel
    # semantics hold + reviewer can distinguish real vs synthetic.
    #
    # Per-batch GTO review requested on these 5. Covers all 8 MUST #49
    # shape categories once combined with commit-13 batch:
    #   Category 4 (folded_mw → folded HU) : SYN-F3_HU_folded
    #   Category 5 (over_narrow)           : SYN-F5_HU_overflow (MUST #15 pathway)
    #   Category 2 (hu_bet_x_call_bet)     : SYN-T_J02_synthetic (4-class chain)
    #   Category 3 (hu_bet_raise_call)     : SYN-T_B05_synthetic (same-street BET-RAISE-CALL)
    #   Category 8 (mw_per_villain all-live): SYN-F6_MW_all_live (3-way no folds)

    # SYN-F3_HU_folded: HU folded-villain sentinel (villain_folded=True).
    # Chain terminates at ':FOLD' on flop; narrow_by_action_history
    # returns ({}, {'chain_steps': [..., 'flop:FOLD'], ...}).
    # extract_range_composition then detects villain_folded=True per
    # HIGH #4 sentinel path.
    'SYN-F3_HU_folded': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'BB', 'CALL'),
        # Flop: BB folds (shouldn't normally happen without a bet, but
        # synthetic test drives the sentinel path). Decision street is
        # any subsequent street; chain will short-circuit on first
        # FOLD encountered.
        ('flop', 'BB', 'FOLD'),
    ],

    # SYN-F5_HU_overflow: HU over-narrow via MUST #15 pathway (chain
    # returns empty WITHOUT :FOLD). Deep chain of narrowing steps that
    # compound to zero surviving mass when applied to the sample range.
    # Distinct from SYN-F2 (MUST #28 floor-truncation path) — this
    # triggers the bare `if not v_range:` without-FOLD branch in
    # extract_range_composition.
    #
    # Board is dry double-paired to force high attrition through narrow
    # steps. Deep chain compounds mass loss via CHECK-CALL collapses.
    # Applied to e.g. a draw-heavy preflop range → can produce empty
    # range without :FOLD step.
    #
    # FIX #2 (commit 13.2.5, GTO review): chain is 2 steps (flop:CALL
    # + turn:CALL), not 3. River is the DECISION STREET and is
    # excluded from the chain per narrow_by_action_history's
    # decision_street gate; river's :BET entry enters via facing_bet
    # filter, not the postflop-chain loop.
    'SYN-F5_HU_overflow': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'BTN', 'BET'),
        ('flop', 'BB', 'CALL'),   # chain step 1: flop:CALL (post-MUST-#11 collapse of CHECK-CALL → CALL only)
        ('turn', 'BB', 'CHECK'),
        ('turn', 'BTN', 'BET'),
        ('turn', 'BB', 'CALL'),   # chain step 2: turn:CALL
        ('river', 'BB', 'BET'),    # DECISION-STREET (excluded from chain per gate; enters via facing_bet)
    ],

    # SYN-F6_MW_all_live: 3-way with both non-hero villains in hand
    # post-chain. Exercises per-villain rendering without partial-fold
    # preamble (MUST #42 wording: standard multiway prose, not "Villain
    # {FOLDED_POS} folded" preamble).
    'SYN-F6_MW_all_live': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: check-through (all 3 check — no folds)
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        # Turn: BB bets, both villains continue (CO calls, BTN will
        # decide — BTN is hero here)
        ('turn', 'BB', 'BET'),
        ('turn', 'CO', 'CALL'),
    ],

    # SYN-T_J02_synthetic: HU BET-CHECK-CALL-BET 4-class chain
    # (matches T_J02 corpus shape). Chain fires all 4 narrow classes
    # post-MUST-#11 collapse:
    #   flop:BET + turn:CALL (CHECK-CALL collapses per MUST #11)
    #   + river facing-bet gate via facing_bet=True.
    'SYN-T_J02_synthetic': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),
        ('flop', 'BTN', 'CALL'),
        ('turn', 'BB', 'CHECK'),
        ('turn', 'BTN', 'BET'),
        ('turn', 'BB', 'CALL'),
        ('river', 'BB', 'BET'),
    ],

    # SYN-F7_HU_donk_x_bet: HU villain-as-OOP-aggressor line covering
    # the hu_donk_x_bet shape bucket per MUST #49 — last uncovered
    # real-world authoring pattern (over_narrow + mass_truncation
    # "buckets" are runtime sentinels, not authoring shapes).
    #
    # FIX #3 (commit 13.2.5, GTO review): covers donk-line systematic-
    # error risk in dry-run rather than during 130-entry lift.
    # DISTINCT from SYN-F5 (BTN-aggression) + delayed-probe shapes.
    #
    # Shape: villain BB donks flop → BTN (hero) calls → BB checks turn
    # → BTN checks → BB bets river (hero decision, facing bet).
    # Chain: flop:BET + turn:CHECK (2 prior-street BB actions narrow
    # against the range); river-BET enters via facing_bet gate.
    'SYN-F7_HU_donk_x_bet': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),          # villain donks as OOP-aggressor
        ('flop', 'BTN', 'CALL'),
        ('turn', 'BB', 'CHECK'),        # villain slows down
        ('turn', 'BTN', 'CHECK'),
        ('river', 'BB', 'BET'),         # decision-street (facing_bet gate)
    ],

    # SYN-T_B05_synthetic: HU BET-RAISE-CALL same-street + turn-CHECK
    # (matches T_B05 corpus shape). MUST #11/#12 pre-filter rule is
    # "keep LAST DECISION-BEARING action" (not "keep RAISE").
    #
    # FIX #1 (commit 13.2.5, GTO review): for villain BB, BB's flop
    # actions are [BET, CALL]. BTN's RAISE is a HERO-side action and
    # is filtered out of BB's villain_street_actions by the position
    # filter in narrow_by_action_history's chain loop (only entries
    # with position == villain_pos are kept). BB's [BET, CALL] then
    # goes through _collapse_same_street_sequence which keeps the
    # LAST decision-bearing action = CALL (not RAISE).
    # FIX #1 (commit 13.2.6, GTO review APPROVE_WITH_FIXES on 13.2.5):
    # narrative cleanup — replaced stale `:814` line ref with a
    # description of the position filter, and clarified chain shape:
    # with decision_street='turn', the chain loop walks flop ONLY
    # (it breaks before processing decision_street actions per the
    # prior-street-only rule). So the chain is exactly [flop:CALL];
    # turn:CHECK is on the decision street and does NOT enter the
    # postflop chain. Prior header comment saying "collapses to
    # RAISE-only" was wrong direction — corrected.
    'SYN-T_B05_synthetic': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),
        ('flop', 'BTN', 'RAISE'),   # hero-side; filtered out of BB's chain
        ('flop', 'BB', 'CALL'),     # BB's last decision-bearing → chain:flop:CALL
        ('turn', 'BB', 'CHECK'),
    ],
}


# ───────────────────────────────────────────────────────────────────────
# COMMIT 13.2.6 FIX #2 — POSITION-AWARE CLASSIFIER PREDICATE
# ───────────────────────────────────────────────────────────────────────
# Per-fixture villain position. Threaded into solver_verify_sidecars
# _classify_shape so the donk-shape predicate can require villain
# (not hero) as the flop bettor — defensive against position-agnostic
# mis-routing in the upcoming 13.3 130-entry full lift.
#
# Source of truth: this dict. The test-side fixture_meta block in
# tests/test_commit13_sidecar_dryrun.py imports villain_pos from here
# (DRY); local fixture_meta retains decision_street/expects_fire only.
#
# Schema: ref_id → villain_pos. Position vocab matches action_history
# tuples ('UTG'/'EP'/'HJ'/'MP'/'CO'/'BTN'/'SB'/'BB').
_REFERENCE_VILLAIN_POS: Dict[str, str] = {
    # Real fixtures (commit 13 dry-run)
    'MW-11':                   'CO',
    'MW-30':                   'CO',
    'FB-17':                   'CO',
    'FB-23':                   'CO',
    'MW-15':                   'BB',
    # Synthetic fixtures (commit 13.2 / 13.2.5)
    'SYN-F3_HU_folded':        'BB',
    'SYN-F5_HU_overflow':      'BB',
    'SYN-F6_MW_all_live':      'CO',
    'SYN-T_J02_synthetic':     'BB',
    'SYN-T_B05_synthetic':     'BB',
    'SYN-F7_HU_donk_x_bet':    'BB',
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
