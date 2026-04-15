---
date: 2026-04-15
from: Builder (Programmer)
to: Main terminal / Owner
re: Track 2 — FB-40 / MW-50 re-eval with hardened harness
status: PARTIAL — dtype guard landed; eval execution BLOCKED on v2.2-harness mismatch
supersedes: n/a
---

# Track 2 — EVAL rerun with hardened harness

## TL;DR

- Dtype guard extension requested by `MAIN_TERMINAL_UPDATE_2026-04-15-c.md` §1
  **landed, test-first, all green.** 4 new regression tests in
  `test_harness_feature_completeness.py::TestDtypeGuard` (16/16 pass).
- Feature-shape mismatch blocks the FB-40 / MW-50 rerun:
  **the hardened harness `reference_evaluator.py` is built for a 54-feature
  model (v8/v9-baseline), but the v2.2 model expects 108 features
  (54 raw + 54 `attn_*`).**
- No 54-feature-width model ships in `river-rats-core/models/`; the only
  action-classifier there is `v2_2_model.json` (108-wide) and
  `gto_model_v9_3way_v2.2.json` (45-wide).
- The v2.2 evaluation script that produced the 72.5% (FB-40) and 80.0%
  (MW-50) figures is **not in the repo** — same absence flagged by Track 3.5
  (`ANOMALY_A_VERIFICATION_2026-04-15.md`: "v2.2 trainer missing from repo").
- Stop condition triggered: *"If the harness API differs from what Track 1
  implemented — STOP, report BLOCKED."* Reporting blocked before committing
  any eval numbers, so we don't publish results from a silently-wrong path.

## 1. Dtype-guard extension — DONE

### 1.1 Tests (test-first)

Added to `river-rats-core/tests/test_harness_feature_completeness.py` a new
`TestDtypeGuard` class with 4 tests:

| Test | Asserts |
|---|---|
| `test_string_value_in_numeric_slot_raises_type_error` | `features_from_dict()` raises `TypeError` naming `street` when `street='flop'` leaks in (simulates the BP-generator ANOMALY-A serialisation bug). |
| `test_validate_feat_dict_rejects_string_value` | `_validate_feat_dict()` raises `ValueError` naming both the hand id and the offending column (`hero_position='BTN'`). |
| `test_bool_value_is_permitted` | Boolean flags produced by `extract_all_features` (`is_made_hand`, `has_flush_draw`) are treated as numeric and do NOT trigger the guard — required to avoid breaking the happy path. |
| `test_none_value_is_rejected` | `None` in a numeric slot is caught by the same guard. |

Before guard implementation: 3 of 4 failed as intended (the bool test passed
vacuously). After implementation: 16/16 pass. Full
`test_harness_feature_completeness.py` suite green (up from 12 to 16 tests).

### 1.2 Implementation

- `river-rats-core/gto_model.py::GtoOracle.features_from_dict`
  after the existing completeness check, iterate the 54 columns and raise
  `TypeError` listing every non-numeric value (excluding `bool` — it is a
  numeric subtype and emitted by the extractor for flags).
- `river-rats-core/reference_evaluator.py::_validate_feat_dict`
  same check mirrored at the harness boundary, raising a `ValueError` that
  includes the hand id.

Both error messages point the operator at `extract_all_features()` and
warn specifically against raw serialisation dicts carrying string codes
like `street='flop'` — the ANOMALY-A failure mode.

### 1.3 Regression surface

Full-core suite: `1047 passed, 128 skipped, 14 failed` — **every one of
the 14 failures predates this change** (10 `test_oracle_router` failures
from missing v8 model files, 1 `test_attention_experiments` integration
skip, 3 `test_training_data_encoding` failures for the known ANOMALY-A
training CSV). Diff ran clean: guard introduces 0 new failures.

## 2. FB-40 / MW-50 eval execution — BLOCKED

### 2.1 Shape mismatch

```
>>> evaluate_facing_bet_test_set(oracle_path='models/v2_2_model.json')
correct: 0/40   accuracy: 0.0   skipped: 40
sample error: 'oracle predict: Feature shape mismatch, expected: 108, got 54'
```

