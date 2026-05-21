---
date: 2026-05-13
from: Orchestrator (Phase 2-F prep — DRAFT pending architect+owner ratification)
to: Builder · QC · Architect · Owner
re: Drift analyzer v1 — spec for the tool that consumes
    old_consensus / new_consensus / opus_tierup and emits DRIFT_REPORT_*
status: DRAFT — SPEC ONLY (no implementation in this comm)
companion docs:
  - review/comms/DRAFT_SPEC_RELABEL_CONSISTENCY_AUDIT_v1_2026-05-13.md
  - review/comms/DRAFT_PILOT_SAMPLE_20HAND_2026-05-13.jsonl
  - review/comms/DRAFT_FULL_SAMPLE_80HAND_2026-05-13.jsonl
target location for implementation:
  - river-rats-core/drift_analyzer.py
  - river-rats-core/tests/test_drift_analyzer.py
  - (per training-provenance addendum, 2026-04-15)
---

# Drift Analyzer v1 — Specification

## 1. Purpose

The drift analyzer is the computational component of the Phase 2-F re-label
consistency audit (SPEC §5 drift metrics, §6 thresholds, §7 output formats).
It consumes the three audit inputs and emits markdown drift reports plus a
per-hand drift detail JSONL.

This document is a **SPEC** for builder authorship. Builder produces:
- `river-rats-core/drift_analyzer.py` (provenance docstring required)
- `river-rats-core/tests/test_drift_analyzer.py`

The analyzer itself is dispatched separately against pilot/full audit outputs
by the orchestrator; this spec does NOT include implementation.

## 2. Inputs

All inputs are JSONL, one record per spot.

### 2.1 `old_consensus.jsonl`

Sourced from `data/4way_corpus/full_700/batch_NNN_consensus.jsonl` for the
spot_ids in the audit sample. Schema (legacy mixed across batches):

```json
{
  "spot_id": "4WF-4-WAY-3--002",
  "consensus_state": "all-agree",   // batch_001 only
  "state":           "all-agree",   // batch_002..007 legacy key
  "consensus_action": "BET",
  "consensus_sizing_pct": 50.0,     // OPTIONAL — only on BET/RAISE
  "sonnet_votes": ["BET","BET","BET","BET","BET"],
  "opus_vote": null
}
```

Loader MUST resolve either `consensus_state` or `state` (pilot agent's
fallback pattern). If neither present, error.

### 2.2 `new_consensus.jsonl`

From `data/4way_corpus/audit_amendment3/{pilot,full}/consensus.jsonl`
(post-v3.5 + AMENDMENT-3 re-label per audit SPEC §4). Same schema as 2.1
with `consensus_state` as canonical key.

### 2.3 `opus_tierup.jsonl`

From the Opus-Verify pass (audit SPEC §6.1). Schema:

```json
{
  "spot_id": "4WF-4-WAY-3--002",
  "opus_verdict_action": "BET",
  "opus_verdict_sizing_pct": 50.0,    // OPTIONAL on BET/RAISE
  "opus_aligns_with": "new",          // "old" | "new" | "neither"
  "rationale_snippet": "..."
}
```

Only drift hands (`old_action ≠ new_action`) need an Opus record;
agree-hands do NOT require one.

## 3. Outputs

### 3.1 `drift_detail.jsonl` (per-hand)

One record per audit-sample spot (20 pilot / 80 full):

```json
{
  "spot_id": "4WF-4-WAY-3--002",
  "stratification_cell": {
    "hero_position": "BTN", "action_context": "opener",
    "street": "flop", "board_texture": "rainbow_dry"
  },
  "old_action": "BET",
  "old_agreement": "5/5",
  "old_sizing_pct": 50.0,
  "old_sizing_bin": "medium",
  "new_action": "BET",
  "new_agreement": "5/5",
  "new_sizing_pct": 65.0,
  "new_sizing_bin": "large",
  "opus_verdict": "new",          // null if no drift
  "opus_verdict_action": "BET",   // null if no drift
  "drift_class": "agree",         // "agree" | "shift"
  "drift_direction": null,        // null|"under-aggress"|"over-aggress"|"lateral"|"illegal"
  "sizing_drift": true,           // same action, different bin
  "fl6_pass": true                // new rationale passes FL6 chain-naming regex
}
```

### 3.2 `DRIFT_REPORT_PILOT.md` / `DRIFT_REPORT_FULL.md`

