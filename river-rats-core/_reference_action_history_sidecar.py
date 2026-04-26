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
    #   Category 4 (folded_hu sentinel)    : SYN-F3_HU_folded
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

    # ─────────────────────────────────────────────────────────────────
    # COMMIT 13.3.1 — BATCH 1/5: FB-01..20 reference entries
    # (FB-17 already shipped in commit 13 dry-run; remaining 19 entries
    # below per MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_2026-04-25.md)
    # ─────────────────────────────────────────────────────────────────
    # Convention recap:
    #   - 3-way CO-open pots: preflop CO RAISE + BTN CALL + BB CALL.
    #     Postflop position order: BB → CO → BTN.
    #   - 3-way BTN-PFR pots (FB-12/13/19): preflop BTN RAISE + CO CALL
    #     + BB CALL. Postflop position order: BB → CO → BTN. Preflop
    #     actor-order detail (CO acting before BTN preflop) is
    #     simplified into single-raise encoding for AH purposes; opener
    #     is metadata-only and the chain only consumes postflop villain
    #     actions per the prior-street-only rule.
    #   - 2-way pots after a fold (FB-20): preserved as 3-way preflop +
    #     full flop sequence including the fold + heads-up turn action.
    # Source: each entry's `action_string` field in
    # training-data/facing_bet_test_set_40.jsonl is the ground-truth
    # decision-street sequence; `_FB_OPENER_POSITION` in
    # reference_evaluator.py provides the preflop opener; prose in
    # `_FB_ACTION_HISTORY` provides the prior-street context for turn
    # decisions (FB-18/19/20).
    # Hero is the position with the "???" marker in the action_string.

    # FB-01: 3-way CO-open. Flop. CO c-bet, BTN folded, hero BB faces HU.
    'FB-01': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for BB; same-street sequence up to hero action.
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],

    # FB-02: 3-way CO-open. Flop. BB donk-bet, CO folded, hero BTN faces HU.
    'FB-02': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for BTN; BB donked, CO folded.
        ('flop', 'BB', 'BET'),
        ('flop', 'CO', 'FOLD'),
    ],

    # FB-03: 3-way CO-open. Flop. CO bet, BTN called, hero BB faces bet+call.
    'FB-03': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
    ],

    # FB-04: 3-way CO-open. Flop. CO c-bet, BTN folded, hero BB.
    # (Same shape as FB-01 with different board.)
    'FB-04': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],

    # FB-05: 3-way CO-open. Flop. CO c-bet 66%, hero BTN first responder
    # (BB behind to act after BTN).
    'FB-05': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for BTN; BB checked, CO bet, BTN to act, BB behind.
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
    ],

    # FB-06: 3-way CO-open. Flop. CO c-bet, BTN folded, hero BB faces HU.
    # (Same shape as FB-01.)
    'FB-06': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],

    # FB-07: 3-way CO-open. Flop. BB donk; hero CO sandwiched (BTN behind).
    'FB-07': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for CO; BB donked, CO to act, BTN behind.
        ('flop', 'BB', 'BET'),
    ],

    # FB-08: 3-way CO-open. Flop. BB donk; hero CO sandwiched.
    # (Same shape as FB-07 with different board.)
    'FB-08': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),
    ],

    # FB-09: 3-way CO-open. Flop. CO pot-bet, hero BTN first responder.
    'FB-09': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
    ],

    # FB-10: 3-way CO-open. Flop. CO c-bet, BTN folded, hero BB closes HU.
    # (Same shape as FB-01.)
    'FB-10': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],

    # FB-11: 3-way CO-open. Flop. BB donk, CO folded, hero BTN closes HU.
    'FB-11': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),
        ('flop', 'CO', 'FOLD'),
    ],

    # FB-12: 3-way BTN-PFR pot. Flop. BB+CO check-through, BTN bet,
    # hero BB first responder (CO still to act after BB).
    'FB-12': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for BB after action returns; check-check-bet,
        # BB facing decision (CO behind).
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'BET'),
    ],

    # FB-13: 3-way BTN-PFR pot. Flop. Check-check-bet, BB folded,
    # hero CO closes HU vs BTN bet.
    'FB-13': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for CO; BB checked then folded after BTN bet.
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'BET'),
        ('flop', 'BB', 'FOLD'),
    ],

    # FB-14: 3-way CO-open. Flop. BB donk, CO folded, hero BTN closes HU.
    # (Same shape as FB-11.)
    'FB-14': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),
        ('flop', 'CO', 'FOLD'),
    ],

    # FB-15: 3-way CO-open. Flop. CO c-bet, BTN folded, hero BB closes HU.
    # (Same shape as FB-01.)
    'FB-15': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],

    # FB-16: 3-way CO-open. Flop. CO bet, BTN called, hero BB faces bet+call.
    # (Same shape as FB-03.)
    'FB-16': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
    ],

    # FB-18: 3-way CO-open. Turn. Flop check-through; turn CO delayed
    # c-bet, hero BTN first responder (BB behind).
    # Prior chain for primary villain CO: flop:CHECK.
    'FB-18': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: check-through (primary villain CO checks → chain step flop:CHECK).
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        # Turn decision for BTN; BB checked, CO bet, BTN to respond, BB behind.
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'BET'),
    ],

    # FB-19: 3-way BTN-PFR pot. Turn. Flop CO bet + BTN called + BB called;
    # turn check-check-BTN bet, hero BB faces decision (sandwich; CO behind).
    # Prior chain for primary villain BTN: flop:CALL.
    'FB-19': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: BB CHECK, CO BET, BTN CALL (primary villain), BB CALL (hero).
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
        ('flop', 'BB', 'CALL'),
        # Turn decision for BB; BB checked, CO checked, BTN bet, BB to respond.
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'BET'),
    ],

    # FB-20: 3-way → 2-way (BB folded flop). Turn HU (CO vs BTN).
    # CO checks, BTN bets, hero CO faces decision.
    # Prior chain for primary villain BTN: flop:BET.
    'FB-20': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: BB CHECK, CO CHECK, BTN BET, BB FOLD, CO CALL (hero closes flop).
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'BET'),
        ('flop', 'BB', 'FOLD'),
        ('flop', 'CO', 'CALL'),
        # Turn decision for CO (HU vs BTN); CO checks, BTN bets, CO to respond.
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'BET'),
    ],

    # ─────────────────────────────────────────────────────────────────
    # COMMIT 13.3.2 — BATCH 2/5: FB-21..40 minus FB-23 reference entries
    # (FB-23 already shipped in commit 13 dry-run; remaining 19 below
    # per MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_2026-04-25.md)
    # ─────────────────────────────────────────────────────────────────
    # Same conventions as 13.3.1 (see batch 1 header comment above).
    # Hero is the position with "???" in the JSONL action_string.
    # Postflop position order: BB → CO → BTN.
    # FB-13 GTO-review NIT-3 (stale `_FB_ACTION_HISTORY:760` prose) is
    # tracked for separate prose-fix commit; same authoring discipline
    # applies here — JSONL action_string is canonical ground truth and
    # supersedes any conflicting `_FB_ACTION_HISTORY` prose. Notable
    # cases in this batch where prose conflicts with action_string are
    # FB-35 (prose "BB folded" on flop, action_string shows BB folds
    # turn) — encoded per action_string.

    # FB-21: 3-way CO-open. Turn. Flop check-through; CO delayed c-bet
    # turn, BTN folded, hero BB faces HU on turn. (Same shape as FB-17.)
    # Prior chain for primary villain CO: flop:CHECK.
    'FB-21': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: check-through (primary villain CO checks → chain step flop:CHECK).
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        # Turn decision for BB; BB checked, CO bet, BTN folded.
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'BET'),
        ('turn', 'BTN', 'FOLD'),
    ],

    # FB-22: 3-way BTN-PFR. Flop. BB+CO check, BTN bet, BB called,
    # hero CO faces bet+call.
    'FB-22': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for CO; check-check-bet-call sequence to CO.
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'BET'),
        ('flop', 'BB', 'CALL'),
    ],

    # FB-24: 3-way CO-open. River. All checked flop+turn; BB donk river,
    # CO folded, hero BTN faces HU on river.
    # Prior chain for primary villain BB: flop:CHECK + turn:CHECK.
    'FB-24': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop check-through (primary villain BB checks).
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        # Turn check-through (primary villain BB checks).
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'CHECK'),
        # River decision for BTN; BB donked, CO folded.
        ('river', 'BB', 'BET'),
        ('river', 'CO', 'FOLD'),
    ],

    # FB-25: 3-way CO-open. River. CO triple-barrel; BTN folded earlier
    # (encoded as flop fold to first c-bet); hero BB faces HU on river.
    # Prior chain for primary villain CO: flop:BET + turn:BET.
    'FB-25': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: CO c-bet, BTN folds first c-bet, BB calls (hero closes flop HU).
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
        ('flop', 'BB', 'CALL'),
        # Turn HU: BB checks, CO 2nd barrel, BB calls (hero closes turn).
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'BET'),
        ('turn', 'BB', 'CALL'),
        # River decision for BB; BB checks, CO 3rd barrel.
        ('river', 'BB', 'CHECK'),
        ('river', 'CO', 'BET'),
    ],

    # FB-26: 3-way CO-open. River. All checked through; BB donk river,
    # CO folded, hero BTN. (Same shape as FB-24, hero/villain swap from
    # the perspective of who acts on river.)
    # Prior chain for primary villain BB: flop:CHECK + turn:CHECK.
    'FB-26': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'CHECK'),
        ('river', 'BB', 'BET'),
        ('river', 'CO', 'FOLD'),
    ],

    # FB-27: 3-way CO-open. Flop. CO c-bet 33%, BTN folded, hero BB.
    # (Same shape as FB-01.)
    'FB-27': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],

    # FB-28: 3-way CO-open. Flop. CO bet, BTN called, hero BB faces bet+call.
    # (Same shape as FB-03.)
    'FB-28': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
    ],

    # FB-29: 3-way CO-open. Flop. BB donk, hero CO sandwiched (BTN behind).
    # (Same shape as FB-07.)
    'FB-29': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),
    ],

    # FB-30: 3-way CO-open. Flop. CO c-bet 66%, hero BTN first responder.
    # (Same shape as FB-05/09.)
    'FB-30': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
    ],

    # FB-31: 3-way CO-open. Flop. BB donk, CO folded, hero BTN closes HU.
    # (Same shape as FB-11/14.)
    'FB-31': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),
        ('flop', 'CO', 'FOLD'),
    ],

    # FB-32: 3-way CO-open. Flop. CO bet, BTN called, hero BB faces bet+call.
    # (Same shape as FB-03/16/28.)
    'FB-32': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
    ],

    # FB-33: 3-way BTN-PFR. Flop. BB+CO check, BTN bet, BB called,
    # hero CO faces bet+call. (Same shape as FB-22.)
    'FB-33': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'BET'),
        ('flop', 'BB', 'CALL'),
    ],

    # FB-34: 3-way BTN-PFR. Flop. BB+CO check, BTN bet 25%, BB called,
    # hero CO faces bet+call. (Same shape as FB-22/33; smaller sizing.)
    'FB-34': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'BET'),
        ('flop', 'BB', 'CALL'),
    ],

    # FB-35: 3-way BTN-PFR. Turn. Flop check-check-bet-call-call (3-way
    # to turn); turn check-check-bet, BB folds, hero CO faces decision.
    # NOTE: `_FB_ACTION_HISTORY:782` prose says "BB folded" on flop, but
    # JSONL action_string ("BB check, CO check, BTN bet 90, BB fold,
    # CO ???") shows BB folding on TURN. Encoded per action_string
    # (canonical ground truth); prose is stale (tracked for batch 13.3
    # prose-cleanup commit alongside FB-13).
    # Prior chain for primary villain BTN: flop:BET.
    'FB-35': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop 3-way: check-check-bet-call-call (BTN bets, BB+CO call).
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'BET'),
        ('flop', 'BB', 'CALL'),
        ('flop', 'CO', 'CALL'),
        # Turn decision for CO; check-check-bet-fold sequence to CO.
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'BET'),
        ('turn', 'BB', 'FOLD'),
    ],

    # FB-36: 3-way → 2-way BTN-PFR (BB folded flop). Turn HU CO vs BTN.
    # CO checks, BTN bets, hero CO faces decision. (Same shape as FB-20.)
    # Prior chain for primary villain BTN: flop:BET.
    'FB-36': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'BET'),
        ('flop', 'BB', 'FOLD'),
        ('flop', 'CO', 'CALL'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'BET'),
    ],

    # FB-37: 3-way BTN-PFR. Turn. Flop check-through; turn check-check-bet,
    # BB folds, hero CO faces HU on turn.
    # Prior chain for primary villain BTN: flop:CHECK.
    'FB-37': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: check-through (primary villain BTN checks → chain step flop:CHECK).
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        # Turn decision for CO; BB checked, CO checked, BTN bet, BB folded.
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'BET'),
        ('turn', 'BB', 'FOLD'),
    ],

    # FB-38: 3-way CO-open. River. All checked flop+turn; BB pot-bet
    # river, hero CO faces decision (BTN behind to act).
    # Prior chain for primary villain BB: flop:CHECK + turn:CHECK.
    'FB-38': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'CHECK'),
        # River decision for CO; BB donked, CO to act, BTN behind.
        ('river', 'BB', 'BET'),
    ],

    # FB-39: 3-way BTN-PFR. River. All checked flop+turn (BTN checks
    # back turn); river check-check-bet, hero BB faces decision.
    # Prior chain for primary villain BTN: flop:CHECK + turn:CHECK.
    'FB-39': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop check-through (primary villain BTN checks).
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        # Turn check-through (BTN checks back per prose).
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'CHECK'),
        # River decision for BB; BB checks, CO checks, BTN bets.
        ('river', 'BB', 'CHECK'),
        ('river', 'CO', 'CHECK'),
        ('river', 'BTN', 'BET'),
    ],

    # FB-40: 3-way BTN-PFR. Flop. BB+CO check, BTN bet, hero BB first
    # responder (CO behind). (Same shape as FB-12.)
    'FB-40': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'BET'),
    ],

    # ─────────────────────────────────────────────────────────────────
    # COMMIT 13.3.3 — BATCH 3/5: MW-12..30 minus MW-15/MW-30 (first
    # multiway batch; 17 entries) per
    # MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_2026-04-25.md.
    # MW-11/15/30 already shipped in commit 13 dry-run.
    # ─────────────────────────────────────────────────────────────────
    # Source: design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md
    # provides hero_position / primary_villain_position / opener /
    # action_history per fixture; reference_evaluator.py:186-227
    # `_ACTION_STRINGS` provides the abbreviated decision-street
    # action_string with `???` marking hero.
    #
    # Conventions:
    #   - 3-way CO-open: preflop CO RAISE + BTN CALL + BB CALL.
    #     Postflop position order: BB → CO → BTN.
    #   - 3-way BTN-PFR: preflop BTN RAISE + SB CALL + BB CALL (or
    #     other callers per design); postflop order: SB → BB → BTN.
    #   - 4-way HJ-open: preflop HJ RAISE + CO CALL + BTN CALL + BB
    #     CALL; postflop order: BB → HJ → CO → BTN.
    #   - 4-way CO-open with SB caller: preflop CO RAISE + BTN CALL +
    #     SB CALL + BB CALL; postflop order: SB → BB → CO → BTN.
    # action_string compression: when the design says "checks around
    # to hero" or hero faces just one bet, intermediate-position
    # checks/folds are inferred from postflop position order even if
    # not explicit in the action_string. All inferred actions are
    # included in the AH for chain-narrowing completeness.
    # ALL MW-12..29 entries are FLOP DECISIONS → expects_chain_fire=
    # False for every entry (no prior postflop street to chain on).

    # MW-12: 3-way CO-open. Flop. JsTs IP overcards on 852r; 3-way
    # checks around to hero BTN. Primary villain BB.
    'MW-12': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for BTN; check-through (BB+CO check, BTN to act).
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
    ],

    # MW-13: 3-way BTN-PFR. Flop. KhJh OOP overcards on A93r;
    # hero SB first to act OOP. Primary villain BTN.
    'MW-13': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for SB; hero acts first OOP, no pre-hero actions.
    ],

    # MW-14: 3-way CO-open. Flop. Td9d flush+gutshot on Jd8d3h;
    # hero BB faces CO bet 33 (BTN folded). Primary villain CO.
    'MW-14': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for BB; BB checked, CO bet, BTN folded.
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],

    # MW-16: 4-way HJ-open. Flop. JsTs IP overcards on 852r; 4-way
    # checks around to hero BTN. Primary villain BB. Compare to MW-12
    # (3-way same hand).
    'MW-16': [
        ('preflop', 'HJ', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for BTN; check-through (BB+HJ+CO check).
        ('flop', 'BB', 'CHECK'),
        ('flop', 'HJ', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
    ],

    # MW-17: 3-way CO-open. Flop. AdKs nut FD+overcards on Jd8d4c;
    # hero BB faces CO bet 33 (BTN folded). Primary villain CO.
    # Same shape as MW-14 (different hand on different board).
    'MW-17': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],

    # MW-18: 3-way CO-open. Flop. Qd3d non-nut FD on Jd8d4c (same
    # board as MW-17; nut-potential comparison). Same shape as MW-17.
    'MW-18': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],

    # MW-19: 3-way CO-open. Flop. TcNc nut straight on QhJs8d; 3-way
    # checks to hero BTN. Primary villain BB. Same shape as MW-12.
    'MW-19': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
    ],

    # MW-20: 4-way HJ-open. Flop. TsNs non-nut straight on KdQcJh;
    # hero BTN faces BB lead 40 into 110 (HJ+CO folded between).
    # Primary villain BB. Pot odds 26.7% confirms HU when BTN acts.
    'MW-20': [
        ('preflop', 'HJ', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for BTN; BB donked, HJ+CO folded, BTN to act.
        ('flop', 'BB', 'BET'),
        ('flop', 'HJ', 'FOLD'),
        ('flop', 'CO', 'FOLD'),
    ],

    # MW-21: 4-way CO-open with SB caller. Flop. Ah9h nut FD+gutshot
    # on JhTh2c; hero BB faces CO bet (BTN folded). SB checked first.
    # Primary villain CO.
    'MW-21': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for BB; SB checked, BB checked, CO bet, BTN folded.
        ('flop', 'SB', 'CHECK'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],

    # MW-22: 4-way CO-open with SB caller. Flop. AdQs nut FD OOP on
    # Kd9d4h; hero BB first to act OOP after SB. Primary villain CO.
    'MW-22': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for BB; SB checked, BB to act.
        ('flop', 'SB', 'CHECK'),
    ],

    # MW-23: 3-way CO-open. Flop. QhJc top pair IP BTN on Q83r;
    # 3-way checks to hero. Primary villain BB. Same shape as MW-12.
    'MW-23': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
    ],

    # MW-24: 3-way BTN-PFR. Flop. QsJd top pair OOP SB on Q83r
    # (mirror of MW-23); hero SB first to act OOP. Primary villain BTN.
    'MW-24': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for SB; hero first to act OOP, no pre-hero actions.
    ],

    # MW-25: 4-way HJ-open. Flop. Ks7s flush draw IP BTN on As9s5d;
    # 4-way checks to hero. Primary villain BB. Same shape family as
    # MW-16 (4-way checks-through-to-BTN).
    'MW-25': [
        ('preflop', 'HJ', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'HJ', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
    ],

    # MW-26: 4-way CO-open with SB caller. Flop. Ks7s flush draw OOP
    # SB on As9s5d (mirror of MW-25); hero SB first to act OOP.
    # Primary villain CO.
    'MW-26': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for SB; hero first to act OOP, no pre-hero actions.
    ],

    # MW-27: 3-way CO-open. Flop. JhJc overpair IP BTN on 962r; 3-way
    # checks to hero. Primary villain BB. Same shape as MW-12/MW-23.
    'MW-27': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
    ],

    # MW-28: 3-way BTN-PFR. Flop. JhJd overpair OOP SB on 962r
    # (mirror of MW-27); hero SB first to act OOP. Primary villain BTN.
    'MW-28': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for SB; hero first to act OOP, no pre-hero actions.
    ],

    # MW-29: 4-way CO-open with SB caller. Flop. KcTh top pair facing
    # single CO bet on KdJc6s; SB checked, BB checked, CO bet, BTN
    # folded, hero BB faces decision. Primary villain CO. Pot odds
    # 22.6% = 35 / (120 preflop pot + 35 CO bet) confirms BTN folded
    # with no caller (post-bet pot 155 is the call denominator).
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
    # COMMIT 13.3.4 — BATCH 4/5: MW-31..50 (second multiway batch;
    # 20 entries) per MAIN_TERMINAL_PR_4_MERGED greenlight (a8af4aa).
    # ─────────────────────────────────────────────────────────────────
    # Same conventions as 13.3.3. NEW shape territory: MW-41..46/49/50
    # are turn/river decisions — first time MW shapes exercise chain
    # narrowing across multiple postflop streets. Same-street collapse
    # (MUST #11/#12) and check-raise scenarios (MW-31, MW-46, MW-50)
    # exercised here.
    # Source: design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md
    # + reference_evaluator.py:186-227 _ACTION_STRINGS for
    # decision-street ground truth.
    # action_string compression rule continues: implicit pre-hero
    # actions inferred from postflop position order + pot-odds
    # confirmation of caller count, included in AH for chain
    # completeness.

    # MW-31: 3-way CO-open. Flop. AsJs TPJK on AcQd5h; check-check-bet,
    # BB folds, CO check-RAISES hero BTN (after BTN c-bets the
    # checked flop). Decision-street check-raise; primary villain CO.
    # Pot 210 = preflop 90 + BTN bet 30 + CO raise 90 = 210. Hero
    # facing 60 to call → 60/270 = 22.2% pot odds ✓.
    'MW-31': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for BTN (facing CO's check-raise);
        # BB checks, CO checks, BTN bets, BB folds, CO raises.
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'BET'),
        ('flop', 'BB', 'FOLD'),
        ('flop', 'CO', 'RAISE'),
    ],

    # MW-32: 3-way CO-open → 2-way (BB folds flop). Turn. JsTs TP on
    # Tc8h4d-3s; CO double-barrels. Primary villain CO; chain step
    # flop:BET. Hero BTN faces decision.
    'MW-32': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: BB checked, CO bet, BTN called, BB folded.
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
        ('flop', 'BB', 'FOLD'),
        # Turn HU CO vs BTN: CO bets, hero BTN faces.
        ('turn', 'CO', 'BET'),
    ],

    # MW-33: 4-way CO-open + SB caller. Flop. 8h8s set on 8d7c3h;
    # bet+call to hero (SB folds). Primary villain CO. Hero BB.
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

    # MW-34: 3-way CO-open. Flop. AcAd overpair on Js9c4d; hero CO is
    # the c-bettor, BB checked first. Primary villain BB. Hero=CO is
    # unusual (CO acts second in BB→CO→BTN postflop order; only BB's
    # check is pre-hero on flop).
    'MW-34': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for CO (BTN behind); BB checks first.
        ('flop', 'BB', 'CHECK'),
    ],

    # MW-35: 3-way CO-open. Flop. QcJd top pair on Qh7c2s, low SPR ~3.
    # BB checks, CO bets, hero BTN faces. Same shape as MW-36/37
    # (different SPRs). Primary villain CO.
    'MW-35': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
    ],

    # MW-36: 3-way CO-open. Flop. Same as MW-35 (Qh7c2s) at standard
    # SPR ~8.
    'MW-36': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
    ],

    # MW-37: 3-way CO-open. Flop. Same as MW-35 (Qh7c2s) at deep SPR
    # ~15.
    'MW-37': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
    ],

    # MW-38: 3-way CO-open. Flop. AhJh nut FD on Kh8h3d; BB donks low
    # SPR ~3, CO folds, hero BTN faces HU. Primary villain BB.
    'MW-38': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'BET'),
        ('flop', 'CO', 'FOLD'),
    ],

    # MW-39: 3-way CO-open. Flop. AhJh nut FD on Kh8h3d (same as
    # MW-38) at deep SPR ~15; CO bets instead of BB donking. Hero
    # BTN. Primary villain CO.
    'MW-39': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
    ],

    # MW-40: 4-way HJ-open. Flop. AhTs top pair on AdJc5h; 4-way checks
    # to hero BTN. Same shape family as MW-16/25 (4-way check-through-
    # to-BTN). Primary villain BB.
    'MW-40': [
        ('preflop', 'HJ', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'HJ', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
    ],

    # MW-41: 3-way CO-open. Turn. QhTc middle pair+gutshot on
    # KsQd7c-Jh; CO double-barrel, hero BTN faces. Primary villain CO;
    # chain step flop:BET. First MW turn-decision in batch 13.3.4.
    'MW-41': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: BB checked, CO bet, BTN called, BB called → 3-way to turn.
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
        ('flop', 'BB', 'CALL'),
        # Turn decision for BTN: BB checks, CO 2nd barrel.
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'BET'),
    ],

    # MW-42: 3-way CO-open → 2-way (BB folds flop). River. AsJs TPTK
    # on AdKc7h-5s-2c; 2-street action then CO checks river. Primary
    # villain CO. Chain steps flop:BET + turn:CALL (CO's turn
    # CHECK→CALL collapses to CALL via MUST #11).
    'MW-42': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: BB checked, CO bet, BTN called, BB folded.
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
        ('flop', 'BB', 'FOLD'),
        # Turn HU: CO checks, hero BTN bets, CO calls.
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'BET'),
        ('turn', 'CO', 'CALL'),
        # River decision for BTN: CO checks.
        ('river', 'CO', 'CHECK'),
    ],

    # MW-43: 4-way CO-open + SB caller. River. 9s7s middle pair on
    # 9d8d5c-2h-Kc; flop+turn check-through, CO leads river, BTN folds,
    # SB folds (per pot-odds 40%), hero BB faces. Primary villain CO.
    # Chain steps flop:CHECK + turn:CHECK (CO's check-throughs).
    'MW-43': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop check-through.
        ('flop', 'SB', 'CHECK'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        # Turn check-through.
        ('turn', 'SB', 'CHECK'),
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'CHECK'),
        # River decision for BB: SB checks, BB checks, CO bets, BTN
        # folds, SB folds (pot-odds 40% confirms no caller before hero).
        ('river', 'SB', 'CHECK'),
        ('river', 'BB', 'CHECK'),
        ('river', 'CO', 'BET'),
        ('river', 'BTN', 'FOLD'),
        ('river', 'SB', 'FOLD'),
    ],

    # MW-44: 3-way CO-open. Turn. Th8h TP+OESD on Ts9h4d-7c; BB donks
    # flop AND turn (double-lead), CO folded turn. Primary villain BB.
    # Chain step flop:BET (BB single action collapses trivially).
    'MW-44': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: BB donks, CO calls, BTN calls → 3-way to turn.
        ('flop', 'BB', 'BET'),
        ('flop', 'CO', 'CALL'),
        ('flop', 'BTN', 'CALL'),
        # Turn: BB leads again, CO folds; hero BTN faces.
        ('turn', 'BB', 'BET'),
        ('turn', 'CO', 'FOLD'),
    ],

    # MW-45: 4-way CO-open + SB caller. Turn. 6d6c flopped set on
    # AcKd6h-Qs; flop check-through (hero slowplays set); turn CO bets,
    # BTN folds, SB folds (pot-odds 38.5% confirms). Primary villain CO.
    # Chain step flop:CHECK.
    'MW-45': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop check-through.
        ('flop', 'SB', 'CHECK'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
        # Turn decision for BB: SB checks, BB checks, CO bets, BTN folds, SB folds.
        ('turn', 'SB', 'CHECK'),
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'BET'),
        ('turn', 'BTN', 'FOLD'),
        ('turn', 'SB', 'FOLD'),
    ],

    # MW-46: 4-way HJ-open → HU CO vs BTN (HJ+BB fold flop).
    # River. Ks7c trips on 7h7d5s-9c-Js; CO BET flop, BTN call, others
    # fold; turn CO check, BTN bet, CO call; river CO check, BTN bet,
    # CO check-RAISES. Primary villain CO. Chain steps flop:BET +
    # turn:CALL (CHECK-CALL collapse). RIVER CHECK-RAISE on
    # decision-street.
    'MW-46': [
        ('preflop', 'HJ', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: BB check, HJ check, CO bet, BTN call, BB fold, HJ fold.
        ('flop', 'BB', 'CHECK'),
        ('flop', 'HJ', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
        ('flop', 'BB', 'FOLD'),
        ('flop', 'HJ', 'FOLD'),
        # Turn HU CO vs BTN: CO check, BTN bet, CO call.
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'BET'),
        ('turn', 'CO', 'CALL'),
        # River decision for BTN (facing CO's check-raise): CO check,
        # BTN bet, CO RAISE.
        ('river', 'CO', 'CHECK'),
        ('river', 'BTN', 'BET'),
        ('river', 'CO', 'RAISE'),
    ],

    # MW-47: 4-way CO-open + SB caller. Flop. AsQs nut FD+gutshot OOP
    # SB on KsJd5s; faces bet+call. Hero=SB. Primary villain CO.
    'MW-47': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for SB; SB checked, BB checked, CO bet, BTN called.
        ('flop', 'SB', 'CHECK'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'CALL'),
    ],

    # MW-48: 3-way BTN-PFR. Flop. AhTc gutshot+overcards low SPR ~2
    # OOP BB on QdJc4s; SB checks, hero BB first to act OOP-after-SB
    # (with BTN behind). Primary villain BTN.
    'MW-48': [
        ('preflop', 'BTN', 'RAISE'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop decision for BB; SB checked first, BB to act, BTN behind.
        ('flop', 'SB', 'CHECK'),
    ],

    # MW-49: 4-way HJ-open → 3-way (HJ folds flop). Turn. AdKd TPTK on
    # As9c5d-Tc; hero BTN bets flop, HJ folds, CO+BB call; turn checks
    # to hero. Primary villain BB. Chain step flop:CALL (BB's
    # CHECK→CALL collapse via MUST #11).
    'MW-49': [
        ('preflop', 'HJ', 'RAISE'),
        ('preflop', 'CO', 'CALL'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: BB check, HJ check, CO check, BTN (hero) bet, BB call,
        # HJ fold, CO call → 3-way to turn (HJ out).
        ('flop', 'BB', 'CHECK'),
        ('flop', 'HJ', 'CHECK'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'BET'),
        ('flop', 'BB', 'CALL'),
        ('flop', 'HJ', 'FOLD'),
        ('flop', 'CO', 'CALL'),
        # Turn decision for BTN: BB check, CO check.
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
    ],

    # MW-50: 4-way CO-open + SB caller → 3-way (SB folds flop). Turn.
    # JcTc top pair on Js8h4d-5c; flop CO bet, BTN raises, SB fold,
    # BB call, CO call → 3-way to turn; turn check-check-BTN bet, hero
    # BB faces. Primary villain BTN. Chain step flop:RAISE (BTN's
    # single flop action collapses trivially to RAISE).
    # Note: hero BB acts second on turn (postflop order BB → CO → BTN
    # in 3-way after SB folds).
    'MW-50': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'SB', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        # Flop: SB check, BB check, CO bet, BTN raise, SB fold, BB call,
        # CO call → 3-way to turn.
        ('flop', 'SB', 'CHECK'),
        ('flop', 'BB', 'CHECK'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'RAISE'),
        ('flop', 'SB', 'FOLD'),
        ('flop', 'BB', 'CALL'),
        ('flop', 'CO', 'CALL'),
        # Turn decision for BB: BB check, CO check, BTN bet.
        ('turn', 'BB', 'CHECK'),
        ('turn', 'CO', 'CHECK'),
        ('turn', 'BTN', 'BET'),
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
    # Commit 13.3.1 — FB-01..20 (FB-17 above)
    'FB-01':                   'CO',
    'FB-02':                   'BB',
    'FB-03':                   'CO',
    'FB-04':                   'CO',
    'FB-05':                   'CO',
    'FB-06':                   'CO',
    'FB-07':                   'BB',
    'FB-08':                   'BB',
    'FB-09':                   'CO',
    'FB-10':                   'CO',
    'FB-11':                   'BB',
    'FB-12':                   'BTN',
    'FB-13':                   'BTN',
    'FB-14':                   'BB',
    'FB-15':                   'CO',
    'FB-16':                   'CO',
    'FB-18':                   'CO',
    'FB-19':                   'BTN',
    'FB-20':                   'BTN',
    # Commit 13.3.2 — FB-21..40 (FB-23 above)
    'FB-21':                   'CO',
    'FB-22':                   'BTN',
    'FB-24':                   'BB',
    'FB-25':                   'CO',
    'FB-26':                   'BB',
    'FB-27':                   'CO',
    'FB-28':                   'CO',
    'FB-29':                   'BB',
    'FB-30':                   'CO',
    'FB-31':                   'BB',
    'FB-32':                   'CO',
    'FB-33':                   'BTN',
    'FB-34':                   'BTN',
    'FB-35':                   'BTN',
    'FB-36':                   'BTN',
    'FB-37':                   'BTN',
    'FB-38':                   'BB',
    'FB-39':                   'BTN',
    'FB-40':                   'BTN',
    # Commit 13.3.3 — MW-12..30 minus MW-15/MW-30 (first multiway batch)
    # Per design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md
    # "Primary villain position" field for each fixture.
    'MW-12':                   'BB',
    'MW-13':                   'BTN',
    'MW-14':                   'CO',
    'MW-16':                   'BB',
    'MW-17':                   'CO',
    'MW-18':                   'CO',
    'MW-19':                   'BB',
    'MW-20':                   'BB',
    'MW-21':                   'CO',
    'MW-22':                   'CO',
    'MW-23':                   'BB',
    'MW-24':                   'BTN',
    'MW-25':                   'BB',
    'MW-26':                   'CO',
    'MW-27':                   'BB',
    'MW-28':                   'BTN',
    'MW-29':                   'CO',
    # Commit 13.3.4 — MW-31..50 (second multiway batch). Per
    # design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md
    # "Primary villain position" field.
    'MW-31':                   'CO',
    'MW-32':                   'CO',
    'MW-33':                   'CO',
    'MW-34':                   'BB',
    'MW-35':                   'CO',
    'MW-36':                   'CO',
    'MW-37':                   'CO',
    'MW-38':                   'BB',
    'MW-39':                   'CO',
    'MW-40':                   'BB',
    'MW-41':                   'CO',
    'MW-42':                   'CO',
    'MW-43':                   'CO',
    'MW-44':                   'BB',
    'MW-45':                   'CO',
    'MW-46':                   'CO',
    'MW-47':                   'CO',
    'MW-48':                   'BTN',
    'MW-49':                   'BB',
    'MW-50':                   'BTN',
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