`GtoOracle.features_from_dict` returns a `(54,)` array built from
`FEATURE_COLUMNS` (54 names, matching the v8/v9-baseline schema used by
`reference_evaluator.py`). The v2.2 model was trained on 108 features
(`54 raw + 54 attn_*`, per `PHASE_4_TRAINING_REPORT_2026-04-15.md` line 23
and `v2_2_evaluation_report.json:n_features=108`). Prediction at inference
requires `attn_*=1` expansion **plus** legal-action masking
(`facing_bet` → legal set) — per the Phase 4 report:

> Legal-action masking applied: when facing_bet=False, predictions
> restricted to CHECK/BET. When facing_bet=True, restricted to
> CALL/RAISE/FOLD. This is the standard oracle constraint and improves
> MW from 44% → 80%.

Neither the `attn_*` expansion nor the legal-action mask exists anywhere
in `reference_evaluator.py` or `gto_model.py`. The 72.5% / 80.0% figures
the directive asks me to reproduce were produced by a **different**
evaluation script — the one that is missing from the repo (same evidence
chain as Track 3.5's v2.2-trainer absence).

### 2.2 Why I did not improvise

Two things I could do instead, both rejected under `CLAUDE.md` stop-and-report:

1. **Build a 108-feature inference wrapper on the fly** (extract 54 raw
   features → extend with 54 `attn_*=1` ones → apply the legal-action
   mask → score v2.2). This would be writing a non-trivial new
   evaluation module and publishing accuracy numbers from it. That is
   the "improvise past a missing-script blocker" pattern the project
   has already flagged (`ANOMALY_A_VERIFICATION_2026-04-15.md`
   BLOCKED-ambiguity). If my reconstruction differs by one hand from
   the missing original's logic, I would incorrectly flag a regression.

2. **Evaluate v9-baseline (45-wide) or v9-3way** against FB-40 / MW-50.
   The 72.5% / 80.0% baseline is v2.2-specific; scoring a different
   model is not the requested verification and would muddy the Gate 7
   decision.

Both paths violate the "STOP and report BLOCKED if source differs from
expectations — do NOT improvise" rule.

### 2.3 What is needed to unblock

Any **one** of the following closes this out:

- **Option A:** Recover / rewrite the v2.2 evaluation script
  (depends on Track 3.5 follow-up — `V22_TRAINER_RECOVERY_2026-04-15.md`
  per `MAIN_TERMINAL_UPDATE_2026-04-15-c.md` §4 Branch B). The trainer
  and eval script are in the same missing-piece — likely live on an
  owner local machine.
- **Option B:** Owner confirms the Track 2 scope was only ever meant to
  verify the **54-feature harness hygiene**, not reproduce v2.2
  numerics; in that case the dtype-guard extension already delivered
  is the full deliverable.
- **Option C:** Explicit authorisation to write a 108-feature harness
  extension (`features_from_dict_v22` with `attn_*=1` expansion +
  legal-action masking), with the understanding that any numeric
  discrepancy vs the 72.5% / 80.0% baseline may come from harness
  reconstruction rather than real model change.

## 3. Per-hand comparison — not produced

Deliberately not included. Publishing a per-hand table from a harness that
errors on all 40 FB-40 hands and would need a reconstructed 108-feature
path for MW-50 would mislead reviewers. Table produced immediately on
unblock via one of the three options above.

## 4. Verdict

**STAND-BY — blocked on v2.2 eval-script recovery.**

Not a STAND and not a CHANGED — the test did not run. The dtype-guard
hygiene improvement is independent and shipped.

## 5. Files changed

- `river-rats-core/gto_model.py` (+18 lines: dtype guard in
  `features_from_dict`)
- `river-rats-core/reference_evaluator.py` (+20 lines: dtype guard in
  `_validate_feat_dict`)
- `river-rats-core/tests/test_harness_feature_completeness.py` (+64 lines:
  `TestDtypeGuard` class, 4 tests)

## 6. Suite result

```
16 passed   test_harness_feature_completeness.py   (was 12, +4 dtype)
1047 passed 128 skipped 14 failed (all 14 pre-existing, unrelated)
```
