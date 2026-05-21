# DRAFT BLUEPRINT — A0 Schema Fix: `predicted_sizing_pct` Dual-Semantics Repair (v2)

**Date:** 2026-05-21
**Author:** Architect (orchestrator-authorized; single-design commit)
**Status:** DRAFT — revision of v1 addressing QC pre-merge findings.
**Supersedes:** `review/comms/DRAFT_BLUEPRINT_A0_SCHEMA_FIX_v1_2026-05-17.md` (v1 retained as historical reference).
**Scope:** Unchanged from v1 — forward-looking schema split + backfill for 4-way corpus batches 001–008.
**Authority:** Per `feedback_orchestrator_decides_not_recommends.md`, this blueprint commits to a SINGLE DESIGN throughout. No menus. Owner can override any commitment; otherwise the design ships as written.

---

## Changes from v1 (per QC findings)

QC pre-merge audit `~/river-rats-qc/findings/2026-05-21-pr459-a0-blueprint-prereview.md` returned `ISSUES FOUND` (2 BLOCKER + 5 SHOULD_FIX + 3 NIT). This revision addresses the BLOCKERs and one SHOULD_FIX promoted to BLOCKER:

| QC ref | Severity | Fix in v2 | Section(s) revised |
|---|---|---|---|
| **F-1** | BLOCKER | Add explicit all-in detection branch BEFORE canonical-set tie-break. When `v == stack_size_bb`, route directly to `predicted_raise_to_bb = v`, status=`clean_all_in`. Resolves §3.2 / §7.3 contradiction. | §3.2 STEP 2.5 (NEW), §3.5 (test 13 added), §7.3 (text revised) |
| **F-2** | BLOCKER | Replace `min_raise_to_bb = to_call_bb * 2` with NL-standard context-aware formula. For preflop facing-open (hero already committed blinds), use `previous_full_bet = to_call_bb + hero_already_committed_bb`, `min_raise_to_bb = 2 × previous_full_bet`. Resolves 19 BB-defend spots in corpus where old rule under-floored min-raise. | §3.1 (revised), §3.2 STEP 1 (REVISED), §3.5 (test 14 added), §7.1.1 (settled), §7.5 (re-predicted) |
| **F-6** | SHOULD_FIX → BLOCKER | Existing `*_consensus.jsonl` has NO sizing field; v2 introduces two sizing columns. Add §3.6 specifying consensus_v2 modal-sizing algorithm: separate modal-vote on action and on sizing; tie-break rules for divergent sizing votes; owner-arb routing on consensus failure. | §3.6 (NEW), §3.5 (test 15 added) |

Additionally addressed inline (small revisions):
- **F-3** (v=66 RAISE omission in §7.5): added row to §7.5 prediction table.
- **F-7** (Example C is not a real tie-break): added Example C-2 demonstrating the actual tie-break path.

Explicitly **deferred** to v3 if needed:
- **F-4** (CANONICAL_MULT brittleness on adjacent multipliers like v=270): single spot today; absorbed by owner-arb queue. Defer.
- **F-5** (`stack_size_bb` semantics — starting vs effective): defer; corpus is uniformly 100bb today and the boundary cases are absorbed by status=`clean_all_in` (F-1 fix). Re-open at deep-stack 200bb axis introduction.
- **F-8** (cosmetic doc note for A0.2 PR body): noted inline in §6 PR A0.2 description; non-blocking.
- **F-9** (4 missing test scenarios): 3 of 4 are added in this v2 (tests 13–15); the 4th (opus-sonnet divergence) is **integrated into test 15** as a sub-case.
- **F-10** (regression test for "action unchanged by normalizer"): integrated into existing test 12 acceptance criterion; not a separate test class. Documented.
- **N-1, N-2, N-3**: deferred.

All other v1 commitments — schema split (§1), brief patch (§2), batch-008 strategy (§4), export schema (§5), rollout sequence under orchestrator override (§6) — remain UNCHANGED.

---

## Problem statement (one paragraph)

The 4-way labeller brief declares `predicted_sizing_pct` as an integer field with TWO different semantics keyed off `predicted_action`:
- For `BET`: integer **% of pot**
- For `RAISE`: integer **bb amount** (raise-to)

Direct inspection of `data/4way_corpus/full_700/` confirms labellers do not consistently honour the dual-semantic contract. Of 282 RAISE labels: 119 use the bb-amount convention (value=9), 62 use a pct-of-pot value (value=75), 21 use a multiplier-of-facing-bet (value=300, 360, 720), 28 sit at ambiguous value=22, with smaller residues at v=10, 22, 25, 27, 30, 66, 100, 270, 360. BET labels (574) are clean: all at 25/33/50/66/75. The dual semantics — and the field NAME `_pct` actively misleading for the RAISE branch — caused the drift.

The bug is **schema-level**, not labeller-level. Renaming the field will not help; we must SPLIT it. No 4-way export code or model artifact has shipped yet — this is a forward-looking fix with no model rollback risk. Batches 001–007 (350 hands × 5 labellers + opus tier-up) and partial batch-008 (~132 labels in flight) require deterministic backfill via normalizer.

---

## §1 — SCHEMA SPLIT (going forward)

### 1.1 New field schema

The single field `predicted_sizing_pct: int | null` is RETIRED for new labels. It is replaced by two mutually exclusive fields:

```json
{
  "predicted_bet_pct":      "int | null   — % of pot; populated iff predicted_action == BET",
  "predicted_raise_to_bb":  "int | null   — bb amount of the raise-TO size (NOT raise-by); populated iff predicted_action == RAISE"
}
```

Both fields are **null** for `CHECK`, `CALL`, `FOLD`. Exactly one is non-null for `BET` or `RAISE`. Never both non-null. Never both null for an aggressive action.

### 1.2 JSON schema (binding)

```json
{
  "type": "object",
  "required": ["spot_id", "labeller_id", "predicted_action", "predicted_bet_pct", "predicted_raise_to_bb", "confidence", "bucket", "reasoning", "num_opponents_at_decision", "primary_axis"],
  "properties": {
    "predicted_action":      {"enum": ["FOLD", "CHECK", "CALL", "BET", "RAISE"]},
    "predicted_bet_pct":     {"type": ["integer", "null"], "enum": [null, 25, 33, 50, 66, 75, 100, 150]},
    "predicted_raise_to_bb": {"type": ["integer", "null"], "minimum": 1, "maximum": 200}
  },
  "allOf": [
    {"if": {"properties": {"predicted_action": {"const": "BET"}}},
     "then": {"properties": {"predicted_bet_pct": {"not": {"const": null}}, "predicted_raise_to_bb": {"const": null}}}},
    {"if": {"properties": {"predicted_action": {"const": "RAISE"}}},
     "then": {"properties": {"predicted_raise_to_bb": {"not": {"const": null}}, "predicted_bet_pct": {"const": null}}}},
    {"if": {"properties": {"predicted_action": {"enum": ["FOLD", "CHECK", "CALL"]}}},
     "then": {"properties": {"predicted_bet_pct": {"const": null}, "predicted_raise_to_bb": {"const": null}}}}
  ]
}
```

