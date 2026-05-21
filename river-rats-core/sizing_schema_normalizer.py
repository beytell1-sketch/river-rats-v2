"""sizing_schema_normalizer.py — A0.1 backfill normalizer for 4-way corpus labels.

Provenance
==========
This module is the deterministic backfill normalizer specified in
`review/comms/DRAFT_BLUEPRINT_A0_SCHEMA_FIX_v2_2026-05-21.md` (orchestrator
re-ratified per `review/comms/RATIFICATION_A0_BLUEPRINT_v2_2026-05-21.md`,
superseding v1's `DRAFT_BLUEPRINT_A0_SCHEMA_FIX_v1_2026-05-17.md`). It
converts legacy 4-way labels carrying the dual-semantics
`predicted_sizing_pct` field into the new split-schema form
(`predicted_bet_pct` + `predicted_raise_to_bb`) defined in blueprint §1.

v2 vs v1 algorithm deltas (per QC pre-merge findings):
  - F-1 (BLOCKER): NEW §3.2 STEP 2.5 — explicit all-in detection BEFORE the
    canonical-set tie-break. If labeller writes v == stack_size_bb, route to
    raise_to_bb=v with new status `clean_all_in`. Was a §3.2/§7.3 contradiction
    in v1; v1 produced raise_to=16 on the only v=100 spot in the corpus
    (4WF-MULTIWAY-171) because canonical-pct branch fired first.
  - F-2 (BLOCKER): NEW §3.2 STEP 1 formula — NL-standard
    `min_raise_to_bb = 2 × previous_full_bet` where
    `previous_full_bet = to_call_bb + hero_already_committed_bb(ctx)`.
    The `hero_already_committed_bb` helper returns 1.0bb for BB preflop,
    0.5bb for SB preflop, 0.0bb otherwise. Postflop is unchanged
    (hero_already_committed_bb=0 → min_raise=2×to_call, equivalent to v1).
  - F-6 (BLOCKER promoted from SHOULD_FIX): NEW §3.6 — `compute_consensus_v2`
    function implementing modal-action + weighted modal-sizing consensus over
    5 sonnet labellers + optional opus tier-up.
  - QC SHOULD_FIX (validate_v2_label dead code): `validate_v2_label` is now
    called from `normalize_label` after producing the result; violations
    are reported via the rationale on the returned label.

Inputs consumed by this script (raw label files for batches 001-008) feed the
v9-4way training export. Per CLAUDE.md §6 training-provenance addendum
(2026-04-15), this module is part of the training pipeline and any model
artifact produced from its output must be reproducible by linking back to the
commit that introduced it.

The orchestrator ratification override (carrying over from v1) moves the
labeller-brief patch from PR A0.1 to PR A0.3 — this file ships WITHOUT a
brief change. Brief still describes legacy `predicted_sizing_pct`.

Algorithm — RAISE normalization (blueprint v2 §3.2)
---------------------------------------------------
For each RAISE label with legacy value v, three candidate interpretations are
considered:
    1. bb        — v as a literal raise-TO bb amount
    2. pct-by    — v as "% of pot raise-BY" => raise-to = facing_bet + v% * pot
    3. mult-bet  — v as "% multiplier of facing bet" (only for canonical mults)

The algorithm proceeds:
    STEP 1     — compute min_raise (NL-standard formula; F-2 fix)
    STEP 2     — compute the 3 candidate raise-to interpretations
    STEP 2.5   — all-in detection (F-1 fix; if v == stack_size_bb,
                 short-circuit with status=clean_all_in BEFORE legality/tie-break)
    STEP 3     — legality filter (each candidate against
                 [min_raise_to_bb, stack_size_bb])
    STEP 4     — canonical-set tie-break (mult > bb > pct > legal-only fallback)

BET normalization (blueprint §3.3) is trivial: legacy v maps directly to
`predicted_bet_pct` if v is in the allowed enum; otherwise malformed_rejected.

Public API
----------
- `normalize_label(label_dict, spot_context_dict) -> NormalizedLabel`
- `normalize_batch(input_jsonl_path, context_jsonl_path, output_v2_path,
                   audit_jsonl_path) -> dict`
- `compute_consensus_v2(spot_labels, opus_label=None) -> ConsensusV2Record`
  (NEW v2 per §3.6 — modal-action + weighted modal-sizing consensus)
- `validate_v2_label(action, bet_pct, raise_to_bb, ctx) -> Optional[str]`
  (§1.4 validation rules; now wired into `normalize_label`)
- CLI (direct file form; the docstring used to advertise `python -m
  river_rats_core...` but the package directory has a hyphen, so that form
  doesn't work — use the direct file form):
       `python3 river-rats-core/sizing_schema_normalizer.py --dry-run <path>`
       `python3 river-rats-core/sizing_schema_normalizer.py --apply <input>
            --context <50hand.jsonl> --output <v2 path> --audit <audit path>`

Min-raise convention (v2)
-------------------------
Per blueprint v2 §3.2 STEP 1: `min_raise_to_bb = 2 × previous_full_bet`
where `previous_full_bet = to_call_bb + hero_already_committed_bb(ctx)`.
This is the live-NL convention; the architect committed to it over the
online-NL alternative (which would yield 4.0 instead of 5.0 for BB-defend);
orchestrator accepted the commitment (RATIFICATION §Commitment 1).

For postflop spots, `hero_already_committed_bb = 0` so `previous_full_bet =
to_call_bb` and `min_raise_to_bb = 2 × to_call_bb` — identical to v1
(postflop spots are unchanged by F-2). Only preflop BB/SB defends shift.

The `river-rats-core/poker_game.py` engine is permissive (no min-raise check
at action time), so the normalizer's stricter rule does not conflict with
engine behaviour; see ratification §7.1.1.

Dependencies
------------
Standard library only (json, dataclasses, argparse, pathlib, sys).
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


# =============================================================================
# Module-level constants (blueprint §3.2 canonical-value tables + §1.3 enums)
# =============================================================================

#: Canonical raise-TO bb amounts seen in the corpus (used as tie-break set).
CANONICAL_BB: frozenset[int] = frozenset(
    {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 18, 22, 27, 30}
)

#: Canonical pct-of-pot raise-BY values (also the BET sizing enum is a subset).
CANONICAL_PCT: frozenset[int] = frozenset({25, 33, 50, 66, 75, 100, 150})

#: Canonical multiplier-of-facing-bet values seen in the corpus.
CANONICAL_MULT: frozenset[int] = frozenset({300, 360, 720})

#: Allowed enum for `predicted_bet_pct` (blueprint §1.3).
ALLOWED_BET_PCT: frozenset[int] = frozenset({25, 33, 50, 66, 75, 100, 150})

#: Hard upper bound on `predicted_raise_to_bb` (blueprint §1.2 JSON schema).
RAISE_TO_BB_MAX: int = 200

#: Pot guard floor for normalization basis (blueprint §5.2 edge case).
POT_BB_FLOOR: float = 0.5


# Type aliases (informational only; runtime is plain str/int).
ActionStr = str  # one of FOLD CHECK CALL BET RAISE
NormalizationStatusStr = str  # clean | ambiguous_resolved | malformed_rejected | no_op


# =============================================================================
# Dataclasses (blueprint §3.1 signatures)
# =============================================================================


@dataclass(frozen=True)
class SpotContext:
    """Subset of fields from batch_NNN_50hand.jsonl needed for legality checks.

    All numeric fields are in big-blinds (bb). `facing_bet` is 0/1 boolean.
    `hero_position` is one of {"UTG","HJ","CO","BTN","SB","BB"} — added in v2
    per F-2 fix to derive `hero_already_committed_bb` for preflop spots.
    Optional with default "" so callers that don't supply it get the v1
    behaviour (hero_committed=0, equivalent to non-blind / postflop).
    """

    pot_bb: float
    to_call_bb: float
    facing_bet: int
    stack_size_bb: float
    street: str  # "preflop" | "flop" | "turn" | "river"
    hero_position: str = ""  # "UTG"|"HJ"|"CO"|"BTN"|"SB"|"BB" — F-2 v2


@dataclass(frozen=True)
class NormalizedSizing:
    """Result of normalising a single label's sizing fields.

    `status` is one of:
      - "clean"               : input matched expected schema; no inference needed.
      - "clean_all_in"        : v == stack_size_bb; interpreted as all-in raise-to
                                (NEW in v2 per F-1 fix; §3.2 STEP 2.5).
      - "ambiguous_resolved"  : input was malformed under brief but a single
                                legal canonical interpretation was found.
      - "malformed_rejected"  : no legal interpretation; spot routes to
                                owner-arb queue.
      - "no_op"               : input was already in v2 schema (idempotent path).
    """

    predicted_bet_pct: Optional[int]
    predicted_raise_to_bb: Optional[int]
    status: NormalizationStatusStr
    rationale: str


@dataclass(frozen=True)
class NormalizedLabel:
    """Full label after normalisation, including the source spot/labeller id.

    `labeller_id` is `int | str`: Sonnet labellers are numbered 1..N
    (int), while the Opus tier-up labeller is identified by the string
    sentinel ``"opus_tierup"`` (see `scripts/run_125i_mw40_verif_opus_tierup.py`).
    Per A0.1.1 / QC A0.2 SHOULD_FIX-1, the field is preserved verbatim and
    NEVER coerced — silent str→int coercion was the latent bug we're fixing.
    """

    spot_id: str
    labeller_id: int | str
    predicted_action: ActionStr
    predicted_bet_pct: Optional[int]
    predicted_raise_to_bb: Optional[int]
    status: NormalizationStatusStr
    rationale: str
    # Carry-through fields preserved verbatim from input label.
    extras: dict[str, Any] = field(default_factory=dict)


# =============================================================================
# Core normalization (pure functions, no I/O)
# =============================================================================


def _coerce_int(value: Any) -> Optional[int]:
    """Return ``int(value)`` if value is a plain integer-valued number; else None."""
    if value is None:
        return None
    if isinstance(value, bool):  # bool is an int subclass; reject explicitly
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if value.is_integer():
            return int(value)
        return None
    return None


def _is_v2_input(label: dict[str, Any]) -> bool:
    """Detect whether the input already conforms to the v2 split schema.

    v2 inputs have `predicted_bet_pct` and `predicted_raise_to_bb` keys
    AND do NOT have a `predicted_sizing_pct` key.
    """
    return (
        "predicted_bet_pct" in label
        and "predicted_raise_to_bb" in label
        and "predicted_sizing_pct" not in label
    )


def hero_already_committed_bb(ctx: SpotContext) -> float:
    """Return the chips hero has already posted at street-start (per blueprint v2 §3.1).

    Preflop: BB has posted 1.0bb; SB has posted 0.5bb; all other positions 0.0bb.
    Postflop: 0.0bb (each new street begins with hero's contribution at 0).

    Used by `normalize_sizing` STEP 1 to compute `previous_full_bet` for the
    NL-standard min-raise formula (F-2 fix). On non-preflop streets and on
    preflop non-blind positions, this function returns 0 and the v2 formula
    reduces to the v1 formula `min_raise = 2 × to_call_bb`.
    """
    if (ctx.street or "").lower() == "preflop":
        pos = (ctx.hero_position or "").upper()
        if pos == "BB":
            return 1.0
        if pos == "SB":
            return 0.5
    return 0.0


def normalize_sizing(
    action: ActionStr,
    legacy_sizing_pct: Optional[int],
    ctx: SpotContext,
) -> NormalizedSizing:
    """Convert a legacy `predicted_sizing_pct` value into the new split schema.

    Implements blueprint §3.2 (RAISE) and §3.3 (BET) exactly.
    """
    action_u = (action or "").upper()

    # --------------------------- FOLD / CHECK / CALL -------------------------
    if action_u in ("FOLD", "CHECK", "CALL"):
        if legacy_sizing_pct is None:
            return NormalizedSizing(
                predicted_bet_pct=None,
                predicted_raise_to_bb=None,
                status="clean",
                rationale=f"{action_u} with null sizing — clean.",
            )
        # Non-null sizing on a non-aggressive action: legacy schema bug.
        # Warn (via rationale) but normalise to null/null with status=clean
        # per blueprint §3.1 docstring spec.
        return NormalizedSizing(
            predicted_bet_pct=None,
            predicted_raise_to_bb=None,
            status="clean",
            rationale=(
                f"WARN: {action_u} carried non-null legacy value "
                f"{legacy_sizing_pct!r}; dropped to null/null per schema."
            ),
        )

    # --------------------------------- BET -----------------------------------
    if action_u == "BET":
        v = legacy_sizing_pct
        if v is None:
            return NormalizedSizing(
                predicted_bet_pct=None,
                predicted_raise_to_bb=None,
                status="malformed_rejected",
                rationale="BET with null sizing — required field missing.",
            )
        if v in ALLOWED_BET_PCT:
            return NormalizedSizing(
                predicted_bet_pct=int(v),
                predicted_raise_to_bb=None,
                status="clean",
                rationale=f"BET v={v} ∈ allowed {{25,33,50,66,75,100,150}}.",
            )
        return NormalizedSizing(
            predicted_bet_pct=None,
            predicted_raise_to_bb=None,
            status="malformed_rejected",
            rationale=(
                f"BET v={v} ∉ allowed {{25,33,50,66,75,100,150}} — rejected."
            ),
        )

    # -------------------------------- RAISE ----------------------------------
    if action_u == "RAISE":
        v = legacy_sizing_pct
        if v is None:
            return NormalizedSizing(
                predicted_bet_pct=None,
                predicted_raise_to_bb=None,
                status="malformed_rejected",
                rationale="RAISE with null sizing — required field missing.",
            )

        # Step 1 (REVISED — F-2 fix): NL-standard min-raise via previous_full_bet.
        # previous_full_bet = to_call_bb + hero_already_committed_bb
        # Postflop and preflop non-blind: hero_committed=0 → equivalent to v1's
        # 2 × to_call_bb formula. Only preflop BB/SB defends shift.
        facing_bet_bb = ctx.to_call_bb
        hero_committed_bb = hero_already_committed_bb(ctx)
        previous_full_bet = facing_bet_bb + hero_committed_bb
        min_raise_to_bb = 2.0 * previous_full_bet
        max_raise_to_bb = ctx.stack_size_bb

        # Step 2: candidate interpretations
        candidate_bb = v
        candidate_pct_to_bb = round(
            facing_bet_bb + (v / 100.0) * ctx.pot_bb
        )
        candidate_mult_to_bb = round((v / 100.0) * facing_bet_bb)

        # Step 2.5 (NEW — F-1 fix): all-in detection.
        # If labeller wrote v exactly equal to the stack size, interpret as
        # an all-in raise-TO tell. This branch fires BEFORE the canonical-set
        # tie-break so that v=100 on a 100bb stack is not silently re-routed
        # through the pct branch (which would produce raise-to=16, contradicting
        # the §7.3 commitment to all-in interpretation).
        # Note: at stack_size_bb=200 (future deep-stack axis), v=100 does NOT
        # match this branch — v=100 falls through to the pct/tie-break path,
        # which is correct (pot-sized raise on a deep stack is not all-in).
        if v == int(round(ctx.stack_size_bb)):
            return NormalizedSizing(
                predicted_bet_pct=None,
                predicted_raise_to_bb=int(v),
                status="clean_all_in",
                rationale=(
                    f"RAISE v={v} == stack_size_bb={ctx.stack_size_bb} → all-in "
                    f"raise-to per §3.2 STEP 2.5 (F-1 fix). Skipped canonical-set "
                    f"tie-break."
                ),
            )

        # Step 3: legality filter
        def _legal(x: float) -> bool:
            return min_raise_to_bb <= x <= max_raise_to_bb and x <= RAISE_TO_BB_MAX

        legal_bb = _legal(candidate_bb)
        legal_pct = _legal(candidate_pct_to_bb)
        legal_mult = _legal(candidate_mult_to_bb)

        # Step 4: tie-break (blueprint §3.2 canonical tables)
        in_canonical_mult = v in CANONICAL_MULT
        in_canonical_bb = v in CANONICAL_BB
        in_canonical_pct = v in CANONICAL_PCT

        rationale_prefix = (
            f"RAISE v={v}; pot={ctx.pot_bb}, to_call={ctx.to_call_bb}, "
            f"stack={ctx.stack_size_bb}; "
            f"candidates: bb={candidate_bb}(legal={legal_bb}), "
            f"pct_to={candidate_pct_to_bb}(legal={legal_pct}), "
            f"mult_to={candidate_mult_to_bb}(legal={legal_mult})."
        )

        # Multiplier interpretation: canonical tells take priority.
        if in_canonical_mult and legal_mult:
            return NormalizedSizing(
                predicted_bet_pct=None,
                predicted_raise_to_bb=int(candidate_mult_to_bb),
                status="ambiguous_resolved",
                rationale=(
                    f"{rationale_prefix} v ∈ CANONICAL_MULT{{300,360,720}} "
                    f"and legal_mult → raise_to={candidate_mult_to_bb}bb."
                ),
            )

        # Pure bb interpretation (most common path).
        if in_canonical_bb and legal_bb and not (in_canonical_pct and legal_pct):
            return NormalizedSizing(
                predicted_bet_pct=None,
                predicted_raise_to_bb=int(candidate_bb),
                status="clean",
                rationale=(
                    f"{rationale_prefix} v ∈ CANONICAL_BB and legal_bb only "
                    f"→ raise_to={candidate_bb}bb."
                ),
            )

        # Pure pct interpretation.
        if in_canonical_pct and legal_pct and not (in_canonical_bb and legal_bb):
            return NormalizedSizing(
                predicted_bet_pct=None,
                predicted_raise_to_bb=int(candidate_pct_to_bb),
                status="ambiguous_resolved",
                rationale=(
                    f"{rationale_prefix} v ∈ CANONICAL_PCT and legal_pct only "
                    f"→ raise_to={candidate_pct_to_bb}bb (pct-raise-by interp)."
                ),
            )

        # Both bb and pct legal (tie path): prefer bb (brief-intent).
        if legal_bb and legal_pct:
            return NormalizedSizing(
                predicted_bet_pct=None,
                predicted_raise_to_bb=int(candidate_bb),
                status="ambiguous_resolved",
                rationale=(
                    f"{rationale_prefix} bb and pct both legal; brief-intent "
                    f"tie-break prefers bb → raise_to={candidate_bb}bb."
                ),
            )

        # Only one of bb/pct legal.
        if legal_bb and not legal_pct:
            return NormalizedSizing(
                predicted_bet_pct=None,
                predicted_raise_to_bb=int(candidate_bb),
                status="clean",
                rationale=(
                    f"{rationale_prefix} only legal_bb → raise_to={candidate_bb}bb."
                ),
            )
        if legal_pct and not legal_bb:
            return NormalizedSizing(
                predicted_bet_pct=None,
                predicted_raise_to_bb=int(candidate_pct_to_bb),
                status="ambiguous_resolved",
                rationale=(
                    f"{rationale_prefix} only legal_pct → raise_to={candidate_pct_to_bb}bb."
                ),
            )

        # Neither legal: malformed-reject.
        return NormalizedSizing(
            predicted_bet_pct=None,
            predicted_raise_to_bb=None,
            status="malformed_rejected",
            rationale=(
                f"{rationale_prefix} no legal interpretation → routed to "
                f"owner-arb queue."
            ),
        )

    # Unknown action — defensive.
    return NormalizedSizing(
        predicted_bet_pct=None,
        predicted_raise_to_bb=None,
        status="malformed_rejected",
        rationale=f"Unknown action {action!r}.",
    )


def normalize_label(
    label_dict: dict[str, Any],
    spot_context_dict: dict[str, Any],
) -> NormalizedLabel:
    """Normalise a single label dict given its matching spot-context dict.

    Round-trip idempotence: if `label_dict` is already in v2 split form,
    the function emits status="no_op" with the existing fields preserved.
    """
    spot_id = label_dict.get("spot_id", "<unknown>")
    # A0.1.1 / QC A0.2 SHOULD_FIX-1: labeller_id is `int | str`. Sonnet
    # labellers are integer IDs (1..N); the Opus tier-up label uses the
    # string sentinel "opus_tierup". Preserve verbatim — DO NOT coerce
    # (previous `int(...)` cast crashed on the Opus string).
    raw_labeller_id = label_dict.get("labeller_id", -1)
    labeller_id: int | str
    if isinstance(raw_labeller_id, bool):
        # bool is an int subclass; treat as integer ID.
        labeller_id = int(raw_labeller_id)
    elif isinstance(raw_labeller_id, str):
        labeller_id = raw_labeller_id
    else:
        labeller_id = int(raw_labeller_id)
    action = label_dict.get("predicted_action", "")

    # Idempotence: detect v2-shaped input.
    if _is_v2_input(label_dict):
        return NormalizedLabel(
            spot_id=spot_id,
            labeller_id=labeller_id,
            predicted_action=action,
            predicted_bet_pct=_coerce_int(label_dict.get("predicted_bet_pct")),
            predicted_raise_to_bb=_coerce_int(label_dict.get("predicted_raise_to_bb")),
            status="no_op",
            rationale="Input already in v2 split schema; passthrough.",
            extras=_extras(label_dict),
        )

    legacy_v = _coerce_int(label_dict.get("predicted_sizing_pct"))

    ctx = SpotContext(
        pot_bb=float(spot_context_dict.get("pot_bb", 0.0)),
        to_call_bb=float(spot_context_dict.get("to_call_bb", 0.0)),
        facing_bet=int(spot_context_dict.get("facing_bet", 0)),
        stack_size_bb=float(spot_context_dict.get("stack_size_bb", 0.0)),
        street=str(spot_context_dict.get("street", "")),
        hero_position=str(spot_context_dict.get("hero_position", "")),
    )

    sized = normalize_sizing(action, legacy_v, ctx)

    # Wire §1.4 validation per QC SHOULD_FIX (validate_v2_label was dead code in v1).
    # Validation only runs on labels with a non-rejected status — malformed_rejected
    # labels intentionally produce null/null which violates the BET/RAISE invariants
    # but is the documented routing path (owner-arb queue).
    rationale = sized.rationale
    if sized.status not in ("malformed_rejected",):
        err = validate_v2_label(
            action=action,
            bet_pct=sized.predicted_bet_pct,
            raise_to_bb=sized.predicted_raise_to_bb,
            ctx=ctx,
        )
        if err is not None:
            rationale = f"{rationale} | VALIDATION FAIL: {err}"

    return NormalizedLabel(
        spot_id=spot_id,
        labeller_id=labeller_id,
        predicted_action=action,
        predicted_bet_pct=sized.predicted_bet_pct,
        predicted_raise_to_bb=sized.predicted_raise_to_bb,
        status=sized.status,
        rationale=rationale,
        extras=_extras(label_dict),
    )


def _extras(label: dict[str, Any]) -> dict[str, Any]:
    """Return label fields outside of the schema-controlled set, verbatim."""
    controlled = {
        "spot_id",
        "labeller_id",
        "predicted_action",
        "predicted_sizing_pct",
        "predicted_bet_pct",
        "predicted_raise_to_bb",
    }
    return {k: v for k, v in label.items() if k not in controlled}


# =============================================================================
# Validation (blueprint §1.4)
# =============================================================================


def validate_v2_label(
    action: ActionStr,
    bet_pct: Optional[int],
    raise_to_bb: Optional[int],
    ctx: SpotContext,
) -> Optional[str]:
    """Return None if the v2 label passes §1.4 rules; else an error string.

    Rules 1-5 are enforced here. Rules 6-7 (FL5 facing_bet sanity) are
    pre-existing and are NOT re-implemented here — they live in the
    labeller-side action validators.
    """
    action_u = (action or "").upper()

    # Rule 1
    if action_u == "BET" and (bet_pct is None or raise_to_bb is not None):
        return "FL7: BET requires non-null bet_pct and null raise_to_bb."

    # Rule 2
    if action_u == "RAISE" and (raise_to_bb is None or bet_pct is not None):
        return "FL7: RAISE requires non-null raise_to_bb and null bet_pct."

    # Rule 3
    if action_u in ("FOLD", "CHECK", "CALL") and (
        bet_pct is not None or raise_to_bb is not None
    ):
        return f"FL7: {action_u} requires both sizing fields null."

    # Rule 4
    if bet_pct is not None and bet_pct not in ALLOWED_BET_PCT:
        return f"FL7: bet_pct {bet_pct} ∉ {sorted(ALLOWED_BET_PCT)}."

    # Rule 5 (REVISED v2 — F-2 fix): NL-standard min-raise per §3.2 STEP 1.
    # previous_full_bet = to_call_bb + hero_already_committed_bb; min_raise = 2 × that.
    if raise_to_bb is not None:
        previous_full_bet = ctx.to_call_bb + hero_already_committed_bb(ctx)
        min_raise = 2.0 * previous_full_bet
        if raise_to_bb < min_raise or raise_to_bb > ctx.stack_size_bb:
            return (
                f"FL7: raise_to_bb={raise_to_bb} outside legal range "
                f"[{min_raise}, {ctx.stack_size_bb}]."
            )

    return None


# =============================================================================
# Consensus v2 — modal-action + weighted modal-sizing (blueprint v2 §3.6)
# =============================================================================


@dataclass(frozen=True)
class ConsensusV2Record:
    """Output of `compute_consensus_v2` per blueprint v2 §3.6.

    Fields
    ------
    spot_id : str
        Identifier for the spot being resolved.
    consensus_action : str
        Modal action across labellers (FOLD/CHECK/CALL/BET/RAISE), or "" if
        sizing-consensus failed at the action level.
    consensus_bet_pct : Optional[int]
        Modal `predicted_bet_pct` if consensus_action == BET; else None.
    consensus_raise_to_bb : Optional[int]
        Weighted-modal `predicted_raise_to_bb` if consensus_action == RAISE;
        else None.
    sizing_status : str
        One of:
            - "clean"                 : unique modal sizing within action-voters.
            - "ambiguous"             : tie broken via canonical-set / smaller-wins.
            - "malformed-via-arb"     : ≥3 action-voters were malformed_rejected;
                                        routed to owner-arb.
            - "high_disagreement"     : spread > 0.5 × max; modal still recorded
                                        but flagged for owner spot-check.
            - "n/a"                   : consensus_action is CHECK/CALL/FOLD (no
                                        sizing).
    rationale : str
        Human-readable audit log entry explaining the decision path.
    """

    spot_id: str
    consensus_action: str
    consensus_bet_pct: Optional[int]
    consensus_raise_to_bb: Optional[int]
    sizing_status: str
    rationale: str


def _modal_action(labels: list[NormalizedLabel]) -> tuple[str, dict[str, int]]:
    """Return (modal_action, vote_counts). Modal is the highest-count action.

    Ties are broken alphabetically (deterministic). Caller is expected to detect
    3-2 splits via the returned counts and route those to owner-arb separately.
    """
    counts: dict[str, int] = {}
    for lab in labels:
        a = (lab.predicted_action or "").upper()
        if not a:
            continue
        counts[a] = counts.get(a, 0) + 1
    if not counts:
        return "", {}
    # Deterministic tie-break: highest count, then alphabetical.
    best = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    return best, counts


def _bet_pct_tiebreak(modal_values: list[int], street: str) -> int:
    """Per §3.6 tie-break for BET sizing: prefer solver-aligned, then smaller.

    Solver-aligned per `feedback_solver_aligned_sizing.md`:
        flop  → 25 / 66
        turn  → 33 / 75
        river → 33 / 75 / 150
    """
    s = (street or "").lower()
    if s == "flop":
        priority = (25, 66)
    elif s == "turn":
        priority = (33, 75)
    elif s == "river":
        priority = (33, 75, 150)
    else:
        priority = ()
    for p in priority:
        if p in modal_values:
            return p
    return min(modal_values)


def _weighted_mode_raise_to_bb(
    voters: list[NormalizedLabel],
) -> tuple[Optional[int], dict[int, float]]:
    """Compute weighted modal raise_to_bb. Weights: clean/clean_all_in=1.0,
    ambiguous_resolved=0.7, malformed_rejected EXCLUDED.

    Returns (modal_value or None, weight_map). Ties broken by preferring the
    smaller value (conservative per §3.6).
    """
    weights: dict[int, float] = {}
    for lab in voters:
        if lab.status == "malformed_rejected":
            continue
        if lab.predicted_raise_to_bb is None:
            continue
        if lab.status in ("clean", "clean_all_in"):
            w = 1.0
        elif lab.status == "ambiguous_resolved":
            w = 0.7
        elif lab.status == "no_op":
            # Treat already-normalized inputs as clean-equivalent.
            w = 1.0
        else:
            w = 0.5
        weights[lab.predicted_raise_to_bb] = weights.get(lab.predicted_raise_to_bb, 0.0) + w
    if not weights:
        return None, {}
    # Sort by descending weight, then ascending value (smaller-wins tie-break).
    best = sorted(weights.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    return best, weights


def compute_consensus_v2(
    spot_labels: list[NormalizedLabel],
    opus_label: Optional[NormalizedLabel] = None,
    spot_context: Optional[SpotContext] = None,
) -> ConsensusV2Record:
    """Compute consensus v2 record per blueprint v2 §3.6.

    Parameters
    ----------
    spot_labels : list[NormalizedLabel]
        The N (typically 5) sonnet labellers' normalized outputs for a single spot.
        All labels must share the same `spot_id`.
    opus_label : Optional[NormalizedLabel]
        Optional opus tier-up label for the same spot. If provided AND
        opus voted the same action as the modal, opus's sizing vote is folded
        into the sizing pool with the same weighting rules as a sonnet vote.
    spot_context : Optional[SpotContext]
        Spot context (used for BET tie-break by street). Optional; if absent,
        BET tie-break falls back to smaller-wins only.

    Algorithm (blueprint v2 §3.6)
    -----------------------------
    Phase 1 — Action consensus (modal action across sonnets; opus folded in
              after a 3-2 split if present — simplified here to "modal includes
              opus when opus agrees with the modal").
    Phase 2 — Sizing consensus (computed only on labellers who voted the modal
              action):
        - BET   : modal predicted_bet_pct; tie-break via _bet_pct_tiebreak.
        - RAISE : weighted modal predicted_raise_to_bb; clean=1.0,
                  ambiguous_resolved=0.7, malformed_rejected EXCLUDED.
                  If ≥3 action-voters were malformed_rejected → sizing failure.
                  If spread (max - min) > 0.5 × max → high_disagreement (modal
                  still recorded but flagged for owner spot-check).
        - CHECK/CALL/FOLD : both sizing fields null; sizing_status="n/a".

    Returns ConsensusV2Record. Spots flagged for owner-arb are surfaced via the
    `sizing_status` field (caller is responsible for routing).
    """
    if not spot_labels:
        return ConsensusV2Record(
            spot_id="",
            consensus_action="",
            consensus_bet_pct=None,
            consensus_raise_to_bb=None,
            sizing_status="malformed-via-arb",
            rationale="Empty spot_labels; cannot compute consensus.",
        )

    spot_id = spot_labels[0].spot_id

    # ────────────────────────── Phase 1: action consensus ──────────────────────
    modal_action, vote_counts = _modal_action(spot_labels)
    if opus_label is not None:
        opus_action = (opus_label.predicted_action or "").upper()
        if opus_action and opus_action == modal_action:
            # Opus confirms modal — fold into pool for sizing (Phase 2).
            pass  # included in action_voters below
        # If opus dissents, modal_action stands but flagged via rationale.

    rationale_parts = [f"action votes={vote_counts}; modal={modal_action!r}"]

    if modal_action == "":
        return ConsensusV2Record(
            spot_id=spot_id,
            consensus_action="",
            consensus_bet_pct=None,
            consensus_raise_to_bb=None,
            sizing_status="malformed-via-arb",
            rationale=" | ".join(rationale_parts + ["no modal action; route to owner-arb."]),
        )

    # ────────────────────────── Phase 2: sizing consensus ──────────────────────
    action_voters = [
        lab for lab in spot_labels
        if (lab.predicted_action or "").upper() == modal_action
    ]
    if opus_label is not None and (opus_label.predicted_action or "").upper() == modal_action:
        action_voters = action_voters + [opus_label]

    # CHECK / CALL / FOLD: no sizing.
    if modal_action in ("CHECK", "CALL", "FOLD"):
        return ConsensusV2Record(
            spot_id=spot_id,
            consensus_action=modal_action,
            consensus_bet_pct=None,
            consensus_raise_to_bb=None,
            sizing_status="n/a",
            rationale=" | ".join(rationale_parts + [f"{modal_action}: no sizing."]),
        )

    # BET sizing consensus.
    if modal_action == "BET":
        bet_votes = [
            lab.predicted_bet_pct for lab in action_voters
            if lab.predicted_bet_pct is not None and lab.status != "malformed_rejected"
        ]
        if not bet_votes:
            return ConsensusV2Record(
                spot_id=spot_id,
                consensus_action="BET",
                consensus_bet_pct=None,
                consensus_raise_to_bb=None,
                sizing_status="malformed-via-arb",
                rationale=" | ".join(rationale_parts + ["BET: no non-malformed sizing votes."]),
            )
        counts: dict[int, int] = {}
        for v in bet_votes:
            counts[v] = counts.get(v, 0) + 1
        max_count = max(counts.values())
        modal_values = [k for k, c in counts.items() if c == max_count]
        if len(modal_values) == 1:
            return ConsensusV2Record(
                spot_id=spot_id,
                consensus_action="BET",
                consensus_bet_pct=modal_values[0],
                consensus_raise_to_bb=None,
                sizing_status="clean",
                rationale=" | ".join(rationale_parts + [
                    f"BET sizing votes={counts}; unique modal={modal_values[0]}."
                ]),
            )
        # Tie-break.
        street = (spot_context.street if spot_context is not None else "")
        picked = _bet_pct_tiebreak(modal_values, street)
        return ConsensusV2Record(
            spot_id=spot_id,
            consensus_action="BET",
            consensus_bet_pct=picked,
            consensus_raise_to_bb=None,
            sizing_status="ambiguous",
            rationale=" | ".join(rationale_parts + [
                f"BET sizing votes={counts}; tied modals={sorted(modal_values)}; "
                f"tie-break (street={street!r})={picked}."
            ]),
        )

    # RAISE sizing consensus (weighted modal, malformed excluded).
    if modal_action == "RAISE":
        # Count malformed action-voters.
        malformed_count = sum(
            1 for lab in action_voters if lab.status == "malformed_rejected"
        )
        # Sizing failure: ≥3 of the RAISE-voting labellers are malformed_rejected.
        # (Threshold matches the 3-2 split threshold used elsewhere per §3.6.)
        if malformed_count >= 3:
            return ConsensusV2Record(
                spot_id=spot_id,
                consensus_action="RAISE",
                consensus_bet_pct=None,
                consensus_raise_to_bb=None,
                sizing_status="malformed-via-arb",
                rationale=" | ".join(rationale_parts + [
                    f"RAISE sizing-consensus FAILURE: {malformed_count} of "
                    f"{len(action_voters)} action-voters malformed_rejected; "
                    "route to owner-arb."
                ]),
            )

        modal_value, weights = _weighted_mode_raise_to_bb(action_voters)
        if modal_value is None:
            return ConsensusV2Record(
                spot_id=spot_id,
                consensus_action="RAISE",
                consensus_bet_pct=None,
                consensus_raise_to_bb=None,
                sizing_status="malformed-via-arb",
                rationale=" | ".join(rationale_parts + [
                    "RAISE: no contributing sizing votes."
                ]),
            )

        # Spread check (high disagreement).
        contributing_values = list(weights.keys())
        spread = max(contributing_values) - min(contributing_values)
        high_disagree = (
            len(contributing_values) >= 2
            and spread > 0.5 * max(contributing_values)
        )
        # Whether the modal value is uniquely the top weight or tied with another.
        max_weight = max(weights.values())
        tied_values = [v for v, w in weights.items() if w == max_weight]
        if len(tied_values) == 1:
            status = "high_disagreement" if high_disagree else "clean"
        else:
            status = "ambiguous"  # tie was broken by smaller-wins (per §3.6)
        return ConsensusV2Record(
            spot_id=spot_id,
            consensus_action="RAISE",
            consensus_bet_pct=None,
            consensus_raise_to_bb=int(modal_value),
            sizing_status=status,
            rationale=" | ".join(rationale_parts + [
                f"RAISE sizing weights={weights}; modal={modal_value}; "
                f"spread={spread} (high_disagree={high_disagree}); "
                f"tied_values={sorted(tied_values)}."
            ]),
        )

    # Defensive fallthrough.
    return ConsensusV2Record(
        spot_id=spot_id,
        consensus_action=modal_action,
        consensus_bet_pct=None,
        consensus_raise_to_bb=None,
        sizing_status="malformed-via-arb",
        rationale=" | ".join(rationale_parts + [f"unknown action {modal_action!r}."]),
    )


# =============================================================================
# Batch processing + audit log
# =============================================================================


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def _build_context_index(context_path: Path) -> dict[str, dict[str, Any]]:
    """Return {spot_id: context_dict} from a `*_50hand.jsonl` context file."""
    idx: dict[str, dict[str, Any]] = {}
    for row in _load_jsonl(context_path):
        sid = row.get("spot_id")
        if sid is not None:
            idx[sid] = row
    return idx


def _label_to_v2_dict(label: NormalizedLabel) -> dict[str, Any]:
    """Convert a NormalizedLabel into the v2 on-disk JSON dict."""
    out: dict[str, Any] = {
        "spot_id": label.spot_id,
        "labeller_id": label.labeller_id,
        "predicted_action": label.predicted_action,
        "predicted_bet_pct": label.predicted_bet_pct,
        "predicted_raise_to_bb": label.predicted_raise_to_bb,
    }
    out.update(label.extras)
    return out


def _audit_record(label: NormalizedLabel, legacy_v: Optional[int]) -> dict[str, Any]:
    """Per-label audit entry written to `*_normalizer_audit.jsonl`."""
    return {
        "spot_id": label.spot_id,
        "labeller_id": label.labeller_id,
        "predicted_action": label.predicted_action,
        "legacy_sizing_pct": legacy_v,
        "predicted_bet_pct": label.predicted_bet_pct,
        "predicted_raise_to_bb": label.predicted_raise_to_bb,
        "status": label.status,
        "rationale": label.rationale,
    }


def normalize_batch(
    input_jsonl_path: str | Path,
    context_jsonl_path: str | Path,
    output_v2_path: Optional[str | Path] = None,
    audit_jsonl_path: Optional[str | Path] = None,
) -> dict[str, int]:
    """Normalise every label in `input_jsonl_path` and emit v2 + audit files.

    When `output_v2_path` is None, no v2 file is written (dry-run mode).
    When `audit_jsonl_path` is None, no audit file is written.

    Returns a summary dict::

        {
          "clean": int,
          "clean_all_in": int,        # NEW v2 (F-1 fix)
          "ambiguous_resolved": int,
          "malformed_rejected": int,
          "no_op": int,
          "total": int,
        }
    """
    in_path = Path(input_jsonl_path)
    ctx_path = Path(context_jsonl_path)
    labels = _load_jsonl(in_path)
    ctx_idx = _build_context_index(ctx_path)

    summary = {
        "clean": 0,
        "clean_all_in": 0,
        "ambiguous_resolved": 0,
        "malformed_rejected": 0,
        "no_op": 0,
        "total": 0,
    }
    v2_lines: list[str] = []
    audit_lines: list[str] = []

    for label in labels:
        sid = label.get("spot_id", "<unknown>")
        ctx_dict = ctx_idx.get(sid, {})
        normalized = normalize_label(label, ctx_dict)
        legacy_v = _coerce_int(label.get("predicted_sizing_pct"))

        summary[normalized.status] = summary.get(normalized.status, 0) + 1
        summary["total"] += 1

        v2_lines.append(json.dumps(_label_to_v2_dict(normalized)))
        audit_lines.append(json.dumps(_audit_record(normalized, legacy_v)))

    if output_v2_path is not None:
        out_path = Path(output_v2_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("\n".join(v2_lines) + ("\n" if v2_lines else ""), encoding="utf-8")

    if audit_jsonl_path is not None:
        audit_path = Path(audit_jsonl_path)
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        audit_path.write_text(
            "\n".join(audit_lines) + ("\n" if audit_lines else ""), encoding="utf-8"
        )

    return summary


# =============================================================================
# CLI
# =============================================================================


def _infer_context_path(input_path: Path) -> Path:
    """Given `batch_NNN_raw_labels_labeller_M.jsonl`, return `batch_NNN_50hand.jsonl`.

    Falls back to `<input>_50hand.jsonl` if pattern doesn't match.
    """
    name = input_path.name
    # Match "batch_NNN_raw_labels_..." => "batch_NNN_50hand.jsonl"
    if "_raw_labels_" in name:
        prefix = name.split("_raw_labels_", 1)[0]
        return input_path.parent / f"{prefix}_50hand.jsonl"
    return input_path.with_name(input_path.stem + "_50hand.jsonl")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sizing_schema_normalizer",
        description=(
            "Normalise legacy `predicted_sizing_pct` labels into the v2 split "
            "schema (`predicted_bet_pct` + `predicted_raise_to_bb`)."
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--dry-run",
        metavar="INPUT_JSONL",
        help=(
            "Print summary counts for the given raw-labels JSONL without "
            "writing any output files."
        ),
    )
    mode.add_argument(
        "--apply",
        metavar="INPUT_JSONL",
        help="Normalise the given raw-labels JSONL and write outputs.",
    )
    parser.add_argument(
        "--context",
        metavar="CONTEXT_JSONL",
        default=None,
        help=(
            "Path to matching `batch_NNN_50hand.jsonl` context file. "
            "If omitted, inferred from --apply/--dry-run path."
        ),
    )
    parser.add_argument(
        "--output",
        metavar="OUTPUT_V2_JSONL",
        default=None,
        help="Output path for v2 labels (required with --apply).",
    )
    parser.add_argument(
        "--audit",
        metavar="AUDIT_JSONL",
        default=None,
        help="Optional audit JSONL path (per-label status + rationale).",
    )

    args = parser.parse_args(argv)

    input_path = Path(args.dry_run if args.dry_run else args.apply)
    if not input_path.exists():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        return 2

    context_path = Path(args.context) if args.context else _infer_context_path(input_path)
    if not context_path.exists():
        print(f"ERROR: context file not found: {context_path}", file=sys.stderr)
        return 2

    if args.dry_run:
        summary = normalize_batch(
            input_jsonl_path=input_path,
            context_jsonl_path=context_path,
            output_v2_path=None,
            audit_jsonl_path=None,
        )
        print(
            "{{clean: {clean}, clean_all_in: {clean_all_in}, "
            "ambiguous_resolved: {ambiguous_resolved}, "
            "malformed_rejected: {malformed_rejected}}}".format(**summary)
        )
        print(
            f"(no_op: {summary['no_op']}, total: {summary['total']}; "
            f"input: {input_path}; context: {context_path})"
        )
        return 0

    # --apply path
    if args.output is None:
        print("ERROR: --apply requires --output", file=sys.stderr)
        return 2
    summary = normalize_batch(
        input_jsonl_path=input_path,
        context_jsonl_path=context_path,
        output_v2_path=Path(args.output),
        audit_jsonl_path=Path(args.audit) if args.audit else None,
    )
    print(
        "{{clean: {clean}, ambiguous_resolved: {ambiguous_resolved}, "
        "malformed_rejected: {malformed_rejected}}}".format(**summary)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
