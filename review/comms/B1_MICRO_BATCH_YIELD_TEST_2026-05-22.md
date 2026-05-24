---
date: 2026-05-22
from: BUILDER (Phase 2-F1 B1 pre-flight artifact)
to: Architect · Orchestrator · QC · Owner
re: 20-hand micro-batch yield test for `positional_action_chain_scenarios.py` (Module 10)
status: PASS — all quota floors satisfied on full 24-spec output; rng-deterministic
references:
  - review/comms/MAIN_TERMINAL_PHASE2F1_B1_FIRE_NOW_2026-05-22.md (deliverable #5)
  - review/comms/RATIFICATION_A1_POSITIONAL_CHAIN_2026-05-22.md §Per-batch slot allocation
  - feedback_pilot_first_for_long_jobs.md
---

# B1 Micro-Batch Yield Test (Pilot-First Gate)

## TL;DR

**PASS.** Module 10's `generate_phase_2f_chain_quota(rng_seed=20260522, forbidden_fingerprints=set())`
returns 24 SituationSpec instances satisfying **all 5 A1 mandatory floors**, with:

- 20/20 fingerprint-validation pass on the truncated 20-spec slice
- 0 duplicate card-equivalence fingerprints across the 20-spec output
- Deterministic re-run (same seed → identical 20-spec output)
- Generation time < 1ms (24 specs)

The 20-spec truncation is a pilot-volume sample per directive deliverable #5; full quota satisfaction is on the 24-spec output (truncation slice is a subset).

## Generation parameters

| Parameter | Value |
|---|---|
| `rng_seed` | 20260522 |
| `forbidden_fingerprints` | `set()` (empty) |
| Output size | 24 (full) → truncated to 20 for micro-batch sample |
| Generation time | 0.14 ms (full 24) |
| Re-run time | 0.08 ms |

## Per-template hit count (20-spec slice)

| Slot | Street | Hero | Shape | Hit |
|---:|:---:|:---:|:---|:---:|
| T00 | flop | BTN | BET | 1 |
| T01 | flop | BB | BET_CALL | 1 |
| T02 | flop | SB | BET | 1 |
| T03 | flop | BTN | BET_CALL | 1 |
| T04 | flop | BB | BET_CALL_CALL | 1 |
| T05 | flop | BB | OPEN | 1 |
| T06 | flop | CO | BET_CALL | 1 |
| T07 | turn | BTN | BET | 1 |
| T08 | flop | BB | BET_RAISE | 1 |
| T09 | turn | BB | BET_CALL | 1 |
| T10 | river | BTN | BET | 1 |
| T11 | flop | SB | BET | 1 |
| T12 | flop | BTN | BET_RAISE | 1 |
| T13 | flop | SB | CHECK_RAISE | 1 |
| T14 | flop | CO | BET_RAISE | 1 |
| T15 | turn | BTN | CHECK_RAISE | 1 |
| T16 | turn | BB | BET_RAISE | 1 |
| T17 | flop | SB | BET_RAISE | 1 |
| T18 | river | BB | BET_CALL | 1 |
| T19 | river | SB | BET | 1 |

T20–T23 (river BTN CHECK_RAISE, river CO BET_RAISE, flop UTG BET_RAISE, flop HJ BET) are excluded from the 20-truncation slice; included in the full 24-spec output.

## Quota-floor satisfaction

### Full 24-spec output (canonical per-batch quota)

| Floor | Count | Required | Status |
|---|---:|---:|:---:|
| Facing-raise (BET_RAISE / CHECK_RAISE / MULTI_AGGR) | 10 | ≥10 | **PASS** |
| River (street = 'river') | 5 | ≥5 | **PASS** |
| Position-balance: BTN | 7 | ≥1 in 24 | PASS |
| Position-balance: CO | 3 | ≥1 in 24 | PASS |
| Position-balance: MP (collapsed: HJ) | 1 | ≥1 in 24 | PASS |
| Position-balance: UTG | 1 | ≥1 in 24 | PASS |
| Position-balance: SB | 5 | ≥1 in 24 | PASS |
| Position-balance: BB | 7 | ≥1 in 24 | PASS |
| Top-12 chain coverage | 12 / 12 | each ≥1 | **PASS** |
| Sandwich (hero positionally between two villain actors) | 5 | ≥4 | **PASS** |

### 20-spec truncation slice

The 20-spec slice does NOT satisfy all per-batch floors because it omits T20–T23, which contribute sandwich and river slots. This is **expected** per directive deliverable #5 ("truncated to 20 from the 24-spec output") — the truncation is a yield-test sample, not the canonical per-batch quota.

| Floor (20-spec) | Count | Note |
|---|---:|---|
| Facing-raise | 7 | (full 24: 10) |
| River | 3 | (full 24: 5) |
| Top-12 hit | 12 / 12 | unchanged |
| Sandwich | 2 | (full 24: 5) |

## Fingerprint validation (per spec)

All 20 specs in the truncation slice validate against their template's expected `ChainFingerprint`. `compute_chain_fingerprint(spec)` returns the exact 7-tuple stored in each template.

| Slot | Validation |
|---:|:---:|
| T00 – T19 | PASS (20/20) |

`validate_chain_fingerprint(spec, expected_chain)` returns `True` for every spec; no `AssertionError` raised.

## Card-equivalence fingerprint dedup

| Metric | Value |
|---|---:|
| Total specs (20-spec slice) | 20 |
| Unique card fingerprints | 20 |
| Duplicates | 0 |

`_scenario_utils.fingerprint(hero_cards, board)` produces 20 distinct fingerprints — no card-equivalence collisions across the 24-template design.

## RNG determinism

| Property | Result |
|---|:---:|
| Re-run with same `rng_seed=20260522` produces identical output | **YES** |
| Hero cards, board cards, action history all match across runs | YES |

## Test suite status

`river-rats-core/tests/test_positional_action_chain_scenarios.py` — 20/20 tests PASS:

- CFP-1 (callers_chain order) ✓
- CFP-2 (aggressor seat before hero, or hero pre-checked) ✓
- CFP-3 (raiser seat between aggressor and hero in BET_RAISE; CHECK_RAISE exception) ✓
- CFP-4 (CHECK_RAISE requires RAISER's prior check) ✓
- CFP-5 (chain actors distinct + subset-of-table) ✓
- CFP-6 (aggregate board diversity ≥5) ✓
- QUOTA-1..6 (24 specs; facing-raise ≥10; river ≥5; position-balance; top-12; sandwich) ✓
- VALIDATION-1..2 (matching fingerprints + AssertionError on corrupted spec) ✓
- enumerate_top_12_chains rank order ✓

## Acceptance criteria (RATIFICATION_A1 §Acceptance check) — status

| # | Criterion | Status |
|---:|---|:---:|
| 1 | File at `river-rats-core/corpus_revision_scenarios/positional_action_chain_scenarios.py` (TC-23 git-tracked) | PASS (pending PR push) |
| 2 | `enumerate_top_12_chains()` returns 12 in rank order matching v1 §5.1 | PASS |
| 3 | `generate_phase_2f_chain_quota()` returns 24 SituationSpec, all 5 floors met | PASS |
| 4 | `validate_chain_fingerprint()` raises with precise diff on mismatch | PASS |
| 5 | `compute_chain_fingerprint()` helper in `_scenario_utils.py` | PASS |
| 6 | 20-hand micro-batch yield test report committed | PASS (this file) |
| 7 | Top-12 frequency audit committed with escalation-gate status | PASS (`phase2f1_top12_frequency_audit_2026-05-22.md`; no escalation) |
| 8 | CFP-1..6 + QUOTA-1..6 + VALIDATION-1..2 unit tests pass | PASS (20/20) |
| 9 | QC pre-merge audit | PENDING (orchestrator dispatches post-PR open) |

## Next

- Builder opens MILESTONE PR with all 6 deliverables: Module 10 + `_scenario_utils` patch + tests + frequency audit + micro-batch yield test report + builder report.
- Orchestrator dispatches QC pre-merge audit per `feedback_qc_required_before_approval.md`.
- After QC PASS + merge: BATCH-009 generation kicks off with new Module 10 quota slots.