Markdown matching audit SPEC §7.1 / §7.2. Schema top-to-bottom:

1. Frontmatter (date, from, to, re, `status: PASS|REVISE-AND-RETRY|HALT`)
2. **TL;DR**: action_drift_rate, net direction, sizing_drift_rate, Opus-rejected count
3. **Per-action 5×5 drift matrix** (§4.3)
4. **Direction classification** counts (under / over / lateral / illegal)
5. **Sizing drift** breakdown (§4.4)
6. **Drift hand details** — one block per shift: spot_id, cell, old action+sizing+rationale, new action+sizing+rationale, Opus verdict
7. **Stratification preservation** chi² + McNemar (§4.6)
8. **Cell-level drift breakdown** (FULL only)
9. **Tail-cell drift coverage** (FULL only)
10. **Top-12 chain coverage** sidebar (FULL only — per audit SPEC §7.2)
11. **Gate decision** checkbox table (§4.7)

## 4. Drift classification logic

### 4.1 `drift_class`

- `agree` ⇔ `old_action == new_action`
- `shift` ⇔ `old_action ≠ new_action`

### 4.2 `drift_direction` (only for shift)

Per `feedback_failure_direction_classification.md`:

| from \ to | FOLD | CALL | CHECK | BET | RAISE |
|---|---|---|---|---|---|
| **FOLD** | (agree) | over-aggress | (illegal) | (illegal) | over-aggress |
| **CALL** | under-aggress | (agree) | (illegal) | over-aggress | over-aggress |
| **CHECK** | (illegal) | (illegal) | (agree) | over-aggress | over-aggress |
| **BET** | (illegal) | (illegal) | under-aggress | (agree) | over-aggress (lateral) |
| **RAISE** | under-aggress | under-aggress | (illegal) | under-aggress (lateral) | (agree) |

Notes:
- `(illegal)` cells should be 0 in practice; non-zero count → WARN
  (likely labeller-output corruption; flagged for owner-arb, §5.5).
- "lateral" within same direction (BET→RAISE, RAISE→BET) is treated as
  the parent direction tag in summary stats but flagged as lateral in
  per-spot detail.
- Audit uses 5-action set {FOLD, CALL, CHECK, BET, RAISE}.

**`class-collapse`** (per memory): when ≥80% of shifts in a single
stratification cell move from a diverse old-action distribution to a
single new action. Detected at report level (§4.6 cell-level breakdown),
not per-spot.

### 4.3 Per-action 5×5 drift matrix

5×5 contingency table over {FOLD, CALL, CHECK, BET, RAISE}:

```
              new=FOLD  new=CALL  new=CHECK  new=BET  new=RAISE
old=FOLD       n_FF      n_FC      n_FH      n_FB      n_FR
old=CALL       n_CF      n_CC      n_CH      n_CB      n_CR
old=CHECK      n_HF      n_HC      n_HH      n_HB      n_HR
old=BET        n_BF      n_BC      n_BH      n_BB      n_BR
old=RAISE      n_RF      n_RC      n_RH      n_RB      n_RR
```

Diagonal = agreement; off-diagonal = shifts by direction.

### 4.4 Sizing drift (BET/RAISE diagonal)

For spots where `old_action == new_action ∈ {BET, RAISE}`:

**BET bins (per audit SPEC §5.3):**
| street | small | medium | large | overbet |
|---|---|---|---|---|
| flop | ≤30% | 30-50% | 50-80% | >80% |
| turn | ≤40% | 40-65% | 65-100% | >100% |
| river | ≤40% | 40-65% | 65-100% | >100% |

**RAISE bins (any street):** 2-2.5x, 2.5-3.5x, 3.5-5x, >5x.

`sizing_drift_rate` = count(same_action_diff_bin) / count(same_action_BET_or_RAISE).

Per-spot: `sizing_drift = (old==new ∈ {BET,RAISE}) AND (old_bin ≠ new_bin)`.

### 4.5 Opus tiebreaker (drift hands only)

Per `feedback_solver_vs_expert_labels.md`, Opus-Verify is a poker-judgment
oracle that classifies drift as "real shift" vs "noise" but does NOT
rewrite either old or new consensus.

