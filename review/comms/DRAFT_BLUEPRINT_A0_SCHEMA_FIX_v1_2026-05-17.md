# DRAFT BLUEPRINT — A0 Schema Fix: `predicted_sizing_pct` Dual-Semantics Repair (v1)

**Date:** 2026-05-17
**Author:** Architect (orchestrator-authorized; single-design commit)
**Status:** DRAFT — awaiting orchestrator ratification before builder dispatch
**Scope:** Forward-looking schema split + backfill for 4-way corpus batches 001–008 (350 + partial-008 labels).
**Authority:** Per `feedback_orchestrator_decides_not_recommends.md`, this blueprint commits to a SINGLE DESIGN throughout. No menus. Owner can override any commitment; otherwise the design ships as written.

---

## Problem statement (one paragraph)

The 4-way labeller brief declares `predicted_sizing_pct` as an integer field with TWO different semantics keyed off `predicted_action`:
- For `BET`: integer **% of pot**
- For `RAISE`: integer **bb amount** (raise-to)

Direct inspection of `data/4way_corpus/full_700/` confirms labellers do not consistently honour the dual-semantic contract. Of 282 RAISE labels: 119 use the bb-amount convention (value=9), 62 use a pct-of-pot value (value=75), 21 use a multiplier-of-facing-bet (value=300, 360, 720), 28 sit at ambiguous value=22. BET labels (574) are clean: all at 25/33/66/75. The dual semantics — and the field NAME `_pct` actively misleading for the RAISE branch — caused the drift.

The bug is **schema-level**, not labeller-level. Renaming the field will not help; we must SPLIT it. No 4-way export code or model artifact has shipped yet — this is a forward-looking fix with no model rollback risk. Batches 001–007 (350 hands × 5 labellers + opus tier-up) and partial batch-008 (~135 labels in flight) require deterministic backfill via normalizer.

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

- `predicted_bet_pct ∈ {25, 33, 50, 66, 75, 100, 150}` — solver-aligned per `feedback_solver_aligned_sizing.md` (flop 25/66; turn 33/75; river 33/75/150). 50 and 100 included as adjacent legal values that occasionally appear in clean BET data (over-call protection on connected boards).
- `predicted_raise_to_bb ∈ [⌈min_raise_bb⌉, ⌊effective_stack_bb⌋]` where `min_raise_bb` and `effective_stack_bb` are computed from the input row's `pot_bb`, `to_call_bb`, and `stack_size_bb`. Values outside this interval are illegal.

### 1.4 Validation rules (REJECT on violation)

A label is REJECTED at consensus-merge if any of these hold:

1. `predicted_action == BET` and (`predicted_bet_pct is None` or `predicted_raise_to_bb is not None`)
2. `predicted_action == RAISE` and (`predicted_raise_to_bb is None` or `predicted_bet_pct is not None`)
3. `predicted_action ∈ {FOLD, CHECK, CALL}` and (`predicted_bet_pct is not None` or `predicted_raise_to_bb is not None`)
4. `predicted_bet_pct ∉ {25, 33, 50, 66, 75, 100, 150}` (when non-null)
5. `predicted_raise_to_bb < min_raise_bb` OR `predicted_raise_to_bb > effective_stack_bb` (illegal sizing)
6. `predicted_action == BET` and `facing_bet > 0` (FL5 — illegal action; pre-existing rule)
7. `predicted_action == RAISE` and `facing_bet == 0` (FL5 — illegal action; pre-existing rule)

Rule violations 1–5 introduce a new failure class **FL7: sizing-field mismatch** (see §2.2). Rules 6–7 stay in FL5.

---

## §2 — BRIEF UPDATE (`data/4way_labeller_brief.md`)

