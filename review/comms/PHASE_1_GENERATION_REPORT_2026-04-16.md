# Phase 1 — v2.3 Factory Generation Report

**Date:** 2026-04-16
**Builder:** River Rats v2 programmer subagent
**Scope:** 10 factory buckets (rows 1-5, 8, 9, 10, 12, U of V23_HAND_GENERATION_PLAN §1.2)
**Outputs:** `training-data/v23_<bucket>.jsonl` × 10

Rows 6, 7 (curated draws) and row 11 (solver-sourced mixed-zone) are NOT in this
scope — separate tracks per the plan.

---

## 1. Per-bucket results

| bucket       | BP (net) | OS (overshoot) | generated | build_failures | predicate_failures | written | validated_clean | meet_BP |
|--------------|---------:|---------------:|----------:|---------------:|-------------------:|--------:|----------------:|:-------:|
| MM_IP_TURN   |       30 |             38 |        38 |              0 |                  0 |      38 |              38 |   YES   |
| MM_IP_FLOP   |       15 |             19 |        19 |              0 |                  0 |      19 |              19 |   YES   |
| MM_OOP_TURN  |       20 |             25 |        25 |              0 |                  0 |      25 |              25 |   YES   |
| SM_IP_TURN   |       20 |             25 |        25 |              0 |                  0 |      25 |              25 |   YES   |
| SM_IP_RIVER  |       15 |             19 |        19 |              0 |                  0 |      19 |              19 |   YES   |
| MON_CHECKED  |       15 |             19 |        19 |              0 |                  0 |      19 |              19 |   YES   |
| RAISE_VALUE  |       20 |             25 |        25 |              0 |                  0 |      25 |              25 |   YES   |
| PROT_DANGER  |       16 |             20 |        20 |              0 |                  0 |      20 |              20 |   YES   |
| PFR_CONT     |       20 |             25 |        25 |              0 |                  0 |      25 |              25 |   YES   |
| UMBRELLA     |      214 |            268 |       268 |              0 |                  0 |     268 |             268 |   YES   |
| **TOTAL**    |  **385** |        **483** |   **483** |          **0** |              **0** | **483** |         **483** |   —     |

- `BP net` = net hands required after the `num_opponents` validator.
- `OS` = overshoot target (25% over BP per plan §1.2).
- `build_failures` = `build_situation()` raised a `ValueError` (typically the
  `num_opponents` validator). Zero across all buckets.
- `predicate_failures` = UMBRELLA-only — records where the Section 2 predicate
  (`facing_bet=0 ∧ num_opponents=2 ∧ villain_checked_back=1 ∧
  villain_range_capped=1 ∧ worse_hand_pct≥0.55 ∧ equity_vs_range≥0.35 ∧
  SPR≤2.0`) did not pass. Zero after reordering villain_positions so the
  non-opener is primary and restricting UMBRELLA to turn/river.
- `validated_clean` = post-build `validate_situation()` reported no errors.

**Validator failure rate:** 0/483 = **0.0%** (stop condition: >25% → none tripped).
**BP shortfall:** none. Every bucket hits OS target exactly; net (all records
validated) ≥ BP target.

---

## 2. Schema preflight per JSONL

Ran `_preflight_schema_check_file()` (same semantics as
`train_model._preflight_schema_check`) against each of the 10 JSONLs:

| file                          | errors |
|-------------------------------|-------:|
| v23_mm_ip_turn.jsonl          |      0 |
| v23_mm_ip_flop.jsonl          |      0 |
| v23_mm_oop_turn.jsonl         |      0 |
| v23_sm_ip_turn.jsonl          |      0 |
| v23_sm_ip_river.jsonl         |      0 |
| v23_mon_checked.jsonl         |      0 |
| v23_raise_value.jsonl         |      0 |
| v23_prot_danger.jsonl         |      0 |
| v23_pfr_cont.jsonl            |      0 |
| v23_umbrella_fill.jsonl       |      0 |
| **TOTAL**                     |  **0** |

All `street` and `hero_position` values are numeric (0/1/2 and 0-5
respectively) across all 483 rows. `normalise_situation()` piped every
record at the serialisation boundary per §1.3.

Sample round-trip verification (first row of `v23_mm_ip_turn.jsonl`):
- `street`: `int` 1  (turn)
- `hero_position`: `int` 3  (BTN)
- `villain_positions`: `['SB', 'BB']`  (length 2, preserved as string list
  for teaching metadata — not normalised per batch5 convention)
- `action_string`: `"SB check, BB check, BTN ???"`
- `num_opponents`: 2
- `has_errors`: false

UMBRELLA predicate verification (disk-level re-check): 268/268 pass.

---

## 3. Test suite

Created `river-rats-core/tests/test_generate_factory_batch6.py` with 4 tests
per plan §1.3 "Test-first":

```
tests/test_generate_factory_batch6.py::test_num_opponents_set_on_every_spec       PASSED
tests/test_generate_factory_batch6.py::test_feat_dict_has_required_metadata       PASSED
tests/test_generate_factory_batch6.py::test_records_are_normalised                PASSED
tests/test_generate_factory_batch6.py::test_mm_ip_turn_action_history_is_checked_to PASSED
```