- `opus_aligns_with == "new"` → drift validated (real shift).
- `opus_aligns_with == "old"` → drift rejected (counts toward "Opus rejected" gate metric, audit SPEC §6.2).
- `opus_aligns_with == "neither"` → both flagged; spot enters solver-verify queue per `feedback_solver_verification_queue.md`.

### 4.6 Stratification + statistical tests

**Chi-square goodness-of-fit (drift concentration):**
H0: drift is uniformly distributed across stratification cells (proportional to sample).
- Compute joint cell distribution (pos × ctx × street × tex) for sample, drift-hand sub-sample, agree-hand sub-sample.
- Test sub-sample vs expected proportional draw.
- Cells with expected count < 1 pooled into "rare" bucket (standard practice).
- Report chi² statistic + dof + p-value.
- If p < 0.05 ⇒ drift is **concentrated**; emit cell-level breakdown.

**McNemar's test (net direction symmetry):**
- 2×2 paired-binary table: (under→over flips) b vs (over→under flips) c.
- χ²_McNemar = (|b - c| - 1)² / (b + c).
- Tests whether shift direction is symmetric across the audit sample.
- If p < 0.05 ⇒ one direction systematically dominates ⇒ AMENDMENT-3-induced bias.

Both reported in the FULL drift report; chi² alone in pilot (McNemar is
underpowered at N=20).

**Cell-level drift breakdown (FULL only):** per populated cell —
cell_count, drift_count, drift_rate, direction breakdown. Cells with
drift_rate > 2× global drift_rate flagged "**HOT**".

**Tail-cell coverage (FULL only):** cells in 4-D space with 0 audit
samples → "no signal available" (insufficient power).

### 4.7 Gate decision

Emit `gate_decision` in report frontmatter per audit SPEC §6.2 thresholds:

**Pilot (N=20):** all four metrics in accept → `PASS`; ≥1 in reject →
`HALT`; otherwise → `MIDDLE — orchestrator-arbitrates`.

**Full (N=80):** same logic; thresholds from audit SPEC §6.2 full table.

Analyzer does NOT decide HALT-vs-revise; orchestrator scope per
`feedback_orchestrator_decides_not_recommends.md`. Analyzer's job is
metric computation + gate-state surfacing.

## 5. Edge cases

| # | Case | Behavior |
|---|---|---|
| 5.1 | Missing Opus verdict on a drift hand | **BLOCK** (exit 2); error: `"drift hand {spot_id} has no Opus-Verify record; re-run Opus-Verify before generating report"`. Hard block — audit cannot gate without complete Opus coverage on drift hands. |
| 5.2 | spot_id mismatch between old/new | **ERROR** (exit 3); message: `"spot_id mismatch — old has N1 spots, new has N2; symdiff={ids}; check pipeline integrity"`. |
| 5.3 | Legacy `state` key in old (batches 002..007) | **WARN** to stderr: `"legacy 'state' key in {file}:{line}; resolved as consensus_state per loader fallback"`. Does NOT block. If new file uses legacy key, WARN there too (pipeline-writer bug to investigate). |
| 5.4 | Missing sizing on a BET/RAISE diagonal hand | **WARN**: spot included in `agree` count but excluded from `sizing_drift_rate` denominator. |
| 5.5 | Illegal action transition (§4.2 `(illegal)` cells, e.g. FOLD→CHECK) | **WARN**: `"illegal action transition {old}→{new} for {spot_id}; possible labeller-output corruption — flagged for owner-arb"`. Spot in shift count with `drift_direction = "illegal"`; surfaced in dedicated illegal-transitions section. |
| 5.6 | Opus verdict "neither" (Opus disagrees with both) | Spot's `opus_aligns_with == "neither"` is NOT counted as "Opus-rejected" (gate metric counts only `"old"` verdicts). Spot added to `solver_verify_pending.jsonl` per `feedback_solver_verification_queue.md`. |

## 6. Acceptance test (synthetic data)

Builder authors `tests/test_drift_analyzer.py`. Architect produces the
golden synthetic inputs + expected drift_detail JSONL.

### 6.1 Test scenarios