### 2.1 Lines 31–34 replacement (diff)

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
+**Why two fields**: BET sizes are naturally expressed as % of pot (solver convention). RAISE sizes are naturally expressed as bb-total raise-TO (because raise-by/raise-to confusion + % of pot ambiguity in multiway is unrecoverable). Do not write a % in `predicted_raise_to_bb` — that is field-mismatch FL7 (see §2.2 of this brief), and your label is REJECTED at consensus.
```

### 2.2 New failure-class entry (insert after FL5 paragraph, ~line 37)

```diff
+**FL7 failure class — sizing-field mismatch**: writing a % value in `predicted_raise_to_bb` (e.g., 75, 300, 360) or a bb value in `predicted_bet_pct` (e.g., 9, 18) is a labelling defect. Specifically:
+- Writing `predicted_raise_to_bb: 75` because you meant "75% of pot" → REJECT. Convert to a raise-to bb value BEFORE writing the label.
+- Writing `predicted_raise_to_bb: 300` because you meant "300% of facing bet" → REJECT. Compute the resulting raise-to and write that integer.
+- Writing `predicted_bet_pct: 9` because you meant "9bb" → REJECT. BET uses % of pot only.
+
+If you cannot compute the raise-to in bb (rare), use `confidence: LOW` and write the value you intended in the reasoning prose; orchestrator owner-arb queue will adjudicate. Do NOT write a malformed value.
```

### 2.3 Output schema replacement (lines 173–187)

```diff
 Per spot to `data/4way_corpus/raw_labels_labeller_<N>.jsonl`:

 ```json
 {
   "spot_id": "4WL-<axis>-<N>",
   "labeller_id": <N>,
   "predicted_action": "FOLD|CHECK|CALL|BET|RAISE",
-  "predicted_sizing_pct": <int or null>,
+  "predicted_bet_pct": <int or null>,
+  "predicted_raise_to_bb": <int or null>,
   "confidence": "HIGH|MEDIUM|LOW",
   "bucket": "<spot-type classification>",
   "reasoning": "<250-400 word per-hand reasoning chain>",
   "num_opponents_at_decision": 3,
   "primary_axis": "<axis label>"
 }
 ```

-Include `predicted_sizing_pct` ONLY for BET or RAISE actions.
+Set `predicted_bet_pct` ONLY for BET; set `predicted_raise_to_bb` ONLY for RAISE; set both to `null` for FOLD/CHECK/CALL. Exactly one is non-null when action is aggressive. Never both.
```

### 2.4 Solver-aligned sizing section (lines 105–112) — clarifying replacement

```diff
 When you label a BET or RAISE action, use solver-aligned sizes:
-- **Flop**: 25% (small c-bet) or 66% (polarized; usually for value+protection on wet boards)
-- **Turn**: 33% (small) or 75% (polarized)
-- **River**: 33% / 75% / 150% (over-bet for polar value/bluff)
+- **BET sizing (% of pot, into `predicted_bet_pct`)**:
+  - Flop: 25 or 66
+  - Turn: 33 or 75
+  - River: 33 / 75 / 150
+- **RAISE sizing (bb raise-TO, into `predicted_raise_to_bb`)**:
+  - vs flop bet: 3.0–4.0× the bet size, converted to total raise-to bb.
+  - vs turn bet: 2.5–3.0× the bet size.
+  - vs river bet: 2.5–3.5× the bet size.
+  - Example: facing a 2.5bb c-bet into 12.5bb, a 3.5× raise = 8.75bb raise-by ⇒ raise-TO ≈ 11.25bb; round to 11. Or if your read is "min-raise with set," use min-raise to bb (e.g., to 5bb).

-Raises (raise-of-bet): 3-4x the bet size on flop; 2.5-3x on turn; 2.5-3.5x on river.
+The `predicted_raise_to_bb` value must be the FINAL chip count put in by hero (raise-to), not the increment. Per `feedback_terminology_raise_vs_bet.md`: a raise is a raise of an existing bet; the raise-to is the cumulative bet level.
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
NormalizationStatus = Literal["clean", "ambiguous_resolved", "malformed_rejected", "no_op"]

@dataclass(frozen=True)
class SpotContext:
    """Subset of fields from batch_NNN_50hand.jsonl needed for legality checks."""
    pot_bb: float          # pot size at decision
    to_call_bb: float      # amount needed to call (0 if facing_bet == 0)
    facing_bet: int        # 0 or 1
    stack_size_bb: float   # effective stack (hero) at decision
    street: str            # "preflop" | "flop" | "turn" | "river"

@dataclass(frozen=True)
class NormalizedSizing:
    predicted_bet_pct: int | None
    predicted_raise_to_bb: int | None
    status: NormalizationStatus
    rationale: str         # human-readable; written to audit log

def normalize_sizing(
    action: Action,
    legacy_sizing_pct: int | None,
    ctx: SpotContext,
) -> NormalizedSizing:
    """
    Convert a legacy `predicted_sizing_pct` value into the new field schema.

    Behaviour:
    - FOLD/CHECK/CALL with non-null legacy value: WARN (legacy schema bug),
      output both fields = None, status="clean".
    - BET with legacy value v: predicted_bet_pct = v (BET semantics are clean).
    - RAISE: dual-interpretation legality check (see §3.2).
    """
    ...