### 1.3 Allowed value ranges (binding)

- `predicted_bet_pct ∈ {25, 33, 50, 66, 75, 100, 150}` — solver-aligned per `feedback_solver_aligned_sizing.md`. 50 and 100 included as adjacent legal values that occasionally appear in clean BET data.
- `predicted_raise_to_bb ∈ [⌈min_raise_to_bb⌉, ⌊stack_size_bb⌋]` where `min_raise_to_bb` is computed via the NL-standard formula in §3.2 STEP 1 and `stack_size_bb` is read directly from the spot context.

### 1.4 Validation rules (REJECT on violation)

A label is REJECTED at consensus-merge if any of these hold:

1. `predicted_action == BET` and (`predicted_bet_pct is None` or `predicted_raise_to_bb is not None`)
2. `predicted_action == RAISE` and (`predicted_raise_to_bb is None` or `predicted_bet_pct is not None`)
3. `predicted_action ∈ {FOLD, CHECK, CALL}` and (`predicted_bet_pct is not None` or `predicted_raise_to_bb is not None`)
4. `predicted_bet_pct ∉ {25, 33, 50, 66, 75, 100, 150}` (when non-null)
5. `predicted_raise_to_bb < min_raise_to_bb` OR `predicted_raise_to_bb > stack_size_bb` (illegal sizing; min_raise_to_bb per §3.2 STEP 1)
6. `predicted_action == BET` and `facing_bet > 0` (FL5 — illegal action; pre-existing rule)
7. `predicted_action == RAISE` and `facing_bet == 0` (FL5 — illegal action; pre-existing rule)

Rule violations 1–5 introduce a new failure class **FL7: sizing-field mismatch**. Rules 6–7 stay in FL5.

---

## §2 — BRIEF UPDATE (`data/4way_labeller_brief.md`)

Identical to v1 §2 (lines 31–34, 37, 105–112, 173–187 patches). Re-included here for builder convenience.

### 2.1 Lines 31–34 replacement

```diff
-**Sizing fields**:
-- `predicted_action: BET` or `RAISE` → MUST specify `predicted_sizing_pct` (an integer % of pot for BET; integer bb amount for RAISE)
-- `predicted_action: CHECK` or `CALL` or `FOLD` → `predicted_sizing_pct: null`
+**Sizing fields** (TWO separate fields — read carefully):
+- `predicted_action: BET` → set `predicted_bet_pct: <int>` (% of pot, ∈ {25, 33, 50, 66, 75, 100, 150}); set `predicted_raise_to_bb: null`.
+- `predicted_action: RAISE` → set `predicted_raise_to_bb: <int>` (bb amount of the raise-TO size — the TOTAL chips you push, NOT the raise-by increment); set `predicted_bet_pct: null`.
+- `predicted_action: CHECK | CALL | FOLD` → BOTH fields null.
+
+**Worked phrasing — copy these EXACTLY**:
+- BET 66% of pot: `"predicted_action": "BET", "predicted_bet_pct": 66, "predicted_raise_to_bb": null`
+- RAISE to 9bb total: `"predicted_action": "RAISE", "predicted_bet_pct": null, "predicted_raise_to_bb": 9`
+- CHECK: `"predicted_action": "CHECK", "predicted_bet_pct": null, "predicted_raise_to_bb": null`
+
+**Why two fields**: BET sizes are naturally expressed as % of pot (solver convention). RAISE sizes are naturally expressed as bb-total raise-TO (because raise-by/raise-to confusion + % of pot ambiguity in multiway is unrecoverable). Do not write a % in `predicted_raise_to_bb` — that is field-mismatch FL7, and your label is REJECTED at consensus.
```

### 2.2 FL7 entry

```diff
+**FL7 failure class — sizing-field mismatch**: writing a % value in `predicted_raise_to_bb` (e.g., 75, 300, 360) or a bb value in `predicted_bet_pct` (e.g., 9, 18) is a labelling defect. If you cannot compute the raise-to in bb, use `confidence: LOW` and write the value you intended in the reasoning prose; owner-arb queue will adjudicate. Do NOT write a malformed value.
```

### 2.3 Output schema replacement (lines 173–187)

```diff
 {
   "spot_id": "4WL-<axis>-<N>",
   "labeller_id": <N>,
   "predicted_action": "FOLD|CHECK|CALL|BET|RAISE",
-  "predicted_sizing_pct": <int or null>,
+  "predicted_bet_pct": <int or null>,
+  "predicted_raise_to_bb": <int or null>,
   "confidence": "HIGH|MEDIUM|LOW",
   ...
 }
```

### 2.4 Solver-aligned sizing section (lines 105–112)

```diff
 When you label a BET or RAISE action, use solver-aligned sizes:
+- **BET sizing (% of pot, into `predicted_bet_pct`)**:
+  - Flop: 25 or 66
+  - Turn: 33 or 75
+  - River: 33 / 75 / 150
+- **RAISE sizing (bb raise-TO, into `predicted_raise_to_bb`)**:
+  - vs flop bet: 3.0–4.0× the bet size, converted to total raise-to bb.
+  - vs turn bet: 2.5–3.0× the bet size.
+  - vs river bet: 2.5–3.5× the bet size.
+  - **Preflop BB-defend min 3-bet**: facing a 2.5bb open, min-raise is to 5bb (i.e., raise-to ≥ 2 × open_size). A min-raise 3-bet from BB is `predicted_raise_to_bb: 5`, NOT 4.
+The `predicted_raise_to_bb` value must be the FINAL chip count put in by hero (raise-to), not the increment.
```

---

## §3 — BACKFILL NORMALIZER (batches 001–008)

### 3.1 File layout and signatures

The normalizer lives in `river-rats-core/sizing_schema_normalizer.py`. Pure-functional; no I/O side effects in the core function. A thin CLI wrapper handles file iteration.