| # | Scenario | Expected |
|---|---|---|
| T1 | All 20 spots agree | drift_rate=0, balanced, gate=PASS |
| T2 | 3 shifts: 2 CALL→FOLD, 1 BET→CHECK | drift_rate=15%, under-aggress=3, gate=PASS (accept boundary) |
| T3 | 7 shifts all CALL→RAISE | drift_rate=35%, over-aggress=7, gate=HALT |
| T4 | 5 shifts mixed: 2 CALL→RAISE, 3 BET→CHECK | drift_rate=25%, balanced ±1, gate=MIDDLE |
| T5 | Drift hand missing Opus verdict | exit 2, no report |
| T6 | spot_id mismatch between old/new | exit 3, no report |
| T7 | Legacy `state` on 3 of 20 | WARN to stderr, report still emitted |
| T8 | BET→BET, medium→large bin | sizing_drift counts 1 |
| T9 | BET→BET, same bin | sizing_drift excludes |
| T10 | FOLD→CHECK (illegal) | WARN, illegal-transitions section populated |
| T11 | Opus verdict "neither" | spot in solver_verify_pending, not in opus-rejected count |
| T12 | All 6 drifts in one cell | chi² flags concentration, HOT cell tagged |

### 6.2 Bit-exact reproducibility

`test_synthetic_recovers_drift_exactly`: given a fixed synthetic input
with hand-coded drift (3 shifts known directions, 2 sizing drifts), the
analyzer's `drift_detail.jsonl` MUST be byte-identical to a checked-in
golden file. Locks the implementation against silent behavior changes.

### 6.3 Optional: property-based test

Hypothesis-style invariants:
- `len(drift_detail) == len(old_consensus) == len(new_consensus)`
- agree-count + shift-count == N
- every shift has an Opus record (or analyzer blocks)
- every `drift_direction in {"under-aggress","over-aggress","lateral","illegal", null}`

## 7. CLI contract

```
python3 -m river_rats_core.drift_analyzer \
  --old data/4way_corpus/audit_amendment3/old_consensus_pilot.jsonl \
  --new data/4way_corpus/audit_amendment3/pilot/consensus.jsonl \
  --opus data/4way_corpus/audit_amendment3/pilot/opus_verify.jsonl \
  --sample {pilot|full} \
  --output-detail data/4way_corpus/audit_amendment3/pilot/drift_detail.jsonl \
  --output-report review/comms/DRIFT_REPORT_PILOT_AMENDMENT3_<DATE>.md
```

Exit codes:
- 0 — report emitted; gate decision in frontmatter
- 1 — unexpected failure (stack trace to stderr)
- 2 — BLOCK (missing Opus on drift hand)
- 3 — ERROR (spot_id mismatch)

## 8. Constraints (per project memory)

- **Read-only on corpus**: analyzer writes only to declared output paths. Never touches `data/4way_corpus/full_700/`.
- **No consensus writes**: Opus-Verify is poker-judgment oracle, NOT a training label (`feedback_solver_vs_expert_labels.md`). Analyzer never rewrites old or new consensus.
- **Provenance docstring**: `river-rats-core/drift_analyzer.py` MUST include top-of-file docstring linking the SHA that produced any emitted artifact (training-provenance addendum 2026-04-15).

## 9. Out of scope (deferred to v2)

- Multi-amendment drift composition (A∪B amendment combinatorics)
- Cross-batch drift over Phase 2-E (this audit is single-snapshot)
- Continuous sizing distance metric (KL or Wasserstein on % pot distribution); v1 uses bin-change drift only

## 10. Builder ratification checklist

- [ ] §2 input schemas match upstream files (legacy `batch_*_consensus.jsonl` + new `consensus.jsonl` + `opus_verify.jsonl`)
- [ ] §3.1 drift_detail schema complete; every field derived per §4
- [ ] §3.2 report schema matches audit SPEC §7.1 / §7.2
- [ ] §4.1 agree/shift = action-only (sizing handled separately, §4.4)
- [ ] §4.2 direction matrix covers all 5×5; `(illegal)` cells per §5.5
- [ ] §4.4 sizing bins match audit SPEC §5.3 exactly
- [ ] §4.5 Opus tiebreaker = poker-judgment only; no consensus writes (`feedback_solver_vs_expert_labels.md`)
- [ ] §4.6 chi² + McNemar's tests defined; cell-level breakdown + tail coverage produce right sections
- [ ] §4.7 gate decision matches audit SPEC §6.2 thresholds
- [ ] §5 all six edge cases handled (block / error / warn)
- [ ] §6 12 test scenarios + golden synthetic file checked in by architect
- [ ] §7 CLI contract + exit codes explicit
- [ ] §8 constraints honored (read-only, no consensus writes, provenance docstring)

End DRAFT.