def run_batch(input_path: str, output_path: str, context_path: str) -> dict:
    """
    Read `*_raw_labels_labeller_N.jsonl` + matching `*_50hand.jsonl` context,
    emit `*_raw_labels_labeller_N_v2.jsonl` with normalized fields,
    plus `*_normalizer_audit.jsonl` with per-label status + rationale.
    Returns: {clean: int, ambiguous_resolved: int, malformed_rejected: int}.
    """
    ...
```

### 3.2 RAISE normalization algorithm (commit to ONE approach)

For each RAISE label with `legacy_sizing_pct = v`:

```
STEP 1: Compute pot context.
  facing_bet_bb = ctx.to_call_bb              # the bet hero is facing, in bb
  min_raise_to_bb = ctx.to_call_bb * 2        # min-raise = double the bet
  max_raise_to_bb = ctx.stack_size_bb         # all-in cap

STEP 2: Compute the two candidate interpretations.
  candidate_bb  = v                                              # interpret as raise-to bb
  candidate_pct_to_bb = round(facing_bet_bb + (v / 100.0) * ctx.pot_bb)
                                                                 # interpret v as "% of pot raise-BY", convert to raise-to
                                                                 # i.e., raise-by = v% of pot; raise-to = facing_bet + raise-by
  candidate_mult_to_bb = round((v / 100.0) * facing_bet_bb)
                                                                 # interpret v as "% multiplier of facing bet"
                                                                 # used ONLY when v ∈ {300, 360, 720} (canonical multiplier tells)

STEP 3: Legality filter (each candidate must satisfy min_raise ≤ X ≤ max_raise).
  legal_bb   = min_raise_to_bb <= candidate_bb   <= max_raise_to_bb
  legal_pct  = min_raise_to_bb <= candidate_pct_to_bb <= max_raise_to_bb
  legal_mult = min_raise_to_bb <= candidate_mult_to_bb <= max_raise_to_bb

STEP 4: Tie-break (commit: canonical-value table).
  CANONICAL_BB  = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 18, 22, 27, 30}   # plausible raise-to amounts
  CANONICAL_PCT = {25, 33, 50, 66, 75, 100, 150}                          # canonical pct-of-pot sizes (used as raise-by%)
  CANONICAL_MULT = {300, 360, 720}                                        # canonical multiplier-of-bet values seen in corpus

  # Multiplier interpretation takes priority for explicit multiplier tells:
  if v in CANONICAL_MULT and legal_mult:
      → predicted_raise_to_bb = candidate_mult_to_bb
      status = "ambiguous_resolved"

  # Pure bb interpretation (most common path):
  elif v in CANONICAL_BB and legal_bb and not (v in CANONICAL_PCT and legal_pct):
      → predicted_raise_to_bb = candidate_bb
      status = "clean"

  # Pure pct interpretation:
  elif v in CANONICAL_PCT and legal_pct and not (v in CANONICAL_BB and legal_bb):
      → predicted_raise_to_bb = candidate_pct_to_bb
      status = "ambiguous_resolved"

  # Both legal AND in both canonical sets (e.g., v=22 with both legal):
  elif legal_bb and legal_pct:
      # Tie-break rule (binding): prefer bb interpretation, because the original brief
      # said "integer bb amount for RAISE" — that is the brief-intent. Labellers who
      # wrote pct values violated the brief; we honour brief-intent on ties.
      → predicted_raise_to_bb = candidate_bb
      status = "ambiguous_resolved"

  # Only one legal:
  elif legal_bb and not legal_pct:
      → predicted_raise_to_bb = candidate_bb
      status = "clean"
  elif legal_pct and not legal_bb:
      → predicted_raise_to_bb = candidate_pct_to_bb
      status = "ambiguous_resolved"

  # Neither legal:
  else:
      → predicted_raise_to_bb = None
      status = "malformed_rejected"
      # Spot is routed to batch_NNN_owner_arb_queue_normalizer.jsonl

  predicted_bet_pct = None  # always None for RAISE