```python
# river-rats-core/sizing_schema_normalizer.py

from dataclasses import dataclass
from typing import Literal

Action = Literal["FOLD", "CHECK", "CALL", "BET", "RAISE"]
NormalizationStatus = Literal[
    "clean",                 # unique legal interpretation
    "clean_all_in",          # v == stack_size_bb (F-1 fix)
    "ambiguous_resolved",    # multiple legal candidates; canonical-set tie-break applied
    "malformed_rejected",    # no legal interpretation; routed to owner-arb
    "no_op",                 # FOLD/CHECK/CALL — sizing already null
]

@dataclass(frozen=True)
class SpotContext:
    """Subset of fields from batch_NNN_50hand.jsonl needed for legality checks.

    Field names verified against actual corpus schema (batch_001_50hand.jsonl):
        spot_id, axis, stack_size_bb, preflop_action (text), board, hero_position,
        hero_cards, num_opponents_at_decision, street, facing_bet, to_call_bb,
        pot_bb, primary_axis, source_anchor, variant_type
    """
    pot_bb: float
    to_call_bb: float
    facing_bet: int               # 0 or 1
    stack_size_bb: float          # effective stack; corpus today uniformly 100
    street: str                   # "preflop" | "flop" | "turn" | "river"
    hero_position: str            # "UTG"|"HJ"|"CO"|"BTN"|"SB"|"BB"

@dataclass(frozen=True)
class NormalizedSizing:
    predicted_bet_pct: int | None
    predicted_raise_to_bb: int | None
    status: NormalizationStatus
    rationale: str                # human-readable audit log entry

def hero_already_committed_bb(ctx: SpotContext) -> float:
    """
    Derive the chips hero already has in the pot for the CURRENT betting round.
    The corpus 50hand.jsonl schema has no explicit `hero_already_committed_bb`
    field; we derive from street + hero_position.

    Preflop: SB has posted 0.5bb; BB has posted 1.0bb; all others 0.0bb.
    Postflop: 0.0bb (the current street starts with hero's contribution at 0
              because to_call_bb is the bet hero faces this street with no
              prior contribution from hero this street).
    """
    if ctx.street == "preflop":
        if ctx.hero_position == "BB":
            return 1.0
        if ctx.hero_position == "SB":
            return 0.5
    return 0.0

def normalize_sizing(
    action: Action,
    legacy_sizing_pct: int | None,
    ctx: SpotContext,
) -> NormalizedSizing:
    """
    Convert a legacy `predicted_sizing_pct` value into the new field schema.

    Behaviour:
    - FOLD/CHECK/CALL with non-null legacy value: WARN (legacy schema bug),
      output both fields = None, status="no_op".
    - BET with legacy value v: predicted_bet_pct = v if v ∈ {25,33,50,66,75,100,150},
      else status="malformed_rejected".
    - RAISE: §3.2 algorithm.
    """
    ...

def run_batch(input_path: str, output_path: str, context_path: str) -> dict:
    """
    Read `*_raw_labels_labeller_N.jsonl` + matching `*_50hand.jsonl` context,
    emit `*_raw_labels_labeller_N_v2.jsonl` with normalized fields,
    plus `*_normalizer_audit.jsonl` with per-label status + rationale.
    Returns: {clean: int, clean_all_in: int, ambiguous_resolved: int, malformed_rejected: int, no_op: int}.
    """
    ...
```

### 3.2 RAISE normalization algorithm (commit to ONE approach)

For each RAISE label with `legacy_sizing_pct = v`:

```
STEP 1 (REVISED — F-2 fix): Compute pot context with NL-standard min-raise.

  facing_bet_bb       = ctx.to_call_bb                  # amount hero must add to call
  hero_committed_bb   = hero_already_committed_bb(ctx)  # see §3.1 derivation
  previous_full_bet   = facing_bet_bb + hero_committed_bb
                                  # = total chips the previous bettor has at the bet level
                                  # Preflop facing 2.5bb open from BB: 1.5 + 1.0 = 2.5
                                  # Postflop facing a 9bb bet (hero has 0 committed this street): 9.0 + 0.0 = 9.0
                                  # Preflop facing a 3-bet (hero opened to 2.5, faces 3-bet to 9):
                                  #     to_call_bb = 9.0 - 2.5 = 6.5; hero_committed_bb = 2.5; previous_full_bet = 9.0

  min_raise_to_bb     = 2 * previous_full_bet
                                  # NL-standard: min raise-to = 2 × the current bet level.
                                  # Equivalently: raise increment ≥ previous raise increment, where the
                                  # opening raise itself is treated as the prior increment.
                                  # Preflop BB-defend example: previous_full_bet=2.5 → min_raise_to=5.0 ✓
                                  # Postflop bet=9 example:    previous_full_bet=9.0 → min_raise_to=18.0 ✓
                                  # Preflop 3-bet-to-9 example: previous_full_bet=9.0 → min_raise_to=18.0 ✓

  max_raise_to_bb     = ctx.stack_size_bb               # all-in cap

  # NOTE on engine alignment: river-rats-core/poker_game.py is permissive (no min-raise
  # legality check at action time). The spec uses the NL-standard rule above independent
  # of engine. See §7.1.1 for the verified ratification.

STEP 2: Compute the candidate interpretations.

  candidate_bb         = v
                                  # interpret as raise-to bb
  candidate_pct_to_bb  = round(facing_bet_bb + (v / 100.0) * ctx.pot_bb)
                                  # interpret v as "% of pot raise-BY", convert to raise-to:
                                  # raise-by = v% × pot; raise-to = facing_bet + raise-by
  candidate_mult_to_bb = round((v / 100.0) * facing_bet_bb)
                                  # interpret v as "% multiplier of facing bet"
                                  # used ONLY when v ∈ CANONICAL_MULT

STEP 2.5 (NEW — F-1 fix): All-in detection.

  # If labeller wrote v exactly equal to the stack size, interpret as
  # an all-in raise-to tell. This branch fires BEFORE the canonical-set
  # tie-break so that v=100 on a 100bb stack is not silently re-routed
  # through the pct branch (which would produce raise-to=16, contradicting
  # the §7.3 commitment to all-in interpretation).

  if v == int(round(ctx.stack_size_bb)):
      predicted_raise_to_bb = v
      status = "clean_all_in"
      predicted_bet_pct = None
      return  # SKIP remaining tie-break logic

  # Note: at stack_size_bb=200 (future deep-stack axis), v=100 does NOT match this
  # branch. v=100 would fall through to STEP 3+ legality + canonical-set tie-break,
  # which is correct — pot-sized raise on a deep stack is a legitimate non-all-in tell.

STEP 3: Legality filter.

  legal_bb   = min_raise_to_bb <= candidate_bb         <= max_raise_to_bb
  legal_pct  = min_raise_to_bb <= candidate_pct_to_bb  <= max_raise_to_bb
  legal_mult = min_raise_to_bb <= candidate_mult_to_bb <= max_raise_to_bb

STEP 4: Tie-break (canonical-value table).

  CANONICAL_BB   = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 18, 22, 27, 30}
  CANONICAL_PCT  = {25, 33, 50, 66, 75, 100, 150}
  CANONICAL_MULT = {300, 360, 720}

  # Multiplier interpretation for explicit multiplier tells:
  if v in CANONICAL_MULT and legal_mult:
      predicted_raise_to_bb = candidate_mult_to_bb
      status = "ambiguous_resolved"

  # Pure bb interpretation (most common path):
  elif v in CANONICAL_BB and legal_bb and not (v in CANONICAL_PCT and legal_pct):
      predicted_raise_to_bb = candidate_bb
      status = "clean"

  # Pure pct interpretation:
  elif v in CANONICAL_PCT and legal_pct and not (v in CANONICAL_BB and legal_bb):
      predicted_raise_to_bb = candidate_pct_to_bb
      status = "ambiguous_resolved"

  # Both legal AND in both canonical sets (e.g., v=22 with both legal):
  elif legal_bb and legal_pct:
      # Tie-break (binding): prefer bb interpretation, because the original brief
      # said "integer bb amount for RAISE" — brief-intent is bb. Honoured on ties.
      predicted_raise_to_bb = candidate_bb
      status = "ambiguous_resolved"

  # Only one legal:
  elif legal_bb and not legal_pct:
      predicted_raise_to_bb = candidate_bb
      status = "clean"
  elif legal_pct and not legal_bb:
      predicted_raise_to_bb = candidate_pct_to_bb
      status = "ambiguous_resolved"

  # Neither legal:
  else:
      predicted_raise_to_bb = None
      status = "malformed_rejected"
      # Spot routed to batch_NNN_owner_arb_queue_normalizer.jsonl

  predicted_bet_pct = None  # always None for RAISE
```

