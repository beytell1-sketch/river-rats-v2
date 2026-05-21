"""sizing_schema_normalizer.py — A0.1 backfill normalizer for 4-way corpus labels.

Provenance
==========
This module is the deterministic backfill normalizer specified in
`review/comms/DRAFT_BLUEPRINT_A0_SCHEMA_FIX_v1_2026-05-17.md` (ratified by
`review/comms/RATIFICATION_A0_BLUEPRINT_2026-05-17.md`). It converts legacy
4-way labels carrying the dual-semantics `predicted_sizing_pct` field into the
new split-schema form (`predicted_bet_pct` + `predicted_raise_to_bb`) defined
in blueprint §1.

Inputs consumed by this script (raw label files for batches 001-008) feed the
v9-4way training export. Per CLAUDE.md §6 training-provenance addendum
(2026-04-15), this module is part of the training pipeline and any model
artifact produced from its output must be reproducible by linking back to the
commit that introduced it.

The orchestrator ratification override (RATIFICATION_A0_BLUEPRINT_2026-05-17)
moves the labeller-brief patch from PR A0.1 to PR A0.3 — this file ships
WITHOUT a brief change. Brief still describes legacy `predicted_sizing_pct`.

Algorithm — RAISE normalization (blueprint §3.2)
-------------------------------------------------
For each RAISE label with legacy value v, three candidate interpretations are
considered:
    1. bb        — v as a literal raise-TO bb amount
    2. pct-by    — v as "% of pot raise-BY" => raise-to = facing_bet + v% * pot
    3. mult-bet  — v as "% multiplier of facing bet" (only for canonical mults)

Each candidate is filtered against legality (min_raise_to_bb <= x <= stack_bb).
Tie-breaks use canonical-value tables (CANONICAL_BB / CANONICAL_PCT /
CANONICAL_MULT). When both bb and pct are legal AND the value is in both
canonical sets, the bb interpretation wins (honours brief-intent per §3.2).

BET normalization (blueprint §3.3) is trivial: legacy v maps directly to
`predicted_bet_pct` if v is in the allowed enum; otherwise malformed_rejected.

Public API
----------
- `normalize_label(label_dict, spot_context_dict) -> NormalizedLabel`
- `normalize_batch(input_jsonl_path, context_jsonl_path, output_v2_path,
                   audit_jsonl_path) -> dict`
- CLI: `python -m river_rats_core.sizing_schema_normalizer --dry-run <path>`
       `python -m river_rats_core.sizing_schema_normalizer --apply <input>
            --context <50hand.jsonl> --output <v2 path> --audit <audit path>`

Min-raise convention
--------------------
Per blueprint §3.2 step 1: `min_raise_to_bb = to_call_bb * 2` (No-Limit
standard "double the bet"). Builder pre-flight verified against
`river-rats-core/poker_game.py` — the engine's `_apply_action` accepts any
raise amount (no enforced floor in code), so the blueprint's NL convention
is consistent with the engine. The reasoning chains in batches 001-007 also
follow this convention.

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
    """

    pot_bb: float
    to_call_bb: float
    facing_bet: int
    stack_size_bb: float
    street: str  # "preflop" | "flop" | "turn" | "river"


@dataclass(frozen=True)
class NormalizedSizing:
    """Result of normalising a single label's sizing fields.

    `status` is one of:
      - "clean"               : input matched expected schema; no inference needed.
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
    """Full label after normalisation, including the source spot/labeller id."""

    spot_id: str
    labeller_id: int
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

        # Step 1: pot context
        facing_bet_bb = ctx.to_call_bb
        min_raise_to_bb = ctx.to_call_bb * 2  # NL standard (blueprint §3.2)
        max_raise_to_bb = ctx.stack_size_bb

        # Step 2: candidate interpretations
        candidate_bb = v
        candidate_pct_to_bb = round(
            facing_bet_bb + (v / 100.0) * ctx.pot_bb
        )
        candidate_mult_to_bb = round((v / 100.0) * facing_bet_bb)

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
    labeller_id = int(label_dict.get("labeller_id", -1))
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
    )

    sized = normalize_sizing(action, legacy_v, ctx)

    return NormalizedLabel(
        spot_id=spot_id,
        labeller_id=labeller_id,
        predicted_action=action,
        predicted_bet_pct=sized.predicted_bet_pct,
        predicted_raise_to_bb=sized.predicted_raise_to_bb,
        status=sized.status,
        rationale=sized.rationale,
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

    # Rule 5
    if raise_to_bb is not None:
        min_raise = ctx.to_call_bb * 2
        if raise_to_bb < min_raise or raise_to_bb > ctx.stack_size_bb:
            return (
                f"FL7: raise_to_bb={raise_to_bb} outside legal range "
                f"[{min_raise}, {ctx.stack_size_bb}]."
            )

    return None


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
            "{{clean: {clean}, ambiguous_resolved: {ambiguous_resolved}, "
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