Tests were written BEFORE the generator (test-first per CLAUDE.md §3).
Initial run: 4 skipped (module absent). Post-build run: 4 passed.

---

## 4. Implementation notes / deviations

### 4.1 UMBRELLA predicate fix

First-pass generation produced 100% UMBRELLA predicate failures because:

1. **Flop street cannot satisfy `villain_checked_back=1`** — the feature is
   set from prior-street checks only, and flop has no prior street.
   Mitigation: UMBRELLA generates turn + river only.
2. **Primary villain default = `villain_positions[0]`** — in archetypes where
   the opener was first in the villain list, the bridge's not-facing-bet
   primary-villain resolution picked the opener, making
   `villain_range_capped=0` (opener is not a defender).
   Mitigation: reorder `villain_positions` so the NON-opener comes first.

Both fixes are local to `build_UMBRELLA_specs()`. No other buckets were
affected because their predicate expectations are trivially satisfied by the
straightforward `villain_positions=[SB, BB]` pattern where neither villain
is the PFR opener (hero-is-PFR-CO-type archetypes).

Re-run after fix: 268/268 predicate pass. Zero build failures.

### 4.2 RAISE_VALUE architecture

RAISE_VALUE is the only facing-bet bucket. Split into two sub-patterns:

- **IP hero** facing flop/turn bet: earlier villains check, last villain
  (the bettor) bets. `villain_positions` ends with the bettor.
- **OOP hero** facing turn bet (turn check-raise pattern): flop checks
  through; on turn, hero checks first; last villain bets. OOP flop would
  require a "donk from an earlier seat", but hero IS earliest (SB/BB), so
  OOP flop RAISE_VALUE is skipped. The OOP turn pattern yields the plan's
  required raise-over-bet context.

### 4.3 Hand-strength definitions (canonical anchor)

Per the plan, MM/SM/MONSTER categorisation uses
`hand_evaluator.evaluate_hand(...).category` directly. Tiers:

- **MONSTER**: `trips`, `set`, `straight`, `flush`, `full_house`, `quads`,
  `straight_flush`
- **STRONG_MADE**: `top_pair_good_kicker`, `top_pair_top_kicker`, `overpair`,
  `two_pair`
- **MEDIUM_MADE**: `top_pair` (weak kicker), `mid_pair`/`middle_pair`,
  `low_pair`/`bottom_pair`, `underpair`, `pair`

These match `hand_categories.HAND_CATEGORY_VALUES` exactly.

### 4.4 SPR constraint

`feature_extractor` computes `spr = 100.0 / pot_size` (fixed
DEFAULT_EFFECTIVE_STACK of 100bb). With `pot=90`, all records land at
`spr ≈ 1.11` — within the plan's SPR 1-2 target range for MM/SM buckets
and within SPR≤2.0 for UMBRELLA.

### 4.5 Metadata preserved

Every record carries the §1.3 required fields:
`villain_positions`, `hero_position` (numeric), `action_string`, `street`
(numeric), plus: `num_opponents=2`, `bucket`, `sub_pattern`, `hero_cards`,
`board_cards`, `description`, `has_errors`, `situation_id`.

---

## 5. Stop conditions check

| condition                                                     | tripped? |
|---------------------------------------------------------------|----------|
| batch5 pattern depends on removed utility                     | no       |
| `num_opponents` validator fires on >25% of specs              | no (0%)  |
| Any bucket `validated_clean < BP * 0.9`                        | no       |
| Generator crashed partway                                     | no       |
| hand_categories ambiguous for a hero-strength sub-pattern     | no       |

None tripped. Generation proceeded clean end-to-end.

---

## 6. Deliverables

- `review/generate_factory_batch6.py` — parameterised generator, 10 buckets.
- `river-rats-core/tests/test_generate_factory_batch6.py` — 4 tests, all pass.
- `training-data/v23_mm_ip_turn.jsonl`      (38 records)
- `training-data/v23_mm_ip_flop.jsonl`      (19 records)
- `training-data/v23_mm_oop_turn.jsonl`     (25 records)
- `training-data/v23_sm_ip_turn.jsonl`      (25 records)
- `training-data/v23_sm_ip_river.jsonl`     (19 records)
- `training-data/v23_mon_checked.jsonl`     (19 records)
- `training-data/v23_raise_value.jsonl`     (25 records)
- `training-data/v23_prot_danger.jsonl`     (20 records)
- `training-data/v23_pfr_cont.jsonl`        (25 records)
- `training-data/v23_umbrella_fill.jsonl`   (268 records)
- **Total:** 483 hands across 10 buckets — exactly OS target.

---

## 7. Overall verdict

**Rows 1-5, 8, 9, 10, 12, U delivered: YES.**

- Every bucket hits BP + 25% overshoot (OS).
- `num_opponents` validator failure rate: 0.0%.
- Schema preflight: 0 errors across all 10 JSONLs.
- UMBRELLA predicate compliance: 100% (268/268).
- 4/4 tests pass.

No flags. No blockers. Ready for Phase 2 (labelling).