**Branch ordering invariant (BINDING):** STEP 2.5 (all-in detection) fires BEFORE STEP 3 (legality) and STEP 4 (tie-break). This is the F-1 fix; v1's algorithm ran STEP 4 before any all-in check, which produced raise-to=16 on the only v=100 spot in the corpus (4WF-MULTIWAY-171).

**Rationale for the all-in branch ordering:** the §7.3 commitment ("if a labeller writes `legacy_sizing_pct` equal to `stack_size_bb`, normalizer interprets as all-in raise-to") is now structurally enforced by branch ordering rather than relying on canonical-set membership accidents. RATIFICATION §7.3 stands as written; v1 contradicted it because the canonical-set branches fired first.

### 3.3 BET normalization (trivial)

For each BET label with `legacy_sizing_pct = v`:
- `predicted_bet_pct = v`
- `predicted_raise_to_bb = None`
- `status = "clean"` if `v ∈ {25, 33, 50, 66, 75, 100, 150}`, else `"malformed_rejected"`

Empirical inspection shows BET labels are 100% clean.

### 3.4 Worked examples

**Example A — clean bb interpretation** (`v = 9`, RAISE, postflop)

Input row (`4WF-CLOSING--306`):
- `pot_bb = 12.5`, `to_call_bb = 2.5`, `facing_bet = 1`, `stack_size_bb = 100`, `street = "flop"`, `hero_position = "BTN"`
- Label: `predicted_action = RAISE`, `legacy_sizing_pct = 9`

```
hero_committed_bb     = 0 (postflop, no prior contribution this street)
previous_full_bet     = 2.5 + 0 = 2.5
min_raise_to_bb       = 2 * 2.5 = 5.0
max_raise_to_bb       = 100

STEP 2.5: v=9 != 100 (stack), skip all-in branch.

candidate_bb          = 9                   ✓ legal (5 ≤ 9 ≤ 100)
candidate_pct_to_bb   = round(2.5 + 0.09 × 12.5) = 4   ✗ illegal (4 < 5)
candidate_mult_to_bb  = round(0.09 × 2.5) = 0          ✗ illegal

Result: legal_bb only → predicted_raise_to_bb = 9, status = "clean"
```

**Example B — pct interpretation** (`v = 75`, RAISE, postflop)

Input (hypothetical): `pot_bb = 36.5`, `to_call_bb = 9.0`, `stack_size_bb = 100`, `street = "flop"`.

```
hero_committed_bb     = 0; previous_full_bet = 9.0; min_raise_to_bb = 18.0
candidate_bb          = 75                  ✓ legal (18 ≤ 75 ≤ 100)
candidate_pct_to_bb   = round(9.0 + 0.75 × 36.5) = 36   ✓ legal
candidate_mult_to_bb  = round(0.75 × 9.0) = 7           ✗ illegal
75 ∈ CANONICAL_PCT, 75 ∉ CANONICAL_BB → pure pct branch
→ predicted_raise_to_bb = 36, status = "ambiguous_resolved"
```

**Example C-1 — boundary case (pct just illegal)** (`v = 22`, pot=36.5, RAISE)

```
previous_full_bet=9.0, min_raise_to_bb=18.0
candidate_bb=22 ✓ legal; candidate_pct_to_bb=round(9.0+0.22×36.5)=17 ✗ (17<18 by 1bb)
Only legal_bb → predicted_raise_to_bb=22, status="clean"
```

**Example C-2 — real tie-break path** (`v = 22`, pot=45, RAISE) — F-7 fix

```
hero_committed_bb=0; previous_full_bet=9.0; min_raise_to_bb=18.0; stack=100
candidate_bb=22                              ✓ legal (18 ≤ 22 ≤ 100)
candidate_pct_to_bb=round(9.0+0.22×45)=19    ✓ legal (18 ≤ 19 ≤ 100)
candidate_mult_to_bb=round(0.22×9)=2         ✗ illegal
22 ∈ CANONICAL_BB AND legal_bb; 22 ∉ CANONICAL_PCT but legal_pct
→ Pure bb branch (canonical match) → predicted_raise_to_bb=22, status="ambiguous_resolved"
```

If instead v ∈ both canonical sets and both legal (a hypothetical pure tie), the tie-break "prefer bb" rule binds. Test 6 covers this; Example C-2 demonstrates the canonical-set branch hit on the real corpus value v=22.

**Example D — preflop BB-defend min-raise (NEW — F-2 fix)** (`v = 5`, RAISE, preflop)

Input row (`4WF-CLOSING--212`):
- `pot_bb = 11.5`, `to_call_bb = 1.5`, `stack_size_bb = 100`, `street = "preflop"`, `hero_position = "BB"`
- Label: `predicted_action = RAISE`, `legacy_sizing_pct = 5` (min-raise 3-bet from BB facing 2.5bb open)

```
hero_committed_bb     = 1.0 (BB has posted)
previous_full_bet     = 1.5 + 1.0 = 2.5         # = the open size
min_raise_to_bb       = 2 × 2.5 = 5.0           # NL min-raise from BB
max_raise_to_bb       = 100

STEP 2.5: v=5 != 100, skip all-in branch.

candidate_bb          = 5                      ✓ legal (5 ≤ 5 ≤ 100, boundary)
candidate_pct_to_bb   = round(1.5 + 0.05 × 11.5) = 2   ✗ illegal
candidate_mult_to_bb  = round(0.05 × 1.5) = 0          ✗ illegal

Result: legal_bb only → predicted_raise_to_bb = 5, status = "clean"
```