```

The canonical-set tie-break is preferred over a numeric threshold (`v ≤ 10 → bb`, `v ≥ 25 → pct`) because the actual corpus distribution sits at discrete values (9, 22, 75, 300, 360, 720) — a value-table lookup is more transparent than a hand-tuned cutoff and aligns with the discrete canonical sizing taxonomy that the brief teaches.

### 3.3 BET normalization (trivial)

For each BET label with `legacy_sizing_pct = v`:
- `predicted_bet_pct = v`
- `predicted_raise_to_bb = None`
- `status = "clean"` if `v ∈ {25, 33, 50, 66, 75, 100, 150}`, else `"malformed_rejected"`

The empirical inspection (orchestrator-verified) shows BET labels are 100% clean — this branch should never reject in practice but the guard exists to catch future drift.

### 3.4 Three worked examples

**Example A — clean bb interpretation** (`v = 9`, RAISE)

Input row (representative of `4WF-CLOSING--306`):
- `pot_bb = 12.5`, `to_call_bb = 2.5`, `facing_bet = 1`, `stack_size_bb = 97.5`
- Label: `predicted_action = RAISE`, `legacy_sizing_pct = 9`

```
min_raise_to_bb  = 2.5 * 2 = 5.0
max_raise_to_bb  = 97.5
candidate_bb     = 9                                  ✓ legal (5 ≤ 9 ≤ 97.5)
candidate_pct_to_bb = round(2.5 + 0.09 * 12.5) = round(3.625) = 4
                                                       ✗ illegal (4 < 5)
candidate_mult_to_bb = round(0.09 * 2.5) = 0          ✗ illegal
Result: legal_bb only → predicted_raise_to_bb = 9, status = "clean"
```

**Example B — pct interpretation** (`v = 75`, RAISE)

Input row (hypothetical raise-of-cbet on flop):
- `pot_bb = 36.5`, `to_call_bb = 9.0`, `facing_bet = 1`, `stack_size_bb = 91.0`
- Label: `predicted_action = RAISE`, `legacy_sizing_pct = 75`

```
min_raise_to_bb  = 9.0 * 2 = 18.0
max_raise_to_bb  = 91.0
candidate_bb     = 75                                 ✓ legal (18 ≤ 75 ≤ 91)
candidate_pct_to_bb = round(9.0 + 0.75 * 36.5) = round(36.375) = 36
                                                       ✓ legal (18 ≤ 36 ≤ 91)
candidate_mult_to_bb = round(0.75 * 9.0) = 7          ✗ illegal (7 < 18)
Both bb and pct legal; v=75 ∈ CANONICAL_PCT AND v=75 ∉ CANONICAL_BB
→ pure pct branch: predicted_raise_to_bb = 36, status = "ambiguous_resolved"
```

Audit-log rationale: `"v=75 ∈ CANONICAL_PCT={25,33,50,66,75,100,150}; bb interpretation legal but value 75 is not in CANONICAL_BB; resolved as pct-of-pot raise-by → raise-to=36bb"`

**Example C — tie-break case** (`v = 22`, RAISE)

Input row (3-bet-pot flop raise):
- `pot_bb = 36.5`, `to_call_bb = 9.0`, `facing_bet = 1`, `stack_size_bb = 91.0`
- Label: `predicted_action = RAISE`, `legacy_sizing_pct = 22`

```
min_raise_to_bb  = 18.0
max_raise_to_bb  = 91.0
candidate_bb     = 22                                 ✓ legal (18 ≤ 22 ≤ 91)
candidate_pct_to_bb = round(9.0 + 0.22 * 36.5) = round(17.03) = 17
                                                       ✗ illegal (17 < 18) — by 1bb margin