Under v1's old `min_raise_to_bb = to_call_bb × 2 = 3.0` rule, this same v=5 spot would have computed `min_raise = 3.0`, admitting the label as clean — same outcome here, but the rule would ALSO have admitted illegal v=4 ("raise-to 4bb" — which is below 2 × open). The v2 formula correctly rejects v=4 on a BB defend.

**Example E — all-in raise** (`v = 100`, RAISE, postflop, stack=100) — F-1 fix

Input row (`4WF-MULTIWAY-171`):
- `pot_bb = 13.5`, `to_call_bb = 2.5`, `stack_size_bb = 100`, `street = "flop"`, `hero_position = "BTN"`
- Label: `predicted_action = RAISE`, `legacy_sizing_pct = 100` (labeller_4)

```
hero_committed_bb = 0; previous_full_bet = 2.5; min_raise_to_bb = 5.0

STEP 2.5: v=100 == stack_size_bb=100 → ALL-IN TELL
→ predicted_raise_to_bb = 100, status = "clean_all_in"
   SKIP STEP 3+4
```

Audit log rationale: `"v=100 == stack_size_bb=100; interpreted as all-in raise-to per §3.2 STEP 2.5 (F-1 fix). Skipped canonical-set tie-break."`

Under v1's old algorithm, this same v=100 spot would have routed through STEP 4 (`100 ∈ CANONICAL_PCT, 100 ∉ CANONICAL_BB`), giving `predicted_raise_to_bb = round(2.5 + 1.0 × 13.5) = 16` — silently re-interpreting an all-in as a pot-sized raise. v2 fixes this.

### 3.5 Test coverage (mandatory before normalizer ships)

Unit tests in `river-rats-core/tests/test_sizing_schema_normalizer.py`:

1. **test_check_call_fold_legacy_value_warned** — non-null `legacy_sizing_pct` on FOLD/CHECK/CALL emits warning, normalizes to null/null, status=`no_op`.
2. **test_bet_clean_value** — BET v=66 → `predicted_bet_pct=66`, `predicted_raise_to_bb=None`, status=`clean`.
3. **test_bet_off_solver_value** — BET v=40 → status=`malformed_rejected`.
4. **test_raise_clean_bb_canonical** — Example A (v=9, pot=12.5, to_call=2.5).
5. **test_raise_pct_canonical** — Example B (v=75, pot=36.5, to_call=9.0).
6. **test_raise_tiebreak_both_legal_prefers_bb** — synthetic pure-tie case (v=22, pot=45, to_call=9 → both bb=22 and pct=19 legal; ∈ CANONICAL_BB only; resolves to bb).
7. **test_raise_multiplier_720** — preflop squeeze v=720, to_call=2.5 → raise-to=18bb.
8. **test_raise_multiplier_300_4bet** — v=300, to_call=9 → raise-to=27bb.
9. **test_raise_neither_legal_malformed** — v=2 facing 9bb (below min-raise) → `malformed_rejected`.
10. **test_raise_above_stack_malformed** — v=201 with stack=100 → `malformed_rejected`.
11. **test_round_trip_idempotence** — normalizer applied to already-normalized v2 file is no-op (no state mutation).
12. **test_consensus_alignment** — five labellers' divergent legacy values for one spot all normalize to same `predicted_raise_to_bb` when consensus action is RAISE. **Acceptance criterion includes**: `output.predicted_action == input.predicted_action` byte-equal for every label (F-10 invariant).
13. **(NEW — F-1)** **test_raise_all_in_v_equals_stack** — v=100 on 100bb stack, postflop spot (pot=13.5, to_call=2.5). Expect `predicted_raise_to_bb = 100`, `status = "clean_all_in"`, and verify the STEP 2.5 short-circuit fires (i.e., NOT routed through CANONICAL_PCT branch). Variant sub-case: same v=100 on 200bb stack must NOT trigger all-in; falls through to pct branch.
14. **(NEW — F-2)** **test_raise_preflop_bb_defend_min_raise** — Example D (v=5, to_call=1.5, pot=11.5, hero_position=BB, street=preflop). Verify `min_raise_to_bb = 5.0` (NOT 3.0); v=5 is legal; status=`clean`. Negative sub-case: v=4 on the same context → `malformed_rejected` (4 < min_raise=5).
15. **(NEW — F-6)** **test_consensus_v2_sizing_modal_5_labellers** — see §3.6. Five labellers vote (RAISE, RAISE, RAISE, RAISE, RAISE) with normalized `predicted_raise_to_bb` ∈ {9, 9, 9, 22, 22}; expect modal=9. Sub-cases:
    - **15a — opus-sonnet sizing divergence (F-9 absorption)**: 5 sonnets all vote v_normalized=9; opus tier-up votes v_normalized=10. Expect modal=9 (opus is one vote in a 6-vote pool; tie-break does not flip the majority).
    - **15b — sizing consensus failure**: votes = {9, 22, 36, 75, 100} (5 distinct values, no mode). Expect spot routed to owner-arb queue with reason="sizing_consensus_failure".

**Acceptance criterion: all 15 tests pass; coverage ≥ 95% lines.** (Up from 12 in v1.)

### 3.6 Consensus v2 schema and modal-sizing logic (NEW vs v1)

**Motivation (F-6).** The existing `data/4way_corpus/full_700/batch_NNN_consensus.jsonl` schema has NO sizing field — only `spot_id`, `consensus_state`, `consensus_action`, `sonnet_votes`, `opus_vote`. v1's RH-5 dismissed this as "no code change required beyond field-name plumbing." QC verified this is incorrect: introducing two sizing columns in consensus_v2 IS a code change. v2 specifies the algorithm here.

**Consensus v2 record schema:**

```json
{
  "spot_id": "...",
  "consensus_state": "all-agree | split-3-2 | opus-overrode | sizing-consensus-failure | ...",
  "consensus_action": "FOLD | CHECK | CALL | BET | RAISE",
  "consensus_bet_pct": "int | null",         // populated iff consensus_action == BET
  "consensus_raise_to_bb": "int | null",     // populated iff consensus_action == RAISE
  "sonnet_votes": ["BET", "BET", ...],       // unchanged
  "opus_vote": "BET | null",                 // unchanged
  "sonnet_sizing_votes": [66, 66, 66, 75, 66],  // NEW: per-labeller normalized sizing
  "opus_sizing_vote": 66                     // NEW: opus tier-up normalized sizing (or null if no tier-up)
}
```

**Algorithm (binding):**

For each spot:

**Phase 1 — Action consensus (unchanged from v1):**
1. Compute modal action across the 5 Sonnet labellers' normalized labels.
2. If 5-0 or 4-1: `consensus_action = mode`, `consensus_state = "all-agree"` or `"split-4-1"`.
3. If 3-2 split: invoke Opus tier-up. If Opus agrees with the 3-side, `consensus_action = 3-side mode`, `consensus_state = "split-3-2-opus-confirmed"`. If Opus dissents to a 3rd action (e.g., 3 BET / 2 RAISE / 1 CALL from Opus), spot routes to owner-arb with `consensus_state = "action-consensus-failure"`.

**Phase 2 — Sizing consensus (NEW):**

This phase runs AFTER Phase 1 commits a `consensus_action` AND AFTER the normalizer has produced per-labeller normalized sizing values. Sizing-consensus is computed ONLY on the labellers whose `predicted_action == consensus_action` (i.e., labellers who agreed on the action). Opus tier-up sizing vote (if Opus voted) is included in the modal pool.

- **If `consensus_action == BET`:**
  - Pool = `{labeller_i.predicted_bet_pct for i in labellers if labeller_i.predicted_action == BET}`
                                                                                  ∪ `{opus.predicted_bet_pct}` (if Opus voted BET)
  - Compute mode across the pool (each value is one of the canonical 7 enum values).
  - If unique mode: `consensus_bet_pct = mode`, `consensus_raise_to_bb = null`.
  - **Tie-break (multiple modal values, e.g., 2×66 vs 2×75):** prefer the solver-aligned value for the street (per `feedback_solver_aligned_sizing.md`). For flop, prefer 25 or 66 in that order; for turn, prefer 33 or 75 in that order; for river, prefer 33, 75, 150 in that order. If still tied (e.g., both candidates are solver-aligned), prefer the SMALLER value (conservative).

- **If `consensus_action == RAISE`:**
  - Pool = `{labeller_i.predicted_raise_to_bb for i in labellers if labeller_i.predicted_action == RAISE AND labeller_i.normalizer_status != "malformed_rejected"}`
                                                                                  ∪ `{opus.predicted_raise_to_bb}` (if Opus voted RAISE AND opus.normalizer_status != "malformed_rejected")
  - Compute mode across the pool.
  - If unique mode: `consensus_raise_to_bb = mode`.
  - **Tie-break — divergent values (binding):**
    1. Weight by normalizer status: clean > clean_all_in > ambiguous_resolved > malformed_rejected. Specifically, in computing the mode, count each `clean`/`clean_all_in` vote as weight 1.0; each `ambiguous_resolved` vote as weight 0.7. `malformed_rejected` votes are excluded from the pool entirely (above).
    2. If weighted-modal is still tied: prefer the SMALLER value (conservative — smaller raise-to is the lower-risk interpretation).
  - **Sizing-consensus failure (route to owner-arb):**
    - If ≥3 of the RAISE-voting labellers are `malformed_rejected` (i.e., the pool has fewer than 2 contributing values from the labeller side), set `consensus_state = "sizing-consensus-failure"`, `consensus_raise_to_bb = null`. Spot is routed to owner-arb queue.
    - If pool spread (max − min) exceeds 50% of the larger value (e.g., votes 9 and 22 differ by 13bb where 22 × 0.5 = 11; spread 13 > 11 → high disagreement), set `consensus_state = "sizing-consensus-high-disagreement"`. The modal value is still recorded but flagged for owner-arb spot-check.

- **If `consensus_action ∈ {CHECK, CALL, FOLD}`:** both `consensus_bet_pct` and `consensus_raise_to_bb` are null. No sizing computation.

**Invariant (BINDING):** sizing-consensus runs AFTER normalizer per-label. Sizing votes from labellers who voted a DIFFERENT action than consensus are EXCLUDED from the pool (rationale: their sizing was for a different action; mixing it would corrupt the modal).

**Code locus:** new function `compute_sizing_consensus(action, normalized_labels, opus_label, ctx)` in `river-rats-core/sizing_schema_normalizer.py`, invoked from the consensus-merge wrapper. The existing `consensus_rule` function (in `scripts/dispatch_4way_labelling_pilot.py` or equivalent) is extended to call this — code change documented in PR A0.2 acceptance.

---

## §4 — IN-FLIGHT BATCH-008 STRATEGY

**Commit: RESUME under old brief; normalize post-hoc.** (Unchanged from v1.)

Rationale (unchanged):
- L1=50/50, L2=36/50, L3=11/50, L4=10/50, L5=25/50 → 132 labels already produced. Restart wastes that work.
- Normalizer is the same code path; zero incremental complexity.
- Labellers have warm-state context; restart forces re-briefing with no benefit (per `feedback_no_deadlines.md`).
- New brief is forward-looking; batch-009+ uses split schema natively.

Decision boundary: if batch-008 produces >10% malformed-rejected, orchestrator+owner review whether to invalidate. Expected rate ≤8% based on batches 001–007 distribution.

---

## §5 — EXPORT SCHEMA for v9-4way training

### 5.1 Training CSV columns (unchanged)

| Column | Type | Domain | Populated when |
|---|---|---|---|
| `action` | categorical | FOLD/CHECK/CALL/BET/RAISE | always |
| `bet_pct` | float | {25, 33, 50, 66, 75, 100, 150} or NaN | iff action=BET |
| `raise_to_bb_normalized` | float | (0, ∞) or NaN | iff action=RAISE |
| `raise_to_bb_raw` | float | (0, 200] or NaN | iff action=RAISE (audit column) |

### 5.2 Normalization basis (unchanged: divide by `pot_bb`)

`raise_to_bb_normalized = predicted_raise_to_bb / pot_bb`. Same rationale as v1.

Edge case: `pot_bb = max(pot_bb, 0.5)` guard. Empirically not triggered (corpus pot_bb ≥ 7).

### 5.3 BET vs RAISE feature symmetry (unchanged)

Both columns express "% of pot." Kept separate for failure-direction diagnostics per `feedback_failure_direction_classification.md`.

---

## §6 — ROLLOUT SEQUENCE

Per orchestrator RATIFICATION override (still applies in v2). Three PRs in strict sequence.

### PR A0.1 — Schema + normalizer (foundation), NO BRIEF CHANGE

**Files added**:
- `river-rats-core/sizing_schema_normalizer.py` (~350 lines — modestly bigger than v1's 300 because of STEP 2.5 + helper functions + §3.6 sizing-consensus function)
- `river-rats-core/tests/test_sizing_schema_normalizer.py` (**15 tests** per §3.5; 3 new beyond v1's 12)

**No brief change.** Brief stays at v1 (legacy single field).

**Acceptance tests**:
- All **15** normalizer unit tests pass.
- `--dry-run` against batch_001_raw_labels_labeller_1.jsonl produces clean summary `{clean: N, clean_all_in: K0, ambiguous_resolved: M, malformed_rejected: K, no_op: J}`.

### PR A0.2 — Backfill batches 001–007

**Files added**:
- `data/4way_corpus/full_700/batch_NNN_raw_labels_labeller_M_v2.jsonl` (35 files)
- `data/4way_corpus/full_700/batch_NNN_raw_labels_opus_tierup_v2.jsonl` (7 files)
- `data/4way_corpus/full_700/batch_NNN_consensus_v2.jsonl` (7 files — re-computed with §3.6 sizing-consensus)
- `data/4way_corpus/full_700/batch_NNN_normalizer_audit.jsonl` (7 files)
- `data/4way_corpus/full_700/batch_NNN_owner_arb_queue_normalizer.jsonl` (7 files; may be empty)

**Acceptance tests** (unchanged from v1 except as marked):
- v2 file has same `spot_id` set as v1.
- For every BET label in v1, v2 has matching `predicted_bet_pct` and null `predicted_raise_to_bb`.
- For every RAISE label with `status ∈ {clean, clean_all_in}`, v2 has the appropriate numeric value in `predicted_raise_to_bb`.
- For every RAISE label classified `malformed_rejected`, that spot appears in `owner_arb_queue_normalizer.jsonl` and is excluded from `consensus_v2.jsonl`.
- **(NEW per §3.6):** consensus_v2 sizing fields are populated per the §3.6 algorithm. Verify on a hand-picked random sample of 10 spots that the modal sizing matches manual inspection.
- Per-batch malformed-rejected rate reported; >15% blocks pending review.
- v2 consensus action distribution matches v1 consensus action distribution exactly (sizing-driven action changes are HARD FAIL — F-10 invariant).

**PR description note (per F-8):** "v2 files use the post-A0.3 split schema; brief.md stays at v1 single-field schema until A0.3. Schema validation between A0.2 and A0.3 will see brief ≠ v2 files; this is expected per orchestrator sequencing override."

### PR A0.3 — Batch-008 resume + normalize + brief patch (FINAL)

Unchanged from v1 + orchestrator override:
- Step 1: labellers 2–5 resume batch-008 under v1 brief.
- Step 2: confirm all 5 batch-008 labellers complete.
- Step 3: run normalizer → `batch_008_*_v2.jsonl` + consensus.
- Step 4 (FINAL commit on A0.3 branch): apply brief patch per §2.
- Brief change takes effect at batch-009 (mini-pilot acceptance per v1 §6 A0.3).

---

## §7 — RATIFICATION CHECKLIST

### 7.1 Legality-check edge cases

- [x] **7.1.1 (UPDATED per F-2):** Min-raise rule verified — `river-rats-core/poker_game.py` is permissive (no min-raise check at action time; engine accepts whatever raise-to value the action emitter computes). The v2 spec uses the NL-standard min-raise rule (`min_raise_to_bb = 2 × previous_full_bet`) independently of engine. Builder is NOT expected to harmonize engine behaviour — the engine is downstream of the spec, not authoritative for it.
- [x] **7.1.2 All-in cap:** `max_raise_to_bb = stack_size_bb`. Confirmed correct for current 100bb corpus. Combined with the new STEP 2.5 all-in branch, the v==stack case is now resolved before legality (v=stack always admits as clean_all_in).
- [x] **7.1.3 Preflop facing-open:** `to_call_bb` and `hero_already_committed_bb` are computed/derived per §3.1; verified against `4WF-CLOSING--212` (BB defend: to_call=1.5, hero_committed=1.0, previous_full_bet=2.5, min_raise=5.0).

### 7.2 Deep-stack handling

- [x] Current corpus uniformly `stack_size_bb=100`. Normalizer correct in this regime.
- [x] Future 200bb axis: STEP 2.5 all-in branch keys off `v == stack_size_bb`, so v=100 at stack=200 falls through to canonical-set tie-break (correct — v=100 at deep stack is pot-sized raise, not all-in). Verified by inspection.

### 7.3 All-in handling (REVISED v2 per F-1)

- [x] **STEP 2.5 (new):** if `v == stack_size_bb`, `predicted_raise_to_bb = v`, `status = "clean_all_in"`, SKIP downstream tie-break.
- [x] This is the orchestrator's intended interpretation per RATIFICATION §7.3 (unchanged from v1 ratification text). The v1 algorithm contradicted it because the canonical-set branches fired before any all-in check.
- [x] If labeller writes v > stack_size_bb, STEP 2.5 does not fire (inequality); all candidates fail STEP 3 legality; spot is `malformed_rejected`.

### 7.4 3-bet/4-bet pot disambiguation

- [x] 3-bet pot: `to_call_bb` is read directly from spot context; `hero_committed_bb` is 0 if hero hasn't acted preflop (i.e., facing the 3-bet for the first time), else equals hero's prior raise size. For the corpus today, this matters only at `4WF-4-WAY-3--*` 3-bet-pot flop spots (where preflop is settled and we're postflop, so `hero_committed_bb = 0` and `previous_full_bet = to_call_bb`).
- [x] 4-bet pot HU: same logic. Sanity-check on `4WF-4-WAY-3--009` (to_call=15 after 3-bet to 9 then 4-bet to 24, postflop): `previous_full_bet=15.0`, `min_raise_to_bb=30.0`. Matches v1 expectation.

### 7.5 Malformed-label rate prediction (UPDATED per F-2 and F-3)

Based on direct corpus inspection. The F-2 fix changes the predicted disposition for the 19 BB-defend spots (v=5 was already passing under both old and new rules in batch_001-007; but the new rule REJECTS values v=4 or below, which is more conservative — none observed in corpus).

| v | RAISE label count | Predicted disposition (v2) | Change vs v1 |
|---|---:|---|---|
| 9 | 119 | clean (bb only legal) | — |
| 75 | 62 | ambiguous_resolved (pct branch) | — |
| 22 | 28 | clean (bb only legal at typical pot=36.5) | — |
| 300 | ~15 | ambiguous_resolved (mult branch) | — |
| 360 | small | ambiguous_resolved (mult branch) | — |
| 720 | small | ambiguous_resolved (mult branch) | — |
| 30 | small | clean (bb only legal) | — |
| 18 | small | clean (bb only legal) | — |
| 27 | small | clean (bb only legal) | — |
| 25 | small | ambiguous_resolved (pct, since 25 ∈ CANONICAL_PCT only) | — |
| **66** | **13** | **ambiguous_resolved (pct branch; raise-to ≈ 11–12bb at typical pot=13.5)** | **NEW per F-3** |
| **100** | **1** (4WF-MULTIWAY-171) | **clean_all_in (STEP 2.5)** | **CHANGED per F-1: was ambiguous_resolved/16, now clean_all_in/100** |
| 270 | 1 (4WF-4-WAY-3--019) | ambiguous_resolved (pct branch; mult missed; absorbed by owner-arb if owner reviews) | F-4 acknowledged; not fixed |
| 10 | small | clean (bb only legal) | — |

**Predicted post-normalization state (v2):** ~98% clean+clean_all_in+ambiguous_resolved, ~2% malformed_rejected. Owner-arb queue: ~10–15 spots total across batches 001–008 (F-1 fix REMOVES one previously-mis-resolved spot; F-2 fix does not change disposition for the 19 BB-defend spots because they all wrote v=5 which is now correctly above min-raise; net effect: malformed rate slightly LOWER than v1's prediction of 12–18, because the algorithm is now more correct — fewer spots silently mis-resolve).

- [x] Owner+orchestrator accept the predicted rate.

### 7.6 Cross-stream sanity (unchanged from v1)

- [x] Branch base verification per `feedback_orchestrator_branch_base_verification.md`.
- [x] Attention-vocab flag per `feedback_attention_flags_when_features_change.md` — deferred to A0.3 (no v9-4way trainer yet).
- [x] Three-way alignment per `feedback_three_way_alignment_after_gap.md`.
- [x] Pre-merge QC on each of A0.1, A0.2, A0.3 per `feedback_qc_required_before_approval.md`.
- [x] TC-23 drift audit per `feedback_spec_vs_infrastructure_code_drift.md` post-A0.1.

### 7.7 Sign-off

- [ ] Architect: v2 blueprint commits to single design throughout; F-1, F-2, F-6 addressed; F-3, F-7 absorbed inline; F-4, F-5, F-8, F-9, F-10, N-1, N-2, N-3 deferred or absorbed per "Changes from v1."
- [ ] Orchestrator: re-ratifies v2 with sequencing override (unchanged) still applying.
- [ ] Owner: notified of v2; reserves override on the F-2 min-raise formula choice (`2 × previous_full_bet`) or the F-6 sizing-consensus tie-break rules.

---

## Rabbit-holes deliberately avoided

**RH-1 (min-raise convention) — RESOLVED in v2:** The v2 spec commits to `min_raise_to_bb = 2 × previous_full_bet` with `previous_full_bet = to_call_bb + hero_already_committed_bb`. This is the NL-standard rule for the cases in the corpus today (preflop opens, postflop bets, and 3-bet/4-bet pots). Builder-time engine harmonization is NOT required because `poker_game.py` is permissive (verified §7.1.1). Engine is downstream; spec is authoritative.

**RH-2 (v9-4way trainer feature vocab):** Unchanged from v1. Trainer doesn't exist yet; A0.3 ratification catches if one lands in parallel.

**RH-3 (rename single field instead of split):** Unchanged — rejected.

**RH-4 (legacy `predicted_sizing_pct` in v2 files):** Unchanged — removed; preserved in audit logs only.

**RH-5 (consensus-merge code change) — REVISED in v2:** The original v1 RH-5 dismissed this as "no code change required beyond field-name plumbing." QC verified this was wrong (existing consensus.jsonl has NO sizing field; sizing-consensus is a NEW computation). v2 §3.6 specifies the algorithm; RH-5 is RETIRED.

**RH-6 (NEW — F-4 brittleness on adjacent multiplier values like v=270):** v=270 is a single spot in the corpus (4WF-4-WAY-3--019). The v2 algorithm resolves it as `ambiguous_resolved` via the pct branch (raise-to=71). The labeller may have meant 300 with a typo; owner-arb queue absorbs the residue. Architect commits NOT to expand CANONICAL_MULT in v2 — the marginal cost (more "ambiguous_resolved" labels with unclear semantics) outweighs the marginal benefit (one corrected spot). Re-open in v3 if more adjacent-multiplier corpus values appear in future axes.

**RH-7 (NEW — F-5 `stack_size_bb` semantics: starting vs effective):** Corpus today is uniformly 100bb starting and the difference between starting and effective stack at decision is small (≤ 2.5bb for the open-only spots). The F-1 fix structurally handles the v==stack boundary case via STEP 2.5; for non-boundary cases, the difference falls well within the legality interval and does not affect normalizer output for any observed corpus value. Re-open when 200bb deep-stack axis lands.

---

## Appendix A — File manifest (for builder)

```
river-rats-core/sizing_schema_normalizer.py                                       (new, PR A0.1)
river-rats-core/tests/test_sizing_schema_normalizer.py                            (new, PR A0.1; 15 tests)
data/4way_corpus/full_700/batch_{001..007}_raw_labels_labeller_{1..5}_v2.jsonl    (new, PR A0.2)
data/4way_corpus/full_700/batch_{001..007}_raw_labels_opus_tierup_v2.jsonl        (new, PR A0.2)
data/4way_corpus/full_700/batch_{001..007}_consensus_v2.jsonl                     (new, PR A0.2; with §3.6 sizing-consensus)
data/4way_corpus/full_700/batch_{001..007}_normalizer_audit.jsonl                 (new, PR A0.2)
data/4way_corpus/full_700/batch_{001..007}_owner_arb_queue_normalizer.jsonl       (new, PR A0.2; may be empty)
data/4way_corpus/full_700/batch_008_raw_labels_labeller_{1..5}_v2.jsonl           (new, PR A0.3)
data/4way_corpus/full_700/batch_008_consensus_v2.jsonl                            (new, PR A0.3)
data/4way_corpus/full_700/batch_008_normalizer_audit.jsonl                        (new, PR A0.3)
data/4way_labeller_brief.md                                                       (edit, PR A0.3 FINAL commit)
```

## Appendix B — Memory rules cited (binding constraints)

Unchanged from v1:
- `feedback_orchestrator_decides_not_recommends.md` — single design throughout.
- `feedback_solver_aligned_sizing.md` — BET enum + §3.6 sizing-consensus tie-break for BET prefers street-solver-aligned values.
- `feedback_terminology_raise_vs_bet.md` — raise=raise-of-existing-bet; raise-TO semantics; v2's NL-standard min-raise rule honours this terminology (v1's `to_call×2` did not).
- `feedback_attention_flags_when_features_change.md` — deferred to A0.3.
- `feedback_bucket_first_labelling.md` — orthogonal.
- `feedback_failure_direction_classification.md` — separate sizing columns.
- `feedback_qc_required_before_approval.md` — pre-merge QC on all 3 PRs.
- `feedback_spec_vs_infrastructure_code_drift.md` (TC-23) — drift audit post-A0.1.
- `feedback_three_way_alignment_after_gap.md` — pre-dispatch alignment.
- `feedback_orchestrator_branch_base_verification.md` — branch lineage.
- `feedback_no_deadlines.md` — quality batch-008 path.
- `feedback_solver_verification_queue.md` — owner-arb cadence.

---

**END OF BLUEPRINT v2.** Awaiting orchestrator re-ratification.