candidate_mult_to_bb = round(0.22 * 9.0) = 2          ✗ illegal
Only legal_bb → predicted_raise_to_bb = 22, status = "clean"
```

Note: this is the non-tie path because pct interpretation falls just outside legality. If the spot had `pot_bb = 45` instead, both would be legal, and the tie-break rule (prefer bb because brief-intent was bb) would apply: `predicted_raise_to_bb = 22`.

### 3.5 Test coverage (mandatory before normalizer ships)

Unit tests in `river-rats-core/tests/test_sizing_schema_normalizer.py`:

1. **test_check_call_fold_legacy_value_warned** — non-null `legacy_sizing_pct` on FOLD/CHECK/CALL emits warning, normalizes to null/null.
2. **test_bet_clean_value** — BET v=66 → `predicted_bet_pct=66`, `predicted_raise_to_bb=None`, status=clean.
3. **test_bet_off_solver_value** — BET v=40 → status=`malformed_rejected` (40 ∉ allowed set).
4. **test_raise_clean_bb_canonical** — Example A (v=9, pot=12.5).
5. **test_raise_pct_canonical** — Example B (v=75, pot=36.5).
6. **test_raise_tiebreak_both_legal_prefers_bb** — v=22 with pot=45 (both interpretations legal); resolves to bb.
7. **test_raise_multiplier_720** — preflop squeeze with v=720, to_call=2.5, expect raise-to=18bb.
8. **test_raise_multiplier_300_4bet** — v=300, to_call=9, expect raise-to=27bb.
9. **test_raise_neither_legal_malformed** — v=2 facing 9bb (below min-raise) → `malformed_rejected`.
10. **test_raise_above_stack_malformed** — v=200 with stack=100 → `malformed_rejected`.
11. **test_round_trip_idempotence** — normalizer applied to already-normalized v2 file is a no-op.
12. **test_consensus_alignment** — five labellers' divergent legacy values for one spot all normalize to same `predicted_raise_to_bb` when consensus action is RAISE (regression test for batch consistency).

Acceptance criterion: all 12 tests pass; coverage ≥ 95% lines.

---

## §4 — IN-FLIGHT BATCH-008 STRATEGY

**Commit: RESUME under old brief; normalize post-hoc.**

Rationale:
- L1 = 50/50 (complete), L2 = 36/50, L3 = 11/50, L4 = 10/50, L5 = 25/50 → 132 labels already produced under old brief. Restarting wastes that work.
- The normalizer is the same code path that handles batches 001–007 — running it on batch-008 adds zero incremental complexity.
- Labellers 2–5 already have warm-state context; restarting forces a fresh briefing cycle that interrupts the production cadence (per `feedback_no_deadlines.md`, we don't truncate quality, but we also don't manufacture re-onboarding overhead with no benefit).
- The new brief is forward-looking; batch-009 onwards uses the split schema natively. The cutover is clean: batches 001–008 = legacy schema + normalizer; batches 009+ = native split schema + zero normalization.

**Decision boundary**: If batch-008 produces a malformed-rejected rate > 10% during post-hoc normalization, that is a signal that the brief change was urgent enough to have warranted a restart — orchestrator+owner reviews and decides whether to invalidate batch-008. The expected rate (extrapolating from batches 001–007: 21 malformed out of 282 RAISE labels = 7.4%) is below the boundary.

---

## §5 — EXPORT SCHEMA for v9-4way training

### 5.1 Training CSV columns

The v9-4way training export (consumed by `river-rats-core/train_model.py`) takes consensus labels and produces a flat CSV with these columns:

| Column | Type | Domain | Populated when |
|---|---|---|---|
| `action` | categorical | FOLD/CHECK/CALL/BET/RAISE | always |
| `bet_pct` | float | {25, 33, 50, 66, 75, 100, 150} or NaN | iff action=BET |
| `raise_to_bb_normalized` | float | (0, ∞) or NaN | iff action=RAISE |
| `raise_to_bb_raw` | float | (0, 200] or NaN | iff action=RAISE (audit column; not used as training feature) |

### 5.2 Normalization basis for `raise_to_bb_normalized` (commit: divide by `pot_bb`)

`raise_to_bb_normalized = predicted_raise_to_bb / pot_bb`

**Rationale**: dividing by `pot_bb` produces a unitless ratio scale-invariant under pot growth across streets. The alternative — dividing by `to_call_bb` — would make the model see "raise size as multiplier of facing bet," which is closer to "raise-by ratio." Both encode the same information, but pot-normalization aligns with how `bet_pct` is already encoded for BET (% of pot), keeping the model's view of sizing on a single consistent axis: "fraction of pot committed by this action."

Edge case: when `pot_bb < 1`, normalization is undefined; guard with `pot_bb = max(pot_bb, 0.5)` before division. (Empirically, all 4-way corpus rows have `pot_bb ≥ 7.0` — preflop limped pots — so the guard is precautionary only.)

### 5.3 BET vs RAISE feature symmetry

Both `bet_pct` and `raise_to_bb_normalized * 100` express sizing as "% of pot." A future model variant can collapse to a single sizing column with an action-conditioned interpretation; current design keeps them separate for diagnostic transparency in failure-direction classification (per `feedback_failure_direction_classification.md` — we need to distinguish "model under-aggresses on BET sizing" from "model under-aggresses on RAISE sizing" at trainer-report time).

---

## §6 — ROLLOUT SEQUENCE

Three PRs in strict sequence. Each has acceptance tests; failing tests block the next PR.

### PR A0.1 — Schema + normalizer (foundation)

**Files added**:
- `river-rats-core/sizing_schema_normalizer.py` (~300 lines)
- `river-rats-core/tests/test_sizing_schema_normalizer.py` (12 tests per §3.5)
- `data/4way_labeller_brief.md` (lines 31–34, 105–112, 173–187 patched per §2)

**Acceptance tests**:
- All 12 normalizer unit tests pass.
- `python -m river_rats_core.sizing_schema_normalizer --dry-run data/4way_corpus/full_700/batch_001_raw_labels_labeller_1.jsonl` produces a normalized output with zero unhandled exceptions and a printed summary `{clean: N, ambiguous_resolved: M, malformed_rejected: K}`.
- Brief change diff matches §2 verbatim (reviewer reads brief side-by-side).

**No corpus mutation** in this PR — code only.

### PR A0.2 — Backfill batches 001–007

**Files added**:
- `data/4way_corpus/full_700/batch_NNN_raw_labels_labeller_M_v2.jsonl` (35 files: 7 batches × 5 labellers)
- `data/4way_corpus/full_700/batch_NNN_raw_labels_opus_tierup_v2.jsonl` (7 files)
- `data/4way_corpus/full_700/batch_NNN_consensus_v2.jsonl` (7 files — re-computed consensus on v2 labels)
- `data/4way_corpus/full_700/batch_NNN_normalizer_audit.jsonl` (7 files — per-label status + rationale)
- `data/4way_corpus/full_700/batch_NNN_owner_arb_queue_normalizer.jsonl` (7 files; may be empty)

**Acceptance tests**:
- For every (batch, labeller, spot), the v2 file has same `spot_id` set as v1.
- For every BET label in v1, v2 has matching `predicted_bet_pct` and null `predicted_raise_to_bb`.
- For every RAISE label classified `status=clean` in audit, v2 has same numeric value in `predicted_raise_to_bb` as v1 had in `predicted_sizing_pct`.
- For every RAISE label classified `status=malformed_rejected`, that spot appears in `owner_arb_queue_normalizer.jsonl` and is excluded from `consensus_v2.jsonl`.
- Per-batch malformed-rejected rate is reported; if any batch exceeds 15%, PR is BLOCKED pending architect+orchestrator review (the normalizer or the brief expectation is wrong).
- v2 consensus action distribution is checked against v1 consensus action distribution; sizing-driven action changes (which should not happen — the normalizer touches sizing only, never action) trigger a hard fail.

### PR A0.3 — Batch-008 resume + normalize

**Files**:
- Labellers 2–5 complete batch-008 under OLD brief (no field schema change for them in-flight; they keep writing `predicted_sizing_pct`).
- After all 5 labellers complete, run normalizer (same as PR A0.2 process) → produce `batch_008_consensus_v2.jsonl`.
- Brief change (§2) takes effect for batch-009 onward; labellers receive updated brief at start of batch-009.

**Acceptance tests**:
- Batch-008 v2 consensus produced with same gate as batches 001–007.
- Batch-009 first 5 labels (mini-pilot) use new schema natively; normalizer is no-op on those (status=clean for all 5 labels of all 5 labellers = 25/25 clean).
- Brief-comprehension check: each labeller's first batch-009 label has correctly null-vs-non-null field combos per §1.4 validation rules. Any violation in the first 5 labels triggers a labeller-side re-briefing.

---

## §7 — RATIFICATION CHECKLIST

The orchestrator runs through this checklist BEFORE dispatching to the builder. Each item must be unambiguously YES; any NO routes back to architect for revision.

### 7.1 Legality-check edge cases

- [ ] Min-raise rule: `min_raise_to_bb = to_call_bb * 2` is correct for the engine's raise convention. (Verify against `river-rats-core/poker_game.py` — see Rabbit-Hole-1 below.)
- [ ] All-in cap: `max_raise_to_bb = stack_size_bb` correctly caps at hero's effective stack, not at full stack (relevant in deep-stack 200bb scenarios — see 7.2).
- [ ] Preflop facing-open: when `facing_bet=1` and `street=preflop`, `to_call_bb` is the OPEN size minus blinds already posted (e.g., facing a 2.5bb open from SB-posted-0.5 → to_call=2.0). Normalizer must read `to_call_bb` directly from the `*_50hand.jsonl` context, not recompute it.

### 7.2 Deep-stack handling

- [ ] All current 4-way corpus spots have `stack_size_bb = 100`. Normalizer is correct in this regime.
- [ ] If a future axis adds deep-stack 200bb spots, the `max_raise_to_bb = stack_size_bb` rule scales naturally. Confirmed by inspection of the algorithm: no hard-coded 100bb constant.

### 7.3 All-in handling

- [ ] If a labeller writes `legacy_sizing_pct` equal to `stack_size_bb` (e.g., 100 in a 100bb stack), normalizer interprets as all-in raise-to. This is at the boundary `legal_bb` and admits.
- [ ] If a labeller writes a value exceeding `stack_size_bb`, all candidates fail legality and the spot is malformed-rejected → owner-arb queue.

### 7.4 3-bet pot disambiguation

- [ ] In a 3-bet pot, `to_call_bb` reflects the 3-bet size minus hero's prior contribution, not the raw 3-bet number. Normalizer's legality check is robust because it uses `to_call_bb` directly from the spot context — no inference required.
- [ ] In a 4-bet pot, same rule applies. Sanity-checked against `4WF-4-WAY-3--009` (4-bet pot HU, to_call_bb=15 after 3-bet to 9 then 4-bet to 24) and the candidate algorithm produces correct min-raise=30.

### 7.5 Malformed-label rate prediction

Based on direct corpus inspection (orchestrator-verified):
- BET labels: 574/574 expected clean (= 100%, status=clean).
- RAISE labels: 282 total breakdown:
  - 119 (v=9): expected clean, bb interpretation.
  - 62 (v=75): expected ambiguous_resolved, pct interpretation.
  - 21 (v=300 and similar): expected ambiguous_resolved, multiplier interpretation if value ∈ CANONICAL_MULT and legal_mult; otherwise pct interpretation.
  - 28 (v=22): expected clean, bb interpretation (only legal candidate per Example C analysis).
  - Remaining 52: expected mix; ~5–8 likely malformed-rejected (e.g., values like 360 in spots where neither legal — small edge of distribution).

**Predicted post-normalization state**: ~98% clean+ambiguous_resolved, ~2% malformed_rejected. Owner-arb queue receives ~12–18 spots total across batches 001–008 (within capacity for owner adjudication in ~30 minutes per `feedback_solver_verification_queue.md` queue-draining cadence).

- [ ] Owner+orchestrator accept the predicted malformed rate. (If too high, brief intent is contested and §3.2 tie-break needs revisiting.)

### 7.6 Cross-stream sanity

- [ ] Per `feedback_orchestrator_branch_base_verification.md`: PR A0.1 branch is rooted at `origin/master`; A0.2 branch rooted at A0.1; A0.3 rooted at A0.2.
- [ ] Per `feedback_attention_flags_when_features_change.md`: schema split is a feature-vocabulary change; downstream `feature_extractor.py` and any attention vocab in v9-4way trainer config must be updated as part of PR A0.2 or A0.3 (which one — see Rabbit-Hole-2 below). Architect commits this to **A0.3** because no v9-4way trainer exists yet; if one is introduced before A0.3, A0.2 must absorb the change.
- [ ] Per `feedback_three_way_alignment_after_gap.md`: this blueprint follows a long quiet day in the project trajectory; before builder dispatch, orchestrator does a three-way state alignment (master HEAD, comms/, GitHub PRs) to confirm no parallel-stream changes have landed since the audits cited in the problem statement were authored.
- [ ] Per `feedback_qc_required_before_approval.md`: this is a MILESTONE PR sequence (schema migration); QC must audit pre-merge on each of A0.1, A0.2, A0.3.
- [ ] Per `feedback_spec_vs_infrastructure_code_drift.md` (TC-23): post-merge of A0.1, EXISTENCE+CONTENT drift audit confirms brief and normalizer agree on field names and value enumeration.

### 7.7 Sign-off

- [ ] Architect: blueprint commits to single design throughout; no remaining open questions.
- [ ] Orchestrator: ratifies and dispatches to builder via MAIN_TERMINAL directive naming PR A0.1 as first action.
- [ ] Owner: notified of the schema split; reserves override on §3.2 tie-break or §4 batch-008 strategy.

---

## Rabbit-holes deliberately avoided

**RH-1 (min-raise convention)**: poker engines diverge on whether "min-raise" means "double the bet" (No-Limit standard) or "match the previous raise increment" (more correct in re-raise sequences). The blueprint uses the simpler "double the to_call" rule, matching the No-Limit conventional interpretation used in the 4-way corpus reasoning chains. Confirming this matches `river-rats-core/poker_game.py` is a builder-time pre-flight check (ratification item 7.1.1) — NOT an architect-time design question, because the difference only matters for malformed-rate prediction at the margins (~2 spots), not for the schema design.

**RH-2 (when does v9-4way trainer learn the new schema)**: The trainer doesn't exist yet. Defining trainer-side feature-vocabulary integration here would be premature design beyond the schema fix scope. PR A0.3 ratification (item 7.6.2) catches this if a trainer lands in parallel.

**RH-3 (renaming `predicted_sizing_pct` while keeping single field)**: Considered and rejected — the dual-semantics is the bug, not the name. Renaming to `predicted_sizing_value` (type-untagged) keeps the ambiguity; splitting into typed fields with explicit per-action nullability removes it structurally. Per `feedback_orchestrator_decides_not_recommends.md`, this blueprint commits to the split, no menu.

**RH-4 (legacy `predicted_sizing_pct` field carried forward in v2 files)**: NOT carried forward. The v2 file schema is the new schema; the legacy field is removed entirely. The `*_normalizer_audit.jsonl` files preserve the legacy values for forensic traceability if needed.

**RH-5 (consensus-merge logic changes)**: The consensus merger (`river-rats-core/...consensus...`) currently votes on `predicted_action` and reports modal sizing. The schema split does not change the consensus algorithm itself — it just operates on `predicted_bet_pct` and `predicted_raise_to_bb` as two independent modal-vote columns. If consensus action is BET, only `bet_pct` matters; if RAISE, only `raise_to_bb`. No code change required beyond field-name plumbing, which the normalizer's `consensus_v2.jsonl` regeneration handles.

---

## Appendix A — File manifest (for builder)

```
river-rats-core/sizing_schema_normalizer.py       (new, PR A0.1)
river-rats-core/tests/test_sizing_schema_normalizer.py  (new, PR A0.1)
data/4way_labeller_brief.md                       (edit, PR A0.1)
data/4way_corpus/full_700/batch_{001..007}_raw_labels_labeller_{1..5}_v2.jsonl   (new, PR A0.2)
data/4way_corpus/full_700/batch_{001..007}_raw_labels_opus_tierup_v2.jsonl       (new, PR A0.2)
data/4way_corpus/full_700/batch_{001..007}_consensus_v2.jsonl                    (new, PR A0.2)
data/4way_corpus/full_700/batch_{001..007}_normalizer_audit.jsonl                (new, PR A0.2)
data/4way_corpus/full_700/batch_{001..007}_owner_arb_queue_normalizer.jsonl      (new, PR A0.2; may be empty)
data/4way_corpus/full_700/batch_008_raw_labels_labeller_{1..5}_v2.jsonl          (new, PR A0.3)
data/4way_corpus/full_700/batch_008_consensus_v2.jsonl                           (new, PR A0.3)
data/4way_corpus/full_700/batch_008_normalizer_audit.jsonl                       (new, PR A0.3)
```

## Appendix B — Memory rules cited (binding constraints on this blueprint)

- `feedback_orchestrator_decides_not_recommends.md` — committed to single design throughout; no menus.
- `feedback_solver_aligned_sizing.md` — BET sizing enum derives from solver-aligned values.
- `feedback_terminology_raise_vs_bet.md` — RAISE means raise of existing bet; bet means first postflop bet. `predicted_raise_to_bb` semantics use raise-TO not raise-BY.
- `feedback_attention_flags_when_features_change.md` — trainer/attention-vocab change tracking deferred to PR A0.3.
- `feedback_bucket_first_labelling.md` — labelling brief retains bucket-first; sizing fix orthogonal.
- `feedback_failure_direction_classification.md` — separate BET vs RAISE sizing columns enable directional failure analysis.
- `feedback_qc_required_before_approval.md` — milestone sequence requires pre-merge QC on all three PRs.
- `feedback_spec_vs_infrastructure_code_drift.md` (TC-23) — drift audit post-A0.1.
- `feedback_three_way_alignment_after_gap.md` — pre-dispatch alignment.
- `feedback_orchestrator_branch_base_verification.md` — branch lineage verification per PR.
- `feedback_no_deadlines.md` — quality path picked for batch-008 resume strategy; no truncation for cadence.
- `feedback_solver_verification_queue.md` — owner-arb queue cadence respected for malformed-rejected residue.

---

**END OF BLUEPRINT v1.** Awaiting orchestrator ratification.
